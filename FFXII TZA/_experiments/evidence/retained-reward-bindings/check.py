"""Read retained EXP081 spans only. No process APIs, input or original-code execution."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct

E = Path(__file__).resolve().parent
OLD = E.parent/'battleunit-live-bindings'
EXPECTED = {'current-complete-memory.json': 'a9ada099cd80f560bf989671cac0ff3be1b4df4d9eb426b2424feea74acc3f33',
            'current-field-memory.json': '9c5769b39267890b4b9d6d3ad9a0b3adce89538a5dd904504f00666f3db97693'}
EXE_SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
TEXT_SHA = '5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
sha = lambda b: hashlib.sha256(b).hexdigest()
q = lambda b, o=0: struct.unpack_from('<Q', b, o)[0]
d = lambda b, o=0: struct.unpack_from('<I', b, o)[0]
w = lambda b, o=0: struct.unpack_from('<H', b, o)[0]


def inputs():
    manifest = json.loads((OLD/'manifest.json').read_text())['files']
    names = list(EXPECTED) + ['cleanup.json', 'exit-check.json', 'save-before.json',
                              'observe.py', 'source-review.json',
                              'current-complete-before.jpg', 'current-field-after.jpg']
    sources, records = {}, {}
    for name in names:
        raw = (OLD/name).read_bytes()
        receipt = manifest[name]
        assert len(raw) == receipt['bytes'] and sha(raw) == receipt['sha256'], name
        if name in EXPECTED:
            assert sha(raw) == EXPECTED[name], name
        sources[name] = dict(bytes=len(raw), sha256=sha(raw))
        if name.endswith('.json'):
            records[name] = json.loads(raw)
    source = records['source-review.json']
    body = (E.parent/'EXP-075-reward-index-prechecks/0023A570.bin').read_bytes()
    assert len(body) == 1808 and sha(body) == source['sha256'] == 'a5194ef62b2556c92117b3ae40980d2ff334a08d495ec9cca82995209cd1d39a'
    assert source['reference_sha256'] == EXE_SHA
    assert sources['observe.py']['sha256'] == source['observer_sha256'] == '3fd84bbf8ffb7acb6f398333275193d7af13bea895f284ded4ccda86689b5438'
    # Original slot loads / destination fields, exactly pinned. No execution.
    for va, raw in {0x23A965: '488b05dc47c802', 0x23A9A5: '48898f700e0000',
                    0x23A9AC: '488b058d47c802', 0x23A9F4: '48898f780e0000'}.items():
        expected = bytes.fromhex(raw)
        assert body[va-0x23A570:va-0x23A570+len(expected)] == expected
    assert 0x23A96C+0x2C847DC == 0x2EBF148
    assert 0x23A9B3+0x2C8478D == 0x2EBF140
    sources['../EXP-075-reward-index-prechecks/0023A570.bin'] = dict(bytes=len(body), sha256=sha(body))
    return records, sources


def reduce(records):
    cleanup, exited = records['cleanup.json'], records['exit-check.json']
    assert cleanup['status'] == 'RESTORED' and not cleanup['processes']
    assert cleanup['backup_unchanged'] and cleanup['files'] == records['save-before.json']['files']
    assert len(cleanup['files']) == 26 and not exited['processes'] and exited['owned_pid'] == 30640
    out = []
    for filename in EXPECTED:
        r = records[filename]
        assert r['status'] == 'OBSERVED' and r['pid'] == 30640
        assert r['exe_sha256'] == EXE_SHA and r['image_base'] == 0x120000
        assert r['modules'] and r['known_read_control'] == '19930d0a1a0a'
        assert r['null_read_rejected'] and r['read_handle_closed']
        assert len(r['code_identity']) == 1
        code = r['code_identity'][0]
        assert code['matches'] and code['bytes'] == 7996981
        assert code['disk_sha256'] == code['live_sha256'] == TEXT_SHA
        assert len(r['samples']) == 2
        for s in r['samples']:
            reads = {x['name']: x for x in s['reads']}
            assert reads and len(reads) == len(s['reads'])
            raw = {}
            for name, span in reads.items():
                b = bytes.fromhex(span['bytes'])
                assert len(b) == span['size'] and sha(b) == span['sha256'], name
                raw[name] = b
            for a, b in [('registry_before', 'registry_after'),
                         ('pool_keep_capacity_before', 'pool_keep_capacity_after'),
                         ('image_address_base_before', 'image_address_base_after')]:
                assert raw[a] == raw[b]
            assert all(s[k] for k in ('registry_stable', 'pool_keep_stable', 'base_stable', 'unit_bindings_stable'))
            for name in ('registry_before', 'registry_after'):
                assert reads[name]['address'] == 0x2EBF120 and reads[name]['size'] == 0x78
            reg = raw['registry_before']
            slot_values = {'base': q(reg, 0x28), 'per_level': q(reg, 0x20)}
            pool, capacity = q(raw['pool_keep_capacity_before']), d(raw['pool_keep_capacity_before'], 24)
            assert pool == s['pool'] and capacity == s['capacity'] == 32
            before, after = raw['battle_unit_pool'], raw['battle_unit_pool_after']
            assert len(before) == len(after) == capacity*0xF50
            assert reads['battle_unit_pool']['address'] == reads['battle_unit_pool_after']['address'] == pool
            base = q(raw['image_address_base_before'])
            units = []
            for slot in range(capacity):
                u, v = (b[slot*0xF50:(slot+1)*0xF50] for b in (before, after))
                # The old observer compared E60..E6F only. Check reward bytes explicitly.
                assert (bool(u[0]&1), u[8:0x18], u[0x698:0x6A8], u[0xE60:0xE80], u[0xEA9]) == (
                    bool(v[0]&1), v[8:0x18], v[0x698:0x6A8], v[0xE60:0xE80], v[0xEA9])
                if not (u[0]&1 and q(u, 0x10) and q(u, 0x698)):
                    continue
                assert u[0xEA9] == slot
                stats_name = f'unit_{slot}_stats'
                stats = raw[stats_name]
                assert len(stats) == 0x1C8 and reads[stats_name]['address'] == q(u, 0x698)
                row = dict(slot=slot, unit=pool+slot*0xF50, actor=q(u, 0x10),
                           stats=q(u, 0x698), kind=stats[5], definition_id=w(stats, 4),
                           definition=q(u, 0xE60), reward_base=q(u, 0xE70),
                           reward_per_level=q(u, 0xE78), reward_bracket_equal=True)
                if row['kind'] == 1:
                    h = raw['enemy_table_header']
                    assert reads['enemy_table_header']['address'] == q(reg)
                    count, stride, ref = d(h, 4), w(h, 8), d(h, 12)
                    start = (base+ref)&0xFFFFFFFFFFFFFFFF
                    table = raw['enemy_table_rows']
                    assert count > 0 and stride >= 0x26 and len(table) == count*stride
                    assert reads['enemy_table_rows']['address'] == start
                    delta = row['definition']-start
                    assert 0 <= delta < len(table) and delta%stride == 0
                    assert delta//stride == stats[4]
                    row.update(enemy_row=delta//stride, reward_base_selector=w(table, delta+0x22),
                               reward_per_level_selector=w(table, delta+0x24))
                units.append(row)
            def covered(pointer, extent):
                return [n for n, z in reads.items() if pointer and z['address'] <= pointer
                        and pointer+extent <= z['address']+z['size']]
            assert covered(0x2EBF120, 0x78) == ['registry_before', 'registry_after']
            if 'enemy_table_header' in reads:
                assert 'enemy_table_header' in covered(q(reg), 0x20)
            out.append(dict(source=filename, sample=s['index'], original_start_unix=s['start_unix'],
                            original_end_unix=s['end_unix'], image_address_base=base,
                            reward_registry_slots=slot_values, registry_bracket_equal=True,
                            occupied_actor_stats_units=units,
                            reward_header_32byte_coverage={k: covered(v, 0x20) for k, v in slot_values.items()},
                            reward_row_first_byte_coverage=[dict(slot=u['slot'], base=covered(u['reward_base'], 1),
                                                                 per_level=covered(u['reward_per_level'], 1)) for u in units]))
    complete = [s for s in out if s['source'].startswith('current-complete')]
    field = [s for s in out if s['source'].startswith('current-field')]
    assert len(complete) == len(field) == 2
    assert all(s['reward_registry_slots'] == dict(base=0, per_level=0) and not s['occupied_actor_stats_units'] for s in complete)
    for s in field:
        assert all(s['reward_registry_slots'].values())
        enemies = [u for u in s['occupied_actor_stats_units'] if u['kind'] == 1]
        party = [u for u in s['occupied_actor_stats_units'] if u['kind'] == 0]
        assert [u['slot'] for u in enemies] == [4, 5, 7] and [u['slot'] for u in party] == [0]
        assert all(u['reward_base'] and u['reward_per_level'] for u in enemies)
        assert party[0]['reward_base'] == party[0]['reward_per_level'] == 0
        assert not any(s['reward_header_32byte_coverage'].values())
        assert all(not u['base'] and not u['per_level'] for u in s['reward_row_first_byte_coverage'])
    return dict(status='RETAINED_SNAPSHOT_OBSERVATIONS_VERIFIED',
                method='A: offline reduction of original EXP081 C observations; no new live run',
                pid=30640, executable_sha256=EXE_SHA, samples=out,
                original_cleanup_verified=True, new_game_session=False,
                limits=['One original process, two samples per stage; sequential non-atomic reads.',
                        'Null slots at the popup are not an observed null installation or death path.',
                        'Nonzero field slot/pointer values do not prove header contents, row validity or lifetime.',
                        'No actual reward header or row bytes were captured in these spans.',
                        'No installer, reward consumer, combat command, action or death was traced.'])


def mutations(records):
    out = []
    for name in ('reward-changed-after-old-stability-flag', 'wrong-registry-address',
                 'empty-field-population', 'restoration-mismatch'):
        bad = copy.deepcopy(records)
        field = bad['current-field-memory.json']
        if name == 'empty-field-population':
            field['samples'] = []
        elif name == 'restoration-mismatch':
            bad['cleanup.json']['files'] = {}
        else:
            reads = {r['name']: r for r in field['samples'][0]['reads']}
            if name == 'wrong-registry-address':
                reads['registry_before']['address'] += 8
            else:
                r = reads['battle_unit_pool_after']
                raw = bytearray.fromhex(r['bytes'])
                raw[4*0xF50+0xE70] ^= 1
                r['bytes'], r['sha256'] = raw.hex(), sha(raw)
                assert field['samples'][0]['unit_bindings_stable'] is True
        try:
            reduce(bad)
        except (AssertionError, KeyError, ValueError):
            out.append(dict(case=name, rejected=True))
        else:
            raise AssertionError(('accepted corrupted observation', name))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutations', action='store_true')
    args = ap.parse_args()
    records, sources = inputs()
    result = reduce(records)
    result['sources'] = sources
    if args.mutations:
        result['receipt_mutations'] = mutations(records)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
