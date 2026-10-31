"""Readable, escaped views of recorded prompt-search evidence. No model calls."""
from difflib import SequenceMatcher
from hashlib import sha256
from html import escape
import re

from IPython.display import HTML, display
import yaml


class EvidenceView:
    def __init__(self, language):
        self.language = language

    def t(self, en, es):
        return es if self.language == 'es' else en

    def show(self, html):
        display(HTML('<div class="evidence-view" style="line-height:1.55;max-width:900px">' + html + '</div>'))

    def table(self, headers, rows):
        def cell(value, tag):
            return f'<{tag} style="text-align:left;padding:6px 10px;border-bottom:1px solid #ddd">{escape(str(value))}</{tag}>'
        return '<table><thead><tr>' + ''.join(cell(h, 'th') for h in headers) + '</tr></thead><tbody>' + ''.join(
            '<tr>' + ''.join(cell(v, 'td') for v in row) + '</tr>' for row in rows) + '</tbody></table>'

    def paragraphs(self, value):
        return ''.join('<p>' + escape(p.strip()).replace('\n', '<br>') + '</p>'
                       for p in re.split(r'\n\s*\n', value.strip()) if p.strip())

    def inputs(self, seed, cases, example, visible):
        self.show('<h3>' + self.t('Seed policy', 'Política semilla') + '</h3>' + self.paragraphs(seed['prompt']))
        self.show(self.table([self.t('Partition', 'Partición'), self.t('Examples', 'Ejemplos')],
            [(self.t(en, es), sum(c['split'] == key for c in cases)) for key, en, es in (
                ('development', 'Development', 'Desarrollo'), ('validation', 'Validation', 'Validación'), ('test', 'Final test', 'Prueba final'))]))
        self.show('<h3>' + self.t('Input example', 'Ejemplo de entrada') + '</h3>' +
            self.table([self.t('Role', 'Rol'), self.t('Message', 'Mensaje')],
                       [(h['role'], h['content']) for h in visible['history']]) +
            '<details><summary>' + self.t('Golden record and evaluator labels', 'Registro golden y etiquetas del evaluador') +
            '</summary><pre style="white-space:pre-wrap;overflow-wrap:anywhere">' +
            escape(yaml.safe_dump(example, sort_keys=False, allow_unicode=True)) + '</pre></details>')

    def bounds(self, config):
        self.show(self.table([self.t('Parameter', 'Parámetro'), self.t('Value', 'Valor')], [
            (self.t('Model', 'Modelo'), config.model),
            (self.t('Rounds / candidates per round', 'Rondas / candidatos por ronda'), f'{config.max_iterations} / {config.candidates_per_iteration}'),
            (self.t('Evaluation repeats', 'Repeticiones de evaluación'), config.evaluation_repeats),
            (self.t('Target / minimum gain', 'Meta / ganancia mínima'), f'{config.target_score} / {config.min_gain}'),
            (self.t('Token budget', 'Presupuesto de tokens'), f'{config.max_total_tokens:,}'),
            (self.t('Estimated cost limit', 'Límite de costo estimado'), f'USD {config.max_cost_usd:.2f}')]))

    def versions(self, report, report_path):
        versions = {v['id']: v for v in report['versions']}
        measured = {report.get('initial_version'): report.get('initial_validation')}
        measured.update({e['version']: e['validation'] for e in report['events'] if 'validation' in e})
        rows = []
        for v in versions.values():
            r = measured.get(v['id'])
            rows.append((v['id'], v['parent'] or '-', f"{r['score']:.1%}" if r else '-',
                         r['violations'] if r else '-', self.t('Yes', 'Sí') if v['id'] == report.get('selected_version') else '-'))
        self.show(self.table([self.t('Version', 'Versión'), self.t('Parent', 'Padre'), self.t('Validation', 'Validación'),
                              self.t('Violations', 'Incumplimientos'), self.t('Retained', 'Conservada')], rows))
        for v in versions.values():
            saved = report_path.parent / v['path']
            if sha256(saved.read_bytes()).hexdigest() != v['sha256']:
                raise ValueError('Saved YAML hash differs from the run manifest')
            if yaml.safe_load(saved.read_text()) != {'prompt': v['prompt']}:
                raise ValueError('Saved policy differs from the report')
            event = next((e for e in report['events'] if e.get('version') == v['id']), None)
            stage = self.t('Seed', 'Semilla') if v['parent'] is None else self.t('One-shot baseline', 'Baseline generado una vez')
            if event:
                stage = self.t('Round', 'Ronda') + f" {event['iteration']}, " + self.t('candidate', 'candidato') + f" {event['candidate'] + 1}"
            html = '<h3>' + escape(v['id'] + ' · ' + stage) + '</h3>'
            r = measured.get(v['id'])
            if r:
                outcome = self.t('Retained at end', 'Conservada al terminar') if v['id'] == report.get('selected_version') else self.t('Not retained', 'No conservada')
                html += '<p><strong>' + outcome + f".</strong> {r['score']:.1%} · " + self.t('Replies with violations: ', 'Respuestas con incumplimientos: ') + str(r['violations']) + '.' + '</p>'
            html += '<p><strong>' + self.t('Policy text (original language)', 'Texto de la política (idioma original)') + '</strong></p>'
            html += '<div style="border-left:3px solid #8296a8;padding-left:16px">' + self.paragraphs(v['prompt']) + '</div>'
            parent = versions.get(v['parent'])
            if parent:
                # Whitespace-normalized word changes avoid repeated YAML quoting and full-line diffs.
                before, after = parent['prompt'].split(), v['prompt'].split()
                changes = []
                for tag, i, j, a, b in SequenceMatcher(None, before, after, autojunk=False).get_opcodes():
                    if tag != 'equal':
                        changes.append((' '.join(before[i:j]) or '-', ' '.join(after[a:b]) or '-'))
                html += '<details><summary>' + self.t('Changes from ', 'Cambios respecto de ') + escape(parent['id']) + '</summary>'
                html += self.table([self.t('Before', 'Antes'), self.t('After', 'Después')], changes) if changes else '<p>' + self.t('No text changes.', 'Sin cambios de texto.') + '</p>'
                html += '</details>'
            self.show(html)

    def evaluation(self, label, result):
        html = '<h3>' + escape(label) + '</h3>'
        if result is None:
            self.show(html + '<p>' + self.t('Incomplete or not reached.', 'Incompleta o no alcanzada.') + '</p>')
            return
        html += f"<p>{result['score']:.1%} · " + self.t('Replies with violations: ', 'Respuestas con incumplimientos: ') + str(result['violations']) + '.</p>'
        rows = []
        for row in result['rows']:
            reply = row['reply']
            decision = f"{reply.get('action')} · {reply.get('debt') or '-'} · {reply.get('payments')} × {reply.get('installment')}"
            rows.append((row['id'], row['repeat'] + 1, decision, self.t('Pass', 'Cumple') if row['success'] else self.t('Fail', 'No cumple')))
        html += self.table([self.t('Example', 'Ejemplo'), self.t('Repeat', 'Repetición'), self.t('Decision', 'Decisión'), self.t('Result', 'Resultado')], rows)
        html += '<details class="trace-details"><summary>' + self.t('Full replies and evaluator rationale', 'Respuestas completas y justificación del evaluador') + '</summary>'
        for row in result['rows']:
            html += '<h4>' + escape(f"{row['id']} · {row['repeat'] + 1}") + '</h4>'
            html += self.table([self.t('Role', 'Rol'), self.t('History', 'Historial')], [(h['role'], h['content']) for h in row['context']['history']])
            html += '<p><strong>' + self.t('Reply: ', 'Respuesta: ') + '</strong>' + escape(row['reply'].get('message', '')) + '</p>'
            html += self.table([self.t('Check', 'Comprobación'), self.t('Result', 'Resultado')], [
                (self.t('Expected decision', 'Decisión esperada'), row['checks']['task_match']),
                (self.t('Violations', 'Incumplimientos'), ', '.join(map(str, row['violations'])) or '-'),
                *[(key, row['judge'].get(key)) for key in ('consistent', 'appropriate', 'clear')]])
            html += '<p><strong>' + self.t('Judge: ', 'Juez: ') + '</strong>' + escape(row['judge'].get('evidence', '')) + '</p>'
        self.show(html + '</details>')

    def evaluations(self, report):
        self.evaluation(self.t('Baseline validation', 'Validación del baseline'), report.get('initial_validation'))
        for event in report['events']:
            if 'development' in event:
                self.evaluation(self.t('Development, round ', 'Desarrollo, ronda ') + str(event['iteration']), event['development'])
            elif 'validation' in event:
                self.evaluation(self.t('Validation ', 'Validación ') + event['version'], event['validation'])
        self.evaluation(self.t('Final test: baseline', 'Prueba final: baseline'), report.get('final_initial'))
        self.evaluation(self.t('Final test: selected policy', 'Prueba final: política seleccionada'), report.get('final_selected'))

    def summary(self, report):
        usage = report.get('usage', {})
        self.show(self.table([self.t('Measure', 'Medida'), self.t('Recorded value', 'Valor registrado')], [
            (self.t('Baseline / retained version', 'Baseline / versión conservada'), f"{report.get('initial_version')} / {report.get('selected_version')}"),
            (self.t('Stop reason', 'Motivo de parada'), self.t('Budget', 'Presupuesto') if report['stop_reason'] == 'budget' else report['stop_reason']),
            (self.t('API calls', 'Llamadas a la API'), usage.get('calls')),
            ('Tokens', f"{usage.get('tokens', 0):,}"),
            (self.t('Estimated cost', 'Costo estimado'), f"USD {usage.get('estimated_cost_usd', 0):.8f}"),
            (self.t('Final comparison', 'Comparación final'), self.t('Complete', 'Completa') if report['final_complete'] else self.t('Incomplete', 'Incompleta'))]))
        if report['final_complete']:
            delta = report['final_selected']['score'] - report['final_initial']['score']
            self.show('<p>' + self.t('Observed final score difference: ', 'Diferencia observada del puntaje final: ') + f'{delta:+.1%}</p>')
        else:
            self.show('<p>' + self.t('The incomplete final comparison does not establish an improvement.', 'La comparación final incompleta no permite establecer una mejora.') + '</p>')


class HarnessTestView(EvidenceView):
    """Compact Spanish views; preserve English experimental prompts verbatim."""
    def __init__(self):
        super().__init__('es')

    def rows(self, headers, rows):
        def label(value):
            if value is True:
                return 'Sí'
            if value is False:
                return 'No'
            return 'No registrado' if value is None else value
        self.show(self.table(headers, [[label(x) for x in row] for row in rows]))

    def prompt(self, title, text, collapsed=False):
        content = '<p><small>Texto original en inglés; entrada o salida del modelo.</small></p>'
        content += '<div style="font-family:system-ui,sans-serif;white-space:normal;overflow-wrap:break-word">'
        content += self.paragraphs(text) + '</div>'
        if collapsed:
            self.show('<details><summary>' + escape(title) + '</summary>' + content + '</details>')
        else:
            self.show('<h4>' + escape(title) + '</h4>' + content)

    def strategy(self, update, reused):
        index = update['after_iteration']
        def sentences(text):
            return '<ul>' + ''.join('<li>' + escape(x) + '</li>'
                                   for x in re.split(r'(?<=[.!?])\s+', text.strip())) + '</ul>'
        self.show('<h4>Actualización ' + str(index) + '</h4>'
                  '<p>Instrucciones que guían la siguiente propuesta. Originales en inglés, '
                  'separados por oraciones para facilitar la lectura.</p>'
                  '<table style="width:100%;table-layout:fixed"><thead><tr>'
                  '<th style="width:50%">Antes: φ' + str(index - 1) + '</th>'
                  '<th style="width:50%">Después: φ' + str(index) + '</th></tr></thead><tbody><tr>'
                  '<td style="vertical-align:top;overflow-wrap:break-word">' + sentences(update['before']) + '</td>'
                  '<td style="vertical-align:top;overflow-wrap:break-word">' + sentences(update['after']) + '</td>'
                  '</tr></tbody></table>')
        self.rows(['Comprobación', 'Resultado'], [
            ['El texto cambió', update['changed']],
            ['Se usó en la propuesta siguiente', reused]])

    def evaluation_rows(self, evaluation):
        names = {'ask': 'Preguntar', 'offer': 'Ofrecer', 'stop': 'Detener', 'accept': 'Aceptar'}
        violations = {'exceeds_declared_capacity': 'Cuota superior a la capacidad',
                      'incorrect_installment': 'Cuota que no corresponde a la deuda',
                      'ignores_explicit_stop': 'Ignora el rechazo a negociar',
                      'fabricated_acceptance': 'Aceptación no autorizada',
                      'unauthorized_plan': 'Plan no permitido',
                      'unexpected_plan_fields': 'Plan en una respuesta sin oferta'}
        self.rows(['Escenario', 'Acción', 'Deuda', 'Pagos', 'Cuota', 'Éxito', 'Incumplimientos'], [
            [r['id'], names.get(r['reply']['action'], r['reply']['action']), r['reply']['debt'],
             r['reply']['payments'], r['reply']['installment'], r['success'],
             '; '.join(violations.get(v, v) for v in r['violations']) or 'Ninguno detectado']
            for r in evaluation['rows']])


def audit_harness_changes(protocol, report, calls):
    """Check parent, request, output, evaluation and selection links for each proposal."""
    import json
    from prompt_search import rule_check, visible, RUNTIME
    requests = {x['call']: x['request'] for x in calls if x['stage'] == 'started'}
    responses = {x['call']: x['response'] for x in calls if x['stage'] == 'received'}

    def output(call):
        response = responses[call]
        text = ''.join(p.get('text', '') for item in response.get('output', [])
                       if item.get('type') == 'message' for p in item.get('content', [])
                       if p.get('type') == 'output_text')
        return json.loads(text)

    def payload(call):
        return json.loads(requests[call]['input'][0]['content'])

    versions = {r['iteration']: r for r in report['rounds']}
    rows = []
    for item in report['rounds'][1:]:
        try:
            parent = versions[item['parent_iteration']]
            call = item['proposal_call']
            before = payload(call)['current_policy'] == parent['policy']
            instructions = requests[call]['instructions'].endswith(item['strategy_used'])
            after = output(call)['prompt'].strip() == item['policy']
            evaluated = True
            offset = 0
            for split in ('development', 'validation'):
                fixtures = protocol['cases'][split]
                evaluated &= len(item[split]['rows']) == len(fixtures)
                for fixture, row in zip(fixtures, item[split]['rows']):
                    offset += 1
                    checks = rule_check(fixture, row['reply'])
                    evaluated &= (row['id'] == fixture['id'] and row['expected'] == fixture['expected']
                                  and row['violations'] == checks['violations']
                                  and row['success'] == (checks['task_match'] and not checks['violations'])
                                  and payload(call + offset) == visible(fixture)
                                  and requests[call + offset]['instructions'] == RUNTIME + '\nPolicy:\n' + item['policy']
                                  and output(call + offset) == row['reply'])
                evaluated &= item[split]['q'] == sum(r['success'] for r in item[split]['rows']) / len(fixtures)
                evaluated &= item[split]['v'] == sum(bool(r['violations']) for r in item[split]['rows']) / len(fixtures)
            selected = item['accepted'] == (item['validation']['v'] == 0 and
                item['validation']['q'] >= parent['validation']['q'] + protocol['config']['min_gain'])
            ok = all([before, instructions, after, evaluated, selected])
        except (KeyError, ValueError, TypeError):
            ok = False
        rows.append([f"Política propuesta {item['iteration']}", bool(ok)])
    for update in report['strategy_updates']:
        try:
            call = update['update_call']
            candidate = versions[update['after_iteration']]
            ok = (payload(call)['current_strategy'] == update['before']
                  and payload(call)['candidate_policy'] == candidate['policy']
                  and payload(call)['development_feedback'] == candidate['development']['rows']
                  and output(call)['prompt'].strip() == update['after'])
        except (KeyError, ValueError, TypeError):
            ok = False
        rows.append([f"Instrucciones actualizadas {update['after_iteration']}", bool(ok)])
    return rows
