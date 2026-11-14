---
title: "Scenario presets: every numbered save-data set a script can load, with its party, levels, gear, gambits, licenses, gil and items"
kind: "reference"
category: "Party"
addresses: "0x0050F810, 0x00239960, 0x02EBF030, 0x02EBF028, 0x00236FA2, 0x00236FBC"
---

## What it lists

A script verb can ask for a numbered set of save data: `0x0050F810`, the handler of verb `0x302B`
`btlAtelSetNextSetSaveData` (entry `0x2B` of the family-3 table at `0x01F281B0`), pops the number and stores it at
`0x0208D455`.
The next area start applies it once, from `BattleSystem_InitializeAreaState` (`0x00234349`), and the table the
sets come from gives the pack its folder name, `test_battle`.

A script only names a set's number, and the game applies it at the next area start. It rebuilds every character from
the party table, then takes the gil, items, seats and leader from the set's scenario row, and each member's level,
gear and gambits from the preset rows with the same number, both in `battle_pack.bin`.

### Applying a set

`0x00239960` reads the number and, when it is not -1, copies it to the byte `0x0208D456` (`0x00239975`) and sets
it back to -1, so a set is applied once (`0x00239966`-`0x0023997B`). -2 resets
the battle state instead (`0x00237DF0`), and any other negative number does nothing (`0x00239993`-`0x00239996`).

A number above the scenario table's row count less 1, compared unsigned, does nothing either (`[0x02EBF030]+4`,
50 in the shipped section 60; `0x0023999C`-`0x002399BB`), so the shipped table passes sets 0 to 49. With the
table pointer null the count is taken as 0 (`0x002399AA`-`0x002399B4`); then, as with a row count of 0, the
bound is `0xFFFFFFFF` and no number is refused. Otherwise (`0x002399E9`-`0x00239DE8`):

1. The party block is reset, keeping bits `0x1000`, `0x2000` and `0x4000` of its flag word and moving bits `0x2`
   and `0x4` of the battle flags `0x02089344` into its bits `0x2000` (New Game+) and `0x4000` (New Game-), clearing
   them in `0x02089344`. All forty member records are rebuilt from the party table with `0x0023AC80`
   (`0x002399E9`-`0x00239ACE`; [Party data](party-data.md), [Battle unit construction](../Characters-And-Objects/battle-unit-construction.md)).
   - Between the flag moves and the rebuilds the kill chain is reset with `0x003183A0` (`0x00239A85`;
     [Kill chain](../Rewards-EXP-Gil-And-Loot/kill-chain.md)).
2. The scenario's gil is set with `0x00300500` ([Gil](../Rewards-EXP-Gil-And-Loot/gil.md)), the inventory
   emptied with `0x003047F0` (`0x00239B22`), and up to 64 entries granted, each an id and a count set with
   `0x00300BA0` ([Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md); `0x00239B11`-`0x00239B5F`).
   - `0x003047F0` stores 0 in every word of the array that each of the fifteen inventory descriptor records
     from `0x01EEBCC0` names by its pointer `+0x08` and length `+0x10`, a null pointer being stepped over
     (`0x00304801`-`0x0030483B`), and jumps to `0x00253480` (`0x0030483D`).
   - `0x00253480` clears the twelve category lists with `0x00253240(list, 1)` and every category bit of
     `[0x020927C0] + 0x3244` but bit `0x1`, with bit `0x1` of `+0x3245` (`0x00253490`-`0x002534B1`).
3. Each party-preset row with this scenario number sets up the member in its record slot: level, gambit preset,
   License Points, the five pieces of gear and the MP share (`0x00239BBC`-`0x00239D7F`).
4. The nine seats are filled from the scenario row with `0x00329080(seat, member, 3)`, and the leader
   selector `[0x02EBF190]+0x5AA4` takes the member in the seat the row's byte `+0x0A` names, or `0xFF`
   when that byte is above 8, through `0x00327870`, which then has `0x00326500` pick the controlled member
   (`0x00239DC0`-`0x00239DE0`; [Party slots](party-slots.md)).
5. Last it calls `0x002CFD10(-1)`, which does not read its argument and clears the menu cursors (`0x00239DE5`-`0x00239DE8`;
   [Loading a save](../Saving-Loading-And-Settings/loading-a-save.md)): it stores 0 in the word
   `[0x020927C0] + 0x38` through `0x002527B0(6, 4, 0)` (`0x002CFD1E`, `0x0025282D`) and jumps to `0x0028E880`
   (`0x002CFD27`), which zeroes the `0xC4` bytes at `[0x0209BE80] + 0xAA60` while that pointer is set
   (`0x0028E880`-`0x0028E89B`).

### Which scripts ask for a set

Of the 1,114 `us` scripts of `plan_master`, one shipping script calls the verb: `naf_b04` asks for set 1. The
developer test script `evt_t0505` calls it five times, for sets 0 (twice), 2 and 3 and for a number held in a
script variable. The other eight language folders make the same calls.

Every new game also asks for set 0: the new-game widget `0x00394130` stores 0 through `0x0023A110` when it is built (`0x003942F9`).

The number `evt_t0505` holds comes from its `loadYoyaku.getLoadYoyaku`, which picks a set by story progress: set 0
below 25, then 35 ranges up to set 24 from 6,750. No script asks for sets 4-10, 14, 16, 19 and 21. The `loaded_by`
column gives each set's callers. These counts cover the 1,114 `us` scripts with a decoded listing, of 1,115:
`evt_t0020` has no EBP2 header.

### A member's preset

| Field | Effect | Sites |
|---|---|---|
| level | the member's level, through the level writer `0x0030C470` | `0x00239BE3`-`0x00239BED` |
| gambit preset | loaded into the member's gambits by `0x00327CB0` ([Gambits](../Enemy-AI-And-Gambits/gambits.md)) | `0x00239BF9`-`0x00239C00` |
| MP bars | the record's byte `+0x20`, the MP bars source ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)) | `0x00239BF2`-`0x00239BF6` |
| License Points | added (65,535 for `0xFFFF`) to the member's License Points `+0x190`, zeroed just before together with the 46 bytes of owned license squares `+0x194`-`+0x1C1` (`0x00239C05`-`0x00239C39`); for party rows 0-6 (the six main characters and Reks; `0x00239C49`) a value other than `0xFFFF` also learns every license square whose row byte `+7` has the member's bit, through `0x00323910` ([Licenses](../Items-Equipment-Shops-And-Licenses/licenses.md)) | `0x00239C05`-`0x00239D63` |
| gear | the five equipment slots, each set with `0x0031A630` ([Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md)) | `0x00239C62`-`0x00239CBF` |
| MP share | current MP = max MP × share / 100, or 0 with augment 39 | `0x00239CC4`-`0x00239D7F` |
| gambit mark | the member's record flag bit `0x4`, taken from bit `0x1` of the first byte of the **next** preset row | `0x00239D83`-`0x00239D94` |

## Columns

[`scenario-presets.tsv`](scenario-presets.tsv), one row per scenario:

| Column | Meaning |
|---|---|
| `scenario` | the set number, 0-49 |
| `party` | the nine seats: the four active, then the five in reserve; `-` for an empty seat |
| `leader` | the member in seat `+0x0A` |
| `gil` | the gil the set gives |
| `items` | each item, piece of gear, magick, technick, quickening or key item granted, with its count |
| `members` | each member the set sets up: name, level, gear, gambit preset, License Points, licenses, MP bars, MP share, and the gambit mark |
| `sites` | the scenario row's file offset in `battle_pack.bin`, and how many preset rows it has |
| `loaded_by` | each script, step and story point, or the new game, that asks for the set ("Which scripts ask for a set" above), or `not loaded` with the reason |
| `item_ids` | each entry of `items` as its encoded id and count, from the words at `+0x10` and the bytes at `+0x90` of the scenario row, `-` for none |
| `gear_ids` | each member's preset row number, member slot (byte `+0x01` of the row), name, level and the five encoded gear ids at `+0x04` of the row, `-` for an empty slot, or `-` alone for a set with no preset rows |

Scenario rows are section 60 (50 × 208 bytes, bound to `0x02EBF030` at `0x00236FA2`); preset rows are section 59
(226 × 44 bytes, bound to `0x02EBF028` at `0x00236FBC`). Names come from each id's class table and text bank.

## Related

- [Party slots](party-slots.md) - the nine seats a set fills.
- [Party data](party-data.md) - the party block a set resets.
- [Gambits](../Enemy-AI-And-Gambits/gambits.md) - the gambit presets and the gambit mark.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the member record fields a preset writes.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Movement: `0x00326500` calls `0x00311E20`; those functions are documented on
  [party control modes](../Engine-Core/party-control-modes.md).
- Save load settings: `0x002CFD10` is called by `0x00280140`; those functions are documented on
  [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md).
- Presentation: `0x002527B0` is called by `0x00579420`; those functions are documented on
  [quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md).
