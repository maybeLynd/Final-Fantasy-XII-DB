# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-world-loot-pickups-the-ten-slot-pool-and-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-WORLD-LOOT-PICKUPS-THE-TEN-SLOT-POOL-A` · Package: `_index/candidates/fable-world-loot-pickups-the-ten-slot-pool-and-homing-1003/` · Page: `13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md` (commit `c29c5b85e`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the certified image (SHA256 73461D08...); every relative call (`fn`+0xNN) resolved to its target:
  - `003B7440` exact: `003B73B0([02EBCC68])`; signed loop bound `[02EBCC60]` (`jle` skip, `jl` loop); stride-8 walk of `02EBCAC0` skipping nulls; `P` = `00359B80(E)`; `00265020(E, P, P+4, P+8)`, `00265240(E, P+0x10, P+0x14, P+0x18)`; `002E9BE0` byte to `P+0x64`; `00263CC0` to `P+0x34`, `00265200` to `P+0x24`, `00263CC0` again to `P+0x34`.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
