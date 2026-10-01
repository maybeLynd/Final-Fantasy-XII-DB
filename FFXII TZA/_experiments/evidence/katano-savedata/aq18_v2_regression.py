"""Run ASTRA's ten falsifying fixtures against the REPAIRED v2 tracker.

The fixtures, the synthetic bytes and the Unicorn ground truth are ASTRA's, taken from
../astra-census-impact/check.py so that the repair is judged by the same controls that
broke v1 rather than by controls chosen after the fact. The bar is raised: v1 was scored
"did it invent an address", v2 is scored EXACTLY - for every fixture the reported set must
equal the address Unicorn actually observed when that address lies in the span, and must
be empty when it does not. A miss now counts as a failure, not as a safe loss.
"""
import contextlib, io, struct, sys, types
from pathlib import Path
from unittest.mock import patch
import capstone
import unicorn
from unicorn import x86_const as U

HERE = Path(__file__).resolve().parent
source = (HERE / 'aq18_span_write_census_v2.py').read_bytes()
LO = 0x2165176

cases = []
def add(name, seed, tail, expected):
    entry = 0x100000 + len(cases) * 0x100
    lea = bytes.fromhex('488d05' if seed == 'rax' else '488d1d') + struct.pack('<i', LO - entry - 7)
    cases.append(dict(name=name, entry=entry, body=lea + bytes.fromhex(tail), expected=expected))

add('direct-positive',                'rax', 'c60001',           LO)
add('call-kills-volatile',            'rax', 'e8f47f0000c60001', 0)
add('call-preserves-nonvolatile',     'rbx', 'e8f47e0000c60301', LO)
add('eax-zero-kills-full-rax',        'rax', '31c0c60001',       0)
add('al-zero-moves-outside-span',     'rax', '30c0c60001',       LO & ~0xff)
add('ax-zero-moves-outside-span',     'rax', '6631c0c60001',     LO & ~0xffff)
add('al-write-changes-exact-target',  'rax', 'b090c60001',       (LO & ~0xff) | 0x90)
add('add-index-base-zero-index',      'rax', '31c94801c1c60101', LO)
add('add-base-index-zero-index',      'rax', '31c94801c8c60001', LO)
add('add-immediate-positive',         'rax', '4883c001c60001',   LO + 1)
assert len(cases) == 10


class Image:
    def __init__(self, *a): pass
    def read(self, address, count):
        for c in cases:
            off = address - c['entry']
            if 0 <= off < len(c['body']): return c['body'][off:off + count]
        raise AssertionError(hex(address))


catalog = 'entry\tbody_bytes\n' + ''.join("%08X\t%d\n" % (c['entry'], len(c['body'])) for c in cases)
kp = types.ModuleType('kit_paths'); kp.EXE = 'DISPOSABLE_FIXTURE'; kp.WORK = 'DISPOSABLE_CATALOG'
df = types.ModuleType('disasm_fn'); df.Image = Image
stdout = io.StringIO(); ns = {'__name__': '__v2_regression_control__'}
def fake_open(path, *a, **k):
    assert str(path).replace('\\', '/') == 'DISPOSABLE_CATALOG/graph/functions.tsv', path
    return io.StringIO(catalog)
with patch.dict(sys.modules, {'kit_paths': kp, 'disasm_fn': df}), \
     patch.object(io, 'open', fake_open), contextlib.redirect_stdout(stdout):
    exec(compile(source.decode('utf-8'), str(HERE / 'aq18_span_write_census_v2.py'), 'exec'), ns)
assert len(ns['fns']) == 10

fails = []
print("%-34s %-10s %-10s %-8s %s" % ("fixture", "truth", "v2 says", "prov", "verdict"))
for c in cases:
    machine = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    for base, size in ((0x100000, 0x10000), (0x2160000, 0x10000), (0, 0x1000), (0x200000, 0x10000)):
        machine.mem_map(base, size)
    machine.reg_write(U.UC_X86_REG_RSP, 0x208000)
    machine.mem_write(c['entry'], c['body'])
    machine.mem_write(0x108100, bytes.fromhex('31c0c3'))      # the legal test callee
    writes = []
    machine.hook_add(unicorn.UC_HOOK_MEM_WRITE,
                     lambda uc, acc, ad, sz, val, u: (None if 0x200000 <= ad < 0x210000
                                                      else writes.append(ad)))
    machine.emu_start(c['entry'], c['entry'] + len(c['body']), count=40)
    assert writes == [c['expected']], (c['name'], writes)

    hits = [h for h in ns['span_hits'] if h[1] == c['entry']]
    got = [h[2] for h in hits]
    prov = ",".join(sorted({h[6] for h in hits})) or "-"
    want = [c['expected']] if ns['LO'] <= c['expected'] < ns['HI'] else []
    ok = got == want
    if not ok: fails.append(c['name'])
    print("%-34s %-10s %-10s %-8s %s" % (
        c['name'], "%08X" % c['expected'],
        ",".join("%08X" % g for g in got) or "(none)", prov,
        "ok" if ok else "FAIL want %s" % ([("%08X" % w) for w in want] or "(none)")))

print()
if fails:
    print("REGRESSION FAILED on %d of 10: %s" % (len(fails), ", ".join(fails)))
    sys.exit(1)
print("PASS: 10 of 10 exact. The five fixtures that falsified v1 - three misplaced")
print("partial-register targets and two missed register-add writes - are now correct,")
print("and the five v1 already handled are unchanged.")
print("BOUND: all ten fixtures are straight-line. None of them tests the linear decode,")
print("which is v2's remaining unsoundness and was v1's too.")
