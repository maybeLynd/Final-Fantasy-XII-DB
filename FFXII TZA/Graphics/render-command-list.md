---
title: "Render command list: the per-frame command objects, the two lists that hold them and the walks that run them"
kind: "system"
category: "Graphics"
addresses: "0x01F7F5E0, 0x01F7F5E8, 0x00186CD0, 0x0018B480, 0x0018AD00, 0x0018C9E0, 0x0018B4E0, 0x0018CA40, 0x0018AFF0, 0x0018C610, 0x00212CC0, 0x0018B100, 0x0018B1B0, 0x0018B510, 0x0018B030, 0x0018B070, 0x0018B0B0, 0x0018B040, 0x0018B810, 0x0018C8F0, 0x00187950, 0x0022A580, 0x001F28B0, 0x00193D50, 0x01DFE0C4, 0x001BDA50, 0x003A1D50, 0x003A1DB0, 0x004FE420, 0x02EBEFC0"
---

## What the player sees

The picture is built in layers: opaque characters and maps, ambient occlusion, water and its
refraction, subsurface scattering, post-processing, the PS2-style depth of field, a Gaussian filter,
video and the scene brackets. Each layer is a small job object the frame creates, files in a list
and runs later; the next frame creates them again.

Five developer-console toggles act on this list directly. Turning off "Enable Map Display" (command 34),
"Enable Character Display" (command 35) or "Enable UI Display" (command 37) drops every map, character or
font-border job from the walks; "Enable VFX Display" (command 38) sets or clears one more bit of the list's
mask; and "Display AO Only" (command 42) stops the second
half of the list at the first job after ambient occlusion has run, so the screen shows the
ambient-occlusion result alone ([debug menu commands](../Engine-Core/debug-menu-commands.md)).

## How it works

### Two lists, one owner

The render-manager installer `0x00186CD0` creates both lists once, at `0x00186D00` and `0x00186D0F`:

- `0x0018B480` allocates the 0x30-byte ordered command list (`0x0018B4AB`) and stores it at `0x01F7F5E0`.
  Its constructor `0x0018AD00` zeroes begin, end and capacity end (`0x0018AD1D`–`0x0018AD24`), sets the class mask
  `+0x20` to `0xFFFFFFFF`, reserves 5,000 entries (`0x0018AD40`, through `0x0018B320`, which allocates them because
  the new list's capacity is below 5,000, `0x0018B342`), and sets the split `+0x24` to 0 and the mark `+0x2C` to -1.
- The same constructor writes a 16-bit zero at `+0x29` (`0x0018AD50`), clearing the opaque-pass byte `+0x29` and the
  afterwater byte `+0x2A`; it does not write the split-armed byte `+0x28`, and it returns the list (`0x0018AD5B`).
- `0x0018C9E0` allocates the 0x20-byte owner list (`0x0018C9F9`) and stores it at `0x01F7F5E8`, with
  begin, end and capacity all zero (`0x0018CA10`–`0x0018CA19`).
- Both creators return at once while their global is already set (`0x0018B4A9`, `0x0018C9F7`); `0x0018B480` first
  hands the test that `0x01F7F5E0` is null to the return stub `0x0016D6A0` (`0x0018B49D`). Each takes its block from
  `0x00210EC0` (`0x0018B4AE`, `0x0018C9FE`), fills it only when the block is non-null (`0x0018B4BB`, `0x0018CA0E`), and
  stores 0 in its global when the allocation fails (`0x0018B4C8`, `0x0018CA32`).

Both are EASTL pointer vectors ([EASTL strings and containers](../Third-Party-Libraries/eastl-strings-and-containers.md)).
Each constructor passes the name `"EASTL vector"` (`0x008C5F58`) to `0x001EDF00`, whose whole body
stores the allocator vtable `0x00902720` and never reads the name. The getters are `0x0018B4E0` (ordered
list) and `0x0018CA40` (owner list); `0x0018B4E0` hands its null test to `0x0016D6A0`, a bare `ret`.

### Enqueueing a command

Every allocating producer is one builder per class, 36 of them from `0x0018B540` to `0x0018CCF0`.
`0x0018C610(owner, mode)` (`PostProcessObj`) shows the shape:

1. `malloc` the 0x20-byte object (`0x0085E730`, `0x0018C62F`, `0x0018C632`) and run the class constructor
   (`0x001F1B80`) with `mode` (`0x0018C646`); a failed allocation leaves a null (`0x0018C655`);
2. append the pointer to the owner list inline (`0x0018C65C`–`0x0018C673`), or through the grow routine
   `0x001AB570` (`0x0018C680`) when full;
3. tail-jump `0x0018AFF0(0x0018B4E0(), object)` (`0x0018C69F`) to append the same pointer to the ordered list.

A null is therefore appended to both lists. The owner list starts with no capacity and grows from its
first append. The ordered list starts with 5,000 reserved entries; `0x0018AFF0` appends in place while the end is
below the capacity end (`0x0018B000`), and the 5,001st append goes through the same grow routine `0x001AB570`
(`0x0018B020`), which doubles the capacity, `n = ([+0x08] - [+0x00]) >> 3` held and `n ? 2 * n : 1` new
(`0x001AB5D5`-`0x001AB5FD`, the doubling at `0x001AB5F0`), and moves the entries. The 36 builders
allocate 0x18 bytes (15 classes), 0x20 (16), 0x28 (3) or 0x30 (2).

Each class constructor starts with the base `0x00212CC0` and stores its argument after the base
fields. `RazorMarkerPushObj`'s `0x001F1C30` takes a zeroed 0x200-byte buffer (`0x00210EC0`) at `+0x18`
and copies the marker name into it, at most 0x1FF characters. `SetRendererCameraObj`'s `0x001F1E80`
keeps the camera at `+0x18` and copies the render manager's byte `+0x1C` to `+0x20`.
`SetScreenIndexToPostProcessManagerObj`'s `0x001F1ED0` keeps the screen index at `+0x18`.

Four other functions call `0x0018AFF0` and append to the ordered list only, so the owner list never
destroys what they add: `MapRenderObject`'s slot 1 `0x001E5270` (its `MapOrderedObject` at `+0x10`),
`CharacterRenderObject`'s slot 1 `0x001F89B0` (its `CharacterOrderedObject` at `+0x28`, when
non-null), the text flush `0x001E8580`, and `0x001F48B0`, which wraps a Gi render command in a
`GeometryInstanceOrderedObject` taken from the command arena `[0x01F7F4C0]` ([Gi render commands](gi-render-commands.md)).

### The game-side wrappers

Small wrappers file fourteen of the classes. They check that the owner list
(`0x0018CA40`) or the render manager (`0x00189120`) exists and pick the arguments:

| Wrapper | Builder | Class | What the wrapper adds |
|---|---|---|---|
| `0x00182220`, `0x00182250` | `0x0018B670`, `0x0018B5D0` | `BegineSceneObj`, `BegineScene0Obj` | argument 0; sets `0x01F7F538` to 1 |
| `0x001823B0`, `0x001823E0` | `0x0018BE70`, `0x0018BDD0` | `EndSceneObj`, `EndScene0Obj` | clears `0x01F7F538` |
| `0x0017F2A0`, `0x00182A60`, `0x00182AD0` | `0x0018B8B0` | `CopyBufferObj` | the source target, below |
| `0x0017F330` | `0x0018BB70` | `CopyFrontBufferForWaterRefraction` | only when the map-art byte `+0x2E5` is set (`0x001A94B0`) |
| `0x00180A30` | `0x0018C2A0` | `RenderAfterWaterObj` | with that byte set, first `0x001A8F80` on the map-art context |
| `0x0017F670`, `0x0017F6B0` | `0x0018C450` | `MaskBorderObj` | `0x0017F670(n)` only when `0x01DF08E8` and `0x01F7F4F0` are set; `0x0017F6B0` passes 3 under its own tests |
| `0x00182280` | `0x0018B710` | `FastClearObj` | through `0x00185CD0`, which also keeps the four arguments at manager `+0xD00`-`+0xD0C` |
| `0x00185A10`, `0x001860E0` | `0x0018CBC0` | `SetRendererCameraObj` | the camera at manager `+0x358` with `+0x1C` = 1, or `+0x690` with `+0x1C` = 0 |
| `0x00183120` | `0x0018CB30` | `SetPrimIdEnableObj` | only when `0x005C5230()` is non-zero; it returns 0, so nothing is filed |
| `0x001EB110` | `0x0018C0D0` | `RazorMarkerPopObj` | only when `[0x01F7F4E0]` exists and its byte `+0x08` is set, as for the push `0x001EB150` |
| `0x001826E0` | `0x0018B970` | `CopyDepthBufferObj` | the render parameters' `+0x2B8` (`0x00193D50`), 0, 0 |
| `0x0017ECF0` | `0x0018C740` | `AmbientOcclusionObj` | nothing |

`0x0017F6B0` files `MaskBorderObj` with 3 when the owner list exists and one of these holds:
`0x01DF08EC` and `0x01F7F4F0` are both set, `0x01F7F4F4` is set, `0x01F7F4F8` is set (the effect draw sets
it for the frame), `0x01F7F500` is set (by `0x00184740` while effect `0x17A` plays), or the movie
player is in state 3 (`0x001B7D20`).

`0x00229F20(water)`, called from the scene draw `0x0022B0B0`, files the ambient-occlusion pass when `0x01FD49E8`
is set: the scope `AO render`, `MaskBorderObj(1)` and a depth copy; with `water` non-zero the scope
`Water effect`, the water refraction copy, `RenderAfterWaterObj`, a pop and another depth copy; then
`AmbientOcclusionObj` and a pop. `0x00182560` returns `0x01F7F538`, the scene-open dword the scene wrappers
write; `0x00183060(x)` stores `x != 0` in `0x01F7F50E`, which `0x0017FE50` returns.

`0x001809E0`, also in the frame bodies, runs `0x001A5A70` and `0x001AA2C0` on the map-art context when its
byte `+0x2E5` is set.

The copy source comes from the render manager's target tables:

- `0x0017F2A0(arg, entry)` takes the entry's target unless its byte `+0x08` is set, and passes 0 and 0.
- `0x00182A60(arg, which, n)` takes `0x00186910(manager, which != 0)` and passes `n` and 1;
  `0x00182AD0(arg, target, n)` passes its own target, `n` and 0.
- `0x001867B0` returns target `+0xB08 + 8 × [+0xC30]`. `0x00186A50` returns `+0xB48 + 8 × [+0xDD0]`, or
  `+0xB50 + …` while `+0xDBB` is set. `0x00186A00` takes `+0xB50` only when the render parameters' byte
  `+0x4A0` is also set (`0x0017F280`). `0x00186910` returns the first or `0x00186A00`'s choice.
- `0x001868A0` and `0x00186840` are `0x00186A50` and `0x00186A00`, each calling `0x001EDDA0` first when
  `0x001EDE70()` is set. `0x0017FDE0`, `0x0017FE60(i)` and `0x0017FEE0(i)` return the target of `0x001867B0`,
  of `0x00186840` or `0x001868A0`, and of `0x00186A00` or `0x00186A50`, or 0 when its byte `+0x08` is set.

- `0x00189530(manager, flag)` copies the target pointer at `+0xB28` (flag set) or `+0xB30` into the
  first table entry `+0xB08`. Its one caller, `PostProcessObj`'s execute `0x001F3300`, passes 0 after
  the post-process work for the screen index `0x01F82EC0` when the device byte `+0xD48` of
  `0x00796E20()` is set, and otherwise copies the result back with `0x001EE8E0`.
- `0x001EEE80(target, w, h)` resizes a target's texture (`0x0060DD70`, same format) when its size `+0x28`/`+0x2C` differs,
  unbinding it first when it is bound (`0x00625F00`, `0x0062BCB0`); `0x001EE180(target, b)` unbinds the same way and stores
  `b` in the target's byte `+9`. Both skip a null target, one whose byte `+0x08` is set, or one with no texture at
  `+0x00`.
- The target rebuild `0x00188B10` resizes ten of the manager's targets to the fit size (`0x00182EB0`, `0x00182E80`)
  and copies `+0xB28` into `+0xB08` (`0x00188B8A`); `0x00188DA0` gives four of them
  `0x02CB8084` through `0x001EE180`.
- The rebuild then calls `0x0060F6B0` on the device `+0x08` with 0, 0, W, H and 0, W x H being 3840 x 2160 when
  byte `+0xDB8` is set or `+0xC30` is 3 and `+0xAD8` x `+0xADC` otherwise (`0x00188CF0`-`0x00188D46`), and at its end
  sets byte `+0xDCC` to 1 (`0x00188D81`).
- The rebuild also prunes the object `[0x01F81210]` (`0x001B6C40`), which `0x00182CA0` and `0x00182B40`
  use: `0x001B6B50` removes every entry for which `0x001B6A70` returns 1, after that function has
  queued the `+0x20` of each node of the entry's list `+0x78` for a deferred call to `0x001B6C30`
  (`0x00185A90`) and emptied its map `+0x70`; it returns 1 when the entry's `+0x60` is 0.

The other accessors read the manager: `0x00182410` its byte `+0xDB9`, `0x00182570` its byte `+0x1C`,
`0x00182490(&w, &h)` the width and height (`0x00182EB0`, `0x00182E80`). `0x001824E0(a, b, c)` fills three
values through `0x00186AB0`: from `0x0018A620()` `+0xD8`, `+0xDC`, `+0xD0`, or, when the `0x001D50D0` object's
byte `+0xC0C` is set, from its `+0xC10`, `+0xC18`, `+0xC14`.

`0x00185A80(manager, n)` adds `n` to the manager's counter `+0xDBC`. The character draw `0x001F5D70`
adds, for each mesh instance it draws, the low 31 bits of the first dword the instance points to
(1 for the single-mesh path), and the map draw
`0x001E2AF0` adds its own counts; the render pass list `0x00187950` copies the total to `+0xDC0` and
clears `+0xDBC` at the start of each frame.

### The command object

The base constructor `0x00212CC0` stores the `OrderedObject` vtable `0x009010B8`, zeroes `+0x08` and
sets the byte `+0x10` to 1 (`0x00212CD5`). The base class's slots 1 and 2 are `0x00861EC6`, the
pure-virtual thunk, so every concrete class supplies three slots: slot 0 destroys, slot 1 executes
with `(object, device)`, slot 2 returns the class key.

Two classes read `+0x08` in their execute slot and forward it as the callee's object:
`MapOrderedObject`'s `0x00212C60` calls `0x001E2AF0` with it when non-null, and
`CharacterOrderedObject`'s `0x00215320` tail-jumps `0x001F5D70` with it.

### The class key is a mask, and nothing sorts

Slot 2 returns a constant for most classes. Both walks AND it with a mask; neither compares two
entries, so the list runs in the order the jobs were appended:

| Key | Slot 2 | Classes |
|---|---|---|
| `0x1` | `0x0053DD10` | the scene brackets, the Razor markers, the MSAA, depth-of-field and primitive-id toggles (11) |
| `0x2` | `0x00290180` | `CharacterOrderedObject` |
| `0x4` | `0x0016EE70` | `MapOrderedObject` |
| `0x10` | `0x001F2880` | the ordinary passes (18) |
| `0x20` | `0x00212E20` | the three `FontBorderOrdered*` classes |
| `0x80` | `0x001F28A0` | `VideoObj` |
| `0x100` | `0x001F2890` | `RenderOpaqueObj`, `RenderAfterWaterObj`, `RenderMapOpaqueObj`, `RenderMonsterGalleryChara` |
| `[+0x18]` | `0x00879750` | `GiResetRenderTargetObj`, `GiResetDefaultRenderTargetObj` (the constructor's argument) |
| `[+0x20]` | `0x001F49E0` | `GeometryInstanceOrderedObject` (the mask `0x001F48B0` was given) |

Besides the constructor, four setters write the list's own mask. Each sets one bit of `+0x20` when its
argument is not 0 and clears it otherwise, and each is called from two sites of one console command, one
passing 1 and one passing 0, with the ordered list from `0x0018B4E0`:

| Setter | Bit | Call sites | Console command | Classes whose fixed key is the bit |
|---|---|---|---|---|
| `0x0018B080` | `0x4` | `0x001D1BED`, `0x001D1C01` | 34 "Enable Map Display" | `MapOrderedObject` |
| `0x0018B070` | `0x2` | `0x001D1C29`, `0x001D1C3D` | 35 "Enable Character Display" | `CharacterOrderedObject` |
| `0x0018B090` | `0x20` | `0x001D1C65`, `0x001D1C79` | 37 "Enable UI Display" | the three `FontBorderOrdered*` classes |
| `0x0018B0A0` | `0x40` | `0x001D1CB0`, `0x001D1CC4` | 38 "Enable VFX Display" | no class in the table above |

Commands 34, 35 and 37 flip a byte (`+0xABC`, `+0xABD`, `+0xABE` of the debug-menu object); command 38
steps `+0xAC0` through 0, 1 and 2 and sets bit `0x40` while the value is not 0. Turning character
display off drops every `CharacterOrderedObject` from every walk, and the map and UI toggles do the
same for their classes.

### The two parts of a frame

At the head of each frame the state machine `0x0022A580` calls the split setter twice through
`0x00183100` → `0x0018CB10` → `0x0018B510`. `0x0018B510` stores whether its argument is non-zero at `+0x28`
and then sets the split `+0x24` to 0 when it is, or to the current count when it is not:

1. `0x00183100(1)` at `0x0022A5AC` sets the split to 0;
2. the frame-open producers run for screen 0: `0x001829A0` (`SetScreenIndexToPostProcessManagerObj`),
   `0x001EC490` (`ApplyJsonForCutSceneObj`) and `0x00214C30` (the depth-of-field commands); between the first two
   `0x00358640(0)` (`0x0022A5BA`) only stores 0 in the draw byte `0x022C7F98` and appends no command;
3. `0x00183100(0)` at `0x0022A5CF` sets the split to the count, so `[0, split)` holds exactly the frame-open commands.

The render body `0x00187950` (application slot 8, [game application](../Engine-Core/game-application.md))
then walks the list with `0x0018B100(list, part, device)`, where `device` is the render manager's
`+0x08` (`0x00187CFF`, `0x00188122`):

- part 1 at `0x00187D05`, entries `[0, split)`;
- the profile scope `"render ordered objects"` (`0x008C5E28`, `0x001880E7`);
- part 0 at `0x00188128`, entries `[split, count)`;
- the teardown pair at `0x00188204` and `0x00188211`.

In order, the body does this:

1. It calls `0x001EE5D0` on `+0xDA0` and `+0xDA4` with the answers of `0x00182EB0` and
   `0x00182E80` and the settings dwords `+0xD24` and `+0xD28` (`0x0018797D`-`0x001879BB`), moves
   `+0xDBC` to `+0xDC0` and zeroes it (`0x001879C0`-`0x001879D1`), and queues on the device,
   through `0x005FEA50`, the
   callback `0x001D5FD0` and then `0x00186610` with the bank index `0x01F7F590`, which it steps
   to `(index + 1) & 3` (`0x001879D8`-`0x00187A0D`).
2. With byte `+0xDB8` set it runs `0x00187860`: here when `+0xDAC` is neither 3 nor 4
   (`0x00187A13`-`0x00187A2E`), and near the end, inside the scope `"output capture 4k
   images"`, when it is 3 or 4 (`0x00188565`-`0x001885A8`).
3. It copies `+0xB28` to `+0xB08`, sets `+0xB58` to `+0xB60` when `+0xDBA` is set and
   `+0xDB9` clear and to `+0xB68` otherwise, and copies `+0xDC8` to `0x01DF0900` while byte
   `+0x01` is set (`0x00187A33`-`0x00187A80`).
4. With
   `+0xDBA` set, `+0xDB9` clear and the multisample count `0x02CB8084` different from `0x01DF0900`,
   it queues `0x00189110` three times, each with a 16-byte record of target and count
   from `0x001A1470([0x01F7F4C0], 0x10)`, for `+0xB58`, the scene target and `+0xB18`, and
   then copies the count to `0x02CB8084` (`0x00187A88`-`0x00187B92`).
5. It takes the camera `+0x690`, or `0x0018A620() + 8` while byte `+0x00` of the object
   `0x0018A620()` answers is set, runs `0x001AC7C0` and `0x00189570` (`0x00187B98`-`0x00187BC2`),
   changes the camera in the two cases below and walks part 1 (`0x00187CEA`-`0x00187D05`).

   The two cases need that byte set. With console byte `+0xC0C` set and the step below -1
   or the dword `+0xB8` of `0x001AD440()` equal to 2, camera `+0xD0`, `+0xC8` and `+0xD4`
   take console `+0xC10`, `+0xC14` and `+0xC18`. With `+0xC0C` clear, console byte `+0xC24`
   set and the step below -1, camera `+0xD0` takes `+0x1E8` of `0x001AD440()`. Either case
   then runs `0x00189130`, `0x0018A120(camera + 8)` and `0x0018A680` (`0x00187BC7`-`0x00187CE5`).

6. While the step `+0xA8` of `0x001AD440()` is below 0 it sets byte `+0xC34` and, inside
   the scope `"update shadowmap"`, runs `0x001F0AD0(shadow object, device, block)`, the
   block being `+0x358` when byte `+0xDC5` is set (which it clears) and `+0x690`
   otherwise; it then clears `+0xC34` (`0x00187D0A`-`0x00187D80`). Every scope is opened by
   `0x001D5630([0x01F7F4E0], device, name)` and closed by `0x001D5620`.
7. It opens and closes the scope `"output cubemap images"` with nothing between and
   calls `0x001D7280(0x001D8210())` (`0x00187D87`-`0x00187DB6`).
8. Once, while the latch `+0xD10` is set, it clears the target `+0xB30` (only with the
   settings byte `+0xD48` set) and the target `+0xB10`: `0x005DC190`, `0x0060D4F0`, the
   viewport `0x0060F6B0(device, 0, 0, w, h, 0)`, `0x0060D190`, `0x005FEFD0(device, 1)` and
   `0x00600A60(device, 2)`. The size is 3840 by 2160 when `+0xDB8` is set or the scene
   index is 3, and `+0xAD8` by `+0xADC` otherwise (`0x00187DC9`-`0x00187FA3`).
9. In the same pass the code for clearing the target `+0xB40` (the same six calls, at
   3840 by 2160, with 0 in place of the 1.0 handed to `0x0060D190`) sits behind `0x005C5230()`
   answering non-zero and the dword `+0x18` being 0 (`0x00187FA8`-`0x0018805B`); `0x005C5230`
   only returns 0, so it never runs.
10. A non-zero answer of `0x0060D190`, `0x005FEFD0` or `0x00600A60` there ends the body with
    that answer (`0x00187E8A`-`0x00187EBF`, `0x00187F65`-`0x00187F9A`; the same tests at
    `0x0018801D`-`0x00188052` belong to step 9 and never run). So do the same calls of
    steps 16 and 18 (`0x00188322`, `0x00188356`, `0x0018843D`, `0x00188451`).
11. Inside the scope named at `0x008C5E00` it runs `0x00188730` (`0x00188060`-`0x0018808A`). It
    then sets the device camera with `0x0060CE50`: the shadow object's camera
    `+0x150 + 0xD8 × [+0x124]` while its dword `+0x120` is not 0, else `0x001EBA40() + 0x48`
    while that object's byte `+0x118` is set, else `+0x08` of the camera of step 5
    (`0x0018808F`-`0x001880E2`).
12. Inside `"render ordered objects"` it walks part 0. While render-parameter byte
    `+0x199` is set it zeroes the bytes `0x01DF08FC` and `0x01F7F594` before the walk and
    sets `0x01DF08FC` to 1 after it (`0x001880E7`-`0x00188144`).
13. Still inside that scope it runs `0x001D5520`, calls `0x001862B0(manager, x, y)` while
    render-parameter byte `+0x164` is set, zeroes `+0xAE0` while byte `+0x118` of
    `0x001EBA40()` is set, and calls `0x00609710(device)`, `0x005FEFD0(device, 0)` on a 0
    answer, and `0x00600A60(device, 2)` (`0x0018814A`-`0x001881F7`).
14. It runs `0x0018B040(0x0018B4E0())` and `0x0018B810(0x0018CA40())`. With console byte
    `+0xC0C` set it puts the camera's `+0xD0`, `+0xC8` and `+0xD4` back from manager
    `+0xCC4`, `+0xCC8` and `+0xCCC`. It runs `0x00188730` again (`0x001881FC`-`0x00188272`).
15. The debug lines are skipped when `+0xDB8` is set with `+0xDAC` not 0 and when
    `+0xCD4` is set. Otherwise they are drawn when the dword at `0x001C1990()` is not 0
    or, of `0x001C2F40()`, the dword `+0x0C` is not 0, the byte `+0x463C` is set or the
    list from `+0x4640` to `+0x4648` of `0x230`-byte entries is not empty.
16. The draw, inside `"render debug menu"`, is `0x0060DA50(device, 0, 1)`,
    `0x005FEFD0(device, 0)`, `0x0016D6A0`, `0x001C2DB0` and `0x00600A60(device, 2)`
    (`0x00188277`-`0x00188369`).
17. With render-parameter byte `+0x199` set, `0x001EE8E0` gets the first qword of the
    scene target, or 0 when that target's byte `+0x08` is set. Else,
    with byte `+0x4A0` set, the step below -1 and byte `+0x180` or `+0x188` set, colour
    grading `0x0018F8F0` runs inside `"Post Process : color correction"`, and only when
    `+0x180` is set (`0x0018836E`-`0x00188425`).
18. In every other case `0x00188730`, `0x005FEFD0(device, 0)` and `0x00600A60(device, 2)`
    run. `0x001EE8E0` then gets, in the same way, the `+0xD0` target of `0x001AD440()` when
    the step is -1 or above and the scene target otherwise (`0x0018842A`-`0x00188500`).

    The arm that would run `0x0018FD70` on the target `+0xB40` in its place needs the step
    below -1, `0x005C5230()` non-zero and the dword `+0x18` 0 (`0x0018848C`-`0x001884CA`);
    `0x005C5230` only returns 0, so it never runs.

19. The brightness pass `0x0018F6B0` follows (`0x00188505`-`0x00188529`); then, inside
    `"output capture images"`, `0x00187550` and `0x00186010` in that order
    (`0x0018852E`-`0x00188560`); then the scope of step 2.
20. It queues `0x001D5FD0` and `0x001D6000`, zeroes byte `+0xDCC`, runs `0x00188B10` when
    byte `+0x00` is set, else `0x00188DA0` when byte `+0x01` is set, zeroes `+0x02` and the
    scene index `+0xC30`, copies `+0xB28` to `+0xB08` again, adds 1 to
    `0x01F7F5A0` and answers 0 (`0x001885AD`-`0x0018861A`).
21. The getters used above: `0x00796E20()` gives the settings (`0x0018797D`, `0x00187DDD`),
    `0x001D50D0()` the console, `0x00193D50()` the render parameters, `0x001AD440()` the step
    object, `0x001F0850()` the shadow object (`0x00187D0A`) and `0x0018B4E0()` the object whose
    parts `0x0018B100(object, part, manager +0x08)` walks (`0x00187CF7`-`0x00187D05`,
    `0x0018811A`-`0x00188128`).
22. `0x0016D6A0`, which only returns, is called after each queue call of step 4, at the
    end of each clear of steps 8 and 9 whether or not it ends the body, and with
    `0x0018B4E0()` before the walk of step 5 (`0x00187CF2`). Step 8 zeroes its latch first
    (`0x00187DD6`). Each camera store of steps 5 and 14 is followed by a call of the
    camera's slot `+0x08`, and step 14 then calls `0x0018A120(camera + 8)` (`0x0018826A`).
23. Step 13 first calls `0x0018D320(render parameters, x, y)` and hands `0x001862B0` the
    values `2 × (x - 0.5)` and `2 × (1.0 - y - 0.5)` (`0x00188165`-`0x001881AC`). In step 5
    `0x001AC7C0` takes `0x001AD440()`, and `0x0018A680` takes `0x0018A620()` and
    `0x0018A620() + 8` (`0x00187BB2`-`0x00187BBA`, `0x00187CD1`-`0x00187CE5`).

For each entry the walk skips a null (`0x0018B159`), calls slot 2 once (`0x0018B164`), skips the entry
when the key does not meet the list mask (`0x0018B167`), and calls slot 1 with the device (`0x0018B187`).

### Display AO Only

Between the mask test and the execute, `0x0018B16C`–`0x0018B17C` leave the walk (to `0x0018B192`) when
byte `0x01DF08FC` is 0 and byte `0x01F7F594` is not. `AmbientOcclusionObj`'s execute `0x001F28B0` sets
`0x01F7F594` to 1 at `0x001F29A3`, on the path that runs only after both of its gates (render-parameter
byte `+0x198` and `0x01DFE0C4`) passed.

Before part 0 the render body tests render-parameter byte `+0x199` (`0x00188103`) and, when it is
set, zeroes both bytes (`0x0018810C`, `0x00188113`); after part 0 it reloads `0x01DF08FC` and sets it
again when `+0x199` is still set (`0x00188132`–`0x00188144`). Console command 42 flips `+0x199`. With
it on, part 0 runs up to the ambient-occlusion job and stops at the next job that passes the mask.

### Class-filtered walks

`0x0018B1B0(list, device, mask, reverse)` runs only entries whose key meets both the caller's mask and
the list mask, calling slot 2 twice per entry (`0x0018B247` and `0x0018B258`, `0x0018B2D3` and `0x0018B2E4`).
Its range comes from the mark `+0x2C` and the render-parameter word `+0x49C` (read by `0x0018D630`):

| Mark | `+0x49C` | Reverse (`0x0018B1D4`) | Forward (`0x0018B280`) |
|---|---|---|---|
| -1 | any | count-1 down to 0 | 0 to count-1 |
| m | 0 | m-1 down to 0 | 0 to m-1 |
| m | non-zero | count-1 down to m | m to count-1 |

The mark is set by `0x0018B030`, which stores the current count, through `0x001829F0`; `MainLoop_Draw`
`0x0022B0B0` calls it at `0x0022B112` when it starts draw 1. Entries before the mark therefore belong to
draw 0 and the frame open, entries from it to draw 1.

The opaque passes are themselves list entries whose execute runs a nested reverse walk, after
setting a pass byte on the list that the character draw body `0x001F5D70` reads:

| Execute | Class | Walk | Pass byte |
|---|---|---|---|
| `0x001F36B0` | `RenderOpaqueObj` | mask 2, reverse (`0x001F370C`) | `+0x29` |
| `0x001F3570` | `RenderMapOpaqueObj` | mask 2, reverse (`0x001F35D0`), then mask 4 (`0x001F361B`) | `+0x29` |
| `0x001F3650` | `RenderMonsterGalleryChara` | mask 2, reverse (`0x001F3689`) | `+0x29` |
| `0x001F3510` | `RenderAfterWaterObj` | mask 2, reverse (`0x001F3549`) | `+0x2A` |

Each sets its byte to 1 before the walk and to 0 after it. A sixth caller, `0x001F06D0`, walks forward
with mask 6 (characters and maps) at `0x001F07C7`.

### Removal and teardown

`0x0018B0B0(list, object)` replaces every entry equal to `object` with null and keeps the count;
`CharacterRenderObject`'s slot 3 `0x001F6D60` calls it (`0x001F6D96`) before freeing its
`CharacterOrderedObject`. Null entries are why every walk tests for them.

Three teardowns empty the lists, each clearing the ordered list before the owner destroys:

| Site | Clear | Owner |
|---|---|---|
| render body `0x00187950` | `0x00188204` | `0x0018B810` at `0x00188211` |
| frame tick `0x0017CCD0` | `0x0017CD53` | `0x0018B810` at `0x0017CD60` |
| frame-end reset `0x001E0590` | `0x001E05A9` | `0x0018C8F0` at `0x001E05B6` |

`0x0018B040` clears the ordered list: `0x0018B3F0(list, 0)` moves the end back to the begin, then the
split is set to 0 and the mark to -1 (`0x0018B050`, `0x0018B057`); no object is touched. `0x0018B810`
calls each non-null object's slot 0 with `edx = 1` (`0x0018B860`), which frees it, and empties the
owner list. The frame tick runs its pair only while byte `0x01FD4A88` is set (`0x0017CD42`) and stores 0
there afterwards (`0x0017CD73`); those are the only two instructions that name the byte.

### The flush

`0x0018C8F0`, used by the frame-end reset, first executes every owner entry whose byte `+0x10` is 0
(`0x0018C933`) with the device `[0x00189120() + 8]` (`0x0018C939`–`0x0018C948`), then destroys every
non-null entry (`0x0018C987`) and empties the list. The execute loop has no null test, so a null left
on the owner list faults at `0x0018C933`.

Exactly four constructors clear `+0x10`: `ApplyJsonForCutSceneObj` (`0x001F1799`), `EnableDofObj`
(`0x001F196A`), `ReadPresetDofForCutSceneObj` (`0x001F1CE4`) and `SetDofObj` (`0x001F1E3E`). These are the
settings commands, so a flush applies the pending cutscene and depth-of-field settings even when no
walk ran them.

### What the execute bodies read

- Byte `0x01DFE0C4` is 1 in the image and is written only by `0x001F2870` (from `cl`) and `0x001F39B0`
  (1). The ambient-occlusion (`0x001F28CB`), Gaussian (`0x001F30E8`), post-process (`0x001F330A`) and
  subsurface-scattering (`0x001F3749`) executes do no work while it is 0.
- `AmbientOcclusionObj` (`0x001F28B0`) runs when render-parameter byte `+0x198` is set (`0x001F28BE`).
- When the device's bit `0x1` bracket is open (`0x00609710`, `0x001F28F4`), that execute first closes it with
  `0x00600A60(device, 6)` (`0x001F2909`). It then calls `0x0018F510(block, device, a, b, c, d)` (`0x001F2969`),
  the ambient-occlusion pass on [post-processing](post-processing.md), with the render manager's
  `a = [+0xB08 + 8 × [+0xC30]]` (`0x001867B0`), `b = [+0xB10]` (`0x001867C0`), `c = [+0xB58]` (`0x00186660`) and
  `d = [+0xB18]` (`0x001867A0`).
- After `0x0018F510` the same execute calls `0x00188730` on the render manager (`0x001F2976`), reopens the
  bracket with `0x005FEFD0(device, 0)` when it closed it (`0x001F299E`), and sets `0x01F7F594` to 1 (`0x001F29A3`).
- `GaussianFilterObj` (`0x001F3090`) runs when any of `+0x19A`, `+0x3E8` or `+0x180` is set (`0x001F309E`–`0x001F30BA`).
- `PostProcessObj`'s constructor `0x001F1B80` stores its mode at `+0x18` and sets the screen index
  `0x01F82EC0` to 0 for mode 0 or increments it otherwise (`0x001F1BB5`); it is the index's only writer.
- `ApplyJsonForCutSceneObj`'s execute `0x001F29C0` passes its `+0x18` to `0x001C3C30` and ignores the device.

### The render-parameter block

`0x00193D50` returns the 0x4A8-byte block kept at `0x01F7F5F0`, creating it on first use with the
constructor `0x0018CD90`; `0x0015CAF0` copies the same pointer to `0x01F81300`. The fields this page uses
are the switches `+0x180`, `+0x198`, `+0x199`, `+0x19A`, `+0x3E8` and the walk selector `+0x49C`,
which the constructor sets to 0 (`0x0018D033`). The constructor also sets the render size
`+0x2E0`/`+0x2E4` to 1920 × 1080 (`0x0018CF61`, `0x0018CF6B`). The block's post-processing fields are on
[post-processing](post-processing.md).

### The character render-object manager

The installer also calls `0x001BDA50` (`0x00186CFB`), which allocates the 0x108-byte manager at
`0x01F81248` (constructor `0x001BC9D0`, getter `0x001BDAB0`). `0x001BDA50` first hands the test that `0x01F81248` is
null to the return stub `0x0016D6A0` (`0x001BDA6D`) and returns at once while the pointer is set (`0x001BDA79`);
otherwise it takes `0x00210EC0(0x108)`, runs `0x001BC9D0` only on a non-null block and stores the result, 0 when
the allocation fails (`0x001BDA9A`). Its first 0x20 bytes are the same pointer
vector, reserved to 50 entries through `0x0018B320` (`0x001BCACC`).

`0x001BD4A0` creates a 0x668-byte `CharacterRenderObject` (`0x001F4DA0`) when its map has no object for the
key and increments `+0xFC` (`0x001BD54F`). `0x001F6E70` increments `+0x100` with a locked `xadd`
(`0x001BD7D0`, from `0x001F7739`). `0x001BD620` reports whether the two counts are equal, and `0x001800C0`
returns 1 while they differ; the field frame tests it at `0x0022ABC2` to decide whether the simulation
tick runs ([frame update order](../Engine-Core/frame-update-order.md)). The render objects
themselves are on [character render object](character-render-object.md).

### The GS command buffers

Beside the object list the frame keeps two flat buffers of 16-byte GS register records. `0x003A1D50`
(from `0x0036F4D0`) clears the two 0x18-byte records `0x02EBEFC0` and `0x02EBEFD8` (`0x004FE3C0`), sets the
fill index `0x02EBEFF0` to 0, and points each at 512 records of the arena `[0x01FD4A78]` through
`0x004FE420(record, 0x200, offset)`: the first at offset 0, the second at offset 0x200 records.
`0x003A1E10(count, offset)` re-points both the same way.

`0x004FE420(record, count, offset)` first releases the record's block through `0x003EC8A0` while its `+0x14` is 0
(`0x004FE42F`-`0x004FE43E`); `0x003EC8A0` frees `+0x00` with `0x003697F0` when it is set and zeroes it. It then sets
`+0x14` to 1 and zeroes `+0x00`, `+0x08` and `+0x10` (`0x004FE446`-`0x004FE454`), and a count of 0 leaves the
record so (`0x004FE45B`).

With a non-zero count `0x004FE420` points `+0x00` and `+0x08` at `[0x01FD4A78] + offset * 16` and stores the
count at `+0x10` (`0x004FE463`-`0x004FE485`). When `offset << 5` is above `0x80000` in an unsigned compare, which
includes every negative offset, it first writes 0 to address 0 (`0x004FE46E`-`0x004FE47E`), a deliberate fault.

Producers append through the current record's write cursor `+0x08`, 0x10 bytes per record.
`0x003A1DB0`, called from 47 sites in 38 functions, flips `0x02EBEFF0`, passes the old buffer's begin and
record count to `0x0036F360`, resets the new buffer's cursor to its begin and returns that record.
`0x0036F360` and the register batch `0x0036D400` are on [graphics thread handshake](graphics-thread-handshake.md).

### The map's pair of buffers

A second pair of the same 0x18-byte records, `0x02EBB700` and `0x02EBB718` with the index `0x02EBB730`,
serves the map draw-list build `0x002F5550`.

- `0x00465F60(n)`, called with `0x100` from `0x0036F4D0` just before `0x003A1D50`, clears both records
  (`0x004FE3C0`), zeroes the index and gives each a block of its own of `n` records through
  `0x004FE3D0`, which allocates with `0x003EC8D0(6, n × 16)`.
- `0x00466070(count, offset)` re-points them: for an offset of 0 or more into the arena `[0x01FD4A78]`
  at `offset` and `count + offset` (`0x004FE420`), for a negative offset back to blocks of their own
  (`0x004FE3D0`).
- `0x002F5550` calls it with `0x100` and 0, then `0x004660F0`, which flips the index and resets the new
  buffer's cursor, and `0x00465FF0`, which appends two records to the other buffer: the first with
  `0x10000000` in its first and last dwords, the second `{0x70000000, 0}` (`0x0046601A`–`0x00466043`).
- `0x00466120`, which `0x002F5550` also calls, does nothing: both its calls go to `0x005C5230`, which
  returns 0.

## Layouts

Ordered command list ([`0x01F7F5E0`]), `0x30` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | begin |  |
| `+0x08` | `void*` | end | append cursor |
| `+0x10` | `void*` | capacity end | 5,000 entries reserved by `0x0018AD00` |
| `+0x18` | `void*` | allocator | vtable `0x00902720` |
| `+0x20` | `u32` | class mask | `0xFFFFFFFF`; bits `0x2`, `0x4`, `0x20`, `0x40` set or cleared by `0x0018B070`-`0x0018B0A0` |
| `+0x24` | `u32` | split | `0x0018B510`; 0 after a clear |
| `+0x28` | `u8` | split armed | `0x0018B510`: argument != 0 |
| `+0x29` | `u8` | opaque pass | 1 during the nested walks of `0x001F36B0`, `0x001F3570`, `0x001F3650` |
| `+0x2A` | `u8` | afterwater | 1 during the nested walk of `0x001F3510` |
| `+0x2C` | `i32` | mark | `0x0018B030`; -1 after a clear |

Owner list ([`0x01F7F5E8`]), `0x20` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | begin |  |
| `+0x08` | `void*` | end |  |
| `+0x10` | `void*` | capacity end | 0 at creation |
| `+0x18` | `void*` | allocator | vtable `0x00902720` |

Command object (OrderedObject), `0x18` bytes and up:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | three slots: destroy, execute(object, device), class key |
| `+0x08` | `void*` | target | 0 from `0x00212CC0`; forwarded by `0x00212C60` and `0x00215320` |
| `+0x10` | `u8` | flush select | 1 from `0x00212CC0`; 0 for the four settings commands |
| `+0x18` | `...` | class fields | PostProcessObj: u32 mode; GiReset*: u32 key; SetDofObj: u8 `+0x18`, f32 `+0x1C`, f32 `+0x20` |

GeometryInstanceOrderedObject (vtable `0x00903920`), `0x28` bytes from [`0x01F7F4C0`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x18` | `void*` | Gi command | `0x001F4950` |
| `+0x20` | `u32` | class key | `0x001F4950`, returned by `0x001F49E0` |

GS command buffer record (`0x02EBEFC0`, `0x02EBEFD8`), `0x18` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | begin | [`0x01FD4A78`] + offset * 16 |
| `+0x08` | `void*` |  | write cursor |
| `+0x10` | `u32` | capacity | `0x200` |
| `+0x14` | `u32` | ready | 1 after `0x004FE420`; while it is 0, `0x004FE420` frees `+0x00` first (`0x003EC8A0`) |

The command classes and their vtables, in vtable order from `0x00902F90` (stride 0x20):

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x00902F90` | `...` | SetRendererCameraObj |  |
| `0x00902FB0` | `...` | BegineSceneObj |  |
| `0x00902FD0` | `...` | EndSceneObj |  |
| `0x00902FF0` | `...` | BegineScene0Obj |  |
| `0x00903010` | `...` | EndScene0Obj |  |
| `0x00903030` | `...` | CopyBufferObj |  |
| `0x00903050` | `...` | CopyDepthBufferObj |  |
| `0x00903070` | `...` | Ps2DofObj |  |
| `0x00903090` | `...` | SetScreenIndexToPostProcessManagerObj |  |
| `0x009030B0` | `...` | ApplyJsonForCutSceneObj |  |
| `0x009030D0` | `...` | ReadPresetDofForCutSceneObj |  |
| `0x009030F0` | `...` | RenderMonsterGalleryChara |  |
| `0x00903110` | `...` | MonsterGallerySoftParticleEnable |  |
| `0x00903130` | `...` | RenderMapOpaqueObj |  |
| `0x00903150` | `...` | RenderOpaqueObj |  |
| `0x00903170` | `...` | RenderAfterWaterObj |  |
| `0x00903190` | `...` | MaskBorderObj |  |
| `0x009031B0` | `...` | RenderSSSObj |  |
| `0x009031D0` | `...` | PostProcessObj |  |
| `0x009031F0` | `...` | AmbientOcclusionObj |  |
| `0x00903210` | `...` | GaussianFilterObj |  |
| `0x00903230` | `...` | CopyFrontBufferForVFXObj |  |
| `0x00903250` | `...` | CopyFrontBufferForChrRefraction |  |
| `0x00903270` | `...` | CopyFrontBufferForWaterRefraction |  |
| `0x00903290` | `...` | ZBufferObj |  |
| `0x009032B0` | `...` | VideoObj |  |
| `0x009032D0` | `...` | RazorMarkerPushObj |  |
| `0x009032F0` | `...` | RazorMarkerPopObj |  |
| `0x00903310` | `...` | FastClearObj |  |
| `0x00903330` | `...` | DisableMsaaObj |  |
| `0x00903350` | `...` | EnableMsaaObj |  |
| `0x00903370` | `...` | SetPrimIdEnableObj |  |
| `0x00903390` | `...` | EnableDofObj |  |
| `0x009033B0` | `...` | SetDofObj |  |
| `0x009033D0` | `...` | GiResetRenderTargetObj |  |
| `0x009033F0` | `...` | GiResetDefaultRenderTargetObj |  |

Outside the block: `MapOrderedObject` `0x009010D8`, `GeometryInstanceOrderedObject` `0x00903920`,
`CharacterOrderedObject` `0x00903940`, and `FontBorderOrderedObject`, `FontBorderOrderedGaussObject`,
`FontBorderOrderedResetObject` at `0x00906D50`, `0x00906D78`, `0x00906DA0`, whose fourth slot `0x00225580`
stores its argument at `+0x18`.

Per-slot tables and instruction-level access lists beside this page:

| Subject | Table |
|---|---|
| every class's slots | [`render-command-list-ordered-object-vtable-slots.tsv`](render-command-list-ordered-object-vtable-slots.tsv) |
| the ordered command list | [`render-command-list-ordered-command-list-accesses.tsv`](render-command-list-ordered-command-list-accesses.tsv) |
| the owner list | [`render-command-list-render-command-owner-list-accesses.tsv`](render-command-list-render-command-owner-list-accesses.tsv) |
| the vector shared by both | [`render-command-list-eastl-pointer-vector-accesses.tsv`](render-command-list-eastl-pointer-vector-accesses.tsv) |
| command objects | [`render-command-list-ordered-object-accesses.tsv`](render-command-list-ordered-object-accesses.tsv) |
| the render-parameter block | [`render-command-list-postprocess-context-accesses.tsv`](render-command-list-postprocess-context-accesses.tsv) |
| the character render-object manager | [`render-command-list-pending-completion-queue-01f81248-accesses.tsv`](render-command-list-pending-completion-queue-01f81248-accesses.tsv) |

### Columns of render-command-list-ordered-object-vtable-slots.tsv

One row per vtable slot of an ordered-object class, 132 rows; slot 0 is the destructor, slot 1 the execute
method, slot 2 the order key and slot 3 the setter of the `FontBorder` classes. Its `body` is the pointer at
`vtable + 8 × slot` on all 132 rows.

| Column | Holds |
|---|---|
| `role` | what the body does, as one or more of the labels below separated by semicolons, then after `->` every direct callee of the body by address: each call or jump with an immediate target outside the body, the callees behind the labels included (35 bodies, 1 to 15 callees) |
| `cite` | one instruction of the body that shows the role: a call or jump where the body has one (84 rows), else its `ret` (45 rows), its first instruction (2 rows) or, once, a `jne` |

| Label in `role` | Meaning |
|---|---|
| `scalar-deleting dtor: member-dtor X + 0x00809950 free on flag` | a slot-0 body that calls the destructor X and `0x00809950` (41 rows) |
| `order key =` | the constant or field the slot-2 body returns (`mov eax, ...; ret`) |
| `setter: this[+18] = arg` | a store of the argument at `+0x18` (3 rows) |
| `PURE VIRTUAL` | a jump to the `_purecall` thunk (2 rows) |
| `profile-slot open` | the body reaches `0x00600A60`, the producer of block opcode `0x18` (19 rows) |
| `scene-begin submit` | the body reaches `0x005FEFD0`, the producer of block opcode `0x16` (19 rows) |
| `scene-cmd submit` | the body reaches `0x005FEA50`, the producer of block opcode `0x2F` (3 rows) |
| `master-enable gate` | the body calls `0x00193D50` and uses the byte `0x01DFE0C4` (5 rows) |

## State

| Address | What |
|---|---|
| `0x01F7F5E0` | the ordered command list |
| `0x01F7F5E8` | the owner list |
| `0x01F7F5F0`, `0x01F81300` | the render-parameter block |
| `0x01F81248` | the character render-object manager |
| `0x01DF08FC`, `0x01F7F594` | the ambient-occlusion exit pair |
| `0x01DFE0C4` | the execute-body enable byte |
| `0x01F82EC0` | the post-process screen index |
| `0x01FD4A88` | the frame tick's teardown gate |
| `0x02EBEFC0`, `0x02EBEFD8`, `0x02EBEFF0` | the two GS command buffers and the fill index |

## Modding notes

- Draw order is append order. To move a pass, change where its builder runs; changing its class
  key only changes which walks run it.
- An entry whose class key is 0 is never executed by any walk. `0x0020E630` files a
  `GeometryInstanceOrderedObject` with key 0 for any mode above 3.
- Do not free a command object yourself: the owner list frees it at the end of the render body, and
  the ordered list holds the same pointer until its clear.
- Objects appended only to the ordered list (map and character companions, text, Gi wrappers) are
  never freed by the lists; their owners or the command arena reclaim them.
- The lists have no lock. Append only from the thread that runs the frame.
- Turning `0x01DFE0C4` off keeps every job allocated and walked but empties the four execute bodies
  that test it.

## Related

- [Graphics thread handshake](graphics-thread-handshake.md): the GS register batch, the kick and the command-state word.
- [Gi render commands](gi-render-commands.md): the commands `GeometryInstanceOrderedObject` carries.
- [Phyre frame](../PhyreEngine/the-frame.md): the draw, its pass mask and the two draws per frame.
- [Game application](../Engine-Core/game-application.md): the frame tick, the render slot and the frame-end reset.
- [Frame update order](../Engine-Core/frame-update-order.md): the frame states that enqueue the passes.
- [Debug menu commands](../Engine-Core/debug-menu-commands.md): commands 34, 35, 37, 38 and 42.
- [EASTL strings and containers](../Third-Party-Libraries/eastl-strings-and-containers.md): the vector layout.
- [Character render object](character-render-object.md) and [post-processing](post-processing.md).
