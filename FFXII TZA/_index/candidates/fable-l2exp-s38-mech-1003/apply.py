"""apply.py - FABLE, 2026-10-03: stage the S-38 flag-word owners section (SWE2-AUDIT-SPEC L2 expansion, item 3).

  python apply.py            dry run: check every anchor, show what would change, write nothing
  python apply.py --apply    write the edit (only when every check passes)

Edit:
  E1  17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md: insert section.txt as "## 14a." after
      section 14, before the line "## 15. Evidence".

Guards:
  - a page with uncommitted content changes (git diff HEAD, or a staged change) is REFUSED;
  - the anchors "## 14. Unresolved" and "## 15. Evidence" must each occur exactly once, in that order, and "## 14a."
    must not exist under another heading;
  - the page's line endings (CRLF or LF) are detected and kept;
  - idempotent: when the section's heading is already present the edit is reported ALREADY and skipped;
  - every relative link in the section must resolve from the contract's folder;
  - the section's heading and every subheading carry "FABLE";
  - the staged page is run through contract_named_state_census's own section parser: 14a must NOT be read as a
    state/types section, and the parser's state lines must be identical before and after (no denominator change);
  - each table in the section keeps one cell-separator count per row.

Prints FAILS N last.
"""
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REPO = os.path.abspath(os.path.join(DB, "..", ".."))
KIT = os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts")
CONTRACT = os.path.join(DB, "17-Presentation-Rendering", "CONTRACT-render-record-pool-lifecycle.md")
HEAD_LINE = ("## 14a. The flag word's owners outside the family - who writes bits 0, 2 and 4, and what the pool "
             "reads back (FABLE, 2026-10-03)")
A_BEFORE = r"^## 14\. Unresolved\s*$"
A_AFTER = r"^## 15\. Evidence\s*$"
APPLY = "--apply" in sys.argv
fails = 0


def report(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", tag, text))


def rel(p):
    return os.path.relpath(p, REPO).replace(os.sep, "/")


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True)


def dirty(p):
    a = git("diff", "--quiet", "HEAD", "--", rel(p)).returncode
    b = git("diff", "--quiet", "--cached", "--", rel(p)).returncode
    return a != 0 or b != 0


def load(p):
    raw = io.open(p, "rb").read()
    eol = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), eol


print("FABLE S-38 flag-word owners section, %s" % ("APPLY" if APPLY else "dry run (no file is written)"))
print("HEAD %s" % git("rev-parse", "--short", "HEAD").stdout.decode().strip())

cdirty = dirty(CONTRACT)
report("G1", not cdirty, "%s is %s" % (rel(CONTRACT), "DIRTY - refused (uncommitted content changes)" if cdirty else "clean"))
_, ceol = load(CONTRACT)
if cdirty:
    src = git("show", "HEAD:" + rel(CONTRACT)).stdout.decode("utf-8").replace("\r\n", "\n")
    print("      staging against the HEAD blob instead, to check the anchors; nothing can be applied")
else:
    src, _ = load(CONTRACT)
print("      line endings kept: %s" % ("CRLF" if ceol == "\r\n" else "LF"))

block = io.open(os.path.join(HERE, "section.txt"), encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n") + "\n"
report("S0", block.split("\n")[0] == HEAD_LINE, "section.txt starts with its heading")
heads = [l for l in block.split("\n") if re.match(r"^#{2,6}\s", l)]
report("S1", heads and all("FABLE" in h for h in heads), "the heading and every subheading carry FABLE (%d heading(s))"
       % len(heads))
lines = src.split("\n")
a14 = [i for i, l in enumerate(lines) if re.match(A_BEFORE, l)]
a15 = [i for i, l in enumerate(lines) if re.match(A_AFTER, l)]
other = [l for l in lines if l.startswith("## 14a.") and l != HEAD_LINE]
report("A1", len(a14) == 1, "anchor '## 14. Unresolved' occurs %d time(s)%s" % (len(a14), " at line %d" % (a14[0] + 1) if a14 else ""))
report("A2", len(a15) == 1, "anchor '## 15. Evidence' occurs %d time(s)%s" % (len(a15), " at line %d" % (a15[0] + 1) if a15 else ""))
report("A3", len(a14) == 1 and len(a15) == 1 and a14[0] < a15[0], "anchors are in order 14 < 15")
report("A4", not other, "no other '## 14a.' heading exists %s" % other)

already = HEAD_LINE in lines
if already:
    staged = src
    print("      E1 ALREADY (the heading is present)")
elif len(a15) == 1:
    i = a15[0]
    pre = lines[:i]
    while pre and not pre[-1].strip():
        pre.pop()
    staged = "\n".join(pre + [""] + block.rstrip("\n").split("\n") + [""] + lines[i:])
    report("E1", True, "14a inserted before line %d (%s)" % (i + 1, lines[i]))
else:
    staged = src
    report("E1", False, "no unique anchor; nothing staged")

links = re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", block)
bad = [l for l in links if not l.startswith("http") and
       not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(CONTRACT), l)))]
report("L1", not bad, "%d relative link(s) in the section resolve from the contract's folder %s" % (len(links), bad))

tables, cur = [], []
for l in block.split("\n") + [""]:
    if l.startswith("|"):
        cur.append(len(re.findall(r"(?<!\\)\|", l)))
    elif cur:
        tables.append(cur)
        cur = []
report("T1", tables and all(len(set(t)) == 1 for t in tables),
       "each of the %d table(s) keeps one cell-separator count per row %s" % (len(tables), [sorted(set(t)) for t in tables]))
outside = [l for l in block.split("\n") if not l.startswith("|") and "|" in l.replace("\\|", "")]
report("T2", not outside, "no '|' outside table rows %s" % outside[:2])

sys.path.insert(0, KIT)
import contract_named_state_census as C  # noqa: E402
before = list(C.state_sections(src))
after = list(C.state_sections(staged))
secs = set(sec for sec, line, fenced in after)
report("C1", not [s for s in secs if s.startswith("14a.")],
       "the census does not read 14a as a state section (state sections: %s)" % sorted(secs))
report("C2", before == after, "the census's state lines are identical before and after (%d lines)" % len(after))
lines2 = staged.split("\n")
pos = [next((i for i, l in enumerate(lines2) if l.startswith(k)), None)
       for k in ("## 14. Unresolved", "## 14a.", "## 15. Evidence")]
report("O1", None not in pos and pos == sorted(pos), "staged order 14 < 14a < 15: %s"
       % [p + 1 if p is not None else None for p in pos])

if APPLY:
    if fails or cdirty:
        print("NOT APPLIED: %d check(s) failed" % fails)
    elif staged == src:
        print("      %s unchanged (ALREADY)" % rel(CONTRACT))
    else:
        io.open(CONTRACT, "wb").write(staged.replace("\n", ceol).encode("utf-8"))
        back, _ = load(CONTRACT)
        report("W", back == staged, "wrote %s" % rel(CONTRACT))
else:
    print("      dry run: contract +%d lines" % (len(staged.split("\n")) - len(src.split("\n"))))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
