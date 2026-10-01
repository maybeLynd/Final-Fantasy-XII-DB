# SD-64: the "non-class" names are string data of shader and material objects, not schema entries (OPUS, 2026-09-30)

Register row SD-64 was registered by SWE2-DATA ([the-file-schema-against-the-runtime-schema.md](../../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md)
section 7). It asks what the 27 non-class names among the file schema's 72 first-pass candidates are for, beyond
"shader-side identifiers". It also asks which file table carries each, and what reads them.

This record is a census of shipped data (tier 9) with a schema join. The checker is `sd64_names.py` (output
`sd64_names.out`, `FAILS 0`). It reads the 169 extracted `.phyre` files at `D:/FFXII MP Mod/extracted` and
`phyre-field-schema.tsv`.

## Method

The first pass's regex (`^P[A-Z]` over identifier-like runs) was not recorded, so its exact 27 cannot be
re-listed. This census uses a stricter, reproducible form:
- **The strings.** Every NUL-delimited string matching `P[A-Z]\w{2,}` that is neither a runtime class leaf nor a name
  in that file's own namespace pool (types, classes, members).
- **Where each sits.** The byte range of the instance list that holds it. Data after the namespace is laid out as the
  36-byte list headers, then, for each list, its objects (`m_objectsSize`) followed by its arrays (`m_arraysSize`).
- **C1, the control for that layout.** Under it, `c1004.dae.phyre`'s `PAssetReference` arrays hold asset ids
  (`…c1004.dae#LODNODE_0`) and its `PString` arrays hold node names (`s0_model`). The alternative order (all objects,
  then all arrays) puts shader parameter names in `PAssetReference`, which is incoherent.

## The answer (OPUS)

- **C2: no file table carries them.** 21 clean names survive, including every example section 3 gives (C3).
  - None of them is in any namespace pool: not the type table, not the class table, not the member names.
  - Every occurrence is array data of some instance list: string payload, not schema.
  - The 169-file first pass read them as "declared names" because it scanned whole files.
- **What they are, by owning object:**

| names | carried by | registered member holding the string (C4) |
|---|---|---|
| `PS2FogVec`, `PS2HSMatrix`, `PS2MatLight`, `PS2PLColor`, `PS2PLPos`, `PS2WHMatrix`, `PS2WHSMatrix`, `PS2ZBias`, `PS2ZBiasEnabled` / `Instance` / `NoGS` / `Original`, `PTAlphaThreshold` | `PShaderParameterDefinition` arrays: shader parameter names, sorted among `MaterialColour`, `NormalMapSampler`… | `PShaderParameterDefinition::m_name` (`PString`, `+0x08`) |
| `POSITION` | `PShaderStreamDefinition` and `PStreamInputDescD3D11` arrays: vertex input semantics, beside `TEXCOORD` | `PShaderStreamDefinition::m_name`, `PStreamInputDescD3D11::m_semantic` |
| `PS_Blur`, `PS_Combine`, `PS_BlendCombine`, `PS_BufferRender`, `PS_RenderRGBL` | `PShaderPassInfo` arrays in effect files (`sao.fx`): pixel-shader entry points, beside `FullScreenTriangle_VS` | `PShaderPassInfo::m_fragmentEntryPoint` (`PString`, `+0x08`) |
| `POSITION_MORPH`, `PROCEDURAL_TEXTURE_ENABLED` | `PMaterialSwitch` arrays: material switch names | `PMaterialSwitch::m_name` |

- **Inside compiled shaders.** The same parameter names and `POSITION` also occur, far more often, inside the arrays
  of `PShaderVertexProgram`, `PShaderFragmentProgram` and `PShaderGeometryProgram`. Those arrays hold the compiled
  shader blobs (`DXBC` sits beside them in `brightnessshader.fx`). The names there are read as the bytecode's own
  reflection tables. That reading is not decoded.
- **The first pass's fragments.** `PDXd`, `PINn` and `PY_` are not NUL-delimited strings. They are runs cut out of
  binary data, and the stricter form never produces them.

**What reads them:** the classes that own them, through registered `PString` members. So these are ordinary
reflected string fields: parameter, semantic, entry-point and switch names that the shader binding and material
code look up by name. The `PS2*` family is the PS2-emulation parameter set of the character shaders (world/HS
matrices, fog vector, point light, Z-bias variants). That family naming is an interpretation of the names.

**For modding:** these names are what a replacement shader or material must use for the engine to bind its
parameters, streams and passes. They live in the object data, not in the file's class schema.

## Limits (OPUS)

- **Not the same 27.** The first pass's exact 27 are not reproducible. This census gives 21 clean names plus the known
  fragment class.
- **Corpus.** The 169-file sample is used for placement. The whole-archive namespace census (`CW-4`) already shows
  these names are not schema names at archive scale. Their placement across all 35,984 files is not re-run.
- **Program blobs.** The reflection-table reading of the program arrays is not decoded.
- **The code that looks names up** (the parameter binding by name) is not traced here.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
