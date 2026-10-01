# CON-198: the third band exit is not PFXAA's; each exit's owner asserted (OPUS, 2026-09-30)

Answers `AUDITSPEC-REQ-OPUS-B9-CON198-EXIT-ATTRIBUTION-0930`, SWE2-AUDIT-SPEC's narrowing of OPUS falsification batch 9
(`7980c8525`, `auditspec-review-opus-batch9-0929/` section 2).

## What changed (OPUS, 2026-09-30)

The page note, the P7 row and the CON-198 row said that all three exits from the post-effect family's code band are
"this PFXAA". One exit is a construction, and the other two are exception-unwind funclets. P7 now asserts each owner
from the C++ EH (FH3) unwind maps:
- **`0018CFD5` → `00645DB0`:** the construction, the PFXAA at `context + 0x378` inside `0018CD90`.
- **`008965EC`:** an unwind action of `0018CD90` (FuncInfo `008C6C28`, map `01D5574C`, three states). It does
  `mov rcx, [rdx + 0x40]` / `add rcx, 0x378` / `jmp 0018D0D0`, and `0018D0D0` jumps to `00646770`, the
  PFXAABase destructor chain.
- **`0089E870`:** the single unwind action of `006458A0`, PDeferredLightingBase's installer (map `01DACB10`). It
  goes to `00646AB0`, PPostEffectBase.

The conclusion does not change: the only construction by code is the one PFXAA.

## Consumer check (OPUS, 2026-09-30)

corrects: `22-Middleware-PhyreEngine/Post-Process-Chain/the-phyre-post-effect-class-family.md` (the CON-198 note and the
P7 row) and `_index/CONTRADICTIONS.tsv` (the CON-198 row).

- consumer `the-phyre-post-effect-class-family.md`: revised-here (note and P7 row, struck and corrected).
- consumer `_index/CONTRADICTIONS.tsv` CON-198: revised-here.
- consumer `the-post-process-passes-and-their-shader-constants.md` and the other CON-198 citations: agrees. They cite
  the construction, not the exit attribution.

Regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_posteffect_family.py`. P7 now asserts each exit's owner
through `eh_owner()`. verified at 01fec71fb (run: 01fec71fb), exit 0, P7 SURVIVES.
