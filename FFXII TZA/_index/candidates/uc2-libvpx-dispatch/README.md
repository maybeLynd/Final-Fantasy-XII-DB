# UC-2: the 63 unreferenced libvpx head blocks are dead - the image's run-time dispatch references only listed bodies (FABLE, Claude Opus 5.5, 2026-09-27)

**Question (UC-2):** "Are the 63 statically unreferenced head blocks dead, or entered by an address built at run time?"

The row already had these facts:
- No relocation, rip-relative operand or direct branch reaches a block.
- `.pdata` agrees.
- The one untested mechanism left was a computed address.

The row also named its own discriminator: *"a run-time CPU-dispatch table would reference every variant, and what is
measured is a clean split between referenced kernels and unreferenced ones."* UC-3 then identified the blocks as
libvpx v1.6.0 assembly, 159 routines.

**Answer: dead.** The image's libvpx *does* carry a run-time CPU dispatch, and this record reads it. It is libvpx's own
x86-64 rtcd:
- two `cpuid` setups fill **eight** function pointers;
- each pointer chooses between **two listed bodies**;
- every other libvpx kernel is called **directly**.

No mechanism in the image can form the address of any of the 159 routines. Each of them also has a source-level
reason never to be called by the VP8 decoder the image contains. The blocks are retained by whole-object linking of
the yasm objects.

## Evidence (`uc2_dispatch.py`, 6 checks, FAILS 0; output `uc2_dispatch.out`)

1. **The dispatch (D1–D3).**
   - `0016F080` fills `02F97500`–`02F97528` (six vp8 sub-pixel / predict pointers, each SSE2 vs SSSE3).
   - `00172580` runs `cpuid` / `xgetbv` and fills `02F974F0` / `02F974F8` (two vpx_dsp pointers, SSE2 vs AVX2 / SSSE3).
   - Each store is a `cmov` between two `lea` candidates, **16 targets**, and every one is a listed body. Five sit in
     the head window (`001260E7`, `001263AD`, `00126E10`, `00127104`, `00133B40`), and none is in a head block.
   - Across every listed body, those eight stores are the only writes to the eight cells.
2. **Everything else is direct (D4).** The ten listed libvpx kernels (UC-3's control C1) are reached by 19 `E8` calls
   from libvpx C (`00170370`, `001738B0`, `00173180`, `00177540`, `001775E0`), and by no address-taking operand.
   An rtcd build that dispatched them would call through pointers.
3. **The SAD question (D5).** The one decoder-side C file that names the unreferenced `vpx_sad16x16/8x8/4x4_sse2`
   is `vp8/common/mfqe.c`, and it names them only in the `#else` arm of `#ifdef USE_SSD`; `USE_SSD` is defined at its
   line 119. The image's MFQE block filter `0017B960` has exactly the USE_SSD shape:
   - three calls through the variance pointer `02F974F0`;
   - two calls to `0017B8A0`;
   - the two `filter_by_weight` kernels, called directly.

   Nothing calls `vpx_sad16x16_sse2` (`0012B200`; raw rel32 sweep, zero).
4. **Every unreferenced routine is explained (D6, `uc2-routine-classes.tsv`).** Classed against libvpx 1.6.0's C
   sources:

   | class | routines |
   |---|---:|
   | named only by non-decoder C (encoder, VP9, other vpx_dsp users) | 105 |
   | named by no C source | 43 |
   | MMX siblings of SSE2 kernels the image calls (x86-64's baseline picks SSE2) | 8 |
   | SADs compiled out by `mfqe.c`'s `USE_SSD` | 3 |
   | **named by the decoder's preprocessed code** | **0** |

## Evidence classes and limits

- **STATIC** (the image) against **tier-6 upstream source** (libvpx tag v1.6.0, the version the banner names).
  Nothing was executed.
- **The classification is by name occurrence in the C sources.** It explains the split; it is not what proves the
  split. The proof is the image side: no reference of any kind, and a dispatch whose sixteen targets are all listed.
- **A computed address outside these mechanisms** (arithmetic on another function's address) is not excluded by a
  static read. Nothing in libvpx builds kernel addresses that way, and the dispatch that does exist is fully read.
- The source classification regenerates when the libvpx source is present (`LIBVPX_SRC`, default
  `%TEMP%/libvpx-1.6.0`); otherwise the committed table is checked.

## Files

- `uc2_dispatch.py`, `uc2_dispatch.out` and `uc2-routine-classes.tsv`.
- `consumer-check.md`.
