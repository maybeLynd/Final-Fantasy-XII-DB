---
title: "Gaining and losing statuses: how a status is added or removed, what can refuse it, and what happens the moment it lands"
kind: "system"
category: "Status effects and KO"
addresses: "0030E360, 0030B9B0, 0030B8E0, 0030B770, 0030B7F0, 00386A70, 003284D0, 0046A800, 00300140, 00300FC0"
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

`0030E360(target, source, status, duration, beat, flags, mode)` adds or removes one status on a stats record
(`0030E360`-`0030E889`). It finds both records' units (`0030E39A`, `0030E3A7`) and works out from its arguments
(`0030E3BB`-`0030E41C`):

| Value | From | Meaning |
|---|---|---|
| adding | mode 3 or 4 | the change sets a bit |
| starts timers | mode 0 or 3 | the duration and beat are written |
| reaction | flags bit 4 clear | the status reaction may play |
| message | flags bit 1 clear | the battle message may post |
| was present | `(+0x3C \| +0x64) & bit` | the status was there before |

Its fourteen call sites include the result applier `003112F0` (`0031153A`, `0031159F`), the HP write `00300530`
(`0030077A`, `003007CF`), the augment rebuild `0030FED0` (`00310409`) and the order handler `002FDDA0`
(`002FDF40`, `002FDF79`).

Two wrappers fix the mode. `0030E990(target, source, status, -, -, flags)` removes: it passes duration
and beat 0 and mode 0 (`0030E994`-`0030E9A9`). `0030EAE0` adds with mode 3 and passes duration, beat
and flags through (`0030EAE4`-`0030EAFC`). `0030E990` is used by:

- `0030E8F0`, for each of the 32 statuses with `flags | 0x200` (`0030E8F0`);
- the area initialisation `002342F0`, which removes X-Zone (31) with flags 0 from each of the 40
  stats records at `[02EBF190] + 8`, `0x1C8` bytes apart (`00234358`-`0023438E`);
- `00318A00` and `00318A90`, which pick `0030EAE0` or `0030E990` by a flag (`00318A49`-`00318A63`,
  `00318AF0`-`00318B14`).

### What refuses a change

With flags bit 0 clear, two gates run on the target and source units (`0030E420`-`0030E45A`):

- `0030B9B0` refuses any change when the battle-wide mask or the target's own mask has a low bit set;
- when adding, `0030B8E0` refuses KO, Stone and X-Zone (the mask `0x80000003`) when either mask has a high bit
  set.

| Mask bit | Set when | Site |
|---|---|---|
| battle 0 | the battle flags `02089340` have a bit of `0x3080` | `0030B77F`-`0030B799` |
| battle 1 | byte `022C2158` bit 0 | `0030B7A3`-`0030B7B0` |
| battle 2, 3, 4 | battle flags bit 10, 9 or 11, the defeat latches ([KO and Game Over](ko-and-game-over.md)) | `0030B7B4`-`0030B7DA` |
| unit 3 | the unit's `+4` bit 5, unless `022C2160` is 5 or 6 | `0030B817`-`0030B830` |
| unit 0 | unit flag bit 8 | `0030B83C`-`0030B847` |
| unit 1 | unit flag bit 30, for a source on the other side | `0030B84C`-`0030B85B` |
| unit 4 | the target is party row 26 | `0030B860`-`0030B87E` |
| unit high 0 | the developer setting `+0xC20` is 1, for a party record | `0030B883`-`0030B8AA` |
| unit high 1 | the developer setting `+0xC20` is 2 | `0030B8B6`-`0030B8C3` |

A unit counts only while its flag bit 4 is set (`0030B80D`). The setting `+0xC20` is the console's
"Invincible" entry ([Debug menu commands](../Engine-Core/debug-menu-commands.md)),
0 in normal play. The HP write uses the same two gates ([HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)).

### KO, Stone and X-Zone on arrival

When adding KO, Stone or X-Zone (`0030E460`-`0030E4BD`):

1. A summoned Esper, a party record of type `0x1B`-`0x27`, goes straight to the defeat cleanup
   `00300FC0(unit, 0)` and nothing else happens: no status bit, no message, no reward (`0030E478`-`0030E49C`).
2. A unit that already has one of the three keeps it, and the change is refused, unless bit 15 of the active
   field record is set (`0030E4A9`-`0030E4BD`).

### The status words

The mode picks the word and the direction (`0030E4C3`-`0030E564`; the mode table is on
[Augments](../Damage-And-Battle-Formulas/augments.md)): modes 0, 1 and 2 clear the bit in `+0x64`, `+0x3C` or `+0x38`, and
modes 3, 4 and 5 set it. A change to a bit already in the asked state does nothing, and mode 3 is also
refused while the bit is in the immunity word `+0x38` (`0030E531`).

Modes 0 and 3 then write the status's duration `+0xBC[s]` and beat `+0x13C[s]` (`0030E567`-`0030E5AF`). A
negative argument takes the default: the duration from `00387730`, the beat from `003876D0`
([Status timers](status-timers.md)).

### Nothing happens unless presence changes

A status is present when either `+0x64` or `+0x3C` holds it. When presence is the same after the write as before,
the function returns there (`0030E5B7`-`0030E5CB`). So adding a status to one word while the other already holds
it, or removing it from one word while the other still holds it, changes the bit and nothing else.

### What a change does

When presence changed, in this order (`0030E5D1`-`0030E828`):

1. **A result record.** Adding builds an empty one (`00386A50`). Removing builds one with `00386A70`, which
   only for Bubble (28) on a unit with HP sets current HP to `(HP + 1) / 2`, half rounded up
   (`00386A94`-`00386AB0`). The record is applied by `003112F0` when it is live, `+0x2C` bit 0
   (`0030E610`-`0030E638`).
2. **Cancelled statuses.** When adding, each status in the new one's cancel mask, row `+0x0C` of the status
   table `[02EBF118]`, is removed with `0030E360(target, source, i, 0, 0, flags | 0x200, mode 0)`
   (`0030E63D`-`0030E6D7`; [Statuses](statuses.md)).
3. **The reaction.** When adding with the reaction allowed, `003284D0` queues reaction 2 for the status, but
   only for a unit within 24 units of the party leader on the ground plane (`0030E6E7`-`0030E6FF`,
   `002FA3B0`-`002FA451`).
4. **The message.** When adding with the message allowed, `0046A800` posts message `0x12` "turns to stone."
   for Stone and `0x11` "is cast into the void." for X-Zone, for a party-side unit only
   (`0030E704`-`0030E727`, `0046A831`-`0046A85A`; [Battle message list](../Battle-Actions/battle-message-list.md)).
5. **The status's own arm**, below (`0030E729`-`0030E759`).
6. **The rebuild.** Unless flags bit 9 is set, `0030FED0` rebuilds the unit's derived stats and auto-statuses
   (`0030E816`-`0030E828`; [Augments](../Damage-And-Battle-Formulas/augments.md)).

### Each status's arm

The byte table `0030E8C4` sends each status to one of eight arms of `0030E8A4`. The arms run only when the
target has a battle unit; without one the function goes straight to the rebuild (`0030E729`-`0030E72C`):

| Status | Arm | Adding | Removing |
|---|---|---|---|
| KO (0) | `0030E80A` | the defeat cleanup `00300FC0(unit, 0)`, then the rewards `00312280(source, unit)` | `00301140`, the recovery |
| Stone (1) | `0030E850` | event `0x200C`, then the same as KO | the recovery |
| X-Zone (31) | `0030E85E` | event `0x200E`, then the same as KO | the recovery |
| Petrify (2) | `0030E7DD` | unit `+0xE9A` bit 1 = the source is a party record | nothing |
| Poison (8) | `0030E7B3` | unit `+0xE9A` bit 0 = the source is a party record | nothing |
| Sleep (4) | `0030E75B` | event `0x2001` | event `0x2001` |
| Confuse (5), Berserk (27) | `0030E770` | `00300140(unit, cancel)`, then `00307D10` | the same |
| every other status | `0030E816` | nothing | nothing |

The two `+0xE9A` bits decide whether a Poison kill or a Stone from Petrify pays the party
([Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)). For Confuse and Berserk, `cancel` is 1, so `00300140`
cancels the action in flight with `003105D0`, except when the unit is changing stance, carries an action at
phase 9 or later, or is dismissing (`0x113`); those give 0 and keep it (`0030E770`-`0030E79F`). Events go through `003299B0` (`0030E766`, `0030E86D`). What the defeat cleanup and the
recovery do is on [KO and Game Over](ko-and-game-over.md).

## Modding notes

- The cancel mask is data: editing a status row's `+0x0C` changes which statuses it removes, with no code change.
- A caller can skip the gates with flags bit 0, the reaction with bit 4 and the message with bit 1.
- Only the KO, Stone, X-Zone, Petrify, Poison, Sleep, Confuse and Berserk arms do anything beyond the status bit
  and its timers; a new effect for any other status needs code.

## Related

- [Statuses](statuses.md) - every status's name, duration and cancel mask.
- [Status timers](status-timers.md) - how the duration and beat run down.
- [Augments](../Damage-And-Battle-Formulas/augments.md) - the mode table and the rebuild.
- [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md) - the HP write that adds KO.
- [KO and Game Over](ko-and-game-over.md) - the defeat cleanup and recovery.
- [Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md) - what an enemy's KO pays.
