[Home](../../README.md) / [Items, equipment, shops and licenses](README.md) / Using an item

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Using an item: how a Potion is an action that costs an item, when the item is taken, given back or kept, and why enemies never spend items | system | Items, equipment, shops and licenses | Items and inventory | How an item is spent in battle: the action row whose category byte marks it as an item and names the item it uses, the reservation taken when the action starts, the consume that keeps it spent and the refund that gives it back when the action is cancelled, the gil reservation that works the same way, the record kind that lets enemies use items for free, and the 51 shipped item actions. | 0x0030EF20, 0x00305640, 0x00300280, 0x003105D0, 0x00309060 |

## What the player sees

- Using a Potion takes one from the inventory as soon as the character starts the action, before it charges.
- If the action is cancelled before it goes off, the Potion comes back.
- Enemies can use items without having or spending any; guests spend the party's items like members do.

## How it works

### An item is an action

Every usable item is an action row ([Action definition row](../Battle-Actions/action-definition-row.md)). A row
whose kind byte `+0x1E` is 3 is an item action, and its word `+0x22` is the item it uses. What the item does,
whom it targets and how it looks are the rest of the row, handled like any other action.

### Taking the item

`0x0030EF20(unit, row)` runs when the action starts, phase 0 of the action ([Action phases](../Battle-Actions/action-phases.md);
`0x00304962`). It does nothing for a unit without a stats record or whose record is not a party record, byte `+5`
not 0 (`0x0030EF60`-`0x0030EF77`). Otherwise:

1. The item id is the row's `+0x22` for a kind-3 row and `0xFFFF` otherwise; it is kept at unit `+0xDC8`, the
   reserved item (`0x0030EF79`-`0x0030EF93`).
2. A reserved item is taken from the inventory at once, `0x003008A0(item, -1, 0, 1, 0)` (`0x0030EF9A`-`0x0030EFB0`,
   [Inventory](inventory.md)).
3. The action's gil cost, `0x00309060`, is kept at unit `+0xE58` and taken from the gil, floored at 0
   (`0x0030EFBB`-`0x0030EFD8`), through `0x00253690` and `0x00254EE0` ([Gil](../Rewards-EXP-Gil-And-Loot/gil.md)). Only actions paid in gil have one: `0x00309060` returns 0 for an enemy record, for an
   action id above `0x21E` and for rows of kind 5 or 6 ([MP gain and cost](../Status-Effects-And-KO/mp.md)).

`0x0030EF20` works out the action index it gives `0x00309060` from the row: `(row - first row) / row size` of the
action table `[0x02EBF138]` (`0x0030EF2F`-`0x0030EF5E`). A null `row` gives the item `0xFFFF` (`0x0030EF7E`-`0x0030EF81`,
`0x0030EF8F`). The cost is stored at `+0xE58` even when it is 0, and the gil is then left as it is
(`0x0030EFC0`-`0x0030EFCA`).

### Keeping it spent

`0x00305640(unit, row, flag)` runs when the action goes off. For a party unit it clears both reservations,
`+0xE58` to 0 and `+0xDC8` to `0xFFFF`, without giving anything back (`0x00305695`-`0x003056BA`). For every unit it
then charges the MP and Mist costs, with `0x10` plus `flag` as the change reason (`0x003056E3`-`0x003056F4`), and takes a
second gil amount, unit `+0xE54`, floored at 0 (`0x00305712`-`0x0030572B`). That amount is set when the action's
result is worked out (`0x00303954`, `0x00303B2E`) and cleared by the unit reset (`0x00236AE5`).

For a party record it then feeds the achievement counters through `0x00253770` (`0x00305730`-`0x003057A5`,
[Achievements](../Steam-And-Achievements/achievements.md)): counter 0, 1 or 2 by 1 for row kind `+0x1E`
0, 1 or 2, and for kind 10 counter 13 by the row index, after `0x00316440`. Other kinds feed no counter
(`0x0030575A`).

It is called from four places:

- the standard action, `0x00304F38`;
- the effect applier `0x00307300`, with `flag` 0, when its fifth argument is 1 and the availability check `0x002FFCF0`
  passes (`0x00307388`-`0x003073B9`);
- the per-target step `0x003191B0`, once per action, on a pass with `again` 0 (`0x00319200`), while unit `+0x700` bit
  `0x2` is clear and only when `0x0030B9B0(target unit, unit)` answers 0 and `0x002FFA60(action, target unit)` answers
  non-zero, with `flag` 1 (`0x00319241`-`0x003192BC`; [Area of
  effect](../Battle-Actions/area-of-effect.md#entry-flags));
- the handler of script verb `0x29D` `spattackplay`, with `flag` 1 (`0x003132B7`).

The effect applier's call never runs: `0x00307300` has one caller, which passes 0 as the fifth argument
(`0x00319354`-`0x00319362`), so its prepare `0x0030EF20` at `0x003073AB` and its consume at `0x003073B9` are skipped
(`0x00307388`).

### Giving it back

`0x00300280(unit)` is called when an action is cancelled, by `BattleUnit_CancelAndResetCurrentAction`
(`0x0031063A`). For a party unit (`0x0030029D`-`0x003002A3`) it adds the reserved item back,
`0x003008A0(item, +1, 0, 1, 0)`, and empties the reservation (`0x003002A5`-`0x003002D0`). It then adds the reserved gil
back through the same `0x00253690` and `0x00254EE0` and clears it (`0x003002D7`-`0x003002F5`).

### Units that never spend items

The record kind byte `+5` is 0 only for the party's own records; enemies have 1
([Licenses](licenses.md) has the same test). The reservation, its clearing and the refund return early for any
other kind, so a non-party unit's item actions take no item and reserve no gil; the MP, Mist and `+0xE54` gil
charges of `0x00305640` apply to every unit.

Guests have party records: `BattleStats_InitializeDefinitionRecord`
writes kind 0 for any row of the party table, with no limit on the row (`0x0023AD41`-`0x0023AD8E`). So guests' item
actions spend the party's items; the License test differs, because it also passes every party row above 6.

## Shipped data

The 51 item actions are action rows 82-145 except 111-123, one for each item id `0x0000`-`0x003F` apart from
`0x001D`-`0x0029`: Potion (row 82, item `0x0000`) to Knot of Rust (row 145, item `0x003F`). Rows 111-123 have kind
255 and still name items `0x001D`-`0x0029` in `+0x22`; with kind 255 they are not item actions.

## Modding notes

- An action spends an item only when its kind byte is 3; setting another action's kind to 3 and its `+0x22` to an
  item makes it cost that item.
- The item leaves the inventory when the action starts, so an item count of 1 cannot be queued by two members at
  once.

## Related

- [Action definition row](../Battle-Actions/action-definition-row.md) - the kind byte and `+0x22`.
- [Action phases](../Battle-Actions/action-phases.md) - when an action starts, goes off or is cancelled.
- [Inventory](inventory.md) - the change function the item goes through.
- [MP gain and cost](../Status-Effects-And-KO/mp.md) - MP, Mist and gil costs.
- [Licenses](licenses.md) - the party-record test, with its extra party-row test.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- UI: `0x002FFCF0` is called by `0x0031EB20`; those functions are documented on
  [action definition row](../Battle-Actions/action-definition-row.md).
