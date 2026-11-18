[Home](../../README.md) / [Battle actions](README.md) / Tutorial battle commands

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Tutorial battle commands: the tutorial_data groups that limit which commands and actions Vaan and Penelo may choose in the battle menu | reference | Battle actions | Action tables | All 6 rows and 5 groups of the shipped tutorial_data table in battle_pack.bin: for each group, the party member a row limits and the actions or the Gambits command that member may still choose; how the battle menu builder applies a group to its command and action rows and greys out everything else with reason 0x2B. | 0x02EBF020, 0x0032A230, 0x0032A320, 0x0032A3E0, 0x0031EB20, 0x0027E050 |

## What it lists

[`tutorial-battle-commands.tsv`](tutorial-battle-commands.tsv) holds one line for each of the 6 rows of the table that registry slot `0x02EBF020`
reaches (`battle_pack.bin` directory entry `+0x70`), and one line for the empty group 0. The rows come in groups;
a group limits the battle menu of each member it has a row for.

A battle chooses its group through the script command `set_interventionmenu_tutorialmode`, whose number reaches the
battle menu as the group to apply. No script in the nine language trees calls it, so no shipped battle limits the menu
this way.

| Group | Rows | Member and what is left |
|---:|---|---|
| 0 | no row | nothing is limited |
| 1 | 0, 1 | Vaan: nothing; Penelo: Potion |
| 2 | 2, 3 | Vaan and Penelo: the Gambits command |
| 3 | 4 | Vaan: Blind and Fire |
| 4 | 5 | Vaan: Hellfire and Pyroclasm |

### Finding the row

`0x0032A230(group, member, &row)` reads the group index at the table's `+0x1C`: a count (5), then the end row of each
group (0, 2, 4, 5, 6). Group *g* is rows end[*g* − 1] to end[*g*] − 1, with end[−1] = 0 (`0x0032A230`-`0x0032A31E`).

- A group outside 0 to count − 1, or an empty group, gives 1 and no row: nothing is limited.
- Otherwise it gives 1 and the row whose word `+0x00` is the member, or 0 when the group has no row for the member.
- The row pointer is set to 0 first (`0x0032A24A`) and to each row as it is scanned (`0x0032A300`), so a 0 answer
  leaves it at the group's last row. The member is a byte, compared zero-extended with the row's word
  (`0x0032A257`, `0x0032A303`).
- The group test is `group < 0` or `group > count − 1` as an unsigned compare (`0x0032A267`-`0x0032A273`). The slot
  `0x02EBF020` is read with no null test (`0x0032A25A`): with it null the read of `+0x1C` is at address `0x1C` and
  faults.

### Applying it

The battle menu builder `0x0031EB20` asks, only for a member with a stats record whose byte `+0x05` is 0
(`0x0031ECEA`-`0x0031ECFA`, `0x0031F18D`-`0x0031F19F`), with the request's dword `+0x04` as the group and the
member's type byte (stats `+0x04`) ([Battle menu](../Menus-And-HUD/battle-menu.md)).

`0x0027E050` and `0x0027D740`
fill that dword, sign-extended, from the menu's word `+0x153A` (`0x0027E2F7`-`0x0027E305`,
`0x0027D82F`-`0x0027D836`), which `0x002778C0` copies from `+0x2FF6` of its source (`0x00279296`), which the
battle-menu widget procedure
`0x00279E20` sets (`0x0027A43C`) from `+0x61C2`, the word `+0x10` of the message that creates the widget (`0x00279E8B`).

That word is the argument of script verb `0x45C`, `set_interventionmenu_tutorialmode`. Its handler
`0x003419D0` pops the argument as an int (`0x00267E10`) and hands it by tail jump through `0x002E2490` to
`0x00290220`, which stores its low word at `+0x10FA0` of `[0x0209BE80]`, read with no null test
(`0x003419D4`-`0x003419E2`, `0x00290220`-`0x00290227`). `0x00290CF0` passes it to `0x00276650` as the fifth argument
(`0x00290D9D`-`0x00290DC0`) and then zeroes it (`0x00290DD1`). `0x00276650` puts it at `+0x10` of the creation
message (`0x00276675`-`0x002766D1`).

No script of the nine language trees calls verb `0x45C`, so no shipped battle applies groups 1 to 4.

- **Command rows:** `0x0032A320(group, member, flag, command)` keeps a command when there is no row, or when an
  entry of the row allows it; otherwise the row is greyed with reason `0x2B` (`0x0031ED00`-`0x0031ED1E`). When the
  group has no row for the member, `0x0032A230` answers 0 and `0x0032A320` returns 0 at once, so the command is
  greyed (`0x0032A337`-`0x0032A341`).
- **Action rows:** when the member's row exists, an action is kept only when it equals an entry whose mask bit is
  clear; otherwise, and when the group has no row for the member, it is greyed with reason `0x2B`
  (`0x0031F1A1`-`0x0031F1FF`). A non-zero answer of `0x0032A230` that leaves the row pointer null keeps every
  action (`0x0031F1B6`-`0x0031F1BE`).

### Which entry allows a command

`0x0032A320` walks the up to seven entries until `0xFFFF`, returns 1 at the first entry that allows the command
and 0 when no entry allows it (`0x0032A39C`, `0x0032A3BB`). For entry *k* (`0x0032A380`-`0x0032A3B9`):

- with mask bit `1 << k` set (the `bt` at `0x0032A38E`), the entry allows only the Gambits command (flag 0,
  command 13);
- otherwise `0x0032A3E0(flag, command, action)` decides. It returns 0 for an action that `0x00322C50(0x14, id, 1)`
  rejects (`0x0032A40B`-`0x0032A412`). For flag 0, the action's kind `+0x1E` equals the command,
  or kind 1-2 allows command 18 (Magicks & Technicks) and kind 5-6 command 19 (Mist); for flag 1, the action is a
  magick (kind 1) of school `+0x2C` & 7 = the command; any other flag gives 0 (`0x0032A463`, `0x0032A4A7`).

The command numbers are the rows of comac_data on [Category names](category-names.md).

### Where the values come from

Each line is a row of the `st2e` table at entry `+0x70` (6 rows of 20 bytes from the section's `+0x20`) or a group
of the group index at the header's `+0x1C`; each entry is named by its action row's name word `+0x34`
([Action list](action-list.md)).

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `+0x00` | `u16` | member | `0x0032A230` | the party row the entry limits (0 Vaan, 5 Penelo) |
| `+0x02` | `u16[7]` | entries | `0x0032A320`, `0x0031EB20` | action rows, ended by `0xFFFF` |
| `+0x10` | `u32` | mask | `0x0032A320`, `0x0031EB20` | bit `1 << k`: entry *k* stands for the Gambits command and is not compared |

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 20 calls with 7 other topics</summary>

**Damage and battle formulas** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

| Function | | Functions |
|---|---|---|
| `0x00322C50` | is called by | `0x002FEF30` |

**Items, equipment, shops and licenses**

| Function | | Functions |
|---|---|---|
| `0x00322C50` | is called by | `0x003096F0`, `0x0030B180`, `0x0030B4B0`, `0x0030B510`, `0x0030B570`, `0x0030B630`, `0x00317930`, `0x0031A510`, `0x00323910`, `0x00323C60`, `0x00323D10`, `0x00323EC0` |
| `0x00322C50` | is also called by | `0x00325F40` |

**Items, equipment, shops and licenses** (explained on [stats](../Damage-And-Battle-Formulas/stats.md), [bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md), [party data](../Party/party-data.md), [party table](../Party/party-table.md))

**Items, equipment, shops and licenses** (explained on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [quickening and esper list](quickening-and-esper-list.md), [command availability](command-availability.md))

**Movement and pathfinding** (explained on [game over](../World-Areas-And-Travel/game-over.md), [party data](../Party/party-data.md))

| Function | | Functions |
|---|---|---|
| `0x00322C50` | is called by | `0x0031BAC0`, `0x00326BB0` |

**Scripts and script commands** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

| Function | | Functions |
|---|---|---|
| `0x003419D0` | calls | `0x00267E10` |

**Status effects and KO** (explained on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00322C50` | is called by | `0x0030E130`, `0x0030FED0`, `0x00310DB0` |

</details>
