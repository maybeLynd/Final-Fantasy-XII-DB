# Affected-consumer check: UQ-70, filelistlocalin.bin and logicpack.bin decoded (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC. The `ashd` payload's proposed
no-admissible-source disposition needs a non-author reviewer.

**The ruling** (controls in `_index/candidates/uq70-filelistlocalin/`):
- **`filelistlocalin.bin`** is the PS2 disc file list. It has 38 sections `{count; absolute string offsets}` and
  24,358 paths, and section k lists file-size-table kind k's family (`filelistlocalin.py`, 6 checks).
- **`logicpack.bin`** is a pack of `.ard`-format AI logic blocks: 1,147 of its 1,310 records are byte-identical to
  shipped `.ard` AI blocks (`logicpack.py`, 4 checks).
- **`katano/event.bin`** is `ashd`, and the image contains no decoder for it.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` UQ-70 | narrowing prepended, FABLE's 2026-09-26 narrowing kept | revised-here |
| `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/unnamed-bin-families.md` UQ-70 box | the family table's "not decoded" cells for these two families | routed-to-FABLE (page owner) |

Run receipt: `filelistlocalin.py` and `logicpack.py` executed at 62d618787 (FAILS 0).
