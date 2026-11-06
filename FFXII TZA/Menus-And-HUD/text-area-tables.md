---
title: "Area table text: the text blocks of the enemy definition tables in the area files"
kind: "reference"
category: "Menus and HUD"
addresses: "0x003EA710, 0x003845F0, 0x02EBF120, 0x0023A570, 0x02EBF170, 0x002B58B0"
---

## What it lists

[text-area-tables.tsv](text-area-tables.tsv) has one row per string of the text block inside an area file's enemy
definition table: 1,146 rows from 162 area files. The table is the `st2e` table in slot 2 of each
`plan_map/<area>/area/<area>.ard`, which `0x003EA710` binds into `0x02EBF120` with `0x003845F0` when the area loads
([Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)). Only the `in` and `ch` trees ship
`.ard` files, byte for byte the same, so the table has those two columns.

### What the strings hold

The text block has one string offset per definition row, and in each file every offset names the same string: the
8 bytes `12 8B 12 8B 12 8B 12 8B`. The `in` column reads it through the Japanese font as `FFFF` and the `ch` column
through the Chinese font as `考考考考`.

An enemy's shown name does not come from this block. The definition row holds a name word at `+0x08`, which
`0x0023A570` renders from the word banks at `0x02EBF170` with `0x002B58B0`
([Enemy names on screen](enemy-names-on-screen.md), [Word bank](text-word-bank.md)).

| `file` | `index` | `in` | `ch` |
|---|---:|---|---|
| `plan_map/asp_b/area/asp_b.ard@730` | 0 | `FFFF` | `考考考考` |
| `plan_map/bds_a/area/bds_a.ard@2780` | 0 | `FFFF` | `考考考考` |

## Columns

| Column | Meaning |
|---|---|
| `file` | the area file's path under `plan_master/<language>/`, then `@` and the table's offset in the file in hex |
| `index` | the string's position in the table's text block, from 0: the definition row it belongs to |
| `in` | the string decoded with the Japanese font |
| `ch` | the same string decoded with the Chinese font |
| `missing` | empty in every row: both trees ship every file |
| `same_bytes` | `in=ch` in every row: the two trees hold the same bytes |

## Data

| Fact | Value |
|---|---|
| area files | 166 in `in` and in `ch`, byte-identical |
| files whose table has rows | 162 |
| strings | 1,146 in each tree, one per definition row, pointing at 162 strings, one per file; all hold the same 8 bytes |

## Related

- [Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md) - the `.ard` file, its section
  directory and the enemy definition rows.
- [Enemy names on screen](enemy-names-on-screen.md) - where an enemy's name comes from.
- [Word bank](text-word-bank.md) - the names the definitions' name words select.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x0023A570` calls `0x00236A60`, `0x00322050`; `0x0023A570` is called by `0x00300E40`, `0x003266C0`; `0x002B58B0` is
  called by `0x0023A570`.
- Actor entity: those functions are documented on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [party control modes](../Engine-Core/party-control-modes.md).
- Combat AI: `0x003845F0` is called by `0x00238880`; those functions are documented on
  [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md).
- Combat action: `0x003845F0` is called by `0x00237FC0`; those functions are documented on
  [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md).
- Combat formula: `0x0023A570` calls `0x0023AC80`; those functions are documented on
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md).
- Gameplay: `0x0023A570` calls `0x00322C50`; those functions are documented on
  [identifier spaces](../Engine-Core/identifier-spaces.md).
- Presentation: `0x002B58B0` is called by `0x00506700`; those functions are documented on
  [battle numbers](battle-numbers.md).
- Spawn encounter lifecycle: `0x0023A570` calls `0x00236100`; `0x0023A570` is called by `0x0023A3B0`; those functions are
  documented on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md).
- World area: `0x003845F0` is called by `0x00238640`, `0x003847B0`; those functions are documented on
  [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md),
  [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md).
- World area: `0x0023A570` calls `0x00313F60`; `0x003845F0` calls `0x003846F0`; `0x003845F0` is called by `0x00236C30`,
  `0x0023A160`; `0x003EA710` calls `0x0023A160`, `0x003DCF00`.
- World area: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [item and ability ids](../Engine-Core/item-and-ability-ids.md),
  [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md).
