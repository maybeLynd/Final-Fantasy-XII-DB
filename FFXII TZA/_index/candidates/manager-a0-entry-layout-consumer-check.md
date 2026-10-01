# Affected-consumer check: ManagerSub00A0Entry re-tiled (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` ManagerSub00A0Entry. OPUS declared four rows on 2026-09-18: `+0x00 ptr0000` (void*),
`+0x08 unobservedSpan0008`, `+0x10 ptr0010` (void*) and `+0x18 unobservedTail0018` (232 bytes, "no access").

**Question.** An audit of DISCOVERED "no access" rows against the store's own field-access index flagged this type.
The index lists 31 accesses by five functions inside the "unobserved" tail. Are those real accesses of the entry, or
misattributions? The same audit found misattributions on bank-generic routes (`route-collision-002ED570/`).

**Discriminator, read from the code.** Does the function reach the entry through the pointer the entry's own code
forms, `parent + 0x20 + (i << 8)`?

**Result** (`manager-a0-entry-layout/a0_entry_layout.py`, L1–L5):
- **Initialiser.** `003F9390` forms the entry itself and writes `+0x20`..`+0xF0` (L4).
- **Reset.** `003F00F0`'s only caller passes the entry. It writes `+0x0C`, `+0x10`, `+0x60..+0x6C`, `+0x70`, `+0x80`,
  `+0xEC` and `+0xF0` (L3).
  - `+0x60..+0x6C` hold (cos a, sin a, −sin a, cos a), computed through the `cosf`/`sinf` imports.
  - `003F1230(entry, a)` rewrites only those four floats.
- **List append.** `003F1290` makes the entry a list **node**, with next/prev at `+0xD0/+0xD8`. Its `[rcx]` and
  `[rcx+0x10]` accesses are to the list **head** (L1).
- **The old pointer rows were wrong.** 2026-09-18's `ptr0000`/`ptr0010` came from exactly those head accesses. The
  entry's `+0x00..+0x0F` is a float vector with w = 1.0 (L2).

**New tiling.** 22 rows, 0x100 bytes, no gaps. 90 bytes stay unobserved: `+0x84..+0xCF`, `+0xEA`, `+0xF4..+0xFF`.
Every meaning is marked not claimed except the list links and the stored cos/sin values.

**Regression.** L5 fails on the pre-fix store and passes after `Tools/work/OPUS/a0entry/patch_store.py`. That was
tested on a copy; `types_index.py --validate` then reports 0 errors and 0 gaps.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` ManagerSub00A0Entry (4 rows → 22) | re-tiled; the four old rows kept verbatim in the first new row's evidence | revised-here |
| `00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md` residue table (`+0x18`, 232 B) | row struck with a dated note (OPUS's own text of 2026-09-19) | revised-here |
| `_types/README.md` "94 % unexplained … neither is built" | dated correction appended (OPUS's own text) | revised-here |
| `_types/types.tsv` ManagerSub00A0Entry evidence ("003F1290 touches only +0x00 ... and +0x10") | dated correction appended by `Tools/work/OPUS/a0entry/patch_types.py` | revised-here |
| `_index/TYPE-COVERAGE.md` | generated; the next `types_index.py --coverage` run refreshes it | agrees |
| the list head `003F1290` receives in `rcx` (0028EAB0 and 14 other callers) | not typed here; the old `+0x00`/`+0x10` facts describe it | routed-to-OPUS-follow-up |

Run receipt: executed at bbd3af82a - `a0_entry_layout.py` L1–L4 PASS, L5 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
