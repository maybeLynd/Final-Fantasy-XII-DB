"""Control for the divergence detector: it must report 3 misplacements where 3 exist.

aq18_v1_v2_divergence.py reported MISPLACED 0 over the shipping image. A detector that
cannot see a misplacement at all reports 0 too, so that number is worth nothing until the
detector is shown to find one. ASTRA's fixtures are the ideal positive: on them v1 is KNOWN
to misplace exactly three sites - `xor al,al`, `xor ax,ax` and `mov al,90h` - with Unicorn
as the arbiter. The same comparison code is pointed at the same two sources over those
fixtures instead of the image.

Expected: MISPLACED 3, and each one an address v1 reported that the hardware never wrote.
"""
import contextlib, io, struct, sys, types
from collections import defaultdict
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
LO = 0x2165176
cases = []
def add(name, seed, tail):
    e = 0x100000 + len(cases) * 0x100
    lea = bytes.fromhex('488d05' if seed == 'rax' else '488d1d') + struct.pack('<i', LO - e - 7)
    cases.append(dict(name=name, entry=e, body=lea + bytes.fromhex(tail)))

add('direct-positive',               'rax', 'c60001')
add('call-kills-volatile',           'rax', 'e8f47f0000c60001')
add('call-preserves-nonvolatile',    'rbx', 'e8f47e0000c60301')
add('eax-zero-kills-full-rax',       'rax', '31c0c60001')
add('al-zero-moves-outside-span',    'rax', '30c0c60001')
add('ax-zero-moves-outside-span',    'rax', '6631c0c60001')
add('al-write-changes-exact-target', 'rax', 'b090c60001')
add('add-index-base-zero-index',     'rax', '31c94801c1c60101')
add('add-base-index-zero-index',     'rax', '31c94801c8c60001')
add('add-immediate-positive',        'rax', '4883c001c60001')

NAME = {c['entry']: c['name'] for c in cases}


class Image:
    def __init__(self, *a): pass
    def read(self, ad, n):
        for c in cases:
            o = ad - c['entry']
            if 0 <= o < len(c['body']): return c['body'][o:o + n]
        raise AssertionError(hex(ad))


catalog = 'entry\tbody_bytes\n' + ''.join("%08X\t%d\n" % (c['entry'], len(c['body'])) for c in cases)
INJECT = "            resolved_sites += 1"
COLLECT = INJECT + "\n            _ALL.append((ins.address, addr))"


def run(path):
    src = path.read_bytes().decode("utf-8")
    assert src.count(INJECT) == 1, path.name
    kp = types.ModuleType('kit_paths'); kp.EXE = 'DISPOSABLE'; kp.WORK = 'DISPOSABLE'
    df = types.ModuleType('disasm_fn'); df.Image = Image
    ns = {"__name__": "__divergence_control__", "_ALL": []}
    with patch.dict(sys.modules, {'kit_paths': kp, 'disasm_fn': df}), \
         patch.object(io, 'open', lambda p, *a, **k: io.StringIO(catalog)), \
         contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src.replace(INJECT, COLLECT), str(path), "exec"), ns)
    return ns["_ALL"]


a1 = run(HERE / "aq18_span_write_census.py")
a2 = run(HERE / "aq18_span_write_census_v2.py")
m1, m2 = defaultdict(list), defaultdict(list)
for s, a in a1: m1[s].append(a)
for s, a in a2: m2[s].append(a)

mis = sorted((s, m1[s], m2[s]) for s in set(m1) & set(m2) if sorted(m1[s]) != sorted(m2[s]))
v2_only = sorted(set(m2) - set(m1))
v1_only = sorted(set(m1) - set(m2))

print("MISPLACED %d   V2-ONLY %d   V1-ONLY %d" % (len(mis), len(v2_only), len(v1_only)))
print()
for s, x1, x2 in mis:
    fn = max(e for e in NAME if e <= s)
    print("  %08X  %-32s v1 %s -> v2 %s"
          % (s, NAME[fn], ",".join("%08X" % v for v in x1), ",".join("%08X" % v for v in x2)))
print()
expect = {'al-zero-moves-outside-span', 'ax-zero-moves-outside-span',
          'al-write-changes-exact-target'}
got = {NAME[max(e for e in NAME if e <= s)] for s, _, _ in mis}
if got != expect:
    print("CONTROL FAILED: expected %s, got %s" % (sorted(expect), sorted(got)))
    sys.exit(1)
print("CONTROL PASSES: the detector finds exactly the three misplacements Unicorn proves,")
print("and names them. So MISPLACED 0 over the shipping image is a measurement, not a")
print("detector that cannot see.")
