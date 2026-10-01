"""Reopened page 2 (SWE2-STRUCT for OPUS, 2026-10-01):
22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md

Run: python -B p2_route4.py   (last line FAILS n; must be FAILS 0)
Input, read only: the certified image Tools/work/exe/FFXII_TZA.exe (sha 73461d08...), parsed here directly.

THE FALSIFICATION PASS - section 3b's Route 4 table, the claim the reopening turned on: of the 22 candidate names,
22 are present as bare strings in .rdata / .data, 21 are named as the template argument of a PClassDescriptor*<T>
RTTI symbol, 21 own a PObjectAccessor<class ...T ...>::Get string, 0 are absent by all three, and PContextSwitch is the
one exception (array accessors only). The attack adds what the table did not test: that each descriptor symbol is a
LIVE RTTI type descriptor (its RVA is held by a complete object locator in .rdata), not a stray string.

  C1-C4  controls: PClusterHeaderBase and PLight (recovered classes) pass all three and the COL test; the enum-like
         PLightType (a type-table entry, CL-2's family) and the fabricated PNoSuchClassZZ have no descriptor;
  C5     sensitivity of F6: the same COL-RVA test run on non-RTTI strings (the accessor names) fires on none
  F1-F5  the 22: bare 22/22; descriptor template argument 21/22; own accessor 21/22; absent by all three 0/22;
         the one exception is PContextSwitch on both, and its accessors are PArray<... PContextSwitch const *,8> only
  F6     every one of the 21 has at least one PClassDescriptor*<T> type descriptor referenced by a COL (live RTTI)
  F7     the bare PContextSwitch string sits at VA 00D809C8 (section 3b, CL-2)
  F8     no false merge: a descriptor match for X never comes from a longer name (e.g. PShaderFragmentProgram vs
         PShaderFragmentProgramD3D11) - the template argument is matched between '@V' and '@'
"""
import hashlib, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
EXE = os.path.join(DB, "Tools", "work", "exe", "FFXII_TZA.exe")
BASE = 0x120000
FAILS = 0
N = 0


def check(cid, ok, text, detail=""):
    global FAILS, N
    N += 1
    if not ok:
        FAILS += 1
    print("%s %-4s %s%s" % ("PASS" if ok else "FAIL", cid, text, ("  -- " + detail) if detail else ""))


d = open(EXE, "rb").read()
sha = hashlib.sha256(d).hexdigest()
check("C0", sha.startswith("73461d08") and sha.endswith("d89721f8"), "the image is the certified EXE", sha[:16])
pe = struct.unpack_from("<I", d, 0x3C)[0]
ns = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(ns):
    o = pe + 24 + opt + i * 40
    nm = d[o:o + 8].rstrip(b"\0").decode("latin1")
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((nm, va, vs, ro, rs))


def sec_of(fo):
    for nm, va, vs, ro, rs in secs:
        if ro <= fo < ro + rs:
            return nm
    return None


def rva_of(fo):
    for nm, va, vs, ro, rs in secs:
        if ro <= fo < ro + rs:
            return va + fo - ro
    return None


rdata = [(ro, rs) for nm, va, vs, ro, rs in secs if nm == ".rdata"][0]
# every NUL-delimited printable string in .rdata / .data
strings = []
for nm, va, vs, ro, rs in secs:
    if nm not in (".rdata", ".data"):
        continue
    for m in re.finditer(rb"[\x20-\x7e]{3,}", d[ro:ro + rs]):
        strings.append((ro + m.start(), m.group().decode("latin1")))
# dwords in .rdata, for the COL test (a COL's pTypeDescriptor is an image-relative RVA at COL+0x0C)
rd = d[rdata[0]:rdata[0] + rdata[1]]
dw = set()
for i in range(0, len(rd) - 3, 4):
    dw.add(struct.unpack_from("<I", rd, i)[0])

CANDS = ["PShaderVertexProgram", "PShaderFragmentProgram", "PShaderFragmentProgramD3D11", "PShaderGeometryProgram",
         "PShaderGeometryProgramD3D11", "PShaderComputeProgram", "PShaderProgramBase",
         "PShaderPassParameterLocationTypesBase", "PShaderPassParameterLocationTypesConstantBuffer", "PTexture2DD3D11",
         "PTextureCubeMapD3D11", "PSamplerStateD3D11", "PStreamInputLayoutD3D11", "PDataBlockBufferD3D11",
         "PIndexDataBlockBufferD3D11", "PBase", "PClassDescriptor", "PContextSwitch", "PNodeContext", "PMaterialSet",
         "PMeshSegmentContext", "PMeshInstanceSegmentContext"]


def probe(name):
    bare = [fo for fo, s in strings if name in s]
    desc = [(fo, s) for fo, s in strings if re.search(r"\?\$PClassDescriptor\w*@V" + re.escape(name) + "@", s)]
    acc = [s for fo, s in strings if re.search(r"PObjectAccessor<class (?:\w+::)*" + re.escape(name) + r" (?:const )?[*&]>::Get$", s)]
    live = []
    for fo, s in desc:
        if s.startswith(".?AV"):
            td_rva = rva_of(fo) - 0x10       # the type descriptor's name field is at +0x10
            if td_rva in dw:
                live.append(s)
    return bare, desc, acc, live


res = {n: probe(n) for n in CANDS + ["PClusterHeaderBase", "PLight", "PLightType", "PNoSuchClassZZ"]}
for cid, n in (("C1", "PClusterHeaderBase"), ("C2", "PLight")):
    b, de, a, lv = res[n]
    check(cid, b and de and a and lv, "control %s (a recovered class): bare, descriptor, accessor and a COL-held descriptor" % n,
          "%d %d %d %d" % (len(b), len(de), len(a), len(lv)))
b, de, a, lv = res["PLightType"]
check("C3", b and not de, "control PLightType (a type-table entry): present as a string, no PClassDescriptor*<T> symbol",
      "%d %d" % (len(b), len(de)))
b, de, a, lv = res["PNoSuchClassZZ"]
check("C4", not b and not de and not a, "control PNoSuchClassZZ (fabricated): absent by all three")
bare = [n for n in CANDS if res[n][0] and all(sec_of(fo) in (".rdata", ".data") for fo in res[n][0])]
desc = [n for n in CANDS if res[n][1]]
acc = [n for n in CANDS if res[n][2]]
none = [n for n in CANDS if not (res[n][0] or res[n][1] or res[n][2])]
check("F1", len(CANDS) == 22 and len(bare) == 22, "bare name present in .rdata / .data: 22 / 22", str(len(bare)))
check("F2", len(desc) == 21 and set(CANDS) - set(desc) == {"PContextSwitch"},
      "named as the template argument of PClassDescriptor*<T>: 21 / 22, the exception PContextSwitch",
      str(sorted(set(CANDS) - set(desc))))
check("F3", len(acc) == 21 and set(CANDS) - set(acc) == {"PContextSwitch"},
      "owns a PObjectAccessor<class ... T ...>::Get: 21 / 22, the exception PContextSwitch", str(sorted(set(CANDS) - set(acc))))
check("F4", not none, "absent by all three: 0 / 22", str(none))
pcs = [s for fo, s in strings if "PObjectAccessor<" in s and "PContextSwitch" in s]
check("F5", pcs and all("PArray<class Phyre::PRendering::PContextSwitch const *,8>" in s for s in pcs),
      "PContextSwitch's accessors are all for PArray<class Phyre::PRendering::PContextSwitch const *,8>", "%d strings" % len(pcs))
notlive = [n for n in desc if not res[n][3]]
check("F6", not notlive and len(desc) == 21,
      "each of the 21 has a PClassDescriptor*<T> type descriptor whose RVA a complete object locator in .rdata holds "
      "(live RTTI, not a stray string)", str(notlive))
accfo = [fo for n in desc for fo, s in strings if s in res[n][2]]
falsecol = [fo for fo in accfo if rva_of(fo) - 0x10 in dw]
check("C5", len(accfo) >= 21 and not falsecol,
      "sensitivity control for F6: the same RVA test on the 21 classes' accessor strings (not RTTI) fires on none",
      "%d strings, %d fire" % (len(accfo), len(falsecol)))
fo = d.find(b"\0PContextSwitch\0") + 1
va = rva_of(fo) + BASE if fo > 0 else None
check("F7", va == 0x00D809C8, "the bare PContextSwitch string is at VA 00D809C8", hex(va) if va else "")
over = []
for n in CANDS:
    for fo, s in res[n][1]:
        m = re.search(r"\?\$PClassDescriptor\w*@V([A-Za-z0-9_]+)@", s)
        if not m or m.group(1) != n:
            over.append((n, s))
check("F8", not over, "every descriptor match names exactly that class as its argument (no longer-name merge)", str(over[:2]))
print("CHECKS %d" % N)
print("FAILS %d" % FAILS)
