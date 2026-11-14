---
title: "Concurrence list: which Concurrence a Quickening chain ends in, by how many Quickenings of each level it used"
kind: "reference"
category: "Battle actions"
addresses: "0x02EBF0A0, 0x002F8D60, 0x0030DB70, 0x00313120, 0x022C2192"
---

## What it lists

[`concurrence-list.tsv`](concurrence-list.tsv) holds one line for each of the 16 rows of the table that registry slot `0x02EBF0A0` reaches
(`battle_pack.bin` directory entry `+0x80`). Each row names a Concurrence, action rows 226-241, and three
thresholds. The chain ends in the Concurrence of the last row whose three thresholds the chain's counts all reach.

The rows in the order they are tried, last row first:

| Row | Concurrence | Action row | First level | Second level | Third level |
|---:|---|---:|---:|---:|---:|
| 15-7 | Black Hole | 241 | 4 | 4 | 4 |
| 6 | Luminescence | 231 | 3 | 3 | 3 |
| 5 | Ark Blast | 234 | 2 | 2 | 2 |
| 4 | Whiteout | 237 | 0 | 0 | 4 |
| 3 | Windburst | 229 | 0 | 4 | 0 |
| 2 | Torrent | 228 | 2 | 2 | 0 |
| 1 | Cataclysm | 227 | 6 | 0 | 0 |
| 0 | Inferno | 226 | 3 | 0 | 0 |

Rows 7-15 are all Black Hole with 4, 4 and 4, so row 15 is the one that matches and rows 7-14 are never chosen.
Eight Concurrences appear in the table; the other eight action rows in 226-241 (230, 232, 233, 235, 236 and
238-240) are named `NOT USED` on [Action list](action-list.md).

### The counters

`0x00313120`, a step of the Quickening chain (`0x022C2170` = 2, `0x022C2174` = 4), looks for the action in the
user's party row `+0x04`-`+0x06` (`0x0031335E`, [Party table](../Party/party-table.md)) and adds one to the
byte `0x022C2192` + the slot that holds it, or to the byte `0x022C2195` when no slot holds it, unless that byte
is `0xFF` (`0x0031339D`-`0x003133A9`). It counts only for a main character: the user has a stats record whose
byte `+0x05` is 0 and whose type `+0x04` is at most 6 (`0x0031334B`-`0x0031335C`).

The three bytes `0x022C2192`-`0x022C2194` count the Quickenings used
from each slot, that is of each level, since a member learns the slots in order with the Quickening
licences. The choice below is given `0x022C2192` and reads three bytes from it (`0x002F8E00`-`0x002F8E17`), and
the clear of the counters stores a word at `0x022C2192` and a byte at `0x022C2194` (`0x0030D731`, `0x0030D738`),
so the byte `0x022C2195` takes no part in the choice and is left as it is by that clear.

Before the counters `0x00313120` does the rest of the step. It answers -1 when `0x0031B7E0` gives no unit,
or when `0x022C2170` is not 2 or `0x022C2174` is not 4 (`0x00313126`-`0x0031314C`). It then copies the `0x208`
bytes at the unit's `+0x778` to `0x022C22B8` and takes the action id from the unit's word `+0x758`
(`0x00313153`-`0x003131C7`). With `[0x02EBF138]` null, or a null answer of `0x0020E600` for its dword `+0x0C`,
it answers -1, the copy already made (`0x003131CA`-`0x003131EA`).

The action row is the low 32 bits of that answer plus the word `+0x08` of `[0x02EBF138]` times the id; a
sum of 0 answers -1 (`0x003131F0`-`0x00313215`). The unit's word `+0x758` becomes `0xFFFF` (`0x00313257`),
`0x00316CF0` is called with the address unit + `0x778`, and `0x00316CD0` is called with it and each of the first
n pointers at `0x022C21B8`, where n is `[0x022C21B4]` for an id of `0xE2` to `0xF1` and 1 for any other
(`0x00313220`-`0x00313297`).

Then come `0x00303830(unit, row, unit + 0x778)` and `0x00305640(unit, row, 1)` (`0x003132A6`, `0x003132B7`),
and the unit's dword `+0x690` is set to 0. When its byte `+0x694` is not `0xFF` and its byte `+0x695`
is `0xFF`, `+0x695` takes the value of `+0x694` and `+0x694` becomes `0xFF` (`0x003132C3`-`0x003132E3`).
The answer of `0x003098D0(unit, row)` is handed to `0x003299B0(unit, answer, 0)`, and `0x0030EC00(unit, id)`
follows (`0x003132F0`-`0x00313308`).

The charge byte is `0x022C2198` + 4 x the byte `+0x04` of the unit's record `+0x698`, read with no null
test (`0x0031330D`-`0x00313318`). While it is below 3, compared unsigned, the low byte of the answer of
`0x00308FF0(unit, id)` is added to it (`0x00313320`-`0x00313333`). The id is stored in the word `0x022C2190`
(`0x0031333D`). After the counters `0x022C2180` goes up by one, `0x022C2170` becomes 4, `0x022C2174` 3 and
`0x022C217C` 0, and the answer is 0 (`0x003133AC`-`0x003133D8`).

The slot search compares the id, as a word, with each of the three row bytes `+0x04` to `+0x06`,
zero-extended; with a null row pointer at the unit's `+0xE60` it compares with `0xFFFF` instead. When
no byte matches, the index left is 3 and the byte raised is `0x022C2195` (`0x0031335E`-`0x003133A9`). The
search runs only when the unit's record `+0x698` is not null, its byte `+0x05` is 0 and its byte
`+0x04` is 6 or less (`0x00313344`-`0x0031335C`).

### The choice

`0x0030DB70(entry, f)` is called from `0x002D5EB0` twice (`0x002D630D`, `0x002D6543`). At `0x002D6543` the entry is null
(`xor ecx, ecx`), and the call reads the last action `0x022C2190`. Unless it is already a Concurrence,
`0xE2`-`0xF1`, it asks `0x002F8D60(0x022C2192)` (`0x0030DC55`):

1. `0x002F8D60` walks the rows from the last to the first (`0x002F8D60`-`0x002F8E49`).
2. A row matches when each of the three counts is at least the row's byte `+0x01`, `+0x02` and `+0x03`.
3. The first match returns its byte `+0x00`, the Concurrence's action row; no match returns -1.

An action row that `0x00322C50(0x14, row, 0)` accepts and that is not `0xFFFF` is stored as row − `0xD0` at
`0x022C2178`; any other answer, and a last action that is already a Concurrence, stores -1 there
(`0x0030DC5A`-`0x0030DC83`, `0x0030DC98`). The call also stores `f` at `0x022C2184` (`0x0030DC8B`) and returns 0. While
`0x01EEBAF0` is not negative, `0x002F8D60` returns the word it selects from `0x022BE930` instead
([Debug menu](../Engine-Core/debug-menu.md)).

At `0x002D630D` the entry is the pointer at `+0x2D0 + i * 0x158` of the object `0x002D5EB0` works on, which
`0x002D62FB` reads before the call, and `f` is that object's `+0x740` (`0x002D62EC`-`0x002D6305`). The entry's
dword `+0` is a unit id and its word `+4` an action id:

- a unit id that `0x0031B7E0` does not resolve returns 1 (`0x0030DB97`);
- action ids `0xF2`, `0xF3` and `0xF4` hand 1, 2 or 3 times the unit's max MP (stats `+0x28`) to
  `0x00300BC0(stats, amount, 0x10)`, which adds it to the stats `+0x06` pool (`0x00300C10`-`0x00300C6A`), and return 1
  (`0x0030DBA5`-`0x0030DC24`);
- any other action that `0x002FFCF0(id, unit)` refuses returns 1 (`0x0030DBBE`-`0x0030DBC5`);
- an available one stores the unit id at `0x022C218C`, id − `0xD0` (-1 for `0xFFFF`) at `0x022C2178` and `f` at
  `0x022C2184`, and returns 0 (`0x0030DBC7`-`0x0030DBF3`, `0x0030DC8B`-`0x0030DC98`).

### Where the values come from

Each line is a row of the `st2e` table at entry `+0x80` (16 rows of 13 bytes from the section's `+0x20`), with
byte `+0x00` named by its action row's name word `+0x34` ([Action list](action-list.md)).

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `+0x00` | `u8` | concurrence | `0x002F8D60` | the action row returned |
| `+0x01` | `u8[3]` | thresholds | `0x002F8D60` | the counts of first-, second- and third-level Quickenings needed |
| `+0x04` | `u8[9]` | | no instruction | `0xFF` on every row |

The table is loaded only by `0x002F8D60` and the loader `0x00236C30`; `0x002F8D60` reads bytes
`+0x00`-`+0x03`, so `+0x04`-`+0x0C` have no reader.

### Properties of the shipped rows

- The table's header gives 16 rows of 13 bytes, one TSV line each.
- On every row byte `+0x00` is a Concurrence row, `0xE2`-`0xF1`, and `+0x04`-`+0x0C` are `0xFF`.
- Example rows: row 0, Inferno, action 226, needs 3 first-level Quickenings and nothing else, and
  is tried last; row 15, Black Hole, action 241, needs 4 of each and is tried first.

## Columns

| Column | Meaning |
|---|---|
| `row` | the row |
| `action_row`, `concurrence` | `+0x00` and its shipped name |
| `level1`, `level2`, `level3` | `+0x01`-`+0x03` |
| `bytes_04_0C` | the nine unread bytes |
| `shadowed_by` | later rows whose thresholds are all at most this row's, so they match first |
| `explanation` | a one-line summary |

## Related

- [Quickenings and summons: the one-at-a-time scene for summons, Esper attacks, Quickenings and chocobo mounting](quickenings-and-summons.md)
- [Party table: every party member, guest, Esper and the Chocobo with their starting stats, equipment, gambits, Quickenings, first-join items and model](../Party/party-table.md)
- [Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts](action-list.md)

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x0031B7E0` calls `0x00263E30`, `0x003588B0`; `0x00322C50` is called by `0x002367A0`, `0x0023A570`, `0x0031B810`,
  `0x003266C0`, `0x00329CC0`.
- Actor entity: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md),
  [party control modes](../Engine-Core/party-control-modes.md),
  [force fight mode](../Engine-Core/force-fight-mode.md); and on [party data](../Party/party-data.md).
- Items equipment shops license: `0x00322C50` is called by `0x003096F0`, `0x0030B180`, `0x0030B4B0`, `0x0030B510`, `0x0030B570`,
  `0x0030B630`, `0x00317930`, `0x0031A510`, `0x00323910`, `0x00323C60`, `0x00323D10`, `0x00323EC0`; `0x00322C50` is also called by
  `0x00325F40`.
- Items equipment shops license: those functions are documented on [stats](../Damage-And-Battle-Formulas/stats.md),
  [bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md),
  [item and ability ids](../Engine-Core/item-and-ability-ids.md), [party data](../Party/party-data.md),
  [party table](../Party/party-table.md).
- Items equipment shops license: and on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [quickening and esper list](quickening-and-esper-list.md), [command availability](command-availability.md).
- Movement: `0x0031B7E0` is called by `0x00312730`, `0x00336710`, `0x00337A50`, `0x00338140`; `0x00322C50` is called by
  `0x0031BAC0`, `0x00326BB0`.
- Movement: those functions are documented on
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md),
  [game over](../World-Areas-And-Travel/game-over.md); and on [party data](../Party/party-data.md).
- Status periodic terminal: `0x00322C50` is called by `0x0030E130`, `0x0030FED0`, `0x00310DB0`; those functions are documented
  on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Platform online achievements: `0x00305640` calls `0x00316440`; those functions are documented on
  [item use](../Items-Equipment-Shops-And-Licenses/item-use.md).
- Rewards progression economy: `0x00305640` calls `0x00253690`, `0x00254EE0`; those functions are documented on
  [item and ability ids](../Engine-Core/item-and-ability-ids.md),
  [debug menu](../Engine-Core/debug-menu.md).
