# RC-22 to RC-25: the .as7 page codec, its tail dictionary, the one walker, and char_silhouette's pages (ORACLE, 2026-09-30)

## The question

SWE2-CONTRACT's batch 3 registered four rows from
`02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/as7-menu-graphics-containers.md` section 7:
- **RC-22:** the per-payload subformat (raw indexed texels, a compressed stream, or a sub-table);
- **RC-23:** what the `tailOff` block holds, and whether anything reads it;
- **RC-24:** which instruction walks `offsets[]` and reads `count` / `tailOff`;
- **RC-25:** which of `char_silhouette`'s 3,096 pages any shipped path indexes.

## Method

[`rc22_as7.py`](rc22_as7.py), output [`rc22_as7.out`](rc22_as7.out). [`arc.py`](arc.py) is the shared helper for this batch:
- it reads files straight from `FFXII_TZA.vbf` through `agent_flow/tools/vbfextract.py`;
- it re-exports the image helpers of `../rc8-cascade-count-0930/img.py`.

The walker was found from the item-icon path. The icon handler `00292390` gets the sheet buffer through the slot getter
`00292050(id >> 6 + 2)`, which reads `obj + 0xD0 + 16k` (the object's copy of the `0209BEA0` slots,
`00291D90`). It then calls `0024AA00(sheet, obj + 0x2C8, id & 63, 1)` at `00292768`. The rest came from reading
`0024AA00`, its only callee `00248500`, and the second caller `002CEFD0`.

The script asserts every code fact it relies on against the image bytes (C3). It re-implements the walker and the
decoder, and decodes every page of all 18 shipped files. Controls, all PASS:

| control | what it checks |
|---|---|
| C1 | every page of all 18 files decodes, and its token stream ends exactly at the next offset (at `tailOff` for the last page), so the re-implementation is exact and the payloads carry nothing else |
| C2 | `item_gra00`..`06` pages decode to 6,144 bytes, the 64 x 96 of `01E0C470`/`01E0C474` that `00292390` copies one byte per texel; `char_silhouette` pages decode to 1,024 bytes, and 0x102 of them fill the 0x40800-byte buffers `002CEFD0` allocates |
| C3a-C3f | the walker, decoder, silhouette-index and setter instructions, byte for byte |
| C4 | `0024AA00` is called only at `00292768`, `002CF2B4` and `002CF2CE`, and `00248500` only at `0024AAF4`; no `.data`/`.rdata` qword holds either address |
| C5 | the silhouette blocks partition the file exactly |

## Result

**RC-24: ANSWERED. `0024AA00(file, dst, first, n)` is the only `.as7` walker.**
- **`count`:** `file[2]*256 + file[3]` (`0024AA0A`-`0024AA2A`).
- **Bounds:** returns 1 when `first >= count` (`0024AA2E`). `n = 0` or `n > count` means "to the end" (`0024AA4E`-`0024AA5A`).
- **`tailOff`:** read big-endian into the dictionary pointer `file + tailOff` (`0024AA5E`-`0024AA97`).
- **Output setup:** it stores `dst` in `02090788` and zeroes the output cursor `02091090`.
- **The walk:** for each page `p` from `first` onward, it reads `offsets[p]` big-endian at `file + 8 + 4p`
  (`0024AAC0`-`0024AAF1`) and calls `00248500(file + offsets[p], dict)`.
- **Callers:**
  - the `item_gra` icon handler `00292390` (one page);
  - the silhouette updater `002CEFD0` (two runs of 0x102 pages).
- **No magic check:** no code tests the `A7` magic.

**RC-22: ANSWERED. A payload is a compressed stream: an LZ-style token stream against a fixed dictionary**
(`00248500`).
- **Literal run:** a byte `c >= 0x80` copies the next `(c & 0x7F) + 1` bytes.
- **Dictionary copy:** otherwise the two bytes `c, x` copy `len = ((2c) >> (8 - b)) + 3` bytes from the dictionary
  at `(c*256 + x) & (0xFFFF >> (b + 1))`.
  - With `b = 5`, as in all 18 files, that is `len = (c >> 2) + 3` and a 1,024-byte window.
  - Copies never refer back into the output: every back-reference points into the file's dictionary, never into the
    page just decoded.
- **What decodes out:** the bytes are **8-bit palette indices, one per texel**.
  - `item_gra` icons are 64 x 96 (6,144 bytes). `00292390` copies them row by row into the texture, with the
    1,024-byte `Item_Clut` palette `id >> 6` (`0029278A`).
  - `char_silhouette` pages are 1,024 bytes each.
- **The `7C 05` units** are dictionary copies of 34 bytes from dictionary offset 5, a run of the background index.
  Page 0 of `item_gra00` is 180 of them plus `54 05`, which is 6,144 bytes of background.
- **`item_gra07`** (6,190 B) is the one exception: 64 pages of 1,536 zero bytes, a blank sheet. Its declared length
  1,536 is shorter than the 6,144 the icon copy reads.

**RC-23: ANSWERED. The `tailOff` block is the codec's header and dictionary. The walker reads it on every call.**
- **Mode byte:** 0 in all 18 files. Modes 0 and 3 decode; 1 and 2 are rejected.
- **Bit width `b`:** 5.
- **Output length per page:** big-endian, 6,144 for `item_gra00`..`06`, 1,536 for `item_gra07`, 1,024 for
  `char_silhouette`.
- **Dictionary body:** the rest of the file, from 34 to 1,024 bytes. Every file's pages use the whole body (the
  maximum dictionary extent referenced equals its length).
- **Mode 3** (unused in shipped files) takes the length from each payload's first two bytes instead.

**RC-25: NARROWED. Every page is reachable, and only as part of a whole 516-page block; which blocks a session shows
depends on one value.**
- **The index:** `002CEFD0` computes `first = 0x204 * T[ch]`, where `T = {0, 1, 3, 2, 4, 5}` (`00917160` plus the
  immediates at `002CEFF7`/`002CEFFF`). It decodes pages `first..first+0x101` into buffer `+0xE0`, and
  `first+0x102..first+0x203` into `+0xE8`: 516 pages per character.
- **The id:** `ch` is the object's byte `+0x10D`. Its only writer is the `.pdata`-less setter `002CEE00(id, flags)`
  (`002CEE1A`), which clears the decode request for any id above 5 (unsigned, so -1 too). The setter has two callers:
  - `005679D0` passes -1 (clear);
  - the pane reset `0056A010` passes word `+0x60` of the current menu member record,
    `00282DF0([0209AC30] + 0xDE0)`.
- **The mapping:** ids 0..5 index disjoint 516-page blocks that cover pages 0 to 3,095 exactly once (C5):

| id | pages |
|---|---|
| 0 | 0-515 |
| 1 | 516-1031 |
| 3 | 1032-1547 |
| 2 | 1548-2063 |
| 4 | 2064-2579 |
| 5 | 2580-3095 |

- **Guests get nothing.** The menu member records are nine records of 0xC0 at `[0209AC30] + 0x408`, placed in the
  order of the id table `00915CE0` = {0, 3, 2, 4, 1, 5, 6, ..., 13, 15} by `00283270`. Ids 6 and up decode no
  silhouette.
- **Where the id comes from.** `00283270` builds member record `k` through `00320040(3, k, record)`. That call
  resolves party slot map 3 (`0031B9F0`) to a stats record `[02EBF190] + 8 + idx * 0x1C8`. `00329220` then clears the
  member record and sets word `+0x60` = -1 (`0032925D`), and later sets it to the stats record's byte `+0x04`
  (`0032946C`/`00329471`), `BattleStatsRecord.definitionRowIndex`.
- **The menu's own rule agrees.** `00283270` counts a member as a main character exactly when that id is 0 to 5 and
  the member is not flagged a guest (`002833B5`-`002833D2`).
- **Residue (static, authored data):** which `definitionRowIndex` values the party stats records carry. If the six
  permanent characters carry 0 to 5, as the menu's own main-member test implies, every page is shown. This record did
  not find the initialiser that writes the party records' `+0x04`: a direct byte-store scan of the functions that
  hold `02EBF190` and use the 0x1C8 stride found none.

## Corroboration

SWE2-DATA answered the same rows the evening before (`../rc22-34-resource-readers-0930/`, commit `1261e2044`). This
record re-derives them independently and agrees on RC-22, RC-23 and RC-24:
- the walker, the codec and the tail layout;
- `item_gra07`'s blank 1,536-byte pages.

On RC-25 it agrees on the page arithmetic and the setter, and adds where the id comes from: `BattleStatsRecord +0x04`
through `00320040` / `00329220`. The one open value moves from "the record word `+0x60`" to "the party stats records'
`definitionRowIndex`".

This record adds the item-icon geometry, which SWE2-DATA leaves unclaimed:
- 64 x 96 at one byte per texel (`01E0C470`/`01E0C474`, and the copy loop at `00292830`);
- the per-sheet 1,024-byte palette pick at `0029278A`.

## Not claimed

- What the 1,024-byte silhouette page depicts, and the geometry `002CF440` draws it with (32 x 32 would fit, but this
  record does not read the draw call's texture header).
- What the stale 4,608 bytes after an `item_gra07` page hold at draw time.
