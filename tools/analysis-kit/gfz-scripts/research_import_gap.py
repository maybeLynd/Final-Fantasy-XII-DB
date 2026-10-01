import io, os, re, collections
import kit_paths as KP  # noqa: E402

ROOT = KP.ROOT
DB = os.path.join(ROOT, "Database", "FFXII TZA")
G = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
RE = re.compile(r"(?<![0-9A-Za-z_])(?:0[xX])?([0-9A-Fa-f]{8})(?![0-9A-Za-z_])")
sep = chr(92)

entries = {}
for ln in io.open(G, encoding="utf-8", errors="replace"):
    p = ln.rstrip("\n").split("\t")
    if len(p) >= 9 and re.match(r"^[0-9A-F]{8}$", p[0]):
        entries[p[0]] = (int(p[2]), p[1], p[3], p[8])

def scan_files(paths):
    hits = collections.defaultdict(set)
    for path, label in paths:
        try:
            t = io.open(path, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for m in RE.finditer(t):
            a = m.group(1).upper()
            if a in entries:
                hits[a].add(label)
    return hits

# database side
dbfiles = []
for root, dirs, files in os.walk(DB):
    dirs[:] = [d for d in dirs if d != "_templates"]
    for f in files:
        if f.endswith(".md"):
            rel = os.path.relpath(os.path.join(root, f), DB).replace(sep, "/")
            if not rel.startswith("_index/"):
                dbfiles.append((os.path.join(root, f), rel))
db = scan_files(dbfiles)

# research PROSE only: top-level Collaboration markdown, excluding tools/ and generated output
COL = os.path.join(ROOT, "Collaboration")
prose = []
for f in sorted(os.listdir(COL)):
    fp = os.path.join(COL, f)
    if os.path.isfile(fp) and f.endswith(".md"):
        prose.append((fp, "Collaboration/" + f))
print("research prose documents at Collaboration/ top level: %d" % len(prose))
h = scan_files(prose)
new = {a: v for a, v in h.items() if a not in db}
print("  cited by that prose            : %d distinct function entries" % len(h))
print("  NOT cited anywhere in database : %d  (%.1f %%)" % (len(new), 100.0*len(new)/len(h) if h else 0))

owned = [a for a in new if entries[a][2]]
named = [a for a in new if not entries[a][1].startswith(("FUN_", "Unwind@", "Catch_All@"))]
print("  of the gap, carrying a PrimaryOwner : %d" % len(owned))
print("  of the gap, carrying a real name    : %d" % len(named))
print()
print("The gap that matters: NAMED and OWNED, i.e. someone identified it and the database lacks it")
both = sorted({a for a in owned} & {a for a in named}, key=lambda a: -entries[a][0])
print("  count: %d" % len(both))
print()
print("%-9s %6s %-42s %-24s %s" % ("addr", "bytes", "name", "owner", "research document"))
for a in both[:32]:
    sz, nm, ow, tg = entries[a]
    src = sorted(new[a])
    print("%-9s %6d %-42s %-24s %s%s" % (a, sz, nm[:42], ow[:24], src[0].replace("Collaboration/", "")[:40],
                                          (" +%d" % (len(src)-1)) if len(src) > 1 else ""))
print()
oc = collections.Counter(entries[a][2] for a in both)
print("owner mix of the named+owned gap:")
for k, v in oc.most_common():
    print("   %-40s %d" % (k, v))
print()
doc = collections.Counter()
for a in both:
    for s in new[a]:
        doc[s] += 1
print("research documents contributing most of the gap:")
for k, v in doc.most_common(12):
    print("   %-56s %d" % (k.replace("Collaboration/", ""), v))
