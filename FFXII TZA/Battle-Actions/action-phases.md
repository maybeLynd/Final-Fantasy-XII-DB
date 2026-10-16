---
title: "Action phases: delay, charge time, approach, execution and the end of a battle action"
kind: "system"
category: "Battle actions"
summary: "The thirteen phases a committed battle action goes through, frame by frame - the random delay before it starts, the charge time and what speeds it up (Haste, Slow, Berserk, augments, the Battle Speed setting), walking into reach, Invisible wearing off, waiting for its turn to be shown, building the targets and resolving the effects, and when the action counts as finished - plus the charge that is kept when the same order is given again."
addresses: ["00304850", "002FA1A0", "002F8410", "002F9C00", "00313DB0", "003105D0"]
---

# Action phases: delay, charge time, approach, execution and the end of a battle action

## What the player sees

After a unit commits to an action, the action runs through a fixed sequence of phases, one or more per
frame.

1. **A short random delay** before anything happens. Enemies wait 1,200 to 2,099 units of
   progress (progress grows by 100 on each update of the action). Party-side units start at once,
   except for an action whose action data is one particular record kind (byte `+0x09` = `0x38`,
   byte `+0x08` = 1) when the last cancelled action's was not: then they wait 1,500 to 2,999.
2. **Setup.** The unit's reach for the action is worked out ([Action range](action-range.md)), the
   charge time is rolled, and **Invisible wears off** - starting any ordinary action removes it.
3. **Approach and charge.** The unit walks into reach while the charge bar fills. The charge time
   comes from the action (or the weapon, for weapon-flag actions) and the unit's speed, with a random
   part, and the augments whose text reads "Reduces action time by N%" shorten it by that
   percentage.
4. **Charge speed.** Haste makes the bar fill 1.5 times as fast, Slow half as fast, Berserk twice as
   fast, and the Battle Speed setting scales everything from 1.0 to 2.0 times.
5. **Arrival** when the unit is in reach **and** fully charged.
6. **Waiting for its turn on screen.** Some actions are shown one at a time; such an action waits
   until the previous one has finished.
7. **Execution.** The targets are gathered ([Area of effect](area-of-effect.md)), the results are worked
   out and the effects are played; summons, Quickenings and other scene actions play their scene
   instead ([Quickenings and summons](quickenings-and-summons.md)).
8. **The end**, once the animation has signalled that it is done.

### Keeping the charge

If a party member's action is cancelled before it goes off and the same action
is ordered again on the same target, the charge continues from where it stopped; enemies keep their
charge whatever the new order.

## How it works

### The state machine

`00304850` (2,034 bytes), called for a unit each frame, keeps its phase in the
unit's byte `+0x6B4` (`rsi = unit + 0x6B0`, `0030487F`). It returns -1 when the unit's target-list
count `+0x77C` is 0, when the action id `+0x714` is above `0x21E`, or - unless unit bit 24 is set -
when the phase is below 9 and the target `+0x710` does not resolve (`00304899`-`003048E2`).

It dispatches the phase at `0030493C`-`0030495A` through the table of 13 image-relative offsets at
`00305044`. Every arm ends with `inc byte [rsi+4]` and falls through to the next one on the same call
unless it has to wait (returning 0). Phase 12 returns 1: the action is finished.

| Phase | Code | What happens | Leaves when |
|---:|---|---|---|
| 0 | `0030495C` | `0030EF20(unit, row)` prepares the costs; `+0x690` = 0; unit flag bits 12, 13, 29, 31, 35 and 46 and bits 7 and 21 of `+0x04` cleared; the delay threshold `+0x764` set (below); the effective action id cached (`00387A50`) | at once |
| 1 | `003049FA` | presentation event; while `+0x760` < `+0x764`, `+0x760` += `002F9F10()` (always 100) and wait | threshold reached, to phase 3 |
| 2 | `00304A49` | entry point only | at once |
| 3 | `00304A4C` | `00305230(unit, id)`; `0030E360(stats, 0, 24, 0, ...)` removes status 24 (Invisible); range bands `002FEB80`; saved charge restored (below); charge limit `+0x76C` = `002F8410(unit)`; `00469AF0` unless the saved charge was restored for the same order; movement reset `003291B0`; `00329F80`, `00306010`; the three presentation slots `+0x694`-`+0x696` released | at once |
| 4 | `00304BA5` | presentation event; movement goal and the bands copied to the movement block (mode 1); approach point from `00339630` (else the target's position, stop distance 0.1); `00319110`; while `+0x768` < `+0x76C`, `+0x768` += `002F9C00(unit)` and `+0x770` = `+0x768`; `0033A1E0` sets bit 7 of `+0x04` (in reach) | in reach and fully charged; a scene action also waits while bit 1 of `022C2158` is set (`00304D3F`-`00304D54`); otherwise a navigation step `00325BB0` and wait |
| 5 | `00304D73` | presentation event; movement reset | at once |
| 6 | `00304DA5` | for action `0x9F` unit bit 35 set; presentation event; the phase-0 flag clears again, bit 7 of `+0x04` set; a presentation slot acquired (`0030CFB0`) | at once |
| 7 | `00304E2C` | `0030CA80` checks the slot; when it asks for the unit to be shown, the unit id goes into the 64-entry ring at `022BEDA4` (write index `022BEDA1`) and unit bit 12 is set; presentation event | slot ready and unit bit 12 clear |
| 8 | `00304EB3` | `00319420(unit+0x6B0)` | at once |
| 9 | `00304EBE` | `+0x770` = 0; targets built (`0030D160`); `00305430`; unit bit 46 set; for ids other than `0xD0`-`0xF1`, previews `00303830`; a scene action (row `+0x0C` bit 30) pays its costs (`00305640`) and starts its scene (`00306760`); any other action posts its resolved presentation event (`0030FE10`) | at once |
| 10 | `00304F62` | a scene action waits while the scene state `022C2160` is 5 or 6, then moves on; any other action: once `+0x690` has bits 1 and 3, unit bit 46 is cleared and, for the controlled member with unit bit 18, bit 0 of `+0x690` set; bit 0 of `+0x690` posts event `0x2001` | scene actions: scene over; others: `0030BC40` returns 1 (`+0x690` bits 0 and 2) |
| 11 | `00304FE9` | unit bit 13 cleared | at once |
| 12 | `00304FF3` | returns 1 | - |

### The delay threshold (phase 0, `00304987`-`003049E5`)

Phase 0 chooses the delay threshold `+0x764` this way:

- When bit 0 of the context word `+0x6B0` is set, it is cleared and the threshold is 0.
- A unit with no stats record or on the enemy side always gets `002FA1A0(unit)`.
- A party-side unit (stats `+0x05` = 0) gets `002FA1A0(unit)` only when its action data `+0x708` is a
  record with byte `+0x09` = `0x38` and byte `+0x08` = 1, and the last cancelled action's data
  `+0x738` (the cancel's copy of `+0x708`) is null or not such a record; otherwise 0.

`002FA1A0` uses the C runtime `rand()` and the frame base `F` = `01DFE0B4` (1 as shipped):

```
enemy side:  1200 * F + rand() % (900 * F)
any other:   1500 * F + rand() % (1500 * F)
```

Ids above `0x21E` never reach this machine (the entry returns -1), so internal orders neither wait
nor clear Invisible here.

### The charge time (`002F8410`, stored as the limit `+0x76C`)

The base `b` is the action row's byte `+0x09`, or, when the row has bit 27 of `+0x0C`, byte `+0x27`
of the weapon's equipment row (0, no charge, when the weapon id is out of range). The limit is 0 - no
charge - when the unit has effect 53 (bit 5 of the effect bytes `+0x6E`/`+0x7E`) and the row's byte
`+0x08` is 0, or effect 54 (bit 6) and the row's flag bit 13. A unit with speed 0 (stats `+0x2D`) gets
`9000 * F`. Otherwise:

```
t = (b * 8 / speed + b) / 10
if b != 0:
    t = t + (rand() % (15 * F)) / 100       party side   (rand() % (90 * F) on the enemy side)
    t = t - t / 100 * p
limit = (int)(30 * F * t * 100)
```

`p` sums the percentages (the `u16` at `+4`) of rows `0x5E`, `0x5F` and `0x60` of the table at
`02EBF040` for effects 94, 95 and 96 (bit 6 of `+0x73` or `+0x83`, bit 7 of `+0x73` or `+0x83`, bit 0
of `+0x74` or `+0x84`). `battle_pack.bin`'s augment text for these three reads "Reduces action time
by N%".

### The charge step (`002F9C00`, per frame in phase 4)

The step added to the charge progress each frame is built in three parts:

| Condition | Step |
|---|---:|
| no Haste or Slow, or both | 100 |
| Haste (status bit 20) | 150 |
| Slow (status bit 15) | 50 |
| Berserk (status bit 27) | the above doubled |

When bit 6 of `022C314C` is set, the step is divided by the sum of byte `+0x10` of the equipment rows of
the unit's five equipment ids (`+0x50`-`+0x58`), with an empty slot counting 0 and a sum of 0 counting
1.

Finally it is multiplied by 100, 120, 140, 160, 180 or 200 percent for a Battle Speed setting of 1 to
6 (`002DDC90`, bits 4-11 of the options word `*(0215E6E0)`, written by Config command 5 through
`002DE0F0`; any other value counts as 3).

### The saved charge (phase 3, `00304ABE`-`00304AF6`)

The cancel `003105D0` copies the commit copy
`+0x718`-`+0x72F` to `+0x730`-`+0x747`, so `+0x740`/`+0x744` hold the cancelled action's target
handle and id, and the commit keeps `+0x770`, the charge at the time, only when the unit is on the
enemy side or the new order repeats them ([Action commit](action-commit.md)). Phase 3 then sets the
progress `+0x768` to `+0x770` under the same condition and zeroes `+0x770`, so the kept charge is used
once.

### Showing one action at a time

`00313DB0`, run every frame from `00234520`, keeps one shown unit at
`02089350`. With none, it takes ids from the ring until one resolves to a living unit (or one waived
by `00377C20()`), clears its bit 12, sets bit 13, stores it and starts the display with
`00226BE0(10, unit id, ...)`. While a unit is shown and no scene is playing (state not 5 or 6), it is
released when it dies or its bit 13 is cleared - which phase 11 does - with `00225CD0(10, -1)`.

### Arrival

The `00305110` term of phase 4's arrival test is always true: `00305110(unit, id)` returns 0
in every case; for an action that may target KO'd or
stoned units (row `+0x2C` bits 6/7) whose target is in that state, it also calls
`00300310(target, ...)` and clears the target's bit 26.

## State

| Field | Width | Meaning |
|---|---|---|
| unit `+0x6B4` | u8 | phase, 0-12 |
| unit `+0x760` / `+0x764` | i32 | delay progress / delay threshold |
| unit `+0x768` / `+0x76C` | i32 | charge progress / charge limit |
| unit `+0x770` | i32 | charge kept for a repeated order |
| unit `+0x740` / `+0x744` | u32 / u16 | target handle and id of the last cancelled action |
| `022BEDA0` / `022BEDA1` / `022BEDA4` | u8 / u8 / ring | read index, write index and entries of the show queue |
| `02089350` | ptr | the unit being shown |

## Modding notes

- The charge time base is byte `+0x09` of an action row (or byte `+0x27` of the weapon row for
  weapon-flag actions with flag bit 27); a 0 makes the action instant.
- The Haste, Slow and Berserk factors are immediates in `002F9C00` (`0x96`, `0x32`, the doubling),
  and the Battle Speed factors the table `{100, 120, 140, 160, 180, 200}` built on the stack there.
- The enemy and party delay ranges are the immediates `0x4B0`/`0x384` and `0x5DC` in `002FA1A0`.

## Related

- [Action commit](action-commit.md) - what is stored before phase 0 and what the cancel keeps.
- [Action range](action-range.md) - the bands computed in phase 3 and used in phase 4.
- [Area of effect](area-of-effect.md) - the targets built in phase 9.
- [Quickenings and summons](quickenings-and-summons.md) - the scene path of phases 9 and 10.
- [Combos](combos.md) - the extra hits that re-enter this sequence.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - status bits
  15, 20, 24 and 27.
