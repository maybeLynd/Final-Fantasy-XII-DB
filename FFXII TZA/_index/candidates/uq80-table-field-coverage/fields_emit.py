# fields_emit.py - write one <table>-fields.tsv per table from uq80_manifest.tsv + the us pack tallies + the reader
# sweep (trace_all.txt).  Columns: offset, width, status, name, value tally (top 5, at the field's element width),
# readers found by the sweep inside the field (addr + instruction; '*' = cited in the manifest and decoded by
# uq80_coverage.py), meaning, evidence class, source.
import os, re, sys, collections, struct
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pack import TABLES, records
SLOT = {n: s for n, s, d in TABLES}
REC = {n: records(d)[0] for n, s, d in TABLES}

sweep = collections.defaultdict(list)   # slot -> [(rowoff:int or None, text, addr, width)]
cur = None
for line in open(os.path.join(HERE, "trace_all.txt")):
    m = re.match(r"== slot (\w+)", line)
    if m: cur = m.group(1); continue
    m = re.match(r"rec (\w+) (\w+) w(\d+) disp=(-?0x[0-9a-f]+) rowoff=(\S+) base=(\S+) idx=(\S+)\s+(.*)", line)
    if m:
        f, a, w, disp, ro, b, ix, text = m.groups()
        mm = re.match(r"(?:walk>=)?(\d+)$", ro)
        sweep[cur].append((int(mm.group(1)) if mm else None, ro, a, int(w), text.strip()))

rows = collections.defaultdict(list)
for line in open(os.path.join(HERE, "uq80_manifest.tsv"), encoding="utf-8"):
    line = line.rstrip("\n")
    if not line or line.startswith("#") or line.startswith("table\t"): continue
    rows[line.split("\t")[0]].append(line.split("\t"))

outdir = HERE
for name in rows:
    recs = REC[name]; slot = SLOT[name]
    out = open(os.path.join(outdir, "%s-fields.tsv" % name), "w", encoding="utf-8", newline="\n")
    out.write("offset\twidth\tstatus\tname\tvalue_tally_top5\treaders_found_by_sweep\tmeaning\tevidence\tsource\n")
    for t, o, w, st, nm, meaning, ev, readers, src in rows[name]:
        o = int(o, 16); w = int(w)
        cited = set(r.split("@")[0].split(":")[0] for r in readers.split(",") if r)
        ew = [int(m) for m in re.findall(r":w(\d+)", readers)]
        el = ew[0] if ew else (w if w in (1, 2, 4) else 1)
        c = collections.Counter()
        for r in recs:
            for e in range(o, o + w, el): c[int.from_bytes(r[e:e + el], "little")] += 1
        tally = "u%d: " % (8 * el) + ", ".join("%s x%d" % (("%#x" % v) if el > 1 else str(v), k) for v, k in c.most_common(5)) + (" (%d distinct)" % len(c))
        rd = []
        for ro, rostr, a, rw, text in sweep.get(slot, []):
            if ro is not None and o <= ro < o + w:
                rd.append("%s%s %s" % (a, "*" if a in cited else "", text if not rostr.startswith("walk") else text + " (walk from +%#x)" % ro))
        for a in sorted(cited - set(x.split("*")[0].split(" ")[0] for x in rd)):
            rd.append("%s* (cited; outside the sweep's offset attribution)" % a)
        out.write("%#04x\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (o, w, st, nm, tally, " | ".join(rd) or "-", meaning, ev or "-", src))
    out.close()
print("wrote", len(rows), "field files")
