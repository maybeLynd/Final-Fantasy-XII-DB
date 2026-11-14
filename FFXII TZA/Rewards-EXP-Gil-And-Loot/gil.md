---
title: "Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters"
kind: "system"
category: "Rewards: EXP, LP, gil and loot"
addresses: "0x00253690, 0x00254EE0, 0x003004B0, 0x00300500, 0x00316A50, 0x00309060, 0x002F95D0, 0x00312280, 0x003F4AA0, 0x0050FAF0, 0x002524C0"
---

## What the player sees

Gil goes up from defeated enemies, chests, selling, quest rewards, story scripts and a character's
first join, and down when buying. It never
goes below 0 and stops at 99,999,999. A party member with "Enables casting of magicks with gil, rather
than MP." (the Turtleshell Choker) pays for magicks in gil. A member with "Convert all license points
earned to gil." (the Cat-ear Hood) turns the LP from each kill into gil. The game keeps two hidden totals, gil gained and gil spent; the
first unlocks the Steam achievement **Plunderer** and the second **Spendthrift**.

Every change of gil passes through one setter, which adds a gain to the gil-gained total or a loss to the gil-spent
total before it stores the new amount. The amounts that unlock Plunderer (100,000 gained) and Spendthrift (1,000,000
spent) are read from the handbook file `menuhandbook.bin`, not from the program.

## How it works

### Storage

Gil is a signed 32-bit value at `+0x08` of the game-state block whose address is held in
`0x02092758`. `0x00253690` reads it (`mov rax, [0x02092758]; mov eax, [rax+8]`).

### The setter

The setter is `0x00254EE0(newValue)`, and every row of Operations reaches it. The save header is the start of the
save image at `0x02164280` (`0x0025397E` stores that address in `[0x02092758]`), and block writes of the image replace
gil without the setter: `0x002EF650` and `0x002EF5F0` zero its `0x56690` bytes (`0x002EF663`, `0x002EF603`), `0x00253A80`
zeroes its first `0x58` bytes (`0x00253A93`), `0x00583C00` copies `0xE240` bytes over it (`0x00583C30`-`0x00583C9D`), and
`0x002EF300` requests a read of `0xE240` bytes of a file into it (`0x002EF317`-`0x002EF336`).

The setter does this:

```c
delta = newValue - gil;                         // 0x00254EF1, on the raw argument
if (delta > 0)      meter(6, delta);            // 0x00254EF8: gained
else if (delta < 0) meter(7, -delta);           // 0x00254EFE-0x00254F00: spent
                                                // delta 0: no meter call (0x00254EF6 jle, 0x00254EFC jns)
v = newValue < 0 ? 0 : newValue;                // 0x00254F10 cmovns
if (v > 99999999) v = 99999999;                 // 0x00254F15 cmovg against 0x05F5E0FF
gil = v;                                        // 0x00254F1F
```

The change is measured before the clamp, so a caller that passes 200,000,000 meters the full
difference even though only 99,999,999 is stored. Most callers floor their value at 0 themselves
before calling the setter (see Operations), so for them the spent amount never exceeds the balance.

### The meter

`0x00316A50(kind, amount)` keeps the gained and spent totals. It ignores kinds above 29
(`0x00316A50 cmp cl, 0x1E`). Each kind has an 8-byte row at `0x00D10460 + kind*8`.

| Kind | Total | Where | Saturates at |
|---|---|---|---|
| 6 | gil gained | `[0x020927C0] + 0x3860` | `0x7FFFFFFF` |
| 7 | gil spent | `[0x020927C0] + 0x3864` | `0x7FFFFFFF` |

The slot is base `0x384C` plus the row's offset byte, read by `0x003166F0` and written by `0x00316BF0`.
For one call the meter does, in order:

1. Computes the new saturating total.
2. Calls `0x00315E90(kind)`, the achievement check, which reads the total stored so far (`0x00316760`),
   before the new one is written.
3. Stores the new total (`0x00316BF0`).

### The achievement check

`0x00315E90(kind)` returns at once if the kind's bit is already set in the done-bitset at
`[0x020927C0] + 0x3844`. Otherwise it compares the stored total with the kind's threshold. On reaching
it, it sets the bit and calls `0x008632B0` with the achievement id from `0x00D10550 + kind*4`: 8 for kind
6 and 10 for kind 7.

`0x008632B0` unlocks the Steam achievement through `0x0020CE60`, which marks the achievement record
(`+0x190` = 1) and calls Steam's user-stats interface (vtable `+0x38`, then `+0x50`). Records 8 and
10 of the achievement descriptor table `0x01DFE410` are `ACH_COUNT_GET_GIL` "Plunderer" (`0x01DFF0D0`)
and `ACH_COUNT_USE_GIL` "Spendthrift" (`0x01DFF400`); each record's first dword is its counter kind, 6
and 7.

The meter runs only for the kind matching the change's direction, and its own check reads the total from
before the update, so the change that reaches a threshold does not unlock the achievement by itself.

The end-of-field-frame sweep `0x00316930` evaluates descriptors 0-29 with the stored totals (`0x00316A36`-`0x00316A43`),
kinds 6 and 7 among them (mode 0, `0x00D10490`, `0x00D10498`), so Plunderer and Spendthrift unlock at the first
sweep after the stored total reaches the threshold, with no further gain or spend
([achievements](../Steam-And-Achievements/achievements.md#the-sweep-and-the-re-send)).

### The thresholds

The thresholds come from the handbook file `menuhandbook.bin`, loaded raw into `[0x022C2550]` by
`0x003158B0` (resource 7, 200). `0x003165C0(kind)` follows four 16-bit relative offsets from file
`+0x08`, then reads a kind bitmask at `+4` and packed 32-bit values at `+8`. When the kind's bit is
clear it returns 0 (`0x0031661A`-`0x0031661C`). Its callers then take the row's dword at `0x00D10464 + kind*8`
(`0x00315F24`-`0x00315F28`, `0x00316AFD`-`0x00316B01`), which is 0 for kinds 6 and 7.

In the shipped files of every language the gained threshold is **100,000** and the spent threshold
is **1,000,000**.

### Gil as an action cost

`0x00309060(unit, action)` returns the gil cost of an action. It returns 0 when any of these holds:

- the unit is an enemy (stats byte `+0x05` = 1);
- the action id is above `0x21E`;
- the action's row in the action table `[0x02EBF138]` has byte `+0x1E` equal to 5 or 6;
- `0x002F9820` does not report the unit as a party member with augment 32 (Offering), bit `0x1` of stats byte
  `+0x6C` or `+0x7C`.

A null unit, or a unit with no record at `+0x698`, does not take the enemy exit and goes on to the
other tests (`0x00309070`-`0x0030907F`). The action row is the low 32 bits of the `0x0020E600` answer for
the dword `+0x0C` of `[0x02EBF138]`, plus the id times the table's word `+0x08` (`0x0030909D`-`0x003090CA`).
With a null `[0x02EBF138]` or a null answer the row address is 0 and the byte is read at address `0x1E`
(`0x00309098`-`0x003090A8`, `0x003090CE`-`0x003090D0`).

Augment row 32's description (id 13032) reads "Enables casting of magicks with gil, rather than
MP.", and the shipped equipment row with augment byte `+0x1A` = 32 is the Turtleshell Choker
(`0x1166`).

Otherwise it returns `0x002F95D0(unit, action)`. With `b` the action row's byte `+0x0A`:

```python
cost = b                            # action ids 0xD0-0xE1 and 0x106-0x112
cost = trunc(b * 64.0 / 50.0) * 10  # every other action
```

### The gil a kill pays

In `0x00312280`, after EXP and LP are handed out:

```c
gil += (enemyStats.b[+0x1C2] - enemyStats.b[+0x88]) * [[enemy+0xE78] + 0x30]
     + [[enemy+0xE70] + 0x30]
     + conversion;                              // 0x0031251D-0x00312549
```

`conversion` adds `level × LP × 5` for each recipient whose stats byte `+0x69` or `+0x79` has bit
`0x10` set. Here `level` is the recipient's byte `+0x1C2` and `LP` is that recipient's share capped
at 999. Such a recipient receives no LP from the kill. This sits under the same reward gate as EXP and
LP (`+0xE9A` and the killer test, see [EXP, LP and level-ups](exp-lp-and-level-ups.md)). The total is floored at 0 and stored through
the setter (`0x00312553`-`0x0031255D`), and the difference is posted as a gain notification (`0x00312566`).

### The gain notification

`0x00469E80(amount)` posts message `0x26` through `0x0046AB10` when the amount
is positive, and does nothing otherwise.
The amount is the dword `+0x10` of a zeroed `0x30`-byte context on its stack, passed as
`0x0046AB10(0, 0x26, context)` (`0x00469E87`-`0x00469EB2`).

## Layouts

### The quest result window

The quest result window is the `0x100`-byte widget with procedure `0x003F4E70` that `0x003F4BD0` builds for the reward record and that keeps itself at `0x02B5F200`.

`QuestResultWindow` (`0x100` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x003F4E70` |
| `+0xC0` | `u8` | skipSetup | the first byte of the creation record (`0x003F4F7E`, `0x003F4F81`); the only creator, `0x003F4BD0`, passes 0 (`0x003F4BED`). While it is 0 the construct message marks the image `0x01E0C1F8` (its `+0x38` bit `0x80`), runs `0x00252B40`(9, 1) and `0x0037F3B0` (`0x003F4FE8`-`0x003F5014`); message 16 for batch 1 passes `+0xC4` to `0x0037EDB0` and keeps `0x0037E8A0`'s result at `+0xC8` (`0x003F4F07`-`0x003F4F29`); message 18 restores the saved `+0xF4` / `+0xF8` through `0x00252B40` and clears the image bit (`0x003F4EAD`); `0x003F4B40` runs `0x0037E4F0`(0) before closing the window (`0x003F4B50`) |
| `+0xC1` | `u8[63]` | window | the window's own fields: `+0xC4` the creation record's dword `+0x10`, `+0xC8` what `0x0037E8A0` returns, `+0xD0`-`+0xF3` the `0x24` bytes the creation record points to, `+0xF4` and `+0xF8` the saved `0x02092730` and bit `0x1` of `0x02092734` (`0x003F4F87`-`0x003F4FE2`); bit `0x2` of `+0xF8` is cleared by the construct message (`0x003F4FAC`) and set by `0x003F4DD0` (`0x003F4E44`) |

The procedure `0x003F4E70` handles messages 1, 2, 16 and 18 and answers 0 for each; any
other message goes to `0x005C5230` (`0x003F4E79`-`0x003F4E9F`). Message 1 ends with
`0x00244960([0x0208EA28], window)` whatever `+0xC0` holds (`0x003F5019`-`0x003F5023`). Message
16 also runs `0x003F4DD0(window)` after storing `+0xC8` (`0x003F4F26`-`0x003F4F30`).

`0x003F4DD0` starts the grant list `0x003F4840` as a `0x130`-byte widget, `0x00244F50(0x130, 0x003F4840, record)`.
The record's dword `+0x00` and qword `+0x10` are 0, and its qword `+0x08` points at four stack qwords:
the window's `+0xC8`, the address of its `+0xD0`, the address of a zeroed `0x18`-byte block and 0
(`0x003F4DEA`-`0x003F4E3F`). It then sets bit `0x2` of the window's dword `+0xF8` and does not read the
call's answer (`0x003F4E44`).

Message 2 closes the window with `0x00244F00` only when bit `0x2` of `+0xF8` is set and
the window at `0x02B5F1F8` is absent or has its byte `+0xC0` at 3 (`0x003F4F3D`-`0x003F4F66`).
Message 18 runs `0x0037E4F0(0)` before the restore, makes the restore only when `+0xF4`
is not -1 and `+0xC0` is 0, and always zeroes `0x02B5F200` (`0x003F4EA4`-`0x003F4EE9`).

## Operations

Every function that changes gil: the callers of the setter and of its two wrappers, with the call site.

| Function | Call | What it does to gil |
|---|---|---|
| `0x00312280` | `0x0031255D` | adds the kill's gil (formula above), then notifies |
| `0x0050FAF0` | via `0x003004B0` | the chest payout, Start of script verb `btlAtelOpenTreasureMessage`: when `0x002FAFD0` reports a gil chest, adds its amount through `0x003004B0(amount, 0)` (no notification) |
| `0x003004B0` | `0x003004D6` | `v` = the 32-bit sum `gil + delta`, or 0 when it is negative, which includes a sum past 2,147,483,647 that wraps (`0x003004C3`-`0x003004D1`), sets `v`, which the setter stores capped at 99,999,999; when argument 2 bit `0x1` is set, notifies `v - old` (`0x003004DB`-`0x003004E5`); returns `v`, not the stored balance (`0x003004EF`) |
| `0x00300500` | `0x0030050F` | floors its argument at 0, sets, returns the floored value |
| `0x00316DF0` | via `0x003004B0` (`0x00317034`) | a party-side character's first activation (record flag `0x10` clear; character type 0-25, record flag `0x8` clear): grants the ten items at `+0x58` with counts at `+0x34` of the character row in `[0x02EBF130]` (row = type byte `+4`), then adds the row's u16 `+0x3E` as gil when non-zero |
| `0x0032A7F0` | via `0x003004B0` (`0x0032A7F2`, jump) | `0x003004B0(n, 0)`; called by the script verbs `addgill` (`0x2E7`, `0x00346943` in `0x00346930`) with `n` and `subgill` (`0x2E8`, `0x00346E30`) with `-n` |
| `0x00239960` | via `0x00300500` (`0x00239B1D`) | applying a SetSaveData preset sets gil to the preset row's u16 `+0x0E` (an absolute set) |
| `0x0032A800` | via `0x00300500` (`0x0032A802`, jump) | `0x00300500(n)`; called by the script verb `debug_setgill` (`0x0A3` in family 2, `0x0050DEF2` in `0x0050DEE0`) |
| `0x002FEEB0` | `0x002FEEF3` | shop purchase: adds the item through `0x003008A0(item, count, 0, 1, flags)`, then gil = max(gil - price, 0); notifies when flags bit `0x1` is set |
| `0x00310870` | `0x003108BD` | shop sale: removes the item through `0x003008A0(item, -count, 0, 1, flags)`, gil = max(gil + price, 0), notifies when flags bit `0x1` is set, then records the sale with `0x003008A0(item, count, 0, 3, 0)` |
| `0x002FD530` | `0x002FD5C0` | inventory class 14 (id nibble 9, ids `0x9000`+; descriptor record 9, handler slot `0x01EEC020`): on a mode-1 add, gil += row dword `+0` × count from table `[0x02EBF070]` row `id - 0x9000`, then notifies `new - old` when the flags argument has bit `0x1` set (`0x00469E80`), then grants the row's items at `+4` and `+8` |
| `0x002FD880` | `0x002FD8B4` | inventory class 19 (id nibble `0xE`; descriptor record 14, handler slot `0x01EEC1D8`): on a mode-1 add, gil += `(id & 0xFFF)` × count |
| `0x003F4AA0` | `0x003F4AC1` | applies a reward record: when bit `0x1` of byte `+0` is set, gil += dword `+4` (not floored before the setter; the setter's clamp applies); then grants the `+0x08`-counted `{item, count}` list at `+0x0C` and the `+0x0A`-counted single items at `+0x1C` through `0x00300B80` |
| `0x0030EF20` | `0x0030EFD8` | reserves an action's gil cost: stores `0x00309060`'s result at unit `+0xE58` (`0x0030EFC0`), then gil = max(gil - cost, 0) |
| `0x00300280` | `0x003002F0` | refunds a party unit's reservation: gil = max(gil + `[unit+0xE58]`, 0), then clears `+0xE58` |
| `0x00305640` | `0x0030572B` | consumes an action: clears a party unit's reservation `+0xE58` without refunding it (so the reserved deduction stands), then, for any unit, gil = max(gil - `[unit+0xE54]`, 0) as a separate charge; `+0xE54` is field `+0x08` of the action's result evaluated per target, stored by `0x00303954` (in `0x00303830`) and `0x00303B2E` (in `0x00303A00`), the last target's value standing |
| `0x003112F0` | `0x00311A9E` | applies a result: when the result's dword `+0x08` is non-zero, gil = max(gil - value, 0) (`0x00311A84`-`0x00311A9E`) |
| `0x003058B0` | `0x003058B5` (jump) | sets gil to 99,999,999 (`mov ecx, 0x05F5E0FF; jmp 0x00254EE0`); called from `0x001D3E9C`, `0x0023E168` and `0x00240BAE` |

The reward record applier `0x003F4AA0` is called only by `0x00290130`, which fetches the record
(`0x003F8C60`), applies it and posts message `0x100` (`0x003F4BD0`). `0x00290130` is reached through the
thunk `0x002E1A50` (`jmp 0x00290130`), called at `0x00344C9A` in `0x00344C60`, the Start handler of the script
verb `questresultwindow` (`0x37C`).

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `[0x02092758] + 0x08` | `i32` | gil, 0-99,999,999 by the setter | `0x00254EE0` (`0x00254F1F`); with the whole save image `0x002EF650`, `0x002EF5F0`, `0x00253A80`, `0x00583C00`, `0x002EF300` |
| `[0x020927C0] + 0x3860` | `i32` | gil gained, saturating at `0x7FFFFFFF` | `0x00316BF0` for kind 6 |
| `[0x020927C0] + 0x3864` | `i32` | gil spent, saturating at `0x7FFFFFFF` | `0x00316BF0` for kind 7 |
| `[0x020927C0] + 0x3844` | bits | counters whose achievement has fired (bit `1 << kind`) | `0x00316A50`, `0x00315E90` |
| unit `+0xE58` | `i32` | gil reserved for the action being carried out | `0x0030EFC0`; cleared by `0x00300280`, `0x00305640` |
| unit `+0xE54` | `i32` | gil amount from the action's result evaluation, deducted on consume | `0x00303954`, `0x00303B2E` |

## Modding notes

- The cap is the constant `0x05F5E0FF` in `0x00254EE0` (`0x00254F09`) and in `0x003058B0`; it is not data.
- The shop's rolling gil total carries the same constant twice: `0x002A1DC0` flags a roll whose end
  passes it, and `0x002524C0(current, change)` returns the change to roll: 99,999,999 for a current
  above the cap, 0 for a negative current, the current itself when the change would go below 0,
  `99,999,999 - current` when the sum would pass the cap, else the change. Raising the cap means
  patching these too.
- When the change would take the total below 0, the change `0x002524C0` tests against the cap is the current, so a
  current of 50,000,000 or more gives `99,999,999 - current` instead of the current (`0x002524DC`-`0x002524F8`).
- Writing `[0x02092758] + 8` directly skips both the clamp and the gained/spent totals. Write through
  `0x00254EE0`, or `0x003004B0` for a relative change.
- The Plunderer and Spendthrift thresholds are in `menuhandbook.bin`, the record reached through the
  four offsets from file `+0x08` (file offset `0xFC` in every language folder except `us`, where it is
  `0xF8`). They are not in the executable.
- The gil price of abilities under the gil-cost effect is `trunc(MP cost × 1.28) × 10`, computed from the
  action row's byte `+0x0A` in `0x002F95D0`. The two id ranges that charge the raw byte are hard-coded
  there.
- A kill's gil comes from the enemy's two records at `+0xE70` and `+0xE78` (dword `+0x30` of each)
  and the level difference in its stats.

## Related

- [EXP, LP and level-ups from kills: who receives them, the formulas, the split, the doublers and the EXP table](exp-lp-and-level-ups.md)
- [Kill chain: chain count, chain level, the chain coin and resets](kill-chain.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](loot-drops.md)

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Save load settings: `0x002EF650` is called by `0x00280140`; those functions are documented on
  [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md).
