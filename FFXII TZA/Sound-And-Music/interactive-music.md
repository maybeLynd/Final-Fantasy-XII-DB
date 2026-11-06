---
title: "Interactive music: the driver's music object, its sections, modes and layers, the commands that start, switch and end it, and its bar-beat-tick timing"
kind: "system"
category: "Sound and music"
addresses: "0x007C82D0, 0x007CAB80, 0x007C1620, 0x007C9E70, 0x007C91F0, 0x007CA7C0, 0x007C5760, 0x007F3570"
---

## What the player sees

- Switching the music version in the Config menu keeps the track playing from the same point in the new version,
  with a short crossfade.
- Every track can start from a chosen bar.

## How it works

### The music object

A playing music is a `Magi::Music` (vtable `0x01CB5E38`), one of eight `0x8D8`-byte objects
([Sound driver objects](sound-driver-objects.md)). It keeps its bank's music header at `+0x18` and a state at `+0xC8`:
1 once built, 2 while it waits for its data, and 7 when it has ended and the update pass frees it (`0x007B7D60`). Its
sample rate is at `+0x64C` and its current section at `+0x638`.

### The music header

A `.mab` bank's `musc` chunk holds one header per music, read through `MabFile` wrapper classes, each named by its
run-time type and built by one accessor:

| Class | Accessor | From |
|---|---|---|
| `Music` | `0x007D0550` | the `musc` chunk, by index |
| `Section` | `0x007D0600` | the music, by index below byte `+0x04` |
| `Mode` | `0x007D0460` | the music, by index below byte `+0x05` |
| `EndMethod`, `StartMethod` | `0x007D0180`, `0x007D0650` | the music; the start-method count is byte `+0x42` |
| `ZeroOne` | `0x007D0710` | the music, by index below byte `+0x43` |
| `Layer`, `Meter`, `CustomPointList`, `VolumeAutomation` | `0x007D03B0`, `0x007D0400`, `0x007D0120`, `0x007D06B0` | a section |
| `ModeParam`, `ModeTransitionParam` | `0x007D04C0`, `0x007D0510` | a mode; the transition records are `0x20` bytes and skip the mode's own index |
| `MusicPoint` | `0x007D05D0` | `0x10`-byte records |
| `Instrument`, `InstrumentChunk`, `InstrumentMaterial` | `0x007D01E0`, `0x007D0210`, `0x007D0380` | the `inst` chunk; materials are `0x20`-byte records |

A header's offset table starts at its `u16` `+0x02`, moved on by `(nameLength + 0x10) & 0xF0`: the name length is
byte `+0x48` of a music header from version 9 and byte `+0x04` of a section header from version 8. `0x007CFFB0` and `0x007CFFE0` build and drop the `MabFile` wrapper. `0x007C30C0` refuses a music whose
section or mode headers are newer than the driver reads ("Music::CheckVersion failed").

### Commands

The game's calls post these commands ([Sound driver objects](sound-driver-objects.md)); the driver thread runs them
in `0x007AB5C0`:

| Type | Arm | Does |
|---:|---|---|
| `0x1C` | `0x007C8370(music, section, ..., time)` | plays a section: only in state 1, fading `+0x190` in to 1.0 over the time, starting at once when the data is in (`0x007C2280`, `0x007C36C0`) and otherwise setting state 2 |
| `0x1D` | `0x007C9E70(music, section)` | moves to a section: `0x007C8B20` builds the transition and `0x007C4790` runs it, and its result is returned; the request carries no timing (`0x007C9F12`) and the current section's sync type, byte `+0x20`, with 3 added to a type of 2 or more before section version 5, as for `0x26` (`0x007C9EF3`-`0x007C9F0D`); with no header yet it only stores the section at `+0x680` and returns 0 (`0x007C9E9D`); a bad index, below 0 or not below header byte `+0x04`, prints "Invalid section index" and returns -1 (`0x007C9EC4`-`0x007C9F98`) |
| `0x1E` | `0x007C91B0` | stores a flag at `+0x5F6` |
| `0x1F` | `0x007C91D0` | ramps the value at `+0x340` |
| `0x20` | `0x007C91F0(music, layer, value, time)` | ramps one of the eight layer volumes at `+0x3A0`, `0x30` bytes apart, to the value over the time (`0x007CA560`, `0x007C9231`) and returns 0; a layer of 8 or more prints "SetLayerVolume index out of range", as does a negative layer through the same unsigned test (`0x007C920F`), and returns -1 (`0x007C92A8`) |
| `0x22` | `0x007C1620(music, mode, value, time)` | starts a mode change: in states 2 and 4 it returns -1 without a message (`0x007C165E`-`0x007C1667`); in a state below 2, in state 7 or with `+0x70C` at 0 it prints "Not appropriate state for transition"; a bad mode index, below 0 or not below header byte `+0x05` (`0x007C168F`-`0x007C16A1`), prints "Invalid mode index"; both messages return -1. Otherwise, when the mode state `+0x70C` is 4, it first hands -1 to every playing layer voice of the current section (`0x007CA440`, `0x007C16D2`); it stores the mode at `+0x704`, clamps the value to 0-1 into `+0x708` (`v < 0` gives 0, `v >= 1` gives 1.0; `0x007C16E2`-`0x007C1700`), sets `+0x740` to -1, builds the blend blocks (`0x007C8010`, `0x007C1715`), ramps `+0x710` to 1.0 over the time (`0x007CA560`, `0x007C1735`), sets `+0x70C` to 5 and returns 0 |
| `0x23` | `0x007C82D0(music, timing, value, section, mode)` | plays a section from a bar, beat and tick, with the same state rule as `0x1C`: outside state 1 it returns -1 (`0x007C82E0`). It stores the section at `+0x638`, seek type 1 at `+0xD4`, the timing at `+0xD8`-`+0xDB`, the value at `+0xDC`, the mode at both `+0x700` and `+0x704`, and 0 at `+0x708` (`0x007C82EB`-`0x007C8332`); unlike `0x1C` it leaves the volume ramp `+0x190` alone. With the data in it starts at once (`0x007C2280`, `0x007C36C0`), otherwise it sets state 2 and returns 0 |
| `0x24` | `0x007C7120(music, section, timing)` | moves to a section at a timing: the sample of the timing (`0x007C65C0`), then `0x007C4790` |
| `0x25` | `0x007C9FB0` | sets the next section and the timing to switch at; a timing past the end prints "SetNextSectionAndTiming timing is over EndTiming!!" |
| `0x26` | `0x007CAB80(music, section, seconds)` | moves to the same timing in another section, as below |
| `0x27` | `0x007CA7C0(music, method)` | starts by a start method below the count: a method of type 1 or 2 plays its section (`0x007C8370`), and type 3 calls `0x007C82D0` with the method's timing `+0x08` and section `+0x06`; an index past the count prints "Invalid method index", and any other type prints a message naming the type that ends "try stop.", and returns -1 without stopping anything. Outside states 1 and 2 it returns -1 at once (`0x007CA7E4`-`0x007CA7E9`); with no header yet it stores the method at `+0x8A0`, sets state 2 and returns 0 (`0x007CA7F6`-`0x007CA7FE`). The count is header byte `+0x42` from header version 7, and 0 before (`0x007CA81D`-`0x007CA828`); a negative index also prints "Invalid method index" (`0x007CA80F`). A valid index sets state 1 first (`0x007CA837`). Every type hands over the method's mode, byte `+0x07`: type 1 plays from 0 seconds with no fade time (`0x007CA94D`-`0x007CA963`), type 2 from the seconds `+0x08` with the fade time `+0x0C` (`0x007CA901`-`0x007CA92F`), and type 3 passes `+0x0C` as the value of `0x007C82D0` (`0x007CA8C0`-`0x007CA8FA`); the callee's result is returned |
| `0x28` | `0x007C5760(music, method)` | ends by an end method; a method type it does not handle prints a message and stops the music. With no header it prints "musicData_ is not streamed yet." and returns -1 (`0x007C5783`); an index below 0 or not below the count, header byte `+0x41` from header version 5 and 0 before, prints "Invalid method index" and returns -1 (`0x007C57FA`-`0x007C581C`). Type 1 stops the music (`0x007C5650`) over the seconds `+0x10` with the curve byte `+0x14`; type 2 moves to the section byte `+0x10` (`0x007C9E70`); type 3 starts a reverb end (`0x007C4030`) with the send `+0x18`, the seconds `+0x10` and the fade `+0x14`; each returns its callee's result. Any other type prints a message naming the type that ends "try stop.", stops the music at once through slot 2 with no time (`0x007C58B8`-`0x007C58C5`) and returns -1 |
| `0x29`, `0x2A` | `0x007C87E0`, `0x007CB320` | add an entry to, and remove one from, the list at `+0x8A8` (`0x007DCB50` appends, `0x007DD220` removes) |
| `0x2B` | `0x007C9C20` | queues the next music, or prints "Music::SetNextMusic can't find nextMusic" |

Commands that need the music's data print "musicData_ is not streamed yet." when it has not arrived. `0x007C6490` gives
the play position in seconds, or prints "Music::GetPlaySec Failed to get currentSample!".

### Moving to another section

`0x007CAB80(music, section, seconds)` is how a music changes version:

1. It takes the current section's sync type, byte `+0x20` (from version 5; earlier ones add 3 when it is 2 or more),
   and finds the next sync point at least `seconds + 0.2` ahead (`0x007C1830`, "Music::SyncTo failed to CalcSampleDelay"
   when there is no sync point).
2. It finds the same bar, beat and tick in the target section (`0x007C65C0`), moving it back so the change starts
   `seconds` before that point.
3. It starts the transition into the target section over `seconds` (`0x007C4790`).

`0x00222AD0` calls it with the new music version as the section and 4.0 seconds ([Music](music.md)); `0x002228A0` passes
the version as the section to `0x1C` and `0x23`.

### Building and freeing

`0x007B7460` creates a music in two steps:

1. `0x007C05C0` builds the object: one voice slot in each of the two layer sets (`+0x674`, `+0x6F8`), every volume,
   pitch and layer ramp at 1.0, a cleared meter cursor at `+0x604` (`0x007F31C0`, `0x007F3930`), and an eight-node
   timing-callback list at `+0x8A8` (`0x007C6EA0`, whose `0x30`-byte nodes `0x007C8830` links into a free chain).
2. `0x007C6FB0` stores the creation values: the bank handles `+0x20` and `+0x28`, the header `+0x18`, the music number
   `+0xB0` and the callback object `+0xB8` with its argument `+0xC0`. It reads the sample rate into `+0x64C`, refuses
   a header newer than the driver reads (`0x007C30C0`) and sets state 1.

`0x007C6770` gives the rate: header `+0x44` from version 6, otherwise section 0's `+0x18`. `0x007C6340` gives the music's
bank from its handle `+0x28` (`0x007B2470`). When the update pass frees an ended music, `0x007C5980` gives back its stream
claims (`0x007E4720`, `0x007E4F70`), releases the bank (`0x007D0A00`), calls slot 2 of the callback object and frees the
callback nodes; `0x007C1100` then puts back the base vtables (slot 0, `0x007C15D0`).

### Loading

While the music waits for its data (states 2 to 4), `0x007CAF70` ("Music::TryLoad") runs on each pass:

1. It waits until the bank is a streaming bank that is ready (slots 1 and 4).
2. Without a header yet, it checks the `.mab` (`0x007D07A0`, "Music::TryLoad failed, mab file is not valid!") and the
   music number against the bank's count ("music number is out of range"), takes the header (`0x007D0550`) and the
   rate, and checks the version.
3. Unless a start method is pending at `+0x8A0`, it finds the start point: seconds `+0xD8` for seek type 0, or a
   timing for seek type 1 (`0x007C67B0`).
4. It claims a stream for every layer of the current section (`0x007C3570`), or prints "Music::TryLoad failed, can't
   find unused audio stream!" and fails, which ends the music.

`0x007C3570(music, section, seconds)` finds the stream already holding each layer's material (`0x007E3040`) or claims a
free one (`0x007E3270`) and requests the material from `seconds` minus the layer's start (`0x007E4310`). `0x007C67B0` gives
the seek timing in seconds (`0x007C65C0`), or prints "GetSeekTimingSec seekType_ is not SEEK_TYPE_TIMING.".

### Layer voices

A music plays each layer of a section as its own voice, in two sets: the current section's at `+0x30` and the
entering or leaving section's at `+0x70`, eight handles each. Two more voices sit at `+0x6F0` and `+0x758`.
`0x007C6B80(music, i)` gives voice `i` across all of them, in that order:

| Function | Does |
|---|---|
| `0x007C3230(music, section, handles, seconds)` | builds one voice per layer (`0x007B5D20`) from the stream (`0x007E3040`, `0x007E3150`) or the `mtrl` chunk (`0x007CF8B0`, `0x007CF860`); a failure stops the voices built so far |
| `0x007C3D60(music, section, handles, a, b)` | sets each live voice's start (`0x007EE450`) to the layer's start minus `a` seconds, less the stream's buffered start when streaming, plus `b` seconds; applies the panning (`0x007EDE90`) and plays it (`0x007EDA60`) |
| `0x007C8440(music, instrument, seconds, handle, material)` | builds and plays a voice for an instrument material of the `inst` chunk with the music's volume, pitch, filter and panning, paused when the music is; a failure prints "failed to create effect voice! materialIndex = %d" |
| `0x007C5AC0(music, out, section, handles)` | gives the section's current sample from its layer voices that report 2 (`0x007EBAB0`): a layer's start plus its voice's position (`0x007EBA40`), wrapped into the loop region when the section loops on itself; -1 when no layer voice plays |
| `0x007C5A70`, `0x007C68E0` | the current sample of the current set, and of the other set's section during a transition (`+0x63C` in states 5 and 6, `+0x640` in 7) |
| `0x007C7090` | answers whether any current layer voice reports 2 |
| `0x007CA440(music, sample, section, handles)` | passes `sample` minus the layer's start to the playing layer voice that holds it (`0x007EE430`), or -1 to every playing layer voice |
| `0x007C6960(music, instrument, material)` | an instrument material's length in seconds, `+0x0C` over `+0x10` |

A voice reports 2 while it plays or is paused. Two more functions keep a looping section whole:

- `0x007CC880` ("Music::UpdateNonLoopVoiceReplay"): when the section loops on itself, it rebuilds every non-looping layer
  (layer `+0x06` 0) whose voice has ended and starts it at the loop position matching the current sample.
- `0x007CCDD0` ("Music::UpdateRemainingLoopCount"): while a change point is set (`+0x67C`), it turns off looping
  (`0x007EA920`) on each looping layer voice whose material ends within that distance plus 128 frames.

### The update pass

The music pass `0x007B7D60` runs `0x007CB330(music, seconds)` on every music once per driver pass:

1. Below state 2, and in state 7, it does nothing.
2. In states 2 to 4 it tries to load (`0x007CAF70`; a failure sets state 7) and runs a pending start method
   (`0x007CA7C0`), until the current section's streams are full (`0x007C2280`); it then starts playing (`0x007C36C0`).
3. In state 5 it runs `0x007CC880`, `0x007CDC20`, `0x007CD350` and `0x007CD920` in that order, then `0x007CC4A0`, `0x007CBC40` and,
   during a reverb end, `0x007CD000`. With no next section (`+0x63C`) and no meter end (`+0x608`), it instead ends the
   music once no layer voice reports 2 (`0x007C7090`).
4. In state 6 it waits for the music's volume (slot 26) to reach 0, then stops every voice and sets state 7.
5. With pausing on (`+0xCC` 1), it pauses every voice once the pause ramp `+0x1D0` reaches 0 and sets `+0xCC` to 2;
   while paused it stops here, except in state 6.
6. During a mode change it moves the mode ramp `+0x710` on by the seconds times the music's pitch, at least 0.1, and
   blends the two modes (`0x007CC110`).
7. It reads the music's zero-one curves and moves its ramps on, handing each changed value to the voices (below).

`0x007C5650(music, seconds, curve)`, slot 2 through `0x007CA9E0`, stops a music: it ramps the volume `+0x190` to 0 and sets
state 6, or with no time, or while paused, stops every voice and sets state 7.

### What the voices are given

The pass recomputes a value only when its ramp moved, and hands it to every voice through `0x007C6B80`:

| Value | From | Handed over by | Voice call |
|---|---|---|---|
| volume | slot 26: header `+0x28` times the curved ramps `+0x150`, `+0x190` and `+0x1D0` and the factors `+0x5B0`-`+0x5B8` | `0x007CE730` | `0x007EE500` |
| pitch | slot 27: the ramps `+0x310` and `+0x340` times the factors `+0x5DC`-`+0x5E8` | `0x007CCD20` | `0x007EE300` |
| granular pitch | `0x007C5DE0`: the ramp `+0x340` times `+0x5E4` | `0x007CBF70`, with `1/value` and `0.025 x value x` the meter's `+0x1C` (120 without one) | `0x007EDB60` |
| low-pass | `0x007C5F70`: the ramp `+0x370` times `+0x5EC` and `+0x5F0` | `0x007CC070` | `0x007EDD20` |
| filter reset | the flags `+0x5F4` and `+0x5F5` | `0x007CBEB0` | `0x007EA9C0` |
| pitch shifter on | the flags `+0x5F6` and `+0x5F7` | `0x007CBDD0` | `0x007EA850` |
| panning | slot 28 | `0x007CCC30` | `0x007EDE90` |
| sends | the end methods of type 3, or the send ramp `+0x840` during a reverb end | `0x007CD110` | `0x007EE470` |

Granular pitch and the pitch shifter switch apply only when header byte `+0x0A` has bit `0x1` set (`0x007CBF70`,
`0x007CBDD0`), and the ramp `+0x340` joins the pitch only then (`0x007C6370`); no shipped music sets it
([Audio effects](audio-effects.md)). `0x007CE730` gives each layer voice the volume times its own factor: `0x007C5E60` for the current set (layer
ramp `+0x3A0 + 0x30 x i`, factor `+0x5BC + 4 x i`, and the blend of the two modes' layer values) and `0x007C6A80` for
the other set.

Each set also has a volume-automation ramp, `+0x290` and `+0x2D0`. During a transition `0x007CE730` multiplies the
entering set by the fade-in `+0x210` and the leaving set by the fade-out `+0x250`, each times its section's volume
(section `+0x30` from version 8, `+0x40` from version 6, otherwise 1.0).

`0x007C5C90` gives a zero-one curve its input by name: "zeroone_slot0" and "zeroone_slot1" read the ramps at `+0xF0` and
`+0x120`, and any other name an external parameter (`0x007B0E90`). The curve's kind byte `+0x06` decides where the mapped
value goes (`0x007CFD00`): 1 the volume factor `+0x5B8`, 2 the pitch factor `+0x5E8`, 4 a layer's factor
`+0x5BC + 4 x layer`, and 5 the low-pass factor `+0x5F0`.

### Modes

A mode gives eight layer volumes and four more values. `0x007C8A00` fills a `0x34`-byte block from a mode record: `+0x10`,
`+0x14` (a pitch, as `2^(x/12)` when bit `0x2` of byte `+0x01` is set), `+0x18`, `+0x1C` (1.0 for a version-0 record),
two flags from bits `0x1` and `0x4` of byte `+0x01`, and the eight layer values from the record's `ModeParam` for the section
(`0x007D04C0`). `0x007C6E10` resets a block: layer 0 at 1.0, the other layers 0, the four values 1.0 and both flags clear.

`0x007C8E60` fills a block between two modes at a blend `t`, and `0x007C8CE0` blends two blocks the same way. Values mix
linearly; a flag the target sets is on once `t` is above 0, a flag the target clears is off once `t` reaches 1, and
before that each keeps the start's value.

`0x007C8010(music, t)` keeps the present blend as the new start blocks (`+0x760`, `+0x7C8`) and builds the target blocks
(`+0x794`, `+0x7FC`) between mode `+0x700` and mode `+0x704` at `t`; with no other section both of its blocks are reset. `0x007CC110` blends the from and to blocks by the mode ramp into the music's factors
(`+0x5B4`, `+0x5E0`, `+0x5E4`, `+0x5EC`, the flags `+0x5F5` and `+0x5F7`) and marks them changed. When the change is
done (mode state `+0x70C` 4), `0x007C7BE0` makes `+0x704` the current mode, resets the ramp, hands every value to the
voices and sets the mode state to 1.

### Transition states

A music's transition state `+0x650` drives section changes and the change to a next music. `0x007C72A0(music, state)`
sets it and acts on entering some states; `0x007CDC20` ("Music::UpdateTransition") works each one on every pass:

| State | On entering (`0x007C72A0`) | Each pass (`0x007CDC20`) |
|---:|---|---|
| `1` | | moves to 2 once a meter is in use (`+0x648`) |
| `2` | starts a queued next music (`+0x830`, `0x007C43F0`), the stored request (`+0x6A8`; `0x007C4790`, or `0x007CAB80` with `+0x6AE` set), or the section's own next section | |
| `3` | | stops the other set's playing voices, and moves to 2 when no voices are left |
| `4` | | claims the target section's (`+0x644`) streams and moves to 2 once all, and a requested instrument's, are full |
| `5` | | refreshes the loop counts (`0x007CCDD0`) and moves to 6 at the change sample `+0x6B8` |
| `6` | resets the fade-out and, with a fade-in time `+0x6C0`, ramps the fade-in `+0x210` to 1.0 | starts the fade-out `+0x250` past its start point and moves to 7 at `+0x6BC` |
| `7` | swaps the two sets with their counts and mode blocks (`0x007CC110`), then finishes the change (`0x007C7CD0`) | once the fade-out is at 0, the extra voice has ended and the fade-in is full, stops the old set and moves to 3 |
| `8` | | loads the next music (`0x007CAF70`) and plays it when ready (`0x007C43F0`), or drops it and moves to 2 |
| `9` | resets the fade-out | fades this music out from the start point and ends it (state 7) at 0 |

Case 7 prints "Music::UpdateTransition (TRANSITION_STATE_POST_ENTRY) Failed to get currentSample!" when no voice
plays. In states 5 to 7 `0x007CDC20` also keeps the change points inside the loop region and moves the other set's
volume automation (`0x007C6D00`, ramp `+0x2D0`).

`0x007C7CD0` finishes a section change: the current section becomes the previous (`+0x640`), the next becomes current,
and the next is the request's target or the new section's own next (byte `+0x22`). It then reloads the meter and the
bar, beat and tick (`0x007C5FE0`, `0x007C6090`, `0x007F3800`), moves a running mode change's end point (`0x007CA440`,
`0x007C7BE0`), and tells the callback object (slot 3).

### Requests

`0x007C23C0` ("SetNextSection") checks a request and stores it at `+0x680` (target `+0x680`, sync type `+0x684`,
timing `+0x6AA`):

- Below state 2, in state 7, or with no next section (`+0x63C`) and no meter end (`+0x608`), it prints "Not appropriate state for
  transition. state_ = %d"; a bad target prints "Invalid section index = %d".
- In states 2 and 4 it only stores the request.
- Sync types 12 to 19 are the section's custom points 0 to 7: "Invalid custom point index = %d, numCustomPoints = %d"
  or "There is no custom points! index = %d" refuse a missing one.
- A request for the current section with no timing cancels a pending change; during state 5 it stops the entering
  set, turns looping back on for the current layers (`0x007EA920`) and returns to state 3.
- Transition state 0 prints "Transition state is invalid!", and states 8 and 9 print "SetNextSection canceled!
  Transitioning to next music...".

`0x007C2A60` ("Music::CheckTransitionTime") works out how long until a request lands: the time to the next sync point of
its type (`0x007C1830`), or to its own bar, beat and tick in the current section (`0x007C65C0`); when that has passed it
warns "Failed to sync to (%d,%d,%d)" and takes the sync point. It is at least the length of the target's transition instrument (section `+0x1C`,
`0x007C6960`) when the request asks for one. With no time left it warns "Transition failed because there remains no time
for transition. keep playing" and drops the request.

`0x007C43F0(music, next)` hands over to a next music. In states 1, 3, 6 and 7 it does nothing; when the next music's streams
are not ready it sets state 8;
otherwise it plays it at this music's next sync point (`0x007C1830`, `0x007C36C0`; "NextMusic CorePlay failed!!" on
failure), takes the fade values from the current section and sets state 9.

### Reverb end

`0x007C4030(music, send, seconds, fade)`, from the end command (`0x007C5760`), ends a music by raising one of its sends:

1. It needs the header ("musicData_ is not streamed yet."), a send from 1 to the header's count `+0x40` ("Invalid
   sendIndex = %d") and no reverb end already running ("Already executing reverb end!").
2. It finds the next sync point at least `seconds` ahead (`0x007C1830`; "Music::ReverbEnd failed to CalcSampleDelay").
3. It stores the send `+0x838`, the time `+0x880`, the fade `+0x884` and the point `+0x87C`, sets `+0x898` and drops
   any pending request.

On each pass `0x007CD000` waits for the point, ramps the send `+0x840` to 1.0 over the time with the curve `+0x894`, and
once it is full stops the music over the fade (slot 2).

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
| `0x007F2EA0` | normalises a timing |
| `0x007F2E30`, `0x007F2F30` | one tick back, one tick forward |
| `0x007F3140` | subtracts one timing from another |
| `0x007F2F10` | rounds up to the next bar when the beat or tick is not 0 |
| `0x007F2FA0`, `0x007F3080` | round a timing (bar `+0`, beat `+2`, tick `+3`) down to the grid of a sync type, and step it by one grid unit: 3 two ticks, 4 three ticks, 5 a beat, 6 two beats, 7 a bar, 8 two bars, 9 four bars, 10 eight bars, and for the step only 2 one tick; rounding clears the smaller units, and a step carries into the next beat at `+0x21` ticks and into the next bar at `+0x20` |
| `0x007F3570` | the sample of a timing: with `d` = timing − start timing `+0x08` (`0x007F3140`), `[+0x00] + d.bar x [+0x2C] + d.beat x [+0x28] + d.tick x [+0x24]`, or `[+0x04]` at the end timing `+0x0C`; a timing before the start or past the end is clamped with a warning ("GetSampleFromTiming timing is before startTiming"), and with byte `+0x18` clear it logs "Invalid Timing!" and returns `[+0x00]` (`0x007F3570`-`0x007F37FE`) |
| `0x007F3800` | the timing of a sample, through `0x007F2EA0`; "GetTimingFromSample Invalid Timing!" outside the music |
| `0x007F3510` | the sample of a custom point: from its timing (`0x007F3570`) when its byte `+0x18` is set, otherwise from its sample |
| `0x007F3430` | the timing of a meter record `+0x08`, or with its byte `+0x18` set the later of it and a given timing, rounded down to the sync grid (`0x007F2FA0`) |
| `0x007F31C0`, `0x007F3930`, `0x007F3DE0` | clear a timing record, clear a meter cursor, store a meter's three values |

`0x007F31F0` converts between seconds, samples and these units ([Sound engine](sound-engine.md)).

### Following the play position

`0x007CD350` ("Music::UpdateTiming") keeps the music's position on each pass:

1. It keeps last pass's timings (`+0x65C`, `+0x660`) and reads the current sample `+0x664` from the current set
   (`0x007C5AC0`). With no voice playing and no change to another section under way (transition state 5 or above), it
   stops every voice and sets state 7.
2. A sample below the last one means the section looped, and `0x007C7950` runs.
3. While the sample is past the meter's end `+0x608`, it moves to the next meter (`0x007C6090`), or prints "Next meter
   not found. currentSample = %d" when no meter is left.
4. At the section's exit point (section `+0x0C`) with no next section, or in state 9, it sets the timing to the
   section's end timing `+0x2C` rounded up to a bar (`0x007F2F10`). During a change to another section it waits, and
   otherwise it logs "Music::UpdateTiming exceeded exitPoint".
5. When the meter carries counts (`+0x61C`), it turns the sample into a bar, beat and tick at `+0x654` (`0x007F3800`),
   with a copy at `+0x658` moved one tick on when the sample is past half a tick (`0x007F2F30`).

`0x007C7950` handles a loop: it wraps the pending change points (`+0x67C`, the mode change's `+0x740`, the reverb end's
`+0x87C`) into the section's loop region, finishes or re-marks a mode change, restarts the volume automation at the
current point (`0x007C6D00`, ramp `+0x290`), counts the loop at `+0x670` and reloads the meter (`0x007C6090`).

| Function | Gives |
|---|---|
| `0x007C61A0` | a section's meter count: byte `+0x04` before version 8, `u16` `+0x18` from version 8 |
| `0x007C5FE0(section, sample)` | the index of the meter holding `sample`, by each meter's start `+0x0C` |
| `0x007C6090(music, cursor, section, meter)` | loads a meter into a cursor (`0x007F3950`), or clears it and prints "Invalid section index:%d" |
| `0x007C61C0` | a section's volume-automation point count: `u16` `+0x1E` from version 10, otherwise 0 |
| `0x007C6D00(music, sample, section)` | the index of the last automation point that starts before `sample`, or -1 |

### Timing callbacks

A music tells its callback object (`+0xB8`) when the music reaches a timing it asked for. Commands `0x29` and `0x2A`
add and remove the requests in the eight-node list `+0x8A8`. `0x007CD920`, on each pass, walks the list while the
callback object exists:

- A request of kind 0 looks at the bar, beat and tick `+0x654`, kind 1 at the rounded copy `+0x658`, and only when it
  changed since the last pass.
- A sync type of 1 to 11 fires when the timing sits on that grid (`0x007F2FA0` leaves it unchanged).
- A sync type of 12 to 19 fires when the timing equals one of that custom point list's points (`0x007D0120`, `0x007D05D0`).

A request that fires calls slot 4 of the callback object with the timing and the request's two values.

### Instruments

A `Magi::Instrument` plays one instrument of a music's `inst` chunk in time with that music; the run-time type data
names it in its list type, `FixedList<4, Magi::Instrument*>`. The pool holds 32 ([Sound driver objects](sound-driver-objects.md)),
and each keeps its voice at `+0x40` and a state at `+0x58`:

| Function | Does |
|---|---|
| `0x007CEF60(instrument, music, sync, semitones, fade)` | command `0x2C`: only in state 1; stores the music and the sync type `+0x28`, starts the volume ramp `+0xB8` over the fade, sets the pitch `2^(semitones/12)` at `+0x200`, and starts it (`0x007CEAB0`) |
| `0x007CEF10` | command `0x2D`: turns off the voice's loop when it has one (`0x007EBA90`, `0x007EA920`), so it ends with its material |
| `0x007CEAB0` | adds it to the category its record's byte `+0x06` names (`0x007A9A10`): an answer of 1 sets state 7 and 2 sets state 3; while paused it sets state 4; otherwise it plays it (`0x007CEB80`), sets state 5 and calls slot 1 of the callback object |
| `0x007CEB80` | picks the material: for kind 4 (record byte `+0x04`) material 1 when the music's next sync point is not on a bar line, otherwise 0; for kind 3 the value `+0x74` times 100; for other kinds 0. It then plays it from the music's next sync point (`0x007C1830`) with its own volume, pitch, filter flag, low-pass and panning |
| `0x007CF010(instrument, seconds)` | the pass (`0x007B82D0`): in state 5 it sets 7 once the voice has gone or ended; in states 2 to 4 it retries the start; in state 6 it stops the voice once the volume ramp `+0xB8` is at 0; then it pauses like a music and hands changed values to the voice |
| `0x007CEE30` | on free: releases the bank and calls slot 2 of the callback object |
| `0x007CEEE0` | gives the instrument's bank (`+0x38`); `0x007B8230`, from `0x007D0A20` and `0x007D0A70`, uses it to stop every instrument of one bank |

The handovers are `0x007CF4F0` (volume, slot 26, `0x007EE500`), `0x007CF4A0` (pitch, slot 27, `0x007EE300`), `0x007CF410`
(panning, slot 28, `0x007EDE90`) and `0x007CF370` (low-pass ramp `+0x140`, `0x007EDD20`); the filter flag `+0x204` goes to
`0x007EA9C0`.

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
- [Audio effects](audio-effects.md) - the pitch shifter and filters the music's voices carry.
