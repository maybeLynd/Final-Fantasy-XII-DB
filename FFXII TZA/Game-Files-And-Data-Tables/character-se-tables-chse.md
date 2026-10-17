---
title: "Character sound tables (chse): the per-model table that names the sound blocks and battle-voice bank a model's animation sounds play from"
kind: "format"
category: "Game files and data tables"
addresses: "002EA530, 021641A8, 002ED950, 002EA6E0, 002E60F0, 002ED910, 003212E0, 0036F0F0, 002E9D90, 002DF9A0"
---

## What the player sees

Each character, monster, summon and weapon model has its own footsteps, cries and swing sounds. Those
sounds are played by the model's animations ([Animation sounds](../Sound-And-Music/animation-sounds.md)), but
the banks they come from are named here: one row per model, giving the sound blocks to load with the model
and, for 39 character, guest and summon models, the bank their battle shouts come from. A model with an
empty row loads no sound blocks; background objects, gadgets and treasure chests ship with every row
empty.

## Where it comes from

### The files

Eight tables ship, one per model class letter, at `ps2data/image/ff12/<in or ch>/common/charseinfo_<letter>.bin`
for the letters `b`, `c`, `g`, `m`, `n`, `s`, `t` and `w`. They are files 12 to 19 of resource kind 9, in
letter order; ids 11 and 20, which the loader also asks for, have no path. Kind 9 is a per-language path
array chosen by `002DF9A0`: the arms for locale ids 7, 8 and 11 (Korean and the two Chinese languages)
install arrays naming the `ch` copies, and every other language gets the `in` copies.

### Loading at boot

`002EA530` runs once, from the binding-table set-up `002EA320`, which boot mode `0022A0B0` reaches through
`00266D10`. For i = 0 to 9 it clears the pointer at `021641A0 + 8 × i` and asks the size of kind 9 file
`0x0B + i` (`0032E400`). When the size is positive it:

1. allocates that many bytes top-down in arena 5 (`0036C1D0(5)`, `0036A190` at `002EA586`);
2. stores the pointer (`002EA596`);
3. files the read `0032E620(9, 0x0B + i, buffer, size, 0)` (`002EA5A9`);
4. labels the block `ChSEinf` (`0036C660` with the string at `00D0F8B0`, `002EA5BB`).

So `021641A8` to `021641E0` hold the tables for `b`, `c`, `g`, `m`,
`n`, `s`, `t` and `w`; nothing frees or reloads them.

## Layouts

`ChseHeader` (`0x10` bytes, offsets from the start of the file):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "CHSE"; ignored |
| `+0x04` | `u16` | version | 1; ignored |
| `+0x06` | `u16` | letter | the file's own letter; ignored |
| `+0x08` | `i32` | count | rows that follow; the row bound |
| `+0x0C` | `u32` | zero | 0; ignored |

`ChseRow` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16` | block0 | SE block for sound group 0; negative = none |
| `+0x02` | `i16` | block1 | SE block for sound group 1, the footsteps; negative = none |
| `+0x04` | `i16` | block2 | SE block for sound group 2; negative = none |
| `+0x06` | `i16` | voiceBank | battle-voice bank number, shoutNN; negative = none |
| `+0x08` | `u8[8]` | unused | 0; ignored |

Row n starts at `16 × (n + 1)` and belongs to the model with number n in that letter class, the model id
`<letter><n>` a script binds ([Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)).
For example row 0 of `charseinfo_c` is `c1004`, the first file of kind 14.

## Shipped data

Measured from the archive, the executable's path arrays and the twelve loose `FileSizeTable_*.fst` files:

| Fact | Value |
|---|---|
| files | 16: 8 tables, each in `in` and `ch`, the two copies byte-identical |
| sizes | `b` 304, `c` 384, `g` 1,680, `m` 4,080, `n` 2,816, `s` 432, `t` 272, `w` 5,248 bytes; `16 + 16 × count` in all 8 |
| header | `CHSE`, version 1, the file's letter at `+0x06`, 0 at `+0x0C`, in all 8 |
| rows, populated | `b` 18, 0; `c` 23, 20; `g` 104, 0; `m` 254, 237; `n` 175, 151; `s` 26, 13; `t` 16, 0; `w` 327, 252; 943 rows, 673 populated |
| unused bytes | `+0x08`-`+0x0F` zero in all 943 rows |
| empty value | every unused slot is `0xFFFF`; no slot holds another negative value |
| `block0` | 252 rows, all in `w`, which uses no other slot; blocks 250-709, 60 distinct |
| `block1` | 338 rows in `c`, `m`, `n` and `s`; blocks 200-249, 46 distinct |
| `block2` | 353 rows in `c`, `m`, `n` and `s`; blocks 300-434, 111 distinct |
| block check | every block id, through the index rule of `002E60F0`, lands on the shipped `se<id>.seb` of the same number |
| `voiceBank` | 39 rows: `c` 14 (banks 0-14), `m` 1 (17), `n` 11 (6-63), `s` 13 (18-30); 35 distinct, bank 5 on 4 rows and bank 7 on 2 |
| voice check | every `voiceBank` names `shoutNN` of the same number in both the kind-33 (`us`) and kind-39 (`jp`) arrays, and both files ship |
| model files | rows map to kind 22 (`b`, file 2n), 14 (`c`, 25n), 13 (`g`, 2n), 34 (`m`, 11n), 19 (`n`, 25n), 23 (`s`, 25n), 25 (`t`, n) and 16 (`w`, n) |
| `.fst` sizes | kind 9 ids 12-19 hold the eight file sizes and ids 11 and 20 hold -1, in all 12 `FileSizeTable_*.fst` |

## Loader behaviour

### The row lookup

`002ED950(boundId)` is the only reader of the table pointers. It takes bits 16-23 as the letter
(`002ED953`-`002ED959`), picks the table through a jump table, and returns
`table + 16 × (row + 1)` for the low 16 bits as the row when the table is loaded and the row is below
the `+0x08` count, compared signed (`002ED9C2`); any other letter, a missing table or a row past the count
gives null. It never checks the magic, the version, the letter field or the file size.

### Slots 0-2: the sound blocks

When a model binding's file arrives, its completion `002E4D20` calls `002EA6E0`, which asks `002ED950`
for the binding's row (`002EA701`).
With a row and no release pending it files a task whose step function is `002E60F0`; without one the
binding is ready at once.

`002E60F0` makes three passes, one per slot. Each pass reads the slot as a signed word (`002E6157`):

- A negative value stores -1 in the binding's slot `+0x30`, `+0x34` or `+0x38` and moves on.
- Otherwise the id becomes a kind-32 file index (`002E6161`-`002E618E`, the rule on
  [Sound banks](../Sound-And-Music/sound-banks.md)). A file with no size is skipped and the slot keeps the
  value 0 that `002E4D20` seeded, not −1, so playback treats it as block handle 0.
- The `.seb` is read into arena 6 and registered with `003A1650`, and the block handle it returns is
  stored in the binding's slot word; a failed registration (-1) moves on.

After the third slot it sets the binding's ready bit, and runs the release `002EAEB0` when one was
requested in the meantime. Sound loading belongs to the binding, so every actor
showing the same model shares one set of blocks.

### Slot 3: the battle-voice bank

`002ED910(actor, boundId)` is called once per model rebuild, from state 4 of the party read-in machine
(`0037B85B`, [Actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md)), with the model the actor's
definition calls for. It returns the actor's own override first: `003212E0` gives the signed word `+0x26`
of the battle unit's `+0xE60` record when the unit's `+0x698` record has byte `+5` = 1. Only when that is
negative, or there is no actor, does it return `voiceBank` sign-extended (`002ED939`).

A bank of 0 or more goes to `0036F0F0(pool, bank)`:

- an entry already holding the bank is reused and its count raised (`0036F240`);
- otherwise it takes a free entry from pool 0 (2 entries at `022D9AB0`) or pool 1 (4 entries at
  `022D9AE0`), unloads what the entry held, and loads the bank's `us` and `jp` files through `0036ED50`
  (kinds 33 and 39, index = the bank);
- with the pool full it returns −1 and the bank is not loaded.

A negative bank skips the pool load and the state that waits for it.

### How animation sounds reach the slots

`002E9D90(actor, group, variant, footstep)` turns an animation sound into a sound id
([Animation sounds](../Sound-And-Music/animation-sounds.md) gives the groups each sound type uses). Its callers
are the verbs `charseplay_move_51e` (`0034B7C0`), `charseplay_voice_520` (`0034C210`) and
`charseplay_weapon_522` (`0034CA40`) ([verb table](../Scripts-And-Script-Commands/verb-table.md)), the emitter
sound helper `0046CC70` that presentation commands `0x19` and `0x29` use, and `0046CC20`
([authored presentation commands](../Graphics/authored-presentation-commands.md)).

It reads the block handle from word `+0x30 + 4 × group` of a binding (`002E9F62`):

- Groups 1 and 2 use the actor's own model binding, `[[actor + 0xC0] + 0x08]`, so `block1` and `block2`.
- Group 0 uses the binding attached in the model's first attach slot, `[[actor + 0xC0] + 0x38]`
  (`002E9F50` adds `0x30`), so `block0` of the attached model. Only the `w` rows author `block0`.
- For group 2 with a variant below 10, when the voice-pool entry (`+0x20`) of the actor the sound
  resolves to (`00263F40`, then `00263F10`) has state 3, its bank loaded, the variant plays from that
  bank instead (`002E9F79`-`002E9F9E`).
- Otherwise the id is the block's registry slot × 512 + variant, or -1 when the handle no longer matches
  its registry record (`003A1240`, called at `002E9FB2`).

## Modding notes

- Row n of `charseinfo_<letter>` is model `<letter>` number n; rows are found by position, so insert none
  and append new rows at the end with `count` raised.
- The buffer is the kind 9 size from the language's `FileSizeTable_*.fst`, rounded up to 64. A grown table
  needs its new size in every `.fst`; the count is never checked against the buffer, so a count past the
  shipped rows reads past it.
- Edit the `in` and `ch` copies alike: which one loads depends on the language.
- Use `0xFFFF` for an empty slot; any value with bit 15 set is treated as none.
- Give `block0`-`block2` only ids that name a shipped `.seb` by the rule on
  [Sound banks](../Sound-And-Music/sound-banks.md): 0-2, 200-499 or 700 and up.
- `block0` sounds only when the model is attached to another model's first attach slot, as weapons are.
  `block1` is the footstep block; its variant is the ground type.
- Keep `voiceBank` from 0 to 63, the length of the kind-33 array; a battle unit with an override word wins
  over it.
- The magic, version, letter, `+0x0C` and each row's last eight bytes are free; nothing reads them.
- The tables are read once at boot.

## Related

- [Animation sounds](../Sound-And-Music/animation-sounds.md): the sound types, groups and variants that read these slots.
- [Sound banks](../Sound-And-Music/sound-banks.md): the `.seb` block index, the block-id rule, the registry and the battle-voice banks.
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): bound ids, letter classes and the binding entry.
- [Actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md): the read-in state that loads the voice bank.
- [File size tables (.fst)](file-size-tables-fst.md): the kind 9 sizes the loader allocates.
- [File requests and the read queue](file-requests-and-the-read-queue.md): the reads the loader files.
- [Languages](../Saving-Loading-And-Settings/languages.md): the locale ids that pick the `in` or `ch` copies.
