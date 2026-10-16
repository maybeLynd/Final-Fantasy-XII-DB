---
title: "Character status visuals: how a status changes a character's colour, light, opacity and shadow"
kind: "system"
category: "Graphics"
addresses: "003E7650, 02B59D80, 00320BB0, 0046FD00, 0046FFA0, 00470050, 004703F0, 004700E0, 0046FBB0, 00470AA0, 00470780, 00470590, 00470B70, 00470660, 00470EB0, 004704C0, 00470230, 0051E3A0, 0051DBF0, 0051DDC0, 0051DC90, 0051E0A0, 0051E170, 0051DE30, 00428CD0, 005044D0, 00428F10, 003ABD50, 003ACC10, 003ACAA0, 003E7CC0, 003E7C70, 02B59D70, 02B59D71, 01F20AA0, 01F21F40, 01F22030"
---

## What the player sees

- A character with several ailments shows one colour look at a time, by a fixed order: Stone, Petrify, Berserk, Doom,
  Blind, Poison, Silence, Sap, Oil, Disable, Disease, HP Critical. Curing the top one brings up the next.
- Poison, Silence, Sap, Disable and Disease share one look, a pulsing darkening that pulls green down most. Blind is a
  plain pulsing darkening and Oil a much deeper one.
- A look fades in over ten frames and must fade out completely before the next one appears; Stone appears and goes at
  once.
- Doom glows a dull red and flashes each time its count ticks; Petrify looks like Stone with a dip of the light on
  each tick; HP Critical flashes red once a second; Berserk turns red and dark on the side facing the camera.
- Invisible makes a character see-through, and an enemy more so than a party member. Slow and Immobilize colour the
  character's shadow orange-red and red. These show alongside a colour look.
- Sleep, Confuse, Immobilize and Float also move the body ([Character rig and look](character-rig-and-look.md)).
- Reverse, Lure, Protect, Shell, Haste, Bravery, Faith, Reflect, Regen and Libra change nothing on the body through this
  mechanism; KO, Bubble and X-Zone only set a flag.
- During status-display denial, and in towns, the colour looks and the Invisible fade are hidden; during status-control
  denial the looks hold still.

## How it works

### The push

`003E7650` runs once per simulation tick from the world tick `00314020`
([Frame update order](../Engine-Core/frame-update-order.md)). It walks 32 presentation records of `0x150`
bytes at `02B59D80`, one per battle-unit slot, skipping records whose word `+0` is 0. `003E7500` sets a record up: word
`+0` = 1, `+4` = the character's render-record index, both blocks initialised with that index (`004700C0`, `0051E140`).

Two readers give other code a record's dwords from `+0xC0`: `003E7D10(slot, n)` takes the record of a
battle-unit slot when its word `+0` is set, and `003E7CD0(index, n)`, from `003B0C50` and `0046CC70`,
the record whose `+4` is a render-record index; both return dword `+0xC0 + 4n`, and 0 while the byte
`02B59D71` is set.

For each record it reads the unit's status word through `00320BB0`: the OR of the stats record's `+0x64` and `+0x3C`
([Statuses](../Status-Effects-And-KO/statuses.md)). Stop is left out of the word while the unit's action id
`+0x714` is `0x21E` or lower and its action phase `+0x6B4` is 9 or more, or while bit 24 of its flag word is set
(`00320C10`-`00320C37`). `00320BB0` also writes whether the stats record's kind byte `+5` is 1 (an enemy) to the record's
`+0x84`.

The record keeps the rig of the character's render record at `+0x10` (`003E6DA0`); with no rig, nothing else runs for
that record. When the word differs from the copy at `+8`, the push stores the bits that were set at `+0x140` and the
bits that were cleared at `+0x144`, then calls one arm per changed bit, cleared bits first. Every arm stores 1 or 0 in
the record's flag dword `+0xC0 + 4 × bit`. Then, changed or not, it runs the two block updates `0046FD00` (block
`+0x20`) and `0051E3A0` (block `+0x70`).

### What each status does

| Status (bit) | What the arm does beyond the flag dword |
|---|---|
| Stone (1) | colour look 0; bit 5 of render record `+0x304` through `00428F10`, which raises dirty bit 28 of `+0x290` |
| Petrify (2), Berserk (27), Doom (6), Blind (7) | colour looks 1, 2, 3, 4 |
| Poison (8), Silence (9), Sap (10), Oil (11), Disable (13), Disease (16) | colour looks 5, 6, 7, 8, 9, 10 |
| HP Critical (29) | colour look 13 |
| Stop (3) | second-block index 4; `+0x304` bit 5 as for Stone; `003E1310(rig, 0, 1 or 0)` stores the value in byte `+7` of rig slot 0, which makes the rig frame pass that slot a time input of 0 |
| Immobilize (14) | second-block index 0; rig controller 7 on or off |
| Slow (15), Invisible (24) | second-block indexes 1 and 3 |
| Sleep (4), Confuse (5) | rig controller 3 and the look controller's byte `+0x1C` bits 1 and 2 |
| Float (26) | rig controller 6 on or off |
| KO (0), Bubble (28), X-Zone (31) | nothing |
| bits 12, 17-23, 25, 30 | no arm |

The arms are `0051E580`-`0051ECF0`, one pair per bit. The rig switches are on
[Character rig and look](character-rig-and-look.md).

The rig arms keep a word per status in the block they are given and reach the rig through the
block's `+0x10`, the look controller (rig slot 2) for its byte `+0x1C`:

| Status | Enter | Leave |
|---|---|---|
| Confuse | `0051E670`: `+0xD4` = 1; controller 3 on unless `+0xD0` (asleep); look byte `+0x1C` bit `0x4` set | `0051E620`: `+0xD4` = 0; controller 3 off; bit `0x4` cleared |
| Sleep | `0051EA10`: `+0xD0` = 1; controller 3 off when confused; bit `0x2` set | `0051E9C0`: `+0xD0` = 0; controller 3 on when confused; bit `0x2` cleared |
| Immobilize | `0051E740`: `+0xF8` = 1, `0051DBF0` on the block's `+0x70`, controller 7 on | `0051E700`: `+0xF8` = 0, `0051DDC0`, controller 7 off |
| Float | `0051E840`: `+0x128` = 1, controller 6 on | `0051E800`: `+0x128` = 0, controller 6 off |

### The colour-look list

Block `+0x20` keeps a fourteen-bit mask at `+0`. The add worker `0046FFA0` and the remove worker `00470050` set or clear
one bit, keep the entry count in the upper seven bits of byte `+7`, and store the lowest set index in byte `+5`, or
`0xFF` when the mask is empty. Byte `+5` is the wanted look; the order in the table above is the index order.

The update `0046FD00(block, render record, display deny, control deny)` runs each tick:

1. It stores the render record at `+0x28` and the hold byte `+0x3A`: the control-deny byte, or 0 while display is
   denied.
2. When the wanted look `+5` differs from the shown look `+4`, it copies it over and sets the changing bit, bit 0 of
   `+7`.
3. It calls the step at `+0x18`; with no step, the changing bit is the answer. A step returns 1 only when its look has
   fully left.
4. Only then, with a non-empty list, it installs the shown look by a switch on `+4`.
5. While display is denied it also zeroes render record byte `+0x5E0` and sets the record mode to 0.

Installing a look clears the changing bit, releases the block's two light handles `+8` and `+0xC`, sets the record
mode and stores the look's step. Indexes 11 and 12 have no arm in the push; index 12 has a look, the tint with offset
`(1.5, 2.0, 2.0)`.

`003E75A0` resets every block in use of the 32 from `02B59D80`, and `003E7D50` one block. Each
reset runs `00470000` on the block's `+0x20`, which clears the mask and the bits of byte `+7`
above bit 0, sets the shown and wanted looks (`+4`, `+5`) to `0xFF` and releases the two lights
`+8` and `+0xC` (`003ABCA0`), and then `0051DC60` on `+0x70`.

### The record mode

`00428CD0(render record, mode)` stores the mode in byte `+0xBA` of the model instance (`00504D20`) of the record and of
every record attached under it, skipping those `00426220` rejects. `005044D0(instance, n)` uses it to pick entry `n`'s
parameter block: `table + entry.offset + mode × entry.stride`, with the table at instance `+0x1F8` plus `+0x21C`,
sixteen-byte entries from table `+0x30`, the stride the word at entry `+2` and the offset the dword at entry `+0xC`.
Stone sets mode 3, the flash frames of Doom and HP Critical mode 2, every other look mode 0.

### The tint

`004703F0` stores the offset at `+0x40`, zeroes the phase and envelope, installs the step `004700E0` and creates a light
(`003AB960`) from an `0x50`-byte request: type 6 (ambient), priority `0xBF`, byte `+3` = 1 and `+4` = 2, target id the
block's `+0x10`, byte `+5` = `0x90` and `+7` = `0x80`. Its handle goes to `+8`.

Each frame `004700E0` returns at once while the hold byte is set. Otherwise the phase `+0x20` rises by
`[01DFE0BC] × 0.0333` and wraps at 1. The envelope `+0x24` rises by `0.1 × [01DFE0BC]` to 1, or falls at that rate while
the changing bit is set; at zero it releases the light, clears the step and returns 1. With `p` the pulse at the phase
(`0046FBB0`, the table `01F20AA0`):

| Value | Formula | Code |
|---|---|---|
| light colour | `offset × (0.5 + 0.5p) × envelope, alpha 1.0` |  |
| record +0x5EC | `1 - (0.8 + 0.2p) × envelope` |  |

Blind's offset is `(-0.5, -0.5, -0.5)`, the shared look's `(-0.2, -0.7, 0)`. Oil installs the same step with
`(-2, -2, -2)` and its own light: type 1 (directional), priority `0xBE`, byte `+5` = `0x80`, byte `+6` = 1, vector
`(0, -1, 0)` at request `+0x30`.

### Stone and Petrify

Stone's step `00470AA0` raises its phase over 30 frames and holds it at 1. Each frame it sets render record byte
`+0x5E0` = 2, `+0x5DC` = `1 + 0.3 × pulse(phase / 2)`, `+0x5EC` = 0.4 and mode 3. When the look changes it sets mode
0, releases both handles and returns 1 in the same frame. It creates no light.

Petrify's step `00470780` has four states in byte `+0x38`; frame counts below are multiplied by `[01DFE0B4]`:

| State | What it does |
|---|---|
| 0, arriving | ambient mode 2 with `+0x5DC = 1 - 0.7 × pulse(t)`, `t` rising by `[01DFE0BC] / 6`; mode 0 and light scale 1.0 for the first three frames, then mode 3 and 0.4; after six frames it reads the Petrify count and goes to state 1 |
| 1, steady | ambient mode 0, mode 3, scale 0.4; a changed, non-zero count starts state 2. When the look must leave: if Stone's bit is in the mask it releases and returns 1 at once, otherwise it goes to state 3 |
| 2, tick | ambient mode 2 with `1 - 0.3 × pulse(t)`, `t` rising by `0.05 × [01DFE0BC]`; mode 3, 0.4; back to state 1 after twenty frames |
| 3, leaving | state 0's dip with mode 3 and 0.4 for three frames, then mode 0 and 1.0; releases and returns 1 after six frames |

The count comes from `00320CF0(unit, status)`, which returns the stats record's `+0xBC + 4 × status` for Petrify and Doom
while the status is set ([Status timers](../Status-Effects-And-KO/status-timers.md)), and -1 otherwise. The unit
is the byte `+0xEA9` of the object behind render record `+0x108` (`00263E50`).

### Doom, HP Critical and Berserk

Doom's installer `00470590` creates the tint's ambient light and installs `00470B70`. In the steady state the envelope
moves by `0.33 × [01DFE0BC]` a frame, the light colour is `envelope × 0.4 × (0.9, -0.2, -0.2)`, the light scale is 1.0
and the mode 0. Every steady frame that is not leaving, a Doom count different from the one remembered at `+0x39`
starts a flash; the installer zeroes `+0x39`, so the look starts with one. The flash runs 21 frames:

| Value | Formula | Code |
|---|---|---|
| light colour | `(0.6 × curve1[f] + 0.4 × envelope) × (0.9, -0.2, -0.2)` |  |
| record +0x5EC | `1 - curve2[f]` |  |
| frames 3-10    : mode 2, record colour +0x5D0 | `(0.84, 0.84, 0.84); otherwise mode 0 and (1, 1, 1)` |  |
| frames 0-20    : ambient mode 1 with +0x5DC | `curve1[f]` |  |

HP Critical's installer `004704C0` creates the same light with the step `00470230`, which runs the same recipe with the
colour `curve1[f] × (0.64, 0, -0.32)` on a 30-frame cycle. From frame 21 to the end of the cycle it sets bit `0x2` of
the light's byte `+7`, which makes the light selector skip it, and clears ambient mode. It checks whether to leave only
when the cycle wraps, so it always finishes its beat.

Berserk's installer `00470660` creates two lights: the tint's ambient into `+8` and Oil's directional request into
`+0xC`. Its step `00470EB0` uses the tint's phase and envelope; with `w = (0.5 + 0.5p) × envelope`:

| Value | Formula | Code |
|---|---|---|
| ambient colour | `(2w, 0, 0)` |  |
| directional colour | `(-3.5w, -3.5w, -3.5w)` |  |
| directional vector | `normalise(point - camera position 02AEDF20)` |  |
| record +0x5EC | `1 - (0.85 + 0.15p) × envelope` |  |

The point is the translation of the matrix `00421E20` returns for bone code `0x100`. While the hold byte is set the step
still re-aims the light every frame and does nothing else.

### Where the lighting fields go

The per-character light gather `003ABD50` copies render record `+0x5EC` to `02B3F518` before it calls the light selector
`003ACC10`. The ambient evaluator `003ACAA0` multiplies a light's colour by `02B3F518` while the enable byte `02B3F502`
is set and the light's byte `+5` is below `0x80`, so the status lights (`0x90`, `0x80`) are never dimmed by it.

In the selector, an ambient light without bit `0x10` in byte `+5` is changed before it is summed: render record byte `+0x5E0`
= 2 multiplies it by `+0x5DC`, and 1 blends it toward the record colour `+0x5D0`-`+0x5D8` by `+0x5DC`. A light is skipped
when its byte `+7` shifted right by two meets the class filter `02B3F520 | 02B3F501`, or when byte `+7` has bit `0x2`.
The lighting itself is on [Character lighting and shadows](character-lighting-and-shadows.md).

### The second block

Block `+0x70` keeps a mask at `+0x10`. Its workers `0051DBF0` (add) and `0051DDC0` (remove) derive three bytes:

| Byte | Value |
|---|---|
| `+0x19`, channel A | 2 when mask bit 2, else 3 when bit 3 (Invisible), else `0xFF` |
| `+0x31`, channel B | 0 when bit 0 (Immobilize), else 1 when bit 1 (Slow), else `0xFF` |
| `+0x33` | mask bit 4 (Stop) |

`0051E3A0` returns at once while control is denied and display is not. Otherwise it runs the wanted, shown, changing
and step protocol for each channel: channel A installs `0051E0A0` for 2 and `0051DC90` for 3, channel B `0051DE30` for
0 and `0051E170` for 1. While the Stop byte is set and display is not denied it calls `003E7450(render record, 0, 0, 1)`
every frame. While display is denied it then writes fade channel 5 = 1.0 (`00428940`), the shadow's `+0xC` = 1.0
(`003B6B10`) and the shadow's colour = 0 (`003B6B30`), after the steps have run.

These steps use a phase stepping by `0.033 × [01DFE0BC]` and an envelope moving by `0.1 × [01DFE0BC]`:

- Invisible, `0051DC90`: fade channel 5 = `1 - (0.6 + 0.2p) × envelope`, or `1 - (0.88 + 0.08p) × envelope` when the
  block's `+0x14` (the record's enemy flag) is set; `00428AF0(record, 1, 1, 0x60)` sets `+0x304` bits 17, 18 and the
  byte at bits 19-26. Leaving restores 1.0 and clears them ([Character fades](character-fades.md)).
- Index 2, `0051E0A0`: fade channel 5 = `1 - envelope`. No status selects it.
- Slow, `0051E170`, while render record `+0x114` holds a shadow: with `s = (0.5 + 0.3p) × envelope`, the shadow's
  colour = `(128s, 32s, 8s)` as integers, and the vector `(1 + 0.1p, 1 - 0.1p, 1 - 0.1p, 1)` goes to `001F1600`, which
  stores it at `02CB8390`; then `0051E510(record, 1)`.
- Immobilize, `0051DE30`: the same with `s = (0.7 + 0.3p) × envelope`, colour `(128s, 16s, 4s)`, vector
  `(1 + 0.3p, 1 - 0.3p, 1 - 0.3p, 1)`, and the shadow's `+0xC` = `1 + (1.5 + 0.5p) × envelope`.
- Leaving, Slow and Immobilize restore the shadow's `+0xC` to 1.0, its colour to 0, store `(0, 0, 0, 1)` at
  `02CB8390` and call `0051E510(record, 0)`.

`0051E510` walks the record and every record attached under it and calls the method at offset `0xC8` of each render
object (record `+0x6B8`) with 1 or 0. The shadow pool is 160 entries of `0xE0` bytes at `[02B40528]`; `003B6B10` and
`003B6B30` write only when the handle matches the entry's `+0x10`.

### The denial latches

- `02B59D70`, control deny, is written only by `003E7CC0`. `002EA8E0(bit, on)` keeps the requester bits in
  `0215FD44` and sets the latch while any is set.
- `02B59D71`, display deny, is written only by `003E7C70`. Setting it ORs `0x20` into the class filter `02B3F501`, clears
  the enable byte `02B3F502` and sets `02B59D68`; clearing reverses all three. `002EA8B0` keeps its requester bits in
  `0215FD45`.

Bit 0 of the requester bytes comes from the `ctrldenystatus` and `dispdenystatus` verbs
([Time stop and freeze](../Engine-Core/time-stop-and-freeze.md)), bit 2 from the town flag
([Party control modes](../Engine-Core/party-control-modes.md)). Class 5 (byte `+7` = `0x80`) is the status
lights, so display denial switches them off and lifts the dimming while the steps keep running.

### Stretching the tables for 60 fps

The pulse table, the two curves and the other frame tables from `01F20530` to `01F264AC` hold one entry per
frame at 30 fps. When the game switches to the 60 fps time base (`001EDDC0`), `0033F020` doubles each
table's frame count and resamples the table in place to twice its entries (`0046FBF0`, `00471100`,
`00471330`, `004715F0`, `004718F0`, `00472580`, `00473210`).

Four resamplers do the work. Each takes the table, the new entry count `n` and the number of channels per entry, copies the
first `n / 2` entries aside, and writes entry `2k` as source entry `k` and entry `2k + 1` as the mean of
source entries `k` and `k + 1`:

| Resampler | Values | Past the last source entry |
|---|---|---|
| `0033E310` | `f32` | wraps to entry 0 (`(k + 1) mod n/2`) |
| `0033E5E0` | `f32` | stops at `n − 1`; the last entry copies source entry `(n − 1) / 2` |
| `0033E990` | signed bytes | wraps |
| `0033ECE0` | unsigned bytes | stops, as `0033E5E0` |

- `0046FBF0` doubles the counts `01F20530` to `01F2053C` and `01F20A98` and resamples the pulse table
  `01F20AA0` among others with `0033E5E0`; `00471100` stretches the two curves `01F21F40` and `01F22030`
  to 60 entries with `0033E310`.
- `00471330`, `004715F0` and `004718F0` double their counts and resample their float tables with
  `0033E310` and `0033E5E0`, and `004718F0` two byte tables with `0033ECE0`.

The first of those counts, `01F20530` (50 in the file), sizes a curve of three floats per entry at
`01F20540`. `0046FB40(t, out)` samples it at `t` from 0 to 1 (entry `t × (count − 1)`, clamped).

Its one caller, `0042F030`, from the character pass `00426090`, walks 32 records of `0x30` bytes at
`02CA48D0`, each live while its handle `+0x04` is set (`0042F190(handle)` clears it, and `0042F000`
clears them all at start-up): a set trigger `+0x1C` starts a run of `30 × [01DFE0B4]` steps with the strength
`trigger × [01DFE0BC]`, each step adds strength × the curve sample to the three floats `+0x20`–`+0x28`,
and the record named by the word `+0x00` gets them at `+0x260`–`+0x268`, its per-axis scale.

- `00472580` and `00473210` double eight and five counts, copy each to a byte beside the tables
  (`01F240F0`, `01F264A8`), halve the floats beside them, and resample three-channel byte tables with
  `0033E990`.

## Layouts

Presentation record, `02B59D80` + slot × `0x150`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000` | `u16` | live | 1 when set up by `003E7500` |
| `004` | `i16` | record | the render-record index |
| `008` | `u32` | shown | the status word last pushed |
| `010` | `void*` | rig | `003E6DA0` of the render record, 0 = none |
| `020` | `0x50` | colourList | block 1 |
| `070` | `0x48` | second | block 2 |
| `0C0` | `u32[32]` | flags | one per status bit |
| `140` | `u32` | setBits |  |
| `144` | `u32` | clearedBits |  |

Colour-look block (record +`0x20`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | mask | bits 0-13 |
| `04` | `u8` | shown |  |
| `05` | `u8` | wanted | lowest set bit, `0xFF` = none |
| `06` | `u8` | frame | flash and cycle counter |
| `07` | `u8` | flags | bit 0 changing, bits 1-7 entry count |
| `08` | `u32` | light0 | handle |
| `0C` | `u32` | light1 | handle |
| `10` | `u32` | target | the render-record index the lights belong to |
| `18` | `void*` | step |  |
| `20` | `f32` | phase |  |
| `24` | `f32` | envelope |  |
| `28` | `void*` | renderRecord |  |
| `38` | `u8` | state | Petrify and Doom |
| `39` | `u8` | count | the remembered Petrify or Doom count |
| `3A` | `u8` | hold | control deny |
| `40` | `f32[4] offset` | the tint's colour offset |  |

Second block (record +`0x70`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `08` | `void*` | renderRecord |  |
| `10` | `u32` | mask |  |
| `14` | `u32` | enemy |  |
| `18` | `u8` | shownA |  |
| `19` | `u8` | wantedA |  |
| `1A` | `u8` | changingA |  |
| `1C` | `f32` | phaseA |  |
| `20` | `f32` | envelopeA |  |
| `28` | `void*` | stepA |  |
| `30` | `u8` | shownB |  |
| `31` | `u8` | wantedB |  |
| `32` | `u8` | changingB |  |
| `33` | `u8` | stop |  |
| `34` | `f32` | phaseB |  |
| `38` | `f32` | envelopeB |  |
| `40` | `void*` | stepB |  |

Render-record fields the looks write:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `5D0` | `f32[3]` | colour | the ambient blend target |
| `5DC` | `f32` | amount | ambient mode amount |
| `5E0` | `u8` | ambientMode | 1 blend, 2 multiply |
| `5EC` | `f32` | lightScale | copied to `02B3F518` |

## Shipped data

Measured from the executable image.

| Fact | Value |
|---|---|
| pulse table `01F20AA0` | 60 floats, a raised cosine from 0.0027 to 1.0 at entry 29 and back to 0; count `01F20538` = 60 |
| curve 1 `01F21F40` | 0.33, 0.66, then 1.0 to entry 11, falling by 0.1 to 0 at entry 21 |
| curve 2 `01F22030` | 0.5, 0.85, then 1.0 to entry 16, falling by 0.2 to 0 at entry 21 |
| frame values at 30 fps | `01DFE0BC` 1.0, `01DFE0B8` 1.0, `01DFE0B4` 1, `01F82E38` 0 |
| frame values at 60 fps | `001EDDC0` stores 0.5, 2.0, 2 and 1, then `0033F020` doubles the pulse table's count (`0046FBF0`) and stretches the two curves over twice the frames (`00471100`) |
| Immobilize constants | 1.5 (`00901B3C`), 0.5 (`01CEBB70`), 0.3 (`0091523C`), 0.7 (`008F3104`) |

## State

- `02B59D80`: the 32 presentation records.
- `02B59D70`, `02B59D71`: the control-deny and display-deny latches; `0215FD44`, `0215FD45` their requester bits.
- `02B3F518`: the light scale of the character being lit; `02B3F501` the class filter; `02B3F502` the scale enable.
- `02CB8390`: the vector Slow and Immobilize store.

## Modding notes

- The order of the colour looks is the bit order of the list; moving a status means changing the index its arm passes.
- The look colours are immediates in the switch of `0046FD00` and in the steps, not data.
- A status light is exempt from the light scale only while its byte `+5` is `0x80` or more.
- Durations are frame counts scaled by `01DFE0B4`, so they keep their length in seconds at 60 fps.

## Related

- [Statuses](../Status-Effects-And-KO/statuses.md): the 32 status bits and the two status words.
- [Status timers](../Status-Effects-And-KO/status-timers.md): the Petrify and Doom counts.
- [Character rig and look](character-rig-and-look.md): the controllers Sleep, Confuse, Immobilize and Float switch.
- [Character fades](character-fades.md): fade channel 5.
- [Character lighting and shadows](character-lighting-and-shadows.md): the light gather and the shadow pool.
- [Character render records](character-render-records.md): the render record.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): the status-denial verbs.
- [Party control modes](../Engine-Core/party-control-modes.md): the town flag.
