# DeveloperConsoleSettings01F81428: the unnamed stretches, cut (OPUS, 2026-09-28)

**State: PENDING INDEPENDENT REVIEW.**

**What changed.** The type carried twenty `spanXXXX u8[N]` rows (DISCOVERED), each an "unnamed stretch" with a count of censused
displacements but no fields. [`dev_console_recut.py`](dev_console_recut.py) ([output](dev_console_recut.out)) cuts them from a
fresh receiver census. Checks C, R and W: FAILS 0; W failed before the patch.

- **C: the census.**
  - Two seeds: the getter `001D50D0` (SEED=call) and the constructor `001CCB20` (SEED=ctor).
  - Only instructions whose displacement is the field itself are kept, and enumerated sites (loop over-reach) are dropped.
  - Before the patch it reached 476 offsets, including 58 of the type's 60 declared rows.
- **R: the cut, derived by the check and not hand-kept.**
  - A field starts at every accessed offset. Its width is the narrowest access there, capped at the next accessed offset.
  - So the constructor's qword zeroing of dword pairs is a packed store, not a field.
  - Typing and grading:
    - read fields are typed from their reads (float for ss-class instructions, signed for movsx / movsxd) and graded PROVEN;
    - write-only fields are typed from the write and graded PROBABLE;
    - a field reached only by a wider access says so and is graded PROBABLE.
  - Before the patch: 20 stretch rows became 154 rows, 121 fields and 33 declared gaps.

**Not claimed:** what any field holds.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` DeveloperConsoleSettings01F81428, the 20 `spanXXXX` rows | cut into 154 rows, each carrying the old row in its evidence | revised-here |

**Run receipt:**
- `dev_console_recut.py` FAILS 0.
- `types_index.py --validate`: 0 errors.
- `check_ctype_widths.py` 0; `check_type_refs.py` 0 dangling; `check_embed_parent_fields.py` 0; `check_census_widths.py` 0.
