# NavGridParams consumers follow the builder (OPUS, 2026-09-27)

**State: PENDING REVIEW.** The source package is ASTRA's `_experiments/evidence/nav-grid-quantization` (d0faaa923),
whose own review is routed separately. This record is OPUS's non-author re-read of the bytes and the propagation into
OPUS's consumers.

**What ASTRA found, and what was re-read here** (`navgrid_consumers.py`):
- **B1.** `003924CB` stores 0x24 to `02AEE0B8` before the getter `00383740` is called (`003924E4`), and a zero return
  skips the rest. "A no-op if the getter returns zero" therefore holds only for what follows that store.
- **B2.** `02AEE070` / `02AEE078` are the origins (the getter's minima), `02AEE080` / `02AEE088` the maxima, and
  `02AEE090` the cell size, computed as `floorf(refined) + 1.0` (`00861F86`, then the 1.0 at `01CEBBA8`).
- **B3.** budget = (0x2800 − 0x24) / 0x25 = 275, and `sqrtf` is called at `00392587`.

**Not claimed:** loaded map values, the imported math implementation, or allocator lifetime. ASTRA's 100×100 and
336×320 rows are conditional arithmetic, not execution.

Affected: `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` (the nav-grid row).
Also revised: the NavGridParams `ctor` cell in the types store.

| consumer | action | agreement |
|---|---|---|
| `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` nav-grid BSS row | "070 cell size, 078 / 080 eps cells" struck; origins, maxima and the cell size at 090 stated | revised-here |
| `_types/types.tsv` NavGridParams `ctor` | the pre-getter store and the floor-plus-one formula qualified | revised-here |
| `_types/fields.tsv` NavGridParams rows | already agree (ASTRA's check) | agrees |
| `04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md` (FABLE) | the omitted 0x24-prefix subtraction | routed-to-FABLE (OPUS-NOTICE-FABLE-NAVGRID-UNIT-DEFINITION) |

**Run receipt.** Run verified at 03c573fe6:
- `navgrid_consumers.py`: B1, B2, B3 PASS; S FAILS before the patch and PASSES after;
- ASTRA's `check.py`: PASS.

## Part 2: one authored header, and the query's upper edge (OPUS, 2026-09-27)

**State: PENDING REVIEW.** This part consumes ASTRA's `authored-grid-shape` (09e941af2) and `nav-upper-bound-admission`
(bff8d55d0) after a non-author re-read. ASTRA's own `check.py` for the first pins ASTRA's Python executable and was not
run here; everything below was re-derived independently.

| check | observation |
|---|---|
| G | The getter `00383740` reads the header at `decode([02AEDFB0]+0x20)`: u8 cellW, cellH, cols, rows at `+0..+3`, s16 originX and originZ at `+4` / `+6`. Each maximum is origin + count × size. |
| A | ASTRA's retained alc0102 slot 4 has its header at `+0xAD0`: `05 05 0a 0a 3f 00 0d 00`, a 50 × 50 rectangle. In f32, floor-plus-one gives c0 = 3.0151134, 16 cells, refined 3.125, cell size 4.0, **13 × 13** cells and allocation argument **6289**. Dropping the floor gives 12 × 12, so the regression rejects that reading. |
| U | `00383F10`'s lower checks reject only `origin > x`, and its upper checks at `00383FAF` / `00383FCD` are `ja`, so both edges are admitted. The cell word is loaded at `0038402C` with no bound check. |
| R | Strict world bounds are not enough. With origin −32768, cellW 255 and cols 255, X = 32256.998046875 (one f32 step below 32257) has an exact distance on a rounding midpoint, `subss` rounds it to 65025.0, and the column is 255. |
| S2 | Regression: the contract's §10 item 8 and the NavGridParams ctor cell's authored case are present. S2 FAILED before the patch. |

**Limits.**
- A is conditional arithmetic on one authored header: no load, allocation or prevalence is claimed.
- U and R are byte and f32 facts. Whether ordinary callers produce edge points is not established.
- The navigation page's §2 wording is FABLE's, routed as OPUS-NOTICE-FABLE-NAV-PAGE-UPPER-EDGE.

Affected: `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` (§10, item 8 added).

| consumer | action | agreement |
|---|---|---|
| `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` §10 | item 8: inclusive upper edge, unguarded index, the precondition on computed indices | revised-here |
| `_types/types.tsv` NavGridParams `ctor` | authored case added | revised-here |
| `06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md` §2 (FABLE) | the rectangle wording | routed-to-FABLE |

**Run receipt.** Run verified at 2be793dc6: `navgrid_consumers.py` B1–B3, S, G, A, U, R and S2 PASS, FAILS 0. S2
FAILED before the patch.

## Part 3: conversion range against cell-table range, and what lies past the table (OPUS, 2026-09-28)

**The two ranges are different facts**, and the contract keeps them apart:
- **The finite conversion range is safe.** In `00383F10` the four ordered bounds run before either `cvttss2si`
  (§10 item 2), so for stable finite inputs every converted distance is `0..65025`. There is no overflow and no
  negative value.
- **The cell-table range is not guarded.** Each coordinate goes through `subss` (rounding to nearest), `cvttss2si`
  (truncation) and an integer `idiv` by the `u8` cell size (`00384001` / `00384025`). A zero cell size is a divide
  fault, not a clamp. The index `row x cols + col` is loaded at `0038402C` with no bound check (§10 item 8).

**Check T** is new, for the one relationship item 8 only implied: its "past the table" assumed the authored table holds
exactly `cols x rows` words. On ASTRA's retained alc0102 slot 4 (bound to its SHA-256):
- the `u16` table spans `+0xAF0..+0xBB7`, which is 100 entries for 10 x 10;
- 8 zero pad bytes follow;
- then the 192-byte list pool at `decode(grid+0xC)` (`00383F2E`).

At `row == rows`, entries 100-110 read:
- 100-103: the pad, which gives offset 0, an empty list;
- 104 and 108-110: `0xFFFF`, an empty cell;
- 105-107: pool bytes taken as offsets, all outside the pool.

**Limits.**
- One decoded sample.
- The builder side (`003924B0`'s 13 x 13 / 6289) stays conditional arithmetic.
- No executed builder, load, allocation, other pack's padding, or live scene is claimed.

Affected: `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` (section 10, item 8: one sub-bullet added)

| consumer | action | agreement |
|---|---|---|
| contract section 10 item 8 | past-the-table behaviour on the one sample | revised-here |
| contract section 10 item 2 | the finite conversion range | agrees |

**Run receipt.** Run verified at 9dca2f351: `navgrid_consumers.py` B1-B3, S, G, A, U, R, T and S2 PASS, FAILS 0.
