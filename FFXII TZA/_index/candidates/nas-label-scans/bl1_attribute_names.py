"""bl1_attribute_names.py - BL-1 (what reflection attribute bits 3-4 mean): the named scan for attribute-name strings
that OPUS asked for before ruling on NO ADMISSIBLE SOURCE (504252efa, 2026-09-26). FABLE, Claude Opus 5.5, 2026-09-26.

The residue is a tool's name for a bit. Nothing reads bits 3-4 at run time, and the file persists them (18,934 of 19,301
joins, BL-1's own narrowing). A name could still ship in two places, so this scan checks both.
  S1 the image. Every NUL-terminated string, ASCII or UTF-16, containing "attrib" in any case, is listed and
     classified. None names a member-attribute flag.
     Control: the image's reflection vocabulary is visible to the same scan. The member names m_asset,
     m_parameterStart and m_parameterCount, whose attribute words BL-1 measured, are found.
  S2 the shipped schema. Every .phyre file's packed namespace (header +4: namespace offset and size) holds a string
     pool. Every string in every distinct pool is referenced by one of three fields: a class record's name (w2), a
     member record's name (w0), or the namespace's leading type table. So the pool is exactly class, member and type
     names, and there is no string an attribute bit could be named by. The attribute word itself is a bare integer
     (member w4).
     Control: the same parse finds the three member names above, and the pool count is printed.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import os, re, struct, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
EXTRACT = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract")
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
# ---- S1
asc = {m.group(1).decode() for m in re.finditer(rb"([\x20-\x7e]{4,120})\x00", d) if re.search(rb"attrib", m.group(1), re.I)}
u16 = {m.group(1).decode("utf-16le") for m in re.finditer(rb"((?:[\x20-\x7e]\x00){4,120})\x00\x00", d)
       if re.search("attrib", m.group(1).decode("utf-16le"), re.I)}
KNOWN = {  # string -> what it is
 "GetFileAttributesW": "Win32 import", "SetFileAttributesW": "Win32 import",
 "UserAttributeBool": "animation-binding target name (beside MorphTargetWeight)", "UserAttributeFloat": "animation-binding target name (beside MorphTargetWeight)",
 "UserAttributeInt": "animation-binding target name (beside MorphTargetWeight)", "UserAttributeVector": "animation-binding target name (beside MorphTargetWeight)",
 ".?AVIGPUInputAttribute@PPFX@@": "RTTI class name (vertex input attribute)",
 "setOrthoAttributesFromAnimation": "script-accessor method name",
}
found = sorted(asc | u16)
unknown = [s for s in found if s not in KNOWN and not s.endswith("attribute_data.bin")]
for s in found: print("   %-70s %s" % (s[:70], KNOWN.get(s, "manifest path" if s.endswith("attribute_data.bin") else "?")))
check("S1 every 'attrib' string in the image is classified, and none names a member-attribute flag",
      unknown == [] and len(found) >= 10, "%d strings (%d UTF-16); unclassified %s" % (len(found), len(u16), unknown))
CTRL = [b"m_asset\x00", b"m_parameterStart\x00", b"m_parameterCount\x00"]
check("S1 control: the reflection member names BL-1 measured are in the image", all(c in d for c in CTRL))
# ---- S2
if not EXTRACT.exists():
    check("S2 extract present", False, str(EXTRACT)); print("FAILS", fails); sys.exit(1)
files = [p for p in EXTRACT.rglob("*") if p.suffix.lower() == ".phyre"]
seen = set(); nstr = nref = 0; unref = {}; hit = set(); bad = 0
for p in files:
    with open(p, "rb") as f:
        h = f.read(12)
        if len(h) < 12: bad += 1; continue
        hs, ns = struct.unpack_from("<II", h, 4)
        f.seek(hs); b = f.read(ns)
    if len(b) < 0x20: bad += 1; continue
    A, nC, nM, sp = struct.unpack_from("<IIII", b, 8)
    base = 0x20 + 4 * A; mb = base + 36 * nC; pool = mb + 24 * nM
    P = b[pool:pool + sp]
    if len(P) != sp or P in seen: continue
    seen.add(P)
    starts = {0} | {i + 1 for i in range(len(P) - 1) if P[i] == 0}
    ref = set(struct.unpack_from("<%dI" % A, b, 0x20))
    ref |= {struct.unpack_from("<9I", b, base + 36 * k)[2] for k in range(nC)}
    ref |= {struct.unpack_from("<6I", b, mb + 24 * q)[0] for q in range(nM)}
    nstr += len(starts); nref += len(starts & ref)
    for s0 in starts - ref: unref.setdefault(P[s0:P.find(b"\0", s0)].decode("latin-1"), p.name)
    for c in CTRL:
        if c in P: hit.add(c)
print("   .phyre files %d, unparsed %d, distinct namespace pools %d, strings %d" % (len(files), bad, len(seen), nstr))
check("S2 every string of every distinct pool is a class, member or type name", nstr > 0 and unref == {},
      "referenced %d of %d; unreferenced e.g. %s" % (nref, nstr, list(unref.items())[:5]))
check("S2 control: the parse sees the three member names", hit == set(CTRL), str(sorted(x.decode() for x in hit)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
