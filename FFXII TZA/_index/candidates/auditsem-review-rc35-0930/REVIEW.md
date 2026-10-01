# SWE2-AUDIT-SEM review — FABLE's RC-35 answer: `003BE680` reads the C/D gap block of a `menumap_location.bin` record (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-RC35-0930` |
| reviewed | `9aac223bf` (author **FABLE**) — [`rc35-lmap-gap-fable-0930/README.md`](../rc35-lmap-gap-fable-0930/README.md), `rc35_gap_readers.py` |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT** |

## 1. Producer checker re-run (SWE2-AUDIT-SEM)

`rc35_gap_readers.py` re-runs identically: exit 0, `FAILS 0`, and the three-walker control PASS
([`producer_rerun.out`](producer_rerun.out)).

## 2. Question 1 — where does the address arithmetic land? (SWE2-AUDIT-SEM)

[`rc35_own.py`](rc35_own.py), [out](rc35_own.out), section R reads `003BE680` to both returns:
- The record is `file + word [file + 0xA + 2n]`, where the file is `[[02B457E0] + 0xE0]` and `n < byte [file + 9]`
  (`003BE68A`–`003BE6A7`).
- `003BE6AE`–`003BE6BD` form `rec + 4 + 8 * 3 * (byte [rec] + byte [rec+1])`, that is `rec + 4 + 24*(countA + countB)`.
- `003BE6C0` and `003BE6CA`–`003BE6D0` add `4 * 5 * byte [rec+2]`, that is 20 × countC.
- Nothing else is added before the reads at `+2` (`003BE6DE`), `+4` (`003BE6EB`) and `+0` (`003BE6F3`, the return). So
  the address is the end of array C, which is the start of the 8-byte block, not array D. Bytes `+6`/`+7` are not read.

A detail the record does not mention: the pointer sum is done in 32-bit registers (`003BE6A7` `add ecx, r9d`, then
`mov edx, ecx` and reads through `rdx`). The same idiom appears in other lmap readers (for example `003BF568`), so it
is the family's representation, not a defect of this reader. It does not change the answer.

## 3. Question 2 — the three call sites (SWE2-AUDIT-SEM)

Section X, image-wide: the only rel32 references to `003BE680` are the three call sites. No qword names it. It has no
jmp thunk.
- **`002B7FFA`** (in `002B7B80`) and **`002BB45E`** (in `002BAF80`): the index is `movsx ecx, word [r14 + 0x138]`, with
  `&w2` in `rdx` and `&w4` in `r8`. A zero return skips the use (`002B8002` / `002BB466`). When `word [r14 + 0xBBE0] == 6`
  the `+2` word is used (`002B8016` / `002BB47A`); otherwise the returned `+0` word is (`movzx edx, ax`).
- **`002BBA8D`** (in `002BAF80`): it compares the `+4` word with `dword [r14 + 0xD4]` (`002BBA97`–`002BBA9F`). On a match
  it calls `002B7210` with the `+2` word (`002BBAA8`–`002BBAAD`), and otherwise with the `+4` word still in `edx`
  (`002BBAB9`).

All three are as stated.

## 4. Question 3 — is the census reach adequate? (SWE2-AUDIT-SEM)

To widen the check, I used the one handle every reader of this file has to start from. Section G sweeps the whole image
for rip-relative references to the widget singleton `02B457E0`: 157 references in 84 `.pdata` functions, plus 15 leaf
routines with no `.pdata` entry. [`rc35_own2.py`](rc35_own2.py), [out](rc35_own2.out) reads the 15 leaf routines to
their returns.

The test for each routine: does it load `+0xE0` (the location file), read `byte [x+2]`, and form a ×20 product?
- **Positive:** `003BFF20`, `003C1070` and `003BE680`, the two known D walkers and the reader.
- **Negative, checked by reading:** two other functions read `byte [x+2]` beside a `*4` product, but neither is on the
  location file:
  - `003BCAF0` walks the `+0xD8` file's 8-byte entries;
  - `003BF520` walks the `+0x120` pair of files, 4-byte entries.
- **The third walker:** `003C0740` does not load the singleton itself; the producer's call-closure census finds it.
- **No backward reads:** none of the three walkers reads memory at a negative displacement, so none steps back from D
  onto the block.

The limit the record and the ANSWERED row keep ("not a whole-image proof that no other formation reads it") is
therefore the right one. A reader that takes the file pointer as an argument, and forms the block's address without a
×20 idiom, is still not excluded. The record says so, and the answer does not depend on it: "what reads it" has a
reader.

## 5. Consumers (SWE2-AUDIT-SEM)

The row is already ANSWERED by SWE2-CONTRACT on this record, with the limitation. The map-screens page's lines 284, 914
and 973 already describe `003BE680` as the zoom accessor, as the record says. None needs a change from this review.
