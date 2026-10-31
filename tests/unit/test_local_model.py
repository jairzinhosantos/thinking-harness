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
from local_model_test import parse_reply, messages_for, encode_chat
import local_model_test as local
from prompt_search import PROMPT_SCHEMA, REPLY_SCHEMA


class LocalTransportTests(unittest.TestCase):
    def test_renderer_preserves_bad_decisions_for_evaluator_to_reject(self):
        case = local.smoke.select_cases()['development'][0]
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
        self.assertIsNone(local.parse_reply(text, local.DECISION_SCHEMA)[1])
        self.assertEqual(local.parse_reply(text, REPLY_SCHEMA)[1], 'invalid_schema')
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
    def test_calibration_uses_only_development_and_no_optimizer(self):
        requests = []
        development = local.smoke.select_cases()['development']

        class Client:
            def __init__(self, *args):
                self.calls = self.tokens = 0
                self.load_seconds = 0
                self.mx = type('Memory', (), {'get_peak_memory': staticmethod(lambda: 0)})

            def length(self, text):
                return len(text.split())

            def ask(self, role, instructions, payload, schema):
                self.calls += 1
                requests.append((role, instructions, payload))
                case = next(c for c in development if c['history'] == payload['history'])
                return {**case['expected'], 'message': 'Control sintético'}, None

        with tempfile.TemporaryDirectory() as directory, \
                patch.dict(local.MODELS, {'stub': ('test/missing', 'test')}, clear=True), \
                patch.object(local.importlib.metadata, 'version', return_value='test-only'):
            path = local.run('stub', directory, Client, calibration=True)
            report = json.loads((path / 'report.json').read_text())
        self.assertEqual(report['calls'], 4)
        self.assertEqual(report['status'], 'completed')
        self.assertEqual(report['rounds'], [])
        self.assertNotIn('test', report)
        self.assertEqual([r['contract'] for r in report['calibration']], ['original', 'explicit'])
        self.assertTrue(all(role == 'negotiator' and local.smoke.OBJECTIVE in instructions
                            for role, instructions, _ in requests))

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
            if protocol['protocol'].endswith('-v1'):
                self.assertEqual(report['rounds'], [])
                continue  # Tokenizer compatibility failure, not an inference measurement.
            calls = [json.loads(line) for line in (directory / 'calls.jsonl').read_text().splitlines()]
            self.assertEqual(report['calls'], len(calls))
            self.assertEqual(report['tokens'], sum(c['input_tokens'] + c['output_tokens'] for c in calls))
            self.assertLessEqual(report['tokens'], protocol['limits']['total_tokens'])
            self.assertEqual(report['protected_source_changes'], 0)
            self.assertEqual('test' in report, report['status'] == 'completed' and protocol.get('kind') != 'calibration')

    def test_selection_reuses_strategy_and_excludes_held_out_feedback(self):
        self.check_search('adaptive')

    def test_fixed_search_never_updates_strategy(self):
        self.check_search('fixed')

    def check_search(self, strategy_mode):
        requests = []
        cases = [c for group in local.smoke.select_cases().values() for c in group] + local.transfer_cases()

        class Client:
            def __init__(self, *args):
                self.calls = self.tokens = 0
                self.load_seconds = 0
                self.mx = type('Memory', (), {'get_peak_memory': staticmethod(lambda: 0)})

            def length(self, text):
                return len(text.split())

            def ask(self, role, instructions, payload, schema):
                self.calls += 1
                requests.append((role, instructions, payload))
                if role == 'proposer':
                    return {'prompt': 'Política propuesta'}, None
                if role == 'strategy_update':
                    return {'prompt': 'Estrategia actualizada'}, None
                if 'Política propuesta' in instructions:
                    case = next(c for c in cases if c['history'] == payload['history'])
                    return {**case['expected'], 'message': 'Respuesta sintética'}, None
                return {'action': 'ask', 'debt': None, 'payments': 0,
                        'installment': 0, 'message': 'Capacidad?'}, None

        with tempfile.TemporaryDirectory() as directory, \
                patch.dict(local.MODELS, {'stub': ('test/missing', 'test')}, clear=True), \
                patch.object(local.importlib.metadata, 'version', return_value='test-only'):
            path = local.run('stub', directory, Client, contract='explicit', strategy_mode=strategy_mode)
            report = json.loads((path / 'report.json').read_text())
        self.assertEqual(report['status'], 'completed')
        self.assertEqual(report['calls'], 27 if strategy_mode == 'adaptive' else 25)
        self.assertEqual([r['duplicate_of'] for r in report['rounds'][1:]], [None, 1, 1])
        self.assertEqual(report['selected_iteration'], 1)
        self.assertEqual([r.get('parent_iteration') for r in report['rounds'][1:]], [0, 1, 1])
        self.assertEqual(report['test']['q'], 1)
        proposals = [r for r in requests if r[0] == 'proposer']
        self.assertEqual(proposals[0][2]['recent_attempts'], [])
        self.assertEqual(proposals[1][2]['recent_attempts'][0]['policy'], 'Política propuesta')
        self.assertEqual(len(report['transfer']['selected']['rows']), 6)
        self.assertEqual(report['transfer']['selected']['q'], 1)
        if strategy_mode == 'adaptive':
            self.assertIn('Estrategia actualizada', proposals[1][1])
        else:
            self.assertEqual(report['strategy_updates'], [])
            self.assertTrue(all(local.smoke.INITIAL_STRATEGY in p[1] for p in proposals))
            self.assertFalse(any(r[0] == 'strategy_update' for r in requests))
        for role, _, payload in requests:
            if role != 'negotiator':
                self.assertNotIn('validation-', json.dumps(payload))
                self.assertNotIn('test-', json.dumps(payload))
                self.assertNotIn('transfer-', json.dumps(payload))
                for feedback in payload['development_feedback']:
                    original = next(c for c in cases if c['id'] == feedback['id'])
                    self.assertEqual(feedback['context'], local.visible(original))


if __name__ == '__main__':
    unittest.main()
