# SWE2-AUDIT-SPEC review of SD-106 (sd106-measure-sites-0930, OPUS, 349fc1359): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `349fc1359` (the record's only commit), [README](../sd106-measure-sites-0930/README.md) and `sd106_sites.py`,
measured at HEAD `b58c633f7`. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD106-0930 | sd106-measure-sites-0930 | `349fc1359` | ACCEPT-WITH-NARROWING |

**Re-run.** [rerun_sd106_sites_b58c633f7.out](rerun_sd106_sites_b58c633f7.out) is identical to the committed `.out` (CR
ignored), M1-M5 PASS, `FAILS 0`. The earlier worker's [rerun_sd106_sites.out](rerun_sd106_sites.out) was identical too.
Package dir clean after re-run: yes.

**Re-derived independently** (lane `b8dis.py` and `ov31_indep.py` helpers; [sd106_callers.py](sd106_callers.py) /
[.out](sd106_callers.out), [sites_dis_a.out](sites_dis_a.out), [sites_dis_b.out](sites_dis_b.out),
[b32d0_dis.out](b32d0_dis.out), [c480_dis.out](c480_dis.out)).
- **Five sites, and only five.** `002B3280` has 5 rel32 sites (`00227FE3 00241DEB 0057C1E2 0057C58B 0057C5DB`, all
  `call`), 0 jcc, no abs64, no rip-relative or image-base-relative reference, and one rva32, which is its own `.pdata`
  entry. The control `002B32D0` returns its two known sites (`002B32B6` call, `002B32C0` jmp), matching the raw
  index. The sibling thunk `002B32C0` has 4 callers of its own (`002A3483 002A6B1C 002A6D3C 002A6DE9`). SD-106 does
  not ask about them.
- **The wrapper's contract is conditional.** `002B3280` passes its 5th-7th arguments through and adds two zeros
  (`002B3284`..`002B32B6`). `002B32D0` branches on `r9d` (`002B3350 test ebp, ebp`):
  - `r9d` ≠ 0: it builds through `002B3C30` and writes `*arg5 = +0x94 + 8` and `*arg6 = +0x96`
    (`002B3363`..`002B3380`). The pointers are outputs, width then height.
  - `r9d` = 0: it builds through `002B3D50` and **reads** `+0x94 = *arg5`, `+0x96 = *arg6` (`002B3389`..`002B33AA`). The
    pointers are inputs.

  All five sites pass `r9d` = 1: `00227FD1 mov r9d, 1`, `00241DE7 lea r9d, [r14+1]` (with `r14d` = 0 at `00241DC3`),
  `0057C1B1 mov r9d, 1`, and `0057C581` / `0057C5CA mov r9d, r15d` with `r15d` = 1 from `0057C4E0` (`r14d` = 0 at
  `0057C4CD`). So "hands back its measured width and height" holds at these five sites. It is not what `002B3280`
  does in general.
- **M2.** The centring reads `[01E0C1D8]` - `[rsp+0x50]` (arg5 = width) and `[01E0C1DC]` - `[rsp+0x58]` (arg6 =
  height), each halved (`00227FF6`..`00228020`). These cells are the UI canvas size. Statically they are 512 and 448,
  and `0024B120` sets them to 0x780 x 0x438 or 0x200 x 0x1C0 (`0024B124`..`0024B143`). "Centred on screen" means
  centred on that canvas.
- **M3.** `[01E0C0D4]` = 96, the minimum width (`00241DFE`..`00241E0E`). The caption buffer `+0x1B0` is filled first by
  `00254F30(+0x1B0, [[arg+8]], 0x200)` (`00241D92`..`00241DA6`), and gets byte 4 when empty.
- **M4.** `[01E0CDC0]` = 16. The choice string is `002F9860(id)`, stored at `+0x5B0 + 16·i` (`0057C18B`..`0057C197`).
  The id word, flag and count are as stated. The add is refused when the count is already 8 (`0057C175 cmp al, 8` /
  `jae`). The new width is max(w + 32, the list widget's `+0x9C` through `[+0xC0]`, the dialog's `+0x9C`)
  (`0057C207`..`0057C22B`). It is written into the list widget together with height = count x `[01E0C0D0]`
  (`0057C22F`..`0057C261`). "Against the rows' widths" is therefore the widest line so far, kept in those two width
  words.
- **M5 describes the paths wrongly.** In `0057C480`'s message arm (`0057C4BF`), `+0x630` = the argument's `+0x20`.
  - If the argument's caption pointer `[r13]` is non-null, it is copied to `+0x1B0` (`0057C4FB`, `0057C501`,
    `00254F30`, 0x400 bytes).
  - If `+0x630` bit 0x20 is **set**, the caption goes through `002B3400` and then `002B3050` (`0057C516`..`0057C556`),
    and the arm jumps to `0057C5FA` **without** calling `002B3280`.
  - If the bit is **clear** (`0057C514 je 0057C568`), the caption is measured at `0057C58B`.
  - If the pointer is **null** (`0057C4F5 je 0057C5A6`), `00861EC0(+0x1B0, 0, 0x400)` clears the buffer. `00861EC0` is a
    thunk to IAT `008C2A60` = VCRUNTIME140 `memset`, `rcx` is `+0x1B0` from `0057C4C6`, and `rdx` is the null pointer.
    The empty caption is then measured at `0057C5DB`, **and the measurement is thrown away**: `0057C5EE`..`0057C607`
    sets height `[rbp+0x50]` = 0 and width `[rbp+0x58]` = 2 x `[01E0CDC0]`.
  - Every path then raises the width to the literal 0x60 (`0057C5FD`..`0057C607`).

  So the README's "after `002B3400` initialises the element on it" names the path that does not reach `002B3280`. The
  checker's M5 tests that `0057C519` / `0057C520` exist. That is a citation of the neighbouring branch: the line is
  present, but it does not support the sentence.

**Controls.**
- The caller sweep's defect would be missing an indirect caller. `002B32D0`'s known jmp site must appear, and it does.
  The same scan type returns `002432B0`'s 113 sites in the SD-2 review.
- The in/out reading's defect would be an output misread as an input. The `r9d` = 0 arm's loads through the pointers
  (`002B3393 movzx eax, word [rax]`) are the positive evidence that the direction flips.

**Citations checked.** M1-M4's instruction lines support their sentences. M5 does not; see above. The layout keys
listed per caller were not re-read. They cite the owning pages.

**Runtime routing.** None. Static.

**Correction wording (the producer applies).**
1. "The answer", first sentence: *"`002B3280` builds a kind-0 element on a text and, called with `r9d` ≠ 0 (as all five
   sites call it), hands back its measured width (`+0x94` + 8) and height (`+0x96`). With `r9d` = 0 it builds through
   `002B3D50` and takes the element's size from the same two pointers instead."*
2. The `0057C58B`, `0057C5DB` row: *"**the confirm caption** again (`+0x1B0`, element `+0xE0`), on two of the message
   arm's three paths. `0057C58B` measures the caption copied from the argument when `+0x630` bit 0x20 is clear (with
   the bit set the caption goes through `002B3400` / `002B3050` and `002B3280` is not called). `0057C5DB` runs when the
   argument has no caption: the buffer is cleared by `memset` (`00861EC0`, 0x400 bytes), and the measured size is
   discarded for height 0 and width 2 x `[01E0CDC0]`. On every path the width is then raised to 0x60."* The "what the
   size is for" cell: *"the dialog's caption width and height, `[rbp+0x58]` / `[rbp+0x50]` (M5)"*.
3. The M2 row: *"centred on the UI canvas `[01E0C1D8]` x `[01E0C1DC]` (512 x 448, or 1920 x 1080 when `0024B120` selects
   it)"*.
4. The checker's M5 comment: drop "after the element is initialised by `002B3400` on the caption". The check itself may
   stay, since the lines exist.
