---
title: "Battle unit fields: the unit record offset by offset, its regions, and every reach the access table proves"
kind: "reference"
category: "Characters and objects"
addresses: "0x00234480, 0x00236A60, 0x00316CD0, 0x00316CF0, 0x003839F0, 0x003839C0, 0x00383670, 0x00234200, 0x00265020, 0x00329220"
---

## What it lists

A battle unit is the `0xF50`-byte combat record every fighting actor holds in the pool of 32
([battle units](battle-units.md)). This page lays the record out by region and names the fields
that a final page has established; the companion table `battle-unit-fields.tsv` lists every access
to a unit that the typed scan reached: the function, the site, the offset, the operand width and
the instruction, each instruction checked against the executable.

### The regions

| Unit offset | Size | Region | Who establishes it |
|---|---|---|---|
| `+0x000` | 8 | the flag word (bit 0 slot in use; the bit table on the battle units page) | [battle units](battle-units.md) |
| `+0x008` | 4 | the actor handle, `0x003589B0(actor)` at bind | [battle units](battle-units.md) |
| `+0x010` | 8 | the bound actor record | [battle units](battle-units.md) |
| `+0x020` | 4 | 1 once the bind walk has run (`0x00234A00`) | [battle units](battle-units.md) |
| `+0x030` | 4 | the killer id the lethal transition records | [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md) |
| `+0x048` | 4 | the HP floor the HP write honours | [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md) |
| `+0x057` | 1 | the actor's entry group `+0xF6`, copied at bind | [battle units](battle-units.md) |
| `+0x080` | 1552 | the block the reuse reset `0x00236A60` zeroes (`+0x80`-`+0x68F`): position, navigation and the waypoint table | this page |
| `+0x0E0` | 16 | the world position, read by `0x00265020` and copied to the spawn record at release | [battle units](battle-units.md) |
| `+0x160` | 4 | the yaw copied to the spawn record's `+0x74` at release | [battle units](battle-units.md) |
| `+0x200` | 1168 | the navigation path state (below) | this page |
| `+0x694` | 3 | three bytes the reset sets to `0xFF`, `0xFFFF` | this page |
| `+0x698` | 8 | the combat stats record | [unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) |
| `+0x6A0` | 8 | the spawn record for an enemy, null for a party member | [battle units](battle-units.md) |
| `+0x6B0` | 4 | the command word: bit 1 a command issued and not yet committed | [action commit](../Battle-Actions/action-commit.md) |
| `+0x6B4` | 1 | the action phase | [action phases](../Battle-Actions/action-phases.md) |
| `+0x6B7`, `+0x6B8` | 2 | combo progress and its saved copy | [combos](../Battle-Actions/combos.md) |
| `+0x700` | 16 | the action block; `+0x708` the action context, `+0x710` the target focus handle, `+0x714` the action id | [action commit](../Battle-Actions/action-commit.md), [battle orders](../Battle-Actions/battle-orders.md) |
| `+0x718` | 16 | the copy of the action block taken at commit | [action commit](../Battle-Actions/action-commit.md) |
| `+0x730`, `+0x740` | 16 + 8 | the cancelled action's record, target and id | [action phases](../Battle-Actions/action-phases.md) |
| `+0x768`, `+0x76C` | 8 | action fields the status record shows while acting | [party member status record](party-member-status-record.md) |
| `+0x778` | 520 | the target buffer (below) | [target selection](../Battle-Actions/target-selection.md) |
| `+0xBA0` | 2 | the issued command's action id | [party member status record](party-member-status-record.md) |
| `+0xBC4`, `+0xBC8` | 4 + `0x200` | the perception candidate cache: count, then 16-byte entries | [enmity](../Enemy-AI-And-Gambits/enmity.md) |
| `+0xDC8` | 2 | the reserved consumed item, `0xFFFF` when none | [command availability](../Battle-Actions/command-availability.md) |
| `+0xE54`, `+0xE58` | 8 | the gil the preview computed and the reserved gil cost | [command availability](../Battle-Actions/command-availability.md) |
| `+0xE60` | 8 | the definition row | [steal](../Damage-And-Battle-Formulas/steal.md) |
| `+0xE68` | 8 | the class row the status record reads `+0x52` and `+0x12` bit 7 from | [party member status record](party-member-status-record.md) |
| `+0xE80` | 16 | the innate augment source | [augments](../Damage-And-Battle-Formulas/augments.md) |
| `+0xEA9` | 1 | the slot index, written at bind | [battle units](battle-units.md) |

## Columns

`battle-unit-fields.tsv`, one row per access site:

| Column | Meaning |
|---|---|
| `function` | the function containing the instruction |
| `name` | the name the scan carried for that function; blank or `FUN_` when none was assigned |
| `site` | the instruction's address |
| `disp` | the unit offset reached |
| `kind` | `r` read, `w` write, `rw` read-modify-write, `addr` the address is formed and passed on |
| `instruction` | the instruction text, checked against the executable |
| `route` | how the scan knew the register held a unit: a pool accessor's return, or an argument passed by a named caller at a named site |
| `note` | `idx` when an index register takes part |

## Data

### The reuse reset

`0x00236A60(unit)` prepares a slot for its next occupant without releasing it:

1. when flag bit 4 is set it first runs `0x003105D0`;
2. it writes `0xFFFF` at `+0x695` and `0xFF` at `+0x694`, and clears flag bits 2, 3, 4, 8, 9, 10, 11
   and 14 (`and dword +0, 0xFFFFB0E3`), bits 34, 38 and 52 (`and dword +4, 0xFFEFFFBB`) and bits 1,
   19, 20, 33 and 47 (the register mask `0xFFFF7FFDFFE7FFFD`);
3. it zeroes `+0x698`, `+0x6A0`, `+0xE60`, `+0xE68`, `+0x24`-`+0x33`, `+0x5C`-`+0x63`, the dword
   `+0xE54`, `+0xEA4`, `+0xEA8`, `+0xDD0`, `+0x64`-`+0x6F`, and sets `+0x74` to all ones, `+0x55`-`+0x56`
   to `0xFFFF`, `+0x52` to 0 and `+0x54` to `0xFF`;
4. it resets the perception cache at `+0xBC0` with `0x00316D30`, which forces header bit 0 on before
   its `0x208`-byte clear and restores it after, and takes the resource accumulator `0x00320450`,
   which returns the dword `+0x70` (only for a unit with flag bit 4, a stats record and no terminal
   status outside a town) and zeroes it;
5. it zeroes `+0xE80`-`+0xE8F`, `+0xE90`, `+0x714` to `0xFFFF`, `+0x6B5`, `+0x6D0`, `+0x6E0`-`+0x6FF`,
   `+0x748`-`+0x757`, `+0xB90`, the low byte of `+0x6B0`, `+0x708`-`+0x713`, `+0x760`-`+0x773`, and
   sets `+0x758` and `+0xDC8` to all ones; the commit copy `+0x718`-`+0x72F` and the cancelled record
   `+0x730`-`+0x747` take the `+0x700`-`+0x717` bytes as they stand after those stores;
6. it zeroes the `0x610` bytes from `+0x80`, resets the navigation state (`0x003839F0` fills
   `+0x210`-`+0x28F` with `0xFF`, `0x003839C0` sets `+0x20C`-`+0x20F` to `0xFFFF`) and ends in
   `0x003176C0`, which zeroes the 32 dwords at `+0xDD4`-`+0xE53`.

The target buffer at `+0x778` is not touched by the reuse reset.

### The navigation path state

Struct BattleUnitPathState base=unit+`0x200` size=`0x490`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | current | the waypoint index the walker is on (`0x00383670` reads and writes it) |
| `+0x0C` | `u16[2]` | endpoints | `0xFFFF` after `0x003839C0` |
| `+0x10` | `u8[128]` | predecessor | the next waypoint after each index; `0xFF` after `0x003839F0` |
| `+0x90` | `f32[2][128] waypoints` | x and z per index; 0x00383670 copies entry i to its output at +0 and +8 |  |

`0x00383670(position, _, out, state, arg)` follows the predecessor chain from `current` while
`0x00383A30` reports each step reached, calls `0x00383C90` for the chosen index, copies that waypoint's
two floats into `out` (with the position's y at `out + 4`) and stores the index back.

### The target buffer

Struct BattleTargetBuffer base=unit+`0x778` size=`0x208`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | header | bit 0 survives the reset `0x00316CF0` |
| `+0x01` | `u8[2]` | cleared by the reset |  |
| `+0x04` | `i32` | count | at most 32; `0x00316CD0` appends at count and increments |
| `+0x08` | `u8[512]` | entries | 32 entries of 16 bytes: the actor at +0, the outcome word at +8 (target selection page) |

### Reset extents

| Clear | Range | Where |
|---|---|---|
| allocation | the whole `0xF50` bytes | `0x00234480` before the bind |
| release | the whole `0xF50` bytes | `0x00234200` after the spawn-record copy |
| reuse | `+0x80`-`+0x68F` zeroed, then `+0x20C`-`+0x20F` and `+0x210`-`+0x28F` set to all ones; the fields listed above | `0x00236A60` |
| perception cache | `+0xBC0`-`+0xDC7`, header bit 0 forced on | `0x00316D30` from the reuse reset |
| target buffer | `+0x778`-`+0x97F`, keeping header bit 0 | `0x00316CF0` |

## Related

- [Battle units](battle-units.md): the pool, the bind and the flag word.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md): the record at `+0x698`.
- [Action commit](../Battle-Actions/action-commit.md), [action phases](../Battle-Actions/action-phases.md) and [target selection](../Battle-Actions/target-selection.md): the action block and the target buffer.
- [Enmity](../Enemy-AI-And-Gambits/enmity.md): the perception cache.
- [Party member status record](party-member-status-record.md): the fields the HUD reads.
