"""apply_17render_c.py [--apply] - 17-Presentation-Rendering readiness map (cloud-reports/re-readiness/17-render.md),
section 3.2 (counts and census figures, report lines 3212-3385) and section 3.3 (stale "open / not read" claims,
corrected claims repeated unstruck, banner disagreements; lines 3385-3751), part C, settled at the shipping image, at
the shipped data (the extracted archive) and in the cited TSVs (OPUS, 2026-10-02).

Each count edit strikes the figure the image, the shipped data or the cited TSV REFUTES and restates it, tagged
*(corrected 2026-10-02, OPUS: ...)* with the recount method; where two figures measure different scopes the edit names
the scope instead of striking either. Each stale "not read / open" claim is struck and pointed at the place that
answers it, tagged *(answered: see ...; 2026-10-02, OPUS)*. Banner edits restate an in-body or README status to the
page's own front-matter word, never above it. Every deciding address inside a function is cited as entry+offset.
The verdict table is scratchpad re17c/verdicts-17c.md (copied into consumer-check.md when this candidate is published).
Items decided with no page wrong, left undecided, or whose line part A or part B already edits carry no edit (listed
in the verdict table). Front-matter audit blocks and multi-line YAML notes are not edited (audit tools own them);
README coverage gaps (pages with no README entry) are routed, not added. No census TSV is edited: the stale generated
TSVs are routed as regenerate requests (vif1-gif-tags.tsv to FABLE; character-render-record-accesses.tsv to
SWE2-STRUCT).
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` comment in the block's comment syntax instead of a strike (their OLD
includes the line end, so NEW never contains OLD); the one front-matter edit is a trailing `# <- corrected` comment on
a single-line value. Changed headings name OPUS.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "17-Presentation-Rendering/"
RM = F + "README.md"
ACH = F + "Authored-Commands/the-authored-presentation-command-handlers.md"
RAMP = F + "CONTRACT-authored-command-ramp-channels.md"
CDL = F + "CONTRACT-coast-down-latch.md"
POOL = F + "CONTRACT-render-record-pool-lifecycle.md"
CROC = F + "CONTRACT-character-render-object.md"
PUB = F + "CONTRACT-character-transform-publish.md"
CRO = F + "Character-Rendering/character-render-object.md"
LIT = F + "Character-Rendering/how-a-character-is-lit.md"
CRR = F + "Character-Render-Records/the-character-render-record-array.md"
RES = F + "Character-Render-Records/render-event-selection-evidence.md"
TRK = F + "Character-Render-Records/how-a-presentation-entry-picks-its-track.md"
FADE = F + "Character-Render-Records/how-a-character-fades-the-ten-channels.md"
STAT = F + "Character-Render-Records/how-a-status-shows-on-a-character.md"
TRAIL = F + "Character-Render-Records/the-bone-trails.md"
RIG = F + "Character-Render-Records/the-rig-of-seventeen-controllers.md"
LOOK = F + "Character-Render-Records/the-staged-look-command.md"
C = F + "CONTRACT-render-command-list-and-graphics-handshake.md"
L = F + "Render-Command-List/the-ordered-render-command-list.md"
H = F + "Graphics-Thread-Handshake/the-shared-command-state-word.md"
GI = F + "Gi-Render-Commands/gi-render-command-family.md"
VIF = F + "Legacy-PS2-GS/the-vif1-vu1-layer.md"
DISP = F + "Effect-File-Formats/effect-element-type-dispatch.md"
FBF = F + "Effect-File-Formats/an-effect-element-frame-by-frame.md"
EFX = F + "Effect-File-Formats/efx-and-efb-effect-containers.md"
ERM = F + "Effect-File-Formats/README.md"
MESH = F + "Effect-File-Formats/effect-mesh-records-kind-54.md"
E00 = F + "Effect-File-Formats/the-element-types-00-0a.md"
E60 = F + "Effect-File-Formats/the-element-types-60-74.md"
MENU = F + "Effect-File-Formats/the-menu-effect-registry.md"
SKEL = F + "Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md"
ADM = F + "Model-And-Motion-Formats/adm-add-motion-tables.md"
FCP = F + "Model-And-Motion-Formats/fcp-character-parameter-block.md"
FDM = F + "Model-And-Motion-Formats/fdm-and-for-entries.md"
MR = F + "Model-And-Motion-Formats/README.md"
FEF = F + "Model-And-Motion-Formats/fef-and-motion-entries.md"
FRP = F + "Model-And-Motion-Formats/frp-object-container.md"
FTE = F + "Model-And-Motion-Formats/fte-fct-texture-colour-tables.md"
OSC = F + "Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md"
POSE = F + "Model-And-Motion-Formats/the-pose-sequencer.md"
CS = F + "Post-Processing/CONTRACT-post-processing-subsystem.md"
CP = F + "Post-Processing/CONTRACT-ppfx-effect-creation.md"
PI = F + "Post-Processing/ppfx-function-identification.md"
CAT = F + "Post-Processing/the-post-processing-effect-catalogue.md"
VR = F + "Visual-Tuning-Parameters/README.md"
RR = F + "Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md"
MH = F + "Movie-Containers/mh-movie-seek-index.md"
PTS = F + "Position-To-Scalar/how-a-position-becomes-a-single-number.md"
SF = F + "Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md"
AF = F + "Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md"
CR = F + "Scripted-Camera/how-a-camera-reaches-the-renderer.md"
P = F + "Scripted-Camera/the-scripted-camera-player.md"

T = "*(corrected 2026-10-02, OPUS: "
A = "*(answered: see "
E = "; 2026-10-02, OPUS)*"
CC = "<- corrected 2026-10-02, OPUS - "
FM = "the page's front matter says "
NOT426 = ("`00426870`+0x33 `call rsi` applies the callback to the record at once and +0x4A `call 0042EF90` walks its "
          "children - this page's own 2026-09-20 correction, `00426870` defers nothing")
CTX = ("container `.ca` + `.cm` blocks (32,151); the all-block census of the authored-command page adds the 30,057 event "
       "`.mot` blocks")
SIZES = ("over all 36 builders the size is `0x18` x 15, `0x20` x 16, `0x28` x 3 and `0x30` x 2 (`0018B710`+0x37 and "
         "`0018B8B0`+0x2E `lea ecx, [rdx + 0x30]`), the last `ecx` write before each `call 0085E730`")
DFE = ("`001EDDC0`, the frame-rate switch, stores 2.0 to `01DFE0B8` (+0x18), 0.5 to `01DFE0BC` (+0x20) and 1 to "
       "`01F82E38` (+0x28) on its non-zero arm; the image holds 1.0, 1.0 and 0")

EDITS = [
    # ---------------------------------------------------------------- 3.2.1 [AC]
    # AC.CC-2 / MM.CC-6: the fef table's "uses" column counts the 32,151 container blocks; the handler page's
    # all-block figures add the event .mot blocks (recount of the extracted archive by file kind).
    (FEF, "`tabB[5]=00520C50`). Command lengths below are corpus-verified; operand\n",
     "`tabB[5]=00520C50`). Command lengths below are corpus-verified *(scope named 2026-10-02, OPUS: the `uses` column "
     "counts the " + CTX + " - e.g. `0x09` 78,455 here and 108,511 there, `0x13` 5,805 and 17,416, `0x16` 329 and 373; "
     "recount of the extracted archive by file kind)*; operand\n"),
    # AC.CC-4: four authored-command setters (two by jmp); the fifth channel's writer 003B5D40 is a direct call.
    (RAMP, "> **Two of the five setters are not in the function census**, and they are exactly the two reached by",
     "> **Two of the ~~five~~ four setters are not in the function census** " + T + "§2's four - `004173D0`+0x57 and "
     "`00417460`+0x57 call `003B6A90` / `003B6A10`, `00417440`+0x17 and `004174D0`+0x17 tail-jump to `003B69B0` / "
     "`003B6950`; the fifth channel's writer `003B5D40` is a direct call at `0041D560`+0x87, not a setter of this "
     "kind)*, and they are exactly the two reached by"),
    # AC.CS-2 / AC.CS-1: README status words against the pages' front matter.
    (RM, "  **PARTIAL, tier 1.** The **28-body `00520xxx` family**: authored presentation commands dispatched",
     "  ~~**PARTIAL, tier 1.**~~ **DOCUMENTED, tier 1.** " + T + FM + "`status: DOCUMENTED`, owner re-status "
     "2026-10-01)* "
     "The **28-body `00520xxx` family**: authored presentation commands dispatched"),
    (RM, "  **SPECIFIED, tier 1, not differentially tested.** 160 slot records",
     "  **SPECIFIED, tier 1, ~~not~~ differentially tested.** " + T + "the contract's front matter says `readiness: "
     "DIFFERENTIAL TESTED` - `diff_ramp_channels.py`, 483 commands, 0 mismatches)* 160 slot records"),
    # AC.CS-11: 00426870 defers nothing (README and handler page).
    (RM, "  `CharacterRenderSystem_Initialize` registrations instruction-exact, plus the deferred-work pair\n",
     "  `CharacterRenderSystem_Initialize` registrations instruction-exact, plus the ~~deferred-work~~ apply-and-recurse "
     "pair " + T + NOT426 + ")*\n"),
    (RM, "**Resource — SERVICE.** `00520E90` on this page — the posted deferred worker for the",
     "**Resource — SERVICE.** `00520E90` on this page — the ~~posted deferred worker~~ per-record callback `00426870` "
     "applies at once " + T + NOT426 + ")* for the"),
    (ACH, "it posts `00520E90` through the deferred-work poster `00426870`, re",
     "it ~~posts `00520E90` through the deferred-work poster `00426870`~~ applies `00520E90` at once through "
     "`00426870` " + T + NOT426 + ")*, re"),
    (ACH, "| `00520E90` | the posted callback | deferred worker: resolves",
     "| `00520E90` | the ~~posted~~ callback `00426870` applies | ~~deferred worker~~ per-record callback " + T +
     "`00426870` calls it at once, `00426870`+0x33)*: resolves"),
    (ACH, "`00426870` — the deferred-work poster — is called by",
     "`00426870` — ~~the deferred-work poster~~ the apply-and-recurse helper " + T + NOT426 + ")* — is called by"),
    (ACH, "lookup-and-bind commands, and the deferred resource-bind pair.",
     "lookup-and-bind commands, and the ~~deferred~~ resource-bind pair (applied at once through `00426870` " + T +
     "`00426870`+0x33 `call rsi`)*)."),
    # AC.CS-12: the two rows' counts are the container scope.
    (ACH, "`+0x290` bit 9 held as a re-entrancy guard; 5,805 authored, all three arms used |",
     "`+0x290` bit 9 held as a re-entrancy guard; 5,805 authored in the `.ca` containers *(scope named 2026-10-02, OPUS: "
     "17,416 in all 62,208 blocks, 11,611 of them in event blocks - the census section below)*, all three arms used |"),
    (ACH, "word `+4` the value; 329 authored, all `enable=1` / `value=0xFFFF` |",
     "word `+4` the value; 329 authored in the `.ca` containers *(scope named 2026-10-02, OPUS: 373 in all blocks, 44 "
     "of them in event blocks - the census section below)*, all `enable=1` / `value=0xFFFF` |"),
    # AC.CS-13: 00520800 writes +0x1C..+0x28 on the shadow object, not the render record.
    (ACH, "`003AFD30`/`003B6930`/`003AFC10`; `+0x1C`–`+0x28` state — **the shadow command**",
     "`003AFD30`/`003B6930`/`003AFC10`; ~~`+0x1C`–`+0x28` state~~ the shadow object's `+0x1C`... state " + T +
     "`00520800`+0x50 loads the record's `+0x118` handle, +0x5E `call 003AFC10` resolves the shadow slot, and the "
     "stores go through its result, e.g. +0xA8 `mov byte ptr [rdx + 0x1c], al`)* — **the shadow command**"),
    (ACH, "`+0x1C`–`+0x28` block. Four of the classes",
     "~~`+0x1C`–`+0x28` block~~ shadow object's `+0x1C`... block, not the record's " + T + "`00520800`+0x5E `call "
     "003AFC10`, then stores through its result)*. Four of the classes"),
    # AC.CS-4..8 (ramp contract).
    (RAMP, "      unnamed. **The record's other 0x60 bytes are unread.**",
     "      unnamed. ~~**The record's other 0x60 bytes are unread.**~~ " + A + "§14 item 5, mostly mapped 2026-09-20" + E),
    (RAMP, "      channel drives stays open, because the shadow draw that consumes the floats is unread on both pages.",
     "      channel drives ~~stays open, because the shadow draw that consumes the floats is unread on both pages~~ "
     + A + "the consumer read just below and §14 item 1, resolved 2026-09-20" + E + "."),
    (RAMP, "zero it. What consumes the weight is\n      unread, as UG-1 is.",
     "zero it. ~~What consumes the weight is~~\n      ~~unread, as UG-1 is.~~ " + A + "the `+0x43` / `+0x98` row of UQ-191's consumer table above - "
     "`003B62D0` eases it through LUT row 5 and blends toward the snapshot, consumer read 2026-09-20" + E),
    (RAMP, "      - **Not established:** what `00358290`, `00181DD0` and `002E05C0` test (they gate the call, not the step); what the",
     "      - **Not established:** ~~what `00358290`, `00181DD0` and `002E05C0` test (they gate the call, not the step);~~ "
     + A + "§14 item 3, all three read 2026-09-20" + E + " what the"),
    (RAMP, "floats — are not in this harness; `TIMING` in the parity sense",
     "floats — are not in this harness " + A + "the `EXP-108` section below, which runs `003B6020` and `003B62D0` from "
     "shipped bytes" + E + "; `TIMING` in the parity sense"),
    # AC.CS-9 / AC.CS-10 / AC.CS-14 (coast-down latch).
    (CDL, "- **`0020E600` and `0051B9E0` are supplied**, so the tail's *decision* is established and those two\n"
          "  functions are not.",
     "- **`0020E600` and `0051B9E0` are supplied**, so the tail's *decision* is established ~~and those two~~\n"
     "  ~~functions are not~~ " + A + "§7a and §15a - both read 2026-09-13; supplying them here is a harness choice" + E
     + "."),
    (CDL, "3. **What `0020E600` and `0051B9E0` are**, which is static work rather than live, and out of this",
     "3. ~~**What `0020E600` and `0051B9E0` are**~~ " + A + "§7a - `0020E600` is `ImageAddress_ResolveRuntimePointer`, "
     "`0051B9E0` a tail jump to `0051F240`" + E + ", which is static work rather than live, and out of this"),
    (CDL, "The document lists the first three. All five, in",
     "~~The document lists the first three.~~ " + A + "the record-array page, which now lists all five" + E + " All five, in"),
    (CDL, "coast-down latch, exactly\" — which this formalises, and whose arming list is three of the five.",
     "coast-down latch, exactly\" — which this formalises, and whose arming list is ~~three of the five~~ all five " + A +
     "the record-array page's latch section" + E + "."),
    (CDL, "entry path, outside this transition.",
     "entry path, ~~outside this transition~~ the fourth stage of this transition " + A + "§7a, added 2026-09-11 - it runs "
     "on every path except servicing" + E + "."),

    # ---------------------------------------------------------------- 3.2.2 / 3.3.2 [RO]
    # RO.CC-1: the census sentence is the 2026-09-16 generation; the TSV now holds a later one.
    (CRO, "writes/clears consistent with a reset. The census is now 160 rows in 31 functions over 69 distinct",
     "writes/clears consistent with a reset. The census ~~is now~~ was then 160 rows *(the TSV now holds 323 rows in 41 "
     "functions over 91 offsets - the later `emit_seeded_census.py` generation; recount of "
     "`character-render-object-accesses.tsv` 2026-10-02, OPUS)* in 31 functions over 69 distinct"),
    # RO.CC-7: the 14-access figure is the receiver census's reach; image-wide there are 19 byte accesses.
    (CRO, "      **the same 14 accesses, 1 write and 13 reads**, so that count now has a second instrument",
     "      **the same 14 accesses, 1 write and 13 reads** *(scope named 2026-10-02, OPUS: within that census's reach; "
     "image-wide the byte accesses at `+0x4B4` are 19 - two writes, `001F4DA0`+0x129 and `001F6E70`+0x8B9, and 17 reads "
     "in 16 functions, all in the class's bodies; CONTRACT-character-render-object.md R-3 / R-4)*, so that count now has "
     "a second instrument"),
    # RO.CS-1 / README: CRO status and the writer / reader counts.
    (CRO, "**Status unchanged at `DOCUMENTED`.** This is a separation check",
     "**Status unchanged at `DOCUMENTED`** *(on 2026-09-02; " + FM + "`status: AUDITED` now - 2026-10-02, OPUS)*. "
     "This is a separation check"),
    (RM, "  **DOCUMENTED, tier 1.** The **1,640-byte object that draws a character**: a complete\n"
         "  31-slot vtable, one construction site, and a **ready flag at `+0x4B4`** with one writer\n"
         "  at the end of setup and twelve readers at method entry.",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + T + FM + "`status: AUDITED`)* The **1,640-byte object that "
     "draws a character**: a complete\n"
     "  31-slot vtable, one construction site, and a **ready flag at `+0x4B4`** with ~~one writer~~ two byte writers, "
     "the constructor's clear and the set\n"
     "  at the end of setup, and ~~twelve readers at method entry~~ seventeen byte reads in sixteen functions, thirteen "
     "of them gating at entry " + T + "`001F4DA0`+0x129 and `001F6E70`+0x8B9 write it; vtable slots 3, 8, 9, 10, 12, 13, "
     "14, 16, 19, 20, 24, 27 and 30 read it; CONTRACT-character-render-object.md R-3 / R-4)*."),
    (CRO, "submission loop. Until it is set, update, submit, material propagation and transform propagation",
     "submission loop. Until it is set, update, submit~~, material propagation and transform propagation~~ and material "
     "propagation " + T + "slot 26 `001FAA10`, transform propagation, never reads `+0x4B4`; §5's 2026-09-27 note)*"),
    (CRO, "  clear, twelve of the class's methods return at their first branch and no amount of correct",
     "  clear, ~~twelve of the class's methods return at their first branch~~ eleven of the class's vtable methods and "
     "two non-virtual helpers gate on it at entry " + T + "slots 3, 8, 9, 10, 12, 13, 14, 19, 20, 24 and 30, plus "
     "`001F89E0` and `001FAD50`; slot 16 reads it late and slot 27 returns it; CONTRACT-character-render-object.md R-4)* "
     "and no amount of correct"),
    (CRO, "method — the end of setup — and **all 12 methods that read it do so within their first 12",
     "method — the end of setup — and " + T + "thirteen vtable methods read it, and slot 16 only at its instruction "
     "118 - §8c's overturns)* **all ~~12~~ 13 methods that read it, all but slot 16, do so within their first 12"),
    (CRO, "  the bone palette a weapon hangs from. Neither has been read; both are named only.",
     "  the bone palette a weapon hangs from. ~~Neither has been read; both are named only.~~ " + A + "§1's 2026-09-27 "
     "correction - slot 24 is read and writes the four refraction parameters, not a tint" + E),
    (CRO, "**The ordering within a frame is not established** — the guard tells you",
     "~~**The ordering within a frame is not established**~~ " + A + "§7, BB-3 answered 2026-09-26 - the render record's "
     "draw fixes the order" + E + " — the guard tells you"),
    (CRO, "      - the pooled element's `3` (a likely expiry count) is not followed here.",
     "      - the pooled element's `3` (a likely expiry count) ~~is not followed here~~ " + A + "the slot-3 bullet above - "
     "the pool's per-frame update calls slot 3 when that three-frame countdown ends" + E + "."),
    (CRO, "call**. No rendering API call has been traced out of these methods, and the",
     "call**. ~~No rendering API call has been traced out of these methods~~ " + A + "§7, BB-1 answered 2026-09-27 - "
     "the class draws through `001F5D70`, reached by slot 1 `00215320`+0x4 `jmp`, which calls Phyre's submit at "
     "`001F5D70`+0x1C8 `call 0060B980`" + E + ", and the"),
    (CRO, "anything currently supporting **BB-1**, this document's standing admission that no draw call has\n"
          "been traced out of these methods.",
     "anything currently supporting **BB-1**, ~~this document's standing admission that no draw call has~~\n"
     "~~been traced out of these methods~~ " + A + "§7 - BB-1 answered 2026-09-27 (`001F5D70` to `0060B980`)" + E + "."),
    (CRO, "each link. The `0x740` stride is the character-render record — the walk is over this page's own\n  table.",
     "each link. The `0x740` stride is the character-render record — the walk is over ~~this page's own~~\n  ~~table~~ "
     "the record array, which §8b shows is not this class " + T + "§8b, 2026-09-02)*."),
    # RO.CC-2: EXP-109's six functions include the constructor.
    (POOL, "`EXP-109` executed all six lifecycle operations plus the constructor and the default writers from",
     "`EXP-109` executed all six ~~lifecycle operations plus the constructor~~ entry points - the constructor and the "
     "five operations " + T + "§2's interface lists six entries, `004269A0` the constructor among them, and EXP-109's "
     "title names the same six)* - and the default writers from"),
    # RO.CC-3: the harness scripts thirteen callees (diff_render_pool.py, constants and the _hook arms).
    (POOL, "reproduces rather than scripts. Eleven\nother callees are oracles",
     "reproduces rather than scripts. ~~Eleven~~ Thirteen *(corrected 2026-10-02, OPUS: `diff_render_pool.py` scripts "
     "13 - `RESET`, `INIT`, `PREP`, `ASK`, `STAMP`, `FINISH`, `HANDOFF`, `CHILD`, `FREEA`, `FREEB`, `DESTROY`, `ASKREL`, "
     "`FIND` - the 13 the §15 row lists)*\nother callees are oracles"),
    (POOL, "- What the **eleven scripted callees** do to a record",
     "- What the **~~eleven~~ thirteen scripted callees** " + T + "the 13 oracles of `diff_render_pool.py`)* do to a record"),
    (POOL, "| what the eleven scripted callees do to a record beyond these fields is NOT established |",
     "| what the ~~eleven~~ thirteen scripted callees do to a record beyond these fields is NOT established " + T +
     "this row lists thirteen)* |"),
    # RO.CC-4: the 370 / 492 figures are the suite's first generation.
    (POOL, "the first loop to cover both, which is the obvious tidy, changes 370 of this suite's 492 lines.",
     "the first loop to cover both, which is the obvious tidy, changes 370 of this suite's 492 lines *(scope named "
     "2026-10-02, OPUS: the suite's first generation; the current 525-command suite compares 581 lines - re-run "
     "2026-10-02, 0 mismatches - and the same control changes 460 of 583, §13)*."),
    (POOL, "hoisting the test to cover both changes 370 of 492 lines |",
     "hoisting the test to cover both changes 370 of 492 lines *(the first suite; 460 of 583 in the current one, §13 - "
     "scope named 2026-10-02, OPUS)* |"),
    # RO.CS-11 / RO.CS-15.
    (POOL, "The five operations are still **unexecuted** — §13's pilot does not exist — so",
     "~~The five operations are still **unexecuted** — §13's pilot does not exist —~~ " + A + "§13 - "
     "`diff_render_pool.py` runs all five as shipped bytes, re-run 2026-10-02: 581 lines, 0 mismatches; and the "
     "correction below" + E + " so"),
    (POOL, "- The bit meanings of the flag word at `+0x18`. Bit 5 is set by promotion; bits 0, 2 and 4 are",
     "- The bit meanings of the flag word at `+0x18`. Bit 5 is set by promotion ~~;~~ and by retirement " + T +
     "`00427C90`+0x123 `or dword ptr [rdi + 0x48818], 0x20`, §5)*; bits 0, 2 and 4 are"),
    (POOL, "`00428863`; the other bits of `+0x18` are set by unrelated callers and are not established here |",
     "`00428863`; ~~the other bits of `+0x18` are set by unrelated callers~~ retire sets it too (`00427C90`+0x123), the "
     "constructor sets bits 0 and 2 (`004269A0`+0x2B9 `or ..., 5`) and promotion brackets bit 0 (`00428710`+0x80.."
     "+0xA7); the other writers, `002E8700`, `002E8CC0`, `002EBBB0` and `002EBBF0`, are outside the family " + T +
     "every `+0x48818` access in the image, retool grep)*; their meanings are not established here |"),
    # RO.CS-4 (character-render-object contract).
    (CROC, "- What the bank-selecting byte at `+0x1C` of the shared accessor's result is, and who writes it.",
     "- ~~What the bank-selecting byte at `+0x1C` of the shared accessor's result is, and who writes it.~~ " + A +
     "CONTRACT-character-transform-publish.md §14.1 - a camera-source flag written by the view publish - and "
     "character-render-object.md's slot-13 section for its writers" + E),
    # RO.CS-5 / RO.CS-6 (transform publish).
    (PUB, "   has no direct call site, so it is a vtable or callback entry.)*\n",
     "   has no direct call site, so it is a vtable or callback entry.)* " + A + "character-render-object.md - it is "
     "slot 13 of the vtable `00903B68`, called through `[rax+0x68]` by slot 16 at `001FA3D0`+0x378" + E + "\n"),
    (PUB, "**Ordering** — the publish must run before whatever flips the parity byte, and the renderer must read",
     "**Ordering** — ~~the publish must run before whatever flips the parity byte,~~ " + A + "§14.1 - nothing flips "
     "it per frame; it is a camera-source flag" + E + " and the renderer must read"),
    (PUB, "`TIMING` — the one this contract cannot specify until §14.1 is answered.",
     "`TIMING` — ~~the one this contract cannot specify until §14.1 is answered~~ " + A + "§14.1, answered: no per-frame "
     "flip exists to order against" + E + "."),
    # RO.CS-10 (lighting).
    (LIT, "- What sets `02B3F520`, `02B3F503` and `02B3F51C`.",
     "- What sets `02B3F520`~~, `02B3F503` and `02B3F51C`~~. " + A + "the `003AC900` paragraph below for `02B3F503` "
     "and `02B3F51C`" + E),

    # ---------------------------------------------------------------- 3.2.3 / 3.3.3 [RA]
    # RA.CC-4: the committed TSV is not the 3,381-row generation.
    (CRR, "not `arg0`). Result **3,381 accesses in 545 functions over 368 displacements** (was",
     "not `arg0`). Result **3,381 accesses in 545 functions over 368 displacements** *(not in the committed file: "
     "`character-render-record-accesses.tsv` holds 2,872 rows in 499 functions over 351 displacements - recount "
     "2026-10-02, OPUS; regeneration routed to SWE2-STRUCT)* (was"),
    # RA.CS-2: the register row is SUPERSEDED, not WITHDRAWN.
    (CRR, "*(closed — the register row is WITHDRAWN.)*",
     "*(closed — the register row is ~~WITHDRAWN~~ SUPERSEDED as a duplicate of `BT-3` " + T + "the register's UQ-197 "
     "row and the front matter say SUPERSEDED)*.)*"),
    # RA.CS-8: the +0x006 meaning.
    (CRR, "  +0x006  i16   (tested == -1 as a latch precondition)\n",
     "  +0x006  i16   (tested == -1 as a latch precondition)   " + CC + "the piece's owner-record link, -1 = unattached "
     "(CONTRACT-coast-down-latch.md section 15 row, answered 2026-09-22)\n"),
    # RA.CS-5 / RA.CS-6 (track pick).
    (TRK, "`+0x2C8` either way. *Who installs the two callbacks was not read.*",
     "`+0x2C8` either way. *~~Who installs the two callbacks was not read.~~* " + A + "render-event-selection-evidence.md "
     "- `002EA320` installs both through `0041D6C0` (`02CA4410 + id*8`): id 6 `002E7090` into `02CA4440` at "
     "`002EA320`+0x1A0 and id 0xC `002E70A0` into `02CA4470` at +0x1B1" + E),
    (TRK, "the selector objects behind `[02CA4668]`; who raises entry bit 6.",
     "~~the selector objects behind `[02CA4668]`~~ " + A + "the handler page's `0x09` section - the pointer is a table "
     "of `0x30` entries of `{1, cell}`, stored by `0041D6E0`" + E + "; who raises entry bit 6."),
    # RA.CS-7 (render-event evidence).
    (RES, "ID invalidation, cleanup-flag producers and remaining native animation callbacks",
     "~~ID invalidation, cleanup-flag producers and~~ " + A + "UQ-193 above for id invalidation - every release caller "
     "resets the id to -1 - and the 2026-09-30 note above for the flag: its only setter is `0041D4D0`" + E +
     " remaining native animation callbacks"),

    # ---------------------------------------------------------------- 3.2.4 / 3.3.4 [RG]
    # RG.CC-1: the status push tests 32 bits; bit 31 has a non-empty pair (0051E7A0 / 0051E7B0).
    (RIG, "chains of thirty-one tests, one call per changed bit.",
     "chains of ~~thirty-one~~ thirty-two tests " + T + "bit 31 too, at `003E7650`+0x318 and +0x580)*, one call per "
     "changed bit."),
    (RIG, "empty stub in both chains**: those ten statuses change nothing on the body through this push. Bit 31 is not tested.",
     "empty stub in both chains**: those ten statuses change nothing on the body through this push. ~~Bit 31 is not "
     "tested.~~ Bit 31 is tested: cleared calls `0051E7A0`, which stores 0 to the record's `+0x13C`, and set calls "
     "`0051E7B0`, which stores 1 " + T + "`003E7650`+0x318 `cmp dword ptr [rbx + 0x144], 0x80000000` / `jb`, +0x580 "
     "the same on `+0x140`; so 44 non-empty arms, the world tick's count)*."),
    (STAT, "things (the forty-two non-empty arms, summarised by script from their bodies):",
     "things (the ~~forty-two~~ forty-four non-empty arms " + T + "bit 31's pair `0051E7A0` / `0051E7B0` too, "
     "`003E7650`+0x318 and +0x580)*, summarised by script from their bodies):"),
    # RG.CC-2 / RG.CS-11 (look page).
    (LOOK, "- What thirteen of the rig's sixteen slots are (section 4a names the look controller, the eye object and the two",
     "- ~~What thirteen of the rig's sixteen slots are~~ " + A + "the-rig-of-seventeen-controllers.md section 2 - "
     "seventeen slots, sixteen populated, fifteen described; only slot 8 is unnamed and slot 4 is empty" + E +
     " (section 4a names the look controller, the eye object and the two"),
    # RG.CC-3.
    (LOOK, "*enables* each slot and names five more - `+0x0C` the Confuse motion",
     "*enables* each slot and names ~~five~~ six more " + T + "the list that follows has six)* - `+0x0C` the Confuse "
     "motion"),
    # RG.CS-8 / RG.CS-10 (look page).
    (LOOK, "- What the controller's `+0x18` (the minimum-duration floor) and the global scale `01DFE0B8` are.",
     "- ~~What the controller's `+0x18` (the minimum-duration floor) and the global scale `01DFE0B8` are.~~ " + A +
     "the rig page section 3a (`+0x18` is the duration, zero meaning one step) and the dispatch page: " + DFE + E),
    (LOOK, "- What `00426220` tests, and what the global `01F82E38` is.",
     "- What `00426220` tests~~, and what the global `01F82E38` is~~. " + A + "an-effect-element-frame-by-frame.md - "
     "`01F82E38` is the half-rate flag; " + DFE + E),
    # RG.CC-5.
    (RIG, "name four of its slots. This page names nine, by a different road:",
     "name four of its slots. This page names nine *(scope named 2026-10-02, OPUS: nine by this road; section 2's "
     "table now describes fifteen of the seventeen, the rest from their bodies in sections 3a and 5 - only slot 8 is "
     "unnamed and slot 4 empty)*, by a different road:"),
    # RG.CS-9 / RG.CS-15 / RG.CS-16 (rig page).
    (RIG, "  float each frame; how that float moves with the frame rate was not established here.",
     "  float each frame; ~~how that float moves with the frame rate was not established here~~ " + A +
     "effect-element-type-dispatch.md - " + DFE + E + "."),
    (RIG, "(bits 5, 6 and 7; what raises them was\nnot read)",
     "(bits 5, 6 and 7; ~~what raises them was~~\n~~not read~~ " + A + "the SWE2-EC7-83 section below - `00429C40`, "
     "`0042BBB0` and `00429B40` copy `+0x304` bits 6, 7 and 15 into them" + E + ")"),
    (RIG, "relative to the character; what triggers it was not traced.",
     "relative to the character; ~~what triggers it was not traced~~ " + A + "section 3a - the event handler "
     "`00427320` switches it on for the HP write's alive events `0x2005` / `0x2006`" + E + "."),
    # RG.CC-4 (fade page evidence row).
    (FADE, "| who writes which channel | members census, 22 sites, counts equal to a raw call sweep | 1 |",
     "| who writes which channel | members census, 22 sites, counts equal to a raw call sweep *(scope named 2026-10-02, "
     "OPUS: direct `call` / `jmp` sites only; the conditional-jump forwarders `00428940` (six callers) and `004293C0` "
     "(one) add channels 2 and 5 - section 3's 2026-09-19 correction)* | 1 |"),
    # RG.CS-20.
    (FADE, "- What channels 2, 3 and 5 were for. No body writes them; nothing in this executable can say.",
     "- What ~~channels 2, 3 and 5 were for. No body writes them; nothing in this executable can say.~~ channel 3 is "
     "for: no body writes it " + T + "section 3's 2026-09-19 correction - channels 2 and 5 are written, through the "
     "forwarder `00428940`)*."),
    (FADE, "| channels 2, 3, 5 have no writer | displacement sweep",
     "| ~~channels 2, 3, 5 have no writer~~ channel 3 has no writer " + T + "2 and 5 are written through the "
     "conditional-jump forwarder `00428940`, section 3)* | displacement sweep"),
    # RG.CS-21.
    (FADE, "| | viewer block flag bit 4, horizontal distance,",
     "| | ~~viewer block~~ system-tail flag bit 4 " + T + "`0042E850`+0x329 `test byte ptr [rsi + 0x48818], 0x10`, "
     "`rsi` the record array base - the tail's camera-inside fade bit, section 4c)*, horizontal distance,"),
    # RG.CS-12 / RG.CS-13 / RG.CS-14 / RG.CS-8 / CM.CS-20 (fade page).
    (FADE, "*The setter's two other callers, both record phases, were\nnot read.*",
     "*The setter's two other callers, both record phases, ~~were~~*\n*~~not read~~.* " + A + "the setter `003B33A0` has three "
     "callers, `0042CBF0`+0x330, `0042D7A0`+0x59 and `0042D830`+0x3A; `0042CBF0` is read whole in section 4a" + E),
    (FADE, "  in the table at `02EBD480` are; what the effect object and the four auxiliary handles are; what bit 14",
     "  in the table at `02EBD480` are " + A + "section 4d - the render-object handle table" + E + "; what the effect "
     "object ~~and the four auxiliary handles~~ is " + A + "section 4d - the four auxiliary handles are bone trails" + E
     + "; what bit 14"),
    (FADE, "`02AEDEF0`.* What fills that matrix was not traced.",
     "`02AEDEF0`.* ~~What fills that matrix was not traced.~~ " + A + "how-a-camera-reaches-the-renderer.md - the camera "
     "update `003820C0` copies the capped-field-of-view copy's matrix into it" + E),
    (FADE, "- What the global `01F82E38` is, whose non-zero value gives a new ramp a head start of one step.",
     "- ~~What the global `01F82E38` is~~ " + A + "an-effect-element-frame-by-frame.md - the half-rate flag; " + DFE + E +
     ", whose non-zero value gives a new ramp a head start of one step."),
    (FADE, "only builder is the camera update `003820C0` (2,125 B, one caller; **not read whole** - only its calls and the",
     "only builder is the camera update `003820C0` (2,125 B, one caller; ~~**not read whole** - only its calls and the~~ "
     + A + "how-a-camera-reaches-the-renderer.md section 4, read instruction by instruction 2026-09-19" + E + " - "
     "here only its calls and the"),
    # RG.CS-6 / RG.CS-7 / RG.CS-17 / RG.CS-18 (status page).
    (STAT, "`0051E170` for 1 (Slow) - three of the four are read in section 4b.",
     "`0051E170` for 1 (Slow) - ~~three~~ all four are read in section 4b " + T + "Immobilize `0051DE30` was read the "
     "same night)*."),
    (STAT, "Three of the four step bodies were read whole. They use",
     "~~Three~~ All four of the step bodies were read whole " + T + "Immobilize's the same night, below)*. They use"),
    (STAT, "`q` being the pulse times a double constant not converted\nhere, and raises",
     "`q` being the pulse times ~~a double constant not converted~~ 0.1\n~~here~~ " + A + "the Immobilize paragraph below - "
     "the two double constants are 0.1 and 0.3" + E + ", and raises"),
    (STAT, "what HP Critical's step writes (section 3's table; that step was not read, so the colour it blends toward is not on\nthis page).",
     "what HP Critical's step writes (section 3's table; ~~that step was not read, so the colour it blends toward is not on~~\n"
     "~~this page~~ " + A + "section 3a - step `00470230` read whole, record colour `+0x5D0` = (0.84, 0.84, 0.84)" + E + ")."),
    (STAT, "and the four step bodies of the second block - named,\n  not read. So what Slow, Stop, Immobilize and Invisible *look like* is not on this page.",
     "and the four step bodies of the second block ~~- named,~~\n  ~~not read. So what Slow, Stop, Immobilize and Invisible "
     "*look like* is not on this page.~~ " + A + "section 4b - all four read; Stop has no step and holds the pose "
     "sequencer's event 0 (section 4)" + E),
    (STAT, "*Lights; decoded in section 3.* What light kind\n  1 is (directional, point, spot) was not read.",
     "*Lights; decoded in section 3.* ~~What light kind~~\n  ~~1 is (directional, point, spot) was not read.~~ " + A +
     "how-a-character-is-lit.md section 5a - kind 1 is a directional light, `003AD540` read whole" + E),
    # RG.CS-5 (bone trails).
    (TRAIL, "an opacity - but that sentence is an inference and nothing below depends on it.",
     "an opacity - ~~but that sentence is an inference and nothing below depends on it~~ " + A + "section 5e - the tag "
     "decodes to a textured, Gouraud-shaded, alpha-blended triangle strip" + E + "."),
    (TRAIL, "The inference in section 5 about a textured strip is unchanged and is\nstill an inference.",
     "~~The inference in section 5 about a textured strip is unchanged and is~~\n~~still an inference.~~ " + A +
     "section 5e - no longer an inference" + E),
    (TRAIL, "say what the program draws, and section 5's inference about a textured strip is unchanged.*",
     "say what the program draws~~, and section 5's inference about a textured strip is unchanged~~.* " + A +
     "section 5e" + E),
    (TRAIL, "program, and the reason section 5's strip remains an inference.",
     "program~~, and the reason section 5's strip remains an inference~~. " + A + "section 5e, where the strip stops "
     "being an inference" + E),
    (TRAIL, "- the unread VU1 program's geometry, which the page itself labels an inference.",
     "- ~~the unread VU1 program's geometry, which the page itself labels an inference.~~ " + A + "section 5e - the "
     "geometry is decoded from the program's own GIF tag" + E),
    # ---------------------------------------------------------------- 3.2.5 / 3.3.5 [CL]
    # CL.CC-1 / CL.CC-8: 36 enqueue builders (40 appenders of 0018AFF0), 139-253 bytes.
    (L, "the same 140-to-150-byte template:",
     "the same ~~140-to-150-byte~~ template " + T + "the 36 builders are 139-253 bytes, 29 of them 140-150 - the "
     "falsification pass's table; recount of the 36 callers of `0018AFF0` in the `0018xxxx` range)*:"),
    (L, "// the shape of all 18 enqueue functions - 0018C610 shown, 148 B\n",
     "// the shape of all 18 enqueue functions - 0018C610 shown, 148 B   // " + CC + "36 builders, not 18 (the 36 "
     "`0018xxxx` callers of 0018AFF0; 40 appenders in all)\n"),
    (L, "| Every enqueue function shares one push_back idiom | complete bodies of all 18 enqueue functions listed in §3,",
     "| Every enqueue function shares one push_back idiom | complete bodies of all 18 enqueue functions listed in §3 "
     "*(scope named 2026-10-02, OPUS: §3's 18; the builders number 36, the falsification pass's table)*,"),
    (C, "· ~40 enqueue functions, `0018C610` (148 B) the worked example",
     "· ~40 enqueue functions *(scope named 2026-10-02, OPUS: 36 builders - the `0018xxxx` callers of `0018AFF0`; "
     "40 counts every appender, four of which allocate nothing)*, "
     "`0018C610` (148 B) the worked example"),
    (C, "enqueue (x40)   e.g. 0018C610\n",
     "enqueue (x40)   e.g. 0018C610   " + CC + "36 builders; 40 counts the four appenders that allocate nothing\n"),
    (C, "enqueue(owner, args):                             # 0018C610 and ~39 siblings\n",
     "enqueue(owner, args):                             # 0018C610 and ~39 siblings   # " + CC + "35 siblings: 36 "
     "builders call 0018AFF0 from 0018xxxx\n"),
    # CL.CC-1: command sizes over all 36 builders (four sizes).
    (L, "`0085E730` call is **`0x18` for eleven of the nineteen builders, `0x20` for seven and `0x28` for one**\n",
     "`0085E730` call is **`0x18` for eleven of the nineteen builders, `0x20` for seven and `0x28` for one** *(scope "
     "named 2026-10-02, OPUS: the nineteen of §2.3; " + SIZES + ")*\n"),
    (L, "| Command objects ship in three sizes, not one | the last write to `ecx` before the `0085E730` call in all **19** enqueue builders: `0x18` × 11, `0x20` × 7, `0x28` × 1 | 1 |",
     "| Command objects ship in ~~three~~ four sizes, not one | the last write to `ecx` before the `0085E730` call in "
     "~~all **19** enqueue builders: `0x18` × 11, `0x20` × 7, `0x28` × 1~~ all 36 builders " + T + SIZES + ")* | 1 |"),
    # CL.CC-2: 43 RTTI classes = 42 concrete + the abstract base.
    (L, "`uncovered_frontier.txt`) resolves **43 concrete classes** deriving from `OrderedObject` —",
     "`uncovered_frontier.txt`) resolves **43 ~~concrete~~ classes** - 42 concrete and the abstract base " + T +
     "`OrderedObject`'s slot 1 is the `_purecall` thunk `00861EC6`; recount of `members/ordered-object-vtable-slots.tsv`, "
     "43 class names)* - deriving from `OrderedObject` —"),
    # CL.CC-6.
    (L, "census is `postprocess-context-accesses.tsv` beside this page — 776 sites over 219 distinct offsets,",
     "census is `postprocess-context-accesses.tsv` beside this page — ~~776~~ 777 sites " + T + "the `+0xEE` section "
     "added the global-slot read; recount of the TSV, 777 rows)* over 219 distinct offsets,"),
    # CL.CC-9: slot 2 has nine implementations across the 42 concrete classes.
    (L, "| 2 | **order key** | a constant return in all 36; three distinct values observed |",
     "| 2 | **order key** | a constant return in all 36; three distinct values observed " + A + "§2.5 - nine "
     "implementations across the 42 concrete classes, seven constants and two data-driven keys" + E + " |"),
    (L, "here. **Slot 2 has only five distinct implementations across the 36 classes**, while slots 0 and 1",
     "here. **Slot 2 has only five distinct implementations across the 36 classes** *(scope named 2026-10-02, OPUS: "
     "across all 42 concrete classes it has nine, §2.5)*, while slots 0 and 1"),
    # CL.CS-4..6, CL.CS-8, CL.CS-9, CL.CS-10.
    (L, "Only the three values above were read. The remaining classes in §4.1 were not opened in this\n"
        "pass and their keys are unknown; see §7.",
     "Only the three values above were read. ~~The remaining classes in §4.1 were not opened in this~~\n"
     "~~pass and their keys are unknown; see §7.~~ " + A + "§7, answered 2026-09-12 - all 36 read, and the §2.5 matrix" + E),
    (L, "  these are shared by many. **The claim survived**, though the sort site itself is still unfound",
     "  these are shared by many. **The claim survived**~~, though the sort site itself is still unfound~~ " + A +
     "§7 - answered 2026-09-14: the list runs in stored order and is not sorted" + E),
    (L, "  happens; no consumer was found. §2.2 states what the values are;",
     "  happens; ~~no consumer was found~~ " + A + "§7 - the consumer executes the list in stored order, 2026-09-14" +
     E + ". §2.2 states what the values are;"),
    (L, "**no consumer that walks either list has been located**, so nobody has read the comparator yet. The",
     "~~**no consumer that walks either list has been located**, so nobody has read the comparator yet.~~ " + A +
     "§7 - the walk was found 2026-09-14 and compares nothing" + E + " The"),
    (L, "**Not claimed:** nothing here was executed or observed live. The sort and execution site remain\n",
     "**Not claimed:** nothing here was executed or observed live. ~~The sort and execution site remain~~ " + A +
     "§7, 2026-09-14 - executed in stored order, never sorted" + E + "\n"),
    (L, "eight zero bytes, then three 32-bit addresses. **What they hold is not established** |",
     "eight zero bytes, then three 32-bit addresses. ~~**What they hold is not established**~~ " + A + "the "
     "falsification pass - each is a class's RTTI Complete Object Locator; checked 2026-10-02: `[00902FB0 - 8]` = "
     "`01CEDAD8`, signature 1 and a self RVA that is the record itself" + E + " |"),
    (L, "        - **Not established:** whether any path clears the manager without the vector also being",
     "        - ~~**Not established:** whether any path clears the manager without the vector also being~~ " + A +
     "CONTRACT-render-command-list-and-graphics-handshake.md I-2 - all three clears are followed by a destroy or a "
     "flush, `0017CCD0`+0x83/+0x90, `00187950`+0x8B4/+0x8C1, `001E0590`+0x19/+0x26" + E),
    (L, "one; `0018B4E0` returns `01F7F5E0` and asserts it is non-null before doing so.",
     "one; `0018B4E0` returns `01F7F5E0` ~~and asserts it is non-null before doing so~~ " + T + "`CON-151`: "
     "`0018B4E0`+0x6..+0x10 hands the non-null test to the empty `0016D6A0`, a compiled-out assert)*."),
    (L, "| `0018B4E0` | second command list getter | 33 B | returns `01F7F5E0`, asserts non-null |",
     "| `0018B4E0` | second command list getter | 33 B | returns `01F7F5E0`~~, asserts non-null~~ " + T + "`CON-151`: "
     "the test goes to the empty `0016D6A0`)* |"),
    (L, "follows and is identical at both sites**: clear the non-owner first, destroy second",
     "follows and is identical at ~~both~~ all three sites** " + T + "the third is the scene teardown, `001E0590`+0x19 "
     "clear then +0x26 flush; CONTRACT-render-command-list-and-graphics-handshake.md I-2)*: clear the non-owner first, "
     "destroy second"),
    (H, "lists owns the command objects, the fixed clear-then-destroy pair at both teardown sites, and a",
     "lists owns the command objects, the fixed clear-then-destroy pair at ~~both~~ all three teardown sites " + T +
     "the contract's I-2, `001E0590`+0x19 / +0x26 the third)*, and a"),
    # CL.CS-7 (contract, AO).
    (C, "1. **Why does ambient occlusion terminate the walk?** I-7 is instruction-exact and its purpose is",
     "1. ~~**Why does ambient occlusion terminate the walk?**~~ " + A + "§4 - GC-1 answered 2026-09-25, the console's "
     "\"Display AO Only\" view" + E + " I-7 is instruction-exact and its purpose is"),
    # CL.CC-5 / CL.CC-7 / CL.CS-11 / CL.CS-12 (handshake page).
    (H, "`02EAF6D8` has **no writer**: no rip-relative store (24 listed references, all reads), no",
     "`02EAF6D8` has **no writer**: no rip-relative store (~~24~~ 17 listed references, all reads " + T + "retool refs "
     "02EAF6D8: 17 reads in 9 functions - the figure the method note below gives)*), no"),
    (H, "| ~~Two threads exist~~ | **WITHDRAWN 2026-09-07** — all nine thread procedures enumerated",
     "| ~~Two threads exist~~ | **WITHDRAWN 2026-09-07** — all nine thread-creation sites *(eight distinct procedures - "
     "§10's 2026-09-16 count; scope named 2026-10-02, OPUS)* enumerated"),
    (H, "disassembling `.text` and is reported at 12 sites against their 11, the difference being the\n"
        "`0x02ADD940` site on a different global.",
     "disassembling `.text` and ~~is reported at 12 sites against their 11, the difference being the~~\n"
     "~~`0x02ADD940` site on a different global~~ agrees with their 11 " + T + "the `0x02ADD940` loop at `0037CCC0`+0x150 is a "
     "copy loop, not a settle-spin - the 2026-09-13 correction above)*."),
    (H, "| Eleven inlined sites on this global, twelve overall |",
     "| Eleven inlined sites on this global~~, twelve overall~~ and none elsewhere " + T + "the `0037CCC0`+0x150 loop is a copy loop, "
     "2026-09-13)* |"),
    (H, "> One 32-bit global is the entire handshake between the thread that runs the game and the thread\n"
        "> that draws it.",
     "> One 32-bit global is the entire handshake ~~between the thread that runs the game and the thread~~\n"
     "> ~~that draws it~~ " + A + "CG-3 - no backend thread; both sides run on the main thread inside the frame" + E + "."),
    (H, "value is **stable across two consecutive reads** — that is, when the other thread is not part-way\n"
        "through updating it.",
     "value is **stable across two consecutive reads** ~~— that is, when the other thread is not part-way~~\n"
     "~~through updating it~~ " + A + "CG-3 - no other thread writes it, so the wait never iterates" + E + "."),
    (H, "non-`volatile` object cannot change between two adjacent reads; on the hardware, another core writes\nit.",
     "non-`volatile` object cannot change between two adjacent reads; ~~on the hardware, another core writes~~\n"
     "~~it~~ on the PS2 hardware another unit wrote it " + A + "CG-3 - on the PC port nothing writes it between the reads" + E + "."),

    # ---------------------------------------------------------------- 3.2.6 / 3.3.6 [GP]
    # GP.CC-1: eleven factories in 00862E50-00865320 (the table).
    (GI, "Thirteen\nfactories sit together at `00862E50`–`00865320`.",
     "~~Thirteen~~ Eleven " + T + "the table below lists eleven in that range; each of the 18 classes has one "
     "installer)*\nfactories sit together at `00862E50`–`00865320`."),
    (VIF, "caller-supplied mode — the eight `Gi*` arena factories at `0086xxxx` plus",
     "caller-supplied mode — the eight `Gi*` ~~arena factories~~ submit helpers at `0086xxxx` *(scope named 2026-10-02, "
     "OPUS: `00862E90`, `00863010`, `00863060`, `00863B90`, `00864E60`, `00865170`, `008652F0` and `00865360` call "
     "`0020E630`; only `00863060` is also one of the Gi page's eleven factories)* plus"),
    # GP.CC-2.
    (GI, "> (`+0x138`), so nine slots are never touched by this family.",
     "> (`+0x138`), so ~~nine slots are~~ five slots lie above it and 25 of the 45 are " + T + "45 slots less the "
     "twenty offsets listed below; slots 40-44 above the highest)* never touched by this family."),
    # GP.CC-3.
    (GI, "and the sizes passed to it span 16 … 360 bytes —",
     "and the sizes passed to it span ~~16 … 360~~ 8 … 1,600 bytes " + T + "the literal `edx` sizes among the 52 sites run from "
     "`001FBD80`+0x36 `mov edx, 8` to `001DB840`+0x35 `mov edx, 0x640`)* —"),
    # GP.CS-7 / GP.CS-8 / GP.CS-9 / GP.CS-11..14 (Gi page).
    (GI, "- **The display list's drain was not found.** All 28 references",
     "- ~~**The display list's drain was not found.**~~ " + A + "§11, The drain - `003A3740` reads the count and sorts "
     "the list" + E + " All 28 references"),
    (GI, "> **BG-11 stays open with its sharpened question recorded**, so it is cheap",
     "> ~~**BG-11 stays open with its sharpened question recorded**~~ " + A + "§20d - BG-11 is answered" + E +
     ", so it is cheap"),
    (GI, "*Unresolved:* what state `+0x4B4` etc. encode;",
     "*Unresolved:* ~~what state `+0x4B4` etc. encode~~ " + A + "character-render-object.md - `+0x4B4` is the "
     "one-way ready latch" + E + ";"),
    (GI, "passes a field, and the two reset commands pass **3**.",
     "passes a field~~, and the two reset commands pass **3**~~ " + T + "WITHDRAWN at pass 8 above: neither reset "
     "command makes any device-vtable call)*."),
    (GI, "image-wide, all `Gi*`.** Nothing outside this family touches the interface.",
     "image-wide, all `Gi*`.** " + T + "the true count is 5 - the §17-era re-census below)* Nothing outside this family "
     "touches the interface."),
    (GI, "## 10. The device is not a C++ class — and the pipeline around it",
     "## 10. The device is ~~not~~ a C++ class, `PrimitiveRendererD3D11` (corrected 2026-10-02, OPUS: §20e) — and the "
     "pipeline around it"),
    (GI, "> **The device layer is either compiled `/GR-` or is a hand-rolled C-style vtable struct. It is not a\n"
         "> Phyre class and not any class in the index.**",
     "> ~~**The device layer is either compiled `/GR-` or is a hand-rolled C-style vtable struct. It is not a~~\n"
     "> ~~Phyre class and not any class in the index.**~~ " + A + "§20e - the device's class is "
     "`PrimitiveRendererD3D11`, RTTI-bearing" + E),
    (GI, "render-thread executor for these `0x80`-byte blocks — **which was not found.**",
     "render-thread executor for these `0x80`-byte blocks — ~~**which was not found.**~~ " + A + "§20d - the block is "
     "never overwritten; `001F4A10` never sees it" + E),
    (GI, "> **Something writes `ctx+0` between enqueue and invocation, and it has not been found.**",
     "> ~~**Something writes `ctx+0` between enqueue and invocation, and it has not been found.**~~ " + A + "§20d - "
     "nothing writes it; `001F4A10` never sees the block" + E),
    # GP.CC-5 / GP.CC-6 / GP.CC-7 / GP.CC-8 / GP.CS-3..6 / GP.CS-10 / GP.CS-15 / GP.CS-16 (VIF page).
    (VIF, "The register list is authored data. §5e decoded one such cell by hand; this applies the same decode to **all 74\n"
          "hub-called builders**.",
     "The register list is authored data. §5e decoded one such cell by hand; this applies the same decode to **all 74\n"
     "hub-called builders** *(scope named 2026-10-02, OPUS: the census of that day; §2.4a's union is now 76 builders, "
     "the two jmp-reached ones added 2026-09-27)*."),
    (VIF, "**And the 29 that carry none mostly cannot.** **21 of them author no `UNPACK` command at all**",
     "**And the 29 that carry none mostly cannot.** " + T + "the 29 predate the correction above - with at least 61 of "
     "the 76 carrying a tag, at most 15 carry none, so the 21 / 8 split below was not re-run)* **21 of them author no "
     "`UNPACK` command at all**"),
    (VIF, "**So §2.4c's 29 tagless builders are fully accounted:** 21 author no `UNPACK` at all, and the 8 that do contain no",
     "~~**So §2.4c's 29 tagless builders are fully accounted:**~~ " + T + "not fully: `00476C80` above writes an A+D "
     "GIF tag, and §2.4c's tag count was corrected to at least 61)* 21 author no `UNPACK` at all, and the 8 that do "
     "contain no"),
    (VIF, "`004ECB70`). **Form comparison (SWE2-FRONTIER, this pass):** eight of them share `004EF860`'s exact shape —",
     "`004ECB70`). **Form comparison (SWE2-FRONTIER, this pass):** eight of them share `004EF860`'s exact shape *(scope "
     "named 2026-10-02, OPUS: of the neighbours listed; the region census `vu1-region-functions.tsv` has a ninth, "
     "`00479370`, 219 B)* —"),
    (VIF, "| VU helper — VU-state toucher, not installed | 54 |",
     "| VU helper — VU-state toucher, not installed | 54 " + T + "ten of them are VU1 microprogram entries, role "
     "`VU1-microprogram(VU-state-toucher)` in the TSV, UQ-213; 44 remain helpers)* |"),
    (VIF, "E8/E9 caller — consistent with VU `JAL`/`JR` sub-programs or install paths not yet found (§7).",
     "E8/E9 caller — ~~consistent with VU `JAL`/`JR` sub-programs or install paths not yet found~~ " + A + "§7 - none "
     "of the 19 is a `JAL` / `JR` target; all 19 are VU1 microprogram entries" + E + " (§7)."),
    (VIF, "            MSCAL  -> program(callback, context)      47 microprograms, mostly 0x470000-0x500000; also 002F0280, 0053F490\n",
     "            MSCAL  -> program(callback, context)      47 microprograms, mostly 0x470000-0x500000; also 002F0280, "
     "0053F490   " + CC + "57 (section 2.3's correction, UQ-213)\n"),
    (VIF, "**PARTIAL.** The interpreter, the machine state, the installation paths and the program population are read.",
     "~~**PARTIAL.**~~ **DOCUMENTED.** " + T + FM + "`status: DOCUMENTED`, UQ-213 and UQ-215 answered 2026-09-27)* The "
     "interpreter, the machine state, the installation paths and the program population are read."),
    (VIF, "- what any single microprogram draws;\n- how the GS data is finally turned into PC draw calls;\n- the UNPACK formats.",
     "- ~~what any single microprogram draws;~~ " + A + "§7, UQ-213" + E + "\n- ~~how the GS data is finally turned "
     "into PC draw calls;~~ " + A + "§2.1b, the GS translator" + E + "\n- ~~the UNPACK formats.~~ " + A + "§7, UQ-215" + E),
    (VIF, "**Not read here:** the render-thread command stream that `001F49F0` hands the replay to",
     "**Not read here:** ~~the render-thread command stream that `001F49F0` hands the replay to~~ " + A + "the Gi "
     "family page §20d - BG-11 is answered" + E),
    (VIF, "   The object's class is not identified here.",
     "   ~~The object's class is not identified here.~~ " + A + "§7 - `[01FC35F8]` holds `02CC1CD0`, the embedded "
     "`PrimitiveRendererD3D11`" + E),
    (VIF, "the rest of `0020ED30`'s state selection, the class behind\n`[01FC35F8]`, and what",
     "the rest of `0020ED30`'s state selection, ~~the class behind~~\n~~`[01FC35F8]`~~ " + A + "§7, the embedded "
     "`PrimitiveRendererD3D11`" + E + ", and what"),

    # ---------------------------------------------------------------- 3.2.7 / 3.3.7 [EF]
    (DISP, "`0043EAB0` (136 B) is a call-free jump-table leaf - `add r8,r9; jmp r8`, arms `jmp 00522290`",
     "`0043EAB0` (136 B) is a call-free jump-table leaf - `add r8,r9; jmp r8`, arms *(eighteen - ten listed here; "
     "also `00528AB0`, `005291C0`, `0052A0F0`, `0052ADB0`, `0052BF70`, `0052D370`, `0052E3F0` and `0047BDA0`, "
     "`0043EAB0`+0x2B..+0x80; the table's 18; 2026-10-02, OPUS)* `jmp 00522290`"),
    (DISP, "The other 27 report **\"no DOCUMENTED citer found\"**",
     "The other 27 *(of the first run's 39; the re-check above counts 25 of 40 - scope named 2026-10-02, OPUS)* report "
     "**\"no DOCUMENTED citer found\"**"),
    (DISP, "biggest first. Nine are\nnamed by a page in this folder or its neighbours",
     "biggest first. ~~Nine~~ Twelve " + T + "the table that follows has twelve rows, each naming its page)* are\n"
     "named by a page in this folder or its neighbours"),
    (DISP, "**PARTIAL.** Read:",
     "~~**PARTIAL.**~~ **DOCUMENTED.** " + T + FM + "`status: DOCUMENTED`)* Read:"),
    (DISP, "- the frame counter step.",
     "- the ~~frame counter~~ birth step " + T + "§2.1's correction - `002F3BC0` runs once per element, at birth)*."),
    (DISP, "- what any individual element type is;",
     "- ~~what any individual element type is;~~ " + A + "UQ-204, answered 2026-09-27 - a table of what each of the 65 "
     "types puts on screen" + E),
    (DISP, "- the link from the EFX chunk runs to element creation.",
     "- ~~the link from the EFX chunk runs to element creation.~~ " + A + "§2.8 - the chain is closed end to end" + E),
    (DISP, "the sub-resource path below. The type values have not yet been matched to authored effect data.",
     "the sub-resource path below. ~~The type values have not yet been matched to authored effect data.~~ " + A + "§2.8 - the dispatch key is the "
     "authored byte" + E),
    (DISP, "### 2.1 The per-frame step — `002F3BC0`",
     "### 2.1 The ~~per-frame~~ birth step (corrected 2026-10-02, OPUS: it runs once per element) — `002F3BC0`"),
    (DISP, "| `002F3BC0` (frame step) | `00441B30` only (`00441E71`) |",
     "| `002F3BC0` (~~frame~~ birth step " + T + "§2.1)*) | `00441B30` only (`00441E71`) |"),
    (DISP, "Which of those paths is update, draw or creation is **not read**.",
     "Which of those paths is update, draw or creation ~~is **not read**~~ " + A + "§2.1 and §2.5 - the step is birth, "
     "`005004C0` creation, the update and the walk the per-frame work" + E + "."),
    (DISP, "`0024E460`, `003A3D20`, `003A2C70`; the drain end of the list; which of the two dispatches",
     "`0024E460` " + A + "its frontier note below" + E + ", `003A3D20`, `003A2C70`; ~~the drain end of the list~~ " + A +
     "\"The drain in full\" above" + E + "; which of the two dispatches"),
    (DISP, "      element `+0` by `002F2D60` (`002F30F2`). *Not* answered: what each of the types is.",
     "      element `+0` by `002F2D60` (`002F30F2`). ~~*Not* answered: what each of the types is.~~ " + A + "the UQ-204 "
     "answer above" + E),
    (DISP, "| method vocabulary + per-type record maps read; step/update tail helpers and emit calls `not read` |",
     "| method vocabulary + per-type record maps read; ~~step/update tail helpers and emit calls `not read`~~ step/update "
     "tails read on an-effect-element-frame-by-frame.md (nine tails and the shared helper `0044B960`), emits in UQ-204 "
     + A + "those pages" + E + " |"),
    (FBF, "## 4. The other seven tails: types `0x02`, `0x04`, `0x05`, `0x06`, `0x07`, `0x0A`",
     "## 4. The other ~~seven~~ six tails (corrected 2026-10-02, OPUS: CON-179 below): types `0x02`, `0x04`, `0x05`, "
     "`0x06`, `0x07`, `0x0A`"),
    (E00, "All ten step/update tails, the cull test,",
     "All ~~ten~~ nine step/update tails and the shared helper `0044B960` " + T + "CON-179 on "
     "an-effect-element-frame-by-frame.md; `0044B960` has 48 call sites)*, the cull test,"),
    (EFX, "> **No `.efx` or `.efb` file was opened to write this sheet.** Neither is in the local extraction and",
     "> ~~**No `.efx` or `.efb` file was opened to write this sheet.**~~ " + A + "the 2026-09-30 update below - every "
     "file has now been opened, §2b" + E + " Neither is in the local extraction and"),
    (EFX, "+0x08  byte[8]  _unread   no reader found in the loader body at 0x003EDAD0\n",
     "+0x08  byte[8]  _unread   no reader found in the loader body at 0x003EDAD0   " + CC + "+0x0C is read by the "
     "caller 003B0660+0xDF as the stream length (section 2b)\n"),
    (EFX, "another function handed the same buffer could read it, and that search was not run. §7. |",
     "another function handed the same buffer could read it, ~~and that search was not run~~ " + A + "§2b - "
     "`003B0660`+0xDF reads `+0x0C` before calling the loader" + E + ". §7. |"),
    (EFX, "second header half and the payload at `+0x10` remain unmeasured, so §7's caveats about them stand",
     "second header half and the payload at `+0x10` ~~remain unmeasured, so §7's caveats about them stand~~ " + A +
     "§2b, measured 2026-09-30" + E),
    (ERM, "**4.5 GB — the second-largest format family in the archive after `.phyre`**, and nothing in the\n"
          "database describes either one.",
     "**4.5 GB — the second-largest format family in the archive after `.phyre`**~~, and nothing in the~~\n"
     "~~database describes either one~~. " + A + "efx-and-efb-effect-containers.md" + E),
    (ERM, "that they are a container and its payload. A sheet should settle that rather than inherit it.",
     "that they are a container and its payload. ~~A sheet should settle that rather than inherit it.~~ " + A +
     "efx-and-efb-effect-containers.md - two formats sharing one container convention" + E),

    # ---------------------------------------------------------------- 3.2.8 / 3.3.8 [ET]
    (MESH, "| `+0x28` 4-byte | 4 B × c18 | 147,220 |",
     "| `+0x28` 4-byte | 4 B × c18 | ~~147,220~~ 155,916 " + T + "the sum of `c18` over the 2,252 records of "
     "`members/effect-mesh-54-records.tsv`, equal to `c1A`'s)* |"),
    (MESH, "consistent with packed RGBA where `0x80` is the GS full-opacity alpha. Colour hypothesis. |",
     "consistent with packed RGBA where `0x80` is the GS full-opacity alpha. ~~Colour hypothesis.~~ " + A + "§8, SD-140 "
     "- a per-corner RGBA8 vertex colour" + E + " |"),
    (MESH, "**0 NaN** — consistent with texture UVs. UV hypothesis. |",
     "**0 NaN** — consistent with texture UVs. ~~UV hypothesis.~~ " + A + "§8, SD-140 - a per-corner texture "
     "coordinate" + E + " |"),
    (MESH, "is consumer-backed; the colour and UV labels for `+0x28` / `+0x2C` stay distributional (`SD-140`).)*",
     "is consumer-backed; the colour and UV labels for `+0x28` / `+0x2C` ~~stay distributional~~ (`SD-140`).)* " + A +
     "§8 - SD-140 answered 2026-09-30" + E),
    (MESH, "  id resolves to a same-file kind-`0x52` record (key 0, sub = id) — **439 / 439\n",
     "  id resolves to a same-file kind-`0x52` record (key 0, sub = id) — **439 / 439** *(scope named 2026-10-02, OPUS: "
     "the 439 records with a nonzero `c1C`, 425 + 14; their ids number 453 - recount of the TSV)* **\n"),
    (MESH, "| type-`0x05` elements | 5,164 (all `0xA00` records,",
     "| type-`0x05` elements | 5,164 *(scope named 2026-10-02, OPUS: this page's walk, which stops at each `.efb`'s "
     "first blob; over every stream 5,204 - 5,168 in `.efx` / `.efb` and 36 embedded, `type_census.tsv`)* (all "
     "`0xA00` records,"),
    (MESH, "the clipper 00521450 (status line current 2026-10-01, SWE2-DATA)\n",
     "the clipper 00521450 (status line current 2026-10-01, SWE2-DATA)   # " + CC + "the register dates SD-140 "
     "ANSWERED 2026-09-30, as section 8 does\n"),
    (E00, "emitter `0039D6C0`;\n",
     "emitter ~~`0039D6C0`~~ " + A + "the GI-14 section - read 2026-10-01" + E + ";\n"),
    (E00, "`00250010`, `003A8240`, ~~`003A8950`~~, `00432300`, `00441EA0`,",
     "`00250010`, `003A8240`, ~~`003A8950`~~, ~~`00432300`~~ " + A + "effect-mesh-records-kind-54.md §8 - the PS2 "
     "colour modulate" + E + ", `00441EA0`,"),
    (E00, "unconfirmed consumers.",
     "~~unconfirmed consumers~~ " + A + "the walks of `0x01` and `0x03` above - mode 6 takes `02AEE908`, the others "
     "`02AEE900` chooses an emitter" + E + "."),
    (E60, "closed by `00431770` - the eight-group 0x65 setup this page already names.",
     "closed by `00431770` - the eight-group ~~0x65~~ `0x67` setup " + T + "the arm's type was corrected to `0x67` at "
     "the head of this paragraph)* this page already names."),
    (MENU, "**PARTIAL.** Read: the table shape, the API, the link to the instance list, the callers. Not read: the record's\n"
           "fields past `+8`, what `+0x338` in an instance means, and which menu uses which id.",
     "~~**PARTIAL.**~~ **DOCUMENTED.** " + T + FM + "`status: DOCUMENTED`)* Read: the table shape, the API, the link to "
     "the instance list, the callers. ~~Not read: the record's~~\n~~fields past `+8`, what `+0x338` in an instance "
     "means, and which menu uses which id.~~ " + A + "UQ-208, UQ-209 and UQ-210, answered 2026-09-17" + E),
    (MENU, "  record +0x10 .. +0x27  not read\n",
     "  record +0x10 .. +0x27  not read   " + CC + "read: +0x10..+0x1C are the spawn call's four arguments (UQ-208, "
     "2026-09-17)\n"),
    (MENU, "`003B2CA0` and `003B2CE0`, whose roles are not read.",
     "`003B2CA0` and `003B2CE0`, whose roles are not read *(answered for `003B2CE0`: the call-free menu-effect "
     "classifier below; 2026-10-02, OPUS)*."),

    # ---------------------------------------------------------------- 3.2.9 / 3.3.9 [MF]
    (FDM, "`1,045/1,066` (the 21 missing are mostly `treasure`/`bg_obj` files). Census:",
     "`1,045/1,066` (the 21 missing are ~~mostly `treasure`/`bg_obj` files~~ all weapons " + T + "the tag set of every "
     "`.cm` in the extracted archive; FCP's 21 `@FCP @FTR @FOR` weapons)*). Census:"),
    (FDM, "(`209`, `111`, `111` files).",
     "(`209`, `111`, `111` ~~files~~ entries, in 45 files " + T + "29 weapons and 16 treasures carry them; recount of "
     "the `.cm` tag sets)*)."),
    (FDM, "- `004201F0` — `@FOR` LOD select, fully disassembled (144 insns).",
     "- `004201F0` — `@FOR` LOD select, fully disassembled (~~144~~ 143 insns " + T + "648 bytes to the `ret` at "
     "`004201F0`+0x287; the falsification pass's count note)*)."),
    (FDM, "+0x40  table A — small records (3 B stride suggested by the B offset arithmetic; content unresolved)\n",
     "+0x40  table A — small records (3 B stride suggested by the B offset arithmetic; content unresolved)   " + CC +
     "resolved 2026-09-29, Table A/B section below\n"),
    (FDM, "…      table B — bytes between u16@0x36 and u16@0x38 (unresolved)\n",
     "…      table B — bytes between u16@0x36 and u16@0x38 (unresolved)   " + CC + "resolved 2026-09-29, Table A/B "
     "section below\n"),
    (FDM, "| sampled; consumers unresolved |",
     "| sampled; consumers ~~unresolved~~ partly read " + A + "the 2026-09-29 table A/B section - five `0x20`-stride "
     "part sub-records, read by the builder" + E + " |"),
    (SKEL, "Which models these\nare on screen is not established here (§7).",
     "~~Which models these~~\n~~are on screen is not established here~~ " + A + "§7, HM-1 2026-09-27 - the ids name a "
     "model's own high-detail variants; `hc1006_03` is `c1006`'s replacement body" + E + " (§7)."),
    (SKEL, "  - **Still open:** which models the ids name (the id space is not a simple `c`+number rule: `C:43` has no\n"
           "    `c1043` model), what pose mode 2 is, and which model the mapping's second skeleton is.",
     "  - **Still open:** ~~which models the ids name (the id space is not a simple `c`+number rule: `C:43` has no~~\n"
     "    ~~`c1043` model)~~ " + A + "the OPUS narrowings above - the ids name files, and the second skeleton is the "
     "element row's parent" + E + ", what pose mode 2 is~~, and which model the mapping's second skeleton is~~."),
    (SKEL, "What `keyB` / `keyC` select when they are not `-1` — four records set them and nothing here\n"
           "says to what.",
     "~~What `keyB` / `keyC` select when they are not `-1` — four records set them and nothing here~~\n"
     "~~says to what.~~ " + A + "§7, HM-1 2026-09-26 - `b` / `c` are the actor's model local number and CLUT number, "
     "and every shipped lookup is keyed (1, 0)" + E),
    (ADM, "What the adjustment looks like on screen, and what the `_town` twin changes,\nare not established (§7).",
     "What the adjustment looks like on screen~~, and what the `_town` twin changes,~~\n"
     "is not established (§7) " + A + "the `_town` answer near the end - the civilian-area variants of the same "
     "additive-pose tracks" + E + "."),
    (ADM, "`field02 = 0` tracks was not cross-tabulated.",
     "`field02 = 0` tracks ~~was not cross-tabulated~~ " + A + "§6's pass - the same 35 tracks, tested as set "
     "equality" + E + "."),
    (ADM, "Not yet run. The census walk is the positive control",
     "~~Not yet run.~~ " + A + "Falsification pass 1 — 2026-09-13 (OPUS), below" + E + " The census walk is the "
     "positive control"),
    (ADM, "+0x04  byte[24]  values       copied as 8 / 4 / 8 / 4-byte pieces; the element types are not fixed by the code\n",
     "+0x04  byte[24]  values       copied as 8 / 4 / 8 / 4-byte pieces; the element types are not fixed by the code   "
     + CC + "the full disassembly below reads a record as {i32 bone; f32 eulerDeg[3]; f32 offset[3]}\n"),
    (ADM, "-0.033)` — plausible numbers, which is a reading of the data and not a traced type (§7).",
     "-0.033)` — plausible numbers~~, which is a reading of the data and not a traced type~~ " + A + "the full "
     "disassembly of `003714A0` below - `{i32 bone; f32 eulerDeg[3]; f32 offset[3]}`" + E + " (§7)."),
    (ADM, "**What it is for is not established.** The marking is measured;",
     "~~**What it is for is not established.**~~ " + A + "the answers near the end - the `field00 = 1` tracks are the "
     "id-match track 0, and its sentinel is the base pose" + E + " The marking is measured;"),
    (ADM, "| `003714A0` | `AddMotion_ApplyBonePose` | ◐ the track/record walk `003716B0`–`0037175C` and the rotation call |",
     "| `003714A0` | `AddMotion_ApplyBonePose` | ◐ the track/record walk `003716B0`–`0037175C` and the rotation call " +
     A + "the full disassembly below" + E + " |"),
    (POSE, "window 00371F2E..00371FD4 read, the rest of its\n3,387 bytes not).",
     "window 00371F2E..00371FD4 read, ~~the rest of its~~\n~~3,387 bytes not~~ " + A + "adm-add-motion-tables.md - the "
     "full disassembly of `003714A0`" + E + ")."),
    (FCP, "| 0–10, 18 — the real table |",
     "| 0–10~~, 18~~ — the real table " + T + "no section 18 exists, the 2026-09-21 tail-section extension)* |"),
    (FCP, "`+0x2A` is removed from the section list and the fence narrowed to\n`u16[19]`, since",
     "`+0x2A` is removed from the section list and the fence narrowed to\n~~`u16[19]`~~ `u16[18]` " + T + "the current "
     "fence, §2 and the 2026-09-21 extension)*, since"),
    (FCP, "The five files where section 21 starts inside that span are named in section 2. |",
     "~~The five files where section 21 starts inside that span are named in section 2.~~ " + T + "there is no "
     "section 21, §2's correction)* |"),
    (FCP, "Sections 5 and 11–17 are authored-only — never present or never read.",
     "Sections ~~5 and~~ 11–17 are authored-only — never present or never read " + T + "section 5 is read inline in "
     "`003E7210`, the offset-word reader inventory below)*."),

    # ---------------------------------------------------------------- 3.2.10 / 3.3.10 [MM]
    (FEF, "  fef_motion_entry_census.py` — 12 checks, `FAILS 0` on the shipping archive.",
     "  fef_motion_entry_census.py` — ~~12~~ 25 checks " + T + "the script's `check(` calls, recounted; FAILS not "
     "re-run here)*, `FAILS 0` on the shipping archive."),
    (FEF, "| `@FMW` | 111 | 45 | motion weight/blend record (this sheet) |",
     "| `@FMW` | 111 | 45 | motion ~~weight/blend~~ track-data record (this sheet) " + T + "the `@FMW` section - "
     "Euler, translation and scale channels)* |"),
    (FEF, "**a directed sway** (op `0x48` is the same command) — deferred event,",
     "**a directed sway** (op `0x48` is the same command) — ~~deferred~~ event applied at once " + T + NOT426 + ")*,"),
    (MR, "the weapon/treasure command names, `@FMN`/`@FMW` the 1:1 name/blend pair, `@FRM` the",
     "the weapon/treasure command names, `@FMN`/`@FMW` the 1:1 name/~~blend~~ track-data pair " + T +
     "fef-and-motion-entries.md's `@FMW` section)*, `@FRM` the"),
    (MR, "parameter-install API (36 members).",
     "parameter-install API (~~36~~ 39 members " + T + "39 rows in `members/model-oscillator-subsystem.tsv`)*)."),
    (OSC, "`members/model-oscillator-subsystem.tsv` lists all 36 members with per-function evidence level.",
     "`members/model-oscillator-subsystem.tsv` lists all ~~36~~ 39 members " + T + "recount of the TSV, 39 rows)* with "
     "per-function evidence level."),
    (FTE, "                                       allocator 00537AA0 (invariant, 1,951/1,951)\n",
     "                                       allocator 00537AA0 (invariant, 1,951/1,951)   " + CC + "1,972/1,972: every "
     "@FCT header record of the 1,044 files (extracted archive)\n"),
    (FTE, "Census over `1,044` files / `1,951` header records:",
     "Census over `1,044` files / ~~`1,951`~~ `1,972` header records " + T + "the `+0x0C` counts summed over every "
     "`@FCT` entry of the extracted archive)*:"),
    (FTE, "values are `0x400` (1618), `0x200` (318), `0x40` (35) →",
     "values are `0x400` (1618), `0x200` (318), `0x40` (~~35~~ 36 " + T + "same census)*) →"),
    (FTE, "`00504D20` (7 bytes; called from the status-look code at `00428D3C`, plus\n`00428CD0` twice and `0042E520`)",
     "`00504D20` (7 bytes; called ~~from the status-look code at `00428D3C`, plus~~\n~~`00428CD0` twice and "
     "`0042E520`~~ at three sites, `00428CD0`+0x6C and +0xB2 and `0042E4F0`+0x30 " + T + "retool callers 00504D20; "
     "X2 below)*)"),
    (FRP, "and none reads the container's parts; what the parts are stays open.",
     "and none reads the container's parts~~; what the parts are stays open~~. " + A + "the 2026-09-30 corrections - "
     "each entry type is read on its own sheet" + E),
    (FRP, "through command `0x09` (that invoker is only partly read),",
     "through command `0x09` (that invoker ~~is only partly read~~ " + A + "the handler page - `00417F40` read whole" +
     E + "),"),

    # ---------------------------------------------------------------- 3.2.11 / 3.3.11 [PP]
    (CAT, "plus `006DF480` (the logger) ×10, `sprintf` ×8, and single calls to the effect loader, `memset`,\n"
          "`free` and the stack-cookie check.",
     "plus `006DF480` (the logger) ×10, `sprintf` ×8, and single calls to ~~the effect loader, `memset`,~~\n"
     "~~`free` and the stack-cookie check~~ eight targets " + T + "every direct call of `0072A320` recounted, 358 "
     "sites to 22 targets: `0078A530`, `0078A120` the effect loader, `0078A960`, `0071B3C0`, `00861EC0` (`memset`), "
     "`00715360`, `0072E940` and `00808C40` the cookie check, once each)*."),
    (CAT, "- **Depth of field** is the largest family by far — 63 techniques — with a separate **Bokeh** family",
     "- **Depth of field** is the largest family by far — 63 techniques *(scope named 2026-10-02, OPUS: §4's Depth "
     "list - 53 `tech_DepthOfField`, 8 `tech_DepthFromDofFactor`, 2 `tech_DepthEncode`)* — with a separate **Bokeh** "
     "family"),
    (CAT, "/* then 332 registrations, in seven shapes */\n",
     "/* then 332 registrations, in seven shapes */   // " + CC + "219 of the 332 are string operations (section 8's "
     "UQ-225 answer); the registrations are mostly inline\n"),
    (CAT, "The registration helpers, by call count:",
     "The ~~registration helpers~~ callees " + T + "the four most-called are the string class, the correction above)*, "
     "by call count:"),
    (CAT, "| `00715C70` | — | 70 B | registration helper, 91 call sites here |",
     "| `00715C70` | — | 70 B | ~~registration helper~~ the string destructor " + T + "UQ-225, 2026-09-18)*, 91 call "
     "sites here |"),
    (CAT, "        -> 00715C70 x88            \\\n",
     "        -> 00715C70 x88            \\   " + CC + "x91, 007157A0 x48, 00719380 x40 (the 2026-09-12 re-census); "
     "332 calls, not ~323, and the first two are string utilities\n"),
    (CAT, "They are excluded above; the 24 real targets all resolve in",
     "They are excluded above; the ~~24~~ 22 real targets " + T + "the struck row above; 358 sites to 22 targets)* all "
     "resolve in"),
    (CAT, "- The **count-argument-as-multiplier** reading rests on **four observed literals** (4, 8, 17, 25) at\n"
          "  call sites of two of the seven helpers. It is consistent with every one of them and is **not**\n"
          "  established for the five helpers whose bodies were not read.",
     "- The **count-argument-as-multiplier** reading rests on ~~**four observed literals** (4, 8, 17, 25)~~ the "
     "complete list of §2 (nine values over 91 sites) at\n"
     "  call sites of two of the seven helpers. It is consistent with every one of them ~~and is **not**~~\n"
     "  ~~established for the five helpers whose bodies were not read~~ " + A + "§8's UQ-225 answer - the helper "
     "bodies are read" + E + "."),
    (CAT, "§'s caveat stands: the count-argument-as-multiplier reading still rests on four observed literals at\n"
          "two of the seven helpers, and is not established for the five whose bodies are unread.",
     "§'s caveat ~~stands~~ " + A + "§2's complete list and §8's helper bodies" + E + ": the count-argument-as-"
     "multiplier reading ~~still rests on four observed literals at~~\n~~two of the seven helpers, and is not "
     "established for the five whose bodies are unread~~ rests on nine values at 91 sites."),
    (CAT, "**Which `cfg` float carries the focus distance is not\nread here.**",
     "~~**Which `cfg` float carries the focus distance is not~~\n~~read here.**~~ " + A + "CONTRACT-post-processing-"
     "subsystem.md - `+0x24` / `+0x28` carry `mDofFocusDistance` / `mDofApertureFnumber`" + E),
    (CAT, "`006DB9A0`'s body is not read here. **So",
     "~~`006DB9A0`'s body is not read here.~~ " + A + "CONTRACT-post-processing-subsystem.md - the chain to "
     "`00707560` `SetGlareParameters`, read 2026-09-25" + E + " **So"),
    (CAT, "- who fills `cfg`, and in particular which float is the cutscene focus distance;",
     "- ~~who fills `cfg`, and in particular which float is the cutscene focus distance;~~ " + A +
     "CONTRACT-post-processing-subsystem.md - `0018EEE0` allocates the `0xF0` block, and `+0x24` is the focus "
     "distance" + E),
    (CS, "  command's `+0x10`)*, and which float carries the cutscene focus distance.",
     "  command's `+0x10`)*~~, and which float carries the cutscene focus distance~~. " + A + "the `cfg` table above - "
     "`+0x24` is `mDofFocusDistance`" + E),
    (CS, "- Let a library error abort the frame. The game ignores it (I-5).",
     "- Let a library error abort the frame. The game ignores it (I-5) " + T + "an `ApplyEffects` error; an "
     "initialisation failure does reach the game - the corrected heading of I-5's section)*."),
    (CP, "3. **Logging disabled** → the normal case; no diagnostic is emitted on any path (I-4).",
     "3. **Logging disabled** → the normal case; no diagnostic is emitted on any path (~~I-4~~ I-5 " + T + "I-5 is the "
     "retail silence; I-4 is the count multiplier)*)."),
    (CP, "   reading the fourteen helpers' bodies; none was read here.",
     "   reading the fourteen helpers' bodies~~; none was read here~~. " + A + "§10's pass 1 - five are string "
     "utilities and registration is the vtable" + E),
    (CP, "   006DF480 x10, sprintf x8, memset, a string release (00715360), the stack-cookie check\n",
     "   006DF480 x10, sprintf x8, memset, a string release (00715360), the stack-cookie check   " + CC + "and single "
     "calls to 0078A530, 0078A960 and 0071B3C0 (0072A320+0x86, +0xBB, +0xEB): 22 direct targets in all\n"),
    (PI, "None. This document produces identity, not mechanism — no PPFX function body has been read.",
     "None. This document produces identity, not mechanism ~~— no PPFX function body has been read~~ " + T + "H-4 and "
     "H-6 below read three bodies)*."),
    (PI, "Not derived. One ordering constraint is stated by the strings themselves:",
     "~~Not derived.~~ " + A + "the-post-processing-effect-catalogue.md §5 and CONTRACT-post-processing-subsystem.md "
     "for the call chain" + E + " One ordering constraint is stated by the strings themselves:"),
    (PI, "147 named functions is the entry point for any",
     "147 named ~~functions~~ entries " + T + "135 functions and 12 funclets, the correction below)* is the entry point "
     "for any"),
    (PI, "becomes the recorded name — and how the three collisions resolve — is this page's call.",
     "becomes the recorded name — and how the ~~three~~ seven collisions " + T + "the count above)* resolve — is this "
     "page's call."),
    (PI, "`CRenderGlare` 5, and sixteen more classes with 1–3 each.",
     "`CRenderGlare` 5, and ~~sixteen~~ at least seventeen more classes with 1–3 each " + T + "the list below alone "
     "names seventeen more)*."),
    (VR, "Absent from the binary and **not** tool-marked, so neither reading explains them:",
     "Absent from the binary as literal strings and **not** tool-marked~~, so neither reading explains them~~ " + A +
     "the reflected-parameter page's W-9, "
     "answered 2026-09-15: the six `mCascadePartition<c>_<q>` keys are read through the template "
     "`\"mCascadePartition%d_%d\"`, and `mCascadeNumber` is 3 wherever authored" + E + ":"),
    (RR, "> the depth-of-field blur — along with the paths of the 15 shader files that consume them.",
     "> the depth-of-field blur — along with the paths of the ~~15 shader files~~ 18 `.phyre` assets " + T + "16 under "
     "`shaders`, the font `tuffysdf.fgen` and the map-texture template - §2's count)* that consume them."),
    (RR, "| The 15 asset paths | authored strings",
     "| The ~~15~~ 18 asset paths " + T + "§2)* | authored strings"),
    (RM, "  eyes, tonemap) and the 15 `.phyre` shader assets that consume them.",
     "  eyes, tonemap) and the ~~15~~ 18 `.phyre` ~~shader~~ assets " + T + "the page's §2 count - 16 shaders, a font "
     "and a map-texture template)* that consume them."),
    (RR, "**Shadow — 28 parameters.** Separately tunable",
     "**Shadow — ~~28~~ 32 parameters.** " + T + "the names listed below; 31 occur as strings, `mCascadePartition` only "
     "as a stem)* Separately tunable"),
    (RR, "**Ambient occlusion — 12 parameters**, and the structure",
     "**Ambient occlusion — ~~12~~ 14 parameters** " + T + "the fourteen below, 2 x 2 x 3 + 2)*, and the structure"),
    (RR, "**Water — 16 parameters**, all shipped",
     "**Water — ~~16~~ 18 parameters** " + T + "the eighteen below, each a string in the image)*, all shipped"),
    (RR, "consumes them has not been read. Recorded as **W-1**.",
     "consumes them has not been read. ~~Recorded as **W-1**.~~ " + T + "W-1 is where the values live, answered in "
     "§8b; this arithmetic is not a register row)*"),
    (RR, "  observed: GraphicsAPI = D3D11 ; kind = shaders | font\n",
     "  observed: GraphicsAPI = D3D11 ; kind = shaders | font   " + CC + "and map/<mapcode>/tex - three directories, "
     "section 2\n"),
    (RM, "  middleware behind FFXII's bloom, depth of field and glare. Identity only; no body read yet.",
     "  middleware behind FFXII's bloom, depth of field and glare. Identity only~~; no body read yet~~ " + T + "the "
     "page's H-4 and H-6 read three bodies)*."),
    (RM, "  **DOCUMENTED, tier 2.** **147 post-processing functions named** from authored diagnostics",
     "  ~~**DOCUMENTED, tier 2.**~~ **AUDITED, tier 2.** **147 post-processing ~~functions~~ names** " + T + FM +
     "`status: AUDITED`; 147 is 135 functions and 12 funclets)* from authored diagnostics"),

    # ---------------------------------------------------------------- 3.2.12 / 3.3.12 [CM]
    (PTS, "`0045E930`–`00537410` and `004427D0`\"*; the lowest is **`00442550`**, and **57 of the 75** sit below",
     "`0045E930`–`00537410` and `004427D0`\"*; the lowest is **`00442550`**, and **~~57~~ 46 of the 75** " + T +
     "recount of `members/fade-node-consumers.tsv`'s callers)* sit below"),
    (PTS, "Euclidean in modes 1–2), and the node is the per-object distance-fade colour**: the 75 call sites",
     "Euclidean in modes 1–2), and the node is the per-object distance-fade colour**: the ~~75 call sites~~ 76 call "
     "sites in 75 functions " + T + "§13's census)*"),
    (PTS, "(the draw-side family `0045E930`–`00537410` and `004427D0`) obtain",
     "(the draw-side family ~~`0045E930`–`00537410` and `004427D0`~~ `00442550`–`00537410` " + T + "§11 - the lowest "
     "caller is `00442550`)*) obtain"),
    (PTS, "a scalar.** What each of them then does with that scalar is **not established here**, and this page",
     "a scalar.** What each of them then does with that scalar ~~is **not established here**~~ " + A + "§13 - at every "
     "one of the 76 sites the output is a modulate" + E + ", and this page"),
    (PTS, "Three arms are distinguished; what selects them is the caller's, and no\n  caller was read.",
     "Three arms are distinguished; what selects them is the caller's~~, and no~~\n  ~~caller was read~~ " + A + "§10 - "
     "byte `+1` of the fade record is the distance mode" + E + "."),
    (PTS, "was re-made.** Which axis lane 1 is. What selects the mode",
     "was re-made.** ~~Which axis lane 1 is.~~ " + A + "§9's cross-reference - lane 1 is Y, the up axis" + E +
     " What selects the mode"),
    (PTS, "| `02F97348` | the singleton | 8 B |",
     "| `02F97348` | ~~the singleton~~ the effect container currently being drawn " + T + "§12 - not one object)* | 8 B |"),
    (PTS, "`003820C0` calls scheduling helpers `00229D20` and `00229D60`;",
     "`003820C0` calls ~~scheduling helpers~~ `00229D20` " + T + "the aspect ratio, how-a-camera-reaches-the-renderer.md "
     "`CON-184`)* and `00229D60`;"),
    (SF, "machine `0035CA70`, the skip family (`003601D0`, `003603F0`, `00360480`, `00360710`) and four\n",
     "machine `0035CA70`, the skip family (`003601D0`, `003603F0`, `00360480`, `00360710`) and ~~four~~ six " + T +
     "six are listed)*\n"),
    (SF, "The layer verbs pop two integers and tail-jump into `002EFA70` with the direction and colour",
     "The layer verbs ~~pop two integers and tail-jump into `002EFA70`~~ " + T + "§9's correction - that describes the "
     "`_d` variants `00D0`–`00D2`, not `00B6`–`00B8`)* with the direction and colour"),
    (SF, "The per-helper bodies (`002DED60`, `00360D70`/`00360E50`, `00360C20`,",
     "The per-helper bodies (`002DED60`, ~~`00360D70`/`00360E50`~~ " + A + "the `00360D70` and `00360E50` sections "
     "below" + E + ", `00360C20`,"),
    (AF, "> this pass did not find them.** What is certain is the arithmetic, because it was read.",
     "> ~~this pass did not find them.~~** " + A + "§6, UE-1 answered 2026-09-14 - the three fields branch C writes "
     "have no reader, and \"a consumer re-derives these fields\" is the reading the code supports" + E + " What is "
     "certain is the arithmetic, because it was read."),
    (CR, "(the shipped scripts do pair their 328 starts with 315 clears and 178 stops).",
     "(the shipped scripts do pair their 328 starts with 315 clears and 178 stops " + T + "and 2 more under the plain "
     "`camerashakestop` name, `members/camerashake-census.tsv`)*)."),
    (CR, "328 starts, **all in the two-argument form**, 315 clears, 178 stops, 13 syncs, 6 changes.",
     "328 starts, **all in the two-argument form**, 315 clears, 178 stops, 13 syncs, 6 changes " + T + "and 2 "
     "`camerashakestop` - the TSV's sixth verb row, so 842)*."),
    (CR, "rebuild that follows; `003CBD60` itself was not read. A",
     "rebuild that follows; ~~`003CBD60` itself was not read~~ " + A + "the SWE2-EC7-53 section - `003CBD60` read" + E +
     ". A"),
    (CR, "two base scalars from `002563F0`, steps the table with\n`0037D970`, reads",
     "two base scalars from `002563F0`, ~~steps the table with~~\n~~`0037D970`~~ calls `0037D970` " + T + "§4a's "
     "2026-09-21 section - not a table step; it fills the accumulator rows)*, reads"),
    (CR, "*Still not read:* the table step, `camerashakechange`",
     "*Still not read:* ~~the table step,~~ " + A + "§4a - `0037D970` is read" + E + " `camerashakechange`"),
    (CR, "| `0037D4C0` shake gather (808 B) | base scalars; table step; current draw |",
     "| `0037D4C0` shake gather (808 B) | base scalars; ~~table step~~ the accumulator fill `0037D970` " + T + "§4a)*; "
     "current draw |"),
    (CR, "- What the matrix at the head of the working block is (the extra factor in `02AEDD30` and `02AEDD70`), what the device",
     "- ~~What the matrix at the head of the working block is (the extra factor in `02AEDD30` and `02AEDD70`),~~ " + A +
     "how-a-position-becomes-a-single-number.md - `00382910` builds it with the 512 x 448 PS2 frame size" + E +
     " what the device"),
    (P, "complete. Not read: `00255850` (961 B) and `00257520` (731 B) beyond their calls into record 5 —\nsee §5.",
     "complete. ~~Not read: `00255850` (961 B) and `00257520` (731 B) beyond their calls into record 5 —~~\n~~see §5.~~ "
     + A + "BY-9, answered 2026-09-14" + E),
    (P, "(`0025A3D0`; what consumes it was not traced).",
     "(`0025A3D0`; ~~what consumes it was not traced~~ " + A + "how-a-camera-reaches-the-renderer.md §2 - `00259970` "
     "submits the static default view at priority `0x14`" + E + ")."),
    (P, "The shake channels at `ActorManagerSlot +0x170` share this layout (builder `003DD230`); their tick\nis not read here.",
     "The shake channels at `ActorManagerSlot +0x170` share this layout (builder `003DD230`)~~; their tick~~\n~~is not "
     "read here~~. " + A + "how-a-camera-reaches-the-renderer.md §4a, the shake chain" + E),
    (P, "What BY-7 still owes: the *meaning* of the resolved record's `+0x194`/`+0x198` fields (the roll/fov",
     "~~What BY-7 still owes: the *meaning* of the resolved record's `+0x194`/`+0x198` fields~~ " + A + "BY-7, answered "
     "2026-09-26 - two of the three angles of the bone's added rotation" + E + " (the roll/fov"),
    (MH, "sub-record, then three\none-argument invokes -",
     "sub-record, then ~~three~~ two\n~~one-argument~~ invokes " + T + "`001B7690`+0x2B `0017D960(1)` and +0x38 "
     "`002E1CA0(1, 0x15)`, then the tail `jmp` at +0x46)* -"),
    (MH, "kind-28 lookups were **not** re-derived here;",
     "kind-28 lookups were **not** re-derived here " + A + "the screen-fade page, which re-derives `001B7F30` "
     "(2026-09-25)" + E + ";"),
    (FBF, "*Whose\nposition the stash holds is that page's open runtime item, not settled here.*",
     "*~~Whose~~*\n*~~position the stash holds is that page's open runtime item, not settled here.~~* " + A +
     "how-a-camera-reaches-the-renderer.md - the eye, added at `02AED5F0`" + E),

    # ---------------------------------------------------------------- README status words (front matter rules)
    (RM, "  **PARTIAL, tier 1.** `setResolutionSize` logs the request",
     "  ~~**PARTIAL, tier 1.**~~ **DOCUMENTED, tier 1.** " + T + FM + "`status: DOCUMENTED`, every register row "
     "answered)* "
     "`setResolutionSize` logs the request"),
    (RM, "  **DOCUMENTED, tier 1 (2026-09-12).** How a script's `camerastart`",
     "  ~~**DOCUMENTED, tier 1 (2026-09-12).**~~ **AUDITED, tier 1 (2026-09-12).** " + T + FM + "`status: AUDITED`)* "
     "How a script's "
     "`camerastart`"),
    (RM, "  **DOCUMENTED, tier 1 (2026-09-12).** The **seven screen-fade layers**",
     "  ~~**DOCUMENTED, tier 1 (2026-09-12).**~~ **AUDITED, tier 1 (2026-09-12).** " + T + FM + "`status: AUDITED`)* "
     "The **seven "
     "screen-fade layers**"),
    (RM, "  **DOCUMENTED, tier 1 (2026-09-19), static.** A body shows",
     "  ~~**DOCUMENTED, tier 1 (2026-09-19), static.**~~ **AUDITED, tier 1 (2026-09-19), static.** " + T + FM +
     "`status: AUDITED`)* A body shows"),
    (RM, "  **DOCUMENTED, tier 1 (2026-09-19), static.** The per-frame update of effect element types",
     "  ~~**DOCUMENTED, tier 1 (2026-09-19), static.**~~ **AUDITED, tier 1 (2026-09-19), static.** " + T + FM +
     "`status: AUDITED`)* The "
     "per-frame update of effect element types"),
    (RM, "  **DOCUMENTED, tier 1, crossref-clean.** Every render pass",
     "  ~~**DOCUMENTED, tier 1, crossref-clean.**~~ **AUDITED, tier 1, crossref-clean.** " + T + FM +
     "`status: AUDITED`)* Every render "
     "pass"),
    (RM, "  **DOCUMENTED, tier 1.** Eighteen classes carrying",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + T + FM + "`status: AUDITED`)* Eighteen classes carrying"),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        if new in t or new.replace("\n", "\r\n") in t:
            print("ALREADY", rel.split("/")[-1]); texts[rel] = t; continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING", rel.split("/")[-1], old[:40]); fails += 1; texts[rel] = t; continue
        n = new.replace("\n", "\r\n") if "\r\n" in hit[0] else new
        texts[rel] = t.replace(hit[0], n, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + rel.split("/")[-1])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
