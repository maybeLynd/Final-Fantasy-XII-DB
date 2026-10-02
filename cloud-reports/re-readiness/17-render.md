# Reconstruction readiness — `FFXII TZA/17-Presentation-Rendering/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-17-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`34861cfd`); no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. |

**Counts:**
- **60 `.md` pages read in full** (36,542 lines): the category `README.md`, 4 sub-folder READMEs, 8 `CONTRACT-*.md` pages and 47 system pages. **60 `.tsv` checks**, layout or count only, over 26 member files named in Appendix A.
- **12 parts** (§1), with **395 entry-point rows**.
- **255** self-stated open gaps (S-) and **231** structural gaps (G-) (§2).
- **471 contradictions** (§3):
  - **193 value-changing** (§3.1), all "page-text only - needs local check". **33** have a favoured side settled by a dated correction on the pages (2 of them only in part: ET.CV-1, MF.CV-3); **160** have no favoured side.
  - **82 count/census disagreements** that change no runtime behaviour (§3.2).
  - **196 stale / banner items** (§3.3): **44** front-matter / body-banner / `README.md`-tag disagreements, **100** stale "not read / open" claims that another page or a later dated section answers, **52** corrected or struck claims still repeated unstruck elsewhere.
- **Rating: NOT YET** overall (§4); of 71 sub-parts, **3 READY, 53 MOSTLY, 15 NOT YET**. **READY:** the `@FRP` and `@FEF` containers and the coast-down seam. **NOT YET:** the PS2 shadow draw and V2 pool, the character render object's draw, the dirty-state protocol, the render-record frame stages, the rig controllers' per-frame output, the render command classes' execute bodies, the D3D11 primitive-renderer device interface, the VU1 microprograms, effect element types `0xA1`-`0xAA`, `@FRM` motion data, the per-model oscillator, the PPFX effect library (byte-faithful) and its function-identification page, the movie (WebM) playback path, and the frame order across the category.

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

## 2. Gaps

### 2.1 Gaps the pages state themselves (still open, or live-only)

Only items still open after every later dated section on the pages was read are listed. Items that a later section answers are in §3.3 as stale text. Ids are `<part>.S-n`.

#### 2.1.1 [AC] Authored commands, ramp channels and the coast-down latch

| id | gap | cite |
|---|---|---|
| AC.S-1 | How often the repeat dispatch fires in play: "its frequency is a live question, not measurable statically" | CONTRACT-authored-command-ramp-channels.md:449-450 |
| AC.S-2 | Threading: "not established. The bodies take no lock" | CONTRACT-authored-command-ramp-channels.md:313-314 |
| AC.S-3 | The `.rdata` words `01CC74B4`/`01CC78B4`: "a second, not-yet-decoded `{u32,u32}` record table" | CONTRACT-authored-command-ramp-channels.md:188-189, :273-274 |
| AC.S-4 | The out record's field names "stay interpretive — the arithmetic is proven, the labels are not" | CONTRACT-authored-command-ramp-channels.md:401-402 |
| AC.S-5 | `02B3F554`: "its consumer is outside static addressing or does not exist" | CONTRACT-authored-command-ramp-channels.md:417 |
| AC.S-6 | Ramp TIMING "is read statically in §9, not measured" | CONTRACT-authored-command-ramp-channels.md:391-392 |
| AC.S-7 | What the V2 shadow pool values do on screen: "is not established here" | Authored-Commands/the-authored-presentation-command-handlers.md:1051-1052, :1139 |
| AC.S-8 | Which bone key 29 / 0x1E is per model; what subtypes 2/6, 4, 5 and 9 look like, and why 7 and 8 are authored; palettes; whether `004218A0`'s by-name lookup matches on kind-2 `@FTR` | Authored-Commands/the-authored-presentation-command-handlers.md:1083-1084, :1139-1141 |
| AC.S-9 | `+0x290` bit 24 re-apply: the 34 wholesale `mov dword` writers "were **not traced**" | Authored-Commands/the-authored-presentation-command-handlers.md:754-758 |
| AC.S-10 | Equal 3/4/5 variant counts: "that was not checked container by container" | Authored-Commands/the-authored-presentation-command-handlers.md:751-752 |
| AC.S-11 | What precedes `0x00` in the other blocks (31,942 − 30,003 = 1,939, my arithmetic): "not tallied" | Authored-Commands/the-authored-presentation-command-handlers.md:291-292 |
| AC.S-12 | The dispatch-table writer sweep "cannot see image-base-relative stores" | Authored-Commands/the-authored-presentation-command-handlers.md:1007-1008 |
| AC.S-13 | Live only: whether a real character reaches 128 stopped calls; which subtypes occur (0x0D) | CONTRACT-coast-down-latch.md:386-392 |
| AC.S-14 | "What index `0x10` is on screen remains unnamed"; the 0x2010 post "is not traced" | CONTRACT-coast-down-latch.md:435-438 |
| AC.S-15 | `01F83530` zero for the process's life is "**supported, not proven**" | CONTRACT-coast-down-latch.md:508-509 |
| AC.S-16 | TIMING, INTEGRATION and PRESENTATION parity are not covered | CONTRACT-coast-down-latch.md:527-531 |
| AC.S-17 | The `+0x457` writer "was read, not run" | CONTRACT-coast-down-latch.md:383-384 |

#### 2.1.2 [RO] Render-record pool, character render object, transform publish and lighting

Short names in this part: **POOL** = `CONTRACT-render-record-pool-lifecycle.md`; **CRO-C** = `CONTRACT-character-render-object.md`; **PUB** = `CONTRACT-character-transform-publish.md`; **CRO** = `Character-Rendering/character-render-object.md`; **LIT** = `Character-Rendering/how-a-character-is-lit.md`.


| id | gap | cite |
|---|---|---|
| RO.S-1 | "The bit meanings of the flag word at `+0x18`" | CONTRACT-render-record-pool-lifecycle.md:531-532 |
| RO.S-2 | `+0x40` and `+0x4C..+0x70`: "no reader observed in a depth-2 route census" | CONTRACT-render-record-pool-lifecycle.md:533-534 |
| RO.S-3 | "`+0x64` … whether it is one field or two is **not** decided" | CONTRACT-render-record-pool-lifecycle.md:535-536 |
| RO.S-4 | "The relationship, if any, between the 16-bit index at `+0x2C` and either list" | CONTRACT-render-record-pool-lifecycle.md:537 |
| RO.S-5 | "Which caller supplies the names that key allocation" | CONTRACT-render-record-pool-lifecycle.md:538 |
| RO.S-6 | "What the eleven scripted callees do to a record beyond these fields is NOT established" | CONTRACT-render-record-pool-lifecycle.md:600, 431-433 |
| RO.S-7 | Retire's child loop: "its termination is **the callee's postcondition, not retire's**" (not driven) | CONTRACT-render-record-pool-lifecycle.md:425-428 |
| RO.S-8 | "What the pointer in `+0x48830` points AT … 16 readers use it" | CONTRACT-render-record-pool-lifecycle.md:868-870 |
| RO.S-9 | "Whether any `PHOOK` implementation reads `+0x48818` bit 0" | CONTRACT-render-record-pool-lifecycle.md:871-873 |
| RO.S-10 | "Left open: `0041D220` / `0041CB90` resource admission and defaults, the native cleanup helpers, and external ID invalidation" | CONTRACT-render-record-pool-lifecycle.md:705-706 |
| RO.S-11 | "Whether `003AB7F0` can unlink a node is not established here" | CONTRACT-render-record-pool-lifecycle.md:702-703 |
| RO.S-12 | Three live-game requests (invariant 3, cursor termination, promotion boundary) | CONTRACT-render-record-pool-lifecycle.md:435-446 |
| RO.S-13 | "The extent of the embedded object at `+0x3E0`" | CONTRACT-character-render-object.md:191; Character-Rendering/character-render-object.md:208 |
| RO.S-14 | "What `r8d` selects … the selector's own meaning stays with the caller" | CONTRACT-character-transform-publish.md:343-347 |
| RO.S-15 | Publish: "nothing observed live" | CONTRACT-character-transform-publish.md:363, 406 |
| RO.S-16 | "the pooled element's `3` (a likely expiry count) is not followed here" (see also RO.CS-7) | Character-Rendering/character-render-object.md:419 |
| RO.S-17 | "`001F5C20`, has no caller in the graph at all and is not explained" | Character-Rendering/character-render-object.md:445-446 |
| RO.S-18 | "Which values each slot receives per frame is not followed here" | Character-Rendering/character-render-object.md:484-485 |
| RO.S-19 | "Which records draw first is the render command list's order, not read here" | Character-Rendering/character-render-object.md:349-350 |
| RO.S-20 | WH/HS matrix meaning: "an interpretation of the names, and no matrix was multiplied out" | Character-Rendering/character-render-object.md:824-826 |
| RO.S-21 | UQ-203 residual: "receiver types at those 18 sites were not proven" | Character-Rendering/character-render-object.md:850-851 |
| RO.S-22 | `+0x118`/`+0x80`/`+0x420` spans: "unread on every route this corpus has" | Character-Rendering/character-render-object.md:1092-1099 |
| RO.S-23 | "The heads of four evaluators (kinds 2 to 5) were not read line by line; what the third space mode (byte `+6` = 1) is for; the units of range" | Character-Rendering/how-a-character-is-lit.md:251-252 |
| RO.S-24 | "What the two typed-handle predicates test, and what byte of the character's object sets the camera-anchored light's float" | Character-Rendering/how-a-character-is-lit.md:256-257 |
| RO.S-25 | "What writes `+0x28C` was not traced" | Character-Rendering/how-a-character-is-lit.md:257-258 |
| RO.S-26 | "What sets `02B3F520`" (the `02B3F503`/`02B3F51C` part is answered, RO.CS-10) | Character-Rendering/how-a-character-is-lit.md:259 |
| RO.S-27 | "what class 3 is was not established" | Character-Rendering/how-a-character-is-lit.md:78-79 |
| RO.S-28 | `004FD4B0`: "only its head … was read"; whether it scales the six directional colours "was not checked"; "what the shader does with the fourth component was not read" | Character-Rendering/how-a-character-is-lit.md:212, 228-230 |
| RO.S-29 | `+0x244`/`+0x248`: "What writes the record's five fields, and what the mode and the other two values do in the draw, were not read" | Character-Rendering/how-a-character-is-lit.md:237-238 |
| RO.S-30 | `003AC110`: "its second half was not read line by line"; its caller is "not read and not named" | Character-Rendering/how-a-character-is-lit.md:191-193, 206-207 |
| RO.S-31 | "Nothing here was observed running" | Character-Rendering/how-a-character-is-lit.md:262 |

#### 2.1.3 [RA] The character render record array, render events, focus point and track pick

Short names in this part: **CRR** = `Character-Render-Records/the-character-render-record-array.md`; **RES** = `Character-Render-Records/render-event-selection-evidence.md`; **FOC** = `Character-Render-Records/the-focus-point-of-a-character.md`; **TRK** = `Character-Render-Records/how-a-presentation-entry-picks-its-track.md`.


| id | gap | cite |
|---|---|---|
| RA.S-1 | 15 `UNRESOLVED` tail fields — "What remains open is meaning, not discovery" | Character-Render-Records/the-character-render-record-array.md:1038-1039 |
| RA.S-2 | meaning of the record's constant blocks (ladder +0xA4..+0xBC, reciprocals, `03 03 05 03`) and 333 untouched bytes; carried to "static-FIELDS work" | Character-Render-Records/the-character-render-record-array.md:376-377 |
| RA.S-3 | the five stage bodies "are not read here" | Character-Render-Records/the-character-render-record-array.md:407 |
| RA.S-4 | no setter for +0x290 bits 2,5,24 and +0x294 bits 4,6,10,11,13,14,20 | Character-Render-Records/the-character-render-record-array.md:773-776 |
| RA.S-5 | `+0x348` mid component / range units "Deliberately not claimed" | Character-Render-Records/the-character-render-record-array.md:831-833 |
| RA.S-6 | `004209C0` +0x2E0 vector "what that vector is was not established" | Character-Render-Records/the-character-render-record-array.md:1067-1068 |
| RA.S-7 | what the empty-callback hierarchy walks were for — "cannot learn from this image" | Character-Render-Records/the-character-render-record-array.md:1057-1058 |
| RA.S-8 | `003E1C50` and `0040ED90` effects "remain outside this package" | Character-Render-Records/render-event-selection-evidence.md:460-461 |
| RA.S-9 | meanings of the two vectors `00372280` resets "require their consumers" | Character-Render-Records/render-event-selection-evidence.md:436-437 |
| RA.S-10 | `0041CA70` helper semantics outside the package | Character-Render-Records/render-event-selection-evidence.md:302-303 |
| RA.S-11 | which in-game situations change the focus source | Character-Render-Records/the-focus-point-of-a-character.md:35-36 |
| RA.S-12 | @FRM census; where +0x66C nibbles are decremented; second vector meaning; three sibling getters | Character-Render-Records/the-focus-point-of-a-character.md:105-109 |
| RA.S-13 | command interpreter advancing the cursor; what starts a pending state; state-word values; who raises entry bit 6 | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:163-164 |
| RA.S-14 | what counts +0x5E down | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:137 |
| RA.S-15 | what reads +0x2E8 bits and the factor | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:144-145 |
| RA.S-16 | `0051B970` callbacks not read | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:152-154 |
| RA.S-17 | what kinds of model carry record flag bit 27 | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:109-110 |

#### 2.1.4 [RG] Rig controllers, fades, status looks, bone trails and the staged look

Short names in this part: **FADE** = `Character-Render-Records/how-a-character-fades-the-ten-channels.md`; **STAT** = `Character-Render-Records/how-a-status-shows-on-a-character.md`; **TRAIL** = `Character-Render-Records/the-bone-trails.md`; **RIG** = `Character-Render-Records/the-rig-of-seventeen-controllers.md`; **LOOK** = `Character-Render-Records/the-staged-look-command.md`.


| id | gap | cite |
|---|---|---|
| RG.S-1 | Channel 3 has no writer ("reset to 1.0; no writer in the sweeps"); bounded negative | Character-Render-Records/how-a-character-fades-the-ten-channels.md:87, :449-450 |
| RG.S-2 | What the owner states behind channel 1 are (`+0x284` bit 27, `+0xCC` value 0x35, `+0x40B` bits 0-1) and which kinds 0x11..0x15 / >= 0x1C are | Character-Render-Records/how-a-character-fades-the-ten-channels.md:425-426 |
| RG.S-3 | What `+0x22C` is | Character-Render-Records/how-a-character-fades-the-ten-channels.md:427 |
| RG.S-4 | What bit 14 of `+0x284` and `+0x2CA` mean in the climb; the effect object | Character-Render-Records/how-a-character-fades-the-ten-channels.md:428-430 |
| RG.S-5 | What the three large bodies that read channel 4 alone do with it | Character-Render-Records/how-a-character-fades-the-ten-channels.md:431 |
| RG.S-6 | Attachment slots 0x10A / 0x7FFF; what 0042F4C0, 004215A0, 00426E40 do | Character-Render-Records/how-a-character-fades-the-ten-channels.md:434-435 |
| RG.S-7 | 003CBB30 body and the camera update 003820C0 not read whole | Character-Render-Records/how-a-character-fades-the-ten-channels.md:334-337 |
| RG.S-8 | "The setter's two other callers, both record phases, were not read" (partly answered, see RG.CS-12) | Character-Render-Records/how-a-character-fades-the-ten-channels.md:248 |
| RG.S-9 | Requester 1 of the cull veto: "only the call site was read" | Character-Render-Records/how-a-character-fades-the-ten-channels.md:284 |
| RG.S-10 | Not followed: presentation-entry callbacks under 0042C410 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:272-273 |
| RG.S-11 | What `+0x304` bit 5 does (Stone/Stop): "What the bit does was not read" | Character-Render-Records/how-a-status-shows-on-a-character.md:71 |
| RG.S-12 | What the model variant blocks hold; what pass the model draw (9,695 B) skips for variant 3 | Character-Render-Records/how-a-status-shows-on-a-character.md:107-110, :372 |
| RG.S-13 | Who calls the variant binder's allocator-side routines | Character-Render-Records/how-a-status-shows-on-a-character.md:120-121 |
| RG.S-14 | Curve tables 01F21F40 / 01F22030 values not read | Character-Render-Records/how-a-status-shows-on-a-character.md:146-147 |
| RG.S-15 | Berserk's point: "which point that is was not read" (code 0x100) | Character-Render-Records/how-a-status-shows-on-a-character.md:202-203 |
| RG.S-16 | What sets the second block's `+0x14` | Character-Render-Records/how-a-status-shows-on-a-character.md:272 |
| RG.S-17 | What the shadow draw does with Slow/Immobilize colour and vector; what virtual slot 25 does | Character-Render-Records/how-a-status-shows-on-a-character.md:283-284, :297-298 |
| RG.S-18 | Light selector 003ACC10 read only in part; filler of 02B3F508 | Character-Render-Records/how-a-status-shows-on-a-character.md:313, :349, :373-374 |
| RG.S-19 | Whether anything selects look 12 or second-block index 2 | Character-Render-Records/how-a-status-shows-on-a-character.md:377 |
| RG.S-20 | VU1 program 0053F490 not read; per-vertex ST/RGBAQ values (UQ-213) | Character-Render-Records/the-bone-trails.md:379-384 |
| RG.S-21 | Sibling sampler 003712C0 not read | Character-Render-Records/the-bone-trails.md:117-118, :30 |
| RG.S-22 | Callers of off-only route 0042F250 (handbook loader, 003B8260, 002E35B0) not read | Character-Render-Records/the-bone-trails.md:80-81, :434-435 |
| RG.S-23 | Entry `+0xC` (20.0) has no reader found | Character-Render-Records/the-bone-trails.md:106 |
| RG.S-24 | Which vertex ADC skips, and why | Character-Render-Records/the-bone-trails.md:377 |
| RG.S-25 | Controller 8 unidentified, no enabler; controller 5 trigger and purpose | Character-Render-Records/the-rig-of-seventeen-controllers.md:270-272 |
| RG.S-26 | What lip flap, nod, head shake, Confuse, Immobilize, body shake updates compute | Character-Render-Records/the-rig-of-seventeen-controllers.md:273-276 |
| RG.S-27 | Bit 8 / controller 10 dirty bit "not traced here" | Character-Render-Records/the-rig-of-seventeen-controllers.md:107 |
| RG.S-28 | What the rotators are attached to in shipped models | Character-Render-Records/the-rig-of-seventeen-controllers.md:163-164 |
| RG.S-29 | Hit-flinch handler 00427320: "only the two windows round the enables were read" | Character-Render-Records/the-rig-of-seventeen-controllers.md:141 |
| RG.S-30 | What the look controller and eye object do each frame | Character-Render-Records/the-staged-look-command.md:212 |
| RG.S-31 | Rig fields `+0x58`..`+0x62`; global `02B59D64` | Character-Render-Records/the-staged-look-command.md:214-215 |
| RG.S-32 | Names of request bits 2, 5, 6, 30; bits 5 and 6 have no stager | Character-Render-Records/the-staged-look-command.md:217-218 |
| RG.S-33 | Who reads staged bits 7 and 8 | Character-Render-Records/the-staged-look-command.md:219 |
| RG.S-34 | What 00426220 tests | Character-Render-Records/the-staged-look-command.md:220 |
| RG.S-35 | What the three reset vectors accumulate; what byte +6 selects | Character-Render-Records/the-staged-look-command.md:195-196 |
| RG.S-36 | All five pages: static, nothing observed running | Character-Render-Records/how-a-character-fades-the-ten-channels.md:437; Character-Render-Records/how-a-status-shows-on-a-character.md:378; Character-Render-Records/the-rig-of-seventeen-controllers.md:281; Character-Render-Records/the-staged-look-command.md:221 |

#### 2.1.5 [CL] Ordered render command list and graphics-thread handshake

Short names in this part: **C** = `CONTRACT-render-command-list-and-graphics-handshake.md`; **L** = `Render-Command-List/the-ordered-render-command-list.md`; **H** = `Graphics-Thread-Handshake/the-shared-command-state-word.md`.


| id | gap | cite |
|---|---|---|
| CL.S-1 | Who writes `+0x08` executeTarget: "a bounded census … finds **no writer**" | CONTRACT-render-command-list-and-graphics-handshake.md:460-467, CONTRACT-render-command-list-and-graphics-handshake.md:495 |
| CL.S-2 | What consumes the staging buffers: "the consumer of the staging buffers at `[02F8F2E0]` … was not traced here" | Graphics-Thread-Handshake/the-shared-command-state-word.md:324, CONTRACT-render-command-list-and-graphics-handshake.md:469-471 |
| CL.S-3 | How a walked command list becomes the kicked buffer: "how a walked-and-executed command list becomes the buffer the three publishers kick" | Graphics-Thread-Handshake/the-shared-command-state-word.md:900-903 |
| CL.S-4 | The Tk workers' callback tables were not followed (limit of CG-3) | CONTRACT-render-command-list-and-graphics-handshake.md:472-473, Graphics-Thread-Handshake/the-shared-command-state-word.md:300-301, Graphics-Thread-Handshake/the-shared-command-state-word.md:149 |
| CL.S-5 | Whether the third publisher's guard byte is ever non-zero: "this publisher is **not known to be unreached** rather than known to run" | Graphics-Thread-Handshake/the-shared-command-state-word.md:286-288 |
| CL.S-6 | What bits 2/3 and `0x14D` meant to the backend: "not decidable from this executable" | Graphics-Thread-Handshake/the-shared-command-state-word.md:231-232 |
| CL.S-7 | Runtime validation is empty: "Nothing in this contract has been observed on a running game." | CONTRACT-render-command-list-and-graphics-handshake.md:416 |
| CL.S-8 | Who registers the `0x20`-stride table at `01EF8B00` that triggers ReadPresetDof: "What registers that table is not read here." | Render-Command-List/the-ordered-render-command-list.md:776-779 |
| CL.S-9 | Render-param record: class name (`EA-2`), the map loader's call sites, "the rest of the ~96 unnamed rows" | Render-Command-List/the-ordered-render-command-list.md:846-847, Render-Command-List/the-ordered-render-command-list.md:814-815 |
| CL.S-10 | `+0xEE`: "NOT CLAIMED: that `+0xEE` has no other writer" | Render-Command-List/the-ordered-render-command-list.md:1268-1273 |
| CL.S-11 | `+0x11..+0x17` bound: "a body outside the 129 that holds a command pointer could still address the gap" | Render-Command-List/the-ordered-render-command-list.md:873-875 |

#### 2.1.6 [GP] Gi render commands and the legacy PS2 GS/VIF layer

Short names in this part: **GI** = `Gi-Render-Commands/gi-render-command-family.md`; **TEX** = `Legacy-PS2-GS/texture-mip-local-memory-budget.md`; **VIF** = `Legacy-PS2-GS/the-vif1-vu1-layer.md`.


| # | gap | cite |
|---|---|---|
| GP.S-1 | Command arena: "Not read: whether a caller resets the cursor each frame." (no other R/ page found answering) | Gi-Render-Commands/gi-render-command-family.md:1000 |
| GP.S-2 | DynGeo slots 3-20 semantic names "beyond the shapes above; which caller dispatches each." | Gi-Render-Commands/gi-render-command-family.md:1054-1055 |
| GP.S-3 | "NOT claimed: what the `01F7F4C0` object is beyond the arena anchor" | Gi-Render-Commands/gi-render-command-family.md:1533 |
| GP.S-4 | Opcode 0x25 fields: "Not claimed: that no other route applies a depth bias to the shadow pass. And the level-1 arms 0x01-0x06 were read no further than their first call." | Gi-Render-Commands/gi-render-command-family.md:1484-1485 |
| GP.S-5 | GS replay: "What the flush submits, and how often shipped packets use each mode, is not established." | Legacy-PS2-GS/the-vif1-vu1-layer.md:175-176 |
| GP.S-6 | GIF size: "Not established: what bounds real producers, how the gate byte is initialised, what the callees do with such sizes" | Legacy-PS2-GS/the-vif1-vu1-layer.md:158-159 |
| GP.S-7 | MSCAL fallback: "Not established: when the count is reset in normal play, and whether a stale slot 0 is ever called." | Legacy-PS2-GS/the-vif1-vu1-layer.md:78 |
| GP.S-8 | Callback flag upper bytes: "Not established: what the upper bytes hold in normal play, and whether the flag ever changes a picture." | Legacy-PS2-GS/the-vif1-vu1-layer.md:88 (Legacy-PS2-GS/the-vif1-vu1-layer.md:89-91 narrows it) |
| GP.S-9 | UNPACK admission: "Not established: whether any shipped packet has these values." | Legacy-PS2-GS/the-vif1-vu1-layer.md:98 |
| GP.S-10 | Vertex colour: "which byte is which channel is not established"; "+0x28-+0x2F ... not written ... does not make it padding" | Legacy-PS2-GS/the-vif1-vu1-layer.md:305-306, Legacy-PS2-GS/the-vif1-vu1-layer.md:317 |
| GP.S-11 | "The leaf also stores `01F83578` ... its reader is not traced here." | Legacy-PS2-GS/the-vif1-vu1-layer.md:357 |
| GP.S-12 | "Not read: ... the rest of `0020ED30`'s state selection" | Legacy-PS2-GS/the-vif1-vu1-layer.md:374 |
| GP.S-13 | "Not read here: ... `001DB640`/`001DB660` beyond §2.1a; what `002105C0` measures." | Legacy-PS2-GS/the-vif1-vu1-layer.md:271 |
| GP.S-14 | "Not read here: what any of the seven draws; the eight `02AE92xx` objects type `'j'` reads; whether the two programs a type installs run in one MSCALF each" | Legacy-PS2-GS/the-vif1-vu1-layer.md:518-519 |
| GP.S-15 | GIF values: "says nothing about what the values mean — what an `ST` pair spans, how `RGBAQ` combines with authored colour" | Legacy-PS2-GS/the-vif1-vu1-layer.md:621-623 |
| GP.S-16 | 2D layer: "what the batcher's topology table at `008F80F8` and the four integers of its mode setter select; how `DynGeoTextureInstance` turns a batch into a draw" | Legacy-PS2-GS/the-vif1-vu1-layer.md:711-712 |
| GP.S-17 | UQ-214 residue: "Not claimed: that the `0x2A8`/`0x168` arithmetic is a double buffer ... or what the `+0x8000` names."; GIF-tag discriminator "was NOT run" | Legacy-PS2-GS/the-vif1-vu1-layer.md:821-824 |
| GP.S-18 | GP.G-6: purpose of 1-vs-4 accounting factor — closed as "NO ADMISSIBLE SOURCE", unanswered in fact | Legacy-PS2-GS/texture-mip-local-memory-budget.md:252 |
| GP.S-19 | UQ-212: record names — "Closed for the gate, unanswered in fact." | Legacy-PS2-GS/texture-mip-local-memory-budget.md:253-257 |
| GP.S-20 | GP.G-5 second surface: "That it was the PS2 double buffer's other half is the reading of the reservation, not something the code shows." | Legacy-PS2-GS/texture-mip-local-memory-budget.md:247-249 |
| GP.S-21 | Bracket-flag quad emitter texture name "was not checked" | Legacy-PS2-GS/the-vif1-vu1-layer.md:699 |

#### 2.1.7 [EF] Effect containers, element dispatch and the per-frame element update

Short names in this part: **DISP** = `Effect-File-Formats/effect-element-type-dispatch.md`; **FBF** = `Effect-File-Formats/an-effect-element-frame-by-frame.md`; **EFX** = `Effect-File-Formats/efx-and-efb-effect-containers.md`; **ERM** = `Effect-File-Formats/README.md`; **CAT** = `README.md`.


| id | gap | cite |
|---|---|---|
| EF.S-1 | "The spawner itself was not read here" (`003A8AE0`) - DISP only gives its callers/callee | Effect-File-Formats/an-effect-element-frame-by-frame.md:156, 303 |
| EF.S-2 | "whether the matrix builder `003A2570` normalises it was not read" (EC7-56 adds calls only) | Effect-File-Formats/an-effect-element-frame-by-frame.md:182-183, 274-276, 303-304 |
| EF.S-3 | "What that global holds was not established" (`02064AB0`) | Effect-File-Formats/an-effect-element-frame-by-frame.md:186 |
| EF.S-4 | whose position the stash `02AED5F0` holds - "that page's open runtime item" | Effect-File-Formats/an-effect-element-frame-by-frame.md:131-132 |
| EF.S-5 | type 0x09's default arm `0043EAB0` "this page does not read" | Effect-File-Formats/an-effect-element-frame-by-frame.md:60-61 |
| EF.S-6 | the 56-byte form "51 times image-wide … some members are reached another way (not traced)" | Effect-File-Formats/effect-element-type-dispatch.md:91-92 |
| EF.S-7 | "Not read here: `002D7FC0`, `003B3D20` and `0039D200` …; what `word[02F8F310]` bit 0 means; the body of `00542100` …; the five other types' builders …; what any of the seven microprograms draws" | Effect-File-Formats/effect-element-type-dispatch.md:596-599 |
| EF.S-8 | "`003A3D20`, `003A2C70`" predicates not read (`0024E460` answered, see E3) | Effect-File-Formats/effect-element-type-dispatch.md:606-607 |
| EF.S-9 | "which codes ever reach this leaf in practice" | Effect-File-Formats/effect-element-type-dispatch.md:607-609 |
| EF.S-10 | type 0x05 walk: "`0039B620`, `002F1F40`, `0026EE00` and `004355D0` beyond their roles; what the `+0x1F1` bits mean …; the four resolve-and-branch blocks" | Effect-File-Formats/effect-element-type-dispatch.md:652-653 |
| EF.S-11 | §2.6 "the inner-table subtype selectors, the kind-3/6 arm interiors, and every per-kind helper body" | Effect-File-Formats/effect-element-type-dispatch.md:733-734 |
| EF.S-12 | §2.7 "`0x56`/`0x57`/`0x59` loaders are call-shape only" | Effect-File-Formats/effect-element-type-dispatch.md:784-785 |
| EF.S-13 | "Which loader caller takes the `.mpk` streams is not traced here" | Effect-File-Formats/effect-element-type-dispatch.md:798-799 |
| EF.S-14 | `01F83530` "run-time value in play is still not observed live" | Effect-File-Formats/effect-element-type-dispatch.md:585-586; Effect-File-Formats/efx-and-efb-effect-containers.md:255-256 |
| EF.S-15 | `002F2D60`'s "five subtype arms' field semantics … not claimed" | Effect-File-Formats/effect-element-type-dispatch.md:1053-1054 |
| EF.S-16 | `002F2530` callees "their own bodies were not read" | Effect-File-Formats/effect-element-type-dispatch.md:936 |
| EF.S-17 | `0xB00` count "was not re-walked" | Effect-File-Formats/efx-and-efb-effect-containers.md:54 |
| EF.S-18 | single-chunk fallback `003EE2D0` "not read" | Effect-File-Formats/efx-and-efb-effect-containers.md:112 |
| EF.S-19 | "The write path is not documented here" | Effect-File-Formats/efx-and-efb-effect-containers.md:451, 622-623 |
| EF.S-20 | null-name fields' path - runtime, SD-194 | Effect-File-Formats/efx-and-efb-effect-containers.md:367-370, 378 |
| EF.S-21 | borrowed-context relocation: "no instance of such a move is observed … the list handlers and native subtype effects are not executed" | Effect-File-Formats/efx-and-efb-effect-containers.md:195-197 |
| EF.S-22 | "Any chunk's meaning" beyond 0x600/0x700 | Effect-File-Formats/efx-and-efb-effect-containers.md:606-610 |

#### 2.1.8 [ET] Effect element types, kind-0x54 meshes, menu effect registry and VFX layers

Short names in this part: **mesh** = `Effect-File-Formats/effect-mesh-records-kind-54.md`; **00-0a** = `Effect-File-Formats/the-element-types-00-0a.md`; **40-42** = `Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md`; **60-74** = `Effect-File-Formats/the-element-types-60-74.md`; **80-97** = `Effect-File-Formats/the-element-types-80-97.md`; **menu** = `Effect-File-Formats/the-menu-effect-registry.md`; **six-layers** = `Effect-File-Formats/the-six-vfx-display-layers.md`.


| id | gap | cite |
|---|---|---|
| ET.S-1 | "uncharacterised pass operators (`0043E7B0`/`00434630`/`00434760`/`00396F20`/`00394B70`/`0043E840`) and the clipper `00521450` itself" | Effect-File-Formats/effect-mesh-records-kind-54.md:223-224 (also `:4`) |
| ET.S-2 | `0x800`-chunk class (32,639 sub-records) "not covered by this census beyond the subtype histogram" | Effect-File-Formats/effect-mesh-records-kind-54.md:187-188 |
| ET.S-3 | kind-0x54 figures "were not re-walked and are a lower bound" | Effect-File-Formats/effect-mesh-records-kind-54.md:48-49 |
| ET.S-4 | plain sprite drawer: "its first 0x340 bytes read, the rest skimmed for calls" | Effect-File-Formats/the-element-types-00-0a.md:335 |
| ET.S-5 | "what UV sources 1, 3 and 4 compute, and `00446050`'s exact colour interpolation" (registered GI-14 at :396, not covered by GI-14 section) | Effect-File-Formats/the-element-types-00-0a.md:396, :430 |
| ET.S-6 | point emitter flag dword "from three predicates not read" | Effect-File-Formats/the-element-types-00-0a.md:273 |
| ET.S-7 | "whether any shipped effect uses mode 6 was not checked" | Effect-File-Formats/the-element-types-00-0a.md:284 |
| ET.S-8 | not-read list: `003AA280`'s internals, `003992B0`, `00398030`, … `002F3890`, `003A2900`, `00808C40` | Effect-File-Formats/the-element-types-00-0a.md:350-355 |
| ET.S-9 | 0x71 triple 4: "the colour sets and the t4 < 0 branch `004D6F46` are not traced" | Effect-File-Formats/the-element-types-60-74.md:270 |
| ET.S-10 | 0xAB default block "calling it a state primer is inference" | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:194-195 |
| ET.S-11 | registry: `003B28F0`/`003B2B40` "bodies were not read beyond the type argument"; `003B2CA0` role not read; "A computed call is outside this census" | Effect-File-Formats/the-menu-effect-registry.md:130-131, :136 |
| ET.S-12 | spawn caller `0055F010` "stays unplaced" | Effect-File-Formats/the-menu-effect-registry.md:100, :119 |
| ET.S-13 | what the mode dword means once installed is "the workbench page's unclaimed item" | Effect-File-Formats/the-menu-effect-registry.md:117 |
| ET.S-14 | audio routine `003B3D20` "what that routine plays is not read here" | Effect-File-Formats/the-menu-effect-registry.md:165 |
| ET.S-15 | six layers: lookups for kinds 4,5,6,9; commit step; transform composer; writers of group-enable words; bracket pair; layer-3 routines; state call values; mode getter meaning; callers | Effect-File-Formats/the-six-vfx-display-layers.md:137-140, :250-251 |
| ET.S-16 | who writes the enable words and the two bytes; what raises bit 11 of `020926E4` | Effect-File-Formats/the-six-vfx-display-layers.md:66-67, :111-112 |
| ET.S-17 | order of layers "is the names', not a measurement" | Effect-File-Formats/the-six-vfx-display-layers.md:54-56 |
| ET.S-18 | odd wait loop ("a bit found set on entry would never be seen to clear") | Effect-File-Formats/the-six-vfx-display-layers.md:49-50 |

#### 2.1.9 [MF] Model formats: add-motion tables, ADM, FCP, FDM/FOR

Short names in this part: **SKEL** = `Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md`; **ADM** = `Model-And-Motion-Formats/adm-add-motion-tables.md`; **FCP** = `Model-And-Motion-Formats/fcp-character-parameter-block.md`; **FDM** = `Model-And-Motion-Formats/fdm-and-for-entries.md`; **MREADME** = `Model-And-Motion-Formats/README.md`.


| id | gap | cite |
|---|---|---|
| MF.S-1 | "Not claimed: what is drawn (nothing found hides the base model), and the run-time order of the `bindp2` / `bindh` calls." | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:221 |
| MF.S-2 | "Whether `1570` is a story-progress value in the units the flag banks use — the number is read, the scale is not." | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:300-301 |
| MF.S-3 | `0037CCC0` read only "to the pair loop's end"; `00372820` and `003703A0` only partly read (◐) | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:136-139 |
| MF.S-4 | "Still open: who consumes the second triple (dead to the sole traced consumer), and what the group header's other floats mean." | Model-And-Motion-Formats/adm-add-motion-tables.md:194-195 |
| MF.S-5 | `002E7CE0` "What that value is was not established." | Model-And-Motion-Formats/adm-add-motion-tables.md:154 |
| MF.S-6 | "what the allocator `00210EC0` does with a saturated size is not read" | Model-And-Motion-Formats/adm-add-motion-tables.md:121 |
| MF.S-7 | Section-8 packet: "What the packet looks like on screen is not read." | Model-And-Motion-Formats/fcp-character-parameter-block.md:732 |
| MF.S-8 | Rig controllers: "what each controller's record holds. Those are the rig page's own unknowns" | Model-And-Motion-Formats/fcp-character-parameter-block.md:391 |
| MF.S-9 | Section 10: "The remaining 42 bytes of the 48 … have no reader" | Model-And-Motion-Formats/fcp-character-parameter-block.md:770-771 |
| MF.S-10 | Section header `+0x04`, `+0x0C`: "no reader found by the tag scan" | Model-And-Motion-Formats/fcp-character-parameter-block.md:186 |
| MF.S-11 | "what the VU1 program does with the pair is not established (no microcode read)" | Model-And-Motion-Formats/fdm-and-for-entries.md:302-303 |
| MF.S-12 | "Which file the partner index names is inferred from that fit, not traced." | Model-And-Motion-Formats/fdm-and-for-entries.md:193-194 |
| MF.S-13 | "Not established here: which of those commands run in play, and whether each `w2` is present in the table of the entity it reaches." | Model-And-Motion-Formats/fdm-and-for-entries.md:312-313 |
| MF.S-14 | `@FDM` descriptor "`+0x0A` / `+0x0B` unread there" | Model-And-Motion-Formats/fdm-and-for-entries.md:229 |
| MF.S-15 | `.nmb` "is the most tractable unknown"; no sheet | Model-And-Motion-Formats/README.md:48-50 |
| MF.S-16 | "These may belong to 04-Actor-Entity rather than 17-Presentation; a sheet decides that" | Model-And-Motion-Formats/README.md:52-53 |

#### 2.1.10 [MM] Motion formats: FEF/motion entries, FRP, FTE/FCT, FTR, oscillator, pose sequencer

Short names in this part: **ACH** = `Authored-Commands/the-authored-presentation-command-handlers.md`.


| # | gap | cite |
|---|---|---|
| MM.S-1 | "What the target-bearing arm's run_r_* looks like against the target, which is a visual question." | Model-And-Motion-Formats/fef-and-motion-entries.md:771 |
| MM.S-2 | which `@FEF` models a session loads is runtime-only ("which a session loads is content") | Model-And-Motion-Formats/fef-and-motion-entries.md:751 |
| MM.S-3 | `@FMW` arm-0 record shapes "are a read attribution"; corpus control "(subagent, not re-run)"; skinning non-inheritance/`+0x1E0`/`+0x6C0` "are read attribution" | Model-And-Motion-Formats/fef-and-motion-entries.md:598-600, :608-609, :697-699 |
| MM.S-4 | "Runtime-only: whether two such models are ever drawn while both are bound, and what the second one then shows." | Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:242-243 |
| MM.S-5 | variant-1 layout reason and alignment policy are declared limits (build tooling); ownership "provisional" | Model-And-Motion-Formats/frp-object-container.md:307-313, :325-333 |
| MM.S-6 | bit 29's value: "SD-195, NO ADMISSIBLE SOURCE" | Model-And-Motion-Formats/ftr-node-table.md:254-256, :282-283 |
| MM.S-7 | "What each controller's record holds is the open section 7 of the rig page" | Model-And-Motion-Formats/ftr-node-table.md:179-181 |
| MM.S-8 | heavy stages `0040FF30`/`00413C80`/`00411650`/`0040B780` "read at head + call-shape level only … the per-sub-entry math is not walked" | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:186-189, :315-316, :352-355 |
| MM.S-9 | GI-19 not established: names of C, D, F, G, H, I and A/B targets; whether the bone-supplying resource entry is the rig's; `0040EEA0`'s second host `0054A9C0` | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:430-434 |
| MM.S-10 | entry `+0x08`: "the +0x28 / +4 reading is not reconciled here" | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:94 |
| MM.S-11 | preset 7 "would read unrelated data; whether any field's weather record carries 7 was not censused" | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:271-272 |
| MM.S-12 | "Not read: the two routines the draw-side copy hands its descriptor and coordinates to; the rest of the three raisers …; … the 571-byte 004778D0 …; the random picker; the rest of the pose applier." | Model-And-Motion-Formats/the-pose-sequencer.md:206-208 |
| MM.S-13 | rectangle head "+2, +4, +8 three more words that feed the copy descriptor; not decoded" | Model-And-Motion-Formats/the-pose-sequencer.md:125 |

#### 2.1.11 [PP] Post-processing and visual tuning parameters

Short names in this part: **CS** = `Post-Processing/CONTRACT-post-processing-subsystem.md`; **CP** = `Post-Processing/CONTRACT-ppfx-effect-creation.md`; **PI** = `Post-Processing/ppfx-function-identification.md`; **CAT** = `Post-Processing/the-post-processing-effect-catalogue.md`; **VR** = `Visual-Tuning-Parameters/README.md`; **RR** = `Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md`; **RCL** = `Render-Command-List/the-ordered-render-command-list.md`; **HL** = `Post-Processing/members/ppfx-handle-layout.tsv`.


| id | gap | cite |
|---|---|---|
| PP.S-1 | Which techniques `ApplyEffects` runs for a given configuration (UQ-227 PARTIAL) | Post-Processing/CONTRACT-post-processing-subsystem.md:260-261; Post-Processing/the-post-processing-effect-catalogue.md:984, Post-Processing/the-post-processing-effect-catalogue.md:1039-1041 |
| PP.S-2 | What steps 1, 3, 4 and 6 configure; API names not in image | Post-Processing/CONTRACT-post-processing-subsystem.md:262; Post-Processing/the-post-processing-effect-catalogue.md:986 |
| PP.S-3 | Which float the map loader passes at `+0x11C`; the computed focus pair's meaning; whether a zone-script verb writes the block | Post-Processing/CONTRACT-post-processing-subsystem.md:151-154 (Render-Command-List/the-ordered-render-command-list.md:1925 names `EnableDofObj`/`SetDofObj` commands, not traced to the block) |
| PP.S-4 | For I-3 features other than motion blur, whether `ApplyEffects` reaches them by another test | Post-Processing/CONTRACT-post-processing-subsystem.md:192-193, Post-Processing/CONTRACT-post-processing-subsystem.md:267-268; Post-Processing/the-post-processing-effect-catalogue.md:1036-1038 |
| PP.S-5 | Nothing observed live | Post-Processing/CONTRACT-post-processing-subsystem.md:269; Post-Processing/CONTRACT-ppfx-effect-creation.md:228-233 |
| PP.S-6 | Whether a registration helper / lookup can fail and what follows | Post-Processing/CONTRACT-ppfx-effect-creation.md:237-238, Post-Processing/CONTRACT-ppfx-effect-creation.md:306 |
| PP.S-7 | What the vtable step at `0072D8D9` is | Post-Processing/CONTRACT-ppfx-effect-creation.md:239-240 |
| PP.S-8 | Total handle count: loop bounds of `0072DFD0`, `0072DAC0`, `0072E5B0`, `0072EC00` | Post-Processing/CONTRACT-ppfx-effect-creation.md:241-243 |
| PP.S-9 | No teardown/unwind for partial registration | Post-Processing/CONTRACT-ppfx-effect-creation.md:141, Post-Processing/CONTRACT-ppfx-effect-creation.md:171 |
| PP.S-10 | What the reset arm destroys and who sets `+0x99` | Post-Processing/the-post-processing-effect-catalogue.md:814 |
| PP.S-11 | `0072DFD0` body not read | Post-Processing/the-post-processing-effect-catalogue.md:806 |
| PP.S-12 | What lies between handle runs | Post-Processing/the-post-processing-effect-catalogue.md:803 |
| PP.S-13 | What the Glare-off `(1.0, 0.0)` pair does to the passes ("an inference") | Post-Processing/the-post-processing-effect-catalogue.md:971-974 |
| PP.S-14 | Platform switch `0065E580(wrapper,1)` not read | Post-Processing/the-post-processing-effect-catalogue.md:1045 |
| PP.S-15 | `EAPERTUREFM_*` members other than `_DISC` not in image | Post-Processing/ppfx-function-identification.md:191-217 |
| PP.S-16 | 545-string / 20-pattern figure not reproducible | Post-Processing/ppfx-function-identification.md:390-393 |
| PP.S-17 | 15 multi-claimed name rows unresolved | Post-Processing/ppfx-function-identification.md:600-605 |
| PP.S-18 | Per-technique semantics: zero shader bodies read (UQ-223 superseded as population) | Post-Processing/the-post-processing-effect-catalogue.md:797-799 |
| PP.S-19 | Fade arithmetic for flying-fade pair not decompiled | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:402 |
| PP.S-20 | OV-42: softEdges F4 premise, loaded-list identity, whether the resource loads, pointers/lifetime/aliasing, other two binder routes | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:791-794 |
| PP.S-21 | Numeric formula for any tuning parameter not asserted | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:284-285, Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:443-444 |
| PP.S-22 | `0059E070` Vignette blocks elided; §3 bodies declared unread (W-7) | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:242, Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:251-252, Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:446-447 |
| PP.S-23 | 44 authored keys with no reader; composed families may move keys | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:663-665, Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:751-753 |
| PP.S-24 | Which targets carry the `+0xC` bit 1 (residue of W-5 narrowing; answered as "no Inverted pass draws") | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:354-360 |

#### 2.1.12 [CM] Scripted camera, screen fade, screen effects, aspect fit, position-to-scalar, movie index

Short names in this part: **MR** = `Movie-Containers/README.md`; **MH** = `Movie-Containers/mh-movie-seek-index.md`; **PTS** = `Position-To-Scalar/how-a-position-becomes-a-single-number.md`; **SF** = `Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md`; **AF** = `Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md`; **CI** = `Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md`; **CR** = `Scripted-Camera/how-a-camera-reaches-the-renderer.md`; **P** = `Scripted-Camera/the-scripted-camera-player.md`; **RM** = `README.md`; **WT** = `../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`.


| # | gap | cite |
|---|---|---|
| CM.S-1 | "which codecs this build accepts, at what resolutions, and what it does with a file it cannot decode — none of which the spec answers" (no later page answers it) | Movie-Containers/README.md:12-14 |
| CM.S-2 | `.mh` `+0x04`, `+0x06`, entry flags meaning: "OUT OF EVIDENCE BOUNDARY ... The residue stays unanswered in fact" (UQ-222 / MH-1) | Movie-Containers/mh-movie-seek-index.md:192-194, 201-205 |
| CM.S-3 | width/height reading of `+0x08`-`+0x10` "is still an inference from the values, not from a consumer" | Movie-Containers/mh-movie-seek-index.md:81-82, 194-195 |
| CM.S-4 | `02AEEA20` "**what it holds in play was not tested**"; all live readings title-screen only | Position-To-Scalar/how-a-position-becomes-a-single-number.md:224-225, 119-121; Position-To-Scalar/how-a-position-becomes-a-single-number.md:4 |
| CM.S-5 | `BI-9` "is not answered — the in-world observation is still the one that would settle it" | Position-To-Scalar/how-a-position-becomes-a-single-number.md:158-160 |
| CM.S-6 | "What kind `0x40` is in authoring terms was not established" | Position-To-Scalar/how-a-position-becomes-a-single-number.md:353-354 |
| CM.S-7 | who sets container bit 5 "was not traced" | Position-To-Scalar/how-a-position-becomes-a-single-number.md:361 |
| CM.S-8 | `UQ-237` residue: "what the stem is *used for* after `001DA290` computes it, and what `[obj+0x7C]` counts" | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:319-320 |
| CM.S-9 | `0035CA70` helper bodies `002DED60`, `00360C20`, `00361630`, `00303D90`, `003C58B0` "**not read** ... which transition the machine sequences ... is left open" (00360D70/00360E50 read later, see E3) | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:177-180 |
| CM.S-10 | `MapIndex` step: "What the `MapIndex` step then triggers is the harness's business" | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:277-278 |
| CM.S-11 | "What each code's movie shows" | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:687-688 |
| CM.S-12 | DXGI `Format`/`ScanlineOrdering`/`Scaling` "rest on the layout match"; "the swap chain must take its format from elsewhere"; census limit (pointer reloaded elsewhere escapes) | Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:116-117, 141-142 |
| CM.S-13 | kinds 2, 5, 6, 7, 0x0D: what they draw; returns of kinds 3, 5, 7 not read | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:254-256, 95, 163-164 |
| CM.S-14 | contents of the three mask tables and three line textures | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:257 |
| CM.S-15 | why `0024D540` is called with 0 from the menu frame and capture-backed frame | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:258-260 |
| CM.S-16 | preset constants: "*What each constant means to the kind's handler was not read*" | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:183-184 |
| CM.S-17 | `0024E910`'s called resets and owner of the fourth target `020926D0` "were not read"; `003DE210`'s third caller "not read" | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:231-232, 222-223 |
| CM.S-18 | keeper of block-address table `0209E6C0` "was not read" | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:104-105 |
| CM.S-19 | soft focus in other language builds; on-screen look | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:261-262 |
| CM.S-20 | the "shared predicate" of submit and "whose vectors override the submitted camera" | Scripted-Camera/how-a-camera-reaches-the-renderer.md:43-45, 336 |
| CM.S-21 | "what the second field-of-view float is for was not established" | Scripted-Camera/how-a-camera-reaches-the-renderer.md:93 |
| CM.S-22 | what `001824E0`'s device method does, the Movement object of the tail, and what `0024E180` does with `02AEDD30` (SWE2 note at Scripted-Camera/how-a-camera-reaches-the-renderer.md:476 lists callees only) | Scripted-Camera/how-a-camera-reaches-the-renderer.md:333-335 |
| CM.S-23 | `02089350` meaning; how often `0037D970` runs; per-frame invocation count of `00314370` | Scripted-Camera/how-a-camera-reaches-the-renderer.md:198-200, 266-269 |
| CM.S-24 | "the curve evaluator the loader calls"; `camerashakechange` / `camerashakeratio` / sync verbs; bank entry layout beyond data id | Scripted-Camera/how-a-camera-reaches-the-renderer.md:286, 318-319 |
| CM.S-25 | skip flag `byte +0x201` "its setter was not traced" | Scripted-Camera/the-scripted-camera-player.md:135 |
| CM.S-26 | frame step `02B4E4B0` "(not traced)" | Scripted-Camera/the-scripted-camera-player.md:355 |
| CM.S-27 | 5.0 vs 1.0 look-at distance observability "NOT established" | Scripted-Camera/the-scripted-camera-player.md:617-619, 743-745 |
| CM.S-28 | which cutscenes set attachment bits 9 and 10 (data question) | Scripted-Camera/the-scripted-camera-player.md:606-607 |
| CM.S-29 | BY-6: "how often play queries such a path or what the camera shows" | Scripted-Camera/the-scripted-camera-player.md:583 |

### 2.2 Structural gaps found while mapping (a port needs these and no page states them)

A function, formula, format, field, initial value or ordering that a re-implementation needs and that no 17-Presentation-Rendering page states. Ids are `<part>.G-n`.

#### 2.2.0 Category-wide structural gaps

These are the gaps that cut across parts. Each is stated in the part tables below; they are drawn together here because
no single page owns them.

| id | what is missing | why a port needs it | where the gap shows |
|---|---|---|---|
| X.G-1 | **One frame order for the category.** Each part orders its own steps, but no page places the character update pipeline (`003323D0` → `00426090`), the authored-command drains, the pool promote/retire, the effect update and walk, the ordered-list walks inside the render pass `00187950`, the Gi drain and reset, the post-processing steps and the graphics-thread handshake against one another. | State seen by each consumer depends on it; double-tick and teardown cases (`0022B8C0`, `01FD4A88`) already show the order matters. | AC.G-6, RO.G-6, RA.G-2, RG.G-1, CL.G-4, CL.G-8, CL.G-15, GP.G-7, EF.G-19, ET.G-19, MF.G-20 |
| X.G-2 | **The D3D11 device interface.** `PrimitiveRendererD3D11` is identified and its slot addresses listed, but almost none of the slot semantics are stated, and the slots each Gi command calls are disputed (GP.CV-1). | Every Gi command, and every ordered-list class that draws, ends in this device. | GP.G-2, GP.CV-1 |
| X.G-3 | **Execute bodies of the render command classes.** 8 of 36 enqueue classes have a described execute body; allocation sizes are known for 19. | Without them nothing is drawn. | CL.G-1, CL.G-2, CL.G-13 |
| X.G-4 | **The VU1 microprograms** (recompiled bodies) behind bone trails, effect types, `@FDM` draws and the oscillator stages are characterised by primitive or call shape only. | The per-vertex output of these paths cannot be written. | GP.G-9, RG.S-20, MF.S-11, MM.G-11, MM.G-13 |
| X.G-5 | **Shared track evaluators.** `004309C0` / `004314E0` / `0042FDB0` are sampled by every effect element and tail, but the track record format and the interpolation between keys are not stated. | All effect motion and colour. | EF.G-6, ET.G-7 |
| X.G-6 | **Frame-rate globals.** `01DFE0B4`, `01DFE0B8` and `01DFE0BC` are read side by side across parts with disputed widths, values and roles (AC.CV-6, RA.CV-10, RG.CV-11, RG.CV-15), and no page states their writer sequence and relation in one place. | Every timer, ramp and fade that is scaled by frame rate. | RG.G-13, RA.G-1, AC.CV-6 |
| X.G-7 | **`@FRM` motion data and the WebM movie path** are bound or opened but never decoded. | Character motion and movie playback. | MM.G-3, CM.G-1 |

#### 2.2.1 [AC] Authored commands, ramp channels and the coast-down latch

| # | what is missing | why a port needs it | where |
|---|---|---|---|
| AC.G-1 | Which callee the `0x09` invoker uses when "Type 1 also hands six floats and a count to the ramp-channel object `+0x35C`". The ramp contract has `003B5D40` with one caller `0041D560`, and "No authored-command class … writes" channel +0x43 | the fifth channel's writer set and the cross-fade start | Authored-Commands/the-authored-presentation-command-handlers.md:792-794 vs CONTRACT-authored-command-ramp-channels.md:195-197 |
| AC.G-2 | The link from `PresentationEntry_RebuildAndFastForwardToTime` to `003B5D40`: §8 says it "reaches it through `003B5D40`", but `003B5D40`'s only caller is `0041D560`, and no 0041D820→0041D560 edge is stated | call graph for fast-forward | CONTRACT-authored-command-ramp-channels.md:300-301 vs :197 |
| AC.G-3 | Per-site argument (4 or 6) of the five `003B6930` calls: "on"/"off" is used without saying whether on means shown or hidden. 003B8670's "on" range contains the `r12d` site | gate polarity per driver | CONTRACT-authored-command-ramp-channels.md:179-182, :409-410 |
| AC.G-4 | No field written to by `003B6900` (the V1 verb `V1(h,6)`/`V1(h,4)`), and no writer of the per-slot `+0x41` pause/hide byte named. Only the allocator writes it in the TSV | the per-slot hide/pause cannot be driven | CONTRACT-authored-command-ramp-channels.md:702, :715-716; ramp-channel-record-accesses.tsv (0x41w only in 003B56D0) |
| AC.G-5 | `0042F030` "the ramp tick `00426090` calls" (global `02CA48F8`): a second ramp in the same pass with no object or layout | frame-pass completeness | CONTRACT-authored-command-ramp-channels.md:956 |
| AC.G-6 | When in the frame the command drains (`0041DA90`/`0041E000`/`0041E1D0`) and the draw stage gate `00428E40` run, relative to the ramp tick | ordering of set vs advance vs draw | Authored-Commands/the-authored-presentation-command-handlers.md:31-34; CONTRACT-authored-command-ramp-channels.md:657-667 |
| AC.G-7 | Bank capacity vs id range: the bank is 0x258 bytes = 75 slots (0x00–0x4A), but ids clamp to 0x4B and "76 ids". Slot 0x4B would be `02CA4668` (the context pointer). The page only says the 0x49–0x4B invokers are NULL ("call 0") | out-of-range id behaviour | Authored-Commands/the-authored-presentation-command-handlers.md:35-36, :48, :64-65, :72-73, :239 |
| AC.G-8 | Complete initial values of a V1 slot set by `003B56D0`. The page says only "sweep ends at +0x9C" (contradicted by the TSV). `003B67F0` gives the 1.0 defaults for some fields | a port must zero/seed each field | CONTRACT-authored-command-ramp-channels.md:201, :473-474, :881 |
| AC.G-9 | Handler bodies described only by callee name or touched field: 0x12 (`003E6DA0`/`003E29F0`), 0x19 (`0046CC70`, 1,069 B; no effect stated, though 0x29 says footstep sound), 0x1E (`003E6A20`), 0x1F (`003E6710`), 0x23 (`004293C0`; `+0x20`/`+0x40`) | handler semantics | Authored-Commands/the-authored-presentation-command-handlers.md:89, :95, :98-99, :102, :243-244 |
| AC.G-10 | `00520100` when `word[rcx+6] != -1`; `00520010`'s per-step work; the `01EFFAF0` flag semantics beyond the `0x10\|0x14` path and bit 4/end-of-track | the submit wrapper and the flag path | Authored-Commands/the-authored-presentation-command-handlers.md:66-67, :124, :126, :264 |
| AC.G-11 | The §12 reproduction formula omits the §7a tail, which §16 says "must" be implemented. The tail is given only as asm fragments; which subtypes reach `speed scale := 1.0f` vs the 0.9 path is ambiguous | the full outcome set | CONTRACT-coast-down-latch.md:152-166, :307-339, :537-538 |
| AC.G-12 | `00424230`'s relation to `00424080` and who calls it; `0041C760`'s role | the stated "permissive default" cannot be placed | CONTRACT-coast-down-latch.md:223-227 |
| AC.G-13 | Initial values of +0x610–+0x62C (who seeds the motion blocks and the latch bit) | first-call behaviour | CONTRACT-coast-down-latch.md:54-62 (no initialiser named) |
| AC.G-14 | What `+0x456` (the sibling counter) gates | the pair reset is required but the second counter's reader is not named | CONTRACT-coast-down-latch.md:279-282 |
| AC.G-15 | `003B5C00`'s channel set (four vs five) and order are not given as code | the fast-forward path | CONTRACT-authored-command-ramp-channels.md:225, :860 (see AC.CV-3) |

#### 2.2.2 [RO] Render-record pool, character render object, transform publish and lighting

Short names in this part: **POOL** = `CONTRACT-render-record-pool-lifecycle.md`; **CRO-C** = `CONTRACT-character-render-object.md`; **PUB** = `CONTRACT-character-transform-publish.md`; **CRO** = `Character-Rendering/character-render-object.md`; **LIT** = `Character-Rendering/how-a-character-is-lit.md`.


| id | what is missing | why a port needs it | where it shows |
|---|---|---|---|
| RO.G-1 | `00420480` record initializer: its parameters (`r9d` + stack "flags") and what it writes. Only `+0x284 = 0x2010F9` is stated | allocate cannot be written without it | CONTRACT-render-record-pool-lifecycle.md:51, 147-148, 460 |
| RO.G-2 | Who sets `+0x284` **bit 2** (the "live" bit release tests). The initializer value 0x2010F9 has bit 2 clear | release's path choice depends on it | CONTRACT-render-record-pool-lifecycle.md:271, 460 |
| RO.G-3 | Initial value of tail `+0x30`/`+0x48830`. The ctor's list (CONTRACT-render-record-pool-lifecycle.md:152-156) omits it; its only writer is `00426480` | allocate passes it to `00420480` on every call | CONTRACT-render-record-pool-lifecycle.md:181, 816-818 |
| RO.G-4 | Values written to tail `+0x40`, `+0x4C..+0x70` ("The tuning block follows") | the constructor | CONTRACT-render-record-pool-lifecycle.md:155, 533 |
| RO.G-5 | Effects of `0041FCF0`, `003E68E0`, `0042C410`, `0042F4C0`, `004200A0`, `00422D50`, `00426EC0` on the record (only one-line roles) | promote/retire/release semantics | CONTRACT-render-record-pool-lifecycle.md:600, 1161-1167, 1199 |
| RO.G-6 | When in the frame `00428710` and `00427C90` run (who calls them, apart from the teardown) | the visibility boundary downstream depends on it | CONTRACT-render-record-pool-lifecycle.md:442-444, 1450 |
| RO.G-7 | `0041F730` full default map ("~100 stores") is given only by example | reset/allocate | CONTRACT-render-record-pool-lifecycle.md:853-856 |
| RO.G-8 | The 0x740 record's tree links (`+0x06` parent, `+0x08` child, `+0x0A` sibling) are not in POOL's §3 link table, which lists only `+0x00/+0x02/+0x04` | retire's drain and the hierarchy walk use them | CONTRACT-render-record-pool-lifecycle.md:76, 236, 848; Character-Rendering/character-render-object.md:885-886 |
| RO.G-9 | Slot 2 setup (2,328 B): no step list apart from the latch write and the two binder calls | the object cannot be initialised | Character-Rendering/character-render-object.md:135, 454 |
| RO.G-10 | Bodies of slots 19 (3,397 B), 24 (547 B), 26 (812 B), 30 (488 B) and of `001F5D70` (the draw): only roles. BB-1's per-method table lives in a candidate README | the draw path | Character-Rendering/character-render-object.md:152, 157, 159, 163, 314-322 |
| RO.G-11 | Field meanings `+0x480..+0x498` (incl. `+0x488`, `+0x490`), `+0x4A4`, `+0x4B0`, `+0x4B5`, `+0x4B6..+0x4BC`, `+0x644`, `+0x654`, `+0x664`; the vector element types at `+0x08` and `+0x390` | setters exist with no semantics | Character-Rendering/character-render-object.md:144, 209-221 |
| RO.G-12 | 0x318 binding record: slot `+0x238` (index 65) has no row in the slot TSV; record bytes `+0x18..+0x2F` not described | the binder writes a contiguous run `+0x30..+0x310` | TSV check (A); Character-Rendering/character-render-object.md:463 |
| RO.G-13 | What slot 16 passes to slot 13 (index, flag, scalars, three matrix sources) | the publish inputs | Character-Rendering/character-render-object.md:338-344; CONTRACT-character-transform-publish.md:343-347 |
| RO.G-14 | The `{object, 3}` countdown: who decrements it and slot 3's teardown trigger | object recycling | Character-Rendering/character-render-object.md:345-346, 398, 419 |
| RO.G-15 | UpdateViewParameters inputs: `[001EBA40()]+0x118` flag and `001EC560()` result have no meaning; param block layout beyond `+0x64..`, `+0xC0..+0xD0` | the formula | Character-Rendering/character-render-object.md:259, 271 |
| RO.G-16 | `001F89E0` ResetState: full write list given only as an EC7 one-liner ("`+0x4B5`=`0x101`", word at a byte field) | the acquire-on-hit path resets with it | Character-Rendering/character-render-object.md:392-393, 1147 |
| RO.G-17 | Light pool: free-entry criterion, the counter `[02B3F504]` initial value and wrap; the light free routine | lights are created and freed | Character-Rendering/how-a-character-is-lit.md:47-50, 392 |
| RO.G-18 | The gather's ordering routines ("two ordering routines", "runs of falling priority") are described by role only; the algorithm is on the status page | the six-light cut | Character-Rendering/how-a-character-is-lit.md:137, 192, 290-292 |
| RO.G-19 | Writers of record `+0x5D0/+0x5DC/+0x5E0/+0x5EC` (ambient mode, light scale) | ambient mode / scale | Character-Rendering/how-a-character-is-lit.md:113-114, 130 |
| RO.G-20 | The relation (if any) between the light pool (`[02B3F528]`, 128 × 0x70) and the 32 × 0x70 table at `02B3F570` used for record `+0x118` | adjacent globals, same stride; not stated | Character-Rendering/how-a-character-is-lit.md:47; CONTRACT-render-record-pool-lifecycle.md:249, 1175 |
| RO.G-21 | Kind-2 "space 1" stores the negated position into "the light's own direction field": offset not given | point-light port | Character-Rendering/how-a-character-is-lit.md:153-154 |

#### 2.2.3 [RA] The character render record array, render events, focus point and track pick

Short names in this part: **CRR** = `Character-Render-Records/the-character-render-record-array.md`; **RES** = `Character-Render-Records/render-event-selection-evidence.md`; **FOC** = `Character-Render-Records/the-focus-point-of-a-character.md`; **TRK** = `Character-Render-Records/how-a-presentation-entry-picks-its-track.md`.


| id | missing | why a port needs it | where |
|---|---|---|---|
| RA.G-1 | Focus countdown reload at FrameLimit=60: reload is "8 x the frame-rate multiplier" into a 4-bit nibble; at multiplier 2 that is 16 > 15 — overflow behaviour not stated | slide timing at 60 fps | Character-Render-Records/the-focus-point-of-a-character.md:67-71, :76 |
| RA.G-2 | Bodies of `RenderSystem_UpdateCharacterRecords` (`00426090`) beyond two calls, and of `0042ED60` call order relative to `00426090` within a frame | frame ordering | Character-Render-Records/the-character-render-record-array.md:637-639, :648-651, :721-723 |
| RA.G-3 | Stage bodies `004264A0`, `00428E40`, `0041E4D0`, `00425DC0`, `00426500` | the draw itself | Character-Render-Records/the-character-render-record-array.md:407 |
| RA.G-4 | 52 handler semantics given only as "distinctive leaf call" (TSV) — e.g. `0042AC30` "+0x124/+0x254/+0x304 field refresh" | dirty protocol effects | Character-Render-Records/the-character-render-record-array.md:778-797 |
| RA.G-5 | `0042A580` returns an uninitialised stack dword used as a rebuild flag — a port must pick a value | determinism | Character-Render-Records/the-character-render-record-array.md:790 |
| RA.G-6 | Selector objects' rules (`01F000A0` table) — not on these pages (partly on the handlers page) | track choice | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:101-103 |
| RA.G-7 | Payload `+0x2C8` vs `+0x0C` bit-12 consumers (see RA.CV-8) not reconciled | entry update passes | Character-Render-Records/render-event-selection-evidence.md:76; Character-Render-Records/how-a-presentation-entry-picks-its-track.md:38, :152-154 |
| RA.G-8 | `0041F340` per-@FLD-entry fill, `0041E500` lookup, `003697C0(6)` post: named, not described | bind / refresh | Character-Render-Records/the-character-render-record-array.md:376, :650-651 |
| RA.G-9 | `0042C410` interior only sketched by callee counts | tail commit | Character-Render-Records/the-character-render-record-array.md:734 |
| RA.G-10 | `003B5980` LOD clamp constants `[low, 1.0]` — `low` value not stated | shadow LOD | Character-Render-Records/the-character-render-record-array.md:712 |
| RA.G-11 | `0051F240` mode 0 vs 1 table provider for the concrete root is kind 1; tagged-handle semantics deferred to another page | lookup | Character-Render-Records/render-event-selection-evidence.md:41-43 |
| RA.G-12 | Initial values of focus fields +0x660..+0x6A8 not stated (only implied by ResetDefaults memset) | first-frame slide | Character-Render-Records/the-focus-point-of-a-character.md:67-71; Character-Render-Records/the-character-render-record-array.md:376 |

#### 2.2.4 [RG] Rig controllers, fades, status looks, bone trails and the staged look

Short names in this part: **FADE** = `Character-Render-Records/how-a-character-fades-the-ten-channels.md`; **STAT** = `Character-Render-Records/how-a-status-shows-on-a-character.md`; **TRAIL** = `Character-Render-Records/the-bone-trails.md`; **RIG** = `Character-Render-Records/the-rig-of-seventeen-controllers.md`; **LOOK** = `Character-Render-Records/the-staged-look-command.md`.


| id | what is missing | why a port needs it | where |
|---|---|---|---|
| RG.G-1 | Relative order, inside one frame, of the status push, the dirty-state pass, the distance-fade phase, the animation-presentation phase (stepper), the root/child frames, the rig frame and the trail update | the fade stepper, the composite and the cull all touch the same channels; one frame of lag changes visuals | Character-Render-Records/how-a-character-fades-the-ten-channels.md:72, :233; Character-Render-Records/the-rig-of-seventeen-controllers.md:117, :228; Character-Render-Records/the-bone-trails.md:126 |
| RG.G-2 | 0041E960 writes `+0x2E0..+0x2EC` (one is a factor of the final opacity) from an "SSE web" and "three global-byte constants" with no formula | `+0x2EC` scales every character's opacity | Character-Render-Records/how-a-character-fades-the-ten-channels.md:644-651, :154 |
| RG.G-3 | `+0x22C` writer and value | factor of final opacity | Character-Render-Records/how-a-character-fades-the-ten-channels.md:154, :427 |
| RG.G-4 | 003E4DD0 described two ways (horizontal extents vs "a fade-channel weight", mode-dispatched product incl. `[r8+0x118]`) - the radius formula for the behind-test depends on it | cull bit 3 | Character-Render-Records/how-a-character-fades-the-ten-channels.md:305, :560 |
| RG.G-5 | 0042E1F0 has no caller / schedule stated | when channel 1 is re-applied each frame | Character-Render-Records/how-a-character-fades-the-ten-channels.md:85, :108 |
| RG.G-6 | Data meanings of the four root-frame side-object scalars: `003AFD80` vector "from +0x160, +0x260..+0x268 and +0x278" with no formula for the middle component | shadow scaling | Character-Render-Records/how-a-character-fades-the-ten-channels.md:372-374 |
| RG.G-7 | Shadow `+0x44` input: "a value from the record times +0x278" - which value not stated | shadow quad scale | Character-Render-Records/how-a-character-fades-the-ten-channels.md:370-371 |
| RG.G-8 | Viewer-inside test uses "the body's band" for height - band bounds not given | channel 4 trigger | Character-Render-Records/how-a-character-fades-the-ten-channels.md:89 |
| RG.G-9 | Distance fade "normalised distance left" - exact normaliser (clip distance, range, near) not written as a formula | channel 0 target | Character-Render-Records/how-a-character-fades-the-ten-channels.md:84 |
| RG.G-10 | Composite scalar sibling `003E4780`: caller-supplied factor, callers not stated | | Character-Render-Records/how-a-character-fades-the-ten-channels.md:155 |
| RG.G-11 | Status unit accessor described only by role; how the unit is found from record `+4` / `+0x108` | push input | Character-Render-Records/how-a-status-shows-on-a-character.md:57, :167, :417-418 |
| RG.G-12 | Light creation `003AB960` "its head read" only; light release routine by role | creating/releasing status lights | Character-Render-Records/how-a-status-shows-on-a-character.md:211, :420-421 |
| RG.G-13 | `01DFE0BC` vs `01DFE0B4` used side by side (tint phase / envelope use 01DFE0BC; flash frame numbers use 01DFE0B4) with no statement of their relation on these pages | frame-rate behaviour of looks | Character-Render-Records/how-a-status-shows-on-a-character.md:156, :223; Character-Render-Records/how-a-character-fades-the-ten-channels.md:64 |
| RG.G-14 | Tint envelope target/start on install: "zeroes the phase and envelope"; Stone phase "rises once over thirty frames" - rate constant not given | timing | Character-Render-Records/how-a-status-shows-on-a-character.md:131, :207 |
| RG.G-15 | Petrify / Doom flash curve values (curve1, curve2) unread, so flash shape cannot be ported | | Character-Render-Records/how-a-status-shows-on-a-character.md:146-147 |
| RG.G-16 | Slow's colour goes "integer colour (128 s, 32 s, 8 s)" through 003B6B30 to shadow `+0x20`; shadow draw interpretation not on page | Slow visual | Character-Render-Records/how-a-status-shows-on-a-character.md:281, :494 |
| RG.G-17 | 00428AF0 three bits at `+0x304`[17..19]: meaning of each bit, and reader 004295E0's use, not stated | Invisible's record field | Character-Render-Records/how-a-status-shows-on-a-character.md:269, :482-484; Character-Render-Records/the-bone-trails.md:469 |
| RG.G-18 | `+0x304` bit 5 reader (dirty bit 28 handler) | Stone/Stop body freeze | Character-Render-Records/how-a-status-shows-on-a-character.md:71 |
| RG.G-19 | Trail draw parameter block "0x20" and the template float block `+0x348`..`+0x3F8` unread | GPU-side reconstruction | Character-Render-Records/the-bone-trails.md:164, :383 |
| RG.G-20 | Trail half-rate gate: "a 27-byte getter of the core runtime, by role" - which getter and its rule | sample cadence | Character-Render-Records/the-bone-trails.md:132 |
| RG.G-21 | 0042F250 "also rewrites three bits of +0x290" - which bits | trail off path | Character-Render-Records/the-bone-trails.md:80-81 |
| RG.G-22 | Rig slot init function: "the rig's slot initialiser" not named or addressed on the page | load path | Character-Render-Records/the-rig-of-seventeen-controllers.md:64-66 |
| RG.G-23 | Countdown sets/clears via "the same wrapper-caller" - the caller's identity for bit 8/eyes absent | | Character-Render-Records/the-rig-of-seventeen-controllers.md:113-115, :127 |
| RG.G-24 | Controller on/off routine addresses per controller mostly not given (only Float 004718D0/00471640, look off 00513150, Confuse on 00515FE0) | to port switches | Character-Render-Records/the-rig-of-seventeen-controllers.md:93-97, :244-246, :298 |
| RG.G-25 | Body-shake update bodies 472/1,294 B: only shape; amount usage unknown | | Character-Render-Records/the-rig-of-seventeen-controllers.md:273-274 |
| RG.G-26 | Look request bits 2 and 4 value semantics (`+0x1D`, `+0x1E` nibbles) | head limits | Character-Render-Records/the-staged-look-command.md:67-68 |
| RG.G-27 | 003E36F0 stages bits 9+10 / 12+13 "bits only" - so three-dword payload source for vector kind 0 is not stated | look-at-point path | Character-Render-Records/the-staged-look-command.md:70, :72 |
| RG.G-28 | `00426220` busy test unexplained; command dropped when busy | lost requests | Character-Render-Records/the-staged-look-command.md:49, :207, :220 |

#### 2.2.5 [CL] Ordered render command list and graphics-thread handshake

Short names in this part: **C** = `CONTRACT-render-command-list-and-graphics-handshake.md`; **L** = `Render-Command-List/the-ordered-render-command-list.md`; **H** = `Graphics-Thread-Handshake/the-shared-command-state-word.md`.


| id | missing | why a port needs it | where |
|---|---|---|---|
| CL.G-1 | Allocation size, constructor arguments and fields for all 36 enqueue classes. The size census covers only "19 enqueue builders". `0018CA50` (SetDofObj, 0x28) is outside it, and SetDofObj's ctor size is "—" | object layout per class | Render-Command-List/the-ordered-render-command-list.md:892, Render-Command-List/the-ordered-render-command-list.md:361, Graphics-Thread-Handshake/the-shared-command-state-word.md:925 |
| CL.G-2 | What slot 1 (execute) does for most classes. Only 8 execute bodies are tabled. C excludes PRESENTATION | without them nothing is drawn | Render-Command-List/the-ordered-render-command-list.md:365-372, CONTRACT-render-command-list-and-graphics-handshake.md:520-521 |
| CL.G-3 | Flush `0018C8F0`: the pseudocode reads `e.flushSelector` with no null test, though the destroy loop tests null. Which `device()` it passes is not named | §10.1 null-append path; execute argument | CONTRACT-render-command-list-and-graphics-handshake.md:397-400, CONTRACT-render-command-list-and-graphics-handshake.md:319-321 |
| CL.G-4 | When in the frame `0018B510` (split) and `0018B030` (mark) are called. Only their wrappers `0018CB10`/`001829F0` are named | decides which entries are in part 1 or part 0 | CONTRACT-render-command-list-and-graphics-handshake.md:274-275, CONTRACT-render-command-list-and-graphics-handshake.md:188-191 |
| CL.G-5 | `+0x28 splitArmed` is written, but no reader is stated | field semantics | CONTRACT-render-command-list-and-graphics-handshake.md:80, Render-Command-List/the-ordered-render-command-list.md:607 |
| CL.G-6 | Writer and polarity of `byte[01FD4A88]` (frame-tick teardown gate) | whether the teardown runs twice or once per frame | CONTRACT-render-command-list-and-graphics-handshake.md:216, CONTRACT-render-command-list-and-graphics-handshake.md:234, CONTRACT-render-command-list-and-graphics-handshake.md:308 |
| CL.G-7 | Value of `+0x49C` contextIndex at construction. C uses it as a boolean | reverse-walk bounds | Render-Command-List/the-ordered-render-command-list.md:812-813, CONTRACT-render-command-list-and-graphics-handshake.md:380-381 |
| CL.G-8 | Ordering of the handshake spins and publishes against the list walks. C's postcondition "`02EBA3F8` has bits 2, 3 and 8 clear" needs the last clear to follow the last publish | frame postcondition | CONTRACT-render-command-list-and-graphics-handshake.md:208-210, Graphics-Thread-Handshake/the-shared-command-state-word.md:900-903 |
| CL.G-9 | A removal path from the ordered list exists elsewhere ("removal is slot 3's `0018B0B0`", `Character-Rendering/character-render-object.md:134`). C and L never mention `0018B0B0`. C names `0018B040` as the only clear | a list op missing from the contract | CONTRACT-render-command-list-and-graphics-handshake.md:60, CONTRACT-render-command-list-and-graphics-handshake.md:389-391 |
| CL.G-10 | The forward arm of `0018B1B0`: C §12 gives "reverse arm" only | bounds of the forward class-filtered walk | CONTRACT-render-command-list-and-graphics-handshake.md:378-387, CONTRACT-render-command-list-and-graphics-handshake.md:155 |
| CL.G-11 | Entry address and callers of the reset burst `GraphicsSync_WaitBackendState100ClearAndResetSharedState`. Value of `02EBA3F8` at load | init of the word | Graphics-Thread-Handshake/the-shared-command-state-word.md:86-89, Graphics-Thread-Handshake/the-shared-command-state-word.md:242-246 |
| CL.G-12 | Writers and initial values of `01DFE0C4` and `01F82EC0`. Whether the screen index resets each frame other than through mode-0 ctors | gating; PostProcessObj behaviour | Render-Command-List/the-ordered-render-command-list.md:386-387, Render-Command-List/the-ordered-render-command-list.md:265-271 |
| CL.G-13 | Where the data-driven keys come from: GiReset* `this[+0x18]` (who sets it), GeometryInstanceOrderedObject `this[+0x20]` | mask filtering for these classes | Render-Command-List/the-ordered-render-command-list.md:307-309, Render-Command-List/the-ordered-render-command-list.md:1008-1011 |
| CL.G-14 | Who frees the four manager-only appended objects (pool or embedded). The owner never sees them | lifetime | Render-Command-List/the-ordered-render-command-list.md:650-666 |
| CL.G-15 | What the render pass `00187950` (3,311 B) does between and around the two walks. C shows "..." | frame order | CONTRACT-render-command-list-and-graphics-handshake.md:241 |

#### 2.2.6 [GP] Gi render commands and the legacy PS2 GS/VIF layer

Short names in this part: **GI** = `Gi-Render-Commands/gi-render-command-family.md`; **TEX** = `Legacy-PS2-GS/texture-mip-local-memory-budget.md`; **VIF** = `Legacy-PS2-GS/the-vif1-vu1-layer.md`.


| # | missing | why a port needs it | where |
|---|---|---|---|
| GP.G-1 | Per-class field layouts of most Gi* commands (only GiPolyGT4T, GiPrim, GiSetTexture fields given; and whether offsets are object- or payload-relative given factories return `result+0x10`) | to build/execute commands | Gi-Render-Commands/gi-render-command-family.md:96, Gi-Render-Commands/gi-render-command-family.md:146-148, Gi-Render-Commands/gi-render-command-family.md:210-211, Gi-Render-Commands/gi-render-command-family.md:979 |
| GP.G-2 | Semantics of most of the 20 device slots (only slot 0, slot 4 batch, 0x80/0x88 stub, 0x128/0x130 bracket described) | execute bodies call them | Gi-Render-Commands/gi-render-command-family.md:1343-1350, Gi-Render-Commands/gi-render-command-family.md:679-682 |
| GP.G-3 | `GiPolyGT4T` resource resolution callees `002D7FA0`/`002D7EE0` and meaning of `0xE00`/`0xDFF` compare | prepare step | Gi-Render-Commands/gi-render-command-family.md:114-115, Gi-Render-Commands/gi-render-command-family.md:146-148 |
| GP.G-4 | Display-list record `+0x20` flag semantics (paths selected), `+0x0C` count use, sort-key bits 24-27 | sort/drain behaviour | Gi-Render-Commands/gi-render-command-family.md:383-387, Gi-Render-Commands/gi-render-command-family.md:352 |
| GP.G-5 | Abandon-condition flags `01DF08FC`/`01F7F594`: meaning, writers, initial values | decides whether records execute | Gi-Render-Commands/gi-render-command-family.md:592 |
| GP.G-6 | Watermark `+0x24` (`0018B510`): who calls it, when | splits prefix/tail passes | Gi-Render-Commands/gi-render-command-family.md:596 |
| GP.G-7 | Frame position of `003A3740` drain and `003A3A00` reset relative to `00187950` | frame ordering | Gi-Render-Commands/gi-render-command-family.md:346-348, Gi-Render-Commands/gi-render-command-family.md:409, Gi-Render-Commands/gi-render-command-family.md:583 |
| GP.G-8 | 0x2F frame field 8 (`&[rsp+0x50]`) meaning | callback ABI | Gi-Render-Commands/gi-render-command-family.md:1294 |
| GP.G-9 | Microprogram semantics: 57 recompiled x64 bodies described only by primitive; inputs/outputs (VU cells, callback ABI) not stated | a port must re-implement or reuse them | Legacy-PS2-GS/the-vif1-vu1-layer.md:799-805, Legacy-PS2-GS/the-vif1-vu1-layer.md:63 |
| GP.G-10 | TOP/TOPS computation in flush `0022C8D0` (UNPACK add-TOPS flag depends on it) | UNPACK addressing | Legacy-PS2-GS/the-vif1-vu1-layer.md:76-77, Legacy-PS2-GS/the-vif1-vu1-layer.md:827 |
| GP.G-11 | Phase-2 state calls `002105B0`, `002104D0`, `00210560(0x51001)`, `002104E0` not described; `00210320` `flag` meaning | replay state | Legacy-PS2-GS/the-vif1-vu1-layer.md:125-127 |
| GP.G-12 | Per-register handler stores beyond the summary (e.g. how ALPHA/TEST map to D3D state) | GS emulation fidelity | Legacy-PS2-GS/the-vif1-vu1-layer.md:843 |
| GP.G-13 | Texture reference descriptor 0x30 layout, the "current dynamic mask", and the continuation-link rule | admission counts | Legacy-PS2-GS/texture-mip-local-memory-budget.md:53-54, Legacy-PS2-GS/texture-mip-local-memory-budget.md:126-127, Legacy-PS2-GS/texture-mip-local-memory-budget.md:130 |
| GP.G-14 | Derived slot record field meanings (+0x00..+0x20) and the consumer that resets them "per frame" (not named) | downstream use | Legacy-PS2-GS/texture-mip-local-memory-budget.md:131-134, Legacy-PS2-GS/texture-mip-local-memory-budget.md:173-174, Legacy-PS2-GS/texture-mip-local-memory-budget.md:211 |
| GP.G-15 | Source record unexplained bytes +0x01..+0x04, +0x0A..+0x0B, +0x10..+0x5F | layout | Legacy-PS2-GS/texture-mip-local-memory-budget.md:119-128 |
| GP.G-16 | Admission walk order (which texture order "Admission stops at the first texture that would cross") | result depends on order | Legacy-PS2-GS/texture-mip-local-memory-budget.md:56-58, Legacy-PS2-GS/texture-mip-local-memory-budget.md:223-225 |
| GP.G-17 | Formats 0x00/0x01 under `format - 2` indexing (underflow handling) | PSM class for 32/24-bit | Legacy-PS2-GS/texture-mip-local-memory-budget.md:182-193 |
| GP.G-18 | Meaning of `0x4000` seed at `02CA5FF0` and of `022D8EA8` | arena policy | Legacy-PS2-GS/texture-mip-local-memory-budget.md:107, Legacy-PS2-GS/texture-mip-local-memory-budget.md:304, Legacy-PS2-GS/texture-mip-local-memory-budget.md:369 |
| GP.G-19 | Frame-index global address (stated only as "one rip-relative write") | FRAME_1 base | Legacy-PS2-GS/texture-mip-local-memory-budget.md:239-248 |
| GP.G-20 | `0020EB60`'s texture-key role (GI says it is one of two `01F83580` readers) is absent from VIF's description of `0020EB60` | texture bind path | Gi-Render-Commands/gi-render-command-family.md:221-224, Legacy-PS2-GS/the-vif1-vu1-layer.md:365-369 |

#### 2.2.7 [EF] Effect containers, element dispatch and the per-frame element update

Short names in this part: **DISP** = `Effect-File-Formats/effect-element-type-dispatch.md`; **FBF** = `Effect-File-Formats/an-effect-element-frame-by-frame.md`; **EFX** = `Effect-File-Formats/efx-and-efb-effect-containers.md`; **ERM** = `Effect-File-Formats/README.md`; **CAT** = `README.md`.


| id | missing | why a port needs it | where |
|---|---|---|---|
| EF.G-1 | Age at birth: `002F2D60` zeroes `+0x3C`/`+0x40`/`+0x48`, then step adds 1.0 to `+0x3C` (conditional); value of `+0x44` and `+0x38` at birth not stated | first-frame timing of tracks, spawn tag start, expiry | Effect-File-Formats/effect-element-type-dispatch.md:56-57, 68-69; Effect-File-Formats/an-effect-element-frame-by-frame.md:43 |
| EF.G-2 | What `002F31C0` does for types < 0x40 (method range "`+0` − `0x40`", TSV `-` below 0x40) though every 0x01-0x0A tail releases through it | release of basic elements | Effect-File-Formats/effect-element-type-dispatch.md:162, 176; Effect-File-Formats/an-effect-element-frame-by-frame.md:79-80, 134-136 |
| EF.G-3 | Who calls the nine tails each frame: FBF never names the caller; DISP blocks show the birth step arms calling them as "prelude" | order: tail at birth vs per update | Effect-File-Formats/an-effect-element-frame-by-frame.md:69-233; Effect-File-Formats/effect-element-type-dispatch.md:2166, 2250, 2254, 2258, 1962 |
| EF.G-4 | Spawner `003A8AE0`: meaning of constant 2, time argument use, owner `+0x1C`/byte `+0x1A`, how sub-resource index becomes element(s) | child spawning | Effect-File-Formats/an-effect-element-frame-by-frame.md:153-156; Effect-File-Formats/effect-element-type-dispatch.md:100 |
| EF.G-5 | Trigger passed by `002F2D60`'s own `003A8950` call at birth | spawn at birth | Effect-File-Formats/effect-element-type-dispatch.md:1050-1051 |
| EF.G-6 | Track record format sampled by `004309C0`/`004314E0`/`0042FDB0` and full definition (0xA00 record) layout; only scattered offsets named | all tails sample tracks | Effect-File-Formats/an-effect-element-frame-by-frame.md:22, 73; Effect-File-Formats/effect-element-type-dispatch.md:931 |
| EF.G-7 | Element object size and complete layout; pool size / free-list initialisation | allocation | Effect-File-Formats/effect-element-type-dispatch.md:39 |
| EF.G-8 | Rate gate multiplier from `001EDDA0()` and exact compare | element rate | Effect-File-Formats/effect-element-type-dispatch.md:138-140 |
| EF.G-9 | Render byte `02AEE910` formula "from the definition's `+0x4A` / `+0x4C` or from `020926F8`" | layer key | Effect-File-Formats/effect-element-type-dispatch.md:127, 854 |
| EF.G-10 | "even-rounded" in expiry test not defined | lifetime end frame | Effect-File-Formats/effect-element-type-dispatch.md:920 |
| EF.G-11 | Return value of `002F2530` and what `0043EF40` does after the loop (`+0x139`, `[+0x2C]` vs `[+0x28]`) | update result handling | Effect-File-Formats/effect-element-type-dispatch.md:89, 960-961 |
| EF.G-12 | 0x800 payload layout beyond id/subtype at +0x280/+0x282; subtype meanings 0..8 | sub-resources used by spawns | Effect-File-Formats/efx-and-efb-effect-containers.md:183-185; Effect-File-Formats/effect-element-type-dispatch.md:812-814 |
| EF.G-13 | `0xB00` record-store chunk (30,033) not one of the loader's seven types; route to `003EE2D0` and link to the `0x50`-kind store (§2.7) not stated | parse completeness | Effect-File-Formats/efx-and-efb-effect-containers.md:49-50, 101-112; Effect-File-Formats/effect-element-type-dispatch.md:736-751 |
| EF.G-14 | Fourth run pointer: "four run pointers `+0x870`–`+0x888`" but only `+0x870`/`+0x878`/`+0x880` assigned; 0x600-family "second buffer" location not given | loader context | Effect-File-Formats/efx-and-efb-effect-containers.md:109-113, 143-144 |
| EF.G-15 | 0x700 subtype bodies' relocated field lists ("a fixed list of sub-blocks") not enumerated | relocation | Effect-File-Formats/efx-and-efb-effect-containers.md:246-249 |
| EF.G-16 | 0x600 record bytes +0x01..+0x09, +0x16 low bits, +0x18..+0x2B meanings beyond lanes/request slots | effect definitions | Effect-File-Formats/efx-and-efb-effect-containers.md:258-277 |
| EF.G-17 | EFB 0xA0 row bytes beyond +0/+1/+4/+5/+8..+0xB; meaning of the 12 bytes in each blob header | EFB binding | Effect-File-Formats/efx-and-efb-effect-containers.md:453-462 |
| EF.G-18 | Element `+0x294` resource index for type 0x05 walk: writer not stated (tail 0x05 does not write it) | type 0x05 draw | Effect-File-Formats/effect-element-type-dispatch.md:643-647; Effect-File-Formats/an-effect-element-frame-by-frame.md:210-213 |
| EF.G-19 | Order of update vs walk within one frame not stated | frame ordering | Effect-File-Formats/effect-element-type-dispatch.md:147-149 |

#### 2.2.8 [ET] Effect element types, kind-0x54 meshes, menu effect registry and VFX layers

Short names in this part: **mesh** = `Effect-File-Formats/effect-mesh-records-kind-54.md`; **00-0a** = `Effect-File-Formats/the-element-types-00-0a.md`; **40-42** = `Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md`; **60-74** = `Effect-File-Formats/the-element-types-60-74.md`; **80-97** = `Effect-File-Formats/the-element-types-80-97.md`; **menu** = `Effect-File-Formats/the-menu-effect-registry.md`; **six-layers** = `Effect-File-Formats/the-six-vfx-display-layers.md`.


| id | what is missing | why a port needs it | where |
|---|---|---|---|
| ET.G-1 | Index lists A/B: what each indexes (positions vs normals vs corners) and why `6·tri + 8·quad` u16 per list | cannot build the mesh topology | Effect-File-Formats/effect-mesh-records-kind-54.md:84-86, :135-136 |
| ET.G-2 | Per-primitive byte `+0x188` ("a small selector") meaning; runtime `+0x18C` flags use | draw-path choice per primitive | Effect-File-Formats/effect-mesh-records-kind-54.md:137-138, :73 |
| ET.G-3 | What a kind-0x52 record is (the `+0x1C` ids resolve to them) | resource bound to a mesh | Effect-File-Formats/effect-mesh-records-kind-54.md:139-141 |
| ET.G-4 | The "alternate vertex-attribute constants" written for language ids 1-6 — values not given | packing differs by language | Effect-File-Formats/effect-mesh-records-kind-54.md:233-235 |
| ET.G-5 | Which caller chooses `00435050` vs `00434CD0` and on what | "One caller chooses between them" unnamed | Effect-File-Formats/effect-mesh-records-kind-54.md:196 |
| ET.G-6 | Handle stride at element `+0x5A0` (32 slots) vs "all ≥ 0x640 B" records (32×8 B would end at 0x6A0) | record extent of type 0x05 | Effect-File-Formats/effect-mesh-records-kind-54.md:149-151, :156; Effect-File-Formats/the-element-types-00-0a.md:85 |
| ET.G-7 | Track evaluators `004309C0`/`004314E0`/`0042FDB0`: interpolation between keyframes, the role of the two arrays per head (A/B) | every element samples tracks | Effect-File-Formats/the-element-types-00-0a.md:78-82, :470-472 |
| ET.G-8 | Seventh method / `003A8950` spawn-slot semantics and `002F31C0` release are only named on these pages | lifecycle | Effect-File-Formats/the-element-types-00-0a.md:473-474; Effect-File-Formats/the-element-types-80-97.md:145-146 |
| ET.G-9 | Types 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6-0xAA have method addresses only; no behaviour section (GI-9 covers 0x40,0x41,0x42,0xA0,0xAB,0xD0,0xD1). type_census.tsv: 0xA2 6,303 chunks / 493 assets | heavily authored types cannot be ported | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:59-73, :108 |
| ET.G-10 | Most 0x80-0x97 walks: program addresses and primitive only, no vertex layout (unlike 0x04/0x06/0x07/0x08) | geometry | Effect-File-Formats/the-element-types-80-97.md:166-173 |
| ET.G-11 | 0x60-0x67/0x68-0x74 walks: VU1 program named, no geometry for most (except 0x71 table) | geometry | Effect-File-Formats/the-element-types-60-74.md:190-203 |
| ET.G-12 | 0x41 seventh `003B42B0` on `+0x234/+0x238`, 0x42 seventh `003D8300` — behaviour not stated | teardown | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:46, :56 |
| ET.G-13 | `00428AF0` (two-bit render field) and `00428CD0` with `+0x235` | 0xD0 apply | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:221-222 |
| ET.G-14 | Relation between group number (1-9, list `020910F0`) and container kind byte `+0` (gate kinds 2-9); group 8 refused yet kind 8 "always" | which effects are drawn | Effect-File-Formats/the-six-vfx-display-layers.md:62-64, :92-101; Effect-File-Formats/the-menu-effect-registry.md:184 |
| ET.G-15 | Menu effects are type-4 contexts; whether "type" = group 4 (drawn last) is never stated | layering of menu effects | Effect-File-Formats/the-menu-effect-registry.md:60; Effect-File-Formats/the-six-vfx-display-layers.md:45 |
| ET.G-16 | `0024B270` instance creation / instance layout (only `+0x304/+0x338/+0x373` named), `003EDAD0` parse | registry spawn | Effect-File-Formats/the-menu-effect-registry.md:60-61, :114 |
| ET.G-17 | `0024EEE0` described as "record registration `0024EE60` runs" while `0024EE60` is the release `003B2AA0` runs — a release calling a register is unexplained | remove path | Effect-File-Formats/the-menu-effect-registry.md:183-187, :363 |
| ET.G-18 | Initial values of `02092162/4/6`, `02AEE910`, `01EF93E8` not given | first-frame behaviour | Effect-File-Formats/the-six-vfx-display-layers.md:65; Effect-File-Formats/the-element-types-00-0a.md:273; Effect-File-Formats/the-element-types-60-74.md:45 |
| ET.G-19 | Who calls the per-element update per frame and in which frame phase (pages state draw-side walk only) | update/draw ordering | Effect-File-Formats/the-element-types-00-0a.md:49-53; Effect-File-Formats/the-six-vfx-display-layers.md:83-84 |
| ET.G-20 | `00258B90` caller/phase not stated | camera handoff ordering | Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:260 |

#### 2.2.9 [MF] Model formats: add-motion tables, ADM, FCP, FDM/FOR

Short names in this part: **SKEL** = `Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md`; **ADM** = `Model-And-Motion-Formats/adm-add-motion-tables.md`; **FCP** = `Model-And-Motion-Formats/fcp-character-parameter-block.md`; **FDM** = `Model-And-Motion-Formats/fdm-and-for-entries.md`; **MREADME** = `Model-And-Motion-Formats/README.md`.


| id | what is missing | why a port needs it | where |
|---|---|---|---|
| MF.G-1 | Which handle slot (`+0x6E8` or `+0x6F0`) holds the `_town` table, and which `00377C20` value means "town" | the applier picks by "handle 1"/"handle 0" and a combat flag; no page maps these to the slots or gives the flag's polarity | Model-And-Motion-Formats/adm-add-motion-tables.md:136-137, 300-302, 492-493 |
| MF.G-2 | Where the kind-0 "current channel parameter" comes from | the interpolation needs it; only `(frame − key0) / span * rate` is given, and frame/key0/span/rate are not defined | Model-And-Motion-Formats/adm-add-motion-tables.md:305-306, 461-463 |
| MF.G-3 | Behaviour when the parameter lies outside the lane range (clamp or extrapolate) | an edge case of the interpolation | Model-And-Motion-Formats/adm-add-motion-tables.md:461-463 |
| MF.G-4 | Euler order / convention of `Matrix4x4f_BuildEulerRotation`, and how the result combines with the base pose (add or replace) | needed to reproduce the pose | Model-And-Motion-Formats/adm-add-motion-tables.md:425, 308 |
| MF.G-5 | Meaning of the 11 all-zero group headers that are not group 0 | §10 explains only the 35 first-group sentinels | Model-And-Motion-Formats/adm-add-motion-tables.md:253-255, 483-484 |
| MF.G-6 | `.adm` registry container (how parsed records are "appended"), the name field's maximum length in the 32-byte record | needed to rebuild the lookup | Model-And-Motion-Formats/adm-add-motion-tables.md:108-109, 115, 431 |
| MF.G-7 | `003703A0`'s joint-follow math (only "each non-`-1` value makes that joint follow the given joint") | needed to apply SkeletonMapping | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:231-233 |
| MF.G-8 | `0037B4D0` body: only a callee list | it is a `0037CB90` caller | Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:116-118 |
| MF.G-9 | Integer default table `01F266B0` contents; float defaults past slot 47 | every weapon reads defaults ("Every weapon's section-9 reads return it") | Model-And-Motion-Formats/fcp-character-parameter-block.md:135-153, 190-192 |
| MF.G-10 | The constants in `0026A490` ("each × a constant"), `003045A0`, `00236210`, `00320DE6`, knockback | the readers' outputs depend on them | Model-And-Motion-Formats/fcp-character-parameter-block.md:238, 337, 342, 344, 348 |
| MF.G-11 | The mode-2 id `0x40000000` reading payload `+0x01` (what it returns) | index 28 of the tunable table | Model-And-Motion-Formats/fcp-character-parameter-block.md:184, 321 |
| MF.G-12 | Payload `+0x2A` per-file value and `+0x38` (`_w38`) meaning, readers | layout fields with no stated role | Model-And-Motion-Formats/fcp-character-parameter-block.md:85, 91 |
| MF.G-13 | Section-1 slots read by the inline `+0x02` readers (`003E4700`, `003E4B71`, …) | readers listed, slots not given | Model-And-Motion-Formats/fcp-character-parameter-block.md:664 |
| MF.G-14 | Range-band table entries for weapon kind 2 (slots 18/19): the table has six kinds but kind 2 is excluded | no page says what slots 18/19 hold | Model-And-Motion-Formats/fcp-character-parameter-block.md:333-338 |
| MF.G-15 | Section-8 record: `+0x1A0` point lies inside the "0x120-byte zero region" (0x90..0x1AF), and `+0x1C0`/`+0x1C4` lie past the three-float tail | the authored layout and the runtime readers do not line up | Model-And-Motion-Formats/fcp-character-parameter-block.md:722-725, 737-754 |
| MF.G-16 | `@FOR` `+0x31..+0x33` given as "(1,1,1)", yet `+0x32` multiplies the variant and `+0x33` clamps `+0xB9` | the bytes have roles that the header does not state | Model-And-Motion-Formats/fdm-and-for-entries.md:68, 142, 165 |
| MF.G-17 | `@FOR` record `+0xC0..+0xDF`, and the `+0x1C` count / `+0x80` array on the `dword[ctx+0x86F8]!=0` arm | part of the 0xE0 record has no meaning | Model-And-Motion-Formats/fdm-and-for-entries.md:94, 137-138, 157-158 |
| MF.G-18 | Where the table-A record count `k` is stored | needed to find table B | Model-And-Motion-Formats/fdm-and-for-entries.md:70 |
| MF.G-19 | `00421280(object,1)` and the `003E57D0` bit `0x2000` (LOD apply) | the LOD step ends in them | Model-And-Motion-Formats/fdm-and-for-entries.md:116-117 |
| MF.G-20 | Frame/timing of `004201F0`, `00373860`, `001BDC40` | B4 ordering | Model-And-Motion-Formats/fdm-and-for-entries.md:96, Model-And-Motion-Formats/adm-add-motion-tables.md:104, 128 |

#### 2.2.10 [MM] Motion formats: FEF/motion entries, FRP, FTE/FCT, FTR, oscillator, pose sequencer

Short names in this part: **ACH** = `Authored-Commands/the-authored-presentation-command-handlers.md`.


| # | missing | why a port needs it | where |
|---|---|---|---|
| MM.G-1 | `.ca` v1 header bytes `+0x30..+0x3F`: the container page gives no fields there (table only at `+0x40`); fef names `+0x30` stride and `+0x34` group count; `+0x38`/`+0x3C` not stated | slot math needs group count/stride; a writer needs the full header | Model-And-Motion-Formats/frp-object-container.md:66-81; Model-And-Motion-Formats/fef-and-motion-entries.md:99-102 |
| MM.G-2 | `@FTR` bit-30 leading u16: ftr says only "skip a leading u16"; what it holds (the record key `00409250` returns when bit 30 set, per Character-Render-Records/how-a-character-fades-the-ten-channels.md:774) is not on the page | key search `003737C0`/`00373540` matches on it; bit 30 is set in every record (:204) | Model-And-Motion-Formats/ftr-node-table.md:86, :75-77 |
| MM.G-3 | `@FRM` payload format: "the two bound regions are handed to the request, not parsed here" — no decode of the motion resource beyond the head offset list | the motion resource is the core motion data | Model-And-Motion-Formats/fef-and-motion-entries.md:704-707, :718-722 |
| MM.G-4 | how `f32[state+0xC]` (frame position) advances per tick (rate from `+0x18 = 0x1E0000`, `+0x20 = 30.0f`?) not stated | sampler and event thresholds both read it | Model-And-Motion-Formats/fef-and-motion-entries.md:271-273, :313 |
| MM.G-5 | full layout of the 0xA0-stride descriptor/state row (`+0x0C`, `+0x16/+0x18/+0x1C`, `+0x48..+0x80`, `+0x88/+0x8C/+0x90/+0x96`, `+0x5E`) only given piecemeal | executor and sampler state | Model-And-Motion-Formats/fef-and-motion-entries.md:254-255, :312-314, :477-482 |
| MM.G-6 | three of ten `0x0B` selector kinds' bodies not described ("seven of ten are read"); op `0x00` tail-call `[[02CA4668]+0x2F8]` callee not described; op `0x04` arms only partly given | track selection behaviour | Model-And-Motion-Formats/fef-and-motion-entries.md:352-355, :312, :315 |
| MM.G-7 | `@FMN` `+0x70` vec2 → `003E2EA0`, `{+0xA4,+0xA0}`/`+0xA8` → `003B5CE0`, `+0xEE` → `003E2D20`: written targets given, meaning of the authored values not stated | the applier arm consumes them every motion | Model-And-Motion-Formats/fef-and-motion-entries.md:519-522 |
| MM.G-8 | 0x290 bone fields `+0x1A0`, `+0x1C0` (read by the inline composer and the `@FMW` apply) and `+0xB8` ("+0xB8/+0x270 parent word") have no stated meaning | pose composition | Model-And-Motion-Formats/ftr-node-table.md:97, :263, :265 |
| MM.G-9 | `0040B180` (554 B, controller 0's evaluator in `003E00C0`) named only; relation to the `003703A0`→`003DFFE0`→`0040ACF0` path not stated; absent from members TSV | which path actually drives sway per frame | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:237-238, :332 |
| MM.G-10 | phase-advance time factor: pose-sequencer Q10 says `0040AA20` "adds +0x24 × [01DFE0BC]"; the oscillator page's advance formulas (`0040ACF0`) state no time factor | 30/60 fps parity | Model-And-Motion-Formats/the-pose-sequencer.md:277; Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:81, :83 |
| MM.G-11 | `0046FAE0(entry, mode', nibble_hi)`, `00415EE0`/`00416FB0` scope/post-step semantics ("call-site roles" only) | tier dispatch | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:128-129, :354 |
| MM.G-12 | `0054B1F0` sub-entry fields `+0x3C/+0x40/+0x4C/+0x2C` (0x50 stride) and `0x20`-stride tail entries' `+0x18`: meaning not stated | effect type 0x72 parameter install | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:170-174 |
| MM.G-13 | oscillator record `+0x10` (row 31 / Q reciprocal) and `+0x1C` (row `022D8FB0`→`022D9350`): what the VU program uses them for not stated | VU math port | Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:79-80 |
| MM.G-14 | phase-entry header: `+0x08` and the initial values of the slot arrays on allocation not stated (only `+0`, `+2`, `+4`, `+0xC`) | sequencer start state | Model-And-Motion-Formats/the-pose-sequencer.md:59, :71-81, :92 |
| MM.G-15 | random picker formula with `pickParam` not stated (picker "not read") | choice distribution | Model-And-Motion-Formats/the-pose-sequencer.md:48, :89, :208 |

#### 2.2.11 [PP] Post-processing and visual tuning parameters

Short names in this part: **CS** = `Post-Processing/CONTRACT-post-processing-subsystem.md`; **CP** = `Post-Processing/CONTRACT-ppfx-effect-creation.md`; **PI** = `Post-Processing/ppfx-function-identification.md`; **CAT** = `Post-Processing/the-post-processing-effect-catalogue.md`; **VR** = `Visual-Tuning-Parameters/README.md`; **RR** = `Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md`; **RCL** = `Render-Command-List/the-ordered-render-command-list.md`; **HL** = `Post-Processing/members/ppfx-handle-layout.tsv`.


| id | missing | why a port needs it | where |
|---|---|---|---|
| PP.G-1 | Meaning of flag bits `0x20000` and `0x1` in `0x20001`, and of the low groups `Initialize` forces (`0x0F`/`0x70`, bit 7) | port must pick equivalent library init | Post-Processing/CONTRACT-post-processing-subsystem.md:73; Post-Processing/the-post-processing-effect-catalogue.md:1021-1022 |
| PP.G-2 | `006CBBC0` default block: only "aspect 16/9, 0x780 and 7 qwords of -1"; full layout, meaning of `0x780` (RCL calls it "size") and kinds 3/5 not stated | needed to reproduce library init | Post-Processing/CONTRACT-post-processing-subsystem.md:72-73; Render-Command-List/the-ordered-render-command-list.md:1720 |
| PP.G-3 | Step 1 reset arm: the two virtual calls' semantics | frames with `cfg+0x99` behave differently | Post-Processing/CONTRACT-post-processing-subsystem.md:82; Post-Processing/the-post-processing-effect-catalogue.md:937 |
| PP.G-4 | Step 3 block content/semantics (`&cfg+0x9C`, size disputed) | input to library each frame | Post-Processing/CONTRACT-post-processing-subsystem.md:85; Post-Processing/the-post-processing-effect-catalogue.md:940 |
| PP.G-5 | Step 4 vec3 meaning ("half-extent" per RCL) and why last is halved | same | Post-Processing/CONTRACT-post-processing-subsystem.md:86; Post-Processing/the-post-processing-effect-catalogue.md:941 |
| PP.G-6 | Step 6 `006CC170` / `006DC820(32.0, -FLT_MAX)` meaning, and who sets `cfg+0x98`/`+0x9A` | same | Post-Processing/CONTRACT-post-processing-subsystem.md:100-101; Post-Processing/the-post-processing-effect-catalogue.md:944 |
| PP.G-7 | Sources of `cfg+0x30`/`+0x34` (step 7 on-path floats) and the 0.5/0.5/0.0/1.0 off defaults' meaning | DOF parameters | Post-Processing/the-post-processing-effect-catalogue.md:945-946; Post-Processing/CONTRACT-post-processing-subsystem.md:137-145 (table omits them) |
| PP.G-8 | Who sets `cfg+0x98`, `+0x99`, `+0x9A`, `+0x9C..`, `+0xDC..+0xE4` (only +0x18..+0x2C and +0x94 sourced) | cfg builder `0018EEE0` only partly described | Post-Processing/CONTRACT-post-processing-subsystem.md:137-145, Post-Processing/CONTRACT-post-processing-subsystem.md:263-265 |
| PP.G-9 | `006CBEA0` run: what "Phyre render-context guard" is; how cfg[0]/[8]/[0x10] map to library calls | run call | Post-Processing/CONTRACT-post-processing-subsystem.md:106-107 |
| PP.G-10 | Effect file base name `<name>` (only suffix literal given) | must load the right `.pso` | Post-Processing/the-post-processing-effect-catalogue.md:97, Post-Processing/the-post-processing-effect-catalogue.md:783-784; Post-Processing/CONTRACT-ppfx-effect-creation.md:217 |
| PP.G-11 | Handle slot map for 15 unplaced and 73 built-string lookups; what `+0x48` vs `+0x60` vs `+0xC8` interface slots are (only "reading, labelled") | a port of the library binding | Post-Processing/the-post-processing-effect-catalogue.md:803, Post-Processing/the-post-processing-effect-catalogue.md:806 |
| PP.G-12 | `0072DCF0` suffix-table full contents and order | determines handle variants | Post-Processing/the-post-processing-effect-catalogue.md:806 |
| PP.G-13 | Two of the 22 call targets / ~4 of 358 sites not itemised (enumerations reach 20 targets, ~356 sites) | census reproduction | Post-Processing/CONTRACT-ppfx-effect-creation.md:82-85, Post-Processing/CONTRACT-ppfx-effect-creation.md:157-162; Post-Processing/the-post-processing-effect-catalogue.md:123-137 |
| PP.G-14 | Wrapper lifetime/teardown (`[02D38540]`, library object, CTextureUtil release caller) not stated | shutdown/reset | Post-Processing/CONTRACT-post-processing-subsystem.md:56-58; Post-Processing/the-post-processing-effect-catalogue.md:814 |
| PP.G-15 | `0065E580(wrapper, 1)` platform switch semantics | device setup | Post-Processing/CONTRACT-post-processing-subsystem.md:290-292 |
| PP.G-16 | `+0x8000` / `+0x400` features (bytes +0x143, +0x144/+0x146) unnamed | feature set | Post-Processing/the-post-processing-effect-catalogue.md:1009-1010 |
| PP.G-17 | Map reader (`001C7940`) key → block field mapping beyond glare/DOF; render-param fields for SAO/HBAO/shadow keys in RR | loading scene JSON into block | Post-Processing/CONTRACT-post-processing-subsystem.md:129; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:345 |
| PP.G-18 | Flying-fade globals' addresses not given | state | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:144-147 |
| PP.G-19 | `001EF2D0`'s target object not identified ("a different object") | cascade defaults | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:741-743 |
| PP.G-20 | Arithmetic consuming any of ~150 parameters (no formula) | the look | Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:284-285 |

#### 2.2.12 [CM] Scripted camera, screen fade, screen effects, aspect fit, position-to-scalar, movie index

Short names in this part: **MR** = `Movie-Containers/README.md`; **MH** = `Movie-Containers/mh-movie-seek-index.md`; **PTS** = `Position-To-Scalar/how-a-position-becomes-a-single-number.md`; **SF** = `Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md`; **AF** = `Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md`; **CI** = `Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md`; **CR** = `Scripted-Camera/how-a-camera-reaches-the-renderer.md`; **P** = `Scripted-Camera/the-scripted-camera-player.md`; **RM** = `README.md`; **WT** = `../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`.


| # | what is missing | why a port needs it | where |
|---|---|---|---|
| CM.G-1 | The WebM player itself: decoder, codec set, A/V sync, what `001B7F30` hands the path to, and who calls the open (only the path build is documented) | movies cannot be played from the DB | Movie-Containers/README.md:11-14; Movie-Containers/mh-movie-seek-index.md:90-92; Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:644-650 |
| CM.G-2 | `0067A9B0` sub-record at `+0x678` (fields `+0x150`,`+0x218`,`+0x238`,`+0x260`,`+0x268`,`+0x288`,`+0x290`,`+0x2A8`,`+0x480`,`+0x4B8`,`+0x4D0`,`+0x508`,`+0x510`) has offsets but no meanings, and its callees (`006CC670`, `006CC730`, `006CCA70`, `00679F40`) are undescribed | movie container lifecycle | Movie-Containers/mh-movie-seek-index.md:241 |
| CM.G-3 | `001B82F0` / `001848A0` / `001B7F20`: when they run and what `edx` carries | ordering of movie ops | Movie-Containers/mh-movie-seek-index.md:230-237 |
| CM.G-4 | fade node: units/type of the near/far words and floor bytes; behaviour when `near == far` is asserted (`0x80`) without the division guard shown; kind values other than 1/2/3/4 | alpha formula incomplete for some inputs | Position-To-Scalar/how-a-position-becomes-a-single-number.md:194-200 |
| CM.G-5 | fade kind 3: the timed-fade value from `003ED0E0` / timer block `02EBB7E4`-`02EBB7EF` is not given as a formula, nor which near/far pair "the depth path again" uses | kind 3 cannot be reproduced | Position-To-Scalar/how-a-position-becomes-a-single-number.md:196-198 |
| CM.G-6 | modifier order and arithmetic: bit 3 blend through `0026EE00` (operation not stated), bit 10 table `02EBF278` layout, bits 12/13 `+0x35C` factor, order in which bits 2/3/4/5/10/12/13 apply | output colour not reproducible exactly | Position-To-Scalar/how-a-position-becomes-a-single-number.md:201-208, 358-362 |
| CM.G-7 | writer and in-play value of `02AEEA20` (labelled "view" in the composition, identity at title) | mode 1/2 distance depends on it | Position-To-Scalar/how-a-position-becomes-a-single-number.md:119-121, 224-225, 238 |
| CM.G-8 | "A second body, 857 bytes in the `00332xxx` run" — unnamed address | second consumer of the ramp | Position-To-Scalar/how-a-position-becomes-a-single-number.md:362 |
| CM.G-9 | fade start: "two frame-rate words defaulted to 1" / "the two words zeroed" — addresses never named; layer descriptor bytes `+0x0C`-`+0x23` of the record unexplained | start/reset state incomplete | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:60-61, 90, 51 |
| CM.G-10 | consumer of `022BDEB0`/`022BDEB4`/`022BDEB8` ("kind and wait words ... for whoever resumes the scene") not named | skip/schedule semantics | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:92, 133-136 |
| CM.G-11 | `00375A20` slot chooser (kind nibble, priority) algorithm; `00374950` pool tick caller and frame position; the "scheduling predicate" that makes it advance 2 | fade duration timing (counter vs `2×frames`) | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:65, 239-242 |
| CM.G-12 | whether the layer start ever sets descriptor `+0x1C` bit 1 (the tick's release condition for kind 1); `+0x24` documented only as "bit 0 = direction 1" | when finished fade records are released by the pool | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:51, 240-242 |
| CM.G-13 | `0024DE70` / `0024CFF0` nine-arm tables: only class 8 described | other handle classes reaching the fade path | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:71-72 |
| CM.G-14 | the three `WorldTransition_*` callers' layer/frames/colour arguments not listed | transitions not reproducible | Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:99 |
| CM.G-15 | aspect record and display object initial values (constructor `001DC5C0` fields not given); `+0x08` in branch C "whatever it held before" | first-fit state | Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:84, 154 |
| CM.G-16 | when `001DDBA0` runs (what triggers `001DC730` / `00182F70`) | ordering of mode change vs render | Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:94-97 |
| CM.G-17 | render-target allocator, its texture getter, late-release list owner, frame-count scaler and pass-mask setters are "described by role and not named" | a port must locate/replicate them | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:77-86, 187, 317-319 |
| CM.G-18 | `003B2F90` note ends mid-sentence ("then `0024C460(3)` reaps") | reaping behaviour | Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:402 |
| CM.G-19 | camera rebuild `003CBD60` math (only callees listed), `003CC080`/`003CC000`/`003CC970` beyond field copies | view matrix build | Scripted-Camera/how-a-camera-reaches-the-renderer.md:84-86, 430; Scripted-Camera/the-scripted-camera-player.md:191-193, 1039-1046 |
| CM.G-20 | `003D83A0` "candidate calculation" and `002563F0` "two base scalars" contents | shake output | Scripted-Camera/how-a-camera-reaches-the-renderer.md:150, 169, 426 |
| CM.G-21 | authored shake entry: width of the 32 curve numbers (0x30 bytes available from `+0x30` in a 0x60 entry); "shared mode flag" in step 5; `[02B58190]` global | sampler parameters/timing | Scripted-Camera/how-a-camera-reaches-the-renderer.md:214, 222-232 |
| CM.G-22 | camera record (0x110) layout beyond `+0` eye, `+0x10` target, `+0xF0` mode; what `0025A2C0`/`0025A3D0` copy; who sets records 0-4 and 6-7 | arbitration stack | Scripted-Camera/the-scripted-camera-player.md:284-289, 511-513, 1093-1101 |
| CM.G-23 | plain timing word `0` (`progress = clock / 0`) and path progress with `word==0` not covered; duration "never 0 in the corpus" only for `+0x22` | divide-by-zero behaviour | Scripted-Camera/the-scripted-camera-player.md:213-214, 387 |
| CM.G-24 | hit-check probe `00230B60` / `0022F430` semantics (only callee lists) | `camerahitcheck` result | Scripted-Camera/the-scripted-camera-player.md:195-197, 1127-1133 |
| CM.G-25 | blend `00257520`: which "position fields" of the record are blended | resume-behind blend | Scripted-Camera/the-scripted-camera-player.md:630-631 |
| CM.G-26 | what reads `02AEDF94` heading and `02AEDE30` (far-1000) — "-" in table | consumers of build outputs | Scripted-Camera/how-a-camera-reaches-the-renderer.md:111-120 |

## 3. Contradictions (statements a re-implementer would have to choose between)

Quotes are exact apart from `…` for an elision and the dropping of markdown emphasis. Each side is cited `page:line`.
"Favoured" is named only where a dated correction on the pages settles the point, and that correction is quoted.
Otherwise the item says **no favoured side**, even where arithmetic or a TSV leans one way; the lean is reported as a
lean. Every value-changing item is **page-text only - needs local check**: this session cannot see the executable.

- §3.1 lists the value-changing items: they change a value, offset, address, constant, formula, mask, polarity or function role that a port would implement.
- §3.2 lists disagreeing counts and census figures. They are values, but they do not change runtime behaviour.
- §3.3 lists stale "open / not read" claims, struck-but-repeated text, and banner disagreements.

Items are grouped by the part whose reader found them. A contradiction that spans two pages is listed once, under the
part that owns one side; where two parts each found the same disagreement, both entries are kept (their quotes differ)
and are joined here:

| topic | items | one-line statement |
|---|---|---|
| base of the `0xA0 × 0x740` render-record pool | AC.CV-5, RO.CV-2 | `022C6F28` (executed in the coast-down harness) vs `[02B3EF28]` (handlers page, `@FEF` page) vs `02095210` (render-object page) |
| `160 × 0x740` and what sits at `+0x48830` | RO.CV-3, RO.CV-16, RA.CV-1 | `0x48830` stated as the product (it is `0x48800`); the `0xA0` argument stored vs unused |
| the frame-rate word `01DFE0B4` | AC.CV-6, RA.CV-10 (see also RG.CV-11, RG.CV-15) | holds 1 vs 2; threshold 30 vs 60; width u32 / word / byte |
| record `+0x114` | RA.CV-3, RG.CV-12 | shadow (ramp-slot) handle vs `animPhaseHandle` |
| record words `+6` / `+8` / `+0xA` and arming | RA.CV-4, AC.CV-8 | own array index vs parent link; arming copies live → cache vs replays the cache |
| timed hold (class `0x03`) with a command value of −1 | RA.CV-7, MM.CV-9 | stays −1 vs coerced to 1 |
| `02EBEF88` | EF.CV-1, ET.CV-9 | effect-instance list root vs global frame stamp |
| the element step method | EF.CV-4, ET.CV-10 (and ET.CV-1) | per-frame vs once at birth (dated 2026-09-29 correction on the dispatch page); PRNG before or after the tail |
| the bank-selector byte at `+0x1C` | RO.CV-4, RO.CV-5 | camera-source flag with two writers vs two-state pass selector with three; chosen vs called back to back |
| handler-bank capacity | RA.CV-12 (and AC.G-7) | 75 slots vs 76 ids |
| VU1 render-command size and trail template | GP.CV-14, RG.CV-7 | `0x488` vs `0x640` bytes; UNPACK `NUM 0x45` vs `num=27` |
| post-processing step 3 and the cutscene loader | PP.CV-3, PP.CV-8 (against the render-command-list page) | two 16-byte stores vs a `0x40`-byte copy; loader writes record `01F812D0` vs the `0x4A8` block |


### 3.1 Value-changing — page-text only - needs local check

Every item in §3.1 is **page-text only - needs local check**: this session cannot see the executable. Where an item names a favoured side, a dated correction on the pages settles it and is quoted; otherwise the item says **no favoured side** (a lean from arithmetic or a TSV is labelled as a lean).

#### 3.1.1 [AC] Authored commands, ramp channels and the coast-down latch

**AC.CV-1 Fifth-channel setter `003AFD30` argument at the presentation reset (0 vs 1)** *(page-text only - needs local check)*
- "the setter's five call sites pass **mode values** — 0 at three sites, 1 on `00520800`'s record-`+3`-nonzero path, and `r12d` at `003B9708` in `003B8670`" (CONTRACT-authored-command-ramp-channels.md:408-410).
- vs "`003AFD30(1)` together with `003B6930(4)` is exactly the pair [the world tick and the field frame] records in the field-frame reset sequence" (Authored-Commands/the-authored-presentation-command-handlers.md:313-315). That page's presentation reset: "`003AFD30(1)`, `003B6930(4)`" (../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md:802-803, `0024D9C0`).
- With 0024D9C0 passing 1, at most two of the five sites pass 0.
- No favoured side. Lean: 1 at two sites (handler page plus world tick).

**AC.CV-2 Command layout of the ramp classes (slot id carried or not)** *(page-text only - needs local check)*
- "a script command of class `0x0D`–`0x10` carries `(slot id, steps, target)`" (CONTRACT-authored-command-ramp-channels.md:297-298).
- vs "Each takes the **shadow handle from the presentation entry's `+0x35C`** … the step count from command byte `+2`, and the two targets from the command's floats at `+4` and `+8`" (CONTRACT-authored-command-ramp-channels.md:257-260; same in Model-And-Motion-Formats/fef-and-motion-entries.md:993-996).
- No favoured side. Lean: :257-260, read whole 2026-09-19.

**AC.CV-3 `003B5C00` steps five channels or four** *(page-text only - needs local check)*
- "`003B5C00(handle)` applies the same five-channel step to one slot" (CONTRACT-authored-command-ramp-channels.md:225-226; also :247-248).
- vs "decrements byte counters `+0..+3` and folds `+0x60`/…/`+0x7C` deltas into the `+0x50`/…/`+0x70`/`+0x78` float pairs" (:860). This lists no `+0x43`/`+0x98`/`+0x9C`.
- No favoured side.

**AC.CV-4 Field sources of command `0x3F` (row vs GI-15)** *(page-text only - needs local check)*
- "posts `00520E90` across the hierarchy, which hands the rig's controller 0 a preset (word `+2`; 0 = off), a direction (floats `+4`..`+0xC`), an id and a flag (word `+0x10`)" (Authored-Commands/the-authored-presentation-command-handlers.md:110). This row is not struck.
- vs "`+0x14` bone | `word[cmd + 2]`, used directly … `+0x16` preset | `word[cmd + 0x10] & 0xFFF` (4, 5 or 6 as authored)" (:1064-1065).
- **Favoured: GI-15**, by the dated correction "*(corrected 2026-10-01, OPUS: the GI-15 section)*" at :364, :372 and :375.

**AC.CV-5 Pool base address of the 0xA0 × 0x740 records** *(page-text only - needs local check)*
- "walking the `022C6F28` manager array (`0xA0` records × `0x740`, `0041F730` per record)" (Authored-Commands/the-authored-presentation-command-handlers.md:75-76); "`R = [022C6F28] + idx * 0x740`" (:512); CONTRACT-coast-down-latch.md:52 "`*(char**)0x022C6F28 + id * 0x740`" (executed, :449).
- vs "the `0x740`-record at `qword[ctx+0x2E0]` (pool `0xA0 × 0x740` at `[02B3EF28]`); record init `0041F730`" (Authored-Commands/the-authored-presentation-command-handlers.md:1002-1003). Also Model-And-Motion-Formats/fef-and-motion-entries.md:430 "at `[02B3EF28]` (pool init `004269A0` → `0041F730`".
- No favoured side. Lean: 022C6F28 (executed in the coast-down harness).

**AC.CV-6 Time base `01DFE0B4`: 1 or 2, and threshold 30 or 60** *(page-text only - needs local check)*
- "Its value is `2`, so the readings agree today" (CONTRACT-coast-down-latch.md:285-286), and "timeBase is 2 -- ONE writer in the image, 001EDDF2 stores the constant -- so the threshold is 60" (:324-325).
- vs "the time base at `01DFE0B4`, which holds `1` in the shipped image so the default threshold is 30" (:349-350).
- Cross-page: "`frameLimit` is `01DFE0B4` (1 at 30 fps, 2 at 60 fps)" (Authored-Commands/the-authored-presentation-command-handlers.md:922). Also "written together by `001EDDC0` as `{2, 2.0, 0.5}` and shipping as `{1, 1.0, 1.0}`; `K-8` shows all three writes happen once at startup" (Effect-File-Formats/effect-element-type-dispatch.md:949-951).
- No favoured side. Lean: image 1, set to 2 at startup, so the runtime threshold is 60 at 60 fps.

**AC.CV-7 Counter value after overflow (−128 onward vs fixed point −76)** *(page-text only - needs local check)*
- "on the 128th increment `cl` is `0x80` and the next `movsx` reads **-128**. From then on the value is negative" (CONTRACT-coast-down-latch.md:268-270), and "it turns negative on the 128th call and this test then passes forever" (:326-327).
- vs "the byte walks `0,1,…,0x7F,0x80` then snaps to `0xB4` and stays: a **negative fixed point of −76**, not a ramp through the negatives. `(uint32)(int8)` of it is ≥ 60 from the 60th call" (:411-414).
- **Favoured: :410-414** (dated "*Confirmed 2026-09-22 (SWE2-CONTRACT-COASTDOWN-ATTACHLINK)*").

**AC.CV-8 What arming does (cross-page)** *(page-text only - needs local check)*
- Contract: "**Arming.** Same replay, and bit 0 of `+0x62C` is set" (CONTRACT-coast-down-latch.md:136). Its §12 arm path replays the cache and sets bit 0 (:328-333), and the copy happens only on the cache path (:335).
- vs the record array page: "-> cachedHeading = liveHeading; cachedSpeed = liveSpeed; flags \|= 1;" (Character-Render-Records/the-character-render-record-array.md:262).
- No favoured side by dated text. Lean: the contract (executed 70/70, :355).

**AC.CV-9 V1 allocator writes +0x30 and +0xBC..+0xD4 (page vs TSV)** *(page-text only - needs local check)*
- "`003B56D0`, `003B6000`, `003B5890`, … touch no `+0x30`/`+0x34` either. One writer (`003B5CE0`), zero readers" (CONTRACT-authored-command-ramp-channels.md:465-468).
- "not even the allocator (whose init sweep ends at `+0x9C`; the highest written field anywhere is `003B62D0`'s `+0xD4` cache float)" (:473-474).
- vs ramp-channel-record-accesses.tsv rows: `003B56D0 … 003B584C 0x30 w mov qword ptr [rbx + 0x30], rsi`; `003B5850 0xBC w`; `003B5857 0xC4 w`; `003B5877 0xD4 w mov dword ptr [rbx + 0xd4], 0x3f800000`.
- No favoured side by dated text. Lean: TSV.

**AC.CV-10 Role of `00521000`/`00521050`** *(page-text only - needs local check)*
- "The `00520xxx` bodies at `00521000`+ (handle-table allocate/resolve/release, …) are a *different* family — the 256-entry × 48-byte handle table at `02CA8450`" (Authored-Commands/the-authored-presentation-command-handlers.md:169-171).
- vs "**Per node, `00521000` (75 B) does three things.**" — the 0x2F per-node event body (:413). Also "**The per-node body `00521050` (154 B) is a filter and a dispatch.**" for 0x14 (:524).
- No favoured side.

**AC.CV-11 Handler `0x14` role (cross-page)** *(page-text only - needs local check)*
- "`00520E70` | tail into `0042DC10` region" (Character-Render-Records/render-event-selection-evidence.md:537).
- vs "`00520E70` (32 B) passes `word[rec + 0]`, the body `00521050`, and the command pointer" to `00426870` (Authored-Commands/the-authored-presentation-command-handlers.md:522).
- No favoured side. Lean: the handler page (read 2026-09-20).

**AC.CV-12 V2 allocator defaults: three values or `+0x24..+0x38`** *(page-text only - needs local check)*
- "The allocator `003AF340` sets `+0x1F = 0x11` and the three first values to 1.0" (Authored-Commands/the-authored-presentation-command-handlers.md:1049-1050).
- vs "`+0x24..+0x38` = `1.0`, `+0x1C` = `0x11000000`" (Model-And-Motion-Formats/fef-and-motion-entries.md:372). That range also spans the rate fields +0x2C/+0x30/+0x38.
- No favoured side.

**AC.CV-13 Binary of mask 0xB9** *(page-text only - needs local check)*
- "*(`0xB9` is `1000 1001 1` — bits 0, 3, 4, 5 and 7" (Authored-Commands/the-authored-presentation-command-handlers.md:562).
- 0xB9 = 1011 1001, so the bit list is right and the binary string is wrong.
- Arithmetic lean: the bit list. No favoured side by dated text.

#### 3.1.2 [RO] Render-record pool, character render object, transform publish and lighting

Short names in this part: **POOL** = `CONTRACT-render-record-pool-lifecycle.md`; **CRO-C** = `CONTRACT-character-render-object.md`; **PUB** = `CONTRACT-character-transform-publish.md`; **CRO** = `Character-Rendering/character-render-object.md`; **LIT** = `Character-Rendering/how-a-character-is-lit.md`.


**RO.CV-1 PUB is named the consumer of the 0x740 pool, but PUB indexes the object's 0x318 array.** *(page-text only - needs local check)*
- CONTRACT-render-record-pool-lifecycle.md:142-144: "**Consumer:** `CONTRACT-character-transform-publish` operates on records reached by walking the active list from `+0x00`. It sees a record only after `00428710` has promoted it". Also CONTRACT-render-record-pool-lifecycle.md:305 "(`+0x2C` here, and the transform publish path)", CONTRACT-render-record-pool-lifecycle.md:623.
- CONTRACT-character-transform-publish.md:81: "the record at `object+0x58` (stride 0x318)". CONTRACT-character-transform-publish.md:447-449: "a different record array; **not** the 0x318 one this operation indexes". Character-Rendering/character-render-object.md:546-552: "functions referencing BOTH : none … **The intersection is empty**".
- No favoured side. Lean: PUB/CRO (the bytes cited are 0x318 array accesses).

**RO.CV-2 The 0x740 pool base address: three values.** *(page-text only - needs local check)*
- CONTRACT-render-record-pool-lifecycle.md:29-30: "The pointer lives at `0x022C6F28`".
- `Model-And-Motion-Formats/fef-and-motion-entries.md:430`: "at `[02B3EF28]` (pool init `004269A0` → `0041F730` …"; `Authored-Commands/the-authored-presentation-command-handlers.md:1003`: "(pool `0xA0 × 0x740` at `[02B3EF28]`)".
- Character-Rendering/character-render-object.md:883-885: "`imul rbx, rax, 0x740` — the body is a recursive depth-first walk over the 0x740-stride record table based at `[rip+0x1e97f63]` (`02095210`)".
- No favoured side. Lean: `022C6F28` (636/639 references, Character-Rendering/character-render-object.md:546, record-array page).

**RO.CV-3 160 × 0x740 arithmetic.** *(page-text only - needs local check)*
- Character-Rendering/character-render-object.md:538: "`160 × 0x740 = 0x48830`, the offset at which `FUN_00426480` writes a trailing dword".
- CONTRACT-render-record-pool-lifecycle.md:463: "`160 × 0x740 = 0x48800`". `Character-Render-Records/the-character-render-record-array.md:425`: "the product is **0x48800**".
- Lean (arithmetic): 0x48800. CRO's row is uncorrected.

**RO.CV-4 Bank-selector singleton: constructor, zeroing site and width.** *(page-text only - needs local check)*
- Character-Rendering/character-render-object.md:753-757: "constructed by **`00184F20`** (`00189061`) … **`00184F59 mov word ptr [rcx+0x1c], si`**" ("+0x1C IS A WORD").
- CONTRACT-character-transform-publish.md:291-292: "(`Ensure` `00189000`, constructed by `00189CE0`, which zeroes the byte at `0018A0EA`)".
- No favoured side.

**RO.CV-5 What the selector byte means, how many writers it has, and the ordering.** *(page-text only - needs local check)*
- CONTRACT-character-transform-publish.md:278-283: "`00185A1D` … and `001860E6` … are the only two other writers image-wide … `003829D0` chooses between the two writers on that result. So the byte says *default camera versus scripted or event view*". CONTRACT-character-transform-publish.md:303-305: "the byte is rewritten on every camera publish of the frame, before the render objects' slot-13 publish reads it".
- Character-Rendering/character-render-object.md:782: "`+0x1C` counts nothing. It is a two-state pass selector." Character-Rendering/character-render-object.md:787-790 lists **three** `+0x1C` writers: "`00185A1D` writes **1**; `001860E6` writes 0; the method that runs only at 0 writes 0". Character-Rendering/character-render-object.md:795: "`003829D0` calls the two back to back (`00382B21`, `00382B28`)". Character-Rendering/character-render-object.md:799-801: "Not established: when the slot-13 writer … runs relative to those two enqueues … which bank it fills in a given frame is not read here".
- `Scripted-Camera/how-a-camera-reaches-the-renderer.md:46`: "one of two wrappers is called (`001821F0` for the default view, `00182340` otherwise)". This supports PUB's choose-one reading against CRO's "back to back".
- No favoured side on the writer count or the ordering. Lean on choose-one versus back-to-back: PUB plus the camera page.

**RO.CV-6 How many matrices the uploader copies into the binding params.** *(page-text only - needs local check)*
- CONTRACT-character-transform-publish.md:334-336: "`+0x100` `PS2WHMatrix`, `+0x108` `PS2HSMatrix` — and `001FAD50` copies the two 192-byte matrix banks (`+0x4C4` / `+0x584`) into the last two".
- Character-Rendering/character-render-object.md:813-815: three rows, ending "`+0x544` | `+0x604` | `+0x110` | `InvPS2WHSMatrix`". The slot TSV has `0x110 InvPS2WHSMatrix`.
- Lean (TSV): three matrices.

**RO.CV-7 Which flag the uploader banks on.** *(page-text only - needs local check)*
- CONTRACT-character-transform-publish.md:28-36 and §14.1 describe a single selector byte `+0x1C`. CONTRACT-character-transform-publish.md:7 and §11 are silent on `+0x1D`.
- Character-Rendering/character-render-object.md:820-822: "The uploader chooses the bank by byte `+0x1D` … The writer `001FB120` chooses its own bank by byte `+0x1C` … — two flags, not one. *(Corrected 2026-09-25…)*".
- Favoured: CRO, by its dated correction (Character-Rendering/character-render-object.md:821-822). PUB's reader-side model is not corrected.

**RO.CV-8 Null-check address of the second sink.** *(page-text only - needs local check)*
- CONTRACT-character-transform-publish.md:155: "null-tested (`001FB18B`, `001FB1A2`)". CONTRACT-character-transform-publish.md:362: "each null-checked at `001FB18B` and `001FB19F`". CONTRACT-character-transform-publish.md:112 cites `001FB198` as the `+0xE8` read.
- No favoured side.

**RO.CV-9 Is CRO `+0x118` (and `+0x80`) zero-initialised or heap garbage?** *(page-text only - needs local check)*
- Character-Rendering/character-render-object.md:907-923: the ctor does `memset(stack buffer, 0, 0x318)` and copies it to `this+0x78` ("`6 * 0x80 + 0x18 = 0x318`"). Character-Rendering/character-render-object.md:931: "gap `+0x118` 632 = **792**". Character-Rendering/character-render-object.md:933-936: the binder fills that table.
- Character-Rendering/character-render-object.md:1080-1081: "the 632 bytes at `+0x118` are **allocated from an unzeroed heap, never cleared, never written individually, and never read**". Character-Rendering/character-render-object.md:1077: "**No `memset` of `this`.**" Character-Rendering/character-render-object.md:1098: "`+0x80` (144 B) and `+0x420` (96 B), are in the same position".
- No favoured side (both dated 2026-09-18/19). Lean (arithmetic in Character-Rendering/character-render-object.md:929-931): zeroed by the block copy.

**RO.CV-10 Release's `+0x284` bit 2: "live" or "retired".** *(page-text only - needs local check)*
- CONTRACT-render-record-pool-lifecycle.md:271/276: "when `+0x284` has bit 2 set (a live record) … the live bit off, bit 30 on". `Character-Render-Records/the-character-render-record-array.md:675`: "`+0x284` bit 2 (live)".
- CONTRACT-render-record-pool-lifecycle.md:843-844: "`d[+0x284] = (d & ~4) | (1<<30)` — the retired bit cleared, bit 30 set".
- No favoured side. Lean: "live" (two places).

**RO.CV-11 `00427A7D` is cited both as the pool-full return and as a zeroing on the success path.** *(page-text only - needs local check)*
- CONTRACT-render-record-pool-lifecycle.md:578: "both are `xor eax, eax` — `004279E2` (duplicate refused) and `00427A7D` (pool full)".
- CONTRACT-render-record-pool-lifecycle.md:457: "`004279E9 cmp …, 0xA0` / `jge` returning 0, and the `inc` is at `00427A7F`". CONTRACT-render-record-pool-lifecycle.md:460: "`eax` is zero from `00427A7D`", used by the free-cursor compare after the increment.
- No favoured side. Lean: the pool-full return lies near `004279E9`, not 2 bytes before the `inc`.

**RO.CV-12 Who writes tail `+0x1C`.** *(page-text only - needs local check)*
- CONTRACT-render-record-pool-lifecycle.md:136-138: "The rest of that list stands: written only by the constructor and by the reset helper `0042ED30`" (the list includes `+0x1C`). CONTRACT-render-record-pool-lifecycle.md:586 says the same.
- CONTRACT-render-record-pool-lifecycle.md:1050-1052: "`002EBC30` … the keyed setter that writes `xmm0` to `[022C6F28]+0x4881C` … is called by the ActorEntity body `0026C8C0`".
- No favoured side.

**RO.CV-13 The constructor's flag word: 0, or `|= 5`.** *(page-text only - needs local check)*
- CONTRACT-render-record-pool-lifecycle.md:154: "flag word `= 0`".
- `Character-Render-Records/the-character-render-record-array.md:951`: "`004269A0` | 741 B — … `+0x48818 |= 5` + config floats".
- No favoured side. Both can be sequential, but the initial value differs (0 versus 5).

**RO.CV-14 Does the constructor touch `+0x2C`?** *(page-text only - needs local check)*
- CONTRACT-render-record-pool-lifecycle.md:87-89: "a third index … It is not one of the six above and no lifecycle operation here touches it". CONTRACT-render-record-pool-lifecycle.md:587: "no lifecycle operation touches it".
- CONTRACT-render-record-pool-lifecycle.md:154-155: construct writes "`+0x2C` `= 0xFFFF`" (construct is an operation, CONTRACT-render-record-pool-lifecycle.md:49).
- No favoured side. Low impact (scope wording).

**RO.CV-15 Object-layout overlap.** *(page-text only - needs local check)*
- Character-Rendering/character-render-object.md:179-189: vectors at `+0x008..+0x070`, then "`+0x0C .. +0x74` early scalar block (slots 2, 13 read; not characterised)".
- The ranges overlap. Slot 13's read in that range is `+0x58`, the record vector (CONTRACT-character-transform-publish.md:81).
- No favoured side. Lean: the "early scalar block" line is stale.

**RO.CV-16 What `+0x48830` holds.** *(page-text only - needs local check)*
- CONTRACT-render-record-pool-lifecycle.md:816-830: "a rebased POINTER … the caller's POINTER".
- `Character-Render-Records/the-character-render-record-array.md:952`: "`0020E620` image-pointer store of the `0xA0` handle into pool `+0x48830`". The same page at :427 says "registers capacity 0xA0 — the argument is **unused**".
- No favoured side.

**RO.CV-17 Which list `003AC110` walks.** *(page-text only - needs local check)*
- Character-Rendering/how-a-character-is-lit.md:185-186, 190: the light list is `02B3F508`/`02B3F510`, and `003AC110` is "The light list has a second walker".
- Character-Rendering/how-a-character-is-lit.md:332: "`003AC110` (1876 B) is the record-less light gather - `01FD4A78` list".
- No favoured side.

**RO.CV-18 Slot 13's call site reads the getter as one or two instructions (role, minor).** *(page-text only - needs local check)*
- CONTRACT-character-render-object.md:121 / :245: "the one-instruction accessor `00189120`".
- CONTRACT-character-transform-publish.md:82: "`mov rax, qword ptr [rip + 0x1df6471]; ret`" and CONTRACT-character-transform-publish.md:119 "a two-instruction getter". Arithmetic check: 0x189127 + 0x1DF6471 = 0x1F7F598, consistent.
- No behaviour change. Recorded because CONTRACT-character-render-object.md:118 also names the call site "`001FB1AC`" as the "shared accessor". Low.

#### 3.1.3 [RA] The character render record array, render events, focus point and track pick

Short names in this part: **CRR** = `Character-Render-Records/the-character-render-record-array.md`; **RES** = `Character-Render-Records/render-event-selection-evidence.md`; **FOC** = `Character-Render-Records/the-focus-point-of-a-character.md`; **TRK** = `Character-Render-Records/how-a-presentation-entry-picks-its-track.md`.


**RA.CV-1. What `00426480` stores at +0x48830.** Character-Render-Records/the-character-render-record-array.md:77-80 "never uses the argument — its entire body encodes the other parameter … `= EncodeImageAddress(param_2);`" vs Character-Render-Records/the-character-render-record-array.md:952 "`0020E620` image-pointer store of the `0xA0` handle into pool `+0x48830`". No favoured side; lean Character-Render-Records/the-character-render-record-array.md:77-80, agreeing with `CONTRACT-render-record-pool-lifecycle.md:817-823` ("`mov rcx, rdx ; the caller's POINTER`"). *(page-text only - needs local check)*

**RA.CV-2. Shadow pool A record shape.** Character-Render-Records/the-character-render-record-array.md:684 "a **160-slot, `0xE0`-byte pool at the pointer `02B40528`**" vs Character-Render-Records/the-character-render-record-array.md:966 "create-once `0x8C00`→`02B40528`; flag clears over 80×`0x1C0` records". No favoured side; lean 0xE0 per `CONTRACT-authored-command-ramp-channels.md:489` ("`0x50` iterations clearing two records at `0x1C0` stride"). *(page-text only - needs local check)*

**RA.CV-3. Role of +0x114.** Character-Render-Records/the-character-render-record-array.md:683-686 (handle of the shadow pool-A entry) vs Character-Render-Records/the-character-render-record-array.md:880-881 "**`+0x114` `animPhaseHandle`** read beside it". No favoured side; lean Character-Render-Records/the-character-render-record-array.md:683 (body-read). *(page-text only - needs local check)*

**RA.CV-4. Roles of record words +6 / +8 / +0xA.** Character-Render-Records/the-character-render-record-array.md:903 "**`+0x6` `ownArrayIndex`** — … to compute the record's own base address; **`+0x8` `nextLinkedIndex`** …; **`+0xA` `altLinkedIndex`** — same pattern for an alternate/parent linked record" vs Character-Render-Records/the-character-render-record-array.md:1061-1062 "through the parent index `+6`, the parent record's" and Character-Render-Records/the-character-render-record-array.md:1043-1044 "the record's two child chains (words `+8` and `+0xA`)"; Character-Render-Records/how-a-presentation-entry-picks-its-track.md:105 "a parent (word `+6`)"; `CONTRACT-coast-down-latch.md:416` "`+0x006` is the record's owner link". No dated correction on CRR; lean parent/child reading (three sources, plus dated 2026-09-22 answer in the contract). *(page-text only - needs local check)*

**RA.CV-5. +0x670..+0x678 and +0x66C/+0x66D roles.** Character-Render-Records/the-character-render-record-array.md:907 "**`+0x674`/`+0x678` are the previous X/Y scalars** for that interpolation" and "`+0x66D` … bit 1 gating the three-channel auxiliary transform interpolation" vs Character-Render-Records/the-focus-point-of-a-character.md:66 "The transformed point goes to **`+0x670**`" and Character-Render-Records/the-focus-point-of-a-character.md:82 "when bit 1 of `+0x66D` is up, snaps to it once and clears the bit". Favoured: FOC, by the dated correction Character-Render-Records/the-character-render-record-array.md:893 "*(corrected 2026-09-19, FABLE: not a blend factor - `+0x670`/`+0x674`/`+0x678` are the three components of the character's focus point…)*" — but the correction was applied only to +0x678 at line 893 and not to line 907. *(page-text only - needs local check)*

**RA.CV-6. `0016D6A0` as a re-resolve helper.** Character-Render-Records/the-character-render-record-array.md:862-863 "value 1 makes the chain walker `0042A580` run the re-resolve helper `0016D6A0`" vs Character-Render-Records/the-character-render-record-array.md:785-789 "*Corrected 2026-09-19 …* `0016D6A0` is `ret 0`: an **empty function**". Favoured: empty function (dated correction Character-Render-Records/the-character-render-record-array.md:785; also Character-Render-Records/the-character-render-record-array.md:790, :1054). *(page-text only - needs local check)*

**RA.CV-7. Timed-hold count when the command word is −1.** Character-Render-Records/how-a-presentation-entry-picks-its-track.md:137 "a command value of -1 is stored as -1" (and `Model-And-Motion-Formats/fef-and-motion-entries.md:997` "(a value of -1 stays -1)") vs `Authored-Commands/the-authored-presentation-command-handlers.md:285` "(or 1 when the word is -1)" and `fef-and-motion-entries.md:314` "(with a `−1→1` coercion)". No favoured side (TRK's falsification T7 checked only `01DFE0B4`, Character-Render-Records/how-a-presentation-entry-picks-its-track.md:202). *(page-text only - needs local check)*

**RA.CV-8. Meaning of presentation-entry `+0x0C` bit 12.** Character-Render-Records/how-a-presentation-entry-picks-its-track.md:38 "bit 12 *tracks start flagged `0x20`*" vs Character-Render-Records/render-event-selection-evidence.md:274-275 "optionally calls `002ED570` / `00372280` under entry `+C` bit `0x1000`" (bone-state reset flag, sole setter `0041D4D0`, Character-Render-Records/render-event-selection-evidence.md:444) vs Character-Render-Records/how-a-presentation-entry-picks-its-track.md:152-153 lead "bit 12 … 'update me in the first pass'". Possibly all true together; no favoured side. (Separate from the completion flag at `+0x2C8` bit 12, Character-Render-Records/render-event-selection-evidence.md:76.) *(page-text only - needs local check)*

**RA.CV-9. Dirty pass membership of +0x290 bits 18 and 27.** Character-Render-Records/the-character-render-record-array.md:742 Pass 1 "`+0x290` bits {2,3,12,19,20,22,23,24,25,29,30}" (no 18) and Character-Render-Records/the-character-render-record-array.md:744 Pass 3 "`+0x290` bits {26,27,28,31,9-again}" vs Character-Render-Records/the-character-render-record-array.md:746 Pass 4 "{4,5,6,13,14,15,16,21,27}" and the TSV (bit 18 in pass 1 at `00427F94`; bit 27 only in pass 4). No dated correction; lean TSV (block counts 13/26 only add up with the TSV lists). *(page-text only - needs local check)*

**RA.CV-10. `01DFE0B4` width and value.** Character-Render-Records/the-character-render-record-array.md:174 "`u32`"; Character-Render-Records/how-a-presentation-entry-picks-its-track.md:136-137 "frames-per-tick word `01DFE0B4`"; Character-Render-Records/the-focus-point-of-a-character.md:69 "`8 * [01DFE0B4]`" "frame-rate multiplier"; `CONTRACT-coast-down-latch.md:284-285` read as dword and signed byte, "Its value is `2`" vs `CONTRACT-coast-down-latch.md:349` "which holds `1` in the shipped image". No favoured side. Value matters for FOC's nibble reload (RA.G-1) and the latch threshold Character-Render-Records/the-character-render-record-array.md:133. *(page-text only - needs local check)*

**RA.CV-11. Entry `+0x18` = primary or current state in class 0x03.** Character-Render-Records/how-a-presentation-entry-picks-its-track.md:134-135 "On the **primary** track it does one thing: raises entry flag bit 3" (entry +0x18 is "the primary track's state", Character-Render-Records/how-a-presentation-entry-picks-its-track.md:39) vs `Authored-Commands/the-authored-presentation-command-handlers.md:285` "If the command's state is the entry's current one it only raises entry flag bit 3" (current = +0x388, Character-Render-Records/how-a-presentation-entry-picks-its-track.md:49). Lean primary (`fef-and-motion-entries.md:314` "if `rec == ctx+0x18`"); no favoured side. *(page-text only - needs local check)*

**RA.CV-12. Handler id range 75 vs 76.** Character-Render-Records/render-event-selection-evidence.md:492 "**75-slot handler-pointer arrays**" (0x258/8) vs Character-Render-Records/render-event-selection-evidence.md:502-503 "`word[record] & 0x7F` clamped to `0x4B` … so the table covers all 75 ids" (0..0x4B is 76) and Character-Render-Records/render-event-selection-evidence.md:510 "the top three slots `0x49`–`0x4B` are **NULL**". Lean: pair table has 76 entries, banks 75; no favoured side. *(page-text only - needs local check)*

**RA.CV-13. Where 160 is enforced (modding/porting capacity).** Character-Render-Records/the-character-render-record-array.md:494-496 "**160 is compiled into three immediates in one function**, and the allocation size is a fourth literal … patching all four" vs Character-Render-Records/the-character-render-record-array.md:655-656 `0042FB80` "refusing when the live count is 160 or more (`0042FC08`)" and Character-Render-Records/render-event-selection-evidence.md:494-496 (`004269A0` walks "`0xA0` records at `0x740` bytes each"). No favoured side; there are more than four sites. *(page-text only - needs local check)*

**RA.CV-14. +0x734 values.** Character-Render-Records/the-character-render-record-array.md:888-889 "a per-kind constant (`2.0`/`1.7`/`1.3`)" vs Character-Render-Records/the-character-render-record-array.md:376 full by-name table (1.5, 1.2, 1.6, 1.1, 1.0 also; chosen by directory letter and name). Lean Character-Render-Records/the-character-render-record-array.md:376 (narrowed 2026-09-18 dated, the tier list is the same date); no favoured side. *(page-text only - needs local check)*

#### 3.1.4 [RG] Rig controllers, fades, status looks, bone trails and the staged look

Short names in this part: **FADE** = `Character-Render-Records/how-a-character-fades-the-ten-channels.md`; **STAT** = `Character-Render-Records/how-a-status-shows-on-a-character.md`; **TRAIL** = `Character-Render-Records/the-bone-trails.md`; **RIG** = `Character-Render-Records/the-rig-of-seventeen-controllers.md`; **LOOK** = `Character-Render-Records/the-staged-look-command.md`.


**RG.CV-1 `003E5D00` immediate set: do the other three words go to zero, or is the value echoed into `step`?** *(page-text only - needs local check)*
- Character-Render-Records/how-a-character-fades-the-ten-channels.md:68 "`base = value * 4096`, the other three words zero."
- Character-Render-Records/how-a-character-fades-the-ten-channels.md:570-573 "the word lands at `[rcx + idx*8 + 0x4C0]` with the `[+0x4C2]` dword zeroed and the word echoed at `[+0x4C6]` - an 8-byte stride element restamp."
- If echoed, `step` = value*4096 (non-zero), and the stepper then runs on that channel. No favoured side.

**RG.CV-2 `003E4370` stepper finish rule: `base += delta` or `base := delta`; step cleared or not.** *(page-text only - needs local check)*
- Character-Render-Records/how-a-character-fades-the-ten-channels.md:73-75 "if `progress` has reached `0x1000` the ramp is finished - `base += delta`, and `progress` and `step` are cleared together".
- Character-Render-Records/how-a-character-fades-the-ten-channels.md:679-681 "each live `word[+6]` step adds into `word[+4]` until it reaches `0x1000`, where `word[+0]` takes `word[+2]` and the `+4` counter resets".
- Falsification RG.S-2 checks only "ten channels from `+0x4C0`, the `0x1000` finish test" (Character-Render-Records/how-a-character-fades-the-ten-channels.md:841), not the update. No favoured side (lean: section 2, as base+delta is the only form consistent with the value formula).

**RG.CV-3 Composite scalar `003E4730`: `/4096 ... /255` vs `x 2^-13 x [00D117C8]`.** *(page-text only - needs local check)*
- Character-Render-Records/how-a-character-fades-the-ten-channels.md:154 "`(+0x4B4 / 4096) * [+0x22C] * [+0x2EC] / 255`".
- Character-Render-Records/how-a-character-fades-the-ten-channels.md:671-673 "multiplied by `00D117C0` (2^-13), `float[+0x22C]`, `float[+0x2EC]` and `00D117C8`".
- 2^-13 is 1/8192, not 1/4096; they agree only if `00D117C8` = 2/255. Value of 00D117C8 not stated. No favoured side.

**RG.CV-4 Ramp starter target scale sign: 4096 vs -4096.** *(page-text only - needs local check)*
- Character-Render-Records/how-a-character-fades-the-ten-channels.md:63 "`delta = (int)(target * 4096) - base`".
- Character-Render-Records/how-a-character-fades-the-ten-channels.md:458 "target scaled by -4096" and Character-Render-Records/how-a-character-fades-the-ten-channels.md:840 "the target scaled by `00D117DC` = −4096".
- Probably a compiled negation, but the page never reconciles. No favoured side.

**RG.CV-5 Chain test `00420FB0`: bits 3, 4, 5 on every ancestor, or bit 3 only on ancestors.** *(page-text only - needs local check)*
- Character-Render-Records/how-a-character-fades-the-ten-channels.md:240-241 "bits 3, 4 and 5 of `+0x284` all up on this record *and on every ancestor up the parent chain*".
- Character-Render-Records/how-a-character-fades-the-ten-channels.md:615-617 "`+0x284` bit 3 plus `(flags & 0x30) == 0x30` gate the same `word[+6]` walk, continuing while bit 3 persists on each linked record".
- Runtime effect is masked today (bit 5 never set, Character-Render-Records/how-a-character-fades-the-ten-channels.md:260-267), but a port with a live bit 5 would differ. No favoured side.

**RG.CV-6 Bone-trail pool addresses: 02CA8420 family vs 02A48F40 family.** *(page-text only - needs local check)*
- Character-Render-Records/the-bone-trails.md:91-93 "at `02CA8420` ... live count `02CA8400` (u16) ... list head `02CA8408` and tail `02CA8410`"; B1 at Character-Render-Records/the-bone-trails.md:497 confirms 02CA8420/02CA8400..02CA8410.
- Character-Render-Records/the-bone-trails.md:449-452 (`0051BC10`) "`cl * 0x3C0` into the `02A48F40` slot table ... the global count `02A48F04` decrements ... (head/tail at `02A48EF4`/`02A48F08`".
- The differences are not one constant (0x25F4E0, 0x25F4FC, 0x25F514), so not a simple rebase. Other pages: Character-Render-Records/how-a-character-fades-the-ten-channels.md:380, `Model-And-Motion-Formats/fcp-character-parameter-block.md:608`, `../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md:848-849` all say 02CA8420. Lean (count of sources + falsification B1): 02CA8420. No dated correction, so no favoured side.

**RG.CV-7 Trail template UNPACK size: NUM 0x45 vs num=27.** *(page-text only - needs local check)*
- Character-Render-Records/the-bone-trails.md:192 "`0x6C` UNPACK | NUM `0x45`, ADDR 0".
- Character-Render-Records/the-bone-trails.md:331 "`UNPACK V4-32 num=27` at `+0x1C`" and Character-Render-Records/the-bone-trails.md:344 "`UNPACK V4-32 num=27 addr=0`".
- 0x45 = 69 quadwords (payload +0x20..+0x470, ending exactly at the MSCALF word at +0x470, Character-Render-Records/the-bone-trails.md:194), 27 = 0x1B quadwords (+0x20..+0x1D0). Lean from arithmetic: 0x45 lines up with the MSCALF offset; but FLUSHE at +0x424 (Character-Render-Records/the-bone-trails.md:193) would then sit inside the payload. No favoured side.

**RG.CV-8 `00428AF0` field width and clear mask: two bits vs three bits, mask clears bits 17-26.** *(page-text only - needs local check)*
- Character-Render-Records/how-a-status-shows-on-a-character.md:269 "sets a two-bit field of the render record (`00428AF0`, arguments 1, 1 and the mask byte `0x60`)".
- Character-Render-Records/how-a-status-shows-on-a-character.md:481-484 "`+0x304` is masked `0xF801FFFF`, then `((r9b << 1 | r8 & 1) << 1 | edx & 1) << 0x11` is folded in - three flag bits at `+0x304`[17..19] - and `+0x294` gets `0x4000000`."
- Mask check: 0xF801FFFF clears bits 17..26 (ten bits), not just 17..19; so the setter also zeroes bits 20..26. Character-Render-Records/the-bone-trails.md:469 (004295E0 extracts bits 17/18/19) agrees with three bits. No favoured side on the field width; the mask arithmetic itself is self-consistent and wider than either prose.

**RG.CV-9 `0051E510` per-node call: virtual slot 25 vs direct `0017F240`.** *(page-text only - needs local check)*
- Character-Render-Records/how-a-status-shows-on-a-character.md:296-297 "calls **virtual slot 25 of each piece's render object** (record `+0x6B8`) with 1, or 0 on leaving".
- Character-Render-Records/how-a-status-shows-on-a-character.md:500 "a live record runs `0017F240([rbx+0x6B8], edx)`".
- Possibly 0017F240 is a thunk to slot 25; neither section says so. No favoured side.

**RG.CV-10 eyemove `003E2810` arguments: (x, y, z) vs (frames, x, y).** *(page-text only - needs local check)*
- Character-Render-Records/the-staged-look-command.md:80 "`003E2810` `(controller, x, y, z)`" with "floats `+0x40`..`+0x48`".
- Character-Render-Records/the-staged-look-command.md:182-183 "`003E2810` `(rig, frames, x, y)` (215 B) writes the eye object: the timer `+0x2C` := frames, and a per-frame velocity `+0x1C`, `+0x20` := (target - current) / frames".
- No favoured side (lean: section 4a, read whole with anchors Character-Render-Records/the-staged-look-command.md:257).

**RG.CV-11 Minimum-duration floor: `[01DFE0B8] * controller[+0x18]` vs `1.0f * [+0x18]`.** *(page-text only - needs local check)*
- Character-Render-Records/the-staged-look-command.md:102 "`frames = max(frames, [01DFE0B8] * controller[+0x18])`".
- Character-Render-Records/the-staged-look-command.md:462 (`003E3340`) "`1.0f * [rdi+0x18]` is `maxss`-floored at the caller's xmm argument".
- Falsification L5 (Character-Render-Records/the-staged-look-command.md:480) "all three minimum-duration variants read `[01DFE0B8]`". 01DFE0B8 ships as 1.0 (`Effect-File-Formats/effect-element-type-dispatch.md:949-950`), so they agree only at 30 fps. Lean: section 3 (L5). No dated correction.

**RG.CV-12 Record `+0x114`: shadow handle vs animPhaseHandle.** *(page-text only - needs local check)*
- Character-Render-Records/how-a-character-fades-the-ten-channels.md:353-354 "the side object of step 2 below, behind the handle `+0x114`, is **the character's shadow**"; Character-Render-Records/how-a-status-shows-on-a-character.md:277-278 same.
- `Character-Render-Records/the-character-render-record-array.md:880-881` "**`+0x114` `animPhaseHandle`** read beside it".
- Role/name conflict a port would carry into its struct. No favoured side (FADE's identification is dated 2026-09-19, Character-Render-Records/how-a-character-fades-the-ten-channels.md:353; the array page's tier text is older but uncorrected).

**RG.CV-13 Record `+0x220`: second colour vs lodScalarVec2.** *(page-text only - needs local check)*
- Character-Render-Records/how-a-character-fades-the-ten-channels.md:180 "instance `+0xA0` := the record's second colour at `+0x220` x the `rgbatrans` colour".
- `Character-Render-Records/the-character-render-record-array.md:900` "**`+0x220` `lodScalarVec2`**".
- No favoured side.

**RG.CV-14 Record `+0x640`: lip-flap timer vs bindingResultDword.** *(page-text only - needs local check)*
- Character-Render-Records/the-rig-of-seventeen-controllers.md:110-111 "the timed forms store `frames / [01DFE0BC]` in `+0x640` (lip flap)".
- `Character-Render-Records/the-character-render-record-array.md:897-898` "**`+0x640` `bindingResultDword`** — written by the binding update `002E3110`".
- Partly reconcilable: Character-Render-Records/the-rig-of-seventeen-controllers.md:318 says 002E3110 "sets the lip-flap bit with a zero timer inline". No favoured side on the field's meaning.

**RG.CV-15 Frame-rate global roles: `01DFE0BC` "low-speed tolerance" vs "reciprocal / time base".** *(page-text only - needs local check)*
- Character-Render-Records/the-bone-trails.md:150 "`step` is the frame-rate time base `01DFE0BC`, 1.0 at the authored rate"; Character-Render-Records/the-rig-of-seventeen-controllers.md:111, :126 use it as the per-frame decrement.
- `Model-And-Motion-Formats/fef-and-motion-entries.md:416-417` "turn-angle scale `01DFE0B8` and the low-speed tolerance `01DFE0BC`"; `Effect-File-Formats/effect-element-type-dispatch.md:949` "`{01DFE0B4 int mode, 01DFE0B8 scale, 01DFE0BC reciprocal}`".
- Values agree (1.0 / 0.5); the names conflict (and Character-Render-Records/the-staged-look-command.md:102 uses 01DFE0B8 as a duration scale, fef calls it turn-angle scale). No favoured side on naming.

#### 3.1.5 [CL] Ordered render command list and graphics-thread handshake

Short names in this part: **C** = `CONTRACT-render-command-list-and-graphics-handshake.md`; **L** = `Render-Command-List/the-ordered-render-command-list.md`; **H** = `Graphics-Thread-Handshake/the-shared-command-state-word.md`.


**CL.CV-1. Slot 2: sort key or mask.** *(page-text only - needs local check)*
- Sort-key side: Render-Command-List/the-ordered-render-command-list.md:30-31 "Every one carries a draw-order number, and that number — not the order the frame enqueued them — decides what ends up in front of what". Render-Command-List/the-ordered-render-command-list.md:45 "runs the list in number order". Render-Command-List/the-ordered-render-command-list.md:139 "That is the draw-order key". Render-Command-List/the-ordered-render-command-list.md:489 "`0x80` | `VideoObj` | composited last, over everything". Render-Command-List/the-ordered-render-command-list.md:519 "later: the list is ordered by slot 2". Render-Command-List/the-ordered-render-command-list.md:572-573 "it is the only thing that determines order — the enqueue sequence does not". README.md:91 "returns a draw-order key".
- Mask side: Render-Command-List/the-ordered-render-command-list.md:197 "the slot-2 value is not a sort key. The walkers run the list in stored order and AND that value as a class mask". Render-Command-List/the-ordered-render-command-list.md:677 "Answered 2026-09-14 (FABLE): none; the list is not ordered by key." CONTRACT-render-command-list-and-graphics-handshake.md:145 "THE ORDER KEY IS A MASK, NOT A SORT KEY, AND NOTHING SORTS."
- **Favoured: mask**, by the dated correction Render-Command-List/the-ordered-render-command-list.md:197 / Render-Command-List/the-ordered-render-command-list.md:677 (2026-09-14).

**CL.CV-2. `+0x10`: enable flag or flushSelector.** *(page-text only - needs local check)*
- Enable side: Render-Command-List/the-ordered-render-command-list.md:113 "+0x10 enabled, on by default". Render-Command-List/the-ordered-render-command-list.md:119 "+0x10 u8 enabled set to 1 by the base constructor". Render-Command-List/the-ordered-render-command-list.md:325 "order 0, enabled 1".
- Flush side: Render-Command-List/the-ordered-render-command-list.md:1918 "`+0x10` is not an `enabled` flag (`CON-149`)". CONTRACT-render-command-list-and-graphics-handshake.md:161-169: the flush "executes the entry when the byte is ZERO … Neither walk tests it at all."
- **Favoured: flushSelector**, by Render-Command-List/the-ordered-render-command-list.md:1894-1928 (2026-09-21).

**CL.CV-3. Whether every enqueue appends to both lists.** *(page-text only - needs local check)*
- Both-lists side: CONTRACT-render-command-list-and-graphics-handshake.md:116-117 "Every enqueue appends the same pointer to both lists". CONTRACT-render-command-list-and-graphics-handshake.md:250-253 "enqueue (x40) … push_back onto the OWNER inline". CONTRACT-render-command-list-and-graphics-handshake.md:208-210 (postcondition): "every command object allocated this frame has had slot 0 called".
- Manager-only side: Render-Command-List/the-ordered-render-command-list.md:650 "4 push into no vector at all, appending to the manager only". Render-Command-List/the-ordered-render-command-list.md:659-660 "none of them pushes into the vector".
- No favoured side. Lean to L, which is dated 2026-09-15 and censused: 40 = 36 + 4. C itself cites "all 40 `0018AFF0` appenders" (CONTRACT-render-command-list-and-graphics-handshake.md:462).

**CL.CV-4. Does the owning vector have a reserve?** *(page-text only - needs local check)*
- Reserve side: CONTRACT-render-command-list-and-graphics-handshake.md:218 "one element array per list, 5,000 entries reserved".
- No-reserve side: CONTRACT-render-command-list-and-graphics-handshake.md:141-143 "`0018C9E0` creates it with begin, end and capacity all zero … with no reserve. It therefore grows on push_back from the first enqueue".
- **Favoured: no reserve on the owner**, by the dated note at CONTRACT-render-command-list-and-graphics-handshake.md:141 (2026-09-25).

**CL.CV-5. Is the grow path ever reached?** *(page-text only - needs local check)*
- Never side: CONTRACT-render-command-list-and-graphics-handshake.md:136-140 "a frame would need five thousand commands to reach it" (the grow branch cited is `0018C664`, the owner's inline push). CONTRACT-render-command-list-and-graphics-handshake.md:273 "the push_back's capacity test at `0018C660` never takes the grow arm in practice (I-3)". CONTRACT-render-command-list-and-graphics-handshake.md:330-331 "Unreached in practice (I-3) and therefore untested by the shipped game". CONTRACT-render-command-list-and-graphics-handshake.md:366 "001AB570 - never reached, see I-3". CONTRACT-render-command-list-and-graphics-handshake.md:474 "The grow path is untested by the shipped game".
- Reached side: CONTRACT-render-command-list-and-graphics-handshake.md:142-143 "grows on push_back from the first enqueue: OPUS's execution measured capacities 1 → 2 → 4 → 8".
- **Favoured: grows (owner)**, by CONTRACT-render-command-list-and-graphics-handshake.md:141 (2026-09-25). CONTRACT-render-command-list-and-graphics-handshake.md:273, CONTRACT-render-command-list-and-graphics-handshake.md:330, CONTRACT-render-command-list-and-graphics-handshake.md:366 and CONTRACT-render-command-list-and-graphics-handshake.md:474 were not updated.

**CL.CV-6. `00600A60`: opens or ends a profile slot.** *(page-text only - needs local check)*
- Opens: Render-Command-List/the-ordered-render-command-list.md:256 "`FUN_00600A60(ctx, n)` opens a numbered profile slot".
- Ends: Render-Command-List/the-ordered-render-command-list.md:1160 "The profile-slot end (`00600A60`, 197 B)". Render-Command-List/the-ordered-render-command-list.md:1166 "`00600A60` requires it set … then clears it … the end".
- No favoured side. Lean: the later interior read (Render-Command-List/the-ordered-render-command-list.md:1158, 2026-09-17).

**CL.CV-7. Key of RenderOpaqueObj and RenderAfterWaterObj.** *(page-text only - needs local check)*
- 0x10 side: Render-Command-List/the-ordered-render-command-list.md:148-149 "`0x10` for the ordinary render passes". Render-Command-List/the-ordered-render-command-list.md:488 "`0x10` | … and the other ordinary passes". README.md:91 "`0x10` for the ordinary passes". All three describe the §2.3 pass rows, which include `RenderOpaqueObj`/`RenderAfterWaterObj` (Render-Command-List/the-ordered-render-command-list.md:170, Render-Command-List/the-ordered-render-command-list.md:174).
- 0x100 side: Render-Command-List/the-ordered-render-command-list.md:1002 "`0x100` | `001F2890` | 4 | `RenderMonsterGalleryChara`, `RenderMapOpaqueObj`, `RenderOpaqueObj`, `RenderAfterWaterObj`". The TSV agrees.
- **Favoured: 0x100**, by the falsification pass at Render-Command-List/the-ordered-render-command-list.md:952-1002 (2026-09-12).

**CL.CV-8. Which allocator creates the lists.** *(page-text only - needs local check)*
- `00210EC0` side: Render-Command-List/the-ordered-render-command-list.md:87 "`list = FUN_00210EC0(0x20)`". Render-Command-List/the-ordered-render-command-list.md:965 "after `FUN_00210EC0(0x20)`".
- `0085E730` side: CONTRACT-render-command-list-and-graphics-handshake.md:218 "through `malloc` `0085E730` (0x30 and 0x20)". CONTRACT-render-command-list-and-graphics-handshake.md:102 "`lea ecx, [rbx + 0x30]` into `malloc`".
- No favoured side.

**CL.CV-9. Does every execute check `01DFE0C4`?** *(page-text only - needs local check)*
- Every side: Render-Command-List/the-ordered-render-command-list.md:386 "a byte; every execute body checks it". Render-Command-List/the-ordered-render-command-list.md:569-570 "Every execute body read in this pass checks it".
- Not-every side: Render-Command-List/the-ordered-render-command-list.md:243-245 shows BegineSceneObj::Execute with no check. Render-Command-List/the-ordered-render-command-list.md:720-721 says ApplyJson's slot 1 "is two instructions — `mov ecx, [rcx+0x18]` then `jmp 001C3C30`". Render-Command-List/the-ordered-render-command-list.md:902 narrows the claim to three bodies.
- No favoured side. Lean: not every.

**CL.CV-10. Number of slots in the base vtable.** *(page-text only - needs local check)*
- 7 slots: CONTRACT-render-command-list-and-graphics-handshake.md:94 "base vtable 009010B8 has 7". CONTRACT-render-command-list-and-graphics-handshake.md:495 "7 slots, slot 5 = `00212C60`".
- 3 slots: the TSV lists `OrderedObject 009010B8` with slots 0-2 only. Render-Command-List/the-ordered-render-command-list.md:310 "Slot 3 exists only in the three `FontBorderOrdered*` classes".
- No favoured side.

**CL.CV-11. GaussianFilterObj run condition.** *(page-text only - needs local check)*
- With master enable: Render-Command-List/the-ordered-render-command-list.md:226-227 checks the profile slot, then "`if (DAT_01DFE0C4 != 0) { ... }`".
- Without it: Render-Command-List/the-ordered-render-command-list.md:498-500 "GaussianFilterObj runs <=> ( … +0x19A … || +0x3E8 … || +0x180 … )", with no `01DFE0C4` term. AO and PostProcess both get one (Render-Command-List/the-ordered-render-command-list.md:497, Render-Command-List/the-ordered-render-command-list.md:501).
- No favoured side.

**CL.CV-12. What `+0x49C` is.** *(page-text only - needs local check)*
- Boolean: CONTRACT-render-command-list-and-graphics-handshake.md:296 "`+0x49C` (read through `0018D630`) chooses which side of the `+0x2C` mark the reverse walk covers". CONTRACT-render-command-list-and-graphics-handshake.md:380 uses it as truthy.
- Index: Render-Command-List/the-ordered-render-command-list.md:812-813 "`+0x49C` is `contextIndex`, a ctor-set signed dword the render methods sign-extend as an index (25 sites)".
- No favoured side.

**CL.CV-13. Which list owns, as stated on H.** *(page-text only - needs local check)*
- Graphics-Thread-Handshake/the-shared-command-state-word.md:925: `0018CA50` "pushes onto the `[rcx+8]`/`[rcx+0x10]` vector …, and `0018B4E0`'s owner receives it through the `0018AFF0` tail".
- CONTRACT-render-command-list-and-graphics-handshake.md:118: "The owning vector destroys; the ordered list never does."
- No favoured side, but C's ownership model is the one proven. This is a role wording on H.

**CL.CV-14. What "the shared command state" is.** *(page-text only - needs local check)*
- The word: Graphics-Thread-Handshake/the-shared-command-state-word.md:29 "One 32-bit global is the entire handshake". Graphics-Thread-Handshake/the-shared-command-state-word.md:57 "`0x02EBA3F8` — a single `dword`".
- Other things: Graphics-Thread-Handshake/the-shared-command-state-word.md:724-725 "the `01FD3AE0`..`01FD3B14` block is the shared command state". Six bodies at Graphics-Thread-Handshake/the-shared-command-state-word.md:563-587 are called "a shared-command-state body" with no reference to `02EBA3F8`. Graphics-Thread-Handshake/the-shared-command-state-word.md:921 calls a JSON-bank reset "the per-epoch rollback of the shared command buffer".
- No favoured side.

**CL.CV-15. Who builds "the ordered list".** *(page-text only - needs local check)*
- Render-Command-List/the-ordered-render-command-list.md:1215 "`00224570` (763 B) is the ordered-list builder".
- CONTRACT-render-command-list-and-graphics-handshake.md:60 "`0018B480` (85 B) make the ordered list, `0018AD00` (105 B) its constructor". Render-Command-List/the-ordered-render-command-list.md:1027 makes `0018B480` the only setter.
- No favoured side.

**CL.CV-16. Role of `001C6E20`.** *(page-text only - needs local check)*
- ApplyJson side: Render-Command-List/the-ordered-render-command-list.md:726 "In the loader `001C6E20` the argument picks the bank" (said of ApplyJson's argument).
- ReadPresetDof side: Render-Command-List/the-ordered-render-command-list.md:738 "`001C6E20`, the body behind `ReadPresetDofForCutSceneObj`, parses `JsonData/0.json`". Render-Command-List/the-ordered-render-command-list.md:720-721: ApplyJson's slot 1 jumps to `001C3C30`, not `001C6E20`.
- No favoured side.

#### 3.1.6 [GP] Gi render commands and the legacy PS2 GS/VIF layer

Short names in this part: **GI** = `Gi-Render-Commands/gi-render-command-family.md`; **TEX** = `Legacy-PS2-GS/texture-mip-local-memory-budget.md`; **VIF** = `Legacy-PS2-GS/the-vif1-vu1-layer.md`.


**GP.CV-1 Which device slots GiTrans / GiTransNz / GiNormal call.** Page-text only - needs local check.
- Gi-Render-Commands/gi-render-command-family.md:313-318: "GiColorRect  GiNormal  GiPolyGT4T  GiPrim / GiScreenImage  GiSprite  GiTrans  GiTransNz / all:  +0x78  ->  +0x98  ->  +0x80" and Gi-Render-Commands/gi-render-command-family.md:916 "The `+0x78 → +0x98 → +0x80` triple holds at 8 of 8."
- Gi-Render-Commands/gi-render-command-family.md:166-167: "misses `GiTrans`, `GiTransNz`, `GiNormal` and `GiZNormalOnOff` entirely, which reach the device only through `+0x78`/`+0x88`/`+0xA0`/`+0xA8`."
- Gi-Render-Commands/gi-render-command-family.md:1642: "`00862D40` (269 B) is the `GiTrans` slot-1 row body - ... plus `call [rax+0x88]`/`[rax+0xA8]`/`[rax+0xA0]`/`[r10+0x78]` vcalls" (same set for GiTransNz, Gi-Render-Commands/gi-render-command-family.md:1646); GiNormal Gi-Render-Commands/gi-render-command-family.md:1638: "`call [r10+0x78]`/`[rax+0x98]`/`[rax+0x80]`/`[rax+0x88]`".
No favoured side (§6 and the interior reads agree for GiTrans; §6 disagrees with Gi-Render-Commands/gi-render-command-family.md:1638 for GiNormal).

**GP.CV-2 What device slot 0 does with the count ("reserve n vertices").** Page-text only - needs local check.
- Gi-Render-Commands/gi-render-command-family.md:121: "its body passes literal `4` to the reservation call"; Gi-Render-Commands/gi-render-command-family.md:101 column "reservation count"; Gi-Render-Commands/gi-render-command-family.md:156 "`[dev+0x000]` reserve 4 vertices -> write pointer".
- Gi-Render-Commands/gi-render-command-family.md:86-88: "~~`[dev+0x000]` is vertex reservation~~: (corrected 2026-09-26 ...: slot 0 reserves nothing and ignores the count. It returns a fixed staging area of `0x7FE0` bytes ... The count goes to slot 4 (`+0x20`), whose batcher checks it against 682 and flushes.)"
Favoured: the dated correction Gi-Render-Commands/gi-render-command-family.md:86-88 (also Gi-Render-Commands/gi-render-command-family.md:361-364).

**GP.CV-3 Are the per-class "current command" globals write-only?** Page-text only - needs local check.
- Gi-Render-Commands/gi-render-command-family.md:982-986: "The "singleton" globals are write-only in the retail image. For all 11 globals in the table, every rip-relative reference is the factory's own store ... nothing reads it back."
- Gi-Render-Commands/gi-render-command-family.md:505-507: GiBeginScene "store to `0x01F83078` = `0x01F83070 + 8`, then call `FUN_001FB840(0x01F83070)`" and Gi-Render-Commands/gi-render-command-family.md:494 `001FB840` reads "`rdx = [node+8]`"; Gi-Render-Commands/gi-render-command-family.md:1668: `00863060` (GiSetTexture factory) references "`02EAF918`/`02EAF920`" and calls `001FB840`.
No favoured side. Lean: `01F83078` (in the 11, Gi-Render-Commands/gi-render-command-family.md:969) is a node's +8 read through a pointer, which a rip-relative census cannot see.

**GP.CV-4 Address of the device container.** Page-text only - needs local check.
- Gi-Render-Commands/gi-render-command-family.md:1126-1127: "The walker's third argument is therefore not the table the commands call — it is the container, and `+0x18C0` of it is the device (§12d, §13b)." (third argument = `&GameApplication[0xE8]`, Gi-Render-Commands/gi-render-command-family.md:1097)
- Gi-Render-Commands/gi-render-command-family.md:1326-1327: "`[ctx]` is the magic-static singleton `02CC0410`, and the device is `02CC1CD0` = `02CC0410 + 0x18C0`"; Gi-Render-Commands/gi-render-command-family.md:1368: "`r14`, which comes from an unrelated magic-static singleton `02CC0410`".
Favoured: Gi-Render-Commands/gi-render-command-family.md:1326-1329 / Gi-Render-Commands/gi-render-command-family.md:1366-1373 (dated 2026-09-22, explicit refutation in §20f). Gi-Render-Commands/gi-render-command-family.md:1127 is not struck.

**GP.CV-5 Where and when Gi execute runs (display-list drain vs render pass list).** Page-text only - needs local check.
- Gi-Render-Commands/gi-render-command-family.md:533-538 (path): "-> FUN_003A3740 merge sort, walk ... -> FUN_001F4A10 jmp [cmd_vtable+8](command, device) EXECUTE" presented as one chain.
- Gi-Render-Commands/gi-render-command-family.md:597-598 (2026-09-20): "So the execute site of §12c is reached once per frame from the render pass list, not from the display-list drain — `FUN_003A3740` only files the record".
Favoured: Gi-Render-Commands/gi-render-command-family.md:567-598 (dated §12e). Note the further hop to the render thread (Gi-Render-Commands/gi-render-command-family.md:1263-1301).

**GP.CV-6 Hand-off queue record layout.** Page-text only - needs local check.
- Gi-Render-Commands/gi-render-command-family.md:1204: "`[02CE4720 + i*0x28 + 0x50] = rbx ; +0x20 event`" and Gi-Render-Commands/gi-render-command-family.md:1206 "`005CD5E0(&entry + 0x40) ; signal`".
- Gi-Render-Commands/gi-render-command-family.md:1256-1259: "`+0x10` the per-slot event created above, `+0x20` the completion object `[target+0x78]`. (This corrects §19f, which labelled `+0x20` "the event" and wrote the signal target as `&entry + 0x40`...)"
Favoured: Gi-Render-Commands/gi-render-command-family.md:1256-1259 (§20a, dated 2026-09-22, explicit correction).

**GP.CV-7 Is the command arena rewound each frame?** Page-text only - needs local check.
- Gi-Render-Commands/gi-render-command-family.md:412-415: "the commands come from a bump allocator (§10); and the arena is rewound by a single pointer store per frame" (the rewind cited is `003A3A00` on `[0x02F8F2D0]`, Gi-Render-Commands/gi-render-command-family.md:409-410).
- Gi-Render-Commands/gi-render-command-family.md:998-1000: "a frame that allocates more commands than the arena holds does not fail. It overwrites the frame's earliest commands in place. Not read: whether a caller resets the cursor each frame." (command arena is `[01F7F4C0]`, Gi-Render-Commands/gi-render-command-family.md:325).
No favoured side. Lean: §17, since the rewound pointer `02F8F2D0` is not the command arena `01F7F4C0`.

**GP.CV-8 Role of `001DB220`.** Page-text only - needs local check.
- Gi-Render-Commands/gi-render-command-family.md:971: "`GiVmax` | `001DB220` (from `001DB840`) | `0x640`"; Effect-File-Formats/effect-element-type-dispatch.md:544: "`GiVmax` (`001DB220`, vtable `009007E8`)".
- Gi-Render-Commands/gi-render-command-family.md:1650: "`001DB220` (273 B) is a sound-request body - `0016D6A0`/`001A1470`/`00861EC0`."
No favoured side (lean GiVmax constructor: two statements, arena call).

**GP.CV-9 Role of `00188730`.** Page-text only - needs local check.
- Gi-Render-Commands/gi-render-command-family.md:201: "reset the render target through the renderer (`00188730` for the default target, `001893C0` for the other)".
- Gi-Render-Commands/gi-render-command-family.md:1626: "`00188730` (651 B) is a gi-render CRT-formatter body".
No favoured side.

**GP.CV-10 Role of slot 0 ("prepare").** Page-text only - needs local check.
- Gi-Render-Commands/gi-render-command-family.md:48-49: "Where slot 0 has a real body it resolves resources; slot 1 runs the command against a device."
- Legacy-PS2-GS/the-vif1-vu1-layer.md:193-194: "what is added here is that for a VU1 command prepare is the whole program run." (`GiVmax` slot 0 = `001DB550`, Legacy-PS2-GS/the-vif1-vu1-layer.md:108-109)
No favoured side (GI's sentence is a general summary; VIF reads the body).

**GP.CV-11 How many GS registers the PC replay honours.** Page-text only - needs local check.
- Legacy-PS2-GS/the-vif1-vu1-layer.md:759: "Only 20 GS registers are honoured (§2.1b)."; Legacy-PS2-GS/the-vif1-vu1-layer.md:281 "Twenty cases have handlers".
- Legacy-PS2-GS/the-vif1-vu1-layer.md:843 (2026-09-30): "PACKED can reach only descriptors 0-0xF, so its arms for `0x3B`-`0x4F` are unreachable; A+D drops RGBAQ, ST, UV, XYZ and FOG. FGE, FIX, FOG, FOGCOL, `(int)Q` and ZBUF_1/2 are stored but never read."
Favoured: Legacy-PS2-GS/the-vif1-vu1-layer.md:843 (dated answer). Legacy-PS2-GS/the-vif1-vu1-layer.md:759 not updated.

**GP.CV-12 Program-table index range.** Page-text only - needs local check.
- Legacy-PS2-GS/the-vif1-vu1-layer.md:104-105: "The `0x3FF` masks and the 1,024-entry address space are VU1's." (with Legacy-PS2-GS/the-vif1-vu1-layer.md:60 "stored at `02068E30[addr]`")
- Legacy-PS2-GS/the-vif1-vu1-layer.md:384: "~~1,024 × 8~~ room for 16,384 × 8 ... the MPG arm indexes it with the command's unmasked imm16 ... the only `0x3FF` masks in `0022C970` are the OFFSET and BASE arms'" (corrected 2026-09-25).
Favoured: Legacy-PS2-GS/the-vif1-vu1-layer.md:384.

**GP.CV-13 What `004EF860` writes before the kick.** Page-text only - needs local check.
- Legacy-PS2-GS/the-vif1-vu1-layer.md:674-675: "writes a 16-bit word `+ 0x8000` into the VU cell at register `02064DB0` ...; copies the cell at register `02064DD0` beside it".
- Legacy-PS2-GS/the-vif1-vu1-layer.md:815-817: "a dword at `+0x00` as `word[02064DB8] + 0x8000` ..., then eight bytes at `+0x04` and four at `+0x0C` from a quadword fetched through the other register and staged at `02064C60`".
No favoured side (width word vs dword; full-cell copy vs 12 bytes; source register DB8 named only in UQ-214). Lean UQ-214 (address-level reading).

**GP.CV-14 Size of the VU1 render command (cross-page).** Page-text only - needs local check.
- Character-Render-Records/the-bone-trails.md:165: "queues one render command of `0x488` bytes with the VU1 microprogram `0053F490` through the registrar 003A35E0" (quoted unchallenged at Legacy-PS2-GS/the-vif1-vu1-layer.md:183).
- Legacy-PS2-GS/the-vif1-vu1-layer.md:110: "`001DB840` allocates the `0x640`-byte command"; Gi-Render-Commands/gi-render-command-family.md:971 `0x640`.
No favoured side. Lean: the bone-trails page itself says "`0x18 + 0x488 = 0x4A0`, so the payload ..." (the-bone-trails.md:199), i.e. 0x488 is the payload, 0x640 the object.

**GP.CV-15 Is the texture budget a fixed 176 pages?** Page-text only - needs local check.
- Legacy-PS2-GS/texture-mip-local-memory-budget.md:220-221: "Budget reality for texture mods: a fixed 1.375 MiB / 176 GS pages, minus two runtime totals."; Legacy-PS2-GS/texture-mip-local-memory-budget.md:351-352: "it is a fixed 1.375 MiB / 176 pages on every machine."
- Legacy-PS2-GS/texture-mip-local-memory-budget.md:226 (2026-09-14): "Because the budget is rounded up to whole pages, it stays at 176 pages only while the two totals together are under `0x800` words. "Fixed" therefore means machine-independent, not independent of the area's texture bank."
Favoured: Legacy-PS2-GS/texture-mip-local-memory-budget.md:226 (later dated precision). Lean from arithmetic: one total is "the largest single-record mip-chain footprint" (Legacy-PS2-GS/texture-mip-local-memory-budget.md:226) and every class's minimum is "`0x800` 32-bit words" (Legacy-PS2-GS/texture-mip-local-memory-budget.md:71), so with any record present the totals are ≥ 0x800 and the budget is at most 175 pages.

**GP.CV-16 First published total: single image or whole mip chain.** Page-text only - needs local check.
- Legacy-PS2-GS/texture-mip-local-memory-budget.md:49: "compute the maximum single-image footprint and a weighted aggregate".
- Legacy-PS2-GS/texture-mip-local-memory-budget.md:226: "`00467B10` stores the largest single-record mip-chain footprint (`00466190`, ...)".
Favoured: Legacy-PS2-GS/texture-mip-local-memory-budget.md:226 (dated 2026-09-14).

**GP.CV-17 What "device" is passed to `0018B100` (naming that changes which object a port hands over).** Page-text only - needs local check.
- Legacy-PS2-GS/the-vif1-vu1-layer.md:230-231: "`0018B100(list, whole, device)` twice a frame ... and only then calls slot 1 with the device."; Gi-Render-Commands/gi-render-command-family.md:583 same naming.
- Gi-Render-Commands/gi-render-command-family.md:1126-1128: "The walker's third argument is therefore not the table the commands call ... Both have been written here as the device." (it is `&GameApplication[0xE8]`, a `PRendererBase`, Gi-Render-Commands/gi-render-command-family.md:1097).
Favoured: Gi-Render-Commands/gi-render-command-family.md:1123-1128 (dated 2026-09-22).

#### 3.1.7 [EF] Effect containers, element dispatch and the per-frame element update

Short names in this part: **DISP** = `Effect-File-Formats/effect-element-type-dispatch.md`; **FBF** = `Effect-File-Formats/an-effect-element-frame-by-frame.md`; **EFX** = `Effect-File-Formats/efx-and-efb-effect-containers.md`; **ERM** = `Effect-File-Formats/README.md`; **CAT** = `README.md`.


**EF.CV-1 `02EBEF88`: instance-list root vs frame stamp.** *(page-text only - needs local check)*
"Loads `[02EBEF88]`, then its `+8`" (Effect-File-Formats/effect-element-type-dispatch.md:115) / "write `02EBEF88` … the list's maintenance" (Effect-File-Formats/effect-element-type-dispatch.md:120) / "the `[02EBEF88+8]` list is walked" (Effect-File-Formats/effect-element-type-dispatch.md:1305) / "`+0x1B8` to `02EBEF88`" (`Effect-File-Formats/the-six-vfx-display-layers.md:264`) vs "If `+0x38` already equals the global frame stamp `[02EBEF88]`, it returns 0" (Effect-File-Formats/effect-element-type-dispatch.md:916). No favoured side; lean list root (4 sites).

**EF.CV-2 Element `+0x44`: track time vs expression id.** *(page-text only - needs local check)*
"they sample the definition's tracks (`[element + 0x20]`) at the element's time `+0x44`" (Effect-File-Formats/an-effect-element-frame-by-frame.md:73); "advances `+0x44`" (Effect-File-Formats/effect-element-type-dispatch.md:925-926); "every curve read takes is the element's `+0x44`" (`Effect-File-Formats/the-element-types-00-0a.md:470`) vs "the transform workbench, with the element's expression id" (Effect-File-Formats/effect-element-type-dispatch.md:244) and "with the element's expression id from `+0x44`" (Effect-File-Formats/effect-element-type-dispatch.md:262). No favoured side; lean time.

**EF.CV-3 Element `+0x20`: definition vs "owner".** *(page-text only - needs local check)*
"its definition → `+0x20`" (Effect-File-Formats/effect-element-type-dispatch.md:840); Effect-File-Formats/an-effect-element-frame-by-frame.md:73 vs "`r14 = qword[element + 0x20]` its owner" (Effect-File-Formats/effect-element-type-dispatch.md:236); FBF itself uses "owner" for a different object ("its owner's active list (head `+0x118` …)", Effect-File-Formats/an-effect-element-frame-by-frame.md:135; "the owner's matrix (`[+8] + 0x40`)", Effect-File-Formats/an-effect-element-frame-by-frame.md:185). No favoured side; lean definition.

**EF.CV-4 What advances `+0x3C`: step +1.0 vs base `+= dt`.** *(page-text only - needs local check)*
"adds **1.0 to the element's float `+0x3C`** … the element's frame counter" (Effect-File-Formats/effect-element-type-dispatch.md:68-69); "`+0x3C  f32  frame counter, +1.0 per step (unless paused)`" (Effect-File-Formats/effect-element-type-dispatch.md:878); "frame counter `+0x3C`" (Effect-File-Formats/effect-element-type-dispatch.md:864) vs "Otherwise `+0x3C += dt`, the float in `xmm2`" (Effect-File-Formats/effect-element-type-dispatch.md:916-917) and "The base … advances the element's age `+0x3C` / `+0x44`" (Effect-File-Formats/an-effect-element-frame-by-frame.md:43). Favoured: base, by the dated correction "the step runs once, at the element's birth, not every frame … The per-frame work is the update (§2.2)" (Effect-File-Formats/effect-element-type-dispatch.md:55-58, 2026-09-29).

**EF.CV-5 `001EDDA0`: half-rate test vs "pause predicate".** *(page-text only - needs local check)*
"That predicate is the engine's **half-rate test** … it returns 0 only in half-rate mode" (Effect-File-Formats/an-effect-element-frame-by-frame.md:257-258); "the 27-byte half-rate test" (Effect-File-Formats/an-effect-element-frame-by-frame.md:264) vs "either the pause predicate `001EDDA0` true or `+0x40` bit 0 clear" (Effect-File-Formats/effect-element-type-dispatch.md:931) / "when the pause predicate is false" (Effect-File-Formats/effect-element-type-dispatch.md:936) / "(unless paused)" (Effect-File-Formats/effect-element-type-dispatch.md:878). Polarity of the gates matches; meaning (pause vs rate) differs. No favoured side.

**EF.CV-6 Does `00441970` always walk the chains?** *(page-text only - needs local check)*
"**It then walks one of two element chains** … calling `002F4020(element, instance)` on each" (Effect-File-Formats/effect-element-type-dispatch.md:129) after the switch (Effect-File-Formats/effect-element-type-dispatch.md:124-126) vs "all other kinds (139 of 145) | `00441A89` … **the chains are not walked at all**" (Effect-File-Formats/effect-element-type-dispatch.md:855); "six kinds walk, the rest are skipped" (Effect-File-Formats/effect-element-type-dispatch.md:857-858). No dated correction of §2.4; lean §2.8 (effect-kind-441970.tsv: 139/145).

**EF.CV-7 Handler sharing in step/update tables.** *(page-text only - needs local check)*
"Within the step, update and walk methods each type has its own function. The setup method alone shares handlers" (Effect-File-Formats/effect-element-type-dispatch.md:179-180); audit "no two types share a handler in either table" (Effect-File-Formats/effect-element-type-dispatch.md:20) vs "**47 types reach 38 distinct routines** (some types share one)" (Effect-File-Formats/effect-element-type-dispatch.md:82); "`0x41`/`0xD0` share the 5 B update stub `00464F10`" (Effect-File-Formats/effect-element-type-dispatch.md:890); "the five `0x80`–`0x97` rows share `0044CC10`/`00450480`/`00539320`" (Effect-File-Formats/effect-element-type-dispatch.md:905-906). TSV: step 47 types / 41 handlers. No favoured side; lean TSV (sharing exists in step and update).

**EF.CV-8 Draw-list entry fields.** *(page-text only - needs local check)*
"`qword[+0]` zero, the **24-bit flags** at `+8` …, and a zero `qword` at `+0x10`" (Effect-File-Formats/effect-element-type-dispatch.md:354-355); "each carrying a 24-bit flags word" (Effect-File-Formats/effect-element-type-dispatch.md:361) vs "**The record's `+8` is the sort key, not a flags word.** … The real flags word is the separate `dword[+0x20]`" (Effect-File-Formats/effect-element-type-dispatch.md:562-566) and "handed to the function pointer at its own `+0x10`" (Effect-File-Formats/effect-element-type-dispatch.md:461). Favoured on `+8`: sort key, by the in-page correction under the 2026-09-20 heading (Effect-File-Formats/effect-element-type-dispatch.md:469, 562). `+0x10` zero = null callback is consistent (cf. `the-element-types-00-0a.md:487` "callback null").

**EF.CV-9 `0024D540` role.** *(page-text only - needs local check)*
"from instance creation `0024D540` / `0024D970`" (Effect-File-Formats/effect-element-type-dispatch.md:158) vs "**`0024D540` is the frame's draw setup.**" (Effect-File-Formats/effect-element-type-dispatch.md:432) and `0024D970` "rebases the context's lists and both tables" (Effect-File-Formats/efx-and-efb-effect-containers.md:191). No favoured side.

**EF.CV-10 `002F2D60` flag-byte clear: whole byte vs mask.** *(page-text only - needs local check)*
"clears the flag byte `+0x1`" (Effect-File-Formats/effect-element-type-dispatch.md:840) vs "clears `+1` bits `0xF9`" (Effect-File-Formats/effect-element-type-dispatch.md:1048-1049). Clearing 0xF9 keeps bits 1-2 (0x06), the attachment flags the base tests ("flag byte `+1` bit 1 … bit 2", Effect-File-Formats/effect-element-type-dispatch.md:931). No favoured side.

**EF.CV-11 Setup "creation arm" type labels disagree with the method table.** *(page-text only - needs local check)*
"`00539030` (316 B) is the `+0x44 = 0x47` creation arm (`005004C0` stub 8)" (Effect-File-Formats/effect-element-type-dispatch.md:2082); likewise `00539170` "0x48" (Effect-File-Formats/effect-element-type-dispatch.md:2102), `00538DB0` "0x44" (Effect-File-Formats/effect-element-type-dispatch.md:2098), `00539610` "0x51", `00539740` "0x52", `00539870` "0x53", `005393B0` "0x4E", `005394A0` "0x4F", `00539980` "0x4D/0x54", `00539A60` "0x57", `00539B30` "0x58/0x5D/0x5E", `00539C10` "0x56", `00539DA0` "0x59/0x5A", `00539E90` "0x5B/0x5C", `00539F80` "0x5F" (Effect-File-Formats/effect-element-type-dispatch.md:2086-2138) vs DISP's own table "`0x05` | `00449970` | `00449930` | `00449AB0` | `00538DB0`" (Effect-File-Formats/effect-element-type-dispatch.md:190) and the TSV (0x08, 0x0A, 0x05, 0x88, 0x89, 0x8A, 0x85, 0x86, 0x84/0x96, 0x8B, 0x8C/0x94/0x95, 0x8D, 0x8F/0x90, 0x91/0x92, 0x97). The same labelling error was corrected for six other arms ("Corrected 2026-09-29 (FABLE, GI-10): by `005004C0`'s table and `members/effect-type-methods.tsv` …", Effect-File-Formats/effect-element-type-dispatch.md:2148-2150) but not for these fifteen. No favoured side for these; lean TSV.

**EF.CV-12 Scope of the sub-walk "one shape" family.** *(page-text only - needs local check)*
"**12,463 bytes in eight bodies, and one pattern.**" (Effect-File-Formats/effect-element-type-dispatch.md:260); "five of this page's large entry-only bodies and three smaller siblings are one mechanism, not eight" (Effect-File-Formats/effect-element-type-dispatch.md:283); EC7-66 "arms `00522300`/…/`005271D0`" (Effect-File-Formats/effect-element-type-dispatch.md:1226) vs the page's own "`0052C070` (3790 B) is a `0043ED30` sub-walk arm" (Effect-File-Formats/effect-element-type-dispatch.md:1678), `0052D920`, `0052EA90` (Effect-File-Formats/effect-element-type-dispatch.md:1682-1686), `005294F0` "the default sub-walk's work body" (Effect-File-Formats/effect-element-type-dispatch.md:1802), `00528150` (Effect-File-Formats/effect-element-type-dispatch.md:1806), `0052B080`, `0052A360` (Effect-File-Formats/effect-element-type-dispatch.md:1842-1846), `00528B50` (Effect-File-Formats/effect-element-type-dispatch.md:1934); TSV sub-walk = 17 non-stub handlers. The decode at Effect-File-Formats/effect-element-type-dispatch.md:215-222 routes 0x42, 0x6B, 0x71-0x74, 0xA9-0xAB to in-leaf stubs `0043EDxx`. No favoured side; lean "eight" counts only direct-call arms.

**EF.CV-13 Type 0x05 walk matrix range.** *(page-text only - needs local check)*
"four `movaps` copy `element + 0x250 … +0x27F` — a 4×4 matrix" (Effect-File-Formats/effect-element-type-dispatch.md:622-623) vs "Matrix at `+0x250`, position row `+0x280`" (Effect-File-Formats/an-effect-element-frame-by-frame.md:212). Four 16-byte moves cover `+0x250..+0x28F`. No favoured side; lean (arithmetic) `+0x28F`.

**EF.CV-14 Element links: one list with head/tail vs two chains.** *(page-text only - needs local check)*
"unlinked from its owner's active list (head `+0x118`, tail `+0x128`, links at element `+0x28` / `+0x30`)" (Effect-File-Formats/an-effect-element-frame-by-frame.md:135-136; survives Effect-File-Formats/an-effect-element-frame-by-frame.md:316) vs "the chain at `+0x118`, linked through element `+0x30` …; otherwise the chain at `+0x128`, linked through element `+0x28`" (Effect-File-Formats/effect-element-type-dispatch.md:130-131). No favoured side; lean one doubly-linked list walked from either end.

**EF.CV-15 Expiry test.** *(page-text only - needs local check)*
"with a lifetime `+0x4C` set and the age past it" (Effect-File-Formats/an-effect-element-frame-by-frame.md:43-44) vs "once the even-rounded `trunc(+0x3C)` exceeds it" (Effect-File-Formats/effect-element-type-dispatch.md:920). No favoured side.

**EF.CV-16 Floor-probe gate bit.** *(page-text only - needs local check)*
"only when the definition's `+0x4B` bit 2 is set" (Effect-File-Formats/an-effect-element-frame-by-frame.md:272) vs "when `byte[[rcx+0x20]+0x4B]` lacks bit `4` the answer is `float[[rcx+0x20]+0x70]`" (Effect-File-Formats/effect-element-type-dispatch.md:2182). Lean: same mask 0x04 if "bit 4" means value 4; otherwise bit 2 vs bit 4. No favoured side.

**EF.CV-17 EFX chunk header: 8 bytes vs 16 bytes.** *(page-text only - needs local check)*
"`struct EfxChunk` … `+0x00 u32 length` / `+0x04 u16 flag` / `+0x06 u16 type`" (Effect-File-Formats/efx-and-efb-effect-containers.md:98-102) vs "The chunk header is `{u32 length, u16 0x100, u16 type, i32 +0x08}` … passes the handler `chunk + 0xC`, and the record starts at `chunk + 0x10`" (Effect-File-Formats/efx-and-efb-effect-containers.md:224-226). No explicit correction; lean §2b (2026-09-30, all files).

**EF.CV-18 0x600 handler offsets (record base).** *(page-text only - needs local check)*
"`003A79C0(chunk)` takes the `0x600` chunk's index byte `+1`, stores it at `+4`, resets the 29 dwords from `+0x30` … registers the record `chunk+4`" (Effect-File-Formats/efx-and-efb-effect-containers.md:479) vs "`003A79C0` stores the chunk's index byte at record `+0`, resets the 29 dwords `+0x2C`–`+0x9F`" (Effect-File-Formats/efx-and-efb-effect-containers.md:258-259) with "record starts at `chunk + 0x10`" (Effect-File-Formats/efx-and-efb-effect-containers.md:226). Consistent only if §4's "chunk" is the handler argument (file chunk+0xC). No favoured side.

**EF.CV-19 EFX header `+0x08..+0x0F`.** *(page-text only - needs local check)*
"`+0x08  byte[8]  _unread`" (Effect-File-Formats/efx-and-efb-effect-containers.md:81, 86); "`+0x08 .. +0x0F` | … **yes — no reader in the function body**" (Effect-File-Formats/efx-and-efb-effect-containers.md:391); "a 16-byte header whose second half nothing reads" (Effect-File-Formats/efx-and-efb-effect-containers.md:527) vs "**`+0x08` is the float `1.0` and `+0x0C` is the file's own size**" (Effect-File-Formats/efx-and-efb-effect-containers.md:222-223). Favoured: §2b, by the dated correction "*Corrected 2026-09-30 …: it is not inert. `+0x0C` is the stream length, which four of the loader's six callers read*" (Effect-File-Formats/efx-and-efb-effect-containers.md:615-617).

**EF.CV-20 Load-time normalisation.** *(page-text only - needs local check)*
"**What loading normalises:** nothing in the header. The `0x600` chunk zero-fill (§2) is the only normalisation found" (Effect-File-Formats/efx-and-efb-effect-containers.md:448-449) vs "**`00333C80`, the `0x600` binder, normalises old versions**" (Effect-File-Formats/efx-and-efb-effect-containers.md:258-271). Favoured: §2b, by "*Corrected 2026-09-30 …: `00333C80` rewrites an `EFX0009` / `EFX0008` record into the `EFX0010` layout*" (Effect-File-Formats/efx-and-efb-effect-containers.md:479).

**EF.CV-21 Chunk type `0x710`.** *(page-text only - needs local check)*
"what a `0x600` or a `0x710` chunk *is* is not established" (Effect-File-Formats/efx-and-efb-effect-containers.md:607) vs type list "`0x600 | 0x610 | 0x620 | 0x630 | 0x700 | 0x800 | 0xA00`" (Effect-File-Formats/efx-and-efb-effect-containers.md:101). No favoured side; lean typo for `0x610`.

**EF.CV-22 Type 0x06 float-track destinations.** *(page-text only - needs local check)*
"**ten float tracks** (`+0x1C0`, `+0x1D0` into `+0x240`, `+0x244`; `+0x140`..`+0x160` into `+0x254`..`+0x25C`; `+0x170`..`+0x190` into `+0x248`..`+0x250`; …)" (Effect-File-Formats/an-effect-element-frame-by-frame.md:215-217) vs "ten floats `def+0x140`..`def+0x1D0` -> `+0x240`..`+0x264` (each `def+0x10*k` to its own field)" (`Effect-File-Formats/the-element-types-00-0a.md:482`). No favoured side; lean FBF (explicit permutation).

#### 3.1.8 [ET] Effect element types, kind-0x54 meshes, menu effect registry and VFX layers

Short names in this part: **mesh** = `Effect-File-Formats/effect-mesh-records-kind-54.md`; **00-0a** = `Effect-File-Formats/the-element-types-00-0a.md`; **40-42** = `Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md`; **60-74** = `Effect-File-Formats/the-element-types-60-74.md`; **80-97** = `Effect-File-Formats/the-element-types-80-97.md`; **menu** = `Effect-File-Formats/the-menu-effect-registry.md`; **six-layers** = `Effect-File-Formats/the-six-vfx-display-layers.md`.


**ET.CV-1 Step body order: PRNG before or after the tail.** *(page-text only - needs local check)*
- Effect-File-Formats/the-element-types-80-97.md:50 "identical step `0044CC10` (54 B = base + PRNG `0044B960` + tail `00450CE0`)"; Effect-File-Formats/the-element-types-60-74.md:45 "called inside the step bodies of `0x0A`, `0x60`–`0x62`, `0x65`, `0x66` before the type tail"; Effect-File-Formats/the-element-types-60-74.md:56-57 "base stepper + PRNG `0044B960` + own tail"; Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:66 "base+PRNG+tail".
- Effect-File-Formats/the-element-types-80-97.md:114 "The order is base, then tail, then `0044B960`."; Effect-File-Formats/the-element-types-00-0a.md:200 "base + shared tail `0044C850`, then step-only `0044B960`".
- Favoured side for the 0x80-0x97 band: tail then PRNG — dated correction Effect-File-Formats/the-element-types-80-97.md:112-114 ("Corrected 2026-09-29 (FABLE, GI-11)"); Effect-File-Formats/the-element-types-80-97.md:50 left unstruck. For 0x60-0x66/0xA0: no favoured side (lean: same as 0x0A).

**ET.CV-2 Shared tail `0045B640`: a walk target or the B1 per-frame tail; and 0x95 vs 0x97 outcome.** *(page-text only - needs local check)*
- Effect-File-Formats/the-element-types-80-97.md:82 "`0045B2A0` (`0x95`) | `*rcx != 0` | shared tail `0045B640`"; :86 "`0045BAD0` (`0x97`) | `*rcx != 0` | shared tail `0045B640`".
- Effect-File-Formats/the-element-types-80-97.md:56-57 "identical step `00455390` (… tail `0045B640`)"; :155 "B1 | `0045B640` (`0x8C`/`94`/`95`/`97`) … type `0x05`'s mesh tail".
- Effect-File-Formats/the-element-types-80-97.md:171 0x95 → "textured strip `0x05C` | a prebuilt strip resource"; :173 "`0x81`, `0x8A`, `0x97` | raw GS packets | - | nothing on PC" — same walk target, different results. No favoured side.

**ET.CV-3 Type 0x96 record family.** *(page-text only - needs local check)*
- Effect-File-Formats/the-element-types-80-97.md:46 family B types "`0x8C`–`0x92`, `0x94`–`0x97`".
- Effect-File-Formats/the-element-types-80-97.md:71 "`0x84`/`0x96` — share setup `00539980` (family A + two resource stores)". No favoured side.

**ET.CV-4 Meaning of the `0039B620` value (element `+0x244`/`+0x258`/…): texture index, workbench slot, or mode.** *(page-text only - needs local check)*
- Effect-File-Formats/the-element-types-00-0a.md:242 "adds the element's texture-frame integer (`+0x258`) to a base and publishes the sum as the current texture index (a 13-byte helper)"; Effect-File-Formats/the-six-vfx-display-layers.md:75 "writes the texture-index base".
- Effect-File-Formats/the-element-types-00-0a.md:111 "resolves a workbench slot from element `+0x244` (`0039B620`)".
- Effect-File-Formats/the-menu-effect-registry.md:117 "`+0x338` is the context's base for the mode dword … every element of a context draws with `mode + base` … What the mode dword means once installed is [the workbench page]'s unclaimed item". No favoured side.

**ET.CV-5 Nine-group 4G runs vs stated ranges (0x50 stride).** *(page-text only - needs local check)*
- Effect-File-Formats/the-element-types-60-74.md:114-115 "`0x6B` … **nine** `0042FCF0` 4-track groups at `0x50` stride `+0x1C0`–`+0x3F0`" — (0x3F0−0x1C0)/0x50 = 7 → 8 groups.
- Effect-File-Formats/the-element-types-60-74.md:87-88 0x67 "nested 3×3 loop … of **nine** 4-track groups `+0x1C0`–`+0x460`" — 0x2A0/0x50 not integer; ninth would start at 0x440.
- Effect-File-Formats/the-element-types-60-74.md:144-146 "nine 4-track groups (`+0x120`–`+0x3F0` for `0x72`…)" — 0x2D0/0x50 = 9 → 10 groups; "`+0x190`–`+0x480`" for 0x73/0x74 → 0x2F0/0x50 not integer.
- Contrast Effect-File-Formats/the-element-types-60-74.md:75-76 0x65 "`+0x180`–`+0x400`" = exactly nine. No favoured side (lean: ranges miswritten; check setups).

**ET.CV-6 Record ends that do not match the listed layout.** *(page-text only - needs local check)*
- Effect-File-Formats/the-element-types-60-74.md:62-63 0x61 "four singles `+0x230`/`+0x240`/`+0x250`/`+0x260` … record end `+0x290`" (last single ends 0x270); Effect-File-Formats/the-element-types-60-74.md:338 "over `+0x80`-`+0x290`".
- Effect-File-Formats/the-element-types-60-74.md:78-80 0x65/0x66 trailing 3G at `+0x7B0`/`+0x810` (end 0x7F0/0x850) vs "records end `+0x880`/`+0x8F0`".
- Effect-File-Formats/the-element-types-00-0a.md:156 0x05 "the record reaches `+0x5A0`, the largest of the group" vs Effect-File-Formats/the-element-types-00-0a.md:172-173 0x06/0x07 bundles to `+0x5E0` (+0xF0) and Effect-File-Formats/the-element-types-00-0a.md:395/:400 definition `+0x6D0`/`+0x6D2`; Effect-File-Formats/effect-mesh-records-kind-54.md:156 type-0x05 records "all ≥ `0x640` B". No favoured side.

**ET.CV-7 Count used for the `+0x2C` array.** *(page-text only - needs local check)*
- Effect-File-Formats/effect-mesh-records-kind-54.md:82-83 / :80 "`+0x0C u16 c1A 8-byte count -> +0x1A, array +0x2C`".
- Effect-File-Formats/effect-mesh-records-kind-54.md:198 consumer table header "`+0x2C` 8-byte (count `+0x18`)". Same for shipped data (c1A == c18 always, Effect-File-Formats/effect-mesh-records-kind-54.md:102); differs for any record where they differ. No favoured side.

**ET.CV-8 `00460120` frees directly or through the deferred-free queue.** *(page-text only - needs local check)*
- Effect-File-Formats/the-element-types-60-74.md:95-96 "seventh `00460120` (80 B) calls `003697F0` and touches `+0x338`/`+0x3B0`/`+0x3C0`/`+0x3D0`".
- Effect-File-Formats/the-menu-effect-registry.md:116 "read `+0x338` of OTHER effect objects as a pointer pushed to the deferred-free queue (`005294B0`, `00460120`)". No favoured side.

**ET.CV-9 Global `02EBEF88`: instance list or frame stamp.** *(page-text only - needs local check)*
- Effect-File-Formats/the-menu-effect-registry.md:67 "two of the … **eleven** writers of the effect instance list `02EBEF88`"; Effect-File-Formats/the-six-vfx-display-layers.md:74 "`+0x1B8` at `02EBEF88`"; Effect-File-Formats/effect-element-type-dispatch.md:115 "Loads `[02EBEF88]`, then its `+8`".
- Effect-File-Formats/effect-element-type-dispatch.md:916 "If `+0x38` already equals the global frame stamp `[02EBEF88]`, it returns 0." No favoured side (lean: list pointer).

**ET.CV-10 Step method role: per-frame bracket or birth.** *(page-text only - needs local check)*
- Effect-File-Formats/the-element-types-00-0a.md:49-53 "Step and update therefore share each type's per-frame tail; they differ in the base phase they bracket."; Effect-File-Formats/the-element-types-00-0a.md:98 "the base stepper (1111 B)".
- Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:113 "The step is the element's birth. Every step first calls `002F2D60`, which zeroes the age"; Effect-File-Formats/the-element-types-60-74.md:182-184 "The step method is the element's **birth**". No dated correction on 00-0a; no favoured side (lean birth, later dated sections).

#### 3.1.9 [MF] Model formats: add-motion tables, ADM, FCP, FDM/FOR

Short names in this part: **SKEL** = `Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md`; **ADM** = `Model-And-Motion-Formats/adm-add-motion-tables.md`; **FCP** = `Model-And-Motion-Formats/fcp-character-parameter-block.md`; **FDM** = `Model-And-Motion-Formats/fdm-and-for-entries.md`; **MREADME** = `Model-And-Motion-Formats/README.md`.


**MF.CV-1. The twelve-tunable ids: the default slot bytes (`DD`) disagree between the §3 table and the §6.1 index table.** Page-text only - needs local check.
- Model-And-Motion-Formats/fcp-character-parameter-block.md:215 "`+0x184` → render record `+0x420` | 2 (9) | `0x09000201` (`0x09000807`) | 9 · 0 · 1 (2), or 7 (8)"; Model-And-Motion-Formats/fcp-character-parameter-block.md:216 "`0x09000403` (`0x09000A09`) | 9 · 0 · 3 (4)"; Model-And-Motion-Formats/fcp-character-parameter-block.md:217 "`0x09000504` | 9 · 0 · 4 (5)"; Model-And-Motion-Formats/fcp-character-parameter-block.md:213 "(`0x09000706`) | … or 6 (7)"; Model-And-Motion-Formats/fcp-character-parameter-block.md:214 "(`0x09000908`) | … or 8 (9)"; Model-And-Motion-Formats/fcp-character-parameter-block.md:218 "`0x09052A2F` | 9 · 5 · 47 (42)"; Model-And-Motion-Formats/fcp-character-parameter-block.md:221 "`0x09082032` | 9 · 8 · 50 (32)"; Model-And-Motion-Formats/fcp-character-parameter-block.md:222 "`0x29081131` | 9 · 8 · 49 (17)".
- Model-And-Motion-Formats/fcp-character-parameter-block.md:312 "| 2 | `09000101` | 9 · 1 · 1"; Model-And-Motion-Formats/fcp-character-parameter-block.md:313 "| 3 | `09000303`"; Model-And-Motion-Formats/fcp-character-parameter-block.md:314 "| 4 | `09000404`"; Model-And-Motion-Formats/fcp-character-parameter-block.md:316 "| 7 | `09000606`"; Model-And-Motion-Formats/fcp-character-parameter-block.md:317 "| 8 | `09000808`"; Model-And-Motion-Formats/fcp-character-parameter-block.md:315 "| 5 | `09052B2F` | 9 · v5 · 43 · 47"; Model-And-Motion-Formats/fcp-character-parameter-block.md:325 "| 32 | `09082C32` | 9 · v8 · 44 · 50"; Model-And-Motion-Formats/fcp-character-parameter-block.md:324 "| 31 | `29081031` | 9 · v8 · 16 · 49".
- The two tables agree on file slots (`FF`) and disagree on `DD`, which is the slot every weapon falls back to.
- **Favoured side: §6.1.** The dated answer UQ-219 settles it: Model-And-Motion-Formats/fcp-character-parameter-block.md:371 "*ANSWERED 2026-09-18 (FABLE)* … the float ids run: file = default for slots 0–10 … v4 file 46 ↔ default 42, v5 47 ↔ 43, v8 50 ↔ 44". Model-And-Motion-Formats/fcp-character-parameter-block.md:173 also says "The two slot bytes are equal up to slot 10". The §3 table's own `0x09052A2F` is the v4-style `DD`=42 on a v5 id. Integer `DD` (16 vs 17) is not settled by UQ-219: lean §6.1.

**MF.CV-2. Is unit tunable index 2 scaled by `+0x26C`?** Page-text only - needs local check. Model-And-Motion-Formats/fcp-character-parameter-block.md:215 says index 2's id `0x09000201` gives "× y-scale; `003E6150` leaves it". Model-And-Motion-Formats/fcp-character-parameter-block.md:196 lists "`0x9000101`" among the ids `003E6150` "multiplies by the render record's scale float `+0x26C`", and Model-And-Motion-Formats/fcp-character-parameter-block.md:312 gives index 2 as "`09000101`". **Favoured side: §6.1** (it follows from MF.CV-1's UQ-219 ruling at Model-And-Motion-Formats/fcp-character-parameter-block.md:371). The ruling makes the id `0x09000101`, which the scaling list multiplies.

**MF.CV-3. Section 9: the "read slots" list and its slot types against the readers.** Page-text only - needs local check.
- Model-And-Motion-Formats/fcp-character-parameter-block.md:122 "`f32[49]` slot … slots 0-9, 30, 32-36, 38-41, 43, 45-48 are read".
- Model-And-Motion-Formats/fcp-character-parameter-block.md:338 "Section-9 slots 14–25 are therefore the per-weapon-kind range bands"; Model-And-Motion-Formats/fcp-character-parameter-block.md:341-342 "reads index 33 — slot 31"; Model-And-Motion-Formats/fcp-character-parameter-block.md:223-224 / Model-And-Motion-Formats/fcp-character-parameter-block.md:241 "dword mode" for slots 41, 40 and 43; Model-And-Motion-Formats/fcp-character-parameter-block.md:240 "bit-field mode … slot 48 … slot 45".
- **Favoured side:** the dated narrowing at Model-And-Motion-Formats/fcp-character-parameter-block.md:362 (2026-09-18) lists the slots no id reads as 11-13, 26-29, 37, 42, 44, 51-56, so 10, 14-25 and 31 are read. The `f32` typing of 40/41/43/45/48 also conflicts with the dword/bit-field reads: no dated correction, so no favoured side on the types.

**MF.CV-4. `.adm` group header field types: `u32` / `byte[8]` against float key lanes.** Page-text only - needs local check. Model-And-Motion-Formats/adm-add-motion-tables.md:83-85 has "`+0x00  byte[8] field00` … `+0x08  u32 field08`". Model-And-Motion-Formats/adm-add-motion-tables.md:459-460 says "lane values 0/1/2 select the floats at group `+0x00`/`+0x04`/`+0x08`". **Favoured side: §10.** MA-1 was answered 2026-09-24, Model-And-Motion-Formats/adm-add-motion-tables.md:191-193: "the group header is a keyframe whose lane `field01` is the driven scalar".

**MF.CV-5. The `.adm` "magic" `04 00 01 00` against files with 1 or 2 tracks.** Page-text only - needs local check. Model-And-Motion-Formats/README.md:29 says "`.adm` is `04 00 01 00`". Model-And-Motion-Formats/adm-add-motion-tables.md:44 says "tracks per file | 4 in 35, 2 in 2, 1 in 2", and Model-And-Motion-Formats/adm-add-motion-tables.md:237-238 says "the four files with no such track are exactly the two-track and one-track files". No favoured side. Lean: the ADM census. The four bytes are `trackCount=4` followed by track 0's `field00=1, field01=0`, so 4 of the 39 files would fail a magic check.

**MF.CV-6. What `0037B4D0` is: a per-tick evaluator or the bind body.** Page-text only - needs local check. Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:116-117 calls it "a 3,175-B per-tick evaluator". Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:321 says "`0037B4D0` — the bind body — initializes the model's movement presentation", and Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:341 says "The bind body `0037B4D0`". No favoured side.

**MF.CV-7. `@FOR` record byte `+0x01`: always 0, or the fourth list's packing kind.** Page-text only - needs local check. Model-And-Motion-Formats/fdm-and-for-entries.md:87 says "`+0x01` | u8 = 0 | sampled". Model-And-Motion-Formats/fdm-and-for-entries.md:92 says "its packing kind is `byte[+0x01]` (`0053C22F`)". Model-And-Motion-Formats/fdm-and-for-entries.md:193 says "the 132 fourth lists are all high models' … 18,049 elements" (kind 0 = empty, Model-And-Motion-Formats/fdm-and-for-entries.md:191). No favoured side. Lean: pass 18 (2026-09-30), since non-empty fourth lists need a non-zero kind.

**MF.CV-8. The same offset `+0x208` holds the `@FOR` entry offset (u32) and the LOD view depth (f32).** Page-text only - needs local check. Model-And-Motion-Formats/fdm-and-for-entries.md:47 says "| `+0x208` | `@FOR` | LOD/variant config", and Model-And-Motion-Formats/fdm-and-for-entries.md:98 says "index `rec+0x208` + base `rec+0x1F8`". Model-And-Motion-Formats/fdm-and-for-entries.md:113 says "`depth = f32[object+0x208]` (the camera-space view distance)". `Character-Render-Records/how-a-character-fades-the-ten-channels.md:625-631` resolves a block through `004780B0(word[rcx+0x64])`, with "`+0x208` != -1 … the `[rsi+0x208]` threshold counts". The two may be different objects, but the page names neither. No favoured side.

**MF.CV-9. Width of the `@FTR` `+0x38` override-slot count: u32 or u16.** Page-text only - needs local check. Model-And-Motion-Formats/fdm-and-for-entries.md:289 says "bounds the ordinal by `@FTR u32 +0x38`", and `Model-And-Motion-Formats/ftr-node-table.md:59` says "`+0x38  u32      tailU16`". On the other side, Model-And-Motion-Formats/fcp-character-parameter-block.md:367 has "`word +0x38`", Model-And-Motion-Formats/fcp-character-parameter-block.md:636 has "`word+0x38`", and `Model-And-Motion-Formats/ftr-node-table.md:316` has "`u16 +0x38`". No favoured side.

**MF.CV-10. A `@FDM` descriptor is 0x10 bytes, yet its `+0x0C` field is indexed as an array.** Page-text only - needs local check. Model-And-Motion-Formats/fdm-and-for-entries.md:209 says "record pool: 0x10-stride descriptors", and Model-And-Motion-Formats/fdm-and-for-entries.md:215-216 says "an entry-relative offset to a `0x10` descriptor". Model-And-Motion-Formats/fdm-and-for-entries.md:230 says "`word[desc+0xC + 2·idx]` resolves … to a sub-record". With `s` up to 7 (kind 1) or a full byte (kind 3, Model-And-Motion-Formats/fdm-and-for-entries.md:180-182), `idx ≥ 2` runs past 0x10. No favoured side.

#### 3.1.10 [MM] Motion formats: FEF/motion entries, FRP, FTE/FCT, FTR, oscillator, pose sequencer

Short names in this part: **ACH** = `Authored-Commands/the-authored-presentation-command-handlers.md`.


**MM.CV-1 NameEquals polarity.** "if (NameEquals(blob+0x10, wantName)) -> hit" (Model-And-Motion-Formats/frp-object-container.md:111) and "compares the blob's own name field … against a caller-supplied string" (:136-137) vs "It returns 0 when all 32 bytes match and 1 at the first differing dword, and FRP_FindEntry takes the non-zero return as the hit … so a supplied name would select files whose name differs from it" (:320-323). Favoured: the dated correction "(Corrected 2026-09-30, SWE2-DATA, frp_checks.py N1–N3 …)" (:318-319). No caller passes a name (:323-324). *(page-text only - needs local check)*

**MM.CV-2 @FRP name field width.** "+0x10  char[16]  name" with "+0x20  u32  _zero0" … "+0x2C  u32  _zero3" (Model-And-Motion-Formats/frp-object-container.md:71-75) vs "it compares eight dwords … 32 bytes, so the header's name field is 32 bytes and the four zero dwords +0x20–+0x2C are its NUL tail" (:319-320). Favoured: the 2026-09-30 correction (:318-319); the struct fence at :71 is not updated. *(page-text only - needs local check)*

**MM.CV-3 @FMN kind dword.** "@FMN carries 0x02000211 and a count" (Model-And-Motion-Formats/frp-object-container.md:353) vs "Header {'@FMN', kind 0x02001111 …} — 0x02001111 is constant in all .cm entries" (Model-And-Motion-Formats/fef-and-motion-entries.md:465-466) and "0x02001111 (13,966) and 0x02001011 (4,337)" (Authored-Commands/the-authored-presentation-command-handlers.md:864). Value-changing: `00409190` picks "0xF0 when bit 12 is set, else 0xC0" (Model-And-Motion-Formats/fef-and-motion-entries.md:990); 0x02000211 has bit 12 clear. No favoured side (lean fef/ACH: census-backed). *(page-text only - needs local check)*

**MM.CV-4 @FTE +0x0C.** "+0x00  '@FTE', u32 kind = 0, u32 entryLen, u32 0" (Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:44) vs "count is u32 @ +0x0C (1:615, 2:170, …)" (:78). No favoured side (lean count: records "count of them" :49). *(page-text only - needs local check)*

**MM.CV-5 @FCT +0x0C.** "+0x00  '@FCT', u32 kind = 0, u32 entryLen, u32 0" (Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:93) vs "+0x0C  u32 count (1..8 typical)" (:95) and "Bounds: idx < dword[entry+0x0C]" (:122). No favoured side (lean count, consumer-read). *(page-text only - needs local check)*

**MM.CV-6 @FCT record stride in the builder.** "word[@FCT + (pal+3)·8] summed, 0053B620–0053B64D" (Model-And-Motion-Formats/fdm-and-for-entries.md:154) vs "rec = FCT + 0x30 + idx*0x10" (Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:96) and "0053AB50 reads +0x00 through FCT + (idx + 3) × 16 (0053B62F)" (:217). No favoured side (lean 16: three statements, T2 check). *(page-text only - needs local check)*

**MM.CV-7 Op 0x1D argument mapping to 003E7450.** "else hi nibble gates byte+0x413 counter, lo nibble → 003E7450(obj, byte+3, 0, lo)" (Model-And-Motion-Formats/fef-and-motion-entries.md:333) vs "event = low nibble of the command's byte +2, choice = byte +3 (0xFF = random), unconditional" with signature "003E7450(record, event, choice, onlyIfChanged)" (Model-And-Motion-Formats/the-pose-sequencer.md:138, :143) and Authored-Commands/the-authored-presentation-command-handlers.md:97 "byte +2 low nibble = event … byte +3 = choice". No favoured side (lean pose-sequencer: falsification Q8 "survives", Model-And-Motion-Formats/the-pose-sequencer.md:275). *(page-text only - needs local check)*

**MM.CV-8 Op 0x09 operand: name or index.** "index s16[ctx+0x2A] + word[cmd+2]>>1 (word[cmd+4]==1 selects the alternate arm)" (Model-And-Motion-Formats/fef-and-motion-entries.md:319) and "that record's op 0x09 names the @FMN (index word[cmd+2] >> 1 …)" (:730-731) vs "@FMN is the bone motion such a block binds by name through command 0x09" (Model-And-Motion-Formats/frp-object-container.md:368) and "The payload from +2 is a name. … When the stream header's byte +4 has bit 0 or 1 the payload is instead a word" (Authored-Commands/the-authored-presentation-command-handlers.md:768-771). Selector condition also differs (`word[cmd+4]==1` vs header byte +4 bits 0/1). No favoured side. *(page-text only - needs local check)*

**MM.CV-9 Op 0x03 hold counter, −1 handling.** "fill rec+0x5E = s16[cmd+2] · global_word (with a −1→1 coercion)" (Model-And-Motion-Formats/fef-and-motion-entries.md:314) and "(or 1 when the word is -1)" (Authored-Commands/the-authored-presentation-command-handlers.md:285) vs "stores there signed word +2 of rcx multiplied by word 01DFE0B4 (a value of -1 stays -1)" (Model-And-Motion-Formats/fef-and-motion-entries.md:997). No favoured side (the 2026-10-01 interior table is later but is not marked as a correction). *(page-text only - needs local check)*

**MM.CV-10 Op 0x2C +0x32A role.** "match advances cursor +0x32A" (Model-And-Motion-Formats/fef-and-motion-entries.md:345) vs "When the score is at least signed word +0x32A it stores it there" (:999) and "applied only if it is at least the rank already held (+0x32A)" (Authored-Commands/the-authored-presentation-command-handlers.md:286). No favoured side (lean score/rank). *(page-text only - needs local check)*

**MM.CV-11 @FMW leaf setters: target offset and index form.** "00418650/004186A0/00418700 are the same three group stores factored as leaf setters (f32[obj + nodeKey*0x10 + chIdx*4 + {0x190,0x1B0,0x1D0}])" (Model-And-Motion-Formats/fef-and-motion-entries.md:672-673) vs "004186A0 … stores xmm3 in float +0x1D0 + 4*(4*edx + r8d)" (:1002) and "00418700 … float +0x1B0 + 4*(4*edx + r8d)" (:1003). Read in order, :673 maps 004186A0 to +0x1B0 and 00418700 to +0x1D0 (swapped), and indexes by `nodeKey*0x10` where the driver uses `nodeKey*0x290` (:658). No favoured side (lean :1001-1003 interior reads). *(page-text only - needs local check)*

**MM.CV-12 0041C260 snapshot: which row array.** "0041C260's snapshot arm copies the eight dwords row+0xF0..0x10C to +0x130..+0x14C" in the node-row context where "dword[+0xFC] = the record's container-relative offset", "word[+0x100] = the record's nodeKey" (Model-And-Motion-Formats/fef-and-motion-entries.md:635-645) vs "it strides the index by 0x290 into r14's rows … copies the eight dwords +0xF0..+0x10C down to +0x130..+0x14C" (:923) and "0041C260 strides the runtime records by 0x290" (Model-And-Motion-Formats/ftr-node-table.md:215-216, :262). No favoured side (lean 0x290 bone rows). *(page-text only - needs local check)*

**MM.CV-13 Bone +0x280 bit 0x10 role.** "word[node+0x280] |= 0x10 marks the node dirty when the state flag +0x96 & 0x20 is set" (Model-And-Motion-Formats/fef-and-motion-entries.md:670-671) vs "unless byte[bone+0x280] has bit 0x10, &bone+0x100 … feeds 00372610 … With bit 0x10 set the vec4 is first multiplied component-wise by bone+0x1E0" (:676-680) and "When +0x280 bit 4 is set it composes inline instead" (Model-And-Motion-Formats/ftr-node-table.md:263). Same bit named as "dirty" and as the composer-path selector. No favoured side. *(page-text only - needs local check)*

**MM.CV-14 @FMW name / stream start.** "char[0x10] name at +0x10 (only half the name field — the u16 stream starts at +0x20)" (Model-And-Motion-Formats/fef-and-motion-entries.md:560-561) vs "u32 +0x30 — base offset", "u32 +0x34 — format arm", "u32 +0x40 — channel-track offset table" (:568-578). No favoured side (lean the "Verified fields"). *(page-text only - needs local check)*

**MM.CV-15 Oscillator mode-byte polarity of 02B59D68.** "forced to 0 when [record + 7] is set while 02B59D68 is zero" (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:107-108) vs "While it is set, section 3's mode byte is forced to 0 (the light stage) for records whose byte +7 is set" (:285-286). No favoured side (6b, 2026-09-29, is later but does not mark §3 corrected; lean 6b, consistent with Character-Render-Records/the-rig-of-seventeen-controllers.md:238-239 "skipped while the global 02B59D68 is non-zero"). *(page-text only - needs local check)*

**MM.CV-16 Which modes run the 00415EE0 scope-open.** "The 00415EE0 scope-open (… storing shared table 01FD4A90 to 02CA43C0) runs for modes 0 and 2 only" (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:116-117) vs "shared table stored to 02CA43C0 by mode-1/0 arms" (:363). No favoured side (lean modes 0/2: mode 1 is "the null tier", :111). *(page-text only - needs local check)*

**MM.CV-17 Oscillator record size.** "the owner type of the 0x40-byte oscillator record" (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:194) vs "+0x40 := the direction, and +0x50 := its horizontal perpendicular" (:525) and "S +0x5C is set to the encoded address of the rig's +0x70" (:397). No favoured side (lean ≥0x60). *(page-text only - needs local check)*

**MM.CV-18 Raw [r14] vs resolved object as the +0x3F record.** "[r14] is itself a pointer to the +0x3F-flagged record while 0020E600 maps it to a separate object checked at +6" (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:52-54) vs "rdi inside 0040ACF0 / 0040D890 / 0040F390 is one record (… always reached through the [r14] encoded-id resolve)" with "+0x3F | u8 | flags" in that record (:69-70, :86) and the tail-jump "0040ACF0(obj, dx, r8, r9)" (:59). No favoured side. *(page-text only - needs local check)*

**MM.CV-19 0054B1F0's chain from the record.** "it resolves [r14] → object → [obj + 8] → the entry-array header rsi" (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:167-168) vs "header S | - | +0x00 → the entry array, +0x04 u8 entry count" (:389) and "S +0x08 is set to the encoded address of the rig's own slot +0x78" (:395). No favoured side (lean GI-19, byte-checked 2026-10-01). *(page-text only - needs local check)*

**MM.CV-20 Count field of the 0x50 bone-link list.** "each node of the header's 0x50-stride list (count byte +0x25 low seven bits)" and "each node of the second list (count +0x23) is re-seated on its bone … when its bone index is 0xFFFF" (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:302-306) vs "A | 0x40 | +0x03 u8 count of B; +0x04 → B" with "B | 0x50 | +0x00 u16 bone index (0xFFFF skips)" (:391-392). No favoured side (may be different lists; not reconciled on the page). *(page-text only - needs local check)*

**MM.CV-21 0040AA20 role and the wind ranges.** "0040AA20 / 0040AAD0 | param setup | ◐ call shape" and "runs 0040AA20(record) once, again if flags2 && !001EDDA0()" (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:356, :177) vs "0040AA20 (138 B) is the oscillator tick 0054B1F0 calls while 02CA4390 is armed: … reseeded from 003D8E50 random draws over the 02CA4380/02CA4398 ranges" (Model-And-Motion-Formats/the-pose-sequencer.md:255); the oscillator page has 02CA4380/02CA4398 as bases and 02CA4384/02CA439C as random ranges ("+0x24 = 003D8E50([02CA439C]) + [02CA4398]", :81; :244-246). No favoured side. *(page-text only - needs local check)*

**MM.CV-22 Wind global types.** "02CA4380–02CA439C | .data f32 ×4-ish" (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:366) vs "stores the preset in the byte 02CA4390", "direction and tilt in 02CA4391/02CA4392", "a mode dword (02CA4394 …)", floats at 02CA4380/84/88/8C/98/9C (:243-249). No favoured side (lean 6b, read whole). *(page-text only - needs local check)*

#### 3.1.11 [PP] Post-processing and visual tuning parameters

Short names in this part: **CS** = `Post-Processing/CONTRACT-post-processing-subsystem.md`; **CP** = `Post-Processing/CONTRACT-ppfx-effect-creation.md`; **PI** = `Post-Processing/ppfx-function-identification.md`; **CAT** = `Post-Processing/the-post-processing-effect-catalogue.md`; **VR** = `Visual-Tuning-Parameters/README.md`; **RR** = `Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md`; **RCL** = `Render-Command-List/the-ordered-render-command-list.md`; **HL** = `Post-Processing/members/ppfx-handle-layout.tsv`.


**PP.CV-1. Step 7 lens: constant 35.0 vs `cfg+0x2C`.** *(page-text only - needs local check)*
- Post-Processing/CONTRACT-post-processing-subsystem.md:102 "On, it passes the enable byte `cfg+0x20`, lens `35.0` and focus floats."; Post-Processing/the-post-processing-effect-catalogue.md:945 "enable byte `cfg+0x20`, alternative-focus byte `cfg+0x21`, lens **`35.0`**, floats `cfg+0x24`/`+0x28`/`+0x30`/`+0x34`".
- Post-Processing/CONTRACT-post-processing-subsystem.md:145 "| `+0x2C` | `+0x120` | the `35.0` both loaders pass — the lens length step 7 divides by 1000 |".
- Whether step 7 reads `cfg+0x2C` (authored block +0x120) or an immediate. No favoured side.

**PP.CV-2. Step 7 on-path float set: `+0x24/+0x28/+0x30/+0x34` vs `+0x24/+0x28/+0x2C`.** *(page-text only - needs local check)*
- Post-Processing/the-post-processing-effect-catalogue.md:945 (above) passes `+0x30`/`+0x34` and not `+0x2C`.
- Post-Processing/CONTRACT-post-processing-subsystem.md:137-145 table maps only `+0x18..+0x2C` into `cfg` and names `+0x2C` as step 7's lens. No favoured side.

**PP.CV-3. Step 3 block size: two 16-byte stores vs 0x40-byte copy.** *(page-text only - needs local check)*
- Post-Processing/the-post-processing-effect-catalogue.md:940 "`&cfg+0x9C`: its contents land in two 16-byte stores at `+0x28`/`+0x38` of an object `006CC1F0` resolves".
- Render-Command-List/the-ordered-render-command-list.md:1652-1659 (SWE2-EC7-121, `006CC1F0` entry) "then copies the 0x40-byte block `[rdx]` into `+0x28..+0x58` and clears `+0x24`".
- 0x20 vs 0x40 bytes; also RCL gates `006DB900`/`006DB8C0` on `byte[+0x24]` clear. No favoured side.

**PP.CV-4. Catalogue build timing: start-up / once vs lazy on first post-processed frame and again after reset.** *(page-text only - needs local check)*
- Post-Processing/the-post-processing-effect-catalogue.md:44 "It runs once, at start-up."; Post-Processing/the-post-processing-effect-catalogue.md:754 "start-up / device init"; Post-Processing/the-post-processing-effect-catalogue.md:768 "This runs once; there is no per-frame path through it."; Post-Processing/CONTRACT-ppfx-effect-creation.md:177 "it runs from the caller's initialisation sequence"; Post-Processing/CONTRACT-ppfx-effect-creation.md:188 "Timing — once, during initialisation, before any pass runs."
- Post-Processing/the-post-processing-effect-catalogue.md:814 (dated) "ANSWERED 2026-09-18 (FABLE): it is not start-up at all. The catalogue is built lazily, on the first frame the post-process render command runs … So the 325 techniques are fetched the first time a frame is post-processed, and again after whatever that reset arm tears down".
- Favoured: the lazy reading, by the dated answer Post-Processing/the-post-processing-effect-catalogue.md:814 (2026-09-18); Post-Processing/CONTRACT-post-processing-subsystem.md:42-43 agrees ("once, lazily, from the first post-processed frame"). CP (2026-09-21) "once" is still open against "again after … reset arm".

**PP.CV-5. Role of the `0072DCF0` count: numbered `_Sn` variants vs suffix-table family.** *(page-text only - needs local check)*
- Post-Processing/the-post-processing-effect-catalogue.md:142-146 "`FUN_0072dcf0(this, &this->slot, "tech_DepthOfField_BackgroundLayerMaskT1_Sn", 0x19);` registers **25** handles under one name — the `_Sn` suffix is a family of shader variants"; Post-Processing/CONTRACT-ppfx-effect-creation.md:115-117 "The two helpers that take a count (`0072DCF0`, 65 sites; `0072EB20`, 26) register *n* handles under one name"; Post-Processing/CONTRACT-ppfx-effect-creation.md:179 "`_Sn` for *n* sampler/shader variants with the count passed as the argument".
- Post-Processing/the-post-processing-effect-catalogue.md:806 "`0072EB20` … formats `"%s%d"` … `0072DCF0` (65 sites) does the same over a lazily filled static table of **suffix strings** - `_REINHARDRGB_RGB`, … so one base name yields a tone-map / colour-space family".
- Post-Processing/members/ppfx-handle-layout.tsv:113 labels the cited 25-count site `suffix-family`. How handle names are formed for 65 sites differs. No favoured side (lean: Post-Processing/the-post-processing-effect-catalogue.md:806 body read + HL label).

**PP.CV-6. Highest handle offset / object minimum: `+0x220DC` (r14) vs `+0x221D8` (this).** *(page-text only - needs local check)*
- Post-Processing/ppfx-function-identification.md:674-676 "The object is at least `0x220E0` bytes. The highest displacement `CreateEffect` touches is `+0x220DC`, and that is through `r14 = rcx + 8`, so the allocation is at least `0x220E4` from `rcx`."
- Post-Processing/the-post-processing-effect-catalogue.md:803 "The slots run from `this + 0xA0` to `this + 0x221D8` (`tech_HybridLogGamma`, the last), so the object is at least `0x221DC` bytes."; Post-Processing/the-post-processing-effect-catalogue.md:814 "allocates `0x22360` bytes".
- Also internal to Post-Processing/ppfx-function-identification.md:674-675: `0x220E0` vs `0x220E4`. Lean (HL): Post-Processing/members/ppfx-handle-layout.tsv:339 `0x221D8 r14 … tech_HybridLogGamma` (raw r14 disp 0x221D0 per HL header) exceeds 0x220DC, so PI's "highest displacement" counts only `lea`s. No dated correction.

**PP.CV-7. Receiver type of `0072A320`: `TEXSHADERSET` vs `CTextureUtil` (0x22360).** *(page-text only - needs local check)*
- Post-Processing/CONTRACT-ppfx-effect-creation.md:62-63 "The receiver is the `TEXSHADERSET` object in `rcx`"; Post-Processing/ppfx-function-identification.md:690-692 "the string in `CreateEffect`'s own body names the class".
- Post-Processing/CONTRACT-post-processing-subsystem.md:58 "| `CTextureUtil` | refcounted singleton at `02EA1590` / `02EA1598` | the catalogue's handle table"; Post-Processing/the-post-processing-effect-catalogue.md:814 "`0x22360` also closes the size left open under UQ-224 (the last handle slot is at `+0x221D8`)".
- Which class/size a port allocates for the handle table. No favoured side.

**PP.CV-8. Where the cutscene loader writes: record `01F812D0` vs the 0x4A8 block `[01F81300]`.** *(page-text only - needs local check)*
- Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:345 "`001C3D50` … reads the cut-scene banks … through the four-step fallback … into the record `01F812D0`".
- Post-Processing/CONTRACT-post-processing-subsystem.md:122-127 "`cfg` is filled from the `0x4A8`-byte render-parameter block that `00193D50` returns; `01F81300` caches the same pointer … The cutscene loader … makes this call (`001C42A6`–`001C42E4`)"; Render-Command-List/the-ordered-render-command-list.md:822-824 "Both write this record through small setters called on `[01F81300]`."
- No favoured side (may be two different destinations of one loader; pages do not reconcile).

**PP.CV-9. `00194250` callers: two vs five; map-loader route.** *(page-text only - needs local check)*
- Render-Command-List/the-ordered-render-command-list.md:794-796 "The two callers are `001C3D50`'s PresetDof arm (§7, `UQ-232`) and `001C5750`, the `sum_` bank's sidecar reader"; Render-Command-List/the-ordered-render-command-list.md:792-793 "Both of its callers read `+0x11C` back **before** the call".
- Post-Processing/CONTRACT-post-processing-subsystem.md:163 "the setter `00194250` has five direct call sites"; Post-Processing/CONTRACT-post-processing-subsystem.md:128-129 "The map loader calls the same two setters, with the enable fixed at 1."
- Affects which loaders feed DOF. No favoured side.

**PP.CV-10. `0078A120` role: `CreateEffectFromFile` wrapper vs `IGPUEffect::CreateEffect`.** *(page-text only - needs local check)*
- Post-Processing/the-post-processing-effect-catalogue.md:172 "`IGPUEffect::CreateEffectFromFile` wrapper; called once"; Post-Processing/CONTRACT-ppfx-effect-creation.md:57 "`IGPUEffect::CreateEffectFromFile` via `0078A120`".
- Post-Processing/ppfx-function-identification.md:578-579 "`0078A120  IGPUEffect::CreateEffect`" / "`0078A240  IGPUEffect::CreateEffectFromFile`" (Post-Processing/ppfx-function-identification.md:630 calls this "agree"). Naming only; no favoured side.

**PP.CV-11. Tuning names: reflection `PClassDataMember` strings vs JSON keys.** *(page-text only - needs local check)*
- Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:125-127 "are **the embedded strings that Phyre reflection's `PClassDataMember` holds**"; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:290-293 call chain "Phyre reflection static initializers -> PClassDataMember descriptors … -> these ~150 names"; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:412 "These are `PClassDataMember` names | … | 1".
- Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:345 (dated) "ANSWERED 2026-09-18 (FABLE) … None of the three is a reflection class; the names are JSON keys, which is why the reflection static-init region never spells them."
- Favoured: JSON-key reading, by the dated W-3 answer Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:345 (2026-09-18); Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:473 agrees ("not the reflection static-init region").

**PP.CV-12. `Inverted` passes: mirrored/reflection pass in the frame vs none draws.** *(page-text only - needs local check)*
- Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:120-121 "The `Inverted` variants are consistent with a mirrored pass — a reflection or an inverted-projection render."; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:296-298 call chain lists `RenderAtmosphere / RenderAtmosphereInverted`, `RenderCameraMotionBlur / ...Inverted` under "render frame".
- Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:354-357 (dated) "ANSWERED 2026-09-27 … no `Inverted` pass draws in this build … Only FXAA is built by game code".
- Favoured: Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:354 (2026-09-27).

**PP.CV-13. `mDofSpecialApertureFnumber` corpus: cutscene vs map.** *(page-text only - needs local check)*
- Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:278 "mDofSpecialApertureFnumber alternate aperture (cutscene?)".
- Post-Processing/CONTRACT-post-processing-subsystem.md:117-118 "`EnableDof` is in the cutscene files only, and map files carry `mDofSpecialApertureFnumber` instead."; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:563 shows it in `maps/alc0101.json`.
- Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:278 is a hedged guess; lean to Post-Processing/CONTRACT-post-processing-subsystem.md:117-118 + Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:563 data. No dated correction.

#### 3.1.12 [CM] Scripted camera, screen fade, screen effects, aspect fit, position-to-scalar, movie index

Short names in this part: **MR** = `Movie-Containers/README.md`; **MH** = `Movie-Containers/mh-movie-seek-index.md`; **PTS** = `Position-To-Scalar/how-a-position-becomes-a-single-number.md`; **SF** = `Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md`; **AF** = `Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md`; **CI** = `Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md`; **CR** = `Scripted-Camera/how-a-camera-reaches-the-renderer.md`; **P** = `Scripted-Camera/the-scripted-camera-player.md`; **RM** = `README.md`; **WT** = `../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`.


**CM.CV-1 Fade colour override: which byte is the flag and which four are the colour.** *(page-text only - needs local check)*
- "when the one-shot byte `022BDD58` is set, the four bytes `022BDD59`–`022BDD5C` are copied in" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:53-54)
- "`022BDD58`–`022BDD5B` are one four-byte parameter block armed by the request flag `022BDD5C`" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:225-226, dated ANSWERED 2026-09-26 but restating "the register on 2026-09-16"). The §2.1 text and `002EFE10(colour…) | arm the one-shot colour override at 022BDD58` (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:91) were not corrected. No favoured side (the 09-26 entry is in a UQ answer, not a correction of §2.1); lean UQ-235 (also ../_index/_inbox/SWE2-AUDIT-SPEC.md:3921 "raises `022BDD5C`=1").

**CM.CV-2 `022BDD57`: a descriptor nibble source vs the top byte of a double.** *(page-text only - needs local check)*
- "`+9` two nibbles from `022BDD57` and `022BDD5D`" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:51)
- "`022BDD57` is the top byte of a double" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:225); also the double at `022BDD50` (8 bytes, `50`-`57`) (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:60). No favoured side.

**CM.CV-3 Descriptor size handed to `00375900`: 0x28 vs 0x68.** *(page-text only - needs local check)*
- "`+0x08`–`+0x2F` | the 0x28-byte descriptor handed to `00375900`" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:51); "`+0x08  u8[0x28] descriptor       +0x28 u32 colour ..., +0x2C u32 = 2 * frames`" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:204, offsets that only fit if record-relative)
- "the 0x68-byte descriptor copied in (`003759C9`–`00375A01`)" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:66); "The pool record is the descriptor copied in whole at `+0x00`–`+0x67`" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:228); kind-4 descriptors use `+0x30` and `+0x50` (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:100-104). A 0x68 copy from record `+8` overruns into the next layers. No favoured side; lean 0x68 (../_index/candidates/rc151617-fable-0930/rc15_typing.md:55 names "a 0x68-byte request descriptor" passed as "`022BDD60 + i*0x30 + 8`").

**CM.CV-4 Fade record stride: 0x30 vs `ecx*24`.** *(page-text only - needs local check)*
- "Seven records of 48 bytes at `022BDD60` (`layer × 0x30`" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:43)
- "`002EF9F0` ... `dword[022BDD60 + ecx*24]`" (../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md:2411); "`byte [022BDD64 + ecx*24]`" (../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md:1590). No favoured side; lean 0x30 (7×0x30 ends at `022BDEB0`, where the words start, Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:194).

**CM.CV-5 `002EF910`: full per-tick poll vs a ~21-byte forwarder.** *(page-text only - needs local check)*
- "`002EF910`, called by `World_UpdateSimulationTick` (`00314020`), polls each of the seven records" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:76), "`002EF910` read whole" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:334), anchors to `002EF9BC` (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:77)
- "`002EF910` (~21 B) — thin forward under a six-register save." (../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md:1482). No favoured side.

**CM.CV-6 Movie fade flags polarity in the row prose.** *(page-text only - needs local check)*
- "`+7 flags (bit 0 white in, bit 1 white out)`" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:114, 207); pseudocode uses `flags & 1` for the fade-in and `(flags & 2) != 0` for the fade-out (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:116-118, Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:717); "Value 2 never occurs, so a white fade-*out* never ships without a white fade-*in*" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:384-385)
- "ids 17, 19, 21 fade to white on the way out (flags 1)" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:126-127). No favoured side by dated correction; lean bit 0 = in (code + Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:384).

**CM.CV-7 "No fade-out lead (`00 0F`)" names the wrong field.** *(page-text only - needs local check)*
- "Ids 4, 10, 42, 48 have no fade-out lead (`00 0F`)" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:126; repeated Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:362)
- field order "`+3 fadeOutLength   +4 fadeOutLead`" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:114); TSV row 4 = `04 1e 1e 00 0f` (+3 = 0, +4 = 0x0F): no fade-out at all, lead 15. No favoured side; lean field order + TSV.

**CM.CV-8 Skip/schedule words overwritten by the start they precede.** *(page-text only - needs local check)*
- start: "The globals `022BDD56 = 3`, `022BDEB0 = 0`, `022BDEB4 = 6` are reset at the end" of `002EFA70` (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:68-69)
- skip: "issues `002EFE40(6)`, `002EFE50(0xFF)` and `002EFA70(4, 0, 0, 0)` ... with kind 6 and a wait of `0xFF` recorded in the two words for whoever resumes the scene" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:133-136); schedule: "`002EFE40(5)` before each start marks the fade as the schedule's" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:128-129). If the reset is at the end of the start, the 0xFF / 5 cannot survive it. No favoured side.

**CM.CV-9 `0035CA70` state 8 polarity.** *(page-text only - needs local check)*
- "`002EFD20(0)` — layer-0 state; exits when it reads 1" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:161)
- "state 8 holds while layer 0's state byte reads 1, resuming at the saved state `+0xC1` once it clears" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:175-176). No favoured side (state 1 = running, 2 = finished, Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:49).

**CM.CV-10 Schedule "issued" bits: bits 3/4 vs "bit 8"/"bit 0x10".** *(page-text only - needs local check)*
- "`ctx+0xF0` bits 3 / 4 "fade-in / fade-out issued"" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:110-111)
- "with `+0xF0` bit 8 clear ... sets bit 8; the mirror block under bit `0x10`" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:717). No favoured side; lean masks 0x08/0x10 = bits 3/4 (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:717 mixes a mask written as "bit 8").

**CM.CV-11 Role of `002DEE50` / `002DEDE0` / `0215EF44`: fade layer vs music track.** *(page-text only - needs local check)*
- "`002DEE50` — ... the fade-flag publish guarded by the `0215EF44` counter ... The write is the layer's armed/visible flag" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:464-469); "`002DEDE0` (80 B) maintains the fade-layer singleton `dword[0215EF44]`" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:525-526)
- "`0215EF44 = 0xFFFFFFFF` (**current track handle**, `-1` = none)" (../_index/OPEN-QUESTIONS.md:1264); "the target-volume write `002DEE50`" (../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md:292). No favoured side.

**CM.CV-12 Viewport far-z constant: hex and decimal disagree.** *(page-text only - needs local check)*
- "`1024.0` and `16,777,215.0` (`0x44800000` / `0x4B7FFBFF`" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:230)
- `0x4B7FFBFF` decodes to 16,776,191.0 (python struct; `0x4B7FFFFF` is 16,777,215.0). Scripted-Camera/how-a-camera-reaches-the-renderer.md:486 gives only the hex. No favoured side; lean the hex (an image read).

**CM.CV-13 `02AED5F0`: "a constant" vs the camera eye.** *(page-text only - needs local check)*
- "`stash   = *(vec4 *)02AED5F0;            /* a constant, §4 */`" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:61); "`02AED5F0` | the stashed constant | 16 B | BSS; `[0, 0, 0, 2.0]` at runtime" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:172)
- "added to the **eye** at `02AED5F0` (the matrix's fourth row)" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:81-82); `0037D970` reads "six floats from `02AED5F0`–`02AED608`" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:168). No favoured side (both may hold; "constant" is a role claim the camera page contradicts).

**CM.CV-14 Scripted camera clock step: source and third factor.** *(page-text only - needs local check)*
- "`step = *(float*)0x02B4E4B0 * c->rate * 1.0f;`" (Scripted-Camera/the-scripted-camera-player.md:131); "`02B4E4B0` | frame step" (Scripted-Camera/the-scripted-camera-player.md:355, 559)
- "The tick delta is `float[0264E4B0] × rate × float[01DFE0BC]` (`003DA0F3`–`003DA100`)" (Scripted-Camera/the-scripted-camera-player.md:951). `01DFE0BC` is the frame-rate time base elsewhere (Effect-File-Formats/effect-element-type-dispatch.md:948). No favoured side.

**CM.CV-15 `00257AD0` role.** *(page-text only - needs local check)*
- "`00257AD0` | `Manager_FindNthKind3Actor` | 116 B | attachment actor lookup" (Scripted-Camera/the-scripted-camera-player.md:303); "the attachment evaluator" (Scripted-Camera/the-scripted-camera-player.md:986)
- "`00257AD0` is the same playhead evaluator `003DA050`'s track loop calls — the camera-shot and attachment paths share it" (Scripted-Camera/the-scripted-camera-player.md:990-991); §12's `003DA050` members do not include it (Scripted-Camera/the-scripted-camera-player.md:959-965). No favoured side.

**CM.CV-16 Player record `+0x169`-`+0x177`: unused vs cached angles.** *(page-text only - needs local check)*
- "`+0x169 u8[15]    unread169     not observed accessed`" (Scripted-Camera/the-scripted-camera-player.md:498)
- "cached angles | `[+0x16C]` yaw, `[+0x170]` pitch | `[+0x16C]` yaw only" (Scripted-Camera/the-scripted-camera-player.md:734, §7a dated 2026-09-15). No favoured side (§7a does not correct the table); lean §7a (body read).

**CM.CV-17 Shake offset setter `00382B70` destination addresses.** *(page-text only - needs local check)*
- "stored at `02AEDF70` (position offset) and `02AEDF80` (target offset), and two floats stored at `02AEDF98` and `02AEDF9C`" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:136-137)
- "`[rcx]`'s four floats and `[rdx]`'s four floats land contiguously at `02A19F64`, then `xmm2` and `xmm3` follow at `02A19F58`/`02A19F54`" (../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md:2570-2572). No favoured side; lean CR (the reset and `003820C0` use the `02AEDFxx` addresses, Scripted-Camera/how-a-camera-reaches-the-renderer.md:69-81).

**CM.CV-18 Display object `+0x38`.** *(page-text only - needs local check)*
- "`001DD8E0` sorts the table ... It also keeps the selected index's position current at object `+0x38` (`001DDA48`)" (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:127-129)
- "`+0x24` / `+0x28` | display-mode index / `DXGI_MODE_DESC` table"; "`+0x38` / `+0x40` | window-size index / table" (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:164, 166); "`+0x38` when the live mode `+0x18` is 0, otherwise `+0x24`" (../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md:500-501). No favoured side.

**CM.CV-19 Kind-28 path array: populated-slot count.** *(page-text only - needs local check)*
- "the 45 pairs occupy 92 of the first 94 slots" (Movie-Containers/mh-movie-seek-index.md:105); "read to the end it holds **45 `.md` + 45 `.mh`** ... in 92 populated slots" (Movie-Containers/mh-movie-seek-index.md:180-181)
- 45 + 45 = 90; ids 0-48 give indices 0-97 (98 slots) minus 8 NULLs (76-81, 92-93) = 90; the `.mh` pointers run to `01ECB7D8` = index 97 (Movie-Containers/mh-movie-seek-index.md:184). No favoured side; arithmetic lean 90.

**CM.CV-20 `0067A9B0`: teardown vs initialiser; "seek" role vs no reader.** *(page-text only - needs local check)*
- "`0067A9B0` (390 B) is the state-`1`→`3` channel teardown ... the seek/reset arm the movie container runs when the seek index is repositioned" (Movie-Containers/mh-movie-seek-index.md:241); "The `0067A9B0` teardown" (Movie-Containers/mh-movie-seek-index.md:216)
- "`0067A9B0(rcx + 0x678)` initializes the trailing sub-record" (Movie-Containers/mh-movie-seek-index.md:250-252); "this build fetches the `.mh` path only to throw it away — **the files are inert**" (Movie-Containers/mh-movie-seek-index.md:34); "no reader" (Movie-Containers/mh-movie-seek-index.md:99). No favoured side.

**CM.CV-21 Branch C integer divide bound.** *(page-text only - needs local check)*
- "`(W - H) / W` truncates to **0** for everything up to `W = 2H`" (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:82)
- `+0x0C = (float)( (W - H) / W ) * 0.5  ; also an INTEGER divide` (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:71): for 0 < H, W−H < W, so it is 0 for every positive H, not only up to W = 2H. Fields have no reader (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:116), so no runtime effect. No favoured side.

**CM.CV-22 Eight view-matrix elements: always vs only under the override.** *(page-text only - needs local check)*
- "copies the working camera's view matrix from `02AED580` to `02AEDE70` and adjusts eight of its elements" (Character-Render-Records/how-a-character-fades-the-ten-channels.md:337)
- "**only when the device override predicate of section 2 is true**, eight elements are replaced" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:114). No favoured side; CR read the body instruction by instruction 2026-09-19 (Scripted-Camera/how-a-camera-reaches-the-renderer.md:75), lean CR.

**CM.CV-23 Cut-in live state address.** *(page-text only - needs local check)*
- "live state block | `02092640` (0x24 B), target `02092638`" (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:66)
- "`0024CF50`, which raises bit 3 and fills the cut-in state from `02092638`" (../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md:692). No favoured side; lean CI.

(0 of 23 E1 items have a favoured side settled by a dated correction.)

### 3.2 Counts and census figures that disagree (no runtime behaviour changes)

#### 3.2.1 [AC] Authored commands, ramp channels and the coast-down latch

- **AC.CC-1 0x2C totals.** "`0x2C` | 417,549 / 325,965 / 445,335 / 387,789" (Authored-Commands/the-authored-presentation-command-handlers.md:235) vs "Of 387,757 `0x2C`" (:293-294). The corpora differ: 62,208 blocks (:224) vs 31,942 (:290-291).
- **AC.CC-2 0x09 totals.** "108,511 authored, one or two per block" (Authored-Commands/the-authored-presentation-command-handlers.md:302) vs "`0x09` | 4 | 78,455 | `00417F40`" (Model-And-Motion-Formats/fef-and-motion-entries.md:319).
- **AC.CC-3 Block counts.** Three corpus sizes: "62,208 blocks" (:224-225), "the 31,942 blocks of the animation containers" (:290-291), and "32,151 blocks, 0 grammar violations, 33 ids used" (:878).
- **AC.CC-4 "five setters" vs four.** The banner says "**Two of the five setters are not in the function census**" (CONTRACT-authored-command-ramp-channels.md:28). The README has "two of the four setters" (README.md:21), and §2 and :251-252 have four setters.
- **AC.CC-5 Function census.** README "Functions | 1,564" (README.md:8). Nothing else to compare on these pages; listed for completeness only.

#### 3.2.2 [RO] Render-record pool, character render object, transform publish and lighting

- **RO.CC-1** Character-Rendering/character-render-object.md:517-518: "The census is now 160 rows in 31 functions over 69 distinct offsets". Measured on `character-render-object-accesses.tsv`: 323 rows, 41 functions, 91 offsets.
- **RO.CC-2** CONTRACT-render-record-pool-lifecycle.md:34: "Five operations share the block"; CONTRACT-render-record-pool-lifecycle.md:9 lists six entries; CONTRACT-render-record-pool-lifecycle.md:782: "`EXP-109` executed all six lifecycle operations plus the constructor".
- **RO.CC-3** CONTRACT-render-record-pool-lifecycle.md:381: "Eleven other callees are oracles"; CONTRACT-render-record-pool-lifecycle.md:600 names thirteen addresses under "the eleven scripted callees"; CONTRACT-render-record-pool-lifecycle.md:611: "two of its thirteen named callees".
- **RO.CC-4** Negative-control size: CONTRACT-render-record-pool-lifecycle.md:167 and CONTRACT-render-record-pool-lifecycle.md:588 say "370 of … 492 lines"; CONTRACT-render-record-pool-lifecycle.md:386 says "460 of 583 lines"; CONTRACT-render-record-pool-lifecycle.md:384 says "581 compared lines".
- **RO.CC-5** Member set: Character-Rendering/character-render-object.md:842 "reached **45 functions**"; Character-Rendering/character-render-object.md:949 "the **48 bodies proved to take this object**".
- **RO.CC-6** CONTRACT-character-render-object.md:91-93: the eleven non-byte writes are "`word`, `dword` or `movss` stores". CONTRACT-character-render-object.md:243: "(2 byte, 4 word, 7 dword)".
- **RO.CC-7** UQ-203's census: Character-Rendering/character-render-object.md:842-843 "returned **the same 14 accesses, 1 write and 13 reads**" over 45 functions. CONTRACT-character-render-object.md:96-106 has 2 byte writes (incl. the ctor) and readers `001F89E0`/`001FAD50` inside the class (Character-Rendering/character-render-object.md:822 "`001FAD50` publishes nothing while `this + 0x4B4` is clear").

#### 3.2.3 [RA] The character render record array, render events, focus point and track pick

- **RA.CC-1. Array-base references.** Character-Render-Records/the-character-render-record-array.md:172 "**639 references image-wide**" vs Character-Render-Records/the-character-render-record-array.md:522 "**636 sites in 372 functions**" (and `Character-Rendering/character-render-object.md:546` "636 sites"); Character-Render-Records/the-character-render-record-array.md:524 calls it a predicate difference.
- **RA.CC-2. Proven field count.** Character-Render-Records/the-character-render-record-array.md:375 "This document proves 14 fields" vs Character-Render-Records/the-character-render-record-array.md:201-217 table of 16 rows.
- **RA.CC-3. Dirty mechanism counts** Character-Render-Records/the-character-render-record-array.md:726-729 (40+11+2+2 = 55) vs "56 test blocks" Character-Render-Records/the-character-render-record-array.md:799; the 56th is the pass-5 "none" row (TSV).
- **RA.CC-4. Census figures** 3,381/545/368 (Character-Render-Records/the-character-render-record-array.md:448) vs 3,097/525 under the array-only recipe (Character-Render-Records/the-character-render-record-array.md:444) vs 2,874/499/351 old; explained as regeneration.

#### 3.2.4 [RG] Rig controllers, fades, status looks, bone trails and the staged look

**RG.CC-1 Status-push arm count: 42 non-empty vs 44.**
- Character-Render-Records/how-a-status-shows-on-a-character.md:62-63 "the forty-two non-empty arms"; Character-Render-Records/the-rig-of-seventeen-controllers.md:194-205 lists 21 statuses x 2 = 42 addresses.
- Character-Render-Records/the-rig-of-seventeen-controllers.md:190 "lists the forty-four arms by their shape"; Character-Render-Records/the-rig-of-seventeen-controllers.md:222 "the other thirty-six arms"; Character-Render-Records/the-rig-of-seventeen-controllers.md:277 "thirty-six of the forty-four status arms"; `../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md:442` "44 slot arms in nine recurring shapes".

**RG.CC-2 Rig slot counts on LOOK.**
- Character-Render-Records/the-staged-look-command.md:213 "What thirteen of the rig's sixteen slots are (section 4a names the look controller, the eye object and the two bone-physics slots ...)" - four named of sixteen leaves twelve, not thirteen; and Character-Render-Records/the-rig-of-seventeen-controllers.md:25 / Character-Render-Records/the-rig-of-seventeen-controllers.md:66 give seventeen slots (16 populated, slot 4 empty).

**RG.CC-3 "names five more" lists six.**
- Character-Render-Records/the-staged-look-command.md:154-155 "names five more - `+0x0C` the Confuse motion, `+0x18` the Float bob, `+0x1C` the Immobilize motion, `+0x24` the lip flap, `+0x34` the nod, `+0x3C` the head shake".

**RG.CC-4 Fade writer census vs real writer set.**
- Character-Render-Records/how-a-character-fades-the-ten-channels.md:13 / :80 / :445 "22 sites, counts equal to a raw call sweep" vs Character-Render-Records/how-a-character-fades-the-ten-channels.md:114-118 "the census ... counted `call` and `jmp` sites only, so its 11 + 3 sites were never the whole story. The forwarder has six callers". TSV still shows 22 (A).

**RG.CC-5 Rig "names nine" vs table.**
- Character-Render-Records/the-rig-of-seventeen-controllers.md:21 "Nine of the seventeen controllers are named" / Character-Render-Records/the-rig-of-seventeen-controllers.md:33 "This page names nine" vs the Character-Render-Records/the-rig-of-seventeen-controllers.md:71-89 table, which names 15 of 17 (all except 4 and 8) after section 3a.

#### 3.2.5 [CL] Ordered render command list and graphics-thread handshake

**CL.CC-1. Number of enqueue functions.** Render-Command-List/the-ordered-render-command-list.md:64 "the shape of all 18 enqueue functions" and Render-Command-List/the-ordered-render-command-list.md:882 "all 18". Render-Command-List/the-ordered-render-command-list.md:611 "nineteen builders" and Render-Command-List/the-ordered-render-command-list.md:892 "all **19** enqueue builders". Render-Command-List/the-ordered-render-command-list.md:621 "**all 20** enqueue call sites". Render-Command-List/the-ordered-render-command-list.md:975 "**36 functions**". Render-Command-List/the-ordered-render-command-list.md:646 "**40 bodies**". CONTRACT-render-command-list-and-graphics-handshake.md:60 "~40 enqueue functions". CONTRACT-render-command-list-and-graphics-handshake.md:353 "~39 siblings". CONTRACT-render-command-list-and-graphics-handshake.md:250 "enqueue (x40)". The dated Render-Command-List/the-ordered-render-command-list.md:967 says "**36, not 18**".

**CL.CC-2. Number of classes.** Render-Command-List/the-ordered-render-command-list.md:49 "thirty-six kinds of job". Render-Command-List/the-ordered-render-command-list.md:279 "**43 concrete classes**". Render-Command-List/the-ordered-render-command-list.md:711 "the RTTI's **42** direct `OrderedObject` subclasses". CONTRACT-render-command-list-and-graphics-handshake.md:95 "42 subclass vtables exist". CONTRACT-render-command-list-and-graphics-handshake.md:493 "the 43-class slot matrix". The TSV has 42 concrete classes plus the base.

**CL.CC-3. Constructor census.** Render-Command-List/the-ordered-render-command-list.md:110 "called by 42 sites". CONTRACT-render-command-list-and-graphics-handshake.md:462 "all 42 subclass ctor bodies … all 41 construction-site callers".

**CL.CC-4. Read references to `02EBA3F8`.** Graphics-Thread-Handshake/the-shared-command-state-word.md:57 and Graphics-Thread-Handshake/the-shared-command-state-word.md:429: "38 read-form". Graphics-Thread-Handshake/the-shared-command-state-word.md:221: "40 loads".

**CL.CC-5. References to `02EAF6D8`.** Graphics-Thread-Handshake/the-shared-command-state-word.md:302: "24 listed references, all reads". Graphics-Thread-Handshake/the-shared-command-state-word.md:419: "censused all 17 sites". Graphics-Thread-Handshake/the-shared-command-state-word.md:494: "Seventeen … exactly the number of references that word has in the image".

**CL.CC-6. Post-process census.** Render-Command-List/the-ordered-render-command-list.md:798: "776 sites". The TSV has 777 rows, after Render-Command-List/the-ordered-render-command-list.md:1257-1258 "It is added there now".

**CL.CC-7. Thread counts.** Graphics-Thread-Handshake/the-shared-command-state-word.md:336 "all nine thread procedures". Graphics-Thread-Handshake/the-shared-command-state-word.md:364 "none of the nine". Graphics-Thread-Handshake/the-shared-command-state-word.md:366 "**eight distinct procedures, not nine**". Graphics-Thread-Handshake/the-shared-command-state-word.md:372 "thirteen threads rather than nine". With eight import threads and four Tk threads the total is 12.

**CL.CC-8. Enqueue body sizes.** Render-Command-List/the-ordered-render-command-list.md:61 "the same 140-to-150-byte template". Render-Command-List/the-ordered-render-command-list.md:968 "**139–253 bytes**; 29 of the 36".

**CL.CC-9. Distinct slot-2 values.** Render-Command-List/the-ordered-render-command-list.md:146 "three distinct values observed". Render-Command-List/the-ordered-render-command-list.md:995 "only five distinct implementations". Render-Command-List/the-ordered-render-command-list.md:301-309 lists 9 implementations family-wide.

#### 3.2.6 [GP] Gi render commands and the legacy PS2 GS/VIF layer

**GP.CC-1 Factories at `00862E50`-`00865320`: thirteen vs eleven.** Gi-Render-Commands/gi-render-command-family.md:957-958 "Thirteen factories sit together at `00862E50`–`00865320`." vs the table Gi-Render-Commands/gi-render-command-family.md:962-967, which lists 11 factories in that range (`00862E50`, `00862FD0`, `00863060`, `00863B40`, `008642A0`, `008647C0`, `00864D10`, `00864E00`, `00865130`, `008652B0`, `00865320`). Also Legacy-PS2-GS/the-vif1-vu1-layer.md:235-236 "the eight `Gi*` arena factories at `0086xxxx`".

**GP.CC-2 Untouched device slots.** Gi-Render-Commands/gi-render-command-family.md:1337-1338 "The highest the `Gi*` family calls is slot 39 (`+0x138`), so nine slots are never touched by this family." vs arithmetic: 45 slots (Gi-Render-Commands/gi-render-command-family.md:1334) minus 20 used (Gi-Render-Commands/gi-render-command-family.md:69) = 25; slots above 39 = 5.

**GP.CC-3 Arena size range.** Gi-Render-Commands/gi-render-command-family.md:334-335 "the sizes passed to it span 16 … 360 bytes" vs Gi-Render-Commands/gi-render-command-family.md:971 `GiVmax` `0x640` (1,600) and Legacy-PS2-GS/the-vif1-vu1-layer.md:110 "the `0x640`-byte command".

**GP.CC-4 Registrar program count.** Legacy-PS2-GS/the-vif1-vu1-layer.md:408-411: 29 registrar programs, 17 shared, plus 10 more → 57; vs Legacy-PS2-GS/the-vif1-vu1-layer.md:799 "the four registrars register 44, and the templates install 35" (implies 22 shared). Not reconciled on the page.

**GP.CC-5 Hub-called builders: 74 vs 76.** Legacy-PS2-GS/the-vif1-vu1-layer.md:526-527 "this applies the same decode to all 74 hub-called builders" (and Legacy-PS2-GS/the-vif1-vu1-layer.md:545 "of the 74") vs Legacy-PS2-GS/the-vif1-vu1-layer.md:441 "The union is 76 distinct builders / 77 distinct objects" (TSV: 76 distinct builders).

**GP.CC-6 Tag-carrying builders exceed the population.** Legacy-PS2-GS/the-vif1-vu1-layer.md:545 "(corrected 2026-09-27 ...: sixteen more carry one ... so at least 61" and Legacy-PS2-GS/the-vif1-vu1-layer.md:547-548 "21 of them author no `UNPACK` command at all — a template with no payload has nowhere to keep a tag": 61 + 21 = 82 > 76 builders (Legacy-PS2-GS/the-vif1-vu1-layer.md:441). `vif1-gif-tags.tsv` still has 75 tags / 45 builders (A).

**GP.CC-7 Template-path vs registrar-path region rows after UQ-213.** Legacy-PS2-GS/the-vif1-vu1-layer.md:776 "microprogram (registrar-path ...) | 28" vs the TSV, which adds 10 `VU1-microprogram(VU-state-toucher)` rows (UQ-213 correction).

**GP.CC-8 XGKICK-shaped leaves: 8 vs 9.** Legacy-PS2-GS/the-vif1-vu1-layer.md:669 "eight of them share `004EF860`'s exact shape" vs Legacy-PS2-GS/the-vif1-vu1-layer.md:782 "XGKICK-shaped leaf (form-matches `004EF860`) | 9 + the `004EF860` reference" (TSV 9) and Legacy-PS2-GS/the-vif1-vu1-layer.md:20 "there are 9".

#### 3.2.7 [EF] Effect containers, element dispatch and the per-frame element update

**EF.CC-1 Step case/handler counts.** "**47 types have a case.**" (Effect-File-Formats/effect-element-type-dispatch.md:66); "every one of the 47 step case handlers calls it" (Effect-File-Formats/effect-element-type-dispatch.md:837-838) vs "step 002F3BC0 | element `+0` | 41 | 41" (Effect-File-Formats/effect-element-type-dispatch.md:168) and "`002F2D60` — 1,111 B, 41 frontier callers at census" (Effect-File-Formats/effect-element-type-dispatch.md:1045). TSV: 41 distinct.

**EF.CC-2 Sub-update leaf arms.** "`0043EAB0` (136 B) … arms `jmp 00522290`/…/`00528050`" (10 listed, Effect-File-Formats/effect-element-type-dispatch.md:1196) vs "sub-update 0043EAB0 | … | 18 | 18" (Effect-File-Formats/effect-element-type-dispatch.md:174); TSV 18.

**EF.CC-3 Frontier total.** Per-row frontier column sums to 246 (Effect-File-Formats/effect-element-type-dispatch.md:168-177) vs "**248 distinct handler functions, 244 of them on the frontier**" (Effect-File-Formats/effect-element-type-dispatch.md:179).

**EF.CC-4 Entry-only queue size.** "The other 27 report **"no DOCUMENTED citer found"**" (Effect-File-Formats/effect-element-type-dispatch.md:690) vs "the queue is now **40** bodies and **25** of them report no citer" (Effect-File-Formats/effect-element-type-dispatch.md:675-676); "39 large bodies" (Effect-File-Formats/effect-element-type-dispatch.md:655).

**EF.CC-5 Queue table rows.** "Nine are named by a page in this folder or its neighbours" (Effect-File-Formats/effect-element-type-dispatch.md:658) vs twelve rows in the table that follows (Effect-File-Formats/effect-element-type-dispatch.md:662-673).

**EF.CC-6 Tail counts.** "## 4. The other seven tails" (Effect-File-Formats/an-effect-element-frame-by-frame.md:163) / method "the ten per-type tails" (Effect-File-Formats/an-effect-element-frame-by-frame.md:9) vs "this section has six tails, not seven, and the method's "ten per-type tails" are nine tails plus `0044B960`" (Effect-File-Formats/an-effect-element-frame-by-frame.md:165-166).

#### 3.2.8 [ET] Effect element types, kind-0x54 meshes, menu effect registry and VFX layers

- **ET.CC-1 `+0x28` entry count.** Effect-File-Formats/effect-mesh-records-kind-54.md:120 "`+0x28` 4-byte | 4 B × c18 | 147,220" vs Effect-File-Formats/effect-mesh-records-kind-54.md:121 "`+0x2C` 8-byte | 8 B × c1A | 155,916 pairs" with Effect-File-Formats/effect-mesh-records-kind-54.md:102 "`c1A == c18` | all 2,252". TSV sum c18 = 155,916 → lean 155,916.
- **ET.CC-2 Id count.** Effect-File-Formats/effect-mesh-records-kind-54.md:139 "`c1C` is 0 in 1,813 records, 1 in 425, 2 in 14" (= 453 id bytes, TSV) vs Effect-File-Formats/effect-mesh-records-kind-54.md:140-141 "439 / 439 all-match" (may count nonzero bytes only).
- **ET.CC-3 Type-0x05 elements.** Effect-File-Formats/effect-mesh-records-kind-54.md:156 "type-`0x05` elements | 5,164" vs Effect-File-Formats/the-element-types-00-0a.md:378 "`0x05` | … | 5,204 / 323" (type_census.tsv 5,204; efx/efb only 5,168). Explained by Effect-File-Formats/effect-mesh-records-kind-54.md:45-49 caveat; still three figures.
- **ET.CC-4 `0039B620` callers.** Effect-File-Formats/the-menu-effect-registry.md:117 "`0039B620`, with fifty-one callers" vs 00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md:681 "`0039B620` — 13 B, 47 frontier callers".
- **ET.CC-5 0x65/0x66 "second-largest".** Effect-File-Formats/the-element-types-60-74.md:80 "records end `+0x880`/`+0x8F0`, the second-largest of the group" — no larger record named on the page (0x68 `+0x7C0`, :103; runtime to `+0x8BC`, :208).
- **ET.CC-6 Tail count.** Effect-File-Formats/the-element-types-00-0a.md:223 "All ten step/update tails" and Effect-File-Formats/the-element-types-00-0a.md:347 "all ten read" vs Effect-File-Formats/an-effect-element-frame-by-frame.md:166 "the method's "ten per-type tails" are nine tails plus `0044B960`" (corrected 2026-09-29, CON-179).

#### 3.2.9 [MF] Model formats: add-motion tables, ADM, FCP, FDM/FOR

**MF.CC-1. Which 21 `.cm` files lack `@FDM`.** Model-And-Motion-Formats/fdm-and-for-entries.md:36 says "`@FDM` `1,045/1,066` (the 21 missing are mostly `treasure`/`bg_obj` files)". Model-And-Motion-Formats/fcp-character-parameter-block.md:276 says "21 weapons carry only `@FCP @FTR @FOR`" (the tag-set sums 855+144+45+21+1 = 1,066 give 1,045 with `@FDM`).

**MF.CC-2. How many `.cm` carry motion entries.** Model-And-Motion-Formats/fdm-and-for-entries.md:322-323 says "`@FMC`/`@FMN`/`@FMW` (`209`, `111`, `111` files)". Model-And-Motion-Formats/fcp-character-parameter-block.md:275 says "the same plus motion entries `@FMC` / `@FMN` / `@FMW` (29 weapons and 16 treasures)". The populations may differ (FDM's sentence does not say `.cm` only).

**MF.CC-3. How many tags the binder `00504F00` loads.** Model-And-Motion-Formats/fcp-character-parameter-block.md:364 says "`00504F00` (loads all six)". Model-And-Motion-Formats/fdm-and-for-entries.md:42 says "resolves all seven `.cm` entries by tag", and Model-And-Motion-Formats/fdm-and-for-entries.md:360 says "the seven tags in order into `+0x208`..`+0x220`".

**MF.CC-4. The section-1 (1.0, 1.0) pair count.** Model-And-Motion-Formats/fcp-character-parameter-block.md:237 says "(0.5, 0.5) in 288 files and (1.0, 1.0) in 229 for the alternate". Model-And-Motion-Formats/fcp-character-parameter-block.md:290 says "`(0.5, 0.5)` in 288 files, `(1.0, 1.0)` in 186, `(0.6, 0.6)` in 125 — and so is the alternate pair at 79 / 80". It is ambiguous whether 229 refers to slots 79/80.

**MF.CC-5. Instruction count of `004201F0`.** Model-And-Motion-Formats/fdm-and-for-entries.md:327 says "fully disassembled (144 insns)". Model-And-Motion-Formats/fdm-and-for-entries.md:359 says "`004201F0` decodes to 143 instructions in its 648 bytes". The page records this itself, with no correction row.

#### 3.2.10 [MM] Motion formats: FEF/motion entries, FRP, FTE/FCT, FTR, oscillator, pose sequencer

**MM.CC-1 fef census check count.** "members/fef_motion_entry_census.py, 8 checks, FAILS 0" (Model-And-Motion-Formats/fef-and-motion-entries.md:16) vs "12 checks, FAILS 0 on the shipping archive" (:837).

**MM.CC-2 @FMN entry total.** ".cm, 111; .ca, 18,303" (Model-And-Motion-Formats/fef-and-motion-entries.md:463) = 18,414 vs "All 20,207 shipped @FMN entries" (:525) and "0xF0 + nrec*22 (10,628 entries) or +2 with a pad u16 (9,579)" (:536-537) = 20,207.

**MM.CC-3 @FCT header record count.** "invariant, 1,951/1,951" and "Census over 1,044 files / 1,951 header records" (Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:98, :111) vs "1,972/1,972" (:101, :102, :104) and "measured 1,970 of 1,972" (:150); the clutBytes histogram "0x400 (1618), 0x200 (318), 0x40 (35)" (:113) sums to 1,971.

**MM.CC-4 +0xBA setter call sites.** "called from the status-look code at 00428D3C, plus 00428CD0 twice and 0042E520" (Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:141-142) vs "the setter has three call sites … and the page counts one of them twice" (:309) and "has three call sites" (:246).

**MM.CC-5 Oscillator member count.** "members/model-oscillator-subsystem.tsv lists all 36 members" (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:185; Model-And-Motion-Formats/README.md:40 "(36 members)") vs 39 data rows in the TSV (A, tsv check).

**MM.CC-6 Command counts, container vs all blocks.** fef table "0x16 | 6 | 329" and "0x13 | 6 | 5,805" (Model-And-Motion-Formats/fef-and-motion-entries.md:330, :328) vs "all 373 shipped 0x16 commands carry 0xFFFF" (Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:268) and Authored-Commands/the-authored-presentation-command-handlers.md:620/:738 ("0x13 17,416 … 0x16 373"; "373 — 329 in containers, 44 in event blocks").

**MM.CC-7 @FMC population.** "a census of all 62,208" (Model-And-Motion-Formats/frp-object-container.md:366-367) vs "32,151 @FMC entries" (Model-And-Motion-Formats/fef-and-motion-entries.md:259) (Authored-Commands/the-authored-presentation-command-handlers.md:224 counts 62,208 blocks including event blocks).

**MM.CC-8 @FMW channel-bearing pairs.** "frameCount equals the paired @FMN's word+0x50 duration in all 15,037 channel-bearing .ca pairs (the 779 exceptions are empty @FMW tables …)" (Model-And-Motion-Formats/fef-and-motion-entries.md:585-587) = 15,816, vs ".ca, 18,303" @FMW (:558); the remainder is not accounted for.

#### 3.2.11 [PP] Post-processing and visual tuning parameters

**PP.CC-1. Call sites/targets enumerated vs 358/22.** Post-Processing/the-post-processing-effect-catalogue.md:121 "358 direct calls to 22 real targets"; Post-Processing/the-post-processing-effect-catalogue.md:123-137 itemises 12 helpers (332) + logger 10 + sprintf 8 + four singles = 18 targets / 354 sites; Post-Processing/CONTRACT-ppfx-effect-creation.md:82-85 + Post-Processing/CONTRACT-ppfx-effect-creation.md:157-162 itemise 14 + `0078A120`, `0078A530`, `0072E940`, memset, `00715360`, cookie = 20 targets / ~356. Post-Processing/the-post-processing-effect-catalogue.md:136-137 names "free"; Post-Processing/CONTRACT-ppfx-effect-creation.md:162 names "a string release (00715360)".

**PP.CC-2. Strings in extent: 369 vs 374/364.** Post-Processing/the-post-processing-effect-catalogue.md:836 "Widening to include `\t\n\r` gives 369."; Post-Processing/CONTRACT-ppfx-effect-creation.md:110-111 "379 targets, 374 of which decode as printable `.rdata` strings and 364 of which are distinct". Different instruments.

**PP.CC-3. PI class census vs its own list.** Post-Processing/ppfx-function-identification.md:457-458 "`CPostEffect` 59, … and sixteen more classes with 1–3 each"; counted Post-Processing/ppfx-function-identification.md:461-597: CPostEffect 58, 17 further classes (23 total).

**PP.CC-4. PPFX API/function totals.** Post-Processing/CONTRACT-post-processing-subsystem.md:237 "the 62 API methods named from its own strings"; Post-Processing/the-post-processing-effect-catalogue.md:991 "names 62 API functions"; Post-Processing/ppfx-function-identification.md:457 "CPostEffect 59" (list shows 58); Post-Processing/ppfx-function-identification.md:30 "135 more functions"; Post-Processing/ppfx-function-identification.md:454-455 "137 of the 150"; Post-Processing/ppfx-function-identification.md:222 "1,766 entries, 1,660 declared"; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:310 "`ThirdParty.Rendering.PPFX` (345 functions)"; README.md:107 "147 post-processing functions named".

**PP.CC-5. Depth-of-field family size.** Post-Processing/the-post-processing-effect-catalogue.md:51 "Depth of field is the largest family by far — 63 techniques"; the "Depth (63)" block (Post-Processing/the-post-processing-effect-catalogue.md:201-266) includes 2 `DepthEncode` + 8 `DepthFromDofFactor`; `tech_DepthOfField_*` = 53 (grep -c).

**PP.CC-6. RR group counts vs the names listed.** Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:129 "Shadow — 28 parameters" lists 32 names (Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:132-139); Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:160 "Ambient occlusion — 12 parameters" lists 14 (Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:163-166; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:265 "2 x 2 x 3 + 2"); Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:185 "Water — 16 parameters" lists 18 (Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:188-193).

**PP.CC-7. `mCascadeNumber` section count.** Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:351 / Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:734 "284 sections"; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:726-727 table 282 (cutscene `Common`) + 1 (maps) = 283; Visual-Tuning-Parameters/README.md:51 "`mCascadeNumber` | 1".

**PP.CC-8. Low-count key file counts.** Visual-Tuning-Parameters/README.md:48-51 `mMapAmbientColorA` 18, `EnableAutoExposure` 3, `mWaterParallax` 2; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:689-690 `mMapAmbientColorA` (19), `EnableAutoExposure` (4), `mWaterParallax` (3) (RR corpus is 797 files incl. cutscenes; VR is maps). Also Visual-Tuning-Parameters/README.md:60-63 R/G/B 70/52/46 files.

**PP.CC-9. Editor-marked keys: 27 vs 34.** Visual-Tuning-Parameters/README.md:28 "27 of the 38 carry authoring-tool markers"; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:670-672 "27 × `*CheckBoxCheckState`" plus "7 × `*Lock`" editor flags (`EnableDofLock` …). Visual-Tuning-Parameters/README.md:35 says "no tool-marked key appears in the binary".

**PP.CC-10. "Nine of the ten are a superseded generation".** Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:675 heading vs body Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:677-691 showing 3 renamed SAO names and 6 others "in the same low-count band" (the tenth unnamed).

**PP.CC-11. 797-file corpus vs its parts.** Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:657-658 corpus = init + maps + cutscenes + fontcluts, "797 files parsed"; 1 + 459 + 337 = 797 leaves 0 for `fontcluts` (Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:380 "one of the 28 `fontclut_%d` entries"). Lean: arithmetic.

**PP.CC-12. `mMotionBlurEnabled` file count vs scene-parameter files.** Post-Processing/CONTRACT-post-processing-subsystem.md:252-253 "the key is 0 in 283 cutscene files and 1 in one"; Post-Processing/CONTRACT-post-processing-subsystem.md:114-115 "283 of the 337 in `jsondata/cutscenes/` are scene-parameter sets"; Visual-Tuning-Parameters/README.md:12 says the 337 cutscene files are "keyed `Cut 1`…`Cut N`".

**PP.CC-13. Shader asset count.** Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:33 "15 shader files"; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:57 "18 files"; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:89 "The count is 18"; Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:408 "The 15 asset paths"; README.md:129 "the 15 `.phyre` shader assets" (15 includes `tuffysdf.fgen`, a font).

#### 3.2.12 [CM] Scripted camera, screen fade, screen effects, aspect fit, position-to-scalar, movie index

- **CM.CC-1 Callers below `0045E930`.** "**57 of the 75** sit below `0045E930`" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:327) vs TSV `fade-node-consumers.tsv`: 46 distinct callers below `0045E930`.
- **CM.CC-2 75 call sites vs 76 sites.** "the 75 call sites" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:211), "Seventy-five places" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:34) vs "**76 sites in 75 functions**" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:380; Position-To-Scalar/how-a-position-becomes-a-single-number.md:321).
- **CM.CC-3 "four" callers listing six.** "four Presentation / UI callers (`00228C70`, `0027EFA0`, `00280140`, `003939B0`, `00394130`, `003EFAA0`)" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:100-101).
- **CM.CC-4 Shake census.** "328 starts, ... 315 clears, 178 stops, 13 syncs, 6 changes" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:307; also Scripted-Camera/how-a-camera-reaches-the-renderer.md:281) sum to 840 vs "842 calls" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:306); TSV has `camerashakestop` 2 extra (180 stops).
- **CM.CC-5 us script corpus size.** "counted in the 1,114 decompiled us scripts" (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:13) vs "all 1,115 `us` `.ebp` containers" (Scripted-Camera/the-scripted-camera-player.md:801).
- **CM.CC-6 "Three" invokes listing two.** "then three one-argument invokes - `0017D960(1)`, `002E1CA0(1)` ... - and the tail `00229AE0(1)`" (Movie-Containers/mh-movie-seek-index.md:253-258).

### 3.3 Stale "not read / open" claims, struck-but-repeated text, and banner disagreements

These do not change a value. A re-implementer would only be misled about what is known. Each part lists (a) front matter vs body banner vs `README.md` tag, (b) stale "not read / open" text that another page or a later dated section answers, and (c) corrected claims still repeated unstruck.

#### 3.3.1 [AC] Authored commands, ramp channels and the coast-down latch

(a) Status vs banner vs README tag:
- **AC.CS-1 Handler page: README PARTIAL vs front matter DOCUMENTED.** README.md:14 "**PARTIAL, tier 1.**" vs Authored-Commands/the-authored-presentation-command-handlers.md:4 "DOCUMENTED — every register row is closed (owner re-status 2026-10-01 …". Also last_reviewed 2026-09-17 (:12).
- **AC.CS-2 Ramp contract: README "not differentially tested" vs readiness DIFFERENTIAL TESTED.** README.md:19 "**SPECIFIED, tier 1, not differentially tested.**" vs CONTRACT-authored-command-ramp-channels.md:6 "readiness: DIFFERENTIAL TESTED # diff_ramp_channels.py, 483 commands / 129 compared lines / 0 mismatches".
- **AC.CS-3 Coast-down contract not in the README; readiness vs mutation verdict.** Not in README.md at all. CONTRACT-coast-down-latch.md:6 "readiness: DIFFERENTIAL TESTED" sits beside "Verdict `FAIL`." (:401); the page says the one real gap was "closed" (:404) but gives no re-run verdict.

(b) Stale "unread / open" claims answered elsewhere:
- **AC.CS-4 "What consumes the weight is unread".** "What consumes the weight is unread, as UG-1 is." (CONTRACT-authored-command-ramp-channels.md:201-202) vs "`+0x43` | `+0x98` | eased through LUT row 5 … **this is the consumer of UG-3's cross-fade weight**" (:152, consumer read 2026-09-20 :143).
- **AC.CS-5 "The record's other 0x60 bytes are unread".** (CONTRACT-authored-command-ramp-channels.md:136) vs "**Mostly mapped 2026-09-20:**" (:451-476).
- **AC.CS-6 "the shadow draw … is unread on both pages".** (CONTRACT-authored-command-ramp-channels.md:142) vs "*Consumer read 2026-09-20 (SWE2-CONTRACT):* the draw **is** read" (:143).
- **AC.CS-7 "Not established: what `00358290`, `00181DD0` and `002E05C0` test".** (CONTRACT-authored-command-ramp-channels.md:238) vs "**All three read 2026-09-20:**" (:419-448).
- **AC.CS-8 "Still not executed. The consumers … are not in this harness".** (CONTRACT-authored-command-ramp-channels.md:390-391) vs "`EXP-108` ran the 160-slot draw pass `003B6020` (677 B) and the `0xA0` record builder `003B62D0`" (:571-572). The qualifier is per-harness, but no cross-reference is given.
- **AC.CS-9 "`0020E600` and `0051B9E0` are supplied … those two functions are not" [established].** (CONTRACT-coast-down-latch.md:381-382), and "What is still owed … 3. **What `0020E600` and `0051B9E0` are**" (:393), vs "**`0020E600` and `0051B9E0` are both read now** (2026-09-13" (:183).
- **AC.CS-10 Record-array page arming list "three of the five".** "The document lists the first three" (CONTRACT-coast-down-latch.md:244) and "whose arming list is three of the five" (:548-549) vs the record-array page listing all five: "object flag `0x08000000` set, `+0x06` equal to `-1`, subtype exactly `0x10`, the incoming speed exactly `0.0`, and a per-record counter at `+0x457`" (Character-Render-Records/the-character-render-record-array.md:131-134; also :257-261).

(c) Corrected claims still repeated unstruck:
- **AC.CS-11 "deferred" for `00426870`.** "`00426870` — the deferred-work poster —" (Authored-Commands/the-authored-presentation-command-handlers.md:128). Also :124 "posts `00520E90` through the deferred-work poster `00426870`", :125 "deferred worker", and :141 "the deferred resource-bind pair". The README repeats it: "plus the deferred-work pair (`00520100` → `00520E90`)" (README.md:16-17) and "the posted deferred worker" (README.md:138). The correction is "**`00426870` (90 B) defers nothing**" (:507-508). Model-And-Motion-Formats/fef-and-motion-entries.md:348 also has "deferred event".
- **AC.CS-12 Stale per-row counts.** Row 0x13 "5,805 authored" (:90) and row 0x16 "329 authored" (:93) vs "The counts that moved are `0x16` (329 → 373) and `0x13` (5,805 → 17,416)" (:624-625). The census headings at :591, :683 and :733 still say "every `.ca` container".
- **AC.CS-13 0x34 writes on the record vs on the shadow object.** Row 0x34 "`+0x1C`–`+0x28` state" (:109) and §5 "through `00520800` — the `+0x1C`–`+0x28` block" (:135-136) put the writes on the render record. vs "a **one-hot** sub-dispatch of eight arms over the record's shadow object" (:320-321), with the GI-15 fields spanning `+0x1C`…`+0x58` on the V2 slot (:1029-1046).
- **AC.CS-14 Coast-down §6 vs §7a on whether the `0020E600` call is part of the transition.** "Calls `0020E600` after the latch logic … — the presentation entry path, outside this transition." (CONTRACT-coast-down-latch.md:123-124) vs "## 7a. The fourth stage — ADDED 2026-09-11 … **It runs on every path except servicing**" (:146-148).

#### 3.3.2 [RO] Render-record pool, character render object, transform publish and lighting

Short names in this part: **POOL** = `CONTRACT-render-record-pool-lifecycle.md`; **CRO-C** = `CONTRACT-character-render-object.md`; **PUB** = `CONTRACT-character-transform-publish.md`; **CRO** = `Character-Rendering/character-render-object.md`; **LIT** = `Character-Rendering/how-a-character-is-lit.md`.


(a) Banners
- **RO.CS-1** CRO front matter `status: AUDITED` (Character-Rendering/character-render-object.md:4). The body says "Status unchanged at `DOCUMENTED`." (Character-Rendering/character-render-object.md:572). The README tags it DOCUMENTED, with "one writer at the end of setup and twelve readers at method entry" (README.md:99-101). That README text contradicts CONTRACT-character-render-object.md:85-88 (two byte writers) and CONTRACT-character-render-object.md:102 (eleven vtable gates).
- **RO.CS-2** LIT front matter `audit: passes: 1 … falsification` (Character-Rendering/how-a-character-is-lit.md:15-18), but the note says "pending first review" (Character-Rendering/how-a-character-is-lit.md:22). The same note says "The five per-kind evaluators, the list builder and the caller of the gather were not read" (Character-Rendering/how-a-character-is-lit.md:20-21), against §5a ("Two of the five kinds, read", Character-Rendering/how-a-character-is-lit.md:140; kinds 3-5, Character-Rendering/how-a-character-is-lit.md:162), the create routine "now read whole" (Character-Rendering/how-a-character-is-lit.md:179) and the caller head read (Character-Rendering/how-a-character-is-lit.md:211-212).
- **RO.CS-3** The three contracts are not listed in README.md (only the ramp-channel contract is, README.md:18).

(b) Stale open claims answered elsewhere
- **RO.CS-4** CONTRACT-character-render-object.md:190: Unresolved "What the bank-selecting byte at `+0x1C` … is, and who writes it". Answered at CONTRACT-character-transform-publish.md:274-283 ("a **camera-source flag** … `00185A1D` … `001860E6`") and at Character-Rendering/character-render-object.md:782-798. Note that these two answers disagree with each other (RO.CV-5).
- **RO.CS-5** CONTRACT-character-transform-publish.md:343-347: "`001FB120` has no direct call site, so it is a vtable or callback entry" / caller unknown. Character-Rendering/character-render-object.md:1019 (`001FA748` `[rax+0x68]` slot 13) and Character-Rendering/character-render-object.md:344 show slot 16 as the caller.
- **RO.CS-6** CONTRACT-character-transform-publish.md:136-139 (§9): "the publish must run before whatever flips the parity byte … the parity flip happens between publishes". CONTRACT-character-transform-publish.md:416-417 §16: "`TIMING` — the one this contract cannot specify until §14.1 is answered". Both are superseded by CONTRACT-character-transform-publish.md:274-288 ("NOTHING FLIPS IT PER FRAME").
- **RO.CS-7** Character-Rendering/character-render-object.md:345-346: "the pool's per-frame update calls it once a released object's three-frame countdown ends". The same answer block at Character-Rendering/character-render-object.md:419 says "the pooled element's `3` (a likely expiry count) is not followed here".
- **RO.CS-8** Character-Rendering/character-render-object.md:294-295 (§5): "**The ordering within a frame is not established** … **BB-3**" — answered at Character-Rendering/character-render-object.md:331-346. Character-Rendering/character-render-object.md:538 (§8b): "count | not established (**BB-4**)" — answered at Character-Rendering/character-render-object.md:388-415.
- **RO.CS-9** Character-Rendering/character-render-object.md:505-509 (§8): "No rendering API call has been traced out of these methods … **BB-1 tracks exactly this gap**". Character-Rendering/character-render-object.md:568-570 and Character-Rendering/character-render-object.md:635-639 say the same. BB-1 is answered at Character-Rendering/character-render-object.md:314-320 (`001F5D70` → `0060B980`).
- **RO.CS-10** Character-Rendering/how-a-character-is-lit.md:259: "What sets `02B3F520`, `02B3F503` and `02B3F51C`". Character-Rendering/how-a-character-is-lit.md:370: `003AC900` "multiplies the `02B3F51C` global, `02B3F503` is set to 1".
- **RO.CS-11** CONTRACT-render-record-pool-lifecycle.md:474-477 (§13a, not struck): "The five operations are still **unexecuted** — §13's pilot does not exist". Contradicted by §13 (CONTRACT-render-record-pool-lifecycle.md:372-378) and corrected at CONTRACT-render-record-pool-lifecycle.md:508-511 ("**That sentence was already false when written.**").

(c) Corrected claims repeated unstruck
- **RO.CS-12** Character-Rendering/character-render-object.md:42-45 (§1): "**Twelve of its thirty-one methods check it as the first thing they do** … update, submit, material propagation and transform propagation all return immediately". The correction at Character-Rendering/character-render-object.md:286 says "slot 26 never reads +0x4B4", and CONTRACT-character-render-object.md:102 counts eleven vtable entry gates. Character-Rendering/character-render-object.md:299-301 (§6) "twelve of the class's methods return at their first branch" and Character-Rendering/character-render-object.md:491-495 (§8) "**exactly one is a write** … **all 12 methods that read it**" repeat the overturned figures (overturned at Character-Rendering/character-render-object.md:597-599).
- **RO.CS-13** Character-Rendering/character-render-object.md:304-306 (§6 modding): slot 24 carries "equipment, tint … Neither has been read; both are named only". Character-Rendering/character-render-object.md:38 corrects it: "slot 24 writes the four refraction parameters, not a status tint".
- **RO.CS-14** Character-Rendering/character-render-object.md:887-888: the 0x740 walk is "over this page's own table". CRO §8b (Character-Rendering/character-render-object.md:529-552) says the 0x740 array "is not this class".
- **RO.CS-15** CONTRACT-render-record-pool-lifecycle.md:531: "Bit 5 is set by promotion" omits retire, which also sets bit 5 (CONTRACT-render-record-pool-lifecycle.md:130-131, "**and by retirement (`00427DB3`)**"). CONTRACT-render-record-pool-lifecycle.md:584: "the other bits of `+0x18` are set by unrelated callers", but CONTRACT-render-record-pool-lifecycle.md:132 has promotion bracketing bit 0 itself.
- **RO.CS-16** CONTRACT-render-record-pool-lifecycle.md:115-116: "`0041F730` opens with `memset(record, 0, 0x740)`". CONTRACT-render-record-pool-lifecycle.md:853-856: "`CLR` is a 1,208-byte default writer, not a memset … **A reconstruction that zero-fills a record produces a different record**". The two do not conflict on `+0x284` = 0, but the first wording invites a zero-fill reset.

#### 3.3.3 [RA] The character render record array, render events, focus point and track pick

Short names in this part: **CRR** = `Character-Render-Records/the-character-render-record-array.md`; **RES** = `Character-Render-Records/render-event-selection-evidence.md`; **FOC** = `Character-Render-Records/the-focus-point-of-a-character.md`; **TRK** = `Character-Render-Records/how-a-presentation-entry-picks-its-track.md`.


(a) banner:
- **RA.CS-1.** Character-Render-Records/the-focus-point-of-a-character.md:18-19 and Character-Render-Records/how-a-presentation-entry-picks-its-track.md:19-21 audit notes "pending first review" vs Character-Render-Records/the-focus-point-of-a-character.md:14-17 / Character-Render-Records/how-a-presentation-entry-picks-its-track.md:15-18 `passes: 1`, `last_pass_kind: falsification` and the falsification sections Character-Render-Records/the-focus-point-of-a-character.md:153, Character-Render-Records/how-a-presentation-entry-picks-its-track.md:187.
- **RA.CS-2.** Character-Render-Records/the-character-render-record-array.md:4 "the rest of the 0x130 tail (UQ-197) is SUPERSEDED as a duplicate of BT-3, answered 2026-09-26" vs Character-Render-Records/the-character-render-record-array.md:378 "*(closed — the register row is WITHDRAWN.)*" and Character-Render-Records/the-character-render-record-array.md:987 "`BT-3` answered (OPUS, 2026-09-15)".
- **RA.CS-3.** CRR and RES not listed in README.md at all; FOC has no own README tag (README.md:53).
- **RA.CS-4.** Character-Render-Records/the-character-render-record-array.md:18 `last_reviewed: 2026-09-02` and Character-Render-Records/the-character-render-record-array.md:27 `crossref_clean: false` against a 2026-09-30 status (Character-Render-Records/the-character-render-record-array.md:4).

(b) stale open claims answered elsewhere:
- **RA.CS-5.** Character-Render-Records/how-a-presentation-entry-picks-its-track.md:130 "*Who installs the two callbacks was not read.*" (`[02CA4470]`, `[02CA4440]`) vs Character-Render-Records/render-event-selection-evidence.md:559-561 `002EA320` "registers … id 6 → `002E7090` … id 0xC → `002E70A0`" into `02CA4410 + id*8` (Character-Render-Records/render-event-selection-evidence.md:492) → `02CA4440` = id 6, `02CA4470` = id 0xC; and `Authored-Commands/the-authored-presentation-command-handlers.md:260-264` ("Slot `02CA4470` is read by the **engine**").
- **RA.CS-6.** Character-Render-Records/how-a-presentation-entry-picks-its-track.md:164 "the selector objects behind `[02CA4668]`" not read vs `Authored-Commands/the-authored-presentation-command-handlers.md:913-918` ("the pointer at `02CA4668` is that table: `0x30` entries of `{1, cell}`").
- **RA.CS-7.** Character-Render-Records/render-event-selection-evidence.md:485-487 "external ID invalidation, cleanup-flag producers … remain architectural questions" vs Character-Render-Records/render-event-selection-evidence.md:184 (UQ-193: callers reset ids to −1) and Character-Render-Records/render-event-selection-evidence.md:444 (only setter of bit `1000` is `0041D4D0`). Unannotated, unlike Character-Render-Records/render-event-selection-evidence.md:276, :282, :317.
- **RA.CS-8.** Character-Render-Records/the-character-render-record-array.md:205 "+0x006 i16 (tested == -1 as a latch precondition)" (meaning blank) vs `CONTRACT-coast-down-latch.md:416-425` (owner link, answered 2026-09-22).

(c) corrected claims repeated:
- **RA.CS-9.** `Character-Rendering/character-render-object.md:538` "`160 × 0x740 = 0x48830`" vs Character-Render-Records/the-character-render-record-array.md:425-427 correction "the product is **0x48800** … Two correct numbers joined by a wrong equation."
- **RA.CS-10.** Character-Render-Records/the-character-render-record-array.md:907 previous-X/Y reading vs Character-Render-Records/the-character-render-record-array.md:893 correction (see RA.CV-5).
- **RA.CS-11.** Character-Render-Records/the-character-render-record-array.md:862-863 re-resolve helper vs Character-Render-Records/the-character-render-record-array.md:785 correction (see RA.CV-6).

#### 3.3.4 [RG] Rig controllers, fades, status looks, bone trails and the staged look

Short names in this part: **FADE** = `Character-Render-Records/how-a-character-fades-the-ten-channels.md`; **STAT** = `Character-Render-Records/how-a-status-shows-on-a-character.md`; **TRAIL** = `Character-Render-Records/the-bone-trails.md`; **RIG** = `Character-Render-Records/the-rig-of-seventeen-controllers.md`; **LOOK** = `Character-Render-Records/the-staged-look-command.md`.


(a) banner / tag
- **RG.CS-1 STAT status AUDITED vs README DOCUMENTED.** Character-Render-Records/how-a-status-shows-on-a-character.md:4 "status: AUDITED" vs README.md:55 "**DOCUMENTED, tier 1 (2026-09-19), static.**"
- **RG.CS-2 LOOK status AUDITED, README gives no own entry.** Character-Render-Records/the-staged-look-command.md:4 "status: AUDITED" vs README.md:51 (listed only under the rig's "**DOCUMENTED ...**" line, README.md:48). Same for FADE (README.md:52), whose front matter is DOCUMENTED.
- **RG.CS-3 STAT front-matter note stale.** Character-Render-Records/how-a-status-shows-on-a-character.md:22-23 "six look bodies are named and not read, and the page says which" vs Character-Render-Records/how-a-status-shows-on-a-character.md:370 "every look of the colour list is now read" and section 4b reading all four second-block steps (Character-Render-Records/how-a-status-shows-on-a-character.md:261, :274, :277, :286).
- **RG.CS-4 TRAIL front-matter note: shape "is an inference".** Character-Render-Records/the-bone-trails.md:21-22 "the on-screen shape is an inference and is labelled as one" vs Character-Render-Records/the-bone-trails.md:365 "So section 1's sentence is no longer an inference. The trail is drawn as a textured, Gouraud-shaded, alpha-blended triangle strip".

(b) stale open claims answered elsewhere
- **RG.CS-5 TRAIL body still calls the strip an inference.** Character-Render-Records/the-bone-trails.md:43-45 "that sentence is an inference"; Character-Render-Records/the-bone-trails.md:168-170; Character-Render-Records/the-bone-trails.md:205-206 "The inference in section 5 about a textured strip is unchanged"; Character-Render-Records/the-bone-trails.md:218-219 vs Character-Render-Records/the-bone-trails.md:365-367 (5e decode).
- **RG.CS-6 STAT: second-block steps "named, not read".** Character-Render-Records/how-a-status-shows-on-a-character.md:370-371 "the four step bodies of the second block - named, not read. So what Slow, Stop, Immobilize and Invisible look like is not on this page"; also Character-Render-Records/how-a-status-shows-on-a-character.md:248 "three of the four are read" and Character-Render-Records/how-a-status-shows-on-a-character.md:257 "Three of the four step bodies were read whole" vs Character-Render-Records/how-a-status-shows-on-a-character.md:286 "Immobilize - `0051DE30` (621 B), read whole the same night".
- **RG.CS-7 STAT: HP Critical step "not read".** Character-Render-Records/how-a-status-shows-on-a-character.md:352-353 "Mode 1 is what HP Critical's step writes (...that step was not read, so the colour it blends toward is not on this page)" vs Character-Render-Records/how-a-status-shows-on-a-character.md:158 "HP Critical - step `00470230` (448 B), read whole" and Character-Render-Records/how-a-status-shows-on-a-character.md:152 "record colour `+0x5D0` = (0.84, 0.84, 0.84)".
- **RG.CS-8 `01F82E38` "what it is" open.** Character-Render-Records/how-a-character-fades-the-ten-channels.md:436 "What the global `01F82E38` is" and Character-Render-Records/the-staged-look-command.md:220 "what the global `01F82E38` is" vs `Effect-File-Formats/an-effect-element-frame-by-frame.md:258` "in half-rate mode (`01F82E38` non-zero and `01DFE0C0` zero)".
- **RG.CS-9 `01DFE0BC` frame-rate behaviour open.** Character-Render-Records/the-rig-of-seventeen-controllers.md:279-280 "how that float moves with the frame rate was not established here" vs `Effect-File-Formats/effect-element-type-dispatch.md:949-950` "written together by `001EDDC0` as `{2, 2.0, 0.5}` and shipping as `{1, 1.0, 1.0}`" (and Character-Render-Records/the-bone-trails.md:150).
- **RG.CS-10 LOOK: `+0x18` and `01DFE0B8` open.** Character-Render-Records/the-staged-look-command.md:216 "What the controller's `+0x18` (the minimum-duration floor) and the global scale `01DFE0B8` are" vs Character-Render-Records/the-rig-of-seventeen-controllers.md:180 "the duration is the controller's `+0x18`; zero means one step" and effect-element-type-dispatch.md:949 "01DFE0B8 scale".
- **RG.CS-11 LOOK: rig slots unnamed.** Character-Render-Records/the-staged-look-command.md:213-214 "the reset functions of the others were not read" vs Character-Render-Records/the-staged-look-command.md:153-155 and Character-Render-Records/the-rig-of-seventeen-controllers.md:71-89 naming fifteen slots; Character-Render-Records/the-staged-look-command.md:168-175 reads the small resets itself.
- **RG.CS-12 FADE: setter's other callers not read.** Character-Render-Records/how-a-character-fades-the-ten-channels.md:248 "The setter's two other callers, both record phases, were not read" vs Character-Render-Records/how-a-character-fades-the-ten-channels.md:189-190 (0042CBF0, read whole, calls `003B33A0`) - one of them at least is read. (Lean; the second caller is not named.)
- **RG.CS-13 FADE section 6 asks what the handle tables / aux handles are.** Character-Render-Records/how-a-character-fades-the-ten-channels.md:428-430 "What the two handle tables of 4d and the object in the table at `02EBD480` are; what the effect object and the four auxiliary handles are" vs Character-Render-Records/how-a-character-fades-the-ten-channels.md:353-357 (shadow pool), Character-Render-Records/how-a-character-fades-the-ten-channels.md:401-404 (render-object handle table), Character-Render-Records/how-a-character-fades-the-ten-channels.md:385-387 (aux handles are bone trails). The `+0x118` table at 02B3F570 remains (see §2.1).
- **RG.CS-14 FADE: who fills 02AEDEF0.** Character-Render-Records/how-a-character-fades-the-ten-channels.md:433 "What fills that matrix was not traced" vs `Scripted-Camera/how-a-camera-reaches-the-renderer.md:116` "`02AEDEF0` | a copy of the **capped-field-of-view copy's** matrix".
- **RG.CS-15 RIG: what raises `+0x40B` bits 5-7.** Character-Render-Records/the-rig-of-seventeen-controllers.md:125 "(bits 5, 6 and 7; what raises them was not read)" vs Character-Render-Records/the-rig-of-seventeen-controllers.md:364 "`dword[+0x304] bit7` folds into `byte[+0x40B] bit6`", Character-Render-Records/the-rig-of-seventeen-controllers.md:369-370, Character-Render-Records/the-rig-of-seventeen-controllers.md:374-375.
- **RG.CS-16 RIG: controller 12 trigger.** Character-Render-Records/the-rig-of-seventeen-controllers.md:257 "what triggers it was not traced" vs Character-Render-Records/the-rig-of-seventeen-controllers.md:139-146 (event handler 00427320 on 0x2005 / 0x2006).
- **RG.CS-17 STAT: light kind 1 unknown.** Character-Render-Records/how-a-status-shows-on-a-character.md:375-376 "What light kind 1 is (directional, point, spot) was not read" vs `Character-Rendering/how-a-character-is-lit.md:142` "**Kind 1 is a directional light - `003AD540` (745 B), read whole.**" (and Character-Render-Records/how-a-status-shows-on-a-character.md:176 itself calls 0x0100BE01 "a directional light").
- **RG.CS-18 STAT: Slow's q constant.** Character-Render-Records/how-a-status-shows-on-a-character.md:281 "`q` being the pulse times a double constant not converted here" vs Character-Render-Records/how-a-status-shows-on-a-character.md:288 "the two double constants are 0.1 and 0.3".
- **RG.CS-19 STAT: variant binder caller not read.** Character-Render-Records/how-a-status-shows-on-a-character.md:120-121 "Its one caller is the record-side routine that ensures a character's bindings, not read" vs Character-Render-Records/the-bone-trails.md:465 "`003E7210` (414 B) ... `00504D30` runs per element" (shape-level only; lean).

(c) corrected claim repeated unstruck
- **RG.CS-20 FADE: "channels 2, 3, 5 have no writer" still unstruck.** Character-Render-Records/how-a-character-fades-the-ten-channels.md:424 "What channels 2, 3 and 5 were for. No body writes them; nothing in this executable can say." and Character-Render-Records/how-a-character-fades-the-ten-channels.md:446 "channels 2, 3, 5 have no writer" vs correction Character-Render-Records/how-a-character-fades-the-ten-channels.md:113 "**Correction 2026-09-19 (FABLE): channels 2 and 5 are written**".
- **RG.CS-21 FADE: "viewer block flag bit 4" name.** Character-Render-Records/how-a-character-fades-the-ten-channels.md:515 "viewer block flag bit 4" vs Character-Render-Records/how-a-character-fades-the-ten-channels.md:227-228 "*(The channel table above said "the camera block's `+0x48818`"; that was wrong.)*" - the 7a row keeps the old "viewer block" naming.

#### 3.3.5 [CL] Ordered render command list and graphics-thread handshake

Short names in this part: **C** = `CONTRACT-render-command-list-and-graphics-handshake.md`; **L** = `Render-Command-List/the-ordered-render-command-list.md`; **H** = `Graphics-Thread-Handshake/the-shared-command-state-word.md`.


(a) Banners and tags:

**CL.CS-1. Status of the list page.** The list page front matter says `status: AUDITED` (Render-Command-List/the-ordered-render-command-list.md:4). README.md:89 says "**DOCUMENTED, tier 1, crossref-clean.**" README.md:91 still carries the struck "draw-order key" reading (see CL.CV-1).

**CL.CS-2. Pages missing from the README.** C (`readiness: BEHAVIORALLY UNDERSTOOD`, CONTRACT-render-command-list-and-graphics-handshake.md:6) and H (`status: AUDITED`, Graphics-Thread-Handshake/the-shared-command-state-word.md:4) are not listed in README.md.

**CL.CS-3. "Empty" runtime section.** CONTRACT-render-command-list-and-graphics-handshake.md:416 says "Empty. Nothing in this contract has been observed on a running game." But CONTRACT-render-command-list-and-graphics-handshake.md:143 cites "OPUS's execution measured capacities 1 → 2 → 4 → 8".

(b) Stale open claims:

**CL.CS-4. Unknown order keys.** Render-Command-List/the-ordered-render-command-list.md:491-492 "The remaining classes in §4.1 were not opened in this pass and their keys are unknown". Answered at Render-Command-List/the-ordered-render-command-list.md:670-673: "ANSWERED 2026-09-12 (OPUS): all 36 read".

**CL.CS-5. Sort site not found.** Render-Command-List/the-ordered-render-command-list.md:917-918 "the sort site itself is still unfound". Render-Command-List/the-ordered-render-command-list.md:924-926 "no consumer was found". Render-Command-List/the-ordered-render-command-list.md:1016 "no consumer that walks either list has been located". Render-Command-List/the-ordered-render-command-list.md:1044-1047 "`-13-7` stays open … The sort and execution site remain unlocated". Answered at Render-Command-List/the-ordered-render-command-list.md:596: "Answered 2026-09-14 (FABLE): it is executed in stored order, and it is not sorted."

**CL.CS-6. Descriptor array contents.** Render-Command-List/the-ordered-render-command-list.md:389 "What they hold is not established". Render-Command-List/the-ordered-render-command-list.md:986-987 (pass 1, 2026-09-12): "It is the Complete Object Locator of the next class".

**CL.CS-7. Why AO ends the walk.** CONTRACT-render-command-list-and-graphics-handshake.md:428-430 "Why does ambient occlusion terminate the walk? … its purpose is not in the bytes … Routed to ASTRA." Answered at CONTRACT-render-command-list-and-graphics-handshake.md:184 "(GC-1 answered 2026-09-25 …)" and at Render-Command-List/the-ordered-render-command-list.md:1943 "ANSWERED 2026-09-25 … 'Display AO Only' view".

**CL.CS-8. Manager cleared without destroy.** Render-Command-List/the-ordered-render-command-list.md:667-668 "Not established: whether any path clears the manager without the vector also being destroyed in the same frame." Answered at CONTRACT-render-command-list-and-graphics-handshake.md:128-134: "all three teardown sites … the image-wide census of both destroyers' callers finds exactly these three, each with the clear first". Render-Command-List/the-ordered-render-command-list.md:601 also lists the clear's three call sites.

(c) Corrected claims still repeated:

**CL.CS-9. The assert.** Render-Command-List/the-ordered-render-command-list.md:81 "asserts it is non-null before doing so". Render-Command-List/the-ordered-render-command-list.md:322 "returns `01F7F5E0`, asserts non-null". Corrected at Render-Command-List/the-ordered-render-command-list.md:1930 "`0018B4E0` does not assert (`CON-151`)" and at CONTRACT-render-command-list-and-graphics-handshake.md:194-198.

**CL.CS-10. Two teardown sites.** Render-Command-List/the-ordered-render-command-list.md:1913-1914 "identical at both sites". Graphics-Thread-Handshake/the-shared-command-state-word.md:895 "the fixed clear-then-destroy pair at both teardown sites". Corrected to three at CONTRACT-render-command-list-and-graphics-handshake.md:128 "~~both~~ all three" and CONTRACT-render-command-list-and-graphics-handshake.md:536.

**CL.CS-11. Twelve spin sites.** Graphics-Thread-Handshake/the-shared-command-state-word.md:166 "reported at 12 sites against their 11". Graphics-Thread-Handshake/the-shared-command-state-word.md:331 "Eleven inlined sites on this global, twelve overall". Corrected at Graphics-Thread-Handshake/the-shared-command-state-word.md:108 "Eleven settle-spin loops exist in `.text`" and Graphics-Thread-Handshake/the-shared-command-state-word.md:132-139.

**CL.CS-12. The second thread.** Graphics-Thread-Handshake/the-shared-command-state-word.md:29-30 "the thread that runs the game and the thread that draws it". Graphics-Thread-Handshake/the-shared-command-state-word.md:72-73 "when the other thread is not part-way through updating it". Graphics-Thread-Handshake/the-shared-command-state-word.md:158-159 "on the hardware, another core writes it". Withdrawn at Graphics-Thread-Handshake/the-shared-command-state-word.md:358 ("Withdrawn") and Graphics-Thread-Handshake/the-shared-command-state-word.md:307-310 (CG-3: "no backend thread behind it").

#### 3.3.6 [GP] Gi render commands and the legacy PS2 GS/VIF layer

Short names in this part: **GI** = `Gi-Render-Commands/gi-render-command-family.md`; **TEX** = `Legacy-PS2-GS/texture-mip-local-memory-budget.md`; **VIF** = `Legacy-PS2-GS/the-vif1-vu1-layer.md`.


(a) status disagreements
**GP.CS-1 GI status.** Gi-Render-Commands/gi-render-command-family.md:4 `status: AUDITED` vs README.md:95 "**DOCUMENTED, tier 1.**"; also Gi-Render-Commands/gi-render-command-family.md:18 `last_reviewed: 2026-09-02` while body corrections run to 2026-09-26 (e.g. Gi-Render-Commands/gi-render-command-family.md:86).
**GP.CS-2 TEX status.** Legacy-PS2-GS/texture-mip-local-memory-budget.md:4 `status: AUDITED` vs Legacy-PS2-GS/texture-mip-local-memory-budget.md:277 "**APPLIED AND PERSISTENCE-CERTIFIED**" vs README.md:102 (no tag).
**GP.CS-3 VIF status.** Legacy-PS2-GS/the-vif1-vu1-layer.md:4 "DOCUMENTED — ... (box pending)" vs Legacy-PS2-GS/the-vif1-vu1-layer.md:32 "**PARTIAL.**" vs Legacy-PS2-GS/the-vif1-vu1-layer.md:902 "page is PARTIAL" vs README (not listed); the boxes are ticked: Legacy-PS2-GS/the-vif1-vu1-layer.md:798 "- [x] **UQ-213.**", Legacy-PS2-GS/the-vif1-vu1-layer.md:825 "- [x] **UQ-215.**".

(b) stale open claims answered elsewhere
**GP.CS-4 VIF banner "Not read".** Legacy-PS2-GS/the-vif1-vu1-layer.md:33-36 "Not read: what any single microprogram draws; how the GS data is finally turned into PC draw calls; the UNPACK formats." vs Legacy-PS2-GS/the-vif1-vu1-layer.md:799 (UQ-213 answered), Legacy-PS2-GS/the-vif1-vu1-layer.md:273-372 + Legacy-PS2-GS/the-vif1-vu1-layer.md:843 (GS translator), Legacy-PS2-GS/the-vif1-vu1-layer.md:826-839 (UQ-215 answered).
**GP.CS-5 `[01FC35F8]` class.** Legacy-PS2-GS/the-vif1-vu1-layer.md:369 "The object's class is not identified here." and Legacy-PS2-GS/the-vif1-vu1-layer.md:374-375 "Not read: ... the class behind `[01FC35F8]`", Legacy-PS2-GS/the-vif1-vu1-layer.md:754 "GS emulation (not read)" vs Legacy-PS2-GS/the-vif1-vu1-layer.md:843 "`[01FC35F8]` holds `02CC1CD0` = `02CC0410 + 0x18C0`, the embedded `PrimitiveRendererD3D11`".
**GP.CS-6 Render-thread stream.** Legacy-PS2-GS/the-vif1-vu1-layer.md:270-271 "Not read here: the render-thread command stream that `001F49F0` hands the replay to — see the Gi family page §12e, where the remaining gap is now stated" vs Gi-Render-Commands/gi-render-command-family.md:1326 "BG-11 is answered."
**GP.CS-7 Display-list drain.** Gi-Render-Commands/gi-render-command-family.md:365-367 "The display list's drain was not found. ... BG-7." vs Gi-Render-Commands/gi-render-command-family.md:375 "`FUN_003A3740` (587 B) reads the count, early-outs at zero, sorts the list".
**GP.CS-8 BG-11 open.** Gi-Render-Commands/gi-render-command-family.md:842 "BG-11 stays open with its sharpened question recorded" vs Gi-Render-Commands/gi-render-command-family.md:1326.
**GP.CS-9 CharacterRenderObject `+0x4B4`.** Gi-Render-Commands/gi-render-command-family.md:1073-1074 "Unresolved: what state `+0x4B4` etc. encode" vs README.md:100 "a ready flag at `+0x4B4` with one writer at the end of setup" (Character-Rendering/character-render-object.md:65 "The ready flag at `+0x4B4`").
**GP.CS-10 VU-state touchers.** Legacy-PS2-GS/the-vif1-vu1-layer.md:779 "VU helper — VU-state toucher, not installed | 54" and Legacy-PS2-GS/the-vif1-vu1-layer.md:793-794 "19 have no E8/E9 caller — consistent with VU `JAL`/`JR` sub-programs" vs Legacy-PS2-GS/the-vif1-vu1-layer.md:851 "none of the 19 is a `JAL` / `JR` sub-program target ... All 19 are VU1 microprogram entries"; also the six "sibling touchers" of Legacy-PS2-GS/the-vif1-vu1-layer.md:792 (`00499A20` …) are among the ten microprograms added at Legacy-PS2-GS/the-vif1-vu1-layer.md:411.

(c) corrected claim repeated unstruck
**GP.CS-11 Reset commands "pass 3".** Gi-Render-Commands/gi-render-command-family.md:243-244 "and the two reset commands pass **3**" vs Gi-Render-Commands/gi-render-command-family.md:138 "WITHDRAWN, pass 8. Neither reset command makes any device-vtable call."
**GP.CS-12 "Exactly 4 sites".** Gi-Render-Commands/gi-render-command-family.md:298-300 "occurs at exactly 4 sites image-wide, all `Gi*`. Nothing outside this family touches the interface." vs Gi-Render-Commands/gi-render-command-family.md:888 "the true count of `Gi*` sites through `[dev+0x000]` is 5".
**GP.CS-13 Device "not a C++ class".** Gi-Render-Commands/gi-render-command-family.md:270 heading "The device is not a C++ class" and Gi-Render-Commands/gi-render-command-family.md:302-303 "The device layer is either compiled `/GR-` or is a hand-rolled C-style vtable struct. It is not a Phyre class and not any class in the index." vs Gi-Render-Commands/gi-render-command-family.md:1356-1357 "The device's class is `PrimitiveRendererD3D11`, which is RTTI-bearing."
**GP.CS-14 "Something writes ctx+0".** Gi-Render-Commands/gi-render-command-family.md:616-618 and Gi-Render-Commands/gi-render-command-family.md:804-806 "Something writes `ctx+0` between enqueue and invocation, and it has not been found." vs Gi-Render-Commands/gi-render-command-family.md:1302-1303 "The four passes searching for a writer of `block+0` were looking for something that does not exist."
**GP.CS-15 47 microprograms.** Legacy-PS2-GS/the-vif1-vu1-layer.md:749 "47 microprograms" and Legacy-PS2-GS/the-vif1-vu1-layer.md:20 "The 47 is internally consistent" vs Legacy-PS2-GS/the-vif1-vu1-layer.md:411 "~~47~~ 57 distinct microprograms".
**GP.CS-16 Tagless builders "fully accounted".** Legacy-PS2-GS/the-vif1-vu1-layer.md:654 "So §2.4c's 29 tagless builders are fully accounted: 21 author no `UNPACK` at all, and the 8 that do contain no tag." vs Legacy-PS2-GS/the-vif1-vu1-layer.md:649 "`00476C80` is the exception - its fill loop ... writes an A+D GIF tag".

#### 3.3.7 [EF] Effect containers, element dispatch and the per-frame element update

Short names in this part: **DISP** = `Effect-File-Formats/effect-element-type-dispatch.md`; **FBF** = `Effect-File-Formats/an-effect-element-frame-by-frame.md`; **EFX** = `Effect-File-Formats/efx-and-efb-effect-containers.md`; **ERM** = `Effect-File-Formats/README.md`; **CAT** = `README.md`.


(a) Status disagreements
- **EF.CS-1 FBF status vs CAT.** "status: AUDITED" (Effect-File-Formats/an-effect-element-frame-by-frame.md:4) vs "**DOCUMENTED, tier 1 (2026-09-19), static.**" (README.md:65).
- **EF.CS-2 DISP front matter vs body.** "status: DOCUMENTED" (Effect-File-Formats/effect-element-type-dispatch.md:4) vs "**PARTIAL.**" (Effect-File-Formats/effect-element-type-dispatch.md:32) and "(Page status PARTIAL …)" (Effect-File-Formats/effect-element-type-dispatch.md:1055); not in CAT.
- **EF.CS-3 EFX banner/front matter vs §2b.** "**No `.efx` or `.efb` file was opened to write this sheet.**" (Effect-File-Formats/efx-and-efb-effect-containers.md:39); `corpus_validated: "… First 8 bytes only — the payload is still unmeasured."` (Effect-File-Formats/efx-and-efb-effect-containers.md:18); "payload still unmeasured" (Effect-File-Formats/efx-and-efb-effect-containers.md:26) vs "every `.efx` and `.efb` file has now been opened for this sheet's own claims" (Effect-File-Formats/efx-and-efb-effect-containers.md:59-60). EFX and DISP and ERM not listed in CAT.

(b) Stale open claims answered elsewhere
- **EF.CS-4** "nothing in the database describes either one" (Effect-File-Formats/README.md:8-9) / "A sheet should settle that" (Effect-File-Formats/README.md:15) vs "**They are not container and payload — they are two formats sharing one container convention**" (Effect-File-Formats/efx-and-efb-effect-containers.md:524-525).
- **EF.CS-5** DISP "Not read: what any individual element type is; … the link from the EFX chunk runs to element creation" (Effect-File-Formats/effect-element-type-dispatch.md:37-40) vs "**UQ-204 — ANSWERED …: what each of the 65 types puts on screen is a table**" (Effect-File-Formats/effect-element-type-dispatch.md:894) and "**Who installs it into the element.** The chain is closed end to end" (Effect-File-Formats/effect-element-type-dispatch.md:827).
- **EF.CS-6** "The type values have not yet been matched to authored effect data" (Effect-File-Formats/effect-element-type-dispatch.md:43-44) vs §2.8 "the element's dispatch key **is** the authored byte" (Effect-File-Formats/effect-element-type-dispatch.md:842-843).
- **EF.CS-7** "Which of those paths is update, draw or creation is **not read**" (Effect-File-Formats/effect-element-type-dispatch.md:149) vs "the step runs once, at the element's birth … The per-frame work is the update (§2.2) and the walk (§2.4)" (Effect-File-Formats/effect-element-type-dispatch.md:55-58).
- **EF.CS-8** "Not read here: … the three predicates `0024E460`, `003A3D20`, `003A2C70`; the drain end of the list" (Effect-File-Formats/effect-element-type-dispatch.md:605-607) vs "`0024E460` (79 B) is the predicate the effect dispatchers call" (Effect-File-Formats/effect-element-type-dispatch.md:1243) and "**The drain in full**" (Effect-File-Formats/effect-element-type-dispatch.md:458-467).
- **EF.CS-9** "*Not* answered: what each of the types is" (Effect-File-Formats/effect-element-type-dispatch.md:902) vs UQ-204 answered (Effect-File-Formats/effect-element-type-dispatch.md:894-899).
- **EF.CS-10** Type-groups row "`0x00`–`0x0A` … step/update tail helpers and emit calls `not read`" (Effect-File-Formats/effect-element-type-dispatch.md:887) vs FBF reading all nine tails "read whole" (Effect-File-Formats/an-effect-element-frame-by-frame.md:9-11, 168).
- **EF.CS-11** "§2's `+0x08` second header half and the payload at `+0x10` remain unmeasured" (Effect-File-Formats/efx-and-efb-effect-containers.md:600-602) and "that search was not run" (Effect-File-Formats/efx-and-efb-effect-containers.md:538) vs §2b (Effect-File-Formats/efx-and-efb-effect-containers.md:222-233) and correction (Effect-File-Formats/efx-and-efb-effect-containers.md:615-617).

(c) Corrected claims still repeated unstruck
- **EF.CS-12** Step still called per-frame: "### 2.1 The per-frame step" (Effect-File-Formats/effect-element-type-dispatch.md:53), "`002F3BC0` (frame step)" (Effect-File-Formats/effect-element-type-dispatch.md:98), "the frame counter step" (Effect-File-Formats/effect-element-type-dispatch.md:35), "`+0x224 u16  stamp from 00250000(), set each step`" (Effect-File-Formats/effect-element-type-dispatch.md:879) vs "~~per-frame~~ step (birth)" (Effect-File-Formats/effect-element-type-dispatch.md:864) and the correction (Effect-File-Formats/effect-element-type-dispatch.md:55).
- **EF.CS-13** "each carrying a 24-bit flags word" (Effect-File-Formats/effect-element-type-dispatch.md:361) unstruck vs "**The record's `+8` is the sort key, not a flags word.**" (Effect-File-Formats/effect-element-type-dispatch.md:562).
- **EF.CS-14** EFX struct "`_unread`" (Effect-File-Formats/efx-and-efb-effect-containers.md:81, 86) and "a 16-byte header whose second half nothing reads" (Effect-File-Formats/efx-and-efb-effect-containers.md:527) unstruck vs correction (Effect-File-Formats/efx-and-efb-effect-containers.md:615-617). (Also EF.CV-19.)
- **EF.CS-15** "The `0x600` chunk zero-fill (§2) is the only normalisation found" (Effect-File-Formats/efx-and-efb-effect-containers.md:448-449) unstruck vs correction (Effect-File-Formats/efx-and-efb-effect-containers.md:479). (Also EF.CV-20.)
- **EF.CS-16** "## 4. The other seven tails" (Effect-File-Formats/an-effect-element-frame-by-frame.md:163) unstruck vs "six tails, not seven" (Effect-File-Formats/an-effect-element-frame-by-frame.md:165).

#### 3.3.8 [ET] Effect element types, kind-0x54 meshes, menu effect registry and VFX layers

Short names in this part: **mesh** = `Effect-File-Formats/effect-mesh-records-kind-54.md`; **00-0a** = `Effect-File-Formats/the-element-types-00-0a.md`; **40-42** = `Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md`; **60-74** = `Effect-File-Formats/the-element-types-60-74.md`; **80-97** = `Effect-File-Formats/the-element-types-80-97.md`; **menu** = `Effect-File-Formats/the-menu-effect-registry.md`; **six-layers** = `Effect-File-Formats/the-six-vfx-display-layers.md`.


(a) banner disagreements
- **ET.CS-1** Effect-File-Formats/the-menu-effect-registry.md:4 "DOCUMENTED … all answered 2026-09-17" vs Effect-File-Formats/the-menu-effect-registry.md:33-34 "PARTIAL. … Not read: the record's fields past +8, what +0x338 in an instance means, and which menu uses which id."
- **ET.CS-2** Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:4 "DOCUMENTED … no open box" vs Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:317-318 "page is PARTIAL — no disposition claimed".
- **ET.CS-3** Effect-File-Formats/effect-mesh-records-kind-54.md:4 "SD-140 answered 2026-10-01 (SWE2-ORACLE…)" vs Effect-File-Formats/effect-mesh-records-kind-54.md:213 "(Answered 2026-09-30, SWE2-ORACLE".
- **ET.CS-4** Effect-File-Formats/the-six-vfx-display-layers.md:4 "DOCUMENTED" with :19-20 "pending first review" vs :246 "Falsification pass 1 — 2026-09-29 (OPUS)".
- **ET.CS-5** Effect-File-Formats/the-element-types-00-0a.md:4 "DOCUMENTED — every register row is closed" vs Effect-File-Formats/the-element-types-00-0a.md:12 `last_reviewed: 2026-09-15` and the open not-read list Effect-File-Formats/the-element-types-00-0a.md:349-355 (incl. `0039D6C0`, see ET.CS-8).

(b) stale open claims answered elsewhere
- **ET.CS-6** Effect-File-Formats/the-menu-effect-registry.md:52 "record +0x10 .. +0x27  not read" vs Effect-File-Formats/the-menu-effect-registry.md:114 "ANSWERED 2026-09-17 … `+0x10 = a`, `+0x14 = b`, `+0x18 = c`, `+0x1C = kind`".
- **ET.CS-7** Effect-File-Formats/the-menu-effect-registry.md:136 "`003B2CA0` and `003B2CE0`, whose roles are not read" vs Effect-File-Formats/the-menu-effect-registry.md:230 "`003B2CE0` (129 B) is a call-free menu-effect classifier".
- **ET.CS-8** Effect-File-Formats/the-element-types-00-0a.md:348-349 "the blended line emitter `0039D6C0`;" (unstruck in not-read list) vs Effect-File-Formats/the-element-types-00-0a.md:273 "the line's `0039D6C0` (457 B, read 2026-10-01 by OPUS" and :485.
- **ET.CS-9** Effect-File-Formats/the-element-types-00-0a.md:354 not-read list includes "`00432300`" vs Effect-File-Formats/effect-mesh-records-kind-54.md:217-218 "The kernel `00432300` is the PS2 colour modulate `min(255, e·c >> 7)`".
- **ET.CS-10** Effect-File-Formats/the-element-types-00-0a.md:360-362 "`02AEE900` … and `02AEE908` … by type-`0x01` walk — draw-state args, unconfirmed consumers" vs Effect-File-Formats/the-element-types-00-0a.md:249 "choose one of two emitters on `02AEE900`" and :276 "Mode 6 … takes `02AEE908`".
- **ET.CS-11** Effect-File-Formats/the-element-types-00-0a.md:396 "`00446050` … registered GI-14" vs Effect-File-Formats/the-element-types-00-0a.md:4 "GI-14 answered" / :503 "GI-14 is answered" — the GI-14 section (:467-503) does not cover `00446050`; :430 still lists it.

(c) corrected claim repeated unstruck
- **ET.CS-12** Effect-File-Formats/effect-mesh-records-kind-54.md:33-34 "the colour and UV labels for `+0x28` / `+0x2C` stay distributional (`SD-140`)" and Effect-File-Formats/effect-mesh-records-kind-54.md:119-121 "Normals hypothesis." / "Colour hypothesis." / "UV hypothesis." vs Effect-File-Formats/effect-mesh-records-kind-54.md:213-216 answered.
- **ET.CS-13** Effect-File-Formats/the-element-types-60-74.md:342 "`+0x44 = 0x67` (corrected …) creation arm … the eight-group 0x65 setup this page already names" — the "0x65" tail left after the type was corrected to 0x67.
- **ET.CS-14** Effect-File-Formats/the-element-types-80-97.md:50 "base + PRNG `0044B960` + tail" unstruck after Effect-File-Formats/the-element-types-80-97.md:114 correction (see ET.CV-1).
- **ET.CS-15** six-layers README tag (README.md:78-79) "Layer 3 has its own path, beside the depth-sorted display list" — compatible with the page, but page :124-128 withdrew the layer-3/sorted-list reading; README tag date "2026-09-19" predates the 2026-09-29 falsification and corrections (:246-269). Minor.

#### 3.3.9 [MF] Model formats: add-motion tables, ADM, FCP, FDM/FOR

Short names in this part: **SKEL** = `Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md`; **ADM** = `Model-And-Motion-Formats/adm-add-motion-tables.md`; **FCP** = `Model-And-Motion-Formats/fcp-character-parameter-block.md`; **FDM** = `Model-And-Motion-Formats/fdm-and-for-entries.md`; **MREADME** = `Model-And-Motion-Formats/README.md`.


**(a) Banner and front matter**

**MF.CS-1. None of the four pages is in the category README.** Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:4 and Model-And-Motion-Formats/adm-add-motion-tables.md:4 say `status: AUDITED`, and Model-And-Motion-Formats/fcp-character-parameter-block.md:4 and Model-And-Motion-Formats/fdm-and-for-entries.md:4 say `status: DOCUMENTED …`. `README.md` lists no tag for any of them (only `README.md:69-72`, the pose sequencer).

**MF.CS-2. FCP pass count.** Model-And-Motion-Formats/fcp-character-parameter-block.md:21 says `passes: 1`. Model-And-Motion-Formats/fcp-character-parameter-block.md:23 says `last_pass_state: opus-fcp-character-parameter-block-pass-2`, and Model-And-Motion-Formats/fcp-character-parameter-block.md:413 is headed "Falsification pass 2 — 2026-09-13 (OPUS)". Model-And-Motion-Formats/fcp-character-parameter-block.md:19 says `last_reviewed: 2026-09-11` against the status re-dated 2026-10-01 (Model-And-Motion-Formats/fcp-character-parameter-block.md:4).

**MF.CS-3. SKEL pass count.** Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:26-27 says `passes: 1`, `last_pass: 2026-09-13`. The body has a second pass, Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:159 "Run 2026-09-15 (OPUS)", and HM-1 edits dated 2026-09-27 (Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:210-220). Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:21 still says `last_reviewed: 2026-09-13`.

**MF.CS-4. ADM review date.** Model-And-Motion-Formats/adm-add-motion-tables.md:20 says `last_reviewed: 2026-09-13`. The body was answered 2026-09-24/26 (Model-And-Motion-Formats/adm-add-motion-tables.md:415, 429).

**(b) Stale "open / not established" claims**

**MF.CS-5. SKEL §1: which models.** Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:57-58 says "Which models these are on screen is not established here (§7)". It is answered at Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:214 "the table maps a model to its own high-detail variants" and Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:218 "`hc1006_03` is `c1006`'s replacement BODY".

**MF.CS-6. SKEL §7 "Still open".** Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:235-236 says "Still open: which models the ids name …, what pose mode 2 is, and which model the mapping's second skeleton is". It is answered at Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:211-215 (ids name files/kinds), Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:216-218 (the second skeleton is the parent; state 2 is the binding state) and Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:218 ("So the 39 values map `hc1006_03`'s joints onto the bound `c1006` model's skeleton").

**MF.CS-7. SKEL §9: `keyB` / `keyC`.** Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:299-300 says "What `keyB` / `keyC` select when they are not `-1` — four records set them and nothing here says to what". It is answered at Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md:225-227: "`b` and `c` are the actor's secondary-context bytes `+0x14C` and `+0x14D`: the model local number (default 1) and CLUT number (default 0)".

**MF.CS-8. ADM §1: what `_town` changes.** Model-And-Motion-Formats/adm-add-motion-tables.md:60-61 says "what the `_town` twin changes, are not established (§7)". It is answered at Model-And-Motion-Formats/adm-add-motion-tables.md:493-494: "`_town` tables are the civilian-area variants of the same additive-pose tracks". (Model-And-Motion-Formats/README.md:33 records this.)

**MF.CS-9. ADM §5: cross-tabulation.** Model-And-Motion-Formats/adm-add-motion-tables.md:180-181 says "was not cross-tabulated". It is answered at Model-And-Motion-Formats/adm-add-motion-tables.md:230-232: "**the same 35 tracks** — tested as set equality".

**MF.CS-10. ADM §6: falsification pass.** Model-And-Motion-Formats/adm-add-motion-tables.md:185 says "Not yet run." Against it, Model-And-Motion-Formats/adm-add-motion-tables.md:204 "Falsification pass 1 — 2026-09-13 (OPUS)" and Model-And-Motion-Formats/adm-add-motion-tables.md:26 `last_pass_state: opus-adm-tables-pass-1`.

**MF.CS-11. ADM record element types.** Model-And-Motion-Formats/adm-add-motion-tables.md:93 says "the element types are not fixed by the code", and Model-And-Motion-Formats/adm-add-motion-tables.md:99 says "a reading of the data and not a traced type (§7)". It is answered at Model-And-Motion-Formats/adm-add-motion-tables.md:420: "A record is `{i32 bone; f32 eulerDeg[3]; f32 offset[3]}`".

**MF.CS-12. ADM §9: the marked track and track 0.** Model-And-Motion-Formats/adm-add-motion-tables.md:244 says "What it is for is not established", and Model-And-Motion-Formats/adm-add-motion-tables.md:260-261 says "Whether `AddMotion_ApplyBonePose` treats track 0 differently". It is answered at Model-And-Motion-Formats/adm-add-motion-tables.md:465-472 (the `field00 = 1` id-match tracks are track 0) and Model-And-Motion-Formats/adm-add-motion-tables.md:483-484 ("the base-pose sentinel for the id-match track").

**MF.CS-13. ADM §4: read depth of `003714A0`.** Model-And-Motion-Formats/adm-add-motion-tables.md:167 marks `003714A0` as "◐ the track/record walk `003716B0`–`0037175C` and the rotation call". Model-And-Motion-Formats/adm-add-motion-tables.md:417 says "full disassembly of `AddMotion_ApplyBonePose` (`003714A0`)". (`Model-And-Motion-Formats/the-pose-sequencer.md:104-105` also says "the rest of its 3,387 bytes not".)

**MF.CS-14. FDM layout block: tables A/B.** Model-And-Motion-Formats/fdm-and-for-entries.md:76 says "table A — small records (3 B stride …; content unresolved)", and Model-And-Motion-Formats/fdm-and-for-entries.md:77 says "table B — … (unresolved)". It is answered at Model-And-Motion-Formats/fdm-and-for-entries.md:131-156: "Table A/B resolved 2026-09-29".

**MF.CS-15. FDM `+0x20` parameter block.** Model-And-Motion-Formats/fdm-and-for-entries.md:94 says "0xA0-byte parameter block, `0xFF` defaults … consumers unresolved". It is partly answered at Model-And-Motion-Formats/fdm-and-for-entries.md:136-138 and Model-And-Motion-Formats/fdm-and-for-entries.md:157-158 ("five `0x20`-stride part sub-records", read by the builder).

**(c) Corrected claims still repeated unstruck**

**MF.CS-16. "Section 18" in the falsification-pass table.** Model-And-Motion-Formats/fcp-character-parameter-block.md:440 says "| 0–10, 18 — the real table |". It was corrected at Model-And-Motion-Formats/fcp-character-parameter-block.md:651: "Every 'section 18' byte region reported earlier is section 2's own extent or its neighbour — no section 18 exists".

**MF.CS-17. Header fence width.** Model-And-Motion-Formats/fcp-character-parameter-block.md:452-453 says "the fence narrowed to `u16[19]`". The current fence is Model-And-Motion-Formats/fcp-character-parameter-block.md:80 and Model-And-Motion-Formats/fcp-character-parameter-block.md:654: "`u16[18]  sectionOffset`".

**MF.CS-18. Section 21 in the §6 table.** Model-And-Motion-Formats/fcp-character-parameter-block.md:299 says "The five files where section 21 starts inside that span are named in section 2." It was corrected at Model-And-Motion-Formats/fcp-character-parameter-block.md:129-131: "**There is no section 21**".

**MF.CS-19. Section 5 "authored-only".** Model-And-Motion-Formats/fcp-character-parameter-block.md:374 (the 2026-09-21 SUPERSEDED note) says "Sections 5 and 11–17 are authored-only — never present or never read." It was corrected at Model-And-Motion-Formats/fcp-character-parameter-block.md:668: "~~**none** — present in 7 blocks, unread~~ inline in `003E7210`, the palette-binding walk of authored command `0x16` … *(corrected 2026-10-01, OPUS …)*".

#### 3.3.10 [MM] Motion formats: FEF/motion entries, FRP, FTE/FCT, FTR, oscillator, pose sequencer

Short names in this part: **ACH** = `Authored-Commands/the-authored-presentation-command-handlers.md`.


(a) banner
**MM.CS-1 Oscillator front-matter dates lag the body.** `last_reviewed: 2026-09-14` and `last_pass: 2026-09-14` (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:18, :22) vs body sections "GI-19 … (OPUS, 2026-10-01)" and "Qualified 2026-10-02" (:376, :403) and status "owner re-status 2026-10-01" (:4).

**MM.CS-2 Pose-sequencer note "pending first review".** "… so that it can never store; pending first review" (Model-And-Motion-Formats/the-pose-sequencer.md:25) vs `last_pass: 2026-09-29`, `last_pass_kind: falsification` (:17-18) and "No correction." (:279). README tag "DOCUMENTED, tier 1." (README.md:69-70) agrees with status (:4).

**MM.CS-3 Category README coverage.** Five of the six pages (fef, frp, fte-fct, ftr, oscillator) have no entry in README.md (grep: no hit); frp is AUDITED (Model-And-Motion-Formats/frp-object-container.md:4) while the others are DOCUMENTED.

(b) stale open claims
**MM.CS-4** "none reads the container's parts; what the parts are stays open" (Model-And-Motion-Formats/frp-object-container.md:149) vs "(Corrected 2026-09-30, SWE2-DATA: each entry type is now read from its readers on its own sheet …" (:59-61) and "(Closed for this sheet 2026-09-30 …)" (:304-306).

**MM.CS-5** Entry `+0x04`/`+0x0C` words: "no reader of them was found" (Model-And-Motion-Formats/frp-object-container.md:353) vs `00409190` "an offset chosen by bits 0-1 and 24-25 of dword +4" (Model-And-Motion-Formats/fef-and-motion-entries.md:990), "0041CD30 bounds the walk by dword[+0x0C]" (:247-248), "Bounds: idx < dword[entry+0x0C]" (Model-And-Motion-Formats/fte-fct-texture-colour-tables.md:122).

**MM.CS-6** "(that invoker is only partly read)" (Model-And-Motion-Formats/frp-object-container.md:368) vs "The invoker 00417F40 (1,717 B) read whole" (Authored-Commands/the-authored-presentation-command-handlers.md:765).

**MM.CS-7** "0040AA20 / 0040AAD0 | param setup | ◐ call shape" (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:356) vs 6b's reading of 0040AAD0's body: "stores direction and tilt in 02CA4391/02CA4392, then builds a unit vector from direction x pi/8 …" (:248-251).

(c) corrected claim still repeated unstruck
**MM.CS-8** "bits 0..11 unique per file in 1,057/1,066, unread by the binder and the four resolvers (a per-bone id, unproven)" left unstruck (Model-And-Motion-Formats/ftr-node-table.md:71-73) beside "[CORRECTED 2026-10-01, OPUS: bits 0..11 are not unread - 00409250 returns them as the record key when +0x04 bit 30 is clear …]" (:75-77).

**MM.CS-9** `@FMW` named a weight/blend record: "@FMW | 111 | 45 | motion weight/blend record" (Model-And-Motion-Formats/fef-and-motion-entries.md:79) and "@FMN/@FMW the 1:1 name/blend pair" (Model-And-Motion-Formats/README.md:45) vs "@FMW — the track-data record" (Model-And-Motion-Formats/fef-and-motion-entries.md:558) with channels "Euler XYZ rotation … translation XYZ … scale XYZ" (:664-666).

#### 3.3.11 [PP] Post-processing and visual tuning parameters

Short names in this part: **CS** = `Post-Processing/CONTRACT-post-processing-subsystem.md`; **CP** = `Post-Processing/CONTRACT-ppfx-effect-creation.md`; **PI** = `Post-Processing/ppfx-function-identification.md`; **CAT** = `Post-Processing/the-post-processing-effect-catalogue.md`; **VR** = `Visual-Tuning-Parameters/README.md`; **RR** = `Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md`; **RCL** = `Render-Command-List/the-ordered-render-command-list.md`; **HL** = `Post-Processing/members/ppfx-handle-layout.tsv`.


(a) banner / tag
**PP.CS-1. PI: README "DOCUMENTED … 147 … no body read yet" vs front matter AUDITED and body.** README.md:106-110 vs Post-Processing/ppfx-function-identification.md:4 `status: AUDITED`; Post-Processing/ppfx-function-identification.md:315 "147 is not 147 functions - it is 135 functions and 12 funclets"; Post-Processing/ppfx-function-identification.md:224-248 (H-6) reads three bodies.
**PP.CS-2. RR: README "15 `.phyre` shader assets" vs Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:89 "The count is 18".** README.md:129 vs Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:89/RR:824.
**PP.CS-3. CS/CP/CAT not in category README** (only PI listed under `Post-Processing/`, README.md:104-110) while Post-Processing/CONTRACT-post-processing-subsystem.md:6 claims `CONTRACT READY`.
**PP.CS-4. CS readiness READY vs scope note.** Post-Processing/CONTRACT-post-processing-subsystem.md:6 `CONTRACT READY` vs Post-Processing/CONTRACT-post-processing-subsystem.md:258-269 list of non-established items incl. which techniques run (UQ-227 PARTIAL); Post-Processing/CONTRACT-ppfx-effect-creation.md:29-37 keeps S-40 SCOPE-SHORT.

(b) stale open claims answered elsewhere
**PP.CS-5. "who fills `cfg`" open.** Post-Processing/the-post-processing-effect-catalogue.md:985 "who fills `cfg`, and in particular which float is the cutscene focus distance" vs Post-Processing/CONTRACT-post-processing-subsystem.md:263-265 "answered 2026-09-25 … `0018EEE0` allocates the `0xF0` block".
**PP.CS-6. Focus-distance float.** Post-Processing/the-post-processing-effect-catalogue.md:968-969 "Which `cfg` float carries the focus distance is not read here." and Post-Processing/CONTRACT-post-processing-subsystem.md:266 "and which float carries the cutscene focus distance" vs Post-Processing/CONTRACT-post-processing-subsystem.md:144 "| `+0x24` / `+0x28` | `+0x114` / `+0x118` | `mDofFocusDistance` / `mDofApertureFnumber` …".
**PP.CS-7. `006DB9A0` body.** Post-Processing/the-post-processing-effect-catalogue.md:972-973 "`006DB9A0`'s body is not read here" vs Post-Processing/CONTRACT-post-processing-subsystem.md:88-93 (2026-09-25) chain to `00707560` `SetGlareParameters`, stores at +0x6E4/+0x6E0/+0xC6C/+0xC70.
**PP.CS-8. Multiplier rests on four literals / five unread helpers.** Post-Processing/the-post-processing-effect-catalogue.md:853-855 and Post-Processing/the-post-processing-effect-catalogue.md:914-916 vs Post-Processing/the-post-processing-effect-catalogue.md:148 complete list (2026-09-29) and Post-Processing/the-post-processing-effect-catalogue.md:806 (helper bodies read 2026-09-18).
**PP.CS-9. PI "no PPFX function body has been read".** Post-Processing/ppfx-function-identification.md:131 "None. This document produces identity, not mechanism — no PPFX function body has been read." and Post-Processing/ppfx-function-identification.md:283-284 "that does not mean its body has been read" vs Post-Processing/ppfx-function-identification.md:168-182 (H-4 narrowed) and Post-Processing/ppfx-function-identification.md:240 "Every one of the three ends `mov eax, 0x80004001`".
**PP.CS-10. PI call chain "Not derived".** Post-Processing/ppfx-function-identification.md:142 vs Post-Processing/the-post-processing-effect-catalogue.md:918-947 and Post-Processing/CONTRACT-post-processing-subsystem.md:80-107.
**PP.CS-11. VR "Eleven genuinely open keys" incl. cascade `_2/_3` and `mCascadeNumber`.** Visual-Tuning-Parameters/README.md:39-46 "Absent from the binary and not tool-marked, so neither reading explains them" vs Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:346-351 (W-9 answered 2026-09-15: `_2`/`_3` read via `"mCascadePartition%d_%d"`; `mCascadeNumber` invariant 3).
**PP.CS-12. RR §4 W-1 label.** Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:284-285 "the arithmetic that consumes them has not been read. Recorded as **W-1**." vs Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:334 "W-1 ANSWERED in section 8b" (W-1 answered a different question).
**PP.CS-13. Contract §14.1 "fourteen helpers".** Post-Processing/CONTRACT-ppfx-effect-creation.md:237-238 "reading the fourteen helpers' bodies" vs Post-Processing/CONTRACT-ppfx-effect-creation.md:89-107 (pass 1: five are string utilities; registration is the vtable).

(c) corrected claims repeated unstruck
**PP.CS-14. "registration helper" rows.** Post-Processing/the-post-processing-effect-catalogue.md:121/123-134 header and Post-Processing/the-post-processing-effect-catalogue.md:174-179 ("registration helper, 91 call sites here") vs Post-Processing/the-post-processing-effect-catalogue.md:117 "CORRECTED 2026-09-18 … not registration helpers".
**PP.CS-15. "332 registrations, in seven shapes".** Post-Processing/the-post-processing-effect-catalogue.md:105 vs Post-Processing/the-post-processing-effect-catalogue.md:806 "section 2's *332 registrations in seven shapes* counted 219 string operations as registrations".
**PP.CS-16. §5 call chain old counts.** Post-Processing/the-post-processing-effect-catalogue.md:758-764 "00715C70 x88 … 007157A0 x45 … 00719380 x37 … ~323 handle registrations" vs Post-Processing/the-post-processing-effect-catalogue.md:888 "91 · 48 · 40" and Post-Processing/the-post-processing-effect-catalogue.md:899-900 "the registration total is 332, not "~323"".
**PP.CS-17. "24 real targets".** Post-Processing/the-post-processing-effect-catalogue.md:846-847 vs Post-Processing/the-post-processing-effect-catalogue.md:825 struck to "358 call sites to 22 real targets".
**PP.CS-18. PI "147 named functions" / "three collisions".** Post-Processing/ppfx-function-identification.md:155 "147 named functions is the entry point" vs Post-Processing/ppfx-function-identification.md:341 "147 − 12 = 135"; Post-Processing/ppfx-function-identification.md:613 "how the three collisions resolve" vs Post-Processing/ppfx-function-identification.md:607-609 "the collisions among NAMES are 7".
**PP.CS-19. RR asset directories.** Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:263 "observed: GraphicsAPI = D3D11 ; kind = shaders | font" vs Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:89-90 "three directories carry `.phyre` assets".
**PP.CS-20. CS §7 "library error" unqualified.** Post-Processing/CONTRACT-post-processing-subsystem.md:256 "Let a library error abort the frame. The game ignores it (I-5)." vs Post-Processing/CONTRACT-post-processing-subsystem.md:200 corrected heading "`ApplyEffects` failures do not reach the game; an initialisation failure before `007009BB` does."
**PP.CS-21. CP misreference.** Post-Processing/CONTRACT-ppfx-effect-creation.md:198 "no diagnostic is emitted on any path (I-4)" — gating is I-5 (Post-Processing/CONTRACT-ppfx-effect-creation.md:125).

#### 3.3.12 [CM] Scripted camera, screen fade, screen effects, aspect fit, position-to-scalar, movie index

Short names in this part: **MR** = `Movie-Containers/README.md`; **MH** = `Movie-Containers/mh-movie-seek-index.md`; **PTS** = `Position-To-Scalar/how-a-position-becomes-a-single-number.md`; **SF** = `Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md`; **AF** = `Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md`; **CI** = `Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md`; **CR** = `Scripted-Camera/how-a-camera-reaches-the-renderer.md`; **P** = `Scripted-Camera/the-scripted-camera-player.md`; **RM** = `README.md`; **WT** = `../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`.


(a) status vs banner vs README:
- **CM.CS-1 Screen fade.** `status: AUDITED` (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:4) vs README "**DOCUMENTED, tier 1 (2026-09-12).**" (README.md:38).
- **CM.CS-2 Scripted camera player.** `status: AUDITED` (Scripted-Camera/the-scripted-camera-player.md:4) vs README "**DOCUMENTED, tier 1 (2026-09-12).**" (README.md:31).
- **CM.CS-3 Aspect fit.** `status: DOCUMENTED — every register row is answered` (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:4) vs README "**PARTIAL, tier 1.** ... What that does on screen is **not** established." (README.md:25-30).
- **CM.CS-4 Cut-in "pending first review".** "note: written by FABLE; ... pending first review" (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:20) vs `last_pass_kind: falsification` 2026-09-29 (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:17-19) and "Falsification pass 1 — 2026-09-29 (OPUS)" (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:406).
- **CM.CS-5 Camera-renderer "pending first review".** (Scripted-Camera/how-a-camera-reaches-the-renderer.md:19-20) vs `last_pass_kind: falsification` (Scripted-Camera/how-a-camera-reaches-the-renderer.md:17) and "Falsification pass 1 — 2026-09-29 (OPUS)" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:494).

(b) stale open claims answered elsewhere:
- **CM.CS-6** "What each of them then does with that scalar is **not established here**" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:34-36) vs §13 "at every one of the 76 sites the node's output is a modulate" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:405).
- **CM.CS-7** "**The meaning of `mode`.** ... what selects them is the caller's, and no caller was read." (Position-To-Scalar/how-a-position-becomes-a-single-number.md:243-244) vs "**byte `+1` of the record is the distance mode**" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:188), and Position-To-Scalar/how-a-position-becomes-a-single-number.md:292-295.
- **CM.CS-8** "**Which axis lane 1 is, is not established here**" / "Not claimed. ... Which axis lane 1 is." (Position-To-Scalar/how-a-position-becomes-a-single-number.md:310, 331) vs "lane 1 is Y, the up axis" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:4; Position-To-Scalar/how-a-position-becomes-a-single-number.md:310 inline).
- **CM.CS-9** "*Whose position the stash holds is that page's open runtime item*" (Effect-File-Formats/an-effect-element-frame-by-frame.md:131) vs "added to the **eye** at `02AED5F0`" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:81-82).
- **CM.CS-10** "**What this does on screen is not established** ... this pass did not find them" (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:86-90) and "**what any of this looks like on screen** | **not established**" (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:182) vs "on-screen scaling cannot follow from them" (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:123-124).
- **CM.CS-11** "The per-helper bodies (`002DED60`, `00360D70`/`00360E50`, ...) ... their bodies are **not read**" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:177-179) vs "`00360D70` (82 B) sweeps ..." (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:482) and "`00360E50` (141 B) ..." (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:520).
- **CM.CS-12** "What the matrix at the head of the working block is (the extra factor in `02AEDD30` and `02AEDD70`)" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:333) vs "`00382910` builds the one at `02AED4A0` with ... **512 × 448**" viewport (Position-To-Scalar/how-a-position-becomes-a-single-number.md:233) and Scripted-Camera/how-a-camera-reaches-the-renderer.md:67 (head of block `02AED4A0`).
- **CM.CS-13** "`003CBD60` itself was not read" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:84) vs "(the page note 'itself was not read' is now read)" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:430).
- **CM.CS-14** "*Not read:* ... `002563F0`" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:286) vs "`002563F0` (185 B) is the camera state writer `0037D4C0` reads its two base scalars from" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:426).
- **CM.CS-15** "The rest of the `0xD0`-byte camera record" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:330-332) vs `003CC080`/`003CC000` writing `+0x90`, `+0xA0`, `+0xB0`, `+0xC0 = 2` kind tag, `+0xC4` (Scripted-Camera/the-scripted-camera-player.md:1039-1045) — partial answer.
- **CM.CS-16** "frame 1 copies into a separate view at `02097B80` (`0025A3D0`; what consumes it was not traced)" (Scripted-Camera/the-scripted-camera-player.md:285-286) vs `00259970` submits "the static default view `02097B80`" at priority `0x14` before the second draw (Scripted-Camera/how-a-camera-reaches-the-renderer.md:55).
- **CM.CS-17** "The shake channels at `ActorManagerSlot +0x170` share this layout ...; their tick is not read here." (Scripted-Camera/the-scripted-camera-player.md:477-478) vs the same page's added note (Scripted-Camera/the-scripted-camera-player.md:116-118) and Scripted-Camera/how-a-camera-reaches-the-renderer.md:205-215.
- **CM.CS-18** "What BY-7 still owes: the *meaning* of the resolved record's `+0x194`/`+0x198` fields" (Scripted-Camera/the-scripted-camera-player.md:930) vs "**ANSWERED 2026-09-26** ... `+0x194` / `+0x198` are two of the three angles of the bone's added rotation" (Scripted-Camera/the-scripted-camera-player.md:590-592).
- **CM.CS-19** "Not read: `00255850` (961 B) and `00257520` (731 B) beyond their calls into record 5" (Scripted-Camera/the-scripted-camera-player.md:39-40; also Scripted-Camera/the-scripted-camera-player.md:286) vs BY-9 "**ANSWERED 2026-09-14**" (Scripted-Camera/the-scripted-camera-player.md:622-646).
- **CM.CS-20** "`003820C0` (2,125 B, one caller; **not read whole**" (Character-Render-Records/how-a-character-fades-the-ten-channels.md:334) vs "*Read instruction by instruction on 2026-09-19*" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:75).
- **CM.CS-21** "The two constant kind-28 lookups were **not** re-derived here" (Movie-Containers/mh-movie-seek-index.md:195-196) vs SF re-derives `001B7F30` (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:644-650, 2026-09-25).

(c) corrected claims still repeated unstruck:
- **CM.CS-22** "steps the table with `0037D970`" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:150-151), "*Still not read:* the table step" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:318), "base scalars; table step" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:349) vs "**`0037D970` is not a "table step"**" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:160) — struck only at Scripted-Camera/how-a-camera-reaches-the-renderer.md:286.
- **CM.CS-23** "The layer verbs pop two integers and tail-jump into `002EFA70`" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:95) vs "§2.3's sentence ... describes `00D0`–`00D2`, not `00B6`–`00B8`" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:403-404).
- **CM.CS-24** "the draw-side family `0045E930`–`00537410` and `004427D0`" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:212) vs "the lowest is **`00442550`** ... its stated bounds are not" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:326-328).
- **CM.CS-25** "the singleton" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:142, 174, 184, 201) vs "Section 10 called `[02F97348]` *the singleton*. It is not one object." (Position-To-Scalar/how-a-position-becomes-a-single-number.md:336).
- **CM.CS-26** "calls scheduling helpers `00229D20` and `00229D60`" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:421) vs "`00229D20` (33 B) is the ~~speed-mode factor~~ **aspect ratio of section 3 (corrected 2026-09-29 ... `CON-184`" (Scripted-Camera/how-a-camera-reaches-the-renderer.md:490).

## 4. Rating

**Overall: NOT YET.** Most sub-parts could be written from the pages with named gaps, but the category has structural
gaps that no page fills: the frame order across the category (X.G-1), the D3D11 device interface (X.G-2), the execute
bodies of the render command classes (X.G-3), the VU1 microprograms (X.G-4), the shared track evaluators (X.G-5), and
`@FRM` motion data and the movie path (X.G-7). On top of these, 160 value-changing contradictions have no favoured side
on the pages (§3.1) and must be settled at the bytes before a port can rely on the affected values.

Sub-part ratings: **3 READY, 53 MOSTLY, 15 NOT YET** (71 rows).

| part | sub-part | rating | why |
|---|---|---|---|
| AC | Ramp channels (V1 table: set, tick, alloc) | **MOSTLY** | Setter, tick and alloc are exact and differentially tested (`CONTRACT-authored-command-ramp-channels.md:6`). Open: the slot's initial values and the allocator's writes (AC.G-8, AC.CV-9, page vs TSV), whether `003B5C00` steps `+0x43` (AC.CV-3), the command layout (AC.CV-2), the `+0x41` / `003B6900` writers (AC.G-4), gate-driver arguments (AC.G-3, AC.CV-1). On PC the channels drive nothing visible (`CONTRACT-authored-command-ramp-channels.md:161`). |
| AC | Shadow draw pass and V2 pool | **NOT YET** | The `0xA0` output goes to a PS2 ring the PC never reads (`CONTRACT-authored-command-ramp-channels.md:161`, `:612-621`). V2 values have no reader (AC.S-5, AC.S-7); the defaults conflict (AC.CV-12). |
| AC | Authored-command dispatch (drains, invokers, banks) | **MOSTLY** | Two-table route and the 25 registrations are instruction-exact. Open: frame placement (AC.G-6), out-of-range ids (AC.G-7, RA.CV-12), flag semantics (AC.G-10); role conflicts AC.CV-10, AC.CV-11; stale "deferred" framing (AC.CS-11). |
| AC | Per-command handlers | **MOSTLY** | Most ids have read bodies and censuses. Open: 0x12, 0x19, 0x1E, 0x1F, 0x23 (AC.G-9); the `0x3F` row is superseded (AC.CV-4, favoured GI-15); pool address (AC.CV-5). |
| AC | Coast-down latch | **MOSTLY** | Executed 70/70. Open: the §12 formula omits the §7a tail (AC.G-11); time base (AC.CV-6); arming semantics vs the record page (AC.CV-8); initial values (AC.G-13). AC.CV-7 is settled (2026-09-22). |
| RO | Render-record pool lifecycle | **MOSTLY** | Lists, cursor, promote/retire/release and tail cells are concrete. Open: record initialiser and scripted callees, live-bit setter, tail `+0x30`, frame scheduling (RO.G-1 to RO.G-7); RO.CV-2, RO.CV-10 to RO.CV-13, RO.CV-16. RO.CV-1 names the wrong consumer contract. |
| RO | Character render object | **NOT YET** | Life cycle and slot order are stated, but the draw is not: `001F5D70`, setup slot 2 and slots 19/24/26/30 are named roles only (RO.G-9, RO.G-10). Many fields have no meaning (RO.G-11). Initial state is self-contradictory (RO.CV-9); layout overlap (RO.CV-15); wrong product (RO.CV-3). |
| RO | Character transform publish | **MOSTLY** | Body fully specified and differentially tested (`CONTRACT-character-transform-publish.md:197`). Missing: what slot 16 passes (RO.G-13). The bank selector conflicts (RO.CV-4, RO.CV-5, RO.CV-7); RO.CV-6 changes the uploader's slot count. |
| RO | How a character is lit | **MOSTLY** | Selector, ambient, five kind evaluators, create routine. Missing: typed-handle predicates, ordering routines and the six-light cut (RO.G-18), light-pool details (RO.G-17), writers of the record lighting fields (RO.G-19). One conflict: RO.CV-17. |
| RA | Record pool, lists and lifecycle (record-array page) | **MOSTLY** | Layout, lists, allocator, removers, promoter, defaults. Open: RA.CV-1 (tail `+0x30`), RA.CV-4 (`+6/+8/+0xA`), RA.CV-13; unresolved tail fields (§2.1.3). |
| RA | Dirty-state protocol | **NOT YET** | The bit census and order exist (`members/dirty-bits.tsv`), but the handlers are leaf-call sketches (§2.2.3), the pass lists conflict with the TSV (RA.CV-9), and some bits have no setter (§2.1.3). |
| RA | Coast-down seam | **READY** | Formulas and constants are complete; only the time-base value must be checked (RA.CV-10). |
| RA | Shadow sync | **MOSTLY** | RA.CV-2 (pool shape), RA.CV-3 (`+0x114`); LOD clamp low bound not stated (§2.2.3). |
| RA | Event selection and entry container | **MOSTLY** | Lookup, ids, admission, release and priority table are exact. Open: RA.CV-8, RA.CV-12; helper effects (§2.1.3). |
| RA | Focus point | **MOSTLY** | The per-frame formula is given. Open: 60 fps nibble overflow (RA.G-1), initial values (RA.G-12), RA.CV-5, RA.CV-10. |
| RA | Track selection | **MOSTLY** | Setup, reset, finder and switch commands exact. Open: RA.CV-7, RA.CV-11; stale RA.CS-5, RA.CS-6. |
| RA | Frame stages (draw) | **NOT YET** | The stage bodies are unread (§2.1.3, RA.G-2). |
| RG | Fade channels | **MOSTLY** | Layout, owners, selectors, cull, clip-verb data. But the immediate setter and the stepper each have two descriptions on the same page (RG.CV-1, RG.CV-2); the opacity formula has an unexplained factor (RG.CV-3). |
| RG | Status looks | **MOSTLY** | Colour list and second block read with constants. Open: curve tables, variant blocks, the 9.7 KB draw, `00428AF0` field (RG.CV-8, RG.G-17). |
| RG | Bone trails | **MOSTLY** | CPU side complete. The vertex program is unread (RG.S-20); the release routine's pool addresses and the template UNPACK size conflict (RG.CV-6, RG.CV-7). |
| RG | Rig of seventeen controllers | **NOT YET** | Switching is documented, but almost no controller's per-frame computation (lip flap, nod, head shake, Confuse, Immobilize, body shake, controllers 5 and 8) is read (§2.1.4). |
| RG | Staged look | **MOSTLY** | Staging, request word, fan-out, dispatcher. The look controller's per-frame behaviour is unread (`Character-Render-Records/the-staged-look-command.md:212`); RG.CV-10, RG.CV-11. |
| CL | Ordered list machinery | **MOSTLY** | Instruction-cited layouts, invariants and pseudocode. Settle first: CL.CV-3 (four appenders skip the owning list), CL.CV-5 (grow path reached; favoured), CL.CV-10 (base vtable slots). Holes: CL.G-3, CL.G-4, CL.G-9, CL.G-10. |
| CL | Command classes (payload and execute) | **NOT YET** | 8 of 36 execute bodies; sizes for 19 builders (CL.G-1, CL.G-2, CL.G-13). Unstruck sort-key text (CL.CV-1, CL.CV-7, both favoured by dated corrections). |
| CL | Frame ordering inside the render pass | **MOSTLY** | Render-pass and teardown order explicit. Not stated: class-filtered walk timing, split/mark timing, gate `01FD4A88`, the handshake's place (CL.G-4, CL.G-6, CL.G-8, CL.G-15). |
| CL | Graphics handshake word | **MOSTLY** | Masks, values, publishers and spin are exact; mask arithmetic checks. Gaps: staging-buffer consumer (§2.1.5), reset entry (CL.G-11); role drift CL.CV-13, CL.CV-14. |
| GP | Gi command objects (factories, arena, node, prepare) | **MOSTLY** | Factory shape, ring allocator and node promotion at instruction level. Missing: per-class layouts (GP.G-1), arena reset (GP.S-1, GP.CV-7). Conflicts: GP.CV-3, GP.CV-10. |
| GP | Submission and execution path | **MOSTLY** | Chain named through the `0x2F` arm. Missing: frame placement (GP.G-7) and record flag bits (GP.G-4). GP.CV-4, GP.CV-5, GP.CV-6, GP.CV-17 are settled by dated sections, but the unstruck text (GP.CS-12 to GP.CS-14) makes the page unsafe to read front to back. |
| GP | Device interface (`PrimitiveRendererD3D11`) | **NOT YET** | Identity and slot addresses only (GP.G-2); the call set per command is disputed (GP.CV-1). |
| GP | VIF1 interpreter and VU machine state | **MOSTLY** | Command semantics, UNPACK grid, MSCAL selection. Missing: TOPS (GP.G-10), initial state. GP.CV-12 settled. |
| GP | VU1 microprograms | **NOT YET** | 57 recompiled bodies characterised by primitive only (GP.G-9). |
| GP | GS replay / translator | **MOSTLY** | Tag walking, sizing, vertex conversion and index generation to bit level. Missing: replay state calls (GP.G-11), handler-to-D3D mapping (GP.G-12). GP.CV-11 settled (`Legacy-PS2-GS/the-vif1-vu1-layer.md:843`). |
| GP | GS texture-mip budget | **MOSTLY** | Algorithm and constants complete. Missing: descriptor layout (GP.G-13), walk order (GP.G-16), slot record (GP.G-14). GP.CV-15 (not a fixed 176 pages) is favoured. |
| EF | Element update (base, nine tails, cull, release, spawn) | **MOSTLY** | Survives a falsification pass. Gaps: spawner (EF.G-4), track format (EF.G-6), age at birth (EF.G-1), `002F31C0` below `0x40` (EF.G-2). Conflicts: EF.CV-1, EF.CV-2, EF.CV-5, EF.CV-10, EF.CV-14 to EF.CV-16. |
| EF | Dispatch tables, birth and setup | **MOSTLY** | A 210-row TSV reproduces the tables, but the prose disagrees with it on sharing and setup labels (EF.CV-7, EF.CV-11, EF.CV-12), and the step is still called per-frame (EF.CV-4, EF.CS-12). |
| EF | Walk and draw list | **MOSTLY** | Append, sort key, arena, drain, rewind. Open: EF.CV-6, EF.CV-8 (favoured), EF.CV-9, EF.CV-13; update vs walk order (EF.G-19). |
| EF | EFX / EFB containers | **MOSTLY** | Header, chunk grammar, binders and EFB rows are corpus-checked. Open: EF.CV-17, EF.CV-18; the `0xB00` route (§2.2.7); stale header text (EF.CV-19, EF.CV-20, both favoured). |
| ET | Kind-0x54 mesh records | **MOSTLY** | Layout and size formula reproduce on all 2,252 records. Open: index lists, kind-0x52 link, pass operators (ET.G-1 to ET.G-5); ET.CV-7. |
| ET | Element types 0x00-0x0A | **MOSTLY** | Setups, tails, point/line/sprite/grid emits. Missing: track evaluators (ET.G-7); `0039B620` meaning conflicts (ET.CV-4). |
| ET | Element types 0x40-0x42, 0xAB, 0xD0, 0xD1 | **MOSTLY** | Well described (GI-9). |
| ET | Element types 0xA1-0xAA | **NOT YET** | Addresses only; 0xA2 alone has 6,303 authored chunks (ET.G-9). |
| ET | Element types 0x60-0x74 | **MOSTLY** | Tails, cores and VU1 programs named; most per-type geometry missing (ET.G-11); record ranges do not add up (ET.CV-5, ET.CV-6); PRNG order (ET.CV-1). |
| ET | Element types 0x80-0x97 | **MOSTLY** | Tail groups clear. Open: ET.CV-2, ET.CV-3; vertex layouts (ET.G-10). |
| ET | Menu effect registry | **MOSTLY** | Table, API, ids and the `+0x338` path. Banner stale (ET.CS-1); instance creation off-page (ET.G-16); ET.CV-4. |
| ET | Six VFX display layers | **MOSTLY** | Survived falsification. Unread: layer 3's routine, kind 4/5/6/9 lookups, enable-word writers (ET.G-14, ET.G-15, ET.G-19). |
| MF | Skeleton mapping / high-model replace | **MOSTLY** | Both layouts, loaders and the bind route; sizes check (196 B, 540 B). Missing: `003703A0` joint-follow math, `0037B4D0` body; MF.CV-6. |
| MF | `.adm` add-motion | **MOSTLY** | File, parse, kind 0/1, degree scale. Missing: kind-0 parameter source (MF.G-2), Euler convention (MF.G-4); MF.CV-4 (favoured), MF.CV-5 (the README's magic rejects 4 files). |
| MF | `@FCP` character parameter block | **MOSTLY** | Getter decode, scaling, the tunable table, sections and event map. The §3 table disagrees with §6.1 (MF.CV-1, MF.CV-2, favoured §6.1 by UQ-219); the integer default table is absent (§2.2.9). |
| MF | `@FDM` / `@FOR` | **MOSTLY** (data and binding; the draw is NOT YET under X.G-4) | Layout conflicts MF.CV-7 to MF.CV-10; the VU1 draw is unread (MF.S-11). |
| MM | `@FRP` container | **READY** | Loader instruction-read and corpus-checked; MM.CV-1, MM.CV-2 favoured by the 2026-09-30 correction. Only MM.G-1 and stale text remain. |
| MM | `@FEF` | **READY** | Embedded payload proven dead; the live companion path is read. MM.S-1, MM.S-2 are runtime or visual only. |
| MM | `@FMC` event bytecode | **MOSTLY** | Grammar and 33 handlers mapped. Operand conflicts MM.CV-7 to MM.CV-10; frame advance, state-row layout, selector kinds missing (MM.G-4 to MM.G-6). |
| MM | `@FMN` / `@FMW` sampling and bone apply | **MOSTLY** | Codecs and channel map given. MM.CV-3, MM.CV-11 to MM.CV-14 conflict; MM.G-7, MM.G-8. |
| MM | `@FRM` | **NOT YET** | Bound and handed on, never decoded (MM.G-3). |
| MM | `@FTE` / `@FCT` | **MOSTLY** | Layouts and consumers read; MM.CV-4 to MM.CV-6 (header `+0x0C`, CLUT stride). |
| MM | `@FTR` | **MOSTLY** | Layout, sizer, flags, consumers; MM.G-2, MM.G-8. MF.CV-9 (`+0x38` width). |
| MM | Per-model oscillator | **NOT YET** | VU stages call-shape only (MM.S-8, MM.G-11, MM.G-13); MM.CV-15 to MM.CV-22 disagree on mode polarity, record size, flag holder, install chain and tick. |
| MM | Pose sequencer | **MOSTLY** | Format, start/step/value read and falsified. Missing: random picker (MM.G-15), copy descriptor (MM.S-13), initial slot state (MM.G-14); MM.CV-7. |
| PP | Frame-side post-processing subsystem | **MOSTLY** | Order, gating, route and options stated. Open: step 7 lens and floats (PP.CV-1, PP.CV-2), step 3 block size (PP.CV-3), steps 1/3/4/6 (PP.G-3, PP.G-4). The library is declared substitutable (`Post-Processing/CONTRACT-post-processing-subsystem.md:238-245`). |
| PP | Library initialisation | **MOSTLY** | Constant `0x20001` and its consequences; the default block is not laid out (PP.G-2). |
| PP | Effect creation and catalogue | **NOT YET** (byte-faithful); MOSTLY if the library is substituted | Name list complete, but handle naming (PP.CV-5), receiver type and size (PP.CV-6, PP.CV-7) and the suffix table (PP.G-12) are not settled. PP.CV-4 favoured (lazy build). |
| PP | PPFX function identification | **NOT YET** | Identity only, no behaviour (README: "Identity only; no body read yet.", `README.md:110`); PP.CC-3, PP.CC-4. |
| PP | Visual tuning parameters / JSON loading | **MOSTLY** | Locations, fallback order, readers, cascade layout. No parameter arithmetic; PP.CV-8; PP.CV-11 and PP.CV-12 favoured; many counts disagree (PP.CC-6 to PP.CC-13). |
| CM | Movie containers (`.webm`, `.mh`) | **NOT YET** | `.mh` laid out but inert; the WebM playback path has only its path build (CM.G-1, CM.S-1); CM.CV-19, CM.CV-20. |
| CM | Position to scalar (distance fade) | **MOSTLY** | Switch, modes, alpha formula, consumer census. Missing: kind-3 timed fade (CM.G-5), modifier order (CM.G-6), `02AEEA20` (CM.G-7); CM.CV-12, CM.CV-13. |
| CM | Screen fade | **MOSTLY** | Starter, poll, verbs, schedule, pool. Byte-level conflicts to settle first: CM.CV-1 to CM.CV-11. Open: kind/wait word consumers and pool tick (CM.G-10 to CM.G-12). |
| CM | Screen mode / aspect fit | **MOSTLY** | Fit arithmetic, readers, DXGI table. Missing: initial state and trigger (CM.G-15, CM.G-16); CM.CV-18, CM.CV-21. |
| CM | Script screen effects | **MOSTLY** | Staging, play, clear, per-frame logic complete. What queued kinds 2/5/6/7/0x0D draw is unknown (§2.1.12); helpers by role only (CM.G-17); CM.CV-23. |
| CM | Camera to renderer | **MOSTLY** | Arbitration and shake sampler precise. Missing: rebuild math, override source (§2.1.12); CM.CV-17, CM.CV-22. |
| CM | Scripted camera player (CAM7) | **MOSTLY**, close to READY | Grammar, layouts, timing, paths, kinds and attachments corpus-validated. Settle CM.CV-14, CM.CV-15, CM.CV-16. |
| — | Frame order across the category | **NOT YET** | X.G-1. |

**To reach MOSTLY overall**, the database would need:
- one statement of the category's frame order (X.G-1);
- the D3D11 device slot semantics and the per-command call sets (X.G-2, GP.CV-1);
- execute bodies and sizes for the remaining render command classes (X.G-3);
- the shared track-record format and evaluators (X.G-5);
- a local check of the cross-part value conflicts (the pool base, `01DFE0B4`, `+0x114`, `+6/+8/+0xA`, `02EBEF88`; see the table at the head of §3) and of the two primitives on the fades page (RG.CV-1, RG.CV-2);
- the rig controllers' per-frame computations (§2.1.4) and the character render object's draw (RO.G-9, RO.G-10).

## Appendix A. Per-part page status quotes and `.tsv` checks

Each table is the reading agent's record for its pages: the front-matter status, the body banner and the README tag, quoted with lines, then every `.tsv` opened to confirm a layout or a count.

### A.1 [AC] Authored commands, ramp channels and the coast-down latch

| path | lines | front-matter status/readiness (line) | body banner (line) | README tag (line) |
|---|---|---|---|---|
| README.md | 145 | none (category index) | "**Engine category.**" (3); table "Functions \| 1,564" (8) | n/a |
| CONTRACT-authored-command-ramp-channels.md | 1041 | "readiness: DIFFERENTIAL TESTED # diff_ramp_channels.py, 483 commands / 129 compared lines / 0 mismatches, mutants killed (SWE2-CONTRACT, 2026-09-13, a27b5cc5)" (:6); "confidence: PROVEN" (:7); "crossref_clean: false" (:22) | "**Two of the five setters are not in the function census**" (:28). Note: it says "five setters", but §2 has four setters | "**SPECIFIED, tier 1, not differentially tested.**" (README.md:19) |
| Authored-Commands/the-authored-presentation-command-handlers.md | 1141 | "status: \"DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS; documented_rule READY): GI-15 answered 2026-10-01 …" (:4). The YAML string opens with `"` and is not closed on :4; "last_reviewed: 2026-09-17" (:12) | none. Opening line: "**Twenty-eight bodies at `00520010`–`00520E90`, 3,695 bytes, one family:**" (:23) | "**PARTIAL, tier 1.** The **28-body `00520xxx` family**" (README.md:14) |
| CONTRACT-coast-down-latch.md | 584 | "readiness: DIFFERENTIAL TESTED   # the latch; its tail's two callees are supplied as oracles — see §13" (:6); "confidence: PROVEN" (:7); "last_reviewed: 2026-09-11" (:17) | "⚠ The invariant is false, and the branch targets say so" (:85); "Verdict `FAIL`." (:401) | not listed |

TSV checks:

| file | what I counted | result | page claim it confirms or contradicts |
|---|---|---|---|
| ramp-channel-record-accesses.tsv | `wc -l`; `awk` unique `function` column | 77 lines (76 rows) in 4 functions: 003B56D0 ×39, 003B5890 ×33, 003B6020 ×3, 003B6890 ×1 | The TSV covers 4 bodies, while the page has "all 21 `02B40528`-referencing bodies read" (CONTRACT-authored-command-ramp-channels.md:498). The TSV is narrower, but this is not a contradiction |
| same | `awk` disp+kind for 003B5890 | reads/writes counters 0x0–0x3 and 0x43; values 0x50/54/58/5C/70/78/98 r+w; deltas 0x60–0x7C and 0x9C read only | confirms §3 five-channel tick (CONTRACT-authored-command-ramp-channels.md:103-109) and the channel table (:72-79) |
| same | `awk` disp+kind for 003B56D0 | writes include `0x30` (`003B584C mov qword ptr [rbx + 0x30], rsi`), `0xBC` (qword), `0xC4`, `0xC8`, `0xCC`, `0xD4` (`003B5877 mov dword ptr [rbx + 0xd4], 0x3f800000`), `0x9C`, and `0x1C` (qword, tagged "zeroclear") | **contradicts** :466-468 ("`003B56D0` … touch no `+0x30`/`+0x34` either. One writer (`003B5CE0`), zero readers") and :473-474 ("not even the allocator (whose init sweep ends at `+0x9C`"). Confirms :469-471 (the `+0x1C` qword zero store). See AC.CV-9 |
| same | `awk` 003B6020 | reads `+0x10`, `+0x40`, `+0x41` | confirms the EXP-108 gate (:579-585) |

### A.2 [RO] Render-record pool, character render object, transform publish and lighting

Short names in this part: **POOL** = `CONTRACT-render-record-pool-lifecycle.md`; **CRO-C** = `CONTRACT-character-render-object.md`; **PUB** = `CONTRACT-character-transform-publish.md`; **CRO** = `Character-Rendering/character-render-object.md`; **LIT** = `Character-Rendering/how-a-character-is-lit.md`.


| page | lines | front matter status/readiness | body banner | README tag |
|---|---:|---|---|---|
| POOL | 1472 | `readiness: BEHAVIORALLY UNDERSTOOD` (:6); `confidence: PROVEN` (:7) | none at the top. §13 has "Executed 2026-09-12 as the twenty-seventh differential pilot … Evidence class: isolated original-code" (:372-373) | not listed (README has no row for it; only `CONTRACT-authored-command-ramp-channels.md` appears, README.md:18) |
| CRO-C | 249 | `readiness: CONTRACT READY` (:6); `confidence: PROVEN` (:7) | "Authored 2026-09-22 by FABLE." (:30) | not listed |
| PUB | 572 | `readiness: BEHAVIORALLY UNDERSTOOD` (:6) | "⚠ §2 and §3 describe the second half of this function … CORRECTED 2026-09-12" (:49-51) | not listed |
| CRO | 1267 | `status: AUDITED` (:4); `audit: passes: 3` (:20) | none. §8b ends "Status unchanged at `DOCUMENTED`." (:572) | README.md:98-101: "**DOCUMENTED, tier 1.** The **1,640-byte object that draws a character** … a **ready flag at `+0x4B4`** with one writer at the end of setup and twelve readers at method entry." |
| LIT | 398 | `status: DOCUMENTED` (:4); audit note "pending first review" (:22) | none | README.md:59-63: "**DOCUMENTED, tier 1 (2026-09-19), static.** Lights are chosen **per character** …" |

TSV checks:

| file | what I counted | result | claim it confirms or contradicts |
|---|---|---|---|
| `Character-Rendering/character-render-object-accesses.tsv` | data rows (`grep -v '^#'`, minus the header); distinct `function` (col 1); distinct `disp` (col 4) | **323 rows, 41 functions, 91 offsets** | contradicts Character-Rendering/character-render-object.md:517-518 "The census is now 160 rows in 31 functions over 69 distinct offsets" (RO.CC-1) |
| same | rows with disp `0x4b4`, by function and kind | 1 write (001F4DA0 @001F4EC9); 15 read rows in 14 functions, but 001FA1A0 @001FA1C9 is listed twice, so 14 distinct read sites: 13 vtable bodies plus 001F89E0. Slot 2's write @001F7729 is not in the TSV | confirms Character-Rendering/character-render-object.md:71-73 (13 vtable reads) and CONTRACT-character-render-object.md:85-88 (constructor clear @001F4EC9). The duplicate row is a TSV defect. The missing slot-2 write is a seed/taint limit (r8-based store) |
| `Character-Rendering/shader-binding-record-0x318-slots.tsv` | data rows with an offset in col 1; `(unstored)` rows | **92 stored + 6 unstored = 98** | confirms Character-Rendering/character-render-object.md:462 "98 times and stores 92" and Character-Rendering/character-render-object.md:831-832 |
| same | the `index` column (0..92) scanned for holes | **index 65 (offset `0x238`) has no row** | the binding slot at record `+0x238` has no name (RO.G-12) |
| same | rows at 0x0E0/0x0E8/0x0F0/0x0F8/0x100/0x108/0x110 | PS2ZBiasEnabled, PS2ZBiasNoGS, PS2ZBiasOriginal, PS2ZBiasInstance, PS2WHMatrix, PS2HSMatrix, **InvPS2WHSMatrix** | confirms Character-Rendering/character-render-object.md:813-817. Contradicts CONTRACT-character-transform-publish.md:334-335, which says the banks go "into the last two" of a run ending at `+0x108` (RO.CV-6) |
| same | rows at 0x088..0x0B0 | lichtColor5, lichtColor6, lichtAmbient, AlphaThreshold, PS2FogVec, clutBank | confirms CONTRACT-character-transform-publish.md:329-331 |

### A.3 [RA] The character render record array, render events, focus point and track pick

Short names in this part: **CRR** = `Character-Render-Records/the-character-render-record-array.md`; **RES** = `Character-Render-Records/render-event-selection-evidence.md`; **FOC** = `Character-Render-Records/the-focus-point-of-a-character.md`; **TRK** = `Character-Render-Records/how-a-presentation-entry-picks-its-track.md`.


| page | lines | front-matter status | body banner | README tag |
|---|---|---|---|---|
| CRR | 1118 (`wc -l`; 1119 with unterminated last line) | Character-Render-Records/the-character-render-record-array.md:4 "status: DOCUMENTED — every register row is closed or dispositioned and the page's residue is answered (owner re-status 2026-09-30, OPUS…)"; also `crossref_clean: false` (Character-Render-Records/the-character-render-record-array.md:27), `last_reviewed: 2026-09-02` (Character-Render-Records/the-character-render-record-array.md:18) | none (no banner block) | not listed (grep of README.md for the file name and "render record" finds nothing) |
| RES | 639 | Character-Render-Records/render-event-selection-evidence.md:4 "status: DOCUMENTED — UQ-192 is NOT A QUESTION … and UQ-193, UQ-194 and UQ-195 are ANSWERED; every box is closed…" | none | not listed |
| FOC | 179 | Character-Render-Records/the-focus-point-of-a-character.md:4 "status: DOCUMENTED"; audit note Character-Render-Records/the-focus-point-of-a-character.md:18-19 "…was uncited and unresolved); pending first review" | none | no own entry; linked only inside the rig-of-seventeen-controllers entry, README.md:47-53 ("**DOCUMENTED, tier 1 (2026-09-19), static.**" at README.md:48 belongs to the rig page; FOC linked at README.md:53) |
| TRK | 206 | Character-Render-Records/how-a-presentation-entry-picks-its-track.md:4 "status: DOCUMENTED"; audit note Character-Render-Records/how-a-presentation-entry-picks-its-track.md:21 "…is not on this page and is named as not read; pending first review" | none | README.md:81-82 "**DOCUMENTED, tier 1 (2026-09-19), static.**" |

TSV checks:

| file | what counted | result | claim |
|---|---|---|---|
| `Character-Render-Records/members/dirty-bits.tsv` | `wc -l` and rows per pass (awk over cols pass/word/bit) | 58 lines = header + 57 rows: pass1 13, pass2 4, pass3 26, pass4 11, pass5 2, "all" 1 (56 blocks + 1 chain row) | confirms block counts Character-Render-Records/the-character-render-record-array.md:742-747 (13/4/26/11/2) |
| same | bit lists per pass | pass1 = +0x290 {2,3,12,**18**,19,20,22,23,24,25,29,30} + +0x294:26; pass3 = +0x290 {9,26,28,31} (**no 27**) + +0x294 22 bits; +0x290:27 only in pass 4 | contradicts the prose lists Character-Render-Records/the-character-render-record-array.md:742 (omits bit 18) and Character-Render-Records/the-character-render-record-array.md:744 (adds bit 27 to pass 3) — see RA.CV-9 |
| same | `clear_kind` column | processor 40, handler 11, inline 2, consume 2, none 1, n/a 1 | confirms Character-Render-Records/the-character-render-record-array.md:726-729 (40/11/2/2); the remaining "none" row is pass-5 bit 20 re-dispatch, the "n/a" row the +0x294:25 chain row |

### A.4 [RG] Rig controllers, fades, status looks, bone trails and the staged look

Short names in this part: **FADE** = `Character-Render-Records/how-a-character-fades-the-ten-channels.md`; **STAT** = `Character-Render-Records/how-a-status-shows-on-a-character.md`; **TRAIL** = `Character-Render-Records/the-bone-trails.md`; **RIG** = `Character-Render-Records/the-rig-of-seventeen-controllers.md`; **LOOK** = `Character-Render-Records/the-staged-look-command.md`.


| page | lines | front matter status | body banner | README tag |
|---|---:|---|---|---|
| FADE | 846 | `status: DOCUMENTED` (:4); audit note "pending first review" (:21-22) | none; dated corrections inline (:113, :144, :260) | not listed as its own entry; named only under the rig entry ("Beside it: ... how a character fades", README.md:52), under "**DOCUMENTED, tier 1 (2026-09-19), static.**" (README.md:48) |
| STAT | 612 | `status: AUDITED` (:4); note "promoted DOCUMENTED -> AUDITED 2026-09-30" (:23) | none | "**DOCUMENTED, tier 1 (2026-09-19), static.**" (README.md:55) |
| TRAIL | 502 | `status: DOCUMENTED` (:4); note "Pending first review" (:31) | none | "**DOCUMENTED, tier 1.**" (README.md:74) |
| RIG | 546 | `status: DOCUMENTED` (:4); note "pending first review" (:22) | none | "**DOCUMENTED, tier 1 (2026-09-19), static.**" (README.md:48) |
| LOOK | 483 | `status: AUDITED` (:4); note "promoted DOCUMENTED -> AUDITED 2026-09-29" (:21) | none | not listed as its own entry; named only under the rig entry (README.md:51) |

No page has a `readiness:` field.

.tsv checks (files under `Character-Render-Records/members/`):

| file | what counted | result | page claim |
|---|---|---|---|
| fade-channel-census.tsv | header comments + `operation` rows | `# start_ramp sites 11`, `# set_immediate sites 3`, `# evaluate sites 8`; 22 data rows (8 evaluate, 3 set_immediate, 11 start_ramp) | confirms Character-Render-Records/how-a-character-fades-the-ten-channels.md:80 "11 ramp starts, 3 immediate sets, 8 evaluations" and Character-Render-Records/how-a-character-fades-the-ten-channels.md:13 "22 = 22"; the census holds no 00428940 / 004293C0 sites, as the erratum Character-Render-Records/how-a-character-fades-the-ten-channels.md:114-123 says |
| look-command-census.tsv | data rows (awk, skipping `#` and header) | 18 rows; header `# forwarders found 18 (control: 18)` | confirms Character-Render-Records/the-staged-look-command.md:43 "Eighteen record-level forwarders" and Character-Render-Records/the-staged-look-command.md:228 |
| rig-verbs-census.tsv | header + verb/argument rows | `# call sites by substring 55891; by parsed call 55891`; lip flap 28035 calls/354 scripts (0: 13834, 1: 14201); nod 26389/347 (0: 13093, 1: 13296); timed lip flap durations 150 x65, 210 x23, 90 x17 | confirms Character-Render-Records/the-rig-of-seventeen-controllers.md:39, Character-Render-Records/the-rig-of-seventeen-controllers.md:43-48, Character-Render-Records/the-rig-of-seventeen-controllers.md:51 "about fourteen thousand times each way", Character-Render-Records/the-rig-of-seventeen-controllers.md:52 "150, 210 and 90 frames" |

### A.5 [CL] Ordered render command list and graphics-thread handshake

Short names in this part: **C** = `CONTRACT-render-command-list-and-graphics-handshake.md`; **L** = `Render-Command-List/the-ordered-render-command-list.md`; **H** = `Graphics-Thread-Handshake/the-shared-command-state-word.md`.


| path | lines | front-matter status/readiness | body status banner | README tag |
|---|---|---|---|---|
| CONTRACT-render-command-list-and-graphics-handshake.md | 590 (all read) | `readiness: BEHAVIORALLY UNDERSTOOD` (:6), `confidence: PROVEN` (:7), `audit: passes: 1` (:22), `crossref_clean: false` (:25) | no status banner. The lead blockquote :31-44 says "Section 13 is **empty**: nothing here is observed live" (:43-44) | not listed (grep of README.md for "CONTRACT-render-command", "handshake" and "S-39": no hit) |
| Render-Command-List/the-ordered-render-command-list.md | 1966 (all read) | `status: AUDITED` (:4), `passes: 1` (:20), `crossref_clean: true` (:23) | no top banner. Inline correction banner at :197 ("⚠ Corrected 2026-09-14 (FABLE, UQ-230)") | README.md:89 "**DOCUMENTED, tier 1, crossref-clean.**". README.md:91 "returns a **draw-order key** — `1` for scene begin, `0x10` for the ordinary passes, `0x80` for video." |
| Graphics-Thread-Handshake/the-shared-command-state-word.md | 927 (all read) | `status: AUDITED` (:4), `passes: 1` (:20), `reopened_count: 2` (:24) | :40-43 "⚠ **Corrected 2026-09-07, hours after this document was written.** … **who consumes the batch is an open question.**" | not listed (no README hit for "shared-command-state" or "Graphics-Thread-Handshake") |

TSV checks:

| file | what was counted | result | claim it confirms or contradicts |
|---|---|---|---|
| Render-Command-List/members/ordered-object-vtable-slots.tsv | `awk` distinct `class` values, with and without `OrderedObject` | 43 classes including the base; **42** without it. 40 classes have 3 rows and 3 classes have 4 rows | Contradicts Render-Command-List/the-ordered-render-command-list.md:279 "**43 concrete classes**". Confirms CONTRACT-render-command-list-and-graphics-handshake.md:95 "42 subclass vtables" and Render-Command-List/the-ordered-render-command-list.md:711 "RTTI's **42** direct". The base `OrderedObject 009010B8` has only slots 0-2 in the TSV, while CONTRACT-render-command-list-and-graphics-handshake.md:94 says "base vtable 009010B8 has 7" (see CL.CV-10) |
| same | slot-2 bodies, via `uniq -c` | `0053DD10`×11, `001F2880`×18, `00212E20`×3, `001F28A0`×1, `001F2890`×4, `00290180`×1, `0016EE70`×1, `00879750`×2, `001F49E0`×1 (= 42), plus base `00861EC6` | Confirms Render-Command-List/the-ordered-render-command-list.md:301-309 value for value |
| Render-Command-List/postprocess-context-accesses.tsv | data rows (`awk NR>1`), and distinct `disp` values | 777 rows; 219 distinct offsets | 219 confirms Render-Command-List/the-ordered-render-command-list.md:798. 777 against "776 sites" (Render-Command-List/the-ordered-render-command-list.md:798) is explained by Render-Command-List/the-ordered-render-command-list.md:1257-1258: "It is added there now" (CL.CC-6) |
| Graphics-Thread-Handshake/members/inert-spin-census.tsv | data rows (header comment line and column line skipped) | 19. The header line reads "inert backward loops 19" | Confirms Graphics-Thread-Handshake/the-shared-command-state-word.md:494 "**nineteen**". The rows do not name the word `02EAF6D8`, so the "seventeen" could not be checked from the TSV |

### A.6 [GP] Gi render commands and the legacy PS2 GS/VIF layer

Short names in this part: **GI** = `Gi-Render-Commands/gi-render-command-family.md`; **TEX** = `Legacy-PS2-GS/texture-mip-local-memory-budget.md`; **VIF** = `Legacy-PS2-GS/the-vif1-vu1-layer.md`.


| page | lines | front matter status | body banner | README tag |
|---|---:|---|---|---|
| GI | 1864 (wc -l) | `status: AUDITED` (Gi-Render-Commands/gi-render-command-family.md:4); `last_reviewed: 2026-09-02` (Gi-Render-Commands/gi-render-command-family.md:18) | none | "**DOCUMENTED, tier 1.** Eighteen classes carrying the PlayStation 2 drawing vocabulary" (README.md:94-95) |
| TEX | 433 | `status: AUDITED` (Legacy-PS2-GS/texture-mip-local-memory-budget.md:4) | "**Status:** **APPLIED AND PERSISTENCE-CERTIFIED**, GN checkpoint 2026-09-02." (Legacy-PS2-GS/texture-mip-local-memory-budget.md:277) | listed with no status tag: "- the 4 MiB GS local-memory texture budget still live in the PC port" (README.md:102) |
| VIF | 906 | `status: DOCUMENTED — UQ-213 answered 2026-09-27 (...); UQ-215 answered 2026-09-27 (...) (box pending)` (Legacy-PS2-GS/the-vif1-vu1-layer.md:4) | "**PARTIAL.** The interpreter, the machine state, the installation paths and the program population are read." (Legacy-PS2-GS/the-vif1-vu1-layer.md:32); interior: "page is PARTIAL — no disposition claimed" (Legacy-PS2-GS/the-vif1-vu1-layer.md:901-902) | not listed (grep of README.md for `the-vif1-vu1-layer` returns nothing) |

TSV checks:

| file | what counted | result | page claim |
|---|---|---|---|
| `Legacy-PS2-GS/vif1-packet-templates.tsv` | data rows (`tail -n +2 | wc -l`) | 77 | confirms "all **77 template rows**" (Legacy-PS2-GS/the-vif1-vu1-layer.md:430) |
| same | `grep -o "UNPACK [A-Z0-9-]*"` count and `uniq -c` | 87, all `UNPACK V4-32` | confirms "All 87 UNPACK commands ... are `V4-32`" (Legacy-PS2-GS/the-vif1-vu1-layer.md:827) and "UNPACK 87" (Legacy-PS2-GS/the-vif1-vu1-layer.md:446) |
| same | distinct builders (col 2, `sort -u`) | 76 | confirms "76 distinct builders" (Legacy-PS2-GS/the-vif1-vu1-layer.md:441); contradicts "all 74 hub-called builders" (Legacy-PS2-GS/the-vif1-vu1-layer.md:526-527) — see GP.CC-5 |
| same | rows with `obj_header` = `0x30` | 37 | confirms "`0x30` on exactly the 37 MPG rows" (Legacy-PS2-GS/the-vif1-vu1-layer.md:450) |
| `Legacy-PS2-GS/members/vu1-region-functions.tsv` | data rows | 351 | confirms "all **351** listed functions" (Legacy-PS2-GS/the-vif1-vu1-layer.md:769) |
| same | role tokens (split on `;`) | `VU-helper(VU-state-toucher)` 44, `VU1-microprogram(VU-state-toucher)` 10, `microprogram(template)` 34, `microprogram(registrar)` 28, `MPG-packet-builder` 36, `startup-template` 73, `sticky-flag-user` 40, `sub-program` 21, `XGKICK-shaped-leaf` 9 + 1 reference, `other` 149, `other(no-caller)` 16 | the TSV has moved 10 rows to microprogram; the page table still says "VU helper — VU-state toucher, not installed | 54" (Legacy-PS2-GS/the-vif1-vu1-layer.md:779) — see GP.CS-10. Confirms "9 + the `004EF860` reference" (Legacy-PS2-GS/the-vif1-vu1-layer.md:782) against "eight of them share" (Legacy-PS2-GS/the-vif1-vu1-layer.md:669) — GP.CC-8 |
| `Legacy-PS2-GS/members/vif1-gif-tags.tsv` | data rows / distinct builders | 75 / 45 | matches the pre-correction "75 tags" (Legacy-PS2-GS/the-vif1-vu1-layer.md:554) and the struck "45 of the 74" (Legacy-PS2-GS/the-vif1-vu1-layer.md:545); does NOT carry the corrected "at least 61" (Legacy-PS2-GS/the-vif1-vu1-layer.md:545) — GP.CC-6 |
| `Gi-Render-Commands/members/geometry-instance-vtable-slots.tsv` | non-comment lines minus header | 144 | confirms "(144 rows)" (Gi-Render-Commands/gi-render-command-family.md:1054) |

### A.7 [EF] Effect containers, element dispatch and the per-frame element update

Short names in this part: **DISP** = `Effect-File-Formats/effect-element-type-dispatch.md`; **FBF** = `Effect-File-Formats/an-effect-element-frame-by-frame.md`; **EFX** = `Effect-File-Formats/efx-and-efb-effect-containers.md`; **ERM** = `Effect-File-Formats/README.md`; **CAT** = `README.md`.


| page | lines | front-matter status | body banner | CAT tag |
|---|---:|---|---|---|
| ERM | 17 | none (no front matter) | none; body says "nothing in the database describes either one" (Effect-File-Formats/README.md:8-9) | not listed |
| DISP | 2292 | "status: DOCUMENTED — the last open box, what 002F2530 does beyond its entry (UQ-206 …) answered 2026-09-17; §2.8 census re-walked and the step's role corrected 2026-09-29" (Effect-File-Formats/effect-element-type-dispatch.md:4); no `readiness:` | "**PARTIAL.** Read:" (Effect-File-Formats/effect-element-type-dispatch.md:32); also "(Page status PARTIAL: this citation is evidence-bearing once the page's own readiness lands…)" (Effect-File-Formats/effect-element-type-dispatch.md:1055-1056) | not listed |
| FBF | 327 | "status: AUDITED" (Effect-File-Formats/an-effect-element-frame-by-frame.md:4); no `readiness:` | none | "**DOCUMENTED, tier 1 (2026-09-19), static.**" (README.md:64-65) |
| EFX | 645 | "status: PARTIAL — the residue this line named is answered in §2b …" (Effect-File-Formats/efx-and-efb-effect-containers.md:4); `corpus_validated: "… First 8 bytes only — the payload is still unmeasured."` (Effect-File-Formats/efx-and-efb-effect-containers.md:18) | "**No `.efx` or `.efb` file was opened to write this sheet.**" (Effect-File-Formats/efx-and-efb-effect-containers.md:39), superseded as history by Effect-File-Formats/efx-and-efb-effect-containers.md:59-61 | not listed |

All four read line by line (DISP in 300-380 line chunks).

.tsv checks (files in `Effect-File-Formats/members/`):

| file | what counted | result | page claim |
|---|---|---|---|
| effect-type-methods.tsv | rows (`wc -l`) | 211 = header + 210 types | confirms "210 rows" (Effect-File-Formats/effect-element-type-dispatch.md:904) |
| effect-type-methods.tsv | non-`default` / non-`-` entries per column, distinct (awk) | step 47 types / **41** distinct; update 47 / 38; walk 46 distinct; setup 38; sub-step/sub-setup/sub-update/sub-walk 18 each; seventh 6; sub-seventh 9; all columns together **248** distinct; only `0016D6A0` in >1 column (3) | confirms table Effect-File-Formats/effect-element-type-dispatch.md:168-179; **contradicts** "Within the step, update and walk methods each type has its own function" (Effect-File-Formats/effect-element-type-dispatch.md:179-180) and audit "no two types share a handler" (Effect-File-Formats/effect-element-type-dispatch.md:20): step shares `0044CC10` (0x80/0x82/0x83), `00455390` (0x8C/0x94/0x95/0x97), `00457E10` (0x8F/0x90); update shares `00450480` x5, `0045B260` x4, `00464F10` (0x41/0xD0), `00456EF0` x2 |
| effect-type-methods.tsv | setup column (col 5) lookup of the 15 "creation arm" addresses | `00539030`→0x08, `00539170`→0x0A, `00538DB0`→0x05, `00539610`→0x88, `00539740`→0x89, `00539870`→0x8A, `005393B0`→0x85, `005394A0`→0x86, `00539980`→0x84/0x96, `00539A60`→0x8B, `00539B30`→0x8C/0x94/0x95, `00539C10`→0x8D, `00539DA0`→0x8F/0x90, `00539E90`→0x91/0x92, `00539F80`→0x97 | **contradicts** the "+0x44 = 0x4N/0x5N" labels Effect-File-Formats/effect-element-type-dispatch.md:2082-2138 (see EF.CV-11) |
| effect-type-methods.tsv | sub-walk column (col 9) | 18 handlers: 0x42 `0047BFA0`, 0x68 `00522D80`, 0x69 `00523D30`, 0x6A `00526080`, 0x6B `005294F0`, 0x70 `0016D6A0`, 0x71 `0052A360`, 0x72 `0052B080`, 0x73 `0052D920`, 0x74 `0052EA90`, 0xA3 `00524A50`, 0xA4 `00522300`, 0xA6 `00524E30`, 0xA7 `00526A10`, 0xA8 `005271D0`, 0xA9 `00528150`, 0xAA `00528B50`, 0xAB `0052C070` | confirms 18 (Effect-File-Formats/effect-element-type-dispatch.md:175); contradicts "eight bodies" scope (EF.CV-12) |
| effect-type-methods.tsv | 0x09 row | default in step/update/walk/setup | confirms Effect-File-Formats/an-effect-element-frame-by-frame.md:60-61 (0x09 → default arm) |
| type_census.tsv | data rows; sum of `chunks` column | 55 rows; 48,868 | confirms "55 distinct types in 48,868 `0xA00` records" (Effect-File-Formats/effect-element-type-dispatch.md:795-796) |
| effect-kind-441970.tsv | rows; rows with target `004419D0` | 145 rows; walk kinds = 0x40 0x41 0xA1 0xA2 0xA5 0xD0; 139 others | confirms Effect-File-Formats/effect-element-type-dispatch.md:854-855; contradicts unconditional walk reading of Effect-File-Formats/effect-element-type-dispatch.md:129 (EF.CV-7) |

### A.8 [ET] Effect element types, kind-0x54 meshes, menu effect registry and VFX layers

Short names in this part: **mesh** = `Effect-File-Formats/effect-mesh-records-kind-54.md`; **00-0a** = `Effect-File-Formats/the-element-types-00-0a.md`; **40-42** = `Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md`; **60-74** = `Effect-File-Formats/the-element-types-60-74.md`; **80-97** = `Effect-File-Formats/the-element-types-80-97.md`; **menu** = `Effect-File-Formats/the-menu-effect-registry.md`; **six-layers** = `Effect-File-Formats/the-six-vfx-display-layers.md`.


| page | lines | front-matter status | body status banner | README tag |
|---|---:|---|---|---|
| Effect-File-Formats/effect-mesh-records-kind-54.md | 237 | `:4` "PARTIAL — record layout and census complete; … SD-140 answered 2026-10-01 … open residue: the uncharacterised pass operators and the clipper 00521450" | none | not listed |
| Effect-File-Formats/the-element-types-00-0a.md | 503 | `:4` "DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS; documented_rule READY)" | none (`:4` carries the history "Was PARTIAL on: …") | not listed |
| Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md | 331 | `:4` "DOCUMENTED — GI-9 answered 2026-09-29 (FABLE) … documented_rule.py READY, no open box or live id" | `:317-318` "page is PARTIAL — no disposition claimed" (inside an evidence-only section) | not listed |
| Effect-File-Formats/the-element-types-60-74.md | 372 | `:4` "DOCUMENTED — GI-10 answered 2026-09-29 (FABLE) … documented_rule.py READY" | none | not listed |
| Effect-File-Formats/the-element-types-80-97.md | 187 | `:4` "DOCUMENTED — GI-11 answered 2026-09-29 (FABLE) … documented_rule.py READY" | none | not listed |
| Effect-File-Formats/the-menu-effect-registry.md | 369 | `:4` "DOCUMENTED — the record fields (UQ-208), the owning screens (UQ-210) and the instance field +0x338 (UQ-209, the context's mode base) all answered 2026-09-17" | `:33-34` "PARTIAL. Read: the table shape, the API, the link to the instance list, the callers. Not read: the record's fields past +8, what +0x338 in an instance means, and which menu uses which id." | not listed |
| Effect-File-Formats/the-six-vfx-display-layers.md | 269 | `:4` "DOCUMENTED"; `:19-20` "…were not read; pending first review" | none | README.md:77-79 "DOCUMENTED, tier 1 (2026-09-19), static. Effects are drawn six times a frame, once per layer … Layer 3 has its own path, beside the depth-sorted display list." |

README grep (`grep -n` for each page name in `README.md`) found only the six-layers page (line 77). The other six are
not listed.

TSV checks (members/ of EFF):

| file | what counted | result | page claim |
|---|---|---|---|
| effect-mesh-54-records.tsv | `wc -l` / awk rows | 2,252 data rows, 1,087 distinct files | confirms Effect-File-Formats/effect-mesh-records-kind-54.md:39-40 |
| same | awk: rows with c18≠c1A; c1E≠0; ok≠1; c18≠3·tri+4·quad; c16≠c14 | 0; 0; 0; 0; 1,670 | confirms `:95`, `:102-103`, `:110`, `:217` |
| same | awk sums of c14 / c16 / c18 / c1A | 50,707 / 52,808 / **155,916** / **155,916** | confirms `:119` (52,808), `:121` (155,916), `:123` (50,707); **contradicts `:120` "147,220"** (ET.CC-1) |
| same | awk tri+quad sum | 41,798 | matches per-primitive byte histogram 40,922+264+612 = 41,798 at `:137-138` |
| same | awk c1C histogram and sum | 0:1,813, 1:425, 2:14; sum 453 | confirms `:139`; sum 453 vs "439 / 439" at `:140-141` (ET.CC-2, may be nonzero-only) |
| same | awk `sub` histogram | identical to the page | confirms `:106` |
| effect-mesh-54-element05.tsv | rows; slots_filled histogram; files | 5,164; {0:1,1:4,268,2:894,3:1}; 1,088 | confirms `:156-158` |
| type_census.tsv | rows for 0x05, 0xD1, 0xA0/0x03/0x07/0x08/0x81/0x8A/0x97, 0x40, 0x94, 0x95, 0xAB, 0xD0 | 0x05 5,204 chunks (5,168 efx/efb); 0xD1 765 chunks/406 files/131 assets; listed-absent types have no row; 0x40 2,254/687; 0xD0 1,437/447; 0xAB 7/3; 0x94 2,344/357; 0x95 456/216 | confirms Effect-File-Formats/the-element-types-00-0a.md:378, Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:265-267 (406 = 297+109 files), Effect-File-Formats/the-element-types-80-97.md:171-173; 0x05 vs mesh page 5,164 is ET.CC-3 |
| type_census.tsv | rows 0xA1-0xA8 | 0xA2 6,303 chunks / 493 assets; 0xA1 504; 0xA3 447; 0xA6 359; 0xA8 367 | shows ET.G-9 (heavily authored types with no behaviour on 40-42) |

### A.9 [MF] Model formats: add-motion tables, ADM, FCP, FDM/FOR

Short names in this part: **SKEL** = `Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md`; **ADM** = `Model-And-Motion-Formats/adm-add-motion-tables.md`; **FCP** = `Model-And-Motion-Formats/fcp-character-parameter-block.md`; **FDM** = `Model-And-Motion-Formats/fdm-and-for-entries.md`; **MREADME** = `Model-And-Motion-Formats/README.md`.


| path | lines (wc -l) | front-matter status | body status banner | category README tag |
|---|---:|---|---|---|
| `Model-And-Motion-Formats/README.md` | 61 | no front matter | none; the format table gives `adm` "per-bone add-motion tables — explained 2026-09-13" (`:9`) | not listed (the only MMF page that `README.md` lists is `the-pose-sequencer.md`, `README.md:69-72`) |
| `Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md` | 520 | `status: AUDITED` (`:4`); `last_reviewed: 2026-09-13` (`:21`); `audit: passes: 1`, `last_pass: 2026-09-13` (`:26-27`) | none | not listed |
| `Model-And-Motion-Formats/adm-add-motion-tables.md` | 501 | `status: AUDITED` (`:4`); `last_reviewed: 2026-09-13` (`:20`); `crossref_clean: true` (`:27`) | none | not listed |
| `Model-And-Motion-Formats/fcp-character-parameter-block.md` | 772 | `status: DOCUMENTED — every register row is closed or dispositioned and the page's residue is answered (owner re-status 2026-10-01, OPUS, …)` (`:4`); `last_reviewed: 2026-09-11` (`:19`); `passes: 1` / `last_pass_state: opus-fcp-character-parameter-block-pass-2` (`:21-23`) | none | not listed |
| `Model-And-Motion-Formats/fdm-and-for-entries.md` | 377 | `status: DOCUMENTED — the @FOR tail lists and the @FDM descriptor +0x08 read 2026-09-30 (SWE2-DATA, UQ-218 pass 18)` (`:4`); `last_reviewed: 2026-09-30` (`:14`) | none | not listed |

No category README line names any of the five pages. `grep -n` on `README.md` for the five page names / `Model-And-Motion` returns only `README.md:69` and `:71` (the pose sequencer).

**.tsv checks:** none. `Model-And-Motion-Formats/members/` holds six census `.py` scripts and `model-oscillator-subsystem.tsv` (`ls`, 7 entries), and none of them covers a figure on these five pages. All census figures below are page-text only.

### A.10 [MM] Motion formats: FEF/motion entries, FRP, FTE/FCT, FTR, oscillator, pose sequencer

Short names in this part: **ACH** = `Authored-Commands/the-authored-presentation-command-handlers.md`.


| page | lines | front-matter status (line) | body banner | category README tag |
|---|---|---|---|---|
| Model-And-Motion-Formats/fef-and-motion-entries.md | 1014 | "DOCUMENTED — the embedded EFX0010 reaches only the ret 0 stub (DD batch 14, A1-A9); which @FEF models a session loads and the target-bearing arm's look are runtime-only (owner re-status 2026-10-01 …; documented_rule READY)" (:5) | none | not listed (README.md has no hit; the sub-folder Model-And-Motion-Formats/README.md:42-46 describes it, no status tag) |
| Model-And-Motion-Formats/frp-object-container.md | 390 | "AUDITED — no register row is open (owner re-status 2026-09-30, OPUS) …" (:4); promoted "2026-10-01 DOCUMENTED -> AUDITED" (:29) | blockquote "One container under two extensions: 3,164 .ca and 1,066 .cm, all @FRP." (:34) | not listed (Model-And-Motion-Formats/README.md:25 links it, no tag) |
| Model-And-Motion-Formats/fte-fct-texture-colour-tables.md | 321 | "DOCUMENTED — the residue is answered (DD batch 10); what a co-drawn model that shares a texture key shows is runtime-only (owner re-status 2026-10-01 …; documented_rule READY)" (:4) | none | not listed |
| Model-And-Motion-Formats/ftr-node-table.md | 328 | "DOCUMENTED — flags, aux values, consumers and tail readers read (DD batches 10 and 14); bit 29's value is NO ADMISSIBLE SOURCE (SD-195) (… documented_rule READY)" (:4) | none | not listed |
| Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md | 542 | "DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS; documented_rule READY) …" (:4); `last_reviewed: 2026-09-14` (:18) | none | not listed (Model-And-Motion-Formats/README.md:37-40 "(36 members)") |
| Model-And-Motion-Formats/the-pose-sequencer.md | 279 | "DOCUMENTED" (:4) | none | README.md:69-70 "**DOCUMENTED, tier 1.** FCP section 7: eight events, … Format tested on all 1,066 FCP blocks." |

No `readiness:` key on any of the six pages (grep `readiness:` over Model-And-Motion-Formats/*.md: no hit).

.tsv checks:

| file | what counted | result | page claim |
|---|---|---|---|
| Model-And-Motion-Formats/members/model-oscillator-subsystem.tsv | `wc -l` = 40; `awk 'NR>1' | wc -l` = 39 data rows; no duplicate addresses (`sort | uniq -c`) | 39 members | contradicts "lists all 36 members" (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:185) and "(36 members)" (Model-And-Motion-Formats/README.md:40) → MM.CC-5 |
| same | grep for `0040B180`, `0040AA20` | neither address is a row; `0054B1F0` is (row 39) | `0040B180` is listed in the page's oscillator band (Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md:332) but not in the members file |

### A.11 [PP] Post-processing and visual tuning parameters

Short names in this part: **CS** = `Post-Processing/CONTRACT-post-processing-subsystem.md`; **CP** = `Post-Processing/CONTRACT-ppfx-effect-creation.md`; **PI** = `Post-Processing/ppfx-function-identification.md`; **CAT** = `Post-Processing/the-post-processing-effect-catalogue.md`; **VR** = `Visual-Tuning-Parameters/README.md`; **RR** = `Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md`; **RCL** = `Render-Command-List/the-ordered-render-command-list.md`; **HL** = `Post-Processing/members/ppfx-handle-layout.tsv`.


| page | lines | front-matter status/readiness | body banner | category README tag |
|---|---|---|---|---|
| CS | 329 | `readiness: CONTRACT READY   # the ordering, the flags and the boundary are STATIC; nothing here was observed live` (Post-Processing/CONTRACT-post-processing-subsystem.md:6); `confidence: PROVEN` (Post-Processing/CONTRACT-post-processing-subsystem.md:7) | "Why this exists. S-40's verdict row is SCOPE-SHORT … this contract is the subsystem view" (Post-Processing/CONTRACT-post-processing-subsystem.md:33-38) | not listed (README lists only PI under `Post-Processing/` — "documented", README.md:104) |
| CP | 317 | `readiness: BEHAVIORALLY UNDERSTOOD` (Post-Processing/CONTRACT-ppfx-effect-creation.md:6); `confidence: PROVEN` (Post-Processing/CONTRACT-ppfx-effect-creation.md:7) | "Scope, stated plainly because it is short of the system … S-40's contract cell should read SCOPE-SHORT, not MET." (Post-Processing/CONTRACT-ppfx-effect-creation.md:29-37) | not listed |
| PI | 736 | `status: AUDITED` (Post-Processing/ppfx-function-identification.md:4) | headline "135 more functions named (plus 12 exception funclets)" (Post-Processing/ppfx-function-identification.md:30) | "DOCUMENTED, tier 2. 147 post-processing functions named … Identity only; no body read yet." (README.md:106-110) |
| CAT | 1045 | `status: AUDITED` (Post-Processing/the-post-processing-effect-catalogue.md:4) | none (lead quote Post-Processing/the-post-processing-effect-catalogue.md:29-31) | not listed |
| VR | 74 | no front matter | none | not listed (folder README) |
| RR | 878 | `status: PARTIAL — OV-42 (live, ASTRA) stays open in the F4 section; … every other register row is closed …` (Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:4) | "PARTIAL. The names and asset paths are authored strings … ~~What each parameter numerically does …~~ (Corrected 2026-09-30 …)" (Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:35-38) | "PARTIAL, tier 2. ~150 authored parameter names … and the 15 `.phyre` shader assets that consume them." (README.md:128-130) |

TSV checks:

| file | what counted | result | page claim |
|---|---|---|---|
| HL | data rows (`awk NR>2`) | 352 | confirms "352 lookups" (Post-Processing/the-post-processing-effect-catalogue.md:803) |
| HL | rows with numeric `this_offset` | 337 placed; 15 `?` | confirms "337 placed … 15 lookups whose store is not within three instructions" (Post-Processing/the-post-processing-effect-catalogue.md:803) |
| HL | rows whose name is a literal other than `(built string)`/`%s%d` | 271 (279 minus 8 `%s%d`) | confirms "271 of those with their literal name" (Post-Processing/the-post-processing-effect-catalogue.md:803) |
| HL | base column | r14 302, rsi 35, ? 15 | confirms "for one run of 35, `this + 0x1AA10`" (Post-Processing/the-post-processing-effect-catalogue.md:803) |
| HL | min/max placed offset | 0xA0 / 0x221D8 (`tech_HybridLogGamma`, Post-Processing/members/ppfx-handle-layout.tsv:339) | confirms Post-Processing/the-post-processing-effect-catalogue.md:803 "`this + 0xA0` to `this + 0x221D8`"; contradicts Post-Processing/ppfx-function-identification.md:674-676 (PP.CV-6). TSV header line says "offset range 0x14..0x221D0" (raw displacements) |
| HL | kind column | inline 0x60 224, inline 0x48 33, suffix-family 65, numbered-family 26, two-dimensional 4 | confirms 224/33 inline (Post-Processing/the-post-processing-effect-catalogue.md:806, Post-Processing/CONTRACT-ppfx-effect-creation.md:102) and 65/26/4 helper sites (Post-Processing/CONTRACT-ppfx-effect-creation.md:83-84) |
| HL | count distribution of suffix+numbered (91 rows) | 1×15, 4×2, 8×42, 16×6, 17×8, 25×5, 32×4, 33×8, 64×1; sum 1,172 | confirms Post-Processing/CONTRACT-ppfx-effect-creation.md:120-121 and Post-Processing/the-post-processing-effect-catalogue.md:148; two-dimensional rows: 3×`-1`, 1×8 → "92 of the 95 family counts resolve" (Post-Processing/the-post-processing-effect-catalogue.md:803) confirmed |
| HL | row for `tech_DepthOfField_BackgroundLayerMaskT1_Sn` | `0xDB60 r14 suffix-family 25` (Post-Processing/members/ppfx-handle-layout.tsv:113) | the Post-Processing/the-post-processing-effect-catalogue.md:142 example is a `0072DCF0` *suffix-family* site (bears on PP.CV-5) |
| CAT (md, not tsv) | `^tech_` lines; family headers; sum | 325; 35 headers summing 325; each header count matches its block; uniforms block 36 lines (Post-Processing/the-post-processing-effect-catalogue.md:703-738) | confirms Post-Processing/the-post-processing-effect-catalogue.md:198, Post-Processing/the-post-processing-effect-catalogue.md:886 |
| PI (md) | the 137-row listing Post-Processing/ppfx-function-identification.md:461-597 by class | 137 rows; CPostEffect 58; 23 classes; 15 "more than one" rows | contradicts Post-Processing/ppfx-function-identification.md:457-458 (PP.CC-3) |

### A.12 [CM] Scripted camera, screen fade, screen effects, aspect fit, position-to-scalar, movie index

Short names in this part: **MR** = `Movie-Containers/README.md`; **MH** = `Movie-Containers/mh-movie-seek-index.md`; **PTS** = `Position-To-Scalar/how-a-position-becomes-a-single-number.md`; **SF** = `Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md`; **AF** = `Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md`; **CI** = `Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md`; **CR** = `Scripted-Camera/how-a-camera-reaches-the-renderer.md`; **P** = `Scripted-Camera/the-scripted-camera-player.md`; **RM** = `README.md`; **WT** = `../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`.


| page | lines | front-matter status / readiness | body banner | category README tag |
|---|---:|---|---|---|
| MR | 35 | no front matter | "Confirmed by the magic census — 2026-09-03" (Movie-Containers/README.md:19); "`.mh` — explained 2026-09-12" (Movie-Containers/README.md:30) | not listed |
| MH | 278 | `status: AUDITED` (Movie-Containers/mh-movie-seek-index.md:4); `corpus_validated: "43 / 43 .mh ... all opened"` (Movie-Containers/mh-movie-seek-index.md:18) | "**the files are inert**" (Movie-Containers/mh-movie-seek-index.md:34); "**Nothing on this page is wrong.**" (Movie-Containers/mh-movie-seek-index.md:135) | not listed |
| PTS | 429 | `status: AUDITED — static; all 76 call sites use the node's output as a modulate ...` (Position-To-Scalar/how-a-position-becomes-a-single-number.md:4); `readiness: SIGNATURE RESOLVED` (Position-To-Scalar/how-a-position-becomes-a-single-number.md:8) | none beyond dated sections (§10 2026-09-12, §11 2026-09-13, §12/§13 2026-09-19) | not listed |
| SF | 719 | `status: AUDITED` (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:4) | none | "**DOCUMENTED, tier 1 (2026-09-12).**" (README.md:38) |
| AF | 217 | `status: DOCUMENTED — every register row is answered (UE-1 to UE-4, 2026-09-14) ...` (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:4); `crossref_clean: false` (Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:19) | none | "**PARTIAL, tier 1.** ... What that does on screen is **not** established." (README.md:25-30) |
| CI | 430 | `status: DOCUMENTED` (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:4); `note: written by FABLE; static throughout ...; pending first review` (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:20) | falsification pass 1 2026-09-29 (Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:406) | "**DOCUMENTED, tier 1 (2026-09-19), static.**" (README.md:43) |
| CR | 519 | `status: DOCUMENTED` (Scripted-Camera/how-a-camera-reaches-the-renderer.md:4); `note: ... pending first review` (Scripted-Camera/how-a-camera-reaches-the-renderer.md:19-20) | falsification pass 1 2026-09-29 (Scripted-Camera/how-a-camera-reaches-the-renderer.md:494) | not listed |
| P | 1196 | `status: AUDITED` (Scripted-Camera/the-scripted-camera-player.md:4); `crossref_clean: false` (Scripted-Camera/the-scripted-camera-player.md:24) | none | "**DOCUMENTED, tier 1 (2026-09-12).**" (README.md:31) |

TSV / member checks:

| file | what counted | result | page claim |
|---|---|---|---|
| `Screen-Fade/members/movie-fade-schedule-names.tsv` | rows, row_bytes column (awk) | 49 rows id 0-48; `1e 1e 3c 3c` in ids 1,5,7,9,11,16,18,21,22,30,34 = 11; flags byte 01 in 17,19,21, 03 in 26,35,43; +2==00 (non-zero rows) 3,13,24,28,29,31; +1==00 with real length 6,10,17,19,20,23,26,27,36,42,43,48; ids 4,10,42,48 = `.. 00 0f` (+3=0, +4=0x0F); id 25 `19 1e 0f cd 96`; id 43 `2b 00 06 00 06 .. 03`; all-zero 0,32,37-41,44-47 (11) | confirms Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:122, 123-128, 362-365, 375-385, 677-681; contradicts the label "no fade-out lead" (Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:126, Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md:362) — see CM.CV-7 |
| `Position-To-Scalar/members/fade-node-consumers.tsv` | header + data rows; distinct callers; callers < 0045E930 (python) | header "76 in 75"; 67 / 8 / 1; 76 rows, 75 distinct; lowest 00442550; **46** distinct callers below 0045E930 | confirms Position-To-Scalar/how-a-position-becomes-a-single-number.md:321, 380-388, 326; contradicts "57 of the 75 sit below `0045E930`" (Position-To-Scalar/how-a-position-becomes-a-single-number.md:327) — CM.CC-1 |
| `Scripted-Camera/members/camerashake-census.tsv` | verb rows | 1a3 328, clear 315, stop_19e 178, sync_1a4 13, change 6, **camerashakestop 2**; sum 842 | confirms Scripted-Camera/how-a-camera-reaches-the-renderer.md:306-307 total 842 and 328/315; page omits the 2 `camerashakestop` (Scripted-Camera/how-a-camera-reaches-the-renderer.md:307 lists 328+315+178+13+6 = 840) — CM.CC-4 |
| `Script-Screen-Effects/members/screen-effect-census.tsv` | 24 verb rows, sum of calls (awk) | 24 verbs, 13,905; aplpha 2304/264; captureonce 2305; clearfade 2306 (2305×15 + 1×10); cutinplay 5/4; setsoftfocusmode 52/49 all `0,0,0,0`; nine verbs 0 | confirms Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md:34-58 |
| `Screen-Mode-And-Aspect-Fit/members/aspect-record-consumers.txt` | method lines, sum of pass-on column | 24 methods, 43 passed on; header "72 call sites, 43 passed on, 29 not passed" | confirms Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md:106-107 |

