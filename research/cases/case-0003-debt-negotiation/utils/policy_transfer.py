"""Evaluate four frozen policies on the reviewed transfer set using local MLX."""
from datetime import datetime, timezone
from pathlib import Path
import time

import yaml

import models
import task


def run():
    case = task.CASE_DIR
    fixture = case / 'policy-transfer-cases.yaml'
    study = yaml.safe_load(fixture.read_text())
    cases = study['cases']
    results = case / 'results'
    sampling = dict(study['protocol']['sampling'])
    limits = dict(models.LIMITS, output_tokens=sampling.pop('max_output_tokens'),
                  calls=4 * len(cases), total_tokens=180000, context_tokens=6144, seconds=1800)
    sampling['seed'] = 11
    sources = ['20261106T221544Z-paired-fixed', '20261106T222100Z-paired-adaptive']
    previous = [task.read_record(results / name) for name in sources]
    policies = {'H0': previous[0][0]['initial_policy'], 'B1': previous[0][1]['selected_policy'],
                'B2': previous[1][1]['selected_policy'], 'Manual': task.REFERENCE_POLICY}
    repo, revision = models.MODELS['qwen3-8b']
    snapshot = Path.home() / '.cache/huggingface/hub' / ('models--' + repo.replace('/', '--')) / 'snapshots' / revision
    provenance = task.source_record([Path(__file__), fixture, Path(models.__file__), Path(task.__file__)])
    folder = results / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-policy-transfer')
    folder.mkdir()
    task.write_json(folder / 'protocol.json', {**provenance, 'cases': cases, 'policies': policies,
                    'source_runs': sources, 'model': repo, 'revision': revision, 'sampling': sampling,
                    'limits': limits, 'design': study['protocol']})
    report = {'status': 'running', 'policies': {}}
    started = time.monotonic()
    client = models.LocalClient('qwen3-8b', folder, snapshot, started, sampling=sampling, limits=limits)
    for name, policy in policies.items():
        rows = []
        start_tokens = client.tokens
        for index, scenario in enumerate(cases):
            seed = 11 + index
            client.seed(seed)
            raw, error = client.ask('negotiator', task.DECISION_RUNTIME + task.POLICY_SEPARATOR + policy,
                                    task.visible(scenario), task.DECISION_SCHEMA)
            check = ({'violations': [error], 'task_match': False} if error else
                     task.rule_check(scenario, task.render_decision(raw)))
            rows.append({'id': scenario['id'], 'call': client.calls, 'seed': seed, 'raw_reply': raw,
                         'expected': scenario['expected'], **check,
                         'success': check['task_match'] and not check['violations']})
            report['policies'][name] = {**task.summarize(rows), 'calls': len(rows), 'tokens': client.tokens - start_tokens}
            task.write_json(folder / 'report.json', report)
        print(name, sum(r['success'] for r in rows), '/', len(rows), flush=True)
    report.update(status='completed', calls=client.calls, tokens=client.tokens, seconds=time.monotonic()-started)
    task.write_json(folder / 'report.json', report)
    task.write_json(folder / 'manifest.json', {p.name: task.digest(p) for p in folder.iterdir()})
    print(folder.name, flush=True)


if __name__ == '__main__':
    run()
