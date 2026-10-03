"""apply.py - FABLE, 2026-10-03: stage the S-21 post-result events section (SWE2-AUDIT-SPEC L2 expansion, item 3).

  python apply.py            dry run: check every anchor, show what would change, write nothing
  python apply.py --apply    write the edit (only when every check passes)

Edit:
  E1  07-Combat-Action/CONTRACT-apply-result-to-target.md: insert section.txt as "## 8a." after section 8, before the
      line "## 9. Determinism".

Guards:
  - a page with uncommitted content changes (git diff HEAD, or a staged change) is REFUSED;
  - the anchors "## 8. Script · resource · event interactions" and "## 9. Determinism" must each occur exactly once, in
    that order, and "## 8a." must not exist under another heading;
  - the page's line endings (CRLF or LF) are detected and kept;
  - idempotent: when the section's heading is already present the edit is reported ALREADY and skipped;
  - every relative link in the section must resolve from the contract's folder;
  - the staged page is run through contract_named_state_census's own section parser: 8a must NOT be read as a
    state/types section (it adds no rows to the types denominator);
  - the section carries no '|' outside its table rows' cell syntax (every table row keeps its column count).

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
CONTRACT = os.path.join(DB, "07-Combat-Action", "CONTRACT-apply-result-to-target.md")
HEAD_LINE = "## 8a. The post-result events: the route, the poster, the ring and the message realiser (FABLE, 2026-10-03)"
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


print("FABLE S-21 post-result events section, %s" % ("APPLY" if APPLY else "dry run (no file is written)"))
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
lines = src.split("\n")
a10 = [i for i, l in enumerate(lines) if re.match(r"^## 8\. Script · resource · event interactions\s*$", l)]
a11 = [i for i, l in enumerate(lines) if re.match(r"^## 9\. Determinism\s*$", l)]
other10a = [l for l in lines if l.startswith("## 8a.") and l != HEAD_LINE]
report("A1", len(a10) == 1, "anchor '## 8. Script · resource · event interactions' occurs %d time(s)%s"
       % (len(a10), " at line %d" % (a10[0] + 1) if a10 else ""))
report("A2", len(a11) == 1, "anchor '## 9. Determinism' occurs %d time(s)%s"
       % (len(a11), " at line %d" % (a11[0] + 1) if a11 else ""))
report("A3", len(a10) == 1 and len(a11) == 1 and a10[0] < a11[0], "anchors are in order 8 < 9")
report("A4", not other10a, "no other '## 8a.' heading exists %s" % other10a)

already = HEAD_LINE in lines
if already:
    staged = src
    print("      E1 ALREADY (the heading is present)")
elif len(a11) == 1:
    i = a11[0]
    pre = lines[:i]
    while pre and not pre[-1].strip():
        pre.pop()
    staged = "\n".join(pre + [""] + block.rstrip("\n").split("\n") + [""] + lines[i:])
    report("E1", True, "8a inserted before line %d (%s)" % (i + 1, lines[i]))
else:
    staged = src
    report("E1", False, "no unique anchor; nothing staged")

# links resolve from the contract's folder
links = re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", block)
bad = [l for l in links if not l.startswith("http") and
       not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(CONTRACT), l)))]
report("L1", not bad, "%d relative link(s) in the section resolve from the contract's folder %s" % (len(links), bad))

# table rows keep their column counts
tables, cur = [], []
for l in block.split("\n") + [""]:
    if l.lstrip().startswith("|"):
        cur.append(len(re.findall(r"(?<!\\)\|", l)))
    elif cur:
        tables.append(cur)
        cur = []
report("T1", tables and all(len(set(t)) == 1 for t in tables),
       "each of the %d tables keeps one cell-separator count per row %s" % (len(tables), [sorted(set(t)) for t in tables]))

# the census parser must not read 8a as a state section
sys.path.insert(0, KIT)
import contract_named_state_census as C  # noqa: E402
secs = set(sec for sec, line, fenced in C.state_sections(staged))
s10a = [s for s in secs if s.startswith("8a.")]
report("C1", not s10a, "the census does not read 8a as a state section (state sections: %s)" % sorted(secs))
lines2 = staged.split("\n")
pos = [next((i for i, l in enumerate(lines2) if l.startswith(k)), None)
       for k in ("## 8. Script", "## 8a.", "## 9. Determinism")]
report("O1", None not in pos and pos == sorted(pos), "staged order 8 < 8a < 9: %s" % [p + 1 if p is not None else None
                                                                                       for p in pos])

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
