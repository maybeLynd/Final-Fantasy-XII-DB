# MapScreenContainer +0x190..+0x1AF: four qword handles filled by one loader (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` MapScreenContainer. Two things were wrong:
- `+0x198 unobservedSpan0198` (8 B), which the field-access index contradicted;
- `+0x1A8 dword01A8` (4 B) followed by `+0x1AC unobservedSpan01AC` (4 B). The field at `+0x1A8` is one qword.

**Result** (`handles.py`, M1–M3):
- **Callers (M1).** `002BA040` and `003CB440` load the container from its own route slots, `0209E5F0` and `02B47760`.
  Both call `00404060` with `rdx = container + 0x190`.
- **Loader (M2).** `00404060` stores four qword handles, returned by `002493D0` / `00249320` for ids 0xB9, 0xBA, 0xB0
  and 0xBF, into `+0x198`, `+0x190`, `+0x1A0` and `+0x1A8`.
- **Why `dword01A8` was 4 bytes.** Its width came from a single dword access, by `002B7590`. That access reads the low
  half of an 8-byte field.

**Store change.**
- `handle198` (void*) replaces the `+0x198` unobserved row.
- `handle1A8` (void*, 8 B) replaces `dword01A8` and `unobservedSpan01AC`.
- The replaced rows are quoted in the new evidence cells.

**Regression.** M3 fails on the pre-fix store and passes after `Tools/work/OPUS/mapscr/patch_store.py`. On a copy,
`types_index.py --validate` reports 0 errors and 0 gaps.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` MapScreenContainer `+0x198`, `+0x1A8`, `+0x1AC` | re-cut; old rows quoted in the evidence | revised-here |
| the unobserved-row audit (`Tools/work/OPUS/silent_unobserved.json`) | this row closed | agrees |

Run receipt: executed at 7238558d8 - `handles.py` M1–M2 PASS; M3 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
