---
title: "Phyre D3D11 device and resources: device and swap-chain creation, the texture formats, texture and buffer objects and how they are mapped, uploaded and released"
kind: "system"
category: "PhyreEngine"
addresses: "0x00625830, 0x00623320, 0x00624F70, 0x006250C0, 0x00625210, 0x00623B10, 0x0061ECD0, 0x00626D90, 0x0062CD40, 0x00616210, 0x02CF7A30, 0x0061FDA0, 0x00620250, 0x00620630, 0x0061E200, 0x0061E270, 0x0061E2E0, 0x00650660, 0x00628100, 0x0060DD70, 0x0060DE00, 0x00610990, 0x006264F0, 0x00626990, 0x00609870, 0x00609950, 0x0062C820, 0x0062BCB0, 0x0062BF40, 0x0062C100, 0x006505A0, 0x005DDBB0, 0x00615550, 0x0061D960, 0x00626060, 0x006097B0, 0x0062C300, 0x006239C0, 0x00616060, 0x0061F200, 0x0061F710, 0x006209C0, 0x0061C080, 0x00615790, 0x00607FA0, 0x005F0590, 0x00623F00, 0x005D8E40"
---

## What the player sees

The window the game draws into, its back buffer and depth buffer, and every texture and constant
the shaders read are made by the code on this page. The swap chain is created windowed, in
`R8G8B8A8_UNORM`, with the refresh rate of the screen's current mode, and the device is refused
unless the adapter reaches Direct3D feature level 11.0.

## How it works

### Building the render context

`0x005FD050` constructs the render context, the static `0x02CC0410`, with `0x00615840` the first time it is
asked for it. Among the members it builds are the back-buffer texture at `+0x170` and the depth texture
at `+0x2F8` (each zeroed and set up by `0x006160B0`), and the colour and depth render targets at
`+0x480` and `+0x4D0`. `0x005DC1C0(target, texture)` attaches a target to its texture: it stores the
texture at `+0x00`, sets bit `0x100` of the texture's `+0x18` and points the texture's `+0x20` at the
target unless another live target already holds it.

When a member's constructor throws, the unwind actions of `0x00615840` destroy what has been built:

- `0x00616740` for each render target: `0x0062B890` when its `+0x18` or `+0x28` is set, which releases the
  views in its two arrays and the four interfaces at `+0x10`–`+0x28`, then `0x005DDB00`, which frees the
  arrays' storage;
- `0x00616520` and `0x00616780` for the eight `0x18`-byte records at `+0x08` and at `+0x570`, whose element
  destructor (`0x0016D6A0`) does nothing.

The context's destructor `0x00616560` runs the same steps among its own.

### Creating the device and swap chain

`0x00625830(context, width, height, samples, …, hwnd)` runs after the adapter is chosen (see the
adapter page under Related). It works on the render context, the static object `0x005FD050` returns.

1. It probes the adapter at context `+0x1880` with `D3D11CreateDevice` (driver type 0, no flags,
   SDK version 7, no device kept) and returns 9 unless the reported feature level is `0xB000` or higher.
2. It fills the `DXGI_SWAP_CHAIN_DESC` at context `+0x120` (layout below): the given size, format
   `0x1C`, refresh rate 60/1, the sample count clamped to 1–16, usage `0x20` (render-target output),
   the buffer count from `+0x184C`, the window, windowed, swap effect 0 and flag 2 (allow mode switch).
3. `EnumDisplaySettingsA` reads the current mode, and `0x00623320` replaces the refresh rate with that
   of the mode matching the screen size; `+0x18A4` takes the rate as a whole number and the values are logged
   (`Init Fresh rate x = %d, y = %d %d  get fresh = %d`).
4. `D3D11CreateDeviceAndSwapChain` is called with the levels `0xB000`, `0xA100`, `0xA000` and no flags;
   it stores the swap chain at `+0x118`, the device at `+0x108`, the immediate context at `+0x110`
   and the level at `+0x168`. A failure is logged (`R != S_OK %d!`, `m_d3dDevice error!!` and the like)
   and returns 9.

Then it:

- calls the factory's `MakeWindowAssociation` (`+0x40`) with flag 1 (no window changes);
- queries the device for `ID3D11Debug` and, when that succeeds, that interface for `ID3D11InfoQueue`;
- takes back buffer 0 with `GetBuffer` (`+0x48`) into the ring of the `PTexture2D` at `+0x170`, reads
  its description into `+0x200`, and gives that texture the `RGBA8` format `0x02CF7480` and the buffer's size;
- sets up the colour render target at `+0x480` and the depth render target at `+0x4D0`
  (`0x00620F60`), with the sample count at their `+0x09` (0 for one sample), and sizes the depth
  texture at `+0x2F8` as `DEPTH24S8` (`0x02CF79C0`) with `0x0060DD70` and `0x00610990`.

It then sets the viewport (`0x0061D3D0`), builds the helpers at `+0x7D8` (`0x00624980`), `+0xB50`
(`0x00624C30`) and `+0x18C0` (`0x006C9CD0`), stores the start `clock()` at `+0x1850`, creates the two
upload-buffer pairs below, and on feature level 11.0 a 16-byte indirect-arguments buffer at `+0x7B8`
(misc flag `0x10`). It binds the colour and depth views with `OMSetRenderTargets` (`+0x108`), the
multisampled ones when the sample count is above 1, creates the default sampler at `+0x1820`
(`0x0061D9C0`) and finally probes the multisample levels (`0x00628690`).

### The screen refresh rate

`0x00623320(context, &rate, width, height)` creates a DXGI factory, takes adapter 0 and its output 0,
and asks `GetDisplayModeList` (`+0x40`) for format `0x1C`. Every listed mode whose width and height
equal the arguments copies its 8-byte refresh rate into `rate`, so the last match wins. With no match
the rate stays 60/1.

### The upload buffer pairs

The context holds two 0x58-byte pair objects, each with two vertex buffers and two index buffers
used alternately (layout below):

- `0x00624F70(pair, device, vbSize, ibSize)` at `+0x708`, sizes from `+0xF4` and `+0xF8`: dynamic
  buffers with CPU write access, a vertex size of 4 MiB and an index size of 1 MiB + 16 when the
  argument is 0, plus a 16-byte-aligned main-memory copy of each.
- `0x00625210(pair, device, …)` at `+0x760`, sizes from `+0xFC` and `+0x100`, goes through `0x006250C0`
  with default usage and bind flag `0x80` added, which also makes the buffers raw (misc `0x20`). It
  then creates an unordered-access view of each: raw views (`R32_TYPELESS`, one element per 4 bytes,
  flag 1) for raw buffers, one element per stride for structured ones.

`0x00626D90(context, i)` makes slot `i` current (`+0x6F0`) and zeroes its used sizes in both pairs.
`0x0061ECD0(context, i)` uploads slot `i` of the first pair through `0x00623B10`: each non-empty
buffer is mapped with `WRITE_DISCARD` and its used bytes are copied from the main-memory copy; 9 on a
failed map.

### Texture formats

A texture names its format through a pointer at `+0x00` to one of 35 static format objects
(`0x38` bytes). Each is built before `main` by its own initialiser, which calls `0x00616210(object,
name, code, flags, five DXGI formats)`; `0x00616210` runs `0x0062CD40` and stores the five formats at
`+0x20`–`+0x30`. `0x0062CD40` stores the name and code and derives from the code:

- the bits per pixel at `+0x14`, from a switch over the code;
- the flags at `+0x18`: the argument's bits outside `0x7E07`, a channel mask from the same switch,
  bit 0 for the block-compressed codes `0x0F`–`0x18` and `0x1D`, bit 1 for the depth codes
  `0x28`–`0x2B` and `0x31`, bit 2 for the float codes `0x1E`–`0x27`.

`0x02CF7A30` (code `0x33`, no bits, no flags) is the null format a texture starts with. The table under Layouts lists all 35.

### Texture objects

The three D3D11 texture classes keep a ring of Direct3D textures in a `PSharray`, like the data
blocks of the draw page, and a word that is non-zero while the ring is created:

| Class | Size | Ring (count, data) | Record | Created word |
|---|---|---|---|---|
| `PTexture2D` | `0x188` | `+0x30`, `+0x38` | `0x58` | `+0xBC` |
| `PTexture3D` | `0x90` | `+0x38`, `+0x40` | `0x28` | `+0x8C` |
| `PTextureCubeMap` | `0x350` | `+0x30`, `+0x38` | `0x40` | `+0xA4` |

Setting the size records the format, width, height (and depth) and mip count and recomputes the level
count at `+0x14`: `0x0060DD70` for 2D and `0x0060DE00` for 3D. Both return 3 when the larger side is
below `1 << mips`, and with bit 1 of `+0x18` (generate mips) the level count is the base-2 logarithm
of the largest side. `0x00610990` recomputes `+0x14` alone. `0x005DCC10` is the 3D base initialiser:
format `0x02CF7A30`, `+0x08` = `0x300`, `+0x18` = 2.

### Creating textures

`0x0061FDA0` (2D), `0x00620250` (3D) and `0x00620630` (cube, six array slices) create every texture of the
ring with the device's `CreateTexture2D` (`+0x28`) or `CreateTexture3D` (`+0x30`), read each
description back with `GetDesc` (`+0x50`), and name the resource for debugging (`PTexture`,
`PTexture_MSAA`, `PTexture3D`, `PCubeMap`, through `0x0061C550`). Then they create the
shader-resource and unordered-access views when asked.

- The format is the format object's `+0x24`; the level count is `+0x10` + 1, or 1 when `+0x14` is 0
  and mips are not generated.
- Bind flags: `0x8` for a shader resource, `0x80` for unordered access, and for a render target
  (`+0x18` bit `0x100`) `0x20`, or `0x40` when the format is a depth format.
- `0x0061FDA0` reads the render target at `+0x20`: sample count 7 becomes 4 samples at quality 16 and
  9 becomes 8 at quality 16, and a multisampled target gets a second texture.
- A 3D texture without initial data, render-target or UAV use and with one level is created
  dynamic with CPU write access; asking for that on a render target returns 5.

The "ensure" functions create the ring only when its first texture is missing and then set the
created word: `0x0061E200` (2D) and `0x0061E270` (3D) pass a shader view and `+0x18` bit `0x400` as the
UAV request, `0x0061E2E0` (cube) a shader view only. `0x00650660` returns 7 for a 3D texture still in the
null format, 0 when it is created, and otherwise calls `0x0061E270`. `0x00628100` re-creates a 2D
texture: it releases a created one, resizes the ring (`0x00627DA0`) and creates it again.

### Mapping textures for writing

`0x00609870` (3D) and `0x00609950` (cube) take a ring record, wait 1 ms at a time while its in-use count is
above 0, map it and set the state byte `+0x08` to 2. The 3D one steps to the record after `+0x0C`,
the cube one takes the counter `0x01F7F5A0` modulo the ring size; both return 7 for the null
format.

`0x006264F0` (3D) and `0x00626990` (cube) fill the caller's layout of up to 12 levels (layouts below).
Level sizes come from the format's bits per pixel `bpp` (format `+0x14`). Each level's sides are
`max(side >> 1, 1)` of the level before; for a block format (format `+0x18` bit 0) the width `w` and height `h` are
first rounded up, `(side + 3) & ~3`. A level's row pitch is `bpp x w x k >> 3`, `k` 4 for a block format and 1
otherwise, its slice pitch `bpp x w x h >> 3` and its size the slice pitch times the depth (`0x006264F0`); a cube
level is square, `bpp x w x w >> 3` (`0x00626990`).

- Without CPU write access (the description's `+0x1C` bit `0x10000`) they log
  `Performance warning: mapping texture that was not created with D3D11_CPU_ACCESS_WRITE flag
  specified - main memory buffer will be allocated.` and hand out a main-memory copy, allocated on
  first use at the full size of the levels (six faces for a cube).
- With it, `0x006264F0` maps each level on the immediate context (`Map`, `+0x70`) with `WRITE_DISCARD`
  for a dynamic texture and `WRITE` otherwise, under the context lock; a failed map returns 9.

`0x0062C820(cube, record, layout)` copies the `0x2A8`-byte layout to `+0xA8`, sets the record's update
entry to this cube and record index, and queues it for the frame slot `0x01F7F590` (`0x0062EB90`, the
deferred upload queue of the draw page).

### Releasing textures

- `0x006505A0` takes `{texture, kind}` and releases a created texture: kind 0 `0x0062BCB0` (2D), 1
  `0x0062BF40` (3D), 2 `0x0062C100` (cube).
- `0x0062BCB0` clears the created word, releases the render
  target's views first when it has them (`0x0062B870`), and for every ring record takes its pending
  upload off the queue (`0x0062EC70`), frees the main-memory copy at `+0x28` and releases the six
  interfaces at `+0x10`, `+0x18`, `+0x20`, `+0x00`, `+0x08` and `+0x30`. The other two do the same
  for their records.
- `0x005DDBB0` destroys the placeholder set below: it releases the sampler at `+0x568`
  (`0x006167C0`) and each of the three textures that is created.

### Placeholder textures

`0x00607FA0(set, options)` fills a set of three textures, when byte `+0x01` of `options` is set: a 2D
texture at `+0x000`, a 3D one at `+0x188` and a cube map at `+0x218`, each made only when the flags of
the `RGBA8` format (`0x02CF7498`) have bit `0x8`, `0x10` or `0x20` respectively.

1. It sizes the texture 4×4 (×4 for 3D) in `RGBA8` with no mips and sets `+0x18` bit `0x200`.
2. It maps the next ring record, fills every level with a checkerboard of `0xFF00FF00` and
   `0xFFFF00FF` (green and magenta in `R8G8B8A8`; `0x005F0590` for the 2D one, inline for the others)
   and unmaps it (`0x0062C360`, `0x0062C570`, `0x0062C820`).
3. It creates the texture when it is not created yet (`0x0061E200`, `0x0061E270`, `0x0061E2E0`).

It then resets the fields of the sampler at `+0x568` whose word `+0x584` has bit 7 clear.

### Constant buffers

A `PConstantBufferD3D11` (`0x50` bytes, constructor `0x00615550`) keeps a main-memory block at `+0x10`
with one copy per ring record, a ring of `0x10`-byte records at `+0x18`/`+0x20` (buffer, dirty word,
in-use count) and a `D3D11_BUFFER_DESC` from `+0x30`.

1. `0x006097B0` steps to the next record, waits while it is in use, creates the buffers first when
   needed (`0x0061D960`), and hands out the record's copy with `0x00626060`: `+0x10` plus `+0x00` × the
   record index, logging `Performance warning: mapping buffer that was not created with
   D3D11_CPU_ACCESS_WRITE flag specified - main memory buffer will be allocated.` without CPU write.
2. `0x0062C300(buffer, i)` marks record `i` dirty; 3 for an index past the ring, `0x15` with no buffer.
3. When a shader binds it, `0x006239C0(buffer, i)` maps a dirty record (`WRITE_DISCARD` when the usage
   at `+0x34` is 2, else `WRITE`), copies `+0x30` bytes from its copy, unmaps and clears the dirty word.

`0x00623EB0(buffer, i)` returns record `i`'s buffer, or null past the ring; `0x00623F00` does the same for
a structured buffer.

### Structured buffers

`0x0061F200(buffer, count, size, flags, data)` creates a `PStructuredBufferD3D11` (`0x68` bytes,
constructor `0x00616060`) of `count × size` bytes for every ring record (`0x28` bytes: buffer, view,
UAV):

- flag 1 makes it dynamic with CPU write access; otherwise it is immutable with data and
  default without, and only then takes bind flag `0x80` beside `0x8`;
- flag `0x10` makes it raw (misc `0x20`, stride 4), otherwise structured (misc `0x40`, stride `size`);
- flag 8 with data creates the buffers empty, then copies a staging buffer holding the data into each
  (`CopyResource`).

It reads the description back into `+0x48` and creates the views: `0x0061F710` a shader view when bind
flag 8 is set (raw: `R32_TYPELESS`, one element per 4 bytes, flag 1), `0x006209C0` an unordered-access
view when bind flag `0x80` is set, one element per buffer element, with the counter flag (4) for
buffer flag 2 or the append flag (2) for buffer flag 4.

### Sampler filters

The sampler builder `0x0061D9C0` turns the engine's filter bytes into a `D3D11_FILTER` with
`0x0061C080(min, mag, comparison, maxAnisotropy)`. A maximum anisotropy of 2 or more gives `0x55`
(anisotropic); a comparison sampler adds `0x80` to every result.

| `min` | `mag` 0 | `mag` non-zero |
|---|---|---|
| 0, 2 | `0x00` | `0x04` |
| 1, 3 | `0x10` | `0x14` |
| 4 | `0x01` | `0x05` |
| 5 | `0x11` | `0x15` |
| any other | `0x00` | `0x00` |

### GPU timer queries

`0x00615790` builds an object with three Direct3D queries from `CreateQuery` (`+0xC0`): a
timestamp-disjoint query (type 3) at `+0x10` and two timestamp queries (type 2) at `+0x18` and
`+0x20`, after `0x005DBFE0` has cleared `+0x00` and the byte `+0x08`.

### Render targets in a cluster

`0x005D8E40(cluster, description)` creates one `PRenderTarget` instance in a cluster (`0x006394E0`, with
descriptor `0x02CB76A0`) and initialises it with `0x00615C90`; it returns null when no object results.
Ten call sites in `0x0064A000`–`0x006560E0` use it.

## Layouts

`RenderContextDevice` (offsets from the start of the context):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0108` | `void*` | device | ID3D11Device |
| `+0x0110` | `void*` | context | ID3D11DeviceContext, the immediate context |
| `+0x0118` | `void*` | swapChain | IDXGISwapChain |
| `+0x0120` | `u8[72]` | swapChainDesc | DXGI_SWAP_CHAIN_DESC filled by `0x00625830` |
| `+0x0168` | `u32` | featureLevel | `0xB000` or higher |
| `+0x0170` | `u8[392]` | backBuffer | PTexture2D; ring texture 0 is the swap chain's buffer 0 |
| `+0x02F8` | `u8[392]` | depth | PTexture2D in DEPTH24S8 |
| `+0x0480` | `u8[80]` | colourTarget | PRenderTarget; sample count at +`0x09` |
| `+0x04D0` | `u8[80]` | depthTarget | PRenderTarget; sample count at +`0x09` |
| `+0x06F0` | `u32` | uploadSlot | set by `0x00626D90` |
| `+0x0708` | `u8[88]` | vertexIndexUpload | UploadBufferPair, sizes from +`0xF4` and +`0xF8` |
| `+0x0760` | `u8[88]` | rawUpload | UploadBufferPair, sizes from +`0xFC` and +`0x100` |
| `+0x07B8` | `void*` | indirectArgs | 16-byte ID3D11Buffer, feature level 11.0 |
| `+0x1850` | `f64` | startClock | clock() at creation |
| `+0x1878` | `void*` | factory | IDXGIFactory |
| `+0x1880` | `void*` | adapter | IDXGIAdapter chosen at start-up |
| `+0x18A4` | `u32` | refreshRate | numerator / denominator |

`DXGI_SWAP_CHAIN_DESC` (`0x48` bytes, offsets from the start of the context+0x120):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | Width | width argument |
| `+0x04` | `u32` | Height | height argument |
| `+0x08` | `u32` | RefreshNumerator | 60, or the screen mode's (`0x00623320`) |
| `+0x0C` | `u32` | RefreshDenominator | 1, or the screen mode's |
| `+0x10` | `u32` | Format | `0x1C` R8G8B8A8_UNORM |
| `+0x14` | `u32` | ScanlineOrdering | 0 |
| `+0x18` | `u32` | Scaling | 0 |
| `+0x1C` | `u32` | SampleCount | 1-16 |
| `+0x20` | `u32` | SampleQuality | 0 |
| `+0x24` | `u32` | BufferUsage | `0x20` |
| `+0x28` | `u32` | BufferCount | from context +`0x184C` |
| `+0x30` | `void*` | OutputWindow | the window argument |
| `+0x38` | `u32` | Windowed | 1 |
| `+0x3C` | `u32` | SwapEffect | 0 |
| `+0x40` | `u32` | Flags | 2 |

`UploadBufferPair` (`0x58` bytes, offsets from the start of the context+0x708):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*[2]` | vertex | dynamic vertex buffers |
| `+0x10` | `void*[2]` | index | dynamic index buffers |
| `+0x20` | `u32[2]` | vertexUsed | bytes to upload |
| `+0x28` | `u32[2]` | indexUsed | bytes to upload |
| `+0x30` | `u32` | vertexSize | 4 MiB by default |
| `+0x34` | `u32` | indexSize | 1 MiB by default; the buffers are 16 bytes larger |
| `+0x38` | `void*[2]` | vertexCopy | main-memory copies; unordered-access views in the pair at +`0x760` |
| `+0x48` | `void*[2]` | indexCopy | main-memory copies; unordered-access views in the pair at +`0x760` |

`TextureFormat` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | name | for example RGBA8 |
| `+0x08` | `u64` | zero | 0 |
| `+0x10` | `u32` | code | engine format code |
| `+0x14` | `u32` | bitsPerPixel | from `0x0062CD40` |
| `+0x18` | `u32` | flags | 1 block-compressed, 2 depth, 4 float; channel mask; argument bits |
| `+0x20` | `u32` | format0 | 0 in every format |
| `+0x24` | `u32` | textureFormat | DXGI format of the texture |
| `+0x28` | `u32` | format2 | depth-stencil view format for depth formats; 0 for block formats |
| `+0x2C` | `u32` | format3 | readable format |
| `+0x30` | `u32` | format4 | 0 for block formats |

`TextureCommon` (offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | format | TextureFormat, `0x02CF7A30` until set |
| `+0x10` | `u32` | mips | mip count given to the size setter |
| `+0x14` | `u32` | levels | derived level count |
| `+0x18` | `u32` | flags | `0x2` generate mips, `0x100` render target, `0x400` UAV |
| `+0x20` | `void*` | renderTarget | sample count at +`0x09` |
| `+0x28` | `u32` | width |  |
| `+0x2C` | `u32` | height |  |
| `+0x30` | `u32` | depth | PTexture3D only |

`Texture2DRecord` (`0x58` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | texture | ID3D11Texture2D |
| `+0x08` | `void*` | msaaTexture | ID3D11Texture2D |
| `+0x10` | `void*` | view | shader-resource view (`0x00623FA0`) |
| `+0x18` | `void*` | interface18 | an interface released with the others |
| `+0x20` | `void*` | uav | unordered-access view (`0x006241D0`) |
| `+0x28` | `void*` | copy | main-memory copy |
| `+0x30` | `void*` | interface30 | an interface released with the others |
| `+0x40` | `u8[24]` | update | pending upload entry |

`Texture3DMapLayout` (`0xC8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | zero |  |
| `+0x08` | `void*` | level0 | first level's data |
| `+0x10` | `u32` | rowPitch0 |  |
| `+0x14` | `u32` | slicePitch0 |  |
| `+0x18` | `u8[176]` | levels1to11 | the same 16-byte entry for levels 1-11 |

`CubeMapLayout` (`0x2A8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | zero |  |
| `+0x08` | `void*[6]` | level0Faces | one pointer per face |
| `+0x38` | `u32` | level0RowPitch |  |
| `+0x40` | `u8[616]` | levels1to11 | the same `0x38`-byte entry for levels 1-11 |

`PConstantBufferD3D11` (`0x50` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | copySize | stride of the main-memory copies |
| `+0x10` | `void*` | copies | one copy per ring record |
| `+0x18` | `u32` | ringCount |  |
| `+0x20` | `u8[16]` | ring | ConstantBufferRecord inline for one record, else a pointer |
| `+0x30` | `u32` | byteWidth | bytes uploaded |
| `+0x34` | `u32` | usage | 2 = dynamic |
| `+0x3C` | `u32` | cpuAccess | `0x10000` = write |
| `+0x48` | `u32` | created |  |

`ConstantBufferRecord` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | buffer | ID3D11Buffer |
| `+0x08` | `u32` | dirty | set by `0x0062C300` |
| `+0x0C` | `u32` | inUse |  |

`PStructuredBufferD3D11` (`0x68` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count | elements |
| `+0x04` | `u32` | size | bytes per element |
| `+0x08` | `u32` | flags | 1 dynamic, 2 counter, 4 append, 8 staged data, `0x10` raw |
| `+0x18` | `u32` | ringCount | `0x28`-byte records: buffer, view, unordered-access view |
| `+0x20` | `void*` | ring |  |
| `+0x48` | `u8[24]` | desc | D3D11_BUFFER_DESC read back after creation |

Texture formats (initialisers `0x00163110`–`0x00163D8F`, one per format):

| Code | Name | Object | Bits | Flags | DXGI formats `+0x20`–`+0x30` |
|---|---|---|---|---|---|
| `0x00` | `L8` | `0x02CF72C0` | 8 | `0xFF8` | 0, `0x3D` ×4 |
| `0x01` | `A8` | `0x02CF72F8` | 8 | `0x11F8` | 0, `0x41` ×4 |
| `0x02` | `LA8` | `0x02CF7330` | 16 | `0x1FF8` | 0, `0x31` ×4 |
| `0x03` | `RG8` | `0x02CF7368` | 16 | `0x7F8` | 0, `0x31` ×4 |
| `0x04` | `L16` | `0x02CF73A0` | 16 | `0xFF8` | 0, `0x39` ×4 |
| `0x05` | `A16` | `0x02CF73D8` | 16 | `0x11F8` | 0, `0x39` ×4 |
| `0x06` | `LA16` | `0x02CF7410` | 32 | `0x1FF8` | 0, `0x24` ×4 |
| `0x07` | `RG16` | `0x02CF7448` | 32 | `0x7F8` | 0, `0x24` ×4 |
| `0x0B` | `RGBA8` | `0x02CF7480` | 32 | `0x1FF8` | 0, `0x1C` ×4 |
| `0x0C` | `ARGB8` | `0x02CF74B8` | 32 | `0x1FF8` | 0, `0x57` ×4 |
| `0x0D` | `A2RGB10` | `0x02CF74F0` | 32 | `0x1FF8` | 0, `0x18` ×4 |
| `0x0E` | `RGBA16` | `0x02CF7528` | 64 | `0x1FF8` | 0, `0x0C` ×4 |
| `0x0F` | `DXT1` | `0x02CF7560` | 4 | `0x1E39` | 0, `0x47`, 0, `0x47`, 0 |
| `0x10` | `DXT3` | `0x02CF7598` | 8 | `0x1E39` | 0, `0x4A`, 0, `0x4A`, 0 |
| `0x11` | `DXT5` | `0x02CF75D0` | 8 | `0x1E39` | 0, `0x4D`, 0, `0x4D`, 0 |
| `0x12` | `BC4` | `0x02CF7608` | 4 | `0x239` | 0, `0x50`, 0, `0x50`, 0 |
| `0x13` | `BC5` | `0x02CF7640` | 8 | `0x1E39` | 0, `0x53`, 0, `0x53`, 0 |
| `0x14` | `BC6` | `0x02CF7678` | 8 | `0x1E39` | 0, `0x5F`, 0, `0x5F`, 0 |
| `0x15` | `BC7` | `0x02CF76B0` | 8 | `0x1E39` | 0, `0x62`, 0, `0x62`, 0 |
| `0x1E` | `RGBA16F` | `0x02CF76E8` | 64 | `0x1FFC` | 0, `0x0A` ×4 |
| `0x1F` | `RGBA32F` | `0x02CF7720` | 128 | `0x1FFC` | 0, `0x02` ×4 |
| `0x20` | `R16F` | `0x02CF7758` | 16 | `0x3FC` | 0, `0x36` ×4 |
| `0x21` | `L16F` | `0x02CF7790` | 16 | `0xFFC` | 0, `0x36` ×4 |
| `0x22` | `R32F` | `0x02CF77C8` | 32 | `0x3FC` | 0, `0x29` ×4 |
| `0x23` | `L32F` | `0x02CF7800` | 32 | `0xFFC` | 0, `0x29` ×4 |
| `0x24` | `RG16F` | `0x02CF7838` | 32 | `0x7FC` | 0, `0x22` ×4 |
| `0x25` | `LA16F` | `0x02CF7870` | 32 | `0x1FFC` | 0, `0x22` ×4 |
| `0x26` | `RG32F` | `0x02CF78A8` | 64 | `0x7FC` | 0, `0x10` ×4 |
| `0x27` | `LA32F` | `0x02CF78E0` | 64 | `0x1FFC` | 0, `0x10` ×4 |
| `0x28` | `DEPTH16` | `0x02CF7950` | 16 | `0x207A` | 0, `0x35`, `0x37`, `0x38`, `0x38` |
| `0x29` | `DEPTH24` | `0x02CF7988` | 32 | `0x207A` | 0, `0x2C`, `0x2D`, `0x2E`, `0x2E` |
| `0x2A` | `DEPTH24S8` | `0x02CF79C0` | 32 | `0x607A` | 0, `0x2C`, `0x2D`, `0x2E`, `0x2E` |
| `0x2B` | `DEPTH32` | `0x02CF79F8` | 32 | `0x207A` | 0, `0x27`, `0x28`, `0x29`, `0x29` |
| `0x32` | `R32` | `0x02CF7918` | 32 | `0x3F8` | 0, `0x2A` ×4 |
| `0x33` | name string at `0x00D26D00` | `0x02CF7A30` | 0 | 0 | 0 ×5 |

Colour formats pass flag argument `0x1F8`, block formats `0x38`, depth formats `0x78`. In the derived
flags, `0x200`, `0x400`, `0x800` and `0x1000` follow the channels the name lists (R, G, B, A; L sets
all three colour bits) and `0x2000` and `0x4000` mark depth and stencil.

## Shipped data

| Fact | Value |
|---|---|
| texture-format objects | 35, at `0x02CF72C0`–`0x02CF7A30`, `0x38` bytes apart |
| block-compressed formats | 7: `DXT1`, `DXT3`, `DXT5`, `BC4`–`BC7` |
| depth formats | 4: `DEPTH16`, `DEPTH24`, `DEPTH24S8`, `DEPTH32` |
| feature levels asked for | `0xB000`, `0xA100`, `0xA000`; below `0xB000` the device is refused |
| default upload sizes | 4 MiB vertex, 1 MiB + 16 index, two of each per pair |

## State

| Address | What |
|---|---|
| `0x02CF7480` | the `RGBA8` format of the back buffer |
| `0x02CF79C0` | the `DEPTH24S8` format of the depth texture |
| `0x02CF7A30` | the null format every texture starts with |
| `0x01F7F5A0` | counter that picks a cube map's ring record |
| `0x01F7F590` | frame slot of the deferred upload queue |

## Modding notes

- The device needs feature level 11.0; the lower levels in the creation list are never kept.
- A texture created without CPU write access can still be mapped, but every map then works on a
  main-memory copy that is uploaded later through the queue, and the game logs a performance warning.
- A format's DXGI value is read from its object's `+0x24`; replacing a format pointer changes the
  texture's format, bits per pixel and block rounding together.
- The refresh rate comes from the mode that matches the screen size, not the window size.

## Related

- [Phyre D3D11 draws and state](phyre-d3d11-draws-and-state.md): the draw calls, bind caches, data-block rings and the deferred upload queue.
- [Graphics adapters and vendor libraries](../Steam-And-Achievements/graphics-adapters-and-vendor-libraries.md): how the adapter is chosen and the multisample probe that ends device creation.
- [Phyre application](phyre-application.md): the framework that opens the window the swap chain draws into.
- [Phyre asset files](phyre-asset-files.md): the texture data a cluster load copies into these objects.
