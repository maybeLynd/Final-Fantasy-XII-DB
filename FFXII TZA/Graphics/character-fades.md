---
title: "Character fades: the ten fade channels, their owners and the coast-down latch"
kind: "system"
category: "Graphics"
addresses: "003E5D60, 003E5D00, 003E5D30, 003E4370, 00428940, 004293C0, 00520180, 002E8B10, 00428C40, 002E84B0, 002E8500, 0033F530, 0033FAD0, 0042E1F0, 0042F880, 0042E850, 0042D7A0, 003E48E0, 003E4240, 003E4730, 003E4780, 003E51F0, 0042CBF0, 004FD4B0, 002E83A0, 002EBC30, 0042ED30, 00424080, 004256E0, 01DFE0B4, 01F82E38"
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

The channels are eight bytes each at record `+4C0`<sub>h</sub>; channel `n` is at `+4C0h + 8n`:

```
+0x0  i16  base, Q12 (0x1000 = 1.0)
+0x2  i16  delta: target - base
+0x4  i16  progress, 0 to 0x1000
+0x6  i16  step per update; 0 = at rest
value = base + ((delta * progress) >> 12)
```

- `003E5D60(record, n, target, frames)` starts a ramp. It first folds the current progress into the
  base, so an interrupted ramp continues from where it is, then sets `delta = target × 4096 − base` and
  `step = 1000h / (max(frames, 1) × [01DFE0B4])`. Progress restarts at one step, or at 0 for channel 1,
  and gains one more step when `01F82E38` is set.
- `003E5D00(record, n, value)` sets a channel at once: base `value × 4096`, the rest 0. The record clear
  `0041F730` sets all ten to 1.0; `003E5D30` puts channels 0, 1 and 4 back to 1.0.
- `00428940(record, n, value, frames)` is the forwarder most writers use: one frame or fewer sets the
  channel at once, more starts a ramp. `004293C0` is the same with a flag that redirects the write to
  the record's first child.
- `003E4370(record)` advances every channel with a non-zero step: progress grows by the step up to
  `1000`<sub>h</sub>, and on the update after it arrives the delta is folded into the base and the channel rests.
  It runs from `0042C410` and `0042C8F0`, the root and child callbacks of the hierarchy walk
  `00426090` starts in each simulation step.

`01DFE0B4` is 1 at 30 fps and 2 at 60, and `01F82E38` is set at 60
([startup constants](../Engine-Core/startup-constants.md)), so a ramp takes the same time at
either rate.

### Who writes which channel

| Channel | Offset | Writer | Meaning |
|---:|---|---|---|
| 0 | `+4C0`<sub>h</sub> | `0042E850` | distance fade; 0 over one frame when culled |
| 1 | `+4C8`<sub>h</sub> | `0042E1F0`, `0042F880`, command `23`<sub>h</sub> (`00520180` → `004293C0`) | attached-piece visibility |
| 2 | `+4D0`<sub>h</sub> | `002E8B10` → `00428940` | time-stop fade ([time stop and freeze](../Engine-Core/time-stop-and-freeze.md)) |
| 3 | `+4D8`<sub>h</sub> | the record clear only | stays at 1.0 |
| 4 | `+4E0`<sub>h</sub> | `0042E850` | viewer-inside fade |
| 5 | `+4E8`<sub>h</sub> | `0051DC90`, `0051E0A0`, `0051E3A0` → `00428940`, one frame | status look ([character status visuals](character-status-visuals.md)) |
| 6-9 | `+4F0`<sub>h</sub>..`+508`<sub>h</sub> | `00428C40(record, r, g, b, a, frames)` | script colour |

`00428C40` starts all four ramps with one frame count. `rgbatrans` (`3B2`<sub>h</sub>, `0033F530`) reaches it
through `002E84B0` and `puppetrgbatrans` (`535`<sub>h</sub>, `0033FAD0`) through `002E8500`; both pass the
popped frame count plus one. A sweep of every reference to `003E5D60`, `003E5D00`, `00428940` and
`004293C0`, conditional jumps included, finds no write of channel 3 and those listed above for the
others; the direct calls are in
[the channel census](character-fades-fade-channel-census.tsv).

### Attached pieces (channel 1)

A piece is a record whose kind byte `+6A0`<sub>h</sub> (from the model's `@FCP` data) is `1C`<sub>h</sub> or above. When a
record's dirty handler `0042AC30` runs (`+290`<sub>h</sub> bit 31 or `+294`<sub>h</sub> bit 3), it passes every descendant
to `0042E1F0`. For a piece whose parent's kind is `11`<sub>h</sub> to `15`<sub>h</sub>, the parent's parent decides:

- its `+284`<sub>h</sub> bit 27 is set, or its event's index (`+CCh & FFFh`) is `35`<sub>h</sub>: channel 1 is set to 0
  at once;
- otherwise, when bits 0-1 of the handled record's `+40B`<sub>h</sub> are both clear, a ramp to 0 over five
  frames;
- otherwise it is set to 1.0 at once.

`0042F880`, the handler that completes a pending attachment (owner at `+3CE`<sub>h</sub>, slot at `+3CC`<sub>h</sub>),
applies the same test for slot `10A`<sub>h</sub> and sets channel 1 to 0 at once when the bits are clear, so the
piece arrives hidden.

### Distance fade and cull (channels 0 and 4)

`0042E850(record)` runs through `0042D7A0` for every record with `+284`<sub>h</sub> bit 2 set, `+2AE`<sub>h</sub> bit 1
clear and no parent.
It clears the three cull bits of `+D3`<sub>h</sub> and measures a distance `d`: from the camera, or from the
reference record at tail `+2C`<sub>h</sub> when that record is live (0 for the reference record itself). With
tail flag bit 0 on:

- `+D3`<sub>h</sub> bit 0: the record fails the visibility test `0046C180` and has `+284`<sub>h</sub> bit 21 and `+D2`<sub>h</sub>
  bit 0;
- `+D3`<sub>h</sub> bit 1: distance fade applies (`+D2`<sub>h</sub> bits 4 and 1) and `d ≥ start + range`;
- `+D3`<sub>h</sub> bit 3: the record has `+284`<sub>h</sub> bit 21 and `+D2`<sub>h</sub> bit 3, and its view depth plus its extent is
  below minus the near limit at tail `+20`<sub>h</sub>.

- `puppet_setcharclipone(d, v)` (`0569`<sub>h</sub>, `00340890`) sets two of these inputs on the render record
  of puppet `d` (`003EB700`) when it is live: `003EB8C0` writes `v` into bit 4 of `+D2`<sub>h</sub>, and
  `003EB960` writes it into bit 3 of `+304`<sub>h</sub> and raises bit 6 of `+290`<sub>h</sub>, whose processor
  `0042BCB0` copies that bit into bit 21 of the children's `+284`<sub>h</sub>.

When `005C5230()` returns non-zero, or record `+6E0`<sub>h</sub> is non-zero, the bits are cleared and no
distance fade applies. A culled record gets channels 0 and 4 ramped to 0 over one frame. Otherwise
channel 0 ramps over one frame to 1.0 when `d ≤ start` and to `sin(((start + range − d) / range) ×
π/2)` inside the band, `start` and `range` being tail `+1C`<sub>h</sub> and `+24`<sub>h</sub>.

The viewer-inside test runs only with tail flag bit 4 set. When the camera's horizontal distance to
the character is below record `+2A8`<sub>h</sub>, plus 0.15 while the character is already faded, and the
camera's height is within the character's half-height band, channel 4 ramps to 0 over three frames
and `+4B7`<sub>h</sub> bit 5 is cleared; otherwise it ramps to 1.0 and the bit is set.

The settings are the record system's tail ([character render records](character-render-records.md)):

- `setcharclipdistance` (`327`<sub>h</sub>, `00348B00`) pops two floats: the first to `+24`<sub>h</sub> (`002E83A0`), the
  second to `+1C`<sub>h</sub> (`002EBC30`);
- `setcharclipfaderange` (`328`<sub>h</sub>, `003493F0`) pops one float into `+24`<sub>h</sub>;
- `0042ED30` restores 34.0 and 4.0 and flag bits 0 and 2.

### Reading the channels

`003E48E0(record, selector)` returns one channel's value for selectors 0 to 9, or a product,
renormalised after every factor:

| Selector | Product of channels |
|---|---|
| `0B`<sub>h</sub> | 0, 1, 2, 3, 4 |
| `0D`<sub>h</sub> | 1, 2, 3, 5 |
| `0E`<sub>h</sub> | 0, 1, 2, 3, 4, 5 |

`003E4240(record, parent)` stores the six-channel product in the word `+4B4`<sub>h</sub>, multiplied by the
parent's `+4B4`<sub>h</sub> when there is a parent, so a piece inherits its owner's fade. `003E4730` turns it into
`(+4B4h / 4096) × [+22Ch] × [+2ECh] / 255`; `003E4780` takes the last factor from its caller.
`003E51F0` returns channels 6 to 9 as four floats divided by 4096.

### The fog block

The factor `+2EC`<sub>h</sub> in the composite is the last of four floats at `+2E0`<sub>h</sub>: a fog colour (`+2E0`<sub>h</sub>,
`+2E4`<sub>h</sub>, `+2E8`<sub>h</sub>, 0 to 255) and a fog amount (`+2EC`<sub>h</sub>, 0 to 255). `0041E960(record)` computes
them each frame. With `+284`<sub>h</sub> bit 29 clear they are 0, 0, 0 and 255. Otherwise it takes the global
fog from `003ED0E0`: the far distance `02EBB7E8`, the scale `255 / (far − near)` with near
`02EBB7E4`, the floor `255 − [02EBB7EF]`, and the colour bytes `02EBB7EC`–`02EBB7EE`.

`0041EC00` sets the record's depth `+2DC`<sub>h</sub>: the w of its projected origin, replaced by the w of a
point at the record's distance from the camera position `02AEDF20` (`005213B0`) straight down the
view when that w exceeds 1 in size (negated for a point behind). The depth gives the raw amount `(far − w) × scale` and the
clamped amount `a` between the floor and 255, and `t = 1 − (a − floor) / (255 − floor)`. With `k` and
the colour `c` from the type-`41`<sub>h</sub> pool below (`003E4E70` returns `1 − k`):

- the colour is `t × fog × k + c × 255 × (1 − k)` per channel, clamped to 0..255;
- the amount is the larger of `raw × k` and `2 × t × c.a × (1 − k) + floor × k`, at most 255.

`0042D050` and `0042CBF0` call it. For an attached record `0042CBF0` takes the parent's projected
point with w + 2 and copies the fog block of the top ancestor, or of the highest one with `+284`<sub>h</sub>
bit 14 (`00202C90`); it computes the record's own block only when that ancestor's word `+2CA`<sub>h</sub>
names the record and `003B4750` finds a pool record for it. A record whose parent is gone is
detached and computes its own (`0041EC00`, `0041E960`).

### The type-`41`<sub>h</sub> pool

Effect type `41`<sub>h</sub> keeps records in the 64-entry pool of `60`<sub>h</sub>-byte records at `[02B404E0]`
([effect element types](effect-element-types.md)), linked in an active list (head `02B404C8`, tail
`02B404D0`, links `+08`<sub>h</sub> and `+10`<sub>h</sub>) and named by `serial << 8 | slot`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | handle |  |
| `04`<sub>h</sub> | `u16` | age in steps; | +`06`<sub>h</sub> u16 frame in the period |
| `20`<sub>h</sub> | `u8` | curve number (3: no curve) |  |
| `21`<sub>h</sub> | `u8` | bits 0-6: 1 linear, other smoothed; bit 7: half strength |  |
| `22`<sub>h</sub> | `u8` | target kind: 1 a render record, 2 a test through 0024E2F0 / 0024E6D0 |  |
| `23`<sub>h</sub> | `u8` | target mode; | +`24`<sub>h</sub> u32 target id |
| `28`<sub>h</sub> | `u16` | lifetime in steps (0: none); | +`2A`<sub>h</sub> u16 period in steps |
| `2C`<sub>h</sub> | `u8` | priority; | +`2D`<sub>h</sub> u8 mask tested against `02B404C1` |
| `30`<sub>h</sub> | `f32` | strength; | +`34`<sub>h</sub> f32 weight |
| `38`<sub>h</sub> | `f32` | 1 / period; | +`3C`<sub>h</sub> f32 phase, 0 to 1 |
| `40`<sub>h</sub> | `f32[4]` | colour | (r, g, b, a); +`4C`<sub>h</sub> is also the lowest weight |
| `50`<sub>h</sub> | `u32` | stamp from 00181DD0() |  |

- `003B4840`, from `00258D70` and `00258E40`, steps every record whose stamp is non-zero or while
  `00181DD0()` returns 0: it adds one to the age and the frame, wraps the frame past the period,
  sets the phase to `frame / period` (at most 1), and unlinks the record once its age passes a
  non-zero lifetime. `003B42B0(handle)` unlinks one record.
- `003B49E0(handle)` restarts a record: age, frame, phase, the byte `+2E`<sub>h</sub> and the weight to 0,
  and `+38`<sub>h</sub> to `1 / period`. `003B4770(handle)` returns the record's `+20`<sub>h</sub> part when the handle
  still matches.
- `003B4A50(index, out)` collects the records that apply to a render record, walking the list and
  stopping at the first record of lower priority once one has matched; a record is skipped while
  its mask shares a bit with `02B404C1`, which the frame setup `0024D540` sets and clears with
  `003B4A30` and `003B4A40`.
- `003B4310(index, out)` evaluates each collected record's curve (a key table per curve number at
  `02B404E8`) at its phase, scales it by the strength into the weight, keeps it at least `+4C`<sub>h</sub>,
  and returns the colour and weight of the record whose luma (`0.299 r + 0.587 g + 0.114 b`) times
  weight is lowest. With no record it returns weight 1.

### Into the model instance

For an attached record `0042CBF0` runs the three readers above, stores `+49C`<sub>h</sub> = composite × script
alpha, and writes the record's model instance:

- `+90`<sub>h</sub> = the colour `+210`<sub>h</sub>;
- `+A0`<sub>h</sub> = the second colour `+220`<sub>h</sub> × the script colour;
- `+B0`<sub>h</sub> = the Q12 composite `+4B4`<sub>h</sub>.

With `+284`<sub>h</sub> bit 26 and a live parent, `+90`<sub>h</sub> comes from the parent's `+210`<sub>h</sub> and `+A0`<sub>h</sub> from the
parent's instance `+A0`<sub>h</sub> × this record's product. The draw setup `004FD4B0` then multiplies the
character's ambient light by `+A0`<sub>h</sub>..`+A8`<sub>h</sub> and its alpha by `+ACh × +B0h / 4096`
([character lighting and shadows](character-lighting-and-shadows.md)).

### The coast-down latch

The movement step asks `00424080(record, &heading, &speed)` before it turns heading and speed into a
position change ([heading and speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md),
which lists every branch). The record keeps a live block at `+610`<sub>h</sub> (heading, speed, accumulator,
flags) and a cached block at `+620`<sub>h</sub>; bit 0 of the word `+62C`<sub>h</sub> is the latch.

1. Latched: the cached speed is multiplied by 0.83 and returned with the cached heading; the latch
   clears once the speed is 0.05 or less. A speed of 1.0 is released on the 17th call.
2. Not latched, for a root record with `+284`<sub>h</sub> bit 27: when the event index (`+CCh & FFFh`) is
   `10`<sub>h</sub>, the requested speed is exactly 0 and the byte `+457`<sub>h</sub> has reached `30 × [01DFE0B4]`, the
   latch is armed and the first decayed value is returned at once.
3. Otherwise, for such a record, the live block moves to the cache and the new heading and speed
   become the live pair, so the cache is always one call behind.

`+457`<sub>h</sub> is advanced by `004256E0`, the record's locomotion selector, in its states 2 and 9 to 11, and
capped at `90 × [01DFE0B4]`; its 16-bit store of 0 at `+456`<sub>h</sub> resets it.

After the latch, when the record has a presentation entry whose resolved data has byte `+1` equal to 1,
events `35`<sub>h</sub> and `36`<sub>h</sub> multiply the accumulator by 0.9 and the speed by the result, event `0D`<sub>h</sub>
forces the speed to 0, and any other event resets the accumulator to 1.0.

## Modding notes

- To fade a character from script without fighting the engine, use the channels it leaves alone:
  `rgbatrans` owns 6 to 9, and nothing but the clear writes channel 3.
- Selector `0B`<sub>h</sub> leaves channel 5 out; whatever reads it ignores Invisibility.
- The glide's feel is the two constants in `00424080`: 0.83 per call and the 0.05 floor.

## Related

- [Character render records](character-render-records.md): the record, its tail settings and the walks.
- [Character lighting and shadows](character-lighting-and-shadows.md): where the fade meets the ambient light.
- [CharacterRenderObject](character-render-object.md): the model instance layout.
- [Character status visuals](character-status-visuals.md): channel 5.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): channel 2.
- [Heading and speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md):
  the caller of the latch.
- [Startup constants](../Engine-Core/startup-constants.md): the frame-rate multiplier.
