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
| `+0x00` | `void*` |  | vtable: `0x00D26BC0` in the image, the module's own after construction |
| `+0x08` | `void*` |  | next module, 0 at the end |
| `+0x10` | `void*` |  | module name string ("Rendering", "Text", ...) |
| `+0x18` | `u32` |  | ordering key, `0xFF` in every module |

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
   at `0x02D3E880` (`0x00677450`); `0x00210EC0` allocates (`0x005A0901`), and a null result is stored without running
   the constructor `0x0062EA20` (`0x005A090E`). The stub `0x005C5230` is called between the two (`0x005A0920`), and
   its 0 lets the set-up go on;
2. registers the core reflected types: a run of calls, ten of whose results go to the name intern
   `0x006388C0`;
3. walks the list from `0x02CACC90`, calling each module's init with the module object; a non-zero result
   is returned at once, so the modules after it never start;
4. registers more core types (`0x00686C40`), calibrates the timers (`0x005CC980`) and stores the start time
   in `0x02CB60E8`; a non-zero result from `0x00686C40` or `0x005CC980` is returned at once (`0x005A0A54`,
   `0x005A0A61`), and the start time is the clock `0x005CC930`'s reading (`0x005A0A63`, `0x005A0A68`);
5. stores `0x40000`, `0x8000` and `0x800` in `0x01F2EB34`, `0x01F2EB38` and `0x01F2EB3C` (`0x006AA380`,
   `0x006AA360`, `0x006AA350`), starts the object from `0x006AA280` (its slot 2), builds the type lists
   and the per-kind index (`0x00637F20`, `0x00637A70`, `0x00638AE0`, whose entries `0x00634350` allocates);
6. returns a non-zero result of that slot 2 (`0x005A0A9C`) or of `0x00638AE0` (`0x005A0ABC`) at once; between
   `0x00637F20` and `0x00637A70` it passes the result of `0x006372A0` to the name intern `0x006388C0` (`0x005A0AA5`,
   `0x005A0AAD`);
7. registers the shutdown walk `0x005A0840` with `atexit` and sets `0x02CACCA0` (`0x005A0AC7`, `0x005A0ACC`), then
   returns 0.

When `0x02CACCA0` is already set it returns 0 at once (`0x005A08F6`). A set-up that returns early leaves the byte
clear and registers no shutdown.

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
3. It runs the deferred-destruction reaper `0x00638C90`, calls the bare `ret 0` stub `0x0016D6A0` (`0x005A088A`), and
   closes the synchronisation object (`0x00677520`).
4. When `0x01F7F5B8` holds the `0xE0`-byte object, it destroys the object's four `0x38`-byte entries (`0x0062EAF0`,
   through the vector destructor iterator `0x00809054` with `0x0062EA60`) and frees the object (`0x00809950`,
   `0x005A08B0`); with `0x01F7F5B8` null it skips both (`0x005A089E`). It then stores 0 in `0x01F7F5B8` and clears
   `0x02CACCA0` (`0x005A08BA`, `0x005A08C5`).

The start-up calls it directly when the message loop ends; the `atexit` call that follows finds the byte clear
and does nothing.

At process exit each module's `atexit` destructor writes the base vtable back and unlinks the object.
Slot 0, `0x005A0CB0`, does the same: it writes `0x00D26BC0` into the object (`0x005A0CC0`), walks from `0x02CACC90` to the
link that holds the object, and only when it finds it there stores the object's `+0x08` in that link and clears the
object's own `+0x08` (`0x005A0CCA`-`0x005A0CF4`); an object not on the list stays as it is. It frees the object's
`0x20` bytes (`0x00809950`, `0x005A0D06`) when bit `0x1` of its flag argument is set, and returns the object
(`0x005A0D0B`).

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
| `PScripting` | `PScript`, `PScheduler`, the asynchronous process batches | calls five member registrars (`0x006822E0`, `0x00681F30`, `0x006827C0`, `0x00681C50`, `0x00681D80`; `0x00685AC4`-`0x00685AD8`), then registers four script library openers by name through `0x006844C0`: `math`, `bit32`, `string`, `coroutine` (`0x00685ADD`-`0x00685B24`); returns 0 (`0x00685B29`) |
| `PPhysics` | box, capsule, cylinder, mesh, plane and sphere shapes, each with a Bullet class; a character camera | 21 types |
| `PDynamicGeometry` | modifier networks, morph weights, render streams | 1 type and 30 helper calls |
| `PLOD` | LOD groups and levels, blend and metric types | 2 types, from the getters `0x006D94E0` and `0x006D98D0`, then calls `0x006C5FF0` and `0x006C5A50` and returns 0 (`0x006C487E`-`0x006C48A2`) |
| `PText` | `PBitmapFont`, `PBitmapFontCharInfo` | two calls |
| `PInputs` | input actions, input sources (pad axes and buttons, keys, mouse, motion, touch, vision tracker), input semantics ([Phyre input semantics](../Controls-And-Input/phyre-input-semantics.md)) | 6 types and 34 helper calls |
| `PGame` | `PGameConfig` | one call, `0x00879D60` |
| `PHierarchy` | `POctree`, `POctreeWorld` | calls four registrars, `0x008786F0`, `0x008780F0`, `0x00878980` and `0x00878630` (`0x0087AE0D`-`0x0087AE1C`), each registering one type with `0x006388C0` (`0x0087870B`, `0x0087810B`, `0x0087899B`, `0x00878644`); sets up `0x02EBA2A8`, creates the `POctreeChildren` allocator at `0x02EBA2A0` and returns 0 (`0x0087AE71`) |
| `PDeveloperExtensions` | the module class only | nothing: init and shutdown are both `0x005C5230` |

The `PHierarchy` init `0x0087AE00` also sets up the static at `0x02EBA2A8` (`0x0087A8C0`), an object of three
arrays at `+0x00`, `+0x10` and `+0x20`. The module shutdown `0x0087AE80` frees the first and last and
the `POctreeChildren` pool; the static's `atexit` destructor `0x0087A830`, registered by `0x0016D5A0`
through `0x008C1570`, frees each of the three that the object owns (bit `0x80000000` of its count clear).

`0x0087AE00` allocates the `0x28`-byte `POctreeChildren` allocator with `0x00584740` (`0x0087AE37`) and builds it with
`0x0067FFB0(allocator, 0x288, 10, 8, "POctreeChildren")` (`0x0087AE46`-`0x0087AE64`); a null allocation is stored at
`0x02EBA2A0` without the build (`0x0087AE44`, `0x0087AE6A`).

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

The module objects, their entry points and how many functions belong to each (the attribution below).

| Module | Object | Registrar | Module vtable | Init | Shutdown | Exit destructor | Functions |
|---|---|---|---|---|---|---|---:|
| `PSerialization` | `0x01F2CD80` | `0x00160320` | `0x00D26C40` | `0x0059D550` | `0x0059FE20` | `0x008A8CE0` | 115 |
| `PScene` | `0x01F2CDF8` | `0x00160380` | `0x00D27DC0` | `0x005A0D20` | stub | `0x008A8DC0` | 76 |
| `PAnimation` | `0x01F2CE20` | `0x001610E0` | `0x00D31260` | `0x005C5C80` | `0x005CB150` | `0x008AAD40` | 1,181 |
| `PRendering` | `0x01F2D680` | `0x00162B70` | `0x00D497F8` | `0x00608A40` | `0x00610630` | `0x008AE6D0` | 2,662 |
| `PPostProcessing` | `0x01F2E800` | `0x00165420` | `0x00D61E30` | `0x00654830` | `0x0065D700` | `0x008B0B40` | 809 |
| `PGeometry` | `0x01F2E9B8` | `0x00165EA0` | `0x00D68DA0` | `0x006716D0` | `0x006739A0` | `0x008B1A60` | 595 |
| `PScripting` | `0x01F2EAC8` | `0x00166210` | `0x00D6FD98` | `0x00685AC0` | `0x00685F60` | `0x008B2670` | 317 |
| `PPhysics` | `0x01F2EB00` | `0x00166C30` | `0x00D79770` | `0x006A4100` | stub | `0x008B3E30` | 1,109 |
| `PDynamicGeometry` | `0x01F2EE60` | `0x00167810` | `0x00D85138` | `0x006C45F0` | `0x006C4750` | `0x008B6A40` | 424 |
| `PLOD` | `0x01F2EE80` | `0x00167870` | `0x00D85168` | `0x006C4860` | stub | `0x008B6AA0` | 106 |
| `PText` | `0x02E5BE88` | `0x00167B90` | `0x00D89C68` | `0x006CCD60` | stub | `0x008B6F00` | 63 |
| `PInputs` | `0x01F44D70` | `0x0016AB40` | `0x01CD7D10` | `0x00875E10` | stub | `0x008B9890` | 639 |
| `PGame` | `0x01F44FE8` | `0x0016AEC0` | `0x01CD7FF0` | `0x008762E0` | stub | `0x008BA260` | 17 |
| `PHierarchy` | `0x01F47550` | `0x0016D5B0` | `0x01CDA1F8` | `0x0087AE00` | `0x0087AE80` | `0x008C1580` | 100 |
| `PDeveloperExtensions` | `0x01F47570` | `0x0016D610` | `0x01CDA228` | stub | stub | `0x008C15E0` | 0 |

"Stub" is `0x005C5230`, which returns 0. The namespaces without a module object are `PFramework` (628 functions), `PGameplay` (147)
and `PVision` (74).

[`phyre-modules-attribution.tsv`](phyre-modules-attribution.tsv) attributes to a module every function that a
PhyreEngine class holds or that PhyreEngine code calls or references, 12,360 in all: by the class it belongs to
when it has one (it sits in a vtable slot of the class, or installs the class's vtable), and otherwise by the
modules whose code calls or references it.

- 10,572 belong to one module, 7,058 of them by class; 1,504 of these belong to the core (`Phyre::` classes and
  code outside any module).
- 1,788 are shared between modules: 150 sit in the vtables of classes from several modules (one body serving
  several classes) and 1,638 are used by several modules' code.
- 2,234 are also used by code outside PhyreEngine.

| Column | Meaning |
|---|---|
| `addr` | the function's entry address |
| `module` | the module it belongs to: its class's module, or the one module whose code uses it; `shared:` and the modules when there is more than one |
| `class_module` | the module of the class it belongs to, `-` for a class in no module |
| `used_by` | the modules whose code calls or references it, and `outside PhyreEngine` when other code does too |
| `classes` | the classes it belongs to, separated by `;` |

A class's module is the namespace it is declared in (`Phyre::PRendering::...`); a template instance belongs to
the module its PhyreEngine parameters name, and core (`PhyreCore`) when they name no module or several. A pointer in a
data table does not count as a use.

[phyre-modules-phyre-function-class-map.tsv](phyre-modules-phyre-function-class-map.tsv) maps every
function filed as PhyreEngine code to the class it belongs to, by the vtable slot it sits in or the
vtable it installs. Its `route` column says which of the two ties the function to a class:

- `slot1`: the function sits in the vtable of one class, which `slot_classes` names.
- `slotN`: it sits in the vtables of several classes, which `slot_classes` lists, separated by `;`: one body
  serving several classes.
- `installs`: its body stores the vtable of a class whose name begins with `Phyre::` into an object, as a
  constructor, a destructor or a factory does; `installed_classes` names the class, or the classes separated by
  `;`.
- `slot1+installs` and `slotN+installs`: both.
- `neither`: the function sits in no vtable and installs no `Phyre::` class's vtable, and both class columns are
  empty.

[phyre-modules-phyre-module-utility-registrars.tsv](phyre-modules-phyre-module-utility-registrars.tsv)
lists the thirteen registrars whose bodies are the same 86 bytes ending in a jump to `0x00808B90`; the other two,
`PScripting`'s `0x00166210` and `PText`'s `0x00167B90`, have bodies of their own.

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PLODGroup` (`0x68` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | m_minBounds | m_minBounds (f32[4]), registered by `0x006C5A50` (`0x00632960` at `0x006C5B76`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PLODGroup; the constructor `0x006C5180` sets it to (FLT_MAX, FLT_MAX, FLT_MAX) (`0x006C5180`-`0x006C5193`), an empty box with m_maxBounds |
| `+0x10` | `f32[4]` | m_maxBounds | m_maxBounds (f32[4]), registered by `0x006C5A50` (`0x00632960` at `0x006C5BE5`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PLODGroup; the constructor `0x006C5180` sets it to (-FLT_MAX, -FLT_MAX, -FLT_MAX) (`0x006C519A`-`0x006C51A8`) |
| `+0x38` | `u8[8]` | bytes38 | the constructor `0x006C5180` writes 1000.0 to m_shaderLODLevelDistance (`+0x34`) and 0 to `+0x38` with one qword store (`0x006C51E0`); no registered member covers it (`0x006C4EC0` registers the `0x68`-byte class at `0x006C4F10`) |
| `+0x61` | `u8[7]` | pad61 | the bytes after m_isEnabled (u8 at `+0x60`) up to the end of the `0x68`-byte class; no registered member covers it (`0x006C4EC0` registers the `0x68`-byte class at `0x006C4F10`) |

`POctree` (`0x50` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | m_center | m_center (f32[4]), registered by `0x008780F0` (`0x00632960` at `0x0087817E`); no shipped .phyre file declares POctree |
| `+0x10` | `f32[4]` | m_halfSize | m_halfSize (f32[4]), registered by `0x008780F0` (`0x00632960` at `0x008781F1`); no shipped .phyre file declares POctree |
| `+0x20` | `f32` | m_maxRadius | m_maxRadius (f32), registered by `0x008780F0` (`0x00632960` at `0x00878264`); no shipped .phyre file declares POctree |
| `+0x24` | `u32` | m_level | m_level (u32), registered by `0x008780F0` (`0x00632960` at `0x008782D7`); no shipped .phyre file declares POctree |
| `+0x30` | `u32` | m_currentObjectCount | m_currentObjectCount (u32), registered by `0x008780F0` (`0x00632960` at `0x00878430`); no shipped .phyre file declares POctree |
| `+0x34` | `u32` | m_totalObjectCount | m_totalObjectCount (u32), registered by `0x008780F0` (`0x00632960` at `0x008784A3`); no shipped .phyre file declares POctree |

`POctreeWorld` (`0xC8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | m_center | m_center (f32[4]), registered by `0x00878980` (`0x00632960` at `0x00878A0A`); no shipped .phyre file declares POctreeWorld |
| `+0x10` | `f32[4]` | m_halfSize | m_halfSize (f32[4]), registered by `0x00878980` (`0x00632960` at `0x00878A79`); no shipped .phyre file declares POctreeWorld |

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

## State

### Module list links

Each module object's `+0x08` is its link to the next module. Its registrar stores the list head there before it
makes the object the head, and its exit destructor reads it to unlink the object, then stores 0. The list code
also reaches every link through the node:

- the init walk `0x005A08E0` (`0x005A0A44`) and the shutdown walk `0x005A0840` (`0x005A0869`) follow each link;
- each registrar's search reads a link only past a node whose key is below `0xFF`, `(u32)[node + 0x18] < 0xFF`
  (`cmp dword ptr [rcx + 0x18], 0xff` then `jae`), which no module has (`0x0016033D`, `0x0016039D`, `0x001610FD`,
  `0x00162B8D`, `0x0016543D`, `0x00165EBD`, `0x0016622D`, `0x00166C4D`, `0x0016782D`, `0x0016788D`, `0x006CCC4C`, `0x0016AB5D`,
  `0x0016AEDD`, `0x0016D5CD`, `0x0016D62D`);
- each exit destructor's search reads the links of the nodes before its own (`0x008A8D0E`, `0x008A8DEE`, `0x008AAD6E`,
  `0x008AE6FE`, `0x008B0B6E`, `0x008B1A8E`, `0x008B269E`, `0x008B3E5E`, `0x008B6A6E`, `0x008B6ACE`, `0x008B6F2E`, `0x008B98BE`,
  `0x008BA28E`, `0x008C15AE`, `0x008C160E`);
- the registrars store through the link where their search stopped (`0x00160359`, `0x001603B9`, `0x00161119`,
  `0x00162BA9`, `0x00165459`, `0x00165ED9`, `0x00166249`, `0x00166C69`, `0x00167849`, `0x001678A9`, `0x006CCC5E`, `0x0016AB79`,
  `0x0016AEF9`, `0x0016D5E9`, `0x0016D649`);
- the exit destructors store through the link that pointed at their object (`0x008A8D26`, `0x008A8E06`, `0x008AAD86`, `0x008AE716`, `0x008B0B86`, `0x008B1AA6`, `0x008B26B6`, `0x008B3E76`, `0x008B6A86`,
  `0x008B6AE6`, `0x008B6F46`, `0x008B98D6`, `0x008BA2A6`, `0x008C15C6`, `0x008C1626`).

The registrars run in initialiser-table order, `0x008C3520` (`PSerialization`) to `0x008C5670` (`PDeveloperExtensions`),
so after the last one each link holds the module registered just before its own.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F2CD88` | `void*` | 0 | `PSerialization` (`0x01F2CD80`) `+0x08`: 0, the end of the list | `0x00160320`, the head at registration, 0 (`0x0016034B`); `0x008A8CE0`, 0 (`0x008A8D29`) | `0x008A8CE0` (`0x008A8D1F`) |
| `0x01F2CE00` | `void*` | 0 | `PScene` (`0x01F2CDF8`) `+0x08`: `PSerialization` | `0x00160380` (`0x001603AB`); `0x008A8DC0`, 0 (`0x008A8E09`) | `0x008A8DC0` (`0x008A8DFF`) |
| `0x01F2CE28` | `void*` | 0 | `PAnimation` (`0x01F2CE20`) `+0x08`: `PScene` | `0x001610E0` (`0x0016110B`); `0x008AAD40`, 0 (`0x008AAD89`) | `0x008AAD40` (`0x008AAD7F`) |
| `0x01F2D688` | `void*` | 0 | `PRendering` (`0x01F2D680`) `+0x08`: `PAnimation` | `0x00162B70` (`0x00162B9B`); `0x008AE6D0`, 0 (`0x008AE719`) | `0x008AE6D0` (`0x008AE70F`) |
| `0x01F2E808` | `void*` | 0 | `PPostProcessing` (`0x01F2E800`) `+0x08`: `PRendering` | `0x00165420` (`0x0016544B`); `0x008B0B40`, 0 (`0x008B0B89`) | `0x008B0B40` (`0x008B0B7F`) |
| `0x01F2E9C0` | `void*` | 0 | `PGeometry` (`0x01F2E9B8`) `+0x08`: `PPostProcessing` | `0x00165EA0` (`0x00165ECB`); `0x008B1A60`, 0 (`0x008B1AA9`) | `0x008B1A60` (`0x008B1A9F`) |
| `0x01F2EAD0` | `void*` | 0 | `PScripting` (`0x01F2EAC8`) `+0x08`: `PGeometry` | `0x00166210` (`0x0016623B`); `0x008B2670`, 0 (`0x008B26B9`) | `0x008B2670` (`0x008B26AF`) |
| `0x01F2EB08` | `void*` | 0 | `PPhysics` (`0x01F2EB00`) `+0x08`: `PScripting` | `0x00166C30` (`0x00166C5B`); `0x008B3E30`, 0 (`0x008B3E79`) | `0x008B3E30` (`0x008B3E6F`) |
| `0x01F2EE68` | `void*` | 0 | `PDynamicGeometry` (`0x01F2EE60`) `+0x08`: `PPhysics` | `0x00167810` (`0x0016783B`); `0x008B6A40`, 0 (`0x008B6A89`) | `0x008B6A40` (`0x008B6A7F`) |
| `0x01F2EE88` | `void*` | 0 | `PLOD` (`0x01F2EE80`) `+0x08`: `PDynamicGeometry` | `0x00167870` (`0x0016789B`); `0x008B6AA0`, 0 (`0x008B6AE9`) | `0x008B6AA0` (`0x008B6ADF`) |
| `0x02E5BE90` | `void*` | 0 (zero-initialised storage) | `PText` (`0x02E5BE88`) `+0x08`: `PLOD` | `0x006CCC10` through the object `0x00167B90` passes (`0x006CCC5A`); `0x008B6F00`, 0 (`0x008B6F49`) | `0x008B6F00` (`0x008B6F3F`) |
| `0x01F44D78` | `void*` | 0 | `PInputs` (`0x01F44D70`) `+0x08`: `PText` | `0x0016AB40` (`0x0016AB6B`); `0x008B9890`, 0 (`0x008B98D9`) | `0x008B9890` (`0x008B98CF`) |
| `0x01F44FF0` | `void*` | 0 | `PGame` (`0x01F44FE8`) `+0x08`: `PInputs` | `0x0016AEC0` (`0x0016AEEB`); `0x008BA260`, 0 (`0x008BA2A9`) | `0x008BA260` (`0x008BA29F`) |
| `0x01F47558` | `void*` | 0 | `PHierarchy` (`0x01F47550`) `+0x08`: `PGame` | `0x0016D5B0` (`0x0016D5DB`); `0x008C1580`, 0 (`0x008C15C9`) | `0x008C1580` (`0x008C15BF`) |
| `0x01F47578` | `void*` | 0 | `PDeveloperExtensions` (`0x01F47570`) `+0x08`: `PHierarchy` | `0x0016D610` (`0x0016D63B`); `0x008C15E0`, 0 (`0x008C1629`) | `0x008C15E0` (`0x008C161F`) |

### Text technique table

The table at `0x02E5BE50` holds one record per text rendering technique, in the order of the names at `0x00D89BE0`.
`0x006CCC10` stores the addresses of the seven `0x20`-byte records, which the initialisers named below build through
`0x005DC6F0` with the technique's name. `0x006CCCE0(mode)` returns entry `mode`, reading it image-base-relative
(`0x006CCCF1`). Only for an entry of 0 would it search the render-pass registry `0x02CBF998` by name and store the
result (`0x006CCD53`); `0x006CCC10` leaves no entry 0.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02E5BE50` | `void*` | 0 | entry 0: `0x02E5BEA8`, `RenderText_AlphaBlend`, built by `0x00167A40` | `0x006CCC10` (`0x006CCC72`); `0x006CCCE0` (`0x006CCD53`) | `0x006CCCE0` (`0x006CCCF1`) |
| `0x02E5BE58` | `void*` | 0 | entry 1: `0x02E5BEC8`, `RenderText_AlphaTest`, built by `0x00167A70` | `0x006CCC10` (`0x006CCC80`); `0x006CCCE0` (`0x006CCD53`) | `0x006CCCE0` (`0x006CCCF1`) |
| `0x02E5BE60` | `void*` | 0 | entry 2: `0x02E5BEE8`, `RenderText_HardEdges`, built by `0x00167AA0` | `0x006CCC10` (`0x006CCC8E`); `0x006CCCE0` (`0x006CCD53`) | `0x006CCCE0` (`0x006CCCF1`) |
| `0x02E5BE68` | `void*` | 0 | entry 3: `0x02E5BF08`, `RenderText_SoftEdges`, built by `0x00167B60` | `0x006CCC10` (`0x006CCC9C`); `0x006CCCE0` (`0x006CCD53`) | `0x006CCCE0` (`0x006CCCF1`) |
| `0x02E5BE70` | `void*` | 0 | entry 4: `0x02E5BF28`, `RenderText_SoftEdgesAndOutline`, built by `0x00167B00` | `0x006CCC10` (`0x006CCCAA`); `0x006CCCE0` (`0x006CCD53`) | `0x006CCCE0` (`0x006CCCF1`) |
| `0x02E5BE78` | `void*` | 0 | entry 5: `0x02E5BF48`, `RenderText_SoftEdgesAndShadow`, built by `0x00167B30` | `0x006CCC10` (`0x006CCCB8`); `0x006CCCE0` (`0x006CCD53`) | `0x006CCCE0` (`0x006CCCF1`) |
| `0x02E5BE80` | `void*` | 0 | entry 6: `0x02E5BF68`, `RenderText_SoftEdgesAndGlow`, built by `0x00167AD0` | `0x006CCC10` (`0x006CCCC6`); `0x006CCCE0` (`0x006CCD53`) | `0x006CCCE0` (`0x006CCCF1`) |

### Animation job pool

The `PAnimation` init `0x005C5C80` ends by jumping to `0x005BEF70` (`0x005C6009`). That function creates the pool only
while `0x02CAD030` is 0. A failed allocation leaves the pointer 0 and makes the init return `0xD`, which stops the
init walk.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CAD030` | `void*` | 0 | the `0x28`-byte pool object named `ANIThreadPoolJobs`, built by `0x0067FFB0(pool, 0x20, 0x80, 8, name)`, which stores `0x20` at `+0x18`, `0x80` at `+0x1C` and 8 at `+0x20` | `0x005BEF70`, the new object (`0x005BEFBD`); `0x005CB150`, the `PAnimation` shutdown, 0 after `0x00680030` and `0x00584730` free the pool (`0x005CB184`) | `0x005BEF70` (`0x005BEF7D`); `0x005CB150` (`0x005CB166`) |

No other instruction loads the pointer (no RIP-relative, image-base-relative or disp32 reference names it), so no
code takes elements from the pool.

### PLOD group flag

Slot `+0x70` of both vtables of the one `PLODGroup` descriptor `0x02E5AE00` (`0x00D85490`, which its registrar
`0x006C4EC0` installs, then `0x00D85518`, which its initialiser `0x001678D0` installs), the slot a loader calls for a
class's loaded list, is `0x006C4CD0`, which jumps to `0x006C68B0`. That function sets one byte before it walks the list.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02E5ACF0` | `u8` | 0 | set to 1 each time `0x006C68B0` runs | `0x006C68B0` (`0x006C68BE`) | no reader: no RIP-relative, image-base-relative or disp32 reference outside the store names it |

### The default class layout interface

`0x01F2E0D0` is the one shared `Phyre::PClassLayoutInterface` (vtable `0x00D26BE0`, RTTI
`.?AVPClassLayoutInterface@Phyre@@`), initialised data that already holds its vtable. `0x006372B0` returns its address
(`0x006372D7`) behind a thread-safe guard on `0x02CF9404` (`0x008092FC`, `0x0080929C`) that registers the exit routine `0x008AF500`
(`0x006372FF`), which stores the vtable again (`0x008AF507`).

The child-class visitors take it as their layout interface: `PFindNestedClassVisitor` (`0x00D276F8`) in `0x0059BED0`
(`0x0059C0F1`), and `PDeleteChildrenVisitor` (`0x00D2D310`) in `0x005A3E50`, `0x005D18C0`, `0x006CEE50` and `0x006D9E30` (`0x005A3E6A`,
`0x005D18DA`, `0x006CEE6A`, `0x006D9E4A`). `0x005FD2A0` passes it to `0x005FD700` (`0x005FD3AD`), and `0x00639C80` compares a layout
pointer with it (`0x00639D30`, `0x00639D35`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F2E0D0` | `PClassLayoutInterface` | the vtable `0x00D26BE0` | the shared default class layout interface | `0x008AF500`, the vtable at exit (`0x008AF507`) | through the address `0x006372B0` returns (`0x006372D7`), by the seven callers above |

### Hierarchy triangle tables

The `PHierarchy` init `0x0087AE00` passes the static `0x02EBA2A8` and level 2 to `0x0087A8C0` (`0x0087AE21`, `0x0087AE26`).
That function sizes two of the static's three `{u32 count, ptr buffer}` arrays from the level. Bit `0x80000000` of a count
marks a buffer the array does not own, which no code frees. It starts them as an octahedron: six corners
(`0x0087A99B`-`0x0087AA35`) and eight triangles (`0x0087AA42`-`0x0087AADD`). It then subdivides the triangles once per
level, starting at `0x0087AB50`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EBA2B0` | `void*` | 0 | `+0x08`: the corner buffer, room for 126 (8 × 4² − 2) records of four floats; the first six are (0, 0, 1, 1), (0, 0, −1, 1) and (±0.7071, ±0.7071, 0, 1) | `0x0087A8C0` (`0x0087A923`); `0x0087AE80`, the `PHierarchy` shutdown, 0 (`0x0087AEDF`); `0x0087A830`, 0 (`0x0087A8A7`) | `0x0087A8C0` (`0x0087A902`, `0x0087A98B`, `0x0087AB70`); `0x0087AE80` (`0x0087AEC5`); `0x0087A830` (`0x0087A898`) |
| `0x02EBA2C8` | `u32` | 0 | `+0x20`: the count of the triangle array, 384 (3 × 8 × 4²) | `0x0087A8C0` (`0x0087A97F`); `0x0087AE80`, 0 (`0x0087AF17`); `0x0087A830`, 0 (`0x0087A868`) | `0x0087A8C0` (`0x0087A930`, `0x0087A963`); `0x0087AE80` (`0x0087AEEC`); `0x0087A830` (`0x0087A847`) |
| `0x02EBA2D0` | `void*` | 0 | `+0x28`: the triangle buffer, `u32` corner indices three per triangle; the first triangle is corners 0, 3 and 4 | `0x0087A8C0` (`0x0087A97B`); `0x0087AE80`, 0 (`0x0087AF10`); `0x0087A830`, 0 (`0x0087A864`) | `0x0087A8C0` (`0x0087A95A`, `0x0087A997`, `0x0087AB50`); `0x0087AE80` (`0x0087AEF6`); `0x0087A830` (`0x0087A853`) |

Apart from `0x0087A8C0`, which builds the arrays, only the shutdown `0x0087AE80` and the exit destructor `0x0087A830`
use them, to free them; `0x008C1570` passes `0x0087A830` the static's address and jumps to it. No instruction but
those in `0x0087AE00`, `0x0087AE80` and `0x008C1570` names `0x02EBA2A8`-`0x02EBA2D7`, RIP-relative, image-base-relative
or as a disp32.

### The engine clock

The engine set-up `0x005A08E0` calls `0x005CC980` (`0x005A0A5A`) before it starts the modules. `0x005CC980` raises the timer
resolution with `timeBeginPeriod(5)`, takes `timeGetTime`, reads the performance-counter frequency into `0x02CB6120`
and its reciprocal into `0x02CB6128`, and takes the counter's first reading. It returns `0x17`, which stops the
set-up, only when both `timeBeginPeriod` and `QueryPerformanceFrequency` failed (`0x005CCA06`, `0x005CCA8D`).

`0x005CC930`, the engine's clock, divides each counter reading by `0x02CB6120`, `t = (f64)counter / (f64)[0x02CB6120]`,
both read as unsigned 64-bit values (`0x005CC939`-`0x005CC975`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CB60F0` | `u8` | 0 (zero-filled tail of `.data`) | 1 when `timeBeginPeriod(5)` returned 0, success | `0x005CC980` (`0x005CC991`, `sete`) | `0x005CC980` (`0x005CCA06`) |
| `0x02CB60F1` | `u8` | 0 (zero-filled tail of `.data`) | 1 when `QueryPerformanceFrequency` returned 1, success | `0x005CC980` (`0x005CC9ED`, `sete`) | `0x005CC980` (`0x005CCA8D`) |
| `0x02CB60F4` | `u32` | 0 (zero-filled tail of `.data`) | the `timeGetTime` milliseconds at set-up | `0x005CC980` (`0x005CC9B8`) | `0x005CC980` (`0x005CCA51`, converted to a double as an unsigned value) |
| `0x02CB6118` | `i64` | 0 (zero-filled tail of `.data`) | the first performance-counter reading; 1 is stored first, then `QueryPerformanceCounter` fills it through the address `0x005CC9D7` passes (`0x005CCA00`) | `0x005CC980` (`0x005CC9AD`, 1; `QueryPerformanceCounter`) | `0x005CC980` (`0x005CCA10`, converted to a double as a signed value) |
| `0x02CB6108` | `f64` | 0 (zero-filled tail of `.data`) | that reading in seconds: `0x02CB6118` times `0x02CB6128` | `0x005CC980` (`0x005CCA24`) | no instruction names it |
| `0x02CB60F8` | `u32` | 0 (zero-filled tail of `.data`) | the reading in milliseconds divided by 2^32 (`0x009002D8` = 1000.0, `0x00D36060` = 2^-32), truncated | `0x005CC980` (`0x005CCA44`) | no instruction names it |
| `0x02CB6100` | `f64` | 0 (zero-filled tail of `.data`) | `0x02CB60F8` times 2^32 (`0x00D36068`) plus `0x02CB60F4` | `0x005CC980` (`0x005CCA68`) | no instruction names it |
| `0x02CB6110` | `f64` | 0 (zero-filled tail of `.data`) | 0.0 | `0x005CC980` (`0x005CCA83`) | no instruction names it |
| `0x02CB6130` | `f64` | 0 (zero-filled tail of `.data`) | 0.0 | `0x005CC980` (`0x005CCA73`) | no instruction names it |
| `0x02CB6138` | `f64` | 0 (zero-filled tail of `.data`) | 0.0 | `0x005CC980` (`0x005CCA7B`) | no instruction names it |

### Render-pass numbering

The `PRendering` init `0x00608A40` ends by jumping to `0x005FD560` (`0x00608DC0`). It sets `+0x18` of every record on the
render-pass list `0x02CBF998` to -1, then numbers the records from 0 in list order, stores the count and sizes the
array `0x02CB6780` to eight bytes per record (`0x0063DE00`). While `0x02CB6358` is set it returns `0x12` and changes
nothing.

`0x005F0720`, called from `0x005CF6E0`, sets that byte and uses the count: it clears that many pointer slots
(`0x005F07A0`-`0x005F07B1`, compared unsigned) and files each record under its number. The `PRendering` shutdown
`0x00610630` clears both and empties `0x02CB6780`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CB635C` | `u32` | 0 (zero-filled tail of `.data`) | the number of records on the render-pass list | `0x005FD560` (`0x005FD5BE`); `0x00610630` (`0x0061066D`, 0) | `0x005F0720` (`0x005F0734`, `0x005F078F`, `0x005F07A5`, `0x005F07F4`) |
| `0x02CB6358` | `u8` | 0 (zero-filled tail of `.data`) | 1 once `0x005F0720` has used the numbers; it locks them | `0x005F0720` (`0x005F073A`, 1); `0x00610630` (`0x00610685`, 0) | `0x005FD560` (`0x005FD564`) |

### Scene-wide parameter buffers

The `PRendering` init calls `0x005FD2A0(0x40)` (`0x00608DA2`) after `0x0062D0D0`.

It points an array at the 23
parameter records of `0x18` bytes at `0x02CB7DA0` that `0x00162B30` builds, names them from the table `0x00D3EB30`, measures one block of them with `0x005FD700`, and allocates that many blocks and
that many constant-buffer objects.

The 23 names, in order: `EyeDirWS`, `EyePosWS`, `Proj`, `View`, `ViewInv`, `ViewInvTranspose`, `ViewProj`, `NearFarPlane`, `NearTimesFarPlane`, `FarMinusNearPlane`, `FarMinusNearInv`, `AspectRatio`, `ViewportWidthHeight`, `ViewportWidthHeightInv`, `ScreenWidthHeight`, `ScreenWidthHeightInv`, `GlobalAmbientColor`, `Time`, `DitherNoiseTexture`, `LowResDepthTexture`, `RWDeferredLightBuffer`, `RWCapturedTriangleBuffer`, `SceneWideParameterConstantBuffer`.

Its count word `0x02CB8448`, the object array `0x02CB8478` and the lock `0x02CB8480`
are listed with `0x005FD2A0` and `0x005FE200` in [phyre-engine-helpers.tsv](phyre-engine-helpers.tsv). The `PRendering`
shutdown `0x00610630` runs `0x005FE200` (`0x00610658`), which takes the lock, releases everything and stores 0.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CB8450` | `void*` | 0 (zero-filled tail of `.data`) | the parameter records: `0x02CB7DA0`, with the count word `0x80000017`, 23 records the array does not own | `0x005FD2A0` (`0x005FD2F1`); `0x005FE200` (`0x005FE256`, 0) | `0x005FD2A0` (`0x005FD2C4`, `0x005FD3CB`); `0x005FE200` (`0x005FE236`) |
| `0x02CB8458` | `u16` | 0 (zero-filled tail of `.data`) | the size of one block, from `0x005FD700`, rounded up to 16 bytes | `0x005FD2A0` (`0x005FD3EF`); `0x005FE200` (`0x005FE2A6`, 0) | no instruction names it |
| `0x02CB8460` | `void*` | 0 (zero-filled tail of `.data`) | the blocks, allocated by `0x0017D260` with 16-byte alignment and zeroed | `0x005FD2A0` (`0x005FD406`); `0x005FE200` (`0x005FE2BF`, 0, after freeing it) | `0x005FE200` (`0x005FE2B3`) |
| `0x02CB8468` | `u32` | 0 (zero-filled tail of `.data`) | the number of blocks: the argument rounded up to even, 64 | `0x005FD2A0` (`0x005FD40D`); `0x005FE200` (`0x005FE2AD`, 0) | no instruction names it |
| `0x02CB8470` | `u32` | 0 (zero-filled tail of `.data`) | the number of `0x50`-byte constant-buffer objects at `0x02CB8478`, also 64; bit `0x80000000` set marks objects the array does not own. Each is built by `0x00615550`, resized by `0x00628050(object, 8)` when its `+0x18` count is not 8, and given `0x5E4` at `+0x00` | `0x005FD2A0` (`0x005FD4CD`); `0x005FE200` (`0x005FE32A`, 0) | `0x005FD2A0` (`0x005FD427`, `0x005FD4AC`); `0x005FE200` (`0x005FE265`, `0x005FE298`, `0x005FE2C6`) |
| `0x02CB84A8` | `u32` | 0 (zero-filled tail of `.data`) | 0 when the blocks are allocated | `0x005FD2A0` (`0x005FD413`) | no instruction names it |

`0x005FD2A0` also zeroes the `0xB30` bytes from `0x02CB84B0` (`0x005FD534`).

### Statics the `PAnimation` shutdown clears

The `PAnimation` shutdown `0x005CB150` empties two more statics after the job pool. The first is an array of
`{u32 count, ptr buffer}` whose buffer it frees when bit `0x80000000` of the count is clear; the exit destructor `0x008A9240`,
registered by `0x00160BE0`, does the same. The second group follows the channel-semantic count `0x02CACF18` and the
`0x100` bytes of semantic slots from `0x02CACF20` (see [animation binding](phyre-animation-binding.md)); it clears them
only when the array's buffer equals `0x02CAD020` (`0x005CB192`). Every instruction that names any of these globals
stores 0.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CAE650` | `u32` | 0 (zero-filled tail of `.data`) | the array's count word | `0x005CB150` (`0x005CB1D8`, 0); `0x008A9240` (`0x008A9276`, 0) | `0x005CB150` (`0x005CB1B4`); `0x008A9240` (`0x008A924D`) |
| `0x02CAE658` | `void*` | 0 (zero-filled tail of `.data`) | the array's buffer | `0x005CB150` (`0x005CB1D1`, 0); `0x008A9240` (`0x008A926F`, 0) | `0x005CB150` (`0x005CB18B`); `0x008A9240` (`0x008A925C`) |
| `0x02CACF1C` | `u32` | 0 (zero-filled tail of `.data`) | the word after the semantic count | `0x005CB150` (`0x005CB19B`, 0) | no instruction names it |
| `0x02CAD020` | `void*` | 0 (zero-filled tail of `.data`) | the qword after the semantic slots | `0x005CB150` (`0x005CB1A1`, 0) | `0x005CB150` (`0x005CB192`, compared for equality) |
| `0x02CAD028` | `u32` | 0 (zero-filled tail of `.data`) | the next dword | `0x005CB150` (`0x005CB1A8`, 0) | no instruction names it |
| `0x02CAD02C` | `u32` | 0 (zero-filled tail of `.data`) | the next dword | `0x005CB150` (`0x005CB1AE`, 0) | no instruction names it |

## Modding notes

- All fifteen objects exist before `main`, at fixed addresses. A loader that runs earlier than
  `0x005A08E0` finds every module registered and no module started.
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
