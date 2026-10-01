"""L-13: the writers of the tick stamp, the transition clock and bank 1, and the bank-1 capture asymmetry (OPUS, 2026-09-27).
Static; complements FABLE's static answer pending ASTRA's review (FABLE-REQ-ASTRA-L13-BANKS).

  K1 the stamp 02089374 has exactly two writers image-wide (RIP-relative census): the area-transition rotation
     SpawnKeep_RotatePersistenceBanksForAreaTransition 00233780 (00233A03) and BattleSystem_ResetRuntimeState 00237DF0
     (00237E53, 0)
  K2 the clock 0208D45C has exactly two writers: an increment in 0032A100 (0032A135; its caller is
     BattleSystem_RunFieldFrameOrchestrator) and a zero store in 0032A160 (0032A160; its caller is 00237DF0)
  K3 no function on the load / restore path (005843E0, 00233550, 00233C10, 00285E60, 0027F2E0, 00255260, 00238A80)
     references the bank-1 pointer 0208E690
  K4 THE ASYMMETRY: SpawnKeep_SerializePersistenceBanks 00233440 (called by both captures, 00229B40 and 00584580) copies
     bank 2 ([0208E698]) to snapshot +0x10 AND bank 1 ([0208E690]) to snapshot +0x10010, with the field-id pair at
     +0 / +2; the restore 00233550 reads only +0x10 into bank 2 and the pair - bank 1 is captured and never read back
Not claimed: the dynamic order of the load path; what any other reader of the snapshot does with +0x10010.
"""
import re, struct, sys, bisect, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 36)[0],) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for ch, vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
keys = sorted(sizes)
def owner(v):
    k = bisect.bisect_right(keys, v) - 1
    return keys[k] if k >= 0 and v < keys[k] + sizes[keys[k]] else None
cs = Cs(CS_ARCH_X86, CS_MODE_64)
_c = {}
def D(f):
    if f not in _c: _c[f] = list(cs.disasm(d[off(f):off(f) + sizes[f]], f))
    return _c[f]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

def rip_refs(target):
    out = []
    for f in {owner(BASE + va + p - ro) for ch, vs, va, rs, ro in SECS if ch & 0x20000000
              for p in range(ro, ro + rs - 4) if BASE + va + p - ro + 4 + struct.unpack_from("<i", d, p)[0] - target in (0, -1, -2, -4)} - {None}:
        for x in D(f):
            m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
            if m and x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) == target:
                write = x.op_str.startswith(("dword ptr [rip", "word ptr [rip", "byte ptr [rip", "qword ptr [rip")) and x.mnemonic in ("mov", "inc", "dec", "add", "sub", "and", "or", "xor")
                out.append((f, x.address, write, "%s %s" % (x.mnemonic, x.op_str)))
    return out
st = rip_refs(0x2089374); ck = rip_refs(0x208D45C)
check("K1 the stamp's writers are the rotation (00233A03) and the reset (00237E53) only",
      sorted((f, a) for f, a, w, s in st if w) == [(0x233780, 0x233A03), (0x237DF0, 0x237E53)], str([(hex(f), hex(a)) for f, a, w, s in st if w]))
check("K2 the clock's writers are the frame increment (0032A135) and the reset's zero store (0032A160) only",
      sorted((f, a) for f, a, w, s in ck if w) == [(0x32A100, 0x32A135), (0x32A160, 0x32A160)], str([(hex(f), hex(a)) for f, a, w, s in ck if w]))
b1 = {f for f, a, w, s in rip_refs(0x208E690)}
LOAD = {0x5843E0, 0x233550, 0x233C10, 0x285E60, 0x27F2E0, 0x255260, 0x238A80}
check("K3 no load / restore function references the bank-1 pointer (%d referencing functions)" % len(b1), len(b1) >= 15 and not (b1 & LOAD))
S = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(0x233440)}
R = D(0x233550); Rt = " | ".join("%s %s" % (x.mnemonic, x.op_str) for x in R)
check("K4 capture copies bank 2 -> +0x10 and bank 1 -> +0x10010; restore reads only +0x10 (bank 2) and the pair",
      S.get(0x233468) == "lea rdx, [rbx + 0x10]" and S.get(0x2334CF) == "lea rcx, [rbx + 0x10010]"
      and "0x1e5b1c6" in S.get(0x2334C3, "") and "0x1e5b23b" in S.get(0x233456, "")
      and "lea rdx, [rcx + 0x10]" in Rt and "0x10010" not in Rt and 0x233550 not in b1)
print("FAILS", fails)
sys.exit(1 if fails else 0)
