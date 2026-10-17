---
title: "HP and KO: how damage and healing change HP, the HP floor and cap, revive from zero and what happens at KO"
kind: "system"
category: "Damage and battle formulas"
addresses: "00300530, 00300520, 003112F0, 0030F340, 00239820, 0030E360, 00469BB0, 00306F00, 003299B0"
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

`00300530(target, delta, source, flags)` changes the current HP of the stats record `target` by `delta`;
`source` is the acting unit's stats record or null. `00300520` is its absolute form: it subtracts the
current HP `+48`<sub>h</sub> from the value and jumps in (`00300520`-`00300523`). Both records are mapped to their
battle units first (`0031B860`, `00300553`, `0030055E`).

| Caller | Site | Value | Flags |
|---|---|---|---|
| the applier, target | `00311668` | result `+24`<sub>h</sub> | from result `+2C`<sub>h</sub>, below |
| the applier, user | `00311739` | result `+20`<sub>h</sub>, when result bit 7 | from result `+2C`<sub>h</sub>, no source record |
| the cap reconcile `0030F340` | `0030F3DC` | cap minus HP | `217`<sub>h</sub> |
| the deferred HP queue `003065D0`, `0030EB10` | `00306699`, `0030EB5F` | queued delta | `0`<sub>h</sub> |
| spawn and timeline code (absolute) | `00235316`, `0023A451`, `0031A09B`, `00329CAE` | value | caller's |

For the target, the applier runs only when result `+2C`<sub>h</sub> bit 8 is set (`00311610`). It uses the
absolute form for bit 3 (`00311657`-`00311661`) and builds the flags as bit 19 → flag 8, bit 10 → flag 5,
bit 18 clear → flag 6, bit 6 clear → flag 4 (`00311608`-`00311651`)
([Action results](../Battle-Actions/action-results.md)). For the user it uses the absolute form for bit
1 and maps bit 9 → flag 5, bit 17 clear → flag 6, bit 5 clear → flag 4 (`0031170A`-`00311732`); it passes
no source record, so the user's own write has no killer.

### The flag bits

The function unpacks its flags first (`00300580`-`00300601`):

| Bit | Effect | Sites |
|---:|---|---|
| `0` | skip both suppression gates | `003005A0`, `00300605`, `0030072F` |
| `1` | no "has fallen" message | `00300588`, `0030079C` |
| `2` | no presentation event at all | `003005D2` |
| `4` | no hit or heal reaction | `0030058D`, `003006AC` |
| `5` | with a delta of 0, the reaction counts as a heal | `003005AB`-`003005C0` |
| `6` | no event while the target survives | `003005E5`, `0030086C` |
| `7` | no damage number | `003005F6`, `003006D8` |
| `8` | the KO event is `200E`<sub>h</sub> | `00300846` |

All flags, including bits this function does not test (`217`<sub>h</sub> carries bit 9), are passed on to the
status write (`0030076E`, `003007B9`).

### Refusals

The change is dropped before anything is written in these cases:

1. With flag bit 0 clear, `0030B9B0(targetUnit, sourceUnit)` returns non-zero (`0030060F`-`00300616`): a low bit
   of the battle or unit eligibility mask is set ([Gaining and losing statuses](../Status-Effects-And-KO/status-changes.md)
   has both masks).
2. The delta is negative and the target has KO, Stone or X-Zone (statuses 0, 1 and 31, mask
   `80000003`<sub>h</sub> over `+64h | +3Ch`), unless `00377C20` reports bit 15 of the active field record
   (`0030061C`-`00300635`, [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)).

A second gate only skips the store: with flag bit 0 clear and a delta of 0 or less, a non-zero
`0030B8E0(targetUnit, sourceUnit)` leaves HP unchanged, but the rest of the function runs
(`0030072F`-`00300747`).

### The floor and the cap

The new HP is `old + delta`, then limited (`0030063B`-`003006A4`):

```python
floor = targetUnit ? targetUnit[+0x48] : 0
if new < floor:            new = floor
else:
    if Disease:            cap = max(old, 1)
    elif Bubble:           cap = 2 * maxHp
    else:                  cap = maxHp
    if new > cap:          new = cap
```

Disease is status 16 (`10000`<sub>h</sub>) and Bubble status 28, both tested on `+64h | +3Ch`; the maximum is
stats `+24`<sub>h</sub>. A value below the floor takes the floor and skips the cap test (`00300651`-`00300654`), so
a floor above the cap stores the floor.

`0030F340` sets current HP to the same cap, up or down: it computes the cap (`0030F34E`-`0030F37C`), returns
when HP already equals it (`0030F381`), and writes the delta `cap - HP` through this function with flags
`217`<sub>h</sub> (`0030F3AC`-`0030F3DC`). From 0 HP that write revives. For an Esper record (party type
`1B`<sub>h</sub>-`27`<sub>h</sub>) at 0 HP or below it first calls `003243F0(unit)` (`0030F383`-`0030F3A7`). Its callers are
the level setter `0030C470` (`0030C5A5`) and the two party and guest loops `0030F3F0` and `0030F4D0`
(`0030F477`, `0030F55E`).

A lower maximum or a new Disease pulls HP down elsewhere: the augment rebuild `0030FED0` limits current HP
to the cap with a bare store, downward only, without this function or the KO sequence
(`003104BF`-`00310508`, [Augments](augments.md)).

### The HP floor

The floor is the battle unit's `+48`<sub>h</sub>. The unit installer zeroes it on every apply (`0023ABDB`). The
script command `btlAtelSetHpLowLimit` sets it: `005105E0` pops one number, truncating a float
(`00267E10`), and `00239820` stores it (`00239832`).

The KO test compares the stored HP with the floor, not with 0 (`00300784`-`0030078E`). So a unit with a
floor of 796 is KO'd when it reaches 796. The revive test compares the HP before the change with 0
(`00300752`), so such a unit cannot be revived by this function.

### Reactions and the number

With a target unit, two publishers run before the store, on the limited value (`003006A7`-`003006E7`):

- `003283D0(targetUnit, delta, isHeal, 0)`, the hit or heal reaction, unless flag bit 4. `isHeal` is
  `delta > 0`, or flag bit 5 when the delta is 0.
- `0028F1F0(targetUnit[+08h], old, new, 0)`, the damage number, unless flag bit 7.

Then it reads the event variant: bit 8 of the source unit's target-buffer entry for this target
(`00316D70` over source `+778`<sub>h</sub>, entry dword at `+788`<sub>h</sub>), or 0 without both units
(`003006F6`-`0030072C`).

### Heal and revive

The store is `00300749`. A strictly positive delta is a heal (`0030074D`): the code re-reads the delta
itself, so a delta of 0 with flag bit 5 is not a heal. If HP before the change was above 0, the function
ends. If it was 0 or below, the target is revived: `0030E360(target, source, status 0, 0, 0, flags,
mode 0)` clears KO (`0030075C`-`0030077A`).

### The KO sequence

The "... has fallen." message depends on who fell: `002F8E90(target)` returns 1 for a party record, 2
for an Esper (party type `1B`<sub>h</sub>-`27`<sub>h</sub>), 4 for an enemy-table unit whose actor class (`00263C20`) is 3,
and 8 or `10`<sub>h</sub> for every other unit (`002F8E99`-`002F8F12`). Only 1, 2 and 4 pass the `& 7` test, so
ordinary enemies get no message.

A delta of 0 or less that leaves HP at or below the floor runs, in order:

1. the "... has fallen." message: `00469BB0(source, target)` posts battle message `10`<sub>h</sub> through
   `0046AB10` when `002F8E90(target) & 7` is non-zero, unless flag bit 1 (`0030079C`-`003007A8`,
   `00469BDC`-`00469BF2`);
2. KO is set: `0030E360(target, source, status 0, -1, -1, flags, mode 3)` (`003007AD`-`003007CF`);
3. with a target unit and a source, the killer: target unit `+30`<sub>h</sub> = source unit `+08`<sub>h</sub>
   (`003007DD`-`003007E5`);
4. for a unit built from the enemy table (byte `+05`<sub>h</sub> of the stats record at unit `+698`<sub>h</sub> is 1), the
   spawn record's death count `+08`<sub>h</sub> (`u16`) goes up by one and `+0C`<sub>h</sub> takes the time in seconds,
   `0032A150() / (int)([01DFE0B8] × 30.0)` as an unsigned divide, with the frame base `01DFE0B8` 1 as
   shipped (`00300805`-`00300829`, [Action phases](../Battle-Actions/action-phases.md));
5. `00306F00(targetUnit)` records the death in the group ledger and ends the function when it completes
   the group ([Boss fights](../Battle-Actions/boss-fights.md); `0030082F`-`00300836`);
6. otherwise, unless flag bit 2, the KO event: `200E`<sub>h</sub> with flag bit 8, else `2007`<sub>h</sub> or `2008`<sub>h</sub> by the
   variant bit, carrying the source unit's `+08`<sub>h</sub> (`00300838`-`00300887`).

A target that survives gets event `2005`<sub>h</sub> plus the variant bit, unless flag bit 2 or 6
(`00300861`-`00300887`). Steps 3 to 6 need a target unit; a record without one is only KO'd
(`003007D4`).

## Shipped data

The `btlAtelSetHpLowLimit` calls in the 2,990 decompiled `us` scripts:

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

- The cap rule is in `00300530` and repeated in `0030F340`; a change to one must be made in both.
- A boss that should survive at a set HP is a `btlAtelSetHpLowLimit` call in its script, not a flag.
- Writing HP directly at stats `+48`<sub>h</sub> skips the KO sequence, the killer and the group ledger.

## Related

- [Action results](../Battle-Actions/action-results.md) - the result record the applier reads.
- [Boss fights](../Battle-Actions/boss-fights.md) - the group ledger and what completes a fight.
- [Battle message list](../Battle-Actions/battle-message-list.md) - message `10`<sub>h</sub>.
- [Elements](elements.md) - the absorb and Reverse rules that decide loss or gain.
- [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md) - the field record bit 15 exception.
