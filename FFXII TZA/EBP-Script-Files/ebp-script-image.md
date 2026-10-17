---
title: "EBP script image: the section-0 header, actor directory, function and jump tables and actor lists a zone or event script runs from"
kind: "format"
category: "EBP script files"
addresses: "0032F850, 0026C8C0, 0026CE60, 00266530, 00266C50, 00358A00, 003589E0, 002652D0, 002674B0, 00267930, 00267BB0, 00267C20, 002641B0, 002642C0, 00264390, 00264AE0, 00264B90, 00264870, 002658B0, 003B7210, 0035A270, 00265770, 022C6C28, 022C6D18"
---

## What the player sees

The script image is the code of a zone or a cutscene: who stands where, what each person says when
spoken to, which door opens, how a cutscene's characters move on cue. Each actor in a scene has its
own entry in the image with a set of named functions (`init`, `main`, `talk` and so on), and the
[script interpreter](../Scripts-And-Script-Commands/script-interpreter.md) runs those functions a
few instructions at a time each frame.

## Where it comes from

Section 0 of each `.ebp` container, at file offset `0x80` in every shipped file
([script container](ebp-script-container.md)). The container walk passes it to `0032F850`, which
binds it to the script manager the file was loaded for. All offsets below are relative to the
image's first byte.

## Layouts

### Header

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | version | 11 in every shipped image; readers below compare it |
| `+0x02` | `u16` | marker | `0x8000` |
| `+0x04` | `u32` | length | bytes of image; the section's slot may be padded beyond it |
| `+0x08` | `u32` | authorOff | -> NUL-terminated author name |
| `+0x0C` | `u32` | sourceOff | -> NUL-terminated source file name, "&lt;script&gt;.src" |
| `+0x10` | `u32` | stampOff | -> NUL-terminated build stamp "MM/DD HH:MM", at +`0x90` |
| `+0x14` | `i32` | typeCounts | -> u16 8, then u16 count[8]: directory entries per actor type |
| `+0x18` | `i32` | directory | -> u32 count, then `0x30`-byte actor entries sorted by type |
| `+0x1C` | `u32` | zero | 0 |
| `+0x20` | `i32` | intPool | -> u32 count, s32 values (PUSHI) |
| `+0x24` | `i32` | floatPool | -> u32 count, f32 values (PUSHF) |
| `+0x28` | `i32` | variables | -> u32 count, 8-byte descriptors (PUSHV, POPV) |
| `+0x2C` | `i32` | tagTables | -> the actor tag tables (PUSHACT, PUSHTAG) |
| `+0x30` | `u32` | listTable | -> u32 count, u32 listOff[count]: the actor lists |
| `+0x34` | `u32` | word34 | non-zero in all but 9 of 10,036 images |
| `+0x38` | `u32` | fileArea | the file-class variable area; `0xC0` in every image |
| `+0x3C` | `u32` | mspSize | size of the msp area |
| `+0x40` | `u32` | mspOff | the msp area (class 3, packed references with tag 3) |
| `+0x44` | `u32` | localSize | size of the local variable storage, 0 in the file |
| `+0x48` | `u32` | localOff | the local variable storage |
| `+0x4C` | `u32` | namePool | NUL-terminated names: +`0x48` + +`0x44` rounded up to 16 |
| `+0x50` | `i16` | startActor | actor ordinal `00266C50` starts, -1 for none |
| `+0x52` | `i16` | entryDefault | entry-point index used for -1 or any negative request |
| `+0x54` | `u32` | entryPointsA | -> u32 count, 32-byte records (`00264B90` kind 0) |
| `+0x58` | `u32` | startList | -> u16 count, s16 function[count] for startActor |
| `+0x5C` | `u32` | table5C | -> u32 count, `0x1C`-byte records (`00264390` mode 0) |
| `+0x60` | `u32` | table60 | -> u32 count, 16-byte records (`002642C0`) |
| `+0x64` | `u32` | weather | -> u8 3, u8 chance[3] (`002658B0`) |
| `+0x68` | `u32` | table68 | -> u32 count, u32 listOff: u16 count, s16 ordinal[] (`003B7210`) |
| `+0x6C` | `u32` | trapRefs | -> u32 count, u32 packedRef[count] (`002641B0`) |
| `+0x70` | `u32` | table70 | -> u32 5, s32 tableOff[5] (`00264AE0`) |
| `+0x74` | `u32` | table74 | -> u32 count, `0x1C`-byte records (`00264390` mode 1) |
| `+0x78` | `i16` | entryMinus2 | entry-point index used for -2 |
| `+0x7A` | `i16` | entryMinus3 | entry-point index used for -3 |
| `+0x7C` | `u32` | word7C | 0 in 1,014 of the 1,114 us images |
| `+0x80` | `u32` | table80 | -> u32 count, {u32 id, u32 mask} (`0035A270`) |
| `+0x84` | `u32` | entryPointsB | -> u32 count, 32-byte records (`00264B90` kind 1) |
| `+0x88` | `u32` | word88 | 0 in 364 of the 1,114 us images |
| `+0x8C` | `u32` | table8C | -> u32 count, 16-byte records (`00264870`) |

### Actor directory entry

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | nameOff | into the name pool: the actor's name |
| `+0x04` | `u16` | type | actor type 0..7 |
| `+0x06` | `u16` | partySlot | `0xFF`, or `0x80`..0x83 for a party member's script |
| `+0x08` | `u32` | codeStart | bytecode base -> actor record +`0x58` |
| `+0x0C` | `u32` | word0C | never more than the bytes to the next entry's code |
| `+0x10` | `u32` | functions | -> u32 count, {u32 nameOff, u32 codeOff}[count] -> record +`0x48` |
| `+0x14` | `u32` | jumps | -> u32 count, u32 codeOff[count] -> record +`0x50` |
| `+0x18` | `u32` | slotFooter | -> s16 18, s16 function[18], one per entry slot |
| `+0x1C` | `u32` | localOff | this actor's slice of the local storage |
| `+0x20` | `u8[16]` | rest of the entry |  |

Function and jump offsets are relative to `codeStart`. The function table's `listOff` follows it
directly: `jumps = functions + 4 + 8 × count` in every entry.

### Actor lists

```python
list table   +0x30 -> u32 count, u32 listOff[count]
list         listOff -> u32 count, {u16 actorOrdinal, u16 functionId}[count]
```

## Shipped data

Measured over the section 0 of all 10,036 containers; `us` figures in brackets.

| Fact | Value |
|---|---|
| version and marker | 11 and `0x8000` in all |
| header | `0x90` bytes: the smallest offset any header field holds is `0x90` in all |
| length | inside the section in all; equal to it in 2,741 (304) |
| source name | `<file>.src` in all but the `kr` and `cn` `ttl_a01_e3`, which name `ttl_a01.src` |
| build stamp | `00/00 00:00` in 10,019 (1,113); `11/22 12:00` in 9 (1); `12/09 15:11` in 2; three other stamps, each in 2 |
| authors | 30 distinct (29); 17 `us` author fields are empty or not printable |
| type counts | 8 entries in all; each equals the directory's count of that type, entries sorted by type |
| directory entries | 237,662 (26,390): type 0 79,325, 6 71,712, 7 36,603, 5 35,865, 1 13,995, 3 162 |
| party-member entries | 26,532 (2,948) |
| functions | 1,412,541 (156,895); at most 140 per actor; function 0 is `init` at code offset 0 in every entry |
| jump targets | 16,515,827 (1,834,423); at most 6,519 per actor |
| slot footer | 18 functions in every entry |
| actor lists | 6,077 (675) images, 44,894 (4,988) lists, 298,410 (33,156) pairs, 3,276 (364) empty, longest 41 |
| list contents | actor ordinals up to 116, function ids up to 63 |
| local storage | empty in 1,449 (161); name pool directly after it in all |
| msp area | size 0 in 3,174 (352) |
| `startActor` | -1 in 4,445 (493), 0 in 4,835 (537), positive in 756 (84) |
| fixed counts | `+0x64` target 3, `+0x6C` target 1, `+0x70` target 5, in all |
| `+0x68` | present with count 2 in 7,101 (789), absent otherwise |
| weather triples | 17 distinct |

## Loader behaviour

### Slot-0 handler

`0032F850(packed)` stores the image at `022C6C28[manager]` and tests only its first byte
(`0032F87E cmp byte ptr [rdi], 0`). A zero byte sets `022C6D18[manager]` to 0 and returns with
nothing bound; otherwise `022C6D18` becomes 1. It then picks the allocator the manager's actor
record pool will come from (`002679F0` calls it through record `+0x88`):

| Manager | Arena | Callback |
|---|---|---|
| 0 and 4 | 5 | `00267930` |
| 1, 2 | `0xD` when enabled, else 5 | `00267BB0` |
| 3 | `0xE` when enabled, else 5 | `00267C20` |

Each callback pushes its arena (`0036C1D0`), allocates with `0036A100`, labels the block
`ateldecode.c` with a per-site tag (`0x1676`, `0x16C1`, `0x16E6`) and pops the arena. The handler
binds the image with `0026C8C0(manager, image, callback)`, stores `00330050` at record `+0x108`
(`00268630`) and clears pending bit 1 ([script container](ebp-script-container.md)).

### The bind

`0026C8C0` fills the manager record ([actor managers](../Characters-And-Objects/actor-managers.md)). From
the header it takes:

| Header | Becomes | How |
|---|---|---|
| image | record `+0x00` | the pointer |
| `+0x14` | record `+0x20` | the sum of the eight type counts: the actor count |
| `+0x20`, `+0x24`, `+0x28`, `+0x2C` | record `+0x68`, `+0x70`, `+0x78`, `+0x80` | image + signed offset |
| `+0x48` | record `+0x50` | image + unsigned offset |
| `+0x50` | record `+0x12` | 1 when not negative (`0026CD1A cmp word ptr [r15 + 0x50], bx`) |

The callback goes to `+0x88`. No offset is checked against `+0x04` or the section's extent.

### Building the actors

When the manager's loads finish, `0026CE60` builds the actor record pool with `002679F0`, which
sizes it from the type counts and initialises one record per directory entry through `00266530`;
it then runs `00266C50` and sets record `+0x40` to image + `[+0x38]` (`0026D2ED`–`0026D2F6`) when
that is still 0. `00266530`:

1. forms the directory as image + `[+0x18]` and the actor's entry at `+4 + index × 0x30`, or
   `× 0x20` when the version word is below 8 (`00266710`–`00266731`), and stores it at record `+0x40`;
2. sets record `+2` to 1 for an index below the type-0 count, else 2 (`002666FC`–`0026670D`);
3. for a `partySlot` of `0x80` to `0x83`, files the record in the party table `0209A1F0` at
   `partySlot & 0x7F` (`00266738`–`00266792`);
4. sets record `+0x48` to the function table, `+0x50` to the jump table and `+0x58` to the code
   base (`00266795`–`002667CA`).

`00266C50` reads `startActor`: when it is not negative it files every non-negative function of
`startList` on that actor, on its top channel in mode 2
([script requests](../Scripts-And-Script-Commands/script-requests.md)).

### Functions, jumps and entry slots

- `00358A00(record, id)` returns the second dword of function `id`'s pair, or 0 when `id` is at or
  above the count; a request starts at the code base plus that offset.
- `003589E0(record, index)` returns jump target `index`, or 0 out of range; the jump opcodes add it
  to the code base, so a jump operand is a table index, not a byte offset.
- `002652D0(slot, record, entrySlot)` gives the function for one of the 18 entry slots: the
  record's override word, or else the footer's entry; with a version word below 6, entry slot 14
  reads slot 7.

### Actor lists

The group request opcodes take a list index as their operand. They resolve the list table and
bound the index by its count; an index at or past it gives a null list (`00261B27`–`00261B57`).
The wait on a list, `002674B0`, steps a cursor over its `{actor, function}` pairs and stays while
any pair's function is still filed on that actor. Filing and waiting are on
[script requests](../Scripts-And-Script-Commands/script-requests.md).

### Header tables read later

Each reader below resolves the offset through `0020E600`, returns null (or a default) for a zero
offset, and bounds the index by the table's count. `002658B0`, `00264AE0` and `00264870` read
manager 0's image only; all but `00264B90`, `003B7210` and `0035A270` also require the manager
record's `+0x10` bit 0.

| Field offset | Reader | Returns |
|---|---|---|
| `+0x54`, `+0x84` | `00264B90`, version above 2 | the first four dwords of 32-byte record `index`; `00377AB0` and `00377900` take three as a position and convert the fourth with `003A1C50` |
| `+0x5C`, `+0x74` | `00264390`, modes 0 and 1 | a pointer to `0x1C`-byte record `index` |
| `+0x60` | `002642C0`, version 9 or above | a pointer to 16-byte record `index`; older versions use `00264260` |
| `+0x64` | `002658B0`, version 7 or above | weather slot's chance byte ([weather](../World-Areas-And-Travel/weather.md)) |
| `+0x68` | `003B7210` | first runs `002E6420` (`003B7231`), which calls `00428FE0(record, 0)` on the character render record of every actor of managers 0 to 2 that has one, then binds the first list's actors through `00262F50` (`003B72C1`): entry 0 to `[02EBCC68]`, entry i to `[02EBCAC0 + 8 × (i − 1)]` while `i − 1 < [02EBCBC0]` |
| `+0x6C` | `002641B0` | base of the reference's class (`00265770`) plus its low 24 bits; class 2 refused ([traps](../World-Areas-And-Travel/traps.md)) |
| `+0x70` | `00264AE0` | image + entry `index` of the five offsets |
| `+0x80` | `0035A270` | for each `{id, mask}` whose id resolves, `002ECAB0(id, bit, 1)` for each set bit 1 to 31 |
| `+0x8C` | `00264870` | a pointer to 16-byte record `index` |

`00264B90` maps the index -1 to `+0x52`, -2 to `+0x78` and -3 to `+0x7A`, and any other negative
index to `+0x52`.

## Modding notes

- Only the first byte of the image is checked; keep the version word at 11, since several readers
  change layout below 9, 8, 7 and 6.
- Keep the directory sorted by type and the type counts equal to it: the director test compares an
  actor's index with the type-0 count.
- Out-of-range function ids and jump indices give offset 0, so the actor runs from its code base
  instead of failing.
- Header offsets are not bounded; a bad offset produces a pointer outside the image.
- Variables, opcodes and requests are on the [script variables](../Scripts-And-Script-Commands/script-variables.md),
  [script interpreter](../Scripts-And-Script-Commands/script-interpreter.md) and
  [script requests](../Scripts-And-Script-Commands/script-requests.md) pages.

## Related

- [Script container](ebp-script-container.md): the file around this section and its loader.
- [Actor managers](../Characters-And-Objects/actor-managers.md): the manager record the bind fills.
- [Actor record](../Characters-And-Objects/actor-record.md): the per-actor record built from each entry.
- [Script interpreter](../Scripts-And-Script-Commands/script-interpreter.md): the opcodes and how the tables are used.
- [Script variables](../Scripts-And-Script-Commands/script-variables.md): descriptors, the file, local and msp areas.
- [Script requests](../Scripts-And-Script-Commands/script-requests.md): entry slots, list requests and waits.
- [Weather](../World-Areas-And-Travel/weather.md): the `+0x64` chances.
- [Resource arenas](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md): the arenas the callbacks allocate from.
