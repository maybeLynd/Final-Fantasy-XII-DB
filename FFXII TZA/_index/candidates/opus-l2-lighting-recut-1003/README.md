# Scene and map lighting settings bound to their JSON keys (OPUS, 2026-10-03)

*repos-91, a local helper, matched the scene loaders' key strings to the stores they make. OPUS checked every cited
code address as an instruction start. Applied by [`apply_recuts.py`](apply_recuts.py) from [`recuts.json`](recuts.json):
10 rows out and 10 in. The research is in [`research.json`](research.json).*

## Applied (OPUS)

**MapLightingTuning02CB7FD0.** The map loader `001C7940` stores each key at its row:
- `+0x98` `waterBias` (mWaterBias);
- `+0xA0`/`+0xA4`/`+0xA8` `mapAmbientColorR/G/B` (mMapAmbientColorR/G/B);
- `+0xB0` `mapAmbientColorCutPercent`, which the console body `001D1660` also reads and writes.

Every one of these is now a float, where the census had uint32. The block is copied as a whole, so most have no
direct reader.

**SceneLightingParams01F82ED0.** Both loaders, `001C3D50` and `001C7940`, store:
- `+0x24` `chrShadowSlopeOffset`;
- `+0x28`/`+0x2C`/`+0x30` `mapChrDirLightColorIntensityR/G/B`. The rows keep their 2026-09-26 names and gain what
  the renderer does with them: they scale each character's directional light.
- `+0x38` `chrShadowDepthBias`. This becomes int32, because both loaders read it as an integer. The renderer
  `001F5D70` converts it.
