---
title: "PhyreEngine modules: the engine libraries linked into the game, where their code lies and how they start and stop"
kind: "system"
category: "PhyreEngine"
addresses: "0x02CACC90, 0x00D26BC0, 0x005A08E0, 0x005A0840, 0x005A0CB0, 0x01F2CDF0, 0x00166210, 0x006CCC10, 0x00167B90, 0x0059D550, 0x005A0D20, 0x005C5C80, 0x00608A40, 0x00654830, 0x006716D0, 0x00685AC0, 0x006A4100, 0x006C45F0, 0x006C4860, 0x006CCD60, 0x00875E10, 0x008762E0, 0x0087AE00, 0x00792350, 0x006388C0, 0x00639450"
---

## What the player sees

Nothing directly. Drawing, animation, the post-processing effects, model and mesh data, the loading of
`.phyre` files and the framework's input layer are PhyreEngine code rather than the game's own; the game
drives them. Every module is started once before the window opens and stopped once when the game
exits, so a module that fails to start stops the game from starting.

## How it works

### The module list

Each PhyreEngine library that has start-up work owns one static object derived from `Phyre::PUtility`
(base vtable `0x00D26BC0`). The objects form a singly linked list whose head is `0x02CACC90`:

PUtility module object:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable: 0x00D26BC0 in the image, the module's own after construction |  |
| `+0x08` | `void*` | next module, 0 at the end |  |
| `+0x10` | `void*` | module name string ("Rendering", "Text", ...) |  |
| `+0x18` | `u32` | ordering key, 0xFF in every module |  |

The base vtable has three slots: `0x005A0CB0` (destroy), and `0x005C5230` (return 0) for init and
shutdown. Each module class overrides init (`+0x08`) and shutdown (`+0x10`) where it has work.

### Registration before `main`

Each module's static initialiser runs from the C run-time initialiser table and has the same shape,
shown by `0x00166210` (`PScripting`): it walks the list while the node's key is below `0xFF`, splices
its object in at that point, writes the module's vtable into the object, and passes the object's
destructor to `atexit` (`0x00808B90`). Every key is `0xFF`, so the walk stops at the head and each module
goes in at the front: the list ends up in the reverse of the initialiser order.

The text module is the exception in form only. Its object `0x02E5BE88` lies in zero-initialised storage,
so its initialiser `0x00167B90` calls a constructor, `0x006CCC10`, that also writes the base vtable, the
key `0xFF` and the name `Text` before inserting, and then fills a seven-pointer table at `0x02E5BE50`
with the addresses of seven `0x20`-byte slots from `0x02E5BEA8`.

### The init walk `0x005A08E0`

The framework start-up calls it once (`0x00798603`, [application framework](phyre-application.md)). Guarded
by the byte `0x02CACCA0`, it:

1. allocates a `0xE0`-byte object (`0x0062EA20`) into `0x01F7F5B8` and creates the synchronisation object
   at `0x02D3E880` (`0x00677450`);
2. registers the core reflected types: a run of calls, ten of whose results go to the name intern
   `0x006388C0`;
3. walks the list from `0x02CACC90`, calling each module's init with the module object; a non-zero result
   is returned at once, so the modules after it never start;
4. registers more core types (`0x00686C40`), calibrates the timers (`0x005CC980`) and stores the start time
   in `0x02CB60E8`;
5. stores `0x40000`, `0x8000` and `0x800` in `0x01F2EB34`, `0x01F2EB38` and `0x01F2EB3C` (`0x006AA380`,
   `0x006AA360`, `0x006AA350`), starts the object from `0x006AA280` (its slot 2), builds the type lists
   and the per-kind index (`0x00637F20`, `0x00637A70`, `0x00638AE0`, whose entries `0x00634350` allocates);
6. registers the shutdown walk `0x005A0840` with `atexit` and sets `0x02CACCA0`.

In list order the inits run: DeveloperExtensions, Hierarchy, Game, Inputs, Text, LOD, DynamicGeometry,
Physics, Scripting, Geometry, PostProcessing, Rendering, Animation, Scene, Serialization.

### Dependency calls that do not run

Several inits, and the `PApplication` constructor `0x00792350`, call other modules' inits directly before
their own work (Rendering calls Geometry, DynamicGeometry and LOD; LOD and PostProcessing call
Rendering; Physics calls Geometry and Scene). Every such call is guarded by the byte `0x01F2CDF0` being
0. That byte is 1 in the image and no instruction writes it, so none of these calls runs and each module
is started by the walk alone.

### Shutdown

`0x005A0840` runs only while `0x02CACCA0` is set:

1. It walks the list calling each module's shutdown and ignores the results.
2. It ends the 5 ms timer period (`0x005CCB90`, `timeEndPeriod(5)`, the counterpart of the `timeBeginPeriod(5)` in
   `0x005CC980`) and stops the `0x006AA280` object (its slot 3).
3. It runs the deferred-destruction reaper `0x00638C90` and closes the synchronisation object (`0x00677520`).
4. It destroys the `0xE0`-byte object's four `0x38`-byte entries (`0x0062EAF0`, through the vector destructor
   iterator `0x00809054` with `0x0062EA60`), frees the object and clears `0x02CACCA0`.

The start-up calls it directly when the message loop ends; the `atexit` call that follows finds the byte clear
and does nothing.

At process exit each module's `atexit` destructor writes the base vtable back and unlinks the object.
Slot 0, `0x005A0CB0`, does the same and frees the object when bit 0 of its flag argument is set.

### What each module holds

The classes named in each namespace's RTTI, plain classes and template arguments alike, say what the
module contains. The init columns count calls to the name intern `0x006388C0`, one per reflected type
the init registers.

| Module | Classes it names | Init |
|---|---|---|
| `PSerialization` | `PStream`, `PStreamReaderFile`, `PStreamWriterFile`, the `PBinary` cluster header types | 1 type; shutdown frees the list at `0x02CA9D88` |
| `PScene` | `PNode` | one call, `0x006B41A0` |
| `PAnimation` | animation sets, clips, channels, channel target binds, blender and time controllers, animation events | 4 types and 47 helper calls |
| `PRendering` | shaders and shader passes, D3D11 textures (2D, 3D, cube), render targets, constant and structured buffers, materials, lights, shadow casters, mesh instances, context switches, the renderer | 22 types, then the render set-up (`0x0062D0D0`, `0x005FD2A0`) |
| `PPostProcessing` | atmospherics, cel shading, deferred lighting, depth of field, FXAA, glow, low-resolution particles, MLAA, motion blur, SSAO, screen-space reflection, each with a D3D11 class | 26 types |
| `PGeometry` | meshes and mesh segments, vertex streams, index and data blocks, skin bone remaps, skeleton joint bounds, material sets | 4 types and 40 helper calls |
| `PScripting` | `PScript`, `PScheduler`, the asynchronous process batches | registers four script library openers by name through `0x006844C0`: `math`, `bit32`, `string`, `coroutine` |
| `PPhysics` | box, capsule, cylinder, mesh, plane and sphere shapes, each with a Bullet class; a character camera | 21 types |
| `PDynamicGeometry` | modifier networks, morph weights, render streams | 1 type and 30 helper calls |
| `PLOD` | LOD groups and levels, blend and metric types | 2 types |
| `PText` | `PBitmapFont`, `PBitmapFontCharInfo` | two calls |
| `PInputs` | input actions, input sources (pad axes and buttons, keys, mouse, motion, touch, vision tracker), input semantics | 6 types and 34 helper calls |
| `PGame` | `PGameConfig` | one call, `0x00879D60` |
| `PHierarchy` | `POctree`, `POctreeWorld` | creates the `POctreeChildren` allocator at `0x02EBA2A0` |
| `PDeveloperExtensions` | the module class only | none: init and shutdown are both `0x005C5230` |

The `PHierarchy` init `0x0087AE00` also sets up the static at `0x02EBA2A8` (`0x0087A8C0`), an object of three
arrays at `+0x00`, `+0x10` and `+0x20`. The module shutdown `0x0087AE80` frees the first and last and
the `POctreeChildren` pool; the static's `atexit` destructor `0x0087A830`, registered by `0x0016D5A0`
through `0x008C1570`, frees each of the three that the object owns (bit 31 of its count clear).

The pool shutdowns `0x00879270` and `0x008792A0`, and the renderer's `0x00610630`, empty a pool with
`0x006803D0` and then trim it with `0x00680210`, which returns every element on the free list to its
block, frees each block whose elements are all free and links the rest back into the free list.

### Namespaces without a module object

Four more namespaces have classes but no `PUtility` object, so nothing starts or stops them as a unit:
`PFramework` (the application, window and input-device classes), `PGameplay` (triggers and trigger
receivers, scriptable components), `PVision` (motion trackers) and `PProfiling` (the CPU profile
timeline). The seven `Phyre::VTS` classes (`ScreenStateWindow`, `ScreenStateFullScreen`,
`ScreenStateBorderless` and their change states) are the display-mode states, with their code at
`007Axxxx` beside the framework.

## Layouts

The module objects, their code and their entry points. The span is the narrowest run of whole 64 KB
zones holding at least 80 % of the vtable slot targets used only by that namespace's classes.

| Module | Object | Registrar | Module vtable | Init | Shutdown | Exit destructor | Code span |
|---|---|---|---|---|---|---|---|
| `PSerialization` | `0x01F2CD80` | `0x00160320` | `0x00D26C40` | `0x0059D550` | `0x0059FE20` | `0x008A8CE0` | `0x00580000`–`0x0059FFFF` |
| `PScene` | `0x01F2CDF8` | `0x00160380` | `0x00D27DC0` | `0x005A0D20` | stub | `0x008A8DC0` | `0x006B0000`–`0x006BFFFF` |
| `PAnimation` | `0x01F2CE20` | `0x001610E0` | `0x00D31260` | `0x005C5C80` | `0x005CB150` | `0x008AAD40` | `0x005A0000`–`0x005CFFFF` |
| `PRendering` | `0x01F2D680` | `0x00162B70` | `0x00D497F8` | `0x00608A40` | `0x00610630` | `0x008AE6D0` | `0x005C0000`–`0x0061FFFF` |
| `PPostProcessing` | `0x01F2E800` | `0x00165420` | `0x00D61E30` | `0x00654830` | `0x0065D700` | `0x008B0B40` | `0x00630000`–`0x0064FFFF` |
| `PGeometry` | `0x01F2E9B8` | `0x00165EA0` | `0x00D68DA0` | `0x006716D0` | `0x006739A0` | `0x008B1A60` | `0x00650000`–`0x0067FFFF` |
| `PScripting` | `0x01F2EAC8` | `0x00166210` | `0x00D6FD98` | `0x00685AC0` | `0x00685F60` | `0x008B2670` | `0x00680000`–`0x0068FFFF` |
| `PPhysics` | `0x01F2EB00` | `0x00166C30` | `0x00D79770` | `0x006A4100` | stub | `0x008B3E30` | `0x00680000`–`0x0068FFFF` |
| `PDynamicGeometry` | `0x01F2EE60` | `0x00167810` | `0x00D85138` | `0x006C45F0` | `0x006C4750` | `0x008B6A40` | `0x006B0000`–`0x006DFFFF` |
| `PLOD` | `0x01F2EE80` | `0x00167870` | `0x00D85168` | `0x006C4860` | stub | `0x008B6AA0` | `0x006C0000`–`0x006CFFFF` |
| `PText` | `0x02E5BE88` | `0x00167B90` | `0x00D89C68` | `0x006CCD60` | stub | `0x008B6F00` | `0x00670000`–`0x0067FFFF` |
| `PInputs` | `0x01F44D70` | `0x0016AB40` | `0x01CD7D10` | `0x00875E10` | stub | `0x008B9890` | `0x00860000`–`0x0087FFFF` |
| `PGame` | `0x01F44FE8` | `0x0016AEC0` | `0x01CD7FF0` | `0x008762E0` | stub | `0x008BA260` | `0x00870000`–`0x0087FFFF` |
| `PHierarchy` | `0x01F47550` | `0x0016D5B0` | `0x01CDA1F8` | `0x0087AE00` | `0x0087AE80` | `0x008C1580` | `0x00870000`–`0x0087FFFF` |
| `PDeveloperExtensions` | `0x01F47570` | `0x0016D610` | `0x01CDA228` | stub | stub | `0x008C15E0` | none |

"Stub" is `0x005C5230`, which returns 0. The namespaces without a module object lie at `0x00790000`–`0x0079FFFF`
(`PFramework`), `0x006A0000`–`0x006CFFFF` (`PGameplay`) and `0x00870000`–`0x0087FFFF` (`PVision`).

Each module's member list sits beside this page. It is a selection of the module's functions: vtable
slot targets of the module's own classes and bodies reached only from them or from the reflection
templates bound to the module. The code-span column, not the list, gives the module's extent.

| Module | Member list | Functions |
|---|---|---:|
| `PAnimation` | [phyre-modules-panimation.tsv](phyre-modules-panimation.tsv) | 238 |
| `PDynamicGeometry` | [phyre-modules-pdynamicgeometry.tsv](phyre-modules-pdynamicgeometry.tsv) | 42 |
| `PFramework` | [phyre-modules-pframework.tsv](phyre-modules-pframework.tsv) | 47 |
| `PGameplay` | [phyre-modules-pgameplay.tsv](phyre-modules-pgameplay.tsv) | 19 |
| `PGeometry` | [phyre-modules-pgeometry.tsv](phyre-modules-pgeometry.tsv) | 72 |
| `PHierarchy` | [phyre-modules-phierarchy.tsv](phyre-modules-phierarchy.tsv) | 16 |
| core (`Phyre::` with no module) | [phyre-modules-phyrecore.tsv](phyre-modules-phyrecore.tsv) | 58 |
| `PInputs` | [phyre-modules-pinputs.tsv](phyre-modules-pinputs.tsv) | 103 |
| `PLOD` | [phyre-modules-plod.tsv](phyre-modules-plod.tsv) | 30 |
| `PPhysics` | [phyre-modules-pphysics.tsv](phyre-modules-pphysics.tsv) | 134 |
| `PPostProcessing` | [phyre-modules-ppostprocessing.tsv](phyre-modules-ppostprocessing.tsv) | 161 |
| `PProfiling` | [phyre-modules-pprofiling.tsv](phyre-modules-pprofiling.tsv) | 1 |
| `PRendering` | [phyre-modules-prendering.tsv](phyre-modules-prendering.tsv) | 310 |
| `PScene` | [phyre-modules-pscene.tsv](phyre-modules-pscene.tsv) | 9 |
| `PScripting` | [phyre-modules-pscripting.tsv](phyre-modules-pscripting.tsv) | 23 |
| `PSerialization` | [phyre-modules-pserialization.tsv](phyre-modules-pserialization.tsv) | 19 |
| `PText` | [phyre-modules-ptext.tsv](phyre-modules-ptext.tsv) | 9 |

[phyre-modules-phyre-function-class-map.tsv](phyre-modules-phyre-function-class-map.tsv) maps every
function filed as PhyreEngine code to the class it belongs to, by the vtable slot it sits in or the
vtable it installs. [phyre-modules-phyre-module-utility-registrars.tsv](phyre-modules-phyre-module-utility-registrars.tsv)
lists thirteen of the fifteen registrars, all but `PScripting`'s `0x00166210` and `PText`'s `0x00167B90`.

## Shipped data

| Fact | Value |
|---|---|
| module objects | 15, 14 with an initial image in `.data`, `PText` in zero-initialised storage |
| initial state of the 14 | base vtable `0x00D26BC0`, next 0, key `0xFF` |
| dependency guard `0x01F2CDF0` | 1 |
| registrar slots in the initialiser table | `0x008C3520` (`PSerialization`) to `0x008C5670` (`PDeveloperExtensions`) |
| RTTI | 2,286 vtables, 1,743 classes under `Phyre::` |
| functions in the function-to-class map | 6,769 |
| placed on one class by a vtable slot | 1,606 |
| at the slots of several classes | 1,063 |
| placed by the vtable they install | 1,846 |
| with no vtable evidence | 2,254 |

## Operations

- Start: `0x005A08E0`, once, from the framework start-up, before the window exists.
- Stop: `0x005A0840`, once, after the message loop; then each module's `atexit` destructor.
- Enumerate: walk from `0x02CACC90` through `+0x08`; `+0x10` names each module.

## Modding notes

- All fifteen objects exist before `main`, at fixed addresses. A loader that runs earlier than
  `0x005A08E0` finds every module registered and none started.
- A module init that returns non-zero stops the walk and the game does not start; the modules after it
  in list order are never initialised.
- Because `0x01F2CDF0` is 1, the list order is the only start order: LOD, for example, starts before
  Rendering although its init carries a call to Rendering's.
- `0x005A0CB0` is slot 0 of every module vtable, so a change there affects how every module is destroyed.

## Related

- [Application framework](phyre-application.md): the start-up function that calls the two walks.
- [Class hierarchy](../Engine-Core/class-hierarchy.md): the RTTI tables the class names and
  vtables come from.
- [Game application](../Engine-Core/game-application.md): the game's application object.
