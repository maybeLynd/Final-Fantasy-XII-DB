[Home](../../README.md) / [Menus and HUD](README.md) / Area table text

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Area table text: the text blocks of the enemy definition tables in the area files | reference | Menus and HUD | Game text tables | Every string of the text blocks that the st2e enemy definition tables in the area .ard files carry, in the in and ch trees that ship the files: one four-character filler string per area table, which code binds the table and where enemy names come from instead, the row count per file, and why the two language columns hold the same bytes. | 0x003EA710, 0x003845F0, 0x02EBF120, 0x0023A570, 0x02EBF170, 0x002B58B0 |

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 20 calls with 11 other topics</summary>

**Characters and objects** (explained on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [force fight mode](../Engine-Core/force-fight-mode.md), [party control modes](../Engine-Core/party-control-modes.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) | calls | [`0x00236A60`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: reset state for reuse (on battle unit construction)<br>[`0x00322050`](../Characters-And-Objects/battle-unit-construction.md) (on battle unit construction) |
| [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) | is called by | [`0x00300E40`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) Battle unit: teardown and despawn (on equipping an item)<br>[`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) |
| [`0x002B58B0`](../Game-Files-And-Data-Tables/battle-text-tables.md) (on battle text tables) | is called by | [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) |

**Enemy AI and gambits** (explained on [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003845F0`](../Battle-Actions/action-definition-row.md) Area data: bind and rebase section descriptor (on action definition row) | is called by | [`0x00238880`](../Game-Files-And-Data-Tables/authored-data-tables.md) Gambit target definition: bind and build menu lookup (on authored data tables) |

**Battle actions** (explained on [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003845F0`](../Battle-Actions/action-definition-row.md) Area data: bind and rebase section descriptor (on action definition row) | is called by | [`0x00237FC0`](../Battle-Actions/action-definition-row.md) (on action definition row) |

**Damage and battle formulas** (explained on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) | calls | [`0x0023AC80`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: initialize definition record (on equipment) |

**Gameplay** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) | calls | [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) |

**Graphics** (explained on [battle numbers](battle-numbers.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002B58B0`](../Game-Files-And-Data-Tables/battle-text-tables.md) (on battle text tables) | is called by | [`0x00506700`](battle-numbers.md) (on battle numbers) |

**Enemy spawning** (explained on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) | calls | [`0x00236100`](../Enemy-Spawning/spawn-record-fields.md) (on spawn record fields) |
| [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) | is called by | [`0x0023A3B0`](../Items-Equipment-Shops-And-Licenses/item-list.md) (on item list) |

**World, areas and travel** (explained on [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md), [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md), [frame update order](../Engine-Core/frame-update-order.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md), [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003845F0`](../Battle-Actions/action-definition-row.md) Area data: bind and rebase section descriptor (on action definition row) | is called by | [`0x00238640`](../Game-Files-And-Data-Tables/battle-text-tables.md) (on battle text tables)<br>[`0x003847B0`](../Game-Files-And-Data-Tables/authored-data-tables.md) (on authored data tables) |
| [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) | calls | [`0x00313F60`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) (on equipping an item) |
| [`0x003845F0`](../Battle-Actions/action-definition-row.md) Area data: bind and rebase section descriptor (on action definition row) | calls | [`0x003846F0`](../Game-Files-And-Data-Tables/authored-data-tables.md) (on authored data tables) |
| [`0x003845F0`](../Battle-Actions/action-definition-row.md) Area data: bind and rebase section descriptor (on action definition row) | is called by | [`0x00236C30`](text-string-tables.md) (on text string tables)<br>[`0x0023A160`](../Enemy-Spawning/bestiary.md) (on bestiary) |
| [`0x003EA710`](text-area-tables.md) | calls | [`0x0023A160`](../Enemy-Spawning/bestiary.md) (on bestiary)<br>[`0x003DCF00`](../Game-Files-And-Data-Tables/ard-area-battle-data.md) (on ard area battle data) |

</details>
