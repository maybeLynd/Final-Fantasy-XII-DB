"""apply.py - FABLE staged correction applier (2026-10-03, on SWE2-AUDIT-SPEC's L2 expansion).

Default is a DRY RUN: it reports what it would change and writes nothing. --apply writes the page.
- Anchored: every edit's OLD text must occur EXACTLY ONCE on the page, or the edit FAILs.
- Refuses a dirty page: if `git status --porcelain` lists the page, --apply refuses; a dry run then
  measures against the HEAD blob instead of the working tree and says so.
- Keeps the page's line endings (CRLF or LF) and writes bytes back unchanged elsewhere.
- Idempotent: an edit whose full replacement is already present is SKIPPED (already applied).
- Prints FAILS N last.
"""
import os
import subprocess
import sys

STAMP = "*(corrected 2026-10-03, FABLE, on SWE2-AUDIT-SPEC's L2 expansion)*"
PAGE = '15-Input/Binding-Profiles/CONTRACT-binding-profiles.md'   # repo-relative path under Database/FFXII TZA/
EDITS = [
    ('E1 section 5 read row: axis-invert bytes are in the pointee',
     '`01F7FFE0+8/+9` (axis invert)',
     '`[01F7FFE0]+0x08` / `[01F7FFE0]+0x09` (axis invert: `InputManager +0x08` / `+0x09`, reached through the 8-byte pointer cell `01F7FFE0`; reads `0019740F`, `0019751A`, `0019752E`, `001975CB`, `001975DF`, each after a qword load of the cell)'),
    ('E2 section 5 written row: the stick-touched flag is in the pointee',
     '`01F7FFE0+0x38` (stick-touched flag)',
     '`[01F7FFE0]+0x38` (stick-touched flag, `InputManager +0x38`: `00197444` loads the pointer cell, `0019744B` stores 1 through it; no `.text` instruction references the static cell `01F80018`)'),
]   # list of (label, old, new_text); the page gets "~~old~~ new_text STAMP"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
REL = "Database/FFXII TZA/" + PAGE
ABS = os.path.join(ROOT, *REL.split("/"))


def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True).stdout


def replacement(old, new):
    return "~~" + old + "~~ " + new + " " + STAMP


def main():
    do_apply = "--apply" in sys.argv
    fails = 0
    dirty = git("status", "--porcelain", "--", REL).decode("utf-8", "replace").strip()
    if dirty:
        print("NOTE page is dirty in the shared tree: %s" % dirty)
        if do_apply:
            print("FAIL refusing --apply on a dirty page")
            print("FAILS 1")
            return 1
        raw = git("show", "HEAD:" + REL)
        src = "HEAD blob"
    else:
        raw = open(ABS, "rb").read()
        src = "working tree (clean)"
    head = git("rev-parse", "--short", "HEAD").decode().strip()
    print("page %s  source %s  HEAD %s  mode %s" % (REL, src, head, "APPLY" if do_apply else "dry-run"))
    text = raw.decode("utf-8")
    crlf = "\r\n" in text
    nl = "\r\n" if crlf else "\n"
    work = text.replace("\r\n", "\n") if crlf else text
    print("line endings %s" % ("CRLF" if crlf else "LF"))
    changed = 0
    for label, old, new in EDITS:
        rep = replacement(old, new)
        n_old = work.count(old)
        n_rep = work.count(rep)
        if n_rep == 1:
            print("SKIP %s: already applied" % label)
            continue
        if n_old != 1:
            print("FAIL %s: OLD text occurs %d times (needs exactly 1)" % (label, n_old))
            fails += 1
            continue
        work = work.replace(old, rep, 1)
        changed += 1
        print("PASS %s: anchored once, would %s (+%d chars)" % (label, "write" if do_apply else "replace", len(rep) - len(old)))
    out = work.replace("\n", nl) if crlf else work
    if do_apply and changed and not fails:
        with open(ABS, "wb") as f:
            f.write(out.encode("utf-8"))
        print("WROTE %s (%d edits)" % (REL, changed))
    elif do_apply and fails:
        print("not written: failures above")
    print("edits %d, to change %d" % (len(EDITS), changed))
    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
