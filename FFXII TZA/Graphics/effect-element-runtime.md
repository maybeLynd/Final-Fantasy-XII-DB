---
title: "Effect element runtime: instances, emitters and elements, the per-step update, birth, release and child spawns, and the six display layers"
kind: "system"
category: "Graphics"
addresses: "0x0024B270, 0x020910F0, 0x02F97348, 0x02EBEF88, 0x0024ED80, 0x00258D70, 0x0024B9B0, 0x003A7050, 0x003A8390, 0x0043EF40, 0x00441B30, 0x002F3BC0, 0x002F2D60, 0x002F3910, 0x002F2530, 0x002F4020, 0x005004C0, 0x002F31C0, 0x005002E0, 0x003A8950, 0x003A8AE0, 0x00258EE0, 0x00259030, 0x0024D370, 0x0024D4E0, 0x00441970, 0x02AEE910, 0x02F8F2F8, 0x02F8F2C6, 0x003A3740, 0x003A3A00, 0x0024D540"
---

## What the player sees

A spell effect is a crowd of small pieces: sparks, streaks, sprites, rings, meshes, lights. Each
piece is an element. Elements are born in bursts at set intervals, move and change colour as their
authored tracks say, spawn further pieces while they live or as they die, and disappear when their
lifetime runs out or they leave their visibility window. They are drawn in six passes at fixed
points of the frame, so some effects sit behind characters and others in front of the menu.

## How it works

### Instances, emitters and elements

The parsed data lives in an effect context, which is on the
[resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) page; its
records are on [effect files](effect-files-efx-efb.md). Running it takes three levels:

- An effect instance, `0x3B0` bytes made by `0x0024B270(template)` from a template. Its byte `+0` is
  its kind; it is linked at the head of `0x020910F0[kind]` through `+0x348` / `+0x350`, stamped with
  `0x00181DD0()` at `+0x3A8`, and made current (`0x0024B270`–`0x0024B385`).
- An emitter, on the list whose block is the instance's `+0x1B8` (first node at `+8`, next at
  node `+8`). Its `+0x100` is an `0x800` emitter record and its `+0x108` an `0xA00` element
  definition.
- An element, on its emitter's active list (head `+0x118`, tail `+0x128`, element links `+0x28`
  back and `+0x30` forward) or free list `+0x120`.

### Making an instance current

`0x0024ED80(instance)` publishes the instance at `0x02F97348` and its context (`+0x340`) at
`0x02F97340`, then the context's record tables and the instance's lists: `0x02EBEF70` = context
`+0x18` (the `0xB00` record store), `0x02EBEFA8` = `+0x38`, `0x02EBEFA0` = `+0x840`, `0x02EBEF90` = `+0x848`
(emitter records), `0x02EBEF78` = `+0x850` (definitions), `0x02EBEF98` = instance `+0x120`, `0x02EBEFB0` =
`+0x130` and `0x02EBEF88` = `+0x1B8` (`0x0024ED80`–`0x0024EDFF`).

It then tail-jumps to `0x0024FCF0` (`0x0024EDFF`), which publishes the instance's draw state:
byte `+3` at `0x02096800`, the colour `+0x320` scaled by `+0x39C` with alpha 1.0 at `0x02096810`, `+0x310` at
`0x02096820` (zero when `+0x378` has bit `0x800`), `+0x300` at `0x02096830`, `+0x330` at `0x02096840` and the depth
offset `+0x338` at `0x02AEE7F4` (`0x0024FD05`-`0x0024FD86`; [menu effects](menu-effects.md)). All the code below
reads these globals.

### The element pool

`0x0043F450(emitter, record, definition, …)` resets the emitter with `0x0043F210`, which frees its old
pool `+0x110` and clears its counters, lists and flags (byte `+0x138` keeps bits 0–1 set and bit 2
clear). It then allocates one block of `+0x20` elements, the count from emitter-record word
`+0x2B2`, links them into the free list `+0x120` and stamps each with the definition's type.

The element size depends on the type. `0x0043F450` handles the main range with `0x0036A230`; its
default arm passes the sub-range types to `0x004FF440`, which uses `0x0036A190` and returns 1 for a type
it does not know (`0x004FF440`):

| Sub-range type | Element bytes |
|---|---|
| `0x42`, `0xA4`, `0xA7`, `0xAA` | `0x240` |
| `0xA6`, `0xA8`, `0xA9` | `0x260` |
| `0xAB` | `0x2B0` |
| `0xA3` | `0x2C0` |
| `0x70` | `0x310` |
| `0x6A` | `0x320` |
| `0x73` | `0x3B0` |
| `0x6B` | `0x3E0` |
| `0x72`, `0x74` | `0x400` |
| `0x71` | `0x440` |
| `0x68` | `0x4D0` |
| `0x69` | `0xAD0` |

### The update pass

In the field frame, each simulation step runs `0x00258D70` ([frame update
order](../Engine-Core/frame-update-order.md)). It calls `0x0024B9B0(0, kind)` for kind 2
when a map bank is loaded (`0x00258DC7` → `0x0026F9D0`), then for the kinds 3, 5, 6, 9, 1, 7 and 4 in
that order (`0x00258DCC`–`0x00258E0C`); the menu frame's `0x00258E40` runs kind 3 alone.

`0x0024B9B0`
refuses kind 8, walks `0x020910F0[kind]` through `+0x348`, skips an instance whose `+0x3A8` differs
from `0x00181DD0()`, makes each current (`0x0024BB6D`) and updates it through `0x003A7050`
(`0x0024B9C8`, `0x0024BA12`–`0x0024BA65`, `0x0024BC16`, `0x0024BE28`).

### Starting and ending an instance

The instance's state byte `+0x370` picks what `0x0024B9B0` does with it after making it current:

- 2 and 8 start it with `0x003A74F0(+0x373)` and set state 1.
- 1 runs `0x003A7EE0` and then the update `0x003A7050`; when the update returns 0 the instance ends
  through `0x003A7300`. On steps where the pass holds the instance, state 1 runs only `0x003A7EE0` and
  `0x003A93F0`.
- 6 runs like 1 but moves to 4 when the update returns 0, and 4 starts the instance again with
  `0x003A74F0`.

The states that update the instance, and the group draw, first rebuild the effect matrices with
`0x0024C060`. One step of it is `0x0039D480(view)`, with the view `0x02AEDEF0`, or `0x02AEE9E0` in a kind-4
instance: it keeps the 64 bytes at `0x02AEEAA0`, turns the unit z vector by the view's rotation
(`0x0039AF70`, `0x00398F90`), and writes at `0x02AEEAE0` a single-axis rotation (`0x00398910`) by the
`atan2` of the result's x and z, which `0x0024C060` folds into `0x02AEEC70` (`0x00397910`).

`0x003A74F0(index)` releases every emitter (`0x003A9160`) and every `0x700` object (`0x003A81E0`), zeroes
the counters `+0x80` and `+0x84` of the block at `0x02EBEFB0`, frees its players (`0x003A7360`) and runs
the record store's kind-`0x59` (`'Y'`) nodes through `0x005043F0` (`0x003AA430`). It then attaches a
player for the `0x600` record `index`, or for index 1 the first record that exists
(`0x003A7460`), and starts every attached player with `0x003337B0`.

The block at `0x02EBEFB0` (instance `+0x130`) holds 16 player pointers, which `0x003A72A0` clears with
the counters when an instance is made. `0x003A7460(index)` takes a `0x2A0`-byte player for the
`0x600` record `index` into the first free pointer and initialises it with `0x00333030`.

`0x003A7360` tears each player down (`0x00333350`) and frees it, then, by the instance's flags, calls
`0x0024C6B0` (`+0x368` bit `0x80`), `0x0024C870` (`+0x368` bit `0x100`) and `0x003AF330(0)` (`+0x3A0` bit 0,
which it clears). `0x003A7300` is `0x003A7360` followed by a call to `0x002FCB60` for each non-zero dword
at `+0x110`–`+0x11C`, which it then clears; `0x003A7420` passes every player to `0x00332FA0`.

### The free list

An owner table that lets go of a running instance does not free it at once. `0x0024EE10(instance)`
unlinks it from its kind list `0x020910F0[kind]` and `0x0024B1F0(instance)` pushes it on the free list
`0x02092170` through `+0x348` and `+0x350`. The loaded-file queue (`0x003B1310`, `0x003B1710`, `0x003B18E0`)
and the kind-1 handles (`0x002FC3C0`) do this for an entry in state 6 and set state 7.
`0x0024C3C0(kind, keep)` moves every instance of a kind except `keep` onto the list; the battle
effect program `0x003B8670` calls it with kind 7 and the current instance (opcode `0x21`).

`0x0024B4F0`, from the field frame `0x0022A770` and the menu frames `0x0022B8C0` and `0x0022BC20`, frees the
blocks queued at `0x02091150` (count `0x02092168`), releases the render targets queued at `0x02091950`
(count `0x0209216A`, `0x00182CA0`) and then drains the free list with `0x0024B580`:

- a kind-1 instance goes back on the list while `0x002FC010` returns 0; that function first counts
  the instance's byte `+0x37B` down to 0;
- an instance of kind 5, 6 or 9 leaves the numbered requests (`0x003B0220`), one of kind 7 the
  loaded-file queue (`0x003B15C0`) and one of kind 4 the menu registry (`0x003B2930`);
- every drained instance then releases its path objects, players and emitters (`0x003A81E0`,
  `0x003A7360`, `0x003A9160`), queues its render target `+0x380` at `0x02091950` (freed at once when 256
  are queued) and frees its block (`0x003697F0`).

`0x0024EE60(instance)` is the immediate form: when the instance is on its kind list it unlinks it
and frees it the same way through `0x0024EEE0`.

### Emptying a group

`0x0024C550(kind)` first clears the kind's owner table: `0x002FBEF0` for kind 1, `0x003B0130` for kinds 5,
6 and 9, `0x003B1310` for kind 7 and `0x00374930` for kind 8, the screen-effect pool of
[screen fades](screen-fades.md). It then frees every context on `0x020910A0[kind]` (`0x0024F410`) and
every instance on `0x020910F0[kind]` (`0x0024C460`). Its callers are `0x0026FB90`, `0x0026FF50`, `0x003B29B0`,
`0x003B2B40` and `0x003B3160`.

- `0x002FBEF0`, with arena 8 selected, moves every handle on the kind-1 used list `0x02EC3D60` to the
  free list `0x02EC3D70`, keeps bits 0–5 and 28–31 of its id, clears its `+0x10` and `+0x14`, zeroes
  `0x02EC3D78` and `0x02EC3D7C`, and frees the kind-1 instances (`0x0024C460(1)`).
- `0x003B0130` frees the instances of kinds 5, 6 and 9 and clears the handle and instance pointer of all
  36 numbered requests.
- `0x003B1310` walks the loaded files as `0x003B18E0` treats one (below), without sparing kept entries,
  and then frees the kind-7 instances.

### The effect teardown

`0x0024E910` ends what a field holds. The area unload `0x002628B0` and the title-return reset `0x003601D0`
call it:

1. `0x002FBEF0`; then every kind-1 context (`0x020910A8`, `0x0024F410`) and instance is freed;
2. `0x0026FF50`, the disposal of the map effect bank;
3. `0x003B2F90` moves every used model-effect slot (`0x02EBDB98`) to the free list `0x02EBDBA0`, ending
   its instance (`0x0024EE60`) and keeping bits 0–5 and 28–31 of its id, and frees the kind-3 instances;
4. `0x003B0130`, then `0x003B26D0`, which releases every loaded file whose flag `+0x20` bit 0 is clear
   (`0x003B18E0`);
5. `0x3FF` goes to the group mask `0x02092160`, and bit `0x2` of `+0x368` is cleared in the instance of
   every model-effect slot (`0x003B3B50`) and of every numbered request (`0x003B1130`);
6. `0x02EBEF68` bit 0, bits `0x400` and `0x800` of `0x020926E4`, the low three bits of `0x02F8F29E` and bit 0
   of `0x02EBDBBC` are cleared, and `0x003AF330(0)` runs;
7. with `0x020926E4` bit `0x40` set it drops the bit and queues the target `0x020926D0` for release;
   last come the motion blur clear `0x0024EB20` and the cut-in clear `0x0024CEB0`.

Bit `0x2` of `+0x368` holds an instance: on such a step `0x0024B9B0` runs only `0x003A7EE0` and
`0x003A93F0` for it. The time stop sets it on the instances whose owner is a stopped actor
(`0x003B3BA0`, `0x003B1180`, through `0x0024FCA0`), and `0x0024FC80` releases them all with step 5 alone.

### Keeping the path objects

The instance's path-object list at `0x02EBEF98` (head `+0`, tail `+8`, links `+0xE8` back and `+0xF0`
forward) is emptied by `0x003A8000` when an instance is made; `0x003A81E0` frees every object, and
`0x003A8130(key, byte)` frees every object with that key and byte. `0x003A7EE0(dt)` clears bit 0 of
every object's byte `+0x103`, then runs the step `0x004FF0D0(object, dt)` on each object whose bit is
still clear.

### Emitter bookkeeping

The emitter block (instance `+0x1B8`, published at `0x02EBEF88`) keeps, from `+0x18`, 32 use counts of
8 bytes, ended by an id of −1:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | id (an emitter's +0x1C; -1 ends the table) |  |
| `+0x04` | `u8` | kind (an emitter's +0x13B) |  |
| `+0x05` | `u8` | bit 0: release pending |  |
| `+0x06` | `u16` | emitters using it |  |

- `0x003A8900` resets the block: the frame stamp and both list ends to 0 and all 32 ids to −1.
- `0x003A8340(id, kind)`, from the emitter maker `0x003A8AE0`, adds one to a matching entry or fills the
  first free one with a count of 1.
- `0x003A9070(id, kind)` removes a matching entry whose count is 0 and closes the gap, returning 0;
  with a count left it sets the pending bit and returns 1. No match returns 1.
- `0x003A87B0(tag)` releases every emitter whose byte `+0x13A` equals the tag, and `0x003A9160` every
  emitter. Each emitter is unlinked, its `+0x110` object handed to `0x003A92D0` and freed, and its use
  count lowered; when a pending entry reaches 0 it is removed and the path objects with the
  emitter's id and kind are freed (`0x003A8130`).

The stop byte `+0x139` has four writers: `0x003A8C80` sets it on every emitter, `0x003A8CB0(n)` on
emitters whose byte `+0x1C` is not `n`, and `0x003A8D40(tag)` on emitters whose `+0x13A` is the tag;
`0x003A8FC0(tag)` returns whether any emitter has the tag. `0x003A8CE0(n)` sets bit 0 of `+0x248` on
every element of the emitters whose `+0x1C` is not `n` and whose definition type is `0x40`.

### The record store's other fronts

The store at `0x02EBEF70` (context `+0x18`) is a list of nodes linked through encoded dwords
(`0x0020E600`): head `+0`, tail `+8`, a list of extra blocks at `+0x10`, and two words at `+0x18` and
`+0x1A`, all of which `0x003A9CC0` zeroes. `0x003AA1F0(key, kind)` returns the first node with that key
word `+0xC` and kind byte `+0xE`, and `0x003AA240(node)` the next node with the same pair.

`0x003AA2E0(key)` runs once per context: when the word `+0x1A` is clear it calls `0x005011B0` for each
kind-`0x52` (`'R'`) node and `0x00501610` for each kind-`0x53` (`'S'`) node of the key, frees the extra
blocks and sets `+0x1A`. It returns 0 when one of those calls returned 0.

Below, "the half-rate cadence" means the cadence test `0x001EDDA0` returning 0
([global state accessors](../Engine-Core/global-state-accessors.md)). `0x003A8390(dt)`
adds 2 to the instance's frame stamp, the first dword of its `+0x1B8` block, or `2 / [0x01DFE0B4]` in
the half-rate cadence (`0x003A839E`–`0x003A83BB`). It then calls
`0x0043EF40(emitter, dt)` for each emitter, with the emitter published at `0x02EBEF80` (`0x003A83E0`).

### The emitter step

`0x0043EF40` returns 0 when the emitter has no emitter record (`0x0043EF8B`). Otherwise it updates every
element on its active list through `0x002F3910(element, emitter, dt)` (`0x0043EF9B`–`0x0043EFC5`). It
then stops emitting when byte `+0x139` is set or its age `+0x2C` has reached a non-zero limit
`+0x28` (`0x0043EFC7`–`0x0043EFEB`), and returns whether elements remain.

An emitting emitter adds `dt` to `+0x2C` and keeps the whole frame in `+0x30`. A top-level emitter
(no parent element at `+0x130`) fires when the integer track at emitter record `+0x10`, evaluated
at that frame, is no more than the time since its last firing `+0x34`. In the half-rate cadence it
fires on even frames only. A firing births as many elements as the integer track at record `+0`
gives, each through `0x00441B30(emitter, age, 0)` (`0x0043F180`–`0x0043F1E4`). The tracks are
[authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md).

### Birth

`0x00441B30(emitter, age, parent)` needs an emitter record and a free element (`0x00441B5C`–`0x00441B6D`).
It places the next element through `0x00442170`, which dispatches on the emitter record's subtype
byte `+0x282` (0 to 8, `0x0044218A`–`0x004421B1`), counts the birth in `+0x24`, and takes the head of
the free list (`0x00441BE1`–`0x00441C0D`).

When the record's byte `+0x2C4` has bits 0–1 equal to 2 a coin
(`0x003A6E60(2)`) can put the element at the tail; otherwise it goes to the head (`0x00441C14`–`0x00441C9F`).
It samples the record's spawn tracks into the emitter (`+0xA0`–`+0xF0`) and calls the birth
dispatcher `0x002F3BC0(element, emitter, age)` (`0x00441CA6`–`0x00441E71`).

`0x002F3BC0` bounds the element's type byte at `0xD1` and calls the type's birth method; every birth
method except type `0x70`'s calls the base birth `0x002F2D60`. Afterwards, unless `0x00314960()` is 0 or the cadence
test returns non-zero, it adds 1.0 to the age `+0x3C`; it stores `0x00250000()` at `+0x224` and clears
`+0x226` (`0x002F3E3F`–`0x002F3E73`).

`0x002F2D60` sets `+0x18` to the emitter record and `+0x20` to the definition, returning 0 when either
is missing (`0x002F2D6F`–`0x002F2DA2`). It clears bits 1 and 2 of `+1`, sets `+8` to the emitter and
`+0x10` to 0, copies the emitter's position, and reads the lifetime `+0x4C` from the integer track
at record `+0x20` (`0x002F2DA4`–`0x002F3029`).

It then copies the sampled spawn values, and the colour `+0x1F0` from the emitter's `+0xF0` when
definition byte `+0x49` has bit `0x2` (else `0x80808080`). It zeroes the age `+0x3C` / `+0x40` and
the update count `+0x48`, copies the definition's type byte `+0x44` into the element's byte `+0`,
marks the eight spawn slots unfired (`+0x1D0`–`+0x1EF` = −1) and stamps `+0x38` with the
instance's frame stamp (`0x002F302C`–`0x002F315B`). A type-0 definition fires its spawn slots with
trigger 1 here (`0x002F317A`–`0x002F3188`).

### The update

`0x002F3910(element, emitter, dt)` bounds the type at `0xD1` and jumps to the type's update method
(`0x002F3910`–`0x002F3939`); type 0's is the base `0x002F2530` itself (`0x002F393C`), and every other
update except type `0x70`'s calls the base, most of them followed by a type tail. The base (`0x002F2530`):

1. While `+0x224` is set and `0x00250000()` is 0, clears it and stops unless the cadence test
   returns non-zero (`0x002F2550`–`0x002F2572`).
2. Returns 0 when `+0x38` equals the frame stamp, so an element updates at most once per stamp
   and not on the step of its birth; otherwise adds `dt` to `+0x3C` (`0x002F2574`–`0x002F2587`).
3. In the half-rate cadence, types `0x67`, `0x68`, `0x6A`, `0x6B`, `0x71`, `0x73` and `0x74` (bit
   set `0x341B` from `0x67`) skip steps whose whole age is odd (`0x002F258C`–`0x002F25B0`).
4. With a lifetime set, once the whole age with bit 0 cleared exceeds it, fires the spawn slots with
   trigger 3, releases the element and returns 0 (`0x002F25B2`–`0x002F25DD`).
5. Computes `n` = whole age minus `+0x44`; returns 0 when `n` is not positive. Otherwise counts the
   update in `+0x48`, stores the whole age in `+0x40`, and sets `+0x44` to the whole age, or to its
   remainder by definition word `+0x40` when definition byte `+0x47` is set (`0x002F25E4`–`0x002F262A`).
6. Returns `n` at once for a definition type of `0xA0` or more; otherwise goes on to sample the
   definition's motion tracks at `+0x44` (`0x002F262D`–`0x002F263C`).

Before the base fires an element's spawn slots with trigger 2 or 3 (`0x003A8950`), it runs
`0x002F3890(element)`: the colour `+0x1F0` is copied to `+0x1F4`, the world position `+0x70` moves
to `+0x80`, and the position `+0x60` becomes the new `+0x70`, turned through the parent's matrix
(`0x0039AF70`, `0x00398F90`) when `+0x10` is set. The children therefore start from where the element
is on that step.

In 60 fps mode (`0x001EDDA0()` returns 0) the base ends by asking `0x001EDBB0(whole age, kind, effect
number, frame)`, the last three read from the instance's `+0x3AC`, `+0x3AE` and `+0x3A2`, and
returns 0 for the step when it answers 1. Outside an event that is a kind-1 effect `0x14A` on an odd
whole age. In an event (`0x001EC560`) it is the one frame when the cut-scene name (`0x001C50C0`)
contains `spc_z0000`, `0x01EF9218` is 8 and the cut-scene frame `0x01F832C4` is `0x39F`.

### The cull, the release and the spawn slots

The type tails end in one fork: `0x005002E0(definition, position)` returns 1 to keep and 0 to cull,
and a culled element is released while a kept one fires its spawn slots with trigger 2. The cull
record is the current instance's `+0x2E0`, or the definition's `+0x60` when that record's first
byte is `0xFF` (`0x005002F9`–`0x0050030F`).

| Cull record field | Meaning |
|---|---|
| byte `+0` | 1: cull by distance; 2: the same with the Y components zeroed; other: no distance test |
| float `+4`, `+8` | cull when the distance is below `+4` or above `+8` |
| byte `+1` bit 0 | also cull when the point projected through `0x02AEECB0` is rejected or falls outside `0x6000`–`0xA000` on either screen word |

The distance is from the point at `0x02AED5F0` to the position transformed by `0x02AEEA20`, computed
by `0x002F1D90` (`0x00500324`–`0x00500381`, `0x005003D9`–`0x00500442`).

The release `0x002F31C0(element, emitter)` runs the type's release method (types `0x40`–`0xD1`, then
the sub-range table `0x0043E9C0` for `0x42`–`0xA3`; anything else has none), unlinks the element
from the active list and pushes it on the free list `+0x120` (`0x002F31CA`–`0x002F3297`). A culled
element is gone, not hidden.

`0x003A8950(trigger, element)` walks eight slots of the element's emitter record: tag byte
`+0x298 + i`, emitter-record index `+0x288 + 2i`, start frame `+0x2A0 + 2i`, definition index
`+0x2C6 + 2i`, and the element's last firing `+0x1D0 + 4i` (`0x003A896E`–`0x003A899A`).

| Tag | Fires |
|---:|---|
| 0 | never |
| 1 | once, when unfired and the whole age has reached the start frame |
| 2 | on trigger 2 only, not on odd frames in the half-rate cadence: first at the start frame, then whenever the time since the last firing reaches the integer track at the indexed emitter record's `+0x10` |
| 3 | on trigger 3 only, the element's ending |
| other | on every call |

A firing calls `0x003A8AE0(index, definition, 2, time, …, element)` (`0x003A8A6C`–`0x003A8A97`).

### Child emitters

`0x003A8AE0` looks up the emitter record in `[[0x02EBEF90]]` and the definition in `[[0x02EBEF78]]`,
returning 0 when either is missing or the record's word `+0x2B2` is 0 (`0x003A8AE8`–`0x003A8B42`). It
reuses a matching emitter (`0x003A8F80`) or makes one (`0x003A9100`, `0x0043F450`), records the parent
element at `+0x130`, and births as many elements as the record's integer track at `+0` gives at
the firing time (`0x003A8B5C`–`0x003A8C22`).

### The emitter's own cull and inheritance

Before an element is placed, `0x0043F2B0(emitter)` applies the cull record of the cull table above to
the emitter's position `+0x80`: the instance's `+0x2D0`, or the emitter record's `+0x2B4` when that
record's first byte is `0xFF`. `0x00441B30` places no element when it returns 0 (`0x00441BD4`), and
`0x003A8AE0` births no children (`0x003A8BF1`).

When a birth has a parent element, `0x00441F10(emitter, parent)` adds the parent's sampled values
into the emitter's spawn values before the birth dispatcher runs, one group per bit of the emitter
record's byte `+0x2C5`:

- bit 0 adds the parent's `+0xB0`, `+0xC0` and `+0xD0` vectors to the emitter's `+0x90`, `+0xA0`
  and `+0xB0`;
- bit 1 multiplies `+0xF4` by the parent's `+0x1F8` and adds `+0x1FC` and `+0x200` to `+0xF8` and
  `+0xFC`; bit 2 adds the parent's `+0x110` and `+0xF0` vectors to `+0xC0` and `+0xD0`;
- bit 3 multiplies `+0xE0`–`+0xE8` by the parent's `+0x120`–`+0x128`; bit 4 mixes the colour `+0xF0`
  with the parent's colour `+0x1F0` through `0x0026EE00`.

`0x00441EA0(emitter)` returns, for an emitter whose parent element's emitter record has byte `+0x283`
above 1, that record's word `+0x286`, or the parent's own word `+0x204` when the byte is 7, and 0
otherwise; the base birth looks up the `0x700` path object the element follows with it
(`0x003A8240`). `0x00441EE0(emitter, element)` tells whether the element is on the emitter's active list.

### Signals and extra steps

- `0x003B3CA0(handle, value)` makes the handle's instance current and calls `0x003A9490`, which signals
  every element of types `0x67`, `0x6B`, `0x71` and `0x72` through `0x0043EE70`: each type's handler
  sets one word of the element to 1 (`0x0045FD00` `+0x3D8`, `0x00529D40` `+0x3D4`, `0x0052A8A0` `+0x434`,
  `0x0052B5D0` `+0x3F8`).
- `0x0024B9B0` calls `0x003A93F0`, which updates the elements of each emitter of type `0x40` or `0xA1`
  that follows a subtype-0 path object whose byte `+0x118` is 3 or 11 a second time, through
  `0x00442310` with `dt` = 2 × `[0x01DFE0BC]`.
- `0x003A92D0(emitter)` releases every element of an emitter of type `0x40`, `0x41`, `0x67`, `0xA1`,
  `0xA3`, `0xD0` or `0xD1`; its default arm `0x004FF360` does the same for `0x42`, `0x6A`, `0x6B`,
  `0x70`–`0x74` and `0xA3`, and leaves the other types' elements alone.

### The 0x700 path objects

A `0x700` record describes a moving reference point. `0x003A8020(index, …, key, byte)` creates an
object for record `index` of `[[0x02EBEFA0]]`: `0x160`, `0x1B0` or `0x1C0` bytes for subtypes 0, 1 and
2–3, record at `+0xE0`, key at `+0x100`, linked on the instance list at `[0x02EBEF98]`; `0x003A8240(key,
index)` finds one. Each subtype has an initialiser, run through `0x004FF110`, and a step, through
`0x004FF0D0`:

| Subtype | Points | Initialiser | Step |
|---:|---|---|---|
| 0 | the anchor at record `+0xD0` | `0x00537C20` | `0x00537BA0` |
| 1 | anchors at `+0xD0` and `+0x160` | `0x00537EA0` | `0x00537CC0` |
| 2 | two anchors and one bend point | `0x00538280` | `0x00537FF0` |
| 3 | two anchors and two bend points | `0x005386F0` | `0x005383B0` |

- An initialiser resets the anchors' state blocks (`+0x110`, `+0x160`) with `0x003A3E20` and runs the
  step once. Subtypes 2 and 3 first sample a fixed bend value (`+0x210`, `+0x290`) into `+0x1B0` and
  `+0x1B4` when bit 1 of the bend's byte (`+0x221`, `+0x2A1`) is set.
- A step resolves the anchors with `0x003A56C0` and fails when one is missing. Subtypes 2 and 3 get
  each bend point from its curve (`0x004FE4E0`, records `+0x1F0` and `+0x270`) or from the fixed value
  (`0x004FE710`).
- Subtype 2 then moves along start, bend and end by the progress track `+0x270`, and subtype 3
  along start, both bends and end by `+0x2F0`, each part sized by its distance (`0x002F1D90`).
  `0x004FEAD0` turns the point into the object's matrix.
- The aim queries `0x00537C50`, `0x00537EE0`, `0x00537F40` and `0x00538780` hand the anchor at `+0xD0`,
  `+0xE0`, `+0x170` or `+0x160` to the anchor query `0x003A4290`, for the aim modes of `0x004FEAD0`.
- `0x004FF080(object)` resets a new object (`0x003A80A3`, `0x003A82E4`): it clears `+0x103` bit 0, `+0x100` and
  `+0xE0` to `+0xFF`, then stores the answer of `0x00250000` in `+0x103` bit 1.
- Every subtype's step starts with `0x004FE930(object, dt)` (`0x00537BC3`, `0x00537CE3`, `0x0053801F`, `0x005383DF`). It adds
  `dt` to the time `+0xF8`, takes the frame `+0xFC` as the whole time less the record's start `+0xC6`, and does
  nothing (returning 0) before the start or past the record's length `+0xC8` when that is not 0.
- Inside that window `0x004FE930` samples the record's tracks (`0x00430B90`): the point into `+0x80` (keeping the last
  one at `+0xC0` when the record's `+0xC3` is set), the track at record `+0x40` into `+0x90` and the one at `+0x80`
  into `+0xB0`, and sets `+0x103` bit 0.
- `0x004FF1B0` and `0x004FF1F0` choose a query by the record's subtype `+0xC2` for `0x0052F560` (`0x0052F76A`, `0x0052F6B4`):
  `0x004FF1B0` calls `0x00537F10` for subtype 1 and `0x005382F0` for the others; `0x004FF1F0` calls `0x005382F0` for 0,
  `0x00537F70` for 1 and `0x00538320` for 2 and 3.

### Timeline tracks

The instance's block at `+0x130` (`[0x02EBEFB0]`) holds sixteen timeline players. `0x003A7050` steps
each through `0x00332750` after the emitter step and frees a player whose step returns 0
(`0x00333350`, `0x003697F0`). A player's tracks are stepped by `0x0046E990(track, dt, slot)`, built from
the `0x600` record's sub-entries; a track's event list is at the sub-entry's `+0x20` (count byte
`+3`, 0 meaning 64), filled by `0x0046F380`, which frees the slot's old event first.

`0x0046EE30(track, sub-entry, id, byte)` fills a new track and `0x0046EFD0(track, slot)` starts it at
time 0. `0x0046EFD0` creates the path objects the sub-entry lists (`0x003A8240`, `0x003A8020`), runs every
enabled subtype-2 event through `0x003B8670`, and fires the time-0 events: subtype 1 births an
emitter (`0x003A8AE0`), first creating its path objects with `0x0046EF10`, and subtype 3 runs
`0x004FF2C0`.

`0x0046E990` adds `dt` to the track's time `+0xC`. It keeps two lists the events start: vibrations
(count `+0x12`, `0x40` bytes each from `+0x20`) and a second kind of channel (count `+0x13`, 16
bytes each from `+0x120`). It then fires the events:

- subtype 2 once its start `+8` is reached, while the time is 0 or the whole time `+0xA` from the
  last step is below its end `+0xC`; if the player was freed meanwhile it returns 0;
- subtype 1 once, when the start is reached and the whole time from the last step is below it;
- subtype 3 from the start to its end, plus 1 in the half-rate cadence.

An event's byte `+5` bit 0 enables it; with bits 1–2 equal to 1 it also needs bit `track byte
+0x10` of the instance's word `+0xC`.

- `0x004FF2C0(event, track)` dispatches on the subtype: 0 and 1 to `0x00538820`, 2 to `0x003B8670`, 3 to
  `0x005372D0`. `0x004FF320(event)` prepares a newly loaded event and returns the address after it:
  subtype 0 is `0x10` bytes, 1 goes to `0x005388F0` (`0x20`), 2 to `0x003B9FB0`, 3 to `0x005375B0`
  (`0x20`).
- `0x00538820` births the emitter record `+0x10` with definition `+0x12` once the track has reached
  the start `+8`; with bit 0 of `+0x14` the key gets the event byte in its high byte and
  `0x0046EF10` creates the path objects first.
- `0x005372D0` starts a vibration when the track is within one frame after the start and fewer than
  four run: the kind-`0x58` pattern record at `+0x1C` (resolved by `0x005375B0` from slot byte
  `+0x10`) goes to a slot (`0x0035B2F0`, `0x0035B580`) with a level from `0x00537410` / 127.
- `0x0046EDD0` (called by `0x00377230`) and the vibration loop of `0x0046E990` stop a finished vibration (`0x0035B1A0`) and
  otherwise set its scale from `0x00537410` / 127 (`0x0035B550`). `0x0046EE70` stops a track's
  vibrations and channels. `0x0046F330` resets a sub-entry: `0xC0000000` at `+0` and 192 null slots.
- `0x0046EF10(track, record, byte)` creates the path object of an emitter record whose byte `+0x283`
  is above 1 (`+0x286`) when it does not exist, and recurses into the record's eight spawn slots
  (`+0x288`).

### The track slots

A player holds sixteen track pointers at `+0x00`–`+0x78`, its `0x600` record at `+0x80`, a flag
byte `+0x90`, a target cursor `+0x91` and a running track counter `+0x92`. The record lists its
sub-entries as encoded pointers at `+0x2C + 4 × n` (`0x0020E600`): byte `+1` and bytes `+2`–`+7` name
the sub-entries a start opens, byte `+9` the one opened per target, and bytes `+0x0A` onward the
one each signal opens.

`0x0020E610(word)` is the null test of such an encoded word, `word == 0`; its only caller, the
type-`0x91` birth arm `0x00459420` ([Effect element types](effect-element-types.md)), uses it to pass over empty words
of the table at `+0x2B0` (`0x00459566`, `0x0045957B`).

- `0x003331A0(player, sub-entry, target)` publishes the player at `0x02EC0F88`, allocates a `0x170`-byte
  track (`0x0036A190`) into the first empty pointer, fills it with `0x0046EE30(track, sub-entry,
  counter, target)`, clears its byte `+0x11` and starts it (`0x0046EFD0`); a start that returns 0
  frees the track (`0x0046EE70`, `0x003697F0`). A target of −1 becomes 0 unless bit `0x1` of `+0x90` is set.
- After a non-null sub-entry, the counter `+0x92` goes up by one whether or not a slot was free; a null
  sub-entry does nothing at all.
- `0x00333280(player, sub-entry, n)` does the same with target −1 and stores `n` in the track's
  byte `+0x11`, the byte `0x003333F0` compares when a script waits on trigger `n`.
- `0x003337B0(player)`, the start, frees all sixteen tracks, then opens the sub-entries of bytes
  `+1`–`+7` whose delay words (`+0x18`, `+0x1A`–`+0x24`) are 0 through `0x003331A0`, and, with bit 0
  of `+0x90` set and word `+0x26` 0, one track of byte `+9` for the next target from `+0x91` that
  `0x003A3E30` finds, stepping `+0x91` past it.
- `0x0024FE70(instance, n)`, the signal, makes the instance current. Without a player it starts a
  state-2 instance (`0x003A74F0`, with `0x02092720` set while `n` is non-zero) or attaches one to a
  state-1 or state-7 instance (`0x003A7460`, also setting `+0x378` bit `0x400`), and sets state 1.
  It then opens the sub-entry of record byte `+0x0A + n` on the first player through `0x00333280`
  and returns 1, or 0 when that byte is 0.

A track's word `+8` is the counter value it was given (`0x0046EE30`), and the emitters its events
birth keep it at `+0x1C` (`0x00538820`, `0x003A8AE0`, `0x0043F450`). The battle effect program stops tracks by that key through `0x00333640(player,
track, frames)`: below 2 frames it frees the track at once and every emitter with its key
(`0x003336C0`, `0x003A8510`); otherwise it stores the key at instance `+0x37C`, the frames at `+0x358`
and `+0x35A`, 1.0 at `+0x35C`, and sets bit `0x2000` of `+0x368` (clearing `0x1000`).

`0x003A7050` counts `+0x35A` down by the whole part of `dt` while bit `0x1000` or `0x2000` is set, keeping the fraction
left at `+0x35C`. At 0, bit `0x2000` frees through `0x00333740(player, key)` the first track with the
key and every emitter with it (`0x003A8510`); bit `0x1000` frees through `0x003334B0(player, key)`
every track and emitter without it (`0x003A8660`).

### The method tables

Every per-type behaviour is a switch on the element's type byte. Five tables cover the main range
and five more the sub-range `0x42`–`0xAB`, which each main table reaches through its default arm.

| Method | Main dispatcher | Key | Sub-range dispatcher |
|---|---|---|---|
| birth | `0x002F3BC0` | element `+0` | `0x0043EBF0` |
| update | `0x002F3910` | element `+0` | `0x0043EAB0` |
| draw | `0x002F4020` | element `+0` minus 1 | `0x0043ED30` |
| setup | `0x005004C0` | definition `+0x44` | `0x00538910` |
| release | `0x002F31C0` | element `+0` minus `0x40` | `0x0043E9C0` |

Decoded from the jump tables: 47 types have main birth, update and setup arms, 46 a draw arm and 6 a
release arm; 18 types have sub-range arms (9 with a release). 65 types have an arm somewhere, with
248 distinct handlers; the per-type list is on [effect element types](effect-element-types.md).
`0x005004C0` runs once per definition, from the `0xA00` record handler.

### The six display layers

`MainLoop_Draw` (`0x0022B0B0`) asks for effects six times through `0x00258EE0(layer)`, each request
bracketed by the engine's marker text. The draw-side order inside a layer comes from the grouped
pass `0x00259030`.

| Layer | Marker | Work |
|---:|---|---|
| 1 | `display VFX [layer : first]` | grouped pass, then `0x0024C640` |
| 2 | `display VFX [layer : after BG]` | the same |
| 3 | `display VFX [layer : TsEffMan_Layer_AfterOBJ]` | no grouped pass: `0x0039D570(0)`, `0x0039D3F0`, a pair of calls chosen on `0x02F8F310` bit 2, then `0x003A3990` |
| 4 | `display VFX [layer : in EFF]` | `0x0039CFF0(0, 0x3C00)`, `0x0036F550` unless `0x00181DD0()` is non-zero, grouped pass, `0x0039CFF0(0, 0x3700)`, `0x0024C640` |
| 5 | `display VFX [layer : after EFF & MENU]` | `0x0036F9F0` unless `0x00181DD0()` is non-zero, then the grouped pass |
| 6 | the same text as 5 | grouped pass |

Every layer request runs between `0x00862C10(0, layer)` and `0x00862C30`. The opening call
(`0x001B2530` on the object `[0x01F7F4D8]`) binds three textures of the render manager to the texture ids
`0xE00`, `0xDFF` and 0, choosing the second set for a layer above 5, stores the pass id at
`+0x90` and the layer without bit `0x10` at `+0x94`, and files a `GiBeginScene` (`0x001FBD80(2)`); the closing call
files a `GiEndScene` (`0x001B2600`).

`0x00862C40`, `0x00862C00` and `0x00862BF0` return those two words; the drain uses them to close and
reopen the bracket around the post-processing block, with `0x10` added to the layer (`0x003A3740`).

`0x00259030(layer)` selects arena 8, calls `0x0024D370(layer, group)` for groups 2, 3, 5, 6, 9, 1, 7 and
4, then drains the draw list (`0x003A3740`) (`0x00259036`–`0x002590C0`). A group is an instance kind.

### Drawing one group

`0x0024D370(layer, group)` takes the list `0x020910F0[group]` and asks the group gate `0x0024D4E0`
(`0x0024D382`–`0x0024D3AF`). The gate refuses group 8; groups 1–4 and 7 need bit `group − 1` in the AND
of `0x02092162`, `0x02092164` and `0x02092166`; group 2 also needs `0x02F8F29E` bit 0 clear and group 5
`0x02EBEF68` bit 0 clear (`0x0024D4E0`–`0x0024D538`).

For each instance the group draw publishes the group at `0x02092700` and skips the instance unless
its `+0x3A8` equals `0x00181DD0()`, the high nibble of its word `+0x378` equals the layer, and the
per-instance gate `0x0024D770(instance, 1)` passes (`0x0024D3C0`–`0x0024D3FC`). It makes the instance
current and walks its emitters through `0x003A72F0` → `0x003A8D80`, which calls `0x00441970` for each
(`0x0024D405`, `0x0024D499`, `0x003A8D84`–`0x003A8DAB`). So an effect's layer is authored in its
instance.

`0x00441970(emitter)` returns when the emitter has no elements. Unless the instance's flag byte
`+0x36A` has bit 0, only emitters whose definition type is `0x40`, `0x41`, `0xA1`, `0xA2`, `0xA5`
or `0xD0` are drawn (`0x0044198E`–`0x004419CE`; the table is
[`effect-element-runtime-effect-kind-441970.tsv`](effect-element-runtime-effect-kind-441970.tsv)). It sets the pass nibble `0x02AEE910`: definition
byte `+0x4C` when `+0x4A` is `0x40` or more, else 8 (`0x004419F5`–`0x00441A0E`).

It then calls `0x002F4020(element, emitter)` for each element, forward from the head, or backward from
the tail when the emitter record's byte `+0x2C4` has bits 0–1 set (`0x00441A15`–`0x00441A82`).

### Instance flags at draw time

Before the emitter walk, `0x0024D370` reads the instance's flag byte `+0x36A`. With bit 0 set it
records the instance's target `+0x380`, when there is one, for texture id `0x3300` at 256
× 224 (`0x002D7D90`), then calls `0x003AA2E0(0)` and skips the instance when that returns 0. With bit 1
set it files a `GiZNormalOnOff` command with 1 (`0x0039D410`, through `0x00864E00`) and sets bit 0 of
`0x02F8F310`, which makes the drain open with `GiTransNz` instead of `GiTrans` (`0x003A3740`).

### Widescreen and mask-border flags

`0x0024E4B0` classifies the current instance's context while the pass id `+0x90` of `[0x01F7F4D8]` is
0 (`0x00862C40`), by its kind byte and its id word `+4`:

| Context | Ids | Bits |
|---|---|---|
| kind 1 | `0x80` | `0x10` |
| kind 1 | `0x89` | `0x8` |
| kind 1 | `0xD5`–`0xD7`, `0xE2`, `0x17A`, `0x182` | `0x2` |
| kind 7 | `0xB0`, `0x2C0`–`0x373` | `0x1` |
| kind 7 | `0x240`–`0x2BF` | `0x1` for 25 listed ids, `0x4` for `0x289`, `0x3` for `0x28B` and `0x2A3`, `0x2` for the rest |

Any other context gets 0. For each instance it draws, `0x0024D370` calls `0x00183090(1)` after the
emitter walk when the flags have bit `0x2`, which sets `0x01F7F4F8`, one of the flags the mask-border
wrapper `0x0017F6B0` tests; the frame state machine `0x0022A580` clears it each frame (`0x00183090(0)`). `0x0024E640` turns the flags into the widescreen mode the element draws use: 1 for
bit `0x1` or a kind-7 id from `0x200` to `0x23F`, else 2, 3 or 4 for bit `0x4`, `0x8` or `0x10`, else
0.

`0x00184740`, from the frame `0x0022A770`, reads the current instance through `0x0024DE30(&kind, &id,
&frame)`, which returns its bytes `+0x3AC`, `+0x3AE` and `+0x3A2` + 1. While a kind-1 effect
`0x17A` is current and the latch `0x01F7F540` is clear, it sets both; any other current effect
clears `0x01F7F500`, another flag `0x0017F6B0` tests. `0x00182D30` clears the latch.

### Soft particles

`0x0024D140(&factor)` answers whether the current context draws soft particles, for the `GiSprite`
builder `0x008647C0` (`+0xD0` and `+0xD4` of the command) and the VU program packet `0x001DB840`
(`+0x630` and `+0x634`). It answers no with a factor of 0.1 unless the pass id is 0 and the layer
`+0x94` is 4, or 3 or 4 when `0x0017FE10()` (the byte `0x01DF08F4`) is non-zero. Otherwise the kind
picks a table from `softparticle_*.csv` ([standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md)):

| Kind | Key | Table |
|---|---|---|
| 1 | id word `+4` | `0x02F95B40` (`magic`) |
| 2 | the instance's word `+4` against the map's rows | `0x02F8F340` (`softparticle_bg.csv`) |
| 3 | `0x003B33D0(id)` | `0x02F96B40` (`chara`) |
| 5, 6, 9 | the effect number `0x003B0940(handle)` | `0x02F95340` (`common`) |
| 7 | id word `+4` | `0x02F96340` (`event`) |

Kinds 4 and 8 answer no. A table entry answers yes when its byte 0 is set, with the factor its
word `+2` / 100; a bound of 512 entries applies. For kind 2 the answer and factor are the matched
row's bytes `+1` and `+2`.

`0x0024F790`, run by the EFB loader `0x0026FB90`, picks the map's rows: it takes the text after the
backslash of the map-art context's name `+0x241` (`0x00180370`), finds the matching 16-byte record in `0x02F93340`, and
stores its first row in `0x01E0C290` and the row count in `0x02092710` (up to the next record, or to
`0x02092714` for the last). No match stores −1.

### Drawing one element

`0x002F4020` returns when the type byte is outside `[0x022BE7D8]`..`[0x01EEBAE0]`, or when `+0x224` is set
while the cadence test returns 0 (`0x002F402A`–`0x002F405B`). With definition byte `+0x4D` non-zero, a
counter in word `+2` and the cadence test set a skip bit in byte `+1` bit 0, and a set bit skips
the draw (`0x002F4070`–`0x002F40E6`). It stores definition byte `+0x75` at `0x02AEF41C`, calls the type's
draw method, and clears `0x02AEF41C` again (`0x002F40EC`–`0x002F4124`, `0x002F4369`).

The debug console's "Particle Draw Type Range" entries set the bounds through `0x002F1CD0(low,
high)`; they ship as 0 and `0xD1`, so every type draws.

### The draw list

Blended primitives do not draw at once. An emitter appends a `0x28`-byte entry to the list at
`[0x02F8F2F8]`, counted by the word `0x02F8F2C6`; the point emitter `0x0039D970`, for one, writes the
projected depth word as the sort key `+8` and ORs the pass nibble into bits 28–31
(`0x0039D986`–`0x0039DA05`). `0x003A3670` allocates the list, `0x190000` bytes, which is 40,960 entries.

`0x003A3740` drains it. It returns for an empty list, sorts the entries by `+8` (`0x003A3A50`), and for
each entry calls the function at `+0x10` with `+0x00`; without one, it submits the command at
`+0x18` through `0x0020E630(command, 2)`, or with flag bit `0x4` defers it to `0x02AEF420` for layer 3's
`0x003A3990` (`0x003A3744`–`0x003A3908`). It empties the list and keeps the last and peak counts
(`0x003A3929`–`0x003A3973`).

`0x0024D540`, the frame's draw setup, drains once more and then rewinds: `0x003A3A00` resets the packet
cursor `0x02F8F2D0` to the arena base `0x02F8F308`, sets its end `0x02F8F2D8`, and zeroes the count
(`0x0024D556`, `0x0024D55B`, `0x003A3A00`–`0x003A3A42`).

Three other producers copy data into the packet arena behind `0x02F8F2D0` and file an entry for it;
each does nothing when the arena lacks room. `0x003A2C80(callback, data, size, pass, key)`, called
from `0x004781A0`, stores the copy at `+0x00` and the callback at `+0x10`, so the drain calls it with
the copy.

`0x003A3010(data, size, key)` and `0x003A31A0`, called from effect types (`0x0044D4A0`,
`0x00453150`, `0x00460BC0`, `0x00522300`; `0x0045BAE0`), build a GS packet around the data, with the blend
word of the current mode, and file it at `+0x00` with no callback and no command. The drain does
nothing with such an entry: it calls a callback when there is one and otherwise submits only when
`+0x00` is null (`0x003A38BA`–`0x003A38CD`).

### Target and anchor queries

Some tails ask for a point from a sub-record. `0x002F3360` switches on the sub-record's byte `+0x90`;
value 3 calls `0x003A56F0`, which samples a vector track (`0x00430B90`) and switches on the byte `+0x48`
minus 1 over 14 cases (`0x002F3384`–`0x002F33EA`, `0x003A575E`–`0x003A5797`). `0x003A4290` has the same
14-case switch on the same byte (`0x003A4303`–`0x003A4319`).

Their arms are in
[`effect-element-runtime-switch-family-3a42-3a56.tsv`](effect-element-runtime-switch-family-3a42-3a56.tsv); [`effect-element-runtime-switch-family-frontier-decode.tsv`](effect-element-runtime-switch-family-frontier-decode.tsv)
decodes `0x00442170` and `0x00442460` (the emitter-record subtype switches) and the record-store
fronts `0x00500980` / `0x00500850`, together with dispatchers outside the effect code.

### Target slots

An instance names its targets in the dword array at `+0x10`, with its count in byte `+0x372`.
With bit `0x200` of word `+0x378` set, both readers below take the global list `0x02096A24` (count
`0x02096B24`) instead.

`0x003A5640(slot)` treats slot −1 as slot 0. In a kind-3 instance it returns the `+0x10` entry as it
is; otherwise it takes the `+0x90` entry, or the `+0x10` entry when that is 0, and returns it through
`0x002E9B80` (the first dword of the actor's `+0xC0` object, or −1).

`0x003A3E30(slot)` returns the `+0x10` entry, or −1 past the count. In a kind-1 instance whose word
`+0x368` is below `0x8000` it first checks the target (`0x003229E0`, `0x00322760`): a target that fails
adds one to byte `+0x374` and gives −1, and a replacement that `0x00322760` reports goes into `+0x10`,
with the old entry kept at `+0x90`, after an effect `0x62` is played on it (`0x003B02A0`).

`0x003A4220(id)` picks one of three lookups by the instance: `0x0036E620` when bits 12–14 of word
`+0x36A` are 3, `0x0036E4B0` in a kind-2 instance, and `0x0036E4E0` (a 64-entry table at `0x022D97B0`)
otherwise or when the first finds nothing; it returns the result through `0x002E9B80`.

Two wrappers hand these to element handlers:

- `0x0024DCE0(mode, n)`, for `0x00524320`: mode 0 gives the current instance's owner `0x003A3FD0(−1)`
  (−1 with no instance current), mode 2 gives `0x003A4220(n)`, and mode 3 the render index of the
  n-th actor of manager 0 (`0x02098E10`) that has one (`0x00358940`, `0x003589B0`, `0x002E9B80`); any
  other mode, or no match, gives −1.
- `0x0024DDD0(&owner, &target)`, for `0x0045FD50` and `0x00529200`, returns `0x003A3FD0(slot)` and
  `0x003A6BA0(slot)` for the slot byte `+0x13B` of the current emitter `[0x02EBEF80]`.
- `0x003A6BA0(slot)` returns a kind-3 instance's `+0x10` entry for the slot (slot 0 for −1) as it is; otherwise it
  passes the slot's `+0x10` entry, or for −1 the `+0x90` entry and else the first `+0x10` one,
  through `0x002E9B80`. With `+0x378` bit `0x200` it reads the global list `0x02096A24` instead.

The three 64-entry tables are filled by script verbs, each taking an index clamped to 0 to 63 and
storing the calling script's actor (`0x00263F10`, `0x003589B0`):

| Verb | Table | Set | Clear |
|---|---|---|---|
| `effectactor(n)` (`0x0126`, `0x00352270`), from manager 3 | `0x022D99B0` | `0x0036E880` | `clear_effectactor` (`0x056F`, `0x00342010`): `0x0036E1A0` |
| `effectactor(n)` from any other manager | `0x022D97B0` | `0x0036E7E0` | `clear_effectactor`: `0x0036E160` |
| `bgeffectactor(n)` (`0x0570`, `0x00352940`) | `0x022D98B0` | `0x0036E7B0` | `clear_bgeffectactor` (`0x0571`, `0x003423C0`): `0x0036E040` |

The manager is the issuer's byte `+0x15`. A clear stores 0.

### Raw owner and target reads

Two more readers take the current instance `[0x02F97348]` without the `0x002E9B80` step:

- `0x003A6D90(slot)`: with `+0x378` bit `0x200` clear, −1 for a kind-3 instance, the `+0x10` entry for
  any slot other than −1 with no compare against the count `+0x372`, and for −1 the `+0x90` entry, or
  the first `+0x10` entry when that is 0. With the bit set, entry `slot` (0 for −1) of `0x02096A24`
  while it is below `0x02096B24`, else −1.
- `0x0024B6F0`, `0x0024C870` and `0x0024F9B0` call `0x003A6D90` with 0, and `0x003B99D0` with the byte `+0x10` of
  `[0x02EBA4F0]` (`0x003B9A5F`).
- `0x003A4070(slot)`: with the bit set, `[0x02096A20]`. Otherwise −1 for a kind-3 instance, and for a
  kind-5, 6 or 9 instance whose request (`0x003B0BF0(+0x04)`) is missing or has target test `+0x11` =
  1; else the slot's `+0x90` entry, or the owner `+0x08` for slot −1 or a zero entry. `0x003B99D0`
  calls it (`0x003B9AA1`).

### Renaming an owner or target

`0x0024C600(old, new)` does nothing unless both ids are non-zero. It then replaces `old` by `new` in
the owner `+0x08` and in both target arrays `+0x10` and `+0x90` (count `+0x372`) of three sets of
instances:

- `0x002FBFA0`: every instance on the kind-1 list `0x020910F0[1]` (`0x020910F8`), through `+0x348`;
- `0x003B0190`: the instance `+0x08` of each of the 36 request entries at `0x02EBEC00` whose handle is
  non-zero and whose target test `+0x11` is not 1;
- `0x003B14F0`: every instance on the kind-7 list `0x020910F0[7]` (`0x02091128`).

Its one caller is the party snapshot read `0x00326D60` (`0x00327117`,
[party slots](../Party/party-slots.md)). For each staged member it passes the unit id saved at
record `+4` and the handle `+0x08` of the unit that now holds the member's party record, when the
two differ.


### Numbered effects on actors

`0x003B02A0(owner, targets, count, number, kind)` plays effect `number` as an instance of kind 5, 6 or 9
and refuses any other kind. Unless the request kind below is 1, it also refuses when
`0x002FC9B0()` plus `0x003B0B70()` exceeds 23. It makes the instance (`0x0024B270`) with state 2 and
the number in `+0x373`, stores the owner at `+0x08`, and appends each target whose render record is
live and passes `0x002E9FE0` to the target array `+0x10`. Numbers 100 to 103 and `0x94` are kind-3
requests in the table below.

The requests sit in 36 entries of `0x18` bytes at `0x02EBEC00`, packed from the start:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | handle: kind << 28 \| serial (0x02EBEF60) |  |
| `+0x04` | `u32` | set by 0x003B0FD0 |  |
| `+0x08` | `void*` | the instance |  |
| `+0x10` | `u8` | effect number; | +`0x11` u8 target test;  +`0x12` u8 kind |
| `+0x13` | `u8` | bits 1-2: request kind (3 for 100-103 and 0x94, 1 when the number's 0x01EFE260 byte is 1, else 0) |  |

- `0x003B0980` returns the first free entry; with all 36 taken it ends the first instance whose
  request kind is 0 or 3 (`0x0024EE60`), closes the gap and returns the last entry.
- `0x003AFFB0(n)`, from `0x002FCCC0`, ends requests from the front of the table until `n` are left,
  sparing request kinds 1 and 2. `0x003B0B70` returns half the number of entries in use.
- `0x003B0BF0(handle)` returns the entry, `0x003B0940(handle)` its effect number or −1, and
  `0x003B0FD0(handle, v)` stores `v` at `+0x04`. `0x003B0C30(owner, number)` is
  `0x003B02A0(owner, 0, 0, number, 5)`.
- `0x003B0820(v)`, with arena 8 selected, ends the instance (`0x0024EE60`) of every entry whose `+0x04`
  equals `v`, closes each gap and clears `0x02EBEF48`. `0x002FCB60(handle)` calls it with its own
  handle first (`0x002FCB79`).
- `0x003B1260(handle, kind)`, for a kind of 1 to 10, calls `0x0024FE70(instance, kind)` with arena 8
  selected.
- `0x003B1050(targets, n)`, from `0x0024FBF0`, raises bit `0x4` of `+0x368` on every kind-5 instance
  whose request kind is 0, or is 1 or 3 and whose owner `+0x08` equals an id of the list (`+0x11`
  = 0) or the value `0x002E9B80` returns for one (`+0x11` = 1).
- `0x002FD090()`, from the same `0x0024FBF0` (`0x0024FC58`), raises bit `0x4` of `+0x368` on the instance `+0x10` of
  every handle on the kind-1 active list `0x02EC3D60`, without a test.

### Battle effect files

Kind-1 effects come from 48 slots of `0x38` bytes at `0x02EC32E0`, chained by `0x002FC200` into a free
list `0x02EC3D70`; the active list runs from `0x02EC3D60` to `0x02EC3D68` through `+0x28` and `+0x30`.

`BattleEffectSlot` (`0x38` bytes, offsets from the start of the 0x02EC32E0):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | handle | bits 0-5 the slot, `0x10000000` the kind |
| `+0x08` | `void*` | context | the type-1 context |
| `+0x10` | `void*` | instance the instance playing it |  |
| `+0x18` | `u32` | request | the file request |
| `+0x1C` | `u32` | size | the file size |
| `+0x20` | `u16` | number | the effect number |
| `+0x23` | `u8` | state | low nibble: 1 wanted, 2 reading, 3 read, 4 freeing, 5 ready, 6 playing |
| `+0x28` | `void*` | next |  |
| `+0x30` | `void*` | previous |  |

`0x002FCF00`, each simulation step from `0x00258D70`, walks the active list:

- state 1 runs `0x002FC860` unless a read already runs (`0x02EC3D7C`, or the loaded-file queue's
  `0x02EBEBE4`). It asks the file size in class `0x0B`, or `0x26` when `0x002DEBB0()` is 0
  (`0x0032E400`); a missing number `0x78`–`0x89` falls back to `0x78`, `0x8A`–`0x99` to `0x8A`, and
  any other to 0. It queues the read (`0x0032E620`) and sets state 2.
- the read's completion `0x002FC830(handle)`: when the handle's low six bits name a slot below 48 whose word
  `+0x00` is the handle, it sets the state's low nibble to 3 (`0x002FC830`-`0x002FC854`).
- the size cache: `0x002FCFF0` (through the stub `0x0036DDB0`) asks the size of all 512 numbers once, keeps them
  at `0x02EC19C0` (8 bytes each) and sets `0x02EC3D7D`; the reset `0x002FC200` clears it (`0x002FC2FF`). While it is
  set, state 1 takes the size from the cache (`0x002FC8AD`), and a missing number falls back to entry 0, not
  to the `0x78` and `0x8A` ranges;
- state 3 builds the context (`0x002FC4A0`);
- state 4 waits until the request is gone (`0x0032E4D0`), then returns the slot to the free list
  (`0x002FC350`) and clears `0x02EC3D7C`;
- state 6 adds 1 to the instance's frame word `+0x3A2`.

`0x002FCCC0(owner, targets, count, handle)` plays a slot in state 5. It sums the 5-bit weights of
the active slots' numbers (`0x02EC19C4`, filled from the 401 bytes at `0x01EEBB10`), ends numbered
requests until `36 − sum` are left (`0x003AFFB0`), and makes an instance (`0x0024B270`): kind 1, the
handle at `+4`, the owner at `+0x08`, the targets at `+0x10` with the count in `+0x372`, the
slot's context at `+0x340`, `+0x3AC` = 1 and the number at `+0x3AE`. It sets state 6 and returns
the handle, or 0.

`0x002EAD00(owner, count, targets, handle)` returns 0 for no targets; otherwise it counts
`0x02CA4EDC` up (`0x0042FCB0`) and plays through `0x002FCCC0`. Its caller `0x00319E40(unit)` gathers the
ids of the unit's targets (list `+0x780`, count `+0x77C`) whose actors exist and plays on them the
handle `0x0030CA50` reads for the unit: entry `+0x695` of the 32 entries of `0x30` bytes at
`0x022C17D0`, its dword `+4`.

- `0x003B1180(targets, n)` selects instances the same way and sets bit `0x2` of their `+0x368`;
  `0x003B1130` clears that bit on every request's instance.
- `0x003B0220(instance)`, from the free-list drain, finds the request holding the instance, moves the
  later entries down and clears the last; `0x003B0770(handle)` does the same by handle after ending the
  instance (`0x0024EE60`). `0x00319E30(handle)` ignores 0 and −1 and tail-jumps to `0x003B0770` otherwise;
  the battle unit code `0x00300E40` and `0x00301140` pass it the unit's `+0x74`.

### Loaded effect files

A second queue at `0x02EBE5E0` holds 32 entries of `0x30` bytes, each an effect file loaded into its
own type-7 context: `+0x00` id, `+0x04` file number, `+0x08` context, `+0x10` instance, `+0x18`
file request, `+0x1C` state, `+0x20` flags, `+0x28` buffer. Only one load runs at a time
(`0x02EBEBE4`). `0x003B25D0`, each simulation step from `0x00258D70`, moves them on:

- state 1 (`0x003B2310`) maps the file number (bit `0x1000` to `0x200 +`, bit `0x2000` to `0x240 +`,
  bit `0x8000` to `0x1FF`, `0xC3` to `0x1FE` when `0x002DEBB0` returns 0), requests the file in class
  `0x0C` (`0x0032E400`, `0x0032E620`) with the completion `0x003B22D0`, which sets state 3, and sets
  state 2;
- state 3 (`0x003B2220`) builds a type-7 context for the id (`0x0024B3A0`), parses the buffer
  (`0x003EDAD0`), copies the high nibble of the first `0x600` record's `+0x16` into the context's
  byte `+2`, and sets state 5;
- state 4 waits until the request is gone (`0x0032E4D0`), then removes the entry and closes the gap.
  `0x003B21E0` clears an entry's id and state when its request is already gone.

`0x003B2830(id, n)`, for `n` of 1 to 10, calls `0x0024FE70(instance, n)` for the entry's instance and
puts `n` in the low nibble of its word `+0x378`. `0x003B27A0(id, n)`, for `n` of 0 to 10, makes the
instance current and passes its `+0x130` block to `0x003339C0` with `n`. `0x003B1560(flag)` clears bit 0
of `+0x20` in every entry when `flag` is 0, and otherwise passes each entry with the bit to
`0x003B18E0`; no code calls it.

### Filing, sharing and releasing a loaded file

`0x003B1A80(file, tag)` files a load with arena 8 selected. It takes the first entry whose id is 0,
returning 0 when all 32 are taken, and gives it the id `0x70000000 | (serial & 0xFFFF) << 12 | (tag &
0x3F) << 6`, the serial counting up at `0x02EBEBE0`. It stores the file number at `+0x04` and clears
the context, the state, the buffer and flag bits 0 and 1. When another entry with the same file is in
state 5 or 6, the new entry takes that entry's context and starts in state 5;
otherwise `0x003B2310` starts the read, and a refused read clears the entry and returns 0.

`0x003B1BA0(owner, targets, count, id, n)` plays an entry. With `n` 0 it needs state 5: it makes a
kind-7 instance on the entry's context (`0x0024B270`), records it at `+0x10`, sets state 6 and copies
flag bit 1 into the instance's hold bit `0x40` of `+0x368`. With `n` non-zero it needs state 5 or
later and only passes `n` to `0x0024FE70` for the existing instance, putting `n` in the low nibble of
`+0x378`. `0x003B2470(id)` returns an entry's instance.

`0x003B18E0(id)` releases one entry by its state, with arena 8 selected:

| State | Release |
|---:|---|
| 1 | the id and state are cleared and the entry removed |
| 2 | the read is cancelled (`0x0032E590`) and the entry goes to state 4 while the request is still queued (`0x0032E4D0`) or `0x0032E520(1)` holds; otherwise as state 3 |
| 3 | `0x003B21E0` clears the entry, the load-running flag `0x02EBEBE4` drops, and the entry is removed |
| 5 | the context is freed (`0x0024F410`) unless another entry for the file in state 5 or 6 holds it (`0x003B2710`); then as state 1 |
| 6 | the instance goes to the free list and the entry to state 7 |
| 4, 7 | nothing |

A removed entry closes the gap and the last entry's id `0x02EBEBB0` is cleared. `0x003B1710(spare)`
applies the same release to every entry, skipping those with flag bit 0 when `spare` is non-zero,
and ends a removed entry's instance (`0x0024EE60`). `0x003B15C0(instance)`, from the free-list drain,
removes the entry whose instance is freed, freeing its context only when no other entry for the
same file in state 5 or 6 has one.

Flag bit 0 keeps a file across an area change. `effectkeepmapjump(slot, b)` (`0x02C5`, `0x0036E9B0`)
writes it through `0x003B2750(id, b)`, and the flag is read by `0x003B24C0(id)`; both accept only an id
whose top nibble is 7. The ordinary area unload runs only `0x0024E910`, whose `0x003B26D0` spares kept
files. When `0x022CB726` is set, as after the title-return reset `0x003601D0`, the unload first runs
`0x0036DF30`, which calls `0x003B1710(0)` and releases every file.

### Script effect slots

Event scripts reach the loaded-file queue through 32 slots of `0x18` bytes at `0x022D94B0`: the
queue id `+0x00`, a state word `+0x04` (0 free, 1 reading, 2 read, 3 playing, 4 cancelled), the
reading manager `+0x08` and the signal bytes `+0x10` ([native commands](../Scripts-And-Script-Commands/native-commands.md)).
Every slot number is clamped to 0 to 31.

- Read: `effectread(id)` (`0x00DB`), `locationeffectread(id)` (`0x0127`) and `questeffectread(id)`
  (`0x01DA`) push slot 0 and the kind 0, 1 or 2; their two-argument forms (`0x00E0`, `0x0128`,
  `0x01DB`) take the slot first. The shared body `0x003576D0` calls `0x0036E320` unless the issuer's
  manager is skipping (`0x00267310`), and then `0x00314D40(1)`.
- `0x0036E320(manager, slot, id, kind)` acts only on a free slot: it clears the signal bytes, adds
  `0x1000` to the id for kind 1 or `0x2000` for kind 2, files it with `0x003B1A80(id, slot)`, which puts
  the slot in bits 6 to 11 of the queue id, keeps the manager, and sets state 1 when it got an id.
- `effectreadsync` (`0x00DC`, slot 0) and `effectreadsync_e1(slot)` (`0x00E1`) poll `0x0036E540`: a
  reading slot waits until `0x0024DE70(id)` reports 2 or 3, then becomes state 2.
- Play: `effectplay(n)` (`0x00DD`, slot 0) and `effectplay_e2(slot, n)` (`0x00E2`) call
  `0x0036E8B0(slot, n)`. A slot in state 2 or 3 whose file reports 2 or 3 becomes state 3 and is
  played by `0x003B1BA0` with the owner `[0x02EBCC70]`, the target list `0x02EBCBE0` (count
  `[0x02EBCC60]`) and `n`. Then `0x0024F8D0` sets bits 12 to 14 of the instance's `+0x36A` to 3 for a
  slot read by manager 3 and to 0 otherwise, which picks the target table above.
- `effectsync` (`0x00DE`, slot 0) and `effectsync_e3(slot)` (`0x00E3`) wait while the state word
  (`0x0036E5A0`) is non-zero; a skip cancels the slot instead.
- Cancel: `effectcancel` (`0x00DF`, slot 0) and `effectcancel_e4(slot)` (`0x00E4`) run `0x0036DDC0`,
  which sets state 4 on a slot in any state but 0 and 4 and, unless the queue entry's flag bit 0 is
  set (`0x003B24C0`), releases the entry (`0x003B18E0`). `effectcancelall` (`0x00E5`,
  handler `0x00350FA0` `jmp 0x0036DE20`) runs `0x003B1710` over the queue and sets every slot to state 4.
- Triggers: `effecttriggersync` (`0x0274`, `0x0275`) waits while `0x0036E5E0(slot, n)` holds: for a
  playing slot, `0x0024FDA0` makes the instance current and asks `0x003333F0` whether one of the 16
  entries of its `+0x130` block has byte `+0x11` equal to `n`, or else `0x003A8FC0(n)`.
  `effecttriggercancel` (`0x01DC`, slot 0) and `effecttriggercancel_1dd(slot, n)` (`0x01DD`) run
  `0x0036DF80`, which passes a non-free slot's id to `0x003B27A0`.
- `effectsignal(slot, v)` (`0x0241`, `0x0036E460`) passes `v` to `0x0024F3C0`, which, for `v` = 1,
  adds 1 to bits 4 to 7 of the instance's word `+0x378`.
- `effecthitsyncbyid` (`0x0440`) waits while `0x0036E640(id)` holds: the file reports 2 or 3 and bit 5
  of the instance's `+0x36A` is clear (`0x0024E210(id, 0)`).

## Layouts

```
effect instance (0x3B0, 0x0024B270)
+0x000  u8    kind (the group and the list 0x020910F0[kind])
+0x120        block published at 0x02EBEF98
+0x130        block published at 0x02EBEFB0
+0x1B8  u32   frame stamp; +0x1C0 first emitter
+0x2E0        cull record (first byte 0xFF: use the definition's)
+0x340  ptr   effect context
+0x348  ptr   next, +0x350 previous
+0x36A  u8    flags: bit 0 draws every emitter
+0x378  u16   high nibble: display layer
+0x3A8  u16   stamp from 0x00181DD0()

emitter
+0x008  ptr   next emitter
+0x024  u32   births
+0x028  u32   emission limit (frames); +0x02C f32 age; +0x030 s32 whole frame; +0x034 f32 last firing
+0x0A0..+0x0F0 sampled spawn values (+0x0F0 colour)
+0x100  ptr   emitter record (0x800); +0x108 element definition (0xA00)
+0x118  ptr   active head; +0x120 free head; +0x128 active tail
+0x130  ptr   parent element; +0x139 u8 stop emitting

element
+0x000  u8    type (from definition +0x44)
+0x001  u8    flags: bit 0 draw skip
+0x002  u16   draw counter
+0x008  ptr   emitter; +0x010 parent; +0x018 emitter record; +0x020 definition
+0x028  ptr   previous; +0x030 next
+0x038  u32   frame stamp at the last update
+0x03C  f32   age; +0x040 s32 whole age; +0x044 s32 track frame; +0x048 s32 updates
+0x04C  s32   lifetime (0 none)
+0x060        position
+0x1D0  s32[8] last firing per spawn slot (-1 unfired)
+0x1F0  u32   colour (0x80808080 neutral)
+0x224  u16   hold word from 0x00250000()

draw-list entry (0x28)
+0x00  u64   callback argument
+0x08  u32   sort key; bits 28-31 pass nibble
+0x10  ptr   callback
+0x18  ptr   command
+0x20  u32   flags
```

## Operations

Per simulation step, one emitter step per emitter of the seven updated kinds, and one base update
per live element. Per frame, six layer requests and up to 40 group draws, each walking the drawn
emitters of one group; each blended primitive costs one draw-list entry, and the list holds 40,960.

## State

The instance lists `0x020910F0`, the current instance `0x02F97348` and context `0x02F97340`, the table
pointers `0x02EBEF70`–`0x02EBEFB0`, the current emitter `0x02EBEF80`, the pass nibble `0x02AEE910`, the blend
pair `0x02AEE900` / `0x02AEE908`, the draw list `0x02F8F2F8` with its count `0x02F8F2C6`, and the packet
cursor `0x02F8F2D0` / `0x02F8F2D8` over `0x02F8F308`.

## Modding notes

- An effect's display layer is the high nibble of its instance word `+0x378`; its group is the
  instance kind. Group 8 is never drawn.
- An element that leaves its cull window is released at once, and its trigger-2 children stop.
  Death bursts belong in tag-3 slots, which fire on the lifetime end.
- The lifetime test uses the whole age with bit 0 cleared, so a lifetime is effectively rounded to
  an even frame count.
- More than 40,960 blended primitives in one frame overrun the draw list; nothing checks the count.

## Related

- [Effect files](effect-files-efx-efb.md): the chunk streams the records come from.
- [Effect element types](effect-element-types.md): what each type does in its methods.
- [Resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md):
  contexts, instances and their teardown.
- [Authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md): the tracks the
  emitters and elements sample.
- [Frame update order](../Engine-Core/frame-update-order.md): where the update pass runs.
- [Global state accessors](../Engine-Core/global-state-accessors.md): the cadence test
  `0x001EDDA0`.
