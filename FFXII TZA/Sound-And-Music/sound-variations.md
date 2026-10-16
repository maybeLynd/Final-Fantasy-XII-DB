---
title: "Sound variations: the random, ordered, cycling and switched sound kinds the driver supports, and the trigger that arms a sound"
kind: "system"
category: "Sound and music"
addresses: "007B2F70, 007BD370, 007E5160, 007E58D0, 007E6360, 007E67C0, 007BD240, 007E7540"
---

## What the player sees

- One sound in a bank always plays the same way: no shipped sound uses the driver's random, ordered, cycling or
  switched kinds.
- The variety in swings, voices and footsteps comes from the character's sound emitter, which picks a different sound
  ([Animation sounds](animation-sounds.md)).

## How it works

### The sound kinds

The factory `007B2F70` builds one object per sound played. It reads the sound record's class byte `+4`
(`007B30C7`):

| Class | Object | Select |
|---:|---|---|
| `0`, `1` | `Sound` | `007BD370`: plays every candidate |
| `2` | `RandomSound` | `007E5160` |
| `3` | `OrderSound` | `007E58D0` |
| `4` | `CycleSound` | `007E6360` |
| `5` | `SwitchSound` | `007E67C0` |

The names are the classes' run-time type names. When the bank is a streaming bank not yet loaded, the factory builds a
`VariationSound` instead (`007B2FF2`): the bank's readiness answer, `007E4300` for a streaming bank, is false, and
`007E56E0` builds it. It keeps only the requested sound number and never selects
(`007E57D0`, `007E57C0`).

### The records

A sound record lists its candidates as 16-byte entries (`007CFAC0`); entry word `+4` names a sequence record in the
bank's `seq ` chunk. A sequence record is read by its version byte `+0`:

| Field | Versions 0-2 | Version 3 and up | Read by |
|---|---|---|---|
| weight `u8` | `+4` | `+10`<sub>h</sub> | `007CF9C0`, `007CF830` |
| group `u8` | `+5` | `+11`<sub>h</sub> | `007CF9A0` |
| switch low `f32` | `+4` (0 below version 2) | `+10`<sub>h</sub> | `007CFBF0` |
| switch high `f32` | `+8` (0 below version 2) | `+14`<sub>h</sub> | `007CFBC0` |

The sound record also holds the candidate count at `+5`, the category at `+6`, the sound's number at `+8`, the last
pick or cursor at `+1`, the cycle interval in milliseconds at `+10`<sub>h</sub>/`+14`<sub>h</sub>, the cycle group limit at `+18`<sub>h</sub> and
the allow-repeat bit 5 of `+19`<sub>h</sub>. The select writes `+1` into the loaded bank data, so every object made from one
record shares it.

### Sets

Random, ordered and cycling sounds walk the candidates in sets: from a candidate, the following ones with the same
group byte join it, and only the first one's weight counts. A plain or switched sound tests every candidate on its own.

### The rules

| Kind | Rule |
|---|---|
| Random | every set of weight 0 plays; one draw `rand() % 101` (`007E5325`-`007E5348`) picks a weighted set by running total; a repeat of `+1` is replaced by the heaviest other weighted set unless `+19`<sub>h</sub> bit 5 allows it |
| Order | every set of non-zero weight plays; the weight-0 sets take turns, one per play, through the cursor `+1`, which wraps (`007E5BC7`-`007E5BD2`) |
| Cycle | as Random, but a set whose group still sounds is also replaced (`007E5E80`); while fewer than `+18`<sub>h</sub> groups sound it picks again every `rand() % (max - min + 1) + min` milliseconds (`007E65B0`, `007E6620`) |
| Switch | every candidate whose `low <= v < high` plays, with `v` a named value: `default`, `distance`, or a lookup by name (`007BD9D0`) |

### The random source

`rand` is the C runtime's (import at `008C3098`). The driver thread seeds it once with `srand` from a microsecond
clock (`007A5404`-`007A540B`), so the draws differ on every run.

### Arming

When a sound plays (`007BDFA0`), its start step `007BD120` runs the select once (`007BD205`). The select calls the
trigger `007BD240(sound, sequence)` for each candidate it chooses:

1. It refuses in states 0, 6 and 7 (`007BD252`-`007BD260`).
2. It takes the next slot, counting it before the bind (`007BD266`-`007BD276`).
3. It binds a `Sequence` object (`007B4EF0`, `007BD2A7`) and pushes the sound's settings to it.
4. It arms the sequence with a start offset and a start delay (`007E7300`, `007BD311`-`007BD333`), which sets its
   state to 2 and plays nothing.

The sequence's own update `007E7540` counts the delay down and then starts it (`007E759A`-`007E75C7`). The delay is
0, so a sound starts on its sequence's next update.

### Playing a sequence

Each kind is the `Sound` object (`007BC8D0` builds it, `007BCE00` tears it down) with its own vtable:
`RandomSound` `007E50A0`, `OrderSound` `007E5810`, `CycleSound` `007E5CD0` and `SwitchSound` `007E6700`;
`007E5DA0`, from the cycling rule, walks the sound's sequences by group (`007CF9A0`). A sound keeps its sequences' handles at `+400`<sub>h</sub>, their count at
`+4C`<sub>h</sub>. `007E6960` builds a `Sequence` and `007E71F0` binds it to its record, printing "seq data invalid!" without one.

When its delay has run out, the sequence starts its track (`007E6AA0`):

1. It finds the track record the sequence names in the bank's `trk ` chunk and creates the track (`007B5690`): a
   `MaterialTrack` (`007E9240`) plays a material, a `SoundTrack` (`007E99E0`) plays another sound, both over the
   `Track` base `007E7A90` (`007E7D40` tears it down).
2. It hands the track the sequence's values (`007E8B30`, `007E8B20`, `007E8AA0`, `007E8AB0`, `007E8AF0`); a
   `SoundTrack` also passes its child sound a ramp and the switch value (`007E9F40`, `007E9EF0`).
3. It applies the sequence's zero-one curves of type 3 to the track (its slot 3), then runs `007E8960` on it.

A sequence's state `+9C`<sub>h</sub> (`007E71E0`) is 2 while it plays, 3 while it stops, 4 once it has ended and 5 while paused:
`007E7340` resumes it, `007E74A0` stops it and `007E7500` pauses it, each passing the change to its track (`007E8A40`,
`007E8B40`, `007E8B90`), whose own state `+1E8`<sub>h</sub> ends at 5. `007E72E0` marks a stop request unless the sequence has
ended.

Each pass the sound passes its values to every sequence, which marks them changed and hands them to its track on its
own update:

| Sound value | Forwarder | Sequence setter |
|---|---|---|
| slot 26 | `007BFE30` | `007E7420` (`+38`<sub>h</sub>) |
| slot 27 | `007BFDB0` | `007E7410` (`+40`<sub>h</sub>) |
| slot 28, three values | `007BFD00` | `007E73F0` (`+48`<sub>h</sub>) |
| the ramp at `+2B0`<sub>h</sub> | `007BFC30` | `007E73D0` (`+54`<sub>h</sub>) |
| byte `+3F8`<sub>h</sub> | `007BFBA0` | `007E73C0` (`+5C`<sub>h</sub>) |
| the ramps at `+248`<sub>h</sub>, by index | `007BFEB0` | `007E7430` (`+60`<sub>h</sub>), which also ramps a `SoundTrack`'s child |
| four bus bytes `+80`<sub>h</sub> | `007BF9B0` | `007E7380` (`+6C`<sub>h</sub>) |
| four send ramps | `007BFA60` | `007E73A0` (`+70`<sub>h</sub>) |

The track side takes them through `007E8A60`, `007E8A80` and `007E8AD0`. `007BE370`, `007BE390` and `007BE500` set a
sound's send bus and level and its main send level, and `007BE4D0` clears `+180`<sub>h</sub> and ramps a value from a macro.
`007E71C0` gives a sequence's sound (its handle at `+10`<sub>h</sub>) and `007E73E0` stores a sequence's `+68`<sub>h</sub>.
`007BD5E0` gives a sound's id, its bank's number over its sound number, once the bank is ready.

### A track's update

The track pass `007B5AD0` runs `007E8BB0(track, seconds)` on every track:

1. It sets the track's state `+1E8`<sub>h</sub> to 5 when a stop was asked (`+1EC`<sub>h</sub>), or in state 4, unless its slot 4 still
   answers true.
2. When its volume ramp or volume LFO moved, it hands `007E87E0`'s value to slot 5.
3. When its pitch ramp or pitch LFO moved, it hands `007E8740`'s value to slot 6.
4. With a curve at `+3B8`<sub>h</sub> it moves the curve on (`007E9030`).
5. When a panning ramp or a panning LFO moved, it hands `007E8410`'s five values to slot 7.
6. It passes changed flags and values to slots 8 to 12: the filter flag, the values `+1A8`<sub>h</sub> and `+1B0`<sub>h</sub>, the four
   bus bytes `+1B4`<sub>h</sub> and the four send levels `+1B8`<sub>h</sub>.

A `MaterialTrack` passes slots 5 to 8 to its voice `+3C8`<sub>h</sub> (`007E95D0` volume, `007E9580` pitch, `007E9500`
panning, `007E92D0` the filter flag through `007EA9C0`). The values are:

```python
volume = base(+0x30) * ramp(+0x38), then + offset(+0x1CC) when above 0 (mode +0x1C8 = 1) or * offset (mode 2) * (1 + LFO(+0x1F8))
pitch = base(+0x68) * ramp(+0x70), then + offset(+0x1D4) (mode +0x1D0 = 1) or * offset (mode 2) * (1 + LFO(+0x268))
```

`007E8410` builds the five panning values: two sums (`+A0`<sub>h</sub> plus the ramp `+B8`<sub>h</sub>, `+A8`<sub>h</sub> plus the ramp `+118`<sub>h</sub>)
and three products (`+A4`<sub>h</sub>, `+B0`<sub>h</sub> and `+AC`<sub>h</sub> times the ramps `+E8`<sub>h</sub>, `+178`<sub>h</sub> and `+148`<sub>h</sub>). The `+A0`<sub>h</sub> sum also
takes the offset mode `+1D8`<sub>h</sub> and the LFO `+2D8`<sub>h</sub>, and the `+A4`<sub>h</sub> product the mode `+1E0`<sub>h</sub> and the LFO `+348`<sub>h</sub>, each
LFO added.

`007E8720` gives a track's sequence (its handle `+10`<sub>h</sub>, `007B5070`).

### Track LFOs

A track has four LFOs of `70`<sub>h</sub> bytes from `+1F8`<sub>h</sub>, which `007F3DF0` clears when the track is built
(`007E7B58`-`007E7B81`): a phase at `+00`<sub>h</sub>, a depth ramp at `+08`<sub>h</sub>, a period ramp at `+38`<sub>h</sub> and a wave byte at `+68`<sub>h</sub>. `007F40B0(lfo, seconds)` moves
a running one on: it advances both ramps and adds `seconds / period` to the phase, keeping its fraction. `007F3E60`
gives its value, the depth times the wave at the phase `p`:

| Wave | Shape |
|---:|---|
| 0 | none: 0 |
| 1 | `sin(2pi * p)` |
| 2 | 1 below `p` 0.5, then -1 |
| 3 | triangle: 0 up to 1 at 0.25, down to -1 at 0.75, up to 0 |
| 4 | rising saw: `2p`, then `2p - 2` from 0.5 |
| 5 | a new random value from 0 to 1 on every call (`007F3E30`, from `rand`) |
| 6 | `-sin(2pi * p)` |
| 7 | -1 below `p` 0.5, then 1 |
| 8 | 0 down to -1 at 0.25, up to 1 at 0.75, then on up to 2 at the end of the cycle |
| 9 | falling saw: `-2p`, then `2 - 2p` from 0.5 |

Wave 8's last quarter is `4(p - 0.75) + 1` (`007F3FFF`-`007F400B`), so it does not return to 0 before the phase wraps.

## Shipped data

Over all 4,609 `.sab` banks:

| | |
|---|---|
| sound records | 13,150 |
| class 0 | 1,985, with no candidate |
| class 1 | 11,165, each with one candidate |
| classes 2-5 | none |
| weights, groups, switch ranges, cycle intervals, allow-repeat bits | 0 in every record |

So every shipped sound is a plain `Sound`, and the random, ordered, cycling and switched rules never run.

## Modding notes

- Setting a sound's class byte to 2-5 and giving it more than one candidate turns on the driver's variation rules;
  the sequence records must carry the weights and groups.
- A random or cycling sound advances the C runtime's `rand`, which the driver thread alone seeds.
- More than 32 candidates would walk past the slot array, because the trigger does not check the slot count.

## Related

- [Sound banks](sound-banks.md) - the bank container and its chunks.
- [Sound effects](sound-effects.md) - the play call that reaches the driver.
- [Animation sounds](animation-sounds.md) - where the game's variation comes from.
