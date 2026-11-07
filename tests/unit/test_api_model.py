"""Offline checks for API budgets, structured responses and secret-free logs."""
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import types
import unittest
from unittest.mock import patch

CASE = Path(__file__).resolve().parents[2] / 'research/cases/case-0003-debt-negotiation'
sys.path.insert(0, str(CASE / 'utils'))
from models import ApiClient
from task import BudgetStop, ProviderFailure, PROMPT_SCHEMA


class ApiModelTests(unittest.TestCase):
    def client(self, folder):
        tokenizer = types.SimpleNamespace(encode=lambda text: list(text.encode()))
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-secret'}), \
             patch.dict(sys.modules, {'tiktoken': types.SimpleNamespace(encoding_for_model=lambda name: tokenizer)}):
            return ApiClient('gpt-4o-mini-2024-07-18', folder, None, time.monotonic(),
                sampling={'temperature': .6}, limits={'calls': 90, 'output_tokens': 2048,
                    'context_tokens': 32768, 'total_tokens': 180000, 'seconds': 1800})

    def test_preflight_stops_without_request(self):
        with tempfile.TemporaryDirectory() as folder:
            client = self.client(folder)
            client.limits['total_tokens'] = 1
            with patch('urllib.request.urlopen') as send:
                with self.assertRaises(BudgetStop):
                    client.ask('proposer', 'Contrato', {}, PROMPT_SCHEMA)
                send.assert_not_called()
            self.assertEqual(client.calls, 0)

    def test_failure_never_retries_or_logs_secret(self):
        with tempfile.TemporaryDirectory() as folder:
            client = self.client(folder)
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-secret'}), patch('urllib.request.urlopen', side_effect=OSError('test-secret')) as send:
                for _ in range(2):
                    with self.assertRaises(ProviderFailure):
                        client.ask('proposer', 'Contrato', {}, PROMPT_SCHEMA)
                self.assertEqual(send.call_count, 1)
            log = (Path(folder) / 'calls.jsonl').read_text()
            self.assertNotIn('test-secret', log)
            self.assertTrue(client.uncertain)
            self.assertGreater(client.tokens, 0)

    def test_usage_schema_and_incomplete_response(self):
        import io
        for status, error in [('completed', None), ('incomplete', 'incomplete_response')]:
            with self.subTest(status=status), tempfile.TemporaryDirectory() as folder:
                client = self.client(folder)
                data = {'status': status, 'usage': {'input_tokens': 100, 'output_tokens': 20},
                    'output': [{'type': 'message', 'content': [{'type': 'output_text', 'text': '{"prompt":"Mejora"}'}]}]}
                with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-secret'}), patch('urllib.request.urlopen', return_value=io.BytesIO(json.dumps(data).encode())) as send:
                    value, actual_error = client.ask('proposer', 'Contrato', {'objective': 'Caso'}, PROMPT_SCHEMA)
                self.assertEqual(actual_error, error)
                self.assertEqual(value, {'prompt': 'Mejora'} if error is None else None)
                self.assertEqual(client.tokens, 120)
                self.assertAlmostEqual(client.cost, (100 * .15 + 20 * .60) / 1e6)
                request = json.loads(send.call_args.args[0].data)
                self.assertTrue(request['text']['format']['strict'])
                self.assertNotIn('seed', request)
                saved = json.loads((Path(folder) / 'calls.jsonl').read_text())
                self.assertEqual(saved['parsed'], value)
