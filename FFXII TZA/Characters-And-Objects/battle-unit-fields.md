---
title: "Battle unit fields: the unit record offset by offset, its regions, and every reach the access table proves"
kind: "reference"
category: "Characters and objects"
addresses: "0x00234480, 0x00236A60, 0x00316CD0, 0x00316CF0, 0x003839F0, 0x003839C0, 0x00383670, 0x00234200, 0x00265020, 0x00329220"
---

## What it lists

A battle unit is the `0xF50`-byte combat record every fighting actor holds in the pool of 32
([battle units](battle-units.md)). This page lays the record out by region and names the fields
that a final page has established; the companion table `battle-unit-fields.tsv` lists every access to a unit:
through the pool `0x0208E688`, the accessors `0x00236820`, `0x00263E30`, `0x0031B7E0`, `0x0031B760`, `0x0031B860`, `0x0031B770` and
`0x002367A0`, the actor's `+0x30` pointer, and the pointers passed on from them, with the clears as `set` rows.

Every way to a unit was followed: the pool is loaded by `0x00234200`, `0x00234480`, `0x002367A0`, `0x00236820`, `0x002368D0` and
`0x00238B70`; the seven accessors' callers were followed, as were the 194 functions that take an actor in an argument
register ([actor record fields](actor-record-fields.md)); of the actor's twelve `+0x30` reads outside the accessors,
seven test the pointer for null and the rest are in the table.

### The regions

| Unit offset | Size | Region | Who establishes it |
|---|---|---|---|
| `+0x000` | 8 | the flag word (bit `0x1` slot in use; the bit table on the battle units page) | [battle units](battle-units.md) |
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
| `+0x6B0` | 4 | the command word: bit `0x2` a command issued and not yet committed | [action commit](../Battle-Actions/action-commit.md) |
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
| `+0xE68` | 8 | the class row the status record reads `+0x52` and `+0x12` bit `0x80` from | [party member status record](party-member-status-record.md) |
| `+0xE80` | 16 | the innate augment source | [augments](../Damage-And-Battle-Formulas/augments.md) |
| `+0xEA9` | 1 | the slot index, written at bind | [battle units](battle-units.md) |
| `+0x018` | 8 | fields the table shows 1 function writing and 1 reading at `+0x18` | this page |
| `+0x024-0x02C` | 16 | fields the table shows 9 functions writing and 6 reading at `+0x24`, `+0x28`, `+0x2C`; zeroed by the reuse reset | this page |
| `+0x038` | 8 | fields the table shows 1 function writing and 2 reading at `+0x38` | this page |
| `+0x040` | 8 | fields the table shows 1 function writing and 17 reading at `+0x40` | this page |
| `+0x04C-0x074` | 44 | fields the table shows 17 functions writing and 19 reading at 15 offsets; set to 0 by the reuse reset; set to 0xFF by the reuse reset; set to 0xFFFF by the reuse reset; zeroed by the reuse reset; set to all ones by the reuse reset | this page |
| `+0x690` | 4 | fields the table shows 10 functions writing and 5 reading at `+0x690` | this page |
| `+0x6B5-0x6B6` | 2 | fields the table shows 5 functions writing and 10 reading at `+0x6B5`, `+0x6B6`; zeroed by the reuse reset | this page |
| `+0x6C0` | 16 | fields the table shows 2 functions writing and 2 reading at `+0x6C0` | this page |
| `+0x6D0-0x6E0` | 32 | fields the table shows 9 functions writing and 4 reading at `+0x6D0`, `+0x6D4`, `+0x6D8`, `+0x6DC`, `+0x6E0`; zeroed by the reuse reset | this page |
| `+0x6E8` | 8 | fields the table shows 4 functions writing and 1 reading at `+0x6E8`; zeroed by the reuse reset | this page |
| `+0x6F0` | 16 | fields the table shows 3 functions writing and 2 reading at `+0x6F0`; zeroed by the reuse reset | this page |
| `+0x6F8` | 8 | fields the table shows 8 functions writing and 1 reading at `+0x6F8`; zeroed by the reuse reset | this page |
| `+0x710-0x714` | 6 | fields the table shows 5 functions writing and 55 reading at `+0x710`, `+0x714`; zeroed by the reuse reset; set to 0xFFFF by the reuse reset | this page |
| `+0x728` | 8 | fields the table shows 2 functions writing and 1 reading at `+0x728` | this page |
| `+0x748-0x764` | 36 | fields the table shows 14 functions writing and 5 reading at 8 offsets; zeroed by the reuse reset; set to all ones by the reuse reset | this page |
| `+0x774` | 4 | fields the table shows 3 functions writing and 2 reading at `+0x774` | this page |
| `+0x988` | 8 | fields the table shows 1 function writing and 2 reading at `+0x988` | this page |
| `+0xB30` | 16 | fields the table shows 1 function writing and 1 reading at `+0xB30` | this page |
| `+0xB40` | 16 | fields the table shows 1 function writing and 1 reading at `+0xB40` | this page |
| `+0xB50` | 16 | fields the table shows 1 function writing and 1 reading at `+0xB50` | this page |
| `+0xB60` | 16 | fields the table shows 1 function writing and 1 reading at `+0xB60` | this page |
| `+0xB70` | 16 | fields the table shows 1 function writing and 1 reading at `+0xB70` | this page |
| `+0xB80` | 16 | fields the table shows 1 function writing and 1 reading at `+0xB80` | this page |
| `+0xB88` | 8 | fields the table shows 1 function writing and 1 reading at `+0xB88` | this page |
| `+0xB90` | 16 | fields the table shows 2 functions writing and 1 reading at `+0xB90`; zeroed by the reuse reset | this page |
| `+0xBA4` | 2 | fields the table shows 1 function writing and 1 reading at `+0xBA4` | this page |
| `+0xBB8` | 4 | fields the table shows 1 function writing and 1 reading at `+0xBB8` | this page |
| `+0xBC0-0xBC1` | 3 | fields the table shows 3 functions writing and 7 reading at `+0xBC0`, `+0xBC1` | this page |
| `+0xDCC-0xDD4` | 12 | fields the table shows 8 functions writing and 4 reading at `+0xDCC`, `+0xDD0`, `+0xDD4`; zeroed by the reuse reset; zeroed by 0x003176C0 from the reuse reset | this page |
| `+0xE70` | 8 | fields the table shows 1 function writing and 4 reading at `+0xE70` | this page |
| `+0xE78` | 8 | fields the table shows 1 function writing and 4 reading at `+0xE78` | this page |
| `+0xE90` | 4 | fields the table shows 2 functions writing and 2 reading at `+0xE90`; zeroed by the reuse reset | this page |
| `+0xE98-0xEB0` | 28 | fields the table shows 12 functions writing and 20 reading at 9 offsets; zeroed by the reuse reset | this page |
| `+0xED0` | 1 | fields the table shows 0 functions writing and 1 reading at `+0xED0` | this page |

## Columns

`battle-unit-fields.tsv`, one row per access site:

| Column | Meaning |
|---|---|
| `function` | the function containing the instruction |
| `name` | the name the scan carried for that function; blank or `FUN_` when none was assigned |
| `site` | the instruction's address |
| `disp` | the unit offset reached |
| `kind` | `r` read, `w` write, `rw` read-modify-write, `addr` the address is formed and passed on, `set` a clear over the span the instruction cell gives |
| `instruction` | the instruction text |
| `route` | how the function reached the unit: `0x0208E688` when it indexes the pool itself (`0x0208E688 (the slot acquire)` for the free-slot walk), an accessor's address when it took that accessor's return, `actor +0x30, the actor as argN from F at S` when it loaded the unit from an actor it was handed, `argN from F at S` when the unit came in as argument N (0 = `rcx`, 1 = `rdx`, 2 = `r8`, 3 = `r9`) from the caller F at the call site S, `argN+0xK` when it came in offset by K, and `sweep` for the two `+0x768`/`+0x76C` pairs found by an image-wide displacement sweep and verified at the site |
| `note` | `idx` when an index register takes part |

## Data

### The reuse reset

`0x00236A60(unit)` prepares a slot for its next occupant without releasing it:

1. when flag bit `0x10` is set it first runs `0x003105D0`;
2. it writes `0xFFFF` at `+0x695` and `0xFF` at `+0x694`, and clears flag bits `0x4`, `0x8`, `0x10`, `0x100`, `0x200`, `0x400`, `0x800`
   and 14 (`and dword +0, 0xFFFFB0E3`), bits `0x400000000`, `0x4000000000` and `0x10000000000000` (`and dword +4, 0xFFEFFFBB`) and bits `0x2`,
   19, 20, 33 and 47 (the register mask `0xFFFF7FFDFFE7FFFD`);
3. it zeroes `+0x698`, `+0x6A0`, `+0xE60`, `+0xE68`, `+0x24`-`+0x33`, `+0x5C`-`+0x63`, the dword
   `+0xE54`, `+0xEA4`, `+0xEA8`, `+0xDD0`, `+0x64`-`+0x6F`, and sets `+0x74` to all ones, `+0x55`-`+0x56`
   to `0xFFFF`, `+0x52` to 0 and `+0x54` to `0xFF`;
4. it resets the perception cache at `+0xBC0` with `0x00316D30`, which forces header bit `0x1` on before
   its `0x208`-byte clear and restores it after, and takes the resource accumulator `0x00320450`,
   which returns the dword `+0x70` (only for a unit with flag bit `0x10`, a stats record and no terminal
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
| `+0x90` | `f32[2][128]` | waypoints | x and z per index; `0x00383670` copies entry i to its output at +0 and +8 |

`0x00383670(position, _, out, state, arg)` follows the predecessor chain from `current` while
`0x00383A30` reports each step reached, calls `0x00383C90` for the chosen index, copies that waypoint's
two floats into `out` (with the position's y at `out + 4`) and stores the index back.

### The target buffer

Struct BattleTargetBuffer base=unit+`0x778` size=`0x208`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | header | bit `0x1` survives the reset `0x00316CF0` |
| `+0x01` | `u8[2]` | cleared by the reset |  |
| `+0x04` | `i32` | count | at most 32; `0x00316CD0` appends at count and increments |
| `+0x08` | `u8[512]` | entries | 32 entries of 16 bytes: the actor at +0, the outcome word at +8 (target selection page) |

### Reset extents

| Clear | Range | Where |
|---|---|---|
| allocation | the whole `0xF50` bytes | `0x00234480` before the bind |
| release | the whole `0xF50` bytes | `0x00234200` after the spawn-record copy |
| reuse | `+0x80`-`+0x68F` zeroed, then `+0x20C`-`+0x20F` and `+0x210`-`+0x28F` set to all ones; the fields listed above | `0x00236A60` |
| perception cache | `+0xBC0`-`+0xDC7`, header bit `0x1` forced on | `0x00316D30` from the reuse reset |
| target buffer | `+0x778`-`+0x97F`, keeping header bit `0x1` | `0x00316CF0` |

In both target buffers, the header byte `+0x03` and the last four bytes `+0x0C`-`+0x0F` of each 16-byte entry go with the buffer as a block. The buffer clears zero them with the rest of the `0x208` bytes (`0x00316CF0`, memset at `0x00316D0B`; the perception cache's `0x00316D30`, memset at `0x00316D4E`). For the buffer at `+0x778`, `0x0030EDA0` copies them back with the action state `+0x6B0`-`+0xB9F` in its 16-byte stores (`0x0030EDB6`-`0x0030EE44`).

The entry's outcome word at `+0x08` is a dword in the code: `0x002FFA14`, `0x0030019B`, `0x00300EAD` and `0x003011E0` clear its bit `0x400` with an `and dword`, and `0x0030071A` loads it as a dword.

### The spans between named fields

The unit bytes between the named fields, by range. The locomotion block at `+0x80` is the solver's argument (`0x00336CE0`), so its offsets are given in block terms as well; the action state `+0x6B0`-`+0xB9F` is the `0x4F0` bytes `0x0030EDA0` restores from the saved block at `[+0xB88]`.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00C` | `u8[4]` | span000C | the four bytes between the actor handle +0x08 and the bound actor record +0x10; the slot acquire 0x00234480 zeroes the whole 0xF50-byte slot (0x002344C7-0x002344D2) |
| `+0x020` | `i32` | bound | 1 after the bind walk: 0x00265A20 calls 0x00234A00(unit, 1) for a unit whose actor's +0x30 is set (0x00265AA4-0x00265AB4), and 0x00234A00 stores it (0x00234A00) |
| `+0x034` | `u8[4]` | span0034 | the four bytes after the killer id +0x30; zeroed with the slot by 0x00234480 (0x002344D2) |
| `+0x059` | `u8[3]` | span0059 | the three bytes after +0x58 (the entry group is +0x57), before the qword the reuse reset 0x00236A60 clears at +0x5C (0x00236AF8); zeroed with the slot by 0x00234480 (0x002344D2) |
| `+0x078` | `u8[8]` | span0078 | the eight bytes before the locomotion block at +0x80, after the fields the reuse reset clears at +0x64-+0x6F (0x00236B41, 0x00236B45); zeroed with the slot by 0x00234480 (0x002344D2) |
| `+0x0C4` | `u8[12]` | span00C4 | bytes +0x44 to +0x4F of the locomotion block at +0x80 (the block the solver 0x00336CE0 takes as its argument), after its goal kind +0x40; zeroed by the reuse reset 0x00236A60 with +0x80-+0x68F (0x00236B12-0x00236BF0) |
| `+0x0FC` | `u8[4]` | span00FC | the fourth dword of the locomotion block's step point +0x70 (unit +0xF0): the solver context copies only its x, y and z and sets its own w to 1.0 (0x00336757-0x00336769); zeroed by the reuse reset (0x00236BF0) |
| `+0x120` | `u8[32]` | span0120 | bytes +0xA0 to +0xBF of the locomotion block, between its destination +0x90 and the detour point copy +0xC0; zeroed by the reuse reset (0x00236BF0) |
| `+0x14C` | `u8[4]` | span014C | the fourth dword after the locomotion block's detour point copy +0xC0-+0xC8, which the solver 0x00336CE0 writes as three floats (0x00336DE1-0x00336DFD); zeroed by the reuse reset (0x00236BF0) |
| `+0x1B4` | `u8[12]` | span01B4 | bytes +0x134 to +0x13F of the locomotion block, between its sidestep odds +0x130 and its direction +0x140; zeroed by the reuse reset (0x00236BF0) |
| `+0x1D4` | `u8[12]` | span01D4 | bytes +0x154 to +0x15F of the locomotion block, between its target handle +0x150 and its goal kind +0x160; zeroed by the reuse reset (0x00236BF0) |
| `+0x1E4` | `u8[12]` | span01E4 | bytes +0x164 to +0x16F of the locomotion block, between its goal kind +0x160 and its flags +0x170 (unit +0x1F0); zeroed by the reuse reset (0x00236BF0) |
| `+0x1F8` | `u8[8]` | span01F8 | the eight bytes between the locomotion block's slot byte +0x177 (unit +0x1F7) and the navigation path state at +0x200; zeroed by the reuse reset (0x00236BF0) |
| `+0x697` | `u8` | span0697 | the byte after the three bytes +0x694-+0x696 the reuse reset sets to 0xFF and 0xFFFF, before the combat stats record pointer +0x698; zeroed with the slot by 0x00234480 (0x002344D2) |
| `+0x6A8` | `u8[8]` | span06A8 | the eight bytes between the spawn record pointer +0x6A0 and the command word +0x6B0; zeroed with the slot by 0x00234480 (0x002344D2) |
| `+0x6BA` | `u8[6]` | span06BA | bytes +0x6BA to +0x6BF at the head of the action state +0x6B0-+0xB9F, which 0x0030EDA0 restores as a whole from the saved block at [+0xB88] (the copy loop 0x0030EDB6-0x0030EE07 nine times 0x80 bytes, then 0x70 bytes at 0x0030EE09-0x0030EE44) |
| `+0x704` | `u8[4]` | span0704 | bytes 4 to 7 of the action block +0x700, copied with it to the commit copy +0x718 and the cancelled copy +0x730 by the reuse reset (0x00236B5C-0x00236B80); restored with the action state by 0x0030EDA0 (0x0030EDEF) |
| `+0x716` | `u8[2]` | span0716 | the two bytes after the action id +0x714, copied with the target focus handle +0x710 as one qword to +0x728 and +0x740 (0x00236B6A-0x00236B95); restored by 0x0030EDA0 (0x0030EDF7) |
| `+0x746` | `u8[2]` | span0746 | the cancelled copy's counterpart of +0x716, written by the qword copies into +0x740 (0x00236B8D; 0x003105D0 at 0x003106E3); restored by 0x0030EDA0 (0x0030EDCF, 0x0030EE1A) |
| `+0x75A` | `u8[2]` | span075A | the two bytes after the word +0x758 the reuse reset sets (0x00236BD9); restored by 0x0030EDA0 (0x0030EDD7, 0x0030EE22) |
| `+0x980` | `u8[8]` | span0980 | the eight bytes after the target buffer +0x778-+0x97F, inside the action state 0x0030EDA0 restores (0x0030EDEF, 0x0030EE3A) |
| `+0xB94` | `u8[12]` | span0B94 | the last twelve bytes of the action state +0x6B0-+0xB9F, after the dword +0xB90 the reuse reset clears (0x00236BE0); restored by 0x0030EDA0's tail copy (0x0030EE44) |
| `+0xBBC` | `u8[4]` | span0BBC | the four bytes between +0xBB8 and +0xBC0, before the perception candidate count +0xBC4; outside the 0x4F0 bytes 0x0030EDA0 restores (they end at +0xB9F) |
| `+0xDCA` | `u8[2]` | span0DCA | the two bytes after the reserved consumed item +0xDC8 (set to 0xFFFF by the reuse reset, 0x00236AFC), just past the 32 entries of the perception cache +0xBC8-+0xDC7 |
| `+0xE5C` | `u8[4]` | span0E5C | the four bytes between the reserved gil cost +0xE58 and the definition row pointer +0xE60; zeroed with the slot by 0x00234480 (0x002344D2) |
| `+0xE94` | `u8[4]` | span0E94 | the four bytes after the dword +0xE90 the reuse reset clears (0x00236B19), before +0xE98; zeroed with the slot by 0x00234480 (0x002344D2) |
| `+0xE9B` | `u8` | span0E9B | the byte after +0xE98-+0xE9A, before +0xE9C; zeroed with the slot by 0x00234480 (0x002344D2) |
| `+0xEAA` | `u8[2]` | span0EAA | the two bytes after the slot index +0xEA9, before +0xEAC; zeroed with the slot by 0x00234480 (0x002344D2) |
| `+0xEB4` | `u8[156]` | tail0EB4 | the bytes from +0xEB4 to the end of the 0xF50-byte unit; 0x0031AD90 returns the address +0xED0 inside them (0x0031AD92); zeroed with the slot by 0x00234480 (0x002344D2) |

### The action snapshot slots

The saved block at `[+0xB88]` is one of 8 slots of `0x4F0` bytes at `0x022BEFC0`; the byte `0x022BEFB0` marks the slots in
use, one bit per slot.

The engage auto-attack `0x00312FA0` calls `0x0030EFF0(unit)` (`0x0031307B`). Unless flag bit `0x1000000` is
set, or the action id `+0x714` is at most `0x21E` with `+0x6B4` at 6 or more, it takes a free slot from `0x0030DFA0`
(`0x0030F02A`), copies the action state `+0x6B0`-`+0xB9F` into it, clears the action state and stores the slot at
`+0xB88` (`0x0030F0F1`). With all 8 slots taken, `0x0030DFA0` returns 0 and nothing is saved.

The next-action selector's
`0x00308270` calls `0x0030EDA0` (`0x003082C6`), which copies the slot back and frees its bit.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022BEFB0` | `u8` | 0 (zero-filled tail of `.data`) | the slots in use: bit n set while slot n (`0x022BEFC0 + 0x4F0 x n`) holds a unit's suspended action state | `0x0030DFA0`, the free slot's bit on (`0x0030DFF7`, `bts`; address formed at `0x0030DFA2`); `0x0030EDA0`, the restored slot's bit off (`0x0030EE97`, `btr`; address formed at `0x0030EE82`); `0x0030E010`, all 8 bits off (`0x0030E04C`), from the area initialisation `0x002342F0` (`0x0023439C`) | `0x0030DFA0` (`0x0030DFD2`, `0x0030DFEE`); `0x0030EDA0` (`0x0030EE8C`); `0x0030E010` (`0x0030E010`) |

## Related

- [Battle units](battle-units.md): the pool, the bind and the flag word.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md): the record at `+0x698`.
- [Action commit](../Battle-Actions/action-commit.md), [action phases](../Battle-Actions/action-phases.md) and [target selection](../Battle-Actions/target-selection.md): the action block and the target buffer.
- [Enmity](../Enemy-AI-And-Gambits/enmity.md): the perception cache.
- [Party member status record](party-member-status-record.md): the fields the HUD reads.
