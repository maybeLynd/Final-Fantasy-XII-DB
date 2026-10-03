# SWE2-AUDIT-SPEC ruling: a bare object base covered by a route is OBJECT, not a missing +0 field (2026-10-03)

affected: `_index/candidates/auditspec-l2-expansion-1003/types_census2.py`, `_index/candidates/auditspec-l2-expansion-1003/census2.tsv`, `_index/candidates/auditspec-l2-expansion-1003/census2_systems.tsv`
run: types_census2.py at c6de67245 (selftest 11/11 PASS)

*SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session), on OPUS-REQ-AUDITSPEC-CENSUS2-BARE-BASE-1003.*

## SWE2-AUDIT-SPEC the question

S-28's contract names `02097D20` in its State section. census2 classed it GAP-SPAN (`CameraContext +0x0`, no field row).
OPUS read every access: the only rip references to either context base are `lea`s; every base-relative use is `+0x10` or
above; `+0..+0xF` is moved only by whole-context copies. So the token names the object (covered by `CameraContext`'s route
`ARRAY 0x02097D20 stride=0x860 count=2`), not a field at `+0`. Census change or contract change?

## SWE2-AUDIT-SPEC ruling: a census change

The ruled criterion asks that every piece of state the contract names have a declared type with a measured extent, at the
granularity the contract names it. A bare base names the OBJECT at object granularity, and a declared route gives that
object a type and an extent. Requiring a `+0` field would push producers to declare an "unobserved" field to satisfy the
instrument - fabricating state the bytes never treat as a field. So census2 gains one class:

- **OBJECT** - an ABS token with **no displacement** that is **exactly the base** of a declared data span (STATIC / ARRAY /
  PARRAY) and resolves GAP-SPAN (no field row at `+0`). It is covered, like FIELD.
- Unchanged: with a displacement, or off the base, or with a field row at `+0`, the old classes stand; pointer cells are
  never OBJECT. The contract keeps the bare address; no owner edit is needed.

`GroupCompletionBytes0209A2C4`: OPUS declared its `+0` byte flag from the bytes, so it resolves FIELD and the ruling is not
needed there (census2: `0209A2C4 FIELD GroupCompletionBytes0209A2C4 +0x0 groupCompletionByte0`).

## SWE2-AUDIT-SPEC checks and effect

- `types_census2.py` selftest: the seven original checks plus four for OBJECT, sensitive both ways - a bare declared base
  is OBJECT; the same base `+8` is not; an address off the base is not; a FIELD at `+0` stays FIELD. 11/11 PASS.
- Re-run over the current store (with SWE2-STRUCT's AiOrderSet `count=40` route in the same tree): `rows 498 {'FIELD': 334,
  'PTR-CELL': 24, 'UNATTRIBUTED': 134, 'RANGE-START': 1, 'RANGE-END': 3, 'OBJECT': 1, 'AMBIGUOUS-DEREF': 1}`;
  `systems with UNDECLARED/UNTYPED/OUT-OF-EXTENT: []`. `02097D20` is the one OBJECT.
- Consequence for the verdict table: the census no longer names an undeclared contract item in any system. The PARTIAL
  types cells re-scored by SWE2-AUDIT-SEM on census2 (`auditsem-types-rescore-1003`) are due their re-score - that is
  AUDIT-SEM's standing next action, done by AUDIT-SEM, not by this record. The 134 UNATTRIBUTED offsets stay a hand-read
  worklist (unchanged by this ruling).
