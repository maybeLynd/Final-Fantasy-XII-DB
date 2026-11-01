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

`0x006DF480` formats the message into the `0x800`-byte buffer `0x02EA0BA0` (`__stdio_common_vsprintf`, `0x006DF4CC`) and
passes it to the callback in `0x02EA0B88` when one is set (`0x006DF4EF`), otherwise to `OutputDebugStringA`
(`0x006DF4FA`). The only store to `0x02EA0B88` is `0x006DF3A0`, which no instruction calls and no 8-byte pointer in the
image names, so the messages go to the debugger output.

Each call site tests two words first:

- `0x01F3BA80`, 2 in the image, must be at least 1 before a message of any kind;
- `0x01F3BA90`, 1 in the image, before the 240 ERROR messages, and `0x01F3BA8C`, 1 in the image, before the 41
  WARNING messages, so both kinds print;
- `0x02EA0B40`, 0, before the 86 plain messages that name their source file and line, and `0x02EA0B44`, 0, before
  15 plain messages such as the `IPfxBaseContext::Initialize()` banner, so none of those prints.

While `0x02EA0B44` is 0, each of the device functions `0x00725AA0`, `0x00725C80`, `0x00725E40`, `0x00725FF0`, `0x007261B0`,
`0x00726360`, `0x00726550`, `0x00726700`, `0x007268C0` and `0x00726A70` also skips one more block (for example `0x00725AF5`).

No instruction stores any of the five words: no RIP-relative store, address-forming instruction or 8-byte pointer
names them, and no base-plus-displacement operand reaches them through the image base.

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
  slot `+0x98` of the `PPFX::IGPUEffect` at `+0x38` (vtable `0x00DAF1B8`) and binds textures through its slot `+0xB8`.
- `0x0078AD20`, the code of `TinyEffect.cpp`, reflects a shader with `D3DReflect` and allocates its
  `0xC0`-byte variable records through `0x006DA880`.
- `0x0077FFE0` maps a GPU resource through slot `+0x70` of the object at `[+0x28] + 0x38`, which takes Map's
  arguments (the resource, subresource 0, type 1, and flag `0x100000`, do-not-wait, when `+0x68` is 2;
  `0x00780002`-`0x00780040`), copies four bytes of it into `+0xA0` to `+0xA3` and unmaps it (slot `+0x78`).
- `0x00735E40` stages up to eight float vectors at `0x02EA1C50` and uploads them through slots
  `+0xD0` and `+0x98` of the same effect at `+0x38` (`0x00789E40`, `0x00789D50`).
- `0x00789D50` counts the upload (`0x02EA40B8`, `0x02EA40BC`) and forwards it through slot `+0x58` of the `PPFX::CTinyEffect` at the effect's `+0xE0`
  (`0x0078FCF0`); the GPU device's own slots `+0x98` and `+0xD0` (vtable `0x00D9EA30`: `0x00724EA0`, `0x00725090`) only
  return `0x80004001`. `0x0074F740` runs it twice (`0x0074FDD9`, `0x007502CD`).
- `0x00741680` runs `0x00740BE0` three times (`0x00741B5C`, `0x00741D2A`, `0x00741F18`).
- `0x007651F0` returns 0 unless its source at `+0x260` is set and three of its intensities are
  positive; otherwise it builds its pass constants from them.

## Layouts

The library's global block, `CPostEffect`, is `0xD40` bytes at `[0x02EA0B70]`: the constructor `0x006FF5D0` clears it and `CPostEffect::Initialize` (`0x006FF900`) builds its members and stores the parameter defaults by calling the library's own setters. The member names are the allocation names Initialize passes to `0x006DA880`; the init flags are the word `0x20001` the game passes (`0x006CBE02`).

`CPostEffect` (`0xD40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x002` | `u8` | initByte002 | cleared by Initialize (`0x006FFA00`); read by no instruction |
| `+0x00A` | `u8` | heightReverse | the SetRenderSceneHeightReverse_Gcm flag: only cleared, by Initialize (`0x006FFBD1`) and by the setter `0x007112F0` (`0x00711332`), so it is always 0; read by `0x006FD110` (`0x006FD479`) |
| `+0x010` | `void*` | deviceContext | the device context: SetDeviceContext `0x00706690` stores it (`0x0070673A`); Initialize hands it to the GPU-device creation in its parameter record (`0x00700110`) |
| `+0x018` | `u64` | qword018 | cleared by the constructor (`0x006FF5FA`); read by no instruction |
| `+0x020` | `void*` | gpuDevice | m_pGPUDevice, the IGPUDevice Initialize creates through `0x00727050` (`0x0070012F`; "IGPUDevice::CreateDevice() failed") and resets through its vtable `+0x28` ("m_pGPUDevice->Reset() failed", `0x00700183`); used by every pass for its draws |
| `+0x028` | `void*` | deviceSurface | the first object the device returns through its vtable `+0x58` (`0x007001D3`); `0x006FD070` falls back to it as the effect source (`0x006FD0F7`) |
| `+0x030` | `void*` | deviceSurface2 | the second object the device returns through its vtable `+0x50` (`0x007001E1`); may be null |
| `+0x038` | `void*` | surfaceDesc | a `0x18`-byte description `+0x28` fills (`0x00700206`-`0x0070024B`); its `+0x08` and `+0x0C` are the width and height Initialize sizes the buffers from (`0x0070033C`-`0x0070034E`) |
| `+0x040` | `void*` | surfaceDesc2 | the matching `0x18`-byte description `+0x30` fills, or a copy of `+0x38` with its first dword 0 when `+0x30` is null (`0x00700232`-`0x00700280`) |
| `+0x048` | `void*` | keptDevice | a device Uninitialize keeps for the next Initialize (`0x007055FC`); Initialize prefers it to `+0x20` (`0x006FFA0A`-`0x006FFA14`) and clears it (`0x006FFA5B`) |
| `+0x050` | `void*` | ptr050 | no instruction stores a pointer here: the constructor clears it (`0x006FF616`) and Uninitialize releases and clears it (`0x00705A68`-`0x00705A77`) |
| `+0x058` | `void*` | depthFactorSource | the depth-factor source texture SetDepthFactorSource stores (`0x00711588`, `0x00711615`); the passes test it with `+0x468` before using the depth-factor path (`0x006F91A2`, `0x006F8073`) |
| `+0x060` | `void*` | outputTarget | the output target `0x0070D340` and `0x0070D360` set (`0x0070D340`, `0x0070D3ED`); ApplyEffects requires it (`0x0070BA5C`); EndPostEffectScene_Process swaps in its own target for the alpha pass and restores it (`0x006FBB20`, `0x006FBD89`) |
| `+0x068` | `u32` | outputKind | the kind stored with `+0x60` (`0x0070D346`, `0x0070D3E8`); 1 during the alpha pass (`0x006FBB2B`); with 1 the internal process takes format code `0x15` (`0x006F9219`-`0x006F9222`) |
| `+0x070` | `void*` | auxSource | the texture `0x0070DD30` stores (`0x0070DD30`); passed with `+0x7C`, `+0x80`, `+0x84` and `+0x88` by `0x006F35B0` (`0x006F3660`-`0x006F3674`) and EndPostEffectScene_InternalProcess (`0x006F94AA`-`0x006F94BE`); Initialize clears it (`0x00704C3F`) |
| `+0x078` | `u8` | auxFlag | cleared by Initialize (`0x00704C3B`) and written by nothing else; UpdateParameters_Base tests it (`0x006F78A9`) |
| `+0x07C` | `u32` | auxValue | 0 from Initialize (`0x00704C43`), written by nothing else; passed with `+0x70` (`0x006F3664`, `0x006F94AE`) |
| `+0x088` | `f32` | auxScale | 0 from Initialize (`0x00704C52`), written by nothing else; passed with `+0x70` (`0x006F3674`, `0x006F94BE`) |
| `+0x090` | `void*` | glareModulatorSource | the source texture of SetGlareModulatorSource (`0x0070D41A`-`0x0070D479`) |
| `+0x098` | `u32` | glareModulatorKind | the source kind of SetGlareModulatorSource (`0x0070D40E`, `0x0070D461`); with a kind and no source texture the internal process uses m_pGlareModulatorWork (`+0x128`) instead (`0x006F9174`-`0x006F9185`, `0x006F9260`) |
| `+0x0A0` | `void*` | glareModulatorTexture | the glare-modulator texture of the current frame: EndPostEffectScene_InternalProcess sets it (`0x006F9304`-`0x006F9548`) and UpdateParameters_Base clears it (`0x006F825F`) |
| `+0x0A8` | `void*` | mapA | the header of the map built by `0x00714800` (`0x006FF643`-`0x006FF648`), keyed by texture: `0x0070D270` looks a source texture up in it for its view (`0x0070D276`-`0x0070D2BE`); `0x006FF840` walks it at shutdown (`0x006FF8B7`) |
| `+0x0B0` | `u64` | mapASize | the second word of the `+0xA8` map, cleared by the constructor (`0x006FF63C`) |
| `+0x0B8` | `void*` | mapB | the header of the map built by `0x007147A0` (`0x006FF661`-`0x006FF666`); walked by `0x006FF840` (`0x006FF88B`) |
| `+0x0C0` | `u64` | mapBSize | the second word of the `+0xB8` map, cleared by the constructor (`0x006FF65A`) |
| `+0x0C8` | `void*` | mapC | the header of the map built by `0x00714740` (`0x006FF67F`-`0x006FF684`); walked by `0x006FF840` (`0x006FF85F`) |
| `+0x0D0` | `u64` | mapCSize | the second word of the `+0xC8` map, cleared by the constructor (`0x006FF678`) |
| `+0x0D8` | `void*` | effectSourceView | the effect source as a view, set by `0x0070D270` (`0x0070D325`); `0x006FD070` uses it first (`0x006FD076`-`0x006FD085`) |
| `+0x0E0` | `void*` | effectSourceTexture | the effect source as a texture; `0x006FD070` asks it for a view through its vtable `+0xA0` when `+0xD8` is null (`0x006FD094`-`0x006FD0BF`); cleared by `0x0070D240` and `0x0070D270` |
| `+0x0E8` | `void*` | effectSourceBuffer | the effect source as a render buffer, set by `0x0070D240` (`0x0070D242`); `0x006FD070` takes its current texture when `+0xD8` and `+0xE0` are null (`0x006FD0CA`-`0x006FD0E8`) |
| `+0x0F0` | `void*` | ptr0F0 | cleared by the constructor (`0x006FF687`) and Initialize (`0x00704C34`), written by nothing else; read by UpdateParameters_Base (`0x006F786A`) and the internal process (`0x006FB3E1`) |
| `+0x0F8` | `u8` | initBit31 | 1 when init flag `0x80000000` was given (`+0x145`, `0x00704C24`-`0x00704C2E`); UpdateParameters_Base tests it (`0x006F7861`) |
| `+0x100` | `u64` | qword100 | cleared by Initialize (`0x00704D60`); read by no instruction |
| `+0x108` | `void*` | renderBuffer | m_pRenderBuffer, the `0xA8`-byte render buffer Initialize allocates under that name (`0x00700977`-`0x007009BB`, constructor `0x0075B710`); its texture array (`+0x48`, current index `+0xA0`) holds the slots the `+0x4C8`.. indices name |
| `+0x110` | `void*` | renderGlare | m_pRenderGlare, the `0x310`-byte glare object (`0x007009C2`-`0x00700A06`, constructor `0x007687E0`); its Initialize, GenerateGlare and TonemapToSurface run from `0x00702223` and the internal process (`0x006FB14E`, `0x006FB6F6`) |
| `+0x118` | `void*` | depthOfField | m_pDepthOfField, the `0x4C0`-byte depth-of-field object (`0x00700AB5`-`0x00700AF9`, constructor `0x007790E0`); ApplyEffects_DepthOfField runs it (`0x006F60A1`) |
| `+0x120` | `void*` | effectColorAlphaDestinationWork | m_pEffectColorAlphaDestinationWork, a `0xA8`-byte render buffer made when `+0x146` is set (`0x00700A61`-`0x00700AAE`); for the alpha output EndPostEffectScene_Process takes its current texture as the effect source (`0x006FB9B5`-`0x006FB9D5`) |
| `+0x128` | `void*` | glareModulatorWork | m_pGlareModulatorWork, a `0xA8`-byte render buffer made when `+0x143` is set (`0x00700A0D`-`0x00700A5A`); the glare-modulator step uses it (`0x006F9260`) |
| `+0x130` | `u8` | dofBuilt | 1 when the depth-of-field quality argument of Initialize is not negative (`0x007004C3`-`0x007004CA`); the depth-of-field setters `0x00708710`, `0x007111C0` and `0x00711820` do nothing without it |
| `+0x133` | `u8` | airyDiscBuilt | aperture Airy disc: 1 with init flag `0x40000` (`0x006FFFB9`-`0x006FFFD3`); SetApertureAiryDiscEnable refuses while it is 0 (`0x0070A066`) |
| `+0x136` | `u8` | temporalAntialiasBuilt | temporal anti-alias: 1 with init flag `0x100000` when the device's `+0x8EB` is 0 (`0x00700283`-`0x007002AA`); Initialize then makes the history buffers (`0x007017E6`); SetTemporalAntialiasEnable refuses while it is 0 (`0x0070AB86`) |
| `+0x137` | `u8` | geometryBlurBuilt | geometry blur: 1 with init flag `0x40000` (`0x006FFE82`-`0x006FFE9C`); Initialize tests it at `0x00701131` |
| `+0x138` | `u8` | gaussianBlurBuilt | Gaussian blur: 1 with init flag `0x40000` (`0x006FFFD9`-`0x006FFFF3`); SetGaussianBlurEnable refuses while it is 0 (`0x0070A0F6`) |
| `+0x13D` | `u8` | heatShimmerParticleBuilt | heat-shimmer particles: 1 when `+0x13C` is set (`0x006FFF43`-`0x006FFF59`); SetHeatShimmerParticleEnable refuses while it is 0 (`0x0070A356`) |
| `+0x13E` | `u8` | feedbackBuilt | feedback: 1 with init flag `0x800000`, which also makes the per-view feedback buffers `+0x1B8` (`0x00703456`-`0x007034BB`); SetFeedbackEnable refuses while it is 0 (`0x0070AF96`) |
| `+0x13F` | `u8` | tonemapConvolutionBuilt | tonemap convolution: 1 when `+0xC48` is 1 or more or init flag `0x80000000` is set (`0x0070377E`-`0x00703802`); then m_pTonemapConvolutionTexture (`+0x1D0`) is made; SetTonemapResampleFilter refuses filter 1 while it is 0 (`0x0070B081`) |
| `+0x144` | `u8` | effectMaskBuilt | effect mask: 1 with init flag `0x400` (`0x00700036`-`0x00700050`); SetEffectMaskColorSource and SetEffectMaskAlphaSource refuse while it is 0 (`0x0070D5E7`, `0x0070D7A7`) |
| `+0x145` | `u8` | initBit31Byte | 1 with init flag `0x80000000` (`0x007037E8`-`0x007037FB`), which also forces `+0x13F`; copied to `+0xF8` (`0x00704C24`) |
| `+0x148` | `void*` | motionBlurInternalVelocityTexture | m_pMotionBlurInternalVelocityTexture (`0x00702AD5`-`0x00702B18`), sized from descriptor `+0xF0`/`+0xF4`; tested by GetMaxMotionBlurCameraRecurrences (`0x006FE52B`) |
| `+0x150` | `void*` | aoNormalDepthTexture | m_pAmbientOcclusion_NormalDepthTexture (`0x00702C5F`-`0x00702CA5`), sized from descriptor `+0xFC`/`+0x100`; used by ApplyEffects_GenerateNormalAndLinearDepth (`0x006F3D32`) and the ambient-occlusion pass `0x006F61F0` (`0x006F6268`) |
| `+0x158` | `void*` | aoNormalDepthReducedVertical | m_pAmbientOcclusion_NormalDepthTexture_ReducedVertical (`0x00702DD4`-`0x00702E17`); read by the ambient-occlusion pass `0x006F61F0` (`0x006F6288`) |
| `+0x160` | `void*` | aoNormalDepthReduced | m_pAmbientOcclusion_NormalDepthTexture_Reduced (`0x00702E1E`-`0x00702E61`); read by `0x006F61F0` and DrawDebugBuffers |
| `+0x168` | `void*` | aoResultReduced | m_pAmbientOcclusion_Result_Reduced (`0x00702E68`-`0x00702EAB`); read by `0x006F61F0` and DrawDebugBuffers |
| `+0x170` | `void*` | aoResultReduced2 | m_pAmbientOcclusion_Result_Reduced2 (`0x00702EB2`-`0x00702EF5`); read by `0x006F61F0` (`0x006F62AC`) |
| `+0x178` | `void*` | aoResultReduced3 | m_pAmbientOcclusion_Result_Reduced3: Initialize initialises it when present ("m_pAmbientOcclusion_Result_Reduced3->Initialize() failed", `0x00703148`-`0x007031B9`); read by `0x006F61F0` (`0x006F626F`) |
| `+0x180` | `void*` | aoResultReducedVertical | m_pAmbientOcclusion_Result_ReducedVertical (`0x00702EFC`-`0x00702F3F`); read by `0x006F61F0` (`0x006F62BB`) |
| `+0x188` | `void*` | aoResult | m_pAmbientOcclusion_Result: Initialize sets it to null (`0x00703238`) and initialises its device only when present (`0x00704089`-`0x007040DF`) |
| `+0x190` | `void*` | temporalAntialiasHistory | m_ppTemporalAntialias_History, one history buffer per effect view, made when `+0x136` is set (`0x007017F3`-`0x00701831`, `0x00701980`-`0x00701A67`); read by the temporal anti-alias pass `0x006F65A0` (`0x006F663C`) |
| `+0x198` | `void*` | taaWeightA | temporal anti-alias: a per-view float array made with the history buffers (`0x00701847`-`0x0070187E`); `0x0070E7A0` resets each view's entry to 1.0 (`0x0070E7F5`-`0x0070E7FC`); read by the temporal anti-alias pass (`0x006F68A0`) |
| `+0x1A0` | `void*` | taaWeightB | temporal anti-alias: a second per-view float array (`0x00701885`-`0x007018BC`), reset to 1.0 by `0x0070E7A0` (`0x0070E803`-`0x0070E80A`); read by `0x006F65A0` |
| `+0x1A8` | `void*` | taaLuminanceScale | temporal anti-alias: a per-view float array (`0x007018C3`-`0x007018FA`) that `0x0070E7A0` resets to the scene luminance scale `+0x6D8` (`0x0070E811`-`0x0070E81F`); read by `0x006F65A0` |
| `+0x1B0` | `void*` | taaPerView16 | temporal anti-alias: a per-view array of 16-byte entries (`0x00701901`-`0x0070195E`) that `0x0070E7A0` clears (`0x0070E822`-`0x0070E82D`); read by `0x006F65A0` |
| `+0x1B8` | `void*` | feedbackBuffers | m_ppFeedbackBuffer, one `0xA8`-byte render buffer per effect view, made when `+0x13E` is set (`0x0070347D`-`0x007035E7`); read by `0x006F6D80` and `0x0070B150` |
| `+0x1C0` | `void*` | feedbackTonemapTexture | m_pFeedbackTonemapTexture, allocated from the texture pool (`0x0075E2D0`) when `+0x1C8` and the device's `+0x8E0` are 0 (`0x00703706`-`0x00703733`); read by `0x006F6D80` (`0x006F6DF0`) |
| `+0x1D0` | `void*` | tonemapConvolutionTexture | m_pTonemapConvolutionTexture, allocated from the texture pool when `+0x13F` is set and `+0x13E` is not (`0x00703809`-`0x00703855`); read by `0x0070B150` (`0x0070B22A`) |
| `+0x1D8` | `u32` | textureCount1D8 | Initialize counts textures into it and then stores 0 (`0x0070389B`-`0x00703916`), so it is always 0; Uninitialize reads it as the count for `+0x1E0` (`0x0070612A`) |
| `+0x1E0` | `void*` | textureArray1E0 | cleared by the constructor (`0x006FF728`) and only released by Uninitialize (`0x0070606F`-`0x00706158`); nothing stores a pointer here |
| `+0x1E8` | `void*` | viewFrameCounts | a per-view dword array (`0x00700DAF`-`0x00700DE9`); EndPostEffectScene_PreProcess increments the active view's entry each frame (`0x006F87A6`-`0x006F87AD`) |
| `+0x1F0` | `i32` | activeView | the active effect view, set by SetActiveView (`0x007067B5`, 0 to m_nEffectViews); -1 in a per-view call means this view |
| `+0x1F8` | `void*` | autoExposureParams | m_pAutoExposureParam, one `0x68`-byte record per effect view (`0x00700B5A`-`0x00700BBF`); its `+0x60` holds m_pQuerySceneLuminance (`0x00700CAC`) and its `+0x58` the exposure the game reads (`0x006DC4B0`) |
| `+0x200` | `void*` | autoFocusParams | m_pAutoFocusParam, one `0x48`-byte record per effect view (`0x00700BC6`-`0x00700C04`); its `+0x40` holds m_pQuerySceneDepth (`0x00700D63`) and its `+0x38` the focused distance the game reads (`0x006DC650`) |
| `+0x208` | `u32` | initFlags | the init flag word as given to Initialize (`0x006FFB86`), before the adjustments made to the copy at `+0x20C` |
| `+0x330` | `u32[2]` | descCopy08 | descriptor copy `+0x08` and `+0x0C` (see PpfxInitDescriptor): the copy at `+0x328` that Initialize takes of `+0x210` (`0x006FFB0B`-`0x006FFB7C`) and adjusts |
| `+0x338` | `u32[2]` | descCopy10 | descriptor copy `+0x10` and `+0x14`, the render width and height overrides |
| `+0x340` | `u32[2]` | descCopy18 | descriptor copy `+0x18` and `+0x1C`, the render-scene width and height overrides |
| `+0x358` | `u8` | descCopy30 | descriptor copy `+0x30`; read at `0x0070256E` for the depth-of-field buffer scale |
| `+0x35C` | `i32` | descCopy34 | descriptor copy `+0x34`, the tonemap convolution level; read at `0x007037A2` and `0x007037B5` |
| `+0x360` | `u32[2]` | descCopy38 | descriptor copy `+0x38` |
| `+0x380` | `u32[2]` | descCopy58 | descriptor copy `+0x58` and `+0x5C`, the two format codes |
| `+0x394` | `u32` | descCopy6C | descriptor copy `+0x6C`, copied into the glare initialisation record (`0x00702120`) |
| `+0x440` | `u8` | depthTexture | the depth texture is used: 1 when init flag `0x10000` (PFXINIT_DEPTHTEXTURE, named by the message at `0x007000C1`) is given and the device's `+0x8E4` is set, 0 when `0x0071BB00` accepts descriptor `+0x38` and `+0x3C` (`0x00700465`-`0x0070049A`); SetDepthFactorSource and UpdateParameters_Base test it (`0x00711526`, `0x006F8079`) |
| `+0x448` | `void*` | reductionTextures | an array of `+0x450` textures made when slots `+0x4C8` and `+0x4D0` differ (`0x00701BD3`-`0x00701C3B`); read by `0x006F2AF0` (`0x006F2BB0`) |
| `+0x450` | `i32` | reductionCount | ceil(log(size ratio of slots `+0x4D0` to `+0x4C8`) / log 0.5) - 1, at least 0 (`0x00701AD4`-`0x00701BD1`); the length of `+0x448` |
| `+0x458` | `void*` | array458 | an array Initialize makes (`0x00701DA3`-`0x00701DFD`); read by the internal process (`0x006F9E50`-`0x006FA151`) |
| `+0x460` | `i32` | count460 | -1 with init flag `0x400000`, else 0 (`0x0070054D`-`0x00700561`); the bound of Initialize's loops over `+0x458` (`0x00701E4A`, `0x00701ED4`) and of the internal process's (`0x006F9DA3`-`0x006F9F80`) |
| `+0x464` | `u8` | initBit17 | bit `0x20000` of the init flags (`0x007004D0`-`0x007004DB`); SetDepthFactorSource tests it (`0x0071164A`) |
| `+0x465` | `u8` | needsDepth | 1 when ambient occlusion, motion blur, depth of field, heat shimmer, init bit `0x10000000` or the antialias falloff (`+0x141`) is on together with `+0x440` or `+0x464` (`0x007004F4`-`0x00700547`); Initialize then checks the depth format (`0x00700693`, `0x0070107B`) |
| `+0x468` | `void*` | depthFactorTexture | the depth-factor texture of SetDepthFactorSource (`0x0071158C`, `0x0071160E`); the passes take the depth-factor path while it or `+0x58` is set |
| `+0x470` | `i32` | depthFactorKind | the kind SetDepthFactorSource stores (`0x007115B1`); the passes compare it with 8 (`0x006F3864`, `0x006F7883`) |
| `+0x474` | `u32` | depthFactorParam | stored by SetDepthFactorSource (`0x0071159F`); read by `0x00708D10` (`0x00708D4C`) |
| `+0x478` | `f32` | depthFactorA | the first float SetDepthFactorSource stores (`0x00711593`-`0x007115B7`, as the first of 16 bytes); the passes take the 16 bytes from here (`0x006DBE4C`, `0x006F31CC`, `0x006F3D77`) |
| `+0x47C` | `f32` | depthFactorB | the second float SetDepthFactorSource stores (`0x00711599`-`0x007115B7`) |
| `+0x480` | `f32` | depthFactorC | `+0x478` divided by itself, 1.0, written by SetDepthFactorSource (`0x007115BE`-`0x007115E5`) |
| `+0x484` | `f32` | depthFactorD | -(`+0x47C` / `+0x478`), written by SetDepthFactorSource (`0x007115C6`-`0x007115DD`) |
| `+0x488` | `u8` | separateSceneBuffer | 1 when the effects need their own copy of the scene: the descriptor's `+0x110`, `+0x48B`, `+0x147`, `+0x48C`, a format or size different from the render buffer, or `0x0071B9C0` (`0x0070060B`-`0x00700670`, `0x00700FC6`-`0x00701074`); tested by the internal process (`0x006F9088`) |
| `+0x489` | `u8` | initBit2 | bit `0x4` of the init flags (`0x007002D1`-`0x007002DD`) |
| `+0x48A` | `u8` | initBit1 | bit `0x2` of the init flags (`0x007002E3`-`0x007002EE`); with `+0x489` and flag `0x100` it sets `+0x48C`; `0x006FC370` uses it to pick the HDR mode (`0x006FC3A8`) |
| `+0x48B` | `u8` | initBit3 | bit `0x8` of the init flags (`0x007002F4`-`0x00700300`); `0x006FC370` and `0x006FE7F0` test it |
| `+0x48C` | `u8` | hdrScene | set when `+0x489` or `+0x48A` is set and init flag `0x100` is given (`0x00700306`-`0x0070032B`); tested by most passes (`0x006F30E2`, `0x006F60C2`) |
| `+0x48D` | `u8` | srgbFormat | set with init flag `0x4000` when `+0x48E` is set (`0x007005A1`-`0x007005B6`), which also picks format code `0x1D` instead of `0x1C` (`0x007005BD`); Initialize tests it for descriptor `+0x5C`'s format (`0x00700FA4`-`0x00700FB4`) |
| `+0x48E` | `u8` | hdrInput | 1 when any of `+0x489`, `+0x48A`, `+0x48B` is set (`0x00700567`-`0x00700588`); `0x0070B390` then stores the inverse scale (`0x0070B3B0`); tested by the internal process |
| `+0x491` | `u8` | initBit3Copy | 1 when `+0x48B` is set (`0x00700618`-`0x0070062F`); tested at `0x00701169` |
| `+0x492` | `u8` | sceneBufferOnly | 1 when the scene needs its own buffer (`+0x488`) but no effect that draws in between is on (none of `+0x130`, `+0x131`, `+0x133`, `+0x134`, `+0x137`, `+0x138`, `+0x13A`, `+0x13C`, `+0x13E`, `+0x140`, `+0x142`), `+0x491` and `+0x147` are clear and the scene size fits the render size (`0x007010E0`-`0x007011A0`); then `+0x4D0` stays 0 (`0x007011CF`) |
| `+0x493` | `u8` | depthOfFieldDeviceFlag | the device's byte `+0x8E0` when depth of field is built (`0x0070123E`-`0x0070125D`), cleared when the depth-of-field table value is 5 to 7 and `0x0077F3C0` answers non-zero (`0x00701263`-`0x0070127A`); EndPostEffectScene_PreProcess tests it (`0x006F89CA`, `0x006F8AB9`) |
| `+0x494` | `u8` | byte494 | cleared and set by `0x006FD110` (`0x006FD1CB`, `0x006FD388`); tested by the internal process (`0x006F9B18`) |
| `+0x498` | `f32` | sceneScaleX | set by `0x0070D190` (`0x0070D1BF`, 0 becomes 1.0); the internal process multiplies by it (`0x006FB1A4`); 1.0 during the alpha pass (`0x006FB9E6`) |
| `+0x49C` | `f32` | sceneScaleY | set by `0x0070D190` (`0x0070D1C7`, 0 becomes 1.0); the internal process multiplies by it (`0x006FB1B1`) |
| `+0x4A8` | `void*` | effectMaskColorSource | the source of SetEffectMaskColorSource (`0x0070D5DA`-`0x0070D639`); read by EndPostEffectScene_Process (`0x006FBEF4`) |
| `+0x4B0` | `void*` | effectMaskAlphaSource | the source of SetEffectMaskAlphaSource (`0x0070D79A`-`0x0070D7F9`); read by EndPostEffectScene_Process (`0x006FBEFB`) |
| `+0x4C0` | `i32` | alphaOutputType | the alpha output type of SetAlphaOutputParameters (`0x0070DBFA`); with 2 EndPostEffectScene_Process runs a second internal pass with neutral colour values for the alpha (`0x006FB92F`, `0x006FBA8E`) |
| `+0x4C4` | `f32` | alphaOutputScale | the scale of SetAlphaOutputParameters (`0x0070DBF0`); applied at `0x006FBF55` |
| `+0x4C8` | `i32` | slotScene | a render-buffer slot index (-1 = the buffer's current one): 0 from Initialize (`0x007011AD`); BeginPostEffectScene copies it to `+0x4D8` (`0x0070B805`) |
| `+0x4CC` | `i32` | slotSceneOffset | 1 when the descriptor's `+0x40` count is not 0 (`0x007011B4`-`0x007011C0`); BeginPostEffectScene adds it to its slot argument (`0x0070B846`) |
| `+0x4D0` | `i32` | slotWork | a render-buffer slot: the `+0x40` count plus 1, or 1, when `+0x488` is set, else 0 (`0x007011C6`-`0x007011F0`) |
| `+0x4D4` | `i32` | slotRingStart | the first slot of the ring the passes rotate through (`0x00701211`, `0x00701315`); EndPostEffectScene_PreProcess and `0x006FE080` wrap within `+0x4D4` .. `+0x4D4` + `+0x36C` - 1 (`0x006F8951`-`0x006F8963`) |
| `+0x4D8` | `i32` | slotCurrent | the slot BeginPostEffectScene makes current in m_pRenderBuffer (`0x0070B80B`-`0x0070B869`) |
| `+0x4DC` | `i32` | slotChainStart | the image the effect chain starts from: the scene slot `+0x4C8` when `+0xD00` lets the chain read the scene buffer itself, else the work slot `+0x4D0` (`0x006F88FB`-`0x006F892E`); the ambient-occlusion pass `0x006F61F0` takes it as its source (`0x006F971B`-`0x006F9756`) |
| `+0x4E0` | `i32` | slotAmbientOcclusionResult | the ambient-occlusion result: the next ring slot while ambient occlusion is on (`+0xD30`), else `+0x4DC` (`0x006F8934`-`0x006F8967`); `0x006F61F0` draws into it (`0x006F62CF`) |
| `+0x4E4` | `i32` | slotTemporalAntialiasSource | the temporal anti-alias source, the same slot as `+0x4E0` (`0x006F896D`); the temporal anti-alias pass `0x006F65A0` reads it (`0x006F6647`) |
| `+0x4E8` | `i32` | slotTemporalAntialiasResult | the temporal anti-alias result: the next ring slot while temporal anti-alias is on (`+0xD31`), else `+0x4E4` (`0x006F8973`-`0x006F89A6`); `0x006F65A0` draws into it (`0x006F6680`) |
| `+0x4EC` | `i32` | slotDepthOfFieldSource | the depth-of-field source: the image after temporal anti-alias when `+0x55C` puts depth of field before motion blur (`0x006F89AC`-`0x006F89B5`), else the image after heat shimmer (`0x006F8A97`-`0x006F8AA4`); the first texture m_pDepthOfField->ApplyDepthOfField (`0x0077ECE0`) gets (`0x006F615B`-`0x006F618B`); also read by the auto-focus pass `0x006F4C40` (`0x006F4EEE`) |
| `+0x4F0` | `i32` | slotDepthOfFieldWork | the depth-of-field work buffer: a ring slot of its own while depth of field is on (`+0xCE3`) and the device flag `+0x493` is clear, else `+0x4EC` (`0x006F89BB`-`0x006F8A04`, `0x006F8AAA`-`0x006F8AF3`); the second texture ApplyDepthOfField gets (`0x006F6135`) |
| `+0x4F4` | `i32` | slotDepthOfFieldResult | the depth-of-field result: one more ring slot when, with `+0xCE3` set and `+0x493` clear, m_pDepthOfField's `+0x139` is also set (`0x0077F3A0`), else `+0x4F0` (`0x006F8A0A`-`0x006F8A3D`, `0x006F8AF9`-`0x006F8B2C`); the third texture ApplyDepthOfField gets (`0x006F6105`-`0x006F6131`) and the render buffer's current texture for the auto-focus pass (`0x006F6046`-`0x006F605C`); with `+0xD29` and `+0xD2A` set the internal process hands it to `0x006F2CB0` (`0x006F97A5`-`0x006F9822`) |
| `+0x4F8` | `i32` | slotOpticalVignetteSource | the optical-vignette source: the image after heat shimmer and the late depth of field (`0x006F8B32`); the vignette step `0x007436B0` reads it while `+0x494` is set (`0x006F9B18`-`0x006F9C4D`) |
| `+0x4FC` | `i32` | slotOpticalVignetteResult | the optical-vignette result: a ring slot of its own while `+0x494` is set, else `+0x4F8` (`0x006F8B38`-`0x006F8B6B`); `0x007436B0`'s destination (`0x006F9B91`-`0x006F9C4D`) |
| `+0x500` | `i32` | slotMotionBlurSource | the motion-blur source: the slot `0x006FE080` is given (`0x006FE08D`); the motion-blur pass `0x006F5740` reads it (`0x006F594B`) |
| `+0x504` | `i32` | slotMotionBlurWork | the motion-blur work buffer, written only while `+0xD09` is set: the source slot, or a ring slot of its own when the frame's recurrence count `+0xD10` is 2 or more (`0x006FE0A3`, `0x006FE0D0`-`0x006FE0DA`); `0x006F5740` passes it to the blur draws with the result slot (`0x006F59C0`-`0x006F59F5`, `0x006F5A88`) |
| `+0x508` | `i32` | slotMotionBlurResult | the motion-blur result: while `+0xD09` is set the next ring slot after the work buffer, or after the velocity buffer, else the source slot (`0x006FE093`, `0x006FE12D`, `0x006FE14C`); `0x006FE080` returns it as the chain's next image (`0x006FE153`) and `0x006F5740` draws into it (`0x006F5992`) |
| `+0x50C` | `i32` | slotMotionBlurVelocity | the motion-blur velocity buffer, written only while `+0xD09` is set: a ring slot of its own when the motion-blur type `+0xD0C` is 2 and neither a velocity source (`+0xA88`) nor m_pMotionBlurInternalVelocityTexture (`+0x148`) exists, else the source slot (`0x006FE0A9`, `0x006FE100`-`0x006FE11E`); UpdateParameters_Base then takes its texture as the velocity map `+0xAA0` (`0x006F821D`-`0x006F8258`) |
| `+0x510` | `i32` | slotHeatShimmerSource | the heat-shimmer source: the image after the early motion blur (`+0xD14`) (`0x006F8A43`-`0x006F8A58`); pTexUtil->HeatShimmerParticles (`0x00749FB0`, named by the message at `0x006F9AC6`) reads it (`0x006F9883`, `0x006F9A8E`) |
| `+0x514` | `i32` | slotHeatShimmerResult | the heat-shimmer result: a ring slot of its own while heat-shimmer particles are on (`+0xD24`, from SetHeatShimmerParticleEnable's `+0xAB0` in `0x006FDD10`), else `+0x510` (`0x006F8A5E`-`0x006F8A91`); HeatShimmerParticles' destination (`0x006F98B0`-`0x006F9A8E`) |
| `+0x518` | `i32` | slotAiryDiscSource | the aperture Airy-disc source: the image after the optical vignette and the late motion blur (`0x006F8B71`-`0x006F8B86`); the Airy-disc step reads it while `+0xD01` is set (`0x006F9CAC`-`0x006F9D21`) |
| `+0x51C` | `i32` | slotAiryDiscWork | the Airy-disc work buffer: the first of two ring slots, written only while `+0xD01` is set (`0x006F8B8C`-`0x006F8BC3`); read by the Airy-disc step (`0x006F9D25`) |
| `+0x520` | `i32` | slotAiryDiscResult | the Airy-disc result: the second ring slot while `+0xD01` is set, else `+0x518` (`0x006F8BC9`-`0x006F8BE2`); read by the Airy-disc step (`0x006F9D4F`) |
| `+0x524` | `i32` | slotGaussianBlurSource | the Gaussian-blur source, the same slot as `+0x520` (`0x006F8BE8`); the Gaussian-blur step, which passes the Gaussian parameters `+0xA20` to `0x00758860` (`0x006FA1ED`-`0x006FA226`), reads it while `+0xD08` is set (`0x006FA00C`-`0x006FA081`) |
| `+0x528` | `i32` | slotGaussianBlurWork | the Gaussian-blur work buffer: the first of two ring slots, written only while `+0xD08` is set (`0x006F8BEE`-`0x006F8C25`); read by the Gaussian-blur step (`0x006FA085`) |
| `+0x52C` | `i32` | slotGaussianBlurResult | the Gaussian-blur result: the second ring slot while `+0xD08` is set, else `+0x524` (`0x006F8C2B`-`0x006F8C44`); read by the Gaussian-blur step (`0x006FA0AF`) |
| `+0x530` | `i32` | slotLensDistortionSource | the lens-distortion source, the same slot as `+0x544` (`0x006F8D07`); the lens-distortion step `0x00743410` reads it while `+0xD27` is set (`0x006FA68F`-`0x006FA6E4`, `0x006FA8B6`) |
| `+0x534` | `i32` | slotLensDistortionResult | the lens-distortion result: a ring slot of its own while `+0xD27` is set, else `+0x530` (`0x006F8D0D`-`0x006F8D47`); `0x00743410`'s destination (`0x006FA711`) |
| `+0x538` | `i32` | slotChromaticAberrationSource | the chromatic-aberration source, the same slot as `+0x54C` (`0x006F8C89`); the chromatic-aberration step `0x00743930`, which takes the parameters `+0x9D8`..+`0xA14`, reads it while `+0x9D5` is set (`0x006FA416`-`0x006FA569`) |
| `+0x53C` | `i32` | slotChromaticAberrationResult | the chromatic-aberration result: a ring slot of its own while `+0x9D5` is set, else `+0x538` (`0x006F8C8F`-`0x006F8CC2`); `0x00743930`'s destination (`0x006FA48F`) |
| `+0x540` | `i32` | slotChromaticAberrationCopySource | the source of the chromatic-aberration copy, the same slot as `+0x53C` (`0x006F8CC8`); `0x007422F0` copies it to `+0x544` while `+0x9DD` is set (`0x006FA56E`-`0x006FA66F`); `+0x9DD` needs `+0x9DC`, which is always 0 (`0x0070476B`; `0x00709FB0`'s only caller `0x006DCCD0` passes 0 at `0x006DCCED`), so the copy never runs |
| `+0x544` | `i32` | slotChromaticAberrationCopyResult | the destination of the chromatic-aberration copy: a ring slot of its own while `+0x9DD` is set, else `+0x540` (`0x006F8CCE`-`0x006F8D01`), so always `+0x540`; read at `0x006FA5E7` |
| `+0x548` | `i32` | slotAntialiasSource | the antialias source, the same slot as `+0x52C` (`0x006F8C4A`); the antialias step `0x0074DC40`, which takes the falloff distances `+0xC58`/`+0xC5C`, reads it while `+0xC55` is set (`0x006FA2C1`-`0x006FA30D`, `0x006FA405`) |
| `+0x54C` | `i32` | slotAntialiasResult | the antialias result: a ring slot of its own while `+0xC55` is set, else `+0x548` (`0x006F8C50`-`0x006F8C83`); `0x0074DC40`'s destination (`0x006FA33A`) |
| `+0x550` | `i32` | slotEffectsResult | the finished effect image, the same slot as `+0x534` (`0x006F8D4D`): the render buffer's current texture while m_pRenderGlare->GenerateGlare (`0x00769C50`) and the tonemap run (`0x006FA9B3`, `0x006FAB76`, `0x006FB116`, `0x006FB1C3`); the scene slot `+0x4C8` replaces it when `+0xD00` is clear, `+0x48F` is set and the HDR encoding word's high half is 7 (`0x006FAA3A`-`0x006FAA50`) |
| `+0x554` | `i32` | slotLuminanceSource | the same slot as `+0x550` (`0x006F8D53`); when the HDR encoding word's high half is 7 the internal process hands its texture to the auto-exposure pass `0x006F4390`, the feedback pass `0x006F6D80` and `0x006F7330` (`0x006FB1FC`-`0x006FB2A0`) |
| `+0x55A` | `u8` | depthOfFieldApplied | 1 once ApplyEffects_DepthOfField has run in the frame (`0x006F61D3`); cleared by EndPostEffectScene_Process (`0x006FB88D`, `0x006FBCD0`) |
| `+0x55B` | `u8` | frameMode55B | set by EndPostEffectScene_Process from bit `0x10` of its flags or the byte `0x02EA147C`, and also when `+0x6D4` is 0 or less (`0x006FB8A2`-`0x006FB8CE`); 1 for the alpha pass (`0x006FBCEA`); tested by the passes (`0x006F43B2`, `0x006F4C61`, `0x006F8779`) |
| `+0x55C` | `u8` | depthOfFieldBeforeMotionBlur | 1 when `+0xD29` is set (`0x006F8912`-`0x006F8928`): EndPostEffectScene_PreProcess then gives depth of field its slots right after temporal anti-alias (`0x006F89AC`) instead of after heat shimmer (`0x006F8A97`), and the internal process draws it there (`0x006F9778`, `0x006F9AD4`) |
| `+0x568` | `i32[2]` | hdrFormatCodes | the HDR encoding codes `0x006FC370` derives from the mode `+0x730`: `+0x568` is 2, 5, 8, 11 or 14 and `+0x56C` is 3, 6, 9, 12 or 15 for modes 3 to 7 in the high half (`0x006FC46E`-`0x006FC557`), both 3 and 1 for an HDR scene `+0x48C` (`0x006FC5CC`-`0x006FC5E2`), 0 without a mode (`0x006FC5EB`-`0x006FC5F2`); 0 from Initialize (`0x007011FD`); `+0x568` is read by ApplyApertureFilter (`0x0070BE4C`, `0x0070C1A2`) |
| `+0x570` | `i32` | hdrTechnique | `0x10` to `0x13` by the HDR encoding, else 0 (`0x006FC45E`-`0x006FC522`); read by EndPostEffectScene_PreProcess (`0x006F8EB6`) |
| `+0x574` | `i32` | hdrFormatCodeCopy | a copy of `+0x568` (`0x006FC565`, `0x006FC5F9`); 0 from Initialize (`0x00701204`); read by the internal process (`0x006FAAA5`) |
| `+0x57C` | `i32` | hdrCode57C | 2, 5, 8, 11 or 14 from `+0x564` (`0x006FC648`-`0x006FC689`); read by ApplyEffects_DepthOfField (`0x006F6074`) |
| `+0x584` | `i32` | hdrValue584 | the result of `0x007140C0` (`0x006FC449`-`0x006FC450`); read by `0x006FE7F0` (`0x006FE80F`) |
| `+0x590` | `i32` | multisampleMode | the mode of SetMultisampleMode (`0x00708159`) |
| `+0x594` | `i32` | multisampleValue | set by SetMultisampleMode (`0x00708163`-`0x00708257`); read by BeginPostEffectScene (`0x0070B86F`) and the internal process |
| `+0x598` | `i32` | sceneArgSlot | BeginPostEffectScene's second argument (`0x0070B7CB`) |
| `+0x59C` | `f32` | sceneArgValue | BeginPostEffectScene's fourth argument, a float (`0x0070B7E0`) |
| `+0x5A8` | `f32` | cameraFar | the far distance of the render-scene perspective: `0x00706C20` stores its second float, 1000.0 when not positive (`0x00706C60`-`0x00706C90`); the game passes the camera's far value (`0x006CC260`) |
| `+0x5AC` | `f32` | cameraFieldOfView | twice the arctangent of `+0x5B0`, the field-of-view angle (`0x00706CA0`-`0x00706CB9`) |
| `+0x5B0` | `f32` | cameraTanHalfAngle | tan of half `0x00706C20`'s third float, or tan(0.392699) when that tangent is not positive (`0x00706C26`-`0x00706C98`) |
| `+0x5C0` | `f32` | prevCameraFar | the previous frame's far distance: `0x00706D90` stores it (`0x00706E00`), the game passing last frame's values (`0x006CC2A3`) |
| `+0x5C4` | `f32` | prevCameraFieldOfView | the previous frame's field-of-view angle (`0x00706E29`) |
| `+0x5C8` | `f32` | prevCameraTanHalfAngle | the previous frame's tan of half the angle (`0x00706E08`) |
| `+0x5D4` | `f32` | viewMatrix00 | cell [0][0] of the camera matrix at `+0x5D4`..+`0x613` that `0x00706F60` copies (`0x00706F89`) and converts with `0x006E3E00` unless its flag is set; identity without a matrix (`0x00707048`) |
| `+0x5E8` | `f32` | viewMatrix11 | cell [1][1] of the camera matrix (`0x0070703E`) |
| `+0x5FC` | `f32` | viewMatrix22 | cell [2][2] of the camera matrix (`0x00707034`) |
| `+0x610` | `f32` | viewMatrix33 | cell [3][3] of the camera matrix (`0x0070702A`) |
| `+0x614` | `f32` | viewInverse00 | cell [0][0] of the inverse `0x006F0800` computes of the camera matrix, at `+0x614`..+`0x653` (`0x00706FC8`; identity at `0x0070709A`) |
| `+0x628` | `f32` | viewInverse11 | cell [1][1] of the inverse camera matrix (`0x00707090`) |
| `+0x650` | `f32` | viewInverse33 | cell [3][3] of the inverse camera matrix (`0x0070707C`) |
| `+0x654` | `f32` | prevViewMatrix00 | cell [0][0] of the previous frame's camera matrix at `+0x654`..+`0x693` (`0x00707249`; identity at `0x00707304`); without its flag `0x00707220` converts `+0x5D4`, not this copy (`0x00707253`) |
| `+0x668` | `f32` | prevViewMatrix11 | cell [1][1] of the previous camera matrix (`0x007072FA`) |
| `+0x67C` | `f32` | prevViewMatrix22 | cell [2][2] of the previous camera matrix (`0x007072F0`) |
| `+0x690` | `f32` | prevViewMatrix33 | cell [3][3] of the previous camera matrix (`0x007072E6`) |
| `+0x694` | `f32` | prevViewInverse00 | cell [0][0] of the inverse of the previous camera matrix at `+0x694`..+`0x6D3` (`0x00707284`; identity at `0x00707356`) |
| `+0x6A8` | `f32` | prevViewInverse11 | cell [1][1] of the previous inverse (`0x0070734C`) |
| `+0x6D0` | `f32` | prevViewInverse33 | cell [3][3] of the previous inverse (`0x00707338`) |
| `+0x6D4` | `f32` | timeStep6D4 | the fifth argument of SetRenderSceneLuminanceScale (`0x00706B98`), 1/60 by default (`0x00704D6E`, `0x00705017`); a value of 0 or less sets `+0x55B` each frame (`0x006FB8C3`-`0x006FB8CE`); read by the auto-exposure pass `0x006F4390`, `0x006F4C40` and `0x006F6D80` |
| `+0x6D8` | `f32` | sceneLuminanceScale | SceneLuminanceScale, the sixth argument of SetRenderSceneLuminanceScale, which must be above 0 (`0x00706BA0`-`0x00706BE6`); 1.0 during the alpha pass (`0x006FBC02`) |
| `+0x6DC` | `f32` | luminanceFactor6DC | 1.0 from Initialize (`0x00704EE8`), forced to 1.0 for the alpha pass and restored (`0x006FBBF8`, `0x006FBDB2`); written by nothing else |
| `+0x6EC` | `u8[4]` | unusedSpan6EC | written and read by no function; nothing fixes its width |
| `+0x6F8` | `i32` | lightShaftIndex | the light shaft the light-shaft setters act on: Initialize sets it to each shaft while it sets them up and then to 0 (`0x00704884`, `0x0070492F`); read by SetLightShaftEnable (`0x00707880`), `0x00707950` and `0x00707A40` |
| `+0x700` | `f32` | focusDistance | depth of field: the focus distance; `0x00708540` stores the game's value (`0x00708542`, from `0x006CC090`), which is the auto-focus distance while the command's auto-focus byte is set |
| `+0x704` | `f32` | focalLength | depth of field: the lens focal length in metres, stored when not negative (`0x00708560`); the game passes 35 / 1000 (`0x006CC144`); 0.024 by default (`0x00704C59`) |
| `+0x708` | `i32` | lensMode | depth of field: 0 from `0x00708540`, 1 from `0x007084E0`, the argument of `0x00708470` (`0x00708577`, `0x00708517`, `0x007084C9`) |
| `+0x70C` | `f32` | apertureFNumber | depth of field: the aperture f-number (`0x00708568`); the game passes its f-number |
| `+0x710` | `f32` | lensParam710 | 1.0 from `0x00708540`, 0 from `0x007084E0`, a stack argument of `0x00708470` (`0x0070857D`, `0x00708521`, `0x007084AA`) |
| `+0x714` | `f32` | lensAngle714 | π/4 from `0x00708540` and `0x007084E0`, a stack argument of `0x00708470` (`0x00708587`, `0x00708527`, `0x007084B2`) |
| `+0x718` | `f32` | dofScale718 | 1.0 from Initialize (`0x00704C84`), written by nothing else; read by ApplyEffects_DepthOfField |
| `+0x728` | `f32` | exposure | the first float of `0x0070B390`, clamped to at least FLT_MIN (`0x0070B390`-`0x0070B3A8`); the game passes the active view's auto-exposure value (`0x006DC4B0` through `0x006CC170`); 1.0 during the alpha pass |
| `+0x72C` | `f32` | exposureScale | the second float of `0x0070B390` (`0x0070B420`); the game passes 2.0 when the device byte is set, else 1.0 (`0x00193E7F`, `0x00193EA6`) |
| `+0x734` | `f32` | hdrRange | the HDR range of `0x0070B390` (stack argument, the game passes 32.0), or 1.0 when `+0x48E` is set and `+0x738` takes 1 / range (`0x0070B3B0`-`0x0070B3F0`); `0x006FC370` keeps `+0x734` / `+0x738` clamped to 0.1..16 or 32 at `+0xC68` |
| `+0x740` | `f32` | block73C_04 | the second float of the 16 bytes Initialize copies from `0x008C5FD0` to `+0x73C` (`0x00704FC7`); read by no instruction |
| `+0x744` | `f32` | block73C_08 | the third float of that copy; read by no instruction |
| `+0x748` | `f32` | block73C_0C | the fourth float of that copy; read by the internal process and EndPostEffectScene_Process |
| `+0x74C` | `f32` | param74C | `0x0070AE10`'s float clamped to 0..1 (`0x0070AE18`-`0x0070AE30`); Initialize passes its default at `0x00704FBB`; read by the internal process and `0x006F4390` |
| `+0x758` | `f32` | focusNear | `+0x750` clamped between the near distance `+0x5A4` and 0.99 × far (`0x006FC7BC`-`0x006FC806`, `0x006FC760`) |
| `+0x75C` | `f32` | focusFar | `+0x754` clamped to the far distance and above `+0x758` (`0x006FC7C4`-`0x006FC846`) |
| `+0x764` | `i32` | vignetteMode | vignette: 0 off, 1 from `0x0070B4B0`, 2 from CPostEffect::SetVignetteByOptics `0x0070B500`, 3 from CPostEffect::SetVignetteByOpticsImageCircle `0x0070B610`, 4 from `0x0070B700` (`0x0070B4EC`, `0x0070B5F9`, `0x0070B6E2`, `0x0070B764`); each setter first stores 0; Initialize leaves it 0 through `0x0070B4B0`(0, 0.05) (`0x0070502C`); read by `0x006FD110` and `0x006FC760` |
| `+0x768` | `f32` | vignetteA | vignette: `0x0070B4B0`'s first float (`0x0070B4DA`) |
| `+0x76C` | `f32` | vignetteB | vignette: `0x0070B4B0`'s second float (`0x0070B4E4`), `0x0070B700`'s stack float (`0x0070B75C`) or SetVignetteByOpticsImageCircle's stack float (`0x0070B66A`) |
| `+0x770` | `f32` | vignetteC | vignette: the first float of SetVignetteByOptics (`0x0070B54D`), SetVignetteByOpticsImageCircle (`0x0070B64C`) and `0x0070B700` (`0x0070B744`) |
| `+0x774` | `f32` | vignetteOpticsA | vignette by optics: SetVignetteByOptics's second float (`0x0070B571`); read by `0x006FC760` and `0x006FD110` |
| `+0x778` | `f32` | vignetteOpticsB | vignette by optics: its third float (`0x0070B579`); read by `0x006FC760` and `0x006FD110` |
| `+0x77C` | `f32` | vignetteOpticsC | vignette by optics: its first stack float (`0x0070B581`); read by `0x006FC760` and `0x006FD110` |
| `+0x780` | `f32` | vignetteOpticsD | vignette by optics: its second stack float (`0x0070B589`); read by `0x006FC760` and `0x006FD110` |
| `+0x788` | `f32` | vignetteCircleA | vignette by optics image circle: SetVignetteByOpticsImageCircle's second float (`0x0070B654`); read by `0x006FC760` and `0x006FD110` |
| `+0x78C` | `f32` | vignetteCircleB | vignette by optics image circle: its third float (`0x0070B65F`); read by `0x006FC760` |
| `+0x790` | `f32` | vignetteCircleC | vignette by optics image circle: its second stack float (`0x0070B672`); read by `0x006FC760` |
| `+0x794` | `f32` | vignetteD | vignette: `0x0070B700`'s second float (`0x0070B74C`) |
| `+0x798` | `f32` | vignetteE | vignette: `0x0070B700`'s third float (`0x0070B754`) |
| `+0x7A0` | `f32` | hdrLimit | `0x0070B390`'s last stack float, FLT_MAX becoming `0x7EFFFFFF` (`0x0070B40D`-`0x0070B42A`); the game passes -FLT_MAX (`0x006CC198`) |
| `+0x96C` | `i32` | colourSpaceA | 0 from Initialize (`0x0070500C`); when it differs from `+0x970`, `0x0070B2A0` composes the matrices `0x006E2C30` and `0x006E3000` build from the two onto the matrix at `+0x92C` (`0x0070B2DE`-`0x0070B32B`) |
| `+0x970` | `i32` | colourSpaceB | 0 from Initialize (the qword at `0x0070500C`); the second value `0x0070B2A0` compares |
| `+0x974` | `u8` | dofEnable | the depth-of-field enable: `0x00708710` stores the game's enable byte when `+0x130` is set, else 0 (`0x00708710`-`0x0070872D`); read by the depth-of-field update `0x006FC760` |
| `+0x975` | `u8` | feedbackEnable | the feedback enable of SetFeedbackEnable (`0x0070AFE7`), 0 when `+0x13E` is clear (`0x0070AFD5`); read by the internal process and `0x0070B150` |
| `+0x978` | `f32` | feedbackParam978 | 0 from Initialize (`0x00704BBB`), written by nothing else; read by `0x006F6D80` (`0x006F71DE`) |
| `+0x9CC` | `f32` | lensParam9CC | π from Initialize (`0x00704582`); read by `0x006F4C40`, the internal process and `0x006FD760` |
| `+0x9F0` | `f32[2]` | pair9F0 | the third float pair of `0x00709FB0` (`0x00709FE6`, from its sixth argument); (0, 0) from Initialize (`0x0070479A`) |
| `+0xA4C` | `i32` | sampleCountA4C | `0x0070A510`'s count argument clamped to 3..8, a negative value kept (`0x0070A526`-`0x0070A57F`); read by UpdateParameters_Base |
| `+0xA78` | `f32` | motionBlurParamA78 | -0.01 from Initialize (`0x00704AE5`), written by nothing else; read by the motion-blur pass `0x006F5740` |
| `+0xAA8` | `u64` | motionBlurStateAA8 | set by UpdateParameters_Base (`0x006F81E3`, `0x006F8200`); read by `0x006F36D0` and the motion-blur pass `0x006F5740` |
| `+0xACC` | `f32` | paramACC | 1.0, the first of four 1.0 floats Initialize stores at `+0xACC` (`0x007049A9`); read by `0x006FC760` |
| `+0xAF8` | `f32` | paramAF8 | 0.28 from Initialize (`0x007049ED`), written by nothing else; read by the internal process |
| `+0xB0C` | `f32` | paramB0C | 1.0 from Initialize (`0x00704A3E`); read by no instruction |
| `+0xB4C` | `f32` | matrixB38_11 | cell [1][1] of the matrix `0x0070A7F0` copies to `+0xB38` (identity at `0x0070A8D4`) |
| `+0xB60` | `f32` | matrixB38_22 | cell [2][2] of the `+0xB38` matrix (`0x0070A8CA`) |
| `+0xB78` | `f32` | matrixB78_00 | cell [0][0] of the inverse `0x0070A7F0` stores at `+0xB78` (`0x0070A868`; identity at `0x0070A930`) |
| `+0xB8C` | `f32` | matrixB78_11 | cell [1][1] of the `+0xB78` inverse (`0x0070A926`) |
| `+0xBA0` | `f32` | matrixB78_22 | cell [2][2] of the `+0xB78` inverse (`0x0070A91C`) |
| `+0xBB4` | `f32` | matrixB78_33 | cell [3][3] of the `+0xB78` inverse (`0x0070A912`) |
| `+0xBB8` | `i32` | aoMaskSource | ambient occlusion: the mask source channel of SetAmbientOcclusionMaskSource, 0 to 5 (`0x0070D945`), 0 when refused; read by the ambient-occlusion pass `0x006F61F0` |
| `+0xBBC` | `u8[4]` | unusedSpanBBC | written and read by no function; nothing fixes its width |
| `+0xBC8` | `f32` | aoMaskWeightR | ambient occlusion: the first float of the 16-byte vector SetAmbientOcclusionMaskSource copies to `+0xBC8` (`0x0070D93B`); 1.0 by default (`0x00704B91`) |
| `+0xBCC` | `f32` | aoMaskWeightG | the second float of the `+0xBC8` vector |
| `+0xBD0` | `f32` | aoMaskWeightB | the third float of the `+0xBC8` vector |
| `+0xBD4` | `f32` | aoMaskWeightA | the fourth float of the `+0xBC8` vector |
| `+0xBD8` | `f32` | aoMaskBiasR | the first float of the second vector SetAmbientOcclusionMaskSource copies to `+0xBD8` (`0x0070D94B`); 0 by default (`0x00704B9C`) |
| `+0xBDC` | `f32` | aoMaskBiasG | the second float of the `+0xBD8` vector |
| `+0xBE0` | `f32` | aoMaskBiasB | the third float of the `+0xBD8` vector |
| `+0xBE4` | `f32` | aoMaskBiasA | the fourth float of the `+0xBD8` vector |
| `+0xBEC` | `i32` | aoSampleCount | ambient occlusion: 16 from Initialize (`0x007046A0`); read by the ambient-occlusion pass `0x006F61F0` |
| `+0xBF0` | `f32` | aoParamBF0 | ambient occlusion: 1.0 from Initialize (`0x007046A6`); read by `0x006F61F0` and UpdateParameters_Base |
| `+0xBF4` | `f32` | aoParamBF4 | ambient occlusion: 1.0 from Initialize (`0x007046B0`); read by `0x006F61F0` and UpdateParameters_Base |
| `+0xC00` | `f32` | aoParamC00 | ambient occlusion: 0.0001 from Initialize (`0x007046C5`); read by `0x006F61F0` |
| `+0xC04` | `f32` | aoParamC04 | ambient occlusion: the first of four 0.5 floats from Initialize (`0x007046D3`); read by `0x006F61F0` |
| `+0xC08` | `f32` | aoParamC08 | the second 0.5 of that vector |
| `+0xC0C` | `f32` | aoParamC0C | the third 0.5 of that vector |
| `+0xC10` | `f32` | aoParamC10 | the fourth 0.5 of that vector |
| `+0xC14` | `f32` | aoParamC14 | ambient occlusion: 1.0 from Initialize (`0x007046DA`); read by `0x006F61F0` |
| `+0xC18` | `f32` | aoParamC18 | ambient occlusion: 1.0 from Initialize (`0x007046E4`); read by `0x006F61F0` |
| `+0xC28` | `i32` | taaParamC28 | temporal anti-alias: 2 from Initialize (`0x00704668`); read by the temporal anti-alias pass `0x006F65A0` and UpdateParameters_Base |
| `+0xC30` | `f32` | taaBlend | temporal anti-alias: `0x0070ABF0`'s first float clamped to 0..1 (`0x0070ABF6`-`0x0070AC49`); 0.05 by default (`0x0070464B`) |
| `+0xC34` | `f32` | taaParamC34 | temporal anti-alias: `0x0070ABF0`'s second float (`0x0070AC04`) |
| `+0xC38` | `f32` | taaParamC38 | temporal anti-alias: a stack float of `0x0070ABF0` clamped to 0..1 (`0x0070AC1F`-`0x0070AC9B`) |
| `+0xC3C` | `f32` | taaParamC3C | temporal anti-alias: `0x0070ABF0`'s third float (`0x0070AC27`) |
| `+0xC40` | `f32` | taaParamC40 | temporal anti-alias: a stack float of `0x0070ABF0` clamped to 0..1 (`0x0070AC0F`-`0x0070AC6B`) |
| `+0xC44` | `f32` | taaParamC44 | temporal anti-alias: `0x0070ACB0`'s float clamped to 0..1 (`0x0070ACB8`-`0x0070ACD0`); read by `0x006F65A0` |
| `+0xC48` | `i32` | tonemapConvolutionLevel | the tonemap convolution level (`0x0070377E`-`0x007037CA`, from descriptor `+0x34`); read by the internal process and `0x0070B150` |
| `+0xC4C` | `i32` | tonemapResampleFilter | the filter of SetTonemapResampleFilter (`0x0070B0CF`); read by the internal process and `0x0070B150` |
| `+0xC50` | `f32` | tonemapResampleScale | \|SetTonemapResampleFilter's float\|, at most 1.0 (`0x0070B0C1`-`0x0070B0FF`) |
| `+0xC60` | `f32` | autoFocusSet | 1.0 once `0x0070F200` accepts auto-focus values (`0x0070F252`); read by the auto-focus pass `0x006F4C40` |
| `+0xC64` | `f32` | autoExposureSet | 1.0 once `0x0070EC90` accepts auto-exposure values (`0x0070ED70`); read by the auto-exposure pass `0x006F4390` |
| `+0xC68` | `f32` | hdrRangeRatio | `+0x734` / `+0x738` clamped to 0.1..16 when `+0x48E` is set, else 0.1..32 (`0x006FC6D1`-`0x006FC74A`); read by `0x006F4390` (`0x006F488E`) |
| `+0xC6C` | `i32` | glareMode | the glare mode of SetGlareParameters (`0x007075C4`); the game passes 1 (`0x006CC1E0`); read by the internal process |
| `+0xC74` | `i32` | glareActive | 1 from Initialize (`0x00704F0C`), and set by nothing else in the code the game reaches; two library setters no instruction or table references write it too: `0x006DB9C0` jumps to `0x00707600` with the object `0x02EA0B70`, which stores its edx argument, and `0x00707610` (behind `0x006DB9E0`) stores -1 (`0x0070761B`); `0x006FE7A0` reports glare on (1.0) while it is non-zero and the glare luminance `+0x6E4` is above 0, and with -1 only while the word `+0xC78` is not below 0 (`0x006FE7A0`-`0x006FE7DD`); read by the internal process and `0x006FE7F0` |
| `+0xCC0` | `i32` | paramCC0 | 1 from Initialize (`0x00704F6B`), written by nothing else; read by `0x006FECC0` |
| `+0xCD0` | `f32` | paramCD0 | 0 from Initialize (`0x007051A1`), written by nothing else; read by the internal process (`0x006FABE9`) |
| `+0xCD4` | `f32` | paramCD4 | 1.0 from Initialize (`0x007051A8`); the internal process divides by it (`0x006FAC47`, `0x006FACD2`) |
| `+0xCD8` | `f32` | paramCD8 | 1.0 from Initialize (`0x0070517D`); read by the internal process (`0x006FAE1E`) |
| `+0xCDC` | `f32` | paramCDC | 1.0 from Initialize (`0x00705187`); read by the internal process (`0x006FAE38`) |
| `+0xCF0` | `f32` | depthOfFieldDepthScaleInverse | 1 / `+0xCE8` (`0x006FD02E`-`0x006FD037`), set by the depth-of-field update `0x006FC760`; with `+0xCF4` it undoes the `+0xCE8`/`+0xCEC` depth map, the last step of `0x00708D10`'s depth conversion (`0x00708E92`-`0x00708ECB`); `0x006FE620` starts the motion-blur depth window from it (`0x006FE671`) |
| `+0xCF4` | `f32` | depthOfFieldDepthOffsetInverse | -(`+0xCEC` / `+0xCE8`) (`0x006FD033`-`0x006FD04C`), the offset that goes with `+0xCF0`; added in `0x00708D10`'s last step (`0x00708EAB`) and in `0x006FE620` (`0x006FE681`) |
| `+0xCF8` | `f32` | depthReferenceDistance | the reference distance of the first step of `0x00708D10`'s depth conversion, which also uses the near and far distances (`0x00708DEF`-`0x00708E36`): the focus distance `+0x700` while depth of field is on (`0x006FCEAA`-`0x006FCEB0`); otherwise the near end of the depth window that motion blur (`+0xA64`/`+0xA68`), heat shimmer (`+0xB10`/`+0xB14`) and the antialias falloff (`+0xC58`/`+0xC5C`) need, the whole near-to-far range when `0x006FD760` asks or motion blur is type 2, raised to at least `+0x758`, and the far distance when nothing needs a window (`0x006FC9DA`-`0x006FCB26`, `0x006FCEDD`), or that window's far end capped at near x 64000 when both scene textures have depth formats and `+0x760` is clear (`0x006FCF3C`-`0x006FCFF5`); also read by `0x006F2CB0`, `0x006FD760`, `0x006FE620`, `0x00708CD0` and `0x0070E1B0` |
| `+0xCFC` | `u8` | effectsBeforeTonemap | 1 when any effect draws before the tonemap this frame: depth of field (`+0xCE3`), ambient occlusion (`+0xD30`), antialias (`+0xC55`), temporal anti-alias (`+0xD31`), chromatic aberration (`+0x9D5`, `+0x9DD`), lens distortion (`+0xD27`), Airy disc (`+0xD01`), Gaussian blur (`+0xD08`), motion blur (`+0xD09`) or heat shimmer (`+0xD24`) (`0x006F832C`-`0x006F8394`); while it is set the chain cannot start in the scene buffer (`0x006F8862`) |
| `+0xCFD` | `u8` | depthResolveNeeded | 1 when the frame needs the depth buffer: `+0xCE5` or `+0xCE0`, or ambient occlusion (`+0xD30`) or the velocity temporal anti-alias (`+0xD32`) working from the depth texture (`+0x440`) rather than a depth-factor source (`+0x468`, `+0x58`) (`0x006F839A`-`0x006F83F1`); EndPostEffectScene_PreProcess then resolves the depth-stencil texture (`0x00722800`, `0x00722900`) and sets `+0x558` (`0x006F8DD3`-`0x006F8DDC`, `0x006F8E3A`-`0x006F8E66`, `0x006F8F6F`-`0x006F8FAD`) and `0x02EA1900` is cleared while it is clear (`0x006F8D40`-`0x006F8D64`) |
| `+0xCFE` | `u8` | hdrEncodingsMatch | 1 when the two 16-bit halves of the HDR encoding word `+0x730` are equal (`0x006FC3EE`-`0x006FC422`); EndPostEffectScene_PreProcess lets HDR input (`+0x48E`) start the chain in the scene buffer only while it is set (`0x006F886B`-`0x006F887B`) |
| `+0xCFF` | `u8` | hdrEncodingAlternate | 1 when `+0x48F` is set and the low half of the HDR encoding word `+0x730` is not 8 (`0x006FC408`-`0x006FC43A`); `0x007140C0` then picks the encoding code `+0x584` (`0x006FC441`-`0x006FC450`), and `0x006FE7F0` moves its encoding code one step (2 to 3, 4 to 5, 6 to 7, 8 to 9; `0x006FE893`-`0x006FE8D1`) |
| `+0xD00` | `u8` | chainFromSceneBuffer | 1 when the effect chain reads the scene buffer itself: no output target (`+0x60`), no effect before the tonemap (`+0xCFC`) and, for HDR input (`+0x48E`), matching encodings (`+0xCFE`) (`0x006F885C`-`0x006F8885`); cleared when the scene texture is larger than the work texture (`0x006F888F`-`0x006F88F4`); `+0x4DC` is then `+0x4C8`, else `+0x4D0` (`0x006F88FB`-`0x006F890C`); while it is clear the internal process first copies the scene into the work slot (`0x006F90CC`-`0x006F94F3`) |
| `+0xD01` | `u8` | airyDiscActive | 1 when the aperture Airy disc is drawn: SetApertureAiryDiscEnable's flag `+0xA16`, `+0x71E` clear, the lens flag `+0xCE4`, `+0xA1D` or depth of field (`+0xCE3`), and the work texture's size times `+0xD04` above 0.725952 (`0x006FD580`-`0x006FD638`; UpdateParameters_Base calls it first, `0x006F7689`); gates the Airy-disc step (`0x006F9CAC`) and its two slots (`0x006F8B8C`) |
| `+0xD04` | `f32` | airyDiscScale | the aperture Airy-disc size per unit of image size: half of what m_pDepthOfField's `0x0076BA40` returns for `+0xA18` (`0x006FCE1F`-`0x006FCE4C`); `0x006FD580` tests the work texture's size times it against 0.725952 (`0x006FD5F9`-`0x006FD638`), the Airy-disc step multiplies by it (`0x006F9D8A`) and `0x006FD110` subtracts it from the vignette value (`0x006FD3B2`) |
| `+0xD08` | `u8` | gaussianBlurActive | 1 when Gaussian blur is drawn: SetGaussianBlurEnable's flag `+0xA1E`, `+0x71E` clear, and one of `+0xA20`, `+0xA24`, `+0xA28` not 0 (`0x006F772D`-`0x006F777E`); gates the Gaussian-blur step (`0x006FA00C`) and its two slots (`0x006F8BEE`) |
| `+0xD09` | `u8` | motionBlurActive | 1 when camera motion blur draws this frame: cleared each frame (`0x006F78EA`), set when the type's routine returns at least one recurrence and the blur passes the length test against `+0xA58` (`0x006F7F11`-`0x006F7F4B`); gates the late motion-blur draw (`0x006F9C52`), `0x006FE080`'s slots (`0x006FE080`), `+0xD14` (`0x006F7FA7`) and `+0xCFC` (`0x006F837D`) |
| `+0xD0C` | `i32` | motionBlurType | the camera motion-blur type for the frame: the type `+0xA3C` while motion blur is enabled (`+0xA39`) and `+0x71E` is clear, else -1 (`0x006FC8EC`-`0x006FC924`); UpdateParameters_Base picks the recurrence routine by it (0: `0x007449B0`, 1: `0x00744B90`, 2: `0x007472C0`; `0x006F7BB9`-`0x006F7EBE`), sets -1 (`0x006F78F1`) and stores it back when the blur draws (`0x006F7F52`); the motion-blur pass picks its draw by it (`0x006F5A46`-`0x006F5B98`); with 2 `0x006FE080` gives the velocity map a slot (`0x006FE100`) |
| `+0xD10` | `i32` | motionBlurRecurrences | the recurrence count the type's routine returned for the frame (`0x006F7C70`, `0x006F7DA8`, `0x006F7EC3`; stored `0x006F7F59`), 0 otherwise (`0x006F78FB`); with 2 or more `0x006FE080` gives the motion blur a work slot of its own (`0x006FE0D0`) |
| `+0xD14` | `u8` | motionBlurEarly | 1 when motion blur runs early in the chain, before heat shimmer: velocity motion blur (`+0xD09` with type 2, `0x006F7FA7`-`0x006F7FB9`), or type 1 or 2 with a usable depth window `+0xA64`/`+0xA68` (`0x007282F0`, `0x006F7FC2`-`0x006F8001`); EndPostEffectScene_PreProcess then gives it its slots before `+0x510` (`0x006F8A43`-`0x006F8A51`) and the internal process draws it there (`0x006F9829`-`0x006F9835`); else after the optical vignette (`0x006F8B71`-`0x006F8B7F`, `0x006F9C5B`-`0x006F9C67`) |
| `+0xD15` | `u8` | velocityMotionBlur | 1 with `+0xD14` when the frame's motion blur is type 2 (`0x006F7FB0`-`0x006F7FB9`); with it UpdateParameters_Base asks for the velocity map (`+0xD2C`, `0x006F8130`-`0x006F816B`) |
| `+0xD18` | `f32` | motionBlurDepthScale | the motion-blur depth window as a scale on depth: `0x006FE620` computes it from `+0xA64`/`+0xA68`, the near and far distances and `+0xCF0`..+`0xCF8` (`0x006FE658`-`0x006FE78A`) when `0x006FE590` accepts motion-blur type 1 or 2 with that window (`0x006F7B8D`-`0x006F7BB4`); cleared each frame (`0x006F7B79`); the motion-blur pass and `0x006F36D0` hand it with `+0xD1C` to their draws (`0x006F5A3F`, `0x006F3A04`) |
| `+0xD1C` | `f32` | motionBlurDepthOffset | the offset that goes with `+0xD18`: written by `0x006FE620` (`0x006FE68D`, `0x006FE78A`), cleared with it (`0x006F7B79`) |
| `+0xD20` | `f32` | velocityMapScale | the velocity-map scale: 0 each frame (`0x006F78E0`); for motion-blur type 2 the length `0x007472C0` returns divided by the work texture's size `+0x60` (`0x006F7EDE`-`0x006F7EF2`, stored `0x006F7F45`); raised to at least the temporal anti-alias value `+0xC38` when temporal anti-alias reprojects (`+0xC28` 1 or 2) (`0x006F8008`-`0x006F8044`); `0x006F36D0` and the motion-blur pass give it to the velocity-map draw `0x007485F0` (`0x006F3AF6`, `0x006F5DC2`) |
| `+0xD34` | `u8[4]` | unusedSpanD34 | written and read by no function; nothing fixes its width |
| `+0xD38` | `void*` | effectSourceCurrent | the effect source in use: `0x006FD070` picks it from `+0xD8`, `+0xE0`, `+0xE8` or `+0x28` (`0x006FD085`-`0x006FD0FB`); EndPostEffectScene_Process sets and restores it around the alpha pass (`0x006FB9D5`, `0x006FBE90`) |

`EndPostEffectScene_PreProcess` (`0x006F8740`) gives each effect that is on its own render-buffer slots from the ring `+0x4D0`, `+0x4D4` .. `+0x4D4` + `+0x36C` - 1 (`0x006F8904`-`0x006F8D53`). An effect that is off passes its source slot on as its result. `EndPostEffectScene_InternalProcess` (`0x006F9030`) then draws the effects in this order:

| Step | Effect | Runs while | Draw (call site) | Source slot | Result slot |
|---|---|---|---|---|---|
| 1 | Ambient occlusion | `+0xD30` | `0x006F61F0` (`0x006F9756`) | `+0x4DC` | `+0x4E0` |
| 2 | Temporal anti-alias | `+0xD31` | `0x006F65A0` (`0x006F9771`) | `+0x4E4` | `+0x4E8` |
| 3 | Depth of field, early | `+0xCE3` and `+0x55C` | `ApplyDepthOfField` `0x0077ECE0` in `0x006F6010` (`0x006F9791`) | `+0x4EC` | `+0x4F4`, work `+0x4F0` |
| 4 | Motion blur, early | `+0xD14` | `0x006F5740` (`0x006F9835`) | `+0x500` | `+0x508`, work `+0x504`, velocity `+0x50C` |
| 5 | Heat-shimmer particles | `+0xD24` | `HeatShimmerParticles` `0x00749FB0` (`0x006F9A8E`) | `+0x510` | `+0x514` |
| 6 | Depth of field, late | `+0xCE3`, `+0x55C` clear | `0x006F6010` (`0x006F9AE9`) | `+0x4EC` | `+0x4F4`, work `+0x4F0` |
| 7 | Optical vignette | `+0x494` | `0x007436B0` (`0x006F9C4D`) | `+0x4F8` | `+0x4FC` |
| 8 | Motion blur, late | `+0xD09`, `+0xD14` clear | `0x006F5740` (`0x006F9C67`) | `+0x500` | `+0x508`, work `+0x504`, velocity `+0x50C` |
| 9 | Aperture Airy disc | `+0xD01` | `0x00758860` (`0x006F9F78`) | `+0x518` | `+0x520`, work `+0x51C` |
| 10 | Gaussian blur | `+0xD08` | `0x00758860` (`0x006FA226`) | `+0x524` | `+0x52C`, work `+0x528` |
| 11 | Antialias | `+0xC55` | `0x0074DC40` (`0x006FA405`) | `+0x548` | `+0x54C` |
| 12 | Chromatic aberration | `+0x9D5` | `0x00743930` (`0x006FA569`) | `+0x538` | `+0x53C` |
| 13 | Chromatic-aberration copy | `+0x9DD`, never set | `0x007422F0` (`0x006FA66F`) | `+0x540` | `+0x544` |
| 14 | Lens distortion | `+0xD27` | `0x00743410` (`0x006FA8B6`) | `+0x530` | `+0x534` |
| 15 | Glare and tonemap | always; glare while `+0xC74` and `+0x6E4` allow (`0x006FAB37`-`0x006FAB69`) | `GenerateGlare` `0x00769C50` (`0x006FB116`), `TonemapToSurface` `0x00769FC0` (`0x006FB53F`) | `+0x550` | the output target |

Each result slot is the next step's source slot: `+0x4E0` = `+0x4E4`, `+0x52C` = `+0x548`, `+0x54C` = `+0x538`, `+0x53C` = `+0x540`, `+0x544` = `+0x530` and `+0x534` = `+0x550` = `+0x554` are stored from one register (`0x006F8967`-`0x006F8D53`). Motion blur takes its slots from `0x006FE080` at whichever of the two places `+0xD14` picks.

The init descriptor, `PFX_INITPARAM` (named by Initialize's check of its first field), is `0x118` bytes. `0x006CBBC0` writes its defaults; `0x006CBD20` builds one on its stack and changes four fields before `0x006DAA70` passes it on (`0x006CBDD7` to `0x006CBDF3`). Initialize copies it to `+0x210` and again to `+0x328` (`0x006FFA65`, `0x006FFB0B`) and works from the second copy.

`PpfxInitDescriptor` (`0x118` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `i32` | effectViews | PFX_INITPARAM::m_nEffectViews, the number of effect views: default 1 (`0x006CBBC2`); Initialize refuses a value below 1 with "PFX_INITPARAM::m_nEffectViews must be greater than or equal to 0." (`0x006FFDBB`) and allocates one auto-exposure record (`0x68` bytes) and one auto-focus record (`0x48` bytes) per view (`0x00700B5A`-`0x00700D9E`) |
| `+0x004` | `u32` | sceneFormat | a texture format code for the effect buffers; 0 (the default) lets `0x006F2380` choose, or the value at rbp-`0x80` when CPostEffect `+0x48F` is set (`0x00700F2B`-`0x00700F59`); read at `0x007003ED` |
| `+0x008` | `u32` | sourceFormat | a second format code (`0x007003F7`); 0 takes `+0x04`'s value unless CPostEffect `+0x48C` is set (`0x00700443`); when it differs from `+0x04`'s result Initialize sets CPostEffect `+0x488` (`0x00700FB8`-`0x00700FC6`) |
| `+0x00C` | `u32` | sampleLimit | read at `0x00700402`; 0 becomes `0x7FFFFFFF` (`0x00701002`-`0x00701011`), the limit Initialize passes to `0x0071B9C0` (`0x0070104D`-`0x0070106A`); 2 or more back from that call sets CPostEffect `+0x488` |
| `+0x010` | `u32` | renderWidth | the render width; 0 (the default) takes the width of the device surface description at CPostEffect `+0x38` (`+0x08`) (`0x00700340`-`0x0070035D`) |
| `+0x014` | `u32` | renderHeight | the render height; 0 takes the device surface's height (`+0x0C`) (`0x0070034B`-`0x0070036C`) |
| `+0x018` | `u32` | sceneWidth | the render-scene width; 0 takes `+0x10`'s result (`0x00700370`-`0x0070037B`); a size different from the render size sets CPostEffect `+0x488` (`0x00700FCD`-`0x00700FE8`) |
| `+0x01C` | `u32` | sceneHeight | the render-scene height; 0 takes `+0x14`'s result (`0x0070037E`-`0x00700389`) |
| `+0x020` | `f32[2]` | aspect | `+0x20` is the view aspect ratio as a float: the game stores 16 / 9 (`0x008C5B38`, `0x006CBDD7`); 0 or less makes Initialize use render width / height (`0x007007AB`-`0x007007C1`, copy at CPostEffect `+0x348`); `+0x24` is a float kept at `+0x34C`: 0 or less becomes 4/3 with init flag `0x20000000`, else 1.0 (`0x0070083F`-`0x00700849`, `0x00700887`-`0x00700891`) |
| `+0x028` | `f32[2]` | sizeRatios | two floats kept at CPostEffect `+0x350` and `+0x354`: a value of 0 or less becomes 1.0, or 1.5 (`+0x28`) and 2/3 (`+0x2C`) when init flags `0x20000000` / `0x40000000` are set (`0x00700829`-`0x007008A5`); the glare sizing divides the aspect ratio by `+0x28` (`0x00701EFA`-`0x00701F18`) and the depth-of-field sizing divides by `+0x2C` (`0x00702566`); default 0 (`0x006CBBD9`) |
| `+0x030` | `u8` | dofScaleLinear | default 1 (`0x006CBC06`); when 0 the depth-of-field buffer scale becomes a square root (`0x0070256E`-`0x0070257F`, copy at CPostEffect `+0x358`) |
| `+0x031` | `u8[3]` | pad031 | written and read by no function; nothing fixes its width |
| `+0x034` | `i32` | tonemapConvolution | the tonemap convolution level: default -1 (`0x006CBC0A`) lets Initialize pick 1 when the render size differs from the device surface and 0 otherwise; any other value is kept at CPostEffect `+0xC48` (`0x0070377E`-`0x007037CA`), and 1 or more allocates m_pTonemapConvolutionTexture (`+0x1D0`) |
| `+0x038` | `u8[8]` | views | the qword 1 (`0x006CBC11`); the game's stack copy stores 0 in its first dword (`0x006CBDE8`) |
| `+0x040` | `i32[2]` | bufferCounts | `+0x40`: a count clamped to 0..16 into CPostEffect `+0x368` (`0x006FFE05`-`0x006FFE1E`), which sets the render-buffer slots `+0x4CC` and `+0x4D0` (`0x007011B7`-`0x007011F0`); `+0x44`: a count kept at `+0x36C`, raised to at least 1 by init flag `0x40000` and to at least 2 by `0x80000` (`0x006FFE2A`-`0x006FFE80`); default 0 (`0x006CBBDD`) |
| `+0x048` | `u32` | referenceWidth | the width the effect buffers are sized from; 0 (the default) takes the render width, or 1280 with init flag `0x200` (`0x007006D9`-`0x0070070B`); the game stores 1920 (`0x006CBDF3`) |
| `+0x04C` | `u8[4]` | glareScale | the glare buffer scale, a float; 0 or less takes `+0x00` of the glare quality row at `0x01F3C5B0` (8 bytes per row, indexed by the glare quality argument) (`0x00701EE7`-`0x00701EF7`); default 0 |
| `+0x050` | `u32[2]` | glareSize | `+0x50`: the glare buffer width, 0 = from the scale (`0x00701F64`-`0x00701F69`); `+0x54`: overrides the glare quality row's `+0x04` (`0x00701F6F`-`0x00701F7C`); default 0 (`0x006CBBE5`) |
| `+0x058` | `u32` | formatA | a texture format code; 0 lets `0x006F2410` choose (`0x00700F5C`-`0x00700F74`); passed into the glare initialisation record (`0x007020F0`) |
| `+0x05C` | `u32` | formatB | a texture format code; 0 lets `0x006F24F0` choose, or `0x1D` when CPostEffect `+0x48D` is set (`0x00700F77`-`0x00700FB4`); passed into the glare initialisation record (`0x007020F9`) |
| `+0x060` | `f32[2]` | glareParams | `+0x60` (default 0.25, `0x006CBC19`) and `+0x64`: the first two values of the record Initialize hands m_pRenderGlare->Initialize (`0x007020C6`-`0x007020DC`, record at rbp+`0xB0`, call at `0x007021E0`) |
| `+0x068` | `u8[2]` | glareFlags | two bytes, default 1 and 1 (`0x006CBC21`), copied into the glare initialisation record (`0x0070213C`-`0x00702150`) |
| `+0x06A` | `u8[2]` | pad06A | written and read by no function; nothing fixes its width |
| `+0x06C` | `u32` | glareCount | default 8 (`0x006CBC27`); copied into the glare initialisation record (`0x00702120`) |
| `+0x070` | `u8[8]` | glareTail | `+0x70`: a float, default 0.25 (`0x006CBC2E`), copied into the glare initialisation record (`0x0070212C`); `+0x74`: 0 makes Initialize call `0x00711C10` after the glare set-up (`0x007022A8`-`0x007022B7`) |
| `+0x078` | `u32[2]` | lightShafts | `+0x78`: the number of light shafts, default 1 (`0x006CBC36`), clamped to 1..16 at CPostEffect `+0x3A0` (`0x007008AF`-`0x007008CA`); with init flag bit `0x10000000` Initialize allocates that many `0x68`-byte light-shaft records at `+0x6F0` (`0x007008D7`-`0x0070092F`) and sets each up (`0x00704878`-`0x00704920`); `+0x7C`: the depth-of-field buffer scale, 0 or less = `+0x00` of the depth-of-field quality row (`0x00700717`, `0x0070254A`-`0x0070255A`) |
| `+0x080` | `u32[2]` | dofSize | `+0x80`: the depth-of-field buffer width, 0 = from the scale (`0x007025E4`); `+0x84`: overrides `+0x04` of the depth-of-field quality table row at `0x01F3C5F0` (`0x1C` bytes per row) (`0x007025F0`-`0x00702600`); default 0 (`0x006CBBED`) |
| `+0x088` | `i32[2]` | dofTable | `+0x88`: overrides `+0x08` of the depth-of-field quality row when above -1 (`0x007007D9`-`0x007007ED`), which `0x00713EB0` converts for the depth-of-field initialisation record (`0x0070276D`-`0x007027A6`); the game stores 2 (`0x006CBDDD`); `+0x8C`: overrides the quality row's `+0x10` when not negative (`0x00702603`-`0x0070261C`); default -1 (`0x006CBC3E`) |
| `+0x090` | `i32[14]` | dofRow | fourteen values that replace the depth-of-field table row at `0x01F3C820` (`0x38` bytes per row) in the depth-of-field initialisation record when the first is not negative (`0x00702620`, `0x007027C9`-`0x0070286E`); default -1 each (`0x006CBC7D`-`0x006CBCBF`) |
| `+0x0C8` | `u32` | dofFormat | the depth-of-field texture format, 0 (the default) = the scene format; checked with the device (vtable `+0x260`) before use (`0x007026FF`-`0x00702757`) |
| `+0x0CC` | `i32` | dofTableB | overrides `+0x0C` of the depth-of-field quality row when above -1, and is forced to 0 while the byte `0x00D9F05E` is 0 (`0x007007F0`-`0x00700819`); 0 makes Initialize call `0x007233F0` on the device (`0x0070275B`-`0x00702768`); default -1 (`0x006CBC49`) |
| `+0x0D0` | `f32` | dofParamA | default 0.85 (`0x006CBC53`); the first of five floats copied into the depth-of-field initialisation record (`0x007029B9`) |
| `+0x0D4` | `f32[2]` | dofParamB | default 0.75 and 0 (`0x006CBC5D`); the second and third floats of the depth-of-field initialisation record (`0x007029C9`, `0x007029D9`) |
| `+0x0DC` | `f32` | dofParamC | default 1.0 (`0x006CBC68`); the fourth float of the depth-of-field initialisation record (`0x007029E9`) |
| `+0x0E0` | `u8[8]` | dofParamD | `+0xE0`: default 1.0 (`0x006CBC72`), the fifth float of the depth-of-field initialisation record (`0x007029F9`); `+0xE4`: overrides the depth-of-field quality row's `+0x14` when non-zero (`0x00702643`-`0x00702650`) |
| `+0x0E8` | `f32` | dofParamE | overrides the depth-of-field quality row's float `+0x18` when positive (`0x00702654`-`0x00702664`); default 0 (`0x006CBBFA`) |
| `+0x0EC` | `u8` | dofFlag | default 0 (`0x006CBC00`); copied into the depth-of-field set-up at `0x00702668` |
| `+0x0ED` | `u8[3]` | pad0ED | written and read by no function; nothing fixes its width |
| `+0x0F0` | `u8[8]` | velocitySize | `+0xF0`: the motion-blur velocity texture scale, a float, 0 = 1.0 (`0x00702B23`-`0x00702B2E`); `+0xF4`: its width, 0 = from the scale (`0x00702B5F`-`0x00702B64`); default 0 (`0x006CBCCA`) |
| `+0x0F8` | `u8[8]` | velocityFormat | `+0xF8`: the motion-blur velocity texture format, 0 = the value `0x00713820` picks (`0x00702BC0`-`0x00702BC8`); `+0xFC`: the ambient-occlusion normal-depth texture scale, a float, 0 = 1.0 (`0x00702D53`-`0x00702D61`); default 0 (`0x006CBCD1`) |
| `+0x100` | `u32` | aoWidth | the ambient-occlusion normal-depth texture width, 0 (the default) = from the scale (`0x00702D96`-`0x00702D9E`) |
| `+0x104` | `u32` | aoFormat | the ambient-occlusion normal-depth texture format, 0 (the default) = `0xA` (`0x00702CAC`-`0x00702CBA`) |
| `+0x108` | `u32` | dword108 | default 0 (`0x006CBCDF`); Initialize reads it into rbp+`0x28` (`0x00700435`) and uses it at `0x0070305A` in the ambient-occlusion set-up |
| `+0x10C` | `u32` | texUtilSize | default `0x100` (`0x006CBCE5`); Initialize hands it to the texture utility as its `+0x222C0` (`0x00700E27`-`0x00700E2D`) |
| `+0x110` | `u8` | externalFlag | default 0 (`0x006CBCEF`); kept at CPostEffect `+0x438`, which Initialize also sets when `+0x114` is 1 or 2 (`0x006FFC99`-`0x006FFCA6`) and copies to `+0x488` (`0x0070060B`) |
| `+0x111` | `u8[3]` | pad111 | written and read by no function; nothing fixes its width |
| `+0x114` | `u32` | externalMode | default 0 (`0x006CBCF5`); 1 or 2 sets CPostEffect `+0x438`, and 2 also adds init flag `0x400` (`0x006FFC99`-`0x006FFDB1`) |

The integration object at `0x02D38540`, `0x10` bytes from `0x0065E5D0`:

`PostProcessingLibraryWrapper` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | record | the `0x78`-byte integration record built by `0x006CBAA0` (`0x0065E553`-`0x0065E56D`); every wrapper of `0x00193DA0` loads it first |
| `+0x08` | `u8` | ready | the ready flag: 0 from the constructor `0x0065E530` (`0x0065E54C`), 1 from `0x0065E580` after `0x006CBD10` (`0x0065E591`, called at `0x0062549D`); `0x0018E470` reads it through `0x001976E0` (`0x0018E481`) and builds the post-process command only while it and the render parameter block's `+0xA0` are set |
| `+0x09` | `u8[7]` | pad009 | written and read by no function; nothing fixes its width |

The render parameter block's switch fields (the block is `0x4A8` bytes; the rest is on
[Graphics settings](../Engine-Core/graphics-settings.md)):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0A0` | `u8` |  | the pass is on (constructor value 1) |
| `+0x0A1` | `u8` |  | the pending value of a delayed change |
| `+0x1F0` | `i32` |  | frames left before the pending value is applied |

The library's global block, `0xD40` bytes at `[0x02EA0B70]`, as far as its constructor `0x006FF5D0`
lays it out:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0A8` | `u8[16]` |  | map header, built by `0x00714800` |
| `+0x0B8` | `u8[16]` |  | map header, built by `0x007147A0` |
| `+0x0C8` | `u8[16]` |  | map header, built by `0x00714740` |
| `+0xC80` | `void*` |  | cleared by the constructor |

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

### Columns of yebis-ppfx-post-effects-unlisted-bodies.tsv

One row per body, 732 rows, each inside the span between two functions of
[`yebis-ppfx-post-effects-members.tsv`](yebis-ppfx-post-effects-members.tsv).

| Column | Holds |
|---|---|
| `member_below` | the nearest function of the member list below the body (183 distinct values) |
| `member_above` | the nearest function of the member list above the body (183 distinct values) |
| `refs` | how many places in the image name the body's start address: a call, jump or RIP-relative operand, a call or jump found by scanning the code bytes, an 8-byte relocated pointer, or a 4-byte image offset in a data section (the unwind table `.pdata` is not counted); 0 on 618 rows, 1 on 112, 2 on 2 |

### Columns of yebis-ppfx-post-effects-diagnostic-strings.tsv

| Column | Holds |
|---|---|
| `owner_functions` | the start addresses of the functions that hold the string's call sites, in address order and separated by spaces; one function on 347 of the 385 rows, up to 12 on six rows. 160 functions occur, all inside the span; `0x006FF900` is the one owner of 44 strings |

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

### The depth of field's sample count

`0x006EF480(n, out, scale)` called with a null `out` returns `3 x n x (n + 1) + 1` at once
(`0x006EF48E`-`0x006EF4B3`). The static initialiser `0x00168EE0` calls it with 5, a null `out` and 1.0, and keeps the
result.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EA4024` | `i32` | 0 (zero-filled tail) | 91, the count `0x006EF480(5, 0, 1.0)` returns; both readers take `trunc(sqrtf(count x 4 / π))` from it (`0x00DABDDC`, 1.27324), which is 10 | `0x00168EE0` (`0x00168EF6`) | `CDepthOfField::CreateDeviceResources` `0x0076F400` (`0x0077075B`); `CDepthOfField::CreateScatterBokehTexture` `0x0077A8C0` (`0x0077AA08`) |

No other instruction reaches `0x02EA4024`: no other RIP-relative, image-base-relative or 32-bit offset reference names
it. The addresses taken near it are two one-time initialisation guards, `0x02EA4020` (`0x00763890`) and `0x02EA4008`
(`0x00764240`), and a loop bound, `0x02EA4010` (`0x00764240`).

### The library's other statics

Every other written static of the library is a row of
[yebis-ppfx-post-effects-state.tsv](yebis-ppfx-post-effects-state.tsv), with its type, start value, meaning and
every writing and reading instruction. The sections below explain each group; the table names the rows.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| each row of [yebis-ppfx-post-effects-state.tsv](yebis-ppfx-post-effects-state.tsv): 210 statics from `0x01F3C500` to `0x02EA40BC` | per row | per row: the image value for the `01F3xxxx` rows, 0 (zero-filled tail of `.data`) for the rest | per row, by group below | per row (`set_by`) | per row (`read_by`); `-` for the 8 statics that no code reads |

### Render-target bindings

`CRenderTexture` (vtable `0x00D9C040`) keeps the device's eight colour targets in two parallel arrays: the render
texture bound to slot *n* at `0x02EA18C0` + 8*n* and the surface of it in use at `0x01F3CB18` + 4*n*. The binder
`0x007224C0` stores both (`0x007225A9`, `0x007225B1`); a caller passing surface -1 gets the stored one (`0x0071FD78`). Every
loop over the slots stops at 8.

- `0x02EA1914` counts the render textures attached to the current device. Slots 0 (`0x007214A0`) and 5 (`0x007215C0`)
  add 1 when a texture attaches to a new device; slot 1 (`0x00721B10`) subtracts 1 when it detaches. An attach at 0
  stores the device in `0x02EA1918` and clears both arrays; a detach back to 0 clears `0x02EA1918` and both arrays. No
  instruction reads `0x02EA1918`.
- `CRenderTexture::BeginTiling` (`0x00722A40`) counts the bound targets into `0x02EA190C` and keeps its first, third and
  fourth arguments and the 16 bytes at its second in `0x02EA1908`, `0x01F3CB38`, `0x02EA1910` and `0x02EA1938`. No
  instruction reads those five. `EndTiling` (`0x00722C80`) clears both arrays and `0x02EA1908`.
- `0x02EA18B1` is 1 while tiling is on: `BeginTiling` returns at once when it is set (`0x00722A44`) and sets it
  (`0x00722C30`); `EndTiling` tests it (`0x00722C84`) and clears it (`0x00722E21`, `r8d` cleared at `0x00722CD5`).
- `BeginTemporaryFilter` `0x006F2560` (`0x006F25EB`) and `EndPostEffectScene_PreProcess` `0x006F8740` (`0x006F8D78`, its copy to
  `CPostEffect` `+0xCE2`) read the flag, and so do `0x00721B10`, `0x00722110`, `0x007224C0`, `0x007226E0`, `0x00722800`, `0x00722900`
  and `0x00722E80`.
- The game calls `BeginTiling` itself at `0x005FED6F` (`0x005FECF0`) and `0x0060F9A0` (`0x0060F830`).

### Device and resource registry

- `0x02EA1948` is the current `IGPUDevice` (vtable `0x00D9EA30`): `IGPUDevice::InitializeDevice` (`0x00723760`) stores
  it and `~IGPUDevice` (`0x00724500`) clears it. The texture creators `0x007875F0` and `0x00787A90` use it when their
  caller passes no device.
- `0x02EA1960` is a 0x28-byte device description that `InitializeDevice` and slot 5 (`0x00724940`) copy from their
  argument, or clear. `InitializeDeviceBuffers` (`0x00723440`) replaces a 0 width (`0x02EA1960`) or height (`0x02EA1964`)
  with the one the device reports through its slot `+0x80` (`0x00723473`), and takes a reference to the back buffer at
  `+0x20` (`0x02EA1980`) when one is given.
- `0x02EA1998` and `0x02EA19A8` are the resource registry of `GPUResourceManage.cpp`: the device of the first
  registration (`0x00727460`, through `0x00727800`) and a 0x18-byte list of the registered resources. The last
  unregistration (`0x007276F0`) frees the list and clears both (`0x00727870`).
- `CRenderTextureArray::InitializeDevice` (`0x0075C080`) hands each member's `InitializeDevice` (`0x00720320`) its
  depth-stencil format through `0x02EA1920` (`0x2D` when the array's `+0x58` is 0) and `0x02EA1924` (the same when its
  flag `0x10000` is set, else 0), and clears both after the call.

### Effect-constant staging buffers

The passes stage their shader constants in three static buffers and hand each to their effect's vector-array setter,
slot `+0x98` of `IGPUEffect` (vtable `0x00DAF1B8`, built by `0x00789900`):

| Buffer | Size | Filled by | Handed over by |
|---|---|---|---|
| A, `0x02EA1A50` | `0x100` bytes, up to the next static `0x02EA1B50` | the loops below and direct stores | 25 calls |
| B, `0x02EA1C50` | 16 vectors: `0x0074AB30` and `0x0074B6A6` hand over 16 | the loops below and direct stores | 38 calls |
| `0x02EA1B50` | 3 vectors | `0x00737740`, `0x00737A30` | `0x0073792C`, `0x00737C86` |

`0x00789D50`, the setter, adds 1 to `0x02EA40B8` and the vector count to `0x02EA40BC`, then calls the effect it wraps
(`+0xE0`) at slot `+0x58`. That is `CTinyEffect` `0x0078FCF0`, which copies the smaller of the count and the
parameter's size, in 16-byte vectors, with `memcpy` (`0x0078FD45`). Nothing reads `0x02EA40B8` or `0x02EA40BC` except
their own adds.

Every call is a row of
[yebis-ppfx-post-effects-constant-uploads.tsv](yebis-ppfx-post-effects-constant-uploads.tsv) with its vector count. A
staged vector is read when a call's count reaches it; the state table lists those calls in each vector's `read_by`.
The loops that write the buffers through a pointer:

| Buffer | Function | Loop stores |
|---|---|---|
| A | `0x00735240`, `0x00735530`, `0x00735720`, `0x00735B70`, `0x007364D0`, `0x00737740`, `0x00737A30`, `0x00737D70` | copy the pass's vectors from its argument, then zero the rest of the count (`0x007353B8`, `0x00735400`, `0x00735440`; `0x00735608`, `0x00735640`; `0x00735A18`, `0x00735A63`, `0x00735AB0`; `0x00735CD9`, `0x00735D20`, `0x00735D60`; `0x007365D8`, `0x00736610`; `0x00737820`, `0x00737848`, `0x00737877`; `0x00737B90`, `0x00737BB9`, `0x00737BE7`; `0x00737F4C`, `0x00737F83`, `0x00737FC0`) |
| A | `0x0073AC70`, `0x0073B5A0` | fill *n* taps with 1/*n*, then add them into tap *n* (`0x0073ADD0`-`0x0073AF73`; `0x0073B679`-`0x0073B752`) |
| A | `0x00735E40` | packs its floats, zero-filled (`0x00736343`, `0x00736365`) |
| A | `0x00774260` | `0x00774A6C`-`0x00774AC4` |
| B | `0x00735E40` | copies up to 8 vectors and zeroes the rest (`0x00735FE8`, `0x00736017`), then the second set (`0x007360CE`-`0x007362E7`) |
| B | `0x00734EB0` | `0x00734F39`-`0x0073509F` |
| B | `0x00774260`, `0x00777590`, `0x007788A0` | through `0x0072F910`, which returns `0x02EA1C50` (`0x00774AD6`-`0x00774B5E`; `0x00777AE4`-`0x00777CFD`; `0x00778D31`-`0x00778D40`) |

### Columns of yebis-ppfx-post-effects-constant-uploads.tsv

| Column | Holds |
|---|---|
| `count_set_at` | the address of the instruction that writes the vector count into `r9d`, the setter's fourth argument, before the call at `site`: a `mov` on 57 of the 65 rows, `lea` on 5, and `add`, `cmovl` and `sar` on one each. It lies in the same function, 4 to 336 bytes before the call |

### Lookup tables built on first call

Four converters fill a small `i32` table the first time they run, set a flag and return the entry their argument
indexes:

| Function | Table | Flag | Entries | Called at |
|---|---|---|---|---|
| `0x00714040` | `0x02EA1498` | `0x02EA14BC` | 0, 1, 10, 2, 4, 6, 8, 14, 1 | `0x0071410B` (`0x007140C0`, the HDR encoding code), `0x006F27BF`, `0x006FABC5`, `0x0070C76A` |
| `0x00713DF0` | `0x02EA14C0` | `0x02EA14E0` | 0, 1, 2, 3, 4, 5, 5, 5 | `0x00702779` (`CPostEffect::Initialize`) |
| `0x00713EB0` | `0x02EA14E8` | `0x02EA14FC` | 0, 0, 2, 6, 6 | `0x00702770` (`0x006FF900`), `0x00711393`, `0x00711431` |
| `0x00713F60` | `0x02EA1550` | `0x02EA1588` | 0 to 13 | `0x006FAE5B` (`0x006F9030`), `0x0070768D` (`0x00707670`) |

`0x00713EB0` is `GetEffectDofEdgeQualityTypeFromEdgeQualityType`: above 4 it logs "Unsupported EPFX_DOFEDGEQUALITY"
(`0x00D90AE0`), and -1 returns `0x10000000`. `0x00713F60` returns -1 for -1.

Four more first-call tables fill with an 8-byte store of -1 and then their values, under a byte flag:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EA1500` | `i32` | 0 (zero-filled tail) | entry 0 of a two-entry table; the leaf `0x00708350` fills it with 0 | `0x006FF900` (`0x007051CC`, 8 bytes over entries 0 and 1; `0x007051D7`); `0x00708350` (`0x0070835A`, 8 bytes; `0x00708365`) | `0x00708350` (`0x0070838B`, for a second argument of 0) |
| `0x02EA1504` | `i32` | 0 (zero-filled tail) | entry 1; `0x00708350` fills it with 1 | `0x006FF900` (`0x007051CC`; `0x007051DE`); `0x00708350` (`0x0070835A`; `0x0070836B`) | `0x00708350` (`0x0070838B`, for a second argument of 1) |
| `0x02EA1508` | `u8` | 0 (zero-filled tail) | 1 once that table is filled | `0x006FF900` (`0x007051C5`); `0x00708350` (`0x00708375`) | `0x006FF900` (`0x007051BC`); `0x00708350` (`0x00708352`) |
| `0x02EA1510` | `i32` | 0 (zero-filled tail) | entry 0 of a four-entry table, 0, 1, 2, 3 (the 16 bytes of `0x01CEBCE0`), filled by whichever of `0x007091B0` and `0x00713FF0` runs first | `0x007091B0` (`0x007091FA`, 8 bytes, -1; `0x00709210`, 16 bytes over the four entries); `0x00713FF0` (`0x00714001`, `0x00714017`) | `0x007091B0` (`0x00709229`, index the dword `+0x470`, or 3 when its fourth argument is set; `0x007091D6`-`0x007091E5`); `0x00713FF0` (`0x00714030`, index its argument); both sign-extend the index and do not bound it |
| `0x02EA1518` | `i32` | 0 (zero-filled tail) | entry 2 of the same table, 2 | `0x007091B0` (`0x00709205`, 8 bytes over entries 2 and 3; `0x00709210`); `0x00713FF0` (`0x0071400C`, `0x00714017`) | `0x007091B0` (`0x00709229`); `0x00713FF0` (`0x00714030`) |
| `0x02EA1520` | `u8` | 0 (zero-filled tail) | 1 once that table is filled | `0x007091B0` (`0x00709218`); `0x00713FF0` (`0x0071401F`) | `0x007091B0` (`0x007091E9`); `0x00713FF0` (`0x00713FF0`) |
| `0x02EA1528` | `i32` | 0 (zero-filled tail) | entry 0 of a four-entry table, 0 to 3 (`0x01CEBCE0`) | `0x006FC760` (`0x006FCB72`, 8 bytes, -1; `0x006FCB88`, 16 bytes) | `0x006FC760` (`0x006FCBD1`, index the dword `+0x708`, sign-extended, not bounded) |
| `0x02EA1530` | `i32` | 0 (zero-filled tail) | entry 2 of that table, 2 | `0x006FC760` (`0x006FCB7D`, 8 bytes over entries 2 and 3; `0x006FCB88`) | `0x006FC760` (`0x006FCBD1`) |
| `0x02EA1538` | `u8` | 0 (zero-filled tail) | 1 once that table is filled | `0x006FC760` (`0x006FCB90`) | `0x006FC760` (`0x006FCB61`) |
| `0x02EA1540` | `i32` | 0 (zero-filled tail) | entry 0 of a two-entry table, 1 | `0x006F9030` (`0x006FAFE0`, 8 bytes over both entries, -1; `0x006FAFF0`) | `0x006F9030` (`0x006FB01D`, index the dword `+0xC6C`, sign-extended, not bounded) |
| `0x02EA1544` | `i32` | 0 (zero-filled tail) | entry 1, 3 | `0x006F9030` (`0x006FAFE0`; `0x006FAFFD`) | `0x006F9030` (`0x006FB01D`) |
| `0x02EA1548` | `u8` | 0 (zero-filled tail) | 1 once that table is filled | `0x006F9030` (`0x006FAFF6`) | `0x006F9030` (`0x006FAFD7`) |

`0x006FE7F0` hands the effect pass two colour matrices through its last two out-parameters (`0x006FEC8D`,
`0x006FECA4`): the matrix at `+0x7A4` when the byte `+0x924` is set and the one at `+0x7E4` when `+0x925` is set,
otherwise 0 (`0x006FE97D`-`0x006FE999`). Two statics, each behind a thread-safe static guard (`0x02EA15E0`, `0x02EA1630`;
`0x008092FC`, `0x0080929C`), can stand in for them:

- It copies the matrix at `+0x92C`, composed with the colour-space conversion when `+0x96C` differs from
  `+0x970` (`0x006FEA23`-`0x006FEA64`). When the copy is not the identity (`0x007124B0`), it is stored at `0x02EA15A0`,
  multiplied by the `+0x7E4` matrix when there is one (the 4×4 product `0x006F1070`), and becomes the second
  out-parameter (`0x006FEA97`-`0x006FEAD2`).
- The second static, `0x02EA15F0`, would be filled the same way from a matrix built as the identity on the stack
  (`0x006FEB37`-`0x006FEB8A`). The identity test always passes, so its stores (`0x006FEBA5`-`0x006FEBC4`) never run, it
  stays 0, and the first out-parameter is passed on as it was.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EA15A0` | `f32[4]` | 0 (zero-filled tail) | row 0 of the colour matrix copy | `0x006FE7F0` (`0x006FEA97`) | `0x006F1070` through the pointer passed at `0x006FEABF`; `0x006FE7F0`'s callers (`0x006F440A`, `0x006F6F3C`, `0x006F73DD`, `0x006FB1F7`) through its last out-parameter (`0x006FECA4`) |
| `0x02EA15B0` | `f32[4]` | 0 (zero-filled tail) | row 1 | `0x006FE7F0` (`0x006FEA9F`) | the same |
| `0x02EA15C0` | `f32[4]` | 0 (zero-filled tail) | row 2 | `0x006FE7F0` (`0x006FEAA7`) | the same |
| `0x02EA15D0` | `f32[4]` | 0 (zero-filled tail) | row 3 | `0x006FE7F0` (`0x006FEAAF`) | the same |
| `0x02EA15F0` | `f32[4]` | 0 (zero-filled tail) | row 0 of the second static, 0 at run time | `0x006FE7F0` (`0x006FEBA5`, never reached) | its address is taken only on the same unreached path (`0x006FEBD3`, `0x006FEBDA`, `0x006FEBE6`) |
| `0x02EA1600` | `f32[4]` | 0 (zero-filled tail) | row 1 of the second static | `0x006FE7F0` (`0x006FEBB1`, never reached) | the same |
| `0x02EA1610` | `f32[4]` | 0 (zero-filled tail) | row 2 of the second static | `0x006FE7F0` (`0x006FEBBD`, never reached) | the same |
| `0x02EA1620` | `f32[4]` | 0 (zero-filled tail) | row 3 of the second static | `0x006FE7F0` (`0x006FEBC4`, never reached) | the same |

Three more words of the library:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F3CAFC` | `i32` | 1 | a three-way setting: `0x00708350` stores entry `n` of the table `0x02EA1500` for its second argument `n` of 0 or 1 (an unsigned bound, `0x0070837C`-`0x0070838E`), -1 for -1 and 0 for any other value (`0x00708397`-`0x0070839F`); `CPostEffect::Initialize` stores -1. When its second argument is 0, `0x007083B0` answers -1, 0 or 1 for those values and -2 for any other (`0x00708436`-`0x00708467`); otherwise it passes the value to `0x007226A0` (`0x00708415`-`0x00708426`) and answers the same way for that result | `0x006FF900` (`0x007051E5`); `0x00708350` (`0x0070838E`, `0x0070839F`) | `0x007083B0` (`0x007083B4`) |
| `0x01F3CB3C` | `u8` | 1 | while it is set, the render-texture `InitializeDevice` (`0x00720320`) ends by calling `0x00722110(texture, 0, -1)` (`0x00720C26`-`0x00720C38`); `IPfxBaseRenderToTexture::Initialize` and `CPostEffect::Initialize` clear it | `0x006E04F0` (`0x006E06D7`); `0x006FF900` (`0x00700DF8`) | `0x00720320` (`0x00720C26`) |
| `0x02EA16B4` | `i32` | 0 (zero-filled tail) | a call counter of `0x006FF050`, kept while the byte `0x02EA147D` is set (`0x006FF074`): `(count + 1) mod 100`, a signed division (`0x006FF084`-`0x006FF0CA`); at 25, with the log levels `0x01F3BA80` and `0x01F3BA8C` at 1 or more (unsigned compares), it logs from source line `0x6DEB` (`0x006FF0DE`-`0x006FF0FB`) | `0x006FF050` (`0x006FF0CA`) | `0x006FF050` (`0x006FF084`) |
| `0x02EA1970` | `u32` | 0 (zero-filled tail) | the device description's `+0x10`; `InitializeDevice` copies it to the device's `+0x28` (`0x00723901`-`0x0072390A`), and the effect code takes it as an unsigned maximum (`cmova`) | `0x00168C10` (`0x00168C20`, 8 bytes over `+0x10` to `+0x17`); `0x00723760` (`0x007238C4`, 8 bytes, 0; `0x007238ED`, 16 bytes over `+0x10` to `+0x1F` from its argument); `0x00724940` (`0x00724968`, 16 bytes) | `0x00723760` (`0x00723901`); `0x006F4390` (`0x006F4B72`); `0x006F4C40` (`0x006F4CF2`, `0x006F4CF8`, `0x006F5660`); `0x00780260` (`0x00780372`, `0x0078037C`); `0x007809C0` (`0x00780A2E`, `0x00780A34`, `0x00780A9A`, `0x00780AA4`); `0x00784E80` (`0x00784F05`, `0x00784F60`, `0x00784F9C`); `0x007850C0` (`0x007850CC`, `0x00785117`); the code at `0x0070684D`, `0x007068A0` and `0x007068A6` |

### Technique-name suffix tables

`TEXSHADERSET::CreateEffect` (`0x0072A320`) looks up its techniques by name. Five helpers keep tables of name
suffixes, filled once while a flag byte (1 in the image) is set; each walk appends every suffix to the base name and
looks the technique up:

| Flag | Table | Suffixes | Filled by | Walked by |
|---|---|---|---|---|
| `0x01F3CD60` | `0x02EA2250` | 22 tone-map pairs, the first empty: `_REINHARDRGB_RGB` to `_ALPHA_RGB` | `0x0072DAC0`, `0x0072DCF0`, `0x0072DFD0` | the same three (`0x0072DC6D`, `0x0072DEFD`, `0x0072E1DD`) |
| `0x01F3CD61` | `0x02EA2300` | 16 curves: `_LINEAR` to `_ALPHALUM_PREMAP`, entry 10 empty | `0x0072E740` | `0x0072E740` (`0x0072E8AD`) |
| `0x01F3CD62` | `0x02EA2380` | 7 channels: `_RVALUE` to `_ABGR8` | `0x0072E2B0`, `0x0072E3E0` | `0x0072E2B0` (`0x0072E370`), `0x0072E3E0` (`0x0072E500`) |
| `0x01F3CD63` | `0x02EA23B8` | empty, `_USNORM` | `0x0072E5B0`, `0x0072E3E0` | `0x0072E5B0` (`0x0072E690`), `0x0072E3E0` (`0x0072E470`) |
| `0x01F3CD64` | `0x02EA23C8` | 7 steps: `_PreMatrix` to `_Gamma` | `0x0072E940` | `0x0072E940` (`0x0072EA34`) |

No instruction calls `0x0072E3E0` and no table points to it; its only references are its unwind entries
(`.pdata` `0x02FEBC28`, `.rdata` `0x01DCBD28`).

### Random states for noise

Two draws keep four 32-bit random states each, seeded once behind a thread-safe guard (`_Init_thread_header`
`0x008092FC`) with 1, `0x3391`, `0x61E9B` and `0xBF1`. While the draw's animate byte is set, each state steps as
`x = x * 0x5D588B65 + 0x1000001`, and `(x >> 14) / 262143` is a value from 0 to 1 that offsets the dither noise:

| States | Guards | Draw |
|---|---|---|
| `0x02EA2400`, `0x02EA2410`, `0x02EA2420`, `0x02EA2430` | `0x02EA2408`-`0x02EA2438` | `0x00739530` (animate byte `+0x130`) |
| `0x02EA2440`, `0x02EA2450`, `0x02EA2460`, `0x02EA2470` | `0x02EA2448`-`0x02EA2478` | `CTextureUtil::DrawRectGPU_TonemapHDR` `0x0073BD30` (`+0x2D0`) |

Two depth-of-field draws keep a xorshift-128 state each, seeded `0x6C078966`, `0xDD5254A5`, `0xB9523B81`,
`0x03DF95B3`: `0x02EA4038`-`0x02EA4044` in `0x00771B30` (guard `0x02EA4048`) and `0x02EA4050`-`0x02EA405C` in `0x00777590`
(guard `0x02EA4060`). Each step is:

```python
t = x ^ (x << 11);  x = y;  y = z;  z = w;  w = w ^ (w >> 19) ^ t ^ (t >> 8)
```

`0x02EA404C` counts the `SetApertureFilterLevelVisualize` branch of `0x00772410`, which prints "does not work properly"
only when the count is 0 or a multiple of 100.

### Glare definitions and colours

The glare code builds its look tables from two `.data` row lists when `CRenderGlare`'s constructor (`0x007687E0`)
allocates the definition object `0x02EA3D50`:

- `0x02EA3D40`: the star-line types, from the seven rows at `0x01F3CF20` (Disable, Cross, CrossFilter, SnowCross,
  SunnyCross, Vertical, Anamorphic), built by `0x0075F160`.
- `0x02EA3D48`: the glare types, from the 14 rows at `0x01F3D000` (Disable, Bloom, Lens Flare, Standard, Cheap Lens
  Camera, Afterimage, the cross filters and the streaks), built by `0x0075F960`.
- `0x0075F160` also writes two colour orders for the lines: `0x02EA3D60` white, red, green, blue and `0x02EA3DA0` white,
  blue, green, red. `0x00764240` picks one (`0x007644C3`) and hands it to the effect (`0x00764FA1`).

The destructor `0x007693B0` frees both tables and the object (`0x0075FA60`, `0x0075F390`). `0x00707670` copies a glare type
by index, but the thunk `0x006DBA00`, which jumps to it, is referenced by no instruction or table.

`0x0075B2F0` returns a seven-entry hexagon pattern built once (flag `0x02EA3D24`): `0x02EA3CB0` is (0, 0, 0, 0) and
entry *i* + 1 is (-sin 60*i*°, cos 60*i*°, 0, 0) for *i* = 0 to 5.

### Constant colours and the allocator's map

- Three draws keep the colour (1, 1, 1, 1) in a guarded lazy static: `0x02EA2480` (`0x00748C00`), `0x02EA3FF8`
  (`0x00764240`) and `0x02EA4010` (`0x00763890`).
- The game's allocator `0x02E5BDE0` counts its live allocations at `+0x08` (`0x02E5BDE8`) and their bytes at `+0x10`
  (`0x02E5BDF0`). It maps each address to its size, file and line in a red-black tree headed at `+0x18`
  (`0x02E5BDF8`). The head is also the nil node that leaf links point to; `+0x30` (`0x02E5BE10`) holds the root, and
  `+0x30` to `+0x40` stand in as the root's parent.
- The initialiser `0x00167990` stores the head's address in all six words. Inserts (`0x006CBA20`), rebalancing
  (`0x0067F700`, `0x0067F9D0`) and erases (`0x0067FE20`) rewrite the root and the nil node's parent word (`0x02E5BE08`), and
  read the second link and the colour bit of the root's parent position (`0x02E5BE18`, `0x02E5BE20`).
- `0x01F3C500` lets `0x006F1270` fill the eleven maximum vectors at `0x02EA13C0` once.
- `0x02EA17B0` is the text `0x0071B070` builds for the texture-creation log lines (`GPUUSAGE_RENDERTARGET`,
  `GPUUSAGE_DEPTHSTENCIL`).

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
