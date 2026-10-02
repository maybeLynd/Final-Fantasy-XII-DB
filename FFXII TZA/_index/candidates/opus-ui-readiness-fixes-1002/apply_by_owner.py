"""apply_by_owner.py OWNER [--apply] - run apply_16ui.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, FRONTIER, SWE2-EC7, SWE2-FRONTIER, SWE2-DATA.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN and the bare "EC7" prefix count as SWE2-EC7; FRONTIER and SWE2-FRONTIER are
separate identities; a tie including OPUS stays OPUS.
OPUS: README.md OPUS 1 + 3 shared / FABLE 4; CONTRACT-text-control-codes-and-dyngeo-draw.md OPUS 5 + 2 shared;
the-selection-the-menu-publishes.md OPUS 3 + 10 shared / FABLE 4; Widget-Object-Model/CONTRACT-widget-object.md OPUS 10
+ 25 shared / SWE2-EC7 23; Widget-Object-Model/the-widget-constructor-and-object-sizes.md OPUS 4 + 25 shared / SWE2-EC7
25; Widget-Object-Model/starting-a-widget-animation-and-the-millisecond-that-becomes-frames.md OPUS 2 + 18 shared;
Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md OPUS 2 + 2 shared / SWE2-STRUCT 3;
Request-Router/ui-request-router.md OPUS 8 + 33 shared / FABLE 10; Text-And-Number-Rendering/the-text-control-code-
language.md OPUS 5 + 13 shared / SWE2-EC7 15; Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md
OPUS 8 + 50 shared / FABLE 8; Text-And-Number-Rendering/font-data-kerning-and-expansion.md OPUS 3 + 13 shared /
SWE2-EC7 13 / SWE2-DATA 10; Dynamic-Geometry-Instances/dyngeo-instance-family.md OPUS 2 + 12 shared / SWE2-EC7 10;
Battle-Hud/the-battle-hud-layout-readers.md OPUS 2 + 9 shared / FABLE 3; Map-Screens/the-map-screens-and-their-shared-
map-data.md OPUS 3 + 22 shared / FABLE 24; Menu-Screen-Atlas/the-menu-screen-atlas.md 12 shared / FABLE 5 / FRONTIER 5;
Unlabelled-Panes/the-unlabelled-procedures.md OPUS 2 + 10 shared; Shared-Dialogs/the-shared-dialog-widgets.md OPUS 2 +
10 shared; Shop-Screens/the-shop-screens.md OPUS 3 + 12 shared; License-Board-View/the-license-board-screen-widgets.md
OPUS 2 + 10 shared; Gambit-Screens/the-gambit-screens.md OPUS 3 + 12 shared; Handbook/the-handbook-screen.md OPUS 2 +
18 shared.
SWE2-EC7: Widget-Object-Model/the-widget-message-protocol.md SWE2-EC7 79 / OPUS 4 + 17 shared / FABLE 22;
Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md SWE2-EC7 91 / OPUS 2 + 21 shared;
Config-Screen/the-config-screen-and-what-a-setting-change-runs.md SWE2-EC7 45 / OPUS 1 + 13 shared;
License-Board-View/the-license-board-grid-build-and-its-change-sweep.md SWE2-EC7 14 / OPUS 2 + 10 shared;
Message-Windows/the-message-window-layout-readers.md SWE2-EC7 13 / OPUS 1 + 11 shared; Quest-List/the-quest-list-
screen.md SWE2-EC7 23 / OPUS 2 + 9 shared; Handbook/the-handbooks-monster-viewer.md SWE2-EC7 3 / OPUS 1.
FABLE: CONTRACT-ui-request-router.md FABLE 5 / OPUS 1.
No overlay carrier and no dirty page among them (scope_guard.py and git status, 2026-10-02).
Held: none at drafting. the-selection-the-menu-publishes.md was named by the ACTIVE board task
OPUS-REQ-AUDITSPEC-MENUSEL-INTERIOR-1001 (SWE2-AUDIT-SPEC, spot-checking its interior citations) at the first guard run;
the task closed (DONE 10:16 UTC) before this was finished, so the page's edits are OPUS's again. OPUS-HELD is kept as an
empty owner so the call shape matches the other folders. Re-run the guard before --apply.
Guard on the OPUS pages (2026-10-02): README.md BLOCKs on board-name collisions only (README basename); the title-asset,
kerning, battle-HUD, map, shop, licence-widget, gambit and handbook pages BLOCK on peer commits under 24 h only (no
ACTIVE task editing them); ui-request-router.md BLOCKed on OPUS-REQ-AUDITSPEC-RECORD-EIGHT-PASS6-SIGNATURES-1001, which
edits the false-positive dispositions file, not the page (and is DONE); the others are WARN or CLEAR. None is dirty.
No census TSV is edited. The section 3.2 count items (CC-1..CC-24) are not edited; the ones that need a TSV changed are
SWE2-DATA regenerate requests, not hand edits.
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages): FRONTIER last wrote the size page's
002B6DB0 row (cfeb75211), the selection page's id-2-arm and menu-state lines (e513a6379, e83f64b9c), the sort bar's
id-12 line and the unlabelled banner (246391ed5), the licence widgets' iterator and sweep rows (25a0dac17) and the
gambit list's arm-18 row (4a14fdecd); FABLE the router's spattack lines and shared-arms line (115e631ce), the DynGeo K and
slot lines (8819fe0f5, 60bebe5cd), the 9-tag table line (2abfbd761), the map page's two 003C2200 lines and banner
(2c8b1c81a, 01dbb1424, 9dfcc6633), the atlas banner and the README's atlas and monster-viewer tags (e347c0d1f,
14918b36e); SWE2-EC7 the alignment-arm line (061188d9d) and the map jump-table line (322a29ea8); SWE2-FRONTIER the kern
subtree line (0cdb6009a); SWE2-DATA the kern-find line and the .fex line (cf5d6545d, 9aa62d505). Every other edited line
on the OPUS-led pages was last written by an OPUS or an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_16ui as base  # noqa: E402

F = "16-UI/"
OWNERS = {
    "SWE2-EC7": {
        F + "Widget-Object-Model/the-widget-message-protocol.md",
        F + "Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md",
        F + "Config-Screen/the-config-screen-and-what-a-setting-change-runs.md",
        F + "License-Board-View/the-license-board-grid-build-and-its-change-sweep.md",
        F + "Message-Windows/the-message-window-layout-readers.md",
        F + "Quest-List/the-quest-list-screen.md",
        F + "Handbook/the-handbooks-monster-viewer.md",
    },
    "FABLE": {
        F + "CONTRACT-ui-request-router.md",
    },
    # No OPUS-led page is held at drafting (see above); kept so `apply_by_owner.py OPUS-HELD` runs and reports 0.
    "OPUS-HELD": set(),
}
LINE_OWNERS = {
    "FRONTIER": ("selector resolve `001EDEC0`",
                 "is the command-confirm path:",
                 "`00272180` + the `01E0C1D8`/`01E0C1DC` state cells",
                 "the five sort modes; each walks the parent's",
                 "loop over `+0x55A` rows/`+0x554` cols",
                 "| sweep wrapper — tail `0055BFF0` |",
                 "calls the `+0xC8` editor child's first vtable slot",
                 "**Status:** PARTIAL — the 25 atlas rows"),
    "FABLE": ("In the generic widgets these ids reach only shared arms",
              "The router's own arm `0028E970` releases and rebuilds",
              "That arm releases the widget at `0209BE80 + 0x10FB0`",
              "`0x760`-byte one there. Verb",
              "K is `16/9` (`008C5B38`) unless the `01F82D18` object",
              "and the four shared slots 4, 5, 6",
              "`out` is the FIRST BYTE of entry `tag[2] & 0x1FF`",
              "releases the slot (`003C2200`) and destroys the page.",
              "**16** (resource batch complete) releases the slot",
              "**PARTIAL.** Read: which code is which screen,",
              "**PARTIAL.** This is an atlas, not a reading.",
              "**DOCUMENTED, tier 1.** The bestiary's 3D monster",
              "**PARTIAL, tier 1.** Track map, location map and world map"),
    "SWE2-EC7": ("returns `(word[+0x94] - xmm1)/2 + byte[+0x99]` — the left/center/right",
                 "six-arm jump table at `02ED4310`"),
    "SWE2-FRONTIER": ("`001FDC02`), and the second arm repeats the walk off `001FC420`",),
    "SWE2-DATA": ("(structurally unreachable — see §3).",
                  "in practice.) What a `.fex` key names is not established"),
}


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
