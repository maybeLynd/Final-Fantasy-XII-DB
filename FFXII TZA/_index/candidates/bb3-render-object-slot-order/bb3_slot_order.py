"""bb3_slot_order.py - BB-3: the order in which a character render record's draw calls its CharacterRenderObject's slots
(FABLE, Claude Opus 5.5, 2026-09-26). Static.

  O1 the record draw 0053AB50 (called only by 0053D780, twice when record +8 bit 0 is set - pass 0 then pass 1 -
     which 00504700 reaches from the render-command path) calls the object through the 0017EFxx-0017F2xx wrappers.
     Each wrapper forwards to one vtable slot (vtable 00903B68); in address order the draw reaches slots
     11, 1, 1, 8, 9, 21, 22, 23, 24, 15, 26, 12, 17, 6, 16.
  O2 no backward jump in 0053AB50 lands between two of those calls and jumps back over one, so address order is
     execution order: each runs at most once per draw call, in that order (each is conditional).
  O3 slot 16 (CharacterRenderObject_SubmitMaterialsWithFadeMode, 001FA3D0) calls, on this (r14 = its rcx), per element:
     slot 14, slot 19, slot 20 (element kinds 2, 5, 10, 13 only: bt 0x2424), slot 10, slot 13 - in that order.
  O4 of the thirteen entry-gated/per-element latch readers, the draw therefore orders 8 -> 9 -> 24 -> 12 -> 16, and
     16 orders 14 -> 19 -> 20 -> 10 -> 13 per element. Slot 3 is the pool's expiry test (001BDAC0, on pooled objects
     only); slot 30 is called from 001F5D70.
  O5 sensitivity: a mis-mapped wrapper would break O1; the check pins each wrapper's single forwarded slot.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
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
def dis(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
DISP = re.compile(r"qword ptr \[r\w+ \+ (0x[0-9a-f]+|\d+)\]")
FUNCS = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = line.rstrip(chr(10)).split(chr(9))
    try: FUNCS[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
def wslot(w):
    """the single vtable slot a wrapper forwards to (call/jmp qword ptr [reg + disp]), within the wrapper's own body;
    None for a wrapper that calls helpers instead (0017F190, 0017F1D0)."""
    s = [int(m.group(1), 0) // 8 for x in dis(w, FUNCS[w]) if x.mnemonic in ("call", "jmp")
         for m in [DISP.fullmatch(x.op_str)] if m]
    return s[0] if s else None
draw = dis(0x53AB50, 0x25DF)
WR = {}
seq = []
for x in draw:
    if x.mnemonic == "call" and x.op_str.startswith("0x"):
        t = int(x.op_str, 16)
        if 0x17F0B0 <= t <= 0x17F260 and t not in (0x17F0D0, 0x17F100):
            if t not in WR: WR[t] = wslot(t)
            if WR[t] is not None: seq.append((x.address, WR[t]))
order = [s for _, s in seq]
EXP = [11, 1, 1, 8, 9, 21, 22, 23, 24, 15, 26, 12, 17, 6, 16]
check("O1 the draw reaches the object's slots in this address order", order == EXP, repr(order))
calls = [a for a, _ in seq]
lo, hi = calls[0], calls[-1]
bad = []
for x in draw:
    if x.mnemonic.startswith("j") and x.op_str.startswith("0x"):
        t = int(x.op_str, 16)
        if t < x.address and any(t < c < x.address for c in calls) and sum(1 for c in calls if t <= c < x.address) >= 1 \
           and any(t <= c for c in calls) and [c for c in calls if t <= c <= x.address]:
            span = [c for c in calls if t <= c <= x.address]
            if len(span) >= 1 and x.address > span[0]: bad.append("%08X->%08X over %d call(s)" % (x.address, t, len(span)))
check("O2 no backward jump re-runs a slot call inside one draw", not bad, repr(bad[:4]))
sub = dis(0x1FA3D0, 0x431)
vc = [(x.address, int(DISP.fullmatch(x.op_str).group(1), 0) // 8) for x in sub
      if x.mnemonic == "call" and DISP.fullmatch(x.op_str) and x.op_str.startswith("qword ptr [r") ]
self_calls = [s for a, s in vc if s in (10, 13, 14, 19, 20)]
recv = any(("mov r14, rcx" == ("%s %s" % (x.mnemonic, x.op_str))) for x in sub[:20])
mask = any(x.mnemonic == "mov" and x.op_str == "ecx, 0x2424" for x in sub)
check("O3 slot 16 calls 14, 19, 20, 10, 13 on this, per element", recv and self_calls == [14, 19, 20, 10, 13] and mask, repr(self_calls))
caller = dis(0x53D780, 0x368)
two = [x.address for x in caller if x.mnemonic == "call" and x.op_str == "0x53ab50"]
check("O4 the draw runs once, or twice when record +8 bit 0 is set", two == [0x53DA5B, 0x53DA94]
      and any(x.mnemonic == "test" and x.op_str == "byte ptr [rbx + 8], 1" for x in caller))
check("O5 sensitivity: bounded to their own bodies, the helper wrappers 0017F190 / 0017F1D0 forward to no slot",
      WR.get(0x17F190) is None and WR.get(0x17F1D0) is None and sum(1 for v in WR.values() if v is not None) == 14,
      repr({"%08X" % k: v for k, v in WR.items()}))
print("FAILS", fails)
sys.exit(1 if fails else 0)
