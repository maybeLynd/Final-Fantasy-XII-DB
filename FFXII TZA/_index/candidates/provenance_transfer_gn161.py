"""provenance_transfer_gn161.py - FABLE, 2026-09-14 (FRONTIER-REQ-FABLE-PROVENANCE-TRANSFER-GN161).

Re-sorts every GZF-derived document that is stale against the certified GN161 parent by the two INDEPENDENT tests the
transfer rulings require:
  1. the witness test: does every function the document cites have an identical, or a purely ADDITIVE, per-function record
     between the snapshot its stamp names and the GN161 parent snapshot (GFZFunctionAnnotationSnapshotV2)?
     additive = plate and repeatable comment empty in the stamped snapshot, stamped tag set a subset of the parent's, and
     name / namespace / symbol source / prototype / signature source / calling convention / flags / thunk / body identical;
  2. the decompiler test: does the document quote decompiler state (decompiler_tokens.py, the one canonical pattern)?
     Snapshots do not witness non-function symbols, the DTM, instruction comments, equates or reference overrides.
and flags, for the additive basis, any line that cites a delta function next to an ABSENCE word (the only claim an
additive delta can falsify), plus any residual/unresolved census figure bound to a generation.

usage: provenance_transfer_gn161.py OUT.tsv      (run from the repository root)
"""
import bisect, io, os, re, struct, sys

ROOT = "Database/"
DB = ROOT + "FFXII TZA/"
sys.path.insert(0, ROOT + "Tools/analysis-kit/gfz-scripts")
from decompiler_tokens import decompiler_tokens  # noqa: E402
exec(open(DB + "_index/candidates/provenance_snapshot_diff.py").read().split("\nA = parse")[0])  # parse(), FIELDS

SNAP = {  # snapshot_sha256 prefix -> file
    "46f02e26": ROOT + "Tools/work/verify/snapshot.fas2.GN158",
    "a9cead87": ROOT + "Tools/work/verify_GFZ_H9E159/snapshot.fas2",
    "b57264ba": ROOT + "Tools/work/verify_GFZ_GN160/snapshot.fas2",
}
GEN = {"2ed8affb": "GN158", "fb9b5e7e": "GN159", "fa0db293": "GN160"}
PARENT_SNAP = ROOT + "Tools/work/verify_GFZ_PARENT/snapshot.fas2"
PARENT_GZF = "11110a34acf6d0fc9ecd1727"

I = {n: k for k, n in enumerate(FIELDS)}
P = parse(PARENT_SNAP)
deltas = {}
for pre, path in SNAP.items():
    S = parse(path)
    assert set(S) == set(P), path
    d = {}
    for e in S:
        a, b = S[e], P[e]
        if a == b:
            continue
        moved = [f for f in FIELDS if a[I[f]] != b[I[f]]]
        additive = (set(moved) <= {"plate_comment", "repeatable_comment", "tags"}
                    and not a[I["plate_comment"]] and not a[I["repeatable_comment"]]
                    and set(a[I["tags"]]) <= set(b[I["tags"]]))
        d[e] = additive
    deltas[pre] = d
    print("%s -> GN161: %d records differ, %d additive" % (os.path.basename(path), len(d), sum(d.values())))

# body intervals from the parent snapshot, for interior citations
iv = sorted((lo, hi, e) for e, r in P.items() for lo, hi in r[I["body_ranges"]])
starts = [x[0] for x in iv]


def owner(a):
    if a in P:
        return a
    k = bisect.bisect_right(starts, a) - 1
    if k >= 0 and iv[k][0] <= a <= iv[k][1]:
        return iv[k][2]
    return None


ABSENCE = re.compile(r"unresolved|unclassified|untagged|no (?:code)?domain|no plate|no comment|uncommented|residual|"
                     r"unnamed|no name|not (?:yet )?(?:classified|named|tagged)|FUN_", re.I)
CENSUS = re.compile(r"\b(?:139|158|160|30)\b[^|\n]{0,40}(?:unresolved|residual)|(?:unresolved|residual)[^|\n]{0,40}\b(?:139|158|160|30)\b", re.I)

rows = []
for root, _dirs, files in os.walk(DB):
    top = os.path.relpath(root, DB).split(os.sep)[0]
    if not re.match(r"^\d\d-", top):
        continue
    for f in sorted(files):
        if not f.endswith(".md") or f == "README.md":
            continue
        p = os.path.join(root, f)
        t = io.open(p, encoding="utf-8").read()
        g = re.search(r"gzf_sha256:\s*([0-9a-f]{64})", t)
        if not g or g.group(1).startswith(PARENT_GZF):
            continue
        s = re.search(r"snapshot_sha256:\s*([0-9a-f]{64})", t)
        rel = os.path.relpath(p, DB).replace(os.sep, "/")
        gen = GEN.get(g.group(1)[:8], "?" + g.group(1)[:8])
        spre = s.group(1)[:8] if s else None
        if spre not in deltas:
            rows.append((rel, gen, spre or "-", "NO-WITNESS", "", "", "", ""))
            continue
        d = deltas[spre]
        body = t.split("\n---", 1)[1] if t.startswith("---") and "\n---" in t else t  # after the front matter only
        cited = set()
        hits_abs = set()
        for ln in body.split("\n"):
            fs = set()
            for m in re.finditer(r"(?<![0-9A-Fa-fx])([0-9A-Fa-f]{8})(?![0-9A-Fa-f])", ln):
                o = owner(int(m.group(1), 16))
                if o is not None:
                    fs.add(o)
            cited |= fs
            if fs & set(d) and ABSENCE.search(ln):
                hits_abs |= fs & set(d)
        touched = sorted(cited & set(d))
        nonadd = [e for e in touched if not d[e]]
        toks = sorted({k for k, _n, _x in decompiler_tokens(body)})
        census = bool(CENSUS.search(body))
        if nonadd:
            witness = "NON-ADDITIVE-DELTA"
        elif hits_abs:
            witness = "ADDITIVE-ABSENCE-REVIEW"
        elif touched:
            witness = "ADDITIVE"
        else:
            witness = "IDENTITY"
        rows.append((rel, gen, spre, witness, "yes" if toks else "no", ",".join(toks),
                     " ".join("%08X" % e for e in touched), ("census " if census else "") +
                     " ".join("%08X" % e for e in sorted(hits_abs))))

# Hand review of the token-free documents (FABLE 2026-09-14): the per-line absence flag cannot see a CENSUS of absence -
# a count of unresolved or untagged functions that the 109 new CodeDomain tags can change without the page citing any of
# them. Every token-free page was grepped for unresolved / residual / unclassified / untagged next to a figure; these two
# state such a census and owe a re-count, not a transfer. (The thunk-layer page's "untagged 181" is a thunk census, and
# none of the 128 delta functions is a thunk.)
CENSUS_REVIEW = {
    "00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md":
        "states '158 unresolved residual functions ... not yet classified' (lines 115, 247); GN161 resolves the residual to 30",
    "01-Script-VM-Native-Bridge/Verb-Dispatch/what-each-script-verb-touches.md":
        "states 93 verbs whose every depth-1 callee is untagged; 111 of the delta functions gained their first tag",
}


def ruling(r):
    if r[4] == "yes":
        return "WAIT-NONFUNCTION-EXPORT"
    if r[0] in CENSUS_REVIEW:
        return "CENSUS-REVIEW: " + CENSUS_REVIEW[r[0]]
    if r[3] == "IDENTITY":
        return "TRANSFER snapshot-identity"
    if r[3] == "ADDITIVE":
        return "TRANSFER additive-annotation delta"
    return "REVIEW " + r[3]


out = open(sys.argv[1], "w", encoding="utf-8", newline="\n")
out.write("# " + __doc__.strip().split("\n")[0] + "\n")
out.write("document\tstamp\tsnapshot\twitness_class\tdecompiler_tokens\ttoken_kinds\tcited_delta_functions\treview_flags\truling\n")
for r in sorted(rows):
    out.write("\t".join(r + (ruling(r),)) + "\n")
import collections
c = collections.Counter((r[1], r[3], r[4]) for r in rows)
for k in sorted(c):
    print("%-6s %-24s tokens=%-3s %4d" % (k[0], k[1], k[2], c[k]))
print("documents:", len(rows), " census-flagged:", sum(1 for r in rows if r[7].startswith("census")))
cr = collections.Counter((r[1], ruling(r).split(":")[0]) for r in rows)
for k in sorted(cr):
    print("%-6s %-40s %4d" % (k[0], k[1], cr[k]))
