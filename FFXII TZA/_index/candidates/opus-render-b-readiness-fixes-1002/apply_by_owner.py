"""apply_by_owner.py OWNER [--apply] - run apply_17render_b.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, FRONTIER, SWE2-EC7, SWE2-DATA, SWE2-FRONTIER.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN and EC7-NN count as SWE2-EC7; a tie including OPUS stays OPUS.
OPUS: Legacy-PS2-GS/texture-mip-local-memory-budget.md OPUS 3 + 10 shared / SWE2-EC7 5;
Effect-File-Formats/efx-and-efb-effect-containers.md OPUS 5 + 14 shared; Effect-File-Formats/the-element-types-80-97.md
0 + 5 shared / FRONTIER 4; Effect-File-Formats/the-element-types-60-74.md 0 + 8 shared / FRONTIER 3, SWE2-FRONTIER 3;
Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md 0 + 5 shared / FRONTIER 3, SWE2-FRONTIER 3;
Model-And-Motion-Formats/README.md 0 + 5 shared; Model-And-Motion-Formats/ftr-node-table.md OPUS 6 / SWE2-DATA 3;
Model-And-Motion-Formats/frp-object-container.md OPUS 2 + 6 shared / FABLE 3;
Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md OPUS 6 + 10 shared / FABLE 5, FRONTIER 5;
Post-Processing/the-post-processing-effect-catalogue.md OPUS 2 + 7 shared / FABLE 9 (tie, stays OPUS);
Post-Processing/CONTRACT-ppfx-effect-creation.md OPUS 3; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-
assets.md OPUS 4 + 10 shared / FABLE 8; Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md OPUS 1 + 20
shared / SWE2-EC7 18; Position-To-Scalar/how-a-position-becomes-a-single-number.md OPUS 1 + 6 shared / FABLE 7 (tie,
stays OPUS); Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md OPUS 2 + 6 shared / FABLE 4.
FABLE: Legacy-PS2-GS/the-vif1-vu1-layer.md FABLE 17 / OPUS 5 + 10 shared; Effect-File-Formats/the-element-types-00-0a.md
FABLE 8 / OPUS 2 + 5 shared; Post-Processing/CONTRACT-post-processing-subsystem.md FABLE 8 / OPUS 2 + 1 shared;
Character-Render-Records/how-a-character-fades-the-ten-channels.md FABLE 26 / SWE2-EC7 22 / OPUS 2 + 1 shared.
SWE2-EC7: Gi-Render-Commands/gi-render-command-family.md 35 / OPUS 1 + 16 shared; Effect-File-Formats/effect-element-
type-dispatch.md 78 / OPUS 4 + 21 shared; Effect-File-Formats/the-menu-effect-registry.md 23 / OPUS 2 + 9 shared;
Model-And-Motion-Formats/the-pose-sequencer.md 3 / OPUS 1; Render-Command-List/the-ordered-render-command-list.md 39 /
OPUS 8 + 24 shared; Scripted-Camera/the-scripted-camera-player.md 26 / OPUS 3 + 17 shared.
SWE2-DATA: Model-And-Motion-Formats/fdm-and-for-entries.md SWE2-DATA 6 / OPUS 1.
Held (OPUS-HELD): six OPUS-led pages are dirty in the working tree with OPUS's own uncommitted work only - the
"Interior citations ... OPUS" sections on fcp-character-parameter-block.md, fte-fct-texture-colour-tables.md,
mh-movie-seek-index.md and ppfx-function-identification.md, and part A's readiness edits on fef-and-motion-entries.md and
the-bone-trails.md. Their edits wait until that work publishes; no OLD string here overlaps those sections. On the held
pages the last writers of some edited lines are other identities, and those edits go to them once the hold lifts:
FABLE the bone-trail line "queues one render command" (2f3f4b5f7); SWE2-DATA the two fte-fct header lines (fa547cea9)
and the fef @FMW header lines (bbcaeb95a, 7d8111938); SWE2-EC7 the mh "initializes the trailing" line (44893cd7f).
No overlay carrier among the pages (scope_guard.py 2026-10-02). No other lane's ACTIVE task edits an OPUS page here: the
Model-And-Motion-Formats/README.md BLOCK names OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929 through a README basename
collision (that README is not in its worksheet), and its listed pages efx-and-efb, frp and the reflected-parameter page
carry no unregistered residue it is still editing (its checkpoint, 2026-10-02).
Guard on the OPUS pages (2026-10-02): CLEAR CONTRACT-ppfx-effect-creation.md and the aspect-fit page; WARN
texture-mip, the 40-42 element types, the catalogue, the reflected-parameter page, the screen fade and
position-to-scalar; BLOCK efx-and-efb, 80-97, 60-74, ftr-node-table and the oscillator page on peer commits under 24 h
(finished sweeps: SWE2-CONTRACT 85718f321, SWE2-DATA cd6bd7f58, 85a2ae3ee, SWE2-AUDIT-SPEC 058c93e21 on frp) and the
README on the basename collision above. Re-run the guard before --apply.
No census TSV is edited.
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages that are not held): FABLE last wrote the
oscillator's "While it is set" line and its wind-globals row (6facc53bc), the catalogue's step-3 row (ab1a50f7f) and
1,172-handles line (67c17a2e9), and position-to-scalar's z-range line (41f35c8b6); FRONTIER the 80-97 step-cluster lines
and family table row (7f6928f4f, e23db2ab1), the 60-74 PRNG row and three 4-track-group lines (3009f5187, e23db2ab1),
the 40-42 0xA0 row (cfb647186) and the oscillator's 01FD4A90 and 0040AA20 rows (973ac1c70); SWE2-DATA the ftr-node-table
+0x38 line (f67421173); SWE2-EC7 the screen fade's 002DEE50, 002DEDE0 and 0037DEA0 lines (c9b292d80, cc713205a,
9faff14ac). Every other edited line on those pages was last written by an OPUS or an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_17render_b as base  # noqa: E402

F = "17-Presentation-Rendering/"
OWNERS = {
    "FABLE": {
        F + "Legacy-PS2-GS/the-vif1-vu1-layer.md",
        F + "Effect-File-Formats/the-element-types-00-0a.md",
        F + "Post-Processing/CONTRACT-post-processing-subsystem.md",
        F + "Character-Render-Records/how-a-character-fades-the-ten-channels.md",
    },
    "SWE2-EC7": {
        F + "Gi-Render-Commands/gi-render-command-family.md",
        F + "Effect-File-Formats/effect-element-type-dispatch.md",
        F + "Effect-File-Formats/the-menu-effect-registry.md",
        F + "Model-And-Motion-Formats/the-pose-sequencer.md",
        F + "Render-Command-List/the-ordered-render-command-list.md",
        F + "Scripted-Camera/the-scripted-camera-player.md",
    },
    "SWE2-DATA": {
        F + "Model-And-Motion-Formats/fdm-and-for-entries.md",
    },
    # Held 2026-10-02 (OPUS): dirty with OPUS's own uncommitted F-interior sections and part-A readiness edits; apply
    # after those publish (the line owners named in the docstring then take their lines).
    "OPUS-HELD": {
        F + "Character-Render-Records/the-bone-trails.md",
        F + "Model-And-Motion-Formats/fef-and-motion-entries.md",
        F + "Model-And-Motion-Formats/fcp-character-parameter-block.md",
        F + "Model-And-Motion-Formats/fte-fct-texture-colour-tables.md",
        F + "Movie-Containers/mh-movie-seek-index.md",
        F + "Post-Processing/ppfx-function-identification.md",
    },
    # No overlay carrier among the pages (scope_guard.py 2026-10-02); kept so the call shape matches other folders.
    "SWE2-FRONTIER": set(),
}
LINE_OWNERS = {
    "FABLE": ("12). While it is set, section 3's mode byte",
              "| `02CA4380`–`02CA439C` | `.data` f32 ×4-ish |",
              "| `&cfg+0x9C`: its contents land in two 16-byte stores",
              "That registers **1,172 handles** in all",
              "map z between the constants `1024.0`"),
    "FRONTIER": ("- `0x80`/`0x82`/`0x83` — identical step `0044CC10`",
                 "  `003A6E60` + `003D8E50` + PRNG + tail `0045B640`",
                 "+ `00431770` init(s) + one resource store",
                 "called inside the step bodies of `0x0A`",
                 "| `0xA0` | step `00460B80`",
                 "of **nine** 4-track groups `+0x1C0`–`+0x460`",
                 "  stride `+0x1C0`–`+0x3F0` plus 12 singles",
                 "start for `0x73`/`0x74` then group runs",
                 "| `01FD4A90` | `.data` ptr |",
                 "| `0040AA20` / `0040AAD0` | param setup |"),
    "SWE2-DATA": ("+0x38  u32      tailU16",),
    "SWE2-EC7": ("follow-up. The write is the layer's armed/visible flag",
                 "`002DEDE0` (80 B) maintains the fade-layer singleton",
                 "with `+0xF0` bit 8 clear"),
}


# Holds lifted 2026-10-02 (OPUS): these pages' holds are lifted; their held edits on other identities' lines go to them.
OWNERS["OPUS-HELD"] = set(OWNERS.get("OPUS-HELD", set())) - set(['17-Presentation-Rendering/Character-Render-Records/the-bone-trails.md', '17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md', '17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md', '17-Presentation-Rendering/Model-And-Motion-Formats/fte-fct-texture-colour-tables.md', '17-Presentation-Rendering/Movie-Containers/mh-movie-seek-index.md', '17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md'])
LINE_OWNERS['FABLE'] = tuple(LINE_OWNERS.get('FABLE', ())) + ('  queues one render command of `0x488` bytes with the VU1 microprogram',)
LINE_OWNERS['SWE2-DATA'] = tuple(LINE_OWNERS.get('SWE2-DATA', ())) + ("+0x00  '@FTE', u32 kind = 0, u32 entryLen, u32 0\n", "+0x00  '@FCT', u32 kind = 0, u32 entryLen, u32 0\n", "Header `{'@FMW', kind 0, entryLen, u32 +0x0C = 0}`, `char[0x10]` name at `+0x10`")
LINE_OWNERS['SWE2-EC7'] = tuple(LINE_OWNERS.get('SWE2-EC7', ())) + ('zero, `0067A9B0(rcx + 0x678)`\ninitializes the trailing\n',)


def owner_of(e):
    if e[0] in OWNERS["OPUS-HELD"]:
        return "OPUS-HELD"
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
