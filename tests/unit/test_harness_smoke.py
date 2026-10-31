"""Offline controls for the illustrative adaptive-prompt experiment."""
import contextlib
import copy
import io
import json
import re
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

CASE = Path(__file__).resolve().parents[2] / 'research/cases/case-0003-debt-negotiation'
sys.path.insert(0, str(CASE / 'utils'))
import harness_smoke_test as smoke


class FakeClient:
    """Deterministic test double, never used as research evidence."""
    instances = []

    def __init__(self, config, directory):
        self.calls = self.tokens = self.cost = 0
        self.uncertain = False
        self.requests = []
        self.instances.append(self)

    def ask(self, role, instructions, payload, schema):
        self.calls += 1
        self.requests.append((role, instructions, payload))
        if role == 'proposer':
            return {'prompt': 'Revised policy'}
        if role == 'strategy_update':
            return {'prompt': f'Revised improvement strategy {self.calls}'}
        if smoke.INITIAL_POLICY in instructions:
            return {'action': 'ask', 'debt': None, 'payments': 0, 'installment': 0, 'message': 'Capacity?'}
        case = next(c for cs in smoke.select_cases().values() for c in cs if c['history'] == payload['history'])
        return {**case['expected'], 'message': 'Test-only response'}


class SmokeTests(unittest.TestCase):
    def test_adaptation_is_reused_and_selection_keeps_ties(self):
        with tempfile.TemporaryDirectory() as directory:
            path = smoke.run(directory, FakeClient)
            result = json.loads((path / 'report.json').read_text())
            client = FakeClient.instances[-1]
            self.assertEqual(result['status'], 'completed')
            self.assertEqual(client.calls, 35)
            self.assertEqual(result['N_uso'], 4)
            self.assertEqual(result['selected_iteration'], 1)
            self.assertFalse(result['rounds'][2]['accepted'])
            self.assertIsNotNone(result['T_meta'])
            proposers = [r for r in client.requests if r[0] == 'proposer']
            self.assertEqual(len(proposers), 5)
            self.assertEqual(len(result['strategy_updates']), 4)
            for i, update in enumerate(result['strategy_updates'], start=1):
                self.assertIn(update['after'], proposers[i][1])
                self.assertEqual(update['after_iteration'], i)
            for role, instructions, payload in client.requests:
                if role in ('proposer', 'strategy_update'):
                    self.assertNotIn('validation-', json.dumps(payload))
                    self.assertNotIn('test-', json.dumps(payload))
                if role == 'negotiator':
                    self.assertEqual(set(payload), {'debts', 'allowed_payment_counts', 'history'})
            self.assertEqual(result['V_prot'], 0)

    def test_quality_and_violations_are_not_complements(self):
        row = {'success': False, 'violations': []}
        self.assertEqual(smoke.summarize([row]), {'q': 0, 'v': 0, 'rows': [row]})
        self.assertFalse(smoke.choose({'q': 1, 'v': .5}, {'q': 0, 'v': 0}, .01))

    def test_provider_failure_stops_without_retry_and_saves_partial_report(self):
        class FailingClient(FakeClient):
            def ask(self, *args):
                self.calls += 1
                self.uncertain = True
                raise smoke.ProviderFailure('test')
        with tempfile.TemporaryDirectory() as directory:
            path = smoke.run(directory, FailingClient)
            result = json.loads((path / 'report.json').read_text())
            self.assertEqual(result['status'], 'stopped')
            self.assertEqual(result['usage']['calls'], 1)
            self.assertTrue(result['usage']['uncertain'])
            self.assertNotIn('test', result)
            self.assertIsNone(result['T_meta'])

    def test_notebook_replay_is_executed_and_never_uses_network(self):
        notebook = json.loads((CASE / 'harness-smoke-test.ipynb').read_text())
        scope = {}
        with patch('urllib.request.urlopen', side_effect=AssertionError('Unexpected network call')), \
                patch('IPython.display.display'), contextlib.redirect_stdout(io.StringIO()):
            for cell in notebook['cells']:
                source = ''.join(cell['source'])
                if cell['cell_type'] == 'code':
                    self.assertIsNotNone(cell['execution_count'])
                    self.assertFalse(any(o['output_type'] == 'error' for o in cell['outputs']))
                    exec(compile(source, 'smoke-notebook-cell', 'exec'), scope)
                else:
                    for link in re.findall(r'\]\(([^)]+)\)', source):
                        if not link.startswith(('https://', 'attachment:')):
                            self.assertTrue((CASE / link).exists(), link)
        self.assertFalse(scope['RUN_LIVE'])
        self.assertEqual(scope['report']['protocol'], smoke.PROTOCOL)
        self.assertEqual(scope['rho'], 1)

    def test_trace_audit_rejects_missing_origins_and_false_evaluations(self):
        from notebook_view import audit_harness_changes
        notebook = json.loads((CASE / 'harness-smoke-test.ipynb').read_text())
        directory = (CASE / notebook['metadata']['evidence']['report']).parent
        protocol, report = smoke.load_run(directory)
        calls = [json.loads(x) for x in (directory / 'calls.jsonl').read_text().splitlines()]
        self.assertTrue(all(ok for _, ok in audit_harness_changes(protocol, report, calls)))
        broken = copy.deepcopy(report)
        broken['rounds'][1]['parent_iteration'] = 99
        self.assertFalse(audit_harness_changes(protocol, broken, calls)[0][1])
        broken = copy.deepcopy(report)
        broken['rounds'][1]['validation']['q'] = 0.123
        self.assertFalse(audit_harness_changes(protocol, broken, calls)[0][1])

    def test_prompt_display_escapes_text_and_uses_readable_comparison(self):
        from notebook_view import HarnessTestView
        view = HarnessTestView()
        with patch('notebook_view.display') as show:
            view.strategy({'after_iteration': 1, 'before': '<script>bad()</script>',
                           'after': 'Inspect failures. Preserve correct behavior.', 'changed': True}, True)
        html = ''.join(call.args[0].data for call in show.call_args_list)
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertIn('Antes: φ0', html)
        self.assertIn('Después: φ1', html)
        self.assertIn('<li>Inspect failures.</li>', html)
        self.assertIn('Sí', html)
        self.assertNotIn('True', html)

    def test_evidence_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = smoke.run(directory, FakeClient)
            (path / 'calls.jsonl').write_text('')
            manifest = json.loads((path / 'manifest.json').read_text())
            manifest['calls.jsonl'] = smoke.digest(path / 'calls.jsonl')
            smoke.write_json(path / 'manifest.json', manifest)
            smoke.load_run(path)
            (path / 'report.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                smoke.load_run(path)


if __name__ == '__main__':
    unittest.main()
