[Home](../../README.md) / [Characters and objects](README.md) / NPC names

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| NPC names: the npcdic.bin name pairs, the actor's name id, and the story flag that swaps a name | system | Characters and objects | Field actors | How a field character's name tag is chosen: the name id every actor carries, the pair of strings that id selects in npcdic.bin, the story flag with the same number that switches to the second string once the player has talked to that character, the two script verbs that assign a name id, and the shipped dictionaries for the nine languages. | 0x003EAC40, 0x003EAC70, 0x003EAC10, 0x003EABE0, 0x00263990, 0x002639E0, 0x0026DEA0, 0x00269F40, 0x0034B9A0, 0x0034C170, 0x002E16B0, 0x00379D20, 0x00272CB0, 0x00272CE0, 0x00268D10, 0x00536310, 0x00536280, 0x00267410, 0x005369C0, 0x00272C80 |

## What the player sees

A townsperson's name tag reads "Imperial", "Rabanastran" or "Wistful Bangaa" until the player has
spoken to that person or a script reveals them, after which the same person is "Sherral" or "Arryl".
Nothing about the character changes: every field character carries a name number, the number picks
a pair of names from one file, and a story flag with the same number decides which of the two is
shown. Most pairs repeat the same name twice, so for them the flag changes nothing visible.

## How it works

### The dictionary file

`0x00379D20`, one of the boot loaders, calls `0x003EAC40`, which asks the resource loader for kind 9,
index `0x1F` with the callback `0x003EAC70` (`0x0051ED10(9, 0x1F, 0x003EAC70)`) and keeps the returned
block at `0x02B5E0D8`. Kind 9 index `0x1F` is the language's `bin/npcdic.bin` (see the
[languages page](../Saving-Loading-And-Settings/languages.md) for the language folder). The callback runs
once the block is in memory:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | when `count` is positive, for each of the `count` entries at `+0x0C` it adds the low 32 bits of the block's address to the stored `i32` offset; the accessors sign-extend the entry into a pointer, so the dictionary works because the block lives in the low 2 GB; | `0x003EAC7E`-`0x003EAC8D` |
| 2 | it writes 1 to `+0x04` in either case. | `0x003EAC8F` |

Entry `2 * id` is pair `id`'s first name and entry `2 * id + 1` its second.

### The accessors

| Function | Returns | Refuses |
|---|---|---|
| `0x003EAC10(id, flag)` | entry `2 * id + (flag != 0)` | no block, or the entry index at or above `count` |
| `0x003EABE0(id)` | entry `2 * id + 1`, the second name | the same |

### Which name is shown

`0x00263990(actor)` resolves an actor's display name:

- when the actor's `i16` at `+0x102` is negative, the name is the literal text pointer at `+0xF8`
  (the spawn entry's own text; for such an actor `0x00263A10` returns the word at `+0x100`, and 0 otherwise);
- otherwise bit `0x4000` of the id is stripped, the 2048-bit story flag bank Bank2048 is asked for flag `id`
  (`0x0032A930`, [Story flags](../Story-Events-And-Hunts/story-flags.md)), and
  `0x003EAC10(id, flagSet)` returns the first name while the flag is clear and the second once it is
  set.

`0x002639E0(id)` does the same from a bare id and `0x0026DEA0(id, flag)` from an explicit pair. Among the callers that put
the name on screen are the text interpreter `0x002AC5F0`¹, `0x002B0280`²,
`0x00272CB0` (the name for an actor handle resolved by `0x003588B0`, or the empty string `0x01CEB638`), `0x00272CE0` and the
field interaction pass `0x00268D10`, which passes the name to `0x003DF760(..., 3, ...)` for an actor whose `+0x1C` bit
`0x2000` is set and whose name's first byte is not 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002ADDAA`, `0x002ADEA3` |
| ² | `0x002B16D4`, `0x002B1730` |
| ³ | `0x00268E58` |

</details>

`0x00272CE0(buffer, handle)` copies the name into a caller's buffer. It writes the empty string when the handle
does not resolve¹ or the name is null². When the 16-bit word `0x00263A10`
returns is non-zero, it builds the text for that word with `0x0024ABE0` in a 32-byte buffer (`0x00272D3C`-`0x00272D48`;
the ordinal's letter, [Enemy names on screen](../Menus-And-HUD/enemy-names-on-screen.md)) and appends it after the name³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003588B0`, `0x00272D0B` |
| ² | `0x00272DA6` |
| ³ | `0x00272D6E`-`0x00272D9D` |

</details>

`0x00268D10` does so on every run in which the talk candidate's record resolves, whether or not it files the talk¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00268E3A`-`0x00268E7F` |

</details>

### Who sets the flag

The message window opener `0x002E16B0(actor, ...)` begins, for a non-null actor, with
`0x0032ABF0(actor +0x102, 1)`¹: opening a conversation with a character sets
that character's name flag, and the setter ignores ids at or above `0x800` as unsigned, so a
literal-named actor (negative id) sets nothing. Scripts can set or clear the same flag through the
flag-bank verbs.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E16DF`-`0x002E16EB` |

</details>

### Who sets the id

`0x00269F40(actor, id)` stores the low 16 bits of the id at `+0x102`¹; a non-negative id has bit
`0x4000` cleared first², and a negative one keeps its low 16 bits as they are. Two script verbs reach it:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00269F48` |
| ² | `0x00269F44` |

</details>

| Verb | Id | Handler | What it does |
|---|---|---|---|
| `setnpcname(id)` | `0x38A` | `0x0034B9A0` | pops the integer (`0x00267E10`); a negative id is stored only when `0x003EABE0(id)` returns a non-null entry |
| `setshopname(shop)` | `0x4A9` | `0x0034C170` | pops the shop index, maps it to the shop record's first `u16` through `0x002FAE40` (the table at `[0x02EBF158]`; an index at or above the record count gives 0, pair 0; the count is the table's word `+0x06`, and 0 with no table; the test is signed (`0x002FAE62`-`0x002FAE64`), so a negative index reads the word at the index times the stride `+0x04` before the first record, whose offset is at `+0x08` (`0x002FAE78`-`0x002FAEA4`), or the word at address 0 with no table), pushes it back (`0x00267F90`) and then stores it like `setnpcname` |

The accessors have no lower bound. For `setnpcname(-1)`, `0x003EABE0` computes index `2 * -1 + 1 = -1`
and reads the dword before the entry array, the dictionary's own `count` (`+0x08`), so -1 is accepted
whenever the dictionary is loaded with a non-zero count; -2 reads the magic at `+0x00` and is always
accepted; lower ids down to -0x40000000 read the memory before the block. Below that, `2 * id + 1` wraps in
32 bits¹ to a non-negative index that the signed `count` test² refuses unless it is
below `count`: -0x7FFFFFFF gives index 3, a real entry.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EABE0` |
| ² | `0x003EABF6` |

</details>

A stored negative id makes the actor show its literal text at `+0xF8` only when bit `0x8000` of its low word is set,
as for every id from -0x8000 to -1. An accepted id such as -0x10000 is stored as 0¹ and is read
as name id 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00269F48` |

</details>

Three script verbs store that literal text on the verb's target actor with `0x00269F20(actor, text, 0)`, which writes
the text pointer at `+0xF8` and 0 at `+0x100` (`0x00269F20`-`0x00269F27`; [EBP text
sections](../EBP-Script-Files/ebp-text-sections.md)).

`fieldsignmes` (`0x178`, `0x00356B70`) takes the row of section 2 of the issuing script that the popped text id names,
through `0x00264D60`¹; `fieldsignmesbyid` (`0x179`, `0x00357120`) takes the row of section 3, through
`0x00264D90`²; `fieldsign` (`0x176`, `0x00355A00`) looks the popped sign id up with `0x002642C0`, changes
nothing when it finds no sign record³, and otherwise takes the section 3 row that the record's word
`+0x0A` names⁴, or the empty string at `0x02F8F2A0` when that word is negative⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00356B9A` |
| ² | `0x0035714A` |
| ³ | `0x00355A2E` |
| ⁴ | `0x00355A90`-`0x00355AAD` |
| ⁵ | `0x00355AC3`-`0x00355AD0` |

</details>

### Ids past the dictionary

Every shipped dictionary has `count` 2282, 1141 pairs, so names exist for ids 0 to 1140. A larger id gives a null
name: `0x003EAC10` and `0x003EABE0` refuse an entry index at or above `count`¹, and `0x00263990`
and `0x002639E0` return what `0x003EAC10` returns. After bit `0x4000` is stripped an actor's id is at most `0x3FFF`, so
ids 1141 to 16383 reach no name. The flag test answers 0 for ids at or above `0x800`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EAC29`, `0x003EABF6` |
| ² | `0x0032A934`-`0x0032A945` |

</details>

`setnpcname` stores a non-negative id without asking the dictionary (`0x0034B9B7`-`0x0034B9B9` jump past the test to
`0x0034B9C7`), and so does `setshopname`¹. Nothing but the value the script passes keeps an
actor id below 1141.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0034C1A3`-`0x0034C1A5` |

</details>

What these callers do with a null name:

| Caller | Site | With a null name |
|---|---|---|
| nine readers of `0x00263990` and `0x002639E0` | `0x0025C5C9`, `0x0025C679`, `0x0025D0C5`, `0x0025D192`, `0x002ADEB3`, `0x002ADDBA`, `0x002B173A`, `0x002B16DE`, `0x002B52F4` | test it and skip the name |
| `0x00272CE0` | `0x00272D22`-`0x00272D25` | writes the empty string (`0x00272DA6`) |
| the battle menu's target-list row painter `0x0027E530`, through `0x00272CB0` | `0x0027E626` | stores it at `+0x1578`, the `+0x28` of the record `+0x1550` that `0x002D8650` hands to `0x002B0280`, which tests it and returns (`0x002B02BD`) |
| a formatted message, through `0x00272CB0` | `0x0027ACE6` | passes it to `0x002B4090` with text `0x7D0`; the formatter skips a null string argument (`0x002B4D7E`) |
| the widest-name measure | `0x002BA5DA`, `0x002BA5F0` | `0x0029CD00` measures it as 0 by 0 (`0x002B313F`-`0x002B3163`) |
| the shop screens, through `0x003EABE0` | `0x0057B9B7`, `0x0057C029` | `0x002CA150` copies it with `0x00254F30`, which copies nothing from a null source (`0x00254F39`) |
| battle messages, through `0x0026DEA0` | `0x00536578` | copied with `0x00254F30`, the same |
| the field interaction pass `0x00268D10` | `0x00268E4D` | reads the first byte at once (`0x00268E55`): for an actor whose `+0x1C` bit `0x2000` is set, a name id from 1141 to 16383, or any id while no dictionary is loaded (`0x003EAC24`), reads address 0 |

### Names in battle messages

The battle message composer `0x005369C0` (called from `0x0046AB10`) names the acting and the target
unit from their stats records, in three steps:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `0x00536310(stats, &fromDictionary)` picks a name reference. A null record gives `0xFFFF`, and a kind-0 record (byte `+0x05`) gives word `+0x30` of the party table row its byte `+0x04` names. It sets `fromDictionary` to 0 first. | `0x00536325` |
| 2 | For any other kind it finds the owning unit (`0x0031B860`, which scans the unit pool for the unit whose `+0x698` is the record) and keeps it at `[0x02EBF188]`. When that unit and its actor `+0x10` exist and the actor has a name id of 0 or more (`0x00267410` tests `+0x102 >= 0`), it returns the id with `fromDictionary` = 1; otherwise word `+0x08` of the unit's definition row `+0xE60`, or 0 with no unit. | `0x005363AA`<br>`0x00263B40` |
| 3 | `0x00536280(ref, fromDictionary)` turns the reference into text. From the dictionary it calls `0x0026DEA0(ref, 1)`, so an enemy with an NPC name id is always named by the pair's second name, whatever the actor's name flag holds. Otherwise `0xFFFF` gives the empty string `0x01CEB638`, and any other reference is split into a bank (`ref >> 11`) and an entry (`ref & 0x7FF`) of the text banks at `[0x02EBF170]` and rendered by `0x002B58B0`. |   |

The party table rows of step 1 start at the offset at `[0x02EBF130] + 0x0C`¹, at the stride in word
`+0x08`²; with no table at `[0x02EBF130]` the step reads the word at address `0x30`. The
fallback of step 2 looks the unit up a second time³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0020E600` |
| ² | `0x00536356`-`0x00536388` |
| ³ | `0x005363DF`-`0x005363F0` |

</details>

With no banks bound at `[0x02EBF170]`, `0x00536280` hands `0x002B58B0` a null row and the name is null¹. The bank and the entry are offsets resolved through `0x0020E600`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005362D7`-`0x005362E1`, `0x002B58B5` |
| ² | `0x005362AC`-`0x005362BF` |

</details>

`0x00272C80(handle)` returns `0x00263A10` of the actor a handle resolves to¹, and -1 when it
does not resolve.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003588B0` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

Struct NpcDictionary base=npcdic.bin size=file:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0000` | `u8[4]` | magic | "NPC0" |
| `+0x0004` | `u32` | relocated | 0 in the file; `0x003EAC70` writes 1 after relocation |
| `+0x0008` | `u32` | count | 2282 in every shipped language: 1141 pairs |
| `+0x000C` | `i32[2282]` | entries | file offsets of the strings; string pointers once relocated |
| `+0x23B4` | `u8[]` | strings | zero-terminated, in the script text encoding (`0x20`-`0x39` = A-Z, `0x3A`-`0x53` = a-z, `0x04` = space) |

The first string begins at `0x0C + 4 * count = 0x23B4` in every shipped file.

```python
name(actor) = actor.i16[0x102] < 0 ? actor.ptr[0xF8] : entries[2 * (id & ~0x4000) + (flagBank2048[id & ~0x4000] ? 1 : 0)]
```

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

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

### Every pair and what reveals its second name

[`npc-name-pairs.tsv`](npc-name-pairs.tsv) has one row for each of the 1,141 pairs of the `us` file. A row gives the
pair, its two names, whether they differ, and the scripts that set, release or test the pair's flag with
`settalknpcname` (`0x399`), `releasetalknpcname` (`0x39A`) and `istalknpcname` (`0x39B`), counted over the 1,114 `us`
scripts.

- 247 pairs have two different names. Each second name appears once flag `id` of the 2048-bit bank is set: by any
  message window whose speaker has that name id¹, or by `settalknpcname`. `releasetalknpcname` clears the
  flag, and the first name comes back.
- 93 pairs appear in the scripts' 57 `settalknpcname`, 79 `releasetalknpcname` and 1 `istalknpcname` calls.
- Seven `settalknpcname` calls take the id from a script array. The table lists such a script under every id the
  array is given, marked "(array)".

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E16B0` |

</details>

### Columns of npc-name-pairs.tsv

| Column | Holds |
|---|---|
| `pair_hex` | the pair number of `pair` in hex, four digits (`0x0000` to `0x0474`), the form the scripts' name ids take |
| `set_by_scripts` | the scripts that call `settalknpcname` (`0x399`) with the pair's id, separated by semicolons; `x2` to `x5` after a script name gives its number of calls when it is more than one, and "(array)" marks a call that takes the id from a script array; `-` on the 1,068 pairs no script sets |
| `released_by_scripts` | the scripts that call `releasetalknpcname` (`0x39A`) with the pair's id, in the same form; every one is `evt_t0090`, once to four times; `-` on 1,105 pairs |
| `tested_by_scripts` | the scripts that call `istalknpcname` (`0x39B`) with the pair's id: `sav_b01` for one pair, `-` on the other 1,140 |

### Where each name is given

[`npc-names-maps.tsv`](npc-names-maps.tsv) has one row per name pair and script, from every `setnpcname` step
with a fixed id in the script step tables of the area pages, from the same calls in the spawn groups of the zone
scripts, which those tables leave out, and from the crystal actor
([Shared zone-script actors](../Story-Events-And-Hunts/shared-zone-script-actors.md)). A row gives:

- the pair's two `us` names;
- the script, the zone it plays in, with the field number, map name and region; a scene script is placed at the
  zone script that loads it;
- how many actors of the script take the name, and their actor names.

What it shows:

- 3,722 steps with a constant id, 7 of them calls on another actor such as `THIRD_ガリフ.setnpcname`, 50 calls in
  spawn groups and the 33 array steps below that name a person give 1,583 rows: 775 pairs in 516 scripts. 198 of
  the pairs have two different names.
- The 50 spawn-group calls name a foe of the group only while `btlAtelIsMimicName` returns 1, bit `0x20` of its
  spawn record's byte `+0` ([Battle units](battle-units.md)): 47 give it Treasure, the chests' name, and 3 a
  crystal's name. Otherwise the group calls `setnpcname(-1)` (50 calls), and the foe shows its own text at `+0xF8`.
- The groups' talk functions `btalk00` to `btalk05` call `setnpcname(-1)` before `btlAtelMimicFunction(0)` (41 calls
  in 18 scripts), so the foe goes back to its own text when its talk function runs.
- The save and gate crystal actor is shared by the crystal maps. It picks the crystal's pair by the number
  `getcrystalid` returns: 0 is Save Crystal, 255 Life Crystal, each of 25 gate numbers its own place's crystal, and
  any other number Gate Crystal. Its rows are its 80 loaded crystals
  ([Save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md)).
- `bts_z01`, `pre_a01` and `pre_b01`, fields 108, 109 and 114, name their treasure chests, and `bts_h01` and
  `bts_y01`, fields 80 and 107, a foe of a spawn group, but no zone-script entry names those scripts.
- 89 more steps, one in each of 89 scripts, take the id from an array of the script's own data, indexed by the
  person: `NPC01`'s background people in `clip_show` in 52 scripts, and `NPC_LABO_0`'s `begin` in 37 Draklor
  Laboratory scripts. The arrays start at 0 in every script, and `EventDirector`'s `init` stores their values as
  constants. In the table these rows name the actor as `NPC01 (clip_show, person k)` or
  `NPC_LABO_0 (begin, person k)`.
  - 33 of the steps name people this way.
  - In 21 scripts no step requests `NPC01`'s `clip_show`, so its step never runs.
  - In 30 Draklor Laboratory scripts no step stores the flag array that `begin` tests, so `begin` skips the verb.
  - In 5 Archades scripts (`alc_b03`, `alc_b04`, `alc_c01`, `alc_f01`, `alc_f02`) every placed person's flag has
    bit `0x2` set. `clip_show` disables talk and skips the verb when the flag ANDed with `0xA` is not 0.

### Columns of npc-names-maps.tsv

| Column | Holds |
|---|---|
| `name_pair_hex` | the pair number of `name_pair` in hex, four digits, as `pair_hex` in npc-name-pairs.tsv; it equals `name_pair` on all 1,583 rows |

</details>

## Modding notes

- To rename a character, edit its pair in `npcdic.bin`; to make a reveal happen, set story flag
  `id` in Bank2048. The second name needs no script change.
- Pairs whose two strings are identical are inert: setting their flag changes nothing visible, and
  the set of visible reveals differs by language (247 ids in English, 275 in French).
- Ids with bit `0x4000` set reach the same pair as without it: `0x00269F40` strips the bit on store and
  `0x00263990` before the flag test and the lookup. The conversation setter in `0x002E16B0` passes the
  raw word, so an id that still carries bit `0x4000` is at least `0x800` and sets no flag.
- A negative name id makes the actor show its own literal text, which is how `setnpcname(-1)` is
  used by the shipped scripts.
- A new name needs a new pair in `npcdic.bin`: an actor id at or above the pair count has no name, and the field
  interaction pass reads its name without a test¹, so such an id on an actor with `+0x1C` bit `0x2000`
  set reads address 0. `setnpcname` does not check a non-negative id.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00268E55` |

</details>

## Related

- [Story flags](../Story-Events-And-Hunts/story-flags.md): Bank2048, the 2048-bit bank the name flag lives in.
- [Languages](../Saving-Loading-And-Settings/languages.md): which language folder the dictionary is loaded from.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): where the flag bank sits in the save.
- [Actor record: the record every field actor is driven through, its pool, its classes, its sub-objects and its lifetime](actor-record.md): the set-up that starts an actor with `+0xF8` the empty string and `+0x102` = `0xFFFF`.
