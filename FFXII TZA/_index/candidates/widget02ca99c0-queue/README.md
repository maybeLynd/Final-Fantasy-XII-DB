# WidgetSingleton02CA99C0: +0xD8..+0x397 is the save-storage operation queue (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` WidgetSingleton02CA99C0, the 19 rows in `+0xD8..+0x397`. They include the
`unobservedSpan0128` (152 B) and `unobservedSpan01C8` (464 B) rows that the unobserved-row audit flagged, and per-field
rows (`dword00D8` … `qword0120`, `qword01C0`) whose widths disagreed with the field-access index. For example,
`dword00E0` is read as a qword and as a byte.

**Result** (`queue.py`, Q1–Q4):
- **The queue itself (Q1, Q2).** The completion `00582240` (`SaveStorageQueue_CompleteFrontOperationAndNotify`) treats
  `+0xD8` as a queue of 0x58-byte entries, with the count byte at `+0x398`. It shifts every entry down, clears the
  vacated one, and calls the notify callback at `+0xC0` when the front entry's `+0x04` bit 1 is clear. Eight entries
  end exactly at the count byte.
- **The entry layout (Q3).** The start routine `00582040` switches on the front entry's `+0x00` kind (0..12) and sets
  its `+0x04` bit 0. It reads the rest as a per-kind union at mixed widths: `+0x08..+0x47` as a qword/dword pair, a byte
  or an address; `+0x48` and `+0x50` as qword, dword or byte.
- **Why the old rows disagreed.** They described entry 0, and one field of entry 2, as fixed parent fields. Each union
  width looked like a different field.

**Store change.** The parent gets one row, `saveQueue0D8 WidgetSingleton02CA99C0QueueEntry[8]`. The replaced rows are
listed in its evidence cell. A new entry type has five rows:
- `opKind int32`;
- `opFlags uint32`;
- `payload08 u8[64]`, `arg48 u8[8]` and `arg50 u8[8]`, all DISCOVERED and marked mixed-width.

The per-kind payload layout is not claimed.

**Regression.** Q4 fails on the pre-fix store and passes after `Tools/work/OPUS/ca99/patch_store.py`. On a copy,
`types_index.py --validate` reports 0 errors and 0 gaps, both alone and with the widget-header patch applied.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` WidgetSingleton02CA99C0 `+0xD8..+0x397` | 19 rows → one queue row; the entry type added | revised-here |
| `_types/types.tsv` | entry type added | revised-here |
| `19-Save-Load-Settings/CONTRACT-storage-read-completion.md` (the queue at `+0xD8`, count `+0x398`, 13-arm dispatch, the `== 8` enqueue refusal) | the store now matches the contract | agrees |
| the unobserved-row audit (`Tools/work/OPUS/silent_unobserved.json`) | this type's two large rows closed | agrees |

Run receipt: executed at 7238558d8 - `queue.py` Q1–Q3 PASS; Q4 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
