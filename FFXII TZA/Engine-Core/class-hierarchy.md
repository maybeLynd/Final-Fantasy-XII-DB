---
title: "Class hierarchy: the C++ classes the executable names through RTTI and what they are"
kind: "system"
category: "Engine core"
addresses: "0x008C5760, 0x00D86960, 0x00903B68, 0x009007E8, 0x009010B8, 0x00904328, 0x00D360A0, 0x005C5230, 0x0016D6A0, 0x0016D680, 0x008F9B80, 0x008F3640"
---

## What the player sees

Nothing. The names are a trace the compiler left for the C++ `dynamic_cast` and `typeid`
operators: every class with virtual functions keeps a record beside its vtable that spells out its
own name and its base classes. The game never prints them. They matter because they turn a block
of anonymous functions into the methods of a named engine class, and because they show where the
game's own code is object-oriented and where it is not.

## How it works

### The locator beside every vtable

A vtable is an array of function pointers in `.rdata`. The 8-byte slot before it holds the address
of a complete object locator, a 24-byte record of six 32-bit fields: a signature of 1, the offset
of this vtable inside its object, a constructor-displacement offset, the image-relative address of
the type descriptor, that of the class hierarchy descriptor, and the locator's own image-relative
address. The last field is what makes the recovery exact: a run of bytes that contains its own
address as a relative pointer is a locator and nothing else.

The type descriptor holds the decorated class name (`.?AVGameApplication@@`), and the hierarchy
descriptor points at an array of base class descriptors, each naming a base and where it sits in
the object. Reading every locator in `.rdata` this way yields 2,286 vtables for 2,248 class names;
102 of the 2,350 type descriptors in the image name types that have no vtable, and 28 names own
two or more vtables (18 own two, 10 own three; 38 vtables beyond each name's first).

The virtual slots of a vtable are the qwords after it that hold function entries, up to the first that does
not: 25,797 slots in all, pointing at 6,882 distinct functions. Four vtables are followed by a short string
whose first 8 bytes look like a `.text` address ([vtable methods](vtable-methods.md)).

### What the classes are

The namespace is the outermost component of the decorated name, so an enclosing class
(`btCollisionWorld::RayResultCallback`, `Sys::Thread`) and a function-local class
(`btBvhTriangleMeshShape::performRaycast::MyNodeOverlapCallback`) count under their owner.

| Namespace | Primary vtables | What it is |
|---|---|---|
| `Phyre` | 1,739 | PhyreEngine: `PInternal` 168, `PPostProcessing` 37, `PInputs` 34, `PAnimation` 29, `PPhysics` 25, `PRendering` 19, `PFramework` 15 and the class-descriptor templates (14 of them over `sce::Vectormath` types) |
| `SQEX::Sd` | 218 | the Square Enix sound driver |
| global namespace | 134 | the game's own classes, the Steam callback templates, `type_info` and four `TAsyncUpdate<…>` templates over Phyre D3D11 resources |
| Bullet (`bt*`) | 76 | the physics library Phyre uses: 53 top-level, 7 nested, `btAxisSweep3Internal<unsigned short>` and 15 function-local callback classes |
| `PPFX`, `Yebis` | 43 | the Yebis post-processing library and its two D3D11 shims |
| `std`, `eastl` | 20 | stream and allocator classes of the C++ libraries |
| `mkvparser`, `JsonBox`, `Sys` | 12 | the WebM parser, the JSON reader and `Sys::Thread` |

The game's own classes fall into a few families:

- the application root `GameApplication` (vtable `0x008C5760`, 31 slots, derived from
  `Phyre::PFramework::PApplication`, `PBase` and `PMemoryBase`, [game
  application](game-application.md)) and the managers `InputManager`, `AsyncJobManager`,
  `AsyncLoadManager`, `AssetListManager`, `SaveloadManager`, `ExtraUI`, `LoadingPage` and
  `MultipleDebugDisplay`;
- the 32 render commands named `…Obj` (`RenderOpaqueObj`, `PostProcessObj`, `ZBufferObj`,
  `VideoObj`, `FastClearObj` and the rest) and the 18 `Gi…` commands (`GiVmax`, `GiSprite`,
  `GiPrim`, `GiSetTexture`, `GiBeginScene`);
- the ordered draw objects (`OrderedObject`, `MapOrderedObject`, `CharacterOrderedObject`,
  `FontBorderOrderedObject` and siblings), the eight `DynGeo…` dynamic geometry instances
  (`DynGeoTextureInstance` with 21 slots), `CharacterRenderObject` (31 slots), `MapRenderObject`,
  `ChrModel` and `PrimitiveRendererD3D11` (vtable `0x00D86960`, 45 slots);
- the 17 audio classes (the banks and controllers `AudioBank`, `MusicAudioController`,
  `StreamAudioBank` and their siblings, `AudioCallback`, `AudioFileLoadManager` and the three
  `AudioSeadObject…` classes) and the two Mersenne twister classes `MTRand_int32` and
  `MTRand_closed`.

No class belongs to combat, the party, items, spawning, the script interpreter or the world: those
systems are procedures over flat record tables, and the only game code with classes is the code
that sits against the engine (application, rendering, loading, input, audio, saving). The
PhyreEngine classes carry the engine's own reflection as well: 1,183 of the Phyre vtables are
`PClassDescriptor…<T>` templates for 409 reflected types: 367 types own three of them (`PTexture3D` has
`…Abstract`, `…Concrete` and `…ForType`), 40 own two and 2 own one.

### Inheritance and shared bodies

2,101 of the 2,242 primary vtables name at least one base: up to 13 bases (the Phyre
`PClassDescriptorHeader<T>` templates) and up to 10 levels deep (`Phyre::PPhysics::PPhysicsCapsule`, `0x00D79A38`).
44 vtables sit at a non-zero object offset, in 34 classes: 28 of them have two or
three vtables, and six `std` stream classes have that secondary vtable only. This is multiple and virtual
inheritance: `PrimitiveRendererD3D11` carries a second vtable
at `+8` for `IBatchMergerEvent` (`0x00D86AD0`, one slot), and the `std` stream classes carry theirs
for their virtual bases.

A derived class copies every base method it does not override, so one function appears in many
vtables: 2,611 of the 6,882 functions sit in more than one class and 4,271 in exactly one. The
linker also folded identical bodies across unrelated classes: `0x005C5230` (`return 0`) fills 2,514
slots, `0x0016D6A0` (`ret`, also the Control Flow Guard stub, [jump thunks](jump-thunks.md)) 1,386
and `0x0016D680` (`return this`) 1,349. A method is attributable to a class only when it appears in
that class alone, and a hook on a shared body reaches every class that folded onto it.

### How an object gets its class

A constructor stamps the vtable address into the object's first qword with
`lea reg, [vtable]; mov [object], reg`.

2,282 of the 2,286 vtables are loaded by such a `lea` in `.text`, at 5,786 sites; the four that no `lea` loads are `AdapterInfoBase` (`0x00906868`),
`Phyre::PClassDataMemberDynamicType<PClassDataMemberDynamic>` (`0x00D58468`),
`SoundObjectManagerCallbackHandler` (`0x01CB4328`) and `SQEX::Sd::HashTable` (`0x01CB4AE8`), whose vtable
address is already stored in static objects in the image file's `.data`: `0x01E02580`, `0x01F2DF30`,
`0x01F403D0`, and `0x01F40440`, `0x01F40C50` and `0x01F41460` for the last.

`AdapterInfoBase` is the base of `AdapterInfos`, `AmdAdapterInfo` and `NvidiaAdapterInfo`; the other three are
the base of no class.

Most static objects get theirs from the C++ initializers that
run before the game's entry point or, like the debug-log sink at `0x02CB6140`, on first use
(`Phyre::PTTYCallback`'s vtable `0x00D360A0`, [debug logging](debug-logging.md)); either way a
global that is zero in the image file has a class fixed at link time. The six static objects
named above hold their vtable address in the image file itself.

## Layouts

```
vtable[-1]  ptr    complete object locator
locator     u32 signature (1), u32 offset in object, u32 cdOffset, u32 typeDescriptor RVA,
            u32 classHierarchyDescriptor RVA, u32 self RVA
typeDesc    ptr type_info vtable, ptr spare, char name[] (".?AV<class>@<namespace>@@")
hierarchy   u32 signature, u32 attributes, u32 base count, u32 base array RVA
base desc   u32 typeDescriptor RVA, u32 contained bases, i32 mdisp, i32 pdisp, i32 vdisp, u32 attributes, u32 hierarchy RVA
vtable      ptr slot[0..n-1], each into .text
```

## Shipped data

| Fact | Value |
|---|---|
| vtables / class names | 2,286 / 2,248, in [class-hierarchy.tsv](class-hierarchy.tsv): vtable, decorated name, class (filled for the 626 rows without template arguments; the others are named by decorated), namespace, offset in the object, slots, base count, and the bases in base-array order joined by ` < `, some in decorated form |
| primary vtables / secondary | 2,242 / 44 (34 classes) |
| virtual slots / distinct functions | 25,797 / 6,882 |
| functions in exactly one class | 4,271 ([vtable methods](vtable-methods.md)) |
| vtables stamped by a `lea` in code | 2,282 at 5,786 sites |
| largest vtables | `PPFX::IGPUDevice` 77, the `SQEX::Sd::Driver` sound family 44; of the game's own `PrimitiveRendererD3D11` 45, `GameApplication` 31, `CharacterRenderObject` 31 |

## Operations

At link time the compiler emits the records; at process start the C++ initializers stamp the
static objects' vtables; at run time a constructor stamps each new object, and a virtual call
reads `[[object] + slot × 8]`. No cast or typeid reads the type descriptors: the executable
imports none of `__RTDynamicCast`, `__RTtypeid`, `__RTCastToVoid` or the `__std_type_info_*`
helpers, so `dynamic_cast` and `typeid` are not linked.

C++ exception handling does read them: the 69 calls to `_CxxThrowException` (through `0x00861ECC`) pass throw
records whose catchable types name type descriptors (`0x0019501D` throws `std::bad_cast`, caught as it or as
`std::exception`), and `__CxxFrameHandler3` matches catch clauses by them.

## State

The records are read-only data in `.rdata` and `.data`. The only state is each object's first
qword.

## Modding notes

- A class and slot pair is a stable hook point across builds in a way an address is not; the
  table gives the slot for every function that belongs to one class.
- Hook a function that is in several classes only if every one of them should change.
- An object whose first qword names a vtable in the table has that class; a pointer run in data
  without a locator before it is a jump table or a callback array, not a class.

## Related

- [Vtable methods](vtable-methods.md): the 25,797 slots as a table.
- [Game application](game-application.md): the `GameApplication` object and its managers.
- [Jump thunks](jump-thunks.md): the shared `ret` stub and the thunks that vtables name.
