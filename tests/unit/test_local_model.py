"""Offline checks for native model transport and failure handling."""
from pathlib import Path
import json
import hashlib
import sys
import tempfile
import unittest
from unittest.mock import patch

CASE = Path(__file__).resolve().parents[2] / 'research/cases/case-0003-debt-negotiation'
sys.path.insert(0, str(CASE / 'utils'))
from models import parse_reply, messages_for, encode_chat
import task as local
from task import PROMPT_SCHEMA, REPLY_SCHEMA


class LocalTransportTests(unittest.TestCase):
    def test_renderer_preserves_bad_decisions_for_evaluator_to_reject(self):
        case = local.select_cases()['development'][0]
        decision = {'action': 'offer', 'debt': 'C', 'payments': 1, 'installment': 600}
        reply = local.render_decision(decision)
        self.assertEqual({k: reply[k] for k in decision}, decision)
        self.assertIn('600', reply['message'])
        self.assertIn('exceeds_declared_capacity', local.rule_check(case, reply)['violations'])
        decision = {'action': 'offer', 'debt': 'C', 'payments': 2, 'installment': 300}
        reply = local.render_decision(decision)
        self.assertTrue(local.rule_check(case, reply)['task_match'])
        self.assertEqual(local.rule_check(case, reply)['violations'], [])

    def test_decision_schema_and_policy_identity(self):
        text = '{"action":"ask","debt":null,"payments":0,"installment":0}'
        self.assertIsNone(parse_reply(text, local.DECISION_SCHEMA)[1])
        self.assertEqual(parse_reply(text, REPLY_SCHEMA)[1], 'invalid_schema')
        self.assertEqual(local.policy_key('Dos  cuotas.\n'), local.policy_key('Dos cuotas.'))
        self.assertNotEqual(local.policy_key('Dos cuotas.'), local.policy_key('Una cuota.'))

    def test_template_is_encoded_as_ids_without_duplicate_special_tokens(self):
        class Tokenizer:
            def apply_chat_template(inner, messages, **kwargs):
                self.assertFalse(kwargs['tokenize'])
                self.assertFalse(kwargs['enable_thinking'])
                return 'native template'
            def encode(inner, text, **kwargs):
                self.assertEqual(text, 'native template')
                self.assertFalse(kwargs['add_special_tokens'])
                return [10, 20, 30]
        self.assertEqual(encode_chat(Tokenizer(), [], 'qwen3'), [10, 20, 30])

    def test_thinking_control_uses_native_template_switch(self):
        class Tokenizer:
            def apply_chat_template(inner, messages, **kwargs):
                self.assertTrue(kwargs['enable_thinking'])
                return 'native thinking template'
            def encode(inner, text, **kwargs):
                return [10, 20]
        self.assertEqual(encode_chat(Tokenizer(), [], 'qwen3-8b', thinking=True), [10, 20])

    def test_json_fence_allowed_but_prose_and_extra_fields_rejected(self):
        self.assertEqual(parse_reply('```json\n{"prompt":"Hola"}\n```', PROMPT_SCHEMA),
                         ({'prompt': 'Hola'}, None))
        self.assertEqual(parse_reply('Respuesta: {"prompt":"Hola"}', PROMPT_SCHEMA)[1], 'invalid_json')
        self.assertEqual(parse_reply('{"prompt":"Hola", "code":"run"}', PROMPT_SCHEMA)[1], 'invalid_schema')

    def test_decision_schema_does_not_accept_boolean_payment_count(self):
        text = '{"action":"offer","debt":"A","payments":true,"installment":200,"message":"Pago"}'
        self.assertEqual(parse_reply(text, REPLY_SCHEMA)[1], 'invalid_schema')

    def test_gemma_fold_preserves_contract_and_data_without_unsupported_role(self):
        for model in ('qwen', 'gemma'):
            messages = messages_for(model, 'Contrato fijo', {'history': 'cliente'}, PROMPT_SCHEMA)
            text = '\n'.join(m['content'] for m in messages)
            self.assertIn('Contrato fijo', text)
            self.assertIn('cliente', text)
            self.assertIn('additionalProperties', text)
            self.assertEqual([m['role'] for m in messages],
                             ['user'] if model == 'gemma' else ['system', 'user'])


class LocalLoopTests(unittest.TestCase):


    def test_recorded_runs_have_intact_manifests_and_balanced_token_counts(self):
        for directory in sorted((CASE / 'results').glob('*-local-*')):
            manifest = json.loads((directory / 'manifest.json').read_text())
            for name, expected in manifest.items():
                self.assertEqual(Path(name).name, name)
                self.assertEqual(hashlib.sha256((directory / name).read_bytes()).hexdigest(), expected)
            protocol = json.loads((directory / 'protocol.json').read_text())
            report = json.loads((directory / 'report.json').read_text())
            if (directory / 'source.py').exists():
                self.assertEqual(hashlib.sha256((directory / 'source.py').read_bytes()).hexdigest(),
                                 protocol['source_hashes']['utils/local_model_test.py'])
            if protocol['protocol'] == 'case-0003-local-model-v1':
                self.assertEqual(report['rounds'], [])
                continue  # Tokenizer compatibility failure, not an inference measurement.
            calls = [json.loads(line) for line in (directory / 'calls.jsonl').read_text().splitlines()]
            self.assertEqual(report['calls'], len(calls))
            self.assertEqual(report['tokens'], sum(c['input_tokens'] + c['output_tokens'] for c in calls))
            self.assertLessEqual(report['tokens'], protocol['limits']['total_tokens'])
            self.assertEqual(report['protected_source_changes'], 0)
            self.assertEqual('test' in report, report['status'] == 'completed' and protocol.get('kind') not in {'calibration', 'reference'})





if __name__ == '__main__':
    unittest.main()
