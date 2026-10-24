---
title: "Timed statuses: how long a status lasts, when Poison, Sap and Regen tick, and what else each unit runs every frame"
kind: "system"
category: "Status effects and KO"
addresses: "0x00310DB0, 0x00385DF0, 0x00386C70, 0x00385570, 0x00385CA0, 0x00386860, 0x003112F0"
---

## What the player sees

- A timed status such as Haste or Protect runs out on its own; Stop freezes every other status's timer while it
  lasts.
- Poison takes a sixteenth of max HP every 12 seconds, Sap takes 1 HP ten times a second but never the last one,
  and Regen heals a little every second and a half.
- The Petrify and Doom counts step down until the unit turns to stone or falls.
- Below a fifth of max HP a unit is in HP Critical.
- An enemy that loses sight of its foes heals back up over time.

## How it works

### The periodic step

`0x00310DB0(unit)` runs for every active unit that is not down, from the unit frame `0x00233F70` (`0x00234001`). It
first refreshes unit `+0x24` (`0x00305E70`) and `+0x60` (`0x002E8100`), and clears unit flag bit 30 once the battle
clock passes `+0xDD0`, the window a revive opens ([KO and Game Over](ko-and-game-over.md); `0x00310DDC`-`0x00310DFC`).
It stops at once, running nothing below, when (`0x00310DCB`-`0x00310E1B`):

- the unit has no stats record;
- a special-sequence scene is on screen (`0x022C2160` is 5 or 6);
- the area's town bit is set.

For a party-side unit (stats `+0x05` = 0) the `+0x24` value is `0x003271E0()`: the id `+0x08` of the
unit that `0x00327150` finds, the slot unit whose stats record is entry `[[0x02EBF190] + 0x5AA4]` (0 to 39)
of the records at `[0x02EBF190] + 8`, or 0 when there is none (`0x00305E70`-`0x00305E97`,
`0x00327150`-`0x003271BF`, `0x003271E0`).

A summoned Esper at 0 HP or below (a signed 32-bit test, `0x00310E5B`-`0x00310E5F`), or whose summoner is gone or
down, is dismissed with `0x003138D0(0)` and nothing else runs (`0x00310E21`-`0x00310EFD`). Then four gates skip to the tail, below (`0x00310F12`-`0x00310F4F`): the actor
manager is not ready (`0x00265680`), the battle or unit eligibility mask is set
([Gaining and losing statuses](status-changes.md)), or unit flag bit 36 is set.

Otherwise it builds a result with `0x00385DF0` and applies it with `0x003112F0(result, 0, stats, 0xFFFF, 0)`
(`0x00310F5D`-`0x00310FAC`). `0x00385DF0` runs five stages in order (`0x00385E08`-`0x00385E3E`): reset the result
(`0x003848E0`), the status countdown, the buff timers, the area drains and the out-of-combat healing.

### The status countdown

`0x00386C70(stats, result)` walks the 32 statuses (`0x00386CD0`-`0x00386F72`). For each status the unit has:

1. While the unit has Stop, every other status is skipped (`0x00386CDE`-`0x00386CE5`, `0x00386E97`-`0x00386E9E`).
2. **The beat.** `+0x13C[s]` loses 10. While it stays above 0 nothing else happens; at 0 the beat fires and
   reloads to row `+0x09` × 30 × frame base (`0x00386CEB`-`0x00386CF5`, `0x00386E74`-`0x00386E84`).
3. **The duration**, only for a status held in the timed word `+0x64` and not in `+0x3C`, whose row has a
   duration. `+0xBC[s]` loses 10; at 0 or below the status goes into the result's remove mask
   (`0x00386E88`-`0x00386F55`).

The duration and beat are set when the status lands ([Gaining and losing statuses](status-changes.md)); their
shipped values are on [Statuses](statuses.md). A status held in `+0x3C`, from gear, never runs out.

### What fires on the beat

| Status | On each beat | Sites |
|---|---|---|
| Poison (8) | HP falls by max HP / 16 (doubled under Bubble), or current HP / 16 under Disease, at least 1 | `0x00386D9B`-`0x00386E39` |
| Sap (10) | HP falls by 1 while it is above 1 | `0x00386D89`-`0x00386D99` |
| Regen (25) | HP rises by `MT19937 % level + 1` | `0x00386D20`-`0x00386D3D` |
| Petrify (2), Doom (6) | the count `+0xBC[s]` falls by 1; the beat before the last step is a quarter of the usual one | `0x00386E3E`-`0x00386E72` |

When the count of Petrify reaches 0 the unit gains Stone; when Doom's does, its HP is set to 0
(`0x00386EF5`-`0x00386F0F`). The HP changes go through the HP write ([HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)),
so a Poison beat can finish a unit.

### HP Critical

After the walk, the step compares the unit's HP after the beat with a fifth of its maximum (max HP, doubled under
Bubble, or current HP under Disease). Above 0 and below that line the unit gains HP Critical; at or above it, or
at 0, it loses it (`0x00386F78`-`0x00386FF3`).

### Buff timers

`0x00385570` counts down the buff timers at `+0x17C` ([Battle buffs](battle-buffs.md); `0x003855CD`-`0x00385645`).
It reads each timer as a signed 16-bit value and leaves one at 0 or below alone (`0x0038562E`-`0x00385631`); a
positive one loses 1, and the step that takes it from 1 to 0 queues the buff for removal from the battle layer
`+0x68` (`0x00385636`-`0x0038563C`). A buff that gear or a licence also holds in `+0x78` stays in effect.

### Area drains

`0x00385CA0` drains HP and MP of party-side units (`0x002FA390`) while battle flags `0x022C314C` bit 0 (HP) or bit 1
(MP) are set (`0x00385CB0`-`0x00385DDC`). Battle orders `0x4139`-`0x4148` set and clear those bits
([Battle orders](../Battle-Actions/battle-orders.md)). The drain lands when the battle clock `0x0032A150` is a
multiple of 10 × frame base:

| Drain | Amount | Sites |
|---|---|---|
| HP | max HP / 100 (doubled under Bubble, current HP under Disease), or 1 when that is below 100 | `0x00385CDE`-`0x00385D62` |
| MP | max MP / 50, or 1 when max MP is below 50 or augment 39 is held | `0x00385D78`-`0x00385DDC` |

### Out-of-combat healing

`0x00386860` heals an enemy-table unit of category 8 that perceives no foe (`0x00386860`-`0x00386A30`;
[Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md)):

1. It needs a unit that is not asleep or diseased, below its maximum HP, with no foe in its perception list
   (`0x002F8E70`) and nobody committed against it (`+0xEA8`).
2. A counter, word `+0x14` of its 64-byte record, rises by one each step; any failed test resets it to 0
   (`0x00386A27`, `0x00386A2C`).
3. Every 30 × frame base steps, starting with the counter at 0, it stores a share of its maximum HP as the
   result's HP change: 0 % for the first 10 such points, 1 % up to 30, 2 % up to 50, and 5 % from then on
   (`0x003869A2`-`0x00386A23`). The 0 % points still store, a change of 0 (`0x003869B2`, `0x00386A23`).

### How the stages share the HP change

The result's `+0x24` is the HP change, and bit 8 of its `+0x2C` sends it to the HP write: the applier adds it
with `0x00300530`, or sets HP to it with `0x00300520` when bit 3 is also set (`0x00311608`-`0x00311668`). The reset
leaves `+0x24` at 0 (`0x003848F5`). The stages then write it in order:

| Stage | What it does to `+0x24` | Sites |
|---|---|---|
| Status countdown | adds: Poison its loss, Sap −1, Regen its heal, each setting bit 8; Doom's last step instead stores 0 and sets bits 8 and 3 | `0x00386D3A`, `0x00386D96`, `0x00386DF2`, `0x00386E1A`, `0x00386E2C`; `0x00386EFF`-`0x00386F06` |
| Buff timers | leaves `+0x24` and `+0x2C` as they are | `0x00385570`-`0x00385675` |
| HP area drain | on a drain point sets bit 8 and replaces it with the loss, −1 or −(the amount above) | `0x00385D03`, `0x00385D33`, `0x00385D62` |
| Out-of-combat healing | on a healing point replaces it with the share; a share above 0 sets bit 8, a share of 0 leaves bit 8 as it was | `0x003869E3`, `0x00386A23` |

The last stage that writes decides the change. For a unit of max HP 1,600 with a Poison beat of −100: with the
HP area drain on the same step the change is −16; on one of an enemy's first 10 healing points it is 0, bit 8
still set by Poison; on a 1 % point it is +16; on a step with neither, −100.

Every store the four stages make to
`+0x2C` is an `or` (`0x00386D20`, `0x00386D3D`, `0x00386D8F`, `0x00386D9B`, `0x00386EFF`, `0x00385D03`, `0x00385D9D`,
`0x003869E3`), so after Doom's last step a later drain or heal value is set as the HP.
The HP Critical test reads `+0x24` at the end of the countdown (`0x00386F78`-`0x00386F91`), before the two later
stages write it.

### After the first apply

The step then runs, in order (`0x00310FB1`-`0x003112AC`):

1. **Traps.** `0x002F8060` checks the authored trap points near the unit; for each unit a trap catches, the trap's
   action is resolved and applied to it ([Trap points](../World-Areas-And-Travel/traps.md)).
2. **Walking MP**, `0x002F9400` ([MP gain and cost](mp.md)).
3. **Pickups.** The controlled member, or a unit walking to a pickup (order `0x4165`), collects the pickup it
   stands on and runs the Chain Bonus ([Loot pickups](../Rewards-EXP-Gil-And-Loot/loot-pickups.md)).
4. **The tail**, which the four gates above also reach: the enmity decay `0x00321530`
   ([Enmity](../Enemy-AI-And-Gambits/enmity.md)) and `0x002FE950`.

## Layouts

Each unit's 64-byte record: for a party record (byte `+5` = 0) `0x0208D480 + type * 0x40`, forty of them, otherwise
`0x0208DE80 + unit[+0xEA9] * 0x40`, thirty-two (`0x00386C21`-`0x00386C51`). Both banks are in the zero-filled tail of
`.data`.

The first list of an action ([Damage formula](../Damage-And-Battle-Formulas/damage-formula.md)) clears the first
`0x14` bytes when it resolves the user's current target, keeping `+0x10` and, with unit byte `+0x6B7` set, the high
nibble of `+0x12` (`0x0038579C`-`0x003857E1`). `0x00386C10` clears the first `0x20` bytes (`0x00386C5B`-`0x00386C66`) when a
unit is placed by `btlAtelSetUnitFinish` (`0x0023A513`) and from `0x00233AD0` (`0x00233BFC`).

`BattleRuntimeUnitRecord` (`0x40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | stored | the value an action keeps between its first list and its committed resolve: Dark Matter and Soul Purge move the Knot of Rust bank into it and deal it (`0x0038DA5D`, `0x0038DA68`); Traveler stores its damage (`0x0038ECD5`, `0x0038ECFF`) and deals it again without a stored preview (`0x0038ED17`); Gil Toss stores the gil sum (`0x00388E51`), copies it to result `+0x08` for the other targets (`0x00388E60`) and slot 147 shares it among the targets (`0x0038EDD6`) (Weapon formulas) |
| `+0x04` | `u32` | failed | one bit per target index: a first-list run that ends failed sets the target's bit (`0x00385A7F`), and the committed resolve then gives that target result kind 6 without running a slot (`0x0038633F`) |
| `+0x08` | `u32` | immune | one bit per target index: set when the first list ends immune (`0x00385AC0`); the committed resolve gives result kind 10 (`0x003862FB`) |
| `+0x0C` | `u32` | hit | one bit per target index: `0x00387B00` sets the target's bit when a finishing slot ends with an HP value (`0x00387B97`; reached from 17 sites in 16 slot functions, `0x0038D280` among them); `0x002FA290` tests a unit's bit for the battle effect program `0x003B8670` (`0x002FA352`, through `0x00322850` at `0x003B88B3`) |
| `+0x10` | `u16` | shadesAction the action Shades of Black (0x9F) turns into: 0x00387A50 stores the random pick of 0x00387130 (0x00387ADE); 0x00387090 returns it (0x0038710E); both resolves put it in place of 0x9F (0x00385801, 0x00385FF7); kept over the first list's clear (0x003857A3, 0x003857E1) |  |
| `+0x12` | `u8` | flags | bit 0 the stored preview (set `0x003857DD`, cleared `0x00386402`; read by Numerology `0x00389D24`, Dark Matter `0x0038DA49` and Traveler `0x0038EC3A`); bits 1-3 the first list's result `+0x18` bits 1-3 (`0x00385AC3`-`0x00385AF2`), copied into the committed result (`0x003860DF`-`0x00386108`); bits 4-7 the combo count (`0x00388660`: `0x0038885D`, `0x00388865`, `0x0038886B`) |
| `+0x13` | `u8` | pad13 | written only by the two clears (`0x003857B2`, `0x00386C62`); read by no instruction; nothing fixes its width |
| `+0x14` | `u16` | healSteps | the out-of-combat healing counter (`0x003869A2`, `0x003869E0`, `0x00386A27`, `0x00386A2C`) |
| `+0x16` | `u8[2]` | pad16 | written only by the clear `0x00386C62`; read by no instruction; nothing fixes its width |
| `+0x18` | `f32` | walkLeft | the walk distance left after the last MP step: `0x002F9400` compares the new distance with it (`0x002F9474`) and stores what is left (`0x002F95A6`) (MP gain and cost) |
| `+0x1C` | `u32` | circle | bit 0: the unit joins the circling formation once KO'd, set by `0x0033CB10` (`0x0033CB60`) when action-timeline event 2 or 6 reaches a KO'd unit (`0x00325651`); bit 1: it has reached its place (`0x0033DA73`); both read by the mode-2 movement `0x0033D890` (`0x0033D953`, `0x0033DA77`) (Battle locomotion) |
| `+0x20` | `u8[32]` | pad20 | read and written by no function; nothing fixes its width |

## Modding notes

- A status's duration and beat are data in its row of `battle_pack.bin` section 15; the code reads 10 off both
  each frame, so the row values are seconds and tenths of a second.
- The Poison, Sap and Regen amounts are code; no row holds them.

## Related

- [Statuses](statuses.md) - the durations, beats and cancel masks.
- [Gaining and losing statuses](status-changes.md) - where the timers are set.
- [Battle buffs](battle-buffs.md) - the buff timers.
- [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md) - the HP write the drains go through.
- [MP gain and cost](mp.md) - walking MP.
