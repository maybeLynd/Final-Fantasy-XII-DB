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
| comparison | 6 | Doom | none (all `0xFF`) |

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
3. **The positive control is that known reader, identified by the instruction, not by the reported RIP.** A data
   breakpoint traps AFTER the access (Intel SDM 17.3.1.2), so the raw context RIP of the known read is the NEXT
   instruction, `0031E245`; the access PC is `0031E241` (`movzx eax, byte ptr [rbp+0x13]`, 4 bytes). A run must show
   that association natively - the trap for this read reports `0031E245`, and decoding back gives `0031E241` - before
   any other hit is interpreted. It is not an answer. A run without it is not qualified.
4. **One accepted transition.** Apply the status by an ordinary game action, then let it expire or be removed.
   Record the add (`0031E1..`) and the clear.
5. **A healthy, bounded run.** Record a fixed wall-clock bound and the process health before and after. For every
   trap record the raw RIP, the normalized access PC, the decoded opcode, the effective address, the access kind
   (read or write - RW windows also trap writes), the instruction's actual access width, and the overlap of
   `[EA, EA + width)` with the sparse span `+0x11..+0x12` / `+0x14..+0x1F`. The watch window's width and the memory
   value after the trap are not the consumed value.

## Reading the result

- **A sparse reader** is a READ whose decoded `[EA, EA + width)` overlaps the sparse span. That is the answer:
  publish the access PC and function, then read that body statically. A write, or a read that touches only `+0x13`
  (the four windows include that extra byte), is not a sparse reader.
- **No hit** in a qualified cycle bounds that cycle only. The span stays **unknown**, not "unread" and not "dead".
- **The Doom row** holds only `0xFF` in the sparse span, but an all-`0xFF` row does not forbid a legitimate read of
  it. A hit there is diagnosed like any other, by its instruction, not treated as a wrong detector or row.

**Not claimed:** what the values 25–31 mean. (`+0x02` is listing 4's order key, `StatusDefinitionRecord.listOrderKey4`, renamed from effectIdSlot02 at `aa84ba258`.)

*Qualified 2026-09-27 on ASTRA-RETURN-OPUS-STATUS-WATCH-PREDICATES (OPUS): prerequisite 3 and 5 and the reading rules above replace the earlier text, which read the positive control from the raw RIP, took a watch window as the access, and treated a Doom-row hit as a detector fault. The rows, the prerequisites 1, 2 and 4, and the one-cycle bound are unchanged.*
