---
title: "Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters"
kind: "system"
category: "Rewards: EXP, LP, gil and loot"
addresses: "00253690, 00254EE0, 003004B0, 00300500, 00316A50, 00309060, 002F95D0, 00312280, 003F4AA0, 0050FAF0, 002524C0"
---

## What the player sees

Gil goes up from defeated enemies, chests, selling, quest rewards, story scripts and a character's
first join, and down when buying. It never
goes below 0 and stops at 99,999,999. A party member with "Enables casting of magicks with gil, rather
than MP." (the Turtleshell Choker) pays for magicks in gil. A member with "Convert all license points
earned to gil." (the Cat-ear Hood) turns the LP from each kill into gil. The game keeps two hidden totals, gil gained and gil spent; the
first unlocks the Steam achievement **Plunderer** and the second **Spendthrift**.

## How it works

### Storage

Gil is a signed 32-bit value at `+0x08` of the game-state block whose address is held in
`02092758`. `00253690` reads it (`mov rax, [02092758]; mov eax, [rax+8]`).

### The setter

Every change goes through `00254EE0(newValue)`:

```c
delta = newValue - gil;                         // 00254EF1, on the raw argument
if (delta > 0)      meter(6, delta);            // 00254EF8: gained
else if (delta < 0) meter(7, -delta);           // 00254EFE-00254F00: spent
                                                // delta 0: no meter call (00254EF6 jle, 00254EFC jns)
v = newValue < 0 ? 0 : newValue;                // 00254F10 cmovns
if (v > 99999999) v = 99999999;                 // 00254F15 cmovg against 0x05F5E0FF
gil = v;                                        // 00254F1F
```

The change is measured before the clamp, so a caller that passes 200,000,000 meters the full
difference even though only 99,999,999 is stored. Most callers floor their value at 0 themselves
before calling the setter (see Operations), so for them the spent amount never exceeds the balance.

### The meter

`00316A50(kind, amount)` keeps the gained and spent totals. It ignores kinds above 29
(`00316A50 cmp cl, 0x1E`). Each kind has an 8-byte row at `00D10460 + kind*8`.

| Kind | Total | Where | Saturates at |
|---|---|---|---|
| 6 | gil gained | `[020927C0] + 0x3860` | `0x7FFFFFFF` |
| 7 | gil spent | `[020927C0] + 0x3864` | `0x7FFFFFFF` |

The slot is base `0x384C` plus the row's offset byte, read by `003166F0` and written by `00316BF0`.
For one call the meter does, in order:

1. Computes the new saturating total.
2. Calls `00315E90(kind)`, the achievement check, which reads the total stored so far (`00316760`),
   before the new one is written.
3. Stores the new total (`00316BF0`).

### The achievement check

`00315E90(kind)` returns at once if the kind's bit is already set in the done-bitset at
`[020927C0] + 0x3844`. Otherwise it compares the stored total with the kind's threshold. On reaching
it, it sets the bit and calls `008632B0` with the achievement id from `00D10550 + kind*4`: 8 for kind
6 and 10 for kind 7.

`008632B0` unlocks the Steam achievement through `0020CE60`, which marks the achievement record
(`+0x190` = 1) and calls Steam's user-stats interface (vtable `+0x38`, then `+0x50`). Records 8 and
10 of the achievement descriptor table `01DFE410` are `ACH_COUNT_GET_GIL` "Plunderer" (`01DFF0D0`)
and `ACH_COUNT_USE_GIL` "Spendthrift" (`01DFF400`); each record's first dword is its counter kind, 6
and 7.

Because the meter runs only for the kind matching the change's direction, and the check reads the
total before the update, Plunderer unlocks on the first gain after gained reaches the threshold, and
Spendthrift on the first spend after spent reaches it.

### The thresholds

The thresholds come from the handbook file `menuhandbook.bin`, loaded raw into `[022C2550]` by
`003158B0` (resource 7, 200). `003165C0(kind)` follows four 16-bit relative offsets from file
`+0x08`, then reads a kind bitmask at `+4` and packed 32-bit values at `+8`. When the kind's bit is
clear, it falls back to the row's dword at `00D10464 + kind*8`, which is 0 for kinds 6 and 7.

In the shipped files of every language the gained threshold is **100,000** and the spent threshold
is **1,000,000**.

### Gil as an action cost

`00309060(unit, action)` returns the gil cost of an action. It returns 0 when any of these holds:

- the unit is an enemy (stats byte `+0x05` = 1);
- the action id is above `0x21E`;
- the action's row in the action table `[02EBF138]` has byte `+0x1E` equal to 5 or 6;
- `002F9820` does not report the unit as a party member with effect 32, bit 0 of stats byte
  `+0x6C` or `+0x7C`.

Augment row 32's description (id 13032) reads "Enables casting of magicks with gil, rather than
MP.", and the shipped equipment row with augment byte `+0x1A` = 32 is the Turtleshell Choker
(`0x1166`).

Otherwise it returns `002F95D0(unit, action)`. With `b` the action row's byte `+0x0A`:

```c
cost = b                               // action ids 0xD0-0xE1 and 0x106-0x112
cost = trunc(b * 64.0 / 50.0) * 10     // every other action
```

### The gil a kill pays

In `00312280`, after EXP and LP are handed out:

```c
gil += (enemyStats.b[+0x1C2] - enemyStats.b[+0x88]) * [[enemy+0xE78] + 0x30]
     + [[enemy+0xE70] + 0x30]
     + conversion;                              // 0031251D-00312549
```

`conversion` adds `level × LP × 5` for each recipient whose stats byte `+0x69` or `+0x79` has bit
`0x10` set. Here `level` is the recipient's byte `+0x1C2` and `LP` is that recipient's share capped
at 999. Such a recipient receives no LP from the kill. This sits under the same reward gate as EXP and
LP (`+0xE9A` and the killer test, see the EXP and LP page). The total is floored at 0 and stored through
the setter (`00312553`-`0031255D`), and the difference is posted as a gain notification (`00312566`).

### The gain notification

`00469E80(amount)` posts message `0x26` through `0046AB10` when the amount
is positive, and does nothing otherwise.

## Operations

Every function that changes gil: the callers of the setter and of its two wrappers, with the call site.

| Function | Call | What it does to gil |
|---|---|---|
| `00312280` | `0031255D` | adds the kill's gil (formula above), then notifies |
| `0050FAF0` | via `003004B0` | the chest payout, Start of script verb `btlAtelOpenTreasureMessage`: when `002FAFD0` reports a gil chest, adds its amount through `003004B0(amount, 0)` (no notification) |
| `003004B0` | `003004D6` | adds `delta`, floors at 0, sets; when argument 2 bit 0 is set, notifies `new - old` (`003004DB`-`003004E5`); returns the new balance |
| `00300500` | `0030050F` | floors its argument at 0, sets, returns the floored value |
| `00316DF0` | via `003004B0` (`00317034`) | a party-side character's first activation (record flag `0x10` clear; character type 0-25, record flag 8 clear): grants the ten items at `+0x58` with counts at `+0x34` of the character row in `[02EBF130]` (row = type byte `+4`), then adds the row's u16 `+0x3E` as gil when non-zero |
| `0032A7F0` | via `003004B0` (`0032A7F2`, jump) | `003004B0(n, 0)`; called by the script verbs `addgill` (`0x2E7`, `00346943` in `00346930`) with `n` and `subgill` (`0x2E8`, `00346E30`) with `-n` |
| `00239960` | via `00300500` (`00239B1D`) | applying a SetSaveData preset sets gil to the preset row's u16 `+0x0E` (an absolute set) |
| `0032A800` | via `00300500` (`0032A802`, jump) | `00300500(n)`; called by the script verb `debug_setgill` (`0x0A3` in family 2, `0050DEF2` in `0050DEE0`) |
| `002FEEB0` | `002FEEF3` | shop purchase: adds the item through `003008A0(item, count, 0, 1, flags)`, then gil = max(gil - price, 0); notifies when flags bit 0 is set |
| `00310870` | `003108BD` | shop sale: removes the item through `003008A0(item, -count, 0, 1, flags)`, gil = max(gil + price, 0), notifies when flags bit 0 is set, then records the sale with `003008A0(item, count, 0, 3, 0)` |
| `002FD530` | `002FD5C0` | inventory class 9 (ids `0x9000`+, slot `01EEC020` of the class table `01EEBD08`): on a mode-1 add, gil += row dword `+0` × count from table `[02EBF070]` row `id - 0x9000`, then notifies `new - old` when the flags argument has bit 0 set (`00469E80`), then grants the row's items at `+4` and `+8` |
| `002FD880` | `002FD8B4` | inventory class 0xE (slot `01EEC1D8`): on a mode-1 add, gil += `(id & 0xFFF)` × count |
| `003F4AA0` | `003F4AC1` | applies a reward record: when bit 0 of byte `+0` is set, gil += dword `+4` (not floored before the setter; the setter's clamp applies); then grants the `+0x08`-counted `{item, count}` list at `+0x0C` and the `+0x0A`-counted single items at `+0x1C` through `00300B80` |
| `0030EF20` | `0030EFD8` | reserves an action's gil cost: stores `00309060`'s result at unit `+0xE58` (`0030EFC0`), then gil = max(gil - cost, 0) |
| `00300280` | `003002F0` | refunds a party unit's reservation: gil = max(gil + `[unit+0xE58]`, 0), then clears `+0xE58` |
| `00305640` | `0030572B` | consumes an action: clears a party unit's reservation `+0xE58` without refunding it (so the reserved deduction stands), then, for any unit, gil = max(gil - `[unit+0xE54]`, 0) as a separate charge; `+0xE54` is field `+0x08` of the action's result evaluated per target, stored by `00303954` (in `00303830`) and `00303B2E` (in `00303A00`), the last target's value standing |
| `003112F0` | `00311A9E` | applies a result: when the result's dword `+0x08` is non-zero, gil = max(gil - value, 0) (`00311A84`-`00311A9E`) |
| `003058B0` | `003058B5` (jump) | sets gil to 99,999,999 (`mov ecx, 0x05F5E0FF; jmp 00254EE0`); called from `001D3E9C`, `0023E168` and `00240BAE` |

The reward record applier `003F4AA0` is called only by `00290130`, which fetches the record
(`003F8C60`), applies it and posts message `0x100` (`003F4BD0`). `00290130` is reached through the
thunk `002E1A50` (`jmp 00290130`), called at `00344C9A` in `00344C60`, the Start handler of the script
verb `questresultwindow` (`0x37C`).

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `[02092758] + 0x08` | i32 | gil, 0-99,999,999 | `00254EE0` (`00254F1F`) |
| `[020927C0] + 0x3860` | i32 | gil gained, saturating at `0x7FFFFFFF` | `00316BF0` for kind 6 |
| `[020927C0] + 0x3864` | i32 | gil spent, saturating at `0x7FFFFFFF` | `00316BF0` for kind 7 |
| `[020927C0] + 0x3844` | bits | counters whose achievement has fired (bit = kind) | `00316A50`, `00315E90` |
| unit `+0xE58` | i32 | gil reserved for the action being carried out | `0030EFC0`; cleared by `00300280`, `00305640` |
| unit `+0xE54` | i32 | gil amount from the action's result evaluation, deducted on consume | `00303954`, `00303B2E` |

## Modding notes

- The cap is the constant `0x05F5E0FF` in `00254EE0` (`00254F09`) and in `003058B0`; it is not data.
- The shop's rolling gil total carries the same constant twice: `002A1DC0` flags a roll whose end
  passes it, and `002524C0(current, change)` returns the change to roll: 99,999,999 for a current
  above the cap, 0 for a negative current, the current itself when the change would go below 0,
  `99,999,999 - current` when the sum would pass the cap, else the change. Raising the cap means
  patching these too.
- Writing `[02092758] + 8` directly skips both the clamp and the gained/spent totals. Write through
  `00254EE0`, or `003004B0` for a relative change.
- The Plunderer and Spendthrift thresholds are in `menuhandbook.bin`, the record reached through the
  four offsets from file `+0x08` (file offset `0xFC` in every language folder except `us`, where it is
  `0xF8`). They are not in the executable.
- The gil price of abilities under the gil-cost effect is `trunc(MP cost × 1.28) × 10`, computed from the
  action row's byte `+0x0A` in `002F95D0`. The two id ranges that charge the raw byte are hard-coded
  there.
- A kill's gil comes from the enemy's two records at `+0xE70` and `+0xE78` (dword `+0x30` of each)
  and the level difference in its stats.

## Related

- [Kill chain: chain count, chain level, the chain coin and resets](kill-chain.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](loot-drops.md)
