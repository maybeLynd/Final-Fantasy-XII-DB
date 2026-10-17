---
title: "Party data: every field of the block the save game keeps for the party, above the forty member records"
kind: "reference"
category: "Party"
addresses: "02EBF190, 00233C10, 002370C0, 0030B6A0, 00320A40, 0031B9F0, 00327C40"
---

## What it lists

The party block is `7410`<sub>h</sub> bytes inside the save image: buffer `02164280` + `4E68C`<sub>h</sub>, which is payload
`+4E48C`<sub>h</sub> ([Save data](../Saving-Loading-And-Settings/save-data-fields.md)). `00233C10` points `02EBF190` at it when the
pointer is empty and rebases the inventory class descriptors, and checks the magic `05071901`<sub>h</sub> when it is set
(`00233C25`-`00233C4D`).

With an empty pointer or a wrong magic `00233C10` then runs the battle-state reset `00237DF0`,
whose first step `0023AF50` resets the block and adds the starting inventory
([Starting inventory](starting-inventory.md)). With the magic in place it rebuilds the gambit order set of all forty
members with `00327F80`, the loop form of `00327DE0` (`00233CAD`; [Gambits](../Enemy-AI-And-Gambits/gambits.md)). The reset `002370C0` clears all `7410`<sub>h</sub> bytes, writes the magic, empties map 0's seats
and zeroes the walked distance (`002370CD`-`0023712E`).

The block holds:

- the forty member stats records from `+8` ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md));
- the inventory: owned counts and learned bits per class, laid out by the descriptors at `01EEBCC0` and rebased by
  `0030B6A0` ([Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md));
- the seats, leader and battle mode ([Party slots](party-slots.md),
  [Battle mode](../Engine-Core/party-control-modes.md));
- the mode flags `+5B04`<sub>h</sub>, whose bits 0 and 1 the status view `00329220` tests for its flag bits 10 and 11; the
  screens read members through that view, the battle menu's target window `002BFD20` among them
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

The census follows the block pointer `02EBF190` and the pointers handed on from it into the functions it reaches;
an access through a pointer it did not follow is not in these two columns. Rows named `pad` have no field.

## Related

- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the forty member records.
- [Party slots](party-slots.md) - the five slot maps and the leader.
- [Scenario presets](scenario-presets.md) - the sets that reset and refill the block.
- [Gambits](../Enemy-AI-And-Gambits/gambits.md) - the gambit banks.
- [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md) - the count words, bits and tallies.
- [Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md) - the Traveler, Knot of Rust and Numerology counters.
