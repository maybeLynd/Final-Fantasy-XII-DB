---
title: "YEBIS and PPFX: the post-effect library, how the game starts and drives it, its licence check and the EnableYebis switch"
kind: "system"
category: "Third-party libraries"
summary: "Silicon Studio's YEBIS post-effect library (its core is named PPFX) as linked into the game: its address span and identity, the source paths and diagnostic log it carries, the API entry points, how the renderer creates its context and runs it each frame, the licence verifier and why the shipped licence never reaches its date test, and the EnableYebis switch with its delayed form."
addresses: ["006DA880", "006DA8A0", "006DA8F0", "006DAA50", "006DA990", "006DAA70", "006DE780", "006DFF40", "0071D9E0", "006FF900", "0070BA00", "00707560", "006DF480", "006CBD20", "006CBEA0", "00193DA0", "0018E470", "00194290", "00194A30", "001F3300", "00167990", "02E5BDE0", "02EA0B70", "02EA0B3C", "02EA0B90", "00D86C00", "00717760"]
---

# YEBIS and PPFX: the post-effect library, how the game starts and drives it, its licence check and the EnableYebis switch

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

### Start-up

1. The static initialiser `00167990` builds the game's allocator object `02E5BDE0` with the vtable
   of `Yebis::YebisPfxMemoryAllocatorD3D11`.
2. The renderer's start-up `006253D0` creates the integration object (`0065E5D0`, kept at
   `02D38540`) and marks it ready: `0065E580` (call at `0062549D`) sets its byte `+8` to 1.
3. The first frame that runs the pass calls `006CBD20` through `0065E5A0`; see the next section.

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

## Layouts

The render parameter block's switch fields (the block is `0x4A8` bytes; the rest is on
[Graphics settings](../Engine-Core/graphics-settings.md)):

```
+0x0A0  u8    the pass is on (constructor value 1)
+0x0A1  u8    the pending value of a delayed change
+0x1F0  i32   frames left before the pending value is applied
```

The library's global block, `0xD40` bytes at `[02EA0B70]`, as far as its constructor `006FF5D0`
lays it out:

```
+0x0A8  map header  built by 00714800
+0x0B8  map header  built by 007147A0
+0x0C8  map header  built by 00714740
+0xC80  ptr         cleared by the constructor
```

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
