---
title: "Sound streaming: the streaming banks, their read streams and ring buffers, and how a voice claims, seeks and reads a stream"
kind: "system"
category: "Sound and music"
addresses: "007B1AB0, 007B1E10, 007E2C50, 007E2BC0, 007E4310, 007E3450, 007E48D0, 007B6C50"
---

## What the player sees

- Long sounds, such as spoken lines and music, start playing before their whole file is in memory.
- A streamed sound can start part-way into its file, as music does when it resumes.

## How it works

### Creating a streaming bank

The game hands the driver a buffer it has filled with the start of a bank file. `007A4AC0` calls `007B1AB0` for a
streaming sound bank and `007A4B30` calls `007B1E10` for a streaming music bank
([Sound driver objects](sound-driver-objects.md)):

1. A null buffer prints "CreateStreamingBank failed! streaming buffer is NULL" (or "CreateStreamingMusicBank ...").
2. A buffer that overlaps one already used by a streaming bank prints "streamingBuffer already used!!!!" and returns
   `0x83000000`; the check walks the streaming-bank list `02EAD490`, comparing with each bank's buffer `+0x88` and
   size `+0x90`.
3. A music bank must ask for 2 to 16 streams (`007B1E10`), or it prints "( 2 or more && less than NUM_MAX_STREAMS )
   streams are needed"; a sound bank asks for one (`007B1D3F`).
4. It takes a bank block and a kind 1 handle, builds a `StreamingBank` (`007E2C50`) and runs its slot 8, which
   (`007E32E0`) keeps the buffer and size, refuses a stream count outside 1 to 16 with "StreamingBank::Initialize
   invalid streamCount", and builds one `0xA0`-byte `AudioStream` per stream (`007E2BC0`) at `+0xB0`.
5. It adds the bank to the streaming-bank list. `007E2CE0` destroys the streams and the bank.

### A stream's read states

Each stream has its own lock at `+0x08` and a read state at `+0x30`:

| State | Set by | Means |
|---:|---|---|
| `1` | `007E4F10` | stopped: material and owner cleared |
| `2` | `007E4310` | a material has been requested |
| `3`, `4` | `007E3450` | reading the material's chunk header, then its header |
| `5` | `007E4410` | marked unused by its owner |
| `6` | `007E3450`, `007E4310`, `007E4DB0` | ready: the ring buffer holds data |
| `8` | | idle with its material still loaded |

`007E3450` advances a requested stream: in state 2 it empties the ring (`007E46D0`) and reads the `mtrl` chunk
header; it then reads the material's header, and once the data is in it sets state 6 and seeks to the start time the
request gave (`007E48D0`). `007E42F0` answers whether a stream is past state 5. `007E4F70` stops every stream of a
bank.

### Requesting and claiming

- `007E4310(stream, material, seconds)` requests a material. When the stream already holds that material and is idle
  (state 8) it only seeks there and sets state 6; otherwise, once the bank is ready (`+0x80` = 4), it stores the
  material at `+0x34`, the start time at `+0x88` and sets state 2.
- `007E3040(bank, material)` finds a stream that holds a material and has no owner; in a sound bank whose header byte
  `+0x05` has bit 0 set, every material shares stream 0. `007E3270` gives a free stream: one with no material, or else
  one in state 8.
- `007E4DB0(stream, voice)` gives a stream to a voice when it has no owner (`+0x98`) and wakes an idle stream to state
  6. `007E4800(stream, voice)` gives it back through `007E4410`, which refuses below state 6 with
  "AudioStream::MarkAsUnused invalid readState_". `007E2EB0(bank, voice)` finds the stream a voice owns.
- A music claims the whole bank: `007E4D50(bank, music)` sets the bank's owner `+0xA8` when it is free, and
  `007E4720(bank, music)` clears it and gives back every stream it owned.

### Reading

The voice feed reads from the ring buffer through:

| Function | Does |
|---|---|
| `007E2F40` | the address of the read position: base `+0x40` plus `+0x5C` modulo the ring size `+0x58` |
| `007E31B0` | the bytes readable in one piece from there, stopping at the loop mark `+0x60`, the end mark `+0x64` and the ring's end |
| `007E4680(stream, n)` | moves the read position on by up to that many bytes |
| `007E4860(stream, n)` | lowers the buffered count `+0x4C` by `n`, never below 0, and drops a pending skip `+0x7C` once its countdown `+0x80` runs out |
| `007E4210`, `007E42A0` | whether the read position has reached the loop mark or the end mark |
| `007E4E20`, `007E4E40` | set the loop flag `+0x84` while no end mark is set, and at the end mark wrap back into the material's loop region |
| `007E4500` | for an Ogg Vorbis material (codec byte `+0x05` = 3), sets the end mark from its extra data once that much is buffered |
| `007E2F90` | the share of the ring that is filled: 0 below state 7, and 1.0 once a material without a loop has been read to its end |
| `007E3150` | the stream's material header |

A sound's slot 37 (`007BD0A0`) asks `007E3030`, which gives the fill share of the bank's first stream.

### Seeking

`007E48D0(stream, seconds)` turns a time into a byte offset in the material and restarts the ring there (`+0x5C`
and `+0x68` to 0, state 6). A codec it cannot seek prints "SeekData no support format!!! %d"; an Ogg Vorbis
material takes the offset from its seek table and prints "MaterialVorbisExtraData::GetSeekOffset failed!" when there is
none, and warns that seeking "will cause timing overlap when streaming Ogg vorbis file".

### Releasing a bank

A streaming bank is released on the job worker: `007E5040`, unless the bank is already released (`+0x1C`) or its job is
still queued (`007B7070`), queues the bank's job object `+0x50` (`007B6C50`) and stops the bank's sounds and music
(`007D0A70`). `007E4260` answers that the bank has finished once it is released, its use count `+0x18` is 0 or less
and its job is done. `007B6C50` puts a job in the 48-entry ring `02EAD8B0` with a fresh non-zero id and wakes the
worker (`007B6D40`); with the ring full it gives id 0 and returns -1. `007B7070(id)` answers whether that job is
running or queued.

## Layouts

The read stream, `StreamingBank::AudioStream`, `0xA0` bytes, built by `007E2BC0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `08` | `u8[40]` | lock | its critical section |
| `30` | `i32` | readState | the states above |
| `34` | `i32` | material | the material index, -1 for none |
| `38` | `u8*` | header | the material's header |
| `40` | `u8*` | ring | the ring buffer |
| `4C` | `i32` | buffered | bytes waiting to be read |
| `58` | `i32` | ringSize | the ring's size in bytes |
| `5C` | `i32` | readPos | the read position, counted from the material's data start |
| `60` | `i32` | loopMark | -1 for none |
| `64` | `i32` | endMark | -1 for none |
| `68` | `i32` | writePos | the write position |
| `84` | `u8` | loop | 1 from `007E2BC0`; set by `007E4E20` |
| `88` | `f64` | startTime | seconds to seek to once ready |
| `90` | `StreamingBank*` | bank | the bank it belongs to |
| `98` | `void*` | owner | the voice reading it, or 0 |

## Modding notes

- A streaming music bank can carry at most 16 streams; each layer of a music that plays at the same time needs its
  own.
- Ogg Vorbis materials can be streamed, but a seek into one may overlap its timing; HCA materials seek exactly.

## Related

- [Sound driver objects](sound-driver-objects.md) - the bank handles and the update pass.
- [Sound engine](sound-engine.md) - the voice feed that reads the streams.
- [Interactive music](interactive-music.md) - music banks and their streams.
- [Voices](voices.md) - the spoken lines the game streams.
