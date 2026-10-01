# OrderedCommandList +0x29: a byte flag around the class-filtered walk (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` OrderedCommandList `+0x0029 unobservedSpan0029` (2 B, "read by nothing found"). The
field-access index shows byte writes and reads at `+0x29`. The mechanical receiver check in `small-unobserved-rows/`
could not tie them to the type, because each access follows a getter call. This record proves the receiver through
that getter.

**Result** (`flag29.py`, O1–O3):
- **The getter returns this type (O1).** `0018B4E0` returns `[01F7F5E0]`, the lazily created singleton slot the
  route names, creating it on demand through `0016D6A0`.
- **The flag (O2).** `001F3570` sets byte `+0x29` to 1 on entry, runs the class-filtered walk `0018B1B0`, and clears
  it afterwards. `001E2AF0` reads it. Every access is a byte access through the getter's return.

**Store change.**
- `+0x29` becomes `walkFlag29 uint8`.
- `+0x2A` becomes `unobservedByte2A`.
- The constructor's word-wide zeroing of `+0x29`/`+0x2A` (0018AD50) is kept on both rows.

**Regression.** O3 fails on the pre-fix store and passes after `Tools/work/OPUS/ocl/patch_store.py`. On a copy,
`types_index.py --validate` reports 0 errors and 0 gaps.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` OrderedCommandList `+0x0029` | re-cut; old row quoted in the evidence | revised-here |
| the unobserved-row audit (`Tools/work/OPUS/silent_unobserved.json`) | this row closed | agrees |

Run receipt: executed at 7238558d8 - `flag29.py` O1–O2 PASS; O3 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
