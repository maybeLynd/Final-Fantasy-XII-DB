[Home](../../README.md) / [Items, equipment, shops and licenses](README.md) / Equipping an item

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Equipping an item: the steps from picking a piece in the equip menu to the rebuilt stats | operation | Items, equipment, shops and licenses | Equipment | The order in which the game equips one piece from the equip menu: the list and its refusal marks, the setter, the eligibility test and the license test, the worn copy moved from the old piece to the new, the hands reconciled, the stats rebuilt and the unit refreshed, and when the setter reloads the fighting units' models; with what happens for a refused piece, a two-handed weapon, a shield, ammunition and taking a piece off, each step linked to the page that explains it. | 0x003FF360, 0x003FFA20, 0x0031A510, 0x00317930, 0x00323C60, 0x00318B40, 0x0030FED0, 0x00324470, 0x00324380 |

## What the player sees

In the equip menu the player picks a slot and a piece from its list. Pieces the character cannot wear are marked,
and the stat rows show the new values next to the current ones. After the choice the piece is worn and the stats
change.

## Steps

1. **The list.** The equip pane `0x003FF360` shows the five slots, the pieces for the chosen slot and the stat rows;
   a piece the character cannot wear is marked, and so is ammunition that does not match the weapon
   ([equipment](equipment.md#the-equip-screen)).
2. **The setter.** Choosing a piece runs `0x003FFA20(slot, id)`, which calls the party-seat setter
   `0x0031A510(member, slot, id, 1)` ([equipment](equipment.md#who-equips),
   [equipment](equipment.md#the-setters)).
   - `member` is `0x00282EA0` of the menu block's word `+0xDE0` (`0x003FFA35`-`0x003FFA4F`). `0x003FFA20` then refreshes
     the menu: `0x00283270(0)`, `0x0027F210`, which fills the five equipment rows, `0x003FEAD0(0)`, `0x00283E40` on
     `[[0x0209AC30] + 0x130] + 0xC0` when `+0x130` is set, `0x002858A0(0, 0)` and last `0x00283840(1)`
     (`0x003FFA54`-`0x003FFAA0`).
3. **The eligibility test.** `0x00317930` checks, in order, the slot, a free copy, the slot bits of the piece's row,
   the pairing with the main hand, the party row's class mask and then the license test `0x00323C60`
   ([equipment](equipment.md#can-it-be-worn), [equipment row](equipment-row.md)).
4. **The license test.** The requirement mask for the piece is built from the license node table and compared
   with the member's owned-square bits; owning any square that lists the piece is enough
   ([licenses](licenses.md#the-test), [License Board](license-board.md)).
5. **The worn copy.** One worn copy moves from the old piece to the new one in the inventory
   ([equipment](equipment.md#the-setters), [inventory](inventory.md#changing-the-inventory)).
6. **The store.** The id is written to the member record's slot word
   ([equipment](equipment.md#the-slot-words), [unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)).
7. **The hands.** `0x00318B40` reconciles the main hand and the off hand: an empty main hand becomes Unarmed, and a
   pairing that no longer holds empties the off hand or unarms the main hand
   ([equipment](equipment.md#the-two-hands)).
8. **The stats.** When the slot's word has changed, `0x0030FED0(record, 0x97)` rebuilds the stats and augments, and
   `0x00324470` refreshes the unit ([equipment](equipment.md#the-setters),
   [stats](../Damage-And-Battle-Formulas/stats.md#the-rebuild),
   [augments](../Damage-And-Battle-Formulas/augments.md#the-rebuild)).
   - `0x00324470(unit)` calls `0x002ECF10(actor, b, 0)`, the actor being the unit's `+0x10` and `b` its flag bit
     `0x800000` as 0 or 1, and the action reset `0x003105D0(unit)` (`0x00324476`-`0x00324490`). It tears the unit down
     with `0x00300E40(unit, 0)` when it has no stats record `+0x698`, or one with KO, Stone or X-Zone (`0x80000003`)
     outside a town (`0x00313F60`), unless unit flag bit `0x2` is set (`0x00324495`-`0x003244C1`).
   - Then it calls `0x002E42D0`, `0x002699D0` and `0x002ECEC0` on the actor `+0x10` and sets unit flag bit `0x40`
     (`0x003244C6`-`0x003244E1`).
9. **The model.** With `flags` bit `0x1` clear, `0x0031A510` then re-records the fighting units and reloads their models
   through `0x00324380`, which runs the model rebuild for slots 0 to 3; the equip menu and the shop pass `flags` 1,
   so their setter call does not reload ([equipment](equipment.md#the-setters),
   [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md#what-runs-it)).

`0x00324380` takes the units of slots 0 to 3 (`0x00236820`). For each unit it calls `0x0037B4B0` on `[unit + 0x10]` when
that is non-null, and records at `0x022C257C + slot` the row byte `+4` of the stats record `[unit + 0x698]` when unit
flag bit `0x4` is set, or `0xFF` for no unit or a clear bit (`0x00324398`-`0x003243D6`). It then jumps to the model
read-in `0x0037CA80` (`0x003243E7`). The stats record is read with no null test (`0x003243BA`-`0x003243C1`), so a unit with
bit `0x4` set and a null `+0x698` faults there.

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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x00236820` is called by `0x0031B770`, `0x00321170`; `0x002699D0` calls `0x003587C0`; `0x002699D0` is called by
  `0x003266C0`, `0x0037B4D0`; `0x002E42D0` is called by `0x003266C0`, `0x0037B4D0`; `0x002ECEC0` is called by `0x003266C0`;
  `0x002ECF10` is called by `0x003266C0`; `0x00300E40` calls `0x0023A570`, `0x0025AB30`, `0x002697E0`, `0x00300FC0`, `0x00322050`.
- Actor entity: `0x00300E40` is called by `0x00233EA0`, `0x00233F70`, `0x002348E0`, `0x003266C0`; `0x003105D0` calls `0x00236820`,
  `0x00236850`; `0x003105D0` is called by `0x00236A60`, `0x00300E40`, `0x00300FC0`, `0x003266C0`; `0x00313F60` is called by
  `0x00233AD0`, `0x00233D70`, `0x00233EA0`, `0x00233F70`, `0x00234200`, `0x00234D40`, `0x00237D80`, `0x0023A570`, `0x003266C0`;
  `0x0031A300` calls `0x00236820`; `0x00324380` calls `0x00236820`.
- Actor entity: `0x00324470` calls `0x00300E40`; `0x0037CA80` calls `0x00233CF0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [enemy respawning](../Enemy-Spawning/enemy-respawning.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [party control modes](../Engine-Core/party-control-modes.md).
- Actor entity: and on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md),
  [native commands](../Scripts-And-Script-Commands/native-commands.md),
  [ko and game over](../Status-Effects-And-KO/ko-and-game-over.md),
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md).
- Actor entity: and on [battle units](../Characters-And-Objects/battle-units.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md),
  [actor record](../Characters-And-Objects/actor-record.md).
- Combat AI: `0x00236820` is called by `0x00301AD0`, `0x00308C20`, `0x003219D0`, `0x003247F0`, `0x00324F20`; `0x00283270` calls
  `0x00327BE0`; `0x003105D0` is called by `0x00308610`; `0x00313F60` is called by `0x00321850`, `0x00321B00`, `0x00321D30`,
  `0x003247F0`, `0x00324F20`.
- Combat AI: those functions are documented on [glossary](../Engine-Core/glossary.md),
  [gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md), [gambits](../Enemy-AI-And-Gambits/gambits.md).
- Combat AI: and on [force fight mode](../Engine-Core/force-fight-mode.md),
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md).
- Combat action: `0x00236820` is called by `0x00306760`, `0x003083B0`, `0x0030F760`, `0x003105D0`; `0x002ECF10` is called by
  `0x002FED60`; `0x00300E40` calls `0x003105D0`; `0x0030FED0` is called by `0x002FDDA0`; `0x003105D0` calls `0x00300280`,
  `0x0030C970`, `0x00310780`; `0x003105D0` is called by `0x0030F760`; `0x00313F60` is called by `0x00319F50`, `0x00323350`,
  `0x00325260`; `0x00324470` calls `0x003105D0`.
- Combat action: those functions are documented on
  [party control modes](../Engine-Core/party-control-modes.md),
  [gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md),
  [identifier spaces](../Engine-Core/identifier-spaces.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Combat action: and on [enemy spawning](../Enemy-Spawning/enemy-spawning.md),
  [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md),
  [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- Combat action: and on [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [animation driven movement](../Movement-And-Pathfinding/animation-driven-movement.md),
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Combat formula: `0x00236820` is called by `0x0031B860`, `0x0031E800`; `0x0030FED0` calls `0x002FEF30`, `0x0031B860`; `0x0030FED0`
  is called by `0x003112F0`; `0x003105D0` is called by `0x002FEF30`; `0x00313F60` is called by `0x00384F40`; `0x0031A510` calls
  `0x0031B860`.
- Combat formula: those functions are documented on
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md),
  [force fight mode](../Engine-Core/force-fight-mode.md), [traps](../World-Areas-And-Travel/traps.md),
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md).
- Gameplay: `0x00236820` is called by `0x0030C210`; `0x0030FED0` calls `0x00322C50`; `0x003105D0` calls `0x00316CF0`; `0x00313F60`
  is called by `0x003176E0`, `0x003257D0`; `0x00317930` calls `0x00309EC0`, `0x00322C50`; `0x0031A510` calls `0x00322C50`;
  `0x00323C60` calls `0x00322C50`.
- Gameplay: those functions are documented on [enmity](../Enemy-AI-And-Gambits/enmity.md),
  [identifier spaces](../Engine-Core/identifier-spaces.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [battle units](../Characters-And-Objects/battle-units.md);
  and on [item and ability ids](../Engine-Core/item-and-ability-ids.md).
- Input: `0x00313F60` is called by `0x00253C70`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Movement: `0x00236820` is called by `0x00326D60`, `0x003278D0`, `0x003357B0`, `0x00336710`, `0x003377C0`, `0x00338140`,
  `0x00338490`, `0x0033C310`, `0x0033CEF0`, `0x0033D200`; `0x002ECEC0` is called by `0x0026C3E0`; `0x002ECF10` is called by
  `0x00345430`; `0x003105D0` calls `0x003291B0`, `0x0033C9B0`; `0x00313F60` is called by `0x0031BAC0`, `0x00326D60`, `0x00329A80`,
  `0x003911D0`.
- Movement: those functions are documented on [party slots](../Party/party-slots.md),
  [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md),
  [bestiary](../Enemy-Spawning/bestiary.md),
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Movement: and on [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [action phases](../Battle-Actions/action-phases.md), [game over](../World-Areas-And-Travel/game-over.md).
- Movement: and on [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md),
  [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md).
- Party: `0x00236820` is called by `0x003261D0`, `0x003273D0`; `0x00283270` is called by `0x00328BD0`; `0x002ECF10` is called by
  `0x00313400`, `0x00313480`; `0x0030FED0` is called by `0x00328BD0`; `0x00313F60` is called by `0x0023B040`, `0x0031AC00`;
  `0x0037B4B0` is called by `0x003261D0`, `0x003273D0`; `0x0037CA80` is called by `0x003261D0`, `0x003273D0`.
- Party: those functions are documented on [party verbs](../Scripts-And-Script-Commands/party-verbs.md),
  [party control modes](../Engine-Core/party-control-modes.md),
  [battle orders](../Battle-Actions/battle-orders.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- Party: and on [frame update order](../Engine-Core/frame-update-order.md),
  [party data](../Party/party-data.md).
- Platform online achievements: `0x00283270` is called by `0x00316930`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Presentation: `0x002E42D0` calls `0x00427280`; `0x00300E40` calls `0x003125E0`; those functions are documented on
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [battle units](../Characters-And-Objects/battle-units.md).
- Rewards progression economy: `0x0030FED0` is called by `0x0030C470`, `0x0030C650`; those functions are documented on
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- Save load settings: `0x00283270` is called by `0x00582860`, `0x005844A0`; those functions are documented on
  [game application](../Engine-Core/game-application.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md).
- Script VM: `0x002E42D0` is called by `0x0034C730`, `0x00351000`; `0x002ECF10` is called by `0x00343290`, `0x00344CC0`,
  `0x00345CD0`, `0x003460C0`, `0x00346620`, `0x00346A10`, `0x00346EB0`, `0x003473E0`, `0x00347970`, `0x00357F00`; `0x0037CA80` is called
  by `0x0034E1F0`.
- Script VM: those functions are documented on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [party control modes](../Engine-Core/party-control-modes.md).
- Spawn encounter lifecycle: `0x00236820` is called by `0x00308D90`; `0x00300E40` calls `0x00237080`; `0x00300E40` is called by
  `0x00234880`, `0x00234990`, `0x002350C0`, `0x00237690`; `0x0030FED0` is called by `0x0023A410`; `0x00313F60` is called by
  `0x00234DA0`, `0x002350C0`.
- Spawn encounter lifecycle: those functions are documented on [battle units](../Characters-And-Objects/battle-units.md),
  [enemy respawning](../Enemy-Spawning/enemy-respawning.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [boss fights](../Battle-Actions/boss-fights.md).
- Spawn encounter lifecycle: and on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [enemy spawning](../Enemy-Spawning/enemy-spawning.md).
- Status periodic terminal: `0x002ECF10` is called by `0x00301140`; `0x0030FED0` calls `0x0030E130`, `0x0030E360`; `0x0030FED0` is
  called by `0x0030E130`, `0x0030E360`, `0x0030E8F0`, `0x0030F690`; `0x003105D0` is called by `0x00300140`, `0x00301140`; `0x00313F60`
  is called by `0x00320450`, `0x00329A20`; `0x0031A510` calls `0x0030FED0`.
- Status periodic terminal: those functions are documented on
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [battle orders](../Battle-Actions/battle-orders.md),
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
- Status periodic terminal: and on [frame update order](../Engine-Core/frame-update-order.md),
  [battle unit fields](../Characters-And-Objects/battle-unit-fields.md), [mp](../Status-Effects-And-KO/mp.md).
- Story event quest hunt: `0x00283E40` calls `0x0032A8A0`; those functions are documented on
  [identifier spaces](../Engine-Core/identifier-spaces.md).
- UI: `0x00236820` is called by `0x0031EB20`, `0x00322A80`; `0x0027F210` is called by `0x0027EDA0`, `0x0027F430`, `0x00285F20`;
  `0x00283270` is called by `0x00281AE0`, `0x002D70F0`; `0x00283840` is called by `0x00560910`; `0x00283E40` calls `0x0029F6E0`,
  `0x00556380`; `0x00313F60` is called by `0x0031EB20`, `0x00322A80`; `0x003FF360` calls `0x00291D70`, `0x002C1A80`; `0x003FFA20`
  calls `0x0027F210`.
- UI: those functions are documented on [action definition row](../Battle-Actions/action-definition-row.md),
  [target selection](../Battle-Actions/target-selection.md),
  [license board screen](../Menus-And-HUD/license-board-screen.md), [menu screens](../Menus-And-HUD/menu-screens.md).
- UI: and on [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md),
  [ui typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md).
- UI: and on [stats](../Damage-And-Battle-Formulas/stats.md), [controls](../Controls-And-Input/controls.md),
  [as7 menu graphics](../Game-Files-And-Data-Tables/as7-menu-graphics.md).
- World area: `0x00313F60` is called by `0x00234590`; `0x00324470` calls `0x00313F60`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [frame update order](../Engine-Core/frame-update-order.md).

---

[← Equipment](equipment.md) | [Licenses →](licenses.md)
