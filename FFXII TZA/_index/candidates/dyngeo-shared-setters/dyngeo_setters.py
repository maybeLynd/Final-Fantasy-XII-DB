"""DynGeoFontTextSpecial{,Final,Shadow}Instance: +0xF8..+0x15B is written by four setters all three vtables share
(OPUS, 2026-09-27). Control. Static.

All three types carried "+0xD0 unobservedSpan00D0 - nothing read here touches it" (144 / 160 / 152 bytes).
  V1 the three vtables (00906DE8 plain, 00906EB8 Final, 00906E50 Shadow; 12 slots each) share slot 1 (00213FE0),
     slot 3 (00214710) and slots 7 / 8 / 9 (002146F0 / 002148E0 / 00214830), so rcx at those entries is the instance
  V2 the setters: 002146F0 stores rdx at +0xF8; 002148E0 stores rdx at +0x100; 00214830 copies five dwords from [rdx]
     to +0x108..+0x118; 00214710 copies sixteen dwords from [rdx] to +0x11C..+0x158
  V3 slot 1, 00213FE0, reads +0xF8, +0x100 and +0x108..+0x118 back (the field-access index's rows for Final / Shadow)
  V4 STORE REGRESSION: in each type, +0xF8 / +0x100 / +0x108 / +0x11C are declared rows and no unobserved row covers
     +0xD0..+0x15B
  V5 +0xD0 is layer i's fill cursor: slot 6 (00213D10) reads [this + i*4 + 0xD0], compares it with layerCount[i] (+0xA8)
     and increments it - the page's table (dyngeo-instance-family.md, BC-3), which the store had left as unobserved
Not claimed: what +0xF8 / +0x100 / +0x108 hold; each type's bytes after +0x15C (no access found).
"""
import os, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]; DB = HERE.parents[2]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def body(f, size): return ["%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(f):off(f) + size], f)]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

VT = {"DynGeoFontTextSpecialInstance": 0x906DE8, "DynGeoFontTextSpecialFinalInstance": 0x906EB8, "DynGeoFontTextSpecialShadowInstance": 0x906E50}
slots = {t: [struct.unpack_from("<Q", d, off(v) + 8 * i)[0] for i in range(12)] for t, v in VT.items()}
shared = {i: {s[i] for s in slots.values()} for i in (1, 3, 7, 8, 9)}
check("V1 the three vtables share slots 1 / 3 / 7 / 8 / 9",
      shared == {1: {0x213FE0}, 3: {0x214710}, 7: {0x2146F0}, 8: {0x2148E0}, 9: {0x214830}}, str({i: sorted("%08X" % x for x in v) for i, v in shared.items()}))
s7, s8, s9, s3 = body(0x2146F0, 8), body(0x2148E0, 8), body(0x214830, 45), body(0x214710, 144)
dst9 = [int(m, 16) for x in s9 for m in re.findall(r"^mov dword ptr \[rcx \+ (0x[0-9a-f]+)\], eax$", x)]
dst3 = [int(m, 16) for x in s3 for m in re.findall(r"^mov dword ptr \[rcx \+ (0x[0-9a-f]+)\], eax$", x)]
check("V2 the setters: +0xF8 / +0x100 qwords, five dwords to +0x108, sixteen to +0x11C",
      s7[0] == "mov qword ptr [rcx + 0xf8], rdx" and s8[0] == "mov qword ptr [rcx + 0x100], rdx"
      and dst9 == [0x108 + 4 * i for i in range(5)] and dst3 == [0x11C + 4 * i for i in range(16)],
      "%d / %d dwords" % (len(dst9), len(dst3)))
r1 = body(0x213FE0, 0x200)
check("V3 slot 1 (00213FE0) reads +0xF8, +0x100 and +0x108..+0x118",
      all(any("[rcx + %s]" % hex(o) in x or "+ %s]" % hex(o) in x for x in r1) for o in (0xF8, 0x100, 0x108, 0x118)))
rows = {}
for l in open(os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] in VT: rows.setdefault(c[0], []).append((int(c[1], 16), int(c[2]), c[3]))
bad = {t: [r for r in rs if r[2].lower().startswith("unobserved") and r[0] < 0x15C and r[0] + r[1] > 0xD0] + [o for o in (0xF8, 0x100, 0x108, 0x11C) if o not in [r[0] for r in rs]]
       for t, rs in rows.items()}
check("V4 STORE REGRESSION: the four setter targets are rows in each type, and no unobserved row covers +0xF8..+0x15B",
      len(rows) == 3 and not any(bad.values()), str({t: v for t, v in bad.items() if v}))
s6 = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x213D10):off(0x213D10) + 0x120], 0x213D10)}
check("V5 +0xD0 is layer i's fill cursor (read, compared with +0xA8, incremented by slot 6)",
      s6.get(0x213D9F) == "movsxd rax, dword ptr [rdi + rsi*4 + 0xd0]" and s6.get(0x213DAC) == "cmp eax, dword ptr [rdi + rsi*4 + 0xa8]"
      and s6.get(0x213E0A) == "inc dword ptr [rdi + rsi*4 + 0xd0]")
print("FAILS", fails)
sys.exit(1 if fails else 0)
