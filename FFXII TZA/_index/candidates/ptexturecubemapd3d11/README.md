# PTextureCubeMapD3D11 past its base, and its 0x40-byte element (OPUS, 2026-09-27)

**State: PENDING REVIEW.** This follows the PTexture2DD3D11 carve with the same method. It is a separate class with its
own element; the 2D layout was not assumed to carry over. The control passing is not acceptance.

| check | observation |
|---|---|
| C0 | Slot 10 of `PClassDescriptorConcrete<PTextureCubeMapD3D11>` (vtable `00D51E90`) is `00612D00`, which calls `006161A0` on the object. |
| C1 | `006161A0` clears the count at `+0x30`, resizes it to one element (`00627800`), and zeroes `+0x78..+0xA7`. |
| C2 | `00627800` is the PSharray resize shape. Its allocator `0061CFA0` has stride `0x40` and builds qwords at `0x00`–`0x18`, a dword at `0x20`, and the `TAsyncUpdate<PTextureCubeMapD3D11>` vtable `00D54358` at `+0x28`. |
| C3 | The device, per element (index << 6): CreateTexture2D into `+0x00` (`00620630`), an SRV into `+0x08` (`0061FC50`), a UAV into `+0x10` (`00620E10`). Element 0's texture reports its description into the class's `+0x78`. |
| C4 | The scheduler `0062C820` writes element `+0x30` := the cube map and `+0x38` := the index, and queues element `+0x28`. |
| C5 | `+0xA4` is the resources-created flag. `0061E2E0` stores 1 after the creator `00620630`, the release `0062C100` stores 0, and `00625F20` tests it before the deferred-lighting release routes to `0062C100`. |
| S | Regression: the rows and the element type exist and tile. S FAILED before the carve. |

**In the store:**
- **PTextureCubeMapD3D11:**
  - `+0x30` is a 72-byte `elements` row, `PSharray<TextureCubeMapD3D11Element>`, identified by the access and resize
    rule.
  - `+0x78` is `textureDesc`, 44 bytes.
  - `+0xA4` is `resourcesCreated`.
  - `+0xA8..+0x34F` stays DISCOVERED and holds the old row's text verbatim.
- **TextureCubeMapD3D11Element (`0x40`):** `texture`, `shaderResourceView`, `unorderedAccessView`, `asyncUpdateVtable`,
  `asyncUpdateCubeMap` and `asyncUpdateIndex`. Three spans (20 bytes) stay DISCOVERED.

**Not claimed:** the class tail, element `+0x18` / `+0x20`, and what the textures hold.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` PTextureCubeMapD3D11 | 800-byte span carved | revised-here |
| `_types/types.tsv` PTextureCubeMapD3D11 `ctor`; new TextureCubeMapD3D11Element | declared | revised-here |

**Run receipt.** Run verified at 513baa66d: `cube_check.py` C0–C5 and S PASS, FAILS 0. S FAILED before the carve.
