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

`0x00797910` runs once (`0x00797910`-`0x007979A2`):

1. It fetches the Steam controller interface into `0x02EA9508` and, when there is one, initialises it.
2. It creates DirectInput 8 into `0x02EA5370`; a failure returns error 9 (`0x0079795D`-`0x00797966`).
3. It asks DirectInput to list every attached device, calling `0x00796230` for each; a failure of that call also
   returns error 9 (`0x0079798D`-`0x00797998`), and success returns 0 (`0x0079799B`).

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

Both callbacks return 1 for every device, whatever its type, so the listing goes on to the next device
(`0x00796253`, `0x00796262`, `0x00796271`; `0x00798A5E`, `0x00798A6D`).

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

Step 3 first calls the Steam interface's slot `+0x10`, then asks slot `+0x18` for the connected controllers and
builds when the count is above 0 (`0x0079775D`-`0x00797783`). Each build allocates with `0x00584740` and skips the
constructor when that returns null (`0x007977A5`, `0x007977FB`, `0x007978CB`); the Steam flag that keeps step 5 from
running and the XInput count are set even then (`0x007977B3`, `0x00797813`-`0x0079781B`).

In step 5 the result of `Acquire` is not tested (`0x007978B9`), and a cooperative-level answer other than "not
implemented" goes on to `EnumObjects` (`0x0079788E`-`0x00797893`). A device whose `SetDataFormat` or `EnumObjects`
call fails, or whose cooperative level answers "not implemented", is left without a release (`0x00797874`,
`0x00797893`, `0x007978AF`).

### What the controllers share

All three constructors call the base `0x00792940`, which links the object into the list `0x01F401E8` and zeroes
`0x244` bytes at `+0x1D0` (`0x00792A89`-`0x00792A96`). The DirectInput and XInput constructors then copy the listed
device's description, `0x244` bytes, into `+0x1D0` (`0x00792AD7`-`0x00792AF1`, `0x00792CF4`-`0x00792D11`), so its instance
GUID is at `+0x1D4`, the field step 2 compares. The Steam constructor `0x00792B70` copies no description, so a Steam
controller holds no GUID. The XInput controller adds its user index at `+0x458` (`0x00792CB0`).

The base stores its second argument at `+0x28` (`0x00792976`). The DirectInput constructor `0x00792AB0` passes the
device that `CreateDevice` opened (`0x00792AC0`, `0x007978D0`); the Steam and XInput constructors pass the value 0
(`0x00792BAA`, `0x00792CC5`). Each constructor then sets its own vtable, `0x01CB2638` for DirectInput, `0x01CB26B8` for
Steam and `0x01CB2678` for XInput (`0x00792AD4`, `0x00792BB9`, `0x00792CDC`), and returns the object
(`0x00792B5C`, `0x00792C78`, `0x00792D81`). The XInput constructor also zeroes `+0x45C`-`+0x46B` (`0x00792CE6`, `0x00792CED`).

The DirectInput controller's polling method `0x007A1A50` returns at once when `+0x28` is 0 (`0x007A1A6F`-`0x007A1A79`),
and its destructor `0x007935C0` unacquires and releases the device when `+0x28` is set (`0x007935E1`-`0x007935FA`).

The base also builds four
`0x48`-byte entries at `+0xB0` with `0x00792D90` (`0x007929BD`), which points each entry's two links at itself and sets
its floats `+0x1C` to 1.0 and `+0x24` to 0.005.

### The XInput library

The XInput constructor `0x00792CB0` ends by calling `0x00862C70`, which loads `.\xinput1_3.dll` with `LoadLibraryW`,
keeps its export ordinal 100 in `0x02EBA3F0` and sets `0x02EAF8F0` (`0x00862C70`-`0x00862CCD`). `0x00862CF0` does the same
load when `0x02EAF8F0` is still 0, reads user 0 through that export into `0x02EBA3E0`, and answers 1 when bit `0x400` of
the button word `0x02EBA3E4` is set, or the button word itself otherwise. The R2 latch of [Escape Mode](escape.md)
reads it (`0x00254213`); nothing else calls `0x00862CF0` or `0x00862C70`.

### The Steam action names

`0x00792B70` keeps the Steam controller handle in `0x02EA95A0`, activates the action set `Global`, and fetches sixteen
digital action handles into `0x02EA9510` and two analog ones into `0x02EA9590`, by the names in the tables at `0x01F40210`
and `0x01F40290`. A Steam Input configuration for the game uses these names.

It does all of this only when the interface's slot `+0x18` reports a connected controller again, keeping the first
handle it lists (`0x00792BBC`-`0x00792BDB`); otherwise the controller is built with no handles fetched (`0x00792BD0`).
The names go through slot `+0x28` for the set, `+0x30` to activate it, `+0x40` for the digital handles and `+0x58`
for the analog ones (`0x00792BE9`-`0x00792C66`).

### Plugging in a pad

The window procedure sets `0x02EA5363` when a device-change message arrives with the code for a device arriving,
`0x8000` (`0x0079973E`-`0x00799747`). The per-frame device update `0x007999E0` sees it, clears it and lists the devices
again with `0x00798A40` (`0x007999E4`-`0x00799A12`). Nothing in this walk removes a controller. When that listing fails,
`0x007999E0` returns 9 at once (`0x00799A15`-`0x00799A19`); otherwise, and on every frame without the flag, it calls the
virtual slot `+0x28` of each object in the live list `0x01F401E8`, from its node at `+0x08`, and returns 0
(`0x00799A23`-`0x00799A72`).

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
| `0x02EA537A` | `u8` | 0 | 1 once a mouse has been set up. The input poll `0x007A2440`, which the window's update slot `0x007A3110` runs on the application's input object, then binds that object to the first controller of kind 0, the mouse (`0x0079A430`, through `0x00796FC0(0, 0)`; the mouse class `0x01CB23F8` answers 0 from slot 1, `0x005C5230`), and clears it; the poll also binds when the object holds no mouse at `+0x150` (`0x007A2446`-`0x007A246B`) | `0x00797460`, 1 (`0x007975CF`); `0x007A2440`, 0 (`0x007A246B`) | `0x007A2440` (`0x007A245D`) |

No other instruction reaches these five. The lists' heads are also taken by the walkers `0x00796FC0`, `0x00797690`,
`0x007999E0`, `0x0079AF20`, `0x0079CEC0` and `0x0079E3D0`, which only follow the first-node links, and the address `0x02EA5370`
that `0x00797910` hands DirectInput (`0x00797942`) is the 8-byte interface pointer, below `0x02EA537A`.

## Modding notes

- A fifth XInput pad is counted but never built.
- Every pad is checked against the registered list by instance GUID, so the walk on each arrival does not build a
  second controller for a pad it already has; a Steam controller holds no GUID, so it is built again on each walk
  while Steam reports one.

## Related

- [keymap.ini](keymap-file.md) - the keyboard bindings.
- [Control names](control-names.md) - the codes the pad buttons use.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Application: `0x00584740` is called by `0x001A98B0`; those functions are documented on
  [game application](../Engine-Core/game-application.md).
- Audio: `0x00584740` is called by `0x002125A0`, `0x00225C40`, `0x006794D0`; those functions are documented on
  [audio manager](../Sound-And-Music/audio-manager.md), [sound engine](../Sound-And-Music/sound-engine.md).
- Platform: `0x00584740` is called by `0x00650D40`; those functions are documented on
  [phyre post effect classes](../PhyreEngine/phyre-post-effect-classes.md).
- Resource: `0x00584740` is called by `0x001A11B0`, `0x001DAD60`, `0x00637C50`; those functions are documented on
  [game application](../Engine-Core/game-application.md),
  [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md).
