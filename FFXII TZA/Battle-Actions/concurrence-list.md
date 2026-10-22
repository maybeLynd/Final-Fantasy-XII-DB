---
title: "Concurrence list: which Concurrence a Quickening chain ends in, by how many Quickenings of each level it used"
kind: "reference"
category: "Battle actions"
addresses: "0x02EBF0A0, 0x002F8D60, 0x0030DB70, 0x00313120, 0x022C2192"
---

## What it lists

`concurrence-list.tsv` holds one line for each of the 16 rows of the table that registry slot `0x02EBF0A0` reaches
(`battle_pack.bin` directory entry `+0x80`). Each row names a Concurrence, action rows 226-241, and three
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

`0x00313120`, a step of the Quickening chain (`0x022C2170` = 2, `0x022C2174` = 4), finds the slot that holds the action in the user's party
row `+0x04`-`+0x06` (`0x0031335E`, [Party table](../Party/party-table.md)) and adds one to the byte
`0x022C2192` + slot, unless that byte is `0xFF`; it counts only for a main character (type below 7). The three bytes count the Quickenings used from each slot, that is of
each level, since a member learns the slots in order with the Quickening licences.

### The choice

`0x0030DB70(0, …)`, called from `0x002D5EB0` (`0x002D630D`, `0x002D6543`), reads the last action `0x022C2190`. Unless it is already a Concurrence,
`0xE2`-`0xF1`, it asks `0x002F8D60(0x022C2192)` (`0x0030DC55`):

1. `0x002F8D60` walks the rows from the last to the first (`0x002F8D60`-`0x002F8E49`).
2. A row matches when each of the three counts is at least the row's byte `+0x01`, `+0x02` and `+0x03`.
3. The first match returns its byte `+0x00`, the Concurrence's action row; no match returns -1.

A valid action row is stored as row − `0xD0` at `0x022C2178`; -1 leaves `0x022C2178` at -1. While `0x01EEBAF0` is not
negative, `0x002F8D60` returns the word it selects from `0x022BE930` instead ([Debug menu](../Engine-Core/debug-menu.md)).

### How it is built

`Database/Tools/catalogues/small_tables.py` reads the `st2e` table at entry `+0x80` (16 rows of 13 bytes from the
section's `+0x20`) and names byte `+0x00` by its action row's name word `+0x34` ([Action list](action-list.md)).

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `+0x00` | `u8` | concurrence | `0x002F8D60` | the action row returned |
| `+0x01` | `u8[3]` | thresholds | `0x002F8D60` | the counts of first-, second- and third-level Quickenings needed |
| `+0x04` | `u8[9]` | | none | `0xFF` on every row |

The table is loaded only by `0x002F8D60` and the loader `0x00236C30`, both decompiled; `0x002F8D60` reads bytes
`+0x00`-`+0x03`, so `+0x04`-`+0x0C` have no reader.

### Checks

- The table's header gives 16 rows of 13 bytes, and the TSV has 16 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts that byte `+0x00` is a Concurrence row, `0xE2`-`0xF1`, and that `+0x04`-`+0x0C` are `0xFF`.
- Rows compared with their reader: row 0, Inferno, action 226, needs 3 first-level Quickenings and nothing else, and
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
