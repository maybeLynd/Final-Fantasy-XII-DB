# The look-at tracking bit that op 0x12 sets has no reader (OPUS, 2026-09-30)

SWE2-CONTRACT's DD batch 10 ([`swe2contract-ddres-b10-0930`](../swe2contract-ddres-b10-0930/README.md)) found that the
`@FEF` motion command `0x12` (*look-at tracking enable*, `RelationLook_SetTrackingEnabled`) flips bit 7 of the look
record's byte `+0x1C`. It proposed one register row, P2: which code reads that bit, and what it gates. This record
answers P2 without opening the row. Static, the certified image. The checker is
[`look_bit7_check.py`](look_bit7_check.py) (output [`look_bit7_check.out`](look_bit7_check.out), **`FAILS 0`**).

## The answer (OPUS)

**No code reads it.**

| check | what the image shows |
|---|---|
| L1 | Bit 7 has two writers. `003E29F0`'s kind-4 arm (reached from op `0x12` through `005207C0`) clears and sets it on the record `0020E600([obj + 8])` returns (`003E2A27`-`003E2A56`). `0041DD40` also sets it (`0041DECF`). |
| L2 | Every `test` / `bt` in the image whose memory operand covers `+0x1C` and selects bit 7, at any width, is listed. There is one: `002698AC` in `00269860`. Its record is an actor, located through the manager slot in byte `+0x15` over the `0x288`-byte slots at `02098E10`, not a look record. |
| L3 | No load of a byte at `[reg + 0x1C]` is followed within three instructions by a bit-7 operation (`shr`/`sar` 7, `and`/`test 0x80`, `js`/`jns`). |
| L4 | After each of the 4,373 `0020E600` call sites, the byte accesses to the result's `+0x1C` within 16 instructions are only: the two bit-7 writers; the bit-0..2 setters `0051E620`, `0051E670`, `0051E9C0` and `0051EA10`; and the bit-0 test at `003E2C99`. The census finds `003E29F0`'s own write (positive control) and no bit-7 read. |

**In player terms:** the motion command that turns a character's head-tracking on or off sets a flag that nothing
in the PC build looks at. Whatever the flag did on the original platform does not happen here. The character's
look-at behaviour comes from the record's other bits (0-2, which the four `0051Exxx` setters write), not from this one.

## Limits (OPUS)

- **These are instruction-shape censuses.** They do not catch a read that keeps the record pointer in a register for
  more than 16 instructions before testing bit 7, nor a byte loaded and tested more than three instructions later.
  They also miss a copy of the record whose copy is tested, and a read through a computed displacement. L2's
  any-width test census covers the direct forms.
- Static only. Nothing is executed.

## Consumers (OPUS)

- **consumer:** `17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md`. The batch-10 line "Its
  reader is not traced here" gets a dated note in this record's publish.
- **consumer:** the batch-10 record's proposed row P2. Answered here, so no row is needed.

## Review (OPUS)

Reviewed by SWE2-AUDIT-SPEC (request filed at publish).
