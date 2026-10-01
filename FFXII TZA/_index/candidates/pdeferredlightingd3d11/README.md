# PDeferredLightingD3D11's own tail (OPUS, 2026-09-27)

**State: PENDING REVIEW.** This is board task OPUS-STRUCT-PDEFERREDLIGHTINGD3D11. The class's `0x158` bytes past
PDeferredLightingBase were one unobserved span. The control passing is not acceptance.

| check | observation |
|---|---|
| L0 | The class descriptor's slot 10 (`006414F0`) calls the constructor `00645BC0`. It installs the class vtable, zeroes 42 qwords, and sets word `+0x4308 := 1`. |
| L1 | `+0x41D8..+0x4238` are 13 record pointers. The destructor releases each through `006505A0`, which dispatches on record byte `+8`: 0 → PTexture2DD3D11, 1 → PTexture3DD3D11, 2 → PTextureCubeMapD3D11. `0065C330` resizes the group the mode dword `+0x4114` selects (3 / 4 / 6 records). |
| L2 | `+0x4240` / `+0x4248` are owned PConstantBufferD3D11 objects (`0x50`). `+0x4250` / `+0x4258` / `+0x4318` / `+0x4320` are owned PStructuredBufferD3D11 objects (`0x68`). |
| L3 | `006568D0` stores 22 named effect-parameter handles (`0018D240(effect, name)`), from "ColorBuffer" at `+0x4260` through "RWScatteredLightingOutputBuffer" at `+0x4300`, plus "DeferredLightCount" at `+0x4328`. |
| L4 | `+0x4308` is ANDed with "device feature level ≥ 11_0" (`[02CC0410+0x168] >= 0xB000`). |
| S | Regression: the tail rows exist and tile. S FAILED before the carve. |

**How the classes in L2 were identified.** Each creation site's constructor issues exactly the same stores as the class
descriptor's own constructor: `00615550` = `00611D60`, and `00616060` = `006127C0`. The allocation sizes match too. The
two releases' gate flags are those classes' `+0x48` and `+0x60`.

**What stays open.**
- `+0x430A` (6 bytes) and `+0x4310` (the pointer `0064A000` returns) stay DISCOVERED.
- `+0x4309` is recorded as a byte cleared after a successful rebuild; its other values are not established.
- The parameters' shader-side use is not claimed.

**Depends on** the texture carves: PTexture2DD3D11, PTexture3DD3D11 and PTextureCubeMapD3D11 (the record kinds), and the
render-context `+0x168` feature level.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` PDeferredLightingD3D11 | 344-byte span carved into 33 rows | revised-here |

**Run receipt.** Run verified at be07cd1aa: `dl_check.py` L0–L4 and S PASS, FAILS 0. S FAILED before the carve.
