"""cell_count_scan.py - list register rows whose cell count differs from their table's column count (FABLE, Claude Opus 5.5,
2026-09-28). An unescaped pipe inside a row's text splits it into extra cells; a reader of the last cell then gets text
instead of the status.
Usage: python cell_count_scan.py [OPEN-QUESTIONS.md]      (exit 1 when any row is split)
Control: python cell_count_scan.py --self-test          (plants one split row and one escaped row; must flag exactly one)
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SPLIT = re.compile(r"(?<!\\)\|")
def scan(lines):
    cols = None; bad = []
    for i, l in enumerate(lines, 1):
        l = l.rstrip("\r")
        if re.match(r"^\|\s*:?-{3,}", l): cols = len(SPLIT.split(l.rstrip(" "))) - 2; continue
        if not l.strip() or l.startswith("#"): cols = None      # a GFM table ends at a blank line or a heading
        m = re.match(r"\| ([A-Z]+-[0-9a-z]+) \|", l)
        if m and cols:
            n = len(SPLIT.split(l.rstrip(" "))) - 2
            if n != cols: bad.append((i, m.group(1), n, cols))
    return bad
if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        t = ["| ID | Question | Status |", "|---|---|---|", "| ZZ-1 | a `x | y` b | ANSWERED |", "| ZZ-2 | a `x \\| y` b | ANSWERED |"]
        r = scan(t); print("self-test:", r); sys.exit(0 if [b[1] for b in r] == ["ZZ-1"] else 1)
    P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "../../OPEN-QUESTIONS.md")
    bad = scan(open(P, encoding="utf-8").read().split("\n"))
    for b in bad: print("line %d %s: %d cells in a %d-column table" % b)
    print("rows with a split cell: %d" % len(bad)); sys.exit(1 if bad else 0)
