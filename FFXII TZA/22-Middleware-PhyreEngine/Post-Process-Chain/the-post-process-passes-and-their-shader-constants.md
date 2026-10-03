---
system: The post-process pass family and its shader constants
category: 22-Middleware-PhyreEngine
status: AUDITED
owner_layer: CodeDomain:Phyre.PostProcess; no PrimaryOwner
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: offline disassembly of the shipping EXE with capstone; function boundaries and
    code-domain tags from the GN160 export at work/graph/functions.tsv; every shader
    parameter name and every literal read from the image, none from a decompiler comment
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-postprocess-pass-1 - the whole census reproduces blind: 65 tagged functions, 17 referencing a string, 12 of them shader parameters, 1 EASTL diagnostic and 4 three-byte decodes, 48 with none; all twelve pass addresses and all twelve body sizes match, and so does each one's set of names. The four the page calls non-strings fell out of my filter on their own because it required four printable characters, so two instruments with different rules drew the same line in the same place
  last_pass_kind: falsification
  crossref_clean: true
  reopened_count: 0
---

# The post-process pass family and its shader constants

> **Twelve functions in FFXII TZA are the game's entire post-process chain**, and each one names
> its shader constants in plain text inside the executable. Reading those names identifies every
> pass without guessing — and the values they push are literals and config fields that can be read
> exactly.

## 1. What a player sees

After the world is drawn, the game runs a series of full-screen passes over the picture before it
reaches the monitor: it darkens creases and contact points, softens the jaggies on edges, blooms
bright areas, blurs what is out of focus, warms or cools the whole image, softens the light bleeding
through skin, and draws the outline around menu text.

Two of those are worth a player's attention specifically.

**The game contains two entirely different ambient-occlusion implementations** — two different ways
of working out which corners should be darker — and they are not variants of one setting; they are
separate code with separate parameters.

**And both of them treat characters and scenery differently.** Every occlusion parameter comes in
two copies, one for characters and one for the scene, so Vaan can be shaded with a different
strength, radius and falloff from the wall he is standing against. That is a deliberate art choice
baked into the engine, and it is visible: character contact shadows in FFXII do not match the
scenery's.

## 2. The twelve passes

All 65 functions tagged `Phyre.Rendering.NativeQualified` were disassembled and every RIP-relative
`lea` target decoded. **17 reference a string at all; 12 of those reference shader-parameter names.**
The other five are not passes — one carries an `EASTL vector` diagnostic string and four
(`005DDBA0`, `005E2BC0`, `005E2C40`, `005E2C90`) point at three bytes that merely decode as text.
**The remaining 48 reference no string and were not read** (`EA-5`) *(answered: see the 2026-09-21 reading - every one of the 48 now has an identity; 2026-10-02, OPUS)*. The names identify the pass:

| address | size | pass | the constants it names |
|---|---:|---|---|
| `0018E4A0` | 2,418 B | **ambient-occlusion blur / composite** | `gAoAxis`, `gAoTex`, `gMainTex`, `gMainTexTexelSize`, `ColorBufferSampler` |
| `0018F6B0` | 567 B | **bloom / bright-pass** | `g_brightPara`, `g_BrightTex` |
| `0018F8F0` | 1,147 B | **colour grading** | `colorR`, `colorG`, `colorB`, `percent`, `gamma`, `resolution`, `apply_MainTex` — interior verified 2026-09-17 (SWE2-FRONTIER): `0018D240` ×8 name-binds first at [`0018F98B`](../../_index/ADDRESS-INDEX.md), `ColorBufferSampler`/`apply_MainTex`/`colorB` strings in-body |
| `0018FE00` | 1,105 B | **single-step edge pass** (interior read 2026-09-17, SWE2-FRONTIER: `0018D240` first at [`0018FEA6`](../../_index/ADDRESS-INDEX.md), `0060D4F0` ×6) | `ColorBuffer`, `ColorBufferSampler`, `SingleStepOffset` |
| `00190260` | 1,273 B | **font border** | `FontBorderSetting`, `FontBorderColor`, `SingleStepOffset` — interior verified 2026-09-17 (SWE2-FRONTIER): `0018D240` name-binds ×5 + `0060D4F0` ×6 + `ColorBuffer`/`ColorBufferSampler` strings, first call [`00190309`](../../_index/ADDRESS-INDEX.md) |
| `00190760` | 2,507 B | **HBAO** | `g_NumSteps`, `g_NumDir`, `g_FocalLen`, `g_HBAOResolution`, `g_RChr`, `g_AngleBiasChr`, `g_ContrastChr`, `g_RSce`, `g_AngleBiasSce`, `g_ContrastSce`, `g_fadeoutScale`, `g_maskBorder`, `tLinDepth`, `tNormal`, `projInfo`, `samNearest` |
| `00191130` | 1,066 B | **depth mask** | `MaskDepth` — interior verified 2026-09-17 (SWE2-FRONTIER): `001BC000` first at [`0019119D`](../../_index/ADDRESS-INDEX.md), `0060F6B0` ×5 + `0060B980` ×4 |
| `00191560` | 2,101 B | **depth of field** | `dofShift`, `MaskBuffer`, `ColorBuffer`, `materialColor`, `customPosition` |
| `00191E90` | 1,847 B | **scalable AO (the second implementation)** | `projScale`, `radiusChr`, `biasChr`, `intensityChr`, `radiusSce`, `biasSce`, `intensitySce`, `g_fadeoutScale`, `CS_Z_buffer`, `tNormal`, `projInfo`, `widthAO`, `heightAO` |
| `001925D0` | 2,839 B | **SMAA** | `areaTex`, `searchTex`, `edgesTex`, `blendTex`, `colorTex`, `smaa_resolution`, `SMAA_RT_METRICS`, `SMAA_THRESHOLD`, `SMAA_MAX_SEARCH_STEPS`, `SMAA_MAX_SEARCH_STEPS_DIAG`, `SMAA_CORNER_ROUNDING`, `LinearSampler`, `PointSampler` |
| `001930F0` | 2,099 B | **subsurface-scattering blur** | `sssBlur`, `useBigKernel`, `blendAmount`, `dir`, `colorTex`, `depthTex`, `normalTex`, `SingleStepOffset` |
| `001EE8E0` | 840 B | **colour-buffer copy** | `ColorBuffer`, `ColorBufferOffset`, `ColorBufferSampler` |

> **The names are the engine's own.** Nothing here is inferred from a function's neighbours or from a
> decompiler's guess: each string is a literal in `.rdata` that the function passes by address to the
> parameter lookup, and the set of names a function passes is what identifies it.

## 3. How a shader constant is written

Every one of the twelve uses the same six-step idiom. This is the whole mechanism:

```c
p = FindShaderParameter(shader, "SMAA_THRESHOLD");   /* 0018D240, 209 B */
if (p != NULL) {
    value = ...;                                     /* built on the stack */
    offset = *(u16 *)(p + 0x10);                     /* byte offset into the block */
    size   = *(u16 *)(p + 0x12) & 0x1FFF;            /* low 13 bits only */
    if (offset + size <= *(u32 *)block)              /* must fit */
        if (offset >= 4)                             /* must not overwrite the header */
            memcpy((u8 *)block + offset, &value, size);   /* 00861EBA */
}
```

**The constant block is `{ u32 declaredSize; u8 data[]; }`**, and offsets are measured from the
*start of the block*, not from the start of the data. That is why the code refuses `offset < 4`:
an offset of 0–3 would overwrite the size field it just validated against.

**The size field is masked to 13 bits** (`and dx, 0x1FFF`), so the upper three bits of
`*(u16 *)(p + 0x12)` carry something else and are discarded here. **What they carry is not read.**

**A missing parameter is silently skipped**, not an error: `0018D240` returning `NULL` jumps straight
to the next parameter. A shader that does not declare `SMAA_CORNER_ROUNDING` simply never has it
written, and nothing reports that.

## 4. SMAA — the full quality ladder, with every constant

`001925D0` reads one integer, `context + 0x184`, and derives four SMAA constants from it. **All four
ladders, complete:**

| `context+0x184` | `SMAA_THRESHOLD` | `SMAA_MAX_SEARCH_STEPS` | `SMAA_MAX_SEARCH_STEPS_DIAG` | `SMAA_CORNER_ROUNDING` |
|---:|---:|---:|---:|---:|
| ≤ 0 | 0.15 | 4 | 0 | 0 |
| 1 | 0.15 | 4 | 0 | 0 |
| 2 | 0.10 | 8 | 0 | 0 |
| 3 | 0.10 | 16 | 8 | 25 |
| 4 | **0.05** | **32** | **16** | 25 |
| ≥ 5 | 0.15 | 4 | 0 | 0 |

The exact branch shapes, so the table can be checked:

```asm
; SMAA_THRESHOLD                     ; SMAA_MAX_SEARCH_STEPS
00192975  cmp ecx,1  / je  -> 0.15   001929FA  mov edx,[rsi+0x184]
0019297A             jle -> 0.15     00192A00  sub edx,1 / je -> 4
0019297C  cmp ecx,3  / jle -> 0.10   00192A05  sub edx,1 / je -> 8
00192981  cmp ecx,4  / jne -> 0.15   00192A0A  sub edx,1 / je -> 16
00192986                     0.05    00192A0F  sub edx,1 / jne -> 4  (else 32)
```

> **These are the canonical SMAA reference presets.** The upstream SMAA header ships
> `SMAA_PRESET_LOW`/`MEDIUM`/`HIGH`/`ULTRA` with `MAX_SEARCH_STEPS` of 4/8/16/32 and thresholds
> 0.15/0.10/0.10/0.05 — **exactly the four rows above.** FFXII did not tune SMAA; it wired the
> stock presets to a quality integer. `CORNER_ROUNDING` is the one departure: upstream's LOW uses
> 100 (which disables the corner pass by saturating it), and this build uses **0** instead.

**`SMAA_RT_METRICS` is computed, not authored** — the standard SMAA render-target metrics vector:

```c
SMAA_RT_METRICS = float4( 1.0f / width, 1.0f / height, (float)width, (float)height );
```

built at `001928D5`–`00192917` from the render target's `+0x28` (width) and `+0x2C` (height), with
`1.0f` taken from `01CEBBA8`. And `smaa_resolution = float2((float)context[0x2E0], (float)context[0x2E4])`.

## 5. The two ambient-occlusion implementations

**Both take the same context object**, and both read their parameters from it — but from **two
adjacent, non-overlapping blocks**, one per implementation. That is the structural proof that they
are two systems rather than two paths through one.

### 5a. The scalable-AO block — `context + 0x1A8 … + 0x1C0`

| field | parameter | conversion applied |
|---|---|---|
| `+0x1A8` | `biasChr` | **`/ 600.0f`** |
| `+0x1AC` | `radiusChr` | direct |
| `+0x1B0` | `intensityChr` | direct |
| `+0x1B4` | `biasSce` | **`/ 600.0f`** |
| `+0x1B8` | `radiusSce` | direct |
| `+0x1BC` | `intensitySce` | direct |
| `+0x1C0` | `g_fadeoutScale` | direct |

`projScale` is the **literal `500.0f`** at `008F3140` — not a config field, not resolution-derived.

> **EA-4 answered 2026-09-12 (FABLE): both blocks are filled from the scene configuration's
> string-keyed map, through two three-float setters each, and the defaults are literals in the
> context's constructor.** The scalable-AO block has setters `001949C0(ctx, bias, radius, intensity)`
> → `+0x1A8`/`+0x1AC`/`+0x1B0` (the Chr triple) and `001949E0` → `+0x1B4`/`+0x1B8`/`+0x1BC` (Sce);
> the HBAO block has `00194330` → `+0x1C4`/`+0x1C8`/`+0x1CC` and `00194350` → `+0x1D0`/`+0x1D4`/`+0x1D8`
> — plain `movss` stores, no unit conversion, so what the map holds is what the pass later
> multiplies by π/180. Both scene-config loaders the console pages name call them: `001C3D50`
> (the preset-aware lookup `001C51D0` then `Variant_ReadFloat` `00200B50`, `001C4586`–`001C46F3`) and
> `001C7940` (`001FF740` lookup, `00200BE0` presence test, `001C8693`–`001C87DB`), reading the keys
> **`mSAOBiasChr` / `mSAORadiusChr` / `mSAOIntensityChr`, `mSAOBiasSce` / `mSAORadiusSce` /
> `mSAOIntensitySce`, `mSAOFadeoutScale`** (→ `+0x1C0`), **`mHBAOBiasChr` / `mHBAORadiusChr` /
> `mHBAOIntensityChr`, `mHBAOBiasSce` / `mHBAORadiusSce` / `mHBAOIntensitySce`, `mHBAOFadeoutScale`**
> (→ `+0x1DC`) — the fourteen `mSAO*` / `mHBAO*` strings in the image, at `008FA658`–`008FA718`. So
> "`g_ContrastChr`" is the key `mHBAOIntensityChr`, and the degree-valued bias is authored under
> `mHBAOBiasChr` in the same map that carries `mDofFocusDistance` — the per-cutscene JSON sidecar
> and the developer console (see [what the console tunes](../../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md)).
> The constructor `0018CD90` seeds the HBAO block before any map is read: bias `0x3F05E354` (0.523),
> radius 1.0, intensity 1.25 for both Chr and Sce (`0018CEE2`–`0018CF14`), fadeout 1.0, `g_NumSteps` 3,
> `g_NumDir` 8 (`0018CF1E`–`0018CF32`); `0018A380` re-seeds the same fields on another path
> (`0018A42C`–`0018A46B`). `g_NumSteps` / `g_NumDir` have no map key — they are the constructor's
> constants only.

### 5b. The HBAO block — `context + 0x1C4 … + 0x1E4`

| field | parameter | conversion applied |
|---|---|---|
| `+0x1C4` | `g_AngleBiasChr` | **`× 3.14159250f / 180.0f`** — authored in **degrees** |
| `+0x1C8` | `g_RChr` | direct |
| `+0x1CC` | `g_ContrastChr` | direct |
| `+0x1D0` | `g_AngleBiasSce` | **`× 3.14159250f / 180.0f`** — degrees |
| `+0x1D4` | `g_RSce` | direct |
| `+0x1D8` | `g_ContrastSce` | direct |
| `+0x1DC` | `g_fadeoutScale` | direct |
| `+0x1E0` | `g_NumSteps` | direct, **integer** |
| `+0x1E4` | `g_NumDir` | direct, **integer** |

The degree→radian constants are literals: `3.141592502593994f` at `008F3120` (the float32 nearest π)
and `180.0f` at `008F3138`.

```c
g_AngleBiasChr = context->angleBiasChrDegrees * 3.14159250f / 180.0f;
```

> **The angle bias is authored in degrees.** That is an artist-facing unit, not a programmer's, and
> it is the strongest single hint that these nine fields come from a tuning asset rather than from
> code.

### 5c. `Chr` and `Sce` — every parameter, twice

**Six of the seven float parameters in each block are a `Chr`/`Sce` pair.** The engine's own naming
splits **characters** from the **scene**, and only `fadeoutScale` is shared.

> **So ambient occlusion in FFXII is not one effect with one strength.** Characters and scenery get
> independent radius, bias and intensity — in both implementations, using the same split. **A modder
> raising AO strength must change both members of each pair**, or characters and world will drift
> apart visually.

**What is not established here:** which of the two implementations a given graphics setting selects,
or whether both ever run. The `GameSetting.ini` key
[`HDAO`](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)
has three values (`Off`, `HalfResolution`, `FullResolution`) and the scalable-AO pass writes
`widthAO`/`heightAO` — which is the shape a half-resolution mode would need — **but the link is not
read, and this document does not claim it.** *(answered: see the 2026-09-14 answer below - the `HDAO` setting selects the AO; 2026-10-02, OPUS)*

## 6. The other passes, with their constants

**Colour grading** (`0018F8F0`) writes `colorR`, `colorG`, `colorB` — a per-channel tint — plus
`percent` (a blend weight), `gamma`, and `resolution`. **This is the whole-screen colour treatment**,
and it is three separate scalars rather than a matrix or a LUT, so it can only scale channels, not
rotate hue.

**Bloom** (`0018F6B0`, only 567 bytes) writes just `g_brightPara` and `g_BrightTex` — the bright-pass
parameters and the texture. It is the smallest of the twelve.

**Depth of field** (`00191560`) writes `dofShift` and binds `MaskBuffer` alongside `ColorBuffer`, so
the blur is masked rather than applied uniformly. Interior read 2026-09-17 (SWE2-FRONTIER): the
2,101-B body binds six names through `0018D240` — `materialColor` and `customPosition` in addition
([`0019162C`](../../_index/ADDRESS-INDEX.md) / `00191640`), then `ColorBuffer`, `MaskBuffer`,
`ColorBufferSampler`, `dofShift` (`00191654`–`00191698`) — with `00861EBA` applies and the
`005DC190`/`00609710`/`0060D4F0`/`0060DB50`/`0060F6B0`/`0060B980` Phyre render calls around them
(of those, `0060B980` is read — a sparse render-item body: `006B6410`/`006B64F0` setup pair at
[`0060BA36`](../../_index/ADDRESS-INDEX.md), `00808F10`, `02CB6360` global, ~~`00606A20`/~~
`00606C60`/`00600B30` teardown; `00606A20` is the variant-key builder, not a teardown *(corrected 2026-10-02, OPUS: it runs each switch evaluator, `00606AB3`-`00606ADF`, then binary-searches the variant table from `00606AFB`; the context-switch page)*).

**Subsurface scattering** (`001930F0`) writes `sssBlur`, `blendAmount`, `dir` and a `useBigKernel`
switch, and binds `colorTex`, `depthTex` and `normalTex`. **`dir` plus a per-pass `SingleStepOffset`
is a separable blur** — the pass runs twice, once per axis. Interior read 2026-09-17 (SWE2-FRONTIER):
the 2,099-B body binds ten names through `0018D240` in order — `LinearSampler`, `PointSampler` (two
samplers the prose list did not name, [`00193183`](../../_index/ADDRESS-INDEX.md) / `001931B9`),
`useBigKernel`, `blendAmount`, `sssBlur`, `dir`, `SingleStepOffset`, then `colorTex`/`depthTex`/
`normalTex` (`001933E4`–`00193497`) — `00861EBA` applies between binds, `001945B0` attaches each
texture. The AO blur at `0018E4A0` has the same
shape with `gAoAxis` — interior read 2026-09-17 (SWE2-FRONTIER): the body binds `ColorBufferSampler`
([`0018E52D`](../../_index/ADDRESS-INDEX.md)), `gMainTexTexelSize` (`0018E5AD`), `gAoAxis` (`0018E68B`)
and `gMainTex` (`0018E6E4`) through the `0018D240` name-binder with `00861EBA` applies between them,
on the constant-context global `01F7E340`.

**Font border** (`00190260`) writes `FontBorderSetting` and `FontBorderColor`. **The outline around
menu text is a full-screen post-process pass**, not a property of the font renderer — which is why
it costs the same whether one word or a full menu is on screen.

## 7. Key addresses

| address | what |
|---|---|
| `0018D240` | `FindShaderParameter(shader, name)` — 209 B, returns a descriptor or `NULL` |
| `00861EBA` | `memcpy` — the constant-block write |
| `001945B0` | 296 B, called before the parameter runs in several passes; ~~**not read**~~ *(answered: see EA-6, 2026-09-12; 2026-10-02, OPUS)* |
| `008F2D58` … `008F3010` | the shader-parameter name strings, contiguous in `.rdata` |
| `008F3120` | `3.141592502593994f` |
| `008F3138` | `180.0f` |
| `008F3140` | `500.0f` — `projScale` |
| `008F3144` | `600.0f` — the scalable-AO bias divisor |
| `008F3148` | `-2.0f` — the `projInfo` reconstruction constant |
| `008F30E8`, `008C5F6C`, `008F30F4` | `0.05f`, `0.10f`, `0.15f` — the SMAA thresholds |
| `01CEBBA8` | `1.0f` |
| `006FF900` | the **`CPostEffect` member-resource populate** — 23,568 B, the largest body in the executable, and read 2026-09-17 (SWE2-FRONTIER): it is the init pass that binds every `m_p*` texture and param object, each failure arm labelled by member name through the `006DF480` diagnostic (`..\src\GPU\GPUPostEffect.cpp(%d)`) — `m_pAmbientOcclusion_NormalDepthTexture[_Reduced[Vertical]]`, `m_pAmbientOcclusion_Result_*`, `m_pAutoExposureParam[`, `m_pAutoFocusParam[`, `m_pDepthOfField`, `m_pRenderBuffer`, `m_pRenderGlare`, `m_ppFeedbackBuffer`, `m_ppTemporalAntialias_History`, `m_pMotionBlurInternalVelocityTexture`, `m_pGlareModulatorWork`, `m_pEffectColorAlphaDestinationWork`. 119 logger sites at [`006FF9AC`](../../_index/ADDRESS-INDEX.md) onward; called from `006DAA70` and `006DE950` |

### Context-object fields cited

| offset | contents |
|---|---|
| `+0x184` | the SMAA quality integer, 1–4 |
| `+0x1A8` … `+0x1C0` | the scalable-AO parameter block, 7 floats |
| `+0x1C4` … `+0x1E4` | the HBAO parameter block, 7 floats and 2 ints |
| `+0x2E0`, `+0x2E4` | render width and height |

## 7a. The render-pass registry at `02CBF998` — sixty named passes, one declared family

`02CBF998` heads a **singly linked, name-keyed intrusive registry** the passes register into at
static-init time. The contract was read off the image on both sides (OPUS, 2026-09-14; re-derived
this pass, every row of `members/render-pass-registry-60.tsv` verified):

- **Node layout** — `+0x00` `const char *name`, `+0x08` `node *next`, `+0x10` `u8` flag (written
  `0` at all 60 sites), `+0x18` `u32` written `0xFFFFFFFF` by the register shim — a slot/index
  sentinel. The 60 nodes span `01F81220`–`02E5BF68`, all past `.data`'s raw end (`01F7E400`), so
  the name field is written at run time by each static constructor — reading `node+0x00` out of
  the image yields nothing; names come from the registration sites.
- **`005DC6F0`** (45 B) — the register shim each site calls: stores `name`/`next=0`/flag byte/
  `+0x18 = -1`, then calls REGISTER.
- **`005FDCB0` REGISTER** (132 B) — name from `[rcx]`; null name returns **`0x11`**
  (`lea eax,[r10+0x11]` with `r10` zero); walks `+0x08` running an inline byte-by-byte compare
  (`r8 = r10 - rax`, `[rax]` vs `[rax+r8]`) and returns **`0x12`** on a duplicate; otherwise
  `mov [r11+8],rbx; mov [02CBF998],r11` — a front push — and returns **`0`**.
- **`005DDD60` UNREGISTER** (79 B) — `rax = head`, `r8 = &02CBF998` so the head case needs no
  special path, `r9 = rcx+8`; compares *addresses* of next fields, then `mov rcx,[rax+8];
  mov [r8],rcx; mov [rax+8],0`.

**The sixty teardown wrappers are one declared family.** Each is the identical 12-byte body
`lea rcx,[node]; jmp 005DDD60`, registered with the MSVC `atexit` wrapper `00808B90` by **tail
call** — the blind-spot spelling EVIDENCE-STANDARD 13ap describes, the same spelling that hid 36
bodies from the CFG family selector. All 60 `lea` 60 distinct nodes. The registration sites share
one shape too: `lea rdx,[name]; lea rcx,[node]; call 005DC6F0; lea rcx,[teardown];
jmp 00808B90`. Member rows: [`members/render-pass-registry-60.tsv`](members/render-pass-registry-60.tsv).

**What the names cover** — the registered set is the engine's whole named-pass vocabulary, grouped:

| family | registered names |
|---|---|
| shadows | ShadowRender, ShadowRenderWithRef, MapShadowRender |
| depth / opaque | OpaqueDepth, OpaqueGray |
| alpha & near-fade | AlphaModeRender, AlphaModeClipRender, NearFadeRender, NearFadeClipRender |
| anti-aliasing | RenderFXAA, RenderFXAAInverted |
| screen-space reflection | ScreenSpaceReflectionPrePass, RenderScreenSpaceReflection, DownsampleScreenSpaceReflectionDepth, CompositeScreenSpaceReflection |
| depth of field | RenderDoFHorizontal, RenderDoFVertical, RenderDoFComposite |
| blur | RenderGaussianBlurX, RenderGaussianBlurY, RenderGaussianBlurYComposite, RenderGaussianBlurYCompositeCombine |
| camera motion blur | RenderCameraMotionBlur, RenderCameraMotionBlurInverted |
| tiled lighting | GenerateLightingTiled, GenerateLightingInstantLightsTiled, RenderPointLight, RenderSpotLight, RenderDirectionalLight |
| atmosphere precompute | PrecomputeTransmittance, PrecomputeSingleScattering, PrecomputeMultipleScattering, PrecomputeSingleIrradiance, PrecomputeMultipleIrradiance, PrecomputeRadiance, InitialiseInscattering, RenderAtmosphere, RenderAtmosphereInverted, RenderRGBL, AddToInscatter, AddToIrradiance, CopyInscatter, CopyIrradiance |
| cel shading | Cel, CelInverted |
| glow | GenerateGlowBuffer |
| material effects | MaterialPostEffect, MaterialPostEffectInverted |
| compositing / texture / video | CompositeToScreen, CompositeToScreenTiled, RenderTextures, ResetTextures, VideoScreen |
| text rendering | RenderText_AlphaBlend, RenderText_AlphaTest, RenderText_HardEdges, RenderText_SoftEdges, RenderText_SoftEdgesAndGlow, RenderText_SoftEdgesAndOutline, RenderText_SoftEdgesAndShadow |

**What is not established here:** the node carries **no function pointer** — this registry is
name-keyed bookkeeping (pass ordering / lookup), not the pass dispatch itself; where each named
pass's body enters the frame is a separate question the constants sections above partially answer
for the twelve biggest.

## 8. Modding notes

- **To change an effect's strength, change the context field, not the shader.** Every value in
  section 5 is read from the context object each time the pass runs, so a hook on the pass entry that
  edits those offsets changes the effect with no shader replacement.
- **AO parameters must be changed in pairs.** `Chr` and `Sce` are independent; editing one leaves
  characters and scenery mismatched.
- **The angle bias is in degrees**, so a plausible edit is a small number like `10.0`, not a radian
  fraction.
- **A shader that does not declare a parameter is not an error.** Adding a constant to a replacement
  shader is not enough on its own — the *name* must match one the pass already looks up, because the
  engine writes only names it has hard-coded.
- **SMAA is stock.** Anyone who knows the reference SMAA presets already knows this build's
  behaviour; the only departure is `CORNER_ROUNDING` at quality ≤ 2, which is `0` here and `100`
  upstream.
- **`projScale = 500.0f` is a literal.** A resolution change does not rescale it, which is worth
  knowing when the scalable-AO pass looks wrong at an unusual resolution.

## 9. What is not known

- [x] **Which graphics setting selects which AO implementation**, and whether both can run in one
  frame. The two parameter blocks are adjacent and disjoint, which proves they are separate systems,
  **but nothing here reads the selector.** `EA-1`.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (EA-1):* **the `HDAO` setting turns AO off or
  on and picks its resolution; which implementation runs is a context field the shipped build fixes to HBAO. The two never
  run in one frame.** The dispatcher is `0018F510`, which calls both passes:
  - **The setting.** It reads `HDAO` from the settings object `[01F82D20] + 0x28`
    ([game settings](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)): 0 `Off`,
    1 `HalfResolution`, 2 `FullResolution`. Value 1 or 2 enables AO, and 2 also sets the full-resolution flag `r8b`
    (`0018F59C`–`0018F5C4`).
  - **The gate and the choice.** With AO enabled and the context's enable byte `+0x198` set, it compares the context
    dword **`+0x344` with 1: equal → HBAO `00190760`, otherwise → the scalable pass `00191E90`** (`0018F5DB`–`0018F666`).
    It is an `if`/`else`, so at most one AO pass runs per call.
  - **Resolution on the HBAO path.** The output targets default to `+0x280`/`+0x288`. When `+0x1E8` is clear and the
    flag is not full, they are replaced by the half-size pair `+0x2A0`/`+0x2A8` (`0018F5E9`–`0018F60C`).
  - **Why HBAO is fixed.** The context's constructor `0018CD90` stores **`+0x344 = 1`** (`0018CFBD`) and `+0x198 = 1`
    (`0018CE7D`). An image-wide census of every `+0x344` displacement found no other store to this object: the
    remaining writers are other structures, such as the renderer's `0x338`-stride pair at `001894E4` and the float
    array at `001A9D7C`. **In the shipped build the scalable pass `00191E90` is reached only if something writes
    `+0x344` through a computed offset**, a route this census cannot see. Interior read 2026-09-17
    (SWE2-FRONTIER): the 1,847-B body binds all thirteen listed constants through `0018D240` in
    table order — `g_fadeoutScale` first at [`00191F1E`](../../_index/ADDRESS-INDEX.md), then
    `projScale`, `radiusChr`, `biasChr`, `radiusSce`, `biasSce`, `intensityChr`, `intensitySce`,
    `tNormal`, `CS_Z_buffer`, `projInfo`, `widthAO`, `heightAO` — each followed by a `00861EBA`
    apply, textures attached by `001945B0`.
- [x] **EA-2.** **What the context object is** — the type that carries `+0x184`, the two AO blocks and the *(NO ADMISSIBLE SOURCE, reviewed and signed 2026-09-26 by OPUS; see the register row EA-2.)*
  render size. Every pass takes it as argument one; **its class was not recovered.** `EA-2`.
  *Narrowed 2026-09-14 (FABLE):* **it is the lazily built `0x4A8`-byte parameter singleton at `01F7F5F0`**, the same object
  the developer console's ~~33 arms~~ 16 arms reach, at 33 call sites *(corrected 2026-09-29, OPUS: the 33 counted call sites)*
  ([the 282-command parameter console](../../00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md)).
  - **How the passes get it.** Each pass's caller fetches it from `00193D50` and passes it as argument one:
    `001F3106` → `0018FE00`, and `00191DEB` → `001925D0`. `00193D50` allocates `0x4A8` bytes on first use and constructs
    them with `0018CD90`, which begins by calling the base constructor `00633040` (a self-linked list at `+0x88`, and
    `+0x98` = 0) and **installs no vtable**, so RTTI cannot name it.
  - **Defaults** from the constructor: SMAA quality `+0x184 = 3`, AO enable `+0x198 = 1`, AO implementation
    `+0x344 = 1`.
  - **The class name is still open.** *(answered: see the 2026-09-22 reading - not recoverable from this image by any route this database uses; 2026-10-02, OPUS)* The reflection-schema route this row proposes remains the way to get it.
  - **Declared 2026-09-17 (SWE2-STRUCT):** the object is in the type store as `PostProcessParamContext`
    (size `0x4A8`, `PTR 0x01F7F5F0`/`0x01F81300`, ctor `0018CD90`) with a 145-row field map and the
    cross-call census `postprocess-context-accesses.tsv`. Naming stayed honest — the outer object has no
    vtable, so `PostProcessParamContext` is a database name, not the class name.
- [x] **EA-3.** **The upper 3 bits of the parameter descriptor's size word** at `+0x12`, discarded by the
  `& 0x1FFF` mask. `EA-3`.
  *Narrowed 2026-09-14 (FABLE), not answered: no code path through the parameter lookup reads them, and nothing in `.text`
  writes them.*
  - **Consumers.** Every `movzx …, word [descriptor + 0x12]` in the 37 callers of `FindShaderParameter` `0018D240` and in
    the writer `001945B0` was disassembled: **110 reads, all masked with `0x1FFF`** before use.
    - **3** of the 110 masks are an immediate `and` (`001E3FAE`, `001E6347`, `005C1243`). The other **107** `and` with a
      register loaded with `0x1FFF`, often well before the read (for example `mov r15d, 0x1fff` at `00190883` in
      `00190760`, and `mov eax, 0x1fff` at `00194669`). How many loads count as hoisted depends on the definition, so no
      count is given: two censuses disagreed (`pub140-scratch/tools/ea3_mask_census.py`). *(Corrected 2026-09-14 after
      AUDITSEM-CONTRA-FABLE-EA3-29: the earlier "29 cases hoisted" did not reproduce.)*
    - The callers include the twelve passes, the character render method `001F7790` (15 reads) and the Phyre-side writers
      `0060E670`, `00654B00`, `00654FE0`, `006561D0` and `0067C440`. (`006561D0` interior read 2026-09-17, SWE2-FRONTIER: 1,273 B — `0018D240` ×37 name-binds incl. `"Asymmetry"`/`"BetaM"`/`"BetaR"`, first at [`00656229`](../../_index/ADDRESS-INDEX.md))
  - **Producers.** No `.text` store to a word at `+0x12` packs bits 13–15 (`or` / `shl 13` / `0xE000`-class operands next
    to the store). The descriptors therefore arrive with those bits already set, from the shader asset's parameter tables.
  - **Residue:** what the asset format puts there, most plausibly a type or array-rank code beside a 13-bit size. A reader
    reaching descriptors without `0018D240` is not excluded.
  *Narrowed further 2026-09-14 (FABLE), later the same day: the word is a reflected Phyre field, registered whole.*
  - **The descriptor is a `PShaderParameterDefinition`.** `FindShaderParameter` (`0018D240`) walks two arrays of
    `0x18`-byte elements, the shader's `+0x48` (count `+0x40`) and `+0x58` (count `+0x50`). It compares the name at
    element `+0x08` and returns the element (`0018D270`–`0018D2A7`, `0018D2C1`–`0018D2F7`).
  - **The field map matches.** The reflection schema ([the recovered field schema](../Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md), `phyre_schema.tsv`) registers
    `PShaderParameterDefinition` with `m_arrayElementCount` u16 `+0x00`, `m_parameterType` u8 `+0x02`, `m_dataType`
    u8 `+0x03`, `m_name` `+0x08`, `m_bufferLoc` `+0x10` and `m_constantBufferLocation` u32 `+0x14`: a `0x18`-byte
    element. `m_bufferLoc` is a `PShaderParameterCaptureBufferLocationSize`, which registers `m_offset` at `+0x0` and
    `m_size` u16 at `+0x2`.
  - **So `+0x10` is `m_offset` and `+0x12` is `m_size`.** `m_size` is registered as a plain `unsigned short`, with no
    bitfield split. The serializer therefore loads all sixteen bits from the shader asset, and the engine's readers
    use thirteen.

  ~~**Still open:**~~ *(answered: see the ANSWERED 2026-09-27 line below - the shipped assets store 0; 2026-10-02, OPUS)* what the asset puts in bits 13–15. It is an authored-data question (read a shipped shader's
  parameter table), and the executable cannot settle it.

  **ANSWERED 2026-09-27 (OPUS):** the shipped assets store **0** there. Every `.phyre` in the extract was read (35,984, none rejected by the namespace controls); the 2,184 that carry `PShaderParameterDefinition` hold 2,184 lists and **648,027 records, all with bits 13-15 of `m_bufferLoc.m_size` clear**. Each record is located through the file's own schema: 13-byte packed records, `m_bufferLoc` at record byte 5 (its class resolved through the member's type reference), `m_size` at +2 inside it. The largest low-13 value is 7,680 (`0x1E00`), so the `0x1FFF` mask never truncates a shipped size either. The sibling `PShaderStreamDefinition` (13,356 records in 92 lists) is also all zero there. Controls: the same loop reads bits 13-15 set in 218,033 records at the high half of `m_constantBufferLocation` (its `0xFFFFFFFF` value); a copy of a real file with one size word's bit 13 set is flagged exactly once; one schema layout in all 2,184 files. New representation fact from the strict extent check: a list's `m_objectsSize` is `count x 13` rounded up to even (339 odd-count lists carry one pad byte). So the mask is a no-op on this title's data and the bits carry no authored content here; why the SDK masks them is not answerable from this image or data. Not covered: descriptors built by code rather than loaded (the row's own write-side sweep covers code). FABLE's unpublished 2026-09-26 scratch census reached the same 648,027 / 0 by a name-lookup route. Control `_index/candidates/ea3-shader-size-bits/ea3_census.py`.
- [x] ~~**What fills the AO parameter blocks.** The degree-valued angle bias argues for an authored
  tuning asset, but **no writer was traced.**~~ **`EA-4` ANSWERED 2026-09-12 (FABLE):** the scene
  configuration's `mSAO*` / `mHBAO*` keys, read by the two scene-config loaders and stored through
  four three-float setters; constructor defaults otherwise. See the note above §5b.
- [x] **UQ-289.** **The 48 `Phyre.Rendering.NativeQualified` functions that reference no string** were not read. *(SUPERSEDED in the register 2026-09-26, FABLE, Claude Opus 5.5: a duplicate; the open residue is carried by **EA-5**)*
  They are 40 % of the tag group by count; **their share of its 44,758 bytes is not measured.** `EA-5`.

  *Narrowed 2026-09-21 (FABLE) — the byte share is measured, and 18 of the 48 are read.* A third
  instrument re-ran the split over the same 65 functions and drew the boundary in the same place:
  **13 bodies carry a real string (22,733 B), four carry only a three-byte run that decodes as text
  (258 B), and the 48 that carry none are 21,767 B — 48.6 % of the 44,758.** So the group is 40 % of
  the tag by count and very nearly half of it by weight, not a tail of stubs. The string body this
  page left unnamed is `001F5D70` (2,924 B, the `EASTL vector` one).
  - **18 of the 48 are the `PContextSwitch` family** — eight static installers at `00167050`–`00167280`,
    the constructor, the base destructor and eight deleting destructors, 1,222 B — read end to end in
    [the context-switch axes and the shader-variant key](../Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md).
    They are the shader-permutation axes: each evaluates one property of the draw, writes its value
    words into a context-variant key, and can write the `-D` define back out.
  - **The other 30 are classified, not read**: 11 `0065xxxx` render bodies (13,651 B) each reached from
    one dispatch body and each calling `0060B980`, two bodies with no caller and no data reference
    (4,948 B), nine single-caller leaves (1,349 B), one shared helper (139 B) and seven vtable-slot
    members (458 B). `UQ-289` stays open on those 30 *(answered: see UQ-289, superseded 2026-09-26; 2026-10-02, OPUS)*.
  - **The eleven are now named, later the same day** — they are the render workers of nine of
    PhyreEngine's post-effect classes, reached from slot 6 of each class's vtable, and the largest two
    are one effect's. [The Phyre post-effect class family](the-phyre-post-effect-class-family.md) reads
    the catalogue out of RTTI: **37 classes, 9 with any implementation**, and Phyre's own MLAA and SSAO
    inert beside the game's SMAA and HBAO passes above. `UQ-289` still wants the bodies; it no longer
    wants their identity.
  - **And the eleven are read, as a population** — every one builds a `PMaterialSelectorMaterialSet`
    on its own stack over the effect's own `+0x30` array and submits through `0060B980`, 24
    submissions between them; the per-worker counts of the shared vocabulary are in §4b of that page.
  - **The two no-caller bodies are the same idiom, on the game's side of the boundary.**
    `001B76E0` (203 B) is read end to end: a float from `00182EE0` stored at `+0x5A0 + 0xC8` and a
    virtual on that sub-object, `0060CE50`, then **scene-begin `005FEFD0`**, a material set installed
    at `[ctx+0x80]` from a game global, the selector built over `[[this+0x100]+0x20]`, the submission,
    and **scene-end `00600A60`** with profile id 3 — the same begin/submit/end shape as the eleven,
    which is worth noticing because the two ends are a *pair* and one page states one of their guards
    backwards (routed, not edited here). `001E2AF0` (4,745 B, the single largest member of the 48) is
    characterised rather than read: **77 direct calls over 26 distinct targets, no string at all**,
    dominated by `001A9930` ×16 and `001AD440` ×11, with exactly one selector and one submission. Its
    bulk is therefore not the draw; what those two helpers are is `EA-8`.
    **`EA-8` ANSWERED 2026-09-22 (FABLE) — and its premise was wrong; see the section at the foot of
    this page.** Both are **eight-byte global getters**, so naming them accounts for none of the bulk.
  - **The last seventeen, and with them the whole population.** The nine single-caller leaves, the
    one shared helper and the seven vtable-slot members — 1,946 B, under 9 % of the 48 by weight —
    are two small class families and their loops:
    - **A two-class pair with its constructors and destructors.** `005DBF60` (25 B) installs the
      vtable `00D498B0`, takes one argument at `+0x08` and zeroes `+0x10`; `005DC0B0` (40 B) is the
      derived form, installing `00D498B0` then `00D498D0` and zeroing out to `+0x20`. `005E2AA0`
      (66 B) and `005E2AF0` (132 B) are those two vtables' deleting destructors.
    - **Two unregistration destructors of the by-name-registry shape.** `006BEC40` and `006C0FE0`
      (125 B each) install a vtable and then, when `[this+0x18]` is non-zero, walk a global list head
      (`02E58CA0`, `02E59BB8`) unlinking `this+0x10` — the same unlink-on-destroy shape as the
      context-switch family's own destructor.
    - **Two lookups through the engine's keyed container.** `005CE850` (89 B) and `005D6E00` (74 B)
      both call `0063BC00` on the same global `02E58060` and then convert the returned node to its
      element with `add rax, -8` — the node-to-element `−8` idiom the class-descriptor and CRT-heap
      containers use.
    - **Array and count loops.** `00613770` (133 B) and `0061C250` (93 B) walk stride-`0x58` and
      stride-`0x10` arrays under a guarded helper; `0061CFA0` (130 B) is a count loop over `this+8`;
      `005DC2F0` (267 B) is ~~an array constructor over `eh_vector_constructor_iterator`~~ `PRenderer`'s constructor, which also builds an embedded array through `eh_vector_constructor_iterator` *(corrected 2026-10-02, OPUS: it stamps `00D49930`, `.?AVPRenderer@PRendering@Phyre@@`, at `005DC375`-`005DC37C`, the only reference to that vtable, then runs `00808FE4` over `+0x140`)*; `0060E9C0`
      (411 B) allocates, frees and rebuilds a container and returns 0.
    - **The shared helper** `006160B0` (139 B, 20 call sites in 13 bodies) resets an object: one call
      to `005DCBE0`, then `[this+0x30] = 0` and a walk from `this+0x38`.
    - The three material-selector bodies `0018D0E0`, `0018D100` and `0018D130` are read on
      [the post-effect family page](the-phyre-post-effect-class-family.md) §5.

    ***So every one of the 48 now has an identity, and the question changes shape.*** It asked what
    they are; that is answered for all 48. What it can still ask is which of them have been read
    **instruction by instruction** rather than characterised — and that is 18 (the context-switch
    family) plus `001B76E0`, `00652940`, `00659A90` and the four selector and predicate bodies. The
    eleven workers were read as a population by their call structure, `001E2AF0` and the seventeen
    above by shape and a partial decode. *A body identified from its shape is not a body read, and
    this page does not spend the one word on the other.*
- [x] ~~**`001945B0`** (296 B), called by several passes before their parameter runs.~~
  **`EA-6` ANSWERED 2026-09-12 (FABLE): it is the parameter-descriptor write into the constant
  buffer.** `001945B0(buffer /*rcx, u32 size at +0*/, descriptor /*rdx*/, value /*r8*/)`: admits
  descriptor type byte `+2` in `{0x12, 0x16, 0x42, 0x43, 0x44, 0xD9 … 0xDC}` (else returns 5); a
  null value returns 5; when the value carries a callback pair at `+8` / `+0x10` it is invoked first
  (`00194613`, a non-zero result is returned); the value's 24 bytes are staged (`00194620`–`00194638`)
  with the first dword rewritten to the descriptor's type when it is not already `0x42`–`0x44`
  (`0019463E`–`00194661`); then `offset = u16 +0x10`, `size = u16 +0x12 & 0x1FFF` (the `EA-3` mask),
  `offset + size ≤ buffer size` and `offset ≥ 4` are required (else 3), and `memcpy(buffer + offset,
  staged, size)` (`001946AC`) returns 0. ~~Eleven call sites in `0018D850`–`00190260`.~~ 53 call sites in 21 functions, eleven of them in `0018D850`–`00190260` *(corrected 2026-10-02, OPUS: the rest include `001930F0`, `00191E90`, `001E2AF0`, `001EE8E0` and `001F7790`)*.

  `0018D850` (3,093 B) interior read, 2026-09-17 (SWE2-FRONTIER): the **effect-record
  registration battery** — the same five-call idiom unrolled ~9 times:
  `0018D340` → `00649C20` → `00600120` → `lea r8,[02D3A440]` → `0063A990` → `00584730`
  (e.g. `0018D8EA`–`0018D9AD`, `0018D9AD`–`0018DA73`, …). `02D3A440` is the material-set
  context head (the `VPMaterialSet` default-materials cell the field schema names for
  `PMeshInstance`/`PMesh`), so each iteration registers one effect's material/context
  record. `0018D160`/`0019CE20`/`0019CB20` set up at entry (`0018D8B0`–`0018D8EA`). This is
  the body the Application-Framework page calls the "builder the graphics noise texture is
  reached from" — the noise-texture arm is one registration among the battery, not the
  whole function.

  **Input — CLIENT (25 edges), accounted 2026-09-17 (SWE2-FRONTIER).** The note names
  `0063A990`, the renderer handoff each registration ends in — Input-layer bodies
  `00873090`, `00873100`, `00873170`, `008731E0` and 21 more call it. The crossing is
  that layer's fan-in on the same shared handoff, not a post-process responsibility.
- [x] ~~**EA-7.** Whether `0018FE00`'s `SingleStepOffset` pass is FXAA~~ **EA-7 ANSWERED
  2026-09-14 (OPUS) — NO, and the engine's FXAA is a different thing in a different band.**
  - **`SingleStepOffset` carries no FXAA information, and this is measurable.** It is referenced by
    exactly **three** functions, and the other two are not anti-aliasing at all: `001930F0` is a
    subsurface-scattering blur (`sssBlur`, `useBigKernel`, `blendAmount`, `dir`, `colorTex`,
    `depthTex`, `normalTex`) and `00190260` is a font-border pass (`FontBorderSetting`,
    `FontBorderColor`). It is a generic one-texel-step uniform. `0018FE00`'s entire string set —
    `ColorBuffer`, `ColorBufferSampler`, `SingleStepOffset` — is the minimal full-screen-filter set
    and is a **strict subset of the font-border pass's**, so it identifies nothing.
  - **FXAA ships as a Phyre class family.** `Phyre::PPostProcessing::PFXAA`, `PFXAABase` and
    `PFXAAD3D11` have real vtables with **distinct per-class slots** — slot-0 constructors
    `00647530` / `00647590` / `006475F0`, slot 1 `00655C10` against `00655DC0`, slot 2 `00657430`
    against `006575E0` — all in the `006xxxxx` band, with the shader
    `/GameData/D3D11/ArtData/shaders/PhyreFXAA.fx.phyre`, script accessors for all three classes, and
    the method names **`RenderFXAA`** and **`RenderFXAAInverted`** registered from `00165120` and
    `001650F0`.
  - **Not claimed:** what `0018FE00` is — its uniform set is too generic to name it — and whether
    `PFXAA` is ever instantiated at runtime. **ANSWERED 2026-09-29 (OPUS, `CON-198`): one is. The context's constructor
    `0018CD90` builds a `PFXAA` at `+0x378` (`00645DB0`), and `00191DA0` runs its worker `0065A640` (through `0065A630`)
    on the arm that is not SMAA.** The `"FXAA exposure scale: %f"` log string at `00D95B00`
    has **0** references, which says its debug logging was compiled out, not that the class is dead.
  - FABLE's narrowing stands and is what made this answerable: `PostAA` does not select this pass.
  *Narrowed 2026-09-14 (FABLE), not answered:* **`PostAA` does not select this pass.**
  - **What `PostAA` controls.** It becomes the context byte `+0x4A3` (`001D51EA`, 1 only for `SMAA_1x`), which chooses
    SMAA or ~~a plain copy~~ **`PFXAA`'s worker on the context's `+0x378` member, then `001EE8E0` (`CON-198`)** inside `00191DA0`.
  - **What gates this pass.** `0018FE00` is called earlier in the same frame step, `001F3090` (`001F3114`), gated only by
    the global byte `01DFE0C4` (1 in the image; writers `001F2870` and `001F39B0`). With `SMAA_1x` it therefore runs
    **in addition to** SMAA, and with `FXAA` it runs beside ~~a plain copy~~ **Phyre's FXAA worker (`CON-198`)**.
  - **What is left.** The pass may still be an FXAA-style filter, but the settings mapping cannot be the evidence. The
    identification now rests on its shader constants alone.

> **Crossing into Application — FINAL-AUDIT pass 22 (FABLE, 2026-09-14).** The base constructor `00633040` is not
> specific to the parameter singleton. Its other caller is `001A98B0`, the builder of the map-art context at `01F81168`
> ([game application](../../00-Engine-Core-Runtime/Application-Root/game-application.md) BE-6). Before it builds that
> context, `001A98B0` allocates `0xA0` bytes, constructs them with the same `00633040`, and stores the
> result at `01F81170` (`001A98DB`–`001A98FC`). So the base with the self-linked list at `+0x88` is shared by at least
> two unrelated game objects. That makes it a weaker handle on the parameter block's class name than the reflection
> route above. What the `0xA0`-byte object at `01F81170` is has not been read.

## 10. Evidence

| claim | evidence | tier |
|---|---|---|
| 17 of 65 reference a string, 12 of those shader-parameter names | every function disassembled, every RIP-relative `lea` target decoded; the 5 non-passes inspected individually | 1 |
| The parameter-write idiom and its bounds checks | read instruction by instruction at four independent sites (`smaa_resolution`, `SMAA_RT_METRICS`, `g_NumSteps`, `g_NumDir`) — identical shape at all four | 1 |
| `00861EBA` is `memcpy` | named in `functions.tsv`; 6-byte thunk | 1 |
| The full SMAA ladder | all four branch chains disassembled with their `cmp` constants and stored immediates | 1 |
| `SMAA_RT_METRICS` is `(1/w, 1/h, w, h)` | the four stores at `001928EC`–`00192917`, with `1.0f` at `01CEBBA8` | 1 |
| The two AO parameter blocks and their offsets | every `movss` source operand read at both passes | 1 |
| Angle bias is degrees | `mulss` by `3.141592502593994f` then `divss` by `180.0f`, twice | 1 |
| `projScale` is the literal `500.0f` | `008F3140`, loaded directly with no config read | 1 |
| The SMAA presets match upstream | comparison against the published SMAA reference header | 3 — external |
| Which setting selects which AO | ~~**not established**~~ *(answered: see the 2026-09-14 answer, the `HDAO` setting; 2026-10-02, OPUS)* | — |
| The context object's class | **not recovered** *(answered: see the 2026-09-22 reading - not recoverable from this image; 2026-10-02, OPUS)* | — |
| `0018FE00` is FXAA | **not established — deliberately not claimed** | — |

## 11. Related

- [`../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)
  — the `Glare`, `HDAO`, `PostAA`, `DepthofField`, `SoftParticle` and `WaterQuality` settings, and
  the quality-preset matrix that drives all six.
- [`../Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`](../Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md)
  — the reflection route that could name the context object's fields, if its class is found.
- [`../The-Frame/what-happens-between-two-frames.md`](../The-Frame/what-happens-between-two-frames.md)
  — where in a frame these passes sit.

## 12. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only — the tag census and the string references re-derived from the image and
`functions.tsv`. Nothing executed.)*

### ✔ The whole census reproduces, and the partition is exact

Re-run blind: take every function carrying the tag, disassemble it, resolve every rip-relative `lea`,
and keep the targets that are a NUL-terminated printable run.

| claim | measured |
|---|---:|
| functions tagged `Phyre.Rendering.NativeQualified` | **65** |
| reference a string at all | **17** |
| of those, reference shader-parameter names | **12** |
| the rest | **1** `EASTL vector` diagnostic + **4** three-byte decodes = **5**; **48** reference no string |

**All twelve pass addresses and all twelve body sizes match**, and so does each one's set of names:
2,418 / 567 / 1,147 / 1,105 / 1,273 / 2,507 / 1,066 / 2,101 / 1,847 / 2,839 / 2,099 / 840.

> **The four §2 excludes excluded themselves.** My filter kept runs of **four or more** printable
> characters ending in NUL, and it found **13** functions — the twelve passes plus `001F5D70`'s
> `EASTL vector`. The four the page names as *"three bytes that merely decode as text"* — `005DDBA0`,
> `005E2BC0`, `005E2C40`, `005E2C90` — **fell out on their own**, because three characters is below
> the threshold. 13 + 4 = 17. **Two instruments with different rules drew the same line in the same
> place**, which is stronger than either counting 17 alone.

The one thing my classifier got wrong was its own heuristic, not the page: it filed `00191130`
(`MaskDepth`) under "other" because the name matches no `g`/`Color`/`Font` prefix. It is a shader
parameter, §2 has it as the **depth mask** pass, and the twelve stand.

**Not claimed.** §3's six-step write idiom and everything after it — **not re-read**; what any pass
does with the values; `EA-5`'s 48 unread functions stay unread. The tag itself is taken from
`functions.tsv`, not re-derived. Nothing executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — SERVICE.** A cited function calls a 93-byte core helper.
- **PlatformOnlineAchievements — MECHANICAL.** The `0018D160` section cites `00796E20`, which the
  Platform-filed `008655A0` calls. The page consults `00796E20` only as `0018D160`'s callee; the
  Platform caller was not read and nothing here depends on it.
- **Presentation — SERVICE.** Presentation-side dispatchers (`001B03D0`, `0039EC30`, `0039F9F0`,
  and the `001C3D50` reflected-parameter dispatcher) call the resolve helpers this page documents
  (`00182F50`, `0018D160`, `001C51D0`, `001C52C0`); the edge runs inward — this page's subjects
  serve Presentation callers, which are not read here.
- **Developer - CLIENT (3 edges).** `00200B50`, `00200BE0`, `00796E20` are called by bodies filed to Developer: `001C2F50`, `001C6320` - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (58 edges).** `00584740`, `00597970`, `00598100`, `0059D920` (+5 more) are called by bodies filed to Input: `0017DDC0`, `0017DE10`, `0017DE60`, `0017DFC0` (+49 more); `0079C140` reaches bodies filed to Input: `0079D010`, `0079D920` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (86 edges).** `00193D50`, `0019CE20`, `001AD440`, `0020B5F0` (+14 more) are called by bodies filed to Resource: `0019EAA0`, `0019EE50`, `001A0CF0`, `001A0E50` (+25 more); `0018D160`, `0019CB20`, `001F5D70`, `00597970` (+6 more) reach bodies filed to Resource: `001D6AA0`, `0020B5F0`, `002150D0`, `002DF980` (+12 more) - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (6 edges).** `0018CD90`, `0018F8F0`, `001EE8E0`, `005FEFD0` (+2 more) are called by bodies filed to UI: `0018EEE0` - shared machinery across the layer boundary, no shared ownership.

## The `0018CD90`/`001925D0` exclusive-subtree cluster — both roots bound (SWE2-FRONTIER, followup queue)

`0018CD90` — EH-guarded pass-object ctor: `00633040(rcx)` base init
(`0018CDAB`), then the pass defaults `byte[+0xA0] = 1`, `word[+0xEC] = 1`,
`byte[+0xEE] = 0` (`0018CDB1`–`0018CDC1`).

| member | role | interior |
| --- | --- | --- |
| `00645DB0` | field reset — `006461B0(rcx)` then zeroes `+0x50`/`+0x58`/`+0x60` (`00645DB9`/`00645DC0`) | [`00645DC0`](../../_index/ADDRESS-INDEX.md) |

`001925D0` ~~(~220 B)~~ (2,839 B *(corrected 2026-10-02, OPUS: its extent; the table above and the 2026-09-13 re-measure)*) — an EH-protected pass body (`rbp` frame,
`0xFFFFFFFE` guard at `rbp+0x17`).

| member | role | interior |
| --- | --- | --- |
| `0060D320` | flag-set wrapper — `00600B30(rcx, 0, 1)` (`0060D32F`/`0060D335`) | [`0060D335`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00633040`, `006461B0`, `00600B30`.

## Interior citation — frontier hubs `0060F6B0` / `0060D4F0` / `0060DB50` (2026-09-17, SWE2-EC7)

Three more of the "Phyre render calls" this page's passes invoke, all on the same
0x80-stride ring + `[ctx+8]` bit-0 busy flag as `00600A60`/`005FEFD0`:

- `0060F6B0` (225 B, 13 A-callers) — the four-parameter submit: same `00600B30` gate and ring
  bump ([`0060F6E7`](../../_index/ADDRESS-INDEX.md)), then on success stores the four args into
  `[ctx+0xC]`..`[+0x18]` when the aux condition passes and clears `[ctx+0xA0]`; full ring -> `0xD`.
- `0060D4F0` (612 B, 11 A-callers) — the packet-list submit: `r8d >= 8` -> `3` (too many),
  walks the `[rdx]` chain running `005C5230` on each node
  ([`0060D54B`](../../_index/ADDRESS-INDEX.md)), then enqueues per element with the same ring
  discipline; `[ctx+0xA0]` carries the last link.
- `0060DB50` (543 B, 10 A-callers) — the wide-descriptor submit: copies an 0x18-byte descriptor
  into `[ctx+0x200]` and sets `byte [ctx+0x219] = 1` ([`0060DB9C`](../../_index/ADDRESS-INDEX.md)–
  `0060DBB3`), then dispatches on `byte [node+8]` {0,1,2} before the same enqueue tail.

All three share the `0x16` busy return and `0xD` ring-full return — one submission protocol,
three payload widths.

## Interior citation — frontier hub `0060D190` (2026-09-18, SWE2-EC7)

`0060D190` — 210 B, 8 A-measured callers; the four-float member of the same `0x80`-stride
record-ring protocol as `0060D4F0`/`0060DB50`/`0060F6B0` on this page. Interior verified:
`00600B30(rcx, 0, 1)` gates submission with the vcall fallback at `0060D1C8`; the write
cursor `[+0x60]` is bounds-checked against `[+0x58]` and wraps to `[+0x50]+0x80`
(`0060D1D3`–`0060D1F4`); `[+0x88]` latches the first record and `[+0x90]` gets `record+0x80`.
The record header is kind **9** at [`0060D22A`](../../_index/ADDRESS-INDEX.md), followed by four floats at
`+0x08`/`+0x0C`/`+0x10`/`+0x14` from `xmm1`–`xmm3` and the stack — a vec4-parameter submit.
Ring full returns `0xD`, matching the sibling codes.

## Interior citation — frontier hubs `00600B30`, `001EE8E0` (2026-09-18, SWE2-EC7)

`00600B30` — 173 B, 8 A-measured callers; the capacity gate every record-ring writer on this
page calls before touching the ring. Interior verified: two window tests — first the input
range `[rcx+0x38]` + `edx` against the occupancy bound `[+0x30]` with wrap to `[+0x28]`
(`00600B46`–`00600B6D`), then the `r8d << 7` slot offset against the `[+0x60]`/`[+0x68]` pair
bounded by `[+0x50]`/`[+0x58]` at [`00600B82`](../../_index/ADDRESS-INDEX.md) — the `<<7` is the `0x80`-record
stride itself. Returns 1 only when both windows admit the submission; that is the `test al`
every writer branches on before writing a record.

`001EE8E0` — 840 B, ~~7 callers~~ 17 call sites in 16 functions *(corrected 2026-10-02, OPUS: it also looks up `ColorBuffer`, `ColorBufferSampler` and `ColorBufferOffset` at `001EE97A`-`001EE9EC` and submits through `0060B980` at `001EEBE1`)*; the submit composer that drives the whole ring battery.
Interior verified: `00189120()` supplies the context (`r14 = [rax+8]`), two resource ids are
resolved through `0018D240` name lookups (`001EE984`/`001EE996`), a `{0, K, 1.0, K*x}` float
record is staged and `memcpy`-fed from a `(w+0x10, w+0x12 & 0x1FFF)` bounded source
(`001EEA3F`–`001EEA70`), then it issues `0060D4F0` x3 at [`001EEA89`](../../_index/ADDRESS-INDEX.md)/`001EEA97`/
`001EEAA5` (selector `r8` = 0, 1, 7), `0060DB50` under a `005DC190` scope (`001EEAD0`),
`0060F6B0` or the `00186B80` fallback depending on `r15`, `005FEFD0` (`001EEB66`), a
three-way `[r14+0x80]` name select on `r12d-3` (`001EEB7E`–`001EEBA3`), `0060B980`
(`001EEBE1`), and `00600A60` with `edx = 2` or `3` on `r15`'s byte `+9` (`001EEC00`). One
call sites the full pass chain this page's writers submit.


## Interior citation — frontier hub `00194540` (2026-09-18, SWE2-EC7)

`00194540` — 105 B, 6 A-measured callers; the bounded record append the post-process bodies
(`001EE8E0`, `0018F8F0`, `0018FE00`…) push through. Interior verified: `[rdx+0x10]` and
`[rdx+0x12] & 0x1FFF` are offset and length; `offset + length > [rcx]` capacity or `r9w < 4`
returns 3 ([`00194578`–`0019458B`](../../_index/ADDRESS-INDEX.md)); otherwise `memcpy`
(`00861EBA`) at [`00194599`–`0019459D`](../../_index/ADDRESS-INDEX.md) copies ~~`r9w`~~ `r8w` *(corrected 2026-10-02, OPUS: `r9w` is the offset, `0019458D`; the length is `r8w`, `00194599`)* bytes from
`rdx` into `rcx + offset` and returns 0. The pass producers fill the shared buffer through this
one bound check.


## Interior citation — frontier hub `005DC190` (2026-09-18, SWE2-EC7)

`005DC190` — 19 B, 28 callers; the 0x18 record initialiser this chain's descriptors use.
Interior verified: stores `{rdx, 0, r8d, 0}` — pointer at `+0x00`, zeroed dword `+0x08`,
`r8d` at `+0x0C` ([`005DC19E`](../../_index/ADDRESS-INDEX.md)), zeroed dword `+0x10` — and
returns `rcx`. A three-field `{ptr, count, tag}` record shape.


### Interior citation — frontier hub `0063A990` (2026-09-18, SWE2-EC7)

`0063A990` — 177 B, 47 callers: the renderer handoff each registration ends in.
Read from the shipping image: `byte[r8+0xFC] & 8` selects the short arm — a
`005CDAA0(1, lea[02D3A440], [r8+0x30])` epoch call returning 0 — while the long
arm allocates `edi * dword[r8+0x38]` bytes through `00639510` and then fills the
`[rax+0x58]` record array at stride `dword[rsi+0x38]` with `0063C910(rsi, rbx)`
per element ([`0063AA16`](../../_index/ADDRESS-INDEX.md)), returning the array
base. `edx == 0` or a failed allocation returns 0.

### Interior citation — frontier hub `00633040` (2026-09-18, SWE2-EC7)

`00633040` — 48 B, 8 callers: the base constructor the pass ctors call.
Verified against the image: `00633070` runs first, then `[rbx+0x88]` becomes a
self-linked pair — `next` and `prev` both written `&self` at
[`00633055`](../../_index/ADDRESS-INDEX.md) — and `[rbx+0x98]` is zeroed. The
intrusive-list node init the page describes.
## SWE2-EC7-32 update (2026-09-18) — `0019CB20` keyed node insert

`0019CB20` (297 B) is the registry insert the entry-setup chain
names: `00674A00(key)` hashes, then the `+0x40`-rooted tree at
`rdi+0x30` is lower-bounded on `+0x20` keys — a hit bumps the
node's refcount (`[r9+0x28]+4++`) and returns the `+8` payload;
a miss allocates from the `rdi+0x60` pool, stamps `+0`/`+4` = 1
and `+0x10` = `esi`, copies the key through `00637C50`, and links
via `0020B5F0(&rdi+0x28, &hash)` — a failed link frees through
`002124C0` and returns 0. Interior anchor `0019CC06` (the `call
0020B5F0` link).

## SWE2-EC7-37 update (2026-09-19) - `0018F6B0`

`0018F6B0` (567 B) is the brightness post-process body - `"g_brightPara"`/`"g_BrightTex"` strings, `01F82D20`/`008F2D38`/`008F3130`/`008F3134`, `0018D240` pair plus `00861EBA`/`001945B0`/`0060D4F0`/`0060DB50`/`0060D190`/`005FEFD0`. Interior anchor `0018F760` (an `0018D240` call).

## SWE2-EC7-39 update (2026-09-19) - `00606A20`

`00606A20` (435 B) is a post-process body - `01F44830`/`02E522E0`, `00808F10`/`00808C40` plus one vcall. Interior anchor `00606A8C` (an `00808F10` call).

## SWE2-EC7-39 update (2026-09-19) - `00654FE0`

`00654FE0` (406 B) is a post-process constant body - `02D34718`/`02D35140`, `"ColorBuffer"`/`"InvColorBufferSize"`/`"LinearClampSampler"`/`"PointClampSampler"` strings, `0018D240` quadruple plus `00861EBA` triple and `00600120`. Interior anchor `00654FFD` (a `00600120` call).

## SWE2-EC7-41 update (2026-09-19) - `00186B80`

`00186B80` (332 B) is a post-process body - `0060F6B0` triple/`0060D190`/`005FEFD0`/`00600A60`/`00182F50`/`00182E50`. Interior anchor `00186C01` (a `0060F6B0` call).

## SWE2-EC7-42 update (2026-09-19) - `00639510`

`00639510` (319 B) is a post-process body - `00D586A0`/`00D586F0`, `005CDAA0` pair/`006394B0`/`00633120`/`00639750`/`00639780`/`00639320`/`00631180`. Interior anchor `00639566` (a `005CDAA0` call).

## SWE2-EC7-44 update (2026-09-19) - `00600120`

`00600120` (263 B) is a post-process body - `0060EFE0`/`006394E0`/`0063ABF0`/`00861EC0`. Interior anchor `00600166` (a `0060EFE0` call).

## SWE2-EC7-47 update (2026-09-19) - `0018D160`

`0018D160` (215 B) is a body - `00796350`/`00796E20` pair. Interior anchor `0018D17B` (a `00796350` call).

## SWE2-EC7-53 update (2026-09-19) - `00637C50`

`00637C50` (439 B) is the post-process key-copy the page names - `00597970`/`00598100`/`0059BD40`/`0059D920`/`0059E070`/`00633070`/`006336E0`/`00584730`/`00584740`. Interior anchor `00637C86` (a `00597970` call).

## SWE2-EC7-56 update (2026-09-19) - `00639780`

`00639780` (198 B) is the post-process allocation fallback the member-registration page names (`0017D260` the `_aligned_malloc` wrapper) - `0017D260`/`0063B3E0`. Interior anchor `006397E0` (a `0017D260` call).

## SWE2-EC7-59 update (2026-09-19) - `0018D340`

`0018D340` (164 B) is a call-free two-level pointer-chain scan - outer `0x38`-stride records (`+0x50` sublist, `+0x74` count gate), inner `[rax+0x78]` chain match (`02CB6780`). Interior anchor `0018D385` (the `[rax+0x78]` chain walk).

## SWE2-EC7-60 update (2026-09-19) - `006461B0`

`006461B0` (156 B) is the `+0x378` polymorphic subobject init the post-process page names - `00584730` single call plus `00D61E50`. Interior anchor `00646237` (a `00584730` call).



## SWE2-EC7-65 update (2026-09-19) - `00633070`

`00633070` (138 B) is the post-process `PInstanceList` base - `0067FFB0` single call plus `00D58650`, runs first before `[rbx+0x88]`. Interior anchor `006330DA` (a `0067FFB0` call).



## SWE2-EC7-66 update (2026-09-19) - `005FDCB0`

`005FDCB0` (132 B) is the REGISTER name-lookup - call-free `02CBF998` chain scan, `r10-rax` distance walk (name from `[rcx]`; null name returns `0x11`). Interior anchor `005FDCE0` (the `[r9]` chain load).


## SWE2-EC7-71 update (2026-09-19) - `00796350` two-pass array sweep measured

`00796350` (103 B) is the pointer-array sweep the Phyre builders share:
pass 1 runs `0063DA50` on each of the `rdx` qword elements
`[rcx .. rcx + rdx*8)`, pass 2 runs `0063B010` on each; any nonzero
return early-exits with that code, an all-zero sweep returns 0 - a
validate-then-finalise pattern over the caller's object list.
Interior anchor `00796370` (the first `0063DA50` call).

## SWE2-EC7-110 update (2026-09-20) - `001B7210` measured

`001B7210` (149 B) is the
counted slot initializer
`001B72B0`, `006497E0`,
`00649C20`, `0064A500` and
`00665360` run: `edx` slots
of 0xC0 bytes walk `rcx +
i * 0xC0`; each zeros `+0`/
`+8`/`+0x10`/`+0x28`/`+0x30`/
`+0x38`, latches `+4` = -1,
`+0x18` = 6, `+0x1C`/`+0x24`
= -1, and `00662A80(slot +
0x40)` builds the embedded
sub-object. A zero count
returns without touching the
object.
Interior anchor `001B728D`
(the `add rbx, 0xC0` slot
stride).

## SWE2-EC7-111 update (2026-09-20) - `00194A00` measured

`00194A00` (38 B) is the
four-field float setter
`001C3D50` and `001C7940`
run: `xmm2` and `xmm3` land
at `[+0x18C]`/`[+0x190]`,
the stack argument at
`[rsp + 0x28]` lands at
`[+0x194]`, and
`byte[+0x188]` clears - the
contiguous `+0x188`..`+0x194`
parameter block the pass
record carries.
Interior anchor `00194A06`
(the `+0x194` store).

## SWE2-EC7-120 update (2026-09-21) - `0065A630` measured

`0065A630` (14 B) is the
byte-shuffle thunk
`00191DA0` uses: it copies
the `[rsp + 0x28]` argument
byte back onto itself and
tails `0065A640` - a
stack-slot canonicalization
forwarder.
Interior anchor `0065A639`
(the `jmp`).

## SWE2-EC7-121 update (2026-09-21) - `0065A640` measured

`0065A640` (790 B) is the
shader-constant apply the
`0065A630` thunk peels
into. `001B81B0` pushes
the `0x42`-tagged record
`02D35140` onto the
`[+0x58]` parameter table;
when `+0x68` holds a
record it derives the
reciprocal texel `1/w`,
`1/h` floats from
`[r9+0x28]`/`[r9+0x2C]` and
`00861EBA`-copies the byte
run indexed by `u16[+0x10]`
bounded by
`(u16[+0x12] & 0x1FFF) +
start <= [r9]`, else it
returns 3. With
`byte[rbp+0x50]` set it
`005DC190`-wraps `+0x50`,
then the
`0060D4F0`/`0060DB50`/
`005FEFD0`/`0060B980`/
`00600A60` chain
(`0060B980` fed the
`rbp-0x38` record pair and
`02D34710`) installs
`02D36DE0` at `[rbx+0x80]`;
the `r15` arm repeats the
chain and picks
`02D36DC0` or `02D37860`
by `([r15+0xC] >> 1) & 1`.
Every nonzero stage exits
through `0016D6A0` on the
`rbp-0x20` temp.
Interior anchor `0065A6A2`
(the first `001B81B0`
push).

## SWE2-EC7-124 update (2026-09-21) - `0060EB60` and `0060EDB0` measured

`0060EB60` (198 B) is the
kind-8 command writer
`00190760` calls: `00600B30`
claims the lock (else
`vtable[+0x10]` releases
`rcx`), a 0x80 record is
bump-taken from the
`+0x50`/`+0x58`/`+0x60`
region (first slot seeded
into `+0x88`, end at `+0x90`),
then `{kind=8, +0xC=ebp,
+0x10=esi, +0x14=edi}` with
two stack dwords at `+8`/
`+0x18`; a full region
returns 0xD.
Interior anchor `0060EBFB`
(the kind store).

`0060EDB0` (108 B) is the
adopt-pointer helper
`00190760` calls: `r8d < 0`
exits 5; when `+8` differs
from `rdx` and `[rcx]` is
not bit-31-flagged the old
buffer is freed with
`00584730`; then `+8 = rdx`
and `[rcx] = r8d |
0x80000000` - the caller's
buffer is adopted as owned.
Interior anchor `0060EE04`
(the `+8` store).

## SWE2-EC7-125 update (2026-09-21) - the command writers, the submit builder, and the lazy resolver measured

`0060D3D0` (198 B) is the
kind-0x26 record writer
`00191560` calls: it takes
`00600B30`'s lock (releasing
through `vtable[+0x10]` when
the object refuses), claims
the next 0x80 record from the
`+0x50`/`+0x58`/`+0x60` bump
region, stamps `+0 = 0x26`,
copies the four byte fields
the caller supplies into
`+8`..`+0xB`, and bumps
`+0x220`. A full region
exits 0xD. Interior anchor
`0060D468` (the kind-0x26
store).

`00600C20` (246 B) is the
kind-0x19 record writer
`0079C140` runs: `+8` bit 0
means closed (exit 0x16);
otherwise it resolves the
owner through `005FD0E0`,
drains with
`005CD8B0(+0x2850, 1000)`
- calling the
`02CB6348`/`02CB6340`
callback pair each retry
until the wait reports
done - then takes
`00600B30`'s lock, bumps a
0x80 record, stamps
`+0 = 0x19`, and bumps
`+0x220`. Interior anchor
`00600CF7` (the kind-0x19
store). The callback pair
is installed by `005FE190`
(documented on the
game-settings page).

`0060C020` (785 B) is the
large record submit
`0060B980` drives: it clears
owner bits with
`btr 0x1f` on each count,
walks the source arrays on
a 0x2C0 stride resolving
inline-vs-indirect
pointers, builds the output
pointer table from record
index and stride, pulls
optional substructures
through `005F08E0`, and
stamps the fields the pass
consumes (`+0x68`, `+0x72`,
`+0x74` among them) before
linking the result into the
submit list. Interior anchor
`0060C110` (the first
`005F08E0` pull).

`005FECF0` (388 B) is the
flag-bit lazy resolver
`0060B980` consults: bit 0
fills `+0xA0` once via
`00604750(+0x98, +0xA8,
+0x20)` and returns it into
`[rsi]`; bit 2 resolves
`00602A40` into `[rsi+8]`;
bit 4 resolves `00602EA0`
into `[rsi+0x10]`; bit 8
runs the `00600F30` ->
`00609D80` -> `0060A010`
chain (with `006B6410`/
`006B64F0` error-string
lookup plus `vtable[+8]`/
`vtable[+0x10]` calls on the
supplied object) into
`[rsi+0x18]`, leaving the
opaque result at
`[rsi+0x20]`. Interior anchor `005FED4D` (the
`00604750` fill).

`005EB370` (371 B) is the
size accumulator `0060B980`
runs ahead of the submit:
`r9` flag bits select which
contributions land in the
`[rsi]` total and the
`[r12]`/`[r13]` components -
bit 1 adds the `*r14` record
size rounded to 16, bit 2
adds a `+0x62` word field,
bit 3 adds `[rbp+0x38]`, and
a present `r15` contributes
`00670E00`-computed
`count*0x88` (+0x80 when the
indexed `+0xC` dword is
negative), rounded to 16.
Two `005FD5F0` lookup loops
over 0x18-stride lists then
count hits into a final
`+2`-biased, 16-aligned size
for `[r13]`. Interior anchor
`005EB3F4` (the `00670E00`
call).

`005FF090` (361 B) is the
matrix fetch-or-identity
`0060B980` calls per record:
when `+0x58` bit 0 is clear
it reads the node at `+8`
and lays its fifteen floats
out as a 4x4 (padding the
empty slots with 0 and the
diagonal tail with the
`1.0f` at `01CEBBA8`); when
the flag says empty it loads
the identity constants at
`008C5F80`..`008C5FD0`
instead. Either way it then
copies the 16 dwords to
`rdx-0x40` and tails into
`005FF200`. Interior anchor
`005FF15E` (the identity
load).

## SWE2-EC7-126 update (2026-09-21) - the submit pipeline's helpers measured

`00670E00` (477 B) is the
non-empty-record count
`005EB370` and `00609D80`
call: `[rcx+0x28]` is a
{slot, run} table indexed by
`edx*2`; when the slot is in
bounds (`[rcx+0x10]` under
`btr 0x1f`) `rbx` lands on
`[rcx+0x18] + slot*24`, and
the body counts how many of
`r10d` consecutive
0x18-stride records carry a
non-zero `+0` dword - eight
per iteration through
`punpckldq`/`pcmpeqd`/
`paddd` (`01CEBCD0` ones,
`01CEBDC0` mask), a scalar
loop mopping the tail. Interior anchor `00670F9C` (the
folded count).

`005FD5F0` (52 B) is the
type-byte predicate the walk
below filters through: the
record's `+2` byte minus
0x12 selects a
`004DD62C`/`004DD624` jump
table (range 0xD0), one arm
returning 1 and the default
0 - the "is this record kind
interesting" test. Interior anchor `005FD619` (the
`jmp rcx` dispatch).

`005F08E0` (657 B) is the
optional-substructure
resolver `0060C020` and
`006007B0` call:
it walks `[rdx]` records
(0x18 stride from `[rdx+8]`),
keeps the kinds `005FD5F0`
passes, lands on the
sub-record at
`rsi + word[+0x10]`, and
dispatches on its tag byte
(`0x13`..`0xE2`, tables
`004D0B94`/`004D0B74`) to
resolve the kind's target -
inline-or-heap lists walked
`count&0x7fffffff` deep,
elements at `imul 0x58` -
into the output cursor `r8`
it returns. Interior anchor
`005F092F` (the `005FD5F0`
filter call).

`005CD8B0` (49 B) is the
drain wait `00600C20` spins
on: it calls the `[rcx]`
object's method through the
`008C20E0` thunk and returns
0 while the result is
neither `0x80`
(WAIT_ABANDONED), `0x102`
(WAIT_TIMEOUT) nor `-1`
(failed); those three map to
5. Interior anchor
`005CD8B7` (the indirect
wait call).

`005FF200` (924 B) is the
record-materialize tail
`005FF090` falls into: when
`+0x58` bit 1 is set it
copies `[rax+0x30]` (masked)
source records from
`[rcx+0x18]` into
0x58-stride outputs at
`r14+0x58`, four records per
iteration with a scalar
mop-up, the dword fields
repacked from the source
layout into the target's.
Interior anchor `005FF260`
(the unrolled copy head).

`00609D80` (652 B) is the
cookie-guarded fill
`005FECF0`'s bit-8 chain
runs second: `00670E00`
counts the live records for
the `+0x40` index, tables of
`count*16` and `count*8` are
laid out against
`[r15+0x28]`, and
`00808F10`/`006718B0`/
`00662A80`/`00808C40` fill
and commit them. Interior anchor `00609DF2` (the
`00670E00` count).

`0060A010` (960 B) is the
two-table matcher
`005FECF0`'s bit-8 chain
ends on: for each `r8+0x98`
record (0x18 stride at
`+0x30`, count `+0x28`
masked) it scans the
`+0x20`/`+0x50`-indexed
0x88-stride table for the
entry whose pointer and flag
byte line up, honouring the
`edx` bitmask per slot; a
miss once-logs through
`005CDAA0` (`00D4B540`) and
exits 0x13. Interior anchor
`0060A1D8` (the `imul 0x88`
record index).

`00602EA0` (2,182 B) is the
transform resolve
`005FECF0`'s bit 4 fills
`[rsi+0x10]` with: it
requires `[rdi+0xA8]`,
pulls the record's
`+0x20`/`+0x90`/`+0x48`/
`+0x28` members, runs
`006090B0` for the inverse,
composes through
`00678B50` and the
`00185100`/`001854C0`
pack helpers, stamps the
result with `006107F0`, and
bounds-checks tail copies
through `00861EBA`. Interior anchor `006032CB` (the
`006090B0` inverse call).

`00600F30` (5,959 B) is the
materializer `005FECF0`'s
bit-8 chain opens with:
cookie-guarded, `xmm13`
holding `1.0f`, it walks the
`rdx` record (`+0x98` header,
`+0x20`, the `+0x50` window,
`+0x30` table), allocates
through `00861F08`/
`00861F14`, builds from the
`008C5F80`..`008C5FD0`
identity constants, and
fills through `005DFCD0`,
`00606BE0`, `005FF5A0`,
`006073D0`, `00670920` and
`00861EBA`, logging via
`005CDAA0` at the reject
paths. Interior anchor
`00600F7B` (the `1.0f`
constant load).

## SWE2-EC7-127 update (2026-09-21) - the materializer's helpers measured

`006718B0` (597 B) is the
per-entry output-record
materializer `00609D80` calls:
it indexes the `{index, count,
multiplier}` record at
`[rcx+0x28] + r8*16`, resolves
the stride-24 element array
`[rcx+0x18]` through the
`btr 0x1f` count at
`[rcx+0x10]`, scans forward
from `r12` for the first
non-zero entry dword, and for
each run element calls
`00600BE0` on `[elem+8]` - a
hit sets `dil` and later
drives `006BA720` for a
length folded into
`+0x78 = (len+edi)*mult` with
kind byte `+0x1c` raised to 4.
Each iteration materializes a
0x88 record (embedded
`+0x28` sub-object carrying
vtable `00D68DD0`, RTTI
`01D20458`; `+0x1d`=2,
`+0x20`=1, `+0x10` = the run
base, `+0x08` = run length
with the `bts 0x1f` heap
flag) and stores it into
`out[r13]`; the return is the
emitted count.
Interior anchor `00671990` (the `00600BE0` predicate call).

`00670920` (175 B) is the
two-level keyed matcher
`00600F30` and `00671670`
call: outer loop over
`[rcx+0x30] & 0x7fffffff`
records at `[rcx+0x38]`
(stride `0x88`), inner loop
over each record's own
`[+0x08] & 0x7fffffff`
elements at `[+0x10]`
(stride 24), comparing
`[elem+8]` against `r8`; on a
match it stores the outer
record through `[rdx]` and
returns the element pointer,
else null.
Interior anchor `00670996` (the `[elem+8] == r8` compare).

`006107F0` (204 B) is the
4x4 matrix transpose
`00602EA0` calls during
transform resolution: all
sixteen elements are lifted
scalar (`movss` per field
into the stack frame) and
stored back as four `movups`
rows - column-major in,
row-major out.
Interior anchor `0061089B` (the first transposed row store).

`006073D0` (50 B) is the
stride-12 inline-or-heap
element getter `00600F30`
uses: `[rcx+0x20]` count under
`btr 0x1f`, the element base
is `[rcx+0x28]` when the count
exceeds 1, the inline storage
at `rcx+0x28` when it is 1,
and null at 0; the return is
`base + edx*12`.
Interior anchor `006073E6` (the `base + idx*12` address).

`00606BE0` (126 B) is the
vec4 gather `00600F30` calls:
with `n = [rcx+0x10] & 0x7fffffff`
over the element array
`[rcx+0x18]`, component i is
read from field `0xC8 +
i*0xE8` whenever `n > i` and
defaults to the `00D50040`
constant pair otherwise -
the four writes land at
`[rdx]`..`[rdx+0xC]`.
Interior anchor `00606BFB` (the `+0x380` component load).

`005FF5A0` (303 B) is the
UV-derivative normalizer
`00600F30` calls: it forms
`1/([rbx+0x38]^2 - [rbx+0x34]^2)`
into `xmm9` (sign-flipped via
the `01CEBDA0` mask), rounds
`[rbx+0x2C]+eps` and
`[rbx+0x28]-eps` through
`00861F08`, and normalizes
`(v - lo)/(hi - lo)` with the
`-1.0` constant `01CEBC9C`;
two of the four outputs are
gated on `[rbx+0x20]` matching
either of the `01F2EDA8` /
`01F2ED48` globals (both hold
vtable `00D82F28`), so the
fallback emits a zeroed /
`1.0` pair for the other
record kind.
Interior anchor `005FF629` (the first `00861F08` call).

`005DFCD0` (264 B) is the
affine point transform
`00600F30` calls: `out.xyz =
v*M + row3` with the implicit
`w = 1` - the row-3 term is
added outright rather than
scaled, and `[rdx+0xC]` is
never written.
Interior anchor `005DFD69` (the `out.x` store).

`005DFDE0` (313 B) is the
explicit-w sibling
`00602EA0` calls: `out.xyz =
v*M + w*row3` with `w` taken
from `[r8+0xC]` and stored
verbatim at `[rdx+0xC]` - the
same shufps ladder as
`005DFCD0` plus the w-scaled
translation term.
Interior anchor `005DFE85` (the `out.x` store).

`00600BE0` (37 B) is the `+0x30`-table `rdx`-match predicate `006718B0` calls: null `rcx` returns 0; otherwise reads the count at `[rcx+0x28]` (`btr 0x1f` heap flag) and walks the `+0x30` element array at stride 24 (`rax = rax*3 + rax`, `lea` into `rax*8`), returning the first element whose `+0` key equals `rdx`, else 0. The guard ordering is reversed from the sibling getters — the `null` test precedes the count load.

Interior anchor `00600C05` (function `00600BE0`).

`0018D3F0` (511 B) is the lazy-singleton arm `00191130` calls: `01F7F5F0` null -> `00210EC0(0x4A8)` + `0018CD90` and store, then `byte[rdx+0x110]` copies to `[rbx+0x20]`, and `[rdi+0x124] == 1` with positive `[rdi+0x128]` runs the `01CEBC70`-constant float ramp - the pass's shared-state init.

Interior anchor `0018D420` (function `0018D3F0`).

## EA-8 answered — two eight-byte getters, and a premise that does not survive measurement (2026-09-22, FABLE)

`EA-8` asks what `001A9930` and `001AD440` are, because *“naming those two would account for most
of the body”* of `001E2AF0` (4,745 B, the largest of `UQ-289`'s 48). **They are named below, and
they account for none of it.**

### The premise, measured (FABLE)

Both callees are **eight bytes**: `mov rax, [rip+disp] ; ret`. The 27 calls to them are 27 loads of
a global. Decomposing the caller by instruction class — controls first: the sweep reproduces this
page's own **77 direct calls over 26 distinct targets**, with `001A9930` ×16 and `001AD440` ×11:

| class | instructions | bytes | share of 4,745 |
|---|---:|---:|---:|
| move / address (`mov`, `lea`, `push`, `pop`) | 581 | 2,832 | **59.7 %** |
| compare | 127 | 546 | 11.5 % |
| branch | 175 | 504 | 10.6 % |
| **call (direct)** | **77** | **385** | **8.1 %** |
| integer / other | 92 | 301 | 6.3 % |
| SSE / float | 33 | 140 | 3.0 % |
| padding | 6 | 37 | 0.8 % |

**44 of the 77 calls (57 %) go to callees of 16 bytes or fewer** — global getters plus the
`0016D6A0` folded stub. Every direct call instruction in the body totals **385 bytes, 8.1 %**. So
the sentence *“naming those two would account for most of the body”* is false by a wide margin, and
the better question is the one the numbers pose: **`001E2AF0` is 59.7 % data movement with one
selector and one submission — what structure is it building?** **Answered in the next section.**

### `001A9930` — the map-art context getter, already named elsewhere (FABLE)

`001A9930` is `mov rax, [01F81168] ; ret`, **251 call sites in 47 functions**. The database already
identifies that global: it is the **`0x520`-byte map-art (`.ta` texture-animation) context** built by
`001A98B0` and stored at `01F81168` by `001A9922`
([the game application](../../00-Engine-Core-Runtime/Application-Root/game-application.md), and the
arm catalogue's slice D, which names `001A9930` as exactly this getter). Its readers cluster on
`+0x2D0`–`+0x304`, and `+0x2E4` is the one field they write.

> **A defect this turned up, routed not edited.** The battle-frame contract records
> `001800E0 = byte[001A9930() + 0x41A] != 0` and glosses the object as *“console singleton
> `*(01F68168)`”*. **`01F68168` has zero rip-relative references anywhere in the image**; the getter
> returns `01F81168`. The mechanism is right — `+0x41A` is confirmed read through this getter — but
> the address is a transposition and the gloss contradicts this database's own pages, which call it
> the map-art context rather than the console. The same sentence is copied into `PROGRAM-STATE.md`.

### `001AD440` — the nested-element registry the render-list helpers index (FABLE)

`001AD440` is `mov rax, [01F811C8] ; ret`, **83 call sites in 20 functions**. Its object is a
lazily created singleton:

```asm
FUN_001AD3E0:  if ([01F811C8] == 0) { rax = 00210EC0(0x258) ; if (rax) 001AA9E0(rax) ; [01F811C8] = rbx }
FUN_001AD440:  mov rax, [01F811C8] ; ret
FUN_001AD450:  rcx = [01F811C8] ; if (rcx) jmp 001ACF80        ; conditional teardown
```

`0x258` bytes, **no vtable** (`001AA9FD` writes a *byte* at `+0`), and its constructor `001AA9E0`
registers five EASTL allocator names, the first from `008F4120` = `"EASTL map"`.

**What it is, from what reads it rather than from its constructor:** the pointer is handed to
`001AC670` ×7, `001AC720` ×6 and `001ABF50` ×3, and the offsets read off it are `+0xA8` ×8,
`+0x40` ×6, `+0xE8` ×2. Those are **exactly the fields this database already documents for those
two helpers** — `001AC670` is *“the bounds-checked nested index the ordered objects run”* (`[rcx+0xA8] < 0`
guard, the `[+0xE8]` vector, each element's `+0x44`-indexed `0x30`-stride sub-array) and `001AC720`
is *“the list-element peek the render-list bodies call”* (same `+0xA8` guard, same `[+0xE8]` vector)
([the ordered render command list](../../17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md)
SWE2-EC7-32 and SWE2-EC7-71).

> **So `01F811C8` is the nested-element registry those two helpers index**, and `001AD440` is its
> accessor. The identification is by **field agreement between two independent readings** — a
> caller-side offset sweep here, and the helper bodies read by another session — not by the
> allocator string, which only says the container is a map.

*Not claimed:* what the elements are. The registry's element type, and what `+0x40` holds, are
unread; `001ABF50` is documented on the character-render page as a record op over `+0x3C0`/`+0x3D0`
at 16-byte stride, which is a third consumer with a different field set.

## What `001E2AF0` builds — a map render pass, chosen by name, then 34 shader constants (2026-09-22, FABLE)

The section above measured the body as three-fifths data movement and left *what it is building* as
the open question. It is two things, in two straight-line regions, and neither is a structure on the
stack: **it picks a named render pass, then fills a constant buffer.**

`001E2AF0(obj /*rcx → rdi*/, ctx /*rdx*/)` is the body `MapOrderedObject`'s `00212C60` tail-jumps into
with `rcx = [mapobj+8]`
([the render-command-list contract](../../17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md)).
Its prologue is `mov rax, rsp … lea rbp, [rax-0x158]`, so **`rbp` is a frame pointer, not an object**,
and `rax` aliases the frame while the eight `xmm6`–`xmm13` spills are taken — both facts are needed
before any displacement off those registers is read as a field.

### Region A, `001E3065`–`001E3347`: the pass is chosen by name (FABLE)

A switch stores one of twelve static record pointers into `[+0x80]`. Each record's first qword is a
`char*`, and the names say exactly what the switch is deciding:

```
DefaultMapRenderPass  Nzt|Zt   Nzw|Zw   At|Nat   NoBlending|LinearBlending|AddtiveBlend|SubtractBlend
                      z-test   z-write  alpha-test          blend mode
```

— nine `DefaultMapRenderPass…` variants plus `NoBlendWithAlphaClip` and `WaterPassForStencil`, and
one slot at `01F82D38` that is `.data` virtual tail, zero at rest. **That twelfth slot is named:
`MapShadowRender`** — corrected 2026-09-22 (FABLE) once the runtime registry was censused; it is
registered by a CRT initializer through `FUN_005DC6F0`, which is why reading the file gave nothing.
See the post-effect family page, §“GF-7, second half”. **`AddtiveBlend` is spelt that way in the
image**, missing its `i`; it is quoted verbatim because a search for `AdditiveBlend` will miss it.

### The array those records belong to, enumerated (FABLE)

[The post-effect class family](the-phyre-post-effect-class-family.md) §"Slot 5" describes this as *“a
stride-`0x20` array of named render passes — `Opaque`, `OpaqueRGB`, `Transparent`, `DeferredRender`,
and a run of `DefaultMapRenderPass…` variants — each `{name, 0, 0, 0xFFFFFFFF}`”*. Walking that shape
in both directions from its `01F2D6E0` (`Transparent`), with an off-stride address rejected as the
control, gives the whole run: **56 records, `01F2D6A0`–`01F2DD80`, ending in a sentinel named
`NULL`**. Full table:
[`members/named-render-pass-array.tsv`](members/named-render-pass-array.tsv).

The vocabulary groups cleanly — 4 general (`Opaque`…`DeferredRender`), 9 `DefaultMapRenderPass`,
4 `AteGequalFbonly*`, 1 `NoBlendWithAlphaClip`, 5 `WaterPassFor*`, 17 `ChrOpaque*`
(`Clip`/`Reflection`/`Refract`/`NoGS`/`PT` in combination), then the post-effect passes
`DOFWriteOnePass`, `SAO*` ×4, `HBAOGenerateAO`, `ColorCorrection`, `SSS`, the three MLAA-shaped
stages `ColorEdgeDetection` / `BlendingWeightCalculation` / `NeighborhoodBlending`, `FontBorderWidth`,
`FontBorderHeight`, `BrightBlend`, `DebugMask`, `NULL`.

### Region B, `001E3514`–`001E3C29`: 34 constants written through a descriptor table (FABLE)

Every store has the same three-instruction shape — fetch a descriptor, read its 16-bit offset, store
one field of the source object at that offset in the buffer:

```asm
001E351C  mov   rax, [r14]              ; a descriptor from the table (r14 += [rdi+0x38] at 001E3514)
001E351F  movzx ecx, word [rax + 0x10]  ; the descriptor's 16-bit buffer offset
001E3523  mov   eax, [rdi + 0xC8]       ; a field of the object
001E3529  mov   [rcx + rsi], eax        ; store it into the constant buffer
```

**`rsi` is the constant buffer, not the second argument** — it is reloaded at `001E34F5`/`001E3502`
(`rsi = [[table + r12] + 8]`), and `[rsi+0]` is its `u32` byte size. Counted with access widths:
**34 stores of the form `[offset + rsi]` — 23 × 4 B, 5 × 8 B, 6 × 16 B**, 228 bytes of constants.

**This is `FUN_001945B0` open-coded.** That helper — already answered on this page as `EA-6`, *“the
parameter-descriptor write into the constant buffer”* — reads the **same** descriptor field,
`movzx r9d, word [rdi+0x10]` at `0019466E`, and compares against the **same** buffer size,
`cmp ecx, [rsi]` at `0019467C`. `001E2AF0` calls it twice and inlines the rest.

**One value is variable-length and is bounds-checked** (`001E360F`–`001E362F`): the offset is masked
to 13 bits, `offset + size` is compared against `[rsi]`, a second test requires ~~`size >= 4`~~ `offset >= 4` *(corrected 2026-10-02, OPUS: `001E3619 cmp r9w, 4`, `r9w` the offset loaded at `001E35FE`; the size is `dx`, `001E3620`)*, and only
then does `memcpy` run. *Not claimed:* that the 34 fixed-width stores are checked — no size compare
was found guarding them, but absence over one body is not a rule, and their widths are compile-time
constants while the `memcpy`'s is not.

> **So the 59.7 % is not overhead.** The body is a *parameter upload*: choose the pass, then move 34
> named constants from the object into the GPU buffer at reflection-supplied offsets, build the one
> material selector and submit once. A call census reads it as *“77 calls, mostly two unknown
> helpers”*; the instruction mix reads it as what it is.

~~*Still not read:* the region between `001E3347` and `001E3514`, and the tail after `001E3C29`.~~ **Both read 2026-09-22 (FABLE) — the section below.**

## EA-2 — the class name is not in the image, and the object's shape is (2026-09-22, FABLE)

`EA-2` identifies the post-process context as the `0x4A8`-byte singleton at `01F7F5F0`
(`00193D50` → constructor `0018CD90`, base `00633040`, no vtable) and leaves the **class name**
open, proposing the reflection schema as *“the obvious route, since a class with floats named
`radiusChr`/`biasChr` would be unmistakable”*.

### The proposed route is dead (FABLE)

**The object is not a reflected class.** Searching
[the recovered field schema](../Reflection-And-Class-Metadata/phyre-field-schema.tsv) for a member
at any of this object's known offsets — `+0x184` (SMAA quality), `+0x198`, `+0x344`, `+0x2E0` —
returns **no rows at all**. A reflected class registers its members through `FUN_00632960`, and
nothing registers these. That is consistent with the row's own finding that the object has no
vtable: it is a game-side struct, not a `Phyre` class, so neither RTTI nor the reflection schema
can name it.

**And nothing else names it either.** `FUN_0018CD90` is **829 bytes with zero rip-relative
operands** — no string, no descriptor, no global. It is a pure defaults writer: chain to
`00633040`, then a run of literal stores (`+0xA0` = 1, `+0xEC` = 1, `+0xF0` = `1.1f`, `+0xF4` =
`0.8f`, `+0xF8` = `0.1f`, `+0x110` = 1, `+0x114` = `4.0f`, `+0x118` = `20.0f`, …).

> **So the class name is not recoverable from this image by any route this database uses.** RTTI
> needs a vtable and there is none; the reflection schema needs a registration and there is none;
> a name string would have to be referenced and the constructor references nothing. Naming it needs
> a source outside the executable — a PDB, a Phyre SDK header, or a matching build.

### What is recoverable, and was not on the row (FABLE)

The base chain says what kind of object it is:

```asm
FUN_00633070 (138 B):  [this] = this ; [this+8] = this        ; an intrusive list head at +0x00
                       rax = this+0x10 ; [rax] = rax ; [rax+8] = rax   ; a second at +0x10
FUN_00633040 (48 B):   call 00633070
                       rax = this+0x88 ; [rax] = rax ; [rax+8] = rax   ; a third at +0x88
                       [this+0x98] = 0
```

Three **self-referential (empty) intrusive list heads**, at `+0x00`, `+0x10` and `+0x88`. So the
post-process context is a **node that can be a member of three lists at once**, carrying ~`0x4A8`
bytes of tuning state behind them. `FUN_00633040` is shared by **8** callers and `FUN_00633070` by
2, so the listable base is a small reusable one rather than this object's own.

*Not claimed:* which three lists, or what the `+0x98` counter beside them holds. And the name hunt
is reported as bounded rather than failed — the three routes above are the ones that exist here, and
all three are closed by measurement rather than by not finding anything.

## `001E2AF0` finished — it loops over materials, and “straight-line” was wrong (2026-09-22, FABLE)

The section above left two spans unread and called regions A and B *“two straight-line regions”*.
**Region B is not straight-line: it is the body of a loop**, and reading the two spans finishes the
body and explains every call count `EA-8` measured.

### The outer loop, and what it walks (FABLE)

```asm
001E34D0  eax = [rcx]             ; rcx = [rsp+0x60]
001E34D2  btr eax, 0x1F           ; clear bit 31 -> the COUNT
001E34D6  cmp r15d, eax ; jae out
001E34DF  cmp eax, 1 ; jbe …      ; count <= 1 -> storage is INLINE at [rcx+8]
001E34E4  rax = [rcx+8]           ; otherwise the heap pointer
001E34F5  rsi = [rax + r12]       ; the r15-th element (r12 = r15 * 8)
001E3502  rsi = [rsi + 8]         ; <- and THIS is the buffer region B writes
```

That is the `PArray` shape this database already documents — a count whose **bit 31 flags inline
versus heap storage**, with the inline object living at `+8`. So the body walks an array of
elements and, for each, takes the element's `+8`.

**And `GF-5`'s schema facts name them.** `PMaterial::m_parameterBuffer` is at offset `0x8`, and
`PParameterBufferBase::m_parameterBufferSize` is at offset `0x0`. The element is a **`PMaterial`**,
`rsi` is its **parameter buffer**, and `[rsi+0]` is that buffer's **reflected size** — which is
exactly the value the bounds-checked `memcpy` at `001E3615` compares against. The check the earlier
section reported as *“against `[rsi]`”* is a check against `m_parameterBufferSize`.

> **So `001E2AF0` writes the same 34 constants into the parameter buffer of every material in an
> array**, not once into one buffer. The earlier section's “34 stores, 228 bytes of constants” is per
> material.

### The span `001E3347`–`001E3514`: four registry lookups and ~~a rect~~ the shadow-blend windows (FABLE; corrected 2026-09-26)

```asm
001E33EB  lea rsi, [rdi + 0x230]        ; the effect's own index array
001E33F5  loop, four times (rbx 0 -> 0x20 step 8):
            001AD440() ; edx = [rsi] ; 001AC670(registry, index)  -> [rbp+rbx+0x38]
            001AD440() ; edx = [rsi] ; 001AC720(registry, index)  -> [rbp+rbx+0x58]
            rsi += 4
```

`FUN_001AD440` is the accessor for the **nested-element registry** `01F811C8` that `EA-8` named, and
`001AC670`/`001AC720` are its bounds-checked index and its element peek. So the loop resolves **four**
indices from the effect's `+0x230` array into two four-entry frame tables.

**That closes `EA-8`'s arithmetic exactly.** Four iterations × two calls = 8, plus the three outside
the loop = **11**, which is the figure `EA-8` measured for `001AD440` without knowing where it came
from.

~~The span then builds a rectangle from four floats of the map-art context (`001A9930()`):
`x = [+0x318] × s`, `w = [+0x31C] × s − x`, `y = [+0x320]`, `h = [+0x324] − y`, with
`[r14+0x5C] >> 11 & 1` able to force `x = −1.0f` and `[rdi+0xC0]` able to force a `1000.0f` clamp.~~

> **Corrected 2026-09-26 (FABLE, Claude Opus 5.5; own error): it is not a rectangle.** The map-JSON loader
> `001C7940` stores the four floats under these keys:
>
> | field | key | store |
> |---|---|---|
> | `+0x318` | `mShadowVertexBlendLowerLimit` | `001C95C1` |
> | `+0x31C` | `mShadowVertexBlendUpperLimit` | `001C960A` |
> | `+0x320` | `mShadowAngleLowerLimit` | `001C9653` |
> | `+0x324` | `mShadowAngleUpperLimit` | `001C969C` |
>
> The span turns them into two (start, width) windows and uploads them as **one float4**. `rbp` is `rsp + 0x100` in
> this frame (the prologue's `lea rbp, [rax-0x158]` against `0x38` of pushes and `sub rsp, 0x220`). So `[rbp−0x80]`
> and `[rbp−0x7C]` are `[rsp+0x80]` and `[rsp+0x84]`, and the four stores fill `[rsp+0x78]`..`[rsp+0x87]`.
> `001E34B9` loads that span whole into `xmm6`, and `001E3560` stores it at descriptor `[r14+0x1F8]`'s offset in
> every material's buffer:
>
> `(vertexLower × 0.5, (vertexUpper − vertexLower) × 0.5, angleLower, angleUpper − angleLower)`
>
> - **The old `s` is the constant 0.5** (`01CEBB70`, loaded into `xmm13` at `001E2C4D`).
> - **The flag overrides the angle pair, not `x`.** `[r14+0x5C]` bit 11 overwrites components 3 and 4 with
>   `(−1.0, 0.0001)` (`001E3492` / `001E3499`).
> - **The `1000.0f` is not one of the four.** When `[rdi+0xC0]` is set, the renderer's `+0xCC0` (`001E33C6`) is
>   raised to at least 1000.0 (`001E33DD`–`001E33E3`). `001E3549` then writes it at descriptor `[r14+8]`.
>
> **The body reads three more map-art fields the same loader names:**
> - `+0x2C0`/`+0x2C4`/`+0x2C8` are `mMapLightColorR`/`G`/`B` (`001C93F0`–`001C9401`). `001E3AFC`–`001E3B0F` upload
>   them as a float3 at descriptor `[r14+0xD0]`.
> - `+0x3D9` is `EnableMapNormalMap` (`001CA4B3`; the cutscene loader stores it too, at `001C4EC8`). `001E337A`
>   reads it only when the console's use-normal-map byte `+0xC71` is set, and the resulting 1 or 0 goes to
>   `[rbp−0x60]`.
> - `+0x43C` and `+0x440` are `mMapShadowDepthBias` (an int) and `mMapShadowSlopeOffset` (`001C8EA1` / `001C8EE8`).
>   Only on the `MapShadowRender` branch (`01F82D38`, `001E305E`), `001E307E` converts the bias to float and
>   `001E3091` passes both to `0060E810`, which records render command `0x25`. After the materials, `001E3CD1`
>   records it again with flag 0 and two zeros. [The Gi command family](../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md)
>   reads that command's stream consumer discarding it.

### The tail after `001E3C29`: one selector, one submit (FABLE)

```asm
001E3C5A  00189120() -> the renderer ; 001E3C66  00185A80(renderer, [rsp+0x34])
001E3C6F  lea rcx, [rip -> 008C6C98] ; [rbp]   = rcx     ; the selector vtable
001E3C7A  [rbp+8] = [r14+0x20]                           ; its PArray
001E3C87  [rsp+0x20] = [rsi+0x220]
001E3C9E  call 0060B980                                  ; the submission
```

`008C6C98` is **`PMaterialSelectorMaterialSet`** — the same selector the eleven Phyre post-effect
workers build ([the post-effect family](the-phyre-post-effect-class-family.md) §5). A game body and
the middleware's own workers submit through the identical interface.

> **`001E2AF0` is now read end to end**: choose a named map render pass → resolve four registry
> elements and the shadow-blend float4 (*“a rect” until 2026-09-26*) → for every material in the array, write 34 constants into its parameter
> buffer at reflection-supplied offsets → build one selector and submit once. It is the single
> largest member of `UQ-289`'s 48, and it moves from *characterised* to *read*.

`001C51D0` (232 B) is the four-deep `001FF740`/`00200BE0` name-resolve chain `001C3D50` runs: it resolves the argument's parent and, on success, prefers the `01F813F8`-indexed `01F813D8` record when `01F81418` is set and that record resolves - else the `01DF6E50` default; it then resolves `"Common"` (`008FA3CC`), the argument, and `01F81328` in turn, and tail-jumps `001FF740` on `01F813C8` (resolved) or `01F81328` (unresolved) - the `01F813xx` table's chained lookup

Interior anchor `001C525A` (function `001C51D0`).

`001C52C0` (227 B) is the cross-slot sibling of `001C51D0` that `001C3D50` also dispatches to: it `001FF740`-resolves `r8` and `00200BE0`-tests it, prefers the `01F81418`-gated `01F813D8[idx*0x10]` record (accepting it only when its own `00200BE0` fails, else `01DF6E50`), resolves "Common" plus the `rbx` name on that record, then picks `01F813C8` over `01F81328` when the second name `00200BE0`-accepts - and tails `001FF740` on the resolved pair

Interior anchor `001C5335` (function `001C52C0`).

`001AC4B0` (446 B) is the parameter line reader `001ACF80` runs per post-process row: `0018A330` parses the line through the `008F6D3C` format pair (`%d`/`%f`), the cursor skips CR/LF, and when the parsed `int` index is below the `([r14+0xF8] - [r14+0xF0]) >> 3` qword count the loop writes the float into the indexed slot - the text-side feed of the shader-constant tables this page maps.

Interior anchor `001AC4CD` (function `001AC4B0`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-post-process-passes-and-their-shader-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00167050` | 66 B | when `006B8D20(01F2EC18)` returns 0, increments dword `02E522E0` and stores 1 in dword `01F2EC38`; on both paths then stores the address `00D80F20` in qword `01F2EC18` and tail-jumps `00808B90` with `rcx` = `008B5830` | `0016705B`, `00167064`, `0016706A`, `00167082`, `0016708D` |
| `00167280` | 66 B | when `006B8D20(01F2ECB8)` returns 0, increments dword `02E522E0` and stores 1 in dword `01F2ECD8`; on both paths then stores the address `00D80FC0` in qword `01F2ECB8` and tail-jumps `00808B90` with `rcx` = `008B5BB0` | `0016728B`, `00167294`, `0016729A`, `001672B2`, `001672BD` |
| `00182E50` | 44 B | when `001DDAB0()` is non-null, calls it again and tail-jumps `001DD110` with that pointer in `rcx`; otherwise returns the float 1.777778 (`008C5B38`) in `xmm0` | `00182E54`, `00182E5E`, `00182E6A`, `00182E6F` |
| `0019EE50` | 167 B | for each qword in the array from qword `rcx+0x100` to qword `rcx+0x108` (count `(end - start) >> 3`, re-read every pass, unsigned index compare), calls `0063DA50` and then `0063B010` on qword `+0x108` of the pointed-to object; on both the empty and the looped path then stores 1 in byte `rcx+0x128` | `0019EE6D`, `0019EE9A`, `0019EEB1`, `0019EECC`, `0019EECE` |
| `001D6AA0` | 53 B | returns 1 when the low byte of `0020B9A0(0020C700(), ecx, rdx)` is non-zero and 0 otherwise | `001D6AAF`, `001D6ABC`, `001D6ACA` |
| `001F39B0` | 38 B | calls `001F9A60(00193D50(), dword rcx+0x18)` and then stores 1 in byte `01DFE0C4` | `001F39B9`, `001F39BE`, `001F39C4`, `001F39C9` |
| `005CE850` | 89 B | calls `0063BC00` with `rcx` = `02E58060` (`rdx` passed through) and returns 0 when the result is null or the result minus 8 is null; otherwise, when `rdx` is non-null, writes `00D498B0` and then `00D498D0` to qword `[rdx]`, the result minus 8 to qword `+8`, 0 to dwords `+0x10` and `+0x18` and to qword `+0x20`, and returns 1 (also 1 when `rdx` is null) | `005CE860`, `005CE86A`, `005CE881`, `005CE88C`, `005CE899` |
| `005D6E00` | 74 B | calls `0063BC00` with `rcx` = `02E58060` (`rdx` passed through) and returns 0 when the result is null or the result minus 8 is null; otherwise, when `rdx` is non-null, writes `00D498B0` to qword `[rdx]`, the result minus 8 to qword `+8` and 0 to dword `+0x10`, and returns 1 (also 1 when `rdx` is null) | `005D6E10`, `005D6E1A`, `005D6E2C`, `005D6E2F`, `005D6E33` |
| `005DBF60` | 25 B | stores the address `00D498B0` at qword `[rcx]`, `rdx` at qword `+8` and 0 at dword `+0x10`, and returns `rcx` | `005DBF67`, `005DBF6A`, `005DBF6D`, `005DBF71` |
| `005DDD60` | 79 B | walks the singly linked list headed by qword `02CBF998` through each node's qword `+8`, keeping the address of the link that points at the current node; when a node equals `rcx` (its `+8` address equals `rcx+8`), stores that node's qword `+8` into the previous link (the head itself for the first node) and zeroes the node's `+8`; returns without change when the list is empty or `rcx` is not found | `005DDD8B`, `005DDD90`, `005DDD94`, `005DDDA7`, `005DDDAA` |
| `0061CFA0` | 130 B | returns 0 when `edx` is 0; otherwise uses `rcx+8` as the storage when `edx` is 1, or `0017D260(edx * 0x40, 8)` when it is larger (unsigned), returning 0 if that is null; then for `edx` elements of `0x40` bytes zeroes qwords `+0`, `+8`, `+0x10`, `+0x18` and dword `+0x20` and stores the address `00D54358` at qword `+0x28`, and returns the storage pointer | `0061CFBB`, `0061CFC9`, `0061CFF9`, `0061D00B`, `0061D019` |
| `00659A90` | 391 B | when qword `rcx+0x58` is non-null, calls `001B81B0(qword +8 of qword rcx+0x10, qword rcx+0x58, &{0x42, 02D34718, r9})` and returns its result if non-zero; does the same with qword `rcx+0x60` and the fifth (stack) argument in place of `r9` when both are non-null; then calls `005DC190(&local, r8, 0)`, stores `02D38000` at qword `rdx+0x80` when `r8` is non-null and bit 1 of its dword `+0xC` is set, else `02D37FE0`; then calls `0060D4F0(rdx, &local, 0)`, `0060DB50(rdx, 0)`, `005FEFD0(rdx, 0)`, `0060B980(rdx, qword 02D34710, &{008C6C98, rcx+0x30}, 0, dword rdx+0x220, 0)` and `00600A60(rdx, 0)` in order, stopping at the first non-zero result; finally calls `0016D6A0(&local)` and returns the last result | `00659AE2`, `00659B3D`, `00659B67`, `00659BDD`, `00659BF9` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-post-process-passes-and-their-shader-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001653B0` | 42 B | calls `00662A80(01F2E860)` and tail-jumps to `00808B90(008B0690)` | Interior anchor `001653BD`; Interior anchor `001653C4`; Interior anchor `001653CA`; Interior anchor `001653D5` |
| `001694E0` | 39 B | calls `005DBF60(02EA5838, 02EA5850)` and tail-jumps to `00808B90(008B7B80)` | Interior anchor `001694E4`; Interior anchor `001694EB`; Interior anchor `001694F2`; Interior anchor `001694F7`; Interior anchor `00169502` |
| `001EEC50` | 41 B | returns at once when `rcx` is null; otherwise tail-jumps to `0063ABF0` with (qword `01F82E50`, qword `[rcx]`) when byte `rcx+8` is 0, or with (qword `01F82E50`, 0) when it is non-zero | Interior anchor `001EEC53`; Interior anchor `001EEC55`; Interior anchor `001EEC65`; Interior anchor `001EEC71`; Interior anchor `001EEC73` |
| `0063AAD0` | 288 B | walks the list at `rcx+0x38` (next at node `+0`, the head read as the end, next taken before each visit) and, for each node `n` whose qword `+0x50` equals `rdx`, unlinks `n` (prev at `+8`) and points both its links at itself; when qword `rcx+0x78` (`t`) is non-null, follows the chain from qword `n+0x50` through qword `+0x78` and, for each element whose dword `+0xEC` is below dword `t+0x10` with bit 31 cleared (unsigned) and whose entry address `qword [t+0x18] + index*32` is non-zero, subtracts dword `n+0x70` from the entry's dword `+0x10` and decrements its dword `+0x14`, first unlinking and self-linking the link pair at `n+0x38` once; then calls `0063B3E0(n)`, `0063AAD0`+0xEC with `n+0x10` and `0063AAD0`+0xF9 with (`rcx+0x50`, `n`) | Interior anchor `0063AB27`; Interior anchor `0063AB3F`; Interior anchor `0063AB71`; Interior anchor `0063ABA1`; Interior anchor `0063ABB3` |
| `00793640` | 83 B | calls `0016D6A0(rcx+0x200)`, then calls `00793640`+0x3B with (`rcx+0x140`, 0x18, 8, `0016D6A0`), and tail-jumps to `005DDBA0(rcx)` | Interior anchor `00793657`; Interior anchor `0079365E`; Interior anchor `00793664`; Interior anchor `0079367B`; Interior anchor `0079368E` |
| `00877790` | 74 B | calls `0063BC00` with `rcx` = `02CB7080` (`rdx` unchanged) and returns its null result when it returns null; otherwise, when `rdx` is non-null, zeroes qwords `rdx+0` and `+0x30`, stores the result at qword `+0x18` and `rdx` itself at qwords `+0x20` and `+0x28`, and calls `00877790`+0x3D with `rdx`; on that path returns with `al` = 1 whether or not `rdx` was null | Interior anchor `008777A0`; Interior anchor `008777A8`; Interior anchor `008777BA`; Interior anchor `008777CD`; Interior anchor `008777D2` |
