"""apply_by_owner.py OWNER [--apply] - run apply_99residual.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, FRONTIER, SWE2-EC7, SWE2-DATA, SWE2-FRONTIER.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN and EC7-NN count as SWE2-EC7; a tie including OPUS stays OPUS.
OPUS: README.md OPUS 12 + 9 shared; the-unresolved-158.md OPUS 2 + 36 shared / FABLE 4; Glyph-Run-Rendering/
how-a-line-of-text-becomes-glyph-quads.md OPUS 2 + 34 shared / SWE2-EC7 22; choosing-the-render-target OPUS 3 + 14
shared / SWE2-EC7 8; painting-a-line-of-text OPUS 2 + 12 shared / SWE2-EC7 10; the-font-painters-public-api OPUS 2 + 10
shared / SWE2-EC7 8; Cutscene-Asset-Slots/cutscene-name-slots OPUS 4 + 28 shared / SWE2-EC7 19; Dead-Nine-Patch-
Renderer/the-box-renderer OPUS 4 + 18 shared; Unlisted-Code/referenced-code OPUS 6 + 14 shared; the-bodies-the-list-cuts-
short OPUS 6 + 1 shared; the-code-the-function-list-does-not-contain OPUS 17 + 9 shared; Unowned-Code-Census OPUS 3 + 20
shared / SWE2-EC7 6; drawing-one-coloured-rectangle OPUS 2 + 9 shared / SWE2-EC7 11 (tie, stays OPUS); measuring-text
OPUS 5 + 9 shared; the-second-icon-drawer OPUS 2 + 10 shared / SWE2-EC7 10; the-widget-background OPUS 2 + 8 shared;
the-widget-tree-draw-pass OPUS 3 + 12 shared.
SWE2-EC7: Glyph-Run-Rendering/drawing-a-line-character-by-character.md 20 / OPUS 2 + 14 shared;
the-blinking-icon-and-its-atlas.md 20 / OPUS 2 + 15 shared; the-nine-patch-window-frame.md 13 / OPUS 2 + 9 shared.
FABLE: Glyph-Run-Rendering/the-shared-drawing-context.md FABLE 10 / OPUS 4 + 5 shared.
Held (OPUS-HELD): Glyph-Run-Rendering/the-text-element-dispatch-table.md (OPUS 5 + 16 shared) is dirty with FABLE's
uncommitted "Interior citations ... (FABLE, 2026-10-02, cloud-drafted)" section and named by FABLE's ACTIVE
FABLE-CLOUD-F-W2-1002 / FABLE-PUB-CLOUDINT-W2-1002, which edit it; Largest-Unclassified-Code/the-largest-unclassified-
functions.md (OPUS 5 + 17 shared / FABLE 16) is dirty with OPUS's pass-22 rename (opus-pass22-repair-1002) and an
uncommitted SD-140 narrowing at its +0x1A-array paragraph whose producer is not an OPUS applier. No OLD string here
overlaps either page's dirty hunks. Once the hold lifts, FABLE takes the dispatch page's lines 198, 221, 228, 370-371
and 657 (668e0216b, 42a4cf588) and the largest-unclassified page's tag-record line (3ad6c2981); SWE2-DATA takes its
SD-123 line (71af93479).
Two OPUS-led pages are dirty with OPUS's own uncommitted work only and stay OPUS: the cutscene page (pass-22 renames
inside its 2026-10-01 OPUS interior-citation table, opus-pass22-repair-1002) and the box-renderer page (its new
"Interior citations ... (OPUS, 2026-10-02, cloud-drafted)" section). No OLD string here overlaps those hunks.
No overlay carrier among the pages (scope_guard.py 2026-10-02). README's BLOCK names other lanes' tasks through a README
basename collision and READY tasks only; the glyph-quads page's BLOCK is a READY review task and a FABLE interior-citation
commit under 24 h, not an ACTIVE task editing it.
Guard (2026-10-02): CLEAR the font painter API, referenced-code, the nine-patch frame and the widget background; WARN
CBC, the render-target chooser, painting, the shared context, the cuts-short and function-list-does-not-contain pages,
the census, the-unresolved-158, the rectangle, measuring, the second icon drawer and the widget tree; BLOCK README,
glyph quads, the dispatch table, the cutscene page, the box renderer, the largest-unclassified page and the blinking icon.
Re-run the guard before --apply.
No census TSV is edited.
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages that are not held): SWE2-FRONTIER last
wrote the glyph-quads subtree rows for 003647E0, 00365FD0 and 00364210 and the painting page's +0x9C pair and 001E7A20
row (0cdb6009a); FABLE the widget-tree SD-102 line (6c817c026), the cutscene page's "still has no caller" line
(160e4fe9d), the-unresolved-158's crossref-backlog line (f8e0716db) and the glyph-quads UQ-367 superseded line
(b090a5cbf); SWE2-EC7 the box renderer's 002D6990 line (8661520d9), the function-list page's two continuation lines
(9680fea9b), the census's 0041E000 and 0041E1D0 lines (442eb5209, be46e51ef), the API's 0017F8E0 line (be08c2af1)
and the cutscene page's 001ED130 and 0024AF50 lines (e4950fd34, b6ab9c0cb); SWE2-DATA the measuring page's open-list
line (71af93479); FRONTIER the function-list page's NOT YET line (6ba4b6a91). Every other edited line on those pages
was last written by an OPUS or an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import apply_99residual as base  # noqa: E402

F = "99-Unresolved-Residual/"
OWNERS = {
    "FABLE": {
        F + "Glyph-Run-Rendering/the-shared-drawing-context.md",
    },
    "SWE2-EC7": {
        F + "Glyph-Run-Rendering/drawing-a-line-character-by-character.md",
        F + "the-blinking-icon-and-its-atlas.md",
        F + "the-nine-patch-window-frame.md",
    },
    # Held 2026-10-02 (OPUS): the dispatch page is dirty with FABLE's ACTIVE interior-citation publication, the
    # largest-unclassified page with an uncommitted SD-140 narrowing whose producer is not OPUS. Apply after both
    # publish (the line owners named in the docstring then take their lines).
    "OPUS-HELD": {
        F + "Glyph-Run-Rendering/the-text-element-dispatch-table.md",
        F + "Largest-Unclassified-Code/the-largest-unclassified-functions.md",
    },
    # No overlay carrier among the pages (scope_guard.py 2026-10-02); kept so the call shape matches other folders.
    "SWE2-FRONTIER": set(),
}
LINE_OWNERS = {
    "SWE2-FRONTIER": ("opcode 1 copies `[rdi+0x37]`",
                      "| `00364210` (367 B) | the span clipper",
                      "with `r8d`/`edx` range checks",
                      "`dword[rdx+0x9C]` element count read",
                      "| `001E7A20` (610 B) |"),
    "FABLE": ("`002DAF30` loads four rows from",
              "Static; and the renderer itself still has no caller.",
              "backlog. They are listed in the TSV",
              "the population is carried by 99-Unresolved-Residual"),
    "SWE2-EC7": ("`002D6990` (783 B) is the dead",
                 "**163 of those blocks as continuations",
                 "**163 blocks - 3,797 bytes",
                 "`0041E000` (461 B) is a call-free",
                 "`0041E1D0` (348 B) is a call-free",
                 "`0x80220040` flag, `01EFFAF0` vtable.",
                 "`0017F8E0` — 50 B, 4 callers",
                 "names: `edx = movsx(00265270())`",
                 "`0024AF50` (368 B) is a cutscene-slot body"),
    "SWE2-DATA": ("What states `0`, `1`, `4`, `5` and `7`",),
    "FRONTIER": ("larger bands\n      stay NOT YET.",),
}


# Holds lifted 2026-10-02 (OPUS): these pages' holds are lifted; their held edits on other identities' lines go to them.
OWNERS["OPUS-HELD"] = set(OWNERS.get("OPUS-HELD", set())) - set(['99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md'])
LINE_OWNERS['FABLE'] = tuple(LINE_OWNERS.get('FABLE', ())) + ("`002ABEC0`'s `rcx` is **not the widget**. Its nine callers pass", 'every embedded base the nine callers use', 'Of twelve slots, five are filled by\nfour distinct bodies.', '001EDEC0  cmp dword ptr [01F82E38], 0   ; scale mode active?\n', 'So the predicate says: **"1 unless the 2x scale mode is on, unsuppressed,')


def owner_of(e):
    if e[0] in OWNERS["OPUS-HELD"]:
        return "OPUS-HELD"
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
