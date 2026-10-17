---
title: "Using an item: how a Potion is an action that costs an item, when the item is taken, given back or kept, and why enemies never spend items"
kind: "system"
category: "Items, equipment, shops and licenses"
addresses: "0030EF20, 00305640, 00300280, 003105D0, 00309060"
---

## What the player sees

- Using a Potion takes one from the inventory as soon as the character starts the action, before it charges.
- If the action is cancelled before it goes off, the Potion comes back.
- Enemies can use items without having or spending any; guests spend the party's items like members do.

## How it works

### An item is an action

Every usable item is an action row ([Action definition row](../Battle-Actions/action-definition-row.md)). A row
whose kind byte `+1E`<sub>h</sub> is 3 is an item action, and its word `+22`<sub>h</sub> is the item it uses. What the item does,
whom it targets and how it looks are the rest of the row, handled like any other action.

### Taking the item

`0030EF20(unit, row)` runs when the action starts, phase 0 of the action ([Action phases](../Battle-Actions/action-phases.md);
`00304962`). It does nothing for a unit without a stats record or whose record is not a party record, byte `+5`
not 0 (`0030EF60`-`0030EF77`). Otherwise:

1. The item id is the row's `+22`<sub>h</sub> for a kind-3 row and `FFFF`<sub>h</sub> otherwise; it is kept at unit `+DC8`<sub>h</sub>, the
   reserved item (`0030EF79`-`0030EF93`).
2. A reserved item is taken from the inventory at once, `003008A0(item, -1, 0, 1, 0)` (`0030EF9A`-`0030EFB0`,
   [Inventory](inventory.md)).
3. The action's gil cost, `00309060`, is kept at unit `+E58`<sub>h</sub> and taken from the gil, floored at 0
   (`0030EFBB`-`0030EFD8`), through `00253690` and `00254EE0` ([Gil](../Rewards-EXP-Gil-And-Loot/gil.md)). Only actions paid in gil have one: `00309060` returns 0 for an enemy record, for an
   action id above `21E`<sub>h</sub> and for rows of kind 5 or 6 ([MP gain and cost](../Status-Effects-And-KO/mp.md)).

### Keeping it spent

`00305640(unit, row, flag)` runs when the action goes off. For a party unit it clears both reservations,
`+E58`<sub>h</sub> to 0 and `+DC8`<sub>h</sub> to `FFFF`<sub>h</sub>, without giving anything back (`00305695`-`003056BA`). For every unit it
then charges the MP and Mist costs, with `10`<sub>h</sub> plus `flag` as the change reason (`003056E3`-`003056F4`), and takes a
second gil amount, unit `+E54`<sub>h</sub>, floored at 0 (`00305712`-`0030572B`). That amount is set when the action's
result is worked out (`00303954`, `00303B2E`) and cleared by the unit reset (`00236AE5`).

It is called from three places:

- the standard action, `00304F38`;
- `Battle_ProcessActionTargetEntry`, once per action, guarded by unit `+700`<sub>h</sub> bit 1, with `flag` 1
  (`003192B7`-`003192BC`);
- the handler of script verb `29D`<sub>h</sub> `spattackplay`, with `flag` 1 (`003132B7`).

A fourth pair of calls, a prepare at `003073AB` and a consume at `003073B9`, runs only when the fifth argument of
`00307300` is 1 (`00307388`), and its only caller passes 0 (`00319354`-`00319362`).

### Giving it back

`00300280(unit)` is called when an action is cancelled, by `BattleUnit_CancelAndResetCurrentAction`
(`0031063A`). For a party unit (`0030029D`-`003002A3`) it adds the reserved item back,
`003008A0(item, +1, 0, 1, 0)`, and empties the reservation (`003002A5`-`003002D0`). It then adds the reserved gil
back through the same `00253690` and `00254EE0` and clears it (`003002D7`-`003002F5`).

### Units that never spend items

The record kind byte `+5` is 0 only for the party's own records; enemies have 1
([Licenses](licenses.md) has the same test). Every step above returns early for any other kind, so a non-party
unit's item actions take no item and reserve no gil. Guests have party records: `BattleStats_InitializeDefinitionRecord`
writes kind 0 for any row of the party table, with no limit on the row (`0023AD41`-`0023AD8E`). So guests' item
actions spend the party's items; the License test differs, because it also passes every party row above 6.

## Shipped data

The 51 item actions are action rows 82-145 except 111-123, one for each item id `0000`<sub>h</sub>-`003F`<sub>h</sub> apart from
`001D`<sub>h</sub>-`0029`<sub>h</sub>: Potion (row 82, item `0000`<sub>h</sub>) to Knot of Rust (row 145, item `003F`<sub>h</sub>). Rows 111-123 have kind
255 and still name items `001D`<sub>h</sub>-`0029`<sub>h</sub> in `+22`<sub>h</sub>; with kind 255 they are not item actions.

## Modding notes

- An action spends an item only when its kind byte is 3; setting another action's kind to 3 and its `+22`<sub>h</sub> to an
  item makes it cost that item.
- The item leaves the inventory when the action starts, so an item count of 1 cannot be queued by two members at
  once.

## Related

- [Action definition row](../Battle-Actions/action-definition-row.md) - the kind byte and `+22`<sub>h</sub>.
- [Action phases](../Battle-Actions/action-phases.md) - when an action starts, goes off or is cancelled.
- [Inventory](inventory.md) - the change function the item goes through.
- [MP gain and cost](../Status-Effects-And-KO/mp.md) - MP, Mist and gil costs.
- [Licenses](licenses.md) - the party-record test, with its extra party-row test.
