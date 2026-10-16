---
title: "YEBIS and PPFX: the post-effect library, how the game starts and drives it, its licence check and the EnableYebis switch"
kind: "system"
category: "Third-party libraries"
addresses: "006DA880, 006DA8A0, 006DA8F0, 006DAA50, 006DA990, 006DAA70, 006DE780, 006DFF40, 0071D9E0, 006FF900, 0070BA00, 00707560, 006DF480, 006CBD20, 006CBEA0, 00193DA0, 0018E470, 00194290, 00194A30, 001F3300, 00167990, 02E5BDE0, 02EA0B70, 02EA0B3C, 02EA0B90, 00D86C00, 00717760, 0065E530, 006CBAA0, 0078A530, 0072A320, 00E21F90"
---

## What the player sees

The remaster's glare around bright light and its depth of field come from a bought-in post-effect
library, Silicon Studio's YEBIS, whose core calls itself PPFX. The game hands it each rendered frame
and it writes the finished image. The Glare and DepthofField options in the
settings switch those two effects; the `EnableYebis` configuration key switches the whole pass off,
and then the frame is shown without post-effects. The library also carries a licence check with an
expiry message, which the shipped game never prints.

## How it works

### The library in the image

The library is the code from `006DA880` to `007911DF`. Its identity is in its own type names and
texts:

- RTTI `Yebis::YebisPfxMemoryAllocatorD3D11` (`01F70BC8`, vtable `00D86BD8`) and
  `Yebis::PfxShimD3D11` (`01F70C38`), beside `PPFX::CPfxMemoryAllocator` (vtable `00D8E1E8`) and
  `PPFX::IPfxContext_Dx11`.
- The licence text `FeatureId = YEBIS_D3D11, ...` (`00D86C00`) and the messages "YEBIS Expiration
  Problem" (`00D8F1A8`) and "The YEBIS library passed over the expiration date : %s" (`00D8F690`).
- The string `TjmjdpoTuvejp` (`00D8F1C8`), which is `SiliconStudio` with every character raised by
  one; no code or data refers to it.

No version text is in the image. The library's diagnostics carry the date "Feb 18 2016".

### Source paths

The image holds 25 distinct PPFX source paths: 24 relative `..\src\` `.cpp` paths and one absolute
header, `d:\bamboo\build\yeblic-ppfxlic-bl2015\src\gpu\GPUClassUtil.h`. Code loads them at 363
places. They are the file argument of the library's tagged allocation:

- At 230 places the next call is the allocator `006DA880(allocator, size, file, line, name)`.
- At 99 places it is `006DA980`, an empty function (`ret 0`) that exception-unwind code calls with
  the same arguments.

So a path names the source file of the code that made the allocation, and a function that loads
`..\src\GPU\GPUDepthOfField.cpp` is that file's code.

### The diagnostic log

`006DF480` is the library's log. It has 801 direct call sites, every one inside the library; 795 of
them load a literal format string, 386 distinct. Most are a prefix naming the source file followed
by the message, such as "..\src\GPU\GPUPostEffect.cpp(%d) : Feb 18 2016 PPFX ERROR: " (113 sites).
The game's own code never calls it.

### Methods named by their diagnostics

The messages a function prints name its method:

| Function | Method |
|---|---|
| `0070B780` | `CPostEffect::BeginPostEffectScene` |
| `0070B990` | `CPostEffect::EndPostEffectScene` |
| `0070CD40` | `CPostEffect::SetFramebuffer`, which refuses to run between Begin and End |
| `00705520` | `CPostEffect::Uninitialize`, which returns `0x80004005` between Begin and End |
| `006E04F0` | `IPfxBaseRenderToTexture::Initialize` |
| `006E07A0` | `IPfxBaseRenderToTexture::Uninitialize` |

### Render states the D3D11 device refuses

Three render-state methods of `IGPUDevice` do nothing and return `0x80004001` (E_NOTIMPL):
`00724EC0` DepthTestEnable, `00724F50` DepthFunc and `00724FF0` AlphaFunc. Each counts its calls
(`02EA1988`, `02EA198C`, `02EA1990`). It prints its "is not supported" warning only when the count
is 0 or leaves 25 when divided by 100, and only while `01F3BA80` and `01F3BA8C` are both non-zero.

### Messages no code prints

No instruction or stored pointer in the image refers to these texts:

- "IGPUDevice::ApplyRenderState_AlphaTestEnable() is not supported (DX10/11)." (`00D9C8A0`);
- the three log lines of
  `CDepthOfField::ApplyDepthOfField_ApertureFilterLevel_EAPERTUREFM_DISC_ApplyApertureFilter`
  (`00DA8660` failed, `00DA8710` succeeded, `00DAADB0` the call).

### Start-up

1. The static initialiser `00167990` builds the game's allocator object `02E5BDE0` with the vtable
   of `Yebis::YebisPfxMemoryAllocatorD3D11`.
2. The renderer's start-up `006253D0` creates the integration object (`0065E5D0`, kept at
   `02D38540`) and marks it ready: `0065E580` (call at `0062549D`) sets its byte `+8` to 1.
3. The first frame that runs the pass calls `006CBD20` through `0065E5A0`; see the next section.

### The integration object

`0065E5D0` allocates the 16-byte object once through `00210EC0` and builds it with `0065E530`, which
clears its record pointer and ready byte, allocates a `0x78`-byte record and fills it with
`006CBAA0`. That constructor clears the context and shim pointers and stores nine fixed values,
among them 1000.0 at `+0x10`, 0.1 at `+0x20`, 10000.0 at `+0x6C` and 45.0 at `+0x70`.

The frame work `00193DA0` reaches the record only through one-line wrappers, each of which loads the
record pointer from the object's `+0x00` and jumps to the integration function:

| Wrapper | Target | Call in `00193DA0` |
|---|---|---|
| `0065E5B0` | none: true when the record's context pointer is set | `00193DD1`, `00193DF5` |
| `0065E5A0` | `006CBD20`, create the context | `00193DE8` |
| `0065E6C0` | `006CC2F0` | the branch taken when the command's `+0x99` is set |
| `0065E6A0` | `006CC1F0`, the first block of scene values | `00193E11` |
| `0065E6B0` | `006CC260`, the second block | `00193E36` |
| `0065E670` | `006CC1E0`, glare, with mode 1 and 1.0 (`01CEBBA8`) added | `00193E6C` |
| `0065E630` | `006CC170`, scale and mode; the mode passes through `006CBD00`, which returns its second argument | `00193EB4` |
| `0065E610` | `006CC090`, depth of field | `00193F40` |
| `0065E5C0` | `006CBEA0`, the render targets and the effect run | `00193F58` |

### Creating the context

`006CBD20` runs on the first post-processed frame:

1. Once (flag `01F31F70`), it installs `02E5BDE0` as the library's allocator (`006DA8F0`) and gives
   the library the licence text `00D86C00` (`006DAA50`, which copies it to `02EA0B58`).
2. It creates the context (`006DA990`, a `0x18`-byte `PPFX::IPfxContext_Dx11`).
3. It builds a default parameter block (`006CBBC0`), fills in the size `0x780` and the flags
   `0x20001`, and calls `006DAA70(context, parameters, 3, 5)`. On failure it logs "Failed to
   initialize PPFX context." through the game's log `005CDAA0` and carries on.
4. It builds a `Yebis::PfxShimD3D11` object and hands it the context.

`006DAA70` is `IPfxBaseContext::Initialize`. It runs the licence verifier once (flag `01F3BB28`) and
keeps the result at `02EA0B90`; with a negative result it returns that result and creates nothing.
Otherwise it allocates the `0xD40`-byte global block (constructor `006FF5D0`), stores it at
`02EA0B70` and runs `CPostEffect::Initialize` (`006FF900`) on it.

### Each frame

The frame routine `001F3300` first calls `00194A30`, which applies a delayed `EnableYebis` change.
`00194A30` also runs a one-time setup: while the block's byte `+0x19B` is 0, when `001DC510()`
returns non-null and `001FDF70` returns 1 for that result, it calls `00193A00` and `00193A80` on the
block and sets `+0x19B`.

The frame routine then asks `0018E470`, which is true when the integration object is ready and the render
parameter block's byte `+0xA0` is set. Only then does it build the post-process command (`0018EEE0`)
whose work is `00193DA0`:

1. With no context yet, it creates one (`006CBD20`). When the command's byte `+0x99` is set, it
   calls `006CC2F0` on the existing context instead.
2. With no context, it stops.
3. It passes two blocks of scene values (`006CC1F0`, `006CC260`).
4. Glare: with the Glare option on, `006CC1E0` hands the command's two glare values to
   `CPostEffect::SetGlareParameters` (`00707560`); with it off, 1.0 and 0.0.
5. `006CC170` passes a scale and mode.
6. Depth of field: with the DepthofField option on, `006CC090` passes the enable byte, a 35 mm lens
   (divided by 1000) and the focus values; off, it passes the effect disabled.
7. `006CBEA0` passes the three render targets the command holds and runs
   `CPostEffect::ApplyEffects` (`0070BA00`, through `006DB660`).

### The licence check

`006DFF40` refuses with "License text is not set." when no text was given. Otherwise it decodes the
text (`0071C550`) and checks it (`0071CD10`, which calls `0071D9E0`). A failure is reported as status
1 "License is not valid.", 2 "License is expired." or anything else "Unexpected License Error.".

`0071D9E0` checks the dates:

1. The six date fields decoded from the signed part (begin and end year, month and day) must equal
   the plain-text fields one by one (`0071DC87` to `0071DCDB`); any difference sets status 1
   (`0071E209`).
2. When all six are 0 it jumps to success (`0071E0F4` to `0071E11A`, target `0071E216`).
3. Otherwise it builds begin at 00:00:00 and end at 23:59:59, converts both with `_mktime64`
   (`0071E169`, `0071E1EB`), reads `_time64` (`0071E176`) and sets status 2 when now is before begin
   or after end (`0071E1FF`).

The shipped text has all six dates 0, so the date window is never evaluated and the check depends
only on the decode and the field match. The expiry messages at `00D8F168`, `00D8F1A8` and
`00D8F690` have no code reference, so nothing prints them.

### EnableYebis

The switch lives in the render parameter block (`[01F81300]`, built by `0018CD90`, which sets it
on). `00194290(block, on, delay)` does nothing when the value is already current. Otherwise:

- Turning it on logs "[YEBIS]Yebis Enable Failed!!!" through `005CDAA0`. The line is printed on every
  change from off to on and reports no failure.
- With `delay` 0 it writes `+0xA0` at once. Otherwise it stores the value at `+0xA1` and the delay
  at `+0x1F0`; `00194A30` counts `+0x1F0` down once per frame and copies `+0xA1` to `+0xA0` when it
  reaches 0.

Four places call it. The scene and map configuration loaders (`001C3D50`, `001C7940`) read the
`EnableYebis` key as an integer, 1 meaning on, with no delay. The debug menu handler `001D1660`
calls it twice. The script command `0x05B0` (`00353420`, through `001EC4D0`) passes a value and a
delay from its two arguments.

### The effect-source tokenizer

`00717760`, the code of `TFXString.cpp`, tokenizes effect source text: it skips `/*`, `*/` and `//`
comments (`00717DEF`) and calls `0071A230` to test for spaces, tabs and newlines. It calls itself
and is called only by `00719FB0`, whose only caller `0071A050` is neither called nor stored anywhere
in the image. The tokenizer is linked and never reached.

### The embedded effect archive

The library's compiled texture effects are a single block of `0xE8E9C2` bytes (15,264,194) in the
image, starting at `00E21F90`. It begins with text fields: `.tfxo file`, three decimal numbers, `hlsl`,
then the effect name `TexUtil_D3D11` and a newline-separated technique list that starts with
`tech_AlchemySsao_T1_S16`.

`0078A530` copies the whole block into a `malloc` buffer in eight runs of `0x1D1D40` bytes (sources
`00E21F90` to `01ADEC50`, the last run shorter) and returns it. Its only caller is
`TEXSHADERSET::CreateEffect()` (`0072A320`, named by its log lines), which on its first call
(`+0x00` still null) hands the copy, its size and the name `_LUMINANCE_REMAP_S1.pso` to `0078A120`,
frees the copy, and then looks up the effect's parameter handles by name (`fParam_FocusDistance`,
`afRGBA_Modulate`, `fParam_GammaCorrection` and others).

### Bodies outside the member lists

Nine large bodies in the span are in neither member list. Each is called only from inside the span
(`006E9C20` from `007422F0`, `007428B0` and `0074CA90`; `0077FFE0` from `00780260`, `00780590` and
`007809C0`), and all are effect-pass code:

- `006E9C20` computes blur tap offsets: it divides the target size by the tap spacing, caps the
  count, and writes one `{x, y, 0, 0}` float vector per tap.
- `00740BE0` clamps a sample count to 4 to 8, selects the shader for it, uploads constants through
  slot `+0x98` of the GPU device at `+0x38` and binds textures through slot `+0xB8`.
- `0078AD20`, the code of `TinyEffect.cpp`, reflects a shader with `D3DReflect` and allocates its
  `0xC0`-byte variable records through `006DA880`.
- `0077FFE0` maps a GPU resource (device slot `+0x70`), copies four bytes of it into `+0xA0` to
  `+0xA3` and unmaps it (slot `+0x78`).
- `00735E40` stages up to eight float vectors at `02EA1C50` and uploads them through device slots
  `+0xD0` and `+0x98`; `0074F740` runs it twice (`0074FDD9`, `007502CD`).
- `00741680` runs `00740BE0` three times (`00741B5C`, `00741D2A`, `00741F18`).
- `007651F0` returns 0 unless its source at `+0x260` is set and three of its intensities are
  positive; otherwise it builds its pass constants from them.

## Layouts

The render parameter block's switch fields (the block is `0x4A8` bytes; the rest is on
[Graphics settings](../Engine-Core/graphics-settings.md)):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0A0` | `u8` | the pass is on (constructor value 1) |  |
| `0A1` | `u8` | the pending value of a delayed change |  |
| `1F0` | `i32` | frames left before the pending value is applied |  |

The library's global block, `0xD40` bytes at `[02EA0B70]`, as far as its constructor `006FF5D0`
lays it out:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0A8` | `map header` | built by 00714800 |  |
| `0B8` | `map header` | built by 007147A0 |  |
| `0C8` | `map header` | built by 00714740 |  |
| `C80` | `void*` | cleared by the constructor |  |

The licence text at `00D86C00`, as shipped:

```
FeatureId = YEBIS_D3D11, BeginYear = 0, BeginMonth = 0, BeginDay = 0, EndYear = 0, EndMonth = 0,
EndDay = 0, MacAddress = 00-00-00-00-00-00, License = 5F7EAB4F21F6A264...
```

## Shipped data

| Fact | Value |
|---|---|
| span | `006DA880` to `007911DF` |
| member lists | `yebis-ppfx-post-effects-members.tsv`, 1,598 functions; `yebis-ppfx-post-effects-unlisted-bodies.tsv`, 732 bodies in the span that the function list does not hold |
| source paths | 25 distinct, 299 copies, 363 loading sites; most sites: `GPUDepthOfField.cpp` 75, `GPUPostEffect.cpp` 48, `GPURenderGlare.cpp` 39, `TFXString.cpp` 30 |
| absolute header path | 12 copies, 6 of them loaded, 20 sites |
| diagnostic log | 801 call sites, 386 distinct literal strings; listed in `yebis-ppfx-post-effects-diagnostic-strings.tsv` |
| licence dates | all six 0 |
| calls into the span from outside | the integration functions at `006CBD20` to `006CC2F0`, static initialisers, exit and unwind code, and seven PhyreEngine calls to `0071F970`, a formatted-scan body (`__stdio_common_vsscanf`) the linker placed inside the span |

## Operations

| Address | Entry point | Name from its own diagnostics |
|---|---|---|
| `006DA880` | allocate through the installed allocator, count it in `02EA0B3C` | |
| `006DA8A0` | free, uncount | |
| `006DA8F0` | install an allocator; refused while `02EA0B3C` is not 0 | `SetMemoryAllocator()` |
| `006DAA50` | set the licence text | |
| `006DA990` | create the context | `IPfxContext::Instantiate()` |
| `006DAA70` | initialise: licence, global block, post-effect | `IPfxBaseContext::Initialize()` |
| `006DE780` | shut down: uninitialise, clear the block's maps, clear `02EA0B70` | `IPfxBaseContext::~IPfxBaseContext()` |
| `006FF900` | build the effect chain on the GPU device | `CPostEffect::Initialize()` |
| `00707560` | glare parameters | `CPostEffect::SetGlareParameters()` |
| `0070BA00` | run the effects on a frame | `CPostEffect::ApplyEffects()` |
| `006DF480` | write a diagnostic line | |

## State

| Address | Holds |
|---|---|
| `02D38540` | the game's integration object; byte `+8` is the ready flag |
| `02E5BDE0` | the game's allocator object |
| `01F3BA68` | the allocator the library uses |
| `02EA0B3C` | live allocations made through `006DA880` |
| `02EA0B58` | the licence text |
| `02EA0B90` | the licence result |
| `02EA0B70` | the global block; only code inside the library reads it |
| `02EA0B78`, `02EA0B80` | two render-to-texture objects `006DAA70` creates and `006DE780` releases |

## Modding notes

- Setting `EnableYebis` to anything but 1 in a scene or map configuration turns every post-effect
  off for that scene; the context stays alive and nothing is re-initialised.
- A non-zero delay through script command `0x05B0` applies the change that many frames later.
- A pending delayed change cannot be cancelled: `00194290` compares a request only with the current
  `+0xA0`. With `+0xA0` = 1 and a delayed 0 pending, a later call asking for 1 (with any delay) is
  ignored, and the 0 still lands when the count reaches 0. An immediate change (delay 0) leaves
  `+0x1F0` running, so an older pending value overwrites it later.
- The "[YEBIS]Yebis Enable Failed!!!" line in the game's log means the pass was switched on.
- The licence text must stay byte for byte as shipped; a changed date field fails the field match.
- The source path a function loads tells which PPFX source file it was compiled from; this is the
  quickest way to find the depth-of-field (`GPUDepthOfField.cpp`) or glare (`GPURenderGlare.cpp`)
  code.

## Related

- [Graphics settings](../Engine-Core/graphics-settings.md): the render parameter block
  and the configuration keys, `EnableYebis` among them.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): the Glare and DepthofField options.
- [Script verb table](../Scripts-And-Script-Commands/verb-table.md): command `0x05B0`.
- [Debug menu](../Engine-Core/debug-menu.md): the menu rows that switch the pass.
- [Post-processing](../Graphics/post-processing.md): the passes the game runs, the
  feature setters and the init bits that leave features off.
