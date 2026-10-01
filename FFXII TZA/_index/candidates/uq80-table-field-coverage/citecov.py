# citecov.py - which DB pages cite each reader instruction address the sweep found (exact 8-hex token match).
# A citation of the instruction address is evidence the page discusses that read; it is NOT proof the page
# states the field's meaning (checked by hand, see coverage.tsv).  Pages under _index/ are excluded.
import os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
DB = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
idx = collections.defaultdict(set)
for root, dirs, files in os.walk(DB):
    if "_index" in root.split(os.sep): continue
    for f in files:
        if not f.endswith(".md"): continue
        p = os.path.join(root, f)
        rel = os.path.relpath(p, DB).replace("\\", "/")
        for tok in set(re.findall(r"\b[0-9A-F]{8}\b", open(p, encoding="utf-8", errors="replace").read())):
            idx[tok].add(rel)
cur = None
rows = []
for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "trace_all.txt")):
    m = re.match(r"== slot (\w+)", line)
    if m: cur = m.group(1); continue
    m = re.match(r"rec (\w+) (\w+) w(\d+) disp=(-?0x[0-9a-f]+) rowoff=(\S+) base=(\S+) idx=(\S+)\s+(.*)", line)
    if m:
        f, a, w, disp, ro, b, ix, text = m.groups()
        pages = sorted(idx.get(a, ()))
        rows.append((cur, ro, int(w), a, f, text.strip(), pages))
want = set(sys.argv[1:])
out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "reader_citations.tsv"), "w", encoding="utf-8")
out.write("slot\trowoff\twidth\tinstr\tfunc\ttext\tpages_citing_instr\n")
for r in rows:
    out.write("%s\t%s\t%d\t%s\t%s\t%s\t%s\n" % (r[0], r[1], r[2], r[3], r[4], r[5], "; ".join(r[6])))
    if not want or r[0] in want:
        print("%s %6s w%d %s %s %-40s %s" % (r[0], r[1], r[2], r[3], r[4], r[5][:40], "; ".join(p.split("/")[-1] for p in r[6])[:200]))
