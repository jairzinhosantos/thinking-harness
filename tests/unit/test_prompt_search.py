"""Offline protocol, evaluator, provider-boundary, and notebook regressions."""
import importlib.util
import io
import json
import re
import yaml
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / 'research/proposals/case-0003-debt-negotiation'
spec = importlib.util.spec_from_file_location('case3_search', CASE / 'prompt_search.py')
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def config(**kwargs):
    return m.Config(**{'model':'test-only-model', 'input_usd_per_million':1,
                       'output_usd_per_million':2, 'max_iterations':2,
                       'evaluation_repeats':1, **kwargs})


class FakeClient:
    """Scripted test double, not an LLM or evidence of improvement."""
    instances = []
    def __init__(self, cfg, directory):
        self.tokens, self.cost, self.calls, self.uncertain = 0, 0.0, 0, False
        self.requests = []
        self.instances.append(self)

    def ask(self, role, instructions, payload, output_schema):
        self.calls += 1
        self.requests.append((role, instructions, payload))
        if role == 'optimizer':
            return {'prompt':'GOOD' if 'current_prompt' in payload else 'INITIAL'}
        if role == 'judge':
            return {'consistent': True, 'appropriate':True, 'clear':True, 'evidence':'Scripted test verdict'}
        if 'Policy:\nGOOD' in instructions:
            case = next(c for c in m.load_cases() if c['history'] == payload['history'])
            return {**case['expected'], 'message':case['reference_reply']}
        return {'action':'ask','debt':None,'payments':0,'installment':0,'message':'What can you afford?'}


class PromptSearchTests(unittest.TestCase):
    def setUp(self):
        self.cases = m.load_cases()
        self.case = next(c for c in self.cases if c['id']=='development-limited')

    def test_rules_reject_bad_amount_capacity_and_consent(self):
        reply = {**self.case['expected'], 'message':'Offer'}
        self.assertTrue(m.rule_check(self.case, reply)['task_match'])
        self.assertEqual(m.rule_check(self.case, reply)['violations'], [])
        reply.update(debt='C', installment=300)
        self.assertIn('exceeds_declared_capacity',m.rule_check(self.case, reply)['violations'])
        reply.update(action='accept',debt='B',installment=150)
        self.assertIn('fabricated_acceptance',m.rule_check(self.case, reply)['violations'])
        reply.update(action='offer', installment=149)
        self.assertIn('incorrect_installment',m.rule_check(self.case, reply)['violations'])

    def test_decline_unknown_and_malformed_outputs(self):
        decline=next(c for c in self.cases if c['id']=='development-declined')
        reply={'action':'offer','debt':'A','payments':2,'installment':100,'message':'Offer'}
        self.assertIn('ignores_explicit_stop',m.rule_check(decline,reply)['violations'])
        reply['payments']=True
        self.assertIn('invalid_fields',m.rule_check(decline,reply)['violations'])
        self.assertTrue(m.rule_check(self.case, {})['violations'])
        unknown=next(c for c in self.cases if c['id']=='development-unknown')
        self.assertIsNone(unknown['declared_capacity'])
        self.assertNotIn('reference_reply',m.visible(unknown))
        self.assertNotIn('expected',m.visible(unknown))

    def test_selection_gates_and_ties(self):
        incumbent={'score':0.5,'violations':0}
        self.assertFalse(m.better({'score':1,'violations':1},incumbent,0.01))
        self.assertFalse(m.better(incumbent,incumbent,0.01))
        self.assertTrue(m.better({'score':0.7,'violations':0},incumbent,0.01))

    def test_complete_search_and_optimizer_partition_isolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=m.run_search(config(),tmp,FakeClient)
            self.assertEqual(result['mode'],'offline_test_double')
            self.assertTrue(result['final_complete'])
            self.assertEqual(result['selected_prompt'],'GOOD')
            self.assertEqual(result['stop_reason'],'target_score')
            self.assertTrue((Path(result['evidence_dir'])/'report.json').exists())
        client=FakeClient.instances[-1]
        test_histories=[c['history'] for c in self.cases if c['split']=='test']
        for role,_,payload in client.requests:
            if role=='optimizer':
                self.assertEqual({c['split'] for c in payload['development']},{'development'})
                serialized=json.dumps(payload)
                for case in self.cases:
                    if case['split']!='development':
                        self.assertNotIn(json.dumps(case['history']),serialized)
            if role=='negotiator':
                self.assertEqual(set(payload),{'debts','allowed_payment_counts','history'})
        first_test=next(i for i,(role,_,p) in enumerate(client.requests)
                        if role=='negotiator' and p['history'] in test_histories)
        self.assertNotIn('optimizer',[role for role,_,_ in client.requests[first_test:]])

    def test_baseline_at_target_skips_search(self):
        class GoodInitial(FakeClient):
            def ask(self,role,instructions,payload,output_schema):
                result=super().ask(role,instructions,payload,output_schema)
                return {'prompt':'GOOD'} if role=='optimizer' else result
        with tempfile.TemporaryDirectory() as tmp:
            result=m.run_search(config(),tmp,GoodInitial)
        self.assertTrue(result['final_complete'])
        self.assertEqual(result['events'],[])
        self.assertEqual(result['initial_prompt'],result['selected_prompt'])

    def test_no_improvement_retains_baseline_and_stops_on_patience(self):
        class Duplicate(FakeClient):
            def ask(self,role,*args):
                result=super().ask(role,*args)
                return {'prompt':'INITIAL'} if role=='optimizer' else result
        with tempfile.TemporaryDirectory() as tmp:
            result=m.run_search(config(patience=1),tmp,Duplicate)
        self.assertEqual(result['stop_reason'],'patience')
        self.assertEqual(result['initial_prompt'],result['selected_prompt'])
        self.assertTrue(result['final_complete'])
        self.assertTrue(any(e.get('status')=='duplicate' for e in result['events']))

    @patch.dict('os.environ',{'OPENAI_API_KEY':'test-placeholder'})
    def test_cost_guard_and_incomplete_output_accounting(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(m.urllib.request,'urlopen') as call:
            client=m.ResponsesClient(config(allow_live=True,max_cost_usd=0.000001),tmp)
            with self.assertRaises(m.BudgetStop):
                client.ask('optimizer','fixed',{},m.PROMPT_SCHEMA)
            call.assert_not_called()
        response={'status':'incomplete','usage':{'input_tokens':12,'output_tokens':30},'output':[]}
        with tempfile.TemporaryDirectory() as tmp, patch.object(m.urllib.request,'urlopen',return_value=io.BytesIO(json.dumps(response).encode())):
            client=m.ResponsesClient(config(allow_live=True),tmp)
            with self.assertRaises(m.ProviderFailure):
                client.ask('optimizer','fixed',{},m.PROMPT_SCHEMA)
            self.assertEqual(client.tokens,42)
            self.assertIn('incomplete',(Path(tmp)/'calls.jsonl').read_text())

    def test_budget_stop_does_not_claim_final_result(self):
        class Exhausted(FakeClient):
            def ask(self,*args):
                if self.calls>=3:
                    raise m.BudgetStop()
                return super().ask(*args)
        with tempfile.TemporaryDirectory() as tmp:
            result=m.run_search(config(),tmp,Exhausted)
            saved=json.loads((Path(result['evidence_dir'])/'report.json').read_text())
        self.assertFalse(saved['final_complete'])
        self.assertEqual(saved['stop_reason'],'budget')

    def test_semantic_mismatch_blocks_structurally_correct_response(self):
        class BadJudge(FakeClient):
            def ask(self,role,*args):
                result=super().ask(role,*args)
                if role=='judge': result['consistent']=False
                return result
        result=m.evaluate(BadJudge(config(),None),'GOOD',[self.case],1)
        self.assertEqual(result['score'],0)
        self.assertEqual(result['violations'],1)

    def test_invalid_config_and_live_opt_in(self):
        with self.assertRaises(ValueError): config(max_cost_usd=float('nan')).validate()
        with self.assertRaises(ValueError): config(max_iterations=0).validate()
        with self.assertRaises(ValueError): config(model='').validate()
        with self.assertRaises(ValueError): m.ResponsesClient(config(),Path('/tmp'))

    @patch.dict('os.environ',{'OPENAI_API_KEY':'test-placeholder'})
    def test_budget_preflight_sends_no_request(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(m.urllib.request,'urlopen') as call:
            client=m.ResponsesClient(config(allow_live=True,max_total_tokens=10),tmp)
            with self.assertRaises(m.BudgetStop):
                client.ask('optimizer','fixed',{},m.PROMPT_SCHEMA)
            call.assert_not_called()

    @patch.dict('os.environ',{'OPENAI_API_KEY':'test-placeholder'})
    def test_transport_failure_stops_without_retry_or_secret_log(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(m.urllib.request,'urlopen',side_effect=TimeoutError) as call:
            client=m.ResponsesClient(config(allow_live=True),tmp)
            for _ in range(2):
                with self.assertRaises(m.ProviderFailure):
                    client.ask('optimizer','fixed',{},m.PROMPT_SCHEMA)
            self.assertEqual(call.call_count,1)
            self.assertTrue(client.uncertain)
            self.assertGreater(client.tokens,0)
            self.assertNotIn('test-placeholder',(Path(tmp)/'calls.jsonl').read_text())

    @patch.dict('os.environ',{'OPENAI_API_KEY':'test-placeholder'})
    def test_provider_accounting_and_structured_request(self):
        response={'status':'completed','model':'test-only-model',
                  'usage':{'input_tokens':10,'output_tokens':20},
                  'output':[{'type':'message','content':[{'type':'output_text','text':'{"prompt":"seed"}'}]}]}
        with tempfile.TemporaryDirectory() as tmp, patch.object(m.urllib.request,'urlopen',return_value=io.BytesIO(json.dumps(response).encode())) as call:
            client=m.ResponsesClient(config(allow_live=True),tmp)
            self.assertEqual(client.ask('optimizer','fixed',{},m.PROMPT_SCHEMA),{'prompt':'seed'})
            self.assertEqual(client.tokens,30)
            self.assertAlmostEqual(client.cost,0.00005)
            body=json.loads(call.call_args.args[0].data)
            self.assertFalse(body['store'])
            self.assertTrue(body['text']['format']['strict'])
            self.assertNotIn('previous_response_id',body)

    def test_notebook_offline_path_never_calls_network(self):
        for name in ('prompt-search.ipynb', 'prompt-search.es.ipynb'):
            self.check_offline_notebook(name)

    def check_offline_notebook(self, name):
        notebook=json.loads((CASE/name).read_text())
        self.assertEqual(notebook['nbformat'],4)
        scope={}
        display=types.ModuleType('IPython.display')
        display.display=lambda *args: None
        display.Markdown=display.HTML=lambda value:value
        with patch.dict(sys.modules,{'IPython':types.ModuleType('IPython'),'IPython.display':display}), \
             patch.object(m.urllib.request,'urlopen',side_effect=AssertionError('Unexpected network call')):
            for cell in notebook['cells']:
                if cell['cell_type']=='code':
                    self.assertEqual(cell['outputs'],[])
                    self.assertIsNone(cell['execution_count'])
                    exec(compile(''.join(cell['source']),'notebook-cell','exec'),scope)
        self.assertFalse(scope['RUN_LIVE'])
        self.assertIsNone(scope['report'])


    def test_yaml_version_lineage_and_candidate_tie_selection(self):
        original=(CASE/'prompt.yaml').read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            result=m.run_search(config(),tmp,FakeClient)
            versions=result['versions']
            self.assertEqual([v['id'] for v in versions],['p000','p001','p002','p003'])
            self.assertEqual([v['parent'] for v in versions],[None,'p000','p001','p001'])
            self.assertEqual(result['initial_version'],'p001')
            self.assertEqual(result['selected_version'],'p002')
            self.assertEqual(sum(e.get('selected',False) for e in result['events']),1)
            for version in versions:
                path=Path(result['evidence_dir'])/version['path']
                self.assertEqual(yaml.safe_load(path.read_text()),{'prompt':version['prompt']})
                self.assertEqual(m.hashlib.sha256(path.read_bytes()).hexdigest(),version['sha256'])
            self.assertIn('golden-set.yaml',result['source_hashes'])
            self.assertIn('prompt.yaml',result['source_hashes'])
        self.assertEqual((CASE/'prompt.yaml').read_bytes(),original)

    def test_disabled_live_switch_and_candidate_schema(self):
        cfg=m.Config(**yaml.safe_load((CASE/'config.yaml').read_text()))
        cfg.validate()
        self.assertFalse(cfg.allow_live)
        with patch.object(m.urllib.request,'urlopen') as network:
            with self.assertRaises(ValueError): m.run_search(cfg)
            network.assert_not_called()
        for candidate in ({'prompt':''},{'prompt':'hello','budget':100},{'prompt':None}):
            with self.assertRaises(m.ProviderFailure): m.get_prompt(candidate)

    def test_bilingual_code_and_local_links(self):
        notebooks=[json.loads((CASE/name).read_text())
                   for name in ('prompt-search.ipynb','prompt-search.es.ipynb')]
        code=[]
        for notebook in notebooks:
            code.append([''.join(c['source']).splitlines() for c in notebook['cells']
                         if c['cell_type']=='code'])
            for cell in notebook['cells']:
                if cell['cell_type']=='markdown':
                    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', ''.join(cell['source'])):
                        if not target.startswith(('https:', 'attachment:')):
                            self.assertTrue((CASE/target.split('#')[0]).exists(),target)
        self.assertNotEqual(code[0][0][0],code[1][0][0])
        code[0][0][0]=code[1][0][0]
        self.assertEqual(code[0],code[1])

    def test_notebook_version_and_trace_display_with_test_evidence(self):
        # Exercise presentation with a marked test double; never publish this as a live run.
        notebook=json.loads((CASE/'prompt-search.ipynb').read_text())
        cells=[''.join(c['source']) for c in notebook['cells'] if c['cell_type']=='code']
        display=types.ModuleType('IPython.display')
        rendered=[]
        display.display=lambda value: rendered.append(value)
        display.Markdown=display.HTML=lambda value:value
        with tempfile.TemporaryDirectory() as tmp, patch.dict(sys.modules,{'IPython.display':display}), \
             patch.object(m.urllib.request,'urlopen',side_effect=AssertionError('Unexpected network call')):
            result=m.run_search(config(),tmp,FakeClient)
            scope={}
            exec(cells[0],scope)
            scope.update(report=result,report_path=Path(result['evidence_dir'])/'report.json')
            for cell in cells[4:]: exec(cell,scope)
            self.assertTrue(any('p003' in str(item) for item in rendered))
            self.assertTrue(any('Scripted test verdict' in str(item) for item in rendered))
            self.assertEqual(result['mode'],'offline_test_double')

if __name__=='__main__':
    unittest.main()
