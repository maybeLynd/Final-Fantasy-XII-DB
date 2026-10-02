"""apply_by_owner.py OWNER [--apply] - run apply_26pkfl.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, SWE2-FRONTIER, SWE2-CONTRACT.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN counts as SWE2-EC7; FRONTIER and SWE2-FRONTIER are separate identities; a tie
including OPUS stays OPUS.
OPUS: README.md 2 shared; Container/pkfl-package-container.md 1 + 11 shared / SWE2-CONTRACT 2.
No overlay carrier among these pages and neither is dirty (scope_guard.py, git status, 2026-10-02).
Held: none. The only open board task naming either page is OPUS-RE-READINESS-26-VALUES-1002, this package's own.
Re-run the guard first.
Guard on the OPUS pages (2026-10-02): BLOCKs are the README basename collisions and SWE2-CONTRACT's finished pass-22
sweep de4492e21 (the container page); neither is a reason to hold. No census TSV is edited: the frozen
Tools/work/formats/pkfl-container-census.tsv (four-byte word indices, 27 of 10,314 rows agree with the pair reading) is
reported to SWE2-DATA for a re-freeze instead.
LINE_OWNERS (git blame --porcelain on every edited line): every edited line was last written by an unprefixed (shared)
commit - 46b6f1cb4, b5fe121ef or 8bd8b26f0 - so none moves to another identity.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_26pkfl as base  # noqa: E402

OWNERS = {
    # No page led by another identity, no held OPUS page and no overlay carrier at drafting (see above); kept so every
    # owner runs and reports.
    "FABLE": set(),
    "SWE2-CONTRACT": set(),
    "OPUS-HELD": set(),
    "SWE2-FRONTIER": set(),
}
LINE_OWNERS = {}


def owner_of(e):
    for o, pages in OWNERS.items():
        if e[0] in pages:
            return o
    for o, prefixes in LINE_OWNERS.items():
        if e[1].startswith(prefixes):
            return o
    return "OPUS"


def main():
    owner = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "OPUS"
    if owner in ("OPUS", *OWNERS, *LINE_OWNERS):
        keep = [e for e in base.EDITS if owner_of(e) == owner]
    else:
        print("unknown owner", owner); print("FAILS 1"); return 1
    print("owner", owner, "edits", len(keep), "of", len(base.EDITS))
    base.EDITS = keep
    return base.main()


if __name__ == "__main__":
    sys.exit(main())
