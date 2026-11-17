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

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16` |  | base, Q12 (`0x1000` = 1.0) |
| `+0x02` | `i16` |  | delta: target - base |
| `+0x04` | `i16` |  | progress, 0 to `0x1000` |
| `+0x06` | `i16` |  | step per update; 0 = at rest |

```
value = base + ((delta * progress) >> 12)
```

- `0x003E5D60(record, n, target, frames)` starts a ramp. It first folds the current progress into the
  base, so an interrupted ramp continues from where it is, then sets `delta = target × 4096 − base` and
  `step = 0x1000 / (max(frames, 1) × [0x01DFE0B4])`. Progress restarts at one step, or at 0 for channel 1,
  and gains one more step when `0x01F82E38` is set.
- `0x003E5D00(record, n, value)` sets a channel at once: base `value × 4096`, the rest 0. The record clear
  `0x0041F730` sets all ten to 1.0; `0x003E5D30` puts channels 0, 1 and 4 back to 1.0.
- `0x00428940(record, n, value, frames)` is the forwarder most writers use: one frame or fewer sets the
  channel at once, more starts a ramp. `0x004293C0` is the same with a flag that redirects the ramp to
  the record's first child.
- The redirect covers only the ramp: for one frame or fewer `0x004293C0` jumps to `0x003E5D00` on the record itself
  whatever the flag (`0x004293C0`-`0x004293C4`). A flag of exactly 1 sends the ramp to the first child `+8`, and
  nothing is written when that index is -1 or the child's `+0x284` is 0 (`0x004293CA`-`0x00429402`). Command `0x23`
  gives the flag its word `+2` (`0x00520190`-`0x0052019F`).
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
popped frame count plus one.

`0x00428C40` takes the frame count as a float and truncates it, `n = (int)count` (`cvttss2si ebx, [rsp + 0x78]`
at `0x00428C4A`), and always ramps through `0x003E5D60`:
channels 6, 7 and 8 by calls and 9 by a tail jump (`0x00428C50`-`0x00428CBE`), so a count below 1 still ramps over
one frame. Both verbs pop five floats with `0x00267DB0`, the frame count first and then alpha, blue, green and red,
and add 1.0 to the count (`0x0033F559`-`0x0033F5A1`, `0x0033FAFB`-`0x0033FB66`).

`0x002E84B0(actor, ...)` writes nothing for a null actor, a null presentation context `+0xC0`, a context whose
dword `+0x00` or word `+0x00` is -1, or a record whose `+0x284` is 0 (`0x002E84B3`-`0x002E84ED`). `0x002E8500`
takes the puppet binding itself and makes the same tests from its dword `+0x00` on (`0x002E8503`-`0x002E8531`).
`puppetrgbatrans` then pops the puppet number (`0x00267E10`), calls the bare `ret` `0x0016D6A0`, and reaches
`0x002E8500` only when `0x003EB720(number)` gives a binding (`0x0033FB35`-`0x0033FB72`).

Of all the references to `0x003E5D60`, `0x003E5D00`, `0x00428940` and `0x004293C0`, conditional jumps included, not one
writes channel 3, and the references that write the other channels are those
listed above. [The channel table](character-fades-fade-channel-census.tsv) holds the direct calls of `0x003E5D00` and
`0x003E5D60`; channels 2 and 5 reach them through the dispatcher `0x00428940` (`0x003E5D00` for `r9` of 1 or less,
`0x003E5D60` for a non-null `rcx`), so their writers are the ones in the table above, not rows of that table.

### Columns of character-fades-fade-channel-census.tsv

One row per direct call or tail jump to one of the three channel functions, 22 rows. The channel is read from
`edx` by walking the 16 instructions before the call forward, without following branches.

| Column | Holds |
|---|---|
| `operation` | the function called: `start_ramp` for `0x003E5D60` (11 rows), `set_immediate` for `0x003E5D00` (3 rows) or `evaluate` for the reader `0x003E48E0` (8 rows) |
| `channel_or_selector` | the value of `edx` at the call: the channel 0 to 9 for `start_ramp` and `set_immediate`, the selector for `evaluate` (`11`, `13` and `14` are the products `0x0B`, `0x0D` and `0x0E` above); a register name when `edx` holds no constant, `edi` once, in the record clear `0x0041F730` |
| `caller` | the start address of the function that makes the call |
| `caller_name` | that function's name in the disassembly's function list; `FUN_` and the address when it carries no name |
| `site` | the address of the `call` or `jmp` instruction |

### Attached pieces (channel 1)

A piece is a record whose kind byte `+0x6A0` (from the model's `@FCP` data) is `0x1C` or above. When a
record's dirty handler `0x0042AC30` runs (`+0x290` bit `0x80000000` or `+0x294` bit `0x8`), it passes every descendant
to `0x0042E1F0`. For a piece whose parent's kind is `0x11` to `0x15`, the parent's parent decides:

- its `+0x284` bit `0x8000000` is set, or its event's index (`+0xCC & 0xFFF`) is `0x35`: channel 1 is set to 0
  at once;
- otherwise, when bits `0x3` of the handled record's `+0x40B` are both clear, a ramp to 0 over five
  frames;
- otherwise it is set to 1.0 at once.

`0x0042E1F0(record, arg)` first runs `0x004292B0(record, [arg + 8], 0)` on every record it is given, piece or not,
then reads the kind through `0x003E5CF0` (`0x0042E20E`-`0x0042E225`); a piece without a parent is left there
(`0x0042E227`-`0x0042E22F`).

The parent's own parent index `+6` is used with no -1 test (`0x0042E258`-`0x0042E264`),
so for a parent without a parent the `+0x284` and `+0xCC` tests read the 0x740 bytes before the record array
`[0x022C6F28]`. The handled record is `[arg + 8]` (`0x0042E2AC`) and the ramp is
`0x003E5D60(record, 1, 0, 5)`, a tail jump (`0x0042E2C1`-`0x0042E2D7`). A record whose word `+0x2F2` is non-zero skips
all of this: it tail-jumps to `0x00423B10(record, [arg + 0x10], dword [arg + 0x20])` (`0x0042E1FA`-`0x0042E208`,
`0x0042E2E6`-`0x0042E2F8`).

`0x0042F880`, the handler that completes a pending attachment (owner at `+0x3CE`, slot at `+0x3CC`),
applies its own test for slot `0x10A` and sets channel 1 to 0 at once when the bits are clear, so the
piece arrives hidden.

For a piece in slot `0x10A` it reads the record that the owner's word `+0x2C8` names (`0x003326C0`), with no null
test before reading its kind (`0x0042F98A`). When that record's kind is `0x11` to `0x15`, the piece is tied to it
instead of the owner, and channel 1 is set to 0 after the tie when bits `0x3` of the owner's `+0x40B` are both
clear (`0x0042F956`-`0x0042F9CD`,
`0x0042FA2E`-`0x0042FA3E`). An owner word `+0x2C8` of -1 ends the handler before the tie (`0x0042F97C`). Unlike
`0x0042E1F0` it does not look at `+0x284` bit `0x8000000` or the event index.

### Distance fade and cull (channels 0 and 4)

`0x0042E850(record)` runs through `0x0042D7A0` for every record with `+0x284` bit `0x4` set, `+0x2AE` bit `0x2`
clear and no parent.
It clears the three cull bits of `+0xD3` and measures a distance `d`: from the camera, or from the
reference record at tail `+0x2C` when that record is live (0 for the reference record itself). With
tail flag bit `0x1` on:

- `+0xD3` bit `0x1`: the record fails the visibility test `0x0046C180` and has `+0x284` bit `0x200000` and `+0xD2`
  bit `0x1`;
- `+0xD3` bit `0x2`: distance fade applies (`+0xD2` bits `0x10` and `0x2`) and `d ≥ start + range`;
- `+0xD3` bit `0x8`: the record has `+0x284` bit `0x200000` and `+0xD2` bit `0x8`, and its view depth plus its extent is
  below minus the near limit at tail `+0x20`.

The visibility test `0x0046C180` asks `0x003B3F10(box)` where the box lies against the view. For each of the eight
corners, it takes the corner's x, y and z from the box's two corner vectors through the index table
`0x00D114C4`-`0x00D11523`, three indices a corner (`0x003B3F73`-`0x003B3FB1`). It transforms the corner with the view
matrix at `0x02B403F0` (`0x00202C90`, `0x00202B70`) and builds a six-bit outcode: x, y and z each above `|w|` or below
`-|w|` (`0x003B3FE0`-`0x003B4030`). It returns 3 when every corner is outside the same side, 1 when some corner is
outside, and 0 otherwise (`0x003B4064`-`0x003B4078`).

| Global | Type | Start | Meaning | Written | Read |
|---|---|---|---|---|---|
| `0x02B404B0` | `u32` | 0 | the outcode history: each corner shifts it left by 6 and puts its own outcode in bits `0x3F` | `0x003B3F10` (`0x003B4042`) | `0x003B3F10`: the shift (`0x003B4033`), then the OR and the AND over the corners (`0x003B404F`, `0x003B4055`), whose result keeps bits `0x3F` (`0x003B4064`, `0x003B4070`) |
| `0x02B404B3` | `u8` | 0 | the history's top byte, set to 0 after each corner, so the word holds the last four corners' outcodes | `0x003B3F10` (`0x003B4048`, the byte of `ebp`, 0 from `0x003B3F65`) | through the word reads above |

- `puppet_setcharclipone(d, v)` (`0x0569`, `0x00340890`) sets two of these inputs on the render record
  of puppet `d` (`0x003EB700`) when it is live: `0x003EB8C0` writes `v` into bit `0x10` of `+0xD2`, and
  `0x003EB960` writes it into bit `0x8` of `+0x304` and raises bit `0x40` of `+0x290`, whose processor
  `0x0042BCB0` copies that bit into bit `0x200000` of the `+0x284` of the record itself and then of its
  children (`0x0042BCDE`-`0x0042BDAA`).
- Each of those copies is made only when `0x00426220` answers 0 for the record it would change
  (`0x0042BD0B`-`0x0042BD12`, `0x0042BD54`-`0x0042BD5B`, `0x0042E764`-`0x0042E76B`).
- `0x002E83B0(actor, on)` writes bit `0x2` of `+0xD2` on the render record of the actor's context `+0xC0`:
  set for a non-zero `on`, cleared for 0, the other bits kept (`0x002E83EC`-`0x002E83F9`). It does nothing for a
  null actor, a null context, a context whose dword `+0x00` is -1 or whose low word is `0xFFFF`, a record
  address of 0, or a record whose dword `+0x284` is 0 (`0x002E83B0`-`0x002E83EA`).
- `0x002392D0(actor, flags)` calls `0x002E83B0(actor, 0)` when `0x0031B760(actor)` answers non-null and `flags`
  has bit `0x10` (`0x002392E4`-`0x002392FB`).
- The record initialiser `0x00420480` sets bits `0x1B` of `+0xD2`, bit `0x2` among them (`0x004204A7`).
  `0x002E83B0(actor, 1)` would put back that default; its one native call passes 0 (`0x002392FB`), reached from
  `btlAtelSetEntryFlag` (handler `0x00510300`, `0x0051031B`) through `0x002392D0` when the flags have bit `0x10`, so in the
  game the bit, once cleared, stays clear until the initialiser runs again.

When record `+0x6E0` is non-zero the bits are cleared and no distance fade applies; the other term of that test,
`0x005C5230()`, returns 0. A culled record gets channels 0 and 4 ramped to 0 over one frame. Otherwise
channel 0 ramps over one frame to 1.0 when `d ≤ start` and to `sin(((start + range − d) / range) ×
π/2)` inside the band, `start` and `range` being tail `+0x1C` and `+0x24`.

The viewer-inside test runs only with tail flag bit `0x10` set. When the camera's horizontal distance to
the character is below record `+0x2A8`, plus 0.15 while the character is already faded, and the
camera's height is within the character's half-height band, channel 4 ramps to 0 over three frames
and `+0x4B7` bit `0x20` is cleared; otherwise it ramps to 1.0 and the bit is set.

`0x0042D7A0` tests the parent as word `+0x06` of -1 (`0x0042D7A6`-`0x0042D7C2`). After `0x0042E850` it calls
`0x00421030(record)` and `0x004210D0(record)`; when the latter returns non-zero and the effect handle `+0x288` is
not -1, it tail-jumps to `0x003B33A0(+0x288, 0x00420FB0(record))`, the visibility write of
[character effects](character-effects.md) (`0x0042D7C7`-`0x0042D7F9`).

The settings are the record system's tail ([character render records](character-render-records.md)):

- `setcharclipdistance_327` (`0x327`, `0x00348B00`) pops two floats: the first to `+0x24` (`0x002E83A0`), the
  second to `+0x1C` (`0x002EBC30`, through `0x0026A460`);
- `setcharclipdistance` (`0x157`, `0x00348310`) pops one float to `+0x1C` the same way;
- `setcharclipfaderange` (`0x328`, `0x003493F0`) pops one float into `+0x24`;
- `0x0042ED30` restores 34.0 and 4.0 and flag bits `0x1` and `0x4`.

Two `f32` globals hold the defaults, both in the zero-filled tail of `.data`: `0x021641F4`, the default
distance, and `0x021641F8`, the default fade range. `0x002EDA70` and `0x002EDA80` store them; `0x002EDA30` and
`0x002EDA40` read them. `0x0026C8C0`, run from the load completion `0x0032F850`, sets both and the tail from them
(`0x0026CD96`-`0x0026CDB9`): 4.0 (`0x01CEBC70`, through `0x002EDA60`) into `0x021641F8` and on to `+0x24`, and 34.0
(`0x00D0F8EC`, through `0x002EDA50`) into `0x021641F4` and on to `+0x1C`. Their verbs:

- `getcharclipdefaultdistance` (`0x329`, `0x00340B50`) and `getcharclipdefaultfaderange` (`0x32A`,
  `0x00340F80`) return the two defaults;
- `setcharclipdefaultdistance` (`0x33E`, `0x00348700`) pops one float into `0x021641F4` and `+0x1C`;
- `setcharclipdefaultfaderange` (`0x33F`, `0x003497D0`) pops one float into `0x021641F8` and `+0x24`;
- `setcharclipdefaultdistance_340` (`0x340`, `0x00348F20`) pops two floats: the first into `0x021641F8` and
  `+0x24`, the second into `0x021641F4` and `+0x1C`.

### Reading the channels

`0x003E48E0(record, selector)` returns one channel's value for selectors 0 to 9, or a product,
renormalised after every factor (each one shifted right by 12). Any selector other than `0x0B`, `0x0D` and
`0x0E` is read as the channel at `+0x4C0 + 8 × selector` (`0x003E48FC`-`0x003E4922`); its eight callers give
4, `0x0B`, `0x0D` and `0x0E` (`0x0042FB59`, `0x0042D3E6`, `0x0042D580`, `0x004FDB49`, `0x0053AE44`, `0x0053AE9A`,
`0x0053AF2B`, `0x0053D9A1`):

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
them each frame. With `+0x284` bit `0x20000000` clear they are 0, 0, 0 and 255. Otherwise it takes the global
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
bit `0x4000` (`0x00202C90`); it computes the record's own block only when that ancestor's word `+0x2CA`
names the record and `0x003B4750` finds a pool record for it. A record whose parent is gone is
detached and computes its own (`0x0041EC00`, `0x0041E960`).

### The type-0x41 pool

Effect type `0x41` keeps records in the 64-entry pool of `0x60`-byte records at `[0x02B404E0]`
([effect element types](effect-element-types.md)), linked in an active list (head `0x02B404C8`, tail
`0x02B404D0`, links `+0x08` and `+0x10`) and named by `serial << 8 | slot`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | handle |  |
| `+0x04` | `u16` |  | age in steps |
| `+0x06` | `u16` | frame in the period |  |
| `+0x20` | `u8` |  | curve number (3: no curve) |
| `+0x21` | `u8` |  | mask `0x7F`: 1 linear, other smoothed; bit `0x80`: half strength |
| `+0x22` | `u8` |  | target kind: 1 a render record, 2 a test through `0x0024E2F0` / `0x0024E6D0` |
| `+0x23` | `u8` |  | target mode |
| `+0x24` | `u32` | target id |  |
| `+0x28` | `u16` |  | lifetime in steps (0: no lifetime) |
| `+0x2A` | `u16` | period in steps |  |
| `+0x2C` | `u8` | priority |  |
| `+0x2D` | `u8` | mask tested against 0x02B404C1 |  |
| `+0x30` | `f32` | strength |  |
| `+0x34` | `f32` | weight |  |
| `+0x38` | `f32` |  | 1 / period |
| `+0x3C` | `f32` | phase, 0 to 1 |  |
| `+0x40` | `f32[4]` |  | colour (r, g, b, a); `+0x4C` is also the lowest weight |
| `+0x50` | `u32` |  | stamp from `0x00181DD0`() |

- `0x003B4160` takes the first of the 64 records whose `+0x00` is 0 and returns 0 when no record is free
  (`0x003B4182`-`0x003B4193`); it gives the record the next serial from `0x02B404C4`, wrapping to 1 above
  `0xFFFFFF` (`0x003B41AB`-`0x003B41BB`), and stores `serial << 8 | slot` at `+0x00` (`0x003B41ED`-`0x003B41F2`),
  which is never 0, the serial being 1 to 0xFFFFFF (its only writers are `0x003B41BB` and the reset's `0x003B480E`).
- Before `0x003B4160` copies the caller's `0x30`-byte block to `+0x20` (`0x003B4212`-`0x003B4225`) it changes
  that block in place: the period word (record `+0x2A`) becomes twice itself when `0x001EDDA0()` answers 0
  (`0x003B41C1`-`0x003B41D1`), and `+0x2E`, `+0x34` and `+0x3C` are set to 0 and `+0x38` to 1 / period
  (`0x003B41F4`-`0x003B420F`).
- `0x003B4160` stores a dword 0 at `+0x04`, which zeroes the age and the frame (`0x003B41EA`), and the answer
  of `0x00181DD0()` at `+0x50` (`0x003B41A8`).
- A record is freed by storing 0 at its `+0x00`: `0x003B42B0` at `0x003B42DC`, `0x003B4840` at `0x003B48D7`, and the
  reset `0x003B4790`, which zeroes all 64 records and the serial (`0x003B480E`-`0x003B481D`).
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

The key tables are two `0x10`-byte entries from `0x02B404E8`, picked by the record's curve number (`0x003B4403`-`0x003B441C`):
a `u32` key count and a pointer to `(phase, value)` pairs of `f32`. The pool reset `0x003B4790` (called from `0x00259180`
at `0x0025919B`) fills them every time it runs:

| Curve | Count | Keys (phase, value) | Stores |
|---|---|---|---|
| 0 | `0x02B404E8` = 3 | `0x02B404F0` = `0x00D11520`: (0, 1.0), (0.5, 0), (1.0, 1.0) | `0x003B47D0`, `0x003B47DA` |
| 1 | `0x02B404F8` = 5 | `0x02B40500` = `0x00D11538`: (0, 1.0), (0.25, 0), (0.5, 1.0), (0.75, 0), (1.0, 1.0) | `0x003B47EA`, `0x003B47F4` |

`0x003B4310` forms the base at `0x003B438A` and reads the count (`0x003B441F`) and the key pointer (`0x003B4427`, `0x003B4460`)
of the record's curve, then the keys around the record's phase (`0x003B4433`, `0x003B446C`-`0x003B4488`). So curve 0 dips
from full to nothing and back once per period, and curve 1 twice.

The pool keeps a byte count of its records. Taking a record adds 1 and the unlink `0x003B42B0` takes 1 away. The step
`0x003B4840` frees a record whose lifetime has run out (`0x003B48D7`) without changing the count, so the count runs ahead
of the records in use. Its only other store is the reset's 0:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B404C0` | `u8` | 0 (zero-filled tail of `.data`) | the records taken less the records unlinked through `0x003B42B0`; wraps at 256 | `0x003B4160`, 1 more (`0x003B419D`, `inc`); `0x003B42B0`, 1 less (`0x003B42CE`, `dec`); the reset `0x003B4790`, 0 (`0x003B481F`) | only the `inc` and `dec` themselves: no other RIP-relative, image-base-relative or disp32 reference names it |

### Into the model instance

For an attached record `0x0042CBF0` runs the three readers above, stores `+0x49C` = composite × script
alpha, and writes the record's model instance:

- `+0x90` = the colour `+0x210`;
- `+0xA0` = the second colour `+0x220` × the script colour;
- `+0xB0` = the Q12 composite `+0x4B4`.

With `+0x284` bit `0x4000000` and a live parent, `+0x90` comes from the parent's `+0x210` and `+0xA0` from the
parent's instance `+0xA0` × this record's product. The draw setup `0x004FD4B0` then multiplies the
character's ambient light by `+0xA0`..`+0xA8` and its alpha by `+0xAC × +0xB0 / 4096`
([character lighting and shadows](character-lighting-and-shadows.md)).

### The coast-down latch

The movement step asks `0x00424080(record, &heading, &speed)` before it turns heading and speed into a
position change ([heading and speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md),
which lists every branch). The record keeps a live block at `+0x610` (heading, speed, accumulator,
flags) and a cached block at `+0x620`; bit `0x1` of the word `+0x62C` is the latch.

1. Latched: the cached speed is multiplied by 0.83 and returned with the cached heading; the latch
   clears once the speed is 0.05 or less. A speed of 1.0 is released on the 17th call.
2. Not latched, for a root record with `+0x284` bit `0x8000000`: when the event index (`+0xCC & 0xFFF`) is
   `0x10`, the requested speed is exactly 0 and the byte `+0x457` has reached `30 × [0x01DFE0B4]`, the
   latch is armed and the first decayed value is returned at once.
3. Otherwise, for such a record, the live block moves to the cache and the new heading and speed
   become the live pair, so the cache is always one call behind.

`+0x457` is advanced by `0x004256E0`, the record's locomotion selector, in its states 2 and 9 to 11, and
capped at `90 × [0x01DFE0B4]`; its 16-bit store of 0 at `+0x456` resets it.

After the latch, when the record has a presentation entry whose resolved data has byte `+1` equal to 1,
events `0x35` and `0x36` multiply the accumulator by 0.9 and the speed by the result, event `0x0D`
forces the speed to 0, and any other event resets the accumulator to 1.0.
A latched call (case 1) returns straight after its decay (`0x0042411A`) and skips this step, so it runs on the
arming call and on every unlatched call, also for a record without bit `0x8000000` or with a parent (`0x00424129`,
`0x00424130`).

## Modding notes

- To fade a character from script without fighting the engine, use the channels it leaves alone:
  `rgbatrans` owns 6 to 9, and nothing but the clear writes channel 3.
- Selector `0x0B` leaves channel 5 out; whatever reads it ignores Invisibility.
- The glide's feel is the two constants in `0x00424080`: 0.83 per call and the speed of 0.05 that releases the latch.

## Related

- [Character render records](character-render-records.md): the record, its tail settings and the walks.
- [Character lighting and shadows](character-lighting-and-shadows.md): where the fade meets the ambient light.
- [CharacterRenderObject](character-render-object.md): the model instance layout.
- [Character status visuals](character-status-visuals.md): channel 5.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): channel 2.
- [Heading and speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md):
  the caller of the latch.
- [Startup constants](../Engine-Core/startup-constants.md): the frame-rate multiplier.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Save load settings: `0x0026C8C0` calls `0x002EF2B0`; those functions are documented on
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
- Story event quest hunt: `0x0026C8C0` calls `0x00377440`; those functions are documented on
  [actor managers](../Characters-And-Objects/actor-managers.md).
- World area: `0x0026C8C0` calls `0x0026DB30`; those functions are documented on
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md).
- Combat AI: `0x0031B760` is called by `0x00239040`, `0x003014C0`, `0x00301AD0`, `0x003087E0`, `0x0030F130`; those functions are
  documented on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md),
  [glossary](../Engine-Core/glossary.md), [area of effect](../Battle-Actions/area-of-effect.md).
- Combat AI: and on [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md).
- Combat action: `0x0031B760` is called by `0x00303830`, `0x00306010`, `0x0030EC00`; those functions are documented on
  [action phases](../Battle-Actions/action-phases.md), [action results](../Battle-Actions/action-results.md).
- Gameplay: `0x0031B760` is called by `0x0030B050`, `0x0030BA30`, `0x0030BFB0`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [battle units](../Characters-And-Objects/battle-units.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- Spawn encounter lifecycle: `0x0031B760` is called by `0x002350C0`, `0x00235360`, `0x002354F0`, `0x002355A0`, `0x00235720`,
  `0x00235EF0`, `0x00235F50`, `0x00235FB0`, `0x00236030`, `0x00236140`, `0x00236670`, `0x002366E0`; `0x0031B760` is also called by
  `0x00236860`, `0x00238FC0`, `0x002391C0`, `0x002393E0`, `0x00239410`, `0x00239710`, `0x00239840`, `0x002398F0`, `0x0023A200`,
  `0x0023A2E0`, `0x0023A3B0`, `0x0023A410`.
- Spawn encounter lifecycle: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [native limits](../Engine-Core/native-limits.md), [battle units](../Characters-And-Objects/battle-units.md),
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md).
- Spawn encounter lifecycle: and on [enemy respawning](../Enemy-Spawning/enemy-respawning.md),
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md),
  [enemy spawning](../Enemy-Spawning/enemy-spawning.md),
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md); and on
  [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md).
