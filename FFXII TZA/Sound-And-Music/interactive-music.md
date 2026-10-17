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

A playing music is a `Magi::Music` (vtable `01CB5E38`), one of eight `8D8`<sub>h</sub>-byte objects
([Sound driver objects](sound-driver-objects.md)). It keeps its bank's music header at `+18`<sub>h</sub> and a state at `+C8`<sub>h</sub>:
1 once built, 2 while it waits for its data, and 7 when it has ended and the update pass frees it (`007B7D60`). Its
sample rate is at `+64C`<sub>h</sub> and its current section at `+638`<sub>h</sub>.

### The music header

A `.mab` bank's `musc` chunk holds one header per music, read through `MabFile` wrapper classes, each named by its
run-time type and built by one accessor:

| Class | Accessor | From |
|---|---|---|
| `Music` | `007D0550` | the `musc` chunk, by index |
| `Section` | `007D0600` | the music, by index below byte `+04`<sub>h</sub> |
| `Mode` | `007D0460` | the music, by index below byte `+05`<sub>h</sub> |
| `EndMethod`, `StartMethod` | `007D0180`, `007D0650` | the music; the start-method count is byte `+42`<sub>h</sub> |
| `ZeroOne` | `007D0710` | the music, by index below byte `+43`<sub>h</sub> |
| `Layer`, `Meter`, `CustomPointList`, `VolumeAutomation` | `007D03B0`, `007D0400`, `007D0120`, `007D06B0` | a section |
| `ModeParam`, `ModeTransitionParam` | `007D04C0`, `007D0510` | a mode; the transition records are `20`<sub>h</sub> bytes and skip the mode's own index |
| `MusicPoint` | `007D05D0` | `10`<sub>h</sub>-byte records |
| `Instrument`, `InstrumentChunk`, `InstrumentMaterial` | `007D01E0`, `007D0210`, `007D0380` | the `inst` chunk; materials are `20`<sub>h</sub>-byte records |

A header's offset table starts at its `u16` `+02`<sub>h</sub>, moved on by `(nameLength + 10h) & F0h`: the name length is
byte `+48`<sub>h</sub> of a music header from version 9 and byte `+04`<sub>h</sub> of a section header from version 8. `007CFFB0` and `007CFFE0` build and drop the `MabFile` wrapper. `007C30C0` refuses a music whose
section or mode headers are newer than the driver reads ("Music::CheckVersion failed").

### Commands

The game's calls post these commands ([Sound driver objects](sound-driver-objects.md)); the driver thread runs them
in `007AB5C0`:

| Type | Arm | Does |
|---:|---|---|
| `1C`<sub>h</sub> | `007C8370(music, section, ..., time)` | plays a section: only in state 1, fading `+190`<sub>h</sub> in to 1.0 over the time, starting at once when the data is in (`007C2280`, `007C36C0`) and otherwise setting state 2 |
| `1D`<sub>h</sub> | `007C9E70(music, section)` | moves to a section: `007C8B20` builds the transition and `007C4790` runs it; with no header yet it only stores the section at `+680`<sub>h</sub>; a bad index prints "Invalid section index" |
| `1E`<sub>h</sub> | `007C91B0` | stores a flag at `+5F6`<sub>h</sub> |
| `1F`<sub>h</sub> | `007C91D0` | ramps the value at `+340`<sub>h</sub> |
| `20`<sub>h</sub> | `007C91F0(music, layer, ...)` | ramps one of the eight layer volumes at `+3A0`<sub>h</sub>, `30`<sub>h</sub> bytes apart; a layer of 8 or more prints "SetLayerVolume index out of range" |
| `22`<sub>h</sub> | `007C1620(music, mode, value, time)` | starts a mode change: in a state below 2, in state 7 or with `+70C`<sub>h</sub> at 0 it prints "Not appropriate state for transition"; a bad mode index prints "Invalid mode index"; otherwise it clamps the value to 0-1, ramps `+710`<sub>h</sub> to 1.0 and sets `+70C`<sub>h</sub> to 5 |
| `23`<sub>h</sub> | `007C82D0(music, timing, ..., section)` | plays a section from a bar, beat and tick, with the same state rule as `1C`<sub>h</sub> |
| `24`<sub>h</sub> | `007C7120(music, section, timing)` | moves to a section at a timing: the sample of the timing (`007C65C0`), then `007C4790` |
| `25`<sub>h</sub> | `007C9FB0` | sets the next section and the timing to switch at; a timing past the end prints "SetNextSectionAndTiming timing is over EndTiming!!" |
| `26`<sub>h</sub> | `007CAB80(music, section, seconds)` | moves to the same timing in another section, as below |
| `27`<sub>h</sub> | `007CA7C0(music, method)` | starts by a start method below the count: a method of type 1 or 2 plays its section (`007C8370`), and type 3 calls `007C82D0` with the method's timing `+08`<sub>h</sub> and section `+06`<sub>h</sub>; an index past the count prints "Invalid method index", and any other type prints a message naming the type that ends "try stop.", and returns -1 without stopping anything |
| `28`<sub>h</sub> | `007C5760(music, method)` | ends by an end method; a method type it does not handle prints a message and stops the music |
| `29`<sub>h</sub>, `2A`<sub>h</sub> | `007C87E0`, `007CB320` | add an entry to, and remove one from, the list at `+8A8`<sub>h</sub> (`007DCB50` appends, `007DD220` removes) |
| `2B`<sub>h</sub> | `007C9C20` | queues the next music, or prints "Music::SetNextMusic can't find nextMusic" |

Commands that need the music's data print "musicData_ is not streamed yet." when it has not arrived. `007C6490` gives
the play position in seconds, or prints "Music::GetPlaySec Failed to get currentSample!".

### Moving to another section

`007CAB80(music, section, seconds)` is how a music changes version:

1. It takes the current section's sync type, byte `+20`<sub>h</sub> (from version 5; earlier ones add 3 when it is 2 or more),
   and finds the next sync point at least `seconds + 0.2` ahead (`007C1830`, "Music::SyncTo failed to CalcSampleDelay"
   when there is none).
2. It finds the same bar, beat and tick in the target section (`007C65C0`), moving it back so the change starts
   `seconds` before that point.
3. It starts the transition into the target section over `seconds` (`007C4790`).

`00222AD0` calls it with the new music version as the section and 4.0 seconds ([Music](music.md)); `002228A0` passes
the version as the section to `1C`<sub>h</sub> and `23`<sub>h</sub>.

### Building and freeing

`007B7460` creates a music in two steps:

1. `007C05C0` builds the object: one voice slot in each of the two layer sets (`+674`<sub>h</sub>, `+6F8`<sub>h</sub>), every volume,
   pitch and layer ramp at 1.0, a cleared meter cursor at `+604`<sub>h</sub> (`007F31C0`, `007F3930`), and an eight-node
   timing-callback list at `+8A8`<sub>h</sub> (`007C6EA0`, whose `30`<sub>h</sub>-byte nodes `007C8830` links into a free chain).
2. `007C6FB0` stores the creation values: the bank handles `+20`<sub>h</sub> and `+28`<sub>h</sub>, the header `+18`<sub>h</sub>, the music number
   `+B0`<sub>h</sub> and the callback object `+B8`<sub>h</sub> with its argument `+C0`<sub>h</sub>. It reads the sample rate into `+64C`<sub>h</sub>, refuses
   a header newer than the driver reads (`007C30C0`) and sets state 1.

`007C6770` gives the rate: header `+44`<sub>h</sub> from version 6, otherwise section 0's `+18`<sub>h</sub>. `007C6340` gives the music's
bank from its handle `+28`<sub>h</sub> (`007B2470`). When the update pass frees an ended music, `007C5980` gives back its stream
claims (`007E4720`, `007E4F70`), releases the bank (`007D0A00`), calls slot 2 of the callback object and frees the
callback nodes; `007C1100` then puts back the base vtables (slot 0, `007C15D0`).

### Loading

While the music waits for its data (states 2 to 4), `007CAF70` ("Music::TryLoad") runs on each pass:

1. It waits until the bank is a streaming bank that is ready (slots 1 and 4).
2. Without a header yet, it checks the `.mab` (`007D07A0`, "Music::TryLoad failed, mab file is not valid!") and the
   music number against the bank's count ("music number is out of range"), takes the header (`007D0550`) and the
   rate, and checks the version.
3. Unless a start method is pending at `+8A0`<sub>h</sub>, it finds the start point: seconds `+D8`<sub>h</sub> for seek type 0, or a
   timing for seek type 1 (`007C67B0`).
4. It claims a stream for every layer of the current section (`007C3570`), or prints "Music::TryLoad failed, can't
   find unused audio stream!" and fails, which ends the music.

`007C3570(music, section, seconds)` finds the stream already holding each layer's material (`007E3040`) or claims a
free one (`007E3270`) and requests the material from `seconds` minus the layer's start (`007E4310`). `007C67B0` gives
the seek timing in seconds (`007C65C0`), or prints "GetSeekTimingSec seekType_ is not SEEK_TYPE_TIMING.".

### Layer voices

A music plays each layer of a section as its own voice, in two sets: the current section's at `+30`<sub>h</sub> and the
entering or leaving section's at `+70`<sub>h</sub>, eight handles each. Two more voices sit at `+6F0`<sub>h</sub> and `+758`<sub>h</sub>.
`007C6B80(music, i)` gives voice `i` across all of them, in that order:

| Function | Does |
|---|---|
| `007C3230(music, section, handles, seconds)` | builds one voice per layer (`007B5D20`) from the stream (`007E3040`, `007E3150`) or the `mtrl` chunk (`007CF8B0`, `007CF860`); a failure stops the voices built so far |
| `007C3D60(music, section, handles, a, b)` | sets each live voice's start (`007EE450`) to the layer's start minus `a` seconds, less the stream's buffered start when streaming, plus `b` seconds; applies the panning (`007EDE90`) and plays it (`007EDA60`) |
| `007C8440(music, instrument, seconds, handle, material)` | builds and plays a voice for an instrument material of the `inst` chunk with the music's volume, pitch, filter and panning, paused when the music is; a failure prints "failed to create effect voice! materialIndex = %d" |
| `007C5AC0(music, out, section, handles)` | gives the section's current sample from its layer voices that report 2 (`007EBAB0`): a layer's start plus its voice's position (`007EBA40`), wrapped into the loop region when the section loops on itself; -1 when none plays |
| `007C5A70`, `007C68E0` | the current sample of the current set, and of the other set's section during a transition (`+63C`<sub>h</sub> in states 5 and 6, `+640`<sub>h</sub> in 7) |
| `007C7090` | answers whether any current layer voice reports 2 |
| `007CA440(music, sample, section, handles)` | passes `sample` minus the layer's start to the playing layer voice that holds it (`007EE430`), or -1 to every playing layer voice |
| `007C6960(music, instrument, material)` | an instrument material's length in seconds, `+0C`<sub>h</sub> over `+10`<sub>h</sub> |

A voice reports 2 while it plays or is paused. Two more functions keep a looping section whole:

- `007CC880` ("Music::UpdateNonLoopVoiceReplay"): when the section loops on itself, it rebuilds every non-looping layer
  (layer `+06`<sub>h</sub> 0) whose voice has ended and starts it at the loop position matching the current sample.
- `007CCDD0` ("Music::UpdateRemainingLoopCount"): while a change point is set (`+67C`<sub>h</sub>), it turns off looping
  (`007EA920`) on each looping layer voice whose material ends within that distance plus 128 frames.

### The update pass

The music pass `007B7D60` runs `007CB330(music, seconds)` on every music once per driver pass:

1. Below state 2, and in state 7, it does nothing.
2. In states 2 to 4 it tries to load (`007CAF70`; a failure sets state 7) and runs a pending start method
   (`007CA7C0`), until the current section's streams are full (`007C2280`); it then starts playing (`007C36C0`).
3. In state 5 it runs `007CC880`, `007CDC20`, `007CD350` and `007CD920` in that order, then `007CC4A0`, `007CBC40` and,
   during a reverb end, `007CD000`. With no next section (`+63C`<sub>h</sub>) and no meter end (`+608`<sub>h</sub>), it instead ends the
   music once no layer voice reports 2 (`007C7090`).
4. In state 6 it waits for the music's volume (slot 26) to reach 0, then stops every voice and sets state 7.
5. With pausing on (`+CC`<sub>h</sub> 1), it pauses every voice once the pause ramp `+1D0`<sub>h</sub> reaches 0 and sets `+CC`<sub>h</sub> to 2;
   while paused it stops here, except in state 6.
6. During a mode change it moves the mode ramp `+710`<sub>h</sub> on by the seconds times the music's pitch, at least 0.1, and
   blends the two modes (`007CC110`).
7. It reads the music's zero-one curves and moves its ramps on, handing each changed value to the voices (below).

`007C5650(music, seconds, curve)`, slot 2 through `007CA9E0`, stops a music: it ramps the volume `+190`<sub>h</sub> to 0 and sets
state 6, or with no time, or while paused, stops every voice and sets state 7.

### What the voices are given

The pass recomputes a value only when its ramp moved, and hands it to every voice through `007C6B80`:

| Value | From | Handed over by | Voice call |
|---|---|---|---|
| volume | slot 26: header `+28`<sub>h</sub> times the curved ramps `+150`<sub>h</sub>, `+190`<sub>h</sub> and `+1D0`<sub>h</sub> and the factors `+5B0`<sub>h</sub>-`+5B8`<sub>h</sub> | `007CE730` | `007EE500` |
| pitch | slot 27: the ramps `+310`<sub>h</sub> and `+340`<sub>h</sub> times the factors `+5DC`<sub>h</sub>-`+5E8`<sub>h</sub> | `007CCD20` | `007EE300` |
| granular pitch | `007C5DE0`: the ramp `+340`<sub>h</sub> times `+5E4`<sub>h</sub> | `007CBF70`, with `1/value` and `0.025 x value x` the meter's `+1C`<sub>h</sub> (120 without one) | `007EDB60` |
| low-pass | `007C5F70`: the ramp `+370`<sub>h</sub> times `+5EC`<sub>h</sub> and `+5F0`<sub>h</sub> | `007CC070` | `007EDD20` |
| filter reset | the flags `+5F4`<sub>h</sub> and `+5F5`<sub>h</sub> | `007CBEB0` | `007EA9C0` |
| pitch shifter on | the flags `+5F6`<sub>h</sub> and `+5F7`<sub>h</sub> | `007CBDD0` | `007EA850` |
| panning | slot 28 | `007CCC30` | `007EDE90` |
| sends | the end methods of type 3, or the send ramp `+840`<sub>h</sub> during a reverb end | `007CD110` | `007EE470` |

Granular pitch and the pitch shifter switch apply only when header byte `+0A`<sub>h</sub> has bit 0 set (`007CBF70`,
`007CBDD0`), and the ramp `+340`<sub>h</sub> joins the pitch only then (`007C6370`); no shipped music sets it
([Audio effects](audio-effects.md)). `007CE730` gives each layer voice the volume times its own factor: `007C5E60` for the current set (layer
ramp `+3A0h + 30h x i`, factor `+5BCh + 4 x i`, and the blend of the two modes' layer values) and `007C6A80` for
the other set.

Each set also has a volume-automation ramp, `+290`<sub>h</sub> and `+2D0`<sub>h</sub>. During a transition `007CE730` multiplies the
entering set by the fade-in `+210`<sub>h</sub> and the leaving set by the fade-out `+250`<sub>h</sub>, each times its section's volume
(section `+30`<sub>h</sub> from version 8, `+40`<sub>h</sub> from version 6, otherwise 1.0).

`007C5C90` gives a zero-one curve its input by name: "zeroone_slot0" and "zeroone_slot1" read the ramps at `+F0`<sub>h</sub> and
`+120`<sub>h</sub>, and any other name an external parameter (`007B0E90`). The curve's kind byte `+06`<sub>h</sub> decides where the mapped
value goes (`007CFD00`): 1 the volume factor `+5B8`<sub>h</sub>, 2 the pitch factor `+5E8`<sub>h</sub>, 4 a layer's factor
`+5BCh + 4 x layer`, and 5 the low-pass factor `+5F0`<sub>h</sub>.

### Modes

A mode gives eight layer volumes and four more values. `007C8A00` fills a `34`<sub>h</sub>-byte block from a mode record: `+10`<sub>h</sub>,
`+14`<sub>h</sub> (a pitch, as `2^(x/12)` when bit 1 of byte `+01`<sub>h</sub> is set), `+18`<sub>h</sub>, `+1C`<sub>h</sub> (1.0 for a version-0 record),
two flags from bits 0 and 2 of byte `+01`<sub>h</sub>, and the eight layer values from the record's `ModeParam` for the section
(`007D04C0`). `007C6E10` resets a block: layer 0 at 1.0, the other layers 0, the four values 1.0 and both flags clear.

`007C8E60` fills a block between two modes at a blend `t`, and `007C8CE0` blends two blocks the same way. Values mix
linearly; a flag the target sets is on once `t` is above 0, a flag the target clears is off once `t` reaches 1, and
before that each keeps the start's value.

`007C8010(music, t)` keeps the present blend as the new start blocks (`+760`<sub>h</sub>, `+7C8`<sub>h</sub>) and builds the target blocks
(`+794`<sub>h</sub>, `+7FC`<sub>h</sub>) between mode `+700`<sub>h</sub> and mode `+704`<sub>h</sub> at `t`; with no other section both of its blocks are reset. `007CC110` blends the from and to blocks by the mode ramp into the music's factors
(`+5B4`<sub>h</sub>, `+5E0`<sub>h</sub>, `+5E4`<sub>h</sub>, `+5EC`<sub>h</sub>, the flags `+5F5`<sub>h</sub> and `+5F7`<sub>h</sub>) and marks them changed. When the change is
done (mode state `+70C`<sub>h</sub> 4), `007C7BE0` makes `+704`<sub>h</sub> the current mode, resets the ramp, hands every value to the
voices and sets the mode state to 1.

### Transition states

A music's transition state `+650`<sub>h</sub> drives section changes and the change to a next music. `007C72A0(music, state)`
sets it and acts on entering some states; `007CDC20` ("Music::UpdateTransition") works each one on every pass:

| State | On entering (`007C72A0`) | Each pass (`007CDC20`) |
|---:|---|---|
| `1` | | moves to 2 once a meter is in use (`+648`<sub>h</sub>) |
| `2` | starts a queued next music (`+830`<sub>h</sub>, `007C43F0`), the stored request (`+6A8`<sub>h</sub>; `007C4790`, or `007CAB80` with `+6AE`<sub>h</sub> set), or the section's own next section | |
| `3` | | stops the other set's playing voices, and moves to 2 when none are left |
| `4` | | claims the target section's (`+644`<sub>h</sub>) streams and moves to 2 once all, and a requested instrument's, are full |
| `5` | | refreshes the loop counts (`007CCDD0`) and moves to 6 at the change sample `+6B8`<sub>h</sub> |
| `6` | resets the fade-out and, with a fade-in time `+6C0`<sub>h</sub>, ramps the fade-in `+210`<sub>h</sub> to 1.0 | starts the fade-out `+250`<sub>h</sub> past its start point and moves to 7 at `+6BC`<sub>h</sub> |
| `7` | swaps the two sets with their counts and mode blocks (`007CC110`), then finishes the change (`007C7CD0`) | once the fade-out is at 0, the extra voice has ended and the fade-in is full, stops the old set and moves to 3 |
| `8` | | loads the next music (`007CAF70`) and plays it when ready (`007C43F0`), or drops it and moves to 2 |
| `9` | resets the fade-out | fades this music out from the start point and ends it (state 7) at 0 |

Case 7 prints "Music::UpdateTransition (TRANSITION_STATE_POST_ENTRY) Failed to get currentSample!" when no voice
plays. In states 5 to 7 `007CDC20` also keeps the change points inside the loop region and moves the other set's
volume automation (`007C6D00`, ramp `+2D0`<sub>h</sub>).

`007C7CD0` finishes a section change: the current section becomes the previous (`+640`<sub>h</sub>), the next becomes current,
and the next is the request's target or the new section's own next (byte `+22`<sub>h</sub>). It then reloads the meter and the
bar, beat and tick (`007C5FE0`, `007C6090`, `007F3800`), moves a running mode change's end point (`007CA440`,
`007C7BE0`), and tells the callback object (slot 3).

### Requests

`007C23C0` ("SetNextSection") checks a request and stores it at `+680`<sub>h</sub> (target `+680`<sub>h</sub>, sync type `+684`<sub>h</sub>,
timing `+6AA`<sub>h</sub>):

- Below state 2, in state 7, or with no next section (`+63C`<sub>h</sub>) and no meter end (`+608`<sub>h</sub>), it prints "Not appropriate state for
  transition. state_ = %d"; a bad target prints "Invalid section index = %d".
- In states 2 and 4 it only stores the request.
- Sync types 12 to 19 are the section's custom points 0 to 7: "Invalid custom point index = %d, numCustomPoints = %d"
  or "There is no custom points! index = %d" refuse a missing one.
- A request for the current section with no timing cancels a pending change; during state 5 it stops the entering
  set, turns looping back on for the current layers (`007EA920`) and returns to state 3.
- Transition state 0 prints "Transition state is invalid!", and states 8 and 9 print "SetNextSection canceled!
  Transitioning to next music...".

`007C2A60` ("Music::CheckTransitionTime") works out how long until a request lands: the time to the next sync point of
its type (`007C1830`), or to its own bar, beat and tick in the current section (`007C65C0`); when that has passed it
warns "Failed to sync to (%d,%d,%d)" and takes the sync point. It is at least the length of the target's transition instrument (section `+1C`<sub>h</sub>,
`007C6960`) when the request asks for one. With no time left it warns "Transition failed because there remains no time
for transition. keep playing" and drops the request.

`007C43F0(music, next)` hands over to a next music. In states 1, 3, 6 and 7 it does nothing; when the next music's streams
are not ready it sets state 8;
otherwise it plays it at this music's next sync point (`007C1830`, `007C36C0`; "NextMusic CorePlay failed!!" on
failure), takes the fade values from the current section and sets state 9.

### Reverb end

`007C4030(music, send, seconds, fade)`, from the end command (`007C5760`), ends a music by raising one of its sends:

1. It needs the header ("musicData_ is not streamed yet."), a send from 1 to the header's count `+40`<sub>h</sub> ("Invalid
   sendIndex = %d") and no reverb end already running ("Already executing reverb end!").
2. It finds the next sync point at least `seconds` ahead (`007C1830`; "Music::ReverbEnd failed to CalcSampleDelay").
3. It stores the send `+838`<sub>h</sub>, the time `+880`<sub>h</sub>, the fade `+884`<sub>h</sub> and the point `+87C`<sub>h</sub>, sets `+898`<sub>h</sub> and drops
   any pending request.

On each pass `007CD000` waits for the point, ramps the send `+840`<sub>h</sub> to 1.0 over the time with the curve `+894`<sub>h</sub>, and
once it is full stops the music over the fade (slot 2).

### Bar, beat and tick

A timing is a bar (`i16`), a beat (`i8`) and a tick (`i8`); a meter gives the ticks per bar (`+20`<sub>h</sub>) and per beat
(`+21`<sub>h</sub>). Every helper works on the total tick count and splits it back:

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
| `007F2FA0`, `007F3080` | round a timing (bar `+0`, beat `+2`, tick `+3`) down to the grid of a sync type, and step it by one grid unit: 3 two ticks, 4 three ticks, 5 a beat, 6 two beats, 7 a bar, 8 two bars, 9 four bars, 10 eight bars, and for the step only 2 one tick; rounding clears the smaller units, and a step carries into the next beat at `+21`<sub>h</sub> ticks and into the next bar at `+20`<sub>h</sub> |
| `007F3570` | the sample of a timing: with `d` = timing − start timing `+08`<sub>h</sub> (`007F3140`), `[+00h] + d.bar x [+2Ch] + d.beat x [+28h] + d.tick x [+24h]`, or `[+04h]` at the end timing `+0C`<sub>h</sub>; a timing before the start or past the end is clamped with a warning ("GetSampleFromTiming timing is before startTiming"), and with byte `+18`<sub>h</sub> clear it logs "Invalid Timing!" and returns `[+00h]` (`007F3570`-`007F37FE`) |
| `007F3800` | the timing of a sample, through `007F2EA0`; "GetTimingFromSample Invalid Timing!" outside the music |
| `007F3510` | the sample of a custom point: from its timing (`007F3570`) when its byte `+18`<sub>h</sub> is set, otherwise from its sample |
| `007F3430` | the timing of a meter record `+08`<sub>h</sub>, or with its byte `+18`<sub>h</sub> set the later of it and a given timing, rounded down to the sync grid (`007F2FA0`) |
| `007F31C0`, `007F3930`, `007F3DE0` | clear a timing record, clear a meter cursor, store a meter's three values |

`007F31F0` converts between seconds, samples and these units ([Sound engine](sound-engine.md)).

### Following the play position

`007CD350` ("Music::UpdateTiming") keeps the music's position on each pass:

1. It keeps last pass's timings (`+65C`<sub>h</sub>, `+660`<sub>h</sub>) and reads the current sample `+664`<sub>h</sub> from the current set
   (`007C5AC0`). With no voice playing and no change to another section under way (transition state 5 or above), it
   stops every voice and sets state 7.
2. A sample below the last one means the section looped, and `007C7950` runs.
3. While the sample is past the meter's end `+608`<sub>h</sub>, it moves to the next meter (`007C6090`), or prints "Next meter
   not found. currentSample = %d" when none is left.
4. At the section's exit point (section `+0C`<sub>h</sub>) with no next section, or in state 9, it sets the timing to the
   section's end timing `+2C`<sub>h</sub> rounded up to a bar (`007F2F10`). During a change to another section it waits, and
   otherwise it logs "Music::UpdateTiming exceeded exitPoint".
5. When the meter carries counts (`+61C`<sub>h</sub>), it turns the sample into a bar, beat and tick at `+654`<sub>h</sub> (`007F3800`),
   with a copy at `+658`<sub>h</sub> moved one tick on when the sample is past half a tick (`007F2F30`).

`007C7950` handles a loop: it wraps the pending change points (`+67C`<sub>h</sub>, the mode change's `+740`<sub>h</sub>, the reverb end's
`+87C`<sub>h</sub>) into the section's loop region, finishes or re-marks a mode change, restarts the volume automation at the
current point (`007C6D00`, ramp `+290`<sub>h</sub>), counts the loop at `+670`<sub>h</sub> and reloads the meter (`007C6090`).

| Function | Gives |
|---|---|
| `007C61A0` | a section's meter count: byte `+04`<sub>h</sub> before version 8, `u16` `+18`<sub>h</sub> from version 8 |
| `007C5FE0(section, sample)` | the index of the meter holding `sample`, by each meter's start `+0C`<sub>h</sub> |
| `007C6090(music, cursor, section, meter)` | loads a meter into a cursor (`007F3950`), or clears it and prints "Invalid section index:%d" |
| `007C61C0` | a section's volume-automation point count: `u16` `+1E`<sub>h</sub> from version 10, otherwise 0 |
| `007C6D00(music, sample, section)` | the index of the last automation point that starts before `sample`, or -1 |

### Timing callbacks

A music tells its callback object (`+B8`<sub>h</sub>) when the music reaches a timing it asked for. Commands `29`<sub>h</sub> and `2A`<sub>h</sub>
add and remove the requests in the eight-node list `+8A8`<sub>h</sub>. `007CD920`, on each pass, walks the list while the
callback object exists:

- A request of kind 0 looks at the bar, beat and tick `+654`<sub>h</sub>, kind 1 at the rounded copy `+658`<sub>h</sub>, and only when it
  changed since the last pass.
- A sync type of 1 to 11 fires when the timing sits on that grid (`007F2FA0` leaves it unchanged).
- A sync type of 12 to 19 fires when the timing equals one of that custom point list's points (`007D0120`, `007D05D0`).

A request that fires calls slot 4 of the callback object with the timing and the request's two values.

### Instruments

A `Magi::Instrument` plays one instrument of a music's `inst` chunk in time with that music; the run-time type data
names it in its list type, `FixedList<4, Magi::Instrument*>`. The pool holds 32 ([Sound driver objects](sound-driver-objects.md)),
and each keeps its voice at `+40`<sub>h</sub> and a state at `+58`<sub>h</sub>:

| Function | Does |
|---|---|
| `007CEF60(instrument, music, sync, semitones, fade)` | command `2C`<sub>h</sub>: only in state 1; stores the music and the sync type `+28`<sub>h</sub>, starts the volume ramp `+B8`<sub>h</sub> over the fade, sets the pitch `2^(semitones/12)` at `+200`<sub>h</sub>, and starts it (`007CEAB0`) |
| `007CEF10` | command `2D`<sub>h</sub>: turns off the voice's loop when it has one (`007EBA90`, `007EA920`), so it ends with its material |
| `007CEAB0` | adds it to the category its record's byte `+06`<sub>h</sub> names (`007A9A10`): an answer of 1 sets state 7 and 2 sets state 3; while paused it sets state 4; otherwise it plays it (`007CEB80`), sets state 5 and calls slot 1 of the callback object |
| `007CEB80` | picks the material: for kind 4 (record byte `+04`<sub>h</sub>) material 1 when the music's next sync point is not on a bar line, otherwise 0; for kind 3 the value `+74`<sub>h</sub> times 100; for other kinds 0. It then plays it from the music's next sync point (`007C1830`) with its own volume, pitch, filter flag, low-pass and panning |
| `007CF010(instrument, seconds)` | the pass (`007B82D0`): in state 5 it sets 7 once the voice has gone or ended; in states 2 to 4 it retries the start; in state 6 it stops the voice once the volume ramp `+B8`<sub>h</sub> is at 0; then it pauses like a music and hands changed values to the voice |
| `007CEE30` | on free: releases the bank and calls slot 2 of the callback object |
| `007CEEE0` | gives the instrument's bank (`+38`<sub>h</sub>); `007B8230`, from `007D0A20` and `007D0A70`, uses it to stop every instrument of one bank |

The handovers are `007CF4F0` (volume, slot 26, `007EE500`), `007CF4A0` (pitch, slot 27, `007EE300`), `007CF410`
(panning, slot 28, `007EDE90`) and `007CF370` (low-pass ramp `+140`<sub>h</sub>, `007EDD20`); the filter flag `+204`<sub>h</sub> goes to
`007EA9C0`.

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
commands `27`<sub>h</sub> and `28`<sub>h</sub> fail their method checks.

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
- [Audio effects](audio-effects.md) - the pitch shifter and filters the music's voices carry.
