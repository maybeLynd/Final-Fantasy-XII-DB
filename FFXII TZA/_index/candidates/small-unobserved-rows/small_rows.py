"""Six small 'unobserved' rows the field-access index contradicts, each re-cut from the accessing instructions
(OPUS, 2026-09-27). Control. Static.
  S1 RECEIVER CHECK, per hit: in the accessing function, the hit's base register also addresses an already-named row
     of the same type, and no instruction between the two writes that register - so the hit is on the same object
  S2 WIDTH / KIND, per new field: the accessing instructions' width (and float or integer) are the new row's
  S3 STORE REGRESSION: none of the re-cut offsets is still covered by an 'unobserved' row
Rows whose hits reach the type through a nested base are NOT in this batch (they need reading, not re-cutting), nor are
MapRefFieldRow +0x4 and OrderedCommandList +0x29, whose hits S1 could not tie to the type (a receiver check failed).
Not claimed: any meaning.
"""
import os, re, struct, sys, bisect, collections
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
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
# (type, old offset, old size) -> the new fields: (offset, size, kind) with kind 'f' float, 'd' double, 'i' integer
PLAN = {
 ("AudioParameterRamp", 0x28, 8): [(0x28, 4, "f"), (0x2C, 4, "f")],
 ("GlyphRunWidget1498", 0xF4, 4): [(0xF4, 2, "i")],
 ("GlyphRunWidget1498", 0x103, 1): [(0x103, 1, "i")],
 ("PApplication", 0x50, 8): [(0x50, 8, "d")],
 ("Widget0209CC18", 0x14C, 4): [(0x14C, 4, "i")],
 ("WidgetSingleton02CA99C0", 0x39B, 100): [(0x39B, 1, "i")],
}
FIELDS = os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv"
rows = collections.defaultdict(list)
for l in open(FIELDS, encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] != "type":
        try: rows[c[0]].append((int(c[1], 16), int(c[2], 0), c[3]))
        except ValueError: pass
hits = collections.defaultdict(list)
for l in open(DB / "_types/field-access-index.tsv", encoding="utf-8"):
    c = l.rstrip("\n").split("\t")
    if len(c) > 6 and c[0] != "type" and c[2] == "0x0" and c[3] != "addr":
        hits[c[0]].append((int(c[1], 16), int(c[4], 16), int(c[5], 16), c[6]))
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8}
bad1, bad2 = [], []
for (t, o, n), new in PLAN.items():
    named = [(ro, rs) for ro, rs, nm in rows[t] if not nm.lower().startswith("unobserved")]
    for no, ns, kind in new:
        hs = [h for h in hits[t] if h[0] == no]
        if not hs: bad2.append((t, hex(no), "no hit")); continue
        for _, f, s, text in hs:
            xs = list(cs.disasm(d[off(f):off(f) + sizes[f]], f)); i = next(k for k, x in enumerate(xs) if x.address == s)
            m = re.search(r"(byte|word|dword|qword) ptr \[(r\w+)(?: \+ (?:0x[0-9a-f]+|\d+))?\]", text)
            if not m or W[m.group(1)] != ns: bad2.append((t, hex(no), text)); continue
            fl = bool(re.match(r"(movss|mulss|addss|subss|divss|comiss|ucomiss)", xs[i].mnemonic)); db = bool(re.match(r"(movsd|subsd|addsd|mulsd|comisd)", xs[i].mnemonic))
            if kind == "f" and not fl or kind == "d" and not (db or xs[i].mnemonic == "mov"): bad2.append((t, hex(no), text))
            reg = m.group(2); ok = False
            for j in list(range(i - 1, -1, -1)) + list(range(i + 1, len(xs))):
                y = xs[j]
                mm = re.search(r"ptr \[%s(?: \+ (0x[0-9a-f]+|\d+))?\]" % reg, y.op_str)
                if mm:
                    dd = int(mm.group(1), 0) if mm.group(1) else 0
                    if any(ro <= dd < ro + rs for ro, rs in named) and not (o <= dd < o + n):
                        rng = range(min(i, j) + 1, max(i, j))
                        if not any(xs[k].op_str.split(",")[0].strip() in (reg, "e" + reg[1:]) and xs[k].mnemonic not in ("cmp", "test", "push") for k in rng):
                            ok = True; break
            if not ok: bad1.append((t, hex(no), "%08X" % s))
check("S1 every hit's base register also addresses a named row of the same type, unclobbered in between", not bad1, str(bad1))
check("S2 each new field's width and float / integer kind are the accessing instructions'", not bad2, str(bad2))
stale = [(t, hex(no)) for (t, o, n), new in PLAN.items() for no, ns, k in new
         if any(ro <= no < ro + rs and nm.lower().startswith("unobserved") for ro, rs, nm in rows[t])]
check("S3 STORE REGRESSION: no re-cut offset is still inside an unobserved row", not stale, str(stale))
print("FAILS", fails)
sys.exit(1 if fails else 0)
