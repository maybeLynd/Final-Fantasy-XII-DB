"""Check every recorded pulse and cleanup; never infer combat execution."""
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
for label, expected in [('title-enter', 49), ('load-stepping-enter', 49),
                        ('dismiss-load-enter', 49), ('field-menu-enter', 49),
                        ('field-menu-c', 2)]:
    p = E / (label + '.json')
    r = json.loads(p.read_text())
    assert r['status'] == 'REGISTERED_PULSE_ONLY' and r['pid'] == 22784
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
observations = dict(status='INPUT_REGISTRATION_AND_PRESENTATION_CONTROL_ONLY',
    method='C: five bounded pulses from the established sender, read-only process observation',
    pid=22784, exe_sha256=EXE, text_sha256=TEXT, pulses=rows,
    presentation='Screenshots individually inspected: title save list, named save Load complete, field, battle-menu open then closed.',
    cleanup_verified=True, prior_failed_brief_input_cause='UNRESOLVED',
    combat_command_queued=False, combat_action_executed=False,
    limits=['No native caller or write trace.', 'No separation of hold duration from packet form.',
            'FABLE title-poll analysis remains peer-owned but no longer gates this input route.'])
(E / 'observation.json').write_text(json.dumps(observations, indent=2) + '\n')
print(json.dumps(observations, indent=2))
