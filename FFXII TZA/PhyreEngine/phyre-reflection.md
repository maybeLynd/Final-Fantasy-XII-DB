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
and takes the next value of the global counter `0x02CF8260` as its index at `+0xE8`. `0x00632C90` is
the same without a parent or adjustment.

The vtable it installs is replaced by the class's own: `PClassDescriptorAbstract<T>`,
`PClassDescriptorConcrete<T>` or `PClassDescriptorForType<T>`, all derived from `PClassDescriptor`,
which derives from `Phyre::PType`.

`PClassDescriptorDynamic` (`0x00632E80`) is a `0x140`-byte form that copies its name and is built at
load time for a class no code registers. Its attach slot
`0x00639290` counts accepted members in the two words at `+0x100` and `+0x102`, and when they differ
first rebuilds the descriptor through `0x0063D550` (empty the six lists, copy the parent's size and
alignment, recompute the offsets through `0x0063E410`).

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
   table holds `0x001603E0`, which calls the Abstract constructor `0x005A7ED0`
   (`0x00632D80(…, "PAnimatableComponent", 0x108, 8, …, 8)`, flag `+0xFC` bit `0x2`, the three buffers
   below), installs the Concrete vtable, clears bit `0x2` and registers the teardown `0x008A8E20`.
   Template classes such as `PArray<T>` are built on first use inside a thread-safe static.
2. Its members are registered by descriptor slot `+0x60` (for `PAnimatableComponent`, `0x005A25E0`
   jumps to `0x005AD8F0`), each member behind its own thread-safe static, and the function ends in the
   finaliser `0x00639450`.

The finaliser calls `0x00639160`, which looks the name up in the namespace (`0x0063BA10`), reports a
second class of the same name, and otherwise links the descriptor's `+0x50` node into the namespace's
class list: at the front, or straight after its parent when the parent belongs to the same namespace.
When the namespace state is 1 or 2 it also computes the layout offsets (`0x0063E410`). The finaliser
then sets `+0xFC` bit `0x40000000`, the mark that members are registered.

### Layout offsets

`0x0063E410` sums `+0xF0` over the class and every ancestor up to the root descriptor `0x02CF8270`
into `+0xF4`, and stores the class's own non-negative `+0xF0` plus the parent's `+0xF8` in `+0xF8`.
A member's position in an object is its registered offset minus the owning class's `+0xF4`
(`0x0063C910`, `0x00639C80`, `0x0063CB80`). `PAnimatableComponent` passes 8: its reflected layout starts
8 bytes into the object, after the vtable pointer. Its member visitor `0x005A2390` is handed
`object + 8`, and descriptor slot `+0x58` (`0x0063FC60`) steps back 8 bytes to call the object's own
destructor.

### The type tree and the namespace

`0x006388C0` registers a descriptor in the global type tree whose header is `0x01F2E780` (returned by
`0x00637440`). It hashes the name from `0x7B5`, multiplying by 33 and adding the low five bits of each
byte, stores the hash at `+0x20` and the name at `+0x28`, and inserts `+0x08` into an ordered tree.
It returns false when the name is already present. The lookup `0x006311D0` orders by hash first and
compares the full string on equal hashes, so case-only differences collide in the hash but never
match.

`0x00638F00` takes a descriptor out of the tree again, erasing its node at `+0x08` (the header
is set up first when it was not); the `PClassDescriptorDynamic` destructor `0x00633590` calls it for a
descriptor with a name.

A namespace is a separate structure: the default one is `0x01F2E330` (returned by `0x006373D0`), its
classes hang off `+0x10`, and child namespaces off `+0x28`. `0x0063BA10` searches a namespace's own
classes, then each child namespace, with an exact byte comparison.

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

Slot `+0x40` is `0x0062EFD0` in the base, Abstract, Concrete and ForType vtables. It refuses the member with 5 when
`offset − [+0xF4] + width + [+0xF8]` exceeds the instance size, with `0x15` when it has no name and
with `0x12` when `0x00597220` finds the name in the class or any ancestor; otherwise it appends the
member to the list at `+0x80` and returns 0. Slot `+0x48` (`0x0062F080`) unlinks it again.

The width comes from `0x0063C0C0`: the context's pointer width (8 with no context) when attribute bit
`0x2` is set, or when the member is a dynamic array (kind 2) without bit `0x40`; otherwise the type's
size at `+0x38`, or the size the context gives a dynamic type.

### Member kinds

| Route | Record | Adds |
|---|---|---|
| `0x00632960` | `PClassDataMember` | the plain member |
| `0x00632A10` | `PClassDataMemberArray` | kind at `+0x5C` (2 a counted buffer such as `PArray<T>::m_els`, 3 a `PArray` member, 4 a `PSharray` member), element size at `+0x58` |
| `0x00632A70` | `PClassDataMemberArrayFixedSize` | kind 1 at `+0x5C`, the type's `+0x3C` at `+0x58`, element count at `+0x60` |
| `0x00632BE0` | `PClassDataMemberEnum` | attribute bit `0x20`, a value at `+0x58` |

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
`PSharray<T>` descriptor. `0x006B67F0` finds an annotation by key.

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
3. `0x00639C80` fills `+0xC8` with `0xFF` and `+0xD0` with zero, copies the parent's masks, then
   clears every byte a member covers in `+0xC8`, logging an overlap when a byte is already clear.
   For a primitive member it writes the member's `WriteMask` into `+0xD0`, or `0xFF` bytes without
   one; for an inline object it copies that class's masks. It sets bit `0x10000000` when no byte of
   `+0xC8` is left set.

So `+0xC8` marks the bytes no member describes and `+0xD0` the bits that belong to member values.
`0x0063C5E0` and `0x0063C1A0` build a class's buffers when needed and return its `+0xD0` and `+0xC8`;
`0x00639C80` uses them for the
masks of inline object members.

### Creating instances

`0x0063A990(cluster, count, descriptor, …)` is `PCluster::create`. A class with `+0xFC` bit `0x8`
logs "has no default constructor and cannot be allocated" and gets nothing. Otherwise `0x00639510`
refuses an abstract class (bit `0x2`) and allocates `count × [+0x38]` bytes with alignment `[+0x3C]`,
and `0x0063C910` initialises each instance in turn: it builds the buffers if needed, then copies the
whole default instance over it. Without a default instance it constructs through slot `+0x50` and
copies the default instance of every inline object member, across the class and its ancestors.

### The cluster's script methods

`0x00635470` publishes four `PCluster` methods on the cluster descriptor `0x02CF8780`:

- `create` (`0x0063AA50`) makes one object: it logs the same "no default constructor" message for bit
  `0x8`, and otherwise builds a one-object instance list through `0x00639510`, initialises the object
  at the list's `+0x58` with `0x0063C910` and returns the object with its descriptor.
- `deleteObject` is `0x0063AD20`.
- `deleteInstancesOfType` (`0x0063AAD0`) removes every instance list of exactly one class: it unlinks
  the list, takes it off the per-type table, destroys its objects (`0x0063B3E0`), frees its blocks
  (`0x00680030`) and returns the list record to the cluster's pool at `+0x50` (`0x00680200`).
- `absorb` (`0x00638FB0`) moves every list of another cluster into this one (see below).

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

The `atexit` thunk `0x008A8E20` restores the class's descriptor vtable and jumps to `0x00633390`, the
base destructor:

1. It installs the `PClassDescriptor` vtable and, when its index at `+0xE8` is the last one handed
   out, decrements `0x02CF8260`.
2. `0x0063D640` unlinks `+0x50` from its namespace and unlinks an emptied non-default namespace.
3. It frees the records of `+0x90` and `+0xA0` whose attribute bit `0x1` is set, with their name,
   then unlinks every remaining node of `+0x80`, `+0x90`, `+0xA0` and `+0xB0` without freeing it.
4. `0x006B6700` unlinks every node of `+0x60`, and the `PType` vtable is installed last.

A member's teardown `0x00633240` detaches it through its owner's slot `+0x48`, drains its annotations
and frees a copied name. The deleting destructors such as `0x005847E0` call `0x00633390` and, when flag
bit `0x1` is set, free the object with `_aligned_free` (`0x00584730`); with bit `0x4` as well they call
the empty `0x0016D6A0` and free nothing.

## Layouts

PType (base of every type and descriptor):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable |  |
| `+0x08` | `void*` | type-tree links (three pointers, +0x08..+0x1F) |  |
| `+0x20` | `u32` | name hash, written by 0x006388C0 |  |
| `+0x28` | `void*` | name, as the tree key |  |
| `+0x30` | `void*` | name |  |
| `+0x38` | `u32` | instance size |  |
| `+0x3C` | `u32` | alignment |  |
| `+0x40` | `void*` | name-writer hook, or null (0x00637320, 0x00637350) |  |
| `+0x48` | `void*` | name-resolver hook, or null (0x006389C0, 0x00638A50) |  |

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
| `+0x50` | `ListNode` | node in the namespace's class list |  |
| `+0x60` | `ListNode` | drained by 0x006B6700 at teardown |  |
| `+0x70` | `void*` | namespace |  |
| `+0x78` | `void*` | parent descriptor, or null |  |
| `+0x80` | `ListNode` | data members |  |
| `+0x90` | `ListNode` | methods |  |
| `+0xA0` | `ListNode` | script functions |  |
| `+0xB0` | `ListNode` | fourth list, emptied by the constructor and the destructor |  |
| `+0xC0` | `void*` | default instance |  |
| `+0xC8` | `void*` | undescribed-byte mask |  |
| `+0xD0` | `void*` | write mask |  |
| `+0xD8` | `void*` | 0 (zeroed by the constructor) |  |
| `+0xE0` | `void*` | 0 (zeroed by the constructor) |  |
| `+0xE8` | `u32` | registration index (0x02CF8260) |  |
| `+0xEC` | `u32` | 0xFFFFFFFF |  |
| `+0xF0` | `i32` | this class's adjustment |  |
| `+0xF4` | `i32` | sum of adjustments to the root |  |
| `+0xF8` | `i32` | layout base of an instance |  |
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
| `+0x100` | `u16` | pair compared by 0x0063D550 to skip a rebuild |  |
| `+0x104` | `u32` | parent's instance size |  |
| `+0x108` | `…` | three {u32, ptr} pairs at +0x108, +0x118, +0x128, zeroed by 0x00632E80 |  |
| `+0x138` | `void*` | tagged name; +0x30 holds it with bit 0 cleared |  |

PClassDataMember (`0x58`; arrays to `+0x64`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable |  |
| `+0x08` | `ListNode` | node in the owner's +0x80 list |  |
| `+0x18` | `void*` | owning descriptor |  |
| `+0x20` | `void*` | name |  |
| `+0x28` | `u32` | attribute word |  |
| `+0x30` | `void*` | type (a PType or a class descriptor) |  |
| `+0x38` | `ListNode` | annotations |  |
| `+0x48` | `u32` | offset in the owner's layout |  |
| `+0x50` | `void*` | dynamic-type helper, or null |  |
| `+0x58` | `u32` | element size (arrays) |  |
| `+0x5C` | `u32` | array kind |  |
| `+0x60` | `u32` | element count (fixed arrays) |  |

PAnnotation (`0x30`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable |  |
| `+0x08` | `ListNode` | node in a member's +0x38 list |  |
| `+0x18` | `void*` | key (0x02CF8570 for WriteMask) |  |
| `+0x20` | `void*` | value type |  |
| `+0x28` | `u32` | fourth constructor argument |  |
| `+0x30` | `u32` | value (PAnnotationWithValue&lt;unsigned int&gt;) |  |

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
| `+0x00` | `visit` | every | member of the class and its ancestors (`0x0063E2E0`) |
| `+0x18` | `get` | the | value from a script context |
| `+0x20` | `put` | the | value into a script context |
| `+0x38` | `scalar` | deleting | destructor |
| `+0x40` | `attach` | a | member (`0x0062EFD0`) |
| `+0x48` | `detach` | a | member (`0x0062F080`) |
| `+0x50` | `construct` | in | place; returns false for a class without one (`0x00657140`) |
| `+0x58` | `destruct` | in | place (`0x0063FC60`) |
| `+0x60` | `register` | the | members (_purecall in ForType&lt;T&gt;) |
| `+0x68` | `push` | the | object's held objects of a named class to a script and count them; -1 by default (`0x00660570`) |

One class overrides slot `+0x68`: `PEntity` (`0x006AB3F0`, which reorders the arguments for `0x006AB540`). It looks the
name up in the namespace (`0x0063BA10`), returns -1 unless that class is `PComponent` or derives from it, and
otherwise pushes every component of the entity whose class is that class or derives from it (`0x00684090`)
and returns how many it pushed.

For a `PMatrix4x3` the wrapper's slot `+0x20` (`0x006B3A90` to `0x006B3610`) builds a 64-byte matrix from the
twelve floats, as (`+0xC`, `+0x1C`, `+0x2C`, 0), (`+0`, `+4`, `+8`, 0), (`+0x10`, `+0x14`, `+0x18`, 0) and
(`+0x20`, `+0x24`, `+0x28`, 1.0 from `0x01CEBBA8`), and pushes it as a script `Matrix` (`0x00684130`).

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

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
| `+0x00` | `u32` | m_totalOutputElementSize m_totalOutputElementSize (u32), registered by 0x006D0FA0 (0x00632960 at | `0x006D126A`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetwork; the placement constructor `0x006CFA50` clears it (`0x006CFA76`) |
| `+0x04` | `u8[4]` | bytes04 | the bytes after m_totalOutputElementSize (`+0x00`), before the dword the placement constructor `0x006CFA50` clears at `+0x08` (`0x006CFA57`); no registered member covers it (`0x006CFC50` registers the `0x70`-byte class at `0x006CFCA0`) |
| `+0x18` | `u32` | m_totalInputCount | m_totalInputCount (u32), registered by `0x006D0FA0` (`0x00632960` at `0x006D10D0`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetwork; the placement constructor `0x006CFA50` clears it (`0x006CFA73`) |
| `+0x1C` | `u8[4]` | bytes1C | the bytes after m_totalInputCount (`+0x18`), before the dword the placement constructor `0x006CFA50` clears at `+0x20` (`0x006CFA5E`); no registered member covers it (`0x006CFC50` registers the `0x70`-byte class at `0x006CFCA0`) |
| `+0x50` | `u32` | m_totalPersistentStateSize m_totalPersistentStateSize (u32), registered by 0x006D0FA0 (0x00632960 | at `0x006D13C1`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetwork; the placement constructor `0x006CFA50` clears it with m_totalStateBlockSize (`0x006CFA80`) |
| `+0x54` | `u32` | m_totalStateBlockSize | m_totalStateBlockSize (u32), registered by `0x006D0FA0` (`0x00632960` at `0x006D1434`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetwork; the placement constructor `0x006CFA50` clears it with m_totalPersistentStateSize (`0x006CFA80`) |
| `+0x58` | `u8` | m_isCompiled | m_isCompiled (u8), registered by `0x006D0FA0` (`0x00632960` at `0x006D14A7`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetwork; the placement constructor `0x006CFA50` clears it (`0x006CFA84`) |
| `+0x59` | `u8[7]` | pad59 | the bytes after m_isCompiled (u8 at `+0x58`), before the dword the placement constructor `0x006CFA50` clears at `+0x60` (`0x006CFA6C`); no registered member covers it (`0x006CFC50` registers the `0x70`-byte class at `0x006CFCA0`) |

`PModifierNetworkDynamicMeshSegment` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u32` | m_segmentInputGroupStart m_segmentInputGroupStart (u32), registered by 0x006BCA20 (0x00632960 at | `0x006BCB20`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkDynamicMeshSegment; cleared with m_segmentOutputGroupStart by the placement constructor `0x005CEEF0` (`0x005CEEFA`) |
| `+0x0C` | `u32` | m_segmentOutputGroupStart m_segmentOutputGroupStart (u32), registered by 0x006BCA20 (0x00632960 | at `0x006BCB93`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkDynamicMeshSegment; cleared with m_segmentInputGroupStart by the placement constructor `0x005CEEF0` (`0x005CEEFA`) |
| `+0x10` | `u32` | m_modifierOutputsAreConsumed m_modifierOutputsAreConsumed (u32), registered by 0x006BCA20 | (`0x00632960` at `0x006BCC06`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkDynamicMeshSegment; cleared by the placement constructor `0x005CEEF0` (`0x005CEEFE`) |
| `+0x14` | `u8[4]` | bytes14 | the bytes after m_modifierOutputsAreConsumed (`+0x10`) up to the end of the `0x18`-byte class; no registered member covers it (`0x006BBB70` registers the `0x18`-byte class at `0x006BBBC0`) |

`PModifierNetworkInstanceInput` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u32` | m_elementSize | m_elementSize (u32), registered by `0x006C3580` (`0x00632960` at `0x006C3612`); no shipped .phyre file declares PModifierNetworkInstanceInput; cleared with `+0x0C` by the placement constructor `0x006C2960` (`0x006C2967`) |
| `+0x0C` | `u8[4]` | bytes0C | cleared with m_elementSize by the placement constructor `0x006C2960` (`0x006C2967`); no registered member covers it (`0x006C2EF0` registers the `0x20`-byte class at `0x006C2F3A`) |

`PSamplerStateBase` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x05` | `u8[3]` | pad05 | the bytes after the byte the placement constructor `0x005D5FE0` sets to 1 at `+0x04` (`0x005D5FED`) up to m_lodBias (`+0x08`); no registered member covers it (`0x005D9E70` registers the `0x20`-byte class at `0x005D9EC0`) |
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
| `+0x04` | `u32` | m_constantBufferLocation m_constantBufferLocation (u32), registered by 0x005E89C0 (0x00632960 at | `0x005E8A4E`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderParameterCaptureBufferLocationTypeConstantBuffer; the placement constructor `0x005D7DE0` clears `+0x04` to `+0x0B` (`0x005D7DEA`) |
| `+0x08` | `u32` | m_size | m_size (u32), registered by `0x005E89C0` (`0x00632960` at `0x005E8ABD`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderParameterCaptureBufferLocationTypeConstantBuffer; cleared with m_constantBufferLocation by the placement constructor `0x005D7DE0` (`0x005D7DEA`) |
| `+0x0D` | `u8[3]` | pad0D | the bytes after the byte the placement constructor `0x005D7DE0` sets to `0x34` at `+0x0C` (`0x005D7DEE`) up to the end of the `0x10`-byte class; no registered member covers it (`0x005DA6D0` registers the `0x10`-byte class at `0x005DA71A`) |

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

## Shipped data

| Fact | Value |
|---|---|
| static descriptor constructions | 399: 384 calls to `0x00632D80` and 15 to `0x00632C90` (a 385th call is inside `0x00632E80`); `PBase` (`0x02CF8270`, size 1) and `PClassDescriptor` (`0x02CF8470`, size `0x100`) by their own initialisers |
| member registrations | 682 calls to `0x00632960` (2 of them the array and dynamic constructors forwarding), 165 to `0x00632A10`, 29 to `0x00632A70`, 21 to `0x00632BE0` |
| plain-member attribute arguments | `0x10` 207, `0x00` 196, `0x08` 123, `0x12` 79, `0x0A` 39, `0x02` 36; the flag argument is 0 at all 680 |
| array kinds | `PArray` 86, pointer array 70, `PSharray` 9; element sizes 8 (113), 4 (36), 1 (7), 2 (6), 16 (3) |
| annotations | 70 constructions; 69 static `WriteMask` annotations (60 `PArray`, 9 `PSharray`) |
| buffers | 384 classes register a default instance and both masks |
| by-name registrations | `0x006388C0`: 523 sites, 516 calls and 7 tail jumps; `0x00639450`: 471 sites, 156 calls and 315 tail jumps |
| base destructor | `0x00633390`: 1,981 sites, 1,186 calls and 795 jumps from the destructor thunks |
| RTTI classes | `PClassDescriptorForType<T>` 409, `Abstract<T>` 393, `Concrete<T>` 331, `WithoutDefaultConstructor<T>` 38, `Wrapper<T>` 15, `PTypeDefault<T>` 12, `PClassDataMemberArrayDynamic<T>` 71, `PClassDataMemberPhyreArray<T>` 59 |

### Data files

These tables stay beside this page. Each lists one generated family or one per-class view.

| File | Rows | What it lists |
|---|---:|---|
| [phyre-reflection-abstract-class-descriptor-constructors.tsv](phyre-reflection-abstract-class-descriptor-constructors.tsv) | 177 | Abstract descriptor constructors such as `0x005A7ED0` |
| [phyre-reflection-abstract-class-descriptor-base-aware-constructors.tsv](phyre-reflection-abstract-class-descriptor-base-aware-constructors.tsv) | 131 | Abstract constructors that pass a parent descriptor |
| [phyre-reflection-pclassdescriptor-static-initialisers.tsv](phyre-reflection-pclassdescriptor-static-initialisers.tsv) | 253 | Concrete static initialisers such as `0x001603E0` |
| [phyre-reflection-descriptor-flag-registrars.tsv](phyre-reflection-descriptor-flag-registrars.tsv) | 33 | descriptor initialisers, 64-byte form |
| [phyre-reflection-descriptor-flag-registrars-compact.tsv](phyre-reflection-descriptor-flag-registrars-compact.tsv) | 4 | descriptor initialisers, 53-byte form |
| [phyre-reflection-guarded-class-registration-stubs.tsv](phyre-reflection-guarded-class-registration-stubs.tsv) | 98 | thread-safe guarded class registrars |
| [phyre-reflection-name-only-class-registration-initialisers.tsv](phyre-reflection-name-only-class-registration-initialisers.tsv) | 110 | initialisers that call `0x006388C0` and jump to `0x00639450` |
| [phyre-reflection-two-member-descriptor-registrars.tsv](phyre-reflection-two-member-descriptor-registrars.tsv) | 38 | array descriptors with `m_count` and `m_els` |
| [phyre-reflection-phyre-registrar-classes.tsv](phyre-reflection-phyre-registrar-classes.tsv) | 409 | registrars and the classes they name |
| [phyre-reflection-phyre-type-name-hashes.tsv](phyre-reflection-phyre-type-name-hashes.tsv) | 399 | type names and their `0x006388C0` hashes |
| [phyre-reflection-phyre-class-instance-sizes.tsv](phyre-reflection-phyre-class-instance-sizes.tsv) | 177 | instance size and alignment per class |
| [phyre-reflection-phyre-class-parent-chain.tsv](phyre-reflection-phyre-class-parent-chain.tsv) | 330 | parent descriptor per class |
| [phyre-reflection-phyre-class-f4-offset-adjustment.tsv](phyre-reflection-phyre-class-f4-offset-adjustment.tsv) | 179 | `+0xF4` per class |
| [phyre-reflection-phyre-default-instances.tsv](phyre-reflection-phyre-default-instances.tsv) | 173 | default instance per class |
| [phyre-reflection-phyre-class-default-buffers.tsv](phyre-reflection-phyre-class-default-buffers.tsv) | 384 | the `+0xC0`, `+0xC8` and `+0xD0` buffers per class |
| [phyre-reflection-phyre-class-descriptor-vtable.tsv](phyre-reflection-phyre-class-descriptor-vtable.tsv) | 315 | each class's descriptor vtable and its slots |
| [phyre-reflection-phyre-class-descriptor-accesses.tsv](phyre-reflection-phyre-class-descriptor-accesses.tsv) | 168 | instructions that access descriptor fields |
| [phyre-reflection-p-type-default-u-int-accesses.tsv](phyre-reflection-p-type-default-u-int-accesses.tsv) | 16 | accesses to the `PTypeDefault<unsigned int>` object |
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
| [phyre-reflection-class-descriptor-static-teardowns.tsv](phyre-reflection-class-descriptor-static-teardowns.tsv) | 403 | descriptor `atexit` teardowns such as `0x008A8E20` |
| [phyre-reflection-pclassdescriptor-destructor-thunks.tsv](phyre-reflection-pclassdescriptor-destructor-thunks.tsv) | 383 | thunks that restore a vtable and jump to `0x00633390` |
| [phyre-reflection-pclassdescriptor-deleting-destructors.tsv](phyre-reflection-pclassdescriptor-deleting-destructors.tsv) | 1,147 | ForType deleting destructors such as `0x005847E0` |
| [phyre-reflection-pclassdescriptor-deleting-destructors-map.tsv](phyre-reflection-pclassdescriptor-deleting-destructors-map.tsv) | 1,148 | the vtable each of them installs |
| [phyre-reflection-data-member-metadata-static-teardowns.tsv](phyre-reflection-data-member-metadata-static-teardowns.tsv) | 852 | member-record `atexit` teardowns |
| [phyre-reflection-pclassdatamember-deleting-destructors.tsv](phyre-reflection-pclassdatamember-deleting-destructors.tsv) | 137 | member-record deleting destructors |
| [phyre-reflection-pclassdatamemberstaticteardownadapter.tsv](phyre-reflection-pclassdatamemberstaticteardownadapter.tsv) | 29 | member-record teardown adapters |
| [phyre-reflection-annotationstaticteardown.tsv](phyre-reflection-annotationstaticteardown.tsv) | 54 | annotation teardowns |
| [phyre-reflection-nameddescriptorstaticteardown.tsv](phyre-reflection-nameddescriptorstaticteardown.tsv) | 14 | named-descriptor teardowns |
| [phyre-reflection-ptypestaticteardown.tsv](phyre-reflection-ptypestaticteardown.tsv) | 16 | `PType` teardowns |
| [phyre-reflection-reflectionstaticteardown.tsv](phyre-reflection-reflectionstaticteardown.tsv) | 27 | other reflection-object teardowns |
| [phyre-reflection-staticdescriptorsingleton.tsv](phyre-reflection-staticdescriptorsingleton.tsv) | 11 | static descriptor singletons |

### Per-class field accesses

Each file lists the instructions that read or write a field of one class: function, site,
displacement, read or write, and how the object pointer was traced.

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
- **Find a member.** `0x00597220(descriptor, name)` searches the class, then its ancestors.
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

Every instruction in the game that writes or reads a descriptor's `+0xFC` is a row of
[phyre-reflection-class-flag-sites.tsv](phyre-reflection-class-flag-sites.tsv): 1006 rows, one per bit and access.
926 instructions touch the word: 380 through a pointer and 546 at a descriptor's static address. Nothing
reads the whole word: every load ends in a bit test, a sign test, a bit extraction or a store back. By bit:

| Bit | Meaning | Written by | Read by |
|---|---|---|---|
| `0x1` | dynamic class | `0x00632E80` (`0x00632F18`) | 21 sites: `0x00633790`, `0x006361C0`, `0x00636280`, `0x00637320`, `0x00637350`, `0x00639450`, `0x00639A60`, `0x0063ABF0`, `0x0063BBC0`, `0x0063C910`, `0x008AF490` (`0x008AF4D6`, through `[0x01F2E340]` - `0x50`), and the 10 core registrars after their `bts` (`0x006344F8` and the same test in the other nine) |
| `0x2` | abstract | set at 393 sites (the 315 class constructors' `or`, the 69 array-type getters and 9 more); cleared at 373 sites: 303 initialisers, the 69 array-type getters after installing the Concrete vtable, and `0x00635DC0` (`0x00635E38`-`0x00635E7C`) | `0x0059AC00` (`0x0059ACDB`), `0x00639510` (`0x0063954C`), `0x00639A60` (`0x00639AF1`), `0x0063A4C0` (`0x0063A51E`) |
| `0x4` | set by the initialisers of `PParameterBuffer` and the three header descriptors; the PCluster loader tests it per class | `0x001615C0` (`0x001615FF`), `0x001605C0` (`0x00160602`), `0x00167DB0` (`0x00167DF2`) and `0x001688F0` (`0x00168932`) | `0x00639780` (`0x006397C0`) and the PCluster loaders `0x0059C250`, `0x0059C700`, `0x0059CE30`, `0x0059D590`, `0x0059D6A0` (twice), `0x0059D940` and `0x0059F500` |
| `0x8` | no default constructor | set by 39 initialisers (load, clear `0x2`, set `0x8`, store); cleared by the three header-descriptor initialisers `0x001605C0`, `0x00167DB0` and `0x001688F0` as they set `0x4` | `0x0059AC00` (`0x0059ACDB`), `0x00639A60` (`0x00639B2C`), `0x0063A990` (`0x0063A99A`), `0x0063AA50` (`0x0063AA5F`) |
| `0x10` | set for the three header descriptors | `0x005B0700` (`0x005B0720`), `0x006D1810` (`0x006D1830`) and `0x006D9FC0` (`0x006D9FE0`), each right after `0x006388C0` registers the descriptor | `0x0059D940` (`0x0059DCD3`-`0x0059DCDB`), which extracts it: 1 for those three classes, 0 for every other |
| `0x20` | set by the class's registrar or wrapper getter before `0x00639450` registers the members: right after `0x006388C0` registers the descriptor by name in 22 registrars, twice between `0x006388C0` and `0x00639450` in `0x00608A40` (`0x00608AC5`, `0x00608C0F`), after the member record is built in the nine wrapper getters `0x006B0760` to `0x006B33F0` (seven Vectormath types, `PMatrix4` and `PMatrix4x3`), and at entry in PBase's registrar (`0x006344B2`) | 34 sites in 33 functions | read by no instruction |
| `0x08000000` | a member is a PSharray (`0x00639EE2`-`0x00639EEF`), or the parent has the bit (`0x00639D9D`-`0x00639DB0`) | `0x00639C80`: cleared (`0x00639CB4`), set (`0x00639EEF`), and copied from the parent's word (`0x00639D9D`-`0x00639DB0`) | `0x00639C80` (the parent's bit, `0x00639DAB`) |
| `0x10000000` | every instance byte is described by a member | `0x00639C80`: cleared (`0x00639CB4`), set (`0x0063A0E2`) | `0x00639850` (`0x00639868`) |
| `0x20000000` | set by `0x0063BC00`, never tested | `0x0063BC00` (`0x0063BC49`) | none |
| `0x40000000` | members registered (`0x00639450`) | set by `0x00636280` (`0x006363E0`), `0x00639450` (`0x00639465`) and the 10 core registrars' `bts` (12 sites); cleared by `0x00638C90` (`0x00638D8D`) | 13 sites in `0x00636280`, `0x00637A70`, `0x00639850`, `0x00639A40`, `0x00639C80` (two), `0x0063A790`, `0x0063BB10`, `0x0063BC00`, `0x0063C1A0`, `0x0063C5E0`, `0x0063C910` (two) |
| `0x80000000` | default instance and masks built | set by `0x00639A60` (`0x00639C55`); cleared by `0x00632E80` (`0x00632F3C`), `0x0063D410` (`0x0063D4DB`) and `0x0063D930` (`0x0063D945`) | 13 sign tests: at the loads of the `0x40000000` readers other than `0x00639A40`, and at `0x00639A60` (`0x00639A94`) |

No instruction writes or reads bits `0x40` to `0x4000000`. The whole word is written as 0 by the 10 core
constructors `0x006316C0`-`0x00632780`, `0x00632C90` (`0x00632D6A`, 8 bytes from `+0xF8`) and `0x00632D80` (`0x00632E69`), and
stored back by the initialisers after they change their bits (43 sites) by the 10 core registrars after their
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
| annotation `+0x30`, 69 rows | `u32` | 0 | `0x7FFFFFFF`; `0x00639C80` takes it through the annotation's slot `+0x08` (`0x005C4D20`, `0x0063A05F`) and copies it into the write mask over `m_count`, leaving out bit 31 | the getter | - |
| `m_els` `+0x00`, 69 rows | `void*` | 0 | the record's `PClassDataMemberArrayDynamic<T>` vtable, installed after `0x00632A10` builds the record | the getter | - |
| `m_els` `+0x28`, 9 rows | `u32` | 0 | attribute bit `0x40` ORed in for a `PSharray<T>` | the getter | - |
| `m_els` `+0x58`, 69 rows | `u32` | 0 | element size: 8 in 51 getters, 4 in 13, 2 in 3, 1 and 16 in one each | the getter | - |
| `m_els` `+0x60`, 69 rows | `void*` | 0 | `0x005C4CC0`, which returns the array's first word without bit 31 | the getter | - |
| `m_els` `+0x68`, 69 rows | `void*` | 0 | 0, or `0x00671250` in the 9 `PSharray<T>` getters | the getter | - |
| `m_els` `+0x70`, 69 rows | `void*` | 0 | the set-elements function of the element type (`0x00673130` in 19 getters, `0x006AF760` in 22) | the getter | - |

In all 69 record vtables slot `+0x20` is `0x006065D0`, which calls `+0x60`; slots `+0x30` and `+0x38` are
`0x00604580`, which calls `+0x68` or, when it is 0, reads the pointer stored in the member; slot `+0x40` is
`0x0060F3D0`, which calls `+0x70` with a buffer and a count and returns `0x15` when it is 0. `0x00673130` frees
a buffer the array owns, then stores the new buffer at `+0x08` and the count with bit 31 set.

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

- `+0xC0`, `+0xC8`, `+0xD0`: the three static buffers, stored by the initialiser;
- `+0x08`-`+0x28`: reset by the registrar only when bit `0x1` of `+0xFC` is set (`0x006344F8` and the same test
  in the others), which the class's own code leaves clear;
- `PBase` `+0x38`: `0x006318A0` stores 1 through the descriptor (`0x00631913`), then the initialiser `0x00164180`
  stores 0 (`0x00164197`).

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
- `0x006CD390`, `PNamedSemanticDynamic::FindOrCreateDynamic`, finds a name with `_stricmp`. On a miss it takes a
  record from the pool `0x02E5C218` and a name slot from `0x02E5C240`, copies the name, sets the flag to 1 and
  registers the record.
- `0x006CD5B0`, slot `+0x50` of `PNamedSemanticDescriptorForDynamicType<PTriggerType>` (`0x00D89F40`, the descriptor
  `0x006CD270` builds at `0x02E5C270`), copies every record's address into an array.

### The per-type table size

The engine set-up `0x005A08E0` calls `0x00638AE0` (`0x005A0AB7`), which walks every class descriptor (the list at
`+0x10` of the object `0x006373D0` returns, linked through `+0x50`), gives every
descriptor its per-type table entry at `+0xEC` (`0x00638C0A`). It stores the number of descriptors it walked. The run
setup `0x0079F150` calls `0x0063C730` (`0x0079F539`), which reads that number and, when the world's per-type table (count
`+0x10`, entries `+0x18`) does not already hold one more than it, gives the table that many `0x20`-byte entries and
links each entry's list to itself.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CF8264` | `u32` | 0 (zero-filled tail of `.data`) | the number of class descriptors `0x00638AE0` numbered | `0x00638AE0` (`0x00638C40`) | `0x0063C730` (`0x0063C744`) |

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
record itself and frees the name buffer `+0x18` when bit 0 of `+0x20` is set.

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
