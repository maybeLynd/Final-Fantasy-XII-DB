---
title: "HP and KO: how damage and healing change HP, the HP floor and cap, revive from zero and what happens at KO"
kind: "system"
category: "Damage and battle formulas"
addresses: "0x00300530, 0x00300520, 0x003112F0, 0x0030F340, 0x00239820, 0x0030E360, 0x00469BB0, 0x00306F00, 0x003299B0"
---

## What the player sees

Every damage and healing number in battle goes through one rule set:

- **No overheal.** HP cannot rise above the maximum, or twice the maximum under Bubble.
- **Disease** stops healing: HP can fall, but cannot rise above its current value.
- **A KO, Stone or X-Zone target takes no more damage.**
- **A heal on a character at 0 HP revives them.** Healing a living character only changes the number.
- **Reaching the bottom KOs the target**: the attacker is recorded as the killer, an enemy's death
  counts towards its group, and "... has fallen." appears when the one who fell is a party member, an
  Esper or an allied unit.
- **Some bosses stop at a set HP.** Their script raises the bottom above 0, so the fight ends or changes
  phase at that HP instead of at 0.

## How it works

### The function and its callers

`0x00300530(target, delta, source, flags)` changes the current HP of the stats record `target` by `delta`;
`source` is the acting unit's stats record or null. `0x00300520` is its absolute form: it subtracts the
current HP `+0x48` from the value and jumps in (`0x00300520`-`0x00300523`). Both records are mapped to their
battle units first (`0x0031B860`, `0x00300553`, `0x0030055E`).

| Caller | Site | Value | Flags |
|---|---|---|---|
| the applier, target | `0x00311668` | result `+0x24` | from result `+0x2C`, below |
| the applier, user | `0x00311739` | result `+0x20`, when result bit `0x80` | from result `+0x2C`, no source record |
| the cap reconcile `0x0030F340` | `0x0030F3DC` | cap minus HP | `0x217` |
| the deferred HP queue `0x003065D0`, `0x0030EB10` | `0x00306699`, `0x0030EB5F` | queued delta | `0x0` |
| spawn and timeline code (absolute) | `0x00235316`, `0x0023A451`, `0x0031A09B`, `0x00329CAE` | value | caller's |

For the target, the applier runs only when result `+0x2C` bit `0x100` is set (`0x00311610`). It uses the
absolute form for bit `0x8` (`0x00311657`-`0x00311661`) and builds the flags as bit `0x80000` → flag `0x100`, bit `0x400` → flag `0x20`,
bit `0x40000` clear → flag `0x40`, bit `0x40` clear → flag `0x10` (`0x00311608`-`0x00311651`)
([Action results](../Battle-Actions/action-results.md)).

For the user it uses the absolute form for bit
`0x2` and maps bit `0x200` → flag `0x20`, bit `0x20000` clear → flag `0x40`, bit `0x20` clear → flag `0x10` (`0x0031170A`-`0x00311732`); it passes
no source record, so the user's own write has no killer.

### The flag bits

The function unpacks its flags first (`0x00300580`-`0x00300601`):

| Bit | Effect | Sites |
|---:|---|---|
| `0x1` | skip both suppression gates | `0x003005A0`, `0x00300605`, `0x0030072F` |
| `0x2` | no "has fallen" message | `0x00300588`, `0x0030079C` |
| `0x4` | no presentation event at all | `0x003005D2` |
| `0x10` | no floating damage or healing number (`0x003283D0`) | `0x0030058D`, `0x003006AC` |
| `0x20` | with a delta of 0, the number counts as a heal | `0x003005AB`-`0x003005C0` |
| `0x40` | no event while the target survives | `0x003005E5`, `0x0030086C` |
| `0x80` | the HP counter of the party list or target window does not start its roll (`0x0028F1F0`) | `0x003005F6`, `0x003006D8` |
| `0x100` | the KO event is `0x200E` | `0x00300846` |

All flags, including bits this function does not test (`0x217` carries bit `0x200`), are passed on to the
status write (`0x0030076E`, `0x003007B9`).

### Refusals

The change is dropped before anything is written in these cases:

1. With flag bit `0x1` clear, `0x0030B9B0(targetUnit, sourceUnit)` returns non-zero (`0x0030060F`-`0x00300616`): a low bit
   of the battle or unit eligibility mask is set ([Gaining and losing statuses](../Status-Effects-And-KO/status-changes.md)
   has both masks).
2. The delta is negative and the target has KO, Stone or X-Zone (statuses 0, 1 and 31, mask
   `0x80000003` over `+0x64 | +0x3C`), unless `0x00377C20` reports bit `0x8000` of the active field record
   (`0x0030061C`-`0x00300635`, [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)).

A second gate only skips the store: with flag bit `0x1` clear and a delta of 0 or less, a non-zero
`0x0030B8E0(targetUnit, sourceUnit)` leaves HP unchanged, but the rest of the function runs
(`0x0030072F`-`0x00300747`).

### The floor and the cap

The new HP is `old + delta`, then limited (`0x0030063B`-`0x003006A4`):

```python
floor = targetUnit ? targetUnit[+0x48] : 0
if new < floor:            new = floor
else:
    if Disease:            cap = max(old, 1)
    elif Bubble:           cap = 2 * maxHp
    else:                  cap = maxHp
    if new > cap:          new = cap
```

Disease is status 16 (`0x10000`) and Bubble status 28, both tested on `+0x64 | +0x3C`; the maximum is
stats `+0x24`. A value below the floor takes the floor and skips the cap test (`0x00300651`-`0x00300654`), so
a floor above the cap stores the floor.

`0x0030F340` sets current HP to the same cap, up or down: it computes the cap (`0x0030F34E`-`0x0030F37C`), returns
when HP already equals it (`0x0030F381`), and writes the delta `cap - HP` through this function with flags
`0x217` (`0x0030F3AC`-`0x0030F3DC`). From 0 HP that write revives. For an Esper record (party type
`0x1B`-`0x27`) at 0 HP or below it first calls `0x003243F0(unit)` (`0x0030F383`-`0x0030F3A7`). Its callers are
the level setter `0x0030C470` (`0x0030C5A5`) and the two party and guest loops `0x0030F3F0` and `0x0030F4D0`
(`0x0030F477`, `0x0030F55E`).

A lower maximum or a new Disease pulls HP down elsewhere: the augment rebuild `0x0030FED0` limits current HP
to the cap with a bare store, downward only, without this function or the KO sequence
(`0x003104BF`-`0x00310508`, [Augments](augments.md)).

### The HP floor

The floor is the battle unit's `+0x48`. The unit installer zeroes it on every apply (`0x0023ABDB`). The
script command `btlAtelSetHpLowLimit` sets it: `0x005105E0` pops one number, truncating a float
(`0x00267E10`), and `0x00239820` stores it (`0x00239832`).

The KO test compares the stored HP with the floor, not with 0 (`0x00300784`-`0x0030078E`). So a unit with a
floor of 796 is KO'd when it reaches 796. The revive test compares the HP before the change with 0
(`0x00300752`), so such a unit cannot be revived by this function.

### The number and the counter roll

With a target unit, two publishers run before the store, on the limited value (`0x003006A7`-`0x003006E7`):

- `0x003283D0(targetUnit, delta, isHeal, 0)` posts the floating damage or healing number through `0x003BBD00`
  ([Battle numbers](../Menus-And-HUD/battle-numbers.md)), unless flag bit `0x10`. `isHeal` is `delta > 0`, or flag bit
  `0x20` when the delta is 0.
- `0x0028F1F0(targetUnit[+0x08], old, new, 0)` starts the roll of the unit's HP counter in the party list or the
  target window ([Party list](../Menus-And-HUD/party-list.md)), unless flag bit `0x80`. An HP change can so move one
  display without the other.

Then it reads the event variant: bit `0x100` of the source unit's target-buffer entry for this target
(`0x00316D70` over source `+0x778`, entry dword at `+0x788`), or 0 without both units
(`0x003006F6`-`0x0030072C`).

### Heal and revive

The store is `0x00300749`. A strictly positive delta is a heal (`0x0030074D`): the code re-reads the delta
itself, so a delta of 0 with flag bit `0x20` is not a heal. If HP before the change was above 0, the function
ends. If it was 0 or below, the target is revived: `0x0030E360(target, source, status 0, 0, 0, flags,
mode 0)` clears KO (`0x0030075C`-`0x0030077A`).

### The KO sequence

The "... has fallen." message depends on who fell: `0x002F8E90(target)` returns 1 for a party record, 2
for an Esper (party type `0x1B`-`0x27`), 4 for an enemy-table unit whose actor class nibble (`0x00263C20`) is 3,
and 8 or `0x10` for every other unit (`0x002F8E99`-`0x002F8F12`). Only 1, 2 and 4 pass the `& 7` test, so
ordinary enemies get no message.

A delta of 0 or less that leaves HP at or below the floor runs, in order:

1. the "... has fallen." message: `0x00469BB0(source, target)` posts battle message `0x10` through
   `0x0046AB10` when `0x002F8E90(target) & 7` is non-zero, unless flag bit `0x2` (`0x0030079C`-`0x003007A8`,
   `0x00469BDC`-`0x00469BF2`);
2. KO is set: `0x0030E360(target, source, status 0, -1, -1, flags, mode 3)` (`0x003007AD`-`0x003007CF`);
3. with a target unit and a source, the killer: target unit `+0x30` = source unit `+0x08`
   (`0x003007DD`-`0x003007E5`);
4. for a unit built from the enemy table (byte `+0x05` of the stats record at unit `+0x698` is 1), the
   spawn record's death count `+0x08` (`u16`) goes up by one and `+0x0C` takes the time in seconds,
   `0x0032A150() / (int)([0x01DFE0B8] × 30.0)` as an unsigned divide, with the frame base `0x01DFE0B8` 1 as
   shipped (`0x00300805`-`0x00300829`, [Action phases](../Battle-Actions/action-phases.md));
5. `0x00306F00(targetUnit)` records the death in the group ledger and ends the function when it completes
   the group ([Boss fights](../Battle-Actions/boss-fights.md); `0x0030082F`-`0x00300836`);
6. otherwise, unless flag bit `0x4`, the KO event: `0x200E` with flag bit `0x100`, else `0x2007` or `0x2008` by the
   variant bit, carrying the source unit's `+0x08` (`0x00300838`-`0x00300887`).

A target that survives gets event `0x2005` plus the variant bit, unless flag bit `0x4` or `0x40`
(`0x00300861`-`0x00300887`). Steps 3 to 6 need a target unit; a record without one is only KO'd
(`0x003007D4`).

Both events go through `0x003299B0(unit, event, value)` (`0x00300887`). It does nothing for event -1 (`0x003299B3`).
Otherwise it stores the value in unit `+0x2C`, ORs `0x5000` into the event when its low 12 bits are `0x100` or
more (`0x003299CA`-`0x003299E4`; the low 12 bits of these events are below `0x100`), and hands the event to the unit's
actor `[unit+0x10]` with `0x002EB030` (`0x003299E9`). `0x003299B0` then keeps the event in unit `+0x5C` and sets `+0x2C`
back to 0 (`0x003299EE`-`0x003299F6`).

`0x002EB030` stores the event in actor `+0xF0` and posts it through `0x002EB0D0` unless actor byte `+0x18` is 1
(`0x002EB04D`-`0x002EB073`).

At Frame Rate 60, Reks's Attack hit a Cactite (72 HP) twice. `0x00300749` stored 72 to 32
(delta -40) and then 32 to 0 (delta -41), each time with the Cactite's unit as the target and Reks's as the
source; `0x00306F00` ran with the Cactite's unit in the same frame as the second store, and its spawn record's
death count `+0x08` went from 0 to 1 and `+0x0C` took 303, the step counter at the kill divided by 60 (at Frame
Rate 60 `0x01DFE0B8` reads 2.0). In the same play `0x00310508` ran 604 times and never changed a value.

## Shipped data

The `btlAtelSetHpLowLimit` calls in the 1,114 `us` scripts:

| Fact | Count |
|---|---:|
| scripts that call it | 502 |
| calls with 0 | 6,723 |
| calls with a value above 0 | 23, in 14 scripts |

The values above 0, by script: `bhm_b01` 35,359; `bhm_c01` 35,877 and 67,105; `dgl_g01` 32,024, 12,809
and 41,046; `dgl_n01` 222,462; `dor_b01` 18,247; `dst_a01` 67; `lus_c01` 98,482, 73,861, 49,241 and
24,620; `lus_e01` 378,596, 283,947, 189,298 and 94,649; `lus_g01`-`lus_g04` 796 each; `naf_a02` 1,000;
`rsn_a01` 824.

## Modding notes

- The cap rule is in `0x00300530` and repeated in `0x0030F340`; a change to one must be made in both.
- A boss that should survive at a set HP is a `btlAtelSetHpLowLimit` call in its script, not a flag.
- Writing HP directly at stats `+0x48` skips the KO sequence, the killer and the group ledger.

## Related

- [Action results](../Battle-Actions/action-results.md) - the result record the applier reads.
- [Boss fights](../Battle-Actions/boss-fights.md) - the group ledger and what completes a fight.
- [Battle message list](../Battle-Actions/battle-message-list.md) - message `0x10`.
- [Elements](elements.md) - the absorb and Reverse rules that decide loss or gain.
- [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md) - the field record bit `0x8000` exception.
