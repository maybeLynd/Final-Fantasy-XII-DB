# SD-122: the subresource-variant binding record, read (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md`

The check is [`sd122_record.py`](sd122_record.py) → [out](sd122_record.out), FAILS 0. Its control is that the pool
base `[02B47798]` has exactly the four rip users the page's section 18 names: `003CCC20`, `003CCF20`, `003CD650` and
`003CD6E0`.

## The record (80 bytes), by what the allocator `003CCC20` and the updater `003CCF20` do

| offset | what it is | evidence |
|---|---|---|
| `+0x00`–`+0x2F` | the **48-byte** payload, copied from the caller by three `movups` pairs, not 32 as the page said | R1 |
| payload `+2` (byte) | the list order: insertion walks past nodes whose byte `+2` is at least this record's | R3, `003CCEA0` |
| payload `+4` | the handle-table index (already on the page) | — |
| payload `+0x08` (word) | the duration: 0 = no limit; otherwise the record expires once elapsed time `+0x34` passes it | R4, `003CCFFA`–`003CD007` |
| payload `+0x0A` (word) | the start delay, counted down by the updater's per-call step (`r14w`) | R4, `003CCFD9` |
| payload `+0x0C` (word) | when non-zero, the allocator adds a spread to `+0x0A` | R5, `003CCC97`, `003CCE2E` |
| `+0x30` | the handle, `(gen << 8) \| index` (already on the page) | R2 |
| `+0x34` | **elapsed time**: zeroed on allocation, seeded with the delay's overshoot, then advanced each call; **bounded by `+0x08`** | R2, R4 |
| `+0x38` / `+0x40` | **next / prev** links in the handle-table entry's list (head `+0x28`, tail `+0x30`), written by the allocator's insert arms; zeroed first | R2, R3 |

The handle-table entry is validated by `[entry + 4] == handle` (`003CCE59`) before the insert. The allocator also bumps
the entry's refcount byte (`+0`) and stores `00181DD0()` at the entry's `+0x38`.

## Consumers

- consumer: `_index/OPEN-QUESTIONS.md` row SD-122: revised-here (ANSWERED).
- consumer: `the-largest-unclassified-functions.md`: revised-here. The box at line ~225 is ticked. The "32-byte payload"
  bullet (line ~921) is struck and corrected, and that correction covers the two code-block comments at lines ~892 and
  ~906.

## Regression

run: sd122_record.py at 4f7bfd847 (FAILS 0)
