import argparse, ast, hashlib, json
from pathlib import Path
W = Path(__file__).resolve().parent
R = W / 'run-01'
ap = argparse.ArgumentParser(); ap.add_argument('--raw', type=Path, default=R / 'raw.json'); ap.add_argument('--out', type=Path, default=W / 'result.json')
a = ap.parse_args(); r = json.loads(a.raw.read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert r['finished'] is True and not r.get('fatal')
assert r['driver_sha256'] == sha(W / 'capture.py')
assert r['prepared_receipt_sha256'] == sha(W / 'source-preparation/receipt.json')
s = json.loads((W / 'source-preparation/receipt.json').read_text())
assert s == r['source_identity'] and s['pending_peer_code_not_executed']
assert s['base_commit'] == 'e8999f966ef1b5d1aac87fcf1e941bd23e9ab2cd'
assert s['final_server_commit'] == '622c0866ddf7b7f1484b92b34adfaa46190ee821'
assert sha(W / 'source-preparation/server-base-repair.py') == s['base_sha256']
assert sha(W / 'source-preparation/server-final.py') == s['final_sha256']
assert sha(R / 'source/Database/Tools/dashboard/server.py') == s['final_sha256']
def selected(p):
    tree = ast.parse(Path(p).read_text()); out = {}
    for n in tree.body:
        if isinstance(n, ast.ClassDef) and n.name == 'State': out[n.name] = ast.dump(n, include_attributes=False)
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id in ('REQUIRED', 'VERIFICATION', 'VERIFY_INPUTS_EVERY'): out[t.id] = ast.dump(n, include_attributes=False)
    assert set(out) == {'State', 'REQUIRED', 'VERIFICATION', 'VERIFY_INPUTS_EVERY'}
    return out
assert selected(W / 'source-preparation/server-base-repair.py') == selected(W / 'source-preparation/server-final.py')
for d in s['dependencies']:
    assert sha(W / 'source-preparation' / d['retained']) == sha(R / 'source' / d['path']) == d['sha256']
    data = (R / 'source' / d['path']).read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == d['git_blob']
    assert d['source_tree_commit'] == s['final_server_commit']
ids = {'deployed-read-only-observation', 'warm-output-positive', 'http-read-only-refusal',
       'same-stat-output-next-request', 'same-stat-tampered-bytes-not-served',
       'warm-output-historical-fallback', 'ordinary-snapshot-tamper-no-fallback',
       'changed-loaded-code-detection', 'input-timer-positive', 'same-stat-input-periodic-detection'}
cases = {c['name']: c for c in r['cases']}
assert set(cases) == ids and len(r['cases']) == len(ids)
assert r['copied_source_restored'] is True
assert len(r['cleanup']) == 5 and len({c['pid'] for c in r['cleanup']}) == 5
assert all(c['handle_terminal_and_reaped'] and c['returncode'] is not None for c in r['cleanup'])
assert r['listener_check']['returncode'] == 0 and not r['listener_check']['rows']
assert set(r['listener_check']['owned_ports']) == {c['port'] for c in r['cleanup']}
facts = {}
o = cases['deployed-read-only-observation']['observed']
facts['deployed-read-only-observation'] = o['status']['status'] == o['overview']['status'] == 200
o = cases['warm-output-positive']['observed']
assert o['cli']['returncode'] == 0 and o['warm']['body']['view']['sentinel'] == 'ORIGINAL', 'Invalid warmed observer control'
facts['warm-output-positive'] = True
facts['http-read-only-refusal'] = cases['http-read-only-refusal']['observed']['status'] == 405
def edit_control(o):
    e = o['edit']; assert e['size_before'] == e['size_after'] and e['mtime_before'] == e['mtime_after']
    assert e['sha_before'] != e['sha_after'] and o['cli']['returncode'] != 0
o = cases['same-stat-output-next-request']['observed']; edit_control(o)
assert o['edit']['size_before'] == 97
facts['same-stat-output-next-request'] = (o['answer']['body'].get('status') == 'INVALID' and 'view' not in o['answer']['body']
    and bool(o['status']['body']['current']['problems']) and o['status']['body']['no_verified_generation'])
facts['same-stat-tampered-bytes-not-served'] = 'TAMPERED' not in json.dumps(cases['same-stat-tampered-bytes-not-served']['observed']['body'])
o = cases['warm-output-historical-fallback']['observed']; assert o['cli']['returncode'] != 0
facts['warm-output-historical-fallback'] = (o['answer']['body']['meta']['historical'] and o['status']['body']['historical']
    and o['answer']['body']['view']['sentinel'] == 'PRIOR_VALID' and o['status']['body']['generation'] == o['prior']
    and 'CORRUPTED' not in json.dumps(o['answer']['body']))
o = cases['ordinary-snapshot-tamper-no-fallback']['observed']; assert o['cli']['returncode'] != 0
facts['ordinary-snapshot-tamper-no-fallback'] = o['answer']['body'].get('status') == 'INVALID' and 'view' not in o['answer']['body']
o = cases['changed-loaded-code-detection']['observed']; assert o['before']['body']['reader_stale'] is False
facts['changed-loaded-code-detection'] = o['after']['body']['reader_stale'] is True
o = cases['input-timer-positive']['observed']; assert o['cli']['returncode'] == 0 and not o['warm']['body']['current']['problems']
assert not o['warm']['body']['reader_stale'] and o['warm']['body']['verified_at'] and '60 s' in o['warm']['body']['verification']
facts['input-timer-positive'] = True
timer = cases['same-stat-input-periodic-detection']['observed']; edit_control(timer)
polls = timer['polls']; assert polls and all(q['status'] == 200 and q['begin'] <= q['end'] for q in polls)
assert all(polls[i]['end'] <= polls[i+1]['begin'] for i in range(len(polls)-1))
assert timer['warm'] == o['warm']
detected = next((q for q in polls if q['body']['current']['problems']), None)
assert detected == timer['first_detection']
no_late = not any(q['begin'] >= timer['warm']['end'] + 60 and not q['body']['current']['problems'] for q in polls)
assert no_late == timer['no_late_current_response']
elapsed = None if detected is None else detected['begin'] - timer['warm']['end']
assert elapsed == timer['first_detection_from_warm_end_seconds']
facts['same-stat-input-periodic-detection'] = (detected is not None and no_late and detected['end'] <= timer['warm']['end'] + 90
    and detected['body']['no_verified_generation'] and timer['answer']['body'].get('status') == 'INVALID' and 'view' not in timer['answer']['body'])
for name, ok in facts.items(): assert cases[name]['passed'] == bool(ok), 'Unchecked producer verdict: ' + name
failed = sorted(n for n, ok in facts.items() if not ok)
result = {'verdict': 'REJECT' if failed else 'ACCEPT', 'scope': 'Returned e8999f966 cache repair, actual private HTTP at immutable published622c0866d; selected cache AST/timing/constants identical',
          'base_commit': s['base_commit'], 'executed_source_tree_commit': s['final_server_commit'],
          'raw_sha256': sha(a.raw), 'facts': facts, 'failed': failed,
          'observation': 'Same97byte/mtime output edit refused on next request, no tampered data. Warm ordinary edit serves verified historical prior; changed snapshot with no fallback refuses. Loaded-copy edit trips reader_stale.',
          'input_timer': {'first_detected_seconds_from_warm_response_end': elapsed, 'requests_observed': len(polls),
              'no_current_response_on_request_started_after60s': no_late, 'warm_verified_at': timer['warm']['body']['verified_at'],
              'detection_verified_at': None if detected is None else detected['body']['verified_at']},
          'cleanup': 'Five exact owned process handles terminal/reaped, netstat0/no owned-port listeners, copied source restored.',
          'limits': 'Method A synthetic tooling/actual HTTP, not shipping FF12/live behavior. Timer verification on incoming requests, not idle background work; polling resolution/HTTP transit limits timing, no multi-file atomicity proof. Production only read-only responsiveness/scope sample: loaded module/PID identity and pending peer source/current deployment not accepted. Whole M3/M0-M5/L1+L2 not complete. Unchanged original build/export observations retain prior source identities; not rerun or credited here.',
          'consumer': 'OPUS structured R2 review/incorporation; propagate request-time timer scope and measured limits into incident/reader claims. Current deployment/final pending-code review remains separate.'}
if a.out.exists(): assert json.loads(a.out.read_text()) == result, 'Preserve old receipt; use new explicit output'
else: a.out.write_text(json.dumps(result, indent=2) + '\n')
print(result['verdict'] + '_SCOPED_CACHE_REPAIR', flush=True)
