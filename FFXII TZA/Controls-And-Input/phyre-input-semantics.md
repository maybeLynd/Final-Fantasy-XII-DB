---
title: "Phyre input semantics: the type, axis and pad-button names of the engine's input sources, how a source turns them into codes, and the one path that reads them"
kind: "reference"
category: "Controls and input"
addresses: "0x02EB8260, 0x02EB82D8, 0x02EB8348, 0x02EB8270, 0x02EB82E0, 0x02EB8350, 0x0079CFB0, 0x0079E2C0, 0x0079DA10, 0x00873FB0, 0x00873FE0, 0x00874080, 0x00874120, 0x00874170, 0x00873100, 0x008760A0, 0x00876490, 0x008768A0, 0x00879750"
---

## What it lists

PhyreEngine's input module describes an input as a list of sources, and each source names what it reads through
semantics: static named objects in three registries. The type semantics say which device a source reads (the 25 listed in the next paragraph),
the axis semantics name a stick axis, and the pad-button semantics name a
pad button. This page lists every one of those objects in
[`phyre-input-semantics.tsv`](phyre-input-semantics.tsv).

The 25 type semantics, in table order: `Key`, `JoypadButton`, `JoypadAxis`, `MouseButton`, `MouseDeltaX`, `MouseDeltaY`, `TouchDragX`, `TouchDragY`, `TouchTwoFingerDragX`, `TouchTwoFingerDragY`, `TouchPinch`, `TouchRotate`, `MotionQuatX`, `MotionQuatY`, `MotionQuatZ`, `MotionQuatW`, `MotionAngularVelocityX`, `MotionAngularVelocityY`, `MotionAngularVelocityZ`, `MotionLinearAccelerationX`, `MotionLinearAccelerationY`, `MotionLinearAccelerationZ`, `VisionTrackerX`, `VisionTrackerY`, `VisionTrackerZ`.

### What the player sees

Nothing. The game reads its keys, buttons and sticks through its own control code ([Controls](controls.md)). The
engine's input sources described here are reached only through a script method of the application, which the game
never calls, so none of these names changes how the game plays.

### The three registries

Each semantic is a static object: a vtable, a name and a link, and for axes and pad buttons a code. At start-up one
small initialiser per object passes it to its registry's insert and registers its teardown with `atexit`; the insert
refuses a null name (`0x11`) or a duplicate (`0x12`) and otherwise pushes the object at the front of the list, the
shape [static initialisation and teardown](../Compiler-And-C-Runtime/static-initialisation-and-teardown.md)
describes (`0x008760A0`: `0x008760AE`, `0x00876116`, `0x00876100`-`0x0087610A`).

The three inserts `0x008760A0`, `0x00876490` and `0x008768A0` are the same code on their own heads. The duplicate test
compares the name byte for byte with that of every object on the list (`0x008760D0`-`0x008760FE`); the push stores the
old head at the object's `+0x10`, makes the object the head and returns 0 (`0x00876100`-`0x0087610A`).

| Class | Objects | vtable | Head | Insert | Named-semantic descriptor |
|---|---|---|---|---|---|
| `PInputTypeSemantic` | 25, `0x01F44D90`-`0x01F44FD0`, no code | `0x01CD7F68` | `0x02EB8260` | `0x008760A0` | `0x02EB8270` |
| `PInputAxisSemantic` | 10, `0x01F45008`-`0x01F45128`, codes 1-10 | `0x01CD80B8` | `0x02EB82D8` | `0x00876490` | `0x02EB82E0` |
| `PInputJoypadButtonSemantic` | 44, `0x01F45148`-`0x01F456A8`, codes 0 and 11-26 | `0x01CD8448` | `0x02EB8348` | `0x008768A0` | `0x02EB8350` |

The pad-button vtable has a second slot, `0x00879750`, which returns the code at `+0x18`; the type and axis vtables
hold only the deleting destructor (`0x01CD7F68`, `0x01CD80B8`; the next qword is the class name). Two more registries
of the same module, the key names and the mouse-button names (head `0x02EB8428`), are on
[Control names](control-names.md) and
[static initialisation and teardown](../Compiler-And-C-Runtime/static-initialisation-and-teardown.md).

### The exit teardowns

Each object's teardown stores the class vtable back into the object and unlinks it from its list (`0x008B9950`:
`0x008B9957`, `0x008B99A3`-`0x008B99AA`). The teardowns run from the runtime's exit table, which the game's normal quit
does not reach ([static initialisation and teardown](../Compiler-And-C-Runtime/static-initialisation-and-teardown.md)).
The deleting destructors `0x00876020`, `0x00876410` and `0x008767F0` do the same store and unlink through the object
they are given (`0x00876030`, `0x00876420`, `0x00876800`).

### The named-semantic descriptors

Each class has a reflection descriptor that lets a pointer to one of its objects be stored and read as the object's
name. `0x00875F00`, `0x008762F0` and `0x008766D0` build them once each, under the guards `0x02EB82D0`, `0x02EB8340` and
`0x02EB83B0`, by calling `0x006B6820`:

| Descriptor | Class name | Size | `+0x40` name getter | `+0x48` name resolver | vtable | Slot 9: find | Slot 10: list |
|---|---|---|---|---|---|---|---|
| `0x02EB8270` | `PInputTypeSemantic` | `0x18` | `0x00876870` | `0x00876130` | `0x01CD7F90` | `0x00876280` | `0x008761A0` |
| `0x02EB82E0` | `PInputAxisSemantic` | `0x20` | `0x00876870` | `0x00876520` | `0x01CD80E0` | `0x00876670` | `0x00876590` |
| `0x02EB8350` | `PInputJoypadButtonSemantic` | `0x20` | `0x00876870` | `0x00876930` | `0x01CD8480` | `0x00876A80` | `0x008769A0` |

- `0x00876870` returns the object's name and its length with the terminator (`0x00876870`-`0x00876894`).
- The resolvers walk the list comparing names, store the object found through their first argument and return
  `0x13` when no object has the name (`0x00876130`-`0x00876196`).
- Slot 9 returns the object with a name, or 0 (`0x00876280`-`0x008762D6`); slot 10 copies every object pointer into
  an array (`0x008761A0`).

These are the type-reference hooks of [Phyre reflection](../PhyreEngine/phyre-reflection.md): the
loader resolves a semantic member through `+0x48`. The PInputs module register `0x00875E10`
([Phyre modules](../PhyreEngine/phyre-modules.md)) adds the three descriptors to the type tree
(`0x00875EA0`, `0x00875EBA`, `0x00875EE1`).

### The input sources

A source is an object of one of 25 classes derived from `PInputSource` (descriptor `0x02EB52F0`, `0x28` bytes). The
base class reflects four members, registered by `0x0086DA70`: `m_typeSemantic` at `+0x10` (`0x0086DB02`), `m_id` at
`+0x18` (`0x0086DB71`), `m_invert` at `+0x1C` (`0x0086DBE0`) and `m_scale` at `+0x20` (`0x0086DC4F`). Six classes add
semantic pointers, each typed by a named-semantic descriptor:

| Class | Size | vtable | Members | Member type | Registered at |
|---|---|---|---|---|---|
| `PInputSourceKey` | `0x40` | `0x01CD6288` | `m_positiveKeySemantic` `+0x30`, `m_negativeKeySemantic` `+0x38` | key semantic | `0x0086DF22`, `0x0086DF95` |
| `PInputSourceJoypadButton` | `0x40` | `0x01CD62A8` | `m_positiveButtonSemantic` `+0x30`, `m_negativeButtonSemantic` `+0x38` | pad-button semantic | `0x0086DDE2`, `0x0086DE55` |
| `PInputSourceJoypadAxis` | `0x38` | `0x01CD62C8` | `m_joypadAxisSemantic` `+0x30` | axis semantic | `0x0086DD19` |
| `PInputSourceMouseButton` | `0x38` | `0x01CD62E8` | `m_mouseButtonSemantic` `+0x30` | mouse-button semantic | `0x0086E119` |
| `PInputSourceMouseDeltaX` | `0x40` | `0x01CD6308` | `m_modifierButtonSemantic` `+0x30`, `m_modifierKeySemantic` `+0x38` | mouse-button, key semantic | `0x0086E1E2`, `0x0086E255` |
| `PInputSourceMouseDeltaY` | `0x40` | `0x01CD6328` | the same two | mouse-button, key semantic | `0x0086E322`, `0x0086E395` |

The other 19 classes (`PInputSourceTouchDragX` and `Y`, `TouchTwoFingerDragX` and `Y`, `TouchPinch`,
`TouchRotate`, `MotionQuatX`-`W`, `MotionAngularVelocityX`-`Z`, `MotionLinearAccelerationX`-`Z` and
`VisionTrackerX`-`Z`, vtables `0x01CD6348`-`0x01CD6588`) are `0x28` bytes and have no semantic member.

### How a source comes into being

Each class's constructor sits in slot 10 of its class descriptor's vtable, which the class's static initialiser
installs (`0x0016A440` stores `0x01CD24E8`, whose slot 10 `0x01CD2538` holds the `PInputSourceJoypadButton` constructor
`0x00869670`; the 25 initialisers are `0x0016A400`-`0x0016AA00`). For the key, pad-button, mouse-button and mouse-delta
classes the entry only calls the real constructor (`0x00869670` calls `0x0086C460` at `0x0086968F`); the other entries
construct in place.

No instruction calls a slot-10 entry directly. The default-buffer builder `0x00639A60` calls it through the descriptor
(`0x00639B20`, `0x00639B3E`) to build the class's default instance at descriptor `+0xC0`. A source a cluster creates is a
byte copy of that instance (`0x0063C961`-`0x0063C974`: the descriptor's `+0x38` bytes from `+0xC0`); only a descriptor
with no default instance has slot 10 construct it (`0x0063C990`).

- Every constructor stores the vtable, the class descriptor at `+0x08`, its type semantic at `+0x10`, 0 at `+0x18`
  and `+0x1C`, and 1.0 at `+0x20` (`0x0086C460`-`0x0086C49B`, `0x00866FA0`-`0x00866FD0`).
- The pad-button, key and mouse-delta constructors then clear `+0x30` and `+0x38` and run their slot 1 (`0x0086C4B0`,
  `0x0086C510`, `0x0086C5E0`, `0x0086C640`), so a new key source holds the key `Empty` object in both pointers.
- The pad-axis constructor clears `+0x30` and `+0x28` itself (`0x00869E65`, `0x00869E69`).
- The mouse-button constructor sets `+0x30` to the mouse-button `Empty` object `0x01F462E8` and reads its code through
  that object's slot 1 (`0x0086C568`-`0x0086C57D`).

The semantic pointers are filled by name when the reflection loader builds a source from data, through the
descriptor's `+0x48` resolver. Slot 2 copies a source: it creates a new object of the same class with
`0x0063A990` (`PCluster::create`), copies `+0x30`, `+0x38` where the class has it, `+0x18`, `+0x1C` and `+0x20`,
and runs the copy's slot 1 (`0x00873100`-`0x0087315C`).

The pad-button slot 2 `0x00873100` calls `0x0063A990(cluster, 1, 0x02EB54F0, 0)` for one `PInputSourceJoypadButton` in
the cluster it is given as its second argument (`0x0087310A`-`0x00873121`), takes the object 8 bytes before the
pointer returned (`0x0087312B`), copies `+0x1C` as a byte and the others whole, and returns the copy (`0x0087315F`).

The key slot 2 `0x00873170` is the same code with the key descriptor `0x02EB53F0` (`0x0087317D`), and so are the
mouse-delta copies `0x00873610` and `0x00873680` with `0x02EB57F0` and `0x02EB58F0`. The pad-axis copy `0x00873090` and the
mouse-button copy `0x008735A0` copy `+0x30` alone besides `+0x18`, `+0x1C` and `+0x20` (`0x008730CA`-`0x008730DE`,
`0x008735DA`-`0x008735EE`).

### Slot 1: from semantics to codes

Slot 1 of each source class that holds semantics stores the code of each semantic at `+0x28` (and `+0x2C` for the
second), replacing a semantic outside the class's band with an `Empty` object first.

| Slot 1 | Class | Out-of-band test | Replacement |
|---|---|---|---|
| `0x00873FE0` | `PInputSourceJoypadButton` | code above 26, a signed test (`0x0087401C`, `0x00874025`); a null semantic is not replaced: it stays null and its code is stored as 0 (`0x00874000`, `0x00874013`, `0x0087403F`, `0x00874061`) | pad-button `Empty` `0x01F45148` (`0x00874015`) |
| `0x00874080` | `PInputSourceKey` | code below 28, a null semantic counting as 0 (`0x008740BC`, `0x008740C5`) | key `Empty` `0x01F456C8` (`0x008740B5`) |
| `0x00874120` | `PInputSourceMouseButton` | null, or a code outside 11-13 (`0x00874138`-`0x0087413E`) | mouse-button `Empty` `0x01F462E8` (`0x00874140`) |
| `0x00874170` | `PInputSourceMouseDeltaX` and `Y` | `+0x30` as for the mouse button (`0x00874188`); `+0x38` null, or the `+0x30` code outside 11-13 (`0x0087419B`-`0x008741B2`) | `0x01F462E8` for `+0x30`, `0x01F456C8` for `+0x38` (`0x008741B4`) |
| `0x00873FB0` | `PInputSourceJoypadAxis` | no test | no replacement; a null semantic gives code 0 (`0x00873FD0`) |

The pad-button, key and mouse slots read a code through the semantic's own slot 1 (`call [rax+8]` at `0x00873FF9`,
`0x0087400E`, `0x0087403A`, `0x00874050`, `0x00874099`, `0x008740AE`, `0x008740DA`, `0x008740F0`, `0x00874135`, `0x00874157`,
`0x00874185`, `0x008741A9`, `0x008741CB`, `0x008741E1`). The axis slot calls `0x00879750` directly (`0x00873FC2`), since the axis
vtable has no slot 1. In `0x00874170` the test of `+0x38` reads the code of `+0x30` (`0x008741A2`).

### Where the input mapper lives

The player's controls are read through one input mapper that lasts the whole run. It is part of the application
object itself, at its `+0xE00`: the application's constructor `0x00792350` runs the mapper constructor `0x00792DD0` there
(`0x00792515`) and then stores that address at `+0xDF8` (`0x00792557`). The mapper's descriptor destroy slot `0x0061ECF0`
only returns 1, so nothing tears the mapper down.

### Reading a source: the evaluator chain

The application's input object at `+0xDF8`, which its script method `getInputMapper` returns (`0x0079D000`), is a
`PInputMapper` (descriptor `0x02EA5560`, named at `0x00791D16`) whose
reflected member `m_inputMap`, at `+0x00`, points at a `PInputMap` (`0x00795627`). Three functions read sources against
the devices:

1. `0x0079CFB0(application, name)` takes the input mapper, finds the action with that name in the input map's
   `m_inputActions` with `0x00873C70` (`0x0079CFCE`), returning 0.0 when there is no map or no such action, and jumps to
   `0x0079E2C0` (`0x0079CFE3`).
2. `0x0079E2C0(mapper, action)` runs `0x0079DA10` on each of the action's sources (`0x0079E31B`) and keeps the value of
   largest magnitude (`0x0079E329`-`0x0079E344`).
   - The sources are the pointer array at the action's `+0x18`, counted by its `+0x10` under mask `0x7FFFFFFF`; a
     null action or a count of 0 returns 0.0 (`0x0079E2D8`-`0x0079E2E9`), and `0x0079CFB0` never passes a null action
     (`0x0079CFD6`).
   - The kept value starts at 0.0 and is replaced only by a strictly larger magnitude (`jbe` at `0x0079E342`), so
     the first of two equal magnitudes wins; the value returned keeps its sign (`0x0079E344`, `0x0079E365`).
3. `0x0079DA10(mapper, source)` picks the device by comparing the source's `+0x10` with the 25 type objects, in the
   order of the table below, and multiplies the result by `m_scale`: `result × m_scale` (`mulss`, `0x0079E291`).

The sign is 1.0 (`0x01CEBBA8`), or -1.0 (`0x01CEBC9C`) when `m_invert` is set (`0x0079DA1D`-`0x0079DA5E`). A negative
semantic flips the sign (`xorps` with `0x01CEBDA0`).

| Type | Compare | What the evaluator reads |
|---|---|---|
| `Key` | `0x0079DA6A` | keyboard device `[mapper + 0x118 + 8 × m_id]`, `m_id` below 7: the byte at `+0x30 + code − 28` for `+0x28` (sign) and `+0x2C` (minus sign), code − 28 below 256 |
| `JoypadAxis` | `0x0079DAD0` | pad `[mapper + 0x88 + 8 × m_id]`: codes 1, 2, 4 and 5 read the stick values at pad `+0x58`, `+0x60`, `+0x68` and `+0x70` (codes 2 and 5 negated); any other code calls the pad's slot 4 (`0x0079DCBE`) |
| `JoypadButton` | `0x0079DCCA` | pad `[mapper + 0x88 + 8 × m_id]`, `m_id` below 18: the byte at `+0x30 + code − 11` for code − 11 below 17 (codes 11-27); codes 17 and 18 take the trigger value from `0x0079C6C0` (`0x0079DD22`, `0x0079DD6E`) |
| `MouseButton` | `0x0079DD78` | mapper bytes `+0x170`, `+0x172`, `+0x171` for codes 11, 12, 13; the result is 1.0 without the sign (`0x0079DDB1`) |
| `MouseDeltaX`, `MouseDeltaY` | `0x0079DDC3`, `0x0079DE1D` | when the modifier code is 0 or its mouse byte is set: the integer at mapper `+0x184` or `+0x188`, times the sign and 0.05 (`0x008F30E8`) |
| `TouchDragX` to `TouchRotate` | `0x0079DE90`-`0x0079E0DB` | the touch device `0x00796FC0(3, m_id)`: values at `+0x8C`, `+0x90`, `+0xE4`, `+0x170`, and two-finger drags computed with `sqrtf` and `cosf` (`0x0079DF6B`, `0x0079DFBF`) |
| `MotionQuatX` to `MotionLinearAccelerationZ` | `0x0079E134`-`0x0079E214` | the motion device `0x00796FC0(4, m_id)`: floats at `+0xE0`-`+0xEC`, `+0x50`-`+0x58`, `+0x40`-`+0x48` |
| `VisionTrackerX` to `Z` | `0x0079E24A`-`0x0079E279` | the vector at mapper `+0x234 + 16 × m_id`, when the byte at `+0x2B4 + m_id` is set |

For the touch, motion and vision types, each class reads one value:

| Class | Value | Read at |
|---|---|---|
| `TouchDragX`, `TouchDragY` | the touch device's `+0x8C`, `+0x90` | `0x0079DEC7`, `0x0079DF0C` |
| `TouchTwoFingerDragX`, `TouchTwoFingerDragY` | computed from the touch device's `+0x120`, `+0x124` with `cosf` and `sqrtf` | `0x0079DFCD`, `0x0079E095` |
| `TouchPinch`, `TouchRotate` | the touch device's `+0xE4`, `+0x170` | `0x0079E0D0`, `0x0079E0F4` |
| `MotionQuatX`, `Y`, `Z`, `W` | the motion device's `+0xE0`, `+0xE4`, `+0xE8`, `+0xEC` | `0x0079E144`, `0x0079E15F`, `0x0079E17A`, `0x0079E195` |
| `MotionAngularVelocityX`, `Y`, `Z` | the motion device's `+0x50`, `+0x54`, `+0x58` | `0x0079E1AE`, `0x0079E1C6`, `0x0079E1DE` |
| `MotionLinearAccelerationX`, `Y`, `Z` | the motion device's `+0x40`, `+0x44`, `+0x48` | `0x0079E1F4`, `0x0079E20C`, `0x0079E224` |
| `VisionTrackerX`, `Y`, `Z` | the first, second and third float of the mapper's vector | `0x0079E25B`, `0x0079E270`, `0x0079E285` |

For a pad axis with codes 1, 2, 4 or 5 the value is zeroed only when both it and its partner axis (`+0x58` with
`+0x60`, `+0x68` with `+0x70`) are inside their dead zones, the float at each record's `+0x24`
(`0x0079DB04`-`0x0079DB52`).

### The one entry

`0x0079CFB0` has no caller. Its only reference is the `lea` at `0x00794A52`, where `0x007943E0` builds the caller object
`0x02EAC670` (vtable `0x01CB3BD8`, function `0x0079CFB0`) for the method `getInput` that it registers on the application
class (`0x007949E2`). `0x007943E0` runs from the application's slot 1, `0x0079F9E0` (`0x0079F9E4`). `0x0079E2C0` and
`0x0079DA10` each have one caller (`0x0079CFE3`, `0x0079E31B`).

So a source is read against the devices only when a script calls `getInput` on the application, and only through a
source that the reflection loader built from data. No game function reads a semantic or a source: outside their
initialisers and teardowns, the registry functions, the source classes and the evaluator, the only references to
the 79 objects are the input recorder `0x0079E880` and the input replay `0x0079A120`, which
[the application framework](../PhyreEngine/phyre-application.md) shows are never called in the
shipped game.

### The code space

The pad-button codes are the pad-button band of the game's own control codes: `Button_0`, `Button_Square` and
`Button_X` are 11, through `Button_15` and `Button_Left` at 26, the same codes [keymap.ini](keymap-file.md) stores
and [Control names](control-names.md) lists for the channel names. The key fallback keeps a key source in the
keyboard band, 28 and up. The axis codes 1-10 are a separate space: they select a stick value of the pad, not a
control code. Inside a mouse source, codes 11-13 mean the three mouse buttons; in keymap.ini the mouse buttons are
codes 1-3.

## Columns

[`phyre-input-semantics.tsv`](phyre-input-semantics.tsv), one row per object, sorted by address:

| Column | Meaning |
|---|---|
| `global` | the object's address; its first qword is the vtable pointer |
| `name` | the name string the object points at (`+0x08`) |
| `class` | `PInputTypeSemantic`, `PInputAxisSemantic` or `PInputJoypadButtonSemantic` |
| `code` | the code at `+0x18`, decimal; `-` for a type object, which has no code |
| `registry` | the head of the list the object is inserted into |
| `initialiser` | the static initialiser, with the address of its insert call |
| `teardown` | the exit teardown it registers |
| `writers` | every instruction that stores into the object's vtable slot: the teardown's store and the class's deleting destructor |
| `readers` | every function that takes the object's address or reads its fields, with the instruction |

## Data

### Semantic objects

`InputTypeSemantic` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | `0x01CD7F68`, stored back by the exit teardown |
| `+0x08` | `void*` | name | the name string, compared by the registry's insert, resolver and find |
| `+0x10` | `void*` | next | the next object in the list, set by the insert `0x008760A0` |

`InputCodeSemantic` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | `0x01CD80B8` for an axis, `0x01CD8448` for a pad button |
| `+0x08` | `void*` | name | the name string |
| `+0x10` | `void*` | next | the next object in the list, set by `0x00876490` or `0x008768A0` |
| `+0x18` | `u32` | code | returned by `0x00879750`; read by the source slot-1 functions |

### Sources and actions

`PInputSource` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | the class vtable, `0x01CD6268` for the base class |
| `+0x08` | `void*` | descriptor | the class descriptor, stored by every source constructor (`0x0086C460`-`0x0086C49B`; `0x00869E3D` in the pad-axis constructor `0x00869E20`); no registered member covers it (`0x0086B410` registers the `0x28`-byte class at `0x0086B460`) |
| `+0x10` | `void*` | m_typeSemantic | one of the 25 type objects; compared by `0x0079DA10` |
| `+0x18` | `u32` | m_id | the device index: keyboard below 7, pad below 18 (`0x0079DA7D`, `0x0079DCE0`); m_id (u32), registered by `0x0086DA70` (`0x00632960` at `0x0086DB71`); no shipped .phyre file declares PInputSource |
| `+0x1C` | `u8` | m_invert | 1 makes the sign -1.0 (`0x0079DA1D`); m_invert (u8), registered by `0x0086DA70` (`0x00632960` at `0x0086DBE0`); no shipped .phyre file declares PInputSource |
| `+0x1D` | `u8[3]` | pad1D | alignment bytes after m_invert (u8 at `+0x1C`) up to m_scale (f32 at `+0x20`); no registered member covers it (`0x0086B410` registers the `0x28`-byte class at `0x0086B460`) |
| `+0x20` | `f32` | m_scale | multiplies the result (`0x0079E291`); 1.0 from the constructor; m_scale (f32), registered by `0x0086DA70` (`0x00632960` at `0x0086DC4F`); no shipped .phyre file declares PInputSource |
| `+0x24` | `u8[4]` | pad24 | the bytes after m_scale (`+0x20`) up to the end of the `0x28`-byte base class, where the derived sources' own fields start; no registered member covers it (`0x0086B410` registers the `0x28`-byte class at `0x0086B460`) |

`PInputSourceJoypadButton` (`0x40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[40]` | base | the PInputSource fields |
| `+0x28` | `u32` | positiveCode | code of `+0x30`, written by `0x00873FE0` |
| `+0x2C` | `u32` | negativeCode | code of `+0x38`, written by `0x00873FE0` |
| `+0x30` | `void*` | m_positiveButtonSemantic | a pad-button object |
| `+0x38` | `void*` | m_negativeButtonSemantic | a pad-button object |

`PInputSourceKey` (`0x40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[40]` | base | the PInputSource fields |
| `+0x28` | `u32` | positiveCode | code of `+0x30`, written by `0x00874080` |
| `+0x2C` | `u32` | negativeCode | code of `+0x38`, written by `0x00874080` |
| `+0x30` | `void*` | m_positiveKeySemantic | a key object |
| `+0x38` | `void*` | m_negativeKeySemantic | a key object |

`PInputSourceMouseDelta` (`0x40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[40]` | base | the PInputSource fields; the X and Y classes share this layout |
| `+0x28` | `u32` | modifierButtonCode | code of `+0x30`, written by `0x00874170` |
| `+0x2C` | `u32` | modifierKeyCode | code of `+0x38`, written by `0x00874170` |
| `+0x30` | `void*` | m_modifierButtonSemantic | a mouse-button object |
| `+0x38` | `void*` | m_modifierKeySemantic | a key object |

`PInputSourceJoypadAxis` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[40]` | base | the PInputSource fields |
| `+0x28` | `u32` | axisCode | code of `+0x30`, written by `0x00873FB0` and the constructor `0x00869E20` |
| `+0x2C` | `u8[4]` | pad2C | alignment bytes between axisCode (u32 at `+0x28`) and m_joypadAxisSemantic (pointer at `+0x30`); no registered member covers it (`0x0086B4C0` registers the `0x38`-byte class at `0x0086B50A`) |
| `+0x30` | `void*` | m_joypadAxisSemantic | an axis object |

`PInputSourceMouseButton` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[40]` | base | the PInputSource fields |
| `+0x28` | `u32` | buttonCode | code of `+0x30`, written by `0x00874120` and the constructor `0x0086C520` |
| `+0x2C` | `u8[4]` | pad2C | alignment bytes between buttonCode (u32 at `+0x28`) and m_mouseButtonSemantic (pointer at `+0x30`); no registered member covers it (`0x0086BCE0` registers the `0x38`-byte class at `0x0086BD2A`) |
| `+0x30` | `void*` | m_mouseButtonSemantic | a mouse-button object |

`PInputAction` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `void*` | m_name | the action name, compared by `0x00873C70` (read through `0x00873C40`); m_name (ptr), registered by `0x0086D670` (`0x00632960` at `0x0086D705`); no shipped .phyre file declares PInputAction; the destructor `0x0086C830` frees it when it owns the text (bit `0x1` clear; `0x0086C8E4`) |
| `+0x10` | `u32` | sourceCount | m_inputSources count; bit `0x80000000` is masked off (`0x0079E2E4`) |
| `+0x14` | `u8[4]` | pad14 | the four bytes between the source count at `+0x10` and the source pointer at `+0x18`, the array header the destructor `0x0086C830` clears (`0x0086C8BB`, `0x0086C8BF`); no registered member covers it (`0x0086B2B0` registers the `0x28`-byte class at `0x0086B300`) |
| `+0x18` | `void*` | sources | m_inputSources, the source pointers `0x0079E2C0` walks |

`PInputMapper` (`0x2C8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x014` | `u8[4]` | bytes14 | the four bytes after the dword the constructor `0x00792DD0` clears at `+0x10` (`0x00792EFF`), before the qword it clears at `+0x18` (`0x00792DE6`); no registered member covers it (`0x00791CD0` registers the `0x2C8`-byte class at `0x00791D20`) |
| `+0x028` | `u8[8]` | bytes28 | the eight bytes between the qword the constructor `0x00792DD0` clears at `+0x20` (`0x00792DEA`) and the one it clears at `+0x30` (`0x00792DEE`); no registered member covers it (`0x00791CD0` registers the `0x2C8`-byte class at `0x00791D20`) |
| `+0x2BC` | `u8[4]` | bytes2BC | the four bytes between the dword the constructor `0x00792DD0` sets to `0x17` at `+0x2B8` (`0x00792E1F`) and the qword it clears at `+0x2C0` (`0x00792E30`); no registered member covers it (`0x00791CD0` registers the `0x2C8`-byte class at `0x00791D20`) |

`PMeshInstanceSegmentContext` (`0x48` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x2C` | `u8[4]` | pad2C | the four bytes between the dword the placement constructor `0x005CF520` sets to -1 at `+0x28` (`0x005CF53B`) and the qword it clears at `+0x30` (`0x005CF542`); no registered member covers it (`0x005D9890` registers the `0x48`-byte class at `0x005D98DA`) |

### Registry globals

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x02EB8260` | `void*` | typeHead | head of the PInputTypeSemantic list (`0x008760A0`, `0x00876130`, `0x00876280`, `0x008761A0`) |
| `0x02EB8270` | `void*` | typeDescriptor | the PInputTypeSemantic named-semantic descriptor, vtable `0x01CD7F90` (`0x00875F86`) |
| `0x02EB82D8` | `void*` | axisHead | head of the PInputAxisSemantic list (`0x00876490`, `0x00876520`, `0x00876670`, `0x00876590`) |
| `0x02EB82E0` | `void*` | axisDescriptor | the PInputAxisSemantic named-semantic descriptor, vtable `0x01CD80E0` (`0x00876376`) |
| `0x02EB8348` | `void*` | buttonHead | head of the PInputJoypadButtonSemantic list (`0x008768A0`, `0x00876930`, `0x00876A80`, `0x008769A0`) |
| `0x02EB8350` | `void*` | buttonDescriptor | the PInputJoypadButtonSemantic named-semantic descriptor, vtable `0x01CD8480` (`0x00876756`) |

## Related

- [Control names](control-names.md) - the key and channel registries, built the same way, and the control codes.
- [Keymap file](keymap-file.md) - the file that stores the same pad-button and key codes.
- [Controls](controls.md) - how the game itself reads keys, buttons and sticks.
- [Static initialisation and teardown](../Compiler-And-C-Runtime/static-initialisation-and-teardown.md) - the
  registry insert shape, the exit teardowns and the mouse-button registry.
- [Phyre modules](../PhyreEngine/phyre-modules.md) - the `PInputs` module and its register
  `0x00875E10`.
- [PhyreEngine application framework](../PhyreEngine/phyre-application.md) - the input mapper, its
  devices, and the recorder and replay that never run.
- [Phyre reflection](../PhyreEngine/phyre-reflection.md) - class descriptors, type references by
  name and `PCluster::create`.
