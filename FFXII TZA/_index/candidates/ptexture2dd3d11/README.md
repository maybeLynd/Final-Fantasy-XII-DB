# PTexture2DD3D11 past its base, and its 0x58-byte element (OPUS, 2026-09-27)

**State: PENDING REVIEW.** This is board task OPUS-STRUCT-PTEXTURE2DD3D11. The control passing is not acceptance.

**Question.** PTexture2DD3D11 (`0x188`) was its `0x30`-byte base plus one 344-byte unobserved span, and reflection
registers no member for the class. What does the code put there?

**Result** (`texture_check.py`, static, certified EXE):

| check | observation |
|---|---|
| T0 | `006160B0` is the class's constructor: slot 10 of `PClassDescriptorConcrete<PTexture2DD3D11>` (vtable `00D51510`, named by RTTI) is `006123F0`, which calls it on the object. |
| T1 | The constructor sets `+0x30 := 1`, builds one element in place at `+0x38` (qwords `+0x38..+0x68`, dword `+0x70`, the `TAsyncUpdate<PTexture2DD3D11>` vtable `00D54348` at `+0x78`), and zeroes `+0x90..+0xBF`. |
| T2 | The element copy `00613770` has stride `0x58`. It moves qwords at `0..0x30`, a dword at `0x38`, the vtable at `0x40`, a qword at `0x48` and a dword at `0x50`; it never touches `0x3C` or `0x54`. |
| T3 | `+0x30` follows the PSharray rule. Every walker strips bit 31, takes the address `+0x38` at count one and `[+0x38]` above one, and indexes elements at `0x58`. |
| T4 | The device (`[02CC0410+0x108]`) creates, per element: a texture with initial data into `+0x00` and one without into `+0x08` (`+0x28`, CreateTexture2D); shader-resource views on each into `+0x10` / `+0x18` (`+0x38`); an unordered-access view into `+0x20` (`+0x40`). Element 0's texture reports its description into the class's `+0x90` (vtable `+0x50`). |
| T5 | The scheduler `0062C360` writes element `+0x48` := the texture and `+0x50` := the index, and queues element `+0x40` through `0062EB90`. |
| T6 | `+0xBC` is the resources-created flag. `0061E200` stores 1 after the creator `0061FDA0`, the release `0062BCB0` stores 0, and `00625F00` tests it before the deferred-lighting release routes to `0062BCB0`. |
| S | Regression: the class rows and the element type exist and tile their extents. S FAILED before the carve. |

**In the store:**
- **PTexture2DD3D11:**
  - `+0x30` is a 96-byte `elements` row, `PSharray<Texture2DD3D11Element>`. The template identity rests on the access
    rule, not on a registration.
  - `+0x90` is `textureDesc`, 44 bytes.
  - `+0xBC` is `resourcesCreated`.
  - `+0xC0..+0x187` stays DISCOVERED and holds the old row's text verbatim.
- **Texture2DD3D11Element (new, `0x58`):** `texture`, `secondTexture`, `shaderResourceView`,
  `secondShaderResourceView`, `unorderedAccessView`, `asyncUpdateVtable`, `asyncUpdateTexture` and `asyncUpdateIndex`.
  Four spans stay DISCOVERED.

**Not merged.** `00620E10` walks a different class at stride `0x40`, and `00620F60` works on a descriptor object; neither
is read into this type.

**Not claimed.** The roles of `+0x28` / `+0x30` / `+0x38` inside the element, the class tail, and what the textures
hold.

Also revised in the store: the type's `ctor` names `006160B0`. No page restates this layout.

Affected: `_index/candidates/d3d11-buffer-element/README.md`: its DISCOVERED byte count, corrected from 24 to 28 (20 + 4 + 4). The commit message and board note of 274e8decc said 24.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` PTexture2DD3D11 | 344-byte span carved | revised-here |
| `_types/types.tsv` PTexture2DD3D11 `ctor`; new Texture2DD3D11Element | declared | revised-here |
| `_types/types.tsv` RenderContext02CC0410 `+0x170` / `+0x2F8` (next package) | embeds this type | agrees |

**Run receipt.** Run verified at a7e1a1f8e: `texture_check.py` T0–T6 and S PASS, FAILS 0. S FAILED before the carve.
