"""apply_by_owner.py OWNER [--apply] - run apply_17render_a.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, SWE2-EC7, SWE2-DATA, SWE2-STRUCT,
SWE2-FRONTIER.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN counts as SWE2-EC7; a tie including OPUS stays OPUS.
OPUS: Model-And-Motion-Formats/fef-and-motion-entries.md OPUS 5 + 11 shared / SWE2-DATA 12;
Character-Rendering/character-render-object.md OPUS 2 + 27 shared / SWE2-EC7 21 / FABLE 10; CONTRACT-coast-down-latch.md
OPUS 6 + 6 shared; Character-Render-Records/the-character-render-record-array.md OPUS 5 + 28 shared / FABLE 10 /
SWE2-STRUCT 9; Character-Render-Records/render-event-selection-evidence.md OPUS 2 + 10 shared / FABLE 3;
Character-Render-Records/the-bone-trails.md OPUS 1 + 5 shared / SWE2-EC7 6 (tie, stays OPUS);
CONTRACT-character-transform-publish.md OPUS 4 + 15 shared / SWE2-EC7 4; CONTRACT-render-command-list-and-graphics-
handshake.md OPUS 3 + 1 shared / FABLE 2.
FABLE: Authored-Commands/the-authored-presentation-command-handlers.md FABLE 30 / OPUS 1 + 4 shared;
Character-Rendering/how-a-character-is-lit.md FABLE 9 / SWE2-EC7 7 / OPUS 2; Character-Render-Records/how-a-character-
fades-the-ten-channels.md FABLE 26 / SWE2-EC7 22 / OPUS 2 + 1 shared; README.md FABLE 10 / OPUS 2 + 7 shared.
SWE2-EC7: CONTRACT-authored-command-ramp-channels.md SWE2-EC7 24 / OPUS 6 + 15 shared; CONTRACT-render-record-pool-
lifecycle.md SWE2-EC7 45 / OPUS 7 + 12 shared; Character-Render-Records/the-staged-look-command.md SWE2-EC7 14 / FABLE 6;
Render-Command-List/the-ordered-render-command-list.md SWE2-EC7 39 / OPUS 8 + 24 shared; Gi-Render-Commands/gi-render-
command-family.md SWE2-EC7 35 / OPUS 1 + 16 shared; Character-Render-Records/how-a-status-shows-on-a-character.md
SWE2-EC7 13 / FABLE 13 / OPUS 2 - a tie without OPUS, split by last writer: the line-269 edit is FABLE's (LINE_OWNERS),
the SWE2-EC7-72 section's lines are SWE2-EC7's.
No overlay carrier and no dirty page among them (scope_guard.py and git status, 2026-10-02).
Held (OPUS-HELD): CONTRACT-character-transform-publish.md and CONTRACT-render-command-list-and-graphics-handshake.md are
targets of OPUS's own ACTIVE cloud task OPUS-CLOUD-F-INTERIOR-W23-1002, so a publish touching them would loop on the
claim. Apply after that task's F-interior ingest. No other lane's ACTIVE task names an OPUS page here.
Guard on the OPUS pages (2026-10-02): fef-and-motion-entries.md BLOCKs on a peer commit under 24 h only (SWE2-DATA
cd6bd7f58, no ACTIVE task editing it); the transform-publish and command-list contracts are CLEAR; the others are WARN.
Re-run the guard before --apply.
No census TSV is edited.
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages): SWE2-DATA last wrote the fef selector
pool line (e45bbb909) and the op-0x34 allocator-defaults line (1fdad99d2); SWE2-EC7 the 0042EF90 interior line of the
render-object page (0f7160ab3) and the three 0051BC10 lines of the bone-trail page (206a8b214); FABLE the render-object
page's "back to back" line (b11e0a0ad); SWE2-STRUCT the record-array page's field-tier lines: +0x114 (e2ee3491e),
+0x6 / +0xA (186e99a7c), +0x66D / +0x674 (78a0f661e), +0x2F2 (48b392677), +0x734 (e2ee3491e) and +0x640 (79748e6fd).
Every other edited line on the OPUS-led pages was last written by an OPUS or an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_17render_a as base  # noqa: E402

F = "17-Presentation-Rendering/"
OWNERS = {
    "FABLE": {
        F + "Authored-Commands/the-authored-presentation-command-handlers.md",
        F + "Character-Rendering/how-a-character-is-lit.md",
        F + "Character-Render-Records/how-a-character-fades-the-ten-channels.md",
        F + "README.md",
    },
    "SWE2-EC7": {
        F + "CONTRACT-authored-command-ramp-channels.md",
        F + "CONTRACT-render-record-pool-lifecycle.md",
        F + "Character-Render-Records/the-staged-look-command.md",
        F + "Render-Command-List/the-ordered-render-command-list.md",
        F + "Gi-Render-Commands/gi-render-command-family.md",
        F + "Character-Render-Records/how-a-status-shows-on-a-character.md",
    },
    # Held 2026-10-02 (OPUS): OPUS's own ACTIVE cloud F task OPUS-CLOUD-F-INTERIOR-W23-1002 holds these pages, so a
    # publish touching them would loop on the claim. Apply after that task's F-interior ingest.
    "OPUS-HELD": {
        F + "CONTRACT-character-transform-publish.md",
        F + "CONTRACT-render-command-list-and-graphics-handshake.md",
    },
    # No overlay carrier among the pages (scope_guard.py 2026-10-02); kept so the call shape matches other folders.
    "SWE2-FRONTIER": set(),
}
LINE_OWNERS = {
    "SWE2-DATA": ("at `[02B3EF28]` (pool init",
                  "`+0x24..+0x38` = `1.0`"),
    "SWE2-EC7": ("`[rip+0x1e97f63]` (`02095210`)",
                 "run: `cl * 0x3C0` into the `02A48F40`",
                 "`02A48F04` decrements",
                 "doubly-linked chain (head/tail at `02A48EF4`"),
    "FABLE": ("`this + 0x690`. `003829D0` calls the two",
              "sets a two-bit field of the render record"),
    "SWE2-STRUCT": ("**`+0x114` `animPhaseHandle`**",
                    "Fourth tier (array-index fields)",
                    "**`+0xA` `altLinkedIndex`**",
                    "byte bitfield with bit 1 gating",
                    "bit 2 reset by `ResetDefaults`. **`+0x674`",
                    "  re-resolve helper `0016D6A0`",
                    "**`+0x734` `kindTunedFloat`**",
                    "**`+0x640` `bindingResultDword`**"),
}


# Holds lifted 2026-10-02 (OPUS): these pages' holds are lifted; their held edits on other identities' lines go to them.
OWNERS["OPUS-HELD"] = set(OWNERS.get("OPUS-HELD", set())) - set(['17-Presentation-Rendering/CONTRACT-character-transform-publish.md', '17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md'])


def owner_of(e):
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
