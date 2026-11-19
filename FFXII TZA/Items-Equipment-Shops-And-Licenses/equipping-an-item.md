[Home](../../README.md) / [Items, equipment, shops and licenses](README.md) / Equipping an item

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Equipping an item: the steps from picking a piece in the equip menu to the rebuilt stats | operation | Items, equipment, shops and licenses | Equipment | The order in which the game equips one piece from the equip menu: the list and its refusal marks, the setter, the eligibility test and the license test, the worn copy moved from the old piece to the new, the hands reconciled, the stats rebuilt and the unit refreshed, and when the setter reloads the fighting units' models; with what happens for a refused piece, a two-handed weapon, a shield, ammunition and taking a piece off, each step linked to the page that explains it. | 0x003FF360, 0x003FFA20, 0x0031A510, 0x00317930, 0x00323C60, 0x00318B40, 0x0030FED0, 0x00324470, 0x00324380 |

## What the player sees

In the equip menu the player picks a slot and a piece from its list. Pieces the character cannot wear are marked,
and the stat rows show the new values next to the current ones. After the choice the piece is worn and the stats
change.

## Steps

| Step | What happens | Where in the code |
|---|---|---|
| 1 | **The list.** The equip pane `0x003FF360` shows the five slots, the pieces for the chosen slot and the stat rows; a piece the character cannot wear is marked, and so is ammunition that does not match the weapon ([equipment](equipment.md#the-equip-screen)). |   |
| 2 | **The setter.** Choosing a piece runs `0x003FFA20(slot, id)`, which calls the party-seat setter `0x0031A510(member, slot, id, 1)` ([equipment](equipment.md#who-equips), [equipment](equipment.md#the-setters)).<br>• `member` is `0x00282EA0` of the menu block's word `+0xDE0`. `0x003FFA20` then refreshes the menu: `0x00283270(0)`, `0x0027F210`, which fills the five equipment rows, `0x003FEAD0(0)`, `0x00283E40` on `[[0x0209AC30] + 0x130] + 0xC0` when `+0x130` is set, `0x002858A0(0, 0)` and last `0x00283840(1)`. | `0x003FFA35`-`0x003FFA4F`<br>`0x003FFA54`-`0x003FFAA0` |
| 3 | **The eligibility test.** `0x00317930` checks, in order, the slot, a free copy, the slot bits of the piece's row, the pairing with the main hand, the party row's class mask and then the license test `0x00323C60` ([equipment](equipment.md#can-it-be-worn), [equipment row](equipment-row.md)). |   |
| 4 | **The license test.** The requirement mask for the piece is built from the license node table and compared with the member's owned-square bits; owning any square that lists the piece is enough ([licenses](licenses.md#the-test), [License Board](license-board.md)). |   |
| 5 | **The worn copy.** One worn copy moves from the old piece to the new one in the inventory ([equipment](equipment.md#the-setters), [inventory](inventory.md#changing-the-inventory)). |   |
| 6 | **The store.** The id is written to the member record's slot word ([equipment](equipment.md#the-slot-words), [unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)). |   |
| 7 | **The hands.** `0x00318B40` reconciles the main hand and the off hand: an empty main hand becomes Unarmed, and a pairing that no longer holds empties the off hand or unarms the main hand ([equipment](equipment.md#the-two-hands)). |   |
| 8 | **The stats.** When the slot's word has changed, `0x0030FED0(record, 0x97)` rebuilds the stats and augments, and `0x00324470` refreshes the unit ([equipment](equipment.md#the-setters), [stats](../Damage-And-Battle-Formulas/stats.md#the-rebuild), [augments](../Damage-And-Battle-Formulas/augments.md#the-rebuild)).<br>• `0x00324470(unit)` calls `0x002ECF10(actor, b, 0)`, the actor being the unit's `+0x10` and `b` its flag bit `0x800000` as 0 or 1, and the action reset `0x003105D0(unit)`. It tears the unit down with `0x00300E40(unit, 0)` when it has no stats record `+0x698`, or one with KO, Stone or X-Zone outside a town, unless unit flag bit `0x2` is set.<br>• Then it calls `0x002E42D0`, `0x002699D0` and `0x002ECEC0` on the actor `+0x10` and sets unit flag bit `0x40`. | `0x00324476`-`0x00324490`<br>`0x80000003`<br>`0x00313F60`<br>`0x00324495`-`0x003244C1`<br>`0x003244C6`-`0x003244E1` |
| 9 | **The model.** With `flags` bit `0x1` clear, `0x0031A510` then re-records the fighting units and reloads their models through `0x00324380`, which runs the model rebuild for slots 0 to 3; the equip menu and the shop pass `flags` 1, so their setter call does not reload ([equipment](equipment.md#the-setters), [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md#what-runs-it)). |   |

`0x00324380` takes the units of slots 0 to 3¹. For each unit it calls `0x0037B4B0` on `[unit + 0x10]` when
that is non-null, and records at `0x022C257C + slot` the row byte `+4` of the stats record `[unit + 0x698]` when unit
flag bit `0x4` is set, or `0xFF` for no unit or a clear bit². It then jumps to the model
read-in `0x0037CA80`³. The stats record is read with no null test⁴, so a unit with
bit `0x4` set and a null `+0x698` faults there.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00236820` |
| ² | `0x00324398`-`0x003243D6` |
| ³ | `0x003243E7` |
| ⁴ | `0x003243BA`-`0x003243C1` |

</details>

## Outcomes

- **A piece the test refuses**: the setter returns -1 before any copy moves, so nothing changes
  ([equipment](equipment.md#can-it-be-worn)).
- **Re-equipping the piece already worn** needs a spare copy, because the free-copy test runs before the old copy
  is released ([equipment](equipment.md#can-it-be-worn)).
- **A two-handed weapon** drops the shield, a shield under a two-handed or ammunition weapon leaves the character
  Unarmed, and removing ammunition unarms its weapon ([equipment](equipment.md#the-two-hands)).
- **Taking a piece off** always succeeds: the setter skips the test for an empty slot
  ([equipment](equipment.md#can-it-be-worn)).
- **Optimise and remove all** set the five slots through `0x0031A710` and `0x0031A300` and reload the models once at
  the end ([equipment](equipment.md#who-equips), [equipment](equipment.md#optimise)).
- **A piece bought in a shop and equipped there** goes through the same setter with the same `flags` 1
  ([equipment](equipment.md#who-equips), [shops](shops.md)).

## Related

- [Equipment](equipment.md): the slots, the test and the hands in full.
- [Licenses](licenses.md): the license test and buying squares.
- [Stats](../Damage-And-Battle-Formulas/stats.md): what the rebuild adds.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 171 calls with 42 other topics</summary>

**Characters and objects** (explained on [frame update order](../Engine-Core/frame-update-order.md), [enemy respawning](../Enemy-Spawning/enemy-respawning.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [party control modes](../Engine-Core/party-control-modes.md), [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [native commands](../Scripts-And-Script-Commands/native-commands.md), [ko and game over](../Status-Effects-And-KO/ko-and-game-over.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [battle units](../Characters-And-Objects/battle-units.md), [force fight mode](../Engine-Core/force-fight-mode.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md), [actor record](../Characters-And-Objects/actor-record.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](equipping-an-item.md) | is called by | [`0x0031B770`](../Enemy-AI-And-Gambits/gambit-conditions.md) Battle unit: find by combatant id (on gambit conditions)<br>[`0x00321170`](../Enemy-Spawning/enemy-respawning.md) Battle unit: get by slot index if unit flag4 set (on enemy respawning) |
| [`0x002699D0`](equipping-an-item.md) | calls | [`0x003587C0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) |
| [`0x002699D0`](equipping-an-item.md) | is called by | [`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots)<br>[`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x002E42D0`](equipping-an-item.md) | is called by | [`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots)<br>[`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x002ECEC0`](equipping-an-item.md) | is called by | [`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) |
| [`0x002ECF10`](equipping-an-item.md) | is called by | [`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) |
| [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn | calls | [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction)<br>[`0x0025AB30`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild)<br>[`0x002697E0`](../Graphics/effect-file-loading.md) (on effect file loading)<br>[`0x00300FC0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00322050`](../Characters-And-Objects/battle-unit-construction.md) (on battle unit construction) |
| [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn | is called by | [`0x00233EA0`](../Characters-And-Objects/battle-units.md) (on battle units)<br>[`0x00233F70`](../Enemy-Spawning/enemy-respawning.md) Battle unit: update lifecycle and combat frame (on enemy respawning)<br>[`0x002348E0`](../Enemy-AI-And-Gambits/enmity.md) (on enmity)<br>[`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) |
| [`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action | calls | [`0x00236820`](equipping-an-item.md)<br>[`0x00236850`](../Enemy-AI-And-Gambits/enemy-order-sets.md) (on enemy order sets) |
| [`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action | is called by | [`0x00236A60`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: reset state for reuse (on battle unit construction)<br>[`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn<br>[`0x00300FC0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) |
| [`0x00313F60`](equipping-an-item.md) | is called by | [`0x00233AD0`](../Enemy-Spawning/spawn-record-fields.md) Battle unit: activate applied definition runtime (on spawn record fields)<br>[`0x00233D70`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00233EA0`](../Characters-And-Objects/battle-units.md) (on battle units)<br>[`0x00233F70`](../Enemy-Spawning/enemy-respawning.md) Battle unit: update lifecycle and combat frame (on enemy respawning)<br>[`0x00234200`](../Characters-And-Objects/battle-units.md) Actor system: release battle unit slot for actor (on battle units)<br>[`0x00234D40`](../Characters-And-Objects/battle-units.md) (on battle units)<br>[`0x00237D80`](../Characters-And-Objects/battle-units.md) (on battle units)<br>[`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction)<br>[`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) |
| [`0x0031A300`](../Menus-And-HUD/status-and-equip-screen.md) Battle stats: clear all equipment slots by mapped id (on status and equip screen) | calls | [`0x00236820`](equipping-an-item.md) |
| [`0x00324380`](equipping-an-item.md) | calls | [`0x00236820`](equipping-an-item.md) |
| [`0x00324470`](equipping-an-item.md) | calls | [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn |
| [`0x0037CA80`](equipping-an-item.md) | calls | [`0x00233CF0`](../Engine-Core/party-control-modes.md) (on party control modes) |

**Enemy AI and gambits** (explained on [glossary](../Engine-Core/glossary.md), [gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md), [frame update order](../Engine-Core/frame-update-order.md), [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md), [gambits](../Enemy-AI-And-Gambits/gambits.md), [force fight mode](../Engine-Core/force-fight-mode.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](equipping-an-item.md) | is called by | [`0x00301AD0`](../Enemy-AI-And-Gambits/enemy-order-sets.md) Ai order: evaluate target selector (on enemy order sets)<br>[`0x00308C20`](../Enemy-AI-And-Gambits/enemy-order-sets.md) Ai order: compute bounded selector scalar (on enemy order sets)<br>[`0x003219D0`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: propagate to perceiving foes (on enmity)<br>[`0x003247F0`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle unit: rebuild perception candidate cache (on enemy ai)<br>[`0x00324F20`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle perception: refresh candidate cache generation (on enemy ai) |
| [`0x00283270`](../Menus-And-HUD/menu-screens.md) (on menu screens) | calls | [`0x00327BE0`](../Menus-And-HUD/menu-screens.md) Gambit config: copy base pair set for stats index (on menu screens) |
| [`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action | is called by | [`0x00308610`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) Battle unit: update combat frame (on heading speed to position delta) |
| [`0x00313F60`](equipping-an-item.md) | is called by | [`0x00321850`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: write for combatant id (on enmity)<br>[`0x00321B00`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: adjust other relevant combatants (on enmity)<br>[`0x00321D30`](../Enemy-AI-And-Gambits/enmity.md) Battle enmity: write all combatant ids (on enmity)<br>[`0x003247F0`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle unit: rebuild perception candidate cache (on enemy ai)<br>[`0x00324F20`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle perception: refresh candidate cache generation (on enemy ai) |

**Battle actions** (explained on [party control modes](../Engine-Core/party-control-modes.md), [gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md), [identifier spaces](../Engine-Core/identifier-spaces.md), [frame update order](../Engine-Core/frame-update-order.md), [enemy spawning](../Enemy-Spawning/enemy-spawning.md), [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md), [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [animation driven movement](../Movement-And-Pathfinding/animation-driven-movement.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](equipping-an-item.md) | is called by | [`0x00306760`](../Party/party-table.md) Battle action: update special presentation sequence (on party table)<br>[`0x003083B0`](../Enemy-AI-And-Gambits/gambit-conditions.md) Battle action: check target eligibility (on gambit conditions)<br>[`0x0030F760`](../Engine-Core/identifier-spaces.md) Battle unit: commit action (on identifier spaces)<br>[`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action |
| [`0x002ECF10`](equipping-an-item.md) | is called by | [`0x002FED60`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning) |
| [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn | calls | [`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action |
| [`0x0030FED0`](equipping-an-item.md) Battle stats: recompute derived state and auto statuses | is called by | [`0x002FDDA0`](../Battle-Actions/battle-orders.md) Battle unit: execute direct state command order (on battle orders) |
| [`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action | calls | [`0x00300280`](../Rewards-EXP-Gil-And-Loot/gil.md) Battle action: refund reserved execution resources (on gil)<br>[`0x0030C970`](../Battle-Actions/action-phases.md) (on action phases)<br>[`0x00310780`](../Battle-Actions/action-commit.md) Battle unit: release target relation and action state (on action commit) |
| [`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action | is called by | [`0x0030F760`](../Engine-Core/identifier-spaces.md) Battle unit: commit action (on identifier spaces) |
| [`0x00313F60`](equipping-an-item.md) | is called by | [`0x00319F50`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: handle actor timeline event (on ko and game over)<br>[`0x00323350`](../Movement-And-Pathfinding/animation-driven-movement.md) Battle action: apply knockback impulse (on animation driven movement)<br>[`0x00325260`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: handle action timeline event (on ko and game over) |
| [`0x00324470`](equipping-an-item.md) | calls | [`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action |

**Damage and battle formulas** (explained on [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [force fight mode](../Engine-Core/force-fight-mode.md), [traps](../World-Areas-And-Travel/traps.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](equipping-an-item.md) | is called by | [`0x0031B860`](../Battle-Actions/battle-log.md) Battle stats: find owning battle unit (on battle log)<br>[`0x0031E800`](../Enemy-AI-And-Gambits/enemy-order-sets.md) Battle stats: get owning actor handle (on enemy order sets) |
| [`0x0030FED0`](equipping-an-item.md) Battle stats: recompute derived state and auto statuses | calls | [`0x002FEF30`](../Enemy-Spawning/bestiary.md) Battle stats: rebuild effective stats and affinity state (on bestiary)<br>[`0x0031B860`](../Battle-Actions/battle-log.md) Battle stats: find owning battle unit (on battle log) |
| [`0x0030FED0`](equipping-an-item.md) Battle stats: recompute derived state and auto statuses | is called by | [`0x003112F0`](../Rewards-EXP-Gil-And-Loot/gil.md) Battle formula: apply target result (on gil) |
| [`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action | is called by | [`0x002FEF30`](../Enemy-Spawning/bestiary.md) Battle stats: rebuild effective stats and affinity state (on bestiary) |
| [`0x00313F60`](equipping-an-item.md) | is called by | [`0x00384F40`](../Battle-Actions/action-results.md) (on action results) |
| [`0x0031A510`](equipment.md) Battle stats: set equipment slot by mapped id (on equipment) | calls | [`0x0031B860`](../Battle-Actions/battle-log.md) Battle stats: find owning battle unit (on battle log) |

**Gameplay** (explained on [enmity](../Enemy-AI-And-Gambits/enmity.md), [identifier spaces](../Engine-Core/identifier-spaces.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [battle units](../Characters-And-Objects/battle-units.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](equipping-an-item.md) | is called by | [`0x0030C210`](../Enemy-AI-And-Gambits/enmity.md) Battle unit: has relationship class2 plus in slot mask (on enmity) |
| [`0x0030FED0`](equipping-an-item.md) Battle stats: recompute derived state and auto statuses | calls | [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) |
| [`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action | calls | [`0x00316CF0`](../Enemy-AI-And-Gambits/gambits.md) Battle target buffer: reset preserving flag0 (on gambits) |
| [`0x00313F60`](equipping-an-item.md) | is called by | [`0x003176E0`](../Battle-Actions/area-of-effect.md) Battle: emit reaction presentation for slot (on area of effect)<br>[`0x003257D0`](equipping-an-item.md) |
| [`0x00317930`](equipping-an-item.md) Equipment: check item eligible for slot | calls | [`0x00309EC0`](../Enemy-AI-And-Gambits/gambit-conditions.md) (on gambit conditions)<br>[`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) |
| [`0x0031A510`](equipment.md) Battle stats: set equipment slot by mapped id (on equipment) | calls | [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) |
| [`0x00323C60`](equipping-an-item.md) Battle stats: has required license for equipment | calls | [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) |

**Controls and input** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00313F60`](equipping-an-item.md) | is called by | [`0x00253C70`](../Controls-And-Input/controls.md) (on controls) |

**Movement and pathfinding** (explained on [party slots](../Party/party-slots.md), [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md), [bestiary](../Enemy-Spawning/bestiary.md), [force fight mode](../Engine-Core/force-fight-mode.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [action phases](../Battle-Actions/action-phases.md), [game over](../World-Areas-And-Travel/game-over.md), [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md), [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](equipping-an-item.md) | is called by | [`0x00326D60`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x003278D0`](../World-Areas-And-Travel/doors-gates-and-map-changes.md) (on doors gates and map changes)<br>[`0x003357B0`](../Movement-And-Pathfinding/battle-locomotion.md) Battle locomotion: query dynamic actor obstruction (on battle locomotion)<br>[`0x00336710`](../Movement-And-Pathfinding/battle-locomotion.md) Battle locomotion: build solver context (on battle locomotion)<br>[`0x003377C0`](../Rewards-EXP-Gil-And-Loot/loot-pickups.md) (on loot pickups)<br>[`0x00338140`](../Battle-Actions/action-range.md) Battle locomotion: resolve target spacing and avoidance (on action range)<br>[`0x00338490`](../Party/party-leader.md) Party follow: solve formation (on party leader)<br>[`0x0033C310`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x0033CEF0`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x0033D200`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion) |
| [`0x002ECEC0`](equipping-an-item.md) | is called by | [`0x0026C3E0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze) |
| [`0x002ECF10`](equipping-an-item.md) | is called by | [`0x00345430`](../Scripts-And-Script-Commands/verb-table.md) (on verb table) |
| [`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action | calls | [`0x003291B0`](../Battle-Actions/battle-orders.md) Battle locomotion: reset path and set targets (on battle orders)<br>[`0x0033C9B0`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion) |
| [`0x00313F60`](equipping-an-item.md) | is called by | [`0x0031BAC0`](../Party/party-slots.md) (on party slots)<br>[`0x00326D60`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x00329A80`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x003911D0`](../Battle-Actions/weapon-motion-list.md) (on weapon motion list) |

**Party** (explained on [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [party control modes](../Engine-Core/party-control-modes.md), [battle orders](../Battle-Actions/battle-orders.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [frame update order](../Engine-Core/frame-update-order.md), [party data](../Party/party-data.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](equipping-an-item.md) | is called by | [`0x003261D0`](../Party/party-members.md) Party configuration: reconcile roster from current selectors (on party members)<br>[`0x003273D0`](../Party/party-members.md) Party configuration: set selectors and reconcile roster (on party members) |
| [`0x00283270`](../Menus-And-HUD/menu-screens.md) (on menu screens) | is called by | [`0x00328BD0`](../Scripts-And-Script-Commands/reward-verbs.md) (on reward verbs) |
| [`0x002ECF10`](equipping-an-item.md) | is called by | [`0x00313400`](../Battle-Actions/battle-orders.md) Battle unit: enter party combat stance (on battle orders)<br>[`0x00313480`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs) |
| [`0x0030FED0`](equipping-an-item.md) Battle stats: recompute derived state and auto statuses | is called by | [`0x00328BD0`](../Scripts-And-Script-Commands/reward-verbs.md) (on reward verbs) |
| [`0x00313F60`](equipping-an-item.md) | is called by | [`0x0023B040`](../Engine-Core/party-control-modes.md) Party control: recompute suppression from leader battle state (on party control modes)<br>[`0x0031AC00`](../Party/party-data.md) (on party data) |
| [`0x0037B4B0`](equipping-an-item.md) | is called by | [`0x003261D0`](../Party/party-members.md) Party configuration: reconcile roster from current selectors (on party members)<br>[`0x003273D0`](../Party/party-members.md) Party configuration: set selectors and reconcile roster (on party members) |
| [`0x0037CA80`](equipping-an-item.md) | is called by | [`0x003261D0`](../Party/party-members.md) Party configuration: reconcile roster from current selectors (on party members)<br>[`0x003273D0`](../Party/party-members.md) Party configuration: set selectors and reconcile roster (on party members) |

**Steam and achievements** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00283270`](../Menus-And-HUD/menu-screens.md) (on menu screens) | is called by | [`0x00316930`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Graphics** (explained on [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [battle units](../Characters-And-Objects/battle-units.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002E42D0`](equipping-an-item.md) | calls | [`0x00427280`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs) |
| [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn | calls | [`0x003125E0`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: compute presentation suppression mask (on ko and game over) |

**Rewards: EXP, LP, gil and loot** (explained on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0030FED0`](equipping-an-item.md) Battle stats: recompute derived state and auto statuses | is called by | [`0x0030C470`](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md) (on stat growth per level)<br>[`0x0030C650`](../Menus-And-HUD/hud.md) Battle stats: advance level to target and recompute growth (on hud) |

**Saving, loading and settings** (explained on [game application](../Engine-Core/game-application.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00283270`](../Menus-And-HUD/menu-screens.md) (on menu screens) | is called by | [`0x00582860`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen)<br>[`0x005844A0`](../Saving-Loading-And-Settings/save-data-fields.md) Save transition: prepare runtime image for capture (on save data fields) |

**Scripts and script commands** (explained on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [party control modes](../Engine-Core/party-control-modes.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002E42D0`](equipping-an-item.md) | is called by | [`0x0034C730`](equipping-an-item.md)<br>[`0x00351000`](equipping-an-item.md) |
| [`0x002ECF10`](equipping-an-item.md) | is called by | [`0x00343290`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00344CC0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x00345CD0`](../Graphics/presentation-entries.md) (on presentation entries)<br>[`0x003460C0`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00346620`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00346A10`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00346EB0`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x003473E0`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00347970`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00357F00`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs) |
| [`0x0037CA80`](equipping-an-item.md) | is called by | [`0x0034E1F0`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild) |

**Enemy spawning** (explained on [battle units](../Characters-And-Objects/battle-units.md), [enemy respawning](../Enemy-Spawning/enemy-respawning.md), [frame update order](../Engine-Core/frame-update-order.md), [boss fights](../Battle-Actions/boss-fights.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [enemy spawning](../Enemy-Spawning/enemy-spawning.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](equipping-an-item.md) | is called by | [`0x00308D90`](../Enemy-Spawning/enemy-spawning.md) Spawn: count active cap tracked actors (on enemy spawning) |
| [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn | calls | [`0x00237080`](../Enemy-Spawning/spawn-record-fields.md) Spawn entry: clear selection transient state for teardown (on spawn record fields) |
| [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn | is called by | [`0x00234880`](../Battle-Actions/boss-fights.md) Spawn group: teardown all grouped spawn units (on boss fights)<br>[`0x00234990`](../Enemy-Spawning/enemy-respawning.md) Spawn group: teardown units by group mask (on enemy respawning)<br>[`0x002350C0`](../Enemy-Spawning/enemy-spawning.md) Spawn lifecycle: check and retire by native range (on enemy spawning)<br>[`0x00237690`](../Battle-Actions/boss-fights.md) Spawn group: teardown all ungrouped spawn units (on boss fights) |
| [`0x0030FED0`](equipping-an-item.md) Battle stats: recompute derived state and auto statuses | is called by | [`0x0023A410`](../Enemy-Spawning/spawn-record-fields.md) Spawn unit: finalize spawn entry activation (on spawn record fields) |
| [`0x00313F60`](equipping-an-item.md) | is called by | [`0x00234DA0`](../Party/party-slots.md) Spawn: validate candidate distance to players (on party slots)<br>[`0x002350C0`](../Enemy-Spawning/enemy-spawning.md) Spawn lifecycle: check and retire by native range (on enemy spawning) |

**Status effects and KO** (explained on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [force fight mode](../Engine-Core/force-fight-mode.md), [battle orders](../Battle-Actions/battle-orders.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [frame update order](../Engine-Core/frame-update-order.md), [battle unit fields](../Characters-And-Objects/battle-unit-fields.md), [mp](../Status-Effects-And-KO/mp.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002ECF10`](equipping-an-item.md) | is called by | [`0x00301140`](../Graphics/effect-file-loading.md) Battle unit: recover from terminal status set if clear (on effect file loading) |
| [`0x0030FED0`](equipping-an-item.md) Battle stats: recompute derived state and auto statuses | calls | [`0x0030E130`](../Status-Effects-And-KO/battle-buffs.md) Battle stats: modify status layer state and process side effects (on battle buffs)<br>[`0x0030E360`](../Engine-Core/identifier-spaces.md) Battle stats: change status and process side effects (on identifier spaces) |
| [`0x0030FED0`](equipping-an-item.md) Battle stats: recompute derived state and auto statuses | is called by | [`0x0030E130`](../Status-Effects-And-KO/battle-buffs.md) Battle stats: modify status layer state and process side effects (on battle buffs)<br>[`0x0030E360`](../Engine-Core/identifier-spaces.md) Battle stats: change status and process side effects (on identifier spaces)<br>[`0x0030E8F0`](../Damage-And-Battle-Formulas/augments.md) (on augments)<br>[`0x0030F690`](../Damage-And-Battle-Formulas/augments.md) Battle stats: remove statuses from mask and recompute (on augments) |
| [`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action | is called by | [`0x00300140`](../Status-Effects-And-KO/status-changes.md) Battle unit: reset action control for status transition (on status changes)<br>[`0x00301140`](../Graphics/effect-file-loading.md) Battle unit: recover from terminal status set if clear (on effect file loading) |
| [`0x00313F60`](equipping-an-item.md) | is called by | [`0x00320450`](../Status-Effects-And-KO/mp.md) Battle unit: take and clear primary resource recovery accumulator (on mp)<br>[`0x00329A20`](../Status-Effects-And-KO/mp.md) Battle unit: add primary resource recovery accumulator (on mp) |
| [`0x0031A510`](equipment.md) Battle stats: set equipment slot by mapped id (on equipment) | calls | [`0x0030FED0`](equipping-an-item.md) Battle stats: recompute derived state and auto statuses |

**Story, events and hunts** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00283E40`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) | calls | [`0x0032A8A0`](../World-Areas-And-Travel/zone-asset-list.md) Persistent flag: query primary or authored threshold gate (on zone asset list) |

**Menus and HUD** (explained on [action definition row](../Battle-Actions/action-definition-row.md), [target selection](../Battle-Actions/target-selection.md), [license board screen](../Menus-And-HUD/license-board-screen.md), [menu screens](../Menus-And-HUD/menu-screens.md), [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md), [ui typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md), [stats](../Damage-And-Battle-Formulas/stats.md), [controls](../Controls-And-Input/controls.md), [as7 menu graphics](../Game-Files-And-Data-Tables/as7-menu-graphics.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](equipping-an-item.md) | is called by | [`0x0031EB20`](../Battle-Actions/action-definition-row.md) Battle menu: build command entry list (on action definition row)<br>[`0x00322A80`](../Battle-Actions/target-selection.md) (on target selection) |
| [`0x0027F210`](equipping-an-item.md) | is called by | [`0x0027EDA0`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x0027F430`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x00285F20`](../Menus-And-HUD/menu-screens.md) (on menu screens) |
| [`0x00283270`](../Menus-And-HUD/menu-screens.md) (on menu screens) | is called by | [`0x00281AE0`](../Game-Files-And-Data-Tables/binmenu-images.md) (on binmenu images)<br>[`0x002D70F0`](../Menus-And-HUD/menu-screens.md) (on menu screens) |
| [`0x00283840`](equipping-an-item.md) | is called by | [`0x00560910`](../Game-Files-And-Data-Tables/battle-text-tables.md) (on battle text tables) |
| [`0x00283E40`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) | calls | [`0x0029F6E0`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x00556380`](../Controls-And-Input/on-screen-keyboard.md) (on on screen keyboard) |
| [`0x00313F60`](equipping-an-item.md) | is called by | [`0x0031EB20`](../Battle-Actions/action-definition-row.md) Battle menu: build command entry list (on action definition row)<br>[`0x00322A80`](../Battle-Actions/target-selection.md) (on target selection) |
| [`0x003FF360`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) | calls | [`0x00291D70`](../Compiler-And-C-Runtime/generated-function-families.md) (on generated function families)<br>[`0x002C1A80`](../Menus-And-HUD/menu-screens.md) (on menu screens) |
| [`0x003FFA20`](equipping-an-item.md) | calls | [`0x0027F210`](equipping-an-item.md) |

**World, areas and travel** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00313F60`](equipping-an-item.md) | is called by | [`0x00234590`](../Battle-Actions/quickenings-and-summons.md) Battle system: run field frame orchestrator (on quickenings and summons) |
| [`0x00324470`](equipping-an-item.md) | calls | [`0x00313F60`](equipping-an-item.md) |

</details>

---

[← Equipment](equipment.md) | [Licenses →](licenses.md)
