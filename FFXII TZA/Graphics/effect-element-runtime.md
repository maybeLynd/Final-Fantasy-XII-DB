---
title: "Effect element runtime: instances, emitters and elements, the per-step update, birth, release and child spawns, and the six display layers"
kind: "system"
category: "Graphics"
addresses: "0024B270, 020910F0, 02F97348, 02EBEF88, 0024ED80, 00258D70, 0024B9B0, 003A7050, 003A8390, 0043EF40, 00441B30, 002F3BC0, 002F2D60, 002F3910, 002F2530, 002F4020, 005004C0, 002F31C0, 005002E0, 003A8950, 003A8AE0, 00258EE0, 00259030, 0024D370, 0024D4E0, 00441970, 02AEE910, 02F8F2F8, 02F8F2C6, 003A3740, 003A3A00, 0024D540"
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

- An effect instance, `3B0`<sub>h</sub> bytes made by `0024B270(template)` from a template. Its byte `+0` is
  its kind; it is linked at the head of `020910F0[kind]` through `+348`<sub>h</sub> / `+350`<sub>h</sub>, stamped with
  `00181DD0()` at `+3A8`<sub>h</sub>, and made current (`0024B270`–`0024B385`).
- An emitter, on the list whose block is the instance's `+1B8`<sub>h</sub> (first node at `+8`, next at
  node `+8`). Its `+100`<sub>h</sub> is an `800`<sub>h</sub> emitter record and its `+108`<sub>h</sub> an `A00`<sub>h</sub> element
  definition.
- An element, on its emitter's active list (head `+118`<sub>h</sub>, tail `+128`<sub>h</sub>, element links `+28`<sub>h</sub>
  back and `+30`<sub>h</sub> forward) or free list `+120`<sub>h</sub>.

### Making an instance current

`0024ED80(instance)` publishes the instance at `02F97348` and its context (`+340`<sub>h</sub>) at
`02F97340`, then the context's record tables and the instance's lists: `02EBEF70` = context
`+18`<sub>h</sub> (the `B00`<sub>h</sub> record store), `02EBEFA8` = `+38`<sub>h</sub>, `02EBEFA0` = `+840`<sub>h</sub>, `02EBEF90` = `+848`<sub>h</sub>
(emitter records), `02EBEF78` = `+850`<sub>h</sub> (definitions), `02EBEF98` = instance `+120`<sub>h</sub>, `02EBEFB0` =
`+130`<sub>h</sub> and `02EBEF88` = `+1B8`<sub>h</sub> (`0024ED80`–`0024EDFF`). All the code below reads these globals.

### The element pool

`0043F450(emitter, record, definition, …)` resets the emitter with `0043F210`, which frees its old
pool `+110`<sub>h</sub> and clears its counters, lists and flags (byte `+138`<sub>h</sub> keeps bits 0–1 set and bit 2
clear). It then allocates one block of `+20`<sub>h</sub> elements, the count from emitter-record word
`+2B2`<sub>h</sub>, links them into the free list `+120`<sub>h</sub> and stamps each with the definition's type.

The element size depends on the type. `0043F450` handles the main range with `0036A230`; its
default arm passes the sub-range types to `004FF440`, which uses `0036A190` and returns 1 for a type
it does not know (`004FF440`):

| Sub-range type | Element bytes |
|---|---|
| `42`<sub>h</sub>, `A4`<sub>h</sub>, `A7`<sub>h</sub>, `AA`<sub>h</sub> | `240`<sub>h</sub> |
| `A6`<sub>h</sub>, `A8`<sub>h</sub>, `A9`<sub>h</sub> | `260`<sub>h</sub> |
| `AB`<sub>h</sub> | `2B0`<sub>h</sub> |
| `A3`<sub>h</sub> | `2C0`<sub>h</sub> |
| `70`<sub>h</sub> | `310`<sub>h</sub> |
| `6A`<sub>h</sub> | `320`<sub>h</sub> |
| `73`<sub>h</sub> | `3B0`<sub>h</sub> |
| `6B`<sub>h</sub> | `3E0`<sub>h</sub> |
| `72`<sub>h</sub>, `74`<sub>h</sub> | `400`<sub>h</sub> |
| `71`<sub>h</sub> | `440`<sub>h</sub> |
| `68`<sub>h</sub> | `4D0`<sub>h</sub> |
| `69`<sub>h</sub> | `AD0`<sub>h</sub> |

### The update pass

In the field frame, each simulation step runs `00258D70` ([frame update
order](../Engine-Core/frame-update-order.md)). It calls `0024B9B0(0, kind)` for kind 2
when a map bank is loaded (`00258DC7` → `0026F9D0`), then for the kinds 3, 5, 6, 9, 1, 7 and 4 in
that order (`00258DCC`–`00258E0C`); the menu frame's `00258E40` runs kind 3 alone.

`0024B9B0`
refuses kind 8, walks `020910F0[kind]` through `+348`<sub>h</sub>, skips an instance whose `+3A8`<sub>h</sub> differs
from `00181DD0()`, makes each current (`0024BB6D`) and updates it through `003A7050`
(`0024B9C8`, `0024BA12`–`0024BA65`, `0024BC16`, `0024BE28`).

### Starting and ending an instance

The instance's state byte `+370`<sub>h</sub> picks what `0024B9B0` does with it after making it current:

- 2 and 8 start it with `003A74F0(+373h)` and set state 1.
- 1 runs `003A7EE0` and then the update `003A7050`; when the update returns 0 the instance ends
  through `003A7300`. On steps where the pass holds the instance, state 1 runs only `003A7EE0` and
  `003A93F0`.
- 6 runs like 1 but moves to 4 when the update returns 0, and 4 starts the instance again with
  `003A74F0`.

The states that update the instance, and the group draw, first rebuild the effect matrices with
`0024C060`. One step of it is `0039D480(view)`, with the view `02AEDEF0`, or `02AEE9E0` in a kind-4
instance: it keeps the 64 bytes at `02AEEAA0`, turns the unit z vector by the view's rotation
(`0039AF70`, `00398F90`), and writes at `02AEEAE0` a single-axis rotation (`00398910`) by the
`atan2` of the result's x and z, which `0024C060` folds into `02AEEC70` (`00397910`).

`003A74F0(index)` releases every emitter (`003A9160`) and every `700`<sub>h</sub> object (`003A81E0`), zeroes
the counters `+80`<sub>h</sub> and `+84`<sub>h</sub> of the block at `02EBEFB0`, frees its players (`003A7360`) and runs
the record store's kind-`59`<sub>h</sub> (`'Y'`) nodes through `005043F0` (`003AA430`). It then attaches a
player for the `600`<sub>h</sub> record `index`, or for index 1 the first record that exists
(`003A7460`), and starts every attached player with `003337B0`.

The block at `02EBEFB0` (instance `+130`<sub>h</sub>) holds 16 player pointers, which `003A72A0` clears with
the counters when an instance is made. `003A7460(index)` takes a `2A0`<sub>h</sub>-byte player for the
`600`<sub>h</sub> record `index` into the first free pointer and initialises it with `00333030`.

`003A7360` tears each player down (`00333350`) and frees it, then, by the instance's flags, calls
`0024C6B0` (`+368`<sub>h</sub> bit `80`<sub>h</sub>), `0024C870` (`+368`<sub>h</sub> bit `100`<sub>h</sub>) and `003AF330(0)` (`+3A0`<sub>h</sub> bit 0,
which it clears). `003A7300` is `003A7360` followed by a call to `002FCB60` for each non-zero dword
at `+110`<sub>h</sub>–`+11C`<sub>h</sub>, which it then clears; `003A7420` passes every player to `00332FA0`.

### The free list

An owner table that lets go of a running instance does not free it at once. `0024EE10(instance)`
unlinks it from its kind list `020910F0[kind]` and `0024B1F0(instance)` pushes it on the free list
`02092170` through `+348`<sub>h</sub> and `+350`<sub>h</sub>. The loaded-file queue (`003B1310`, `003B1710`, `003B18E0`)
and the kind-1 handles (`002FC3C0`) do this for an entry in state 6 and set state 7.
`0024C3C0(kind, keep)` moves every instance of a kind except `keep` onto the list; the battle
effect program `003B8670` calls it with kind 7 and the current instance (opcode `21`<sub>h</sub>).

`0024B4F0`, from the field frame `0022A770` and the menu frames `0022B8C0` and `0022BC20`, frees the
blocks queued at `02091150` (count `02092168`), releases the render targets queued at `02091950`
(count `0209216A`, `00182CA0`) and then drains the free list with `0024B580`:

- a kind-1 instance goes back on the list while `002FC010` returns 0; that function first counts
  the instance's byte `+37B`<sub>h</sub> down to 0;
- an instance of kind 5, 6 or 9 leaves the numbered requests (`003B0220`), one of kind 7 the
  loaded-file queue (`003B15C0`) and one of kind 4 the menu registry (`003B2930`);
- every drained instance then releases its path objects, players and emitters (`003A81E0`,
  `003A7360`, `003A9160`), queues its render target `+380`<sub>h</sub> at `02091950` (freed at once when 256
  are queued) and frees its block (`003697F0`).

`0024EE60(instance)` is the immediate form: when the instance is on its kind list it unlinks it
and frees it the same way through `0024EEE0`.

### Emptying a group

`0024C550(kind)` first clears the kind's owner table: `002FBEF0` for kind 1, `003B0130` for kinds 5,
6 and 9, `003B1310` for kind 7 and `00374930` for kind 8, the screen-effect pool of
[screen fades](screen-fades.md). It then frees every context on `020910A0[kind]` (`0024F410`) and
every instance on `020910F0[kind]` (`0024C460`). Its callers are `0026FB90`, `0026FF50`, `003B29B0`,
`003B2B40` and `003B3160`.

- `002FBEF0`, with arena 8 selected, moves every handle on the kind-1 used list `02EC3D60` to the
  free list `02EC3D70`, keeps bits 0–5 and 28–31 of its id, clears its `+10`<sub>h</sub> and `+14`<sub>h</sub>, zeroes
  `02EC3D78` and `02EC3D7C`, and frees the kind-1 instances (`0024C460(1)`).
- `003B0130` frees the instances of kinds 5, 6 and 9 and clears the handle and instance pointer of all
  36 numbered requests.
- `003B1310` walks the loaded files as `003B18E0` treats one (below), without sparing kept entries,
  and then frees the kind-7 instances.

### The effect teardown

`0024E910` ends what a field holds. The area unload `002628B0` and the title-return reset `003601D0`
call it:

1. `002FBEF0`; then every kind-1 context (`020910A8`, `0024F410`) and instance is freed;
2. `0026FF50`, the disposal of the map effect bank;
3. `003B2F90` moves every used model-effect slot (`02EBDB98`) to the free list `02EBDBA0`, ending
   its instance (`0024EE60`) and keeping bits 0–5 and 28–31 of its id, and frees the kind-3 instances;
4. `003B0130`, then `003B26D0`, which releases every loaded file whose flag `+20`<sub>h</sub> bit 0 is clear
   (`003B18E0`);
5. `3FF`<sub>h</sub> goes to the group mask `02092160`, and bit `2`<sub>h</sub> of `+368`<sub>h</sub> is cleared in the instance of
   every model-effect slot (`003B3B50`) and of every numbered request (`003B1130`);
6. `02EBEF68` bit 0, bits `400`<sub>h</sub> and `800`<sub>h</sub> of `020926E4`, the low three bits of `02F8F29E` and bit 0
   of `02EBDBBC` are cleared, and `003AF330(0)` runs;
7. with `020926E4` bit `40`<sub>h</sub> set it drops the bit and queues the target `020926D0` for release;
   last come the motion blur clear `0024EB20` and the cut-in clear `0024CEB0`.

Bit `2`<sub>h</sub> of `+368`<sub>h</sub> holds an instance: on such a step `0024B9B0` runs only `003A7EE0` and
`003A93F0` for it. The time stop sets it on the instances whose owner is a stopped actor
(`003B3BA0`, `003B1180`, through `0024FCA0`), and `0024FC80` releases them all with step 5 alone.

### Keeping the path objects

The instance's path-object list at `02EBEF98` (head `+0`, tail `+8`, links `+E8`<sub>h</sub> back and `+F0`<sub>h</sub>
forward) is emptied by `003A8000` when an instance is made; `003A81E0` frees every object, and
`003A8130(key, byte)` frees every object with that key and byte. `003A7EE0(dt)` clears bit 0 of
every object's byte `+103`<sub>h</sub>, then runs the step `004FF0D0(object, dt)` on each object whose bit is
still clear.

### Emitter bookkeeping

The emitter block (instance `+1B8`<sub>h</sub>, published at `02EBEF88`) keeps, from `+18`<sub>h</sub>, 32 use counts of
8 bytes, ended by an id of −1:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i32` | id (an emitter's `+1C`<sub>h</sub>; -1 ends the table) |  |
| `04`<sub>h</sub> | `u8` | kind (an emitter's `+13B`<sub>h</sub>) |  |
| `05`<sub>h</sub> | `u8` | bit 0: release pending |  |
| `06`<sub>h</sub> | `u16` | emitters using it |  |

- `003A8900` resets the block: the frame stamp and both list ends to 0 and all 32 ids to −1.
- `003A8340(id, kind)`, from the emitter maker `003A8AE0`, adds one to a matching entry or fills the
  first free one with a count of 1.
- `003A9070(id, kind)` removes a matching entry whose count is 0 and closes the gap, returning 0;
  with a count left it sets the pending bit and returns 1. No match returns 1.
- `003A87B0(tag)` releases every emitter whose byte `+13A`<sub>h</sub> equals the tag, and `003A9160` every
  emitter. Each emitter is unlinked, its `+110`<sub>h</sub> object handed to `003A92D0` and freed, and its use
  count lowered; when a pending entry reaches 0 it is removed and the path objects with the
  emitter's id and kind are freed (`003A8130`).

The stop byte `+139`<sub>h</sub> has four writers: `003A8C80` sets it on every emitter, `003A8CB0(n)` on
emitters whose byte `+1C`<sub>h</sub> is not `n`, and `003A8D40(tag)` on emitters whose `+13A`<sub>h</sub> is the tag;
`003A8FC0(tag)` returns whether any emitter has the tag. `003A8CE0(n)` sets bit 0 of `+248`<sub>h</sub> on
every element of the emitters whose `+1C`<sub>h</sub> is not `n` and whose definition type is `40`<sub>h</sub>.

### The record store's other fronts

The store at `02EBEF70` (context `+18`<sub>h</sub>) is a list of nodes linked through encoded dwords
(`0020E600`): head `+0`, tail `+8`, a list of extra blocks at `+10`<sub>h</sub>, and two words at `+18`<sub>h</sub> and
`+1A`<sub>h</sub>, all of which `003A9CC0` zeroes. `003AA1F0(key, kind)` returns the first node with that key
word `+C`<sub>h</sub> and kind byte `+E`<sub>h</sub>, and `003AA240(node)` the next node with the same pair.

`003AA2E0(key)` runs once per context: when the word `+1A`<sub>h</sub> is clear it calls `005011B0` for each
kind-`52`<sub>h</sub> (`'R'`) node and `00501610` for each kind-`53`<sub>h</sub> (`'S'`) node of the key, frees the extra
blocks and sets `+1A`<sub>h</sub>. It returns 0 when one of those calls returned 0.

Below, "the half-rate cadence" means the cadence test `001EDDA0` returning 0
([global state accessors](../Engine-Core/global-state-accessors.md)). `003A8390(dt)`
adds 2 to the instance's frame stamp, the first dword of its `+1B8`<sub>h</sub> block, or `2 / [01DFE0B4]` in
the half-rate cadence (`003A839E`–`003A83BB`). It then calls
`0043EF40(emitter, dt)` for each emitter, with the emitter published at `02EBEF80` (`003A83E0`).

### The emitter step

`0043EF40` returns 0 when the emitter has no emitter record (`0043EF8B`). Otherwise it updates every
element on its active list through `002F3910(element, emitter, dt)` (`0043EF9B`–`0043EFC5`). It
then stops emitting when byte `+139`<sub>h</sub> is set or its age `+2C`<sub>h</sub> has reached a non-zero limit
`+28`<sub>h</sub> (`0043EFC7`–`0043EFEB`), and returns whether elements remain.

An emitting emitter adds `dt` to `+2C`<sub>h</sub> and keeps the whole frame in `+30`<sub>h</sub>. A top-level emitter
(no parent element at `+130`<sub>h</sub>) fires when the integer track at emitter record `+10`<sub>h</sub>, evaluated
at that frame, is no more than the time since its last firing `+34`<sub>h</sub>. In the half-rate cadence it
fires on even frames only. A firing births as many elements as the integer track at record `+0`
gives, each through `00441B30(emitter, age, 0)` (`0043F180`–`0043F1E4`). The tracks are
[authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md).

### Birth

`00441B30(emitter, age, parent)` needs an emitter record and a free element (`00441B5C`–`00441B6D`).
It places the next element through `00442170`, which dispatches on the emitter record's subtype
byte `+282`<sub>h</sub> (0 to 8, `0044218A`–`004421B1`), counts the birth in `+24`<sub>h</sub>, and takes the head of
the free list (`00441BE1`–`00441C0D`).

When the record's byte `+2C4`<sub>h</sub> has bits 0–1 equal to 2 a coin
(`003A6E60(2)`) can put the element at the tail; otherwise it goes to the head (`00441C14`–`00441C9F`).
It samples the record's spawn tracks into the emitter (`+A0`<sub>h</sub>–`+F0`<sub>h</sub>) and calls the birth
dispatcher `002F3BC0(element, emitter, age)` (`00441CA6`–`00441E71`).

`002F3BC0` bounds the element's type byte at `D1`<sub>h</sub> and calls the type's birth method; every birth
method except type `70`<sub>h</sub>'s calls the base birth `002F2D60`. Afterwards, unless `00314960()` is 0 or the cadence
test returns non-zero, it adds 1.0 to the age `+3C`<sub>h</sub>; it stores `00250000()` at `+224`<sub>h</sub> and clears
`+226`<sub>h</sub> (`002F3E3F`–`002F3E73`).

`002F2D60` sets `+18`<sub>h</sub> to the emitter record and `+20`<sub>h</sub> to the definition, returning 0 when either
is missing (`002F2D6F`–`002F2DA2`). It clears bits 1 and 2 of `+1`, sets `+8` to the emitter and
`+10`<sub>h</sub> to 0, copies the emitter's position, and reads the lifetime `+4C`<sub>h</sub> from the integer track
at record `+20`<sub>h</sub> (`002F2DA4`–`002F3029`).

It then copies the sampled spawn values, and the colour `+1F0`<sub>h</sub> from the emitter's `+F0`<sub>h</sub> when
definition byte `+49`<sub>h</sub> has bit `2`<sub>h</sub> (else `80808080`<sub>h</sub>). It zeroes the age `+3C`<sub>h</sub> / `+40`<sub>h</sub> and
the update count `+48`<sub>h</sub>, copies the definition's type byte `+44`<sub>h</sub> into the element's byte `+0`,
marks the eight spawn slots unfired (`+1D0`<sub>h</sub>–`+1EF`<sub>h</sub> = −1) and stamps `+38`<sub>h</sub> with the
instance's frame stamp (`002F302C`–`002F315B`). A type-0 definition fires its spawn slots with
trigger 1 here (`002F317A`–`002F3188`).

### The update

`002F3910(element, emitter, dt)` bounds the type at `D1`<sub>h</sub> and jumps to the type's update method
(`002F3910`–`002F3939`); type 0's is the base `002F2530` itself (`002F393C`), and every other
update except type `70`<sub>h</sub>'s calls the base, most of them followed by a type tail. The base (`002F2530`):

1. While `+224`<sub>h</sub> is set and `00250000()` is 0, clears it and stops unless the cadence test
   returns non-zero (`002F2550`–`002F2572`).
2. Returns 0 when `+38`<sub>h</sub> equals the frame stamp, so an element updates at most once per stamp
   and not on the step of its birth; otherwise adds `dt` to `+3C`<sub>h</sub> (`002F2574`–`002F2587`).
3. In the half-rate cadence, types `67`<sub>h</sub>, `68`<sub>h</sub>, `6A`<sub>h</sub>, `6B`<sub>h</sub>, `71`<sub>h</sub>, `73`<sub>h</sub> and `74`<sub>h</sub> (bit
   set `341B`<sub>h</sub> from `67`<sub>h</sub>) skip steps whose whole age is odd (`002F258C`–`002F25B0`).
4. With a lifetime set, once the whole age with bit 0 cleared exceeds it, fires the spawn slots with
   trigger 3, releases the element and returns 0 (`002F25B2`–`002F25DD`).
5. Computes `n` = whole age minus `+44`<sub>h</sub>; returns 0 when `n` is not positive. Otherwise counts the
   update in `+48`<sub>h</sub>, stores the whole age in `+40`<sub>h</sub>, and sets `+44`<sub>h</sub> to the whole age, or to its
   remainder by definition word `+40`<sub>h</sub> when definition byte `+47`<sub>h</sub> is set (`002F25E4`–`002F262A`).
6. Returns `n` at once for a definition type of `A0`<sub>h</sub> or more; otherwise goes on to sample the
   definition's motion tracks at `+44`<sub>h</sub> (`002F262D`–`002F263C`).

Before the base fires an element's spawn slots with trigger 2 or 3 (`003A8950`), it runs
`002F3890(element)`: the colour `+1F0`<sub>h</sub> is copied to `+1F4`<sub>h</sub>, the world position `+70`<sub>h</sub> moves
to `+80`<sub>h</sub>, and the position `+60`<sub>h</sub> becomes the new `+70`<sub>h</sub>, turned through the parent's matrix
(`0039AF70`, `00398F90`) when `+10`<sub>h</sub> is set. The children therefore start from where the element
is on that step.

In 60 fps mode (`001EDDA0()` returns 0) the base ends by asking `001EDBB0(whole age, kind, effect
number, frame)`, the last three read from the instance's `+3AC`<sub>h</sub>, `+3AE`<sub>h</sub> and `+3A2`<sub>h</sub>, and
returns 0 for the step when it answers 1. Outside an event that is a kind-1 effect `14A`<sub>h</sub> on an odd
whole age. In an event (`001EC560`) it is the one frame when the cut-scene name (`001C50C0`)
contains `spc_z0000`, `01EF9218` is 8 and the cut-scene frame `01F832C4` is `39F`<sub>h</sub>.

### The cull, the release and the spawn slots

The type tails end in one fork: `005002E0(definition, position)` returns 1 to keep and 0 to cull,
and a culled element is released while a kept one fires its spawn slots with trigger 2. The cull
record is the current instance's `+2E0`<sub>h</sub>, or the definition's `+60`<sub>h</sub> when that record's first
byte is `FF`<sub>h</sub> (`005002F9`–`0050030F`).

| Cull record field | Meaning |
|---|---|
| byte `+0` | 1: cull by distance; 2: the same with the Y components zeroed; other: no distance test |
| float `+4`, `+8` | cull when the distance is below `+4` or above `+8` |
| byte `+1` bit 0 | also cull when the point projected through `02AEECB0` is rejected or falls outside `6000`<sub>h</sub>–`A000`<sub>h</sub> on either screen word |

The distance is from the point at `02AED5F0` to the position transformed by `02AEEA20`, computed
by `002F1D90` (`00500324`–`00500381`, `005003D9`–`00500442`).

The release `002F31C0(element, emitter)` runs the type's release method (types `40`<sub>h</sub>–`D1`<sub>h</sub>, then
the sub-range table `0043E9C0` for `42`<sub>h</sub>–`A3`<sub>h</sub>; anything else has none), unlinks the element
from the active list and pushes it on the free list `+120`<sub>h</sub> (`002F31CA`–`002F3297`). A culled
element is gone, not hidden.

`003A8950(trigger, element)` walks eight slots of the element's emitter record: tag byte
`+298h + i`, emitter-record index `+288h + 2i`, start frame `+2A0h + 2i`, definition index
`+2C6h + 2i`, and the element's last firing `+1D0h + 4i` (`003A896E`–`003A899A`).

| Tag | Fires |
|---:|---|
| 0 | never |
| 1 | once, when unfired and the whole age has reached the start frame |
| 2 | on trigger 2 only, not on odd frames in the half-rate cadence: first at the start frame, then whenever the time since the last firing reaches the integer track at the indexed emitter record's `+10`<sub>h</sub> |
| 3 | on trigger 3 only, the element's ending |
| other | on every call |

A firing calls `003A8AE0(index, definition, 2, time, …, element)` (`003A8A6C`–`003A8A97`).

### Child emitters

`003A8AE0` looks up the emitter record in `[[02EBEF90]]` and the definition in `[[02EBEF78]]`,
returning 0 when either is missing or the record's word `+2B2`<sub>h</sub> is 0 (`003A8AE8`–`003A8B42`). It
reuses a matching emitter (`003A8F80`) or makes one (`003A9100`, `0043F450`), records the parent
element at `+130`<sub>h</sub>, and births as many elements as the record's integer track at `+0` gives at
the firing time (`003A8B5C`–`003A8C22`).

### The emitter's own cull and inheritance

Before an element is placed, `0043F2B0(emitter)` applies the cull record of the cull table above to
the emitter's position `+80`<sub>h</sub>: the instance's `+2D0`<sub>h</sub>, or the emitter record's `+2B4`<sub>h</sub> when that
record's first byte is `FF`<sub>h</sub>. `00441B30` places no element when it returns 0 (`00441BD4`), and
`003A8AE0` births no children (`003A8BF1`).

When a birth has a parent element, `00441F10(emitter, parent)` adds the parent's sampled values
into the emitter's spawn values before the birth dispatcher runs, one group per bit of the emitter
record's byte `+2C5`<sub>h</sub>:

- bit 0 adds the parent's `+B0`<sub>h</sub>, `+C0`<sub>h</sub> and `+D0`<sub>h</sub> vectors to the emitter's `+90`<sub>h</sub>, `+A0`<sub>h</sub>
  and `+B0`<sub>h</sub>;
- bit 1 multiplies `+F4`<sub>h</sub> by the parent's `+1F8`<sub>h</sub> and adds `+1FC`<sub>h</sub> and `+200`<sub>h</sub> to `+F8`<sub>h</sub> and
  `+FC`<sub>h</sub>; bit 2 adds the parent's `+110`<sub>h</sub> and `+F0`<sub>h</sub> vectors to `+C0`<sub>h</sub> and `+D0`<sub>h</sub>;
- bit 3 multiplies `+E0`<sub>h</sub>–`+E8`<sub>h</sub> by the parent's `+120`<sub>h</sub>–`+128`<sub>h</sub>; bit 4 mixes the colour `+F0`<sub>h</sub>
  with the parent's colour `+1F0`<sub>h</sub> through `0026EE00`.

`00441EA0(emitter)` returns, for an emitter whose parent element's emitter record has byte `+283`<sub>h</sub>
above 1, that record's word `+286`<sub>h</sub>, or the parent's own word `+204`<sub>h</sub> when the byte is 7, and 0
otherwise; the base birth looks up the `700`<sub>h</sub> path object the element follows with it
(`003A8240`). `00441EE0(emitter, element)` tells whether the element is on the emitter's active list.

### Signals and extra steps

- `003B3CA0(handle, value)` makes the handle's instance current and calls `003A9490`, which signals
  every element of types `67`<sub>h</sub>, `6B`<sub>h</sub>, `71`<sub>h</sub> and `72`<sub>h</sub> through `0043EE70`: each type's handler
  sets one word of the element to 1 (`0045FD00` `+3D8`<sub>h</sub>, `00529D40` `+3D4`<sub>h</sub>, `0052A8A0` `+434`<sub>h</sub>,
  `0052B5D0` `+3F8`<sub>h</sub>).
- `0024B9B0` calls `003A93F0`, which updates the elements of each emitter of type `40`<sub>h</sub> or `A1`<sub>h</sub>
  that follows a subtype-0 path object whose byte `+118`<sub>h</sub> is 3 or 11 a second time, through
  `00442310` with `dt` = 2 × `[01DFE0BC]`.
- `003A92D0(emitter)` releases every element of an emitter of type `40`<sub>h</sub>, `41`<sub>h</sub>, `67`<sub>h</sub>, `A1`<sub>h</sub>,
  `A3`<sub>h</sub>, `D0`<sub>h</sub> or `D1`<sub>h</sub>; its default arm `004FF360` does the same for `42`<sub>h</sub>, `6A`<sub>h</sub>, `6B`<sub>h</sub>,
  `70`<sub>h</sub>–`74`<sub>h</sub> and `A3`<sub>h</sub>, and leaves the other types' elements alone.

### The `700`<sub>h</sub> path objects

A `700`<sub>h</sub> record describes a moving reference point. `003A8020(index, …, key, byte)` creates an
object for record `index` of `[[02EBEFA0]]`: `160`<sub>h</sub>, `1B0`<sub>h</sub> or `1C0`<sub>h</sub> bytes for subtypes 0, 1 and
2–3, record at `+E0`<sub>h</sub>, key at `+100`<sub>h</sub>, linked on the instance list at `[02EBEF98]`; `003A8240(key,
index)` finds one. Each subtype has an initialiser, run through `004FF110`, and a step, through
`004FF0D0`:

| Subtype | Points | Initialiser | Step |
|---:|---|---|---|
| 0 | the anchor at record `+D0`<sub>h</sub> | `00537C20` | `00537BA0` |
| 1 | anchors at `+D0`<sub>h</sub> and `+160`<sub>h</sub> | `00537EA0` | `00537CC0` |
| 2 | two anchors and one bend point | `00538280` | `00537FF0` |
| 3 | two anchors and two bend points | `005386F0` | `005383B0` |

- An initialiser resets the anchors' state blocks (`+110`<sub>h</sub>, `+160`<sub>h</sub>) with `003A3E20` and runs the
  step once. Subtypes 2 and 3 first sample a fixed bend value (`+210`<sub>h</sub>, `+290`<sub>h</sub>) into `+1B0`<sub>h</sub> and
  `+1B4`<sub>h</sub> when bit 1 of the bend's byte (`+221`<sub>h</sub>, `+2A1`<sub>h</sub>) is set.
- A step resolves the anchors with `003A56C0` and fails when one is missing. Subtypes 2 and 3 get
  each bend point from its curve (`004FE4E0`, records `+1F0`<sub>h</sub> and `+270`<sub>h</sub>) or from the fixed value
  (`004FE710`).
- Subtype 2 then moves along start, bend and end by the progress track `+270`<sub>h</sub>, and subtype 3
  along start, both bends and end by `+2F0`<sub>h</sub>, each part sized by its distance (`002F1D90`).
  `004FEAD0` turns the point into the object's matrix.
- The aim queries `00537C50`, `00537EE0`, `00537F40` and `00538780` hand the anchor at `+D0`<sub>h</sub>,
  `+E0`<sub>h</sub>, `+170`<sub>h</sub> or `+160`<sub>h</sub> to the anchor query `003A4290`, for the aim modes of `004FEAD0`.

### Timeline tracks

The instance's block at `+130`<sub>h</sub> (`[02EBEFB0]`) holds sixteen timeline players. `003A7050` steps
each through `00332750` after the emitter step and frees a player whose step returns 0
(`00333350`, `003697F0`). A player's tracks are stepped by `0046E990(track, dt, slot)`, built from
the `600`<sub>h</sub> record's sub-entries; a track's event list is at the sub-entry's `+20`<sub>h</sub> (count byte
`+3`, 0 meaning 64), filled by `0046F380`, which frees the slot's old event first.

`0046EE30(track, sub-entry, id, byte)` fills a new track and `0046EFD0(track, slot)` starts it at
time 0. `0046EFD0` creates the path objects the sub-entry lists (`003A8240`, `003A8020`), runs every
enabled subtype-2 event through `003B8670`, and fires the time-0 events: subtype 1 births an
emitter (`003A8AE0`), first creating its path objects with `0046EF10`, and subtype 3 runs
`004FF2C0`.

`0046E990` adds `dt` to the track's time `+C`<sub>h</sub>. It keeps two lists the events start: vibrations
(count `+12`<sub>h</sub>, `40`<sub>h</sub> bytes each from `+20`<sub>h</sub>) and a second kind of channel (count `+13`<sub>h</sub>, 16
bytes each from `+120`<sub>h</sub>). It then fires the events:

- subtype 2 once its start `+8` is reached, while the time is 0 or the whole time `+A`<sub>h</sub> from the
  last step is below its end `+C`<sub>h</sub>; if the player was freed meanwhile it returns 0;
- subtype 1 once, when the start is reached and the whole time from the last step is below it;
- subtype 3 from the start to its end, plus 1 in the half-rate cadence.

An event's byte `+5` bit 0 enables it; with bits 1–2 equal to 1 it also needs bit `track byte
+10h` of the instance's word `+C`<sub>h</sub>.

- `004FF2C0(event, track)` dispatches on the subtype: 0 and 1 to `00538820`, 2 to `003B8670`, 3 to
  `005372D0`. `004FF320(event)` prepares a newly loaded event and returns the address after it:
  subtype 0 is `10`<sub>h</sub> bytes, 1 goes to `005388F0` (`20`<sub>h</sub>), 2 to `003B9FB0`, 3 to `005375B0`
  (`20`<sub>h</sub>).
- `00538820` births the emitter record `+10`<sub>h</sub> with definition `+12`<sub>h</sub> once the track has reached
  the start `+8`; with bit 0 of `+14`<sub>h</sub> the key gets the event byte in its high byte and
  `0046EF10` creates the path objects first.
- `005372D0` starts a vibration when the track is within one frame after the start and fewer than
  four run: the kind-`58`<sub>h</sub> pattern record at `+1C`<sub>h</sub> (resolved by `005375B0` from slot byte
  `+10`<sub>h</sub>) goes to a slot (`0035B2F0`, `0035B580`) with a level from `00537410` / 127.
- `0046EDD0` (called by `00377230`) and the vibration loop of `0046E990` stop a finished vibration (`0035B1A0`) and
  otherwise set its scale from `00537410` / 127 (`0035B550`). `0046EE70` stops a track's
  vibrations and channels. `0046F330` resets a sub-entry: `C0000000`<sub>h</sub> at `+0` and 192 null slots.
- `0046EF10(track, record, byte)` creates the path object of an emitter record whose byte `+283`<sub>h</sub>
  is above 1 (`+286`<sub>h</sub>) when it does not exist, and recurses into the record's eight spawn slots
  (`+288`<sub>h</sub>).

### The track slots

A player holds sixteen track pointers at `+00`<sub>h</sub>–`+78`<sub>h</sub>, its `600`<sub>h</sub> record at `+80`<sub>h</sub>, a flag
byte `+90`<sub>h</sub>, a target cursor `+91`<sub>h</sub> and a running track counter `+92`<sub>h</sub>. The record lists its
sub-entries as encoded pointers at `+2Ch + 4 × n` (`0020E600`): byte `+1` and bytes `+2`–`+7` name
the sub-entries a start opens, byte `+9` the one opened per target, and bytes `+0A`<sub>h</sub> onward the
one each signal opens.

- `003331A0(player, sub-entry, target)` publishes the player at `02EC0F88`, allocates a `170`<sub>h</sub>-byte
  track (`0036A190`) into the first empty pointer, fills it with `0046EE30(track, sub-entry,
  counter, target)`, clears its byte `+11`<sub>h</sub> and starts it (`0046EFD0`); a start that returns 0
  frees the track (`0046EE70`, `003697F0`). A target of −1 becomes 0 unless bit `1`<sub>h</sub> of `+90`<sub>h</sub> is set.
- After a non-null sub-entry, the counter `+92`<sub>h</sub> goes up by one whether or not a slot was free; a null
  sub-entry does nothing at all.
- `00333280(player, sub-entry, n)` does the same with target −1 and stores `n` in the track's
  byte `+11`<sub>h</sub>, the byte `003333F0` compares when a script waits on trigger `n`.
- `003337B0(player)`, the start, frees all sixteen tracks, then opens the sub-entries of bytes
  `+1`–`+7` whose delay words (`+18`<sub>h</sub>, `+1A`<sub>h</sub>–`+24`<sub>h</sub>) are 0 through `003331A0`, and, with bit 0
  of `+90`<sub>h</sub> set and word `+26`<sub>h</sub> 0, one track of byte `+9` for the next target from `+91`<sub>h</sub> that
  `003A3E30` finds, stepping `+91`<sub>h</sub> past it.
- `0024FE70(instance, n)`, the signal, makes the instance current. Without a player it starts a
  state-2 instance (`003A74F0`, with `02092720` set while `n` is non-zero) or attaches one to a
  state-1 or state-7 instance (`003A7460`, also setting `+378`<sub>h</sub> bit `400`<sub>h</sub>), and sets state 1.
  It then opens the sub-entry of record byte `+0Ah + n` on the first player through `00333280`
  and returns 1, or 0 when that byte is 0.

A track's word `+8` is the counter value it was given (`0046EE30`), and the emitters its events
birth keep it at `+1C`<sub>h</sub> (`00538820`, `003A8AE0`, `0043F450`). The battle effect program stops tracks by that key through `00333640(player,
track, frames)`: below 2 frames it frees the track at once and every emitter with its key
(`003336C0`, `003A8510`); otherwise it stores the key at instance `+37C`<sub>h</sub>, the frames at `+358`<sub>h</sub>
and `+35A`<sub>h</sub>, 1.0 at `+35C`<sub>h</sub>, and sets bit `2000`<sub>h</sub> of `+368`<sub>h</sub> (clearing `1000`<sub>h</sub>).

`003A7050` counts `+35A`<sub>h</sub> down by the whole part of `dt` while bit `1000`<sub>h</sub> or `2000`<sub>h</sub> is set, keeping the fraction
left at `+35C`<sub>h</sub>. At 0, bit `2000`<sub>h</sub> frees through `00333740(player, key)` the first track with the
key and every emitter with it (`003A8510`); bit `1000`<sub>h</sub> frees through `003334B0(player, key)`
every track and emitter without it (`003A8660`).

### The method tables

Every per-type behaviour is a switch on the element's type byte. Five tables cover the main range
and five more the sub-range `42`<sub>h</sub>–`AB`<sub>h</sub>, which each main table reaches through its default arm.

| Method | Main dispatcher | Key | Sub-range dispatcher |
|---|---|---|---|
| birth | `002F3BC0` | element `+0` | `0043EBF0` |
| update | `002F3910` | element `+0` | `0043EAB0` |
| draw | `002F4020` | element `+0` minus 1 | `0043ED30` |
| setup | `005004C0` | definition `+44`<sub>h</sub> | `00538910` |
| release | `002F31C0` | element `+0` minus `40`<sub>h</sub> | `0043E9C0` |

Decoded from the jump tables: 47 types have main birth, update and setup arms, 46 a draw arm and 6 a
release arm; 18 types have sub-range arms (9 with a release). 65 types have an arm somewhere, with
248 distinct handlers; the per-type list is on [effect element types](effect-element-types.md).
`005004C0` runs once per definition, from the `A00`<sub>h</sub> record handler.

### The six display layers

`MainLoop_Draw` (`0022B0B0`) asks for effects six times through `00258EE0(layer)`, each request
bracketed by the engine's marker text. The draw-side order inside a layer comes from the grouped
pass `00259030`.

| Layer | Marker | Work |
|---:|---|---|
| 1 | `display VFX [layer : first]` | grouped pass, then `0024C640` |
| 2 | `display VFX [layer : after BG]` | the same |
| 3 | `display VFX [layer : TsEffMan_Layer_AfterOBJ]` | no grouped pass: `0039D570(0)`, `0039D3F0`, a pair of calls chosen on `02F8F310` bit 2, then `003A3990` |
| 4 | `display VFX [layer : in EFF]` | `0039CFF0(0, 3C00h)`, `0036F550` unless `00181DD0()` is non-zero, grouped pass, `0039CFF0(0, 3700h)`, `0024C640` |
| 5 | `display VFX [layer : after EFF & MENU]` | `0036F9F0` unless `00181DD0()` is non-zero, then the grouped pass |
| 6 | the same text as 5 | grouped pass |

Every layer request runs between `00862C10(0, layer)` and `00862C30`. The opening call
(`001B2530` on the object `[01F7F4D8]`) binds three textures of the render manager to the texture ids
`E00`<sub>h</sub>, `DFF`<sub>h</sub> and 0, choosing the second set for a layer above 5, stores the pass id at
`+90`<sub>h</sub> and the layer without bit `10`<sub>h</sub> at `+94`<sub>h</sub>, and files a `GiBeginScene` (`001FBD80(2)`); the closing call
files a `GiEndScene` (`001B2600`).

`00862C40`, `00862C00` and `00862BF0` return those two words; the drain uses them to close and
reopen the bracket around the post-processing block, with `10`<sub>h</sub> added to the layer (`003A3740`).

`00259030(layer)` selects arena 8, calls `0024D370(layer, group)` for groups 2, 3, 5, 6, 9, 1, 7 and
4, then drains the draw list (`003A3740`) (`00259036`–`002590C0`). A group is an instance kind.

### Drawing one group

`0024D370(layer, group)` takes the list `020910F0[group]` and asks the group gate `0024D4E0`
(`0024D382`–`0024D3AF`). The gate refuses group 8; groups 1–4 and 7 need bit `group − 1` in the AND
of `02092162`, `02092164` and `02092166`; group 2 also needs `02F8F29E` bit 0 clear and group 5
`02EBEF68` bit 0 clear (`0024D4E0`–`0024D538`).

For each instance the group draw publishes the group at `02092700` and skips the instance unless
its `+3A8`<sub>h</sub> equals `00181DD0()`, the high nibble of its word `+378`<sub>h</sub> equals the layer, and the
per-instance gate `0024D770(instance, 1)` passes (`0024D3C0`–`0024D3FC`). It makes the instance
current and walks its emitters through `003A72F0` → `003A8D80`, which calls `00441970` for each
(`0024D405`, `0024D499`, `003A8D84`–`003A8DAB`). So an effect's layer is authored in its
instance.

`00441970(emitter)` returns when the emitter has no elements. Unless the instance's flag byte
`+36A`<sub>h</sub> has bit 0, only emitters whose definition type is `40`<sub>h</sub>, `41`<sub>h</sub>, `A1`<sub>h</sub>, `A2`<sub>h</sub>, `A5`<sub>h</sub>
or `D0`<sub>h</sub> are drawn (`0044198E`–`004419CE`; the table is
`effect-element-runtime-effect-kind-441970.tsv`). It sets the pass nibble `02AEE910`: definition
byte `+4C`<sub>h</sub> when `+4A`<sub>h</sub> is `40`<sub>h</sub> or more, else 8 (`004419F5`–`00441A0E`).

It then calls `002F4020(element, emitter)` for each element, forward from the head, or backward from
the tail when the emitter record's byte `+2C4`<sub>h</sub> has bits 0–1 set (`00441A15`–`00441A82`).

### Instance flags at draw time

Before the emitter walk, `0024D370` reads the instance's flag byte `+36A`<sub>h</sub>. With bit 0 set it
records the instance's target `+380`<sub>h</sub>, when there is one, for texture id `3300`<sub>h</sub> at 256
× 224 (`002D7D90`), then calls `003AA2E0(0)` and skips the instance when that returns 0. With bit 1
set it files a `GiZNormalOnOff` command with 1 (`0039D410`, through `00864E00`) and sets bit 0 of
`02F8F310`, which makes the drain open with `GiTransNz` instead of `GiTrans` (`003A3740`).

### Widescreen and mask-border flags

`0024E4B0` classifies the current instance's context while the pass id `+90`<sub>h</sub> of `[01F7F4D8]` is
0 (`00862C40`), by its kind byte and its id word `+4`:

| Context | Ids | Bits |
|---|---|---|
| kind 1 | `80`<sub>h</sub> | `10`<sub>h</sub> |
| kind 1 | `89`<sub>h</sub> | `8`<sub>h</sub> |
| kind 1 | `D5`<sub>h</sub>–`D7`<sub>h</sub>, `E2`<sub>h</sub>, `17A`<sub>h</sub>, `182`<sub>h</sub> | `2`<sub>h</sub> |
| kind 7 | `B0`<sub>h</sub>, `2C0`<sub>h</sub>–`373`<sub>h</sub> | `1`<sub>h</sub> |
| kind 7 | `240`<sub>h</sub>–`2BF`<sub>h</sub> | `1`<sub>h</sub> for 25 listed ids, `4`<sub>h</sub> for `289`<sub>h</sub>, `3`<sub>h</sub> for `28B`<sub>h</sub> and `2A3`<sub>h</sub>, `2`<sub>h</sub> for the rest |

Any other context gets 0. For each instance it draws, `0024D370` calls `00183090(1)` after the
emitter walk when the flags have bit `2`<sub>h</sub>, which sets `01F7F4F8`, one of the flags the mask-border
wrapper `0017F6B0` tests; the frame state machine `0022A580` clears it each frame (`00183090(0)`). `0024E640` turns the flags into the widescreen mode the element draws use: 1 for
bit `1`<sub>h</sub> or a kind-7 id from `200`<sub>h</sub> to `23F`<sub>h</sub>, else 2, 3 or 4 for bit `4`<sub>h</sub>, `8`<sub>h</sub> or `10`<sub>h</sub>, else
0.

`00184740`, from the frame `0022A770`, reads the current instance through `0024DE30(&kind, &id,
&frame)`, which returns its bytes `+3AC`<sub>h</sub>, `+3AE`<sub>h</sub> and `+3A2`<sub>h</sub> + 1. While a kind-1 effect
`17A`<sub>h</sub> is current and the latch `01F7F540` is clear, it sets both; any other current effect
clears `01F7F500`, another flag `0017F6B0` tests. `00182D30` clears the latch.

### Soft particles

`0024D140(&factor)` answers whether the current context draws soft particles, for the `GiSprite`
builder `008647C0` (`+D0`<sub>h</sub> and `+D4`<sub>h</sub> of the command) and the VU program packet `001DB840`
(`+630`<sub>h</sub> and `+634`<sub>h</sub>). It answers no with a factor of 0.1 unless the pass id is 0 and the layer
`+94`<sub>h</sub> is 4, or 3 or 4 when `0017FE10()` (the byte `01DF08F4`) is non-zero. Otherwise the kind
picks a table from `softparticle_*.csv` ([standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md)):

| Kind | Key | Table |
|---|---|---|
| 1 | id word `+4` | `02F95B40` (`magic`) |
| 2 | the instance's word `+4` against the map's rows | `02F8F340` (`softparticle_bg.csv`) |
| 3 | `003B33D0(id)` | `02F96B40` (`chara`) |
| 5, 6, 9 | the effect number `003B0940(handle)` | `02F95340` (`common`) |
| 7 | id word `+4` | `02F96340` (`event`) |

Kinds 4 and 8 answer no. A table entry answers yes when its byte 0 is set, with the factor its
word `+2` / 100; a bound of 512 entries applies. For kind 2 the answer and factor are the matched
row's bytes `+1` and `+2`.

`0024F790`, run by the EFB loader `0026FB90`, picks the map's rows: it takes the text after the
backslash of the map-art context's name `+241`<sub>h</sub> (`00180370`), finds the matching 16-byte record in `02F93340`, and
stores its first row in `01E0C290` and the row count in `02092710` (up to the next record, or to
`02092714` for the last). No match stores −1.

### Drawing one element

`002F4020` returns when the type byte is outside `[022BE7D8]`..`[01EEBAE0]`, or when `+224`<sub>h</sub> is set
while the cadence test returns 0 (`002F402A`–`002F405B`). With definition byte `+4D`<sub>h</sub> non-zero, a
counter in word `+2` and the cadence test set a skip bit in byte `+1` bit 0, and a set bit skips
the draw (`002F4070`–`002F40E6`). It stores definition byte `+75`<sub>h</sub> at `02AEF41C`, calls the type's
draw method, and clears `02AEF41C` again (`002F40EC`–`002F4124`, `002F4369`).

The debug console's "Particle Draw Type Range" entries set the bounds through `002F1CD0(low,
high)`; they ship as 0 and `D1`<sub>h</sub>, so every type draws.

### The draw list

Blended primitives do not draw at once. An emitter appends a `28`<sub>h</sub>-byte entry to the list at
`[02F8F2F8]`, counted by the word `02F8F2C6`; the point emitter `0039D970`, for one, writes the
projected depth word as the sort key `+8` and ORs the pass nibble into bits 28–31
(`0039D986`–`0039DA05`). `003A3670` allocates the list, `190000`<sub>h</sub> bytes, which is 40,960 entries.

`003A3740` drains it. It returns for an empty list, sorts the entries by `+8` (`003A3A50`), and for
each entry calls the function at `+10`<sub>h</sub> with `+00`<sub>h</sub>; without one, it submits the command at
`+18`<sub>h</sub> through `0020E630(command, 2)`, or with flag bit `4`<sub>h</sub> defers it to `02AEF420` for layer 3's
`003A3990` (`003A3744`–`003A3908`). It empties the list and keeps the last and peak counts
(`003A3929`–`003A3973`).

`0024D540`, the frame's draw setup, drains once more and then rewinds: `003A3A00` resets the packet
cursor `02F8F2D0` to the arena base `02F8F308`, sets its end `02F8F2D8`, and zeroes the count
(`0024D556`, `0024D55B`, `003A3A00`–`003A3A42`).

Three other producers copy data into the packet arena behind `02F8F2D0` and file an entry for it;
each does nothing when the arena lacks room. `003A2C80(callback, data, size, pass, key)`, called
from `004781A0`, stores the copy at `+00`<sub>h</sub> and the callback at `+10`<sub>h</sub>, so the drain calls it with
the copy.

`003A3010(data, size, key)` and `003A31A0`, called from effect types (`0044D4A0`,
`00453150`, `00460BC0`, `00522300`; `0045BAE0`), build a GS packet around the data, with the blend
word of the current mode, and file it at `+00`<sub>h</sub> with no callback and no command. The drain does
nothing with such an entry: it calls a callback when there is one and otherwise submits only when
`+00`<sub>h</sub> is null (`003A38BA`–`003A38CD`).

### Target and anchor queries

Some tails ask for a point from a sub-record. `002F3360` switches on the sub-record's byte `+90`<sub>h</sub>;
value 3 calls `003A56F0`, which samples a vector track (`00430B90`) and switches on the byte `+48`<sub>h</sub>
minus 1 over 14 cases (`002F3384`–`002F33EA`, `003A575E`–`003A5797`). `003A4290` has the same
14-case switch on the same byte (`003A4303`–`003A4319`).

Their arms are in
`effect-element-runtime-switch-family-3a42-3a56.tsv`; `effect-element-runtime-switch-family-frontier-decode.tsv`
decodes `00442170` and `00442460` (the emitter-record subtype switches) and the record-store
fronts `00500980` / `00500850`, together with dispatchers outside the effect code.

### Target slots

An instance names its targets in the dword array at `+10`<sub>h</sub>, with its count in byte `+372`<sub>h</sub>.
With bit `200`<sub>h</sub> of word `+378`<sub>h</sub> set, both readers below take the global list `02096A24` (count
`02096B24`) instead.

`003A5640(slot)` treats slot −1 as slot 0. In a kind-3 instance it returns the `+10`<sub>h</sub> entry as it
is; otherwise it takes the `+90`<sub>h</sub> entry, or the `+10`<sub>h</sub> entry when that is 0, and returns it through
`002E9B80` (the first dword of the actor's `+C0`<sub>h</sub> object, or −1).

`003A3E30(slot)` returns the `+10`<sub>h</sub> entry, or −1 past the count. In a kind-1 instance whose word
`+368`<sub>h</sub> is below `8000`<sub>h</sub> it first checks the target (`003229E0`, `00322760`): a target that fails
adds one to byte `+374`<sub>h</sub> and gives −1, and a replacement that `00322760` reports goes into `+10`<sub>h</sub>,
with the old entry kept at `+90`<sub>h</sub>, after an effect `62`<sub>h</sub> is played on it (`003B02A0`).

`003A4220(id)` picks one of three lookups by the instance: `0036E620` when bits 12–14 of word
`+36A`<sub>h</sub> are 3, `0036E4B0` in a kind-2 instance, and `0036E4E0` (a 64-entry table at `022D97B0`)
otherwise or when the first finds nothing; it returns the result through `002E9B80`.

Two wrappers hand these to element handlers:

- `0024DCE0(mode, n)`, for `00524320`: mode 0 gives the current instance's owner `003A3FD0(−1)`
  (−1 with no instance current), mode 2 gives `003A4220(n)`, and mode 3 the render index of the
  n-th actor of manager 0 (`02098E10`) that has one (`00358940`, `003589B0`, `002E9B80`); any
  other mode, or no match, gives −1.
- `0024DDD0(&owner, &target)`, for `0045FD50` and `00529200`, returns `003A3FD0(slot)` and
  `003A6BA0(slot)` for the slot byte `+13B`<sub>h</sub> of the current emitter `[02EBEF80]`.
- `003A6BA0(slot)` returns a kind-3 instance's `+10`<sub>h</sub> entry for the slot (slot 0 for −1) as it is; otherwise it
  passes the slot's `+10`<sub>h</sub> entry, or for −1 the `+90`<sub>h</sub> entry and else the first `+10`<sub>h</sub> one,
  through `002E9B80`. With `+378`<sub>h</sub> bit `200`<sub>h</sub> it reads the global list `02096A24` instead.

The three 64-entry tables are filled by script verbs, each taking an index clamped to 0 to 63 and
storing the calling script's actor (`00263F10`, `003589B0`):

| Verb | Table | Set | Clear |
|---|---|---|---|
| `effectactor(n)` (`0126`<sub>h</sub>, `00352270`), from manager 3 | `022D99B0` | `0036E880` | `clear_effectactor` (`056F`<sub>h</sub>, `00342010`): `0036E1A0` |
| `effectactor(n)` from any other manager | `022D97B0` | `0036E7E0` | `clear_effectactor`: `0036E160` |
| `bgeffectactor(n)` (`0570`<sub>h</sub>, `00352940`) | `022D98B0` | `0036E7B0` | `clear_bgeffectactor` (`0571`<sub>h</sub>, `003423C0`): `0036E040` |

The manager is the issuer's byte `+15`<sub>h</sub>. A clear stores 0.


### Numbered effects on actors

`003B02A0(owner, targets, count, number, kind)` plays effect `number` as an instance of kind 5, 6 or 9
and refuses any other kind. Unless the request kind below is 1, it also refuses when
`002FC9B0()` plus `003B0B70()` exceeds 23. It makes the instance (`0024B270`) with state 2 and
the number in `+373`<sub>h</sub>, stores the owner at `+08`<sub>h</sub>, and appends each target whose render record is
live and passes `002E9FE0` to the target array `+10`<sub>h</sub>. Numbers 100 to 103 and `94`<sub>h</sub> are kind-3
requests in the table below.

The requests sit in 36 entries of `18`<sub>h</sub> bytes at `02EBEC00`, packed from the start:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | handle: kind << 28 \| serial (02EBEF60) |  |
| `04`<sub>h</sub> | `u32` | set by 003B0FD0 |  |
| `08`<sub>h</sub> | `void*` | the instance |  |
| `10`<sub>h</sub> | `u8` | effect number; | +`11`<sub>h</sub> u8 target test;  +`12`<sub>h</sub> u8 kind |
| `13`<sub>h</sub> | `u8` | bits 1-2: request kind (3 for 100-103 and `94`<sub>h</sub>, 1 when the number's 01EFE260 byte is 1, else 0) |  |

- `003B0980` returns the first free entry; with all 36 taken it ends the first instance whose
  request kind is 0 or 3 (`0024EE60`), closes the gap and returns the last entry.
- `003AFFB0(n)`, from `002FCCC0`, ends requests from the front of the table until `n` are left,
  sparing request kinds 1 and 2. `003B0B70` returns half the number of entries in use.
- `003B0BF0(handle)` returns the entry, `003B0940(handle)` its effect number or −1, and
  `003B0FD0(handle, v)` stores `v` at `+04`<sub>h</sub>. `003B0C30(owner, number)` is
  `003B02A0(owner, 0, 0, number, 5)`.
- `003B1260(handle, kind)`, for a kind of 1 to 10, calls `0024FE70(instance, kind)` with arena 8
  selected.
- `003B1050(targets, n)`, from `0024FBF0`, raises bit `4`<sub>h</sub> of `+368`<sub>h</sub> on every kind-5 instance
  whose request kind is 0, or is 1 or 3 and whose owner `+08`<sub>h</sub> equals an id of the list (`+11`<sub>h</sub>
  = 0) or the value `002E9B80` returns for one (`+11`<sub>h</sub> = 1).

### Battle effect files

Kind-1 effects come from 48 slots of `38`<sub>h</sub> bytes at `02EC32E0`, chained by `002FC200` into a free
list `02EC3D70`; the active list runs from `02EC3D60` to `02EC3D68` through `+28`<sub>h</sub> and `+30`<sub>h</sub>.

`BattleEffectSlot` (`38`<sub>h</sub> bytes, offsets from the start of the 02EC32E0):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | handle | bits 0-5 the slot, `10000000`<sub>h</sub> the kind |
| `08`<sub>h</sub> | `void*` | context | the type-1 context |
| `10`<sub>h</sub> | `void*` | instance the instance playing it |  |
| `18`<sub>h</sub> | `u32` | request | the file request |
| `1C`<sub>h</sub> | `u32` | size | the file size |
| `20`<sub>h</sub> | `u16` | number | the effect number |
| `23`<sub>h</sub> | `u8` | state | low nibble: 1 wanted, 2 reading, 3 read, 4 freeing, 5 ready, 6 playing |
| `28`<sub>h</sub> | `void*` | next |  |
| `30`<sub>h</sub> | `void*` | previous |  |

`002FCF00`, each simulation step from `00258D70`, walks the active list:

- state 1 runs `002FC860` unless a read already runs (`02EC3D7C`, or the loaded-file queue's
  `02EBEBE4`). It asks the file size in class `0B`<sub>h</sub>, or `26`<sub>h</sub> when `002DEBB0()` is 0
  (`0032E400`); a missing number `78`<sub>h</sub>–`89`<sub>h</sub> falls back to `78`<sub>h</sub>, `8A`<sub>h</sub>–`99`<sub>h</sub> to `8A`<sub>h</sub>, and
  any other to 0. It queues the read (`0032E620`) and sets state 2.
- the size cache: `002FCFF0` (through the stub `0036DDB0`) asks the size of all 512 numbers once, keeps them
  at `02EC19C0` (8 bytes each) and sets `02EC3D7D`; the reset `002FC200` clears it (`002FC2FF`). While it is
  set, state 1 takes the size from the cache (`002FC8AD`), and a missing number falls back to entry 0, not
  to the `78`<sub>h</sub> and `8A`<sub>h</sub> ranges;
- state 3 builds the context (`002FC4A0`);
- state 4 waits until the request is gone (`0032E4D0`), then returns the slot to the free list
  (`002FC350`) and clears `02EC3D7C`;
- state 6 adds 1 to the instance's frame word `+3A2`<sub>h</sub>.

`002FCCC0(owner, targets, count, handle)` plays a slot in state 5. It sums the 5-bit weights of
the active slots' numbers (`02EC19C4`, filled from the 401 bytes at `01EEBB10`), ends numbered
requests until `36 − sum` are left (`003AFFB0`), and makes an instance (`0024B270`): kind 1, the
handle at `+4`, the owner at `+08`<sub>h</sub>, the targets at `+10`<sub>h</sub> with the count in `+372`<sub>h</sub>, the
slot's context at `+340`<sub>h</sub>, `+3AC`<sub>h</sub> = 1 and the number at `+3AE`<sub>h</sub>. It sets state 6 and returns
the handle, or 0.

`002EAD00(owner, count, targets, handle)` returns 0 for no targets; otherwise it counts
`02CA4EDC` up (`0042FCB0`) and plays through `002FCCC0`. Its caller `00319E40(unit)` gathers the
ids of the unit's targets (list `+780`<sub>h</sub>, count `+77C`<sub>h</sub>) whose actors exist and plays on them the
handle `0030CA50` reads for the unit: entry `+695`<sub>h</sub> of the 32 entries of `30`<sub>h</sub> bytes at
`022C17D0`, its dword `+4`.

- `003B1180(targets, n)` selects instances the same way and sets bit `2`<sub>h</sub> of their `+368`<sub>h</sub>;
  `003B1130` clears that bit on every request's instance.
- `003B0220(instance)`, from the free-list drain, finds the request holding the instance, moves the
  later entries down and clears the last; `003B0770(handle)` does the same by handle after ending the
  instance (`0024EE60`). `00319E30(handle)` ignores 0 and −1 and tail-jumps to `003B0770` otherwise;
  the battle unit code `00300E40` and `00301140` pass it the unit's `+74`<sub>h</sub>.

### Loaded effect files

A second queue at `02EBE5E0` holds 32 entries of `30`<sub>h</sub> bytes, each an effect file loaded into its
own type-7 context: `+00`<sub>h</sub> id, `+04`<sub>h</sub> file number, `+08`<sub>h</sub> context, `+10`<sub>h</sub> instance, `+18`<sub>h</sub>
file request, `+1C`<sub>h</sub> state, `+20`<sub>h</sub> flags, `+28`<sub>h</sub> buffer. Only one load runs at a time
(`02EBEBE4`). `003B25D0`, each simulation step from `00258D70`, moves them on:

- state 1 (`003B2310`) maps the file number (bit `1000`<sub>h</sub> to `200h +`, bit `2000`<sub>h</sub> to `240h +`,
  bit `8000`<sub>h</sub> to `1FF`<sub>h</sub>, `C3`<sub>h</sub> to `1FE`<sub>h</sub> when `002DEBB0` returns 0), requests the file in class
  `0C`<sub>h</sub> (`0032E400`, `0032E620`) with the completion `003B22D0`, which sets state 3, and sets
  state 2;
- state 3 (`003B2220`) builds a type-7 context for the id (`0024B3A0`), parses the buffer
  (`003EDAD0`), copies the high nibble of the first `600`<sub>h</sub> record's `+16`<sub>h</sub> into the context's
  byte `+2`, and sets state 5;
- state 4 waits until the request is gone (`0032E4D0`), then removes the entry and closes the gap.
  `003B21E0` clears an entry's id and state when its request is already gone.

`003B2830(id, n)`, for `n` of 1 to 10, calls `0024FE70(instance, n)` for the entry's instance and
puts `n` in the low nibble of its word `+378`<sub>h</sub>. `003B27A0(id, n)`, for `n` of 0 to 10, makes the
instance current and passes its `+130`<sub>h</sub> block to `003339C0` with `n`. `003B1560(flag)` clears bit 0
of `+20`<sub>h</sub> in every entry when `flag` is 0, and otherwise passes each entry with the bit to
`003B18E0`; no code calls it.

### Filing, sharing and releasing a loaded file

`003B1A80(file, tag)` files a load with arena 8 selected. It takes the first entry whose id is 0,
returning 0 when all 32 are taken, and gives it the id `70000000h | (serial & FFFFh) << 12 | (tag &
3Fh) << 6`, the serial counting up at `02EBEBE0`. It stores the file number at `+04`<sub>h</sub> and clears
the context, the state, the buffer and flag bits 0 and 1. When another entry with the same file is in
state 5 or 6, the new entry takes that entry's context and starts in state 5;
otherwise `003B2310` starts the read, and a refused read clears the entry and returns 0.

`003B1BA0(owner, targets, count, id, n)` plays an entry. With `n` 0 it needs state 5: it makes a
kind-7 instance on the entry's context (`0024B270`), records it at `+10`<sub>h</sub>, sets state 6 and copies
flag bit 1 into the instance's hold bit `40`<sub>h</sub> of `+368`<sub>h</sub>. With `n` non-zero it needs state 5 or
later and only passes `n` to `0024FE70` for the existing instance, putting `n` in the low nibble of
`+378`<sub>h</sub>. `003B2470(id)` returns an entry's instance.

`003B18E0(id)` releases one entry by its state, with arena 8 selected:

| State | Release |
|---:|---|
| 1 | the id and state are cleared and the entry removed |
| 2 | the read is cancelled (`0032E590`) and the entry goes to state 4 while the request is still queued (`0032E4D0`) or `0032E520(1)` holds; otherwise as state 3 |
| 3 | `003B21E0` clears the entry, the load-running flag `02EBEBE4` drops, and the entry is removed |
| 5 | the context is freed (`0024F410`) unless another entry for the file in state 5 or 6 holds it (`003B2710`); then as state 1 |
| 6 | the instance goes to the free list and the entry to state 7 |
| 4, 7 | nothing |

A removed entry closes the gap and the last entry's id `02EBEBB0` is cleared. `003B1710(spare)`
applies the same release to every entry, skipping those with flag bit 0 when `spare` is non-zero,
and ends a removed entry's instance (`0024EE60`). `003B15C0(instance)`, from the free-list drain,
removes the entry whose instance is freed, freeing its context only when no other entry for the
same file in state 5 or 6 has one.

Flag bit 0 keeps a file across an area change. `effectkeepmapjump(slot, b)` (`02C5`<sub>h</sub>, `0036E9B0`)
writes it through `003B2750(id, b)`, and the flag is read by `003B24C0(id)`; both accept only an id
whose top nibble is 7. The ordinary area unload runs only `0024E910`, whose `003B26D0` spares kept
files. When `022CB726` is set, as after the title-return reset `003601D0`, the unload first runs
`0036DF30`, which calls `003B1710(0)` and releases every file.

### Script effect slots

Event scripts reach the loaded-file queue through 32 slots of `18`<sub>h</sub> bytes at `022D94B0`: the
queue id `+00`<sub>h</sub>, a state word `+04`<sub>h</sub> (0 free, 1 reading, 2 read, 3 playing, 4 cancelled), the
reading manager `+08`<sub>h</sub> and the signal bytes `+10`<sub>h</sub> ([native commands](../Scripts-And-Script-Commands/native-commands.md)).
Every slot number is clamped to 0 to 31.

- Read: `effectread(id)` (`00DB`<sub>h</sub>), `locationeffectread(id)` (`0127`<sub>h</sub>) and `questeffectread(id)`
  (`01DA`<sub>h</sub>) push slot 0 and the kind 0, 1 or 2; their two-argument forms (`00E0`<sub>h</sub>, `0128`<sub>h</sub>,
  `01DB`<sub>h</sub>) take the slot first. The shared body `003576D0` calls `0036E320` unless the issuer's
  manager is skipping (`00267310`), and then `00314D40(1)`.
- `0036E320(manager, slot, id, kind)` acts only on a free slot: it clears the signal bytes, adds
  `1000`<sub>h</sub> to the id for kind 1 or `2000`<sub>h</sub> for kind 2, files it with `003B1A80(id, slot)`, which puts
  the slot in bits 6 to 11 of the queue id, keeps the manager, and sets state 1 when it got an id.
- `effectreadsync` (`00DC`<sub>h</sub>, slot 0) and `effectreadsync_e1(slot)` (`00E1`<sub>h</sub>) poll `0036E540`: a
  reading slot waits until `0024DE70(id)` reports 2 or 3, then becomes state 2.
- Play: `effectplay(n)` (`00DD`<sub>h</sub>, slot 0) and `effectplay_e2(slot, n)` (`00E2`<sub>h</sub>) call
  `0036E8B0(slot, n)`. A slot in state 2 or 3 whose file reports 2 or 3 becomes state 3 and is
  played by `003B1BA0` with the owner `[02EBCC70]`, the target list `02EBCBE0` (count
  `[02EBCC60]`) and `n`. Then `0024F8D0` sets bits 12 to 14 of the instance's `+36A`<sub>h</sub> to 3 for a
  slot read by manager 3 and to 0 otherwise, which picks the target table above.
- `effectsync` (`00DE`<sub>h</sub>, slot 0) and `effectsync_e3(slot)` (`00E3`<sub>h</sub>) wait while the state word
  (`0036E5A0`) is non-zero; a skip cancels the slot instead.
- Cancel: `effectcancel` (`00DF`<sub>h</sub>, slot 0) and `effectcancel_e4(slot)` (`00E4`<sub>h</sub>) run `0036DDC0`,
  which sets state 4 on a slot in any state but 0 and 4 and, unless the queue entry's flag bit 0 is
  set (`003B24C0`), releases the entry (`003B18E0`). `effectcancelall` (`00E5`<sub>h</sub>,
  handler `00350FA0` `jmp 0036DE20`) runs `003B1710` over the queue and sets every slot to state 4.
- Triggers: `effecttriggersync` (`0274`<sub>h</sub>, `0275`<sub>h</sub>) waits while `0036E5E0(slot, n)` holds: for a
  playing slot, `0024FDA0` makes the instance current and asks `003333F0` whether one of the 16
  entries of its `+130`<sub>h</sub> block has byte `+11`<sub>h</sub> equal to `n`, or else `003A8FC0(n)`.
  `effecttriggercancel` (`01DC`<sub>h</sub>, slot 0) and `effecttriggercancel_1dd(slot, n)` (`01DD`<sub>h</sub>) run
  `0036DF80`, which passes a non-free slot's id to `003B27A0`.
- `effectsignal(slot, v)` (`0241`<sub>h</sub>, `0036E460`) passes `v` to `0024F3C0`, which, for `v` = 1,
  adds 1 to bits 4 to 7 of the instance's word `+378`<sub>h</sub>.
- `effecthitsyncbyid` (`0440`<sub>h</sub>) waits while `0036E640(id)` holds: the file reports 2 or 3 and bit 5
  of the instance's `+36A`<sub>h</sub> is clear (`0024E210(id, 0)`).

## Layouts

```
effect instance (0x3B0, 0024B270)
+0x000  u8    kind (the group and the list 020910F0[kind])
+0x120        block published at 02EBEF98
+0x130        block published at 02EBEFB0
+0x1B8  u32   frame stamp; +0x1C0 first emitter
+0x2E0        cull record (first byte 0xFF: use the definition's)
+0x340  ptr   effect context
+0x348  ptr   next, +0x350 previous
+0x36A  u8    flags: bit 0 draws every emitter
+0x378  u16   high nibble: display layer
+0x3A8  u16   stamp from 00181DD0()

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
+0x224  u16   hold word from 00250000()

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

The instance lists `020910F0`, the current instance `02F97348` and context `02F97340`, the table
pointers `02EBEF70`–`02EBEFB0`, the current emitter `02EBEF80`, the pass nibble `02AEE910`, the blend
pair `02AEE900` / `02AEE908`, the draw list `02F8F2F8` with its count `02F8F2C6`, and the packet
cursor `02F8F2D0` / `02F8F2D8` over `02F8F308`.

## Modding notes

- An effect's display layer is the high nibble of its instance word `+378`<sub>h</sub>; its group is the
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
  `001EDDA0`.
