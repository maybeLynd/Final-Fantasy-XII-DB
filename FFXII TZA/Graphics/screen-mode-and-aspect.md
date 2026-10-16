---
title: "Screen mode and aspect: the aspect fit, the Super Wide bound and the display object"
kind: "system"
category: "Graphics"
addresses: "001DDBA0, 001DDAC0, 001DDAB0, 01F82D18, 001DD120, 001DD8C0, 001DCE20, 0017FFD0, 00186B80, 00229D20, 001DC730, 001DD420, 001DD8E0, 001DC5C0, 001DDA70"
---

## What the player sees

On a window or screen of 16:9 or narrower the game shows a 16:9 picture, which the engine calls
Normal Mode. On a wider display it switches to Super Wide Mode: the 3D scene widens to the real
shape of the display, while full-screen overlays keep 16:9 proportions in the middle. The widest
shape the game describes is 48:9 (16:3); past that the width it uses is clamped. The mode name the
developer display prints is "Super Wide Mode" or "Normal Mode".

## How it works

### Setting a resolution

`001DDBA0(display, w, h)` is the only way into the fit. It stores the size in the settings object
`[01F82D20]` (see [game settings](../Saving-Loading-And-Settings/game-settings.md)) and then fits it:

1. With ScreenMode (setting 2, `+0x08`) at 0, windowed, it stores `w << 16 | h` as WindowSize
   (setting 11) through `001DF340` (`001DDBD3`), rebuilds the window-size list (`001DD8E0`,
   `001DDBDB`) and calls `0017DB80`; otherwise it stores the same word as Resolution (setting 1,
   `001DDBEC`).
2. It writes `GameSetting.ini` (`001DFD40`, `001DDBF8`).
3. It logs `[Screen Mode]setResolutionSize w = %d ,h = %d Screen Mode = %d` (`00900910`) with
   ScreenMode, and tail-jumps to the fit `001DDAC0` with the same three arguments (`001DDC39`).

The setter is reached through `00182F70(w, h)`, which fetches the display object, and from
`001DC730`. Its callers are the application start-up (`0017CEB0`, with the start-up size), the
window-event handler `007A3C10` (event 0, a packed new size), the screen-mode switch `007A3E00`
(the monitor rectangle or the desktop size), and `001DC730`, which applies the selected entry of
the window-size list in windowed mode and of the display-mode list otherwise, then stores the
mode's refresh rate (`001DC76F`).

### The fit

`001DDAC0(record, W, H)` first stores `W` at `+0x10` and `H` at `+0x14` and computes
`ratio = W / H` as floats (`001DDAEC`). It compares the ratio with `16/9` (`008C5B38`) and `16/3`
(`00900A0C`):

| Ratio | Branch | Mode `+0x00` | Size | `+0x04` / `+0x08` / `+0x0C` |
|---|---|---|---|---|
| up to 16:9 | `001DDAF5`-`001DDB18` | 0 | height becomes `(int)(W / (16/9))` | 1.0, 1.0, 0 |
| above 48:9 | `001DDB26`-`001DDB52` | 1 | width becomes `(int)(H × 16/3)` | 1.0, 1.0, 0 |
| between | `001DDB53`-`001DDB9E` | 1 | kept | see below; `+0x08` not written |

The middle branch divides integers: `+0x04 = (float)(W − H / W)` (`div` at `001DDB63`) and
`+0x0C = (float)((W − H) / W) × 0.5` (`001DDB7D`, constant `01CEBB70`). In this branch `W` is
always greater than `H`, so both quotients are 0: `+0x04` receives the width in pixels and
`+0x0C` receives 0. Nothing reads these three fields (see below), so the values have no effect.
`+0x08` holds 1.0 from the constructor (`001DC5C0`) and every branch that writes it writes 1.0.

### Who reads the fit

The fit is read through the getter `001DDAB0` (`mov rax, [01F82D18]`). The readers take the
mode and the fitted size:

- `001DD8C0` answers `mode == 1` (Super Wide); its second test `005C5230` returns 0. The wrapper
  `00182F50` serves it to six callers.
- `001DD120` returns the aspect: `(float)W / (float)H` from `+0x10` / `+0x14` in mode 1, and the
  constant 16/9 otherwise (`001DD126`-`001DD164`). `00182EE0` wraps it.
- `00225680` and `002256A0` return `+0x10` and `+0x14`; `00182440` returns the mode word.
- `001DCE20` writes "Super Wide Mode" (`00900960`) for mode 1, else "Normal Mode" (`00900970`),
  into the object's `+0x80` through `001A1E40` (`001DCE26`-`001DCE43`); the developer console
  `001CD0E0` prints it.

A sweep of every function that reaches the object through the getter or `01F82D18` directly,
and of every function the object is passed to, finds no read of `+0x04`, `+0x08` or `+0x0C`
outside the fit and the constructor.

### What the aspect drives

- The renderer's projection: `00229D20` returns 4/3 unless the frame-mode byte `02064AD1` is 1, 2,
  3 or 5, and then the display object's aspect through `00182EE0`; the camera update stores it at
  `02AED4E0` and builds the projection with it ([scripted camera](scripted-camera.md)).
- The 16:9 scale factor: `0017FFD0` returns `001DD110()` (the constant 16/9) divided by the aspect,
  so 1.0 in Normal Mode and below 1.0 in Super Wide Mode. Its callers multiply horizontal
  positions by it; the full-screen quad `001D8B20` spans `±factor` across, keeping a 16:9 quad
  centred on a wider screen.
- The viewport: `00186B80` in Normal Mode (`00182F50` false) sets the viewport width to 16/9 of
  the height it is given and centres it on the given rectangle; in Super Wide Mode it uses the
  rectangle as given.

- The 16:9 in that viewport comes from `00182E50`, which returns `001DD110()` when the display
  object exists and the same constant 16/9 when it does not.
- The window offset: each frame the render pass list `00187950` stores at render-manager `+0xDA0`
  and `+0xDA4` the offset that centres the fit size (`00182EB0`, `00182E80`: `+0x10` and `+0x14`,
  or 1920 × 1080 without a display object) in the window size (`+0xD24`, `+0xD28` of
  `00796E20()`).
- `001EE5D0` gives that offset: 0, 0 for equal sizes, half the width difference when the fit is
  narrower in aspect, otherwise half the height difference, made positive. The colour-buffer copy
  `001EE8E0` hands the offset to `00186B80`.

- The frame-mode zoom: `00229D60` returns 1.1547 for frame mode 2 (`02064AD1`), 4/3 for mode 3,
  1.0966 for mode 5 and 1.0 otherwise. The projection builder `003CBB30` multiplies the scale
  `1 / tan(fov / 2)` by it on both axes, and the camera update passes it to the renderer
  (`00182640`). `00229DA0(mode)` returns the same values for a given mode; `00247AE0` and
  `0029CF30` call it with 2.

### The display-mode list

The constructor `001DC5C0` calls `001DD420`, which enumerates the outputs of the adapter
(`IDXGIAdapter::EnumOutputs`, vtable `+0x38`) and asks each for its modes with
`IDXGIOutput::GetDisplayModeList` (vtable `+0x40`) in format 28, `R8G8B8A8_UNORM` (`006242C0`).
Each 28-byte entry is a `DXGI_MODE_DESC`. The list keeps a mode only when:

- it is at least 1280 × 720 (`0x500` × `0x2D0`) and its refresh denominator is not 0;
- its refresh rate, numerator over denominator as a whole number, is 59 or 60 Hz, or with any FrameLimit but 1
  (the shipped 0 is 30 fps) also 29 or 30 Hz (`0017D8F0` reads FrameLimit).

It then sorts by width and height, keeps one entry per size, and selects the entry whose pixel
count is nearest the Resolution setting's. With no usable mode the list is one entry of the
Resolution size at 60/1 Hz.

### The window-size list

`001DD8E0` copies the display-mode list into the window-size list at `+0x40` with one spare entry,
looks for the WindowSize setting (`+0x2C` height, `+0x2E` width as 16-bit halves) and selects it;
when it is missing it writes it into the spare entry and sorts it into place by width, then height.
The windowed resolution row therefore always offers the current window size.

## Layouts

The display object is 0x180 bytes, built once by `001DDA70` and constructed by `001DC5C0`; its
first 0x18 bytes are the fit record.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | mode | 0 Normal Mode, 1 Super Wide Mode (ctor 0) |
| `04` | `f32` | fitA | 1.0 or the width (middle branch); no reader |
| `08` | `f32` | fitB | 1.0; no reader |
| `0C` | `f32` | fitC | 0; no reader |
| `10` | `u32` | width | fitted width |
| `14` | `u32` | height | fitted height |
| `18` | `u32` | screenMode | ScreenMode at construction (setting 2) |
| `20` | `u32` | modeCount | display-mode entries (ctor 1) |
| `24` | `u32` | modeIndex | selected display mode |
| `28` | `void*` | modes | DXGI_MODE_DESC[modeCount], `0x1C` each |
| `30` | `u32` | refreshHz | numerator / denominator of the selected mode (ctor 60) |
| `34` | `u32` | windowLast | last index of the window-size list |
| `38` | `u32` | windowIndex | selected window size |
| `40` | `void*` | windowSizes | `0x1C` entries, modeCount + 1 |
| `48` | `u32` | adapter | selected adapter index |
| `5C` | `u32` | outputCount | outputs of the adapter |
| `60` | `u32` | monitor | selected output (ctor: setting 26, Monitor) |
| `78` | `void*` | adapters | `0x140`-byte adapter records |
| `80` | `string` | modeName | "Super Wide Mode" or "Normal Mode" (`001DCE20`) |

DXGI_MODE_DESC (`0x1C`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | Width |  |
| `04` | `u32` | Height |  |
| `08` | `u32` | RefreshRate.Numerator |  |
| `0C` | `u32` | RefreshRate.Denominator |  |
| `10` | `u32` | Format |  |
| `14` | `u32` | ScanlineOrdering |  |
| `18` | `u32` | Scaling |  |

## Shipped data

| Fact | Value |
|---|---|
| widescreen bound `008C5B38` | 1.7777778 (16/9) |
| super-wide bound `00900A0C` | 5.3333335 (16/3, 48:9) |
| half `01CEBB70` | 0.5 |
| mode names | "Super Wide Mode" `00900960`, "Normal Mode" `00900970` |
| aspect outside the frame modes 1, 2, 3, 5 | 4/3 (`0x3FAAAAAB`, `00229D20`) |

## Modding notes

- Only the mode and the fitted size reach the renderer; patching the middle branch's integer
  divides changes nothing on screen.
- To allow shapes wider than 48:9, raise the float at `00900A0C`; the clamp is the only limit.
- Display modes below 1280 × 720, or at a refresh rate other than 29, 30, 59 or 60 Hz, never
  appear in the resolution list.

## Related

- [Config screen](../Menus-And-HUD/config-screen.md): the Resolution, Screen Mode and adapter rows that
  call `001DC730`.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): Resolution, ScreenMode, WindowSize,
  FrameLimit and Monitor.
- [Global state accessors](../Engine-Core/global-state-accessors.md): the getter
  `001DDAB0`.
- [Scripted camera](scripted-camera.md): the projection the aspect feeds.
- [Script screen effects](script-screen-effects.md): screen quads that use the 16:9 factor.
