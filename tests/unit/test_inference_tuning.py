"""Check tuning selection, confirmation isolation and immutable evidence."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import yaml

CASE = Path(__file__).resolve().parents[2] / 'research/cases/case-0003-debt-negotiation'
sys.path.insert(0, str(CASE / 'utils'))
import inference_tuning as tuning
import api_reference_test as api


class TuningTests(unittest.TestCase):
    def test_selection_prefers_zero_violations_and_breaks_ties_before_confirmation(self):
        items = [{'sampling': {'temperature': t}, 'q': q, 'v': v} for t,q,v in [(0,1,.1),(.3,.9,0),(.7,.9,0)]]
        self.assertEqual(tuning.select_profile(items)['sampling']['temperature'], .3)

    def test_confirmation_fixtures_are_disjoint_and_expected_decisions_pass(self):
        cases = yaml.safe_load((CASE / 'inference-confirmation-cases.yaml').read_text())['cases']
        known = [c for g in tuning.local.smoke.select_cases().values() for c in g] + tuning.local.transfer_cases()
        self.assertFalse({json.dumps(c['history']) for c in cases} & {json.dumps(c['history']) for c in known})
        for case in cases:
            check = tuning.local.rule_check(case, tuning.local.render_decision(case['expected']))
            self.assertTrue(check['task_match'])
            self.assertEqual(check['violations'], [])
            self.assertNotIn('expected', tuning.local.visible(case))

    def test_tuning_excludes_confirmation_and_changes_sampling_only(self):
        requests = []
        class Client:
            def __init__(self, key, folder, snapshot, started, **kwargs):
                self.calls = self.tokens = 0
                self.sampling = kwargs['sampling']
                self.mx = type('Memory', (), {'get_peak_memory': staticmethod(lambda: 0),
                    'random': type('Random', (), {'seed': staticmethod(lambda seed: None)})})
            def ask(self, role, instructions, payload, schema):
                self.calls += 1
                requests.append((instructions, payload, self.sampling.copy()))
                return {'action':'ask','debt':None,'payments':0,'installment':0}, None
        with tempfile.TemporaryDirectory() as folder, patch.object(tuning.importlib.metadata, 'version', return_value='stub'):
            path = tuning.run(output_root=folder, client_factory=Client)
            protocol, report = tuning.read_record(path)
        self.assertEqual(report['status'], 'completed')
        self.assertEqual(len(requests),84)
        self.assertEqual(len({r[0] for r in requests}),1)
        self.assertTrue(all('expected' not in r[1] for r in requests))
        self.assertFalse(any(c['id'].startswith('confirmation-') for c in protocol['cases']))
        self.assertEqual(len(report['profiles']),3)
        self.assertEqual(len({r[2]['temperature'] for r in requests}),3)

    def test_api_reference_requires_opt_in_and_stops_before_confirmation_on_failure(self):
        with self.assertRaises(ValueError):
            api.run()
        requests = []
        class Client:
            def __init__(self, config, folder):
                self.calls = self.tokens = self.cost = 0
            def ask(self, role, instructions, payload, schema):
                self.calls += 1
                requests.append(payload)
                return {'action':'ask','debt':None,'payments':0,'installment':0}
        with tempfile.TemporaryDirectory() as folder:
            path = api.run(allow_live=True, output_root=folder, client_factory=Client)
            _, report = tuning.read_record(path)
        self.assertEqual(len(requests), 12)
        self.assertFalse(report['passes'])
        self.assertIsNone(report['confirmation'])
        self.assertTrue(all('expected' not in r for r in requests))

    def test_api_confirmation_runs_only_after_success_and_preserves_all_repeats(self):
        known = [c for g in tuning.local.smoke.select_cases().values() for c in g] + tuning.local.transfer_cases()
        confirm = yaml.safe_load((CASE / 'inference-confirmation-cases.yaml').read_text())['cases']
        expected = {json.dumps(tuning.local.visible(c), sort_keys=True): c['expected'] for c in known+confirm}
        class Client:
            def __init__(self, config, folder):
                self.calls = self.tokens = self.cost = 0
            def ask(self, role, instructions, payload, schema):
                self.calls += 1
                return expected[json.dumps(payload, sort_keys=True)]
        with tempfile.TemporaryDirectory() as folder:
            path = api.run(allow_live=True, output_root=folder, client_factory=Client)
            _, report = tuning.read_record(path)
        self.assertEqual(report['calls'],36)
        self.assertTrue(report['passes'])
        self.assertEqual(len(report['confirmation']['rows']),24)

    def test_failed_tuning_cannot_enter_confirmation(self):
        folders = sorted((CASE / 'results').glob('*-inference-*/manifest.json'))
        for manifest in folders:
            protocol, report = tuning.read_record(manifest.parent)
            if protocol['phase'] == 'tuning' and not report['selected']['passes']:
                with tempfile.TemporaryDirectory() as folder:
                    with self.assertRaises(ValueError):
                        tuning.run(protocol['model_key'], confirmation_of=manifest.parent, output_root=folder)
                    self.assertEqual(list(Path(folder).iterdir()), [])

    def test_notebook_uses_only_saved_evidence(self):
        notebook = json.loads((CASE / 'inference-tuning.ipynb').read_text())
        scope = {}
        with patch('urllib.request.urlopen', side_effect=AssertionError('Unexpected network call')), patch('IPython.display.display'):
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    self.assertIsInstance(cell['execution_count'], int)
                    self.assertFalse(any(o['output_type']=='error' for o in cell['outputs']))
                    exec(compile(''.join(cell['source']), 'inference-notebook-cell', 'exec'), scope)
        self.assertTrue(scope['records'])

    def test_recorded_evidence_tokens_and_hashes(self):
        for folder in (CASE / 'results').glob('*-inference-*'):
            if not (folder / 'manifest.json').exists():
                continue
            protocol, report = tuning.read_record(folder)
            calls = [json.loads(line) for line in (folder / 'calls.jsonl').read_text().splitlines()]
            self.assertEqual(report['calls'], len(calls))
            self.assertEqual(report['tokens'], sum(c['input_tokens']+c['output_tokens'] for c in calls))
            self.assertLessEqual(report['tokens'], protocol['limits']['total_tokens'])
            for name in ('inference_tuning.py','local_model_test.py','harness_smoke_test.py','prompt_search.py'):
                self.assertEqual(hashlib.sha256((folder/name).read_bytes()).hexdigest(), protocol['source_hashes']['utils/'+name])


if __name__ == '__main__':
    unittest.main()
