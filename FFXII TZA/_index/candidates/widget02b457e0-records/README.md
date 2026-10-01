# WidgetSingleton02B457E0: +0x120 is two 0xA8-byte records (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` WidgetSingleton02B457E0 `+0x120 unobservedSpan0120` (336 B, "declared gap"). The
field-access index contradicted it with 48 hits, at in-hand bases `0x120` and `0x138`.

**Result** (`records.py`, R1–R3):
- **The teardown walks two records (R1).** `003C2210` starts at `this + 0x120`, with stride `0xA8` and count 2. For
  each record it:
  - releases every slot of the qword array at `+0x18` through `0024A680` and nulls it, up to the count byte at
    `+0x13`;
  - zeroes the count;
  - releases the `+0x00` handle through `003697F0` and nulls it.
- **The layout closes at `+0x270` (R2),** the next declared row.

**Store change.**
- A new type, `WidgetSingleton02B457E0Record` (0xA8, `EMBED ... +0x120 stride=0xA8 count=2`).
- Its rows are `handle00`, `qword08`, `byte10`, `byte12`, `slotCount13` and `slots18 void*[18]`, plus two small
  unobserved spans.
- The parent row becomes `records120 Record[2]`.
- The slot-array bound of 18 comes from the layout only.

**Regression.** R3 fails on the pre-fix store and passes after `Tools/work/OPUS/b457/patch_store.py`. On a copy,
`types_index.py --validate` reports 0 errors and 0 gaps.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` WidgetSingleton02B457E0 `+0x120` and the new record rows | re-cut; the old row quoted in the evidence | revised-here |
| `_types/types.tsv` | record type added | revised-here |
| the unobserved-row audit (`Tools/work/OPUS/silent_unobserved.json`) | this 336-B row closed | agrees |

Run receipt: executed at 7238558d8 - `records.py` R1–R2 PASS; R3 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
