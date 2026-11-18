[Home](../../README.md) / [Game files and data tables](README.md) / Character sound tables (chse)

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Character sound tables (chse): the per-model table that names the sound blocks and battle-voice bank a model's animation sounds play from | format | Game files and data tables | Data tables and configs | The charseinfo_&lt;letter&gt;.bin files: one CHSE table per model class with one 16-byte row per model number, giving three SE block ids and a battle-voice bank; the boot loader that reads all eight, the row lookup by bound id, the block loads and the voice-bank fallback that read the rows, how animation sounds pick a slot, the 943 shipped rows, and the rules an edited table must follow. | 0x002EA530, 0x021641A8, 0x002ED950, 0x002EA6E0, 0x002E60F0, 0x002ED910, 0x003212E0, 0x0036F0F0, 0x002E9D90, 0x002DF9A0 |

## What the player sees

Each character, monster, summon and weapon model has its own footsteps, cries and swing sounds. Those
sounds are played by the model's animations ([Animation sounds](../Sound-And-Music/animation-sounds.md)), but
the banks they come from are named here: one row per model, giving the sound blocks to load with the model
and, for 39 models (14 characters, 11 NPC models, 13 summons and the monster model `m1208`), the bank their
battle shouts come from. A model with an
empty row loads no sound blocks; background objects, gadgets and treasure chests ship with every row
empty.

When a model's file arrives, the game reads its row and loads the named sound blocks with it. An animation sound then
picks a block by its group: groups 1 and 2, footsteps among them, come from the model's own row, and group 0 from the
row of the model held in its first attach slot, as weapons are.

## Where it comes from

### The files

Eight tables ship, one per model class letter, at `ps2data/image/ff12/<in or ch>/common/charseinfo_<letter>.bin`
for the letters `b`, `c`, `g`, `m`, `n`, `s`, `t` and `w`. They are files 12 to 19 of resource kind 9, in
letter order; ids 11 and 20, which the loader also asks for, have no path. Kind 9 is a per-language path
array chosen by `0x002DF9A0`: the arms for locale ids 7, 8 and 11 (Korean and the two Chinese languages)
install arrays naming the `ch` copies, and every other language gets the `in` copies.

### Loading at boot

`0x002EA530` runs once, from the binding-table set-up `0x002EA320`, which boot mode `0x0022A0B0` reaches through
`0x00266D10`. For i = 0 to 9 it clears the pointer at `0x021641A0 + 8 × i` and asks the size of kind 9 file
`0x0B + i` (`0x0032E400`). When the size is positive it:

1. allocates that many bytes top-down in arena 5 (`0x0036C1D0(5)`, `0x0036A190` at `0x002EA586`): `0x0036C1D0(5, 5)`
   pushes the arena and `0x0036C140` pops it again right after the allocation (`0x002EA58E`);
2. stores the pointer (`0x002EA596`), with no test for a null allocation;
3. files the read `0x0032E620(9, 0x0B + i, buffer, size, 0)` (`0x002EA5A9`);
4. labels the block `ChSEinf` (`0x0036C660` with the string at `0x00D0F8B0`, `0x002EA5BB`), with i as the tag
   (`0x002EA5AE`).

So `0x021641A8` to `0x021641E0` hold the tables for `b`, `c`, `g`, `m`,
`n`, `s`, `t` and `w`; nothing frees or reloads them.

## Layouts

All multi-byte fields are little-endian.

`ChseHeader` (`0x10` bytes, offsets from the start of the file):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "CHSE"; ignored |
| `+0x04` | `u8[2]` | version | bytes 01 00 in all 8 files; read by no function: the eight table pointers are loaded by one function, `0x002ED950` (`0x002ED977`-`0x002ED9B6`), which reads the count at `+0x08` and returns a row address, and the file is copied whole by the read `0x0032E620`; nothing fixes its width |
| `+0x06` | `u8[2]` | letter | the file's own letter then 0, in all 8 files; read by no function: as for `+0x04`, the one loader `0x002ED950` reads only the count `+0x08` (`0x002ED9C2`) and `0x0032E620` copies the file whole; nothing fixes its width |
| `+0x08` | `i32` | count | rows that follow; the row bound |
| `+0x0C` | `u8[4]` | zero | 0 in all 8 files; read by no function: as for `+0x04`, the one loader `0x002ED950` reads only the count `+0x08` (`0x002ED9C2`) and `0x0032E620` copies the file whole; nothing fixes its width |

`ChseRow` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16` | block0 | SE block for sound group 0; negative = no block |
| `+0x02` | `i16` | block1 | SE block for sound group 1, the footsteps; negative = no block |
| `+0x04` | `i16` | block2 | SE block for sound group 2; negative = no block |
| `+0x06` | `i16` | voiceBank | battle-voice bank number, shoutNN; negative = no bank |
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
| block check | every block id, through the index rule of `0x002E60F0`, lands on the shipped `se<id>.seb` of the same number |
| `voiceBank` | 39 rows: `c` 14 (banks 0-14), `m` 1 (17), `n` 11 (6-63), `s` 13 (18-30); 35 distinct, bank 5 on 4 rows and bank 7 on 2 |
| voice check | every `voiceBank` names `shoutNN` of the same number in both the kind-33 (`us`) and kind-39 (`jp`) arrays, and both files ship |
| model files | rows map to kind 22 (`b`, file 2n), 14 (`c`, 25n), 13 (`g`, 2n), 34 (`m`, 11n), 19 (`n`, 25n), 23 (`s`, 25n), 25 (`t`, n) and 16 (`w`, n) |
| `.fst` sizes | kind 9 ids 12-19 hold the eight file sizes and ids 11 and 20 hold -1, in all 12 `FileSizeTable_*.fst` |

[`character-se-rows.tsv`](character-se-rows.tsv) holds all 943 rows, each with the model it belongs to: `letter`, `number`, `bound_id`, the
model's `.cm` path (`model`), the four values (`block0`, `block1`, `block2`, `voice_bank`, empty when negative), the
`.seb` each block names (`se_files`), the `shoutNN` bank (`shout`) and `populated`. [Model asset list](../Graphics/model-asset-list.md)
gives the same blocks per model, beside the model's other files.

## Loader behaviour

### The row lookup

`0x002ED950(boundId)` is the only reader of the table pointers. It takes the bits under mask `0xFF0000` as the letter
(`0x002ED953`-`0x002ED959`), picks the table through a jump table, and returns
`table + 16 × (row + 1)` for the low 16 bits as the row when the table is loaded and the row is below
the `+0x08` count, compared signed (`0x002ED9C2`); any other letter, a missing table or a row past the count
gives null. It never checks the magic, the version, the letter field or the file size.

### Slots 0-2: the sound blocks

When a model binding's file arrives, its completion `0x002E4D20` calls `0x002EA6E0`, which asks `0x002ED950`
for the binding's row (`0x002EA701`).
With a row and no release pending it files a task whose step function is `0x002E60F0`; without one the
binding is ready at once.

With a row and no release pending, `0x002EA6E0` first writes the three zero values `0x002E4D20` passes into
the slots `+0x30`, `+0x34` and `+0x38` (`0x002EA720`-`0x002EA72F`), and only then tests the task `0x002F16B0`
gave: with all 32 tasks taken it files nothing (`0x002EA734`), the binding is ready at once and its slots
stay 0. Without a row, or with a release pending (`0x002EA6FC`), the slots keep the `0xFFFFFFFF` the
allocator `0x002E25E0` set (`0x002E2627`, `0x002E262B`).

`0x002E60F0` makes three passes, one per slot. Each pass reads the slot as a signed word (`0x002E6157`):

- A negative value stores -1 in the binding's slot `+0x30`, `+0x34` or `+0x38` and moves on.
- Otherwise the id becomes a kind-32 file index (`0x002E6161`-`0x002E618E`, the rule on
  [Sound banks](../Sound-And-Music/sound-banks.md)). A file with no size is skipped and the slot keeps the
  value 0 that `0x002E4D20` seeded, not −1, so playback treats it as block handle 0.
- The `.seb` is read into arena 6: a buffer from `0x0036B160` between `0x0036C1D0(6, 5)` and `0x0036C140`, and
  the read `0x0032E620` (`0x002E6277`). The slot holds the buffer handle while the task waits, one step at a time,
  until `0x0032E4D0` answers 0 (`0x002E6290`).
- Then `0x0036D200` runs on the handle (`0x002E61D6`). A handle of 0 stores -1 and moves on (`0x002E622D`). Any other
  is registered with `0x003A1650`, and the block handle it returns is
  stored in the binding's slot dword; a failed registration (-1) moves on, and otherwise the task waits until
  `0x003A1290` answers 2 (`0x002E61FE`).

After the third slot it sets the binding's ready bit, and runs the release `0x002EAEB0` when one was
requested in the meantime (`0x002E629E`-`0x002E62AB`); its step state is then 9, which later steps leave as it is
(`0x002E62C9`). The row is read with no null test (`0x002E6157`), and `0x002EA6E0` files the task only for a model with
a row. Sound loading belongs to the binding, so every actor
showing the same model shares one set of blocks.

### Slot 3: the battle-voice bank

`0x002ED910(actor, boundId)` is called once per model rebuild, from state 4 of the party read-in machine
(`0x0037B85B`, [Actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md)), with the model the actor's
definition calls for. It returns the actor's own override first: `0x003212E0` gives the signed word `+0x26`
of the battle unit's `+0xE60` record when the unit's `+0x698` record has byte `+5` = 1. Only when that is
negative, or there is no actor, does it return `voiceBank` sign-extended (`0x002ED939`).

`0x003212E0` returns -1 for a null actor, a null unit (`0x00263E30`, the actor's `+0x30`), a null `+0x698`
record or a byte `+5` other than 1 (`0x003212E7`-`0x00321303`); it reads `+0xE60` with no null test
(`0x00321305`). With no actor `0x002ED910` skips `0x003212E0` (`0x002ED91F`). When `0x002ED950` finds no row for the
model, `0x002ED910` returns the override's negative answer, or -1 with no actor (`0x002ED943`).

A bank of 0 or more goes to `0x0036F0F0(pool, bank)`, which itself returns −1 for a negative bank
(`0x0036F104`):

- an entry already holding the bank is reused and its count raised (`0x0036F240`): the match needs a non-zero
  state byte `+0` and the id `+0x14`; the count `+0x16` is raised and byte `+3` cleared (`0x0036F118`,
  `0x0036F11C`);
- otherwise it takes a free entry, the first whose count is 0, from pool 0 (2 entries at `0x022D9AB0`) or,
  for any other pool number, pool 1 (4 entries at `0x022D9AE0`), unloads what the entry held, and loads the
  bank's `us` and `jp` files through `0x0036ED50` (kinds 33 and 39, index = the bank);
- the unload runs only when the entry's handle `+0x0C` is set: `0x002DF440` (a jump to `0x001DC100`) with byte
  `+1`, plus 2 when byte `+2` is non-zero, then `0x00369800` on `+0x0C` and on `+0x10`, and `+0x04` to `+0x13`
  are zeroed (`0x0036F1C8`-`0x0036F1FF`); the count is then set to 1 and the id to the bank (`0x0036F21C`,
  `0x0036F220`);
- it returns `(+2 << 4) | +1` of the entry (`0x0036F124`, `0x0036F217`);
- with the pool full it returns −1 and the bank is not loaded.

A negative bank skips the pool load and the state that waits for it.

### How animation sounds reach the slots

`0x002E9D90(actor, group, variant, footstep)` turns an animation sound into a sound id
([Animation sounds](../Sound-And-Music/animation-sounds.md) gives the groups each sound type uses). Its callers
are the verbs `charseplay_move_51e` (`0x0034B7C0`), `charseplay_voice_520` (`0x0034C210`) and
`charseplay_weapon_522` (`0x0034CA40`) ([verb table](../Scripts-And-Script-Commands/verb-table.md)), the emitter
sound helper `0x0046CC70` that presentation commands `0x19` and `0x29` use, and `0x0046CC20`
([authored presentation commands](../Graphics/authored-presentation-commands.md)).

It reads the block handle from dword `+0x30 + 4 × group` of a binding (`0x002E9F62`). The binding hangs off
`+0xC0` of the actor the sound resolves to: `0x00263F40` (`0x002E9DF9`) replaces an actor whose byte `+0x18` is 1
with the record `0x003587C0` finds for its byte `+0x19` and word `+0x1A`, when it finds one.

- Groups 1 and 2 use the actor's own model binding, `[[actor + 0xC0] + 0x08]`, so `block1` and `block2`.
- Group 0 uses the binding attached in the model's first attach slot, `[[actor + 0xC0] + 0x38]`
  (`0x002E9F50` adds `0x30`), so `block0` of the attached model. Only the `w` rows author `block0`.
- A group above 2, a null `+0xC0` or a null binding gives -1 (`0x002E9E72`, `0x002E9F4E`, `0x002E9F60`).
- For group 1 with a footstep flag of 0 or more the variant argument is replaced by the footstep sound
  worked out from the ground type ([Small bin tables](small-bin-tables.md)); a negative flag keeps the
  variant and clears the flag (`0x002E9E99`).
- For group 2 with a variant below 10, when the voice-pool entry (`+0x20`) of the actor the sound
  resolves to (`0x00263F40`, then `0x00263F10`) is 0 or more and has state 3, its bank loaded, the variant
  plays from that bank instead (`0x002E9F79`-`0x002E9F9E`). The id is then `0x40000000 | slot << 8 | variant`,
  the slot from `0x0036EC50`; an id that comes out negative goes on to the block lookup (`0x002E9FA0`).
- `0x0036EC50(handle)`, for a handle other than -1, finds the voice-pool record
  `0x022D9AB0 + 0x18 × (handle & 0xF)` when `handle & 0xF0` is 0, and the one at the same
  index from `0x022D9AE0` otherwise, and
  answers the record's signed byte `+0x01`, plus 2 when its byte `+0x02` is not 0
  (`0x0036EC65`-`0x0036EC9B`).
- Otherwise a non-zero footstep flag first adds the weather variant flag `0x02099DBC` to the variant
  (`0x002E9FA7`), and the id is the block's registry slot × 512 + variant, or -1 when the handle no longer
  matches its registry record (`0x003A1240`, called at `0x002E9FB2`).
- When the voice id came out negative and `0x003A1240` answers -1, `0x002E9D90` answers
  that negative voice id, not -1: the result is replaced only by an answer other than
  -1 (`0x002E9FA0`, `0x002E9FB7`-`0x002E9FBA`).

Before any of that, `0x002E9D90` returns -1, so no sound plays, while byte `0x022CB726` is set (`0x003603C0`,
`0x002E9DB2`), while a skip of mask index 1 to 3 has executed (`0x00360670`, `0x002E9DBF`), while the bytes
`0x0215FD54` and `0x0215FD55` are not both set (`0x002E9DC5`-`0x002E9DD5`), for a negative variant (`0x002E9DDD`) and
for a null actor (`0x002E9DF0`). The script binder `0x0026C8C0` sets both bytes to 1 through `0x002EC590(1)` and
`0x002EC5A0(1)` (`0x0026CA75`, `0x0026CA7F`).

It also returns -1 unless the resolved actor's manager `0x00263FF0(byte +0x15)` has bit `0x20` of `+0x17` set
and a byte `+0x10` below `0x80` with bit `0x1` set, manager 0's byte `+0x10` is below `0x80`, and the actor
has bit `0x10` of `+0x08` set (`0x002E9E24`-`0x002E9E53`).

`0x0215FD55`'s setter `0x002EC5A0` has only that call. `0x0215FD54`'s setter `0x002EC590` is also
reached by tail jumps from the script verbs setcharseplayall (`0x0033F227`, argument not 0), stopenvsoundall
(`0x00354C68`, 0) and startenvsoundall (`0x00355081`, 1), so a script can switch the character sounds off and on
again. Both bytes are 0 until the first script binding:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0215FD54` | `u8` | 0 (zero-filled tail of `.data`) | the first of the two gate bytes of the character sound player: 1 once a script has been bound, 0 after stopenvsoundall, 1 again after startenvsoundall or setcharseplayall with an argument other than 0 | `0x002EC590` (`0x002EC590`, its argument), from `0x0026C8C0` (`0x0026CA75`, 1), setcharseplayall `0x0033F210` (`0x0033F227`, argument not 0), stopenvsoundall `0x00354C50` (`0x00354C68`, 0) and startenvsoundall `0x00355060` (`0x00355081`, 1) | `0x002E9D90` (`0x002E9DCC`) |
| `0x0215FD55` | `u8` | 0 (zero-filled tail of `.data`) | the second of the two gate bytes of the character sound player, 1 once a script has been bound | `0x002EC5A0` (`0x002EC5A0`, its argument), from `0x0026C8C0` (`0x0026CA7F`, 1) | `0x002E9D90` (`0x002E9DC5`) |

## Modding notes

- Row n of `charseinfo_<letter>` is model `<letter>` number n; rows are found by position, so insert no rows
  and append new rows at the end with `count` raised.
- The buffer is the kind 9 size from the language's `FileSizeTable_*.fst`, rounded up to 64. A grown table
  needs its new size in every `.fst`; the count is never checked against the buffer, so a count past the
  shipped rows reads past it.
- Edit the `in` and `ch` copies alike: which one loads depends on the language.
- Use `0xFFFF` for an empty slot; any value with bit `0x8000` set is treated as an empty slot.
- Give `block0`-`block2` only ids that reach a shipped `.seb` by the rule on
  [Sound banks](../Sound-And-Music/sound-banks.md): 0, 2, 200-434 and 700-709 load the `.seb` of the same number,
  id 1 loads `se007.seb`, ids 192, 193 and 195 load `se000`, `se007` and `se002`, and ids 500-634 load
  `se300`-`se434`.
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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat: `0x00263E30` is called by `0x003206E0`; those functions are documented on
  [battle units](../Characters-And-Objects/battle-units.md).
- Combat AI: `0x00263E30` is called by `0x003247F0`, `0x00324F20`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md).
- Combat formula: `0x00263E30` is called by `0x00320A70`; those functions are documented on
  [battle log](../Battle-Actions/battle-log.md).
- Gameplay: `0x00263E30` is called by `0x003176E0`, `0x0031ADB0`, `0x00321380`; those functions are documented on
  [battle units](../Characters-And-Objects/battle-units.md), [bestiary](../Enemy-Spawning/bestiary.md),
  [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md).
- Save load settings: `0x0032E4D0` is called by `0x00280140`; those functions are documented on
  [resource arena and relocation](resource-arena-and-relocation.md).
- Status periodic terminal: `0x00263E30` is called by `0x00386860`; those functions are documented on
  [status timers](../Status-Effects-And-KO/status-timers.md).
- Story event quest hunt: `0x0026C8C0` calls `0x00377440`; those functions are documented on
  [actor managers](../Characters-And-Objects/actor-managers.md).
- UI: `0x00263E30` is called by `0x0031EB20`; those functions are documented on
  [action definition row](../Battle-Actions/action-definition-row.md).
