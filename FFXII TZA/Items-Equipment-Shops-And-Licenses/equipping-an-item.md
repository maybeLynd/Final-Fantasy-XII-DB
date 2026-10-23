---
title: "Equipping an item: the steps from picking a piece in the equip menu to the rebuilt stats"
kind: "operation"
category: "Items, equipment, shops and licenses"
addresses: "0x003FF360, 0x003FFA20, 0x0031A510, 0x00317930, 0x00323C60, 0x00318B40, 0x0030FED0, 0x00324470, 0x00324380"
---

## What the player sees

In the equip menu the player picks a slot and a piece from its list. Pieces the character cannot wear are marked,
and the stat rows show the new values next to the current ones. After the choice the piece is worn and the stats
change.

## Steps

1. **The list.** The equip pane `0x003FF360` shows the five slots, the pieces for the chosen slot and the stat rows;
   a piece the character cannot wear is marked, and so is ammunition that does not match the weapon
   ([equipment](equipment.md#the-equip-screen)).
2. **The setter.** Choosing a piece runs `0x003FFA20`, which calls the party-seat setter
   `0x0031A510(member, slot, id, 1)` ([equipment](equipment.md#who-equips),
   [equipment](equipment.md#the-setters)).
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
   `0x00324470` refreshes the unit ([equipment](equipment.md#the-setters), [stats](../Damage-And-Battle-Formulas/stats.md#the-rebuild),
   [augments](../Damage-And-Battle-Formulas/augments.md#the-rebuild)).
9. **The model.** With `flags` bit 0 clear, `0x0031A510` then re-records the fighting units and reloads their models
   through `0x00324380`, which runs the model rebuild for slots 0 to 3; the equip menu and the shop pass `flags` 1,
   so their setter call does not reload ([equipment](equipment.md#the-setters),
   [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md#what-runs-it)).

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
