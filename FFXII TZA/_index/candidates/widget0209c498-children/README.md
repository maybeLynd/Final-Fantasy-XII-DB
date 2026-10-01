# WidgetSingleton0209C498: two child widgets of 0x148 at +0x160 and +0x2A8 (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` WidgetSingleton0209C498, four rows: `+0x160 qword0160`, `+0x168 unobservedSpan0168`
(320 B), `+0x2A8 qword02A8` and `+0x2B0 unobservedSpan02B0` (320 B). The field-access index contradicted both spans
with 75 hits each, all at in-hand bases `0x160` and `0x2A8`.

**Result** (`children.py`, C1–C3):
- **Two in-place widgets.** `0029D4D0` builds two widgets in place with `00245000`, at `[0209C498] + 0x160` and
  `+ 0x2A8`. Both are 0x148 bytes and use the handler `0029D550`.
- **The spans hold the base fields.** The index hits are the shared widget code (`002482E0`, `00244DD0`, the
  initialiser `002465F0`) reading and writing each child's base fields.
- **They tile exactly.** The two children fill `+0x160..+0x3EF`.

**Store change.** Two rows, `childWidget160` and `childWidget2A8`, each typed `Widget` and 0x148 bytes long. The
convention is the one widget-derived types use for their own base, applied here to whole embedded children.

**Regression.** C3 fails on the pre-fix store and passes after `Tools/work/OPUS/c498/patch_store.py`. On a copy,
`types_index.py --validate` reports 0 errors and 0 gaps, both alone and with the widget-header patch
(`widget-header-embedding/`) applied as well.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` WidgetSingleton0209C498 `+0x160..+0x3EF` | 4 rows → 2 embedded children; old rows quoted in the evidence | revised-here |
| the unobserved-row audit (`Tools/work/OPUS/silent_unobserved.json`) | this type's two 320-B rows closed | agrees |

Run receipt: executed at 7238558d8 - `children.py` C1–C2 PASS; C3 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
