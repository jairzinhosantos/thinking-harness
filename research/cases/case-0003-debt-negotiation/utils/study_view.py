"""Read and display recorded experiments without model or network access."""
import hashlib
import html
import json
from pathlib import Path

from IPython.display import HTML, display

RUNS = {
    'inference': '20261106T204139Z-inference-qwen3-8b-thinking-tuning',
    'confirmation': '20261106T204259Z-inference-qwen3-8b-thinking-confirmation',
    'fixed': '20261106T221544Z-paired-fixed',
    'adaptive': '20261106T222100Z-paired-adaptive',
    'fixed_budget': '20261106T224117Z-paired-fixed-tokens-4096',
    'adaptive_budget': '20261106T224923Z-paired-adaptive-tokens-4096',
    'fixed_schema': '20261106T231518Z-paired-fixed-tokens-4096-structured',
    'adaptive_schema': '20261106T232337Z-paired-adaptive-tokens-4096-structured',
}


def load_records(case_dir):
    """Validate manifests before loading immutable run data."""
    records = {}
    for key, name in RUNS.items():
        folder = Path(case_dir) / 'results' / name
        manifest = json.loads((folder / 'manifest.json').read_text())
        for filename, digest in manifest.items():
            if Path(filename).name != filename:
                raise ValueError('Manifest contains a nested path')
            if hashlib.sha256((folder / filename).read_bytes()).hexdigest() != digest:
                raise ValueError(f'Evidence hash mismatch: {name}/{filename}')
        records[key] = {
            'name': name,
            'protocol': json.loads((folder / 'protocol.json').read_text()),
            'report': json.loads((folder / 'report.json').read_text()),
            'calls': [json.loads(line) for line in (folder / 'calls.jsonl').read_text().splitlines()],
        }
    return records


def cell(value):
    if isinstance(value, (dict, list)):
        return '<pre style="white-space:pre-wrap;text-align:left;margin:0">' + html.escape(json.dumps(value, ensure_ascii=False, indent=2)) + '</pre>'
    return html.escape(str(value)).replace('\n', '<br>')


def table(headers, rows):
    style = 'text-align:left;vertical-align:top;padding:10px;border-bottom:1px solid #d5dce3;overflow-wrap:anywhere'
    header = ''.join(f'<th style="{style}">{html.escape(str(value))}</th>' for value in headers)
    body = ''.join('<tr>' + ''.join(f'<td style="{style}">{cell(value)}</td>' for value in row) + '</tr>' for row in rows)
    display(HTML(f'<table style="width:100%;border-collapse:collapse"><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table>'))


def prompt(title, text, *, folded=False):
    """Preserve source text and escape any embedded HTML."""
    body = f'<div style="white-space:pre-wrap;border-left:3px solid #597b98;background:#f5f8fb;padding:14px;text-align:left">{html.escape(str(text))}</div>'
    title = html.escape(title)
    content = f'<details><summary><strong>{title}</strong></summary>{body}</details>' if folded else f'<h4>{title}</h4>{body}'
    display(HTML(content))


def percent(value):
    return 'Sin evaluar' if value is None else f'{value:.0%}'


def label(record):
    return 'B1' if record['protocol']['strategy'] == 'fixed' else 'B2'


def call_for(record, role, iteration):
    event = next(e for e in record['report']['events'] if e['role'] == role and e['iteration'] == iteration)
    return next(c for c in record['calls'] if c['call'] == event['call'])


def show_start(records):
    record = records['adaptive']
    p = record['protocol']
    prompt('H0 · Política inicial', p['initial_policy'])
    prompt('φ0 · Instrucciones iniciales', p['initial_strategy'])
    for role, title, iteration in [('negotiator', 'Negociador', 0), ('proposer', 'Mejorador', 1), ('strategy_update', 'Actualizador', 1)]:
        call = call_for(record, role, iteration)
        text = next(m['content'] for m in call['messages'] if m['role'] == 'system')
        prompt(f'{title} · System prompt', text, folded=True)


def show_first_proposal(records):
    record = records['adaptive']
    proposal = call_for(record, 'proposer', 1)
    payload = json.loads(next(m['content'] for m in proposal['messages'] if m['role'] == 'user'))
    prompt('Objetivo fijo', payload['objective'], folded=True)
    rows = payload['development_feedback']
    descriptions = {
        'development-largest': 'Elegir la mayor deuda viable\nCapacidad de pago: 330 al mes',
        'development-declined': 'Respetar el rechazo\nEl cliente pide detener la negociación',
        'transfer-unknown': 'Preguntar por la capacidad\nEl cliente aún no sabe cuánto puede pagar',
        'confirmation-consent': 'Confirmar el plan aceptado\nEl cliente acepta A en dos cuotas de 100',
    }
    table(['Caso de desarrollo', 'Respuesta de H0', 'Referencia', 'Correcta', 'Incumplimientos'], [
        [descriptions.get(r['id'], 'Caso sin descripción') + '\nID: ' + r['id'],
         r['raw_reply'] if r['raw_reply'] is not None else 'Sin respuesta válida', r['expected'],
         'Sí' if r['success'] else 'No',
         ', '.join('Corte por límite de salida (output_limit)' if v == 'output_limit' else v
                   for v in r['violations']) or 'Ninguno'] for r in rows])
    first = record['report']['rounds'][1]
    prompt('H1 · Política candidata', first['policy'])
    initial = record['report']['rounds'][0]
    table(['Versión', 'Q validación', 'V validación', 'Selección'], [
        ['H0', percent(initial['validation']['q']), percent(initial['validation']['v']), 'Reemplazada' if first['accepted'] else 'Conservada'],
        ['H1', percent(first['validation']['q']), percent(first['validation']['v']), 'Aceptada' if first['accepted'] else 'Rechazada']])


def show_updates(records):
    record = records['adaptive']
    report = record['report']
    rows = []
    for index, update in enumerate(report['strategy_updates'], 1):
        following = next((r for r in report['rounds'] if r['iteration'] == update['after_iteration'] + 1), None)
        reused = following is not None and following['strategy_used'] == update['after']
        rows.append([f'φ{index}', update['after_iteration'], 'Sí' if update['changed'] else 'No',
                     following['iteration'] if reused else 'No registrada', update.get('error') or 'Ninguno'])
        prompt(f'φ{index} · Instrucciones nuevas', update['after'], folded=index > 1)
    table(['Versión', 'Tras intento', 'Texto cambiado', 'Usada en intento', 'Error'], rows)


def show_rounds(records):
    rows = []
    for key in ('fixed', 'adaptive'):
        record = records[key]
        kept = 0
        for r in record['report']['rounds']:
            if r['accepted']:
                kept = r['iteration']
            note = ('Inicio' if r['iteration'] == 0 else 'Aceptada' if r['accepted'] else 'Rechazada')
            if r.get('error'):
                note = 'Fuera del esquema; sin política evaluable'
            elif r.get('duplicate_of') is not None:
                note = f'Duplicada del intento {r["duplicate_of"]}'
            rows.append([label(record), r['iteration'], f'H{r["parent_iteration"]}' if 'parent_iteration' in r else '—',
                         percent(r.get('validation', {}).get('q')), percent(r.get('validation', {}).get('v')), note, f'H{kept}'])
            if r['iteration'] > 1 and 'policy' in r:
                prompt(f'{label(record)} · H candidata {r["iteration"]} · {note}', r['policy'], folded=True)
    table(['Condición', 'Intento', 'Parte de', 'Q candidata', 'V candidata', 'Resultado', 'H conservada'], rows)


def length_rows(record):
    """Count characters/whitespace words; reuse native token counts from the run."""
    rows = []
    for r in record['report']['rounds']:
        for symbol, text_key, token_key in [('H', 'policy', 'policy_tokens'), ('φ', 'strategy_used', 'strategy_tokens')]:
            text = r.get(text_key)
            if text is None:
                continue
            rows.append([label(record), r['iteration'], symbol, len(text), len(text.split()),
                         r.get(token_key, 'No registrado'), percent(r.get('validation', {}).get('q')),
                         'Inicial' if r['iteration'] == 0 else 'Sí' if r['accepted'] else 'No'])
    return rows


def show_lengths(records):
    rows = length_rows(records['fixed']) + length_rows(records['adaptive'])
    for symbol, title in [('H', 'H · políticas candidatas'), ('φ', 'φ · instrucciones utilizadas')]:
        display(HTML(f'<h4>{title}</h4>'))
        subset = [r for r in rows if r[2] == symbol]
        headers = ['Búsqueda · intento', 'Caracteres', 'Palabras', 'Tokens', 'Q validación'] if symbol == 'H' else ['Búsqueda · intento', 'Caracteres', 'Palabras', 'Tokens']
        table(headers, [[f'{r[0]} · {r[1]}', *r[3:6], *([r[6]] if symbol == 'H' else [])] for r in subset])


def show_case(records, case_id):
    record = records['adaptive']
    case = next(c for c in record['protocol']['cases']['test'] if c['id'] == case_id)
    table(['Rol', 'Historial original'], [[m['role'], m['content']] for m in case['history']])
    rows = [['Referencia', *[case['expected'][k] for k in ('action', 'debt', 'payments', 'installment')], '—']]
    for key in ('fixed', 'adaptive'):
        r = records[key]['report']
        for phase, title in [('initial', 'H0'), ('selected', f'H{r["selected_iteration"]}')]:
            row = next(x for x in r['test'][phase]['rows'] if x['id'] == case_id)
            reply = row['raw_reply'] or {}
            rows.append([f'{label(records[key])} · {title}', *[reply.get(k, 'Sin respuesta') for k in ('action', 'debt', 'payments', 'installment')],
                         'Sí' if row['success'] else 'No'])
    table(['Versión', 'Acción', 'Deuda', 'Pagos', 'Cuota', 'Correcta'], rows)


def show_outcomes(records):
    rows = []
    for key, title in [('fixed', 'Test 4 · 2.048'), ('adaptive', 'Test 4 · 2.048'),
                       ('fixed_budget', 'Test 4 · 4.096'), ('adaptive_budget', 'Test 4 · 4.096'),
                       ('fixed_schema', 'Test 5 · 4.096'), ('adaptive_schema', 'Test 5 · 4.096')]:
        record = records[key]
        report = record['report']
        count = lambda phase: f"{sum(r['success'] for r in report['test'][phase]['rows'])}/{len(report['test'][phase]['rows'])}"
        valid = sum(c.get('error') is None for c in record['calls'])
        rows.append([title, label(record), count('initial'), f"H{report['selected_iteration']}: {count('selected')}", percent(report['test']['selected']['v']),
                     f"{valid}/{len(record['calls'])}", sum(c.get('error') == 'output_limit' for c in record['calls']), report['tokens']])
    table(['Prueba · tope', 'Condición', 'H0: aciertos', 'H elegida: aciertos', 'V final', 'Llamadas sin error', 'Cortes', 'Tokens totales'], rows)


def show_sources(records):
    display(HTML('<details><summary>Registros originales</summary><ul>' + ''.join(f'<li>{html.escape(key)}: <a href="../results/{r["name"]}/report.json">{r["name"]}</a></li>' for key, r in records.items()) + '</ul></details>'))
