"""apply.py - FABLE staged correction applier (2026-10-03, on SWE2-AUDIT-SPEC's L2 expansion). S-06, I-4.

Default is a DRY RUN: it reports what it would change and writes nothing. --apply writes the page.
- Anchored: every edit's OLD text (or insertion anchor) must occur EXACTLY ONCE on the page, or the edit FAILs.
- Refuses a dirty page: if `git status --porcelain` lists the page, --apply refuses; a dry run then
  measures against the HEAD blob instead of the working tree and says so.
- Keeps the page's line endings (CRLF or LF) and writes bytes back unchanged elsewhere.
- Idempotent: an edit whose full replacement (or inserted block) is already present is SKIPPED.
- Prints FAILS N last.
Edit kinds: ("strike", label, old, new)  -> "~~old~~ new STAMP"
            ("insert", label, anchor, block) -> block inserted immediately after anchor
"""
import os
import subprocess
import sys

STAMP = "*(corrected 2026-10-03, FABLE, on SWE2-AUDIT-SPEC's L2 expansion)*"
PAGE = "00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md"

EDITS = [
    ("strike", "I-4 lead sentence: the table is ten of 27 constants, not every operand",
     "Every RIP-relative operand of an\n`addss`/`subss`/`movss`/`mulss` in the body, resolved through the correct section:",
     "The body has **481** RIP-relative operands of an `addss`/`subss`/`movss`/`mulss`, resolved through the correct "
     "section: **249** load or store `.bss` setting cells, **6** load or store two file-backed `.data` setting cells "
     "(`01DFE194`, `01DFE1AC`), and **226** read `.rdata` constants with **27** distinct values. The table prints ten "
     "of the 27, and the cut is not a reference threshold (`1.0` x8, `-0.02` x3 and `0.002` x3 are not printed); the "
     "full set follows it:"),
    ("insert", "I-4 full .rdata constant set after the table",
     "| 0.001 | 13 | | 0.03 | 3 |\n",
     "\n**The full `.rdata` set** *(added 2026-10-03, FABLE, on SWE2-AUDIT-SPEC's L2 expansion; "
     "[`check_s06.py`](../../_index/candidates/fable-l2exp-s06-1003/check_s06.py))*: the ten above, plus `1.0` x8, "
     "`-0.02` x3, `0.002` x3, `0.005` x2, `-0.005` x2, `0.005556` x2 (`009002B8`, f32 of 1/180; `subss` `001D2B59` and "
     "`addss` `001D2B6E`, both in id 104's arm `001D2B4D`), and one reference each to `-0.001`, `-0.1`, `-0.5`, `0.5`, "
     "`0.0722`, `0.2126`, `0.7152`, `0.99`, `1.01`, `10.0` and `48.0`: **27 values, 226 references**, of which the "
     "printed ten carry 195.\n"),
    ("strike", "I-4 1.0 x11 note: three of the eleven are a .data setting cell",
     "*One discrepancy with the page, recorded rather than\nsmoothed: it ranks `1.0` at 8 references and this scan finds "
     "**11**. The scan covers\n`addss`/`subss`/`movss`/`mulss`; the page does not state its instruction set, so the two are\n"
     "measuring slightly different things and the difference is method, not error.*",
     "The page's `1.0` x8 is right for the constant: this scan's 11 are 8 `.rdata` references plus 3 to the `.data` "
     "setting cell `01DFE1AC` (id 169's *SSS Diffuse a*, image value `1.0`), which is a setting the arm steps, not a "
     "step. The same holds for falsification pass 1's `0.5` x4: one `.rdata` reference (`01CEBB70`) and 3 to the "
     "setting cell `01DFE194` (id 111, image value `0.5`)."),
    ("strike", "I-4 runtime-step arm counts: one count per arm, and the two .data-cell arms re-attributed",
     "**56 arms step by exactly 0.01**, then 0.1 (7), 0.02 (7), 0.001 (6), 0.05 (5),\n1.0 (4), **0.005 (4)**, 0.03 (3) "
     "and **0.005556 (2)**.",
     "**55 arms step by exactly 0.01**, then 0.02 (8), 0.1 (7), 0.001 (6), 0.05 (5), 0.03 (3), 1.0 (2), **0.005 (2)** "
     "and **0.005556 (1)**: 89 arms. The earlier figures were the replay's own tally, which counts an arm once per "
     "signed value written, so the six arms seen writing both +k and -k (`001D1867`, `001D1ED4`, `001D1F0D`, "
     "`001D2A38`, `001D2B4D`, `001D2B83`) counted twice. Two arms do not start from zero, because they step "
     "file-backed `.data` setting cells the fixture leaves at their image values: id 111 (`001D2881`) steps "
     "`01DFE194` (0.5) by 0.02, and id 169 (`001D29CC`) steps `01DFE1AC` (1.0) by 0.1. The replay therefore "
     "recorded 0.52 / 0.5 and 1.1 / 1.0 for them, and those are not steps."),
]

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
    for kind, label, old, new in EDITS:
        if kind == "strike":
            rep = replacement(old, new)
            if work.count(rep) == 1:
                print("SKIP %s: already applied" % label)
                continue
            n = work.count(old)
            if n != 1:
                print("FAIL %s: OLD text occurs %d times (needs exactly 1)" % (label, n))
                fails += 1
                continue
            work = work.replace(old, rep, 1)
            delta = len(rep) - len(old)
        else:
            if work.count(old + new) == 1:
                print("SKIP %s: already applied" % label)
                continue
            n = work.count(old)
            if n != 1:
                print("FAIL %s: anchor occurs %d times (needs exactly 1)" % (label, n))
                fails += 1
                continue
            work = work.replace(old, old + new, 1)
            delta = len(new)
        changed += 1
        print("PASS %s: anchored once, would %s (+%d chars)" % (label, "write" if do_apply else "change", delta))
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
