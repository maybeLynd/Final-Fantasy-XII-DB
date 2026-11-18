[Home](../../README.md) / [Story, events and hunts](README.md) / Story flags

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Story flags: the five banks of yes-or-no flags the save keeps, the story schedule some flag ids read instead, who sets and reads each, and the flags a new game starts with | system | Story, events and hunts | Story progress and flags | How the game remembers what has happened: the five flag banks in the save payload with their offsets and id ranges, the accessors and their bounds, the encoded id whose bit `0x4000` reads the story schedule in mapjumpgroupflagrom.bin instead of a flag, ids 0 and 1 as always and never, what each bank holds (map-jump groups and map icons, names learned by talking, chests opened and traps fired, two script-only banks), every native setter and reader, the main menu items the schedule unlocks, and the reset that clears the banks and sets the 52 starting flags. | 0x0032A8A0, 0x00377970, 0x0032AB60, 0x0032ABF0, 0x0032AD70, 0x0032AA60, 0x00379160, 0x002EF2D0 |

## What the player sees

- Places on the map open up, characters' names appear once they have spoken, and a one-time chest stays empty once it
  is opened: its flag is in the save. Most chests have no flag and can be there again later
  ([treasure chests](../World-Areas-And-Travel/treasure-chests.md)).
- Some menu entries, such as Equip, Licenses, Gambits and the World Map, appear only after a certain point in the
  story.
- A new game starts with a set of map flags already on.

Most of these flags are bits in the save that scripts, talks, chests and traps switch on. The menu entries work
differently: their flag numbers point into `mapjumpgroupflagrom.bin`, a list of story counter values, so they appear
once the counter reaches the listed point. The map flags a new game starts with are listed in `mapjumpgroupinit.bin`.

## How it works

### The banks

Every bank is in the save payload, the bytes from `SaveImage_GetPersistentPayloadBase` (`0x002EF2B0`,
[Save data](../Saving-Loading-And-Settings/save-data-fields.md)), one bit per id, byte `id >> 3`, bit value `1 << (id & 7)`:

| Bank | Payload offset | Ids | Setter / query | Script verbs | Holds |
|---|---|---|---|---|---|
| Primary | `+0x14F4` | 2-511 set, 0-511 read | `0x0032AB60` / the gate `0x0032A8A0` | `0x430` `setmapjumpgroupflag` (also `0x301` `setnaviicon`), `0x431` `releasemapjumpgroupflag` (also `0x302`), `0x432` `ismapjumpgroupflag` (also `0x300`) | map-jump groups and map icons |
| Bank2048 | `+0x13B4` | `0`-`2047` | `0x0032ABF0` / `0x0032A930` | `0x399` `settalknpcname`, `0x39A` `releasetalknpcname`, `0x39B` `istalknpcname` | names learned by talking |
| Bank512, first half | `+0x14B4`, bits 0-255 | `0`-`255` | `0x0032AD70` / `0x0032AA60` | `0x3F3` `settreasurebattleflag`, `0x3F4` `releasetreasurebattleflag`, `0x3F6` `istreasurebattleflag` | chests opened, traps fired |
| Bank512, second half | `+0x14B4`, bits 256-511 | `0`-`255` | `0x0032ADF0` / `0x0032AAD0` | `0x3F1` `settreasureflag`, `0x3F2` `releasetreasureflag`, `0x3F5` `istreasureflag` | scripts only |
| Bank64A | `+0x1384` | `0`-`63` | `0x0032AC70` / `0x0032A9A0` | `0x2FA` `setshutoralappear`, `0x2F9` `clearshutoralappear`, `0x2F8` `isshutoralappear` | scripts only |
| Bank64B | `+0x138C` | `0`-`63` | `0x0032ACF0` / `0x0032AA00` | `0x2FD` `setshutoralenable`, `0x2FC` `clearshutoralenable`, `0x2FB` `isshutoralenable` | scripts only |

An id outside a bank's range reads as 0 and sets nothing. The four Bank64 accessors test the range with a signed
compare only¹ and split the id with a signed divide by 8², so a negative id is not refused:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0032A9A4`, `0x0032AA04`, `0x0032AC77`, `0x0032ACF7` |
| ² | `0x0032A9B7`-`0x0032A9C9`, `0x0032AC83`-`0x0032AC9F` |

</details>

- an id that is not a multiple of 8 gives an 8-bit mask of 0 (`shl bl, cl` with a count of 25 to 31), so it reads
  as 0 and sets or clears nothing;
- an id of −8k reaches bit `0x1` of the byte k below the bank: Bank64B id −64 is bit `0x1` of `+0x1384`, which is
  Bank64A id 0.

Nothing outside the twelve accessors reads or writes these offsets from the payload base.

Payload bytes `+0xCF6`-`+0xFFF`, between the script variables ([Script variables](../Scripts-And-Script-Commands/script-variables.md),
which end at `+0xCF5`) and the quest fields at `+0x1000` ([Quests](quests.md)), are read and written by no function on their own;
nothing fixes their width. Only the payload clears¹ and the whole-image copies² cover them.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EF2E8`, `0x002EF603`, `0x002EF663` |
| ² | `0x00229B40`, `0x002EF570`, `0x00583C00`, `0x00583CB0` |

</details>

### The gate

`0x0032A8A0(id)` reads the Primary bank through an encoded id¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0032A8A0`-`0x0032A919` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | Bits `0x3FFF` are the index; bits `0x8000` and above are dropped. | `0x0032A8A8` |
| 2 | With bit `0x4000` set it answers the story schedule for that index, below. | `0x0032A8AE`-`0x0032A8BB` |
| 3 | An index of 512 or more answers 0. | `0x0032A8C0`-`0x0032A8C8` |
| 4 | Index 0 answers 1 and index 1 answers 0, without reading the bank: always and never. | `0x0032A8D0`-`0x0032A8E0` |
| 5 | Any other index answers its Primary bit. | `0x0032A8E9`-`0x0032A911` |

So `0xFFFF` asks the schedule for index `0x3FFF`, which does not exist, and answers 0. Fourteen call sites test for
`0xFFFF` first and do not call the gate:

- the map screens at `0x003BCE09`, `0x003BD5C4`, `0x003BD6B5`, `0x003BD9A1`, `0x003C070A`, `0x003C0BC2`, `0x003C0CA4`, `0x003C0F8E`,
  `0x003C103C`, `0x003C12FC`, `0x003C18E2`, `0x003C19C7` and `0x003C2504`;
- `0x00575ECF`.

They treat it differently: `0x003C0B70` answers 0 for it¹, and `0x003C06E0` answers its unlocked bit².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003C0BBD` |
| ² | `0x003C06F7` |

</details>

### The story schedule

`0x00377970(index)` answers from `mapjumpgroupflagrom.bin`¹. The record for the index is a
rising list of story counter values, the last one marked by bit `0x8000`. The answer starts false and flips at each value
the main story counter has reached, comparing as signed 16-bit numbers, so a record of two values is true from the
first value up to, but not including, the second. The counter is `FieldData_GetVariable0`², the word at
the start of the save payload: slot 0's variable block is bound to the payload base³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00377970`-`0x003779EE` |
| ² | `0x00265270` |
| ³ | `0x0026CAF8`-`0x0026CAFD` |

</details>

`0x0032A8A0` passes the id's low 14 bits as the record index¹. `0x00377970` answers false when the file is
not loaded, when the index is at or past the count, and when the record's offset is 0². It
reads values until one carries bit `0x8000` or the counter is below the next value³, so a record whose last value lacks the bit reads on into the values after it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0032A8A8` |
| ² | `0x0037797F`-`0x00377997` |
| ³ | `0x003779BC`, `0x003779C6`, `0x003779D8` |

</details>

The file is kind 9 file `0xA`, requested by `0x00378540` under the name `MJGP_ROM`; its completion `0x00378BA0` keeps the
pointer at `0x02ADD0C8`.

### Who sets and reads them

Besides the script verbs:

- **Names.** Opening a message window, `0x002E16B0`, sets the Bank2048 bit of the speaking actor's name id
 ¹. Four verbs open one: `0x461` `mes`², `0x1FF` `aask_1ff`³,
  `0x17C` `shapewin`⁴ and the developer verb `0x2043` `debug_mesask_43`⁵.
- **Name readers.** `0x00263990`, `0x002639E0` and two map-screen label readers use the Bank2048 bit to pick the second
  name of the pair ([NPC names](../Characters-And-Objects/npc-names.md)).
- **Chests.** A chest record's byte `+0x09` is its flag, `0xFF` for no flag. `setuptreasure` `0x2BE` does not place a
  chest whose flag is set⁶, and opening it, family-3 verb `0x37`, sets the flag before the
  contents are rolled⁷. A chest with `0xFF` is gated at setup by story flag 255.
- **Traps.** A trap record's byte `+0x04` is its flag. Arming skips a trap whose flag is set⁸,
  and setting it off sets the flag⁹.
- **Primary writers.** The setter `0x0032AB60` has five callers and no others: the new-game list¹⁰, the
  release and set verbs¹¹, the chocobo dismount, which clears id `0x73`¹², and the
  thunk `0x0032ABE0`. Battle orders use that thunk to set or clear ids 2-255 through the register writer `0x00329E60`,
  kind 8¹³.
- **Readers of the gate.** 58 call sites in 30 functions, plus the register reader `0x00321190`, kind 8 (`0x00321244`,
  through the thunk `0x0032A920`): the main menu, the map screens and map icons, the field's records¹⁴, the
  save screen and the Clan Primer.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E16DA`-`0x002E16EB` |
| ² | `0x00348EFF` |
| ³ | `0x0034AE98` |
| ⁴ | `0x0033FA18` |
| ⁵ | `0x0050EB67` |
| ⁶ | `0x002FAEE2`-`0x002FAEF0` |
| ⁷ | `0x002FAFEA`-`0x002FAFFD` |
| ⁸ | `0x002FA7E8`-`0x002FA7FA` |
| ⁹ | `0x002F8243`-`0x002F8253` |
| ¹⁰ | `0x00379198` |
| ¹¹ | `0x0034DDA4`, `0x0034EE37` |
| ¹² | `0x0035CE79` |
| ¹³ | `0x00329EEC`-`0x00329EF7` |
| ¹⁴ | `0x00264920` |

</details>

### Starting flags

The new-game reset `0x002EF2D0` clears the first `0x1538` bytes of the payload, which hold every bank, and jumps to
`0x00379160`¹. `0x00379160` sets each id listed in `mapjumpgroupinit.bin` with `0x0032AB60(id, 1)`²; while the list is not loaded (`0x02ADD0D0` null, `0x0037916D`-`0x00379170`) or its count is 0³ it sets nothing. `0x002EF2D0` is called by `0x00266D10`⁴ and by the save-image
reset `0x002EF650`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EF2D4`-`0x002EF2F1` |
| ² | `0x00379160`-`0x003791B5` |
| ³ | `0x0037917F`-`0x00379182` |
| ⁴ | `0x00266DC4` |
| ⁵ | `0x002EF674` |

</details>

The list is kind 9 file `0x28`, requested by `0x00378540` under the name `MJGPINIT`, kept at `0x02ADD0D0` by its
completion `0x00378B90`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003787BD` |

</details>

`mapjumpgroupinit.bin` and `eventmemorylist.bin` (kind 9 file `0x29`, requested under the name `EVTMEM`;
[Event memory](event-memory.md)) share one shape: an 8-byte magic, a `u16` count at `+0x08` and `u16` ids from
`+0x0A`. `0x00379160` reads the first that way¹ and `0x00377440` the second². `0x00378540` requests both, and its one caller `0x00377CC0`³ first clears both pointers,
`0x02ADD0D0`⁴ and `0x02ADD0A8`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00379177`, `0x0037917B` |
| ² | `0x0037744F`, `0x0037745B` |
| ³ | `0x00377D8C` |
| ⁴ | `0x00377D1C` |
| ⁵ | `0x00377D77` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `char[8]` | magic | "FLAGROM1" |
| `+0x008` | `u16` | count | 152 |
| `+0x00A` | `u16[152]` | offsets | file offset of each record |
| `+0x13A` | `u16[271]` | lists | the records: story counter values, bit `0x8000` on each record's last value |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[8]` | magic | "FLAGDEF1" |
| `+0x08` | `u16` | count | 53 |
| `+0x0A` | `u16[53]` | ids | the Primary ids a new game starts with |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

Both files are identical in all nine languages.

The main menu entries and other readers that use the schedule¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00281AE0`, `0x00283690`, `0x00283730` |

</details>

| Encoded id | Record | True from story counter | Used by |
|---|---|---:|---|
| `0x4004` | 4 | 25 | the Equip entry |
| `0x4006` | 6 | 62 | the Licenses entry and the License Board |
| `0x4007` | 7 | 62 | the Clan Primer entry |
| `0x4008` | 8 | 244 | the Party entry, and choosing the leader in the field |
| `0x4009` | 9 | 240 | the Gambits entry |
| `0x4010` | 16 | 40 | the World Map entry |
| `0x400B` | 11 | 62 | two Clan Primer screens, and the clan rank written into the save header (`0x00583F17`) |
| `0x4067` | 103 | 300 to 305 | a Party menu command |

The menu entry text is `menu_command.bin` rows 203-214. Records 0, 2 and `0x87` need the counter at 32,767, and
record 1 is true for any counter of 0 or more.

[`story-flags-schedule.tsv`](story-flags-schedule.tsv) gives all 152 records of `mapjumpgroupflagrom.bin`: the
encoded id, the record's offset, its values and the story counter values for which `0x00377970` answers true. The
records fill the file from `0x13A` to its end, 271 values, and no two share a list. 48 records have one value, 98
two, one three, three four and two six.

| Column | Meaning |
|---|---|
| `record` | the record's index, from 0 |
| `encoded_id` | the Primary id that reads it, `0x4000` + record |
| `offset` | the record's offset from the file start |
| `values` | the record's story counter values, without bit `0x8000` |
| `true_while_counter` | the counter values for which the answer is true; `32767 only` for a record whose only value is 32,767 |

The 53 starting ids of `mapjumpgroupinit.bin` are 0, `0x56`, `0x65`, `0x66`, `0x70`, `0x79`, `0x7A`, `0x80`, `0xFC`,
`0x108`, `0x10B`, `0x10C`, `0x11C`, `0x12C`-`0x134`, `0x136`, `0x137`, `0x13A`-`0x155` and `0x158`. Id 0 is outside
the setter's range, so 52 flags are set.

</details>

## Modding notes

- A Primary id read through the gate with bit `0x4000` set is a story-counter band, not a flag: setting the flag does
  nothing for it.
- Ids 0 and 1 are permanent always and never answers; the setter cannot store them.
- Editing `mapjumpgroupflagrom.bin` moves the story points at which menus and map groups open.
- A record is a rising list of counter values with bit `0x8000` on the last; leave it out and the reader goes on
  into the next record's values¹. A record at offset 0 is always false².
- `mapjumpgroupinit.bin` is read as a `u16` count at `+0x08` and that many `u16` ids³, each
  set with `0x0032AB60(id, 1)`; an id outside 2 to 511 sets nothing.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003779C6` |
| ² | `0x00377997` |
| ³ | `0x00379177`-`0x003791A4` |

</details>

## Related

- [Save data](../Saving-Loading-And-Settings/save-data-fields.md) - the payload the banks sit in.
- [Quests](quests.md) - the quest bits just before the banks.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name pairs the Bank2048 bit chooses between.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 2 calls with 2 other topics</summary>

**Enemy spawning** (explained on [enemy respawning](../Enemy-Spawning/enemy-respawning.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00229B40`](../Saving-Loading-And-Settings/save-data-fields.md) World transition snapshot: capture runtime state (on save data fields) | calls | [`0x00233440`](../Saving-Loading-And-Settings/save-data-fields.md) Spawn keep: serialize persistence banks (on save data fields) |

**Enemy AI and gambits** (explained on [glossary](../Engine-Core/glossary.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00321190`](../Enemy-AI-And-Gambits/enemy-order-sets.md) (on enemy order sets) | is called by | [`0x00301AD0`](../Enemy-AI-And-Gambits/enemy-order-sets.md) Ai order: evaluate target selector (on enemy order sets) |

</details>

---

[← Story progress](story-progress.md) | [Story counter values →](story-counter-values.md)
