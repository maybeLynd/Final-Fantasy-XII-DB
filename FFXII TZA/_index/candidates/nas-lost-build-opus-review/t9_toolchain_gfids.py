"""T-9 review (OPUS, reviewer of NO ADMISSIBLE SOURCE package 2, 2026-09-26): is the source of the twelve .gfids dwords
really a lost build?
  T1 the image's twelve .gfids dwords, VirtualSize 0x30, and a file with no COFF symbol table (reproduces the row).
  T2 the image's Rich header records the toolset: linker 14.0, the game's own code at compiler build 24215 (VS2015
     Update 3), and prebuilt objects at builds 24123, 24210 and 23026 - the builds of the VS2015 static runtime
     libraries, which the link pulled in.
  T3 the prebuilt runtime is guard-aware. In the installed toolset (whatever version is present) the x64 static
     runtime libraries (libcmt, libvcruntime, libcpmt, libucrt, the legacy_stdio and exe_initialize helpers ...)
     contain objects with a .gfids$y section, and every value in every one is below that object's own NumberOfSymbols:
     they are COFF symbol-table indices, the image's twelve's reading. So in a link made without /guard:cf, the guard-aware objects that contribute .gfids$y
     include the runtime's own - and those ship with the public toolchain, with full symbol tables.
Conclusion for the review: which functions the twelve index is answerable in principle from the VS2015 Update 3 /
Windows 10 SDK static runtime libraries (a public download), so the source is not lost. (That toolset is not installed
here, so this check does not answer T-9; it shows the answer's source exists.)
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import os, re, struct, sys
from pathlib import Path
import pefile
ROOT = Path(__file__).resolve().parents[5]
EXE = ROOT / "Database/Tools/work/exe/FFXII_TZA.exe"
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
pe = pefile.PE(str(EXE), fast_load=True)
# ---- T1
g = [s for s in pe.sections if s.Name.rstrip(b"\0") == b".gfids"]
vals = list(struct.unpack_from("<12I", g[0].get_data(), 0)) if g else []
check("T1 .gfids declares 0x30 bytes = twelve dwords, and the file has no COFF symbol table",
      len(g) == 1 and g[0].Misc_VirtualSize == 0x30 and vals == [49, 48, 19, 10, 13, 16, 69, 113, 10, 98, 55, 11]
      and pe.FILE_HEADER.NumberOfSymbols == 0 and pe.FILE_HEADER.PointerToSymbolTable == 0, str(vals))
# ---- T2
r = pe.parse_rich_header()["values"]
rich = {(r[i] >> 16, r[i] & 0xFFFF): r[i + 1] for i in range(0, len(r), 2)}
builds = sorted({b for (_, b) in rich})
own = sum(c for (p, b), c in rich.items() if b == 24215 and p in (260, 261))
pre = {b: sum(c for (p, bb), c in rich.items() if bb == b and p in (257, 259, 260, 261)) for b in (24123, 24210, 23026)}
print("   Rich builds %s; C/C++ objects at 24215: %d; prebuilt at %s" % (builds, own, pre))
check("T2 linker 14.0; the game's code at 24215 (VS2015 U3); prebuilt objects at 24123 / 24210 / 23026",
      pe.OPTIONAL_HEADER.MajorLinkerVersion == 14 and pe.OPTIONAL_HEADER.MinorLinkerVersion == 0 and own > 900
      and all(v > 0 for v in pre.values()))
# ---- T3
ROOTS = [r"C:\Program Files\Microsoft Visual Studio", r"C:\Program Files (x86)\Microsoft Visual Studio",
         r"C:\Program Files (x86)\Microsoft Visual Studio 14.0", r"C:\Program Files (x86)\Windows Kits\10\Lib"]
RUNTIME = re.compile(r"^(libcmt|libvcruntime|libcpmt|libucrt|legacy_stdio|exe_initialize|iso_stdio|libconcrt)", re.I)
def members(b):
    o = 8; ln = b""
    while o + 60 <= len(b):
        h = b[o:o + 60]; nm = h[:16].decode("latin-1").strip(); size = int(h[48:58].decode().strip() or 0)
        d = b[o + 60:o + 60 + size]
        if nm == "//": ln = d
        elif nm not in ("/", ""): yield d
        o += 60 + size + (size & 1)
def gfids(obj):
    if len(obj) < 20 or struct.unpack_from("<H", obj, 0)[0] != 0x8664: return []
    nsec, opt = struct.unpack_from("<H", obj, 2)[0], struct.unpack_from("<H", obj, 16)[0]
    out = []; nsym = struct.unpack_from("<I", obj, 12)[0]
    for i in range(nsec):
        s = 20 + opt + 40 * i
        if obj[s:s + 8].rstrip(b"\0") == b".gfids$y":
            size, ptr = struct.unpack_from("<II", obj, s + 16)
            out += list(struct.unpack_from("<%dI" % (size // 4), obj, ptr))
    return [(x, nsym) for x in out]
libs = []
for rt in ROOTS:
    for dp, dn, fn in os.walk(rt):
        if os.path.basename(dp).lower() != "x64": continue
        libs += [os.path.join(dp, f) for f in fn if f.lower().endswith(".lib") and RUNTIME.match(f)]
nobj = 0; allv = []; per = {}; below = True
for lp in libs:
    b = open(lp, "rb").read()
    if not b.startswith(b"!<arch>\n"): continue
    for d in members(b):
        v = gfids(d)
        if v:
            nobj += 1; allv += [x for x, _ in v]; below = below and all(x < n for x, n in v); per[os.path.basename(lp)] = per.get(os.path.basename(lp), 0) + 1
print("   runtime libraries scanned %d; objects with .gfids$y %d; by library %s; value range %s" %
      (len(libs), nobj, dict(sorted(per.items())[:12]), (min(allv), max(allv)) if allv else None))
check("T3 the static runtime's own objects carry .gfids$y, and every value is an index into that object's symbol table",
      nobj > 0 and below and any(k.lower().startswith("libcmt") for k in per))
print("FAILS", fails)
sys.exit(1 if fails else 0)
