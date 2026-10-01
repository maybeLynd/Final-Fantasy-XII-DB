# WidgetSingleton02CA8F38 +0x148: a dword set to -1 through the object embedded at +0xC0 (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` WidgetSingleton02CA8F38 `+0x140 unobservedSpan0140` (12 B). The field-access index
contradicted it with one write at in-hand base `0xC0`.

**Result** (`w148.py`, W1–W3):
- **The caller passes the embedded object (W1).** `00550540` loads the singleton from its own slot `02CA8F38` and
  calls `00562F90` with `rcx = singleton + 0xC0`.
- **The callee's writes (W2).** `00562F90` writes the object's `+0x10`, `+0x18` and a dword `-1` at `+0x88`.
- **The base checks out.** The first two writes land on the singleton's existing `qword00D0` and `qword00D8` rows. The
  third lands on `+0x148`.

**Store change.** The 12-byte row becomes `unobservedSpan0140 u8[8]` plus `int148 int32`.

**Regression.** W3 fails on the pre-fix store and passes after `Tools/work/OPUS/ca8f/patch_store.py`. On a copy,
`types_index.py --validate` reports 0 errors and 0 gaps.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` WidgetSingleton02CA8F38 `+0x140` | re-cut; old row quoted in the evidence | revised-here |
| the unobserved-row audit (`Tools/work/OPUS/silent_unobserved.json`) | this row closed | agrees |

Run receipt: executed at 7238558d8 - `w148.py` W1–W2 PASS; W3 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
