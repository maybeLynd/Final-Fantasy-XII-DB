# LegacyPs2GsReferenceDescriptor +0x02: a signed word read through the descriptor array (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` LegacyPs2GsReferenceDescriptor `+0x0000 unobservedSpan0000` (4 B). The field-access
index contradicted it with an indexed read at `+0x02`.

**Result** (`refdesc02.py`, G1–G3):
- **The element is this type (G1).** `003A6FC0` loads the array base from the context's `+0x178`, the pointer this
  type's route is `CHAIN`ed on. It forms each element as `index × 0x30`, the element stride.
- **The read (G2).** It reads the word at element `+0x02` sign-extended, then shifts it left by 6 (×64).

**Store change.** The 4-byte row becomes `unobservedSpan0000 u8[2]` plus `word02 int16`. What the scaled value indexes
is not claimed.

**Regression.** G3 fails on the pre-fix store and passes after `Tools/work/OPUS/refdesc/patch_store.py`. On a copy,
`types_index.py --validate` reports 0 errors and 0 gaps.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` LegacyPs2GsReferenceDescriptor `+0x0000` | re-cut; old row quoted in the evidence | revised-here |
| the unobserved-row audit (`Tools/work/OPUS/silent_unobserved.json`) | this row closed | agrees |

Run receipt: executed at 7238558d8 - `refdesc02.py` G1–G2 PASS; G3 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
