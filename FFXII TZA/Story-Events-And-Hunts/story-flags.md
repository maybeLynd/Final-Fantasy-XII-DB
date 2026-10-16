---
title: "Story flags: the five banks of yes-or-no flags the save keeps, the story schedule some flag ids read instead, who sets and reads each, and the flags a new game starts with"
kind: "system"
category: "Story, events and hunts"
addresses: "0032A8A0, 00377970, 0032AB60, 0032ABF0, 0032AD70, 0032AA60, 00379160, 002EF2D0"
---

## What the player sees

- Places on the map open up, characters' names appear once they have spoken, and opened chests stay empty: each is a
  flag in the save.
- Some menu entries, such as Equip, Licenses, Gambits and the World Map, appear only after a certain point in the
  story.
- A new game starts with a set of map flags already on.

## How it works

### The banks

Every bank is in the save payload, the bytes from `SaveImage_GetPersistentPayloadBase` (`002EF2B0`,
[Save data](../Saving-Loading-And-Settings/save-data-fields.md)), one bit per id, byte `id >> 3`, bit `id & 7`:

| Bank | Payload offset | Ids | Setter / query | Script verbs | Holds |
|---|---|---|---|---|---|
| Primary | `+14F4`<sub>h</sub> | 2-511 set, 0-511 read | `0032AB60` / the gate `0032A8A0` | `430`<sub>h</sub> `setmapjumpgroupflag` (also `301`<sub>h</sub> `setnaviicon`), `431`<sub>h</sub> `releasemapjumpgroupflag` (also `302`<sub>h</sub>), `432`<sub>h</sub> `ismapjumpgroupflag` (also `300`<sub>h</sub>) | map-jump groups and map icons |
| Bank2048 | `+13B4`<sub>h</sub> | `0`-`2047` | `0032ABF0` / `0032A930` | `399`<sub>h</sub> `settalknpcname`, `39A`<sub>h</sub> `releasetalknpcname`, `39B`<sub>h</sub> `istalknpcname` | names learned by talking |
| Bank512, first half | `+14B4`<sub>h</sub>, bits 0-255 | `0`-`255` | `0032AD70` / `0032AA60` | `3F3`<sub>h</sub> `settreasurebattleflag`, `3F4`<sub>h</sub> `releasetreasurebattleflag`, `3F6`<sub>h</sub> `istreasurebattleflag` | chests opened, traps fired |
| Bank512, second half | `+14B4`<sub>h</sub>, bits 256-511 | `0`-`255` | `0032ADF0` / `0032AAD0` | `3F1`<sub>h</sub> `settreasureflag`, `3F2`<sub>h</sub> `releasetreasureflag`, `3F5`<sub>h</sub> `istreasureflag` | scripts only |
| Bank64A | `+1384`<sub>h</sub> | `0`-`63` | `0032AC70` / `0032A9A0` | `2FA`<sub>h</sub> `setshutoralappear`, `2F9`<sub>h</sub> `clearshutoralappear`, `2F8`<sub>h</sub> `isshutoralappear` | scripts only |
| Bank64B | `+138C`<sub>h</sub> | `0`-`63` | `0032ACF0` / `0032AA00` | `2FD`<sub>h</sub> `setshutoralenable`, `2FC`<sub>h</sub> `clearshutoralenable`, `2FB`<sub>h</sub> `isshutoralenable` | scripts only |

An id outside a bank's range reads as 0 and sets nothing. The four Bank64 accessors test the range with a signed
compare only (`0032A9A4`, `0032AA04`, `0032AC77`, `0032ACF7`), so a negative id reaches the bank's bytes below it.
Nothing outside the twelve accessors reads or writes these offsets from the payload base.

### The gate

`0032A8A0(id)` reads the Primary bank through an encoded id (`0032A8A0`-`0032A919`):

1. Bits 0-13 are the index; bits 15 and above are dropped (`0032A8A8`).
2. With bit 14 set it answers the story schedule for that index, below (`0032A8AE`-`0032A8BB`).
3. An index of 512 or more answers 0 (`0032A8C0`-`0032A8C8`).
4. Index 0 answers 1 and index 1 answers 0, without reading the bank (`0032A8D0`-`0032A8DD`): always and never.
5. Any other index answers its Primary bit (`0032A8E9`-`0032A911`).

So `FFFF`<sub>h</sub> asks the schedule for index `3FFF`<sub>h</sub>, which does not exist, and answers 0. Fourteen call sites test for
`FFFF`<sub>h</sub> first and do not call the gate:

- the map screens at `003BCE09`, `003BD5C4`, `003BD6B5`, `003BD9A1`, `003C070A`, `003C0BC2`, `003C0CA4`, `003C0F8E`,
  `003C103C`, `003C12FC`, `003C18E2`, `003C19C7` and `003C2504`;
- `00575ECF`.

They treat it differently: `003C0B70` answers 0 for it (`003C0BBD`), and `003C06E0` answers its unlocked bit
(`003C06F7`).

### The story schedule

`00377970(index)` answers from `mapjumpgroupflagrom.bin` (`00377970`-`003779EE`). The record for the index is a
rising list of story counter values, the last one marked by bit 15. The answer starts false and flips at each value
the main story counter has reached, comparing as signed 16-bit numbers, so a record of two values is true from the
first value up to, but not including, the second. The counter is `FieldData_GetVariable0` (`00265270`), the word at
the start of the save payload: slot 0's variable block is bound to the payload base (`0026CAF8`-`0026CAFD`).

The file is kind 9 file `A`<sub>h</sub>, requested by `00378540` under the name `MJGP_ROM`; its completion `00378BA0` keeps the
pointer at `02ADD0C8`.

### Who sets and reads them

Besides the script verbs:

- **Names.** Opening a message window, `002E16B0`, sets the Bank2048 bit of the speaking actor's name id
  (`002E16DA`-`002E16EB`). Four verbs open one: `461`<sub>h</sub> `mes` (`00348EFF`), `1FF`<sub>h</sub> `aask_1ff` (`0034AE98`),
  `17C`<sub>h</sub> `shapewin` (`0033FA18`) and the developer verb `2043`<sub>h</sub> `debug_mesask_43` (`0050EB67`).
- **Name readers.** `00263990`, `002639E0` and two map-screen label readers use the Bank2048 bit to pick the second
  name of the pair ([NPC names](../Characters-And-Objects/npc-names.md)).
- **Chests.** A chest record's byte `+09`<sub>h</sub> is its flag, `FF`<sub>h</sub> for none. `setuptreasure` `2BE`<sub>h</sub> does not place a
  chest whose flag is set (`002FAEE2`-`002FAEF0`), and opening it, family-3 verb `37`<sub>h</sub>, sets the flag before the
  contents are rolled (`002FAFEA`-`002FAFFD`). A chest with `FF`<sub>h</sub> is gated at setup by bit 255.
- **Traps.** A trap record's byte `+04`<sub>h</sub> is its flag. Arming skips a trap whose flag is set (`002FA7E8`-`002FA7FA`),
  and setting it off sets the flag (`002F8243`-`002F8253`).
- **Primary writers.** The setter `0032AB60` has five callers and no others: the new-game list (`00379198`), the
  release and set verbs (`0034DDA4`, `0034EE37`), the chocobo dismount, which clears id `73`<sub>h</sub> (`0035CE79`), and the
  thunk `0032ABE0`. Battle orders use that thunk to set or clear ids 0-255 through the register writer `00329E60`,
  kind 8 (`00329EEC`-`00329EF7`). The AI operand resolver reads them through the gate, kind 8 (`00321244`).
- **Readers of the gate.** 58 call sites in 30 functions, plus the AI resolver: the main menu, the map screens and map
  icons, the field's records (`00264920`), the save screen and the Clan Primer.

### Starting flags

The new-game reset `002EF2D0` clears the first `1538`<sub>h</sub> bytes of the payload, which hold every bank, and jumps to
`00379160` (`002EF2D4`-`002EF2F1`). `00379160` sets each id listed in `mapjumpgroupinit.bin` with `0032AB60(id, 1)`
(`00379160`-`003791B5`). `002EF2D0` is called by `00266D10` (`00266DC4`) and by the save-image reset `002EF650`
(`002EF674`). The list is kind 9 file `28`<sub>h</sub>, requested by `00378540` under the name `MJGPINIT`, kept at `02ADD0D0`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `char[8]` | magic | "FLAGROM1" |
| `008`<sub>h</sub> | `u16` | count | 152 |
| `00A`<sub>h</sub> | `u16[152]` | offsets | file offset of each record |
| `13A`<sub>h</sub> | `u16[271]` | lists | the records: story counter values, bit 15 on each record's last value |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[8]` | magic | "FLAGDEF1" |
| `08`<sub>h</sub> | `u16` | count | 53 |
| `0A`<sub>h</sub> | `u16[53]` | ids | the Primary ids a new game starts with |

## Shipped data

Both files are identical in all nine languages.

The main menu entries and other readers that use the schedule (`00281AE0`, `00283690`, `00283730`):

| Encoded id | Record | True from story counter | Used by |
|---|---|---:|---|
| `4004`<sub>h</sub> | 4 | 25 | the Equip entry |
| `4006`<sub>h</sub> | 6 | 62 | the Licenses entry and the License Board |
| `4007`<sub>h</sub> | 7 | 62 | the Clan Primer entry |
| `4008`<sub>h</sub> | 8 | 244 | the Party entry, and choosing the leader in the field |
| `4009`<sub>h</sub> | 9 | 240 | the Gambits entry |
| `4010`<sub>h</sub> | 16 | 40 | the World Map entry |
| `400B`<sub>h</sub> | 11 | 62 | two Clan Primer screens, and the clan rank written into the save header (`00583F17`) |
| `4067`<sub>h</sub> | 103 | 300 to 305 | a Party menu command |

The menu entry text is `menu_command.bin` rows 203-214. Records 0, 2 and `87`<sub>h</sub> need the counter at 32,767, and
record 1 is true for any counter of 0 or more.

The 53 starting ids of `mapjumpgroupinit.bin` are 0, `56`<sub>h</sub>, `65`<sub>h</sub>, `66`<sub>h</sub>, `70`<sub>h</sub>, `79`<sub>h</sub>, `7A`<sub>h</sub>, `80`<sub>h</sub>, `FC`<sub>h</sub>,
`108`<sub>h</sub>, `10B`<sub>h</sub>, `10C`<sub>h</sub>, `11C`<sub>h</sub>, `12C`<sub>h</sub>-`134`<sub>h</sub>, `136`<sub>h</sub>, `137`<sub>h</sub>, `13A`<sub>h</sub>-`155`<sub>h</sub> and `158`<sub>h</sub>. Id 0 is outside
the setter's range, so 52 flags are set.

## Modding notes

- A Primary id read through the gate with bit 14 set is a story-counter band, not a flag: setting the flag does
  nothing for it.
- Ids 0 and 1 are permanent always and never answers; the setter cannot store them.
- Editing `mapjumpgroupflagrom.bin` moves the story points at which menus and map groups open.

## Related

- [Save data](../Saving-Loading-And-Settings/save-data-fields.md) - the payload the banks sit in.
- [Quests](quests.md) - the quest bits just before the banks.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name pairs the Bank2048 bit chooses between.
