# SWE2-AUDIT-SPEC review of SD-2 (sd2-r2-label-element-0930, OPUS, 7573a1b87): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `7573a1b87` (the record's only commit), [README](../sd2-r2-label-element-0930/README.md) and `sd2_check.py`,
measured at HEAD `b58c633f7`. Static, certified image, plus the shipped data files.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD2-0930 | sd2-r2-label-element-0930 | `7573a1b87` | ACCEPT |

**Re-run.** `sd2_check.py` writes `battle_4_c-letters.png` beside itself, so it was run as a byte-identical copy,
[rerun_sd2_check_copy.py](rerun_sd2_check_copy.py) (`cmp` equal to the package script). [rerun_sd2_check.out](rerun_sd2_check.out)
is identical to the committed `.out` (CR ignored), W1-W4 and D1-D3 PASS, `FAILS 0`, and the regenerated
[battle_4_c-letters.png](battle_4_c-letters.png) is byte-identical to the committed one. Re-run again at `b58c633f7`:
still identical. Package dir clean after re-run: yes (`git status --porcelain` on it is empty).

**Re-derived independently.**
- **Data source** ([sd2_rects.py](sd2_rects.py) / [.out](sd2_rects.out)). The package read the VBF at
  `D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf`. The extract tree `D:/FFXII_TZA_extract` holds the same bytes:
  "extract == VBF copy for 20 of 20 files (10 languages)" for `mrppack_ys.bin` and `tex2pack_ys.bin`. The us sha256
  prefixes are `ceec522d4125f14f` (mrppack, 104512 B) and `24a799ed14012525` (tex2pack, 4894416 B). All data reads
  below come from the extract tree.
- **Record 12, parsed a different way.** The package walks items one after another from the end of table A. I jumped
  instead to record 12's own row-relative `+0x10` offset (the relocation the MRP page describes at `002A1AC3`..`002A1AD9`).
  The result is the same: dword0 `0x1000300C` (12 items), `+0xC` = 7, items at unit `+0xCD0`.
- **The item-to-rectangle mapping, decoded from code and data. This was the step the README left to the eye.**
  - The type-2 constructor `0029F4C0` computes `T = [atlas+0x20] + 0x30` (`0029F4E7`, `0029F4F1`). It looks the item's
    `u16 +0x0E` up through two levels (`0029F4F5`..`0029F505`) and stores `T + u16[T+0x10] + entry*8` at node `+0x20`
    (`0029F50B`..`0029F518`). It copies the item's `u16 +0x10` to node `+0xA` (`0029F51C`, `0029F520`). Types 2 and 9
    reach it from the constructor table at `00243538`: slots 1 and 8 both hold `0024344B`, which calls `0029F4C0` at
    `00243451`.
  - The widget's own item painter `00366A30` reads the rectangle at `[node+0x20] + (s16)node+0xA * 8` (`00366A3A`,
    `00366A43`, `00366A6F`..`00366AA4`): x = `u16 +0`, y = `u16 +2`, w = `u16 +4 & 0xFFF`, h = bits 12-23 of the dword
    at `+4`. So the item's `+0x10` "cell" is a **frame index into the atlas's sub-image table**.
  - `00366A30`'s only callers are `00366E26` and `00366E8B`, both inside the draw arm; the per-item helper `00367110`
    has only `00366CDB` ([sd2_static.py](sd2_static.py) / [.out](sd2_static.out): E8/E9, jcc and stored pointers).
  - `0024A1D0` stores `rdx + 0x10` at slot `+0x20` (`0024A1EB`, `0024A238`). `00280670` passes
    `pack + u32[pack + 4k]` (`002806B0`, `002806B3`). So `T` is the TIM2 file + 0x40, the user-data area after the
    0x30-byte picture header. `battle_4_c`'s picture header is 0x780 bytes, so it carries 1872 bytes of user data.
  - Decoded: all twelve items use code `0x0B00`, which resolves to entry 180. [sd2_frames.out](sd2_frames.out) gives
    frames 0-7 of entry 180 as eight 46 x 42 rectangles on a three-wide grid at x 0 / 46 / 92, y 384 / 426 / 468. Frame
    *n* is grid cell *n* read row-major. The drawn items 0-6 (frames `0 1 2 2 5 6 7`) land at (0,384) (46,384) (92,384)
    (92,384) (92,426) (0,468) (46,468).
  - Cropping those seven rectangles in draw order ([rects_strip.png](rects_strip.png)) reads **F L E E I N G**. Reading
    the glyph shapes is still a visual reading, the reviewer's as well as the author's. **Which rectangle each item
    draws is no longer inferred.**
  - Undrawn items 7-11 (frames `6 1 7 8 9`) decode to N, L, G, a 1 x 1 rectangle and a 128 x 64 "HP" arrow
    ([rects_strip_7_11.png](rects_strip_7_11.png)). The README makes no claim about them.
- **W1-W4 re-read with the lane's disassembler** (`b8dis.py`).
  - Message dispatch at `00366BAA`..`00366BC1`: message 1 goes to the construct arm `00367044`, message 2 to
    `00366EFB`, message 4 to the draw arm `00366BD0`.
  - Construct: `0036704B`..`0036705C` passes `rcx = w+0x50`, `rdx = [[0209AC30]+8]`, `r8d = 0xC` to `002432B0`.
    `0036705C` is one of `002432B0`'s 113 raw call sites (index 113, my scan 113, jcc 0). `[01E0C1E8]` = `009152B0`,
    which reads "battle_4_c". `003670DC` calls `0024A5A0` with it and stores the result at `+0xC0`.
  - `00280980` fills slot *k* of `[0209AC30]` (8-byte stride, *k* < 23 since `rdi < 0x5c` by 4) with
    `pack + u32[pack + 4k]` from `[[0209AC30]+0x3D0]`. So `+8` is unit 1 of whatever pack sits at `+0x3D0`. That
    `+0x3D0` holds `mrppack_ys` remains the generator's read, as the README says. The unit's own name array does name
    `battle_4_c` for all twelve items, which is consistent with it.
  - Draw: `00366C6A`/`00366C71` loads the counter `word [[w+0xC8]]` and shifts it left 8. The step is
    `([022CBE08] << 7) / (+0xC + 1)`, computed at `00366CE6`..`00366D01`. `00366D06` multiplies it by the item index.
    `00366D0D jg 00366EB4` skips the item while the product exceeds the counter, so item *i* draws once the counter
    reaches it (equality draws). `+0xC8` is the message-1 argument's `+8` (`00367096`/`0036709A`). The loop bound is
    `00366ED5 cmp esi, [rax+0xc]` / `jb`.

**Controls.**
- The defect a wrong lookup would cause is a wrong rectangle. Its control is that the decoded source size must equal the
  authored 46 x 42 and must lie in the atlas: every drawn rectangle is 46 x 42 and inside 1024 x 512 (check B). Frame 8
  shows the control can fail, since it decodes to 1 x 1.
- The defect a wrong frame origin would cause is an off-by-one. Frames 3 and 4 decode to the A and P positions the
  package's crop shows, and the repeated item frame 2 gives the same rectangle twice.
- The defect for the data source is a stale VBF. The hash comparison covers all 20 files.

**Citations checked.** W1-W4 sites above were opened. EXP-025 and FM-1 are corroboration that the README cites without
leaning on them, so they are not re-read.

**Runtime routing.** None. The mapping is settled statically.

**Correction wording.** None needed for the verdict. Optionally, the producer may replace the Limits bullet "The
cell-to-rectangle mapping is inferred. ..." with: *"The cell-to-rectangle mapping is decoded (SWE2-AUDIT-SPEC review
`auditspec-review-sd2-0930/sd2_rects.py`): all twelve items resolve code `0x0B00` to sub-image entry 180 of
`battle_4_c`. The item's `+0x10` is a frame offset from that entry, read by `00366A30` at `[node+0x20] + frame*8`, and
frames 0-7 are 46 x 42 cells on a three-wide grid at x 0/46/92, y 384/426/468. Only the glyph reading of those
rectangles is visual."*
