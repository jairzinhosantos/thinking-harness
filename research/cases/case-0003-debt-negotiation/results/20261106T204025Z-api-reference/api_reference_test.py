"""Bounded API reference control after local inference tuning."""
import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import yaml

import local_model_test as local
from prompt_search import Config, ResponsesClient, BudgetStop, ProviderFailure

CASE = local.CASE_DIR


def run(*, allow_live=False, temperature=None, output_root=None, client_factory=ResponsesClient):
    config = Config(model='gpt-4o-mini-2024-07-18', input_usd_per_million=.15,
                    output_usd_per_million=.60, max_cost_usd=.25,
                    max_total_tokens=50000, max_output_tokens=512, allow_live=allow_live,
                    temperature=temperature)
    if not allow_live:
        raise ValueError('Live execution requires --allow-live')
    known = [c for group in local.smoke.select_cases().values() for c in group] + local.transfer_cases()
    confirmation = yaml.safe_load((CASE / 'inference-confirmation-cases.yaml').read_text())['cases']
    folder = Path(output_root or CASE / 'results') / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-api-reference')
    folder.mkdir(parents=True, exist_ok=False)
    sources = [Path(__file__), Path(local.__file__), Path(local.smoke.__file__),
               Path(local.__file__).with_name('prompt_search.py'), CASE / 'harness-test-cases.yaml',
               CASE / 'local-transfer-cases.yaml', CASE / 'inference-confirmation-cases.yaml']
    hashes = {str(p.relative_to(CASE)): local.smoke.digest(p) for p in sources}
    protocol = {'protocol': 'case-0003-api-reference-v1', 'model': config.model,
        'config': asdict(config), 'known_cases': known, 'confirmation_cases': confirmation,
        'policy': local.REFERENCE_POLICY, 'runtime': local.DECISION_RUNTIME,
        'sampling': {'temperature': temperature, 'other_parameters': 'Provider defaults; no seed control.'},
        'criterion': 'Q >= 0.80 and zero observed violations, on known cases and confirmation separately.',
        'stop': '12 known cases; only if criterion passes, 8 confirmation cases repeated 3 times. Maximum 36 calls, 900 seconds, USD 0.25 application budget. No retry.',
        'interpretation': 'Manual fixed policy; feasibility control, not self-improvement or causal comparison with local sampling.',
        'source_hashes': hashes}
    local.smoke.write_json(folder / 'protocol.json', protocol)
    for path in sources[:4]:
        (folder / path.name).write_bytes(path.read_bytes())
    (folder / 'calls.jsonl').touch()
    report = {'status': 'running', 'evaluations': []}
    started = time.monotonic()
    client = None
    try:
        client = client_factory(config, folder)
        for phase, repeats, cases in [('known', 1, known), ('confirmation', 3, confirmation)]:
            if phase == 'confirmation' and not report['known_passes']:
                break
            for repeat in range(repeats):
                rows = []
                for case in cases:
                    if client.calls >= 36 or time.monotonic() - started >= 900:
                        raise BudgetStop('Reference limit reached')
                    if any(local.smoke.digest(CASE / name) != digest for name, digest in hashes.items()):
                        raise ValueError('Protected source changed')
                    reply = client.ask('negotiator', local.DECISION_RUNTIME + local.smoke.POLICY_SEPARATOR + local.REFERENCE_POLICY,
                                       local.visible(case), local.DECISION_SCHEMA)
                    _, error = local.parse_reply(json.dumps(reply), local.DECISION_SCHEMA)
                    check = {'task_match': False, 'violations': [error]} if error else local.rule_check(case, local.render_decision(reply))
                    rows.append({'id': case['id'], 'raw_reply': reply, 'expected': case['expected'], **check,
                                 'success': check['task_match'] and not check['violations']})
                result = {'phase': phase, 'repeat': repeat, **local.smoke.summarize(rows)}
                report['evaluations'].append(result)
                if phase == 'known':
                    report['known_passes'] = result['q'] >= .8 and result['v'] == 0
                local.smoke.write_json(folder / 'report.json', report)
                print(phase, repeat, 'Q=', result['q'], 'V=', result['v'], flush=True)
        confirmed = [row for r in report['evaluations'] if r['phase'] == 'confirmation' for row in r['rows']]
        report['confirmation'] = local.smoke.summarize(confirmed) if confirmed else None
        report['passes'] = bool(confirmed) and report['confirmation']['q'] >= .8 and report['confirmation']['v'] == 0
        report['status'] = 'completed'
    except (BudgetStop, ProviderFailure, ValueError, RuntimeError) as exc:
        report.update(status='stopped', error_type=type(exc).__name__)
    finally:
        report.update(calls=client.calls if client else 0, tokens=client.tokens if client else 0,
                      estimated_cost_usd=client.cost if client else 0, elapsed_seconds=time.monotonic()-started)
        local.smoke.write_json(folder / 'report.json', report)
        local.smoke.write_json(folder / 'manifest.json', {p.name: local.smoke.digest(p) for p in folder.iterdir() if p.is_file() and p.name != 'manifest.json'})
    return folder


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--allow-live', action='store_true')
    parser.add_argument('--temperature', type=float)
    args = parser.parse_args()
    print(run(allow_live=args.allow_live, temperature=args.temperature))
