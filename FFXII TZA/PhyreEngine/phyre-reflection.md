---
title: "Phyre reflection: how PhyreEngine describes its classes at run time, registers their members and creates instances"
kind: "system"
category: "PhyreEngine"
addresses: "0x00632D80, 0x00632C90, 0x00632E80, 0x005A7ED0, 0x001603E0, 0x00639450, 0x00639160, 0x0063E410, 0x006388C0, 0x006311D0, 0x0063BA10, 0x00632960, 0x00632FB0, 0x00632A10, 0x00632A70, 0x00632BE0, 0x0062EFD0, 0x0062F080, 0x00597220, 0x0063C0C0, 0x006B66C0, 0x006B67D0, 0x006B67F0, 0x0063A990, 0x00639510, 0x0063C910, 0x00639A60, 0x00639C80, 0x0063CB80, 0x00633390, 0x0063D550, 0x0063D640, 0x006B6700, 0x00633240, 0x005847E0, 0x00584730, 0x02CF8260, 0x01F2E330, 0x01F2E780, 0x02CF8270, 0x02CF8470, 0x02CF8570"
---

## What the player sees

Nothing directly. Every model, texture, shader, animation and scene the game loads from a `.phyre`
file becomes an object through this layer: the loader finds each class in the file by name, matches
its fields to the members registered here, and builds instances from the class's default instance.
A class or field the executable does not register cannot be brought in by editing assets.

## How it works

### The class descriptor and its types

Each reflected class has one descriptor, a `Phyre::PClassDescriptor` object of `0x100` bytes. The
constructor `0x00632D80(descriptor, namespace, name, size, alignment, parent, adjust)` empties the six
list heads, stores the name pointer at `+0x30`, the instance size at `+0x38`, the alignment at
`+0x3C`, the namespace at `+0x70`, the parent descriptor at `+0x78` and the adjustment at `+0xF0`,
and takes the next value of the global counter `0x02CF8260` as its index at `+0xE8` (`0x00632E39`-`0x00632E45`).
`0x00632C90` is the same without a parent or adjustment.

Both also point the three type-tree links `+0x08`, `+0x10` and `+0x18` at `+0x08`, zero the hash `+0x20` and the
key `+0x28` (`0x00632D8E`-`0x00632DA1`), zero the hooks `+0x40` and `+0x48`, install the vtable `0x00D581C0`
(`0x00632DCE`), zero the five words `+0xC0` to `+0xE0`, store `0xFFFFFFFF` at `+0xEC` and return the descriptor.
`0x00632D80` zeroes `+0xF4` and `+0xF8` with one 8-byte store (`0x00632E62`) and the flags `+0xFC` (`0x00632E69`).
`0x00632C90` stores 0 in `+0x78` (`0x00632CEC`) and zeroes `+0xF0` to `+0xFF` with two 8-byte stores (`0x00632D63`,
`0x00632D6A`).

The vtable it installs is replaced by the class's own: `PClassDescriptorAbstract<T>`,
`PClassDescriptorConcrete<T>` or `PClassDescriptorForType<T>`, all derived from `PClassDescriptor`,
which derives from `Phyre::PType`.

`PClassDescriptorDynamic` (`0x00632E80`) is a `0x140`-byte form that copies its name and is built at
load time for a class no code registers.

`0x00632E80(descriptor, namespace, name, parent)` calls `0x00632D80` with the parent's instance size `+0x38` as the
size, the parent's alignment `+0x3C` and the negated parent size as the adjustment (`0x00632EA6`-`0x00632EC1`). It reads
the parent without a null test; `0x0059AC00` skips a class whose parent has no descriptor (`0x0059ACD5`), and
`0x0062FB80` gives `PBase` (`0x02CF8270`).

It installs its vtable `0x00D58380`, zeroes the two words at `+0x100` and the three pairs at `+0x108`, stores the
parent's size at `+0x104`, copies the name with `0x001C26B0` into `+0x138` (0 for a null name), points `+0x30` at the
copy with bit `0x1` cleared and sets flag bit `0x1` (`0x00632F18`).

It then computes the offsets (`0x0063E410`), grows the default instance and masks (`0x0063AE50`), clears flag bit
`0x80000000` (`0x00632F3C`) and builds the default instance and masks (`0x00639A60`, then `0x00639C80`, each given 0),
using no result of these calls. When the default instance `+0xC0` exists, the class is `PComponent` (`0x02E4E720`) or
derives from it, and the instance size is at least `0x18`, it stores the descriptor in the default instance's
class-descriptor field `+0x10`, counted from the layout base `+0xF8` (`0x00632F5A`-`0x00632F8D`). It returns the
descriptor.

`0x0062FB80` builds one in place with no name under `PBase` in the default namespace (`0x006373D0`) when its address
argument is non-null (`0x0062FB9E`), and returns 1 either way.

Its attach slot
`0x00639290` counts accepted members in the two words at `+0x100` and `+0x102`, and when they differ
first rebuilds the descriptor through `0x0063D550` (empty the six lists, copy the parent's size and
alignment, recompute the offsets through `0x0063E410`).

Its attach slot `0x00639290(descriptor, member, third)` answers 0 at once, counting nothing, for a member whose
qword `+0x20` equals the qword at `0x01F2DF28` (`0x0063929F`-`0x006392B5`). Otherwise, after the rebuild, it attaches
through `0x0062EFD0(descriptor, member, third)`; a non-zero answer is returned with nothing counted
(`0x006392E5`-`0x006392EE`). After the two counts it calls `0x0063D930(descriptor, third)` and answers 0
(`0x006392F0`-`0x00639304`).

`0x0063D550` itself rebuilds when the two words differ or are both 0, and keeps the descriptor when they are equal
and non-zero (`0x0063D556`-`0x0063D56C`). The rebuild points the six lists `+0x50`, `+0x80`, `+0x90`, `+0xA0`, `+0xB0`
and `+0x60` at themselves and zeroes both words (`0x0063D572`-`0x0063D5E0`). With a parent `+0x78` it also stores the
parent's size in `+0x104` and `+0x38`, its alignment in `+0x3C` and `-[parent+0x38]` in `+0xF0`, then calls
`0x0063E410` (`0x0063D5EF`-`0x0063D60F`); without a parent the rebuild ends after the lists and the two words.

Rebuilt or not, `0x0063D550` then refreshes the name
pointer `+0x30` from `+0x138` and tail-jumps to `0x0063AE50` (`0x0063D634`), which grows the default instance
`+0x110` and the two mask buffers `+0x120` and `+0x130` to the instance size `+0x38`, zeroes the added bytes
and points `+0xC0`, `+0xC8` and `+0xD0` at them; it returns `0xD` when the allocation fails.

A dynamic class's members are placed one after another. `0x0063C630`, called from `0x006393A0`, takes
the member's width and alignment from its type (8 and 8 for attribute bit `0x2`), aligns the running
end at `+0x104`, adds the width, raises `+0x3C` to the alignment and rounds `+0x38` up to it, and
returns the member's offset less the parent's size.

Loaded `PClassDataMemberDynamic` records are reset by that descriptor's slot `+0x70` (`0x0062F4E0`, which jumps to `0x006361C0`): it empties each
record's node and annotation list, clears attribute bit `0x1`, takes the name from the tagged pointer
at `+0x58`, and places the record through `0x0063D410` when its owner is dynamic.

### Registration

A class is registered in two steps:

1. Its descriptor is built. For most classes this runs before `main`: the C runtime's initialiser
   table holds `0x001603E0`, which calls the Abstract constructor `0x005A7ED0` (`0x00632D80`, see below), clears
   bit `0x2` (`0x001603F0`), installs the Concrete vtable `0x00D29E90` (`0x00160405`) and registers the teardown
   `0x008A8E20` (`0x00160410`).
   Template classes such as `PArray<T>` are built on first use inside a thread-safe static.
2. Its members are registered by descriptor slot `+0x60` (for `PAnimatableComponent`, `0x005A25E0`
   jumps to `0x005AD8F0`), each member behind its own thread-safe static, and the function ends in the
   finaliser `0x00639450`.

For `PAnimatableComponent`, `0x005A7ED0` calls `0x00632D80(…, "PAnimatableComponent", 0x108, 8, …, 8)` on the
static descriptor `0x02CAD140` (`0x005A7F1A`), the parent `…` being `PComponent` (`0x02E4E720`). It installs the
Abstract vtable `0x00D29BF0` (`0x005A7F27`), sets flag `+0xFC` bit `0x2` (`0x005A7F2A`), registers the three buffers
below (`0x0063DC80`, `0x0063DF90`, `0x0063DFA0`) and returns the descriptor (`0x005A7F5F`).

The finaliser calls `0x00639160(namespace, descriptor)` (`0x00639460`), which looks the name `+0x30` up in the
namespace (`0x0063BA10`, `0x0063917C`). Finding the descriptor itself, it returns at once (`0x00639189`). Finding another
class of that name, it reports a second class of the same name: it tail-jumps to the log call `0x005CDAA0` on
channel 2 with the message that a class descriptor of that name already exists in this namespace, and links
nothing (`0x0063918F`-`0x006391AD`).

Otherwise it links the descriptor's `+0x50` node into the namespace's
class list: at the front, or straight after its parent when the parent belongs to the same namespace
(`0x00639208`-`0x00639244`). When the namespace held no class before and is not the default namespace, it then links
the namespace's own node `+0x00` at the front of the default namespace's child list `+0x28` (`0x0063924C`-`0x00639277`).

Before it links, a namespace in state 2 logs "Adding class '%s' to namespace after initialization" on channel 1
(`0x006391E0`-`0x006391F2`).
When the namespace state is 1 or 2 it also computes the layout offsets (`0x0063E410`). The finaliser
then sets `+0xFC` bit `0x40000000`, the mark that members are registered (`0x00639465`).

For a dynamic class (bit `0x1` of `+0xFC`) the finaliser then resets the tree node at `+0x08`, its links at
`+0x08`, `+0x10` and `+0x18` to the node itself and `+0x20` and `+0x28` to 0, and tail-jumps to `0x006388C0`, which
enters the descriptor in the type tree (`0x00639478`-`0x0063949D`). Any other class returns there (`0x006394A7`).

### Layout offsets

`0x0063E410` sums `+0xF0` over the class and every ancestor up to the root descriptor `0x02CF8270`
into `+0xF4`, the root's own `+0xF0` left out (`0x0063E416`-`0x0063E448`), and stores the class's own non-negative
`+0xF0` plus the parent's `+0xF8` in `+0xF8`, that is `max([+0xF0], 0) + [parent+0xF8]`, with 0 for the parent's
part when there is no parent (`0x0063E44A`-`0x0063E47F`).

A member's position in an object is its registered offset minus the owning class's `+0xF4`
(`0x0063C910`, `0x00639C80`, `0x0063CB80`). `PAnimatableComponent` passes 8: its reflected layout starts
8 bytes into the object, after the vtable pointer. Its member visitor `0x005A2390` is handed the
object and forms `object + 8` itself (`0x005A2399`), keeping a null object null (`0x005A23A8`), before
it calls `0x0063E2E0` on `0x02CAD140` (`0x005A23B3`, `0x005A23D0`). Descriptor slot `+0x58` (`0x0063FC60`)
steps back 8 bytes to call the object's own destructor.

### The type tree and the namespace

`0x006388C0` registers a descriptor in the global type tree whose header is `0x01F2E780` (returned by
`0x00637440`). It hashes the name `+0x30` from `0x7B5`, multiplying by 33 and adding the low five bits of each
byte (`0x00638920`-`0x0063892A`) and stores the hash at `+0x20` and the name at `+0x28` (`0x00638976`, `0x0063897C`).
`0x006314B0` then links `+0x08` into the ordered tree at the end of its walk (`0x00631589`-`0x0063159F`), `0x0067F700`
rebalances the tree (`0x00638998`), and `0x006388C0` returns true.

It returns false when the name is already present (`0x006311D0` finds it, `0x0063894A`); when the name `+0x30` is
null, before the tree is touched (`0x006388D4`-`0x006388E2`); and when `0x006314B0` returns non-zero, after `+0x20` and
`+0x28` are written (`0x0063898A`).

The lookup `0x006311D0` orders by hash first and compares the full string on equal hashes, so case-only
differences collide in the hash but never match.

`0x00638F00` takes a descriptor out of the tree again, erasing its node at `+0x08` (the header
is set up first when it was not); the `PClassDescriptorDynamic` destructor `0x00633590` calls it for a
descriptor with a name.

A namespace is a separate structure: the default one is `0x01F2E330` (returned by `0x006373D0`), its
classes hang off `+0x10`, and child namespaces off `+0x28`. `0x0063BA10` searches a namespace's own
classes, then each child namespace, with an exact byte comparison.

`0x0063BA10(namespace, name)` returns 0 for a null name (`0x0063BA2D`) and reads the namespace without a null test
(`0x0063BA33`). It walks the class list through each descriptor's `+0x50` node, skips a class without a name `+0x30`,
and returns the first descriptor whose name matches. It then calls itself on each child namespace in turn
(`0x0063BAAA`), so the search reaches every namespace below, and returns the first hit, or 0.

### Type references by name

A type object's `+0x40` and `+0x48` hold two hooks that are null in most types. The type of `PType`
(`0x01F2E370`, set up by `0x00637720`) and the descriptor of `PClassDescriptor` (`0x02CF8470`, set up by
`0x00634830`) fill them, so a pointer to a type is written and read as the type's name:

- `+0x40` gives the name and its length with the terminator. The class-descriptor form `0x00637320`
  returns `0x14` for a dynamic class (bit `0x1`); the `PType` form is `0x00637350`.
- `+0x48` resolves a name. `0x00638A50` (`PType`) and `0x006389C0` (`PClassDescriptor`) hash it as
  `0x006388C0` does, search the type tree with `0x006311D0`, store the type found and return `0x13` when
  no type has that name.

The loader reaches `+0x48` through `0x0063DC30`, which returns `0x15` when the hook is null.

The set-up `0x00634830` first runs `0x006388C0` on the descriptor `0x02CF8470` and stores the two hooks. Once, under
the guard `0x02CF9070`, it asks `0x005A7A40(0x02CF8470, 0x00D58488)` for the method `isTypeOf`; when that answers
null it links the node `0x01F2DFB0` at the tail `0x02CF8508` of the descriptor's method list `0x02CF8500`
(`+0x90`); either way it registers the exit routine `0x008AF510` with `0x00808B90` (`0x00634844`-`0x006348F6`).

It then fills that node's caller, on every call: the caller object's address `0x01F2DFE0` at the node's
`+0x28` (`0x01F2DFD8`), the vtable `0x00D59010` at `0x01F2DFE0`, and at `0x01F2DFE8` the member-function pointer
`0x0063CB60` with a 0 adjustment in the dword `0x01F2DFF0`. It calls `0x00639160(the qword
0x02CF84E0, 0x02CF8470)` and sets bit `0x40000000` of `0x02CF856C`. With bit `0x1` of that dword set it points
`0x02CF8478`, `0x02CF8480` and `0x02CF8488` at `0x02CF8478`, clears the dword `0x02CF8490` and the qword
`0x02CF8498` and ends in a jump to `0x006388C0(0x02CF8470)` (`0x006348FB`-`0x0063499A`).

The `PType` name hook `0x00637350` first calls slot `+0x08` of the type; when that returns an object whose byte
`+0xFC` has bit `0x1` set, the hook answers `0x12` and stores nothing (`0x0063736B`-`0x0063737C`).

`0x0063DC90` installs such a pair. The `PAssetReferenceImport` descriptor `0x02D3E780` (registered by
`0x00675DA0`) gets `0x00676F50` and `0x00677470`, which store a reference as a byte-swapped 16-bit index into
the cluster's list of `0x18`-byte import records instead of a name. Reading one, `0x00677470` chains
the pointer into the import record's list at `+0x10`; both return 7 when the cluster has no import
list.

A `PNamedSemanticDescriptor` (built by `0x006B6820`) uses the same two hooks for a registry of named
objects. `PRenderDataType` (`0x00661A70`) resolves names with `0x0066F580` over the list `0x02D38DB8`,
which `0x0066F4F0` fills, and `PModifier` (`0x006D5810`) with `0x006D5AF0` over `0x02E9FD60`; both return
`0x13` when no entry has the name.

### Member records

`0x00632960(record, descriptor, type, name, offset, attrs, flag, context)` builds a
`Phyre::PClassDataMember`. `0x00632FB0` fills its list node, owner and name, and copies the name into
new storage when attribute bit `0x1` is set. The constructor stores the type at `+0x30` and the
offset at `+0x48`, sets attribute bit `0x2` for the duration of the call when `flag` is 2, and calls
descriptor slot `+0x40`.

`0x00632FB0(node, owner, name, attrs)` is given the record's node `+0x08` by `0x00632960` (`0x00632987`). It points both
links of the node at itself and stores the owner at node `+0x10`, the name at node `+0x18` and the attribute word at
node `+0x20` (`0x00632FBA`-`0x00632FCF`). With bit `0x1` it allocates `strlen(name) + 1` bytes through `0x0017D260`
(`0x00633005`), copies the name and its terminator there with `memcpy` (`0x0063301C`) and stores the copy at node
`+0x18`, or 0 when the allocation fails (`0x00633026`). It returns the node (`0x0063302F`).

The constructor also installs its vtable `0x00D580B0`, empties the annotation list at `+0x38` and clears the helper
`+0x50`. It hands the slot the record and `context`, restores the attribute word afterwards and returns the record
whatever the slot answers, so a member the slot refuses stays built but unlinked (`0x006329DD`-`0x006329F4`).

Slot `+0x40` is `0x0062EFD0` in the base, Abstract, Concrete and ForType vtables. It refuses the member with 5 when
`offset − [+0xF4] + width + [+0xF8]` exceeds the instance size, with `0x15` when it has no name and
with `0x12` when `0x00597220` finds the name in the class or any ancestor; otherwise it appends the
member to the list at `+0x80` and returns 0. Slot `+0x48` (`0x0062F080`) unlinks it again.

The width comes from `0x0063C0C0(record, context)`: the context's pointer width (its slot `+0x08`; 8 with no context)
when attribute bit `0x2` is set, or when the member is a dynamic array (kind 2) without bit `0x40`
(`0x0063C128`-`0x0063C137`, `0x0063C172`-`0x0063C187`). Otherwise it is the type's size at `+0x38`, or, with a context,
the size the context's slot `+0x10` gives the class that the type's own slot `+0x08` returns
(`0x0063C0E4`-`0x0063C0F9`): a class descriptor returns itself there (`0x0016D680`), a `PType` returns 0 (`0x005C5230`)
and keeps the size `+0x38`.

### Member kinds

| Route | Record | Adds |
|---|---|---|
| `0x00632960` | `PClassDataMember` | the plain member |
| `0x00632A10` | `PClassDataMemberArray` | kind at `+0x5C` (2 a counted buffer such as `PArray<T>::m_els`, 3 a `PArray` member, 4 a `PSharray` member), the element type's alignment at `+0x58` (4 for `PMatrix4`, a 0x40-byte element, at `0x005ED448`; 2 for `PSkinBoneRemap`, two `u16`, at `0x0066A0A7`) |
| `0x00632A70` | `PClassDataMemberArrayFixedSize` | kind 1 at `+0x5C`, the type's `+0x3C` at `+0x58`, element count at `+0x60` |
| `0x00632BE0` | `PClassDataMemberEnum` | attribute bit `0x20`, a value at `+0x58` |

The array, fixed-size and enum routes differ at attach time. `0x00632A10` forwards to `0x00632960` with its array kind
as `flag` and context 0 (`0x00632A28`-`0x00632A41`), so a kind-2 member is checked against the instance size as
pointer-wide; it then stores the kind and the alignment and installs its vtable `0x00D58100`. `0x00632A70` and
`0x00632BE0` build the record inline as `0x00632960` would, without the `flag` test, and give the attach slot context 0
(`0x00632AE9`, `0x00632C54`); `0x00632BE0` ORs `0x20` into the word `0x00632FB0` stores (`0x00632C15`).

`0x00632A70` attaches before it stores the kind, the count and its vtable `0x00D58160` (`0x00632AF2`-`0x00632B0C`), so the
bound check of `0x0062EFD0` measures one element; `0x00632BE0` installs its vtable `0x00D580D8` and the value after the
attach. All three return the record whatever the slot answers. Slot `+0x08` of the two array vtables (`0x0016D680`)
returns the record, and that of the plain, enum and dynamic vtables (`0x005C5230`) returns 0; `0x0059D2D0`, `0x00599390`
and `0x0063C0C0` read the array kind through it.

A registering function can OR further attribute bits into the record after the call (bit `0x10`,
`0x08` or `0x40`; `0x00633100` adds `0x4` when it attaches a dynamic-type helper at `+0x50`). The
attribute word is what the loader compares against a file's member record. `0x0063BBA0` returns a
member's type: the helper's answer (its slot `+0x08`) when a helper is attached, else `+0x30`.

### Methods and script functions

The same record base built by `0x00632FB0` is linked into two further lists: `+0x90` holds the class's
callable methods (`0x005AD8F0` links `playOnce` after the duplicate check `0x005A7A40`) and `+0xA0` the
functions published to the script layer (`0x005B2860` links `GetGlobalTime` after `0x005A0470`).

### Annotations

A member's list at `+0x38` holds annotations. `0x006B66C0(annotation, key, type, value)` builds a
`0x30`-byte `Phyre::PAnnotation`, and `0x006B67D0` links it to a member. All 69 static annotations in
the executable are a `PAnnotationWithValue<unsigned int>` keyed by `0x02CF8570`, the key `0x001641C0`
names `WriteMask`, with the value `0x7FFFFFFF`, on the `m_count` member of a `PArray<T>` or
`PSharray<T>` descriptor.

`0x006B66C0(annotation, key, type, value)` points the two links of the node at `+0x08` at the node,
installs the vtable `0x00D80930` at `+0x00`, stores the key at `+0x18`, the type at `+0x20` and the value
dword at `+0x28`, and returns the annotation (`0x006B66C0`-`0x006B66E0`).

`0x006B67D0(list head, annotation)` puts the annotation's node `+0x08` at the front of the list: the
node's next is the old first, its previous is the head, and the head and the old first then point at the
node (`0x006B67D0`-`0x006B67E1`).

`0x006B67F0(list, key)` finds an annotation by key: it walks the annotation list it is given from its first node and
returns the first annotation whose key `+0x18` is the given pointer, or 0 at the end of the list
(`0x006B67F0`-`0x006B681D`).

### Default instance and masks

Each class registers three static buffers of its instance size: the default instance at `+0xC0`
(`0x0063DC80`), and two masks at `+0xC8` (`0x0063DF90`) and `+0xD0` (`0x0063DFA0`). They are built on first
use, when `+0xFC` bit `0x80000000` is clear:

1. `0x00639A60` fills `+0xC0` and `+0xC8` with `0xA5` and constructs the class into `+0xC8` through
   slot `+0x50`. Unless bit `0x8` is set it constructs again into `+0xC0` and logs a
   "position dependant constructor" message when the two differ. It copies `+0xC8` into `+0xC0`,
   copies the default instances of inline object members with bit `0x40` or kind 4, and sets bit
   `0x80000000`.
2. A class whose slot `+0x50` has no constructor is built by `0x0063CB80` instead, from its parent's
   and its members' default instances.
3. In `0x00639A60` the paths in full: it returns at once when `+0xC0` or `+0xC8` is null or bit `0x80000000` is
   already set (`0x00639A73`, `0x00639A83`, `0x00639A96`). A dynamic class (bit `0x1`) goes to `0x0063CB80`, given
   `0x00639A60`'s own second argument, and to nothing else before bit `0x80000000` is set (`0x00639AB6`-`0x00639AC3`).
4. Every other class gets the two `0xA5` fills (`memset`, `0x00639AD8`, `0x00639AEC`). An abstract class (bit `0x2`)
   stops there and only has bit `0x80000000` set (`0x00639AF1`). The rest are constructed into `[+0xC8]` through
   slot `+0x50` (`0x00639B20`); when the slot answers 0, `0x0063CB80(descriptor, 0)` builds the class (`0x00639BA4`).
5. When the slot constructs and bit `0x8` is clear, the second construction into `[+0xC0]` (`0x00639B3E`) is
   compared with `memcmp`, the message goes to channel 1 (`0x00639B52`-`0x00639B6A`), and that second object is
   destroyed through slot `+0x58` at `[+0xC0] + [+0xF8]` (`0x00639B78`). After the copy (`memcpy`, `0x00639B8C`)
   the object in `+0xC8` is destroyed through slot `+0x58` at `[+0xC8] + [+0xF8]` (`0x00639B9A`).
6. On both construction paths it walks its own list `+0x80` (`0x00639BA9`-`0x00639C44`). A member is copied when its
   type is a class (the type's slot `+0x08` answers a descriptor), attribute bit `0x2` is clear and bit `0x40` is
   set or the kind is 4: the member class's default instance (`0x0063BB10`) goes to
   `[+0xC0] + [+0xF8] + offset - [owner+0xF4]` with its size `+0x38` (`0x00639C2D`). Bit `0x80000000` is set at
   `0x00639C55`.
7. `0x0063CB80(descriptor, context)` first copies the parent's default instance (`0x0063BB10`) to
   `[+0xC0] + [+0xF8] - [parent+0xF8]`: the parent's size `+0x38`, or the context's slot `+0x10` answer when that
   is smaller, and only when the parent has a default instance and `size <= [+0x38]` of the class itself
   (`0x0063CBAA`-`0x0063CBF8`).
8. It then walks its own list `+0x80`. It skips a member with attribute bit `0x2`, a dynamic array (kind 2)
   without bit `0x40` and a member whose type is not a class (`0x0063CC55`-`0x0063CC7A`).
9. Each other member gets the default instance of its class (`0x0063BB10`) at
   `[+0xC0] + [+0xF8] + offset - [owner+0xF4] - [type+0xF8] + [type+0xF4]`, once, or `[+0x60]` times one after
   another for a fixed array (kind 1), each copy the width `0x0063C0C0` gives (`0x0063CCA8`-`0x0063CCE5`).
10. `0x00639C80` fills `+0xC8` with `0xFF` and `+0xD0` with zero, copies the parent's masks, then
   clears every byte a member covers in `+0xC8`, logging an overlap when a byte is already clear.
   For a primitive member it writes the member's `WriteMask` into `+0xD0`, or `0xFF` bytes without
   one; for an inline object it copies that class's masks. It sets bit `0x10000000` when no byte of
   `+0xC8` is left set.

So `+0xC8` marks the bytes no member describes and `+0xD0` the bits that belong to member values.
`0x0063C5E0` and `0x0063C1A0` build a class's buffers when needed and return its `+0xD0` and `+0xC8`;
`0x00639C80` uses them for the
masks of inline object members.

`0x0063BB10` returns the qword `+0xC0` at once when bit `0x80000000` of the flags `+0xFC` is set. Otherwise it
calls the descriptor's slot `+0x60` when bit `0x40000000` is clear, then `0x00639A60(class, 0)` and
`0x00639C80(class, 0)`, and returns `+0xC0` (`0x0063BB16`-`0x0063BB50`).

`0x0063BC00` returns the qword `+0xD8` when it is not null. Otherwise it builds the buffers the same way when
bit `0x80000000` is clear; with a default instance at `+0xC0` it sets bit `0x20000000` and returns that
instance plus the signed dword `+0xF8`; with no default instance it returns the null `+0xD8`
(`0x0063BC06`-`0x0063BC63`).

### Creating instances

`0x0063A990(cluster, count, descriptor, …)` is `PCluster::create`. A class with `+0xFC` bit `0x8`
logs "has no default constructor and cannot be allocated" and gets nothing (`0x0063A99A`-`0x0063A9BE`); a count of
0 gets 0 (`0x0063A9CD`). Otherwise `0x00639510`
refuses an abstract class (bit `0x2`) and allocates `count × [+0x38]` bytes with alignment `[+0x3C]`,
and `0x0063C910` initialises each instance in turn: it builds the buffers if needed, then copies the
whole default instance over it.

Without a default instance it constructs through slot `+0x50` and
copies the default instance of every inline object member, across the class and its ancestors. `0x0063A990` hands
its fourth argument to `0x00639510` as extra bytes (`0x0063A9D6`), steps from the list's `+0x58` by `[+0x38]` per
object (`0x0063AA10`-`0x0063AA22`) and returns the first object, or 0 when `0x00639510` returns no list (`0x0063A9E9`).

`0x0063C910(descriptor, object)` returns the object. When bit `0x80000000` is clear it first calls slot `+0x60`,
the member registration, if bit `0x40000000` is clear, then builds the buffers (`0x00639A60`, `0x00639C80`, each
given 0) (`0x0063C93D`-`0x0063C95C`). With a default instance it copies `[+0x38]` bytes from `+0xC0` to
`object - [+0xF8]` (`0x0063C961`-`0x0063C974`). Without one it constructs at `object - [+0xF8]` through slot `+0x50`
and returns 0 when the slot answers 0 (`0x0063C990`-`0x0063C995`, `0x0063CB40`).

After a construction it walks the list `+0x80` of the class and then of each ancestor `+0x78`
(`0x0063C9C0`-`0x0063CB14`). It takes each member whose type is a class (the type's slot `+0x08` answers a
descriptor), without attribute bit `0x2` and not a dynamic array (kind 2): one element, or `[+0x60]` elements for
a fixed array (kind 1) (`0x0063CA28`-`0x0063CA4C`). The first element is at
`object + offset - [owner+0xF4] + [type+0xF4]`, the next ones `[type+0x38]` apart.

For each element, unless the class that owns the list is dynamic (bit `0x1`), it first destroys the element
through the type's slot `+0x58` (`0x0063CA84`). It then builds the type's buffers when needed and copies
`[type+0x38]` bytes of the type's `+0xC0` to `element - [type+0xF8]` (`0x0063CAD2`).

`0x00639510(cluster, bytes, count, descriptor, extra)` returns the new instance list, or 0:

1. A byte size or count of 0 gets 0 (`0x0063953B`, `0x00639543`).
2. An abstract class logs "is abstract and an instance list cannot be allocated" on channel 1 and gets 0
   (`0x0063954C`-`0x0063956B`).
3. When `bytes < count * [+0x38]` it logs "Trying to allocate list of %d '%s' instances in %d bytes when %d bytes
   are required" on channel 1 and gets 0 (`0x00639570`-`0x00639599`).
4. It takes a list record from the cluster's pool at `+0x50` (`0x006394B0`, `0x006395A2`) and gets 0 when the pool
   is out of records (`0x006395B2`). It grows the size to `bytes + extra` (`0x006395B4`) and sets the record up for the
   descriptor and the cluster (`0x00633120`, `0x006395C6`).
5. It takes the bytes at alignment `[+0x3C]` from the cluster's block at `+0x48` when they fit (`0x00639750`,
   `0x006395D7`), and `0x00639780` sets the list up on them (`0x006395E8`).
6. `0x00639780` allocates the bytes through `0x0017D260` when the block returned 0 (`0x006397DA`-`0x006397E0`), runs
   `0x0063B3E0` on the list (`0x006397F0`), and stores the storage at `+0x60`, the first
   object `[+0x60] + [descriptor+0xF8]` at `+0x58`, the count at `+0x70` and `+0x74`, the owned flag `+0x7C` and
   `bytes - count * [+0x38]` at `+0x78` (`0x006397FC`-`0x00639824`).
7. `0x00639780` refuses a count above 1 for a class with bit `0x4` (`0x006397BA`-`0x006397C7`) and a failed
   allocation (`0x006397EB`); the record then goes back to the pool (`0x00631180`, `0x00639625`) and the result is 0.
8. Otherwise it sets the loaded byte `+0x7D` (`0x006395F1`), appends the list to the cluster's list `+0x38`
   (`0x006395F5`-`0x00639607`), enters it in the world's per-type table through `0x00639320` when the cluster has a
   world `+0x78` (`0x0063960B`-`0x00639617`), and returns the list.

The record set-up `0x00633120(record, descriptor, cluster)` points the record's two links `+0x00` and `+0x08` at
itself, calls `0x0067FFB0(record + 0x10, the descriptor's size +0x38, 0, its alignment +0x3C, its name +0x30)`,
points the two links at `+0x38` and `+0x40` at `+0x38`, stores the cluster at `+0x48` and the descriptor
at `+0x50`, clears the qwords `+0x58` to `+0x70` and the dword `+0x78`, stores `0x101` in the word `+0x7C`
and returns the record (`0x0063312F`-`0x0063318B`).

`0x00639780(record, count, bytes, storage)` itself answers 0 when `count * [descriptor+0x38] > bytes`
(`0x006397A9`-`0x006397B8`), and 1 on success (`0x00639822`). It allocates only when bytes is not 0 and no storage
is given, and the owned flag `+0x7C` is 1 when no storage was given (`0x006397D0`-`0x0063981F`).

`0x00631180(pool, record)` calls `0x0063B3E0(record)` and `0x00680030(record + 0x10)` and ends in a jump to
`0x00680200(pool, record)` (`0x0063119D`-`0x006311BC`).

### The cluster's script methods

`0x00635470` publishes four `PCluster` methods on the cluster descriptor `0x02CF8780`:

- `create` (`0x0063AA50`) makes one object: it logs the same "no default constructor" message for bit
  `0x8`, and otherwise builds a one-object instance list through `0x00639510`, initialises the object
  at the list's `+0x58` with `0x0063C910` and returns the object with its descriptor.
- `deleteObject` is `0x0063AD20`: it answers 1 for a null object and otherwise jumps to `0x0063ABF0` with its
  arguments unchanged (`0x0063AD20`-`0x0063AD29`).
- `deleteInstancesOfType` (`0x0063AAD0`) removes every instance list of exactly one class: it unlinks
  the list, takes it off the per-type table, destroys its objects (`0x0063B3E0`), frees its blocks
  (`0x00680030`) and returns the list record to the cluster's pool at `+0x50` (`0x00680200`).
- `absorb` (`0x00638FB0`) moves every list of another cluster into this one (see below).

Each method is a `0x28`-byte node (`0x01F2E140`, `0x01F2E190`, `0x01F2E1E0`, `0x01F2E230`) built behind its own guard and
appended to the descriptor's method list, whose anchor is `0x02CF8810`, the descriptor's `+0x90`, and whose tail word is
`0x02CF8818`. Each append reads the tail, links the node after it and stores the node as the new tail (`0x006354EE`,
`0x0063550D`; `0x0063559E`, `0x006355BD`; `0x0063564C`, `0x0063566B`; `0x006356FA`, `0x00635719`). The teardowns `0x008AF2B0`,
`0x008AF370`, `0x008AF310` and `0x008AF220` unlink the nodes at exit.

Each of the four stores the node's previous link in `[next + 8]` and its next link in `[previous]`, then
points the node's two qwords at the node itself: `0x008AF220` for the node `0x01F2E230` (`0x008AF22D`-`0x008AF250`),
`0x008AF2B0` for `0x01F2E140` (`0x008AF2BD`-`0x008AF2E0`), `0x008AF310` for `0x01F2E1E0` (`0x008AF31D`-`0x008AF340`) and
`0x008AF370` for `0x01F2E190` (`0x008AF37D`-`0x008AF3A0`).

Each also frees the node's name, copied into owned storage, through `0x00584730` when bit `0x1` of its
attribute word `+0x20` is set: `0x008AF220` the pointer the qword `0x01F2E248` (`+0x18`) holds, under the byte
`0x01F2E250`; `0x008AF2B0` `0x01F2E158` under `0x01F2E160`; `0x008AF310` `0x01F2E1F8` under `0x01F2E200`; and `0x008AF370`
`0x01F2E1A8` under `0x01F2E1B0` (`0x008AF257`-`0x008AF267`, `0x008AF2E7`-`0x008AF2F7`, `0x008AF347`-`0x008AF357`,
`0x008AF3A7`-`0x008AF3B7`).

`0x008AF490` walks the whole class list from the qword `0x01F2E340` at exit, each class being its node less
`0x50` and the next node read from the class's `+0x50` before the class is used, and calls vtable slot
`+0x38` with 1 on every class whose byte `+0xFC` has bit `0x1` set (`0x008AF49A`-`0x008AF4ED`).

A cluster's `+0x78` points at the world it belongs to, whose per-type table (count `+0x10`, entries
`+0x18`) holds `0x20`-byte entries indexed by each descriptor's
`+0xEC`. An entry heads the lists of its class and counts their objects at `+0x10` and the lists at
`+0x14`. A list is linked under its own class's entry and counted in every ancestor's.

`0x00638FB0` first merges the other cluster's pool of list records into this one (`0x00680080`, which
returns 5 when the two pools' record sizes differ). Each list then leaves the per-type table of the other cluster's world
and that cluster's list, joins the end of this cluster's list and its world's table, takes this cluster at its `+0x48` and is
passed to `0x00677550`, which, for a list of a class derived from `PAssetReference` (`0x02D3E680`),
sets every object's `+0x48` to that cluster. The other cluster's chain at `+0x48` is moved over last.

`0x0063D6B0(world, cluster)` takes a cluster whose `+0x78` is that world off it: it unlinks the
cluster's node at `+0x88`, clears `+0x78` and removes each of its lists from the per-type table.

`0x0063B3E0` calls descriptor slot `+0x58` on every object of a loaded list (`+0x7D`) except the slots
on the chain at `+0x10`, frees the storage when the list owns it (`+0x7C`) and zeroes the count.

### Member visits

Descriptor slot `+0x00` walks the members of a class and its ancestors (`0x0063E2E0`) and hands each
to `0x0063CE80`, which applies the member type's own slot `+0x00` to every element through `0x0059FDB0`.
The flag argument picks the order: non-zero walks each `+0x80` list forwards, zero backwards, and the
flag is passed on to the member types. A type's slot `+0x00` is the step applied to one element; for
`PQWord` (`PTypeDefault<PQWord>`, `0x0063E170`) it reverses the value's sixteen bytes in place (`0x00637E10`)
and returns 1.

Eight core classes carry the walk inlined for their own descriptor, one copy per order, and their
slot `+0x00` adapters only choose between the two copies and return 1:

| Class | Descriptor | Slot `+0x00` | Forward | Backward | Object offset |
|---|---|---|---|---|---|
| `PClassDataMemberDynamic` | `0x02CF8370` | `0x0062F3E0` | `0x00630640` | `0x00630C80` | `+0x08` |
| `PClassDescriptor` | `0x02CF8470` | `0x0062F0C0` | `0x006306E0` | `0x00630D20` | `+0x30` |
| `PClassMember` | `0x02CF8680` | `0x0062F960` | `0x00630820` | `0x00630E60` | 0 |
| `PCluster` | `0x02CF8780` | `0x0062F200` | `0x006308C0` | `0x00630F00` | 0 |
| `PClusterDependencyList` | `0x02CF8880` | `0x0062EE00` | `0x00630960` | `0x00630FA0` | 0 |
| `PNamespace` | `0x02CF8980` | `0x0062F5A0` | `0x00630A00` | `0x00631040` | `+0x10` |
| `PWorld` | `0x02CF8A80` | `0x0062F740` | `0x00630AA0` | `0x006310E0` | 0 |
| `PSharray<PString>` | from `0x00635DC0` | `0x0063DFB0` | `0x00630500` | `0x00630B40` | 0 |

The object offset is added to the object pointer before the walk, as the class's reflected layout
starts that far into the object.

### Teardown

The `atexit` thunk `0x008A8E20` puts back the `PClassDescriptorForType` vtable `0x00D29A38` and jumps to
`0x00633390`, the base destructor:

1. It installs the `PClassDescriptor` vtable and, when its index at `+0xE8` is the last one handed
   out, decrements `0x02CF8260`.
2. `0x0063D640` unlinks `+0x50` from its namespace and unlinks an emptied non-default namespace.
   Called as `0x0063D640(namespace, descriptor)` (`0x006333E0`), it points the unlinked node `+0x50` at itself
   (`0x0063D646`-`0x0063D665`).
3. The namespace counts as emptied when its class list `+0x10` is now empty; when it is also not the default
   namespace (`0x006373D0`), `0x0063D640` unlinks the namespace's own node `+0x00`, the node `0x00639160` links into
   the default namespace's child list `+0x28`, and points it at itself (`0x0063D67E`-`0x0063D6A3`). Only the class
   list is tested, not the child namespaces `+0x28`.
4. It frees the records of `+0x90` and `+0xA0` whose attribute bit `0x1` is set, with their name,
   then unlinks every remaining node of `+0x80`, `+0x90`, `+0xA0` and `+0xB0` without freeing it.
5. `0x006B6700` unlinks every node of `+0x60`, and the `PType` vtable is installed last.

A member's teardown `0x00633240` installs the `PClassDataMember` vtable `0x00D580B0` (`0x0063325E`), detaches the
member through its owner's slot `+0x48` when its node `+0x08` is linked (`0x00633265`-`0x00633274`), drains its
annotations `+0x38` (`0x006B6700`, `0x0063327C`) and, with attribute bit `0x1`, frees the copied name `+0x20`
(`0x00584730`, `0x00633282`-`0x0063328C`).

The deleting destructors such as `0x005847E0` install their own vtable (`0x00D24540` in `0x005847E0`, `0x00584800`),
call `0x00633390` and, when flag bit `0x1` is set, free the object with `_aligned_free` (`0x00584730`); with bit
`0x4` as well they call the empty `0x0016D6A0` and free nothing (in `0x005847E0` with the size `0x100`,
`0x00584820`-`0x00584828`). Either way they return the object (`0x0058482E`).

## Layouts

PType (base of every type and descriptor):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable |  |
| `+0x08` | `void*` |  | type-tree links (three pointers, `+0x08`..+`0x1F`) |
| `+0x20` | `u32` |  | name hash, written by `0x006388C0` |
| `+0x28` | `void*` |  | name, as the tree key |
| `+0x30` | `void*` | name |  |
| `+0x38` | `u32` |  | instance size |
| `+0x3C` | `u32` | alignment |  |
| `+0x40` | `void*` |  | name-writer hook, or null (`0x00637320`, `0x00637350`) |
| `+0x48` | `void*` |  | name-resolver hook, or null (`0x006389C0`, `0x00638A50`) |

Every list in these records is a circular doubly linked list of 16-byte nodes: a list is empty when its
node points at itself, and a member sits in a list through a node inside it (`0x006B6700` drains one,
taking each member at its node minus 8).

`ListNode` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | next | the next node, or this node when the list is empty |
| `+0x08` | `void*` | prev | the previous node |

PClassDescriptor (`0x100`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x50` | `ListNode` |  | node in the namespace's class list |
| `+0x60` | `ListNode` |  | drained by `0x006B6700` at teardown |
| `+0x70` | `void*` | namespace |  |
| `+0x78` | `void*` |  | parent descriptor, or null |
| `+0x80` | `ListNode` |  | data members |
| `+0x90` | `ListNode` | methods |  |
| `+0xA0` | `ListNode` |  | script functions |
| `+0xB0` | `ListNode` |  | fourth list, emptied by the constructor and the destructor |
| `+0xC0` | `void*` |  | default instance |
| `+0xC8` | `void*` |  | undescribed-byte mask |
| `+0xD0` | `void*` |  | write mask |
| `+0xD8` | `void*` |  | 0 (zeroed by the constructor) |
| `+0xE0` | `void*` |  | 0 (zeroed by the constructor) |
| `+0xE8` | `u32` |  | registration index (`0x02CF8260`) |
| `+0xEC` | `u32` |  | value `0xFFFFFFFF` |
| `+0xF0` | `i32` |  | this class's adjustment |
| `+0xF4` | `i32` |  | sum of adjustments to the root |
| `+0xF8` | `i32` |  | layout base of an instance |
| `+0xFC` | `u32` | flags |  |

A list is a `{next, prev}` pair that points at itself when empty; a node sits 8 bytes into its
record, and an owned node has bit `0x1` at node `+0x20`.

```
+0xFC flags
0x00000001  dynamic class (built by 0x00632E80)
0x00000002  abstract: no instance list (0x00639510)
0x00000004  set by four initialisers: PParameterBuffer's (0x001615C0) and the three header descriptors'
            (0x001605C0, 0x00167DB0, 0x001688F0); the PCluster loaders test it per class
0x00000008  no default constructor: PCluster::create refuses it
0x00000010  set for the three header descriptors right after 0x006388C0 registers them (0x005B0700,
            0x006D1810, 0x006D9FC0); 0x0059D940 extracts it
0x00000020  set by a class's registrar or wrapper getter before 0x00639450 registers the members; never read
0x00000040-0x04000000  no instruction writes or reads them
0x08000000  a member is a PSharray, or the parent has the bit
0x10000000  every instance byte is described by a member
0x20000000  set by 0x0063BC00, never tested
0x40000000  members registered (0x00639450)
0x80000000  default instance and masks built
```

PClassDescriptorDynamic (`0x140`), beyond the base:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x100` | `u16` |  | pair compared by `0x0063D550` to skip a rebuild |
| `+0x104` | `u32` |  | parent's instance size |
| `+0x108` | `…` |  | three {u32, ptr} pairs at `+0x108`, `+0x118`, `+0x128`, zeroed by `0x00632E80` |
| `+0x138` | `void*` |  | tagged name; `+0x30` holds it with bit `0x1` cleared |

PClassDataMember (`0x58`; arrays to `+0x64`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable |  |
| `+0x08` | `ListNode` |  | node in the owner's `+0x80` list |
| `+0x18` | `void*` |  | owning descriptor |
| `+0x20` | `void*` | name |  |
| `+0x28` | `u32` |  | attribute word |
| `+0x30` | `void*` |  | type (a PType or a class descriptor) |
| `+0x38` | `ListNode` | annotations |  |
| `+0x48` | `u32` |  | offset in the owner's layout |
| `+0x50` | `void*` |  | dynamic-type helper, or null |
| `+0x58` | `u32` |  | element alignment (arrays) |
| `+0x5C` | `u32` |  | array kind |
| `+0x60` | `u32` |  | element count (fixed arrays) |

PAnnotation (`0x30`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable |  |
| `+0x08` | `ListNode` |  | node in a member's `+0x38` list |
| `+0x18` | `void*` |  | key (`0x02CF8570` for WriteMask) |
| `+0x20` | `void*` |  | value type |
| `+0x28` | `u32` |  | fourth constructor argument |
| `+0x30` | `u32` |  | value (PAnnotationWithValue&lt;unsigned int&gt;) |

```
attribute word (member +0x28)
0x01  name copied into owned storage; freed at teardown
0x02  stored as a pointer
0x04  dynamic-type helper attached (0x00633100)
0x08, 0x10  set per class by the registering function
0x20  enum member (0x00632BE0)
0x40  a kind-2 array measured and defaulted inline, not as a pointer (PSharray<T>::m_u)
```

Descriptor vtable slots (PClassDescriptorConcrete&lt;PAnimatableComponent&gt;, `0x00D29E90`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` |  | visit every member of the class and its ancestors (`0x0063E2E0`) |
| `+0x18` | `...` |  | get the value from a script context |
| `+0x20` | `...` |  | put the value into a script context |
| `+0x38` | `...` |  | scalar deleting destructor |
| `+0x40` | `...` |  | attach a member (`0x0062EFD0`) |
| `+0x48` | `...` |  | detach a member (`0x0062F080`) |
| `+0x50` | `...` |  | construct in place; returns false for a class without one (`0x00657140`) |
| `+0x58` | `...` |  | destruct in place (`0x0063FC60`) |
| `+0x60` | `...` |  | register the members (_purecall in ForType&lt;T&gt;) |
| `+0x68` | `...` |  | push the object's held objects of a named class to a script and count them; -1 by default (`0x00660570`) |

One class overrides slot `+0x68`: `PEntity` (`0x006AB3F0`, which reorders the arguments for `0x006AB540`). It looks the
name up in the namespace (`0x0063BA10`), returns -1 unless that class is `PComponent` or derives from it, and
otherwise pushes every component of the entity whose class is that class or derives from it (`0x00684090`)
and returns how many it pushed.
`0x00684090` loads the qword `+0x10` of its second argument as the third argument and jumps to `0x00682D20`
(`0x00684090`-`0x00684094`).

For a `PMatrix4x3` the wrapper's slot `+0x20` (`0x006B3A90` to `0x006B3610`) builds a 64-byte matrix from the
twelve floats, as (`+0xC`, `+0x1C`, `+0x2C`, 0), (`+0`, `+4`, `+8`, 0), (`+0x10`, `+0x14`, `+0x18`, 0) and
(`+0x20`, `+0x24`, `+0x28`, 1.0 from `0x01CEBBA8`), and pushes it as a script `Matrix` (`0x00684130`).

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

The placement constructors named in the fences each skip a null block and answer 1. Fifteen of the eighteen
also make stores that the fences do not list, and so does `0x005A1510`, the placement constructor of
`PBlendableAnimationSource` (slot `+0x50` of its vtable `0x00D288E0`):

- `0x005A1510` stores 1.0 in the dwords `+0x08` and `+0x0C` and in the low dword of the qword `+0x50` (high dword
  0), the vtables `0x00D313B0`, `0x00D313E0` and `0x00D314E0` at `+0x10`, `+0x38` and `+0x58`, and 0 in the qwords
  `+0x00`, `+0x20`, `+0x28`, `+0x48`, `+0x68`, `+0x70` and `+0x78` and the dwords `+0x18`, `+0x30`, `+0x40`
  and `+0x60` (`0x005A1510`-`0x005A1577`).
- `0x005CEEF0` also clears the qword `+0x00` (`0x005CEEF7`).
- `0x005D3C60` also clears the qwords `+0x10`, `+0x20` and `+0x30` and the dwords `+0x18` and `+0x28`
  (`0x005D3C70`-`0x005D3C7E`).
- `0x005D5FE0` stores `0x01010105` in the dword `+0x00` and `0x400` in the qword `+0x18` (`0x005D5FE5`,
  `0x005D5FFF`).
- `0x005D7B60` stores the address `0x02CF7A30` in the qword `+0x00`, 2 in the dword `+0x18` and 0 in the qword
  `+0x20` (`0x005D7B65`-`0x005D7B82`).
- `0x005D7DE0` also clears the word `+0x00` (`0x005D7DE7`).
- `0x0065EC80` stores `0x334` in the word `+0x0C` (`0x0065EC8D`).
- `0x00660A20` also clears the dword `+0x08`, the qword `+0x10` and the dword `+0x18` (`0x00660A2A`-`0x00660A31`).
- `0x006611F0` also clears the dword `+0x08`, the qword `+0x10`, the dword `+0x20` and the qword `+0x28`
  (`0x006611F9`-`0x00661206`).
- `0x005D1700` stores the address `0x02CF7A30` in the qword `+0x00`, `0x300` in the word `+0x08`, 0 in the qword
  `+0x0C`, the dword `+0x14` and the qword `+0x20`, and 2 in the dword `+0x18` (`0x005D1705`-`0x005D171E`,
  `0x005D1725`).
- `0x005D27B0` stores the address `0x01F2DD80` in the qword `+0x00` and 0 in the dwords `+0x08`, `+0x18`, `+0x28`
  and `+0x38` and the qwords `+0x10`, `+0x20`, `+0x30` and `+0x40` (`0x005D27B5`-`0x005D27D9`).
- `0x0065EA30` stores -1 in the dword `+0x04`, 0 in the dword `+0x08` and the qword `+0x10`, 6 in the dword
  `+0x18`, and -1 in the qword `+0x1C` and the dword `+0x24` (`0x0065EA37`-`0x0065EA56`).
- `0x006A7B10` stores the address `0x01F31F78` in the qword `+0x00` and 1.0 in the floats `+0x24`, `+0x2C` and
  `+0x38`; it leaves 0 in the dword `+0x08`, the qwords `+0x10` and `+0x18`, the dwords `+0x20`, `+0x28`,
  `+0x30`, `+0x34` and `+0x3C`, the qword `+0x40` and the dwords `+0x48` and `+0x4C` (`0x006A7B15`-`0x006A7B5E`).
- `0x006C2960` stores -1 in the qword `+0x00` and 0 in the qwords `+0x08`, `+0x10` and `+0x18`
  (`0x006C2967`-`0x006C2976`).
- `0x006C4A60` also clears the qword `+0x00`, the dword `+0x08` and the qword `+0x10`; its qword store of
  10000.0 at `+0x1C` clears the dword `+0x20`. When the address block + `0x28` is not null it then stores 1.0
  in the float `+0x28` with 0 in the dword above it, 4 in the dword `+0x30` and 1 in the dword `+0x20`
  (`0x006C4A78`-`0x006C4AA4`).
- `0x006CFA50` also clears the qwords `+0x10`, `+0x28`, `+0x38`, `+0x40`, `+0x48` and `+0x68` and the dword
  `+0x30` (`0x006CFA5A`-`0x006CFA7C`).

Other constructors and destructors of this page's classes:

- `0x005ACFA0`, slot `+0x00` of the `PTimeIntervalController` vtable `0x00D313B0`, is that class's deleting
  destructor: it installs the base vtable `0x00D312F0`; with bit `0x1` of its second argument set and bit `0x4`
  clear it frees the object through `0x00584730`; with both set it calls the empty `0x0016D6A0` with the size
  `0x28` and frees nothing; it returns the object (`0x005ACFB2`-`0x005ACFE1`).
- `0x005DBF60` installs the vtable `0x00D498B0` at `+0x00`; `0x005DC0B0` installs `0x00D498B0` and then `0x00D498D0`,
  stores its second argument at `+0x08` and clears the dwords `+0x10` and `+0x18` and the qword `+0x20`;
  both return the object (`0x005DBF60`-`0x005DBF6A`, `0x005DC0B0`-`0x005DC0D7`).
- `0x006161A0` runs `0x005DCC40` on the object, clears the dword `+0x30` and calls `0x00627800(object + 0x30, 1)`,
  clears the qwords `+0x78`, `+0x80`, `+0x88`, `+0x90`, `+0x98` and `+0xA0`, and returns the object
  (`0x006161B6`-`0x00616205`).
- `0x006332A0` installs the vtable `0x00D580B0`; when the node at `+0x08` is linked (its first qword is not its
  own address) it calls slot `+0x48` of the owner at `+0x18` with the member; it runs `0x006B6700` on `+0x38`;
  and it frees the name at `+0x20` with `0x00584730` when bit `0x1` of the byte `+0x28` is set
  (`0x006332B7`-`0x006332EC`).

`PConstantBufferBase` (`0xC` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_size | m_size (u32), registered by `0x005E3B70` (`0x00632960` at `0x005E3BF5`); no shipped .phyre file declares PConstantBufferBase; the placement constructor `0x005CE780` clears `+0x00` to `+0x07` (`0x005CE787`) |
| `+0x04` | `u8[4]` | bytes04 | cleared with m_size by the placement constructor `0x005CE780` (`0x005CE787`); no registered member covers it (`0x005D8FC0` registers the `0xC`-byte class at `0x005D9010`) |
| `+0x09` | `u8[3]` | pad09 | the bytes after the byte the placement constructor `0x005CE780` clears at `+0x08` (`0x005CE78A`) up to the end of the `0xC`-byte class; no registered member covers it (`0x005D8FC0` registers the `0xC`-byte class at `0x005D9010`) |

`PDataBlockBase` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_stride | m_stride (u32), registered by `0x00665620` (`0x00632960` at `0x00665721`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PDataBlockBase; the placement constructor `0x00660A20` clears it with m_elementCount (`0x00660A27`) |
| `+0x04` | `u32` | m_elementCount | m_elementCount (u32), registered by `0x00665620` (`0x00632960` at `0x00665794`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PDataBlockBase; cleared with m_stride by the placement constructor `0x00660A20` (`0x00660A27`) |
| `+0x1E` | `u8[2]` | pad1E | the bytes after the word the placement constructor `0x00660A20` sets to `0x300` at `+0x1C` (`0x00660A34`) up to the end of the `0x20`-byte class; no registered member covers it (`0x00661BD0` registers the `0x20`-byte class at `0x00661C20`) |

`PIndexDataBlockBase` (`0x14` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_minimumIndex | m_minimumIndex (u32), registered by `0x006660D0` (`0x00632960` at `0x006662B7`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PIndexDataBlockBase; the placement constructor `0x0065EC80` clears it with m_maximumIndex (`0x0065EC87`) |
| `+0x04` | `u32` | m_maximumIndex | m_maximumIndex (u32), registered by `0x006660D0` (`0x00632960` at `0x0066632A`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PIndexDataBlockBase; cleared with m_minimumIndex by the placement constructor `0x0065EC80` (`0x0065EC87`) |
| `+0x08` | `u32` | m_elementCount | m_elementCount (u32), registered by `0x006660D0` (`0x00632960` at `0x006661D5`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PIndexDataBlockBase; cleared by the placement constructor `0x0065EC80` (`0x0065EC8A`) |
| `+0x0F` | `u8[1]` | pad0F | the byte after the byte the placement constructor `0x0065EC80` clears at `+0x0E` (`0x0065EC93`), before the dword it clears at `+0x10` (`0x0065EC96`); no registered member covers it (`0x00662080` registers the `0x14`-byte class at `0x006620D0`) |

`PLODLevel` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x18` | `f32` | m_minimumThreshold | m_minimumThreshold (f32), registered by `0x006C5FF0` (`0x00632960` at `0x006C617E`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PLODLevel; the placement constructor `0x006C4A60` sets it to 0 (`0x006C4A82`) and m_maximumThreshold (`+0x1C`) to 10000.0 (`0x006C4A85`) |
| `+0x24` | `u8[4]` | bytes24 | the bytes at `+0x24`, after `+0x20` and before `+0x28`; no registered member covers it (`0x006C4F70` registers the `0x38`-byte class at `0x006C4FC0`) |
| `+0x34` | `u8[4]` | bytes34 | the bytes after `+0x30` up to the end of the `0x38`-byte class; no registered member covers it (`0x006C4F70` registers the `0x38`-byte class at `0x006C4FC0`) |

`PMeshInstanceSegmentStreamBinding` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `void*` | m_name | m_name (ptr), registered by `0x005E68B0` (`0x00632960` at `0x005E69B0`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PMeshInstanceSegmentStreamBinding; cleared by the placement constructor `0x005CEEF0` (`0x005CEEFA`) |
| `+0x10` | `u16` | m_nameHash | m_nameHash (u16), registered by `0x005E68B0` (`0x00632960` at `0x005E6A23`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PMeshInstanceSegmentStreamBinding; cleared with m_index and m_inputSet by the placement constructor `0x005CEEF0` (dword store `0x005CEEFE`) |
| `+0x12` | `u8` | m_index | m_index (u8), registered by `0x005E68B0` (`0x00632960` at `0x005E6A96`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PMeshInstanceSegmentStreamBinding; cleared by the placement constructor `0x005CEEF0` (`0x005CEEFE`) |
| `+0x13` | `u8` | m_inputSet | m_inputSet (u8), registered by `0x005E68B0` (`0x00632960` at `0x005E6B09`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PMeshInstanceSegmentStreamBinding; cleared by the placement constructor `0x005CEEF0` (`0x005CEEFE`) |
| `+0x14` | `u8[4]` | bytes14 | the bytes after m_inputSet (u8 at `+0x13`) up to the end of the `0x18`-byte class; no registered member covers it (`0x005D9930` registers the `0x18`-byte class at `0x005D9980`) |

`PMeshSegmentBase` (`0x30` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_materialIndex | m_materialIndex (u32), registered by `0x00666E90` (`0x00632960` at `0x00666F1E`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PMeshSegmentBase; the placement constructor `0x0065EA30` sets it to 0 (`0x0065EA3E`) |
| `+0x2C` | `u8[4]` | bytes2C | the bytes after the dword the placement constructor `0x0065EA30` clears at `+0x28` (`0x0065EA5D`) up to the end of the `0x30`-byte class; no registered member covers it (`0x00662480` registers the `0x30`-byte class at `0x006624D0`) |

`PModifierNetwork` (`0x70` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_totalOutputElementSize | m_totalOutputElementSize (u32), registered by `0x006D0FA0` (`0x00632960` at `0x006D126A`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetwork; the placement constructor `0x006CFA50` clears it (`0x006CFA76`) |
| `+0x04` | `u8[4]` | bytes04 | the bytes after m_totalOutputElementSize (`+0x00`), before the dword the placement constructor `0x006CFA50` clears at `+0x08` (`0x006CFA57`); no registered member covers it (`0x006CFC50` registers the `0x70`-byte class at `0x006CFCA0`) |
| `+0x18` | `u32` | m_totalInputCount | m_totalInputCount (u32), registered by `0x006D0FA0` (`0x00632960` at `0x006D10D0`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetwork; the placement constructor `0x006CFA50` clears it (`0x006CFA73`) |
| `+0x1C` | `u8[4]` | bytes1C | the bytes after m_totalInputCount (`+0x18`), before the dword the placement constructor `0x006CFA50` clears at `+0x20` (`0x006CFA5E`); no registered member covers it (`0x006CFC50` registers the `0x70`-byte class at `0x006CFCA0`) |
| `+0x50` | `u32` | m_totalPersistentStateSize | m_totalPersistentStateSize (u32), registered by `0x006D0FA0` (`0x00632960` at `0x006D13C1`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetwork; the placement constructor `0x006CFA50` clears it with m_totalStateBlockSize (`0x006CFA80`) |
| `+0x54` | `u32` | m_totalStateBlockSize | m_totalStateBlockSize (u32), registered by `0x006D0FA0` (`0x00632960` at `0x006D1434`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetwork; the placement constructor `0x006CFA50` clears it with m_totalPersistentStateSize (`0x006CFA80`) |
| `+0x58` | `u8` | m_isCompiled | m_isCompiled (u8), registered by `0x006D0FA0` (`0x00632960` at `0x006D14A7`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetwork; the placement constructor `0x006CFA50` clears it (`0x006CFA84`) |
| `+0x59` | `u8[7]` | pad59 | the bytes after m_isCompiled (u8 at `+0x58`), before the dword the placement constructor `0x006CFA50` clears at `+0x60` (`0x006CFA6C`); no registered member covers it (`0x006CFC50` registers the `0x70`-byte class at `0x006CFCA0`) |

`PModifierNetworkDynamicMeshSegment` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u32` | m_segmentInputGroupStart | m_segmentInputGroupStart (u32), registered by `0x006BCA20` (`0x00632960` at `0x006BCB20`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkDynamicMeshSegment; cleared with m_segmentOutputGroupStart by the placement constructor `0x005CEEF0` (`0x005CEEFA`) |
| `+0x0C` | `u32` | m_segmentOutputGroupStart | m_segmentOutputGroupStart (u32), registered by `0x006BCA20` (`0x00632960` at `0x006BCB93`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkDynamicMeshSegment; cleared with m_segmentInputGroupStart by the placement constructor `0x005CEEF0` (`0x005CEEFA`) |
| `+0x10` | `u32` | m_modifierOutputsAreConsumed | m_modifierOutputsAreConsumed (u32), registered by `0x006BCA20` (`0x00632960` at `0x006BCC06`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkDynamicMeshSegment; cleared by the placement constructor `0x005CEEF0` (`0x005CEEFE`) |
| `+0x14` | `u8[4]` | bytes14 | the bytes after m_modifierOutputsAreConsumed (`+0x10`) up to the end of the `0x18`-byte class; no registered member covers it (`0x006BBB70` registers the `0x18`-byte class at `0x006BBBC0`) |

`PModifierNetworkInstanceInput` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u32` | m_elementSize | m_elementSize (u32), registered by `0x006C3580` (`0x00632960` at `0x006C3612`); no shipped .phyre file declares PModifierNetworkInstanceInput; cleared with `+0x0C` by the placement constructor `0x006C2960` (`0x006C2967`) |
| `+0x0C` | `u8[4]` | bytes0C | cleared with m_elementSize by the placement constructor `0x006C2960` (`0x006C2967`); no registered member covers it (`0x006C2EF0` registers the `0x20`-byte class at `0x006C2F3A`) |

`PSamplerStateBase` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x05` | `u8[3]` | pad05 | the bytes after m_wrapR (u8 at `+0x04`, registered by `0x005E7070` at `0x005E72D9`; the placement constructor `0x005D5FE0` sets it to 1 at `0x005D5FED`) up to m_lodBias (`+0x08`); no registered member covers it (`0x005D9E70` registers the `0x20`-byte class at `0x005D9EC0`) |
| `+0x08` | `f32` | m_lodBias | m_lodBias (f32), registered by `0x005E7070` (`0x00632960` at `0x005E734C`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PSamplerStateBase; the placement constructor `0x005D5FE0` sets it to 0 (`0x005D5FF1`) |
| `+0x10` | `u32` | m_borderColor | m_borderColor (u32), registered by `0x005E7070` (`0x00632960` at `0x005E7432`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PSamplerStateBase; the placement constructor `0x005D5FE0` sets it to 0 with the qword store that writes 1.0 to `+0x0C` (`0x005D5FF4`) |
| `+0x14` | `u32` | m_baseLevel | m_baseLevel (u32), registered by `0x005E7070` (`0x00632960` at `0x005E74A5`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PSamplerStateBase; the placement constructor `0x005D5FE0` sets it to 0 (`0x005D5FFC`) |

`PSceneRenderPass` (`0x50` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x48` | `u8` | m_platformsAreInclude | m_platformsAreInclude (u8), registered by `0x005E7E60` (`0x00632960` at `0x005E81A5`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PSceneRenderPass; the placement constructor `0x005D27B0` clears it (`0x005D27DD`) |
| `+0x49` | `u8[7]` | pad49 | the bytes after m_platformsAreInclude (u8 at `+0x48`) up to the end of the `0x50`-byte class; no registered member covers it (`0x005D9F20` registers the `0x50`-byte class at `0x005D9F70`) |

`PShader` (`0x40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u8[4]` | bytes04 | the bytes after the dword the placement constructor `0x005D3C60` sets to `0xF` at `+0x00` (`0x005D3C67`), before the dword it clears at `+0x08` (`0x005D3C6D`); no registered member covers it (`0x005DA070` registers the `0x40`-byte class at `0x005DA0C0`) |
| `+0x38` | `u32` | m_parameterBufferSize | m_parameterBufferSize (u32), registered by `0x005E81E0` (`0x00632960` at `0x005E8424`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShader; the placement constructor `0x005D3C60` sets it to 0 (`0x005D3C82`) |
| `+0x3C` | `u8[4]` | bytes3C | the bytes after m_parameterBufferSize (`+0x38`) up to the end of the `0x40`-byte class; no registered member covers it (`0x005DA070` registers the `0x40`-byte class at `0x005DA0C0`) |

`PShaderParameterCaptureBufferLocationTypeConstantBuffer` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u32` | m_constantBufferLocation | m_constantBufferLocation (u32), registered by `0x005E89C0` (`0x00632960` at `0x005E8A4E`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderParameterCaptureBufferLocationTypeConstantBuffer; the placement constructor `0x005D7DE0` clears `+0x04` to `+0x0B` (`0x005D7DEA`) |
| `+0x08` | `u32` | m_size | m_size (u32), registered by `0x005E89C0` (`0x00632960` at `0x005E8ABD`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderParameterCaptureBufferLocationTypeConstantBuffer; cleared with m_constantBufferLocation by the placement constructor `0x005D7DE0` (`0x005D7DEA`) |
| `+0x0D` | `u8[3]` | pad0D | the bytes after m_type (u8 at `+0x0C`, registered by `0x005E89C0` at `0x005E8B2C`; the placement constructor `0x005D7DE0` sets it to `0x34` at `0x005D7DEE`) up to the end of the `0x10`-byte class; no registered member covers it (`0x005DA6D0` registers the `0x10`-byte class at `0x005DA71A`) |

`PShape` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_indexCount | m_indexCount (u32), registered by `0x006673A0` (`0x00632960` at `0x00667544`); no shipped .phyre file declares PShape; the placement constructor `0x006611F0` sets it to 0 (`0x006611F7`) |
| `+0x04` | `u8[4]` | pad04 | alignment bytes between m_indexCount (`+0x00`) and m_indices (PArray at `+0x08`); no registered member covers it (`0x006625D0` registers the `0x38`-byte class at `0x00662620`) |
| `+0x18` | `u32` | m_vertexCount | m_vertexCount (u32), registered by `0x006673A0` (`0x00632960` at `0x006676C1`); no shipped .phyre file declares PShape; the placement constructor `0x006611F0` sets it to 0 (`0x00661200`) |
| `+0x1C` | `u8[4]` | pad1C | alignment bytes between m_vertexCount (`+0x18`) and m_vertexData (PArray at `+0x20`); no registered member covers it (`0x006625D0` registers the `0x38`-byte class at `0x00662620`) |
| `+0x32` | `u8[6]` | pad32 | the bytes after m_indexFormat (u8 at `+0x31`; the placement constructor `0x006611F0` sets `+0x30` and `+0x31` to `0x34` at `0x0066120A`) up to the end of the `0x38`-byte class; no registered member covers it (`0x006625D0` registers the `0x38`-byte class at `0x00662620`) |

`PStreamInputDescD3D11` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | m_semantic | m_semantic (ptr), registered by `0x00618390` (`0x00632960` at `0x0061841D`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PStreamInputDescD3D11 |
| `+0x10` | `u32` | m_semanticIndex | m_semanticIndex (u32), registered by `0x00618390` (`0x00632960` at `0x00618503`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PStreamInputDescD3D11 |
| `+0x14` | `u32` | m_d3dFormat | m_d3dFormat (u32), registered by `0x00618390` (`0x00632960` at `0x00618576`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PStreamInputDescD3D11 |
| `+0x18` | `u32` | m_inputSlot | m_inputSlot (u32), registered by `0x00618390` (`0x00632960` at `0x006185E9`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PStreamInputDescD3D11 |
| `+0x1C` | `u8[4]` | bytes1C | the bytes after m_inputSlot (`+0x18`) up to the end of the `0x20`-byte class; no registered member covers it (`0x00615170` registers the `0x20`-byte class at `0x006151C0`) |

`PStructuredBufferBase` (`0x14` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_elementCount | m_elementCount (u32), registered by `0x005EAAA0` (`0x00632960` at `0x005EAB2E`); no shipped .phyre file declares PStructuredBufferBase; the placement constructor `0x005D0090` clears `+0x00` to `+0x07` (`0x005D0097`) |
| `+0x04` | `u32` | m_elementSize | m_elementSize (u32), registered by `0x005EAAA0` (`0x00632960` at `0x005EABA1`); no shipped .phyre file declares PStructuredBufferBase; cleared with m_elementCount by the placement constructor `0x005D0090` (`0x005D0097`) |
| `+0x08` | `u32` | m_flags | m_flags (u32), registered by `0x005EAAA0` (`0x00632960` at `0x005EAC14`); no shipped .phyre file declares PStructuredBufferBase; the placement constructor `0x005D0090` clears `+0x08` to `+0x0F` (`0x005D009A`) |
| `+0x0C` | `u8[4]` | bytes0C | cleared with m_flags by the placement constructor `0x005D0090` (`0x005D009A`); no registered member covers it (`0x005DB910` registers the `0x14`-byte class at `0x005DB960`) |
| `+0x11` | `u8[3]` | pad11 | the bytes after the byte the placement constructor `0x005D0090` clears at `+0x10` (`0x005D009E`) up to the end of the `0x14`-byte class; no registered member covers it (`0x005DB910` registers the `0x14`-byte class at `0x005DB960`) |

`PTexture3DBase` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x28` | `u32` | m_width | m_width (u32), registered by `0x005EAD90` (`0x00632960` at `0x005EAE22`); no shipped .phyre file declares PTexture3DBase |
| `+0x2C` | `u32` | m_height | m_height (u32), registered by `0x005EAD90` (`0x00632960` at `0x005EAE95`); no shipped .phyre file declares PTexture3DBase |
| `+0x30` | `u32` | m_depth | m_depth (u32), registered by `0x005EAD90` (`0x00632960` at `0x005EAF08`); no shipped .phyre file declares PTexture3DBase |
| `+0x34` | `u8[4]` | bytes34 | the bytes after m_depth (`+0x30`) up to the end of the `0x38`-byte class; no registered member covers it (`0x005DBBA0` registers the `0x38`-byte class at `0x005DBBEA`) |

`PTextureCommonBase` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0A` | `u8[2]` | pad0A | the bytes after the word the placement constructor `0x005D7B60` sets to `0x300` at `+0x08` (`0x005D7B71`), before the qword it clears at `+0x0C` (`0x005D7B77`); no registered member covers it (`0x005DBC40` registers the `0x28`-byte class at `0x005DBC90`) |
| `+0x10` | `u32` | m_mipmapCount | m_mipmapCount (u32), registered by `0x005EAF40` (`0x00632960` at `0x005EB0B9`); the cluster loader binds it by name (`0x0059B430`) in the 35,978 shipped .phyre files that declare PTextureCommonBase; the placement constructor `0x005D7B60` clears it with the qword store at `+0x0C` (`0x005D7B77`) |
| `+0x14` | `u32` | m_maxMipLevel | m_maxMipLevel (u32), registered by `0x005EAF40` (`0x00632960` at `0x005EB12C`); the cluster loader binds it by name (`0x0059B430`) in the 35,978 shipped .phyre files that declare PTextureCommonBase; the placement constructor `0x005D7B60` clears it (`0x005D7B7B`) |

`PTextureCubeMapBase` (`0x30` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x28` | `u32` | m_size | m_size (u32), registered by `0x005EB2B0` (`0x00632960` at `0x005EB339`); the cluster loader binds it by name (`0x0059B430`) in the 6,781 shipped .phyre files that declare PTextureCubeMapBase; the placement constructor `0x005D1700` sets it to 0 (`0x005D1722`) |
| `+0x2C` | `u8[4]` | bytes2C | the bytes after m_size (`+0x28`) up to the end of the `0x30`-byte class; no registered member covers it (`0x005DBD90` registers the `0x30`-byte class at `0x005DBDDA`) |

`PTimeIntervalController` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x18` | `f32` | m_parentBase | the parent time at which the interval starts: `0x005C5330` takes the parent controller's time (slot `+0x20` of `+0x10`, or the global time at `0x02CACF14`) minus it (`0x005C5383`); m_parentBase (f32), registered by `0x005B2990` (`0x00632960` at `0x005B2A94`); no shipped .phyre file declares PTimeIntervalController |
| `+0x1C` | `f32` | m_localBase | the local time at the start of the interval: `0x005C5330` adds it last (`0x005C53B5`), so the result is m_localBase + sign * ((t - m_parentBase) mod abs(m_localRange)); m_localBase (f32), registered by `0x005B2990` (`0x00632960` at `0x005B2B07`); no shipped .phyre file declares PTimeIntervalController |
| `+0x20` | `f32` | m_localRange | the interval's length: `0x005C5330` wraps the elapsed parent time into it with fmodf (`0x005C5362`-`0x005C5392`); a negative length runs the interval backwards (sign -1.0, `0x005C5371`); m_localRange (f32), registered by `0x005B2990` (`0x00632960` at `0x005B2B7A`); no shipped .phyre file declares PTimeIntervalController |
| `+0x24` | `u8[4]` | bytes24 | the bytes after m_localRange (`+0x20`) up to the end of the `0x28`-byte class; no registered member covers it (`0x005A9340` registers the `0x28`-byte class at `0x005A938A`) |

For a negative `fmodf` result r, `0x005C5330` goes on with `r + sign * range` before it applies the sign and
adds `m_localBase` (`0x005C5397`-`0x005C53B5`).

`PTrigger` (`0x58` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x50` | `u8` | m_enabled | whether the trigger is enabled; m_enabled (u8), registered by `0x006A7EE0` (`0x00632960` at `0x006A8159`); no shipped .phyre file declares PTrigger; the script methods getEnabled (registered at `0x006A827F`) and setEnabled (`0x006A8349`) read and write it through `0x006A9150` and `0x006A9280`; the placement constructor `0x006A7B10` sets it to 1 (`0x006A7B61`) |
| `+0x51` | `u8[7]` | pad51 | the bytes after m_enabled (u8 at `+0x50`) up to the end of the `0x58`-byte class; no registered member covers it (`0x006A7BA0` registers the `0x58`-byte class at `0x006A7BF0`) |

`PVertexStream` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_offset | m_offset (u32), registered by `0x00667A60` (`0x00632960` at `0x00667B61`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PVertexStream; the placement constructor `0x0065F960` sets it to 0 (`0x0065F967`) |
| `+0x04` | `u8[4]` | bytes04 | the bytes after m_offset (`+0x00`), before the qword the placement constructor `0x0065F960` clears at `+0x08` (`0x0065F969`); no registered member covers it (`0x006627E0` registers the `0x18`-byte class at `0x00662830`) |
| `+0x12` | `u8[6]` | bytes12 | the bytes after the word the placement constructor `0x0065F960` sets to `0xFF34` at `+0x10` (`0x0065F96D`) up to the end of the `0x18`-byte class; no registered member covers it (`0x006627E0` registers the `0x18`-byte class at `0x00662830`) |

`PDebugUtils` (`0x58` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C` | `u8[4]` | bytes0C | `+0xC` to `+0xF`; no registered member covers it (`0x00791C20` registers the `0x58`-byte class at `0x00791C70`) |
| `+0x18` | `u8[56]` | bytes18 | `+0x18` to `+0x4F`; no registered member covers it (`0x00791C20` registers the `0x58`-byte class at `0x00791C70`) |
| `+0x51` | `u8[7]` | pad51 | the bytes after m_autoClear (u8 at `+0x50`) up to the end of the `0x58`-byte class; no registered member covers it (`0x00791C20` registers the `0x58`-byte class at `0x00791C70`) |

`PShaderParameterCaptureBufferLocationType` (`0x4` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x03` | `u8[1]` | pad03 | the byte after m_type (u8 at `+0x02`) up to the end of the 4-byte class; no registered member covers it (`0x005DA630` registers the `0x4`-byte class at `0x005DA67A`) |

`PDynamicMesh` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | the vtable pointer, `0x00D68DF0` for the class: stored by `0x00662A50` (`0x00662A57`) and `0x00663080` (`0x0066309E`); `0x00671E80` calls through its slot `+0x28` (`0x00671F87`-`0x00671F9C`); no registered member covers it (`0x00661E80` registers the `0x38`-byte class at `0x00661ED0`) |
| `+0x30` | `u8[8]` | dword30 | `0x00662A50` clears the dword at `+0x30` (`0x00662A6E`); no registered member covers it (`0x00661E80` registers the `0x38`-byte class at `0x00661ED0`) |

`PDynamicMeshInstance` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x10` | `u8[8]` | dword10 | the constructors `0x005DBF60` and `0x005DC0B0` clear the dword at `+0x10` (`0x005DBF71`, `0x005DC0CD`); `+0x08` holds the constructor's second argument (`0x005DBF6D`); no registered member covers it (`0x005D9120` registers the `0x18`-byte class at `0x005D9170`) |

`PModifierNetworkDynamicMesh` (`0x78` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x3C` | `u8[4]` | pad3C | the four bytes between the array count at `+0x38` and its pointer at `+0x40`, both released by the destructor `0x006BBC70` (`0x006BBCEF`, `0x006BBCFB`); no registered member covers it (`0x006BBAD0` registers the `0x78`-byte class at `0x006BBB1A`) |
| `+0x4C` | `u8[4]` | pad4C | the four bytes between the array count at `+0x48` and its pointer at `+0x50`, both released by the destructor `0x006BBC70` (`0x006BBCCD`, `0x006BBCD9`); no registered member covers it (`0x006BBAD0` registers the `0x78`-byte class at `0x006BBB1A`) |
| `+0x5C` | `u8[4]` | pad5C | the four bytes between the array count at `+0x58` and its pointer at `+0x60`, both released by the destructor `0x006BBC70` (`0x006BBCAB`, `0x006BBCB7`); no registered member covers it (`0x006BBAD0` registers the `0x78`-byte class at `0x006BBB1A`) |
| `+0x6C` | `u8[4]` | pad6C | the four bytes between the array count at `+0x68` and its pointer at `+0x70`, both released by the destructor `0x006BBC70` (`0x006BBC87`, `0x006BBC93`); no registered member covers it (`0x006BBAD0` registers the `0x78`-byte class at `0x006BBB1A`) |

`PModifierNetworkDynamicMeshInstance` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x1C` | `u8[4]` | pad1C | the four bytes between the array count at `+0x18` and its pointer at `+0x20`, both released by the destructor `0x005E2AF0` (`0x005E2B13`, `0x005E2B1F`); no registered member covers it (`0x005D99E0` registers the `0x28`-byte class at `0x005D9A2A`) |

`PShadowRenderer` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u8[4]` | bytes04 | `+0x4` to `+0x7`; no registered member covers it (`0x005DB7C0` registers the `0x10`-byte class at `0x005DB810`) |

Three class registrations, a constructor, three deleting destructors and a placement constructor, read at
the bytes:

- `0x006625D0` registers `PShape`: `0x00632D80(descriptor, the result of 0x006373D0, the name 0x00D66048, 0x38, 8,
  the result of 0x006372A0, 0)` at `0x00662620`; it then installs the vtable `0x00D66600`, sets bit `0x2` of
  `+0xFC` and hands `0x02D395D0`, `0x02D39610` and `0x02D39650` to `0x0063DC80`, `0x0063DF90` and `0x0063DFA0`
  (`0x006625EB`-`0x0066265F`).
- `0x006BBAD0` registers `PModifierNetworkDynamicMesh`, a `0x78`-byte class, the same way at `0x006BBB1A` with
  the name at `0x00D81778`, the alignment 8, the base `0x02D3A140` and 0; the vtable is `0x00D81268`, bit `0x2` of
  `+0xFC` is set and
  `0x02E57DE0`, `0x02E57E60` and `0x02E57EE0` go to the same three functions (`0x006BBAE6`-`0x006BBB59`).
- `0x00791C20` registers `PDebugUtils`, name `0x01CB09D0`, size `0x58`, at `0x00791C70` with the alignment 8, the
  result of `0x006372A0` and 0; the vtable is `0x01CB0BD0`, bit `0x2` of `+0xFC` is set and `0x02EAC0A0`,
  `0x02EAC100` and `0x02EAC160` go to the same three functions (`0x00791C3B`-`0x00791CAF`).
- Each of the three returns its descriptor (`0x00662665`, `0x006BBB5F`, `0x00791CB5`).
- `0x00662A50` installs the vtable `0x00D68DF0`, clears the qword `+0x08`, the dword `+0x10`, the qword `+0x18`,
  the dword `+0x20`, the qword `+0x28` and the dword `+0x30`, and returns the object (`0x00662A50`-`0x00662A71`).
- `0x00675700`, slot 0 of `0x00D6C378`, the vtable of the `m_asset` member's helper, stores that vtable, runs
  `0x00633770` on the object, frees the `0x20`-byte object through `0x00809950` when bit `0x1` of its second
  argument is set, and returns the object (`0x0067570A`-`0x00675730`).
- `0x0067E690` and `0x006B4170`, slot 0 of the caller objects' vtables under State, install the vtable
  `0x00D27B80`, free the object through `0x00809950` when bit `0x1` of the second argument is set, with the
  size `0x10` in `0x0067E690` and `0x18` in `0x006B4170`, and return the object (`0x0067E696`-`0x0067E6B2`,
  `0x006B4176`-`0x006B4192`).
- `0x006BE990`, the placement constructor of `PLight` (slot `+0x50` of the vtable `0x00D82B58`), skips a null
  block and answers 1 (`0x006BE990`-`0x006BE9E1`).
- On a block `0x006BE990` stores 0.5 in the floats `+0x00`, `+0x04` and `+0x08` and 1.0 in `+0x0C`, 0 in the
  qwords `+0x10` and `+0x18`, the address `0x01F2ED48` in the qword `+0x20`, 0 in the dword `+0x28`, the float
  `0x3EC90FDB` in `+0x2C`, 1.0 in the float `+0x30` with 0 in the dword above it, and `0x7F7FFFFF` in the
  dword `+0x38` with 0 in the dword above it (`0x006BE995`-`0x006BE9D7`).

`0x00819990`, which the note on the `+0x20` and `+0x18` reads under Project notes names, is the Lua collector's
sweep of a table list's keys; it is described on [Lua runtime](../Third-Party-Libraries/lua-runtime.md).

## Shipped data

| Fact | Value |
|---|---|
| static descriptor constructions | 399: 384 calls to `0x00632D80` and 15 to `0x00632C90` (a 385th call is inside `0x00632E80`); `PBase` (`0x02CF8270`, size 1) and `PClassDescriptor` (`0x02CF8470`, size `0x100`) by their own initialisers |
| member registrations | 682 calls to `0x00632960` (2 of them the array and dynamic constructors forwarding), 165 to `0x00632A10`, 29 to `0x00632A70`, 21 to `0x00632BE0` |
| plain-member attribute arguments | `0x10` 207, `0x00` 196, `0x08` 123, `0x12` 79, `0x0A` 39, `0x02` 36; the flag argument is 0 at all 680 |
| array kinds | `PArray` 86, pointer array 70, `PSharray` 9; element alignments 8 (113), 4 (36), 1 (7), 2 (6), 16 (3) |
| annotations | 70 constructions; 69 static `WriteMask` annotations (60 `PArray`, 9 `PSharray`) |
| buffers | 384 classes register a default instance and both masks |
| by-name registrations | `0x006388C0`: 523 sites, 516 calls and 7 tail jumps; `0x00639450`: 471 sites, 156 calls and 315 tail jumps |
| base destructor | `0x00633390`: 1,981 sites, 1,186 calls and 795 jumps from the destructor thunks |
| RTTI classes | `PClassDescriptorForType<T>` 409, `Abstract<T>` 393, `Concrete<T>` 331, `WithoutDefaultConstructor<T>` 38, `Wrapper<T>` 15, `PTypeDefault<T>` 12, `PClassDataMemberArrayDynamic<T>` 71, `PClassDataMemberPhyreArray<T>` 59 |

### Data files

These tables stay beside this page. Each lists one generated family or one per-class view.

| File | Rows | What it lists |
|---|---:|---|
| [phyre-reflection-abstract-class-descriptor-constructors.tsv](phyre-reflection-abstract-class-descriptor-constructors.tsv) | 178 | Abstract descriptor constructors such as `0x005A7ED0` |
| [phyre-reflection-abstract-class-descriptor-base-aware-constructors.tsv](phyre-reflection-abstract-class-descriptor-base-aware-constructors.tsv) | 132 | Abstract constructors that pass a parent descriptor |
| [phyre-reflection-pclassdescriptor-static-initialisers.tsv](phyre-reflection-pclassdescriptor-static-initialisers.tsv) | 254 | Concrete static initialisers such as `0x001603E0` |
| [phyre-reflection-descriptor-flag-registrars.tsv](phyre-reflection-descriptor-flag-registrars.tsv) | 34 | descriptor initialisers, 64-byte form |
| [phyre-reflection-descriptor-flag-registrars-compact.tsv](phyre-reflection-descriptor-flag-registrars-compact.tsv) | 5 | descriptor initialisers, 53-byte form |
| [phyre-reflection-guarded-class-registration-stubs.tsv](phyre-reflection-guarded-class-registration-stubs.tsv) | 99 | thread-safe guarded class registrars |
| [phyre-reflection-name-only-class-registration-initialisers.tsv](phyre-reflection-name-only-class-registration-initialisers.tsv) | 110 | initialisers that call `0x006388C0` and jump to `0x00639450` |
| [phyre-reflection-two-member-descriptor-registrars.tsv](phyre-reflection-two-member-descriptor-registrars.tsv) | 38 | array descriptors with `m_count` and `m_els` |
| [phyre-reflection-phyre-registrar-classes.tsv](phyre-reflection-phyre-registrar-classes.tsv) | 409 | registrars and the classes they name |
| [phyre-reflection-phyre-type-name-hashes.tsv](phyre-reflection-phyre-type-name-hashes.tsv) | 399 | type names and their `0x006388C0` hashes |
| [phyre-reflection-phyre-class-instance-sizes.tsv](phyre-reflection-phyre-class-instance-sizes.tsv) | 177 | instance size and alignment per class |
| [phyre-reflection-phyre-class-parent-chain.tsv](phyre-reflection-phyre-class-parent-chain.tsv) | 330 | parent descriptor per class |
| [phyre-reflection-phyre-class-f4-offset-adjustment.tsv](phyre-reflection-phyre-class-f4-offset-adjustment.tsv) | 179 | `+0xF4` per class |
| [phyre-reflection-phyre-default-instances.tsv](phyre-reflection-phyre-default-instances.tsv) | 173 | default instance per class |
| [phyre-reflection-phyre-class-default-buffers.tsv](phyre-reflection-phyre-class-default-buffers.tsv) | 384 | the `+0xC0`, `+0xC8` and `+0xD0` buffers per class |
| [phyre-reflection-array-type-names.tsv](phyre-reflection-array-type-names.tsv) | 69 | the class name each array-type getter receives, with one call that passes it |
| [phyre-reflection-phyre-class-descriptor-vtable.tsv](phyre-reflection-phyre-class-descriptor-vtable.tsv) | 315 | each class's descriptor vtable and its slots |
| [phyre-reflection-phyre-class-descriptor-accesses.tsv](phyre-reflection-phyre-class-descriptor-accesses.tsv) | 227 | instructions that access descriptor fields |
| [phyre-reflection-p-type-default-u-int-accesses.tsv](phyre-reflection-p-type-default-u-int-accesses.tsv) | 19 | accesses to the `PTypeDefault<unsigned int>` object |
| [phyre-reflection-ptexture2d-d3d11-accesses.tsv](phyre-reflection-ptexture2d-d3d11-accesses.tsv) | 24 | accesses to a `PTexture2DD3D11`, from its constructor `0x006160B0` |
| [phyre-reflection-ptexture-cube-map-d3d11-accesses.tsv](phyre-reflection-ptexture-cube-map-d3d11-accesses.tsv) | 95 | accesses to a `PTextureCubeMapD3D11`, from its constructor `0x006161A0` (placement constructor `0x00612D00`) |
| [phyre-reflection-rtti-class-vtables.tsv](phyre-reflection-rtti-class-vtables.tsv) | 2,286 | class name to vtable for every polymorphic class |
| [phyre-reflection-pclassdescriptorconcrete-placement-default-ctors.tsv](phyre-reflection-pclassdescriptorconcrete-placement-default-ctors.tsv) | 123 | slot `+0x50` construct-in-place bodies |
| [phyre-reflection-object-traversal-adapters.tsv](phyre-reflection-object-traversal-adapters.tsv) | 304 | slot `+0x00` member-visit adapters |
| [phyre-reflection-flag-selected-traversal-adapters.tsv](phyre-reflection-flag-selected-traversal-adapters.tsv) | 11 | member-visit adapters that pass the order flag |
| [phyre-reflection-registry-fetch-traversal-adapters.tsv](phyre-reflection-registry-fetch-traversal-adapters.tsv) | 84 | member-visit adapters that fetch their descriptor first |
| [phyre-reflection-object-lifecycle-lookup-adapters.tsv](phyre-reflection-object-lifecycle-lookup-adapters.tsv) | 6 | adapters that call `0x0063BC00` |
| [phyre-reflection-shared-runtime-identity-dispatch-adapters.tsv](phyre-reflection-shared-runtime-identity-dispatch-adapters.tsv) | 6 | adapters that call `0x00639850` |
| [phyre-reflection-static-descriptor-singleton-lazyinit-adapters.tsv](phyre-reflection-static-descriptor-singleton-lazyinit-adapters.tsv) | 7 | guarded descriptor singletons |
| [phyre-reflection-nativeadapter-staticdescriptorsingletonlazyinit2.tsv](phyre-reflection-nativeadapter-staticdescriptorsingletonlazyinit2.tsv) | 5 | guarded descriptor singletons, second form |
| [phyre-reflection-nativeadapter-staticdescriptorsingletonlazyinit3.tsv](phyre-reflection-nativeadapter-staticdescriptorsingletonlazyinit3.tsv) | 4 | guarded descriptor singletons, third form |
| [phyre-reflection-nativeadapter-singletonallocdescriptorinstall.tsv](phyre-reflection-nativeadapter-singletonallocdescriptorinstall.tsv) | 5 | adapters that allocate an 8-byte object and install a descriptor |
| [phyre-reflection-nativeadapter-descriptorfieldselecttail.tsv](phyre-reflection-nativeadapter-descriptorfieldselecttail.tsv) | 4 | adapters that select a descriptor field |
| [phyre-reflection-class-descriptor-static-teardowns.tsv](phyre-reflection-class-descriptor-static-teardowns.tsv) | 404 | descriptor `atexit` teardowns such as `0x008A8E20` |
| [phyre-reflection-pclassdescriptor-destructor-thunks.tsv](phyre-reflection-pclassdescriptor-destructor-thunks.tsv) | 384 | thunks that restore a vtable and jump to `0x00633390` |
| [phyre-reflection-pclassdescriptor-deleting-destructors.tsv](phyre-reflection-pclassdescriptor-deleting-destructors.tsv) | 1,148 | ForType deleting destructors such as `0x005847E0` |
| [phyre-reflection-pclassdescriptor-deleting-destructors-map.tsv](phyre-reflection-pclassdescriptor-deleting-destructors-map.tsv) | 1,149 | the vtable each of them installs |
| [phyre-reflection-data-member-metadata-static-teardowns.tsv](phyre-reflection-data-member-metadata-static-teardowns.tsv) | 853 | member-record `atexit` teardowns |
| [phyre-reflection-pclassdatamember-deleting-destructors.tsv](phyre-reflection-pclassdatamember-deleting-destructors.tsv) | 138 | member-record deleting destructors |
| [phyre-reflection-pclassdatamemberstaticteardownadapter.tsv](phyre-reflection-pclassdatamemberstaticteardownadapter.tsv) | 30 | member-record teardown adapters |
| [phyre-reflection-annotationstaticteardown.tsv](phyre-reflection-annotationstaticteardown.tsv) | 55 | annotation teardowns |
| [phyre-reflection-nameddescriptorstaticteardown.tsv](phyre-reflection-nameddescriptorstaticteardown.tsv) | 15 | named-descriptor teardowns |
| [phyre-reflection-ptypestaticteardown.tsv](phyre-reflection-ptypestaticteardown.tsv) | 17 | `PType` teardowns |
| [phyre-reflection-reflectionstaticteardown.tsv](phyre-reflection-reflectionstaticteardown.tsv) | 28 | other reflection-object teardowns |
| [phyre-reflection-staticdescriptorsingleton.tsv](phyre-reflection-staticdescriptorsingleton.tsv) | 12 | static descriptor singletons |

### Columns of the one-column lists

Fourteen of the data files above have one column, `entry`: the entry address of one body, one row per body in
address order. Every body of a list has the form below; sizes are body lengths in bytes.

| File | Each body |
|---|---|
| `phyre-reflection-abstract-class-descriptor-constructors.tsv` | 152 bytes: calls `0x006373D0`, then `0x00632D80` with an image address as its sixth argument, stores the vtable, sets bit `0x2` of `+0xFC` and calls `0x0063DC80`, `0x0063DF90` and `0x0063DFA0` |
| `phyre-reflection-abstract-class-descriptor-base-aware-constructors.tsv` | 163 bytes: the same, except that the sixth argument of `0x00632D80` is the value `0x006372A0` returns |
| `phyre-reflection-pclassdescriptor-static-initialisers.tsv` | 53 bytes: calls its class's constructor (254 different ones) on a static descriptor, clears bit `0x2` of the descriptor's `+0xFC`, stores a vtable at its `+0x00` and jumps to `atexit` (`0x00808B90`) with a teardown |
| `phyre-reflection-class-descriptor-static-teardowns.tsv` | 26 bytes: stores a vtable at a static descriptor and jumps to the base destructor `0x00633390` with that descriptor in `rcx` |
| `phyre-reflection-pclassdescriptor-destructor-thunks.tsv` | 15 bytes: stores a vtable at `[rcx]` and jumps to `0x00633390` |
| `phyre-reflection-pclassdescriptor-deleting-destructors.tsv` | 92 bytes: stores a vtable at `[rcx]` and calls `0x00633390`; when bit `0x1` of the flag argument is set it calls `_aligned_free` (`0x00584730`), or, with bit `0x4` also set, `0x0016D6A0` with the size `0x100` (1,144 rows) or `0x108` (`0x005A4010`, `0x005D1DC0`, `0x006CEFC0`, `0x006D9EA0`) |
| `phyre-reflection-data-member-metadata-static-teardowns.tsv` | 12 bytes: loads a static object into `rcx` and jumps to `0x00633240` (662 rows) or `0x006332A0` (191 rows) |
| `phyre-reflection-pclassdatamember-deleting-destructors.tsv` | 82 bytes: calls `0x006332A0`, then `0x00584730` or `0x0016D6A0` by the flag argument, as the descriptor deleting destructors do |
| `phyre-reflection-pclassdatamemberstaticteardownadapter.tsv` | 12 bytes: loads a static object into `rcx` and jumps to `0x00633240` |
| `phyre-reflection-annotationstaticteardown.tsv` | 12 bytes: loads a static object into `rcx` and jumps to `0x006B6750` |
| `phyre-reflection-nameddescriptorstaticteardown.tsv` | 12 bytes: loads a static object into `rcx` and jumps to `0x006B68A0` |
| `phyre-reflection-ptypestaticteardown.tsv` | 15 bytes: stores a vtable at a static object and returns |
| `phyre-reflection-reflectionstaticteardown.tsv` | 12 bytes: loads a static object into `rcx` and jumps to `0x006B6750` (15 rows), `0x00633240` (9), `0x006332A0` (3) or `0x006B68A0` (1) |
| `phyre-reflection-staticdescriptorsingleton.tsv` | 98 bytes: returns the address of a static; on first use it registers a teardown with `atexit` (`0x00808B90`) between `_Init_thread_header` (`0x008092FC`) and `_Init_thread_footer` (`0x0080929C`) |

### Columns of phyre-reflection-descriptor-flag-registrars.tsv and phyre-reflection-descriptor-flag-registrars-compact.tsv

One row per initialiser, 34 and 5 rows in address order. Each body calls a constructor on a static descriptor,
stores the descriptor's vtable, changes its flags word `+0xFC` and jumps to `atexit` (`0x00808B90`) with the
teardown. The 64-byte bodies clear bit `0x2` and set bit `0x8` in one read-modify-write; the 53-byte bodies only
clear bit `0x2`.

| Column | Holds |
|---|---|
| `entry` | the initialiser's entry address |
| `size` | the body length in bytes: 64 in the first table, 53 in the second |
| `object` | the static descriptor: the constructor's `rcx` and the address the vtable is stored at |
| `vtable` | the address stored at the descriptor's `+0x00`. Its RTTI names a `PClassDescriptorWithoutDefaultConstructor<T>` on all 34 rows of the first table and a `PClassDescriptorConcrete<T>` on all 5 of the second |
| `constructor` | the function the initialiser calls on the descriptor |
| `teardown` | the function passed to `atexit` |

### Columns of phyre-reflection-guarded-class-registration-stubs.tsv

One row per registrar, 99 rows in address order. Each body calls `_Init_thread_header` (`0x008092FC`),
`_Init_thread_footer` (`0x0080929C`) and `atexit` (`0x00808B90`).

| Column | Holds |
|---|---|
| `entry` | the registrar's entry address |
| `size` | the body length in bytes, from 129 to 3,757 |
| `call_targets` | every function the body calls or jumps to other than those three, in address order and separated by commas; 1 to 14 per row |
| `guarded_callees` | the functions of `call_targets` whose own bodies call `_Init_thread_header`, separated by commas; `-` on the 23 rows with no such callee |

### Columns of phyre-reflection-pclassdescriptor-deleting-destructors-map.tsv

One row per deleting destructor, 1,149 rows in address order: the 1,148 of
`phyre-reflection-pclassdescriptor-deleting-destructors.tsv` and `0x005D2630`, a body of the same 92-byte form.

| Column | Holds |
|---|---|
| `entry` | the destructor's entry address |
| `vtable` | the vtable it stores at `[rcx]` before it calls the base destructor; 400 distinct values |
| `base_destructor` | the base destructor it calls: `0x00633390` on every row |

### Per-class field accesses

Each file lists the instructions that read or write a field of one class: function, site,
displacement, read or write, and where the object pointer comes from.

| Class | File | Rows |
|---|---|---:|
| `PApplicationViewport` | [phyre-reflection-census-papplication-viewport-accesses.tsv](phyre-reflection-census-papplication-viewport-accesses.tsv) | 6 |
| `PAssetReferenceImport` | [phyre-reflection-census-passet-reference-import-accesses.tsv](phyre-reflection-census-passet-reference-import-accesses.tsv) | 3 |
| `PAsyncProcessHeader` | [phyre-reflection-census-pasync-process-header-accesses.tsv](phyre-reflection-census-pasync-process-header-accesses.tsv) | 5 |
| `PBitmapFontCharInfo` | [phyre-reflection-census-pbitmap-font-char-info-accesses.tsv](phyre-reflection-census-pbitmap-font-char-info-accesses.tsv) | 7 |
| `PClassDescriptorDynamic` | [phyre-reflection-census-pclass-descriptor-dynamic-accesses.tsv](phyre-reflection-census-pclass-descriptor-dynamic-accesses.tsv) | 177 |
| `PConstantBufferBase` | [phyre-reflection-census-pconstant-buffer-base-accesses.tsv](phyre-reflection-census-pconstant-buffer-base-accesses.tsv) | 2 |
| `PConstantBufferD3D11` | [phyre-reflection-census-pconstant-buffer-d3d11-accesses.tsv](phyre-reflection-census-pconstant-buffer-d3d11-accesses.tsv) | 12 |
| `PDataBlockBase` | [phyre-reflection-census-pdata-block-base-accesses.tsv](phyre-reflection-census-pdata-block-base-accesses.tsv) | 5 |
| `PDataBlockBufferD3D11` | [phyre-reflection-census-pdata-block-buffer-d3d11-accesses.tsv](phyre-reflection-census-pdata-block-buffer-d3d11-accesses.tsv) | 6 |
| `PDataBlockD3D11` | [phyre-reflection-census-pdata-block-d3d11-accesses.tsv](phyre-reflection-census-pdata-block-d3d11-accesses.tsv) | 24 |
| `PDebugUtils` | [phyre-reflection-census-pdebug-utils-accesses.tsv](phyre-reflection-census-pdebug-utils-accesses.tsv) | 4 |
| `PDynamicMesh` | [phyre-reflection-census-pdynamic-mesh-accesses.tsv](phyre-reflection-census-pdynamic-mesh-accesses.tsv) | 12 |
| `PDynamicMeshInstance` | [phyre-reflection-census-pdynamic-mesh-instance-accesses.tsv](phyre-reflection-census-pdynamic-mesh-instance-accesses.tsv) | 1 |
| `PEntity` | [phyre-reflection-census-pentity-accesses.tsv](phyre-reflection-census-pentity-accesses.tsv) | 7 |
| `PIndexDataBlockBase` | [phyre-reflection-census-pindex-data-block-base-accesses.tsv](phyre-reflection-census-pindex-data-block-base-accesses.tsv) | 5 |
| `PIndexDataBlockBufferD3D11` | [phyre-reflection-census-pindex-data-block-buffer-d3d11-accesses.tsv](phyre-reflection-census-pindex-data-block-buffer-d3d11-accesses.tsv) | 6 |
| `PIndexDataBlockD3D11` | [phyre-reflection-census-pindex-data-block-d3d11-accesses.tsv](phyre-reflection-census-pindex-data-block-d3d11-accesses.tsv) | 24 |
| `PIndirectArgsBufferBase` | [phyre-reflection-census-pindirect-args-buffer-base-accesses.tsv](phyre-reflection-census-pindirect-args-buffer-base-accesses.tsv) | 2 |
| `PIndirectArgsBufferD3D11` | [phyre-reflection-census-pindirect-args-buffer-d3d11-accesses.tsv](phyre-reflection-census-pindirect-args-buffer-d3d11-accesses.tsv) | 6 |
| `PInputAction` | [phyre-reflection-census-pinput-action-accesses.tsv](phyre-reflection-census-pinput-action-accesses.tsv) | 15 |
| `PInputMap` | [phyre-reflection-census-pinput-map-accesses.tsv](phyre-reflection-census-pinput-map-accesses.tsv) | 3 |
| `PInputMapper` | [phyre-reflection-census-pinput-mapper-accesses.tsv](phyre-reflection-census-pinput-mapper-accesses.tsv) | 125 |
| `PInputSource` | [phyre-reflection-census-pinput-source-accesses.tsv](phyre-reflection-census-pinput-source-accesses.tsv) | 1 |
| `PInputSourceJoypadAxis` | [phyre-reflection-census-pinput-source-joypad-axis-accesses.tsv](phyre-reflection-census-pinput-source-joypad-axis-accesses.tsv) | 8 |
| `PInputSourceMouseButton` | [phyre-reflection-census-pinput-source-mouse-button-accesses.tsv](phyre-reflection-census-pinput-source-mouse-button-accesses.tsv) | 10 |
| `PLODGroup` | [phyre-reflection-census-plodgroup-accesses.tsv](phyre-reflection-census-plodgroup-accesses.tsv) | 16 |
| `PLODLevel` | [phyre-reflection-census-plodlevel-accesses.tsv](phyre-reflection-census-plodlevel-accesses.tsv) | 8 |
| `PMaterialSet` | [phyre-reflection-census-pmaterial-set-accesses.tsv](phyre-reflection-census-pmaterial-set-accesses.tsv) | 2 |
| `PMeshInstanceBounds` | [phyre-reflection-census-pmesh-instance-bounds-accesses.tsv](phyre-reflection-census-pmesh-instance-bounds-accesses.tsv) | 6 |
| `PMeshInstanceSegmentContext` | [phyre-reflection-census-pmesh-instance-segment-context-accesses.tsv](phyre-reflection-census-pmesh-instance-segment-context-accesses.tsv) | 9 |
| `PMeshInstanceSegmentStreamBinding` | [phyre-reflection-census-pmesh-instance-segment-stream-binding-accesses.tsv](phyre-reflection-census-pmesh-instance-segment-stream-binding-accesses.tsv) | 3 |
| `PMeshParticleSystemBase` | [phyre-reflection-census-pmesh-particle-system-base-accesses.tsv](phyre-reflection-census-pmesh-particle-system-base-accesses.tsv) | 40 |
| `PMeshSegmentBase` | [phyre-reflection-census-pmesh-segment-base-accesses.tsv](phyre-reflection-census-pmesh-segment-base-accesses.tsv) | 8 |
| `PMeshSegmentContext` | [phyre-reflection-census-pmesh-segment-context-accesses.tsv](phyre-reflection-census-pmesh-segment-context-accesses.tsv) | 5 |
| `PModifierNetwork` | [phyre-reflection-census-pmodifier-network-accesses.tsv](phyre-reflection-census-pmodifier-network-accesses.tsv) | 14 |
| `PModifierNetworkDynamicMesh` | [phyre-reflection-census-pmodifier-network-dynamic-mesh-accesses.tsv](phyre-reflection-census-pmodifier-network-dynamic-mesh-accesses.tsv) | 36 |
| `PModifierNetworkDynamicMeshInstance` | [phyre-reflection-census-pmodifier-network-dynamic-mesh-instance-accesses.tsv](phyre-reflection-census-pmodifier-network-dynamic-mesh-instance-accesses.tsv) | 10 |
| `PModifierNetworkDynamicMeshSegment` | [phyre-reflection-census-pmodifier-network-dynamic-mesh-segment-accesses.tsv](phyre-reflection-census-pmodifier-network-dynamic-mesh-segment-accesses.tsv) | 3 |
| `PModifierNetworkInfoPacketModifierCode` | [phyre-reflection-census-pmodifier-network-info-packet-modifier-code-accesses.tsv](phyre-reflection-census-pmodifier-network-info-packet-modifier-code-accesses.tsv) | 4 |
| `PModifierNetworkInstanceInput` | [phyre-reflection-census-pmodifier-network-instance-input-accesses.tsv](phyre-reflection-census-pmodifier-network-instance-input-accesses.tsv) | 4 |
| `PSamplerStateBase` | [phyre-reflection-census-psampler-state-base-accesses.tsv](phyre-reflection-census-psampler-state-base-accesses.tsv) | 6 |
| `PSceneRenderPass` | [phyre-reflection-census-pscene-render-pass-accesses.tsv](phyre-reflection-census-pscene-render-pass-accesses.tsv) | 10 |
| `PSceneWideParameterBuffer` | [phyre-reflection-census-pscene-wide-parameter-buffer-accesses.tsv](phyre-reflection-census-pscene-wide-parameter-buffer-accesses.tsv) | 2 |
| `PScheduler` | [phyre-reflection-census-pscheduler-accesses.tsv](phyre-reflection-census-pscheduler-accesses.tsv) | 90 |
| `PShader` | [phyre-reflection-census-pshader-accesses.tsv](phyre-reflection-census-pshader-accesses.tsv) | 8 |
| `PShaderParameterCaptureBufferLocationType` | [phyre-reflection-census-pshader-parameter-capture-buffer-location-type-accesses.tsv](phyre-reflection-census-pshader-parameter-capture-buffer-location-type-accesses.tsv) | 2 |
| `PShaderParameterCaptureBufferLocationTypeConstantBuffer` | [phyre-reflection-census-pshader-parameter-capture-buffer-location-type-constant-buffer-accesses.tsv](phyre-reflection-census-pshader-parameter-capture-buffer-location-type-constant-buffer-accesses.tsv) | 3 |
| `PShaderParameterCaptureBufferStream` | [phyre-reflection-census-pshader-parameter-capture-buffer-stream-accesses.tsv](phyre-reflection-census-pshader-parameter-capture-buffer-stream-accesses.tsv) | 3 |
| `PShaderParameterDefinition` | [phyre-reflection-census-pshader-parameter-definition-accesses.tsv](phyre-reflection-census-pshader-parameter-definition-accesses.tsv) | 3 |
| `PShadowRenderer` | [phyre-reflection-census-pshadow-renderer-accesses.tsv](phyre-reflection-census-pshadow-renderer-accesses.tsv) | 2 |
| `PShadowSplit` | [phyre-reflection-census-pshadow-split-accesses.tsv](phyre-reflection-census-pshadow-split-accesses.tsv) | 5 |
| `PShape` | [phyre-reflection-census-pshape-accesses.tsv](phyre-reflection-census-pshape-accesses.tsv) | 7 |
| `PStreamInputDescD3D11` | [phyre-reflection-census-pstream-input-desc-d3d11-accesses.tsv](phyre-reflection-census-pstream-input-desc-d3d11-accesses.tsv) | 4 |
| `PStructuredBufferBase` | [phyre-reflection-census-pstructured-buffer-base-accesses.tsv](phyre-reflection-census-pstructured-buffer-base-accesses.tsv) | 3 |
| `PStructuredBufferD3D11` | [phyre-reflection-census-pstructured-buffer-d3d11-accesses.tsv](phyre-reflection-census-pstructured-buffer-d3d11-accesses.tsv) | 23 |
| `PTexture3DBase` | [phyre-reflection-census-ptexture3d-base-accesses.tsv](phyre-reflection-census-ptexture3d-base-accesses.tsv) | 8 |
| `PTextureCommonBase` | [phyre-reflection-census-ptexture-common-base-accesses.tsv](phyre-reflection-census-ptexture-common-base-accesses.tsv) | 6 |
| `PTextureCubeMapBase` | [phyre-reflection-census-ptexture-cube-map-base-accesses.tsv](phyre-reflection-census-ptexture-cube-map-base-accesses.tsv) | 7 |
| `PTimeIntervalController` | [phyre-reflection-census-ptime-interval-controller-accesses.tsv](phyre-reflection-census-ptime-interval-controller-accesses.tsv) | 6 |
| `PTrigger` | [phyre-reflection-census-ptrigger-accesses.tsv](phyre-reflection-census-ptrigger-accesses.tsv) | 16 |
| `PTriggerReceiverComponent` | [phyre-reflection-census-ptrigger-receiver-component-accesses.tsv](phyre-reflection-census-ptrigger-receiver-component-accesses.tsv) | 11 |
| `PUtility` | [phyre-reflection-census-putility-accesses.tsv](phyre-reflection-census-putility-accesses.tsv) | 3 |
| `PVertexStream` | [phyre-reflection-census-pvertex-stream-accesses.tsv](phyre-reflection-census-pvertex-stream-accesses.tsv) | 3 |

## Operations

- **Find a class by name.** `0x0063BA10(namespace, name)`; the default namespace is `0x006373D0()`.
- **Find a type by name.** Hash as in `0x006388C0` and walk the tree at `0x01F2E780` with `0x006311D0`.
- **Type-tree lookup.** `0x006311D0(header, key)` takes a key of the hash (`u32` at `+0x00`) and the name pointer
  (`+0x08`). It starts at the header's `+0x18` and returns 0 for an empty tree (`0x006311E2`). At each descriptor it
  compares the hash `+0x20` first and, on an equal hash, the name `+0x28` byte for byte (`0x0063120B`-`0x00631245`);
  a match returns the descriptor, which is the link that reached it less 8 (`0x00631278`-`0x0063127D`).
- **Type-tree descent.** In `0x006311D0` a result of 1 (`node hash > key hash`, or on equal hashes
  `key name > node name` at the first differing byte) follows the descriptor's `+0x08` link and -1 follows
  `+0x10` (`0x0063124C`-`0x00631250`); reaching the header returns 0 (`0x0063126B`-`0x00631270`).
- **Find a member.** `0x00597220(descriptor, name)` searches the class, then its ancestors. It walks the list `+0x80`
  of each descriptor up the `+0x78` chain and returns the first member record whose name `+0x20` matches byte for
  byte, skipping members without a name; it returns 0 for a null descriptor or name (`0x0059722B`, `0x00597233`) and
  when no member matches.
- **Create instances.** `0x0063A990(cluster, count, descriptor, …)`; `0x0063C910(descriptor, object)`
  initialises one object from the default instance.
- **Visit members.** Descriptor slot `+0x00` walks every member of the class and its ancestors.

## State

| Address | What |
|---|---|
| `0x02CF8260` | next descriptor index |
| `0x01F2E330` | default namespace |
| `0x01F2E780` | type-tree header |
| `0x02CF8270` | `PBase`, the root descriptor |
| `0x02CF8470` | the descriptor of `PClassDescriptor` |
| `0x02CF8570` | the `WriteMask` annotation key |

### Registration statics

The descriptors, member records, type objects and lists that registration builds are static objects.
[phyre-reflection-state.tsv](phyre-reflection-state.tsv) gives each of their fields that code writes
directly: the object, the class, the field, its type, its start value in the file, its meaning, and every
instruction that writes or reads it, as `function (site, value)`. A `-` under `read_by` means that no
RIP-relative, image-base-relative or disp32 reference names the field.

The `family` column groups the rows:

| Family | Globals | What |
|---|---:|---|
| `class-flags` | 318 | the `+0xFC` flags of the descriptors that initialisers and registrars build |
| `array-getter` | 698 | the fields that the 69 array-type descriptor getters write |
| `data-member` | 354 | member records: the registrars' vtable and attribute stores, and the core records built inline |
| `callable` | 873 | the method and script-function records and their caller objects |
| `builtin-type` | 130 | the 13 built-in type objects |
| `enum-type` | 44 | the 4 enum type objects built on first use |
| `core-descriptor` | 90 | the fields of the 10 core descriptors that their own code writes |
| `members-registered` | 15 | the bytes that mark a class's members as registered |
| `header-handler` | 4 | the handler at `+0x100` of the header descriptors |
| `named-semantic` | 3 | the list of named-semantic descriptors and two of their vtables |
| `named-registry` | 4 | the registries of named light, shadow-caster, LOD-blend and trigger objects |
| `named-type` | 23 | the light and shadow-caster type objects and the other named values registered by name |
| `default-namespace` | 6 | the fields of the default namespace `0x01F2E330` |
| `type-tree` | 5 | the link words of the type-tree header `0x01F2E780` |

### Class flags

Each row of `class-flags` is the flags word of one descriptor. Its constructor clears the word and its own
code sets bits; the code listed in Layouts (`+0xFC flags`) adds the rest at run time. The rows split by
the value the class's own code leaves:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `+0xFC` of each of 240 `class-flags` descriptors whose meaning ends "leaves it at 0x0" | `u32` | 0 | concrete class: the constructor sets bit `0x2`, the initialiser clears it | the initialiser (`and`, site per row); through the descriptor, the class's constructor (`or 2`) and `0x00632D80` (`0x00632E69`) or `0x00632C90` (`0x00632D6A`, an 8-byte store from `+0xF8`) | - |
| `+0xFC` of each of 33 descriptors left at `0x8` | `u32` | 0 | no default constructor: the initialiser clears bit `0x2` and sets bit `0x8` in one read-modify-write | as above | the initialiser's own load (site per row) |
| `+0xFC` of each of 29 descriptors left at `0x20` | `u32` | 0 | bit `0x20` set by the class's member registrar, or by the getter of a `PClassDescriptorWrapper<T>` class, after it registers the members | the initialiser and the registrar (sites per row) | - |
| `0x02CB757C` | `u32` | 0 | `PParameterBuffer` (`PClassDescriptorHeaderWithoutDefaultConstructor`): the initialiser `0x001615C0` clears bit `0x2` and sets bits `0x4` and `0x8` (`0x001615FF`); `0x00639780` tests bit `0x4` (`0x006397C0`) | `0x001615C0` (`0x001615FF`); through the descriptor, `0x005D9B30` (`0x005D9B8A`, bit `0x2`), `0x00632D80` (`0x00632E69`, 0) | `0x001615C0` (`0x001615F3`) |
| `+0xFC` of the 3 header descriptors `0x02CADC3C` (`PAnimationClipBinding`), `0x02E5E52C` (`PModifierNetworkInfoPacket`) and `0x02EA094C` (`POccluderGeometryObject`), left at `0x14` | `u32` | 0 | header class (`PClassDescriptorHeader`): the initialiser clears bits `0x2` and `0x8` and sets bit `0x4` in one read-modify-write; the class's registrar sets bit `0x10` right after `0x006388C0` registers the descriptor | the initialiser (`0x001605C0` at `0x00160602`, `0x00167DB0` at `0x00167DF2`, `0x001688F0` at `0x00168932`) and the registrar (`0x005B0700` at `0x005B0720`, `0x006D1810` at `0x006D1830`, `0x006D9FC0` at `0x006D9FE0`); through the descriptor, the class's constructor (`or 2`) and `0x00632D80` (`0x00632E69`) | the initialiser's own load (`0x001605E5`, `0x00167DD5`, `0x00168915`) |
| `0x02CB747C` | `u32` | 0 | `PParameterBufferBase` (`PClassDescriptorAbstract`), left at `0x22`: no initialiser clears the abstract bit `0x2` that its constructor sets; the registrar `0x005E6E70` sets bit `0x20` (`0x005E6E89`) | `0x005E6E70` (`0x005E6E89`); through the descriptor, `0x005D9BD0` (`0x005D9C30`, bit `0x2`), `0x00632D80` (`0x00632E69`, 0) | - |
| `0x02CB9DFC` | `u32` | 0 | `PShaderParameterCaptureBufferTextureBase` (`PClassDescriptorWithoutDefaultConstructor`), left at `0x28`: the initialiser `0x00161C90` clears bit `0x2` and sets bit `0x8` (`0x00161CC1`), the registrar `0x005E9350` sets bit `0x20` (`0x005E9370`) | `0x00161C90` (`0x00161CC1`), `0x005E9350` (`0x005E9370`); through the descriptor, `0x005DAD20` (`0x005DAD80`, bit `0x2`), `0x00632D80` (`0x00632E69`, 0) | `0x00161C90` (`0x00161CB5`) |
| `+0xFC` of the 10 core descriptors (`0x02CF836C`, `0x02CF846C`, `0x02CF856C`, `0x02CF867C`, `0x02CF877C`, `0x02CF887C`, `0x02CF897C`, `0x02CF8A7C`, `0x02CF8B7C`, `0x02CF962C`) | `u32` | 0 | the core registrars set bit `0x40000000` themselves, as `0x00639450` does for other classes | per row | per row |

The 69 array-type descriptors are in `array-getter`: each getter sets bit `0x2` while it builds the descriptor
and clears it after installing the Concrete vtable.

A getter keeps its class name in a static of its own and fills it from the first caller that passes a name. For
`PArray<PUInt32>` the getter `0x005B4E00` builds the descriptor `0x02CB3B50` with the name in `0x02CB5BC8` (`0x005B4E78`,
`0x005B4E9D`), 0 on the first call; once a caller passes a name while the descriptor's name `0x02CB3B80` is 0, it stores
that name in both (`0x005B4F31`, `0x005B4F3F`, `0x005B4F46`).

`0x005B1D90` passes `[0x01F2D110]` (`0x005B1DB5`), which the image points at the text `PArray<PUInt32>` (`0x00D329D8`); the
calls at `0x005B1DFF`, `0x005B82DC`, `0x005B82EE`, `0x005BB255`, `0x005C7982`, `0x005C7E32`, `0x005CACA0` and `0x005CACBB` give no
name.

All 69 getters are named this way. 682 direct calls reach them, not one by a jump, and no RIP-relative address form
or 8-byte pointer in the image names a getter. 98 of the calls load the name from an image pointer to a static
string, the other 584 give no name, and no getter receives two different names.

The 69 names, each with one call that passes it, are in
[phyre-reflection-array-type-names.tsv](phyre-reflection-array-type-names.tsv), and the 69 rows of
[phyre-reflection-phyre-class-default-buffers.tsv](phyre-reflection-phyre-class-default-buffers.tsv) carry them.
Each getter passes the instance size to `0x00632D80` from a register it zeroes, as `0x005B4E00` does (`0x005B4E3E`,
`0x005B4E99`): `0x10`, or `0x50` for `PSharray<PDataBlockBufferD3D11>` and `PSharray<PIndexDataBlockBufferD3D11>`.

Every instruction in the game that writes or reads a descriptor's `+0xFC` is a row of
[phyre-reflection-class-flag-sites.tsv](phyre-reflection-class-flag-sites.tsv): 1006 rows, one per bit and access.
926 instructions touch the word: 380 through a pointer and 546 at a descriptor's static address. Nothing
reads the whole word: every load ends in a bit test, a sign test, a bit extraction or a store back. By bit:

| Bit | Meaning | Written by | Read by |
|---|---|---|---|
| `0x1` | dynamic class | `0x00632E80` (`0x00632F18`) | 21 sites: `0x00633790`, `0x006361C0`, `0x00636280`, `0x00637320`, `0x00637350`, `0x00639450`, `0x00639A60`, `0x0063ABF0`, `0x0063BBC0`, `0x0063C910`, `0x008AF490` (`0x008AF4D6`, through `[0x01F2E340]` - `0x50`), and the 10 core registrars after their `bts` (`0x006344F8` and the same test in the other nine) |
| `0x2` | abstract | set at 393 sites (the 315 class constructors' `or`, the 69 array-type getters and 9 others: `0x00163DB0` (`0x00163DCD`), `0x00163E30` (`0x00163E4D`), `0x00163EA0` (`0x00163EBA`), `0x00163F20` (`0x00163F3A`), `0x00163FA0` (`0x00163FBA`), `0x00164010` (`0x0016402A`), `0x00164090` (`0x001640AD`), `0x00164100` (`0x0016411A`), `0x00635DC0` (`0x00635E38`)); cleared at 373 sites: 303 initialisers, the 69 array-type getters after installing the Concrete vtable, and `0x00635DC0` (`0x00635E38`-`0x00635E7C`) | `0x0059AC00` (`0x0059ACDB`), `0x00639510` (`0x0063954C`), `0x00639A60` (`0x00639AF1`), `0x0063A4C0` (`0x0063A51E`) |
| `0x4` | set by the initialisers of `PParameterBuffer` and the three header descriptors; the PCluster loader tests it per class | `0x001615C0` (`0x001615FF`), `0x001605C0` (`0x00160602`), `0x00167DB0` (`0x00167DF2`) and `0x001688F0` (`0x00168932`) | `0x00639780` (`0x006397C0`) and the PCluster loaders `0x0059C250`, `0x0059C700`, `0x0059CE30`, `0x0059D590`, `0x0059D6A0` (twice), `0x0059D940` and `0x0059F500` |
| `0x8` | no default constructor | set by 39 initialisers (load, clear `0x2`, set `0x8`, store); cleared by the three header-descriptor initialisers `0x001605C0`, `0x00167DB0` and `0x001688F0` as they set `0x4` | `0x0059AC00` (`0x0059ACDB`), `0x00639A60` (`0x00639B2C`), `0x0063A990` (`0x0063A99A`), `0x0063AA50` (`0x0063AA5F`) |
| `0x10` | set for the three header descriptors | `0x005B0700` (`0x005B0720`), `0x006D1810` (`0x006D1830`) and `0x006D9FC0` (`0x006D9FE0`), each right after `0x006388C0` registers the descriptor | `0x0059D940` (`0x0059DCD3`-`0x0059DCDB`), which extracts it: 1 for those three classes, 0 for every other |
| `0x20` | set by the class's registrar or wrapper getter before `0x00639450` registers the members: right after `0x006388C0` registers the descriptor by name in 22 registrars, twice between `0x006388C0` and `0x00639450` in `0x00608A40` (`0x00608AC5`, `0x00608C0F`), after the member record is built in the nine wrapper getters `0x006B0760` to `0x006B33F0` (seven Vectormath types, `PMatrix4` and `PMatrix4x3`), and at entry in PBase's registrar (`0x006344B2`) | 34 sites in 33 functions | read by no instruction |
| `0x08000000` | a member is a PSharray (`0x00639EE2`-`0x00639EEF`), or the parent has the bit (`0x00639D9D`-`0x00639DB0`) | `0x00639C80`: cleared (`0x00639CB4`), set (`0x00639EEF`), and copied from the parent's word (`0x00639D9D`-`0x00639DB0`) | `0x00639C80` (the parent's bit, `0x00639DAB`) |
| `0x10000000` | every instance byte is described by a member | `0x00639C80`: cleared (`0x00639CB4`), set (`0x0063A0E2`) | `0x00639850` (`0x00639868`) |
| `0x20000000` | set by `0x0063BC00`, never tested | `0x0063BC00` (`0x0063BC49`) | no reader |
| `0x40000000` | members registered (`0x00639450`) | set by `0x00636280` (`0x006363E0`), `0x00639450` (`0x00639465`) and the 10 core registrars' `bts` (12 sites); cleared by `0x00638C90` (`0x00638D8D`) | 13 sites in `0x00636280`, `0x00637A70`, `0x00639850`, `0x00639A40`, `0x00639C80` (two), `0x0063A790`, `0x0063BB10`, `0x0063BC00`, `0x0063C1A0`, `0x0063C5E0`, `0x0063C910` (two) |
| `0x80000000` | default instance and masks built | set by `0x00639A60` (`0x00639C55`); cleared by `0x00632E80` (`0x00632F3C`), `0x0063D410` (`0x0063D4DB`) and `0x0063D930` (`0x0063D945`) | 13 sign tests: at the loads of the `0x40000000` readers other than `0x00639A40`, and at `0x00639A60` (`0x00639A94`) |

No instruction writes or reads bits `0x40` to `0x4000000`. The whole word is written as 0 by the 10 core
constructors `0x006316C0`-`0x00632780`, `0x00632C90` (`0x00632D6A`, 8 bytes from `+0xF8`) and `0x00632D80` (`0x00632E69`), and
stored back by the initialisers after they change their bits (43 sites), by the 10 core registrars after their
`bts` (10 sites), and once more by `0x00635DC0` (`0x00635E7C`) after it sets and clears bit `0x2`.

### Array-type descriptor getters

A getter such as `0x005B5130` (`PArray<float, 4>`) builds its descriptor, an `m_count` member, the `WriteMask`
annotation on it and an `m_els` member, each behind its own thread-safe static, then registers the
descriptor (`0x006388C0`, `0x00639450`). Ten of its statics are in `array-getter`:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| descriptor `+0xFC`, 69 rows | `u32` | 0 | flags: bit `0x2` set while the getter builds the descriptor, cleared after the Concrete vtable is installed | the getter (two sites per row); through the descriptor, `0x00632D80` (`0x00632E69`, 0) | - |
| descriptor `+0x30`, 69 rows | `void*` | 0 | the descriptor's name: 0 until the getter is called with a name, then the name static's value | the getter | the getter's test of it |
| name static, 68 rows | `void*` | 0 | the first non-null name the getter is passed; it is also the name the getter passes to `0x00632D80` | the getter (after a `cmove`) | the getter |
| annotation `+0x00`, 69 rows | `void*` | 0 | vtable `0x00D32D50`, `PAnnotationWithValue<unsigned int>` | the getter | - |
| annotation `+0x30`, 69 rows | `u32` | 0 | `0x7FFFFFFF`; `0x00639C80` takes it through the annotation's slot `+0x08` (`0x005C4D20`, `0x0063A05F`) and copies it into the write mask over `m_count`, leaving out bit `0x80000000` | the getter | - |
| `m_els` `+0x00`, 69 rows | `void*` | 0 | the record's `PClassDataMemberArrayDynamic<T>` vtable, installed after `0x00632A10` builds the record | the getter | - |
| `m_els` `+0x28`, 9 rows | `u32` | 0 | attribute bit `0x40` ORed in for a `PSharray<T>` | the getter | - |
| `m_els` `+0x58`, 69 rows | `u32` | 0 | the element type's alignment: 8 in 51 getters, 4 in 12, 2 in 3, 1 in 2 and 16 in 1 | the getter | - |
| `m_els` `+0x60`, 69 rows | `void*` | 0 | `0x005C4CC0`, which returns the array's first word without bit `0x80000000` | the getter | - |
| `m_els` `+0x68`, 69 rows | `void*` | 0 | 0, or `0x00671250` in the 9 `PSharray<T>` getters | the getter | - |
| `m_els` `+0x70`, 69 rows | `void*` | 0 | the set-elements function of the element type (`0x00673130` in 19 getters, `0x006AF760` in 22) | the getter | - |

In all 69 record vtables slot `+0x20` is `0x006065D0`, which calls `+0x60`; slots `+0x30` and `+0x38` are
`0x00604580`, which calls `+0x68` or, when it is 0, reads the pointer stored in the member; slot `+0x40` is
`0x0060F3D0`, which calls `+0x70` with a buffer and a count and returns `0x15` when it is 0. `0x00673130` frees
a buffer the array owns, then stores the new buffer at `+0x08` and the count with bit `0x80000000` set.

### Member records and callables

Member registrars build records with `0x00632960`, `0x00632A10`, `0x00632A70` and `0x00632BE0`. Two of their
stores are direct (`data-member`):

- 49 vtable stores at `+0x00`: the `PClassDataMemberPhyreArray<T>`, `PClassDataMemberPhyreSharray<T>` or
  `PClassDataMemberArrayDynamic<T>` vtable, installed after `0x00632A10` builds the record;
- 44 attribute ORs at `+0x28`: bit `0x10` or `0x08` after the constructor stores the attributes.

The core registrars build their member records inline, field by field, as `0x00632960` would; the owner's
attach slot `+0x40` (`0x0062EFD0` in every core descriptor vtable) then links each record into `+0x80`. Their
rows give every field. The `m_type` member of `PClassDataMemberDynamic` gets a dynamic-type helper at
`0x01F2DF30` and attribute bit `0x4` (`0x00634668`).

A method or script-function record (`callable`) is a `0x30`-byte `PClassMember`: list node `+0x00`/`+0x08`,
owner `+0x10`, name `+0x18`, attributes `+0x20`, and at `+0x28` a pointer to its caller object, which
follows at `+0x30`. A `PMethodCallerConcrete` record is linked into the owner's `+0x90` list, a
`PFunctionCallerConcrete` record into `+0xA0`:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| record `+0x08`, 26 rows | `void*` | 0, or the record's own address | previous-record link: the registrar links the record at the end of the list | the registrar; the exit teardown, which unlinks the record and stores the record's address | the exit teardown |
| record `+0x28`, 49 rows | `void*` | 0 | the caller object's address | the registrar (41 store 0 first) | - |
| caller `+0x00`, 49 rows | `void*` | 0 | the caller's vtable | the registrar | - |
| caller `+0x08`, 49 rows | `void*` or `u8[16]` | 0 | the function called: 8 bytes for a function, or a 16-byte member-function pointer with a 0 adjustment at `+0x10` in 9 records | the registrar | - |

For `PFunctionCallerConcrete<float>` (`0x00D34C08`) slots `+0x08` (`0x005C1350`) and `+0x10` (`0x005CBCC0`) call
through `+0x08`.

### Built-in and enum types

The built-in types `PType`, `bool`, `PChar`, `PUInt8`, `PInt16`, `PUInt16`, `PInt32`, `PUInt32`, `PUInt64`,
`PInt64`, `float`, `double` and `PUInt128` are static `PType` objects at `0x01F2E370`-`0x01F2E780`. The file
already holds their fields. `0x00637F20`, which registers every one of them by name with `0x006388C0`, stores
them again behind each type's guard; seven of them are also built by other functions (`0x00637720` for `PType`;
`0x006315B0` and `0x00637650` for `PUInt32`), as each row lists.

The enum types `Phyre::PResult` (`0x02CB07A0`, getter `0x005A6670`), `PSamplerStateFilterFormatType`
(`0x02CC02D0`, `0x005D8CA0`), `PSamplerStateWrapFormatType` (`0x02CC0330`, `0x005D8D70`) and `PCollisionGroup`
(`0x02E4A0D0`, `0x0068F0F0`) are `PTypeDefault<unsigned int>` objects of size 4 built on first use; their exit
teardowns put back the `PType` vtable `0x00D31168`.

In both families the three tree links point at the object's own `+0x08` and the hash and key are 0;
`0x006388C0` sets them when it registers a type.

### Core descriptors and the default namespace

The core descriptors `PBase` (`0x02CF8270`), `PClassDataMemberDynamic`, `PClassDescriptor`,
`PClassDescriptorDynamic`, `PClassMember`, `PCluster`, `PClusterDependencyList`, `PNamespace`, `PWorld`
(`0x02CF8370`-`0x02CF8A80`) and `PSharray<PString>` (`0x02CF9530`) are built by their own code. Their rows cover:

- `+0xC0`, `+0xC8`, `+0xD0`: the three static buffers, stored by the initialiser, for `PBase` by its registrar
  `0x006344A0` (`0x006344C0`-`0x006344DC`);
- `+0x08`-`+0x28`: reset by the registrar only when bit `0x1` of `+0xFC` is set (`0x006344F8` and the same test
  in the others), which the class's own code leaves clear;
- `PBase` `+0x38`: `0x006318A0` stores 1 through the descriptor (`0x00631913`), then the initialiser `0x00164180`
  stores 0 (`0x00164197`), installs the vtable `0x00D582D0` at `+0x00` and registers the teardown `0x008AF190` with
  `0x00808B90` (`0x00164190`-`0x001641B3`).

`0x006344A0` is the registrar of `PBase` `0x02CF8270`. It sets bit `0x20` of the flags `0x02CF836C`, stores the
addresses `0x02CF8FA0`, `0x02CF8FA1` and `0x02CF8FA2` at the descriptor's `+0xC0`, `+0xC8` and `+0xD0`, calls
`0x00639160(the qword 0x02CF82E0, 0x02CF8270)` and sets bit `0x40000000`. With bit `0x1` of the flags set it points
the three qwords `0x02CF8278`, `0x02CF8280` and `0x02CF8288` at `0x02CF8278`, clears the dword `0x02CF8290` and the
qword `0x02CF8298` and ends in a jump to `0x006388C0(0x02CF8270)` (`0x006344A4`-`0x00634532`).

The default namespace `0x01F2E330` is built behind guard `0x02CF94EC` by whichever of `0x006316C0`-`0x00632780`,
`0x00637A70`, `0x00638C90` and `0x0063C730` runs first, each storing the same empty lists. Its state word
`0x01F2E350` is set to 1 by `0x00637A70` (`0x00637AB8`) while it computes every class's layout offsets, then to 2
(`0x00637B60`) while it builds every class's default instance and masks; `0x00638C90` clears bit `0x40000000`
of every class and sets it back to 0 (`0x00638DAB`).

### Other registration statics

- `members-registered`: the byte after a getter's guard (`0x02CACDB4` for `PTimer`); the getter stores 1 right
  after `0x00639450` and skips the member registration while it is set.
- `header-handler`: `+0x100` of the header descriptors `PAnimationClipBinding`, `PParameterBuffer`,
  `PModifierNetworkInfoPacket` and `POccluderGeometryObject`; slot `+0x78` of each descriptor jumps to it.
- `named-semantic`: `0x01F2EBB8` heads the list of every `PNamedSemanticDescriptor`; `0x006B6820` links each new
  descriptor's `+0x50` node at the front.
- `named-registry`: `0x02E58CA0` (`PLightType`), `0x02E59BB8` (`PShadowCasterType`) and `0x02EA0748`
  (`PLODBlendType`) head lists linked through `+0x10` and keyed by the name at `+0x08`. `0x006BFC60`,
  `0x006C2380` and `0x006D9A70` add an object at the front; they return `0x12` for a name already present
  and `0x11` for an object with no name.
- `type-tree`: the link words `0x01F2E788`-`0x01F2E7A8` of the header `0x01F2E780`; `0x00636280` and `0x00638F00` set
  them to the header's address, an empty tree, behind guard `0x02CF9524`.

The `PLOD` enumerations register their values in two named registries. `0x006D9680` adds a `PLODMetricType` (vtable
`0x00D8DCA8`) to the list `0x02EA06D8`, and the initialisers `0x00168850`, `0x00168870` and `0x00168890` register
`DistanceToBoundBox` (`0x01F323A8`), `DistanceToNode` (`0x01F32390`) and `ScreenSize` (`0x01F323C0`) through it.

`0x001688B0` and `0x001688D0` register the `PLODBlendType` (vtable `0x00D8DD88`) values `Distance` (`0x01F323D8`) and `Time`
(`0x01F323F0`) through `0x006D9A70` into `0x02EA0748`. Each record holds its vtable at `+0x00`, its name at `+0x08` and the list
link at `+0x10`; the teardowns `0x008B76B0`, `0x008B7710`, `0x008B7770`, `0x008B77E0` and `0x008B7840` unlink them at exit.

### More method and script-function records

The `callable` and `data-member` families also hold the records that 22 more member registrars build, from
`PTimer` (`0x005A02D0`) to `PInputAction` (`0x0086D670`): 134 records, 125 in a method list and 9 in a script-function
list, each row with the same fields and wording as above. Their registrars:

| Class | Registrar | Records |
|---|---|---:|
| `PAnimatableComponent` | `0x005AD8F0` | 23 |
| `PAnimationClip` | `0x005AFBC0` | 10 |
| `PAnimationSet` | `0x005B1900` | 3 |
| `PApplication` | `0x007943E0` | 13 |
| `PApplicationViewport` | `0x00794E80` | 5 |
| `PAssetReference` | `0x00675740` | 5 |
| `PDebugUtils` | `0x00795320` | 2 |
| `PEntity` | `0x006AB7E0` | 7 |
| `PInputAction` | `0x0086D670` | 2 |
| `PInputMapper` | `0x00795590` | 2 |
| `PInstancesComponent` | `0x006AE350` | 4 |
| `PMaterialSet` | `0x00666550` | 3 |
| `PNode` | `0x006B41A0` | 14 |
| `PPhysicsRigidBody` | `0x00695AB0` | 12 |
| `PPhysicsWorld` | `0x00697AC0` | 8 |
| `PPostEffectManager` | `0x006491B0` | 5 |
| `PRandomGenerator` | `0x006B04B0` | 1 |
| `PScheduler` | `0x00681F30` | 4 |
| `PTimer` | `0x005A02D0` | 1 |
| `PWorldMatrix` | `0x0067E6C0` | 4 |
| `Quat` | `0x006B0EC0` | 4 |
| `Vector2` | `0x006B1320` | 2 |

For the 105 records whose caller fields have rows, the registrar stores 0 in the record's `+0x28` right after
`0x00632FB0` builds it, and the caller object's address once the caller is built. Of these caller objects, 44 hold a 16-byte member-function pointer and
61 an 8-byte function. The `data-member` rows add the vtable and attribute stores of `m_animationClips`
(`PAnimatableComponent`), `m_channels` and `m_constantChannels` (`PAnimationClip`) and `m_postEffects`
(`PPostEffectManager`).

### Method and member records of 40 more registrars

The `callable` family also holds the method records of 14 more registrars, all in a method list (`+0x90`): 62
previous-record links (`+0x08`) and, for 63 records, the caller pointer `+0x28`, the caller's vtable and the
function it calls, 8 bytes in 59 records and a 16-byte member-function pointer in 4. The registrar stores 0 in
`+0x28` right after `0x00632FB0` builds the record and the caller object's address once the caller is built.
`POccluderGeometryInstance::getLocalToWorldMatrix` is the one record of the 63 whose link is among the rows
above.

| Class | Registrar | Records |
|---|---|---:|
| `PAnimationChannelTarget` | `0x005AF3B0` | 4 |
| `PCamera` | `0x006784E0` | 1 |
| `PComponent` | `0x006AAA80` | 2 |
| `PLODGroup` | `0x006C5A50` | 2 |
| `PLight` | `0x006BED60` | 10 |
| `PMaterial` | `0x005E4AA0` | 7 |
| `PMeshInstance` | `0x005E5400` | 8 |
| `POccluderGeometryInstance` | `0x006C8310` | 1 |
| `PPhysicsCharacterCamera` | `0x00694260` | 4 |
| `PPhysicsCharacterControllerBase` | `0x006949A0` | 2 |
| `PPhysicsRigidBodyBase` | `0x00696470` | 6 |
| `PSamplerStateBase` | `0x005E7070` | 11 |
| `PTextureCommonBase` | `0x005EAF40` | 1 |
| `PTrigger` | `0x006A7EE0` | 4 |

The `data-member` family adds the direct stores of the member registrars of 30 more classes (four of them,
`0x005E5400`, `0x00696470`, `0x006A7EE0` and `0x006C5A50`, also build method records above), from
`PAnimationChannel` (`0x005AF0A0`) to `PTrigger` (`0x006A7EE0`): 43 vtable stores at `+0x00` (38
`PClassDataMemberPhyreArray<T>`, 5 `PClassDataMemberPhyreSharray<T>`), each after `0x00632A10` builds the record,
and 39 attribute ORs at `+0x28` (bit `0x10` in 28, bit `0x08` in 11) after the constructor stores the
attributes.

`members-registered` adds the guard bytes of the descriptor getters of `CD3D11_RASTERIZER_DESC`
(`0x02CF53C4`, stored at `0x0061438D` by `0x00613E80`), `CD3D11_DEPTH_STENCIL_DESC` (`0x02CF5B84`, `0x00613E5F`,
`0x00613A30`) and `D3D11_RENDER_TARGET_BLEND_DESC` (`0x02CF5FB4`, `0x00614A6B`, `0x00614640`), each right after the
getter's `call 0x00639450`.

### Light and shadow-caster types

`PLightType` and `PShadowCasterType` objects are `0x20`-byte named values: vtable `+0x00`, name `+0x08`, registry
link `+0x10`, mask `+0x18`, index `+0x1C`. Each of the eight static objects has an initialiser that registers it
(`0x006BFC60` or `0x006C2380`) and, when that succeeds, sets its mask and index and stores it in its type's index table.
The rows are family `named-type`.

| Object | Name | Mask | Index | Initialiser | Exit teardown |
|---|---|---|---:|---|---|
| `0x01F2ED48` | `PointLight` | `0x1` | 0 | `0x001674B0` | `0x008B6000` |
| `0x01F2ED68` | `DirectionalLight` | `0x2` | 1 | `0x00167450` | `0x008B5F60` |
| `0x01F2ED88` | `AmbientLight` | `0x4` | 2 | `0x001673F0` | `0x008B5EC0` |
| `0x01F2EDA8` | `SpotLight` | `0x8` | 3 | `0x00167500` | `0x008B60A0` |
| `0x01F2EDC8` | `NoShadow` | `0x1` | 0 | `0x001676A0` | `0x008B6730` |
| `0x01F2EDE8` | `PCFShadowMap` | `0x2` | 1 | `0x001676F0` | `0x008B67D0` |
| `0x01F2EE08` | `CascadedShadowMap` | `0x4` | 2 | `0x001675E0` | `0x008B65F0` |
| `0x01F2EE28` | `CombinedCascadedShadowMap` | `0x8` | 3 | `0x00167640` | `0x008B6690` |

The index tables are `0x02E58CB0` (light types) and `0x02E59BC0` (shadow-caster types), 32 slots each. `0x006BFC40` and
`0x006C2300` return slot *i* for *i* below `0x20` and 0 otherwise; their one caller, `0x006B9630`, takes each type's
name (`+0x08`) for the `-DLIGHTTYPE_<i>=` and `-DSHADOWTYPE_<i>=` defines. `0x006B9120` tests a type's mask against
the effect's words and packs its index. `0x006B9CF0` copies an effect's supported light types (`+0x28`) and
shadow-caster types (`+0x38`), sorts the light types by mask with the comparator `0x006B8D10` and packs the same
index pairs.

The exit teardown, and the destructor `0x006BEC40` or `0x006C0FE0` (reached from slot 0 of the vtable `0x00D82F28` or
`0x00D83B60`), puts back the class vtable. When the mask is not 0 it unlinks the object from its registry and stores
0 in its index table at the object's index.

### Trigger types

`0x02E5C210` heads the registry of named `PTriggerType` values (family `named-registry`). Its records hold a name at
`+0x00`, the next record at `+0x08` and at `+0x10` a flag, 1 for a record taken from the pool. `0x006CD4F0` puts a record at the front; it returns
`0x11` for a record with no name and `0x12` for a name already present.

- `0x00167C50` registers the static record `0x01F31F78`, `UnsetTrigger`, and `0x008B6FC0` unlinks it at exit.
- `0x006CD390`, `PNamedSemanticDynamic::FindOrCreateDynamic`, answers null for a null name and finds a name in
  the list `0x02E5C210` with `_stricmp`, returning the record found (`0x006CD39D`-`0x006CD3C7`).
- On a miss it reports through `0x005CDAA0(1, 0x00D4E5C0, name)` and takes a record from the pool `0x02E5C218`
  and a name slot from `0x02E5C240`; an empty pool is grown first with `0x00680150(pool, the dword 0x02E5C234)`
  for the records and `0x00680150(pool, the dword 0x02E5C25C)` for the slots (`0x006CD3DD`-`0x006CD455`).
- With both in hand it copies the name and its terminator with `0x00861EBA`, stores the slot at the record's
  `+0x00`, 0 at `+0x08` and 1 in the byte `+0x10`, and registers the record with `0x006CD4F0`. Without a
  record or without a slot it does none of this and returns the record it has, null or unfilled
  (`0x006CD45C`-`0x006CD4A4`).
- `0x006CD5B0`, slot `+0x50` of `PNamedSemanticDescriptorForDynamicType<PTriggerType>` (`0x00D89F40`, the descriptor
  `0x006CD270` builds at `0x02E5C270`), copies every record's address into an array.

### The per-type table size

The engine set-up `0x005A08E0` calls `0x00638AE0` (`0x005A0AB7`), which walks every class descriptor (the list at
`+0x10` of the object `0x006373D0` returns, linked through `+0x50`), gives every
descriptor its per-type table entry at `+0xEC` (`0x00638C0A`). It stores the number of descriptors it walked. The run
setup `0x0079F150` calls `0x0063C730` (`0x0079F539`), which reads that number and, when the world's per-type table (count
`+0x10`, entries `+0x18`) does not already hold one more than it, gives the table that many `0x20`-byte entries.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CF8264` | `u32` | 0 (zero-filled tail of `.data`) | the number of class descriptors `0x00638AE0` numbered | `0x00638AE0` (`0x00638C40`) | `0x0063C730` (`0x0063C744`) |

`0x0063C730(table)` takes n = the dword `0x02CF8264`. When n + 1 is not the table's count `+0x10` it asks
`0x006343E0(n + 1, the array +0x18, the smaller of n + 1 and the count without its top bit)` for a new
array; a null answer with n + 1 not 0 ends the function with the result `0xD`. It frees the old array with
`0x00584730` when that differs from the new one, is not null and the count's bit `0x80000000` is clear,
then stores the new array and the count n + 1 (`0x0063C744`-`0x0063C7A7`).

`0x006343E0(count, old, keep)` returns null for a count of 0 or when `0x0017D260(count * 0x20, 8)` gives
nothing. It copies the first keep entries of `0x20` bytes from old, and gives each further entry two links
at the entry itself, a null qword `+0x10` and -1 in the dword `+0x18` (`0x006343FE`-`0x00634474`). Whether or
not the array was replaced, `0x0063C730` then links entries 1 to n at the tail of the list headed by entry 0
(`0x0063C7AA`-`0x0063C7E6`).

Once, under the guard `0x02CF94EC`, it makes the default namespace `0x01F2E330`: the two links at
`0x01F2E330` point at it, the links `0x01F2E340` and `0x01F2E348` at `0x01F2E340`, the dword `0x01F2E350` is 0,
the links `0x01F2E358` and `0x01F2E360` point at `0x01F2E358`, and `0x008AF490` is registered with `0x00808B90`
(`0x0063C892`-`0x0063C900`).

It then walks the class list from the qword `0x01F2E340`, each class being its node less `0x50` and the
next node the class's `+0x50`. For a class whose dword `+0xEC` is not negative it counts the links of the
chain through `+0x78` and stores that count in the dword `+0x18` of the entry numbered by `+0xEC`. The
result is 0 (`0x0063C814`-`0x0063C87B`).

### Two `PCameraProjection` script methods

The engine set-up also calls the `PCameraProjection` member registrar `0x006788C0` (`0x005A096E`). After registering
`m_aspect`, it builds two method records, each behind its own thread-safe guard (`0x02D3F760`, `0x02D3F7C0`): `0x00632FB0`
builds the record with its name (`setNearPlane`, `setFarPlane`), and when `0x005A7A40` finds no method of that name
the registrar appends the record to the method list at `+0x90` of the class the record names at `+0x10`. The
record's `+0x00` takes the list's sentinel and `+0x08` the previous last record.

It then stores 0 in the record's
caller pointer `+0x28`, builds the caller object beside the record and points `+0x28` at it.

Each record's exit
teardown (`0x008B1F20`, `0x008B1EC0`, registered at `0x006789FF` and `0x00678AD7`) unlinks it, points both links at the
record itself and frees the name buffer `+0x18` when bit `0x1` of `+0x20` is set.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02D3F718` | `void*` | 0 (zero-filled tail of `.data`) | `setNearPlane` record (`0x02D3F710`) `+0x08`: the record before it in the method list | `0x006788C0` (`0x006789F1`); `0x008B1F20` (`0x008B1F50`, the record's own address) | `0x008B1F20` (`0x008B1F34`) |
| `0x02D3F738` | `void*` | 0 (zero-filled tail of `.data`) | `setNearPlane` record `+0x28`: the caller object `0x02D3F740` | `0x006788C0` (`0x006789BB`, 0; `0x00678A49`, `0x02D3F740`) | callers of the method, through the record |
| `0x02D3F740` | `void*` | 0 (zero-filled tail of `.data`) | the caller object's vtable, `0x00D6CC78` (slots `0x006B4170`, `0x00678F90`) | `0x006788C0` (`0x00678A2F`) | callers of the method, through the record |
| `0x02D3F748` | `u8[16]` | 0 (zero-filled tail of `.data`) | the caller object's member-function pointer: `0x00679120` and 0. `0x00679120` stores its float argument (`xmm1`) at `+0xC0` of the object and jumps to the object's slot 1 | `0x006788C0` (`0x00678A3B`, one 16-byte store) | the caller object's slots, through the object |
| `0x02D3F778` | `void*` | 0 (zero-filled tail of `.data`) | `setFarPlane` record (`0x02D3F770`) `+0x08`: the record before it | `0x006788C0` (`0x00678AC9`); `0x008B1EC0` (`0x008B1EF0`, the record's own address) | `0x008B1EC0` (`0x008B1ED4`) |
| `0x02D3F798` | `void*` | 0 (zero-filled tail of `.data`) | `setFarPlane` record `+0x28`: the caller object `0x02D3F7A0` | `0x006788C0` (`0x00678A93`, 0; `0x00678B1A`, `0x02D3F7A0`) | callers of the method, through the record |
| `0x02D3F7A0` | `void*` | 0 (zero-filled tail of `.data`) | the caller object's vtable, `0x00D6CC78` | `0x006788C0` (`0x00678B00`) | callers of the method, through the record |
| `0x02D3F7A8` | `u8[16]` | 0 (zero-filled tail of `.data`) | the caller object's member-function pointer: `0x00679110` and 0. `0x00679110` stores its float argument at `+0xC4` and jumps to slot 1 | `0x006788C0` (`0x00678B0C`, one 16-byte store) | the caller object's slots, through the object |

### Five `PAssetReference` script callables

The `PAssetReference` member registrar `0x00675740` registers `m_id`, `m_asset` and `m_assetType`, each behind its own
thread-safe guard (`0x00632960` at `0x006757D9`, `0x0067584C`, `0x006758BE`). For `m_asset` it also builds, behind the guard
`0x02D3E9F0`, a dynamic-type helper at `0x02D3E9D0`: `0x00633100` points the helper's `+0x08` at the member record
`0x02D3E910`, sets the member's attribute bit `0x4` and stores the helper's address in the member's `+0x50`
(`0x02D3E960`). The registrar then gives the helper its own vtable and member-function pointer.

Outside the guard, on every call, the registrar stores the helper's address in `0x02D3E960` again (`0x00675954`). At
exit `0x008B1D50` restores the vtable and runs `0x00633770`, which stores the base vtable `0x00D58098` and clears the
member's `+0x50`.

It then builds five records the way the `PCameraProjection` registrar above does: the methods `getID`, `getAsset`
and `getAssetType` in the method list `+0x90` (looked up with `0x005A7A40`), and the script functions
`GetAssetReferenceByAsset` and `GetAssetReferenceByID` in the script-function list `+0xA0` (looked up with
`0x005A0470`). Each record's `+0x28` is set to 0 inside its guarded block. The caller object and the record's pointer
to it are stored after the guard, on every call. The exit teardowns (`0x008B1CE0`, `0x008B1C20`, `0x008B1C80`, `0x008B1B40`,
`0x008B1BA0`) unlink the records as above.

Each of the five unlinks its record the same way and points the record's two qwords at the record itself:
`0x008B1B40` for `0x02D3EB20` (`0x008B1B4D`-`0x008B1B70`), `0x008B1BA0` for `0x02D3EB80` (`0x008B1BAD`-`0x008B1BD0`),
`0x008B1C20` for `0x02D3EA60` (`0x008B1C2D`-`0x008B1C50`), `0x008B1C80` for `0x02D3EAC0` (`0x008B1C8D`-`0x008B1CB0`) and
`0x008B1CE0` for `0x02D3EA00` (`0x008B1CED`-`0x008B1D10`).

Each also frees the record's name, copied into owned storage, through `0x00584730` when bit `0x1` of its
attribute word `+0x20` is set: `0x008B1B40` the pointer the qword `0x02D3EB38` (`+0x18`) holds, under the byte
`0x02D3EB40`; `0x008B1BA0` `0x02D3EB98` under `0x02D3EBA0`; `0x008B1C20` `0x02D3EA78` under `0x02D3EA80`; `0x008B1C80`
`0x02D3EAD8` under `0x02D3EAE0`; and `0x008B1CE0` `0x02D3EA18` under `0x02D3EA20` (`0x008B1B77`-`0x008B1B87`,
`0x008B1BD7`-`0x008B1BE7`, `0x008B1C57`-`0x008B1C67`, `0x008B1CB7`-`0x008B1CC7`, `0x008B1D17`-`0x008B1D27`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02D3E960` | `void*` | 0 (zero-filled tail of `.data`) | `m_asset` member record (`0x02D3E910`) `+0x50`: its dynamic-type helper `0x02D3E9D0` | `0x00633100` (`0x00633116`), through the helper `0x00675740` passes (`0x0067591C`); `0x00675740` (`0x00675954`); `0x00633770`, 0 (`0x0063377E`), at exit through the helper's `+0x08` | users of the member, through the record |
| `0x02D3E9D0` | `void*` | 0 (zero-filled tail of `.data`) | the helper's vtable: `0x00D58098` from `0x00633100`, then `0x00D6C378` (slot 0 `0x00675700`, the helper's destructor) | `0x00633100` (`0x0063310B`), through the helper address `0x00675740` passes; `0x00675740` (`0x00675928`); `0x00675700` (`0x00675713`) and `0x00633770` (`0x00633777`), through the object; `0x008B1D50` (`0x008B1D5E`) | users of the member, through `0x02D3E960` |
| `0x02D3E9E0` | `u8[16]` | 0 (zero-filled tail of `.data`) | the helper's member-function pointer: `0x00677A70` and 0. `0x00677A70` returns the qword at `+0x40` of its object | `0x00675740` (`0x00675934`, one 16-byte store) | the helper's slots, through the object |
| `0x02D3EA28` | `void*` | 0 (zero-filled tail of `.data`) | `getID` record (`0x02D3EA00`) `+0x28`: the caller object `0x02D3EA30` | `0x00675740` (`0x0067599E`, 0; `0x00675A2C`, `0x02D3EA30`) | callers of the method, through the record |
| `0x02D3EA30` | `void*` | 0 (zero-filled tail of `.data`) | the caller object's vtable, `0x00D6C520` (slot 0 `0x006B4170`) | `0x00675740` (`0x00675A12`) | callers of the method, through the record |
| `0x02D3EA38` | `u8[16]` | 0 (zero-filled tail of `.data`) | the caller object's member-function pointer: `0x005C4D20` and 0. `0x005C4D20` returns its object's address plus `0x30` | `0x00675740` (`0x00675A1E`, one 16-byte store) | the caller object's slots, through the object |
| `0x02D3EA88` | `void*` | 0 (zero-filled tail of `.data`) | `getAsset` record (`0x02D3EA60`) `+0x28`: the caller object `0x02D3EA90` | `0x00675740` (`0x00675A76`, 0; `0x00675B04`, `0x02D3EA90`) | callers of the method, through the record |
| `0x02D3EA90` | `void*` | 0 (zero-filled tail of `.data`) | the caller object's vtable, `0x00D6C550` (slot 0 `0x006B4170`) | `0x00675740` (`0x00675AEA`) | callers of the method, through the record |
| `0x02D3EA98` | `u8[16]` | 0 (zero-filled tail of `.data`) | the caller object's member-function pointer: `0x00677A50` and 0. `0x00677A50` copies the qwords at `+0x38` and `+0x40` of its object into its result | `0x00675740` (`0x00675AF6`, one 16-byte store) | the caller object's slots, through the object |
| `0x02D3EAE8` | `void*` | 0 (zero-filled tail of `.data`) | `getAssetType` record (`0x02D3EAC0`) `+0x28`: the caller object `0x02D3EAF0` | `0x00675740` (`0x00675B4E`, 0; `0x00675BDC`, `0x02D3EAF0`) | callers of the method, through the record |
| `0x02D3EAF0` | `void*` | 0 (zero-filled tail of `.data`) | the caller object's vtable, `0x00D6C580` (slot 0 `0x006B4170`) | `0x00675740` (`0x00675BC2`) | callers of the method, through the record |
| `0x02D3EAF8` | `u8[16]` | 0 (zero-filled tail of `.data`) | the caller object's member-function pointer: `0x00677A70` and 0 | `0x00675740` (`0x00675BCE`, one 16-byte store) | the caller object's slots, through the object |
| `0x02D3EB48` | `void*` | 0 (zero-filled tail of `.data`) | `GetAssetReferenceByAsset` record (`0x02D3EB20`) `+0x28`: the caller object `0x02D3EB50` | `0x00675740` (`0x00675C26`, 0; `0x00675CA6`, `0x02D3EB50`) | callers of the script function, through the record |
| `0x02D3EB50` | `void*` | 0 (zero-filled tail of `.data`) | the caller object's vtable, `0x00D6C4C0` (slot 0 `0x0067E690`) | `0x00675740` (`0x00675C8A`) | callers of the script function, through the record |
| `0x02D3EB58` | `void*` | 0 (zero-filled tail of `.data`) | the function the caller object calls, `0x00676A70` | `0x00675740` (`0x00675C98`) | the caller object's slots, through the object |
| `0x02D3EBA8` | `void*` | 0 (zero-filled tail of `.data`) | `GetAssetReferenceByID` record (`0x02D3EB80`) `+0x28`: the caller object `0x02D3EBB0` | `0x00675740` (`0x00675CF0`, 0; `0x00675D70`, `0x02D3EBB0`) | callers of the script function, through the record |
| `0x02D3EBB0` | `void*` | 0 (zero-filled tail of `.data`) | the caller object's vtable, `0x00D6C4F0` (slot 0 `0x0067E690`) | `0x00675740` (`0x00675D54`) | callers of the script function, through the record |
| `0x02D3EBB8` | `void*` | 0 (zero-filled tail of `.data`) | the function the caller object calls, `0x00676BD0` | `0x00675740` (`0x00675D62`) | the caller object's slots, through the object |

## Modding notes

- A class's members exist only in code. A new field needs a new registration; a file cannot add one
  to a static class.
- Members are found by exact name, through the class and its ancestors. Names are case-sensitive
  even though their hash is not.
- New objects start as a copy of the default instance, so bytes no member describes still hold the
  constructor's values.
- The reflection layer reports problems through the Phyre log call `0x005CDAA0`, whose output the
  shipped game never shows.
- Descriptors are aligned allocations; release them with `_aligned_free`.

## Related

- [Class hierarchy](../Engine-Core/class-hierarchy.md): the RTTI that names every descriptor template.
- [Debug logging](../Engine-Core/debug-logging.md): where the reflection layer's messages go.
- [Lua runtime](../Third-Party-Libraries/lua-runtime.md): the Lua interpreter linked beside PhyreEngine.
- [Bullet physics](../Third-Party-Libraries/bullet-physics.md): the physics classes registered here.
- [Bigfile archive](../Game-Files-And-Data-Tables/bigfile-archive.md): where the `.phyre` files are stored.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x007F9360` is called by `0x007F7680`, `0x007F79C0`, `0x007F7B70`, `0x007F7CC0`, `0x007F7FF0`, `0x007F8140`, `0x007F8FD0`,
  `0x007F91B0`, `0x007FAE00`, `0x007FB400`, `0x007FB7F0`, `0x007FBF00`; `0x007F9360` is also called by `0x007FC620`, `0x007FCD80`,
  `0x007FDA10`; those functions are documented on
  [media decoder libraries](../Third-Party-Libraries/media-decoder-libraries.md).
- Platform: `0x005A08E0` calls `0x005CC930`; `0x00608A40` calls `0x005CD0A0`; `0x0079F150` calls `0x005CC930`, `0x005CD0A0`,
  `0x006253D0`; those functions are documented on [game application](../Engine-Core/game-application.md),
  [graphics adapters and vendor libraries](../Steam-And-Achievements/graphics-adapters-and-vendor-libraries.md).
