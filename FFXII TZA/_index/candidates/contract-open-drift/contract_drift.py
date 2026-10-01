# contract_drift.py (FABLE, Claude Opus 5.5, 2026-09-26) - contract lines that call a question id open/unestablished while its
# register row is ANSWERED. Candidates for hand review only (a line may discuss the id historically, or an unanswered sub-part).
# First run found UQ-136 (level-advance contract) and DD-1 (binding-profiles contract, contradicting its own section 7a).
import os, re
DB = str(__import__("pathlib").Path(__file__).resolve().parents[3])
status = {}
for l in open(os.path.join(DB, "_index", "OPEN-QUESTIONS.md"), encoding="utf-8"):
    m = re.match(r"^\| ([A-Z][A-Za-z]*-[0-9]+[a-z]?) \| .* \| ([^|]*) \|\s*$", l.rstrip("\n"))
    if m: status[m.group(1)] = m.group(2).strip()
OPENW = re.compile(r"\b(open|not established|unresolved|stays open|remain[s]? open|unanswered)\b", re.I)
HIST = re.compile(r"~~|answered|resolved|closed|superseded|corrected", re.I)
for dp, dn, fn in os.walk(DB):
    if "_index" in dp or "_inbox" in dp: continue
    for f in fn:
        if not (f.startswith("CONTRACT-") and f.endswith(".md")): continue
        p = os.path.join(dp, f)
        inside = False                      # a ~~strike~~ may span lines; a line that starts inside one is struck text
        for i, l in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
            was = inside
            inside = (l.count("~~") % 2 == 1) != inside
            if was or not OPENW.search(l) or HIST.search(l): continue
            for q in set(re.findall(r"(?<![A-Za-z0-9-])([A-Z][A-Za-z]*-[0-9]+[a-z]?)(?![0-9])", l)):
                st = status.get(q, "").lstrip("*~ ")   # a bold **ANSWERED cell counts (the page scan missed AS-2 without this)
                if st.upper().startswith("ANSWERED") or st.upper().startswith("CLOSED"):
                    print("%-8s %-10s %s:%d  %s" % (q, st[:10], os.path.relpath(p, DB)[-55:], i, l.strip()[:120]))
