# A flow-aware CharacterRenderRecord census, and five spans it cuts (OPUS, 2026-09-27, BT-2)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**Why.** `character-render-record-accesses.tsv` (OPUS, 734d34df6) tracks registers linearly. 9a07bdaab showed that it
drops accesses when a base register is redefined on another path, and that it invents rows when a register's value is
carried across a branch. This is a second instrument beside it, not a replacement. The old file stays as a dated
result.

**Method** (`crr_flow_census.py`): a must-analysis per function, over its control-flow graph.
- **State:** each register maps to "record base + k on every path".
- **Seeds:**
  - pool formation, idx × 0x740 plus the base at `[022C6F28]`, in either order;
  - a call site that passes record + k in rcx / rdx / r8 / r9. Each distinct (argument, k) is analysed separately,
    iterated over the call graph to a fixpoint.
- **Transfer:**
  - mov and lea copy or offset the base;
  - add or sub of an immediate moves k;
  - a cmov into a tracked register keeps it (null-or-record);
  - a call kills the volatile registers;
  - any other write kills.
- **Joins** take the intersection.

**Result.** 2,889 accesses in 487 functions, from 345 argument seeds; every field is inside the record.
- It agrees with the linear census on 2,438 sites.
- 451 sites are in this census only, and 224 are in the linear census only. The latter are reached through
  memory-loaded pointers and spills, which this census does not follow.

**Positive controls:**
- P1: it finds `002EDF90`'s four literal `+0x6C8` stores, which the linear census dropped.
- P2: no field falls outside the record.

**Re-cuts** (`crr_flow_check.py` N1, N2, S; the old rows are kept in the evidence cells):
- **`+0x5F5` and `+0x5F6`.** These are bytes +5 and +6 of the `+0x5F0` sub-object.
  - `0046CC70` reads them separately (`0046CDD1`, `0046CDC9`) and passes them to `002E9D90`.
  - One word store of `0x0C00` (`0046CDC3`) defaults them to 0 / `0x0C` when the mode argument is 1.
  - The receiver chain is in the bytes: `0046CBB0` forms the record from the pool, adds `0x5F0` and calls `0046CC70`.
- **`+0x4CE`, `+0x4D6`, `+0x4DE`, `+0x4E6`.** These are word 3 of presentation-channel entries 1–4, in the 8-byte
  (4 × int16) array whose entries 0 and 5 already declare word 3.
  - `003E5D30` writes entries 0, 1 and 4 whole, with qword `0x1000`.

DISCOVERED in CharacterRenderRecord falls from 176 bytes in 37 spans to 166 bytes in 32.

**Other hits in the old spans.** They are blocks already documented as carried by a 16-byte move (`+0x61E`, `+0x62E`,
`+0x68C`), or address formations (`lea`), not accesses.

**Limits.** The census does not follow:
- pointers loaded from memory (a record pointer held by another object: for example `00429140`'s `+0x110` store, and
  `00417110`'s entry `+0x2E0`);
- stack spills;
- return values;
- indexed operands.

So an unhit span is still not proven untouched.

**Follow-up.** The 451 census-only sites are accesses the linear census missed on already-declared fields. They should
be checked against their rows' widths and writer lists. That is not done here.

**Run receipt:** `crr_flow_check.py`:
- FAIL (S) on the store before the re-cut;
- after it, P1–P2, N1–N2 and S PASS, FAILS 0 (2026-09-27);
- `types_index --validate` on the patched copy: 0 errors, 0 gaps.

`crr-flow-accesses.tsv` holds the census rows.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` CharacterRenderRecord `+0x5F5` (split into `+0x5F5` / `+0x5F6`), `+0x4CE`, `+0x4D6`, `+0x4DE`, `+0x4E6` | replaced; the old rows are kept | revised-here |
| `_index/OPEN-QUESTIONS.md` BT-2 | narrowing prepended; row stays OPEN | revised-here |
| `17-Presentation-Rendering/Character-Render-Records/character-render-record-accesses.tsv` | kept as a dated result; this census sits beside it | agrees (second instrument) |
