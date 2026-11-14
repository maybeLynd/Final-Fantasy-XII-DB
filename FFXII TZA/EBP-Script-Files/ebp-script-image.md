---
title: "EBP script image: the section-0 header, actor directory, function and jump tables and actor lists a zone or event script runs from"
kind: "format"
category: "EBP script files"
addresses: "0x0032F850, 0x0026C8C0, 0x0026CE60, 0x00266530, 0x00266C50, 0x00358A00, 0x003589E0, 0x002652D0, 0x002674B0, 0x00267930, 0x00267BB0, 0x00267C20, 0x002641B0, 0x002642C0, 0x00264390, 0x00264AE0, 0x00264B90, 0x00264870, 0x002658B0, 0x003B7210, 0x0035A270, 0x00265770, 0x022C6C28, 0x022C6D18"
---

## What the player sees

The script image is the code of a zone or a cutscene: who stands where, what each person says when
spoken to, which door opens, how a cutscene's characters move on cue. Each actor in a scene has its
own entry in the image with a set of named functions (`init`, `main`, `talk` and so on), and the
[script interpreter](../Scripts-And-Script-Commands/script-interpreter.md) runs those functions a
few instructions at a time each frame.

Besides the code, the image header holds values other systems read: three weather chances for the zone, the zone's
exploration field number, which the game uses to look up the save's map-exploration marks, and the chest model that
`setuptreasure` places.

## Where it comes from

Section 0 of each `.ebp` container, at file offset `0x80` in every shipped file
([script container](ebp-script-container.md)). The container walk passes it to `0x0032F850`, which
binds it to the script manager the file was loaded for. All offsets below are relative to the
image's first byte.

## Layouts

All multi-byte fields are little-endian.

### Header

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | version | 11 in every shipped image; readers below compare it |
| `+0x02` | `u16` | marker | `0x8000` |
| `+0x04` | `u32` | length | bytes of image; the section's slot may be padded beyond it |
| `+0x08` | `u32` | authorOff | -> NUL-terminated author name |
| `+0x0C` | `u32` | sourceOff | -> NUL-terminated source file name, "&lt;script&gt;.src" |
| `+0x10` | `u32` | stampOff | -> NUL-terminated build stamp "MM/DD HH:MM", at `+0x90` |
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
| `+0x4C` | `u32` | namePool | NUL-terminated names: `+0x48` + `+0x44` rounded up to 16 |
| `+0x50` | `i16` | startActor | actor ordinal `0x00266C50` starts, -1 for no actor |
| `+0x52` | `i16` | entryDefault | entry-point index used for -1 or any negative request |
| `+0x54` | `u32` | entryPointsA | -> u32 count, 32-byte records (`0x00264B90` kind 0) |
| `+0x58` | `u32` | startList | -> u16 count, s16 function[count] for startActor |
| `+0x5C` | `u32` | table5C | -> u32 count, `0x1C`-byte records (`0x00264390` mode 0) |
| `+0x60` | `u32` | table60 | -> u32 count, 16-byte records (`0x002642C0`) |
| `+0x64` | `u32` | weather | -> u8 3, u8 chance[3] (`0x002658B0`) |
| `+0x68` | `u32` | table68 | -> u32 count, u32 listOff: u16 count, s16 ordinal[] (`0x003B7210`, `0x003B72F0`) |
| `+0x6C` | `u32` | trapRefs | -> u32 count, u32 packedRef[count] (`0x002641B0`) |
| `+0x70` | `u32` | table70 | -> u32 5, s32 tableOff[5] (`0x00264AE0`) |
| `+0x74` | `u32` | table74 | -> u32 count, `0x1C`-byte records (`0x00264390` mode 1) |
| `+0x78` | `i16` | entryMinus2 | entry-point index used for -2 |
| `+0x7A` | `i16` | entryMinus3 | entry-point index used for -3 |
| `+0x7C` | `i16` | explorationField | exploration field id (`0x00264790`, `0x002551B0`); 0, or 289 to 1,143 |
| `+0x7E` | `i16` | word7E | returned by `0x00264770`; 0, or 1 to 31 when `+0x7C` is set |
| `+0x80` | `u32` | table80 | -> u32 count, {u32 id, u32 mask} (`0x0035A270`) |
| `+0x84` | `u32` | entryPointsB | -> u32 count, 32-byte records (`0x00264B90` kind 1) |
| `+0x88` | `i16` | treasureModel | setuptreasure's chest model (`0x0026E060`, version 11 or above); -1, 0, 4 or 5 |
| `+0x8A` | `u16` | pad8A | 0 in every image |
| `+0x8C` | `u32` | table8C | -> u32 count, 16-byte records (`0x00264870`) |

### Actor directory entry

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | nameOff | into the name pool: the actor's name |
| `+0x04` | `u16` | type | actor type 0..7 |
| `+0x06` | `u16` | partySlot | `0xFF`, or `0x80`..0x83 for a party member's script |
| `+0x08` | `u32` | codeStart | bytecode base -> actor record `+0x58` |
| `+0x0C` | `u32` | word0C | never more than the bytes to the next entry's code |
| `+0x10` | `u32` | functions | -> u32 count, {u32 nameOff, u32 codeOff}[count] -> record `+0x48` |
| `+0x14` | `u32` | jumps | -> u32 count, u32 codeOff[count] -> record `+0x50` |
| `+0x18` | `u32` | slotFooter | -> s16 18, s16 function[18], one per entry slot |
| `+0x1C` | `u32` | localOff | this actor's slice of the local storage |
| `+0x20` | `u16` | copy | the actor's copy number: `0x00263880` returns it (`0x002638AA`) for an image of version 8 or more |
| `+0x22` | `u8[14]` |  | rest of the entry |

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
| name pool | `+0x4C` = `+0x48` + `+0x44` rounded up to 16, in all |
| `+0x7C`, `+0x7E` | both non-zero in 900 (100), both 0 in 9,136 (1,014); `+0x7C` 289 to 1,143, `+0x7E` 1 to 31 |
| `+0x88` | -1 in 6,571 (729), 0 in 3,276 (364), 4 in 171 (19), 5 in 18 (2); `+0x8A` 0 in all |
| weather triples | 17 distinct |

## Loader behaviour

### Slot-0 handler

`0x0032F850(packed)` stores the image at `0x022C6C28[manager]` and tests only its first byte
(`0x0032F87E cmp byte ptr [rdi], 0`). A zero byte sets `0x022C6D18[manager]` to 0 and returns with
nothing bound (`0x0032F88D`-`0x0032F8A6`); that path does not touch the pending word, so pending bit `0x2` stays set
and it does not run `0x0032F1B0`, and on it a manager of 5 or more goes to `__report_rangecheckfailure`
(`0x0032F883`-`0x0032F887`, `0x0032FA04`).

Otherwise `0x022C6D18` becomes 1 (`0x0032F8B6`). It then picks the allocator the manager's actor record pool will
come from (`0x002679F0` calls it through record `+0x88`):

| Manager | Arena | Callback |
|---|---|---|
| 0 and 4, and 1 to 3 when their arena is not enabled | 5 | `0x00267930` (`0x0032F8FE`, `0x0032F94E`-`0x0032F95A`) |
| 1, 2 with `0xD` enabled | `0xD` | `0x00267BB0` (`0x0032F945`) |
| 3 with `0xE` enabled | `0xE` | `0x00267C20` (`0x0032F923`) |

Each callback pushes its arena (`0x0036C1D0`), allocates with `0x0036A100`, labels the block
`ateldecode.c` with a per-site tag (`0x1676`, `0x16C1`, `0x16E6`) and pops the arena. The handler
pushes the chosen arena itself with `0x0036C1D0(arena, 5)` (`0x0032F91E`, `0x0032F940`, `0x0032F955`),
binds the image with `0x0026C8C0(manager, image, callback)` (`0x0032F966`), stores `0x00330050` at record `+0x108`
(`0x00268630`, `0x0032F974`), pops the arena (`0x0036C140`, `0x0032F979`) and clears pending bit `0x2` (`0x0032F98E`)
([script container](ebp-script-container.md)).

With the bit cleared it applies the container's clearer rule (`0x0032F99A`-`0x0032F9BF`): when the word without
bit `0x1` is zero it clears bit `0x8` of the record's `+0x11`, and when the word went from non-zero to zero it
runs `0x0032F1B0(manager)`. For manager 0, once bits `0x2` and `0x200` are both clear (`0x0032F9D0`), it then runs
`0x0025AFC0(0)` and `0x002EACC0(0x00331990, [0x022C6D28])` (`0x0032F9DA`-`0x0032F9EE`).

`0x00330050(record)` is a jump to the teardown `0x0032ED80` with the record's dword `+0x28`
as the manager (`0x00330050`-`0x00330053`).

### The bind

`0x0026C8C0` fills the manager record ([actor managers](../Characters-And-Objects/actor-managers.md)). From
the header it takes:

| Header | Becomes | How |
|---|---|---|
| image | record `+0x00` | the pointer |
| `+0x14` | record `+0x20` | the sum of the eight type counts: the actor count |
| `+0x20`, `+0x24`, `+0x28`, `+0x2C` | record `+0x68`, `+0x70`, `+0x78`, `+0x80` | image + signed offset |
| `+0x48` | record `+0x50` | image + unsigned offset |
| `+0x50` | record `+0x12` | 1 when not negative (`0x0026CD1A cmp word ptr [r15 + 0x50], bx`) |

The callback goes to `+0x88`. No offset is checked against `+0x04` or the section's extent.

### Building the actors

When the manager's loads finish, `0x0026CE60` builds the actor record pool with `0x002679F0`, which
sizes it from the type counts and initialises one record per directory entry through `0x00266530`;
it then runs `0x00266C50` and sets the manager slot's `+0x40` to image + `[+0x38]` (`0x0026D2ED`–`0x0026D2F6`) when
that is still 0. `0x00266530`:

1. forms the directory as image + `[+0x18]` and the actor's entry at `+4 + index × 0x30`, or
   `× 0x20` when the version word is below 8 (`0x00266710`–`0x00266731`), and stores it at record `+0x40`;
2. sets record `+2` to 2 for an index below the type-0 count, a signed 32-bit compare, else 1
   (`0x002666FC`–`0x0026670D`);
3. for a `partySlot` of `0x80` to `0x83`, files the record in the party table `0x0209A1F0` at
   `partySlot & 0x7F` (`0x00266738`–`0x00266792`);
4. sets record `+0x48` to the function table, `+0x50` to the jump table and `+0x58` to the code
   base (`0x00266795`–`0x002667CA`).

`0x00266C50` reads `startActor`: when it is not negative it files every non-negative function of
`startList` on that actor, on its top channel in mode 2
([script requests](../Scripts-And-Script-Commands/script-requests.md)), through
`0x003DBB60(actor, channels - 1, function, 2, 0)` (`0x00266CD2`). A `startList` offset of 0 files nothing
(`0x00266C92`), and when `startActor` names no record (`0x00358940` gives null) the first function that is not
negative makes it read the channel count at address `0x88` (`0x00266CBB`), which faults.

### Functions, jumps and entry slots

- `0x00358A00(record, id)` returns the second dword of function `id`'s pair, or 0 when `id` is at or
  above the count; a request starts at the code base plus that offset.
- `0x003589E0(record, index)` returns jump target `index`, or 0 out of range; the jump opcodes add it
  to the code base, so a jump operand is a table index, not a byte offset.
- `0x002652D0(slot, record, entrySlot)` gives the function for one of the 18 entry slots: the
  record's override word, or else the footer's entry; with a version word below 6, entry slot 14
  reads slot 7. The footer is the image plus the dword at `+0x18` of the record's entry `+0x40`
  (`0x00265319`-`0x0026532F`); an entry slot above 17 (`0x002652DD`) or at or above the footer's signed count word
  (`0x0026533A`) gives -1.

### Actor lists

The group request opcodes take a list index as their operand. They resolve the list table and
bound the index by its count; an index at or past it gives a null list (`0x00261B27`–`0x00261B57`).
The wait on a list, `0x002674B0`, steps a cursor over its `{actor, function}` pairs and stays while
a pair from the cursor on still has its function filed on that actor: the cursor stops on that pair and
moves past each pair that is no longer filed (`0x0026751C`), and the pairs behind it are not tested again.
Filing and waiting are on
[script requests](../Scripts-And-Script-Commands/script-requests.md).

### Header tables read later

Each reader below resolves the offset through `0x0020E600`, returns null (or a default) for a zero
offset, and bounds the index by the table's count, except `0x002658B0`: it answers 33 for a zero offset
(`0x002658F6`, `0x00265910`), clamps the slot to 0 to 2, `i = n - 1 < 0 ? 0 : n - 1 > 2 ? 2 : n - 1` for its
argument `n` (`0x002658B8`-`0x002658C8`), and reads the byte `[section + 1 + i]`, never the section's count byte
(`0x00265900`). `0x002658B0`, `0x00264AE0` and `0x00264870` read
manager 0's image only; all but `0x00264B90`, `0x003B7210` and `0x0035A270` also require the manager
record's `+0x10` bit `0x1`.

| Field offset | Reader | Returns |
|---|---|---|
| `+0x54`, `+0x84` | `0x00264B90`, version above 2 | the first four dwords of 32-byte record `index`; `0x00377AB0` and `0x00377900` take three as a position and convert the fourth with `0x003A1C50` |
| `+0x5C`, `+0x74` | `0x00264390`, modes 0 and 1 | a pointer to `0x1C`-byte record `index`: image + offset + 4 + `index * 0x1C` (`0x002643F5`-`0x002643FD`), with the index compared unsigned against the count (`0x002643F3`); any mode other than 0 and 1 returns null (`0x0026439D`-`0x002643A6`) |
| `+0x60` | `0x002642C0`, version 9 or above | a pointer to 16-byte record `index`; older versions use `0x00264260`; for an older version `0x002642C0` widens 8-byte record `index` from `0x00264260` into one static copy and returns its address (`0x0026436F`): `0x0209A290` and `0x0209A292` take the record's words `+0` and `+2` (`0x00264334`, `0x0026433F`), `0x0209A294` is `0xFFFF` (`0x0026435F`), `0x0209A296` is 0 (`0x00264368`), and `0x0209A298` and `0x0209A29A` take its words `+4` and `+6` (`0x0026434A`, `0x00264355`); every such call rewrites the copy |
| `+0x64` | `0x002658B0`, version 7 or above | weather slot's chance byte ([weather](../World-Areas-And-Travel/weather.md)) |
| `+0x68` | `0x003B7210` | first runs `0x002E6420` (`0x003B7231`), which calls `0x00428FE0(record, 0)` on the character render record of every actor of managers 0 to 2 that has one, then binds the first list's actors through `0x00262F50` (`0x003B72C1`): entry 0 to `[0x02EBCC68]`, entry i to `[0x02EBCAC0 + 8 × (i − 1)]` while `i − 1 < [0x02EBCBC0]`; each actor is the record `0x00358940` gives for the entry's ordinal (`0x003B7295`, `0x003B72B2`), a negative ordinal is skipped (`0x003B727D`), entry 0 is bound only while `[0x02EBCC68]` is non-null (`0x003B72A1`-`0x003B72A9`), and a zero `+0x68` offset or a list-table count of 0 or less binds nothing, after `0x002E6420` has run (`0x003B7239`, `0x003B7246`); `0x003B72F0` (`capturepartyforsummon`), when the count is above 1 (`0x003B731D`), reads the second list (`0x003B7323`) and has the actor at each non-negative ordinal i (`0x003B7356`) capture `[0x02EBCA80 + 8 × i]` while i is below `[0x02EBCAA0]` (`0x003B7358`-`0x003B7375`) |
| `+0x6C` | `0x002641B0` | base of the reference's class (`0x00265770`) plus its low 24 bits; class 2 refused ([traps](../World-Areas-And-Travel/traps.md)) |
| `+0x70` | `0x00264AE0` | image + entry `index` of the five offsets |
| `+0x80` | `0x0035A270` | for each `{id, mask}` whose id resolves, `0x002ECAB0(id, i, 1)` for each bit `1 << i` set in `mask & 0xFFFFFFFE`: it makes the given manager's record current (`0x0026A480`, `0x0035A28F`) and restores the previous one at the end (`0x0035A392`); the table id is turned into a bound id by `0x002E9A60` (`0x0035A2E7`), and only a non-zero bound id whose entry `0x002E99C0(0x002EB7A0(bound id))` exists and is ready (`0x002E4C20`) goes on (`0x0035A2F2`-`0x0035A316`); that entry gets bit `0x1` of `+0x19` (`0x0035A318`), and for each `i` from 1 to 31 with `mask & (1 << i)` set and a positive bound id it calls `0x002ECAB0(bound id, i, 1)` and then `0x002ECAB0(bound id, 0, 1)` (`0x0035A330`-`0x0035A35F`) |
| `+0x8C` | `0x00264870` | a pointer to 16-byte record `index`: image + offset + 4 + `index * 16` (`0x002648BD`-`0x002648C8`); the bound is a signed compare (`0x002648B4`), so a negative index passes it and gives a pointer before the table |

`0x002E6420` walks a manager only while bit `0x1` of its byte `+0x10` is set, over the
ordinals from its word `+0x1DE` for its word `+0x1D6`. For each, `0x00358940(manager,
ordinal)` gives an object; when that, its pointer `+0xC0`, a dword there other than -1
and a word there other than `0xFFFF` are all present, the record is
`[0x022C6F28] + 0x740 × word`, and `0x00428FE0(record, 0)` is called only for a record
address other than 0 whose dword `+0x284` is not 0 (`0x002E6440`-`0x002E64A8`).

`0x00264B90` maps the index -1 to `+0x52`, -2 to `+0x78` and -3 to `+0x7A`, and any other negative
index to `+0x52`. The tests run in that order on the replaced value, so a `+0x52` of -2 goes on to `+0x78`, and
an index still negative after the last `+0x52` read becomes 0 (`0x00264BEE`-`0x00264C1F`).

`0x00264B90(list, manager, index, x, y, z, angle)` zeroes its four outputs first (`0x00264BBE`-`0x00264BD8`) and
answers 0 for a null image (`0x00264BE3`), a version of 2 or less (`0x00264C23`), a list offset that decodes to 0 or
an index not below the count (`0x00264C3D`-`0x00264C49`). Any non-zero `list` takes `+0x84`, and the list is the
image plus the low 32 bits of the decoded offset (`0x00264C42`-`0x00264C44`); a found record answers 1.

Four more header fields are read as values, not as table offsets:

- `+0x4C`: `0x00263A30(manager, ordinal)` returns the image plus `+0x4C` plus the first int of the entry's
  `+0x40` record (`0x00263A83`-`0x00263A8C`), the issuer name `captureactor` (`0x00354E10`) searches by, and
  `0x00263E40(image, offset)` returns the image plus `+0x4C` plus `offset` (`0x00263E40`-`0x00263E4A`);
- `+0x7C`: `0x00264790` returns this signed word of manager 0's image (`0x002647A5`), or -1 while manager
  0's record `+0x10` lacks bit `0x1`. `0x003C4AE0` passes a positive value to `0x002551B0(0, field)`, which
  indexes the save's exploration bitmaps through `0x003779F0` ([menu map
  files](../Game-Files-And-Data-Tables/menu-map-files.md));
- `+0x7E`: `0x00264770` returns it the same way (`0x00264785`). The map screen's point-list pane `0x002BA310`
  compares it with its list's words at `+0xCC` (`0x002BA4A0`-`0x002BA4AA`), and `0x002B7B80` (`0x002B8621`) and
  `0x004048E0` (`0x00404A6A`) read it;
- `+0x88`: `0x0026E060`, for `setuptreasure` (`0x00354435`, `0x003552DE`), reads this word of manager 0's
  image when the record's `+0x10` has bit `0x1` and the version is 11 or above (`0x0026E093`-`0x0026E09B`).
  A non-negative value ORed with `0x3000000` is the chest model's name index, resolved by `0x002E9A60`
  through the name table (`0x00263F80`); otherwise the model is -1 ([script name
  bindings](../Scripts-And-Script-Commands/script-name-bindings.md)).

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
- [`ebp-script-image-actdef-header-census.tsv`](ebp-script-image-actdef-header-census.tsv): for each of the header's
  first 76 bytes (`+0x00` to `+0x4B`) over the shipped images, whether it is constant, zero or varying, with its
  distinct values (76 rows).
- [`ebp-script-image-list-wait-census.tsv`](ebp-script-image-list-wait-census.tsv): every list request (`REQALL`,
  `REQIALL`, `REQWAITALL`) in the 6,077 images that carry actor lists: the list it names, the list's length and its
  first 12 actor:function pairs (60,362 rows).
- [`ebp-script-image-actor-lists.tsv`](ebp-script-image-actor-lists.tsv): every actor list of every shipped image in
  all nine trees, 44,894 rows: `tree`, `script`, `list` (its index in the list table), `list_offset` (from the image
  start), `list_len` (0 to 41) and `pairs`, all of the list's `{actorOrdinal, functionId}` pairs as `ordinal:funcid`,
  separated by commas (empty for the 3,276 empty lists).

### Columns of ebp-script-image-list-wait-census.tsv

One row per request opcode in each script of each shipped script image.

| Column | Holds |
|---|---|
| `pc` | the opcode's offset in the script image (the block that starts at file `+0x80`), in hexadecimal without `0x` |
| `opname` | the opcode: `REQALL` (`0x5F`, 47,812 rows), `REQWAITALL` (`0x61`, 8,851) or `REQIALL` (`0x63`, 3,699) |
| `lists_in_script` | the count word of the image's list table, the table at the offset in header `+0x30`: how many actor lists the image carries, 1 to 81 on these rows |
| `in_range` | 1 when the opcode's list index is below that count, 0 when the request names a null list; 1 on all 60,362 rows |
| `list_len` | the number of `{actor, function}` pairs in the named list, 0 to 41 |
| `pairs(ordinal:funcid, first 12)` | the list's first 12 pairs, each as the actor's ordinal and the function id, `ordinal:funcid`, separated by commas; empty when the list has no pair |

- [`ebp-script-image-req-channel-census-1.tsv`](ebp-script-image-req-channel-census-1.tsv): every `REQ`, `REQSW`,
  `REQEW`, `REQWAIT`, `REQALL`, `REQIALL`, `REQCHG` and `REQWAITALL` instruction in the shipped images, with the
  pushes before it and, for `REQ`, `REQSW` and `REQEW`, the channel its first push gives: the first part, the images
  up to `ps2data/plan_master/fr/event/vic_a/vic_a0300/vic_a0300.ebp` (265,073 rows).
- [`ebp-script-image-req-channel-census-2.tsv`](ebp-script-image-req-channel-census-2.tsv): the second part, the
  images from `ps2data/plan_master/fr/event/vic_a/vic_a0301/vic_a0301.ebp` on (264,955 rows).

In the two parts:

- `file` is the image, `script` the script's index in it, `pc` the instruction's offset in the script section
  (hex), and `opcode` and `opname` the instruction.
- `args_push_order` is the pushes that build its arguments, in order (`PUSHII:1` pushes 1). It is empty in the
  8,851 `REQWAITALL` rows: no push builds that instruction's arguments.
- `channel_class` is `const-int` where a pushed constant gives the channel of a `REQ`, `REQSW` or `REQEW`, and
  `n/a` for the other five instructions, whose pushes `args_push_order` gives whole.
- `channel_byte` is that constant's low byte, and `ge80` is 1 for a channel byte of `0x80` or more (0 in every row).

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Core runtime: `0x002B7B80` calls `0x001EDEC0`; those functions are documented on
  [global state accessors](../Engine-Core/global-state-accessors.md).
- Input: `0x002B7B80` calls `0x00250200`; `0x00358940` is called by `0x00226BE0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md).
- Platform online achievements: `0x00264790` is called by `0x003160C0`; `0x003779F0` is called by `0x003160C0`; those
  functions are documented on [handbook files](../Game-Files-And-Data-Tables/handbook-files.md).
- World area: `0x00358940` is called by `0x0025E400`, `0x002623A0`; those functions are documented on
  [actor record fields](../Characters-And-Objects/actor-record-fields.md),
  [frame update order](../Engine-Core/frame-update-order.md).
