---
title: "Formula slots: every calculator slot with what it computes, what it reads and which recipes run it"
kind: "reference"
category: "Damage and battle formulas"
summary: "All 202 slots of the calculator table at 01EFA5C0: for each, its function and size, the recipes whose first or committed list contain it, what it computes, the stats, action-row, weapon-row, result and scratch fields it reads and writes, the statuses and effect ids it tests, and the instruction sites that show it."
addresses: "01EFA5C0, 01EF96C0, 00385F60, 00385680, 003847C0, 0016D6A0"
---

## What it lists

Every number a battle action produces comes from calculator slots. The table at `01EFA5C0` holds 202
function pointers; a recipe names slots by their index ([Formula recipes](formula-recipes.md)). Both
runners call a slot as `slot(source, target, &context)`: `00385680` for a recipe's first list (`003859FF`)
and `00385F60` for its committed list (`003863D0`). No other code calls a slot body directly: an `E8`/`E9`
scan of the code section finds no call to any of them, and no other pointer to one exists outside the
table.

The context is built by `003847C0` ([Damage formula](damage-formula.md)). The slots pass their answer to
the resolver through scratch globals such as the scale `02AEE054` and the HP loss `02AEE004`
([Elements](elements.md) shows one finisher).

In the shipped executable:

- 202 slots point to 152 functions. One of them, `0016D6A0`, is a single `ret 0`, and it fills 42 slots.
- Seven functions fill more than one slot: `00388FE0` (23, 24), `00389670` (40, 45, 46), `00389F80` (60, 63),
  `0038AA90` (61, 64, 75), `0038AAF0` (65, 76), `0038D280` (113, 125) and `0038F5A0` (115, 160).
- 42 slots are in no shipped recipe. 38 of them are the `ret 0` slot; slots 37 and 118 run only when other
  slots call them through the table (37 from 15, 191 and 192; 118 from 185 and from `00387CB0`, behind
  181 and 182), and 73 and 131 are called by nothing.
- Four `ret 0` slots do appear in shipped recipes: 28, 193, 198 and 199.

## Columns

`formula-slots.tsv`, one row per slot:

| Column | Meaning |
|---|---|
| `slot` | the slot index, 0-201 |
| `function` | the function the table holds |
| `size` | the function's size in bytes |
| `recipes_first`, `recipes_committed` | the recipes whose first or committed list contains the slot, or `-` |
| `computes` | what the body does, from its instructions |
| `reads`, `writes` | the fields it reads and writes: `S+` and `T+` for the source's and target's stats record, `act+` for the action row, `wpn+` for the main-hand weapon row, `res+` for the result record, `ctx+` for the context, and scratch globals by address |
| `statuses_tested` | the source's (`ctx+4`) or target's (`ctx+8`) statuses it tests, by name |
| `effects_tested` | the merged effect bits (`ctx+0x1A`...) and the layer bits (`+0x68`, `+0x78`) it tests, with the effect's augment text, or "(no augment text)" when the augment text bank holds none |
| `sites` | the instructions that show the row |

Two formulas the rows use often are written once in them:

- `v(X)` is the 12.5 % variance, `(MT19937 % (int)(X * 12.5)) / 100`, or 0 when `X / 8` is below 0.01;
- `refHP(X)` is X's max HP, doubled under Bubble, or under Disease its current HP and at least 1.

## Related

- [Formula recipes](formula-recipes.md) - which slots each recipe lists.
- [Damage formula](damage-formula.md) - the order a typical attack and magick runs its slots in.
- [Weapon formulas](weapon-formulas.md) - the weapon preparation slots.
- [Elements](elements.md) - the element slots and the finishers.
- [Steal](steal.md) - slot 195.
