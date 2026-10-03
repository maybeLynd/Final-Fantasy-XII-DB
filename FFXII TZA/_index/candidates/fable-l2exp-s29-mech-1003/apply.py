"""apply.py - FABLE, 2026-10-03: stage the S-29 item-use section (SWE2-AUDIT-SPEC L2 expansion, item 3).

  python apply.py            dry run: check every anchor, show what would change, write nothing
  python apply.py --apply    write the edit (only when every check passes)

Edit:
  E1  12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md: insert section.txt as "## 7a." after section 7,
      before the line "## 8. Script · resource · event interactions".

Guards:
  - a page with uncommitted content changes (git diff HEAD, or a staged change) is REFUSED;
  - the anchors "## 7. State transitions ..." and "## 8. Script · resource · event interactions" must each occur exactly
    once, in that order, and "## 7a." must not exist under another heading;
  - the page's line endings (CRLF or LF) are detected and kept;
  - idempotent: when the section's heading is already present the edit is reported ALREADY and skipped;
  - every relative link in the section must resolve from the contract's folder;
  - every heading and subheading of the section names FABLE;
  - the staged page is run through contract_named_state_census's own section parser: 7a must NOT be read as a
    state/types section (it adds no rows to the types denominator);
  - every table row keeps its column count.

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
CONTRACT = os.path.join(DB, "12-Items-Equipment-Shops-License", "CONTRACT-inventory-class-storage.md")
HEAD_LINE = "## 7a. Item use: reserve, then consume or refund (FABLE, 2026-10-03)"
A7 = r"^## 7\. State transitions .*$"
A8 = r"^## 8\. Script · resource · event interactions\s*$"
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


print("FABLE S-29 item-use section, %s" % ("APPLY" if APPLY else "dry run (no file is written)"))
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
blines = block.split("\n")
report("S0", blines[0] == HEAD_LINE, "section.txt starts with its heading")
heads = [l for l in blines if l.startswith("#")]
report("S1", heads and all("FABLE" in h for h in heads), "all %d heading(s) of the section name FABLE %s"
       % (len(heads), [h for h in heads if "FABLE" not in h]))
lines = src.split("\n")
a7 = [i for i, l in enumerate(lines) if re.match(A7, l)]
a8 = [i for i, l in enumerate(lines) if re.match(A8, l)]
other7a = [l for l in lines if l.startswith("## 7a.") and l != HEAD_LINE]
report("A1", len(a7) == 1, "anchor '## 7. State transitions ...' occurs %d time(s)%s"
       % (len(a7), " at line %d" % (a7[0] + 1) if a7 else ""))
report("A2", len(a8) == 1, "anchor '## 8. Script · resource · event interactions' occurs %d time(s)%s"
       % (len(a8), " at line %d" % (a8[0] + 1) if a8 else ""))
report("A3", len(a7) == 1 and len(a8) == 1 and a7[0] < a8[0], "anchors are in order 7 < 8")
report("A4", not other7a, "no other '## 7a.' heading exists %s" % other7a)

already = HEAD_LINE in lines
if already:
    staged = src
    print("      E1 ALREADY (the heading is present)")
elif len(a8) == 1:
    i = a8[0]
    pre = lines[:i]
    while pre and not pre[-1].strip():
        pre.pop()
    staged = "\n".join(pre + [""] + block.rstrip("\n").split("\n") + [""] + lines[i:])
    report("E1", True, "7a inserted before line %d (%s)" % (i + 1, lines[i]))
else:
    staged = src
    report("E1", False, "no unique anchor; nothing staged")

links = re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", block)
bad = [l for l in links if not l.startswith("http") and
       not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(CONTRACT), l)))]
report("L1", not bad, "%d relative link(s) in the section resolve from the contract's folder %s" % (len(links), bad))

tables, cur = [], []
for l in blines + [""]:
    if l.startswith("|"):
        cur.append(len(re.findall(r"(?<!\\)\|", l)))
    elif cur:
        tables.append(cur)
        cur = []
report("T1", tables and all(len(set(t)) == 1 for t in tables),
       "each of the %d tables keeps one cell-separator count per row %s" % (len(tables), [sorted(set(t)) for t in tables]))

sys.path.insert(0, KIT)
import contract_named_state_census as C  # noqa: E402
secs = set(sec for sec, line, fenced in C.state_sections(staged))
s7a = [s for s in secs if s.startswith("7a.")]
report("C1", not s7a, "the census does not read 7a as a state section (state sections: %s)" % sorted(secs))
lines2 = staged.split("\n")
pos = [next((i for i, l in enumerate(lines2) if re.match(k, l)), None)
       for k in (A7, r"^## 7a\.", A8)]
report("O1", None not in pos and pos == sorted(pos), "staged order 7 < 7a < 8: %s" % [p + 1 if p is not None else None
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
