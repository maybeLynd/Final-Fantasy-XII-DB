[Home](../../README.md) / [Sound and music](README.md) / Sound variations

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Sound variations: the random, ordered, cycling and switched sound kinds the driver supports, and the trigger that arms a sound | system | Sound and music | Sound effects and voices | How the sound driver chooses what to play for one sound: the class byte that selects a plain, random, ordered, cycling or switched sound, the candidate and sequence records they read, sets of candidates by group, each kind's rule with its weighted roll, rotation, cycle timer or switch range, the random seed, the trigger that arms a sequence for the next update, what a track hands its voice on each pass with its four LFOs and their ten wave shapes, and the shipped banks, where every sound is plain with at most one candidate. | 0x007B2F70, 0x007BD370, 0x007E5160, 0x007E58D0, 0x007E6360, 0x007E67C0, 0x007BD240, 0x007E7540 |

## What the player sees

- One sound in a bank always plays the same way: no shipped sound uses the driver's random, ordered, cycling or
  switched kinds.
- The variety in swings, voices and footsteps comes from the character's sound emitter, which picks a different sound
  ([Animation sounds](animation-sounds.md)).

## How it works

### The sound kinds

The factory `0x007B2F70` builds one object per sound played. It reads the sound record's class byte `+4`
(`0x007B30C7`):

| Class | Object | Select |
|---:|---|---|
| `0`, `1` | `Sound` | `0x007BD370`: plays every candidate: for each of the record's `+5` candidates it finds the sequence record that entry word `+4` names and calls the trigger, whatever the trigger returns, then returns 0 (`0x007BD3D7`-`0x007BD486`, `0x007BD4BC`) |
| `2` | `RandomSound` | `0x007E5160` |
| `3` | `OrderSound` | `0x007E58D0` |
| `4` | `CycleSound` | `0x007E6360` |
| `5` | `SwitchSound` | `0x007E67C0` |

The names are the classes' run-time type names. When the bank is a streaming bank not yet loaded, the factory builds a
`VariationSound` instead (`0x007B2FF2`): the bank's readiness answer, `0x007E4300` for a streaming bank, is false, and
`0x007E56E0` builds it. It keeps only the requested sound number and never selects
(`0x007E57D0`, `0x007E57C0`).

The factory finds the record by its index or, for an id with bit `0x40000000` set, by the sound number at record
`+8` that equals the id without that bit (`0x007B302C`-`0x007B308E`). A number that matches no record, an index below 0
or not below the count (`0x007B3095`-`0x007B30A9`), a class above 5 (`0x007B311D`) or a null block (`0x007B30D3`,
`0x007B3149`) builds nothing and returns -1 (`0x007B3170`).

Otherwise the factory runs the class's constructor: `0x007BC8D0` for classes 0 and 1 (`0x007B3127`), `0x007E50A0`,
`0x007E5810`, `0x007E5CD0` or `0x007E6700` for classes 2 to 5 (`0x007B30DB`, `0x007B30EE`, `0x007B3101`, `0x007B3114`), or
`0x007E56E0` for the `VariationSound` (`0x007B3151`). It then runs the object's slot 40 (`+0x140`) with a block of its
arguments and returns that slot's result (`0x007B315E`-`0x007B3168`).

### The records

A sound record lists its candidates as 16-byte entries (`0x007CFAC0`); entry word `+4` names a sequence record in the
bank's `seq ` chunk. A sequence record is read by its version byte `+0`:

| Field | Versions 0-2 | Version 3 and up | Read by |
|---|---|---|---|
| weight `u8` | `+4` | `+0x10` | `0x007CF9C0`, `0x007CF830` |
| group `u8` | `+5` | `+0x11` | `0x007CF9A0` |
| switch low `f32` | `+4` (0 below version 2) | `+0x10` | `0x007CFBF0` |
| switch high `f32` | `+8` (0 below version 2) | `+0x14` | `0x007CFBC0` |

The sound record also holds the candidate count at `+5`, the category at `+6`, the sound's number at `+8`, the last
pick or cursor at `+1`, the cycle interval in milliseconds at `+0x10`/`+0x14`, the cycle group limit at `+0x18` and
the allow-repeat bit `0x20` of `+0x19`. The select writes `+1` into the loaded bank data, so every object made from one
record shares it.

### Sets

Random, ordered and cycling sounds walk the candidates in sets: from a candidate, the following ones with the same
group byte join it, and only the first one's weight counts. A plain or switched sound tests every candidate on its own.

### The rules

| Kind | Rule |
|---|---|
| Random | every set of weight 0 plays; one draw `rand() % 101` (`0x007E5325`-`0x007E5348`) picks a weighted set by running total; a repeat of `+1` is replaced by the heaviest other weighted set unless `+0x19` bit `0x20` allows it |
| Order | every set of non-zero weight plays; the weight-0 sets take turns, one per play, through the cursor `+1`, which wraps (`0x007E5BC7`-`0x007E5BD2`) |
| Cycle | as Random, but a set whose group still sounds is also replaced (`0x007E5E80`); while fewer than `+0x18` groups sound it picks again every `rand() % (max - min + 1) + min` milliseconds (`0x007E65B0`, `0x007E6620`) |
| Switch | every candidate whose `low <= v < high` plays, with `v` a named value: `default`, `distance`, or a lookup by name (`0x007BD9D0`) |

### The random source

`rand` is the C runtime's (import at `0x008C3098`). The driver thread seeds it once with `srand` from a microsecond
clock (`0x007A5404`-`0x007A540B`), so the draws differ on every run.

### Arming

When a sound plays (`0x007BDFA0`), its start step `0x007BD120` runs the select once (`0x007BD205`). The select calls the
trigger `0x007BD240(sound, sequence)` for each candidate it chooses:

1. It refuses in states 0, 6 and 7 (`0x007BD252`-`0x007BD260`), returning -1 (`0x007BD365`).
2. It takes the next slot, counting it before the bind (`0x007BD266`-`0x007BD276`).
3. It binds a `Sequence` object (`0x007B4EF0`, `0x007BD2A7`) into the slot's handle at `+0x400`; a negative result
   skips the next two steps and is returned, with the slot still counted (`0x007BD2AF`-`0x007BD2B1`).
4. It pushes the sound's settings to it: `0x007BFE30`, `0x007BFDB0`, `0x007BFD00`, `0x007BFEB0` for indexes 0 and 1,
   `0x007BFBA0` and `0x007BFC30` (`0x007BD2D8`-`0x007BD30C`).
5. It arms the sequence with a start offset and a start delay (`0x007E7300`, `0x007BD311`-`0x007BD333`), which sets its
   state to 2 and plays nothing. The offset is `+0x500` while the sound's state is 1 or 2 and 0 otherwise
   (`0x007BD311`-`0x007BD32B`); the delay is `+0x51C` (`0x007BD317`). `0x007E7300` returns -1 without arming a sequence
   that is not in state 1 (`0x007E7307`, `0x007E7309`), and the trigger does not test that result.
6. On every exit it sets its sequence argument's vtable word to `0x01CB4D48`; after a bind it returns the bind's
   result (`0x007BD342`-`0x007BD34C`, `0x007BD35B`).

The sequence's own update `0x007E7540` counts the delay down and then starts it (`0x007E759A`-`0x007E75C7`). The delay is
0, so a sound starts on its sequence's next update.

### Playing a sequence

Each kind is the `Sound` object (`0x007BC8D0` builds it, `0x007BCE00` tears it down) with its own vtable, which the
kind's constructor writes after it runs `0x007BC8D0`: `RandomSound` `0x007E50A0` writes `0x01CB87A8`, `OrderSound`
`0x007E5810` writes `0x01CB8AD8`, `CycleSound` `0x007E5CD0` writes `0x01CB8C70` and `SwitchSound` `0x007E6700` writes
`0x01CB8E08` (`0x007E50AE`, `0x007E581E`, `0x007E5CDE`, `0x007E670E`).

`0x007E5DA0`, from the cycling rule, walks the sound's sequences by group (`0x007CF9A0`). A sound keeps its sequences'
handles at `+0x400`, their count at `+0x4C`. `0x007E6960` builds a `Sequence` and `0x007E71F0` binds it to its record,
printing "seq data invalid!" without one.

When its delay has run out, the sequence starts its track (`0x007E6AA0`):

1. It finds the track record the sequence names in the bank's `trk ` chunk and creates the track (`0x007B5690`): a
   `MaterialTrack` (`0x007E9240`) plays a material, a `SoundTrack` (`0x007E99E0`) plays another sound, both over the
   `Track` base `0x007E7A90` (`0x007E7D40` tears it down).
2. It hands the track the sequence's values (`0x007E8B30`, `0x007E8B20`, `0x007E8AA0`, `0x007E8AB0`, `0x007E8AF0`); a
   `SoundTrack` also passes its child sound a ramp and the switch value (`0x007E9F40`, `0x007E9EF0`).
3. It applies the sequence's zero-one curves of type 3 to the track (its slot 3), then runs `0x007E8960` on it.

A sequence's state `+0x9C` (`0x007E71E0`) is 2 while it plays, 3 while it stops, 4 once it has ended and 5 while paused:
`0x007E7340` resumes it, `0x007E74A0` stops it and `0x007E7500` pauses it, each passing the change to its track (`0x007E8A40`,
`0x007E8B40`, `0x007E8B90`), whose own state `+0x1E8` ends at 5. `0x007E72E0` marks a stop request unless the sequence has
ended.

Each pass the sound passes its values to every sequence, which marks them changed and hands them to its track on its
own update:

| Sound value | Forwarder | Sequence setter |
|---|---|---|
| slot 26 | `0x007BFE30` | `0x007E7420` (`+0x38`) |
| slot 27 | `0x007BFDB0` | `0x007E7410` (`+0x40`) |
| slot 28, three values | `0x007BFD00` | `0x007E73F0` (`+0x48`) |
| the ramp at `+0x2B0` | `0x007BFC30` | `0x007E73D0` (`+0x54`) |
| byte `+0x3F8` | `0x007BFBA0` | `0x007E73C0` (`+0x5C`) |
| the ramps at `+0x248`, by index | `0x007BFEB0` | `0x007E7430` (`+0x60`), which also ramps a `SoundTrack`'s child |
| four bus bytes `+0x80` | `0x007BF9B0` | `0x007E7380` (`+0x6C`) |
| four send ramps | `0x007BFA60` | `0x007E73A0` (`+0x70`) |

The track side takes them through `0x007E8A60`, `0x007E8A80` and `0x007E8AD0`. `0x007BE370`, `0x007BE390` and `0x007BE500` set a
sound's send bus and level and its main send level, and `0x007BE4D0` clears `+0x180` and ramps a value from a macro.
`0x007E71C0` gives a sequence's sound (its handle at `+0x10`) and `0x007E73E0` stores a sequence's `+0x68`.
`0x007BD5E0` gives a sound's id, its bank's number over its sound number, once the bank is ready.

### A track's update

The track pass `0x007B5AD0` runs `0x007E8BB0(track, seconds)` on every track:

1. It sets the track's state `+0x1E8` to 5 when a stop was asked (`+0x1EC`), or in state 4, unless its slot 4 still
   answers true.
2. When its volume ramp or volume LFO moved, it hands `0x007E87E0`'s value to slot 5.
3. When its pitch ramp or pitch LFO moved, it hands `0x007E8740`'s value to slot 6.
4. With a curve at `+0x3B8` it moves the curve on (`0x007E9030`).
5. When a panning ramp or a panning LFO moved, it hands `0x007E8410`'s five values to slot 7.
6. It passes changed flags and values to slots 8 to 12: the filter flag, the values `+0x1A8` and `+0x1B0`, the four
   bus bytes `+0x1B4` and the four send levels `+0x1B8`.

A `MaterialTrack` passes slots 5 to 8 to its voice `+0x3C8` (`0x007E95D0` volume, `0x007E9580` pitch, `0x007E9500`
panning, `0x007E92D0` the filter flag through `0x007EA9C0`). The values are:

```python
volume = base(+0x30) * ramp(+0x38), then + offset(+0x1CC) when above 0 (mode +0x1C8 = 1) or * offset (mode 2) * (1 + LFO(+0x1F8))
pitch = base(+0x68) * ramp(+0x70), then + offset(+0x1D4) (mode +0x1D0 = 1) or * offset (mode 2) * (1 + LFO(+0x268))
```

`0x007E8410` builds the five panning values: two sums (`+0xA0` plus the ramp `+0xB8`, `+0xA8` plus the ramp `+0x118`)
and three products (`+0xA4`, `+0xB0` and `+0xAC` times the ramps `+0xE8`, `+0x178` and `+0x148`). The `+0xA0` sum also
takes the offset mode `+0x1D8` and the LFO `+0x2D8`, and the `+0xA4` product the mode `+0x1E0` and the LFO `+0x348`, each
LFO added.

`0x007E8720` gives a track's sequence (its handle `+0x10`, `0x007B5070`).

### Track LFOs

A track has four LFOs of `0x70` bytes from `+0x1F8`, which `0x007F3DF0` clears when the track is built
(`0x007E7B58`-`0x007E7B81`): a phase at `+0x00`, a depth ramp at `+0x08`, a period ramp at `+0x38` and a wave byte at `+0x68`. `0x007F40B0(lfo, seconds)` moves
a running one on: it advances both ramps and adds `seconds / period` to the phase, keeping its fraction. `0x007F3E60`
gives its value, the depth times the wave at the phase `p`:

| Wave | Shape |
|---:|---|
| 0 | flat: 0 |
| 1 | `sin(2pi * p)` |
| 2 | 1 below `p` 0.5, then -1 |
| 3 | triangle: 0 up to 1 at 0.25, down to -1 at 0.75, up to 0 |
| 4 | rising saw: `2p`, then `2p - 2` from 0.5 |
| 5 | a new random value from 0 to 1 on every call (`0x007F3E30`, from `rand`) |
| 6 | `-sin(2pi * p)` |
| 7 | -1 below `p` 0.5, then 1 |
| 8 | 0 down to -1 at 0.25, up to 1 at 0.75, then on up to 2 at the end of the cycle |
| 9 | falling saw: `-2p`, then `2 - 2p` from 0.5 |

Wave 8's last quarter is `4(p - 0.75) + 1` (`0x007F3FFF`-`0x007F400B`), so it does not return to 0 before the phase wraps.

## Shipped data

Over all 4,609 `.sab` banks:

| | |
|---|---|
| sound records | 13,150 |
| class 0 | 1,985, with no candidate |
| class 1 | 11,165, each with one candidate |
| classes 2-5 | 0 |
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
