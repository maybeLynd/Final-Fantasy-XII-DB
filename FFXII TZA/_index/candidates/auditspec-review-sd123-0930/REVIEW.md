# SWE2-AUDIT-SPEC review of SD-123 (sd123-kind52-image-record-0930, OPUS, 524d5aacd): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `524d5aacd` (the record's only commit), [README](../sd123-kind52-image-record-0930/README.md) and
`sd123_kind52.py`. Measured at HEAD 17a959c94. Static, certified image, plus the shipped effect data in
D:/FFXII_TZA_extract.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD123-0930 | sd123-kind52-image-record-0930 | `524d5aacd` | ACCEPT-WITH-NARROWING |

Kind `0x52` is the effect container's image (texture) record, and the header, palette and mesh-handle readings hold.
"Paletted" does not hold: the loader has three direct-colour formats, and **5,786 of the 16,862 shipped kind-0x52
records use one of them**, with no palette. The compiled `0x80` / `0x81` cases the record cites cannot run.

**Re-run.** [rerun_sd123_kind52.out](rerun_sd123_kind52.out) is identical to the committed `sd123_kind52.out`,
ignoring CR. I1-I4 PASS, `FAILS 0`. Package dir clean after re-run: yes (`git status --porcelain` prints nothing).

**Re-derived independently.** Sources: [sd123_indep.py](sd123_indep.py) / [.out](sd123_indep.out) (lane loader
`ov31_indep.py`), [kind_switch.out](kind_switch.out), [dis_loader.out](dis_loader.out),
[dis_clut.out](dis_clut.out), [dis_dispatch.out](dis_dispatch.out), and the shipped-data census
[sd123_formats.py](sd123_formats.py) / [.out](sd123_formats.out) (own walker).
- **Kind 0x52 is this loader.**
  - The record-kind switch in `003A9EF0` (`add eax,-0x50; cmp eax,9`; table IB + 0x28A1BC) sends kind 0x52 to
    `003A9FA2`. That arm allocates 0x1D0, then calls `00500B70` and `00500C00` (`003A9FB7` / `003A9FC2`).
  - The other caller of `00500C00` is `005009B8`.
- **I1 holds.** The format byte lands at `+0xA0`, which is then ANDed with 0x3F (`00500C39`). Bit 6 goes to `+0x1C8`,
  bit 7 to `+0x1CA`. The count byte goes to `+0xA2`. The words go to `+0x1CC` / `+0x1CE` / `+0xA8` / `+0xAA`, and
  `+0xA8` / `+0xAA` are copied to `+0xA4` / `+0xA6`.
- **The 0x80 / 0x81 cases are dead in this loader.**
  - `+0xA0` is written only at `00500C2A` and `00500C39` before its two reads (`00500CE1`, `00500EDD`).
  - No callee between those points receives `rdi`.
  - So `+0xA0 <= 0x3F` whenever it is read. The palette switch's `sub ecx, 0x7f` case (`00500CF1`, which the
    checker's I2 pins) and the jump-table arms for 0x80 (`00500F8F`, `00184130`) and 0x81 (`00500FD3`, `00184370`)
    cannot run.
  - File bytes 0x80 / 0x81 do select 16 / 256 colours, but through the mask. They take arms 0 / 1.
- **The live formats** (jump table at `00500EF1`; 8 arms, decoded for indices 0..0x81):

  | masked format | arm | surface call | bytes consumed | palette |
  |---|---|---|---|---|
  | 0 | `00500F0C` | `00183EE0` | w·h/2 | count × 64 B |
  | 1 | `00500F54` | `00184140` | w·h | count × 1,024 B |
  | 2 | `00501014` | `00183A00` | w·h·2 | must be 0 |
  | 3 | `0050104E` | `00183C60` | w·h·3 | must be 0 |
  | 4 | `00501089` | `00183EB0` | w·h·4 | must be 0 |
  | 5..0x3F | `005010CF` | none | none | none |

  - w and h are `+0xA4` / `+0xA6`, the copies of `+0xA8` / `+0xAA`.
  - With a palette count above 0, only formats 0 and 1 pass: any other format returns 0 at `00500CFB`.
  - With count 0, the palette block is skipped, and formats 2-4 create a surface.
- **I2's palette pair.**
  - Each palette's data goes to `001837A0(src, n, 1)`, which is `0017E8E0` with `r9d = 1`, stored at `+0xC8 + 8i`.
  - `00183760` is called with `rcx = 0` (`00500D36` / `00500D9D`), which is `0017E8E0` with `r9d = 4` and no data.
    It is a same-size companion handle at `+0x148 + 8i`, not a second submit of the palette.
- **I3 citation.** The checker's "sized by `+0xA8` × `+0xAA`" pins `00500FA4` / `00500FB4`, which sit in the dead 0x80
  arm. The live arms read `+0xA4` / `+0xA6`. The values are equal, so the sentence holds by value, but the pinned
  lines are the wrong ones.
- **I4 holds.**
  - `004370D0`..`004370DA` resolves each `+0x1C` id through `003AA280(key, 0x52, id)` into the block whose handle
    `004370B2` stores at `+0x184`.
  - `00431AC4`..`00431AF2` follows `+0xB0` → `+0x184` → `[0]` → `+0x10`.
- **Shipped data** (every EFX stream: 4,229 files, the .efx / .efb set plus the 531-file embedded list).
  - **Count.** There are **16,862** kind-0x52 records. The README's 13,161 is the older .efx / .efb-from-+0x10 walk,
    a lower bound (the kind-54 page's GI-8 caveat).
  - **Format bytes.** 0x00 619, 0x01 6,610, 0x04 169, 0x40 12, 0x41 1,347, 0x44 5,617, 0x80 500, 0x81 1,988. Masked,
    that is 0 = 1,131, 1 = 9,945, 4 = 5,786, and never 2, 3 or 5+.
  - **Palette counts.** The count is 1 in every format-0/1 record and 0 in every format-4 record.
  - Bit 6 is set in 6,976 records.

**Controls.**
- **Size control** (sensitive to wrong field offsets or a wrong bytes-per-pixel reading). The predicted size is
  0x10 + palettes + w·h·bpp. It falls within the 16-byte padding of the payload for **16,859 / 16,862** records, and for
  all 5,786 format-4 records at 4 bytes per pixel.
  - The 3 misses are format 0x80 records in `g0118.cm` / `mrm0202.mpk`. Their payload is longer than the loader
    consumes, and that is harmless.
- **Kind count.** My walk's kind histogram is a superset of the published 13,161 walk: every kind is at least its
  published count.
- **Jump table.** The decode separates index 0 and index 1 into distinct arms, so it is not collapsing arms.
- **Mask scan.** The `+0xA0` scan finds the known first store `00500C2A`.

**Citations checked.**
- `00500C39`, `00500C4E`, `00500C58`, `00500C63` and `00500C6D`..`00500CAE` support I1.
- `00500D08` / `00500D6F` / `00500D5B` support the 1,024 / 64-byte strides.
- `00500CF1` supports nothing that can run (the dead case).
- `00500FA4` / `00500FB4` / `00184130` / `00184370` sit in dead arms.
- `004370D0` / `004370DA` / `004370B2` / `00431AC4`..`00431AF2` support I4.

**Correction wording** (the producer applies it to the README; the SD-123 register row's summary follows):
- Title and summary: "effect record kind `0x52` is the effect container's image (texture) record: 4- or 8-bit
  indexed with one palette, or 4-byte-per-pixel direct colour".
- The answer:
  > A kind-`0x52` record is an image: a format, a palette count and a size. The loader masks the format to 6 bits
  > (`00500C39`; bit 7 is kept at `+0x1CA`, bit 6 at `+0x1C8`). Format 0 is 4-bit indexed (64-byte palettes, w·h/2
  > pixel bytes), format 1 is 8-bit indexed (1,024-byte palettes, w·h), and formats 2 / 3 / 4 are 2 / 3 / 4 bytes per
  > pixel with no palette. A palette count above 0 with any format other than 0 / 1 fails the load.
- I2:
  > each palette's data goes through `001837A0` (+0xC8 + 8i); `00183760` makes a same-size handle with no data
  > (+0x148 + 8i).

  Drop "(or 0x81)" / "(or 0x80)" as separate cases, and say instead: "file bytes with bit 7 or 6 set select the same
  palettes through the mask".
- I3: list the live surface calls `00183EE0` / `00184140` / `00183A00` / `00183C60` / `00183EB0`. Say `00184130` /
  `00184370` are the unreachable 0x80 / 0x81 arms. Say the surface is sized by `+0xA4` × `+0xA6` (copies of `+0xA8` /
  `+0xAA`).
- For modding:
  > the 16,862 kind-`0x52` records over every EFX stream (13,161 in the .efx / .efb-only walk) are the effect
  > containers' textures: 11,076 indexed (1,131 with 16 colours, 9,945 with 256, one palette each) and 5,786 direct
  > colour at 4 bytes per pixel. No shipped record uses formats 2 or 3.
- The checker should pin the mask (`00500C39`) instead of `00500CF1`, and the live arms instead of `00500FA4` /
  `00500FB4`.
