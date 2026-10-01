"""Executed access census of the widget draw record (OPUS, 2026-09-25): 002D8C00's 0xA0-byte record as the widget-tree pass
00245E60 builds, composes and publishes it, over the two-node tree of check.py (root + child, no handlers), up to the recorded
boundary 001DD8C4. The records live on the stack; their addresses are read from the widgets' +0x38 after a first run and are
identical on the second (Session.call starts every call at the same rsp). Output census.json {"root"/"child": {"off/width/rw":
[pc...]}}. Executed domain only: offsets the pass does not touch are absent, not proven dead."""
import collections
import json
import os
import struct
import sys

from unicorn import UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
from unicorn.x86_const import UC_X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "check.py")).read().split("# A - the record builder")[0]
exec(compile(src, "check_prefix", "exec"))
W.ALLOWED |= W.closure(0x217150)
R, C, X = 0x76290000, 0x76291000, 0x76292000


def tree():
    for base in (R, C):
        uc.mem_write(base, bytes(0x200))
    uc.mem_write(R + 0x40, struct.pack("<I", 5)); uc.mem_write(C + 0x40, struct.pack("<I", 5))
    uc.mem_write(R + 0x18, struct.pack("<Q", C)); uc.mem_write(C + 0x10, struct.pack("<Q", R))
    for node in (R, C):
        uc.mem_write(node + 0x9C, struct.pack("<HH", 0x40, 0x20))
        uc.mem_write(node + 0xA0, bytes([0x80, 0x80, 0xFF]))
    uc.mem_write(X, struct.pack("<16f", 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1))


# Hooks are registered BEFORE the only run: unicorn reuses translation blocks compiled without a read callback, so a
# hook added after a first run misses reads (measured: 1 read event). Every stack access is logged raw and classified
# once the run has published the two record addresses in the widgets' +0x38.
raw = []


def mk(rw):
    def h(u, access, a, n, v, _):
        if W.STACK <= a < W.STACK + W.STACK_SZ:
            raw.append((a, n, rw, u.reg_read(UC_X86_REG_RIP)))
    return h


uc.hook_add(UC_HOOK_MEM_WRITE, mk("w")); uc.hook_add(UC_HOOK_MEM_READ, mk("r"))
tree(); ok = S.call(PASS, R, X)
rrec, crec = rd64(R + 0x38), rd64(C + 0x38)
acc = {"root": collections.defaultdict(set), "child": collections.defaultdict(set)}
for a, n, rw, pc in raw:
    for name, base in (("root", rrec), ("child", crec)):
        if base <= a < base + 0xA0:
            acc[name]["%02X/%d/%s" % (a - base, n, rw)].add("%08X" % pc)
out = {"records": {"root": "%X" % rrec, "child": "%X" % crec}, "stop": ["%08X" % a for a in list(S.st["trace"])[-2:]],
       "root": {k: sorted(v) for k, v in sorted(acc["root"].items())}, "child": {k: sorted(v) for k, v in sorted(acc["child"].items())}}
json.dump(out, open(os.path.join(HERE, "census.json"), "w"), indent=1, sort_keys=True)
for name in ("root", "child"):
    print(name, " ".join(sorted(out[name])))
print("stop", out["stop"])
