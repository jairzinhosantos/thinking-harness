"""Local presentation server. Run one real adaptive attempt or replay a captured session."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import tempfile
import threading
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'utils'))


def live(emit, directory):
    import models
    import task
    from paired_search import fixtures, SAMPLING

    started = time.monotonic()
    emit('start', policy=task.INITIAL_POLICY, strategy=task.INITIAL_STRATEGY)
    emit('phase', stage='load', title='Cargando Qwen3 8B')
    name, revision = models.MODELS['qwen3-8b']
    snapshot = Path.home()/'.cache/huggingface/hub'/('models--'+name.replace('/', '--'))/'snapshots'/revision
    client = models.LocalClient('qwen3-8b', directory, snapshot, started, sampling=SAMPLING,
                                limits={**models.LIMITS, 'output_tokens': 2048, 'context_tokens': 6144,
                                        'total_tokens': 90000, 'seconds': 1500})
    cases = fixtures()

    def ask(stage, role, title, instructions, payload, schema, seed):
        emit('phase', stage=stage, title=title)
        client.seed(seed)
        def fragment(raw, count):
            # Qwen emits its public answer after the reasoning delimiter.
            answer = raw.partition('</think>')[2]
            if answer or count % 24 == 0:
                emit('stream', text=answer, tokens=count)
        client.on_generation = fragment
        return client.ask(role, instructions, payload, schema)

    def evaluate(policy, version, split):
        rows = []
        for index, case in enumerate(cases[split]):
            title = f'{version} · {split} · {index+1}/{len(cases[split])}'
            reply, error = ask('evaluate','negotiator',title,task.DECISION_RUNTIME+task.POLICY_SEPARATOR+policy,
                               task.visible(case),task.DECISION_SCHEMA,(1011 if split=='development' else 2011)+index)
            check = {'task_match':False,'violations':[error]} if error else task.rule_check(case,task.render_decision(reply))
            row = {'id':case['id'],'context':task.visible(case),'expected':case['expected'],'raw_reply':reply,
                   **check,'success':check['task_match'] and not check['violations']}
            rows.append(row)
            emit('case', version=version, split=split, ok=row['success'], violations=check['violations'],
                 message=case['history'][-1]['content'], reply=reply, expected=case['expected'])
        return task.summarize(rows)

    policy = task.INITIAL_POLICY
    dev = evaluate(policy,'H0','development')
    initial = evaluate(policy,'H0','validation')
    strategy = task.INITIAL_STRATEGY
    value, error = ask('propose','proposer','Qwen escribe H1',task.PROPOSAL_CONTRACT+strategy+task.NOVELTY_CONTRACT,
                       {'objective':task.OBJECTIVE,'current_policy':policy,'recent_attempts':[],
                        'development_feedback':dev['rows']},task.PROMPT_SCHEMA,10012)
    if error:
        emit('decision', accepted=False, title='Se conserva H0', reason='Propuesta inválida · '+error)
        return
    candidate = task.get_prompt(value)
    emit('candidate', policy=candidate)
    dev = evaluate(candidate,'H1','development')
    validation = evaluate(candidate,'H1','validation')
    accepted = task.choose(validation,initial,.01)
    emit('decision',accepted=accepted,title='Se acepta H1' if accepted else 'Se conserva H0',
         reason=f"Validación · Q {initial['q']:.0%} → {validation['q']:.0%} · V {validation['v']:.0%}")
    value,error = ask('update','strategy_update','Qwen revisa φ',task.UPDATE_CONTRACT,
                      {'objective':task.OBJECTIVE,'current_strategy':strategy,'candidate_policy':candidate,
                       'development_feedback':dev['rows']},task.PROMPT_SCHEMA,20012)
    emit('strategy', text=task.get_prompt(value) if not error else strategy, error=error)


def serve(args):
    events = []
    changed = threading.Condition()
    connected = threading.Event()
    directory = Path(tempfile.mkdtemp(prefix='thinking-harness-demo-'))
    log = directory/'events.jsonl'
    start = time.monotonic()
    def emit(kind, **fields):
        event = {'event':kind,'t':round(time.monotonic()-start,3),**fields}
        line = json.dumps(event,ensure_ascii=False)
        with log.open('a') as f:
            f.write(line+'\n')
        with changed:
            events.append(line)
            changed.notify_all()
        if kind == 'stream':
            return
        detail = fields.get('title') or fields.get('text', '')[:100]
        if kind == 'case':
            status = 'OK' if fields['ok'] else 'FALLO'
            detail = f"{fields['version']} · {fields['split']} · {status} · {fields['reply']}"
        elif kind == 'decision':
            detail = f"{fields['title']} · {fields['reason']}"
        elif kind in ('start', 'candidate'):
            detail = fields['policy']
        print(f"[{event['t']:7.1f}s] {kind:10} {detail}", flush=True)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args): pass
        def do_GET(self):
            if self.path=='/':
                html=(HERE/'index.html').read_bytes()
                self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(html)
            elif self.path=='/events':
                self.send_response(200);self.send_header('Content-Type','text/event-stream');self.send_header('Cache-Control','no-cache');self.end_headers()
                connected.set()
                try:
                    index=int(self.headers.get('Last-Event-ID','0'))
                    while True:
                        with changed:
                            changed.wait_for(lambda:len(events)>index,timeout=8)
                            batch=events[index:]
                        if not batch:self.wfile.write(b': pulse\n\n')
                        for line in batch:
                            index+=1
                            self.wfile.write(f'id: {index}\ndata: {line}\n\n'.encode())
                        self.wfile.flush()
                except (BrokenPipeError,ConnectionResetError,ValueError):pass
            else:self.send_error(404)

    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    print(f'Abre http://127.0.0.1:{server.server_port}  |  Registro: {log}',flush=True)
    try:
        connected.wait()
        emit('mode', text='Grabación' if args.replay else 'En vivo')
        if args.replay:
            previous=None
            for line in args.replay.read_text().splitlines():
                obj=json.loads(line); stamp=obj.pop('t'); kind=obj.pop('event')
                if previous is not None:time.sleep(max(0,stamp-previous)/args.speed)
                previous=stamp
                if kind not in ('mode','done'):emit(kind,**obj)
        else:live(emit,directory)
    except Exception as exc:
        emit('error',title=str(exc))
    finally:
        emit('done')
    print('Sesión terminada. Ctrl+C para cerrar.',flush=True)
    try:threading.Event().wait()
    except KeyboardInterrupt:pass
    server.shutdown()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=8765)
    parser.add_argument('--replay',type=Path)
    parser.add_argument('--speed',type=float,default=1)
    args=parser.parse_args()
    if args.speed<=0:parser.error('--speed must be positive')
    serve(args)
