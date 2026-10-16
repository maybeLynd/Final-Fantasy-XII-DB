---
title: "Controllers: how a gamepad is found, the three kinds of controller the game builds, plugging one in during play, and the Steam Input action names"
kind: "system"
category: "Controls and input"
summary: "How a pad becomes a controller: the start-up device walk and its two callbacks, the device types each accepts, the duplicate test, the Steam, XInput and DirectInput controller objects and the order they are tried in, the four-pad XInput limit, the XInput library the game loads and its pad-0 button read, the DirectInput set-up and its failure rules, the eighteen Steam Input action names, and the device-arrival message that repeats the walk."
addresses: "00797910, 00796230, 00798A40, 00797690, 00792B70, 00792CB0, 00792AB0, 007999E0"
---

## What the player sees

- A pad can be plugged in before the game starts or while it runs.
- Up to four Xbox-style pads are used; other pads work through DirectInput, and a Steam controller through Steam
  Input.
- A DirectInput pad stops responding while the game window is not in front.

## How it works

### Start-up

`00797910` runs once (`00797910`-`007979A3`):

1. It fetches the Steam controller interface into `02EA9508` and, when there is one, initialises it.
2. It creates DirectInput 8 into `02EA5370`; a failure returns error 9 (`0079795D`-`00797966`).
3. It asks DirectInput to list every attached device, calling `00796230` for each; a failure of that call also
   returns error 9 (`0079798D`-`00797998`).

### The two callbacks

`00796230` (start-up) and `00798A40` (device arrival) look at the device type byte `+0x24` of each listed device:

| Type | `00796230` | `00798A40` |
|---|---|---|
| `0x12` mouse | the mouse set-up `00797460` | the same |
| `0x13` keyboard | the keyboard set-up `007973D0` | ignored |
| `0x14` joystick, `0x15` gamepad, `0x18` first-person | the pad set-up `00797690` | the same |
| any other | ignored | ignored |

The pad test is `(type - 0x14) & 0xFA == 0` and `type != 0x19` (`00796242`-`0079624C`), which passes exactly
`0x14`, `0x15` and `0x18` and leaves out `0x19`, the device-control type. So the keyboard is set up only at start-up;
mice and pads also when they arrive.

### One pad

`00797690(device)` decides what to build (`00797690`-`0079790D`):

1. `00797AD0` tests whether the device is an XInput pad; a yes also sets `02EA5379`.
2. It returns when a registered controller of kind 2 in the list `01F401E8` already holds this device's instance
   GUID; it checks up to 18 of them.
3. When the Steam interface reports a connected controller, it builds a Steam controller, `0x458` bytes, with
   `00792B70`.
4. For an XInput pad, when fewer than four have been counted, it builds an XInput controller, `0x470` bytes, with
   `00792CB0` and the count `02EA9500` as its user index; the count goes up for every XInput pad, built or not.
5. For any other pad, and only when step 3 built nothing, it opens a DirectInput device: `CreateDevice`,
   `SetDataFormat`, `SetCooperativeLevel` with flags 6, non-exclusive and foreground only, `EnumObjects` with
   `00796280`, then `Acquire`, and builds a DirectInput controller, `0x458` bytes, with `00792AB0`. A failure of
   `CreateDevice`, `SetDataFormat` or `EnumObjects`, or a cooperative-level answer of "not implemented", leaves the
   pad unused.

An XInput pad is never opened through DirectInput, and a Steam controller and an XInput controller can both be built
for one pad.

### What the controllers share

All three constructors call the base `00792940`, which links the object into the list `01F401E8` and zeroes
`0x244` bytes at `+0x1D0` (`00792A89`-`00792A96`). The DirectInput and XInput constructors then copy the listed
device's description, `0x244` bytes, into `+0x1D0` (`00792AD7`-`00792AF1`, `00792CF4`-`00792D11`), so its instance
GUID is at `+0x1D4`, the field step 2 compares. The Steam constructor `00792B70` copies none, so a Steam controller
holds no GUID. The XInput controller adds its user index at `+0x458` (`00792CB0`).

The base also builds four
`0x48`-byte entries at `+0xB0` with `00792D90` (`007929BD`), which points each entry's two links at itself and sets
its floats `+0x1C` to 1.0 and `+0x24` to 0.005.

### The XInput library

The XInput constructor `00792CB0` ends by calling `00862C70`, which loads `.\xinput1_3.dll` with `LoadLibraryW`,
keeps its export ordinal 100 in `02EBA3F0` and sets `02EAF8F0` (`00862C70`-`00862CCD`). `00862CF0` does the same
load when `02EAF8F0` is still 0, reads user 0 through that export into `02EBA3E0`, and answers 1 when bit `0x400` of
the button word `02EBA3E4` is set, or the button word itself otherwise. The R2 latch of [Escape Mode](escape.md)
reads it; a raw scan finds no other caller of `00862CF0` or `00862C70` than these two and the constructor.

### The Steam action names

`00792B70` keeps the Steam controller handle in `02EA95A0`, activates the action set `Global`, and fetches sixteen
digital action handles into `02EA9510` and two analog ones into `02EA9590`, by the names in the tables at `01F40210`
and `01F40290`. A Steam Input configuration for the game uses these names.

### Plugging in a pad

The window procedure sets `02EA5363` when a device-change message arrives with the code for a device arriving,
`0x8000` (`0079973E`-`00799747`). The per-frame device update `007999E0` sees it, clears it and lists the devices
again with `00798A40` (`007999E4`-`00799A12`). Nothing in this walk removes a controller.

## Shipped data

| Kind | Names |
|---|---|
| digital | Up, Down, Left, Right, Circle, Cross, Square, Triangle, L1, L2, L3, R1, R2, R3, Start, Select |
| analog | LeftAnalog, RightAnalog |

## Modding notes

- A fifth XInput pad is counted but never built.
- Every pad is checked against the registered list by instance GUID, so the walk on each arrival does not build a
  second controller for a pad it already has; a Steam controller holds no GUID, so it is built again on each walk
  while Steam reports one.

## Related

- [keymap.ini](keymap-file.md) - the keyboard bindings.
- [Control names](control-names.md) - the codes the pad buttons use.
