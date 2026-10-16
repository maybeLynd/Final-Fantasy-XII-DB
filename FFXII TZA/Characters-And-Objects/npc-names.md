---
title: "NPC names: the npcdic.bin name pairs, the actor's name id, and the story flag that swaps a name"
kind: "system"
category: "Characters and objects"
summary: "How a field character's name tag is chosen: the name id every actor carries, the pair of strings that id selects in npcdic.bin, the persistent flag with the same number that switches to the second string once the player has talked to that character, the two script verbs that assign a name id, and the shipped dictionaries for the nine languages."
addresses: ["003EAC40", "003EAC70", "003EAC10", "003EABE0", "00263990", "002639E0", "0026DEA0", "00269F40", "0034B9A0", "0034C170", "002E16B0", "00379D20", "00272CB0", "00272CE0", "00268D10"]
---

# NPC names: the npcdic.bin name pairs, the actor's name id, and the story flag that swaps a name

## What the player sees

A townsperson's name tag reads "Imperial", "Rabanastran" or "Wistful Bangaa" until the player has
spoken to that person or a script reveals them, after which the same person is "Sherral" or "Arryl".
Nothing about the character changes: every field character carries a name number, the number picks
a pair of names from one file, and a story flag with the same number decides which of the two is
shown. Most pairs repeat the same name twice, so for them the flag changes nothing visible.

## How it works

### The dictionary file

`00379D20`, one of the boot loaders, calls `003EAC40`, which asks the resource loader for kind 9,
index `0x1F` with the callback `003EAC70` (`0051ED10(9, 0x1F, 003EAC70)`) and keeps the returned
block at `02B5E0D8`. Kind 9 index `0x1F` is the language's `bin/npcdic.bin` (see the
[languages page](../Saving-Loading-And-Settings/languages.md) for the language folder). The callback runs
once the block is in memory:

1. when `count` is positive, for each of the `count` entries at `+0x0C` it adds the low 32 bits of
   the block's address to the stored `i32` offset (`003EAC7E`-`003EAC8D`); the accessors sign-extend
   the entry into a pointer, so the dictionary works because the block lives in the low 2 GB;
2. it writes 1 to `+0x04` (`003EAC8F`) in either case.

Entry `2 * id` is pair `id`'s first name and entry `2 * id + 1` its second.

### The accessors

| Function | Returns | Refuses |
|---|---|---|
| `003EAC10(id, flag)` | entry `2 * id + (flag != 0)` | no block, or the entry index at or above `count` |
| `003EABE0(id)` | entry `2 * id + 1`, the second name | the same |

### Which name is shown

`00263990(actor)` resolves an actor's display name:

- when the actor's `i16` at `+0x102` is negative, the name is the literal text pointer at `+0xF8`
  (the spawn entry's own text; for such an actor `00263A10` returns the word at `+0x100`, and 0 otherwise);
- otherwise bit 14 of the id is stripped, the 2048-bit persistent flag bank is asked for flag `id`
  (`0032A930`, persistent flag banks), and
  `003EAC10(id, flagSet)` returns the first name while the flag is clear and the second once it is
  set.

`002639E0(id)` does the same from a bare id and `0026DEA0(id, flag)` from an explicit pair. The
callers that put the name on screen are `00272CB0` (the name for an actor handle resolved by
`003588B0`, or the empty string `01CEB638`), `00272CE0` (copies it into a caller's buffer and, when `00263A10` returns non-zero, appends the
32-character text `0024ABE0` builds) and the field interaction pass
`00268D10`, which passes the name to `003DF760(..., 3, ...)` for an actor whose `+0x1C` bit 13 is
set.

### Who sets the flag

The message window opener `002E16B0(actor, ...)` begins, for a non-null actor, with
`0032ABF0(actor +0x102, 1)` (`002E16DF`-`002E16EB`): opening a conversation with a character sets
that character's name flag, and the setter ignores ids at or above `0x800` as unsigned, so a
literal-named actor (negative id) sets nothing. Scripts can set or clear the same flag through the
flag-bank verbs.

### Who sets the id

`00269F40(actor, id)` stores the id at `+0x102`; a non-negative id has bit 14 cleared first, a
negative one is stored as it is. Two script verbs reach it:

| Verb | Id | Handler | What it does |
|---|---|---|---|
| `setnpcname(id)` | `0x38A` | `0034B9A0` | pops the integer (`00267E10`); a negative id is stored only when `003EABE0(id)` returns a non-null entry |
| `setshopname(shop)` | `0x4A9` | `0034C170` | pops the shop index, maps it to the shop record's first `u16` through `002FAE40` (the table at `[02EBF158]`; an index at or above the record count gives 0, pair 0), pushes it back (`00267F90`) and then stores it like `setnpcname` |

The accessors have no lower bound. For `setnpcname(-1)`, `003EABE0` computes index `2 * -1 + 1 = -1`
and reads the dword before the entry array, the dictionary's own `count` (`+0x08`), so -1 is accepted
whenever the dictionary is loaded with a non-zero count; -2 reads the magic at `+0x00` and is always
accepted; lower ids read the memory before the block. A negative id makes the actor show its literal
text at `+0xF8`.

## Layouts

```
struct NpcDictionary base=npcdic.bin size=file
+0x00  u8[4]        magic      "NPC0"
+0x04  u32          relocated  0 in the file; 003EAC70 writes 1 after relocation
+0x08  u32          count      2282 in every shipped language: 1141 pairs
+0x0C  i32[2282]    entries    file offsets of the strings; string pointers once relocated
+0x23B4 u8[]        strings    zero-terminated, in the script text encoding (0x20-0x39 = A-Z, 0x3A-0x53 = a-z, 0x04 = space)
```

The first string begins at `0x0C + 4 * count = 0x23B4` in every shipped file.

```
name(actor) = actor.i16[0x102] < 0 ? actor.ptr[0xF8]
            : entries[2 * (id & ~0x4000) + (flagBank2048[id & ~0x4000] ? 1 : 0)]
```

## Shipped data

All nine dictionaries (`ch`, `cn`, `de`, `es`, `fr`, `in`, `it`, `kr`, `us`) carry the magic `NPC0`, a
relocation flag of 0 and `count` 2282, so the id space is shared across languages; the number of
pairs whose two names differ is not:

| Language | File size | Pairs whose names differ |
|---|---|---|
| `us` | 37,545 | 247 |
| `ch` | 36,357 | 250 |
| `in` | 30,426 | 250 |
| `kr` | 38,861 | 250 |
| `cn` | 36,006 | 252 |
| `de` | 43,006 | 255 |
| `es` | 40,218 | 257 |
| `it` | 42,109 | 261 |
| `fr` | 38,860 | 275 |

Examples from the `us` file:

| Pair | First name | Second name |
|---|---|---|
| 0 | Rabanastran | Rabanastran |
| 1 | Imperial | Imperial |
| 16 | Imperial | Sherral |
| 104 | Rabanastran | Arryl |
| 105 | Rabanastran | Nathyl |
| 123 | Rabanastran | Gatsly |
| 157 | Viera | Wandering Viera |
| 159 | Viera | Ktjn |
| 220 | Cockatrice | Agytha |
| 221 | Nomad | Arjie |

## Modding notes

- To rename a character, edit its pair in `npcdic.bin`; to make a reveal happen, set persistent flag
  `id` in the 2048-bit bank. The second name needs no script change.
- Pairs whose two strings are identical are inert: setting their flag changes nothing visible, and
  the set of visible reveals differs by language (247 ids in English, 275 in French).
- Ids with bit 14 set reach the same pair as without it: `00269F40` strips the bit on store and
  `00263990` before the flag test and the lookup. The conversation setter in `002E16B0` passes the
  raw word, so an id that still carries bit 14 is at least `0x800` and sets no flag.
- A negative name id makes the actor show its own literal text, which is how `setnpcname(-1)` is
  used by the shipped scripts.

## Related

- Persistent flag banks: the 2048-bit bank the name flag lives in.
- [Languages](../Saving-Loading-And-Settings/languages.md): which language folder the dictionary is loaded from.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): where the flag bank sits in the save.
- [The spawn keep entry](../Enemy-Spawning/spawn-record-fields.md): where an actor's `+0xF8` text and `+0x102` id come from.
