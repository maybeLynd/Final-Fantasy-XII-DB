[Home](../../README.md) / [Battle actions](README.md) / Weapon motion list

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Weapon motion list: the animation set each weapon's motion class gives a battle unit, from the WepJob_Matrix table | reference | Battle actions | Action tables | All 23 rows of the shipped WepJob_Matrix table in battle_pack.bin: the animation set for each weapon motion class, the weapons of each class, the bare-handed row for Brawler (augment 9), the set every party unit gets in the action caches, and the functions that read the table. | 0x02EBF180, 0x003202F0, 0x003203B0, 0x00325A20, 0x00325AD0, 0x00320170, 0x00320230 |

## What it lists

[`weapon-motion-list.tsv`](weapon-motion-list.tsv) holds one line for each of the 23 rows of the table that registry slot `0x02EBF180` points
at (`battle_pack.bin` directory entry `+0x04`). The table is not an `st2e` table: it is a `u16` stride (1), a `u16`
row count (23), and then one byte per row from `+0x04`. Row *m* is a weapon motion class, the byte `+0x26` of a
main-hand equipment row ([Equipment row](../Items-Equipment-Shops-And-Licenses/equipment-row.md)), and its byte is an
animation set.

So the weapon in a unit's main hand decides its animation set: the game reads the weapon's motion class from its
equipment row and takes that class's byte here, which the game uses for the motion lane of the unit's model. An enemy
whose definition row names a set uses that set instead.

### How the set is chosen

`0x003202F0(stats, &set)` gives a unit its animation set¹. It first sets `set` to −1, and a
null record keeps it and returns −1²; each rule below returns 0:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003202F0`-`0x00320443` |
| ² | `0x003202FA`, `0x0032030B` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | An enemy record (stats `+0x05` = 1) whose definition row byte `+0x13` is not `0xFF` takes that byte. The row is `[unit + 0xE60]` of the battle unit `0x0031B860` finds for the record; a record with no unit goes on to the next rule. | `0x0032031F`-`0x0032033C`<br>`0x00320327` |
| 2 | A record whose main hand `+0x50` is `0x1000`, Unarmed, with no off-hand item (`+0x52` = `0xFFFF`) and Brawler (augment 9) in either augment layer (`+0x69` or `+0x79` bit `0x2`) takes row 22. | `0x0032034B`-`0x00320384` |
| 3 | Otherwise `0x003203B0(main hand)` takes the row of the main-hand item's motion class `+0x26` when the id is not `0xFFFF` and the item's slot bits `+0x07` are below `0x20`; any other id gives row −1, the high byte of the row count, 0. | `0x003203B0`-`0x0032043C` |

Its callers:

- `0x00320170` gives the motion lane of a unit's model
  ([Actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md)). It calls `0x003202F0` with the stats record
  `[unit + 0x698]` of the unit behind the id¹, and with 0, which gives −1, when battle
  flag `0x02089340` bit `0x10` is clear or there is no actor or unit².
- `0x00320170` sends an actor that is one of the four `0x00263750` roster actors to `0x00320230(slot, &set)`
  instead³.
- `0x00320230` does the same for the member in a seat of slot map 4. It answers 22 itself for the seat `0x00327200`
  returns (`0x00304650` jumps to it) while `0x00303EC0` holds, and in that state uses the Chocobo's record
  `[0x02EBF190]` + `0x2E58` for seat 3⁴.
- Otherwise `0x00320230` takes the member byte at `[0x02EBF190]` + `0x5A90` + seat × 2 and its record
  `[0x02EBF190]` + 8 + member × `0x1C8`; a seat that `0x00322C50(0x17, seat, 0)` refuses, or a member above
  `0x27`, goes to `0x003202F0` with 0, which gives −1⁵.
- `0x00325A20` and `0x00325AD0`, the two action caches of [Action phases](action-phases.md), call it only for a unit
  that is not a party unit; a party unit (stats `+0x05` = 0) gets the byte of row 1 there, set 1
 ⁶. A unit whose stats record `+0x698` is null is not a party unit there:
  it goes to `0x003202F0` with 0, which gives −1⁷.
  - A null unit is sent to the same branch⁸, which then reads `[0 + 0x698]`
   ⁹ and faults.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003588B0`, `0x00263E30` |
| ² | `0x0032018F`-`0x003201F2` |
| ³ | `0x003201B0`-`0x0032021C` |
| ⁴ | `0x00320240`-`0x00320285` |
| ⁵ | `0x0032028A`-`0x003202E2` |
| ⁶ | `0x00325A50`-`0x00325A5A`, `0x00325AD0` |
| ⁷ | `0x00325A43`, `0x00325AEB` |
| ⁸ | `0x00325A3A`, `0x00325ADF` |
| ⁹ | `0x00325A62`, `0x00325B09` |

</details>

### Where the values come from

Each line is one of the 23 bytes after the stride and count at entry `+0x04`, with, for its motion class, the names
of the main-hand equipment rows 0-419 (slot bits `+0x07` below `0x20`) whose `+0x26` is that class, leaving out the
rows named Reserve.

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `+0x00` | `u16` | stride | `0x003202F0`, `0x00325A20`, `0x00325AD0` | the row size, 1 |
| `+0x02` | `u16` | count | no instruction | 23 |
| `+0x04` | `u8[23]` | sets | `0x003202F0`, `0x00325A20`, `0x00325AD0` | the animation set of each motion class |

The slot is loaded by `0x00320376` and `0x0032042D`¹, `0x00325A50`² and `0x00325AF5`³,
and stored once by the loader⁴; none of them reads the count.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003202F0` |
| ² | `0x00325A20` |
| ³ | `0x00325AD0` |
| ⁴ | `0x00236C74` |

</details>

### Properties of the shipped rows

- The header gives stride 1 and 23 rows, one TSV line each.
- Example rows: motion class 3 (the 27 weapons listed in the next item) gives set 3;
  motion class 22, read only by the bare-handed rule, gives set 2; row 1, Unarmed, gives set 1, the set of every party
  unit in the action caches.
- The 27 weapons of motion class 3, in equipment table order: Broadsword, Longsword, Iron Sword, Zwill Blade, Ancient Sword, Blood Sword, Lohengrin, Flametongue, Demonsbane, Icebrand, Platinum Sword, Bastard Sword, Diamond Sword, Runeblade, Deathbringer, Stoneblade, Durandal, Mythril Sword, Hero's Blade, Joyeuse, Chirijiraden, Flimsy Blade, Mythril Blade, Kumbha, Great Trango, Karkata, Simha.
- Motion classes 0, 9, 16, 19 and 22 have no shipped weapon; class 22 is reached only through the bare-handed rule.

## Columns

| Column | Meaning |
|---|---|
| `motion_class` | the row, a weapon motion class |
| `animation_set` | the row's byte |
| `weapons`, `first_weapons` | how many main-hand rows have the class, and every one of them by name, in row order; the 13 main-hand rows named Reserve (ten of class 1, rows 179 and 180 of class 13, row 186 of class 18) and the 108 named `NOT USED` are not counted |
| `explanation` | a one-line summary |

## Related

- [Equipment row: every field of a weapon, shield, armor, accessory or ammunition data row and its bonus record](../Items-Equipment-Shops-And-Licenses/equipment-row.md)
- [Action phases: delay, charge time, approach, execution and the end of a battle action](action-phases.md)
- [Actor model rebuild: the state machine that reloads an actor's model, attachments and body for its current definition, and what runs it](../Characters-And-Objects/actor-model-rebuild.md)

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 77 calls with 16 other topics</summary>

**Enemy AI and gambits** (explained on [frame update order](../Engine-Core/frame-update-order.md), [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md), [glossary](../Engine-Core/glossary.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [battle units](../Characters-And-Objects/battle-units.md), [enmity](../Enemy-AI-And-Gambits/enmity.md), [gambit screen](../Menus-And-HUD/gambit-screen.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse) | is called by | [`0x003247F0`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle unit: rebuild perception candidate cache (on enemy ai)<br>[`0x00324F20`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle perception: refresh candidate cache generation (on enemy ai) |
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is called by | [`0x00301AD0`](../Enemy-AI-And-Gambits/enemy-order-sets.md) Ai order: evaluate target selector (on enemy order sets)<br>[`0x003215C0`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: read for combatant id (on enmity)<br>[`0x00321630`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: get highest relevant (on enmity)<br>[`0x00321770`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: any above threshold (on enmity)<br>[`0x00321850`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: write for combatant id (on enmity)<br>[`0x003219D0`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: propagate to perceiving foes (on enmity)<br>[`0x00321B00`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: adjust other relevant combatants (on enmity)<br>[`0x00321E40`](weapon-motion-list.md) Battle enmity: clamp and store<br>[`0x00327A10`](../Menus-And-HUD/widgets.md) Gambit config: classify action target pair compatibility (on widgets)<br>[`0x00327CB0`](../Enemy-AI-And-Gambits/gambits.md) Gambit config: load authored preset and rebuild runtime orders (on gambits) |

**Items, equipment, shops and licenses** (explained on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [stats](../Damage-And-Battle-Formulas/stats.md), [bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md), [party data](../Party/party-data.md), [party table](../Party/party-table.md), [quickening and esper list](quickening-and-esper-list.md), [command availability](command-availability.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0031B860`](battle-log.md) Battle stats: find owning battle unit (on battle log) | is called by | [`0x0031A410`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: set equipment slot by stats index (on equipment)<br>[`0x0031A510`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: set equipment slot by mapped id (on equipment)<br>[`0x0031A630`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: set equipment slot direct (on equipment)<br>[`0x00323910`](../Items-Equipment-Shops-And-Licenses/buying-a-license.md) Battle stats: set license node state and apply side effects (on buying a license) |
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is called by | [`0x003096F0`](../Damage-And-Battle-Formulas/stats.md) Equipment: check matching secondary partner selected or owned (on stats)<br>[`0x0030B180`](../Items-Equipment-Shops-And-Licenses/bazaar.md) Battle id class d: reset purchased entry and nested prerequisite state (on bazaar)<br>[`0x0030B4B0`](../Engine-Core/item-and-ability-ids.md) (on item and ability ids)<br>[`0x0030B510`](action-list.md) (on action list)<br>[`0x0030B570`](../Items-Equipment-Shops-And-Licenses/bazaar.md) Battle id class d: set runtime flag bit1 if supported (on bazaar)<br>[`0x0030B630`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar)<br>[`0x00317930`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) Equipment: check item eligible for slot (on equipping an item)<br>[`0x0031A510`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: set equipment slot by mapped id (on equipment)<br>[`0x00323910`](../Items-Equipment-Shops-And-Licenses/buying-a-license.md) Battle stats: set license node state and apply side effects (on buying a license)<br>[`0x00323C60`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) Battle stats: has required license for equipment (on equipping an item)<br>[`0x00323D10`](../Items-Equipment-Shops-And-Licenses/licenses.md) Battle stats: check license node acquire reason (on licenses)<br>[`0x00323EC0`](command-availability.md) Battle stats: has required license for action (on command availability) |
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is also called by | [`0x00325F40`](../Items-Equipment-Shops-And-Licenses/inventory.md) Inventory derived index: update on presence transition (on inventory) |

**Movement and pathfinding** (explained on [frame update order](../Engine-Core/frame-update-order.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [battle units](../Characters-And-Objects/battle-units.md), [party data](../Party/party-data.md), [party slots](../Party/party-slots.md), [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md), [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md), [bestiary](../Enemy-Spawning/bestiary.md), [force fight mode](../Engine-Core/force-fight-mode.md), [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md), [status timers](../Status-Effects-And-KO/status-timers.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md), [game over](../World-Areas-And-Travel/game-over.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263750`](../Graphics/model-asset-list.md) (on model asset list) | is called by | [`0x0034A940`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0037CF00`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0037D000`](../Party/party-slots.md) (on party slots) |
| [`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse) | is called by | [`0x00319490`](../Rewards-EXP-Gil-And-Loot/loot-pickups.md) (on loot pickups)<br>[`0x00326BB0`](../Party/party-data.md) (on party data)<br>[`0x00326D60`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x00329A80`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00329B00`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) (on heading speed to position delta)<br>[`0x003357B0`](../Movement-And-Pathfinding/battle-locomotion.md) Battle locomotion: query dynamic actor obstruction (on battle locomotion)<br>[`0x003377C0`](../Rewards-EXP-Gil-And-Loot/loot-pickups.md) (on loot pickups)<br>[`0x00338490`](../Party/party-leader.md) Party follow: solve formation (on party leader)<br>[`0x0033C310`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x003911D0`](weapon-motion-list.md) |
| [`0x0031B860`](battle-log.md) Battle stats: find owning battle unit (on battle log) | is called by | [`0x0033CB10`](../Status-Effects-And-KO/status-timers.md) (on status timers)<br>[`0x0033D890`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion) |
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is called by | [`0x0031BAC0`](../Party/party-slots.md) (on party slots)<br>[`0x00326BB0`](../Party/party-data.md) (on party data) |

**Rewards: EXP, LP, gil and loot** (explained on [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0031B860`](battle-log.md) Battle stats: find owning battle unit (on battle log) | is called by | [`0x002F8BB0`](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md) Reward: compute experience for recipient (on stat growth per level)<br>[`0x0030C650`](../Menus-And-HUD/hud.md) Battle stats: advance level to target and recompute growth (on hud) |

**Scripts and script commands** (explained on [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263750`](../Graphics/model-asset-list.md) (on model asset list) | is called by | [`0x003415D0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00341CB0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00342250`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00342910`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x00342EC0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x003446D0`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00344740`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00346EB0`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x003473E0`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00347970`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x0034AF80`](weapon-motion-list.md)<br>[`0x0034DF40`](weapon-motion-list.md) |
| [`0x00263750`](../Graphics/model-asset-list.md) (on model asset list) | is also called by | [`0x0034F060`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x0034F890`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x00350050`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x003507B0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x003509E0`](weapon-motion-list.md)<br>[`0x00352190`](../Story-Events-And-Hunts/mt-bur-omisace-scripts.md) (on mt bur omisace scripts)<br>[`0x00352FA0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x003537D0`](weapon-motion-list.md) |

**Status effects and KO** (explained on [status timers](../Status-Effects-And-KO/status-timers.md), [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md), [force fight mode](../Engine-Core/force-fight-mode.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse) | is called by | [`0x00386860`](../Status-Effects-And-KO/statuses.md) Battle formula: build runtime counter periodic hp credit (on statuses) |
| [`0x0031B860`](battle-log.md) Battle stats: find owning battle unit (on battle log) | is called by | [`0x002F9400`](../Status-Effects-And-KO/mp.md) Battle unit: resolve periodic primary resource recovery step (on mp)<br>[`0x0030E360`](../Engine-Core/identifier-spaces.md) Battle stats: change status and process side effects (on identifier spaces)<br>[`0x0030F690`](../Damage-And-Battle-Formulas/augments.md) Battle stats: remove statuses from mask and recompute (on augments)<br>[`0x0030FED0`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) Battle stats: recompute derived state and auto statuses (on equipping an item)<br>[`0x00386860`](../Status-Effects-And-KO/statuses.md) Battle formula: build runtime counter periodic hp credit (on statuses) |
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is called by | [`0x0030E130`](../Status-Effects-And-KO/battle-buffs.md) Battle stats: modify status layer state and process side effects (on battle buffs)<br>[`0x0030FED0`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) Battle stats: recompute derived state and auto statuses (on equipping an item)<br>[`0x00310DB0`](action-results.md) Battle unit: run periodic combat maintenance (on action results) |

</details>
