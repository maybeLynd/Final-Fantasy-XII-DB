# RenderContext02CC0410: a type for the render singleton (OPUS, 2026-09-27)

**State: PENDING REVIEW.** This is board task OPUS-STRUCT-RENDER-CONTEXT-02CC0410. The control passing is not
acceptance.

**Question.** Fourteen pages cite the magic static at `02CC0410` (`005FD050`): its `+0x108` device and its `+0x18C0`
primitive renderer. The store had no type for it. What does its own code establish?

**Result** (`render_check.py`, static, certified EXE):

| check | observation |
|---|---|
| R1 | `005FD050` constructs `02CC0410` once with `00615840` and returns it; `00624670` jumps to `005FD050`. |
| R2 | `00615840` zeroes `+0x108 / +0x110 / +0x118`, builds PTexture2DD3D11 objects in place at `+0x170` and `+0x2F8` (memset `0x188`, then `006160B0`), sets `+0x184C := 1`, and builds the `+0x18C0` subobject (`006C8750`). |
| R3 | `00625830` fills `+0x120` as the DXGI_SWAP_CHAIN_DESC it passes to D3D11CreateDeviceAndSwapChain, and passes ppSwapChain = `+0x118`, ppDevice = `+0x108` and ppImmediateContext = `+0x110`. |
| R4 | `+0x168` is the feature level the device was created at: `pFeatureLevel` is `rsp+0x60` (`00625A32` / `00625A37`), copied to `+0x168` at `00625B0C` and compared with `0xB000` (11_0) at `00625DE3` and by the deferred-lighting pass. |
| S | Regression: the type exists (`AT LEAST 0x18C0`) with rows tiling to `0x18C0`. S FAILED before the declaration. |

**Details of R3:**
- The description is zeroed as nine qwords.
- The buffer count comes from `+0x184C`; the format is `0x1C`; the refresh rate is `0x3C/1`, then adjusted by
  `00623320`, with `+0x18A4` := numerator / denominator.
- Usage is `0x20`, the window goes in `+0x30`, windowed is 1, and flags are 2.

**Extent.**
- At least `0x18C0`: the subobject at `+0x18C0` writes to at least its own `+0x880`.
- At most `0x22200`: the next statically referenced address is `02CE2610`, `005FD050`'s init guard.
- The teardown is `008ADDD0`, registered with atexit.

**Not claimed.** The base region (`005DC0E0`), the constructor-initialised middle (`+0x480..+0x184B`), the roles of the
two textures, and the type of the `+0x18C0` subobject. The input page calls that subobject a PrimitiveRendererD3D11;
it is not typed here.

Affected: none of the pages is edited. They already cite the addresses this type now anchors (gi-render-command-family
§20, the input stack page).

| consumer | action | agreement |
|---|---|---|
| `_types/types.tsv` / `fields.tsv` RenderContext02CC0410 | declared, 14 rows | revised-here |
| `17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md` §20 (`[ctx]` = `02CC0410`) | consistent | agrees |
| `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md` (`02CC0410 + 0x18C0`) | consistent | agrees |
| d3d11-buffer-element E1 (274e8decc) | the same `+0x108` / `+0x110` | agrees |

**Run receipt.** Run verified at 4be7a78ed: `render_check.py` R1–R4 and S PASS, FAILS 0. S FAILED before the
declaration.

## The +0x520..+0x82F span, from its objects' creators and teardown (OPUS, 2026-09-28)

[`render_buffers.py`](render_buffers.py) ([output](render_buffers.out)), checks D, V, U, P, R and W: FAILS 0. W failed before the
patch.

**How the span was found.** The census seeded from the context's getter `005FD050` reaches 6 displacements. Seeded from its
`jmp` alias `00624670`, which has 25 of the 111 call sites, it reaches 526. The teardown `0062B5A0` (reached at `0079F079` through
the alias) and the initialiser `00625CC0` give each object its routines. The census over-projects the release loops past their
two iterations, so the bodies were read by hand.

| context offset | type | what it is (creator / release) |
|---|---|---|
| +0x520, +0x548 | RenderContextRecord28 | `005DBF30`; set by `00607D10` (u32, u32, pointer); `00604B82` reads the pair as floats |
| +0x570 | RenderContextRecord18[8] | the vector constructor iterator with `005DC1B0` |
| +0x6F8 / +0x700 | uint32 / void* | the count and pointer of an array of 0x30-byte records. It is resized by `0061CE30`; bit 31 of the count marks it not owned |
| +0x708 | RenderDynamicBuffers58 | `00624F70`: 2 dynamic vertex + 2 index ID3D11Buffer, the sizes, 16-aligned CPU copies / `0062B430` |
| +0x760 | RenderUavBuffers58 | `00625210` → `006250C0`: the same header with bind \| 0x80 and misc 0x20, plus raw R32 UAVs / `0062B4E0` |
| +0x7B8 | void* | a COM object the teardown releases |
| +0x7C0 / +0x7D0 | float[4] / float | 0.1, 0.1, 0.8, 0.5 (`00625408`) / 1.0 (the constructor) |
| +0x7D8 | RenderPrimitivePass1E8 | `00624980`: vertex buffer, input layout, constant buffer, a vertex and three pixel shaders / `0062B290` |
| +0xF4..+0x103 | uint32 x 4 | the sizes the initialiser passes to the two buffer creators (0 = 0x400000 / 0x100000) |

**The pass state at +0x830 moved into the +0x7D8 object, as its +0x58.** `0062B290` receives the context's +0x7D8 and releases
its own +0x58 with `0062BA30`, the pass-state release. So the object is 0x1E8 bytes and ends at +0x9C0, where the second pass
state begins; the teardown releases that second one directly. The row `passState830` is now `RenderPrimitivePass1E8.passState`.
`render_substates.py` W accepts that successor.

**Not claimed:**
- what the 0x28 and 0x18 records and the +0x630 object are;
- what the 0x30 array elements hold;
- what the +0x7C0 floats tune;
- each shader's role.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` RenderContext02CC0410 `unobservedSpan0520` (784 B), `passState830`, `unobservedSpan0000` (264 B) | carved into 20 rows; `passState830` re-homed as `RenderPrimitivePass1E8` +0x58; +0xF4..+0x103 split out, with history in evidence | revised-here |
| `_types/types.tsv` | five types added (RenderContextRecord28, RenderContextRecord18, RenderDynamicBuffers58, RenderUavBuffers58, RenderPrimitivePass1E8) | revised-here |
| `render_substates.py` W (the `passState830` row) | successor clause added; its output is unchanged | revised-here |
| `gi-render-command-family.md` §20, the input-stack page | cite the context and +0x18C0, not this span | agrees |

**Run receipt:** `render_buffers.py` FAILS 0. `render_substates.py`, `render_primitive.py`, `render_batch.py` and `render_check.py`
each FAILS 0. `types_index.py --validate`: 0 errors. `check_ctype_widths.py` 0; `check_type_refs.py` 0 dangling.
`check_embed_parent_fields.py` 0 disagreements. `check_route_ctype_agreement.py`: 0 new.

## +0x1820..+0x18BF: sampler, viewport, DXGI adapter and output (OPUS, 2026-09-28)

[`render_present.py`](render_present.py) ([output](render_present.out)), checks S, M, M2, V, A, F and W: FAILS 0. W failed
before the patch.

**Which census hits were kept.** The rows come from the alias-seeded census, keeping only instructions whose displacement is
the context offset itself. The census also projects the +0xB50 pass-state loop (`00624E95`) one iteration too far, onto
+0x1820..+0x187C, and those projected hits were discarded.

| offset | row | evidence |
|---|---|---|
| +0x1820 | `sampler1820` PSamplerStateD3D11 | `005DC400` then +0x20 cleared: the body of its constructor `00615CD0` and of its descriptor's placement constructor `006135E0` (vtable `00D500E8`). `0061D9C0` creates the sampler (CreateSamplerState). The teardown matches its destroy `006132E0` |
| +0x1848 / +0x1849 | mode bytes | `0062AAB0` modes 0 / 1 / 2 give 0 / 1 / 0x101, with +0x184C |
| +0x1850 | `initClock` double | `clock()` at initialisation |
| +0x185C..+0x1870 | viewport origin, width, height; target width, height | the resize writes. `0061D3D0` flips the viewport against +0x1870, then calls RSSetViewports |
| +0x1878 / +0x1880 | `dxgiFactory` / `dxgiAdapter` | EnumAdapters / EnumOutputs; the teardown releases both |
| +0x1890 | `fullscreen` | GetFullscreenState on +0x118 |
| +0x1894 / +0x1898 / +0x18A0 | output index / HMONITOR / mode count | `006242C0` |
| +0x18A8 / +0x18AC / +0x18B0 | `value18A8` / `adapterIndex` / `adapterMask` | `006278DD` (8 / `0017ECE0()`) / the adapter scan |

**Not claimed:** what modes 0, 1 and 2 select, and what +0x18A8 means.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` RenderContext02CC0410 `unobservedSpan1820` / `1850` / `18A8` | carved into 23 rows, with history in evidence | revised-here |
| `render_substates.py` docstring (the +0x1820 object not claimed) | now claimed here; its checks are unaffected | agrees |

**Run receipt:** `render_present.py` FAILS 0. `render_buffers.py`, `render_substates.py`, `render_primitive.py`, `render_batch.py`
and `render_check.py` each FAILS 0. `types_index.py --validate`: 0 errors. Width, reference, embed and route checks: 0.

## +0x000..+0x0F3: the region 005DC0E0 initialises (OPUS, 2026-09-28)

[`render_base.py`](render_base.py) ([output](render_base.out)), checks C, S, V and W: FAILS 0. W failed before the patch.

`005DC0E0` has one caller, the context's constructor at `00615863`, so the rows stay the context's and no base class is
claimed.

- **Byte +0 routes the requested buffer sizes** (`0079E4A0`, one 16-byte store at +0xF4):
  - non-zero: the dynamic pair +0xF4 / +0xF8 gets them;
  - zero: the UAV pair +0xFC / +0x100 gets them.

  The other pair keeps 0, which its creator reads as the default.
- **Byte +1 is set when the initialiser `006253D0` succeeds.** `0079F070` tests it before calling the teardown.
- **Eight more RenderContextRecord18 sit at +0x08.** They have the same element constructor, `005DC1B0`, as the +0x570
  array.
- **+0xE8 / +0xF0 copy the +0x700 array pointer and its count.** `0061CE30` stores them when the count is unchanged.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` RenderContext02CC0410 `unobservedSpan0000` (244 B) | carved into 13 rows | revised-here |
| `_types/types.tsv` RenderContextRecord18 instance | now sixteen: at +0x08 and +0x570 | revised-here |

**Run receipt:** `render_base.py` FAILS 0; the six other render-context records FAILS 0; the store validators 0.

## PrimitiveRendererD3D11's four spans: pending state, the frame latch, setters (OPUS, 2026-09-28)

[`render_primitive_state.py`](render_primitive_state.py) ([output](render_primitive_state.out)), checks L, S, M and W: FAILS
0. W failed before the patch.

**Source.** The renderer's vtable census (`00D86960`), keeping only instructions whose displacement is the field itself.

- **L: the frame latch `006C8920`.** It copies 49 pending fields into the copy the draw path reads, then clears the dirty bytes
  +0x208F1 and +0x208F3. The check derives the map from the body itself.
  - +0x10..+0x8C are copied to +0x20868..+0x208E4.
  - +0x1A0..+0x1B8 are copied to +0x1C0..+0x1D8.
  - The pending bytes and dwords at +0x2089x..+0x209xx go to their latched slots.
  - The 16-byte rect +0x20900 goes to +0x20910.
- **S: the setters, by vtable slot.**
  - 6: the 0x40 block at +0x10.
  - 8: the vec4 at +0x50, the pair at +0x60, the flag at +0x68, the float at +0x6C and pointers at +0x1A0..+0x1B0.
  - 9: +0x70 / +0x74.
  - 10: +0x1B8.
  - 11: +0x208E8 / +0x208EC.
  - 12: +0x855.
  - 15: +0x7C.
  - 26: +0x1E8 / +0x1EC.
  - 7: +0x860 / +0x868.
  - 32: the scissor rect +0x20900 = {x, y, x + w, y + h} with its enable byte +0x20920.
  - Non-virtual: `006CAC30` writes +0x851 / +0x852, and `006CAE70` writes +0x80 / +0x84.
- **M: the pointer pair.** `006C8920` picks +0x190 / +0x198 from four pointer pairs by +0x851 / +0x852.

**Not claimed:**
- what the block, the vec4 and the bytes hold;
- the D3D11 objects behind the qwords. They stay uint64 because no dereference is cited.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` PrimitiveRendererD3D11 `unobservedSpan00010` / `000C8` / `00848` / `20868` | carved into 110 rows, with history in evidence | revised-here |

**Run receipt:** `render_primitive_state.py` FAILS 0. The seven other render-context records each FAILS 0. The store validators: 0.
