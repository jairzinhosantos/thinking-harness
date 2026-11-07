"""Check holdout isolation, paired randomness, selection and adaptation accounting."""
import hashlib
import json
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

CASE=Path(__file__).resolve().parents[2]/'research/cases/case-0003-debt-negotiation'
sys.path.insert(0,str(CASE/'utils'))
import paired_search as paired


class PairedSearchTests(unittest.TestCase):
    def test_reserved_cases_are_new_and_references_pass_fixed_evaluator(self):
        cases=paired.fixtures()
        known=[c for g in paired.task.select_cases().values() for c in g]+paired.task.transfer_cases()
        known+=json.loads((CASE/'inference-confirmation-cases.yaml').read_text())['cases']
        self.assertFalse({json.dumps(c['history']) for c in cases['test']} & {json.dumps(c['history']) for c in known})
        self.assertEqual([len(cases[k]) for k in ('development','validation','test')],[4,4,8])
        for split in ('development','validation','test'):
            for case in cases[split]:
                result=paired.task.rule_check(case,paired.task.render_decision(case['expected']))
                self.assertTrue(result['task_match'])
                self.assertEqual(result['violations'],[])

    def test_paired_search_hides_holdout_counts_updates_and_retains_ties(self):
        fixtures=paired.fixtures()
        lookup={json.dumps(paired.task.visible(c),sort_keys=True):c['expected'] for split in ('development','validation','test') for c in fixtures[split]}
        requests=[]
        configurations=[]
        class Client:
            def __init__(self,key,folder,snapshot,started,**kwargs):
                configurations.append(kwargs['limits'].copy())
                self.calls=self.tokens=self.proposals=0
                self.limits=kwargs['limits']
                self.sampling=kwargs['sampling']
                self.mx=type('MX',(),{'get_peak_memory':staticmethod(lambda:0),
                    'random':type('R',(),{'seed':staticmethod(lambda seed:None)})})
            def seed(self, value): pass
            def peak_memory(self): return 0
            def length(self,text): return len(text.split())
            def ask(self,role,instructions,payload,schema):
                self.calls+=1;self.tokens+=10
                requests.append((role,payload,self.sampling.copy()))
                if role=='proposer':
                    self.proposals+=1
                    return {'prompt':f'Candidate policy {self.proposals}'},None
                if role=='strategy_update':
                    return {'prompt':f'Updated strategy {self.proposals}'},None
                if instructions.endswith(paired.task.INITIAL_POLICY):
                    return {'action':'ask','debt':None,'payments':0,'installment':0},None
                return lookup[json.dumps(payload,sort_keys=True)],None
        reports=[]
        with tempfile.TemporaryDirectory() as folder,patch.object(paired.importlib.metadata,'version',return_value='stub'):
            for mode in ('fixed','adaptive'):
                path=paired.run(mode,output_root=folder,client_factory=Client,output_tokens=4096)
                reports.append(json.loads((path/'report.json').read_text()))
        self.assertTrue(all(c['output_tokens']==4096 and c['context_tokens']==8192 for c in configurations))
        self.assertTrue(all(c['total_tokens']==120000 for c in configurations))
        for report in reports:
            self.assertEqual(report['status'],'completed')
            self.assertEqual(report['selected_iteration'],1)
            self.assertEqual(len(report['rounds']),6)
            self.assertTrue(report['passes'])
            self.assertEqual(report['test']['initial']['q'],1/8)
            self.assertEqual(report['test']['selected']['q'],1)
            self.assertEqual(report['tokens'],10*report['calls'])
            self.assertEqual(report['first_validation_target']['iteration'],1)
        self.assertEqual([r['calls'] for r in reports],[69,73])
        self.assertEqual([len(r['strategy_updates']) for r in reports],[0,4])
        self.assertEqual(reports[1]['rounds'][2]['strategy_used'],'Updated strategy 1')
        self.assertEqual(reports[1]['rounds'][5]['strategy_used'],'Updated strategy 4')
        for role,payload,sampling in requests:
            if role in ('proposer','strategy_update'):
                self.assertTrue({r['id'] for r in payload['development_feedback']} <= {c['id'] for c in fixtures['development']})
            else:
                self.assertNotIn('expected',payload)
        for phase in ('development','validation','test'):
            seeds=[{e['seed'] for e in r['events'] if e['phase']==phase} for r in reports]
            self.assertEqual(seeds[0],seeds[1])

    def test_output_budget_is_bounded(self):
        with self.assertRaises(ValueError):
            paired.run('fixed',output_tokens=0)
        with self.assertRaises(ValueError):
            paired.run('fixed',output_tokens=16384)

    def test_notebook_replays_without_network_or_models(self):
        notebook=json.loads((CASE / 'notebooks' / 'paired-search.ipynb').read_text())
        scope={}
        with patch('urllib.request.urlopen',side_effect=AssertionError('Unexpected network')), patch('IPython.display.display'):
            for cell in notebook['cells']:
                if cell['cell_type']=='code':
                    self.assertIsInstance(cell['execution_count'],int)
                    self.assertFalse(any(o['output_type']=='error' for o in cell['outputs']))
                    exec(compile(''.join(cell['source']),'paired-notebook-cell','exec'),scope)
        self.assertEqual(len(scope['records']),2)

    def test_recorded_evidence_is_intact(self):
        for manifest_path in (CASE/'results').glob('*-paired-*/manifest.json'):
            folder=manifest_path.parent
            for name,digest in json.loads(manifest_path.read_text()).items():
                self.assertEqual(Path(name).name,name)
                self.assertEqual(paired.task.digest(folder/name),digest)
            protocol=json.loads((folder/'protocol.json').read_text())
            report=json.loads((folder/'report.json').read_text())
            calls=[json.loads(line) for line in (folder/'calls.jsonl').read_text().splitlines()]
            self.assertEqual(report['calls'],len(calls))
            self.assertEqual(report['tokens'],sum(c['input_tokens']+c['output_tokens'] for c in calls))
            self.assertEqual(report['tokens'],sum(e['tokens'] for e in report['events']))
            self.assertLessEqual(report['tokens'],protocol['limits']['total_tokens'])
            self.assertEqual(report['protected_source_changes'],0)
            for name,digest in protocol['source_hashes'].items():
                if 'base_commit' in protocol and 'source_storage' in protocol:
                    ref = f"{protocol['base_commit']}:research/cases/case-0003-debt-negotiation/{name}"
                    data = subprocess.check_output(['git', 'show', ref], cwd=CASE)
                    self.assertEqual(hashlib.sha256(data).hexdigest(), digest)
                else:
                    self.assertEqual(paired.task.digest(folder/Path(name).name),digest)


if __name__=='__main__': unittest.main()
