---
title: "Character fades: the ten fade channels, their owners and the coast-down latch"
kind: "system"
category: "Graphics"
addresses: "0x003E5D60, 0x003E5D00, 0x003E5D30, 0x003E4370, 0x00428940, 0x004293C0, 0x00520180, 0x002E8B10, 0x00428C40, 0x002E84B0, 0x002E8500, 0x0033F530, 0x0033FAD0, 0x0042E1F0, 0x0042F880, 0x0042E850, 0x0042D7A0, 0x003E48E0, 0x003E4240, 0x003E4730, 0x003E4780, 0x003E51F0, 0x0042CBF0, 0x004FD4B0, 0x002E83A0, 0x002EBC30, 0x0042ED30, 0x00424080, 0x004256E0, 0x01DFE0B4, 0x01F82E38"
---

## What the player sees

A character does not have one opacity. Its render record carries ten fade channels, and what is drawn
is a product of several of them, so separate effects never fight:

- a character at the edge of view distance fades in over a band instead of popping, and is gone in one
  frame when culled;
- when the camera moves inside a character, that character fades out over three frames and back in
  over three when the camera leaves;
- a weapon or other attached piece can be hidden at once or over five frames, and always takes on its
  owner's fade;
- the actors a time stop removes fade out and back in;
- Invisibility holds a character at a low opacity;
- the script verb `rgbatrans` recolours and fades an actor over a number of frames.

A character that stops after a sustained run can also glide to a halt over a few frames instead of
stopping dead; that is the coast-down latch at the end of this page.

## How it works

### One channel

The channels are eight bytes each at record `+0x4C0`; channel `n` is at `+0x4C0 + 8n`:

```
+0x0  i16  base, Q12 (0x1000 = 1.0)
+0x2  i16  delta: target - base
+0x4  i16  progress, 0 to 0x1000
+0x6  i16  step per update; 0 = at rest
value = base + ((delta * progress) >> 12)
```

- `0x003E5D60(record, n, target, frames)` starts a ramp. It first folds the current progress into the
  base, so an interrupted ramp continues from where it is, then sets `delta = target × 4096 − base` and
  `step = 0x1000 / (max(frames, 1) × [0x01DFE0B4])`. Progress restarts at one step, or at 0 for channel 1,
  and gains one more step when `0x01F82E38` is set.
- `0x003E5D00(record, n, value)` sets a channel at once: base `value × 4096`, the rest 0. The record clear
  `0x0041F730` sets all ten to 1.0; `0x003E5D30` puts channels 0, 1 and 4 back to 1.0.
- `0x00428940(record, n, value, frames)` is the forwarder most writers use: one frame or fewer sets the
  channel at once, more starts a ramp. `0x004293C0` is the same with a flag that redirects the write to
  the record's first child.
- `0x003E4370(record)` advances every channel with a non-zero step: progress grows by the step up to
  `0x1000`, and on the update after it arrives the delta is folded into the base and the channel rests.
  It runs from `0x0042C410` and `0x0042C8F0`, the root and child callbacks of the hierarchy walk
  `0x00426090` starts in each simulation step.

`0x01DFE0B4` is 1 at 30 fps and 2 at 60, and `0x01F82E38` is set at 60
([startup constants](../Engine-Core/startup-constants.md)), so a ramp takes the same time at
either rate.

### Who writes which channel

| Channel | Offset | Writer | Meaning |
|---:|---|---|---|
| 0 | `+0x4C0` | `0x0042E850` | distance fade; 0 over one frame when culled |
| 1 | `+0x4C8` | `0x0042E1F0`, `0x0042F880`, command `0x23` (`0x00520180` → `0x004293C0`) | attached-piece visibility |
| 2 | `+0x4D0` | `0x002E8B10` → `0x00428940` | time-stop fade ([time stop and freeze](../Engine-Core/time-stop-and-freeze.md)) |
| 3 | `+0x4D8` | the record clear only | stays at 1.0 |
| 4 | `+0x4E0` | `0x0042E850` | viewer-inside fade |
| 5 | `+0x4E8` | `0x0051DC90`, `0x0051E0A0`, `0x0051E3A0` → `0x00428940`, one frame | status look ([character status visuals](character-status-visuals.md)) |
| 6-9 | `+0x4F0`..`+0x508` | `0x00428C40(record, r, g, b, a, frames)` | script colour |

`0x00428C40` starts all four ramps with one frame count. `rgbatrans` (`0x3B2`, `0x0033F530`) reaches it
through `0x002E84B0` and `puppetrgbatrans` (`0x535`, `0x0033FAD0`) through `0x002E8500`; both pass the
popped frame count plus one. A sweep of every reference to `0x003E5D60`, `0x003E5D00`, `0x00428940` and
`0x004293C0`, conditional jumps included, finds no write of channel 3 and those listed above for the
others; the direct calls are in
[the channel census](character-fades-fade-channel-census.tsv).

### Attached pieces (channel 1)

A piece is a record whose kind byte `+0x6A0` (from the model's `@FCP` data) is `0x1C` or above. When a
record's dirty handler `0x0042AC30` runs (`+0x290` bit 31 or `+0x294` bit 3), it passes every descendant
to `0x0042E1F0`. For a piece whose parent's kind is `0x11` to `0x15`, the parent's parent decides:

- its `+0x284` bit 27 is set, or its event's index (`+0xCC & 0xFFF`) is `0x35`: channel 1 is set to 0
  at once;
- otherwise, when bits 0-1 of the handled record's `+0x40B` are both clear, a ramp to 0 over five
  frames;
- otherwise it is set to 1.0 at once.

`0x0042F880`, the handler that completes a pending attachment (owner at `+0x3CE`, slot at `+0x3CC`),
applies the same test for slot `0x10A` and sets channel 1 to 0 at once when the bits are clear, so the
piece arrives hidden.

### Distance fade and cull (channels 0 and 4)

`0x0042E850(record)` runs through `0x0042D7A0` for every record with `+0x284` bit 2 set, `+0x2AE` bit 1
clear and no parent.
It clears the three cull bits of `+0xD3` and measures a distance `d`: from the camera, or from the
reference record at tail `+0x2C` when that record is live (0 for the reference record itself). With
tail flag bit 0 on:

- `+0xD3` bit 0: the record fails the visibility test `0x0046C180` and has `+0x284` bit 21 and `+0xD2`
  bit 0;
- `+0xD3` bit 1: distance fade applies (`+0xD2` bits 4 and 1) and `d ≥ start + range`;
- `+0xD3` bit 3: the record has `+0x284` bit 21 and `+0xD2` bit 3, and its view depth plus its extent is
  below minus the near limit at tail `+0x20`.

- `puppet_setcharclipone(d, v)` (`0x0569`, `0x00340890`) sets two of these inputs on the render record
  of puppet `d` (`0x003EB700`) when it is live: `0x003EB8C0` writes `v` into bit 4 of `+0xD2`, and
  `0x003EB960` writes it into bit 3 of `+0x304` and raises bit 6 of `+0x290`, whose processor
  `0x0042BCB0` copies that bit into bit 21 of the children's `+0x284`.

When `0x005C5230()` returns non-zero, or record `+0x6E0` is non-zero, the bits are cleared and no
distance fade applies. A culled record gets channels 0 and 4 ramped to 0 over one frame. Otherwise
channel 0 ramps over one frame to 1.0 when `d ≤ start` and to `sin(((start + range − d) / range) ×
π/2)` inside the band, `start` and `range` being tail `+0x1C` and `+0x24`.

The viewer-inside test runs only with tail flag bit 4 set. When the camera's horizontal distance to
the character is below record `+0x2A8`, plus 0.15 while the character is already faded, and the
camera's height is within the character's half-height band, channel 4 ramps to 0 over three frames
and `+0x4B7` bit 5 is cleared; otherwise it ramps to 1.0 and the bit is set.

The settings are the record system's tail ([character render records](character-render-records.md)):

- `setcharclipdistance` (`0x327`, `0x00348B00`) pops two floats: the first to `+0x24` (`0x002E83A0`), the
  second to `+0x1C` (`0x002EBC30`);
- `setcharclipfaderange` (`0x328`, `0x003493F0`) pops one float into `+0x24`;
- `0x0042ED30` restores 34.0 and 4.0 and flag bits 0 and 2.

### Reading the channels

`0x003E48E0(record, selector)` returns one channel's value for selectors 0 to 9, or a product,
renormalised after every factor:

| Selector | Product of channels |
|---|---|
| `0x0B` | 0, 1, 2, 3, 4 |
| `0x0D` | 1, 2, 3, 5 |
| `0x0E` | 0, 1, 2, 3, 4, 5 |

`0x003E4240(record, parent)` stores the six-channel product in the word `+0x4B4`, multiplied by the
parent's `+0x4B4` when there is a parent, so a piece inherits its owner's fade. `0x003E4730` turns it into
`(+0x4B4 / 4096) × [+0x22C] × [+0x2EC] / 255`; `0x003E4780` takes the last factor from its caller.
`0x003E51F0` returns channels 6 to 9 as four floats divided by 4096.

### The fog block

The factor `+0x2EC` in the composite is the last of four floats at `+0x2E0`: a fog colour (`+0x2E0`,
`+0x2E4`, `+0x2E8`, 0 to 255) and a fog amount (`+0x2EC`, 0 to 255). `0x0041E960(record)` computes
them each frame. With `+0x284` bit 29 clear they are 0, 0, 0 and 255. Otherwise it takes the global
fog from `0x003ED0E0`: the far distance `0x02EBB7E8`, the scale `255 / (far − near)` with near
`0x02EBB7E4`, the floor `255 − [0x02EBB7EF]`, and the colour bytes `0x02EBB7EC`–`0x02EBB7EE`.

`0x0041EC00` sets the record's depth `+0x2DC`: the w of its projected origin, replaced by the w of a
point at the record's distance from the camera position `0x02AEDF20` (`0x005213B0`) straight down the
view when that w exceeds 1 in size (negated for a point behind). The depth gives the raw amount `(far − w) × scale` and the
clamped amount `a` between the floor and 255, and `t = 1 − (a − floor) / (255 − floor)`. With `k` and
the colour `c` from the type-`0x41` pool below (`0x003E4E70` returns `1 − k`):

- the colour is `t × fog × k + c × 255 × (1 − k)` per channel, clamped to 0..255;
- the amount is the larger of `raw × k` and `2 × t × c.a × (1 − k) + floor × k`, at most 255.

`0x0042D050` and `0x0042CBF0` call it. For an attached record `0x0042CBF0` takes the parent's projected
point with w + 2 and copies the fog block of the top ancestor, or of the highest one with `+0x284`
bit 14 (`0x00202C90`); it computes the record's own block only when that ancestor's word `+0x2CA`
names the record and `0x003B4750` finds a pool record for it. A record whose parent is gone is
detached and computes its own (`0x0041EC00`, `0x0041E960`).

### The type-0x41 pool

Effect type `0x41` keeps records in the 64-entry pool of `0x60`-byte records at `[0x02B404E0]`
([effect element types](effect-element-types.md)), linked in an active list (head `0x02B404C8`, tail
`0x02B404D0`, links `+0x08` and `+0x10`) and named by `serial << 8 | slot`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | handle |  |
| `+0x04` | `u16` | age in steps; | +`0x06` u16 frame in the period |
| `+0x20` | `u8` | curve number (3: no curve) |  |
| `+0x21` | `u8` | bits 0-6: 1 linear, other smoothed; bit 7: half strength |  |
| `+0x22` | `u8` | target kind: 1 a render record, 2 a test through 0x0024E2F0 / 0x0024E6D0 |  |
| `+0x23` | `u8` | target mode; | +`0x24` u32 target id |
| `+0x28` | `u16` | lifetime in steps (0: none); | +`0x2A` u16 period in steps |
| `+0x2C` | `u8` | priority; | +`0x2D` u8 mask tested against `0x02B404C1` |
| `+0x30` | `f32` | strength; | +`0x34` f32 weight |
| `+0x38` | `f32` | 1 / period; | +`0x3C` f32 phase, 0 to 1 |
| `+0x40` | `f32[4]` | colour | (r, g, b, a); +`0x4C` is also the lowest weight |
| `+0x50` | `u32` | stamp from 0x00181DD0() |  |

- `0x003B4840`, from `0x00258D70` and `0x00258E40`, steps every record whose stamp is non-zero or while
  `0x00181DD0()` returns 0: it adds one to the age and the frame, wraps the frame past the period,
  sets the phase to `frame / period` (at most 1), and unlinks the record once its age passes a
  non-zero lifetime. `0x003B42B0(handle)` unlinks one record.
- `0x003B49E0(handle)` restarts a record: age, frame, phase, the byte `+0x2E` and the weight to 0,
  and `+0x38` to `1 / period`. `0x003B4770(handle)` returns the record's `+0x20` part when the handle
  still matches.
- `0x003B4A50(index, out)` collects the records that apply to a render record, walking the list and
  stopping at the first record of lower priority once one has matched; a record is skipped while
  its mask shares a bit with `0x02B404C1`, which the frame setup `0x0024D540` sets and clears with
  `0x003B4A30` and `0x003B4A40`.
- `0x003B4310(index, out)` evaluates each collected record's curve (a key table per curve number at
  `0x02B404E8`) at its phase, scales it by the strength into the weight, keeps it at least `+0x4C`,
  and returns the colour and weight of the record whose luma (`0.299 r + 0.587 g + 0.114 b`) times
  weight is lowest. With no record it returns weight 1.

### Into the model instance

For an attached record `0x0042CBF0` runs the three readers above, stores `+0x49C` = composite × script
alpha, and writes the record's model instance:

- `+0x90` = the colour `+0x210`;
- `+0xA0` = the second colour `+0x220` × the script colour;
- `+0xB0` = the Q12 composite `+0x4B4`.

With `+0x284` bit 26 and a live parent, `+0x90` comes from the parent's `+0x210` and `+0xA0` from the
parent's instance `+0xA0` × this record's product. The draw setup `0x004FD4B0` then multiplies the
character's ambient light by `+0xA0`..`+0xA8` and its alpha by `+0xAC × +0xB0 / 4096`
([character lighting and shadows](character-lighting-and-shadows.md)).

### The coast-down latch

The movement step asks `0x00424080(record, &heading, &speed)` before it turns heading and speed into a
position change ([heading and speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md),
which lists every branch). The record keeps a live block at `+0x610` (heading, speed, accumulator,
flags) and a cached block at `+0x620`; bit 0 of the word `+0x62C` is the latch.

1. Latched: the cached speed is multiplied by 0.83 and returned with the cached heading; the latch
   clears once the speed is 0.05 or less. A speed of 1.0 is released on the 17th call.
2. Not latched, for a root record with `+0x284` bit 27: when the event index (`+0xCC & 0xFFF`) is
   `0x10`, the requested speed is exactly 0 and the byte `+0x457` has reached `30 × [0x01DFE0B4]`, the
   latch is armed and the first decayed value is returned at once.
3. Otherwise, for such a record, the live block moves to the cache and the new heading and speed
   become the live pair, so the cache is always one call behind.

`+0x457` is advanced by `0x004256E0`, the record's locomotion selector, in its states 2 and 9 to 11, and
capped at `90 × [0x01DFE0B4]`; its 16-bit store of 0 at `+0x456` resets it.

After the latch, when the record has a presentation entry whose resolved data has byte `+1` equal to 1,
events `0x35` and `0x36` multiply the accumulator by 0.9 and the speed by the result, event `0x0D`
forces the speed to 0, and any other event resets the accumulator to 1.0.

## Modding notes

- To fade a character from script without fighting the engine, use the channels it leaves alone:
  `rgbatrans` owns 6 to 9, and nothing but the clear writes channel 3.
- Selector `0x0B` leaves channel 5 out; whatever reads it ignores Invisibility.
- The glide's feel is the two constants in `0x00424080`: 0.83 per call and the 0.05 floor.

## Related

- [Character render records](character-render-records.md): the record, its tail settings and the walks.
- [Character lighting and shadows](character-lighting-and-shadows.md): where the fade meets the ambient light.
- [CharacterRenderObject](character-render-object.md): the model instance layout.
- [Character status visuals](character-status-visuals.md): channel 5.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): channel 2.
- [Heading and speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md):
  the caller of the latch.
- [Startup constants](../Engine-Core/startup-constants.md): the frame-rate multiplier.
