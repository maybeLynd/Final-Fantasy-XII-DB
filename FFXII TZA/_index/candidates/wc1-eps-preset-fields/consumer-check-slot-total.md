# Affected-consumer check: WC-1's slot total corrected from 72 to 68 (FABLE, Claude Opus 5.5, 2026-09-27)

**The defect.** The README's totals said 72 slots: 52 roles, 4 read but ignored, 12 padding, 4 in classId 9.
SWE2-DATA's recount (on `FABLE-REQ-SWE2DATA-G3-ANSWERED-BY-WC1`, 6c6a6d3b0) says 68. FABLE re-counted from `fields.tsv`,
the record's own per-slot table, and agrees:
- **68 rows** (SurroundReverb 32, Compressor 8, BuildReverb 8, Filter 4, SideChainInput 4, SimpleFilter 4,
  GranularPitchShift 4, the classId-9 nop arm 4);
- **52** roles;
- **5** read but ignored (SurroundReverb's five EQ band type codes);
- **7** padding (SideChainInput `+4`..`+0xC`, SimpleFilter and GranularPitchShift `+8`/`+0xC`);
- **4** in classId 9.

The per-slot table was right, and only the summary line was wrong.

affected: _index/candidates/wc1-eps-preset-fields/README.md (the Totals line)
run: controls.py in this folder at a94e63b6f reproduces controls.out; the recount reads fields.tsv (68 rows) and is the sensitivity check - 72 is not reachable from the table.

| consumer | what it said | state |
|---|---|---|
| `_index/candidates/wc1-eps-preset-fields/README.md`, Totals | 72 / 52 / 4 / 12 / 4 | revised-here: struck and restated 68 / 52 / 5 / 7 / 4 |
| _index/OPEN-QUESTIONS.md WC-1 | "52 of 72 slots have a role" | revised-here: 72 struck, 68 with the split |
| `18-Audio/Sound-Bank-And-Voice-Formats/sead-win-config.md` sections 6d/7 (SWE2-DATA, 6c6a6d3b0) | 68, 52 / 5 / 7 / 4 | agrees (it is the recount) |
| `_index/candidates/wc1-eps-preset-fields/fields.tsv` | one row per slot | agrees; unchanged |

Regenerated with it: nothing.
