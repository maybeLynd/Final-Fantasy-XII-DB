---
title: "Sound engine: the driver's class families, what a voice does in one tick, where its samples come from, and the diagnostics it prints"
kind: "system"
category: "Sound and music"
summary: "The SQEX sound driver inside the game: its class families and the three voice kinds, what a source voice does in one 256-frame tick, which codecs feed it and that every shipped material is HCA, the 48 kHz eight-channel output and the device thread, the voice factory, pass and lifecycle, the command queue with its 54 action types, the threads and their pacing, the version and diagnostic strings, and the time-unit converter."
addresses: "007E0B60, 007EBAD0, 007EAA60, 007AF740, 007B0000, 007AEA20, 007AB5C0, 007F31F0"
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

A playing sound is a `Driver::Sound` (vtable `01CB5A30`) or a `Magi::Music` (`01CB5E38`); both implement
`Driver::ISound` (`01CB58C8`), whose methods the driver's commands call. Each bank is an `OnMemoryBank` (`01CB83F8`)
or a `StreamingBank` (`01CB84E8`), told apart by vtable slot 1: 1 (`007BD590`) or 2 (`007E3260`).

### The three voice kinds

The mixer is a graph of three `Driver::Core` voice classes. Slot 1 of each returns its kind:

| Class | Vtable (slots) | Kind | Role |
|---|---|---:|---|
| `CoreSourceVoice` | `01CB8360` (17) | 3 (`007D14C0`) | renders one source's samples |
| `CoreSubmixVoice` | `01CB82D0` (7) | 2 (`007E3260`) | a bus that sources send into |
| `CoreMasterVoice` | `01CB8290` (7) | 1 (`007BD590`) | the final mix |

A source voice holds up to eight send slots (destination and gain, 16 bytes each, `+0x218`) and a list of effects
(`+0x270`). Its open call `007E0980(voice, rate, channels, format, buffer, callback, sends, effects)` refuses more than
eight channels or format 0 and sets state 1.

### One tick of a source voice

The voice pass calls `007E0B60` once per 256-frame block for every live source voice:

1. It renders silence unless the voice is playing (state 3, `007E0B8C`) and holds a queued buffer (`+0xB0`,
   `007E0B9C`).
2. The step is the source rate over the device rate (`007AED00`), times the pitch `+0x108` (`007E0C0D`); a step of 0 or
   less renders silence.
3. When a marker sample `+0xA8` falls inside this block, it calls the producer's marker callback once and clears the
   marker (`007E0C81`-`007E0CC5`).
4. It builds the gain rows: for each source channel, eight output gains from the matrix at `+0x10C`, times the sample
   scale, which is 1/32767 (`01CB83E8`) for 16-bit input and 1.0 for float (`007E0CE1`-`007E0DA4`).
5. A negative start offset `+0xA0` is a start delay: the voice renders zeros and counts it up (`007E0DA9`-`007E0E6F`).
6. It ramps the gain from the current `+0x104` to the target `+0x100` across the block (`007E0E71`-`007E0EBE`). A step
   of exactly 1.0 copies samples; any other step resamples linearly (`007E0EDC`).
7. When a buffer runs out, it retires it (`007E0F21`-`007E0F6A`) and calls the producer's buffer callback, slot 1
   (`007E0F70`-`007E0F99`). That callback decodes and queues the next buffer, so decoding runs on the device thread.
8. It runs each effect on the block (`007E2418`-`007E2457`). It then mixes into each send: a kind 1 destination
   through `007DFE30`, a kind 2 through `007E0550` (`007E2462`-`007E2525`).

A source voice queues at most two buffers. `007E0A40` refuses a third, and refuses a byte count that is not a whole
number of frames (`(format 1 ? 2 : 4) x channels` bytes).

### Where samples come from

A `Driver::Voice` (vtable `01CB92A8`) feeds a source voice from one bank material. `Voice::Initialize` `007EBAD0`
reads the material's channels (byte `+4`), codec (byte `+5`) and rate (dword `+8`), and opens a decoder by codec:
the HCA decoder (`00123870`, `00123A50`) or the Vorbis stream (`007F5970`). The feed below runs the block decoders:

| Codec | Format | Block decoder, run by the feed |
|---:|---|---|
| 1 | 16-bit PCM, read in place | none |
| 2 | Microsoft ADPCM blocks | `007F6FB0`, which builds the seven coefficient pairs (256, 0) to (392, -232) and the 16-entry adaptation table 230 to 768 as constants; samples per block `007F7350` |
| 3 | Ogg Vorbis | `007F6750` |
| 7 | CRI HCA, to float | `001242F0` |

Any other codec prints "Voice::Initialize failed no support format!!! %d" (`007EC6BA`) and the voice does not play.
Every voice gets a `SimpleFilter` as effect 0 (`007EA003`); a sound effect of type 6 adds a `Flanger` (`007D99E0`),
and music adds a `GranularPitchShift` (`007DA0A0`). The sends go to the bus the sound header names, or to a master
port, falling back to port 1 (`007EA460`).

The feed `007EAA60` runs from the voice's buffer callback `007ED4C0`:

1. While the source voice holds fewer than two buffers and the end flag `+0x12C` is clear, it decodes one buffer.
2. It queues the buffer with the running sample position `+0x130` (`007EB95B` on failure).
3. With the loop flag `+0x120` set it wraps over the material's loop region `+0xC`-`+0x10`; otherwise the end of the
   data sets `+0x12C`.
4. For an in-memory HCA material whose header byte `+0xD` is set, each frame byte is first XORed with the 256-byte table
   `01F41D30`.

When the voice has ended and its source voice is empty, `007ED4C0` sets the voice's state to 4.

### The HCA mixer

`HCAMixerVoice` (slot 1 `007DD040`) mixes several HCA inputs through the CRI mixer `00121D40` into one source voice.
It is built only by `007DCD70`, the only writer of `[02EAE088]`, when the configuration's `hcam` flag is set. A voice
joins it instead of opening its own source voice only when its HCA header byte `+0xC` is set (`007DCAA0`).

### The external source

`ExternalSourceVoice` (slot 1 `007B93A0`) is a voice its caller feeds with 16-bit buffers through `007B93E0`.
`006794D0` is its only creator; it opens it at 48000 Hz with three buffers of 48000 frames each
(`006794FC`-`00679533`).

### Output format and the device

The driver's start-up `007AEF30` fixes the mix format:

| Setting | Value |
|---|---|
| rate | 48000 Hz (`007AC691`) |
| channels | 8 (`007AC698`); any other count is refused with "enable SIMD, need rendering channel 8" |
| frames per block | 256 (`007A4F46`) |
| source voice pool | the sum of three start-up counts, each capped (`007A4ED7`-`007A4EFD`) |
| buses | one submix per `bus ` chunk record |
| masters | one (`02EAD358`); a second (`02EAD360`) only with start-up byte `+0x1C` set, which is 0 |

The device asks for each block through `007DF690`, which runs `007AF740` under the lock `02EAE0B0`:

1. With `[02EAD390]` = 1 every master buffer is zeroed and sent.
2. Otherwise it runs the voice pass `007B0000`.
3. For each master it copies the mix clamped to -1 to 1 when the device has eight channels, or folds it down through
   `007B0B80` otherwise; it resamples with `007B0390` when the device rate is not 48000.
4. It hands the block to the device (`007DF3F0`), and updates a per-channel peak meter at `[02EAD378]`.

### The voice factory, pass and lifecycle

`007AEA20(out, rate, channels, format, callback, ..., heap)` builds a source voice. With `heap` 0 it takes one from
the pool `02EAD250` and links it into the list `02EAD2A0`; with `heap` 1 it allocates 0x2B8 bytes (`007AD460`) and
links it into `02EAD300`. `Voice::Initialize` (`007ED303`) and the HCA mixer (`007DCE64`) give 0; the external source
(`007B91BC`) gives 1.

The voice pass `007B0000` runs once per block:

1. It clears the masters (`007DFA50`) and each submix (`007E0040`).
2. It walks the pooled sources, then the allocated ones. A source in state 4 is unlinked, its buffer and object are
   returned, and its destructor runs; every other source renders (`007E0B60`).
3. It finishes the submixes (`007E01F0`) and then the masters (`007DFBB0`).

A source voice moves from open (1) to playing (3, slot 3 `007E2710`) or paused (2, slot 4 `007E2760`), and stop (slot 5
`007E07F0`) sets 4, which the next pass retires.

### The command queue

Game calls do not touch voices directly; they post actions. A poster takes an action from the free list `02EAD028`
(`007AB460`; when none is left it prints "Action exhausted!!") and appends it with `007AB550`. The driver thread
drains the queue in order in `007AB5C0`, by the action's type through the 54-entry jump table `007AC080`:

| Types | Arms | Does |
|---|---|---|
| `0x00`-`0x08` | `007AAA20` with `007AA5B0`, `007AA570`, `007AAD90`, `007AAC80` and others | category volume and pitch |
| `0x09` | `007B2470`, `007D0A20` | bank |
| `0x0A` | `007B44C0`, `007BDFA0` | play a sound |
| `0x0B`-`0x1B` | `007AB1E0`, then an `ISound` method | stop `007BED30`, pause `007BEF30`, resume `007BE0B0`, volume `007BEAF0`, pitch `007BE8A0`, panning `007BE590`, low-pass `007BE3F0`, and the rest |
| `0x1C`-`0x2D` | `007B77E0`, then a `Magi::Music` method | music, from `007C8370` to `007CEF60` |
| `0x2E`, `0x2F`, `0x31` | `007AC3E0` | mixer bus |
| `0x30` | `007ACD30` | effect preset |
| `0x32`, `0x33` | `007B1210`; `007B6350`, `007AE550` | two further driver arms |
| `0x34`, `0x35` | `007B4A00(0)` then `007AF560`, a jump to `007DF620`; `007B48F0(0)` then `007AF540`, a jump to `007DF560` | two arms that reach the output renderer |

The busiest posters are stop `007A84A0` (20 call sites), resume `007A7A20` (8), play `007A78B0` (7, type `0x0A` for a
sound and `0x1C` for music), pause `007A8590` (5) and set volume `007A81F0` (5).

### Threads

| Thread | Body | Pacing |
|---|---|---|
| driver update | `007A5400`, started at `007A5232` | drains the command queue (`007AB5C0`) and updates sounds, then `Sleep(10)` (`007A5521`); seeds `srand` once (`007A540B`) |
| spatial layer | `007A5E50`, started at `007A5D6D` | `Sleep(32)` (`007A5EE5`) |
| `AudioSampleThread` | `007DD950`, created at `007DE9B2` | waits up to 1000 ms on the device events (`007DD66A`); a buffer event renders blocks (`007DEC50`), a timeout or reset rebuilds the device (`007DD9F0`) |
| mock device | `007DEB80`, created at `007DE19C` | a 5 ms timer standing in for the device when the WASAPI device fails to start (`007DD9F0`) |
| job worker | `007B6D40`, started at `007B6FE4` | runs the jobs of a 48-entry ring (`02EAD8B0`) |

The update thread takes its priority from start-up block `+0x44` (`SetThreadPriority`, `007A524E`) and its affinity
mask from `+0x4C` (`SetThreadAffinityMask`, `007A5263`); the spatial thread's mask is `0x7C` (`002108D6`). The sample
thread's priority comes from the device's start-up block (`007DEA45`).

### Identity and diagnostics

The driver start-up `007A4D50` prints "master version 16.7.14.A" from the format "%s version %X.%X.%X.%X"
(`01CB42E0`, `007A4D86`-`007A4DBD`). The CRI libraries carry "HCA Mixer Ver.2.00.00 Build:Jul 31 2015 16:45:20"
(`01CB7AC0`) and "HCA Decoder (Float) Ver.2.05.00 Build:Jul 31 2015 16:45:20" (`01CBA5D0`).

The exe holds 159 strings starting "[sead]": 116 errors, 25 warnings and 18 info lines. They are referenced from 208
places in 90 functions; `Voice::Initialize` alone has 27. Each is formatted (`0019C5D0`) and written with
`OutputDebugStringA`, then passed to the sink `007A5570`. The sink forwards it to the game's audio callback object
(vtable `00906A18`), whose slot 3 `0016D6A0` is a bare `ret`, so the messages reach only the debug output.

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

`007F31F0(meter, value, from, to)` converts a music time between units through a sample count. A value of 0, or a
meter rate `+0x30` of 0 or less, gives 0. The units are:

| Unit | To samples | Without the meter's counts (byte `+0x18`) |
|---:|---|---|
| 0 | seconds x rate | - |
| 1 | samples | - |
| 2 | x `[+0x24]` | 0.125 s |
| 3 | x `[+0x28]` | 0.5 s |
| 4 | x `[+0x2C]` | 2 s |

The sample count is truncated to a whole number (`007F3321`); on the way out units 2 and 3 divide by the whole
numbers `rate / 8` and `rate / 2` (`007F33CB`, `007F339B`). A unit above 4 gives 0. The music commands `007C92F0` and
`007CC4A0` call it.

## Shipped data

Over the `mtrl` chunks of all 4,609 `.sab` and 116 `.mab` banks:

| Banks | Codec | Materials |
|---|---:|---:|
| `.win.sab` | 7 (HCA) | 9,836 |
| `.win.sab` | 0 | 2 |
| `.orb.sab` (`shout`) | 4 | 1,329 |
| `.mab` | 7 (HCA) | 348 |

The game names its banks with the `.win.sab` suffix (`00908998`), so every material it loads is HCA; the `.orb`
copies use codec 4, which `Voice::Initialize` does not accept. HCA header byte `+0xC` is 0 in all 10,184 HCA materials, so the HCA mixer is
never used; byte `+0xD` is 1 in the 348 music materials and 0 in the rest. 11,374 materials are 48000 Hz and 139 are
44100 Hz; 7,759 are mono and 3,754 stereo.

## Modding notes

- A replacement sound can be 16-bit PCM (codec 1), Microsoft ADPCM (2), Ogg Vorbis (3) or HCA (7); the driver plays
  all four.
- The mix is always 48 kHz in eight channels; a material at another rate is resampled per voice.
- Setting HCA header byte `+0xD` turns on the XOR table `01F41D30` for an in-memory material.
- The driver's messages can be read with a debug-output viewer while the game runs.

## Related

- [Sound banks](sound-banks.md) - the bank files the voices read.
- [Sound engine configuration](sound-engine-config.md) - the start-up file, buses and the `hcam` flag.
- [Sound effects](sound-effects.md) - the play call that posts actions.
- [Sound variations](sound-variations.md) - how a sound picks what to play.
- [Music](music.md) - the music commands.
- [Spatial sound](spatial-sound.md) - the layer thread.
