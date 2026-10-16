---
title: "Vibration: the pad vibration that scenes and effects play, the request slots and their steps, the Vibration Function setting, and how the levels reach an XInput or Steam pad"
kind: "system"
category: "Controls and input"
addresses: "02EC0B80, 0035B2F0, 0035B580, 0035B650, 0035AF20, 0035AE30, 0035FED0, 0035F590, 0035F690, 001E1120, 007A2140, 0035B1A0"
---

## What the player sees

- Some scenes and effects make the pad vibrate; the Config option Vibration Function turns it off.
- Only a pad that was the last device used vibrates: after a key or mouse press the pad stays still until one of
  its buttons or sticks is used again.
- A vibration that goes on for a long time fades out, stays off for a while, and comes back.
- An Xbox-style pad and a Steam controller vibrate; other pads do not.

## How it works

### The request slots

Vibration requests live in 32 slots of `20`<sub>h</sub> bytes at `02EC0B80`. `0035B270`, run once from `0022A0B0`
(`0022A429`), chains every slot into the free list `02EC0B60`, empties the playing list `02EC0B61` (`FF`<sub>h</sub>), clears
the eight recorded handles `022C8030`, the pattern table `02EC0B68` and the pause mask `02EC0B40`, and sets the output
switch `02EC0B3C` to 1 (`0035B2D5`-`0035B2DC`). No rip-relative store writes `02EC0B3C` elsewhere.

A handle is the slot's generation times 256 plus the slot number plus 1 (`0035B2F0`). Every function that takes
a handle first compares the generation, so a stale handle does nothing:

- `0035B240(handle)` returns the slot's state, or 0 for a stale handle.
- `0035B550(handle, strength)` sets the strength.
- `0035B1A0(handle)` frees the slot: it unlinks it from the playing list, raises the generation, puts it at the
  head of the free list and clears its state and pattern.

### Starting a vibration

1. `0035B2F0(pattern, channel)` takes the head of the free list when its state is 0: state 1, strength 1.0, track 1
   at pair 0 and track 2 at the pair the pattern's first `u16` names, and links it into the playing list.
2. `0035B580(handle, mask)` starts a slot in state 1: it keeps the mask and moves to state 2, or straight to state 4
   when the mask shares a bit with the pause mask `02EC0B40` (`0035B5AB`).
3. `0035B650(index, mask)` does both for pattern `index` of the loaded table on channel 0, when the index is below
   the table's count and one of the eight entries at `022C8030` is empty, and records the handle there.

| Starter | What it plays |
|---|---|
| verb `vibplay` `23D`<sub>h</sub>, handler `0034AC30` | `0035B650(pattern, 2)` through `00379F20`, unless `00267310` answers non-zero for the actor's byte `+15`<sub>h</sub> |
| verb `vibstop` `23E`<sub>h</sub>, handler `0034B0F0` | frees the eight recorded handles (`0035B460`) |
| `0034B3C0` | answers whether a recorded handle is playing or paused (`0035B380`), or frees them when `00267310` answers non-zero |
| effect sequence element of kind 3 (`004FF2C0`) | `005372D0`: on the element's frame, with fewer than four running, `0035B2F0(pattern, 0)` and `0035B580(handle, 1)`, strength `00537410`'s answer over 127 |

Each frame `0046E990` and `0046EDD0` set the strength of a sequence's running vibrations again from `00537410` and
free those that have stopped; `0046EE70` frees all of a sequence's vibrations.

### Stepping

`0035AF20` turns the time into whole steps; the field frame calls it at `0022A955`, `0022AC7A` and `0022ADDE`:

```python
accumulator 022C8050 += 10000 * [01DFE0BC]
steps = accumulator / 10000, run in one pass
accumulator = accumulator % 10000
```

The pass clears the levels `02EC0B50` (two channels of two `i32`, track 1 then track 2), then steps each playing
slot whose mask shares no bit with `02EC0B40`. A track's pair k is `{duration, level}` at `+4 + 2k`, and the next
pair's level is its end:

```python
level = int(start + (end - start) * frame / duration) * strength    (integer division, then the f32 strength)
```

The larger of that and the level already there is kept, the frame counts up, and at the duration the track moves
to the next pair. A pair with duration 0 ends its track, and a slot whose two tracks have both ended goes to state
4.

### Pausing

- `0035B4B0(mask)` adds the bits to `02EC0B40` and moves every playing slot whose mask shares a bit to state 3.
- `0035B510(mask)` removes the bits and moves every slot in state 3 back to 2, whatever its mask.
- `00226280` calls `0035B4B0(5)` when bit 29 of the flags it combines is clear and `0035B510(FFh)` otherwise
  (`002264AE`, `002264B7`).

So `vibplay`'s mask 2 is never paused, and an effect's mask 1 is.

### Output to the pad channel

`0035AE30` runs after the stepping. With the switch `02EC0B3C` on it calls `0035FED0(channel, 1, track 1 level)` and
`0035FED0(channel, 0, track 2 level)` for channels 0 and 1, and with it off it sends zeros (`0035AE41`-`0035AE95`).
It then frees every recorded handle in state 4 (`0035AEA1`-`0035AEE2`).

`0035FED0(channel, actuator, level)` stores the level byte at `+06h + actuator` of the channel record `022CAE90`
(`294`<sub>h</sub> bytes each) and the vsync count `022CA5E0` at `+1Ch + 4 × actuator`. The two capture frames, the full
menu frame and the capture-backed frame first clear the four levels with `0035AF10` (`0022AF63`, `0022B009`,
`0022BA0B`, `0022BCB7`).

### From the channel to the pad

On every poll `0035F420` calls `0035F590` (`0035F548`):

1. With the channel's flag bit 2 set, the large value is the envelope `+16`<sub>h</sub> times the actuator-1 level `+07`<sub>h</sub>,
   shifted right 14, and the small value is bit 0 of the envelope times the actuator-0 level `+06`<sub>h</sub>, shifted
   right 21; without it both are 0.
2. It hands them through `008628F0` to `001E1120(pad +02h, small, large)`, and sets flag bit 4 when either level it read
   is non-zero. `0035FCA0` clears bit 4 before each poll (`0035FCE8`).
3. `001E1120` sends zeros instead unless the input manager's last-device byte `+38`<sub>h</sub> says the pad was used last
   (`00197780`) and `00228480` answers 0 (`001E1148`-`001E116F`).
4. `00198E80` takes the n-th registered controller of kind 2 (`0079D620`, `00796FC0(2, n)`) and `007A1080` stores the
   large value at `+98`<sub>h</sub>, the small one at `+99`<sub>h</sub> and 1 at `+9A`<sub>h</sub>.

The XInput pad's update `007A2140` passes `+98`<sub>h</sub> / 255 × 65535 as the left motor and 65535 or 0 for a
non-zero or zero `+99`<sub>h</sub> as the right motor to `XInputSetState` (`007A21C5`-`007A2224`). The Steam controller's update
`007A1CD0` calls slot `88`<sub>h</sub> of the Steam controller interface `02EA9508` with `+98`<sub>h</sub> × 256 and `+99`<sub>h</sub> × 256. A
displacement scan of the listed functions in `00790000`-`007A5000` finds no other reader of `+98`<sub>h</sub>, so a DirectInput
pad gets no vibration.

### The Vibration Function setting

The Config option Vibration Function is bit 13 of the options word `*0215E6E0`. `002DE080` stores it from the Config
screen (`00240865`) and `002DDA30` applies it when the options are loaded; both pass it to `0035FF30(0, bit)`,
which sets or clears flag bit 2 of channel 0 (`002DDAA4`). Channel 1 has no setter of that bit in a raw call scan
of `0035FF30`.

### The fade-out

`0035F690` runs after each poll of the channel (`0035FD8D`) and moves the envelope `+16`<sub>h</sub> between 0 and `4000`<sub>h</sub> by
the step `+18`<sub>h</sub>:

| While | Count | What happens |
|---|---|---|
| vibrating (flag bit 4) | `+12`<sub>h</sub> past `6DF`<sub>h</sub> (1759 polls) | the step becomes -546: the envelope falls |
| vibrating | `+12`<sub>h</sub> past `6FE`<sub>h</sub> (1790 polls) | the envelope is held at 0 while `+10`<sub>h</sub> counts |
| vibrating | `+10`<sub>h</sub> past `B3`<sub>h</sub> (180 polls) | the step becomes +546 and the counts restart |
| not vibrating | `+14`<sub>h</sub> reaches `B4`<sub>h</sub> (180 polls) | the envelope returns to `4000`<sub>h</sub> and `+12`<sub>h</sub> to 0 |

## Layouts

A request slot is `20`<sub>h</sub> bytes; the 32 slots sit at `02EC0B80`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | next | the next slot in the free or playing list; `FF`<sub>h</sub> ends it |
| `01`<sub>h</sub> | `u8` | state | 0 free, 1 taken, 2 playing, 3 paused, 4 finished |
| `02`<sub>h</sub> | `u16` | generation | raised by every free (`0035B1A0`) |
| `08`<sub>h</sub> | `u8*` | pattern | the pattern record |
| `10`<sub>h</sub> | `f32` | strength | 1.0 when taken; set by `0035B550` |
| `14`<sub>h</sub> | `u16` | step1 | track 1's pair |
| `16`<sub>h</sub> | `u16` | step2 | track 2's pair |
| `18`<sub>h</sub> | `u8` | frame1 | steps into track 1's pair |
| `19`<sub>h</sub> | `u8` | frame2 | steps into track 2's pair |
| `1A`<sub>h</sub> | `i16` | channel | the level pair it writes |
| `1C`<sub>h</sub> | `u8` | mask | the pause bits it answers to |

## Shipped data

`common/eventvib.bin` holds 11 patterns. In every one track 2 starts at pair 2, whose duration is 0, so only track 1
plays:

| Patterns | Duration in steps | Level |
|---|---:|---|
| 0, 3 | 15, 35 | 120 |
| 1 | 15 | 155 rising to 160 |
| 4 | 35 | 160 |
| 2, 5 | 15, 35 | 230 |
| 6, 7 | 15, 35 | 255 |
| 8, 9, 10 | 5 | 140, 180, 255 |

## Modding notes

- A second track in `eventvib.bin` drives the right motor, which is either off or full: the small value is 1 only
  for a level of 128 or more at full envelope.
- The table's patterns always play on channel 0, the only channel the Vibration Function setting reaches.
- `0035B510` resumes every paused vibration, not only those of the mask it clears.
- The pattern file's layout is on [Small .bin tables](../Game-Files-And-Data-Tables/small-bin-tables.md).

## Related

- [Controls](controls.md) - the channel record, the poll and the last-device byte.
- [Controllers](controllers.md) - the XInput, Steam and DirectInput controllers.
- [Small .bin tables](../Game-Files-And-Data-Tables/small-bin-tables.md) - the `VIB0` file.
- [Config screen](../Menus-And-HUD/config-screen.md) - the Vibration Function row.
