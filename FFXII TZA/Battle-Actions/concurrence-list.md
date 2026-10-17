---
title: "Concurrence list: which Concurrence a Quickening chain ends in, by how many Quickenings of each level it used"
kind: "reference"
category: "Battle actions"
addresses: "02EBF0A0, 002F8D60, 0030DB70, 00313120, 022C2192"
---

## What it lists

`concurrence-list.tsv` holds one line for each of the 16 rows of the table that registry slot `02EBF0A0` reaches
(`battle_pack.bin` directory entry `+80`<sub>h</sub>). Each row names a Concurrence, action rows 226-241, and three
thresholds. The chain ends in the Concurrence of the last row whose three thresholds the chain's counts all reach.

| Tried | Concurrence | First level | Second level | Third level |
|---:|---|---:|---:|---:|
| 1 | Black Hole | 4 | 4 | 4 |
| 2 | Luminescence | 3 | 3 | 3 |
| 3 | Ark Blast | 2 | 2 | 2 |
| 4 | Whiteout | 0 | 0 | 4 |
| 5 | Windburst | 0 | 4 | 0 |
| 6 | Torrent | 2 | 2 | 0 |
| 7 | Cataclysm | 6 | 0 | 0 |
| 8 | Inferno | 3 | 0 | 0 |

Rows 7-15 are all Black Hole with 4, 4 and 4, so row 15 is the one that matches and rows 7-14 are never chosen.

### The counters

`00313120`, a step of the Quickening chain (`022C2170` = 2, `022C2174` = 4), finds the slot that holds the action in the user's party
row `+04`<sub>h</sub>-`+06`<sub>h</sub> (`0031335E`, [Party table](../Party/party-table.md)) and adds one to the byte
`022C2192` + slot, unless that byte is `FF`<sub>h</sub>; it counts only for a main character (type below 7). The three bytes count the Quickenings used from each slot, that is of
each level, since a member learns the slots in order with the Quickening licences.

### The choice

`0030DB70(0, …)`, called from `002D5EB0` (`002D630D`, `002D6543`), reads the last action `022C2190`. Unless it is already a Concurrence,
`E2`<sub>h</sub>-`F1`<sub>h</sub>, it asks `002F8D60(022C2192)` (`0030DC55`):

1. `002F8D60` walks the rows from the last to the first (`002F8D60`-`002F8E49`).
2. A row matches when each of the three counts is at least the row's byte `+01`<sub>h</sub>, `+02`<sub>h</sub> and `+03`<sub>h</sub>.
3. The first match returns its byte `+00`<sub>h</sub>, the Concurrence's action row; no match returns -1.

A valid action row is stored as row − `D0`<sub>h</sub> at `022C2178`; -1 leaves `022C2178` at -1. While `01EEBAF0` is not
negative, `002F8D60` returns the word it selects from `022BE930` instead ([Debug menu](../Engine-Core/debug-menu.md)).

### How it is built

`Database/Tools/catalogues/small_tables.py` reads the `st2e` table at entry `+80`<sub>h</sub> (16 rows of 13 bytes from the
section's `+20`<sub>h</sub>) and names byte `+00`<sub>h</sub> by its action row's name word `+34`<sub>h</sub> ([Action list](action-list.md)).

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `00`<sub>h</sub> | `u8` | concurrence | `002F8D60` | the action row returned |
| `01`<sub>h</sub> | `u8[3]` | thresholds | `002F8D60` | the counts of first-, second- and third-level Quickenings needed |
| `04`<sub>h</sub> | `u8[9]` | | none | `FF`<sub>h</sub> on every row |

The table is loaded only by `002F8D60` and the loader `00236C30`, both decompiled; `002F8D60` reads bytes
`+00`<sub>h</sub>-`+03`<sub>h</sub>, so `+04`<sub>h</sub>-`+0C`<sub>h</sub> have no reader.

### Checks

- The table's header gives 16 rows of 13 bytes, and the TSV has 16 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts that byte `+00`<sub>h</sub> is a Concurrence row, `E2`<sub>h</sub>-`F1`<sub>h</sub>, and that `+04`<sub>h</sub>-`+0C`<sub>h</sub> are `FF`<sub>h</sub>.
- Rows compared with their reader: row 0, Inferno, action 226, needs 3 first-level Quickenings and nothing else, and
  is tried last; row 15, Black Hole, action 241, needs 4 of each and is tried first.

## Columns

| Column | Meaning |
|---|---|
| `row` | the row |
| `action_row`, `concurrence` | `+00`<sub>h</sub> and its shipped name |
| `level1`, `level2`, `level3` | `+01`<sub>h</sub>-`+03`<sub>h</sub> |
| `bytes_04_0C` | the nine unread bytes |
| `shadowed_by` | later rows whose thresholds are all at most this row's, so they match first |
| `explanation` | a one-line summary |

## Related

- [Quickenings and summons: the one-at-a-time scene for summons, Esper attacks, Quickenings and chocobo mounting](quickenings-and-summons.md)
- [Party table: every party member, guest, Esper and the Chocobo with their starting stats, equipment, gambits, Quickenings, first-join items and model](../Party/party-table.md)
- [Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts](action-list.md)
