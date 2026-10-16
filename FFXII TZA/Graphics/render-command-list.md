---
title: "Render command list: the per-frame command objects, the two lists that hold them and the walks that run them"
kind: "system"
category: "Graphics"
addresses: "01F7F5E0, 01F7F5E8, 00186CD0, 0018B480, 0018AD00, 0018C9E0, 0018B4E0, 0018CA40, 0018AFF0, 0018C610, 00212CC0, 0018B100, 0018B1B0, 0018B510, 0018B030, 0018B070, 0018B0B0, 0018B040, 0018B810, 0018C8F0, 00187950, 0022A580, 001F28B0, 00193D50, 01DFE0C4, 001BDA50, 003A1D50, 003A1DB0, 004FE420, 02EBEFC0"
---

## What the player sees

The picture is built in layers: opaque characters and maps, ambient occlusion, water and its
refraction, subsurface scattering, post-processing, the PS2-style depth of field, a Gaussian filter,
video and the scene brackets. Each layer is a small job object the frame creates, files in a list
and runs later; the next frame creates them again.

Two developer-console toggles act on this list directly. "Enable Character Display" (command 35)
removes every character from the opaque passes, and "Display AO Only" (command 42) stops the second
half of the list at the first job after ambient occlusion has run, so the screen shows the
ambient-occlusion result alone ([debug menu commands](../Engine-Core/debug-menu-commands.md)).

## How it works

### Two lists, one owner

The render-manager installer `00186CD0` creates both lists once, at `00186D00` and `00186D0F`:

- `0018B480` allocates the 0x30-byte ordered command list (`0018B4AB`) and stores it at `01F7F5E0`.
  Its constructor `0018AD00` sets the class mask `+0x20` to `0xFFFFFFFF`, reserves 5,000 entries
  (`0018AD40`, through `0018B320`), and sets the split `+0x24` to 0 and the mark `+0x2C` to -1.
- `0018C9E0` allocates the 0x20-byte owner list (`0018C9F9`) and stores it at `01F7F5E8`, with
  begin, end and capacity all zero (`0018CA10`–`0018CA19`).

Both are EASTL pointer vectors ([EASTL strings and containers](../Third-Party-Libraries/eastl-strings-and-containers.md)).
Each constructor passes the name `"EASTL vector"` (`008C5F58`) to `001EDF00`, whose whole body
stores the allocator vtable `00902720` and never reads the name. The getters are `0018B4E0` (ordered
list) and `0018CA40` (owner list); `0018B4E0` hands its null test to `0016D6A0`, a bare `ret`.

### Enqueueing a command

Every allocating producer is one builder per class, 36 of them from `0018B540` to `0018CCF0`.
`0018C610` (`PostProcessObj`) shows the shape:

1. `malloc` the object (`0085E730`, `0018C632`) and run the class constructor (`001F1B80`); a failed
   allocation leaves a null (`0018C655`);
2. append the pointer to the owner list inline (`0018C65C`–`0018C673`), or through the grow routine
   `001AB570` (`0018C680`) when full;
3. tail-jump `0018AFF0(0018B4E0(), object)` (`0018C69F`) to append the same pointer to the ordered list.

A null is therefore appended to both lists. The owner list starts with no capacity and grows from its
first append; the ordered list's 5,000 reserved entries are its whole working size. The 36 builders
allocate 0x18 bytes (15 classes), 0x20 (16), 0x28 (3) or 0x30 (2).

Each class constructor starts with the base `00212CC0` and stores its argument after the base
fields. `RazorMarkerPushObj`'s `001F1C30` takes a zeroed 0x200-byte buffer (`00210EC0`) at `+0x18`
and copies the marker name into it, at most 0x1FF characters. `SetRendererCameraObj`'s `001F1E80`
keeps the camera at `+0x18` and copies the render manager's byte `+0x1C` to `+0x20`.
`SetScreenIndexToPostProcessManagerObj`'s `001F1ED0` keeps the screen index at `+0x18`.

Four other functions call `0018AFF0` and append to the ordered list only, so the owner list never
destroys what they add: `MapRenderObject`'s slot 1 `001E5270` (its `MapOrderedObject` at `+0x10`),
`CharacterRenderObject`'s slot 1 `001F89B0` (its `CharacterOrderedObject` at `+0x28`, when
non-null), the text flush `001E8580`, and `001F48B0`, which wraps a Gi render command in a
`GeometryInstanceOrderedObject` taken from the command arena `[01F7F4C0]` ([Gi render commands](gi-render-commands.md)).

### The game-side wrappers

Small wrappers file fourteen of the classes. They check that the owner list
(`0018CA40`) or the render manager (`00189120`) exists and pick the arguments:

| Wrapper | Builder | Class | What the wrapper adds |
|---|---|---|---|
| `00182220`, `00182250` | `0018B670`, `0018B5D0` | `BegineSceneObj`, `BegineScene0Obj` | argument 0; sets `01F7F538` to 1 |
| `001823B0`, `001823E0` | `0018BE70`, `0018BDD0` | `EndSceneObj`, `EndScene0Obj` | clears `01F7F538` |
| `0017F2A0`, `00182A60`, `00182AD0` | `0018B8B0` | `CopyBufferObj` | the source target, below |
| `0017F330` | `0018BB70` | `CopyFrontBufferForWaterRefraction` | only when the map-art byte `+0x2E5` is set (`001A94B0`) |
| `00180A30` | `0018C2A0` | `RenderAfterWaterObj` | with that byte set, first `001A8F80` on the map-art context |
| `0017F670`, `0017F6B0` | `0018C450` | `MaskBorderObj` | `0017F670(n)` only when `01DF08E8` and `01F7F4F0` are set; `0017F6B0` passes 3 under its own tests |
| `00182280` | `0018B710` | `FastClearObj` | through `00185CD0`, which also keeps the four arguments at manager `+0xD00`-`+0xD0C` |
| `00185A10`, `001860E0` | `0018CBC0` | `SetRendererCameraObj` | the camera at manager `+0x358` with `+0x1C` = 1, or `+0x690` with `+0x1C` = 0 |
| `00183120` | `0018CB30` | `SetPrimIdEnableObj` | only when `005C5230()` is non-zero; it returns 0, so nothing is filed |
| `001EB110` | `0018C0D0` | `RazorMarkerPopObj` | only when `[01F7F4E0]` exists and its byte `+0x08` is set, as for the push `001EB150` |
| `001826E0` | `0018B970` | `CopyDepthBufferObj` | the render parameters' `+0x2B8` (`00193D50`), 0, 0 |
| `0017ECF0` | `0018C740` | `AmbientOcclusionObj` | none |

`0017F6B0` files `MaskBorderObj` with 3 when the owner list exists and one of these holds:
`01DF08EC` and `01F7F4F0` are both set, `01F7F4F4` is set, `01F7F4F8` is set (the effect draw sets
it for the frame), `01F7F500` is set (by `00184740` while effect `0x17A` plays), or the movie
player is in state 3 (`001B7D20`).

`00229F20(water)`, called from the scene draw `0022B0B0`, files the ambient-occlusion pass when `01FD49E8`
is set: the scope `AO render`, `MaskBorderObj(1)` and a depth copy; with `water` non-zero the scope
`Water effect`, the water refraction copy, `RenderAfterWaterObj`, a pop and another depth copy; then
`AmbientOcclusionObj` and a pop. `00182560` returns `01F7F538`, the scene-open byte the scene wrappers
write; `00183060(x)` stores `x != 0` in `01F7F50E`, which `0017FE50` returns.

`001809E0`, also in the frame bodies, runs `001A5A70` and `001AA2C0` on the map-art context when its
byte `+0x2E5` is set.

The copy source comes from the render manager's target tables:

- `0017F2A0(arg, entry)` takes the entry's target unless its byte `+0x08` is set, and passes 0 and 0.
- `00182A60(arg, which, n)` takes `00186910(manager, which != 0)` and passes `n` and 1;
  `00182AD0(arg, target, n)` passes its own target, `n` and 0.
- `001867B0` returns target `+0xB08 + 8 × [+0xC30]`. `00186A50` returns `+0xB48 + 8 × [+0xDD0]`, or
  `+0xB50 + …` while `+0xDBB` is set. `00186A00` takes `+0xB50` only when the render parameters' byte
  `+0x4A0` is also set (`0017F280`). `00186910` returns the first or `00186A00`'s choice.
- `001868A0` and `00186840` are `00186A50` and `00186A00`, each calling `001EDDA0` first when
  `001EDE70()` is set. `0017FDE0`, `0017FE60(i)` and `0017FEE0(i)` return the target of `001867B0`,
  of `00186840` or `001868A0`, and of `00186A00` or `00186A50`, or 0 when its byte `+0x08` is set.

- `00189530(manager, flag)` copies the target pointer at `+0xB28` (flag set) or `+0xB30` into the
  first table entry `+0xB08`. Its one caller, `PostProcessObj`'s execute `001F3300`, passes 0 after
  the post-process work for the screen index `01F82EC0` when the device byte `+0xD48` of
  `00796E20()` is set, and otherwise copies the result back with `001EE8E0`.
- `001EEE80(target, w, h)` resizes a target's texture (`0060DD70`, same format) when its size
  `+0x28`/`+0x2C` differs, unbinding it first when it is bound (`00625F00`, `0062BCB0`);
  `001EE180(target, b)` unbinds the same way and stores `b` in the target's byte `+9`. Both skip a
  null target or one whose byte `+0x08` is set.
- The target rebuild `00188B10` resizes ten of the
  manager's targets to the fit size (`00182EB0`, `00182E80`), and `00188DA0` gives four of them
  `02CB8084` through `001EE180`.
- The rebuild also prunes the object `[01F81210]` (`001B6C40`), which `00182CA0` and `00182B40`
  use: `001B6B50` removes every entry for which `001B6A70` returns 1, after that function has
  queued the `+0x20` of each node of the entry's list `+0x78` for a deferred call to `001B6C30`
  (`00185A90`) and emptied its map `+0x70`; it returns 1 when the entry's `+0x60` is 0.

The other accessors read the manager: `00182410` its byte `+0xDB9`, `00182570` its byte `+0x1C`,
`00182490(&w, &h)` the width and height (`00182EB0`, `00182E80`). `001824E0(a, b, c)` fills three
values through `00186AB0`: from `0018A620()` `+0xD8`, `+0xDC`, `+0xD0`, or, when the `001D50D0` object's
byte `+0xC0C` is set, from its `+0xC10`, `+0xC18`, `+0xC14`.

`00185A80(manager, n)` adds `n` to the manager's counter `+0xDBC`. The character draw `001F5D70`
adds, for each mesh instance it draws, the low 31 bits of the first dword the instance points to
(1 for the single-mesh path), and the map draw
`001E2AF0` adds its own counts; the render pass list `00187950` copies the total to `+0xDC0` and
clears `+0xDBC` at the start of each frame.

### The command object

The base constructor `00212CC0` stores the `OrderedObject` vtable `009010B8`, zeroes `+0x08` and
sets the byte `+0x10` to 1 (`00212CD5`). The base class's slots 1 and 2 are `00861EC6`, the
pure-virtual thunk, so every concrete class supplies three slots: slot 0 destroys, slot 1 executes
with `(object, device)`, slot 2 returns the class key.

Two classes read `+0x08` in their execute slot and forward it as the callee's object:
`MapOrderedObject`'s `00212C60` calls `001E2AF0` with it when non-null, and
`CharacterOrderedObject`'s `00215320` tail-jumps `001F5D70` with it.

### The class key is a mask, and nothing sorts

Slot 2 returns a constant for most classes. Both walks AND it with a mask; neither compares two
entries, so the list runs in the order the jobs were appended:

| Key | Slot 2 | Classes |
|---|---|---|
| `0x1` | `0053DD10` | the scene brackets, the Razor markers, the MSAA, depth-of-field and primitive-id toggles (11) |
| `0x2` | `00290180` | `CharacterOrderedObject` |
| `0x4` | `0016EE70` | `MapOrderedObject` |
| `0x10` | `001F2880` | the ordinary passes (18) |
| `0x20` | `00212E20` | the three `FontBorderOrdered*` classes |
| `0x80` | `001F28A0` | `VideoObj` |
| `0x100` | `001F2890` | `RenderOpaqueObj`, `RenderAfterWaterObj`, `RenderMapOpaqueObj`, `RenderMonsterGalleryChara` |
| `[+0x18]` | `00879750` | `GiResetRenderTargetObj`, `GiResetDefaultRenderTargetObj` (the constructor's argument) |
| `[+0x20]` | `001F49E0` | `GeometryInstanceOrderedObject` (the mask `001F48B0` was given) |

The only writer of the list's own mask besides the constructor is `0018B070`, which sets or clears
bit `0x2`. Console command 35 calls it with the new state of "Enable Character Display"
(`001D1C29`, `001D1C3D`), so turning character display off drops every `CharacterOrderedObject`
from every walk.

### The two parts of a frame

At the head of each frame the state machine `0022A580` calls the split setter twice through
`00183100` → `0018CB10` → `0018B510`. `0018B510` stores whether its argument is non-zero at `+0x28`
and then sets the split `+0x24` to 0 when it is, or to the current count when it is not:

1. `00183100(1)` at `0022A5AC` sets the split to 0;
2. the frame-open producers run for screen 0: `001829A0` (`SetScreenIndexToPostProcessManagerObj`),
   `001EC490` (`ApplyJsonForCutSceneObj`) and `00214C30` (the depth-of-field commands);
3. `00183100(0)` at `0022A5CF` sets the split to the count, so `[0, split)` holds exactly the frame-open commands.

The render body `00187950` (application slot 8, [game application](../Engine-Core/game-application.md))
then walks the list with `0018B100(list, part, device)`, where `device` is the render manager's
`+0x08` (`00187CFF`, `00188122`):

- part 1 at `00187D05`, entries `[0, split)`;
- the profile scope `"render ordered objects"` (`008C5E28`, `001880E7`);
- part 0 at `00188128`, entries `[split, count)`;
- the teardown pair at `00188204` and `00188211`.

For each entry the walk skips a null (`0018B159`), calls slot 2 once (`0018B164`), skips the entry
when the key does not meet the list mask (`0018B167`), and calls slot 1 with the device (`0018B187`).

### Display AO Only

Between the mask test and the execute, `0018B16C`–`0018B17C` leave the walk (to `0018B192`) when
byte `01DF08FC` is 0 and byte `01F7F594` is not. `AmbientOcclusionObj`'s execute `001F28B0` sets
`01F7F594` to 1 at `001F29A3`, on the path that runs only after both of its gates (render-parameter
byte `+0x198` and `01DFE0C4`) passed.

Before part 0 the render body tests render-parameter byte `+0x199` (`00188103`) and, when it is
set, zeroes both bytes (`0018810C`, `00188113`); after part 0 it reloads `01DF08FC` and sets it
again when `+0x199` is still set (`00188132`–`00188144`). Console command 42 flips `+0x199`. With
it on, part 0 runs up to the ambient-occlusion job and stops at the next job that passes the mask.

### Class-filtered walks

`0018B1B0(list, device, mask, reverse)` runs only entries whose key meets both the caller's mask and
the list mask, calling slot 2 twice per entry (`0018B247` and `0018B258`, `0018B2D3` and `0018B2E4`).
Its range comes from the mark `+0x2C` and the render-parameter word `+0x49C` (read by `0018D630`):

| Mark | `+0x49C` | Reverse (`0018B1D4`) | Forward (`0018B280`) |
|---|---|---|---|
| -1 | any | count-1 down to 0 | 0 to count-1 |
| m | 0 | m-1 down to 0 | 0 to m-1 |
| m | non-zero | count-1 down to m | m to count-1 |

The mark is set by `0018B030`, which stores the current count, through `001829F0`; `MainLoop_Draw`
`0022B0B0` calls it at `0022B112` when it starts draw 1. Entries before the mark therefore belong to
draw 0 and the frame open, entries from it to draw 1.

The opaque passes are themselves list entries whose execute runs a nested reverse walk, after
setting a pass byte on the list that the character draw body `001F5D70` reads:

| Execute | Class | Walk | Pass byte |
|---|---|---|---|
| `001F36B0` | `RenderOpaqueObj` | mask 2, reverse (`001F370C`) | `+0x29` |
| `001F3570` | `RenderMapOpaqueObj` | mask 2, reverse (`001F35D0`), then mask 4 (`001F361B`) | `+0x29` |
| `001F3650` | `RenderMonsterGalleryChara` | mask 2, reverse (`001F3689`) | `+0x29` |
| `001F3510` | `RenderAfterWaterObj` | mask 2, reverse (`001F3549`) | `+0x2A` |

Each sets its byte to 1 before the walk and to 0 after it. A sixth caller, `001F06D0`, walks forward
with mask 6 (characters and maps) at `001F07C7`.

### Removal and teardown

`0018B0B0(list, object)` replaces every entry equal to `object` with null and keeps the count;
`CharacterRenderObject`'s slot 3 `001F6D60` calls it (`001F6D96`) before freeing its
`CharacterOrderedObject`. Null entries are why every walk tests for them.

Three teardowns empty the lists, each clearing the ordered list before the owner destroys:

| Site | Clear | Owner |
|---|---|---|
| render body `00187950` | `00188204` | `0018B810` at `00188211` |
| frame tick `0017CCD0` | `0017CD53` | `0018B810` at `0017CD60` |
| frame-end reset `001E0590` | `001E05A9` | `0018C8F0` at `001E05B6` |

`0018B040` clears the ordered list: `0018B3F0(list, 0)` moves the end back to the begin, then the
split is set to 0 and the mark to -1 (`0018B050`, `0018B057`); no object is touched. `0018B810`
calls each non-null object's slot 0 with `edx = 1` (`0018B860`), which frees it, and empties the
owner list. The frame tick runs its pair only while byte `01FD4A88` is set (`0017CD42`) and stores 0
there afterwards (`0017CD73`); those are the only two instructions that name the byte.

### The flush

`0018C8F0`, used by the frame-end reset, first executes every owner entry whose byte `+0x10` is 0
(`0018C933`) with the device `[00189120() + 8]` (`0018C939`–`0018C948`), then destroys every
non-null entry (`0018C987`) and empties the list. The execute loop has no null test, so a null left
on the owner list faults at `0018C933`.

Exactly four constructors clear `+0x10`: `ApplyJsonForCutSceneObj` (`001F1799`), `EnableDofObj`
(`001F196A`), `ReadPresetDofForCutSceneObj` (`001F1CE4`) and `SetDofObj` (`001F1E3E`). These are the
settings commands, so a flush applies the pending cutscene and depth-of-field settings even when no
walk ran them.

### What the execute bodies read

- Byte `01DFE0C4` is 1 in the image and is written only by `001F2870` (from `cl`) and `001F39B0`
  (1). The ambient-occlusion (`001F28CB`), Gaussian (`001F30E8`), post-process (`001F330A`) and
  subsurface-scattering (`001F3749`) executes do no work while it is 0.
- `AmbientOcclusionObj` (`001F28B0`) runs when render-parameter byte `+0x198` is set (`001F28BE`).
- `GaussianFilterObj` (`001F3090`) runs when any of `+0x19A`, `+0x3E8` or `+0x180` is set (`001F309E`–`001F30BA`).
- `PostProcessObj`'s constructor `001F1B80` stores its mode at `+0x18` and sets the screen index
  `01F82EC0` to 0 for mode 0 or increments it otherwise (`001F1BB5`); it is the index's only writer.
- `ApplyJsonForCutSceneObj`'s execute `001F29C0` passes its `+0x18` to `001C3C30` and ignores the device.

### The render-parameter block

`00193D50` returns the 0x4A8-byte block at `01F7F5F0`, creating it on first use with the
constructor `0018CD90`; `0015CAF0` copies the same pointer to `01F81300`. The fields this page uses
are the switches `+0x180`, `+0x198`, `+0x199`, `+0x19A`, `+0x3E8` and the walk selector `+0x49C`,
which the constructor sets to 0 (`0018D033`). The constructor also sets the render size
`+0x2E0`/`+0x2E4` to 1920 × 1080 (`0018CF61`, `0018CF6B`). The block's post-processing fields are on
[post-processing](post-processing.md).

### The character render-object manager

The installer also calls `001BDA50` (`00186CFB`), which allocates the 0x108-byte manager at
`01F81248` (constructor `001BC9D0`, getter `001BDAB0`). Its first 0x20 bytes are the same pointer
vector, reserved to 50 entries through `0018B320` (`001BCACC`).

`001BD4A0` creates a 0x668-byte `CharacterRenderObject` (`001F4DA0`) when its map has none for the
key and increments `+0xFC` (`001BD54F`). `001F6E70` increments `+0x100` with a locked `xadd`
(`001BD7D0`, from `001F7739`). `001BD620` reports whether the two counts are equal, and `001800C0`
returns 1 while they differ; the field frame tests it at `0022ABC2` to decide whether the simulation
tick runs ([frame update order](../Engine-Core/frame-update-order.md)). The render objects
themselves are on [character render object](character-render-object.md).

### The GS command buffers

Beside the object list the frame keeps two flat buffers of 16-byte GS register records. `003A1D50`
(from `0036F4D0`) clears the two 0x18-byte records `02EBEFC0` and `02EBEFD8` (`004FE3C0`), sets the
fill index `02EBEFF0` to 0, and points each at 512 records of the arena `[01FD4A78]` through
`004FE420(record, 0x200, offset)`: the first at offset 0, the second at offset 0x200 records.
`003A1E10(count, offset)` re-points both the same way.

Producers append through the current record's write cursor `+0x08`, 0x10 bytes per record.
`003A1DB0`, called from 47 sites in 38 functions, flips `02EBEFF0`, passes the old buffer's begin and
record count to `0036F360`, resets the new buffer's cursor to its begin and returns that record.
`0036F360` and the register batch `0036D400` are on [graphics thread handshake](graphics-thread-handshake.md).

### The map's pair of buffers

A second pair of the same 0x18-byte records, `02EBB700` and `02EBB718` with the index `02EBB730`,
serves the map draw-list build `002F5550`.

- `00465F60(n)`, called with `0x100` from `0036F4D0` just before `003A1D50`, clears both records
  (`004FE3C0`), zeroes the index and gives each a block of its own of `n` records through
  `004FE3D0`, which allocates with `003EC8D0(6, n × 16)`.
- `00466070(count, offset)` re-points them: for an offset of 0 or more into the arena `[01FD4A78]`
  at `offset` and `count + offset` (`004FE420`), for a negative offset back to blocks of their own
  (`004FE3D0`).
- `002F5550` calls it with `0x100` and 0, then `004660F0`, which flips the index and resets the new
  buffer's cursor, and `00465FF0`, which appends two records to the other buffer: the first with
  `0x10000000` in its first and last dwords, the second `{0x70000000, 0}` (`0046601A`–`00466043`).
- `00466120`, which `002F5550` also calls, does nothing: both its calls go to `005C5230`, which
  returns 0.

## Layouts

Ordered command list ([`01F7F5E0`]), `0x30` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | begin |  |
| `08` | `void*` | end | append cursor |
| `10` | `void*` | capacity end | 5,000 entries reserved by `0018AD00` |
| `18` | `void*` | allocator | vtable `00902720` |
| `20` | `u32` | class mask | `0xFFFFFFFF`; bit `0x2` toggled by `0018B070` |
| `24` | `u32` | split | `0018B510`; 0 after a clear |
| `28` | `u8` | split armed | `0018B510`: argument != 0 |
| `29` | `u8` | opaque pass | 1 during the nested walks of `001F36B0`, `001F3570`, `001F3650` |
| `2A` | `u8` | afterwater | 1 during the nested walk of `001F3510` |
| `2C` | `i32` | mark | `0018B030`; -1 after a clear |

Owner list ([`01F7F5E8`]), `0x20` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | begin |  |
| `08` | `void*` | end |  |
| `10` | `void*` | capacity end | 0 at creation |
| `18` | `void*` | allocator | vtable `00902720` |

Command object (OrderedObject), `0x18` bytes and up:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | vtable | three slots: destroy, execute(object, device), class key |
| `08` | `void*` | target | 0 from `00212CC0`; forwarded by `00212C60` and `00215320` |
| `10` | `u8` | flush select | 1 from `00212CC0`; 0 for the four settings commands |
| `18` | `...` | class fields | PostProcessObj: u32 mode; GiReset*: u32 key; SetDofObj: u8 +`0x18`, f32 +`0x1C`, f32 +`0x20` |

GeometryInstanceOrderedObject (vtable `00903920`), `0x28` bytes from [`01F7F4C0`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `18` | `void*` | Gi command | `001F4950` |
| `20` | `u32` | class key | `001F4950`, returned by `001F49E0` |

GS command buffer record (`02EBEFC0`, `02EBEFD8`), `0x18` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | begin | [`01FD4A78`] + offset * 16 |
| `08` | `void*` | write cursor |  |
| `10` | `u32` | capacity | `0x200` |
| `14` | `u32` | ready | 1 after `004FE420` |

The command classes and their vtables, in vtable order from `00902F90` (stride 0x20):

```
00902F90 SetRendererCameraObj        00903110 MonsterGallerySoftParticleEnable  00903290 ZBufferObj
00902FB0 BegineSceneObj              00903130 RenderMapOpaqueObj                009032B0 VideoObj
00902FD0 EndSceneObj                 00903150 RenderOpaqueObj                   009032D0 RazorMarkerPushObj
00902FF0 BegineScene0Obj             00903170 RenderAfterWaterObj               009032F0 RazorMarkerPopObj
00903010 EndScene0Obj                00903190 MaskBorderObj                     00903310 FastClearObj
00903030 CopyBufferObj               009031B0 RenderSSSObj                      00903330 DisableMsaaObj
00903050 CopyDepthBufferObj          009031D0 PostProcessObj                    00903350 EnableMsaaObj
00903070 Ps2DofObj                   009031F0 AmbientOcclusionObj               00903370 SetPrimIdEnableObj
00903090 SetScreenIndexToPostProcess 00903210 GaussianFilterObj                 00903390 EnableDofObj
         ManagerObj                  00903230 CopyFrontBufferForVFXObj          009033B0 SetDofObj
009030B0 ApplyJsonForCutSceneObj     00903250 CopyFrontBufferForChrRefraction   009033D0 GiResetRenderTargetObj
009030D0 ReadPresetDofForCutSceneObj 00903270 CopyFrontBufferForWaterRefraction 009033F0 GiResetDefaultRenderTargetObj
009030F0 RenderMonsterGalleryChara
```

Outside the block: `MapOrderedObject` `009010D8`, `GeometryInstanceOrderedObject` `00903920`,
`CharacterOrderedObject` `00903940`, and `FontBorderOrderedObject`, `FontBorderOrderedGaussObject`,
`FontBorderOrderedResetObject` at `00906D50`, `00906D78`, `00906DA0`, whose fourth slot `00225580`
stores its argument at `+0x18`.

Per-slot tables and instruction-level access lists beside this page:

| Subject | Table |
|---|---|
| every class's slots | `render-command-list-ordered-object-vtable-slots.tsv` |
| the ordered command list | `render-command-list-ordered-command-list-accesses.tsv` |
| the owner list | `render-command-list-render-command-owner-list-accesses.tsv` |
| the vector shared by both | `render-command-list-eastl-pointer-vector-accesses.tsv` |
| command objects | `render-command-list-ordered-object-accesses.tsv` |
| the render-parameter block | `render-command-list-postprocess-context-accesses.tsv` |
| the character render-object manager | `render-command-list-pending-completion-queue-01f81248-accesses.tsv` |

## State

| Address | What |
|---|---|
| `01F7F5E0` | the ordered command list |
| `01F7F5E8` | the owner list |
| `01F7F5F0`, `01F81300` | the render-parameter block |
| `01F81248` | the character render-object manager |
| `01DF08FC`, `01F7F594` | the ambient-occlusion exit pair |
| `01DFE0C4` | the execute-body enable byte |
| `01F82EC0` | the post-process screen index |
| `01FD4A88` | the frame tick's teardown gate |
| `02EBEFC0`, `02EBEFD8`, `02EBEFF0` | the two GS command buffers and the fill index |

## Modding notes

- Draw order is append order. To move a pass, change where its builder runs; changing its class
  key only changes which walks run it.
- An entry whose class key is 0 is never executed by any walk. `0020E630` files a
  `GeometryInstanceOrderedObject` with key 0 for any mode above 3.
- Do not free a command object yourself: the owner list frees it at the end of the render body, and
  the ordered list holds the same pointer until its clear.
- Objects appended only to the ordered list (map and character companions, text, Gi wrappers) are
  never freed by the lists; their owners or the command arena reclaim them.
- The lists have no lock. Append only from the thread that runs the frame.
- Turning `01DFE0C4` off keeps every job allocated and walked but empties the four execute bodies
  that test it.

## Related

- [Graphics thread handshake](graphics-thread-handshake.md): the GS register batch, the kick and the command-state word.
- [Gi render commands](gi-render-commands.md): the commands `GeometryInstanceOrderedObject` carries.
- [Phyre frame](../PhyreEngine/the-frame.md): the draw, its pass mask and the two draws per frame.
- [Game application](../Engine-Core/game-application.md): the frame tick, the render slot and the frame-end reset.
- [Frame update order](../Engine-Core/frame-update-order.md): the frame states that enqueue the passes.
- [Debug menu commands](../Engine-Core/debug-menu-commands.md): commands 35 and 42.
- [EASTL strings and containers](../Third-Party-Libraries/eastl-strings-and-containers.md): the vector layout.
- [Character render object](character-render-object.md) and [post-processing](post-processing.md).
