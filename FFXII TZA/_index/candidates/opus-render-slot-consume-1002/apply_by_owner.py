"""apply_by_owner.py OWNER [--apply] - run apply_render_slot.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, SWE2-EC7.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN and EC7-NN count as SWE2-EC7; a tie including OPUS stays OPUS.
OPUS: Character-Render-Records/the-character-render-record-array.md OPUS 5 + 28 shared / FABLE 10, SWE2-STRUCT 9,
SWE2-EC7 4 + EC7 2, FRONTIER 2, SWE2-DATA 1.
SWE2-EC7: CONTRACT-render-record-pool-lifecycle.md SWE2-EC7 38 + EC7 7 = 45 / OPUS 7 + 12 shared = 19, FRONTIER 6,
FABLE 2, SWE2-CONTRACT 1, SWE2-STRUCT 1. The EC7 majority is its appended interior-citation batches; every line
edited here (sections 2, 4, 7, 10, 13, 13a, 15 and the EXP-109 fold) was last written by an OPUS or an unprefixed
(shared) commit (5aef7e216, 95b75ae51, 268cc5ade, 5df5afb7d, 8e2fb06c1), so the board may reassign it to OPUS; until
then the 20 edits are a request to SWE2-EC7.
Not touched: CONTRACT-character-render-object.md (FABLE 4 / OPUS 1) describes a different object (the 001F4EC9
constructor's), and Character-Rendering/character-render-object.md carries no statement these packets reach.
Dirty-page note: the-character-render-record-array.md is dirty with OPUS's own uncommitted readiness strikes only
(opus-render-a-readiness-fixes-1002: the coast-down code line, the "more than four" patch list, the two dirty-bit pass
lines and the 00426480 / 003B6890 member rows). No OLD string here overlaps those lines, so the page stays OPUS; the
guard reports BLOCK (dirty) until that work publishes, so --apply waits for it or rides with it.
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led page): none - every edited line was last
written by an unprefixed (shared) commit (46b6f1cb4, f837e0154, 8f980795a).
Guard (scope_guard.py from FFXII TZA/, 2026-10-02): BLOCK the-character-render-record-array.md (dirty - OPUS's own
work above; inbox mentions SWE2-EC7.md and SWE2-FRONTIER.md are historical, and the READY
AUDITSEM-CONTRA-FRONTIER-DIRTYBITS targets section 14, which no edit here touches); WARN
CONTRACT-render-record-pool-lifecycle.md (peer commit 65f4854dd, SWE2-STRUCT, 24-72 h; FABLE.md inbox mention is the
2026-09 citation notice). Re-run the guard before --apply.
No census TSV and no _types file is edited; the type changes are a request to SWE2-STRUCT (consumption-notes.md).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_render_slot as base  # noqa: E402

F = "17-Presentation-Rendering/"
OWNERS = {
    "SWE2-EC7": {
        F + "CONTRACT-render-record-pool-lifecycle.md",
    },
}
# No edited line on the OPUS-led page was last written by another identity (blame 2026-10-02).
LINE_OWNERS = {}


# Superseded 2026-10-02 12:10 (OPUS): FABLE corrected these three spots itself after this draft (the id-first claim
# on the array page's line 100 and the field-map line, and the 00429291 row). They are not applied by anyone.
SUPERSEDED = ("when the slot is not in use, and every consumer tests that first.",
              "  +0x000  i16   id                 -1 when the slot is free; every consumer tests this first",
              "| `00429291` → `0041F730` | same |")


def owner_of(e):
    if e[1].startswith(SUPERSEDED):
        return "SUPERSEDED"
    for o, prefixes in LINE_OWNERS.items():
        if e[1].startswith(prefixes):
            return o
    for o, pages in OWNERS.items():
        if e[0] in pages:
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
