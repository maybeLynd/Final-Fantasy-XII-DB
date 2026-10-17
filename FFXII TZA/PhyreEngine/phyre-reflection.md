---
title: "Phyre reflection: how PhyreEngine describes its classes at run time, registers their members and creates instances"
kind: "system"
category: "PhyreEngine"
addresses: "00632D80, 00632C90, 00632E80, 005A7ED0, 001603E0, 00639450, 00639160, 0063E410, 006388C0, 006311D0, 0063BA10, 00632960, 00632FB0, 00632A10, 00632A70, 00632BE0, 0062EFD0, 0062F080, 00597220, 0063C0C0, 006B66C0, 006B67D0, 006B67F0, 0063A990, 00639510, 0063C910, 00639A60, 00639C80, 0063CB80, 00633390, 0063D550, 0063D640, 006B6700, 00633240, 005847E0, 00584730, 02CF8260, 01F2E330, 01F2E780, 02CF8270, 02CF8470, 02CF8570"
---

## What the player sees

Nothing directly. Every model, texture, shader, animation and scene the game loads from a `.phyre`
file becomes an object through this layer: the loader finds each class in the file by name, matches
its fields to the members registered here, and builds instances from the class's default instance.
A class or field the executable does not register cannot be brought in by editing assets.

## How it works

### The class descriptor and its types

Each reflected class has one descriptor, a `Phyre::PClassDescriptor` object of `100`<sub>h</sub> bytes. The
constructor `00632D80(descriptor, namespace, name, size, alignment, parent, adjust)` empties the six
list heads, stores the name pointer at `+30`<sub>h</sub>, the instance size at `+38`<sub>h</sub>, the alignment at
`+3C`<sub>h</sub>, the namespace at `+70`<sub>h</sub>, the parent descriptor at `+78`<sub>h</sub> and the adjustment at `+F0`<sub>h</sub>,
and takes the next value of the global counter `02CF8260` as its index at `+E8`<sub>h</sub>. `00632C90` is
the same without a parent or adjustment.

The vtable it installs is replaced by the class's own: `PClassDescriptorAbstract<T>`,
`PClassDescriptorConcrete<T>` or `PClassDescriptorForType<T>`, all derived from `PClassDescriptor`,
which derives from `Phyre::PType`.

`PClassDescriptorDynamic` (`00632E80`) is a `140`<sub>h</sub>-byte form that copies its name and is built at
load time for a class no code registers. Its attach slot
`00639290` counts accepted members in the two words at `+100`<sub>h</sub> and `+102`<sub>h</sub>, and when they differ
first rebuilds the descriptor through `0063D550` (empty the six lists, copy the parent's size and
alignment, recompute the offsets).

A dynamic class's members are placed one after another. `0063C630`, called from `006393A0`, takes
the member's width and alignment from its type (8 and 8 for attribute bit `2`<sub>h</sub>), aligns the running
end at `+104`<sub>h</sub>, adds the width, raises `+3C`<sub>h</sub> to the alignment and rounds `+38`<sub>h</sub> up to it, and
returns the member's offset less the parent's size.

Loaded `PClassDataMemberDynamic` records are reset by that descriptor's slot `+70`<sub>h</sub> (`0062F4E0`, which jumps to `006361C0`): it empties each
record's node and annotation list, clears attribute bit `1`<sub>h</sub>, takes the name from the tagged pointer
at `+58`<sub>h</sub>, and places the record through `0063D410` when its owner is dynamic.

### Registration

A class is registered in two steps:

1. Its descriptor is built. For most classes this runs before `main`: the C runtime's initialiser
   table holds `001603E0`, which calls the Abstract constructor `005A7ED0`
   (`00632D80(…, "PAnimatableComponent", 108h, 8, …, 8)`, flag `+FC`<sub>h</sub> bit `2`<sub>h</sub>, the three buffers
   below), installs the Concrete vtable, clears bit `2`<sub>h</sub> and registers the teardown `008A8E20`.
   Template classes such as `PArray<T>` are built on first use inside a thread-safe static.
2. Its members are registered by descriptor slot `+60`<sub>h</sub> (for `PAnimatableComponent`, `005A25E0`
   jumps to `005AD8F0`), each member behind its own thread-safe static, and the function ends in the
   finaliser `00639450`.

The finaliser calls `00639160`, which looks the name up in the namespace (`0063BA10`), reports a
second class of the same name, and otherwise links the descriptor's `+50`<sub>h</sub> node into the namespace's
class list: at the front, or straight after its parent when the parent belongs to the same namespace.
When the namespace state is 1 or 2 it also computes the layout offsets (`0063E410`). The finaliser
then sets `+FC`<sub>h</sub> bit `40000000`<sub>h</sub>, the mark that members are registered.

### Layout offsets

`0063E410` sums `+F0`<sub>h</sub> over the class and every ancestor up to the root descriptor `02CF8270`
into `+F4`<sub>h</sub>, and stores the class's own non-negative `+F0`<sub>h</sub> plus the parent's `+F8`<sub>h</sub> in `+F8`<sub>h</sub>.
A member's position in an object is its registered offset minus the owning class's `+F4`<sub>h</sub>
(`0063C910`, `00639C80`, `0063CB80`). `PAnimatableComponent` passes 8: its reflected layout starts
8 bytes into the object, after the vtable pointer. Its member visitor `005A2390` is handed
`object + 8`, and descriptor slot `+58`<sub>h</sub> (`0063FC60`) steps back 8 bytes to call the object's own
destructor.

### The type tree and the namespace

`006388C0` registers a descriptor in the global type tree whose header is `01F2E780` (returned by
`00637440`). It hashes the name from `7B5`<sub>h</sub>, multiplying by 33 and adding the low five bits of each
byte, stores the hash at `+20`<sub>h</sub> and the name at `+28`<sub>h</sub>, and inserts `+08`<sub>h</sub> into an ordered tree.
It returns false when the name is already present. The lookup `006311D0` orders by hash first and
compares the full string on equal hashes, so case-only differences collide in the hash but never
match.

`00638F00` takes a descriptor out of the tree again, erasing its node at `+08`<sub>h</sub> (the header
is set up first when it was not); the `PClassDescriptorDynamic` destructor `00633590` calls it for a
descriptor with a name.

A namespace is a separate structure: the default one is `01F2E330` (returned by `006373D0`), its
classes hang off `+10`<sub>h</sub>, and child namespaces off `+28`<sub>h</sub>. `0063BA10` searches a namespace's own
classes, then each child namespace, with an exact byte comparison.

### Type references by name

A type object's `+40`<sub>h</sub> and `+48`<sub>h</sub> hold two hooks that are null in most types. The type of `PType`
(`01F2E370`, set up by `00637720`) and the descriptor of `PClassDescriptor` (`02CF8470`, set up by
`00634830`) fill them, so a pointer to a type is written and read as the type's name:

- `+40`<sub>h</sub> gives the name and its length with the terminator. The class-descriptor form `00637320`
  returns `14`<sub>h</sub> for a dynamic class (bit `1`<sub>h</sub>); the `PType` form is `00637350`.
- `+48`<sub>h</sub> resolves a name. `00638A50` (`PType`) and `006389C0` (`PClassDescriptor`) hash it as
  `006388C0` does, search the type tree with `006311D0`, store the type found and return `13`<sub>h</sub> when
  no type has that name.

The loader reaches `+48`<sub>h</sub> through `0063DC30`, which returns `15`<sub>h</sub> when the hook is null.

`0063DC90` installs such a pair. The `PAssetReferenceImport` descriptor `02D3E780` (registered by
`00675DA0`) gets `00676F50` and `00677470`, which store a reference as a byte-swapped 16-bit index into
the cluster's list of `18`<sub>h</sub>-byte import records instead of a name. Reading one, `00677470` chains
the pointer into the import record's list at `+10`<sub>h</sub>; both return 7 when the cluster has no import
list.

A `PNamedSemanticDescriptor` (built by `006B6820`) uses the same two hooks for a registry of named
objects. `PRenderDataType` (`00661A70`) resolves names with `0066F580` over the list `02D38DB8`,
which `0066F4F0` fills, and `PModifier` (`006D5810`) with `006D5AF0` over `02E9FD60`; both return
`13`<sub>h</sub> when no entry has the name.

### Member records

`00632960(record, descriptor, type, name, offset, attrs, flag, context)` builds a
`Phyre::PClassDataMember`. `00632FB0` fills its list node, owner and name, and copies the name into
new storage when attribute bit `1`<sub>h</sub> is set. The constructor stores the type at `+30`<sub>h</sub> and the
offset at `+48`<sub>h</sub>, sets attribute bit `2`<sub>h</sub> for the duration of the call when `flag` is 2, and calls
descriptor slot `+40`<sub>h</sub>.

Slot `+40`<sub>h</sub> is `0062EFD0` in the base, Abstract, Concrete and ForType vtables. It refuses the member with 5 when
`offset − [+F4h] + width + [+F8h]` exceeds the instance size, with `15`<sub>h</sub> when it has no name and
with `12`<sub>h</sub> when `00597220` finds the name in the class or any ancestor; otherwise it appends the
member to the list at `+80`<sub>h</sub> and returns 0. Slot `+48`<sub>h</sub> (`0062F080`) unlinks it again.

The width comes from `0063C0C0`: the context's pointer width (8 with no context) when attribute bit
`2`<sub>h</sub> is set, or when the member is a dynamic array (kind 2) without bit `40`<sub>h</sub>; otherwise the type's
size at `+38`<sub>h</sub>, or the size the context gives a dynamic type.

### Member kinds

| Route | Record | Adds |
|---|---|---|
| `00632960` | `PClassDataMember` | the plain member |
| `00632A10` | `PClassDataMemberArray` | kind at `+5C`<sub>h</sub> (2 a counted buffer such as `PArray<T>::m_els`, 3 a `PArray` member, 4 a `PSharray` member), element size at `+58`<sub>h</sub> |
| `00632A70` | `PClassDataMemberArrayFixedSize` | kind 1 at `+5C`<sub>h</sub>, the type's `+3C`<sub>h</sub> at `+58`<sub>h</sub>, element count at `+60`<sub>h</sub> |
| `00632BE0` | `PClassDataMemberEnum` | attribute bit `20`<sub>h</sub>, a value at `+58`<sub>h</sub> |

A registering function can OR further attribute bits into the record after the call (bit `10`<sub>h</sub>,
`08`<sub>h</sub> or `40`<sub>h</sub>; `00633100` adds `4`<sub>h</sub> when it attaches a dynamic-type helper at `+50`<sub>h</sub>). The
attribute word is what the loader compares against a file's member record. `0063BBA0` returns a
member's type: the helper's answer (its slot `+08`<sub>h</sub>) when a helper is attached, else `+30`<sub>h</sub>.

### Methods and script functions

The same record base built by `00632FB0` is linked into two further lists: `+90`<sub>h</sub> holds the class's
callable methods (`005AD8F0` links `playOnce` after the duplicate check `005A7A40`) and `+A0`<sub>h</sub> the
functions published to the script layer (`005B2860` links `GetGlobalTime` after `005A0470`).

### Annotations

A member's list at `+38`<sub>h</sub> holds annotations. `006B66C0(annotation, key, type, value)` builds a
`30`<sub>h</sub>-byte `Phyre::PAnnotation`, and `006B67D0` links it to a member. All 69 static annotations in
the executable are a `PAnnotationWithValue<unsigned int>` keyed by `02CF8570`, the key `001641C0`
names `WriteMask`, with the value `7FFFFFFF`<sub>h</sub>, on the `m_count` member of a `PArray<T>` or
`PSharray<T>` descriptor. `006B67F0` finds an annotation by key.

### Default instance and masks

Each class registers three static buffers of its instance size: the default instance at `+C0`<sub>h</sub>
(`0063DC80`), and two masks at `+C8`<sub>h</sub> (`0063DF90`) and `+D0`<sub>h</sub> (`0063DFA0`). They are built on first
use, when `+FC`<sub>h</sub> bit `80000000`<sub>h</sub> is clear:

1. `00639A60` fills `+C0`<sub>h</sub> and `+C8`<sub>h</sub> with `A5`<sub>h</sub> and constructs the class into `+C8`<sub>h</sub> through
   slot `+50`<sub>h</sub>. Unless bit `8`<sub>h</sub> is set it constructs again into `+C0`<sub>h</sub> and logs a
   "position dependant constructor" message when the two differ. It copies `+C8`<sub>h</sub> into `+C0`<sub>h</sub>,
   copies the default instances of inline object members with bit `40`<sub>h</sub> or kind 4, and sets bit
   `80000000`<sub>h</sub>.
2. A class whose slot `+50`<sub>h</sub> has no constructor is built by `0063CB80` instead, from its parent's
   and its members' default instances.
3. `00639C80` fills `+C8`<sub>h</sub> with `FF`<sub>h</sub> and `+D0`<sub>h</sub> with zero, copies the parent's masks, then
   clears every byte a member covers in `+C8`<sub>h</sub>, logging an overlap when a byte is already clear.
   For a primitive member it writes the member's `WriteMask` into `+D0`<sub>h</sub>, or `FF`<sub>h</sub> bytes without
   one; for an inline object it copies that class's masks. It sets bit `10000000`<sub>h</sub> when no byte of
   `+C8`<sub>h</sub> is left set.

So `+C8`<sub>h</sub> marks the bytes no member describes and `+D0`<sub>h</sub> the bits that belong to member values.
`0063C5E0` and `0063C1A0` build a class's buffers when needed and return its `+D0`<sub>h</sub> and `+C8`<sub>h</sub>;
`00639C80` uses them for the
masks of inline object members.

### Creating instances

`0063A990(cluster, count, descriptor, …)` is `PCluster::create`. A class with `+FC`<sub>h</sub> bit `8`<sub>h</sub>
logs "has no default constructor and cannot be allocated" and gets nothing. Otherwise `00639510`
refuses an abstract class (bit `2`<sub>h</sub>) and allocates `count × [+38h]` bytes with alignment `[+3Ch]`,
and `0063C910` initialises each instance in turn: it builds the buffers if needed, then copies the
whole default instance over it. Without a default instance it constructs through slot `+50`<sub>h</sub> and
copies the default instance of every inline object member, across the class and its ancestors.

### The cluster's script methods

`00635470` publishes four `PCluster` methods on the cluster descriptor `02CF8780`:

- `create` (`0063AA50`) makes one object: it logs the same "no default constructor" message for bit
  `8`<sub>h</sub>, and otherwise builds a one-object instance list through `00639510`, initialises the object
  at the list's `+58`<sub>h</sub> with `0063C910` and returns the object with its descriptor.
- `deleteObject` is `0063AD20`.
- `deleteInstancesOfType` (`0063AAD0`) removes every instance list of exactly one class: it unlinks
  the list, takes it off the per-type table, destroys its objects (`0063B3E0`), frees its blocks
  (`00680030`) and returns the list record to the cluster's pool at `+50`<sub>h</sub> (`00680200`).
- `absorb` (`00638FB0`) moves every list of another cluster into this one (see below).

A cluster's `+78`<sub>h</sub> points at the world it belongs to, whose per-type table (count `+10`<sub>h</sub>, entries
`+18`<sub>h</sub>) holds `20`<sub>h</sub>-byte entries indexed by each descriptor's
`+EC`<sub>h</sub>. An entry heads the lists of its class and counts their objects at `+10`<sub>h</sub> and the lists at
`+14`<sub>h</sub>. A list is linked under its own class's entry and counted in every ancestor's.

`00638FB0` first merges the other cluster's pool of list records into this one (`00680080`, which
returns 5 when the two pools' record sizes differ). Each list then leaves the per-type table of the other cluster's world
and that cluster's list, joins the end of this cluster's list and its world's table, takes this cluster at its `+48`<sub>h</sub> and is
passed to `00677550`, which, for a list of a class derived from `PAssetReference` (`02D3E680`),
sets every object's `+48`<sub>h</sub> to that cluster. The other cluster's chain at `+48`<sub>h</sub> is moved over last.

`0063D6B0(world, cluster)` takes a cluster whose `+78`<sub>h</sub> is that world off it: it unlinks the
cluster's node at `+88`<sub>h</sub>, clears `+78`<sub>h</sub> and removes each of its lists from the per-type table.

`0063B3E0` calls descriptor slot `+58`<sub>h</sub> on every object of a loaded list (`+7D`<sub>h</sub>) except the slots
on the chain at `+10`<sub>h</sub>, frees the storage when the list owns it (`+7C`<sub>h</sub>) and zeroes the count.

### Member visits

Descriptor slot `+00`<sub>h</sub> walks the members of a class and its ancestors (`0063E2E0`) and hands each
to `0063CE80`, which applies the member type's own slot `+00`<sub>h</sub> to every element through `0059FDB0`.
The flag argument picks the order: non-zero walks each `+80`<sub>h</sub> list forwards, zero backwards, and the
flag is passed on to the member types.

Eight core classes carry the walk inlined for their own descriptor, one copy per order, and their
slot `+00`<sub>h</sub> adapters only choose between the two copies and return 1:

| Class | Descriptor | Slot `+00`<sub>h</sub> | Forward | Backward | Object offset |
|---|---|---|---|---|---|
| `PClassDataMemberDynamic` | `02CF8370` | `0062F3E0` | `00630640` | `00630C80` | `+08`<sub>h</sub> |
| `PClassDescriptor` | `02CF8470` | `0062F0C0` | `006306E0` | `00630D20` | `+30`<sub>h</sub> |
| `PClassMember` | `02CF8680` | `0062F960` | `00630820` | `00630E60` | 0 |
| `PCluster` | `02CF8780` | `0062F200` | `006308C0` | `00630F00` | 0 |
| `PClusterDependencyList` | `02CF8880` | `0062EE00` | `00630960` | `00630FA0` | 0 |
| `PNamespace` | `02CF8980` | `0062F5A0` | `00630A00` | `00631040` | `+10`<sub>h</sub> |
| `PWorld` | `02CF8A80` | `0062F740` | `00630AA0` | `006310E0` | 0 |
| `PSharray<PString>` | from `00635DC0` | `0063DFB0` | `00630500` | `00630B40` | 0 |

The object offset is added to the object pointer before the walk, as the class's reflected layout
starts that far into the object.

### Teardown

The `atexit` thunk `008A8E20` restores the class's descriptor vtable and jumps to `00633390`, the
base destructor:

1. It installs the `PClassDescriptor` vtable and, when its index at `+E8`<sub>h</sub> is the last one handed
   out, decrements `02CF8260`.
2. `0063D640` unlinks `+50`<sub>h</sub> from its namespace and unlinks an emptied non-default namespace.
3. It frees the records of `+90`<sub>h</sub> and `+A0`<sub>h</sub> whose attribute bit `1`<sub>h</sub> is set, with their name,
   then unlinks every remaining node of `+80`<sub>h</sub>, `+90`<sub>h</sub>, `+A0`<sub>h</sub> and `+B0`<sub>h</sub> without freeing it.
4. `006B6700` unlinks every node of `+60`<sub>h</sub>, and the `PType` vtable is installed last.

A member's teardown `00633240` detaches it through its owner's slot `+48`<sub>h</sub>, drains its annotations
and frees a copied name. The deleting destructors such as `005847E0` call `00633390` and, when flag
bit `1`<sub>h</sub> is set, free the object with `_aligned_free` (`00584730`); with bit `4`<sub>h</sub> as well they call
the empty `0016D6A0` and free nothing.

## Layouts

PType (base of every type and descriptor):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | vtable |  |
| `08`<sub>h</sub> | `void*` | type-tree links (three pointers, `+08`<sub>h</sub>..`+1F`<sub>h</sub>) |  |
| `20`<sub>h</sub> | `u32` | name hash, written by 006388C0 |  |
| `28`<sub>h</sub> | `void*` | name, as the tree key |  |
| `30`<sub>h</sub> | `void*` | name |  |
| `38`<sub>h</sub> | `u32` | instance size |  |
| `3C`<sub>h</sub> | `u32` | alignment |  |
| `40`<sub>h</sub> | `void*` | name-writer hook, or null (00637320, 00637350) |  |
| `48`<sub>h</sub> | `void*` | name-resolver hook, or null (006389C0, 00638A50) |  |

Every list in these records is a circular doubly linked list of 16-byte nodes: a list is empty when its
node points at itself, and a member sits in a list through a node inside it (`006B6700` drains one,
taking each member at its node minus 8).

`ListNode` (`10`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | next | the next node, or this node when the list is empty |
| `08`<sub>h</sub> | `void*` | prev | the previous node |

PClassDescriptor (`100`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `50`<sub>h</sub> | `ListNode` | node in the namespace's class list |  |
| `60`<sub>h</sub> | `ListNode` | drained by 006B6700 at teardown |  |
| `70`<sub>h</sub> | `void*` | namespace |  |
| `78`<sub>h</sub> | `void*` | parent descriptor, or null |  |
| `80`<sub>h</sub> | `ListNode` | data members |  |
| `90`<sub>h</sub> | `ListNode` | methods |  |
| `A0`<sub>h</sub> | `ListNode` | script functions |  |
| `B0`<sub>h</sub> | `ListNode` | fourth list, emptied by the constructor and the destructor |  |
| `C0`<sub>h</sub> | `void*` | default instance |  |
| `C8`<sub>h</sub> | `void*` | undescribed-byte mask |  |
| `D0`<sub>h</sub> | `void*` | write mask |  |
| `D8`<sub>h</sub> | `void*` | 0 (zeroed by the constructor) |  |
| `E0`<sub>h</sub> | `void*` | 0 (zeroed by the constructor) |  |
| `E8`<sub>h</sub> | `u32` | registration index (02CF8260) |  |
| `EC`<sub>h</sub> | `u32` | `FFFFFFFF`<sub>h</sub> |  |
| `F0`<sub>h</sub> | `i32` | this class's adjustment |  |
| `F4`<sub>h</sub> | `i32` | sum of adjustments to the root |  |
| `F8`<sub>h</sub> | `i32` | layout base of an instance |  |
| `FC`<sub>h</sub> | `u32` | flags |  |

A list is a `{next, prev}` pair that points at itself when empty; a node sits 8 bytes into its
record, and an owned node has bit `1`<sub>h</sub> at node `+20`<sub>h</sub>.

```
+0xFC flags
0x00000001  dynamic class (built by 00632E80)
0x00000002  abstract: no instance list (00639510)
0x00000008  no default constructor: PCluster::create refuses it
0x08000000  a member is a PSharray, or the parent has the bit
0x10000000  every instance byte is described by a member
0x40000000  members registered (00639450)
0x80000000  default instance and masks built
```

PClassDescriptorDynamic (`140`<sub>h</sub>), beyond the base:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `100`<sub>h</sub> | `u16` | pair compared by 0063D550 to skip a rebuild |  |
| `104`<sub>h</sub> | `u32` | parent's instance size |  |
| `108`<sub>h</sub> | `…` | three {u32, ptr} pairs at `+108`<sub>h</sub>, `+118`<sub>h</sub>, `+128`<sub>h</sub>, zeroed by 00632E80 |  |
| `138`<sub>h</sub> | `void*` | tagged name; `+30`<sub>h</sub> holds it with bit 0 cleared |  |

PClassDataMember (`58`<sub>h</sub>; arrays to +`64`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | vtable |  |
| `08`<sub>h</sub> | `ListNode` | node in the owner's `+80`<sub>h</sub> list |  |
| `18`<sub>h</sub> | `void*` | owning descriptor |  |
| `20`<sub>h</sub> | `void*` | name |  |
| `28`<sub>h</sub> | `u32` | attribute word |  |
| `30`<sub>h</sub> | `void*` | type (a PType or a class descriptor) |  |
| `38`<sub>h</sub> | `ListNode` | annotations |  |
| `48`<sub>h</sub> | `u32` | offset in the owner's layout |  |
| `50`<sub>h</sub> | `void*` | dynamic-type helper, or null |  |
| `58`<sub>h</sub> | `u32` | element size (arrays) |  |
| `5C`<sub>h</sub> | `u32` | array kind |  |
| `60`<sub>h</sub> | `u32` | element count (fixed arrays) |  |

PAnnotation (`30`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | vtable |  |
| `08`<sub>h</sub> | `ListNode` | node in a member's `+38`<sub>h</sub> list |  |
| `18`<sub>h</sub> | `void*` | key (02CF8570 for WriteMask) |  |
| `20`<sub>h</sub> | `void*` | value type |  |
| `28`<sub>h</sub> | `u32` | fourth constructor argument |  |
| `30`<sub>h</sub> | `u32` | value (PAnnotationWithValue&lt;unsigned int&gt;) |  |

```
attribute word (member +0x28)
0x01  name copied into owned storage; freed at teardown
0x02  stored as a pointer
0x04  dynamic-type helper attached (00633100)
0x08, 0x10  set per class by the registering function
0x20  enum member (00632BE0)
0x40  a kind-2 array measured and defaulted inline, not as a pointer (PSharray<T>::m_u)
```

Descriptor vtable slots (PClassDescriptorConcrete&lt;PAnimatableComponent&gt;, `00D29E90`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `visit` | every | member of the class and its ancestors (`0063E2E0`) |
| `18`<sub>h</sub> | `get` | the | value from a script context |
| `20`<sub>h</sub> | `put` | the | value into a script context |
| `38`<sub>h</sub> | `scalar` | deleting | destructor |
| `40`<sub>h</sub> | `attach` | a | member (`0062EFD0`) |
| `48`<sub>h</sub> | `detach` | a | member (`0062F080`) |
| `50`<sub>h</sub> | `construct` | in | place; returns false for a class without one (`00657140`) |
| `58`<sub>h</sub> | `destruct` | in | place (`0063FC60`) |
| `60`<sub>h</sub> | `register` | the | members (_purecall in ForType&lt;T&gt;) |

## Shipped data

| Fact | Value |
|---|---|
| static descriptor constructions | 399: 384 calls to `00632D80` and 15 to `00632C90` (a 385th call is inside `00632E80`); `PBase` (`02CF8270`, size 1) and `PClassDescriptor` (`02CF8470`, size `100`<sub>h</sub>) by their own initialisers |
| member registrations | 682 calls to `00632960` (2 of them the array and dynamic constructors forwarding), 165 to `00632A10`, 29 to `00632A70`, 21 to `00632BE0` |
| plain-member attribute arguments | `10`<sub>h</sub> 207, `00`<sub>h</sub> 196, `08`<sub>h</sub> 123, `12`<sub>h</sub> 79, `0A`<sub>h</sub> 39, `02`<sub>h</sub> 36; the flag argument is 0 at all 680 |
| array kinds | `PArray` 86, pointer array 70, `PSharray` 9; element sizes 8 (113), 4 (36), 1 (7), 2 (6), 16 (3) |
| annotations | 70 constructions; 69 static `WriteMask` annotations (60 `PArray`, 9 `PSharray`) |
| buffers | 384 classes register a default instance and both masks |
| by-name registrations | `006388C0`: 523 sites, 516 calls and 7 tail jumps; `00639450`: 471 sites, 156 calls and 315 tail jumps |
| base destructor | `00633390`: 1,981 sites, 1,186 calls and 795 jumps from the destructor thunks |
| RTTI classes | `PClassDescriptorForType<T>` 409, `Abstract<T>` 393, `Concrete<T>` 331, `WithoutDefaultConstructor<T>` 38, `Wrapper<T>` 15, `PTypeDefault<T>` 12, `PClassDataMemberArrayDynamic<T>` 71, `PClassDataMemberPhyreArray<T>` 59 |

### Data files

These tables stay beside this page. Each lists one generated family or one per-class view.

| File | Rows | What it lists |
|---|---:|---|
| [phyre-reflection-abstract-class-descriptor-constructors.tsv](phyre-reflection-abstract-class-descriptor-constructors.tsv) | 177 | Abstract descriptor constructors such as `005A7ED0` |
| [phyre-reflection-abstract-class-descriptor-base-aware-constructors.tsv](phyre-reflection-abstract-class-descriptor-base-aware-constructors.tsv) | 131 | Abstract constructors that pass a parent descriptor |
| [phyre-reflection-pclassdescriptor-static-initialisers.tsv](phyre-reflection-pclassdescriptor-static-initialisers.tsv) | 253 | Concrete static initialisers such as `001603E0` |
| [phyre-reflection-descriptor-flag-registrars.tsv](phyre-reflection-descriptor-flag-registrars.tsv) | 33 | descriptor initialisers, 64-byte form |
| [phyre-reflection-descriptor-flag-registrars-compact.tsv](phyre-reflection-descriptor-flag-registrars-compact.tsv) | 4 | descriptor initialisers, 53-byte form |
| [phyre-reflection-guarded-class-registration-stubs.tsv](phyre-reflection-guarded-class-registration-stubs.tsv) | 98 | thread-safe guarded class registrars |
| [phyre-reflection-name-only-class-registration-initialisers.tsv](phyre-reflection-name-only-class-registration-initialisers.tsv) | 110 | initialisers that call `006388C0` and jump to `00639450` |
| [phyre-reflection-two-member-descriptor-registrars.tsv](phyre-reflection-two-member-descriptor-registrars.tsv) | 38 | array descriptors with `m_count` and `m_els` |
| [phyre-reflection-phyre-registrar-classes.tsv](phyre-reflection-phyre-registrar-classes.tsv) | 409 | registrars and the classes they name |
| [phyre-reflection-phyre-type-name-hashes.tsv](phyre-reflection-phyre-type-name-hashes.tsv) | 399 | type names and their `006388C0` hashes |
| [phyre-reflection-phyre-class-instance-sizes.tsv](phyre-reflection-phyre-class-instance-sizes.tsv) | 177 | instance size and alignment per class |
| [phyre-reflection-phyre-class-parent-chain.tsv](phyre-reflection-phyre-class-parent-chain.tsv) | 330 | parent descriptor per class |
| [phyre-reflection-phyre-class-f4-offset-adjustment.tsv](phyre-reflection-phyre-class-f4-offset-adjustment.tsv) | 179 | `+F4`<sub>h</sub> per class |
| [phyre-reflection-phyre-default-instances.tsv](phyre-reflection-phyre-default-instances.tsv) | 173 | default instance per class |
| [phyre-reflection-phyre-class-default-buffers.tsv](phyre-reflection-phyre-class-default-buffers.tsv) | 384 | the `+C0`<sub>h</sub>, `+C8`<sub>h</sub> and `+D0`<sub>h</sub> buffers per class |
| [phyre-reflection-phyre-class-descriptor-vtable.tsv](phyre-reflection-phyre-class-descriptor-vtable.tsv) | 315 | each class's descriptor vtable and its slots |
| [phyre-reflection-phyre-class-descriptor-accesses.tsv](phyre-reflection-phyre-class-descriptor-accesses.tsv) | 168 | instructions that access descriptor fields |
| [phyre-reflection-p-type-default-u-int-accesses.tsv](phyre-reflection-p-type-default-u-int-accesses.tsv) | 16 | accesses to the `PTypeDefault<unsigned int>` object |
| [phyre-reflection-ptexture2d-d3d11-accesses.tsv](phyre-reflection-ptexture2d-d3d11-accesses.tsv) | 24 | accesses to a `PTexture2DD3D11`, from its constructor `006160B0` |
| [phyre-reflection-ptexture-cube-map-d3d11-accesses.tsv](phyre-reflection-ptexture-cube-map-d3d11-accesses.tsv) | 95 | accesses to a `PTextureCubeMapD3D11`, from its constructor `006161A0` (placement constructor `00612D00`) |
| [phyre-reflection-rtti-class-vtables.tsv](phyre-reflection-rtti-class-vtables.tsv) | 2,286 | class name to vtable for every polymorphic class |
| [phyre-reflection-pclassdescriptorconcrete-placement-default-ctors.tsv](phyre-reflection-pclassdescriptorconcrete-placement-default-ctors.tsv) | 123 | slot `+50`<sub>h</sub> construct-in-place bodies |
| [phyre-reflection-object-traversal-adapters.tsv](phyre-reflection-object-traversal-adapters.tsv) | 304 | slot `+00`<sub>h</sub> member-visit adapters |
| [phyre-reflection-flag-selected-traversal-adapters.tsv](phyre-reflection-flag-selected-traversal-adapters.tsv) | 11 | member-visit adapters that pass the order flag |
| [phyre-reflection-registry-fetch-traversal-adapters.tsv](phyre-reflection-registry-fetch-traversal-adapters.tsv) | 84 | member-visit adapters that fetch their descriptor first |
| [phyre-reflection-object-lifecycle-lookup-adapters.tsv](phyre-reflection-object-lifecycle-lookup-adapters.tsv) | 6 | adapters that call `0063BC00` |
| [phyre-reflection-shared-runtime-identity-dispatch-adapters.tsv](phyre-reflection-shared-runtime-identity-dispatch-adapters.tsv) | 6 | adapters that call `00639850` |
| [phyre-reflection-static-descriptor-singleton-lazyinit-adapters.tsv](phyre-reflection-static-descriptor-singleton-lazyinit-adapters.tsv) | 7 | guarded descriptor singletons |
| [phyre-reflection-nativeadapter-staticdescriptorsingletonlazyinit2.tsv](phyre-reflection-nativeadapter-staticdescriptorsingletonlazyinit2.tsv) | 5 | guarded descriptor singletons, second form |
| [phyre-reflection-nativeadapter-staticdescriptorsingletonlazyinit3.tsv](phyre-reflection-nativeadapter-staticdescriptorsingletonlazyinit3.tsv) | 4 | guarded descriptor singletons, third form |
| [phyre-reflection-nativeadapter-singletonallocdescriptorinstall.tsv](phyre-reflection-nativeadapter-singletonallocdescriptorinstall.tsv) | 5 | adapters that allocate an 8-byte object and install a descriptor |
| [phyre-reflection-nativeadapter-descriptorfieldselecttail.tsv](phyre-reflection-nativeadapter-descriptorfieldselecttail.tsv) | 4 | adapters that select a descriptor field |
| [phyre-reflection-class-descriptor-static-teardowns.tsv](phyre-reflection-class-descriptor-static-teardowns.tsv) | 403 | descriptor `atexit` teardowns such as `008A8E20` |
| [phyre-reflection-pclassdescriptor-destructor-thunks.tsv](phyre-reflection-pclassdescriptor-destructor-thunks.tsv) | 383 | thunks that restore a vtable and jump to `00633390` |
| [phyre-reflection-pclassdescriptor-deleting-destructors.tsv](phyre-reflection-pclassdescriptor-deleting-destructors.tsv) | 1,147 | ForType deleting destructors such as `005847E0` |
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

- **Find a class by name.** `0063BA10(namespace, name)`; the default namespace is `006373D0()`.
- **Find a type by name.** Hash as in `006388C0` and walk the tree at `01F2E780` with `006311D0`.
- **Find a member.** `00597220(descriptor, name)` searches the class, then its ancestors.
- **Create instances.** `0063A990(cluster, count, descriptor, …)`; `0063C910(descriptor, object)`
  initialises one object from the default instance.
- **Visit members.** Descriptor slot `+00`<sub>h</sub> walks every member of the class and its ancestors.

## State

| Address | What |
|---|---|
| `02CF8260` | next descriptor index |
| `01F2E330` | default namespace |
| `01F2E780` | type-tree header |
| `02CF8270` | `PBase`, the root descriptor |
| `02CF8470` | the descriptor of `PClassDescriptor` |
| `02CF8570` | the `WriteMask` annotation key |

## Modding notes

- A class's members exist only in code. A new field needs a new registration; a file cannot add one
  to a static class.
- Members are found by exact name, through the class and its ancestors. Names are case-sensitive
  even though their hash is not.
- New objects start as a copy of the default instance, so bytes no member describes still hold the
  constructor's values.
- The reflection layer reports problems through the Phyre log call `005CDAA0`, whose output the
  shipped game never shows.
- Descriptors are aligned allocations; release them with `_aligned_free`.

## Related

- [Class hierarchy](../Engine-Core/class-hierarchy.md): the RTTI that names every descriptor template.
- [Debug logging](../Engine-Core/debug-logging.md): where the reflection layer's messages go.
- [Lua runtime](../Third-Party-Libraries/lua-runtime.md): the Lua interpreter linked beside PhyreEngine.
- [Bullet physics](../Third-Party-Libraries/bullet-physics.md): the physics classes registered here.
- [Bigfile archive](../Game-Files-And-Data-Tables/bigfile-archive.md): where the `.phyre` files are stored.
