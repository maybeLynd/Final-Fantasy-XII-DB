# RC-29 to RC-34: an independent check of the console table, loca_*.cl2, menuquest.lst and meshdata.mg answers (ORACLE, 2026-09-30)

## The question

SWE2-CONTRACT's batch 3 registered six rows:
- **RC-29:** the walker of the "menu resource manifest" at `.rdata` `008FCE00`-`008FD2D0`;
- **RC-30:** the reader of a loaded `loca_*.cl2`;
- **RC-31:** the `menuquest.lst` parser;
- **RC-32:** the `meshdata.mg` reader;
- **RC-33:** `meshdata.mg`'s undecoded bytes;
- **RC-34:** which textures the `mainN.psd` slots resolve to.

SWE2-DATA answered all six on 2026-09-29 (`../rc22-34-resource-readers-0930/`, commit `1261e2044`): five answered and
RC-30 narrowed. This record checks their load-bearing facts with its own code. It then narrows RC-30 further, by
bounding two of the three request sites SWE2-DATA left open and reducing the third to one argument byte.

## Method

[`rc29_review.py`](rc29_review.py), output [`rc29_review.out`](rc29_review.out). It uses:
- the batch helper `../rc22-as7-pages-0930/arc.py`;
- the kind-7 row replay `../rc6-console-map-codes-0930/rc5_paths.py`.

Each check (K) re-derives its fact from the image or the shipped files. All pass.

| check | what it re-derives | result |
|---|---|---|
| K29a | every decoded instruction whose rip target falls in the block, plus a raw scan for the image-base-relative displacement `0x7DCE00` | exactly `001D150F` (in `001D0390`), `001D537D` and `001D542A` (in `001D5260`), and `001CD186` (`[rsi + rcx*4 + 0x7DCE00]`) |
| K29b | page geometry | `001D5260` stores 14 at `+0xA88`; the block is 14 x 0x58 bytes |
| K29c | the block's contents | every u32 is a console command id no larger than `0x126`, the row renderer's range |
| K30a | site `003C9950` (id `0xE + byte[obj+0xC1]`) | the byte's writers in the widget module are: 5 (`003C95F9`), 2 (`003C9611`), the table `00D11720` = {0, 2, 3, 4, 3, 6, 0, 0} (`003C974F`), or the `003C9A30` loop index 0-6 (`003C9D28`/`003C9D46`); so the id is `0x0E`-`0x14` |
| K30b | site `002CEAE0` (id `0x10 + byte[[0209AC30]+0xB2D]`) | gated by `+0xD3C` bit 1; the byte and the gate are set together only at `002833ED`/`00283400`, from a guest member's id word `+0x60` (its `BattleStatsRecord.definitionRowIndex`, see RC-25 in `../rc22-as7-pages-0930/`); otherwise the byte is 0xFF and the gate is clear (`002832C7`, `002832D5`) |
| K30c | site `00575C30` (id `u16 00D23740[arg[0]] + word[obj+0xCA]` (+ `word arg[2]`)) | only caller `00575B2B` (the message proc `00575A50`); table entries 0-5 are 552-852 and entries 6 and 7 are 0 |
| K31a | `0037EFC0` (no `.pdata`) | count u16 at `+0x0E`, entries at `+0x10` with stride 8, first match, string `lst + u16[+8] + u16[entry+2]` |
| K31b | all 9 `menuquest.lst` | header `+4` = 100 in all; directory ids unique; entry `+4` words only 0, 3 and 4 |
| K32 | `00274780` and the file | returns `buf + s32[buf + 8i]`; `meshdata.mg` is two `{offset, size}` entries (`0x10`+`0x2C0`, `0x2D0`+`0x3280`) that fill its 13,648 bytes exactly |
| K34 | `00D23270` and the kind-7 rows | the name table is `main0..3.psd` → `w_main0..3`, `upper` → `w_shade_p`, `linetex` → `w_line01`; kind 7 `0xA8` = `WorldMap\meshdata.mg`, `0xAA` = `w_shade_p.tm2`, `0xAB`-`0xAE` = `Tm2_Menu\w_main0..3.tm2` |

## Result

- **RC-29: agrees with SWE2-DATA, ANSWERED with the premise refuted.** The block is the developer console's 14-page x
  22-row command-id table. Four code sites reach it: three rip-relative, one image-base-relative.
- **RC-30: NARROWED further.** Of SWE2-DATA's three unbounded computed-id sites:
  - `003C9950` **cannot** request `0xE2`-`0xE4`: its id is `0x0E`-`0x14`.
  - `002CEAE0` requests `0x10 + d`, where `d` is a guest member's `definitionRowIndex`. It reaches a `loca_*.cl2` id
    only if a guest's `definitionRowIndex` is `0xD2`-`0xD4`. That is the same authored value RC-25 leaves open.
  - `00575C30` cannot reach them when its message byte `arg[0]` is 0-5 (the id is then at least `0x228`). It can only
    through `arg[0]` 6 or 7, where the table entry is 0 and the id is `word[obj+0xCA]` (+ `word arg[2]`).
  - SWE2-DATA's 18 computed-kind path-API sites are untouched here.
  - **Residue (static):** a guest's `definitionRowIndex` range; `00575A50`'s message byte `arg[0]` and
    `word[obj+0xCA]`; the 18 computed-kind sites.
- **RC-31: agrees, ANSWERED.** The directory walk, the 100 that no reader bounds, the `+4` words 0/3/4, and the
  unique ids that make the lookup independent of the shipped order all re-derive.
- **RC-32 and RC-33: agree, ANSWERED.** The two-entry `{offset, size}` directory re-derives, and it dissolves the
  "different order" premise as SWE2-DATA states. This record did not re-run SWE2-DATA's 125-check vertex, strip and
  slot walk (`mg_reader_check.py`). It checked only the directory geometry that the RC-33 byte placement rests on.
- **RC-34: agrees, ANSWERED.** `mainN.psd` draws with `Tm2_Menu\w_mainN.tm2`, kind 7 ids `0xAB`-`0xAE`, in the
  `us` region's array.

## Not claimed

- The `+0xC1` writer set is from a raw scan limited to the widget module `003C0000`-`003D0000`, not the whole image.
- SWE2-DATA's RC-33 byte-by-byte placement and its draw-path details, beyond the directory geometry checked here.
- Anything about the `CLT2` component order or `variant`: no reader is reached yet.
