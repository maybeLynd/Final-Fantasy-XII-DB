[Home](../../README.md) / [Controls and input](README.md) / Controllers

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Controllers: how a gamepad is found, the three kinds of controller the game builds, plugging one in during play, and the Steam Input action names | system | Controls and input | How input works | How a pad becomes a controller: the start-up device walk and its two callbacks, the device types each accepts, the duplicate test, the Steam, XInput and DirectInput controller objects and the order they are tried in, the four-pad XInput limit, the XInput library the game loads and its pad-0 button read, the DirectInput set-up and its failure rules, the eighteen Steam Input action names, and the device-arrival message that repeats the walk. | 0x00797910, 0x00796230, 0x00798A40, 0x00797690, 0x00792B70, 0x00792CB0, 0x00792AB0, 0x007999E0 |

## What the player sees

- A pad can be plugged in before the game starts or while it runs.
- Up to four Xbox-style pads are used; other pads work through DirectInput, and a Steam controller through Steam
  Input.
- A DirectInput pad stops responding while the game window is not in front.

At start-up, and again whenever a device is plugged in, the game lists every attached device and builds one controller
for each pad. It builds a Steam controller when Steam reports one, an XInput controller for each of the first four
Xbox-style pads, and a DirectInput one for any other pad. The per-frame device update then runs every controller in
that list.

## How it works

### Start-up

`0x00797910` runs once¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00797910`-`0x007979A2` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | It fetches the Steam controller interface into `0x02EA9508` and, when there is one, initialises it. |   |
| 2 | It creates DirectInput 8 into `0x02EA5370`; a failure returns error 9. | `0x0079795D`-`0x00797966` |
| 3 | It asks DirectInput to list every attached device, calling `0x00796230` for each; a failure of that call also returns error 9, and success returns 0. | `0x0079798D`-`0x00797998`<br>`0x0079799B` |

### The two callbacks

`0x00796230` (start-up) and `0x00798A40` (device arrival) look at the device type byte `+0x24` of each listed device:

| Type | `0x00796230` | `0x00798A40` |
|---|---|---|
| `0x12` mouse | the mouse set-up `0x00797460` | the same |
| `0x13` keyboard | the keyboard set-up `0x007973D0` | ignored |
| `0x14` joystick, `0x15` gamepad, `0x18` first-person | the pad set-up `0x00797690` | the same |
| any other | ignored | ignored |

The pad test is `(type - 0x14) & 0xFA == 0` and `type != 0x19`¹, which passes exactly
`0x14`, `0x15` and `0x18` and leaves out `0x19`, the device-control type. So the keyboard is set up only at start-up;
mice and pads also when they arrive.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00796242`-`0x0079624C` |

</details>

Both callbacks return 1 for every device, whatever its type, so the listing goes on to the next device¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00796253`, `0x00796262`, `0x00796271`; `0x00798A5E`, `0x00798A6D` |

</details>

### One pad

`0x00797690(device)` decides what to build¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00797690`-`0x0079790D` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `0x00797AD0` tests whether the device is an XInput pad; a yes also sets `0x02EA5379`. Steps 4 and 5 do not reuse this answer: they call `0x00797AD0` again and branch on the second answer. | `0x007977B9`<br>`0x007977C0` |
| 2 | It returns when a registered controller of kind 2 in the list `0x01F401E8` already holds this device's instance GUID; it checks up to 18 of them. All three controller kinds answer 2 (vtable slot `+8`, `0x00290180`), and the test comes before step 3, so an existing controller of any kind stops it. | `0x0079773A`-`0x00797759`<br>`0x0079774E` |
| 3 | When the Steam interface reports a connected controller, it builds a Steam controller, `0x458` bytes, with `0x00792B70`. |   |
| 4 | For an XInput pad, when fewer than four have been counted, it builds an XInput controller, `0x470` bytes, with `0x00792CB0` and the count `0x02EA9500` as its user index; the count goes up for every XInput pad, built or not. |   |
| 5 | For any other pad, and only when step 3 built nothing, it opens a DirectInput device: `CreateDevice`, `SetDataFormat`, `SetCooperativeLevel` with flags 6, non-exclusive and foreground only, `EnumObjects` with `0x00796280`, then `Acquire`, and builds a DirectInput controller, `0x458` bytes, with `0x00792AB0`. A failure of `CreateDevice`, `SetDataFormat` or `EnumObjects`, or a cooperative-level answer of "not implemented", leaves the pad unused. |   |

An XInput pad is never opened through DirectInput, and a Steam controller and an XInput controller can both be built
for one pad.

Step 3 first calls the Steam interface's slot `+0x10`, then asks slot `+0x18` for the connected controllers and
builds when the count is above 0¹. Each build allocates with `0x00584740` and skips the
constructor when that returns null²; the Steam flag that keeps step 5 from
running and the XInput count are set even then³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0079775D`-`0x00797783` |
| ² | `0x007977A5`, `0x007977FB`, `0x007978CB` |
| ³ | `0x007977B3`, `0x00797813`-`0x0079781B` |

</details>

In step 5 the result of `Acquire` is not tested¹, and a cooperative-level answer other than "not
implemented" goes on to `EnumObjects`². A device whose `SetDataFormat` or `EnumObjects`
call fails, whose cooperative level answers "not implemented", or whose controller allocation returns null after
`Acquire`, is left without a release³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007978B9` |
| ² | `0x0079788E`-`0x00797893` |
| ³ | `0x00797874`, `0x00797893`, `0x007978AF`, `0x007978CE` |

</details>

### What the controllers share

All three constructors call the base `0x00792940`, which links the object into the list `0x01F401E8` and zeroes
`0x244` bytes at `+0x1D0`¹. The DirectInput and XInput constructors then copy the listed
device's description, `0x244` bytes, into `+0x1D0`², so its instance
GUID is at `+0x1D4`, the field step 2 compares. The Steam constructor `0x00792B70` copies no description, so a Steam
controller holds no GUID. The XInput controller adds its user index at `+0x458`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00792A89`-`0x00792A96` |
| ² | `0x00792AD7`-`0x00792AF1`, `0x00792CF4`-`0x00792D11` |
| ³ | `0x00792CB0` |

</details>

The base stores its second argument at `+0x28`¹. The DirectInput constructor `0x00792AB0` passes the
device that `CreateDevice` opened²; the Steam and XInput constructors pass the value 0³. Each constructor then sets its own vtable, `0x01CB2638` for DirectInput, `0x01CB26B8` for
Steam and `0x01CB2678` for XInput⁴, and returns the object⁵. The XInput constructor also zeroes `+0x45C`-`+0x46B`⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00792976` |
| ² | `0x00792AC0`, `0x007978D0` |
| ³ | `0x00792BAA`, `0x00792CC5` |
| ⁴ | `0x00792AD4`, `0x00792BB9`, `0x00792CDC` |
| ⁵ | `0x00792B5C`, `0x00792C78`, `0x00792D81` |
| ⁶ | `0x00792CE6`, `0x00792CED` |

</details>

The DirectInput controller's polling method `0x007A1A50` returns at once when `+0x28` is 0¹,
and its destructor `0x007935C0` unacquires and releases the device when `+0x28` is set².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007A1A6F`-`0x007A1A79` |
| ² | `0x007935E1`-`0x007935FA` |

</details>

The base also builds four
`0x48`-byte entries at `+0xB0` with `0x00792D90`¹, which points each entry's two links at itself and sets
its floats `+0x1C` to 1.0 and `+0x24` to 0.005.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007929BD` |

</details>

### The XInput library

The XInput constructor `0x00792CB0` ends by calling `0x00862C70`, which loads `.\xinput1_3.dll` with `LoadLibraryW`,
keeps its export ordinal 100 in `0x02EBA3F0` and sets `0x02EAF8F0`¹. `0x00862CF0` does the same
load when `0x02EAF8F0` is still 0, reads user 0 through that export into `0x02EBA3E0`, and answers 1 when bit `0x400` of
the button word `0x02EBA3E4` is set, or the button word itself otherwise. The R2 latch of [Escape Mode](escape.md)
reads it²; nothing else calls `0x00862CF0` or `0x00862C70`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00862C70`-`0x00862CCD` |
| ² | `0x00254213` |

</details>

### The Steam action names

`0x00792B70` keeps the Steam controller handle in `0x02EA95A0`, activates the action set `Global`, and fetches sixteen
digital action handles into `0x02EA9510` and two analog ones into `0x02EA9590`, by the names in the tables at `0x01F40210`
and `0x01F40290`. A Steam Input configuration for the game uses these names.

It does all of this only when the interface's slot `+0x18` reports a connected controller again, keeping the first
handle it lists¹; otherwise the controller is built with no handles fetched².
The names go through slot `+0x28` for the set, `+0x30` to activate it, `+0x40` for the digital handles and `+0x58`
for the analog ones³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00792BBC`-`0x00792BDB` |
| ² | `0x00792BD0` |
| ³ | `0x00792BE9`-`0x00792C66` |

</details>

### Plugging in a pad

The window procedure sets `0x02EA5363` when a device-change message arrives with the code for a device arriving,
`0x8000`¹. The per-frame device update `0x007999E0` sees it, clears it and lists the devices
again with `0x00798A40`². Nothing in this walk removes a controller. When that listing fails,
`0x007999E0` returns 9 at once³; otherwise, and on every frame without the flag, it calls the
virtual slot `+0x28` of each object in the live list `0x01F401E8`, from its node at `+0x08`, and returns 0⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0079973E`-`0x00799747` |
| ² | `0x007999E4`-`0x00799A12` |
| ³ | `0x00799A15`-`0x00799A19` |
| ⁴ | `0x00799A23`-`0x00799A72` |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

| Kind | Names |
|---|---|
| digital | Up, Down, Left, Right, Circle, Cross, Square, Triangle, L1, L2, L3, R1, R2, R3, Start, Select |
| analog | LeftAnalog, RightAnalog |

</details>

## State

<details>
<summary>Show the state it keeps</summary>

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
| `0x02EA537A` | `u8` | 0 | Set to 1 at `0x007975CF`, which runs only when `0x02EA58B8` already names a mouse object (`0x00797480`-`0x00797483`), so a first set-up leaves it 0. The input poll `0x007A2440`, which the window's update slot `0x007A3110` runs on the application's input object, then binds that object to the first controller of kind 0, the mouse (`0x0079A430`, through `0x00796FC0(0, 0)`; the mouse class `0x01CB23F8` answers 0 from slot 1, `0x005C5230`), and clears it; the poll also binds when the object holds no mouse at `+0x150` (`0x007A2446`-`0x007A246B`) | `0x00797460`, 1 (`0x007975CF`); `0x007A2440`, 0 (`0x007A246B`) | `0x007A2440` (`0x007A245D`) |

No other instruction reaches these five. The lists' heads are also taken by the walkers `0x00796FC0`, `0x00797690`,
`0x007999E0`, `0x0079AF20`, `0x0079CEC0` and `0x0079E3D0`, which only follow the first-node links, and the address `0x02EA5370`
that `0x00797910` hands DirectInput¹ is the 8-byte interface pointer, below `0x02EA537A`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00797942` |

</details>

`0x00796FC0(kind, n)` walks the list whose head is `0x01F401E8`: each element is the object 8 bytes before its link,
and the next link is the object's `+0x08`¹. It asks each object for its kind
through slot 1 of its vtable² and returns the n-th object, counted from 0, whose kind equals the
argument³; it returns 0 when the list ends first⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00796FF8`, `0x00797013`-`0x00797021` |
| ² | `0x00797006` |
| ³ | `0x00797009`-`0x00797011`, `0x00797044` |
| ⁴ | `0x00797027` |

</details>

</details>

## Modding notes

- A fifth XInput pad is counted but never built.
- Every pad is checked against the registered list by instance GUID before anything is built¹, so the
  walk on each arrival does not build a second controller for a pad it already has. A Steam controller holds no
  GUID and never satisfies that test itself, but an XInput or DirectInput controller holding the pad's GUID still
  stops the Steam build.
- While Steam reports a controller, each walk builds a new Steam controller for every pad that no controller holds:
  a pad that is not XInput (step 5 is skipped once step 3 builds, `0x00797826`) and a fifth XInput pad².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0079774E` |
| ² | `0x007977C8` |

</details>

## Related

- [keymap.ini](keymap-file.md) - the keyboard bindings.
- [Control names](control-names.md) - the codes the pad buttons use.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 9 calls with 5 other topics</summary>

**Application** (explained on [game application](../Engine-Core/game-application.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00584740`](../Compiler-And-C-Runtime/memory-and-allocation.md) (on memory and allocation) | is called by | [`0x001A98B0`](../World-Areas-And-Travel/map-art.md) (on map art) |

**Sound and music** (explained on [audio manager](../Sound-And-Music/audio-manager.md), [sound engine](../Sound-And-Music/sound-engine.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00584740`](../Compiler-And-C-Runtime/memory-and-allocation.md) (on memory and allocation) | is called by | [`0x002125A0`](controllers.md)<br>[`0x00225C40`](controllers.md)<br>[`0x006794D0`](../Sound-And-Music/sound-engine.md) (on sound engine) |

**Platform** (explained on [phyre post effect classes](../PhyreEngine/phyre-post-effect-classes.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00584740`](../Compiler-And-C-Runtime/memory-and-allocation.md) (on memory and allocation) | is called by | [`0x00650D40`](controllers.md) |

**Game files and data tables** (explained on [game application](../Engine-Core/game-application.md), [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00584740`](../Compiler-And-C-Runtime/memory-and-allocation.md) (on memory and allocation) | is called by | [`0x001A11B0`](../Game-Files-And-Data-Tables/async-load-manager.md) (on async load manager)<br>[`0x001DAD60`](../Game-Files-And-Data-Tables/prefetch-manifests.md) (on prefetch manifests)<br>[`0x00637C50`](../PhyreEngine/phyre-asset-files.md) (on phyre asset files) |

**Scripts and script commands**

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00290180`](controllers.md) | is called by | [`0x003423E0`](controllers.md) |

</details>
