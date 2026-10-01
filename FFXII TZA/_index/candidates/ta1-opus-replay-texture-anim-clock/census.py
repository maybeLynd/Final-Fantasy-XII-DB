"""Executed access census of the tag-23 slot family (OPUS, 2026-09-25): every read and write the builder 00466E70, the binder
004677A0, the accumulator 004678E0 and the advance 004668C0 make into the 0x50 slots, the 0x18 track entries and the 0x130
records, over the shipped dst0101 chunk (same world as check.py). Output: census.json {phase: {kind: {"off/width/rw": [pc]}}}.
Executed domain only - offsets no phase touches are absent, not proven dead.

REVISED the same day: the first version registered its READ hook after the build phase had run, and unicorn reuses
translation blocks compiled without a read callback, so reads in code first run during the build (the builder runs one bind
and one advance) could be missed. Both hooks are now registered before the build; every access to the arena-6 block is
logged raw and classified after the build has published the layout."""
import collections
import json
import os
import sys

from unicorn import UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
from unicorn.x86_const import UC_X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0]]
src = open(os.path.join(HERE, "check.py")).read().split("okB = S.call(BUILD, CH)")[0]
exec(compile(src, "check_prefix", "exec"))          # world, arena 6, chunk placed at CH - identical to check.py

phase = ["build"]
raw = []


def mk(rw):
    def h(u, access, a, n, v, _):
        if blk <= a < blk + 0x400400:
            raw.append((phase[0], a, n, rw, u.reg_read(UC_X86_REG_RIP)))
    return h


uc.hook_add(UC_HOOK_MEM_WRITE, mk("w")); uc.hook_add(UC_HOOK_MEM_READ, mk("r"))
okB = S.call(BUILD, CH)
count, table = dw(0x2EBB6E0), q(0x2EBB6F0)
regions = [(table, count * 0x50, "slot", 0x50)]
for i in range(count):
    s = table + i * 0x50
    nt, nr = w16(s + 0x30), w16(s + 0x32)
    if q(s + 0x20) and nt > 0:
        regions.append((q(s + 0x20), nt * 0x18, "track", 0x18))
    if q(s + 0x28) and nr > 0:
        regions.append((q(s + 0x28), nr * 0x130, "record", 0x130))
rets = {"build_returned": okB}
for ph, fn, kw in (("bind", BIND, {}), ("accumulate", ACCUM, {"xmm": {0: 1.0}}), ("advance", ADVANCE, {})):
    phase[0] = ph
    rets[ph + "_returned"] = S.call(fn, **kw)
acc = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(set)))
for ph, a, n, rw, pc in raw:
    for base, size, kind, stride in regions:
        if base <= a < base + size:
            acc[ph][kind]["%03X/%d/%s" % ((a - base) % stride, n, rw)].add("%08X" % pc)
            break
out = {ph: {k: {o: sorted(p) for o, p in sorted(v.items())} for k, v in kinds.items()} for ph, kinds in acc.items()}
out.update(rets)
json.dump(out, open(os.path.join(HERE, "census.json"), "w"), indent=1, sort_keys=True)
for ph in ("build", "bind", "accumulate", "advance"):
    for kind, offs in sorted(out.get(ph, {}).items()):
        print(ph, kind, " ".join(sorted(offs)))
