"""sd64_names.py - where the file schema's "non-class" P-names live (OPUS, 2026-09-30; register SD-64).
Over the 169 extracted .phyre files (D:/FFXII MP Mod/extracted), every NUL-delimited string matching P[A-Z]\\w{2,}
that is neither a runtime class leaf (phyre-field-schema.tsv) nor a name in the file's own namespace pool (types,
classes, members) is placed in the instance list whose byte range holds it. Data layout after the namespace: the
36-byte instance-list headers, then per list its objects (m_objectsSize, +0x0C) followed by its arrays
(m_arraysSize, +0x10). Control C1 confirms that layout on the one file every list class is known in: under it the
PAssetReference arrays hold asset ids ('#') and the PString arrays hold node names.
"""
import collections, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "D:/FFXII MP Mod/extracted"
TSV = os.path.join(HERE, "..", "..", "..", "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata", "phyre-field-schema.tsv")
rt = set()
for l in open(TSV, encoding="utf-8"):
    p = l.rstrip("\r\n").split("\t")
    if p and p[0] and p[0] != "class_leaf":
        rt.add(p[0].split("<")[0])


def parse(d):
    h = struct.unpack_from("<21I", d, 0)
    hsz, nssz, nL = h[1], h[2], h[4]
    ns = d[hsz:hsz + nssz]
    nT, nC, nM, _ = struct.unpack_from("<IIII", ns, 8)
    coff = 0x20 + 4 * nT
    poff = coff + 36 * nC + 24 * nM
    nm = lambda o: ns[poff + o:ns.index(b"\0", poff + o)].decode("latin-1")
    cls = [nm(struct.unpack_from("<9I", ns, coff + 36 * c)[2]) for c in range(nC)]
    pool = set(x.decode("latin-1") for x in ns[poff:].split(b"\0") if x)
    spans, a = [], hsz + nssz + 36 * nL
    for k in range(nL):
        L = struct.unpack_from("<9I", d, hsz + nssz + 36 * k)
        cn = cls[L[0] - 1] if 0 < L[0] <= nC else "?"
        spans.append((cn, a, a + L[3], a + L[3] + L[4]))
        a += L[3] + L[4]
    return hsz + nssz, pool, spans, a


fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


where = collections.defaultdict(collections.Counter)
files, ends_ok, in_pool = 0, 0, 0
ctl = {}
for dp, dn, fn in os.walk(ROOT):
    for f in sorted(fn):
        if not f.lower().endswith(".phyre"):
            continue
        d = open(os.path.join(dp, f), "rb").read()
        nsend, pool, spans, end = parse(d)
        files += 1
        ends_ok += end <= len(d)
        if f == "c1004.dae.phyre":
            for cn, o0, o1, a1 in spans:
                if cn in ("PAssetReference", "PString"):
                    ctl[cn] = [x.decode("latin-1") for x in re.findall(rb"[\x20-\x7e]{4,}", d[o1:a1])][:3]
        for m in re.finditer(rb"(?<=\x00)P[A-Z][A-Za-z0-9_]{2,}(?=\x00)", d):
            s, i = m.group().decode(), m.start()
            if s in rt:
                continue
            if s in pool:
                in_pool += 1
                continue
            own = next(("%s %s" % (cn, "objects" if i < o1 else "arrays") for cn, o0, o1, a1 in spans if o0 <= i < a1),
                       "header/namespace" if i < nsend else "after the lists")
            where[s][own] += 1
check("C1", files == 169 and ends_ok == 169 and all("#" in x for x in ctl.get("PAssetReference", ["-"]))
      and ctl.get("PString") and not any("#" in x for x in ctl["PString"]),
      "169 files; lists end inside every file; c1004 PAssetReference arrays %s, PString arrays %s"
      % (ctl.get("PAssetReference", [])[:1], ctl.get("PString", [])[:2]))
print("\nfile-only P-names (not a runtime class leaf, not in the file's namespace pool): %d" % len(where))
owners = collections.Counter()
for s in sorted(where):
    print("   %-28s %s" % (s, dict(where[s])))
    owners.update(where[s])
print("\nby owning list:", dict(owners))
check("C2", all(k.endswith("arrays") for k in owners),
      "every occurrence sits in some instance list's array data - none in the namespace or the objects")
check("C3", {"PS2WHMatrix", "POSITION", "POSITION_MORPH", "PS_Blur", "PS_Combine", "PS2ZBias"} <= set(where),
      "the page's named examples are all in the set")
# C4 - the owning classes that are not shader programs hold the names in registered string members
sch = collections.defaultdict(dict)
for l in open(TSV, encoding="utf-8"):
    p = l.rstrip("\r\n").split("\t")
    if len(p) > 4:
        sch[p[0]][p[2]] = p[4]
want = {"PShaderParameterDefinition": "m_name", "PShaderStreamDefinition": "m_name", "PShaderPassInfo": "m_fragmentEntryPoint",
        "PMaterialSwitch": "m_name", "PStreamInputDescD3D11": "m_semantic"}
check("C4", all(sch[k].get(m) == "VPString" for k, m in want.items())
      and {k.split(" ")[0] for k in owners} - set(want) <= {"PShaderVertexProgram", "PShaderFragmentProgram", "PShaderGeometryProgram"},
      "non-program owners carry the names in registered PString members %s" % sorted("%s::%s" % kv for kv in want.items()))
print("FAILS %d" % fails)
