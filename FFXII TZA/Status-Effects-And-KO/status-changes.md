---
title: "Gaining and losing statuses: how a status is added or removed, what can refuse it, and what happens the moment it lands"
kind: "system"
category: "Status effects and KO"
addresses: "0x0030E360, 0x0030B9B0, 0x0030B8E0, 0x0030B770, 0x0030B7F0, 0x00386A70, 0x003284D0, 0x0046A800, 0x00300140, 0x00300FC0"
---

## What the player sees

A status icon appears or goes, and with it:

- the statuses the new one cancels are removed, as its help text says (Haste removes Slow);
- the unit reacts, when it is near the party leader;
- a party member turned to stone or sent to X-Zone gets its battle message;
- KO, Stone and X-Zone end the unit's part in the fight, and an enemy pays out;
- losing Bubble halves the unit's current HP;
- Confuse and Berserk interrupt what the unit was doing.

Some moments refuse every status change, such as while the battle is frozen or a defeat is being handled.

## How it works

### The status write

`0x0030E360(target, source, status, duration, beat, flags, mode)` adds or removes one status on a stats record
(`0x0030E360`-`0x0030E889`). It finds both records' units (`0x0030E39A`, `0x0030E3A7`) and works out from its arguments
(`0x0030E3BB`-`0x0030E41C`):

| Value | From | Meaning |
|---|---|---|
| adding | mode 3 or 4 | the change sets a bit |
| starts timers | mode 0 or 3 | the duration and beat are written |
| reaction | flags bit `0x10` clear | the status reaction may play |
| message | flags bit `0x2` clear | the battle message may post |
| was present | `(+0x3C \| +0x64) & bit` | the status was there before |

Its fourteen call sites include the result applier `0x003112F0` (`0x0031153A`, `0x0031159F`), the HP write `0x00300530`
(`0x0030077A`, `0x003007CF`), the augment rebuild `0x0030FED0` (`0x00310409`) and the order handler `0x002FDDA0`
(`0x002FDF40`, `0x002FDF79`).

Two wrappers fix the mode. `0x0030E990(target, source, status, -, -, flags)` removes: it passes duration
and beat 0 and mode 0 (`0x0030E994`-`0x0030E9A9`). `0x0030EAE0` adds with mode 3 and passes duration, beat
and flags through (`0x0030EAE4`-`0x0030EAFC`). `0x0030E990` is used by:

- `0x0030E8F0`, for each of the 32 statuses with `flags | 0x200` (`0x0030E8F0`);
- the area initialisation `0x002342F0`, which removes X-Zone (31) with flags 0 from each of the 40
  stats records at `[0x02EBF190] + 8`, `0x1C8` bytes apart (`0x00234358`-`0x0023438E`);
- `0x00318A00` and `0x00318A90`, which pick `0x0030EAE0` or `0x0030E990` by a flag (`0x00318A49`-`0x00318A63`,
  `0x00318AF0`-`0x00318B14`). `setpartybattlestatus` (`0x00347F80`) reaches `0x00318A00` through `0x00473820`, which
  sets the flag to 1 (`0x00473823`), so it always calls the add `0x0030EAE0`.

### What refuses a change

With flags bit `0x1` clear, two gates run on the target and source units (`0x0030E420`-`0x0030E45A`):

- `0x0030B9B0` refuses any change when the battle-wide mask or the target's own mask has a low bit set;
- when adding, `0x0030B8E0` refuses KO, Stone and X-Zone (the mask `0x80000003`) when either mask has a high bit
  set.

| Mask bit | Set when | Site |
|---|---|---|
| battle `0x1` | the battle flags `0x02089340` have a bit of `0x3080` | `0x0030B77F`-`0x0030B799` |
| battle `0x2` | byte `0x022C2158` bit `0x1` | `0x0030B7A3`-`0x0030B7B0` |
| battle `0x4`, `0x8`, `0x10` | battle flags bit `0x400`, `0x200` or `0x800`, the defeat latches ([KO and Game Over](ko-and-game-over.md)) | `0x0030B7B4`-`0x0030B7DA` |
| unit `0x8` | the unit's `+4` bit `0x20`, unless `0x022C2160` is 5 or 6 | `0x0030B817`-`0x0030B830` |
| unit `0x1` | unit flag bit `0x100` | `0x0030B83C`-`0x0030B847` |
| unit `0x2` | unit flag bit `0x40000000`, for a source on the other side | `0x0030B84C`-`0x0030B85B` |
| unit `0x10` | the target is party row 26 | `0x0030B860`-`0x0030B87E` |
| unit `0x10000` | the developer setting `+0xC20` is 1, for a party record | `0x0030B883`-`0x0030B8AA` |
| unit `0x20000` | the developer setting `+0xC20` is 2 | `0x0030B8B6`-`0x0030B8C3` |

A unit counts only while its flag bit `0x10` is set (`0x0030B80D`). The setting `+0xC20` is the console's
"Invincible" entry ([Debug menu commands](../Engine-Core/debug-menu-commands.md)),
0 in normal play. The HP write uses the same two gates ([HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)).

### KO, Stone and X-Zone on arrival

When adding KO, Stone or X-Zone (`0x0030E460`-`0x0030E4BD`):

1. A summoned Esper, a party record of type `0x1B`-`0x27`, goes straight to the defeat cleanup
   `0x00300FC0(unit, 0)` and nothing else happens: no status bit, no message, no reward (`0x0030E478`-`0x0030E49C`).
2. A unit that already has one of the three keeps it, and the change is refused, unless bit `0x8000` of the active
   field record is set (`0x0030E4A9`-`0x0030E4BD`).

### The status words

The mode picks the word and the direction (`0x0030E4C3`-`0x0030E564`; the mode table is on
[Augments](../Damage-And-Battle-Formulas/augments.md)): modes 0, 1 and 2 clear the bit in `+0x64`, `+0x3C` or `+0x38`, and
modes 3, 4 and 5 set it. A change to a bit already in the asked state does nothing, and mode 3 is also
refused while the bit is in the immunity word `+0x38` (`0x0030E531`).

Modes 0 and 3 then write the status's duration `+0xBC[s]` and beat `+0x13C[s]` (`0x0030E567`-`0x0030E5AF`). A
negative argument takes the default: the duration from `0x00387730`, the beat from `0x003876D0`
([Status timers](status-timers.md)).

### What an unchanged presence skips

A status is present when either `+0x64` or `+0x3C` holds it. When presence is the same after the write as before,
the function returns there (`0x0030E5B7`-`0x0030E5CB`), before the result record, the cancelled statuses, the
reaction, the message, the arm and the rebuild below.

The bit change and, in modes 0 and 3, the duration and beat stores (`0x0030E594`, `0x0030E5AF`) come before that test
and stay made. So adding a status with mode 3 while `+0x3C`
already holds it restarts its duration and beat, and removing it from `+0x64` with mode 0 while `+0x3C` still
holds it writes the duration and beat it is given, 0 and 0 from `0x0030E990` (`0x0030E998`-`0x0030E9A4`). In modes 1, 2,
4 and 5 such a change moves the bit alone.

### What a change does

When presence changed, in this order (`0x0030E5D1`-`0x0030E828`):

1. **A result record.** Adding builds an empty one (`0x00386A50`). Removing builds one with `0x00386A70`, which
   only for Bubble (28) on a unit with HP sets current HP to `(HP + 1) / 2`, half rounded up
   (`0x00386A94`-`0x00386AB0`). The record is applied by `0x003112F0` when it is live, `+0x2C` bit `0x1`
   (`0x0030E610`-`0x0030E638`).
2. **Cancelled statuses.** When adding, each status in the new one's cancel mask, row `+0x0C` of the status
   table `[0x02EBF118]`, is removed with `0x0030E360(target, source, i, 0, 0, flags | 0x200, mode 0)`
   (`0x0030E63D`-`0x0030E6D7`; [Statuses](statuses.md)).
3. **The reaction.** When adding with the reaction allowed, `0x003284D0` queues reaction 2 for the status, but
   only for a unit within 24 units of the party leader on the ground plane (`0x0030E6E7`-`0x0030E6FF`,
   `0x002FA3B0`-`0x002FA451`). The reaction is a popup of the status's name, posted through `0x003BBD00`
   ([Battle numbers](../Menus-And-HUD/battle-numbers.md)).
4. **The message.** When adding with the message allowed, `0x0046A800` posts message `0x12` "turns to stone."
   for Stone and `0x11` "is cast into the void." for X-Zone, for a party-side unit only
   (`0x0030E704`-`0x0030E727`, `0x0046A831`-`0x0046A85A`; [Battle message list](../Battle-Actions/battle-message-list.md)).
5. **The status's own arm**, below (`0x0030E729`-`0x0030E759`).
6. **The rebuild.** Unless flags bit `0x200` is set, `0x0030FED0` rebuilds the unit's derived stats and auto-statuses
   (`0x0030E816`-`0x0030E828`; [Augments](../Damage-And-Battle-Formulas/augments.md)).

### Each status's arm

The byte table `0x0030E8C4` sends each status to one of eight arms of `0x0030E8A4`. The arms run only when the
target has a battle unit; without one the function goes straight to the rebuild (`0x0030E729`-`0x0030E72C`):

| Status | Arm | Adding | Removing |
|---|---|---|---|
| KO (0) | `0x0030E80A` | the defeat cleanup `0x00300FC0(unit, 0)`, then the rewards `0x00312280(source, unit)` | `0x00301140`, the recovery |
| Stone (1) | `0x0030E850` | event `0x200C`, then the same as KO | the recovery |
| X-Zone (31) | `0x0030E85E` | event `0x200E`, then the same as KO | the recovery |
| Petrify (2) | `0x0030E7DD` | unit `+0xE9A` bit `0x2` = the source is a party record | nothing |
| Poison (8) | `0x0030E7B3` | unit `+0xE9A` bit `0x1` = the source is a party record | nothing |
| Sleep (4) | `0x0030E75B` | event `0x2001` | event `0x2001` |
| Confuse (5), Berserk (27) | `0x0030E770` | `0x00300140(unit, cancel)`, then `0x00307D10` | the same |
| every other status | `0x0030E816` | nothing | nothing |

The two `+0xE9A` bits decide whether a Poison kill or a Stone from Petrify pays the party
([Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)). For Confuse and Berserk, `cancel` is 1, so `0x00300140`
cancels the action in flight with `0x003105D0`, except when the unit is changing stance, carries an action at
phase 9 or later, or is dismissing (`0x113`); those give 0 and keep it (`0x0030E770`-`0x0030E79F`). Events go through `0x003299B0` (`0x0030E766`, `0x0030E86D`). What the defeat cleanup and the
recovery do is on [KO and Game Over](ko-and-game-over.md).

On a party wipe the defeat cleanup sets battle flag `0x400` or `0x200`, arms the request and recomputes party
control with `0x0023B040` (`0x00301063`-`0x003010C0`; [Party leader](../Party/party-leader.md)).

## Modding notes

- The cancel mask is data: editing a status row's `+0x0C` changes which statuses it removes, with no code change.
- A caller can skip the gates with flags bit `0x1`, the reaction with bit `0x10` and the message with bit `0x2`.
- Only the KO, Stone, X-Zone, Petrify, Poison, Sleep, Confuse and Berserk arms do anything beyond the status bit
  and its timers; a new effect for any other status needs code.

## Related

- [Statuses](statuses.md) - every status's name, duration and cancel mask.
- [Status timers](status-timers.md) - how the duration and beat run down.
- [Augments](../Damage-And-Battle-Formulas/augments.md) - the mode table and the rebuild.
- [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md) - the HP write that adds KO.
- [KO and Game Over](ko-and-game-over.md) - the defeat cleanup and recovery.
- [Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md) - what an enemy's KO pays.
