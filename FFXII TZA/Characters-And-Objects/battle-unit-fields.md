---
title: "Battle unit fields: the unit record offset by offset, its regions, and every reach the access table proves"
kind: "reference"
category: "Characters and objects"
addresses: "00234480, 00236A60, 00316CD0, 00316CF0, 003839F0, 003839C0, 00383670, 00234200, 00265020, 00329220"
---

## What it lists

A battle unit is the `F50`<sub>h</sub>-byte combat record every fighting actor holds in the pool of 32
([battle units](battle-units.md)). This page lays the record out by region and names the fields
that a final page has established; the companion table `battle-unit-fields.tsv` lists every access
to a unit that the typed scan reached: the function, the site, the offset, the operand width and
the instruction, each instruction checked against the executable.

### The regions

| Unit offset | Size | Region | Who establishes it |
|---|---|---|---|
| `000`<sub>h</sub> | 8 | the flag word (bit 0 slot in use; the bit table on the battle units page) | [battle units](battle-units.md) |
| `008`<sub>h</sub> | 4 | the actor handle, `003589B0(actor)` at bind | [battle units](battle-units.md) |
| `010`<sub>h</sub> | 8 | the bound actor record | [battle units](battle-units.md) |
| `020`<sub>h</sub> | 4 | 1 once the bind walk has run (`00234A00`) | [battle units](battle-units.md) |
| `030`<sub>h</sub> | 4 | the killer id the lethal transition records | [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md) |
| `048`<sub>h</sub> | 4 | the HP floor the HP write honours | [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md) |
| `057`<sub>h</sub> | 1 | the actor's entry group `+F6`<sub>h</sub>, copied at bind | [battle units](battle-units.md) |
| `080`<sub>h</sub> | 1552 | the block the reuse reset `00236A60` zeroes (`+80`<sub>h</sub>-`+68F`<sub>h</sub>): position, navigation and the waypoint table | this page |
| `0E0`<sub>h</sub> | 16 | the world position, read by `00265020` and copied to the spawn record at release | [battle units](battle-units.md) |
| `160`<sub>h</sub> | 4 | the yaw copied to the spawn record's `+74`<sub>h</sub> at release | [battle units](battle-units.md) |
| `200`<sub>h</sub> | 1168 | the navigation path state (below) | this page |
| `694`<sub>h</sub> | 3 | three bytes the reset sets to `FF`<sub>h</sub>, `FFFF`<sub>h</sub> | this page |
| `698`<sub>h</sub> | 8 | the combat stats record | [unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) |
| `6A0`<sub>h</sub> | 8 | the spawn record for an enemy, null for a party member | [battle units](battle-units.md) |
| `6B0`<sub>h</sub> | 4 | the command word: bit 1 a command issued and not yet committed | [action commit](../Battle-Actions/action-commit.md) |
| `6B4`<sub>h</sub> | 1 | the action phase | [action phases](../Battle-Actions/action-phases.md) |
| `6B7`<sub>h</sub>, `6B8`<sub>h</sub> | 2 | combo progress and its saved copy | [combos](../Battle-Actions/combos.md) |
| `700`<sub>h</sub> | 16 | the action block; `+708`<sub>h</sub> the action context, `+710`<sub>h</sub> the target focus handle, `+714`<sub>h</sub> the action id | [action commit](../Battle-Actions/action-commit.md), [battle orders](../Battle-Actions/battle-orders.md) |
| `718`<sub>h</sub> | 16 | the copy of the action block taken at commit | [action commit](../Battle-Actions/action-commit.md) |
| `730`<sub>h</sub>, `740`<sub>h</sub> | 16 + 8 | the cancelled action's record, target and id | [action phases](../Battle-Actions/action-phases.md) |
| `768`<sub>h</sub>, `76C`<sub>h</sub> | 8 | action fields the status record shows while acting | [party member status record](party-member-status-record.md) |
| `778`<sub>h</sub> | 520 | the target buffer (below) | [target selection](../Battle-Actions/target-selection.md) |
| `BA0`<sub>h</sub> | 2 | the issued command's action id | [party member status record](party-member-status-record.md) |
| `BC4`<sub>h</sub>, `BC8`<sub>h</sub> | 4 + `200`<sub>h</sub> | the perception candidate cache: count, then 16-byte entries | [enmity](../Enemy-AI-And-Gambits/enmity.md) |
| `DC8`<sub>h</sub> | 2 | the reserved consumed item, `FFFF`<sub>h</sub> when none | [command availability](../Battle-Actions/command-availability.md) |
| `E54`<sub>h</sub>, `E58`<sub>h</sub> | 8 | the gil the preview computed and the reserved gil cost | [command availability](../Battle-Actions/command-availability.md) |
| `E60`<sub>h</sub> | 8 | the definition row | [steal](../Damage-And-Battle-Formulas/steal.md) |
| `E68`<sub>h</sub> | 8 | the class row the status record reads `+52`<sub>h</sub> and `+12`<sub>h</sub> bit 7 from | [party member status record](party-member-status-record.md) |
| `E80`<sub>h</sub> | 16 | the innate augment source | [augments](../Damage-And-Battle-Formulas/augments.md) |
| `EA9`<sub>h</sub> | 1 | the slot index, written at bind | [battle units](battle-units.md) |

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

`00236A60(unit)` prepares a slot for its next occupant without releasing it:

1. when flag bit 4 is set it first runs `003105D0`;
2. it writes `FFFF`<sub>h</sub> at `+695`<sub>h</sub> and `FF`<sub>h</sub> at `+694`<sub>h</sub>, and clears flag bits 2, 3, 4, 8, 9, 10, 11
   and 14 (`and dword +0, FFFFB0E3h`), bits 34, 38 and 52 (`and dword +4, FFEFFFBBh`) and bits 1,
   19, 20, 33 and 47 (the register mask `FFFF7FFDFFE7FFFD`<sub>h</sub>);
3. it zeroes `+698`<sub>h</sub>, `+6A0`<sub>h</sub>, `+E60`<sub>h</sub>, `+E68`<sub>h</sub>, `+24`<sub>h</sub>-`+33`<sub>h</sub>, `+5C`<sub>h</sub>-`+63`<sub>h</sub>, the dword
   `+E54`<sub>h</sub>, `+EA4`<sub>h</sub>, `+EA8`<sub>h</sub>, `+DD0`<sub>h</sub>, `+64`<sub>h</sub>-`+6F`<sub>h</sub>, and sets `+74`<sub>h</sub> to all ones, `+55`<sub>h</sub>-`+56`<sub>h</sub>
   to `FFFF`<sub>h</sub>, `+52`<sub>h</sub> to 0 and `+54`<sub>h</sub> to `FF`<sub>h</sub>;
4. it resets the perception cache at `+BC0`<sub>h</sub> with `00316D30`, which forces header bit 0 on before
   its `208`<sub>h</sub>-byte clear and restores it after, and takes the resource accumulator `00320450`,
   which returns the dword `+70`<sub>h</sub> (only for a unit with flag bit 4, a stats record and no terminal
   status outside a town) and zeroes it;
5. it zeroes `+E80`<sub>h</sub>-`+E8F`<sub>h</sub>, `+E90`<sub>h</sub>, `+714`<sub>h</sub> to `FFFF`<sub>h</sub>, `+6B5`<sub>h</sub>, `+6D0`<sub>h</sub>, `+6E0`<sub>h</sub>-`+6FF`<sub>h</sub>,
   `+748`<sub>h</sub>-`+757`<sub>h</sub>, `+B90`<sub>h</sub>, the low byte of `+6B0`<sub>h</sub>, `+708`<sub>h</sub>-`+713`<sub>h</sub>, `+760`<sub>h</sub>-`+773`<sub>h</sub>, and
   sets `+758`<sub>h</sub> and `+DC8`<sub>h</sub> to all ones; the commit copy `+718`<sub>h</sub>-`+72F`<sub>h</sub> and the cancelled record
   `+730`<sub>h</sub>-`+747`<sub>h</sub> take the `+700`<sub>h</sub>-`+717`<sub>h</sub> bytes as they stand after those stores;
6. it zeroes the `610`<sub>h</sub> bytes from `+80`<sub>h</sub>, resets the navigation state (`003839F0` fills
   `+210`<sub>h</sub>-`+28F`<sub>h</sub> with `FF`<sub>h</sub>, `003839C0` sets `+20C`<sub>h</sub>-`+20F`<sub>h</sub> to `FFFF`<sub>h</sub>) and ends in
   `003176C0`, which zeroes the 32 dwords at `+DD4`<sub>h</sub>-`+E53`<sub>h</sub>.

The target buffer at `+778`<sub>h</sub> is not touched by the reuse reset.

### The navigation path state

Struct BattleUnitPathState base=unit+`200`<sub>h</sub> size=`490`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i32` | current | the waypoint index the walker is on (`00383670` reads and writes it) |
| `0C`<sub>h</sub> | `u16[2]` | endpoints | `FFFF`<sub>h</sub> after `003839C0` |
| `10`<sub>h</sub> | `u8[128]` | predecessor | the next waypoint after each index; `FF`<sub>h</sub> after `003839F0` |
| `90`<sub>h</sub> | `f32[2][128] waypoints` | x and z per index; 00383670 copies entry i to its output at +0 and +8 |  |

`00383670(position, _, out, state, arg)` follows the predecessor chain from `current` while
`00383A30` reports each step reached, calls `00383C90` for the chosen index, copies that waypoint's
two floats into `out` (with the position's y at `out + 4`) and stores the index back.

### The target buffer

Struct BattleTargetBuffer base=unit+`778`<sub>h</sub> size=`208`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | header | bit 0 survives the reset `00316CF0` |
| `01`<sub>h</sub> | `u8[2]` | cleared by the reset |  |
| `04`<sub>h</sub> | `i32` | count | at most 32; `00316CD0` appends at count and increments |
| `08`<sub>h</sub> | `u8[512]` | entries | 32 entries of 16 bytes: the actor at +0, the outcome word at +8 (target selection page) |

### Reset extents

| Clear | Range | Where |
|---|---|---|
| allocation | the whole `F50`<sub>h</sub> bytes | `00234480` before the bind |
| release | the whole `F50`<sub>h</sub> bytes | `00234200` after the spawn-record copy |
| reuse | `+80`<sub>h</sub>-`+68F`<sub>h</sub> zeroed, then `+20C`<sub>h</sub>-`+20F`<sub>h</sub> and `+210`<sub>h</sub>-`+28F`<sub>h</sub> set to all ones; the fields listed above | `00236A60` |
| perception cache | `+BC0`<sub>h</sub>-`+DC7`<sub>h</sub>, header bit 0 forced on | `00316D30` from the reuse reset |
| target buffer | `+778`<sub>h</sub>-`+97F`<sub>h</sub>, keeping header bit 0 | `00316CF0` |

## Related

- [Battle units](battle-units.md): the pool, the bind and the flag word.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md): the record at `+698`<sub>h</sub>.
- [Action commit](../Battle-Actions/action-commit.md), [action phases](../Battle-Actions/action-phases.md) and [target selection](../Battle-Actions/target-selection.md): the action block and the target buffer.
- [Enmity](../Enemy-AI-And-Gambits/enmity.md): the perception cache.
- [Party member status record](party-member-status-record.md): the fields the HUD reads.
