"""Schema-constrained final JSON for MLX; free reasoning before the closing tag."""
from lmformatenforcer import CharacterLevelParserConfig, JsonSchemaParser, TokenEnforcer, TokenEnforcerTokenizerData
from models import LocalClient


def tokenizer_data(tokenizer):
    """Prepare Qwen byte-level tokens without importing the Torch integration."""
    # Follow LMFE's tokenizer adapter convention: contextual decode after a prefix.
    # Reference: lmformatenforcer/integrations/transformers.py (MIT license).
    prefix = tokenizer.encode('0', add_special_tokens=False)
    prefix_text = tokenizer.decode(prefix)
    specials = set(tokenizer.all_special_ids)
    vocabulary = tokenizer.get_vocab()
    vocab_size = max(vocabulary.values()) + 1
    regular = []
    for token in sorted(set(vocabulary.values())):
        if token in specials:
            continue
        contextual = tokenizer.decode(prefix + [token])[len(prefix_text):]
        standalone = tokenizer.decode([token])
        regular.append((token, contextual, len(contextual) > len(standalone)))
    eos = sorted(tokenizer.eos_token_ids) if hasattr(tokenizer, 'eos_token_ids') else tokenizer.eos_token_id
    return TokenEnforcerTokenizerData(regular, lambda ids: tokenizer.decode(ids).rstrip('\ufffd'),
                                     eos, False, vocab_size)


def schema_for_grammar(value):
    """Express nullable string enums as an equivalent union supported by LMFE."""
    if isinstance(value, list):
        return [schema_for_grammar(item) for item in value]
    if not isinstance(value, dict):
        return value
    if value.get('type') == ['string', 'null'] and None in value.get('enum', []):
        if set(value) != {'type', 'enum'}:
            raise ValueError('Review additional nullable-enum constraints before conversion')
        return {'anyOf': [{'type': 'string', 'enum': [x for x in value['enum'] if x is not None]},
                          {'type': 'null'}]}
    return {key: schema_for_grammar(item) for key, item in value.items()}


class FinalJsonMask:
    """Mask only final-answer tokens. Never inspect labels or alter completed text."""
    def __init__(self, data, schema, close_token):
        self.enforcer = TokenEnforcer(data, JsonSchemaParser(schema_for_grammar(schema), config=CharacterLevelParserConfig(max_consecutive_whitespaces=12, force_json_field_order=False, max_json_array_length=20)))
        self.close_token = close_token
        self.eos_tokens = data.eos_token_id if isinstance(data.eos_token_id, list) else [data.eos_token_id]
        self.prefix_length = None
        self.stats = {'backend': 'lm-format-enforcer', 'activated': False, 'mask_steps': 0}

    def allowed(self, tokens):
        if self.prefix_length is None:
            # MLX prefill may leave only the last prompt token for processors.
            self.prefix_length = len(tokens)
        generated = tokens[self.prefix_length:]
        if self.close_token not in generated:
            return None
        boundary = generated.index(self.close_token) + 1
        suffix = generated[boundary:]
        self.stats['activated'] = True
        self.stats['mask_steps'] += 1
        if suffix and suffix[-1] in self.eos_tokens:
            return self.eos_tokens
        allowed = self.enforcer.get_allowed_tokens(suffix).allowed_tokens
        if not allowed:
            raise ValueError('Schema mask has no allowed continuation')
        return allowed

    def __call__(self, tokens, logits):
        import mlx.core as mx
        allowed = self.allowed(tokens.tolist())
        if allowed is None:
            return logits
        mask = mx.full((logits.shape[-1],), -float('inf'), dtype=logits.dtype)
        mask[mx.array(allowed)] = 0
        return logits + mask


class StructuredLocalClient(LocalClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.sampling.get('enable_thinking'):
            raise ValueError('This adapter requires Qwen thinking mode')
        close = self.tokenizer.encode('</think>', add_special_tokens=False)
        if len(close) != 1:
            raise ValueError('Expected one closing-think token')
        self.close_token = close[0]
        self.schema_tokenizer = tokenizer_data(self.tokenizer)

    def output_processors(self, schema):
        processor = FinalJsonMask(self.schema_tokenizer, schema, self.close_token)
        return [processor], processor.stats
