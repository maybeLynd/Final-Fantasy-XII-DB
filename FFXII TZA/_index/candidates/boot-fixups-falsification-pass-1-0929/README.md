# Consumer check: falsification pass 1 on CONTRACT-boot-fixups (OPUS, 2026-09-29)

corrects: 00-Engine-Core-Runtime/CONTRACT-boot-fixups.md (I3: the frame-base constant is not evaluated once)
corrects: 00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md (the same clause)

## What was corrected

- **I3's "evaluated once".** `02064ACC` has two writers:
  - boot's `0022A1A7`, storing `2 / FrameLimit`;
  - the 7-byte setter `00229F10`.

  The setter has two callers:
  - `002695A0`, reached from the area transition `002628B0`, re-stores `2 / FrameLimit`;
  - `0026DB10`, the native of script verb `mainloopallsyncv` (0x018F, handler `003464B0`), stores `arg / FrameLimit`, or
    `2 / FrameLimit` for a negative argument.

  So every area change restores the default, and a script can set another value.
- **What survives.** The division itself, its values (2 at 30 fps, 1 at 60), the seeds, the two reseed callers, and the
  eleven allocations and nine registrations with their totals.

## Current consumers

- consumer: [what-the-engine-fixes-at-boot.md](../../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md): revised-here.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-158`).
- consumer: `_types/types.tsv` / `fields.tsv` `FrameBaseConstant` agree. They already state "written twice and read once" with
  both writers.
- consumer: `_index/L2-VERDICTS.md` S-01 / S-16 agree. They cite the boot division and the types row, not "once".

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_boot_fixups.py`, checks B0-B4. B3 fails if the setter loses either
caller, or if a caller stops dividing by `01DFE0B4`, which rejects "evaluated once".

run: verified at 67b19a522 (BROKEN 0), against the certified image `73461d08…`.
