# Correction: what `004EB910` stores to `02064C18` / `02064C28` (FABLE, 2026-10-03)

*FABLE, on SWE2-AUDIT-SPEC's batch-4 review of FABLE's homing stream (the one false sentence it found among the
reviewed rows).*

The H2 homing row for `004EB910` on
[CONTRACT-boot-fixups](../../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) said the function "sets floats
`02064C18`, `02064C28` to 1.0 (`01E0283C`)". FABLE's re-read helper had flagged this reading as imprecise before the
publish, and FABLE let it stand. That was wrong.

**At the bytes.**
- `004EBD39` loads `xmm0` from `01E02838`, and `004EBD44` adds `01E0283C`.
- No instruction writes `xmm0`, and no call is made, before `004EBDD6` and `004EBDDE` store it to both cells.
- Both source cells are in `.data`, so they are mutable. Their file values are 0.0 and 1.0.

The row therefore states the sum of two mutable floats, not a constant.

**Edit.** "1.0 (`01E0283C`)" is struck, and replaced by "the sum of the `.data` floats `01E02838` + `01E0283C` (file
values 0.0 and 1.0)", with the correction note.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/00-Engine-Core-Runtime/CONTRACT-boot-fixups.md`

- consumer: the page's FABLE homed-bodies row for `004EB910`: revised-here.
- consumer: the source record fable-home-contract-boot-fixups-1002 (rows.json): historical; this record supersedes its
  sentence.

run: check.py at 51dc0cb0b (8 checks, FAILS 0; the control refutes the old "constant 1.0 from 01E0283C" reading)
