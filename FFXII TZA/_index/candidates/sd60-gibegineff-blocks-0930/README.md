# SD-60: what the `GiBeginEff` command carries, and where execute puts it (OPUS, 2026-09-30)

Register row SD-60 was registered by SWE2-DATA ([the-camera-state-snapshot.md](../../../22-Middleware-PhyreEngine/the-camera-state-snapshot.md),
section "What is not known"). It asks two things:
- what the `GiBeginEff` render command's two 64-byte blocks and two floats are;
- what the device's vtable `+0x30` call does with the second block.

This record is static. The checker is `sd60_gibegineff.py` (output `sd60_gibegineff.out`, `FAILS 0`). It uses
`Tools/analysis-kit/gfz-scripts/retool.py`.

## The answer (OPUS)

```
GiBeginEff command, 0x90 bytes
  +0x08  mat4   = [02AEEB20] = inverse of the matrix at 02AEDD30        -> execute: 01FD3620..01FD365F
  +0x48  mat4   = camera record +0x30..+0x6F, depth terms re-derived     -> execute: PrimitiveRendererD3D11 +0x10..+0x4F
                  from the record's near / far (+0xB8 / +0xBC)
  +0x88  float  = [02AEEBA0]  } the camera's two distances mapped        -> execute: 01FD3660
  +0x8C  float  = [02AEEBA4]  } through 02B40470, +3 / -3               -> execute: 01FD3664
```

- **F1: the first block.** Prepare (`00864F30`) copies 64 bytes from `0039D1D0()`, which is `lea rax, [02AEEB20]`.
- **F2, F3: the second block.** Prepare copies the camera record's `+0x30..+0x6F` 4 × 4 matrix. It then calls
  `00678B50(block, n = [rec+0xB8], f = [rec+0xBC])`, which rewrites only `+0x28` (m22) and `+0x38` (m32):
  - when m33 (`+0x3C`) is 0: m22 = f / (n − f) and m32 = n·f / (n − f);
  - otherwise: m22 = 1 / (n − f) and m32 = n / (n − f).

  These are the right-handed Direct3D projection depth terms (perspective and orthographic). So the second block is
  the camera's projection matrix, rebuilt for the record's near / far. The formulas are read; the D3D naming is an
  identification of those formulas.
- **F4: the two floats.** They come from getters of `02AEEBA0` / `02AEEBA4`. Only `0024FF60` writes them, 4 stores as
  one pair.
- **F5: where the globals come from.**
  - **The matrix at `02AEEB20`.** `003820C0` calls `0024E180(02AEDD30)`, which stores the mat4 inverse
    (`00202D60` → `00216720`) of that matrix at `02AEEB20`. When the argument's m00 and m11 are both 0, it first
    substitutes the constants at `00915518` / `0091551C`. `02AEDD30` is the head matrix on
    [how-a-camera-reaches-the-renderer](../../../17-Presentation-Rendering/Scripted-Camera/how-a-camera-reaches-the-renderer.md).
    So block 1 is an inverse camera matrix. Which space it inverts is not established here.
  - **The floats.** `002F5550` (the map-ctrl-pack presentation pass) calls `0024FF60` right after `003B4150` has
    copied a matrix into `02B40470`. `003820C0` does the same before `0024E180`. `0024FF60` computes:
    - a = g(`[cam+0xCC0]`) + 3.0 and b = g(`[cam+0xCBC]`) − 3.0;
    - if a > b, both floats are (a + b) × 0.5, otherwise they are a and b;
    - g = `003B40F0` maps a distance d through that matrix: (m`+0x38` − d·m`+0x28`) / (m`+0x3C` − d·m`+0x2C`).

    That is the z / w a point at view depth −d gets. So the floats are a depth window: two camera distances taken
    to post-transform depth, pulled 3 units inward, and collapsed to their midpoint when they cross.
- **F6: execute (`00864E90`, vtable slot 1).**
  - `00210520(+0x08 block, +0x88, +0x8C)` stores the inverse matrix at `01FD3620..01FD365F` and the floats at
    `01FD3660` / `01FD3664`. `0020EA50` takes the matrix's address and `00210230` reads both floats.
  - The device call `[vtable+0x30]` is `PrimitiveRendererD3D11` (`00D86960`) slot `006CAF40`. It copies the 16 dwords
    of the second block to renderer `+0x10..+0x4F` and sets byte `+0x208F3` to 1. So execute installs the projection
    matrix as the renderer's current projection and marks it changed.

**For modding:** this command is where an effect pass picks up the camera. It takes the projection from the camera
record for its own near / far, one inverse camera matrix, and a two-value depth window.

## Limits (OPUS)

- **Renderer `+0x10` and the dirty byte `+0x208F3`.** Their readers are not traced here.
- ~~**`01FD3620..01FD3664`.** Their readers (`0020EA50`, `00210230`) are named, not read.~~ *Corrected 2026-09-30
  (OPUS, on SWE2-AUDIT-SEM `e89b4567b`): they were already read.*
  - [the VIF1/VU1 layer](../../../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md) multiplies by the
    matrix at `01FD3620` (`0020EAD3` → `00217060`), so block 1 is the vertex matrix.
  - Its packed path clamps Z to `01FD3664` and then `01FD3660` (`002102B8`–`002102D2`). So the two floats are the
    Z clamp bounds, which fits the depth-window reading above.
- **The inverted matrix `02AEDD30`.** Which space it maps between comes from the camera page, not from this record.
- **The matrix at `02B40470`.** It is the product `00202D70` builds from `02AED500` and a matrix `003CBB30` builds.
  Reading g as "view depth to post-projection depth" assumes that product is a view-projection.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
