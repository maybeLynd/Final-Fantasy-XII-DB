# Six small "unobserved" rows re-cut from their accessing instructions (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv`, six rows the field-access index contradicts:

| type | row | becomes |
|---|---|---|
| AudioParameterRamp | `+0x28` (8 B) | `float028`, `float02C` |
| GlyphRunWidget1498 | `+0xF4` (4 B) | `word0F4` int16, plus a 2-byte unobserved span |
| GlyphRunWidget1498 | `+0x103` (1 B) | `byte103` |
| PApplication | `+0x50` (8 B) | `double050` |
| Widget0209CC18 | `+0x14C` (4 B) | `dword14C` |
| WidgetSingleton02CA99C0 | `+0x39B` (100 B) | `byte39B`, plus a 99-byte unobserved span |

**Receiver check (S1).** A hit counts only if, in the accessing function, its base register also addresses an
already-named field of the same type, and nothing overwrites that register between the two accesses. Two candidates
failed it and are **left out**: MapRefFieldRow `+0x4` and OrderedCommandList `+0x29`. Rows reached through a nested
base need reading and are left out too.

**Widths (S2).** Each new field takes the width of the instructions that access it, and float, double or integer
according to their mnemonics.

**Regression (S3).** S3 fails on the pre-fix store and passes after `Tools/work/OPUS/smallrows/patch_store.py`. On a
copy, `types_index.py --validate` reports 0 errors and 0 gaps, both alone and combined with the widget-header and
save-queue patches.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv`, the six rows | re-cut; each old row quoted in its first replacement's evidence | revised-here |
| the unobserved-row audit (`Tools/work/OPUS/silent_unobserved.json`) | six rows closed; MapRefFieldRow `+0x4`, OrderedCommandList `+0x29` and the nested-base rows stay open | agrees |

Run receipt: executed at 7238558d8 - `small_rows.py` S1–S2 PASS; S3 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
