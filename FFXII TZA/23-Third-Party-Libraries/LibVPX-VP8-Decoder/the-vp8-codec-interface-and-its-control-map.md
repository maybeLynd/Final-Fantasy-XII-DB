---
system: The VP8 codec interface and its control map - four handlers reached only by a stored pointer
category: 23-Third-Party-Libraries
status: DOCUMENTED
owner_layer: ThirdParty:Video.LibVPX_VP8_1_6_0
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the interface object read field by field from the image; the control map walked to its
    terminator; every handler body decoded; the base relocation table used to establish that the
    table pointer is each missing handler's only reference
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_kind: derivation
  last_pass_state: opus-vp8-iface-1 - reached by following the six unlisted blocks that carry a
    relocation (UD-3). Four of the eleven control handlers are absent from the function census;
    their only reference is a qword in this table.
  crossref_clean: false
  reopened_count: 0
---

# The VP8 codec interface and its control map

> `0016F070` is eight bytes - `lea rax, [rip + 0x1b6c219]` and `ret`. It hands back the object at
> `01CDB290`, whose first field points at the string **`WebM Project VP8 Decoder v1.6.0`**. That
> object is libvpx's codec interface, and **four of the eleven control handlers it reaches are not
> in the function census at all.**

## 1. The interface object at `01CDB290`

Read field by field from the image; every non-null slot in the first `0x48` bytes is a relocated
pointer.

| off | value | what it is |
|---|---|---|
| `+0x00` | `01CEB698` | the name string, **`WebM Project VP8 Decoder v1.6.0`** |
| `+0x08` | `0014000100000005` | two packed 32-bit fields - `00000005` and `00140001` |
| `+0x10` | `0016E110` | `vp8_init` |
| `+0x18` | `0016E210` | `vp8_destroy` |
| `+0x20` | **`01CDB320`** | **the control map** - section 2 |
| `+0x28` | `0016E380` | `vp8_peek_si` |
| `+0x30` | `0016E3A0` | (unnamed, 26 B sibling of `vp8_peek_si`) |
| `+0x38` | `0016E4A0` | `vp8_decode` — interior read 2026-09-17 (SWE2-FRONTIER): 1,494 B frame-decode
  body, carries `"Invalid frame width"`/`"Invalid frame height"`/`"Failed to allocate frame buffers"`,
  decode helpers `0016E290`/`0016E3C0`/`0016F2A0`, first call at [`0016E4EF`](../../_index/ADDRESS-INDEX.md) |
| `+0x40` | `0016EA80` | `vp8_get_frame` |
| `+0x48` .. `+0x90` | all zero | **nothing here is populated** |

**The names are the census's own**, not this page's: `vp8_init`, `vp8_destroy`, `vp8_peek_si`,
`vp8_peek_si_internal`, `vp8_decode` and `vp8_get_frame` are already in `functions.tsv` under those
names. The zero tail corroborates
[`../third-party-middleware-inventory.md`](../third-party-middleware-inventory.md)'s finding that
**only the decoder is linked** - the second half of this structure is empty.

## 2. The control map at `01CDB320`

A `{u64 id, pointer}` pair array, walked here to its terminator at `01CDB3D0` (`0xFFFFFFFF`).

| id | handler | in the census? | what the body does |
|---:|---|---|---|
| `1` | `0016EC20` | yes | - |
| `2` | `0016ECE0` | yes | - |
| **`3`** | **`0016EE40`** | **NO** | sets `[ctx+0xF8] = 1`, then copies **8 bytes from `[arg]` to `+0xFC` and 4 more from `[arg+8]` to `+0x104`** - a 12-byte configuration struct behind an enable flag |
| `4` | `0016EE70` | yes | `mov eax, 4 / ret` |
| `5` | `0016EE70` | yes | the same six bytes - **one shared body for four ids** |
| `6` | `0016EE70` | yes | " |
| `7` | `0016EE70` | yes | " |
| **`0x100`** | **`0016EE80`** | **NO** | requires `[ctx+0x1A8] == 0`, then from `[ctx+0x1B0]` packs three dwords at `+0x2BEC`, `+0x2BF0`, `+0x2BF4` as **`a + 2*(b + 2*c)`** - three flags into bits 0, 1, 2 - and stores the result through the out-pointer |
| **`0x101`** | **`0016EFF0`** | **NO** | ~~walks a `0x4C`-stride array twice over, comparing `[entry+2]`, and ORs three values into one dword through the out-pointer~~ **a 56-byte getter** (corrected 2026-09-15, `OPUS-CONTRA-VP8-HANDLER-0X101-MISATTRIBUTED`): returns 8 when the out-pointer or `[ctx+0x1B0]` is null, 1 when `[+0x1A38]` is null, else copies dword `+0x88` of that object through the out-pointer and returns 0 (`0016EFF0`–`0016F027`). `0016EFF0` is not in the function list, so a containing-function lookup had returned `0016EEC0` and its body was described here |
| `0x102` | `0016EEC0` | yes | the `0x4C`-stride nested loops formerly described under `0x101` (294 B, ~~two~~ three nested loop pairs over a `0x4C` stride *(corrected 2026-10-02, OPUS: passes for `3`, `2` and `1` at `0016EEC0+0x60`, `+0xA0` and `+0xD6`; UQ-310's answer)*) |
| **`0x103`** | **`0016F030`** | **NO** | stores **two qwords** from `[arg]` into `[ctx+0x108]` and `[ctx+0x110]`, or **zeroes both** when the argument is null - a callback pointer and its state |
| `0xFFFFFFFF` | - | - | terminator |

## 3. The error convention, derived from the handlers themselves

~~Three~~ Four distinct return values appear *(corrected 2026-10-02, OPUS: `0016EFF0+0x20` `mov eax, 1` when `[+0x1A38]` is null, row `0x101` above; the table below lists the other three)*, and each is reached by a distinguishable path:

| value | reached when |
|---:|---|
| `0` | the handler did its work |
| `4` | **always** - the shared body at `0016EE70` serving ids 4-7 is `mov eax, 4 / ret` |
| `8` | the argument pointer is null (`0016EE40`, `0016EE80`, `0016EFF0`) |

**Four control ids exist and are unconditionally refused.** That is a fact about this build, read
from a six-byte function, and it means those four features are present in the interface and absent
from the binary.

> In libvpx's public error enum these are `VPX_CODEC_OK`, `VPX_CODEC_INCAPABLE` and
> `VPX_CODEC_INVALID_PARAM`, and the ids `1`-`7` and `0x100`-`0x103` are its VP8 encoder-side and
> decoder-side control ranges. ~~**That mapping is inference from the upstream library, not something~~
> ~~this image states**~~ *(answered: `UQ-307` - the map is libvpx 1.6.0's `vp8_ctf_maps` and each body matches instruction for instruction; the names still come from the headers; 2026-10-02, OPUS)*, and the header is not in this repository. The numbers and the behaviour above
> are read from the image; the upstream *names* are not.

## 4. Why four handlers are missing from the census

The base relocation table is the loader's own list of every absolute address in the image. For each
of the four, **the qword in this control map is its only reference** - no `call`, no `jmp`, no
rip-relative `lea`, and no second relocation anywhere.

That is exactly the condition under which a reference-derived census produces nothing: the analysis
follows code references, and a function whose address is only ever *stored* is never defined. It is
the same mechanism recorded for `002FE7D0`, the `0x4021` wait handler, which FABLE read on
2026-09-12 and which sits in an action-dispatch table for the same reason.

See
[`../../99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md`](../../99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md)
for the measurement that found these four: **33,914 of 34,270 listed bodies carry an admissible static
reference** (~~34,262~~ counted `.pdata` entries, which are banned as evidence *(pass 6, 2026-09-15, OPUS)*), **and the unreferenced remainder is 244,619 bytes.**

## 5. What this does to the libvpx attribution

The middleware inventory pins libvpx VP8 1.6.0 from the banner string. **That banner is this
structure's name field** - the interface points at it - and the five functions the interface
dispatches to are already named `vp8_*` in the census. For *this* structure and the bodies it
reaches, the attribution is no longer a string match near some code: it is the library's own
dispatch table with the library's own entry points in it.

> **This does not raise the attribution of the 66 SIMD blocks at the head of `.text`.** Those are a
> separate population, ~~reached by nothing at all~~ referenced only by the decoder object and by each other - each of the 63 members of `libvpx-vp8-dsp-kernels.tsv` has a direct caller or a `lea`, and `0016F080` `lea`s four *(corrected 2026-10-02, OPUS: `0016F080+0xC4`..`+0xE7`; the inventory's kernel row)*, and they stay at tier 2 on the evidence recorded
> there. **One structure being proven does not prove its neighbourhood.**

## 6. What is not known

- [x] **UQ-307.** **Which upstream control each id is.** The ids and the behaviour are read; the names are not
      in the image.
      **ANSWERED 2026-09-26 (OPUS): the map is libvpx 1.6.0's `vp8_ctf_maps`, eleven entries in its order.**
      - `1` is `VP8_SET_REFERENCE`: it converts `vpx_ref_frame_t` and calls `vp8dx_set_reference` `0016F450`.
      - `2` is `VP8_COPY_REFERENCE`. It has the same guard and image conversion (not read in full).
      - `3` is `VP8_SET_POSTPROC`.
      - `4`-`7` are the four `VP8_SET_DBG_*` controls. They share one `VPX_CODEC_INCAPABLE` body, as 1.6.0 builds them
        without the postproc visualizer.
      - `0x100` is `VP8D_GET_LAST_REF_UPDATES`, `0x101` `VP8D_GET_FRAME_CORRUPTED`, `0x102` `VP8D_GET_LAST_REF_USED` and
        `0x103` `VPXD_SET_DECRYPTOR`. Each body matches instruction for instruction.
      - The names come from libvpx's headers; the image supplies the ids, the bodies and the version. See [`uq308-uq310-opus-libvpx-context-and-mode-info.md`](../../_index/candidates/uq308-uq310-opus-libvpx-context-and-mode-info.md).
- [x] **UQ-308.** **What `[ctx+0x1A8]`, `[ctx+0x1B0]` and the `0x2BEC` triple are** in the decoder's own
      context structure. Not laid out here.
      **ANSWERED 2026-09-26 (OPUS).** The context is libvpx 1.6.0's `vpx_codec_alg_priv_t`, 0x330 bytes, from its own
      `vpx_memalign(16, 0x330)` in `vp8_init_ctx` `0016E070`.
      - `+0x1A8` is `yv12_frame_buffers.use_frame_threads`. Its only writer, `vp8_init` (`0016E1F1`), writes 0, so every
        gate on it passes in this build.
      - `+0x1B0` is `pbi[0]`, the `VP8D_COMP` decoder instance (0x4480 bytes, `create_decompressor` `0016F2A0`).
      - `pbi+0x2BEC` / `+0x2BF0` / `+0x2BF4` are `refresh_last_frame` / `refresh_golden_frame` / `refresh_alt_ref_frame`.
        Control `0x100` reports them with weights 1 / 2 / 4.
      - Declared as `VpxVp8DecoderContext` and `Vp8DecoderInstance` in `_types`. See [`uq308-uq310-opus-libvpx-context-and-mode-info.md`](../../_index/candidates/uq308-uq310-opus-libvpx-context-and-mode-info.md).
- [x] ~~**UQ-309.** **Whether the game ever calls any of these controls.** `0016F070` hands out the interface;
      who asks for it, and whether any caller issues a control at all, is not established.~~ **Answered 2026-09-14
      (FABLE): no control is ever issued, and the dispatcher that would issue one is not in the image.**
      - **One consumer.** The 8-byte getter `0016F070` (`lea rax, [01CDB290]`) has a single call site, at `0067A55F`,
        in the 1,253-byte movie decoder set-up.
        - That set-up passes the interface straight to `vpx_codec_dec_init_ver` (`0067A57D`), with ABI version `0xA`,
          flags 0 and a configuration of `{threads, 0x780, 0x438}`.
        - The first field is the population count of a mask that one import returns, with a second import as a fallback when that count is zero. 0x780 × 0x438 is 1920 × 1080
          (`0067A54E`–`0067A558`).
        - Decoding then runs through `vpx_codec_decode`.
      - **No dispatcher.** libvpx's `vpx_codec_control_` walks `iface->ctrl_maps` in 16-byte `{id, fn}` steps and calls
        `fn`. A sweep of every listed function up to 4,000 bytes finds none that steps a register by `0x10`, compares the
        entry it points at, and calls through `[reg + 8]`.
        **Strengthened 2026-09-15 (`OPUS-CONTRA-VPX-BLOCK-IS-5-PERCENT`, re-derived by FABLE).** Over the whole curated libvpx
        population ([`libvpx-vp8-decoder.tsv`](../members/libvpx-vp8-decoder.tsv) + [`libvpx-vp8-dsp-kernels.tsv`](../members/libvpx-vp8-dsp-kernels.tsv),
        188 members, 85,842 B, no size cap) there is **no `call qword ptr [reg + 8]` at all**. OPUS's one tag-population site
        lies in an engine manager constructor that is mis-tagged as libvpx support (`OPUS-NOTICE-VPX-SINGLETON-MISTAG`).
      - **No reader of the map field** — ~~Across the libvpx block (`0016D840`–`0016F080`, including `vpx_codec_dec_init_ver`,
        `vpx_codec_decode` and `vpx_codec_destroy`), no instruction reads interface `+0x20`.~~ **narrowed 2026-09-15.**
        - The negative was measured only over `0016D840`–`0016F080`. That span is about 5% of libvpx by byte (18 of 188 curated
          members, 4,382 B), and its low edge is not libvpx: the curated decoder object starts at `0016DDD0`.
        - Across the full population there are 62 memory operands at displacement `0x20` off a non-stack register. They are
          not triaged: a displacement is not a type, and most index frame buffers and thread contexts.
        - **So "nothing reads interface `+0x20`" holds for the three API entry points in the span only.** The conclusion below
          rests on the full-population dispatcher negative and the handler-address census, not on this one.
      - **No other reference.** The control handlers' addresses occur only as the map's own qwords: once each, and eight
        times for the shared body of ids 4–7.
      - So the control map is linked data that nothing walks. A caller in the image's unreferenced code would itself be
        unreachable.
- [x] **UQ-310.** **The `0x4C`-stride array `0016EEC0` walks** (this row said `0016EFF0`; corrected below). Two nested loops over it, contents unread.
      *Re-pointed and narrowed 2026-09-15 (OPUS) — **the address in this question is wrong**, and
      it is wrong because of the misattribution this page already corrected today
      (`OPUS-CONTRA-VP8-HANDLER-0X101-MISATTRIBUTED`, row `0x101` above). **`0016EFF0` walks
      nothing** — it is a 56-byte getter. **The `0x4C`-stride walk is in `0016EEC0`**, whose body
      the misattribution had printed under `0016EFF0`. The question is real; only its address was.*
      - **It is a 2-D grid, and the context names both dimensions.** With `r11 = [rcx+0x1B0]` (the
        codec context): base **`[r11+0x1EB0]`**, outer count **`[r11+0x1E74]`**, inner count
        **`[r11+0x1E78]`**, entry size **`0x4C`** (`0016EEEF`–`0016EF3F`).
      - **Each row carries one entry more than the inner count.** After the inner loop ends, the
        cursor advances a further `0x4C` at **`0016EF35`** before the next row — so the row pitch is
        `(inner + 1) × 0x4C`, not `inner × 0x4C`. A reader that assumes a dense grid will drift by
        one entry per row.
      - **The discriminant is a byte at `+0x02`, and two values are searched.** The first pass looks
        for **`3`** (`0016EF20`) and the second, over the same grid from the same base, for **`2`**
        (`0016EF60`) — ~~two full passes, not one~~ three full passes, the third for `1` *(corrected 2026-10-02, OPUS: `0016EEC0+0xD6` compares the byte with `dil` = 1; the answer below)*.
      - **The whole walk is gated on `[rcx+0x1A8] == 0`** (`0016EECE`) and on the out-pointer being
        non-null; otherwise it returns without touching the grid.
      - ~~**Still open:** what the other `0x4A` bytes of each entry hold, and what kinds `2` and `3`
        mean. **UQ-310.**~~
      - **ANSWERED 2026-09-26 (OPUS).** The grid is libvpx 1.6.0's `MODE_INFO` array, `common.mi`. Its row pitch is
        `mode_info_stride` (`+0x1E7C`) = `mb_cols + 1`, with one border entry per row.
        - **There are three passes, not two.** The third (`0016EF7D`-`0016EFB0`) compares against `dil` = 1, and the result
          is `altref*4 | golden*2 | last`. This is `vp8dx_references_buffer` inlined three times.
        - `+0x02` is `mbmi.ref_frame`, so kinds `3` and `2` are **altref** and **golden**, and `1` is **last**.
        - Every byte of the 0x4C entry is read in the mode decoder (`0017B580`, `0017A320`, `0017B010`, `0017AC50`):
          `mode`, `uv_mode`, `ref_frame`, `is_4x4`, `mv.row`, `mv.col`, `partitioning`, `mb_skip_coeff`,
          `need_to_clamp_mvs`, `segment_id`, and `bmi[16]` at `+0x0C`.
        - Declared as `Vp8ModeInfo` in `_types`. See [`uq308-uq310-opus-libvpx-context-and-mode-info.md`](../../_index/candidates/uq308-uq310-opus-libvpx-context-and-mode-info.md). **UQ-310.**
- [x] **UQ-311 ANSWERED 2026-09-15 (OPUS) — they are libvpx's `abi_version` and `caps`, and
      the caps value decomposes exactly, with no bit left over.**
      - **`+0x08` = `0x00000005` is `abi_version`** — `VPX_CODEC_INTERNAL_ABI_VERSION`. It is
        **not** the `0xA` §5 records being passed to `vpx_codec_dec_init_ver`: that is
        `VPX_DECODER_ABI_VERSION`, a different constant of the same library, so the two coexisting
        is expected rather than a discrepancy.
      - **`+0x0C` = `0x00140001` is `caps`**, and it is exactly three flags — `0x1` **DECODER**,
        `0x40000` **POSTPROC**, `0x100000` **INPUT_FRAGMENTS**. **`0x140001` with those three
        cleared is `0`**, and that zero is the check: a mis-mapping would almost certainly leave a
        bit over.
      - **What it says about the build.** The interface advertises a **decoder only** — no
        `ENCODER` bit — with post-processing and fragmented input compiled in, and **without**
        `FRAME_THREADING`, `ERROR_CONCEALMENT`, `PUT_SLICE` or `PUT_FRAME`. The absent
        `FRAME_THREADING` is the interesting one next to §5's note that the configuration passes a
        thread count.
      - *Scope, stated so the credit is right: the version pin is the table above, not this answer.
        `+0x00`'s name string `WebM Project VP8 Decoder v1.6.0` was already recorded there, and it is
        what makes matching these offsets against that version's `vpx_codec_iface_t` legitimate. The
        flag **names** come from libvpx's public headers; the image supplies the offsets, the values
        and the version.* **UQ-311.**

## 7. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| the interface object's layout and contents | read field by field at `01CDB290`; every pointer slot cross-checked against the relocation table | 1 |
| `0016F070` returns it | `lea rax, [rip + 0x1b6c219]` / `ret`, eight bytes, target `01CDB290` | 1 |
| the control map's eleven entries and terminator | walked from `01CDB320` to `01CDB3D0` | 1 |
| four handlers are absent from `functions.tsv` | literal lookup against the census | 1 |
| **the table pointer is their only reference** | the base relocation table plus direct-branch and `lea` scans over all of `.text` | 1 |
| each handler's behaviour | full disassembly of each body | 1 |
| ids 4-7 are unconditionally refused | `0016EE70` is `mov eax, 4 / ret` and four ids point at it | 1 |
| **the upstream names of the ids and error codes** | libvpx's public headers, **not present in this repository** | 3 |

## 8. Related

- [`../third-party-middleware-inventory.md`](../third-party-middleware-inventory.md) - where libvpx VP8 1.6.0 is pinned, at ~~73 listed functions~~ 183 declared functions - decoder 116, its UC-1 row 4, kernels 63 *(answered: the inventory's front matter; 2026-10-02, OPUS)*
- [`../../99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md`](../../99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md) - the census defect these four fall through
- [`../../99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md`](../../99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md) - the referenced population, of which these are the pointer-reached six
- [`../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md`](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md) - `002FE7D0`, the same defect in the engine's own code
- [`../../17-Presentation-Rendering/Movie-Containers/README.md`](../../17-Presentation-Rendering/Movie-Containers/README.md) - the 10.4 GB of `.webm` this decoder exists for
