---
title: "Party data: every field of the block the save game keeps for the party, above the forty member records"
kind: "reference"
category: "Party"
addresses: "0x02EBF190, 0x00233C10, 0x002370C0, 0x0030B6A0, 0x00320A40, 0x0031B9F0, 0x00327C40"
---

## What it lists

The party block is `0x7410` bytes inside the save image: buffer `0x02164280` + `0x4E68C`, which is payload
`+0x4E48C` ([Save data](../Saving-Loading-And-Settings/save-data-fields.md)). `0x00233C10` points `0x02EBF190` at it when the
pointer is empty and rebases the inventory class descriptors, and checks the magic `0x05071901` when it is set
(`0x00233C25`-`0x00233C4D`).

With an empty pointer or a wrong magic `0x00233C10` then runs the battle-state reset `0x00237DF0`,
whose first step `0x0023AF50` resets the block and adds the starting inventory
([Starting inventory](starting-inventory.md)). With the magic in place it rebuilds the gambit order set of all forty
members with `0x00327F80`, the loop form of `0x00327DE0` (`0x00233CAD`; [Gambits](../Enemy-AI-And-Gambits/gambits.md)).

The reset `0x002370C0` clears all `0x7410` bytes, writes the magic, clears the inventory counts and empties the menu category lists of `[0x020927C0]` (`0x003047F0`, `0x002370E5`; [Save data](../Saving-Loading-And-Settings/save-data-fields.md)), empties map 0's seats
and zeroes the walked distance (`0x002370CD`-`0x0023712E`).

The block holds:

- the forty member stats records from `+8` ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md));
- the inventory: owned counts and learned bits per class, laid out by the descriptors at `0x01EEBCC0` and rebased by
  `0x0030B6A0` ([Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md));
- the seats, leader and battle mode ([Party slots](party-slots.md),
  [Battle mode](../Engine-Core/party-control-modes.md));
- the mode flags `+0x5B04`, whose bits 0 and 1 the status view `0x00329220` tests for its flag bits 10 and 11; the
  screens read members through that view, the battle menu's target window `0x002BFD20` among them
  ([Party member status record](../Characters-And-Objects/party-member-status-record.md),
  [Battle menu](../Menus-And-HUD/battle-menu.md));
- the counters three formulas keep ([Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md));
- the gambit banks ([Gambits](../Enemy-AI-And-Gambits/gambits.md)).

## Columns

`party-data.tsv`, one row per field:

| Column | Meaning |
|---|---|
| `offset` | the field's offset in the block |
| `width_type` | its width and type; `record`, `bank` and the bracketed counts are arrays |
| `field` | its name on this page |
| `meaning` | what it holds, with the instructions that show it |
| `writers`, `readers` | the functions an access census of the block finds writing and reading it, with one site each; a store counts for every byte it covers, a read for its first byte, and a function that only takes a field's address is listed as a reader |

The census follows the block pointer `0x02EBF190` and the pointers handed on from it into the functions it reaches;
an access through a pointer it did not follow is not in these two columns. Rows named `pad` have no field.

## Related

- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the forty member records.
- [Party slots](party-slots.md) - the five slot maps and the leader.
- [Scenario presets](scenario-presets.md) - the sets that reset and refill the block.
- [Gambits](../Enemy-AI-And-Gambits/gambits.md) - the gambit banks.
- [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md) - the count words, bits and tallies.
- [Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md) - the Traveler, Knot of Rust and Numerology counters.
