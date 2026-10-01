"""Review current raw input, tracer and cleanup receipts; never promote an incomplete campaign."""
import hashlib
import json
from pathlib import Path

E = Path(__file__).resolve().parent
REPO = E.parents[5]
sha = lambda b: hashlib.sha256(b).hexdigest()
EXE = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
TEXT = '5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
SENDER = '7a635333e0a842ca140cc64e03d98b4e70cd9944cea776a8f064c3f279c76fae'
rows = []
for label, expected in [('title-enter', 49), ('load-enter', 49), ('dismiss-enter', 49),
                        ('baseline-enter', 49), ('baseline-c', 2),
                        ('capture-enter', 49), ('capture-c', 2)]:
    p = E / (label + '.json')
    r = json.loads(p.read_text())
    assert r['status'] == 'REGISTERED_PULSE_ONLY' and r['pid'] == 40504
    assert r['null_read_rejected'] and r['read_handle_closed']
    assert r['down_accepted'] == r['up_accepted'] == 2
    assert r['seen_indices'] == [expected] and .35 <= r['held_elapsed'] < .5
    assert not r.get('error')
    for path, digest in r['sources'].items():
        assert sha((REPO / path).read_bytes()) == digest, path
        if path.endswith('/runtime_input_probe.py'):
            assert digest == SENDER, 'The historical sender changed'
    for key in ('before', 'after'):
        q = r[key]
        assert q['exe_sha256'] == EXE and q['image_base'] == 0x120000
        assert q['module_verdict'] == 'clean' and q['modules']
        assert len(q['code_identity']) == 1
        code = q['code_identity'][0]
        assert code['bytes'] == 7996981
        assert code['disk_sha256'] == code['live_sha256'] == TEXT
    groups = {phase: [s for s in r['samples'] if s['phase'] == phase]
              for phase in ('baseline', 'held', 'release')}
    assert len(groups['baseline']) == 35 and groups['held'] and len(groups['release']) == 1
    addresses = set()
    for s in r['samples']:
        raw = bytes.fromhex(s['raw'])
        assert len(raw) == 256
        indices = [i for i, v in enumerate(raw) if v]
        assert indices == s['nonzero_indices']
        assert s['status'] == 'STABLE_CHAIN' and s['chain_before'] == s['chain_after']
        assert s['array_address'] == s['array_address_after']
        addresses.add(s['array_address'])
        assert set(indices) <= {expected}
    assert len(addresses) == 1
    assert not any(s['nonzero_indices'] for s in groups['baseline'] + groups['release'])
    assert any(s['nonzero_indices'] == [expected] for s in groups['held'])
    rows.append(dict(receipt=p.name, sha256=sha(p.read_bytes()), expected_index=expected,
                     code=expected+28, held_seconds=r['held_elapsed'],
                     baseline_samples=len(groups['baseline']), held_samples=len(groups['held']),
                     positive_samples=sum(bool(s['nonzero_indices']) for s in groups['held']),
                     module_count_before=len(r['before']['modules']),
                     module_count_after=len(r['after']['modules'])))

cleanup = json.loads((E / 'cleanup.json').read_text())
before = json.loads((E / 'save-before.json').read_text())
assert cleanup['status'] == 'RESTORED' and not cleanup['processes']
assert cleanup['backup_unchanged'] and cleanup['files'] == before['files']
assert len(cleanup['files']) == 26 and cleanup['changed_keys'] == ['LUIDLow']
for root in (Path(before['source']), Path(before['backup'])):
    current = {str(p.relative_to(root)): dict(bytes=p.stat().st_size, sha256=sha(p.read_bytes()))
               for p in root.rglob('*') if p.is_file()}
    assert current == before['files']
controls = json.loads((E / 'guard-controls.json').read_text())['results']
assert len(controls) == 4 and all(not r['down_after'] for r in controls)
assert controls[0]['error'] is None and all(r['error'] for r in controls[1:])

load = lambda name: json.loads((E / name).read_text())
capture = load('deadline-capture/result.json')
api = load('deadline-capture/api.json')
invocation = load('capture-invocation.json')
assert invocation['exit_code'] == 0 and not invocation['stderr']
assert capture['status'] == 'PASS' and not capture['errors'] and capture['detach']
assert capture['hits'] and all(h['rip'] == 0x3A1C50 for h in capture['hits'])
assert all(ok for _, ok in capture['arming']) and capture['arming']
clear = capture['cleanup']
assert clear['status'] == 'PASS' and clear['clears'] and clear['verified']
assert all(ok for _, ok in clear['clears'] + clear['verified'])
assert {tid for tid, _ in clear['clears']} == {tid for tid, _ in clear['verified']}
assert all(x['result'] for x in api if 'result' in x)
for op in ('DebugActiveProcess', 'DebugSetProcessKillOnExit', 'DebugBreakProcess',
           'stopped_cleanup', 'DebugActiveProcessStop', 'capture_end'):
    assert len([x for x in api if x['operation'] == op]) == 1, op
detach = next(x for x in api if x['operation'] == 'DebugActiveProcessStop')['unix']
cleanup_start = next(x for x in api if x['operation'] == 'timeout_cleanup_begin')['unix']
readbacks = [x['context'] for x in api if x['operation'] == 'GetThreadContext'
             and cleanup_start <= x['unix'] < detach]
assert len(readbacks) >= len(clear['verified'])
assert all(not c[k] for c in readbacks[-len(clear['verified']):]
           for k in ('Dr0', 'Dr1', 'Dr2', 'Dr3', 'Dr7'))
for path, digest in load('origins.json')['unchanged_capture'].items():
    assert sha((REPO / path).read_bytes()) == digest == capture['sources'][Path(path).name]

windows = {}
for label in ('baseline', 'capture'):
    w = load(label + '-window.json')
    assert w['status'] == 'OBSERVED' and w['pid'] == 40504 and w['samples']
    assert w['exe_sha256'] == EXE and w['code_identity'][0]['live_sha256'] == TEXT
    assert w['code_identity'][0]['matches'] and w['module_verdict'] == 'clean'
    samples = w['samples']
    assert samples[-1]['seconds'] >= 64.9
    assert all(x['foreground_pid'] == 40504 for x in samples)
    assert all(a['seconds'] < b['seconds'] and a['cpu_seconds'] <= b['cpu_seconds']
               for a, b in zip(samples, samples[1:]))
    bins = []
    for start in range(0, 60, 10):
        interval = [x for x in samples if start <= x['seconds'] < start + 10]
        assert interval and interval[-1]['cpu_seconds'] > interval[0]['cpu_seconds']
        bins.append(interval[-1]['cpu_seconds'] - interval[0]['cpu_seconds'])
    debugs = [x for x in samples if x['debugger_present']]
    assert bool(debugs) == (label == 'capture')
    inputs = {key: load(label + '-' + key + '.json')['down_at_unix'] - w['window_start_unix']
              for key in ('enter', 'c')}
    windows[label] = dict(samples=len(samples), end_seconds=samples[-1]['seconds'],
        debugger_samples=len(debugs), cpu_10s_deltas=bins, input_offsets=inputs)
    if label == 'capture':
        post = [x for x in samples if w['window_start_unix'] + x['seconds'] >= detach]
        assert post and not any(x['debugger_present'] for x in post)
        post_bins = []
        for offset in (0, 5, 10, 15):
            group = [x for x in post if offset <= x['seconds'] - post[0]['seconds'] < offset + 5]
            assert group and group[-1]['cpu_seconds'] > group[0]['cpu_seconds']
            post_bins.append(group[-1]['cpu_seconds'] - group[0]['cpu_seconds'])
        windows[label].update(post_detach_seconds=post[-1]['seconds'] - post[0]['seconds'],
            post_detach_samples=len(post), post_detach_5s_cpu_deltas=post_bins)

assert all(load('capture-' + key + '.json')['down_at_unix'] > detach for key in ('enter', 'c'))
# A partial run must never inherit the tracer CLI's PASS label as campaign completion.
missing = ['separate 65-second post window', 'matched input timing across three windows']
assert not (E / 'post-window.json').exists()
observations = dict(status='PARTIAL_POSITIVE_ORIGINAL_CAMPAIGN_INCOMPLETE', method='C',
    pid=40504, exe_sha256=EXE, text_sha256=TEXT, pulses=rows,
    capture=dict(hits=len(capture['hits']), entry='003A1C50',
        hit_threads=sorted({h['tid'] for h in capture['hits']}),
        cleared_threads=len(clear['clears']), verified_threads=len(clear['verified']),
        api_records=len(api), detach_unix=detach, sources=capture['sources']),
    windows=windows, original_campaign_complete=False, outstanding_controls=missing,
    cleanup_verified=True, prior_failed_brief_input_cause='UNRESOLVED',
    combat_command_queued=False, combat_action_executed=False,
    presentation='Screenshots inspected: named Stepping save, load complete, field; menu opens and closes before/after tracing; Vaan103/103.',
    limitations=['No separate post window; no timing-equivalent CPU/overhead comparison.',
        'Debugging and simulated input are interventions; no memory writes or injected native gameplay calls.',
        'Debugger presence and CPU are sampled sequentially, not atomic whole-process proof.',
        'One loaded state and one 1-second site; no combat handler, stack extension or long-run qualification.',
        'Clean modules means the recorded census and watched-module policy; no universal module-state guarantee.'])
(E / 'observation.json').write_text(json.dumps(observations, indent=2) + '\n')
print(json.dumps({k:v for k,v in observations.items() if k not in ('pulses','capture')},indent=2))
