"""apply.py - FABLE, 2026-10-03: stage the S-01 section "4a. The archive mount and the startup latch".

  python apply.py            dry run: check every anchor, show what would change, write nothing
  python apply.py --apply    write the edit (only when every check passes)

Edit:
  E1  00-Engine-Core-Runtime/CONTRACT-boot-fixups.md: insert section.txt after section 4, before the line "## 5. State".

Guards:
  - a page with uncommitted content changes (git diff HEAD, or a staged change) is REFUSED; the anchors are then
    checked against the HEAD blob so the dry run still says whether the edit would land;
  - the anchors "## 4. Preconditions" and "## 5. State" must occur exactly once and in order;
  - the new invariant ids I6..I9 must not already be defined in the page;
  - the page's line endings (CRLF or LF) are detected and kept;
  - idempotent: if the section heading is already present the edit is reported ALREADY and skipped;
  - the staged page is run through contract_named_state_census's own section parser: 4a must NOT be read as a
    Types/State section, and the census rows of the page must be identical before and after;
  - the section's link to check_s01.py must resolve from the contract's folder.
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
CONTRACT = os.path.join(DB, "00-Engine-Core-Runtime", "CONTRACT-boot-fixups.md")
APPLY = "--apply" in sys.argv
MARK = "## 4a. The archive mount and the startup latch"
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


print("FABLE S-01 section 4a, %s" % ("APPLY" if APPLY else "dry run (no file is written)"))
print("HEAD %s" % git("rev-parse", "--short", "HEAD").stdout.decode().strip())

cdirty = dirty(CONTRACT)
report("G1", not cdirty, "%s is %s" % (rel(CONTRACT), "DIRTY - refused (uncommitted content changes)" if cdirty
                                        else "clean"))
_, eol = load(CONTRACT)
if cdirty:
    src = git("show", "HEAD:" + rel(CONTRACT)).stdout.decode("utf-8").replace("\r\n", "\n")
    print("      staging against the HEAD blob instead, to check the anchors; nothing can be applied")
    print("      working-tree diff: %s" % git("diff", "--shortstat", "HEAD", "--", rel(CONTRACT)).stdout.decode().strip())
else:
    src, eol = load(CONTRACT)
print("      line endings kept: %s" % ("CRLF" if eol == "\r\n" else "LF"))

lines = src.split("\n")
pos = []
for i, h in enumerate((r"^## 4\. Preconditions", r"^## 5\. State\s*$")):
    hits = [k for k, l in enumerate(lines) if re.match(h, l)]
    pos.append(hits[0] if len(hits) == 1 else None)
    report("A%d" % (i + 1), len(hits) == 1, "anchor %s occurs %d time(s)%s" % (
        h, len(hits), " at line %d" % (hits[0] + 1) if len(hits) == 1 else ""))
report("A3", None not in pos and pos[0] < pos[1], "anchors in order 4 < 5: %s" % [p and p + 1 for p in pos])

ids = [i for i in ("I6", "I7", "I8", "I9") if re.search(r"\*\*%s\b" % i, src)]
report("I1", not ids or MARK in src, "the new invariant ids I6..I9 are not already defined in the page: %s" % ids)

block = io.open(os.path.join(HERE, "section.txt"), encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")
report("S1", block.startswith(MARK) and "FABLE, 2026-10-03" in block.split("\n")[0],
       "section heading carries the marker and 'FABLE, 2026-10-03'")
print("      section.txt: %d lines" % len(block.split("\n")))

if MARK in src:
    staged, msg = src, "ALREADY present - skipped"
elif pos[1] is not None:
    i = pos[1]
    pre = lines[:i]
    while pre and not pre[-1].strip():
        pre.pop()
    staged = "\n".join(pre + [""] + block.split("\n") + [""] + lines[i:])
    msg = "inserted before line %d (%s)" % (i + 1, lines[i])
else:
    staged, msg = None, "no anchor"
report("E1", staged is not None, "4a %s" % msg)
staged = staged or src

# E3 (neighbour gate, 2026-10-03): 4a cites its subject, slot 2 `0017CEB0`, by entry, and that body calls the
# Application-layer `0017D6B0`. The edge is part of I6's claim, so it is accounted for in the page's own crossing
# section, as the last bullet of "## Cross-subsystem neighbours", in that section's bullet style.
CROSS_HEAD = "## Cross-subsystem neighbours"
CROSS_LINE = ("- **Application — SERVICE (1 edge; FABLE, 2026-10-03, §4a).** 1 outbound: page-cited `0017CEB0` "
              "(slot 2, the archive mount) calls the Application bootstrap body `0017D6B0` as its fifth call "
              "(`0017CEB0` + 0x50, I6), `0017CEB0` -> `0017D6B0`. The mount is this page's subject; what "
              "`0017D6B0` builds is open (§4a).")
sl = staged.split("\n")
hh = [k for k, l in enumerate(sl) if l.startswith(CROSS_HEAD)]
if CROSS_LINE in staged:
    report("E3", True, "Application crossing bullet ALREADY present - skipped")
elif len(hh) == 1:
    k = hh[0] + 1
    while k < len(sl) and not re.match(r"^#{1,3} ", sl[k]):
        k += 1
    j = k
    while j > hh[0] + 1 and not sl[j - 1].strip():
        j -= 1
    staged = "\n".join(sl[:j] + [CROSS_LINE] + sl[j:])
    report("E3", True, "Application crossing bullet inserted as the last line of the crossing section (before line %d: %s)"
           % (k + 1, sl[k][:60] if k < len(sl) else "EOF"))
else:
    report("E3", False, "crossing heading %r occurs %d time(s) (needs 1)" % (CROSS_HEAD, len(hh)))

sl = staged.split("\n")
p4 = next((k for k, l in enumerate(sl) if l.startswith("## 4. Preconditions")), None)
p4a = next((k for k, l in enumerate(sl) if l.startswith(MARK)), None)
p5 = next((k for k, l in enumerate(sl) if re.match(r"^## 5\. State\s*$", l)), None)
report("E2", None not in (p4, p4a, p5) and p4 < p4a < p5, "staged order 4 < 4a < 5: %s" % [p4, p4a, p5])

link = "../_index/candidates/fable-l2exp-s01-mech-1003/check_s01.py"
report("L1", link in block and os.path.exists(os.path.normpath(os.path.join(os.path.dirname(CONTRACT), link))),
       "the section's check link resolves from the contract's folder")

sys.path.insert(0, KIT)
try:
    import contract_named_state_census as C  # noqa: E402

    def rows(t):
        return [(s, l) for s, l, f in C.state_sections(t)]
    before, after = rows(src), rows(staged)
    secs = sorted(set(s for s, _ in after))
    report("C1", not any(s.startswith("4a") for s in secs), "the census does not read 4a as a state section; "
           "state sections: %s" % secs)
    report("C2", before == after, "census rows unchanged by the insert (%d rows)" % len(after))
except Exception as ex:  # the census module is the gate's own; failing to load it is a failure
    report("C1", False, "contract_named_state_census not loadable: %r" % ex)

if APPLY:
    if fails:
        print("NOT APPLIED: %d check(s) failed" % fails)
    elif staged == src:
        print("      %s unchanged (ALREADY)" % rel(CONTRACT))
    else:
        io.open(CONTRACT, "wb").write(staged.replace("\n", eol).encode("utf-8"))
        back, _ = load(CONTRACT)
        report("W", back == staged, "wrote %s" % rel(CONTRACT))
else:
    print("      dry run: contract +%d lines" % (len(staged.split("\n")) - len(src.split("\n"))))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
