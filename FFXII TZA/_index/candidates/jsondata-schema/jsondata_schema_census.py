"""The schema of the shipped jsondata/ documents: nesting, per-key value types and ranges, and the reader that spells
each key (OPUS, 2026-09-25, block 293). For S-39's script/data cell ("the JSON schema itself is not decoded").

Inputs: an extracted jsondata/ tree (vbfextract.py of the retail FFXII_TZA.vbf) and the SHA-asserted EXE.
Readers: the 17-function population of reflected-render-parameters-and-shader-assets.md s8d (every JSON member lookup
goes through 001FF740 / 001FF6B0). For each key name, its NUL-terminated ASCII string is located in .rdata/.data and
every rip-relative reference to it is attributed to its containing function (functions.tsv); a key is 'read by F' when
F references the string and F is one of the 17. Composed families ('Cut N', 'PresetDof N', 'MonsterId%d',
'fontclut_%d', bare numerics) are grouped by their template.
Outputs: jsondata_schema.tsv (one row per family x path) and jsondata_schema.out.txt (summary). Read-only.
usage: python jsondata_schema_census.py <jsondata-dir>
"""
import bisect
import collections
import hashlib
import json
import os
import re
import struct
import sys

sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts")
import data_xref_scan as X  # noqa: E402

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
READERS = {0x1CA600, 0x1C7940, 0x1C3D50, 0x1C6320, 0x1C76E0, 0x1C3760, 0x1C6E20, 0x1C5750, 0x1C7360, 0x1C7520,
           0x1CC800, 0x1C2F50, 0x1CC920, 0x1C51D0, 0x1C52C0, 0x1C5530, 0x1C5570}
HERE = os.path.dirname(os.path.abspath(__file__))
FAILED = []


def family(rel):
    parts = rel.replace("\\", "/").split("/")
    return parts[0] if len(parts) > 1 else parts[0][:-5]


COMPOSED = [(re.compile(r"^Cut \d+$"), "Cut N"), (re.compile(r"^PresetDof ?\d+$"), "PresetDof N"),
            (re.compile(r"^MonsterId\d+$"), "MonsterIdN"), (re.compile(r"^fontclut_\d+$"), "fontclut_N"),
            (re.compile(r"^\d+$"), "N")]


def template(k):
    for rx, t in COMPOSED:
        if rx.match(k):
            return "<" + t + ">"
    return k


def vtype(v):
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, str):
        return "string"
    if isinstance(v, list):
        inner = sorted(set(vtype(x) for x in v)) or ["empty"]
        return "array<%s>" % "|".join(inner)
    if isinstance(v, dict):
        return "object"
    return "null"


def main(root):
    stats = collections.OrderedDict()
    fams = collections.Counter()
    for dp, _, fs in os.walk(root):
        for f in sorted(fs):
            if not f.endswith(".json"):
                continue
            rel = os.path.relpath(os.path.join(dp, f), root)
            fam = family(rel)
            fams[fam] += 1
            try:
                doc = json.load(open(os.path.join(dp, f), encoding="utf-8-sig"))
            except ValueError as e:
                FAILED.append((rel, str(e)))
                continue

            def walk(o, path):
                if isinstance(o, dict):
                    for k, v in o.items():
                        p = path + "/" + template(k)
                        s = stats.setdefault((fam, p), {"types": collections.Counter(), "files": set(), "n": 0,
                                                        "min": None, "max": None, "key": k})
                        s["types"][vtype(v)] += 1
                        s["files"].add(rel)
                        s["n"] += 1
                        if isinstance(v, (int, float)) and not isinstance(v, bool):
                            s["min"] = v if s["min"] is None else min(s["min"], v)
                            s["max"] = v if s["max"] is None else max(s["max"], v)
                        walk(v, p)
                elif isinstance(o, list):
                    for x in o:
                        if isinstance(x, (dict, list)):
                            walk(x, path + "[]")
            walk(doc, "")
    # readers per key name
    raw = open(EXE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA
    secs = X.sections_of(raw)
    names = sorted(set(p.rsplit("/", 1)[-1].replace("[]", "") for (_, p) in stats))
    name_va = {}
    for n in names:
        pat = n.encode() + b"\0"
        vas = []
        i = raw.find(b"\0" + pat)
        while i != -1:
            off = i + 1
            for _nm, ro, sz, v in secs:
                if ro <= off < ro + sz:
                    vas.append(v + off - ro)
            i = raw.find(b"\0" + pat, i + 1)
        if vas:
            name_va[n] = vas
    wanted = set(va for vs in name_va.values() for va in vs)
    res = X.scan(raw, secs, X.entries(FUNCS), wanted)
    starts = sorted(int(l.split("\t")[0], 16) for l in open(FUNCS, encoding="utf-8", errors="replace") if l[:1] in "0123456789ABCDEF")
    va_readers = collections.defaultdict(set)
    va_refs = collections.defaultdict(set)
    for a, hits in res.items():
        for ins, mn, ops, f in hits:
            fn = f if f else starts[bisect.bisect_right(starts, ins) - 1]
            va_refs[a].add(fn)
            if fn in READERS:
                va_readers[a].add(fn)
    rows = []
    for (fam, p), s in stats.items():
        leaf = p.rsplit("/", 1)[-1].replace("[]", "")
        rd = sorted(set().union(*[va_readers[va] for va in name_va.get(leaf, [])]) if leaf in name_va else [])
        anyref = sorted(set().union(*[va_refs[va] for va in name_va.get(leaf, [])]) if leaf in name_va else [])
        rows.append((fam, p, "|".join("%s:%d" % kv for kv in s["types"].most_common()), len(s["files"]), s["n"],
                     "" if s["min"] is None else repr(s["min"]), "" if s["max"] is None else repr(s["max"]),
                     ",".join("%08X" % r for r in rd) or ("composed" if leaf.startswith("<") else "none"),
                     ",".join("%08X" % r for r in anyref[:4])))
    with open(os.path.join(HERE, "jsondata_schema.tsv"), "w", encoding="utf-8", newline="\n") as o:
        o.write("family\tpath\tvalue_types\tfiles\toccurrences\tmin\tmax\treaders(17-set)\tany_image_ref\n")
        for r in rows:
            o.write("\t".join(str(x) for x in r) + "\n")
    out = ["jsondata schema census (OPUS block 293) - %d files parsed, %d not strict JSON" % (sum(fams.values()), len(FAILED))]
    out += ["  NOT STRICT JSON: %s - %s" % x for x in FAILED]
    for fam, n in fams.most_common():
        fr = [r for r in rows if r[0] == fam]
        read = sum(1 for r in fr if r[7] not in ("none", "composed"))
        mixed = sum(1 for r in fr if "|" in r[2])
        out.append("  %-24s files %4d  paths %4d  read-by-17 %4d  composed %3d  unread %4d  mixed-type paths %d"
                   % (fam, n, len(fr), read, sum(1 for r in fr if r[7] == "composed"), sum(1 for r in fr if r[7] == "none"), mixed))
    open(os.path.join(HERE, "jsondata_schema.out.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1])
