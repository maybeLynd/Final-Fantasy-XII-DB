"""escape_rows.py IN OUT - repair register rows whose cell count differs from their 3-column table (FABLE, Claude Opus 5.5,
2026-09-28). Two defects, both fixed without changing any text other than one backslash per pipe:
  over-split  a literal "|" inside a row's text (e.g. `(a << 8) | b`, |x|) splits it into extra cells; each such pipe is
              escaped. The cell groups are fixed per row below and checked: the status cell must start with a verdict word.
  under-split the separator before the status was written escaped (" \\| **ANSWERED"), so the status sits in the question
              cell; the one escaped pipe followed by a verdict word is unescaped. A row with zero or several candidates
              is refused, not guessed.
Every repaired row must reproduce the original line when all "\\|" are read as "|", and must end with exactly 3 cells.
"""
import re, sys
SPLIT = re.compile(r"(?<!\\)\|")
VERDICT = r"\s*(?:\*\*|~~|\*)?\s*(?:ANSWERED|PARTIAL|OPEN|SUPERSEDED|WITHDRAWN|NOT A QUESTION|NO ADMISSIBLE SOURCE|OUT OF EVIDENCE BOUNDARY|CLOSED|RESOLVED|DISSOLVED|NARROWED|QUALIFIED)"
STATUS = re.compile(r"^" + VERDICT)
OVER = {"PS-1": [[0], [1, 2, 3], [4]], "BI-13": [[0], [1], [2, 3]], "UQ-210": [[0], [1, 2], [3]],
        "UQ-218": [[0], [1, 2, 3, 4], [5]], "UQ-242": [[0], [1], [2, 3, 4, 5, 6]], "UQ-255": [[0], [1], [2, 3, 4, 5]]}
def cells_of(body): return SPLIT.split(body)[1:-1]
def fix(q, l):
    cr = chr(13) if l.endswith(chr(13)) else ""
    body = l[:-1] if cr else l
    tail = body[len(body.rstrip(" ")):]; body = body.rstrip(" ")
    cells = cells_of(body)
    if q in OVER:
        g = OVER[q]
        if sorted(k for x in g for k in x) != list(range(len(cells))): return None, "groups do not cover %d cells" % len(cells)
        new = ["\\|".join(cells[k] for k in x) for x in g]
    elif len(cells) == 2:
        cands = [m.start() for m in re.finditer(r"\\\|(?=" + VERDICT + ")", cells[1])]
        if len(cands) != 1: return None, "%d escaped-separator candidates" % len(cands)
        k = cands[0]; new = [cells[0], cells[1][:k], cells[1][k + 2:]]
    else:
        return None, "%d cells, no rule" % len(cells)
    if not STATUS.match(new[2]): return None, "status cell reads %r" % new[2][:40]
    out = "|" + "|".join(new) + "|" + tail + cr
    if out.replace("\\|", "|") != l.replace("\\|", "|"): return None, "text changed beyond the escapes"
    if len(cells_of(out.rstrip(chr(13)).rstrip(" "))) != 3: return None, "still not 3 cells"
    return out, None
def apply(t, report=False):
    lines = t.split("\n"); cols = None; fixed, refused = [], []
    for i, l in enumerate(lines):
        s = l.rstrip("\r")
        if re.match(r"^\|\s*:?-{3,}", s): cols = len(SPLIT.split(s.rstrip(" "))) - 2; continue
        if not s.strip() or s.startswith("#"): cols = None
        m = re.match(r"\| ([A-Z]+-[0-9a-z]+) \|", s)
        if not (m and cols == 3): continue
        if len(cells_of(s.rstrip(" "))) == 3: continue
        out, why = fix(m.group(1), l)
        if out is None: refused.append((i + 1, m.group(1), why))
        else: lines[i] = out; fixed.append(m.group(1))
    if report:
        print("fixed %d: %s" % (len(fixed), fixed))
        for r in refused: print("refused line %d %s: %s" % r)
    if set(OVER) - set(fixed): sys.exit("REFUSE: an over-split row was not fixed: %s" % sorted(set(OVER) - set(fixed)))
    return "\n".join(lines), fixed, refused
if __name__ == "__main__":
    t = open(sys.argv[1], encoding="utf-8", newline="").read()
    out, fixed, refused = apply(t, report=True)
    open(sys.argv[2], "w", encoding="utf-8", newline="").write(out); print("ok", len(fixed))
