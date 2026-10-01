# Consumer check: falsification pass 1 on CONTRACT-developer-tuning-console (OPUS, 2026-09-29)

corrects: 00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md (§3's and §5's per-callee "arms", §10.5's "110 arms carry both addss and subss"; I-2 sharpened)

## What was corrected

- **The per-callee figures are call sites, not arms.** 45 / 33 / 13 / 10 / 9 are exact as call sites in
  `001D1660`. The arms that reach `001A9930`, `00193D50`, `001DF340`, `001DDAB0` and `001C2F40`, following each arm's
  control flow, are 14 / 16 / 15 / 2 / 4.
  - Slice D §5.2 found the first two (14, 16) independently and earlier.
  - The AUDIT-LOG recorded the error shape, but the correction never reached the primary page or this contract.
- **§10.5:** 110 arms reach `addss`, and 59 of them also reach `subss`.
- **I-2, sharpened:** the out-of-range exit enters the shared epilogue at `001D4C09`, after the `xmm6`, `xmm7` and
  `rbp` restores, which it never saved. The 56 shared ids enter at `001D4BFA`.

## Current consumers

- consumer: [the-282-command-parameter-console.md](../../../00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md): revised-here. Its helper table and address table carried "N arms"; now struck, with call sites and arms written.
- consumer: [the-post-process-passes-and-their-shader-constants.md](../../../22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md): revised-here. "the developer console's 33 arms" now reads 16 arms at 33 call sites.
- consumer: [arm-catalogue-slice-D-ids-108-139.md](../../../00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-D-ids-108-139.md) agrees. §5.2 is the source of the correction; it quotes the old rule in order to refute it.
- consumer: [numeric-formatting-and-character-mapping.md](../../../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md) agrees. It cites "45 call sites read as 45 arms" as an error shape.
- consumer: `_index/AUDIT-LOG.md` agrees. It records the same error shape.
- consumer: [s06-opus-replay-console-arms](../s06-opus-replay-console-arms/README.md) agrees. It quotes the "33 arms" relationship as history, and its per-arm write scopes are measured per arm.
- consumer: `CONTRACT-ppfx-effect-creation.md` agrees. It cites this contract only for the PostProcessParamContext distinction.

## Regression

regression: [`falsify_developer_tuning_console.py`](../../../../Tools/analysis-kit/gfz-scripts/falsify_developer_tuning_console.py),
at `Database/Tools/analysis-kit/gfz-scripts/falsify_developer_tuning_console.py`, checks D0-D11:
- D8 fails if the call-site figures stop matching;
- D10 fails if the 110 / 59 split changes;
- D2 fails if the out-of-range entry moves.

run: verified at 0dd72898c (BROKEN 0), against the certified image `73461d08…`.
