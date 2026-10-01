import io, os, re, collections
import kit_paths as KP  # noqa: E402
import os

DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")
G = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
RE = re.compile(r"(?<![0-9A-Za-z_])(?:0[xX])?([0-9A-Fa-f]{8})(?![0-9A-Za-z_])")
sep = chr(92)

entries = {}
for ln in io.open(G, encoding="utf-8", errors="replace"):
    p = ln.rstrip("\n").split("\t")
    if len(p) >= 9 and re.match(r"^[0-9A-F]{8}$", p[0]):
        entries[p[0]] = (int(p[2]), p[1], p[3])

md = collections.defaultdict(set)
tsv = collections.defaultdict(set)
for root, dirs, files in os.walk(DB):
    dirs[:] = [d for d in dirs if d != "_templates"]
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), DB).replace(sep, "/")
        if f.endswith(".md"):
            if rel.startswith("_index/"):
                continue                       # indices echo; they are not citations
            tgt = md
        elif f.endswith(".tsv"):
            tgt = tsv
        else:
            continue
        t = io.open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
        for m in RE.finditer(t):
            a = m.group(1).upper()
            if a in entries:
                tgt[a].add(rel)

only_tsv = {a: v for a, v in tsv.items() if a not in md}
print("function entries cited in .md documents      : %d" % len(md))
print("function entries cited in .tsv side files    : %d" % len(tsv))
print("cited ONLY in a .tsv, in no document         : %d" % len(only_tsv))
print()
by_file = collections.Counter()
for a, v in only_tsv.items():
    for f in v:
        by_file[f] += 1
print("where those live:")
for k, n in by_file.most_common():
    print("   %-58s %d" % (k, n))
print()
owned = [a for a in only_tsv if entries[a][2]]
named = [a for a in only_tsv if not entries[a][1].startswith(("FUN_", "Unwind@", "Catch_All@"))]
print("of the .tsv-only set: %d owned, %d carry a real name" % (len(owned), len(named)))
big = sorted(only_tsv, key=lambda a: -entries[a][0])[:12]
print()
print("largest 12 by body size:")
for a in big:
    sz, nm, ow = entries[a]
    print("   %s %6dB %-44s %-24s %s" % (a, sz, nm[:44], (ow or "-")[:24],
                                         sorted(only_tsv[a])[0]))
