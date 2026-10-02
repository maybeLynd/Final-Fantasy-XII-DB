"""apply_by_owner.py OWNER [--apply] - run apply_17render_c.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, FRONTIER, SWE2-EC7, SWE2-DATA, SWE2-FRONTIER.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN and EC7-NN count as SWE2-EC7; a tie including OPUS stays OPUS; a tie without
OPUS is split by the last writer of each edited line.
OPUS: CONTRACT-coast-down-latch.md OPUS 6 + 6 shared; CONTRACT-character-transform-publish.md OPUS 4 + 15 shared /
SWE2-EC7 4; Character-Rendering/character-render-object.md OPUS 2 + 27 shared / SWE2-EC7 21;
Character-Render-Records/the-character-render-record-array.md OPUS 5 + 28 shared / FABLE 10;
Character-Render-Records/render-event-selection-evidence.md OPUS 2 + 10 shared / FABLE 3;
Character-Render-Records/the-bone-trails.md OPUS 1 + 5 shared / SWE2-EC7 6 (tie, stays OPUS);
CONTRACT-render-command-list-and-graphics-handshake.md OPUS 3 + 1 shared / FABLE 2;
Effect-File-Formats/efx-and-efb-effect-containers.md OPUS 5 + 14 shared; Effect-File-Formats/README.md 0 + 1 shared;
Effect-File-Formats/the-element-types-60-74.md 0 + 8 shared / SWE2-FRONTIER 3, FRONTIER 3;
Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md OPUS 11 + 13 shared / SWE2-EC7 19;
Model-And-Motion-Formats/fcp-character-parameter-block.md OPUS 6 + 19 shared / FABLE 6; Model-And-Motion-Formats/
README.md 0 + 5 shared; Model-And-Motion-Formats/fef-and-motion-entries.md OPUS 5 + 11 shared / SWE2-DATA 12;
Model-And-Motion-Formats/frp-object-container.md OPUS 2 + 6 shared / FABLE 3; Model-And-Motion-Formats/
fte-fct-texture-colour-tables.md OPUS 4 / SWE2-DATA 2; Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md
OPUS 6 + 10 shared / FABLE 5, FRONTIER 5; Post-Processing/CONTRACT-ppfx-effect-creation.md OPUS 3;
Post-Processing/ppfx-function-identification.md OPUS 3 + 8 shared / FABLE 3; Post-Processing/the-post-processing-
effect-catalogue.md OPUS 2 + 7 shared / FABLE 9 (tie, stays OPUS); Visual-Tuning-Parameters/README.md 0 + 1 shared;
Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md OPUS 4 + 10 shared / FABLE 8;
Movie-Containers/mh-movie-seek-index.md OPUS 2 + 8 shared / SWE2-EC7 2; Position-To-Scalar/how-a-position-becomes-a-
single-number.md OPUS 1 + 6 shared / FABLE 7 (tie, stays OPUS); Screen-Fade/the-screen-fade-layers-and-the-movie-fade-
schedule.md OPUS 1 + 20 shared / SWE2-EC7 18; Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md
OPUS 2 + 6 shared / FABLE 4.
FABLE: CONTRACT-character-render-object.md FABLE 4 / OPUS 1; Character-Rendering/how-a-character-is-lit.md FABLE 9 /
OPUS 2; Character-Render-Records/how-a-presentation-entry-picks-its-track.md FABLE 6 / OPUS 1;
Character-Render-Records/how-a-character-fades-the-ten-channels.md FABLE 26 / SWE2-EC7 22; Legacy-PS2-GS/the-vif1-vu1-
layer.md FABLE 17 / OPUS 5 + 10 shared; Effect-File-Formats/the-element-types-00-0a.md FABLE 8 / OPUS 2 + 5 shared;
Post-Processing/CONTRACT-post-processing-subsystem.md FABLE 8 / OPUS 2 + 1 shared; Authored-Commands/the-authored-
presentation-command-handlers.md FABLE 30 / OPUS 1 + 4 shared; README.md FABLE 10 / OPUS 2 + 7 shared; and the two tie
pages without OPUS, split by last writer - Character-Render-Records/how-a-status-shows-on-a-character.md (FABLE 13 /
SWE2-EC7 13 / OPUS 2) and Effect-File-Formats/an-effect-element-frame-by-frame.md (FABLE 3 / SWE2-EC7 3 / OPUS 2): every
edited line on both was last written by FABLE (6040ed83b, 995219992, 08bc4504f, da4a15f31, b9fcc96b8; 7990379e5).
SWE2-EC7: CONTRACT-authored-command-ramp-channels.md 24 / OPUS 6 + 15 shared; CONTRACT-render-record-pool-lifecycle.md
45 / OPUS 7 + 12 shared; Character-Render-Records/the-rig-of-seventeen-controllers.md 23 / OPUS 1 + 1 shared;
Character-Render-Records/the-staged-look-command.md 14 / OPUS 1; Render-Command-List/the-ordered-render-command-list.md
39 / OPUS 8 + 24 shared; Graphics-Thread-Handshake/the-shared-command-state-word.md 28 / OPUS 4 + 20 shared;
Gi-Render-Commands/gi-render-command-family.md 35 / OPUS 1 + 16 shared; Effect-File-Formats/effect-element-type-
dispatch.md 78 / OPUS 4 + 21 shared; Effect-File-Formats/the-menu-effect-registry.md 23 / OPUS 2 + 9 shared;
Model-And-Motion-Formats/adm-add-motion-tables.md 13 / OPUS 2 + 7 shared; Model-And-Motion-Formats/the-pose-sequencer.md
3 / OPUS 1; Scripted-Camera/how-a-camera-reaches-the-renderer.md 13 / OPUS 1 + 3 shared; Scripted-Camera/the-scripted-
camera-player.md 26 / OPUS 3 + 17 shared.
SWE2-DATA: Effect-File-Formats/effect-mesh-records-kind-54.md SWE2-DATA 4 / OPUS 0 + 3 shared;
Model-And-Motion-Formats/fdm-and-for-entries.md SWE2-DATA 6 / OPUS 1.
No overlay carrier among the pages (scope_guard.py 2026-10-02, all 52 pages), so SWE2-FRONTIER takes nothing.
Not held (OPUS-HELD is empty): the OPUS pages dirty in the working tree carry OPUS's own uncommitted work only - the
"Interior citations ... (OPUS, 2026-10-02" sections on CONTRACT-character-transform-publish.md, CONTRACT-render-command-
list-and-graphics-handshake.md, fcp-character-parameter-block.md, fte-fct-texture-colour-tables.md,
mh-movie-seek-index.md and ppfx-function-identification.md, and parts A/B's applied readiness strikes on the others -
and no OLD string here touches a dirty line (git blame: no uncommitted line among the edited ones) or a line part A or
part B edits, applied or pending (in-memory overlap check). OPUS-CLOUD-F-INTERIOR-W23-1002, which held the two contracts
for part A, is DONE. No other lane's ACTIVE task edits or audits an OPUS page here: the three README pages are named by
OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929 and AUTO-REPAIR-ORACLE-REQ-AUDITSPEC-SD7-0930 only through the README
basename collision.
Guard on the OPUS pages (2026-10-02): WARN add-motion-skeleton-and-high-model-tables.md (peer commit 24-72 h); BLOCK
every other one - dirty with OPUS's own work as above, finished peer commits (SWE2-CONTRACT 85718f321, SWE2-DATA
cd6bd7f58, 85a2ae3ee on the 60-74 and oscillator pages, SWE2-AUDIT-SPEC 058c93e21 on frp; 24-72 h: SWE2-FRONTIER
54e8a524e, FABLE 7903502f7, SWE2-STRUCT 65f4854dd, SWE2-DATA 29436f1ad, FABLE 9dad2a1ad / 6c817c026) and the README
basename collision. Re-run the guard, and publish parts A/B's OPUS work first, before --apply.
No census TSV is edited. Regenerate requests: SWE2-STRUCT, character-render-record-accesses.tsv (2,872 rows / 499
functions / 351 displacements against the page's 3,381 / 545 / 368 generation); FABLE, members/vif1-gif-tags.tsv
(75 tags in 45 builders against the page's corrected "at least 61" tag-carrying builders).
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages): FABLE last wrote the render-object
"pooled element's 3" line (7424a725a), the bone-trail "that sentence is an inference" line (2f3f4b5f7), the 60-74
"eight-group 0x65 setup" line (4e32dd8df), the skeleton page's "Still open" bullet (ba69c0caa), the frp "none reads the
container's parts" and "only partly read" lines (57589e164, b129b7d79) and the catalogue's three cfg / 006DB9A0 lines
(ab1a50f7f); SWE2-EC7 the render-object 0x740-walk lines (0f7160ab3) and the mh "then three one-argument invokes" lines
(44893cd7f); SWE2-DATA the record-array UQ-197 line (d5261fb4e), the fcp "Sections 5 and 11-17" note (a99867d19), the
fef census-check line (7d8111938) and @FMW row (bbcaeb95a), the Model README @FMN/@FMW line (bbcaeb95a) and the four
fte-fct lines (f67421173, fa547cea9); FRONTIER the Model README "36 members" line and the oscillator's member-count line
(973ac1c70) and the screen fade's per-helper-bodies line (cbc007bd3). Every other edited line on those pages was last
written by an OPUS or an unprefixed (shared) commit.
"""
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_17render_c as base  # noqa: E402

F = "17-Presentation-Rendering/"
OWNERS = {
    "FABLE": {
        F + "CONTRACT-character-render-object.md",
        F + "Character-Rendering/how-a-character-is-lit.md",
        F + "Character-Render-Records/how-a-presentation-entry-picks-its-track.md",
        F + "Character-Render-Records/how-a-character-fades-the-ten-channels.md",
        F + "Character-Render-Records/how-a-status-shows-on-a-character.md",
        F + "Legacy-PS2-GS/the-vif1-vu1-layer.md",
        F + "Effect-File-Formats/the-element-types-00-0a.md",
        F + "Effect-File-Formats/an-effect-element-frame-by-frame.md",
        F + "Post-Processing/CONTRACT-post-processing-subsystem.md",
        F + "Authored-Commands/the-authored-presentation-command-handlers.md",
        F + "README.md",
    },
    "SWE2-EC7": {
        F + "CONTRACT-authored-command-ramp-channels.md",
        F + "CONTRACT-render-record-pool-lifecycle.md",
        F + "Character-Render-Records/the-rig-of-seventeen-controllers.md",
        F + "Character-Render-Records/the-staged-look-command.md",
        F + "Render-Command-List/the-ordered-render-command-list.md",
        F + "Graphics-Thread-Handshake/the-shared-command-state-word.md",
        F + "Gi-Render-Commands/gi-render-command-family.md",
        F + "Effect-File-Formats/effect-element-type-dispatch.md",
        F + "Effect-File-Formats/the-menu-effect-registry.md",
        F + "Model-And-Motion-Formats/adm-add-motion-tables.md",
        F + "Model-And-Motion-Formats/the-pose-sequencer.md",
        F + "Scripted-Camera/how-a-camera-reaches-the-renderer.md",
        F + "Scripted-Camera/the-scripted-camera-player.md",
    },
    "SWE2-DATA": {
        F + "Effect-File-Formats/effect-mesh-records-kind-54.md",
        F + "Model-And-Motion-Formats/fdm-and-for-entries.md",
    },
    # No OPUS page is held for part C (docstring); kept so the call shape matches parts A and B.
    # Held 2026-10-02 12:05 (OPUS): FABLE applied its routed part-A edit on this page and has not published it yet;
    # OPUS edits wait so FABLE's commit carries only FABLE's hunk.
    "OPUS-HELD": {"17-Presentation-Rendering/Character-Rendering/character-render-object.md"},
    # No overlay carrier among the pages (scope_guard.py 2026-10-02).
    "SWE2-FRONTIER": set(),
}
LINE_OWNERS = {
    "FABLE": ("      - the pooled element's `3` (a likely expiry count)",
              "an opacity - but that sentence is an inference",
              "closed by `00431770` - the eight-group 0x65 setup",
              "  - **Still open:** which models the ids name",
              "and none reads the container's parts;",
              "through command `0x09` (that invoker is only partly read)",
              "**Which `cfg` float carries the focus distance is not",
              "`006DB9A0`'s body is not read here.",
              "- who fills `cfg`, and in particular which float"),
    "SWE2-EC7": ("each link. The `0x740` stride is the character-render record",
                 "sub-record, then three\none-argument invokes"),
    "SWE2-DATA": ("*(closed — the register row is WITHDRAWN.)*",
                  "Sections 5 and 11–17 are authored-only",
                  "  fef_motion_entry_census.py` — 12 checks",
                  "| `@FMW` | 111 | 45 | motion weight/blend record",
                  "the weapon/treasure command names, `@FMN`/`@FMW` the 1:1 name/blend pair",
                  "                                       allocator 00537AA0 (invariant, 1,951/1,951)",
                  "Census over `1,044` files / `1,951` header records:",
                  "values are `0x400` (1618), `0x200` (318), `0x40` (35)",
                  "`00504D20` (7 bytes; called from the status-look code"),
    "FRONTIER": ("parameter-install API (36 members).",
                 "`members/model-oscillator-subsystem.tsv` lists all 36 members",
                 "The per-helper bodies (`002DED60`, `00360D70`/`00360E50`"),
}


# Holds lifted 2026-10-02 (OPUS): these pages' holds are lifted; their held edits on other identities' lines go to them.
OWNERS["OPUS-HELD"] = set(OWNERS.get("OPUS-HELD", set())) - set(['17-Presentation-Rendering/Character-Rendering/character-render-object.md'])
LINE_OWNERS['FABLE'] = tuple(LINE_OWNERS.get('FABLE', ())) + ("      - the pooled element's `3` (a likely expiry count) is not followed here.",)
LINE_OWNERS['SWE2-EC7'] = tuple(LINE_OWNERS.get('SWE2-EC7', ())) + ('each link. The `0x740` stride is the character-render record — the walk is over ',)


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
