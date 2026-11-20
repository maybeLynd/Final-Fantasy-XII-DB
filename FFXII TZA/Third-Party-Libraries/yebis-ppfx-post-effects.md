[Home](../../README.md) / [Third-party libraries](README.md) / YEBIS and PPFX

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| YEBIS and PPFX: the post-effect library, how the game starts and drives it, its licence check and the EnableYebis switch | system | Third-party libraries | Library details | Silicon Studio's YEBIS post-effect library (its core is named PPFX) as linked into the game: its address span and identity, the source paths and diagnostic log it carries, the API entry points, how the renderer creates its context and runs it each frame, the licence verifier and why the shipped licence never reaches its date test, and the EnableYebis switch with its delayed form. | 0x006DA880, 0x006DA8A0, 0x006DA8F0, 0x006DAA50, 0x006DA990, 0x006DAA70, 0x006DE780, 0x006DFF40, 0x0071D9E0, 0x006FF900, 0x0070BA00, 0x00707560, 0x006DF480, 0x006CBD20, 0x006CBEA0, 0x00193DA0, 0x0018E470, 0x00194290, 0x00194A30, 0x001F3300, 0x00167990, 0x02E5BDE0, 0x02EA0B70, 0x02EA0B3C, 0x02EA0B90, 0x00D86C00, 0x00717760, 0x0065E530, 0x006CBAA0, 0x0078A530, 0x0072A320, 0x00E21F90 |

## What the player sees

The remaster's glare around bright light and its depth of field come from a bought-in post-effect
library, Silicon Studio's YEBIS, whose core calls itself PPFX. The game hands it each rendered frame
and it writes the finished image. The Glare and DepthofField options in the
settings switch those two effects; the `EnableYebis` configuration key switches the whole pass off,
and then the frame is shown without post-effects. The library also carries a licence check with an
expiry message, which the shipped game never prints.

The `EnableYebis` value is read from the scene and map configuration files, where 1 means on. A script command can
also switch the pass, and can ask for the change to wait a set number of frames.

## How it works

### The library in the image

The library is the code from `0x006DA880` to `0x007911DF`. Its identity is in its own type names and
texts:

- RTTI `Yebis::YebisPfxMemoryAllocatorD3D11` (`0x01F70BC8`, vtable `0x00D86BD8`) and
  `Yebis::PfxShimD3D11`¹, beside `PPFX::CPfxMemoryAllocator` (vtable `0x00D8E1E8`) and
  `PPFX::IPfxContext_Dx11`.
- The licence text `FeatureId = YEBIS_D3D11, ...`² and the messages "YEBIS Expiration
  Problem"³ and "The YEBIS library passed over the expiration date : %s"⁴.
- The string `TjmjdpoTuvejp`⁵, which is `SiliconStudio` with every character raised by
  one; no code or data refers to it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x01F70C38` |
| ² | `0x00D86C00` |
| ³ | `0x00D8F1A8` |
| ⁴ | `0x00D8F690` |
| ⁵ | `0x00D8F1C8` |

</details>

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

`0x006DF480` is the library's log. It has 801 direct call sites, 800 calls and the tail jump at
`0x00788471`, every one inside the library. At 798 of them every path into the call loads a literal
format string; the other three¹ print a message the function
assembled on the stack.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00727604`, `0x007276A0`, `0x007277A0` |

</details>

Seven calls are shared by branches that load different strings, so 422 distinct strings reach the
log over 835 string-and-call pairs. Most are a prefix naming the source file followed by the
message, such as "..\src\GPU\GPUPostEffect.cpp(%d) : Feb 18 2016 PPFX ERROR: " (113 sites).
The game's own code never calls it.

`0x006DF480` formats the message into the `0x800`-byte buffer `0x02EA0BA0` (`__stdio_common_vsprintf`, `0x006DF4CC`) and
passes it to the callback in `0x02EA0B88` when one is set¹, otherwise to `OutputDebugStringA`². The only store to `0x02EA0B88` is `0x006DF3A0`, which no instruction calls and no 8-byte pointer in the
image names, so the messages go to the debugger output. On both paths it returns the formatter's result, or -1
when that result is negative³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006DF4EF` |
| ² | `0x006DF4FA` |
| ³ | `0x006DF4D2`-`0x006DF4E0`, `0x006DF4F1`, `0x006DF500` |

</details>

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
| `0x006DE950` | `ppfxInitialize()` |
| `0x00708110` | `CPostEffect::SetMultisampleMode` |
| `0x0070B780` | `CPostEffect::BeginPostEffectScene` |
| `0x0070B990` | `CPostEffect::EndPostEffectScene` |
| `0x0070CD40` | `CPostEffect::SetFramebuffer`, which refuses to run between Begin and End |
| `0x00705520` | `CPostEffect::Uninitialize`, which returns `0x80004005` between Begin and End |
| `0x006E04F0` | `IPfxBaseRenderToTexture::Initialize` |
| `0x006E07A0` | `IPfxBaseRenderToTexture::Uninitialize` |
| `0x007067E0` | `CPostEffect::UpdateAlternateFrame` |
| `0x00707880` | `CPostEffect::SetLightShaftEnable` |

`0x007067E0` is `CPostEffect::UpdateAlternateFrame` by its log string¹. With a null `m_pGPUDevice` (`+0x20`)
it returns `0x80004005`; with the byte `+0x00` set it returns the same, after the ERROR line of `0x00D96A70` (source
line `0xC33`) when the levels `0x01F3BA80` and `0x01F3BA90` are both at least 1; otherwise it calls
`0x007247E0(m_pGPUDevice)` and returns 0². The only direct call or jump to it is the jump of the
thunk `0x006DB460`, which loads `[0x02EA0B70]`; no direct call or jump and no stored address in the image names that
thunk.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00D96A70` |
| ² | `0x007067E4`-`0x00706833` |

</details>

`CPostEffect::SetLightShaftEnable`¹ reads the byte `+0xFC` of `m_pRenderGlare` (`+0x110`) and tests it
against the enable². With it set, the enable byte goes to `+0x60` of the `0x68`-byte record
`[+0x6F0]` + `+0x6F8` x `0x68`, written 0 and then 1 for a non-zero enable, and the call returns 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00707880` |
| ² | `0x00707884`-`0x007078AC` |
| ³ | `0x007078AE`-`0x007078E8` |

</details>

With that byte clear a zero enable returns 0 and a non-zero one returns 1, after the WARNING line
`CPostEffect::SetLightShaftEnable(): Initialize() with PFXINIT_LIGHTSHAFT flag for light shafts.` (`0x00D94BB0`, source
line `0x2BDA`) when the levels `0x01F3BA80` and `0x01F3BA8C` are both at least 1¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007078ED`-`0x0070791C` |

</details>

### Render states the D3D11 device refuses

Three render-state methods of `IGPUDevice` do nothing and return `0x80004001` (E_NOTIMPL):
`0x00724EC0` DepthTestEnable, `0x00724F50` DepthFunc and `0x00724FF0` AlphaFunc. Each counts its calls¹. It prints its "is not supported" warning only when the count
is 0 or leaves 25 when divided by 100, and only while `0x01F3BA80` and `0x01F3BA8C` are both non-zero.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02EA1988`, `0x02EA198C`, `0x02EA1990` |

</details>

### Messages no code prints

No instruction or stored pointer in the image refers to these texts:

- "IGPUDevice::ApplyRenderState_AlphaTestEnable() is not supported (DX10/11)."¹;
- the three log lines of
  `CDepthOfField::ApplyDepthOfField_ApertureFilterLevel_EAPERTUREFM_DISC_ApplyApertureFilter`
  (`0x00DA8660` failed, `0x00DA8710` succeeded, `0x00DAADB0` the call).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00D9C8A0` |

</details>

### Start-up

| Step | What happens | Where in the code |
|---|---|---|
| 1 | The static initialiser `0x00167990` builds the game's allocator object `0x02E5BDE0` with the vtable of `Yebis::YebisPfxMemoryAllocatorD3D11`: the base constructor `0x006DA860` stores the vtable `0x00D8E1E8` and the initialiser replaces it with `0x00D86BD8`.<br>• It zeroes the allocation count `+0x08` and the byte count `+0x10` and stores the head `0x02E5BDF8` in the six tree words `+0x18` to `+0x40`.<br>• It sets up the node pool at `+0x48` with `0x0067FFB0(pool, 0x40, 8, 8, "PMapPair")`, which stores the name at the pool's `+0x08`, `0x40` at `+0x18`, 8 at `+0x1C` and at `+0x20`, and zero at `+0x00` and `+0x10`.<br>• It ends by registering the teardown `0x008B6E00` with `atexit`, through a tail jump.<br>• The teardown stores the vtable `0x00D86BD8` in `0x02E5BDE0`. While the root `0x02E5BE10` is neither the head `0x02E5BDF8` nor 0, it erases that node with `0x0067FE20(head, node)` and calls `0x0016D6A0(node)`, an empty function, so nothing is freed there. Then it calls `0x006803D0(pool)` and `0x00680030(pool)` on the pool `0x02E5BE28` and `0x0067F580(head)` twice. | `0x001679A4`<br>`0x001679B0`<br>`0x001679B9`, `0x001679BF`<br>`0x001679D2`-`0x001679F5`<br>`0x02E5BE28`<br>`0x00167A1D`<br>`0x0067FFB8`-`0x0067FFDA`<br>`0x00808B90`<br>`0x00167A2E`<br>`0x008B6E14`-`0x008B6E1B`<br>`0x008B6E30`-`0x008B6E54`<br>`0x008B6E56`-`0x008B6E7B` |
| 2 | The renderer's start-up `0x006253D0` creates the integration object (`0x0065E5D0`, kept at `0x02D38540`) and marks it ready: `0x0065E580` (call at `0x0062549D`) sets its byte `+8` to 1. |   |
| 3 | The first frame that runs the pass calls `0x006CBD20` through `0x0065E5A0`; see the next section. |   |

### The integration object

`0x0065E5D0` allocates the 16-byte object once through `0x00210EC0` and builds it with `0x0065E530`, which
clears its record pointer and ready byte¹, allocates a `0x78`-byte record through
`0x00210EC0`² and fills it with `0x006CBAA0`³. When that allocation returns null, the record
pointer stays 0⁴. `0x0065E530` returns the object⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0065E549`, `0x0065E54C` |
| ² | `0x0065E553` |
| ³ | `0x0065E565` |
| ⁴ | `0x0065E560`, `0x0065E56D` |
| ⁵ | `0x0065E570` |

</details>

That constructor clears the context and shim pointers at `+0x00` and `+0x08`¹ and stores
nine fixed values: 1000.0 at `+0x10`, 1.0 at `+0x14`, 10.0 at `+0x18`, 1000.0 at `+0x1C`, 0.1 at `+0x20`, the
byte 1 at `+0x24`, 1.0 at `+0x68`, 10000.0 at `+0x6C` and 45.0 at `+0x70`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006CBAAD`, `0x006CBAA9` |
| ² | `0x006CBAA2`-`0x006CBAE1` |

</details>

The frame work `0x00193DA0` reaches the record only through one-line wrappers, each of which loads the
record pointer from the object's `+0x00` and jumps to the integration function:

| Wrapper | Target | Call in `0x00193DA0` |
|---|---|---|
| `0x0065E5B0` | no target: true when the record's context pointer is set | `0x00193DD1`, `0x00193DF5` |
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

| Step | What happens | Where in the code |
|---|---|---|
| 1 | Once (flag `0x01F31F70`), it installs `0x02E5BDE0` as the library's allocator and gives the library the licence text `0x00D86C00` (`0x006DAA50`, which copies it to `0x02EA0B58`). | `0x006DA8F0` |
| 2 | It creates the context (`0x006DA990`, a `0x18`-byte `PPFX::IPfxContext_Dx11`), through the jump `0x006DEF20`, and stores it at its first argument's `+0x00`. Only step 1 is behind the flag; this and the steps below run on every call. | `0x006CBD6D`, `0x006CBD72` |
| 3 | It builds a default parameter block and fills in four fields: 16/9 (1.777778, `0x008C5B38`) at `+0x20`, 0 at `+0x38`, the size `0x780` at `+0x48` and 2 at `+0x88`. | `0x006CBBC0`<br>`0x006CBDD7`-`0x006CBDF3` |
| 4 | It calls `0x006DAA70(context, record, 3, 5, 0x20001, parameters)`: the flags `0x20001` are the fifth argument, and `record` is three 8-byte words, the second argument's `+0x110` and two zeros. On failure (non-zero, `0x006CBE11`) it logs "Failed to initialize PPFX context." through the game's log `0x005CDAA0` at level 2 and carries on. | `0x006CBE0A`<br>`0x006CBD7C`-`0x006CBD8D` |
| 5 | It calls `0x006DB4C0(context, 0)` and `0x006DC5C0(context, 0, 5.0)`, then builds a `Yebis::PfxShimD3D11` object and hands it the context: `0x20` bytes from `0x00210EC0`, vtable `0x00D899A8`, 0 at `+0x10` and the context at `+0x18`, kept at the first argument's `+0x08`. | `0x009146E4`, `0x006CBE27`-`0x006CBE39`<br>`0x006CBE3E`-`0x006CBE73` |

When `0x00210EC0` returns null in step 5, the body stores 0 at the first argument's `+0x08` and writes the context to
address `0x18`, which faults¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006CBE53`, `0x006CBE69`-`0x006CBE73` |

</details>

`0x006DAA70` is `IPfxBaseContext::Initialize`. It runs the licence verifier once (flag `0x01F3BB28`) and
keeps the result at `0x02EA0B90`; with a negative result it returns that result and creates nothing.
Otherwise it allocates the `0xD40`-byte global block (constructor `0x006FF5D0`), stores it at
`0x02EA0B70` and runs `CPostEffect::Initialize`¹ on it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006FF900` |

</details>

`0x006DE950` is `ppfxInitialize()`, named by its log lines ("==== ppfxInitialize() ====", `0x00D8ED08`). No call, jump
or stored pointer in the image reaches it: the game starts the library through `0x006DAA70`. It has no licence step
and, unlike `0x006DAA70`, never keeps an existing block:

- it releases an existing global block (`0x006DEB40`, when `[0x02EA0B70]` is not null; `0x006DE9B2`-`0x006DE9BC`);
- it allocates the `0xD40`-byte block¹, constructs it², stores it at `0x02EA0B70` and runs
  `CPostEffect::Initialize`³ on it with its own five arguments⁴. A null
  allocation skips the constructor⁵, so 0 is stored and `0x006FF900` is given a null block, whose
  byte `+0x00` is the first thing it reads of the block⁶;
- on a negative result it logs the failure and returns 0⁷;
- otherwise it logs the GPU memory in use, the dword `+0x9F0` of the object at the block's `+0x20`, in bytes, KB
  and MB, and returns 1⁸.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006DA880` |
| ² | `0x006FF5D0` |
| ³ | `0x006FF900` |
| ⁴ | `0x006DE9C1`-`0x006DEA1F` |
| ⁵ | `0x006DE9EE` |
| ⁶ | `0x006FF9C3` |
| ⁷ | `0x006DEA28`-`0x006DEA67` |
| ⁸ | `0x006DEA6C`-`0x006DEB0F` |

</details>

`BeginPostEffectScene`¹ first calls slot `+0x1C0` of the object `+0x20` and keeps the answer².
It stores its second argument at `+0x598`, its fourth, a float, at `+0x59C` and its fifth at `+0x5A0`³. It makes the scene slot `+0x4C8` current at `+0x4D8`. A sixth argument of 0 or more stores 0
in `0x02EA1900`, calls `0x00722900(0x1F, 0, 0, 0, 0, 1.0, 0, 0, 0)`, keeps that answer in place of the first, and makes
`[+0x4CC]` plus that argument current⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0070B780` |
| ² | `0x0070B7B5` |
| ³ | `0x0070B7CB`-`0x0070B7E0` |
| ⁴ | `0x0070B805`-`0x0070B850` |

</details>

The current slot goes to `+0xA0` of the render buffer `+0x108`, and `0x0075BFC0(buffer, [+0x594], 0x7FFFFFFF)` runs¹. While the byte `+0x147` is clear it then calls
`0x0075CD90(buffer, the current slot, 1, the second argument, the third, the float, the fifth, 0, 0, flag)` and keeps
that answer; the flag is `0x30000` when bit `0x10000000` of the second argument is set, else `0x10000`². A float below 0 is passed there as 0 while the byte `+0xCCC` is set and as 1.0 otherwise³; `+0x59C` holds the float as it came.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0070B856`-`0x0070B87C` |
| ² | `0x0070B881`-`0x0070B913` |
| ³ | `0x0070B7C6`-`0x0070B7F8` |

</details>

With `+0x147` set it makes no such call. If the output target `+0x60` is then null it answers `0x80004005` and leaves
the byte `+0x00` as it was¹; when the levels `0x01F3BA80` and `0x01F3BA90` are both at least 1 it
first logs, through `0x006DF480`, a PPFX ERROR line, source line `0x2728`: "CPostEffect::BeginPostEffectScene(): At
least SetEffectSource() must be called if Initialize() was called with PFXINIT_RENDERSCENE_EXTERNAL flag."

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0070B895`-`0x0070B8D8` |

</details>

Otherwise it looks at the answer it kept last. A negative one is returned, after an ERROR line under the same two
levels, source line `0x273D`: "CPostEffect::BeginPostEffectScene(): m_pRenderBuffer->SetRenderTarget() failed (0x%x:
%s).", with the answer and the text `0x0071B3C0(answer)` gives for it. Any other answer sets the byte `+0x00` to 1 and
`BeginPostEffectScene` returns 0¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0070B915`-`0x0070B95B` |

</details>

`0x00708110` is `CPostEffect::SetMultisampleMode(mode)`. While the byte `+0x00` is set, which its message calls
being between `BeginPostEffectScene` and `EndPostEffectScene`, it logs and returns `0x80004005`¹. Otherwise it stores the mode at `+0x590`² and:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00708114`-`0x0070814D` |
| ² | `0x00708159` |

</details>

- with byte `+0x147` set it stores 0 at `+0x594` and returns 1¹;
- else it looks at the object at `+0x108`: whether its `+0x68` is not null, and whether either dword `+0xC0` or
  `+0xC4` of the object at its `+0x60` is not 0²;
- with `+0x68` null, mode 3 becomes mode 0 and mode 1 is refused: it logs "Cannot set multisample mode to
  PFXMSM_SINGLESAMPLE" and returns `0x80070057`³;
- with both dwords 0, mode 2 is refused the same way with "PFXMSM_MULTISAMPLE"⁴;
- a mode still 3 stores 1 at `+0x594` and at `+0xA4` of the `+0x108` object, mode 2 stores 0 at both and any
  other mode stores itself⁵. These paths return 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00708152`-`0x0070816E` |
| ² | `0x00708173`-`0x007081A6` |
| ³ | `0x007081AA`-`0x007081B4`, `0x007081F9`-`0x00708230` |
| ⁴ | `0x007081B6`-`0x007081F4` |
| ⁵ | `0x00708235`-`0x00708264` |

</details>

A refused mode has already been stored at `+0x590`. The game passes mode 0 both times: `0x006DB4C0`, which
`0x006CBD20` calls with 0¹, jumps here with the global block `[0x02EA0B70]`², and `CPostEffect::Initialize` calls it with 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006CBE25`-`0x006CBE27` |
| ² | `0x006DB4C0`-`0x006DB4C7` |
| ³ | `0x007051B2`-`0x007051B7` |

</details>

`CPostEffect::ApplyAmbientOcclusion`¹ takes a mode and one more value. It answers `0x80004005`
while the byte `+0x00` is set, and for a mode other than 2 and 3 while the pointer `+0x60` is null².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0070BB00` |
| ² | `0x0070BB0A`-`0x0070BB90` |

</details>

Each of the two refusals first logs an ERROR line through `0x006DF480` when the levels `0x01F3BA80`
and `0x01F3BA90` are both at least 1: source line `0x6D77`, "CPostEffect::ApplyAmbientOcclusion(): Cannot be
called while BeginPostEffectScene() and EndPostEffectScene().", or source line `0x6D84`,
"CPostEffect::ApplyAmbientOcclusion(): Call SetEffectSource() before call ApplyAmbientOcclusion()."¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0070BB12`-`0x0070BB3E`, `0x0070BB61`-`0x0070BB8B` |

</details>

Otherwise it calls `0x006FC160(object, its third argument)`, `0x006F3BE0(object)`, `0x007142F0()`, whose result it
keeps, and `0x00714560()`¹, and chooses what the pass draws from. For mode 1 and for every
mode not named here it is the pointer `+0x60`. Modes 2 and 3 pass null, and mode 3 also sets the pass's
fourth argument to 1².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0070BBC2`-`0x0070BBDE` |
| ² | `0x0070BBE5`-`0x0070BC01` |

</details>

Mode 0 also uses `+0x60` while the byte `+0x8E0` of the device `+0x20` is set. With that byte clear it first
calls `0x007422F0(kept result, pointer +0x60, texture, twelve constants)` with the texture of a work slot of
the render buffer `+0x108`, and then uses that slot's texture¹. The slot index is the
object's dword `+0x4D0`, and -1 stands for the buffer's current slot, its `+0xA0`; the texture is the slot's
entry in the buffer's list `+0x48`, or null when the slot is not below the buffer's count `+0x3C`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0070BC06`-`0x0070BCF3` |

</details>

The other twelve arguments of that `0x007422F0` call are constants: 0, the address of four floats of 1.0, a 0
dword, two 0 bytes, the floats 0 and 0, the dword 1, the floats 0 and 1.0, the address of two null qwords,
and 0¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0070BC17`-`0x0070BCC0` |

</details>

`ApplyAmbientOcclusion` then calls the pass `0x006F61F0(object, that source, [+0xD38], the mode-3 byte, 1)`¹ and `0x006FC200(object)`², and returns the latter's answer when negative, else 0³. It tests the answer of none of the six calls before `0x006FC200`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0070BD0D` |
| ² | `0x0070BD15` |
| ³ | `0x0070BD22`-`0x0070BD37` |

</details>

### Each frame

The frame routine `0x001F3300` returns at once while the byte `0x01DFE0C4` is 0¹. Otherwise, when the
context in its second argument has its bit `0x1` bracket open², it closes it with
`0x00600A60(ctx, 3)`³ and opens it again with `0x005FEFD0(ctx, 0)` before it returns⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001F3317` |
| ² | `0x00609710`, `0x001F3325` |
| ³ | `0x001F3339` |
| ⁴ | `0x001F3429` |

</details>

Then it calls `0x00194A30`¹, which applies a delayed `EnableYebis` change: it stores
`+0x1F0 - 1` only while `+0x1F0 > 0`, and copies `+0xA1` to `+0xA0` when that store leaves 0².
`0x00194A30` also runs a one-time setup: while the block's byte `+0x19B` is 0, when `0x001DC510()`
returns non-null and `0x001FDF70` returns 1 for that result, it calls `0x00193A00` and `0x00193A80` on the
block and sets `+0x19B`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001F3346` |
| ² | `0x00194A41`-`0x00194A55` |

</details>

`0x001DC510()` returns the `0x18`-byte object `[0x01F82D10]`, made once when `0x001DDAB0()` answers non-zero and null until
then, or when `0x00210EC0(0x18)` gives nothing¹. Its dwords `+0x00`, `+0x04` and
`+0x08` start at 0², with the defaults 1.0, 0.5 and 0.6 at `+0x0C`, `+0x10` and `+0x14`³; `0x001DC3D0(object)` then fills it and the pointer is stored⁴.
`0x001FDF70(object)` returns its first dword.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001DC51F`-`0x001DC54A`, `0x001DC582` |
| ² | `0x001DC54E`-`0x001DC551` |
| ³ | `0x001DC554`-`0x001DC562` |
| ⁴ | `0x001DC56C`-`0x001DC576` |

</details>

`0x001DC3D0` returns 0 on both paths¹; it stores nothing while `0x001DDAB0()` gives null². Otherwise, with h the value `0x002256A0(object)` returns for the object `0x001DDAB0()` gives³, it stores 0 at `+0x08`, h / 1080 at `+0x0C` and h / 1080 x 0.6 at `+0x14`, or 1.0 and 0.6
when h is not above 0, 0.5 at `+0x10` and 1 at `+0x00`⁴. It does not store the dword `+0x04`,
which the constructor left at 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001DC44A` |
| ² | `0x001DC3D9`-`0x001DC3E1` |
| ³ | `0x001DC3E3`-`0x001DC3EB` |
| ⁴ | `0x001DC3F8`-`0x001DC444` |

</details>

The setup copies its values into the block, each reader falling back to the default unless the first or second dword
is 1 (the last needs the first dword):

| Block field offset | Reader | Value | Clamp |
|---|---|---|---|
| `+0x19C` | `0x00193940` through `0x001DC460` | `+0x08`, else 0 | 0 to 3; a negative value gives 0 |
| `+0x1A0` | `0x00193A00` through `0x001DC4A0` | `+0x0C`, else 1.0 | at least 0 |
| `+0x1A4` | `0x001939A0` through `0x001DC480` | `+0x10`, else 0.5 | 0 to 1.0 |
| `+0x1EC` | `0x00193A80` through `0x001DC4C0` | `+0x14`, else 0.6 | at least 0 |

`0x00193A00` repeats the test itself, `0x001DC510()` not null and `0x001FDF70(object)` equal to 1, and stores nothing when
it fails¹. When it passes it calls `0x00193940(block)`², makes the same test once
more and, only when it holds again, stores `+0x1A0` from `0x001DC4A0(0x001DC510())`, at least 0³.
Either way it ends in a jump to `0x001939A0(block)`⁴, so that one call fills `+0x19C`, `+0x1A0` and
`+0x1A4`; `0x00193A80` fills `+0x1EC`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00193A09`-`0x00193A23` |
| ² | `0x00193A28` |
| ³ | `0x00193A2D`-`0x00193A5D` |
| ⁴ | `0x00193A6D` |

</details>

The frame routine then asks `0x0018E470`, which is true when the integration object is ready and the render
parameter block's byte `+0xA0` is set. Only then does it build the post-process command¹
whose work is `0x00193DA0`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0018EEE0` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | With no context yet, it creates one. When the command's byte `+0x99` is set, it calls `0x006CC2F0` instead, whether a context exists or not. `0x006CC2F0` releases a context through its slot `+0x08` and a shim through its slot 0 with 1, and clears each pointer, so step 2 then stops the frame's work. | `0x006CBD20`<br>`0x00193DB8`-`0x00193DC2`<br>`0x006CC2FF`-`0x006CC321` |
| 2 | With no context, it stops. |   |
| 3 | It passes two blocks of scene values. `0x006CC1F0` keeps the last first block: while its byte `+0x24` is 0 it calls `0x006DB900(target, kept block +0x28, 1)` and `0x006DB8C0(target, new block, 1)`, the target being `[[+0x08] + 0x18]`, and it always copies the new `0x40` bytes to `+0x28`-`+0x67` and stores 0 at `+0x24`. | `0x006CC1F0`, `0x006CC260`<br>`0x006CC1FA`-`0x006CC228`<br>`0x006CC22D`-`0x006CC24C` |
| 4 | Glare: with the Glare option on, `0x006CC1E0` hands the command's two glare values to `CPostEffect::SetGlareParameters`; with it off, 1.0 and 0.0. | `0x00707560` |
| 5 | `0x006CC170` passes a scale and mode: 2.0 and mode 2 when the command's byte `+0x98` is set; otherwise 1.0 with mode 1 when the byte `+0x9A` is set and mode -1 when it is clear. `0x006CC170` first asks `0x006DC4B0(target, -1)` for a float and calls `0x006DC820(target, that float, scale, mode, 32.0, -3.4028235e38)`. | `0x00193E7F`, `0x00193E87`<br>`0x00193E8F`-`0x00193EAE`<br>`0x006CC182`-`0x006CC193`<br>`0x006CC198`-`0x006CC1C5` |
| 6 | Depth of field: with the DepthofField option on, `0x006CC090` passes the enable byte, a 35 mm lens (divided by 1000) and the focus values; off, it passes the effect disabled.<br>• `0x006CC090` calls `0x006DBC20(target, enable)` and does the rest only while the byte is set.<br>• While enabled it first passes its auto-focus byte, its sixth argument, through `0x006DC600(target, 0, byte)`; with that byte set it calls `0x006DC760(target, 0, seventh, eighth)` and `0x006DC700(target, 0, 0.1, 100.0)`, and the float `0x006DC650(target, -1)` returns replaces the focus distance.<br>• Last it calls `0x006DBC60(target, focus distance, fourth argument, fifth argument / 1000)`. | `0x006CC0B8`<br>`0x006CC0BF`<br>`0x006CC0CB`-`0x006CC0D8`<br>`0x006CC0DF`<br>`0x006CC0E1`-`0x006CC131`<br>`0x006CC134`-`0x006CC150` |
| 7 | `0x006CBEA0` passes the three render targets the command holds and runs `CPostEffect::ApplyEffects` (`0x0070BA00`, through `0x006DB660`).<br>• In `0x006CBEA0` a target whose byte `+0x08` is set counts as null. The first target's texture and size (`+0x90`, `+0x94`) go to `0x0070D360` through `0x006DD5F0`, and the second's to `0x007116A0` through `0x006DD700`.<br>• `0x007116A0` sets the byte `+0x6FD` to 1 and looks its third argument, the texture, up in the map `+0xC8`. The object found there goes to `SetDepthFactorSource` as its texture: `0x007114F0(this, kind, texture, 0, parameter, float, float)`, the kind being `0x007116A0`'s second argument and the last three its seventh, eighth and ninth. `0x007116A0` returns that call's answer.<br>• With no object there, a texture for which the map `+0xB8` holds a non-null entry is passed on as no source at all, both pointers null. Any other texture is first made through `0x006F1F60(object, texture, the fourth, fifth and sixth arguments, two stack addresses)`; a negative answer of it is returned, and otherwise the pointer it left goes on as the texture.<br>• The third target's `+0x28`, or `+0x20` while its byte `+0x09` is set, goes to `0x0070D270` through `0x006DD570`. The shim's `+0x08` and `+0x10` both take the first target.<br>• After the run `0x006CBEA0` takes the context lock, calls the state reset `0x0061C2B0` on the device context at `+0x110` of the object `0x00624670` returns and releases the lock. It ignores the result of `ApplyEffects`. | `0x006CBECF`, `0x006CBF3B`, `0x006CBFCC`<br>`0x006CBF2E`<br>`0x006CBFC7`<br>`0x007116AC`-`0x0071170E`<br>`0x00711798`-`0x007117C9`<br>`0x00711714`-`0x00711758`<br>`0x0071175A`-`0x00711793`<br>`0x006CBFDA`-`0x006CC01A`<br>`0x006CBF37`, `0x006CC023`<br>`0x00615BC0`, `0x006CC03E`<br>`0x006CC04C`-`0x006CC058`<br>`0x00616700`, `0x006CC066` |

After building the command, `0x001F3300` compares its object's `+0x18` with the screen index `0x01F82EC0`¹. When they match and the device byte `+0xD48` of `0x00796E20()` is set, it calls
`0x00189530(manager, 0)` on the render manager `0x00189120()`². Otherwise it hands `0x001EE8E0` the
manager's targets from `0x001867C0`, `0x001867B0` and `0x00186660`³. Whether or not it built the
command, it then calls `0x00188730(manager)`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001F3351` |
| ² | `0x001F33A9` |
| ³ | `0x001F33C1`-`0x001F3408` |
| ⁴ | `0x001F3415` |

</details>

### The feedback pass

`0x006F6D80(effects, source)` is the feedback pass. It clears the byte `+0xD33` on entry, sets it to 1 at the end and
returns 0¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006F6DFA`, `0x006F72B8`-`0x006F72BA` |

</details>

It works with three textures. The target is the feedback tone-map texture `+0x1C0`; when that is null, it is a texture
of the view's feedback buffer `[+0x1B8]` (one per view, indexed by the view `+0x1F0`), at index `c & 1`, where `c` is
the view's dword in the array `+0x1E8`¹. The same pick gives the current feedback texture, and
the index `(c - 1) & 1` gives the previous one². An index not below the buffer's count `+0x3C`
gives a null texture, and so does a null `+0x1B8`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006F6DF0`-`0x006F6E53` |
| ² | `0x006F6E57`-`0x006F6EE4` |

</details>

It binds the target¹ and calls `0x00769FC0` with the source, the target's size (`+0x5C`,
`+0x60`) and these effect values²:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00722E80`, `0x006F6FF5` |
| ² | `0x006F6F41`-`0x006F7163` |

</details>

- the exposure ratio `+0x728 / +0x6D8`, or `+0x728 / (+0x728 * +0x6DC)` when the byte `+0x48C` is set;
- the ratio `+0x348 / +0x34C`;
- the floats `+0x998` to `+0x9A8`, with `+0x99C` and `+0x9A0` passed as 0 when the byte `+0x994` is 0;
- whether the byte `+0x55B` is 0;
- `+0x74C`, `+0x73C`, `+0x7A0` and `+0x110`.

It then takes the object `0x007142F0` returns and calls `0x00714560`. When the byte `+0x1C8` is 0, it binds the current
feedback texture¹. Last, it calls `0x00743B70` with that object, the previous texture, the
target, the current texture and two weights²:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006F7175`-`0x006F71CD` |
| ² | `0x006F72B3` |

</details>

```python
a = +0x978
b = +0x97C;  if b < 0:  b = 1 - a  # 0x006F71D2-0x006F71ED
if +0x980 > 0:  # 0x006F71F2-0x006F7230
    e = +0x6D4 / +0x980                              (the time step over the rate)
    a = powf(a, e)
    b = 1 - powf(1 - b, e)
```

Its other arguments are the block `+0x824` when the byte `+0x926` is set (else null), the block `+0x864` when the byte
`+0x927` is set (else null), and the float `+0x984`, or `+0x348` when `+0x984` is 0 or less¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006F7234`-`0x006F7268` |

</details>

Initialize sets `+0x978` to 0¹. The setter `0x0070B000(effects, a, b, rate)` sets `+0x978`, `+0x97C` and
`+0x980`²; it is reached only by the jump at `0x006DC7A7` in `0x006DC7A0`, which passes the global
block `[0x02EA0B70]` and which no call, jump or stored pointer in the executable names. So while `+0x978` keeps its 0,
`a` is 0 whenever `+0x980` is 0 or less or the time step `+0x6D4` is above 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00704BBB` |
| ² | `0x0070B002`-`0x0070B01B` |

</details>

`0x006F7330(effects, source)` does the first half of the pass on another target. It clears `+0xD33`, takes its target
from `0x0070B150(effects)`¹, binds it², and calls `0x00769FC0` with the source, that target's size
and the same effect values³. It then returns 0 with `+0xD33` set to 1⁴, with no
blend with an earlier frame.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006F7382` |
| ² | `0x006F743B` |
| ³ | `0x006F75FB` |
| ⁴ | `0x006F7600`-`0x006F7602` |

</details>

### The licence check

`0x006DFF40` refuses with "License text is not set." when no text was given. Otherwise it has `0x0071C550`
build a `0x20`-byte buffer from two constants of the image, the bytes at `0x00D8E9E8` with the string
`[0x01F3BB20]` names as the key (below), and checks the licence text with that buffer (`0x0071CD10`, which
calls `0x0071D9E0`). A failure is reported as status
1 "License is not valid.", 2 "License is expired." or anything else "Unexpected License Error.".

`0x0071CD10` builds a record on its stack that starts with the dwords 2000, 1, 1, 2000, 1, 1 and holds three empty
strings¹, stores 0 in the checker's qwords `+0x48` and `+0x50`, and calls
`0x0071D170(checker, record)` and then, only when that answers 0, `0x0071D9E0(checker, record)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0071CD3D`-`0x0071CD8B` |
| ² | `0x0071CD8F`-`0x0071CDB4` |

</details>

The first answer of the two that is not 0 is `0x0071CD10`'s own answer. When both answer 0 it copies the record's dwords
`+0x0C`, `+0x10` and `+0x14` to the checker's `+0x4C`, `+0x50` and `+0x54` and answers 0¹.
Either way it ends by calling `0x0071EF10(record)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0071CDB6`-`0x0071CDC8` |
| ² | `0x0071CDD4` |

</details>

After a first argument it does not read, `0x0071C550` takes an out pointer, an out length, a source, its
length, a key and the key's length¹. For a length of 0 it
returns with nothing written².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0071C55E`-`0x0071C575`, `0x0071C5D2`, `0x0071C66B` |
| ² | `0x0071C56C`-`0x0071C56F` |

</details>

Otherwise it asks `0x006DA880` for length + 9 bytes¹, stores length + 1
in the block's first qword² and the address 8 bytes in through the out pointer, null for a null
block³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0071C5A2` |
| ² | `0x0071C5B0` |
| ³ | `0x0071C5AC`-`0x0071C5BA` |

</details>

It zero-fills length + 1 bytes there, copies the source in¹ and stores the length
through the out length². With a key length other than 0 it XORs each byte with the next key
byte, starting the key again at its end³; with a key length of 0 it inverts every byte⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0071C5BF`, `0x0071C5CD` |
| ² | `0x0071C5DF` |
| ³ | `0x0071C660`-`0x0071C68C` |
| ⁴ | `0x0071C5E7`-`0x0071C65C` |

</details>

`0x006DFF40` passes the `0x20` bytes at `0x00D8E9E8` as the source and the 32-character string `[0x01F3BB20]`
names (`0x00D8E998` in the image) as the key, its length taken at `0x006DFFBF`-`0x006DFFC9`¹, so its buffer is those bytes XORed with that string, byte for byte. The licence
text, the pointer `0x02EA0B60`, is first read after that call².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006DFFB8`-`0x006DFFF1` |
| ² | `0x006E0064` |

</details>

"No text" means the dword `0x02EA0B58` is 0¹. Otherwise `0x006DFF40` hands `0x0071C550` the
string pointer `[0x01F3BB20]` and that string's length, with the address `0x00D8E9E8` and the value `0x20`
before them, and gets back a buffer pointer and a length². A null buffer is
logged as "License is not valid." as well³. Both refusals answer
`0x8000FFFF`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006DFF6C` |
| ² | `0x006DFFB8`-`0x006DFFF1` |
| ³ | `0x006DFFFA`-`0x006E0029` |
| ⁴ | `0x006DFFA4`, `0x006E002E` |

</details>

With a buffer it builds a reader from the buffer and the length¹
and a checker². It makes a temporary string of the text the pointer
`0x02EA0B60` names and hands it to `0x001A5500` with the checker's `+0x08`, then does the same for the
text the reader's `+0x08` names with the checker's `+0x28`³. The answer of
`0x0071CD10(checker)` is `0x006DFF40`'s own answer⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007158B0`, `0x006E0038`-`0x006E0044` |
| ² | `0x0071CB80`, `0x006E004E` |
| ³ | `0x006E0064`-`0x006E0105` |
| ⁴ | `0x006E0129`-`0x006E012E`, `0x006E0201` |

</details>

After the check the buffer is freed with `0x006DA8A0([0x01F3BA68], buffer - 8)`¹.
Only when the answer is not 0 is the status fetched, with `0x0071CCE0(checker)`².
Each of the five log lines is written only while the dwords `0x01F3BA80` and `0x01F3BA90` are both at
least 1³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006E0130`-`0x006E0144` |
| ² | `0x006E0149`-`0x006E0155` |
| ³ | `0x006DFF75`-`0x006DFF85`, `0x006DFFFF`-`0x006E000F`, `0x006E015F`-`0x006E0171`, `0x006E0192`-`0x006E01A2`, `0x006E01BE`-`0x006E01CE` |

</details>

The first argument of `0x0071C550` is the address of a stack slot¹, and the reader call is
`0x007158B0(reader, buffer, length, -1)` with the length as a dword². Each
temporary string is filled by `0x001A5630` and handed over as `0x001A5500(field, string, 0, -1)`; when
its capacity is `0x10` or more after that, it is released by `0x001DFA10`³. Before the body returns with the checker's answer it calls
`0x0071CC30(checker)` and `0x00715C70(reader)`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006DFFED` |
| ² | `0x006E0038`-`0x006E0044` |
| ³ | `0x006E008E`-`0x006E00BE`, `0x006E00F0`-`0x006E0120` |
| ⁴ | `0x006E01EE`-`0x006E01FC` |

</details>

`0x0071D9E0` checks the dates:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | The six date fields decoded from the signed part (begin and end year, month and day) must equal the plain-text fields one by one (`0x0071DC87` to `0x0071DCDB`); any difference sets status 1. | `0x0071E209` |
| 2 | When all six are 0 it jumps to success (`0x0071E0F4` to `0x0071E11A`, target `0x0071E216`). |   |
| 3 | Otherwise it builds begin at 00:00:00 and end at 23:59:59, converts both with `_mktime64`, reads `_time64` and sets status 2 when now is before begin or after end. | `0x0071E169`, `0x0071E1EB`<br>`0x0071E176`<br>`0x0071E1FF` |

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

Four places call it. The scene and map configuration loaders¹ read the
`EnableYebis` key as an integer, 1 meaning on, with no delay. The debug menu handler `0x001D1660`
calls it twice. The script command `0x05B0` (`0x00353420`, through `0x001EC4D0`) passes a value and a
delay from its two arguments.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001C3D50`, `0x001C7940` |

</details>

### The effect-source tokenizer

`0x00717760`, the code of `TFXString.cpp`, tokenizes effect source text: it skips `/*`, `*/` and `//`
comments¹ and calls `0x0071A230` to test for spaces, tabs and newlines. It calls itself
and is called only by `0x00719FB0`, whose only caller `0x0071A050` is neither called nor stored anywhere
in the image. The tokenizer is linked and never reached.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00717DEF` |

</details>

### The embedded effect archive

The library's compiled texture effects are a single block of `0xE8E9C2` bytes (15,264,194) in the
image, starting at `0x00E21F90`. It begins with text fields: `.tfxo file`, three decimal numbers, `hlsl`,
then the effect name `TexUtil_D3D11` and a newline-separated technique list that starts with
`tech_AlchemySsao_T1_S16`.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00000` | `char[16]` |  | value ".tfxo file" |
| `+0x00010` | `char[16]` |  | decimal: the block's size less `0x40` (`15264130`) |
| `+0x00020` | `char[16]` |  | decimal: the size of the text at `+0x40` (313026) |
| `+0x00030` | `char[8]` |  | decimal: the program count (2621) |
| `+0x00038` | `char[8]` |  | value "hlsl" |
| `+0x00040` | `text` |  | effect name; technique count; one line per technique: name, vertex shader, its program, pixel shader, its program; "GlobalParameter:"; parameter count; one line per parameter |
| `+0x4C702` | `record[]` |  | 256 bytes each, one per program: name, decimal offset, decimal size, NUL-separated |
| `+0xF0402` | `DXBC[]` |  | the programs end to end; each record's offset is from here |

| Table | Rows | One row per |
|---|---:|---|
| [`yebis-ppfx-post-effects-techniques.tsv`](yebis-ppfx-post-effects-techniques.tsv) | 2,624 | technique: `index`, `technique`, `vertex_shader`, `vertex_program`, `pixel_shader`, `pixel_program` |
| [`yebis-ppfx-post-effects-parameters.tsv`](yebis-ppfx-post-effects-parameters.tsv) | 35 | global parameter: `index`, `name`, and the two stored numbers `field_2` and `field_3` |
| [`yebis-ppfx-post-effects-programs.tsv`](yebis-ppfx-post-effects-programs.tsv) | 2,621 | program: `index`, `name`, `profile` (`vs_4_0` 37, `ps_4_0` 2,584), both offsets, `bytes`, `sha256`, and `same_bytes_as`, the earlier program with the same bytes (68 rows) |
| [`yebis-ppfx-post-effects-program-outputs.tsv`](yebis-ppfx-post-effects-program-outputs.tsv) | 6,243 | each written output of each distinct program: `program`, `profile`, `register`, `components`, `semantic`, `computed_from` (`c:cb0[n]` constant registers, `t:` textures, `v:` inputs), `decided_by`. `computed_from` is `-` when only literals reach the component. The listing holds no reflection data, so this table names registers and `semantic` is `-` in all 6,243 rows. The programs' own names are in their RDEF chunks (constants in 2,534 programs, resources in all 2,553; the two reflection tables below) and OSGN chunks (all 2,553: `SV_TARGET`, `TEXCOORD`, `SV_POSITION`) |
| [`yebis-ppfx-post-effects-program-samples.tsv`](yebis-ppfx-post-effects-program-samples.tsv) | 32,442 | every texture read: `program`, `line`, `instruction`, `texture`, `sampler`, `level`, `coordinate_from`, `decided_by`. 31,770 read by derivatives, 30,636 of them with a fixed texel offset, and 672 at an explicit level |
| [`yebis-ppfx-post-effects-program-conditions.tsv`](yebis-ppfx-post-effects-program-conditions.tsv) | 17 | every `discard`: `program`, `line`, `instruction`, `operand`, `decided_by`. The programs have no other branch |
| [`yebis-ppfx-post-effects-program-listing.tsv`](yebis-ppfx-post-effects-program-listing.tsv) | 249,452 | profile line, declaration or instruction of each of the 2,553 distinct programs: `program`, `line`, `text`, as `D3DDisassemble` of `d3dcompiler_47.dll` prints it, `container_byte`, the byte offset of the instruction's first word in the DXBC container; `token`, its index in the bytecode words, where word 0 is the version word; `dwords`, its length in 32-bit words; and `immediates`, the exact words of each `l(...)` operand as hexadecimal, operands apart by a space and `-` when it has none. `add r1.x, r1.x, l(0.000000)` in program 51 is the word `0x34800000` |
| [`yebis-ppfx-post-effects-reflection-variables.tsv`](yebis-ppfx-post-effects-reflection-variables.tsv) | 81,088 | constant of each program's reflection data, 2,534 programs: `program`, `buffer`, `slot`, `buffer_bytes`, `variable`, `offset`, `bytes`, `register`, `class`, `base`, `rows`, `columns`, `elements`, `stored_used`, `instructions`, `default_words` (hexadecimal) and `default_value`, or `none` for no stored default |
| [`yebis-ppfx-post-effects-reflection-resources.tsv`](yebis-ppfx-post-effects-reflection-resources.tsv) | 7,590 | bound resource of each program: `program`, `name`, `kind`, `return`, `dimension`, `samples`, `slot`, `count`, `flags`, `instructions` (those naming any slot from `slot` to `slot + count - 1`) |
| [`yebis-ppfx-post-effects-parameter-handles.tsv`](yebis-ppfx-post-effects-parameter-handles.tsv) | 35 | global parameter: `parameter`, `handle_field` (its place in the effect set), `looked_up_at`, `stored_at`, `setter_calls` |
| [`yebis-ppfx-post-effects-parameter-setter-calls.tsv`](yebis-ppfx-post-effects-parameter-setter-calls.tsv) | 260 | call or tail jump that sets a parameter on the effect: `parameter`, `slot` of `IGPUEffect`, `slot_function`, `site`, `function`, and for a staged upload its `staging_buffer` and `vector_count` |

A technique's two program numbers are the positions of `TexUtil_D3D11\<shader>.vso` and `.pso` in the records,
in all 2,624.
These tables give what the block stores. Which technique a frame runs is the library's choice at run time.

A variable's `register` follows from its byte offset: `fParam_ScreenSpaceScale` at byte 80, eight bytes, is
`cb0[5].xy`. Every program was compiled by `Microsoft (R) HLSL Shader Compiler 9.29.952.3111`, and `$Globals` is
4,096 bytes in each of the 2,534 that have it. Three things are kept apart:

- `default_words` is what the program's container stores: for `fParam_ScreenSpaceScale`, `0x3F800000,0xBF800000`,
  which are (1, -1).
- `stored_used` is the compiler's own flag, and `instructions` counts the program's instructions that read a
  register and component the variable occupies. The two agree on all 81,088 rows: 9,840 are used and 71,248 are not.
- What the game writes at run time is neither of those. It is whatever the setter calls below pass.

`0x0072A320` looks up 34 of the 35 parameters by name through slot `+0x48`. 31 are single handles stored in the effect
set¹. Each setter then takes the handle back from that field, which ties the name to the
call. All 67 rows of [the constant uploads](yebis-ppfx-post-effects-constant-uploads.tsv) join to a parameter this
way.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0072A4CB`-`0x0072A7C5` |

</details>

The three sampler arrays go through `0x0072EC00`, which looks up one name per index and stores each handle in the next
4-byte field¹: `asamp2D_Texture` 16 from `+0x10`, `asamp3D_Texture` 16 from `+0x50`,
`asamp2D_VertexTexture` 4 from `+0x90`. `asamp2D_Texture[0]` and `[1]` are also stored at `+0x08` and `+0x0C`². Slot `+0xB8` binds textures with handles from these fields, in 107 calls.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0072ED75`, `0x0072ED78` |
| ² | `0x0072D10F`, `0x0072D124` |

</details>

`m44_ModelViewProject` is the one with no lookup, and no program reads it: `stored_used` is 0 in all 2,534.
`Database/Tools/catalogues/yebis_handles.py` and `dxbc_tokens.py` write these tables.

`Database/Tools/catalogues/yebis_effects.py` writes them.

`0x0078A530` copies the whole block into a `malloc` buffer in eight runs of `0x1D1D40` bytes (sources
`0x00E21F90` to `0x01ADEC50`, the last run shorter) and returns it. Its only caller is
`TEXSHADERSET::CreateEffect()` (`0x0072A320`, named by its log lines), which on its first call
(`+0x00` still null) hands the copy, its size and the name `_LUMINANCE_REMAP_S1.pso` to `0x0078A120`,
frees the copy, and then looks up the effect's parameter handles by name (`fParam_FocusDistance`,
`afRGBA_Modulate`, `fParam_GammaCorrection` and others).

### Bodies outside the member lists

Eight of the bodies below are in neither member list; the ninth, `0x00789D50`, is in the function list and no
instruction calls it directly. Each of the eight is called only from inside the span
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
    `k` 1 in mode 0, else 0.5¹. In mode 0 with a positive last argument `e` and one tap on both axes it
    uses two per axis, at `±e / R`.
  - The vectors take both axes in steps of `max(twelfth argument, 1)`, and the count is returned
   ².
- `0x00740BE0` clamps a sample count to 4 to 8, selects the shader for it, uploads constants through
  slot `+0x98` of the `PPFX::IGPUEffect` at `+0x38` (vtable `0x00DAF1B8`) and binds textures through its slot `+0xB8`.
- `0x0078AD20`, the code of `TinyEffect.cpp`, reflects a shader with `D3DReflect` and allocates its
  `0xC0`-byte variable records through `0x006DA880`.
- `0x0077FFE0` returns 0 and does nothing else when the float `+0x7C` is 0 or above³. Otherwise
  it maps a GPU resource, the `+0x38` of the object at `+0x98`, through slot `+0x70` of the object at
  `[+0x28] + 0x38`, which takes Map's arguments (the resource, subresource 0, type 1, and flag `0x100000`,
  do-not-wait, when `+0x68` is 2; `0x00780002`-`0x00780040`).
- When that map answers a negative value, `0x0077FFE0` returns it and stores nothing⁴. Otherwise
  the first four bytes it gave go to `+0xA2`, `+0xA1`, `+0xA0` and `+0xA3`, in that order⁵;
  `0x0077FFE0` then unmaps the resource (slot `+0x78`, `0x00780095`), calls `0x007804C0(object)`⁶ and returns
  the map's answer.
- `0x00788430` is `IGPUBuffer::Unmap`. With the mapped byte `+0xC4` clear it only logs "IGPUBuffer::Unmap(): Buffer
  is not mapped." as a PPFX ERROR line of `GPUInterfaceBuffer.cpp`, line 1001, when the two log levels
  `0x01F3BA80` and `0x01F3BA90` are 1 or more⁷.
- With the byte set, `0x00788430` calls slot `+0x78` of the device context at `+0x30` of the object `+0x18`, with
  the buffer the pointer array `+0xB8` holds at index `+0xC0` and subresource 0, and clears the byte
 ⁸. A null `+0x18` skips the `+0x30` load⁹, and the vtable
  pointer is then read from address 0¹⁰.
- `0x00735E40` stages up to eight float vectors at `0x02EA1C50` and uploads them through slots
  `+0xD0` and `+0x98` of the same effect at `+0x38`¹¹. `0x00789E40` is a jump to slot `+0x88` of
  the object at the effect's `+0xE0`¹². `0x0074F740` runs `0x00735E40` twice
 ¹³.
- `0x00789D50` counts the upload¹⁴ and forwards it through slot `+0x58` of the `PPFX::CTinyEffect` at the effect's `+0xE0`
 ¹⁵; the GPU device's own slots `+0x98` and `+0xD0` (vtable `0x00D9EA30`: `0x00724EA0`, `0x00725090`) only
  return `0x80004001`.
- `0x007850C0` stores the low byte of its second argument in the buffer `+0x30` at the index its third argument gives.
  For a negative index it uses `d % max([0x02EA1970], 1)`, both unsigned, where `d` is the dword `+0x28` of the object
  at `+0x18`¹⁶.
- `0x00741680` runs `0x00740BE0` three times¹⁷.
- `0x007651F0` returns 0 unless its source at `+0x260` is set and three of its intensities are
  positive; otherwise it builds its pass constants from them.
- `0x0070E1B0` is `CPostEffect::ApplyStaticSceneEffects`, named by its two messages; it takes a dword that selects the
  depth conversion, two floats, a byte and one more value. It answers `0x80004005` while the byte `+0x00` is set
 ¹⁸.
- Otherwise `0x0070E1B0` calls `BeginPostEffectScene` as `0x0070B780(object, 0, 0, lowest float, 0, -1)`
 ¹⁹, then `0x007142F0()`, whose result it keeps, `0x00714560()` and
  `0x00731E80(that result, 0x10, 1, 2)`²⁰.
- Unless the depth-factor kind `+0x470` is 3, `0x0070E1B0` then answers `0x80004005` again, with no call that undoes
  what `BeginPostEffectScene` did²¹.
- Each of those two refusals first logs an ERROR line through `0x006DF480` when the levels `0x01F3BA80` and `0x01F3BA90` are
  both at least 1: source line `0x79A9`, "CPostEffect::ApplyStaticSceneEffects(): Cannot be called while
  BeginPostEffectScene() and EndPostEffectScene().", or source line `0x79C0`, "CPostEffect::ApplyStaticSceneEffects():
  If ApplyStaticSceneEffects() is called, SetDepthFactorSource() must be PFXDFSRC_A."
- The two ERROR lines are logged at `0x0070E1D7`-`0x0070E201` and `0x0070E265`-`0x0070E28F`.
- With kind 3 it takes a depth conversion: the constants 1.0, 0, 1.0, 0 when the selecting dword is 7, else what
  `0x00708D10(object, block, that dword, 0, its two floats)` writes²². It runs the update
  `0x006FC760(object)` while the byte `+0x6FD` is set (`0x0070E2ED`-`0x0070E2F9`, and again at `0x0070E352`-`0x0070E367`).
- It calls slot `+0x88` of the object `+0x50`, keeps the dword answered and calls that object's slot `+0x78` with 1
 ²³; after the draw it calls slot `+0x78` again with the kept dword²⁴. It
  does not test `+0x50` for null.
- The draw is `0x007407E0(kept result, the values below)`²⁵; in order they are: 0, 0, the dwords `+0x5C` and
  `+0x60` of the scene slot's texture as floats, 0, 0, 1.0, 1.0, the object `+0x50`, two bytes of 1, the near and far
  distances `+0x5A4` and `+0x5A8`, the reference distance `+0xCF8`, the float `+0x6D8`, a float `m`, the conversion
  block, a copy of the 16 bytes at `+0xCE8`, and 0²⁶.
- `m` is `+0x6D8` while the byte `+0x48E` is set and the byte argument is 0, else 1.0²⁷. The
  scene slot is `+0x4C8`, or the current slot `+0xA0` of the render buffer `+0x108` for -1; its texture is the slot's
  entry in the buffer's list `+0x48`, taken as null, and still read, when the slot is not below the count `+0x3C`
 ²⁸.
- `0x0070E1B0` ends with `0x006FB810(object, its sixth argument, 0)`²⁹. A negative answer is returned, after an
  ERROR line under the same two levels, source line `0x5D29`: "CPostEffect::EndPostEffectScene():
  EndPostEffectScene_Process() failed (0x%x: %s).", with the answer and the text `0x0071B3C0(answer)` gives for it. Any
  other answer gives 0³⁰.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006E9A90` |
| ² | `0x006E9C20`-`0x006EA05B` |
| ³ | `0x0077FFE6`-`0x0077FFF6` |
| ⁴ | `0x00780046`-`0x00780048` |
| ⁵ | `0x00780052`-`0x00780079` |
| ⁶ | `0x0078009B` |
| ⁷ | `0x00788436`-`0x00788471` |
| ⁸ | `0x00788476`-`0x007884A0` |
| ⁹ | `0x0078848B`-`0x0078848E` |
| ¹⁰ | `0x00788494` |
| ¹¹ | `0x00789E40`, `0x00789D50` |
| ¹² | `0x00789E40`-`0x00789E4A` |
| ¹³ | `0x0074FDD9`, `0x007502CD` |
| ¹⁴ | `0x02EA40B8`, `0x02EA40BC` |
| ¹⁵ | `0x0078FCF0` |
| ¹⁶ | `0x007850C7`-`0x00785105` |
| ¹⁷ | `0x00741B5C`, `0x00741D2A`, `0x00741F18` |
| ¹⁸ | `0x0070E1BF`-`0x0070E20B` |
| ¹⁹ | `0x0070E210`-`0x0070E235` |
| ²⁰ | `0x0070E23A`-`0x0070E257` |
| ²¹ | `0x0070E25C`-`0x0070E299` |
| ²² | `0x0070E29E`-`0x0070E2E5` |
| ²³ | `0x0070E333`-`0x0070E34E` |
| ²⁴ | `0x0070E47C`-`0x0070E485` |
| ²⁵ | `0x0070E477` |
| ²⁶ | `0x0070E3D0`-`0x0070E474` |
| ²⁷ | `0x0070E2FE`-`0x0070E32B` |
| ²⁸ | `0x0070E36C`-`0x0070E3CD` |
| ²⁹ | `0x0070E495` |
| ³⁰ | `0x0070E4A5`-`0x0070E4E8` |

</details>

### Reading the luminance back

`0x00780590(object, flag)` is `CTextureUtil::GetResult_UpdateInternalLuminance`, the name its own warning gives
(`0x00DAC250`, logged with the file `..\src\GPU\GPUTextureLuminance.cpp`). It is one of the three callers of `0x0077FFE0`
([above](#bodies-outside-the-member-lists)). It returns 0 and does nothing else when the float `+0x7C` is 0 or above¹. Otherwise the mode `+0x68` picks what runs before `0x007804C0(object)`², and it
returns 0:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007805A7`-`0x007805B9` |
| ² | `0x0078073A` |

</details>

- Mode 2 calls `0x0077FFE0(object)` until it answers 0, after one "CPU may be blocked." warning (line `0x589`) when the
  log levels `0x01F3BA80` and `0x01F3BA8C` are 1 or more¹.
- Mode 5 runs the same loop and gives the warning (line `0x626`, under the same log levels) only before the second
  call².
- Modes 3 and 4 ask each of the `+0x44` objects in the pointer array `+0x48` for a value through its slot `+0x58`,
  with the flag as the third argument, and cap each answer at `0xFF`, a negative answer kept³.
- Mode 4 then stores four bytes: with three or more objects, `+0xA2`, `+0xA1`, `+0xA0` and `+0xA3` take answers 0, 1,
  2 and 3; with fewer, `+0xA0`, `+0xA1` and `+0xA2` take answer 0 and `+0xA3` takes answer 1⁴.
  Mode 3 stores none of them.
- Mode 1 and any other mode go straight to `0x007804C0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007805D5`-`0x0078060E` |
| ² | `0x0078062E`-`0x0078066E` |
| ³ | `0x00780675`-`0x007806D9` |
| ⁴ | `0x007806EF`-`0x00780729` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

The library's global block, `CPostEffect`, is `0xD40` bytes at `[0x02EA0B70]`: the constructor `0x006FF5D0` clears it and `CPostEffect::Initialize`¹ builds its members and stores the parameter defaults by calling the library's own setters. The member names are the allocation names Initialize passes to `0x006DA880`; the init flags are the word `0x20001` the game passes².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006FF900` |
| ² | `0x006CBE02` |

</details>

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
| `+0x050` | `void*` | ptr050 | no instruction stores a pointer here: the constructor clears it (`0x006FF616`) and Uninitialize releases and clears it (`0x00705A68`-`0x00705A77`); ApplyStaticSceneEffects `0x0070E1B0` calls its slots `+0x88` and `+0x78` without a null test (`0x0070E333`-`0x0070E34E`, `0x0070E485`) |
| `+0x058` | `void*` | depthFactorSource | the depth-factor source texture SetDepthFactorSource stores (`0x00711588`, `0x00711615`); the passes test it with `+0x468` before using the depth-factor path (`0x006F91A2`, `0x006F8073`) |
| `+0x060` | `void*` | outputTarget | the output target `0x0070D340` and `0x0070D360` set (`0x0070D340`, `0x0070D3ED`); ApplyEffects requires it while the byte `+0x147` is set (`0x0070BA53`, `0x0070BA5C`); EndPostEffectScene_Process swaps in its own target for the alpha pass and restores it (`0x006FBB20`, `0x006FBD89`) |
| `+0x068` | `u32` | outputKind | the kind stored with `+0x60` (`0x0070D346`, `0x0070D3E8`); 1 during the alpha pass (`0x006FBB2B`); with 1 the internal process takes format code `0x15` (`0x006F9219`-`0x006F9222`) |
| `+0x070` | `void*` | auxSource | the texture `0x0070DD30` stores (`0x0070DD30`); passed with `+0x7C`, `+0x80`, `+0x84` and `+0x88` by `0x006F35B0` (`0x006F3660`-`0x006F3674`) and EndPostEffectScene_InternalProcess (`0x006F94AA`-`0x006F94BE`); Initialize clears it (`0x00704C3F`) |
| `+0x078` | `u8` | auxFlag | cleared by Initialize (`0x00704C3B`) and written by nothing else; UpdateParameters_Base tests it (`0x006F78A9`) |
| `+0x07C` | `u32` | auxValue | 0 from Initialize (`0x00704C43`), written by nothing else; passed with `+0x70` (`0x006F3664`, `0x006F94AE`) |
| `+0x088` | `f32` | auxScale | 0 from Initialize (`0x00704C52`), written by nothing else; passed with `+0x70` (`0x006F3674`, `0x006F94BE`) |
| `+0x090` | `void*` | glareModulatorSource | the source texture of SetGlareModulatorSource (`0x0070D414`-`0x0070D479`): its third argument for a non-zero kind while the byte `+0x143` is set, cleared for kind 0 and for a non-zero kind while `+0x143` is 0 |
| `+0x098` | `u32` | glareModulatorKind | the source kind of SetGlareModulatorSource (`0x0070D40E`, `0x0070D461`): a kind above 5 answers `0x80070057` with nothing stored, after the ERROR line when the levels `0x01F3BA80` and `0x01F3BA90` are both at least 1 (`0x0070D409`-`0x0070D40C`, `0x0070D488`-`0x0070D4B7`); a non-zero kind while `+0x143` is 0 is stored as 0 with the answer 1, after the WARNING line (line `0x7A9B`) when `0x01F3BA80` and `0x01F3BA8C` are both at least 1 (`0x0070D427`-`0x0070D46E`); every other call answers 0; with a kind and no source texture the internal process uses m_pGlareModulatorWork (`+0x128`) instead (`0x006F9174`-`0x006F9185`, `0x006F9260`) |
| `+0x0A0` | `void*` | glareModulatorTexture | the glare-modulator texture of the current frame: EndPostEffectScene_InternalProcess sets it (`0x006F9304`-`0x006F9548`) and UpdateParameters_Base clears it (`0x006F825F`) |
| `+0x0A8` | `void*` | mapA | the header of the map built by `0x00714800` (`0x006FF643`-`0x006FF648`), keyed by texture: `0x0070D270` looks a source texture up in it for its view (`0x0070D276`-`0x0070D2BE`) and on a miss calls `0x006F1E00`(this, texture, its third to seventh arguments, &view), returning a negative answer with nothing stored (`0x0070D2C7`-`0x0070D2FB`); `0x006FF840` walks it at shutdown (`0x006FF8B7`) |
| `+0x0B0` | `u64` | mapASize | the second word of the `+0xA8` map, cleared by the constructor (`0x006FF63C`) |
| `+0x0B8` | `void*` | mapB | the header of the map built by `0x007147A0` (`0x006FF661`-`0x006FF666`); walked by `0x006FF840` (`0x006FF88B`) |
| `+0x0C0` | `u64` | mapBSize | the second word of the `+0xB8` map, cleared by the constructor (`0x006FF65A`) |
| `+0x0C8` | `void*` | mapC | the header of the map built by `0x00714740` (`0x006FF67F`-`0x006FF684`); walked by `0x006FF840` (`0x006FF85F`) |
| `+0x0D0` | `u64` | mapCSize | the second word of the `+0xC8` map, cleared by the constructor (`0x006FF678`) |
| `+0x0D8` | `void*` | effectSourceView | the effect source as a view, set by `0x0070D270` (`0x0070D325`); `0x006FD070` uses it first (`0x006FD076`-`0x006FD085`); cleared by `0x0070D240` (`0x0070D249`) |
| `+0x0E0` | `void*` | effectSourceTexture | the effect source as a texture; `0x006FD070` asks it for a view through its vtable `+0xA0` when `+0xD8` is null (`0x006FD094`-`0x006FD0BF`): a negative answer is returned as it is (`0x006FD0B7`), otherwise the view the call wrote stays in `+0xD38` and `0x006FD070` calls slot `+0x08` of that view (`0x006FD0B9`-`0x006FD0BF`) and returns 0; cleared by `0x0070D240` and `0x0070D270` |
| `+0x0E8` | `void*` | effectSourceBuffer | the effect source as a render buffer, set by `0x0070D240` (`0x0070D242`); `0x006FD070` takes its current texture when `+0xD8` and `+0xE0` are null (`0x006FD0CA`-`0x006FD0E8`); cleared by `0x0070D270` (`0x0070D30F`) |
| `+0x0F0` | `void*` | ptr0F0 | cleared by the constructor (`0x006FF687`) and Initialize (`0x00704C34`), stored by `0x0070DC90` (`0x0070DD14`); read by UpdateParameters_Base (`0x006F786A`) and the internal process (`0x006FB3E1`) |
| `+0x0F8` | `u8` | initBit31 | 1 when init flag `0x80000000` was given (`+0x145`, `0x00704C24`-`0x00704C2E`); UpdateParameters_Base tests it (`0x006F7861`) |
| `+0x100` | `u64` | qword100 | cleared by Initialize (`0x00704D60`); read by no instruction |
| `+0x108` | `void*` | renderBuffer | m_pRenderBuffer, the `0xA8`-byte render buffer Initialize allocates under that name (`0x00700977`-`0x007009BB`, constructor `0x0075B710`); its texture array (`+0x48`, current index `+0xA0`) holds the slots the `+0x4C8`.. indices name |
| `+0x110` | `void*` | renderGlare | m_pRenderGlare, the `0x310`-byte glare object (`0x007009C2`-`0x00700A06`, constructor `0x007687E0`); its Initialize, GenerateGlare and TonemapToSurface run from `0x00702223` and the internal process (`0x006FB14E`, `0x006FB6F6`) |
| `+0x118` | `void*` | depthOfField | m_pDepthOfField, the `0x4C0`-byte depth-of-field object (`0x00700AB5`-`0x00700AF9`, constructor `0x007790E0`); ApplyEffects_DepthOfField runs it (`0x006F60A1`). While `+0x130` is set, `0x00711820` stores its float argument at `+0x184` and its third argument, a dword, at `+0x188` of it and returns 0 (`0x0071182F`-`0x0071184E`); while `+0x130` is 0 it stores nothing and returns 1 (`0x00711820`-`0x0071182E`) |
| `+0x120` | `void*` | effectColorAlphaDestinationWork | m_pEffectColorAlphaDestinationWork, a `0xA8`-byte render buffer made when `+0x146` is set (`0x00700A61`-`0x00700AAE`); for the alpha output EndPostEffectScene_Process takes its current texture as the effect source (`0x006FB9B5`-`0x006FB9D5`) |
| `+0x128` | `void*` | glareModulatorWork | m_pGlareModulatorWork, a `0xA8`-byte render buffer made when `+0x143` is set (`0x00700A0D`-`0x00700A5A`); the glare-modulator step uses it (`0x006F9260`) |
| `+0x130` | `u8` | dofBuilt | 1 when the depth-of-field quality argument of Initialize is not negative (`0x007004C3`-`0x007004CA`). Without it `0x00711820` stores nothing and returns 1 (`0x00711829`), `0x007111C0` skips only its store at `+0x250` of m_pDepthOfField (`0x007111D1`-`0x007111DA`), and `0x00708710` stores a 0 enable (`0x00708720`) |
| `+0x133` | `u8` | airyDiscBuilt | aperture Airy disc: 1 with init flag `0x40000` (`0x006FFFB9`-`0x006FFFD3`); SetApertureAiryDiscEnable refuses while it is 0 (`0x0070A066`) |
| `+0x136` | `u8` | temporalAntialiasBuilt | temporal anti-alias: 1 with init flag `0x100000` when the device's `+0x8EB` is 0 (`0x00700283`-`0x007002AA`); Initialize then makes the history buffers (`0x007017E6`); while it is 0 SetTemporalAntialiasEnable (`0x0070AB80`) stores 0 at `+0xC24` and returns 1, for a non-zero enable after the WARNING line when the levels `0x01F3BA80` and `0x01F3BA8C` are both at least 1 (`0x0070AB86`-`0x0070ABCC`) |
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
| `+0x198` | `void*` | taaWeightA | temporal anti-alias: a per-view float array made with the history buffers (`0x00701847`-`0x0070187E`); `0x0070E7A0` resets an entry to 1.0 (`0x0070E7F5`-`0x0070E7FC`): the view its second argument names, -1 meaning the active view `+0x1F0`, and every view only for `0x7FFFFFFF` (`0x0070E7C0`-`0x0070E7F3`, `0x0070E832`-`0x0070E843`); it answers 1 with nothing done while `+0x136` is 0 (`0x0070E7A4`-`0x0070E7B7`), else 0; read by the temporal anti-alias pass (`0x006F68A0`) |
| `+0x1A0` | `void*` | taaWeightB | temporal anti-alias: a second per-view float array (`0x00701885`-`0x007018BC`); `0x0070E7A0` resets the same entry to 1.0 (`0x0070E803`-`0x0070E80A`); read by `0x006F65A0` |
| `+0x1A8` | `void*` | taaLuminanceScale | temporal anti-alias: a per-view float array (`0x007018C3`-`0x007018FA`); `0x0070E7A0` resets the same entry to the scene luminance scale `+0x6D8` (`0x0070E811`-`0x0070E81F`); read by `0x006F65A0` |
| `+0x1B0` | `void*` | taaPerView16 | temporal anti-alias: a per-view array of 16-byte entries (`0x00701901`-`0x0070195E`); `0x0070E7A0` clears the same entry (`0x0070E822`-`0x0070E82D`); read by `0x006F65A0` |
| `+0x1B8` | `void*` | feedbackBuffers | m_ppFeedbackBuffer, one `0xA8`-byte render buffer per effect view, made when `+0x13E` is set (`0x0070347D`-`0x007035E7`); read by `0x006F6D80` and `0x0070B150` |
| `+0x1C0` | `void*` | feedbackTonemapTexture | m_pFeedbackTonemapTexture, allocated from the texture pool (`0x0075E2D0`, which calls `0x0075E330`(this, 1, its second to eighth arguments), `0x0075E2D4`-`0x0075E311`) when `+0x1C8` and the device's `+0x8E0` are 0 (`0x00703706`-`0x00703733`); read by `0x006F6D80` (`0x006F6DF0`) |
| `+0x1D0` | `void*` | tonemapConvolutionTexture | m_pTonemapConvolutionTexture, allocated from the texture pool when `+0x13F` is set and `+0x13E` is not (`0x00703809`-`0x00703855`); read by `0x0070B150` (`0x0070B22A`) |
| `+0x1D8` | `u32` | textureCount1D8 | Initialize counts textures into it and then stores 0 (`0x0070389B`-`0x00703916`), so it is always 0; Uninitialize reads it as the count for `+0x1E0` (`0x0070612A`) |
| `+0x1E0` | `void*` | textureArray1E0 | cleared by the constructor (`0x006FF728`) and only released by Uninitialize (`0x0070606F`-`0x00706158`); nothing stores a pointer here |
| `+0x1E8` | `void*` | viewFrameCounts | a per-view dword array (`0x00700DAF`-`0x00700DE9`); EndPostEffectScene_PreProcess increments the active view's entry each frame (`0x006F87A6`-`0x006F87AD`) |
| `+0x1F0` | `i32` | activeView | the active effect view, set by SetActiveView (`0x007067B5`, 0 to m_nEffectViews); -1 in a per-view call means this view. The setter `0x00706760` answers `0x80004005` while the byte `+0x00` is set, after the ERROR line when the levels `0x01F3BA80` and `0x01F3BA90` are both at least 1 (`0x00706764`-`0x00706798`), and `0x80070057` for a view below 0 or above `+0x328` (`0x007067A2`-`0x007067CD`); it also stores the view at `+0x20C` of m_pRenderGlare (`+0x110`) when that pointer is not null (`0x007067AE`-`0x007067C0`) and returns 0 |
| `+0x1F8` | `void*` | autoExposureParams | m_pAutoExposureParam, one `0x68`-byte record per effect view (`0x00700B5A`-`0x00700BBF`); its `+0x60` holds m_pQuerySceneLuminance (`0x00700CAC`) and its `+0x58` the exposure the game reads (`0x006DC4B0`) |
| `+0x200` | `void*` | autoFocusParams | m_pAutoFocusParam, one `0x48`-byte record per effect view (`0x00700BC6`-`0x00700C04`); its `+0x40` holds m_pQuerySceneDepth (`0x00700D63`) and its `+0x38` the focused distance the game reads (`0x006DC650`) ; `0x0070F200`(object, view, byte, float, float) first stores 1.0 in the object's dword `+0xC60` (`0x0070F252`), then writes the record's `+0x20` (its first float, below 0 as 0 and above 1.0 as 1.0, `0x0070F20D`-`0x0070F226`), its float `+0x28` (fifth argument, 0 unless above 0, `0x0070F229`-`0x0070F234`) and byte `+0x24` (the low byte of its byte argument) (`0x0070F2C1`-`0x0070F2D1`): for the view named when it is 0 or more and below the signed count `+0x328` (any other view gets no write and the answer 0), for the view of field `+0x1F0` when -1 is named, and for every view below the signed count `+0x328` when `0x7FFFFFFF` is named (`0x0070F25C`-`0x0070F29C`, `0x0070F2D6`-`0x0070F2E0`) ; it answers 1 when a record it wrote has a null `+0x40`, else 0 (`0x0070F2BB`-`0x0070F2C7`, `0x0070F2EC`). The tests at `0x0070F237`-`0x0070F24C` end in the answer `0x80070057` (`0x0070F2F1`) and are not true after the two clamps |
| `+0x208` | `u32` | initFlags | the init flag word as given to Initialize (`0x006FFB86`), before the adjustments made to the copy at `+0x20C` |
| `+0x330` | `u32[2]` | descCopy08 | descriptor copy `+0x08` and `+0x0C` (see PpfxInitDescriptor): the copy at `+0x328` that Initialize takes of `+0x210` (`0x006FFB0B`-`0x006FFB7C`) and adjusts |
| `+0x338` | `u32[2]` | descCopy10 | descriptor copy `+0x10` and `+0x14`, the render width and height overrides |
| `+0x340` | `u32[2]` | descCopy18 | descriptor copy `+0x18` and `+0x1C`, the render-scene width and height overrides |
| `+0x358` | `u8` | descCopy30 | descriptor copy `+0x30`; read at `0x0070256E` for the depth-of-field buffer scale |
| `+0x35C` | `i32` | descCopy34 | descriptor copy `+0x34`, the tonemap convolution level; read at `0x007037A2` and `0x007037B5` |
| `+0x360` | `u32[2]` | descCopy38 | descriptor copy `+0x38` |
| `+0x380` | `u32[2]` | descCopy58 | descriptor copy `+0x58` and `+0x5C`, the two format codes |
| `+0x394` | `u32` | descCopy6C | descriptor copy `+0x6C`, copied into the glare initialisation record (`0x00702120`) |
| `+0x440` | `u8` | depthTexture | the depth texture is used: 1 when init flag `0x10000` (PFXINIT_DEPTHTEXTURE, named by the message at `0x007000C1`) is given and the device's `+0x8E4` is set, else 0 (`0x00700465`-`0x00700486`); then 0 when `0x0071BB00` answers 1 for the dwords `+0x248` and `+0x24C`, descriptor `+0x38` and `+0x3C` (`0x0070048C`-`0x0070049A`). `0x0071BB00` answers 0 when the first of them is 0 or 1 and 1 for every other first value, whatever the second is (`0x0071BB03`-`0x0071BB63`). SetDepthFactorSource and UpdateParameters_Base test it (`0x00711526`, `0x006F8079`) |
| `+0x448` | `void*` | reductionTextures | an array of `+0x450` textures made when slots `+0x4C8` and `+0x4D0` differ (`0x00701BD3`-`0x00701C3B`); read by `0x006F2AF0` (`0x006F2BB0`) |
| `+0x450` | `i32` | reductionCount | ceil(log(size ratio of slots `+0x4D0` to `+0x4C8`) / log 0.5) - 1, at least 0 (`0x00701AD4`-`0x00701BD1`); the length of `+0x448` |
| `+0x458` | `void*` | array458 | an array Initialize makes (`0x00701DA3`-`0x00701DFD`); read by the internal process (`0x006F9E50`-`0x006FA151`) |
| `+0x460` | `i32` | count460 | -1 with init flag `0x400000`, else 0 (`0x0070054D`-`0x00700561`); the bound of Initialize's loops over `+0x458` (`0x00701E4A`, `0x00701ED4`) and of the internal process's (`0x006F9DA3`-`0x006F9F80`) |
| `+0x464` | `u8` | initBit17 | bit `0x20000` of the init flags (`0x007004D0`-`0x007004DB`); SetDepthFactorSource tests it (`0x0071164A`) |
| `+0x465` | `u8` | needsDepth | 1 when ambient occlusion, motion blur, depth of field, heat shimmer, init bit `0x10000000` or the antialias falloff (`+0x141`) is on together with `+0x440` or `+0x464` (`0x007004F4`-`0x00700547`); Initialize then checks the depth format (`0x00700693`, `0x0070107B`) |
| `+0x468` | `void*` | depthFactorTexture | the depth-factor texture of SetDepthFactorSource (`0x0071158C`, `0x0071160E`); the passes take the depth-factor path while it or `+0x58` is set |
| `+0x470` | `i32` | depthFactorKind | the kind SetDepthFactorSource stores (`0x007115B1`); the passes compare it with 8 (`0x006F3864`, `0x006F7883`); ApplyStaticSceneEffects requires 3, which its message calls PFXDFSRC_A (`0x0070E25C`, the text at `0x00D931D0`) |
| `+0x474` | `u32` | depthFactorParam | stored by SetDepthFactorSource (`0x0071159F`); `0x00708D10` takes it as the depth form when it is called with form 6 (`0x00708D4C`, `0x00708D58`) |
| `+0x478` | `f32` | depthFactorA | the first float SetDepthFactorSource stores (`0x00711593`-`0x007115B7`, as the first of 16 bytes); the passes take the 16 bytes from here (`0x006DBE4C`, `0x006F31CC`, `0x006F3D77`) |
| `+0x47C` | `f32` | depthFactorB | the second float SetDepthFactorSource stores (`0x00711599`-`0x007115B7`) |
| `+0x480` | `f32` | depthFactorC | 1.0 / `+0x478`, written by SetDepthFactorSource (`0x007115BE`-`0x007115E5`) |
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
| `+0x4A0` | `f32` | sceneScale4A0 | the third float of `0x0070D190` (`0x0070D1CF`), stored as it is |
| `+0x4A4` | `f32` | sceneScale4A4 | the stack float of `0x0070D190` (`0x0070D1AF`-`0x0070D1B7`), stored as it is; `0x0070D190` returns 0 (`0x0070D1B5`), and turns a first or second float of 0 into 1.0 before it stores them (`0x0070D19B`-`0x0070D1AC`) |
| `+0x4A8` | `void*` | effectMaskColorSource | the source of SetEffectMaskColorSource (`0x0070D5DA`-`0x0070D639`); read by EndPostEffectScene_Process (`0x006FBEF4`) |
| `+0x4B0` | `void*` | effectMaskAlphaSource | the source of SetEffectMaskAlphaSource (`0x0070D79A`-`0x0070D7F9`); read by EndPostEffectScene_Process (`0x006FBEFB`) |
| `+0x4B8` | `u32` | effectMaskColorKind | the kind of SetEffectMaskColorSource (`0x0070D5CE`): above 4 answers `0x80070057` with nothing stored (`0x0070D5C9`-`0x0070D5CC`, `0x0070D648`-`0x0070D677`); kind 0 clears the source `+0x4A8`; a non-zero kind while the byte `+0x144` is 0 clears both and answers 1 (`0x0070D5D4`-`0x0070D62E`); the accepting paths answer 0 (`0x0070D5D8`, `0x0070D640`); the ERROR line (`0x7AEF`) and the WARNING line (`0x7B06`) print under the same two level tests as SetGlareModulatorSource's |
| `+0x4BC` | `u32` | effectMaskAlphaKind | the kind of SetEffectMaskAlphaSource (`0x0070D78E`), with the same rules for `+0x4B0` (`0x0070D789`-`0x0070D837`; the ERROR line `0x7B59` and the WARNING line `0x7B70`; the accepting paths answer 0 at `0x0070D798` and `0x0070D800`) |
| `+0x4C0` | `i32` | alphaOutputType | the alpha output type of SetAlphaOutputParameters (`0x0070DBFA`): -1 means the dword `+0x43C` (`0x0070DBA4`-`0x0070DBA9`), and a type above `+0x43C` answers `0x80070057` with nothing stored, after the ERROR line (line `0x7BCD`) when the levels `0x01F3BA80` and `0x01F3BA90` are both at least 1 (`0x0070DBAF`-`0x0070DBE6`); with 2 EndPostEffectScene_Process runs a second internal pass with neutral colour values for the alpha (`0x006FB92F`, `0x006FBA8E`); the storing path answers 0 (`0x0070DBF8`) |
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
| `+0x540` | `i32` | slotChromaticAberrationCopySource | the source of the chromatic-aberration copy, the same slot as `+0x53C` (`0x006F8CC8`); `0x007422F0` copies it to `+0x544` while `+0x9DD` is set (`0x006FA56E`-`0x006FA66F`); `+0x9DD` needs `+0x9DC`, which is always 0: its only caller `0x006DCCD0` calls it as `0x00709FB0`([`0x02EA0B70`], its second argument, 0, its third, fourth, fifth) (`0x0070476B`, `0x006DCCD4`-`0x006DCCF0`), so the copy never runs |
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
| `+0x59C` | `f32` | sceneArgValue | BeginPostEffectScene's fourth argument, a float, as it came (`0x0070B7E0`) |
| `+0x5A0` | `i32` | sceneArgFifth | BeginPostEffectScene's fifth argument (`0x0070B7D1`), which it also hands to `0x0075CD90` (`0x0070B8FE`) |
| `+0x5A4` | `f32` | cameraNear | the first float of `0x00706C20`, 1.0 when it is 0 or below (`0x00706C53`-`0x00706C81`); the float before the far distance, read with it by the depth-of-field update `0x006FC760` (`0x006FC7E2`) |
| `+0x5A8` | `f32` | cameraFar | the far distance of the render-scene perspective: `0x00706C20` stores its second float, 1000.0 when 0 or below (`0x00706C60`-`0x00706C90`); the game passes the camera's far value (`0x006CC260`) |
| `+0x5AC` | `f32` | cameraFieldOfView | twice the arctangent of `+0x5B0`, the field-of-view angle (atanf through the import thunk, `0x00861F44`(`+0x5B0`); `0x00706CA0`-`0x00706CB9`) |
| `+0x5B0` | `f32` | cameraTanHalfAngle | tan of half `0x00706C20`'s third float, or tan(0.392699) when that tangent is 0 or below (tanf through the import thunk: `0x00861F1A`(half the float), `0x00861F1A`(0.392699); `0x00706C26`-`0x00706C98`) |
| `+0x5B4` | `f32[2]` | cameraPair5B4 | set to 0 by `0x00706C20` as one qword (`0x00706C89`); both floats are read by `0x006FC760` (`0x006FCC11`, `0x006FCC1F`) |
| `+0x5BC` | `f32` | prevCameraNear | the previous frame's first float: `0x00706D90` stores it, 1.0 when it is 0 or below (`0x00706DC3`-`0x00706DF1`) |
| `+0x5C0` | `f32` | prevCameraFar | the previous frame's far distance: `0x00706D90` stores it, 1000.0 when it is 0 or below (`0x00706DD0`-`0x00706E00`), the game passing last frame's values (`0x006CC2A3`) |
| `+0x5C4` | `f32` | prevCameraFieldOfView | the previous frame's field-of-view angle (`0x00861F44`(`+0x5C8`); `0x00706E10`-`0x00706E29`) |
| `+0x5C8` | `f32` | prevCameraTanHalfAngle | the previous frame's tan of half the angle, tan(0.392699) when it is 0 or below (`0x00861F1A`(half the float), `0x00861F1A`(0.392699); `0x00706DB4`-`0x00706E08`) |
| `+0x5CC` | `u64` | prevCameraQword5CC | set to 0 by `0x00706D90` as one qword (`0x00706DF9`) |
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
| `+0x6D8` | `f32` | sceneLuminanceScale | SceneLuminanceScale, the sixth argument of SetRenderSceneLuminanceScale (`0x00706B70`), which must be above 0: otherwise the setter leaves the field and returns `0x80070057`, after the ERROR line when the levels `0x01F3BA80` and `0x01F3BA90` are both at least 1 (`0x00706BA0`-`0x00706BD9`); 1.0 during the alpha pass (`0x006FBC02`). The setter first runs `0x00706C20`(this, its three floats) (`0x00706B7F`), stores `+0x6D4` in either case (`0x00706B98`) and returns `0x00706C20`'s answer when that is negative, else 0, after storing the accepted value at `+0x6D8` (`0x00706BE6`-`0x00706BFF`); `0x00706C20` returns 0 at its one exit (`0x00706CAD`), so the negative case does not arise |
| `+0x6DC` | `f32` | luminanceFactor6DC | 1.0 from Initialize (`0x00704EE8`), forced to 1.0 for the alpha pass and restored (`0x006FBBF8`, `0x006FBDB2`); written by nothing else |
| `+0x6EC` | `u8[4]` | unusedSpan6EC | written and read by no function; nothing fixes its width |
| `+0x6F8` | `i32` | lightShaftIndex | the light shaft the light-shaft setters act on: Initialize sets it to each shaft while it sets them up and then to 0 (`0x00704884`, `0x0070492F`); read by SetLightShaftEnable (`0x00707880`), `0x00707950` and `0x00707A40` |
| `+0x6FD` | `u8` | changeFlag6FD | a change flag for the update `0x006FC760`, which clears it (`0x006FC7D0`). Set to 1 by `0x00706C20` and `0x00706D90` (`0x00706C4C`, `0x00706DBC`), `0x00706F60` and `0x00707220` (`0x00706F6A`, `0x0070722A`), `0x00708470`, `0x007084E0` and `0x00708540`, each twice (`0x00708486` and `0x007084C2`, `0x007084ED` and `0x00708510`, `0x0070854D` and `0x00708570`), `0x00708710` (`0x00708717`), `0x007114F0` (`0x007114F6`) and `0x007116A0` (`0x007116AC`), among others: the library's code holds 48 byte stores of 1 at displacement `+0x6FD`, 31 in 22 listed functions from `0x006F2690` to `0x007116A0` and 17 outside the function list, and one store of 0, the update's. `0x00708CD0` runs the update first while it is set (`0x00708CD6`-`0x00708CE2`) |
| `+0x700` | `f32` | focusDistance | depth of field: the focus distance; `0x00708540` stores the game's value (`0x00708542`, from `0x006CC090`), which is the auto-focus distance while the command's auto-focus byte is set; `0x00708470` and `0x007084E0` store their first float (`0x0070847B`, `0x007084E2`) |
| `+0x704` | `f32` | focalLength | depth of field: the lens focal length in metres, stored when 0 or more and left as it was for a negative value or a NaN (`0x0070855E`-`0x00708560`; `0x00708494`-`0x00708496` from the seventh argument of `0x00708470`, `0x007084FE`-`0x00708500` from the third float of `0x007084E0`); the game passes 35 / 1000 (`0x006CC144`); 0.024 by default (`0x00704C59`) |
| `+0x708` | `i32` | lensMode | depth of field: 0 from `0x00708540`, 1 from `0x007084E0`, the argument of `0x00708470` (`0x00708577`, `0x00708517`, `0x007084C9`) |
| `+0x70C` | `f32` | apertureFNumber | depth of field: the aperture f-number (`0x00708568`, `0x007084BA`, `0x00708508`); the game passes its f-number |
| `+0x710` | `f32` | lensParam710 | 1.0 from `0x00708540`, 0 from `0x007084E0`, a stack argument of `0x00708470` (`0x0070857D`, `0x00708521`, `0x007084AA`) |
| `+0x714` | `f32` | lensAngle714 | π/4 from `0x00708540` and `0x007084E0`, a stack argument of `0x00708470` (`0x00708587`, `0x00708527`, `0x007084B2`) |
| `+0x718` | `f32` | dofScale718 | 1.0 from Initialize (`0x00704C84`), written by nothing else; read by ApplyEffects_DepthOfField |
| `+0x720` | `f32[2]` | lensPair720 | set to 0 as one qword by `0x00708470`, `0x007084E0` and `0x00708540` (`0x0070848D`, `0x007084F7`, `0x00708557`); both floats are read by `0x006FC760` (`0x006FCB97`, `0x006FCBA6`) |
| `+0x728` | `f32` | exposure | the first float of `0x0070B390`, clamped to at least FLT_MIN (`0x0070B390`-`0x0070B3A8`); the game passes the active view's auto-exposure value (`0x006DC4B0` through `0x006CC170`); 1.0 during the alpha pass |
| `+0x72C` | `f32` | exposureScale | the second float of `0x0070B390`, stored as 0 when it is 0 or below (`0x0070B3FA`-`0x0070B420`); the game passes 2.0 when the device byte is set, else 1.0 (`0x00193E7F`, `0x00193EA6`) |
| `+0x730` | `i32` | exposureMode | the fourth argument of `0x0070B390`, stored on every call (`0x0070B3B7`) |
| `+0x734` | `f32` | hdrRange | the HDR range of `0x0070B390` (stack argument, the game passes 32.0), or 1.0 when `+0x48E` is set and `+0x738` takes 1 / range (`0x0070B3B0`-`0x0070B3F0`); `0x006FC370` keeps `+0x734` / `+0x738` clamped to 0.1..16 or 32 at `+0xC68` |
| `+0x740` | `f32` | block73C_04 | the second float of the 16 bytes Initialize copies from `0x008C5FD0` to `+0x73C` (`0x00704FC7`); read by no instruction |
| `+0x744` | `f32` | block73C_08 | the third float of that copy; read by no instruction |
| `+0x748` | `f32` | block73C_0C | the fourth float of that copy; read by the internal process and EndPostEffectScene_Process |
| `+0x74C` | `f32` | param74C | `0x0070AE10`'s float clamped to 0..1 (`0x0070AE18`-`0x0070AE30`); Initialize passes its default at `0x00704FBB`; read by the internal process and `0x006F4390` |
| `+0x758` | `f32` | focusNear | `+0x750` clamped between the near distance `+0x5A4` and 0.99 × far (`0x006FC7BC`-`0x006FC806`, `0x006FC760`) |
| `+0x75C` | `f32` | focusFar | `+0x754` clamped to the far distance and above `+0x758` (`0x006FC7C4`-`0x006FC846`) |
| `+0x764` | `i32` | vignetteMode | vignette: 0 off, 1 from `0x0070B4B0`, 2 from CPostEffect::SetVignetteByOptics `0x0070B500`, 3 from CPostEffect::SetVignetteByOpticsImageCircle `0x0070B610`, 4 from `0x0070B700` (`0x0070B4EC`, `0x0070B5F9`, `0x0070B6E2`, `0x0070B764`); the two optics setters store 0 first (`0x0070B511`, `0x0070B630`) and the other two store 0 only when they refuse (`0x0070B4CD`, `0x0070B724`); Initialize leaves it 0 through `0x0070B4B0`(0, 0.05) (`0x0070502C`); read by `0x006FD110` and `0x006FC760` |
| `+0x768` | `f32` | vignetteA | vignette: `0x0070B4B0`'s first float (`0x0070B4DA`) |
| `+0x76C` | `f32` | vignetteB | vignette: `0x0070B4B0`'s second float (`0x0070B4E4`), `0x0070B700`'s stack float (`0x0070B75C`) or SetVignetteByOpticsImageCircle's stack float (`0x0070B66A`) |
| `+0x770` | `f32` | vignetteC | vignette: the first float of SetVignetteByOptics (`0x0070B54D`), SetVignetteByOpticsImageCircle (`0x0070B64C`) and `0x0070B700` (`0x0070B744`) |
| `+0x774` | `f32` | vignetteOpticsA | vignette by optics: SetVignetteByOptics's second float (`0x0070B571`); read by `0x006FC760` and `0x006FD110` |
| `+0x778` | `f32` | vignetteOpticsB | vignette by optics: its third float (`0x0070B579`); read by `0x006FC760` and `0x006FD110` |
| `+0x77C` | `f32` | vignetteOpticsC | vignette by optics: its first stack float (`0x0070B581`); read by `0x006FC760` and `0x006FD110` |
| `+0x780` | `f32` | vignetteOpticsD | vignette by optics: its second stack float (`0x0070B589`); read by `0x006FC760` and `0x006FD110` |
| `+0x784` | `u8` | vignetteOpticsFlagA | vignette by optics: SetVignetteByOptics's third stack argument, a byte (`0x0070B555`-`0x0070B55A`) |
| `+0x785` | `u8` | vignetteOpticsFlagB | its fourth stack argument (`0x0070B566`-`0x0070B56B`), or the third stack argument of SetVignetteByOpticsImageCircle (`0x0070B641`-`0x0070B646`) |
| `+0x788` | `f32` | vignetteCircleA | vignette by optics image circle: SetVignetteByOpticsImageCircle's second float (`0x0070B654`); read by `0x006FC760` and `0x006FD110` |
| `+0x78C` | `f32` | vignetteCircleB | vignette by optics image circle: its third float (`0x0070B65F`); read by `0x006FC760` |
| `+0x790` | `f32` | vignetteCircleC | vignette by optics image circle: its second stack float (`0x0070B672`); read by `0x006FC760` |
| `+0x794` | `f32` | vignetteD | vignette: `0x0070B700`'s second float (`0x0070B74C`) |
| `+0x798` | `f32` | vignetteE | vignette: `0x0070B700`'s third float (`0x0070B754`) |
| `+0x79C` | `u8` | vignetteFlag79C | vignette: `0x0070B700`'s third stack argument, a byte (`0x0070B731`-`0x0070B73C`); not stored when the setter refuses |
| `+0x7A0` | `f32` | hdrLimit | `0x0070B390`'s last stack float, FLT_MAX becoming `0x7EFFFFFF` (`0x0070B40D`-`0x0070B42A`); the game passes -FLT_MAX (`0x006CC198`). `0x0070B390` returns 0; its `0x80070057` return (`0x0070B433`) sits behind a test of 0 above 0 (`0x0070B405`-`0x0070B40B`) and is never taken |
| `+0x96C` | `i32` | colourSpaceA | 0 from Initialize (`0x0070500C`). `0x0070B2A0` copies the 64 bytes at `+0x92C` to its second argument (`0x0070B2AD`-`0x0070B2DA`) and returns that pointer; when `+0x96C` differs from `+0x970` it first calls `0x006E2C30`(&a, `+0x96C`), `0x006E3000`(&b, `+0x970`) and `0x006F1070`(&c, &a, &b) (`0x0070B2DE`-`0x0070B318`) and then `0x006F1070`(copy, copy, &c) (`0x0070B32B`); `+0x92C` itself is not written |
| `+0x970` | `i32` | colourSpaceB | 0 from Initialize (the qword at `0x0070500C`); the second value `0x0070B2A0` compares |
| `+0x974` | `u8` | dofEnable | the depth-of-field enable: `0x00708710` stores the game's enable byte when `+0x130` is set and returns 0, else stores 0 and returns 1 (`0x00708710`-`0x00708733`), setting `+0x6FD` in both cases (`0x00708717`); read by the depth-of-field update `0x006FC760` |
| `+0x975` | `u8` | feedbackEnable | the feedback enable of SetFeedbackEnable (`0x0070AFE7`), 0 when `+0x13E` is clear (`0x0070AFD5`); read by the internal process and `0x0070B150` |
| `+0x978` | `f32` | feedbackParam978 | 0 from Initialize (`0x00704BBB`); also the setter `0x0070B000`'s second argument (`0x0070B002`), reached only from `0x006DC7A0`, which no call, jump or stored pointer names; read by `0x006F6D80` (`0x006F71DE`) |
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
| `+0xC24` | `u8` | temporalAntialiasEnable | the enable byte of SetTemporalAntialiasEnable: its argument while `+0x136` is set (`0x0070ABD7`, answer 0), else 0 (`0x0070ABC5`, answer 1) |
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
| `+0xC64` | `f32` | autoExposureSet | 1.0 from every call of `0x0070EC90`, whose one refusing return no input reaches (`0x0070ED70`); read by the auto-exposure pass `0x006F4390` |
| `+0xC68` | `f32` | hdrRangeRatio | `+0x734` / `+0x738` clamped to 0.1..16 when `+0x48E` is set, else 0.1..32 (`0x006FC6D1`-`0x006FC74A`); read by `0x006F4390` (`0x006F488E`) |
| `+0xC6C` | `i32` | glareMode | the glare mode of SetGlareParameters (`0x007075C4`); the game passes 1 (`0x006CC1E0`); read by the internal process |
| `+0xC70` | `f32` | glareRemapFactor | SetGlareParameters' fifth argument, refused when 0 or below (`0x0070756D`); stored when above 0.001, 0.001 (`0x3A83126F`) otherwise (`0x007075AB`-`0x007075E1`); read by the internal process (`0x006FAB86`, `0x006FB015`) |
| `+0xC74` | `i32` | glareActive | 1 from Initialize (`0x00704F0C`), and set by nothing else in the code the game reaches; two library setters no instruction or table references write it too: `0x006DB9C0` jumps to `0x00707600` with the object `0x02EA0B70`, which stores its edx argument, and `0x00707610` (behind `0x006DB9E0`) stores -1 (`0x0070761B`); `0x006FE7A0` reports glare on (1.0) while it is non-zero and the glare luminance `+0x6E4` is above 0, and with -1 only while the word `+0xC78` is not below 0 (`0x006FE7A0`-`0x006FE7DD`); read by the internal process and `0x006FE7F0` |
| `+0xCC0` | `i32` | paramCC0 | 1 from Initialize (`0x00704F6B`), written by nothing else; read by `0x006FECC0` |
| `+0xCD0` | `f32` | paramCD0 | 0 from Initialize (`0x007051A1`), written by nothing else; read by the internal process (`0x006FABE9`) |
| `+0xCD4` | `f32` | paramCD4 | 1.0 from Initialize (`0x007051A8`); the internal process divides by it (`0x006FAC47`, `0x006FACD2`) |
| `+0xCD8` | `f32` | paramCD8 | 1.0 from Initialize (`0x0070517D`); read by the internal process (`0x006FAE1E`) |
| `+0xCDC` | `f32` | paramCDC | 1.0 from Initialize (`0x00705187`); read by the internal process (`0x006FAE38`) |
| `+0xCF0` | `f32` | depthOfFieldDepthScaleInverse | 1 / `+0xCE8` (`0x006FD02E`-`0x006FD037`), set by the depth-of-field update `0x006FC760`; with `+0xCF4` it undoes the `+0xCE8`/`+0xCEC` depth map, the last step of `0x00708D10`'s depth conversion (`0x00708E92`-`0x00708ECB`); `0x006FE620` starts the motion-blur depth window from it (`0x006FE671`) |
| `+0xCF4` | `f32` | depthOfFieldDepthOffsetInverse | -(`+0xCEC` / `+0xCE8`) (`0x006FD033`-`0x006FD04C`), the offset that goes with `+0xCF0`; added in `0x00708D10`'s last step (`0x00708EAB`) and in `0x006FE620` (`0x006FE681`) |
| `+0xCF8` | `f32` | depthReferenceDistance | the reference distance of the first step of `0x00708D10`'s depth conversion, which also uses the near and far distances (`0x00708DEF`-`0x00708E36`): the focus distance `+0x700` while depth of field is on (`0x006FCEAA`-`0x006FCEB0`); otherwise the near end of the depth window that motion blur (`+0xA64`/`+0xA68`), heat shimmer (`+0xB10`/`+0xB14`) and the antialias falloff (`+0xC58`/`+0xC5C`) need, the whole near-to-far range when `0x006FD760` asks or motion blur is type 2, raised to at least `+0x758`, and the far distance when nothing needs a window (`0x006FC9DA`-`0x006FCB26`, `0x006FCEDD`), or that window's far end capped at near x 64000 when both scene textures have depth formats and `+0x760` is clear (`0x006FCF3C`-`0x006FCFF5`); also read by `0x006F2CB0`, `0x006FD760`, `0x006FE620`, `0x0070E1B0` and `0x00708CD0`, which returns it after running the update `0x006FC760`(this) when `+0x6FD` is set (`0x00708CD6`-`0x00708CF5`) |
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
| `+0xD38` | `void*` | effectSourceCurrent | the effect source in use: `0x006FD070` picks it from `+0xD8`, `+0xE0`, `+0xE8` or `+0x28` (`0x006FD085`-`0x006FD0FB`); EndPostEffectScene_Process sets and restores it around the alpha pass (`0x006FB9D5`, `0x006FBE90`); cleared by `0x0070D240` (`0x0070D257`), which also clears `+0xD8` and `+0xE0` (`0x0070D249`, `0x0070D250`), and by `0x0070D270` (`0x0070D31A`), which also clears `+0xE0` and `+0xE8` (`0x0070D302`, `0x0070D30F`) |

`SetDepthFactorSource`¹ takes a kind, a texture, a second source object, a parameter and two
floats, and first sets the byte `+0x6FD` to 1². It has a source when either pointer is set³. A kind of 9 is resolved first⁴: with no source it becomes 8
while the byte `+0x440` is set and 3 otherwise; with a source it becomes 0 when the source's format code is
`0x14`, `0x28`, `0x2D` or `0x37` and 3 otherwise. The format code is the texture's dword `+0x44`, or the
second object's `+0xB0` when no texture is given.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007114F0` |
| ² | `0x007114F6` |
| ³ | `0x007114FD`-`0x0071150C` |
| ⁴ | `0x0071151C`-`0x00711557` |

</details>

A parameter of 5 is resolved next¹: with a source it becomes 0 for those four format
codes and 2 for any other; with no source it becomes 0 when the kind, as resolved, is 8 and 2 otherwise.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0071156B`-`0x00711640` |

</details>

With a source while the byte `+0x464` is 0, the call stores nothing more and answers `0x80004001`¹. When the levels `0x01F3BA80` and `0x01F3BA90` are both at least 1 it first logs, through
`0x006DF480`, a PPFX ERROR line, source line `0x8001`: "CPostEffect::SetDepthFactorSource(): Initialize() with
PFXINIT_DEPTHFACTORSOURCETEXTURE flag for user depth factor texture."

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00711645`-`0x00711682` |

</details>

Otherwise it answers 0 and stores the kind at `+0x470` and the parameter at `+0x474`. With a source and a kind
other than 8 it keeps the texture at `+0x468`, the second object at `+0x58` and the two floats at `+0x478` and
`+0x47C`¹; in every other case it stores 0 in both pointers and the floats 1.0 and 0². The 16-byte store that carries the floats also puts 0 in `+0x480` and `+0x484`³; the last two stores replace that with `1.0 / [+0x478]` at `+0x480` and
`-([+0x47C] / [+0x478])` at `+0x484`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007115F8`-`0x00711619` |
| ² | `0x00711585`-`0x0071158C` |
| ³ | `0x007115A7`-`0x007115B7` |
| ⁴ | `0x007115BE`-`0x007115E5` |

</details>

`EndPostEffectScene_PreProcess`¹ gives each effect that is on its own render-buffer slots from the ring `+0x4D0`, `+0x4D4` .. `+0x4D4` + `+0x36C` - 1². An effect that is off passes its source slot on as its result. `EndPostEffectScene_InternalProcess`³ then draws the effects in this order:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006F8740` |
| ² | `0x006F8904`-`0x006F8D53` |
| ³ | `0x006F9030` |

</details>

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

Each result slot is the next step's source slot: `+0x4E0` = `+0x4E4`, `+0x52C` = `+0x548`, `+0x54C` = `+0x538`, `+0x53C` = `+0x540`, `+0x544` = `+0x530` and `+0x534` = `+0x550` = `+0x554` are stored from one register¹. Motion blur takes its slots from `0x006FE080` at whichever of the two places `+0xD14` picks.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006F8967`-`0x006F8D53` |

</details>

`0x00708D10` writes a depth conversion to its second argument: 16 bytes holding a scale `a`, an offset `b`, `1.0 / a`
and `-(b / a)`¹, and returns 0. Its third and fourth arguments name the depth form converted
from and to; a 6 stands for the parameter `+0x474`². While the byte `+0x6FD` is set it runs the
update `0x006FC760(object)` first (`0x00708D5E`-`0x00708D67`, and once more at `0x00708DDE`-`0x00708DEA` when the two forms
differ).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00708F65`-`0x00708FA2` |
| ² | `0x00708D46`-`0x00708D58` |

</details>

It starts from `a = 1.0`, `b = 0` and, when the two forms differ, applies each step that lies between the lower and
the higher of them, in rising order¹. Step 0 to 1 uses the near distance `n` (`+0x5A4`), the
far distance `f` (`+0x5A8`) and the reference distance `r` (`+0xCF8`): `a = (f - n) × r / (f × n)` and
`b = 1.0 - r / n`. Step 1 to 2 applies the depth-of-field map: `a = a × [+0xCE8]`, `b = b × [+0xCE8] + [+0xCEC]`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00708D8F`-`0x00708ECB` |

</details>

Step 2 to 3 applies the inverse map the same way, `a = a × [+0xCF0]`, `b = b × [+0xCF0] + [+0xCF4]`, and then
`a = a × k`, `b = b × k` with `k` the float `0x00709540(object)` returns¹. When the form
converted to is the lower of the two, the result is then inverted: `b = -(b / a)`, `a = 1.0 / a`². Last, on every path, come its two stack floats `s` and `o`, unless `s` is 1.0 and `o` is 0:
`b = b - (o / s) × a`, then `a = a × (1.0 / s)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00708E92`-`0x00708ECB` |
| ² | `0x00708ED9`-`0x00708EFA` |
| ³ | `0x00708F00`-`0x00708F5F` |

</details>

`0x0070EC90`, the auto-exposure setter, takes a view, two floats `p` and `q` and five stack floats `t1` to `t5`. It
holds `p` to 0..1.0 and `q` and `t1` to 0 or more¹. `t2`, `t3` and `t4`, each when below 0,
take `p`, `q` and `t1` as just limited², and are then held to the same limits: `t2` to 0..1.0,
`t3` and `t4` to 0 or more³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0070ECA7`-`0x0070ECD9` |
| ² | `0x0070ECDC`-`0x0070ED03` |
| ³ | `0x0070ED06`-`0x0070ED25` |

</details>

It stores 1.0 at `+0xC64`¹ and writes the values to the `0x68`-byte auto-exposure record of the view,
`[+0x1F8] + 0x68 × view`: the view named when it is 0 or more and below the signed count `+0x328`, the active view
`+0x1F0` standing for -1, and every view below the count for `0x7FFFFFFF`; any other view gets no record². The record takes `t5` at `+0x30`, `p` at `+0x34`, `q` at `+0x38`, `t1` at `+0x3C` and `t2`,
`t3`, `t4` at `+0x40`, `+0x44` and `+0x48`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0070ED70` |
| ² | `0x0070ED7A`-`0x0070EE0E` |

</details>

`0x0070EC90` answers 1 when a record it wrote has a null qword `+0x60`, else 0¹. Its
`0x80070057` return² is never taken: the eight tests before it³ ask whether a value
lies outside the limit it has just been held to, and each is a `comiss` / `ja` pair, which a value that is not a
number does not take either.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0070EDD9`-`0x0070EDE3`, `0x0070EE15` |
| ² | `0x0070EE26` |
| ³ | `0x0070ED28`-`0x0070ED6A` |

</details>

The init descriptor, `PFX_INITPARAM` (named by Initialize's check of its first field), is `0x118` bytes. `0x006CBBC0` writes its defaults; `0x006CBD20` builds one on its stack and changes four fields before `0x006DAA70` passes it on (`0x006CBDD7` to `0x006CBDF3`). Initialize copies it to `+0x210` and again to `+0x328`¹ and works from the second copy.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006FFA65`, `0x006FFB0B` |

</details>

`PpfxInitDescriptor` (`0x118` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `i32` | effectViews | PFX_INITPARAM::m_nEffectViews, the number of effect views: default 1 (`0x006CBBC2`); Initialize refuses a value below 1 with "PFX_INITPARAM::m_nEffectViews must be greater than or equal to 0." (`0x006FFDBB`) and allocates one auto-exposure record (`0x68` bytes) and one auto-focus record (`0x48` bytes) per view (`0x00700B5A`-`0x00700D9E`) |
| `+0x004` | `u32` | sceneFormat | a texture format code for the effect buffers; 0 (the default) lets `0x006F2380` choose, or the value at rbp-`0x80` when CPostEffect `+0x48F` is set (`0x00700F2B`-`0x00700F59`); read at `0x007003ED`. `0x006F2380` returns `0x00726FB0`(CPostEffect `+0x20`, flags, 3, list, 7, `0xA`): the flags 1 plus `0x80000` when bit `0x1000` of CPostEffect `+0x20C` is set, the list `0xA`, `0xA`, `0xB`, 2, `0x18`, `0x1C`, `0x57`, its count and the fallback `0xA` (`0x006F2393`-`0x006F23F2`) |
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
| `+0x05C` | `u32` | formatB | a texture format code; 0 lets `0x006F24F0` choose, or `0x1D` when CPostEffect `+0x48D` is set (`0x00700F77`-`0x00700FB4`); passed into the glare initialisation record (`0x007020F9`). `0x006F24F0` returns `0x00726FB0`(CPostEffect `+0x20`, `0x20001`, 3, list, 5, `0x18`): the list `0x18`, `0x18`, `0x1C`, `0x57`, `0x58`, its count and the fallback `0x18` (`0x006F2503`-`0x006F253D`) |
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

`0x00713820`, which picks the velocity format of `+0xF8`, turns seven texture format codes into others and returns every
other code as it came: `0x1D` gives `0x1C`, `0x48` gives `0x47`, `0x4B` gives `0x4A`, `0x4E` gives `0x4D`, `0x5B`
gives `0x57`, `0x5D` gives `0x58` and `0x63` gives `0x62`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00713822`-`0x00713897` |

</details>

The integration object at `0x02D38540`, `0x10` bytes from `0x0065E5D0`:

`PostProcessingLibraryWrapper` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | record | the `0x78`-byte integration record built by `0x006CBAA0` (`0x0065E553`-`0x0065E56D`); every wrapper of `0x00193DA0` loads it first |
| `+0x08` | `u8` | ready | the ready flag: 0 from the constructor `0x0065E530` (`0x0065E54C`), 1 from `0x0065E580` after `0x006CBD10` (`0x0065E591`, called at `0x0062549D`), which only stores its second argument's low byte at `+0x74` of the record (`0x006CBD10`); `0x0018E470` reads the flag through `0x001976E0` (`0x0018E481`) and builds the post-process command only while it and the render parameter block's `+0xA0` are set |
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

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

| Fact | Value |
|---|---|
| span | `0x006DA880` to `0x007911DF` |
| member lists | [`yebis-ppfx-post-effects-members.tsv`](yebis-ppfx-post-effects-members.tsv), 1,599 functions; [`yebis-ppfx-post-effects-unlisted-bodies.tsv`](yebis-ppfx-post-effects-unlisted-bodies.tsv), 732 bodies in the span that the function list does not hold |
| source paths | 25 distinct, 299 copies, 363 loading sites; most sites: `GPUDepthOfField.cpp` 75, `GPUPostEffect.cpp` 48, `GPURenderGlare.cpp` 39, `TFXString.cpp` 30 |
| absolute header path | 12 copies, 6 of them loaded, 20 sites |
| diagnostic log | 801 call sites, 422 distinct literal strings; listed in [`yebis-ppfx-post-effects-diagnostic-strings.tsv`](yebis-ppfx-post-effects-diagnostic-strings.tsv) |
| licence dates | all six 0 |
| calls into the span from outside | the integration functions at `0x006CBD20` to `0x006CC2F0`, static initialisers, exit and unwind code, and seven PhyreEngine calls to `0x0071F970`, a formatted-scan body (`__stdio_common_vsscanf`) the linker placed inside the span |

### Columns of yebis-ppfx-post-effects-members.tsv

One row per function, 1,599 rows in address order.

| Column | Holds |
|---|---|
| `entry` | the function's entry address, from `0x006DA880` to `0x00791140`, all inside the span |

### Columns of yebis-ppfx-post-effects-unlisted-bodies.tsv

One row per body, 732 rows, each inside the span between two functions of
[`yebis-ppfx-post-effects-members.tsv`](yebis-ppfx-post-effects-members.tsv).

| Column | Holds |
|---|---|
| `member_below` | the nearest function of the member list below the body (183 distinct values) |
| `member_above` | the nearest function of the member list above the body (183 distinct values) |
| `refs` | how many places in the image name the body's start address: a call, jump or RIP-relative operand, a call or jump byte sequence in the code that targets it, an 8-byte relocated pointer, or a 4-byte image offset in a data section (the unwind table `.pdata` is not counted); 0 on 618 rows, 1 on 112, 2 on 2 |

### Columns of yebis-ppfx-post-effects-diagnostic-strings.tsv

| Column | Holds |
|---|---|
| `format_string` | the literal as the image holds it, with a backslash written `\\`, a line feed `\n` and a tab `\t`; 422 rows, one per distinct string |
| `call_sites` | the calls to `0x006DF480` that the string reaches as the format: the `lea rcx` that loads it is followed forward through branches to the call, so a call shared by several branches counts once for each string. The column sums to 835 over 798 calls |
| `owner_functions` | the start addresses of the functions that hold the string's call sites, in address order and separated by spaces; one function on 383 of the 422 rows, up to 44 on one row. 160 functions occur, all inside the span; `0x006FF900` is the one owner of 73 strings |

</details>

## Operations

| Address | Entry point | Name from its own diagnostics |
|---|---|---|
| `0x006DA880` | allocate through the installed allocator, count it in `0x02EA0B3C` | |
| `0x006DA8A0` | free, uncount | |
| `0x006DA8F0` | install an allocator; refused while `0x02EA0B3C` is not 0: then it prints the ERROR line "SetMemoryAllocator(): Call when any pfx interface is not instantiated yet." while `0x01F3BA80` and `0x01F3BA90` are both non-zero and returns `0x80004005` (`0x006DA8FB`, `0x006DA91B`-`0x006DA92C`); otherwise it stores its argument at `0x01F3BA68`, or the built-in allocator `0x01F3BA78` for a null argument, and returns 0 (`0x006DA936`-`0x006DA94B`) | `SetMemoryAllocator()` |
| `0x006DAA50` | set the licence text | |
| `0x006DA990` | create the context: `0x18` bytes from `0x006DA880` through the installed allocator `[0x01F3BA68]`, tagged `..\src\ppfx.cpp`, line 702 and "IPfxContext::Instantiate()" (`0x006DA9C4`); a block it gets is built by `0x006E0390` (vtable `0x00D8FA10`, 1 at `+0x08`, zero at `+0x10`) and given the vtable `0x00D8F918` (`0x006DA9D9`-`0x006DA9E5`); a failed allocation returns null (`0x006DA9ED`) | `IPfxContext::Instantiate()` |
| `0x006DAA70` | initialise: licence, global block, post-effect | `IPfxBaseContext::Initialize()` |
| `0x006DE780` | shut down: uninitialise, clear the block's maps, clear `0x02EA0B70`. It sets the vtable `0x00D8F8E8` (`0x006DE7AD`); with `[0x02EA0B70]` null it goes straight to the closing banner (`0x006DE7E9`). Otherwise it releases `0x02EA0B78` and `0x02EA0B80` through their slot `+0x08` and clears them (`0x006DE7F2`-`0x006DE81F`), runs `0x00705520(block, 0)`, `CPostEffect::Uninitialize` (`0x006DE82F`), and on a negative result prints an ERROR line with the code and its text from `0x0071B3C0` (`0x006DE859`-`0x006DE873`). Then `0x006FF840` clears the block's maps (`0x006DE8C2`), `0x006DA8A0` frees the block through `[0x01F3BA68]` (`0x006DE8CE`), `0x02EA0B70` is cleared (`0x006DE8D4`) and the object's `+0x10` is zeroed (`0x006E0370`, `0x006DE8E4`). It ends by a tail jump to `0x006E03C0`, which stores the vtable `0x00D8F9E8` (`0x006DE939`). The opening banner, the success line and the closing banner print only while `0x01F3BA80` and `0x02EA0B40` are non-zero, and the closing banner is skipped after a failed Uninitialize (`0x006DE8E9`) | `IPfxBaseContext::~IPfxBaseContext()` |
| `0x006FF900` | build the effect chain on the GPU device | `CPostEffect::Initialize()` |
| `0x00707560` | glare parameters: refuses a fifth argument (GlareRemapFactor) of 0 or below with the ERROR line "GlareRemapFactor must be greater than 0.0." and returns `0x80004005` (`0x0070756D`, `0x007075A1`); otherwise it stores the mode at `+0xC6C` (`0x007075C4`), the two values at `+0x6E4` and `+0x6E0` (`0x007075CB`, `0x007075D3`) and the factor at `+0xC70` when it is above 0.001, or 0.001 otherwise (`0x007075AB`, `0x007075DB`, `0x007075E1`), and returns 0 (`0x007075E7`) | `CPostEffect::SetGlareParameters()` |
| `0x0070B4B0` | vignette, mode 1: clears the byte `+0x3B8` of the object `+0x118` when that object is set (`0x0070B4B0`-`0x0070B4BC`); a first float of 0 stores mode 0 at `+0x764` and neither float (`0x0070B4C6`-`0x0070B4D7`); any other value stores both floats at `+0x768` and `+0x76C` and mode 1; it returns 0 either way | |
| `0x0070B500` | vignette by optics: stores mode 0, clears the byte `+0x3B8` of the object `+0x118` with no pointer test (`0x0070B504`-`0x0070B51B`) and stores its five floats and two bytes at `+0x770`-`+0x785`. It returns 0 with mode 0 when the first float is 0 or below and the optics values are unusable: the second float 0 or below, the second stack float 0, or the third float and the first stack float both 0 (`0x0070B50E`-`0x0070B549`, `0x0070B591`-`0x0070B595`). Otherwise, while the byte `+0x132` is 0, it returns 1 with mode 0, after the WARNING line "CPostEffect::SetVignetteByOptics(): Initialize() with PFXINIT_OPTICALVIGNETTING flag for optical vignetting." (line `0x298E`) when the levels `0x01F3BA80` and `0x01F3BA8C` are both at least 1 and the optics values are usable or the first float is above 0 (`0x0070B597`-`0x0070B5D8`); with `+0x132` set it stores its fifth stack argument, a byte, at `+0x3B8` of the object `+0x118`, when that is set, and mode 2, and returns 0 (`0x0070B5E2`-`0x0070B603`) | `CPostEffect::SetVignetteByOptics()` |
| `0x0070B610` | vignette by optics image circle: stores mode 0, clears the byte `+0x3B8` of the object `+0x118` without testing the pointer (`0x0070B630`-`0x0070B63A`), stores its third stack argument, a byte, at `+0x785` (`0x0070B646`) and its five floats. With the first and the second float both 0 or below it returns 0 with mode 0 (`0x0070B62D`, `0x0070B65C`-`0x0070B67E`). Otherwise, while the byte `+0x132` is 0, it returns 1, after the same WARNING text under its own name (line `0x29CE`) when the levels `0x01F3BA80` and `0x01F3BA8C` are both at least 1 and, besides, the second float is not 0 or below, or the first is above 0 (`0x0070B680`-`0x0070B6C1`); with `+0x132` set it stores its fourth stack argument, a byte, at `+0x3B8` of the object, when that is set, and mode 3, and returns 0 (`0x0070B6CB`-`0x0070B6EC`) | `CPostEffect::SetVignetteByOpticsImageCircle()` |
| `0x0070B700` | vignette, mode 4: stores its second stack argument, a byte, at `+0x3B8` of the object `+0x118` when that object is set (`0x0070B700`-`0x0070B711`). When its first float is 0 or below and its third is below 0 it stores mode 0 and nothing else (`0x0070B71A`-`0x0070B72E`); otherwise it stores its third stack argument, a byte, at `+0x79C`, the four floats and mode 4 (`0x0070B731`-`0x0070B764`). It returns 0 either way | |
| `0x0070B990` | end the scene: calls `0x006FB810(its own first three arguments, unchanged)` (`0x0070B996`) and returns 0, or the negative result it gave, after the ERROR line "CPostEffect::EndPostEffectScene(): EndPostEffectScene_Process() failed (0x%x: %s)." (line `0x5D29`, the result and its name from `0x0071B3C0(result)`) when the levels `0x01F3BA80` and `0x01F3BA90` are both at least 1 (`0x0070B99D`-`0x0070B9E4`) | `CPostEffect::EndPostEffectScene()` |
| `0x0070BA00` | run the effects on a frame: refused with `0x80004005` while the byte `+0x00` is set ("Cannot be called while BeginPostEffectScene() and EndPostEffectScene()", `0x0070BA0A`, `0x0070BA43`), and while the byte `+0x147` is set with no output target at `+0x60` ("At least SetEffectSource() must be called", `0x0070BA53`-`0x0070BA92`); otherwise it calls `BeginPostEffectScene` (`0x0070B780`, `0x0070BAC2`) with 0, 0, the float `0xFF7FFFFF`, 0 and -1, then `EndPostEffectScene` (`0x0070B990`, `0x0070BACF`) with its own second argument and 0, and returns End's result when it is negative, else 0 (`0x0070BAD9`-`0x0070BADE`) | `CPostEffect::ApplyEffects()` |
| `0x006DF480` | write a diagnostic line | |

## State

<details>
<summary>Show the state it keeps</summary>

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

`0x006EF480(n, out, scale)` called with a null `out` returns `3 x n x (n + 1) + 1` at once¹. The static initialiser `0x00168EE0` calls it with 5, a null `out` and 1.0, and keeps the
result.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006EF48E`-`0x006EF4B3` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EA4024` | `i32` | 0 (zero-filled tail) | 91, the count `0x006EF480(5, 0, 1.0)` returns; both readers take `trunc(sqrtf(count x 4 / π))` from it (`0x00DABDDC`, 1.27324), which is 10 | `0x00168EE0` (`0x00168EF6`) | `CDepthOfField::CreateDeviceResources` `0x0076F400` (`0x0077075B`); `CDepthOfField::CreateScatterBokehTexture` `0x0077A8C0` (`0x0077AA08`) |

No other instruction reaches `0x02EA4024`: no other RIP-relative, image-base-relative or 32-bit offset reference names
it. The addresses taken near it are two one-time initialisation guards, `0x02EA4020`¹ and `0x02EA4008`², and a loop bound, `0x02EA4010`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00763890` |
| ² | `0x00764240` |
| ³ | `0x00764240` |

</details>

### The library's other statics

Every other written static of the library is a row of
[yebis-ppfx-post-effects-state.tsv](yebis-ppfx-post-effects-state.tsv), with its type, start value, meaning and
every writing and reading instruction. The sections below explain each group; the table names the rows.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| each row of [yebis-ppfx-post-effects-state.tsv](yebis-ppfx-post-effects-state.tsv): 211 statics from `0x01F3C500` to `0x02EA40BC` | per row | per row: the image value for the `01F3xxxx` rows, 0 (zero-filled tail of `.data`) for the rest | per row, by group below | per row (`set_by`) | per row (`read_by`); `-` for the 8 statics that no code reads |

### Render-target bindings

`CRenderTexture` (vtable `0x00D9C040`) keeps the device's eight colour targets in two parallel arrays: the render
texture bound to slot *n* at `0x02EA18C0` + 8*n* and the surface of it in use at `0x01F3CB18` + 4*n*. The binder
`0x007224C0` stores both¹; a caller passing surface -1 gets the stored one². Every
loop over the slots stops at 8.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007225A9`, `0x007225B1` |
| ² | `0x0071FD78` |

</details>

The binder takes the texture, the slot, a flag word, a byte, the surface index and one more value. The surface pointer
is the entry for that index in the list at the texture's `+0xD0 + 8 × [+0xA0]`¹. It first
calls `0x007226E0(slot, flag word, flag word, 0, 1.0, 0, &local)`, unless bit `0x2` of the flag word is set while the
tiling flag `0x02EA18B1` is 0, and returns a negative answer of that call at once².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007224D0`-`0x00722500` |
| ² | `0x00722504`-`0x0072253B` |

</details>

Then it binds the surface through slot `+0x30` of the device at the texture's `+0x28`, passing the slot, the surface
pointer and its last argument; it returns a negative answer of that call and otherwise stores the two array entries¹. It calls `BeginTiling`, `0x00722A40(8, 0, 1.0, 0)`², unless bit `0x4` of the flag
word or bit `0x80000000` of the texture's `+0x38` is set, or the texture's second list, at `+0xE0 + 8 × [+0xA0]`,
holds null for that surface³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0072257F`-`0x007225B1` |
| ² | `0x007225E9` |
| ³ | `0x007225B9`-`0x007225DC` |

</details>

Last, when the byte argument is set, the binder hands slot `+0x78` of the device a block of four dwords and two floats
taken from the texture: `([+0x64] >> s) + [+0x9C]`, `([+0x68] >> s) + [+0x9C]`, `[+0x5C] >> s` and `[+0x60] >> s`,
with `s` the surface index, then the texture's floats `+0x6C` and `+0x70`¹. It returns a
negative answer of that call, and 0 in every other case².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0072261D`-`0x0072266A` |
| ² | `0x0072266D`-`0x00722671` |

</details>

That last call is made only when one of three things holds, every offset here being the texture's: `+0x9C` is not 0;
the surface's recorded size, the dwords `+0x08` and `+0x0C` of its `0x18`-byte entry in the list at `+0x80`, differs
from `[+0x5C] >> s` and `[+0x60] >> s`; or the floats `+0x6C` and `+0x70` are not 0 and 1.0¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00722541`-`0x0072257C`, `0x007225EE`-`0x0072261B` |

</details>

- `0x02EA1914` counts the render textures attached to the current device. Slots 0¹ and 5²
  add 1 when a texture attaches to a new device; slot 1³ subtracts 1 when it detaches. An attach at 0
  stores the device in `0x02EA1918` and clears both arrays; a detach back to 0 clears `0x02EA1918` and both arrays. No
  instruction reads `0x02EA1918`.
- Slot 0⁴ answers 1 at once when bit `0x80000000` of the texture's dword `+0x38` is set
 ⁵. Otherwise it calls `0x007273E0(its own two arguments)` and returns a negative answer as it is
 ⁶.
- Slot 0 counts the attach in `0x02EA1914` when its second argument, the device, is not null and the texture's `+0x28`
  after that call differs from the value read before it; with the count at 0 it first stores the device in `0x02EA1918`
  and zeroes the four qwords from `0x01F3CB18` and the nine from `0x02EA18C0`⁷.
- Slot 0 then calls `0x00720320(texture)` when the texture's `+0x28` and the dword `+0x44` are both set and `+0xA8` or
  `+0xB8` is 0, and returns its answer when negative; in every other case it returns 0⁸.
- `CRenderTexture::BeginTiling`⁹ counts the bound targets into `0x02EA190C` and keeps its first, third and
  fourth arguments and the 16 bytes at its second in `0x02EA1908`, `0x01F3CB38`, `0x02EA1910` and `0x02EA1938`. No
  instruction reads those five. `EndTiling`¹⁰ clears both arrays and `0x02EA1908`.
- `0x02EA18B1` is 1 while tiling is on: `BeginTiling` returns at once when it is set¹¹ and sets it
 ¹²; `EndTiling` tests it¹³ and clears it (`0x00722E21`, `r8d` cleared at `0x00722CD5`).
- `BeginTemporaryFilter` `0x006F2560`¹⁴ and `EndPostEffectScene_PreProcess` `0x006F8740` (`0x006F8D78`, its copy to
  `CPostEffect` `+0xCE2`) read the flag, and so do `0x00721B10`, `0x00722110`, `0x007224C0`, `0x007226E0`, `0x00722800`, `0x00722900`
  and `0x00722E80`.
- `BeginTiling` is called only inside the library, by `0x007224C0`¹⁵ and `0x00722E80`¹⁶. The
  game's calls at `0x005FED6F`¹⁷ and `0x0060F9A0`¹⁸ go to the per-draw block builder `0x00602A40`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007214A0` |
| ² | `0x007215C0` |
| ³ | `0x00721B10` |
| ⁴ | `0x007214A0` |
| ⁵ | `0x007214AF`-`0x007214C2` |
| ⁶ | `0x007214D7`-`0x007214DE` |
| ⁷ | `0x007214B9`, `0x007214EB`-`0x00721564` |
| ⁸ | `0x0072156A`-`0x00721598` |
| ⁹ | `0x00722A40` |
| ¹⁰ | `0x00722C80` |
| ¹¹ | `0x00722A44` |
| ¹² | `0x00722C30` |
| ¹³ | `0x00722C84` |
| ¹⁴ | `0x006F25EB` |
| ¹⁵ | `0x007225E9` |
| ¹⁶ | `0x0072311A` |
| ¹⁷ | `0x005FECF0` |
| ¹⁸ | `0x0060F830` |

</details>

### Device and resource registry

- `0x02EA1948` is the current `IGPUDevice` (vtable `0x00D9EA30`): `IGPUDevice::InitializeDevice`¹ stores
  it and `~IGPUDevice`² clears it. The texture creators `0x007875F0` and `0x00787A90` use it when their
  caller passes no device.
- `0x02EA1960` is a 0x28-byte device description. `InitializeDevice` copies it from its argument or clears it; slot 5
 ³ copies it when an argument is given and otherwise leaves it⁴.
- Slot 5 then calls `0x00724830(device)`⁵. When the argument's `+0x18` is set and differs from the device's
  `+0x30`, it calls slot `+0x10` of the old one, if any, and stores 0 there⁶, then stores the new one
  there and calls its slot `+0x08`⁷. It ends with `InitializeDeviceBuffers`, `0x00723440(device)`
 ⁸, and returns that answer when it is negative, else 0⁹.
- `0x00724830` calls slot `+0x08` of each pointer that is set among the eight from the device's `+0x8F0` and those at
  `+0x930`, `+0x9B8`, `+0x9E0` and `+0x9E8`, stores 0 in each of these, and returns 0¹⁰.
- `InitializeDeviceBuffers`¹¹ replaces a 0 width¹² or height¹³
  with the one the device reports through its slot `+0x80`¹⁴, and takes a reference to the back buffer at
  `+0x20`¹⁵ when one is given.
- `0x02EA1998` and `0x02EA19A8` are the resource registry of `GPUResourceManage.cpp`: the device of the first
  registration (`0x00727460`, through `0x00727800`) and a 0x18-byte list of the registered resources.
- `0x00727800` stores its argument at `0x02EA1998`¹⁶, sets the count `0x02EA19A0` to 0¹⁷ and stores at
  `0x02EA19A8` the list with its three qwords at 0, or 0 when the allocation
  `0x006DA880([0x01F3BA68], 0x18, 0x00D9ECE8, 0x12A, 0)` answers null¹⁸; it returns 0 either way.
- The unregistration `0x007276F0` does nothing and returns 0 for a resource whose `+0x28` is 0¹⁹.
  Otherwise it takes 1 from the count `0x02EA19A0`²⁰ and looks the resource up in the list
 ²¹. Found, it closes the gap with `memmove` (the import slot `0x008C2A40`) and takes 8 from the
  list's end pointer `+0x08`²².
- Not found, it builds the text `WORN: "<name>" is not registered.` from the name at the resource's `+0x18` with
  `0x007195B0(&first, 0x00D9ED98, resource + 0x18)` and `0x00719460(its answer, &second, 0x00D9EE08)`²³
  and calls `0x00715C70(&first)` on the first temporary string²⁴.
- It then logs the text through `0x006DF480` as a PPFX WARNING line, source line `0x1C8`, only when the levels
  `0x01F3BA80` and `0x01F3BA8C` are both at least 1²⁵; logged or not, it goes on and calls
  `0x00715C70(&second)` on the second temporary string²⁶.
- Either way `0x007276F0` then clears the resource's byte `+0x30`²⁷. When the count is 0 or less it frees the
  list and clears both statics and the count through `0x00727870()`²⁸. It returns the count
 ²⁹.
- `CRenderTextureArray::InitializeDevice`³⁰ hands each member's `InitializeDevice`³¹ its
  depth-stencil format through `0x02EA1920` (`0x2D` when the array's `+0x58` is 0) and `0x02EA1924` (the same when its
  flag `0x10000` is set, else 0), and clears both after the call.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00723760` |
| ² | `0x00724500` |
| ³ | `0x00724940` |
| ⁴ | `0x00724955`-`0x00724974` |
| ⁵ | `0x0072497C` |
| ⁶ | `0x007249A5` |
| ⁷ | `0x00724983`-`0x007249B4` |
| ⁸ | `0x007249BA` |
| ⁹ | `0x007249C4`-`0x007249C9` |
| ¹⁰ | `0x00724847`-`0x007248D9` |
| ¹¹ | `0x00723440` |
| ¹² | `0x02EA1960` |
| ¹³ | `0x02EA1964` |
| ¹⁴ | `0x00723473` |
| ¹⁵ | `0x02EA1980` |
| ¹⁶ | `0x00727808` |
| ¹⁷ | `0x00727823` |
| ¹⁸ | `0x00727831`-`0x00727855` |
| ¹⁹ | `0x00727707`-`0x00727710` |
| ²⁰ | `0x00727715` |
| ²¹ | `0x00727729`-`0x00727741` |
| ²² | `0x007277B2`-`0x007277C3` |
| ²³ | `0x00727743`-`0x00727768` |
| ²⁴ | `0x00727773` |
| ²⁵ | `0x00727778`-`0x007277A0` |
| ²⁶ | `0x007277AB` |
| ²⁷ | `0x007277C8` |
| ²⁸ | `0x007277CC`-`0x007277D6` |
| ²⁹ | `0x007277DB` |
| ³⁰ | `0x0075C080` |
| ³¹ | `0x00720320` |

</details>

### Effect-constant staging buffers

The passes stage their shader constants in three static buffers and hand each to their effect's vector-array setter,
slot `+0x98` of `IGPUEffect` (vtable `0x00DAF1B8`, built by `0x00789900`):

| Buffer | Size | Filled by | Handed over by |
|---|---|---|---|
| A, `0x02EA1A50` | `0x100` bytes, up to the next static `0x02EA1B50` | the loops below and direct stores | 25 calls |
| B, `0x02EA1C50` | 16 vectors: `0x0074AB30` and `0x0074B6A6` hand over 16 | the loops below and direct stores | 40 calls |
| `0x02EA1B50` | 3 vectors | `0x00737740`, `0x00737A30` | `0x0073792C`, `0x00737C86` |

`0x00789D50`, the setter, adds 1 to `0x02EA40B8` and the vector count to `0x02EA40BC`, then calls the effect it wraps
(`+0xE0`) at slot `+0x58`. That is `CTinyEffect` `0x0078FCF0`, which copies the smaller of the count and the
parameter's size, in 16-byte vectors, with `memcpy`¹. Nothing reads `0x02EA40B8` or `0x02EA40BC` except
their own adds.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0078FD45` |

</details>

`0x0078FCF0` answers `0x80070057` and copies nothing when its second argument minus 1 is negative or not below the
number of pointers between `+0xD0` and `+0xD8`, or when the dword `+0x20` of the parameter that pointer names is not 2¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0078FCF4`-`0x0078FD27`, `0x0078FD51` |

</details>

Otherwise the copy, a `memcpy` through the import thunk, `0x00861EBA(destination, source, length)`, takes its source
from the function's third argument¹, goes to the address in the parameter's `+0x50`, is
`[0x01F3D9F4] × min(count, s)` bytes long with `s` the parameter's dword `+0x30`, and `0x0078FCF0` answers 0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0078FCF7`, `0x0078FD42` |
| ² | `0x0078FD29`-`0x0078FD4A` |

</details>

`0x00789900`, the constructor, first runs the base constructor `0x00784E80(this)`¹, then stores the vtable
`0x00DAF1B8` at `+0x00`², 0 in the four qwords `+0xC8` to `+0xE0`³ and `0xA` in the
dword `+0x10`⁴, and returns the object. The getter `0x0072F920` returns the address of buffer A, `0x02EA1A50`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00789909` |
| ² | `0x00789915` |
| ³ | `0x0078991A`-`0x0078992F` |
| ⁴ | `0x00789939` |

</details>

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
| B | `0x00734EB0` | copies the first vectors (`0x00734F30`-`0x00734F41`), then stores the later ones less the first (`0x00734FF0`-`0x007351B2`); zeros fill each part (`0x00734F50`-`0x00734F8F`, `0x007351C1`-`0x007351FF`) |
| B | `0x00774260`, `0x00777590`, `0x007788A0` | through `0x0072F910`, which returns `0x02EA1C50` (`0x00774AD6`-`0x00774B5E`; `0x00777AE4`-`0x00777CFD`; `0x00778D31`-`0x00778D40`) |

`0x00734EB0` uploads one vector list in two parts. It takes a count, the vectors, a second count (0 stands for the
first, `0x00734ED9`-`0x00734EE4`) and a limit. The first part is `min(count, limit)` vectors copied to `0x02EA1C50` as they
are, or as many zeros when no vectors are given, with zeros after them up to `min(second count, limit)`; that many
vectors are uploaded through slot `+0x98` of the effect `+0x38` under the handle `+0xFC`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00734F14`-`0x00734FA5` |

</details>

The second part starts at `0x02EA1C50` again: the `max(count - limit, 0)` vectors from vector [limit] on, each stored
less vector [0] of the list, float by float¹, or as many zeros when no vectors are given², with zeros after them up to `max(second count - limit, 0)`. That many vectors are uploaded
under the handle `+0x100` by a jump to the same slot, whose answer is thus the function's (`+0x98` again;
`0x007351D2`-`0x00735231`). A second count not above the limit makes that an upload of 0 vectors.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00734FAE`-`0x007351B2` |
| ² | `0x007351B6`-`0x007351D0` |

</details>

`0x0073AC70` is a weighted draw of 1 to 8 source textures; any other count answers `0x80004001`¹. Its technique is a dword of a table in the object, at index `count × 0x16 + v`, with `v` its fifteenth
argument²: the table `+0x1B348`, or `+0x1B608` when a remap pair, its twelfth argument, is
given whose first float is not 0; an entry of 0 falls back to the tables `+0x1ADC8` and `+0x1B088`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0073ACA2`-`0x0073ACA8`, `0x0073B13B` |
| ² | `0x0073ACEA`-`0x0073ACF9` |
| ³ | `0x0073ACD6`-`0x0073AD27` |

</details>

It sets the technique through slot `+0xD0` of the effect `+0x38`¹ and hands the textures to slot `+0xB0`
under the handle `+0x150`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0073AD39` |
| ² | `0x0073AD57` |

</details>

The weights go to `0x02EA1A50`: the caller's vectors, its thirteenth argument, when given, else `1.0 / count` in all
four floats of each tap¹. Vector [count] is their sum, float by float²,
and count + 1 vectors are uploaded through slot `+0x98` under the handle `+0x108`³. An extra texture, when
given, is bound through slot `+0xB8` under the handle `+0x40`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0073AD74`-`0x0073ADDB` |
| ² | `0x0073ADE9`-`0x0073AF7C` |
| ³ | `0x0073AF92` |
| ⁴ | `0x0073AFA8`-`0x0073AFB7` |

</details>

Its sixth to ninth arguments are a rectangle `x0`, `y0`, `x1`, `y1`. `0x02EA1C50` takes `(x1 - x0) × 0.5`,
`-(y1 - y0) × 0.5`, `x0 + (x1 - x0) × 0.5` and `y0 + (y1 - y0) × 0.5`¹. With a remap pair
`p`, `q` whose `p` is not 0 a second vector follows: `u = p / 0.99609375`, `v = q - 0.00390625`, `1.0 / u` and
`-(v / u)`². One vector, or two in that case, is uploaded through slot `+0x98` under the handle
`+0x118`³; with no pair or `p` = 0 there is no second vector.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0073AFBD`-`0x0073B028` |
| ² | `0x0073B030`-`0x0073B07A` |
| ³ | `0x0073B093`-`0x0073B0A1` |

</details>

`0x0073AC70` then sets the 16 bytes at `0x00DA5E90` (the floats 1.0, 1000.0, 0, 0) under the handle `+0xDC` through slot
`+0x88`¹ and ends in
`0x00732D80(object, its first three floats, its fifth argument, -1.0, 1.0, 1.0, -1.0, its last argument)`, whose answer
it returns².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0073B0C5` |
| ² | `0x0073B10C` |

</details>

`0x0073B5A0` is the same weighted draw of 1 to 8 taps with the rectangle handed on to the draw; any other count answers
`0x80004001`¹. It binds no list of textures: the count is that of the weight
vectors. It asks `0x0075B260(this, count, byte, w > 0, 1, 1, dword)` for the technique, the byte and the dword being
arguments of its own and `w` its stack float, and sets it through slot `+0xD0`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0073B5D5`-`0x0073B5DB`, `0x0073BB1D` |
| ² | `0x0073B5E1`-`0x0073B641` |

</details>

It stages the weights and their sum in `0x02EA1A50` as `0x0073AC70` does and uploads count + 1 vectors through slot
`+0x98` under the handle `+0x108`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0073B659`-`0x0073B8BE` |

</details>

It then uploads five vectors from `0x02EA1C50` through slot `+0x98` under the handle `+0x10C`¹.
Vector 0 is the 16 bytes `a` its first pointer argument names; vector 1 is `p0 × a0`, `p1 × a1`, `p0 × a2`,
`p1 × a3` for the pair `p` its second pointer names. Vector 2 is `p0`, `p1`, a stack float and `w`; vector 3 is two
more stack floats and two zeros. Vector 4 is `2.0 / (x1 - x0)`, `2.0 / (y1 - y0)`, `-1.0 - x0 × 2.0 / (x1 - x0)` and
`-1.0 - y0 × 2.0 / (y1 - y0)`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0073B8C4`-`0x0073BA2B` |

</details>

An optional texture object has its slot `+0x70` called and the dword answered kept, its slot `+0x68` called with 4,
and is bound through slot `+0xB8` under the handle `+0x40`; a second optional texture is bound under `+0x44`¹. The draw is
`0x00732D80(object, the first three floats, the fifth argument, x0, y0, x1, y1, the last argument)`²;
afterwards slot `+0x68` of the first texture is called with the kept dword³, and the draw's
answer is returned.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0073BA3C`-`0x0073BA86` |
| ² | `0x0073BACF` |
| ³ | `0x0073BAF8`-`0x0073BB05` |

</details>

### Columns of yebis-ppfx-post-effects-constant-uploads.tsv

| Column | Holds |
|---|---|
| `count_set_at` | the address of the instruction that writes the vector count into `r9d`, the setter's fourth argument, before the call at `site`: a `mov` on 59 of the 67 rows, `lea` on 5, and `add`, `cmovl` and `sar` on one each. It lies in the same function, 4 to 336 bytes before the call |

### Lookup tables built on first call

Four converters fill a small `i32` table the first time they run, set a flag and return the entry their argument
indexes:

| Function | Table | Flag | Entries | Called at |
|---|---|---|---|---|
| `0x00714040` | `0x02EA1498` | `0x02EA14BC` | 0, 1, 10, 2, 4, 6, 8, 14, 1 | `0x0071410B` (`0x007140C0`, the HDR encoding code), `0x006F27BF`, `0x006FABC5`, `0x0070C76A` |
| `0x00713DF0` | `0x02EA14C0` | `0x02EA14E0` | 0, 1, 2, 3, 4, 5, 5, 5 | `0x00702779` (`CPostEffect::Initialize`) |
| `0x00713EB0` | `0x02EA14E8` | `0x02EA14FC` | 0, 0, 2, 6, 6 | `0x00702770` (`0x006FF900`), `0x00711393`, `0x00711431` |
| `0x00713F60` | `0x02EA1550` | `0x02EA1588` | 0 to 13 | `0x006FAE5B` (`0x006F9030`), `0x0070768D` (`0x00707670`) |

`0x00713EB0` is `GetEffectDofEdgeQualityTypeFromEdgeQualityType`: above 4 it logs "Unsupported EPFX_DOFEDGEQUALITY"¹, and -1 returns `0x10000000`. `0x00713F60` returns -1 for -1.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00D90AE0` |

</details>

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

`0x007091B0` leaves through a jump to `0x00729870(dword +0x44 of its second argument)` when its third argument is set, or
when that dword is `0x14`, `0x28`, `0x2D` or `0x37` (the mask `0x80210000100000`, `0x007091B0`-`0x007091D0`,
`0x00709256`-`0x00709259`). Otherwise it takes the dword `+0x470` of the object, or 3 when its fourth argument is set, as
the index into the four-entry table `0x02EA1510` and returns the entry when that is 0 to 3 and -1 for any other value¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007091D6`-`0x00709255` |

</details>

`0x006FE7F0` hands the effect pass two colour matrices through its last two out-parameters¹: the matrix at `+0x7A4` when the byte `+0x924` is set and the one at `+0x7E4` when `+0x925` is set,
otherwise 0². Two statics, each behind a thread-safe static guard³, can stand in for them:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006FEC8D`, `0x006FECA4` |
| ² | `0x006FE97D`-`0x006FE999` |
| ³ | `0x02EA15E0`, `0x02EA1630`; `0x008092FC`, `0x0080929C` |

</details>

- It copies the matrix at `+0x92C`, composed with the colour-space conversion when `+0x96C` differs from
  `+0x970`¹. When the copy is not the identity², it is stored at `0x02EA15A0`,
  multiplied by the `+0x7E4` matrix when there is one (the 4×4 product `0x006F1070`), and becomes the second
  out-parameter³.
- The second static, `0x02EA15F0`, would be filled the same way from a matrix built as the identity on the stack
 ⁴. The identity test always passes, so its stores⁵ never run, it
  stays 0, and the first out-parameter is passed on as it was.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006FEA23`-`0x006FEA64` |
| ² | `0x007124B0` |
| ³ | `0x006FEA97`-`0x006FEAD2` |
| ⁴ | `0x006FEB37`-`0x006FEB8A` |
| ⁵ | `0x006FEBA5`-`0x006FEBC4` |

</details>

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

`TEXSHADERSET::CreateEffect`¹ looks up its techniques by name. Five helpers keep tables of name
suffixes, filled once while a flag byte (1 in the image) is set; each walk appends every suffix to the base name and
looks the technique up:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0072A320` |

</details>

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
only when the count after the add is 0 or leaves 100 when divided by 200, `c == 0 || c % 200 == 100` with
`c = [0x02EA404C] + 1` (a signed division, `0x007732E7`-`0x00773314`), and only while `0x01F3BA80` and `0x01F3BA8C` are both
at least 1 (unsigned compares, `0x00773316`-`0x00773326`).

### Glare definitions and colours

`CRenderGlare`'s constructor `0x007687E0` runs the base constructor `0x00727200(this, 0)`¹, stores the vtable
`0x00DA8420` at `+0x00`² and its member defaults, and allocates the one-byte definition object through
`0x006DA880([0x01F3BA68], 1, 0x00DA7960, 0x118, 0)` (source line 280). When that allocation answers it runs `0x0075F160()` and
`0x0075F960()`; it stores the pointer, or 0, in `0x02EA3D50`³. It ends with
`0x007603E0(object, its second argument)`⁴ and returns the object.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00768802` |
| ² | `0x0076880F` |
| ³ | `0x00768919`-`0x00768951` |
| ⁴ | `0x0076895E` |

</details>

The member defaults¹ are 0 in the qwords `+0x38` and `+0x40`, the dword `+0x48`, the byte
`+0x4C`, the six qwords `+0x50` to `+0x78`, the three qwords `+0x9C` to `+0xAC`, the dword `+0xB4`, the byte `+0xB8`,
the six qwords `+0xBC` to `+0xE4` and the qword `+0x108`. At `+0x80` and again at `+0xEC` stands a block of the same
shape: the word `0x0101`, a 0 byte at the block's `+0x02`, the dword 1 at `+0x04`, a 0 byte at `+0x08`, the dword 2 at
`+0x0C`, a 0 byte at `+0x10`, the dword 1 at `+0x14` and a 0 word at `+0x18`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00768814`-`0x0076890D` |

</details>

The glare code builds its look tables from two `.data` row lists when `CRenderGlare`'s constructor¹
allocates the definition object `0x02EA3D50`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007687E0` |

</details>

- `0x02EA3D40`: the star-line types, from the seven rows at `0x01F3CF20` (Disable, Cross, CrossFilter, SnowCross,
  SunnyCross, Vertical, Anamorphic), built by `0x0075F160`.
- `0x02EA3D48`: the glare types, from the 14 rows at `0x01F3D000` (Disable, Bloom, Lens Flare, Standard, Cheap Lens
  Camera, Afterimage, the cross filters and the streaks), built by `0x0075F960`, which does nothing when the pointer is
  already set¹ and returns 0 either way.
- Otherwise `0x0075F960` runs `0x0075F160()`² and allocates `0x628` bytes through
  `0x006DA880([0x01F3BA68], 0x628, 0x00DA6F38, 0x28C, 0)`³: the number 14 in the first qword, then 14
  records of `0x70` bytes, in each of which it stores 0 in the qwords `+0x00`, `+0x08`, `+0x18`, `+0x28`, `+0x38` and
  `+0x48` to `+0x68` and in the dword `+0x30`⁴.
- It stores the first record's address in `0x02EA3D48`, or 0 when the allocation answered null⁵,
  and in both cases calls `0x0075FC50(record k, row k)` for the 14 rows of `0x38` bytes, record k being at
  `[0x02EA3D48] + 0x70 × k`⁶.
- `0x0075F160` also writes two colour orders for the lines: `0x02EA3D60` white, red, green, blue and `0x02EA3DA0` white,
  blue, green, red. `0x00764240` picks one⁷ and hands it to the effect⁸.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0075F964`-`0x0075F96C` |
| ² | `0x0075F981` |
| ³ | `0x0075F9A6`-`0x0075F9B1` |
| ⁴ | `0x0075F9B7`-`0x0075FA0F` |
| ⁵ | `0x0075F9B3`, `0x0075FA11` |
| ⁶ | `0x0075FA18`-`0x0075FA40` |
| ⁷ | `0x007644C3` |
| ⁸ | `0x00764FA1` |

</details>

The destructor `0x007693B0` frees both tables and the object¹. `0x00707670` copies a glare type
by index, but the thunk `0x006DBA00`, which jumps to it, is referenced by no instruction or table.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0075FA60`, `0x0075F390` |

</details>

For an index (its third argument) from 0 to 13, compared unsigned, and a non-null output (its second), `0x00707670`
takes the `0x70`-byte record `[0x02EA3D48]` + `0x00713F60(index)` x `0x70` and copies 18 fields into the output's
`+0x00`-`+0x44`, returning the output pointer; otherwise it returns 0¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00707677`-`0x00707728` |

</details>

`0x0075B2F0` returns a seven-entry hexagon pattern built once (flag `0x02EA3D24`): `0x02EA3CB0` is (0, 0, 0, 0) and
entry *i* + 1 is (-sin 60*i*°, cos 60*i*°, 0, 0) for *i* = 0 to 5.

`0x00769640` is slot 3 (`+0x18`) of the `PPFX::CRenderGlare` vtable `0x00DA8420`: it gives back what the glare
renderer created on the device. It first calls `0x007142F0`, whose result it keeps, and `0x00714560`¹, and then:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00769660`-`0x00769668` |

</details>

- for each of the thirteen objects at `+0x238`, `+0x280`, `+0x288`, `+0x290`, `+0x298`, `+0x210`, `+0x248`,
  `+0x250`, `+0x258`, `+0x2A0`, `+0x2B0`, `+0x2A8` and `+0x260` that is not null it calls the object's slot `+0x20`
  with 0, frees it through the library allocator (`0x006DA8A0` on `[0x01F3BA68]`) and clears the field
 ¹;
- it frees the array at `+0x1C8` and clears the field²; this free and every array or block
  free below starts 8 bytes before the stored pointer;
- it releases each non-null entry of the pointer array at `+0x270`, whose count is the dword `+0xF0`, the same
  way, then frees that array and the one at `+0x278`³;
- it does the same for the entries of the array at `+0x230`, whose count is the dword `+0xD0`, and frees it and
  the array at `+0x240`⁴. The `+0x270` pass is skipped when that pointer is null
 ⁵ and compares its count unsigned⁶; this pass reads the count signed⁷
  and indexes `+0x230` without a null test⁸;
- for a non-null block at `+0x220` it calls `0x0075E690` with the qword `+0x22248` of the first call's result,
  the dword `+0x228` and the block, frees the block and clears both fields⁹;
- it ends with `0x007604A0` and `0x00727450` on the renderer and returns the latter's result when that is negative,
  else 0¹⁰. `0x00727450` is `xor eax, eax` and `ret`, so the result is 0 every time.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0076966D`-`0x007698FC` |
| ² | `0x007698B0`-`0x007698CC` |
| ³ | `0x00769903`-`0x007699A1` |
| ⁴ | `0x007699A8`-`0x00769A53` |
| ⁵ | `0x0076990A` |
| ⁶ | `0x00769914` |
| ⁷ | `0x007699A8` |
| ⁸ | `0x007699C0`-`0x007699C7` |
| ⁹ | `0x00769A5A`-`0x00769A9B` |
| ¹⁰ | `0x00769AA1`-`0x00769AB6` |

</details>

`0x0077E0B0` is slot 3 of the `PPFX::CDepthOfField` vtable `0x00DABD60` and does the same for the depth of field. A
counted object below is dropped: 1 is taken off its dword `+0x08` and, at 0, its slot `+0x20` is called with 0
and it is freed; the field is cleared either way¹. After the same two calls²:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0077E19B`-`0x0077E1BF` |
| ² | `0x0077E0C7`-`0x0077E0D4` |

</details>

- for each of the `+0xDC` records of `0x108` bytes in the array at `+0x4B8`, it hands the record's `+0x38` to
  `0x0075E7C0` on the object at `+0x4B0` when the record's byte `+0x40` is 0¹;
- it hands the record's blocks `+0x68` and `+0x78`, with the counts `+0x60` and `+0x70`, to `0x0075E690` and frees
  them²;
- it drops the record's counted objects: `+0xA0` and `+0xA8` while the effect's byte `+0x130` is 0, else `+0x80`,
  `+0x88`, `+0x90` and `+0x98`, with `+0xA0` and `+0xA8` cleared undropped; the `+0x18C` entries from `+0x48`; and
  `+0xB0` and `+0xB8`³;
- it drops the counted object at `+0x258`⁴;
- for each of the `+0x300` entries of the four array pairs at `+0x308 + 8k` and `+0x328 + 8k`, `k` from 0 to 3,
  it calls the entry's slot `+0x08` and clears it; it frees the twenty arrays at `+0x308` to `+0x3A0`, clears the
  count and frees the array at `+0x3A8`⁵;
- it calls slot `+0x08` of the objects at `+0x268`, `+0x270`, `+0x290`, `+0x298` and `+0x3B0` and clears the
  fields⁶;
- it does the per-entry call for the `+0x2D0` entries of the arrays at `+0x2D8` and `+0x2E0`, and frees those and
  the arrays at `+0x2E8`, `+0x2F0` and `+0x2F8`⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0077E100`-`0x0077E11B` |
| ² | `0x0077E120`-`0x0077E17E` |
| ³ | `0x0077E182`-`0x0077E3D8` |
| ⁴ | `0x0077E3DE`-`0x0077E40E` |
| ⁵ | `0x0077E415`-`0x0077E531` |
| ⁶ | `0x0077E538`-`0x0077E5AE` |
| ⁷ | `0x0077E5B7`-`0x0077E6C8` |

</details>

The last group has the dword `+0x408` as its count `n`, and the body skips its loop when `n` is 0¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0077E6CF`-`0x0077E6E3` |

</details>

- it drops entries 0 to `n` of the array at `+0x440`, one more than the count¹;
- for entries below `n` it calls slot `+0x08` of the entries of `+0x420` and `+0x428`, and drops the counted
  entries of `+0x448`, `+0x450`, `+0x458`, `+0x460`, `+0x478`, `+0x480` and, when that array is not null,
  `+0x498`²;
- it frees the eighteen arrays at `+0x410` to `+0x498` and clears the count³;
- it frees the record array `+0x4B8`, calls slot `+0x20` of the object at `+0x4B0` with 0 and frees it, hands
  the block `+0x4A0` with the count `+0x4A8` to `0x0075E690` and frees that⁴;
- it ends with `0x0076BFA0` and `0x00727450` on the effect and returns the latter's result when that is negative,
  else 0⁵; `0x00727450` always answers 0, so this result is 0 too.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0077E6F0`-`0x0077E72B`, `0x0077E93B`-`0x0077E94B` |
| ² | `0x0077E72F`-`0x0077E937` |
| ³ | `0x0077E951`-`0x0077EBCE` |
| ⁴ | `0x0077EBC7`-`0x0077EC62` |
| ⁵ | `0x0077EC68`-`0x0077EC82` |

</details>

### Constant colours and the allocator's map

- Three draws keep the colour (1, 1, 1, 1) in a guarded lazy static: `0x02EA2480`¹, `0x02EA3FF8`
 ² and `0x02EA4010`³.
- The game's allocator `0x02E5BDE0` counts its live allocations at `+0x08`⁴ and their bytes at `+0x10`
 ⁵. It maps each address to its size, file and line in a red-black tree headed at `+0x18`
 ⁶. The head is also the nil node that leaf links point to; `+0x30`⁷ holds the root, and
  `+0x30` to `+0x40` stand in as the root's parent.
- The initialiser `0x00167990` stores the head's address in all six words. Inserts⁸, rebalancing
 ⁹ and erases¹⁰ rewrite the root and the nil node's parent word¹¹, and
  read the second link and the colour bit of the root's parent position¹².
- `0x01F3C500` lets `0x006F1270` fill the eleven maximum vectors at `0x02EA13C0` once.
- `0x02EA17B0` is the text `0x0071B070` builds for the texture-creation log lines. It empties the text¹³,
  appends `GPUUSAGE_RENDERTARGET` for bit `0x1` of its first argument and `GPUUSAGE_DEPTHSTENCIL` for bit `0x2`, with
  ` | ` between them when both are set, and returns the text's address¹⁴.
- With its second argument, a byte, set, `0x0071B070` appends the short forms `RT` and `DS` in their place, with `|`
  between them. Each piece is written at the text's end by `0x0017D2E0(end, format, name)`¹⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00748C00` |
| ² | `0x00764240` |
| ³ | `0x00763890` |
| ⁴ | `0x02E5BDE8` |
| ⁵ | `0x02E5BDF0` |
| ⁶ | `0x02E5BDF8` |
| ⁷ | `0x02E5BE10` |
| ⁸ | `0x006CBA20` |
| ⁹ | `0x0067F700`, `0x0067F9D0` |
| ¹⁰ | `0x0067FE20` |
| ¹¹ | `0x02E5BE08` |
| ¹² | `0x02E5BE18`, `0x02E5BE20` |
| ¹³ | `0x0071B086` |
| ¹⁴ | `0x0071B09D`-`0x0071B160` |
| ¹⁵ | `0x0071B0EA`, `0x0071B156` |

</details>

</details>

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 4 calls with 3 other topics</summary>

**Developer** (explained on [game application](../Engine-Core/game-application.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00796E20`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | is called by | [`0x001C2F50`](../Game-Files-And-Data-Tables/standard-file-formats.md) (on standard file formats) |

**Steam and achievements** (explained on [steam integration](../Steam-And-Achievements/steam-integration.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00796E20`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | is called by | [`0x008655A0`](../Steam-And-Achievements/steam-integration.md) (on steam integration) |

**Saving, loading and settings** (explained on [debug logging](../Engine-Core/debug-logging.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001A5500`](yebis-ppfx-post-effects.md) | is called by | [`0x001DE5D0`](../Saving-Loading-And-Settings/game-settings.md) (on game settings) |
| [`0x001A5630`](yebis-ppfx-post-effects.md) | is called by | [`0x001DE5D0`](../Saving-Loading-And-Settings/game-settings.md) (on game settings) |

</details>
