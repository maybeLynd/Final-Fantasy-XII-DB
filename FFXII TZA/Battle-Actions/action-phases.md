---
title: "Action phases: delay, charge time, approach, execution and the end of a battle action"
kind: "system"
category: "Battle actions"
addresses: "00304850, 002FA1A0, 002F8410, 002F9C00, 00313DB0, 003105D0, 0030CBE0, 0030D070, 0030CA80, 0030C970"
---

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
   until the previous one has finished. Every action also waits until its visual effect and its
   animation are loaded, and when too many effects or animations are loaded already it waits in line
   behind the actions that asked first.
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
| `0` | `0030495C` | `0030EF20(unit, row)` prepares the costs; `+0x690` = 0; unit flag bits 12, 13, 29, 31, 35 and 46 and bits 7 and 21 of `+0x04` cleared; the delay threshold `+0x764` set (below); the effective action id cached (`00387A50`) | at once |
| `1` | `003049FA` | presentation event; while `+0x760` < `+0x764`, `+0x760` += `002F9F10()` (always 100) and wait | threshold reached, to phase 3 |
| `2` | `00304A49` | entry point only | at once |
| `3` | `00304A4C` | `00305230(unit, id)`; `0030E360(stats, 0, 24, 0, ...)` removes status 24 (Invisible); range bands `002FEB80`; saved charge restored (below); charge limit `+0x76C` = `002F8410(unit)`; `00469AF0` unless the saved charge was restored for the same order; movement reset `003291B0`; `00329F80`, `00306010`; the three presentation slots `+0x694`-`+0x696` released | at once |
| `4` | `00304BA5` | presentation event; movement goal and the bands copied to the movement block (mode 1); approach point from `00339630` (else the target's position, stop distance 0.1); `00319110`; while `+0x768` < `+0x76C`, `+0x768` += `002F9C00(unit)` and `+0x770` = `+0x768`; `0033A1E0` sets bit 7 of `+0x04` (in reach) | in reach and fully charged; a scene action also waits while bit 1 of `022C2158` is set (`00304D3F`-`00304D54`); otherwise a navigation step `00325BB0` and wait |
| `5` | `00304D73` | presentation event; movement reset | at once |
| `6` | `00304DA5` | for action `0x9F` unit bit 35 set; presentation event; the phase-0 flag clears again, bit 7 of `+0x04` set; a presentation slot acquired (`0030CFB0`) | at once |
| `7` | `00304E2C` | `0030CA80` checks the slot; when it asks for the unit to be shown, the unit id goes into the 64-entry ring at `022BEDA4` (write index `022BEDA1`) and unit bit 12 is set; presentation event | slot ready and unit bit 12 clear |
| `8` | `00304EB3` | `00319420(unit+0x6B0)` | at once |
| `9` | `00304EBE` | `+0x770` = 0; targets built (`0030D160`); `00305430`; unit bit 46 set; for ids other than `0xD0`-`0xF1`, previews `00303830`; a scene action (row `+0x0C` bit 30) pays its costs (`00305640`) and starts its scene (`00306760`); any other action posts its resolved presentation event (`0030FE10`) | at once |
| `10` | `00304F62` | a scene action waits while the scene state `022C2160` is 5 or 6, then moves on; any other action: once `+0x690` has bits 1 and 3, unit bit 46 is cleared and, for the controlled member with unit bit 18, bit 0 of `+0x690` set; bit 0 of `+0x690` posts event `0x2001` | scene actions: scene over; others: `0030BC40` returns 1 (`+0x690` bits 0 and 2) |
| `11` | `00304FE9` | unit bit 13 cleared | at once |
| `12` | `00304FF3` | returns 1 | - |

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

```python
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
| no Haste or Slow, or both | `100` |
| Haste (status bit 20) | `150` |
| Slow (status bit 15) | `50` |
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

### The presentation slots

Phases 6 and 7 hold the action in a presentation slot until its effect, its animation and, for a
scene action, its scene are loaded. There are 32 slots of `0x30` bytes at `022C17B0` (layout below),
chained in the order they were taken from `022BE978` (first) to `022BEB88` (last). A unit keeps its
slot number in `+0x694` (`0xFF` for none).

### Taking a slot

Phase 6 calls `0030CFB0(unit + 0x690, unit id, action id)` with the effective action id from
`00387090` (`00304E12`-`00304E24`):

1. Nothing happens when `+0x694` already holds a slot (`0030CFBF`).
2. A scene action (row `+0x0C` bit 30) takes the single scene reservation, bit 1 of `022C2158`, and
   gets no slot while that bit is already set. A Quickening or Concurrence id (`0xD0`-`0xF1`) skips
   the reservation while the scene state `022C2160` is 5 or 6 (`0030D011`-`0030D046`).
3. `0030D070(unit id, action id)` takes the first slot whose action id `+0x1C` is `0xFFFF`, appends
   it to the chain, sets its three load states to 1 and stores both ids; with all 32 in use it
   returns `0xFF` (`0030D070`-`0030D154`). The result goes to `+0x694` (`0030D056`).

The script verb `spattackread` (`0x29B`, `00348870`) calls `0030EEA0(unit, n)`: while `022C2170` is
4 it stores `0xD0 + n` (or -1 for `n` = -1) in the unit's `+0x758`, takes a slot for that id through
`0030CFB0` and sets `022C2170` to 1; it returns -1 when the unit does not resolve and -2 in any other
state (`0030EEA0`-`0030EF16`).

### Loading, once a frame

`0030CBE0`, run every frame from `00234590` (`002346F4`), walks the chain in order. For each slot whose
unit resolves and whose action id passes `00322C50(0x14, id, 1)` it first asks `0030C890` whether
the loads fit (`0030CC92`):

| `0030C890` returns | The slot |
|---:|---|
| 0, no room | waits, and marks every later slot as behind it (`0030CDE1`) |
| 1, room, behind a waiting slot | clears its cached answers (bits 1-4 of `+0x2C`) and waits (`0030CCA8`) |
| 1, room, first in line | loads |
| 2, nothing to load | loads |

Loading advances each of the three states from 1 (asked) through 2 (loading) to 3 (done), as the
next three sections describe.

### Loading the effect

The effect state is `+0x10`. The effect id is `0030A190(row)`: the row's `+0x28` for ids
`0xD0`-`0xF1` while the scene state is 5 or 6, otherwise the row's `+0x24` unless it is `0xFFFF`,
negative or the row has bit 30; else -1 (`0030A190`-`0030A238`).

`00328360(id)` returns -1 for -1 and otherwise starts the effect through `0042FCE0`, which counts
the start at `02CA4ED4` and calls `002FCBF0` (`00328360`-`00328368`, `0042FCE0`-`0042FCE6`). The
handle goes to `+0x24`: -1 makes the state 3, 0 leaves it at 1, any other handle 2. State 2 becomes 3
once `003226D0(handle)` sees `0024DE70` report 2 (`0030CCC0`-`0030CD05`).

### Loading the animation

The animation state is `+0x14`. `00325B40(unit, 003098D0(unit, row))` asks the streamed-animation
cache `003DCCF0` for the action's animation event. It asks nothing, and returns 0, when the unit lacks
flag bit 4 or a stats record, or has KO, Stone or X-Zone outside a field with bit 15
(`00325B40`-`00325B96`).

The answer goes to `+0x28`: 0 stays at 1, `0x80000000` gives 3, `0x80000001` gives 3 and sets unit
flag bit 31, any other 2. State 2 becomes 3 once `003DCB90` reports 3 for it (`0030CD1B`-`0030CD74`).

### Loading the scene

The scene state is `+0x18`. `0030CE10` asks for the scene
([Quickenings and summons](quickenings-and-summons.md)); on state 2, a unit without flag bit 29, or
one whose `00306B10` returns 1, sets slot bit 0 and state 3 (`0030CD93`-`0030CDD8`).

### Whether the loads fit

`0030C890(slot, unit, row)` keeps two answers in the slot's `+0x2C`: bits 1-2 for the animation and
bits 3-4 for the effect, each 0 (no room), 1 (fits) or 2 (nothing to load). It recomputes them only
while either is 0, and returns 2 when both are 2, 0 when either is 0, and 1 otherwise
(`0030C89F`-`0030C963`):

- The animation answer is `00325A20(unit, event)`: the same cache asked without loading
  (`003DC410`), giving 0 for no room, 2 for `0x80000000` or `0x80000001`, and 1 for any other result
  (`00325A78`-`00325AB5`).
- The effect answer is `0031A230(id)`: 2 for id -1, else 1 when `002FCAC0(id)` agrees and 0 when it
  does not (`0031A230`-`0031A24D`). `002FCAC0` refuses when the effect pool's free list `02EC3D70` is
  empty, and otherwise adds the weights of every pool entry in state 1, 2, 3 or 5 and the new
  effect's weight, and agrees when the sum is at most 24 (`002FCAC0`-`002FCB2B`).

```python
weight(id) = u16 at 02EC19C4 + id * 8, bits 0-4
fits = sum(weight of the pool entries in states 1, 2, 3, 5) + weight(id) <= 24
```

Both caches take their animation set from `00325AD0(unit)`: for a party-side unit (stats `+0x05` =
0) the byte at `T + u16[T] + 4` of the table `T` = `[02EBF180]`, otherwise the value `003202F0`
gives for the stats record (`00325AD0`, `00325A50`-`00325A73`).

### Ready and shown

Phase 7 calls `0030CA80(slot, unit, &show)` (`00304E3E`). It returns 1 when all three states are 3,
and 0 at once when slot bit 0 is set and `02089340` has bit `0x400` (`0030CB00`-`0030CB4A`).
`show` is set only for a ready slot whose unit has neither flag bit 12 nor 13, and then only when one
of these holds (`0030CB4C`-`0030CBA7`):

- the row's `+0x2C` has bit 8;
- the effect id `+0x24` of the row is valid (not `0xFFFF`, not negative, row bit 30 clear) and
  `002FCB40(id)`, bit 5 of the byte at `02EC19C4 + id * 8`, is 1;
- slot bit 0 is set.

With `02089340` bit `0x200`, `show` and the return are cleared (`0030CBAD`-`0030CBBF`).

### Releasing a slot

`0030C970(slot)` unlinks the slot from the chain and then (`0030C970`-`0030CA42`):

1. `00325A00(+0x28)` releases the animation through `003DC780` when the value has any of bits 1-30
   set or is 1.
2. `00317EC0(+0x24)` stops the effect through `0042FCC0` unless the handle is -1 or 0; the stop is
   counted at `02CA4ED8` and done by `002FCB60`.
3. When the scene state `+0x18` is not 0, `00306570` clears the scene for the slot's unit.
4. The slot is reset: flags bits 0-4 cleared, action id `0xFFFF`, effect handle -1, animation
   `0x80000000`, states and unit id 0.

Phase 3 releases the unit's three slot bytes `+0x694`-`+0x696` (`00304B75`, `00304B86`,
`00304B97`); the reset `003105D0` and `00310780` release them too (`00310618`, `0031062B`,
`00310819`), as do `00300060`, `003065D0`, `00308270` and `00309990`.

### Arrival

The `00305110` term of phase 4's arrival test is always true: `00305110(unit, id)` returns 0
in every case; for an action that may target KO'd or
stoned units (row `+0x2C` bits 6/7) whose target is in that state, it also calls
`00300310(target, ...)` and clears the target's bit 26.

## Layouts

A presentation slot is `0x30` bytes; the 32 slots sit at `022C17B0` (`0030D078`).

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `PresentationSlot*` | next | the next slot in the chain (`0030D11F`, `0030C9B7`) |
| `08` | `PresentationSlot*` | prev | the previous slot in the chain (`0030D122`, `0030C9CF`) |
| `10` | `i32` | effectState | 0 free, 1 asked, 2 loading, 3 done (`0030CCB1`-`0030CD05`) |
| `14` | `i32` | animState | the same for the animation (`0030CD0C`-`0030CD74`) |
| `18` | `i32` | sceneState | the same for the scene (`0030CD7B`-`0030CDD8`) |
| `1C` | `u16` | actionId | `0xFFFF` when free (`0030D0AA`, `0030CA22`) |
| `20` | `u32` | unitId | the owner's unit id (`0030D14B`) |
| `24` | `i32` | effectHandle | -1 none (`0030CCCF`, `0030CA34`) |
| `28` | `u32` | animResult | the cache's answer; `0x80000000` none (`0030CD30`, `0030CA2D`) |
| `2C` | `u32` | flags | bit 0 scene granted; bits 1-2 the animation answer, bits 3-4 the effect answer (`0030C8E2`-`0030C907`) |

## State

| Field | Width | Meaning |
|---|---|---|
| unit `+0x6B4` | `u8` | phase, 0-12 |
| unit `+0x760` / `+0x764` | `i32` | delay progress / delay threshold |
| unit `+0x768` / `+0x76C` | `i32` | charge progress / charge limit |
| unit `+0x770` | `i32` | charge kept for a repeated order |
| unit `+0x740` / `+0x744` | `u32` / `u16` | target handle and id of the last cancelled action |
| `022BEDA0` / `022BEDA1` / `022BEDA4` | `u8` / `u8` / `u8[512]` | read index, write index and the show queue: 64 entries of 8 bytes, a unit id in each entry's first dword (`00304E5C`) |
| `02089350` | `void*` | the unit being shown |
| unit `+0x694`-`+0x696` | `u8` | presentation slot numbers, `0xFF` for none |
| `022BE978` / `022BEB88` | `PresentationSlot*` | first and last slot of the chain |

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
