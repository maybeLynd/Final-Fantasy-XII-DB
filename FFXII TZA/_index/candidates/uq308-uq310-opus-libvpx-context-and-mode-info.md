# UQ-308 / UQ-310: the VP8 decoder's context fields and its 0x4C grid are libvpx 1.6.0's `vpx_codec_alg_priv_t` and `MODE_INFO` (OPUS, 2026-09-26)

**Evidence class: STATIC.** Every instruction below was re-read in the shipping image (sha256 `73461d08…21f8`).
The version is pinned by the interface's own name string, `WebM Project VP8 Decoder v1.6.0` at `01CEB698`. The
image supplies the offsets, widths, values and control flow. The member **names** and enum names come from libvpx
1.6.0's headers, the same basis as UQ-311. Independent review is requested (author OPUS).

## 1. The four "absent" control handlers are libvpx's, body for body

The control map at `01CDB320` has eleven entries: ids 1-7 and `0x100`-`0x103`. That is exactly the size of
`vp8_dx_iface.c`'s `vp8_ctf_maps`. The four handlers that UQ-308/UQ-310 are about match it instruction for
instruction.

| id | libvpx name | handler | what the body does |
|---:|---|---|---|
| `0x100` | `VP8D_GET_LAST_REF_UPDATES` | `0016EE80` | returns `8` (`VPX_CODEC_INVALID_PARAM`) on a null argument or when `[ctx+0x1A8]` != 0 (`0016EE83`-`0016EE8F`). Otherwise stores `[pbi+0x2BEC] + 2*([pbi+0x2BF0] + 2*[pbi+0x2BF4])` (`0016EE98`-`0016EEB5`): weights 1/2/4 = `VP8_LAST_FRAME`/`VP8_GOLD_FRAME`/`VP8_ALTR_FRAME` |
| `0x101` | `VP8D_GET_FRAME_CORRUPTED` | `0016EFF0` | returns `8` on a null argument or a null `pbi`. Returns `1` (`VPX_CODEC_ERROR`) when `[pbi+0x1A38]` (`frame_to_show`) is null. Otherwise it reports that buffer's `+0x88` (`corrupted`) (`0016F004`-`0016F01C`) |
| `0x102` | `VP8D_GET_LAST_REF_USED` | `0016EEC0` | the same two error exits. Then **three** grid passes testing `[entry+2]` against 3, 2 and 1 (`0016EF20`, `0016EF60`, `0016EF96`, `dil = 1`), result `alt*4 \| gold*2 \| last` (`0016EFB4`-`0016EFCD`). This is `vp8dx_references_buffer` inlined three times |
| `0x103` | `VPXD_SET_DECRYPTOR` | `0016F030` | copies `{cb, state}` into `+0x108`/`+0x110`, or zeroes both on a null argument |

Control `3` (`0016EE40`, `VP8_SET_POSTPROC`) belongs to the same family. It sets `+0xF8 = 1` and copies the 12-byte
`vp8_postproc_cfg_t` to `+0xFC`.

**The page's UQ-310 text said the walk makes two passes; there are three.** The third pass (`0016EF7D`-`0016EFB0`)
compares against `dil`, which was set to 1 at `0016EEF6`. That is why the row saw only two immediates.

## 2. UQ-308: `[ctx+0x1A8]`, `[ctx+0x1B0]` and the `0x2BEC` triple

- **The context is `vpx_codec_alg_priv_t`, size `0x330`, from its own allocation.** `vp8_init_ctx` (`0016E070`)
  allocates it with `vpx_memalign(16, 0x330)`: `malloc(0x347)` at `0016E079`, the pointer aligned at `0016E090`-`0016E09A`,
  the original stored at -8, and a memset of `0x330` at `0016E094`-`0016E0A5`.
- **Eleven accessed offsets fall where libvpx 1.6.0 puts the members.** This depends only on the image and the
  pinned version's struct:
  - `+0x08` `init_flags` (`0016E0B1`);
  - `+0xD8` `cfg` (`0016E0D7`-`0016E0EC`);
  - `+0xE4` `si.sz = 0x10` (`0016E0C4`);
  - `+0xF8`/`+0xFC` the postproc pair;
  - `+0x108`/`+0x110` `decrypt_cb`/`decrypt_state` (`0016E0B6`, `0016F03B`);
  - `+0x1A8` `yv12_frame_buffers.use_frame_threads`;
  - `+0x1B0` `yv12_frame_buffers.pbi[0]`;
  - `+0x2B8`/`+0x2BC` `fragments.enabled`/`count` (`0016E1D6`-`0016E1E4`).

  With `vpx_image_t` at 0x88 bytes, `img` runs `+0x118`-`+0x19F`, which puts `img_setup` at `+0x1A0` and
  `use_frame_threads` at `+0x1A8`. `pbi[32]` then ends at `+0x2B0` (`user_priv`), fragments start at `+0x2B8`, and
  `ptrs[9]` + `sizes[9]` end at `0x32C`. Rounded, that is `0x330`, the allocation size.
- **`[ctx+0x1A8]` = `use_frame_threads`, and in this build it is always 0.** `vp8_init` writes 0 at `0016E1F1`
  (libvpx 1.6.0: "for now, disable frame threading"). That is its **only** writer in the libvpx object `0016DDD0`-`0017C890`
  (census of every `[reg+0x1A8]` access). Every reader (`0016E216`, `0016E5EB`, `0016EC36`, `0016ECF9`, `0016EE88`,
  `0016EECE`) therefore takes the single-thread path.
- **`[ctx+0x1B0]` = `pbi[0]`, the decoder instance (`VP8D_COMP`).** `vp8_decode` stores `create_decompressor`'s result
  there (`0016E5F4`-`0016E5F9`). `create_decompressor` (`0016F2A0`) allocates `vpx_memalign(32, 0x4480)`: `malloc(0x44A7)`
  at `0016F2BC`, memset `0x4480` at `0016F2F5`.
- **The `0x2BEC` triple is `common.refresh_last_frame`, `refresh_golden_frame` and `refresh_alt_ref_frame`.** Control
  `0x100` gives them weights 1, 2 and 4, which are libvpx's `VP8_LAST_FRAME`, `VP8_GOLD_FRAME` and `VP8_ALTR_FRAME`.
  The weights, not the order, fix which is which.

## 3. UQ-310: the 0x4C grid is `MODE_INFO`, and every byte is accounted for

The grid is `common.mi` (`pbi+0x1EB0`), with `mb_rows` rows (`+0x1E74`) and `mb_cols` entries per row (`+0x1E78`). The
row pitch is `common.mode_info_stride` (`+0x1E7C`) = `mb_cols + 1`. The extra entry is libvpx's border column, which
is why each walk adds one more `0x4C` after the inner loop. `+0x1E7C` is the stride the key-frame reader uses to find
the macroblock above (`mi - stride*0x4C`, `0017A328`/`0017A398`).

Each entry was read in the bodies that write it:
- the mode loop `0017B580` (`vp8_decode_mode_mvs`);
- the key-frame reader `0017A320` (`read_kf_modes`), chosen when `common.frame_type` (`+0x1E64`) is 0;
- the inter reader `0017B010` (`read_mb_modes`);
- the split-mv decoder `0017AC50` (`decode_split_mv`).

| off | size | libvpx member | the instructions |
|---|---|---|---|
| `+0x00` | 1 | `mbmi.mode` | from `read_kf_ymode` at `0017A345`, B_PRED tested as 4 (`0017A347`). The inter reader stores 5/6/7/8/9 = NEARESTMV/NEARMV/ZEROMV/NEWMV/SPLITMV (`0017B469`, `0017B464`, `0017B4EA`, `0017B43B`, `0017B3E6`) |
| `+0x01` | 1 | `mbmi.uv_mode` | `read_uv_mode` `0017A250` result, stored at `0017A485` / `0017B54A` |
| `+0x02` | 1 | `mbmi.ref_frame` | 0 on key frames (`0017A339`). On inter frames it is `read(prob_intra)`, then `read(prob_last)`, then `2 + read(prob_gf)` (`0017B05D`, `0017B0B7`), with the probabilities at `pbi+0x4444`/`+0x4445`/`+0x4446` |
| `+0x03` | 1 | `mbmi.is_4x4` | cleared per macroblock (`0017B809`). Set to 1 for B_PRED (`0017A381`, `0017B50C`) and for SPLITMV (`0017B3E9`) |
| `+0x04` | 2 | `mbmi.mv.row` | `read_mvcomponent(mvc)*2` (`0017B3F8`-`0017B407`) plus the best-mv row (`0017B420`) |
| `+0x06` | 2 | `mbmi.mv.col` | `read_mvcomponent(mvc+0x13)*2` (`0017B40B`-`0017B417`) plus the best-mv column (`0017B429`). The pair also moves as one `int_mv` dword |
| `+0x08` | 1 | `mbmi.partitioning` | `decode_split_mv` reads probabilities 110/111/150 (`0017AC90`, `0017ACB6`, `0017ACC7`) and stores `s` at `0017AFF4` |
| `+0x09` | 1 | `mbmi.mb_skip_coeff` | read with `prob_skip_false` (`pbi+0x4447`) when `common.mb_no_coeff_skip` (`pbi+0x1E80`) is set, else 0 (`0017B790`-`0017B805`) |
| `+0x0A` | 1 | `mbmi.need_to_clamp_mvs` | cleared at `0017B083`, stored at `0017B456`, ORed per sub-block at `0017AF8A` |
| `+0x0B` | 1 | `mbmi.segment_id` | read from a three-probability tree (`pbi+0xF64`..`+0xF66`) when `pbi+0xF61` and `+0xF60` are set. Set to 0 on key frames when `+0xF61` is clear (`0017B620`-`0017B78C`) |
| `+0x0C` | 64 | `bmi[16]` | 4 bytes each. The key-frame reader reads the above macroblock's `bmi[12+i]` and its own `bmi[i-4]` (`0017A3C2`, `0017A3E4`). The split decoder writes `bmi[k]` (`0017AFB7`) and reads the left neighbour's `bmi[k+3]` and the above one's `bmi[k+12]` (`0017AD26`, `0017AD43`) |

So the byte at `+0x02` is the reference frame. The "kinds 2 and 3" the row asked about are **golden** and
**altref**, and the third pass is **last**.

## 4. What is declared

- **`Vp8ModeInfo` (0x4C).** `TYPE RESOLVED`, every field `SEMANTICALLY IDENTIFIED`. Route `CHAIN Vp8DecoderInstance
  +0x1EB0 stride=0x4C`.
- **`VpxVp8DecoderContext` (0x330).** `TYPE RESOLVED`. Eleven accessed rows are stated. The unaccessed members
  (`base` except `init_flags`, `decoder_init`, `img`, `img_setup`, `user_priv`, `fragments.ptrs`/`sizes`) are
  `DISCOVERED` rows marked *position only*.
- **`Vp8DecoderInstance` (0x4480).** `SIGNATURE RESOLVED`. Nineteen accessed members are stated: the macroblock edges,
  `frame_to_show`, `frame_type`, the grid geometry, `mi`, `mb_no_coeff_skip`, the refresh triple, the modes bool
  decoder and the four probabilities. The rest is tiled with unobserved spans. The embedded `MACROBLOCKD` and
  `VP8_COMMON` are not typed separately.
- `types_index.py --validate`: 779 types, 0 errors, 0 gaps. `check_storage_class.py`: 0 hard failures.

## 5. Not claimed

- The names of `pbi+0xF60`/`+0xF61`. The code shows only that they gate the segment-id read.
- The layout of `vpx_image_t` beyond its extent.
- Anything about how the engine drives the decoder (who calls `vpx_codec_decode`, or which controls it issues). The
  page's "no dispatcher" finding stands.
- Whether libvpx 1.6.0 was built unmodified. Every body read here matches it; the rest of the object was not
  compared.
