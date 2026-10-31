"""Bounded MLX inference test using cached, pinned models. No loading on import."""
import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import time

from jsonschema import Draft202012Validator

import harness_smoke_test as smoke
from prompt_search import (CASE_DIR, PROMPT_SCHEMA, REPLY_SCHEMA, get_prompt,
                           rule_check, visible, ProviderFailure, BudgetStop)

PROTOCOL = "case-0003-local-model-v2"
MODELS = {
    "qwen": ("mlx-community/Qwen2.5-1.5B-Instruct-4bit",
             "8b403126fc14f14cfc99bb4cfa72ecbc129ea677"),
    "gemma": ("mlx-community/gemma-2-2b-it-4bit",
              "2c715097ff9c081a6ac1e5cd239e2ac756b5bd99"),
    "qwen3": ("mlx-community/Qwen3-4B-4bit",
              "4dcb3d101c2a062e5c1d4bb173588c54ea6c4d25"),
}
LIMITS = {"iterations": 3, "calls": 23, "output_tokens": 1024,
          "context_tokens": 4096, "total_tokens": 50000,
          "seconds": 900, "mlx_memory_bytes": 8 * 1024**3,
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


def encode_chat(tokenizer, messages, key):
    """Render first: Transformers 5 can return a mapping when tokenize=True."""
    options = {"enable_thinking": False} if key == "qwen3" else {}
    rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, **options)
    tokens = tokenizer.encode(rendered, add_special_tokens=False)
    if not isinstance(tokens, list) or not all(type(token) is int for token in tokens):
        raise ValueError("Expected native token IDs")
    return tokens


class LocalClient:
    def __init__(self, key, directory, snapshot, started):
        import mlx.core as mx
        from mlx_lm import load
        self.mx, self.key, self.directory = mx, key, directory
        self.started, self.calls, self.tokens = started, 0, 0
        mx.set_memory_limit(LIMITS["mlx_memory_bytes"])
        mx.set_cache_limit(LIMITS["mlx_cache_bytes"])
        mx.random.seed(42)
        mx.reset_peak_memory()
        self.model, self.tokenizer = load(str(snapshot), tokenizer_config={"trust_remote_code": False})
        self.load_seconds = time.monotonic() - started

    def length(self, text):
        return len(self.tokenizer.encode(text, add_special_tokens=False))

    def ask(self, role, instructions, payload, schema):
        from mlx_lm import stream_generate
        from mlx_lm.sample_utils import make_sampler
        messages = messages_for(self.key, instructions, payload, schema)
        prompt = encode_chat(self.tokenizer, messages, self.key)
        reserve = len(prompt) + LIMITS["output_tokens"]
        if (self.calls >= LIMITS["calls"] or reserve > LIMITS["context_tokens"]
                or self.tokens + reserve > LIMITS["total_tokens"]
                or time.monotonic() - self.started >= LIMITS["seconds"]):
            raise BudgetStop("Local inference limit reached")
        self.calls += 1
        entry = {"call": self.calls, "role": role, "messages": messages,
                 "input_tokens": len(prompt), "raw_output": ""}
        started = time.monotonic()
        result, error = None, None
        try:
            for result in stream_generate(self.model, self.tokenizer, prompt=prompt,
                                          max_tokens=LIMITS["output_tokens"],
                                          sampler=make_sampler(temp=0.0)):
                entry["raw_output"] += result.text
                if time.monotonic() - self.started >= LIMITS["seconds"]:
                    raise BudgetStop("Local time limit reached")
            if result is None:
                raise ProviderFailure("No generation returned")
            value, error = parse_reply(entry["raw_output"], schema)
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


def run(key, output_root=None, client_factory=LocalClient):
    repo, revision = MODELS[key]
    snapshot = Path.home() / ".cache/huggingface/hub" / ("models--" + repo.replace("/", "--")) / "snapshots" / revision
    if client_factory is LocalClient and not (snapshot / "model.safetensors").is_file():
        raise FileNotFoundError("Pinned weights not cached; download separately before running")
    directory = Path(output_root or CASE_DIR / "results") / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-local-" + key)
    directory.mkdir(parents=True, exist_ok=False)
    sources = [Path(__file__), Path(smoke.__file__), Path(__file__).with_name("prompt_search.py"),
               CASE_DIR / "harness-test-cases.yaml"]
    hashes = {str(p.relative_to(CASE_DIR)): smoke.digest(p) for p in sources}
    model_hashes = {p.name: smoke.digest(p) for p in snapshot.iterdir() if p.is_file()} if snapshot.exists() else {}
    cases = smoke.select_cases()
    protocol = {"protocol": PROTOCOL, "model": repo, "revision": revision,
                "model_files_sha256": model_hashes, "limits": LIMITS, "cases": cases,
                "runtime": smoke.RUNTIME, "initial_policy": smoke.INITIAL_POLICY,
                "initial_strategy": smoke.INITIAL_STRATEGY, "objective": smoke.OBJECTIVE,
                "proposal_contract": smoke.PROPOSAL_CONTRACT, "update_contract": smoke.UPDATE_CONTRACT,
                "source_hashes": hashes, "temperature": 0, "seed": 42, "adapters": None,
                "enable_thinking": False if key == "qwen3" else None,
                "quantization": "4-bit, as distributed in the pinned MLX snapshot",
                "selection": "Validation q gain >=0.01 and v=0; keep incumbent on ties.",
                "stop": "Three proposals or resource/runtime/proposal failure; no retry.",
                "invalid_output": "Negotiator output fails the case; invalid proposal/update stops the run.",
                "format": "Schema in prompt; no constrained decoding. Strip one JSON fence only.",
                "roles": "Native system+user for Qwen; instructions folded into user for Gemma 2.",
                "metric_scope": "Structured decisions; message meaning and clarity not judged.",
                "length": "Native tokenizer without special tokens for H and phi; full chat template for input.",
                "api_calls": 0, "hardware": "Apple M5 Max, 40 GPU cores, 48 GB unified memory",
                "python": platform.python_version(),
                "packages": {n: importlib.metadata.version(n) for n in
                             ("mlx", "mlx-lm", "transformers", "tokenizers", "jsonschema", "PyYAML")},
                "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=CASE_DIR, text=True).strip()}
    smoke.write_json(directory / "protocol.json", protocol)
    (directory / "calls.jsonl").touch()
    report = {"protocol": PROTOCOL, "model_key": key, "status": "running", "rounds": [],
              "strategy_updates": [], "selected_iteration": None}
    client = None
    started = time.monotonic()

    def checkpoint():
        smoke.write_json(directory / "report.json", report)

    def ask(role, instructions, payload, schema):
        if any(smoke.digest(CASE_DIR / p) != h for p, h in hashes.items()):
            raise ValueError("Protected source changed")
        return client.ask(role, instructions, payload, schema)

    def evaluate(policy, split):
        rows = []
        for case in cases[split]:
            reply, error = ask("negotiator", smoke.RUNTIME + smoke.POLICY_SEPARATOR + policy, visible(case), REPLY_SCHEMA)
            check = {"task_match": False, "violations": [error]} if error else rule_check(case, reply)
            rows.append({"id": case["id"], "reply": reply, "expected": case["expected"], **check,
                         "success": check["task_match"] and not check["violations"]})
        return smoke.summarize(rows)

    try:
        client = client_factory(key, directory, snapshot, started)
        policy, strategy = smoke.INITIAL_POLICY, smoke.INITIAL_STRATEGY
        incumbent = {"iteration": 0, "policy": policy, "policy_tokens": client.length(policy),
                     "strategy_tokens": client.length(strategy), "strategy_used": strategy,
                     "development": evaluate(policy, "development"),
                     "validation": evaluate(policy, "validation"), "accepted": True}
        report["rounds"].append(incumbent)
        report["selected_iteration"] = 0
        checkpoint()
        for iteration in range(1, LIMITS["iterations"] + 1):
            value, error = ask("proposer", smoke.PROPOSAL_CONTRACT + strategy,
                               {"objective": smoke.OBJECTIVE, "current_policy": policy,
                                "development_feedback": incumbent["development"]["rows"]}, PROMPT_SCHEMA)
            if error:
                raise ProviderFailure("Invalid proposer output: " + error)
            proposal = get_prompt(value)
            candidate = {"iteration": iteration, "parent_iteration": incumbent["iteration"],
                         "policy": proposal, "policy_tokens": client.length(proposal),
                         "strategy_used": strategy, "strategy_tokens": client.length(strategy),
                         "development": evaluate(proposal, "development"),
                         "validation": evaluate(proposal, "validation")}
            candidate["accepted"] = smoke.choose(candidate["validation"], incumbent["validation"], .01)
            report["rounds"].append(candidate)
            if candidate["accepted"]:
                policy, incumbent = proposal, candidate
                report["selected_iteration"] = iteration
            checkpoint()
            print(f"{key} iteration={iteration} q={candidate['validation']['q']} accepted={candidate['accepted']}", flush=True)
            if iteration < LIMITS["iterations"]:
                value, error = ask("strategy_update", smoke.UPDATE_CONTRACT,
                                   {"objective": smoke.OBJECTIVE, "current_strategy": strategy,
                                    "candidate_policy": proposal,
                                    "development_feedback": candidate["development"]["rows"]}, PROMPT_SCHEMA)
                if error:
                    raise ProviderFailure("Invalid updater output: " + error)
                updated = get_prompt(value)
                report["strategy_updates"].append({"after_iteration": iteration, "before": strategy,
                                                   "after": updated, "changed": updated != strategy,
                                                   "before_tokens": client.length(strategy),
                                                   "after_tokens": client.length(updated)})
                strategy = updated
                checkpoint()
        report["test"] = evaluate(policy, "test")
        report["status"] = "completed"
    except (BudgetStop, ProviderFailure, ValueError, RuntimeError) as exc:
        report.update(status="stopped", stop_type=type(exc).__name__)
        if isinstance(exc, (BudgetStop, ProviderFailure)):
            report["stop_reason"] = str(exc)
    finally:
        report.update(elapsed_seconds=time.monotonic() - started,
                      calls=client.calls if client else 0, tokens=client.tokens if client else 0,
                      load_seconds=client.load_seconds if client else None,
                      peak_mlx_gb=client.mx.get_peak_memory() / 1e9 if client else None,
                      protected_source_changes=sum(smoke.digest(CASE_DIR / p) != h for p, h in hashes.items()))
        checkpoint()
        smoke.write_json(directory / "manifest.json", {p.name: smoke.digest(p) for p in directory.iterdir()
                                                       if p.is_file() and p.name != "manifest.json"})
    return directory


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=MODELS)
    args = parser.parse_args()
    print(run(args.model))
