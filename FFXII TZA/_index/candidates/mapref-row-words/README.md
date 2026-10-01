# MapRefFieldRow +0x04 / +0x06: two words read through the row's own route (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` MapRefFieldRow `+0x0004 unobservedSpan0004` (4 B, "not read by the weather path").
The field-access index shows word reads at `+0x04` and `+0x06`.

Mechanical receiver check: the batch check in `small-unobserved-rows/` could not tie these reads to the type, because
the getters touch no other field through the same register. This record proves the receiver another way, from the
row's own route.

**Result** (`rowwords.py`, R1–R3):
- **The row is formed from the route (R1).** `00264ED0` and `00264F90` load the header from the slot `02099D88`, the
  same slot the route's own site `0026D910` loads. Each forms the row as `header + *(int32*)(header+4) + id * 8`, the
  route's RELOFF array with stride 8.
- **The reads (R2).** `00264ED0` returns the word at row `+4` and `00264F90` the word at `+6`. `0026DB30` forms the row
  the same way and reads `+6`.

**Store change.** The 4-byte row becomes `word04 uint16` and `word06 uint16`. The shipped values quoted in the old row
fit that split: row 0's dword `0x00010000` is `+4 = 0x0000`, `+6 = 0x0001`, and row 1's `0x00010001` is `0x0001`,
`0x0001`. Meaning is not claimed.

**Regression.** R3 fails on the pre-fix store and passes after `Tools/work/OPUS/mapref/patch_store.py`. On a copy,
`types_index.py --validate` reports 0 errors and 0 gaps.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` MapRefFieldRow `+0x0004` | re-cut; old row quoted in the evidence | revised-here |
| the unobserved-row audit (`Tools/work/OPUS/silent_unobserved.json`) | this row closed | agrees |

Run receipt: executed at 7238558d8 - `rowwords.py` R1–R2 PASS; R3 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
