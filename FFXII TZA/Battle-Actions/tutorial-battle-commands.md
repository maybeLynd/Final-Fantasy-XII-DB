---
title: "Tutorial battle commands: the tutorial_data groups that limit which commands and actions Vaan and Penelo may choose in the battle menu"
kind: "reference"
category: "Battle actions"
addresses: "02EBF020, 0032A230, 0032A320, 0032A3E0, 0031EB20, 0027E050"
---

## What it lists

`tutorial-battle-commands.tsv` holds one line for each of the 6 rows of the table that registry slot `02EBF020`
reaches (`battle_pack.bin` directory entry `+70`<sub>h</sub>), and one line for the empty group 0. The rows come in groups;
a group limits the battle menu of each member it has a row for.

| Group | Rows | Member and what is left |
|---:|---|---|
| 0 | none | nothing is limited |
| 1 | 0, 1 | Vaan: nothing; Penelo: Potion |
| 2 | 2, 3 | Vaan and Penelo: the Gambits command |
| 3 | 4 | Vaan: Blind and Fire |
| 4 | 5 | Vaan: Hellfire and Pyroclasm |

### Finding the row

`0032A230(group, member, &row)` reads the group index at the table's `+1C`<sub>h</sub>: a count (5), then the end row of each
group (0, 2, 4, 5, 6). Group *g* is rows end[*g* − 1] to end[*g*] − 1, with end[−1] = 0 (`0032A230`-`0032A31E`).

- A group outside 0 to count − 1, or an empty group, gives 1 and no row: nothing is limited.
- Otherwise it gives 1 and the row whose word `+00`<sub>h</sub> is the member, or 0 when the group has no row for the member.

### Applying it

The battle menu builder `0031EB20` asks with the request's word `+04`<sub>h</sub> as the group and the member's type byte
(stats `+04`<sub>h</sub>) ([Battle menu](../Menus-And-HUD/battle-menu.md)). `0027E050` and `0027D740` fill that word from the menu's
word `+153A`<sub>h</sub> (`0027E2F7`, `0027D82F`), which `002778C0` copies from `+2FF6`<sub>h</sub> of its source (`00279296`), which the battle-menu widget procedure
`00279E20` sets (`0027A43C`).

- **Command rows:** `0032A320(group, member, flag, command)` keeps a command when there is no row, or when an
  entry of the row allows it; otherwise the row is greyed with reason `2B`<sub>h</sub> (`0031ED00`-`0031ED1E`).
- **Action rows:** when the member's row exists, an action is kept only when it equals an entry whose mask bit is
  clear; otherwise, and when the group has no row for the member, it is greyed with reason `2B`<sub>h</sub>
  (`0031F1A1`-`0031F1FF`).

### Which entry allows a command

`0032A320` walks the up to seven entries until `FFFF`<sub>h</sub>. For entry *k* (`0032A380`-`0032A3B9`):

- with mask bit *k* set, the entry allows only the Gambits command (flag 0, command 13);
- otherwise `0032A3E0(flag, command, action)` decides: for flag 0, the action's kind `+1E`<sub>h</sub> equals the command,
  or kind 1-2 allows command 18 (Magicks & Technicks) and kind 5-6 command 19 (Mist); for flag 1, the action is a
  magick (kind 1) of school `+2C`<sub>h</sub> & 7 = the command.

The command numbers are the rows of comac_data on [Category names](category-names.md).

### How it is built

`Database/Tools/catalogues/small_tables.py` reads the `st2e` table at entry `+70`<sub>h</sub> (6 rows of 20 bytes from the
section's `+20`<sub>h</sub>) and the group index at the header's `+1C`<sub>h</sub>, and names each entry by its action row's name
word `+34`<sub>h</sub> ([Action list](action-list.md)).

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `00`<sub>h</sub> | `u16` | member | `0032A230` | the party row the entry limits (0 Vaan, 5 Penelo) |
| `02`<sub>h</sub> | `u16[7]` | entries | `0032A320`, `0031EB20` | action rows, ended by `FFFF`<sub>h</sub> |
| `10`<sub>h</sub> | `u32` | mask | `0032A320`, `0031EB20` | bit *k*: entry *k* stands for the Gambits command and is not compared |

The table is loaded only by `0032A230` and the loader `00236C30`. The words of a masked entry (`5000`<sub>h</sub>,
`5005`<sub>h</sub>) are only tested against `FFFF`<sub>h</sub>.

### Checks

- The table's header gives 6 rows of 20 bytes, the group index 5 groups ending at row 6, and the TSV has 7 data
  lines (the 6 rows and group 0).
- Two runs over the same file give byte-identical output.
- Rows compared with their readers: row 1 limits Penelo (`+00`<sub>h</sub> = 5) to action 82, Potion; row 2 has mask 1, so
  its entry `5000`<sub>h</sub> leaves Vaan only the Gambits command; row 0 has no entry, so in group 1 every command and action
  of Vaan is greyed.

## Columns

| Column | Meaning |
|---|---|
| `group`, `row` | the group and the row |
| `member` | `+00`<sub>h</sub> by name |
| `ids`, `mask` | the entries other than `FFFF`<sub>h</sub>, and `+10`<sub>h</sub> |
| `allowed` | what the entries leave the member |
| `explanation` | a one-line summary |

## Related

- [Battle menu: the command lists, the party HP and MP list, the help line, the boss and overhead gauges, and how a chosen command is issued](../Menus-And-HUD/battle-menu.md)
- [Command availability: why a battle command is greyed out or refused, and the refusal codes](command-availability.md)
- [Category names: the battle command, magick school, element and equipment class name tables](category-names.md)
