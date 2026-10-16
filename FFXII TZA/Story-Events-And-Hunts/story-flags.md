---
title: "Story flags: the five banks of yes-or-no flags the save keeps, the story schedule some flag ids read instead, who sets and reads each, and the flags a new game starts with"
kind: "system"
category: "Story, events and hunts"
summary: "How the game remembers what has happened: the five flag banks in the save payload with their offsets and id ranges, the accessors and their bounds, the encoded id whose bit 14 reads the story schedule in mapjumpgroupflagrom.bin instead of a flag, ids 0 and 1 as always and never, what each bank holds (map-jump groups and map icons, names learned by talking, chests opened and traps fired, two script-only banks), every native setter and reader, the main menu items the schedule unlocks, and the reset that clears the banks and sets the 52 starting flags."
addresses: ["0032A8A0", "00377970", "0032AB60", "0032ABF0", "0032AD70", "0032AA60", "00379160", "002EF2D0"]
---

# Story flags: the five banks of yes-or-no flags the save keeps, the story schedule some flag ids read instead, who sets and reads each, and the flags a new game starts with

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
| Primary | `+0x14F4` | 2-511 set, 0-511 read | `0032AB60` / the gate `0032A8A0` | `0x430` `setmapjumpgroupflag` (also `0x301` `setnaviicon`), `0x431` `releasemapjumpgroupflag` (also `0x302`), `0x432` `ismapjumpgroupflag` (also `0x300`) | map-jump groups and map icons |
| Bank2048 | `+0x13B4` | 0-2047 | `0032ABF0` / `0032A930` | `0x399` `settalknpcname`, `0x39A` `releasetalknpcname`, `0x39B` `istalknpcname` | names learned by talking |
| Bank512, first half | `+0x14B4`, bits 0-255 | 0-255 | `0032AD70` / `0032AA60` | `0x3F3` `settreasurebattleflag`, `0x3F4` `releasetreasurebattleflag`, `0x3F6` `istreasurebattleflag` | chests opened, traps fired |
| Bank512, second half | `+0x14B4`, bits 256-511 | 0-255 | `0032ADF0` / `0032AAD0` | `0x3F1` `settreasureflag`, `0x3F2` `releasetreasureflag`, `0x3F5` `istreasureflag` | scripts only |
| Bank64A | `+0x1384` | 0-63 | `0032AC70` / `0032A9A0` | `0x2FA` `setshutoralappear`, `0x2F9` `clearshutoralappear`, `0x2F8` `isshutoralappear` | scripts only |
| Bank64B | `+0x138C` | 0-63 | `0032ACF0` / `0032AA00` | `0x2FD` `setshutoralenable`, `0x2FC` `clearshutoralenable`, `0x2FB` `isshutoralenable` | scripts only |

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

So `0xFFFF` asks the schedule for index `0x3FFF`, which does not exist, and answers 0. Fourteen call sites test for
`0xFFFF` first and do not call the gate:

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

The file is kind 9 file `0xA`, requested by `00378540` under the name `MJGP_ROM`; its completion `00378BA0` keeps the
pointer at `02ADD0C8`.

### Who sets and reads them

Besides the script verbs:

- **Names.** Opening a message window, `002E16B0`, sets the Bank2048 bit of the speaking actor's name id
  (`002E16DA`-`002E16EB`). Four verbs open one: `0x461` `mes` (`00348EFF`), `0x1FF` `aask_1ff` (`0034AE98`),
  `0x17C` `shapewin` (`0033FA18`) and the developer verb `0x2043` `debug_mesask_43` (`0050EB67`).
- **Name readers.** `00263990`, `002639E0` and two map-screen label readers use the Bank2048 bit to pick the second
  name of the pair ([NPC names](../Characters-And-Objects/npc-names.md)).
- **Chests.** A chest record's byte `+0x09` is its flag, `0xFF` for none. `setuptreasure` `0x2BE` does not place a
  chest whose flag is set (`002FAEE2`-`002FAEF0`), and opening it, family-3 verb `0x37`, sets the flag before the
  contents are rolled (`002FAFEA`-`002FAFFD`). A chest with `0xFF` is gated at setup by bit 255.
- **Traps.** A trap record's byte `+0x04` is its flag. Arming skips a trap whose flag is set (`002FA7E8`-`002FA7FA`),
  and setting it off sets the flag (`002F8243`-`002F8253`).
- **Primary writers.** The setter `0032AB60` has five callers and no others: the new-game list (`00379198`), the
  release and set verbs (`0034DDA4`, `0034EE37`), the chocobo dismount, which clears id `0x73` (`0035CE79`), and the
  thunk `0032ABE0`. Battle orders use that thunk to set or clear ids 0-255 through the register writer `00329E60`,
  kind 8 (`00329EEC`-`00329EF7`). The AI operand resolver reads them through the gate, kind 8 (`00321244`).
- **Readers of the gate.** 58 call sites in 30 functions, plus the AI resolver: the main menu, the map screens and map
  icons, the field's records (`00264920`), the save screen and the Clan Primer.

### Starting flags

The new-game reset `002EF2D0` clears the first `0x1538` bytes of the payload, which hold every bank, and jumps to
`00379160` (`002EF2D4`-`002EF2F1`). `00379160` sets each id listed in `mapjumpgroupinit.bin` with `0032AB60(id, 1)`
(`00379160`-`003791B5`). `002EF2D0` is called by `00266D10` (`00266DC4`) and by the save-image reset `002EF650`
(`002EF674`). The list is kind 9 file `0x28`, requested by `00378540` under the name `MJGPINIT`, kept at `02ADD0D0`.

## Layouts

```struct FlagRom base=file size=0x358
+0x000  char[8]   magic    "FLAGROM1"
+0x008  u16       count    152
+0x00A  u16[152]  offsets  file offset of each record
+0x13A  u16[271]  lists    the records: story counter values, bit 15 on each record's last value
```

```struct FlagDef base=file size=0x74
+0x00  char[8]  magic  "FLAGDEF1"
+0x08  u16      count  53
+0x0A  u16[53]  ids    the Primary ids a new game starts with
```

## Shipped data

Both files are identical in all nine languages.

The main menu entries and other readers that use the schedule (`00281AE0`, `00283690`, `00283730`):

| Encoded id | Record | True from story counter | Used by |
|---|---|---:|---|
| `0x4004` | 4 | 25 | the Equip entry |
| `0x4006` | 6 | 62 | the Licenses entry and the License Board |
| `0x4007` | 7 | 62 | the Clan Primer entry |
| `0x4008` | 8 | 244 | the Party entry, and choosing the leader in the field |
| `0x4009` | 9 | 240 | the Gambits entry |
| `0x4010` | 16 | 40 | the World Map entry |
| `0x400B` | 11 | 62 | two Clan Primer screens, and the clan rank written into the save header (`00583F17`) |
| `0x4067` | 103 | 300 to 305 | a Party menu command |

The menu entry text is `menu_command.bin` rows 203-214. Records 0, 2 and `0x87` need the counter at 32,767, and
record 1 is true for any counter of 0 or more.

The 53 starting ids of `mapjumpgroupinit.bin` are 0, `0x56`, `0x65`, `0x66`, `0x70`, `0x79`, `0x7A`, `0x80`, `0xFC`,
`0x108`, `0x10B`, `0x10C`, `0x11C`, `0x12C`-`0x134`, `0x136`, `0x137`, `0x13A`-`0x155` and `0x158`. Id 0 is outside
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
