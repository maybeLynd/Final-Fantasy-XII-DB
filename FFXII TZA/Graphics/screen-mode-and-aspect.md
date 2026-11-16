---
title: "Screen mode and aspect: the aspect fit, the Super Wide bound and the display object"
kind: "system"
category: "Graphics"
addresses: "0x001DDBA0, 0x001DDAC0, 0x001DDAB0, 0x01F82D18, 0x001DD120, 0x001DD8C0, 0x001DCE20, 0x0017FFD0, 0x00186B80, 0x00229D20, 0x001DC730, 0x001DD420, 0x001DD8E0, 0x001DC5C0, 0x001DDA70"
---

## What the player sees

On a window or screen of 16:9 or narrower the game shows a 16:9 picture, which the engine calls
Normal Mode. On a wider display it switches to Super Wide Mode: the 3D scene widens to the real
shape of the display, while full-screen overlays keep 16:9 proportions in the middle. The widest
shape the game describes is 48:9 (16:3); past that the width it uses is clamped. The mode name the
developer display prints is "Super Wide Mode" or "Normal Mode".

## How it works

### Setting a resolution

`0x001DDBA0(display, w, h)` is the only way into the fit. It stores the size in the settings object
`[0x01F82D20]` (see [game settings](../Saving-Loading-And-Settings/game-settings.md)) and then fits it:

1. With ScreenMode (setting 2, `+0x08`) at 0, windowed, it stores `w << 16 | h` as WindowSize
   (setting 11) through `0x001DF340` (`0x001DDBD3`), rebuilds the window-size list (`0x001DD8E0`,
   `0x001DDBDB`) and calls `0x0017DB80`; otherwise it stores the same word as Resolution (setting 1,
   `0x001DDBEC`).
2. It writes `GameSetting.ini` (`0x001DFD40`, `0x001DDBF8`).
3. It logs `[Screen Mode]setResolutionSize w = %d ,h = %d Screen Mode = %d` (`0x00900910`) with
   ScreenMode, and tail-jumps to the fit `0x001DDAC0` with the same three arguments (`0x001DDC39`).

The setter is reached through `0x00182F70(w, h)`, which fetches the display object, and from
`0x001DC730`. Its callers are the application start-up (`0x0017CEB0`, with the start-up size), the
window-event handler `0x007A3C10` (event 0, a packed new size), the screen-mode switch `0x007A3E00`
(the monitor rectangle or the desktop size), and `0x001DC730`, which applies the selected entry of
the window-size list in windowed mode and of the display-mode list otherwise, then stores the
mode's refresh rate (`0x001DC76F`).

Both lists hold `0x1C`-byte entries with the width at `+0x00` and the height at `+0x04`. In windowed
mode (the display object's `+0x18` is 0) `0x001DC730` takes entry `+0x38` of the list at `+0x40`,
otherwise entry `+0x24` of the list at `+0x28`, and calls `0x001DDBA0(object, width, height)`
(`0x001DC736`-`0x001DC76A`). The rate it then stores at `+0x30` is the display-mode entry's dword `+0x08`
over its dword `+0x0C`, unsigned; it is taken from entry `+0x24` of the list at `+0x28` in
both modes (`0x001DC76F`-`0x001DC784`).

The division is made with no test for a dword `+0x0C` of 0 (`0x001DC780`). The body ends in a jump to
`0x007A04F0` (`0x001DC78C`).

`0x001DC730` then tail-jumps to `0x007A04F0` (`0x001DC78C`), which queues request 1 with
the WindowSize (windowed) or the Resolution on the game window's `+0x48` queue (`0x007A3BD0`, `0x007A0530`;
[Phyre application](../PhyreEngine/phyre-application.md)).

### The fit

`0x001DDAC0(record, W, H)` first stores `W` at `+0x10` and `H` at `+0x14` and computes
`ratio = W / H` as floats (`0x001DDAEC`). It compares the ratio with `16/9` (`0x008C5B38`) and `16/3`
(`0x00900A0C`):

| Ratio | Branch | Mode `+0x00` | Size | `+0x04` / `+0x08` / `+0x0C` |
|---|---|---|---|---|
| up to 16:9 | `0x001DDAF5`-`0x001DDB18` | 0 | height becomes `(int)(W / (16/9))` | 1.0, 1.0, 0 |
| above 48:9 | `0x001DDB26`-`0x001DDB52` | 1 | width becomes `(int)(H × 16/3)` | 1.0, 1.0, 0 |
| between | `0x001DDB53`-`0x001DDB9E` | 1 | kept | see below; `+0x08` not written |

The middle branch divides integers: `+0x04 = (float)(W − H / W)` (`div` at `0x001DDB63`) and
`+0x0C = (float)((W − H) / W) × 0.5` (`0x001DDB7D`, constant `0x01CEBB70`). In this branch `W` is
always greater than `H`, so both quotients are 0: `+0x04` receives the width in pixels and
`+0x0C` receives 0. Nothing reads these three fields (see below), so the values have no effect.
`+0x08` holds 1.0 from the constructor (`0x001DC5C0`) and every branch that writes it writes 1.0.

### Who reads the fit

The fit is read through the getter `0x001DDAB0` (`mov rax, [0x01F82D18]`). The readers take the
mode and the fitted size:

- `0x001DD8C0` answers `mode == 1` (Super Wide); its second test `0x005C5230` returns 0. The wrapper
  `0x00182F50` serves it to six callers.
- `0x001DD120` returns the aspect: `(float)W / (float)H` from `+0x10` / `+0x14` in mode 1, and the
  constant 16/9 otherwise (`0x001DD126`-`0x001DD164`). `0x00182EE0` wraps it. In mode 1 it first calls
  the same second test `0x005C5230` (`0x001DD12E`) and takes the 16/9 at `0x008C5B38` when that answers
  non-zero; `0x005C5230` is `xor eax, eax; ret`, so mode 1 always gives the ratio. `W` and `H` are
  converted as unsigned 32-bit values (`0x001DD137`-`0x001DD148`).
- `0x00225680` and `0x002256A0` return `+0x10` and `+0x14`; `0x00182440` returns the mode word.
- `0x001DCE20` writes "Super Wide Mode" (`0x00900960`) for mode 1, else "Normal Mode" (`0x00900970`),
  into the object's `+0x80` through `0x001A1E40` (`0x001DCE26`-`0x001DCE43`); the developer console
  `0x001CD0E0` prints it.

A sweep of every function that reaches the object through the getter or `0x01F82D18` directly,
and of every function the object is passed to, finds no read of `+0x04`, `+0x08` or `+0x0C`
outside the fit and the constructor.

### What the aspect drives

- The renderer's projection: `0x00229D20` returns 4/3 unless the frame-mode byte `0x02064AD1` is 1, 2,
  3 or 5, and then the display object's aspect through `0x00182EE0`; the camera update stores it at
  `0x02AED4E0` and builds the projection with it ([scripted camera](scripted-camera.md)).
- The 16:9 scale factor: `0x0017FFD0` returns `0x001DD110()` (the constant 16/9) divided by the aspect,
  so 1.0 in Normal Mode and below 1.0 in Super Wide Mode. Its callers multiply horizontal
  positions by it; the full-screen quad `0x001D8B20` spans `±factor` across, keeping a 16:9 quad
  centred on a wider screen.
- With no display object (`0x001DDAB0` returns 0), `0x0017FFD0` divides the 16/9 at `0x008C5B38` by 0.0,
  `16/9 ÷ 0`, and returns positive infinity while the divide-by-zero exception is masked, which the body
  does not change (`0x0017FFF5`, `0x00180025`-`0x00180028`).
- The viewport: `0x00186B80` in Normal Mode (`0x00182F50` false) sets the viewport width to 16/9 of
  the height it is given and centres it on the given rectangle; in Super Wide Mode it uses the
  rectangle as given. The width is `w - (int)(w - h × 16/9)` and the left edge moves right by
  `(int)(w - h × 16/9) / 2` (`0x00186C48`-`0x00186C87`), both through the viewport setter `0x0060F6B0`.
- Before that, `0x00186B80` returns at once when the render manager has no device at `+0x08`
  (`0x00186BA6`). It sets a viewport over the whole target, 3,840 × 2,160 while the boot byte `+0xDB8`
  is set or `+0xC30` is 3 and `+0xAD8` × `+0xADC` otherwise (`0x00186C01`), posts the clear colour
  0, 0, 0, 0 (`0x0060D190`, `0x00186C19`), and opens the colour bracket with `0x005FEFD0(device, 1)` and
  closes it with `0x00600A60(device, 0)` (`0x00186C27`, `0x00186C32`).

- The 16:9 in that viewport comes from `0x00182E50`, which returns `0x001DD110()` when the display
  object exists and the same constant 16/9 when it does not.
- The window offset: each frame the render pass list `0x00187950` stores at render-manager `+0xDA0`
  and `+0xDA4` the offset that centres the fit size (`0x00182EB0`, `0x00182E80`: `+0x10` and `+0x14`,
  or 1920 × 1080 without a display object) in the window size (`+0xD24`, `+0xD28` of
  `0x00796E20()`).
- `0x001EE5D0` gives that offset: 0, 0 for equal sizes, half the width difference when the fit is
  narrower in aspect, otherwise half the height difference, made positive. The colour-buffer copy
  `0x001EE8E0` hands the offset to `0x00186B80`.

- The frame-mode zoom: `0x00229D60` returns 1.1547 for frame mode 2 (`0x02064AD1`), 4/3 for mode 3,
  1.0966 for mode 5 and 1.0 otherwise. The projection builder `0x003CBB30` multiplies the scale
  `1 / tan(fov / 2)` by it on both axes, and the camera update passes it to the renderer
  (`0x00182640`). `0x00229DA0(mode)` returns the same values for a given mode; `0x00247AE0` and
  `0x0029CF30` call it with 2.

### The display-mode list

The constructor `0x001DC5C0` first stores its defaults (`0x001DC5C6`-`0x001DC630`): mode 0, `+0x04` and `+0x08`
1.0, `+0x0C` and the fitted size 0, one display mode (`+0x20` 1, `+0x24` 0), 60 Hz at `+0x30`, `+0x34` 1,
`+0x50` 1, zero at `+0x1C`, `+0x28`, `+0x38`, `+0x40`, `+0x48`, `+0x4C`, `+0x54`, `+0x58`, `+0x5C` and
`+0x78`, the settings' `+0x68` (Monitor) at `+0x60` and the settings' `+0x08` (ScreenMode) at `+0x18`.

It then calls `0x001DD170` (`0x001DC636`), which enumerates the adapters into a table
of `0x140`-byte entries at `+0x78` (count `+0x50`), takes `+0x4C` as the adapter `+0x48`, and stores that
adapter's DeviceID and LUID halves (entry `+0x104`, `+0x128`, `+0x12C`) as settings 19, 20 and 21 through
`0x001DF340` (`0x001DD384`, `0x001DD3AC`, `0x001DD3D4`).

It then calls `0x001DD420` (`0x001DC63E`), which enumerates the outputs of the adapter
(`IDXGIAdapter::EnumOutputs`, vtable `+0x38`) and asks each for its modes with
`IDXGIOutput::GetDisplayModeList` (vtable `+0x40`) in format 28, `R8G8B8A8_UNORM` (`0x006242C0`).
Each 28-byte entry is a `DXGI_MODE_DESC`. The list keeps a mode only when:

- it is at least 1280 × 720 (`0x500` × `0x2D0`) and its refresh denominator is not 0;
- its refresh rate, numerator over denominator as a whole number, is 59 or 60 Hz, or with any FrameLimit but 1
  (the shipped 0 is 30 fps) also 29 or 30 Hz (`0x0017D8F0` reads FrameLimit).

It then sorts by width and height, keeps one entry per size, and selects the entry whose pixel
count is nearest the Resolution setting's. With no usable mode the list is one entry of the
Resolution size at 60/1 Hz.

### Switching the swap chain

`0x0079C140` keeps the swap chain in step with the chosen mode through three device functions:

- `0x00625F30(device)` answers 1 when the output's mode list changed: a different count (format 28, `+0x18A0`) or
  output (`+0x1898`) than the device kept (`0x0079C340`);
- `0x0062B250(device)` answers 0 only while the device is full screen (`+0x1890` = 1) and the swap chain reports it is
  not (`IDXGISwapChain::GetFullscreenState`, vtable `+0x58`; `0x0079C36F`);
- `0x00629690(device, w, h, full, hz)` sets the mode (`0x0079C444`), in the steps below, and returns 1 when both
  switches succeed.

1. It lists the output's modes and logs `[Screen Mode]number of modes: %d  pOutput = %x`.
2. It takes the mode of that size whose refresh rate is `hz`; when no mode matches it takes the last one, or fails in
   full screen.
3. It logs the mode id and the desktop refresh rate (`EnumDisplaySettingsA`).
4. It switches the full-screen state (`SetFullscreenState`, vtable `+0x50`) and resizes the target (`ResizeTarget`,
   `+0x70`), and logs `[Screen Mode]Full Screen Result : Target = %d , Mode = %d`.

`0x006278B0(device, w, h)` resizes the swap chain itself (`0x0062389D`, `0x007A0663`): it unbinds the targets (vtable
`+0x108`), releases the colour and depth views (`0x0062B890`), calls `ResizeBuffers` (`+0x68`) with the device's count
`+0x148` and format `+0x130`, takes buffer 0 again (`GetBuffer`, `+0x48`), rebuilds the views (`0x00620F60`) and the
viewport (`0x0061D3D0`, `0x00607D10`), and binds the targets again (`0x00627B67`-`0x00627BA6`), returning 0. It
returns `0x15` without a swap chain (`0x006278E3`-`0x006278FC`).

A failed `ResizeBuffers` skips to the rebind and still returns 0 (`0x0062799F`-`0x006279A1`). A null buffer 0
returns `0x15` (`0x006279D0`-`0x006279DD`), and a non-zero answer of `0x0062B890`, `0x00620F60` or `0x0060DD70` is
returned at once (`0x00627939`, `0x00627963`, `0x00627A8D`, `0x00627ABA`, `0x00627AE9`), both without binding the
targets again. A target's views are released only when it holds one (`+0x28` or `+0x18` non-zero) and
rebuilt only when it then holds none (`0x00627921`-`0x0062792D`, `0x00627A77`-`0x00627A81`).

### The window-size list

`0x001DD8E0` copies the display-mode list into the window-size list at `+0x40` with one spare entry,
looks for the WindowSize setting (`+0x2C` height, `+0x2E` width as 16-bit halves) and selects it;
when it is missing it writes it into the spare entry and sorts it into place by width, then height.
The windowed resolution row therefore always offers the current window size.

`0x001DD8E0` returns at once while the display-mode list `+0x28` is null (`0x001DD8EE`). When `+0x34`
differs from the mode count `+0x20`, it frees the old window list (`0x00210EB0`), sets `+0x34` to the
count and allocates `(count + 1) × 0x1C` bytes for it (`0x00210EC0`, `0x001DD8FC`-`0x001DD929`). It copies
`(+0x34 + 1) × 0x1C` bytes from `+0x28` (`memcpy`, `0x00861EBA`, `0x001DD93E`) and zeroes the spare
entry's width, height and refresh numerator and denominator (`0x001DD951`-`0x001DD980`). The search runs
over entries 0 to `+0x34`, the spare included, and stores the matching index at `+0x38` (`0x001DDA62`).

With no match it sets `+0x38` to the spare's index `+0x34` (`0x001DD9DD`) and walks entries 0 to `+0x34`
once, swapping each entry of greater width, or equal width and greater height, with the last entry
(`0x001DD9F7`-`0x001DDA3F`); the index of the first swap becomes `+0x38` (`0x001DDA48`).

## Layouts

The display object is 0x180 bytes, built once by `0x001DDA70` and constructed by `0x001DC5C0`; its
first 0x18 bytes are the fit record.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | mode | 0 Normal Mode, 1 Super Wide Mode (ctor 0) |
| `+0x04` | `f32` | fitA | 1.0 or the width (middle branch); no reader |
| `+0x08` | `f32` | fitB | 1.0; no reader |
| `+0x0C` | `f32` | fitC | 0; no reader |
| `+0x10` | `u32` | width | fitted width |
| `+0x14` | `u32` | height | fitted height |
| `+0x18` | `u32` | screenMode | ScreenMode at construction (setting 2) |
| `+0x20` | `u32` | modeCount | display-mode entries (ctor 1) |
| `+0x24` | `u32` | modeIndex | selected display mode |
| `+0x28` | `void*` | modes | DXGI_MODE_DESC[modeCount], `0x1C` each |
| `+0x30` | `u32` | refreshHz | numerator / denominator of the selected mode (ctor 60) |
| `+0x34` | `u32` | windowLast | last index of the window-size list |
| `+0x38` | `u32` | windowIndex | selected window size |
| `+0x40` | `void*` | windowSizes | `0x1C` entries, modeCount + 1 |
| `+0x48` | `u32` | adapter | selected adapter index |
| `+0x5C` | `u32` | outputCount | outputs of the adapter |
| `+0x60` | `u32` | monitor | selected output (ctor: setting 26, Monitor) |
| `+0x78` | `void*` | adapters | `0x140`-byte adapter records |
| `+0x80` | `string` | modeName | "Super Wide Mode" or "Normal Mode" (`0x001DCE20`) |

DXGI_MODE_DESC (`0x1C`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | Width |  |
| `+0x04` | `u32` | Height |  |
| `+0x08` | `u32` | RefreshRate.Numerator |  |
| `+0x0C` | `u32` | RefreshRate.Denominator |  |
| `+0x10` | `u32` | Format |  |
| `+0x14` | `u32` | ScanlineOrdering |  |
| `+0x18` | `u32` | Scaling |  |

## Shipped data

| Fact | Value |
|---|---|
| widescreen bound `0x008C5B38` | 1.7777778 (16/9) |
| super-wide bound `0x00900A0C` | 5.3333335 (16/3, 48:9) |
| half `0x01CEBB70` | 0.5 |
| mode names | "Super Wide Mode" `0x00900960`, "Normal Mode" `0x00900970` |
| aspect outside the frame modes 1, 2, 3, 5 | 4/3 (`0x3FAAAAAB`, `0x00229D20`) |

## Modding notes

- Only the mode and the fitted size reach the renderer; patching the middle branch's integer
  divides changes nothing on screen.
- To allow shapes wider than 48:9, raise the float at `0x00900A0C`; the clamp is the only limit.
- Display modes below 1280 × 720, or at a refresh rate other than 29, 30, 59 or 60 Hz, never
  appear in the display-mode list. The window-size list still adds the current WindowSize, which the
  settings parser keeps at 640 × 360 or more ([Game settings](../Saving-Loading-And-Settings/game-settings.md)),
  and with no usable mode the display-mode list is one entry of the Resolution size at 60/1 Hz.

## Related

- [Config screen](../Menus-And-HUD/config-screen.md): the Resolution, Screen Mode and adapter rows that
  call `0x001DC730`.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): Resolution, ScreenMode, WindowSize,
  FrameLimit and Monitor.
- [Global state accessors](../Engine-Core/global-state-accessors.md): the getter
  `0x001DDAB0`.
- [Scripted camera](scripted-camera.md): the projection the aspect feeds.
- [Script screen effects](script-screen-effects.md): screen quads that use the 16:9 factor.
