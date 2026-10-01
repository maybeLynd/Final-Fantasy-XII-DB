"""descriptor_drains.py - the facts under FABLE's 2026-09-27 descriptor qualification (FABLE, Claude Opus 5.5; on
ASTRA-RETURN-FABLE-DESCRIPTOR-MEMBERSHIP-PROVENANCE). Static.

  D1 the first free-walk skips an unowned node: 00633415 test byte [rbx+0x20], 1 / 00633419 je (leave linked, no free).
  D2 later in the same body (00633390) the drains run after it: from 006334B2 to the +0x60 hand-off, every node store
     is an unlink/self-link and the only call is the hand-off 0063355B -> 006B6700 (drain loops contain no call).
  D3 006B6700, the +0x60 drain, contains no call at all (unlink only).
  D4 planted negative: the free-walk region 00633400-0063344C DOES contain calls (the two frees), so the "no call"
     matcher is sensitive.
The qualification this supports: an unlink without a free shows the destructor does not own a node, not where the node's
storage came from. Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, b): return [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(b)], a)]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
fw = {a: "%s %s" % (m, o) for a, m, o in ins(0x633400, 0x63344C)}
check("D1 the free-walk skips an unowned node",
      fw.get(0x633415) == "test byte ptr [rbx + 0x20], 1" and fw.get(0x633419) == "je 0x633449")
dr = ins(0x6334B2, 0x633560)
calls = [(a, o) for a, m, o in dr if m == "call"]
check("D2 the drains call nothing but the +0x60 hand-off",
      calls == [(0x63355B, "0x6b6700")], str(["%08X %s" % c for c in calls]))
body = ins(0x6B6700, 0x6B6700 + 0x60)
end = next((i for i, (a, m, o) in enumerate(body) if m == "ret"), None)
check("D3 the +0x60 drain calls nothing", end is not None and not any(m == "call" for a, m, o in body[:end]),
      "ret at %s" % (("%08X" % body[end][0]) if end is not None else None))
check("D4 planted negative: the free-walk region does contain calls", any(m == "call" for a, m, o in ins(0x633400, 0x63344C)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
