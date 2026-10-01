# W-5 — the `Inverted` render passes draw nothing in this build

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC and DATA. Nothing was executed.**
Control: `w5_inverted.py` (6 checks, FAILS 0; V6 needs the local extract at `D:/FFXII_TZA_extract`).

**Answer.** The five `Inverted` names are variants inside PhyreEngine's stock post-effect classes. Each class picks
its variant when the render target it is given carries bit 1 of the dword at `+0xC`. In FFXII none of them can draw:
- four of the five classes have no construction path in the game;
- the fifth, FXAA, loads an effect file with no `Inverted` technique.

They are not a water-reflection pass. The row's guess is refuted for this build.

## What the code shows

- **V1 — one reader each.** A raw rip-displacement sweep of `.text` finds exactly three readers for each name object:
  - its start-up initializer, which passes the literal text;
  - its atexit stub;
  - one selector.

  | name object | text | selector |
  |---|---|---|
  | `02D37A60` | `CelInverted` | `006587F0` |
  | `02D38000` | `MaterialPostEffectInverted` | `00659A90` |
  | `02D37FC0` | `RenderAtmosphereInverted` | `00658470` |
  | `02D376A0` | `RenderCameraMotionBlurInverted` | `00659C20` |
  | `02D37860` | `RenderFXAAInverted` | `0065A640` |

- **V2 — one test.** All five selectors test the same bit of the target-descriptor argument: bit 1 of its dword
  `+0xC`. The test sites are `0065871B`, `00658ABF`, `00659B48`, `00659DE4` and `0065A888`.
  This corrects my 2026-09-17 narrowing, which said the FXAA and motion-blur selectors branch on something else.
- **V3 — five library classes.** Each selector's caller is slot 6 of one class's vtable, named from its RTTI
  complete-object locator:

  | class | vtable | slot 6 |
  |---|---|---|
  | `Phyre::PPostProcessing::PAtmospherics` | `00D628A0` | `0065B270` |
  | `PCelShading` | `00D627B0` | `0065B340` |
  | `PMaterialPostEffect` | `00D62940` | `0065B750` |
  | `PMotionBlur` | `00D62170` | `0065B820` |
  | `PFXAA` | `00D625D0` | `0065B590` |

- **V4 — only FXAA is built by the game.**
  - PFXAA's vtable is written by `00645DB0`, which game code calls at `0018CFD5`, and game code also calls the
    FXAA selector directly (`0065A630`, from `0018FD70` and `00191DA0`).
  - For each of the other four classes, one function writes the vtable. That function has no rel32 caller and
    exactly one pointer to it, its reflection class descriptor.
  - Those classes could therefore be built only by a descriptor lookup, which is driven by data naming the class.
- **V5 — no effect files for the four.** The image names 13 `.fx.phyre` effect files. None is an atmosphere, cel,
  material-post-effect or motion-blur effect. `PhyreFXAA.fx.phyre` is one of the 13.

## What the shipped data shows

- **V6 — no Inverted technique.** `PhyreFXAA.fx.phyre` carries the techniques `RenderFXAA` and `RenderRGBL` only.
  None of the 99 files in `gamedata/d3d11/artdata/shaders` contains the string `Inverted`. The positive control
  `RenderFXAA` is found in exactly that one file.
- **The whole extract (one-off scan, not in the control).** A byte search of every file under
  `D:/FFXII_TZA_extract` (89,414 files, 58,894,815,547 bytes, all nine language copies) finds zero files containing
  any of these strings:
  - `Inverted`;
  - the class names `PAtmospherics`, `PCelShading`, `PMaterialPostEffect`, `PMotionBlur`, `PFXAA`,
    `PPostEffectBase`, `PDepthOfField`;
  - the technique stems `RenderAtmosphere`, `MaterialPostEffect`, `RenderCameraMotionBlur`.

  No shipped asset asks the reflection system for the four unbuilt classes. And no shipped effect has an `Inverted`
  technique to draw, for FXAA or anything else.

## What this does not claim

- **What bit 1 means to PhyreEngine** (for example a vertically flipped target). The image only tests the bit, so
  this record does not name it.
- **What FXAA does if a target ever carries the bit.** It would store the name of a technique its effect lacks.
  Whether that pass then skips or fails is not read here.
- **Anything live.**
