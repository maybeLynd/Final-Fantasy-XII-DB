[Home](../../README.md) / [PhyreEngine](README.md) / Phyre D3D11 device and resources

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Phyre D3D11 device and resources: device and swap-chain creation, the texture formats, texture and buffer objects and how they are mapped, uploaded and released | system | PhyreEngine | Drawing and shaders | How PhyreEngine's Direct3D 11 renderer creates its device and swap chain on the chosen adapter, the 35 texture-format objects and the DXGI formats they carry, the 2D, 3D and cube-map texture objects with their rings of Direct3D resources, the constant and structured buffers, the two pairs of dynamic upload buffers in the render context, and the helpers that create, map, upload and release them. | 0x00625830, 0x00623320, 0x00624F70, 0x006250C0, 0x00625210, 0x00623B10, 0x0061ECD0, 0x00626D90, 0x0062CD40, 0x00616210, 0x02CF7A30, 0x0061FDA0, 0x00620250, 0x00620630, 0x0061E200, 0x0061E270, 0x0061E2E0, 0x00650660, 0x00628100, 0x0060DD70, 0x0060DE00, 0x00610990, 0x006264F0, 0x00626990, 0x00609870, 0x00609950, 0x0062C820, 0x0062BCB0, 0x0062BF40, 0x0062C100, 0x006505A0, 0x005DDBB0, 0x00615550, 0x0061D960, 0x00626060, 0x006097B0, 0x0062C300, 0x006239C0, 0x00616060, 0x0061F200, 0x0061F710, 0x006209C0, 0x0061C080, 0x00615790, 0x00607FA0, 0x005F0590, 0x00623F00, 0x005D8E40 |

## What the player sees

The window the game draws into, its back buffer and depth buffer, and every texture and constant
the shaders read are made by the code on this page. The swap chain is created windowed, in
`R8G8B8A8_UNORM`, and the device is refused unless the adapter reaches Direct3D feature level 11.0.

The swap chain starts at the refresh rate of the last mode, on the first output of the first adapter,
whose size is the screen's current size, or at 60/1 when none matches or the lookup fails
([The screen refresh rate](#the-screen-refresh-rate)). Later mode switches are a separate step
([Screen mode and aspect](../Graphics/screen-mode-and-aspect.md)).

Each finished frame is shown either in step with the screen's refresh (vsync) or held to the game's frame rate
by sleeping until the frame is due. With VSync setting 2 in full screen, vsync is dropped while the average GPU
time per frame is above about 16 ms (33 ms at sync interval 2), so a slow scene tears instead of halving its rate.

## How it works

### Building the render context

`0x005FD050` constructs the render context, the static `0x02CC0410`, with `0x00615840` the first time it is
asked for it. Among the members it builds are the back-buffer texture at `+0x170` and the depth texture
at `+0x2F8` (each zeroed and set up by `0x006160B0`), and the colour and depth render targets at
`+0x480` and `+0x4D0`. `0x005DC1C0(target, texture)` attaches a target to its texture: it stores the
texture at `+0x00`, sets bit `0x100` of the texture's `+0x18` and points the texture's `+0x20` at the
target unless another live target already holds it.

It also builds two `0x28`-byte records at `+0x520` and `+0x548` with `0x005DBF30`¹, which zeroes
the qwords `+0x00`, `+0x08` and `+0x18` and the dword `+0x10` of each and gives each the null format `0x02CF7A30` at
`+0x20`. `0x00607D10` then gives both one size, the first as `RGBA8` `0x02CF7480` and the second as `DEPTH24S8` `0x02CF79C0`². The first record's `+0x18` and `+0x1C` (context `+0x538` and `+0x53C`) are the width and
height that a post effect configured with a zero size takes ([post effect classes](phyre-post-effect-classes.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00615940`, `0x0061594D` |
| ² | `0x00625D0F`, `0x00625D28` |

</details>

When a member's constructor throws, the unwind actions of `0x00615840` destroy what has been built:

- `0x00616740` for each render target: `0x0062B890` when its `+0x18` or `+0x28` is set, which releases the
  views in its two arrays and the four interfaces at `+0x10`–`+0x28`, then `0x005DDB00`:
  - it frees each array's storage (pointers `+0x48` and `+0x38`) through `0x00584730` unless bit `0x80000000`
    of its count (`+0x40`, `+0x30`) is set, and zeroes both pointers and counts on every path
   ¹;
  - it then jumps to `0x006108C0`², which detaches the target from its texture `[target+0x00]` when
    the texture's `+0x20` points back at the target and the target's byte `+0x08` is 0, 1 or 2: it clears bit
    `0x100` of the texture's `+0x18` and zeroes the texture's `+0x20` and the target's `+0x00`
   ³;
- `0x00616520` and `0x00616780` for the eight `0x18`-byte records at `+0x08` and at `+0x570`, whose element
  destructor⁴ does nothing.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005DDB17`-`0x005DDB5A` |
| ² | `0x005DDB6A` |
| ³ | `0x006108E5`-`0x00610984` |
| ⁴ | `0x0016D6A0` |

</details>

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
   of the last mode matching the screen size, keeping 60/1 without one; `+0x18A4` takes the rate as a whole
   number and the values are logged (`Init Fresh rate x = %d, y = %d %d  get fresh = %d`).
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
 ¹, with the sample count at their `+0x09` (0 for one sample), and sizes the depth
  texture at `+0x2F8` as `DEPTH24S8`² with `0x0060DD70` and `0x00610990`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00620F60` |
| ² | `0x02CF79C0` |

</details>

It then sets the viewport¹, builds the helpers at `+0x7D8`², `+0xB50`³ and `+0x18C0`⁴, stores the start `clock()` at `+0x1850`, creates the two
upload-buffer pairs below, and on feature level 11.0 a 16-byte indirect-arguments buffer at `+0x7B8`
(misc flag `0x10`). It binds the colour and depth views with `OMSetRenderTargets` (`+0x108`), the
multisampled ones when the sample count is above 1, creates the default sampler at `+0x1820`⁵ and finally probes the multisample levels⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0061D3D0` |
| ² | `0x00624980` |
| ³ | `0x00624C30` |
| ⁴ | `0x006C9CD0` |
| ⁵ | `0x0061D9C0` |
| ⁶ | `0x00628690` |

</details>

After step 4 the function returns 9 when `GetBuffer` gives no buffer¹ and when
the `CreateBuffer` call for `+0x7B8` answers a negative value². A non-zero answer
of one of these calls is returned at once: `0x00620F60`³, `0x0060DD70`⁴,
`0x00624980`⁵, `0x00624C30`⁶, `0x006C9CD0`⁷, `0x00624F70`⁸,
`0x00625210`⁹ and `0x0061D9C0`¹⁰.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00625B7B`-`0x00625B83` |
| ² | `0x00625E25`-`0x00625E2A` |
| ³ | `0x00625C4A`, `0x00625CB9` |
| ⁴ | `0x00625C87` |
| ⁵ | `0x00625D3C` |
| ⁶ | `0x00625D53` |
| ⁷ | `0x00625D6A` |
| ⁸ | `0x00625DB5` |
| ⁹ | `0x00625DDB` |
| ¹⁰ | `0x00625E75` |

</details>

`0x00620F60` is called for a render target only while the target's qwords `+0x28` and `+0x18` are both 0¹. The answer is 0 only after `0x00628690`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00625C36`-`0x00625C40`, `0x00625CA3`-`0x00625CAF` |
| ² | `0x00625E79`-`0x00625E81` |

</details>

The function also stores 0 in the dword `+0x1890` before the call of step 4¹, clears bit
`0x1` of the dwords `+0x48C` and `+0x4DC`² and bit `0x2` of the dword `+0x310`³. Before the viewport call it stores the width in `+0x1864` and `+0x186C`, the height in
`+0x1868` and `+0x1870` and 0 in the qword `+0x185C`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00625A1F` |
| ² | `0x00625B94`, `0x00625C5E` |
| ³ | `0x00625C8F` |
| ⁴ | `0x00625CC3`-`0x00625CEA` |

</details>

### The screen refresh rate

`0x00623320(context, &rate, width, height)` creates a DXGI factory (`CreateDXGIFactory`, `0x0062335A`), takes adapter 0
(`EnumAdapters`, `+0x38`) and its output 0 (`EnumOutputs`, `+0x38`), and asks `GetDisplayModeList` (`+0x40`) for
format `0x1C`: first for the mode count, then for the modes, into a block of count × `0x1C` bytes from `0x0017D260`¹. Every listed mode whose width and height equal the arguments copies its 8-byte refresh
rate into `rate`, so the last match wins². With no match the rate stays 60/1.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006233C1`, `0x00623413` |
| ² | `0x00623430`-`0x00623449` |

</details>

When the factory, the adapter, the output or either mode list fails, the list is empty or the block cannot be
allocated, it skips the rest and `rate` keeps the 60/1 the caller put there. It frees the block with `0x00584730`
and releases the output, the adapter and the factory, each one it obtained¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0062345A`-`0x00623481` |

</details>

### The upload buffer pairs

The context holds two 0x58-byte pair objects, each with two vertex buffers and two index buffers
used alternately (layout below):

- `0x00624F70(pair, device, vbSize, ibSize)` at `+0x708`, sizes from `+0xF4` and `+0xF8`: dynamic
  buffers with CPU write access, a vertex size of 4 MiB and an index size of 1 MiB + 16 when the
  argument is 0, plus a 16-byte-aligned main-memory copy of each.
- `0x00624F70` stores the sizes at `+0x30` and `+0x34`¹. The index buffers and their copies
  are 16 bytes larger than `+0x34` whatever the argument². Both kinds have usage 2
  (dynamic), the vertex buffers bind flag 1 and the index buffers bind flag 2, and they are created without data.
- It creates only the buffers whose slot is still null³ and returns 9 at the first failed
  `CreateBuffer` (`+0x18`, `0x006250B5`), before any copy is made. It allocates each copy only when its slot is null
  (`0x00625060`, `0x00625078`; `0x0017D260`, alignment 16), stores the result without a test and returns 0.
- `0x00625210(pair, device, …)` at `+0x760`, sizes from `+0xFC` and `+0x100`, goes through `0x006250C0`
  with default usage and bind flag `0x80` added, which also makes the buffers raw (misc `0x20`). It
  then creates an unordered-access view of each: raw views (`R32_TYPELESS`, one element per 4 bytes,
  flag 1) for raw buffers, one element per stride for structured ones.
- `0x006250C0(pair, device, vbSize, ibSize, usage, bindFlags, cpuAccess)` sizes and creates the buffers as
  `0x00624F70` does: 4 MiB and 1 MiB for sizes of 0, stored at `+0x30` and `+0x34`, index buffers 16 bytes larger,
  only the null slots, 9 at the first failure⁴. It makes no main-memory copies and returns 0.
- Each buffer `0x006250C0` creates takes the given usage and CPU access and bind flag 1 or 2 with `bindFlags`
  added; misc `0x20` comes with any non-zero `bindFlags`⁵.
- `0x00625210` gives `0x006250C0` usage 0 and CPU access 0 and returns its non-zero result⁶. It reads each
  buffer's description (`GetDesc`, `+0x50`) and stores the views at `+0x38` (vertex) and `+0x48` (index) through
  `CreateUnorderedAccessView` (`+0x40`); a failure returns 9⁷, and success returns 0.
- A vertex buffer's view is raw for misc bit `0x20`⁸, structured for bit `0x40`⁹, and
  otherwise has format 0 and 0 elements. The index buffers always get raw views, whatever their misc flags
 ¹⁰. Each call stores four new views in those slots without releasing what they held.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00624FA6`, `0x00624FDE` |
| ² | `0x00624FD2`, `0x00625086` |
| ³ | `0x00625006`, `0x0062502A` |
| ⁴ | `0x006251FB` |
| ⁵ | `0x00625144`, `0x0062517A` |
| ⁶ | `0x00625250` |
| ⁷ | `0x00625392` |
| ⁸ | `0x006252B6` |
| ⁹ | `0x006252D0` |
| ¹⁰ | `0x00625320`-`0x0062537B` |

</details>

`0x00626D90(context, i)` makes slot `i` current (`+0x6F0`) and zeroes its used sizes in both pairs.
`0x0061ECD0(context, i)` uploads slot `i` of the first pair through `0x00623B10(pair, immediate context, i)`: each
non-empty buffer is mapped with `WRITE_DISCARD` and its used bytes are copied from the main-memory copy; 9 on a
failed map.

`0x00623B10` takes the vertex buffer first: when its used size `+0x20` + 4 × `i` is not 0 it maps the buffer
`+0x00` + 8 × `i` (`Map`, `+0x70`, `0x00623B5A`), copies from `+0x38` + 8 × `i` with `memcpy`¹ and
unmaps it (`Unmap`, `+0x78`). The index buffer follows the same way with the used size `+0x28`, the buffer `+0x10`
and the copy `+0x48`². A failed map or a null mapped pointer returns 9 at once³, so a failed vertex map leaves the index buffer as it was. The used sizes keep their values, and the
body returns 0 when both steps succeed.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00861EBA` |
| ² | `0x00623B90`-`0x00623BEA` |
| ³ | `0x00623C04` |

</details>

### Texture formats

A texture names its format through a pointer at `+0x00` to one of 35 static format objects
(`0x38` bytes). Each is built before `main` by its own initialiser, which calls `0x00616210(object,
name, code, flags, five DXGI formats)`; `0x00616210` runs `0x0062CD40` and stores the five formats at
`+0x20`–`+0x30`.

`0x0062CD40(object, name, code, flags)` stores the name at `+0x00`, 0 at `+0x08` (the registry link) and the code at
`+0x10`¹, returns the object, and derives from the code:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0062CD43`-`0x0062CD4A` |

</details>

- the bits per pixel at `+0x14`, from a switch over the code; the codes `0x19`–`0x1C` and every code above
  `0x32` take its default, 0 bits per pixel and no channel mask¹;
- the flags at `+0x18`: the argument's bits outside `0x7E07`, a channel mask from the same switch,
  bit `0x1` for the block-compressed codes `0x0F`–`0x18` and `0x1D`, bit `0x2` for the depth codes
  `0x28`–`0x2B` and `0x31`, bit `0x4` for the float codes `0x1E`–`0x27`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0062CD52`, `0x0062CEC1` |

</details>

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
count at `+0x14`: `0x0060DD70(texture, width, height, format, mips)` for 2D and `0x0060DE00(texture, width, height,
depth, format, mips)` for 3D. Both return 3 when the larger side is below `1 << mips`, and with bit `0x2` of
`+0x18` (generate mips) the level count is the base-2 logarithm of the largest side.

The 3 comes only for a non-zero `mips`, from the larger of width and height alone (the depth takes no part), and
before any store¹. When the arguments all equal the stored values
(width `+0x28`, height `+0x2C`, for 3D depth `+0x30`, format `+0x00`, mips `+0x10`), they return 0 with no store².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0060DD77`-`0x0060DD91`, `0x0060DE07`-`0x0060DE21` |
| ² | `0x0060DD97`-`0x0060DDAC`, `0x0060DE2C`-`0x0060DE47` |

</details>

Otherwise they store the arguments there. The level count is then `n = 0; while (s > 1) { s >>= 1; n++; }`,
the rounded-down base-2 logarithm `floor(log2(s))` for `s >= 1`, of the largest side `s` (for 3D, of all three),
`s = max(w, h)` or `max(w, h, d)`¹, with generate mips (bit `0x2` of
`+0x18`), and `mips` itself without; `+0x14` is written only when that value differs from it, and they return 0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0060DDC7`-`0x0060DDE7`, `0x0060DE66`-`0x0060DE89` |
| ² | `0x0060DDAE`-`0x0060DDF3`, `0x0060DE49`-`0x0060DE95` |

</details>

`0x00610990` recomputes `+0x14` alone, the same way from the stored `+0x28` and `+0x2C`, or from `+0x10` without
generate mips¹. `0x005DCC10` is the 3D base initialiser: format `0x02CF7A30`, `+0x08` = `0x300`,
`+0x18` = 2.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00610990`-`0x006109C8` |

</details>

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
- `0x00620630` creates nothing and returns, testing in this order, 5 when its fifth argument is non-zero
  (`0x00620671`-`0x0062068A`; both callers give 0), 0x17 when the device pointer, qword `+0x108` of the object
  `0x005FD050` returns, is null¹, and 5 when the render target at `+0x20` is set and has
  a non-zero sample count (byte `+0x09`, `0x00620730`-`0x00620747`).
- It returns 9 at the first failed `CreateTexture2D`, without the description, name or views², and otherwise the first non-zero result of the view creators it was asked for (`0x0061FC50` for a
  shader view, `0x00620E10` for an unordered-access view, `0x0062095F`-`0x00620983`), else 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0062069C`-`0x006206B2` |
| ² | `0x006208E0`, `0x006209AF` |

</details>

The "ensure" functions create the ring only when its first texture is missing and then set the
created word: `0x0061E200` (2D) and `0x0061E270` (3D) pass a shader view and `+0x18` bit `0x400` as the
UAV request, `0x0061E2E0` (cube) a shader view only, each with 0 as the second and fifth arguments of
`0x0061FDA0`, `0x00620250` or `0x00620630`.

They set the created word (`+0xBC`, `+0x8C`, `+0xA4`) to 1 on both paths, also when the create function fails,
and return its result, or 0 when the first texture is already there¹. With a ring count of 0 the first-texture pointer is null and the read at
address 0 faults².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0061E247`, `0x0061E259`, `0x0061E2B7`, `0x0061E2C9`, `0x0061E31E`, `0x0061E330` |
| ² | `0x0061E227`, `0x0061E297`, `0x0061E307` |

</details>

`0x00650660` returns 7 for a 3D texture still in the
null format, 0 when it is created, and otherwise calls `0x0061E270`.

`0x00628100(texture, count)` re-creates a 2D texture: it releases a created one, resizes the ring¹ and
creates it again. The release runs only while the created word `+0xBC` is set², and its non-zero
result is returned³. It then waits, 1 ms at a time, until every record's in-use count is 0⁴, and a failed resize returns its result, `0xD` when the new ring cannot be allocated⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00627DA0` |
| ² | `0x0062810A` |
| ³ | `0x0062811F` |
| ⁴ | `0x0062B100` |
| ⁵ | `0x0062813B`, `0x00627DF9` |

</details>

It creates the ring only when the first texture is missing, as `0x0061E200` does: `0x0061FDA0` with a shader view
and `+0x18` bit `0x400` as the UAV request¹. It sets the created word to 1 whatever the
creation returns² and returns that result, or 0 when the first texture exists. A count of 0 leaves
the ring pointer null, and the read of the first texture at `0x0062815B` faults at address 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00628160`-`0x00628176` |
| ² | `0x0062817D` |

</details>

### Mapping textures for writing

`0x00609870` (3D) and `0x00609950` (cube) take a ring record, wait 1 ms at a time while its in-use count is
above 0, map it and set the state byte `+0x08` to 2. The 3D one steps to the record after `+0x0C`,
the cube one takes the counter `0x01F7F5A0` modulo the ring size; both return 7 for the null
format.

Before that, when the created word is 0 they create the ring with `0x0061E270` or `0x0061E2E0` and return its result
when it is not 0¹. The 3D index wraps to 0 when the one after `+0x0C` equals the ring
count²; neither body stores the index, `+0x0C` or the counter.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006098A8`, `0x00609988` |
| ² | `0x006098D7`-`0x006098DC` |

</details>

The wait reads the record's `+0x20` (`0x28`-byte records for 3D, `0x40`-byte for cube) and calls `Sleep(1)`¹. The map is `0x006264F0` or `0x00626990` with the record index and the caller's layout; the
state byte is set only when it returns 0, and its result is returned². A ring count of 0
counts as 1 with a null base, so the in-use read faults.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0060990B`, `0x006099F5` |
| ² | `0x00609932`, `0x00609A1C` |

</details>

`0x006264F0` (3D) and `0x00626990` (cube) fill the caller's layout of up to 12 levels (layouts below).
Level sizes come from the format's bits per pixel `bpp` (format `+0x14`). Each level's sides are
`max(side >> 1, 1)` of the level before; for a block format (format `+0x18` bit `0x1`) the width `w` and height `h` are
first rounded up, `(side + 3) & ~3`. A level's row pitch is `bpp x w x k >> 3`, `k` 4 for a block format and 1
otherwise, its slice pitch `bpp x w x h >> 3` and its size the slice pitch times the depth¹; a cube
level is square, `bpp x w x w >> 3`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006264F0` |
| ² | `0x00626990` |

</details>

- Without CPU write access (the description's `+0x1C` bit `0x10000`) they log
  `Performance warning: mapping texture that was not created with D3D11_CPU_ACCESS_WRITE flag
  specified - main memory buffer will be allocated.` and hand out a main-memory copy, allocated on
  first use at the full size of the levels (six faces for a cube).
- With it, `0x006264F0` maps each level on the immediate context (`Map`, `+0x70`) with `WRITE_DISCARD`
  for a dynamic texture and `WRITE` otherwise, under the context lock; a failed map returns 9.

`0x0062C820(cube, record, layout)` copies the `0x2A8`-byte layout to `+0xA8`, sets the record's update
entry to this cube and record index, and queues it for the frame slot `0x01F7F590` (`0x0062EB90`, the
deferred upload queue of the draw page). It returns 3 for a record index past the ring¹ and `0x15`
when the record has no texture². Otherwise it works under the context lock (`0x00615BC0` at
`0x0062C8A1`, released through `0x005CD7D0` at `0x0062C985`) and returns 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0062C85A` |
| ² | `0x0062C892` |

</details>

The update entry is the record's `+0x28`: the cube goes to its `+0x08` and the index to its `+0x10`¹. The queue pointer `0x01F7F5B8` goes to `0x0062EB90` without the null test the releases make; with a null
queue and the slot below 4, the insert's read at `0x00199DC9` is at most address `0xC0` and faults. A ring count of
0 leaves the ring pointer null, and the record read at `0x0062C88C` faults at address 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0062C94B`, `0x0062C94F` |

</details>

### Releasing textures

- `0x006505A0` takes `{texture, kind}` and releases a created texture: kind 0 `0x0062BCB0` (2D), 1
  `0x0062BF40` (3D), 2 `0x0062C100` (cube).
- The kind is the byte at `+0x08`, and the release is a tail jump whose result `0x006505A0` returns. It returns
  without a release for a null argument¹, a null texture, a kind above 2² or a texture
  whose created word is 0: `0x00625F00`, `0x00625F10` and `0x00625F20` test `+0xBC`, `+0x8C` and `+0xA4`.
- `0x0062BCB0` clears the created word, releases the render
  target's views first when it has them³, and for every ring record takes its pending
  upload off the queue⁴, frees the main-memory copy at `+0x28` and releases the six
  interfaces at `+0x10`, `+0x18`, `+0x20`, `+0x00`, `+0x08` and `+0x30`.
- `0x0062BF40` (3D) clears the created word `+0x8C`⁵ and releases the render target's views through
  `0x0062B890` under the test `0x0062B870` makes, returning a non-zero result⁶. For every `0x28`-byte
  record it releases the interfaces at `+0x08`, `+0x10` and `+0x00` and frees the main-memory copy at `+0x18`
 ⁷, zeroing each slot. It makes no `0x0062EC70` call, and returns 0.
- `0x0062C100` (cube) does the same with the created word `+0xA4`⁸ and `0x40`-byte records. Like
  `0x0062BCB0`⁹, it takes a record's upload entry `+0x28` off the queue¹⁰ only
  when the copy at `+0x18` is set and `0x01F7F5B8` is not null¹¹, and frees that copy.
  Then it releases `+0x08`, `+0x10` and `+0x00`.
- Before that, each of the three waits, 1 ms at a time (`Sleep`, `0x005CCB80`), until every ring record's in-use
  count is 0: `0x0062B100` (2D, `0x0062BCBE`), `0x0062B170` (3D, record `+0x20`) and `0x0062B1E0` (cube, record `+0x20`).
  With a ring count of 0 the ring pointer is null, and the first count read faults below address `0x40`
 ¹².
- `0x005DDBB0` destroys the placeholder set below: it releases the sampler at `+0x568`
 ¹³ and each of the three textures that is created. `0x006167C0` releases the sampler's interface at
  `+0x20` (`+0x588` of the set) when it is set, zeroes it and clears bit `0x80` of its word `+0x1C` (`+0x584`);
  it ends in a jump to the no-op `0x0016D6A0`.
- `0x005DDBB0` takes the cube map at `+0x218` first, then the 3D texture at `+0x188` and the 2D one at `+0x000`:
  each is released through `0x0062C100`, `0x0062BF40` or `0x0062BCB0` when its created word is set¹⁴, then destroyed by `0x00616D20`, `0x00616CC0` or `0x00616C60` whether it was created or not.
- Each of those destructors waits 1 ms at a time until no ring record is in use¹⁵ and calls the same release function again. It frees the ring's storage with `0x00584730` when the
  count is above 1, bit `0x80000000` of the count is clear and the pointer is set, and zeroes the count and the
  pointer.
- Their base part¹⁶ logs `A PTextureCommonBase object is being destroyed whilst
  still mapped` when the byte `+0x08` is set, and passes a render target at `+0x20` to `0x006108C0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006505A7` |
| ² | `0x006505C7` |
| ³ | `0x0062B870` |
| ⁴ | `0x0062EC70` |
| ⁵ | `0x0062BF5A` |
| ⁶ | `0x0062BF79` |
| ⁷ | `0x00584730` |
| ⁸ | `0x0062C11A` |
| ⁹ | `0x0062BD38`, `0x0062BD62` |
| ¹⁰ | `0x0062EC70` |
| ¹¹ | `0x0062C193`, `0x0062C1C2` |
| ¹² | `0x0062B12E`, `0x0062B19E`, `0x0062B20E` |
| ¹³ | `0x006167C0` |
| ¹⁴ | `0x00625F20`, `0x00625F10`, `0x00625F00` |
| ¹⁵ | `0x0062B1E0`, `0x0062B170`, `0x0062B100` |
| ¹⁶ | `0x005DE390`, `0x005DE310`, `0x005DE290` |

</details>

### Placeholder textures

`0x00607FA0(set, options)` fills a set of three textures, when byte `+0x01` of `options` is set: a 2D
texture at `+0x000`, a 3D one at `+0x188` and a cube map at `+0x218`, each made only when the flags of
the `RGBA8` format¹ have bit `0x8`, `0x10` or `0x20` respectively.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02CF7498` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | It sizes the texture 4×4 (×4 for 3D) in `RGBA8` with no mips and sets `+0x18` bit `0x200`. |   |
| 2 | It maps the next ring record, fills every level with a checkerboard of `0xFF00FF00` and `0xFFFF00FF` (green and magenta in `R8G8B8A8`; `0x005F0590` for the 2D one, inline for the others) and commits it. | `0x0062C360`, `0x0062C570`, `0x0062C820` |
| 3 | It creates the texture when it is not created yet. | `0x0061E200`, `0x0061E270`, `0x0061E2E0` |

It then resets the fields of the sampler at `+0x568` whose word `+0x584` has bit `0x80` clear.

`0x005F0590(data, width, height, rowPitch)` writes `width` dwords on each of `height` rows, the rows `rowPitch` bytes
apart: `0xFFFF00FF` where bit `0x1` of row XOR column is set and `0xFF00FF00` where it is clear, so each square is
one texel¹. A null `data` or a height of 0 returns with no store².
The 2D placeholder gives it the mapped 4×4 level 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005F05C0`-`0x005F05DD` |
| ² | `0x005F059B`, `0x005F05A3` |
| ³ | `0x0060808F` |

</details>

The 2D commit `0x0062C360(texture, index, layout)` returns 3 for an index at or past the ring count (`+0x30` without
bit `0x80000000`, 1 when 0; `0x0062C39D`) and `0x15` for a ring record whose first qword is 0¹. With
bit `0x10000` of `+0xB4` set it unmaps subresources 0 to min(`+0x10`, 11), or 0 alone when `+0x18` has bit `0x2`,
on the immediate context (`+0x110` of `0x005FD050()`, `Unmap` at `+0x78`, `0x0062C51A`) under the context lock², and returns 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0062C3D0` |
| ² | `0x00615BC0` |

</details>

With the bit clear it unmaps nothing: it copies the `0xC8`-byte layout to `+0xC0`, stores the texture and the
index at `+0x48` and `+0x50` of the record, in its update entry at `+0x40`, queues that entry for the frame slot
`0x01F7F590`¹ and returns 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0062EB90`, `0x0062C402`-`0x0062C4C7` |

</details>

### Constant buffers

A `PConstantBufferD3D11` (`0x50` bytes, constructor `0x00615550`) keeps a main-memory block at `+0x10`
with one copy per ring record, a ring of `0x10`-byte records at `+0x18`/`+0x20` (buffer, dirty word,
in-use count) and a `D3D11_BUFFER_DESC` from `+0x30`.

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `0x006097B0` steps to the next record, waits while it is in use, creates the buffers first when needed, and hands out the record's copy with `0x00626060`: `+0x10` plus `+0x00` × the record index, logging `Performance warning: mapping buffer that was not created with D3D11_CPU_ACCESS_WRITE flag specified - main memory buffer will be allocated.` without CPU write. | `0x0061D960` |
| 2 | `0x00626060(buffer, i, &copy)` returns 3 for an index past the ring and `0x15` when record `i` has no buffer. Otherwise it logs that warning when `+0x3C` lacks bit `0x10000`, stores `+0x10` plus the 32-bit product of `+0x00` and `i` through `copy` and returns 0. | `0x0062608D`<br>`0x006260CF`<br>`0x006260E4`<br>`0x00626100`-`0x0062610E` |
| 3 | `0x0062C300(buffer, i)` marks record `i` dirty; 3 for an index past the ring, `0x15` with no buffer. It stores 1 in the record's dirty word `+0x08` and returns 0. In both, the ring count at `+0x18` counts as at least 1; with a count of 0 the ring pointer is null, and the read of record 0's buffer faults at address 0. | `0x0062C34F`<br>`0x006260C8`, `0x0062C342` |
| 4 | When a shader binds it, `0x006239C0(buffer, i)` maps a dirty record (`WRITE_DISCARD` when the usage at `+0x34` is 2, else `WRITE`), copies `+0x30` bytes from its copy, unmaps and clears the dirty word. |   |

`0x00623EB0(buffer, i)` returns record `i`'s buffer, or null past the ring; `0x00623F00` does the same for
a structured buffer.

The steps of the list above, at the bytes:

- When the created word `+0x48` is 0¹, `0x006097B0` calls `0x0061D960` and returns its result when that
  is not 0². Its record is the one after `+0x04`, 0 when that equals the ring count, and
  the body leaves `+0x04` as it is.
- `0x006097B0` then calls `Sleep(1)` while the record's `+0x0C` is above 0³, sets the byte
  `+0x08` to 1 when `0x00626060` returns 0⁴, and returns that result.
- `0x0061D960` reads the first record's buffer and, when it is null, calls `0x0061F070(buffer, +0x00, 0)`
 ⁵. It sets the created word `+0x48` to 1 on both paths, also when `0x0061F070` fails, and returns
  `0x0061F070`'s result, or 0. With a ring count of 0 the record pointer is null and the read at address 0
  faults⁶.
- `0x006239C0` returns 0 at once for a clean record⁷. Under the context lock⁸ it maps the
  record's buffer on the immediate context `+0x110` (`Map`, `+0x70`, `0x00623A65`), copies with `memcpy` from
  `+0x10` + `+0x00` × `i`⁹, unmaps (`Unmap`, `+0x78`) and returns 0.
- A failed map or a null mapped pointer makes `0x006239C0` release the lock and return 9 with the dirty word
  still set¹⁰. The index `i` meets no bound test against the ring count.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00625EC0` |
| ² | `0x006097C0`-`0x006097D3` |
| ³ | `0x00609830`-`0x0060983F` |
| ⁴ | `0x0060985C` |
| ⁵ | `0x0061D994` |
| ⁶ | `0x0061D987` |
| ⁷ | `0x00623A0F` |
| ⁸ | `0x00615BC0` |
| ⁹ | `0x00623A83` |
| ¹⁰ | `0x00623AC1`-`0x00623AE6` |

</details>

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

Both read the flags from the description (bind flags `+0x50`, misc flags `+0x58`), return 0 at once when their
bind flag is clear¹ and work under the context lock². For each ring record they
call `CreateShaderResourceView` (`+0x38`, `0x0061F806`) or `CreateUnorderedAccessView` (`+0x40`, `0x00620AE8`) on the
record's buffer and store the view at the record's `+0x08` or `+0x10`. The first failure releases the lock and
returns 9³; otherwise they return 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0061F735`, `0x006209E0` |
| ² | `0x00615BC0` |
| ³ | `0x0061F84B`, `0x00620B2D` |

</details>

`0x0061F710` passes a description only for a raw buffer (misc `0x20`, view dimension `0xB`), and a null one, a view
of the whole buffer, otherwise¹. `0x006209C0` always passes a buffer view (dimension 1). A raw
buffer gets `R32_TYPELESS`, one element per 4 bytes and flag 1 alone; any other gets format 0 and `+0x00`
elements, with flag 4 when buffer flag 2 is set, else flag 2 when buffer flag 4 is set, else 0². A ring count of 0 counts as one record with a null base, so the first buffer read faults.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0061F754`-`0x0061F78D` |
| ² | `0x00620A25`-`0x00620A66` |

</details>

### Sampler filters

The sampler builder `0x0061D9C0` turns the engine's filter bytes into a `D3D11_FILTER` with
`0x0061C080(min, mag, comparison, maxAnisotropy)`. A maximum anisotropy of 2 or more gives `0x55` (anisotropic);
a comparison sampler adds `0x80` to every result.

`0x0061D9C0(sampler)` returns 0 at once when `+0x20` is already set¹, and when the device pointer
`+0x108` of the context `0x005FD050` answers is null it creates nothing and returns 0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0061D9DE` |
| ² | `0x0061D9EC`-`0x0061D9FC` |

</details>

Otherwise it calls the device's `CreateSamplerState` (`+0xB8`) into `+0x20`¹
and returns `0xE` when that answers a negative value or leaves `+0x20` null². After a successful call it passes the new object, the sampler,
the text `PSamplerState` and the sampler again to `0x0061C550`³, sets bit `0x80`
of `+0x1C`⁴ and returns 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0061DB1C`-`0x0061DB77` |
| ² | `0x0061DB82`-`0x0061DB8D`, `0x0061DBD0` |
| ³ | `0x0061DB86`-`0x0061DB9C` |
| ⁴ | `0x0061DBA1`-`0x0061DBA8` |

</details>

| `min` | `mag` 0 | `mag` non-zero |
|---|---|---|
| 0, 2 | `0x00` | `0x04` |
| 1, 3 | `0x10` | `0x14` |
| 4 | `0x01` | `0x05` |
| 5 | `0x11` | `0x15` |
| any other | `0x00` | `0x00` |

The run setup's `0x0064A0E0` (called at `0x0079F50C`, [Phyre application](phyre-application.md)) builds two
samplers this way. Unless bit `0x80` of an object's `+0x34` is set¹, it presets the
five bytes at `+0x18` and passes them to `0x0061D9C0`². It builds the
second only when the first returns 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02D34734`, `0x02D3515C` |
| ² | `0x0064A3F9`-`0x0064A46A`, `0x0064A482`-`0x0064A4EC` |

</details>

| Byte offset | object `0x02D34700` | object `0x02D35128` |
|---|---|---|
| `+0x18` | `0x02D34718` = 0 | `0x02D35140` = 1 |
| `+0x19` | `0x02D34719` = 0 | `0x02D35141` = 1 |
| `+0x1A` | `0x02D3471A` = 2 | `0x02D35142` = 2 |
| `+0x1B` | `0x02D3471B` = 2 | `0x02D35143` = 2 |
| `+0x1C` | `0x02D3471C` = 2 | `0x02D35144` = 2 |

At its start `0x0064A0E0` points `0x02D35178` at `0x01F2E820`. When the pointer named other storage and bit
`0x80000000` of the word `0x02D35170` was clear, it first passes that storage and the word's low 31 bits to
`0x001B7170`. It then stores `0x01F2E820`, sets the word to `0x80000001`¹ and writes 2 at
`0x01F2E838`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0064A0EB`-`0x0064A149` |
| ² | `0x0064A13B` |

</details>

### GPU timer queries

`0x00615790` builds an object with three Direct3D queries from `CreateQuery` (`+0xC0`): a
timestamp-disjoint query (type 3) at `+0x10` and two timestamp queries (type 2) at `+0x18` and
`+0x20`, after `0x005DBFE0` has cleared `+0x00` and the byte `+0x08`.

### Render targets in a cluster

`0x005D8E40(cluster, texture)` creates one `PRenderTarget` instance in a cluster (`0x006394E0`, with
descriptor `0x02CB76A0`) and initialises it with `0x00615C90`; it returns null when no object results.
It calls `0x006394E0(cluster, 1, 0x02CB76A0, 0)`¹ and takes the instance from `+0x60` of the result²: a null result or a null `+0x60` returns null³. Otherwise it calls
`0x00615C90(instance, texture)`⁴ and returns the instance; `0x00615C90` attaches the instance to the
texture with `0x005DC1C0`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005D8E65` |
| ² | `0x005D8E76` |
| ³ | `0x005D8E84` |
| ⁴ | `0x005D8E93` |
| ⁵ | `0x00615C99` |

</details>

Ten call sites in `0x0064A000`–`0x006560E0`
use it (`0x0064A066` to `0x0065612E`).

### Presenting a frame

The render thread's block `0x19` arm `0x006234A0(context)` shows each finished frame. After the device call
`+0x378` it returns 0 without a swap chain (`+0x118`). Its sync interval is `0x0017ECE0()`, the value `0x00184960`
posts to `0x01DF08F8` ([startup constants](../Engine-Core/startup-constants.md)), and 1 when the
refresh rate `+0x18A4` is below 31.

It uses vsync when the VSync byte `+0x1848` is set and either the swap chain is full screen (`+0x1890`) or
desktop composition is off (`DwmIsCompositionEnabled`, `0x00623517`).

In full screen with VSync setting 2 (byte `+0x1849`) it keeps a running average, `avg = sum / n`, of the GPU frame
time, the double `+0xD70` of the console object that the frame-marker table stores
([post-processing](../Graphics/post-processing.md)) and `0x0017D880` returns. Each frame adds it
to `0x02CF2550` and counts `0x02CF2548` up, `sum = [0x02CF2550] + 0x0017D880()` and `n = [0x02CF2548] + 1`; above 30
frames the count stays 30 and the sum loses one average, `n > 30 ? (n = 30, sum = sum - avg)`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00623564`-`0x006235AF` |

</details>

While no fade layer other than 3 runs (`0x0022A040`, [screen fades](../Graphics/screen-fades.md)),
the monster viewer's byte `+0x118` is clear¹ and the post-process parameter object's byte `+0x1E9`
is set², vsync stays on only while `avg < (0x0017ECE0() == 2 ? 0.0327 : 0.0158)`: while that average
is below 0.0327 s³ at sync interval 2, or 0.0158 s⁴ otherwise⁵.
Without vsync the interval is 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00181DD0` |
| ² | `0x00182780` |
| ³ | `0x00D56050` |
| ⁴ | `0x00D56048` |
| ⁵ | `0x006235B7`-`0x006235F6` |

</details>

`IDXGISwapChain::Present` (vtable `+0x40`) gets the interval and the flag `DXGI_PRESENT_TEST` (1) while the
countdown `+0x18A8` is not 0. `DXGI_STATUS_OCCLUDED`¹ sets the countdown to 1, any other success
lowers it by 1 while it is above 0², and a failure makes the arm return 0. The swap-chain
resize `0x006278B0` sets it to 8 divided by the interval, `[+0x18A8] = 8 / 0x0017ECE0()` (unsigned), when
`0x00180170()` is false (`0x006278C4`-`0x006278DD`,
[screen mode and aspect](../Graphics/screen-mode-and-aspect.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x087A0001` |
| ² | `0x00623650`-`0x0062365C` |

</details>

A frame limiter runs after an occluded vsync present, and on every frame without vsync while the byte
`0x01F2DE89` is set; it is 1 in the file and no instruction writes it. Its target is the unraised interval
× 1/60 s¹ when the refresh rate is a multiple of 10, otherwise × 0.0166833 s (`0x00900378`, 59.94 Hz):
`target = 0x0017ECE0() × ([+0x18A4] % 10 == 0 ? 1/60 : 0.0166833)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x009010A0` |
| ² | `0x00623671`-`0x006236A4` |

</details>

The limiter begins the multimedia timer period ([Phyre application](phyre-application.md)) and reads the time
since engine start (`0x005CC930()` minus `0x02CB60E8`). The last frame time `0x01F2DF10` starts as `DBL_MAX`
(`7FEFFFFFFFFFFFFF` in the file, compared with `0x009010A8`); at that value it becomes the time less one target¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00623704` |

</details>

While the time since `0x01F2DF10` is short of the target, it sleeps the remaining milliseconds (times -1000.0,
`0x00D56058`) rounded down to a multiple of the timer period `0x02CF2540`, less 1: `Sleep(ms - ms % [0x02CF2540] - 1)`
with `ms = (u32)((now - [0x01F2DF10] - target) × -1000.0)` and now that time, the rounding only when `0x02CF2540` is
not 0 and no sleep when that value is 0. It then calls `Sleep(0)` until the target is reached¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0062370C`-`0x006237AB` |

</details>

`0x01F2DF10` then advances by one target, or to the time less one target when the frame is more than a target late:
`[0x01F2DF10] = now - min(target, now - [0x01F2DF10] - target)`¹. Without vsync the frame is
then presented at interval 0², with the same countdown.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006237AD`-`0x006237B5` |
| ² | `0x006237C6` |

</details>

After a vsync present that was not occluded, when `[0x02CF2544] != 0`, it ends the timer period unless the average
above is in use, `timeEndPeriod([0x02CF2540])`, clearing `0x02CF2544` when the call returns 0¹,
and advances `0x01F2DF10` by one target, `[0x01F2DF10] = [0x01F2DF10] + target`². Last,
when the buffer count
`+0x184C` differs from the description's `+0x148`, it copies it there and resizes the swap chain (`0x006278B0`
with the size `+0x120`, `+0x124`), and returns 1.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0062380A`-`0x00623831` |
| ² | `0x00623862`-`0x00623871` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

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
| `+0x0480` | `u8[80]` | colourTarget | PRenderTarget; sample count at `+0x09` |
| `+0x04D0` | `u8[80]` | depthTarget | PRenderTarget; sample count at `+0x09` |
| `+0x06F0` | `u32` | uploadSlot | set by `0x00626D90` |
| `+0x0708` | `u8[88]` | vertexIndexUpload | UploadBufferPair, sizes from `+0xF4` and `+0xF8` |
| `+0x0760` | `u8[88]` | rawUpload | UploadBufferPair, sizes from `+0xFC` and `+0x100` |
| `+0x07B8` | `void*` | indirectArgs | 16-byte ID3D11Buffer, feature level 11.0 |
| `+0x1848` | `u8` | vsync | 1 for VSync settings 1 and 2 (`0x0062AAB0`); `0x006234A0` presents with vsync while set |
| `+0x1849` | `u8` | adaptiveVsync | 1 for VSync setting 2 only (the word `0x101` with `+0x1848`) |
| `+0x184C` | `u32` | bufferCount | the swap chain's buffer count; 1 from the constructor |
| `+0x1850` | `f64` | startClock | clock() at creation |
| `+0x1878` | `void*` | factory | IDXGIFactory |
| `+0x1880` | `void*` | adapter | IDXGIAdapter chosen at start-up |
| `+0x1890` | `u32` | fullscreen | 1 when GetFullscreenState (`+0x58`) reports full screen |
| `+0x18A4` | `u32` | refreshRate | numerator / denominator |
| `+0x18A8` | `u32` | testPresents | presents left with DXGI_PRESENT_TEST; 8 / interval at a resize |

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
| `+0x28` | `u32` | BufferCount | from context `+0x184C` |
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
| `+0x38` | `void*[2]` | vertexCopy | main-memory copies; unordered-access views in the pair at `+0x760` |
| `+0x48` | `void*[2]` | indexCopy | main-memory copies; unordered-access views in the pair at `+0x760` |

`TextureFormat` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | name | for example RGBA8 |
| `+0x08` | `void*` | next | registry link: 0 from `0x0062CD40`, the old head on insert (`0x0062D152`), 0 on unlink (`0x0062D72C`) |
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
| `+0x20` | `void*` | renderTarget | sample count at `+0x09` |
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

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

| Fact | Value |
|---|---|
| texture-format objects | 35, at `0x02CF72C0`–`0x02CF7A30`, `0x38` bytes apart |
| block-compressed formats | 7: `DXT1`, `DXT3`, `DXT5`, `BC4`–`BC7` |
| depth formats | 4: `DEPTH16`, `DEPTH24`, `DEPTH24S8`, `DEPTH32` |
| feature levels asked for | `0xB000`, `0xA100`, `0xA000`; below `0xB000` the device is refused |
| default upload sizes | 4 MiB vertex, 1 MiB + 16 index, two of each per pair |

</details>

## State

<details>
<summary>Show the state it keeps</summary>

| Address | What |
|---|---|
| `0x02CF7480` | the `RGBA8` format of the back buffer |
| `0x02CF79C0` | the `DEPTH24S8` format of the depth texture |
| `0x02CF7A30` | the null format every texture starts with |
| `0x01F7F5A0` | counter that picks a cube map's ring record |
| `0x01F7F590` | frame slot of the deferred upload queue |
| `0x01F2DF10` | `f64`, the frame limiter's last frame time (`DBL_MAX` at start) |
| `0x01F2DE89` | `u8`, 1: the frame limiter runs without vsync |
| `0x02CF2548` | `u32`, frames in the GPU-time average, at most 30: `n = n + 1 > 30 ? 30 : n + 1` (`0x00623564`, `0x006235A5`) |
| `0x02CF2550` | `f64`, the sum of that average: `sum = sum + 0x0017D880()`, less `sum / n` when n passes 30 (`0x00623573`-`0x006235AF`) |

### The texture-format registry

The `PRendering` init calls `0x0062D0D0`¹, which puts each texture-format object on a registry keyed by its
name (`+0x00`) and linked through its `+0x08`, and stores the object's address in the table `0x02CF7120` at the
object's code (`+0x10`). It inserts `L8`, `A8`, `LA8` and `RG8` itself and the rest through `0x0062D040`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00608D96` |

</details>

Each insert
walks the list comparing names and fails with `0x12` for a name already present, or `0x11` for a null name;
otherwise it stores the old head in the object's `+0x08` and makes the object the head.

The `PRendering` shutdown
`0x00610630` calls `0x0062D740`¹, which clears each table slot and unlinks the objects, the first five inline
and the rest through `0x0062D6D0`. Its walk pointer starts at the head, so the store `[r9]` writes the head or the
`+0x08` of the object before, and it then stores 0 in the object's own `+0x08`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0061068C` |

</details>

The other readers are `0x0062D660`,
which stores the object whose name matches through its first argument or returns `0x13`, `0x0062DBD0`, which counts
the list and copies every object's address into an array, and `0x0062DCB0`, which returns the object whose name
matches, or 0.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CF7110` | `void*` | 0 (zero-filled tail of `.data`) | head of the texture-format registry | `0x0062D0D0` (`0x0062D160`, `0x0062D1D0`, `0x0062D230`, `0x0062D299`); `0x0062D040` (`0x0062D0AA`); through the unlink pointer, `0x0062D740` (`0x0062D7B8`, `0x0062D818`, `0x0062D878`, `0x0062D8D8`, `0x0062D938`) and `0x0062D6D0` (`0x0062D729`) | `0x0062D040` (`0x0062D05C`); `0x0062D0D0` (`0x0062D0FF`); `0x0062D660` (`0x0062D672`); `0x0062D6D0` (`0x0062D6E9`); `0x0062D740` (`0x0062D744`, `0x0062D7BF`, `0x0062D81F`, `0x0062D87F`, `0x0062D8DF`, `0x0062D93F`); `0x0062DBD0` (`0x0062DBDF`, `0x0062DC70`); `0x0062DCB0` (`0x0062DCBB`) |
| `0x02CF72C8` | `void*` | 0 (zero-filled tail of `.data`) | `L8` (`0x02CF72C0`) `+0x08`: the head before it, 0 | `0x0062D0D0` (`0x0062D152`); `0x0062D740` (`0x0062D7BB`, 0, through the object) | the walks of the list, through the object; `0x0062D740` compares its address (`0x0062D77C`) |
| `0x02CF7300` | `void*` | 0 (zero-filled tail of `.data`) | `A8` (`0x02CF72F8`) `+0x08`: `L8` | `0x0062D0D0` (`0x0062D1C2`); `0x0062D740` (`0x0062D81B`, 0, through the object) | the walks of the list, through the object; `0x0062D740` compares its address (`0x0062D7DC`) |
| `0x02CF7338` | `void*` | 0 (zero-filled tail of `.data`) | `LA8` (`0x02CF7330`) `+0x08`: `A8` | `0x0062D0D0` (`0x0062D222`); `0x0062D740` (`0x0062D87B`, 0, through the object) | the walks of the list, through the object; `0x0062D740` compares its address (`0x0062D83C`) |
| `0x02CF7370` | `void*` | 0 (zero-filled tail of `.data`) | `RG8` (`0x02CF7368`) `+0x08`: `LA8` | `0x0062D0D0` (`0x0062D292`); `0x0062D740` (`0x0062D8DB`, 0, through the object) | the walks of the list, through the object; `0x0062D740` compares its address (`0x0062D89C`) |

The walks that read an object's `+0x08` are in `0x0062D040`, `0x0062D0D0`, `0x0062D660`, `0x0062D6D0`, `0x0062D740`,
`0x0062DBD0` and `0x0062DCB0`. The unlink stores through `[r9]` also write one of these links when the object removed
is the one after it, and `0x0062D6D0` stores 0 in the `+0x08` of the object it removes¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0062D72C` |

</details>

</details>

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 15 calls with 6 other topics</summary>

**Application** (explained on [phyre application](phyre-application.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x005CC930`](phyre-modules.md) (on phyre modules) | is called by | [`0x00799980`](phyre-application.md) (on phyre application) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md), [startup constants](../Engine-Core/startup-constants.md), [game application](../Engine-Core/game-application.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00181DD0`](../Graphics/effect-drawing.md) (on effect drawing) | is called by | [`0x0022B8C0`](../Graphics/graphics-thread-handshake.md) (on graphics thread handshake) |
| [`0x00184960`](phyre-d3d11-device-and-resources.md) | calls | [`0x001EDE70`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x001EDEF0`](../Engine-Core/startup-constants.md) (on startup constants)<br>[`0x00229EA0`](../Graphics/effect-drawing.md) (on effect drawing) |
| [`0x00184960`](phyre-d3d11-device-and-resources.md) | is called by | [`0x0022A0B0`](../Saving-Loading-And-Settings/languages.md) (on languages)<br>[`0x0022B7E0`](../Graphics/graphics-thread-handshake.md) (on graphics thread handshake) |
| [`0x005CC930`](phyre-modules.md) (on phyre modules) | is called by | [`0x001E03F0`](../Engine-Core/game-application.md) (on game application) |

**Controls and input** (explained on [phyre application](phyre-application.md), [screen mode and aspect](../Graphics/screen-mode-and-aspect.md), [game application](../Engine-Core/game-application.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x005CC930`](phyre-modules.md) (on phyre modules) | is called by | [`0x00196480`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x0079D920`](phyre-application.md) (on phyre application) |
| [`0x00615BC0`](phyre-d3d11-device-and-resources.md) | is called by | [`0x0079C140`](phyre-application.md) (on phyre application)<br>[`0x007A05D0`](phyre-d3d11-device-and-resources.md) |
| [`0x006278B0`](phyre-d3d11-device-and-resources.md) | is called by | [`0x007A05D0`](phyre-d3d11-device-and-resources.md) |
| [`0x0062AAB0`](phyre-d3d11-device-and-resources.md) | is called by | [`0x0079C140`](phyre-application.md) (on phyre application) |

**Menus and HUD** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00181DD0`](../Graphics/effect-drawing.md) (on effect drawing) | is called by | [`0x0024B9B0`](../Graphics/effect-element-runtime.md) (on effect element runtime) |

</details>
