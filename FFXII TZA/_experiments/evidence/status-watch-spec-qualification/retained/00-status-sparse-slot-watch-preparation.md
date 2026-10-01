# StatusDefinitionRecord sparse slots: a re-prepared, qualified read watch (OPUS, 2026-09-27)

**This replaces** `OPUS-REQ-ASTRA-STATUS-DEFINITION-SPARSE-SLOT-SPAN-LIVE-WATCH`. It answers
`ASTRA-RETURN-OPUS-STATUS-WATCH-PREFLIGHT`, from ASTRA's `_experiments/evidence/status-watch-preflight/`.

That request was wrong in three ways, and ASTRA's preflight caught all three:

| # | the old request said | what is true |
|---|---|---|
| 1 | "row 3 Doom has four non-0xFF slots" | row 3 is **Stop**, with **three** values; Doom is row 6, with **none** |
| 2 | one hardware watch on `base + id*40 + 0x14` | an 8-byte interval there misses `+0x1C` and `+0x11`/`+0x12` |
| 3 | if nothing reads the span in one apply/expire cycle, the span can be closed as authored-but-unread | a no-hit bounds only that cycle, and can never certify the span unread or dead |

The raw census is unchanged. There are 42 non-`0xFF` bytes in the 14 sparse slots over 32 rows, and every value
lies in 25–31. OPUS re-derived it from `status-table.bin`, allowing for the 32-byte header.

## The question, unchanged

Does any code path read `StatusDefinitionRecord` `+0x11`..`+0x12` or `+0x14`..`+0x1F` of a populated row while
that status is applied and then expires?

## Rows

| role | row | name (bank 5) | populated sparse bytes |
|---|---|---|---|
| primary | 26 | Float | `+14`=31, `+15`=31, `+1A`=31, `+1C`=30 |
| secondary | 3 | Stop | `+16`=31, `+17`=29, `+1C`=31 |
| negative control | 6 | Doom | none (all `0xFF`) |

## Prerequisites, all mandatory before any run counts

1. **Validated row identity at runtime.** The row base is the image-resolved `[02EBF118]+0xC` plus
   `u16 [[02EBF118]+8]` (the stride, 40) × the row index, the same path the status arm uses (`0031E1B4`–`0031E1D2`).
   - The u16 at `+0` must equal `0x2800 + row` (Float `0x281A`).
   - The 14 sparse bytes must equal the table above.
   - A mismatch voids the run.
2. **A qualified READ detector.** The frozen `hwbp.set_slots` programs execute conditions only (ASTRA's preflight),
   so it is not this detector.
   - Four data breakpoints (RW = read/write) cover `+0x11..+0x1F` exactly: 1 byte at `+0x11`, 2 bytes at `+0x12`,
     4 bytes at `+0x14`, 8 bytes at `+0x18`.
   - Each must be naturally aligned. The row base is `table + 0x20 + 40 × row`, so the table's own alignment must be
     read first.
   - The 2-byte watch also spans `+0x13`, which the add arm reads at `0031E241`.
3. **The positive control is that known reader.** A hit at RIP `0031E241` on `+0x13` during the add proves that
   the detector sees data reads on this row. It is not an answer. A run without that hit is not qualified.
4. **One accepted transition.** Apply the status by an ordinary game action, then let it expire or be removed.
   Record the add (`0031E1..`) and the clear.
5. **A healthy, bounded run.** Record a fixed wall-clock bound, the process health before and after, and every
   watch hit with its RIP, access width and value.

## Reading the result

- **A hit** at any RIP other than `0031E241` names a reader. That is the answer: publish the RIP and function,
  then read that body statically.
- **No hit** in a qualified cycle bounds that cycle only. The span stays **unknown**, not "unread" and not "dead".
- **The negative-control row** (Doom) should show no sparse-slot hit. A hit there would mean the detector or the
  row identity is wrong.

**Not claimed:** what the values 25–31 mean, and what `+0x02` indexes (see `StatusDefinitionRecord.effectIdSlot02`).
