---
title: "Controllers: how a gamepad is found, the three kinds of controller the game builds, plugging one in during play, and the Steam Input action names"
kind: "system"
category: "Controls and input"
addresses: "0x00797910, 0x00796230, 0x00798A40, 0x00797690, 0x00792B70, 0x00792CB0, 0x00792AB0, 0x007999E0"
---

## What the player sees

- A pad can be plugged in before the game starts or while it runs.
- Up to four Xbox-style pads are used; other pads work through DirectInput, and a Steam controller through Steam
  Input.
- A DirectInput pad stops responding while the game window is not in front.

## How it works

### Start-up

`0x00797910` runs once (`0x00797910`-`0x007979A3`):

1. It fetches the Steam controller interface into `0x02EA9508` and, when there is one, initialises it.
2. It creates DirectInput 8 into `0x02EA5370`; a failure returns error 9 (`0x0079795D`-`0x00797966`).
3. It asks DirectInput to list every attached device, calling `0x00796230` for each; a failure of that call also
   returns error 9 (`0x0079798D`-`0x00797998`).

### The two callbacks

`0x00796230` (start-up) and `0x00798A40` (device arrival) look at the device type byte `+0x24` of each listed device:

| Type | `0x00796230` | `0x00798A40` |
|---|---|---|
| `0x12` mouse | the mouse set-up `0x00797460` | the same |
| `0x13` keyboard | the keyboard set-up `0x007973D0` | ignored |
| `0x14` joystick, `0x15` gamepad, `0x18` first-person | the pad set-up `0x00797690` | the same |
| any other | ignored | ignored |

The pad test is `(type - 0x14) & 0xFA == 0` and `type != 0x19` (`0x00796242`-`0x0079624C`), which passes exactly
`0x14`, `0x15` and `0x18` and leaves out `0x19`, the device-control type. So the keyboard is set up only at start-up;
mice and pads also when they arrive.

### One pad

`0x00797690(device)` decides what to build (`0x00797690`-`0x0079790D`):

1. `0x00797AD0` tests whether the device is an XInput pad; a yes also sets `0x02EA5379`.
2. It returns when a registered controller of kind 2 in the list `0x01F401E8` already holds this device's instance
   GUID; it checks up to 18 of them.
3. When the Steam interface reports a connected controller, it builds a Steam controller, `0x458` bytes, with
   `0x00792B70`.
4. For an XInput pad, when fewer than four have been counted, it builds an XInput controller, `0x470` bytes, with
   `0x00792CB0` and the count `0x02EA9500` as its user index; the count goes up for every XInput pad, built or not.
5. For any other pad, and only when step 3 built nothing, it opens a DirectInput device: `CreateDevice`,
   `SetDataFormat`, `SetCooperativeLevel` with flags 6, non-exclusive and foreground only, `EnumObjects` with
   `0x00796280`, then `Acquire`, and builds a DirectInput controller, `0x458` bytes, with `0x00792AB0`. A failure of
   `CreateDevice`, `SetDataFormat` or `EnumObjects`, or a cooperative-level answer of "not implemented", leaves the
   pad unused.

An XInput pad is never opened through DirectInput, and a Steam controller and an XInput controller can both be built
for one pad.

### What the controllers share

All three constructors call the base `0x00792940`, which links the object into the list `0x01F401E8` and zeroes
`0x244` bytes at `+0x1D0` (`0x00792A89`-`0x00792A96`). The DirectInput and XInput constructors then copy the listed
device's description, `0x244` bytes, into `+0x1D0` (`0x00792AD7`-`0x00792AF1`, `0x00792CF4`-`0x00792D11`), so its instance
GUID is at `+0x1D4`, the field step 2 compares. The Steam constructor `0x00792B70` copies none, so a Steam controller
holds no GUID. The XInput controller adds its user index at `+0x458` (`0x00792CB0`).

The base also builds four
`0x48`-byte entries at `+0xB0` with `0x00792D90` (`0x007929BD`), which points each entry's two links at itself and sets
its floats `+0x1C` to 1.0 and `+0x24` to 0.005.

### The XInput library

The XInput constructor `0x00792CB0` ends by calling `0x00862C70`, which loads `.\xinput1_3.dll` with `LoadLibraryW`,
keeps its export ordinal 100 in `0x02EBA3F0` and sets `0x02EAF8F0` (`0x00862C70`-`0x00862CCD`). `0x00862CF0` does the same
load when `0x02EAF8F0` is still 0, reads user 0 through that export into `0x02EBA3E0`, and answers 1 when bit `0x400` of
the button word `0x02EBA3E4` is set, or the button word itself otherwise. The R2 latch of [Escape Mode](escape.md)
reads it; a raw scan finds no other caller of `0x00862CF0` or `0x00862C70` than these two and the constructor.

### The Steam action names

`0x00792B70` keeps the Steam controller handle in `0x02EA95A0`, activates the action set `Global`, and fetches sixteen
digital action handles into `0x02EA9510` and two analog ones into `0x02EA9590`, by the names in the tables at `0x01F40210`
and `0x01F40290`. A Steam Input configuration for the game uses these names.

### Plugging in a pad

The window procedure sets `0x02EA5363` when a device-change message arrives with the code for a device arriving,
`0x8000` (`0x0079973E`-`0x00799747`). The per-frame device update `0x007999E0` sees it, clears it and lists the devices
again with `0x00798A40` (`0x007999E4`-`0x00799A12`). Nothing in this walk removes a controller.

## Shipped data

| Kind | Names |
|---|---|
| digital | Up, Down, Left, Right, Circle, Cross, Square, Triangle, L1, L2, L3, R1, R2, R3, Start, Select |
| analog | LeftAnalog, RightAnalog |

## State

The input objects sit in two lists with their own head nodes: `0x01F401E8` (`+0x00` the first node, `+0x08` the last)
for the live ones and `0x01F401F8` for retired mice. An object's node is at its `+0x08`. Besides the base `0x00792940`
of the three pad controllers, the keyboard object `0x007927C0` (from `0x007973D0`, `0x00797451`) and the mouse object
`0x00792870` (from `0x00797460`, `0x00797669`) link themselves to the end of the live list. Each list starts empty, its
head pointing at itself in the file.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F401F0` | `void*` | `0x01F401E8` | the live list's last node | `0x007927C0` (`0x00792815`); `0x00792870` (`0x007928C2`); `0x00792940` (`0x00792992`); through the nodes, when the last one is unlinked: `0x00797460` (`0x007975A2`) and the shutdown `0x00799860` (`0x007998AA`) | `0x007927C0` (`0x007927F4`); `0x00792870` (`0x007928AA`); `0x00792940` (`0x0079297A`) |
| `0x01F40200` | `void*` | `0x01F401F8` | the retired list's last node | `0x00797460` (`0x007975C8`); through the nodes, when the shutdown `0x007998E0` unlinks the last one (`0x0079994A`) | `0x00797460` (`0x007975B0`) |
| `0x02EA58B8` | `void*` | 0 | the mouse object. When a mouse is set up again, `0x00797460` unlinks the old one's six `0x48`-byte entries from `+0x30` that still name it (`0x00797489`-`0x00797593`), moves it from the live list to the retired list (`0x00797597`-`0x007975C8`), builds a new one and stores it here; the retired objects are destroyed only at shutdown (`0x007998E0`) | `0x00797460` (`0x00797671`) | `0x00797460` (`0x00797479`) |
| `0x01F3DA04` | `u8` | 1 | lets the XInput controller's poll `0x007A2140` run (`0x007A2194`-`0x007A219B`). On Windows 7 (`GetVersionExA` platform 2, version 6.1) with an XInput pad marked in `0x02EA5379`, the poll calls `0x00799A80`, which clears it and notes the clock's second in `0x01F4012C`, then sets it again once more than `0x01F40188` (1) second has passed and clears `0x02EA5379`, so it happens once (`0x00799A80`-`0x00799B06`) | `0x00799A80`: 0 (`0x00799AD8`), 1 (`0x00799AFF`) | `0x007A2140` (`0x007A2194`) |

No other instruction reaches these four. The search covered the executable's RIP-relative references (the lists'
heads are taken by the functions above and by the walkers `0x00796FC0`, `0x00797690`, `0x007999E0`, `0x0079AF20`,
`0x0079CEC0` and `0x0079E3D0`, which only follow the first-node links), its image-base-relative references, which hold
none of them.

A scan of `.text` for the 32-bit offsets of `0x01F401E8`, `0x01F401F0`, `0x01F401F8`, `0x01F40200`,
`0x02EA58B8` and `0x01F3DA04` from the image base, which finds only bytes of the call instruction at `0x00614B7A`, not an
operand.

## Modding notes

- A fifth XInput pad is counted but never built.
- Every pad is checked against the registered list by instance GUID, so the walk on each arrival does not build a
  second controller for a pad it already has; a Steam controller holds no GUID, so it is built again on each walk
  while Steam reports one.

## Related

- [keymap.ini](keymap-file.md) - the keyboard bindings.
- [Control names](control-names.md) - the codes the pad buttons use.
