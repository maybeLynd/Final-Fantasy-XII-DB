---
title: "Timed statuses: how long a status lasts, when Poison, Sap and Regen tick, and what else each unit runs every frame"
kind: "system"
category: "Status effects and KO"
summary: "The periodic step every battle unit takes each frame: what stops it, the countdown that ends a timed status, the beat on which Poison, Sap and Regen drain or heal and the Petrify and Doom counts step, the HP Critical line, Stop freezing the other timers, the buff timers, the area drains of HP and MP, the out-of-combat healing of a disengaged enemy, and the Esper dismiss, traps, walking MP, pickups and enmity decay that follow."
addresses: ["00310DB0", "00385DF0", "00386C70", "00385570", "00385CA0", "00386860", "003112F0"]
---

# Timed statuses: how long a status lasts, when Poison, Sap and Regen tick, and what else each unit runs every frame

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

`00310DB0(unit)` runs for every active unit that is not down, from the unit frame `00233F70` (`00234001`). It
first refreshes unit `+0x24` (`00305E70`) and `+0x60` (`002E8100`), and clears unit flag bit 30 once the battle
clock passes `+0xDD0`, the window a revive opens ([KO and Game Over](ko-and-game-over.md); `00310DDC`-`00310DFC`).
It stops at once, running nothing below, when (`00310DCB`-`00310E1B`):

- the unit has no stats record;
- a special-sequence scene is on screen (`022C2160` is 5 or 6);
- the area's town bit is set.

A summoned Esper at 0 HP, or whose summoner is gone or down, is dismissed with `003138D0(0)` and nothing else
runs (`00310E21`-`00310EFD`). Then four gates skip to the tail, below (`00310F12`-`00310F4F`): the actor
manager is not ready (`00265680`), the battle or unit eligibility mask is set
([Gaining and losing statuses](status-changes.md)), or unit flag bit 36 is set.

Otherwise it builds a result with `00385DF0` and applies it with `003112F0(result, 0, stats, 0xFFFF, 0)`
(`00310F5D`-`00310FAC`). `00385DF0` runs five stages in order (`00385E08`-`00385E3E`): reset the result
(`003848E0`), the status countdown, the buff timers, the area drains and the out-of-combat healing.

### The status countdown

`00386C70(stats, result)` walks the 32 statuses (`00386CD0`-`00386F72`). For each status the unit has:

1. While the unit has Stop, every other status is skipped (`00386CDE`-`00386CE5`, `00386E97`-`00386E9E`).
2. **The beat.** `+0x13C[s]` loses 10. While it stays above 0 nothing else happens; at 0 the beat fires and
   reloads to row `+0x09` × 30 × frame base (`00386CEB`-`00386CF5`, `00386E74`-`00386E84`).
3. **The duration**, only for a status held in the timed word `+0x64` and not in `+0x3C`, whose row has a
   duration. `+0xBC[s]` loses 10; at 0 or below the status goes into the result's remove mask
   (`00386E88`-`00386F55`).

The duration and beat are set when the status lands ([Gaining and losing statuses](status-changes.md)); their
shipped values are on [Statuses](statuses.md). A status held in `+0x3C`, from gear, never runs out.

### What fires on the beat

| Status | On each beat | Sites |
|---|---|---|
| Poison (8) | HP falls by max HP / 16 (doubled under Bubble), or current HP / 16 under Disease, at least 1 | `00386D9B`-`00386E39` |
| Sap (10) | HP falls by 1 while it is above 1 | `00386D89`-`00386D99` |
| Regen (25) | HP rises by `MT19937 % level + 1` | `00386D20`-`00386D3D` |
| Petrify (2), Doom (6) | the count `+0xBC[s]` falls by 1; the beat before the last step is a quarter of the usual one | `00386E3E`-`00386E72` |

When the count of Petrify reaches 0 the unit gains Stone; when Doom's does, its HP is set to 0
(`00386EF5`-`00386F0F`). The HP changes go through the HP write ([HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)),
so a Poison beat can finish a unit.

### HP Critical

After the walk, the step compares the unit's HP after the beat with a fifth of its maximum (max HP, doubled under
Bubble, or current HP under Disease). Above 0 and below that line the unit gains HP Critical; at or above it, or
at 0, it loses it (`00386F78`-`00386FF3`).

### Buff timers

`00385570` counts down the buff timers at `+0x17C` by one each step, and clears a buff whose timer reaches 0
([Battle buffs](battle-buffs.md); `003855CD`-`00385645`).

### Area drains

`00385CA0` drains HP and MP of party-side units (`002FA390`) while battle flags `022C314C` bit 0 (HP) or bit 1
(MP) are set (`00385CB0`-`00385DDC`). Battle orders `0x4139`-`0x4148` set and clear those bits
([Battle orders](../Battle-Actions/battle-orders.md)). The drain lands when the battle clock `0032A150` is a
multiple of 10 × frame base:

| Drain | Amount | Sites |
|---|---|---|
| HP | max HP / 100 (doubled under Bubble, current HP under Disease), or 1 when that is below 100 | `00385CDE`-`00385D62` |
| MP | max MP / 50, or 1 when max MP is below 50 or augment 39 is held | `00385D78`-`00385DDC` |

### Out-of-combat healing

`00386860` heals an enemy-table unit of category 8 that perceives no foe (`00386860`-`00386A30`;
[Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md)):

1. It needs a unit that is not asleep or diseased, below its maximum HP, with no foe in its perception list
   (`002F8E70`) and nobody committed against it (`+0xEA8`).
2. A counter, word `+0x14` of its 64-byte record, rises by one each step; any failed test resets it to 0
   (`00386A27`, `00386A2C`).
3. Every 30 × frame base steps it heals a share of its maximum HP: nothing for the first 10 such points,
   1 % up to 30, 2 % up to 50, and 5 % from then on (`003869A2`-`00386A23`).

### After the first apply

The step then runs, in order (`00310FB1`-`003112AC`):

1. **Traps.** `002F8060` checks the authored trap points near the unit; for each unit a trap catches, the trap's
   action is resolved and applied to it ([Trap points](../World-Areas-And-Travel/traps.md)).
2. **Walking MP**, `002F9400` ([MP gain and cost](mp.md)).
3. **Pickups.** The controlled member, or a unit walking to a pickup (order `0x4165`), collects the pickup it
   stands on and runs the Chain Bonus ([Loot pickups](../Rewards-EXP-Gil-And-Loot/loot-pickups.md)).
4. **The tail**, which the four gates above also reach: the enmity decay `00321530`
   ([Enmity](../Enemy-AI-And-Gambits/enmity.md)) and `002FE950`.

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
