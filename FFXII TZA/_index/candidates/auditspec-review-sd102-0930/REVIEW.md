# SWE2-AUDIT-SPEC review of SD-102 (sd102-glyph-emitter-commands-0930 at d1f7f06ac): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS.
Reviewed: `d1f7f06ac`, [the record](../sd102-glyph-emitter-commands-0930/README.md) and `sd102_emitters.py`.
Static, the certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD102-0930 | [sd102-glyph-emitter-commands-0930](../sd102-glyph-emitter-commands-0930/README.md) | `d1f7f06ac` | ACCEPT-WITH-NARROWING |

**Re-run.** `sd102_emitters.py` at HEAD: E1-E7 PASS, `FAILS 0`; the output is identical to the committed `.out`
ignoring CR ([rerun_sd102_emitters.out](rerun_sd102_emitters.out)).

**Re-derived independently: the packet decode HOLDS** ([sd102_review.py](sd102_review.py), [sd102_review.out](sd102_review.out)).
I decoded every immediate in `002DAF30`, `002DAC70` and `002DD350` by the PS2 field layout, not by the pinned
instruction text.
- **GIF tag (`002DB020`).** `0xD000400000000001` is NLOOP 1, EOP 0, PRE 1, FLG 0 (PACKED) and NREG 13.
- **REGS (`002DB034`).** `0x431431431431E` is A+D, then (RGBAQ, UV, XYZF2) four times.
- **PRIM (`002DB004` / `002DB00C`).** `0x15C` is TRISTRIP with IIP 1, TME 1, ABE 1 and FST 1. `0x154` is the same
  with IIP 0.
- **VIF codes.** `002DAD1A` is FLUSHE. `002DAD21` `0x6c068100` is UNPACK V4-32, NUM 6, ADDR 0x100, FLG 1. `002DACAC`
  ORs UNPACK V4-32 with FLG 1 onto the computed NUM. `002DD35D` is MSCAL.
- **The A+D tag (`002DAD31`).** `0x1000000000000005` is NLOOP 5, NREG 1.

E1-E7 are right as decodes.

**Where the kick goes.** The record says a sealed chunk is "sealed and kicked (`0016D6A0`, `003A1DB0`)".
- `0016D6A0` is the 3-byte `ret 0` stub (`_guard_check_icall`), so it does nothing here.
- `003A1DB0` (`RenderCommand_SubmitCurrentBufferAndSwap`) flips the ring index `02EBEFF0`. It then calls `0036F360`,
  which ends the buffer with a FLUSHE record (`0036F395`) and then stores its address and count into the folded
  cell `02EBA3F8` (`0036F3A6`, `0036F3AC`).

A rip-relative census of the ring and of the cell ([sd102_consumers.py](sd102_consumers.py),
[sd102_consumers.out](sd102_consumers.out)) found:
- **The ring.** 73 references in 36 functions. They include this emitter (`002DAF49`) and the kick, which is the
  positive control.
- **The cell.** 64 references in 19 functions. The sampled readers are same-cell spin compares, for example
  `0022B2C0` / `0022B2C6` / `cmp` / `jne`. No reader takes the buffer address.

This is the chain [the-vif1-vu1-layer.md §2.7](../../../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md)
already documents for the 2D layer ("described twice, drawn once"): its step 3 kick "hands the buffer to nothing".

**The narrowing.** The record's **For modding** paragraph says every glyph is "drawn twice over, as a legacy PS2
packet for the emulated VU1 path and as ... draw calls on the PC draw context", so "a text colour or blend change has
to reach both". That contradicts §2.7. The packet is *described* twice but *drawn* once, on the draw context. The
decode findings E1-E7 are unaffected.

**Controls.** E1-E7 compare pinned instruction text at fixed addresses. They catch a changed image but cannot catch a
misreading of the fields. My field decode above is the check for that. Nothing in the checker tests the modding
sentence.

**A side note that agrees with the record.** §2.7 step 1 names `+0x5A` a brightness word and `+0x58` an alpha word, on
a scale where 0x80 is one. This supports the record's cautious reading of the four ints (`+0x5A` three times, then
`+0x58`) as a colour.

**Correction wording for the row owner (SWE2-DATA)**, for SD-102's answer and the record's modding line:

> The glyph emitters `002DAF30` / `002DAC70` build a PS2 VIF/GIF packet (decoded in sd102) on the shared packet ring
> `02EBEFC0`. Its kick, `003A1DB0` → `0036F360`, only publishes to the folded cell `02EBA3F8`, and the packet has no
> consumer (the-vif1-vu1-layer.md §2.7). What reaches the screen is the same state and quad sent to the draw context
> `[01F811E8]`. A text colour or blend mod needs only that path.
