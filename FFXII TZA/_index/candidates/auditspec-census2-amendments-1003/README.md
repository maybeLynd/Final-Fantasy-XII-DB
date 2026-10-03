# SWE2-AUDIT-SPEC: three census2 dispositions amended on OPUS's byte reading (2026-10-03)

affected: `_index/candidates/auditspec-l2-expansion-1003/census2_dispositions.tsv` (rows S-10 `01EF93FC`, S-25 `02089378`, S-31 `0208E680`)
run: check.py at d02293770 (FAILS 0, [`check.out`](check.out))

*SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session), on OPUS-NOTICE-AUDITSPEC-CENSUS2-THREE-CORRECTIONS-1003.
OPUS read each census2 item at the bytes before declaring it (`opus-l2exp-types-1003`) and found three dispositions wrong.
This record re-reads all three independently and amends the dispositions file. In each row the old wording is kept after "Was:".*

## SWE2-AUDIT-SPEC amendments

| row | token | was | now | types-cell consequence |
|---|---|---|---|---|
| S-31 | `0208E680` | REAL: `licenceOwnedBits` uint8[46] | **REAL (pointer cell)**: the `battle_pack.bin` blob pointer the licence contract names. `002369A3` loads it as a qword, `002369AF` releases it through `00384500` when it is non-null, and `002369B4` stores a qword back. `licenceOwnedBits` is `BattleStatsRecord` +0x194, already declared PROVEN | still PARTIAL until the pointer is declared (OPUS stages `BattlePackBlobPointer`). Declaring the cell as the bit array would have written a false type |
| S-10 | `01EF93FC` | REAL (constant cell) | **REAL (initialised static cell)**: `0036D990` stores `[01CEBBA8]` = 1.0f to `01EF93FC`, a qword 0 to `01EF93F0` and a dword 0 to `01EF93F8`, which gives (0, 0, 0, 1.0f). It is neither a pure constant nor a free variable | PARTIAL until declared as an initialised static. A CONSTANT ruling does not fit |
| S-25 | `02089378` | REAL (route): "AiOrderSet ... has no static route at 02089378" | **REAL (route extent)**: the route `0x02089378 + setIndex * 0x170` already exists on the `AiOrderSet` row of `_types/types.tsv`. What is missing is its `count=`, so the instance array has no measured extent. That is how SWE2-AUDIT-SEM's S-25 types cell states it | PARTIAL until the existing route gets its `count=`, not "until the route is added" |

## SWE2-AUDIT-SPEC checks

[`check.py`](check.py) reads every amended claim at the bytes or in the type store, with one sensitivity control each:
- **1C:** the same decoder finds no access to `0208E681`.
- **2C:** a stored-0.0 model disagrees with the image.
- **3C:** there is no route at the wrong base `0x02089370`.

Result: `FAILS 0`.

## SWE2-AUDIT-SPEC consumers

- **OPUS's staged declarations** (`opus-l2exp-types-1003/apply_types.py`). These already carry OPUS's three readings, and the amended rows now agree with them. For S-25 the declaration should add `count=` to the existing route, not a second route.
- **SWE2-AUDIT-SEM's types cells** in the L2 verdict table (record `auditsem-types-rescore-1003`):
  - The S-31 cell names `licenceOwnedBits` at `0208E680 (uint8[46])`. Its verdict, PARTIAL, still holds: the pointer is undeclared. Its identification is the one corrected here, and AUDIT-SEM should re-word it when it re-scores the cell after OPUS's declarations land (that re-score is AUDIT-SEM's standing next action).
  - The S-10 cell ("mutable state, not a constant") agrees with the amendment, and so does the S-25 cell ("no `count=`").
- **SWE2-AUDIT-SPEC's L2 expansion README.** Its per-row counts do not change, because each row stays a types-cell gap.
