"""Paired five-proposal B1/B2 pilot with local Qwen and isolated evaluation cases."""
import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import time

import models
import task

CASE = task.CASE_DIR
PROTOCOL = 'case-0003-output-budget-v1'
SAMPLING = {'temperature': .6, 'top_p': .95, 'top_k': 20, 'enable_thinking': True, 'seed': 11}
LIMITS = {**models.LIMITS, 'iterations': 5, 'calls': 90, 'output_tokens': 2048,
          'context_tokens': 6144, 'total_tokens': 180000, 'seconds': 1800}
SEARCH_TOKENS = 120000
FINAL_TOKENS = 60000


def fixtures():
    return json.loads((CASE / 'paired-search-cases.yaml').read_text())


def run(strategy, output_root=None, client_factory=None, *, output_tokens=2048, decoding="prompt_only", model="qwen3-8b", allow_live=False):
    if strategy not in ('fixed', 'adaptive'):
        raise ValueError('Unknown strategy')
    if output_tokens not in (2048, 4096, 8192):
        raise ValueError('Output limit must be 2048, 4096 or 8192')
    limits = {**LIMITS, 'output_tokens': output_tokens,
              'context_tokens': output_tokens + 4096}
    if decoding not in ('prompt_only', 'json_schema'):
        raise ValueError('Unknown decoding mode')
    is_api = model == 'gpt-4o-mini-2024-07-18'
    if model not in models.MODELS and not is_api:
        raise ValueError('Unknown model')
    real_client = client_factory in (None, models.LocalClient, models.ApiClient)
    if is_api and real_client and not allow_live:
        raise ValueError('API execution requires --allow-live')
    if client_factory is None:
        client_factory = models.ApiClient if is_api else models.LocalClient
    sampling = {'temperature': .6} if is_api else SAMPLING
    if is_api:
        if decoding != 'prompt_only':
            raise ValueError('API already uses its native JSON schema')
        limits['context_tokens'] = 32768
    if decoding == 'json_schema' and client_factory is models.LocalClient:
        from structured_output import StructuredLocalClient
        client_factory = StructuredLocalClient
    cases = fixtures()
    sources = [Path(__file__), Path(models.__file__), Path(task.__file__), CASE / 'paired-search-cases.yaml']
    if decoding == 'json_schema':
        sources.append(Path(__file__).with_name('structured_output.py'))
    provenance = task.source_record(sources, require_clean=real_client)
    hashes = provenance['source_hashes']
    repo, revision = (model, None) if is_api else models.MODELS[model]
    snapshot = None if is_api else Path.home() / '.cache/huggingface/hub' / ('models--'+repo.replace('/','--')) / 'snapshots' / revision
    folder = Path(output_root or CASE / 'results') / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-paired-'+model+'-'+strategy+('-tokens-'+str(output_tokens) if output_tokens != 2048 else '')+('-structured' if decoding == 'json_schema' else ''))
    folder.mkdir(parents=True, exist_ok=False)
    protocol = {'protocol': 'case-0003-structured-search-v1' if decoding == 'json_schema' else PROTOCOL, 'strategy': strategy, 'model': repo, 'revision': revision,
        'decoding': decoding,
        'schema_constraint': 'Mask final JSON only after </think>, in all three roles. Nullable string enum compiled as equivalent anyOf; up to 12 consecutive whitespace characters, free field order. No repair, retry, forced answer or expected labels. Free reasoning and post-generation validation retained.' if decoding == 'json_schema' else 'Prompt instructions only; post-generation validation.',
        'sampling': sampling, 'limits': limits, 'search_tokens': SEARCH_TOKENS, 'final_tokens': FINAL_TOKENS,
        'cases': cases, 'objective': task.OBJECTIVE, 'initial_policy': task.INITIAL_POLICY,
        'initial_strategy': task.INITIAL_STRATEGY, 'runtime': task.DECISION_RUNTIME,
        'proposal_contract': task.PROPOSAL_CONTRACT+task.NOVELTY_CONTRACT,
        'update_contract': task.UPDATE_CONTRACT, 'source_hashes': hashes,
        'model_files_sha256': {p.name: task.digest(p) for p in snapshot.iterdir() if p.is_file()} if snapshot and snapshot.exists() else {},
        'selection': 'Validation Q gain >= 0.01 and V=0; keep incumbent on ties. Development feedback only is sent to proposer/updater.',
        'criterion': 'Final selected test Q >= 0.80 and V=0. Target reached during search is validation only, not confirmation.',
        'pairing': 'Same initial policy, strategy, inference, fixtures and limits. Evaluation seed=11+1000*split_index+case_index, reset for each call, independent of policy/iteration/condition. Proposal seed=10011+iteration, update seed=20011+iteration.',
        'duplicates': 'NFC/whitespace duplicates reuse scores; never accepted. Same seeds make this reuse consistent within the pilot.',
        'invalid_output': 'Invalid proposal counts as one attempt, keeps incumbent, no updater for that attempt. Invalid update keeps current strategy. No automatic request retry.',
        'stop': 'Five proposal attempts, search-token limit or runtime/source failure. Final evaluation has a separate 60000-token reserve within the 180000 total and 1800-second cap.',
        'final': 'Test evaluated only after selection; new for Test 4, reused for output-budget tuning. Evaluate H0 and selected on same case seeds. Reuse baseline if H0 remains selected. No post-test changes.',
        'scope': 'One paired search per condition; no significance or superiority claim. Test 4 cases are already known; no new confirmation claim. Manual policy from Test 3 is not supplied to either search. Structured decisions only; messages use fixed renderer.',
        'output_budget_comparison': {'output_tokens': output_tokens,
            'meaning': 'Maximum new tokens per call, including reasoning and final JSON; EOS may stop earlier.',
            'context': '4096 input-token headroom plus output reserve. No truncation or extra input context is added.',
            'known_test': True,
            'interpretation': 'Runs reuse inspected Test 4 cases: exploratory tuning, not fresh confirmation.',
            'escalation': 'Run 4096 for both conditions; try 8192 only if output_limit persists. Stop after that bounded pair. No automatic model scaling.'},
        'human_edits_during_search': 0, 'provider': 'openai' if is_api else 'mlx',
        'api_budget_usd': .50 if is_api else 0, 'api_pricing_per_million': {'input': .15, 'output': .60} if is_api else None,
        **provenance,
        'packages': {n:importlib.metadata.version(n) for n in ('jsonschema','PyYAML') + (('tiktoken',) if is_api else ('mlx','mlx-lm','transformers','tokenizers')) + (('lm-format-enforcer','pydantic','interegular') if decoding == 'json_schema' else ())}}
    protocol['model_key'] = model
    if is_api:
        protocol.update(protocol='case-0003-api-paired-v1', decoding='api_json_schema',
            pairing='Same task, prompts, cases, evaluator and budgets; no API seed control.',
            schema_constraint='Native Responses JSON schema; no repair or retry.',
            duplicates='Exact NFC/whitespace duplicates reuse the first observed scores; no API determinism assumed.',
            output_budget_comparison={'output_tokens': output_tokens, 'context_tokens': limits['context_tokens'],
                'known_test': True, 'interpretation': 'Exploratory API comparison on known cases; no fresh confirmation.'})
    task.write_json(folder/'protocol.json', protocol)
    (folder/'calls.jsonl').touch()
    report = {'status':'running','strategy':strategy,'rounds':[],'strategy_updates':[],
              'events':[], 'selected_iteration':0, 'first_validation_target':None}
    client = None
    started = time.monotonic()
    iteration = 0

    def checkpoint():
        task.write_json(folder/'report.json', report)

    def ask(role, instructions, payload, schema, seed, phase):
        if any(task.digest(CASE/name)!=digest for name,digest in hashes.items()):
            raise ValueError('Protected source changed')
        client.seed(seed)
        client.sampling = {**sampling,'seed':seed}
        before_calls, before_tokens = client.calls, client.tokens
        try:
            return client.ask(role,instructions,payload,schema)
        finally:
            report['events'].append({'iteration':iteration,'role':role,'phase':phase,'seed':None if is_api else seed,
                'call':client.calls if client.calls>before_calls else None,
                'tokens':client.tokens-before_tokens,'cumulative_tokens':client.tokens,
                'elapsed_seconds':time.monotonic()-started})
            checkpoint()

    def evaluate(policy, split):
        rows=[]
        split_index={'development':1,'validation':2,'test':3}[split]
        for index,case in enumerate(cases[split]):
            reply,error=ask('negotiator',task.DECISION_RUNTIME+task.POLICY_SEPARATOR+policy,
                task.visible(case),task.DECISION_SCHEMA,11+1000*split_index+index,split)
            check={'task_match':False,'violations':[error]} if error else task.rule_check(case,task.render_decision(reply))
            rows.append({'id':case['id'],'context':task.visible(case),'expected':case['expected'],
                'raw_reply':reply,**check,'success':check['task_match'] and not check['violations']})
        return task.summarize(rows)

    try:
        client=client_factory(model,folder,snapshot,started,sampling=sampling,
                              limits={**limits,'total_tokens':SEARCH_TOKENS})
        policy,strategy_text=task.INITIAL_POLICY,task.INITIAL_STRATEGY
        incumbent={'iteration':0,'policy':policy,'strategy_used':strategy_text,
            'policy_tokens':client.length(policy),'strategy_tokens':client.length(strategy_text),
            'development':evaluate(policy,'development'),'validation':evaluate(policy,'validation'),'accepted':True}
        report['rounds'].append(incumbent)
        seen={task.policy_key(policy):incumbent}
        checkpoint()
        try:
            for iteration in range(1,6):
                history=[{'policy':r['policy'],'development_failures':[
                    {'id':row['id'],'task_match':row['task_match'],'violations':row['violations']}
                    for row in r['development']['rows']]} for r in report['rounds'][1:] if 'development' in r][-2:]
                value,error=ask('proposer',task.PROPOSAL_CONTRACT+strategy_text+task.NOVELTY_CONTRACT,
                    {'objective':task.OBJECTIVE,'current_policy':policy,'recent_attempts':history,
                     'development_feedback':incumbent['development']['rows']},task.PROMPT_SCHEMA,10011+iteration,'search')
                if not error:
                    try:
                        proposal=task.get_prompt(value)
                    except task.ProviderFailure:
                        error='invalid_prompt'
                if error:
                    report['rounds'].append({'iteration':iteration,'accepted':False,'error':error,
                        'strategy_used':strategy_text,'proposal':value})
                    checkpoint()
                    print(strategy,'proposal',iteration,'invalid:',error,flush=True)
                    continue
                previous=seen.get(task.policy_key(proposal))
                candidate={'iteration':iteration,'parent_iteration':incumbent['iteration'],'policy':proposal,
                    'policy_tokens':client.length(proposal),'strategy_used':strategy_text,
                    'strategy_tokens':client.length(strategy_text),'duplicate_of':previous['iteration'] if previous else None,
                    'development':previous['development'] if previous else evaluate(proposal,'development'),
                    'validation':previous['validation'] if previous else evaluate(proposal,'validation')}
                candidate['accepted']=previous is None and task.choose(candidate['validation'],incumbent['validation'],.01)
                if previous is None:
                    seen[task.policy_key(proposal)]=candidate
                report['rounds'].append(candidate)
                if candidate['accepted']:
                    policy,incumbent=proposal,candidate
                    report['selected_iteration']=iteration
                if report['first_validation_target'] is None and incumbent['validation']['q']>=.8 and incumbent['validation']['v']==0:
                    report['first_validation_target']={'iteration':iteration,'tokens':client.tokens,'elapsed_seconds':time.monotonic()-started}
                checkpoint()
                print(strategy,'proposal',iteration,'validation Q=',candidate['validation']['q'],'accepted=',candidate['accepted'],flush=True)
                if strategy=='adaptive' and iteration<5:
                    value,error=ask('strategy_update',task.UPDATE_CONTRACT,
                        {'objective':task.OBJECTIVE,'current_strategy':strategy_text,
                         'candidate_policy':proposal,'development_feedback':candidate['development']['rows']},
                         task.PROMPT_SCHEMA,20011+iteration,'search')
                    updated=strategy_text
                    if not error:
                        try:
                            updated=task.get_prompt(value)
                        except task.ProviderFailure:
                            error='invalid_prompt'
                    report['strategy_updates'].append({'after_iteration':iteration,'before':strategy_text,'after':updated,
                        'changed':updated!=strategy_text,'error':error})
                    strategy_text=updated
                    checkpoint()
            report['search_status']='completed'
        except task.BudgetStop:
            report['search_status']='budget_exhausted'
        report['search_tokens']=client.tokens
        report['search_seconds']=time.monotonic()-started
        report['selected_policy']=policy
        report['selected_strategy']=strategy_text
        checkpoint()
        client.limits['total_tokens']=min(limits['total_tokens'],client.tokens+FINAL_TOKENS)
        baseline=evaluate(task.INITIAL_POLICY,'test')
        selected=evaluate(policy,'test') if report['selected_iteration'] else baseline
        report['test']={'initial':baseline,'selected':selected,'selected_reuses_initial':report['selected_iteration']==0}
        report['passes']=selected['q']>=.8 and selected['v']==0
        report['status']='completed' if report['search_status']=='completed' else 'search_limited_final_complete'
    except (task.BudgetStop,task.ProviderFailure,ValueError,RuntimeError) as exc:
        report.update(status='stopped',error_type=type(exc).__name__)
    finally:
        report.update(calls=client.calls if client else 0,tokens=client.tokens if client else 0,
            elapsed_seconds=time.monotonic()-started,peak_mlx_gb=client.peak_memory() if client else None,
            estimated_cost_usd=getattr(client, 'cost', 0), usage_uncertain=getattr(client, 'uncertain', False),
            protected_source_changes=sum(task.digest(CASE/name)!=digest for name,digest in hashes.items()))
        checkpoint()
        task.write_json(folder/'manifest.json',{p.name:task.digest(p) for p in folder.iterdir() if p.is_file() and p.name!='manifest.json'})
    return folder


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--strategy',choices=('fixed','adaptive'),required=True)
    parser.add_argument('--output-tokens', type=int, choices=(2048,4096,8192), default=2048)
    parser.add_argument('--decoding', choices=('prompt_only','json_schema'), default='prompt_only')
    parser.add_argument('--model', choices=(*models.MODELS, 'gpt-4o-mini-2024-07-18'), default='qwen3-8b')
    parser.add_argument('--allow-live', action='store_true')
    args=parser.parse_args()
    print(run(args.strategy, output_tokens=args.output_tokens, decoding=args.decoding, model=args.model, allow_live=args.allow_live))
