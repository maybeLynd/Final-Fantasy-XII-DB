# SD-105: the reveal's three inputs are set from the lag bound and the nested run (OPUS, 2026-09-30)

Register row SD-105 was registered by SWE2-DATA ([the-shared-drawing-context.md](../../../99-Unresolved-Residual/Glyph-Run-Rendering/the-shared-drawing-context.md)
section 3g). It asks for three of the text reveal's inputs:
- the text block's `+0x90` default;
- the writer of the fade step `+0x50`;
- the signed word at `[rbp+0x1C]` that the progress ratio scales.

This record is static. The checker is `sd105_inputs.py` (output `sd105_inputs.out`, `FAILS 0`).

## The answer (OPUS)

- **V1: `+0x90` = −(s8)`+0x9E`.** All three builders set it: the shared wrapper `002B32D0` and the kind-0 builders
  `002B3C30` / `002B3D50`. `+0x9E` is the lag bound, which the base fill `002AC1E0` sets to 8 (UQ-173). So at rest
  `+0x90` is −8, and `002AF960` copies it into the full-opacity counter `+0x10DC`.
- **V2: `+0x50` = 1.0 / (s8)`+0x9E`.** ~~`002B32D0` writes it: 0.125 with the default bound, one lag unit per fade
  step. The message-window run builder `002A4830` copies `+0x50` wholesale from its source record.~~ Two code paths
  compute it: the wrapper `002B32D0` (`002B33F0`, after the base fill's `+0x9E` = 8, so 0.125), and the markup
  parser's `"` tag (`0F 22`) in `002A8C50`. That tag first sets `+0x9E` to its second payload byte & 0x1F
  (`003FFEE0` at `002A9456`), then stores `+0x50` (`002A947A`). At text position 0 it also sets `+0x90` =
  −(s8)`+0x9E` and `+0x9D` = 0 (`002A94B4`..`002A94C1`). Element copies (`002A4830` and others) carry `+0x50`
  across unchanged. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd105-0930/REVIEW.md) item 1)* So the fade
  fraction `+0x10E4` = (s8)`+0x9D` × `+0x50` is the lag behind the head divided by its bound.
- **V3: order.** Inside `002B32D0`, both values are set after either builder has run. Every element built through
  the wrapper therefore ends with both derived from `+0x9E`.
- **V4: `[rbp+0x1C]` is the nested element's reveal budget.**
  - ~~In the control-code engine `002AC5F0`, `[rbp−0x70]` is a text element built on the frame for a nested run (the
    argument insertion), so `[rbp+0x1C]` is that element's `+0x8C` (−0x70 + 0x8C = +0x1C).~~ `[rbp−0x70]` is a
    0xD0-byte copy of the current element `r14` (`002AD495`..`002AD52E`), made for a nested run (the argument
    insertion). So `[rbp+0x1C]` is the copy's `+0x8C`. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd105-0930/REVIEW.md) item 2)*
  - ~~`002AD569` stores `002B43C0`'s result on the nested element there. Reading that result as the nested run's count
    is an interpretation.~~ `002AD569` stores `002B43C0`'s result there. `002B43C0` lays the text out on a copy whose
    head `+0x8C` is `strlen(text)`, and returns `002AF340`'s character count (the SWE2-DATA page §4 reading). *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd105-0930/REVIEW.md) item 2)*
  - The outer run's progress ratio (`+0x10D8` over the per-call total `[rbp−0x78]`) scales it, and the smaller value
    is kept (`002AD653`–`002AD6CD`).
  - The outer counters are then saved and `+0x10D8` is replaced for the nested draw.

**In player terms:** the soft edge of the typewriter is `+0x9E` glyphs long (8). The newest glyph fades by 1/8 per
position behind the head. An inserted value (a name, a number) reveals in proportion to how far the line around it
has got, rather than all at once.

## Limits (OPUS)

- **`002B43C0`.** What it returns is read as the nested run's count, not traced.
- **Direct builder calls.** Elements built by a direct call to `002B3C30` / `002B3D50` (from `002A1B00` / `002A3250`)
  get `+0x90` but not `+0x50` there. Their `+0x50` is whatever the storage held (base fill or template), which is
  not traced. `002A1B00`'s element is a copy of the element at `r14` (`002A1B34`..`002A1BCB`), so it carries that
  element's `+0x50`. `002A3250`'s is not traced. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd105-0930/REVIEW.md) item 3)*
- ~~**Authored overrides.** Whether any authored data sets `+0x9E` to something other than 8 is not checked.~~
  **Authored overrides.** The `"` tag (`0F 22`) sets `+0x9E` per text (0-31). Whether shipped text uses it is not
  checked. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd105-0930/REVIEW.md) item 3)*
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
