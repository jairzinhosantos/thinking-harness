"""Check grammar boundaries, schema validity and separation from task correctness."""
import base64
import hashlib
import json
from pathlib import Path
import string
import sys
import unittest
from unittest.mock import patch

CASE = Path(__file__).resolve().parents[2] / 'research/cases/case-0003-debt-negotiation'
sys.path.insert(0, str(CASE / 'utils'))
from structured_output import FinalJsonMask, tokenizer_data, schema_for_grammar
import local_model_test as local


class CharacterTokenizer:
    def __init__(self):
        self.characters = list(dict.fromkeys(string.printable + 'áéíóúñ'))
        self.vocab = {c: i for i, c in enumerate(self.characters)}
        self.close = len(self.vocab)
        self.eos_token_id = self.close + 1
        self.vocab.update({'</think>': self.close, '<eos>': self.eos_token_id})
        self.all_special_ids = [self.close, self.eos_token_id]
    def get_vocab(self): return self.vocab
    def encode(self, text, **kwargs): return [self.vocab[c] for c in text]
    def decode(self, ids): return ''.join(self.characters[i] for i in ids if i < self.close)


class StructuredOutputTests(unittest.TestCase):
    def setUp(self):
        self.tokenizer = CharacterTokenizer()
        self.data = tokenizer_data(self.tokenizer)

    def start(self, schema):
        mask = FinalJsonMask(self.data, schema, self.tokenizer.close)
        # A closing tag in the prompt is not the generated reasoning boundary.
        prefix = [self.tokenizer.close, 3]
        self.assertIsNone(mask.allowed(prefix))
        self.assertIsNone(mask.allowed(prefix + [5]))
        tokens = prefix + [5, self.tokenizer.close]
        self.assertIsNotNone(mask.allowed(tokens))
        return mask, tokens

    def consume(self, mask, tokens, text):
        for token in self.tokenizer.encode(text):
            self.assertIn(token, mask.allowed(tokens), self.tokenizer.decode([token]))
            tokens.append(token)
        return mask.allowed(tokens)

    def test_instance_allowed_schema_copy_and_early_stop_blocked(self):
        mask, tokens = self.start(local.PROMPT_SCHEMA)
        self.assertNotIn(self.tokenizer.eos_token_id, mask.allowed(tokens))
        self.consume(mask, tokens, '{"')
        self.assertNotIn(self.tokenizer.vocab['t'], mask.allowed(tokens))
        allowed = self.consume(mask, tokens, 'prompt":"Revisa la cuota y la decisión."}')
        self.assertIn(self.tokenizer.eos_token_id, allowed)
        self.assertTrue(mask.stats['activated'])

    def test_wrong_business_decision_still_passes_structure(self):
        case = next(c for c in local.transfer_cases() if c['declared_capacity'] is not None)
        wrong = {'action': 'ask', 'debt': None, 'payments': 0, 'installment': 0}
        mask, tokens = self.start(local.DECISION_SCHEMA)
        allowed = self.consume(mask, tokens, json.dumps(wrong))
        self.assertIn(self.tokenizer.eos_token_id, allowed)
        self.assertFalse(local.rule_check(case, local.render_decision(wrong))['task_match'])

    def test_nullable_enum_conversion_preserves_allowed_values(self):
        from jsonschema import Draft202012Validator
        before = local.DECISION_SCHEMA['properties']['debt']
        after = schema_for_grammar(before)
        for value in [None, 'A', 'B', 'C', 'D', '', 0, True, {}, []]:
            self.assertEqual(Draft202012Validator(before).is_valid(value),
                             Draft202012Validator(after).is_valid(value))
        self.assertEqual(before['type'], ['string', 'null'])

    def test_default_client_has_no_generation_mask(self):
        client = local.LocalClient.__new__(local.LocalClient)
        self.assertEqual(client.output_processors(local.PROMPT_SCHEMA), ([], None))


class StructuredEvidenceTests(unittest.TestCase):
    def test_recorded_structure_and_accounting(self):
        for folder in (CASE / 'results').glob('*-structured'):
            if not (folder / 'manifest.json').exists():
                continue
            for name, digest in json.loads((folder / 'manifest.json').read_text()).items():
                self.assertEqual(Path(name).name, name)
                self.assertEqual(local.smoke.digest(folder / name), digest)
            protocol = json.loads((folder / 'protocol.json').read_text())
            report = json.loads((folder / 'report.json').read_text())
            calls = [json.loads(line) for line in (folder / 'calls.jsonl').read_text().splitlines()]
            self.assertEqual(protocol['decoding'], 'json_schema')
            self.assertEqual(report['tokens'], sum(c['input_tokens'] + c['output_tokens'] for c in calls))
            self.assertEqual(report['calls'], len(calls))
            for call in calls:
                if call.get('error') is None:
                    self.assertTrue(call['structured_generation']['activated'])
                    schema = local.DECISION_SCHEMA if call['role'] == 'negotiator' else local.PROMPT_SCHEMA
                    value, error = local.parse_reply(call['raw_output'].split('</think>', 1)[-1].strip(), schema)
                    self.assertIsNone(error)
                    self.assertEqual(value, call['parsed'])

    def test_notebook_replays_offline(self):
        path = CASE / 'structured-output.ipynb'
        notebook = json.loads(path.read_text())
        for name, digest in notebook['metadata']['evidence']['prior_notebooks_sha256'].items():
            self.assertEqual(local.smoke.digest(CASE / name), digest)
        for cell in notebook['cells']:
            diagram = cell['metadata'].get('diagram')
            if diagram:
                self.assertEqual(local.smoke.digest(CASE / diagram['source']), diagram['source_sha256'])
                preview = next(iter(cell['attachments'].values()))['image/png']
                self.assertEqual(hashlib.sha256(base64.b64decode(preview)).hexdigest(), diagram['preview_sha256'])
        scope = {}
        with patch('urllib.request.urlopen', side_effect=AssertionError('Unexpected network')), patch('IPython.display.display'):
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    self.assertIsInstance(cell['execution_count'], int)
                    self.assertFalse(any(o['output_type'] == 'error' for o in cell['outputs']))
                    exec(compile(''.join(cell['source']), 'structured-notebook-cell', 'exec'), scope)
        self.assertEqual(len(scope['records']), 4)


if __name__ == '__main__': unittest.main()
