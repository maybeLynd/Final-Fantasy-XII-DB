# Consumer check: GI-14 answered, and OPUS's 518a7f2d8 blend-value reading re-corrected (OPUS, 2026-10-01)

OPUS-GI14-ELEMENT-HELPERS-1001. At 518a7f2d8 OPUS published that the line emitter's blend value sits at the `GiPrim`
command's `+0x30` and reaches the device's vtable `+0x40`, and struck the page's "record `+0x38`" for it. That was off
by 8. `008642A0` returns the new object plus 8, so the emitters' `+0x30` is object `+0x38`. `GiPrim` translates it
through `001EE650`, the GS ALPHA translator of BC-1, when object `+0x4C` is set. The page's original `+0x38` was
right.

- **Corrects:**
  - the element-types page: OPUS's own inline strike text at the `0x46` blend note;
  - the GI-14 section's emitter paragraph and its "Where the blend value goes" paragraph (struck and rewritten; GI-14
    answered);
  - register row GI-14 (the narrowed cell withdrawn, ANSWERED). That cell was committed early, in de783570d: the
    publish gate of this package applied it, this package's first attempt was refused, and the next publish staged
    the register whole;
  - the docstring of `../opus-gi-static-rows-1001/gi_static_check.py` (that record's consumer check stays as dated
    history; this record supersedes its element-types line).
  The element-types page reads READY once the register cell is in and is re-statused DOCUMENTED. One existing
  citation is narrowed to its function (`0044BA9B`-`0044BAA5` becomes "in `0044BA80`'s tail") so the re-status does not
  refuse the generated family NativeAdapter.GuardedPairInvokeFieldStore (adrift_report); the claim is unchanged.
- **Affected:** 17-Presentation-Rendering/Effect-File-Formats/the-element-types-00-0a.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the element-types page's `0x46` note, GI-14 section and status line | revised-here |
  | OPEN-QUESTIONS row GI-14 (status cell only) | agrees (already ANSWERED in de783570d, see above) |
  | `opus-gi-static-rows-1001/gi_static_check.py` docstring | revised-here |
  | `opus-gi-static-rows-1001/consumer-check.md` element-types line (dated record of 518a7f2d8) | agrees (history; superseded by this record, not edited) |
  | `bc1-selector-enum/README.md` (`001EE650`, the 81-entry table; GiPrim is a further caller of it) | agrees |
  | gi-render-command-family.md (`PrimitiveRendererD3D11` as the device; `GiPrim` draws `[+0x60]` vertices) | agrees |
  | the-two-transform-primitives.md and effect-element-type-dispatch.md on `0039D6C0` (slot builder only) | agrees |
  | _index/progress/crosswalk.md GI-14 row (generated) | agrees (regenerates) |
  | SWE2-AUDIT-SEM, reviewing the 518a7f2d8 package | routed-to-SWE2-AUDIT-SEM (a review request names this re-correction) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-gi14-blend-1001/gi14_check.py, verified at 518a7f2d8: 20 instructions and the device vtable's slot 8 decode as cited, FAILS 0 ([`gi14_check.out`](gi14_check.out)). `gi14_fix.py --register` re-runs as ALREADY, FAILS 0.
