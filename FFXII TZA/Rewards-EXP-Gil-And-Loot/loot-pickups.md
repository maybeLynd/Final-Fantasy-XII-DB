---
title: "Loot pickups: the ten-slot pool, creation and eviction, the one-minute lifetime and blink, collection on contact, and the pickup object"
kind: "system"
category: "Rewards: EXP, LP, gil and loot"
addresses: "00319CA0, 00319600, 00319920, 003197B0, 002FB150, 00319850, 00319A20, 00319B10, 0028F000, 003FA160, 003FC510"
---

## What the player sees

When an enemy dies and its loot roll gives at least one item, a pickup appears where the enemy
stood and the party collects everything in it, up to seven stacks, by walking the controlled
character over it. A pickup waits one minute. For the last five seconds it blinks, faster and
faster, and then it is gone. Only ten pickups can exist at once: an eleventh drop destroys the
oldest one still on the ground. A pickup that an enemy walks over disappears without giving the
party anything. The game clock has to be running for the minute to pass; while it is stopped, the
pickups wait.

## How it works

### When a pickup is made

The kill handler `00312280` makes the pickup after EXP, LP and gil are paid (see the kill rewards
page). In order (`0031256B`-`003125B4`):

1. `00265020` reads the dead enemy's position from its actor (`[enemy+0x10]`, position at
   `[actor+0xB8]`, only for an actor whose byte `+0x03` has kind 1 or 3 in its top three bits;
   otherwise 0, 0, 0).
2. `00319490(&position)` runs the placement test. A result of 0 ends the sequence with no pickup
   (`00312595`-`00312597`).
3. `003180F0(enemy, &drops)` rolls the seven drop entries (see the loot drops page). A result of 0,
   no item in any entry, ends the sequence (`003125A6`-`003125A8`).
4. `00319CA0(&drops, &position)` creates the pickup.

### The placement test

`00319490` chooses the unit that the test is made for and calls `003377C0(unit, position)`:

- The unit is the party leader's battle unit: the focus handle `022C7FE0` (`003590D0`) resolved
  by `003588B0` to its registry entry, and the unit is `[entry+0x30]` (`00263E30`). It is used only
  when `02089340` has bit 4 set and the unit's first byte has bit 3 (`003194AD`-`003194D2`);
  otherwise the unit is null.
- `003377C0` returns 0 for a null unit or one without an actor (`003377E3`-`003377F6`), so in that
  case no pickup is made.
- The acting unit is `0031ABE0([00236820(unit.b[+0xEA9])] + 8)` (`00337845`-`0033784D`). When
  `002EA7F0(acting)` returns 0 (`00337858`) the neighbour check is skipped and `00337700` runs at
  once.
- Otherwise it queries the units around the position (`00391D10` at `003378B2`, or `003920F0` at
  `003378E6` when a coordinate is NaN, up to 32 results) and walks them (`00337900`-`00337987`).
  - Skipped: the acting unit itself; a result whose `[+0xE68]` byte `+0x18` bits 1-3 equal 1
    when the leader's own equal 4; every result while `00314EB0(acting)` is 0.
  - Each remaining result is classed by `00313F80(acting, result)`; any classed result makes the
    function return 0 (`0033798D`-`0033799A`).
- With none it returns `00337700(unit, position)` (`003379A4`): the position must pass `00391410`
  (result 0), its ground cell from `00384130` must not be `0xFF`, and `00336390(position,
  max(r1, r2), unit.b[+0x1F4])` must be non-zero, which tests `0026E100` at the point and at the
  four corners `x ± r`, `z ± r`. `r1`, `r2` are the leader actor's two radii from `00265090`.

The position passed carries a fourth lane of 1.0 (`01CEBBA8`, `003194F8`).

### The pool

Ten pickup slots of `0x60` bytes start at `02EC0FA0`; the live ones form a doubly linked list
with head `02EC1360` and tail `02EC1368`. `00319B10` resets the pool: it zeroes every slot's
state, stamp, links and handle, numbers the slots 0-9 in their first dword, clears the head and
tail, and clears the presence table through `002FB250`. It runs from the area initialisation
`002342F0` (`0023443C`) and from `002341C0` (`002341F0`).

### Creation and eviction

`00319CA0(drops, position)`:

1. Scans the ten slots for one whose state `+0x04` is 0 (`00319CC5`-`00319CDA`).
2. When none is free it evicts the list head, the oldest pickup: unlinks it, posts presentation
   op 5 on its handle (`0028F000(handle, 5, ...)`), clears its presence record (`002FB2A0(slot)`),
   and zeroes its state, stamp, links and handle (`00319CDC`-`00319D3C`). That slot is reused.
3. Links the slot at the tail, copies the 56 bytes of drop entries to `+0x20`, and sets state 1
   (`00319D3F`-`00319D96`).
4. Builds the 24-byte creation descriptor: the position with fourth lane 1.0, the appearance from
   `00319A20(drops)`, and the chain level `022C3158` mapped through `01EED3A8` (`{0, 1, 2, 3}`,
   so the level itself for 0-3, and 0 for a level of 4 or more) (`00319D9D`-`00319DF0`).
5. Posts presentation op 1 and keeps the returned handle at `+0x58` (`00319DF4`-`00319E05`).
6. When the chain count `022C3164` is above 0 it calls `0016D6A0`, a `ret 0` stub that does
   nothing (`00319E08`-`00319E10`).

No drop is refused for lack of space; an older pickup is always sacrificed.

### The appearance

`00319A20(drops)` walks the seven entries. For an item id of class 1 (`0x1000`-`0x1FFF`, the
equipment ids) it takes the row `(id - 0x1000) * rowSize` of the equipment table `[02EBF0F8]`
(base through `0020E600`, row size at table `+0x08`) and maps the row's byte `+0x09` with
`0031E9F0`:

| Byte `+0x09` | `0031E9F0` result |
|---|---|
| 0 | 1 |
| 1, 10, 11, 12, 15, 16 | 2 |
| 2-6, 13, 14 | 3 |
| 7, 8, 9, 17 | 4 |
| 23-26 | 5 |
| 18 | 6 |
| 19 | 7 |
| 20 | 8 |
| 21, 22 | 9 |
| anything else | 0 |

The appearance value is 0 as soon as one entry maps to 1-5 (the function returns at once), 1 when an entry
maps to 6 and none to 1-5, and 2 otherwise, including for a pickup without equipment. Byte `+0x09`
is the equipment class; the class list is on the
[item id page](../Items-Equipment-Shops-And-Licenses/equipment-row.md).

### The lifetime

`00319600` runs every frame from the battle frame orchestrator `00234590` (`00234708`) and walks
the live list. It reads the frame counter `0208D45C` and the step constant `-30.0` (`01CEBCAC`,
loaded at `00319634`) scaled by the frame-rate scalar `01DFE0B8`:

```c
step = (int)(scalar * -30.0f);                    // -30 with the scalar at 1.0
// state 1: waiting for the object to land
if (0028EFE0(handle) == 2) { stamp = now; state = 2; publish position (002FB2D0) }   // 00319739-00319775
// states 2..6: the blink
if (now >= stamp - step * (60 - (7 - state))) { state += 1; 0028F000(handle, 2, &(7 - oldState)) }  // 003196E9-00319732
// state 7: expiry
if (now >= stamp - step * 60) { unlink; 0028F000(handle, 4, ...); 002FB2A0(slot); zero }         // 00319664-003196E1
```

The comparisons are unsigned (`jc` at `00319718` and `00319682`). With the scalar at 1.0 the
thresholds are:

| State | Fires at | Presentation call |
|---|---|---|
| 2 to 3 | stamp + 1650 | `0028F000(handle, 2, 5)` |
| 3 to 4 | stamp + 1680 | `0028F000(handle, 2, 4)` |
| 4 to 5 | stamp + 1710 | `0028F000(handle, 2, 3)` |
| 5 to 6 | stamp + 1740 | `0028F000(handle, 2, 2)` |
| 6 to 7 | stamp + 1770 | `0028F000(handle, 2, 1)` |
| 7, removed | stamp + 1800 | `0028F000(handle, 4, ...)` |

The frame counter `0208D45C` is incremented by `0032A100` (`0032A135`, called from `00234590` at
`002345CA`) only in a frame where the battle clock `003EBA90(0)` changed since the previous frame
(`022C317C`). It is reset to 0 by `0032A160` from the battle-state reset `00237DF0` (`00237E37`).

The scalar `01DFE0B8` is 1.0 in the image and becomes 2.0 at `001EDDD8` together with the 60 fps
gate `01F82E38` = 1 (`001EDDE8`). The lifetime is therefore 1800 frames at the base rate and 3600
at 60 fps: one minute either way at the 30 fps base (see the
[game settings page](../Saving-Loading-And-Settings/game-settings.md)).

### Collection on contact

The periodic unit maintenance `00310DB0` runs the contact test for a unit that is the controlled
character (its handle `+0x08` equals the focus `022C7FE0`, `003273B0` at `003110DC`) or whose
action word `+0x714` is `0x4165` (`003110E8`-`003110F4`):

1. `002FB150(unit, 1.0)` returns the first presence record, in slot order, whose XZ distance
   (`004686D0`) from the unit's actor position is strictly below `max(r1, r2) + 1.0`, with the
   radii from `00265090`; -1 when none (`00311105`-`0031110E`).
2. `00469E30(stats)` posts message `0x4E` through `0046AB10` when `002F8E90()` returns 8
   (`0031111B`).
3. A party record (stats byte `+0x05` = 0) collects it: `00319A00(slot, unit handle)`
   (`00311141`). Any other record, or no record, destroys it: `00319830(slot, unit handle)`
   (`00311284`).
4. For a party record the tick then rolls the chain bonus (see the loot drops page).

`00319920(slot, handle)`, the collect, grants every entry whose id is not `0xFFFF` with
`00300B80(id, count, 1)`, the inventory add with the notification flag (`00319950`-`00319972`),
adds 1 to the pickup counter `022C3174` (`00319974`), unlinks the slot, posts op 3 with the
collecting unit's handle, clears the presence record and zeroes state, stamp, links and handle
(`0031997A`-`003199E8`). `003197B0` is the same retirement without the grants and the counter.

### The nearest pickup

`00319850(unit, &out)` walks the live list and, through `002FB310(slot, &pos)`, takes the present
position with the smallest squared XZ distance (`003A1960`) from the unit's position `+0xE0`; the
ceiling starts at `02F973B8`, which `002368D0` sets to +inf (`00914700`, `002368F0`). It returns
the slot, or -1 when none is present. Its one caller is the movement goal decoder `00312730`
(`003129AF`): goal `0x4165` becomes the nearest pickup's position with a stop distance of
`(max(r1, r2) + 1.0) - 0.1`, computed in that order.

### The presence table

Ten records of `0x20` bytes at `022BE7F0` tell the contact and nearest tests where the live
pickups are. `002FB2D0(slot, &pos)` publishes a position (returns -1 for a slot above 9, -2 when
the record is already present, else 1), `002FB2A0(slot)` clears it, `002FB310(slot, &pos)` reads
it, and `002FB250` clears all ten.

### The pickup object

`0028F000(handle, op, arg)` drives the HUD world-object manager at `[0209BE80] + 0x57E0` and does
nothing when `0209BE80` is 0:

| Op | Effect | Function |
|---|---|---|
| 1 | create from the descriptor; returns the element address as the handle | `003FA160` |
| 2 | blink step with the remaining count 5..1 | `003FAA10` |
| 3 | collected by the unit in the argument | `003FA820(handle, unit)` |
| 4 | expired | `003FA820(handle, 0)` |
| 5 | evicted | `003FA820(handle, 0)` |
| 6 | end every element | `003FA900` |

`003FA160` takes the first free of 13 elements of `0x2A0` bytes at manager `+0x270` (free when
`+0x272` bit 0 is clear) and fills it:

- state `+0x260` = 1, fall speed `+0x264` = -0.25, appearance `+0x268`, chain level `+0x26C`;
- start position `+0x00` = the descriptor's position, rest position `+0x10` = its x and z with the
  ground height from `0026E350`; both y values + 0.5;
- linked at the end of the manager's list `+0x2490`; sound `0x50` (`00249C60`).

It returns the element, or 0 when all 13 are in use. The handle is the element's address kept in a
dword (`00319E05`), and `003FA730` reads `[handle+0x272]` before any null test.

The element update `003FC510` runs the element through its states:

- State 1: the element moves toward its rest height each frame, its speed `+0x264` growing by
  `0.02 × 01DFE0BC` per frame, and becomes state 2 on a later frame when the rest height lies
  between the old and new y, or when y already equals it (`003FC839`, `003FC8D5`). `0028EFE0`
  (`003FA730`) reports that state to the lifetime walk.
- Op 2 sets the fade step `+0x288` from the table `{4096, 2730.67, 2048, 1638.4, 1365.33, 1170.29}
  × 01DFE0BC` indexed by the remaining count, so each blink is faster than the last. `01DFE0BC` is
  1.0 in the image and 0.5 at 60 fps (`001EDDE0`), which halves the per-frame step.
- Op 3 marks the element collected, sets a phase from `sin(0208F570 × π / 30)` and plays sound
  `0x46` when a unit is given. The update then shrinks the element (state 3) and sets its state to
  0 when its scale `+0x270` has reached 0.

## Layouts

`LootPickupSlot` (`0x60` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `i32` | slot | 0-9, the index into the presence table; written by `00319B10` |
| `04` | `i32` | state | 0 free, 1 falling, 2 landed, 3-6 blinking, 7 last blink; `00319CA0`, `00319600` |
| `08` | `u32` | stamp | frame counter `0208D45C` when the pickup landed; `00319600` |
| `0C` | `u32` | pad | zeroed with the stamp (one qword store) and never read |
| `10` | `u64` | prev | pointer to the previous live pickup; `00319CA0`, `00319600`, `00319920`, `003197B0` |
| `18` | `u64` | next | pointer to the next live pickup; same writers |
| `20` | `u8[56] drops` | seven entries {u16 item, u16 pad, i32 count}, 0xFFFF = empty; copied by 00319CA0 |  |
| `58` | `u32` | handle | the pickup object; `00319CA0` |
| `5C` | `u32` | tail | not written by any of the five pool functions (`00319B10`, `00319CA0`, `00319600`, `00319920`, `003197B0`) |

`LootPresenceRecord` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | present | 1 when a position is published; `002FB2D0`, `002FB2A0`, `002FB250` |
| `01` | `u8[15] pad` | not written by the four presence functions |  |
| `10` | `f32[4] position` | x, y, z, 1.0; 002FB2D0 |  |

`LootPickupDescriptor` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `f32[4] position` | x, y, z, 1.0; 00319CA0 |  |
| `10` | `i32` | look | `00319A20` result, 0-2 |
| `14` | `i32` | level | chain level 0-3 through `01EED3A8` |

## Operations

| Function | Role |
|---|---|
| `00319490(&pos)` | placement test for a drop position; returns `003377C0`'s result |
| `00319CA0(&drops, &pos)` | create a pickup, evicting the oldest when the pool is full |
| `00319600()` | per-frame lifetime: landing, five blink steps, expiry |
| `00319A00(slot, handle)` / `00319920` | collect: grant the entries, count the pickup, retire the slot |
| `00319830(slot, handle)` / `003197B0` | retire the slot without grants |
| `00319B10()` | reset the pool and the presence table |
| `00319A20(&drops)` | appearance value (0, 1 or 2) from the equipment classes inside |
| `002FB150(unit, extra)` | first presence record within the unit's radius plus `extra` |
| `00319850(unit, &out)` | nearest present pickup, no radius |
| `002FB2D0` / `002FB2A0` / `002FB310` / `002FB250` | publish, clear, read, clear all presence records |
| `0028F000(handle, op, &arg)` | presentation ops 1-6 |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `02EC0FA0` | 10 × `0x60` | the pickup slots | `00319B10`, `00319CA0`, `00319600`, `00319920`, `003197B0` |
| `02EC1360` / `02EC1368` | ptr | live-list head and tail | the same five |
| `022BE7F0` | 10 × `0x20` | presence records | `002FB2D0`, `002FB2A0`, `002FB250` |
| `0208D45C` | u32 | frame counter, advances only while the battle clock runs | `0032A100`, reset by `0032A160` |
| `022C3174` | i32 | pickups collected since the last chain level rise | `00319920`; reset on a rise (`003184EC`) and by `003183A0` |
| `02F973B8` | f32 | +inf, the search ceiling | `002368D0` (`002368F0`) |

## Modding notes

- Ten is a literal: the scan bound in `00319CA0` (`00319CD0`) and the slot numbering in `00319B10`
  must change together, with a larger array at `02EC0FA0`.
- The lifetime is the `60` and the `-30.0` in `00319600`; the scalar `01DFE0B8` is the global
  frame-rate scalar and changes every timed system at once.
- A drop buffer must hold seven entries with `0xFFFF` in every unused one; an unset middle entry is
  granted.
- The appearance value is computed once at creation.
- Eviction is silent: the evicted pickup gets op 5, the same call as expiry.

## Related

- [Kill rewards: what an enemy's death triggers, when it gives nothing, and the order of chain, EXP, LP, gil, loot and counters](kill-rewards.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](loot-drops.md)
- [Kill chain: chain count, chain level, the chain coin and resets](kill-chain.md)
