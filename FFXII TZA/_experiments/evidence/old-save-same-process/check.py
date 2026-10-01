"""Reduce only this retained, incomplete setup run; never opens FF12."""
import copy
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parent
EXE = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
TEXT = '5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
PULSES = {
    'title-enter': 49, 'load-modern-enter': 49, 'dismiss-modern-enter': 49,
    'open-main-menu-r': 17, 'cancel-status-c': 2, 'select-config-i': 8,
    'open-config-enter': 49,
}
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda name: json.loads((ROOT / name).read_text(encoding='utf-8'))


def identity(r):
    assert r['exe_sha256'] == EXE and r['image_base'] == 0x120000
    assert r['module_verdict'] == 'clean' and r['modules']
    assert len(r['code_identity']) == 1
    c = r['code_identity'][0]
    assert c['bytes'] == 7996981 and c['disk_sha256'] == c['live_sha256'] == TEXT


def pulse(r, expected):
    assert r['status'] == 'REGISTERED_PULSE_ONLY' and r['pid'] == 52384
    assert r['hwnd'] == 102564144 and r['read_handle_closed'] and r['null_read_rejected']
    assert r['down_accepted'] == r['up_accepted'] == 2
    identity(r['before']); identity(r['after'])
    counts = dict(baseline=0, held=0, release=0)
    positive = 0
    for s in r['samples']:
        assert s['status'] == 'STABLE_CHAIN'
        assert s['array_address'] == s['array_address_after']
        assert s['chain_before'] == s['chain_after']
        raw = bytes.fromhex(s['raw'])
        assert len(raw) == 256
        nz = [i for i, value in enumerate(raw) if value]
        assert nz == s['nonzero_indices']
        counts[s['phase']] += 1
        if s['phase'] == 'held':
            assert set(nz) <= {expected}
            positive += bool(nz)
        else:
            assert not nz
    assert counts['baseline'] == 35 and counts['held'] > 0 and counts['release'] == 1
    assert positive > 0 and r['seen_indices'] == [expected]
    return dict(samples=counts, positive_held_samples=positive,
                index=expected, held_seconds=r['held_elapsed'])


def main():
    results = {n: pulse(load(n + '.json'), i) for n, i in PULSES.items()}
    original = load('open-main-menu-r.json')
    empty = copy.deepcopy(original); empty['samples'] = []
    no_detection = copy.deepcopy(original)
    for s in no_detection['samples']:
        s['raw'] = '00' * 256; s['nonzero_indices'] = []
    for name, bad in [('empty', empty), ('no_detection', no_detection)]:
        try:
            pulse(bad, 17)
        except AssertionError:
            pass
        else:
            raise AssertionError(name + ' false pass')

    r = load('current-field-memory.json')
    identity(r)
    assert r['status'] == 'OBSERVED' and r['pid'] == 52384 and r['read_handle_closed']
    assert r['known_read_control'] == '19930d0a1a0a' and r['null_read_rejected']
    assert len(r['samples']) == 2
    samples = []
    for s in r['samples']:
        assert s['registry_stable'] and s['pool_keep_stable'] and s['base_stable']
        assert s['unit_bindings_stable']
        spans = {v['name']: v for v in s['reads']}
        assert len(spans) == len(s['reads']) == 26
        data = {}
        for name, v in spans.items():
            raw = bytes.fromhex(v['bytes'])
            assert len(raw) == v['size'] and sha(raw) == v['sha256']
            data[name] = raw
        for a, b in [('registry_before', 'registry_after'),
                     ('pool_keep_capacity_before', 'pool_keep_capacity_after'),
                     ('image_address_base_before', 'image_address_base_after')]:
            assert data[a] == data[b]
        B = struct.unpack_from('<Q', data['registry_before'], 0x70)[0]
        assert B == s['battle_binding'] == 0x21B290C
        image = data['active_save_image']; block = data['bound_battle_block']
        assert spans['active_save_image']['address'] == 0x2164280
        assert spans['bound_battle_block']['address'] == B
        assert block == image[0x4E68C:0x4E68C + 0x7410]
        samples.append(dict(index=s['index'], full_spans=len(spans),
                            battle_stamp=hex(struct.unpack_from('<I', block)[0]),
                            levels=[block[8 + i * 0x1C8 + 0x1C2] for i in range(6)],
                            keep_nonzero_bytes=[sum(x != 0 for x in data['keep_bank_' + str(i)]) for i in (1, 2)],
                            field_id=hex(struct.unpack_from('<H', image, 0x1244)[0]),
                            battle_sha256=sha(block), keep_bindings=s['keep_bindings'],
                            history=list(struct.unpack('<IHHI', data['field_history_stamp_before']))))

    before, after = load('save-before.json'), load('cleanup.json')
    assert len(before['files']) == 26 and before['files'] == after['files']
    assert after['status'] == 'RESTORED' and after['backup_unchanged']
    assert after['changed_keys'] == ['LUIDLow'] and after['processes'] == []
    assert load('process-after.json')['processes'] == []
    assert load('reference-after.json')['sha256'] == EXE
    assert load('reference-after.json')['pc_control_reset']
    assert not list(ROOT.glob('old-after-current-*-memory.json'))
    assert not (ROOT / 'returned-title-memory.json').exists()
    output = dict(status='VALID_SETUP_EVIDENCE_ONLY',
                  intended_save_question='INCOMPLETE: older load and returned title never reached',
                  method='Offline reduction of retained live reads and OS-input observations',
                  pulses=results, samples=samples, negative_controls_rejected=['empty', 'no_detection'],
                  cleanup_verified=True,
                  limits=['Registration is not menu acceptance: inspect the associated screenshots.',
                          'A held navigation key can repeat; one pulse is not one menu step.',
                          'No same-process older load, lifetime, reset writer or native call order is established.',
                          'One initialized modern field; sequential reads are not atomic.'])
    (ROOT / 'observation.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print('VALID_SETUP_EVIDENCE_ONLY: seven registered/released pulses; two samples/52 spans; empty/no-detection rejected.')
    print('Older-save comparison INCOMPLETE. All26 original hashes restored; PC control off.')
    for s in samples:
        print('sample', s['index'], 'levels', s['levels'], 'keep nonzero', s['keep_nonzero_bytes'])


if __name__ == '__main__':
    main()
