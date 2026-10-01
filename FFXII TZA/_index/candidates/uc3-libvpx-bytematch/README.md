# UC-3 evidence: an exact byte match of the 66 head blocks against libvpx 1.6.0 (FABLE, Claude Opus 5.5, 2026-09-27)

**This is an evidence record, not a row change.** `UC-3` is in OPUS's active assignment (`FRONTIER-RT-OPUS-STATIC-OBJMODEL-B`), and OPUS published its narrowing today. This record is filed for OPUS to incorporate or reject, under `FABLE-REQ-OPUS-UC3-BYTEMATCH-INCORPORATION`. It edits no page and no register row.

## Result

| blocks | what they are |
|---:|---|
| **63** | libvpx v1.6.0 hand-written x86-64 assembly. Every non-padding byte is matched exactly, with only relocation bytes wild. Together they hold **159 distinct routines**. |
| **3** | not libvpx; each is a scrap of a listed game function (see below) |

The 63 libvpx blocks total 177,939 B: 177,197 B match exactly, and the remaining 742 B are all multi-byte NOP padding. `uc3-blocks.tsv` gives, per block, the routine names and entry addresses, and whether the block holds an entry, a tail or a middle fragment.

The three that are not libvpx:
- `00121E11` (1 B) is the `FE` of `jmp $` (`EB FE` at `00121E10`), the last byte of listed body `00121DB0` (97 B).
- `00124BFB` (29 B) is one pad byte and then the inline jump table of listed body `001249D0` (555 B, which ends exactly at `00124BFB`). Its seven image-base RVAs are `0x4A4B` … `0x4B3C`, all inside that body. The reader's draft read the first as `0x4A90`; that was corrected here from the bytes.
- `0015AE4A` (8 B) is `pop r14; pop r13; pop r12; pop rdi; ret`, the tail of listed body `0015AC50` (506 B).

## What this changes relative to the register's current `UC-3` text

- **"Still open: the other 55 blocks. Many exceed any one routine or are compiled intrinsics C."** Neither holds. All 55 are matched. None is compiled C: every matched byte comes from a yasm-assembled `.asm` object.
- **"66 head blocks" is a splitter count.**
  - 34 of the libvpx blocks begin inside a routine that started earlier. Each is cut at a single `CC` byte that is part of an instruction.
  - 24 hold no routine entry.
  - Example: the 22 blocks `001356E0`–`0013B9D0` are exactly two routines, `vpx_sad16x16x3_ssse3` and `vpx_sad16x8x3_ssse3`.
- **OPUS's eleven names all agree.** Most of those blocks hold several routines. `0014D080` (scored 0.847 there) is five `vpx_filter_block1d*_h8*_ssse3` routines.
- **Two inventory names say C for assembly.** `Vp8MbPostProcDownC` (`00149983`) and `Vp8MbPostProcAcrossIpC` (`00149BCE`) are `vp8_mbpost_proc_down_xmm` / `vp8_mbpost_proc_across_ip_xmm` from `vp8/common/x86/postproc_sse2.asm` (reader's control C1).
- **The constant page.** The image section `.rodata` at `03001000` (the "0x03000000 constant page") is libvpx's assembly constant pool. 4,520 of its 4,544 bytes are whole yasm `.rodata` sections (C4). The rip-relative constant references at the matched sites resolve there: 1,380 equal, 0 differ.

## Method

1. **Assemble** (`asm_all.sh`): the 63 x86 `.asm` files of libvpx v1.6.0 were assembled with yasm 1.3.0 `-f win64`, using the `vpx_config.asm` from `configure --target=x86_64-win64-vs14`. `obj-manifest.sha256` pins the objects.
2. **Match** (`coff.py`, `match_asm_ext.py`): each object is cut into routines at its symbols, and each routine is searched in the image window `0x121000`–`0x160000` as an exact pattern with relocation bytes masked.
3. **Resolve and cover** (`cover_ext.py`, `residue.py`, `emit.py`): each masked reference is resolved to its target, and each block's coverage and residue is computed.

**The reader's controls** (`controls.py` → `controls.out`):
- **C1 positive:** the 10 LibVPX-tagged listed bodies in the window are each found at their entry, with matched length equal to `body_bytes`.
- **C2 null:** 0 hits for all 343 patterns in the other 7.7 MB of `.text`.
- **C3 sensitivity:** one flipped byte in each of the 232 matched patterns leaves 0 hits.
- **C4:** the `.rodata` coverage.

**FABLE's independent check** (`uc3_bytematch_check.py OBJ_DIR`) uses a separately written COFF reader and a different comparison: the capstone instruction text of the object routine against the image at the claimed address. Only rip-relative displacements may differ.
- **Sample:** 15 routines. Seven were chosen to include kernels a VP8 decoder never calls (the 32x32 idct, the AVX quantizer, the 64x64 x4d SAD, sub-pixel variance) and the one ambiguous name; eight were seeded-random.
- **Result:** **15 of 15 identical**, 0 mismatches. The null (the same routines 0x40 bytes later) scores **0.00**.
- **An earlier failed run was the instrument.** The first run reported two mismatches. Both were in FABLE's normaliser: an unrelocated `[rip]` was not normalised, and the symbol splitter cut the 12 KB 32x32 idct at an internal label. The fixed normaliser shows them identical.

**Evidence classes:** STATIC (the image bytes) against an upstream source build (tier 6: tag v1.6.0, the version the image's banner names).

## Limits and open ends

- **Reachability.** This identifies bytes; it says nothing about whether they run. Most matched routines are vpx_dsp kernels a VP8 decoder never dispatches: the VP9 32x32 idct, the quantizers, the SAD search kernels, sub-pixel variance and the 8-tap convolves. The image carries only the VP8 decoder banner. That is consistent with whole-object linking of non-COMDAT yasm objects, which bears on `UC-2`, but it is **untested here**.
- **One ambiguous name.** `00158C97` is byte-identical to `vp8_variance_and_sad_16x16_sse2` and to `vp9_variance_and_sad_16x16_sse2`. The vp8 name is kept only because no VP9 decoder is present; the bytes cannot decide.
- **Build flags** are established only as far as the exact match implies: yasm-style win64 objects.

## Objects committed 2026-09-27 (on OPUS-NOTICE-FABLE-UC3-OBJECTS-DURABLE)

The 63 yasm objects are now in `obj/` beside this record, byte-identical to `obj-manifest.sha256`. The check runs without the scratchpad: `python uc3_bytematch_check.py obj` (BAD 0, null 0.00).
