---
title: "Phyre reflection: how PhyreEngine describes its classes at run time, registers their members and creates instances"
kind: "system"
category: "PhyreEngine"
summary: "PhyreEngine's run-time class reflection in the executable: the 0x100-byte class descriptor and its registration in a namespace and a by-name type tree, the member records that give each field's name, type, offset and attribute word, array members and annotations, the default instance and the two masks built per class, how PCluster::create sizes and initialises instances, how descriptors are torn down, and the data files that list the generated functions and the per-class field accesses."
addresses: ["00632D80", "00632C90", "00632E80", "005A7ED0", "001603E0", "00639450", "00639160", "0063E410", "006388C0", "006311D0", "0063BA10", "00632960", "00632FB0", "00632A10", "00632A70", "00632BE0", "0062EFD0", "0062F080", "00597220", "0063C0C0", "006B66C0", "006B67D0", "006B67F0", "0063A990", "00639510", "0063C910", "00639A60", "00639C80", "0063CB80", "00633390", "0063D550", "0063D640", "006B6700", "00633240", "005847E0", "00584730", "02CF8260", "01F2E330", "01F2E780", "02CF8270", "02CF8470", "02CF8570"]
---

# Phyre reflection: how PhyreEngine describes its classes at run time, registers their members and creates instances

## What the player sees

Nothing directly. Every model, texture, shader, animation and scene the game loads from a `.phyre`
file becomes an object through this layer: the loader finds each class in the file by name, matches
its fields to the members registered here, and builds instances from the class's default instance.
A class or field the executable does not register cannot be brought in by editing assets.

## How it works

### The class descriptor and its types

Each reflected class has one descriptor, a `Phyre::PClassDescriptor` object of `0x100` bytes. The
constructor `00632D80(descriptor, namespace, name, size, alignment, parent, adjust)` empties the six
list heads, stores the name pointer at `+0x30`, the instance size at `+0x38`, the alignment at
`+0x3C`, the namespace at `+0x70`, the parent descriptor at `+0x78` and the adjustment at `+0xF0`,
and takes the next value of the global counter `02CF8260` as its index at `+0xE8`. `00632C90` is
the same without a parent or adjustment.

The vtable it installs is replaced by the class's own: `PClassDescriptorAbstract<T>`,
`PClassDescriptorConcrete<T>` or `PClassDescriptorForType<T>`, all derived from `PClassDescriptor`,
which derives from `Phyre::PType`.

`PClassDescriptorDynamic` (`00632E80`) is a `0x140`-byte form that copies its name and is built at
load time for a class no code registers. Its attach slot
`00639290` counts accepted members in the two words at `+0x100` and `+0x102`, and when they differ
first rebuilds the descriptor through `0063D550` (empty the six lists, copy the parent's size and
alignment, recompute the offsets).

### Registration

A class is registered in two steps:

1. Its descriptor is built. For most classes this runs before `main`: the C runtime's initialiser
   table holds `001603E0`, which calls the Abstract constructor `005A7ED0`
   (`00632D80(…, "PAnimatableComponent", 0x108, 8, …, 8)`, flag `+0xFC` bit `0x2`, the three buffers
   below), installs the Concrete vtable, clears bit `0x2` and registers the teardown `008A8E20`.
   Template classes such as `PArray<T>` are built on first use inside a thread-safe static.
2. Its members are registered by descriptor slot `+0x60` (for `PAnimatableComponent`, `005A25E0`
   jumps to `005AD8F0`), each member behind its own thread-safe static, and the function ends in the
   finaliser `00639450`.

The finaliser calls `00639160`, which looks the name up in the namespace (`0063BA10`), reports a
second class of the same name, and otherwise links the descriptor's `+0x50` node into the namespace's
class list: at the front, or straight after its parent when the parent belongs to the same namespace.
When the namespace state is 1 or 2 it also computes the layout offsets (`0063E410`). The finaliser
then sets `+0xFC` bit `0x40000000`, the mark that members are registered.

### Layout offsets

`0063E410` sums `+0xF0` over the class and every ancestor up to the root descriptor `02CF8270`
into `+0xF4`, and stores the class's own non-negative `+0xF0` plus the parent's `+0xF8` in `+0xF8`.
A member's position in an object is its registered offset minus the owning class's `+0xF4`
(`0063C910`, `00639C80`, `0063CB80`). `PAnimatableComponent` passes 8: its reflected layout starts
8 bytes into the object, after the vtable pointer. Its member visitor `005A2390` is handed
`object + 8`, and descriptor slot `+0x58` (`0063FC60`) steps back 8 bytes to call the object's own
destructor.

### The type tree and the namespace

`006388C0` registers a descriptor in the global type tree whose header is `01F2E780` (returned by
`00637440`). It hashes the name from `0x7B5`, multiplying by 33 and adding the low five bits of each
byte, stores the hash at `+0x20` and the name at `+0x28`, and inserts `+0x08` into an ordered tree.
It returns false when the name is already present. The lookup `006311D0` orders by hash first and
compares the full string on equal hashes, so case-only differences collide in the hash but never
match.

A namespace is a separate structure: the default one is `01F2E330` (returned by `006373D0`), its
classes hang off `+0x10`, and child namespaces off `+0x28`. `0063BA10` searches a namespace's own
classes, then each child namespace, with an exact byte comparison.

### Member records

`00632960(record, descriptor, type, name, offset, attrs, flag, context)` builds a
`Phyre::PClassDataMember`. `00632FB0` fills its list node, owner and name, and copies the name into
new storage when attribute bit `0x1` is set. The constructor stores the type at `+0x30` and the
offset at `+0x48`, sets attribute bit `0x2` for the duration of the call when `flag` is 2, and calls
descriptor slot `+0x40`.

Slot `+0x40` is `0062EFD0` in the base, Abstract, Concrete and ForType vtables. It refuses the member with 5 when
`offset − [+0xF4] + width + [+0xF8]` exceeds the instance size, with `0x15` when it has no name and
with `0x12` when `00597220` finds the name in the class or any ancestor; otherwise it appends the
member to the list at `+0x80` and returns 0. Slot `+0x48` (`0062F080`) unlinks it again.

The width comes from `0063C0C0`: the context's pointer width (8 with no context) when attribute bit
`0x2` is set, or when the member is a dynamic array (kind 2) without bit `0x40`; otherwise the type's
size at `+0x38`, or the size the context gives a dynamic type.

### Member kinds

| Route | Record | Adds |
|---|---|---|
| `00632960` | `PClassDataMember` | the plain member |
| `00632A10` | `PClassDataMemberArray` | kind at `+0x5C` (2 a counted buffer such as `PArray<T>::m_els`, 3 a `PArray` member, 4 a `PSharray` member), element size at `+0x58` |
| `00632A70` | `PClassDataMemberArrayFixedSize` | kind 1 at `+0x5C`, the type's `+0x3C` at `+0x58`, element count at `+0x60` |
| `00632BE0` | `PClassDataMemberEnum` | attribute bit `0x20`, a value at `+0x58` |

A registering function can OR further attribute bits into the record after the call (bit `0x10`,
`0x08` or `0x40`; `00633100` adds `0x4` when it attaches a dynamic-type helper at `+0x50`). The
attribute word is what the loader compares against a file's member record.

### Methods and script functions

The same record base built by `00632FB0` is linked into two further lists: `+0x90` holds the class's
callable methods (`005AD8F0` links `playOnce` after the duplicate check `005A7A40`) and `+0xA0` the
functions published to the script layer (`005B2860` links `GetGlobalTime` after `005A0470`).

### Annotations

A member's list at `+0x38` holds annotations. `006B66C0(annotation, key, type, value)` builds a
`0x30`-byte `Phyre::PAnnotation`, and `006B67D0` links it to a member. All 69 static annotations in
the executable are a `PAnnotationWithValue<unsigned int>` keyed by `02CF8570`, the key `001641C0`
names `WriteMask`, with the value `0x7FFFFFFF`, on the `m_count` member of a `PArray<T>` or
`PSharray<T>` descriptor. `006B67F0` finds an annotation by key.

### Default instance and masks

Each class registers three static buffers of its instance size: the default instance at `+0xC0`
(`0063DC80`), and two masks at `+0xC8` (`0063DF90`) and `+0xD0` (`0063DFA0`). They are built on first
use, when `+0xFC` bit `0x80000000` is clear:

1. `00639A60` fills `+0xC0` and `+0xC8` with `0xA5` and constructs the class into `+0xC8` through
   slot `+0x50`. Unless bit `0x8` is set it constructs again into `+0xC0` and logs a
   "position dependant constructor" message when the two differ. It copies `+0xC8` into `+0xC0`,
   copies the default instances of inline object members with bit `0x40` or kind 4, and sets bit
   `0x80000000`.
2. A class whose slot `+0x50` has no constructor is built by `0063CB80` instead, from its parent's
   and its members' default instances.
3. `00639C80` fills `+0xC8` with `0xFF` and `+0xD0` with zero, copies the parent's masks, then
   clears every byte a member covers in `+0xC8`, logging an overlap when a byte is already clear.
   For a primitive member it writes the member's `WriteMask` into `+0xD0`, or `0xFF` bytes without
   one; for an inline object it copies that class's masks. It sets bit `0x10000000` when no byte of
   `+0xC8` is left set.

So `+0xC8` marks the bytes no member describes and `+0xD0` the bits that belong to member values.

### Creating instances

`0063A990(cluster, count, descriptor, …)` is `PCluster::create`. A class with `+0xFC` bit `0x8`
logs "has no default constructor and cannot be allocated" and gets nothing. Otherwise `00639510`
refuses an abstract class (bit `0x2`) and allocates `count × [+0x38]` bytes with alignment `[+0x3C]`,
and `0063C910` initialises each instance in turn: it builds the buffers if needed, then copies the
whole default instance over it. Without a default instance it constructs through slot `+0x50` and
copies the default instance of every inline object member, across the class and its ancestors.

### Teardown

The `atexit` thunk `008A8E20` restores the class's descriptor vtable and jumps to `00633390`, the
base destructor:

1. It installs the `PClassDescriptor` vtable and, when its index at `+0xE8` is the last one handed
   out, decrements `02CF8260`.
2. `0063D640` unlinks `+0x50` from its namespace and unlinks an emptied non-default namespace.
3. It frees the records of `+0x90` and `+0xA0` whose attribute bit `0x1` is set, with their name,
   then unlinks every remaining node of `+0x80`, `+0x90`, `+0xA0` and `+0xB0` without freeing it.
4. `006B6700` unlinks every node of `+0x60`, and the `PType` vtable is installed last.

A member's teardown `00633240` detaches it through its owner's slot `+0x48`, drains its annotations
and frees a copied name. The deleting destructors such as `005847E0` call `00633390` and, when flag
bit `0x1` is set, free the object with `_aligned_free` (`00584730`); with bit `0x4` as well they call
the empty `0016D6A0` and free nothing.

## Layouts

```
PType (base of every type and descriptor)
+0x00  ptr   vtable
+0x08  ptr   type-tree links (three pointers, +0x08..+0x1F)
+0x20  u32   name hash, written by 006388C0
+0x28  ptr   name, as the tree key
+0x30  ptr   name
+0x38  u32   instance size
+0x3C  u32   alignment
+0x40  u64   0
+0x48  u64   0
```

```
PClassDescriptor (0x100)
+0x50  list  node in the namespace's class list
+0x60  list  drained by 006B6700 at teardown
+0x70  ptr   namespace
+0x78  ptr   parent descriptor, or null
+0x80  list  data members
+0x90  list  methods
+0xA0  list  script functions
+0xB0  list  fourth list, emptied by the constructor and the destructor
+0xC0  ptr   default instance
+0xC8  ptr   undescribed-byte mask
+0xD0  ptr   write mask
+0xD8  ptr   0 (zeroed by the constructor)
+0xE0  ptr   0 (zeroed by the constructor)
+0xE8  u32   registration index (02CF8260)
+0xEC  u32   0xFFFFFFFF
+0xF0  i32   this class's adjustment
+0xF4  i32   sum of adjustments to the root
+0xF8  i32   layout base of an instance
+0xFC  u32   flags
```

A list is a `{next, prev}` pair that points at itself when empty; a node sits 8 bytes into its
record, and an owned node has bit `0x1` at node `+0x20`.

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

```
PClassDescriptorDynamic (0x140), beyond the base
+0x100  u16  pair compared by 0063D550 to skip a rebuild
+0x104  u32  parent's instance size
+0x108  …    three {u32, ptr} pairs at +0x108, +0x118, +0x128, zeroed by 00632E80
+0x138  ptr  tagged name; +0x30 holds it with bit 0 cleared
```

```
PClassDataMember (0x58; arrays to +0x64)
+0x00  ptr   vtable
+0x08  list  node in the owner's +0x80 list
+0x18  ptr   owning descriptor
+0x20  ptr   name
+0x28  u32   attribute word
+0x30  ptr   type (a PType or a class descriptor)
+0x38  list  annotations
+0x48  u32   offset in the owner's layout
+0x50  ptr   dynamic-type helper, or null
+0x58  u32   element size (arrays)
+0x5C  u32   array kind
+0x60  u32   element count (fixed arrays)
```

```
PAnnotation (0x30)
+0x00  ptr   vtable
+0x08  list  node in a member's +0x38 list
+0x18  ptr   key (02CF8570 for WriteMask)
+0x20  ptr   value type
+0x28  u32   fourth constructor argument
+0x30  u32   value (PAnnotationWithValue<unsigned int>)
```

```
attribute word (member +0x28)
0x01  name copied into owned storage; freed at teardown
0x02  stored as a pointer
0x04  dynamic-type helper attached (00633100)
0x08, 0x10  set per class by the registering function
0x20  enum member (00632BE0)
0x40  a kind-2 array measured and defaulted inline, not as a pointer (PSharray<T>::m_u)
```

```
descriptor vtable slots (PClassDescriptorConcrete<PAnimatableComponent>, 00D29E90)
+0x00  visit every member of the class and its ancestors (0063E2E0)
+0x18  get the value from a script context
+0x20  put the value into a script context
+0x38  scalar deleting destructor
+0x40  attach a member (0062EFD0)
+0x48  detach a member (0062F080)
+0x50  construct in place; returns false for a class without one (00657140)
+0x58  destruct in place (0063FC60)
+0x60  register the members (_purecall in ForType<T>)
```

## Shipped data

| Fact | Value |
|---|---|
| static descriptor constructions | 399: 384 calls to `00632D80` and 15 to `00632C90` (a 385th call is inside `00632E80`); `PBase` (`02CF8270`, size 1) and `PClassDescriptor` (`02CF8470`, size `0x100`) by their own initialisers |
| member registrations | 682 calls to `00632960` (2 of them the array and dynamic constructors forwarding), 165 to `00632A10`, 29 to `00632A70`, 21 to `00632BE0` |
| plain-member attribute arguments | `0x10` 207, `0x00` 196, `0x08` 123, `0x12` 79, `0x0A` 39, `0x02` 36; the flag argument is 0 at all 680 |
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
| [phyre-reflection-phyre-class-f4-offset-adjustment.tsv](phyre-reflection-phyre-class-f4-offset-adjustment.tsv) | 179 | `+0xF4` per class |
| [phyre-reflection-phyre-default-instances.tsv](phyre-reflection-phyre-default-instances.tsv) | 173 | default instance per class |
| [phyre-reflection-phyre-class-default-buffers.tsv](phyre-reflection-phyre-class-default-buffers.tsv) | 384 | the `+0xC0`, `+0xC8` and `+0xD0` buffers per class |
| [phyre-reflection-phyre-class-descriptor-vtable.tsv](phyre-reflection-phyre-class-descriptor-vtable.tsv) | 315 | each class's descriptor vtable and its slots |
| [phyre-reflection-phyre-class-descriptor-accesses.tsv](phyre-reflection-phyre-class-descriptor-accesses.tsv) | 168 | instructions that access descriptor fields |
| [phyre-reflection-p-type-default-u-int-accesses.tsv](phyre-reflection-p-type-default-u-int-accesses.tsv) | 16 | accesses to the `PTypeDefault<unsigned int>` object |
| [phyre-reflection-rtti-class-vtables.tsv](phyre-reflection-rtti-class-vtables.tsv) | 2,286 | class name to vtable for every polymorphic class |
| [phyre-reflection-pclassdescriptorconcrete-placement-default-ctors.tsv](phyre-reflection-pclassdescriptorconcrete-placement-default-ctors.tsv) | 123 | slot `+0x50` construct-in-place bodies |
| [phyre-reflection-object-traversal-adapters.tsv](phyre-reflection-object-traversal-adapters.tsv) | 303 | slot `+0x00` member-visit adapters |
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
- **Visit members.** Descriptor slot `+0x00` walks every member of the class and its ancestors.

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
