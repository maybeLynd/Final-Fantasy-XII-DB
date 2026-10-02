# Reconstruction readiness — `FFXII TZA/17-Presentation-Rendering/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-17-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`34861cfd`); no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. |

**Counts:**
- **60 `.md` pages read in full** (36,542 lines): the category `README.md`, 4 sub-folder READMEs, 6 `CONTRACT-*.md` pages and 49 system pages. **60 `.tsv` checks**, layout or count only, over 26 member files named in Appendix A.
- **12 parts** (§1), with **395 entry-point rows**.
- **255** self-stated open gaps (S-) and **231** structural gaps (G-) (§2).
- **471 contradictions** (§3):
  - **193 value-changing** (§3.1), all "page-text only - needs local check". **33** have a favoured side settled by a dated correction on the pages (2 of them only in part: ET.CV-1, MF.CV-3); **160** have no favoured side.
  - **82 count/census disagreements** that change no runtime behaviour (§3.2).
  - **196 stale / banner items** (§3.3): **44** front-matter / body-banner / `README.md`-tag disagreements, **100** stale "not read / open" claims that another page or a later dated section answers, **52** corrected or struck claims still repeated unstruck elsewhere.
- **Rating: NOT YET** overall (§4). **READY:** `@FRP` and `@FEF` containers, the coast-down seam. **MOSTLY:** 33 sub-parts. **NOT YET:** the D3D11 primitive-renderer device interface, VU1 microprograms, the render command classes' execute bodies, the character render object's draw, the rig controllers' per-frame output, `@FRM` motion data, the oscillator VU stages, the PPFX effect library (byte-faithful), effect element types `0xA1`-`0xAA`, the movie (WebM) playback path, and the frame order across the category.

| part | S | G | CV (favoured) | CC | CS (banner / stale / repeated) |
|---|---:|---:|---:|---:|---|
| AC authored commands, ramps, coast-down | 17 | 15 | 13 (2) | 5 | 14 (3 / 7 / 4) |
| RO pool, render object, transform publish, lighting | 31 | 21 | 18 (1) | 7 | 16 (3 / 8 / 5) |
| RA record array, render events, focus, track pick | 17 | 12 | 14 (2) | 4 | 11 (4 / 4 / 3) |
| RG rig, fades, status looks, trails, staged look | 36 | 28 | 15 (0) | 5 | 21 (4 / 15 / 2) |
| CL command list, graphics handshake | 11 | 15 | 16 (5) | 9 | 12 (3 / 5 / 4) |
| GP Gi commands, PS2 GS/VIF | 21 | 20 | 17 (9) | 8 | 16 (3 / 7 / 6) |
| EF effect containers, dispatch, element update | 22 | 19 | 22 (4) | 6 | 16 (3 / 8 / 5) |
| ET element types, kind 0x54, menu registry, layers | 18 | 20 | 10 (1) | 6 | 15 (5 / 6 / 4) |
| MF add-motion, ADM, FCP, FDM/FOR | 16 | 20 | 10 (4) | 5 | 19 (4 / 11 / 4) |
| MM FEF, FRP, FTE/FCT, FTR, oscillator, pose | 13 | 15 | 22 (2) | 8 | 9 (3 / 4 / 2) |
| PP post-processing, visual tuning | 24 | 20 | 13 (3) | 13 | 21 (4 / 9 / 8) |
| CM camera, fade, screen effects, aspect, movies | 29 | 26 | 23 (0) | 6 | 26 (5 / 16 / 5) |
| **total** | **255** | **231** | **193 (33)** | **82** | **196 (44 / 100 / 52)** |

Citation form: `page:line`, where `page` is the path **inside `FFXII TZA/17-Presentation-Rendering/`** (for example
`Scripted-Camera/the-scripted-camera-player.md:76`). A range `:a-b` covers lines a to b. A bare `:n` refers to the page
cited last in the same row or bullet. Paths beginning `../` point outside the category; such a page was opened only to
check one cross-page statement and was not audited. Some parts define short page names (for example **CRO**); each part
states its short names at its start, and every cite still carries a line. "Not stated" means none of the
17-Presentation-Rendering pages says it. Several pages in this folder are being edited by other lanes; **every quotation
is the `34861cfd` text**.

Method: twelve readers each took one part and read every line of its pages; this report merges their records. Every
quoted string was then checked mechanically against the snapshot text (whole-file match after removing markdown
emphasis and backticks; quotes that wrap across page lines were rejoined). Every flagged quote was then checked by hand
and found in the page text. Sibling `.tsv` files were opened only to confirm a layout or a count that a page states;
each check is named in Appendix A, with its result. Where the arithmetic of two stated numbers was checked (a start plus
a size, a mask, a product), the check is shown at the item.

Ids: `<part>.S-n` self-stated gap, `<part>.G-n` structural gap, `<part>.CV-n` value-changing contradiction,
`<part>.CC-n` count disagreement, `<part>.CS-n` stale or banner item. Part codes are listed at the head of §1.

## Pages read

The table gives each page's front-matter status as it stands and how the category `README.md` (145 lines) tags it. The
full status quotes, the body banners and the `.tsv` checks are in Appendix A. Disagreements between the columns are
listed per part in §3.3. Across the folder, `README.md` tags 21 pages, links 3 more without a tag of their own
(`README.md:51-53`) and does not list 36. It also has two "## Systems in this category" headings (`README.md:11`,
`:126`).

| # | page | lines | part | front matter (line) | `README.md` tag (line) |
|---|---|---:|---|---|---|
| 1 | `README.md` | 145 | AC | — | — |
| 2 | `Authored-Commands/the-authored-presentation-command-handlers.md` | 1,141 | AC | :4 DOCUMENTED (2026-10-01) | 13-14: "**PARTIAL, tier 1.**" |
| 3 | `CONTRACT-authored-command-ramp-channels.md` | 1,041 | AC | :6 DIFFERENTIAL TESTED | 18-19: "**SPECIFIED, tier 1, not differentially tested.**" |
| 4 | `CONTRACT-character-render-object.md` | 249 | RO | :6 CONTRACT READY | not listed |
| 5 | `CONTRACT-character-transform-publish.md` | 572 | RO | :6 BEHAVIORALLY UNDERSTOOD | not listed |
| 6 | `CONTRACT-coast-down-latch.md` | 584 | AC | :6 DIFFERENTIAL TESTED | not listed |
| 7 | `CONTRACT-render-command-list-and-graphics-handshake.md` | 590 | CL | :6 BEHAVIORALLY UNDERSTOOD | not listed |
| 8 | `CONTRACT-render-record-pool-lifecycle.md` | 1,472 | RO | :6 BEHAVIORALLY UNDERSTOOD | not listed |
| 9 | `Character-Render-Records/how-a-character-fades-the-ten-channels.md` | 846 | RG | :4 DOCUMENTED | 52: linked inside the rig entry ("[how a character fades](…)"), no tag of its own |
| 10 | `Character-Render-Records/how-a-presentation-entry-picks-its-track.md` | 206 | RA | :4 DOCUMENTED | 81-82: "**DOCUMENTED, tier 1 (2026-09-19), static.**" |
| 11 | `Character-Render-Records/how-a-status-shows-on-a-character.md` | 612 | RG | :4 AUDITED | 54-55: "**DOCUMENTED, tier 1 (2026-09-19), static.**" |
| 12 | `Character-Render-Records/render-event-selection-evidence.md` | 639 | RA | :4 DOCUMENTED — UQ-192 … | not listed |
| 13 | `Character-Render-Records/the-bone-trails.md` | 502 | RG | :4 DOCUMENTED | 73-74: "**DOCUMENTED, tier 1.**" |
| 14 | `Character-Render-Records/the-character-render-record-array.md` | 1,118 | RA | :4 DOCUMENTED — every register row is closed … | not listed |
| 15 | `Character-Render-Records/the-focus-point-of-a-character.md` | 179 | RA | :4 DOCUMENTED | 53: linked inside the rig entry, no tag |
| 16 | `Character-Render-Records/the-rig-of-seventeen-controllers.md` | 546 | RG | :4 DOCUMENTED | 47-48: "**DOCUMENTED, tier 1 (2026-09-19), static.**" |
| 17 | `Character-Render-Records/the-staged-look-command.md` | 483 | RG | :4 AUDITED | 51: linked inside the rig entry, no tag |
| 18 | `Character-Rendering/character-render-object.md` | 1,267 | RO | :4 AUDITED | 98-99: "**DOCUMENTED, tier 1.**" |
| 19 | `Character-Rendering/how-a-character-is-lit.md` | 398 | RO | :4 DOCUMENTED | 59-60: "**DOCUMENTED, tier 1 (2026-09-19), static.**" |
| 20 | `Effect-File-Formats/README.md` | 17 | EF | none | not listed |
| 21 | `Effect-File-Formats/an-effect-element-frame-by-frame.md` | 327 | EF | :4 AUDITED | 64-65: "**DOCUMENTED, tier 1 (2026-09-19), static.**" |
| 22 | `Effect-File-Formats/effect-element-type-dispatch.md` | 2,292 | EF | :4 DOCUMENTED — … | not listed |
| 23 | `Effect-File-Formats/effect-mesh-records-kind-54.md` | 237 | ET | :4 PARTIAL — … | not listed |
| 24 | `Effect-File-Formats/efx-and-efb-effect-containers.md` | 645 | EF | :4 PARTIAL — … | not listed |
| 25 | `Effect-File-Formats/the-element-types-00-0a.md` | 503 | ET | :4 DOCUMENTED — … GI-14 | not listed |
| 26 | `Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md` | 331 | ET | :4 DOCUMENTED — GI-9 | not listed |
| 27 | `Effect-File-Formats/the-element-types-60-74.md` | 372 | ET | :4 DOCUMENTED — GI-10 | not listed |
| 28 | `Effect-File-Formats/the-element-types-80-97.md` | 187 | ET | :4 DOCUMENTED — GI-11 | not listed |
| 29 | `Effect-File-Formats/the-menu-effect-registry.md` | 369 | ET | :4 DOCUMENTED — … | not listed |
| 30 | `Effect-File-Formats/the-six-vfx-display-layers.md` | 269 | ET | :4 DOCUMENTED | 77-78: "**DOCUMENTED, tier 1 (2026-09-19), static.**" |
| 31 | `Gi-Render-Commands/gi-render-command-family.md` | 1,864 | GP | :4 AUDITED | 94-95: "**DOCUMENTED, tier 1.**" |
| 32 | `Graphics-Thread-Handshake/the-shared-command-state-word.md` | 927 | CL | :4 AUDITED | not listed |
| 33 | `Legacy-PS2-GS/texture-mip-local-memory-budget.md` | 433 | GP | :4 AUDITED | 102: "- the 4 MiB GS local-memory texture budget still live in the PC port" (no status tag) |
| 34 | `Legacy-PS2-GS/the-vif1-vu1-layer.md` | 906 | GP | :4 DOCUMENTED — UQ-213 … (box pending) | not listed |
| 35 | `Model-And-Motion-Formats/README.md` | 61 | MF | none | not listed |
| 36 | `Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md` | 520 | MF | :4 AUDITED | not listed |
| 37 | `Model-And-Motion-Formats/adm-add-motion-tables.md` | 501 | MF | :4 AUDITED | not listed |
| 38 | `Model-And-Motion-Formats/fcp-character-parameter-block.md` | 772 | MF | :4 DOCUMENTED — … | not listed |
| 39 | `Model-And-Motion-Formats/fdm-and-for-entries.md` | 377 | MF | :4 DOCUMENTED — … | not listed |
| 40 | `Model-And-Motion-Formats/fef-and-motion-entries.md` | 1,014 | MM | :5 DOCUMENTED — … | not listed |
| 41 | `Model-And-Motion-Formats/frp-object-container.md` | 390 | MM | :4 AUDITED — … | not listed |
| 42 | `Model-And-Motion-Formats/fte-fct-texture-colour-tables.md` | 321 | MM | :4 DOCUMENTED — … | not listed |
| 43 | `Model-And-Motion-Formats/ftr-node-table.md` | 328 | MM | :4 DOCUMENTED — … | not listed |
| 44 | `Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md` | 542 | MM | :4 DOCUMENTED — GI-19 … | not listed |
| 45 | `Model-And-Motion-Formats/the-pose-sequencer.md` | 279 | MM | :4 DOCUMENTED | 69-70: "**DOCUMENTED, tier 1.**" |
| 46 | `Movie-Containers/README.md` | 35 | CM | none | not listed |
| 47 | `Movie-Containers/mh-movie-seek-index.md` | 278 | CM | :4 AUDITED | not listed |
| 48 | `Position-To-Scalar/how-a-position-becomes-a-single-number.md` | 429 | CM | :4 AUDITED — static; … | not listed |
| 49 | `Post-Processing/CONTRACT-post-processing-subsystem.md` | 329 | PP | :6 CONTRACT READY | not listed (the folder is tagged at 104: "### [`Post-Processing/`](Post-Processing/) — **documented**") |
| 50 | `Post-Processing/CONTRACT-ppfx-effect-creation.md` | 317 | PP | :6 BEHAVIORALLY UNDERSTOOD | not listed (folder tag 104) |
| 51 | `Post-Processing/ppfx-function-identification.md` | 736 | PP | :4 AUDITED | 106-107: "**DOCUMENTED, tier 2.**", with "Identity only; no body read yet." (110) |
| 52 | `Post-Processing/the-post-processing-effect-catalogue.md` | 1,045 | PP | :4 AUDITED | not listed (folder tag 104) |
| 53 | `Render-Command-List/the-ordered-render-command-list.md` | 1,966 | CL | :4 AUDITED | 88-89: "**DOCUMENTED, tier 1, crossref-clean.**" |
| 54 | `Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md` | 719 | CM | :4 AUDITED | 37-38: "**DOCUMENTED, tier 1 (2026-09-12).**" |
| 55 | `Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md` | 217 | CM | :4 DOCUMENTED — every register row is answered … | 24-25: "**PARTIAL, tier 1.**", plus "What that does on screen is **not** established." (29) |
| 56 | `Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md` | 430 | CM | :4 DOCUMENTED | 42-43: "**DOCUMENTED, tier 1 (2026-09-19), static.**" |
| 57 | `Scripted-Camera/how-a-camera-reaches-the-renderer.md` | 519 | CM | :4 DOCUMENTED | not listed |
| 58 | `Scripted-Camera/the-scripted-camera-player.md` | 1,196 | CM | :4 AUDITED | 30-31: "**DOCUMENTED, tier 1 (2026-09-12).**" |
| 59 | `Visual-Tuning-Parameters/README.md` | 74 | PP | none | not listed |
| 60 | `Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md` | 878 | PP | :4 PARTIAL — OV-42 … | 128-129: "**PARTIAL, tier 2.**" |

