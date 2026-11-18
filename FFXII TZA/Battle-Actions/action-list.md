[Home](../../README.md) / [Battle actions](README.md) / Action list

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts | reference | Battle actions | Action tables | All 543 action rows of the shipped battle_pack.bin, decoded field by field: the action id and name, its kind, MP or Mist cost, charge time base, power, hit, damage recipe, element, status chance and statuses, ranges, reach and area, knockback, enmity, effect and cinematic ids, the command list page and row, the three flag words with their documented bits named, the help and description lines, and a one-line explanation. | 0x02EBF138, 0x0031C5D0, 0x0031DBB1, 0x0031DBBE, 0x002F9860, 0x00305F10, 0x003093D0, 0x00320D70 |

## What it lists

[`action-list.tsv`](action-list.tsv) holds one line for each of the 543 rows of the action table that registry slot `0x02EBF138`
reaches (`battle_pack.bin` directory entry `+0x3C`). Row *n* is action id *n*. What every field does, and the code
that reads it, is on [Action definition row](action-definition-row.md); this page is the shipped content.

By kind: 1 Attack, 81 magicks, 24 technicks, 51 items, 13 summons, 18 Quickenings, 235 Foecraft moves, 16 traps,
26 Esper attacks, 16 Concurrences, the six special rows 151 and 153-157 (`actstop`, `escape`, `escapestop` and three
Reserve rows), and 56 rows of kind 255. Of those 56, 47 are named `NOT USED` or Reserve; the other nine are named rows
with no linked id (`+0x22` = `0xFFFF`): `Do nothing.` (146), Mount (148), Dismount (149), `sousachange` (152), three
Mist Charge rows (242-244), Chain Bonus (245) and Dismiss (275).

The kind counts include rows named as unused: 24 of the 235 Foecraft rows are named Reserve and 8 of the 16
Concurrence rows `NOT USED`. With the 47 such rows of kind 255 and the three kind-13 Reserve rows, 82 rows in all
are reserve data: the id check and the commit accept them and no enemy order or other shipped table names them. The
party route refuses the 35 of kinds 7, 10 and 13. Rows 111-123 are the action rows of the item rows `0x001D`-`0x0029`,
also named Reserve.

The `enemy_users` column names, for every row, the enemies that use it. An enemy uses an action when an order set its definition names ([Enemy order sets](../Enemy-AI-And-Gambits/enemy-order-sets.md), `used_by`) holds an order with that action word, or a weighted pick (`0x8000` + run, `[0x02EBF160]`, drawn by `0x00308EC0`) whose run lists it. 305 of the 543 rows have such users, 39 of them only through weighted picks. Attack has the most, 426 enemy names, then Lunge 183, Protect 83, Ram 74 and Shell 48.

### Where the values come from

Each line is read from the shipped `battle_pack.bin` in these steps:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | the `st2e` table at entry `+0x3C`: 543 rows of 60 bytes from the section's `+0x20`; |   |
| 2 | the name word `+0x34` through the word banks at entry `+0xF8`; | `0x00305F10` |
| 3 | the help line `+0x00` (4000 for no help line) and the description `+0x2E` through the text groups, group `id / 1000` and row `id % 1000` as `0x002F9860` resolves them for `0x0031C5D0`; | `0x0031DBB1`, `0x0031DBBE` |
| 4 | every one-byte text code through the glyph table of the shipped `us` font `font00.dat` (records of `0x24` bytes from `+0x28`, key = byte - `0x20`, the glyph's UTF-8 at `+0x04`, as [Fonts](../Menus-And-HUD/fonts.md) describes); token `0x02` (line break) is written as a space; |   |
| 5 | element bits by the names on [Elements](../Damage-And-Battle-Formulas/elements.md), status bits by the names in [Statuses](../Status-Effects-And-KO/statuses.md)' table; |   |
| 6 | each flag word kept as hex, with beside it only the bits that have a named effect on [Action definition row](action-definition-row.md); `+0x2C` bits `0x1000` and `0x8000` take their names from [Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md). | `0x0030846A`, `0x003084B3` |

`0x00305F10` shows the name of the row in the low word of `0x022C2190`: it splits the name word `+0x34` into the bank
`w >> 11` and the entry `w & 0x7FF`¹, and hands the text, or a null text when `0x02EBF138`,
its rows or `0x02EBF170` are missing², to `0x002B58B0(text, 0)`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00305F9B`, `0x00305FCE` |
| ² | `0x00305F45`-`0x00305F67` |

</details>

That result goes to `0x002902D0` with `[0x022C2180]`, or with `0xC8` for rows `0xE2`-`0xF1`¹, and `0x00305F10` returns 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00305F2C`-`0x00305F42`, `0x00305FF5` |

</details>

`0x003093D0(id)` returns the `linked_id` of an item row: it checks `id` with `0x00322C50(0x14, id, 0)`, takes the row
at the table base plus `id` times the stride at table `+8`, and returns its `+0x22` when the kind `+0x1E` is 3. It
returns `0xFFFF` when the check fails, the table is missing or the kind is any other¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003093E2`-`0x00309435` |

</details>

`0x00320D70` reads `range_near_tenths` and `range_middle_tenths` as `[row + 0x02 + i] / 10.0`, the bytes `+0x02`
and `+0x03` divided by 10.0 for its fourth argument `i` (`divss xmm0, [0x008F8180]`, `0x00320DE6`-`0x00320DF5`), or an
equipment parameter when bit `0x4000000` of `+0x0C` is set¹; [Action range](action-range.md) has the
rule.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00320D74` |

</details>

### Properties of the shipped rows

- The table's header gives 543 rows of 60 bytes, one TSV line each.
- The kind counts equal the shipped counts on [Action definition row](action-definition-row.md), "The kind byte".
- Example rows: row 0 Cure (kind 1, 8 MP, power 20, help "Restore a small amount of HP to one
  ally."), row 150 Attack (kind 0, help 4000, description "Attack with weapon in hand."), row 169 Steal (kind 2,
  linked id `0x400B`, cost 0, flags `0x00004688`, help "Steal from one foe.").

## Columns

| Column | Meaning |
|---|---|
| `id`, `name` | the action id (the row) and its shipped name |
| `kind`, `kind_name` | `+0x1E` and its name from the kind table (`-` for 255) |
| `category` | `+0x1C`, which picks the presentation event |
| `linked_id` | `+0x22`, the magick, technick, item or ability id the row stands for |
| `cost` | `+0x0A`: MP, or Mist charges for summons and Quickenings |
| `b0B` | `+0x0B`, 1-3 on rows 182-207 only |
| `charge_base`, `power`, `power2`, `hit`, `recipe` | `+0x09`, `+0x10`, `+0x11`, `+0x12`, `+0x08` (0 = the weapon's recipe) |
| `element`, `status_chance`, `statuses`, `boost_percent` | `+0x13`, `+0x14`, `+0x18`, `+0x15` |
| `range_near_tenths`, `range_middle_tenths`, `reach_tenths` | `+0x02`, `+0x03`, `+0x05` |
| `area_radius`, `area_angle` | `+0x06`, `+0x07` (0 = the target alone) |
| `knockback` | `+0x04` |
| `enmity_direct`, `enmity_spread`, `enmity_others` | `+0x1D`, `+0x1F`, `+0x20` |
| `effect_class`, `effect_id`, `cinematic_id`, `event` | `+0x21`, `+0x24`, `+0x28`, `+0x30` |
| `esper` | summons: the Esper's party-table row `+0x26` |
| `menu_page`, `menu_row`, `ai_reaction` | `+0x38`, `+0x39`, `+0x3A` |
| `flags`, `flag_names` | `+0x0C` as hex and the bits with a named effect |
| `flags2`, `flag2_names` | `+0x2C` as hex and the bits with a named effect |
| `target_flags`, `target_flag_names` | `+0x36` as hex and the bits with a named effect |
| `help_id`, `help` | `+0x00` and its shipped line (4000 = no line) |
| `desc_id`, `description` | `+0x2E` and its shipped line |
| `explanation` | a one-line summary built from the row's own fields: what nothing shipped names, for the `NOT USED` and Reserve rows, "kind 255, no linked id" for the nine named kind-255 rows |
| `enemy_users` | how many distinct enemy names use the action through their order sets, then the names in alphabetical order; a definition with no name as `No name (<area> row <n>)`; `-` when no order of the 1,422 sets names it |

## Related

- [Action definition row: power, targeting, range, element and flag fields of a battle action](action-definition-row.md)
- [Equipment list: every weapon, shield, armor, accessory and ammunition row with its name, class, price, stats, elements, statuses and bonuses](../Items-Equipment-Shops-And-Licenses/equipment-list.md)

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 36 calls with 11 other topics</summary>

**Characters and objects** (explained on [party control modes](../Engine-Core/party-control-modes.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [force fight mode](../Engine-Core/force-fight-mode.md), [party data](../Party/party-data.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002B58B0`](../Game-Files-And-Data-Tables/battle-text-tables.md) (on battle text tables) | is called by | [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) |
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is called by | [`0x002367A0`](../Party/party-members.md) (on party members)<br>[`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction)<br>[`0x0031B810`](../Enemy-AI-And-Gambits/enmity.md) Battle unit: find mapped definition selector by index (on enmity)<br>[`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots)<br>[`0x00329CC0`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) Battle slot map: initialize mapping classes (on strong and weak mode) |

**Damage and battle formulas** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is called by | [`0x002FEF30`](../Enemy-Spawning/bestiary.md) Battle stats: rebuild effective stats and affinity state (on bestiary) |

**Items, equipment, shops and licenses** (explained on [stats](../Damage-And-Battle-Formulas/stats.md), [bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md), [party data](../Party/party-data.md), [party table](../Party/party-table.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [quickening and esper list](quickening-and-esper-list.md), [command availability](command-availability.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is called by | [`0x003096F0`](../Damage-And-Battle-Formulas/stats.md) Equipment: check matching secondary partner selected or owned (on stats)<br>[`0x0030B180`](../Items-Equipment-Shops-And-Licenses/bazaar.md) Battle id class d: reset purchased entry and nested prerequisite state (on bazaar)<br>[`0x0030B4B0`](../Engine-Core/item-and-ability-ids.md) (on item and ability ids)<br>[`0x0030B510`](action-list.md)<br>[`0x0030B570`](../Items-Equipment-Shops-And-Licenses/bazaar.md) Battle id class d: set runtime flag bit1 if supported (on bazaar)<br>[`0x0030B630`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar)<br>[`0x00317930`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) Equipment: check item eligible for slot (on equipping an item)<br>[`0x0031A510`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: set equipment slot by mapped id (on equipment)<br>[`0x00323910`](../Items-Equipment-Shops-And-Licenses/buying-a-license.md) Battle stats: set license node state and apply side effects (on buying a license)<br>[`0x00323C60`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) Battle stats: has required license for equipment (on equipping an item)<br>[`0x00323D10`](../Items-Equipment-Shops-And-Licenses/licenses.md) Battle stats: check license node acquire reason (on licenses)<br>[`0x00323EC0`](command-availability.md) Battle stats: has required license for action (on command availability) |
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is also called by | [`0x00325F40`](../Items-Equipment-Shops-And-Licenses/inventory.md) Inventory derived index: update on presence transition (on inventory) |

**Movement and pathfinding** (explained on [game over](../World-Areas-And-Travel/game-over.md), [party data](../Party/party-data.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is called by | [`0x0031BAC0`](../Party/party-slots.md) (on party slots)<br>[`0x00326BB0`](../Party/party-data.md) (on party data) |

**Party** (explained on [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [party data](../Party/party-data.md), [party control modes](../Engine-Core/party-control-modes.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is called by | [`0x003170E0`](../Party/party-members.md) Party configuration: add selector07 to25 to available primary index (on party members)<br>[`0x0031AC00`](../Party/party-data.md) (on party data)<br>[`0x0031B510`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x00320800`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x00321100`](../Party/party-members.md) (on party members)<br>[`0x00326500`](../Party/party-leader.md) Party focus: select and request default actor (on party leader)<br>[`0x003287A0`](../Party/party-members.md) Party configuration: demote other runtime roster selectors to non roster (on party members)<br>[`0x00328DB0`](../Party/party-members.md) Party configuration: reconcile runtime roster first three from requested selectors (on party members)<br>[`0x00329080`](../Scripts-And-Script-Commands/party-verbs.md) Party configuration: set definition selector for index (on party verbs) |

**Graphics** (explained on [battle numbers](../Menus-And-HUD/battle-numbers.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002B58B0`](../Game-Files-And-Data-Tables/battle-text-tables.md) (on battle text tables) | is called by | [`0x00506700`](../Menus-And-HUD/battle-numbers.md) (on battle numbers) |

**Random numbers** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00308EC0`](../Enemy-AI-And-Gambits/enemy-order-sets.md) Battle data: resolve weighted id (on enemy order sets) | calls | [`0x00328370`](../Random-Numbers/random-number-generators.md) (on random number generators) |

**Status effects and KO** (explained on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is called by | [`0x0030E130`](../Status-Effects-And-KO/battle-buffs.md) Battle stats: modify status layer state and process side effects (on battle buffs)<br>[`0x0030FED0`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) Battle stats: recompute derived state and auto statuses (on equipping an item)<br>[`0x00310DB0`](action-results.md) Battle unit: run periodic combat maintenance (on action results) |

</details>
