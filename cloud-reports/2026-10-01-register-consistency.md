# Cloud report: register vs page consistency sweep (2026-10-01)

Report only. Nothing under `FFXII TZA/` or `Tools/` was edited. This report is a pointer for local verification, not evidence (docs/CLOUD_AGENTS.md, output contract 4).

## Counts

| category | findings |
|---|---|
| (a) front-matter `status:` contradicts register row | 3 |
| (b) prose says open/pending/not read/not established about a closed id, no answer note on the line | 71 |
| (c) unticked box on a closed id / ticked box on an OPEN id | 0 |
| (d) "pending review" note where a review record exists | 10 |

Scope and method: 530 pages under `[0-9][0-9]-*/`; register `_index/OPEN-QUESTIONS.md` parsed to 1,805 ids (1,517 ANSWERED, 133 SUPERSEDED, 53 CLOSED, 42 NOT A QUESTION, 18 NO ADMISSIBLE SOURCE, 17 OUT OF EVIDENCE BOUNDARY, 7 WITHDRAWN, 5 OPEN, 6 PARTLY ANSWERED, 1 PARTIAL, others). Text inside `~~strike~~` (including multi-line) and code fences was ignored. A box's own id follows the register's label-form rule (`**ID.**`, else first bolded id). The register is the authority; a row with an unrecognised leading word was read from the first bolded status word in the row.

Caveats: (b) is a wording heuristic. It flags a clause with an open-wording phrase next to a register id and skips any line that also carries ANSWERED/SUPERSEDED/CLOSED/Reconciled, so it can both miss stale text and flag a legitimate "narrowed residue stays open" sentence. Each (b) line needs a human read. Status lines of ids that the register lists as OPEN or PARTIAL (RC-5, OV-42, GR-18) were checked and are consistent with their pages.

## (a) Front-matter status contradicts the register

- `13-Rewards-Progression-Economy/experience-and-license-point-award.md:4` — **GR-16** (ANSWERED 2026-10-01)
  - quote: `status: PARTIAL — SECTION-03 independent peer acceptance pending (GR-16); reward-row binding lifetime (GR-17) and edge-state reachability (GR-18) open; …`
  - contradiction: status calls GR-16 pending; its row closed 2026-10-01 by auditsem-review-section03-1001 (ACCEPT-WITH-NARROWING).
  - proposed: status: PARTIAL — SECTION-03 independent acceptance recorded 2026-10-01 (GR-16, auditsem-review-section03-1001, ACCEPT-WITH-NARROWING N1); edge-state reachability (GR-18, PARTIAL) open; …
- `13-Rewards-Progression-Economy/experience-and-license-point-award.md:4` — **GR-17** (ANSWERED 2026-09-30)
  - quote: `…reward-row binding lifetime (GR-17) and edge-state reachability (GR-18) open; …`
  - contradiction: Same line calls GR-17 open; its row is ANSWERED 2026-09-30 (record gr17-reward-table-lifetime-0930) and the body box at line 222 is already ticked [x].
  - proposed: Drop GR-17 from the "open" list: "reward-row binding lifetime (GR-17) answered 2026-09-30; edge-state reachability (GR-18) open".
- `13-Rewards-Progression-Economy/how-experience-is-computed-and-divided.md:4` — **GR-16** (ANSWERED 2026-10-01)
  - quote: `status: REOPENED — SECTION-03 independent peer acceptance pending (GR-16); converted to a function note of the award page 2026-09-30 (FABLE)`
  - contradiction: status calls GR-16 pending; row closed 2026-10-01.
  - proposed: status: REOPENED — SECTION-03 independent acceptance recorded 2026-10-01 (GR-16, ACCEPT-WITH-NARROWING); converted to a function note of the award page 2026-09-30 (FABLE). (Whether REOPENED itself should change is the owner's call.)

Checked, no finding: no status line calls an OPEN id answered. `spawn-placement-and-retirement.md:4` (REOPENED) already says L-12/L-13 are SUPERSEDED.

## (b) Prose says open/pending for a closed id

Sorted by folder. Format: `file:line` · id (register status) · matched phrase · quote · proposed wording.


### 00-Engine-Core-Runtime

- `00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md:668` · **O-4** (ANSWERED) · "stays open"
  - quote: `**O-4 stays open**: what the six modes *mean* is still not established, and this pass did not`
  - proposed: Reword to "O-4 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-D-ids-108-139.md:321` · **UQ-15** (ANSWERED 2026-09-25 (FABLE, Claude Opus ) · "stays open"
  - quote: `'+0x2F8' has no console arm and no loader store, and no reader turned up in the UQ-15 census, so it stays open.`
  - proposed: Reword to "UQ-15 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `00-Engine-Core-Runtime/Startup-Data-Construction/generated-float-table-builders.md:468` · **BH-1** (ANSWERED) · "not established"
  - quote: `- **BH-1 moves from "not established" to "extractable".** A decoder over the 65 builders' immediate`
  - proposed: Reword to "BH-1 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "not established".

### 01-Script-VM-Native-Bridge

- `01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md:427` · **BF-1** (ANSWERED 2026-09-27 (FABLE, Claude Opus ) · "stays open"
  - quote: `read in full in §13. **That historical remaining-body count is not refreshed by Section11. BF-1 stays open:** the new`
  - proposed: Reword to "BF-1 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md:654` · **EF-2** (ANSWERED 2026-09-25 (FABLE, Claude Opus ) · "stays open"
  - quote: `*(Read by OPUS 2026-09-14. 'EF-2' stays open on the producer side and is narrowed on the reader`
  - proposed: Reword to "EF-2 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md:1062` · **BQ-7** (CLOSED) · "stays open"
  - quote: `is unusual, and each is a small, bounded read. **BQ-7** stays open on those four categories.`
  - proposed: Reword to "BQ-7 is closed (register)"; if a narrower residue remains, give it its own row id.

### 02-Resource-And-Asset-Pipeline

- `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md:571` · **AY-6** (ANSWERED) · "stays open"
  - quote: `not run through this function. **AY-6 stays open**, and **AY-7** is the new question: what`
  - proposed: Reword to "AY-6 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md:908` · **AG-2** (ANSWERED 2026-09-26 (FABLE, Claude Opus ) · "stays open"
  - quote: `> from. **AG-2 stays open**, now with a stated next step: name the 'battle_pack.bin' directory fields`
  - proposed: Reword to "AG-2 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".

### 05-Spawn-Encounter-Lifecycle

- `05-Spawn-Encounter-Lifecycle/CONTRACT-spawn-placement.md:107` · **L-7** (ANSWERED 2026-09-02 — nothing does at ge) · "unresolved"
  - quote: `and 'Z' are set; **what supplies the vertical coordinate is unresolved** and recorded as 'L-7'`
  - proposed: Reword to "L-7 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "unresolved".
- `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md:1655` · **L-13** (SUPERSEDED 2026-09-27 (OPUS) under FRONT) · "remains open"
  - quote: `or prove which tick/current-bank state an actual load reaches. L-13 remains open at that`
  - proposed: Reword to say L-13 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.
- `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md:1956` · **F-3** (ANSWERED 2026-09-13 (FABLE)) · "pending"
  - quote: `byte. This answers the local guard portion of weather question **F-3**, pending its owner's`
  - proposed: Reword to "F-3 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "pending".
- `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md:1987` · **L-13** (SUPERSEDED 2026-09-27 (OPUS) under FRONT) · "stays open"
  - quote: `**L-13 stays open:** actual save completion to field request, intervening flag writers and`
  - proposed: Reword to say L-13 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.
- `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md:2171` · **L-13** (SUPERSEDED 2026-09-27 (OPUS) under FRONT) · "remains open"
  - quote: `**L-13 remains open.** If the area controller and load controller belong to one destroyed`
  - proposed: Reword to say L-13 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.
- `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md:2321` · **L-13** (SUPERSEDED 2026-09-27 (OPUS) under FRONT) · "stays open"
  - quote: `**L-13 stays open.** Native root initialization and explicit attach/completion routes are`
  - proposed: Reword to say L-13 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.
- `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md:3538` · **L-13** (SUPERSEDED 2026-09-27 (OPUS) under FRONT) · "remains open"
  - quote: `L-13 remains open for current-to-old session reuse, initialized nonzero banks,`
  - proposed: Reword to say L-13 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.

### 06-Movement-And-Navigation

- `06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md:143` · **DP-2** (SUPERSEDED 2026-09-26 (FABLE, Claude Opu) · "not established"
  - quote: `> player can see it is not established.** 'DP-2'.`
  - proposed: Reword to say DP-2 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.

### 07-Combat-Action

- `07-Combat-Action/Action-Dispatch/battle-action-handler-table.md:668` · **AT-8** (ANSWERED by reference 2026-09-14 (FABLE)) · "remains open"
  - quote: `- **Not what lies above id 542.** 'AT-8' remains open on the contents of the space; this adds that the`
  - proposed: Reword to "AT-8 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "remains open".
- `07-Combat-Action/CONTRACT-native-command-seam.md:253` · **CS-4** (ANSWERED 2026-09-12 (FABLE)) · "not read"
  - quote: `**Audio — SERVICE (1 edge).** The presentation-ring drain '00313DB0' ends by calling '002DEE70', a 13-byte trampoline that jumps into the audio layer's sound-command dispatcher with the fixed argumen…`
  - proposed: Reword to "CS-4 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "not read".
- `07-Combat-Action/CONTRACT-native-command-seam.md:255` · **CS-2** (ANSWERED 2026-09-12 (FABLE)) · "pending"
  - quote: `**CombatAI — CLIENT and SERVICE (3 edges).** 'BattleUnit_SelectAndCommitNextAction' '00305AB0' and 'BattleUnit_TrySelectAndCommitAiOrderFromSet' '00305CC0' call the commit funnel '0030F760', and the …`
  - proposed: Reword to "CS-2 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "pending".
- `07-Combat-Action/Command-And-Action-Seam/native-command-seam.md:256` · **AH-6** (CLOSED 2026-09-02) · "stays open"
  - quote: `re-derived. **AH-6 stays open**, which is the correct state - a stamp records verification, and`
  - proposed: Reword to "AH-6 is closed (register)"; if a narrower residue remains, give it its own row id.

### 08-Combat-Formula

- `08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md:496` · **FT-4** (ANSWERED) · "remains open"
  - quote: `not re-derived, and 'FT-4' remains open.`
  - proposed: Reword to "FT-4 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "remains open".

### 09-Combat-AI-And-Gambits

- `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md:1761` · **Z-2** (ANSWERED 2026-09-17 (FABLE): the 24 byte) · "not established"
  - quote: `still not established"*, leaving Z-2 open on the layout. They are established here, from **two`
  - proposed: Reword to "Z-2 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "not established".

### 10-Status-Periodic-Terminal

- `10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md:626` · **EY-1** (ANSWERED) · "remains open"
  - quote: `says. 'EY-1' remains open.`
  - proposed: Reword to "EY-1 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "remains open".

### 14-Story-Event-Quest-Hunt

- `14-Story-Event-Quest-Hunt/persistent-flag-banks.md:651` · **AA-2** (ANSWERED 2026-09-26 (FABLE, Claude Opus ) · "stays OPEN"
  - quote: `flags or that 'Bank64A' holds "hunts".** Those labels remain unproven, and **AA-2 stays OPEN** with`
  - proposed: Reword to "AA-2 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays OPEN".

### 15-Input

- `15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md:1017` · **UQ-146** (SUPERSEDED 2026-09-27 (FABLE, Claude Opu) · "stays open"
  - quote: `access was observed, and the dangling return's lifetime is untouched. 'UQ-146' stays open on exactly the`
  - proposed: Reword to say UQ-146 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.
- `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md:35` · **SD-5** (ANSWERED 2026-09-30 (OPUS `ce2b4380d`, s) · "stays open"
  - quote: `channel builders, the bridge and the keyboard path are read (§2, §5). What stays open is registered as SD-5 to`
  - proposed: Reword to "SD-5 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md:553` · **SD-5** (ANSWERED 2026-09-30 (OPUS `ce2b4380d`, s) · "stays open"
  - quote: `and the '0x80' neutral AP-2 (a literal at '008F3A2C'), §5. What stays open is SD-5 to SD-9.)* *(Pointer 2026-10-01`
  - proposed: Reword to "SD-5 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".

### 16-UI

- `16-UI/CONTRACT-ui-request-router.md:228` · **R-4** (ANSWERED) · "not read"
  - quote: `- **What '003F4E70' does with the latch.** It is the third reader in R-4 and was not read.`
  - proposed: Reword to "R-4 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "not read".
- `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md:688` · **Y-2** (ANSWERED 2026-09-20 (SWE2-DATA)) · "stays open"
  - quote: `**Y-2 stays open**, with the convention split recorded as a lead: when comparing schema names to data`
  - proposed: Reword to "Y-2 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md:995` · **UQ-156** (ANSWERED) · "Still open"
  - quote: `- *Still open on UQ-156:* the meaning of container '+0x179D2' bits 9–11, the reopen after a link, and what`
  - proposed: Reword to "UQ-156 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "Still open".
- `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md:1036` · **UQ-156** (ANSWERED) · "Still open"
  - quote: `- *Still open on UQ-156:* what each page draws (arm 4's callees), what '003C1DF0' and '003BD890' do, and who`
  - proposed: Reword to "UQ-156 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "Still open".
- `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md:1055` · **UQ-156** (ANSWERED) · "Still open"
  - quote: `- *Still open on UQ-156:* what each page draws (arm 4's callees), and the container's lifetime (who destroys`
  - proposed: Reword to "UQ-156 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "Still open".
- `16-UI/Widget-Object-Model/a-512-byte-widget-that-registers-itself-once.md:299` · **EJ-1** (ANSWERED 2026-09-14 (FABLE): the invento) · "stays open"
  - quote: `**Not claimed.** What the widget *is* — 'EJ-1' stays open, now with eight unread arms rather than`
  - proposed: Reword to "EJ-1 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `16-UI/Widget-Object-Model/the-widget-message-protocol.md:677` · **GG-3** (ANSWERED 2026-09-25 (FABLE, Claude Opus ) · "pending"
  - quote: `**Why this was re-run.** A pending answer to the input contract's 'GG-3' described '00248030' in three`
  - proposed: Reword to "GG-3 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "pending".
- `16-UI/Widget-Object-Model/the-widget-message-protocol.md:1363` · **DL-1** (ANSWERED 2026-09-25 (FABLE, Claude Opus ) · "stays open"
  - quote: `'DL-1' stays open for the three, each with a named next step rather than a blank.`
  - proposed: Reword to "DL-1 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".

### 17-Presentation-Rendering

- `17-Presentation-Rendering/Character-Render-Records/the-bone-trails.md:259` · **UQ-213** (ANSWERED 2026-09-27 (FABLE, Claude Opus ) · "stays open"
  - quote: `*The bounded read §5b set up. It does not name the GS registers, so 'UQ-213' stays open; what it adds is the`
  - proposed: Reword to "UQ-213 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `17-Presentation-Rendering/Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md:269` · **GI-9** (ANSWERED 2026-09-29 (FABLE, Claude Opus ) · "remains open"
  - quote: `*Nothing of GI-9 remains open (2026-09-29): the last item, what '0xD0''s blend selector produces on screen, is`
  - proposed: Reword to "GI-9 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "remains open".
- `17-Presentation-Rendering/Effect-File-Formats/the-element-types-60-74.md:299` · **GI-10** (ANSWERED 2026-09-29 (FABLE, Claude Opus ) · "remains open"
  - quote: `*Nothing of GI-10 remains open (2026-09-29). The coverage limit on names above is not a residue: no ability-keyed`
  - proposed: Reword to "GI-10 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "remains open".
- `17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md:842` · **BG-11** (ANSWERED 2026-09-22 (FABLE), page §20.) · "stays open"
  - quote: `> **BG-11 stays open with its sharpened question recorded**, so it is cheap to resume for anyone who`
  - proposed: Reword to "BG-11 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md:842` · **UQ-384** (ANSWERED 2026-09-30 (SWE2-STRUCT for OPU) · "is open"
  - quote: `class behind '[01FC35F8]', and the state handlers' stores. *(Marker normalised 2026-09-30 (FABLE, [record](../../_index/candidates/qid-marker-truth-fable-0930/README.md)): the box named no row; its r…`
  - proposed: Reword to "UQ-384 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "is open".
- `17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md:147` · **SD-141** (ANSWERED 2026-10-01 (OPUS, static; recor) · "are open"
  - quote: `instruction reads (['rrp_checks.py'](../../_index/candidates/dd-data-4-0930/rrp_checks.py) F1, F2). Who consumes them is 'SD-141'.)* ~~*('SD-141' answered 2026-09-30, OPUS, [record](../../_index/cand…`
  - proposed: Reword to "SD-141 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "are open".

### 18-Audio

- `18-Audio/Audio-Boundary/CONTRACT-sound-request.md:95` · **SR-2** (NO ADMISSIBLE SOURCE (FABLE 2026-09-14, ) · "still open"
  - quote: `> 'SR-2', and it is still open.`
  - proposed: Reword to "SR-2 has no admissible source / is out of the evidence boundary (register)" instead of "still open".
- `18-Audio/Audio-Boundary/how-a-sound-fades-the-ramp-and-its-six-curves.md:144` · **DQ-1** (ANSWERED 2026-09-14 (FABLE): no — the ad) · "not read"
  - quote: `'elapsed', which this document did not read.** 'DQ-1'.`
  - proposed: Reword to "DQ-1 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "not read".
- `18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md:70` · **AS-2** (ANSWERED 2026-09-22 (FABLE)) · "still open"
  - quote: `§1 calls the 'shout' banks *“the battle voice clips”*, and the register carried 'AS-2' as still open`
  - proposed: Reword to "AS-2 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "still open".
- `18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md:378` · **UQ-255** (ANSWERED 2026-09-27 (SWE2-DATA, `SWE2-DA) · "stays open"
  - quote: `half, what the 'u32' and 'u8' MEAN, is untouched by this and stays open as 'UQ-255'.*`
  - proposed: Reword to "UQ-255 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".

### 19-Save-Load-Settings

- `19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md:322` · **EO-1** (ANSWERED 2026-09-26 (FABLE, Claude Opus ) · "unresolved"
  - quote: `the tables are initialised”*; what the field holds before that is **unresolved**, 'EO-1'.`
  - proposed: Reword to "EO-1 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "unresolved".
- `19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md:277` · **AU-5** (ANSWERED - it is `DecideButton` in GameS) · "still open"
  - quote: `(**AU-5**, still open). It converts one lead into a finding and leaves the rest labelled.`
  - proposed: Reword to "AU-5 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "still open".
- `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md:632` · **V-9** (ANSWERED 2026-09-13 (FABLE): compressed,) · "stays open"
  - quote: `it actually is stays open as **V-9**. *(Answered in the next section, 2026-09-13.)*`
  - proposed: Reword to "V-9 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md:795` · **AB-5** (ANSWERED 2026-09-10 (FABLE)) · "stays OPEN"
  - quote: `**AB-5 stays OPEN**, now with a recorded reason: a pointer-propagation-aware analysis is required,`
  - proposed: Reword to "AB-5 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays OPEN".

### 21-RNG-And-Determinism

- `21-RNG-And-Determinism/rng-streams.md:720` · **CQ-5** (ANSWERED 2026-09-14 (OPUS) — YES, and th) · "remains open"
  - quote: `whether the presentation stream is inlined remains open as 'CQ-5'.`
  - proposed: Reword to "CQ-5 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "remains open".

### 22-Middleware-PhyreEngine

- `22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md:627` · **BA-1** (OUT OF EVIDENCE BOUNDARY for the residue) · "is open"
  - quote: `here rests on one. This is open question **BA-1**.`
  - proposed: Reword to "BA-1 has no admissible source / is out of the evidence boundary (register)" instead of "is open".
- `22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md:458` · **UQ-289** (SUPERSEDED 2026-09-26 (FABLE, Claude Opu) · "stays open"
  - quote: `members (458 B). 'UQ-289' stays open on those 30.`
  - proposed: Reword to say UQ-289 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.
- `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md:1031` · **BL-1** (OUT OF EVIDENCE BOUNDARY (FABLE 2026-09-) · "unresolved"
  - quote: `takes all three values. Filed as BL-1 unresolved rather than softened into a plausible sentence.`
  - proposed: Reword to "BL-1 has no admissible source / is out of the evidence boundary (register)" instead of "unresolved".
- `22-Middleware-PhyreEngine/Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md:832` · **UQ-289** (SUPERSEDED 2026-09-26 (FABLE, Claude Opu) · "stays open"
  - quote: `'UQ-289' stays open on those 30.`
  - proposed: Reword to say UQ-289 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.
- `22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md:1112` · **BA-1** (OUT OF EVIDENCE BOUNDARY for the residue) · "stays open"
  - quote: `**Not claimed:** nothing here was executed or observed live; 'BA-1' stays open, and the thread and`
  - proposed: Reword to "BA-1 has no admissible source / is out of the evidence boundary (register)" instead of "stays open".

### 23-Third-Party-Libraries

- `23-Third-Party-Libraries/Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md:487` · **B-1** (SUPERSEDED 2026-09-26 (FABLE, Claude Opu) · "is open"
  - quote: `mechanism identities. This is open question **B-1** work.`
  - proposed: Reword to say B-1 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.
- `23-Third-Party-Libraries/Lua-Core/CONTRACT-lua-chunk-loader.md:361` · **DA-1** (SUPERSEDED 2026-09-26 (FABLE, Claude Opu) · "still open"
  - quote: `need a breakpoint or a trace, which 'F-3' lists as not built. **That is why 'DA-1' is still open, and`
  - proposed: Reword to say DA-1 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.
- `23-Third-Party-Libraries/Lua-Core/CONTRACT-lua-chunk-loader.md:449` · **DA-1** (SUPERSEDED 2026-09-26 (FABLE, Claude Opu) · "stays open"
  - quote: `**Not claimed:** no runtime observation; 'DA-1' stays open.`
  - proposed: Reword to say DA-1 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.
- `23-Third-Party-Libraries/Lua-Core/the-lua-loader-and-what-it-accepts.md:247` · **DA-1** (SUPERSEDED 2026-09-26 (FABLE, Claude Opu) · "not read"
  - quote: `'00684F60' is a **third** call site not named by 'DA-1''s four-executor set, and is not read here.`
  - proposed: Reword to say DA-1 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.
- `23-Third-Party-Libraries/Lua-Core/the-lua-loader-and-what-it-accepts.md:414` · **UQ-312** (SUPERSEDED 2026-09-26 (FABLE, Claude Opu) · "stays open"
  - quote: `at run time is 'UQ-312''s question, which stays open.`
  - proposed: Reword to say UQ-312 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.
- `23-Third-Party-Libraries/third-party-middleware-inventory.md:1000` · **X-8** (OUT OF EVIDENCE BOUNDARY for the one res) · "stays open"
  - quote: `run of ≥6 bytes was scanned and matched against each library's markers. **X-8 stays open for those`
  - proposed: Reword to "X-8 has no admissible source / is out of the evidence boundary (register)" instead of "stays open".

### 24-Compiler-And-CRT-Runtime

- `24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md:110` · **T-9** (ANSWERED 2026-09-27 (FABLE, Claude Opus ) · "stays open"
  - quote: `> **Why 'T-9' stays open, now for a proven reason rather than an assumed one.** Its narrowing says`
  - proposed: Reword to "T-9 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md:440` · **S-2** (ANSWERED 2026-09-26 (FABLE, Claude Opus ) · "stays open"
  - quote: `> switch spelling is toolchain knowledge this image cannot settle alone**, so 'S-2' stays open; what`
  - proposed: Reword to "S-2 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md:830` · **BQ-27** (ANSWERED 2026-09-28 (SWE2-FRONTIER rulin) · "stays open"
  - quote: `*(Read by OPUS 2026-09-14. 'BQ-27' stays open on the 345. What changes is that "static reading`
  - proposed: Reword to "BQ-27 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md:546` · **OC-4** (ANSWERED 2026-09-15 (FABLE) — all 99 enu) · "not read"
  - quote: `The subsystem attribution of the 99 callers (OC-4 counts them and this pass did not read them);`
  - proposed: Reword to "OC-4 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "not read".

### 25-EBP-Script-Container

- `25-EBP-Script-Container/Sections/section-019.md:317` · **CD-2** (SUPERSEDED 2026-09-27 (FABLE, Claude Opu) · "stays open"
  - quote: `> reason it is unlikely to change, not evidence that it does not. 'CD-2' stays open for the write`
  - proposed: Reword to say CD-2 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.

### 99-Unresolved-Residual

- `99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md:1485` · **UQ-347** (ANSWERED 2026-09-18 (FABLE): it is a VIF) · "not read"
  - quote: `command words mean to the render thread is UQ-347's territory and is not read here.`
  - proposed: Reword to "UQ-347 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "not read".
- `99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md:933` · **UQ-367** (SUPERSEDED 2026-09-26 (FABLE, Claude Opu) · "stays open"
  - quote: `**What this resolves and what stays open.** 'UQ-367''s narrowed producer question is`
  - proposed: Reword to say UQ-367 is SUPERSEDED (register) and name the live successor row; or strike the open claim and keep it as dated history.
- `99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md:187` · **BI-1** (ANSWERED - it is the render-model SUBRES) · "still unknown"
  - quote: `found. **What it DOES is still unknown.** **BI-1.**`
  - proposed: Reword to "BI-1 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "still unknown".
- `99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md:535` · **BI-8** (ANSWERED 2026-09-14 (FABLE): the per-man) · "stays open"
  - quote: `handler; neither has been followed. **BI-8** stays open with a defined shape.`
  - proposed: Reword to "BI-8 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "stays open".
- `99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md:680` · **BI-8** (ANSWERED 2026-09-14 (FABLE): the per-man) · "still unknown"
  - quote: `**What the buckets hold is still unknown.** This does not answer BI-8; it confirms the mechanism and`
  - proposed: Reword to "BI-8 is ANSWERED (register)"; if a residue remains, register it under a new row id and cite that id instead of "still unknown".

## (c) Checkboxes

No findings. Every `- [ ]` box whose own id is a closed row, and every `- [x]` box whose own id is an OPEN/IN PROGRESS/BLOCKED row, was looked for across all 530 pages; none exist outside struck text. (`experience-and-license-point-award.md:225` is unticked on GR-18, which is PARTIAL, so consistent.)

## (d) "Pending review" where a review record exists

- `02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md:177` — **RC-37** · record: auditspec-review-rc37-0930 — ACCEPT; row ANSWERED
  - quote: `ate 2, and in state 3 it completes on the status slot '0215EFF4' the previous read left (OPUS 2026-09-30, RC-37, '_index/candidates/rc37-refused-read-0930/', static; pending SWE2-AUDIT-SPEC review). …`
  - proposed: …static; reviewed ACCEPT by SWE2-AUDIT-SPEC, auditspec-review-rc37-0930).
- `13-Rewards-Progression-Economy/CONTRACT-defeat-rewards-sequence.md:30` — **GR-16 (SECTION-03)** · record: auditsem-review-section03-1001 — ACCEPT-WITH-NARROWING; row ANSWERED 2026-10-01
  - quote: `status: locally validated; peer acceptance pending`
  - proposed: Replace "independent peer acceptance pending" with "independent review ACCEPT-WITH-NARROWING 2026-10-01 (SWE2-AUDIT-SEM, auditsem-review-section03-1001, GR-16; narrowing N1)".
- `13-Rewards-Progression-Economy/CONTRACT-defeat-rewards-sequence.md:38` — **GR-16 (SECTION-03)** · record: auditsem-review-section03-1001 — ACCEPT-WITH-NARROWING; row ANSWERED 2026-10-01
  - quote: `> **SECTION-03 production review, 2026-09-22; independent peer acceptance pending.**`
  - proposed: Replace "independent peer acceptance pending" with "independent review ACCEPT-WITH-NARROWING 2026-10-01 (SWE2-AUDIT-SEM, auditsem-review-section03-1001, GR-16; narrowing N1)".
- `13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md:27` — **GR-16 (SECTION-03)** · record: auditsem-review-section03-1001 — ACCEPT-WITH-NARROWING; row ANSWERED 2026-10-01
  - quote: `status: "PRODUCTION COMPLETE; formal peer acceptance pending"`
  - proposed: Replace "independent peer acceptance pending" with "independent review ACCEPT-WITH-NARROWING 2026-10-01 (SWE2-AUDIT-SEM, auditsem-review-section03-1001, GR-16; narrowing N1)".
- `13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md:299` — **GR-16 (SECTION-03)** · record: auditsem-review-section03-1001 — ACCEPT-WITH-NARROWING; row ANSWERED 2026-10-01
  - quote: `production corrections and leaves formal peer acceptance pending.`
  - proposed: Replace "independent peer acceptance pending" with "independent review ACCEPT-WITH-NARROWING 2026-10-01 (SWE2-AUDIT-SEM, auditsem-review-section03-1001, GR-16; narrowing N1)".
- `13-Rewards-Progression-Economy/experience-and-license-point-award.md:27` — **GR-16 (SECTION-03)** · record: auditsem-review-section03-1001 — ACCEPT-WITH-NARROWING; row ANSWERED 2026-10-01
  - quote: `status: locally validated; peer acceptance pending`
  - proposed: Replace "independent peer acceptance pending" with "independent review ACCEPT-WITH-NARROWING 2026-10-01 (SWE2-AUDIT-SEM, auditsem-review-section03-1001, GR-16; narrowing N1)".
- `13-Rewards-Progression-Economy/experience-and-license-point-award.md:35` — **GR-16 (SECTION-03)** · record: auditsem-review-section03-1001 — ACCEPT-WITH-NARROWING; row ANSWERED 2026-10-01
  - quote: `> **SECTION-03 production review, 2026-09-22; independent peer acceptance pending** (registered as GR-16, 2026-09-30).`
  - proposed: Replace "independent peer acceptance pending" with "independent review ACCEPT-WITH-NARROWING 2026-10-01 (SWE2-AUDIT-SEM, auditsem-review-section03-1001, GR-16; narrowing N1)".
- `13-Rewards-Progression-Economy/how-experience-is-computed-and-divided.md:30` — **GR-16 (SECTION-03)** · record: auditsem-review-section03-1001 — ACCEPT-WITH-NARROWING; row ANSWERED 2026-10-01
  - quote: `status: locally validated; peer acceptance pending`
  - proposed: Replace "independent peer acceptance pending" with "independent review ACCEPT-WITH-NARROWING 2026-10-01 (SWE2-AUDIT-SEM, auditsem-review-section03-1001, GR-16; narrowing N1)".
- `13-Rewards-Progression-Economy/how-experience-is-computed-and-divided.md:38` — **GR-16 (SECTION-03)** · record: auditsem-review-section03-1001 — ACCEPT-WITH-NARROWING; row ANSWERED 2026-10-01
  - quote: `> **SECTION-03 production review, 2026-09-22; independent peer acceptance pending** (registered as GR-16, 2026-09-30).`
  - proposed: Replace "independent peer acceptance pending" with "independent review ACCEPT-WITH-NARROWING 2026-10-01 (SWE2-AUDIT-SEM, auditsem-review-section03-1001, GR-16; narrowing N1)".
- `13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md:38` — **GR-16 (SECTION-03)** · record: auditsem-review-section03-1001 — ACCEPT-WITH-NARROWING; row ANSWERED 2026-10-01
  - quote: `> **SECTION-03 production review, 2026-09-22; independent peer acceptance pending** (registered as GR-16, 2026-09-30).`
  - proposed: Replace "independent peer acceptance pending" with "independent review ACCEPT-WITH-NARROWING 2026-10-01 (SWE2-AUDIT-SEM, auditsem-review-section03-1001, GR-16; narrowing N1)".

### Possible, not counted (record only names the page or section; needs a read)

Front-matter lines reading "locally validated; formal independent acceptance pending" sit on pages that some `auditspec-review-*` / `auditsem-review-*` record mentions by file name (for example `auditspec-review-section02-0930`, `auditspec-review-ddres-b6-0930`, `auditspec-review-dd-02-b2-0930`, `auditspec-review-dd-02-restatus-0930`, `auditsem-review-p22-b2-b7-0930`). I could not tell from the text whether each record accepts that page. Pages: `02-Resource-And-Asset-Pipeline/` CONTRACT-resource-request-queue.md:21,26; the-resource-request-queue.md:28; resource-section-addressing.md:28 (line 155 already says it is superseded); the-source-block-mover-and-separate-consumer-refresh.md:13; the-nonempty-prf-registration-and-specialized-relocation.md:20; the-resource-owner-from-copy-or-borrow-to-disposal.md:21. Proposed wording if a local read confirms: cite the review record and its verdict in place of "pending".

## Needs local check

- Whether each (b) "stays open" sentence is a real residue that deserves its own row, or a stale restatement. Needs reading the page body and, for exe claims, the executable.
- GR-16 closure is "ACCEPT-WITH-NARROWING"; whether pages should say accepted or accepted-with-narrowing, and whether REOPENED status on `how-experience-is-computed-and-divided.md` should change, is an owner decision.
- Sixteen pages carry "pending first review" (e.g. `07-Combat-Action/how-close-a-unit-must-stand-to-act.md:22`, `15-Input/how-a-gamepad-becomes-a-controller-object.md:21`, `18-Audio/how-an-animation-makes-a-sound.md:23`, `19-Save-Load-Settings/how-a-manual-save-is-committed.md`). No review record under `_index/candidates/` names them, so they are not findings; confirm against the board.
- Nothing here was checked against game data.

