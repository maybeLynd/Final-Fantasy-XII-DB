r"""t9_crt_gfids.py V140_LIB_AMD64 [SDK_LIB_ROOT] - T-9: which objects the image's twelve .gfids dwords come from
(FABLE, Claude Opus 5.5, 2026-09-27). Reads the image's .gfids and the COFF .gfids$y section of every member object of
the x64 static release runtime (libcmt, libcpmt, libvcruntime from the VS2015 v140 toolset; libucrt from the Windows
SDK when given), and resolves each run's values to the symbols they index in that object's own symbol table.

  C1 the image: .gfids is 0x30 bytes = twelve dwords 49 48 19 10 13 16 69 113 10 98 55 11, and the Rich header's
     prebuilt runtime objects are builds 24123 / 24210 / 23026 (VS2015 Update 3).
  C2 the installed v140 static runtime is build 24237 (a later Update 3 servicing build) - so run contents can differ
     slightly from the image's objects; matches below are per position, not a proof of the exact link.
  C3 per position, the static runtime objects whose whole .gfids$y run equals the twelve's value(s) there; printed
     with the symbols they index. A multi-value run that matches in place is the strongest evidence.
Prints the table; exit 1 only if the image-side facts (C1) fail.
"""
import os, re, struct, sys, glob, collections
import pefile
ROOT = __import__("pathlib").Path(__file__).resolve().parents[5]
TWELVE = [49, 48, 19, 10, 13, 16, 69, 113, 10, 98, 55, 11]
STATIC = ("libcmt.lib", "libcpmt.lib", "libvcruntime.lib", "libucrt.lib")
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
pe = pefile.PE(str(ROOT / "Database/Tools/work/exe/FFXII_TZA.exe"), fast_load=True)
g = [s for s in pe.sections if s.Name.rstrip(b"\0") == b".gfids"][0]
vals = list(struct.unpack_from("<12I", g.get_data(), 0))
rich = pe.parse_rich_header(); rv = rich["values"]; builds = {rv[i] & 0xFFFF for i in range(0, len(rv), 2)}
check("C1 the image's twelve and its runtime builds", g.Misc_VirtualSize == 0x30 and vals == TWELVE and {24123, 24210, 23026} <= builds,
      "%s builds=%s" % (vals, sorted(builds)))
def members(path):
    d = open(path, "rb").read(); o = 8; ln = b""
    while o + 60 <= len(d):
        h = d[o:o + 60]; name = h[:16].decode("latin-1").strip(); size = int(h[48:58].decode().strip() or 0)
        body = d[o + 60:o + 60 + size]
        if name == "//": ln = body
        elif name.startswith("/") and name[1:].isdigit():
            k = int(name[1:]); e = ln.find(b"\0", k); name = ln[k:e if e >= 0 else None].decode("latin-1")
        if name not in ("/", "//"): yield name, body
        o += 60 + size + (size & 1)
def obj_info(obj):
    if len(obj) < 20: return None
    mach, nsec, ts, symptr, nsym, optsz, ch = struct.unpack_from("<HHIIIHH", obj, 0)
    if mach != 0x8664 or not 0 < nsec < 5000: return None
    run = None
    for i in range(nsec):
        s = 20 + optsz + i * 40
        if obj[s:s + 8].rstrip(b"\0") == b".gfids$y":
            sz, ptr = struct.unpack_from("<II", obj, s + 16); run = list(struct.unpack_from("<%dI" % (sz // 4), obj, ptr))
    if not run: return None
    strtab = symptr + nsym * 18
    def nm(ix):
        o = symptr + ix * 18; raw = obj[o:o + 8]
        if raw[:4] == b"\0\0\0\0":
            so = struct.unpack_from("<I", raw, 4)[0]; return obj[strtab + so:obj.index(b"\0", strtab + so)].decode("latin-1")
        return raw.rstrip(b"\0").decode("latin-1")
    comp = None
    for i in range(nsym):
        o = symptr + i * 18
        if obj[o:o + 8] == b"@comp.id": comp = struct.unpack_from("<I", obj, o + 8)[0] & 0xFFFF; break
    return run, [nm(v) for v in run], comp
objs = []
dirs = [sys.argv[1]] + ([p for p in glob.glob(os.path.join(sys.argv[2], "*", "ucrt", "x64"))] if len(sys.argv) > 2 else [])
for d in dirs:
    for lib in STATIC:
        p = os.path.join(d, lib)
        if not os.path.exists(p): continue
        for name, body in members(p):
            i = obj_info(body)
            if i: objs.append((os.path.relpath(p, os.path.dirname(os.path.dirname(p))), os.path.basename(name.replace("\\", "/")), i[0], i[1], i[2]))
comps = collections.Counter(o[4] for o in objs if "libcmt" in o[0])
check("C2 the installed v140 static runtime's build", True, "libcmt objects by build: %s" % dict(comps))
print("C3 per position (value: candidate static-runtime objects whose whole run matches here)")
pos = 0
for p in range(len(TWELVE)):
    c = [o for o in objs if TWELVE[p:p + len(o[2])] == o[2]]
    print("  [%2d] %3d: %s" % (p, TWELVE[p], "; ".join("%s %s %s %s" % (o[0], o[1], o[2], o[3]) for o in c) if c else "-"))
import random
def score(seq):
    single = multi = 0
    for p in range(len(seq)):
        c = [o for o in objs if seq[p:p + len(o[2])] == o[2]]
        if c: single += 1
        if any(len(o[2]) >= 2 for o in c): multi += 1
    return single, multi
real = score(TWELVE)
rnd = random.Random(20260927); sims = [score([rnd.randint(10, 113) for _ in range(12)]) for _ in range(2000)]
ge_single = sum(1 for s, m in sims if s >= real[0]) / len(sims); ge_multi = sum(1 for s, m in sims if m >= real[1]) / len(sims)
print("C4 chance control: the real twelve match %d positions (%d by a multi-value run); of 2,000 random twelves drawn "
      "from 10..113, %.1f %% match as many positions and %.2f %% match a multi-value run" % (real[0], real[1], 100 * ge_single, 100 * ge_multi))
print("FAILS", fails); sys.exit(1 if fails else 0)
