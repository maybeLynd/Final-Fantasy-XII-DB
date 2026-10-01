# PTexture3DD3D11 past its base, and its 0x28-byte element (OPUS, 2026-09-27)

**State: PENDING REVIEW.** This is the third texture class, found as record kind 1 of the deferred-lighting release
(`006505A0`). It has its own element; neither the 2D nor the cube layout was assumed. The control passing is not
acceptance.

| check | observation |
|---|---|
| D0 | Slot 10 of `PClassDescriptorConcrete<PTexture3DD3D11>` is `00611340`. It runs the base `005DCC10`, clears the count at `+0x38`, resizes to one (`00627750`), and zeroes `+0x68..+0x8F`. |
| D1 | The allocator `0061CF20` has stride `0x28` and zeroes qwords at `0x00`–`0x18` and a dword at `0x20`. The element has no async-update object. |
| D2 | The device creates, per element (index × 5 × 8): CreateTexture3D into `+0x00`, with element 0's GetDesc into the class's `+0x68` (`00620250`); an SRV into `+0x08` (`0061FAF0`); a UAV into `+0x10` (`00620CB0`). |
| D3 | `+0x8C` is the resources-created flag. It is set to 1 after `00620250`, set to 0 by the release `0062BF40`, and tested by `00625F10` before the deferred-lighting release routes to `0062BF40`. |
| S | Regression: the rows and the element type exist and tile. S FAILED before the carve. |

**In the store.**
- PTexture3DD3D11 now has `elements` (48 bytes), `textureDesc` (36) and `resourcesCreated` (4). They tile the class
  exactly, so no DISCOVERED span is left in it.
- The new Texture3DD3D11Element (`0x28`) has `texture`, `shaderResourceView` and `unorderedAccessView`; 16 bytes stay
  DISCOVERED.
- The old 88-byte row's text is kept verbatim in the `elements` row.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` PTexture3DD3D11 | 88-byte span carved | revised-here |
| `_types/types.tsv` PTexture3DD3D11 `ctor`; new Texture3DD3D11Element | declared | revised-here |
| OPUS-STRUCT-PDEFERREDLIGHTINGD3D11 | record kind 1 = PTexture3DD3D11 (kinds 0 / 2 = 2D / cube) | input to that task |

**Run receipt.** Run verified at 6876a9d69: `tex3d_check.py` D0–D3 and S PASS, FAILS 0. S FAILED before the carve.
