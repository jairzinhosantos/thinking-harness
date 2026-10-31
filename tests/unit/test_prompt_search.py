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
CASE = ROOT / 'research/cases/case-0003-debt-negotiation'
spec = importlib.util.spec_from_file_location('case3_search', CASE / 'utils/prompt_search.py')
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
        for name in ('prompt-search.ipynb',):
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
                    self.assertIsInstance(cell['execution_count'], int)
                    self.assertFalse(any(o['output_type']=='error' for o in cell['outputs']))
                    exec(compile(''.join(cell['source']),'notebook-cell','exec'),scope)
        self.assertFalse(scope['RUN_LIVE'])
        self.assertFalse(scope['config'].allow_live)
        self.assertEqual(scope['report']['mode'],'live')
        self.assertEqual(scope['report']['run_id'],notebook['metadata']['evidence']['report'].split('/')[1])


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
            self.assertIn('utils/prompt_search.py',result['source_hashes'])
            for source, digest in result['source_hashes'].items():
                self.assertEqual(m.hashlib.sha256((CASE/source).read_bytes()).hexdigest(), digest)
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

    def test_canonical_spanish_notebook_and_local_links(self):
        self.assertEqual(sorted(p.name for p in CASE.glob('*.ipynb')), ['harness-smoke-test.ipynb', 'prompt-search.ipynb'])
        notebook=json.loads((CASE/'prompt-search.ipynb').read_text())
        first_code=next(''.join(c['source']) for c in notebook['cells'] if c['cell_type']=='code')
        self.assertIn("LANGUAGE = 'es'", first_code)
        for cell in notebook['cells']:
            if cell['cell_type']=='markdown':
                for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', ''.join(cell['source'])):
                    if not target.startswith(('https:', 'attachment:')):
                        self.assertTrue((CASE/target.split('#')[0]).exists(),target)

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


    def test_notebook_reading_content_and_diagram_provenance(self):
        import base64
        for name in ('prompt-search.ipynb',):
            notebook = json.loads((CASE/name).read_text())
            prose = '\n'.join(''.join(c['source']) for c in notebook['cells'] if c['cell_type'] == 'markdown')
            for internal in ('OPENAI_API_KEY', 'RUN_LIVE', 'REPLAY_REPORT', 'allow_live', '```mermaid', 'Regenerar'):
                self.assertNotIn(internal, prose)
            diagrams = [c for c in notebook['cells'] if 'diagram' in c['metadata']]
            self.assertEqual(len(diagrams), 1)
            for cell in diagrams:
                manifest = cell['metadata']['diagram']
                source = CASE / manifest['source']
                preview = base64.b64decode(cell['attachments']['workflow.png']['image/png'])
                self.assertEqual(m.hashlib.sha256(source.read_bytes()).hexdigest(), manifest['source_sha256'])
                self.assertEqual(m.hashlib.sha256(preview).hexdigest(), manifest['preview_sha256'])
        guide = (CASE/'README.md').read_text()
        for internal in ('OPENAI_API_KEY', 'RUN_LIVE', 'REPLAY_REPORT', 'allow_live', 'ipykernel install'):
            self.assertNotIn(internal, guide)

    def test_presentation_escapes_untrusted_prompt_and_judge_text(self):
        display = types.ModuleType('IPython.display')
        rendered = []
        display.display = rendered.append
        display.HTML = lambda value: value
        with patch.dict(sys.modules, {'IPython.display': display}):
            view_spec = importlib.util.spec_from_file_location('case_view_test', CASE/'utils/notebook_view.py')
            view_module = importlib.util.module_from_spec(view_spec)
            view_spec.loader.exec_module(view_module)
            view = view_module.EvidenceView('es')
            self.assertEqual(view.paragraphs('<script>alert(1)</script>'),
                             '<p>&lt;script&gt;alert(1)&lt;/script&gt;</p>')
            self.assertIn('&lt;img', view.table(['Text'], [['<img src=x>']]))

    def test_published_live_evidence_is_consistent_and_shared(self):
        notebook=json.loads((CASE/'prompt-search.ipynb').read_text())
        evidence=notebook['metadata']['evidence']
        path=CASE/evidence['report']
        self.assertEqual(m.hashlib.sha256(path.read_bytes()).hexdigest(),evidence['sha256'])
        report=json.loads(path.read_text())
        self.assertEqual(report['mode'],'live')
        self.assertFalse(report['usage']['uncertain'])
        versions={v['id']:v for v in report['versions']}
        self.assertEqual(len(versions),len(report['versions']))
        for version in versions.values():
            policy=path.parent/version['path']
            self.assertEqual(m.hashlib.sha256(policy.read_bytes()).hexdigest(),version['sha256'])
            self.assertEqual(yaml.safe_load(policy.read_text()),{'prompt':version['prompt']})
            if version['parent'] is not None: self.assertIn(version['parent'],versions)
        self.assertEqual(versions[report['selected_version']]['prompt'],report['selected_prompt'])
        ledger=[json.loads(line) for line in (path.parent/'usage.jsonl').read_text().splitlines()]
        received=[row for row in ledger if row['stage']=='received']
        self.assertEqual(len(received),report['usage']['calls'])
        self.assertEqual(sum(row['usage']['input_tokens']+row['usage']['output_tokens'] for row in received),report['usage']['tokens'])
        self.assertAlmostEqual(sum(row['estimated_cost_usd'] for row in received),report['usage']['estimated_cost_usd'])
        evaluations=[report['initial_validation']]
        for event in report['events']:
            evaluations.extend(event[key] for key in ('development','validation') if key in event)
        for result in evaluations:
            self.assertAlmostEqual(result['score'],sum(row['success'] for row in result['rows'])/len(result['rows']))
            self.assertEqual(result['violations'],sum(bool(row['violations']) for row in result['rows']))
        self.assertFalse(report['final_complete'])
        self.assertNotIn('final_selected',report)
        self.assertEqual(report['selected_version'],report['initial_version'])
        self.assertFalse(any(event.get('selected') for event in report['events']))
        provenance=json.loads((path.parent/'provenance.json').read_text())
        guard=provenance['budget_diagnosis']
        self.assertGreater(guard['projected_tokens'],guard['limit'])
        self.assertEqual(guard['consumed_tokens'],report['usage']['tokens'])

    def test_objective_extraction_excludes_results_and_rejects_bad_boundaries(self):
        objective=m.load_objective()
        self.assertIn('mayor deuda viable',objective)
        self.assertNotIn('83 815',objective)
        self.assertNotIn('Resultados registrados',objective)
        self.assertNotIn('Modelamiento',objective)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'README.md'
            path.write_text('private outcomes\n<!-- objective:start -->\nfixed objective\n<!-- objective:end -->\nvalidation failures')
            self.assertEqual(m.load_objective(path),'fixed objective')
            for invalid in ('missing markers', '<!-- objective:start --><!-- objective:end -->',
                            '<!-- objective:end -->text<!-- objective:start -->',
                            '<!-- objective:start -->a<!-- objective:start -->b<!-- objective:end -->'):
                path.write_text(invalid)
                with self.assertRaises(ValueError): m.load_objective(path)

    def test_case_has_one_spanish_markdown_and_legacy_evidence_is_distinct(self):
        markdown=[p.relative_to(CASE).as_posix() for p in CASE.rglob('*.md')
                  if not {'runs','_local','.venv'} & set(p.relative_to(CASE).parts)]
        self.assertEqual(markdown,['README.md'])
        self.assertEqual(m.PROTOCOL,'case-0003-prompt-search-v3')
        self.assertIn('case-0003-prompt-search-v2',m.REPLAY_PROTOCOLS)
        with tempfile.TemporaryDirectory() as tmp:
            result=m.run_search(config(),tmp,FakeClient)
            self.assertEqual(result['protocol'],m.PROTOCOL)
            self.assertEqual(result['objective_sha256'],m.hashlib.sha256(m.load_objective().encode()).hexdigest())
            self.assertIn('README.md',result['source_hashes'])
            for role,_,payload in FakeClient.instances[-1].requests:
                if role=='optimizer': self.assertEqual(payload['objective'],m.load_objective())

if __name__=='__main__':
    unittest.main()
