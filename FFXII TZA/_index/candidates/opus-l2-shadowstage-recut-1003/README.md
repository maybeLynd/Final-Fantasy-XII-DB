# The shadow constant stage declared, and five scene settings named (OPUS, 2026-10-03)

*repos-91, a local helper, surveyed the undeclared statics around the scene constant block. OPUS checked every cited
code address as an instruction start: 208 in the new type and the rest in the re-cuts, none bad. Two appliers:
[`apply_recuts.py`](apply_recuts.py) re-cuts 7 rows into 8 from [`recuts.json`](recuts.json), and
[`apply_newtype.py`](apply_newtype.py) declares the new type from [`research.json`](research.json) `new_type`.*

## New type: ShadowConstantsStage02CB8160 (0x2C0, OPUS)

This is the stretch between CharacterLightingTuningBank (`02CB80A0`, 0xC0, ending at `02CB8160`) and
SssLightingParams02CB8420, which no type declared. It is the shadow part of the scene-wide constant block
`02CB7FD0..02CB843C`: `006084B0` copies the block in a single 704-byte call. The update-shadowmap scope body
`001F0AD0` of the render pass `00187950` fills it from ShadowSettings, the pointer `001F0850()` returns. The
declaration has 30 field rows and no overlaps, ending exactly at 0x2C0. Among them:
- `+0x000 shadowMatrices`: the eight shadow-map matrices, where entry n is ShadowSettings `+0x1C0 + n*0xD8`;
- `+0x220 lightDirection`: a staged copy of ShadowSettings `+0xFC`;
- `+0x200`: a 32-byte copy of the unnamed source span `+0x850..+0x86F`, whose meaning is not claimed.

## Re-cuts (OPUS)

- **ShadowSettings01F82EA8 `+0xF0`/`+0xF4`** become `shadowValueG` and `shadowValueB`. Both loaders store these keys
  beside ShadowValueR at `+0xEC`, and `001F0AD0` stages all three.
- **PostProcessParamContext `+0x170..+0x17B`** was one f32[2] row and one f32 row. It becomes three rows,
  `colorR`/`colorG`/`colorB`, each holding the scene setting minus 0.5: the loader subtracts 0.5 before storing.
- **PostProcessParamContext `+0x334`/`+0x338`/`+0x33C`** were named after their constructor defaults (0.25, 1.0,
  0.25). They become `nearRatio`, `farRatio` and `blurFactor`. Both loaders write these keys through the cell
  `01F81300`. The defaults stay true when no scene sets a key.

## Noted, not applied (OPUS)

- PostProcessParamContext `+0x17C contrastR`: the loader stores mContrastR minus 0.5 too (`001C7D4C subss xmm0,
  xmm6`), and the row does not say so. This is a follow-up.
- SssLightingParams02CB8420 `+0x0..+0x8`: `001F08A0` normalises a direction and publishes it there, as the
  weather-apply page describes. That is not re-cut here.
