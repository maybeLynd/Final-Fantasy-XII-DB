"""Focused actual HTTP controls for the returned cache repair; no peer-source import."""
import hashlib, importlib.util, json, os, shutil, socket, subprocess, sys, time
import urllib.error, urllib.request
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
R = W / 'run-01'
assert not R.exists(), 'Retain completed/failed run; never overwrite or replay'
prepared = W / 'source-preparation'
identity = json.loads((prepared / 'receipt.json').read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(prepared / 'server-final.py') == identity['final_sha256']
assert identity['cache_AST_and_constants_identical'] and identity['pending_peer_code_not_executed']
R.mkdir()
root = R / 'source'
server_path = root / 'Database/Tools/dashboard/server.py'
server_path.parent.mkdir(parents=True)
shutil.copyfile(prepared / 'server-final.py', server_path)
for d in identity['dependencies']:
    assert sha(prepared / d['retained']) == d['sha256']
    f = root / d['path']; f.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(prepared / d['retained'], f)
gpath = root / 'Database/Tools/analysis-kit/gfz-scripts/generation.py'
spec = importlib.util.spec_from_file_location('independent_cache_generation', gpath)
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
base = str(Path(sys._base_executable))
raw = {'method': 'A actual private dashboard HTTP; labelled synthetic tooling stores; production read-only',
       'driver_sha256': sha(__file__), 'prepared_receipt_sha256': sha(prepared / 'receipt.json'),
       'source_identity': identity, 'python': sys.version, 'child_executable': base,
       'cases': [], 'http': [], 'commands': [], 'cleanup': [], 'finished': False}
names = ('overview', 'systems', 'vbf', 'executable', 'types', 'evidence', 'fleet')
children = []
def dump(): (R / 'raw.json').write_text(json.dumps(raw, indent=2) + '\n')
def record(name, observed, passed, limits=''):
    raw['cases'].append({'name': name, 'observed': observed, 'passed': bool(passed), 'limits': limits})
def http(url, path, method='GET', retain=True):
    start = time.monotonic()
    try:
        with urllib.request.urlopen(urllib.request.Request(url + path, method=method), timeout=5) as q:
            code, content = q.status, q.read()
    except urllib.error.HTTPError as e: code, content = e.code, e.read()
    body = json.loads(content) if content[:1] in (b'{', b'[') else content.decode(errors='replace')
    receipt = {'url': url + path, 'method': method, 'status': code, 'body': body,
               'begin': start, 'end': time.monotonic()}
    if retain: raw['http'].append(receipt)
    return receipt
def cli(store):
    args = [base, '-B', str(gpath), 'verify', store.root]
    p = subprocess.run(args, capture_output=True, text=True, timeout=10)
    receipt = {'args': args, 'returncode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
    raw['commands'].append(receipt)
    return receipt
def fixture(name):
    d = R / name; d.mkdir()
    inp = d / 'source-input'; inp.write_bytes(b'ordinary controlled input\n')
    store = G.Store(str(d / 'store'))
    return d, inp, store, {'controlled': {'path': str(inp)}}
def build(store, inputs, marker):
    b = store.begin(inputs, {'name': 'ASTRA retained same-stat recipe', 'sha256': raw['driver_sha256']})
    for n in names:
        Path(b.output_path('view-' + n + '.json')).write_text(json.dumps({'view': n, 'status': 'OK', 'title': n, 'measures': [], 'sentinel': marker}))
    return store.commit(b, ['view-' + n + '.json' for n in names])
def launch(store):
    s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
    log = open(Path(store.root).parent / 'server-log.txt', 'wb')
    args = [base, '-B', str(server_path), '--root', store.root, '--port', str(port)]
    p = subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT)
    child = {'process': p, 'log': log, 'base': 'http://127.0.0.1:' + str(port), 'port': port, 'args': args}
    children.append(child)
    until = time.monotonic() + 12
    while time.monotonic() < until:
        assert p.poll() is None, 'Private server exited before baseline'
        try:
            a = http(child['base'], '/api/status')
            assert a['status'] == 200
            return child
        except (urllib.error.URLError, ConnectionError, TimeoutError): time.sleep(.1)
    raise TimeoutError('Private server startup exceeded12s')
def stop(child):
    if child.get('stopped'): return
    p = child['process']
    if p.poll() is None: p.terminate()
    try: p.wait(timeout=5)
    except subprocess.TimeoutExpired: p.kill(); p.wait(timeout=5)
    child['log'].close(); child['stopped'] = True
    raw['cleanup'].append({'pid': p.pid, 'port': child['port'], 'args': child['args'],
                           'returncode': p.returncode, 'handle_terminal_and_reaped': p.poll() is not None})
def same_stat_edit(f, old, new):
    before = f.stat(); a = f.read_bytes(); b = a.replace(old, new)
    assert a != b and len(a) == len(b)
    f.write_bytes(b); os.utime(f, ns=(before.st_atime_ns, before.st_mtime_ns)); after = f.stat()
    return {'size_before': before.st_size, 'size_after': after.st_size,
            'mtime_before': before.st_mtime_ns, 'mtime_after': after.st_mtime_ns,
            'sha_before': hashlib.sha256(a).hexdigest(), 'sha_after': sha(f)}
try:
    # Production is never changed/restarted. This sample is not a loaded-code identity proof.
    deployed = http('http://127.0.0.1:8765', '/api/status')
    overview = http('http://127.0.0.1:8765', '/api/view/overview')
    record('deployed-read-only-observation', {'status': deployed, 'overview': overview},
           deployed['status'] == overview['status'] == 200,
           'Observed responsiveness/scope fields only; loaded process/module identity and pending peer code are not accepted.')

    d, inp, st, inputs = fixture('same-stat-output')
    gid = build(st, inputs, 'ORIGINAL'); c = launch(st)
    try:
        good = cli(st); warm = http(c['base'], '/api/view/overview')
        assert good['returncode'] == 0 and warm['body']['view']['sentinel'] == 'ORIGINAL'
        record('warm-output-positive', {'cli': good, 'warm': warm}, True)
        deny = http(c['base'], '/api/status', method='POST')
        record('http-read-only-refusal', deny, deny['status'] == 405)
        f = Path(st.root) / gid / 'outputs/view-overview.json'
        edit = same_stat_edit(f, b'ORIGINAL', b'TAMPERED'); control = cli(st)
        answer = http(c['base'], '/api/view/overview'); status = http(c['base'], '/api/status')
        record('same-stat-output-next-request', {'edit': edit, 'cli': control, 'answer': answer, 'status': status},
               control['returncode'] != 0 and answer['body'].get('status') == 'INVALID' and 'view' not in answer['body']
               and bool(status['body']['current']['problems']) and status['body']['no_verified_generation'])
        record('same-stat-tampered-bytes-not-served', answer, 'TAMPERED' not in json.dumps(answer['body']))
    finally: stop(c)

    d, inp, st, inputs = fixture('warm-historical-fallback')
    old = build(st, inputs, 'PRIOR_VALID'); gid = build(st, inputs, 'NEW_VALID'); c = launch(st)
    try:
        warm = http(c['base'], '/api/view/overview'); assert warm['body']['view']['sentinel'] == 'NEW_VALID'
        f = Path(st.root) / gid / 'outputs/view-overview.json'; f.write_bytes(f.read_bytes().replace(b'NEW_VALID', b'CORRUPTED'))
        control = cli(st); answer = http(c['base'], '/api/view/overview'); status = http(c['base'], '/api/status')
        record('warm-output-historical-fallback', {'cli': control, 'answer': answer, 'status': status, 'prior': old},
               control['returncode'] != 0 and answer['body']['meta']['historical'] and status['body']['historical']
               and answer['body']['view']['sentinel'] == 'PRIOR_VALID' and status['body']['generation'] == old
               and 'CORRUPTED' not in json.dumps(answer['body']))
    finally: stop(c)

    d, inp, st, inputs = fixture('ordinary-snapshot-tamper'); gid = build(st, inputs, 'NO_INVALID_DATA'); c = launch(st)
    try:
        warm = http(c['base'], '/api/view/overview'); assert warm['body']['view']['sentinel'] == 'NO_INVALID_DATA'
        (Path(st.root) / gid / 'inputs/controlled').write_bytes(b'ordinary snapshot mismatch\n')
        control = cli(st); answer = http(c['base'], '/api/view/overview')
        record('ordinary-snapshot-tamper-no-fallback', {'cli': control, 'answer': answer},
               control['returncode'] != 0 and answer['body'].get('status') == 'INVALID' and 'view' not in answer['body'])
    finally: stop(c)

    d, inp, st, inputs = fixture('stale-reader-control'); gid = build(st, inputs, 'CODE_CONTROL'); c = launch(st)
    saved = server_path.read_bytes()
    try:
        before = http(c['base'], '/api/status'); assert before['body']['reader_stale'] is False
        server_path.write_bytes(saved + b'\n# PRIVATE POST-LOAD DETECTION CONTROL\n')
        after = http(c['base'], '/api/status')
        record('changed-loaded-code-detection', {'before': before, 'after': after}, after['body']['reader_stale'] is True)
    finally: stop(c); server_path.write_bytes(saved)

    # Separate store/child: no output edit or source change may reset this input timer.
    d, inp, st, inputs = fixture('same-stat-input-timer'); gid = build(st, inputs, 'TIMER_BASELINE'); c = launch(st)
    try:
        good = cli(st); warm = http(c['base'], '/api/status')
        assert good['returncode'] == 0 and not warm['body']['current']['problems'] and not warm['body']['reader_stale']
        assert warm['body']['verified_at'] and '60 s' in warm['body']['verification']
        record('input-timer-positive', {'cli': good, 'warm': warm}, True)
        edit = same_stat_edit(Path(st.root) / gid / 'inputs/controlled', b'ordinary', b'changed!')
        control = cli(st); assert control['returncode'] != 0
        polls = []; first = None; until = warm['end'] + 90
        while time.monotonic() < until:
            a = http(c['base'], '/api/status', retain=False)
            assert a['status'] == 200 and c['process'].poll() is None
            polls.append(a)
            if a['body']['current']['problems']:
                first = a; break
            # A served request starting after the full 60s bound may not remain CURRENT.
            if a['begin'] >= warm['end'] + 60: break
            time.sleep(1)
        no_late_current = not any(a['begin'] >= warm['end'] + 60 and not a['body']['current']['problems'] for a in polls)
        answer = http(c['base'], '/api/view/overview')
        record('same-stat-input-periodic-detection', {'edit': edit, 'cli': control, 'warm': warm, 'polls': polls,
            'first_detection': first, 'no_late_current_response': no_late_current, 'answer': answer,
            'first_detection_from_warm_end_seconds': None if first is None else first['begin'] - warm['end']},
            first is not None and no_late_current and first['end'] <= warm['end'] + 90
            and first['body']['no_verified_generation'] and answer['body'].get('status') == 'INVALID' and 'view' not in answer['body'],
            'Active roughly1s client polling; due verification on actual requests. Does not prove idle background checks or atomic multi-file reads.')
    finally: stop(c)
    raw['finished'] = True
except BaseException as e:
    raw['fatal'] = {'type': type(e).__name__, 'reason': str(e)}
    raise
finally:
    for c in children: stop(c)
    raw['copied_source_restored'] = sha(server_path) == identity['final_sha256']
    q = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, timeout=10)
    raw['listener_check'] = {'returncode': q.returncode, 'owned_ports': [c['port'] for c in raw['cleanup']],
        'rows': [l for l in q.stdout.splitlines() if 'LISTENING' in l and any(l.split()[1].endswith(':' + str(c['port'])) for c in raw['cleanup'])]}
    dump()
print('CACHE_R2_CAPTURE', [c['name'] for c in raw['cases'] if not c['passed']], flush=True)
