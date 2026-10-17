---
title: "Phyre D3D11 device and resources: device and swap-chain creation, the texture formats, texture and buffer objects and how they are mapped, uploaded and released"
kind: "system"
category: "PhyreEngine"
addresses: "00625830, 00623320, 00624F70, 006250C0, 00625210, 00623B10, 0061ECD0, 00626D90, 0062CD40, 00616210, 02CF7A30, 0061FDA0, 00620250, 00620630, 0061E200, 0061E270, 0061E2E0, 00650660, 00628100, 0060DD70, 0060DE00, 00610990, 006264F0, 00626990, 00609870, 00609950, 0062C820, 0062BCB0, 0062BF40, 0062C100, 006505A0, 005DDBB0, 00615550, 0061D960, 00626060, 006097B0, 0062C300, 006239C0, 00616060, 0061F200, 0061F710, 006209C0, 0061C080, 00615790, 00607FA0, 005F0590, 00623F00, 005D8E40"
---

## What the player sees

The window the game draws into, its back buffer and depth buffer, and every texture and constant
the shaders read are made by the code on this page. The swap chain is created windowed, in
`R8G8B8A8_UNORM`, with the refresh rate of the screen's current mode, and the device is refused
unless the adapter reaches Direct3D feature level 11.0.

## How it works

### Building the render context

`005FD050` constructs the render context, the static `02CC0410`, with `00615840` the first time it is
asked for it. Among the members it builds are the back-buffer texture at `+170`<sub>h</sub> and the depth texture
at `+2F8`<sub>h</sub> (each zeroed and set up by `006160B0`), and the colour and depth render targets at
`+480`<sub>h</sub> and `+4D0`<sub>h</sub>. `005DC1C0(target, texture)` attaches a target to its texture: it stores the
texture at `+00`<sub>h</sub>, sets bit `100`<sub>h</sub> of the texture's `+18`<sub>h</sub> and points the texture's `+20`<sub>h</sub> at the
target unless another live target already holds it.

When a member's constructor throws, the unwind actions of `00615840` destroy what has been built:

- `00616740` for each render target: `0062B890` when its `+18`<sub>h</sub> or `+28`<sub>h</sub> is set, which releases the
  views in its two arrays and the four interfaces at `+10`<sub>h</sub>–`+28`<sub>h</sub>, then `005DDB00`, which frees the
  arrays' storage;
- `00616520` and `00616780` for the eight `18`<sub>h</sub>-byte records at `+08`<sub>h</sub> and at `+570`<sub>h</sub>, whose element
  destructor (`0016D6A0`) does nothing.

The context's destructor `00616560` runs the same steps among its own.

### Creating the device and swap chain

`00625830(context, width, height, samples, …, hwnd)` runs after the adapter is chosen (see the
adapter page under Related). It works on the render context, the static object `005FD050` returns.

1. It probes the adapter at context `+1880`<sub>h</sub> with `D3D11CreateDevice` (driver type 0, no flags,
   SDK version 7, no device kept) and returns 9 unless the reported feature level is `B000`<sub>h</sub> or higher.
2. It fills the `DXGI_SWAP_CHAIN_DESC` at context `+120`<sub>h</sub> (layout below): the given size, format
   `1C`<sub>h</sub>, refresh rate 60/1, the sample count clamped to 1–16, usage `20`<sub>h</sub> (render-target output),
   the buffer count from `+184C`<sub>h</sub>, the window, windowed, swap effect 0 and flag 2 (allow mode switch).
3. `EnumDisplaySettingsA` reads the current mode, and `00623320` replaces the refresh rate with that
   of the mode matching the screen size; `+18A4`<sub>h</sub> takes the rate as a whole number and the values are logged
   (`Init Fresh rate x = %d, y = %d %d  get fresh = %d`).
4. `D3D11CreateDeviceAndSwapChain` is called with the levels `B000`<sub>h</sub>, `A100`<sub>h</sub>, `A000`<sub>h</sub> and no flags;
   it stores the swap chain at `+118`<sub>h</sub>, the device at `+108`<sub>h</sub>, the immediate context at `+110`<sub>h</sub>
   and the level at `+168`<sub>h</sub>. A failure is logged (`R != S_OK %d!`, `m_d3dDevice error!!` and the like)
   and returns 9.

Then it:

- calls the factory's `MakeWindowAssociation` (`+40`<sub>h</sub>) with flag 1 (no window changes);
- queries the device for `ID3D11Debug` and, when that succeeds, that interface for `ID3D11InfoQueue`;
- takes back buffer 0 with `GetBuffer` (`+48`<sub>h</sub>) into the ring of the `PTexture2D` at `+170`<sub>h</sub>, reads
  its description into `+200`<sub>h</sub>, and gives that texture the `RGBA8` format `02CF7480` and the buffer's size;
- sets up the colour render target at `+480`<sub>h</sub> and the depth render target at `+4D0`<sub>h</sub>
  (`00620F60`), with the sample count at their `+09`<sub>h</sub> (0 for one sample), and sizes the depth
  texture at `+2F8`<sub>h</sub> as `DEPTH24S8` (`02CF79C0`) with `0060DD70` and `00610990`.

It then sets the viewport (`0061D3D0`), builds the helpers at `+7D8`<sub>h</sub> (`00624980`), `+B50`<sub>h</sub>
(`00624C30`) and `+18C0`<sub>h</sub> (`006C9CD0`), stores the start `clock()` at `+1850`<sub>h</sub>, creates the two
upload-buffer pairs below, and on feature level 11.0 a 16-byte indirect-arguments buffer at `+7B8`<sub>h</sub>
(misc flag `10`<sub>h</sub>). It binds the colour and depth views with `OMSetRenderTargets` (`+108`<sub>h</sub>), the
multisampled ones when the sample count is above 1, creates the default sampler at `+1820`<sub>h</sub>
(`0061D9C0`) and finally probes the multisample levels (`00628690`).

### The screen refresh rate

`00623320(context, &rate, width, height)` creates a DXGI factory, takes adapter 0 and its output 0,
and asks `GetDisplayModeList` (`+40`<sub>h</sub>) for format `1C`<sub>h</sub>. Every listed mode whose width and height
equal the arguments copies its 8-byte refresh rate into `rate`, so the last match wins. With no match
the rate stays 60/1.

### The upload buffer pairs

The context holds two `58`<sub>h</sub>-byte pair objects, each with two vertex buffers and two index buffers
used alternately (layout below):

- `00624F70(pair, device, vbSize, ibSize)` at `+708`<sub>h</sub>, sizes from `+F4`<sub>h</sub> and `+F8`<sub>h</sub>: dynamic
  buffers with CPU write access, a vertex size of 4 MiB and an index size of 1 MiB + 16 when the
  argument is 0, plus a 16-byte-aligned main-memory copy of each.
- `00625210(pair, device, …)` at `+760`<sub>h</sub>, sizes from `+FC`<sub>h</sub> and `+100`<sub>h</sub>, goes through `006250C0`
  with default usage and bind flag `80`<sub>h</sub> added, which also makes the buffers raw (misc `20`<sub>h</sub>). It
  then creates an unordered-access view of each: raw views (`R32_TYPELESS`, one element per 4 bytes,
  flag 1) for raw buffers, one element per stride for structured ones.

`00626D90(context, i)` makes slot `i` current (`+6F0`<sub>h</sub>) and zeroes its used sizes in both pairs.
`0061ECD0(context, i)` uploads slot `i` of the first pair through `00623B10`: each non-empty
buffer is mapped with `WRITE_DISCARD` and its used bytes are copied from the main-memory copy; 9 on a
failed map.

### Texture formats

A texture names its format through a pointer at `+00`<sub>h</sub> to one of 35 static format objects
(`38`<sub>h</sub> bytes). Each is built before `main` by its own initialiser, which calls `00616210(object,
name, code, flags, five DXGI formats)`; `00616210` runs `0062CD40` and stores the five formats at
`+20`<sub>h</sub>–`+30`<sub>h</sub>. `0062CD40` stores the name and code and derives from the code:

- the bits per pixel at `+14`<sub>h</sub>, from a switch over the code;
- the flags at `+18`<sub>h</sub>: the argument's bits outside `7E07`<sub>h</sub>, a channel mask from the same switch,
  bit 0 for the block-compressed codes `0F`<sub>h</sub>–`18`<sub>h</sub> and `1D`<sub>h</sub>, bit 1 for the depth codes
  `28`<sub>h</sub>–`2B`<sub>h</sub> and `31`<sub>h</sub>, bit 2 for the float codes `1E`<sub>h</sub>–`27`<sub>h</sub>.

`02CF7A30` (code `33`<sub>h</sub>, no bits, no flags) is the null format a texture starts with. The table under Layouts lists all 35.

### Texture objects

The three D3D11 texture classes keep a ring of Direct3D textures in a `PSharray`, like the data
blocks of the draw page, and a word that is non-zero while the ring is created:

| Class | Size | Ring (count, data) | Record | Created word |
|---|---|---|---|---|
| `PTexture2D` | `188`<sub>h</sub> | `+30`<sub>h</sub>, `+38`<sub>h</sub> | `58`<sub>h</sub> | `+BC`<sub>h</sub> |
| `PTexture3D` | `90`<sub>h</sub> | `+38`<sub>h</sub>, `+40`<sub>h</sub> | `28`<sub>h</sub> | `+8C`<sub>h</sub> |
| `PTextureCubeMap` | `350`<sub>h</sub> | `+30`<sub>h</sub>, `+38`<sub>h</sub> | `40`<sub>h</sub> | `+A4`<sub>h</sub> |

Setting the size records the format, width, height (and depth) and mip count and recomputes the level
count at `+14`<sub>h</sub>: `0060DD70` for 2D and `0060DE00` for 3D. Both return 3 when the larger side is
below `1 << mips`, and with bit 1 of `+18`<sub>h</sub> (generate mips) the level count is the base-2 logarithm
of the largest side. `00610990` recomputes `+14`<sub>h</sub> alone. `005DCC10` is the 3D base initialiser:
format `02CF7A30`, `+08`<sub>h</sub> = `300`<sub>h</sub>, `+18`<sub>h</sub> = 2.

### Creating textures

`0061FDA0` (2D), `00620250` (3D) and `00620630` (cube, six array slices) create every texture of the
ring with the device's `CreateTexture2D` (`+28`<sub>h</sub>) or `CreateTexture3D` (`+30`<sub>h</sub>), read each
description back with `GetDesc` (`+50`<sub>h</sub>), and name the resource for debugging (`PTexture`,
`PTexture_MSAA`, `PTexture3D`, `PCubeMap`, through `0061C550`). Then they create the
shader-resource and unordered-access views when asked.

- The format is the format object's `+24`<sub>h</sub>; the level count is `+10`<sub>h</sub> + 1, or 1 when `+14`<sub>h</sub> is 0
  and mips are not generated.
- Bind flags: `8`<sub>h</sub> for a shader resource, `80`<sub>h</sub> for unordered access, and for a render target
  (`+18`<sub>h</sub> bit `100`<sub>h</sub>) `20`<sub>h</sub>, or `40`<sub>h</sub> when the format is a depth format.
- `0061FDA0` reads the render target at `+20`<sub>h</sub>: sample count 7 becomes 4 samples at quality 16 and
  9 becomes 8 at quality 16, and a multisampled target gets a second texture.
- A 3D texture without initial data, render-target or UAV use and with one level is created
  dynamic with CPU write access; asking for that on a render target returns 5.

The "ensure" functions create the ring only when its first texture is missing and then set the
created word: `0061E200` (2D) and `0061E270` (3D) pass a shader view and `+18`<sub>h</sub> bit `400`<sub>h</sub> as the
UAV request, `0061E2E0` (cube) a shader view only. `00650660` returns 7 for a 3D texture still in the
null format, 0 when it is created, and otherwise calls `0061E270`. `00628100` re-creates a 2D
texture: it releases a created one, resizes the ring (`00627DA0`) and creates it again.

### Mapping textures for writing

`00609870` (3D) and `00609950` (cube) take a ring record, wait 1 ms at a time while its in-use count is
above 0, map it and set the state byte `+08`<sub>h</sub> to 2. The 3D one steps to the record after `+0C`<sub>h</sub>,
the cube one takes the counter `01F7F5A0` modulo the ring size; both return 7 for the null
format.

`006264F0` (3D) and `00626990` (cube) fill the caller's layout of up to 12 levels (layouts below).
Level sizes come from the format's bits per pixel `bpp` (format `+14`<sub>h</sub>). Each level's sides are
`max(side >> 1, 1)` of the level before; for a block format (format `+18`<sub>h</sub> bit 0) the width `w` and height `h` are
first rounded up, `(side + 3) & ~3`. A level's row pitch is `bpp x w x k >> 3`, `k` 4 for a block format and 1
otherwise, its slice pitch `bpp x w x h >> 3` and its size the slice pitch times the depth (`006264F0`); a cube
level is square, `bpp x w x w >> 3` (`00626990`).

- Without CPU write access (the description's `+1C`<sub>h</sub> bit `10000`<sub>h</sub>) they log
  `Performance warning: mapping texture that was not created with D3D11_CPU_ACCESS_WRITE flag
  specified - main memory buffer will be allocated.` and hand out a main-memory copy, allocated on
  first use at the full size of the levels (six faces for a cube).
- With it, `006264F0` maps each level on the immediate context (`Map`, `+70`<sub>h</sub>) with `WRITE_DISCARD`
  for a dynamic texture and `WRITE` otherwise, under the context lock; a failed map returns 9.

`0062C820(cube, record, layout)` copies the `2A8`<sub>h</sub>-byte layout to `+A8`<sub>h</sub>, sets the record's update
entry to this cube and record index, and queues it for the frame slot `01F7F590` (`0062EB90`, the
deferred upload queue of the draw page).

### Releasing textures

- `006505A0` takes `{texture, kind}` and releases a created texture: kind 0 `0062BCB0` (2D), 1
  `0062BF40` (3D), 2 `0062C100` (cube).
- `0062BCB0` clears the created word, releases the render
  target's views first when it has them (`0062B870`), and for every ring record takes its pending
  upload off the queue (`0062EC70`), frees the main-memory copy at `+28`<sub>h</sub> and releases the six
  interfaces at `+10`<sub>h</sub>, `+18`<sub>h</sub>, `+20`<sub>h</sub>, `+00`<sub>h</sub>, `+08`<sub>h</sub> and `+30`<sub>h</sub>. The other two do the same
  for their records.
- `005DDBB0` destroys the placeholder set below: it releases the sampler at `+568`<sub>h</sub>
  (`006167C0`) and each of the three textures that is created.

### Placeholder textures

`00607FA0(set, options)` fills a set of three textures, when byte `+01`<sub>h</sub> of `options` is set: a 2D
texture at `+000`<sub>h</sub>, a 3D one at `+188`<sub>h</sub> and a cube map at `+218`<sub>h</sub>, each made only when the flags of
the `RGBA8` format (`02CF7498`) have bit `8`<sub>h</sub>, `10`<sub>h</sub> or `20`<sub>h</sub> respectively.

1. It sizes the texture 4×4 (×4 for 3D) in `RGBA8` with no mips and sets `+18`<sub>h</sub> bit `200`<sub>h</sub>.
2. It maps the next ring record, fills every level with a checkerboard of `FF00FF00`<sub>h</sub> and
   `FFFF00FF`<sub>h</sub> (green and magenta in `R8G8B8A8`; `005F0590` for the 2D one, inline for the others)
   and unmaps it (`0062C360`, `0062C570`, `0062C820`).
3. It creates the texture when it is not created yet (`0061E200`, `0061E270`, `0061E2E0`).

It then resets the fields of the sampler at `+568`<sub>h</sub> whose word `+584`<sub>h</sub> has bit 7 clear.

### Constant buffers

A `PConstantBufferD3D11` (`50`<sub>h</sub> bytes, constructor `00615550`) keeps a main-memory block at `+10`<sub>h</sub>
with one copy per ring record, a ring of `10`<sub>h</sub>-byte records at `+18`<sub>h</sub>/`+20`<sub>h</sub> (buffer, dirty word,
in-use count) and a `D3D11_BUFFER_DESC` from `+30`<sub>h</sub>.

1. `006097B0` steps to the next record, waits while it is in use, creates the buffers first when
   needed (`0061D960`), and hands out the record's copy with `00626060`: `+10`<sub>h</sub> plus `+00`<sub>h</sub> × the
   record index, logging `Performance warning: mapping buffer that was not created with
   D3D11_CPU_ACCESS_WRITE flag specified - main memory buffer will be allocated.` without CPU write.
2. `0062C300(buffer, i)` marks record `i` dirty; 3 for an index past the ring, `15`<sub>h</sub> with no buffer.
3. When a shader binds it, `006239C0(buffer, i)` maps a dirty record (`WRITE_DISCARD` when the usage
   at `+34`<sub>h</sub> is 2, else `WRITE`), copies `+30`<sub>h</sub> bytes from its copy, unmaps and clears the dirty word.

`00623EB0(buffer, i)` returns record `i`'s buffer, or null past the ring; `00623F00` does the same for
a structured buffer.

### Structured buffers

`0061F200(buffer, count, size, flags, data)` creates a `PStructuredBufferD3D11` (`68`<sub>h</sub> bytes,
constructor `00616060`) of `count × size` bytes for every ring record (`28`<sub>h</sub> bytes: buffer, view,
UAV):

- flag 1 makes it dynamic with CPU write access; otherwise it is immutable with data and
  default without, and only then takes bind flag `80`<sub>h</sub> beside `8`<sub>h</sub>;
- flag `10`<sub>h</sub> makes it raw (misc `20`<sub>h</sub>, stride 4), otherwise structured (misc `40`<sub>h</sub>, stride `size`);
- flag 8 with data creates the buffers empty, then copies a staging buffer holding the data into each
  (`CopyResource`).

It reads the description back into `+48`<sub>h</sub> and creates the views: `0061F710` a shader view when bind
flag 8 is set (raw: `R32_TYPELESS`, one element per 4 bytes, flag 1), `006209C0` an unordered-access
view when bind flag `80`<sub>h</sub> is set, one element per buffer element, with the counter flag (4) for
buffer flag 2 or the append flag (2) for buffer flag 4.

### Sampler filters

The sampler builder `0061D9C0` turns the engine's filter bytes into a `D3D11_FILTER` with
`0061C080(min, mag, comparison, maxAnisotropy)`. A maximum anisotropy of 2 or more gives `55`<sub>h</sub>
(anisotropic); a comparison sampler adds `80`<sub>h</sub> to every result.

| `min` | `mag` 0 | `mag` non-zero |
|---|---|---|
| 0, 2 | `00`<sub>h</sub> | `04`<sub>h</sub> |
| 1, 3 | `10`<sub>h</sub> | `14`<sub>h</sub> |
| 4 | `01`<sub>h</sub> | `05`<sub>h</sub> |
| 5 | `11`<sub>h</sub> | `15`<sub>h</sub> |
| any other | `00`<sub>h</sub> | `00`<sub>h</sub> |

### GPU timer queries

`00615790` builds an object with three Direct3D queries from `CreateQuery` (`+C0`<sub>h</sub>): a
timestamp-disjoint query (type 3) at `+10`<sub>h</sub> and two timestamp queries (type 2) at `+18`<sub>h</sub> and
`+20`<sub>h</sub>, after `005DBFE0` has cleared `+00`<sub>h</sub> and the byte `+08`<sub>h</sub>.

### Render targets in a cluster

`005D8E40(cluster, description)` creates one `PRenderTarget` instance in a cluster (`006394E0`, with
descriptor `02CB76A0`) and initialises it with `00615C90`; it returns null when no object results.
Ten call sites in `0064A000`–`006560E0` use it.

## Layouts

`RenderContextDevice` (offsets from the start of the context):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0108`<sub>h</sub> | `void*` | device | ID3D11Device |
| `0110`<sub>h</sub> | `void*` | context | ID3D11DeviceContext, the immediate context |
| `0118`<sub>h</sub> | `void*` | swapChain | IDXGISwapChain |
| `0120`<sub>h</sub> | `u8[72]` | swapChainDesc | DXGI_SWAP_CHAIN_DESC filled by `00625830` |
| `0168`<sub>h</sub> | `u32` | featureLevel | `B000`<sub>h</sub> or higher |
| `0170`<sub>h</sub> | `u8[392]` | backBuffer | PTexture2D; ring texture 0 is the swap chain's buffer 0 |
| `02F8`<sub>h</sub> | `u8[392]` | depth | PTexture2D in DEPTH24S8 |
| `0480`<sub>h</sub> | `u8[80]` | colourTarget | PRenderTarget; sample count at +`09`<sub>h</sub> |
| `04D0`<sub>h</sub> | `u8[80]` | depthTarget | PRenderTarget; sample count at +`09`<sub>h</sub> |
| `06F0`<sub>h</sub> | `u32` | uploadSlot | set by `00626D90` |
| `0708`<sub>h</sub> | `u8[88]` | vertexIndexUpload | UploadBufferPair, sizes from +`F4`<sub>h</sub> and +`F8`<sub>h</sub> |
| `0760`<sub>h</sub> | `u8[88]` | rawUpload | UploadBufferPair, sizes from +`FC`<sub>h</sub> and +`100`<sub>h</sub> |
| `07B8`<sub>h</sub> | `void*` | indirectArgs | 16-byte ID3D11Buffer, feature level 11.0 |
| `1850`<sub>h</sub> | `f64` | startClock | clock() at creation |
| `1878`<sub>h</sub> | `void*` | factory | IDXGIFactory |
| `1880`<sub>h</sub> | `void*` | adapter | IDXGIAdapter chosen at start-up |
| `18A4`<sub>h</sub> | `u32` | refreshRate | numerator / denominator |

`DXGI_SWAP_CHAIN_DESC` (`48`<sub>h</sub> bytes, offsets from the start of the context+`120`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | Width | width argument |
| `04`<sub>h</sub> | `u32` | Height | height argument |
| `08`<sub>h</sub> | `u32` | RefreshNumerator | 60, or the screen mode's (`00623320`) |
| `0C`<sub>h</sub> | `u32` | RefreshDenominator | 1, or the screen mode's |
| `10`<sub>h</sub> | `u32` | Format | `1C`<sub>h</sub> R8G8B8A8_UNORM |
| `14`<sub>h</sub> | `u32` | ScanlineOrdering | 0 |
| `18`<sub>h</sub> | `u32` | Scaling | 0 |
| `1C`<sub>h</sub> | `u32` | SampleCount | 1-16 |
| `20`<sub>h</sub> | `u32` | SampleQuality | 0 |
| `24`<sub>h</sub> | `u32` | BufferUsage | `20`<sub>h</sub> |
| `28`<sub>h</sub> | `u32` | BufferCount | from context +`184C`<sub>h</sub> |
| `30`<sub>h</sub> | `void*` | OutputWindow | the window argument |
| `38`<sub>h</sub> | `u32` | Windowed | 1 |
| `3C`<sub>h</sub> | `u32` | SwapEffect | 0 |
| `40`<sub>h</sub> | `u32` | Flags | 2 |

`UploadBufferPair` (`58`<sub>h</sub> bytes, offsets from the start of the context+`708`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*[2]` | vertex | dynamic vertex buffers |
| `10`<sub>h</sub> | `void*[2]` | index | dynamic index buffers |
| `20`<sub>h</sub> | `u32[2]` | vertexUsed | bytes to upload |
| `28`<sub>h</sub> | `u32[2]` | indexUsed | bytes to upload |
| `30`<sub>h</sub> | `u32` | vertexSize | 4 MiB by default |
| `34`<sub>h</sub> | `u32` | indexSize | 1 MiB by default; the buffers are 16 bytes larger |
| `38`<sub>h</sub> | `void*[2]` | vertexCopy | main-memory copies; unordered-access views in the pair at +`760`<sub>h</sub> |
| `48`<sub>h</sub> | `void*[2]` | indexCopy | main-memory copies; unordered-access views in the pair at +`760`<sub>h</sub> |

`TextureFormat` (`38`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | name | for example RGBA8 |
| `08`<sub>h</sub> | `u64` | zero | 0 |
| `10`<sub>h</sub> | `u32` | code | engine format code |
| `14`<sub>h</sub> | `u32` | bitsPerPixel | from `0062CD40` |
| `18`<sub>h</sub> | `u32` | flags | 1 block-compressed, 2 depth, 4 float; channel mask; argument bits |
| `20`<sub>h</sub> | `u32` | format0 | 0 in every format |
| `24`<sub>h</sub> | `u32` | textureFormat | DXGI format of the texture |
| `28`<sub>h</sub> | `u32` | format2 | depth-stencil view format for depth formats; 0 for block formats |
| `2C`<sub>h</sub> | `u32` | format3 | readable format |
| `30`<sub>h</sub> | `u32` | format4 | 0 for block formats |

`TextureCommon` (offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | format | TextureFormat, `02CF7A30` until set |
| `10`<sub>h</sub> | `u32` | mips | mip count given to the size setter |
| `14`<sub>h</sub> | `u32` | levels | derived level count |
| `18`<sub>h</sub> | `u32` | flags | `2`<sub>h</sub> generate mips, `100`<sub>h</sub> render target, `400`<sub>h</sub> UAV |
| `20`<sub>h</sub> | `void*` | renderTarget | sample count at +`09`<sub>h</sub> |
| `28`<sub>h</sub> | `u32` | width |  |
| `2C`<sub>h</sub> | `u32` | height |  |
| `30`<sub>h</sub> | `u32` | depth | PTexture3D only |

`Texture2DRecord` (`58`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | texture | ID3D11Texture2D |
| `08`<sub>h</sub> | `void*` | msaaTexture | ID3D11Texture2D |
| `10`<sub>h</sub> | `void*` | view | shader-resource view (`00623FA0`) |
| `18`<sub>h</sub> | `void*` | interface18 | an interface released with the others |
| `20`<sub>h</sub> | `void*` | uav | unordered-access view (`006241D0`) |
| `28`<sub>h</sub> | `void*` | copy | main-memory copy |
| `30`<sub>h</sub> | `void*` | interface30 | an interface released with the others |
| `40`<sub>h</sub> | `u8[24]` | update | pending upload entry |

`Texture3DMapLayout` (`C8`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | zero |  |
| `08`<sub>h</sub> | `void*` | level0 | first level's data |
| `10`<sub>h</sub> | `u32` | rowPitch0 |  |
| `14`<sub>h</sub> | `u32` | slicePitch0 |  |
| `18`<sub>h</sub> | `u8[176]` | levels1to11 | the same 16-byte entry for levels 1-11 |

`CubeMapLayout` (`2A8`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | zero |  |
| `08`<sub>h</sub> | `void*[6]` | level0Faces | one pointer per face |
| `38`<sub>h</sub> | `u32` | level0RowPitch |  |
| `40`<sub>h</sub> | `u8[616]` | levels1to11 | the same `38`<sub>h</sub>-byte entry for levels 1-11 |

`PConstantBufferD3D11` (`50`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | copySize | stride of the main-memory copies |
| `10`<sub>h</sub> | `void*` | copies | one copy per ring record |
| `18`<sub>h</sub> | `u32` | ringCount |  |
| `20`<sub>h</sub> | `u8[16]` | ring | ConstantBufferRecord inline for one record, else a pointer |
| `30`<sub>h</sub> | `u32` | byteWidth | bytes uploaded |
| `34`<sub>h</sub> | `u32` | usage | 2 = dynamic |
| `3C`<sub>h</sub> | `u32` | cpuAccess | `10000`<sub>h</sub> = write |
| `48`<sub>h</sub> | `u32` | created |  |

`ConstantBufferRecord` (`10`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | buffer | ID3D11Buffer |
| `08`<sub>h</sub> | `u32` | dirty | set by `0062C300` |
| `0C`<sub>h</sub> | `u32` | inUse |  |

`PStructuredBufferD3D11` (`68`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | count | elements |
| `04`<sub>h</sub> | `u32` | size | bytes per element |
| `08`<sub>h</sub> | `u32` | flags | 1 dynamic, 2 counter, 4 append, 8 staged data, `10`<sub>h</sub> raw |
| `18`<sub>h</sub> | `u32` | ringCount | `28`<sub>h</sub>-byte records: buffer, view, unordered-access view |
| `20`<sub>h</sub> | `void*` | ring |  |
| `48`<sub>h</sub> | `u8[24]` | desc | D3D11_BUFFER_DESC read back after creation |

Texture formats (initialisers `00163110`–`00163D8F`, one per format):

| Code | Name | Object | Bits | Flags | DXGI formats `+20`<sub>h</sub>–`+30`<sub>h</sub> |
|---|---|---|---|---|---|
| `00`<sub>h</sub> | `L8` | `02CF72C0` | 8 | `FF8`<sub>h</sub> | 0, `3D`<sub>h</sub> ×4 |
| `01`<sub>h</sub> | `A8` | `02CF72F8` | 8 | `11F8`<sub>h</sub> | 0, `41`<sub>h</sub> ×4 |
| `02`<sub>h</sub> | `LA8` | `02CF7330` | 16 | `1FF8`<sub>h</sub> | 0, `31`<sub>h</sub> ×4 |
| `03`<sub>h</sub> | `RG8` | `02CF7368` | 16 | `7F8`<sub>h</sub> | 0, `31`<sub>h</sub> ×4 |
| `04`<sub>h</sub> | `L16` | `02CF73A0` | 16 | `FF8`<sub>h</sub> | 0, `39`<sub>h</sub> ×4 |
| `05`<sub>h</sub> | `A16` | `02CF73D8` | 16 | `11F8`<sub>h</sub> | 0, `39`<sub>h</sub> ×4 |
| `06`<sub>h</sub> | `LA16` | `02CF7410` | 32 | `1FF8`<sub>h</sub> | 0, `24`<sub>h</sub> ×4 |
| `07`<sub>h</sub> | `RG16` | `02CF7448` | 32 | `7F8`<sub>h</sub> | 0, `24`<sub>h</sub> ×4 |
| `0B`<sub>h</sub> | `RGBA8` | `02CF7480` | 32 | `1FF8`<sub>h</sub> | 0, `1C`<sub>h</sub> ×4 |
| `0C`<sub>h</sub> | `ARGB8` | `02CF74B8` | 32 | `1FF8`<sub>h</sub> | 0, `57`<sub>h</sub> ×4 |
| `0D`<sub>h</sub> | `A2RGB10` | `02CF74F0` | 32 | `1FF8`<sub>h</sub> | 0, `18`<sub>h</sub> ×4 |
| `0E`<sub>h</sub> | `RGBA16` | `02CF7528` | 64 | `1FF8`<sub>h</sub> | 0, `0C`<sub>h</sub> ×4 |
| `0F`<sub>h</sub> | `DXT1` | `02CF7560` | 4 | `1E39`<sub>h</sub> | 0, `47`<sub>h</sub>, 0, `47`<sub>h</sub>, 0 |
| `10`<sub>h</sub> | `DXT3` | `02CF7598` | 8 | `1E39`<sub>h</sub> | 0, `4A`<sub>h</sub>, 0, `4A`<sub>h</sub>, 0 |
| `11`<sub>h</sub> | `DXT5` | `02CF75D0` | 8 | `1E39`<sub>h</sub> | 0, `4D`<sub>h</sub>, 0, `4D`<sub>h</sub>, 0 |
| `12`<sub>h</sub> | `BC4` | `02CF7608` | 4 | `239`<sub>h</sub> | 0, `50`<sub>h</sub>, 0, `50`<sub>h</sub>, 0 |
| `13`<sub>h</sub> | `BC5` | `02CF7640` | 8 | `1E39`<sub>h</sub> | 0, `53`<sub>h</sub>, 0, `53`<sub>h</sub>, 0 |
| `14`<sub>h</sub> | `BC6` | `02CF7678` | 8 | `1E39`<sub>h</sub> | 0, `5F`<sub>h</sub>, 0, `5F`<sub>h</sub>, 0 |
| `15`<sub>h</sub> | `BC7` | `02CF76B0` | 8 | `1E39`<sub>h</sub> | 0, `62`<sub>h</sub>, 0, `62`<sub>h</sub>, 0 |
| `1E`<sub>h</sub> | `RGBA16F` | `02CF76E8` | 64 | `1FFC`<sub>h</sub> | 0, `0A`<sub>h</sub> ×4 |
| `1F`<sub>h</sub> | `RGBA32F` | `02CF7720` | 128 | `1FFC`<sub>h</sub> | 0, `02`<sub>h</sub> ×4 |
| `20`<sub>h</sub> | `R16F` | `02CF7758` | 16 | `3FC`<sub>h</sub> | 0, `36`<sub>h</sub> ×4 |
| `21`<sub>h</sub> | `L16F` | `02CF7790` | 16 | `FFC`<sub>h</sub> | 0, `36`<sub>h</sub> ×4 |
| `22`<sub>h</sub> | `R32F` | `02CF77C8` | 32 | `3FC`<sub>h</sub> | 0, `29`<sub>h</sub> ×4 |
| `23`<sub>h</sub> | `L32F` | `02CF7800` | 32 | `FFC`<sub>h</sub> | 0, `29`<sub>h</sub> ×4 |
| `24`<sub>h</sub> | `RG16F` | `02CF7838` | 32 | `7FC`<sub>h</sub> | 0, `22`<sub>h</sub> ×4 |
| `25`<sub>h</sub> | `LA16F` | `02CF7870` | 32 | `1FFC`<sub>h</sub> | 0, `22`<sub>h</sub> ×4 |
| `26`<sub>h</sub> | `RG32F` | `02CF78A8` | 64 | `7FC`<sub>h</sub> | 0, `10`<sub>h</sub> ×4 |
| `27`<sub>h</sub> | `LA32F` | `02CF78E0` | 64 | `1FFC`<sub>h</sub> | 0, `10`<sub>h</sub> ×4 |
| `28`<sub>h</sub> | `DEPTH16` | `02CF7950` | 16 | `207A`<sub>h</sub> | 0, `35`<sub>h</sub>, `37`<sub>h</sub>, `38`<sub>h</sub>, `38`<sub>h</sub> |
| `29`<sub>h</sub> | `DEPTH24` | `02CF7988` | 32 | `207A`<sub>h</sub> | 0, `2C`<sub>h</sub>, `2D`<sub>h</sub>, `2E`<sub>h</sub>, `2E`<sub>h</sub> |
| `2A`<sub>h</sub> | `DEPTH24S8` | `02CF79C0` | 32 | `607A`<sub>h</sub> | 0, `2C`<sub>h</sub>, `2D`<sub>h</sub>, `2E`<sub>h</sub>, `2E`<sub>h</sub> |
| `2B`<sub>h</sub> | `DEPTH32` | `02CF79F8` | 32 | `207A`<sub>h</sub> | 0, `27`<sub>h</sub>, `28`<sub>h</sub>, `29`<sub>h</sub>, `29`<sub>h</sub> |
| `32`<sub>h</sub> | `R32` | `02CF7918` | 32 | `3F8`<sub>h</sub> | 0, `2A`<sub>h</sub> ×4 |
| `33`<sub>h</sub> | name string at `00D26D00` | `02CF7A30` | 0 | 0 | 0 ×5 |

Colour formats pass flag argument `1F8`<sub>h</sub>, block formats `38`<sub>h</sub>, depth formats `78`<sub>h</sub>. In the derived
flags, `200`<sub>h</sub>, `400`<sub>h</sub>, `800`<sub>h</sub> and `1000`<sub>h</sub> follow the channels the name lists (R, G, B, A; L sets
all three colour bits) and `2000`<sub>h</sub> and `4000`<sub>h</sub> mark depth and stencil.

## Shipped data

| Fact | Value |
|---|---|
| texture-format objects | 35, at `02CF72C0`–`02CF7A30`, `38`<sub>h</sub> bytes apart |
| block-compressed formats | 7: `DXT1`, `DXT3`, `DXT5`, `BC4`–`BC7` |
| depth formats | 4: `DEPTH16`, `DEPTH24`, `DEPTH24S8`, `DEPTH32` |
| feature levels asked for | `B000`<sub>h</sub>, `A100`<sub>h</sub>, `A000`<sub>h</sub>; below `B000`<sub>h</sub> the device is refused |
| default upload sizes | 4 MiB vertex, 1 MiB + 16 index, two of each per pair |

## State

| Address | What |
|---|---|
| `02CF7480` | the `RGBA8` format of the back buffer |
| `02CF79C0` | the `DEPTH24S8` format of the depth texture |
| `02CF7A30` | the null format every texture starts with |
| `01F7F5A0` | counter that picks a cube map's ring record |
| `01F7F590` | frame slot of the deferred upload queue |

## Modding notes

- The device needs feature level 11.0; the lower levels in the creation list are never kept.
- A texture created without CPU write access can still be mapped, but every map then works on a
  main-memory copy that is uploaded later through the queue, and the game logs a performance warning.
- A format's DXGI value is read from its object's `+24`<sub>h</sub>; replacing a format pointer changes the
  texture's format, bits per pixel and block rounding together.
- The refresh rate comes from the mode that matches the screen size, not the window size.

## Related

- [Phyre D3D11 draws and state](phyre-d3d11-draws-and-state.md): the draw calls, bind caches, data-block rings and the deferred upload queue.
- [Graphics adapters and vendor libraries](../Steam-And-Achievements/graphics-adapters-and-vendor-libraries.md): how the adapter is chosen and the multisample probe that ends device creation.
- [Phyre application](phyre-application.md): the framework that opens the window the swap chain draws into.
- [Phyre asset files](phyre-asset-files.md): the texture data a cluster load copies into these objects.
