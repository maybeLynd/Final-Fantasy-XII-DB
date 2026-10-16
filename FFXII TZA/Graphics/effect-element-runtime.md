---
title: "Effect element runtime: instances, emitters and elements, the per-step update, birth, release and child spawns, and the six display layers"
kind: "system"
category: "Graphics"
summary: "How a parsed effect runs: the 0x3B0-byte effect instance and its kind list, the emitters an instance keeps and the elements each emitter owns, the update pass that runs once per simulation step, the element's birth, its base update and type tail, the cull test that releases an element or fires its eight child-spawn slots, the five method tables keyed by the element type, and the six display layers whose grouped passes walk the elements, append to the depth-sorted draw list and drain it."
addresses: ["0024B270", "020910F0", "02F97348", "02EBEF88", "0024ED80", "00258D70", "0024B9B0", "003A7050", "003A8390", "0043EF40", "00441B30", "002F3BC0", "002F2D60", "002F3910", "002F2530", "002F4020", "005004C0", "002F31C0", "005002E0", "003A8950", "003A8AE0", "00258EE0", "00259030", "0024D370", "0024D4E0", "00441970", "02AEE910", "02F8F2F8", "02F8F2C6", "003A3740", "003A3A00", "0024D540"]
---

# Effect element runtime: instances, emitters and elements, the per-step update, birth, release and child spawns, and the six display layers

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

- An effect instance, `0x3B0` bytes made by `0024B270(template)` from a template. Its byte `+0` is
  its kind; it is linked at the head of `020910F0[kind]` through `+0x348` / `+0x350`, stamped with
  `00181DD0()` at `+0x3A8`, and made current (`0024B270`–`0024B385`).
- An emitter, on the list whose block is the instance's `+0x1B8` (first node at `+8`, next at
  node `+8`). Its `+0x100` is an `0x800` emitter record and its `+0x108` an `0xA00` element
  definition.
- An element, on its emitter's active list (head `+0x118`, tail `+0x128`, element links `+0x28`
  back and `+0x30` forward) or free list `+0x120`.

### Making an instance current

`0024ED80(instance)` publishes the instance at `02F97348` and its context (`+0x340`) at
`02F97340`, then the context's record tables and the instance's lists: `02EBEF70` = context
`+0x18` (the `0xB00` record store), `02EBEFA8` = `+0x38`, `02EBEFA0` = `+0x840`, `02EBEF90` = `+0x848`
(emitter records), `02EBEF78` = `+0x850` (definitions), `02EBEF98` = instance `+0x120`, `02EBEFB0` =
`+0x130` and `02EBEF88` = `+0x1B8` (`0024ED80`–`0024EDFF`). All the code below reads these globals.

### The update pass

In the field frame, each simulation step runs `00258D70` ([frame update
order](../Engine-Core/frame-update-order.md)). It calls `0024B9B0(0, kind)` for kind 2
when a map bank is loaded (`00258DC7` → `0026F9D0`), then for the kinds 3, 5, 6, 9, 1, 7 and 4 in
that order (`00258DCC`–`00258E0C`); the menu frame's `00258E40` runs kind 3 alone.

`0024B9B0`
refuses kind 8, walks `020910F0[kind]` through `+0x348`, skips an instance whose `+0x3A8` differs
from `00181DD0()`, makes each current (`0024BB6D`) and updates it through `003A7050`
(`0024B9C8`, `0024BA12`–`0024BA65`, `0024BC16`, `0024BE28`).

Below, "the half-rate cadence" means the cadence test `001EDDA0` returning 0
([global state accessors](../Engine-Core/global-state-accessors.md)). `003A8390(dt)`
adds 2 to the instance's frame stamp, the first dword of its `+0x1B8` block, or `2 / [01DFE0B4]` in
the half-rate cadence (`003A839E`–`003A83BB`). It then calls
`0043EF40(emitter, dt)` for each emitter, with the emitter published at `02EBEF80` (`003A83E0`).

### The emitter step

`0043EF40` returns 0 when the emitter has no emitter record (`0043EF8B`). Otherwise it updates every
element on its active list through `002F3910(element, emitter, dt)` (`0043EF9B`–`0043EFC5`). It
then stops emitting when byte `+0x139` is set or its age `+0x2C` has reached a non-zero limit
`+0x28` (`0043EFC7`–`0043EFEB`), and returns whether elements remain.

An emitting emitter adds `dt` to `+0x2C` and keeps the whole frame in `+0x30`. A top-level emitter
(no parent element at `+0x130`) fires when the integer track at emitter record `+0x10`, evaluated
at that frame, is no more than the time since its last firing `+0x34`. In the half-rate cadence it
fires on even frames only. A firing births as many elements as the integer track at record `+0`
gives, each through `00441B30(emitter, age, 0)` (`0043F180`–`0043F1E4`). The tracks are
[authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md).

### Birth

`00441B30(emitter, age, parent)` needs an emitter record and a free element (`00441B5C`–`00441B6D`).
It places the next element through `00442170`, which dispatches on the emitter record's subtype
byte `+0x282` (0 to 8, `0044218A`–`004421B1`), counts the birth in `+0x24`, and takes the head of
the free list (`00441BE1`–`00441C0D`).

When the record's byte `+0x2C4` has bits 0–1 equal to 2 a coin
(`003A6E60(2)`) can put the element at the tail; otherwise it goes to the head (`00441C14`–`00441C9F`).
It samples the record's spawn tracks into the emitter (`+0xA0`–`+0xF0`) and calls the birth
dispatcher `002F3BC0(element, emitter, age)` (`00441CA6`–`00441E71`).

`002F3BC0` bounds the element's type byte at `0xD1` and calls the type's birth method; every birth
method except type `0x70`'s calls the base birth `002F2D60`. Afterwards, unless `00314960()` is 0 or the cadence
test returns non-zero, it adds 1.0 to the age `+0x3C`; it stores `00250000()` at `+0x224` and clears
`+0x226` (`002F3E3F`–`002F3E73`).

`002F2D60` sets `+0x18` to the emitter record and `+0x20` to the definition, returning 0 when either
is missing (`002F2D6F`–`002F2DA2`). It clears bits 1 and 2 of `+1`, sets `+8` to the emitter and
`+0x10` to 0, copies the emitter's position, and reads the lifetime `+0x4C` from the integer track
at record `+0x20` (`002F2DA4`–`002F3029`).

It then copies the sampled spawn values, and the colour `+0x1F0` from the emitter's `+0xF0` when
definition byte `+0x49` has bit `0x2` (else `0x80808080`). It zeroes the age `+0x3C` / `+0x40` and
the update count `+0x48`, copies the definition's type byte `+0x44` into the element's byte `+0`,
marks the eight spawn slots unfired (`+0x1D0`–`+0x1EF` = −1) and stamps `+0x38` with the
instance's frame stamp (`002F302C`–`002F315B`). A type-0 definition fires its spawn slots with
trigger 1 here (`002F317A`–`002F3188`).

### The update

`002F3910(element, emitter, dt)` bounds the type at `0xD1` and jumps to the type's update method
(`002F3910`–`002F3939`); type 0's is the base `002F2530` itself (`002F393C`), and every other
update except type `0x70`'s calls the base, most of them followed by a type tail. The base (`002F2530`):

1. While `+0x224` is set and `00250000()` is 0, clears it and stops unless the cadence test
   returns non-zero (`002F2550`–`002F2572`).
2. Returns 0 when `+0x38` equals the frame stamp, so an element updates at most once per stamp
   and not on the step of its birth; otherwise adds `dt` to `+0x3C` (`002F2574`–`002F2587`).
3. In the half-rate cadence, types `0x67`, `0x68`, `0x6A`, `0x6B`, `0x71`, `0x73` and `0x74` (bit
   set `0x341B` from `0x67`) skip steps whose whole age is odd (`002F258C`–`002F25B0`).
4. With a lifetime set, once the whole age with bit 0 cleared exceeds it, fires the spawn slots with
   trigger 3, releases the element and returns 0 (`002F25B2`–`002F25DD`).
5. Computes `n` = whole age minus `+0x44`; returns 0 when `n` is not positive. Otherwise counts the
   update in `+0x48`, stores the whole age in `+0x40`, and sets `+0x44` to the whole age, or to its
   remainder by definition word `+0x40` when definition byte `+0x47` is set (`002F25E4`–`002F262A`).
6. Returns `n` at once for a definition type of `0xA0` or more; otherwise goes on to sample the
   definition's motion tracks at `+0x44` (`002F262D`–`002F263C`).

### The cull, the release and the spawn slots

The type tails end in one fork: `005002E0(definition, position)` returns 1 to keep and 0 to cull,
and a culled element is released while a kept one fires its spawn slots with trigger 2. The cull
record is the current instance's `+0x2E0`, or the definition's `+0x60` when that record's first
byte is `0xFF` (`005002F9`–`0050030F`).

| Cull record field | Meaning |
|---|---|
| byte `+0` | 1: cull by distance; 2: the same with the Y components zeroed; other: no distance test |
| float `+4`, `+8` | cull when the distance is below `+4` or above `+8` |
| byte `+1` bit 0 | also cull when the point projected through `02AEECB0` is rejected or falls outside `0x6000`–`0xA000` on either screen word |

The distance is from the point at `02AED5F0` to the position transformed by `02AEEA20`, computed
by `002F1D90` (`00500324`–`00500381`, `005003D9`–`00500442`).

The release `002F31C0(element, emitter)` runs the type's release method (types `0x40`–`0xD1`, then
the sub-range table `0043E9C0` for `0x42`–`0xA3`; anything else has none), unlinks the element
from the active list and pushes it on the free list `+0x120` (`002F31CA`–`002F3297`). A culled
element is gone, not hidden.

`003A8950(trigger, element)` walks eight slots of the element's emitter record: tag byte
`+0x298 + i`, emitter-record index `+0x288 + 2i`, start frame `+0x2A0 + 2i`, definition index
`+0x2C6 + 2i`, and the element's last firing `+0x1D0 + 4i` (`003A896E`–`003A899A`).

| Tag | Fires |
|---:|---|
| 0 | never |
| 1 | once, when unfired and the whole age has reached the start frame |
| 2 | on trigger 2 only, not on odd frames in the half-rate cadence: first at the start frame, then whenever the time since the last firing reaches the integer track at the indexed emitter record's `+0x10` |
| 3 | on trigger 3 only, the element's ending |
| other | on every call |

A firing calls `003A8AE0(index, definition, 2, time, …, element)` (`003A8A6C`–`003A8A97`).

### Child emitters

`003A8AE0` looks up the emitter record in `[[02EBEF90]]` and the definition in `[[02EBEF78]]`,
returning 0 when either is missing or the record's word `+0x2B2` is 0 (`003A8AE8`–`003A8B42`). It
reuses a matching emitter (`003A8F80`) or makes one (`003A9100`, `0043F450`), records the parent
element at `+0x130`, and births as many elements as the record's integer track at `+0` gives at
the firing time (`003A8B5C`–`003A8C22`).

### The method tables

Every per-type behaviour is a switch on the element's type byte. Five tables cover the main range
and five more the sub-range `0x42`–`0xAB`, which each main table reaches through its default arm.

| Method | Main dispatcher | Key | Sub-range dispatcher |
|---|---|---|---|
| birth | `002F3BC0` | element `+0` | `0043EBF0` |
| update | `002F3910` | element `+0` | `0043EAB0` |
| draw | `002F4020` | element `+0` minus 1 | `0043ED30` |
| setup | `005004C0` | definition `+0x44` | `00538910` |
| release | `002F31C0` | element `+0` minus `0x40` | `0043E9C0` |

Decoded from the jump tables: 47 types have main birth, update and setup arms, 46 a draw arm and 6 a
release arm; 18 types have sub-range arms (9 with a release). 65 types have an arm somewhere, with
248 distinct handlers; the per-type list is on [effect element types](effect-element-types.md).
`005004C0` runs once per definition, from the `0xA00` record handler.

### The six display layers

`MainLoop_Draw` (`0022B0B0`) asks for effects six times through `00258EE0(layer)`, each request
bracketed by the engine's marker text. The draw-side order inside a layer comes from the grouped
pass `00259030`.

| Layer | Marker | Work |
|---:|---|---|
| 1 | `display VFX [layer : first]` | grouped pass, then `0024C640` |
| 2 | `display VFX [layer : after BG]` | the same |
| 3 | `display VFX [layer : TsEffMan_Layer_AfterOBJ]` | no grouped pass: `0039D570(0)`, `0039D3F0`, a pair of calls chosen on `02F8F310` bit 2, then `003A3990` |
| 4 | `display VFX [layer : in EFF]` | `0039CFF0(0, 0x3C00)`, `0036F550` unless `00181DD0()` is non-zero, grouped pass, `0039CFF0(0, 0x3700)`, `0024C640` |
| 5 | `display VFX [layer : after EFF & MENU]` | `0036F9F0` unless `00181DD0()` is non-zero, then the grouped pass |
| 6 | the same text as 5 | grouped pass |

`00259030(layer)` selects arena 8, calls `0024D370(layer, group)` for groups 2, 3, 5, 6, 9, 1, 7 and
4, then drains the draw list (`003A3740`) (`00259036`–`002590C0`). A group is an instance kind.

### Drawing one group

`0024D370(layer, group)` takes the list `020910F0[group]` and asks the group gate `0024D4E0`
(`0024D382`–`0024D3AF`). The gate refuses group 8; groups 1–4 and 7 need bit `group − 1` in the AND
of `02092162`, `02092164` and `02092166`; group 2 also needs `02F8F29E` bit 0 clear and group 5
`02EBEF68` bit 0 clear (`0024D4E0`–`0024D538`).

For each instance the group draw publishes the group at `02092700` and skips the instance unless
its `+0x3A8` equals `00181DD0()`, the high nibble of its word `+0x378` equals the layer, and the
per-instance gate `0024D770(instance, 1)` passes (`0024D3C0`–`0024D3FC`). It makes the instance
current and walks its emitters through `003A72F0` → `003A8D80`, which calls `00441970` for each
(`0024D405`, `0024D499`, `003A8D84`–`003A8DAB`). So an effect's layer is authored in its
instance.

`00441970(emitter)` returns when the emitter has no elements. Unless the instance's flag byte
`+0x36A` has bit 0, only emitters whose definition type is `0x40`, `0x41`, `0xA1`, `0xA2`, `0xA5`
or `0xD0` are drawn (`0044198E`–`004419CE`; the table is
`effect-element-runtime-effect-kind-441970.tsv`). It sets the pass nibble `02AEE910`: definition
byte `+0x4C` when `+0x4A` is `0x40` or more, else 8 (`004419F5`–`00441A0E`).

It then calls `002F4020(element, emitter)` for each element, forward from the head, or backward from
the tail when the emitter record's byte `+0x2C4` has bits 0–1 set (`00441A15`–`00441A82`).

### Drawing one element

`002F4020` returns when the type byte is outside `[022BE7D8]`..`[01EEBAE0]`, or when `+0x224` is set
while the cadence test returns 0 (`002F402A`–`002F405B`). With definition byte `+0x4D` non-zero, a
counter in word `+2` and the cadence test set a skip bit in byte `+1` bit 0, and a set bit skips
the draw (`002F4070`–`002F40E6`). It stores definition byte `+0x75` at `02AEF41C`, calls the type's
draw method, and clears `02AEF41C` again (`002F40EC`–`002F4124`, `002F4369`).

### The draw list

Blended primitives do not draw at once. An emitter appends a `0x28`-byte entry to the list at
`[02F8F2F8]`, counted by the word `02F8F2C6`; the point emitter `0039D970`, for one, writes the
projected depth word as the sort key `+8` and ORs the pass nibble into bits 28–31
(`0039D986`–`0039DA05`). `003A3670` allocates the list, `0x190000` bytes, which is 40,960 entries.

`003A3740` drains it. It returns for an empty list, sorts the entries by `+8` (`003A3A50`), and for
each entry calls the function at `+0x10` with `+0x00`; without one, it submits the command at
`+0x18` through `0020E630(command, 2)`, or with flag bit `0x4` defers it to `02AEF420` for layer 3's
`003A3990` (`003A3744`–`003A3908`). It empties the list and keeps the last and peak counts
(`003A3929`–`003A3973`).

`0024D540`, the frame's draw setup, drains once more and then rewinds: `003A3A00` resets the packet
cursor `02F8F2D0` to the arena base `02F8F308`, sets its end `02F8F2D8`, and zeroes the count
(`0024D556`, `0024D55B`, `003A3A00`–`003A3A42`).

### Target and anchor queries

Some tails ask for a point from a sub-record. `002F3360` switches on the sub-record's byte `+0x90`;
value 3 calls `003A56F0`, which samples a vector track (`00430B90`) and switches on the byte `+0x48`
minus 1 over 14 cases (`002F3384`–`002F33EA`, `003A575E`–`003A5797`). `003A4290` has the same
14-case switch on the same byte (`003A4303`–`003A4319`).

Their arms are in
`effect-element-runtime-switch-family-3a42-3a56.tsv`; `effect-element-runtime-switch-family-frontier-decode.tsv`
decodes `00442170` and `00442460` (the emitter-record subtype switches) and the record-store
fronts `00500980` / `00500850`, together with dispatchers outside the effect code.

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
  `001EDDA0`.
