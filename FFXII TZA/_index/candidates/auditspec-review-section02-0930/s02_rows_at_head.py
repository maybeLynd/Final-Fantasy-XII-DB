"""s02_rows_at_head.py - are SECTION-02's 14 canonical row changes (1 types.tsv row, 13 fields.tsv rows) still present at
HEAD, and if a row changed later, which columns? Reads the _types files at git HEAD (the working tree has peer edits).
"""
import io, json, os

DB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
rows = json.load(io.open(os.path.join(DB, "_experiments", "evidence", "continuation-section02-resource-queue",
                                      "canonical_row_changes.json"), encoding="utf-8"))


def table(name):
    import subprocess
    t = subprocess.run(["git", "show", "HEAD:./_types/" + name], cwd=DB, capture_output=True, check=True).stdout
    L = t.decode("utf-8").replace("\r\n", "\n").split("\n")
    hdr = L[0].split("\t")
    return hdr, [dict(zip(hdr, l.split("\t"))) for l in L[1:] if l.strip()]


cache = {}
same = 0
for r in rows:
    f = r["file"].split("/")[-1]
    if f not in cache:
        cache[f] = table(f)
    hdr, recs = cache[f]
    key = r["key"]
    cur = [x for x in recs if all(x.get(k) == v for k, v in key.items())]
    if not cur:
        print("MISSING %s %s" % (f, key))
        continue
    c = cur[0]
    diff = [k for k, v in r["after"].items() if c.get(k) != v]
    if not diff:
        same += 1
        print("SAME    %s %s" % (f, key))
    else:
        print("CHANGED %s %s columns %s" % (f, key, diff))
        for k in diff:
            print("          after: %r" % (r["after"][k][:160],))
            print("          head:  %r" % (c.get(k, "")[:160],))
print("rows %d, unchanged since SECTION-02: %d" % (len(rows), same))
