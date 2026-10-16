---
title: "NPC names: the npcdic.bin name pairs, the actor's name id, and the story flag that swaps a name"
kind: "system"
category: "Characters and objects"
addresses: "003EAC40, 003EAC70, 003EAC10, 003EABE0, 00263990, 002639E0, 0026DEA0, 00269F40, 0034B9A0, 0034C170, 002E16B0, 00379D20, 00272CB0, 00272CE0, 00268D10, 00536310, 00536280, 00267410, 005369C0, 00272C80"
---

## What the player sees

A townsperson's name tag reads "Imperial", "Rabanastran" or "Wistful Bangaa" until the player has
spoken to that person or a script reveals them, after which the same person is "Sherral" or "Arryl".
Nothing about the character changes: every field character carries a name number, the number picks
a pair of names from one file, and a story flag with the same number decides which of the two is
shown. Most pairs repeat the same name twice, so for them the flag changes nothing visible.

## How it works

### The dictionary file

`00379D20`, one of the boot loaders, calls `003EAC40`, which asks the resource loader for kind 9,
index `1F`<sub>h</sub> with the callback `003EAC70` (`0051ED10(9, 1Fh, 003EAC70)`) and keeps the returned
block at `02B5E0D8`. Kind 9 index `1F`<sub>h</sub> is the language's `bin/npcdic.bin` (see the
[languages page](../Saving-Loading-And-Settings/languages.md) for the language folder). The callback runs
once the block is in memory:

1. when `count` is positive, for each of the `count` entries at `+0C`<sub>h</sub> it adds the low 32 bits of
   the block's address to the stored `i32` offset (`003EAC7E`-`003EAC8D`); the accessors sign-extend
   the entry into a pointer, so the dictionary works because the block lives in the low 2 GB;
2. it writes 1 to `+04`<sub>h</sub> (`003EAC8F`) in either case.

Entry `2 * id` is pair `id`'s first name and entry `2 * id + 1` its second.

### The accessors

| Function | Returns | Refuses |
|---|---|---|
| `003EAC10(id, flag)` | entry `2 * id + (flag != 0)` | no block, or the entry index at or above `count` |
| `003EABE0(id)` | entry `2 * id + 1`, the second name | the same |

### Which name is shown

`00263990(actor)` resolves an actor's display name:

- when the actor's `i16` at `+102`<sub>h</sub> is negative, the name is the literal text pointer at `+F8`<sub>h</sub>
  (the spawn entry's own text; for such an actor `00263A10` returns the word at `+100`<sub>h</sub>, and 0 otherwise);
- otherwise bit 14 of the id is stripped, the 2048-bit persistent flag bank is asked for flag `id`
  (`0032A930`, [persistent flag banks](../Story-Events-And-Hunts/story-flags.md)), and
  `003EAC10(id, flagSet)` returns the first name while the flag is clear and the second once it is
  set.

`002639E0(id)` does the same from a bare id and `0026DEA0(id, flag)` from an explicit pair. The
callers that put the name on screen are `00272CB0` (the name for an actor handle resolved by
`003588B0`, or the empty string `01CEB638`), `00272CE0` (copies it into a caller's buffer and, when `00263A10` returns non-zero, appends the
32-character text `0024ABE0` builds) and the field interaction pass
`00268D10`, which passes the name to `003DF760(..., 3, ...)` for an actor whose `+1C`<sub>h</sub> bit 13 is
set.

### Who sets the flag

The message window opener `002E16B0(actor, ...)` begins, for a non-null actor, with
`0032ABF0(actor +102h, 1)` (`002E16DF`-`002E16EB`): opening a conversation with a character sets
that character's name flag, and the setter ignores ids at or above `800`<sub>h</sub> as unsigned, so a
literal-named actor (negative id) sets nothing. Scripts can set or clear the same flag through the
flag-bank verbs.

### Who sets the id

`00269F40(actor, id)` stores the id at `+102`<sub>h</sub>; a non-negative id has bit 14 cleared first, a
negative one is stored as it is. Two script verbs reach it:

| Verb | Id | Handler | What it does |
|---|---|---|---|
| `setnpcname(id)` | `38A`<sub>h</sub> | `0034B9A0` | pops the integer (`00267E10`); a negative id is stored only when `003EABE0(id)` returns a non-null entry |
| `setshopname(shop)` | `4A9`<sub>h</sub> | `0034C170` | pops the shop index, maps it to the shop record's first `u16` through `002FAE40` (the table at `[02EBF158]`; an index at or above the record count gives 0, pair 0), pushes it back (`00267F90`) and then stores it like `setnpcname` |

The accessors have no lower bound. For `setnpcname(-1)`, `003EABE0` computes index `2 * -1 + 1 = -1`
and reads the dword before the entry array, the dictionary's own `count` (`+08`<sub>h</sub>), so -1 is accepted
whenever the dictionary is loaded with a non-zero count; -2 reads the magic at `+00`<sub>h</sub> and is always
accepted; lower ids read the memory before the block. A negative id makes the actor show its literal
text at `+F8`<sub>h</sub>.

### Names in battle messages

The battle message composer `005369C0` (called from `0046AB10`) names the acting and the target
unit from their stats records, in three steps:

1. `00536310(stats, &fromDictionary)` picks a name reference. A null record gives `FFFF`<sub>h</sub>, and a
   kind-0 record (byte `+05`<sub>h</sub>) gives word `+30`<sub>h</sub> of the party table row its byte `+04`<sub>h</sub> names.
2. For any other kind it finds the owning unit (`0031B860`, which scans the unit pool for the unit
   whose `+698`<sub>h</sub> is the record). When that unit's actor has a name id of 0 or more (`00267410`
   tests `+102h >= 0`), it returns the id (`00263B40`) with `fromDictionary` = 1; otherwise word
   `+08`<sub>h</sub> of the unit's definition row `+E60`<sub>h</sub>, or 0 with no unit.
3. `00536280(ref, fromDictionary)` turns the reference into text. From the dictionary it calls
   `0026DEA0(ref, 1)`, so an enemy with an NPC name id is always named by the pair's second name,
   whatever the actor's name flag holds. Otherwise `FFFF`<sub>h</sub> gives the empty string `01CEB638`, and
   any other reference is split into a bank (`ref >> 11`) and an entry (`ref & 7FFh`) of the text
   banks at `[02EBF170]` and rendered by `002B58B0`.

`00272C80(handle)` returns `00263A10` of the actor a handle resolves to (`003588B0`), and -1 when it
does not resolve.

## Layouts

Struct NpcDictionary base=npcdic.bin size=file:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0000`<sub>h</sub> | `u8[4]` | magic | "NPC0" |
| `0004`<sub>h</sub> | `u32` | relocated | 0 in the file; `003EAC70` writes 1 after relocation |
| `0008`<sub>h</sub> | `u32` | count | 2282 in every shipped language: 1141 pairs |
| `000C`<sub>h</sub> | `i32[2282]` | entries | file offsets of the strings; string pointers once relocated |
| `23B4`<sub>h</sub> | `u8[]` | strings | zero-terminated, in the script text encoding (`20`<sub>h</sub>-`39`<sub>h</sub> = A-Z, `3A`<sub>h</sub>-`53`<sub>h</sub> = a-z, `04`<sub>h</sub> = space) |

The first string begins at `0Ch + 4 * count = 23B4h` in every shipped file.

```python
name(actor) = actor.i16[0x102] < 0 ? actor.ptr[0xF8] : entries[2 * (id & ~0x4000) + (flagBank2048[id & ~0x4000] ? 1 : 0)]
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
  raw word, so an id that still carries bit 14 is at least `800`<sub>h</sub> and sets no flag.
- A negative name id makes the actor show its own literal text, which is how `setnpcname(-1)` is
  used by the shipped scripts.

## Related

- [Persistent flag banks](../Story-Events-And-Hunts/story-flags.md): the 2048-bit bank the name flag lives in.
- [Languages](../Saving-Loading-And-Settings/languages.md): which language folder the dictionary is loaded from.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): where the flag bank sits in the save.
- [The spawn keep entry](../Enemy-Spawning/spawn-record-fields.md): where an actor's `+F8`<sub>h</sub> text and `+102`<sub>h</sub> id come from.
