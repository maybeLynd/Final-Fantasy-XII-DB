---
title: "PhyreEngine modules: the engine libraries linked into the game, where their code lies and how they start and stop"
kind: "system"
category: "PhyreEngine"
summary: "The PhyreEngine modules in the executable: the fifteen PUtility module objects that register themselves before main on one list, the init walk that starts them and the shutdown walk and exit destructors that stop them, what each module holds by its RTTI class names, each module's code span and entry points, the namespaces that have no module object, and the member lists and function-to-class map kept beside the page."
addresses: ["02CACC90", "00D26BC0", "005A08E0", "005A0840", "005A0CB0", "01F2CDF0", "00166210", "006CCC10", "00167B90", "0059D550", "005A0D20", "005C5C80", "00608A40", "00654830", "006716D0", "00685AC0", "006A4100", "006C45F0", "006C4860", "006CCD60", "00875E10", "008762E0", "0087AE00", "00792350", "006388C0", "00639450"]
---

# PhyreEngine modules: the engine libraries linked into the game, where their code lies and how they start and stop

## What the player sees

Nothing directly. Drawing, animation, the post-processing effects, model and mesh data, the loading of
`.phyre` files and the framework's input layer are PhyreEngine code rather than the game's own; the game
drives them. Every module is started once before the window opens and stopped once when the game
exits, so a module that fails to start stops the game from starting.

## How it works

### The module list

Each PhyreEngine library that has start-up work owns one static object derived from `Phyre::PUtility`
(base vtable `00D26BC0`). The objects form a singly linked list whose head is `02CACC90`:

```
PUtility module object
+0x00  ptr   vtable: 00D26BC0 in the image, the module's own after construction
+0x08  ptr   next module, 0 at the end
+0x10  ptr   module name string ("Rendering", "Text", ...)
+0x18  u32   ordering key, 0xFF in every module
```

The base vtable has three slots: `005A0CB0` (destroy), and `005C5230` (return 0) for init and
shutdown. Each module class overrides init (`+0x08`) and shutdown (`+0x10`) where it has work.

### Registration before `main`

Each module's static initialiser runs from the C run-time initialiser table and has the same shape,
shown by `00166210` (`PScripting`): it walks the list while the node's key is below `0xFF`, splices
its object in at that point, writes the module's vtable into the object, and passes the object's
destructor to `atexit` (`00808B90`). Every key is `0xFF`, so the walk stops at the head and each module
goes in at the front: the list ends up in the reverse of the initialiser order.

The text module is the exception in form only. Its object `02E5BE88` lies in zero-initialised storage,
so its initialiser `00167B90` calls a constructor, `006CCC10`, that also writes the base vtable, the
key `0xFF` and the name `Text` before inserting, and then fills a seven-pointer table at `02E5BE50`
with the addresses of seven `0x20`-byte slots from `02E5BEA8`.

### The init walk `005A08E0`

The framework start-up calls it once (`00798603`, [application framework](phyre-application.md)). Guarded
by the byte `02CACCA0`, it:

1. allocates a `0xE0`-byte object (`0062EA20`) into `01F7F5B8` and creates the synchronisation object
   at `02D3E880` (`00677450`);
2. registers the core reflected types: a run of calls, ten of whose results go to the name intern
   `006388C0`;
3. walks the list from `02CACC90`, calling each module's init with the module object; a non-zero result
   is returned at once, so the modules after it never start;
4. registers more core types (`00686C40`), calibrates the timers (`005CC980`) and stores the start time
   in `02CB60E8`;
5. sizes and starts the object from `006AA280` (`0x40000`, `0x8000`, `0x800`, then its slot 2), builds
   the type lists and the per-kind index (`00637F20`, `00637A70`, `00638AE0`);
6. registers the shutdown walk `005A0840` with `atexit` and sets `02CACCA0`.

In list order the inits run: DeveloperExtensions, Hierarchy, Game, Inputs, Text, LOD, DynamicGeometry,
Physics, Scripting, Geometry, PostProcessing, Rendering, Animation, Scene, Serialization.

### Dependency calls that do not run

Several inits, and the `PApplication` constructor `00792350`, call other modules' inits directly before
their own work (Rendering calls Geometry, DynamicGeometry and LOD; LOD and PostProcessing call
Rendering; Physics calls Geometry and Scene). Every such call is guarded by the byte `01F2CDF0` being
0. That byte is 1 in the image and no instruction writes it, so none of these calls runs and each module
is started by the walk alone.

### Shutdown

`005A0840` runs only while `02CACCA0` is set. It walks the list calling each module's shutdown and
ignores the results, then stops the `006AA280` object (its slot 3), runs the deferred-destruction
reaper `00638C90`, closes the synchronisation object (`00677520`), frees the `0xE0`-byte object and
clears `02CACCA0`. The start-up calls it directly when the message loop ends; the `atexit` call that
follows finds the byte clear and does nothing.

At process exit each module's `atexit` destructor writes the base vtable back and unlinks the object.
Slot 0, `005A0CB0`, does the same and frees the object when bit 0 of its flag argument is set.

### What each module holds

The classes named in each namespace's RTTI, plain classes and template arguments alike, say what the
module contains. The init columns count calls to the name intern `006388C0`, one per reflected type
the init registers.

| Module | Classes it names | Init |
|---|---|---|
| `PSerialization` | `PStream`, `PStreamReaderFile`, `PStreamWriterFile`, the `PBinary` cluster header types | 1 type; shutdown frees the list at `02CA9D88` |
| `PScene` | `PNode` | one call, `006B41A0` |
| `PAnimation` | animation sets, clips, channels, channel target binds, blender and time controllers, animation events | 4 types and 47 helper calls |
| `PRendering` | shaders and shader passes, D3D11 textures (2D, 3D, cube), render targets, constant and structured buffers, materials, lights, shadow casters, mesh instances, context switches, the renderer | 22 types, then the render set-up (`0062D0D0`, `005FD2A0`) |
| `PPostProcessing` | atmospherics, cel shading, deferred lighting, depth of field, FXAA, glow, low-resolution particles, MLAA, motion blur, SSAO, screen-space reflection, each with a D3D11 class | 26 types |
| `PGeometry` | meshes and mesh segments, vertex streams, index and data blocks, skin bone remaps, skeleton joint bounds, material sets | 4 types and 40 helper calls |
| `PScripting` | `PScript`, `PScheduler`, the asynchronous process batches | registers four script library openers by name through `006844C0`: `math`, `bit32`, `string`, `coroutine` |
| `PPhysics` | box, capsule, cylinder, mesh, plane and sphere shapes, each with a Bullet class; a character camera | 21 types |
| `PDynamicGeometry` | modifier networks, morph weights, render streams | 1 type and 30 helper calls |
| `PLOD` | LOD groups and levels, blend and metric types | 2 types |
| `PText` | `PBitmapFont`, `PBitmapFontCharInfo` | two calls |
| `PInputs` | input actions, input sources (pad axes and buttons, keys, mouse, motion, touch, vision tracker), input semantics | 6 types and 34 helper calls |
| `PGame` | `PGameConfig` | one call, `00879D60` |
| `PHierarchy` | `POctree`, `POctreeWorld` | creates the `POctreeChildren` allocator at `02EBA2A0` |
| `PDeveloperExtensions` | the module class only | none: init and shutdown are both `005C5230` |

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
| `PSerialization` | `01F2CD80` | `00160320` | `00D26C40` | `0059D550` | `0059FE20` | `008A8CE0` | `00580000`–`0059FFFF` |
| `PScene` | `01F2CDF8` | `00160380` | `00D27DC0` | `005A0D20` | stub | `008A8DC0` | `006B0000`–`006BFFFF` |
| `PAnimation` | `01F2CE20` | `001610E0` | `00D31260` | `005C5C80` | `005CB150` | `008AAD40` | `005A0000`–`005CFFFF` |
| `PRendering` | `01F2D680` | `00162B70` | `00D497F8` | `00608A40` | `00610630` | `008AE6D0` | `005C0000`–`0061FFFF` |
| `PPostProcessing` | `01F2E800` | `00165420` | `00D61E30` | `00654830` | `0065D700` | `008B0B40` | `00630000`–`0064FFFF` |
| `PGeometry` | `01F2E9B8` | `00165EA0` | `00D68DA0` | `006716D0` | `006739A0` | `008B1A60` | `00650000`–`0067FFFF` |
| `PScripting` | `01F2EAC8` | `00166210` | `00D6FD98` | `00685AC0` | `00685F60` | `008B2670` | `00680000`–`0068FFFF` |
| `PPhysics` | `01F2EB00` | `00166C30` | `00D79770` | `006A4100` | stub | `008B3E30` | `00680000`–`0068FFFF` |
| `PDynamicGeometry` | `01F2EE60` | `00167810` | `00D85138` | `006C45F0` | `006C4750` | `008B6A40` | `006B0000`–`006DFFFF` |
| `PLOD` | `01F2EE80` | `00167870` | `00D85168` | `006C4860` | stub | `008B6AA0` | `006C0000`–`006CFFFF` |
| `PText` | `02E5BE88` | `00167B90` | `00D89C68` | `006CCD60` | stub | `008B6F00` | `00670000`–`0067FFFF` |
| `PInputs` | `01F44D70` | `0016AB40` | `01CD7D10` | `00875E10` | stub | `008B9890` | `00860000`–`0087FFFF` |
| `PGame` | `01F44FE8` | `0016AEC0` | `01CD7FF0` | `008762E0` | stub | `008BA260` | `00870000`–`0087FFFF` |
| `PHierarchy` | `01F47550` | `0016D5B0` | `01CDA1F8` | `0087AE00` | `0087AE80` | `008C1580` | `00870000`–`0087FFFF` |
| `PDeveloperExtensions` | `01F47570` | `0016D610` | `01CDA228` | stub | stub | `008C15E0` | none |

"Stub" is `005C5230`, which returns 0. The namespaces without a module object lie at `00790000`–`0079FFFF`
(`PFramework`), `006A0000`–`006CFFFF` (`PGameplay`) and `00870000`–`0087FFFF` (`PVision`).

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
lists thirteen of the fifteen registrars, all but `PScripting`'s `00166210` and `PText`'s `00167B90`.

## Shipped data

| Fact | Value |
|---|---|
| module objects | 15, 14 with an initial image in `.data`, `PText` in zero-initialised storage |
| initial state of the 14 | base vtable `00D26BC0`, next 0, key `0xFF` |
| dependency guard `01F2CDF0` | 1 |
| registrar slots in the initialiser table | `008C3520` (`PSerialization`) to `008C5670` (`PDeveloperExtensions`) |
| RTTI | 2,286 vtables, 1,743 classes under `Phyre::` |
| functions in the function-to-class map | 6,769 |
| placed on one class by a vtable slot | 1,606 |
| at the slots of several classes | 1,063 |
| placed by the vtable they install | 1,846 |
| with no vtable evidence | 2,254 |

## Operations

- Start: `005A08E0`, once, from the framework start-up, before the window exists.
- Stop: `005A0840`, once, after the message loop; then each module's `atexit` destructor.
- Enumerate: walk from `02CACC90` through `+0x08`; `+0x10` names each module.

## Modding notes

- All fifteen objects exist before `main`, at fixed addresses. A loader that runs earlier than
  `005A08E0` finds every module registered and none started.
- A module init that returns non-zero stops the walk and the game does not start; the modules after it
  in list order are never initialised.
- Because `01F2CDF0` is 1, the list order is the only start order: LOD, for example, starts before
  Rendering although its init carries a call to Rendering's.
- `005A0CB0` is slot 0 of every module vtable, so a change there affects how every module is destroyed.

## Related

- [Application framework](phyre-application.md): the start-up function that calls the two walks.
- [Class hierarchy](../Engine-Core/class-hierarchy.md): the RTTI tables the class names and
  vtables come from.
- [Game application](../Engine-Core/game-application.md): the game's application object.
