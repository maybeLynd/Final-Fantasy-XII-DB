"""Pages not at DOCUMENTED (progress.coverage_documented), classified by what their `status:` line names (OPUS, 2026-09-29).

For each page the status line's register-style ids are looked up with check_questions.read_table:
  every-named-row-closed   every id it names is ANSWERED or WITHDRAWN (incl. dispositioned) in the register
  names-live-row           at least one named id is OPEN / PARTIAL / BLOCKED / UNKNOWN
  names-no-register-id     the line names no id the register holds (the residue is in prose)
Writes census.tsv beside this file and prints the counts. Reads only; changes no page.
"""
import collections, io, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
import check_questions as C, progress as PR
reg, _ = C.read_table(DB)
rows, cnt = [], collections.Counter()
for p in PR.docs(DB):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    if PR.coverage_documented(t):
        continue
    head = t[:t.find("\n---", 3)] if t.startswith("---") else t[:4000]
    m = re.search(r"^status:\s*(.*)$", head, re.M)
    st = m.group(1).strip() if m else ""
    word = (st.split()[0].strip("*`\"") if st.split() else "(none)")
    ids = sorted(set(re.findall(r"\b([A-Z]{1,4}-\d{1,4}[a-z]?)\b", st)))
    known = [i for i in ids if i in reg]
    live = [i for i in known if reg[i] not in ("ANSWERED", "WITHDRAWN")]
    k = "names-no-register-id" if not known else ("names-live-row" if live else "every-named-row-closed")
    cnt[(word, k)] += 1
    rows.append((os.path.relpath(p, DB).replace("\\", "/"), word, k, ",".join("%s=%s" % (i, reg[i]) for i in known)))
with io.open(os.path.join(HERE, "census.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("page\tstatus_word\tclass\tnamed_rows\n")
    for r in sorted(rows):
        f.write("\t".join(r) + "\n")
for k, v in cnt.most_common():
    print(v, k)
print("pages not documented:", len(rows))
