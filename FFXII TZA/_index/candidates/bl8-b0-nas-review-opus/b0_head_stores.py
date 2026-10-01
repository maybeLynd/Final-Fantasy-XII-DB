"""OPUS's reviewer negative for BL-8 +0xB0 (2026-09-27): is a +0xB0 list head's ADDRESS ever saved for a later walk?

FABLE's control (bl8-b0-walkers/bl8_walkers.py) leaves open "a walker built from a head held in memory". A head held in
memory has to be formed first: lea r, [base + 0xB0], then stored. This sweeps every listed body for that shape (the
store within 8 instructions, the head's own self-link stores [r] / [r+8] excluded) and reads the sites in the reflection
band 00590000-006C0000, where the descriptor code lives.

  H1 positive control: the same sweep finds the +0x80 data-member list's link stores in the band (>= 20 sites)
  H2 at +0xB0 the band holds exactly 10 sites in 4 functions: 005CCD00, 00602EA0, 0060B980, 00655690
  H3 none of the four bases is a class descriptor:
       005CCD00 forms [rbp + 0xB0] and 00655690 [rsp + 0xB0] - stack frames;
       0060B980 forms [this + 0xB0] where this comes from 0018E4A0, whose object is read at +0x220 just before the
       call (0018E812) - beyond a descriptor's 0x100 extent;
       00602EA0 forms [this + 0xB0] where its caller stores a call's result at this +0xA0 (005FED52) - a descriptor
       holds a list head there
Not claimed: code outside the listed bodies, or a head formed by other arithmetic.
"""
import struct, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_MEM, CS_OP_REG

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
def body(f):
    o = off(f); return list(cs.disasm(d[o:o + sizes[f]], f)) if o is not None and sizes.get(f, 0) > 0 else []

sites = collections.defaultdict(list)   # D -> [(f, lea address, base register)]
for f in sorted(sizes):
    if not (0x121000 <= f < 0x900000): continue
    o = off(f)
    if o is None or sizes[f] <= 0: continue
    raw = d[o:o + sizes[f]]
    if b"\x80\x00\x00\x00" not in raw and b"\xb0\x00\x00\x00" not in raw: continue
    xs = body(f)
    for i, x in enumerate(xs):
        if x.mnemonic != "lea" or x.operands[1].mem.disp not in (0x80, 0xB0) or not x.operands[1].mem.base or x.operands[1].mem.index:
            continue
        base = x.reg_name(x.operands[1].mem.base)
        if base == "rip": continue
        r = x.reg_name(x.operands[0].reg)
        for y in xs[i + 1:i + 8]:
            if y.mnemonic == "mov" and len(y.operands) == 2 and y.operands[0].type == CS_OP_MEM and y.operands[1].type == CS_OP_REG \
                    and y.reg_name(y.operands[1].reg) == r:
                if y.operands[0].mem.base and y.reg_name(y.operands[0].mem.base) == r: continue
                sites[x.operands[1].mem.disp].append((f, x.address, base)); break
band = lambda D: [s for s in sites[D] if 0x590000 <= s[0] < 0x6C0000]
check("H1 the sweep finds the +0x80 list's link stores in the band", len(band(0x80)) >= 20, "(%d)" % len(band(0x80)))
b0 = band(0xB0)
check("H2 +0xB0: 10 band sites in 4 functions", len(b0) == 10 and sorted({s[0] for s in b0}) == [0x5CCD00, 0x602EA0, 0x60B980, 0x655690],
      "(%d sites: %s)" % (len(b0), " ".join("%08X" % f for f in sorted({s[0] for s in b0}))))
bases = {f: {s[2] for s in b0 if s[0] == f} for f in (0x5CCD00, 0x602EA0, 0x60B980, 0x655690)}
e1 = [x for x in body(0x18E4A0) if 0x18E800 <= x.address <= 0x18E826]
e2 = [x for x in body(0x5FEC80 if 0x5FEC80 in sizes else max(k for k in sizes if k <= 0x5FED8C)) if 0x5FED40 <= x.address <= 0x5FED8C]
ok3 = (bases[0x5CCD00] == {"rbp"} and bases[0x655690] == {"rsp"}
       and any(x.op_str == "eax, dword ptr [rbx + 0x220]" for x in e1) and any(x.op_str == "rcx, rbx" and x.mnemonic == "mov" for x in e1)
       and any(x.op_str == "qword ptr [rbx + 0xa0], rax" for x in e2) and any(x.op_str == "rcx, rbx" for x in e2))
check("H3 none of the four bases is a class descriptor (two stack frames, two non-descriptor receivers)", ok3,
      "(bases %s)" % {("%08X" % k): sorted(v) for k, v in bases.items()})
print("FAILS", fails)
raise SystemExit(1 if fails else 0)
