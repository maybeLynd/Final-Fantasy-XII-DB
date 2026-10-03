"""ps_present_tense_check.py - SWE2-DATA, 2026-10-03, FABLE-REQ-DATA-CONTEXT-REFRESH-MIRROR-PROGRESS-1003 part (4).

Rejects the superseded present-tense readings in PROGRAM-STATE.md section 1/2 (each may survive only inside ~~strike~~),
and checks the figures PROGRAM-STATE now quotes against the generated PROGRESS.md, so a later drift fails here instead of
going stale silently. Read-only.  Run: python -B ps_present_tense_check.py   (FAILS 0 is the only pass)
Self-test: python -B ps_present_tense_check.py --self-test  (each mutation must be caught)."""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PS = os.path.join(DB, "_index", "PROGRAM-STATE.md")
PG = os.path.join(DB, "PROGRESS.md")

SUPERSEDED = [
    r"\*\*not reached by any subsystem\.\*\*",          # L2 row, contradicted by the scoped L2 verdicts
    r"\*\*346 documents, 28/28 categories\*\*",         # copied volatile count
    r"### Current at HEAD `c65b1a16`",                  # a dated snapshot labelled current
]


def unstruck(t):
    return re.sub(r"~~.*?~~", "", t, flags=re.S)


def check(ps, pg):
    out = []
    head = ps[:ps.find("## 3.")] if "## 3." in ps else ps
    for pat in SUPERSEDED:
        if re.search(pat, unstruck(head)):
            out.append("superseded phrase outside ~~strike~~: /%s/" % pat)
    m = re.search(r"\*\*(\d+) MET of (\d+) systems\*\*", pg)
    if not m:
        out.append("PROGRESS.md states no 'N MET of M systems' L2 line")
    elif m.group(1) != m.group(2):
        out.append("PROGRESS.md L2 is %s of %s - PROGRAM-STATE's 'MET for every system' no longer holds"
                   % (m.group(1), m.group(2)))
    if "DB_GOAL" not in pg or "NOT_MET" not in pg:
        out.append("PROGRESS.md no longer reads DB_GOAL NOT_MET - PROGRAM-STATE's L2 row must be revisited")
    elif "the whole-database goal is NOT_MET" not in ps:
        out.append("PROGRAM-STATE's L2 row does not state the whole-database goal is NOT_MET")
    p = re.search(r"(\d+) of (\d+) pilots certified", pg)
    q = re.search(r"reads (\d+) of\s+(\d+) pilots certified", ps)
    if not (p and q) or p.groups() != q.groups():
        out.append("pilot count disagrees: PROGRESS.md %s vs PROGRAM-STATE %s"
                   % (p and p.groups(), q and q.groups()))
    if "PROGRESS.md](../PROGRESS.md)" not in ps:
        out.append("PROGRAM-STATE section 1 does not link the generated PROGRESS.md")
    return out


def main():
    ps = open(PS, encoding="utf-8").read().replace("\r\n", "\n")
    pg = open(PG, encoding="utf-8").read().replace("\r\n", "\n")
    if "--self-test" in sys.argv:
        muts = [
            ("L2 phrase unstruck", ps.replace("~~**not reached by any subsystem.**", "**not reached by any subsystem.** ~~", 1), pg),
            ("old count unstruck", ps.replace("~~**346 documents, 28/28 categories**~~", "**346 documents, 28/28 categories**", 1), pg),
            ("heading back to Current", ps.replace("### Measured at HEAD `c65b1a16`", "### Current at HEAD `c65b1a16`", 1), pg),
            ("PROGRESS L2 drops", ps, re.sub(r"\*\*(\d+) MET of (\d+) systems\*\*", "**51 MET of 52 systems**", pg, count=1)),
            ("pilot count drifts", ps, re.sub(r"(\d+) of (\d+) pilots certified", "1 of 45 pilots certified", pg, count=1)),
        ]
        bad = [n for n, a, b in muts if not check(a, b)]
        base = check(ps, pg)
        print("self-test: %d mutation(s) caught of %d; unmutated findings %d" % (len(muts) - len(bad), len(muts), len(base)))
        print("FAILS %d" % (len(bad) + len(base)))
        return 1 if bad or base else 0
    out = check(ps, pg)
    for o in out:
        print("FAIL  " + o)
    print("checked PROGRAM-STATE.md section 1/2 against PROGRESS.md")
    print("FAILS %d" % len(out))
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main())
