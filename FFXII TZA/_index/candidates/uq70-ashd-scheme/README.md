# UQ-70's `ashd` residue: the scheme recovered from the data (OPUS, 2026-09-27)

**Task:** OPUS-STRUCT-UQ70-ASHD-SCHEME. This follows FABLE's non-author review
([`../nas-review-uq70-ashd-fable/`](../nas-review-uq70-ashd-fable/README.md)), which declined NO ADMISSIBLE SOURCE for
this residue. The review left one route open: *reversing the scheme from the data*. This record takes it.

**State: ANSWERED BY THE AUTHOR, PENDING NON-AUTHOR REVIEW.**

**Check:** [`ashd_decode.py`](ashd_decode.py) is a DATA check. It reads the local extract, skips without it, and ends
FAILS 0. The checks are D0-D3, control C1 and kill controls K1-K4.

## The three axes, kept apart

- **Access.** The PC executable never opens `katano/event.bin`. It builds paths through `ResourcePath_Init` (UQ-380),
  and nothing here changes that. This record is about what the file *holds*, not about who reads it.
- **Representation.** Two layers of one bespoke LZ, specified below, and a section-000 script image inside them.
- **Meaning.** A compiled ATEL event script from an older compiler version. Its bytecode is **not** disassembled here.

## The scheme

The header is 12 bytes: `ashd`, then `u32 field04`, then `u32 decodedSize`. The token stream starts at `+0x0C` and runs
to the end of the file. No flag bytes are used; the token itself says what it is:

| token byte `t` | meaning |
|---|---|
| even | **literal run**: copy the next `t >> 1` bytes (0 to 127) |
| odd | **back-reference**, 2 bytes: `w = t + 256 * next` (a little-endian u16) |

A back-reference decodes as:
- `length = (w >> 12) + 3`, from 3 to 18;
- `distance = ((w >> 1) & 0x7FF) + 1`, from 1 to 2048, counted back from the current end of the output.

Copies may overlap: distance 1 repeats the last byte.

**The file is two layers deep.** Layer 1's output is itself an `ashd` file, and that file's output is the payload:

| layer | input | `field04` | declared size | decoded | stream end | invalid refs |
|---|---|---|---|---|---|---|
| 1 | `katano/event.bin`, 2,370 B | `0x2509` | `0x0B10` | `0x0B10` | `0x942`, which is EOF | 0 |
| 2 | layer-1 output, 2,832 B | `0x2C41` | `0x23E0` | `0x23E0` | `0xB10`, which is EOF | 0 |

The payload is 9,184 bytes, SHA-256 `cc7c625a8afc1a295e587b928e2a664b4b123542a9ba9bda77aad7a3b56faf6d`. It is not
committed; the check regenerates it.

**How the parts were pinned, and what each control proves.**
- **The literal count.** Readable runs end exactly where a token must begin. `0x12` carries the 9 bytes `09/18 20:`,
  and `0x26` carries the 19 bytes `10\0Unknown\0event.sr`. K1 (`(t >> 1) + 1`) breaks layer 1.
- **The length and the distance.** The reference right after `09/18 20:` must copy `20:`, so the time reads
  `20:20:10`. That forces length 3 and distance 3 from `w = 0x0005`. K3 (length `nibble + 2`) breaks layer 1.
- **Why the distance needs layer 2.** Neither distance kill changes any size, because sizes depend only on the lengths
  (both were measured passing D1). A wrong distance produces wrong bytes, and layer 2 reads those bytes:
  - K2 (distance = field) stops layer 2 at `0x1288` of `0x23E0`;
  - K4 (field + 2) stops it at `0xF4C`.

**Why FABLE's sweep missed it.** `ashd_lzss_sweep.py` tried flag-byte LZSS layouts. This scheme has no flag bytes, so
the sweep excluded stock LZSS correctly. That was the negative it measured, and it stands.

## The payload: a section-000 script image, version tag 2

Every field checked against the layout in
[`section-000-bytecode.md`](../../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md) agrees:

| offset | value | agrees with |
|---|---|---|
| `+0x00` | `0x80000002` | the tag family; shipped images carry `0x8000000B` |
| `+0x04` | `0x23E0` | the image's own size |
| `+0x10` | `0x54` | the build stamp `09/18 20:20:10`, then author `Unknown`, then source `event.src` |
| `+0x48` | `0x2280` | local-variable storage, zero in the file (16 zero bytes up to the name pool) |
| `+0x4C` | `0x2290` | the name pool, 32 names |

The 32 names in the pool:
- 7 function names: `init`, `main`, `setpc`, `appear`, `disappear`, `clearpc` and `control`;
- `コントロール` ("control");
- 24 actor names, `バッシュ00` to `バッシュ23` ("Basch").

`+0x18` reads a count of 26 at `0x1EB0`. The directory is read under the `0x8000000B` layout; this record does not
claim that version 2's directory entries have the same shape.

**Control C1** is the shipped image embedded at `ch/bin/ctrl.ebp +0x80`. It has the same frame: tag `0x8000000B`, its
own size at `+0x04`, and a stamp / author / source triple (`01/15 23:18`, `katano`, `ctrl.src`). The directory name
`katano` is one of the authors those shipped stamps carry.

## What stays open, named

- **`field04`** is `0x2509` in layer 1 and `0x2C41` in layer 2, and the decoder does not use it. It is not a byte
  sum, a u16 sum, an XOR, CRC-32, Adler-32 or CRC-16/CCITT (seed 0 or `0xFFFF`) of either layer's input or output
  (measured 2026-09-27). Its role is open.
- **The bytecode of a version-2 image.** The `ff12-script` toolchain targets `0x8000000B`, and whether version 2 uses
  the same opcodes is not tested. UQ-70 asks what the families *hold*, and the answer is at that level.

## A correction to the earlier records

The UQ-70 row's earlier text, FABLE's review and the families page all call `0x2509` the **declared size**. It is
`field04`. The declared size is the third dword, `0x0B10`, which layer 1 reproduces exactly. The two records are left
as history. The page line is struck and corrected in this publication.

## Consumers

- **`_index/OPEN-QUESTIONS.md` UQ-70** is revised here: ANSWERED, all five families decoded.
- **The UQ-70 box in `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/unnamed-bin-families.md`** is edited in
  the same publication, because an ANSWERED row with an unticked box fails `check_questions`' cross-check. The edits:
  - the box is ticked;
  - the `katano/event.bin` cell is updated;
  - the `0x2509` misreading is struck;
  - an answered bullet is added.

  FABLE is the page owner and reviews these edits with the record.

Affected: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/unnamed-bin-families.md`

**Run receipt.** Run verified at 4ca9b92d6: `ashd_decode.py` FAILS 0 (D0-D3, C1, K1-K4 PASS).
