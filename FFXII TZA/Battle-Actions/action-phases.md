---
title: "Action phases: delay, charge time, approach, execution and the end of a battle action"
kind: "system"
category: "Battle actions"
addresses: "0x00304850, 0x002FA1A0, 0x002F8410, 0x002F9C00, 0x00313DB0, 0x003105D0, 0x0030CBE0, 0x0030D070, 0x0030CA80, 0x0030C970"
---

## What the player sees

After a unit commits to an action, the action runs through a fixed sequence of phases, one or more per
frame.

1. **A short random delay** before anything happens. Enemies wait 1,200 to 2,099 units of
   progress (progress grows by 100 on each update of the action). Party-side units start at once,
   except in one case: when the action belongs to one particular kind of action context and the last
   cancelled action did not, they wait 1,500 to 2,999.
2. **Setup.** The unit's reach for the action is worked out ([Action range](action-range.md)), the
   charge time is rolled, and **Invisible wears off** - starting any ordinary action removes it.
3. **Approach and charge.** The unit walks into reach while the charge bar fills. The charge time
   comes from the action (or the weapon, for weapon-flag actions) and the unit's speed, with a random
   part, and each of the three Swiftness licenses (augments 94-96) shortens it by 12 %, the value at
   `+4` of its augment row (the help text says 10 %).
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

While one action is being shown, the game marks a set of menu requests as unavailable in its action-availability
table, and the menu request handler refuses each request so marked until the shown unit is released.

### Keeping the charge

If a party member's action is cancelled before it goes off and the same action
is ordered again on the same target, the charge continues from where it stopped; enemies keep their
charge whatever the new order.

## How it works

### The state machine

`0x00304850` (2,034 bytes), called for a unit each frame, keeps its phase in the
unit's byte `+0x6B4` (`rsi = unit + 0x6B0`, `0x0030487F`). It returns -1 when the unit's target-list
count `+0x77C` is 0, when the action id `+0x714` is above `0x21E`, or - unless unit bit `0x1000000` is set -
when the phase is below 9 and the target `+0x710` does not resolve (`0x00304899`-`0x003048E2`).

It dispatches the phase at `0x0030493C`-`0x0030495A` through the table of 13 image-relative offsets at
`0x00305044`. Every arm ends with `inc byte [rsi+4]` and falls through to the next one on the same call
unless it has to wait (returning 0); the scene arm of phase 10, while the scene state `0x022C2160` is
not 5 or 6, raises the phase to 11 and returns 0 (`0x00304F62`-`0x00304F8C`), so phase 11 runs on the
next call. Phase 12 returns 1: the action is finished.

| Phase | Code | What happens | Leaves when |
|---:|---|---|---|
| `0` | `0x0030495C` | `0x0030EF20(unit, row)` prepares the costs; `+0x690` = 0; unit flag bits `0x1000`, `0x2000`, `0x20000000`, `0x80000000`, `0x800000000` and `0x400000000000` and bits `0x80` and `0x200000` of `+0x04` cleared; the delay threshold `+0x764` set (below); the effective action id cached (`0x00387A50`) | at once |
| `1` | `0x003049FA` | presentation event; while `+0x760` < `+0x764`, `+0x760` += `0x002F9F10()` (always 100) and wait | threshold reached, to phase 3 |
| `2` | `0x00304A49` | entry point only | at once |
| `3` | `0x00304A4C` | `0x00305230(unit, id)`; `0x0030E360(stats, 0, 24, 0, ...)` removes status 24 (Invisible); range bands `0x002FEB80`; saved charge restored (below); charge limit `+0x76C` = `0x002F8410(unit)`; `0x00469AF0` unless the saved charge was restored for the same order; movement reset `0x003291B0`; `0x00329F80`, `0x00306010`; the three presentation slots `+0x694`-`+0x696` released | at once |
| `4` | `0x00304BA5` | presentation event; movement goal and the bands copied to the movement block (mode 1); approach point from `0x00339630`, which always answers 1 (`0x00339A24`), so the arm for a 0 answer (the target's position, stop distance 0.1, `0x00304CAF`-`0x00304CC8`) is not taken; `0x00319110`; while `+0x768` < `+0x76C`, `+0x768` += `0x002F9C00(unit)` and `+0x770` = `+0x768`; `0x0033A1E0` sets bit `0x80` of `+0x04` (in reach) | in reach and fully charged; a scene action also waits while bit `0x2` of `0x022C2158` is set (`0x00304D3F`-`0x00304D54`); otherwise a navigation step `0x00325BB0` and wait |
| `5` | `0x00304D73` | presentation event; movement reset | at once |
| `6` | `0x00304DA5` | for action `0x9F` unit bit `0x800000000` set; presentation event; the phase-0 flag clears again, bit `0x80` of `+0x04` set; a presentation slot acquired (`0x0030CFB0`) | at once |
| `7` | `0x00304E2C` | `0x0030CA80` checks the slot; when it asks for the unit to be shown, the unit id goes into the 64-entry ring at `0x022BEDA4` (write index `0x022BEDA1`) and unit bit `0x1000` is set; presentation event | slot ready and unit bit `0x1000` clear |
| `8` | `0x00304EB3` | `0x00319420(unit+0x6B0)` | at once |
| `9` | `0x00304EBE` | `+0x770` = 0; targets built (`0x0030D160`); `0x00305430`; unit bit `0x400000000000` set; for ids other than `0xD0`-`0xF1` (the Quickenings and Concurrences, which skip both), the previews `0x00303830` and, for a scene action (row `+0x0C` bit `0x40000000`), the cost payment `0x00305640`; a scene action then starts its scene (`0x00306760`); any other action posts its resolved presentation event (`0x0030FE10`) | at once |
| `10` | `0x00304F62` | a scene action waits while the scene state `0x022C2160` is 5 or 6, then moves on; any other action: once `+0x690` has bits `0x2` and `0x8`, unit bit `0x400000000000` is cleared and, for the controlled member with unit bit `0x40000`, bit `0x1` of `+0x690` set; bit `0x1` of `+0x690` posts event `0x2001` | scene actions: scene over; others: `0x0030BC40` returns 1 (`+0x690` bits `0x1` and `0x4`) |
| `11` | `0x00304FE9` | unit bit `0x2000` cleared | at once |
| `12` | `0x00304FF3` | returns 1 | - |

`0x00303830(unit, row, list)` previews the action in one of two ways (`0x00303854`-`0x00303868`).
With a non-zero count byte `+0x6B6` it walks that many bytes from `+0x6B9`: each names
target stats through `0x00320A40`, and a null answer or a user with no battle unit
(`0x0031B860` of unit `+0x698`) skips the byte (`0x00303887`-`0x003038B0`).

For each target it clears a `0x148`-byte result on its stack, sets bit `0x1` of the
result's first dword when the user unit's first qword has bit `0x800000000`, and
calls `0x00385680` and then `0x004698C0`, both as `(row index, user stats, target stats,
result)`; the row index is `(row - first row) / row size` for the table `0x02EBF138`.
The result's dword `+0x08` goes to the user unit's `+0xE54` (`0x003038BE`-`0x00303954`).

With a count of 0 it walks the target list, `0x10`-byte entries from `+0x08` with the
count at `+0x04`: each entry whose unit `0x0031B760` resolves gets
`0x00303A00(user stats, target stats, row, index, entry + 8, 0)` (`0x00303981`-`0x003039D6`).

### The delay threshold (phase 0, `0x00304987`-`0x003049E5`)

Phase 0 chooses the delay threshold `+0x764` this way:

- When bit `0x1` of the command word `+0x6B0` is set, it is cleared and the threshold is 0.
- A unit with no stats record or on the enemy side always gets `0x002FA1A0(unit)`.
- A party-side unit (stats `+0x05` = 0) gets `0x002FA1A0(unit)` only when its action context `+0x708` is a
  record with byte `+0x09` = `0x38` and byte `+0x08` = 1, and the last cancelled action's context
  `+0x738` (the cancel's copy of `+0x708`) is null or not such a record; otherwise 0.

`0x002FA1A0` uses the C runtime `rand()` and the frame base `F` = `0x01DFE0B4` (1 at 30 fps, 2 at 60: `0x001EDDF2`):

```
enemy side:  1200 * F + rand() % (900 * F)
any other:   1500 * F + rand() % (1500 * F)
```

Ids above `0x21E` never reach this machine (the entry returns -1), so internal orders neither wait
nor clear Invisible here.

### The charge time (`0x002F8410`, stored as the limit `+0x76C`)

The base `b` is the action row's byte `+0x09`, or, when the row has bit `0x8000000` of `+0x0C`, byte `+0x27`
of the weapon's equipment row (0, no charge, when the weapon id is out of range). The limit is 0 - no
charge - when the unit has augment 53 (Celerity) (bit `0x20` of the augment layer bytes `+0x6E`/`+0x7E`) and the row's byte
`+0x08` is 0, or augment 54 (Swiftcast) (bit `0x40`) and the row's flag bit `0x2000`. A unit with speed 0 (stats `+0x2D`) gets
`9000 * F`. Otherwise:

```python
t = (b * 8 / speed + b) / 10
if b != 0:
    t = t + (rand() % (15 * F)) / 100       party side   (rand() % (90 * F) on the enemy side)
    t = t - t / 100 * p
limit = (int)(30 * F * t * 100)
```

`p` sums the percentages (the `u16` at `+4`) of rows `0x5E`, `0x5F` and `0x60` of the table at
`0x02EBF040` for effects 94, 95 and 96 (bit `0x40` of `+0x73` or `+0x83`, bit `0x80` of `+0x73` or `+0x83`, bit `0x1`
of `+0x74` or `+0x84`). `battle_pack.bin`'s augment text for these three reads "Reduces action time
by 10%.", while the value at `+4` is 12.

### The charge step (`0x002F9C00`, per frame in phase 4)

The step added to the charge progress each frame is built in three parts:

| Condition | Step |
|---|---:|
| no Haste or Slow, or both | `100` |
| Haste (status bit `0x100000`) | `150` |
| Slow (status bit `0x8000`) | `50` |
| Berserk (status bit `0x8000000`) | the above doubled: `step = step + step` when `s & 0x8000000` (`add edi, edi`, `0x002F9C5C`-`0x002F9C62`), with the status word `s = [+0x698][+0x64] OR [+0x698][+0x3C]` (`0x002F9C23`-`0x002F9C26`) |

When bit `0x40` of `0x022C314C` is set (`[0x022C314C] & 0x40`, `0x0031A900`), the step is divided by the sum of byte
`+0x10` of the equipment rows of the unit's five equipment ids (`+0x50`-`+0x58`), with an empty slot counting 0
and a sum of 0 counting 1: `step = step / (sum == 0 ? 1 : sum)` (`cmove esi, eax` at `0x002F9E8D`, `idiv esi` at
`0x002F9E93`).

Finally it is multiplied by 100, 120, 140, 160, 180 or 200 percent for a Battle Speed setting of 1 to
6 (`0x002DDC90`, the field `0xFF0` of the options word `*(0x0215E6E0)`, written by Config command 5 through
`0x002DE0F0`; any other value counts as 3).

### The saved charge (phase 3, `0x00304ABE`-`0x00304AF6`)

The cancel `0x003105D0` copies the commit copy
`+0x718`-`+0x72F` to `+0x730`-`+0x747`, so `+0x740`/`+0x744` hold the cancelled action's target
handle and id, and the commit keeps `+0x770`, the charge at the time, only when the unit is on the
enemy side or the new order repeats them ([Action commit](action-commit.md)). Phase 3 then sets the
progress `+0x768` to `+0x770` under the same condition and zeroes `+0x770`, so the kept charge is used
once.

### Showing one action at a time

`0x00313DB0`, run every frame from `0x00234520`, keeps one shown unit at `0x02089350`. With no unit shown, it pops ids from
the 64-entry ring at `0x022BEDA4` (read index `0x022BEDA0`, write index `0x022BEDA1`; id 0 when the two match) and
resolves each with `0x0031B7E0`, which answers 0 while bit `0x10` of `0x02089340` is clear or `0x003588B0` finds no actor.
An id that resolves to no unit ends the search for the frame, with that id consumed (`0x00313E11`); an empty ring ends
it the same way, since `0x003588B0(0)` is 0.

Every unit it resolves has its bit `0x1000` cleared and its bit `0x2000` set (`0x00313E17`, `0x00313E1E`) before it is
tested. A unit with no record at `+0x698` (`0x00313E2F`), or with KO, Stone or X-Zone (mask `0x80000003` of that
record's `+0x64` and `+0x3C`) while `0x00377C20()` is 0 (`0x00313E37`-`0x00313E46`), is passed over and the next id is
popped. The first living unit (or one waived by `0x00377C20()`) is stored and starts the display with
`0x00226BE0(10, unit id, ...)` (`0x00313E48`, `0x00313E98`).

That call passes fade -1 and flag -1, and at party-control level 2 (`0x0030D9A0`) a non-zero `0x0031E860(0x00327200())`
as a one-entry handle list (`0x00313E52`-`0x00313E75`). The body then runs the apply `0x00226280`, the sound stop
`0x002DEE70` and `0x00313A00` (`0x00313E9D`-`0x00313EA7`).

While a unit is shown and no scene is playing (state not 5 or 6; with state 5 or 6 the body returns at
`0x00313EC8`), it is released when it dies (KO, Stone or X-Zone while `0x00377C20()` is 0) or its bit `0x2000` is
cleared - which phase 11 does - with `0x00225CD0(10, -1)`. It is also released when it has no record at `+0x698`
(`0x00313ED4`). The release zeroes `0x02089350` and ends with a tail jump to `0x00313A00` (`0x00313EF5`-`0x00313F13`).

While a unit is shown, `0x00313A00` sets the bits `0x1019FF` (`0x1` to `0x100`, `0x800`, `0x1000` and `0x100000`) of row
2 of the action-availability table
`0x0215F1C0` (`0x00313A68`-`0x00313AF5`; [Action availability](../Controls-And-Input/action-availability.md)), and the menu
request router `0x00254B50` refuses a request whose id a set bit lists (`0x00254B80`-`0x00254BC1`;
[Menu requests](../Menus-And-HUD/menus.md)).

### The presentation slots

Phases 6 and 7 hold the action in a presentation slot until its effect, its animation and, for a
scene action, its scene are loaded. There are 32 slots of `0x30` bytes at `0x022C17B0` (layout below),
chained in the order they were taken from `0x022BE978` (first) to `0x022BEB88` (last). A unit keeps its
slot number in `+0x694` (`0xFF` when it holds no slot).

### Taking a slot

Phase 6 calls `0x0030CFB0(unit + 0x690, unit id, action id)` with the effective action id from
`0x00387090` (`0x00304E12`-`0x00304E24`):

1. Nothing happens when `+0x694` already holds a slot (`0x0030CFBF`).
2. A scene action (row `+0x0C` bit `0x40000000`) takes the single scene reservation, bit `0x2` of `0x022C2158`, and
   gets no slot while that bit is already set. A Quickening or Concurrence id (`0xD0`-`0xF1`) skips
   the reservation while the scene state `0x022C2160` is 5 or 6 (`0x0030D011`-`0x0030D046`).
3. `0x0030D070(unit id, action id)` takes the first slot whose action id `+0x1C` is `0xFFFF`, appends
   it to the chain, sets its three load states to 1 and stores both ids; with all 32 in use it
   returns `0xFF` (`0x0030D070`-`0x0030D154`). The result goes to `+0x694` (`0x0030D056`).

The script verb `spattackread` (`0x29B`, `0x00348870`) calls `0x0030EEA0(unit, n)`: while `0x022C2170` is
4 it stores `0xD0 + n` (or -1 for `n` = -1) in the unit's `+0x758`, takes a slot for that id through
`0x0030CFB0` and sets `0x022C2170` to 1; it returns -1 when the unit does not resolve and -2 in any other
state (`0x0030EEA0`-`0x0030EF16`).

### Loading, once a frame

`0x0030CBE0`, run every frame from `0x00234590` (`0x002346F4`), walks the chain in order. For each slot whose
unit resolves (`0x0031B7E0(+0x20)`), whose action id passes `0x00322C50(0x14, id, 1)` and whose action row
resolves (the table `[0x02EBF138]` and its base from `0x0020E600` non-null, `0x0030CC3F`-`0x0030CC83`) it first asks
`0x0030C890` whether the loads fit (`0x0030CC92`); a slot that fails any of these is skipped and marks no later
slot (`0x0030CC1F`, `0x0030CC39`, `0x0030CC49`, `0x0030CC5A`, `0x0030CC83`):

| `0x0030C890` returns | The slot |
|---:|---|
| 0, no room | waits, and marks every later slot as behind it (`0x0030CDE1`) |
| 1, room, behind a waiting slot | clears its cached answers (bits `0x1E` of `+0x2C`) and waits (`0x0030CCA8`) |
| 1, room, first in line | loads |
| 2, nothing to load | loads |

Loading advances each of the three states from 1 (asked) through 2 (loading) to 3 (done), as the
next three sections describe.

### Loading the effect

The effect state is `+0x10`. The effect id is `0x0030A190(row)`: the row's `+0x28` for ids
`0xD0`-`0xF1` while the scene state is 5 or 6, otherwise the row's `+0x24` unless it is `0xFFFF`,
negative or the row has bit `0x40000000`; else -1 (`0x0030A190`-`0x0030A238`).

`0x00328360(id)` returns -1 for -1 and otherwise starts the effect through `0x0042FCE0`, which counts
the start at `0x02CA4ED4` and calls `0x002FCBF0` (`0x00328360`-`0x00328368`, `0x0042FCE0`-`0x0042FCE6`). The
handle goes to `+0x24`: -1 makes the state 3, 0 leaves it at 1, any other handle 2. State 2 becomes 3
once `0x003226D0(handle)` sees `0x0024DE70` report 2 (`0x0030CCC0`-`0x0030CD05`).

### Loading the animation

The animation state is `+0x14`. `0x00325B40(unit, 0x003098D0(unit, row))` asks the streamed-animation
cache `0x003DCCF0` for the action's animation event. It asks nothing, and returns 0, when the unit lacks
flag bit `0x10` or a stats record, or has KO, Stone or X-Zone outside a field with bit `0x8000`
(`0x00325B40`-`0x00325B96`).

The answer goes to `+0x28`: 0 stays at 1, `0x80000000` gives 3, `0x80000001` gives 3 and sets unit
flag bit `0x80000000`, any other 2. State 2 becomes 3 once `0x003DCB90` reports 3 for it (`0x0030CD1B`-`0x0030CD74`).

### Loading the scene

The scene state is `+0x18`. On state 1 `0x0030CE10(unit, row)` asks for the scene
([Quickenings and summons](quickenings-and-summons.md)): an answer of -1 makes the state 3 at once without
touching slot bit `0x1`, 1 makes it 2, and any other answer leaves it at 1 (`0x0030CD93`-`0x0030CDB1`). On state 2,
a unit without flag bit `0x20000000`, or
one whose `0x00306B10` returns 1, sets slot bit `0x1` and state 3 (`0x0030CDB8`-`0x0030CDD8`).

### Whether the loads fit

`0x0030C890(slot, unit, row)` keeps two answers in the slot's `+0x2C`: bits `0x6` for the animation and
bits `0x18` for the effect, each 0 (no room), 1 (fits) or 2 (nothing to load). It recomputes them only
while either is 0, and returns 2 when both are 2, 0 when either is 0, and 1 otherwise
(`0x0030C89F`-`0x0030C963`):

- The animation answer is `0x00325A20(unit, event)`: the same cache asked without loading
  (`0x003DC410`), which for a motion not yet held that would fit still releases the ready entries without
  users when no entry is free (`0x003DCE5E`), giving 0 for no room, 2 for `0x80000000` or `0x80000001`, and 1
  for any other result
  (`0x00325A78`-`0x00325AB5`).
- The effect answer is `0x0031A230(id)`: 2 for id -1, else 1 when `0x002FCAC0(id)` agrees and 0 when it
  does not (`0x0031A230`-`0x0031A24D`). `0x002FCAC0` refuses when the effect pool's free list `0x02EC3D70` is
  empty, and otherwise adds the weights of every pool entry in state 1, 2, 3 or 5 and the new
  effect's weight, and agrees when the sum is at most 24 (`0x002FCAC0`-`0x002FCB2B`).

```python
weight(id) = u16 at 0x02EC19C4 + id * 8, bits 0x1F
fits = sum(weight of the pool entries in states 1, 2, 3, 5) + weight(id) <= 24
```

Both caches take their animation set from `0x00325AD0(unit)`: for a party-side unit (stats `+0x05` =
0) the byte at `T + u16[T] + 4` of the table `T` = `[0x02EBF180]`, otherwise the value `0x003202F0`
gives for the stats record (`0x00325AD0`, `0x00325A50`-`0x00325A73`).

### Ready and shown

Phase 7 calls `0x0030CA80(slot, unit, &show)` (`0x00304E3E`). With a non-null `show` it first writes 0 there
(`0x0030CAFA`). It returns 1 when all three states are 3,
and 0 at once when slot bit `0x1` is set and `0x02089340` has bit `0x400` (`0x0030CB00`-`0x0030CB4A`).
`show` is set only for a ready slot whose unit has neither flag bit `0x1000` nor `0x2000` (the test of
`0x3000` at `0x0030CB58`), and then only when one
of these holds (`0x0030CB4C`-`0x0030CBA7`):

- the row's `+0x2C` has bit `0x100`;
- the effect id `+0x24` of the row is valid (not `0xFFFF`, not negative, row bit `0x40000000` clear) and
  `0x002FCB40(id)`, bit `0x20` of the byte at `0x02EC19C4 + id * 8`, is 1. No store sets that bit: the word is cleared
  by the reset `0x002FC200` and written only there, with the value masked to `0x1F` (`0x002FC2E4`-`0x002FC2EE`), so this
  case does not hold;
- slot bit `0x1` is set.

When `show` ends up 1 and `0x02089340` has bit `0x200`, `show` and the return are cleared (`0x0030CBA9`,
`0x0030CBAD`-`0x0030CBBF`); when `show` ends up 0, or the caller passes no `show`, the return is the ready answer
whatever bit `0x200` is (`0x0030CB4F`, `0x0030CBAB`, `0x0030CBC3`).

### Releasing a slot

`0x0030C970(slot)` takes a slot index. An index above `0x1F` (`0xFF` included) names no slot, and the call
does nothing (`0x0030C983`-`0x0030C9A4`, `0x0030C9F2`). Otherwise it unlinks the slot from the chain, moving the
chain's first `0x022BE978` or last `0x022BEB88` slot when the slot was one of them, and zeroes its two links, and
then (`0x0030C9B7`-`0x0030CA42`):

1. `0x00325A00(+0x28)` releases the animation through `0x003DC780` when the value has any of bits `0x7FFFFFFE`
   set or is 1.
2. `0x00317EC0(+0x24)` stops the effect through `0x0042FCC0` unless the handle is -1 or 0; the stop is
   counted at `0x02CA4ED8` and done by `0x002FCB60`.
3. When the scene state `+0x18` is not 0, `0x00306570` clears the scene for the slot's unit, the unit
   `0x0031B7E0` finds for the unit id `+0x20` (`0x0030CA09`-`0x0030CA14`).
4. The slot is reset: flags `0x1F` cleared, action id `0xFFFF`, effect handle -1, animation
   `0x80000000`, states and unit id 0.

Phase 3 releases the unit's three slot bytes `+0x694`-`+0x696` (`0x00304B75`, `0x00304B86`,
`0x00304B97`); the reset `0x003105D0` and `0x00310780` release them too (`0x00310618`, `0x0031062B`,
`0x00310819`), as do `0x00300060`, `0x003065D0`, `0x00308270` and `0x00309990`.

### Arrival

The `0x00305110` term of phase 4's arrival test is always true: `0x00305110(unit, id)` returns 0 in every case. For an id
below `0x116` with row `+0x2C` bit `0x40` or `0x80` (the action may target KO'd or stoned units), a target that
resolves, has no stats record or is in that state, and answers 0 from `0x002E9600(target +0x10)` also gets
`0x00300310(target, ...)` and has its bit `0x4000000` cleared.

## Layouts

A presentation slot is `0x30` bytes; the 32 slots sit at `0x022C17B0` (`0x0030D078`).

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `PresentationSlot*` | next | the next slot in the chain (`0x0030D11F`, `0x0030C9B7`) |
| `+0x08` | `PresentationSlot*` | prev | the previous slot in the chain (`0x0030D122`, `0x0030C9CF`) |
| `+0x10` | `i32` | effectState | 0 free, 1 asked, 2 loading, 3 done (`0x0030CCB1`-`0x0030CD05`) |
| `+0x14` | `i32` | animState | the same for the animation (`0x0030CD0C`-`0x0030CD74`) |
| `+0x18` | `i32` | sceneState | the same for the scene (`0x0030CD7B`-`0x0030CDD8`) |
| `+0x1C` | `u16` | actionId | `0xFFFF` when free (`0x0030D0AA`, `0x0030CA22`) |
| `+0x20` | `u32` | unitId | the owner's unit id (`0x0030D14B`) |
| `+0x24` | `i32` | effectHandle | -1 when no effect is held (`0x0030CCCF`, `0x0030CA34`) |
| `+0x28` | `u32` | animResult | the cache's answer; `0x80000000` when no animation is held (`0x0030CD30`, `0x0030CA2D`) |
| `+0x2C` | `u32` | flags | bit `0x1` scene granted; bits `0x6` the animation answer, bits `0x18` the effect answer (`0x0030C8E2`-`0x0030C907`) |

## State

| Field | Width | Meaning |
|---|---|---|
| unit `+0x6B4` | `u8` | phase, 0-12 |
| unit `+0x760` / `+0x764` | `i32` | delay progress / delay threshold |
| unit `+0x768` / `+0x76C` | `i32` | charge progress / charge limit |
| unit `+0x770` | `i32` | charge kept for a repeated order |
| unit `+0x740` / `+0x744` | `u32` / `u16` | target handle and id of the last cancelled action |
| `0x022BEDA0` / `0x022BEDA1` / `0x022BEDA4` | `u8` / `u8` / `u8[512]` | read index, write index and the show queue: 64 entries of 8 bytes, a unit id in each entry's first dword (`0x00304E5C`) |
| `0x02089350` | `void*` | the unit being shown |
| unit `+0x694`-`+0x696` | `u8` | presentation slot numbers, `0xFF` when no slot is held |
| `0x022BE978` / `0x022BEB88` | `PresentationSlot*` | first and last slot of the chain |

## Modding notes

- The charge time base is byte `+0x09` of an action row (or byte `+0x27` of the weapon row for
  weapon-flag actions with flag bit `0x8000000`); a 0 makes the action instant.
- The Haste, Slow and Berserk factors are immediates in `0x002F9C00` (`0x96`, `0x32`, the doubling),
  and the Battle Speed factors the table `{100, 120, 140, 160, 180, 200}` built on the stack there.
- The enemy and party delay ranges are the immediates `0x4B0`/`0x384` and `0x5DC` in `0x002FA1A0`.

## Related

- [Action commit](action-commit.md) - what is stored before phase 0 and what the cancel keeps.
- [Action range](action-range.md) - the bands computed in phase 3 and used in phase 4.
- [Area of effect](area-of-effect.md) - the targets built in phase 9.
- [Quickenings and summons](quickenings-and-summons.md) - the scene path of phases 9 and 10.
- [Combos](combos.md) - the extra hits that re-enter this sequence.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - status bits
  `0x8000`, `0x100000`, `0x1000000` and `0x8000000`.
