---
title: "Loot pickups: the ten-slot pool, creation and eviction, the one-minute lifetime and blink, collection on contact, and the pickup object"
kind: "system"
category: "Rewards: EXP, LP, gil and loot"
addresses: "0x00319CA0, 0x00319600, 0x00319920, 0x003197B0, 0x002FB150, 0x00319850, 0x00319A20, 0x00319B10, 0x0028F000, 0x003FA160, 0x003FC510"
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

The kill handler `0x00312280` makes the pickup after EXP, LP and gil are paid (see
[Kill rewards](kill-rewards.md)). In order (`0x0031256B`-`0x003125B4`):

1. `0x00265020` reads the dead enemy's position from its actor (`[enemy+0x10]`, position at
   `[actor+0xB8]`, only for an actor whose byte `+0x03` has kind 1 or 3 in its top three bits;
   otherwise 0, 0, 0).
2. `0x00319490(&position)` runs the placement test. A result of 0 ends the sequence with no pickup
   (`0x00312595`-`0x00312597`).
3. `0x003180F0(enemy, &drops)` rolls the seven drop entries (see [Loot drops](loot-drops.md)). A result of 0,
   no item in any entry, ends the sequence (`0x003125A6`-`0x003125A8`).
4. `0x00319CA0(&drops, &position)` creates the pickup.

### The placement test

`0x00319490` chooses the unit that the test is made for and calls `0x003377C0(unit, position)`:

- The unit is the party leader's battle unit: the focus handle `0x022C7FE0` (`0x003590D0`) resolved
  by `0x003588B0` to its registry entry, and the unit is `[entry+0x30]` (`0x00263E30`). It is used only
  when `0x02089340` has bit `0x10` set and the unit's first byte has bit `0x8` (`0x003194AD`-`0x003194D2`);
  otherwise the unit is null.
- `0x003377C0` returns 0 for a null unit or one without an actor (`0x003377E3`-`0x003377F6`), so in that
  case no pickup is made.
- The acting unit is `0x0031ABE0([0x00236820(unit.b[+0xEA9])] + 8)` (`0x00337845`-`0x0033784D`). When
  `0x002EA7F0(acting)` returns 0 (`0x00337858`) the neighbour check is skipped and `0x00337700` runs at
  once.
- Otherwise it queries the units around the position (`0x00391D10` at `0x003378B2`, or `0x003920F0` at
  `0x003378E6` when a coordinate is NaN, up to 32 results) and walks them (`0x00337900`-`0x00337987`).
  - Skipped: the acting unit itself; a result whose `[+0xE68]` byte `+0x18` holds 1 in the
    three-bit field under the mask `0xE` when the leader's own field holds 4
    (`0x0033792B`-`0x00337951`); every result while `0x00314EB0(acting)` is 0.
  - Each remaining result is classed by `0x00313F80(acting, result)`; any classed result makes the
    function return 0 (`0x0033798D`-`0x0033799A`).
- With none it returns `0x00337700(unit, position)` (`0x003379A4`): the position must pass `0x00391410`
  (result 0), its ground cell from `0x00384130` must not be `0xFF`, and `0x00336390(position,
  max(r1, r2), unit.b[+0x1F4])` must be non-zero, which tests `0x0026E100` at the point and at the
  four corners `x ± r`, `z ± r`. `r1`, `r2` are the leader actor's two radii from `0x00265090`.

The position passed carries a fourth lane of 1.0 (`0x01CEBBA8`, `0x003194F8`).

### The pool

Ten pickup slots of `0x60` bytes start at `0x02EC0FA0`; the live ones form a doubly linked list
with head `0x02EC1360` and tail `0x02EC1368`. `0x00319B10` resets the pool: it zeroes every slot's
state, stamp, links and handle, numbers the slots 0-9 in their first dword, clears the head and
tail, and clears the presence table through `0x002FB250`. It runs from the area initialisation
`0x002342F0` (`0x0023443C`) and from `0x002341C0` (`0x002341F0`).

### Creation and eviction

`0x00319CA0(drops, position)`:

1. Scans the ten slots for one whose state `+0x04` is 0 (`0x00319CC5`-`0x00319CDA`).
2. When none is free it evicts the list head, the oldest pickup: unlinks it, posts presentation
   op 5 on its handle (`0x0028F000(handle, 5, ...)`), clears its presence record (`0x002FB2A0(slot)`),
   and zeroes its state, stamp, links and handle (`0x00319CDC`-`0x00319D3C`). That slot is reused.
3. Links the slot at the tail, copies the 56 bytes of drop entries to `+0x20`, and sets state 1
   (`0x00319D3F`-`0x00319D96`).
4. Builds the 24-byte creation descriptor: the position with fourth lane 1.0, the appearance from
   `0x00319A20(drops)`, and the chain level `0x022C3158` mapped through `0x01EED3A8` (`{0, 1, 2, 3}`,
   so the level itself for 0-3, and 0 for a level of 4 or more) (`0x00319D9D`-`0x00319DF0`).
5. Posts presentation op 1 and keeps the returned handle at `+0x58` (`0x00319DF4`-`0x00319E05`).
6. When the breaks in a row `0x022C3164` are above 0 it calls `0x0016D6A0`, a `ret 0` stub that does
   nothing (`0x00319E08`-`0x00319E10`).

No drop is refused for lack of space; an older pickup is always sacrificed.

### The appearance

`0x00319A20(drops)` walks the seven entries. For an item id of class 1 (`0x1000`-`0x1FFF`, the
equipment ids) it takes the row `(id - 0x1000) * rowSize` of the equipment table `[0x02EBF0F8]`
(base through `0x0020E600`, row size at table `+0x08`) and maps the row's byte `+0x09` with
`0x0031E9F0`:

| Byte `+0x09` | `0x0031E9F0` result |
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
[equipment row page](../Items-Equipment-Shops-And-Licenses/equipment-row.md).

### The lifetime

`0x00319600` runs every frame from the battle frame orchestrator `0x00234590` (`0x00234708`) and walks
the live list. It reads the frame counter `0x0208D45C` and the step constant `-30.0` (`0x01CEBCAC`,
loaded at `0x00319634`) scaled by the frame-rate scalar `0x01DFE0B8`:

```c
step = (int)(scalar * -30.0f);                    // -30 with the scalar at 1.0
// state 1: waiting for the object to land
if (0x0028EFE0(handle) == 2) { stamp = now; state = 2; publish position (0x002FB2D0) }   // 0x00319739-0x00319775
// states 2..6: the blink
if (now >= stamp - step * (60 - (7 - state))) { state += 1; 0x0028F000(handle, 2, &(7 - oldState)) }  // 0x003196E9-0x00319732
// state 7: expiry
if (now >= stamp - step * 60) { unlink; 0x0028F000(handle, 4, ...); 0x002FB2A0(slot); zero }         // 0x00319664-0x003196E1
```

The landing position comes from `0x0028EFC0(handle, out)` (`0x0031975E`), which forwards to the world-object part,
`0x003FA6E0([0x0209BE80] + 0x57E0, handle, out)`, before `0x002FB2D0` publishes it.

The comparisons are unsigned (`jc` at `0x00319718` and `0x00319682`). With the scalar at 1.0 the
thresholds are:

| State | Fires at | Presentation call |
|---|---|---|
| 2 to 3 | stamp + 1650 | `0x0028F000(handle, 2, 5)` |
| 3 to 4 | stamp + 1680 | `0x0028F000(handle, 2, 4)` |
| 4 to 5 | stamp + 1710 | `0x0028F000(handle, 2, 3)` |
| 5 to 6 | stamp + 1740 | `0x0028F000(handle, 2, 2)` |
| 6 to 7 | stamp + 1770 | `0x0028F000(handle, 2, 1)` |
| 7, removed | stamp + 1800 | `0x0028F000(handle, 4, ...)` |

The frame counter `0x0208D45C` is incremented by `0x0032A100` (`0x0032A135`, called from `0x00234590` at
`0x002345CA`) only in a frame where the battle clock `0x003EBA90(0)` changed since the previous frame
(`0x022C317C`). It is reset to 0 by `0x0032A160` from the battle-state reset `0x00237DF0` (`0x00237E37`).

The scalar `0x01DFE0B8` is 1.0 in the image and becomes 2.0 at `0x001EDDD8` together with the 60 fps
gate `0x01F82E38` = 1 (`0x001EDDE8`). The lifetime is therefore 1800 frames at the base rate and 3600
at 60 fps: one minute either way at the 30 fps base (see the
[game settings page](../Saving-Loading-And-Settings/game-settings.md)).

### Collection on contact

The periodic unit maintenance `0x00310DB0` runs the contact test for a unit that is the controlled
character (its handle `+0x08` equals the focus `0x022C7FE0`, `0x003273B0` at `0x003110DC`) or whose
action word `+0x714` is `0x4165` (`0x003110E8`-`0x003110F4`):

1. `0x002FB150(unit, 1.0)` returns the first presence record, in slot order, whose XZ distance
   (`0x004686D0`) from the unit's actor position is strictly below `max(r1, r2) + 1.0`, with the
   radii from `0x00265090`; -1 when none (`0x00311105`-`0x0031110E`).
2. `0x00469E30(stats)` posts message `0x4E` through `0x0046AB10` when `0x002F8E90()` returns 8
   (`0x0031111B`).
3. A party record (stats byte `+0x05` = 0) collects it: `0x00319A00(slot, unit handle)`
   (`0x00311141`). Any other record, or no record, destroys it: `0x00319830(slot, unit handle)`
   (`0x00311284`).
4. For a party record the tick then rolls the chain bonus (see [Loot drops](loot-drops.md)).

`0x00319920(slot, handle)`, the collect, grants every entry whose id is not `0xFFFF` with
`0x00300B80(id, count, 1)`, the inventory add with the notification flag (`0x00319950`-`0x00319972`),
adds 1 to the pickup counter `0x022C3174` (`0x00319974`), unlinks the slot, posts op 3 with the
collecting unit's handle, clears the presence record and zeroes state, stamp, links and handle
(`0x0031997A`-`0x003199E8`). `0x003197B0` is the same retirement without the grants and the counter.

### The nearest pickup

`0x00319850(unit, &out)` walks the live list and, through `0x002FB310(slot, &pos)`, takes the present
position with the smallest squared XZ distance (`0x003A1960`) from the unit's position `+0xE0`; the
ceiling starts at `0x02F973B8`, which `0x002368D0` sets to +inf (`0x00914700`, `0x002368F0`). It returns
the slot, or -1 when none is present. Its one caller is the movement goal decoder `0x00312730`
(`0x003129AF`): goal `0x4165` becomes the nearest pickup's position with a stop distance of
`(max(r1, r2) + 1.0) - 0.1`, computed in that order.

### The presence table

Ten records of `0x20` bytes at `0x022BE7F0` tell the contact and nearest tests where the live
pickups are. `0x002FB2D0(slot, &pos)` publishes a position (returns -1 for a slot above 9, -2 when
the record is already present, else 1), `0x002FB2A0(slot)` clears it, `0x002FB310(slot, &pos)` reads
it, and `0x002FB250` clears all ten.

### The pickup object

`0x0028F000(handle, op, arg)` drives the HUD world-object manager at `[0x0209BE80] + 0x57E0` and does
nothing when `0x0209BE80` is 0:

| Op | Effect | Function |
|---|---|---|
| 1 | create from the descriptor; returns the element address as the handle | `0x003FA160` |
| 2 | blink step with the remaining count 5..1 | `0x003FAA10` |
| 3 | collected by the unit in the argument | `0x003FA820(handle, unit)` |
| 4 | expired | `0x003FA820(handle, 0)` |
| 5 | evicted | `0x003FA820(handle, 0)` |
| 6 | end every element | `0x003FA900` |

`0x003FA160` takes the first free of 13 elements of `0x2A0` bytes at manager `+0x270` (free when
`+0x272` bit `0x1` is clear) and fills it:

- state `+0x260` = 1, fall speed `+0x264` = -0.25, appearance `+0x268`, chain level `+0x26C`;
- start position `+0x00` = the descriptor's position, rest position `+0x10` = its x and z with the
  ground height from `0x0026E350`; both y values + 0.5;
- linked at the end of the manager's list `+0x2490`; sound `0x50` (`0x00249C60`).

It returns the element, or 0 when all 13 are in use. The handle is the element's address kept in a
dword (`0x00319E05`), and `0x003FA730` reads `[handle+0x272]` before any null test.

The element update `0x003FC510` runs the element through its states:

- State 1: the element moves toward its rest height each frame, its speed `+0x264` growing by
  `0.02 × 0x01DFE0BC` per frame, and becomes state 2 on a later frame when the rest height lies
  between the old and new y, or when y already equals it (`0x003FC839`, `0x003FC8D5`). `0x0028EFE0`
  (`0x003FA730`) reports that state to the lifetime walk.
- Op 2 sets the fade step `+0x288` from the table `{4096, 2730.67, 2048, 1638.4, 1365.33, 1170.29}
  × 0x01DFE0BC` indexed by the remaining count, so each blink is faster than the last. `0x01DFE0BC` is
  1.0 in the image and 0.5 at 60 fps (`0x001EDDE0`), which halves the per-frame step.
- Op 3 marks the element collected, sets a phase from `sin(0x0208F570 × π / 30)` and plays sound
  `0x46` when a unit is given. The update then shrinks the element (state 3) and sets its state to
  0 when its scale `+0x270` has reached 0.

## Layouts

`LootPickupSlot` (`0x60` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | slot | 0-9, the index into the presence table; written by `0x00319B10` |
| `+0x04` | `i32` | state | 0 free, 1 falling, 2 landed, 3-6 blinking, 7 last blink; `0x00319CA0`, `0x00319600` |
| `+0x08` | `u32` | stamp | frame counter `0x0208D45C` when the pickup landed; `0x00319600` |
| `+0x0C` | `u8[4]` | pad | read and written by none of the five pool functions (the stamp store `0x00319754` is a dword); nothing fixes its width |
| `+0x10` | `u64` | prev | pointer to the previous live pickup; `0x00319CA0`, `0x00319600`, `0x00319920`, `0x003197B0` |
| `+0x18` | `u64` | next | pointer to the next live pickup; same writers |
| `+0x20` | `u8[56]` | drops | seven entries {u16 item, u16 pad, i32 count}, `0xFFFF` = empty; copied by `0x00319CA0` |
| `+0x58` | `u32` | handle | the pickup object; `0x00319CA0` |
| `+0x5C` | `u8[4]` | tail | read and written by none of the five pool functions (`0x00319B10`, `0x00319CA0`, `0x00319600`, `0x00319920`, `0x003197B0`); nothing fixes its width |

`LootPresenceRecord` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | present | 1 when a position is published; `0x002FB2D0`, `0x002FB2A0`, `0x002FB250` |
| `+0x01` | `u8[15]` | pad | not written by the four presence functions |
| `+0x10` | `f32[4]` | position | x, y, z, 1.0; `0x002FB2D0` |

`LootPickupDescriptor` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | position | x, y, z, 1.0; `0x00319CA0` |
| `+0x10` | `i32` | look | `0x00319A20` result, 0-2 |
| `+0x14` | `i32` | level | chain level 0-3 through `0x01EED3A8` |

### The drop entry

Each of the seven entries at `+0x20` of a pickup slot is 8 bytes.

`LootDropEntry` (`0x8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | itemId | the granted item id; `0xFFFF` marks the slot empty and skips it without ending the walk |
| `+0x02` | `u8[2]` | pad02 | copied with the seven entries by the pickup's creation (the 16-byte and 8-byte copies at `0x00319D78`-`0x00319D91` in `0x00319CA0`); read by no instruction; nothing fixes its width |
| `+0x04` | `u32` | quantity | how many of the item to grant; passed to the grant call in edx |

## Operations

| Function | Role |
|---|---|
| `0x00319490(&pos)` | placement test for a drop position; returns `0x003377C0`'s result |
| `0x00319CA0(&drops, &pos)` | create a pickup, evicting the oldest when the pool is full |
| `0x00319600()` | per-frame lifetime: landing, five blink steps, expiry |
| `0x00319A00(slot, handle)` / `0x00319920` | collect: grant the entries, count the pickup, retire the slot |
| `0x00319830(slot, handle)` / `0x003197B0` | retire the slot without grants |
| `0x00319B10()` | reset the pool and the presence table |
| `0x00319A20(&drops)` | appearance value (0, 1 or 2) from the equipment classes inside |
| `0x002FB150(unit, extra)` | first presence record within the unit's radius plus `extra` |
| `0x00319850(unit, &out)` | nearest present pickup, no radius |
| `0x002FB2D0` / `0x002FB2A0` / `0x002FB310` / `0x002FB250` | publish, clear, read, clear all presence records |
| `0x0028F000(handle, op, &arg)` | presentation ops 1-6 |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `0x02EC0FA0` | 10 × `0x60` | the pickup slots | `0x00319B10`, `0x00319CA0`, `0x00319600`, `0x00319920`, `0x003197B0` |
| `0x02EC1360` / `0x02EC1368` | `void*` | live-list head and tail | the same five |
| `0x022BE7F0` | 10 × `0x20` | presence records | `0x002FB2D0`, `0x002FB2A0`, `0x002FB250` |
| `0x0208D45C` | `u32` | frame counter, advances only while the battle clock runs | `0x0032A100`, reset by `0x0032A160` |
| `0x022C3174` | `i32` | pickups collected since the last chain level rise | `0x00319920`; reset on a rise (`0x003184EC`) and by `0x003183A0` |
| `0x02F973B8` | `f32` | +inf, the search ceiling | `0x002368D0` (`0x002368F0`) |

The pool reset `0x00319B10` and the presence clear `0x002FB250` are unrolled, so they write every slot and every record at
a fixed address. Slot n starts at `0x02EC0FA0` + n × `0x60`; the slot functions `0x00319A00` and `0x00319830` form the same
address from a sign-extended index (`0x00319A00`-`0x00319A12`, `0x00319830`-`0x00319842`). The slot fields at their fixed
addresses:

| Slot | `+0x00` slot number | `+0x04` state | `+0x10` prev | `+0x18` next | `+0x58` handle |
|---|---|---|---|---|---|
| 0 | `0x02EC0FA0` | `0x02EC0FA4` | `0x02EC0FB0` | `0x02EC0FB8` | `0x02EC0FF8` |
| 1 | `0x02EC1000` | `0x02EC1004` | `0x02EC1010` | `0x02EC1018` | `0x02EC1058` |
| 2 | `0x02EC1060` | `0x02EC1064` | `0x02EC1070` | `0x02EC1078` | `0x02EC10B8` |
| 3 | `0x02EC10C0` | `0x02EC10C4` | `0x02EC10D0` | `0x02EC10D8` | `0x02EC1118` |
| 4 | `0x02EC1120` | `0x02EC1124` | `0x02EC1130` | `0x02EC1138` | `0x02EC1178` |
| 5 | `0x02EC1180` | `0x02EC1184` | `0x02EC1190` | `0x02EC1198` | `0x02EC11D8` |
| 6 | `0x02EC11E0` | `0x02EC11E4` | `0x02EC11F0` | `0x02EC11F8` | `0x02EC1238` |
| 7 | `0x02EC1240` | `0x02EC1244` | `0x02EC1250` | `0x02EC1258` | `0x02EC1298` |
| 8 | `0x02EC12A0` | `0x02EC12A4` | `0x02EC12B0` | `0x02EC12B8` | `0x02EC12F8` |
| 9 | `0x02EC1300` | `0x02EC1304` | `0x02EC1310` | `0x02EC1318` | `0x02EC1358` |

Every field is 0 at load, since the pool lies in the zero-filled tail of `.data`. The writers and readers of each
field, the same for all ten slots:

| Field offset | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `+0x00` | `i32` | 0 | the slot's own number n, passed to the presence functions | `0x00319B10`: n for slots 1-9 (`0x00319B12`, `0x00319C3E`-`0x00319C84`), 0 for slot 0 (`0x00319B45`) | `0x00319CA0` (`0x00319D29`), `0x00319600` (`0x003196CE`, `0x0031976D`), `0x00319920` (`0x003199C4`), `0x003197B0` (`0x00319803`), `0x00319850` (`0x00319890`; returned from `0x003198E6`) |
| `+0x04` | `i32` | 0 | the state, 0 free to 7 last blink | `0x00319B10`, 0; `0x00319CA0`, 1 (`0x00319D96`) and 0 on eviction (`0x00319D30`); `0x00319600`, 2 on landing (`0x00319757`), state + 1 per blink (`0x0031972F`), 0 on expiry (`0x003196D5`); `0x00319920`, 0 (`0x003199DC`); `0x003197B0`, 0 (`0x0031980C`). Every 0 is a qword store that also clears the stamp at `+0x08` | `0x00319CA0` (`0x00319CC5`, equal to 0 means free); `0x00319600` (`0x00319640`; signed compares with 1, 6 and 7 at `0x00319643`-`0x0031965E`) |
| `+0x10` | `void*` | 0 | the previous live slot | `0x00319B10`, 0; `0x00319CA0` (`0x00319D0A` on the next slot, `0x00319D38`, `0x00319D56`, `0x00319D63`); `0x00319600` (`0x003196AF`, `0x003196DD`); `0x00319920` (`0x003199A1`, `0x003199E4`); `0x003197B0` (`0x003197E0`, `0x00319814`) | `0x00319CA0` (`0x00319CE3`, `0x00319D01`), `0x00319600` (`0x00319688`, `0x003196A6`), `0x00319920` (`0x0031997A`, `0x00319998`), `0x003197B0` (`0x003197B9`, `0x003197D7`) |
| `+0x18` | `void*` | 0 | the next live slot | `0x00319B10`, 0; `0x00319CA0` (`0x00319CF0` on the previous slot, `0x00319D34`, `0x00319D4B`, `0x00319D71`); `0x00319600` (`0x00319695`, `0x003196D9`); `0x00319920` (`0x00319987`, `0x003199E0`); `0x003197B0` (`0x003197C6`, `0x00319810`) | `0x00319CA0` (`0x00319CE7`, `0x00319CFD`), `0x00319600` (`0x0031968C`, `0x003196A2`, `0x0031977A`), `0x00319920` (`0x0031997E`, `0x00319994`), `0x003197B0` (`0x003197BD`, `0x003197D3`), `0x00319850` (`0x003198E8`) |
| `+0x58` | `u32` | 0 | the pickup object's handle | `0x00319B10`, 0; `0x00319CA0`, the op 1 result (`0x00319E05`) and 0 on eviction (`0x00319D3C`); `0x00319600`, 0 (`0x003196E1`); `0x00319920`, 0 (`0x003199E8`); `0x003197B0`, 0 (`0x00319818`) | `0x00319CA0` (`0x00319D17`), `0x00319600` (`0x003196BC`, `0x0031971A`, `0x00319739`, `0x00319751`), `0x00319920` (`0x003199AE`), `0x003197B0` (`0x003197ED`) |

Presence record n starts at `0x022BE7F0` + n × `0x20`. Its present byte for records 1-9 lies at `0x022BE810`, `0x022BE830`,
`0x022BE850`, `0x022BE870`, `0x022BE890`, `0x022BE8B0`, `0x022BE8D0`, `0x022BE8F0` and `0x022BE910`:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022BE810` to `0x022BE910`, step `0x20` | `u8` | 0 (zero-filled tail) | 1 while record n holds a published pickup position | `0x002FB250`, 0 (`0x002FB257`-`0x002FB28F`); `0x002FB2D0`, 1 (`0x002FB2F8`); `0x002FB2A0`, 0 (`0x002FB2B3`) | `0x002FB2D0` (`0x002FB2E3`, equal to 1 refuses the publish); `0x002FB310` (`0x002FB31E`, 0 returns no position); `0x002FB150` (`0x002FB1E0`, walking records 0-9 with a signed count at `0x002FB214`) |

`0x002FB2D0` and `0x002FB2A0` refuse a record number above 9 with an unsigned compare (`0x002FB2D3`, `0x002FB2A3`), so a
negative number is refused as well. `0x002FB310` takes the number without a bound.

## Modding notes

- Ten is a literal: the scan bound in `0x00319CA0` (`0x00319CD0`) and the slot numbering in `0x00319B10`
  must change together, with a larger array at `0x02EC0FA0`.
- The lifetime is the `60` and the `-30.0` in `0x00319600`; the scalar `0x01DFE0B8` is the global
  frame-rate scalar and changes every timed system at once.
- A drop buffer must hold seven entries with `0xFFFF` in every unused one; an unset middle entry is
  granted.
- The appearance value is computed once at creation.
- Eviction is silent: the evicted pickup gets op 5, which runs the same `0x003FA820(handle, 0)` as
  expiry's op 4.

## Related

- [Kill rewards: what an enemy's death triggers, when it gives nothing, and the order of chain, EXP, LP, gil, loot and counters](kill-rewards.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](loot-drops.md)
- [Kill chain: chain count, chain level, the chain coin and resets](kill-chain.md)
