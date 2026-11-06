"""Bounded local inference tuning with a frozen manual policy and separate confirmation."""
import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import time
import yaml

import local_model_test as local

CASE = local.CASE_DIR
PROTOCOL = "case-0003-inference-tuning-v1"
PROFILES = [{"temperature": t, "top_p": .8, "top_k": 20} for t in (0., .3, .7)]
SEEDS = (11, 22, 33)
LIMITS = {**local.LIMITS, "calls": 108, "total_tokens": 150000, "seconds": 1800,
          "output_tokens": 512, "iterations": 0, "mlx_memory_bytes": 28 * 1024**3}


def grid():
    return [{**p, "seed": seed} for p in PROFILES for seed in (SEEDS[:1] if p['temperature'] == 0 else SEEDS)]


def summarize_profiles(evaluations):
    summaries = []
    for profile in PROFILES:
        runs = [r for r in evaluations if all(r['sampling'][k] == v for k, v in profile.items())]
        if len(runs) != (1 if profile['temperature'] == 0 else len(SEEDS)):
            continue
        rows = [row for r in runs for row in r['rows']]
        q = sum(r['success'] for r in rows) / len(rows)
        v = sum(bool(r['violations']) for r in rows) / len(rows)
        summaries.append({"sampling": profile, "q": q, "v": v,
                          "successes": sum(r['success'] for r in rows), "count": len(rows),
                          "passes": q >= .8 and v == 0})
    return summaries


def select_profile(summaries):
    # Prefer zero violations, then success rate; ties use lower temperature.
    return max(summaries, key=lambda r: (r['v'] == 0, r['q'], -r['v'], -r['sampling']['temperature']))


def read_record(folder):
    folder = Path(folder)
    manifest = json.loads((folder / 'manifest.json').read_text())
    for name, digest in manifest.items():
        if Path(name).name != name or local.smoke.digest(folder / name) != digest:
            raise ValueError('Invalid evidence manifest')
    return json.loads((folder / 'protocol.json').read_text()), json.loads((folder / 'report.json').read_text())


def run(key='qwen3-8b', confirmation_of=None, output_root=None, client_factory=local.LocalClient, *, thinking=False):
    source = None
    if confirmation_of:
        previous_protocol, previous = read_record(confirmation_of)
        if previous['status'] != 'completed' or previous_protocol['phase'] != 'tuning' or previous_protocol['model_key'] != key:
            raise ValueError('Confirmation requires completed matching tuning evidence')
        if (previous_protocol['policy'] != local.REFERENCE_POLICY
                or previous_protocol['runtime'] != local.DECISION_RUNTIME
                or previous_protocol['revision'] != local.MODELS[key][1]
                or any(local.smoke.digest(CASE / name) != digest
                       for name, digest in previous_protocol['source_hashes'].items()
                       if name != 'utils/inference_tuning.py')):
            raise ValueError('Confirmation policy, model, evaluator or fixtures changed')
        if not previous['selected']['passes']:
            raise ValueError('Selected profile must pass tuning before confirmation')
        sampling = previous['selected']['sampling']
        thinking = previous_protocol['enable_thinking']
        configurations = [{**sampling, 'seed': seed} for seed in SEEDS]
        source = Path(confirmation_of).name
        cases = yaml.safe_load((CASE / 'inference-confirmation-cases.yaml').read_text())['cases']
    else:
        configurations = ([{'temperature': .6, 'top_p': .95, 'top_k': 20, 'seed': 11,
                            'enable_thinking': True}] if thinking else grid())
        cases = [c for group in local.smoke.select_cases().values() for c in group] + local.transfer_cases()
    phase = 'confirmation' if confirmation_of else 'tuning'
    folder = Path(output_root or CASE / 'results') / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-inference-' + key + ('-thinking' if thinking else '') + '-' + phase)
    folder.mkdir(parents=True, exist_ok=False)
    repo, revision = local.MODELS[key]
    snapshot = Path.home() / '.cache/huggingface/hub' / ('models--' + repo.replace('/', '--')) / 'snapshots' / revision
    sources = [Path(__file__), Path(local.__file__), Path(local.smoke.__file__),
               Path(local.__file__).with_name('prompt_search.py'), CASE / 'harness-test-cases.yaml',
               CASE / 'local-transfer-cases.yaml', CASE / 'inference-confirmation-cases.yaml']
    hashes = {str(p.relative_to(CASE)): local.smoke.digest(p) for p in sources}
    limits = {**LIMITS, **({'output_tokens': 2048, 'context_tokens': 6144} if thinking else {})}
    protocol = {'protocol': PROTOCOL + ('-thinking' if thinking else ''), 'phase': phase, 'model_key': key, 'model': repo, 'revision': revision,
        'sampling_grid': configurations, 'limits': limits, 'policy': local.REFERENCE_POLICY,
        'runtime': local.DECISION_RUNTIME, 'cases': cases, 'source_hashes': hashes,
        'model_files_sha256': {p.name: local.smoke.digest(p) for p in snapshot.iterdir() if p.is_file()} if snapshot.exists() else {},
        'confirmation_of': source, 'confirmation_manifest_sha256': local.smoke.digest(Path(confirmation_of) / 'manifest.json') if confirmation_of else None,
        'enable_thinking': thinking, 'quantization': '4-bit', 'fine_tuning': False, 'api_calls': 0,
        'criterion': 'Q >= 0.80 and zero observed rule violations; provisional pilot criterion, not reliability certification.',
        'selection': 'Zero violations first; then highest Q, lowest violation rate and lower temperature. All tuning trials retained.',
        'stop': 'One finite grid, no retry; abort on resource or source-integrity failure.',
        'interpretation': 'Inference tuning with a fixed manual policy, not recursive self-improvement. Known fixtures used for tuning; confirmation frozen before runs.',
        'packages': {n: importlib.metadata.version(n) for n in ('mlx','mlx-lm','transformers','tokenizers','jsonschema','PyYAML')}}
    local.smoke.write_json(folder / 'protocol.json', protocol)
    for p in sources[:4]:
        (folder / p.name).write_bytes(p.read_bytes())
    (folder / 'calls.jsonl').touch()
    report = {'status': 'running', 'evaluations': []}
    started = time.monotonic()
    client = None
    try:
        client = client_factory(key, folder, snapshot, started, sampling=configurations[0], limits=limits)
        for sampling in configurations:
            client.sampling = sampling
            client.mx.random.seed(sampling['seed'])
            rows = []
            for case in cases:
                if any(local.smoke.digest(CASE / name) != digest for name, digest in hashes.items()):
                    raise ValueError('Protected source changed')
                raw, error = client.ask('negotiator', local.DECISION_RUNTIME + local.smoke.POLICY_SEPARATOR + local.REFERENCE_POLICY,
                                        local.visible(case), local.DECISION_SCHEMA)
                reply = local.render_decision(raw) if not error else raw
                check = {'task_match': False, 'violations': [error]} if error else local.rule_check(case, reply)
                rows.append({'id': case['id'], 'raw_reply': raw, 'expected': case['expected'], **check,
                             'success': check['task_match'] and not check['violations']})
            result = {'sampling': sampling.copy(), **local.smoke.summarize(rows)}
            report['evaluations'].append(result)
            local.smoke.write_json(folder / 'report.json', report)
            print(phase, sampling, 'Q=', result['q'], 'V=', result['v'], flush=True)
        if phase == 'tuning':
            if thinking:
                result = report['evaluations'][0]
                report['profiles'] = [{'sampling': {k:v for k,v in configurations[0].items() if k != 'seed'},
                    'q': result['q'], 'v': result['v'], 'successes': sum(r['success'] for r in result['rows']),
                    'count': len(result['rows']), 'passes': result['q'] >= .8 and result['v'] == 0}]
            else:
                report['profiles'] = summarize_profiles(report['evaluations'])
            report['selected'] = select_profile(report['profiles'])
        else:
            rows = [row for r in report['evaluations'] for row in r['rows']]
            report['confirmation'] = local.smoke.summarize(rows)
            report['passes'] = report['confirmation']['q'] >= .8 and report['confirmation']['v'] == 0
        report['status'] = 'completed'
    except (local.BudgetStop, local.ProviderFailure, ValueError, RuntimeError) as exc:
        report.update(status='stopped', error_type=type(exc).__name__)
    finally:
        report.update(calls=client.calls if client else 0, tokens=client.tokens if client else 0,
                      elapsed_seconds=time.monotonic() - started,
                      peak_mlx_gb=client.mx.get_peak_memory()/1e9 if client else None)
        local.smoke.write_json(folder / 'report.json', report)
        local.smoke.write_json(folder / 'manifest.json', {p.name: local.smoke.digest(p) for p in folder.iterdir() if p.is_file() and p.name != 'manifest.json'})
    return folder


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', choices=local.MODELS, default='qwen3-8b')
    parser.add_argument('--confirmation-of')
    parser.add_argument('--thinking', action='store_true')
    args = parser.parse_args()
    print(run(args.model, args.confirmation_of, thinking=args.thinking))
