---
title: "Tutorial battle commands: the tutorial_data groups that limit which commands and actions Vaan and Penelo may choose in the battle menu"
kind: "reference"
category: "Battle actions"
addresses: "0x02EBF020, 0x0032A230, 0x0032A320, 0x0032A3E0, 0x0031EB20, 0x0027E050"
---

## What it lists

`tutorial-battle-commands.tsv` holds one line for each of the 6 rows of the table that registry slot `0x02EBF020`
reaches (`battle_pack.bin` directory entry `+0x70`), and one line for the empty group 0. The rows come in groups;
a group limits the battle menu of each member it has a row for.

| Group | Rows | Member and what is left |
|---:|---|---|
| 0 | none | nothing is limited |
| 1 | 0, 1 | Vaan: nothing; Penelo: Potion |
| 2 | 2, 3 | Vaan and Penelo: the Gambits command |
| 3 | 4 | Vaan: Blind and Fire |
| 4 | 5 | Vaan: Hellfire and Pyroclasm |

### Finding the row

`0x0032A230(group, member, &row)` reads the group index at the table's `+0x1C`: a count (5), then the end row of each
group (0, 2, 4, 5, 6). Group *g* is rows end[*g* − 1] to end[*g*] − 1, with end[−1] = 0 (`0x0032A230`-`0x0032A31E`).

- A group outside 0 to count − 1, or an empty group, gives 1 and no row: nothing is limited.
- Otherwise it gives 1 and the row whose word `+0x00` is the member, or 0 when the group has no row for the member.

### Applying it

The battle menu builder `0x0031EB20` asks with the request's word `+0x04` as the group and the member's type byte
(stats `+0x04`) ([Battle menu](../Menus-And-HUD/battle-menu.md)). `0x0027E050` and `0x0027D740` fill that word from the menu's
word `+0x153A` (`0x0027E2F7`, `0x0027D82F`), which `0x002778C0` copies from `+0x2FF6` of its source (`0x00279296`), which the battle-menu widget procedure
`0x00279E20` sets (`0x0027A43C`).

- **Command rows:** `0x0032A320(group, member, flag, command)` keeps a command when there is no row, or when an
  entry of the row allows it; otherwise the row is greyed with reason `0x2B` (`0x0031ED00`-`0x0031ED1E`).
- **Action rows:** when the member's row exists, an action is kept only when it equals an entry whose mask bit is
  clear; otherwise, and when the group has no row for the member, it is greyed with reason `0x2B`
  (`0x0031F1A1`-`0x0031F1FF`).

### Which entry allows a command

`0x0032A320` walks the up to seven entries until `0xFFFF`. For entry *k* (`0x0032A380`-`0x0032A3B9`):

- with mask bit *k* set, the entry allows only the Gambits command (flag 0, command 13);
- otherwise `0x0032A3E0(flag, command, action)` decides: for flag 0, the action's kind `+0x1E` equals the command,
  or kind 1-2 allows command 18 (Magicks & Technicks) and kind 5-6 command 19 (Mist); for flag 1, the action is a
  magick (kind 1) of school `+0x2C` & 7 = the command.

The command numbers are the rows of comac_data on [Category names](category-names.md).

### Where the values come from

Each line is a row of the `st2e` table at entry `+0x70` (6 rows of 20 bytes from the section's `+0x20`) or a group
of the group index at the header's `+0x1C`; each entry is named by its action row's name word `+0x34`
([Action list](action-list.md)).

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `+0x00` | `u16` | member | `0x0032A230` | the party row the entry limits (0 Vaan, 5 Penelo) |
| `+0x02` | `u16[7]` | entries | `0x0032A320`, `0x0031EB20` | action rows, ended by `0xFFFF` |
| `+0x10` | `u32` | mask | `0x0032A320`, `0x0031EB20` | bit *k*: entry *k* stands for the Gambits command and is not compared |

The table is loaded only by `0x0032A230` and the loader `0x00236C30`. The words of a masked entry (`0x5000`,
`0x5005`) are only tested against `0xFFFF`.

### Properties of the shipped rows

- The table's header gives 6 rows of 20 bytes and the group index 5 groups ending at row 6; the TSV has a line for
  each of the 6 rows and one for group 0.
- Example rows: row 1 limits Penelo (`+0x00` = 5) to action 82, Potion; row 2 has mask 1, so
  its entry `0x5000` leaves Vaan only the Gambits command; row 0 has no entry, so in group 1 every command and action
  of Vaan is greyed.

## Columns

| Column | Meaning |
|---|---|
| `group`, `row` | the group and the row |
| `member` | `+0x00` by name |
| `ids`, `mask` | the entries other than `0xFFFF`, and `+0x10` |
| `allowed` | what the entries leave the member |
| `explanation` | a one-line summary |

## Related

- [Battle menu: the command lists, the party HP and MP list, the help line, the boss and overhead gauges, and how a chosen command is issued](../Menus-And-HUD/battle-menu.md)
- [Command availability: why a battle command is greyed out or refused, and the refusal codes](command-availability.md)
- [Category names: the battle command, magick school, element and equipment class name tables](category-names.md)
