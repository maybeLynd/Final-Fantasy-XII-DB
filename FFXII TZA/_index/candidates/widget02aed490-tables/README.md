# WidgetSingleton02AED490: two counted, keyed tables where the store had a word, four qwords and 1.2 KB unobserved (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` WidgetSingleton02AED490 `+0xEE..+0x5EF`. That range held eight rows:
- `word00EE`;
- `qword00F0`, `qword0100`, `qword0108`, `qword03F0`, all typed void*;
- `unobservedSpan00F8`, `unobservedSpan0110` (736 B) and `unobservedTail03F8` (504 B).

Two of them had surfaced in the unobserved-row audit as contradicted by the field-access index.

**Discriminator.** Whether the code addressing the range walks it with a fixed stride from a fixed base, with a count
kept beside it.

**Result** (`tables.py`, T1–T6):
- **Table A:** 0x18-byte entries from `+0xF0`, live count in the byte at `+0xEE`. The release frees each entry's
  `+0x10` and clears its `+0x00` (T1).
- **Table B:** 0x10-byte entries from `+0x3F0`, live count in the byte at `+0xEF`. The append writes at
  `+0x3F0 + count * 0x10` (T2).
- **Lookup.** Both tables are searched by byte `+1`, and by byte `+2` as well when `+1` is 2 (T3).
- **Removal.** Both shift the tail down by their stride (T4).
- **Size.** `0xF0 + 32*0x18 = 0x3F0` and `0x3F0 + 32*0x10 = 0x5F0`, the object's end, so each table holds 32 (T5).
  Whether an append checks that bound is **not claimed**.

**Store change.**
- The two byte counts replace the old `+0xEE` word.
- `entriesA` (`WidgetSingleton02AED490EntryA[32]`) and `entriesB` (`...EntryB[32]`) replace the rest.
- Two entry types are declared (`EMBED` routes). Their fields are the key bytes, entry A's released `+0x10` handle
  and state byte, and entry B's `+0x08` value.
- Each replaced row is quoted in the first new row's evidence cell.
- On a copy, `types_index.py --validate` reports 0 errors and 0 gaps.

**Regression.** T6 fails on the pre-fix store and passes after `Tools/work/OPUS/w490/patch_store.py`.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` WidgetSingleton02AED490 `+0xEE..+0x5EF` | re-cut; old rows quoted in the new evidence | revised-here |
| `_types/types.tsv` | two entry types added | revised-here |
| the unobserved-row audit (`Tools/work/OPUS/silent_unobserved.json`) | this type's `+0x3F8` tail row is closed | agrees |

Run receipt: executed at bbd3af82a - `tables.py` T1–T5 PASS, T6 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
