# SD-63: the 703-byte body lays out the scene-wide shader constant buffer (OPUS, 2026-09-30)

Register row SD-63 was registered by SWE2-DATA (`how-a-class-registers-its-array-members-and-annotations.md` §9). It asks
what the 703-byte Presentation-side body that fetches the `PClassLayoutInterface` static lays out. That body rewrites
words `+0x08` / `+0x0A` of 24-byte records (`005FD320`–`005FD3A7`) and passes the interface to `005FD700` as its fifth
argument. This record is static. The checker is `sd63_scene_layout.py` (output `sd63_scene_layout.out`, `FAILS 0`).
It prints the table it reads and uses `Tools/analysis-kit/gfz-scripts/retool.py`.

## The answer (OPUS)

**The body (`005FD2A0`) builds Phyre's scene-wide shader parameter table and lays out its constant buffer.**

- **F1: the table.** It copies 23 source entries (16 bytes each at `00D3EB38`: a name pointer at `−8`, then two
  dwords) into 24-byte records at `02CB7DA8`:
  - the name, copied into a string pool at `02CBC390`;
  - the two dwords as bytes at `−6` / `−5`;
  - word `+0x08` cleared;
  - word `+0x0A` cut to its top 3 bits.

  The count `0x80000017` is stored at `02CB8448`.
- **F2: what the entries are.** They are the scene-wide shader parameters:
  - camera: `EyeDirWS`, `EyePosWS`, `Proj`, `View`, `ViewInv`, `ViewInvTranspose`, `ViewProj`;
  - clip planes and viewport: `NearFarPlane`, `NearTimesFarPlane`, `FarMinusNearPlane`, `FarMinusNearInv`,
    `AspectRatio`, `ViewportWidthHeight(Inv)`, `ScreenWidthHeight(Inv)`;
  - other: `GlobalAmbientColor`, `Time`;
  - resources: `DitherNoiseTexture`, `LowResDepthTexture`, `RWDeferredLightBuffer`, `RWCapturedTriangleBuffer`,
    `SceneWideParameterConstantBuffer`.

  Each has an index and a type code. The codes read consistently: 49 for every matrix, 3 for the two world-space
  vectors, 1 for the width/height pairs, 0 for scalars, 2 for the colour, and 52 for every texture and buffer. Those
  readings are interpretations of the codes.
- **F3: the layout.** `005FD700(8, [02CB8450], count, &size, PClassLayoutInterface)` computes the layout. The body
  rounds the size up to 16 and stores it at `02CB8458`, then allocates and zeroes a buffer of `size × (even instance
  count)` at `02CB8460`.
- **The rewrites.** Word `+0x08` is cleared before the layout call, as an offset field would be before it is
  assigned. That is an inference; `005FD700` is not read here.

**For modding:** these are the names a shader uses to read the camera, viewport, time and ambient values that the
engine uploads once per scene.

## Limits (OPUS)

- **`005FD700` itself** is not read. Which record field it writes the offsets into is inferred, not shown.
- **Type codes.** The codes' meanings are read from which names carry them, not from a code table.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
