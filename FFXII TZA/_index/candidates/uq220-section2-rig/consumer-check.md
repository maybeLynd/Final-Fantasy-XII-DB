# Affected-consumer check: UQ-220 answered; FCP section 2's slot domain named (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `uq220_section2_rig.py` beside this file (8 checks, FAILS 0).

SWE2-DATA's 2026-09-21 layout of FCP section 2 left the 19-slot key domain unnamed and called the `@FTR` node table
"the prime suspect". It is not. Section 2 is copied to the resource entry's `+0x94`, which is the rig, and the rig's
slot initialiser treats slot *n* as controller *n*. Of the 19 slots:
- slots 0–3 and 5–16 are initialised;
- slot 4 is authored in 52 blocks but not initialised;
- slots 17 and 18 are empty in all 1,066 blocks.

| consumer | what it said | state |
|---|---|---|
| `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md`, section 2 layout | "their key domain (the 19 slots) is not yet named … the FTR node table is the prime suspect" | revised-here (struck; the domain is named beside it) |
| same page, the `UQ-220` box | open; residue "the section-2 slot domain and record semantics, and the FTR-side consumers of the copy" | revised-here (ticked, answer beneath; record semantics routed to the rig page's section 7, section 8's copy to `UQ-218`) |
| same page, the section-2 `struct` block (`u32[19] slotOffset`, the 68-byte anchor, the `0x90` self-offset) | the layout | agrees (the control reads the same `u32[19]` table; the initialiser's `-1` tests fall on the anchor's two `i32 -1` fields) |
| `17-Presentation-Rendering/Character-Render-Records/the-rig-of-seventeen-controllers.md` §2 | the rig at entry `+0x94`; controller *n* at `+4n`; 0–16 named; 4 "nothing" | agrees; revised-here with a dated "where the rig comes from" note (authored section 2; slot 4 authored in 52 files; slots 17 and 18) |
| `17-Presentation-Rendering/Model-And-Motion-Formats/the-pose-sequencer.md` | section 7 is the pose sequencer | agrees (cited as section 7's answer) |
| `17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md` | the skeleton-side record it is handed is the rig | agrees (slot 0, the sway, is initialised like the others) |
| `_index/OPEN-QUESTIONS.md` UQ-218 | the other `@Fx` entries and the `@FTR` path | agrees; unchanged. Its FTR-side question is not closed by this: section 8's copy readers stay there |
| `_index/OPEN-QUESTIONS.md` UQ-220 | PARTIAL | revised-here (ANSWERED; the previous status kept as history) |
