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
import task as smoke


class SmokeTests(unittest.TestCase):

    def test_spanish_fixtures_preserve_splits_and_expected_decisions(self):
        original = {item['id']: item for item in smoke.load_cases()}
        translated = smoke.select_cases()
        self.assertEqual({split: len(items) for split, items in translated.items()},
                         {'development': 2, 'validation': 2, 'test': 2})
        for split, items in translated.items():
            for item in items:
                source = original[item['id']]
                for field in ('split', 'group', 'expected', 'declared_capacity', 'declined', 'accepted_plan'):
                    self.assertEqual(item[field], source[field])
                self.assertNotEqual(item['history'], source['history'])
                self.assertEqual([t['role'] for t in item['history']], [t['role'] for t in source['history']])

    def test_quality_and_violations_are_not_complements(self):
        row = {'success': False, 'violations': []}
        self.assertEqual(smoke.summarize([row]), {'q': 0, 'v': 0, 'rows': [row]})
        self.assertFalse(smoke.choose({'q': 1, 'v': .5}, {'q': 0, 'v': 0}, .01))


    def test_notebook_replay_is_executed_and_never_uses_network(self):
        notebook = json.loads((CASE / 'notebooks' / 'harness-smoke-test.ipynb').read_text())
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
                            self.assertTrue((CASE / 'notebooks' / link).exists(), link)
        self.assertFalse(scope['RUN_LIVE'])
        self.assertEqual(scope['report']['protocol'], 'case-0003-harness-smoke-v3')
        self.assertEqual(scope['rho'], 1)

    def test_trace_audit_rejects_missing_origins_and_false_evaluations(self):
        from notebook_view import audit_harness_changes
        notebook = json.loads((CASE / 'notebooks' / 'harness-smoke-test.ipynb').read_text())
        directory = (CASE / notebook['metadata']['evidence']['report']).parent
        protocol, report = smoke.read_record(directory)
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



if __name__ == '__main__':
    unittest.main()
