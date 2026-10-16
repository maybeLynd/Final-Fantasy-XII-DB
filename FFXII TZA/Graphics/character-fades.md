---
title: "Character fades: the ten fade channels, their owners and the coast-down latch"
kind: "system"
category: "Graphics"
summary: "How a character fades in, out and through states: the ten Q12 fade channels of a render record and how one ramps, which system writes each channel (distance fade and cull, attached pieces, the time stop, statuses, the viewer-inside fade, the script colour), how the channels are multiplied and carried to the model instance and the lighting, and the coast-down latch that lets a stopping character glide to a halt."
addresses: ["003E5D60", "003E5D00", "003E5D30", "003E4370", "00428940", "004293C0", "00520180", "002E8B10", "00428C40", "002E84B0", "002E8500", "0033F530", "0033FAD0", "0042E1F0", "0042F880", "0042E850", "0042D7A0", "003E48E0", "003E4240", "003E4730", "003E4780", "003E51F0", "0042CBF0", "004FD4B0", "002E83A0", "002EBC30", "0042ED30", "00424080", "004256E0", "01DFE0B4", "01F82E38"]
---

# Character fades: the ten fade channels, their owners and the coast-down latch

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

- `003E5D60(record, n, target, frames)` starts a ramp. It first folds the current progress into the
  base, so an interrupted ramp continues from where it is, then sets `delta = target × 4096 − base` and
  `step = 0x1000 / (max(frames, 1) × [01DFE0B4])`. Progress restarts at one step, or at 0 for channel 1,
  and gains one more step when `01F82E38` is set.
- `003E5D00(record, n, value)` sets a channel at once: base `value × 4096`, the rest 0. The record clear
  `0041F730` sets all ten to 1.0; `003E5D30` puts channels 0, 1 and 4 back to 1.0.
- `00428940(record, n, value, frames)` is the forwarder most writers use: one frame or fewer sets the
  channel at once, more starts a ramp. `004293C0` is the same with a flag that redirects the write to
  the record's first child.
- `003E4370(record)` advances every channel with a non-zero step: progress grows by the step up to
  `0x1000`, and on the update after it arrives the delta is folded into the base and the channel rests.
  It runs from `0042C410` and `0042C8F0`, the root and child callbacks of the hierarchy walk
  `00426090` starts in each simulation step.

`01DFE0B4` is 1 at 30 fps and 2 at 60, and `01F82E38` is set at 60
([startup constants](../Engine-Core/startup-constants.md)), so a ramp takes the same time at
either rate.

### Who writes which channel

| Channel | Offset | Writer | Meaning |
|---:|---|---|---|
| 0 | `+0x4C0` | `0042E850` | distance fade; 0 over one frame when culled |
| 1 | `+0x4C8` | `0042E1F0`, `0042F880`, command `0x23` (`00520180` → `004293C0`) | attached-piece visibility |
| 2 | `+0x4D0` | `002E8B10` → `00428940` | time-stop fade ([time stop and freeze](../Engine-Core/time-stop-and-freeze.md)) |
| 3 | `+0x4D8` | the record clear only | stays at 1.0 |
| 4 | `+0x4E0` | `0042E850` | viewer-inside fade |
| 5 | `+0x4E8` | `0051DC90`, `0051E0A0`, `0051E3A0` → `00428940`, one frame | status look ([character status visuals](character-status-visuals.md)) |
| 6-9 | `+0x4F0`..`+0x508` | `00428C40(record, r, g, b, a, frames)` | script colour |

`00428C40` starts all four ramps with one frame count. `rgbatrans` (`0x3B2`, `0033F530`) reaches it
through `002E84B0` and `puppetrgbatrans` (`0x535`, `0033FAD0`) through `002E8500`; both pass the
popped frame count plus one. A sweep of every reference to `003E5D60`, `003E5D00`, `00428940` and
`004293C0`, conditional jumps included, finds no write of channel 3 and those listed above for the
others; the direct calls are in
[the channel census](character-fades-fade-channel-census.tsv).

### Attached pieces (channel 1)

A piece is a record whose kind byte `+0x6A0` (from the model's `@FCP` data) is `0x1C` or above. When a
record's dirty handler `0042AC30` runs (`+0x290` bit 31 or `+0x294` bit 3), it passes every descendant
to `0042E1F0`. For a piece whose parent's kind is `0x11` to `0x15`, the parent's parent decides:

- its `+0x284` bit 27 is set, or its event's index (`+0xCC & 0xFFF`) is `0x35`: channel 1 is set to 0
  at once;
- otherwise, when bits 0-1 of the handled record's `+0x40B` are both clear, a ramp to 0 over five
  frames;
- otherwise it is set to 1.0 at once.

`0042F880`, the handler that completes a pending attachment (owner at `+0x3CE`, slot at `+0x3CC`),
applies the same test for slot `0x10A` and sets channel 1 to 0 at once when the bits are clear, so the
piece arrives hidden.

### Distance fade and cull (channels 0 and 4)

`0042E850(record)` runs through `0042D7A0` for every record with `+0x284` bit 2 set, `+0x2AE` bit 1
clear and no parent.
It clears the three cull bits of `+0xD3` and measures a distance `d`: from the camera, or from the
reference record at tail `+0x2C` when that record is live (0 for the reference record itself). With
tail flag bit 0 on:

- `+0xD3` bit 0: the record fails the visibility test `0046C180` and has `+0x284` bit 21 and `+0xD2`
  bit 0;
- `+0xD3` bit 1: distance fade applies (`+0xD2` bits 4 and 1) and `d ≥ start + range`;
- `+0xD3` bit 3: the record has `+0x284` bit 21 and `+0xD2` bit 3, and its view depth plus its extent is
  below minus the near limit at tail `+0x20`.

When `005C5230()` returns non-zero, or record `+0x6E0` is non-zero, the bits are cleared and no
distance fade applies. A culled record gets channels 0 and 4 ramped to 0 over one frame. Otherwise
channel 0 ramps over one frame to 1.0 when `d ≤ start` and to `sin(((start + range − d) / range) ×
π/2)` inside the band, `start` and `range` being tail `+0x1C` and `+0x24`.

The viewer-inside test runs only with tail flag bit 4 set. When the camera's horizontal distance to
the character is below record `+0x2A8`, plus 0.15 while the character is already faded, and the
camera's height is within the character's half-height band, channel 4 ramps to 0 over three frames
and `+0x4B7` bit 5 is cleared; otherwise it ramps to 1.0 and the bit is set.

The settings are the record system's tail ([character render records](character-render-records.md)):

- `setcharclipdistance` (`0x327`, `00348B00`) pops two floats: the first to `+0x24` (`002E83A0`), the
  second to `+0x1C` (`002EBC30`);
- `setcharclipfaderange` (`0x328`, `003493F0`) pops one float into `+0x24`;
- `0042ED30` restores 34.0 and 4.0 and flag bits 0 and 2.

### Reading the channels

`003E48E0(record, selector)` returns one channel's value for selectors 0 to 9, or a product,
renormalised after every factor:

| Selector | Product of channels |
|---|---|
| `0x0B` | 0, 1, 2, 3, 4 |
| `0x0D` | 1, 2, 3, 5 |
| `0x0E` | 0, 1, 2, 3, 4, 5 |

`003E4240(record, parent)` stores the six-channel product in the word `+0x4B4`, multiplied by the
parent's `+0x4B4` when there is a parent, so a piece inherits its owner's fade. `003E4730` turns it into
`(+0x4B4 / 4096) × [+0x22C] × [+0x2EC] / 255`; `003E4780` takes the last factor from its caller.
`003E51F0` returns channels 6 to 9 as four floats divided by 4096.

### Into the model instance

For an attached record `0042CBF0` runs the three readers above, stores `+0x49C` = composite × script
alpha, and writes the record's model instance:

- `+0x90` = the colour `+0x210`;
- `+0xA0` = the second colour `+0x220` × the script colour;
- `+0xB0` = the Q12 composite `+0x4B4`.

With `+0x284` bit 26 and a live parent, `+0x90` comes from the parent's `+0x210` and `+0xA0` from the
parent's instance `+0xA0` × this record's product. The draw setup `004FD4B0` then multiplies the
character's ambient light by `+0xA0`..`+0xA8` and its alpha by `+0xAC × +0xB0 / 4096`
([character lighting and shadows](character-lighting-and-shadows.md)).

### The coast-down latch

The movement step asks `00424080(record, &heading, &speed)` before it turns heading and speed into a
position change ([heading and speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md),
which lists every branch). The record keeps a live block at `+0x610` (heading, speed, accumulator,
flags) and a cached block at `+0x620`; bit 0 of the word `+0x62C` is the latch.

1. Latched: the cached speed is multiplied by 0.83 and returned with the cached heading; the latch
   clears once the speed is 0.05 or less. A speed of 1.0 is released on the 17th call.
2. Not latched, for a root record with `+0x284` bit 27: when the event index (`+0xCC & 0xFFF`) is
   `0x10`, the requested speed is exactly 0 and the byte `+0x457` has reached `30 × [01DFE0B4]`, the
   latch is armed and the first decayed value is returned at once.
3. Otherwise, for such a record, the live block moves to the cache and the new heading and speed
   become the live pair, so the cache is always one call behind.

`+0x457` is advanced by `004256E0`, the record's locomotion selector, in its states 2 and 9 to 11, and
capped at `90 × [01DFE0B4]`; its 16-bit store of 0 at `+0x456` resets it.

After the latch, when the record has a presentation entry whose resolved data has byte `+1` equal to 1,
events `0x35` and `0x36` multiply the accumulator by 0.9 and the speed by the result, event `0x0D`
forces the speed to 0, and any other event resets the accumulator to 1.0.

## Modding notes

- To fade a character from script without fighting the engine, use the channels it leaves alone:
  `rgbatrans` owns 6 to 9, and nothing but the clear writes channel 3.
- Selector `0x0B` leaves channel 5 out; whatever reads it ignores Invisibility.
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
