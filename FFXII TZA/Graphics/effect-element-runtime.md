---
title: "Effect element runtime: instances, emitters and elements, the per-step update, birth, release, child spawns and timeline tracks"
kind: "system"
category: "Graphics"
addresses: "0x0024B270, 0x020910F0, 0x02F97348, 0x02EBEF88, 0x0024ED80, 0x00258D70, 0x0024B9B0, 0x003A7050, 0x003A8390, 0x0043EF40, 0x00441B30, 0x002F3BC0, 0x002F2D60, 0x002F3910, 0x002F2530, 0x002F4020, 0x005004C0, 0x002F31C0, 0x005002E0, 0x003A8950, 0x003A8AE0, 0x003A4290, 0x003A2B20"
---

## What the player sees

A spell effect is a crowd of small pieces: sparks, streaks, sprites, rings, meshes, lights. Each
piece is an element. Elements are born in bursts at set intervals, move and change colour as their
authored tracks say, spawn further pieces while they live or as they die, and disappear when their
lifetime runs out or they leave their visibility window.

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
byte `+3` at `0x02096800`, the scale `+0x320` times `+0x39C` (`0x003A2B20`) with w 1.0 at `0x02096810`, `+0x310` at
`0x02096820` (zero when `+0x378` has bit `0x800`), `+0x300` at `0x02096830`, `+0x330` at `0x02096840` and the depth
offset `+0x338` at `0x02AEE7F4` (`0x0024FD05`-`0x0024FD86`; [menu effects](menu-effects.md)). All the code below
reads these globals.

### The element pool

`0x0043F450(emitter, record, definition, …)` resets the emitter with `0x0043F210`, which frees its old
pool `+0x110` and clears its counters, lists and flags (byte `+0x138` keeps bits `0x3` set and bit `0x4`
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
`0x0024C6B0` (`+0x368` bit `0x80`), `0x0024C870` (`+0x368` bit `0x100`) and `0x003AF330(0)` (`+0x3A0` bit `0x1`,
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
- `0x003B1310` walks the loaded files as `0x003B18E0` treats one ([effect file loading](effect-file-loading.md#filing-sharing-and-releasing-a-loaded-file)), without sparing kept entries,
  and then frees the kind-7 instances.

### The effect teardown

`0x0024E910` ends what a field holds. The area unload `0x002628B0` and the title-return reset `0x003601D0`
call it:

1. `0x002FBEF0`; then every kind-1 context (`0x020910A8`, `0x0024F410`) and instance is freed;
2. `0x0026FF50`, the disposal of the map effect bank;
3. `0x003B2F90` moves every used model-effect slot (`0x02EBDB98`) to the free list `0x02EBDBA0`, ending
   its instance (`0x0024EE60`) and keeping bits 0–5 and 28–31 of its id, and frees the kind-3 instances;
4. `0x003B0130`, then `0x003B26D0`, which releases every loaded file whose flag `+0x20` bit `0x1` is clear
   (`0x003B18E0`);
5. `0x3FF` goes to the group mask `0x02092160`, and bit `0x2` of `+0x368` is cleared in the instance of
   every model-effect slot (`0x003B3B50`) and of every numbered request (`0x003B1130`);
6. `0x02EBEF68` bit `0x1`, bits `0x400` and `0x800` of `0x020926E4`, the low three bits of `0x02F8F29E` and bit `0x1`
   of `0x02EBDBBC` are cleared, and `0x003AF330(0)` runs;
7. with `0x020926E4` bit `0x40` set it drops the bit and queues the target `0x020926D0` for release;
   last come the motion blur clear `0x0024EB20` and the cut-in clear `0x0024CEB0`.

Bit `0x2` of `+0x368` holds an instance: on such a step `0x0024B9B0` runs only `0x003A7EE0` and
`0x003A93F0` for it. The time stop sets it on the instances whose owner is a stopped actor
(`0x003B3BA0`, `0x003B1180`, through `0x0024FCA0`), and `0x0024FC80` releases them all with step 5 alone.

### Keeping the path objects

The instance's path-object list at `0x02EBEF98` (head `+0`, tail `+8`, links `+0xE8` back and `+0xF0`
forward) is emptied by `0x003A8000` when an instance is made; `0x003A81E0` frees every object, and
`0x003A8130(key, byte)` frees every object with that key and byte. `0x003A7EE0(dt)` clears bit `0x1` of
every object's byte `+0x103`, then runs the step `0x004FF0D0(object, dt)` on each object whose bit is
still clear.

### Emitter bookkeeping

The emitter block (instance `+0x1B8`, published at `0x02EBEF88`) keeps, from `+0x18`, 32 use counts of
8 bytes, ended by an id of −1:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | id (an emitter's +0x1C; -1 ends the table) |  |
| `+0x04` | `u8` | kind (an emitter's +0x13B) |  |
| `+0x05` | `u8` | bit 0x1: release pending |  |
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
`0x003A8FC0(tag)` returns whether any emitter has the tag. `0x003A8CE0(n)` sets bit `0x1` of `+0x248` on
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

When the record's byte `+0x2C4` has bits `0x3` equal to 2 a coin
(`0x003A6E60(2)`) can put the element at the tail; otherwise it goes to the head (`0x00441C14`–`0x00441C9F`).
It samples the record's spawn tracks into the emitter (`+0xA0`–`+0xF0`) and calls the birth
dispatcher `0x002F3BC0(element, emitter, age)` (`0x00441CA6`–`0x00441E71`).

`0x002F3BC0` bounds the element's type byte at `0xD1` and calls the type's birth method; every birth
method except type `0x70`'s calls the base birth `0x002F2D60`. Afterwards, unless `0x00314960()` is 0 or the cadence
test returns non-zero, it adds 1.0 to the age `+0x3C`; it stores `0x00250000()` at `+0x224` and clears
`+0x226` (`0x002F3E3F`–`0x002F3E73`).

`0x002F2D60` sets `+0x18` to the emitter record and `+0x20` to the definition, returning 0 when either
is missing (`0x002F2D6F`–`0x002F2DA2`). It clears bits `0x2` and `0x4` of `+1`, sets `+8` to the emitter and
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
4. With a lifetime set, once the whole age with bit `0x1` cleared exceeds it, fires the spawn slots with
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
| byte `+1` bit `0x1` | also cull when the point projected through `0x02AEECB0` is rejected or falls outside `0x6000`–`0xA000` on either screen word |

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

- bit `0x1` adds the parent's `+0xB0`, `+0xC0` and `+0xD0` vectors to the emitter's `+0x90`, `+0xA0`
  and `+0xB0`;
- bit `0x2` multiplies `+0xF4` by the parent's `+0x1F8` and adds `+0x1FC` and `+0x200` to `+0xF8` and
  `+0xFC`; bit `0x4` adds the parent's `+0x110` and `+0xF0` vectors to `+0xC0` and `+0xD0`;
- bit `0x8` multiplies `+0xE0`–`+0xE8` by the parent's `+0x120`–`+0x128`; bit `0x10` mixes the colour `+0xF0`
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
  `+0x1B4` when bit `0x2` of the bend's byte (`+0x221`, `+0x2A1`) is set.
- A step resolves the anchors with `0x003A56C0` and fails when one is missing. Subtypes 2 and 3 get
  each bend point from its curve (`0x004FE4E0`, records `+0x1F0` and `+0x270`) or from the fixed value
  (`0x004FE710`).
- Subtype 2 then moves along start, bend and end by the progress track `+0x270`, and subtype 3
  along start, both bends and end by `+0x2F0`, each part sized by its distance (`0x002F1D90`).
  `0x004FEAD0` turns the point into the object's matrix.
- The aim queries `0x00537C50`, `0x00537EE0`, `0x00537F40` and `0x00538780` hand the anchor at `+0xD0`,
  `+0xE0`, `+0x170` or `+0x160` to the anchor query `0x003A4290`, for the aim modes of `0x004FEAD0`.
- `0x004FF080(object)` resets a new object (`0x003A80A3`, `0x003A82E4`): it clears `+0x103` bit `0x1`, `+0x100` and
  `+0xE0` to `+0xFF`, then stores the answer of `0x00250000` in `+0x103` bit `0x2`.
- Every subtype's step starts with `0x004FE930(object, dt)` (`0x00537BC3`, `0x00537CE3`, `0x0053801F`, `0x005383DF`). It adds
  `dt` to the time `+0xF8`, takes the frame `+0xFC` as the whole time less the record's start `+0xC6`, and does
  nothing (returning 0) before the start or past the record's length `+0xC8` when that is not 0.
- Inside that window `0x004FE930` samples the record's tracks (`0x00430B90`): the point into `+0x80` (keeping the last
  one at `+0xC0` when the record's `+0xC3` is set), the track at record `+0x40` into `+0x90` and the one at `+0x80`
  into `+0xB0`, and sets `+0x103` bit `0x1`.
- `0x004FF1B0` and `0x004FF1F0` choose a query by the record's subtype `+0xC2` for `0x0052F560` (`0x0052F76A`, `0x0052F6B4`):
  `0x004FF1B0` calls `0x00537F10` for subtype 1 and `0x005382F0` for the others; `0x004FF1F0` calls `0x005382F0` for 0,
  `0x00537F70` for 1 and `0x00538320` for 2 and 3.

### Aiming an object

`0x004FEAD0(object, position)` sets a path object's orientation. It builds the object's matrix from its `+0x90` sample in
the record's kind `+0xC4` (`0x00398480`, `0x004FEAF9`). Unless the record's `+0xC5` is set, it then adds the position it is
given to the object's point `+0x80` (`0x004FEB12`-`0x004FEB92`). After that the record's aim mode `+0xC3` picks what the
object faces (`0x004FEB9C`-`0x004FEBCD`):

| Aim mode `+0xC3` | What the object faces |
|---|---|
| 1 | the point it kept at `+0xC0`, copied to the aim point `0x02CA80C0` (`0x004FEDF3`-`0x004FEDFA`) |
| 2 | the orientation of the anchor at `+0xD0` (`0x00537C50`), or at `+0xE0` for subtype 1 (`0x00537EE0`), copied into the aim matrix `0x02CA80D0` |
| 3 | the orientation of the anchor at `+0x170` for subtype 1 (`0x00537F40`), at `+0x160` for subtypes 2 and 3 (`0x00538780`), or at `+0xD0` for subtype 0 (`0x00537C50`), copied into `0x02CA80D0` |
| 4 | the point of the anchor at `+0xD0` (`0x005382F0`), or at `+0xE0` for subtype 1 (`0x00537F10`), written to `0x02CA80C0` |
| 5 | the point of the anchor at `+0xD0` for subtype 0 (`0x005382F0`), at `+0x170` for subtype 1 (`0x00537F70`), or at `+0x160` for subtypes 2 and 3 (`0x00538320`), written to `0x02CA80C0` |
| 0, or above 5 | nothing: the matrix stays as built (`0x004FEBCD`) |

- For modes 2 and 3 the anchor query `0x003A4290` writes the anchor's matrix into `0x02CA80D0`-`0x02CA810F`. `0x004FEAD0` then
  sets the last row `0x02CA8100` to `(0, 0, 0, 1)` from `0x008C5FD0`, which keeps the turn and drops the move (`0x004FECDF`,
  `0x004FED01`, `0x004FED23`, `0x004FED45`, `0x004FED81`, `0x004FEDA3`, `0x004FEDC5`, `0x004FEDE7`).
- For modes 1, 4 and 5 the point query `0x003A56F0` writes the anchor's point into `0x02CA80C0`, with its last lane set to
  1.0 (`0x003A5766`, `0x003A576B`), and adds the anchor's offsets to it.
- `0x004FEAD0` then subtracts the object's point from it, giving the aim vector: the point `+0x80`, or the position it
  was given when `+0xC5` is set (`0x004FEE02`-`0x004FEE85`). The difference goes through the vector cells
  `0x022D92E0`-`0x022D92EC` and is stored back in `0x02CA80C0` (`0x004FEE99`).
- The record's kind `+0xC4` then picks the builder (table at `0x004FF068`): `0x003A2690` for kinds 0 and 2, `0x003A2570` for
  1 and 4, `0x003A2440` for 3 and 5 (`0x004FEEB7`-`0x004FEF12`); a kind above 5 skips the builder and keeps the matrix as
  it stands (`0x004FEEAE`-`0x004FEEB1`).
- Each builder makes a rotation from the aim vector and the object's `+0xD0`. It normalises with `0x003A27C0` and
  crosses with `0x00398390`. An aim vector of 0 leaves the identity (`0x003A247A`, `0x003A24A3`). `0x004FEAD0` copies the
  result into `0x02CA80D0`-`0x02CA810F` (`0x004FEF17`-`0x004FEF3B`).
- In every mode from 1 to 5, `0x00397910(0x02CA80D0, object, object)` then combines the aim matrix with the object's
  matrix (`0x004FEF42`-`0x004FEF4F`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA80C0` | `vec` | 0 (zero-filled tail of `.data`) | the aim point, then the aim vector: an anchor's point (modes 4 and 5) or the kept point `+0xC0` (mode 1), less the object's point | `0x004FEAD0` (`0x004FEDFA`, `0x004FEE99`); `0x003A56F0` (`0x003A5766`, `0x003A576B`; adds at `0x003A5804`-`0x003A5825`, `0x003A5941`-`0x003A5958`, `0x003A667F`-`0x003A6690`, `0x003A6756`-`0x003A6787`, `0x003A6889`-`0x003A68AC`), through `0x003A56C0` from `0x005382F0`, `0x00537F10`, `0x00537F70` and `0x00538320` | `0x004FEAD0` (`0x004FEE09`); `0x003A2440` (`0x003A2473`, `0x003A247F`, `0x003A248D`, `0x003A2499`), `0x003A2570` (`0x003A25A3`, `0x003A25AF`, `0x003A25BD`, `0x003A25C9`), `0x003A2690` (`0x003A26C3`, `0x003A26CF`, `0x003A26DD`, `0x003A26E9`), through `0x004FEEDE`, `0x004FEEF8`, `0x004FEF12`; `0x003A56F0` (`0x003A57FF`-`0x003A581F`, `0x003A5930`-`0x003A593C`, `0x003A666E`-`0x003A668A`, `0x003A6717`, `0x003A6747`-`0x003A6781`, `0x003A6884`-`0x003A68A6`) |
| `0x02CA80D0` | `vec` | 0 (zero-filled tail of `.data`) | row 0 of the aim matrix | `0x004FEAD0` (`0x004FEF1A`); `0x003A4290` (`0x003A43BC`, `0x003A536B`, `0x003A5437`, `0x003A540C`, `0x003A540F`), through `0x00537C50`, `0x00537EE0`, `0x00537F40` and `0x00538780` | `0x00397910` (`0x00397966`, through `0x004FEF45`) |
| `0x02CA80E0` | `vec` | 0 (zero-filled tail of `.data`) | row 1 of the aim matrix | `0x004FEAD0` (`0x004FEF25`); `0x003A4290` (`0x003A43C3`, `0x003A5372`, `0x003A543E`, `0x003A5413`, `0x003A5417`), through the same four queries | `0x00397910` (`0x0039796E`, through `0x004FEF45`) |
| `0x02CA80F0` | `vec` | 0 (zero-filled tail of `.data`) | row 2 of the aim matrix | `0x004FEAD0` (`0x004FEF30`); `0x003A4290` (`0x003A43CB`, `0x003A537A`, `0x003A5446`, `0x003A541B`, `0x003A541F`), through the same four queries | `0x00397910` (`0x0039797F`, through `0x004FEF45`) |
| `0x02CA8100` | `vec` | 0 (zero-filled tail of `.data`) | row 3 of the aim matrix, the move: `(0, 0, 0, 1)` in modes 2 and 3 | `0x004FEAD0` (`0x004FEF3B`; `(0, 0, 0, 1)` at `0x004FECDF`, `0x004FED01`, `0x004FED23`, `0x004FED45`, `0x004FED81`, `0x004FEDA3`, `0x004FEDC5`, `0x004FEDE7`); `0x003A4290` (`0x003A43D3`, `0x003A43ED`, `0x003A5382`, `0x003A5423`, `0x003A5427`, `0x003A5454`, `0x003A5467`, `0x003A5489`, `0x003A54F1`, `0x003A54FC`, `0x003A5501`), through the same four queries | `0x003A4290` (`0x003A43DD`, `0x003A43E8`, `0x003A43F8`, `0x003A545E`, `0x003A5484`); `0x00397910` (`0x0039798E`, through `0x004FEF45`) |

### Timeline tracks

The instance's block at `+0x130` (`[0x02EBEFB0]`) holds sixteen timeline players. `0x003A7050` steps
each through `0x00332750` after the emitter step and frees a player whose step returns 0
(`0x00333350`, `0x003697F0`). A player's tracks are stepped by `0x0046E990(track, dt, slot)`, built from
the `0x600` record's sub-entries; a track's event list is at the sub-entry's `+0x20` (count byte
`+3`, 0 meaning 64), filled by `0x0046F380`, which frees the slot's old event first.

When the checks at `0x00332A07`-`0x00332A39` pass, the player step `0x00332750` sets bit `0x4` of the player's `+0x90` on the
first such step (`0x00332A61`). On later steps it counts the player's `+0xA0` up and returns 0 once the count reaches
the limit `0x02EC0F90`, so the player is freed (`0x00332A3B`-`0x00332A5C`). `0x02EC0F90` (`i32`, 0 at start, zero-filled
tail of `.data`) is set by `0x003333D0` (`0x003333E7`), which `0x001EDDC0` calls at `0x001EDE52`, to the frame-time factor
`0x01DFE0B8` times 30.0 (`0x008F8D80`), truncated and shifted left by 2: 120 in this build. `0x00332750` reads it at
`0x00332A52`.

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

An event's byte `+5` bit `0x1` enables it; with bits `0x6` equal to 1 it also needs bit `track byte
+0x10` of the instance's word `+0xC`.

- `0x004FF2C0(event, track)` dispatches on the subtype: 0 and 1 to `0x00538820`, 2 to `0x003B8670`, 3 to
  `0x005372D0`. `0x004FF320(event)` prepares a newly loaded event and returns the address after it:
  subtype 0 is `0x10` bytes, 1 goes to `0x005388F0` (`0x20`), 2 to `0x003B9FB0`, 3 to `0x005375B0`
  (`0x20`).
- `0x00538820` births the emitter record `+0x10` with definition `+0x12` once the track has reached
  the start `+8`; with bit `0x1` of `+0x14` the key gets the event byte in its high byte and
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
  `+1`–`+7` whose delay words (`+0x18`, `+0x1A`–`+0x24`) are 0 through `0x003331A0`, and, with bit `0x1`
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

### Moving the owner actor

Opcodes `0x1C` and `0x1D` of the battle effect program `0x003B8670` (cases `0x003B8EBD` and `0x003B8FB2`) move the actor
that owns the current instance: `0x003588B0` of the instance's `+0x08`, or of the slot-0 target `[0x02096A20]` when
`+0x378` bit `0x200` is set (`0x003B8EBD`-`0x003B8EDA`).

The first of them in an instance, while `+0x368` bit `0x80` is clear, saves the actor's position (`0x00265020` into `0x02092180`-`0x02092188`), its facing (`0x00265200`) and its `+0x08`
bit `0x8` and `+0x09` bit `0x40`, the bits `partyusecharhit` sets
([party verbs](../Scripts-And-Script-Commands/party-verbs.md)). It then calls `0x003B7E10(0)` unless `+0x368` bit
`0x100` is set, and sets bit `0x80` (`0x003B8EF2`-`0x003B8F68`).

- `0x1C` clears both actor bits (`0x0026A430(actor, 0)`, `0x003B8F74`), sets `0x02092190` to 1 and places the actor at the
  operand's floats `+0x04`, `+0x08` and `+0x0C` times 0.01 (`0x0026AF80`, `0x003B8F79`-`0x003B8F9E`).
- `0x1D` sets `0x02092190` to 1 and turns the actor to operand `+0x08` in degrees, `x 2 x π / 360` (`0x0026B5A0`,
  `0x003B9064`-`0x003B9081`).

`0x0024C6B0` puts the actor back. Opcode `0x1E` calls it (`0x003B9095`), `0x003A7360` calls it while `+0x368` bit `0x80` is
set (`0x003A73BD`), and `0x0024C870` calls it (`0x0024C8D4`).

1. It does nothing while bit `0x80` is clear.
2. It clears `0x02092190` and stops there while `0x020921B0` is non-zero (`0x0024C6C8`-`0x0024C6D9`).
3. It calls `0x003B7E10(1)`. When bit `0x100` is set it clears bit `0x80` and runs the target's restore `0x0024C870`
   first (`0x0024C704`-`0x0024C71A`).
4. It restores the two bits (`0x0026A430`, `0x0026A3A0`), the position (`0x0026AF80`) and the facing (`0x0026B5A0`)
   (`0x0024C74C`-`0x0024C793`), and clears bit `0x80`.

`0x0024C870` restores the target actor the same way from `0x020921A0`-`0x020921BC`, clearing `0x020921B0`. It stops while
`0x02092190` is non-zero (`0x0024C88D`-`0x0024C89E`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209218C` | `u32` | 0 (zero-filled tail) | the owner actor's saved `+0x08` bit `0x8` (`0x00263F70`); `0x0026A430` puts it back into `+0x08` bit `0x8` and `+0x09` bit `0x40` | `0x003B8670`: opcode `0x1C` (`0x003B8F33`), opcode `0x1D` (`0x003B9028`); `0x0024C970`, 0 (its `0x1670`-byte clear from `0x020910A0`, `0x0024C983`) | `0x0024C6B0` (`0x0024C74C`) |
| `0x02092190` | `u32` | 0 (zero-filled tail) | 1 once opcode `0x1C` or `0x1D` has moved the owner actor; while it is non-zero `0x0024C870` restores nothing | `0x003B8670`, 1: opcode `0x1C` (`0x003B8F79`), opcode `0x1D` (`0x003B9064`); `0x0024C6B0`, 0 (`0x0024C6CF`); `0x0024C970`, 0 (`0x0024C983`) | `0x0024C870` (`0x0024C88D`) |
| `0x02092194` | `f32` | 0 (zero-filled tail) | the owner actor's saved facing (`0x00265200`), restored with `0x0026B5A0` | `0x003B8670`: opcode `0x1C` (`0x003B8F23`), opcode `0x1D` (`0x003B9018`); `0x0024C970`, 0 (`0x0024C983`) | `0x0024C6B0` (`0x0024C788`) |
| `0x0209219C` | `u32` | 0 (zero-filled tail) | the owner actor's saved `+0x09` bit `0x40` (`0x00263E70`), restored with `0x0026A3A0` after `0x0209218C` | `0x003B8670`: opcode `0x1C` (`0x003B8F3E`), opcode `0x1D` (`0x003B9033`); `0x0024C970`, 0 (`0x0024C983`) | `0x0024C6B0` (`0x0024C75A`) |

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

## Layouts

Effect instance (`0x3B0`, `0x0024B270`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8` | kind (the group and the list 0x020910F0[kind]) |  |
| `+0x120` | `...` | block published at 0x02EBEF98 |  |
| `+0x130` | `...` | block published at 0x02EBEFB0 |  |
| `+0x1B8` | `u32` | frame stamp |  |
| `+0x1C0` | `...` | first emitter |  |
| `+0x2E0` | `...` | cull record (first byte 0xFF: use the definition's) |  |
| `+0x340` | `void*` | effect context |  |
| `+0x348` | `void*` | next |  |
| `+0x350` | `...` | previous |  |
| `+0x36A` | `u8` | flags: bit 0x1 draws every emitter |  |
| `+0x378` | `u16` | high nibble: display layer |  |
| `+0x3A8` | `u16` | stamp from 0x00181DD0() |  |

Emitter:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x008` | `void*` | next emitter |  |
| `+0x024` | `u32` | births |  |
| `+0x028` | `u32` | emission limit (frames) |  |
| `+0x02C` | `f32` | age |  |
| `+0x030` | `i32` | whole frame |  |
| `+0x034` | `f32` | last firing |  |
| `+0x0A0-0x0F0` | `...` | sampled spawn values (+0x0F0 colour) |  |
| `+0x100` | `void*` | emitter record (0x800) |  |
| `+0x108` | `...` | element definition (0xA00) |  |
| `+0x118` | `void*` | active head |  |
| `+0x120` | `...` | free head |  |
| `+0x128` | `...` | active tail |  |
| `+0x130` | `void*` | parent element |  |
| `+0x139` | `u8` | stop emitting |  |

Element:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8` | type (from definition +0x44) |  |
| `+0x001` | `u8` | flags: bit 0x1 draw skip |  |
| `+0x002` | `u16` | draw counter |  |
| `+0x008` | `void*` | emitter |  |
| `+0x010` | `...` | parent |  |
| `+0x018` | `...` | emitter record |  |
| `+0x020` | `...` | definition |  |
| `+0x028` | `void*` | previous |  |
| `+0x030` | `...` | next |  |
| `+0x038` | `u32` | frame stamp at the last update |  |
| `+0x03C` | `f32` | age |  |
| `+0x040` | `i32` | whole age |  |
| `+0x044` | `i32` | track frame |  |
| `+0x048` | `i32` | updates |  |
| `+0x04C` | `i32` | lifetime (0 none) |  |
| `+0x060` | `...` | position |  |
| `+0x1D0` | `i32[8]` | last firing per spawn slot (-1 unfired) |  |
| `+0x1F0` | `u32` | colour (0x80808080 neutral) |  |
| `+0x224` | `u16` | hold word from 0x00250000() |  |

## Operations

Per simulation step, one emitter step per emitter of the seven updated kinds, and one base update
per live element.

## State

The instance lists `0x020910F0`, the current instance `0x02F97348` and context `0x02F97340`, the table
pointers `0x02EBEF70`–`0x02EBEFB0` and the current emitter `0x02EBEF80`.

The draw state `0x0024FCF0` publishes is the start of a block, `0x02096800`-`0x02096D2B`, that the start-up reset
`0x00259250` returns to its boot values ([start-up constants](../Engine-Core/startup-constants.md)). Other
pages name other words of it: the effect program's flags `0x020968C8`
([effect file loading](effect-file-loading.md)), the target slots `0x02096A20`-`0x02096B34`
([effect anchors and targets](effect-anchors-and-targets.md)), and the chunk words `0x02096B40` and `0x02096BA4`
([effect files](effect-files-efx-efb.md)).

The scale is `0x02096810`-`0x0209681C`. `0x0024FCF0` copies the instance's
`+0x320` into it and multiplies it by `+0x39C` (`0x003A2B20`, `0x0024FD0B`-`0x0024FD29`). It then sets w to 1.0
(`0x0024FD3B`), as `0x0024C060` also does (`0x0024C212`). The rows give the words this page owns:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02096814` | `f32` | 0 (zero-filled tail) | the scale's y: `0x0024C060` scales the effect matrix `0x02AEEA20` by it (`0x0039ADE0`, called at `0x0024C21A`), and the anchor queries divide a point's y by it | `0x0024FCF0` (`0x0024FD12`, 16 bytes, then `0x003A2B20` at `0x003A2B51`); `0x00259250`, 1.0 (`0x00259303`) | `0x003A2B20` (`0x003A2B26`, from `0x0024FD29`); `0x0039ADE0` (`0x0039AE19`-`0x0039AE4B`, from `0x0024C21A`); `0x003A4290` (`0x003A456F`, `0x003A479E`); `0x003A56F0` (`0x003A5914`, `0x003A5B3E`) |
| `0x02096818` | `f32` | 0 (zero-filled tail) | the scale's z, used the same way | `0x0024FCF0` (`0x0024FD12`; `0x003A2B51`); `0x00259250`, 1.0 (`0x0025930D`) | `0x003A2B20` (`0x003A2B26`); `0x0039ADE0` (`0x0039AE5A`-`0x0039AE82`); `0x003A4290` (`0x003A4581`, `0x003A47AB`); `0x003A56F0` (`0x003A5922`, `0x003A5B52`) |
| `0x02096844` | `u8` | 0 (zero-filled tail) | the byte after the word `0x02096840`, which `0x0024FCF0` sets from the instance's `+0x330`; the reset sets it to 0 | `0x00259250`, 0 (`0x00259358`) | no instruction names it |
| `0x02096884` | `u8[8]` | 0 (zero-filled tail) | eight bytes the reset sets to `00 10 01 01 00 00 00 00`. Byte `0x02096885` (`0x10`) and `0x0209688C` decide whether the `0x42` pool's step `0x003D8190` runs after the effect updates. Byte `0x02096887` (1) makes the effect-camera chunk submit the camera record `0x02096D30` | `0x00259250` (`0x00259295`, one 8-byte store) | `0x00258D70` (`0x00258E1B`, `0x02096885`); `0x00258E40` (`0x00258E8A`, `0x02096885`); `0x003ED8A0` (`0x003ED965`, `0x02096887`) |
| `0x0209688C` | `u8` | 0 (zero-filled tail) | with the low nibble of `0x02096885`: the field step and the menu step run `0x003D8190` when that nibble is 0 or this byte is non-zero (`0x00258E1B`-`0x00258E2D`, `0x00258E8A`-`0x00258EA0`); the reset leaves the nibble 0 | `0x00259250`, 0 (`0x002592F3`) | `0x00258D70` (`0x00258E24`); `0x00258E40` (`0x00258E93`) |
| `0x0209688E` | `u32` | 0 (zero-filled tail) | set to 0 by the reset | `0x00259250` (`0x002592A0`) | no instruction names it |
| `0x02096892` | `u32` | 0 (zero-filled tail) | set to `0x200` by the reset | `0x00259250` (`0x002592AA`) | no instruction names it |
| `0x02096896` | `u16` | 0 (zero-filled tail) | set to `0x8040` by the reset | `0x00259250` (`0x002592B4`) | no instruction names it |
| `0x020968A0` | `f32[4]` | 0 (zero-filled tail) | set to (0, 0, 0, 1.0) from `0x008C5FD0` by the reset | `0x00259250` (`0x00259269`) | no instruction names it |
| `0x020968B4` | `u32` | 0 (zero-filled tail) | set to `0x80000080` by the reset, after the neutral colour `0x020968B0` | `0x00259250` (`0x002592C7`) | no instruction names it |
| `0x020968B8` | `u16` | 0 (zero-filled tail) | set to 1 by the reset | `0x00259250` (`0x002592D1`) | no instruction names it |
| `0x020968E8` | `u32` | 0 (zero-filled tail) | set to 0 by the reset | `0x00259250` (`0x002592E6`) | no instruction names it |
| `0x020968EC` | `u16` | 0 (zero-filled tail) | set to 0 by the reset | `0x00259250` (`0x002592EC`) | no instruction names it |
| `0x020968EE` | `u8` | 0 (zero-filled tail) | set to 0 by the reset | `0x00259250` (`0x002592E0`) | no instruction names it |
| `0x020969F0` | `u32` | 0 (zero-filled tail) | set to 0 by the reset | `0x00259250` (`0x00259317`) | no instruction names it |
| `0x020969F8` | `u32` | 0 (zero-filled tail) | set to 0 by the reset | `0x00259250` (`0x0025931D`) | no instruction names it |
| `0x02096A00` | `u32` | 0 (zero-filled tail) | set to 0 by the reset | `0x00259250` (`0x00259323`) | no instruction names it |
| `0x02096A08` | `u32` | 0 (zero-filled tail) | set to 0 by the reset, below the target count `0x02096A20` | `0x00259250` (`0x00259329`) | no instruction names it |
| `0x02096B3C` | `u32` | 0 (zero-filled tail) | set to 0 by the reset, below the chunk word `0x02096B40` | `0x00259250` (`0x0025932F`) | no instruction names it |
| `0x02096BA0` | `u32` | 0 (zero-filled tail) | set to 0 by the reset, whose 8-byte store also clears the chunk word `0x02096BA4` ([effect files](effect-files-efx-efb.md), written by `0x003EE2D0` at `0x003EE319`, `0x003EE378`, `0x003EE395`) | `0x00259250` (`0x00259335`, 8 bytes) | no instruction names it |
| `0x02096BA8` | `u32` | 0 (zero-filled tail) | set to 0 by the reset | `0x00259250` (`0x0025933C`) | no instruction names it |
| `0x02096C60` | `u8` | 0 (zero-filled tail) | flags; the reset clears bit `0x1` and keeps the rest | `0x00259250` (`0x00259260`) | `0x00259250` (`0x00259260`, the same `and`) |
| `0x02096C78` | `u32` | 0 (zero-filled tail) | set to 0 by the reset | `0x00259250` (`0x00259352`) | no instruction names it |
| `0x02096D21` | `u8` | 0 (zero-filled tail) | set to 0 by the reset | `0x00259250` (`0x00259342`) | no instruction names it |
| `0x02096D24` | `f32` | 0 (zero-filled tail) | set to 0.0 by the reset, before `0x02096D28` = 1 | `0x00259250` (`0x00259285`) | no instruction names it |
| `0x02F8F320` | `u32` | 0 (zero-filled tail) | set to 1 by the field step `0x00258D70` and the menu step `0x00258E40` before they update the effects | `0x00258D70`, 1 (`0x00258DC1`, `edi` = 1 from `0x00258D95`); `0x00258E40`, 1 (`0x00258E74`) | no instruction names it |

The kind lists `0x020910F0[kind]` are eight-byte heads, cleared with the rest of `0x020910A0`-`0x0209270F` by `0x0024C970`
(`0x0024C983`, and the 8-byte stores `0x0024C9F0`-`0x0024CA05`). The head of kind 3 is also read by name:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02091108` | `void*` | 0 (zero-filled tail) | the head of the kind-3 list, `0x020910F0[3]`; the frame's draw setup `0x0024D540` takes its first instance, makes that instance's context `+0x340` current at `0x02F97340` and the instance itself `0x02F97348` (`0x0024D573`-`0x0024D5A0`) | `0x0024C970` (`0x0024CA05`, `0x0024C983`); as the head of kind `kind`: `0x0024B270` (`0x0024B35A`), `0x0024C3C0` (`0x0024C3FB`), `0x0024C460` (`0x0024C531`), `0x0024DB80` (`0x0024DBF1`), `0x0024E7D0` (`0x0024E841`), `0x0024F4D0` (`0x0024F540`), each through `0x020910A0` + `0x50`; the unlinks `0x0024EE10` (`0x0024EE32`) and `0x0024EE60` (`0x0024EEA5`, through the head's address `0x0024EE72`) | `0x0024D540` (`0x0024D573`); as the head of kind `kind`: `0x0024B270` (`0x0024B324`), `0x0024C3C0` (`0x0024C3CD`), `0x0024C460` (`0x0024C47A`), `0x0024DB80` (`0x0024DBAA`), `0x0024E7D0` (`0x0024E7FA`), `0x0024F4D0` (`0x0024F4FA`), through `0x020910A0` + `0x50`; `0x0024B9B0` (`0x0024BA12`), `0x0024D050` (`0x0024D070`, walking every head from `0x0024D05F`), `0x0024D370` (`0x0024D38B`), `0x0024E210` (`0x0024E225`), `0x0024E2F0` (`0x0024E313`), `0x0024E6D0` (`0x0024E6F6`), `0x0024EE60` (`0x0024EE76`), `0x0024F680` (`0x0024F696`), `0x0024F8D0` (`0x0024F8E1`), `0x0024F920` (`0x0024F938`), `0x0024FDA0` (`0x0024FDBF`) |
| `0x020910B0` | `void*` | 0 (zero-filled tail) | `0x020910A0[2]`, the head of the kind-2 context list (a context's kind is its byte `+0`) | `0x0024C970`, 0 (`0x0024C983`, the `0x1670`-byte clear; `0x0024C9B8`); `0x0024B3A0` (`0x0024B457`); `0x0024F410` (`0x0024F438`); `0x0024C550`, 0 (`0x0024C5C1`) | `0x0024B3A0` (`0x0024B438`); `0x0024F610` (`0x0024F61F`); `0x0024C550` (`0x0024C5A0`); `0x0024C640` (`0x0024C658`, which walks kinds 1 to 7) |
| `0x020910B8` | `void*` | 0 (zero-filled tail) | `0x020910A0[3]`, the head of the kind-3 context list (a context's kind is its byte `+0`) | `0x0024C970`, 0 (`0x0024C983`, the `0x1670`-byte clear; `0x0024C9BF`); `0x0024B3A0` (`0x0024B457`); `0x0024F410` (`0x0024F438`); `0x0024C550`, 0 (`0x0024C5C1`) | `0x0024B3A0` (`0x0024B438`); `0x0024F610` (`0x0024F61F`); `0x0024C550` (`0x0024C5A0`); `0x0024C640` (`0x0024C658`, which walks kinds 1 to 7) |
| `0x020910C0` | `void*` | 0 (zero-filled tail) | `0x020910A0[4]`, the head of the kind-4 context list (a context's kind is its byte `+0`) | `0x0024C970`, 0 (`0x0024C983`, the `0x1670`-byte clear; `0x0024C9C6`); `0x0024B3A0` (`0x0024B457`); `0x0024F410` (`0x0024F438`); `0x0024C550`, 0 (`0x0024C5C1`) | `0x0024B3A0` (`0x0024B438`); `0x0024F610` (`0x0024F61F`); `0x0024C550` (`0x0024C5A0`); `0x0024C640` (`0x0024C658`, which walks kinds 1 to 7) |
| `0x020910C8` | `void*` | 0 (zero-filled tail) | `0x020910A0[5]`, the head of the kind-5 context list (a context's kind is its byte `+0`) | `0x0024C970`, 0 (`0x0024C983`, the `0x1670`-byte clear; `0x0024C9CD`); `0x0024B3A0` (`0x0024B457`); `0x0024F410` (`0x0024F438`); `0x0024C550`, 0 (`0x0024C5C1`) | `0x0024B3A0` (`0x0024B438`); `0x0024F610` (`0x0024F61F`); `0x0024C550` (`0x0024C5A0`); `0x0024C640` (`0x0024C658`, which walks kinds 1 to 7) |
| `0x020910D0` | `void*` | 0 (zero-filled tail) | `0x020910A0[6]`, the head of the kind-6 context list (a context's kind is its byte `+0`) | `0x0024C970`, 0 (`0x0024C983`, the `0x1670`-byte clear; `0x0024C9D4`); `0x0024B3A0` (`0x0024B457`); `0x0024F410` (`0x0024F438`); `0x0024C550`, 0 (`0x0024C5C1`) | `0x0024B3A0` (`0x0024B438`); `0x0024F610` (`0x0024F61F`); `0x0024C550` (`0x0024C5A0`); `0x0024C640` (`0x0024C658`, which walks kinds 1 to 7) |
| `0x020910D8` | `void*` | 0 (zero-filled tail) | `0x020910A0[7]`, the head of the kind-7 context list (a context's kind is its byte `+0`) | `0x0024C970`, 0 (`0x0024C983`, the `0x1670`-byte clear; `0x0024C9DB`); `0x0024B3A0` (`0x0024B457`); `0x0024F410` (`0x0024F438`); `0x0024C550`, 0 (`0x0024C5C1`) | `0x0024B3A0` (`0x0024B438`); `0x0024F610` (`0x0024F61F`); `0x0024C550` (`0x0024C5A0`); `0x0024C640` (`0x0024C658`, which walks kinds 1 to 7) |
| `0x020910E0` | `void*` | 0 (zero-filled tail) | `0x020910A0[8]`, the head of the kind-8 context list (a context's kind is its byte `+0`) | `0x0024C970`, 0 (`0x0024C983`, the `0x1670`-byte clear; `0x0024C9E2`); `0x0024B3A0` (`0x0024B457`); `0x0024F410` (`0x0024F438`); `0x0024C550`, 0 (`0x0024C5C1`) | `0x0024B3A0` (`0x0024B438`); `0x0024F610` (`0x0024F61F`); `0x0024C550` (`0x0024C5A0`) |
| `0x020910E8` | `void*` | 0 (zero-filled tail) | `0x020910A0[9]`, the head of the kind-9 context list (a context's kind is its byte `+0`) | `0x0024C970`, 0 (`0x0024C983`, the `0x1670`-byte clear; `0x0024C9E9`); `0x0024B3A0` (`0x0024B457`); `0x0024F410` (`0x0024F438`); `0x0024C550`, 0 (`0x0024C5C1`) | `0x0024B3A0` (`0x0024B438`); `0x0024F610` (`0x0024F61F`); `0x0024C550` (`0x0024C5A0`) |
| `0x02091100` | `void*` | 0 (zero-filled tail) | `0x020910F0[2]`, the head of the kind-2 instance list (linked through `+0x348` / `+0x350`) | `0x0024C970`, 0 (`0x0024C983`; `0x0024C9FE`); `0x0024B270` (`0x0024B35A`); `0x0024C3C0` (`0x0024C3FB`); `0x0024C460` (`0x0024C531`); `0x0024DB80` (`0x0024DBF1`); `0x0024E7D0` (`0x0024E841`); `0x0024F4D0` (`0x0024F540`); `0x0024EE10` (`0x0024EE32`); `0x0024EE60` (`0x0024EEA5`, through the entry's address) | `0x0024B270` (`0x0024B324`); `0x0024B9B0` (`0x0024BA12`); `0x0024C3C0` (`0x0024C3CD`); `0x0024C460` (`0x0024C47A`); `0x0024D050` (`0x0024D070`, every kind in turn); `0x0024D370` (`0x0024D38B`); `0x0024DB80` (`0x0024DBAA`); `0x0024E210` (`0x0024E225`); `0x0024E2F0` (`0x0024E313`); `0x0024E6D0` (`0x0024E6F6`); `0x0024E7D0` (`0x0024E7FA`); `0x0024EE60` (`0x0024EE76`); `0x0024F4D0` (`0x0024F4FA`); `0x0024F680` (`0x0024F696`); `0x0024F8D0` (`0x0024F8E1`); `0x0024F920` (`0x0024F938`); `0x0024FDA0` (`0x0024FDBF`) |
| `0x02091110` | `void*` | 0 (zero-filled tail) | `0x020910F0[4]`, the head of the kind-4 instance list (linked through `+0x348` / `+0x350`) | `0x0024C970`, 0 (`0x0024C983`; `0x0024CA0C`); `0x0024B270` (`0x0024B35A`); `0x0024C3C0` (`0x0024C3FB`); `0x0024C460` (`0x0024C531`); `0x0024DB80` (`0x0024DBF1`); `0x0024E7D0` (`0x0024E841`); `0x0024F4D0` (`0x0024F540`); `0x0024EE10` (`0x0024EE32`); `0x0024EE60` (`0x0024EEA5`, through the entry's address) | `0x0024B270` (`0x0024B324`); `0x0024B9B0` (`0x0024BA12`); `0x0024C3C0` (`0x0024C3CD`); `0x0024C460` (`0x0024C47A`); `0x0024D050` (`0x0024D070`, every kind in turn); `0x0024D370` (`0x0024D38B`); `0x0024DB80` (`0x0024DBAA`); `0x0024E210` (`0x0024E225`); `0x0024E2F0` (`0x0024E313`); `0x0024E6D0` (`0x0024E6F6`); `0x0024E7D0` (`0x0024E7FA`); `0x0024EE60` (`0x0024EE76`); `0x0024F4D0` (`0x0024F4FA`); `0x0024F680` (`0x0024F696`); `0x0024F8D0` (`0x0024F8E1`); `0x0024F920` (`0x0024F938`); `0x0024FDA0` (`0x0024FDBF`) |
| `0x02091118` | `void*` | 0 (zero-filled tail) | `0x020910F0[5]`, the head of the kind-5 instance list (linked through `+0x348` / `+0x350`) | `0x0024C970`, 0 (`0x0024C983`; `0x0024CA13`); `0x0024B270` (`0x0024B35A`); `0x0024C3C0` (`0x0024C3FB`); `0x0024C460` (`0x0024C531`); `0x0024DB80` (`0x0024DBF1`); `0x0024E7D0` (`0x0024E841`); `0x0024F4D0` (`0x0024F540`); `0x0024EE10` (`0x0024EE32`); `0x0024EE60` (`0x0024EEA5`, through the entry's address) | `0x0024B270` (`0x0024B324`); `0x0024B9B0` (`0x0024BA12`); `0x0024C3C0` (`0x0024C3CD`); `0x0024C460` (`0x0024C47A`); `0x0024D050` (`0x0024D070`, every kind in turn); `0x0024D370` (`0x0024D38B`); `0x0024DB80` (`0x0024DBAA`); `0x0024E210` (`0x0024E225`); `0x0024E2F0` (`0x0024E313`); `0x0024E6D0` (`0x0024E6F6`); `0x0024E7D0` (`0x0024E7FA`); `0x0024EE60` (`0x0024EE76`); `0x0024F4D0` (`0x0024F4FA`); `0x0024F680` (`0x0024F696`); `0x0024F8D0` (`0x0024F8E1`); `0x0024F920` (`0x0024F938`); `0x0024FDA0` (`0x0024FDBF`) |
| `0x02091120` | `void*` | 0 (zero-filled tail) | `0x020910F0[6]`, the head of the kind-6 instance list (linked through `+0x348` / `+0x350`) | `0x0024C970`, 0 (`0x0024C983`; `0x0024CA1A`); `0x0024B270` (`0x0024B35A`); `0x0024C3C0` (`0x0024C3FB`); `0x0024C460` (`0x0024C531`); `0x0024DB80` (`0x0024DBF1`); `0x0024E7D0` (`0x0024E841`); `0x0024F4D0` (`0x0024F540`); `0x0024EE10` (`0x0024EE32`); `0x0024EE60` (`0x0024EEA5`, through the entry's address) | `0x0024B270` (`0x0024B324`); `0x0024B9B0` (`0x0024BA12`); `0x0024C3C0` (`0x0024C3CD`); `0x0024C460` (`0x0024C47A`); `0x0024D050` (`0x0024D070`, every kind in turn); `0x0024D370` (`0x0024D38B`); `0x0024DB80` (`0x0024DBAA`); `0x0024E210` (`0x0024E225`); `0x0024E2F0` (`0x0024E313`); `0x0024E6D0` (`0x0024E6F6`); `0x0024E7D0` (`0x0024E7FA`); `0x0024EE60` (`0x0024EE76`); `0x0024F4D0` (`0x0024F4FA`); `0x0024F680` (`0x0024F696`); `0x0024F8D0` (`0x0024F8E1`); `0x0024F920` (`0x0024F938`); `0x0024FDA0` (`0x0024FDBF`) |
| `0x02091130` | `void*` | 0 (zero-filled tail) | `0x020910F0[8]`, the head of the kind-8 instance list (linked through `+0x348` / `+0x350`) | `0x0024C970`, 0 (`0x0024C983`; `0x0024CA28`); `0x0024B270` (`0x0024B35A`); `0x0024C3C0` (`0x0024C3FB`); `0x0024C460` (`0x0024C531`); `0x0024DB80` (`0x0024DBF1`); `0x0024E7D0` (`0x0024E841`); `0x0024F4D0` (`0x0024F540`); `0x0024EE10` (`0x0024EE32`); `0x0024EE60` (`0x0024EEA5`, through the entry's address) | `0x0024B270` (`0x0024B324`); `0x0024B9B0` (`0x0024BA12`); `0x0024C3C0` (`0x0024C3CD`); `0x0024C460` (`0x0024C47A`); `0x0024D050` (`0x0024D070`, every kind in turn); `0x0024D370` (`0x0024D38B`); `0x0024DB80` (`0x0024DBAA`); `0x0024E210` (`0x0024E225`); `0x0024E2F0` (`0x0024E313`); `0x0024E6D0` (`0x0024E6F6`); `0x0024E7D0` (`0x0024E7FA`); `0x0024EE60` (`0x0024EE76`); `0x0024F4D0` (`0x0024F4FA`); `0x0024F680` (`0x0024F696`); `0x0024F8D0` (`0x0024F8E1`); `0x0024F920` (`0x0024F938`); `0x0024FDA0` (`0x0024FDBF`) |
| `0x02091138` | `void*` | 0 (zero-filled tail) | `0x020910F0[9]`, the head of the kind-9 instance list (linked through `+0x348` / `+0x350`) | `0x0024C970`, 0 (`0x0024C983`; `0x0024CA2F`); `0x0024B270` (`0x0024B35A`); `0x0024C3C0` (`0x0024C3FB`); `0x0024C460` (`0x0024C531`); `0x0024DB80` (`0x0024DBF1`); `0x0024E7D0` (`0x0024E841`); `0x0024F4D0` (`0x0024F540`); `0x0024EE10` (`0x0024EE32`); `0x0024EE60` (`0x0024EEA5`, through the entry's address) | `0x0024B270` (`0x0024B324`); `0x0024B9B0` (`0x0024BA12`); `0x0024C3C0` (`0x0024C3CD`); `0x0024C460` (`0x0024C47A`); `0x0024D050` (`0x0024D070`, every kind in turn); `0x0024D370` (`0x0024D38B`); `0x0024DB80` (`0x0024DBAA`); `0x0024E210` (`0x0024E225`); `0x0024E2F0` (`0x0024E313`); `0x0024E6D0` (`0x0024E6F6`); `0x0024E7D0` (`0x0024E7FA`); `0x0024EE60` (`0x0024EE76`); `0x0024F4D0` (`0x0024F4FA`); `0x0024F680` (`0x0024F696`); `0x0024F8D0` (`0x0024F8E1`); `0x0024F920` (`0x0024F938`); `0x0024FDA0` (`0x0024FDBF`) |
| `0x02091148` | `void*` | 0 (zero-filled tail) | entry 1 of the effect callback table `0x02091140`. `0x0024F780(n, f)` stores entry `n`, and its one caller `0x0036E310` passes 0 | `0x0024C970`, 0 (`0x0024C983`; `0x0024CAD6`); `0x0024F780` (`0x0024F78A`, entry `n`) | no instruction names it |
| `0x0209216C` | `u16` | 0 (zero-filled tail) | the word after the two queue counts `0x02092168` (blocks at `0x02091150`) and `0x0209216A` (render targets at `0x02091950`), cleared by the effect init | `0x0024C970`, 0 (`0x0024C983`; `0x0024CA80`) | no instruction names it |
| `0x020925C0` | `u8` | 0 (zero-filled tail) | cleared by the effect init | `0x0024C970`, 0 (`0x0024C983`; `0x0024CADD`) | no instruction names it |
| `0x020925D0` | `u64` | 0 (zero-filled tail) | cleared by the effect init | `0x0024C970`, 0 (`0x0024C983`; `0x0024CAE3`) | no instruction names it |

## Modding notes

- An element that leaves its cull window is released at once, and its trigger-2 children stop.
  Death bursts belong in tag-3 slots, which fire on the lifetime end.
- The lifetime test uses the whole age with bit `0x1` cleared, so a lifetime is effectively rounded to
  an even frame count.

## Related

- [Effect drawing](effect-drawing.md): the display layers and the draw list.
- [Effect anchors and targets](effect-anchors-and-targets.md): anchor queries and target slots.
- [Effect file loading](effect-file-loading.md): battle effect slots and the loaded-file queue.
- [Effects on actors and scripts](effects-on-actors-and-scripts.md): numbered effects on actors and script effect slots.
- [Effect files](effect-files-efx-efb.md): the chunk streams the records come from.
- [Effect element types](effect-element-types.md): what each type does in its methods.
- [Resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md):
  contexts, instances and their teardown.
- [Authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md): the tracks the
  emitters and elements sample.
- [Frame update order](../Engine-Core/frame-update-order.md): where the update pass runs.
- [Global state accessors](../Engine-Core/global-state-accessors.md): the cadence test
  `0x001EDDA0`.
