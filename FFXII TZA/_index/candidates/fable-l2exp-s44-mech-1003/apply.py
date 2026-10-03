"""apply.py - FABLE, 2026-10-03: stage S-44's language code -> id section (SWE2-AUDIT-SPEC L2 expansion, item 3).

  python apply.py            dry run: check every anchor, show what would change, write nothing
  python apply.py --apply    write the edit (only when every check passes)

Edit:
  E1  19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md: insert section.txt
      ("## 8a. Language code to id ...") after section 8, before the line "## 9. Determinism".

Guards:
  - a page with uncommitted content changes (git diff HEAD, or a staged index difference) is REFUSED;
  - both anchors ("## 8. Script", "## 9. Determinism") must occur exactly once and in order;
  - the page's line endings (CRLF or LF) are detected and kept;
  - idempotent: when the section heading is already present the edit is reported ALREADY and skipped;
  - the staged page is run through contract_named_state_census's own section parser: 8a must NOT be read as a
    Types/State section, so the S-44 types denominator is unchanged (the two cells 8a names, 0x01E02814 and the
    FileCache's +0x1B8..+0x1BA, are routed for declaration instead - README);
  - every relative link the section adds must resolve from the contract's folder.

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
CONTRACT = os.path.join(DB, "19-Save-Load-Settings", "Game-Settings-Config", "CONTRACT-game-setting-config.md")
APPLY = "--apply" in sys.argv
MARKER = "## 8a. Language code to id"
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


print("FABLE S-44 language code -> id section, %s" % ("APPLY" if APPLY else "dry run (no file is written)"))
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

lines = src.split("\n")
pos = []
for k, h in enumerate((r"^## 8\. Script", r"^## 9\. Determinism\s*$"), 1):
    hits = [i for i, l in enumerate(lines) if re.match(h, l)]
    pos.append(hits[0] if len(hits) == 1 else None)
    report("A%d" % k, len(hits) == 1, "anchor %s occurs %d time(s)%s" % (h, len(hits), " at line %d" % (hits[0] + 1) if len(hits) == 1 else ""))
report("A3", None not in pos and pos[0] < pos[1], "anchors in order 8 < 9: %s" % [p and p + 1 for p in pos])

block = io.open(os.path.join(HERE, "section.txt"), encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")
report("S1", block.startswith(MARKER) and "FABLE, 2026-10-03" in block.split("\n")[0],
       "section.txt starts with the 8a heading and names FABLE, 2026-10-03")

if MARKER in src:
    staged, msg = src, "ALREADY present - skipped"
    report("E1", True, "8a %s" % msg)
elif None in pos:
    staged = src
    report("E1", False, "8a not staged: anchor missing")
else:
    i = pos[1]
    pre = lines[:i]
    if pre and pre[-1].strip():
        pre = pre + [""]
    staged = "\n".join(pre + block.split("\n") + [""] + lines[i:])
    report("E1", True, "8a inserted before line %d (%s)" % (i + 1, lines[i][:40]))

sl = staged.split("\n")
order = [next((i for i, l in enumerate(sl) if l.startswith(k)), None) for k in ("## 8. Script", MARKER, "## 9. Determinism")]
report("E2", None not in order and order == sorted(order), "staged order 8 < 8a < 9: %s" % [o and o + 1 for o in order])

cdir = os.path.dirname(CONTRACT)
links = re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", block)
bad = [l for l in links if not l.startswith("http") and not os.path.exists(os.path.normpath(os.path.join(cdir, l)))]
report("L1", not bad, "%d relative link(s) in 8a resolve from the contract's folder%s" % (len(links), (": missing %s" % bad) if bad else ""))

sys.path.insert(0, KIT)
try:
    import contract_named_state_census as C  # noqa: E402

    def secs(t):
        return sorted(set(s for s, _, _ in C.state_sections(t)))

    before, after = secs(src), secs(staged)
    report("C1", not [s for s in after if s.startswith("8a")], "the census does not read 8a as a Types/State section")
    report("C2", before == after, "the census's state sections are unchanged by the insert: %s" % after)
except Exception as e:  # the census module is the gate's own; failing to load it is a failure, not a skip
    report("C0", False, "contract_named_state_census could not run: %r" % (e,))

if APPLY:
    if fails:
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
