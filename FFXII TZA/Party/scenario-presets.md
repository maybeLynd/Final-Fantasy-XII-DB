---
title: "Scenario presets: every numbered save-data set a script can load, with its party, levels, gear, gambits, licenses, gil and items"
kind: "reference"
category: "Party"
addresses: "0050F810, 00239960, 02EBF030, 02EBF028, 00236FA2, 00236FBC"
---

## What it lists

A script verb can ask for a numbered set of save data: `0050F810`, the handler of verb `0x302B`
`btlAtelSetNextSetSaveData` (entry `0x2B` of the family-3 table at `01F281B0`), pops the number and stores it at
`0208D455`.
The next area start applies it once, from `BattleSystem_InitializeAreaState` (`00234349`), and the table the
sets come from gives the pack its folder name, `test_battle`.

### Applying a set

`00239960` reads the number and sets it back to -1, so a set is applied once (`00239966`-`0023997B`). -2 resets
the battle state instead (`00237DF0`), and a number past the 50 scenarios does nothing (`002399BB`). Otherwise
(`002399E9`-`00239DE8`):

1. The party block is reset, keeping bits 12-14 of its flag word and taking bits 1 and 2 of the battle flags
   `02089344` into its bits 13 and 14; all forty member records are set up again from the party table
   ([Party data](party-data.md); `002399E9`-`00239ACE`).
2. The scenario's gil is set, the inventory emptied, and up to 64 entries granted, each an id and a count
   (`00239B11`-`00239B5F`).
3. Each party-preset row with this scenario number sets up the member in its record slot: level, gambit preset,
   License Points, the five pieces of gear and the MP share (`00239BBC`-`00239D7F`).
4. The nine seats are filled from the scenario row with `00329080(seat, member, 3)`, and the leader is the member
   in seat `+0x0A` (`00239DC0`-`00239DE0`; [Party slots](party-slots.md)).

### Which scripts ask for a set

Of the 1,114 `us` scripts of `plan_master`, one shipping script calls the verb: `naf_b04` asks for set 1. The
developer test script `evt_t0505` calls it five times, for sets 0 (twice), 2 and 3 and for a number held in a
script variable. The other eight language folders make the same calls.

### A member's preset

| Field | Effect | Sites |
|---|---|---|
| level | the member's level, through the level writer `0030C470` | `00239BE3`-`00239BED` |
| gambit preset | loaded into the member's gambits ([Gambits](../Enemy-AI-And-Gambits/gambits.md)) | `00239BF9`-`00239C00` |
| MP bars | the record's byte `+0x20`, the MP bars source ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)) | `00239BF2`-`00239BF6` |
| License Points | added to the member's License Points `+0x190`, zeroed just before (65,535 for `0xFFFF`); for one of the six main characters a value other than `0xFFFF` also learns every license square whose row byte `+7` has the member's bit | `00239C05`-`00239D63` |
| gear | the five equipment slots | `00239C62`-`00239CBF` |
| MP share | current MP = max MP × share / 100, or 0 with augment 39 | `00239CC4`-`00239D7F` |
| gambit mark | the member's record flag bit 2, taken from bit 0 of the first byte of the **next** preset row | `00239D83`-`00239D94` |

## Columns

`scenario-presets.tsv`, one row per scenario:

| Column | Meaning |
|---|---|
| `scenario` | the set number, 0-49 |
| `party` | the nine seats: the four active, then the five in reserve; `-` for an empty seat |
| `leader` | the member in seat `+0x0A` |
| `gil` | the gil the set gives |
| `items` | each item, piece of gear, magick, technick, quickening or key item granted, with its count |
| `members` | each member the set sets up: name, level, gear, gambit preset, License Points, licenses, MP bars, MP share, and the gambit mark |
| `sites` | the scenario row's file offset in `battle_pack.bin`, and how many preset rows it has |

Scenario rows are section 60 (50 × 208 bytes, bound to `02EBF030` at `00236FA2`); preset rows are section 59
(226 × 44 bytes, bound to `02EBF028` at `00236FBC`). Names come from each id's class table and text bank.

## Related

- [Party slots](party-slots.md) - the nine seats a set fills.
- [Party data](party-data.md) - the party block a set resets.
- [Gambits](../Enemy-AI-And-Gambits/gambits.md) - the gambit presets and the gambit mark.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the member record fields a preset writes.
