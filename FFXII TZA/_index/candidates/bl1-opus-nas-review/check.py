"""BL-1 NO ADMISSIBLE SOURCE review (OPUS, reviewer, 2026-09-26): the places a shipped name for attribute bits 3-4 could
still be, beyond FABLE's nas-label-scans/bl1_attribute_names.py (which searches 'attrib' strings and the .phyre pools).
  R1 the image's flag vocabulary. Every NUL-terminated string (ASCII or UTF-16) matching a wide flag-word pattern
     (serialize, transient, editable, readonly, persist, hidden, export, MEMBER_, PHYRE_, flag, pointer, array, attrib...)
     is classified. None is a member-attribute flag name. Control: the pattern sees m_isPersistent, a reflection member.
  R2 the member-descriptor class names. The image names its descriptor classes in RTTI (PClassDataMember, ...Array,
     ...Dynamic, ...Enum, ...). All 682 direct registrations go through 00632960, which installs PClassDataMember's
     vtable 00D580B0; the 165 array registrations and the one dynamic one are subclass constructors (00632A10 /
     00632B30) that call it and install their own. The 0x00 / 0x08 / 0x10 split is inside the one plain class, so no
     class name can be a name for it.
  R3 the annotation keys. Members carry named annotations (BL-5). The key constructor 006B66F0 has one caller, which
     passes "WriteMask", and the annotation attach 006B67D0 has 70 callers (BL-5's 70 WriteMask annotations). No
     annotation key names anything else.
  R4 the rest of the shipped data. None of the non-.phyre files in the full extract contains m_parameterStart,
     m_asset or m_innerConeAngle, so no shipped text or header describes the reflection schema.
     Control: the same needles are found in the .phyre files (first 400 checked until one hits).
Prints PASS/FAIL per check; exit 1 on any FAIL. Argument: the extract root (default D:/FFXII_TZA_extract).
"""
import os, re, struct, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
EXE = ROOT / "Database/Tools/work/exe/FFXII_TZA.exe"
EXTRACT = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract")
import pefile
img = pefile.PE(str(EXE), fast_load=True).get_memory_mapped_image(); IB = 0x120000
raw = EXE.read_bytes()
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
def callers(tgt):
    out = []
    for m in re.finditer(rb"\xE8", img[0x1000:0x8C0000 - IB]):
        o = m.start() + 0x1000
        if o + IB + 5 + struct.unpack_from("<i", img, o + 1)[0] == tgt: out.append(o + IB)
    return out
def cstr(a):
    o = a - IB; e = img.find(b"\0", o, o + 200)
    return img[o:e].decode("latin-1") if 0 <= o and e > o else None
# ---- R1
strs = {m.group(1).decode() for m in re.finditer(rb"([\x20-\x7e]{3,160})\x00", raw)}
strs |= {m.group(1).decode("utf-16le") for m in re.finditer(rb"((?:[\x20-\x7e]\x00){3,160})\x00\x00", raw)}
PAT = re.compile(r"serializ|transient|editable|readonly|read_only|nosave|no_save|persist|hidden|export|MEMBER_|_MEMBER|"
                 r"PHYRE_|CLASS_FLAG|FIELD_FLAG|memberflag|attrflag|ispointer|isarray|pointerto|arrayof|attrib", re.I)
KNOWN = {
    "%s NOT EDITABLE": "debug-menu label", "Serialization": "namespace name", "phyre_pscript": "module name",
    "GetFileAttributesW": "Win32 import", "SetFileAttributesW": "Win32 import",
    "setOrthoAttributesFromAnimation": "script-accessor method name",
    "Type::putPointerToScriptContext: Not implemented for '%s' type": "script error message",
}
def cls(s):
    if s in KNOWN: return KNOWN[s]
    if s.startswith(".?A"): return "RTTI type name"
    if s.startswith("m_"): return "reflection member name"
    if s.startswith("UserAttribute"): return "animation-binding target name"
    if "PScriptAccessors" in s or s.startswith("Phyre::"): return "script accessor / qualified type name"
    if "\\" in s or "/" in s: return "path"
    if s.startswith("%s%s:%d(") and "NOT EDITABLE" in s: return "debug-menu help line"
    if re.fullmatch(r"P?[A-Z][A-Za-z0-9]*(<.*>)?", s): return "class name"
    return None
hits = sorted(s for s in strs if PAT.search(s))
unk = [s for s in hits if cls(s) is None]
for s in hits: print("   %-90s %s" % (s[:90], cls(s)))
check("R1 every flag-vocabulary string in the image is classified, none a member-attribute flag name",
      hits and not unk, "%d of %d strings; unclassified %s" % (len(hits), len(strs), unk[:8]))
check("R1 control: the pattern sees the reflection member m_isPersistent", "m_isPersistent" in hits)
# ---- R2
def vt_rtti(vt):
    col = struct.unpack_from("<Q", img, vt - 8 - IB)[0]
    return cstr(IB + struct.unpack_from("<I", img, col + 12 - IB)[0] + 0x10)
def installs(fn, vt, span=0xB0):
    for o in range(fn - IB, fn - IB + span):
        if img[o] in (0x48, 0x4C) and img[o + 1] == 0x8D and (img[o + 2] & 0xC7) == 0x05 and \
           o + IB + 7 + struct.unpack_from("<i", img, o + 3)[0] == vt: return True
    return False
n_plain, n_arr, n_dyn = len(callers(0x632960)), len(callers(0x632A10)), len(callers(0x632B30))
r = {"00D580B0": vt_rtti(0xD580B0), "00D58100": vt_rtti(0xD58100), "00D58358": vt_rtti(0xD58358)}
print("   registrar calls: 00632960 %d, 00632A10 %d, 00632B30 %d; vtables %s" % (n_plain, n_arr, n_dyn, r))
check("R2 all direct registrations build one class (00632960 installs PClassDataMember 00D580B0)",
      n_plain == 682 and installs(0x632960, 0xD580B0) and r["00D580B0"] == ".?AVPClassDataMember@Phyre@@")
check("R2 the subclass constructors are the array and dynamic ones, and each calls 00632960",
      r["00D58100"] == ".?AVPClassDataMemberArray@Phyre@@" and r["00D58358"] == ".?AVPClassDataMemberDynamic@Phyre@@"
      and 0x632A41 in callers(0x632960) and 0x632B89 in callers(0x632960), "arrays %d, dynamic %d" % (n_arr, n_dyn))
# ---- R3
kc = callers(0x6B66F0)
names = []
for c in kc:
    blob = img[c - IB - 48:c - IB]
    for o in range(len(blob) - 7):
        if blob[o] in (0x48, 0x4C) and blob[o + 1] == 0x8D and (blob[o + 2] & 0xC7) == 0x05:
            s = cstr(c - 48 + o + 7 + struct.unpack_from("<i", blob, o + 3)[0])
            if s and len(s) > 2 and s.isprintable(): names.append(s)
na = len(callers(0x6B67D0))
check("R3 the only annotation key built is WriteMask, and 70 annotations are attached",
      len(kc) == 1 and names == ["WriteMask"] and na == 70, "key callers %s names %s attaches %d" % (["%08X" % c for c in kc], names, na))
# ---- R4
if not EXTRACT.exists():
    check("R4 extract present", False, str(EXTRACT)); print("FAILS", fails); sys.exit(1)
NEED = [b"m_parameterStart", b"m_asset\x00", b"m_innerConeAngle"]
nfiles = 0; found = {}; ctrl = False; nphy = 0
for dp, dn, fn in os.walk(EXTRACT):
    for f in fn:
        p = os.path.join(dp, f)
        if f.lower().endswith(".phyre"):
            if not ctrl and nphy < 400:
                nphy += 1
                b = open(p, "rb").read(); ctrl = any(n in b for n in NEED)
            continue
        try:
            with open(p, "rb") as fh:                  # streamed with an overlap, so large videos are read too
                tail = b""
                while True:
                    blk = fh.read(16 << 20)
                    if not blk: break
                    b = tail + blk
                    hit = next((n for n in NEED if n in b), None)
                    if hit: found[p] = hit.decode(errors="replace"); break
                    tail = b[-32:]
        except OSError:
            found.setdefault("(unreadable)", p); continue
        nfiles += 1
print("   non-.phyre files read %d" % nfiles)
check("R4 no non-.phyre shipped file names a reflection member", nfiles > 0 and not found, str(list(found.items())[:5]))
check("R4 control: the needles are found in a .phyre file", ctrl, "after %d .phyre files" % nphy)
print("FAILS", fails)
sys.exit(1 if fails else 0)
