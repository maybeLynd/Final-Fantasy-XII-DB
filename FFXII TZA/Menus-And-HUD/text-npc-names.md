---
title: "NPC name strings: every name of the npcdic.bin dictionaries in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00379D20, 0x003EAC40, 0x02B5E0D8, 0x003EAC10, 0x00263990, 0x002639E0, 0x0026DEA0, 0x00272CB0, 0x00268D10, 0x00536280"
---

## What it lists

[text-npc-names.tsv](text-npc-names.tsv) has one row per entry of `bin/npcdic.bin`, with the name in each of the nine
language trees: 2,282 rows, the same count in every language. Every shipped dictionary holds 2,282 entries, so the
name ids mean the same character in every language.

`0x00379D20` loads the dictionary at boot through `0x003EAC40` and keeps it at `0x02B5E0D8`. Entry `2 x id` is the first
name of pair `id` and entry `2 x id + 1` its second (`0x003EAC10`). A field character shows the first name until the
story flag with the same number as its pair is set, and the second after it (`0x00263990`, `0x002639E0`, `0x0026DEA0`).

The name tag (`0x00272CB0`), the field interaction pass (`0x00268D10`) and the battle log (`0x00536280`, always the second name)
put the names on screen. [NPC names](../Characters-And-Objects/npc-names.md) describes the file, the flag and the
script verbs that give an actor its name id.

### Reading the rows

| `index` | Pair | `us` | `de` | `in` |
|---:|---:|---|---|---|
| 0 | 0, first | `Rabanastran` | `Rabanastre-Bürger` | `ラバナスタ市民` |
| 1 | 0, second | `Rabanastran` | `Rabanastre-Bürger` | `ラバナスタ市民` |
| 32 | 16, first | `Imperial` | `Imperialer Soldat` | `帝国兵` |
| 33 | 16, second | `Sherral` | `Scharmal` | `シャルアール` |

Pair 0 repeats one name, so its flag changes nothing on screen; pair 16 shows `Imperial` until its flag is set
and `Sherral` after. The names hold no text codes.

## Columns

| Column | Meaning |
|---|---|
| `index` | the entry: pair `index / 2`, its first name when `index` is even and its second when odd |
| `us` to `ch` | the name in that language tree, decoded with the tree's font |
| `missing` | the languages whose dictionary has no entry `index`; empty in every row |
| `same_bytes` | the groups of languages whose name bytes are identical, each group's languages joined by `=` and the groups by `;`; only groups of two or more |

## Data

| Fact | Value |
|---|---|
| entries | 2,282 in each of the nine languages, 1,141 pairs |
| empty names | entries 1924 and 1925 in all nine languages; 1873, 1875, 1881 and 1883 also in `cn` and `ch`; 1996 and 2065 also in `cn` |

## Related

- [NPC names](../Characters-And-Objects/npc-names.md) - the dictionary file, the name flag, the pairs whose names differ
  and the verbs that assign a name id.
- [Text codes](text-codes.md) - the escape `0F 38` that inserts a name into message text.
- [String tables](text-string-tables.md) - the battle messages whose unit names come from here.
