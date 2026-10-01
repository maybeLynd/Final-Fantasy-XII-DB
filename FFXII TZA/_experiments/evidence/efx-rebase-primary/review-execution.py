"""Review saved original-code EFX traces; does not execute original code."""
import copy
import hashlib
import json
from pathlib import Path
import struct

work = Path('Database/Tools/work/ASTRA')
raw = (work/'efx-rebase-result.json').read_bytes()
receipt = json.loads(raw)
cases = receipt['cases']
assert len(cases) == 15 and len({c['name'] for c in cases}) == 15
MASK = (1 << 64)-1
CTX, TABLE, A00 = 0x50000000, 0x50002000, 0x50004000

def memory_review(c):
    assert c['returned'] and c['stack_ok'] and c['nonvolatile_ok']
    assert c['code_unchanged'] and c['error'] is None and not c['invalid']
    assert c['visited'] and c['calls']
    mem = {}
    for a, h in c['injected_writes']:
        mem.update({int(a, 16)+i: v for i, v in enumerate(bytes.fromhex(h))})
    for a, h in c['before'].items():
        assert bytes(mem.get(int(a, 16)+i, 0) for i in range(len(h)//2)).hex() == h
    for ip, op, a, n, value in c['memory']:
        a = int(a, 16)
        assert ip in c['visited'] and n > 0
        if op == 'R':
            assert bytes(mem.get(a+i, 0) for i in range(n)).hex() == value, (c['name'], ip, hex(a), 'read')
        else:
            assert op == 'W'
            b = int(value, 16).to_bytes(n, 'little')
            mem.update({a+i: v for i, v in enumerate(b)})
    for a, h in c['after'].items():
        assert bytes(mem.get(int(a, 16)+i, 0) for i in range(len(h)//2)).hex() == h, (c['name'], a, 'final')

def u64(c, a, offset=0, which='after'):
    return struct.unpack_from('<Q', bytes.fromhex(c[which][hex(a)]), offset)[0]

globals_expected = {0x2F97340: CTX, 0x2EBEF70: CTX+0x18, 0x2EBEFA8: CTX+0x38,
                    0x2EBEFA0: CTX+0x840, 0x2EBEF90: CTX+0x848, 0x2EBEF78: CTX+0x850}
summaries = []
for c in cases:
    memory_review(c)
    writes = [v for v in c['memory'] if v[1] == 'W']
    row = dict(name=c['name'], memory_events=len(c['memory']), writes=len(writes),
               calls=[v['target'] for v in c['calls']])
    if c['name'].startswith('provider-'):
        assert c['rax'] == c['prediction']['return_value'] and c['prediction_matches']
        assert not writes
        expected_read = c['name'] not in ('provider-null', 'provider-invalid-small-tag', 'provider-untagged-full')
        assert len(c['memory']) == int(expected_read)
        if expected_read:
            assert c['memory'][0][:4] == ['0x36b14d', 'R', '0x500008', 8]
        row['return_value'] = c['rax']
    elif c['name'].startswith('context-'):
        p = c['prediction']
        assert u64(c, CTX, 0x858) == int(p['stored_base'], 16)
        assert u64(c, TABLE) == int(p['table0'], 16)
        assert u64(c, TABLE, 8) == int(p['table1'], 16)
        assert u64(c, TABLE, 0x9F8) == int(p['table_last'], 16)
        assert c['before'][hex(A00)] == c['after'][hex(A00)]
        changed = c['name'] in ('context-positive-forward', 'context-positive-backward', 'context-fourGiB-difference')
        enabled = c['name'] != 'context-flag-clear'
        expected_writes = dict(globals_expected) if enabled else {}
        if changed:
            expected_writes.update({CTX+0x858: int(p['stored_base'], 16),
                                    TABLE+8: int(p['table1'], 16),
                                    TABLE+0x9F8: int(p['table_last'], 16)})
            dispatch = [v for v in c['calls'] if v['target'] == '0x442460']
            assert len(dispatch) == 2
            for call, field in zip(dispatch, ('table1', 'table_last')):
                assert int(call['args'][0], 16) == int(p[field], 16)
                assert int(call['args'][1], 16) == int(p['delta32'], 16)
                following = c['memory'][call['event_index']]
                assert following[:4] == ['0x442460', 'R', hex(int(p[field], 16)+0x282), 1]
                assert following[4] == '09'
            table_reads = [int(a, 16) for ip, op, a, n, v in c['memory']
                           if op == 'R' and ip == '0x3a988a']
            assert table_reads == list(range(TABLE+8, TABLE+0xA00, 8))
            a00_reads = [int(a, 16) for ip, op, a, n, v in c['memory']
                         if op == 'R' and ip == '0x3a9bca']
            assert a00_reads == list(range(A00+8, A00+0x1800, 8))
            assert writes[-1][:4] == ['0x24d9a7', 'W', hex(CTX+0x858), 8]
        assert len(writes) == len(expected_writes)
        assert {int(a, 16): int(v, 16) for ip, op, a, n, v in writes} == expected_writes
        assert all(n == 8 for ip, op, a, n, v in writes)
        if c['name'] == 'context-flag-clear':
            assert len(c['memory']) == 1 and len(c['calls']) == 1
        if 'sign-extension' in c['name']:
            assert c['calls'][1]['target'] == '0x3ab7f0'
            assert c['calls'][1]['args'][0] == '0xffffffff80002000'
            assert len(c['calls']) == 2
        row.update(stored_base=hex(u64(c, CTX, 0x858)), entry1=hex(u64(c, TABLE, 8)),
                   signed_delta=p['signed_delta'])
    else:
        assert c['name'] == 'instance-direct-negative-delta'
        expected = {0x51000000+0x390: 0x3FFFF000}
        for a, offsets in ((0x51001000, (0x100, 0x108)), (0x51002000, (0x100, 0x108)),
                           (0x51003000, (0x18, 0x20)), (0x51004000, (0x18, 0x20))):
            for offset in offsets:
                expected[a+offset] = (u64(c, a, offset, 'before')-0x1000) & MASK
                assert u64(c, a, offset) == expected[a+offset]
        assert len(writes) == len(expected)
        assert {int(a, 16): int(v, 16) for ip, op, a, n, v in writes} == expected
        assert all(n == 8 for ip, op, a, n, v in writes)
        assert writes[-1][:4] == ['0x24d95d', 'W', '0x51000390', 8]
        assert u64(c, 0x51001000, 0x108) == u64(c, 0x51003000, 0x20) == 0xFFFFFFFFFFFFF000
        row['zero_fields_become'] = '0xfffffffffffff000'
    summaries.append(row)

# Reader negative control: remove a real nonzero table repair from a private trace copy.
# The return and ABI flags still pass; complete memory/final-state reconciliation must fail.
damaged = copy.deepcopy(next(c for c in cases if c['name'] == 'context-positive-forward'))
del damaged['memory'][next(i for i, v in enumerate(damaged['memory'])
                          if v[:4] == ['0x3a98a8', 'W', '0x50002008', 8])]
try:
    memory_review(damaged)
except AssertionError as e:
    negative = dict(intervention='Omitted one table write in private receipt copy; original receipt unchanged',
                    rejected=True, reason=str(e))
else:
    raise AssertionError('incomplete-memory reader control failed')

result = dict(evidence_class='B: isolated shipping code in injected state, not live gameplay',
              receipt_sha256=hashlib.sha256(raw).hexdigest(),
              cases=summaries, negative_control=negative,
              final='All 15 nonempty instruction runs return with original code intact, ABI preserved, and complete nonstack memory/final-state reconciliation. Native handler, caller initialization and scheduling limits remain.')
(work/'efx-rebase-execution-review.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, indent=2))
