---
title: "Formula recipes: every damage recipe with its slot lists and the actions and weapons that use it"
kind: "reference"
category: "Damage and battle formulas"
summary: "All 109 recipes of the recipe table at 01EF96C0: for each, the calculator slots of its first list (run when the action executes, deciding hit, evade and knockback) and of its committed list (damage and effects), and the shipped action rows and weapon rows that select it, with their names."
addresses: ["01EF96C0", "01EFA5C0", "00385F60", "00385680"]
---

# Formula recipes: every damage recipe with its slot lists and the actions and weapons that use it

## What it lists

Every action resolves through one of 109 recipes. A recipe is a list of calculator slots, and a slot is
one entry of the function table at `01EFA5C0`. The recipe table at `01EF96C0` holds one pointer per
recipe, and each pointer leads to two lists of `int32` slot numbers, each ended by -1.

- **The first list** runs when the action executes, through `00385680` (the slot call at `003859FF`).
  `00303830` calls it at `00303910`, and is itself called from the action state machine at `00304F1D`;
  `00303A00` calls it at `00303AD7`. It decides hit, evade, block, parry and knockback.
- **The committed list** runs in `00385F60`: it skips the first list (`00386365`-`0038637B`) and calls each
  slot of the second at `003863D0`, stopping early when `02AEDFB8` is 1 (`003863D7`).

An action takes its recipe from byte `+0x08` of its row (`0038617E`). Recipe 0 means "the weapon's": the
resolver then takes byte `+0x19` of the main-hand weapon row (`003861FD`). A recipe of `0x6D` (109) or more
returns -1 (`00386182`, `00386212`). [Weapon formulas](weapon-formulas.md) explains the weapon recipes and
[Steal](steal.md) walks through one action recipe.

Besides recipe 0, shipped actions use 89 recipes and weapons 11, and 8 recipes are used by neither (15, 28, 44, 71, 80,
81, 89, 106). Recipe 0 is the recipe byte of 73 action rows, among them Attack.

## Columns

`formula-recipes.tsv`, one row per recipe:

| Column | Meaning |
|---|---|
| `recipe` | the recipe number, 0-108 |
| `preview_slots` | the first list, as slot numbers into `01EFA5C0` |
| `committed_slots` | the committed list |
| `action_rows` | how many of the 543 action rows have this recipe byte (`battle_pack.bin` section 14, byte `+0x08`) |
| `actions` | those rows: the action id and its name, the bank-0 entry its name word `+0x34` names |
| `weapon_rows` | how many weapon rows (equipment classes 0-17, `battle_pack.bin` section 13) have this recipe byte `+0x19` |
| `weapons` | those rows by equipment class, with up to three named items per class |

Names are the US texts. In them `-` and `'` replace the text codes `{A5}` and `{AC}`, and the formatting
prefix of the Reserve rows is dropped.

## Related

- [Weapon formulas](weapon-formulas.md) - the weapon recipes 20-29, 64 and 104 and the special action
  recipes.
- [Steal](steal.md) - recipe 49.
- [Elements](elements.md) - the element slots 92-99 and the finishers 113 and 125.
- [Action definition row](../Battle-Actions/action-definition-row.md) - the recipe byte of an action.
