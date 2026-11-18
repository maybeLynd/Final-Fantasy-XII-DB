[Home](../../README.md) / [Sound and music](README.md) / Sound streaming

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Sound streaming: the streaming banks, their read streams and ring buffers, and how a voice claims, seeks and reads a stream | system | Sound and music | The sound engine | How the sound driver plays a bank that is not held whole in memory: the streaming sound and music banks and the checks that create them, the one to sixteen read streams each bank owns, a stream's read states and ring buffer, how a voice or a music claims a stream, requests a material, seeks into it and reads from it, how a bank is released through the job worker, and the stream object's layout. | 0x007B1AB0, 0x007B1E10, 0x007E2C50, 0x007E2BC0, 0x007E4310, 0x007E3450, 0x007E48D0, 0x007B6C50 |

## What the player sees

- Long sounds, such as spoken lines and music, start playing before their whole file is in memory.
- A streamed sound can start part-way into its file, as music does when it resumes.

## How it works

### Creating a streaming bank

The game hands the driver a buffer it has filled with the start of a bank file. `0x007A4AC0` calls `0x007B1AB0` for a
streaming sound bank and `0x007A4B30` calls `0x007B1E10` for a streaming music bank
([Sound driver objects](sound-driver-objects.md)):

1. A null buffer prints "CreateStreamingBank failed! streaming buffer is NULL" (or "CreateStreamingMusicBank ...").
2. A buffer that overlaps one already used by a streaming bank prints "streamingBuffer already used!!!!" and returns
   `0x83000000`; the check walks the streaming-bank list `0x02EAD490`, comparing with each bank's buffer `+0x88` and
   size `+0x90`.
3. A music bank must ask for 2 to 16 streams (`0x007B1E10`), or it prints "( 2 or more && less than NUM_MAX_STREAMS )
   streams are needed"; a sound bank asks for one (`0x007B1D3F`).
4. It takes a bank block and a kind 1 handle, builds a `StreamingBank` (`0x007E2C50`) and runs its slot 8, which
   (`0x007E32E0`) keeps the buffer and size, refuses a stream count outside 1 to 16 with "StreamingBank::Initialize
   invalid streamCount", and builds one `0xA0`-byte `AudioStream` per stream (`0x007E2BC0`) at `+0xB0`.
5. It adds the bank to the streaming-bank list. `0x007E2CE0` destroys the streams and the bank.

`0x007E2C50` runs the `Bank` base constructor `0x007D07C0` and writes the vtables `0x01CB84E8` at `+0x00`, `0x01CB8548` at
`+0x08` and `0x01CB8568` at `+0x50`, the job object (`0x007E2C5D`-`0x007E2C82`). It sets up the critical section at
`+0x58` (`InitializeCriticalSection`, `0x007E2C86`), zeroes `+0x80`, the buffer `+0x88`, the size `+0x90`, the byte
`+0x94`, `+0x98`, `+0xA0`, the owner `+0xA8` and the 16 stream pointers from `+0xB0` (`0x007E2C8C`-`0x007E2CC7`), and
returns the bank (`0x007E2CCA`).

### A stream's read states

Each stream has its own lock at `+0x08` and a read state at `+0x30`:

| State | Set by | Means |
|---:|---|---|
| `1` | `0x007E4F10`; `0x007E4F70` for each stream of a bank (`0x007E4FEF`) | stopped: material and owner cleared |
| `2` | `0x007E4310` | a material has been requested |
| `3`, `4` | `0x007E3450` | reading the material's chunk header, then its header |
| `5` | `0x007E4410` | marked unused by its owner |
| `6` | `0x007E3450`, `0x007E4310`, `0x007E4DB0`, `0x007E48D0` | ready: the ring buffer holds data |
| `7` | `0x007E3450` (`0x007E3C72`) | from 6, once a fill finds `writePos - readPos + buffered` at `ringSize` or more, or, for a material with no loop region, `+0x6C` at `+0x70` or more (`0x007E3A70`-`0x007E3AA2`, `0x007E3C59`) |
| `8` | `0x007E3450` (`0x007E3CAC`) | idle with its material still loaded: from 5 it empties the ring and clears the start time (`0x007E3C92`-`0x007E3CA5`) |

`0x007E3450` advances a requested stream: in state 2 it empties the ring (`0x007E46D0`) and reads the `mtrl` chunk
header; it then reads the material's header, and once the data is in it sets state 6 and seeks to the start time the
request gave (`0x007E48D0`). `0x007E42F0` answers whether a stream is past state 5. `0x007E4F70` stops every stream of a
bank.

### Requesting and claiming

- `0x007E4310(stream, material, seconds)` requests a material. When the stream already holds that material and is idle
  (state 8) it only seeks there and sets state 6; otherwise, once the bank is ready (`+0x80` = 4), it stores the
  material at `+0x34`, the start time at `+0x88` and sets state 2.
- `0x007E4310` holds the stream's lock `+0x08` throughout (`0x007E4342`, `0x007E43E5`). A material below 0, or not below
  the count of the `mtrl` chunk of the bank's header (bank slot 7, `0x007E4363`; `0x007CF8B0`, `0x007E4366`-`0x007E4383`),
  or a bank that is not ready (`0x007E43BE`) returns -1 and changes nothing; a request returns 0 (`0x007E4333`,
  `0x007E43EB`).
- In the idle case `0x007E4310` seeks (`0x007E48D0`) only when `seconds` is above 0 (`0x007E4393`), and it sets state 6
  either way (`0x007E43A7`).
- `0x007E3040(bank, material)` finds a stream that holds a material and has no owner; in a sound bank whose header byte
  `+0x05` has bit `0x1` set, every material shares stream 0. `0x007E3270` gives a free stream: one with no material, or else
  one in state 8.
- `0x007E4DB0(stream, voice)` gives a stream to a voice when it has no owner (`+0x98`) and wakes an idle stream to state
  6. `0x007E4800(stream, voice)` gives it back through `0x007E4410`, which refuses below state 6 with
  "AudioStream::MarkAsUnused invalid readState_". `0x007E2EB0(bank, voice)` finds the stream a voice owns.
- A music claims the whole bank: `0x007E4D50(bank, music)` sets the bank's owner `+0xA8` when it is free, and
  `0x007E4720(bank, music)` clears it and gives back every stream it owned.

### Reading

The voice feed reads from the ring buffer through:

| Function | Does |
|---|---|
| `0x007E2F40` | the address of the read position: base `+0x40` plus `+0x5C` modulo the ring size `+0x58` |
| `0x007E31B0` | the bytes readable in one piece from there, stopping at the loop mark `+0x60`, the end mark `+0x64` and the ring's end |
| `0x007E4680(stream, n)` | moves the read position on by up to that many bytes |
| `0x007E4860(stream, n)` | lowers the buffered count `+0x4C` by `n`, never below 0, and drops a pending skip `+0x7C` once its countdown `+0x80` runs out |
| `0x007E4210`, `0x007E42A0` | whether the read position has reached the loop mark or the end mark |
| `0x007E4E20`, `0x007E4E40` | set the loop flag `+0x84` while no end mark is set, and at the end mark wrap back into the material's loop region |
| `0x007E4500` | for an Ogg Vorbis material (codec byte `+0x05` = 3), sets the end mark from its extra data once that much is buffered |
| `0x007E2F90` | the share of the ring that is filled: 0 below state 7, and 1.0 once a material without a loop has been read to its end |
| `0x007E3150` | the stream's material header |

A sound's slot 37 (`0x007BD0A0`) asks `0x007E3030`, which gives the fill share of the bank's first stream.

### Seeking

`0x007E48D0(stream, seconds)` turns a time into a byte offset in the material and restarts the ring there (`+0x5C`
and `+0x68` to 0, state 6). A codec it cannot seek prints "SeekData no support format!!! %d"; an Ogg Vorbis
material takes the offset from its seek table and prints "MaterialVorbisExtraData::GetSeekOffset failed!" when there is
no seek offset, and warns that seeking "will cause timing overlap when streaming Ogg vorbis file".

### Releasing a bank

A streaming bank is released on the job worker: `0x007E5040`, unless the bank is already released (`+0x1C`) or its
job is still queued (`0x007B7070`), queues the bank's job object `+0x50` (`0x007B6C50`). Every path then ends in
`0x007D0A70` (`0x007E5090`), which stops the bank's sounds and music only for a bank whose byte `+0x1C` is set
(`0x007D0A76`) and does nothing for the others. `0x007E4260` answers that the bank has finished once it is
released, its use count `+0x18` is 0 or less and its job is done.

`0x007B6C50` puts a job in the 48-entry ring `0x02EAD8B0` with a fresh non-zero id and wakes the
worker (`0x007B6D40`); with the ring full it gives id 0 and returns -1. `0x007B7070(id)` answers whether that job is
running or queued.

`0x007B6C50(id, job)` holds the lock `0x02EAD828` throughout (`0x007B6C60`, `0x007B6D29`). The ring is full when
`posted - taken >= 48` (`0x007B6C6D`-`0x007B6C80`). Each slot is 16 bytes, the id at `+0` and the job at `+8`
(`0x007B6CD5`, `0x007B6CDF`). It writes the id to its first argument (`0x007B6C99`; 0 at `0x007B6C84` when full), signals
the event only while a worker waits (`0x007B6CEA`-`0x007B6CF2`) and returns 0 (`0x007B6D20`).

## Layouts

The read stream, `StreamingBank::AudioStream`, `0xA0` bytes, built by `0x007E2BC0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u8[40]` | lock | its critical section |
| `+0x30` | `i32` | readState | the states above |
| `+0x34` | `i32` | material | the material index, -1 for no material |
| `+0x38` | `u8*` | header | the material's header |
| `+0x40` | `u8*` | ring | the ring buffer |
| `+0x4C` | `i32` | buffered | bytes waiting to be read |
| `+0x58` | `i32` | ringSize | the ring's size in bytes |
| `+0x5C` | `i32` | readPos | the read position, counted from the material's data start |
| `+0x60` | `i32` | loopMark | -1 for no loop mark |
| `+0x64` | `i32` | endMark | -1 for no end mark |
| `+0x68` | `i32` | writePos | the write position |
| `+0x84` | `u8` | loop | 1 from `0x007E2BC0`; set by `0x007E4E20` |
| `+0x88` | `f64` | startTime | seconds to seek to once ready |
| `+0x90` | `StreamingBank*` | bank | the bank it belongs to |
| `+0x98` | `void*` | owner | the voice reading it, or 0 |

`0x007E2BC0(stream, bank)` writes the vtable `0x01CB84D8` at `+0x00` (`0x007E2BD4`), sets up the lock
(`InitializeCriticalSection`, `0x007E2BDE`) and stores the bank at `+0x90` (`0x007E2BE6`). It sets the read state 0,
the material -1, both marks -1 and the loop byte 1 (`0x007E2BF2`, `0x007E2C25`, `0x007E2C2C`, `0x007E2C34`), zeroes
`+0x38`-`+0x5F`, `+0x68`-`+0x83`, the byte `+0x85` and the owner `+0x98` (`0x007E2BF5`-`0x007E2C1B`, `0x007E2C34`), and
returns the stream; `startTime` `+0x88` is not written.

## State

### The streaming-bank list

The list at `0x02EAD490` is an `ObjectList` ([Sound driver objects](sound-driver-objects.md)): `0x00169B10` sets it up
at start-up and `0x008B89A0` takes it down at exit, `0x007B2700` builds its nodes (`0x007B2600`, `0x007B2854`), the bank
creators add a bank at the front (`0x007AF380`, from `0x007B1DB6` and `0x007B216C`) and the update pass `0x007B2920` takes a
finished bank out (`0x007B2880`, from `0x007B2A12`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAD498` | `i32` | 0 | list `+0x08`, capacity: the nodes the list holds | `0x00169B10`, 0 with `+0x0C` (`0x00169B2D`); through the address: `0x007B2600` (`0x007B2665`), from `0x007B2700` | through the address: `0x007B6AA0` (`0x007B6AB1`, `0x007B6AE6`), from `0x007B2600` (`0x007B26DC`); `0x007B2880` (`0x007B2888`), from `0x007B2920` |
| `0x02EAD49C` | `i32` | 0 | list `+0x0C`, nodes in use | `0x00169B10` (`0x00169B2D`); `0x008B89A0`, 0 (`0x008B89DD`); through the address: `0x007B2600` (`0x007B2651`) with `0x007B6AA0` (`0x007B6AF5`), from `0x007B2700`; `0x007AF380` (`0x007AF459`), from `0x007B1AB0` and `0x007B1E10`; `0x007B2880` (`0x007B2908`), from `0x007B2920` | through the address: `0x007AF380` (`0x007AF459`); `0x007B2880` (`0x007B2908`) |
| `0x02EAD4A0` | `void*` | 0 | list `+0x10`, the `DriverListNode` array | `0x00169B10` (`0x00169B34`); `0x008B89A0`, 0 after freeing it (`0x008B89F1`); through the address: `0x007B2600` (`0x007B2641`, `0x007B26D5`), from `0x007B2700` | `0x008B89A0`, which frees it at exit (`0x008B89A4`); through the address: `0x007B2600` (`0x007B2615`) with `0x007B6AA0` (`0x007B6AA0`, `0x007B6AC0`, `0x007B6AC9`), from `0x007B2700`; `0x007B2880` (`0x007B2898`), from `0x007B2920` |
| `0x02EAD4B0` | `void*` | 0 | list `+0x20`, the first node in use; each node holds its bank at `+0x20` and the next node at `+0x10` | `0x00169B10` (`0x00169B3C`); `0x008B89A0` (`0x008B8A00`); through the address: `0x007B2600` (from `0x007B2700`), `0x007AF380` (from `0x007B1AB0`, `0x007B1E10`), `0x007B2880` (from `0x007B2920`) | `0x007B1AB0` (`0x007B1B62`) and `0x007B1E10` (`0x007B1EE7`), which walk the banks for an overlapping buffer; `0x007B2920` (`0x007B29E5`), which finds the node of the bank it retires |

### The job ring

`0x007B6C50` and the worker `0x007B6D40` share the ring `0x02EAD8B0` under the lock `0x02EAD828`. They count jobs posted and
taken in two words and use the slot `count mod 48` (`0x007B6C9B`-`0x007B6CDF`, `0x007B6D99`-`0x007B6DCB`); when the taken
count `0x02EAD894` and the posted count `0x02EAD898` have both reached 48, `taken >= 48 && posted >= 48`, the worker
reduces each to its remainder mod 48, `taken % 48` and `posted % 48` (`0x007B6DD2`-`0x007B6E21`); while either is below
48 it leaves both as they are (`0x007B6DD6`, `0x007B6DDC`).

The worker sleeps on a
manual-reset event guarded by the lock `0x02EAD850`: it registers as a waiter, waits until a post has raised the
generation and released waiters remain, and the last released waiter resets the event (`0x007B6E66`-`0x007B6F30`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAD858`, `0x02EAD860`, `0x02EAD868`, `0x02EAD870` | `u8[8]` each | 0 | bytes `+0x08`-`+0x27` of the event's lock `0x02EAD850`, a Windows critical section (`InitializeCriticalSection`, import `0x008C20B0`), whose state Windows keeps there | `0x00169E90`, 0 (`0x00169EA4`, `0x00169EAB`, `0x00169EB2`, `0x00169EB9`), then `InitializeCriticalSection` through the address (`0x00169ED5`); `EnterCriticalSection` and `LeaveCriticalSection` (`0x008C20B8`, `0x008C20C0`) through the address, from `0x007B6C50` (`0x007B6CE4`, `0x007B6D1A`) and `0x007B6D40` (`0x007B6E6D`, `0x007B6E86`, `0x007B6EB7`, `0x007B6EDE`, `0x007B6EFC`, `0x007B6F1F`); `DeleteCriticalSection` (`0x008C20D0`) from `0x008B8D40` at exit (`0x008B8D5C`) | only those Windows calls, through the address |
| `0x02EAD878` | `void*` | 0 | the event's handle, `CreateEventW` with manual reset, not signalled | `0x00169E90`, 0 and then the handle (`0x00169EC0`, `0x00169F07`) | `0x007B6C50`, `SetEvent` (`0x007B6CF4`); `0x007B6D40`, `WaitForSingleObject` and `ResetEvent` (`0x007B6EA0`, `0x007B6F29`); `0x008B8D40`, `CloseHandle` at exit (`0x008B8D44`) |
| `0x02EAD880` | `i32` | 0 | the waiters on the event | `0x00169E90` (`0x00169EC7`, `0x00169EE0`); `0x007B6D40`, 1 more before the wait and 1 less after (`0x007B6E73`, `0x007B6F02`) | `0x007B6C50`, which signals only when it is above 0 (`0x007B6CEA`, `0x007B6D01`) |
| `0x02EAD884` | `i32` | 0 | the waiters the last signal releases: a post sets it to the waiter count, each released waiter takes 1, and the one that brings it to 0 resets the event | `0x00169E90` (`0x00169EC7`, `0x00169EE9`); `0x007B6C50` (`0x007B6D07`); `0x007B6D40` (`0x007B6F0F`) | `0x007B6D40` (`0x007B6EBD`, `0x007B6F16`) |
| `0x02EAD888` | `i32` | 0 | the signal generation, 1 more on each post that signals; a waiter leaves only when it differs from the value it saw on arrival | `0x00169E90` (`0x00169ECE`, `0x00169EF1`); `0x007B6C50` (`0x007B6D0D`) | `0x007B6D40` (`0x007B6E80`, `0x007B6EC7`) |
| `0x02EAD894` | `i32` | 0 | the jobs taken | `0x007B6D40` (`0x007B6DB1`, `0x007B6E21`); `0x007B6F70`, 0 (`0x007B6FB0`) | `0x007B6C50` (`0x007B6C77`); `0x007B6D40` (`0x007B6D87`); `0x007B7070` (`0x007B7099`) |
| `0x02EAD898` | `i32` | 0 | the jobs posted; the ring is full at 48 more than the jobs taken | `0x007B6C50` (`0x007B6CB9`); `0x007B6D40` (`0x007B6E1A`); `0x007B6F70`, 0 (`0x007B6FC2`) | `0x007B6C50` (`0x007B6C6D`); `0x007B6D40` (`0x007B6D7D`); `0x007B7070` (`0x007B709F`) |
| `0x02EAD89C` | `i32` | 0 | the last job id given; the next is 1 more, skipping 0 (`0x007B6C8E`-`0x007B6CA3`) | `0x007B6C50` (`0x007B6CA3`); `0x007B6F70`, 0 (`0x007B6FCA`) | `0x007B6C50` (`0x007B6C8E`) |

No other instruction reaches these globals.

## Modding notes

- A streaming music bank can carry at most 16 streams; each layer of a music that plays at the same time needs its
  own.
- Ogg Vorbis materials can be streamed, but a seek into one may overlap its timing; HCA materials seek exactly.

## Related

- [Sound driver objects](sound-driver-objects.md) - the bank handles and the update pass.
- [Sound engine](sound-engine.md) - the voice feed that reads the streams.
- [Interactive music](interactive-music.md) - music banks and their streams.
- [Voices](voices.md) - the spoken lines the game streams.
