"""incorporate.py - bring the SD register rows current with answers already committed in records (FABLE, 2026-09-30).
Input: incorp/plan.tsv (id, sha, verdict, subject answer, record dir(s), checks) from collect.py, with the verdict
overrides below. Answered rows: the status cell gets a leading ANSWERED lead citing the commit and record, the old text
kept as '*Was:*'; their unticked page boxes are ticked with a dated note. Narrowed rows: a dated narrowing is inserted
after the existing lead; boxes untouched. Pages that are dirty are skipped (and the row too, to keep the ledger
consistent). All-or-nothing; CRLF-safe. --check validates and prints the plan."""
import io, os, re, subprocess, sys
os.chdir(r"C:\Users\Kristian\source\repos\XIIOnline")
DB = "Database/FFXII TZA/"
OQ = DB + "_index/OPEN-QUESTIONS.md"
OVERRIDE = {"SD-164": "answered", "SD-166": "narrowed", "SD-167": "answered"}
CELL = re.compile(r"(?<!\\)\|")
BOX = re.compile(r"^(\s*-\s*)\[ \]")
plan = []
for l in io.open("Database/Tools/work/FABLE/incorp/plan.tsv", encoding="utf-8").read().splitlines():
    rid, sha, verdict, subj, recs, checks = l.split("\t")
    plan.append((rid, sha, OVERRIDE.get(rid, verdict), subj.strip().rstrip("."), recs.split(";")[0]))
dirty = set(subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True).stdout.split("\n"))
def load(p):
    raw = io.open(p, encoding="utf-8", newline="").read()
    return raw.replace("\r\n", "\n"), "\r\n" in raw[:20000]
oq, oq_crlf = load(OQ)
if OQ in dirty and "--check" not in sys.argv: print("REFUSED: register dirty"); sys.exit(2)
lines = oq.split("\n")
pages = {}
problems, done = [], []
for rid, sha, verdict, subj, rec in plan:
    idx = [i for i, l in enumerate(lines) if l.startswith("| %s |" % rid)]
    if len(idx) != 1: problems.append("%s row x%d" % (rid, len(idx))); continue
    cells = CELL.split(lines[idx[0]])
    st = cells[-2].strip()
    reclink = "candidates/" + rec.split("/_index/candidates/", 1)[1] + "/README.md"
    if verdict == "answered":
        new = ("**ANSWERED 2026-09-30 (OPUS `%s`, static; record [`%s`](%s); incorporated by FABLE for the SD section;"
               " review as the record routes it):** %s. *Was:* %s" % (sha, reclink.split("/")[1], reclink, subj, st))
    else:
        m = re.match(r"^(\*\*[^*]+\*\*)\s*", st)
        if not m: problems.append("%s: no lead" % rid); continue
        new = "%s *Narrowed 2026-09-30 (OPUS `%s`; record [`%s`](%s)):* %s. %s" % (m.group(1), sha, reclink.split("/")[1], reclink, subj, st[m.end():])
    if "|" in new.replace("\\|", ""): problems.append("%s: pipe in text" % rid); continue
    cells[-2] = " " + new + " "
    lines[idx[0]] = "|".join(cells)
    done.append((rid, verdict))
    if verdict != "answered": continue
    # tick this id's unticked boxes on live pages
    for root, dirs, files in os.walk(DB):
        if any(s in root for s in ("retained", "source-preimages", "_experiments", "_index")): continue
        for fn in files:
            if not fn.endswith(".md"): continue
            p = os.path.join(root, fn).replace("\\", "/")
            if p not in pages:
                t = io.open(p, encoding="utf-8", errors="replace").read()
                if not re.search(r"\bSD-\d+\b", t): continue
                pages[p] = [load(p), False]
            (t, crlf), _ = pages[p]
            L = t.split("\n"); ch = False
            i = 0
            while i < len(L):
                if re.match(r"^\s*-\s*\[[x ]\]", L[i]):
                    j = i + 1
                    while j < len(L) and L[j].strip() and not re.match(r"^\s*-\s*\[[x ]\]", L[j]) and not L[j].startswith("#"): j += 1
                    if BOX.match(L[i]) and re.search(r"\b%s\b" % rid, "\n".join(L[i:j])):
                        rel = os.path.relpath(DB + "_index/" + reclink, os.path.dirname(p)).replace("\\", "/")
                        L[i] = BOX.sub(r"\1[x]", L[i], 1)
                        L[j - 1] = L[j - 1] + " *(%s answered 2026-09-30 by OPUS `%s`, [record](%s).)*" % (rid, sha, rel)
                        ch = True
                    i = j
                else: i += 1
            if ch: pages[p] = [("\n".join(L), crlf), True]
touched = [p for p, (_, c) in pages.items() if c]
bad = [p for p in touched if p in dirty]
if bad: problems.append("dirty pages would be touched: %s" % bad)
print("rows: %d answered, %d narrowed; pages touched %d" % (sum(1 for d in done if d[1] == "answered"),
      sum(1 for d in done if d[1] != "answered"), len(touched)))
for p in touched: print("  ", p[len(DB):])
if problems: print("REFUSED:", problems); sys.exit(2)
io.open("Database/Tools/work/FABLE/incorp/pages.txt", "w", encoding="utf-8").write("\n".join(touched) + "\n")
if "--check" in sys.argv: print("CHECK OK"); sys.exit(0)
o = "\n".join(lines)
io.open(OQ, "w", encoding="utf-8", newline="").write(o.replace("\n", "\r\n") if oq_crlf else o)
for p in touched:
    (t, crlf), _ = pages[p]
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n") if crlf else t)
print("applied")
