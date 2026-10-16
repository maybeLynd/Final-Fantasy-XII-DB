---
title: "Phyre field schema: the class and member tables in every .phyre file and how the loader matches them to registered members"
kind: "format"
category: "PhyreEngine"
summary: "The packed namespace each .phyre file carries after its 84-byte header: the type table, the nine-word class records and six-word member records with their names, file offsets, widths and attribute words; how the loader checks it, finds each class and member by name in the run-time reflection data, reports differences and picks a copy routine per member; and the shipped figures, in which every class and member a file declares is registered by the executable."
addresses: ["0059E070", "0059A3B0", "0059B430", "0059BA40", "0059D2D0", "0059AC00", "006393A0", "00632B30", "00632E80", "0063BA10", "00597220", "00632960", "00632A10", "00632A70", "00632BE0", "0062EFD0", "00633100", "006318A0", "00631C40", "00599390", "00595E70", "0059A030", "0016D6A0", "005CDAA0"]
---

# Phyre field schema: the class and member tables in every .phyre file and how the loader matches them to registered members

## What the player sees

Nothing directly. Each model, texture, shader and scene file states which classes and fields its
data was written with, and the game lines that list up with the fields the executable registers
before it copies any data. Because the shipped files and the executable agree on every class and
field name, every asset loads through the plain path.

## Where it comes from

Every `.phyre` file starts with a cluster header whose marker is `RYHP` and whose size `m_size` is
84 in every shipped file; the packed namespace follows at byte 84 and is `m_packedNamespaceSize`
bytes long. `0059E070` reads the header through `0059A3B0`, then the namespace.

The other half is the executable's own registrations: every reflected member is registered by one
of four constructors (`00632960` plain, `00632A10` array, `00632A70` fixed-size array, `00632BE0`
enum), each passing the class descriptor, the member's type, name, byte offset and attribute word.

## Layouts

```
packed namespace (at m_size)
+0x00  u32  0x01020304, byte-order mark
+0x04  u32  namespace size (equals m_packedNamespaceSize)
+0x08  u32  nTypes
+0x0C  u32  nClasses
+0x10  u32  nMembers
+0x14  u32  stringPoolSize
+0x18  u32  0 in every shipped file
+0x1C  u32  size of an optional block, 0 in every shipped file
+0x20  u32  string-pool offset of each type name [nTypes]
       ...  class records, 9 u32 each [nClasses]
       ...  member records, 6 u32 each [nMembers]
       ...  NUL-separated string pool [stringPoolSize]
```

```
class record (9 u32)
w0  parent: 1-based index of the parent class record, 0 for none
w1  top 4 bits 0..4; low 28 bits the size of one record of the class in the file layout
w2  name, string-pool offset
w3  number of member records that follow for this class
w4  0
w5  0
w6  0
w7  flags; bit 0x1 asks for a dynamic class when no registered class matches
w8  0
```

Members are stored in class order: class *i* owns the next `w3` member records, and the sum of
`w3` over the classes is `nMembers` in every shipped file.

```
member record (6 u32)
w0  name, string-pool offset
w1  type: a type-table index when below nTypes, else nTypes + 1-based class index
w2  offset in the file layout of the class
w3  width in the file layout (one element for a fixed-size array)
w4  attribute word; bit 0x80000000 marks a counted buffer (PArray<T>::m_els, PSharray<T>::m_u, PString::m_buffer)
w5  element count of a fixed-size array, otherwise 0
```

The attribute word in `w4`, with bit 31 masked off, is the run-time member's attribute word: bit
`0x2` a pointer, `0x4` a dynamic-type helper, `0x20` an enum, `0x40` an inline counted buffer, and
the per-class bits `0x08` and `0x10`.

```
registration call (00632960), Win64 arguments
rcx         record
rdx         class descriptor
r8          type (a PType or class descriptor)
r9          member name
[rsp+0x20]  byte offset in the run-time layout
[rsp+0x28]  attribute word
[rsp+0x30]  0 at every static site
[rsp+0x38]  context passed to the attach slot
```

`00632A10` adds the array kind and element size as arguments 7 and 8, `00632A70` the element count
as argument 7, and `00632BE0` ORs `0x20` into the attribute word. A registering function may OR
`0x08`, `0x10` or `0x40` into the record afterwards, and `00633100` adds `0x4`.

### File layout against run-time layout

The file offset is not the run-time offset. Of the 527 class and member pairs shipped files declare,
250 have the same offset in both; of the 154 classes with members, 41 have every member at its
run-time offset, for example `PClusterHeaderBase`, whose 18 fields sit at 0 to 68 in both. The other
113 are packed: in `PAssetReference`, `m_id`, `m_asset` and `m_assetType` sit at file offsets 0, 1
and 2 with width 1, against run-time offsets inside a `0x50`-byte object. An object pointer has
width 1 and a `PArray` member width 5 in a packed class.

## Shipped data

| Fact | Value |
|---|---|
| `.phyre` files | 35,984; `m_size` 84 in all |
| namespaces passing the byte-order mark and the size identity | 35,984 |
| `+0x18` and `+0x1C` | 0 in every file |
| records | 201,576 type entries, 684,244 class records, 2,192,621 member records |
| distinct names | 19 type-table names, 177 class names, 349 member names, 527 class and member pairs |
| type-table names | `PAnimationKeyDataType`, `PChar`, `PContextSwitch`, `PInt16`, `PInt32`, `PLODBlendType`, `PLODMetricType`, `PLightType`, `PModifier`, `PRenderDataType`, `PSceneRenderPassType`, `PShadowCasterType`, `PTextureFormatBase`, `PUInt128`, `PUInt16`, `PUInt32`, `PUInt8`, `bool`, `float` |
| class records with `w7` bit `0x1` | 0 |
| `w7` values | 0 (523,918), 8 (66,379), 32 (49,068), 2 (38,322), 12, 34 and 40 (2,184 each), 20 (5) |
| fixed-size arrays (`w5` non-zero) | 16 pairs, counts 2 to 23 |
| class names with a registered descriptor of that name | 177 of 177 (`PBase` and `PClassDescriptor` from `006318A0` and `00631C40`) |
| pairs registered statically under that class | 527 of 527 |
| member records whose `w4` & `0x7FFFFFFF` equals the run-time attribute word | 2,192,621 of 2,192,621 |
| static member registrations in the executable | 895 (680 plain, 165 array, 29 fixed-size, 21 enum) over 278 descriptors |

`PArray<T>` and `PSharray<T>` appear in files under their full instantiation names
(`PArray<PAnimationChannel *>`); each is registered by its own template descriptor.

### Data files

| File | Rows | What it lists |
|---|---:|---|
| [phyre-field-schema-field-schema.tsv](phyre-field-schema-field-schema.tsv) | 686 | registered members: class, member, offset, type, attribute word, registration site |
| [phyre-field-schema-accessor-fields.tsv](phyre-field-schema-accessor-fields.tsv) | 73 | member offsets and widths read from script-accessor adapters |

## Loader behaviour

### Checking the namespace

`0059E070` returns `0x15` when the byte at `02CA9D90` is clear and `0xB` when the stream's slot
`+0x10` check fails. After the header it accepts the namespace only when it starts with `0x01020304` and
`+0x04 == +0x1C + 0x20 + 4 × (nTypes + 9 × nClasses + 6 × nMembers) + stringPoolSize`; otherwise it
returns 6. It then matches the tables (`0059B430`), handles dynamic classes (`0059AC00`) and reads
the instances (`0059E300`).

### Matching by name

`0059B430` resolves everything by name:

- **Types.** Each type-table name is hashed and looked up in the global type tree; a miss logs
  "Unable to find type".
- **Classes.** Each class name is looked up in the type tree and must belong to the target
  namespace, then in the namespace itself (`0063BA10`). A miss with `w7` bit `0x1` clear logs "File
  refers to compiled class … which does not exist in the current runtime".
- **Members.** Each member name is searched in the matched class's member list and then its
  ancestors', with an exact comparison, so a file member can land on a base-class member.
- **Member types.** `w1` selects a type-table entry or a class record, and the entry's matched type
  becomes the member's file type.

### Reporting differences

`0059BA40` compares each matched class with its file record and logs, through `005CDAA0`:

- a parent that was added, removed or changed;
- a member in the file but not in the executable, or the reverse;
- a member whose type changed;
- a member whose attribute word differs (run-time word without bit `0x1` against `w4` without bit
  31);
- a fixed-size array whose element count differs from `w5`.

None of these stops the load.

### Choosing a copy routine

`0059D2D0` gives every file member a routine, walking the parent records first:

- no matching run-time member: the empty `0016D6A0`, so the bytes are skipped;
- same type, and the run-time width (the type's size, or 8 for a pointer) equals `w3`: `00599390`,
  or `00595E70` for a one-byte member that is not an array;
- same type with a different width, or a fixed-size array whose count differs while offset and
  attribute word match: skipped;
- different type: the conversion `0059A030` returns, or skipped when there is none.

### Dynamic classes

For a class record with `w7` bit `0x1` and no registered match, `0059AC00` takes the parent from
`w0`, refuses an abstract parent or one without a default constructor, and builds a
`PClassDescriptorDynamic` (`00632E80`). Its file members become `PClassDataMemberDynamic` records
through `006393A0` and `00632B30`. A flagged class still without a descriptor returns `0x13`. No
shipped file sets the flag.

## Modding notes

- A file's class and member names must match registered names exactly. A renamed member is skipped
  and only logged, and the log is never shown in the shipped game.
- File offsets need not match run-time offsets; the loader copies member by member. Keep each
  member's type and width (`w3`) equal to the registered ones, or its data is dropped.
- Setting `w7` bit `0x1` on a class the executable does not have makes the loader build it from the
  file's members, under a parent that is concrete and has a default constructor.
- The attribute word in a file must equal the registered one apart from bit 31; a different word
  only logs a message.

## Related

- [Bigfile archive](../Game-Files-And-Data-Tables/bigfile-archive.md): where the 35,984 `.phyre` files are stored.
- [Debug logging](../Engine-Core/debug-logging.md): the log call that carries the loader's messages.
- [Class hierarchy](../Engine-Core/class-hierarchy.md): the RTTI names of the descriptor templates.
- [Bullet physics](../Third-Party-Libraries/bullet-physics.md): the physics classes, which no shipped file declares.
