# Consumer check: falsification pass 1 on CONTRACT-text-control-codes-and-dyngeo-draw (OPUS, 2026-09-29)

corrects: 16-UI/CONTRACT-text-control-codes-and-dyngeo-draw.md (I-1 and §2's "seven callers, one shape"; §7's and §10.1's out-of-range escape; §12's caller comment)
corrects: 16-UI/Text-And-Number-Rendering/the-text-control-code-language.md (§5 modding note: unknown selectors, inside and outside the range)

## What was corrected

- **The seven callers are not one shape.** Five loop on the return with `test eax, eax / je` (`002A9726`, `002AA6A8`,
  `002AB5B0`, `002AF783`, `002B2393`). Two are single-shot length probes: `002B1FB0` at `002B207E` and `002B5730` at
  `002B5823` never test `eax` and read the cursor delta (`[rsp+0x28] − start`).
- **The out-of-range escape.** Only the `0x0F` is consumed; the selector is printed by the next call. This is FABLE's
  2026-09-25 I-6 correction, which §7, §10.1 and the language page's modding note had not received. The do-nothing
  selectors inside the range behave the same way (I-3).

## Current consumers

- consumer: [the-text-control-code-language.md](../../../16-UI/Text-And-Number-Rendering/the-text-control-code-language.md): revised-here. Its §5 modding note carried both stale readings of the escape. Its §3 caller table lists sites only and agrees.
- consumer: `_index/L2-VERDICTS.md` S-37 agrees. It counts seven callers and asserts no shape.
- consumer: [the-text-element-dispatch-table.md](../../../99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md) agrees. It names `002A8C50` as one of the seven, a looper.
- consumer: `_index/COVERAGE.md` and `_index/AUDIT-LOG.md` agree. Both record the caller count, not a shape.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_text_control_codes.py`, checks T0-T16:
- T1 fails if the five/two split changes;
- T16 fails if a cursor write appears on the out-of-range path.

run: verified at 62c566676 (BROKEN 0), against the certified image `73461d08…`.
