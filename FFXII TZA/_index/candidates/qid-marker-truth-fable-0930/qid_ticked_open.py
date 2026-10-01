"""qid_ticked_open.py - FABLE measurement (2026-09-30): TICKED checkboxes that name no register id and whose LIVE
(unstruck) text still says the item is only narrowed / partly answered / open / not read. Such a box counts as closed on
its page while nothing in the register backs it. Box text = the box line plus its indented continuation lines.
Positive control: a synthetic ticked box "- [x] Foo. **Narrowed 2026-09-30:** bar" with no id must be flagged."""
import io, os, re, sys
import os as _o; DB = _o.path.normpath(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "..", ".."))
DB = _o.path.dirname(DB)
reg = io.open(os.path.join(DB, "_index", "OPEN-QUESTIONS.md"), encoding="utf-8").read()
ids = set(re.findall(r"^\| ([A-Z][A-Z0-9]{0,6}-\d{1,4}[a-z]?) \|", reg, re.M))
TOK = re.compile(r"(?<![A-Za-z0-9_/-])([A-Z][A-Z0-9]{0,6}-\d{1,4}[a-z]?)(?![0-9A-Za-z])")
W = re.compile(r"(?i)\b(narrowed|half answered|partly answered|partially|still open|remains open|stays open|not (?:yet )?(?:read|established|known))\b")
def flag(txt):
    if any(t in ids for t in TOK.findall(txt)): return None
    m = W.search(re.sub(r"~~.*?~~", "", txt)); return m.group(0) if m else None
assert flag("- [x] Foo. **Narrowed 2026-09-30:** bar") == "Narrowed", "control failed"
out, total = [], 0
for root, dirs, files in os.walk(DB):
    dirs[:] = [d for d in dirs if d not in ("_experiments", "_inbox", "candidates", "progress", "_types", "archive")]
    for fn in files:
        if not fn.endswith(".md") or fn in ("OPEN-QUESTIONS.md", "ADDRESS-INDEX.md", "AUDIT-LOG.md"): continue
        p = os.path.join(root, fn); rel = os.path.relpath(p, DB).replace("\\", "/")
        L = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
        for i, l in enumerate(L):
            s = l.strip()
            if not re.match(r"^[-*] \[[xX]\]", s): continue
            j, txt = i + 1, s
            while j < len(L) and L[j].startswith("      ") and not re.match(r"^\s*[-*] \[", L[j]): txt += " " + L[j].strip(); j += 1
            if any(t in ids for t in TOK.findall(txt)): continue
            total += 1
            f = flag(txt)
            if f: out.append((rel, i + 1, f, re.sub(r"~~.*?~~", "", txt)))
print("ticked boxes naming no register id: %d; of them, live text says not closed: %d" % (total, len(out)))
for r in out: print("%s:%d [%s]\n    %s" % (r[0], r[1], r[2], r[3][:700]))
