"""Model transports only: cached MLX weights or a bounded OpenAI API call."""
import json
import os
from pathlib import Path
import time
import urllib.request
from jsonschema import Draft202012Validator
from task import CASE_DIR, BudgetStop, ProviderFailure

MODELS = {
    "qwen3-32b": ("mlx-community/Qwen3-32B-4bit",
                   "bcaaf7f538adf166c1080a2befdb4f6019f66639"),
    "qwen": ("mlx-community/Qwen2.5-1.5B-Instruct-4bit",
             "8b403126fc14f14cfc99bb4cfa72ecbc129ea677"),
    "gemma": ("mlx-community/gemma-2-2b-it-4bit",
              "2c715097ff9c081a6ac1e5cd239e2ac756b5bd99"),
    "qwen3": ("mlx-community/Qwen3-4B-4bit",
              "4dcb3d101c2a062e5c1d4bb173588c54ea6c4d25"),
    "qwen3-8b": ("mlx-community/Qwen3-8B-4bit",
                 "545dc4251c05440727734bcd94334791f6ab0192"),
}


LIMITS = {"iterations": 3, "calls": 35, "output_tokens": 1024,
          "context_tokens": 4096, "total_tokens": 50000,
          "seconds": 900, "mlx_memory_bytes": 12 * 1024**3,
          "mlx_cache_bytes": 256 * 1024**2}


def parse_reply(text, schema):
    """Accept a bare JSON object or one enclosing JSON fence; never repair content."""
    content = text.strip()
    if content.startswith("```json\n") and content.endswith("```"):
        content = content[8:-3].strip()
    try:
        value = json.loads(content)
    except (ValueError, TypeError):
        return None, "invalid_json"
    if list(Draft202012Validator(schema).iter_errors(value)):
        return None, "invalid_schema"
    return value, None


def messages_for(key, instructions, payload, schema):
    contract = instructions + "\nDevuelve únicamente un objeto JSON que cumpla este esquema:\n" + json.dumps(schema, ensure_ascii=False)
    data = json.dumps(payload, ensure_ascii=False)
    if key == "gemma":
        # Gemma 2's native template does not support the system role.
        return [{"role": "user", "content": contract + "\n\nDatos de entrada:\n" + data}]
    return [{"role": "system", "content": contract}, {"role": "user", "content": data}]


def encode_chat(tokenizer, messages, key, *, thinking=False):
    """Render first: Transformers 5 can return a mapping when tokenize=True."""
    options = {"enable_thinking": thinking} if key.startswith("qwen3") else {}
    rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, **options)
    tokens = tokenizer.encode(rendered, add_special_tokens=False)
    if not isinstance(tokens, list) or not all(type(token) is int for token in tokens):
        raise ValueError("Expected native token IDs")
    return tokens


class LocalClient:
    def __init__(self, key, directory, snapshot, started, *, sampling=None, limits=None):
        import mlx.core as mx
        from mlx_lm import load
        self.limits = dict(LIMITS if limits is None else limits)
        self.sampling = dict(sampling or {"temperature": 0.0, "top_p": 1.0, "top_k": 0, "seed": 42})
        self.mx, self.key, self.directory = mx, key, directory
        self.started, self.calls, self.tokens = started, 0, 0
        mx.set_memory_limit(self.limits["mlx_memory_bytes"])
        mx.set_cache_limit(self.limits["mlx_cache_bytes"])
        mx.random.seed(self.sampling["seed"])
        mx.reset_peak_memory()
        self.model, self.tokenizer = load(str(snapshot), tokenizer_config={"trust_remote_code": False})
        self.load_seconds = time.monotonic() - started

    def seed(self, value):
        self.mx.random.seed(value)

    def peak_memory(self):
        return self.mx.get_peak_memory() / 1e9

    def length(self, text):
        return len(self.tokenizer.encode(text, add_special_tokens=False))

    def output_processors(self, schema):
        """Allow an explicit decoding adapter without changing prompt-only runs."""
        return [], None

    def ask(self, role, instructions, payload, schema):
        from mlx_lm import stream_generate
        from mlx_lm.sample_utils import make_sampler
        messages = messages_for(self.key, instructions, payload, schema)
        thinking = self.sampling.get("enable_thinking", False)
        prompt = encode_chat(self.tokenizer, messages, self.key, thinking=thinking)
        reserve = len(prompt) + self.limits["output_tokens"]
        if (self.calls >= self.limits["calls"] or reserve > self.limits["context_tokens"]
                or self.tokens + reserve > self.limits["total_tokens"]
                or time.monotonic() - self.started >= self.limits["seconds"]):
            raise BudgetStop("Local inference limit reached")
        self.calls += 1
        entry = {"call": self.calls, "role": role, "messages": messages,
                 "input_tokens": len(prompt), "raw_output": ""}
        started = time.monotonic()
        result, error = None, None
        try:
            processors, processor_stats = self.output_processors(schema)
            if processor_stats is not None:
                entry["structured_generation"] = processor_stats
            for result in stream_generate(self.model, self.tokenizer, prompt=prompt,
                                          max_tokens=self.limits["output_tokens"],
                                          logits_processors=processors or None,
                                          sampler=make_sampler(temp=self.sampling["temperature"], top_p=self.sampling["top_p"], top_k=self.sampling["top_k"])):
                entry["raw_output"] += result.text
                if getattr(self, "on_generation", None):
                    self.on_generation(entry["raw_output"], result.generation_tokens)
                if time.monotonic() - self.started >= self.limits["seconds"]:
                    raise BudgetStop("Local time limit reached")
            if result is None:
                raise ProviderFailure("No generation returned")
            answer = entry["raw_output"]
            if thinking:
                # Qwen's template opens the reasoning segment; keep the full trace,
                # but validate only the final answer after the closing delimiter.
                answer = answer.split("</think>", 1)[1].strip() if "</think>" in answer else ""
            value, error = parse_reply(answer, schema)
            if result.finish_reason != "stop":
                value, error = None, "output_limit"
            entry.update(parsed=value, error=error, finish_reason=result.finish_reason)
            return value, error
        except (BudgetStop, ValueError, RuntimeError) as exc:
            entry.update(error=type(exc).__name__, finish_reason="interrupted")
            raise
        finally:
            output_tokens = result.generation_tokens if result else 0
            self.tokens += len(prompt) + output_tokens
            entry.update(output_tokens=output_tokens, elapsed_seconds=time.monotonic() - started,
                         peak_mlx_gb=self.mx.get_peak_memory() / 1e9)
            with (self.directory / "calls.jsonl").open("a") as file:
                file.write(json.dumps(entry, ensure_ascii=False) + "\n")
            self.mx.clear_cache()


class ApiClient:
    """Same search interface, with strict JSON and bounded usage; no retries."""
    def __init__(self, key, directory, snapshot, started, *, sampling, limits):
        from dotenv import load_dotenv
        load_dotenv(CASE_DIR / '.env', override=False)
        import tiktoken
        if not os.environ.get('OPENAI_API_KEY'):
            raise ValueError('Set OPENAI_API_KEY in the environment')
        self.model = key
        self.directory, self.started = Path(directory), started
        self.sampling, self.limits = dict(sampling), dict(limits)
        self.calls = self.tokens = 0
        self.cost = 0.0
        self.uncertain = False
        self.tokenizer = tiktoken.encoding_for_model(key)

    def seed(self, value):
        pass  # Responses API has no paired seed parameter.

    def peak_memory(self):
        return None

    def length(self, text):
        return len(self.tokenizer.encode(text))

    def ask(self, role, instructions, payload, schema):
        if self.uncertain:
            raise ProviderFailure('Previous usage is uncertain; no further calls')
        messages = messages_for('api', instructions, payload, schema)
        body = {'model': self.model, 'input': messages, 'store': False,
                'temperature': self.sampling['temperature'],
                'max_output_tokens': self.limits['output_tokens'],
                'text': {'format': {'type': 'json_schema', 'name': role, 'strict': True, 'schema': schema}}}
        raw = json.dumps(body, ensure_ascii=False).encode()
        # Bytes plus framing allowance conservatively reserve input usage.
        incoming = len(raw) + 4096
        reserve = incoming + self.limits['output_tokens']
        cost = (incoming * .15 + self.limits['output_tokens'] * .60) / 1e6
        if (self.calls >= self.limits['calls'] or reserve > self.limits['context_tokens']
                or self.tokens + reserve > self.limits['total_tokens']
                or self.cost + cost > .50 or time.monotonic() - self.started >= self.limits['seconds']):
            raise BudgetStop('API budget reached')
        self.calls += 1
        self.tokens += reserve
        self.cost += cost
        entry = {'call': self.calls, 'role': role, 'messages': messages,
                 'reserved_tokens': reserve, 'reserved_cost_usd': cost}
        start = time.monotonic()
        try:
            request = urllib.request.Request('https://api.openai.com/v1/responses', data=raw,
                headers={'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'], 'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=min(60, max(1, self.limits['seconds'] - (start - self.started)))) as response:
                data = json.load(response)
            usage = data['usage']
            input_tokens, output_tokens = usage['input_tokens'], usage['output_tokens']
            if any(type(n) is not int or n < 0 for n in (input_tokens, output_tokens)):
                raise ValueError('Invalid provider usage')
            actual = (input_tokens * .15 + output_tokens * .60) / 1e6
            self.tokens += input_tokens + output_tokens - reserve
            self.cost += actual - cost
            entry.update(input_tokens=input_tokens, output_tokens=output_tokens, estimated_cost_usd=actual)
            if input_tokens + output_tokens > reserve or actual > cost:
                raise ValueError('Usage exceeded reservation')
            text = ''.join(p.get('text', '') for item in data.get('output', []) if item.get('type') == 'message'
                           for p in item.get('content', []) if p.get('type') == 'output_text')
            value, error = parse_reply(text, schema)
            if data.get('status') != 'completed':
                value, error = None, 'incomplete_response'
            entry.update(raw_output=text, parsed=value, error=error, finish_reason=data.get('status'),
                         response_id=data.get('id'), model=data.get('model'))
            return value, error
        except Exception as exc:
            self.uncertain = True
            entry.update(error=type(exc).__name__, usage_uncertain=True)
            raise ProviderFailure('API request failed; no retry; inspect the saved record') from None
        finally:
            entry['elapsed_seconds'] = time.monotonic() - start
            with (self.directory / 'calls.jsonl').open('a') as file:
                file.write(json.dumps(entry, ensure_ascii=False) + '\n')
