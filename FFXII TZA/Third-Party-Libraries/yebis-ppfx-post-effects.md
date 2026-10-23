---
title: "YEBIS and PPFX: the post-effect library, how the game starts and drives it, its licence check and the EnableYebis switch"
kind: "system"
category: "Third-party libraries"
addresses: "0x006DA880, 0x006DA8A0, 0x006DA8F0, 0x006DAA50, 0x006DA990, 0x006DAA70, 0x006DE780, 0x006DFF40, 0x0071D9E0, 0x006FF900, 0x0070BA00, 0x00707560, 0x006DF480, 0x006CBD20, 0x006CBEA0, 0x00193DA0, 0x0018E470, 0x00194290, 0x00194A30, 0x001F3300, 0x00167990, 0x02E5BDE0, 0x02EA0B70, 0x02EA0B3C, 0x02EA0B90, 0x00D86C00, 0x00717760, 0x0065E530, 0x006CBAA0, 0x0078A530, 0x0072A320, 0x00E21F90"
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

The library is the code from `0x006DA880` to `0x007911DF`. Its identity is in its own type names and
texts:

- RTTI `Yebis::YebisPfxMemoryAllocatorD3D11` (`0x01F70BC8`, vtable `0x00D86BD8`) and
  `Yebis::PfxShimD3D11` (`0x01F70C38`), beside `PPFX::CPfxMemoryAllocator` (vtable `0x00D8E1E8`) and
  `PPFX::IPfxContext_Dx11`.
- The licence text `FeatureId = YEBIS_D3D11, ...` (`0x00D86C00`) and the messages "YEBIS Expiration
  Problem" (`0x00D8F1A8`) and "The YEBIS library passed over the expiration date : %s" (`0x00D8F690`).
- The string `TjmjdpoTuvejp` (`0x00D8F1C8`), which is `SiliconStudio` with every character raised by
  one; no code or data refers to it.

No version text is in the image. The library's diagnostics carry the date "Feb 18 2016".

### Source paths

The image holds 25 distinct PPFX source paths: 24 relative `..\src\` `.cpp` paths and one absolute
header, `d:\bamboo\build\yeblic-ppfxlic-bl2015\src\gpu\GPUClassUtil.h`. Code loads them at 363
places. They are the file argument of the library's tagged allocation:

- At 230 places the next call is the allocator `0x006DA880(allocator, size, file, line, name)`.
- At 99 places it is `0x006DA980`, an empty function (`ret 0`) that exception-unwind code calls with
  the same arguments.

So a path names the source file of the code that made the allocation, and a function that loads
`..\src\GPU\GPUDepthOfField.cpp` is that file's code.

### The diagnostic log

`0x006DF480` is the library's log. It has 801 direct call sites, every one inside the library; 795 of
them load a literal format string, 386 distinct. Most are a prefix naming the source file followed
by the message, such as "..\src\GPU\GPUPostEffect.cpp(%d) : Feb 18 2016 PPFX ERROR: " (113 sites).
The game's own code never calls it.

### Methods named by their diagnostics

The messages a function prints name its method:

| Function | Method |
|---|---|
| `0x0070B780` | `CPostEffect::BeginPostEffectScene` |
| `0x0070B990` | `CPostEffect::EndPostEffectScene` |
| `0x0070CD40` | `CPostEffect::SetFramebuffer`, which refuses to run between Begin and End |
| `0x00705520` | `CPostEffect::Uninitialize`, which returns `0x80004005` between Begin and End |
| `0x006E04F0` | `IPfxBaseRenderToTexture::Initialize` |
| `0x006E07A0` | `IPfxBaseRenderToTexture::Uninitialize` |

### Render states the D3D11 device refuses

Three render-state methods of `IGPUDevice` do nothing and return `0x80004001` (E_NOTIMPL):
`0x00724EC0` DepthTestEnable, `0x00724F50` DepthFunc and `0x00724FF0` AlphaFunc. Each counts its calls
(`0x02EA1988`, `0x02EA198C`, `0x02EA1990`). It prints its "is not supported" warning only when the count
is 0 or leaves 25 when divided by 100, and only while `0x01F3BA80` and `0x01F3BA8C` are both non-zero.

### Messages no code prints

No instruction or stored pointer in the image refers to these texts:

- "IGPUDevice::ApplyRenderState_AlphaTestEnable() is not supported (DX10/11)." (`0x00D9C8A0`);
- the three log lines of
  `CDepthOfField::ApplyDepthOfField_ApertureFilterLevel_EAPERTUREFM_DISC_ApplyApertureFilter`
  (`0x00DA8660` failed, `0x00DA8710` succeeded, `0x00DAADB0` the call).

### Start-up

1. The static initialiser `0x00167990` builds the game's allocator object `0x02E5BDE0` with the vtable
   of `Yebis::YebisPfxMemoryAllocatorD3D11`.
2. The renderer's start-up `0x006253D0` creates the integration object (`0x0065E5D0`, kept at
   `0x02D38540`) and marks it ready: `0x0065E580` (call at `0x0062549D`) sets its byte `+8` to 1.
3. The first frame that runs the pass calls `0x006CBD20` through `0x0065E5A0`; see the next section.

### The integration object

`0x0065E5D0` allocates the 16-byte object once through `0x00210EC0` and builds it with `0x0065E530`, which
clears its record pointer and ready byte, allocates a `0x78`-byte record and fills it with
`0x006CBAA0`. That constructor clears the context and shim pointers and stores nine fixed values,
among them 1000.0 at `+0x10`, 0.1 at `+0x20`, 10000.0 at `+0x6C` and 45.0 at `+0x70`.

The frame work `0x00193DA0` reaches the record only through one-line wrappers, each of which loads the
record pointer from the object's `+0x00` and jumps to the integration function:

| Wrapper | Target | Call in `0x00193DA0` |
|---|---|---|
| `0x0065E5B0` | none: true when the record's context pointer is set | `0x00193DD1`, `0x00193DF5` |
| `0x0065E5A0` | `0x006CBD20`, create the context | `0x00193DE8` |
| `0x0065E6C0` | `0x006CC2F0` | the branch taken when the command's `+0x99` is set |
| `0x0065E6A0` | `0x006CC1F0`, the first block of scene values | `0x00193E11` |
| `0x0065E6B0` | `0x006CC260`, the second block | `0x00193E36` |
| `0x0065E670` | `0x006CC1E0`, glare, with mode 1 and 1.0 (`0x01CEBBA8`) added | `0x00193E6C` |
| `0x0065E630` | `0x006CC170`, scale and mode; the mode passes through `0x006CBD00`, which returns its second argument | `0x00193EB4` |
| `0x0065E610` | `0x006CC090`, depth of field | `0x00193F40` |
| `0x0065E5C0` | `0x006CBEA0`, the render targets and the effect run | `0x00193F58` |

### Creating the context

`0x006CBD20` runs on the first post-processed frame:

1. Once (flag `0x01F31F70`), it installs `0x02E5BDE0` as the library's allocator (`0x006DA8F0`) and gives
   the library the licence text `0x00D86C00` (`0x006DAA50`, which copies it to `0x02EA0B58`).
2. It creates the context (`0x006DA990`, a `0x18`-byte `PPFX::IPfxContext_Dx11`).
3. It builds a default parameter block (`0x006CBBC0`), fills in the size `0x780` and the flags
   `0x20001`, and calls `0x006DAA70(context, parameters, 3, 5)`. On failure it logs "Failed to
   initialize PPFX context." through the game's log `0x005CDAA0` and carries on.
4. It builds a `Yebis::PfxShimD3D11` object and hands it the context.

`0x006DAA70` is `IPfxBaseContext::Initialize`. It runs the licence verifier once (flag `0x01F3BB28`) and
keeps the result at `0x02EA0B90`; with a negative result it returns that result and creates nothing.
Otherwise it allocates the `0xD40`-byte global block (constructor `0x006FF5D0`), stores it at
`0x02EA0B70` and runs `CPostEffect::Initialize` (`0x006FF900`) on it.

### Each frame

The frame routine `0x001F3300` first calls `0x00194A30`, which applies a delayed `EnableYebis` change.
`0x00194A30` also runs a one-time setup: while the block's byte `+0x19B` is 0, when `0x001DC510()`
returns non-null and `0x001FDF70` returns 1 for that result, it calls `0x00193A00` and `0x00193A80` on the
block and sets `+0x19B`.

`0x001DC510()` returns the `0x18`-byte object `[0x01F82D10]`, made once when `0x001DDAB0` answers non-zero, with the
defaults 1.0, 0.5 and 0.6 at `+0x0C`, `+0x10` and `+0x14`, then filled by `0x001DC3D0`; `0x001FDF70` returns its
first word. The setup copies its values into the block, each reader falling back to the default unless the
first or second word is 1 (the last needs the first word):

| Block field offset | Reader | Value | Clamp |
|---|---|---|---|
| `+0x19C` | `0x00193940` through `0x001DC460` | `+0x08`, else 0 | 0 to 3; a negative value gives 0 |
| `+0x1A0` | `0x00193A00` through `0x001DC4A0` | `+0x0C`, else 1.0 | at least 0 |
| `+0x1A4` | `0x001939A0` through `0x001DC480` | `+0x10`, else 0.5 | 0 to 1.0 |
| `+0x1EC` | `0x00193A80` through `0x001DC4C0` | `+0x14`, else 0.6 | at least 0 |

The frame routine then asks `0x0018E470`, which is true when the integration object is ready and the render
parameter block's byte `+0xA0` is set. Only then does it build the post-process command (`0x0018EEE0`)
whose work is `0x00193DA0`:

1. With no context yet, it creates one (`0x006CBD20`). When the command's byte `+0x99` is set, it
   calls `0x006CC2F0` on the existing context instead.
2. With no context, it stops.
3. It passes two blocks of scene values (`0x006CC1F0`, `0x006CC260`).
4. Glare: with the Glare option on, `0x006CC1E0` hands the command's two glare values to
   `CPostEffect::SetGlareParameters` (`0x00707560`); with it off, 1.0 and 0.0.
5. `0x006CC170` passes a scale and mode.
6. Depth of field: with the DepthofField option on, `0x006CC090` passes the enable byte, a 35 mm lens
   (divided by 1000) and the focus values; off, it passes the effect disabled.
7. `0x006CBEA0` passes the three render targets the command holds and runs
   `CPostEffect::ApplyEffects` (`0x0070BA00`, through `0x006DB660`).

### The licence check

`0x006DFF40` refuses with "License text is not set." when no text was given. Otherwise it decodes the
text (`0x0071C550`) and checks it (`0x0071CD10`, which calls `0x0071D9E0`). A failure is reported as status
1 "License is not valid.", 2 "License is expired." or anything else "Unexpected License Error.".

`0x0071D9E0` checks the dates:

1. The six date fields decoded from the signed part (begin and end year, month and day) must equal
   the plain-text fields one by one (`0x0071DC87` to `0x0071DCDB`); any difference sets status 1
   (`0x0071E209`).
2. When all six are 0 it jumps to success (`0x0071E0F4` to `0x0071E11A`, target `0x0071E216`).
3. Otherwise it builds begin at 00:00:00 and end at 23:59:59, converts both with `_mktime64`
   (`0x0071E169`, `0x0071E1EB`), reads `_time64` (`0x0071E176`) and sets status 2 when now is before begin
   or after end (`0x0071E1FF`).

The shipped text has all six dates 0, so the date window is never evaluated and the check depends
only on the decode and the field match. The expiry messages at `0x00D8F168`, `0x00D8F1A8` and
`0x00D8F690` have no code reference, so nothing prints them.

### EnableYebis

The switch lives in the render parameter block (`[0x01F81300]`, built by `0x0018CD90`, which sets it
on). `0x00194290(block, on, delay)` does nothing when the value is already current. Otherwise:

- Turning it on logs "[YEBIS]Yebis Enable Failed!!!" through `0x005CDAA0`. The line is printed on every
  change from off to on and reports no failure.
- With `delay` 0 it writes `+0xA0` at once. Otherwise it stores the value at `+0xA1` and the delay
  at `+0x1F0`; `0x00194A30` counts `+0x1F0` down once per frame and copies `+0xA1` to `+0xA0` when it
  reaches 0.

Four places call it. The scene and map configuration loaders (`0x001C3D50`, `0x001C7940`) read the
`EnableYebis` key as an integer, 1 meaning on, with no delay. The debug menu handler `0x001D1660`
calls it twice. The script command `0x05B0` (`0x00353420`, through `0x001EC4D0`) passes a value and a
delay from its two arguments.

### The effect-source tokenizer

`0x00717760`, the code of `TFXString.cpp`, tokenizes effect source text: it skips `/*`, `*/` and `//`
comments (`0x00717DEF`) and calls `0x0071A230` to test for spaces, tabs and newlines. It calls itself
and is called only by `0x00719FB0`, whose only caller `0x0071A050` is neither called nor stored anywhere
in the image. The tokenizer is linked and never reached.

### The embedded effect archive

The library's compiled texture effects are a single block of `0xE8E9C2` bytes (15,264,194) in the
image, starting at `0x00E21F90`. It begins with text fields: `.tfxo file`, three decimal numbers, `hlsl`,
then the effect name `TexUtil_D3D11` and a newline-separated technique list that starts with
`tech_AlchemySsao_T1_S16`.

`0x0078A530` copies the whole block into a `malloc` buffer in eight runs of `0x1D1D40` bytes (sources
`0x00E21F90` to `0x01ADEC50`, the last run shorter) and returns it. Its only caller is
`TEXSHADERSET::CreateEffect()` (`0x0072A320`, named by its log lines), which on its first call
(`+0x00` still null) hands the copy, its size and the name `_LUMINANCE_REMAP_S1.pso` to `0x0078A120`,
frees the copy, and then looks up the effect's parameter handles by name (`fParam_FocusDistance`,
`afRGBA_Modulate`, `fParam_GammaCorrection` and others).

### Bodies outside the member lists

Nine large bodies in the span are in neither member list. Each is called only from inside the span
(`0x006E9C20` from `0x007422F0`, `0x007428B0` and `0x0074CA90`; `0x0077FFE0` from `0x00780260`, `0x00780590` and
`0x007809C0`), and all are effect-pass code:

- `0x006E9C20` computes blur tap offsets: it divides the target size by the tap spacing, caps the
  count, and writes one `{x, y, 0, 0}` float vector per tap.
  - Per axis, with size `s` (third or fourth argument), spacing `p` (`s x` the tenth or eleventh argument when
    that is positive, else the fifth or sixth) and cap `m` (eighth): `n = min(ceil(s / 2 / p), m)` while the mode
    byte (ninth) is 0, else `n = min(ceil(s / p), m)`.
  - Before the cap, `n` drops by 1 when `n > 1`, `p >= 8` and `q = (n - 1) x p x 2` (mode 0) or `q = (n - 1) x p`
    satisfies `s - 2(n - 1) <= q < s` (mode 0) or `s - (n - 1) <= q < s`.
  - Tap `i` of an axis is at `(2i - (n - 1)) x k / R`, `R` the target resolution (first or second argument) and
    `k` 1 in mode 0, else 0.5 (`0x006E9A90`). In mode 0 with a positive last argument `e` and one tap on both axes it
    uses two per axis, at `±e / R`.
  - The vectors take both axes in steps of `max(twelfth argument, 1)`, and the count is returned
    (`0x006E9C20`-`0x006EA05B`).
- `0x00740BE0` clamps a sample count to 4 to 8, selects the shader for it, uploads constants through
  slot `+0x98` of the GPU device at `+0x38` and binds textures through slot `+0xB8`.
- `0x0078AD20`, the code of `TinyEffect.cpp`, reflects a shader with `D3DReflect` and allocates its
  `0xC0`-byte variable records through `0x006DA880`.
- `0x0077FFE0` maps a GPU resource (device slot `+0x70`), copies four bytes of it into `+0xA0` to
  `+0xA3` and unmaps it (slot `+0x78`).
- `0x00735E40` stages up to eight float vectors at `0x02EA1C50` and uploads them through device slots
  `+0xD0` and `+0x98`; `0x0074F740` runs it twice (`0x0074FDD9`, `0x007502CD`).
- `0x00741680` runs `0x00740BE0` three times (`0x00741B5C`, `0x00741D2A`, `0x00741F18`).
- `0x007651F0` returns 0 unless its source at `+0x260` is set and three of its intensities are
  positive; otherwise it builds its pass constants from them.

## Layouts

The render parameter block's switch fields (the block is `0x4A8` bytes; the rest is on
[Graphics settings](../Engine-Core/graphics-settings.md)):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0A0` | `u8` | the pass is on (constructor value 1) |  |
| `+0x0A1` | `u8` | the pending value of a delayed change |  |
| `+0x1F0` | `i32` | frames left before the pending value is applied |  |

The library's global block, `0xD40` bytes at `[0x02EA0B70]`, as far as its constructor `0x006FF5D0`
lays it out:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0A8` | `map header` | built by 0x00714800 |  |
| `+0x0B8` | `map header` | built by 0x007147A0 |  |
| `+0x0C8` | `map header` | built by 0x00714740 |  |
| `+0xC80` | `void*` | cleared by the constructor |  |

The licence text at `0x00D86C00`, as shipped:

```python
FeatureId = YEBIS_D3D11, BeginYear = 0, BeginMonth = 0, BeginDay = 0, EndYear = 0, EndMonth = 0,
EndDay = 0, MacAddress = 00-00-00-00-00-00, License = 5F7EAB4F21F6A264...
```

## Shipped data

| Fact | Value |
|---|---|
| span | `0x006DA880` to `0x007911DF` |
| member lists | [`yebis-ppfx-post-effects-members.tsv`](yebis-ppfx-post-effects-members.tsv), 1,598 functions; [`yebis-ppfx-post-effects-unlisted-bodies.tsv`](yebis-ppfx-post-effects-unlisted-bodies.tsv), 732 bodies in the span that the function list does not hold |
| source paths | 25 distinct, 299 copies, 363 loading sites; most sites: `GPUDepthOfField.cpp` 75, `GPUPostEffect.cpp` 48, `GPURenderGlare.cpp` 39, `TFXString.cpp` 30 |
| absolute header path | 12 copies, 6 of them loaded, 20 sites |
| diagnostic log | 801 call sites, 386 distinct literal strings; listed in [`yebis-ppfx-post-effects-diagnostic-strings.tsv`](yebis-ppfx-post-effects-diagnostic-strings.tsv) |
| licence dates | all six 0 |
| calls into the span from outside | the integration functions at `0x006CBD20` to `0x006CC2F0`, static initialisers, exit and unwind code, and seven PhyreEngine calls to `0x0071F970`, a formatted-scan body (`__stdio_common_vsscanf`) the linker placed inside the span |

## Operations

| Address | Entry point | Name from its own diagnostics |
|---|---|---|
| `0x006DA880` | allocate through the installed allocator, count it in `0x02EA0B3C` | |
| `0x006DA8A0` | free, uncount | |
| `0x006DA8F0` | install an allocator; refused while `0x02EA0B3C` is not 0 | `SetMemoryAllocator()` |
| `0x006DAA50` | set the licence text | |
| `0x006DA990` | create the context | `IPfxContext::Instantiate()` |
| `0x006DAA70` | initialise: licence, global block, post-effect | `IPfxBaseContext::Initialize()` |
| `0x006DE780` | shut down: uninitialise, clear the block's maps, clear `0x02EA0B70` | `IPfxBaseContext::~IPfxBaseContext()` |
| `0x006FF900` | build the effect chain on the GPU device | `CPostEffect::Initialize()` |
| `0x00707560` | glare parameters | `CPostEffect::SetGlareParameters()` |
| `0x0070BA00` | run the effects on a frame | `CPostEffect::ApplyEffects()` |
| `0x006DF480` | write a diagnostic line | |

## State

| Address | Holds |
|---|---|
| `0x02D38540` | the game's integration object; byte `+8` is the ready flag |
| `0x02E5BDE0` | the game's allocator object |
| `0x01F3BA68` | the allocator the library uses |
| `0x02EA0B3C` | live allocations made through `0x006DA880` |
| `0x02EA0B58` | the licence text |
| `0x02EA0B90` | the licence result |
| `0x02EA0B70` | the global block; only code inside the library reads it |
| `0x02EA0B78`, `0x02EA0B80` | two render-to-texture objects `0x006DAA70` creates and `0x006DE780` releases |

## Modding notes

- Setting `EnableYebis` to anything but 1 in a scene or map configuration turns every post-effect
  off for that scene; the context stays alive and nothing is re-initialised.
- A non-zero delay through script command `0x05B0` applies the change that many frames later.
- A pending delayed change cannot be cancelled: `0x00194290` compares a request only with the current
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
