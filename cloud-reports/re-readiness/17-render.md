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

## 1. Interface

17-Presentation-Rendering is a set of subsystems, not one pipeline. The parts below follow the folder layout. Each part has its own entry points, layouts, state, order and dependencies, as the pages state them. Part codes (AC, RO, …) prefix every gap and contradiction id in §2 and §3.

| code | part | pages |
|---|---|---|
| AC | Authored commands, ramp channels and the coast-down latch | README.md, CONTRACT-authored-command-ramp-channels.md, Authored-Commands/, CONTRACT-coast-down-latch.md |
| RO | Render-record pool, character render object, transform publish and lighting | CONTRACT-render-record-pool-lifecycle.md, CONTRACT-character-render-object.md, CONTRACT-character-transform-publish.md, Character-Rendering/ (2) |
| RA | The character render record array, render events, focus point and track pick | Character-Render-Records/ (record array, render-event evidence, focus point, track pick) |
| RG | Rig controllers, fades, status looks, bone trails and the staged look | Character-Render-Records/ (fades, status, bone trails, rig, staged look) |
| CL | Ordered render command list and graphics-thread handshake | CONTRACT-render-command-list-and-graphics-handshake.md, Render-Command-List/, Graphics-Thread-Handshake/ |
| GP | Gi render commands and the legacy PS2 GS/VIF layer | Gi-Render-Commands/, Legacy-PS2-GS/ (2) |
| EF | Effect containers, element dispatch and the per-frame element update | Effect-File-Formats/ (README, dispatch, frame-by-frame, EFX/EFB) |
| ET | Effect element types, kind-0x54 meshes, menu effect registry and VFX layers | Effect-File-Formats/ (kind 0x54, four element-type pages, menu registry, six layers) |
| MF | Model formats: add-motion tables, ADM, FCP, FDM/FOR | Model-And-Motion-Formats/ (README, add-motion, ADM, FCP, FDM/FOR) |
| MM | Motion formats: FEF/motion entries, FRP, FTE/FCT, FTR, oscillator, pose sequencer | Model-And-Motion-Formats/ (FEF, FRP, FTE/FCT, FTR, oscillator, pose sequencer) |
| PP | Post-processing and visual tuning parameters | Post-Processing/ (4), Visual-Tuning-Parameters/ (2) |
| CM | Scripted camera, screen fade, screen effects, aspect fit, position-to-scalar, movie index | Movie-Containers/ (2), Position-To-Scalar/, Screen-Fade/, Screen-Mode-And-Aspect-Fit/, Script-Screen-Effects/, Scripted-Camera/ (2) |

### 1.1 [AC] Authored commands, ramp channels and the coast-down latch

#### AC — Entry points

| entry (size) | callers as stated | what it does | cite |
|---|---|---|---|
| `003B6890` (110 B per record-array page) | not stated on ramp page; "from `CharacterRenderSystem_Initialize`" (Character-Render-Records/the-character-render-record-array.md:685) | lazy table alloc of 0x8C00 bytes at `[02B40528]`; zeroes `02B40520`/`02B40524`; clears `+0x40` bit 0 of all 160 records | CONTRACT-authored-command-ramp-channels.md:62-63, :344-349 |
| `003B6A90` (117 B), `003B6A10` (119 B) | class 0x0D callback `004173D0`, class 0x0F callback `00417460` (110 B each) | pair setters (two targets) | CONTRACT-authored-command-ramp-channels.md:74,76,256-262 |
| `003B69B0`, `003B6950` (not in function census) | reached by tail `jmp` from the 0x0E/0x10 callbacks (names `00417440`/`004174D0` are given only on Model-And-Motion-Formats/fef-and-motion-entries.md:994,996) | single setters | CONTRACT-authored-command-ramp-channels.md:28-31,75,77 |
| `003B5890` | `00426090` (`00426112`) ← `RenderSystem_RunCharacterUpdatePipeline` `003323D0` ← `0022A770` (once), `0022B8C0` (two sites) | per-pass tick over 160 records, five channels | CONTRACT-authored-command-ramp-channels.md:100-110, :216-221, :244-246 |
| `003B5C00` (214 B) | `0041C850` (`0041C8E6`), `PresentationEntry_RebuildAndFastForwardToTime` `0041D820` (`0041D9C6`) | steps one slot; checks handle and enable only | CONTRACT-authored-command-ramp-channels.md:224-229, :860 |
| `003B5D40(handle, n)` | `0041D560` (`0041D5E7`) | starts the +0x43 cross-fade weight | CONTRACT-authored-command-ramp-channels.md:196-200 |
| `003B67F0` (155 B) | `003723B0` | reset; 1.0f defaults | CONTRACT-authored-command-ramp-channels.md:201, :881 |
| `003B56D0(renderRecordIndex)` | render-record promotion (handle kept at record +0x114) | slot alloc; mints `gen<<8\|slot` | CONTRACT-authored-command-ramp-channels.md:205-211, :264-267 |
| `003B6000` (27 B) | render record drop | slot free | CONTRACT-authored-command-ramp-channels.md:283; Character-Render-Records/the-character-render-record-array.md:1097 |
| `003B6930` | 5 sites: `0024D9C0`, `003B8670` ×2, `00520800` ×2 | `gate = (gate & (arg >> 2)) \| (arg & 3)`; args 4/6 | CONTRACT-authored-command-ramp-channels.md:169-184, :269-274 |
| `003B6020` (677 B) | `00521440` ← tail of stage gate `00428E40` | 160-slot draw pass, hide test | CONTRACT-authored-command-ramp-channels.md:192, :571, :657-667 |
| `003B62D0` (1,301 B) | `003B6020` (`003B6224`) | builds the 0xA0 output record from the channels | CONTRACT-authored-command-ramp-channels.md:143-160, :586 |
| leaf setters `003B5CE0`, `003B5E20`, `003B6B10/6B30/6B60/6B80/6BB0/6BD0`, `003B6900` | not stated (003B6900 is the V1 verb of the shadow sync, :702) | write other record fields | CONTRACT-authored-command-ramp-channels.md:452-461, :702 |
| drains `0041DA90`, `0041E000`, `0041E1D0` | not stated | walk command stream at `[arg2+0x368] + [arg1+0x90] + 4`; id = `word & 0x7F`, clamp 0x4B | Authored-Commands/the-authored-presentation-command-handlers.md:31-36 |
| invoker `01EFFAF0[id]` (16-byte record, 0x20-byte thunk) | the drains | loads `[02CA4410+id*8]`, null → ret, `jmp handler(render_record, cmd)` | Authored-Commands/the-authored-presentation-command-handlers.md:41-51 |
| `0041D6C0(id, fn)` (9 B), `0041D6D0`, `0041D6E0`; `0041CCA0` | `CharacterRenderSystem_Initialize` `004269A0`; seeders `002EA320`/`002EA5F0` | register in bank A / bank B / context ptr; clear both 0x258-byte banks | Authored-Commands/the-authored-presentation-command-handlers.md:71-83, :113-118 |
| 25 registered handlers (ids 0x05 bank B; 0x11–0x48 bank A) | invokers only ("no direct caller") | see table | Authored-Commands/the-authored-presentation-command-handlers.md:85-111 |
| invoker-only ids 0x00 `00417810`, 0x01 `00417920`, 0x03 `00417A80`, 0x04 `00417AD0`, 0x05 `00417C60`, 0x08 `00417D00`, 0x09 `00417F40`, 0x0A `00418600`, 0x0B `00417110`, 0x2C `00417DE0` | drains | act on the presentation entry directly | Authored-Commands/the-authored-presentation-command-handlers.md:282-287, :765, :884-906 |
| `00520100` | `PresentationEmbeddedRecord_ActivatePendingState` `0041DD40` | if `word[rcx+6] == -1`, posts `00520E90` through `00426870` | Authored-Commands/the-authored-presentation-command-handlers.md:124 |
| `00520E90` (361 B) | via `00426870` from `00520100`, `00520510`, `005205B0` | sway-oscillator configurator (`0040ABF0`: bone → +0x3C, preset → +0x3E) | Authored-Commands/the-authored-presentation-command-handlers.md:110, :125, :1057-1059 |
| `00520010` | `0046E3E0`, `0046E6F0`, `00477F20` | shared helper iterating `dword[rcx+0x40]` | Authored-Commands/the-authored-presentation-command-handlers.md:126 |
| `00426870` (90 B) | `00520100`, `003E6A60`, `00520E70`, `00520510`, `005205B0` | immediate `fn(R,arg)` plus depth-first sub-tree traversal | Authored-Commands/the-authored-presentation-command-handlers.md:128-129, :507-519 |
| `00424080` `Movement_ModifyHeadingSpeedForObjectState` (427 B) | `Movement_ComputeDeltaFromHeadingSpeed` `002E4380` | coast-down latch (`cx` id, `rdx` heading ptr, `r8` speed ptr) | CONTRACT-coast-down-latch.md:28-31, :43-48, :564-565 |
| `0051B9E0` → `0051F240` (138 B) | `00424080` (`004241BD`) | `PresentationEntryReferenceContainer_ResolveEntryById` | CONTRACT-coast-down-latch.md:183-197 |
| `00424230` | not stated | returns 1 on `[rcx+0xC4]==-1` or null lookup, else `0041C760(resolved) & 1` | CONTRACT-coast-down-latch.md:223-227 |
| `004256E0` (writer of +0x456/+0x457) | not stated | saturating counters | CONTRACT-coast-down-latch.md:256-265, :279-282 |

#### AC — Inputs and outputs (record layouts)

**V1 shadow/ramp slot** (160 × 0xE0 at `[02B40528]`; CONTRACT-authored-command-ramp-channels.md:65, :146-152, :452-476):

| off | size | meaning | cite |
|---|---|---|---|
| +0x00/+0x01/+0x02/+0x03/+0x43 | u8 each | step counters for ch0 (0x0D), ch1 (0x0E), ch2 (0x0F), ch3 (0x10), ch+0x43 | :72-79 |
| +0x04 | ? | render record index | :208 |
| +0x08/+0x0C/+0x14/+0x18/+0x20–+0x28/+0x2C | scalars/vec3 | factors multiplied into the out record (leaf setters) | :458-460 |
| +0x10 | u32 | handle `gen<<8\|slot` (identity guard) | :85, :205-211 |
| +0x1C | u32 | unused (allocator zero) | :469-472 |
| +0x30/+0x34 | 2×f32 | saved UV-offset snapshot | :452-453 |
| +0x38/+0x3A | u16 | current/previous blend selector | :454 |
| +0x3C/+0x3E | u16 | two model bones | :208-209 |
| +0x40 | u8 | bit0 enable; bit 0x20 forces morph complete; bit 0x40 selects out+0x54 source | :104, :157-159, :589 |
| +0x41 | u8 | bit0 pause; bit1 hide | :105, :324-326 |
| +0x44/+0x48/+0x4C | f32 | UV scale/offset | :455 |
| +0x50,+0x54 / +0x58,+0x5C / +0x70 / +0x78 / +0x98 | f32 | channel values | :74-79 |
| +0x60,+0x64 / +0x68,+0x6C / +0x74 / +0x7C / +0x9C | f32 | deltas | :74-79 |
| +0x80–+0x94 | 6×f32 | cross-fade snapshot (B set) | :198, :456 |
| +0xA0–+0xB8 | | snapshot buffer (003B5E20); +0xAC from arg+0x54; +0xB0 angle (radians) | :457, :740-762 |
| +0xBC | f32 | extra rotation offset | :457 |
| +0xC0–+0xD4 | 6×f32 | 003B62D0 computed cache (pre-transform) | :159-160, :644-646 |
| +0xD8–+0xDF | 8 B | untouched tail | :473-476 |

Globals: `02B40520` generation serial, `02B40524` gate (bit0 pause-all, bit1 hide-all), `02B40528` table ptr (CONTRACT-authored-command-ramp-channels.md:162-172, :344-347).
Output: a 0xA0 record per visible slot is copied into the PS2 ring `02EBEFC0` and submitted by `003A1DB0`; the PC consumes none of it (:161, :612-621).
The LUT is `0046FAE0`: row `(3*edx+r8d)*0x1E0` at `01F20E60`, count dword `01F20A98` = 60 (:152, :558-561, :625-636).

**Authored command record** (Authored-Commands/the-authored-presentation-command-handlers.md):
- Header: `u16 (length << 7 | id)`, then the payload. A track group is `u16 time key, u16 (length << 6 | count)` (:218-219).
- The `@FMC` block has its name at +0x10, the track count at +0x0C and the first track header at +0x30 (:215-216).
- Handlers read the subtype at +2/+3 and parameters from +4 (:62).
- Ramp classes 0x0D–0x10:
  - byte +2 is steps;
  - floats +4 (and +8 for the pairs) are the targets;
  - the handle comes from the entry's `+0x35C` (CONTRACT-authored-command-ramp-channels.md:258-260).
- Per-id payloads are in the tables at :85-111 and :282-287, and in the per-command sections.

**Handler bank / invoker tables:**
- Bank A `02CA4410`: 75 qwords (0x258 bytes).
- Bank B `02CA4670`: only slot 5 is used.
- Context pointer `02CA4668`, which holds `.data` table `01F000A0` (0x30 × `{1, cell}`).
- Invoker table `01EFFAF0`: 16-byte records `{invoker, flag dword}`.

Sources: Authored-Commands/the-authored-presentation-command-handlers.md:44-48, :71-73, :148-161, :914-915.

**V2 shadow pool** (`02B3F550` 32-byte header, then 32 × 0x70 at `02B3F570`):
- `+4` is the handle.
- Ramps are `{count, value, rate}` at `{+0x1C,+0x24,+0x2C}`, `{+0x1D,+0x28,+0x30}`, `{+0x1E,+0x34,+0x38}`, `{+0x54,+0x3C,+0x48}`, `{+0x55,+0x44,+0x4C}`.
- `+0x1F` is the mode nibbles; `+0x40`/`+0x50` are f32; `+0x56` is u16; `+0x58` is flags.

Sources: Authored-Commands/the-authored-presentation-command-handlers.md:1029-1050; CONTRACT-authored-command-ramp-channels.md:403-418, :920-929.

**Coast-down record** (`*(char**)022C6F28 + id*0x740`):

| off | meaning |
|---|---|
| +0x000 | id (−1 = free) |
| +0x006 | owner link |
| +0x0C4 | presentation entry id |
| +0x0CC | event word |
| +0x284 | object flags |
| +0x456/+0x457 | i8 counters |
| +0x610–+0x61C | live {heading f32, speed f32, scale f32, flags u16 (bit0)} |
| +0x620–+0x62C | cached mirror of the live block |

Sources: CONTRACT-coast-down-latch.md:52-65, :279-282, :416-438.
The 0x30-byte reference-container entry is: flags +0x00, handle +0x10, cached pointer +0x18, delta +0x20 (:208-211).
Constants: `0.83f` @`00D12434`, `0.05f` @`008F30E8`, `0.9f` @`008FCC8C`, time base @`01DFE0B4` (:348-350).

#### AC — State (globals and objects, with lifetime)

| object | lifetime / init | cite |
|---|---|---|
| `02B40528` V1 table | created once by `003B6890` while null; never freed (not stated) | CONTRACT-authored-command-ramp-channels.md:329-330 |
| `02B40520` serial | 0 at alloc; +1 per slot alloc; past 0xFFFFFF → 1 | :207, :347 |
| `02B40524` gate | 0 at alloc; only `003B6930` writes it; bit0 never set | :169-172 |
| V1 slot | `003B56D0` → `003B6000`; reset `003B67F0`; complete per-field initial values not tabulated (see AC.G-8) | :264-267, :881 |
| bank A/B | cleared by `0041CCA0` at init; filled by `004269A0` plus seeders `002EA320`/`002EA5F0` | Authored-Commands/the-authored-presentation-command-handlers.md:73-81, :113-118 |
| V2 header `02B3F554` | init 1 by `003AFCD0`; setter `003AFD30`; no reader | CONTRACT-authored-command-ramp-channels.md:407-417 |
| `02B4D7D0` pool (32 × 0x60), `02B4D7A0` count, `02B4D7A4` gen, `02B4D7A2` gate | gate set by script verb 0x4A0, cleared by `002628B0` and `003D8C30` | Authored-Commands/the-authored-presentation-command-handlers.md:663-679, :1095-1101 |
| coast-down latch `+0x62C` bit0 | set by arm; cleared by service release or the cache copy; initial value not stated | CONTRACT-coast-down-latch.md:129-144 |
| `+0x456/+0x457` | reset together by `00425C63`; walks to fixed point 0xB4 | :279-282, :410-415 |
| `01DFE0B4` time base | see AC.CV-6 | :285, :349 |

#### AC — Order (what runs when, and what triggers it)

- **Ramp tick.** Field frame `0022A770` → `003323D0` → `00426090` → `003B5890` at `00426112`, gated by `00358290()` (CONTRACT-authored-command-ramp-channels.md:216-218, :421-422).
- **Full menu.** `0022B8C0` runs the tick at two sites, so a closing menu can tick twice (:219-221).
- **Repeat dispatch.** `0017D6E0` can run `0022A490` twice per animate call (:230-237).
- **V2 tick.** `003AF460` is called from `00426117` (Model-And-Motion-Formats/fef-and-motion-entries.md:383-384, not on the assigned pages).
- **Draw.** `00428E40` gates on `+0x48842 == 1 && +0x48843 == 0`, then runs walk `00426420`, then tails `00521440` → `003B6020` (:657-667). Its order relative to `00426090` is not stated.
- **Ramp-tick channel order.** 0, 2, 1, 3, 0x43 (:112).
- **Commands.** The three drains run on stream progress. A command takes effect immediately in its handler; `00426870` is immediate, not deferred (Authored-Commands/the-authored-presentation-command-handlers.md:507-519). When the drains run in the frame is not stated.
- **Coast-down.** The latch is called per movement-delta computation (CONTRACT-coast-down-latch.md:564-565). Calls per frame are not stated (:528-529).

#### AC — Dependencies

- **Character render record array / pool lifecycle.** The handle at +0x114 is the V1 slot (CONTRACT-authored-command-ramp-channels.md:137-141).
- **PS2 command ring.** `02EBEFC0` with `003A1DB0` and `0036F360` (:161).
- **Frame dispatch.** `22-Middleware-PhyreEngine/The-Frame` (:217). Gates: the pass-enable table, the monster viewer and the UI request (:419-448).
- **Battle unit.** `00325260`, `00325090` and `003250F0` handle ids 4, 6 and 0x0C (Authored-Commands/the-authored-presentation-command-handlers.md:246-266, :1120-1137).
- **Audio.** `0046CBA0` and `0046CC70` (:87, :106).
- **Rig.** Controllers `0042BED0`, controller 2 and controller 0 (:585-587, :795-799, :110).
- **Resource layer.** `002ED570`, `0020E600`, `@FRP`/`@FMN`/`@FMW`/`@FTR` (:271, :813-820, :1054-1058).
- **Camera-shake pool.** (:1092-1094)
- **Movement.** `002E4380` (CONTRACT-coast-down-latch.md:564-568).
- **Reference container.** `0051F240` (:184-185).
- **Event store.** `00424D80` (:231).

### 1.2 [RO] Render-record pool, character render object, transform publish and lighting

Short names in this part: **POOL** = `CONTRACT-render-record-pool-lifecycle.md`; **CRO-C** = `CONTRACT-character-render-object.md`; **PUB** = `CONTRACT-character-transform-publish.md`; **CRO** = `Character-Rendering/character-render-object.md`; **LIT** = `Character-Rendering/how-a-character-is-lit.md`.


#### RO — Entry points

| entry (size) | callers as stated | what it does | cite |
|---|---|---|---|
| `004269A0` pool construct | not stated in POOL (another page gives `CharacterRenderSystem_Initialize`, `Character-Render-Records/the-character-render-record-array.md:562`) | calls `0041F730` on all 160 records, then seeds the tail (heads -1, free/live 0, flag 0, +0x2C 0xFFFF, tuning block) | CONTRACT-render-record-pool-lifecycle.md:152-156 |
| `004278E0` look up by name | allocate (`004279DC`) | walks the active list (skips `+0x290` bit 1), then the pending list (no skip). Hit: `movzx eax, r10w`. Miss: `or eax,-1` | CONTRACT-render-record-pool-lifecycle.md:158-170 |
| `004279B0` allocate | "Which caller supplies the names … " is open | duplicate→0; full→0; take nextFree; clear; link at the pending tail; `00420480` init; set `+0x290` bit 0; liveCount++; advance the cursor | CONTRACT-render-record-pool-lifecycle.md:51, 172-190, 333-365 |
| `00428710` promote | not stated | per pending record: `0041FCF0`; `+0x414`=tail `+0x28`; `003E68E0`→`+0x114`=`003B56D0(id)`; bracket bit 0 around `0042C410`; clear rec `+0x290` bit 0; move to the active tail; set flag bit 5; finally both pending ends = -1 | CONTRACT-render-record-pool-lifecycle.md:198-218 |
| `00427C90` retire | not stated (the teardown `0042ED60` runs it, CONTRACT-render-record-pool-lifecycle.md:1450) | for actives with `+0x290` bit 1: unlink; liveCount--; end fixups by the record's id; `0042F4C0`; drain the child list `+0x08` via `00426EC0`; free `+0x114`/`+0x118`; `004200A0`; flag bit 5 | CONTRACT-render-record-pool-lifecycle.md:225-241 |
| `00429140` release | not stated | null→0. `+0x284` bit 2 set: mark (`+0x290`\|=2 …), no unlink. Bit 2 clear and `+0x290` bit 0: pending unlink, count--, `0041F730`. Returns 1 otherwise | CONTRACT-render-record-pool-lifecycle.md:267-291 |
| `00426480` (30 B) tail `+0x30` setter | not stated | stores `0020E620(ptr)` at `+0x48830`; the only writer | CONTRACT-render-record-pool-lifecycle.md:816-824 |
| `0042ED60` (162 B) pool teardown | `00332660` | clears `+0x48818` bit 0x20 around `00427C90`/`00428710`, walks the chain via `0042DA30`, then `00427DE0(1)`, `00427BD0` | CONTRACT-render-record-pool-lifecycle.md:1450 |
| `001F4DA0` CRO construct (516 B) | the sole site `001BD527` in `001BD4A0` | builds the vectors; clears `+0x4B4`; copies a zeroed 0x318 block into `+0x78` | CONTRACT-character-render-object.md:50,55; Character-Rendering/character-render-object.md:50-63, 907-923 |
| `001F51E0` destructor body | slot 0 only | re-installs the vtable, zeroes `+0x28`, destroys `+0x3E0`, frees the `+0x390` vector (0x24 stride) | Character-Rendering/character-render-object.md:424-430 |
| `001F6E70` slot 2 setup (2,328 B) | from `001BD4A0` on a miss | sets `+0x4B4`=1 at `001F7729` (+2,233); calls the binder `001F7790` twice | CONTRACT-character-render-object.md:52, 86-88; Character-Rendering/character-render-object.md:454-458 |
| `001FB120` slot 13 publish (496 B) | "reached only through vtable slot 13" (CONTRACT-character-transform-publish.md:42); called by slot 16 at `001FA748` (Character-Rendering/character-render-object.md:1019) once per material element (Character-Rendering/character-render-object.md:338-344) | latch gate; zero-motion test; two sinks; bank copy by `[01F7F598]+0x1C` | CONTRACT-character-transform-publish.md:42-47, 172-184 |
| `001FAD50` uploader (non-virtual) | not stated | copies the bank chosen by `+0x1D` into PS2WH/HS/InvWHS and ZBiasOriginal/Instance; gated on `+0x4B4` | Character-Rendering/character-render-object.md:805-822 |
| `001F5D70` draw (non-virtual) | `00215320` (CharacterOrderedObject slot 1) | "calls Phyre's draw submit `0060B980` per mesh instance, in a shadow, alpha or opaque mode" | Character-Rendering/character-render-object.md:314-320 |
| `001BD4A0` acquire / `001BD840` release | pose update `Skeleton_UpdateFinalPoseAndCombatLook` (acquire); `CharacterRenderRecord_TeardownAndReset` (release) | per-model pool: tree keyed by `+0x2A0`, active vector, `{object,3}` | Character-Rendering/character-render-object.md:388-407 |
| slot 8 `001F9B20` UpdateViewParameters (1,211 B) | the record draw | map-lighting fix-up (ambient rgb×I+O; 6 lights, upward test) | Character-Rendering/character-render-object.md:253-275 |
| other slots 0-30 | the vtable `00903B68` | table of one-line roles | Character-Rendering/character-render-object.md:131-163 |
| `003AB960` light create (506 B) | the weather preset rebuild; the status tint | takes a pool entry; handle; copies the 0x50 request to `+0x20`; precomputes; appends to the list | Character-Rendering/how-a-character-is-lit.md:47-50, 179-186 |
| `003ABD00` (26 B) | not stated | handle→block, checking the whole handle | Character-Rendering/how-a-character-is-lit.md:50 |
| `003ACC10` selector (2,342 B) | the gather | class filter, scope, type switch, ambient contest; returns the directional count | Character-Rendering/how-a-character-is-lit.md:69-123 |
| `003ACAA0` ambient evaluator (358 B) | the selector | colour by subtype; luminance strength; light scale | Character-Rendering/how-a-character-is-lit.md:125-131, 260-261 |
| `003ABD50` gather (950 B) | `004FD4B0` model-instance draw setup | stores the scale, calls the selector, evaluates by kind, writes ≤6 into the 0xE0 block | Character-Rendering/how-a-character-is-lit.md:133-138, 211-216 |
| `003AD540` / `003AE0E0` / `003AD830` / `003AE4C0` / `003ADC40` | the gather | kinds 1-5: directional, point, plane-cut point, spot, segment | Character-Rendering/how-a-character-is-lit.md:142-175 |
| `003AC110` (1,876 B) record-less gather | "a body in the effect-element address band, not read" | the selector and gather for non-characters | Character-Rendering/how-a-character-is-lit.md:188-207 |
| `003ACA80` (7 B) / `003ACA90` (9 B) | status deny (bit 5), the effect driver (bit 0), `002628B0`/`0026C8C0` (clear bit 3) | OR / clear bits in `02B3F501` | Character-Rendering/how-a-character-is-lit.md:74-79, 285-287 |
| `003AC900` (28 B) | `00376AC0`, `00376BE0` | `02B3F51C *= xmm0`; `02B3F503 = 1` | Character-Rendering/how-a-character-is-lit.md:370 |
| `0041F270` (124 B) | not stated | publishes the record's blend override to instance `+0x244..+0x250` | Character-Rendering/how-a-character-is-lit.md:232-238 |

#### RO — Inputs and outputs (record layouts)

**Pool block** (`*(char**)0x022C6F28`, 0x48930 B = 160 × 0x740 + 0x130; CONTRACT-render-record-pool-lifecycle.md:28-30, 463)

| offset | size | meaning | cite |
|---|---|---|---|
| tail +0x00/+0x04 | 4/4 | headActive/tailActive (−1 = none) | CONTRACT-render-record-pool-lifecycle.md:69-70 |
| +0x08/+0x0C | 4/4 | nextFreeIndex / liveCount (one 8-byte ctor store) | CONTRACT-render-record-pool-lifecycle.md:71-72, 155-156 |
| +0x10/+0x14 | 4/4 | headPending/tailPending | CONTRACT-render-record-pool-lifecycle.md:73-74 |
| +0x18 | 4 | flag word: bit 5 set by promote and retire; bit 0 bracketed | CONTRACT-render-record-pool-lifecycle.md:130-133 |
| +0x1C | 8 (qword store) | 34.0f, and the same store zeroes +0x20 | CONTRACT-render-record-pool-lifecycle.md:840-842 |
| +0x24 | 4 | 4.0f | CONTRACT-render-record-pool-lifecycle.md:842 |
| +0x28 | 4 | 0x3E2AAAAB = 1/6, copied to rec `+0x414` at promote | CONTRACT-render-record-pool-lifecycle.md:832-836 |
| +0x2C | 2 | a 16-bit index, 0xFFFF sentinel, scaled by 0x740 | CONTRACT-render-record-pool-lifecycle.md:87-89 |
| +0x30 | 4 | image-relative pointer (written only by `00426480`), passed through `0020E600` to `00420480` | CONTRACT-render-record-pool-lifecycle.md:181-182, 816-830 |
| +0x40, +0x4C..+0x70 | — | ctor-written; no reader seen; +0x64 is an 8-byte span | CONTRACT-render-record-pool-lifecycle.md:533-536 |

**0x740 record fields the pool uses**: `+0x00` id i16; `+0x02` prev i16; `+0x04` next i16 (CONTRACT-render-record-pool-lifecycle.md:76); `+0x08` child-list head (CONTRACT-render-record-pool-lifecycle.md:236); `+0x06`/`+0x0A` written −1 by the drain (CONTRACT-render-record-pool-lifecycle.md:848); `+0x10` handle resolved by `0020E600`, `+0x18` (CONTRACT-render-record-pool-lifecycle.md:278); `+0x1C` name (NUL-terminated) (CONTRACT-render-record-pool-lifecycle.md:159); `+0x108` (8 B) and `+0x110` zeroed by release (CONTRACT-render-record-pool-lifecycle.md:275); `+0x114` handle into the 160×0xE0 pool at `[02B40528]`; `+0x118` handle into the 32×0x70 table at `02B3F570` (CONTRACT-render-record-pool-lifecycle.md:246-249); `+0x284` state dword (0 = free; init 0x2010F9; bit 2 live; bit 30) (CONTRACT-render-record-pool-lifecycle.md:108-109, 276, 460); `+0x290` (bit 0 allocated-not-promoted, bit 1 marked for retire) (CONTRACT-render-record-pool-lifecycle.md:183, 208, 273); `+0x2AE` bit 0 (CONTRACT-render-record-pool-lifecycle.md:274); `+0x414` (CONTRACT-render-record-pool-lifecycle.md:202). Slot handle = `(gen<<8)|slot`, the generation clamps to 1 above 0xFFFFFF (CONTRACT-render-record-pool-lifecycle.md:604).

**CharacterRenderObject** (0x668 B; Character-Rendering/character-render-object.md:177-224; CONTRACT-character-render-object.md:62-67)

| offset | size | meaning | cite |
|---|---|---|---|
| +0x000 | 8 | vtable `00903B68` | Character-Rendering/character-render-object.md:178 |
| +0x008/10/18, alloc +0x020 | 3×8+8 | vector, element 0x10 | Character-Rendering/character-render-object.md:179-181 |
| +0x028 | 8 | ctorBoundRef; the `CharacterOrderedObject` child that slot 1 appends | Character-Rendering/character-render-object.md:182, 134 |
| +0x030/38/40, alloc +0x048 | | material pointer vector | Character-Rendering/character-render-object.md:183-185 |
| +0x050 | 8 | boundSubobjectRef | Character-Rendering/character-render-object.md:186 |
| +0x058/60/68, alloc +0x070 | | record array, element 0x318 (binding record) | Character-Rendering/character-render-object.md:187-188 |
| +0x078..+0x38F | 0x318 | the object's own CharacterShaderParamTable (zeroed by the ctor block copy) | Character-Rendering/character-render-object.md:929-938 |
| +0x390/398/3A0, alloc +0x3A8 | | 0x24-element vector | Character-Rendering/character-render-object.md:196-197, 427-428 |
| +0x3B0..+0x3BC | 16 | input vec4 to `001ABF50` | Character-Rendering/character-render-object.md:198-203 |
| +0x3C0, +0x3D0 | 16+16 | out vectors (0s / 4s) | Character-Rendering/character-render-object.md:204-207 |
| +0x3E0 | ? | embedded object (dtor `006336E0`), extent unproven | Character-Rendering/character-render-object.md:208 |
| +0x420 | 96 | undefined span | Character-Rendering/character-render-object.md:1098-1099 |
| +0x480..+0x498 | | slots 2/3/19/20; +0x488 → model entry (`[[object+0x488]+0x2A0]`) | Character-Rendering/character-render-object.md:209, 398 |
| +0x498, +0x49C, +0x4B0, +0x4B6, +0x4B8, +0x4BC | | setter/getter scalars | Character-Rendering/character-render-object.md:210-220 |
| +0x4A4 | | flag (slot 11) | Character-Rendering/character-render-object.md:144 |
| +0x4A8 | 4 | float = arg f (slot 8) | Character-Rendering/character-render-object.md:255 |
| +0x4AC | 4 | float (1.0f from ctor; compared with 0.9 by slot 16) | Character-Rendering/character-render-object.md:214-215 |
| +0x4B4 | 1 | ready latch | CONTRACT-character-render-object.md:64, 85-88 |
| +0x4C4..+0x583 / +0x584..+0x643 | 192/192 | banks A/B: PS2WHMatrix, PS2HSMatrix, InvPS2WHSMatrix | Character-Rendering/character-render-object.md:813-815 |
| +0x644, +0x654, +0x664 | | slot 9; slot 24 dword at +0x664 | Character-Rendering/character-render-object.md:221-229 |

**0x318 binding record** (`[obj+0x58] + i*0x318`): `+0x00` owner (the shader); `[[rec+0]+8]` = the parameter data block (Character-Rendering/character-render-object.md:833-839); `+0x08/+0x10` bank-A scalars, `+0x0C/+0x14` bank-B scalars (CONTRACT-character-transform-publish.md:88-89); `+0x30..+0x310` 92 descriptor pointers by name (Character-Rendering/character-render-object.md:462-464, TSV); `+0xE0` PS2ZBiasEnabled, `+0xE8` PS2ZBiasNoGS (CONTRACT-character-transform-publish.md:311-315). A descriptor's `+0x10` is a u16 byte offset into the data block (CONTRACT-character-transform-publish.md:66-68, 327-329).

**Publish args**: `rcx` obj, `edx` index (not bound-checked), `r8d` flag (zero test only), `xmm3` scalarA, `[rsp+0x70]` scalarB, three matrix pointers on the stack (CONTRACT-character-transform-publish.md:44, 172-184). The zero-motion dword is `(a==0&&b==0)?0:1`, NaN→1, -0→0 (CONTRACT-character-transform-publish.md:140-144).

**Light request** (0x50 B at entry+0x20; Character-Rendering/how-a-character-is-lit.md:53-62): `+0` type (6 ambient, 7 own list, 1-5 kinds); `+1` priority; `+2` subtype; `+3/+4` scope; `+5` flags (bit 4 ambient-mode exempt, bits 1-3 matrix, ≥0x80 scale exempt); `+6` space mode (Character-Rendering/how-a-character-is-lit.md:144, 152-153); `+7` (bit 0 exclusive, bit 1 skip, bits 2-7 class); `+8` target; `+0xC` range (Character-Rendering/how-a-character-is-lit.md:155); `+0x10` colour; `+0x1C` the camera float; `+0x20` position; `+0x30` vector or k; `+0x40/+0x44` turn pair (kind 1/9) or kind-specific; `+0x48`, `+0x4C`. Pool: 128 × 0x70 at `[02B3F528]`; links prev `+8`, next `+0x10`; list head `02B3F508`, tail `02B3F510` (Character-Rendering/how-a-character-is-lit.md:47, 184-185). Output block: global `02CA8110`, 0xE0 B; colours `+0x60`, ambient `+0xC0`, camera-light index `+0xD0` (Character-Rendering/how-a-character-is-lit.md:138, 146, 215-216).

#### RO — State (globals and objects, with lifetime)

| state | lifetime / init | cite |
|---|---|---|
| pool pointer `0x022C6F28` | allocated once at `003325E7`, never freed | CONTRACT-render-record-pool-lifecycle.md:28-30 |
| tail block | ctor `004269A0` sets the heads to −1, free/live to 0, flag 0, +0x2C 0xFFFF | CONTRACT-render-record-pool-lifecycle.md:152-156 |
| CRO `+0x4B4` | ctor 0; slot 2 sets 1; never cleared | CONTRACT-character-render-object.md:85-88 |
| CRO `+0x118` span (632 B) | "allocated from an unzeroed heap, never cleared" — contradicted, RO.CV-9 | Character-Rendering/character-render-object.md:1080 |
| singleton `[01F7F598]` (0xDD8 B) | lazy `00189000`; ctor `00184F20` zeroes the word `+0x1C` (Character-Rendering/character-render-object.md:753-758) or ctor `00189CE0` zeroes it at `0018A0EA` (CONTRACT-character-transform-publish.md:291-292): RO.CV-4 | — |
| singleton `+0x1C` / `+0x1D` | +0x1C written 1 by `00185A1D`, 0 by `001860E6` (and 0 by a third method, Character-Rendering/character-render-object.md:790); +0x1D set per pass from command `+0x20` | Character-Rendering/character-render-object.md:787-798 |
| per-model CRO pool | tree keyed by `+0x2A0`, active vector; `{object,3}` on release | Character-Rendering/character-render-object.md:391-399 |
| light globals | `02B3F501` (filter, set/clear by `003ACA80`/`003ACA90`); `02B3F520` (filter, setter unknown); `02B3F502` (scale enable); `02B3F503`/`02B3F51C` (set by `003AC900`); `02B3F518` (scale, from rec `+0x5EC`, or 1.0 for non-characters); `02B3F504` counter | Character-Rendering/how-a-character-is-lit.md:74-75, 111-112, 129-131, 197, 370, 392 |

#### RO — Order (what runs when, and what triggers it)

- **Pool**: allocate puts a record on pending; it is invisible to active walks until `00428710` runs (CONTRACT-render-record-pool-lifecycle.md:189-190, 442-444). When promote/retire run in the frame: not stated ("it cannot show when a real walk happens", CONTRACT-render-record-pool-lifecycle.md:443). The teardown `0042ED60` runs retire then promote (bit 0x20 bracket) (CONTRACT-render-record-pool-lifecycle.md:1450).
- **Record draw → object slots** (static): "11, 1, 1, **8, 9**, 21, 22, 23, **24**, 15, 26, **12**, 17, 6, **16**" (Character-Rendering/character-render-object.md:336-337). Inside slot 16, per material: 14, 19, 20 (kinds 2/5/10/13), 10, 13 (Character-Rendering/character-render-object.md:338-344). The draw body runs once per record, and again (pass 1) when record `+8` bit 0 is set (Character-Rendering/character-render-object.md:333-334). Slot 1 appends the child to `[01F7F5E0]`; the render pass list walks it → `00215320` → `001F5D70` → `0060B980` (Character-Rendering/character-render-object.md:316-320).
- **Bank selector**: written by the camera publish `003829D0` (from `00259820`, `00259970`, `003ED8A0`; the camera publish is reached from `00314370`, called 3× by `0022A770` and 2× by MainLoop) "before the render objects' slot-13 publish reads it" (CONTRACT-character-transform-publish.md:299-305), versus "Not established: when the slot-13 writer … runs relative to those two enqueues" (Character-Rendering/character-render-object.md:799-801). RO.CV-5.
- **Lighting**: `004FD4B0` calls the gather, then rewrites the ambient in place (Character-Rendering/how-a-character-is-lit.md:211-222). Light list order = creation order (Character-Rendering/how-a-character-is-lit.md:185-186).

#### RO — Dependencies

Allocator `00210EC0` → Bullet `malloc` (Character-Rendering/character-render-object.md:1075); camera publish / view system (CONTRACT-character-transform-publish.md:296-305; Character-Rendering/how-a-character-is-lit.md:97-98 camera pos `02AEDF20`); the application-root singleton `00189000` (CONTRACT-character-transform-publish.md:291); Phyre draw `0060B980` (Character-Rendering/character-render-object.md:320); material `FindShaderParameter` `0018D240` (CONTRACT-character-transform-publish.md:312-313); the resource/handle layer `002ED570`, `003AB7F0`, `0020E600`/`0020E620` (CONTRACT-render-record-pool-lifecycle.md:278, 826-830); the shadow-object pools `003B56D0`/`003B6000`, `003AF340`/`003AFBE0` (CONTRACT-render-record-pool-lifecycle.md:246-249); typed-handle predicates and group bits `003AED20` (Character-Rendering/how-a-character-is-lit.md:89, 105, 257); the status page (gather details, Character-Rendering/how-a-character-is-lit.md:135-136); weather (light makers, Character-Rendering/how-a-character-is-lit.md:64-65); the model instance `004FD4B0` (Character-Rendering/how-a-character-is-lit.md:211).

### 1.3 [RA] The character render record array, render events, focus point and track pick

Short names in this part: **CRR** = `Character-Render-Records/the-character-render-record-array.md`; **RES** = `Character-Render-Records/render-event-selection-evidence.md`; **FOC** = `Character-Render-Records/the-focus-point-of-a-character.md`; **TRK** = `Character-Render-Records/how-a-presentation-entry-picks-its-track.md`.


#### RA — Entry points

| entry (size) | callers as stated | what it does | cite |
|---|---|---|---|
| `003325C0` (12 B) | `0022A0B0` once at boot | `lea rcx,[022C6F30]`, tail-jumps to `003325D0` | Character-Render-Records/the-character-render-record-array.md:937-939, :947 |
| `003325D0` CharacterRenderSystem_AllocateAndInitialize (139 B) | `003325C0` | stores ctx→`022C6F20`, allocates `0x48930`→`022C6F28`, then `0041E550`→`0041E3A0`→`004269A0`→`00426480` | Character-Render-Records/the-character-render-record-array.md:57-65, :159, :948 |
| `0041E3A0` RenderResourceRoot_InitializeSubcontainers (233 B) | `003325D0` | eleven-arm battery; `root+DA8 = root+160`; `0051BA20` at `0041E42F`, `0051B9D0` at `0041E470` (64 ref slots) | Character-Render-Records/the-character-render-record-array.md:950; Character-Render-Records/render-event-selection-evidence.md:201-206, :578-580 |
| `004269A0` CharacterRenderSystem_Initialize (741 B) | `003325D0` | `0041F730`×160, tail seeds (head/tail −1, cursor 0), ~25 handler registrations, `+0x48818 |= 5`, config floats (34.0, 4.0, 1/6) | Character-Render-Records/the-character-render-record-array.md:951, :562-567, :605-616; Character-Render-Records/render-event-selection-evidence.md:494-497 |
| `00426480` PublishRootPointer (30 B) | `003325D0` tail call `00332656` | stores encoded pointer at tail +0x30 (but see RA.CV-1) | Character-Render-Records/the-character-render-record-array.md:76-81, :160, :515, :952 |
| `0041F730` CharacterRenderRecord_ResetDefaults | `004269A0`, removers | `memset(record,0,0x740)` then seeds (full default map) | Character-Render-Records/the-character-render-record-array.md:376, :588 |
| `004279B0` record allocator | `0042FB80` (sole caller) | refuses at 160, cursor round-robin, links into pending list | Character-Render-Records/the-character-render-record-array.md:465-491, :564-567, :653-656 |
| `0042FB80` | not stated | writes instance key `cn\plan`+byte at record +0x1C, name at +0x3C, refuses if live≥160 | Character-Render-Records/the-character-render-record-array.md:653-658 |
| `00428710` promoter | via `0042ED60` (`00332660`) | per pending record: `0041FCF0` bind, +0x414 from tail+0x28, +0x114 from `003B56D0`, clear +0x290 bit 0, move pending→active | Character-Render-Records/the-character-render-record-array.md:569-575, :649-651 |
| `00427C90` active remover / `00429140` pending remover (358 B) | not stated / not stated | unlink, `liveCount--`, cursor reset at 0, `0041F730` | Character-Render-Records/the-character-render-record-array.md:577-590 |
| `00426420` ReconcileActiveRecords | not stated (per frame) | gate tail+0x42==1 && +0x43==0, walk active list, call `00426340` | Character-Render-Records/the-character-render-record-array.md:91-96, :239-245, :667-669 |
| `00426340` SyncShadowObjects (211 B) | `00426420` | shadow pool-A/B mode bits and LOD (4 steps) | Character-Render-Records/the-character-render-record-array.md:162, :672-681 |
| `00427DE0` RenderRecords_ProcessDirtyState | `0042ED60` (arg 1, from `00332660`), `00426090` RenderSystem_UpdateCharacterRecords (arg 0, from `003323D0`) — "the only two call sites" | five sweeps of +0x290/+0x294, tail commit | Character-Render-Records/the-character-render-record-array.md:718-737 |
| `0042ED60` | tail-jmp from `00332660` | clears tail+0x18 bit 5, runs remover+promoter, rebinds | Character-Render-Records/the-character-render-record-array.md:648-651 |
| `00424080` Movement_ModifyHeadingSpeedForObjectState (427 B) | only `002E4380` (Movement) | coast-down latch and event-index speed rules on caller's heading/speed pointers | Character-Render-Records/the-character-render-record-array.md:107-153, :294-299, :309-315 |
| `00332440` / `00332510` (124 B) | thunk `00332420`, frame driver `001EC060` | named-scope stages: preprocessing `004264A0`, shadow `00428E40`, draw objects `0041E4D0`, after emission `00425DC0`, draw clip `00426500` | Character-Render-Records/the-character-render-record-array.md:407, :1094 |
| `004288E0` (87 B) | not stated | walks active list; `003E43D0` on records with +0x290 bit 1 clear | Character-Render-Records/the-focus-point-of-a-character.md:59-61 |
| `003E43D0` focus update (814 B) | `004288E0` | computes focus point +0x670, slide, smoothed +0x680 | Character-Render-Records/the-focus-point-of-a-character.md:57-83 |
| `003E5810` focus getter (160 B) | look solver, viewer-matrix bodies, 4 actor services, 2 UI | `out = M*(+0x680)+(+0x670)` | Character-Render-Records/the-focus-point-of-a-character.md:87-93 |
| `0051B9E0`→`0051F240` (5 B thunk, 138 B) | `00424080`, `00424230`, `004235C0`, `00423050`, `00423570`, `00423AB0` | entry lookup by id (×0x30), lazy cache rebind | Character-Render-Records/render-event-selection-evidence.md:36-53; Character-Render-Records/the-character-render-record-array.md:322-329 |
| `00424230` (77 B) | `004235C0` sel 0 | permissive default: entry +2C8 bit 12 | Character-Render-Records/render-event-selection-evidence.md:75-78 |
| `004235C0` selection policy (459 B) | `0041FCA0`, `00424550` (sel 0), `00424D80` | event priority / kind gating | Character-Render-Records/render-event-selection-evidence.md:92-121 |
| `0041FCA0` getter | not stated | returns +CC or +CE | Character-Render-Records/render-event-selection-evidence.md:134-149 |
| `00424550` (799 B), `00424D80` (1,607 B) | per-frame path `00427DE0`→`0042AC30`→`00423B10`→`00424D80` | admission via `0051BA80`; store event into +0xCC / entry +0x31C | Character-Render-Records/render-event-selection-evidence.md:160-165, :184; Character-Render-Records/the-character-render-record-array.md:385-388, :397 |
| `0051BA80` admission | `00424550`, `00424D80` only | builds 0x3A0 payload, `0051F080` | Character-Render-Records/render-event-selection-evidence.md:184, :281-288 |
| `0051BA40` release | callers reset stored id to −1 | `0041CF00` then `0051F190` | Character-Render-Records/render-event-selection-evidence.md:184, :267-272 |
| `0051B9F0` rebase | not stated | `0051F620` re-cache all + `0051F580` callback `0051BC00→0041CA70` | Character-Render-Records/render-event-selection-evidence.md:290-294 |
| `0051B970` (96 B) entry update | not stated | three walks, phase word `02CA83F4` = 0/1/2 | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:149-154 |
| drains `0041DA90`, `0041E000`, `0041E1D0` | not stated | walk command records, `call [01EFFAF0+id*16]` | Character-Render-Records/render-event-selection-evidence.md:501-507 |
| `0041CD30` track setup (357 B), `0041CFC0` reset (325 B), `0041C9A0` finder (203 B) | `0041D220` init (for stream 0), reset callers not stated | track state setup/rewind/find | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:61-84; Character-Render-Records/render-event-selection-evidence.md:398-405 |
| command handlers `00417920` (0x01), `00417110` (0x0B), `00418600` (0x0A), `00417A80` (0x03), `00417D00` (0x08), `00417CC0` (0x06), `0041CEC0` dirty mark | drains via `01EFFAF0` | track switch etc. | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:86-145 |
| 25 `0052xxxx` handlers (table) | invokers `004174F0+` via banks `02CA4410`/`02CA4670` | per-id record work | Character-Render-Records/render-event-selection-evidence.md:531-557 |

#### RA — Inputs and outputs (record layouts)

Allocation (Character-Render-Records/the-character-render-record-array.md:180-192, :555-567, :605-616, :642-651, :987-1019):

| offset | size | meaning | cite |
|---|---|---|---|
| base+0 .. +0x487FF | 160 × 0x740 | records | Character-Render-Records/the-character-render-record-array.md:181 |
| tail +0x00 / +0x04 | i32 | active head / tail, −1 empty | Character-Render-Records/the-character-render-record-array.md:562-563 |
| tail +0x08 / +0x0C | i32 | nextFreeIndex (cursor, wraps at 160) / liveCount (refuse at 160) | Character-Render-Records/the-character-render-record-array.md:564-565 |
| tail +0x10 / +0x14 | i32 | pending head / tail | Character-Render-Records/the-character-render-record-array.md:566-567 |
| tail +0x18 | u32 | flags: b0 distance cull, b2 set/unused, b4 external fade, b5 active-list dirty | Character-Render-Records/the-character-render-record-array.md:642-651 |
| tail +0x1C / +0x24 | f32 | fade start 34.0 / width 4.0; `sin(((start+width−d)/width)·π/2)` | Character-Render-Records/the-character-render-record-array.md:605-614 |
| tail +0x28 | f32 | 1/6 → record +0x414 | Character-Render-Records/the-character-render-record-array.md:615-631 |
| tail +0x2C | i32 | focus record index or −1 | Character-Render-Records/the-character-render-record-array.md:635-639 |
| tail +0x30 | u32 | encoded image-relative pointer (00426480) | Character-Render-Records/the-character-render-record-array.md:189, :80 |
| tail +0x42 / +0x43 | u8 | gateEnabled ==1 / gateInhibit ==0 | Character-Render-Records/the-character-render-record-array.md:190-191 |
| tail +0x54 | — | `0x80404040`, no reader | Character-Render-Records/the-character-render-record-array.md:639-640 |
| tail +0x70..+0x12F | 192 B | no access | Character-Render-Records/the-character-render-record-array.md:1012-1015 |
| tail: 24 fields, 9 named, 15 UNRESOLVED | | | Character-Render-Records/the-character-render-record-array.md:999-1006 |

Record (0x740) — principal fields:

| off | size | meaning | cite |
|---|---|---|---|
| +0x000 | i16 | id, −1 free | Character-Render-Records/the-character-render-record-array.md:202 |
| +0x002 / +0x004 | i16 | prev / next active index | Character-Render-Records/the-character-render-record-array.md:203-204, :569-570 |
| +0x006 | i16 | owner/parent link (see RA.CV-4) | Character-Render-Records/the-character-render-record-array.md:205, :903, :1061-1062 |
| +0x008 / +0x00A | i16 | child chains (see RA.CV-4) | Character-Render-Records/the-character-render-record-array.md:903, :1043-1044 |
| +0x010 | ptr64 | encoded context pointer (dword readers use low half) | Character-Render-Records/the-character-render-record-array.md:206, :220 |
| +0x01C / +0x03C | 8 B / 32 B | instance key `cn\plan`+byte / model container name | Character-Render-Records/the-character-render-record-array.md:653-658 |
| +0x064 | i16 | model-instance selector (−1 none) | Character-Render-Records/the-character-render-record-array.md:1080-1083, :905 |
| +0x090..+0x09E | 8×i16 | @FLD entries | Character-Render-Records/the-character-render-record-array.md:376 |
| +0x0C0 | u8 | b1 LOD scripted, b2 alpha scripted, b3-4 shadow kind | Character-Render-Records/the-character-render-record-array.md:677-681, :698-706 |
| +0x0C4 / +0x0C8 | i32 | presentation entry ids (−1 none) | Character-Render-Records/the-character-render-record-array.md:207; Character-Render-Records/render-event-selection-evidence.md:184 |
| +0x0CC / +0x0CE | i16 | current / alternate render event (kind nibble + 12-bit index) | Character-Render-Records/the-character-render-record-array.md:382-384; Character-Render-Records/render-event-selection-evidence.md:93, :134-137 |
| +0x114 / +0x118 | handle | shadow pool A (0xE0 ×160 at `02B40528`) / pool B (0x70 ×32 at `02B3F570`) | Character-Render-Records/the-character-render-record-array.md:683-698 |
| +0x120..+0x12C, +0x250..+0x258 | f32 | pitch,yaw,roll,1 / previous | Character-Render-Records/the-character-render-record-array.md:223-229 |
| +0x180 / +0x1C0 | mat4 | model rotation / identity | Character-Render-Records/the-character-render-record-array.md:227, :376 |
| +0x260..+0x26C | f32 | scaleVec, uniformScale | Character-Render-Records/the-character-render-record-array.md:854-857 |
| +0x274 / +0x27C | f32 | scripted shadow alpha / LOD | Character-Render-Records/the-character-render-record-array.md:703-708 |
| +0x284 | u32 | object flags (b2 live, b6, b7, b12, b14 char-dir, b26/27, b30 skip, 0x08000000 latch) | Character-Render-Records/the-character-render-record-array.md:209, :675, :664, :724 |
| +0x290 / +0x294 | u32 | dirty words (56-block census) | Character-Render-Records/the-character-render-record-array.md:718-776 |
| +0x2B0..+0x2BC / +0x3BC..+0x3C8 | f32 | flush / staged params | Character-Render-Records/the-character-render-record-array.md:811-829 |
| +0x304 | u32 | presentationFlags (b10, b11, b12-13 shadow kind) | Character-Render-Records/the-character-render-record-array.md:840-844, :1093, :1108-1109 |
| +0x400 / +0x408 | ptr / u16 | FCP payload ptr / selector | Character-Render-Records/the-character-render-record-array.md:845-850 |
| +0x414 | f32 | 1/6, write-only on PC | Character-Render-Records/the-character-render-record-array.md:615-631 |
| +0x457 | i8 | stop-frame counter | Character-Render-Records/the-character-render-record-array.md:210 |
| +0x4B8..+0x4BB | u8 | cached selector choices for kinds 0,2,0xA,0x10 | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:105-108 |
| +0x4C0..+0x50F | 10×8 B | Q12 channels {base,delta,progress,step} | Character-Render-Records/the-character-render-record-array.md:873-877 |
| +0x610..+0x62C | f32/u16 | heading/speed cache; latch flags | Character-Render-Records/the-character-render-record-array.md:211-217 |
| +0x660 / +0x690 | vec3 | last focus position kind 1 / kind 0 | Character-Render-Records/the-focus-point-of-a-character.md:67-71 |
| +0x66C | u8 | two 4-bit countdowns (hi kind 1, lo kind 0) | Character-Render-Records/the-focus-point-of-a-character.md:67-68 |
| +0x66D | u8 | b0 keep bone height, b1 snap second vector | Character-Render-Records/the-focus-point-of-a-character.md:50, :65, :82 |
| +0x670 / +0x680 | vec3 | focus point / smoothed vector | Character-Render-Records/the-focus-point-of-a-character.md:66, :81 |
| +0x6A8 | dword | kind returned by `003E6070` (always 0) | Character-Render-Records/the-focus-point-of-a-character.md:82-83 |
| +0x6D8 / +0x6DC | | selector entry bit 13 / choice | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:104 |
| +0x734 / +0x73C | f32 / i | per-model constant by name / 1 for four models | Character-Render-Records/the-character-render-record-array.md:376 |

Presentation entry (0x3A0 payload) and container:

| off | meaning | cite |
|---|---|---|
| container +4 low 2 bits kind; +8 table; +10 capacity (64); +14 count; +18 cursor; +1C/+20 head/tail ids | Character-Render-Records/render-event-selection-evidence.md:221-228 |
| node 0x30: +0 state (b0 occupied, b1 refresh); +4 id = `slot|0x10000`; +8/+C links; +10 source; +18 cache; +20 offset | Character-Render-Records/render-event-selection-evidence.md:230-237, :249 |
| payload +0C flags (b6 switch allowed, b7 waiting, b9 dirty, b12, b13, b14, b18; `|= 00100001` at init) | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:38; Character-Render-Records/render-event-selection-evidence.md:340 |
| payload +18/+20 primary track ptr / index (`+18 = +30 + 0xA0*sign32(+20)`) | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:39; Character-Render-Records/render-event-selection-evidence.md:300 |
| payload +28 count (=4), +30 four 0xA0 subrecords | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:41-42; Character-Render-Records/render-event-selection-evidence.md:392-396 |
| payload +2C8 bit 12 completion flag | Character-Render-Records/render-event-selection-evidence.md:76, :193 |
| payload +2DA/+2DC selector arg / kind; +2E0 owning record; +2E8 bits 0-2; +31C event word; +338/+330 group id/table; +340 rate; +354 blend factor; +358 0x10; +368 authored stream; +378/+37C @FRM; +380/+384 snapshot; +388 playing track | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:43-49, :139-144; Character-Render-Records/render-event-selection-evidence.md:319-337, :343-356, :375-381 |
| track state 0xA0: +00 id, +04 state word, +18 0x1E0000, +20 30.0, +50/+52 −1, +5E hold countdown, +68 −1, +80 track, +84 header off, +88 start cursor, +8C cursor, +90 marker, +94 last choice, +95 active, +96 flags, +98/+9C floats | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:54-59, :136; Character-Render-Records/render-event-selection-evidence.md:393-395 |
| track header: byte +0 kind (1 primary), +3 command count, word +4 next distance, commands from +6, len `word[+2]>>6` | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:51-52 |
| `01F00410` priority bytes 0..0x58 (values 0..4), 0x59-0x5F zero | Character-Render-Records/render-event-selection-evidence.md:193 |
| `01EFFAF0` 16-byte `{invoker, flag}`, id `word & 0x7F` clamped 0x4B | Character-Render-Records/render-event-selection-evidence.md:499-511 |
| `02CA4410`/`02CA4670` handler banks of 75 slots; `02CA4668` single pointer | Character-Render-Records/render-event-selection-evidence.md:491-493 |

#### RA — State (globals and objects, with lifetime)

| global | size / lifetime | cite |
|---|---|---|
| `022C6F28` pool pointer | set once by `003325D0`; also re-stored by `00332440` | Character-Render-Records/the-character-render-record-array.md:172, :407 |
| `022C6F20` render context | `003325D0` first; `00332440`/`00332510` restore | Character-Render-Records/the-character-render-record-array.md:173, :1094 |
| `01DFE0B4` time base | "u32" (Character-Render-Records/the-character-render-record-array.md:174); value not stated on these pages | Character-Render-Records/the-character-render-record-array.md:174; Character-Render-Records/the-focus-point-of-a-character.md:69; Character-Render-Records/how-a-presentation-entry-picks-its-track.md:136-137 |
| `02B40528` shadow pool A (0x8C00) + generation `02B40520`, mask `02B40524` | `003B6890` from Initialize; wrap 0xFFFFFF→1 | Character-Render-Records/the-character-render-record-array.md:400, :684-686, :966 |
| `02B3F570` pool B (32×0x70) | `003AFCD0` | Character-Render-Records/the-character-render-record-array.md:695-697, :967 |
| `01F20C80` ease table (60, count `01F2053C`; 120 under FrameLimit=60) | boot `001EDDC0`→`0033F020` | Character-Render-Records/the-focus-point-of-a-character.md:75-76 |
| `02CA4410`/`02CA4670` banks, `02CA4668` | zeroed by `0041CCA0`, filled by `004269A0` and `002EA320` | Character-Render-Records/render-event-selection-evidence.md:218, :491-497, :559-565 |
| `02CA83F4` phase word | `0051B970`, back to 0 | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:149-152 |
| record init values | ResetDefaults map; focus fields +0x660..+0x6A8 only by the memset (not stated explicitly) | Character-Render-Records/the-character-render-record-array.md:376 |

#### RA — Order (what runs when, and what triggers it)

| when | what | cite |
|---|---|---|
| boot | `0022A0B0`→`003325C0`→`003325D0` (alloc, battery, Initialize, publish) | Character-Render-Records/the-character-render-record-array.md:937-952 |
| frame driver `001EC060` / `00332420` | `00332440(ctx,array,stage)`: 0 preprocessing `004264A0`, 1 shadow `00428E40`, 2 draw objects `0041E4D0` + after emission `00425DC0`, 3 draw clip; `00332510` runs 0,2 back to back | Character-Render-Records/the-character-render-record-array.md:407, :1094 |
| `003323D0` | `00426090` UpdateCharacterRecords → `00427DE0`(0); `003B5890` tween step at `00426112` | Character-Render-Records/the-character-render-record-array.md:691, :721-723 |
| `00332660`→`0042ED60` | remover, promoter, `00427DE0`(1) | Character-Render-Records/the-character-render-record-array.md:648-651, :721-722 |
| `00427DE0` | five passes, fixed bit order, tail commit only when arg && work | Character-Render-Records/the-character-render-record-array.md:718-747 |
| promoter | a record allocated this frame is not walked until the promoter runs | Character-Render-Records/the-character-render-record-array.md:574-575 |
| `004288E0` | focus update for records with +0x290 bit 1 clear | Character-Render-Records/the-focus-point-of-a-character.md:59-61 |
| Movement `002E5030`→`002E4380`→`00424080` | per movement update | Character-Render-Records/the-character-render-record-array.md:309-315 |
| order of `0051B970` relative to the above | not stated | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:149 |

#### RA — Dependencies

Movement (`06`, heading-speed page) Character-Render-Records/the-character-render-record-array.md:335-339; Party focus handle `002E9B80` Character-Render-Records/the-character-render-record-array.md:637-638; resource layer (`002ED570`, `003AB7F0`, `00409xxx`, chunk finder) Character-Render-Records/render-event-selection-evidence.md:364-382, Character-Render-Records/the-focus-point-of-a-character.md:175; skeleton (`003710E0`, `00421FF0`, `00370F60`) Character-Render-Records/the-focus-point-of-a-character.md:54, Character-Render-Records/the-character-render-record-array.md:709; battle unit callbacks id 4/6/0xC (`002EA320`) Character-Render-Records/render-event-selection-evidence.md:559-565; script verbs `setshadowlod`/`setshadowalpha` Character-Render-Records/the-character-render-record-array.md:703-708; boot frame-limit `001EDDC0` Character-Render-Records/the-focus-point-of-a-character.md:177; CoreRT image-pointer pair `0020E600`/`0020E620` Character-Render-Records/the-character-render-record-array.md:923-928; authored command handlers page Character-Render-Records/how-a-presentation-entry-picks-its-track.md:27.

### 1.4 [RG] Rig controllers, fades, status looks, bone trails and the staged look

Short names in this part: **FADE** = `Character-Render-Records/how-a-character-fades-the-ten-channels.md`; **STAT** = `Character-Render-Records/how-a-status-shows-on-a-character.md`; **TRAIL** = `Character-Render-Records/the-bone-trails.md`; **RIG** = `Character-Render-Records/the-rig-of-seventeen-controllers.md`; **LOOK** = `Character-Render-Records/the-staged-look-command.md`.


#### RG — Entry points

| entry (address, size) | callers as stated | what it does | cite |
|---|---|---|---|
| `003E5D60` ramp start (182 B) `(record, channel, float target, int frames)` | 00428940 forwarder, 0042E850, 0042E1F0, 00428C40 | collapse base, `delta = target*4096 - base`, `step = 0x1000/(max(frames,1)*[01DFE0B4])`, progress = step (0 for channel 1), +1 step if `01F82E38` != 0 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:61-66 |
| `003E5D00` set (44 B) `(record, channel, float value)` | ResetDefaults (all ten, 1.0), 0042E1F0, 0042F880, 00428940 | base = value*4096; other words (disputed, RG.CV-1) | Character-Render-Records/how-a-character-fades-the-ten-channels.md:68-69, :570-573 |
| `003E5D30` (34 B) `(record)` | 004215A0, 004218A0 | channels 0, 1, 4 := 1.0 (three qword stores of 0x1000) | Character-Render-Records/how-a-character-fades-the-ten-channels.md:70, :742 |
| `003E4370` step (88 B) `(record)` | "the root and the child animation-presentation-phase updates" | per-channel step (disputed finish rule, RG.CV-2) | Character-Render-Records/how-a-character-fades-the-ten-channels.md:72-75, :677-681 |
| `00428940` forwarder (20 B) `(record, channel, value, frames)` | five second-block status looks (ch 5), `002E8B10` (ch 2) | frames <= 1 -> 003E5D00; else, record non-null -> 003E5D60 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:114-118; Character-Render-Records/how-a-status-shows-on-a-character.md:473-476 |
| `004293C0` forwarder (67 B) `(record, channel, value, frames, flag)` | authored command 0x23 `00520180` | flag 1 redirects to attached child `+8`; channel 1 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:119-122 |
| `00428C40` (131 B) `(record, r, g, b, a, frames)` | `002E84B0` (`rgbatrans` 03B2), `002E8500` (`puppetrgbatrans` 0535) | ramps channels 6-9 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:90, :126-128 |
| `002E8B10` (77 B) `(actor, value, frames)` | time-stop per-actor pass `00226640` | channel 2 through 00428940 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:86 |
| `003E48E0` evaluator (604 B) `(record, selector)` | 0042D050 (0x0D, 0x0E), 0042FB20 (0x0B), three Presentation bodies (ch 4) | selector table 0..9 / 0x0B / 0x0D / 0x0E | Character-Render-Records/how-a-character-fades-the-ten-channels.md:132-148 |
| `003E4240` composite (269 B) `(record, parent)` | 0042CBF0, 0042D050 | six-channel product -> `+0x4B4`, x parent's `+0x4B4` | Character-Render-Records/how-a-character-fades-the-ten-channels.md:150-152 |
| `003E4730` composite scalar (66 B); sibling `003E4780` | 0042CBF0, 0042D050 | float opacity (formula disputed, RG.CV-3) | Character-Render-Records/how-a-character-fades-the-ten-channels.md:153-155, :670-674 |
| `003E51F0` vector (701 B) `(record, float out[4])` | 0042CBF0, 0042D050 | channels 6..9 / 4096 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:157-160 |
| `0042E850` distance fade and cull (1,238 B) | `0042D7A0`, per-record callback of the distance-fade system phase (taken by lea at 0042650E) | cull bits of `+0xD3`, channels 0 and 4 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:84, :89, :230-237, :304-321 |
| `0042E1F0` (269 B) | not stated | channel 1 attached-piece visibility | Character-Render-Records/how-a-character-fades-the-ten-channels.md:85 |
| `0042F880` (608 B) | dirty bit 19 of `+0x290` | pending attachment, channel 1 to 0.0 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:94-111 |
| `0042CBF0` child frame (884 B) | not stated (entry conditions only) | channels -> model instance for attached record | Character-Render-Records/how-a-character-fades-the-ten-channels.md:164-192 |
| `0042D050` root frame (1,776 B) | not stated (entry conditions only) | channels -> instance, shadow, aux handles, two alphas | Character-Render-Records/how-a-character-fades-the-ten-channels.md:348-398 |
| `0041EC00` projected origin (480 B) | root records, orphaned pieces | `+0x2D0..+0x2DC` | Character-Render-Records/how-a-character-fades-the-ten-channels.md:200-214 |
| `0042FB20` (85 B) `(handle)` | not stated | selector 0x0B as float, 1.0 for -1/dead | Character-Render-Records/how-a-character-fades-the-ten-channels.md:146-147 |
| script verbs `setcharclipall` 0x156, `setcharclipdistance` 0x327 (00348B00), 0x33E (00348700), 0x33F (003497D0), 0x340 (00348F20) | scripts | veto bit / clip distance / fade range | Character-Render-Records/how-a-character-fades-the-ten-channels.md:283, :291-296 |
| `003E7650` status push (1,566 B) | `World_UpdateSimulationTick` 00314020, one site 00314341 | 32 records, change masks, per-bit arms, two block updates | Character-Render-Records/how-a-status-shows-on-a-character.md:56-59, :414; Character-Render-Records/the-rig-of-seventeen-controllers.md:337 |
| `0046FFA0` add (85 B) / `00470050` remove (97 B) | push arms | colour-list mask, lowest set index -> `+5` | Character-Render-Records/how-a-status-shows-on-a-character.md:78-80 |
| `0046FD00` colour-look update (615 B) | push | state machine | Character-Render-Records/how-a-status-shows-on-a-character.md:83-101 |
| `0051DBF0` add (109 B) / `0051DDC0` remove | push arms | second-block mask -> bytes +0x19/+0x31/+0x33 | Character-Render-Records/how-a-status-shows-on-a-character.md:237-244 |
| `0051E3A0` second-block update (362 B) | push | two channels + Stop | Character-Render-Records/how-a-status-shows-on-a-character.md:246-253 |
| look installers / steps: 004703F0+004700E0 tint; 00470AA0 Stone; 00470780 Petrify; 00470660+00470EB0 Berserk; 00470590+00470B70 Doom; 004704C0+00470230 HP Critical; 0051DC90 Invisible; 0051E0A0 idx 2; 0051E170 Slow; 0051DE30 Immobilize | 0046FD00 / 0051E3A0 | per look | Character-Render-Records/how-a-status-shows-on-a-character.md:129-140, :158-231, :261-292 |
| `00428CD0` record mode (269 B) -> `00504D20` (7 B) | look installers | mode to instance byte `+0xBA`, and subtree | Character-Render-Records/how-a-status-shows-on-a-character.md:99-101 |
| `00504D30` variant binder (310 B) | "the record-side routine that ensures a character's bindings, not read" (STAT); `003E7210` per element (TRAIL) | 20 binding slots | Character-Render-Records/how-a-status-shows-on-a-character.md:112-121; Character-Render-Records/the-bone-trails.md:465 |
| `003ABD50` light gather (950 B) | not stated | reads `+0x5EC`, six lights | Character-Render-Records/how-a-status-shows-on-a-character.md:307-324 |
| `00520160` (23 B) authored command 0x11 | command table | `+0x3D0` := byte +2, `+0x294` bit 24 | Character-Render-Records/the-bone-trails.md:74 |
| `00425E70` fan-out (202 B) | dirty pass 00427DE0 at 0042858C | applies to record, child, hierarchies | Character-Render-Records/the-bone-trails.md:75-76 |
| `003E6770` build/switch off (276 B) `(record, enable)` | 00425E70 | creates up to 4 trail entries into `+0x438..+0x444` | Character-Render-Records/the-bone-trails.md:77 |
| `0051C270` init (265 B) | render root subcontainer init | pool alloc, header zero, image reg, template build | Character-Render-Records/the-bone-trails.md:91-94, :180-181 |
| `0051CC30` create (385 B), `0051CC10` off (26 B), `0051BC10` release (93 B), `0051CDC0` opacity (27 B) | 003E6770; release: 003E74C0, 0041E860, 004213E0; opacity: 003E70F0 | pool lifecycle | Character-Render-Records/the-bone-trails.md:83-87, :96-115; Character-Render-Records/how-a-character-fades-the-ten-channels.md:378-380 |
| `0051C3C0` update (2,128 B) | "the render root's presentation update", once a frame | per-entry update | Character-Render-Records/the-bone-trails.md:124-150 |
| `0051BC70` draw (1,525 B) | tail jump from 0041E4D0 at 0041E4EF | layer 3 effects, then trails via VU1 program 0053F490 | Character-Render-Records/the-bone-trails.md:152-170, :23-26 |
| `003E1350` off / `003E1610` on (629 B / n.s.) `(rig, n)` | dirty-pass wrappers 0042DD90, 0042BDE0, 0042DCD0, 0042D8B0, 0042E690; countdown | n > 16 rejected; tail-jump to controller on/off | Character-Render-Records/the-rig-of-seventeen-controllers.md:93-97, :500-508 |
| verb setters 002E8570, 002EDF30, 002EE0D0, 002EE130, 002EDE70, 002EDED0, 002EDDC0 | verbs (Character-Render-Records/the-rig-of-seventeen-controllers.md:104-106, :133) | `+0x304` bit, dirty bit, timer | Character-Render-Records/the-rig-of-seventeen-controllers.md:102-111, :133-137 |
| `0042EE90` countdown (254 B) | `00428F80` (82 B) system phase over the active list | timers +0x640/+0x644/+0x648 | Character-Render-Records/the-rig-of-seventeen-controllers.md:117-129 |
| `003E00C0` rig frame (1,631 B) | not stated | sway, solve order, apply order | Character-Render-Records/the-rig-of-seventeen-controllers.md:228-242 |
| `003DFE70` (171 B) `(rig, index, target, frames)` | authored command 0x24 | rotator ramp | Character-Render-Records/the-rig-of-seventeen-controllers.md:159-163 |
| `00429920` apply (299 B) | `RenderRecords_ProcessDirtyState` | look command to rig of record, child, chains | Character-Render-Records/the-staged-look-command.md:48-55 |
| `003E37F0` applier (909 B) `(rig, command)` | 00429920, 0042D970 | request word | Character-Render-Records/the-staged-look-command.md:61-88 |
| 18 forwarders (`add rcx,0x580; jmp builder`) -> 18 builders (17-48 B) | actor-service layer | stage bits | Character-Render-Records/the-staged-look-command.md:43-46 |
| `003E37E0` clear (11 B) | not stated | memset 0x50 | Character-Render-Records/the-staged-look-command.md:57, :392-394 |
| `002EC3F0` dispatcher (263 B) | 002E28E0, 002E3110, 002E64E0, 002EAAA0, 002EBE50 | steering record -> one of six services | Character-Render-Records/the-staged-look-command.md:108-124 |
| `003E3D70` rig rebind (961 B) | `00372350` (84 B) only | resets every slot | Character-Render-Records/the-staged-look-command.md:134-162, :164-167 |
| `003E0910` denybonephysical (154 B) `(rig, deny)` | applier bit 0 | byte `+0x62`; restarts slots +4, +0x38 on lift | Character-Render-Records/the-staged-look-command.md:177-180 |
| `003E2810` eyemove (215 B), `003E28F0` eyemovediff (184 B) | applier bits 27, 28 | eye object | Character-Render-Records/the-staged-look-command.md:182-186 (args disputed RG.CV-10) |
| `005154B0` look controller reset (329 B) | four callers, none read | | Character-Render-Records/the-staged-look-command.md:188-196 |

#### RG — Inputs and outputs (record layouts)

Fade channel (`Character-Render-Records/how-a-character-fades-the-ten-channels.md:51-58`): ten 8-byte records at render record `+0x4C0`..`+0x50F`:

| off | size | meaning | cite |
|---|---|---|---|
| +0 | s16 | base, Q12 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:52 |
| +2 | s16 | delta = target - base | Character-Render-Records/how-a-character-fades-the-ten-channels.md:53 |
| +4 | s16 | progress 0..0x1000 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:54 |
| +6 | s16 | step; 0 = at rest | Character-Render-Records/how-a-character-fades-the-ten-channels.md:55 |

value = base + ((delta*progress)>>12) (Character-Render-Records/how-a-character-fades-the-ten-channels.md:58). Channel owners: 0 `+0x4C0` distance; 1 `+0x4C8` piece; 2 `+0x4D0` time-stop fade; 3 `+0x4D8` none; 4 `+0x4E0` viewer-inside; 5 `+0x4E8` Invisible; 6-9 `+0x4F0..+0x508` rgbatrans (Character-Render-Records/how-a-character-fades-the-ten-channels.md:82-90). Selectors 0x0B = ch0..4, 0x0D = ch1,2,3,5, 0x0E = ch0..5 (Character-Render-Records/how-a-character-fades-the-ten-channels.md:135-140).

Other render-record fields written/read by these pages:

| off | size | meaning | cite |
|---|---|---|---|
| +0x4B4 | s16 | composite Q12 (x parent's) | Character-Render-Records/how-a-character-fades-the-ten-channels.md:150-152 |
| +0x49C | f32 | final opacity = composite scalar x rgbatrans alpha | Character-Render-Records/how-a-character-fades-the-ten-channels.md:178, :364-365 |
| +0x22C, +0x2EC | f32 | 0..255 factors of the scalar; +0x2E0..+0x2EC written by 0041E960, clamped 255 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:154, :644-651 |
| +0x210 / +0x220 | vec | colour / second colour -> instance +0x90 / +0xA0 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:179-181 |
| +0x2D0..+0x2DC | vec4 | projected origin; +0x2D8 sort depth; child = parent +2.0 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:171-172, :203-209 |
| +0xD3 | byte | cull bits 0 outside, 1 too far, 3 behind | Character-Render-Records/how-a-character-fades-the-ten-channels.md:304, :312-316 |
| +0x284 | u32 | bit 2 live-root cond., bit 3 not culled, bit 4 display requested, bit 5 (no live source), bit 6 chain, bit 10 pending, bit 11, bit 13 matrix choice, bit 14, bit 21, bit 23, bit 26 parent colours, bit 27 owner hide | Character-Render-Records/how-a-character-fades-the-ten-channels.md:85, :186, :240-267, :314-316, :350, :389 |
| +0x290 | u32 | dirty bits: 1 (countdown skip), 4, 5, 13, 14, 15, 16, 19, 28 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:94, :254, :263; Character-Render-Records/the-rig-of-seventeen-controllers.md:102-106, :124, :134; Character-Render-Records/how-a-status-shows-on-a-character.md:71 |
| +0x294 | u32 | dirty bits 24 (trails), 26 (00428AF0) | Character-Render-Records/the-bone-trails.md:74; Character-Render-Records/how-a-status-shows-on-a-character.md:484 |
| +0x304 | u32 | requested-state: bit 1 display, bit 2 (never touched), bit 5 Stone/Stop, bit 6 lip, bit 7 nod, bit 8 eyes, bit 15 head shake, bit 16 body shake, bits 17-19 (00428AF0) | Character-Render-Records/how-a-character-fades-the-ten-channels.md:254-264; Character-Render-Records/how-a-status-shows-on-a-character.md:71, :482-484; Character-Render-Records/the-rig-of-seventeen-controllers.md:102-107, :134 |
| +0x3CC / +0x3CE | word | attachment slot id / owner record index | Character-Render-Records/how-a-character-fades-the-ten-channels.md:95-96 |
| +0x3D0 | byte | trail state from command 0x11 | Character-Render-Records/the-bone-trails.md:74 |
| +0x3F4 / +0x3F5 / +0x3F6 | byte/byte/word | command 0x13 flags / piece selector / target | Character-Render-Records/the-rig-of-seventeen-controllers.md:155 |
| +0x40B | byte | bits 0-1 piece rule; bits 5, 6, 7 timer active | Character-Render-Records/how-a-character-fades-the-ten-channels.md:85; Character-Render-Records/the-rig-of-seventeen-controllers.md:125, :364-375 |
| +0x438..+0x444 | 4 x dword | trail handles (0xFFFF = none) | Character-Render-Records/how-a-character-fades-the-ten-channels.md:379; Character-Render-Records/the-bone-trails.md:77 |
| +0x4B7 | byte | bit 5 viewer-inside state | Character-Render-Records/how-a-character-fades-the-ten-channels.md:89 |
| +0x4BC | f32 | body shake amount | Character-Render-Records/the-rig-of-seventeen-controllers.md:135 |
| +0x580 | 0x50 | staged look command record | Character-Render-Records/the-staged-look-command.md:30 |
| +0x5D0 / +0x5DC / +0x5E0 / +0x5EC | vec / f32 / byte / f32 | ambient blend colour / ambient amount / ambient mode / light scale | Character-Render-Records/how-a-status-shows-on-a-character.md:302, :345-351, :152-153 |
| +0x640 / +0x644 / +0x648 | f32 | lip / nod / head-shake timers (`frames / [01DFE0BC]`) | Character-Render-Records/the-rig-of-seventeen-controllers.md:110-111 |
| +0x6E0 | | handbook monster viewer flag; cancels cull | Character-Render-Records/how-a-character-fades-the-ten-channels.md:318-320 |
| +0x114 / +0x118 / +0x288 | handle | shadow (pool 02B40528, 160 x 0xE0) / 0x70 table 02B3F570 / render-object handle (02EBD480) | Character-Render-Records/how-a-character-fades-the-ten-channels.md:353-357, :367-374, :189, :401-404 |

Model instance writes: +4 sort key, +0x50 matrix, +0x90, +0xA0, +0xB0, +0x1E4/+0x1E8, +8 bit 1, +0xBA mode (Character-Render-Records/how-a-character-fades-the-ten-channels.md:179-187, :389-390; Character-Render-Records/how-a-status-shows-on-a-character.md:100).

Render-record system tail (base `[022C6F28]`): +0x48800 active-list head (Character-Render-Records/the-rig-of-seventeen-controllers.md:118); +0x48818 flags bit 0 culling, bit 2, bit 4 camera-inside (Character-Render-Records/how-a-character-fades-the-ten-channels.md:223, :389); +0x4881C clip distance, +0x48820 near, +0x48824 fade range, +0x4882C reference record (Character-Render-Records/how-a-character-fades-the-ten-channels.md:223-225). Defaults at 021641F4 / 021641F8 (Character-Render-Records/how-a-character-fades-the-ten-channels.md:294-295).

Status records: 32 x 0x150 at 02B59D80 (Character-Render-Records/how-a-status-shows-on-a-character.md:56); +4 render index, +8 last status word, +0x140 set bits, +0x144 cleared bits, +0xC0 + 4*bit flag dwords, block +0x20 (mask +0, shown +4, wanted +5, +6 frame counter, +7 changing bit 0 / count upper bits, +8/+0xC light handles, +0x18 step, +0x20 phase, +0x24 envelope, +0x28 render record, +0x38 state, +0x39 remembered count, +0x3A hold, +0x40 offset), block +0x70 (+0x10 mask, +0x14 variant, +0x19/+0x31/+0x33) (Character-Render-Records/how-a-status-shows-on-a-character.md:57-61, :78-98, :207, :223-224, :237-244, :591).

Light request (0x50 B; pool 128 x 0x70 at `[02B3F528]`, request at entry +0x20): +0 type, +1 priority, +2 subtype, +3/+4 scope, +5 and +7 flags, +8 target id, +0x10 colour, +0x30 vector (Character-Render-Records/how-a-status-shows-on-a-character.md:211-220). Gather output 0xE0 B: +0x00..+0x50 directions SoA, +0x60+0x10i colours, +0xC0 ambient, +0xD0 last index (Character-Render-Records/how-a-status-shows-on-a-character.md:310-324).

Trail descriptor = FCP section 4: count u32 (cap 4) then 0x50-byte descriptors from +0x10 (Character-Render-Records/the-bone-trails.md:49-60): +0 u8 own-image, +2 u16 bone, +4 u16 owner index (runtime), +8 f32, +0xC f32, +0x10 4 x vec4. Pool entry 0x3C0 (Character-Render-Records/the-bone-trails.md:98-113): +0 handle `serial<<8|slot`, +4 on, +5 flags (bit 0 no update, bit 1 no draw), +6 samples 1..16, +7 alternator, +8 owner opacity, +0xC 20.0, +0x10 fade, +0x14, +0x18/+0x20 prev/next, +0x30 tip x16, +0x130 base x16, +0x230 direction x16 (+0x40), +0x330/+0x334 angle, +0x370 descriptor copy. Draw template 0x4A0 B at 02CA8A90 (Character-Render-Records/the-bone-trails.md:157, :187-197); GIF tag at +0x20: PRIM 0x05C, NREG 6, REGS ST, RGBAQ, XYZF2 x2 (Character-Render-Records/the-bone-trails.md:347-360).

Rig: 17 encoded-pointer dwords at resource entry +0x94 (count +0x90), controller n at +4n; FCP section 2; slots 17/18 at +0x44/+0x48 empty (Character-Render-Records/the-rig-of-seventeen-controllers.md:56-68; Character-Render-Records/the-staged-look-command.md:164-165). Rig fields +0x58, +0x5C (0x0101), +0x5E, +0x5F, +0x60, +0x62 deny, +0x63 flag, +0x68/+0x6C record indices, +0x70/+0x74, +0x78/+0x7C (Character-Render-Records/the-staged-look-command.md:157-162, :177; Character-Render-Records/the-rig-of-seventeen-controllers.md:229, :236).

Look command record (0x50 B): +0 request word (bits per Character-Render-Records/the-staged-look-command.md:63-83), +4..+0xC floats, +0x10..+0x1C bits 7/8 floats, +0x20 / +0x30 dword triples, +0x40..+0x48 eye floats (Character-Render-Records/the-staged-look-command.md:63-88). Look controller (rig slot +8) fields +0x10/+0x14, +0x18 duration, +0x1C bits 0/1/2/5, +0x1D, +0x1E, +0x28 eye object, +0x3C, +0x50..+0x5C, +0x60..+0x6C, +0x70, +0x74, +0x78/+0x7C, +0x88, +0x8C (Character-Render-Records/the-staged-look-command.md:66-99; Character-Render-Records/the-rig-of-seventeen-controllers.md:219).

#### RG — State (globals and objects, with lifetime)

| state | lifetime / init | cite |
|---|---|---|
| fade channels | ResetDefaults sets all ten to 1.0; record zero-filled at creation | Character-Render-Records/how-a-character-fades-the-ten-channels.md:69, :265 |
| `01F82E38` | read via 001EDE70; meaning not stated on these pages (see RG.CS-8) | Character-Render-Records/how-a-character-fades-the-ten-channels.md:66, :436 |
| `01DFE0B4` / `01DFE0B8` / `01DFE0BC` | frame-rate multiplier / min-duration scale / time base, "1.0 at the authored rate" | Character-Render-Records/how-a-character-fades-the-ten-channels.md:64; Character-Render-Records/the-staged-look-command.md:102; Character-Render-Records/the-bone-trails.md:150 |
| tail +0x4881C / +0x48824 | "The system starts at 34.0 and 4.0" | Character-Render-Records/how-a-character-fades-the-ten-channels.md:298 |
| tail +0x48818 | set and cleared by 002E8CC0/002EBBB0/002EBBF0 and the initialiser; initial value not stated on these pages (other page: `+0x48818 |= 5`, the-character-render-record-array.md:951) | Character-Render-Records/how-a-character-fades-the-ten-channels.md:231-232 |
| `0215FD56` cull veto byte | one bit per requester; flag bit 0 = byte == 0; initial not stated | Character-Render-Records/how-a-character-fades-the-ten-channels.md:276-279 |
| `02B59D70` control-deny latch | writer 003E7CC0 via 002EA8E0 / byte 0215FD44 | Character-Render-Records/how-a-status-shows-on-a-character.md:87-90 |
| `02B59D68` display-deny latch | written only by the display-deny latch | Character-Render-Records/the-rig-of-seventeen-controllers.md:239-242 |
| `02B59D60` sway override | never written on PC, always 0 | Character-Render-Records/the-rig-of-seventeen-controllers.md:229 |
| `02B3F518` light scale; `02B3F502` enable; `02B3F501` class filter; `02B3F508` light list | gather writes 02B3F518; filler of 02B3F508 not read | Character-Render-Records/how-a-status-shows-on-a-character.md:312-313, :326-336 |
| pulse table `01F20AA0`, count `01F20538` = 60 | 120 entries under FrameLimit=60 | Character-Render-Records/how-a-status-shows-on-a-character.md:226, :455-460 |
| curve tables `01F21F40`, `01F22030`; bob tables `01F223B0`, `01F22590`, `01F22670`; flinch `01F22130`, `01F22170` | filled at start-up; values not read | Character-Render-Records/how-a-status-shows-on-a-character.md:145-147; Character-Render-Records/the-rig-of-seventeen-controllers.md:248-252, :254-255 |
| status records 02B59D80 | `003E7500` slot init: `word +0 = 1`, `+4 = edx`, `+8 = 0`, zeroes 0x80 at +0xC0, inits two blocks | Character-Render-Records/how-a-status-shows-on-a-character.md:591 |
| trail pool 02CA8420 (16 x 0x3C0), header 02CA8400..02CA8410 | 0051C270 allocates and zeroes; entries free themselves | Character-Render-Records/the-bone-trails.md:91-94, :148-150 |
| trail image 01F2A220 (64x64 8-bit + 256 palette) | registered by init | Character-Render-Records/the-bone-trails.md:93-94 |
| arccos table 00D12590 (16,384) | static | Character-Render-Records/the-bone-trails.md:138-140 |
| rig | slot initialiser at load; rebind resets; slot 4 never initialised | Character-Render-Records/the-rig-of-seventeen-controllers.md:64-67; Character-Render-Records/the-staged-look-command.md:134-162 |
| look command record | zeroed after each apply | Character-Render-Records/the-staged-look-command.md:57 |
| record `+0x5EC` | "1.0 (a record initialiser stores it)" | Character-Render-Records/how-a-status-shows-on-a-character.md:344 |

#### RG — Order (what runs when, and what triggers it)

- Once per simulation tick: World_UpdateSimulationTick -> status push 003E7650 -> per changed bit arms -> both block updates (Character-Render-Records/how-a-status-shows-on-a-character.md:414, :59).
- Dirty-state pass 00427DE0: applies `+0x290`/`+0x294` bits; rig wrappers (Character-Render-Records/the-rig-of-seventeen-controllers.md:99-115); trail fan-out on bit 24 (Character-Render-Records/the-bone-trails.md:75); look apply 00429920 (Character-Render-Records/the-staged-look-command.md:48); verbs take effect at next pass (Character-Render-Records/the-rig-of-seventeen-controllers.md:261).
- System phase 00428F80 walks active list -> 0042EE90 countdown (Character-Render-Records/the-rig-of-seventeen-controllers.md:117-129).
- Distance-fade system phase -> 0042D7A0 -> 0042E850, 00421030, 003B33A0 (Character-Render-Records/how-a-character-fades-the-ten-channels.md:233-244).
- Child/root animation-presentation phase -> 003E4370 stepper (Character-Render-Records/how-a-character-fades-the-ten-channels.md:72); root frame 0042D050 / child frame 0042CBF0 (Character-Render-Records/how-a-character-fades-the-ten-channels.md:164, :348).
- Render root presentation update -> 0051C3C0 trail update once a frame (Character-Render-Records/the-bone-trails.md:126).
- Phase-2 model pass 0041E4D0 tail-jumps 0051BC70: effect layer 3, then trails (Character-Render-Records/the-bone-trails.md:154-157).
- Rig frame 003E00C0: sway; skip rest if flag; look fed; matrices reset; solve 10, 8, 1, 2, 9, 11, 13, 15, 14, 5 (x2), 16, 6, 7, 12, 3, 16; apply 11, 10, 2, 9, 13, 15, 8, 1, 14, 5, 12, 7, 3, 6 (Character-Render-Records/the-rig-of-seventeen-controllers.md:228-235).
- Look update: wanted vs shown -> step -> install only after step reports left (Character-Render-Records/how-a-status-shows-on-a-character.md:83-96).
- Relative order of tick, dirty pass, phases and rig frame within one frame: not stated.

#### RG — Dependencies

Script VM verbs (Character-Render-Records/how-a-character-fades-the-ten-channels.md:525-527; Character-Render-Records/the-rig-of-seventeen-controllers.md:308-309; Character-Render-Records/the-staged-look-command.md:273-274); core scheduling getter 001EDE70 (Character-Render-Records/how-a-character-fades-the-ten-channels.md:529-530; Character-Render-Records/the-staged-look-command.md:276-278); resource table 002ED570 / 004780B0 (Character-Render-Records/how-a-character-fades-the-ten-channels.md:535-537; Character-Render-Records/the-staged-look-command.md:280-282; Character-Render-Records/the-bone-trails.md:428-429); time-stop registry set 5 (ch 2) and set 3 (trail `+5`) (Character-Render-Records/how-a-character-fades-the-ten-channels.md:86; Character-Render-Records/the-bone-trails.md:102, :437-438); status pages / battle stats `+0xBC + 4*status` (Character-Render-Records/how-a-status-shows-on-a-character.md:167-170, :417-418); lighting layer how-a-character-is-lit (Character-Render-Records/how-a-status-shows-on-a-character.md:355-356); shadow pool / ramp-channels contract (Character-Render-Records/how-a-character-fades-the-ten-channels.md:353-357; Character-Render-Records/how-a-status-shows-on-a-character.md:277-279); render-object handle table 02EBD480 / battle runtime ladder (Character-Render-Records/how-a-character-fades-the-ten-channels.md:401-404); effect layer 3 / VFX display layers (Character-Render-Records/the-bone-trails.md:154-156; Character-Render-Records/how-a-character-fades-the-ten-channels.md:245-247); VIF1/VU1 layer and registrar 003A35E0 (Character-Render-Records/the-bone-trails.md:165-166, :176-178); camera matrices 02AEDDB0 / 02AEDDF0 / 02AEDEF0 (Character-Render-Records/how-a-character-fades-the-ten-channels.md:203-214, :332-344); steering record (Character-Render-Records/the-staged-look-command.md:108-124, :270-271); world tick (Character-Render-Records/the-rig-of-seventeen-controllers.md:337); FCP sections 2 and 4 (Character-Render-Records/the-rig-of-seventeen-controllers.md:61-63; Character-Render-Records/the-bone-trails.md:36); authored commands 0x11, 0x13, 0x23, 0x24 (Character-Render-Records/the-bone-trails.md:74; Character-Render-Records/the-rig-of-seventeen-controllers.md:153-163; Character-Render-Records/how-a-character-fades-the-ten-channels.md:85); HP write events 0x2005/0x2006 (Character-Render-Records/the-rig-of-seventeen-controllers.md:141-146); pose sequencer event 0 for Stop (Character-Render-Records/how-a-status-shows-on-a-character.md:249-251); position-to-scalar node 002F1F40 (Character-Render-Records/how-a-character-fades-the-ten-channels.md:407-409).

### 1.5 [CL] Ordered render command list and graphics-thread handshake

Short names in this part: **C** = `CONTRACT-render-command-list-and-graphics-handshake.md`; **L** = `Render-Command-List/the-ordered-render-command-list.md`; **H** = `Graphics-Thread-Handshake/the-shared-command-state-word.md`.


#### CL — Entry points

| entry (size) | callers as stated | what it does | cite |
|---|---|---|---|
| `0018B480` (85 B) | `00186CD0` only (device init) | creates the ordered list once: malloc 0x30, then ctor, stores `[01F7F5E0]` | CONTRACT-render-command-list-and-graphics-handshake.md:60, CONTRACT-render-command-list-and-graphics-handshake.md:272. Render-Command-List/the-ordered-render-command-list.md:1027 "**1** — `00186CD0`" |
| `0018AD00` (105 B) | `0018B480` | ordered-list ctor: classMask = -1, split = 0, reverseMark = -1, reserve of 0x1388 (5,000) through `0018B320` at `0018AD48` | CONTRACT-render-command-list-and-graphics-handshake.md:60, CONTRACT-render-command-list-and-graphics-handshake.md:136-137, Render-Command-List/the-ordered-render-command-list.md:1905-1908 |
| `0018B4E0` (33 B) | 56 functions, 78 sites | getter for `[01F7F5E0]`. The assert folds to `ret 0` | CONTRACT-render-command-list-and-graphics-handshake.md:60, CONTRACT-render-command-list-and-graphics-handshake.md:194-198, Render-Command-List/the-ordered-render-command-list.md:1029 |
| `0018C9E0` (95 B) | `00186CD0` only | creates the owning vector: 0x20 bytes, begin/end/cap = 0, no reserve | CONTRACT-render-command-list-and-graphics-handshake.md:60, CONTRACT-render-command-list-and-graphics-handshake.md:141-143, Render-Command-List/the-ordered-render-command-list.md:1028 |
| `0018CA40` (8 B) | 46 functions, 67 sites | getter for `[01F7F5E8]` | Render-Command-List/the-ordered-render-command-list.md:1030, Render-Command-List/the-ordered-render-command-list.md:980 |
| enqueue functions: 36, contiguous `0018B540`–`0018CCF0`. Worked example `0018C610` (148 B) | pass wrappers of 30–70 B; owner passed in `rcx` from `0018CA40` at all 20 sites traced | malloc a node, run the class ctor (which calls the base `00212CC0`), push_back onto the owner inline, then tail-jump `0018AFF0` onto the ordered list | Render-Command-List/the-ordered-render-command-list.md:975, Render-Command-List/the-ordered-render-command-list.md:617-623, CONTRACT-render-command-list-and-graphics-handshake.md:353-359 |
| four manager-only appenders: `001E5270`, `001F89B0`, `001F48B0`, `001E8580` | slot 1 of MapRenderObject and of CharacterRenderObject; GeometryInstance registrar | append to the ordered list only (embedded or pool objects) | Render-Command-List/the-ordered-render-command-list.md:650-660, Render-Command-List/the-ordered-render-command-list.md:701-705 |
| `0018AFF0` (58 B) | 40 bodies (not address-taken) | push_back onto the ordered list | Render-Command-List/the-ordered-render-command-list.md:323, Render-Command-List/the-ordered-render-command-list.md:645-647 |
| `00212CC0` (26 B) | 42 sites | base ctor: `[+8]=0`, `[+0]`=vtable `009010B8`, `[+0x10]=1` | Render-Command-List/the-ordered-render-command-list.md:110-114, Render-Command-List/the-ordered-render-command-list.md:852-854, CONTRACT-render-command-list-and-graphics-handshake.md:356 |
| `0018B100` (173 B) | render pass `00187950` at `00187D05` (dl=1) and at `00188128` (dl=0) | forward masked walk, with the I-7 early exit | CONTRACT-render-command-list-and-graphics-handshake.md:60-62, CONTRACT-render-command-list-and-graphics-handshake.md:368-376 |
| `0018B1B0` (361 B) | 5 functions / 6 sites: `001F06D0`, `001F3510`, `001F3570`(×2), `001F3650`, `001F36B0` | class-filtered walk, forward or reverse. Calls slot 2 twice per entry | CONTRACT-render-command-list-and-graphics-handshake.md:255-256, Render-Command-List/the-ordered-render-command-list.md:602, CONTRACT-render-command-list-and-graphics-handshake.md:155-157 |
| `0018B510` (35 B) | wrapper `0018CB10` only | sets the split `+0x24` (0 when armed, else count) and `+0x28` | CONTRACT-render-command-list-and-graphics-handshake.md:188-190, CONTRACT-render-command-list-and-graphics-handshake.md:274 |
| `0018B030` (15 B) | wrapper `001829F0` only | `+0x2C` = count | CONTRACT-render-command-list-and-graphics-handshake.md:190-191, CONTRACT-render-command-list-and-graphics-handshake.md:275 |
| `0018B070` | developer console | toggles bit 1 of classMask | CONTRACT-render-command-list-and-graphics-handshake.md:79, Render-Command-List/the-ordered-render-command-list.md:679 |
| `0018B040` (36 B) | `0017CD53`, `00188204`, `001E05A9` | clears the ordered list: `0018B3F0(list,0)`, split = 0, mark = -1 | CONTRACT-render-command-list-and-graphics-handshake.md:120-122, Render-Command-List/the-ordered-render-command-list.md:601 |
| `0018B810` (159 B) | `0017CD60`, `00188211` | destroys the owner: slot 0 with `edx=1`, then resize to 0 | CONTRACT-render-command-list-and-graphics-handshake.md:119-120, Render-Command-List/the-ordered-render-command-list.md:628-632 |
| `0018C8F0` (233 B) | scene teardown `001E0590` at `001E05B6` | flush: execute entries whose `+0x10==0`, destroy all, empty | CONTRACT-render-command-list-and-graphics-handshake.md:123-126 |
| `0018B3F0` (138 B) | `0018B040`, `001A8BA0` | 8-byte-element vector resize | Render-Command-List/the-ordered-render-command-list.md:1528-1538 |
| `001AB570` (318 B) | every push_back slow path | grow and insert | Render-Command-List/the-ordered-render-command-list.md:324 |
| `0036F2C0` `GraphicsSync_ClearSharedCommandStateBits` (43 B) | `0022B2D0` (MainLoop_Draw), `0022B7A4`, `MainLoop_UpdateAndRenderFrame`, six scheduler bodies | settle-spin, then `and [02EBA3F8], 0xFFFFFEF3` | Graphics-Thread-Handshake/the-shared-command-state-word.md:62-77, CONTRACT-render-command-list-and-graphics-handshake.md:571-573, Graphics-Thread-Handshake/the-shared-command-state-word.md:123-126 |
| `0036F360` (150 B) `GraphicsCommand_PublishCompletedBatchState100` | ← `003A1DB0` ← `0036D400` ← `0022B000` ← `0022A580` … ← `0017CCD0` | address, count, three loads, then `0x100` into `02EBA3F8` | Graphics-Thread-Handshake/the-shared-command-state-word.md:320, Graphics-Thread-Handshake/the-shared-command-state-word.md:260-261 |
| `003A2D80` (171 B) | root `0022BEB0` VFXSystem_RenderLayerPass | memcpy to `[02F8F2E0]`, spin on `02EAF6D8`, `xor 0x400`, then the same publish | Graphics-Thread-Handshake/the-shared-command-state-word.md:321, Graphics-Thread-Handshake/the-shared-command-state-word.md:261-263 |
| `003A2E30` (314 B) | `0045BAE0` ← guard `0045BAD0` ← `002F4020` ← `00441970` | the same, plus two hand-built 16-byte records, then count+2 | Graphics-Thread-Handshake/the-shared-command-state-word.md:322, Graphics-Thread-Handshake/the-shared-command-state-word.md:267-279 |
| reset burst `GraphicsSync_WaitBackendState100ClearAndResetSharedState` (interior `0036F2F0`–`0036F352`) | not stated | nine stores ending in 0 | Graphics-Thread-Handshake/the-shared-command-state-word.md:242-246, Graphics-Thread-Handshake/the-shared-command-state-word.md:382-386 |
| `EffectCapture_ProcessCaptureDraw` `003749F0` / `…Secondary…` `00376050` | not stated | `OR 0x10000` … `AND 0xFFFEFEFF` | Graphics-Thread-Handshake/the-shared-command-state-word.md:88, Graphics-Thread-Handshake/the-shared-command-state-word.md:199-200 |

#### CL — Inputs and outputs (record layouts)

`OrderedCommandList` `[01F7F5E0]`, 0x30 bytes (CONTRACT-render-command-list-and-graphics-handshake.md:73-84):

| off | size | meaning | cite |
|---|---|---|---|
| +0x00 / +0x08 / +0x10 | 8 each | pBegin / pEnd / pCapacityEnd | CONTRACT-render-command-list-and-graphics-handshake.md:74-76 |
| +0x18 | 8 | allocator: vtable `00902720` stored by `001EDF00` | CONTRACT-render-command-list-and-graphics-handshake.md:77, CONTRACT-render-command-list-and-graphics-handshake.md:108-112 |
| +0x20 | 4 | classMask, -1 at ctor; bit 1 toggled by `0018B070` | CONTRACT-render-command-list-and-graphics-handshake.md:78 |
| +0x24 | 4 | forwardSplit, 0 at ctor | CONTRACT-render-command-list-and-graphics-handshake.md:79 |
| +0x28 | 1 | splitArmed: `0018B515` writes `(arg != 0)` | CONTRACT-render-command-list-and-graphics-handshake.md:80 |
| +0x29 | 1 | chrOpaqueActive (pass flag, read by `001F5D70`) | CONTRACT-render-command-list-and-graphics-handshake.md:81, CONTRACT-render-command-list-and-graphics-handshake.md:437-447 |
| +0x2A | 1 | afterwaterActive | CONTRACT-render-command-list-and-graphics-handshake.md:82, CONTRACT-render-command-list-and-graphics-handshake.md:441-442 |
| +0x2B | 1 | dead pad | CONTRACT-render-command-list-and-graphics-handshake.md:83, CONTRACT-render-command-list-and-graphics-handshake.md:448-450 |
| +0x2C | 4 (s32) | reverseMark: -1 = whole list | CONTRACT-render-command-list-and-graphics-handshake.md:84, CONTRACT-render-command-list-and-graphics-handshake.md:188-192 |

`RenderCommandOwnerList` `[01F7F5E8]`, 0x20 bytes: begin/end/cap at +0/+8/+0x10, allocator at +0x18 (CONTRACT-render-command-list-and-graphics-handshake.md:86-90; Render-Command-List/the-ordered-render-command-list.md:96-101).

`OrderedObject`: base 0x18 bytes. `+0x00` vftable (slot 0 dtor, slot 1 execute(this, device), slot 2 order key / class mask). `+0x08` executeTarget, nullable. `+0x10` u8 flushSelector, 1 by default. `+0x11..+0x17` tail padding (CONTRACT-render-command-list-and-graphics-handshake.md:92-99, CONTRACT-render-command-list-and-graphics-handshake.md:65, Render-Command-List/the-ordered-render-command-list.md:850-862). Subclass fields from +0x18: PostProcessObj mode +0x18 (size 0x20). SetDofObj float +0x1C (size 0x28). ApplyJson int +0x18. GiReset* key at +0x18. GeometryInstanceOrderedObject key at +0x20 (Render-Command-List/the-ordered-render-command-list.md:127-128, Render-Command-List/the-ordered-render-command-list.md:719-720, Render-Command-List/the-ordered-render-command-list.md:307-309). Allocation sizes: 0x18 ×11, 0x20 ×7, 0x28 ×1 over 19 builders (Render-Command-List/the-ordered-render-command-list.md:892).

Order-key values (slot 2): 1 ×11, 0x10 ×18, 0x100 ×4, 0x80 ×1, per-instance ×2 inside the 36-class block (Render-Command-List/the-ordered-render-command-list.md:998-1004). Outside the block: 0x20 ×3, 0x2, 0x4, and `this[+0x20]` (Render-Command-List/the-ordered-render-command-list.md:301-309). The key is ANDed, never sorted (CONTRACT-render-command-list-and-graphics-handshake.md:145-148).

Vtable block `00902F90`–`009033F0`, 36 vtables at stride 0x20. Each vtable's own Complete Object Locator (COL) sits 8 bytes before it (Render-Command-List/the-ordered-render-command-list.md:388, Render-Command-List/the-ordered-render-command-list.md:983-990). Class list: Render-Command-List/the-ordered-render-command-list.md:416-453.

JSON value: 16 bytes, type tag at +0, payload at +8, type 6 = absent. Banks `01F813A8`/`01F813D8` are double-buffered by parity `01F813F8` (Render-Command-List/the-ordered-render-command-list.md:742-745). Files: `JsonData/init.json`, `JsonData/CutScenes/<scene>.json` and its `_2ndScreen` twin, `JsonData/0.json` (Render-Command-List/the-ordered-render-command-list.md:730-741). 103 keys, with a four-step fallback (Render-Command-List/the-ordered-render-command-list.md:746-751).

Render-parameter record `00193D50()`: 0x4A8 bytes, cached at `01F7F5F0` (= `01F81300`). Switches: AO +0x198, gaussian +0x19A/+0x180/+0x3E8, Display-AO-Only +0x199, contextIndex +0x49C. DOF group +0x110..+0x120. Key-named fields Render-Command-List/the-ordered-render-command-list.md:828-838. +0xEE is always 0 (Render-Command-List/the-ordered-render-command-list.md:784-785, Render-Command-List/the-ordered-render-command-list.md:801-815, Render-Command-List/the-ordered-render-command-list.md:1242).

Handshake word `02EBA3F8` (dword). Masks: publish `=0x100`, consume `&=0xFFFFFEF3`, backend `&=0xFFFFFFCF`, capture `|=0x10000` and `&=0xFFFEFEFF` (Graphics-Thread-Handshake/the-shared-command-state-word.md:174-184). Publishers store `buffer & 0x3FF0`, then the count, then 0x100, all into the one cell (Graphics-Thread-Handshake/the-shared-command-state-word.md:320). 16-byte DMA-tag records; terminator `{0x10000000,0}`; cap 0x200 records (Graphics-Thread-Handshake/the-shared-command-state-word.md:320, Graphics-Thread-Handshake/the-shared-command-state-word.md:322). Staging buffers at `[02F8F2E0]`, two of them 0x400 apart (Graphics-Thread-Handshake/the-shared-command-state-word.md:321). Reset burst values: `022D9B50` low dword, `0x7FFF0`, 0, address ×2, `(w&~4)|8`, `w&~0x30`, `0x14D`, 0 (Graphics-Thread-Handshake/the-shared-command-state-word.md:243-245).

#### CL — State (globals and objects, with lifetime)

| state | lifetime / init | cite |
|---|---|---|
| `[01F7F5E0]`, `[01F7F5E8]` | created once per process at device init; never freed | CONTRACT-render-command-list-and-graphics-handshake.md:272, CONTRACT-render-command-list-and-graphics-handshake.md:219 |
| per-frame command objects | one malloc per enqueue; freed once per frame by slot 0 with `edx=1` | CONTRACT-render-command-list-and-graphics-handshake.md:218-219 |
| `byte[01DF08FC]` | written only by `00187950`: zeroed under +0x199, restored at `00188144`; initial value not stated | CONTRACT-render-command-list-and-graphics-handshake.md:227, CONTRACT-render-command-list-and-graphics-handshake.md:181-182 |
| `byte[01F7F594]` | writers `00187950` and `001F28B0` (AO ran → 1); one reader `0018B100` | CONTRACT-render-command-list-and-graphics-handshake.md:228, CONTRACT-render-command-list-and-graphics-handshake.md:177-179 |
| `byte[01FD4A88]` | gates the frame-tick teardown; writer and initial value not stated | CONTRACT-render-command-list-and-graphics-handshake.md:216, CONTRACT-render-command-list-and-graphics-handshake.md:308 |
| `01DFE0C4` | master render enable byte; writer and initial value not stated | Render-Command-List/the-ordered-render-command-list.md:386 |
| `01F82EC0` | screen index, maintained by the PostProcessObj ctor (0 on mode 0, else +1); initial value not stated | Render-Command-List/the-ordered-render-command-list.md:265-271 |
| `02EBA3F8` | written by 8 functions, all on the main thread; reset burst ends with 0; value at image load not stated | Graphics-Thread-Handshake/the-shared-command-state-word.md:146-147, Graphics-Thread-Handshake/the-shared-command-state-word.md:86 |
| `02EAF6D8` | never written; zero for the life of the process (past `.data` raw size) | Graphics-Thread-Handshake/the-shared-command-state-word.md:301-306 |
| `01F81280` / `01F81281` | ApplyJson gate, set by `001CC600` | Render-Command-List/the-ordered-render-command-list.md:765-768 |

#### CL — Order (what runs when, and what triggers it)

1. Frame open: `001EC490` enqueues ApplyJson twice, with arg 0 (from `0022A5C1`) and arg 1 (from `0022B120` in MainLoop_Draw) (Render-Command-List/the-ordered-render-command-list.md:723-725). MainLoop_Draw `0022B0B0` runs the pass wrappers under the pass gate `(022C7F90[drawMode] >> bit) & 1` (Render-Command-List/the-ordered-render-command-list.md:509-517).
2. Render pass `00187950` ("render ordered objects"): part-1 walk at `00187D05`; if +0x199 is set, it zeroes `01DF08FC`/`01F7F594`; part-0 walk at `00188128`; restore at `00188144`; clear `00188204`, then destroy `00188211` (CONTRACT-render-command-list-and-graphics-handshake.md:238-245, CONTRACT-render-command-list-and-graphics-handshake.md:402-407).
3. Class-filtered walks run from the five `001F0xxx`/`001F3xxx` drivers (CONTRACT-render-command-list-and-graphics-handshake.md:255-256). Their place in the frame is not stated.
4. Frame tick `0017CCD0`: gated on `01FD4A88`, clear `0017CD53` then destroy `0017CD60`, as "the fallback when the render pass did not run" (CONTRACT-render-command-list-and-graphics-handshake.md:233-236, CONTRACT-render-command-list-and-graphics-handshake.md:307-308).
5. Scene teardown `001E0590` (called by frame reset `0017D6E0`): clear `001E05A9`, then flush `001E05B6` (CONTRACT-render-command-list-and-graphics-handshake.md:247-248, CONTRACT-render-command-list-and-graphics-handshake.md:569).
6. Handshake: inline spin at `0022B2C0`, then call `0036F2C0` at `0022B2D0` in MainLoop_Draw; spin at `0022BAD0` in MainLoop_UpdateAndRenderFrame; nine more spins (Graphics-Thread-Handshake/the-shared-command-state-word.md:108-121, CONTRACT-render-command-list-and-graphics-handshake.md:200-203). The publish happens through `0036D400` → `003A1DB0` → `0036F360` (Graphics-Thread-Handshake/the-shared-command-state-word.md:260-261, Graphics-Thread-Handshake/the-shared-command-state-word.md:519-526). Where this sits relative to steps 1-5 is not stated (Graphics-Thread-Handshake/the-shared-command-state-word.md:900-903).

#### CL — Dependencies

Render params `00193D50` (shared with Resource `001A7A50`; Render-Command-List/the-ordered-render-command-list.md:935). Heap allocator `001A1470` (pool `01F7F4C0`) (Render-Command-List/the-ordered-render-command-list.md:655-656). The device argument is `&GameApplication[0xE8]` PRendererBase (stated on `Gi-Render-Commands/gi-render-command-family.md:1099-1107`). Developer console command 42 (CONTRACT-render-command-list-and-graphics-handshake.md:184). Main-loop pages (game-application, CONTRACT-world-simulation-tick) own the timing (CONTRACT-render-command-list-and-graphics-handshake.md:576-577). JSON loaders `001C3760`/`001C5930`/`001C6E20` (Render-Command-List/the-ordered-render-command-list.md:730-741). Phyre submit `005FEFD0`/`00600A60` (Render-Command-List/the-ordered-render-command-list.md:1158-1175). Tk thread API `008636E0` (Graphics-Thread-Handshake/the-shared-command-state-word.md:294-297).

### 1.6 [GP] Gi render commands and the legacy PS2 GS/VIF layer

Short names in this part: **GI** = `Gi-Render-Commands/gi-render-command-family.md`; **TEX** = `Legacy-PS2-GS/texture-mip-local-memory-budget.md`; **VIF** = `Legacy-PS2-GS/the-vif1-vu1-layer.md`.


#### GP — Entry points

| entry (address, size) | callers as stated | what it does | cite |
|---|---|---|---|
| Gi* arena factories, e.g. `GiColorRect` `00863B40`; table of 18 | game emitters (callers not enumerated) | `rcx=[01F7F4C0]`, `edx=size`, call `001A1470`; store vtable if non-null; store result into per-class global; return `result+0x10` or object | Gi-Render-Commands/gi-render-command-family.md:960-980 |
| `001A1470(arena,size)` 93 B, 52 sites | all factories, `0020E680`, `001F48B0` | ring allocator: request `(size&~0xF)+0x10`; advance if `cursor+request<end`, else restart at `base+request`, return base | Gi-Render-Commands/gi-render-command-family.md:334, Gi-Render-Commands/gi-render-command-family.md:990-996 |
| `0020E680` 50 B | 35 frontier callers | allocate 16-byte node from `[01F7F4C0]`, call `0016D6A0` (no-op) | Gi-Render-Commands/gi-render-command-family.md:1525-1531 |
| `001FB840(node)` 43 B, 16 callers | factories, `001DB840`, `0020E670` thunk | promote `node+8` to `node+0`, tail-jump command vtable slot 0 (prepare) | Gi-Render-Commands/gi-render-command-family.md:492-507, Gi-Render-Commands/gi-render-command-family.md:1572-1576 |
| `0020E630(node,mode)` 63 B, 31 callers | `003A35E0`, `003A3740` path, Gi factories | mode → mask 0→8, 1→0x20, 2→0x40, 3→0x20, else 0; tail `001FB810` | Gi-Render-Commands/gi-render-command-family.md:600-603, Gi-Render-Commands/gi-render-command-family.md:1567-1570, Legacy-PS2-GS/the-vif1-vu1-layer.md:215-223 |
| `001FB810` 18 B | `0020E630` | `rdx=[rcx]`, `rcx=[01F7F4D0]`, `r8d=edx`, `jmp 001A17F0` | Gi-Render-Commands/gi-render-command-family.md:1600-1606 |
| `001F48B0` (GeometryRenderTargetImmediate slot 0) 149 B | `001A17F0` default handler | allocate 0x28 record (vtable `00903920`, +0x18 command, +0x20 mask), push_back to list in `01F7F5E0` | Gi-Render-Commands/gi-render-command-family.md:571-581 |
| `0018AFF0` 58 B, 40 callers | `001F48B0`, render objects | push_back on pointer vector (`[+8]` cursor, `[+0x10]` end, grow `001AB570`) | Gi-Render-Commands/gi-render-command-family.md:578, Gi-Render-Commands/gi-render-command-family.md:1546-1553 |
| `003A3670` | not stated | sole writer of display-list base; allocates 0x190000 + 0xC8028 sort scratch + data arena | Gi-Render-Commands/gi-render-command-family.md:406-407 |
| `003A3A00` | not stated | per-frame reset: zero count, rewind `[02F8F2D0]` to `[02F8F308]` | Gi-Render-Commands/gi-render-command-family.md:409-410 |
| `003A3740` 587 B | "driven from render passes (`VFXSystem_RenderLayerPass`, `FUN_003A2BD0`, `FUN_003A3740`)" | read count, merge sort `003A3A50(0,count-1)`, walk 0x28 records; raw callback or node → `0020E630` | Gi-Render-Commands/gi-render-command-family.md:346-348, Gi-Render-Commands/gi-render-command-family.md:375-376, Gi-Render-Commands/gi-render-command-family.md:385-386, Gi-Render-Commands/gi-render-command-family.md:597-598 |
| `003A34D0` / `003A35E0` | VU1 draw callers (e.g. bone trails, `0044E530`) | build `GiVmax` via `001DB840`; sorted (draw list) vs immediate (`0020E630(node,2)`) submit | Legacy-PS2-GS/the-vif1-vu1-layer.md:240-248 |
| `001DB840` | `003A34D0`, `003A35E0` | allocate 0x640 `GiVmax`, chunk descriptors (scratch `01F82D08`, MPG template `01DFD038`, payloads), `002105C0`, `001FB840(node)` | Legacy-PS2-GS/the-vif1-vu1-layer.md:110-111, Legacy-PS2-GS/the-vif1-vu1-layer.md:188-209 |
| `001DB7E0` | `00540DB0`, `00540C70` (effect finalisers) | construct `GiVmax` (0x640) with no packets | Legacy-PS2-GS/the-vif1-vu1-layer.md:261-266 |
| `001DB340` | `001DB840`, `00540DB0` | append payload chunk | Legacy-PS2-GS/the-vif1-vu1-layer.md:203, Legacy-PS2-GS/the-vif1-vu1-layer.md:265 |
| `00187950` (render pass list) | application slot 8 render path | calls `0018B100(list, whole, device)` at `00187D05` (whole=1) and `00188128` (whole=0) | Gi-Render-Commands/gi-render-command-family.md:583-586 |
| `0018B100(list,whole,dev)` | `00187950` | per record: mask=slot2; skip if `mask & [list+0x20]`==0; abandon if `byte[01DF08FC]==0 && byte[01F7F594]!=0`; slot1(record, dev) | Gi-Render-Commands/gi-render-command-family.md:588-594 |
| `001F49F0` (record slot 1) | `0018B100` | `005FEA50(dev, 001F4A10, [rec+0x18])` | Gi-Render-Commands/gi-render-command-family.md:1086-1092 |
| `005FEA50(target,fn,arg)` 209 B, 10 callers | `001F49F0` etc. | reserve 0x80 block in ring `[t+0x50..0x58]` cursor `+0x60`; may first call target slot 2; writes `0x2F`, fn, arg; publishes `[t+0x88]..[t+0x90]` | Gi-Render-Commands/gi-render-command-family.md:609-614, Gi-Render-Commands/gi-render-command-family.md:776-785, Gi-Render-Commands/gi-render-command-family.md:1176-1183, Gi-Render-Commands/gi-render-command-family.md:1580-1587 |
| `00600D20` (PRendererBase slot 2) | `005FEA50` flush | write {start,end,event} into queue `02CE4720` slot, signal, reset ring | Gi-Render-Commands/gi-render-command-family.md:1183, Gi-Render-Commands/gi-render-command-family.md:1196-1208, Gi-Render-Commands/gi-render-command-family.md:1255-1259 |
| `00607D20(queue)` | `0079F150` at `0079F54E` | create queue: semaphores, 256 events, CreateThread(`005FE1F0`, queue), 64 KB stack | Gi-Render-Commands/gi-render-command-family.md:1245-1253 |
| `006106A0(queue)` (thread proc via `005FE1F0`) | thread | wait slot event, reset, `0060A410(queue,start,end)`, release completion | Gi-Render-Commands/gi-render-command-family.md:1263-1273 |
| `0060A410(queue,start,end)` | `006106A0` | walk 0x80 blocks; opcode `[block]`; 47-way switch; 0x2F builds 3-qword frame {`02CC0410`, `&[rsp+0x50]`, cmd} and calls `[block+8]` | Gi-Render-Commands/gi-render-command-family.md:1279-1301, Gi-Render-Commands/gi-render-command-family.md:1307-1308 |
| `00607410` (level-1 default) | `0060A410` default arm `0060A9C6` | 40-way dispatch on opcodes 0x07-0x2E | Gi-Render-Commands/gi-render-command-family.md:1382-1395 |
| `001F4A10` (callback) | `0060A410` 0x2F arm only | device = `[ctx]+0x18C0` via `00624660`; `jmp [cmd_vtable+8](cmd, device)` | Gi-Render-Commands/gi-render-command-family.md:512-518, Gi-Render-Commands/gi-render-command-family.md:790-797 |
| Gi slot 1 bodies (table) | `001F4A10` | execute against device `02CC1CD0` | Gi-Render-Commands/gi-render-command-family.md:101-112, Gi-Render-Commands/gi-render-command-family.md:1326-1329 |
| `006CA760` (device slot 0) | 5 Gi* bodies | returns `this+0x10880` staging (0x7FE0 bytes), resets index `+0x18860`, publishes `+0xB8` | Gi-Render-Commands/gi-render-command-family.md:86-88, Gi-Render-Commands/gi-render-command-family.md:657-665, Gi-Render-Commands/gi-render-command-family.md:361-364 |
| `00210570` (GiSetTexture target) | `00863040` | store `{ptr,dword}` at `01F83580 + id*16` if signed `id < 0x4000` | Gi-Render-Commands/gi-render-command-family.md:210-217 |
| `0022C940(packet,size,cb,ctx)` / `0022C970` | `001DB550` per chunk | VIF1 decode (STCYCL, OFFSET, BASE, MPG, DIRECT/HL, UNPACK, MSCAL/F) | Legacy-PS2-GS/the-vif1-vu1-layer.md:51-63 |
| `001DB550` (`GiVmax` slot 0) | `001FB840` | walk chunk list, `0022C940` per chunk with callback `001DB640` | Legacy-PS2-GS/the-vif1-vu1-layer.md:107-110 |
| `001DB640`→`001DB660` | decoder DIRECT and microprogram leaves | copy GIF packet (size `0020F310`) into `+0x228` list, flag into `+0x430` | Legacy-PS2-GS/the-vif1-vu1-layer.md:111, Legacy-PS2-GS/the-vif1-vu1-layer.md:118-122 |
| `001DB3D0` (`GiVmax` slot 1) | `001F4A10` (execute) | state set, `00210320(packet,device,flag)` per copy, state reset | Legacy-PS2-GS/the-vif1-vu1-layer.md:124-127, Legacy-PS2-GS/the-vif1-vu1-layer.md:843 |
| `00210320` | `001DB3D0` | GIF tag replay by mode (PACKED→`0020F3E0`, REGLIST ends, IMAGE skip) | Legacy-PS2-GS/the-vif1-vu1-layer.md:160-176 |
| `0020F3E0` | `00210320` | PACKED: per-descriptor flush + dispatch to 20 handlers | Legacy-PS2-GS/the-vif1-vu1-layer.md:275-291 |
| `0020EC80` / `0020EB60` / `0020ED30` | XYZ2 kick at 682, flush | draw state select, copy vertices/indices, device slot `+0x28` | Legacy-PS2-GS/the-vif1-vu1-layer.md:294, Legacy-PS2-GS/the-vif1-vu1-layer.md:360-372 |
| `008631E0(packet,program,addr)` 84 B, 37 callers | template builders | append `(0x4A000000|addr, program)` to `02EAF930` | Legacy-PS2-GS/the-vif1-vu1-layer.md:393-395, Legacy-PS2-GS/the-vif1-vu1-layer.md:899-906 |
| `002F7380` 723 B | `0026E290` (verified sole caller) | rebuild texture-slot table | Legacy-PS2-GS/texture-mip-local-memory-budget.md:43-61, Legacy-PS2-GS/texture-mip-local-memory-budget.md:112 |
| `00466190` / `003A1E50` / `00466220` / `00467AA0` / `00467AD0` / `00467B00` / `00467B10` | `002F7380` (and not stated) | mip footprint / GS page size / 4-bit PSM test / budget / seed / publish | Legacy-PS2-GS/texture-mip-local-memory-budget.md:100-108 |

#### GP — Inputs and outputs (record layouts)

Display-list record, stride 0x28, base `[02F8F2F8]`, count u16 `[02F8F2C6]`, capacity 40,960 (Gi-Render-Commands/gi-render-command-family.md:341-343, Gi-Render-Commands/gi-render-command-family.md:406-407):

| off | size | meaning | cite |
|---|---|---|---|
| +0x00 | qword | argument passed as rcx to callback | Gi-Render-Commands/gi-render-command-family.md:382 |
| +0x08 | dword | sort key; 24 bits value + display-layer nibble from `byte[02AEE910]` in top byte; "pass nibble ... in bits 28-31" | Gi-Render-Commands/gi-render-command-family.md:383, Gi-Render-Commands/gi-render-command-family.md:352 |
| +0x0C | dword | appender-supplied count | Gi-Render-Commands/gi-render-command-family.md:384 |
| +0x10 | qword | raw function pointer, `call rax` with rcx only | Gi-Render-Commands/gi-render-command-family.md:385, Gi-Render-Commands/gi-render-command-family.md:397-398 |
| +0x18 | qword | 16-byte node (from `0020E680`), used when +0x10 null | Gi-Render-Commands/gi-render-command-family.md:386 |
| +0x20 | byte | flags: bit 1 early branch, bit 2 deferred-path select | Gi-Render-Commands/gi-render-command-family.md:387 |

Node (16 B): `+0` live command, `+8` staging command (Gi-Render-Commands/gi-render-command-family.md:501-502). Ordered record (0x28, vtable `00903920`): `+0x18` command, `+0x20` mask (Gi-Render-Commands/gi-render-command-family.md:573); slot 0 dtor `mov edx,0x28`, slot 1 `001F49F0`, slot 2 `001F49E0` returns `[rec+0x20]` (Gi-Render-Commands/gi-render-command-family.md:541-542, Gi-Render-Commands/gi-render-command-family.md:590).

Render block (0x80, ring of PRendererBase): `+0x00` dword opcode, `+0x08` fn / payload start, `+0x10` arg (Gi-Render-Commands/gi-render-command-family.md:609-613, Gi-Render-Commands/gi-render-command-family.md:1393-1395). Opcode vocabulary: level 1 real arms 0x01-0x06, 0x2F; level 2 0x07-0x2E, 40 arms (Gi-Render-Commands/gi-render-command-family.md:1287-1288, Gi-Render-Commands/gi-render-command-family.md:1393); 19 producers over 19 opcodes (Gi-Render-Commands/gi-render-command-family.md:1414-1437); inert handlers `0060D760` (0x1D 0x1E 0x1F 0x25 0x27 0x28 0x29 0x2B) and `005C5230` (0x2E) (Gi-Render-Commands/gi-render-command-family.md:1443-1446); 0x25 = {flag +0x08, bias +0x0C, slope +0x10} (Gi-Render-Commands/gi-render-command-family.md:1482). Full table in `members/render-block-opcode-isa.tsv` (Gi-Render-Commands/gi-render-command-family.md:1380).

Hand-off queue `02CE4720`: record R(i) = queue+0x30+0x28*i: +0x00 start, +0x08 end, +0x10 per-slot event, +0x20 completion `[target+0x78]`; 256 slots (Gi-Render-Commands/gi-render-command-family.md:1255-1258, Gi-Render-Commands/gi-render-command-family.md:1196).

0x2F callback frame: field 0 context (`02CC0410`), field 8 `&[rsp+0x50]`, field 0x10 Gi command (Gi-Render-Commands/gi-render-command-family.md:1293-1296).

Gi command fields as stated: `GiPolyGT4T` `[this+0xF8]&0x3FFF` resource id → `[this+0xD0]`/`[this+0xD8]` (Gi-Render-Commands/gi-render-command-family.md:146-148); stream `[cmd+0x10]`, `[cmd+0x14]`... (Gi-Render-Commands/gi-render-command-family.md:96); `GiPrim` count `[+0x60]` (Gi-Render-Commands/gi-render-command-family.md:233, Gi-Render-Commands/gi-render-command-family.md:919); `GiSetTexture` u16 id `+0x08`, ptr `+0x10`, dword `+0x0C` (Gi-Render-Commands/gi-render-command-family.md:210-211). Arena sizes: SetTexture 0x18, ColorRect 0x70, Prim 0x68, Sprite 0xE0, PolyGT4T 0x100, ZNormalOnOff 0x10, BeginEff 0x90, SetRtForRtSampling 0x18, ScreenImage 0xC0, GiVmax 0x640; GiBeginScene 8 (Gi-Render-Commands/gi-render-command-family.md:963-971, Gi-Render-Commands/gi-render-command-family.md:505). Reset cmds: 0x20, `+0x08`=0, `+0x10`=1, `+0x18` order key (Gi-Render-Commands/gi-render-command-family.md:195-200).

Device `PrimitiveRendererD3D11` vtable `00D86960` (45 slots), 20 used offsets with bodies (Gi-Render-Commands/gi-render-command-family.md:1343-1350); staging buffer `+0x10880` (0x7FE0 = 682 × 0x30 vertices), index `+0x18860`, current `+0xB8` (Gi-Render-Commands/gi-render-command-family.md:657-663, Gi-Render-Commands/gi-render-command-family.md:86-88).

Texture-id table `01F83580`: 16-byte entries `{pointer, dword}`, key `(TEX0>>37)&0x3FFF`, current slot `01FD3688`, PSM threshold 0x300000 / 0x200000 (Gi-Render-Commands/gi-render-command-family.md:212-224, Legacy-PS2-GS/the-vif1-vu1-layer.md:370-372).

VIF1: word `[31:24] code [23:0] params` (Legacy-PS2-GS/the-vif1-vu1-layer.md:735); MPG = `0x4A000000|addr` + u64 function pointer (Legacy-PS2-GS/the-vif1-vu1-layer.md:736); UNPACK: `vn=(cmd>>2)&3`, `vl=cmd&3`, bit14 unsigned, bit15 add-TOPS, bits16-23 NUM, low 10 bits ADDR, mask bit ignored (Legacy-PS2-GS/the-vif1-vu1-layer.md:827); V4_5 RGBA5551 formula (Legacy-PS2-GS/the-vif1-vu1-layer.md:827); V2-32 / V4_5 stride defects (Legacy-PS2-GS/the-vif1-vu1-layer.md:828-832); only V4_32 used (Legacy-PS2-GS/the-vif1-vu1-layer.md:827, Legacy-PS2-GS/the-vif1-vu1-layer.md:834).

GIF tag: NLOOP 0-14, EOP 15, PRE 46, PRIM 47-57, FLG 58-59, NREG 60-63 (0=16); sizes PACKED `(NREG×NLOOP+1)×16`, REGLIST `round_even(NREG×NLOOP)×8+16`, IMAGE `(NLOOP+1)×16`; flat 16 if `byte[01E027C0]`==0 (Legacy-PS2-GS/the-vif1-vu1-layer.md:131-144, Legacy-PS2-GS/the-vif1-vu1-layer.md:160).

GS vertex 48 B at `01FC3620+n*48`: X bits0-15×0.0625, Y bits32-47×0.0625, Z second qword bits 4-27, clamp `01FD3664`/`01FD3660`; colour floats +0x10-+0x1C; UV +0x20/+0x24; +0x28-+0x2F not written; matrix `01FD3620` row-vector convention, summation order, divide by W (Legacy-PS2-GS/the-vif1-vu1-layer.md:295-317). Indices u16 at `01FCB610` per PRIM table; readiness requirement/carry table (Legacy-PS2-GS/the-vif1-vu1-layer.md:318-358).

`GiVmax` object 0x640: `+8` state flag, `+0x224`/`+0x228` copy count/list, `+0x42C`/`+0x430` flag count/list, `+0x638` byte from `002105C0` (Legacy-PS2-GS/the-vif1-vu1-layer.md:121-125, Legacy-PS2-GS/the-vif1-vu1-layer.md:189). Packet chunks: 1 = `01F82D08` (8 B), 2 = `01DFD038` (0x10, MPG word + program at +8), 3/4 payloads (Legacy-PS2-GS/the-vif1-vu1-layer.md:199-204).

Templates: 77 rows; object header 0x30 (37 MPG rows), 0x10 (19), sub-header `0x10WWWWWW` (Legacy-PS2-GS/the-vif1-vu1-layer.md:430-456); GIF tag stats (Legacy-PS2-GS/the-vif1-vu1-layer.md:554-605).

Texture source record 0x60: +0x00 u8 format, +0x05 u8 mipCount (≤7), +0x06 u16 width, +0x08 u16 height, +0x0C u16 continuation, +0x0E int16 refCount then slot (Legacy-PS2-GS/texture-mip-local-memory-budget.md:119-128, Legacy-PS2-GS/texture-mip-local-memory-budget.md:154-166). Reference descriptor 0x30 (fields not stated) (Legacy-PS2-GS/texture-mip-local-memory-budget.md:130). Derived slot record 0x28: qwords +0x00..+0x18, byte +0x20, +0x21..+0x27 never written (Legacy-PS2-GS/texture-mip-local-memory-budget.md:131-134). Owner +0x218 ptr, +0x228 u32 count (Legacy-PS2-GS/texture-mip-local-memory-budget.md:136-138). PSM dispatch `format-2` (Legacy-PS2-GS/texture-mip-local-memory-budget.md:182-193); class table (Legacy-PS2-GS/texture-mip-local-memory-budget.md:73-78). Budget `(0x1007FF - used) & 0xFFFFF800`, `used = 3*(W*H) + totals` (Legacy-PS2-GS/texture-mip-local-memory-budget.md:80-82, Legacy-PS2-GS/texture-mip-local-memory-budget.md:304).

#### GP — State (globals and objects, with lifetime)

| object | address / size | lifetime / init | cite |
|---|---|---|---|
| command arena | `[01F7F4C0]` | installed by `0017D4C0`; per-frame reset "Not read" | Gi-Render-Commands/gi-render-command-family.md:425-426, Gi-Render-Commands/gi-render-command-family.md:1000 |
| deferred-handler object | `[01F7F4D0]`, 0x10 | installed once by `0017D4C0`; ctor `001A17D0` writes vtable `008F5F28`, `[+8]=self` | Gi-Render-Commands/gi-render-command-family.md:425-431 |
| display list | base `[02F8F2F8]`, count u16 `[02F8F2C6]`, data arena `[02F8F2D0]`/base `[02F8F308]` | allocated by `003A3670`; reset by `003A3A00` per frame | Gi-Render-Commands/gi-render-command-family.md:341-343, Gi-Render-Commands/gi-render-command-family.md:406-410 |
| ordered-record list (EASTL vector) | in global `01F7F5E0` | built once at device init `00186CD0`→`0018B480`, 5000 reserved, `+0x20`=0xFFFFFFFF; `+0x24` watermark by `0018B510` | Gi-Render-Commands/gi-render-command-family.md:579-581, Gi-Render-Commands/gi-render-command-family.md:596 |
| abandon flags | `byte[01DF08FC]`, `byte[01F7F594]` | meaning, writers, init not stated | Gi-Render-Commands/gi-render-command-family.md:592 |
| PRendererBase | `&GameApplication[0xE8]`, app static `01F7E350` | ring `+0x50/+0x58/+0x60`, pending `+0x88/+0x90`, event `+0x78`; init not stated | Gi-Render-Commands/gi-render-command-family.md:1094-1095, Gi-Render-Commands/gi-render-command-family.md:1103, Gi-Render-Commands/gi-render-command-family.md:1119-1121, Gi-Render-Commands/gi-render-command-family.md:1201 |
| block queue | `02CE4720` magic static (getter `005FD0E0`), read cursor `+0x2830`, write cursor `02CE6F54`, sems `+0x2840`/`+0x2850` | created `00607D20` (from `0079F150`), torn down `00610420` | Gi-Render-Commands/gi-render-command-family.md:1215-1223, Gi-Render-Commands/gi-render-command-family.md:1246-1252, Gi-Render-Commands/gi-render-command-family.md:1265 |
| render context | `02CC0410` magic static, ctor `00615840` | getter `005FD050`/`00624670` | Gi-Render-Commands/gi-render-command-family.md:1307-1315 |
| device | `02CC1CD0` = `02CC0410+0x18C0` | ctor `006C8750` (vtables `00D86960` / `00D86AD0`) | Gi-Render-Commands/gi-render-command-family.md:1320-1329 |
| per-class last-created globals (11) | `02EAF900` … `01F83088` | written by factories; "write-only" (but see GP.CV-3) | Gi-Render-Commands/gi-render-command-family.md:960-987 |
| GiBeginScene state | `01F83060` done, `01F83064` armed, `01F83068` mode, `01F83070` node | `001FBD80` | Gi-Render-Commands/gi-render-command-family.md:1537-1543 |
| texture-id table | `01F83580` 0x4000×16 B; image base `01F83530` | writer `00210570`; init "what the image initialises" deferred to other page | Gi-Render-Commands/gi-render-command-family.md:212-220 |
| VU memory | `02064E30`, 0x4000 (1024×16) | init not stated | Legacy-PS2-GS/the-vif1-vu1-layer.md:381 |
| VU registers | `02064B00`-`02064E30`; status `02064DEC` | status set only by `0022CC40`/`0022CC30`; init not stated | Legacy-PS2-GS/the-vif1-vu1-layer.md:382-383 |
| program table | `02068E30`, 0x20000 | MPG writes; never cleared (count reset leaves table) | Legacy-PS2-GS/the-vif1-vu1-layer.md:384, Legacy-PS2-GS/the-vif1-vu1-layer.md:75-77 |
| VIF regs | `02088E30` BASE, `+4` OFFSET, `+8` status, `+0xC` WL, `+0x10` CYCLE, `+0x14` count, list `02088E50` | init not stated; count reset by an 11-byte routine | Legacy-PS2-GS/the-vif1-vu1-layer.md:57-60, Legacy-PS2-GS/the-vif1-vu1-layer.md:385, Legacy-PS2-GS/the-vif1-vu1-layer.md:75 |
| GS replay state | `01FC3620` vertices, `01FCB610` indices, `01F83564`/`01F83568` counts, `01F83561/62/6C/70/74/78`, `01FD3611`, `01FD3620`, `01FD3660/64`, `01F8357F`, `01E027C0`, `01FC35F8` | `01FC35F8` written only at `0021037B`; other inits not stated | Legacy-PS2-GS/the-vif1-vu1-layer.md:294-357, Legacy-PS2-GS/the-vif1-vu1-layer.md:843 |
| MPG template / scratch | `01DFD038` (word never written), `01F82D08` | rewritten each `001DB840` call | Legacy-PS2-GS/the-vif1-vu1-layer.md:202-209 |
| template queue | `02EAF930`, count `02EB37B0` | `008631E0` | Legacy-PS2-GS/the-vif1-vu1-layer.md:393, Legacy-PS2-GS/the-vif1-vu1-layer.md:903-905 |
| 2D layer | `0215E6D0` bracket flag, ring desc `02EBEFC0`, index `02EBEFF0`, kick cell `02EBA3F8`, batcher `[01F811E8]` | per pages cited in table | Legacy-PS2-GS/the-vif1-vu1-layer.md:695-700 |
| texture model | `022D8EAC`=512, `022D8EB4`=448 (single writer `0036D280`), `02CA5FF0`=0x4000, `02CA5FF4` blocks, `02CA6004` max, `02CA6008` aggregate; frame index (address not stated)=0 | Legacy-PS2-GS/texture-mip-local-memory-budget.md:144-148, Legacy-PS2-GS/texture-mip-local-memory-budget.md:226, Legacy-PS2-GS/texture-mip-local-memory-budget.md:304, Legacy-PS2-GS/texture-mip-local-memory-budget.md:321-323, Legacy-PS2-GS/texture-mip-local-memory-budget.md:239-248 |
| texture slot table | owner `+0x218`/`+0x228` | reallocated on every zone rebuild; 7 bytes/elt uninitialised | Legacy-PS2-GS/texture-mip-local-memory-budget.md:59-61, Legacy-PS2-GS/texture-mip-local-memory-budget.md:174-175 |

#### GP — Order (what runs when, and what triggers it)

1. Emit (game thread): factory → `001A1470` → command into node+8 → `001FB840` prepare (slot 0) runs immediately (Gi-Render-Commands/gi-render-command-family.md:530-531, Gi-Render-Commands/gi-render-command-family.md:504-507). For `GiVmax` the whole VIF program runs inside `001DB840` before the registrar returns (Legacy-PS2-GS/the-vif1-vu1-layer.md:188-194).
2. Submit: either display-list record via `003A34D0` / emitters (sorted later by `003A3740`), or `0020E630(node,2)` immediately (`003A35E0`) (Legacy-PS2-GS/the-vif1-vu1-layer.md:246). `003A3740` files records via `0020E630` (Gi-Render-Commands/gi-render-command-family.md:597-598).
3. `001F48B0` appends 0x28 record to vector `01F7F5E0` (Gi-Render-Commands/gi-render-command-family.md:571-581).
4. Once per frame the render pass list `00187950` runs `0018B100` twice (prefix whole=1, tail whole=0) (Gi-Render-Commands/gi-render-command-family.md:583-597).
5. Record slot 1 → `005FEA50` enqueue 0x2F block into PRendererBase ring → flush slot 2 `00600D20` → queue (Gi-Render-Commands/gi-render-command-family.md:1086-1095, Gi-Render-Commands/gi-render-command-family.md:1176-1208).
6. Render thread `006106A0` → `0060A410` → 0x2F arm → `001F4A10` → Gi execute (slot 1) on device (Gi-Render-Commands/gi-render-command-family.md:1263-1301, Gi-Render-Commands/gi-render-command-family.md:512-518). `GiVmax` slot 1 replays GIF copies (Legacy-PS2-GS/the-vif1-vu1-layer.md:124-127).
7. `003A3A00` resets display list per frame (Gi-Render-Commands/gi-render-command-family.md:409-410); when in frame: not stated.
8. Texture: Weather slot → `00379290` → `0026E8D0` sets dirty → `0026E290` → `002F7380` on field init/rebuild only; not on runtime weather change (Legacy-PS2-GS/texture-mip-local-memory-budget.md:197-207, Legacy-PS2-GS/texture-mip-local-memory-budget.md:228-229).

#### GP — Dependencies

- 00-Engine-Core: application slot 8 / `00187950` (Gi-Render-Commands/gi-render-command-family.md:584-585); `0017D4C0` CoreRuntimeScheduling installer (Gi-Render-Commands/gi-render-command-family.md:425-427); vtable index (Gi-Render-Commands/gi-render-command-family.md:46).
- Effect system: element finalisers `00540DB0`/`00540C70` draw through `GiVmax` (Legacy-PS2-GS/the-vif1-vu1-layer.md:261-268); display list shared with effect elements (Gi-Render-Commands/gi-render-command-family.md:353-355, Legacy-PS2-GS/the-vif1-vu1-layer.md:248-251); type `0x97` raw packets never submitted (Legacy-PS2-GS/the-vif1-vu1-layer.md:834).
- 02-Resource: authored-table contract §7 (image-address base) (Gi-Render-Commands/gi-render-command-family.md:218-220).
- 16-UI: DynGeo family (Gi-Render-Commands/gi-render-command-family.md:267, Legacy-PS2-GS/the-vif1-vu1-layer.md:700-701).
- Movement (trigger owner) and WorldAreaField/Weather (Legacy-PS2-GS/texture-mip-local-memory-budget.md:92-96, Legacy-PS2-GS/texture-mip-local-memory-budget.md:198-210).
- Platform: semaphores/CreateThread (Gi-Render-Commands/gi-render-command-family.md:1247-1252, Gi-Render-Commands/gi-render-command-family.md:1492-1497).
- Bone trails / character records (Legacy-PS2-GS/the-vif1-vu1-layer.md:182-187); graphics-thread handshake page (Legacy-PS2-GS/the-vif1-vu1-layer.md:698).

### 1.7 [EF] Effect containers, element dispatch and the per-frame element update

Short names in this part: **DISP** = `Effect-File-Formats/effect-element-type-dispatch.md`; **FBF** = `Effect-File-Formats/an-effect-element-frame-by-frame.md`; **EFX** = `Effect-File-Formats/efx-and-efb-effect-containers.md`; **ERM** = `Effect-File-Formats/README.md`; **CAT** = `README.md`.


#### EF — Entry points

| entry (size) | callers as stated | what it does | cite |
|---|---|---|---|
| `003A8D80` via thunk `003A72F0` | `0024D370` at `0024D499` | instance-list walk: `[02EBEF88]`→`+8`, per node store `02EBEF80`, call `00441970(node)` | Effect-File-Formats/effect-element-type-dispatch.md:113-118 |
| `00441970` | `003A8D80` | one instance: needs `+0x118`; kind switch on `[[+0x108]+0x44]` (only 6 kinds walk when `[02F97348]+0x36A` bit 0 clear); walks chain `+0x118`/`+0x30` or `+0x128`/`+0x28`, `002F4020(element, instance)` each | Effect-File-Formats/effect-element-type-dispatch.md:123-131, 845-858 |
| `002F4020` (walk, 3rd dispatcher) | `00441970` | type bound `[022BE7D8]`..`0xD1`; stamp check `+0x224`; rate gate def `+0x4D`; `003A3D10(def+0x75)`; switch on type−1 (46 arms, default `0043ED30`); `003A3D10` again | Effect-File-Formats/effect-element-type-dispatch.md:133-145 |
| `0043ED30` (133 B) | `002F4020` default | sub-walk on type−0x42, 0x42..0xAB, 19 slots | Effect-File-Formats/effect-element-type-dispatch.md:199-224, 1226 |
| `002F3910` (update) | `0043EF40` (`0043EFBA`), `00442310` (`00442354`) | 47 types → 38 routines, default `0043EAB0`; type 0 = `002F2530` | Effect-File-Formats/effect-element-type-dispatch.md:80-89, 99 |
| `0043EF40` | `003A8390`, `0043F450` | caller-timed update pump: loop `[obj+0x118]`/`+0x30`, `002F3910(node,obj,xmm2)`; gate on `+0x1B0`; post-loop `+0x139`, `[+0x2C]` vs `[+0x28]` | Effect-File-Formats/effect-element-type-dispatch.md:102, 937-962 |
| `00442310` | `003A93F0` (kinds 0xA1/0x40 only) | self-timed pump, step = `2.0 × [01DFE0BC]` | Effect-File-Formats/effect-element-type-dispatch.md:945-956, 2274 |
| `002F2530` (2,094 B) | every update routine; type 0's update arm | shared base/motion integrator (gates, age, expiry, motion, floor, angle wrap, attachments, completion) | Effect-File-Formats/effect-element-type-dispatch.md:909-936; Effect-File-Formats/an-effect-element-frame-by-frame.md:40-61 |
| per-type tails `00442600` 0x01, `00449560` 0x02, `004428F0` 0x03, `00445B50` 0x04, `0044A180` 0x05, `00447830` 0x06, `00448800` 0x07, `0044B3C0` 0x08, `0044C850` 0x0A | not stated on FBF; DISP shows step arms calling `00449560`, `00445B50`, `00447830`, `00448800`, `0044A180` as "prelude" | sample tracks into element, end in cull fork | Effect-File-Formats/an-effect-element-frame-by-frame.md:69-233; Effect-File-Formats/effect-element-type-dispatch.md:1962, 2166, 2250, 2254, 2258 |
| `005002E0` (389 B) | the nine tails | cull test, 1 keep / 0 cull | Effect-File-Formats/an-effect-element-frame-by-frame.md:119-132 |
| `002F31C0` (233 B) "seventh method" | tails, `002F2530`, `003A8DD0`, `003A92D0`, `00442600` | release: type teardown, unlink, push free list | Effect-File-Formats/an-effect-element-frame-by-frame.md:134-138; Effect-File-Formats/effect-element-type-dispatch.md:161-163 |
| `003A8950(trigger, element)` (394 B) | tails (trigger 2), base (2 for type 0, 3 on end), `002F2D60` | child-spawn slots | Effect-File-Formats/an-effect-element-frame-by-frame.md:140-156; Effect-File-Formats/effect-element-type-dispatch.md:1050-1051 |
| `003A8AE0` | `003A8950`, `003A8DD0`, `0046EFD0`, `00538820` | sub-resource spawner → `00441B30` | Effect-File-Formats/an-effect-element-frame-by-frame.md:153; Effect-File-Formats/effect-element-type-dispatch.md:100-101 |
| `00441B30` (element loop) | `003A8AE0` (`003A8C19`), `0043EF40` (`0043F1DB`) | takes element off owner free list `+0x120`, runs step `002F3BC0` (`00441E71`) | Effect-File-Formats/effect-element-type-dispatch.md:55-58, 98, 100 |
| `002F3BC0` (step = birth) | `00441B30` only | each arm calls `002F2D60`; 47 cases, default `0043EBF0`; +1.0 to `+0x3C`; `+0x224` stamp | Effect-File-Formats/effect-element-type-dispatch.md:53-76 |
| `002F2D60` (1,111 B) | every step arm; sub-step arms (e.g. `0052A130`) | wires element: `+0x18` spawn record, `+0x8` instance, `+0x20` definition; copies type to `+0`; colour `+0x1F0` = `0x80808080` | Effect-File-Formats/effect-element-type-dispatch.md:827-843, 1045-1051 |
| `005004C0` (setup, def `+0x44`) / `00538910` sub | `003A9A70`, `003A99F0`, `003A9BA0` (from `003EDAD0`/`003ED8A0` and `0024D540`/`0024D970`) | setup method at element build | Effect-File-Formats/effect-element-type-dispatch.md:154-159 |
| `003EDAD0(data,size)` EFX loader | six constructors `002FC4A0`, `0026FB90`, `003B38B0`, `003B29B0`, `003B0660`, `003B2220` | magic check, chunk walk | Effect-File-Formats/efx-and-efb-effect-containers.md:385-407, 156-163, 618-621 |
| `0026FB90(data)` EFB loader | thunk `0026FF90` from `003788F0` | magic check, blobs, binding rows | Effect-File-Formats/efx-and-efb-effect-containers.md:429-462, 618-621 |
| `003A7E80` / `003A79C0` / `003A9730` / `003A9A70` | `003EDAD0` | chunk handlers 0x700 / 0x600 / 0x800 / 0xA00 | Effect-File-Formats/efx-and-efb-effect-containers.md:109-113, 479 |
| `004FF270` (55 B) / `00333C80` (889 B) | `003A7E80` / `003A79C0` | 0x700 relocator / 0x600 version normaliser | Effect-File-Formats/efx-and-efb-effect-containers.md:235-277 |
| `00377DC0` / `003788F0` / `003789A0` / `00378230` | `00378A60` (from `00331990` x2, `mapload` `0050D4D0`) | .efb request (0x43D170 block), mode-1 parse, mode-0 stub completion, teardown | Effect-File-Formats/efx-and-efb-effect-containers.md:284-300, 328-337 |
| `00540DB0` (389 B), `003A33B0` (280 B), `0039D6C0`, `0039D970` + 20 more | element walk arms | append 0x28 draw-list entry | Effect-File-Formats/effect-element-type-dispatch.md:342-367, 1822 |
| `0024D540` | `MainLoop_Draw`, `MainLoop_UpdateAndRenderFrame` | frame draw setup: `002D7FC0`, `003B3D20`, `003A3740` drain, `003A3A00` rewind, `0039D200` | Effect-File-Formats/effect-element-type-dispatch.md:432-449 |
| `003A3670` | not stated | allocates list 0x190000 B (`02F8F2F8`) and 0xC8028 B (`02F8F300`), zeroes counter | Effect-File-Formats/effect-element-type-dispatch.md:399-405 |

#### EF — Inputs and outputs (record layouts)

**EFX file** (Effect-File-Formats/efx-and-efb-effect-containers.md:79-82, 98-102, 222-233):

| off | size | meaning | cite |
|---|---|---|---|
| +0x00 | 8 | magic `EFX0010`/`EFX0009`/`EFX0008`, version global `01EFF3B0` = 10/9/8; unknown → version 10, return | Effect-File-Formats/efx-and-efb-effect-containers.md:80, 398-421 |
| +0x08 | 4 | float 1.0 in all files, unread | Effect-File-Formats/efx-and-efb-effect-containers.md:222-223, 231-232 |
| +0x0C | 4 | stream size; passed as size by 4 of 6 callers | Effect-File-Formats/efx-and-efb-effect-containers.md:223, 228-231 |
| +0x10 | … | chunk stream to `+0x0C` | Effect-File-Formats/efx-and-efb-effect-containers.md:89, 223-224 |
| chunk +0x00 | u32 | length (to next chunk) | Effect-File-Formats/efx-and-efb-effect-containers.md:99, 225 |
| chunk +0x04 | u16 | must be `0x100` else fallback `003EE2D0` | Effect-File-Formats/efx-and-efb-effect-containers.md:100, 393 |
| chunk +0x06 | u16 | type 0x600/0x610/0x620/0x630/0x700/0x800/0xA00 | Effect-File-Formats/efx-and-efb-effect-containers.md:101 |
| chunk +0x08 | i32 | stored to `02EBB738` before handler (bias) | Effect-File-Formats/efx-and-efb-effect-containers.md:225-226 |
| chunk +0x0C | 4 | handler arg; for 0xA00 `{u16 id, u8 type, u8 pad}` (type at +0xE) | Effect-File-Formats/efx-and-efb-effect-containers.md:226; Effect-File-Formats/effect-element-type-dispatch.md:806-808 |
| chunk +0x10 | … | record | Effect-File-Formats/efx-and-efb-effect-containers.md:226 |

Run handling: 0x700 run → one alloc at context `+0x880`, `003A7E80` each; 0x800 → `+0x870`, `003A9730`; 0xA00 → `+0x878`, `003A9A70`; copy vs borrow on context `+2` mask 4; 0x600/0x610/0x620 second buffer, 0x630 ends run (Effect-File-Formats/efx-and-efb-effect-containers.md:107-114, 134-140). Sizing: 0x600 `+0xB0`; 0x610 `n=byte chunk+0x13 (0→0x40)`, `n*4+0x30`, copy advance `0x330-(0xC0-n)*4`; 0x620 `+length` (Effect-File-Formats/efx-and-efb-effect-containers.md:119-129).
0x600 record (0xA0 B): index byte at +0; lane bytes +0x0A..+0x14 (11); 29 request dwords +0x2C..+0x9F reset to encoded null; high nibble of +0x16 = last non-zero lane; v8/v9 rewritten to v10 layout (Effect-File-Formats/efx-and-efb-effect-containers.md:258-277).
0x700 record: `+0xC0` index word, `+0xC2` subtype; subtype 0..3 fixed sizes 0x160/0x200/0x280/0x300 (8,029/472/60/64 chunks); dwords relocated `stored + low32(record) + bias` (Effect-File-Formats/efx-and-efb-effect-containers.md:235-256, 479).
0x800: id/subtype stored at payload +0x280/+0x282, payload published in `*(02EBEF90)[id]` (no bound check); subtype 0..8; 0xA00 via `02EBEF78` (Effect-File-Formats/efx-and-efb-effect-containers.md:183-186; Effect-File-Formats/effect-element-type-dispatch.md:812-814).

**EFB file** (Effect-File-Formats/efx-and-efb-effect-containers.md:84-87, 232-233, 453-462): +0x00 magic `EFB0001`/`EFB0002` (global `02F8F29D` = 1/2; reject returns 0); +0x08 u16 blob count; +0x0A u16 row count (`02F8F23A`); +0x0C u32 = 0; blobs `{u32 size; 12 bytes; EFX[size]}`; then rows: byte+0 type (3 → 0xA0 row, 1 → 0x60 skipped, 0 end), +1 must be 1, +4 binding channel 0-63, +5 definition id (`0024F610`), +8..+0xB per-weather-slot enables indexed slot+1.

**Element object** (fields stated; FBF + DISP):

| off | meaning | cite |
|---|---|---|
| +0x00 u8 | type (copied from def +0x44) | Effect-File-Formats/effect-element-type-dispatch.md:877, 834; Effect-File-Formats/an-effect-element-frame-by-frame.md:54 |
| +0x01 | flags: bit0 rate-gate skip; bit1/bit2 attachment resolvers | Effect-File-Formats/effect-element-type-dispatch.md:139, 931 |
| +0x02 word | rate-gate counter | Effect-File-Formats/effect-element-type-dispatch.md:138-139 |
| +0x08 | instance ("owner", matrix at `[+8]+0x40`) | Effect-File-Formats/effect-element-type-dispatch.md:839; Effect-File-Formats/an-effect-element-frame-by-frame.md:185 |
| +0x10 | parent (matrix `[+0x10]+0x40`) | Effect-File-Formats/an-effect-element-frame-by-frame.md:84 |
| +0x18 | spawn/source record (slots at +0x288..+0x2C6) | Effect-File-Formats/effect-element-type-dispatch.md:839; Effect-File-Formats/an-effect-element-frame-by-frame.md:141 |
| +0x20 | definition | Effect-File-Formats/effect-element-type-dispatch.md:840; Effect-File-Formats/an-effect-element-frame-by-frame.md:73 |
| +0x28 / +0x30 | list links | Effect-File-Formats/an-effect-element-frame-by-frame.md:135-136 |
| +0x38 | frame stamp compare | Effect-File-Formats/effect-element-type-dispatch.md:916 |
| +0x3C f32 | age (float) | Effect-File-Formats/effect-element-type-dispatch.md:917; Effect-File-Formats/an-effect-element-frame-by-frame.md:43 |
| +0x40 | current frame / first-frame flag, bit0 odd | Effect-File-Formats/effect-element-type-dispatch.md:926; Effect-File-Formats/an-effect-element-frame-by-frame.md:149,181 |
| +0x44 | whole-frame time used for track sampling | Effect-File-Formats/effect-element-type-dispatch.md:925-926; Effect-File-Formats/an-effect-element-frame-by-frame.md:73 |
| +0x48 | update count | Effect-File-Formats/effect-element-type-dispatch.md:925 |
| +0x4C | lifetime | Effect-File-Formats/effect-element-type-dispatch.md:920; Effect-File-Formats/an-effect-element-frame-by-frame.md:43-44 |
| +0x60 | position | Effect-File-Formats/an-effect-element-frame-by-frame.md:83 |
| +0x64 | floor/height compare | Effect-File-Formats/an-effect-element-frame-by-frame.md:46-47 |
| +0x70/+0x80 | position history (new/prev) | Effect-File-Formats/an-effect-element-frame-by-frame.md:74 |
| +0x90/+0xA0 | pre-parent history (type 0x05) | Effect-File-Formats/an-effect-element-frame-by-frame.md:178,213 |
| +0xB0/+0xB4/+0xC0 | velocity / vertical velocity / added vector | Effect-File-Formats/effect-element-type-dispatch.md:931 |
| +0xE0/E4/E8 | angle accumulators wrapped ±2π | Effect-File-Formats/effect-element-type-dispatch.md:931 |
| +0x130 / +0x140 | motion direction (>0.001) / up vector | Effect-File-Formats/an-effect-element-frame-by-frame.md:181-185 |
| +0x1D0+4i | last-fired frame per slot (-1 never) | Effect-File-Formats/an-effect-element-frame-by-frame.md:142 |
| +0x1F0 / +0x1F4 | instance colour (neutral `80808080`) / first colour copy | Effect-File-Formats/an-effect-element-frame-by-frame.md:75-78 |
| +0x1F8/+0x1FC/+0x200 | cached motion tracks | Effect-File-Formats/effect-element-type-dispatch.md:931 |
| +0x220 | cached floor | Effect-File-Formats/an-effect-element-frame-by-frame.md:272 |
| +0x224 / +0x226 | stamp from `00250000()` / cleared | Effect-File-Formats/effect-element-type-dispatch.md:70, 879-880 |
| +0x230.. | type-specific outputs (per FBF §2/§4 tables) | Effect-File-Formats/an-effect-element-frame-by-frame.md:83-233 |

Spawn slots (record `[element+0x18]`): tag `+0x298+i`, index `+0x288+2i`, start `+0x2A0+2i`, param `+0x2C6+2i`, 8 slots; tags 0 never / 1 once / 2 repeat (trigger 2, odd-frame skip, interval from `[[02EBEF90]][index]+0x10` via `004314E0`) / 3 trigger 3 / other every call (Effect-File-Formats/an-effect-element-frame-by-frame.md:140-152).
Cull record (`[02F97348]+0x2E0`, or def `+0x60` if first byte 0xFF): byte+0 mode 1/2/other, float +4/+8 window, byte+1 bit0 screen test `0x6000`..`0xA000` (Effect-File-Formats/an-effect-element-frame-by-frame.md:119-127).
Definition fields named: +0x44 type, +0x45 floor arm, +0x46 bounce percent, +0x48, +0x49 (≥0x20 percent alpha; bits 2,3), +0x4A bits 2-4 orientation mode, +0x4B bit1 scale composer / bit2 anchor floor, +0x4D rate, +0x4E, +0x4F anchor, +0x50/+0x54/+0x58 motion scales, +0x60 cull record, +0x70 floor, +0x75, tracks at +0x00/+0x10/+0x20/+0x30 (percent)/+0x80.. (Effect-File-Formats/an-effect-element-frame-by-frame.md:76-91, 171, 272; Effect-File-Formats/effect-element-type-dispatch.md:138, 141, 931).

**Draw list** `[02F8F2F8]`, count `word[02F8F2C6]`, entry 0x28: +0 arg (zero from `00540DB0`), +8 sort key (layer nibble from `02AEE910` in top byte +0xB, 24-bit key), +0xC second arg, +0x10 callback (null), +0x18 command node, +0x20 flags dword; capacity 40,960 per frame, no bound check; packet arena `02F8F2D0`/`02F8F2D8` from `02F8F308` (Effect-File-Formats/effect-element-type-dispatch.md:342-356, 403-406, 461, 505-507, 562-566; 00-0a cross-check `the-element-types-00-0a.md:486-491`).

#### EF — State (globals and objects, with lifetime)

| global/object | lifetime | initial | cite |
|---|---|---|---|
| `02EBEF88` instance list root (`+8` head); also compared as "global frame stamp" (EF.CV-1) | written by ten `0024B270`–`0024F4D0` + `003B8260` | not stated | Effect-File-Formats/effect-element-type-dispatch.md:115, 120, 916 |
| `02EBEF80` current instance | set per node by `003A8D80` | not stated | Effect-File-Formats/effect-element-type-dispatch.md:117 |
| `02F97348` action context / current container (cull record `+0x2E0`, `+0x36A`) | not stated | not stated | Effect-File-Formats/effect-element-type-dispatch.md:124; Effect-File-Formats/an-effect-element-frame-by-frame.md:120 |
| `02F97340` loader context (0x890-byte heap copy of template by `0024B3A0`; list `020910A0[kind]`) | ctor → `0024F410` teardown | template zeroed; `+2` = 0 or 0xC | Effect-File-Formats/efx-and-efb-effect-containers.md:135, 141-153 |
| element pool: owner active list `+0x118`/`+0x128`, free list `+0x120` | `00441B30` takes, `002F31C0` returns | not stated | Effect-File-Formats/an-effect-element-frame-by-frame.md:134-137; Effect-File-Formats/effect-element-type-dispatch.md:57 |
| `02EBEF90` 0x800 table (320 entries), `02EBEF78` 0xA00 table, `[02EBEFA8]` 0x600 table (= ctx +0x38), `[02EBEFA0]` 0x700 table (= ctx +0x840) | released by `003A9600`/`003A9950`, `003A75B0`/`003A7D30` | not stated | Effect-File-Formats/efx-and-efb-effect-containers.md:183-189, 279-282; Effect-File-Formats/effect-element-type-dispatch.md:813 |
| `02EBB738` per-chunk bias | per chunk | — | Effect-File-Formats/efx-and-efb-effect-containers.md:225 |
| `01EFF3B0` EFX version, `02F8F29D` EFB version | per load; reject leaves 10 | not stated | Effect-File-Formats/efx-and-efb-effect-containers.md:401-421, 436-439 |
| `02F8F2C0..` EffectDrawListHeader (counter `+6`, cursors `02F8F2D0/EF.G-8`, stats `02F8F2CC/CE/E8/F0`) | alloc `003A3670`; drain `003A3740`; rewind `003A3A00` per frame | counter zeroed by `003A3670` | Effect-File-Formats/effect-element-type-dispatch.md:399-467 |
| `02ADD088` EFB block (0x43D170 B) | `00377DC0` alloc; freed only by `00378230` | — | Effect-File-Formats/efx-and-efb-effect-containers.md:284-300 |
| `01DFE0B4/B8/BC` frame-rate triple | written once at startup by `001EDDC0` | ships {1,1.0,1.0} | Effect-File-Formats/effect-element-type-dispatch.md:948-951 |
| `01EF93E8` render RNG, `022D9138` mode word | not stated | not stated | Effect-File-Formats/an-effect-element-frame-by-frame.md:234-238 |
| `01F83530` pointer base | zero at image load | 0 | Effect-File-Formats/effect-element-type-dispatch.md:577-586 |

#### EF — Order (what runs when, and what triggers it)

1. Frame draw setup `0024D540` (from MainLoop_Draw / MainLoop_UpdateAndRenderFrame): `002D7FC0`, `003B3D20`, drain `003A3740`, rewind `003A3A00`, `0039D200` (Effect-File-Formats/effect-element-type-dispatch.md:432-449).
2. Instance walk `0024D370` → `003A72F0` → `003A8D80` → `00441970` → `002F4020` per element (walk/draw) (Effect-File-Formats/effect-element-type-dispatch.md:113-145). Walk arms append to the draw list during the frame (Effect-File-Formats/effect-element-type-dispatch.md:448-450).
3. Update: `0043EF40` (caller dt) or `00442310` (2.0×reciprocal) → `002F3910` → `002F2530` base (once per game frame; age; half-rate gate; expiry/floor end → `003A8950(3)` + `002F31C0`) → type tail → `005002E0` → release `002F31C0` or `003A8950(2)` (Effect-File-Formats/effect-element-type-dispatch.md:937-956; Effect-File-Formats/an-effect-element-frame-by-frame.md:40-61, 79-80). Who triggers `0043EF40` per frame: callers `003A8390`/`0043F450` only (Effect-File-Formats/effect-element-type-dispatch.md:102).
4. Birth: `003A8AE0` → `00441B30` (free list) → `002F3BC0` step → `002F2D60` (Effect-File-Formats/effect-element-type-dispatch.md:55-58); setup `005004C0` when elements are built from EFX parse / instance creation (Effect-File-Formats/effect-element-type-dispatch.md:154-159).
5. Load: `003EDAD0` chunk handlers at file load; `004FF270` relocation once (Effect-File-Formats/efx-and-efb-effect-containers.md:235-256).
Relative order of steps 2 and 3 within a frame: not stated.

#### EF — Dependencies

CoreRuntimeScheduling `001EDDA0` half-rate test (Effect-File-Formats/an-effect-element-frame-by-frame.md:264-266); Movement `00264670`/`002F3750` floor anchor (Effect-File-Formats/an-effect-element-frame-by-frame.md:272); Audio clamps `0036DDA0`/`0036DD90` (Effect-File-Formats/an-effect-element-frame-by-frame.md:268-270); RNG `01EF93E8` (Effect-File-Formats/an-effect-element-frame-by-frame.md:234-236); Position-To-Scalar distance fade/stash `02AED5F0`, matrix `02AEEA20` (Effect-File-Formats/an-effect-element-frame-by-frame.md:129-132); Game settings half-rate/frame-rate triple (Effect-File-Formats/an-effect-element-frame-by-frame.md:256-258; Effect-File-Formats/effect-element-type-dispatch.md:948-952); Authored expressions `004309C0`/`004314E0`/`00431830` (Effect-File-Formats/effect-element-type-dispatch.md:630-635); Shared transform workbench `004355D0`, `0042FDB0` (Effect-File-Formats/effect-element-type-dispatch.md:647-649); Legacy-PS2 VIF1/VU1 GiVmax `001DB7E0`/`001DB840`, `003A34D0`/`003A35E0` (Effect-File-Formats/effect-element-type-dispatch.md:527-560); Gi family `0020E630` (Effect-File-Formats/effect-element-type-dispatch.md:559-560); ActorEntity `003588B0`, `00265020` (Effect-File-Formats/effect-element-type-dispatch.md:988-995); Resource `002ED570`, `0036A100`, `003B37E0` (Effect-File-Formats/effect-element-type-dispatch.md:1020; Effect-File-Formats/efx-and-efb-effect-containers.md:204-207); Memory arena `0036C1D0`/`0036C140`, `0036B130` (Effect-File-Formats/efx-and-efb-effect-containers.md:445, 193-194); Weather roll EFB channels 0 / 0x1F (Effect-File-Formats/efx-and-efb-effect-containers.md:460-461); Map load `00331990`/`00378A60` (Effect-File-Formats/efx-and-efb-effect-containers.md:329-331); FEF op 0x28 lane map (Effect-File-Formats/efx-and-efb-effect-containers.md:273-274); model path `003B38B0` → `003EDAD0` (Effect-File-Formats/effect-element-type-dispatch.md:799-800).

### 1.8 [ET] Effect element types, kind-0x54 meshes, menu effect registry and VFX layers

Short names in this part: **mesh** = `Effect-File-Formats/effect-mesh-records-kind-54.md`; **00-0a** = `Effect-File-Formats/the-element-types-00-0a.md`; **40-42** = `Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md`; **60-74** = `Effect-File-Formats/the-element-types-60-74.md`; **80-97** = `Effect-File-Formats/the-element-types-80-97.md`; **menu** = `Effect-File-Formats/the-menu-effect-registry.md`; **six-layers** = `Effect-File-Formats/the-six-vfx-display-layers.md`.


#### ET — Entry points

| entry (size) | callers as stated | what it does | cite |
|---|---|---|---|
| `00258EE0` VFX layer pass (307 B) | `MainLoop_Draw` `0022B0B0` (layer-6 pass at `0022B694`) | six layers by number; markers; layers 1,2,4,5,6 call grouped pass; layer 3 own path | Effect-File-Formats/the-six-vfx-display-layers.md:26-38, :160 |
| `00259030` grouped pass (179 B) | `00258EE0` | bracket, wait bit 8 of `02EAF6D8`, two emit-module routines, groups 2,3,5,6,9,1,7,4 via `0024D370`, drain `003A3740` | Effect-File-Formats/the-six-vfx-display-layers.md:43-50 |
| `0024D370` group draw (367 B) | grouped pass | walks containers of a group from `020910F0` | Effect-File-Formats/the-six-vfx-display-layers.md:58-84 |
| `0024D4E0` group gate (94 B) | `0024D370`; also registry walker `00377230` | enable-word AND test | Effect-File-Formats/the-six-vfx-display-layers.md:64-67; Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:119 |
| `0024D770` per-container gate (431 B) | `0024D370`; `00377230` | kind-switched draw permission | Effect-File-Formats/the-six-vfx-display-layers.md:89-101; Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:119 |
| `0024ED80` make container current (132 B) | `0024D370`; UI `0024B9B0` | publishes ten globals | Effect-File-Formats/the-six-vfx-display-layers.md:72-79, :162, :264 |
| `0024C640` layer-table reset (97 B) | `00258EE0` tail `00258F8B` (layers 1,2,4), `002590F0` | zeroes `word[+0x32]` per chain of `020910A0` rows 1-9 (8 skipped), clears `0x1800` B at `02F8DA00` and `02F8C200` | Effect-File-Formats/the-six-vfx-display-layers.md:186-197 |
| `0039CFF0` (198 B) | `00258EE0` layer 4 only, ids `0x3C00`/`0x3700` | ensure-allocated state call | Effect-File-Formats/the-six-vfx-display-layers.md:236-238 |
| `0036F550` (1172 B) / `0036F9F0` (438 B) | `00258EE0` | per-layer record emit / reset | Effect-File-Formats/the-six-vfx-display-layers.md:218, :226 |
| step dispatcher, one driver `00441B30` | — | runs a step on an element just taken off owner free list `+0x120` (step = birth) | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:113-115 |
| `002F2D60` base step (1111 B) | every derived step | zeroes age `+0x3C`/`+0x40`, update count `+0x48` | Effect-File-Formats/the-element-types-00-0a.md:39-41, :98; Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:113-114 |
| `002F2530` base update (2094 B) | every derived update | frame-advance | Effect-File-Formats/the-element-types-00-0a.md:49-51, :99 |
| `00500470` base setup | every setup | rebases four heads `+0x00..+0x30`, returns `element+0x80` | Effect-File-Formats/the-element-types-00-0a.md:54-57, :97 |
| setup helpers `004304F0`/`00430AF0`/`0042FCF0`/`00431040`/`00430A60`/`00431580`/`00431770` | setups | rebase heads/groups/bundles; float/int scale | Effect-File-Formats/the-element-types-00-0a.md:76-85, :227-231 |
| `005002E0` cull/fork | every tail | selects `002F31C0` release or `003A8950(2)` spawn | Effect-File-Formats/the-element-types-00-0a.md:473-474; Effect-File-Formats/the-element-types-80-97.md:145-146 |
| per-type step/update/walk/setup/seventh | dispatch tables | per-type rows | Effect-File-Formats/the-element-types-00-0a.md:93-202; Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:34-93; Effect-File-Formats/the-element-types-60-74.md:53-153; Effect-File-Formats/the-element-types-80-97.md:41-118 |
| emit front ends `0039C550` (121 B, 1 point), `0039C4C0` (134 B, 2 points) | walks 0x01, 0x03 | project, clip, choose emitter on `02AEE900` | Effect-File-Formats/the-element-types-00-0a.md:247-249 |
| emitters `0039D890`/`0039D5A0` (mode 0), `0039D970`/`0039D6C0` (modes 1-7) | front ends | build GiPrim; modes 1-7 append display-list entry | Effect-File-Formats/the-element-types-00-0a.md:270-273, :485-496 |
| `008642A0` GiPrim constructor (133 B) | emitters | allocates `0x68`-byte record for n vertices, returns record+8 | Effect-File-Formats/the-element-types-00-0a.md:255-256, :503 |
| grid emitter `004434D0` (3,681 B) / `00444340` | walks 0x04/0x06/0x07 | up to four texture layers | Effect-File-Formats/the-element-types-00-0a.md:417-422 |
| sprite frame drawers `00501A50` / `00502280` | 0x02, 0x0A walks | multi-part sprite frame | Effect-File-Formats/the-element-types-00-0a.md:375, :335-340 |
| `00377230` registry walker | `MainLoop_Draw`, `MainLoop_UpdateAndRenderFrame` | per drawn frame: visibility, shown bit, apply body of 0x40/0x41/0x42/0xD0 | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:118-122 |
| `00377190` registry issuer | the four births | 128-slot registry `02ADBFE0` | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:116-118 |
| `003D83A0` shake list walker (2,190 B) | only `0037D970` | shake accumulator | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:156-163 |
| `00258B90` (472 B) | not stated | copies effect camera `02092628` into `02096FA0` each frame, switches cameras 6,4 off on release | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:260-263 |
| `003B4310` | `CharacterRenderRecord_UpdateViewDependentPresentationFactors` via `003E4E70` | darkest colour filter per character | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:138-141 |
| kind-0x54 loader `00436D00` | dispatcher `003A9EF0` | payload → runtime mesh | Effect-File-Formats/effect-mesh-records-kind-54.md:27-29, :70-88 |
| `003A9A70` | — | publishes `0xA00` element record into table `02EBEF78` (768 slots) | Effect-File-Formats/effect-mesh-records-kind-54.md:146-147 |
| `003AA280(key, kind, sub)` | setups | record resolver | Effect-File-Formats/effect-mesh-records-kind-54.md:149-150; Effect-File-Formats/the-element-types-00-0a.md:85 |
| vertex prep `00435050` / `00434CD0` | "one caller chooses" (not named) | one-record copy / two-record blend | Effect-File-Formats/effect-mesh-records-kind-54.md:194-201 |
| kernel `00432300` | vertex prep | `min(255, e·c >> 7)` | Effect-File-Formats/effect-mesh-records-kind-54.md:217-219 |
| `003B29B0` registry reset+load | `00558FB0`, `00561390`, `00572E10` | clear 64 records, `0024C460(4)`/`0024C550(4)`, build `0x890` EFX template byte+0=4 via `0024B3A0`, parse `003EDAD0` | Effect-File-Formats/the-menu-effect-registry.md:60, :74 |
| `003B2D80(a,b,c,kind)` spawn | 13 sites, 8 callers | instance via `0024B270`, free record via `003B2BC0`, stores args | Effect-File-Formats/the-menu-effect-registry.md:61, :114, :119 |
| `003B2BC0` find free | spawn | scan id==0, unrolled ×4 | Effect-File-Formats/the-menu-effect-registry.md:62 |
| `003B2AA0(id)` remove | `00557DB0` (6 sites), `005588C0`, `00558960`, `0055B560`, trio | release `+8` via `0024EE60`, compaction, clear `02EBE598` | Effect-File-Formats/the-menu-effect-registry.md:63, :75 |
| `003B2930(instance)` | not stated | remove by pointer | Effect-File-Formats/the-menu-effect-registry.md:64 |
| `003B2F50(id,value)` | achievements trio only | `[instance+0x338] = value` | Effect-File-Formats/the-menu-effect-registry.md:65, :116 |
| `003B2CE0` (129 B) | not stated | classifier → 0..5 | Effect-File-Formats/the-menu-effect-registry.md:230 |
| `0024C550` (138 B) | registry reset | per-kind list drain | Effect-File-Formats/the-menu-effect-registry.md:194-200 |
| `0024FCF0` | activation callers `0024D050`, `0024D540`, `003B8260` | publishes instance `+0x300..+0x338` | Effect-File-Formats/the-menu-effect-registry.md:117 |

#### ET — Inputs and outputs (record layouts)

**`0xB00` chunk (kind-0x54 record store)** — Effect-File-Formats/effect-mesh-records-kind-54.md:55-64

| off | size | meaning |
|---|---|---|
| +0x00 | u32 | chunk length (16-aligned) |
| +0x04 | u16 | flag = 0x100 |
| +0x06 | u16 | type = 0xB00 |
| +0x08 | u32 | stream length = length − 0x10 |
| +0x0C | u16 | key (0 in all 2,252) |
| +0x0E | u8 | kind = 0x54 |
| +0x0F | u8 | sub (selector id) |
| +0x10 | … | payload, padded |

**kind-0x54 payload** — Effect-File-Formats/effect-mesh-records-kind-54.md:72-88, size formula :92-93

| off | size | meaning → runtime |
|---|---|---|
| +0x00 | u8 | flags (0x07 always): bits 0-2 → `+0x18C`; bit 3 borrow/copy |
| +0x02 | u16 | tri → `+0x10` |
| +0x04 | u16 | quad → `+0x12` |
| +0x06 | u16 | c14 positions → `+0x14`, array `+0x20`, 16 B, w forced 1.0 |
| +0x08 | u16 | c16 vectors → `+0x16`, array `+0x24`, 16 B (unit normals, `:203-206`) |
| +0x0A | u16 | c18 → `+0x18`, array `+0x28`, 4 B (RGBA8 per-corner colour, `:215`) |
| +0x0C | u16 | c1A → `+0x1A`, array `+0x2C`, 8 B (float UV, `:216`) |
| +0x0E | u16 | c1C → `+0x1C`, ids `+0x180`, handles `+0x184` (8 B each) |
| +0x10 | u16 | c1E → `+0x1E`, 20-B inline records `+0x30` (cap 16; always 0) |
| +0x12 | — | arrays: pos, vec, 4B, 8B, 20B; if flags&1 index lists A, B (2·(6·tri+8·quad) B each → `+0x170`/`+0x174`); (tri+quad) bytes → `+0x188`; c1C id bytes → `+0x180` |

`c18 = 3·tri + 4·quad` (Effect-File-Formats/effect-mesh-records-kind-54.md:217). Ids resolve to same-file kind-0x52 records (Effect-File-Formats/effect-mesh-records-kind-54.md:139-141).

**`0xA00` element-definition chunk** — `{u16 id, u8 type, u8 pad}` at chunk+0x0C, record at chunk+0x10 (Effect-File-Formats/effect-mesh-records-kind-54.md:145-148).

**Element definition record (`[element+0x20]`)** — opens with four track heads `+0x00..+0x3F` (Effect-File-Formats/the-element-types-00-0a.md:97, :210-215);
head = 0x10 B `{ptrA, ptrB, …, countA @+0xC, countB @+0xD}`, each pointer to `{u32, f32}` 8-B keyframe arrays (Effect-File-Formats/the-element-types-00-0a.md:78-82);
groups 3G = 0x40 B, 4G heads at +0/+0x10/+0x20/+0x30 (Effect-File-Formats/the-element-types-00-0a.md:79-80); `0xF0`-byte texture-layer bundle: sub-tracks +0x00/+0x40,
encoded ptrs +0x90/+0x94/+0xE0/+0xE4, byte +0xA9, +0xAA bits 4-5 (Effect-File-Formats/the-element-types-00-0a.md:227-231). Definition `+0x44` = type
(Effect-File-Formats/the-element-types-60-74.md:334; dispatch page). `+0x49` bits 5-7 = blend mode (Effect-File-Formats/the-element-types-00-0a.md:268, :317); `+0x30` = percent/blend track (Effect-File-Formats/the-element-types-00-0a.md:243-244,
:282-283); `+0x48` rotation order (Effect-File-Formats/the-element-types-00-0a.md:320); `+0x4A` bit 2 view-built matrix (Effect-File-Formats/the-element-types-00-0a.md:316). Per-type maps: Effect-File-Formats/the-element-types-00-0a.md:104-196;
Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:36-46, :66-73; Effect-File-Formats/the-element-types-60-74.md:55-153; Effect-File-Formats/the-element-types-80-97.md:45-63.

**Element (runtime) fields named** — `+0` type byte/draw byte; `+0x3C`/`+0x40` age, `+0x44` frame index, `+0x48` update
count (Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:113-114; Effect-File-Formats/the-element-types-00-0a.md:469; Effect-File-Formats/the-element-types-60-74.md:184); `+0x1F0` colour, `+0x1F1` bits (Effect-File-Formats/effect-mesh-records-kind-54.md:162-164, :201, :219); `+0x230` matrix
(Effect-File-Formats/the-element-types-00-0a.md:111, :312); per-type fields in GI-14 table Effect-File-Formats/the-element-types-00-0a.md:476-483.

**Blend table** `01EFAC20[mode]`, eight qwords `0x44, 0x48, 0x42, 0x44, 0x49, 0x46, 0x80000000A8, 4`; mode 6 uses `02AEE908`
(Effect-File-Formats/the-element-types-00-0a.md:275-280). GiPrim `+0x38` → `001EE650` GS ALPHA translator (Effect-File-Formats/the-element-types-00-0a.md:503). Topology table `01F44D20` (`0,1,6,2,3,4,…`) at
record `+0x48` (Effect-File-Formats/the-element-types-00-0a.md:257-258).

**Display-list entry** (`[02F8F2F8]`, count `02F8F2C6`), 0x28 B: callback/arg null, sort key `+8` = depth with pass nibble
`02AEE910` in bits 28-31, `+0xC` = 1, own command list `+0x18`, flag dword `+0x20` (Effect-File-Formats/the-element-types-00-0a.md:273, :485-491).

**0x40 light request** kinds 0/1/2 → words 0x8002/0x8001/0x8006 (Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:128-133). **0x41 filter record** 64-slot pool
`02B404E0`, 0x60 B (Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:135-141). **0x42 shake slot** 32×0x60 pool `02B4D7D0`, request copied to +0x30..+0x4F; f0/f1/f2 at
def +0x124/+0x128/+0x12C (Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:143-154). **0xAB packet** nine 16-B descriptors, `0x4F0 + 0x2D0 + 0x2E0·(n−1)` (Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:169-188).
**0xD0** flag word +0x232, selector +0x230 table (Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:199-216), render record `022C6F28 + id×0x740` fields
+0x220..+0x22C, +0x4A0..+0x4B0 (Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:218-227).

**Menu registry record** (`02EBDBC0..02EBE5C0`, 64 × 0x28): +0x00 u32 id (0 free), +0x08 instance ptr, +0x10 a, +0x14 b,
+0x18 c, +0x1C kind, +0x20 bit 0 cleared, +0x24 untouched (Effect-File-Formats/the-menu-effect-registry.md:49-53, :114). Id = `(count & 0xFFFFFFF) | bit 30` (Effect-File-Formats/the-menu-effect-registry.md:119).
Instance fields: `+0x338` mode base (Effect-File-Formats/the-menu-effect-registry.md:117), `+0x373` kind (Effect-File-Formats/the-menu-effect-registry.md:114), `+0x304` float (+2.45 for kind 0x13, Effect-File-Formats/the-menu-effect-registry.md:114).

**Effect container (group list)**: next `+0x348`, mode word `+0x3A8`, layer = top nibble of `+0x378`, flag byte `+0x36A`,
`+0x364` never-draw, kind byte `+0`, resource `+0x340`, `+0x380` commit pointer, `+0x39B` (Effect-File-Formats/the-six-vfx-display-layers.md:69-81, :91-98).

#### ET — State (globals and objects, with lifetime)

| global | size / shape | lifetime / init | cite |
|---|---|---|---|
| `02EBDBC0` registry | 64 × 0x28 | cleared by `003B29B0`; compaction keeps it compact | Effect-File-Formats/the-menu-effect-registry.md:49, :60, :63 |
| `02EBE5C0` count/state word | u32 | cleared by `003B29B0` (`003B2A27`) | Effect-File-Formats/the-menu-effect-registry.md:53 |
| `02EBEF88` effect instance list | ptr | eleven writers | Effect-File-Formats/the-menu-effect-registry.md:67-68; Effect-File-Formats/the-six-vfx-display-layers.md:74 |
| `02EBEF78` element record table | 768 slots (0x1800 B) | freed by `003A9950` | Effect-File-Formats/effect-mesh-records-kind-54.md:147; Effect-File-Formats/the-menu-effect-registry.md:367 |
| `020910F0` group list heads | one ptr per group | not stated | Effect-File-Formats/the-six-vfx-display-layers.md:62 |
| `020910A0` per-kind table rows 1-9 | `+8` chains | `0024C640` zeroes `word[+0x32]` | Effect-File-Formats/the-six-vfx-display-layers.md:186-191; Effect-File-Formats/the-menu-effect-registry.md:196 |
| `02092162/4/6` group-enable words | 3 words | writers not read | Effect-File-Formats/the-six-vfx-display-layers.md:65-67 |
| `02092700` current group | int | set per group, reset to −1 | Effect-File-Formats/the-six-vfx-display-layers.md:68 |
| `02F97348`, `02F97340`, `02EBEF90`, `02EBEF88` … | current container / resource / sub-resource | written by `0024ED80` | Effect-File-Formats/the-six-vfx-display-layers.md:72-75 |
| `02EBD480` handle table | 64 × 0x38 | per-frame bit-1 handshake | Effect-File-Formats/the-six-vfx-display-layers.md:98 |
| `02F8F310` | byte | bit 0 raised by container flag bit 1; bit 2 chooses layer-3 path | Effect-File-Formats/the-six-vfx-display-layers.md:81-82, :118-119 |
| `02F8F2F8` / `02F8F2C6` | sorted list base / count | drained by `003A3740` each layer | Effect-File-Formats/the-element-types-00-0a.md:273; Effect-File-Formats/the-six-vfx-display-layers.md:46 |
| `02AEE900` / `02AEE908` | blend mode dword / track qword | written by walks, read by emitters | Effect-File-Formats/the-element-types-00-0a.md:243-249, :268 |
| `02AEE910` | pass nibble byte | not stated here | Effect-File-Formats/the-element-types-00-0a.md:273 |
| `02AEE7F4` / `02AEE7F0` | mode base / mode+base | `0024FCF0` / `0039B620` | Effect-File-Formats/the-menu-effect-registry.md:117 |
| `01EF93E8`, `022D9138` | PRNG state / guard | not stated | Effect-File-Formats/the-element-types-60-74.md:45 |
| `02091150` / `02092168` | deferred-free queue (0x100 qwords) / count | not stated | Effect-File-Formats/the-element-types-60-74.md:48 |
| `02ADBFE0` | 128 × 0x20 registry, handle `serial<<8|slot` | births register, `00377360` unregisters | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:116-118 |
| `02B404E0` | 64 × 0x60 filter pool | not stated | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:135 |
| `02B4D7D0` | 32 × 0x60 shake pool | slot freed on duration | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:143-151 |
| `02B4D7B8` | global shake scale | not stated | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:163 |
| `02092628` | current effect camera ptr | set by 0xD1 tail, cleared by `00258B90` | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:260-261 |
| `02092631` / `02092632` | release flags | set by `003D90C0` | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:261 |
| `020926C0` | global scene colour | multiplied by 0xD0 | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:200 |
| `01E02814` | language id | written at startup `0022A0CB` | Effect-File-Formats/effect-mesh-records-kind-54.md:231 |

#### ET — Order (what runs when, and what triggers it)

| when | what | cite |
|---|---|---|
| each draw frame | `MainLoop_Draw` → `00258EE0` six times (layer 6 at `0022B694`); exact call order of layers "not a measurement" | Effect-File-Formats/the-six-vfx-display-layers.md:25-27, :54-56, :160 |
| per layer 1,2,4,5,6 | grouped pass: groups 2,3,5,6,9,1,7,4, then drain `003A3740` | Effect-File-Formats/the-six-vfx-display-layers.md:44-48, :133 |
| layer 4 | state call `0x3C00` … `0x3700` | Effect-File-Formats/the-six-vfx-display-layers.md:36, :134 |
| layers 4,5 | extra call unless mode getter non-zero | Effect-File-Formats/the-six-vfx-display-layers.md:36-37, :135 |
| after layers 1,2,4 | `0024C640` reset | Effect-File-Formats/the-six-vfx-display-layers.md:196-197 |
| per container | gate → make current → transform composer → instance-list walk → element walks | Effect-File-Formats/the-six-vfx-display-layers.md:69-84 |
| element birth | step method (free-list pop by `00441B30`) | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:113-115 |
| per frame | update = base `002F2530` + tail; tail ends in cull/fork | Effect-File-Formats/the-element-types-00-0a.md:49-53, :472-474 |
| step body | base, then tail, then `0044B960` (0x80-0x97) | Effect-File-Formats/the-element-types-80-97.md:114 |
| per drawn frame | `00377230` registry apply for 0x40/0x41/0x42/0xD0 | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:118-121 |
| per frame | `0024D540` activation, driven by `MainLoop_UpdateAndRenderFrame` | Effect-File-Formats/the-menu-effect-registry.md:169 |

#### ET — Dependencies

Gi render commands (GiPrim, `001EE650`, display list): Effect-File-Formats/the-element-types-00-0a.md:254, :503. Workbench `0026EE00`/`002F1F40`/`0039B620`/`0039AF70`:
Effect-File-Formats/the-element-types-00-0a.md:58-64. VU0 register bank: Effect-File-Formats/the-element-types-00-0a.md:156-160. Character lighting: Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:127. Character render record/object (refraction):
Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:218-246. Camera system / shake: Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:157-163, :260-263. Battle action effects → `magic\mNNNN.efx`: Effect-File-Formats/the-element-types-60-74.md:274-281.
Per-model oscillator: Effect-File-Formats/the-element-types-60-74.md:201. UI/licence board/achievements: Effect-File-Formats/the-menu-effect-registry.md:96-100, :119. Language cache: Effect-File-Formats/effect-mesh-records-kind-54.md:228-237. Distance-fade
node: Effect-File-Formats/the-element-types-00-0a.md:239-245. Resource allocator `0036A190`: Effect-File-Formats/the-element-types-00-0a.md:461. World transition field id: Effect-File-Formats/the-element-types-80-97.md:187.

### 1.9 [MF] Model formats: add-motion tables, ADM, FCP, FDM/FOR

Short names in this part: **SKEL** = `Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md`; **ADM** = `Model-And-Motion-Formats/adm-add-motion-tables.md`; **FCP** = `Model-And-Motion-Formats/fcp-character-parameter-block.md`; **FDM** = `Model-And-Motion-Formats/fdm-and-for-entries.md`; **MREADME** = `Model-And-Motion-Formats/README.md`.


#### MF — Entry points

| entry (address, size) | callers as stated | what it does | cite |
|---|---|---|---|
| `AddMotion_LoadSkeletonMapping` `0036FFF0` | `0022A0B0` at `0022A442` | opens `SkeletonMapping.bin` with `001D6F20(path,1)`, `_alloca(size+1 rounded to 16)`, reads whole, parses; size 0 skips | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:90-98 |
| `AddMotion_LoadHighModelReplace` `0037CCC0` | `0022A0B0` at `0022A43D` | same load pattern; first pass counts records, then fills a `count × 0x30` zeroed array | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:90-103, 163-167 |
| `0022A0B0` | not stated on these pages (World body `00266D10` calls it, Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:350) | "the boot routine" | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:234 |
| `0037CB90(modelId, b, c)` replacement lookup | `003409F0`, `bindhoff` handler `003460F0` (verb `0x00D8`), `0037B4D0` | `-1` unless `01E02800` set and table loaded; first record matching id and `b`/`c` (or `-1`), returns the last pair whose threshold `<=` `FieldData_GetVariable0` (`00265270`) | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:111-118 |
| `00372820` pose-record setup (1,844 B) | `0046E4D0` | copies 32-byte name to record `+0x20`, scans mapping, stores the **last** matching index at `+0xB0` (`-1` none); calls `00373DC0`, `00373D00`, `00373EA0` | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:107-110, 360-372, 506, 518 |
| `Skeleton_UpdateFinalPoseAndCombatLook` `003703A0` | `0046E0F0` (from `0041E340` "per model record between frames"), after `00373F40` | indexes `02AD9E30` by `+0xB0`; "maps only at state 2" | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:108-110, 218, 510 |
| `AddMotion_LoadResources` `001BDD20` | `001BDC40` at `001BDC7F` (once) | reads `add_motion_list.txt`, for each name parses `%s.adm` and `%s_town.adm` | Model-And-Motion-Formats/adm-add-motion-tables.md:104-113 |
| `AddMotion_ParseFile` `001BE1A0` | `001BE00F` (from the loader) | builds 32-byte record / 16-byte tracks / `0x28` groups / `0x1C` records | Model-And-Motion-Formats/adm-add-motion-tables.md:115-117 |
| `AddMotion_LookupByModelName` `001BE430` (235 B) | `00863110` only | finds a model's record and its `"%s_town"` twin | Model-And-Motion-Formats/adm-add-motion-tables.md:127-128, 342, 435-436 |
| `00863110` (183 B) | `002EDF90` only | resource id → path → base name (last `\` to first `.`) → name lookup; fills both handles | Model-And-Motion-Formats/adm-add-motion-tables.md:147-149, 436 |
| `002EDF90(recordIndex, request, resourceId)` (179 B) | the element binder of the actor's secondary context (party read-in state machine k-enum): set = request 1 base / request 2 body; clear = 0 to both | five-state machine on render record `+0x6C8`; stores handles `+0x6E8`/`+0x6F0` | Model-And-Motion-Formats/adm-add-motion-tables.md:135-152 |
| `002E7CE0` (226 B) | not stated | applies a 16-bit value to the base record, and to the body record only in state 1 | Model-And-Motion-Formats/adm-add-motion-tables.md:152-154 |
| `AddMotion_ApplyBonePose` `003714A0` (3,387 B) | `Skeleton_ComposeFinalPose` `00373860` (1,170 B) only | builds `table1[bone]=trackIndex`, `table2[bone]=recordIndex` from group 0; selects groups by kind 0 (key interpolation) or kind 1 (id match); lerps Euler degrees; `Matrix4x4f_BuildEulerRotation` `0046D380` | Model-And-Motion-Formats/adm-add-motion-tables.md:128-133, 295-311, 415-484 |
| `004776D0` (117 B) | `003714A0` | packed channel-table decoder at `02CA6CA0 + cl*0x40`; returns slot value or `-1` | Model-And-Motion-Formats/adm-add-motion-tables.md:318, 465-467 |
| `0017FFB0` (32 B) / `00180060` (36 B) / `00180090` (40 B) | `003714A0` | town override getter (`001BE420()+0x20`); interp-override flag `+0xCF1`; override value `+0xCF4` of `001D50D0()` | Model-And-Motion-Formats/adm-add-motion-tables.md:315-317 |
| `CharacterRenderRecord_RefreshFCPPayloadByRecordId` `002EDBD0` | not stated on page | resolves model id `+0x408`, finds `'@FCP'` by tag + record name `+0x3C`, stores section+0x30 at `+0x400` (0 if missing) | Model-And-Motion-Formats/fcp-character-parameter-block.md:161-168 |
| `003E55F0` payload getter | eleven callers (not listed) | returns record `+0x400` | Model-And-Motion-Formats/fcp-character-parameter-block.md:168, 187 |
| `004FE270` float getter / `004FE2F0` int and bit-field getter | 43 call sites, 50 ids | `SS VV DD FF` decode, default tables `01F265B0` / `01F266B0` | Model-And-Motion-Formats/fcp-character-parameter-block.md:170-185, 255-256, 462-464 |
| `003E6150(recordIndex,id)` | battle side; `002ECE50` | float read × render record `+0x26C` for listed ids, ÷ for `0x9001E1F` | Model-And-Motion-Formats/fcp-character-parameter-block.md:194-199 |
| `003204E0` / `003204D0` | `00239E10` (12×), `00320D70`, `BattleFormula_ComputeKnockbackImpulseScale`, `003045A0`, `00236210` | index 0-33 → id via `01EED320`; optional y-scale multiply/divide | Model-And-Motion-Formats/fcp-character-parameter-block.md:202-209, 305-348 |
| `00239E10` installer | `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` | writes the twelve unit tunables | Model-And-Motion-Formats/fcp-character-parameter-block.md:202-224 |
| `0041E5B0(record,state,eventId)` | `004292B0` | six-byte event map → `@FMC` entry `[record+0x2FA]+i`, started by `00423B10` | Model-And-Motion-Formats/fcp-character-parameter-block.md:99-104, 188 |
| `003E5AD0(record,id)` | `0041EDE0`, `0041F010` and others | special-bone lookup: section1 `+0x14C + id×2`; ids `0x104/0x105/0x106` → `+0x3A/+0x3C/+0x3E` | Model-And-Motion-Formats/fcp-character-parameter-block.md:119, 187 |
| `0041EDE0(parent,child,slot,mode)` (555 B), `0041F010(parent,child)` | `0041F010`: `004215A0` (dirty bit 19), `00424D80` (×2); command `0x15` via `00429760` | attach child to parent bone through section 3 | Model-And-Motion-Formats/fcp-character-parameter-block.md:562-593 |
| `003E6770(record,enable)` (276 B) | not stated | section 4 → up to 4 trail objects in pool `02CA8420`, handles `+0x438..+0x444` | Model-And-Motion-Formats/fcp-character-parameter-block.md:606-616 |
| `0041FCF0` render-record initialiser | not stated here | reads section 2 via `003E4B40`, `+0x24` length; `0041F340` → `00372820` memcpy into `@FTR` tail; section-8 copy at `0041F5CE`/`0041F5D9`; turns section 8 on | Model-And-Motion-Formats/fcp-character-parameter-block.md:630-645, 719-721, 745 |
| `003AF3B0` (in `003AF390`) | — | section 10: spawn period = `f32[+8] / u8[+0x10]` | Model-And-Motion-Formats/fcp-character-parameter-block.md:760-768 |
| Section-8 routines `0051D310`, `0051CDE0`, `0051DB60`/`00519720`, `0051DBE0`, `0051D2F0` | `00425E10`, `00425DC0`, `003E6710`, LOD updates `0042CBF0`/`0042D050`, `00421280`/`004213E0` | per-frame update, draw, on/off, LOD scale, hide/freeze merge | Model-And-Motion-Formats/fcp-character-parameter-block.md:735-750 |
| `00504F00` entry binder | not stated | resolves seven tags into render record `+0x208..+0x220`; stamps `+0xB8`, `+0xB9`, `+0xB3` | Model-And-Motion-Formats/fdm-and-for-entries.md:42-53, 160-166 |
| `CharacterRenderRecord_SelectLODForViewDepth` `004201F0` (648 B) | not stated on page | distance LOD → `+0x2A4` lodFrac, then `00421280(object,1)` | Model-And-Motion-Formats/fdm-and-for-entries.md:96-119, 359 |
| `00504840(entry,key)` | `00420480` at `0042061B` only | keyed `f32[rec+0x18]` → `modelRec+0x26C` | Model-And-Motion-Formats/fdm-and-for-entries.md:121-129, 362 |
| `00504740` | not stated | twin of `00504840` keyed by `s8[obj+0xB8]` | Model-And-Motion-Formats/fdm-and-for-entries.md:160-161 |
| `005048A0(object,key)` | `005210BB` only | key → ordinal or `-1` | Model-And-Motion-Formats/fdm-and-for-entries.md:269-271, 363 |
| `00521050` | handler `00520E70` via `00426870` (one command `0x14` per node) | flag test vs `+0x2F2`, composite key, `00373060(obj, ordinal, w6)` | Model-And-Motion-Formats/fdm-and-for-entries.md:272-285 |
| `00373060` | `00521050` only | writes `w6` into `@FTR` override slot, sets `0x1000` unless `0x7FFF` | Model-And-Motion-Formats/fdm-and-for-entries.md:284-294, 364 |
| `00371330` slot reader | `0053C36F` / `0053C3AD` only | replaces the descriptor's s8 defaults while `0x1000` set | Model-And-Motion-Formats/fdm-and-for-entries.md:295-301 |
| draw builder `0053AB50` / `0053B2xx`, `0053D140`, `0053D4B0`, caller `0053D780` | `0053D780` (fourth list only for class `'h'`) | table A/B texture/palette selection, per-part draw lists, VU1 rows | Model-And-Motion-Formats/fdm-and-for-entries.md:131-194, 299-301 |

#### MF — Inputs and outputs (record layouts)

**SkeletonMapping.bin** (Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:62-71, 96-98): file `i32 count` (`1`), then per record `char[32] name` + `i32 n` + `n × i32`. One record `hc1006_03`, `n = 39`, 196 B (Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:45). Runtime: `count × 0x30` array at `02AD9E30` with name `+0x00`, `n` `+0x20`, pointer to `n×4` values `+0x28` (Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:96-98). Values: 0-19 `-1`, 20-29 `27 28 29 27 28 29 30 27 28 29`, 30 `-1`, 31-38 `33` (Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:153-154).

**HighModelReplace.bin** (Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:73-86, 163-167, 189-198): record `i32 modelId, i32 keyB, i32 keyC` then `(i32 replacement, i32 minProgress)` pairs until `-1`; the stream ends with a further `-1`; source record is `12 + 8N + 4` bytes. 22 records, 540 B (`22×12 + 23×8 + 22×4 + 4 = 540`, Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:265). Runtime 48-byte record: `+0x00 id`, `+0x04 f1`, `+0x08 f2`, `+0x0C extraCount`, `+0x10 extraA[4]`, `+0x20 extraB[4]` (Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:191-198). The id is `(letter << 16) + N` (Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:215, 282).

**.adm** (Model-And-Motion-Formats/adm-add-motion-tables.md:63-94, 452-455): `i16 trackCount`; per track 8 B `{u8 field00, u8 field01, u16 field02, u16 groupCount, u16 recordCount}`; per group a 0x1C header + `recordCount × 0x1C` records. Record = `{i32 bone; f32 eulerDeg[3]; f32 offset[3]}` (Model-And-Motion-Formats/adm-add-motion-tables.md:420). Parsed: 32-byte file record (`+0x00` name, `+0x14` track count, `+0x18` track array), 16-byte track (`+0x00 field02, +0x02 recordCount, +0x04 groupCount, +0x06 field00, +0x07 field01, +0x08 group array`), 0x28-byte group (record array `+0x20`, id `+0x18`) (Model-And-Motion-Formats/adm-add-motion-tables.md:115-117, 452-455, 468). Kind 0: lane `field01` (0/1/2) selects the float at group `+0x00/+0x04/+0x08`, `t = (param − lane[g]) / (lane[g+1] − lane[g])` (Model-And-Motion-Formats/adm-add-motion-tables.md:457-464). Degrees × π/180 → bone record `+0x190/+0x194/+0x198` (Model-And-Motion-Formats/adm-add-motion-tables.md:421-425).

**@FCP** (Model-And-Motion-Formats/fcp-character-parameter-block.md:71-95, 653-658): section header 0x30 (`'@FCP'`, `0`, size, `1`, `char[32]` name); payload header 0x40: `u16 sectionOffset[18]` (`+0x00`), `u32 ftrTailLen` `+0x24`, `+0x2A` per-file value, `+0x2C` six-byte event map, `+0x32` version `0x0A`, `+0x36` special-bone id, `+0x3A/+0x3C/+0x3E` special bones. Section 1: 0x190 B, float slots; `+0x14C` `u16[32]` bone table (Model-And-Motion-Formats/fcp-character-parameter-block.md:115-119). Section 2: `u32[19]` slot offsets, 68-byte anchor `+0x4C`, blob `+0x90`; slot n = rig controller n (Model-And-Motion-Formats/fcp-character-parameter-block.md:678-696). Section 3: 0x3C0 attachment table (Model-And-Motion-Formats/fcp-character-parameter-block.md:576-581). Section 4: `0x10 + n × 0x50`, n ≤ 4 (Model-And-Motion-Formats/fcp-character-parameter-block.md:606-613). Section 6: 16 × 0x10 dead table (Model-And-Motion-Formats/fcp-character-parameter-block.md:700-708). Section 7: pose sequencer (other page). Section 8: `0x10 + n × 0x1D0` (Model-And-Motion-Formats/fcp-character-parameter-block.md:602-603, 722-725, 737-755). Section 9: 0x180 (Model-And-Motion-Formats/fcp-character-parameter-block.md:121-125). Section 10: 48 B, `f32 +8`, `u8 +0x10` read (Model-And-Motion-Formats/fcp-character-parameter-block.md:765-767). Property id `SS VV DD FF` (Model-And-Motion-Formats/fcp-character-parameter-block.md:170-175). Default tables `01F265B0` (float) / `01F266B0` (int) (Model-And-Motion-Formats/fcp-character-parameter-block.md:190). Tunable index table: Model-And-Motion-Formats/fcp-character-parameter-block.md:308-326.

**@FOR** (Model-And-Motion-Formats/fdm-and-for-entries.md:64-94): header `+0x30 u8 recordCount`, `+0x34 tableA_off = 0x40`, `+0x36 tableB_off`, `+0x38 recordBase`, `+0x3A lodThresholdCount`, `+0x3B lodCap`, `+0x3C/+0x3E` u16 cm distances; record 0xE0: `+0x00` key, `+0x02` u8[3] packing kind, `+0x05` u8[3] selector counts, `+0x08/+0x0A/+0x0C` list offsets, `+0x0E` fourth list, `+0x10..+0x16` counts, `+0x18 f32` key value, `+0x20` five 0x20 part sub-records (Model-And-Motion-Formats/fdm-and-for-entries.md:157-158). Table-B index `bIdx = byte[tableA + 3·sel + part] + byte[@FOR+0x32]·variant`; pair = `{texture slot, palette slot}` (Model-And-Motion-Formats/fdm-and-for-entries.md:142-156). List element decode by kind 1/2/3 (Model-And-Motion-Formats/fdm-and-for-entries.md:178-182).

**@FDM** (Model-And-Motion-Formats/fdm-and-for-entries.md:198-211, 224-238): `+0x30 u16 variantCount`, `+0x32 keyTable_off = 0x50`, `+0x34/+0x38/+0x3C` u32 list offsets, keyTable `{u32 count, u32 keys[]}`; descriptor 0x10: `+0x00 u16 = 1`, `+0x02/+0x03 s8` defaults, `+0x04 u32` slot ordinals `A=(bits>>8)&0x3FF`, `B=(bits>>18)&0x3FF`, `+0x08` s8 pair, `+0x0C` u16 offset region → sub-record `{u32 link, u16 boneListOff @+4, u32 @+8}`; bone index × `0x290`. Composite key `((w4 >> 2) << 16) | w2` (Model-And-Motion-Formats/fdm-and-for-entries.md:249-256). Override slot `core + count*0x292 + 2*ordinal` (Model-And-Motion-Formats/fdm-and-for-entries.md:285).

#### MF — State (globals and objects, with lifetime)

| state | lifetime / init | cite |
|---|---|---|
| `02AD9E30` / `02AD9E38` mapping array / count (BSS) | set by `0036FFF0` at boot; initial value not stated | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:147 |
| `02ADD940` / `02ADD938` replacement array / count (BSS) | set by `0037CCC0` | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:148 |
| `01E02800` lookup enable byte | `1` in the image, "no RIP writer" | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:111, 149 |
| pose record `+0x20` name, `+0xB0` mapping index | written by `00372820` | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:107-108 |
| pose record init: `1.0f` at `+0x1AC/+0x1CC/+0x1EC/+0x1E8/+0x1E4/+0x1E0`, `word[+0x280]` | `00373DC0` | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:370 |
| `.adm` registry singleton `0x1F81250` (`+0x20` flag dword) | installer `001BE3E0`, getter `001BE420`; contents beyond `+0x20` not stated | Model-And-Motion-Formats/adm-add-motion-tables.md:431-434 |
| render record `+0x6C8` bind state 0-4; `+0x6E8`/`+0x6F0` handles | `002EDF90` | Model-And-Motion-Formats/adm-add-motion-tables.md:136-146 |
| per-record scratch triplets `rsi+0x708` | lazily allocated in `003714A0` by `0019C580`, cleared by `00861EC0` | Model-And-Motion-Formats/adm-add-motion-tables.md:302-304 |
| `table1`/`table2` (`[r13+0x88] × 4` bytes, filled `0xFF`) | per call in `003714A0` | Model-And-Motion-Formats/adm-add-motion-tables.md:125 |
| override object `001D50D0()` `+0xCF1` flag, `+0xCF4` value | writers not stated | Model-And-Motion-Formats/adm-add-motion-tables.md:316-317 |
| render record `+0x400` FCP payload pointer | `002EDBD0`; 0 when missing | Model-And-Motion-Formats/fcp-character-parameter-block.md:166-167 |
| battle unit `+0x164 … +0x1F5` tunables | `00239E10` at unit activation | Model-And-Motion-Formats/fcp-character-parameter-block.md:202-224, 354 |
| render record `+0x438..+0x444` aux handles | `003E6770`, "runs only while the first handle is still `0xFFFF`" | Model-And-Motion-Formats/fcp-character-parameter-block.md:609-611 |
| `+0x40B` bits 0-1 default attach mode, bits 2-3 used mode | not stated who initialises | Model-And-Motion-Formats/fcp-character-parameter-block.md:588-590 |
| section-8 runtime copy at aux base + record `+0x300`; on-reset `+0`=0, `+0x10`=0, `+0x14`=1.0, `+0x1C4`=1, header `+6`=1, `+7`=0 | `0051DB60` from `003E6710` (promoter passes 1) | Model-And-Motion-Formats/fcp-character-parameter-block.md:734, 745-747 |
| render record `+0x1F8` blob base, `+0x208..+0x220` entry offsets (`-1` = none) | `00504F00` | Model-And-Motion-Formats/fdm-and-for-entries.md:42-58 |
| obj `+0xB8` variant key, `+0xB9` clamped arg, `+0xB3` LOD count | `00504F00` | Model-And-Motion-Formats/fdm-and-for-entries.md:163-166 |
| `+0x2A4` lodFrac, `+0x64` | `004201F0` | Model-And-Motion-Formats/fdm-and-for-entries.md:114-115 |
| `@FTR` override slots | init `0x7FFF`, flag `0x1000` cleared by `00372820` / `00372510` | Model-And-Motion-Formats/fdm-and-for-entries.md:293-294 |

#### MF — Order (what runs when, and what triggers it)

| what | trigger | cite |
|---|---|---|
| bin tables load | boot `0022A0B0`, call sites `0022A43D` (`HighModelReplace`) and `0022A442` (`SkeletonMapping`) — order only by address | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:90-91 |
| `.adm` load | `001BDC40` once; when in start-up not stated | Model-And-Motion-Formats/adm-add-motion-tables.md:104 |
| bind | script verbs (`bindp`, `bindp2`, `bindhoff`) → poll `003409F0` mode 3 → `00342640` → `002E3110` k=4 → state 2 | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:218-219 |
| `.adm` handle bind | secondary-context element binder → `002EDF90` → `00863110` → `001BE430` | Model-And-Motion-Formats/adm-add-motion-tables.md:135-152 |
| between frames | `0041E340` → `0046E0F0` per model record → `00373F40` → `003703A0` | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:510 |
| pose compose | `00373860` → `003714A0`; frame timing not stated | Model-And-Motion-Formats/adm-add-motion-tables.md:128-129 |
| render-record init | `0041FCF0`: section 2 → `@FTR` tail; section 8 copy; section 8 on | Model-And-Motion-Formats/fcp-character-parameter-block.md:630-645, 719-721, 745 |
| unit activation | `00233AD0` → `00239E10` | Model-And-Motion-Formats/fcp-character-parameter-block.md:202 |
| section 8 per frame | update `0051D310` from `00425E10` in `RenderSystem_RunCharacterUpdatePipeline` `003323D0`; draw `0051CDE0` from `00425DC0` (after-emission stage of `00332440`) | Model-And-Motion-Formats/fcp-character-parameter-block.md:736-741 |
| command `0x14` | `00520E70` → `00426870` (hierarchy broadcast) → `00521050` → `00373060` | Model-And-Motion-Formats/fdm-and-for-entries.md:273-285 |
| attach | dirty-bit-19 `004215A0`, `00424D80`; command `0x15` (`active` mode 1, `deact` mode 0) via `00429760` | Model-And-Motion-Formats/fcp-character-parameter-block.md:574, 590-593 |
| LOD select | `004201F0`; caller and timing not stated on this page | Model-And-Motion-Formats/fdm-and-for-entries.md:96-119 |

#### MF — Dependencies

Resource layer (`001D6F20` file open, `00409660`, `00409A30`, `002ED570`; Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:91, Model-And-Motion-Formats/fcp-character-parameter-block.md:163-165, Model-And-Motion-Formats/fdm-and-for-entries.md:43); WorldAreaField / FieldData (`FieldData_GetVariable0` `00265270`, `FieldData_GetActiveFieldRecordBit15` `00377C20`; Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:114, Model-And-Motion-Formats/adm-add-motion-tables.md:300, Model-And-Motion-Formats/fcp-character-parameter-block.md:237); Script VM bind verbs (Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:218-219, 328-331); party read-in state machine (Model-And-Motion-Formats/adm-add-motion-tables.md:150-152); battle unit field map (Model-And-Motion-Formats/fcp-character-parameter-block.md:261, 410); Movement (`0026B2E0`, `002E28E0`; Model-And-Motion-Formats/fcp-character-parameter-block.md:404, Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:321-326); rig of seventeen controllers (Model-And-Motion-Formats/fcp-character-parameter-block.md:377); bone trails (Model-And-Motion-Formats/fcp-character-parameter-block.md:615); authored-command handlers `0x14`/`0x15`/`0x16` (Model-And-Motion-Formats/fdm-and-for-entries.md:277, Model-And-Motion-Formats/fcp-character-parameter-block.md:593, 668); `@FTR` node table (Model-And-Motion-Formats/fdm-and-for-entries.md:49, 285); `@FTE`/`@FCT` (Model-And-Motion-Formats/fdm-and-for-entries.md:150-156); pose sequencer (Model-And-Motion-Formats/adm-add-motion-tables.md:130-131); VU1 microcode, not read (Model-And-Motion-Formats/fdm-and-for-entries.md:302-303).

### 1.10 [MM] Motion formats: FEF/motion entries, FRP, FTE/FCT, FTR, oscillator, pose sequencer

Short names in this part: **ACH** = `Authored-Commands/the-authored-presentation-command-handlers.md`.


#### MM — Entry points

| entry (size) | callers as stated | what it does | cite |
|---|---|---|---|
| `FRP_FindEntry` `00408FA0` | via zero-start thunk `00408F90`, "whose four callers all pass no name and the tag @FRM" | magic/variant/bounds-checked linear scan of the offset table from `startIndex`; returns index or −1 | Model-And-Motion-Formats/frp-object-container.md:95-113, :319-324 |
| `NameEquals` `00408F30` | `FRP_FindEntry` | 8-dword compare of blob `+0x10` vs caller string; 0 = match, 1 = differ | Model-And-Motion-Formats/frp-object-container.md:136-140, :319-322 |
| `004090D0` | `00408F80` (index), `00409780`/`00409A30` (tag+name) | `.ca` v1 slot selector: slot = `80*group + cmdSlot` | Model-And-Motion-Formats/fef-and-motion-entries.md:97-106; Model-And-Motion-Formats/frp-object-container.md:170 |
| `00504F00` (binder) | render-record bind | stores 7 entry offsets at render record `+0x208..+0x220`; `+0xB8`/`+0xB9` selectors; calls `00504940` at `00505026` | Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:37-39, :286, :170-172; Model-And-Motion-Formats/fef-and-motion-entries.md:142 |
| `00504940` | `00504F00` | `@FEF` sub-record bind; passes `@FEF+0x30` to stub `0016D6A0` (`ret 0`) | Model-And-Motion-Formats/fef-and-motion-entries.md:142-151 |
| `0041E580` (12 B thunk) → `00409FE0` | load-completion callbacks `002E4DB4`, `002E4EFA`, `003DC371`, `003DD8AB` | instances the appended companion `chara\hNNNN.efx` (type-3 effect, `003B38B0`→`003EDAD0`), handle → `obj+0x44` | Model-And-Motion-Formats/fef-and-motion-entries.md:167-221, :744-753 |
| `0040A230` (via `00409F80`) | start-up chain `0017D000`→…→`0041E3A0` | seeds 144 `obj_finish` path rows of `02B64380` | Model-And-Motion-Formats/fef-and-motion-entries.md:192-203, :957 |
| `0041D220` / `0041D2C5`-`0041D374` | admission `0051BA80` (from `00424550`, `00424D80`) | presentation-entry init: `+0x31C`/`+0x31A`, `@FMC`→`+0x320`, `@FRM`→`+0x378`/`+0x37C` | Model-And-Motion-Formats/fef-and-motion-entries.md:109-120, :448-451, :709-714 |
| `0041BEE0` / `0041B4E0` | not stated | motion-descriptor init / resolution of `@FMN` (`desc+0x54`,`+0x70`) and `@FMW` (`desc+0x58`,`+0x78`) | Model-And-Motion-Formats/fef-and-motion-entries.md:474-482, :562-564 |
| `0041CD30` | not stated | scans `@FMC` records, finds `0xFFFF` sub-record → `state+0x90`, cursor init `+0x88/+0x8C`, stamps record index | Model-And-Motion-Formats/fef-and-motion-entries.md:280-283, :730-731 |
| `0041E000` executor | per-tick `0041DBD2`; flush `0041DBB8`/`0041DC47`/`0041DCC6` (r8d=−1); catch-up `0041C8FF` | fires sub-records with `key ≤ threshold` via table `01EFFAF0` (76 × 0x10) | Model-And-Motion-Formats/fef-and-motion-entries.md:251-258, :284-290 |
| `0041C040`-`0041C1D9` → `0041B550` → `0041B650` | descriptor init | `@FMN` tail walker; per-node 9 channel slots init from `@FMW` | Model-And-Motion-Formats/fef-and-motion-entries.md:484-501, :631-645 |
| `0041A470` sampler; driver `004193xx`-`0041A46B` (named `00418880` in ftr) | per frame | key-cursor advance + linear sample; writes node staging `+0x190/+0x1B0/+0x1D0` | Model-And-Motion-Formats/fef-and-motion-entries.md:647-673; Model-And-Motion-Formats/ftr-node-table.md:265 |
| `0041BDC0` | not stated | re-seek twin | Model-And-Motion-Formats/fef-and-motion-entries.md:652-654 |
| `00423B10` | event map via FCP `+0x2FA` | motion starter; hands `@FRM` `+0x37C` region to request `+0xE8`/`+0x100` | Model-And-Motion-Formats/fef-and-motion-entries.md:451-461, :718-722 |
| `003AF460` / `003AFB30` | `00426117` per frame / `@FMC` seek paths `0041C8F1`, `0041D9D1` | op-0x34 shadow-param ramps | Model-And-Motion-Formats/fef-and-motion-entries.md:383-390 |
| `004256E0` (via `00422400`/`00422410`) | op 0x0B selector kinds 0/0xA/0xB | locomotion band classifier | Model-And-Motion-Formats/fef-and-motion-entries.md:392-418, :728-742 |
| `00504D30(record, idx, sub, out)` | `003E7210` (from `00427FF7`, `0042B566`) | `@FCT` palette bind, `(idx,sub)` dedup | Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:120-130, :259-263 |
| `005044D0` / setter `00504D20` (7 B) | `00428CD0` (record mode) | `@FCT` page select by `s8[rec+0xBA]` | Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:136-146, :245-257 |
| `0053AB50` (~0x1E00 B) | twice from `0053D780` | combined `@FOR`/`@FTE`/`@FCT`/`@FDM` draw builder | Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:154-179 |
| `005210F0` / `00504520` | `0053AB50` | 256-slot texture cache lookup / slot fill | Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:229-234 |
| `003712E0` sizer, `00372820` binder, `003713C0` | model load | `@FTR` expansion to 0x290 bone records + FCP section-2 tail copy, `003E1C50` address pass | Model-And-Motion-Formats/ftr-node-table.md:108-144, :298-300 |
| `00409300` / `004094D0` / `00373DC0` | `00372820` | bone field copiers / identity init | Model-And-Motion-Formats/ftr-node-table.md:82-92, :237-245 |
| `00373860` + `00372610` | `003705BA` | final-pose composer | Model-And-Motion-Formats/fef-and-motion-entries.md:675-683; Model-And-Motion-Formats/ftr-node-table.md:263-264 |
| `003703A0` (`Skeleton_UpdateFinalPoseAndCombatLook`) | `004242B0`, `0046E0F0` | calls `003DFFE0` at `003705F9`; skinning palette | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:38-43, :453 |
| `003DFFE0` (224 B) | `003703A0` | oscillator gate; tail-jumps `0040ACF0(obj, dx, r8, r9)` or `0040ED80` | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:45-59 |
| `0040ACF0` / `0040D890` / `0040F390` | `003DFFE0` | per-frame driver / sub-stepped twin / reset to rest | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:100-138, :298-311 |
| `0040DBB0` / `0040B780` | `0040ACF0`, `0040D890` | direct / blend node apply via VU0 bank | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:140-149, :427-428 |
| `0054B1F0` | `0052B5E0`, `0052BBD0` (effect element type 0x72) | oscillator parameter install | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:162-179, :288-296 |
| `0040AAD0` / `0040B3B0` / `0040DB70` | `002E3D40` (verbs 0x481/0x482, field init), `002EAB40`/`002EAA60`; `0040DB70` from `004269A0` via `003E0720` | map-wind globals | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:240-267 |
| `0040ABF0` (241 B) | callback `00520E90` of op 0x3F | per-record sway preset/direction | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:510-529 |
| `003E00C0` (1,631 B) | rig frame | slot-table walk; controller 0 via `0040B180` | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:209-238 |
| `003E6F50` / `003E7450` / `003E6A20` | `003E7450`: op 0x1D `00520D30`, `0041DF83`, `0051E47B`; `003E6A20`: op 0x1E `00520DF0` | section-7 accessor / start event / reset slot | Model-And-Motion-Formats/the-pose-sequencer.md:40-42, :138-148 |
| `00477370` start / `00477480` step / `004776D0` value / `00477670` reset | step: "the root record's animation-presentation phase"; value: `AddMotion_ApplyBonePose` window `00371F2E..00371FD4` | pose sequencer | Model-And-Motion-Formats/the-pose-sequencer.md:85-100, :104-108 |
| `00477750` / `00477B10` | model-instance draw | slot count ×128 / texture-patch copy | Model-And-Motion-Formats/the-pose-sequencer.md:112-131 |
| `004772E0` allocator | `0041FCF0` at `0041FEAC` | phase-entry alloc, variant = n−1 | Model-And-Motion-Formats/the-pose-sequencer.md:59-63 |

#### MM — Inputs and outputs (record layouts)

**@FRP container** (Model-And-Motion-Formats/frp-object-container.md:66-81, :319-320): `+0x00 '@FRP'`; `+0x04` variant 0/1 (else −1); `+0x08` contentLength (unread by finder, :119); `+0x0C` entryCount; `+0x10` name (32-byte compare, :319-320); `+0x20..+0x2C` zero; offset table `u32[entryCount]` at `+0x30` (v0) / `+0x40` (v1), offsets relative to the table base. v1 `.ca`: `dword[+0x30]` = FMC-band stride 80, `dword[+0x34]` = group count (Model-And-Motion-Formats/fef-and-motion-entries.md:99-106). Entry header common shape: tag, word +4, length +8, word +0xC, 32-byte name +0x10 (Model-And-Motion-Formats/frp-object-container.md:348-353).

**@FEF** (Model-And-Motion-Formats/fef-and-motion-entries.md:127-132): `+0x00 '@FEF'`, kind 0, entryLen, `+0x0C`=1; `+0x10 char[0x20]` name; `+0x30` embedded `EFX0010` (dead). Live payload = companion at `dword[r14 + roundup64(size) − 4]` (:209-214, :747-749); `02B64380` row index fold: first char ×1,280, Horner ×10, bias −0x1A0A (:185-189).

**@FMC** (Model-And-Motion-Formats/fef-and-motion-entries.md:238-250): header `{'@FMC', kind 1, entryLen, +0x0C = event record count}`, name +0x10, records from +0x30: `{u8 kind, u8 0, u8 0, u8 subCount, u16 byteLen}`; sub-record `{u16 key, u16 {cmdCount:6, byteLen:10}}`; command `{u16 {opcode:7, byteLen:9}}` + operands. Key = frame index; `0xFFFF` = sub-record #0 run every tick (:269-285). Opcode table with lengths (:310-348).

**@FMN** (Model-And-Motion-Formats/fef-and-motion-entries.md:465-556): kind `0x02001111`, `+0x0C` record count, names +0x10/+0x30, `+0x50` word duration, `+0x54` post-block offset (dead), `+0x60..+0x6F` clamp pairs, `+0x70` vec2, `+0xA0/+0xA4/+0xA8`, `+0xEE`; tail at `+0xF0` (via `00409190`, :990): 22-byte records `{u16 nodeKey, u16 {chMask:9, byteLen:6, flag:1}, u16 chIdx[9]}`.

**@FMW** (Model-And-Motion-Formats/fef-and-motion-entries.md:560-629): `+0x30` track base, `+0x34` arm (1 packed / 0 run tables), `+0x40` channel offset table (u16 arm 1 / u32 arm 0); arm-1 descriptor `{u8 frameCount, u8 cnt, u16, u32[cnt], {u32 litOff|flags, f32 bias, f32 scale}…}`; flag codec `0x80` s16 LE / `0x40` repeat / else s8; arm-0 head `{frameCount(bit31 ext), nA, nB[, nC + nC×0x1C]}`, A 8 B, B 16 B records. Runtime channel slot 0x1C B (:638-643); node row stride 0x108 (:656). Channels 0-2 Euler XYZ radians, 3-5 translation, 6-8 scale (:662-666).

**@FRM** (Model-And-Motion-Formats/fef-and-motion-entries.md:703-722): header `{'@FRM', 0, entryLen, 1}`, name; `+0x30` u32 offset list; bound to entry `+0x378`/`+0x37C`; payload "handed to the request, not parsed here".

**@FTE** (Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:43-74): `+0x30 u8 count + u8[]`; records 0x20 at `+0x40`: `+0x00` VRAM bytes, `+0x04/+0x06` w/h, `+0x08` PSM (0x13/0x14), `+0x0A/+0x0C` RRW/RRH, `+0x0E` DPSM 0, `+0x10` 0, `+0x14` upload bytes = RRW·RRH·4, `+0x18` payload off, `+0x1C` cache key.

**@FCT** (Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:92-109): records 0x10 at `+0x30`: `+0x00` vramBytes 0x2000, `+0x02` clutBytes, `+0x04` RRW, `+0x05` pageCount 4, `+0x06` RRH, `+0x08` id (unread), `+0x0C` payloadOff; page = `entry + payloadOff + s8[rec+0xBA]·clutBytes` (:139-140).

**@FTR** (Model-And-Motion-Formats/ftr-node-table.md:51-80): kind 2, `+0x0C` count, `+0x30` count2, `+0x34` auxOff, `+0x38` tailU16, `+0x40` index `(recOff<<12)|ordinal`; records at `align16(0x40+4·count)`: `+0x00` link (bits 12-23 parent, 0-11 key), `+0x04` flags, `+0x08` u16 index stream; length rule `8 + 2 × (b30 + b31 + 16·b21 + b22 + b23 + … + b29)` padded to 4 (:209-210). Runtime: core `count·0x292 + tailU16·2`, render record `+0x80/+0x84/+0x88/+0x8A/+0x90/+0x94/+0xB0` (:111-127).

**Oscillator** (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:72-98, :387-397): record `+0x00` → entry array, `+0x04` count, `+0x05` parent flag, `+0x08` (rig slot +0x78), `+0x0C` parent id, `+0x10` f32 → VU row 31, `+0x1C`, `+0x20/+0x24/+0x28` global pair, `+0x2C` param block, `+0x30/+0x34/+0x38` per-record pair, `+0x3C` bone, `+0x3E` enable/preset, `+0x3F` flags, `+0x40` direction, `+0x50` perpendicular (:524-529), `+0x5C` render record. Entry 0x30 (A/C/D/F/G/H/I lists).

**FCP section 7 / pose sequencer** (Model-And-Motion-Formats/the-pose-sequencer.md:44-56): 8 event offsets; 6-byte event records `{slot, pickParam, u16 rel, enabled, pad}`; choice table T; sequence `{u16 frameCount, {u16 dur, u8 endAction, u8 value}…}`; R rectangle table (:120-128). Phase entries 32 × 0x40 at `02CA6CA0`; slot arrays `+0x10..+0x38` (:69-81).

#### MM — State (globals and objects, with lifetime)

| state | lifetime / init | cite |
|---|---|---|
| `02B64380` path-row table (`.data` virtual tail, zero-filled) | seeded at start-up by `0040A230` | Model-And-Motion-Formats/fef-and-motion-entries.md:190-200 |
| `02CA4410` hook tabA / `02CA4670` tabB | `0041CCA0` zero-fills at init; `0041D6C0`/`0041D6D0` install; registrations `00426A0D`-`00426B84`, `002EA4xx` | Model-And-Motion-Formats/fef-and-motion-entries.md:295-301 |
| `02CA4668` selector table ptr (`01F000A0`) | installed via `0041D6E0` | Model-And-Motion-Formats/fef-and-motion-entries.md:321 |
| 0x740 selector state records (`0xA0` pooled at `[02B3EF28]`) | `004269A0`→`0041F730` memset, `+0x40F=0xFFFF`, −1 fills; reset at `004252A7` | Model-And-Motion-Formats/fef-and-motion-entries.md:428-446 |
| shadow-param pool `02B3F570` (32 × 0x70) | `003AFCD0` pool-init; alloc `003AF340`, defaults listed | Model-And-Motion-Formats/fef-and-motion-entries.md:365-390 |
| `02B40528` 0xE0-stride param rows | written by ops 0x0D-0x10 / `003B5CE0`; init not stated | Model-And-Motion-Formats/fef-and-motion-entries.md:355-356, :986 |
| texture cache 256 slots (`00521290`/`005210F0`) | shared by key; last binder's descriptor; init not stated | Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:71, :229-234 |
| render record `+0x140` (16), `+0x180` (20-byte map), `+0x194` (20 handles), `+0x100` (0x20 u16) | teardown `00504C40`; init not stated ("`0xFF` free slot") | Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:122-130 |
| 0x290 bone records | built by `00372820`/`00373DC0`; scale vec4s set 1.0 | Model-And-Motion-Formats/ftr-node-table.md:237-245 |
| skinning palette `renderRecord+0x6C0` | lazily `0019C580(0x12,0,count*0x40)` | Model-And-Motion-Formats/fef-and-motion-entries.md:684-690 |
| map-wind globals `02CA4380`-`02CA439C`, `02CA43A0` | `0040DB70` clears at `004269A0`; set by `0040B3B0`/`0040AAD0` | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:240-253 |
| `02B59D60` | never written, zero | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:277-281 |
| `02B59D68` display-deny latch | writer `003E0B40` | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:283-286 |
| oscillator record | authored in FCP section 2 (rig slot 0), relocated by `0040EEA0`; `+0x08/+0x0C/+0x5C` set by `003E1C50`; reset `0040F390`; rig `+0x60` = 30 at rebind | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:381-397, :61-65 |
| phase entries `02CA6CA0` (32 × 0x40) | `004772E0` alloc (variant n−1); table reset `004778A0`; initial slot values not stated | Model-And-Motion-Formats/the-pose-sequencer.md:59-72, :206-207 |
| `02CA6C98` global freeze | not stated who writes | Model-And-Motion-Formats/the-pose-sequencer.md:92-93 |

#### MM — Order (what runs when, and what triggers it)

| when | what | cite |
|---|---|---|
| start-up | `0041E3A0` → `00409F80` → `0040A230` seeds `02B64380` | Model-And-Motion-Formats/fef-and-motion-entries.md:197-200 |
| model load | `00372820` builds bones, appends FCP section 2, `003E1C50`; `00504F00` binds entries | Model-And-Motion-Formats/ftr-node-table.md:139-144 |
| load completion | `0041E580` → `00409FE0` instances `@FEF` companion | Model-And-Motion-Formats/fef-and-motion-entries.md:750-751 |
| per tick, motion | `0xFFFF` block via `0041DAD3` every tick; keyed run `0041E000` with `threshold = cvttss2si(f32[state+0xC])` (`0041DBD2`); flush at end position; catch-up `0041C8FF` | Model-And-Motion-Formats/fef-and-motion-entries.md:271-290 |
| per frame | `003AF460` shadow ramps from `00426117` | Model-And-Motion-Formats/fef-and-motion-entries.md:383-384 |
| final pose | `003703A0` → `003DFFE0` (after motion, before draw) → `0040ACF0` | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:38-43 |
| rig frame | `003E00C0`: controller 0 first (`0040B180`), then slot table order | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:235-238 |
| sim-step frames | `00477480` step (word +0 ≠0, word +2 = 0, `02CA6C98` = 0) | Model-And-Motion-Formats/the-pose-sequencer.md:91-98 |
| draw | `00477750` count, then `00477B10` copy | Model-And-Motion-Formats/the-pose-sequencer.md:112-120 |

#### MM — Dependencies

EFX containers / effect instance pool (Model-And-Motion-Formats/fef-and-motion-entries.md:135-138, :215-218); AsyncLoadManager `01F81160` (:744-746); authored-command handlers page, ramp-channel contract, fade channels (:303-308); FCP page (`+0x2FA`, section 2 rig, section 7) (Model-And-Motion-Formats/fef-and-motion-entries.md:451-454; Model-And-Motion-Formats/ftr-node-table.md:177-181; Model-And-Motion-Formats/the-pose-sequencer.md:33); fdm/for page (Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:166-173, :193-197); status looks (`00428CD0`) (Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:245-249); rig of seventeen controllers (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:61-63); VU0 register bank (:369); weather/field record and script verbs (:255-267); effect element type 0x72 (:288-296); add-motion tables (Model-And-Motion-Formats/the-pose-sequencer.md:30, :104-110); time-stop registry (:93-95); half-rate gate `001EDE70`/`001EDE80` (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:105; Model-And-Motion-Formats/the-pose-sequencer.md:272).

### 1.11 [PP] Post-processing and visual tuning parameters

Short names in this part: **CS** = `Post-Processing/CONTRACT-post-processing-subsystem.md`; **CP** = `Post-Processing/CONTRACT-ppfx-effect-creation.md`; **PI** = `Post-Processing/ppfx-function-identification.md`; **CAT** = `Post-Processing/the-post-processing-effect-catalogue.md`; **VR** = `Visual-Tuning-Parameters/README.md`; **RR** = `Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md`; **RCL** = `Render-Command-List/the-ordered-render-command-list.md`; **HL** = `Post-Processing/members/ppfx-handle-layout.tsv`.


#### PP — Entry points

| entry | callers as stated | what it does | cite |
|---|---|---|---|
| `00193DA0` (post-process frame callback) | enqueued by `PostProcessObj::Execute` (`001F3300`) when `01DFE0C4` on; call via `0018EEE0` | per-frame configure-then-run of the PPFX library | Post-Processing/CONTRACT-post-processing-subsystem.md:63, Post-Processing/CONTRACT-post-processing-subsystem.md:80; Post-Processing/the-post-processing-effect-catalogue.md:814, Post-Processing/the-post-processing-effect-catalogue.md:925-928; Render-Command-List/the-ordered-render-command-list.md:237 |
| `0065E5A0` (8 B thunk) → `006CBD20` (376 B) | sole caller `00193DE8` | lazy create: licence registration, default param block, `006DAA70(…,3,5,…,0x20001)` | Post-Processing/CONTRACT-post-processing-subsystem.md:63-74; Render-Command-List/the-ordered-render-command-list.md:1720 |
| `006DAA70` `IPfxBaseContext::Initialize` | sole caller `006CBE0A` | forwards 5th arg to `Initialize` (`006DAD0A`) | Post-Processing/CONTRACT-post-processing-subsystem.md:64; Post-Processing/the-post-processing-effect-catalogue.md:1019-1020; Post-Processing/ppfx-function-identification.md:589 |
| `006FF900` `CPostEffect::Initialize` | `006DAA70`; dead `006DE950` | stores flags at `+0x20C` (`006FFB8C`), derives feature bytes | Post-Processing/CONTRACT-post-processing-subsystem.md:65, Post-Processing/CONTRACT-post-processing-subsystem.md:181-182; Post-Processing/the-post-processing-effect-catalogue.md:995, Post-Processing/the-post-processing-effect-catalogue.md:1001-1010 |
| `0065E6C0` → `006CC2F0` | `00193DA0` when `cfg+0x99` set | two virtual calls (slot 1, slot 0) on library object; unnamed | Post-Processing/CONTRACT-post-processing-subsystem.md:82; Post-Processing/the-post-processing-effect-catalogue.md:937 |
| `0065E6A0` → `006CC1F0` (107 B) | `00193DA0` | step 3, `&cfg+0x9C` block commit | Post-Processing/CONTRACT-post-processing-subsystem.md:85; Post-Processing/the-post-processing-effect-catalogue.md:940; Render-Command-List/the-ordered-render-command-list.md:1652-1659 (see PP.CV-3) |
| `0065E6B0` → `006CC260` (133 B) | `00193DA0` | step 4, vec3 `cfg+0xDC/+0xE0/+0xE4`, last ×0.5 | Post-Processing/CONTRACT-post-processing-subsystem.md:86; Post-Processing/the-post-processing-effect-catalogue.md:941 |
| `0065E670` → `006CC1E0` → `006DB9A0` → `00707560` `SetGlareParameters` | `00193DA0` | step 5 glare | Post-Processing/CONTRACT-post-processing-subsystem.md:87-93; Post-Processing/the-post-processing-effect-catalogue.md:942-943 |
| `0065E630` → `006CBD00` → `006CC170` | `00193DA0` | step 6; then `006DC820(32.0, -FLT_MAX)` | Post-Processing/CONTRACT-post-processing-subsystem.md:100-101; Post-Processing/the-post-processing-effect-catalogue.md:944 |
| `0065E610` → `006CC090` | `00193DA0` | step 7 DOF lens setter (`006DBC20`, `006DC700`, `006DC650`) | Post-Processing/CONTRACT-post-processing-subsystem.md:102-104; Post-Processing/the-post-processing-effect-catalogue.md:945-946, Post-Processing/the-post-processing-effect-catalogue.md:958-965 |
| `0065E5C0` → `006CBEA0` → `006DB660` → `0070BA00` `ApplyEffects` | each single caller (`00193F58`, `0065E5C3`, `006CC031`, `006DB667`) | step 8, the run | Post-Processing/CONTRACT-post-processing-subsystem.md:105-107, Post-Processing/CONTRACT-post-processing-subsystem.md:175-178, Post-Processing/CONTRACT-post-processing-subsystem.md:323 |
| `0065E5D0` (64 B) | `0018E470`, `006253D0` | lazily builds 0x10-byte wrapper at `[02D38540]` (alloc via `00210EC0`, ctor `0065E530`) | Post-Processing/CONTRACT-post-processing-subsystem.md:56, Post-Processing/CONTRACT-post-processing-subsystem.md:290-292; Render-Command-List/the-ordered-render-command-list.md:1390-1393 |
| `0065E5B0` (11 B) | `00193DA0` | "is it created?" `[[rcx]] != 0` | Post-Processing/CONTRACT-post-processing-subsystem.md:56; Post-Processing/the-post-processing-effect-catalogue.md:814 |
| `0072D820` (396 B) `TEXSHADERSET::InitializeDevice` | slot-0 method (4,903 B) of `PPFX::CTextureUtil` vtable `00DA5DA8`, called from the 23,568-byte library create routine | logs, calls `0072A320`, tests result `0072D879`, then `call [rax+0x38]` `0072D8D9` | Post-Processing/CONTRACT-ppfx-effect-creation.md:55-58; Post-Processing/the-post-processing-effect-catalogue.md:807-814; Post-Processing/ppfx-function-identification.md:597 |
| `0072A320` (13,547 B, 2,965 insns) `TEXSHADERSET::CreateEffect` | only `0072D872` | loads effect via `0078A120` once; registers 325 techniques / 36 uniforms | Post-Processing/CONTRACT-ppfx-effect-creation.md:54-57; Post-Processing/the-post-processing-effect-catalogue.md:170 |
| `0078A120` (273 B) | `0072A320` at `0072A3D1` | `IGPUEffect::CreateEffectFromFile` wrapper (or `IGPUEffect::CreateEffect`, PP.CV-9) | Post-Processing/the-post-processing-effect-catalogue.md:172; Post-Processing/CONTRACT-ppfx-effect-creation.md:281; Post-Processing/ppfx-function-identification.md:578 |
| `0072DCF0` (718 B), `0072EB20` (215 B), `0072DFD0` (716 B), `0072DAC0`, `0072E5B0`, `0072E940`, `0072EC00` | `0072A320` | family registration wrappers | Post-Processing/CONTRACT-ppfx-effect-creation.md:101-105, Post-Processing/CONTRACT-ppfx-effect-creation.md:159-160; Post-Processing/the-post-processing-effect-catalogue.md:806 |
| JSON setters `00194310` / `00194250` | cutscene loader `001C3D50` (`001C42A6`–`001C42E4`, `001C4179`–`001C42A1`), map loader | write render-parameter block `+0xF4/+0xF8`, `+0x110..+0x120` | Post-Processing/CONTRACT-post-processing-subsystem.md:124-129; Render-Command-List/the-ordered-render-command-list.md:790-794 |
| `0018EEE0` | `PostProcessObj::Execute` | allocates 0xF0 `cfg` via `001A1470([01F7F4C0])`, fills it, `005FEA50` enqueues kind-0x2F command | Post-Processing/CONTRACT-post-processing-subsystem.md:263-265, Post-Processing/CONTRACT-post-processing-subsystem.md:303-309 |
| `001C7940` (11,445 B) / `001CA600` (8,186 B) / `001C3D50` (4,607 B) + 14 smaller | via `001FF740` member lookup | JSON readers (maps / UISize / cutscenes) | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:345, Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:632-648 |
| `001C76E0` (357 B) | `001C5F20` path (`001C61CD`) | `mClutIndex` handler → font clut entry | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:381-390 |
| `001A9B00` (34 B) | `001C7940` loop `001C91F8` | stores cascade matrix element | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:716-717 |
| `001EF2D0` | not stated | writes cascade defaults 0.008/0.016/0.035 at another object's `+0x870/+0x874/+0x878` | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:741-743 |
| `0059E070` (656 B) Vignette, `00656B20`, `00655180`, `00656F20`, `00648100`/`006561D0`, `006C0540`/`0580`/`05F0` | not stated | Phyre PostProcessing parameter classes; bodies declared unread (W-7) | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:240-252 |
| `00658470` atmosphere selector (+`006587F0`, `00659A90`, `0065A640`, `00659C20`) | `0065B270` (vtable method) | pick plain / Inverted / RenderTextures pass by target `+0xC` bit 1 | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:360, Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:370-372 |

#### PP — Inputs and outputs (record layouts)

`cfg` (post-process command param block, `[ctx+0x10]`, 0xF0 bytes per Post-Processing/CONTRACT-post-processing-subsystem.md:263-264):

| off | size | meaning | cite |
|---|---|---|---|
| +0x00 / +0x08 / +0x10 | 8 each | colour source, depth source, output target → `006CBEA0` | Post-Processing/CONTRACT-post-processing-subsystem.md:105-106; Post-Processing/the-post-processing-effect-catalogue.md:947 |
| +0x18 | 4 f | `mGlareLuminance` (from block +0xF4) → library +0x6E4 | Post-Processing/CONTRACT-post-processing-subsystem.md:98-99, Post-Processing/CONTRACT-post-processing-subsystem.md:141 |
| +0x1C | 4 f | `mGlareThreshold` (block +0xF8) → library +0x6E0 | Post-Processing/CONTRACT-post-processing-subsystem.md:99, Post-Processing/CONTRACT-post-processing-subsystem.md:142 |
| +0x20 | 1 | DOF enable (block +0x110, `EnableDof`) | Post-Processing/CONTRACT-post-processing-subsystem.md:143; Post-Processing/the-post-processing-effect-catalogue.md:945 |
| +0x21 | 1 | alternative-focus byte → `0.1…100.0` pair via `006DC700` | Post-Processing/the-post-processing-effect-catalogue.md:945, Post-Processing/the-post-processing-effect-catalogue.md:961-962 |
| +0x24 / +0x28 | 4 f each | `mDofFocusDistance` / `mDofApertureFnumber` (block +0x114/+0x118); replaced by "a computed pair" when caller's `+0x124` is 1 | Post-Processing/CONTRACT-post-processing-subsystem.md:144 |
| +0x2C | 4 f | block +0x120, `35.0` (but see PP.CV-1) | Post-Processing/CONTRACT-post-processing-subsystem.md:145 |
| +0x30 / +0x34 | 4 f each | passed by step 7 when on; source not stated | Post-Processing/the-post-processing-effect-catalogue.md:945 |
| +0x94 | 4 f | from block byte +0xEE, permanently 0.0f | Render-Command-List/the-ordered-render-command-list.md:1247-1258 |
| +0x98 | 1 | step 6: set → 2.0, mode 2 | Post-Processing/CONTRACT-post-processing-subsystem.md:100; Post-Processing/the-post-processing-effect-catalogue.md:944 |
| +0x99 | 1 | selects reset arm (step 1) | Post-Processing/CONTRACT-post-processing-subsystem.md:82; Post-Processing/the-post-processing-effect-catalogue.md:937 |
| +0x9A | 1 | step 6 mode 1 vs -1 | Post-Processing/the-post-processing-effect-catalogue.md:944 |
| +0x9C | 0x20 or 0x40 (PP.CV-3) | step 3 block | Post-Processing/the-post-processing-effect-catalogue.md:940; Render-Command-List/the-ordered-render-command-list.md:1652-1659 |
| +0xDC/+0xE0/+0xE4 | 4 f each | step 4 vec3, last halved | Post-Processing/the-post-processing-effect-catalogue.md:941 |

Render-parameter block (`PostProcessParamContext`, 0x4A8, `[01F7F5F0]` = `[01F81300]`, alloc `00193D50`): +0xF4/+0xF8 glare (setter `00194310`), +0x110 enable byte, +0x114 focus, +0x118 f-number, +0x11C preserved, +0x120 35.0 (setter `00194250`), +0x330 `mMotionBlurEnabled` (setter `001944C0`, ctor 1, no reader), +0x1E8 HBAO Full Res byte (console id 45). Post-Processing/CONTRACT-post-processing-subsystem.md:122-129, Post-Processing/CONTRACT-post-processing-subsystem.md:133-134, Post-Processing/CONTRACT-post-processing-subsystem.md:250-254; Post-Processing/CONTRACT-ppfx-effect-creation.md:67; Render-Command-List/the-ordered-render-command-list.md:797, Render-Command-List/the-ordered-render-command-list.md:831-832.

Library object (`CPostEffect`, `[02EA0B70]`): +0x108 (ctor 0 `006FF68E`, written only `007009BB`), +0x131…+0x146 feature "initialised" bytes, +0x147 (set only `00700083` iff flags & 0x800), +0x20C flags, +0x6E0/+0x6E4 glare floats, +0xC6C flag 1, +0xC70 remap factor (≥0.001). Post-Processing/CONTRACT-post-processing-subsystem.md:57, Post-Processing/CONTRACT-post-processing-subsystem.md:90-93, Post-Processing/CONTRACT-post-processing-subsystem.md:221-224; Post-Processing/the-post-processing-effect-catalogue.md:1006-1010.

Flag word → features (Post-Processing/the-post-processing-effect-catalogue.md:1006-1010): 0x40000 → +0x131..+0x134 (+0x135 with 0x200000), +0x137, +0x138, +0x13C(→+0x13D), +0x142 (lens distortion, Airy disc, motion blur, geometry blur, Gaussian, heat shimmer, CA); 0x4000000 → +0x13A/+0x13B (AO); 0x8000000 → +0x140/+0x141 (PP AA + falloff); 0x8000 → +0x143 (unnamed); 0x400 → +0x144/+0x146 (unnamed). Build constant `0x20001` (Post-Processing/CONTRACT-post-processing-subsystem.md:73).

TEXSHADERSET / handle receiver: 32-bit handles at byte offsets from `this+8` (`0072A496`) and `this+0x1AA10` (`0072BA97`); slots +0xA0..+0x221D8; family destination = `count` dwords from listed offset; object ≥0x221DC, allocation 0x22360 (CTextureUtil). Post-Processing/the-post-processing-effect-catalogue.md:803, Post-Processing/the-post-processing-effect-catalogue.md:814; HL. Twelve unrolled arrays (base/terms/stride) Post-Processing/ppfx-function-identification.md:654-667.

String class used by catalogue: `{i32 length, i32 capacity, char *buffer}`; capacity 0x40/0x80/~2×len rounded to 16 (Post-Processing/the-post-processing-effect-catalogue.md:806).

Effect file: `<name>` + `_LUMINANCE_REMAP_S1.pso` under `TexUtil_D3D11\` (Post-Processing/the-post-processing-effect-catalogue.md:97, Post-Processing/the-post-processing-effect-catalogue.md:783-784); base name not stated.

GameSettingConfig `*(01F82D20)`: +0x30 DepthofField, +0x34 Glare, enum{Off|On}, default On (Post-Processing/CONTRACT-post-processing-subsystem.md:59; Post-Processing/the-post-processing-effect-catalogue.md:949-953).

JSON data: `jsondata/init.json` 176 keys defaults; 459 `maps/<mapcode>.json` strict overrides (39 keys in alc0101); 337 cutscene files (283 are scene-parameter sets), fallback Cut N → Common → `01F81328` → `01F813C8`; `uisize.json` 231 keys. Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:345, Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:547-555; Post-Processing/CONTRACT-post-processing-subsystem.md:114-115.
Cascade matrix: `obj + 0x350 + (row*3+col)*4`, row = q-1 (q∈1..3), col = c (0..2), key `"mCascadePartition%d_%d"` (`008FB2D8`) Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:704-718.
Font clut: `painter + 0xF68 + 36·index`, index bounded to 0x1B; entry +0x04..+0x10 shadow RGBA, +0x14..+0x20 font RGBA Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:386-388.
softEdges binding: definition 8, capture offset 160, size 8; packed def 13 B, native 24 B with `m_bufferLoc` offset word +0x10 / size word +0x12; size masked 0x1FFF; copy to receiver +0x118 (= owner +0x120..+0x127) Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:765-773.
GaussianFilterSetting.ini tiers (15×15 … 3×3, Factor 0.91, BlendAmount 0.5) Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:511-521. keymap.ini 16/8/3/3 Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:526-529.
SceneWideParameterConstantBuffer +0x5D4 `mShadowFlyingFadeSpeed`, +0x5DC `mShadowFlyingFadeRange` Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:402.

#### PP — State (globals and objects, with lifetime)

| global / object | lifetime | initial | cite |
|---|---|---|---|
| wrapper `[02D38540]` (0x10 B; holds library context at +0; `byte +8` zeroed) | lazily created by `0065E5D0`; never freed (not stated) | NULL until first use | Post-Processing/CONTRACT-post-processing-subsystem.md:56; Render-Command-List/the-ordered-render-command-list.md:1390, RCL (0065E530 entry) |
| library object `[02EA0B70]` (`CPostEffect`) | created by `006CBD20` on first post-processed frame | not stated | Post-Processing/CONTRACT-post-processing-subsystem.md:57, Post-Processing/CONTRACT-post-processing-subsystem.md:67-68 |
| `CTextureUtil` singleton `02EA1590` / refcount `02EA1598` | 123-B acquire allocs 0x22360 when null; 117-B release calls slot 4 + frees at last ref | null | Post-Processing/the-post-processing-effect-catalogue.md:814; Post-Processing/CONTRACT-post-processing-subsystem.md:58 |
| licence guard `01F31F70` | one-time | not stated | Post-Processing/CONTRACT-post-processing-subsystem.md:71 |
| log gates `01F3BA80`, `02EA0B40`, `01F3BA90` | read only | off in retail | Post-Processing/the-post-processing-effect-catalogue.md:188-190; Post-Processing/CONTRACT-ppfx-effect-creation.md:125-127 |
| `PostProcessParamContext` `[01F7F5F0]`/`[01F81300]` | lazy, `00193D50`; ctor `0018CD90` | ctor defaults 0.8/0.1 glare, enable 1, +0x330 = 1 | Post-Processing/CONTRACT-post-processing-subsystem.md:119, Post-Processing/CONTRACT-post-processing-subsystem.md:160, Post-Processing/CONTRACT-post-processing-subsystem.md:252; Render-Command-List/the-ordered-render-command-list.md:797 |
| `GameSettingConfig` `*(01F82D20)` | Save/Load layer | Glare/DOF default On | Post-Processing/CONTRACT-post-processing-subsystem.md:59 |
| JSON stores `01F813C8` (init), `01F81328` (per-map), `01F813A8`/`01F813D8` (cutscene banks), record `01F812D0`, UISize doc `01F81318` → settings +0x3B00 | built by `001C61F0`, `001C5930`, `001C6C00`; `001C7290` re-applies after resetting banks | not stated | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:345 |
| flying-fade globals (two) | written by `001C7940` | defaults document fallback | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:144-147 |

#### PP — Order (what runs when, and what triggers it)

Per post-processed frame (Post-Processing/CONTRACT-post-processing-subsystem.md:80-107; Post-Processing/the-post-processing-effect-catalogue.md:933-947): step 1 (`+0x99` reset arm, or lazy create if no library object) → step 2 return if still no object (`00193DFC`) → 3 → 4 → 5 glare (always called, args depend on option) → 6 → 7 DOF (always called) → 8 run + Phyre render-context guard. Trigger: `PostProcessObj::Execute` enqueues `00193DA0` when `01DFE0C4` on (Post-Processing/the-post-processing-effect-catalogue.md:814). Catalogue build (CP) happens inside the lazy create of the first such frame (Post-Processing/the-post-processing-effect-catalogue.md:814) and again after the reset arm (Post-Processing/the-post-processing-effect-catalogue.md:814). JSON readers: map reader run by `001C61F0` on map load; cutscene banks by `001C5930`; apply gate `01F81280` raised by `001CC600` from the per-frame `0017D6E0` (Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:345, Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:873). Library scene bracket: `BeginPostEffectScene`…`EndPostEffectScene`, `SetFramebuffer` refused inside (Post-Processing/ppfx-function-identification.md:144-151).

#### PP — Dependencies

Render command list (`PostProcessObj::Execute`, kind-0x2F command) Post-Processing/CONTRACT-post-processing-subsystem.md:285, Post-Processing/CONTRACT-post-processing-subsystem.md:303-306; Save/Load settings (`GameSettingConfig`) Post-Processing/CONTRACT-post-processing-subsystem.md:294-295; Platform (`006253D0` shares wrapper, `0065E580(wrapper,1)`) Post-Processing/CONTRACT-post-processing-subsystem.md:290-292; Resource logger `005CDAA0` Post-Processing/CONTRACT-post-processing-subsystem.md:297-301; CoreRuntimeScheduling arena `[01F7F4C0]` Post-Processing/CONTRACT-post-processing-subsystem.md:308-310; Developer console writes block (16 arms, 33 sites) Post-Processing/CONTRACT-post-processing-subsystem.md:130-136; Phyre post-process chain (22-Middleware) Post-Processing/CONTRACT-ppfx-effect-creation.md:34; Yebis/PPFX source map (23-Third-Party) Post-Processing/the-post-processing-effect-catalogue.md:814; JSON parser `JsonBox` / `001FF740` Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:471, Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:634; Phyre asset loader (`0059EC40`, `0059CD14`) Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:781-789; D3D11 constant buffer path `006097B0`→`00626060` Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:402.

### 1.12 [CM] Scripted camera, screen fade, screen effects, aspect fit, position-to-scalar, movie index

Short names in this part: **MR** = `Movie-Containers/README.md`; **MH** = `Movie-Containers/mh-movie-seek-index.md`; **PTS** = `Position-To-Scalar/how-a-position-becomes-a-single-number.md`; **SF** = `Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md`; **AF** = `Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md`; **CI** = `Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md`; **CR** = `Scripted-Camera/how-a-camera-reaches-the-renderer.md`; **P** = `Scripted-Camera/the-scripted-camera-player.md`; **RM** = `README.md`; **WT** = `../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`.


#### CM — Entry points

| entry (size) | callers as stated | what it does | cite |
|---|---|---|---|
| `001B7F30` movie open | player (via `001847D0()` id) | `002DF980(0x1C, id×2)` → basename between last `\` and `.` → `"%s%s.webm"` under `/GameData/D3D11/ArtData/video/` | Movie-Containers/mh-movie-seek-index.md:90-92; Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:644-654 |
| `0035B840` (via stub `00356460`) | not stated | fetches kind-28 index 2m+1 (`.mh`) and discards it, then `001848A0` | Movie-Containers/mh-movie-seek-index.md:93-95 |
| `001848A0` (24 B) → `001B82F0` → `0067A9B0(rcx+0x678)` (390 B) | `0035B840` | movie-container op; `0067A9B0` state-1→3 channel teardown | Movie-Containers/mh-movie-seek-index.md:230-241 |
| `001B7690` (75 B) | `001B7F30`, `001B8400` | cold-start: `dword[rcx]=-1`, zero +4/+9/+0x18/+0x20, `0067A9B0(rcx+0x678)`, `0017D960(1)`, `002E1CA0(1)`, tail `00229AE0(1)` | Movie-Containers/mh-movie-seek-index.md:245-258 |
| `002F1F40(actor, position, out)` (1,510 B) | 75 functions / 76 sites, `00442550`…`00537410` | per-object distance-fade modulate colour (init `0x80808080`, byte 3 alpha) | Position-To-Scalar/how-a-position-becomes-a-single-number.md:180-215, 321, 326 |
| `002F1D90` (289 B) | `002F1F40` | lock, `|b−a|` (sqrtf `00861F14`), unlock | Position-To-Scalar/how-a-position-becomes-a-single-number.md:167 |
| `0024BFD0` (130 B) | effect driver once a frame in draw 0 | global-scale ramp on `020926E8` (bits 8/9 of `020926E4`) | Position-To-Scalar/how-a-position-becomes-a-single-number.md:362 |
| `002EFA70(layer, frames, direction, white)` | `fadeout`/`whiteout`/`fadein` (00B6-00B8), `_d0/_d1/_d2` (00D0-00D2), three `WorldTransition_*`, runtime pass, `0035CA70`, skip family `003601D0`,`003603F0`,`00360480`,`00360710`, `00228C70`,`0027EFA0`,`00280140`,`003939B0`,`00394130`,`003EFAA0`, `0037DEA0` | start a fade on one of 7 layers | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:59-69, 95-101, 116-118 |
| `002EF910` | `World_UpdateSimulationTick` (`00314020`) | per-tick poll of 7 records | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:76-81 |
| `002EF840`/`002EF890`/`002EFA20` | `002EF890` = `mapjump` (008D, `00355350`); `002EF840` ×7 by `003600D0` | free one / all / reset | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:87-90, 571-574 |
| `002EF9F0`/`002EFD20`/`002EFE10`/`002EFE40`/`002EFE50`/`002EFE60` | schedule, skip, `0035CA70` | handle / state / colour override / words `022BDEB4`/`022BDEB0`/`022BDEB8` | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:89-92 |
| `002EFD50`/`002EFD80(n)`/`002EFDC0(n)` | `efffadein`/`efffadeout` (0268/0269) | single effect-fade handle via `0036E750(0,0,&params,n,9)` | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:93 |
| `00375900(&desc)` (~186 B), `00375A20`, `003B0F80`, `00375AE0`, `00375470`, `00374950` | fade start, CI per-frame bodies | screen-effect descriptor pool 32×0x70 at `02EBF9E0`; slot chooser; live-handle list; state query; release; pool tick | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:61-72, 228-242; Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:90-98 |
| `0037DDD0` / `0037DEA0` (239 B) | under `MainLoop_UpdateAndRenderFrame` | movie-fade schedule row select into `02ADED98`, apply | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:107-118, 717 |
| `0035CA70` (1,118 B) via factory `0035CFA0`, procedure `0035C960` | `00304440`, `003CA310` msg 0x12 (+8==0x8102) | 14-state sequencer (fade out → … → fade in) | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:138-180 |
| `001DDBA0` → tail `001DDAC0(record, W, H)` | `00182F70`, `001DC730` | log + aspect fit into 0x18-byte record | Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:25-27, 42-73, 94-97 |
| `001DD120`, `001DD8C0`, `001DCE20`, `00225680`, `002256A0` | 24 methods / 72 getter sites | aspect (W/H in mode 1 else 16/9), mode==1, mode name, width, height | Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:110-114 |
| `001DDA70` / `001DC5C0` / `001DDAB0` | `0017D6B0` startup sequencer | build / construct / get display object `[01F82D18]` | Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:154, 192 |
| `0024CF50` / `0024CEB0` / `0024CBE0`→`003AA6B0` | `cutinplay` `003DF8F0`; `cutinclear`; driver `0024D540` | cut-in play / clear / per-frame | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:68-70, 125, 129-140 |
| `0024EC00` / `0024EB20` / `0024EA10`→`003AAA50` | `moveblurplay`, fade tick `003DE160`, clear; driver | motion blur | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:68-70, 155-196 |
| `0024FAE0` / `0024FA40` / `003AB500` | service `0036E810` (from `0034FA00` and area unload ×2) | soft focus | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:200-210, 233-236 |
| `0024D540` (551 B) driver | `MainLoop_Draw` `0022B0B0`, `MainLoop_UpdateAndRenderFrame`, `0022BC20` | gate on frame mode 2 or 6; calls three per-frame bodies | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:88-90, 268; ../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md:692 |
| `003DE210` (40 B), `0024E910` (256 B), `0024C7C0` (172 B) | area unload, skip cleanup, one unread | forced blur fade end; effect teardown; ordinary mask | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:219-232, 75 |
| `003829D0(camera, priority)` (373 B) | `00259820` (0x14), `00259970` (0x14), `003ED8A0` (0x64) | submit to 8 slots | Scripted-Camera/how-a-camera-reaches-the-renderer.md:37-56 |
| `003820C0` (2,125 B) | one caller, a five-byte-call wrapper | arbitration + build of matrices | Scripted-Camera/how-a-camera-reaches-the-renderer.md:58-127 |
| `00382910` (163 B) | graphics start-up wrapper | reset | Scripted-Camera/how-a-camera-reaches-the-renderer.md:69-71 |
| `00382B70` (119 B) | `0037D4C0`, `0037D890` | shake offset setter | Scripted-Camera/how-a-camera-reaches-the-renderer.md:136-138 |
| `0037D4C0` (808 B) / `0037D890` (209 B) / `0037D970` (0xF5) | once per draw / `00314020`, `003143D0` | shake gather / reset / accumulator write | Scripted-Camera/how-a-camera-reaches-the-renderer.md:147-196, 422; ../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md:1140 |
| `003DCFB0` (285 B), `0037D1F0` (712 B), `0037D130` (190 B) | `00314370` (5-slot loop) | shake driver, sampler, parameter loader | Scripted-Camera/how-a-camera-reaches-the-renderer.md:205-283 |
| `003DD230` / `003DD320` / `003DCF60` | handlers `00349730` (1a3, 019C), `003492F0` (1a2); `019E`; `01A1` | start / stop / clear shake | Scripted-Camera/how-a-camera-reaches-the-renderer.md:287-303 |
| `003DA400` / `003DA4D0` / `003DA570` / `003DA000` / `003DA2D0` / `003DA330` | camera verbs table | start / stop / change / clear / rate / hit-check | Scripted-Camera/the-scripted-camera-player.md:95-110 |
| `003DA050` (302 B) | `00314370` (5-slot loop) | per-slot camera channel tick | Scripted-Camera/the-scripted-camera-player.md:112-141, 941-957; Scripted-Camera/how-a-camera-reaches-the-renderer.md:244-259 |
| `00258350` (1,942 B) / `00257A00` | `002555A0` / tick on skip | CAM7 interpreter / run to end | Scripted-Camera/the-scripted-camera-player.md:159-197, 143-145 |
| `002555D0` (279 B) | per frame (caller not stated) | publish to camera record 5 / sub-view; `CameraSystem_SetCameraActive(5)` | Scripted-Camera/the-scripted-camera-player.md:282-289 |
| `002572E0` (570 B) | manager runtime init | decode attachment word | Scripted-Camera/the-scripted-camera-player.md:80-83, 399-415 |
| `00257830`/`00257520`, `00255C50`/`00255850`, easing `00256650` | `resumebehindcamera` 0x1E4, `behindtoeventcamera` 0x34F | two eased blends writing record 5 | Scripted-Camera/the-scripted-camera-player.md:622-646 |

#### CM — Inputs and outputs (record layouts)

**`.mh`** — header 0x18: `+0` char[4] `.mhe`; `+4` u8 (1/5/9); `+5` u8 1; `+6` u16 varies; `+8` u16 width 512; `+0xA` u16 height 352/448; `+0xC` u32 streamBytes; `+0x10` u32 frameCount; `+0x14` u32 entryCount; entries 0xC: `+0` u32 offset, `+4` u32 frame, `+8` u32 flags (Movie-Containers/mh-movie-seek-index.md:63-79). File size `0x18 + 12×entryCount` (Movie-Containers/mh-movie-seek-index.md:44). Not read by the game (Movie-Containers/mh-movie-seek-index.md:86-99).
**Kind-28 path array** `01ECB4D0`: index 2m `.md`, 2m+1 `.mh`, NULL-sparse at 76-81, 92-93 (Movie-Containers/mh-movie-seek-index.md:86-88, 104-107); installed by `ResourcePath_Init` `002DFAF9`/`002DFB00` (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:652).

**Fade node record** (`[02F97348]+0x2F0` or `[actor+0x20]+0x50`): `+0` fade kind 1/2/3/4; `+1` distance mode 0/1/2; `+2`/`+3` floor bytes; `+4`/`+8` pair (kind 2), `+6`/`+0xA` pair (kind 1); `+0xC` float (kind 3) (Position-To-Scalar/how-a-position-becomes-a-single-number.md:184-200). Container flag word `+0x368` bits 2,3,4,5,10,12,13; colours `+0x334`/`+0x398`; `+0x35C`, `+0x377`, `+0x37C` (Position-To-Scalar/how-a-position-becomes-a-single-number.md:201-208, 343-346). Output dword colour `0x80808080` with byte 3 = `clamp((far−d)/(far−near)×255, floor, 256)×0.5` (Position-To-Scalar/how-a-position-becomes-a-single-number.md:180-200).
Matrices: `02AEEA20` 64 B, `02AED5F0` 16 B, `02AEECB0` 64 B, `02F97348` 8 B (Position-To-Scalar/how-a-position-becomes-a-single-number.md:171-174); viewport `004679C0(m,w,h)`: m00=w/2, m11=−h/2, m30/m31=2048, m33=1, z 1024…`0x4B7FFBFF` (Position-To-Scalar/how-a-position-becomes-a-single-number.md:227-231; Scripted-Camera/how-a-camera-reaches-the-renderer.md:486).

**Fade layer** `022BDD60`, 7 × 0x30: `+0` handle (`0x80000000|counter`); `+4` state 0/1/2; `+5` direction; `+0x08`-`+0x2F` descriptor (`+8`=1 kind, `+9` nibbles, `+0xA`=1, `+0xB`, `+0x24` flags, `+0x28` colour, `+0x2C`=2×frames) (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:43-51, 199-204). Globals `022BDD50` double, `022BDD56`-`022BDD5D`, `022BDEB0`/`B4`/`B8` (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:194).
**Pool record** `02EBF9E0`, 32 × 0x70: `+0x00`-`+0x67` descriptor, `+0x68` handle, `+0x6C` elapsed counter (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:228-229); counter `02EC07E8` (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:66). Descriptor generic: `+0` kind, low nibble `+1` pass, `+2` class, `+0x1C` flags (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:93-98); kind 4: `+0x20` image, `+0x28` palette, `+0x30` qword PS2 tex reg, `+0x50` texture (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:100-105).
**Movie fade row** (battle_pack.bin dir entry +0x118, `st2e`, count 49, stride 8, data at +0x20; 432-byte section): `+0` id, `+1` fadeInStart, `+2` fadeInLength, `+3` fadeOutLength, `+4` fadeOutLead, `+7` flags bit0 white in / bit1 white out (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:113-118, 206-207, 352-356). Player ctx: `+0x14` elapsed, `+0xC0→+0x10` length, `+0xC8` row, `+0xF0` issued bits (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:109-111).
**0035CA70 task** 0xD0 B: `+0xC0` state, `+0xC1` saved next, `+0xC2` msg byte, `+0xC4`/`+0xC8` handles (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:140-148).

**Aspect record** (start of display object `[01F82D18]`, 0x18 B): `+0` mode 0/1; `+4`,`+8`,`+0xC` floats (unread); `+0x10` W; `+0x14` H (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:46-53, 103-117). Display object 0x180 B: `+0x18` live screen mode, `+0x20` mode count, `+0x24`/`+0x28` display-mode index / DXGI_MODE_DESC table (0x1C stride: W, H, RefreshNum, RefreshDen, Format, ScanlineOrdering, Scaling), `+0x30` refresh Hz, `+0x38`/`+0x40` window-size index/table, `+0x48`..`+0x78` adapters, `+0x80` mode-name string (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:131-170, 146). Constants 16/9 `008C5B38`, 16/3 `00900A0C` (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:31-34).

**CI staging/live**: cut-in staging `02B59D20` 0x24 B (`+0` type, `+1` bit0 linefade, `+4`/`+8` pos, `+0xC` rotation, `+0x10` linewidth, `+0x14`/`+0x18` uv, `+0x1C` colour, `+0x20` line colour), live `02092640`, target `02092638`, 5 handles `02092664` (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:65-66, 112-123). Blur staging `02B58C38` 12 B (`+0` preset, `+1` clut, `+2` noise, `+3` screen, `+4` bit0 capture-once, `+8` float strength), live `02092678`, targets `02092688/90/98`, 8 handles `020926A0`, fade task ptr `02B58C48` (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:144-153, 188). Soft focus `020925F0` 0x30 B (`+0` mode, `+1` b, `+2` size sel, `+4` amount), target `02092620`, 3 handles `02092600` (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:66, 202-206). Flag word `020926E4` bits 0,3,4,5,6,10,11 (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:67, 229-231). Late-release list 256 at `02091950`, count `0209216A` (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:77-79). Skip dword `01FD4A70` (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:172-174).

**Camera submit**: 8 slots × 0xE0 at `02AED630` (`+0`..`+0xCF` camera, `+0xD0` submitted, `+0xD4` priority) (Scripted-Camera/how-a-camera-reaches-the-renderer.md:39-41). Camera record 0xD0: `+0` near, `+4` far, `+8` fov, `+0xC` fov2, `+0x10` 1/tan(fov/2), `+0x20` view matrix, `+0x60` world matrix (eye `+0x90`), `+0xA0` look-at, `+0xC4` roll (Scripted-Camera/how-a-camera-reaches-the-renderer.md:330-332); `+0xB0` third vector, `+0xC0` kind tag 2/3 (Scripted-Camera/the-scripted-camera-player.md:1039-1045). Working block `02AED4A0` (camera at `+0xC0` = `02AED560`) (Scripted-Camera/how-a-camera-reaches-the-renderer.md:67). Matrices `02AEDD30`,`02AEDD70`,`02AEDDB0`,`02AEDDF0`,`02AEDE30`,`02AEDE70`,`02AEDEB0`,`02AEDEF0`, heading `02AEDF94` (Scripted-Camera/how-a-camera-reaches-the-renderer.md:109-120). Offsets `02AEDF70`/`02AEDF80` vec4, `02AEDF98`/`02AEDF9C` floats, `02AEDFA0` (Scripted-Camera/how-a-camera-reaches-the-renderer.md:69-71, 136-138).
**Shake table** `02ADDA34`, 5 × 0x3D0 (header `+0` entry array, `+8` curve table; 4 channels × 0xF0 with draw tag) (Scripted-Camera/how-a-camera-reaches-the-renderer.md:140-145, 225); accumulator `02EBF380 + draw×0x20` (28 B written) (Scripted-Camera/how-a-camera-reaches-the-renderer.md:173, 193-196); option flags `02EBF3C4`, `02EBF3C0` (Scripted-Camera/how-a-camera-reaches-the-renderer.md:180-185). Authored entry 0x60 B: 32 curve numbers from `+0x30`, duration word `+0x28` (Scripted-Camera/how-a-camera-reaches-the-renderer.md:222-232). Bank behind slot `+0xF0`: count `+4`, 16-byte entries, data id at `+0x14+index×16` (Scripted-Camera/how-a-camera-reaches-the-renderer.md:296-297).
**Slot channel** (camera `+0x110`, shake `+0x170`), 0x18 B: `+0` shot/data id, `+4` frame/draw tag, `+8` u16 state, `+0xA` u16 entry/bank index, `+0xC` f32 clock, `+0x10` f32 rate, `+0x14` u8 clockRunning (Scripted-Camera/the-scripted-camera-player.md:466-475; Scripted-Camera/how-a-camera-reaches-the-renderer.md:208, 297). Frame-owner words slot `+0x18`/`+0x1A` (camera), `+0x1C`/`+0x1E` (shake) (Scripted-Camera/the-scripted-camera-player.md:88, 945; Scripted-Camera/how-a-camera-reaches-the-renderer.md:210, 301).
**CAM7** (EBP section_009/008): record `+0` 0, `+4` length, `+8` name, `+0x20` attachment word, `+0x24`/`+0x26` joint words, `+0x28` command stream ending `0xFF`+3 pad (Scripted-Camera/the-scripted-camera-player.md:361-363); Key 0x40, Segment 0x2C, Curve `0x18+0x24k`, CurveKey 0x24, Path `0x20+0x38s+8a`, PathSegment 0x38, arc pair {distance, param} (Scripted-Camera/the-scripted-camera-player.md:365-459); attachment word bit map (Scripted-Camera/the-scripted-camera-player.md:401-411). Player record 0x2E0 at `02092830 + slot×0xBB0 + ch×0x2E0`, slot header `02092800` (Scripted-Camera/the-scripted-camera-player.md:149-155, 480-509). Frame views `02096370` 2×0x40 (eye `+0`, target `+0x10`, roll `+0x20`, fov `+0x24`) (Scripted-Camera/the-scripted-camera-player.md:188-190, 351). Camera records `02097300` 8×0x110 (`+0` eye, `+0x10` target, `+0xF0` mode), active mask `02098DEC`, sub-view `02097B80` (Scripted-Camera/the-scripted-camera-player.md:284-289, 352-354, 511-513, 1059).

#### CM — State (globals and objects, with lifetime)

| state | address / size | lifetime | init | cite |
|---|---|---|---|---|
| fade layers | `022BDD60`, 7×0x30 | `002EFA20` reset; `002EF840`/`002EF890` free; `003600D0` frees 0-6 | reset: state byte `022BDD56=3`, handles zero, `022BDEB4=6` | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:90, 571-574 |
| fade globals | `022BDD50` double; `022BDD56`-`5D`; `022BDEB0/B4/B8` | start zeroes `022BDD50`, sets `022BDD56=3`,`022BDEB0=0`,`022BDEB4=6` | as left | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:59-69 |
| descriptor pool | `02EBF9E0` 32×0x70, counter `02EC07E8` | kept packed; release shifts down | elapsed zeroed at alloc | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:61-67, 228-238 |
| movie schedule row | `02ADED98` | selected each frame in mode 1/2 | not stated | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:107-108 |
| aspect / display object | `[01F82D18]` 0x180 | built `001DDA70`, constructed `001DC5C0` | not stated (`+0x08` "whatever it held before") | Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:84, 154 |
| settings | `01F82D20` GameSettingConfig (31 u32) | stored once at `00798261` | defaults per settings page | Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:151-153 |
| fade-node globals | `02AEEA20`,`02AED5F0`,`02AEECB0`,`02F97348`,`020926E8` | BSS (zero in image); runtime title-screen values only | zero at load | Position-To-Scalar/how-a-position-becomes-a-single-number.md:87-93, 101-143 |
| effect scale ramp | `020926E4` flags (bits 8/9), `020926E6` count, `020926E8` value, `020926EC` target, `020926F0` step | time-stop setters; `0024BFD0` | zero (BSS) | Position-To-Scalar/how-a-position-becomes-a-single-number.md:362 |
| CI blocks | see B2 | staging reset at every area change; clear on unload | `resetcutinparam`/`resetmoveblurparam` defaults (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:114-123, 146-153) | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:216-218 |
| camera slots | `02AED630` 8×0xE0 | flags cleared by `003820C0` each update; zeroed by `00382910` | 0 | Scripted-Camera/how-a-camera-reaches-the-renderer.md:62-64, 69 |
| shake offsets | `02AEDF70`,`02AEDF80`,`02AEDF98`,`02AEDF9C` | written by `00382B70` | zero, w=1.0 (`00382910`) | Scripted-Camera/how-a-camera-reaches-the-renderer.md:69-71 |
| shake table / accumulators | `02ADDA34`; `02EBF380` | `0037D890` resets (tags −1, accum zero) | — | Scripted-Camera/how-a-camera-reaches-the-renderer.md:147-148 |
| CAM7 slots / players | `02092800` 5×0xBB0; scratch `02096520` | `002556F0` InitAll; `002566E0` reset one | `+0x184 = −1` | Scripted-Camera/the-scripted-camera-player.md:151-158, 301, 349-350 |
| camera records | `02097300` 8×0x110, mask `02098DEC` | not stated | not stated | Scripted-Camera/the-scripted-camera-player.md:284-289 |
| blend globals | `020963F0`-`02096404`; `02096270`-`02096290` | starters `00257830`/`00255C50` | not stated | Scripted-Camera/the-scripted-camera-player.md:627-636 |

#### CM — Order (what runs when, and what triggers it)

| what | when / trigger | cite |
|---|---|---|
| fade poll `002EF910` | per world tick from `World_UpdateSimulationTick` | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:76 |
| movie fade schedule `0037DDD0` | under `MainLoop_UpdateAndRenderFrame`, when player mode 1 or 2 | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:107-109 |
| descriptor counter tick `00374950` | "1 per tick, or 2 on the first tick" — caller not stated | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:239 |
| CI per-frame bodies | `0024D540`, frame mode 2 or 6; argument = draw 0/1 | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:88-90 |
| blur skip | `MainLoop_Draw` returns early when `01FD4A70` set | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:172-174 |
| effect scale ramp `0024BFD0` | effect driver once a frame in draw 0 | Position-To-Scalar/how-a-position-becomes-a-single-number.md:362 |
| fade node `002F1F40` | while an element of the current container is drawn; container current set by `0024D5A0` / `0024ED80` | Position-To-Scalar/how-a-position-becomes-a-single-number.md:337-339, 371-373 |
| camera submit | `00259820` (active), `00259970` before second draw (frame body `0022A770`), `003ED8A0` effect parse | Scripted-Camera/how-a-camera-reaches-the-renderer.md:52-56, 386-387 |
| camera update `003820C0` | consumes all submissions; none → previous matrices stand | Scripted-Camera/how-a-camera-reaches-the-renderer.md:62-65 |
| shake gather `0037D4C0` | once per draw | Scripted-Camera/how-a-camera-reaches-the-renderer.md:150 |
| `00314370` (slot loop: `003DA050` then `003DCFB0`) | from `0022A770` ×3, `MainLoop_UpdateAndRenderFrame` ×2; per-frame count "not established" | Scripted-Camera/how-a-camera-reaches-the-renderer.md:244-269 |
| `002555D0` publish | "per frame" (caller not stated) | Scripted-Camera/the-scripted-camera-player.md:282 |
| aspect fit | on `001DC730` / `00182F70` (trigger not stated) | Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:94-97 |
| `ResourcePath_Init` before any movie | boot body `0022A0B0` | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:700-702 |

#### CM — Dependencies

Resource (kind-0x1C path table, string helpers `001A0A90`/`001A0BB0`/`001A1220`) (Movie-Containers/mh-movie-seek-index.md:223; Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:301-311, 692-698); Audio (`005CD330` etc. row-buffer releases in `0067A9B0`) (Movie-Containers/mh-movie-seek-index.md:216); Script VM verbs (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:95-98; Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:293-296; Scripted-Camera/how-a-camera-reaches-the-renderer.md:420; Scripted-Camera/the-scripted-camera-player.md:95-104); world tick / field frame (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:76; Scripted-Camera/how-a-camera-reaches-the-renderer.md:386-387, 422); time-stop registry (`020926E8` ramp; display-deny `02B59D71`) (Position-To-Scalar/how-a-position-becomes-a-single-number.md:361-362); character fade (`003B30D0` writes container colours) (Position-To-Scalar/how-a-position-becomes-a-single-number.md:348-351); RNG gameplay MT19937 via `RNG_MT19937_NextFloatClosed` (Scripted-Camera/how-a-camera-reaches-the-renderer.md:234-239, 416); settings Screen Shake `02EBF3C4` (Scripted-Camera/how-a-camera-reaches-the-renderer.md:183-185); DXGI mode list from Platform `001DD420`/`006242C0` (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:203-210); `GameSettingConfig_WriteFile` (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:212-214); EBP section_008/009/010 (Scripted-Camera/the-scripted-camera-player.md:70-78, 541); frame pass mask / queued-effect kinds (22-Middleware The-Frame) (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:286-289); Movement `0026E500`/`00233230` (Scripted-Camera/how-a-camera-reaches-the-renderer.md:392-394).

