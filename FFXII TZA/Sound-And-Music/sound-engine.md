---
title: "Sound engine: the driver's class families, what a voice does in one tick, where its samples come from, and the diagnostics it prints"
kind: "system"
category: "Sound and music"
addresses: "0x007E0B60, 0x007EBAD0, 0x007EAA60, 0x007AF740, 0x007B0000, 0x007AEA20, 0x007AB5C0, 0x007F31F0"
---

## What the player sees

- Every sound effect, voice line and music track is mixed by one engine into an eight-channel 48 kHz output, which is
  then folded down to the player's speakers.
- Sounds start, pause, resume and stop a fraction of a second after the game asks, because each request waits in a queue
  for the sound thread.
- Nothing about the engine shows on screen: its error and warning messages go only to the Windows debug output.

## How it works

### Class families

The driver is Square Enix's `SQEX::Sd` library. The run-time type data names 124 plain classes and 83 template
instantiations, not counting the nested `NODE` helper structs (one plain, 19 template), and every engine object derives
from a `SeadObject<a, b>` template:

| Family | Plain classes | Holds |
|---|---:|---|
| `Driver` | 58 | sounds, banks, tracks, sequences, voices, effects, categories, the mixer; `Core` 8, `WASAPI` 5, `CRI` 2 of them |
| `ConfigFile` | 20 | the configuration file's records ([Sound engine configuration](sound-engine-config.md)) |
| `MabFile` | 17 | music banks ([Music](music.md)) |
| `SabFile` | 10 | sound banks ([Sound banks](sound-banks.md)) |
| `Lay` | 10 | the spatial layer ([Spatial sound](spatial-sound.md)) |
| `AudioBinaryFile` | 6 | the shared file container |
| `Magi` | 1 | `Music` |

A playing sound is a `Driver::Sound` (vtable `0x01CB5A30`) or a `Magi::Music` (`0x01CB5E38`); both implement
`Driver::ISound` (`0x01CB58C8`), whose methods the driver's commands call. Each bank is an `OnMemoryBank` (`0x01CB83F8`)
or a `StreamingBank` (`0x01CB84E8`), told apart by vtable slot 1: 1 (`0x007BD590`) or 2 (`0x007E3260`).

### The three voice kinds

The mixer is a graph of three `Driver::Core` voice classes. Slot 1 of each returns its kind:

| Class | Vtable (slots) | Kind | Role |
|---|---|---:|---|
| `CoreSourceVoice` | `0x01CB8360` (17) | 3 (`0x007D14C0`) | renders one source's samples |
| `CoreSubmixVoice` | `0x01CB82D0` (7) | 2 (`0x007E3260`) | a bus that sources send into |
| `CoreMasterVoice` | `0x01CB8290` (7) | 1 (`0x007BD590`) | the final mix |

A source voice holds up to eight send slots (destination and gain, 16 bytes each, `+0x218`) and a list of effects
(`+0x270`). Its open call `0x007E0980(voice, rate, channels, format, buffer, callback, sends, effects)` refuses more than
eight channels or format 0 and sets state 1.

### One tick of a source voice

The voice pass calls `0x007E0B60` once per 256-frame block for every live source voice:

1. It renders silence unless the voice is playing (state 3, `0x007E0B8C`) and holds a queued buffer (`+0xB0`,
   `0x007E0B9C`).
2. The step is the source rate over the device rate (`0x007AED00`), times the pitch `+0x108` (`0x007E0C0D`); a step of 0 or
   less renders silence.
3. When a marker sample `+0xA8` falls inside this block, it calls the producer's marker callback once and clears the
   marker (`0x007E0C81`-`0x007E0CC5`).
4. It builds the gain rows: for each source channel, eight output gains from the matrix at `+0x10C`, times the sample
   scale, which is 1/32767 (`0x01CB83E8`) for 16-bit input and 1.0 for float (`0x007E0CE1`-`0x007E0DA4`).
5. A negative start offset `+0xA0` is a start delay: the voice renders zeros and counts it up (`0x007E0DA9`-`0x007E0E6F`).
6. It ramps the gain from the current `+0x104` to the target `+0x100` across the block (`0x007E0E71`-`0x007E0EBE`). A step
   of exactly 1.0 copies samples; any other step resamples linearly (`0x007E0EDC`).
7. When a buffer runs out, it retires it (`0x007E0F21`-`0x007E0F6A`) and calls the producer's buffer callback, slot 1
   (`0x007E0F70`-`0x007E0F99`). That callback decodes and queues the next buffer, so decoding runs on the device thread.
8. It runs each effect on the block (`0x007E2418`-`0x007E2457`). It then mixes into each send: a kind 1 destination
   through `0x007DFE30`, a kind 2 through `0x007E0550` (`0x007E2462`-`0x007E2525`).

A source voice queues at most two buffers. `0x007E0A40` refuses a third, and refuses a byte count that is not a whole
number of frames (`(format 1 ? 2 : 4) x channels` bytes).

### Where samples come from

A `Driver::Voice` (vtable `0x01CB92A8`) feeds a source voice from one bank material. `Voice::Initialize` `0x007EBAD0`
reads the material's channels (byte `+4`), codec (byte `+5`) and rate (dword `+8`), and opens a decoder by codec:
the HCA decoder (`0x00123870`, `0x00123A50`) or the Vorbis stream (`0x007F5970`). The feed below runs the block decoders:

| Codec | Format | Block decoder, run by the feed |
|---:|---|---|
| 1 | 16-bit PCM, read in place | none |
| 2 | Microsoft ADPCM blocks | `0x007F6FB0`, which builds the seven coefficient pairs (256, 0) to (392, -232) and the 16-entry adaptation table 230 to 768 as constants; samples per block `0x007F7350` |
| 3 | Ogg Vorbis | `0x007F6750` |
| 7 | CRI HCA, to float | `0x001242F0` |

Any other codec prints "Voice::Initialize failed no support format!!! %d" (`0x007EC6BA`) and the voice does not play.
Every voice gets a `SimpleFilter` as effect 0 (`0x007EA003`); a sound effect of type 6 adds a `Flanger` (`0x007D99E0`),
and a music whose header is version 1 or later with bit `0x1` of `+0x0A` set adds a `GranularPitchShift`
(`0x007DA0A0`, `0x007ED186`-`0x007ED19A`), built bypassed; no shipped music sets that bit. The sends go to the bus the sound header names, or to a master
port, falling back to port 1 (`0x007EA460`).

The feed `0x007EAA60` runs from the voice's buffer callback `0x007ED4C0`:

1. While the source voice holds fewer than two buffers and the end flag `+0x12C` is clear, it decodes one buffer.
2. It queues the buffer with the running sample position `+0x130` (`0x007EB95B` on failure).
3. With the loop flag `+0x120` set it wraps over the material's loop region `+0xC`-`+0x10`; otherwise the end of the
   data sets `+0x12C`.
4. For an in-memory HCA material whose header byte `+0xD` is set, each frame byte is first XORed with the 256-byte table
   `0x01F41D30`.

When the voice has ended and its source voice is empty, `0x007ED4C0` sets the voice's state to 4.

### The voice's controls

A `Voice` keeps its source voice at `+0x68` and a state at `+0x70`: 1 once open, 2 playing, 3 paused and 4 ended.
`0x007EBAB0` reports it as 0, 1, 2 or 3 (3 for state 4), and every control below refuses an ended voice:

| Control | Function | Does |
|---|---|---|
| play | `0x007EDA60` | from state 1 only: fills the source voice (`0x007EAA60`) and runs its slot 3, or ends the voice when that fails |
| resume | `0x007EDAB0` | runs the source voice's slot 3 and sets state 2 |
| pause | `0x007EE6F0` | runs its slot 4 and sets state 3 |
| stop | `0x007EE670` | runs its slot 4 and sets state 4, or for a looping type 5 or 6 material only marks the end at `+0x12C` (`0x007EE6AF`) |
| volume | `0x007EE500` | clamps to 0-1 |
| pitch | `0x007EE300` | clamps to 1/512-2 and sets the source voice's pitch (slot 7) |
| low-pass | `0x007EDD20` | clamps to 0-1 and sets the `SimpleFilter`'s parameter `0x400` through `0x007D99A0` |
| granular pitch | `0x007EDB60` | clamps to 0.5-512 on the voice's `GranularPitchShift` effect |
| filter reset | `0x007EA9C0` | with a true flag sets the filter's parameter `0x400` to half the device rate (`0x007AED00`); stores the opposite flag at `+0x90` |
| loop | `0x007EA920`, `0x007EBA90` | set the loop flag `+0x120`, and answer whether the material has a loop region and the flag is set |
| effect value | `0x007EDB10` | sets a value of effect 1, 2 or 3 at `+0x108` |
| sends | `0x007EDAF0`, `0x007EDE70`, `0x007EE470` | set a send level on the source voice (its slot 16); `0x007EE470` can scale the current one |

A value that is not a finite number prints "set invalid volume!!", "set invalid pitch!!", "set invalid lowpass value!!"
or "set invalid granular pitch value!!". `0x007EBA40` gives a time read from the source voice, and `0x007EE430` and
`0x007EE450` pass two values on to it (`0x007E2660`, `0x007E2680`).

The decoders read an in-memory material through three callbacks `Voice::Initialize` hands them: `0x007EE730` copies
whole frames from the read position `+0x138`, `0x007EE7F0` sets that position and `0x007EE900` returns it. A streamed
material is read through `0x007EE800`, which takes the bank's stream for this voice (`0x007E2EB0`, `0x007E31B0`).

### The HCA mixer

`HCAMixerVoice` (slot 1 `0x007DD040`) mixes several HCA inputs through the CRI mixer `0x00121D40` into one source voice.
It is built only by `0x007DCD70`, the only writer of `[0x02EAE088]`, when the configuration's `hcam` flag is set. A voice
joins it instead of opening its own source voice only when its HCA header byte `+0xC` is set (`0x007DCAA0`).

`0x007DC6B0` builds the mixer voice, and `0x007DC730` frees its CRI mixer (`0x00121030`), buffers and inputs. `0x007DCAC0`
joins an input: it registers the voice with the CRI mixer (`0x00121770`) and appends it to the input list (`0x007DCB50`),
whose nodes `0x007DCC60` builds.

### The external source

`ExternalSourceVoice` (slot 1 `0x007B93A0`) is a voice its caller feeds with 16-bit buffers through `0x007B93E0`.
`0x006794D0` is its only creator; it opens it at 48000 Hz with three buffers of 48000 frames each
(`0x006794FC`-`0x00679533`).

`0x007A4930` is the driver call behind it: it allocates `0x520` bytes, builds the object (`0x007B8D40`; `0x007B8E50` puts
back its base vtables) and opens it (`0x007B9050`), returning its `IExternalSourceVoice` interface at `+0x08` or freeing
it on failure. `0x007B9590` moves queued caller blocks, from a 32-entry queue at `+0x78`, into the source voice's buffers
while it holds fewer than two, and `0x007B9AF0`, run for each external source by the update pass, advances its volume
and pitch ramps.

The movie player's `ExternalVoice` wraps it. `0x00679130` builds the wrapper with two events at `+0x30` and `+0x48`,
and `0x006792C0` closes them (`0x005CD700`) and puts back the driver's `ExternalVoiceCallback` vtable.
`0x0067A240(voice, samples, bytes)`, from the movie audio feed `0x00679600`, waits on `+0x48` (`0x005CD840`) and copies
the block into buffer `count % 3` of `+0x10`, `+0x18` and `+0x20`. The first time, with `+0x40` clear, it queues the
buffer at `+0x10` on the source (slot 1), signals `+0x30` (`0x005CD5E0`) and sets `+0x40`.

### Output format and the device

The driver's start-up `0x007AEF30` fixes the mix format:

| Setting | Value |
|---|---|
| rate | 48000 Hz (`0x007AC691`) |
| channels | 8 (`0x007AC698`); any other count is refused with "enable SIMD, need rendering channel 8" |
| frames per block | 256 (`0x007A4F46`) |
| source voice pool | the sum of three start-up counts, each capped: `min(+0x20, 2 x ([0x02EAD3E8] + 32)) + min(+0x24, 128) + min(+0x28, 32)` of the start-up block, unsigned (`0x007A4EC0`-`0x007A4EFD`) |
| buses | one submix per `bus ` chunk record |
| masters | one (`0x02EAD358`); a second (`0x02EAD360`) only with start-up byte `+0x1C` set, which is 0 |

The device asks for each block through `0x007DF690`, which runs `0x007AF740` under the lock `0x02EAE0B0`:

1. With `[0x02EAD390]` = 1 every master buffer is zeroed and sent.
2. Otherwise it runs the voice pass `0x007B0000`.
3. For each master it copies the mix clamped to -1 to 1 when the device has eight channels, or folds it down through
   `0x007B0B80` otherwise; it resamples with `0x007B0390` when the device rate is not 48000.
4. It hands the block to the device (`0x007DF3F0`), and updates a per-channel peak meter at `[0x02EAD378]`.

The two output ports are `WASAPI::AudioRenderer` objects at `0x02EAE0B8` and `0x02EAE0C0`, built by `0x007DDED0` (`0x007DD2B0`;
`0x007DD360` stops and frees one) with two callbacks, `0x007DF690` and `0x007DF660`; the second runs the function the start-up
block gives at `0x02EAE0A8` under the lock `0x02EAE0B0`.

`0x007DDD60` and `0x007DDE20` give a port's channel count and rate. `0x007DD980` reads a device
format: 16-bit PCM gives sample kind 2 and float gives 1. A renderer takes requests through a four-entry ring
(`0x007DDC20`) and output blocks through another (`0x007DF340`); `0x007DD410` releases a `WASAPIDevice`'s interfaces.

When a device changes, `0x007AF570` prints "Device Changed! [%d][Channel:%d][SamplingRate:%d]" and reallocates the
port's four output buffers for 1.1 blocks at the new rate and channel count, cut to a whole frame.

### The voice factory, pass and lifecycle

`0x007AEA20(out, rate, channels, format, callback, ..., heap)` builds a source voice. With `heap` 0 it takes one from
the pool `0x02EAD250` and links it into the list `0x02EAD2A0`; with `heap` 1 it allocates 0x2B8 bytes (`0x007AD460`) and
links it into `0x02EAD300` (`0x007AF490`). `Voice::Initialize` (`0x007ED303`) and the HCA mixer (`0x007DCE64`) give 0; the external source
(`0x007B91BC`) gives 1. `0x007E0650` builds a source voice and `0x007E0720` tears one down; `0x007AED10` and `0x007AEE20` build
the two fixed source lists.

The masters and buses take their blocks from the same pool `0x02EAD250`. `0x007AE930(out, ..., port)` builds the master
of an output port (`0x007DF930`, then `0x007DFB20` with a buffer from `0x02EAD200`), and `0x007AEC10` builds a submix
(`0x007DFF20`, then `0x007E0130`; `0x007DFF80` frees its two buffers) and links it into `0x02EAD2D0`.

The voice pass `0x007B0000` runs once per block:

1. It clears the masters (`0x007DFA50`) and each submix (`0x007E0040`).
2. It walks the pooled sources, then the allocated ones. A source in state 4 is unlinked, its buffer and object are
   returned, and its destructor runs; every other source renders (`0x007E0B60`).
3. It finishes the submixes (`0x007E01F0`) and then the masters (`0x007DFBB0`).

A source voice moves from open (1) to playing (3, slot 3 `0x007E2710`) or paused (2, slot 4 `0x007E2760`), and stop (slot 5
`0x007E07F0`) sets 4, which the next pass retires.

### The command queue

Game calls do not touch voices directly; they post actions. A poster takes an action from the free list `0x02EAD028`
(`0x007AB460`; when none is left it prints "Action exhausted!!") and appends it with `0x007AB550`. The driver thread
drains the queue in order in `0x007AB5C0`, by the action's type through the 54-entry jump table `0x007AC080`.

Types `0x00`-`0x04`, `0x07` and `0x08` first find a category with `0x007AAA20(id)`: entry `id` of the table at
`[0x02EAD008]` while `id` is below `[0x02EAD000]`, and the arm does nothing when that is null. A category's sound list is at `+0x28` of its `+0x58` object, or of
the category itself when `+0x58` is null. A ramp (`0x007CA560`) moves a value from where it is now to a target over
a time.

| Types | Arms | Does |
|---|---|---|
| `0x00` | `0x007AAA20`, then `0x007AA5B0` | stops each sound on the category's list whose slot `+0xC0` answer equals the category's `+0x60` (`ISound` slot `+0x10`) |
| `0x01` | `0x007AAA20`, then `0x007AA680` | when the category's pause count `+0x64` is 0, pauses those sounds (slot `+0x18`) and keeps the value at `+0x68`; either way counts it up |
| `0x02` | `0x007AAA20`, then `0x007AA3E0` | when the pause count is 1, resumes them (slot `+0x20`); either way counts it down, to no lower than 0 |
| `0x03` | `0x007AAA20`, then `0x007AA570` | starts the ramp of entry n + 1 of the category's 48-byte array at `+0x38` (count `+0x78`) |
| `0x04` | `0x007AAA20`, then `0x007AA550` | starts the ramp at the category's `+0x40` |
| `0x05` | `0x007AAD90` | starts the global ramp at `0x01F403E0` |
| `0x06` | `0x007AAC80` | starts the global ramp at `0x01F40410` |
| `0x07` | `0x007AAA20`, then `0x007AA4E0` | sets the category's bytes `+0x80` and `+0x81` |
| `0x08` | `0x007AAA20`, then `0x007AA4D0` | sets the category's bytes `+0x82` and `+0x83` |
| `0x09` | `0x007B2470`, `0x007D0A20` | bank |
| `0x0A` | `0x007B44C0`, `0x007BDFA0` | play a sound |
| `0x0B`-`0x1B` | `0x007AB1E0`, then an `ISound` method | one slot per type, in the next table |
| `0x1C`-`0x2D` | `0x007B77E0`, then a `Magi::Music` method | music, from `0x007C8370` to `0x007CEF60` |
| `0x2E`, `0x2F`, `0x31` | `0x007AC3E0` | mixer bus |
| `0x30` | `0x007ACD30` | effect preset |
| `0x32`, `0x33` | `0x007B1210`; `0x007B6350`, `0x007AE550` | two further driver arms |
| `0x34`, `0x35` | `0x007B4A00(0)` then `0x007AF560`, a jump to `0x007DF620`; `0x007B48F0(0)` then `0x007AF540`, a jump to `0x007DF560` | two arms that reach the output renderer |

`0x007AB1E0` turns the action's handle into a sound by its low byte: 2 through `0x007B44C0`, 8 through `0x007B77E0` and 9
through `0x007B7FD0`. The arm then calls one slot of that object's vtable, `Driver::Sound` (`0x01CB5A30`) or `Magi::Music`
(`0x01CB5E38`); `0x007AC3D0` only returns -1.

| Type | Slot | `Driver::Sound` | `Magi::Music` |
|---|---|---|---|
| `0x0B` | `+0x10` | `0x007BED30` (stop) | `0x007CA9E0` |
| `0x0C` | `+0x18` | `0x007BEF30` (pause) | `0x007CA9F0` |
| `0x0D` | `+0x20` | `0x007BE0B0` (resume) | `0x007C8890` |
| `0x0E` | `+0x38` | `0x007BEAF0` (volume) | `0x007CA650` |
| `0x0F` | `+0x40` | `0x007BE8A0` (pitch) | `0x007CA420` |
| `0x10` | `+0x48` | `0x007BE590` (panning) | `0x007CA370` |
| `0x11` | `+0x90` | `0x007BECD0` | `0x007CA750` |
| `0x12` | `+0x50` | `0x007BE510` | `0x007CA350` |
| `0x13` | `+0x58` | `0x007BEC70` | `0x007CA730` |
| `0x14` | `+0x60` | `0x007BE3E0` | `0x007C91C0` |
| `0x15` | `+0x68` | `0x007BE3F0` (low-pass) | `0x007C92D0` |
| `0x16` | `+0x70` | `0x007BE3D0` | `0x007C91A0` |
| `0x17` | `+0x78` | `0x007BE360` | `0x007C8CD0` |
| `0x18` | `+0x80` | `0x007BE3C0` | `0x007C9190` |
| `0x19` | `+0x88` | `0x007BEAE0` | `0x007AC3D0` |
| `0x1A` | `+0x98` | `0x007BEA30` | `0x007AC3D0` |
| `0x1B` | `+0xA0` | `0x007BE980` | `0x007AC3D0` |

The busiest posters are stop `0x007A84A0` (20 call sites), resume `0x007A7A20` (8), play `0x007A78B0` (7, type `0x0A` for a
sound and `0x1C` for music), pause `0x007A8590` (5) and set volume `0x007A81F0` (5).

### Threads

| Thread | Body | Pacing |
|---|---|---|
| driver update | `0x007A5400`, started at `0x007A5232` | drains the command queue (`0x007AB5C0`) and updates sounds, then `Sleep(10)` (`0x007A5521`); seeds `srand` once (`0x007A540B`) |
| spatial layer | `0x007A5E50`, started at `0x007A5D6D` | `Sleep(32)` (`0x007A5EE5`) |
| `AudioSampleThread` | `0x007DD950`, created at `0x007DE9B2` | waits up to 1000 ms on the device events (`0x007DD66A`); a buffer event renders blocks (`0x007DEC50`), a timeout or reset rebuilds the device (`0x007DD9F0`) |
| mock device | `0x007DEB80`, created at `0x007DE19C` | a 5 ms timer standing in for the device when the WASAPI device fails to start (`0x007DD9F0`) |
| job worker | `0x007B6D40`, started at `0x007B6FE4` | runs the jobs of a 48-entry ring (`0x02EAD8B0`) |

The update thread takes its priority from start-up block `+0x44` (`SetThreadPriority`, `0x007A524E`) and its affinity
mask from `+0x4C` (`SetThreadAffinityMask`, `0x007A5263`); the spatial thread's mask is `0x7C` (`0x002108D6`). The sample
thread's priority comes from the device's start-up block (`0x007DEA45`).

### Identity and diagnostics

The driver start-up `0x007A4D50` prints "master version 16.7.14.A" from the format "%s version %X.%X.%X.%X"
(`0x01CB42E0`, `0x007A4D86`-`0x007A4DBD`). The CRI libraries carry "HCA Mixer Ver.2.00.00 Build:Jul 31 2015 16:45:20"
(`0x01CB7AC0`) and "HCA Decoder (Float) Ver.2.05.00 Build:Jul 31 2015 16:45:20" (`0x01CBA5D0`).

The exe holds 159 strings starting "[sead]": 116 errors, 25 warnings and 18 info lines. They are referenced from 208
places in 90 functions; `Voice::Initialize` alone has 27. Each is formatted (`0x0019C5D0`) and written with
`OutputDebugStringA`, then passed to the sink `0x007A5570`. The sink forwards it to the game's audio callback object
(vtable `0x00906A18`), whose slot 3 `0x0016D6A0` is a bare `ret`, so the messages reach only the debug output.

| Group | Strings | Checks |
|---|---:|---|
| music | 59 | invalid section, mode, meter or transition; music not streamed yet; no free stream; timing out of range |
| decode and streams | 32 | unsupported codec, failed HCA and Vorbis calls, stream not ready, failed send or source creation |
| device | 28 | each WASAPI call, thread creation and priority, channel count; info lines for device and session changes |
| pools and lists | 13 | actions, layer actions, tracks, the sound heap and the voice lists running out |
| data and configuration | 13 | invalid sequence or track data, a category loop, a bad effect preset or bus |
| parameter range | 11 | volume, pitch, panning and low-pass values out of range |
| external source | 3 | initialize, queue overflow, resume |

### The time-unit converter

`0x007F31F0(meter, value, from, to)` converts a music time between units through a sample count. A value of 0, or a
meter rate `+0x30` of 0 or less, gives 0. The units are:

| Unit | To samples | Without the meter's counts (byte `+0x18`) |
|---:|---|---|
| 0 | seconds x rate | - |
| 1 | samples | - |
| 2 | x `[+0x24]` | 0.125 s |
| 3 | x `[+0x28]` | 0.5 s |
| 4 | x `[+0x2C]` | 2 s |

The sample count is truncated to a whole number (`0x007F3321`); on the way out units 2 and 3 divide by the whole
numbers `rate / 8` and `rate / 2` (`0x007F33CB`, `0x007F339B`). A unit above 4 gives 0. The music commands `0x007C92F0` and
`0x007CC4A0` call it.

## Shipped data

Over the `mtrl` chunks of all 4,609 `.sab` and 116 `.mab` banks:

| Banks | Codec | Materials |
|---|---:|---:|
| `.win.sab` | 7 (HCA) | 9,836 |
| `.win.sab` | 0 | 2 |
| `.orb.sab` (`shout`) | 4 | 1,329 |
| `.mab` | 7 (HCA) | 348 |

The game names its banks with the `.win.sab` suffix (`0x00908998`), so every material it loads is HCA; the `.orb`
copies use codec 4, which `Voice::Initialize` does not accept. HCA header byte `+0xC` is 0 in all 10,184 HCA materials, so the HCA mixer is
never used; byte `+0xD` is 1 in the 348 music materials and 0 in the rest. 11,374 materials are 48000 Hz and 139 are
44100 Hz; 7,759 are mono and 3,754 stereo. The two codec-0 materials, both in `se000`, have rate 0 and 0 channels.

## State

### Threads and the device

`0x007A5550`, the start routine of every driver thread, calls the function at `+0x08` of the block it is given with the
argument at `+0x10` (`0x007A5557`-`0x007A555B`). All of these are 0 in the file unless shown.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EACF70` | `void*` | 0 | the driver update thread's handle, from `_beginthreadex` | `0x00169660`, 0 (`0x00169669`); `0x007A4D50` (`0x007A5238`) | `0x007A4D50`, to set the thread's affinity mask from start-up block `+0x4C` unless that is -1 (`0x007A5259`) |
| `0x02EACF78` | `void*` | 0 | `+0x08` of that thread's block: its body `0x007A5400` | `0x00169660` (`0x00169670`); `0x007A4D50` (`0x007A51FE`) | `0x007A5550`, through the block's address (`0x007A51F7`) |
| `0x02EACF80` | `void*` | 0 | `+0x10` of that block: the body's argument, 0 | `0x00169660` (`0x00169677`); `0x007A4D50` (`0x007A522B`) | `0x007A5550`, through the block's address |
| `0x02EACF88` | `i32` | 0 | 0, stored with an exchange whose old value is not used | `0x00169640` (`0x00169649`); `0x007A4D50` (`0x007A4DC5`) | only those two exchanges |
| `0x02EACF8C` | `u8` | 0 | the update thread's stop flag: the thread ends when it is not 0, and nothing stores anything but 0 | `0x007A4D50`, 0 (`0x007A5210`) | `0x007A5400` (`0x007A5411`, `0x007A552C`) |
| `0x02EACF8D` | `u8` | 0 | 1 once the driver has started: a second start returns at once, and the spatial layer's start `0x007A5B50` asks `0x007A52B0` for it first (`0x007A5B7E`) | `0x007A4D50`, 1 (`0x007A5224`) | `0x007A4D50` (`0x007A4D73`); `0x007A52B0` (`0x007A52B0`) |
| `0x02EACF90` | `u64` | 0 | the clock count (`0x007AD630`) at the update thread's last pass; the pass time is the difference over the clock rate (`0x007AD670`) | `0x007A4D50` (`0x007A4ED0`); `0x007A5400` (`0x007A548C`) | `0x007A5400` (`0x007A545D`) |
| `0x02EACF98` | `void*` | 0 | start-up block `+0x10`: the address of `+0x28` of the sound object `[0x01FD36A0]` (`0x00210814`), whose class `0x00906A18` has the return stub `0x0016D6A0` in slots 1 to 3 | `0x007A4D50` (`0x007A4DCF`) | `0x007A5400`, which calls its slot 1 before each pass (`0x007A5440`) and slot 2 after it (`0x007A550F`); `0x007A5570`, which formats each driver message and hands it with its level to slot 3 (`0x007A559A`, `0x007A5622`) |
| `0x02EACFD0` | `void*` | 0 | the spatial layer thread's handle | `0x001696D0`, 0 (`0x001696D9`); `0x007A5B50`, from `_beginthreadex` (`0x007A5D6D`, import `0x008C2D70`; stored at `0x007A5D73`) | `0x007A5B50`, to set the thread's affinity (`0x007A5D94`) |
| `0x02EACFD8` | `void*` | 0 | `+0x08` of that thread's block: its body `0x007A5E50` | `0x001696D0` (`0x001696E0`); `0x007A5B50` (`0x007A5D46`) | `0x007A5550`, through the block's address (`0x007A5D1D`) |
| `0x02EACFE0` | `void*` | 0 | `+0x10` of that block: the body's argument, 0 | `0x001696D0` (`0x001696E7`); `0x007A5B50` (`0x007A5D66`) | `0x007A5550`, through the block's address |
| `0x02EACFE8` | `u8` | 0 | 1 once the spatial layer has started; a second start returns at once | `0x007A5B50` (`0x007A5D54`) | `0x007A5B50` (`0x007A5B6B`) |
| `0x02EACFE9` | `u8` | 0 | the spatial thread's stop flag: the thread ends when it is not 0, and nothing stores anything but 0 | `0x007A5B50`, 0 (`0x007A5D3F`) | `0x007A5E50` (`0x007A5E54`, `0x007A5EF0`) |
| `0x02EACFF0` | `u64` | 0 | the clock count (`0x007AD630`) at the spatial thread's last pass; the pass time is the difference over the clock rate | `0x007A5B50` (`0x007A5D2F`); `0x007A5E50` (`0x007A5EBA`) | `0x007A5E50` (`0x007A5E8B`) |
| `0x02EAD810` | `void*` | 0 | the job worker thread's handle | `0x00169F50`, 0 (`0x00169F59`); `0x007B6F70`, from `_beginthreadex` (`0x007B6FE4`, import `0x008C2D70`; stored at `0x007B6FEA`) | `0x007B6F70`, to set its affinity (`0x007B7006`) |
| `0x02EAD818` | `void*` | 0 | `+0x08` of the worker's block: its body `0x007B6D40` | `0x00169F50` (`0x00169F60`); `0x007B6F70` (`0x007B6FA4`) | `0x007A5550`, through the block's address (`0x007B6F9B`) |
| `0x02EAD820` | `void*` | 0 | `+0x10` of that block: the argument, 0 | `0x00169F50` (`0x00169F67`); `0x007B6F70` (`0x007B6FDD`) | `0x007A5550`, through the block's address |
| `0x02EAD890` | `u8` | 0 | the job worker's stop flag: the loop ends when it is not 0, and nothing stores anything but 0 | `0x007B6F70`, 0 (`0x007B6FD6`) | `0x007B6D40` (`0x007B6D44`, `0x007B6F43`) |
| `0x02EAD8A0` | `i32` | 0 | the id of the job the worker is running, 0 when none; the worker copies the job's 16-byte ring entry here | `0x007B6D40` (`0x007B6DCB`, and 0 after the job at `0x007B6E54`); `0x007B6F70`, 0 (`0x007B703F`) | `0x007B7070`, which answers whether a job is still pending or running (`0x007B7091`) |
| `0x02EAD8A8` | `void*` | 0 | the running job's object, whose slot 1 the worker calls | `0x007B6D40` (`0x007B6DCB`, and 0 after the job at `0x007B6E5A`); `0x007B6F70`, 0 (`0x007B7047`) | `0x007B6D40` (`0x007B6E35`) |
| `0x01F40438` | `u8` | 1 | 1 until the first block: the first block copies its per-channel peaks into the meter at `[0x02EAD380]`, every later block keeps the larger of the two; nothing sets it back to 1 | `0x007AF740`, 0 (`0x007AFE68`) | `0x007AF740` (`0x007AFC15`) |
| `0x02EAD3AC` | `i32` | 0 | a position `0x007AF740` reads and advances only while `[0x02EAD390]` is 2 (`0x007AFEF4`-`0x007AFF79`); the only store to `0x02EAD390` puts 0 there (`0x007AEF30`, `0x007AF339`, the same 0 it stores into `0x02EAD308`), so in the shipped game this is never reached | `0x007AF740` (`0x007AFF79`) | `0x007AF740` (`0x007AFF06`, `0x007AFF6D`) |
| `0x02EAE090` | `i32` | 0 | the size of the HCA mixer's silent buffer, its argument's `+0x08` times 512 | `0x007DCD70` (`0x007DCD9A`) | `0x007DCD70` (`0x007DCDA5`); `0x007DCE20` (`0x007DCFF2`) and `0x007DD040` (`0x007DD1DF`), which hand the buffer to the voice's slot at `+0x48` |
| `0x02EAE098` | `void*` | 0 | that buffer, allocated with tag 5 (`0x007AD550`) and zeroed | `0x007DCD70` (`0x007DCDB1`) | `0x007DCE20` (`0x007DCFF9`); `0x007DD040` (`0x007DD1E6`) |
| `0x02EAE0A0` | `void*` | 0 | the block callback from the device block `+0x08`, `0x007AF740` (`0x007AEFEC`) | `0x007DDED0` (`0x007DDEFA`) | called by `0x007DF690` under the lock `0x02EAE0B0` when the device asks for a block (`0x007DF6AA`) |

The one address taken near the update thread's block, `0x02EACF68` (`0x007A4190`, `0x008A5AF0`), is a one-time
initialisation guard and reaches none of it.

### The external sources

The update pass keeps every open external source in a list linked through each source's `+0x4F0` (previous) and
`+0x4F8` (next); `0x007B9050` puts a newly opened source at the front, and `0x007B99B0` takes out a source whose byte
`+0x488` is set and whose `+0x68` object's slot 2 answers 0 or less (`0x007B99F2`-`0x007B9A86`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EADD30` | `void*` | 0 | the first source | `0x007B9050` (`0x007B92FA`, `0x007B9334`); `0x007B99B0` (`0x007B9A3C`) | `0x007B9050` (`0x007B92E9`, `0x007B9318`, `0x007B9326`); `0x007B99B0` (`0x007B99CB`, `0x007B9A30`) |
| `0x02EADD38` | `void*` | 0 | the last source | `0x007B9050` (`0x007B92F3`); `0x007B99B0` (`0x007B9A53`) | `0x007B99B0` (`0x007B9A43`) |
| `0x02EADD40` | `i32` | 0 | the sources in the list | `0x007B9050` (`0x007B933B`); `0x007B99B0` (`0x007B9A86`) | the same two |

### Voice lists and the command queue

The pooled source voices and the submixes are `ObjectList`s, the command queue a `DriverQueue` and the allocated
source voices a list of `0x20`-byte nodes (class `0x01CB4AB8`, previous `+0x08`, next `+0x10`, voice `+0x18`) that
`0x007AF490` puts at the front; the layouts are on [Sound driver objects](sound-driver-objects.md). "Through the
address" names the helpers a function hands the list to.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAD048` | `void*` | 0 | command queue `+0x08`, the cells, 1,024 of them | `0x00169720` (`0x00169744`); `0x008B86A0`, 0 after freeing them (`0x008B86F1`); through the address: `0x007AB240` (`0x007AB27C`, `0x007AB332`), from `0x007AB390` (`0x007AB3E2`) | `0x008B86A0`, which frees them at exit (`0x008B86A4`); through the address: `0x007AB240`, which frees the old cells and chains the new ones (`0x007AB255`, `0x007AB350`) |
| `0x02EAD050` | `void*` | 0 | command queue `+0x10`, first free cell | `0x00169720` (`0x00169744`); `0x007AB550` (`0x007AB56F`); `0x007AB5C0` (`0x007AB65D`); `0x008B86A0` (`0x008B86F1`); through the address: `0x007AB240` (from `0x007AB390`) | `0x007AB550` (`0x007AB556`); `0x007AB5C0` (`0x007AB64C`) |
| `0x02EAD058` | `void*` | 0 | command queue `+0x18`, first queued cell | `0x00169720` (`0x0016974C`); `0x007AB550` (`0x007AB587`); `0x007AB5C0` (`0x007AB645`); `0x008B86A0` (`0x008B8700`); through the address: `0x007AB240` (from `0x007AB390`) | `0x007AB550` (`0x007AB57E`); `0x007AB5C0` (`0x007AB5E7`, `0x007AC01C`) |
| `0x02EAD068` | `i32` | 0 | command queue `+0x28`, capacity: 1,024 cells | `0x00169720`, 0 with `+0x2C` (`0x0016973D`); through the address: `0x007AB240` (`0x007AB2B0`), from `0x007AB390` (`0x007AB3E2`) | no instruction |
| `0x02EAD06C` | `i32` | 0 | command queue `+0x2C`, cells queued | `0x00169720` (`0x0016973D`); `0x007AB550` (`0x007AB59B`); `0x007AB5C0` (`0x007AB657`); `0x008B86A0` (`0x008B86DD`); through the address: `0x007AB240` (from `0x007AB390`) | `0x007AB550` (`0x007AB59B`); `0x007AB5C0` (`0x007AB657`) |
| `0x02EAD2A8` | `i32` | 0 | pooled source-voice list `+0x08`, capacity: the nodes the list holds | `0x00169930` (`0x0016994D`); through the address: `0x007AED10` with `0x007B6AA0` (from `0x007AEF30`) | `0x007B0000` (`0x007B00FF`); through the address: `0x007AED10` with `0x007B6AA0` (from `0x007AEF30`) |
| `0x02EAD2AC` | `i32` | 0 | pooled source-voice list `+0x0C`, nodes in use | `0x00169930` (`0x0016994D`); `0x007B0000` (`0x007B018A`); `0x008B8850` (`0x008B888D`); through the address: `0x007AF380` (from `0x007AEA20`); `0x007AED10` with `0x007B6AA0` (from `0x007AEF30`) | `0x007B0000` (`0x007B018A`); through the address: `0x007AF380` (from `0x007AEA20`) |
| `0x02EAD2B0` | `void*` | 0 | pooled source-voice list `+0x10`, the `DriverListNode` array | `0x00169930` (`0x00169954`); `0x008B8850` (`0x008B88A1`); through the address: `0x007AED10` with `0x007B6AA0` (from `0x007AEF30`) | `0x007B0000` (`0x007B010F`); `0x008B8850` (`0x008B8854`); through the address: `0x007AED10` with `0x007B6AA0` (from `0x007AEF30`) |
| `0x02EAD2B8` | `void*` | 0 | pooled source-voice list `+0x18`, first free node | `0x00169930` (`0x00169954`); `0x007B0000` (`0x007B0193`); `0x008B8850` (`0x008B88A1`); through the address: `0x007AF380` (from `0x007AEA20`); `0x007AED10` with `0x007B6AA0` (from `0x007AEF30`) | `0x007B0000` (`0x007B016F`, `0x007B017A`); through the address: `0x007AF380` (from `0x007AEA20`) |
| `0x02EAD2C0` | `void*` | 0 | pooled source-voice list `+0x20`, first node in use | `0x00169930` (`0x0016995C`); `0x007B0000` (`0x007B012E`); `0x008B8850` (`0x008B88B0`); through the address: `0x007AF380` (from `0x007AEA20`); `0x007AED10` with `0x007B6AA0` (from `0x007AEF30`) | `0x007B0000` (`0x007B00B4`); through the address: `0x007AF380` (from `0x007AEA20`) |
| `0x02EAD2C8` | `void*` | 0 | pooled source-voice list `+0x28`, last node in use | `0x00169930` (`0x0016995C`); `0x007B0000` (`0x007B0151`); `0x008B8850` (`0x008B88B0`); through the address: `0x007AF380` (from `0x007AEA20`); `0x007AED10` with `0x007B6AA0` (from `0x007AEF30`) | through the address: `0x007AF380` (from `0x007AEA20`) |
| `0x02EAD2D8` | `i32` | 0 | submix list `+0x08`, capacity: the nodes the list holds | `0x001699A0`, 0 with `+0x0C` (`0x001699BD`); through the address: `0x007AEE20` (`0x007AEE85`), from `0x007AEF30` (`0x007AF2FA`) | through the address: `0x007B6AA0` (`0x007B6AB1`, `0x007B6AE6`), from `0x007AEE20` (`0x007AEF0B`) |
| `0x02EAD2DC` | `i32` | 0 | submix list `+0x0C`, nodes in use | `0x001699A0` (`0x001699BD`); `0x008B88D0` (`0x008B890D`); through the address: `0x007AF380` (`0x007AF459`), from `0x007AEC10` (`0x007AEC99`); `0x007AEE20` (`0x007AEE71`) with `0x007B6AA0` (`0x007B6AF5`), from `0x007AEF30` | through the address: `0x007AF380` (`0x007AF459`), from `0x007AEC10` |
| `0x02EAD2E0` | `void*` | 0 | submix list `+0x10`, the `DriverListNode` array | `0x001699A0` (`0x001699C4`); `0x008B88D0` (`0x008B8921`); through the address: `0x007AEE20` (`0x007AEE61`, `0x007AEF04`), from `0x007AEF30` | `0x008B88D0`, which frees it at exit (`0x008B88D4`); through the address: `0x007AEE20` (`0x007AEE35`) with `0x007B6AA0` (`0x007B6AA0`, `0x007B6AC0`, `0x007B6AC9`), from `0x007AEF30` |
| `0x02EAD2F0` | `void*` | 0 | submix list `+0x20`, first node in use | `0x001699A0` (`0x001699CC`); `0x008B88D0` (`0x008B8930`); through the address: `0x007AF380` (from `0x007AEC10`); `0x007AEE20` with `0x007B6AA0` (from `0x007AEF30`) | `0x007B0000` (`0x007B0076`, `0x007B02F1`); through the address: `0x007AF380` (from `0x007AEC10`) |
| `0x02EAD308` | `i32` | 0 | allocated source-voice list `+0x08`, nodes in the list | `0x00169830` (`0x00169839`, `0x0016984A`); `0x007AEF30` (`0x007AF331`); `0x007B0000` (`0x007B0292`); `0x008B87B0` (`0x008B87E9`); through the address: `0x007AF490` (from `0x007AEA20`) | `0x007B0000` (`0x007B0292`); through the address: `0x007AF490` (from `0x007AEA20`) |
| `0x02EAD310` | `void*` | 0 | allocated source-voice list `+0x10`, first node | `0x00169830` (`0x0016985B`); `0x007AEF30` (`0x007AF347`); `0x007B0000` (`0x007B024C`); `0x008B87B0` (`0x008B87FA`); through the address: `0x007AF490` (from `0x007AEA20`) | `0x007AEF30` (`0x007AF2FF`); `0x007B0000` (`0x007B01FD`); `0x008B87B0` (`0x008B87B6`); through the address: `0x007AF490` (from `0x007AEA20`) |
| `0x02EAD318` | `void*` | 0 | allocated source-voice list `+0x18`, last node | `0x00169830` (`0x0016985B`); `0x007AEF30` (`0x007AF347`); `0x007B0000` (`0x007B026F`); `0x008B87B0` (`0x008B87FA`); through the address: `0x007AF490` (from `0x007AEA20`) | no instruction |

No other instruction reaches these globals.

## Modding notes

- A replacement sound can be 16-bit PCM (codec 1), Microsoft ADPCM (2), Ogg Vorbis (3) or HCA (7); the driver plays
  all four.
- The mix is always 48 kHz in eight channels; a material at another rate is resampled per voice.
- Setting HCA header byte `+0xD` turns on the XOR table `0x01F41D30` for an in-memory material.
- The driver's messages can be read with a debug-output viewer while the game runs.

## Related

- [Sound banks](sound-banks.md) - the bank files the voices read.
- [Sound engine configuration](sound-engine-config.md) - the start-up file, buses and the `hcam` flag.
- [Sound effects](sound-effects.md) - the play call that posts actions.
- [Sound variations](sound-variations.md) - how a sound picks what to play.
- [Music](music.md) - the music commands.
- [Spatial sound](spatial-sound.md) - the layer thread.
