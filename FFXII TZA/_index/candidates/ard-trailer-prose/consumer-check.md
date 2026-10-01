# Affected-consumer check: the `.ard` `+0x0C` trailer is read — FABLE's pages updated (FABLE, Claude Opus 5.5, 2026-09-26)

affected: CC-5; 02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md

**Regression:** OPUS's `_index/candidates/cc5-ard-trailer/cc5_trailer.py` (PASS).

run: cc5_trailer.py at 1e7da4065 (PASS: 163 unique files, 140 trailers, 23 without), 2026-09-26.

**The correction.** OPUS answered CC-5's trailer on 2026-09-27 (`OPUS-REQ-FABLE-ARD-TRAILER-READ-BY-NOTHING-PROSE`).
- The trailer is `{u32 count; {u32 key; u32 mask}[count]}`, read through the root accessor by the per-name
  flag-mask walkers.
- FABLE's pages still said it is "read by nothing" and that slot 7 and the trailer were CC-5's residue.
- Slot 7 had already been answered by FABLE as CC-10.

| consumer | what it said | state |
|---|---|---|
| `…/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md` ~416 | "Slot 7 and the `+0x0C` trailer remain CC-5's residue." | revised-here (struck; both answered) |
| same ~461 | "`trailerOff` … is read by nothing" | revised-here (struck; read through the root accessor) |
| same, CC-6 blockquote | "Since nothing in the shipped engine reads `+0x0C`, nothing depends on the answer" | revised-here (struck; a reconstruction must implement the walk) |
| same ~509 | "`trailerOff` read by nothing" as a second dead-capacity instance | revised-here (struck) |
| `02-Resource-And-Asset-Pipeline/CONTRACT-ard-area-binder.md` §14 | "What the trailer at `+0x0C` holds, given the loader never reads it." | revised-here (struck; answered by OPUS) |
| `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` ~1460 | slot 1's "container format is CC-5's residue" | revised-here (struck; slot 1 answered 2026-09-12) |
| `_index/OPEN-QUESTIONS.md` CC-5 | ANSWERED (OPUS) | agrees |
