"""bg56_gi_bodies.py - BG-5 and BG-6: the six shape-A Gi command bodies against the D3D11 primitive renderer, and
what device slot 0 really does (FABLE, Claude Opus 5.5, 2026-09-26; read line by line by a delegated read-only pass,
anchors re-checked here).

  D1 the device: vtable 00D86960 is PrimitiveRendererD3D11 by RTTI. Its slots are 0 = 006CA760, 1 = 006CB5E0,
     4 (+0x20) = 006C8C50, 6 (+0x30) = 006CAF40, 8 (+0x40) = 006CAEB0, 11 (+0x58) = 006CAD90, 15 (+0x78) = 006CAB80,
     19 (+0x98) = 006CAB40, 20/21 (+0xA0/+0xA8) = 006CABF0 / 006CAC00, 37 (+0x128) = 006C9B00 and
     39 (+0x138) = 006C9AF0. Slots 16 and 17 (+0x80 / +0x88) are both 0060D760 = `mov eax, 0x17; ret`, a constant stub.
  D2 (BG-6) slot 0 reserves nothing. 006CA760 overwrites rdx (the count) before reading it (006CA766), returns
     this + 0x10880 + idx*0x7FE0, zeroes the index (006CA774) and publishes the pointer at +0xB8 (006CA781).
     Image-wide, the index cell +0x18860 is touched only by those two instructions, so idx is always 0. The staging
     area is 0x7FE0 bytes, 682 vertices of 0x30. The count goes to slot 4, whose batcher compares pending + count
     with 0x2AA = 682 and flushes (006DA600, 006DA609).
  D3 (BG-5) each body's class is the RTTI of the vtable that holds it at slot 1. The draws are:
     - GiSprite (00864330), GiColorRect (00863850) and GiScreenImage (0020E6C0) each call slot 4 once with 4 vertices
       (008646D9/008646E9, 00863AFA/00863B0A, 0020E9B4/0020E9C4);
     - GiPrim (00863D80) draws [r14+0x60] vertices (00864142);
     - GiNormal (008651A0) makes no slot-4 call: it draws nothing.
  D4 GiSprite scales V by the constant at 009068D0 = 1.142857 (8/7, 512/448).
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
funcs = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def q(v): return struct.unpack_from("<Q", d, off(v))[0]
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); return "%s %s" % (x.mnemonic, x.op_str)
def body(f): return list(cs.disasm(d[off(f):off(f) + funcs[f]], f))
def rtti(vt):
    col = q(vt - 8); o = off(col)
    if o is None: return ""
    td = BASE + struct.unpack_from("<IIII", d, o)[3]; t = off(td + 16)
    return d[t:d.find(b"\0", t)].decode("latin-1") if t else ""
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
VT = 0xD86960
SL = {0: 0x6CA760, 1: 0x6CB5E0, 4: 0x6C8C50, 6: 0x6CAF40, 8: 0x6CAEB0, 11: 0x6CAD90, 15: 0x6CAB80, 16: 0x60D760,
      17: 0x60D760, 19: 0x6CAB40, 20: 0x6CABF0, 21: 0x6CAC00, 37: 0x6C9B00, 39: 0x6C9AF0}
check("D1 PrimitiveRendererD3D11's slots; +0x80 and +0x88 are the constant stub mov eax, 0x17; ret",
      rtti(VT) == ".?AVPrimitiveRendererD3D11@@" and all(q(VT + 8 * k) == v for k, v in SL.items())
      and at(0x60D760) == "mov eax, 0x17" and at(0x60D765).strip() == "ret", rtti(VT))
vs, va, rs, ro = secs[0]
cs2 = Cs(CS_ARCH_X86, CS_MODE_64); cs2.skipdata = True
cell = [x.address for x in cs2.disasm(d[ro:ro + rs], BASE + va) if "+ 0x18860]" in x.op_str]
check("D2 slot 0 overwrites the count, returns the fixed staging area and publishes it; +0x18860 is touched only there; "
      "the batcher bounds at 0x2AA = 682 = 0x7FE0 / 0x30",
      at(0x6CA760) == "mov eax, dword ptr [rcx + 0x18860]" and at(0x6CA766) == "imul rdx, rax, 0x7fe0"
      and at(0x6CA774) == "mov dword ptr [rcx + 0x18860], 0" and at(0x6CA781) == "mov qword ptr [rcx + 0xb8], rax"
      and sorted(cell) == [0x6CA760, 0x6CA774] and at(0x6DA609) == "cmp eax, 0x2aa" and 0x7FE0 // 0x30 == 0x2AA == 682,
      "image-wide +0x18860 sites %s" % ["%08X" % a for a in cell])
GI = {"GiSprite": 0x864330, "GiColorRect": 0x863850, "GiScreenImage": 0x20E6C0, "GiPrim": 0x863D80, "GiNormal": 0x8651A0, "GiBeginEff": 0x864E90}
def owner(b):
    """the RTTI name of every vtable holding b at slot 1 (search .rdata for the qword)."""
    names = set(); pat = struct.pack("<Q", b); k = d.find(pat)
    while k != -1:
        for vs_, va_, rs_, ro_ in secs:
            if ro_ <= k < ro_ + rs_:
                vt = BASE + va_ + (k - ro_) - 8
                if off(vt - 8) is not None: names.add(rtti(vt))
        k = d.find(pat, k + 1)
    return names
own = {c: owner(b) for c, b in GI.items()}
check("D3 each body is slot 1 of its class's vtable", all(any(c in nm for nm in own[c]) for c in GI), str({c: sorted(v) for c, v in own.items()}))
draws = {c: [x.address for x in body(b) if x.mnemonic == "call" and x.op_str.endswith("+ 0x20]")] for c, b in GI.items() if b in funcs}
check("D3 draws: Sprite/ColorRect/ScreenImage one 4-vertex slot-4 call each, GiPrim [r14+0x60] vertices, GiNormal none",
      draws.get("GiSprite") == [0x8646E9] and at(0x8646D9) == "mov r9d, 4" and draws.get("GiColorRect") == [0x863B0A]
      and at(0x863AFA) == "mov r9d, 4" and draws.get("GiScreenImage") == [0x20E9C4] and at(0x20E9B4) == "mov r9d, 4"
      and at(0x864142) == "mov r9d, dword ptr [r14 + 0x60]" and draws.get("GiNormal") == [],
      str({c: ["%08X" % a for a in v] for c, v in draws.items()}))
uses = [x.address for x in body(0x864330) if "rip" in x.op_str and re.search(r"rip \+ (0x[0-9a-f]+)", x.op_str)
        and x.address + x.size + int(re.search(r"rip \+ (0x[0-9a-f]+)", x.op_str).group(1), 16) == 0x9068D0]
check("D4 GiSprite reads the 8/7 V-scale constant 009068D0 = 1.142857",
      abs(struct.unpack_from("<f", d, off(0x9068D0))[0] - 8 / 7) < 1e-6 and len(uses) >= 1, "%d reads" % len(uses))
fl = {c: [x.address for x in body(b) if x.mnemonic in ("call", "jmp") and x.op_str.endswith("+ 0x128]")] for c, b in GI.items() if b in funcs}
check("D5 slot +0x128 (006C9B00) is called by GiSprite and GiPrim as well, so it is not only the end-scene bracket",
      q(VT + 8 * 37) == 0x6C9B00 and fl.get("GiSprite") and fl.get("GiPrim"), str({c: ["%08X" % a for a in v] for c, v in fl.items() if v}))
print("FAILS", fails)
sys.exit(1 if fails else 0)
