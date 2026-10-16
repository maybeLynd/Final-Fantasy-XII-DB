---
title: "Interactive music: the driver's music object, its sections, modes and layers, the commands that start, switch and end it, and its bar-beat-tick timing"
kind: "system"
category: "Sound and music"
addresses: "007C82D0, 007CAB80, 007C1620, 007C9E70, 007C91F0, 007CA7C0, 007C5760, 007F3570"
---

## What the player sees

- Switching the music version in the Config menu keeps the track playing from the same point in the new version,
  with a short crossfade.
- Every track can start from a chosen bar.

## How it works

### The music object

A playing music is a `Magi::Music` (vtable `01CB5E38`), one of eight `0x8D8`-byte objects
([Sound driver objects](sound-driver-objects.md)). It keeps its bank's music header at `+0x18` and a state at `+0xC8`:
1 once built, 2 while it waits for its data, and 7 when it has ended and the update pass frees it (`007B7D60`). Its
sample rate is at `+0x64C` and its current section at `+0x638`.

### The music header

A `.mab` bank's `musc` chunk holds one header per music, read through `MabFile` wrapper classes, each named by its
run-time type and built by one accessor:

| Class | Accessor | From |
|---|---|---|
| `Music` | `007D0550` | the `musc` chunk, by index |
| `Section` | `007D0600` | the music, by index below byte `+0x04` |
| `Mode` | `007D0460` | the music, by index below byte `+0x05` |
| `EndMethod`, `StartMethod` | `007D0180`, `007D0650` | the music; the start-method count is byte `+0x42` |
| `ZeroOne` | `007D0710` | the music, by index below byte `+0x43` |
| `Layer`, `Meter`, `CustomPointList`, `VolumeAutomation` | `007D03B0`, `007D0400`, `007D0120`, `007D06B0` | a section |
| `ModeParam`, `ModeTransitionParam` | `007D04C0`, `007D0510` | a mode; the transition records are `0x20` bytes and skip the mode's own index |
| `MusicPoint` | `007D05D0` | `0x10`-byte records |
| `Instrument`, `InstrumentChunk`, `InstrumentMaterial` | `007D01E0`, `007D0210`, `007D0380` | the `inst` chunk; materials are `0x20`-byte records |

A header's offset table starts at its `u16` `+0x02`, moved on by `(nameLength + 0x10) & 0xF0`: the name length is
byte `+0x48` of a music header from version 9 and byte `+0x04` of a section header from version 8. `007CFFB0` and `007CFFE0` build and drop the `MabFile` wrapper. `007C30C0` refuses a music whose
section or mode headers are newer than the driver reads ("Music::CheckVersion failed").

### Commands

The game's calls post these commands ([Sound driver objects](sound-driver-objects.md)); the driver thread runs them
in `007AB5C0`:

| Type | Arm | Does |
|---:|---|---|
| `0x1C` | `007C8370(music, section, ..., time)` | plays a section: only in state 1, fading `+0x190` in to 1.0 over the time, starting at once when the data is in (`007C2280`, `007C36C0`) and otherwise setting state 2 |
| `0x1D` | `007C9E70(music, section)` | moves to a section: `007C8B20` builds the transition and `007C4790` runs it; with no header yet it only stores the section at `+0x680`; a bad index prints "Invalid section index" |
| `0x1E` | `007C91B0` | stores a flag at `+0x5F6` |
| `0x1F` | `007C91D0` | ramps the value at `+0x340` |
| `0x20` | `007C91F0(music, layer, ...)` | ramps one of the eight layer volumes at `+0x3A0`, `0x30` bytes apart; a layer of 8 or more prints "SetLayerVolume index out of range" |
| `0x22` | `007C1620(music, mode, value, time)` | starts a mode change: in a state below 2, in state 7 or with `+0x70C` at 0 it prints "Not appropriate state for transition"; a bad mode index prints "Invalid mode index"; otherwise it clamps the value to 0-1, ramps `+0x710` to 1.0 and sets `+0x70C` to 5 |
| `0x23` | `007C82D0(music, timing, ..., section)` | plays a section from a bar, beat and tick, with the same state rule as `0x1C` |
| `0x24` | `007C7120(music, section, timing)` | moves to a section at a timing: the sample of the timing (`007C65C0`), then `007C4790` |
| `0x25` | `007C9FB0` | sets the next section and the timing to switch at; a timing past the end prints "SetNextSectionAndTiming timing is over EndTiming!!" |
| `0x26` | `007CAB80(music, section, seconds)` | moves to the same timing in another section, as below |
| `0x27` | `007CA7C0(music, method)` | starts by a start method below the count: a method of type 1 or 2 plays its section (`007C8370`), and type 3 calls `007C82D0` with the method's timing `+0x08` and section `+0x06`; an index past the count prints "Invalid method index", and any other type prints a message naming the type that ends "try stop.", and returns -1 without stopping anything |
| `0x28` | `007C5760(music, method)` | ends by an end method; a method type it does not handle prints a message and stops the music |
| `0x29`, `0x2A` | `007C87E0`, `007CB320` | add an entry to, and remove one from, the list at `+0x8A8` (`007DCB50` appends, `007DD220` removes) |
| `0x2B` | `007C9C20` | queues the next music, or prints "Music::SetNextMusic can't find nextMusic" |

Commands that need the music's data print "musicData_ is not streamed yet." when it has not arrived. `007C6490` gives
the play position in seconds, or prints "Music::GetPlaySec Failed to get currentSample!".

### Moving to another section

`007CAB80(music, section, seconds)` is how a music changes version:

1. It takes the current section's sync type, byte `+0x20` (from version 5; earlier ones add 3 when it is 2 or more),
   and finds the next sync point at least `seconds + 0.2` ahead (`007C1830`, "Music::SyncTo failed to CalcSampleDelay"
   when there is none).
2. It finds the same bar, beat and tick in the target section (`007C65C0`), moving it back so the change starts
   `seconds` before that point.
3. It starts the transition into the target section over `seconds` (`007C4790`).

`00222AD0` calls it with the new music version as the section and 4.0 seconds ([Music](music.md)); `002228A0` passes
the version as the section to `0x1C` and `0x23`.

### Bar, beat and tick

A timing is a bar (`i16`), a beat (`i8`) and a tick (`i8`); a meter gives the ticks per bar (`+0x20`) and per beat
(`+0x21`). Every helper works on the total tick count and splits it back:

```python
total = bar * ticksPerBar + beat * ticksPerBeat + tick
bar = total / ticksPerBar
beat = (total - bar * ticksPerBar) / ticksPerBeat
tick = the rest
```

| Function | Does |
|---|---|
| `007F2EA0` | normalises a timing |
| `007F2E30`, `007F2F30` | one tick back, one tick forward |
| `007F3140` | subtracts one timing from another |
| `007F2F10` | rounds up to the next bar when the beat or tick is not 0 |
| `007F2FA0`, `007F3080` | round a timing (bar `+0`, beat `+2`, tick `+3`) down to the grid of a sync type, and step it by one grid unit: 3 two ticks, 4 three ticks, 5 a beat, 6 two beats, 7 a bar, 8 two bars, 9 four bars, 10 eight bars, and for the step only 2 one tick; rounding clears the smaller units, and a step carries into the next beat at `+0x21` ticks and into the next bar at `+0x20` |
| `007F3570` | the sample of a timing; a timing before the start or past the end is clamped with a warning ("GetSampleFromTiming timing is before startTiming") |
| `007F3800` | the timing of a sample, through `007F2EA0`; "GetTimingFromSample Invalid Timing!" outside the music |
| `007F3510` | the sample of a custom point: from its timing (`007F3570`) when its byte `+0x18` is set, otherwise from its sample |
| `007F3430` | the timing of a meter record `+0x08`, or with its byte `+0x18` set the later of it and a given timing, rounded down to the sync grid (`007F2FA0`) |
| `007F31C0`, `007F3930`, `007F3DE0` | clear a timing record, clear a meter cursor, store a meter's three values |

`007F31F0` converts between seconds, samples and these units ([Sound engine](sound-engine.md)).

## Shipped data

Over the 116 `.mab` banks, each with one music:

| Field | Value in every music |
|---|---|
| header version | 11 |
| sections | 3 |
| modes | 1 |
| start methods | 0 |
| end methods | 0 |

So the three sections are the three music versions, the mode change has no other mode to go to, and with any shipped music
commands `0x27` and `0x28` fail their method checks.

## Modding notes

- A replacement `.mab` needs three sections, or a music version past its last section prints "Invalid section index"
  and keeps playing the old one.
- A section's sync type decides how far ahead a version change can land: the change waits for the next sync point at
  least 4.2 seconds away.

## Related

- [Music](music.md) - which track plays and the music version option.
- [Sound driver objects](sound-driver-objects.md) - the music pool and the posters.
- [Sound streaming](sound-streaming.md) - the streams a music bank reads.
- [Sound engine](sound-engine.md) - the time-unit converter.
