---
title: "Sound driver objects: the handles, fixed pools and calls through which the game creates, finds, commands and queries banks, sounds and music"
kind: "system"
category: "Sound and music"
addresses: "0x007B2CB0, 0x007B1660, 0x007B72B0, 0x007B2200, 0x007A87C0, 0x007A7010, 0x007A9160, 0x007DF790"
---

## What the player sees

- Nothing directly: every sound effect, voice line and music track the game plays is one of these driver objects.
- The number of sounds, music tracks and banks that can exist at once is fixed when the game starts.

## How it works

### Handles

The driver gives every object it creates an eight-byte handle, and every call names an object by its handle:

| Bytes | Holds |
|---|---|
| `0` | the object's kind |
| `2`-`3` | the object's slot in its pool's list |
| `4`-`7` | a serial number, one more than the last one given to that kind |

`0x007B2CB0` writes all three for a sound (`0x007B2E49`-`0x007B2E4F`), `0x007B1660` for a bank, `0x007B5690` for a track,
`0x007B5D20` for a voice and `0x007B72B0` for a music. A lookup takes the slot, checks it is live (bit 0 of the list node's
`+0x1C`) and compares the whole handle with the object's own copy, so a handle of an object that has ended finds
nothing:

| Kind | Object | Lookup | Its copy of the handle |
|---:|---|---|---|
| `1` | `Bank` | `0x007B2470` | `+0x10` |
| `2` | `Sound` | `0x007B44C0` | slot 22, `0x007BD5D0` (`+0x18`) |
| `3` | `Sequence` | `0x007B5070` | `0x007E71B0` |
| `4` | `Track` | `0x007B58C0` | `+0x08` |
| `5` | `Voice` | `0x007B5E50` | `+0x40` |
| `7` | `Lay` source | `0x007BC2B0` | `+0x08` |
| `8` | `Magi::Music` | `0x007B77E0` | slot 22 |
| `9` | `Magi::Instrument` | `0x007B7FD0` | slot 22 |

`0x007A9160` turns a kind 7 handle into the driver handle its `Lay` source plays (source slot 4) and passes a kind 8
handle through; the music calls below use it, so they accept either. The handle helpers `0x007A4380` (-1), `0x007A5F10`
(0), `0x007A46E0`, `0x007A4C40`, `0x007A4C70`, `0x007A47A0`, `0x007A9060` and `0x007A9080` build or copy a handle value, and
`0x007A59E0`, `0x007A59F0`, `0x007A5B20`, `0x007A5B00` and `0x007A5660` do the same for the four-byte `Lay` handles.

### Pools and lists

`0x007A4D50` builds every pool when the driver starts. A pool is a fixed-block heap (`0x007DF790` builds it, `0x007DF750`
takes a block, `0x007DF8D0` gives one back, `0x007DF910` gives a block's index, `0x007DF890` frees it), and each kind has
a list of `0x28`-byte nodes that its handles index:

| Objects | Builder | Block | Count | List |
|---|---|---:|---:|---|
| banks | `0x007B2700` | `0x158` | 1,024 | the bank lists at `0x02EAD410`, one in the shipped start-up block (`0x007B2500`), and the streaming-bank list (`0x007B2600`) |
| sounds | `0x007B4770` | `0x540` | 92 | `0x02EAD540` and `0x02EAD570` (`0x007B4670`); torn down by `0x007B4840` |
| sequences | `0x007B51F0` | `0xC8` | 184 | `0x02EAD600` (`0x007B50F0`) |
| tracks | `0x007B5A00` | `0x3D0` | 184 | `0x02EAD690` (`0x007B5900`) |
| voices | `0x007B5F90` | `0x470` | 128 | `0x02EAD720` (`0x007B5E90`) |
| events | `0x007B67E0` | `0x38` | 64 | `0x02EAD7E0` (`0x007B66E0`); torn down by `0x007B69C0` |
| music | `0x007B7C10` | `0x8D8` | 8 | `0x02EADC10` (`0x007B7B00`) |
| instruments | `0x007B8170` | `0x208` | 32 | `0x02EADCD0` (`0x007B8060`); never built in the shipped game (below) |

The counts are the shipped ones: the sound count is the categories' sum plus 32 and the sequences and tracks twice
that (`0x007A4ECC`, `0x007A4ED7`), the voice count is the three start-up counts of
[Sound engine configuration](sound-engine-config.md), the bank and event counts come from the start-up block
`0x00210760` fills (`0x400`, `0x40`), and the music and instrument counts are constants of their builders. `0x007B6AA0`
links a fresh list's nodes into its free chain.

The instrument pool is never built in the shipped game. The driver start `0x007A4D50` calls the instrument builder
`0x007B8170` only when start-up block `+0x28` is not 0 (`0x007A519B`-`0x007A51A0`), and `0x00210760` stores 0 there: its
8-byte store at `0x00210831` writes `0x20` to `+0x24` and 0 to `+0x28`. So the instrument pool and list stay empty, the
flag `0x02EADC74` that only the builder sets (`0x007B8209`) stays 0, and `0x007B8220` answers 0.

`0x007AF380` puts a node at the front of a list and `0x007B5580` at the
back; both print "list append error full!" when no node is free. `0x007B2880` takes a node out, and `0x007B14C0` empties a bank list.

### Finding by number

Banks and sounds are also kept in hash tables of 257 buckets (`0x007E27B0`): banks at `0x01F40440`, sounds at
`0x01F40C50`. `0x007E2880` adds an object, `0x007E2910` removes it and `0x007E27F0` moves a found one to the front of its
bucket.

- `0x007B2200(id)` finds the bank whose number is the id's high 16 bits, in bucket `(id >> 16) % 257`
  (`0x007B2251`); a bank with a sound table must also hold the id's low 16 bits as a sound number.
- `0x007B4540(id)` finds a playing sound by its sound number and its bank's number; `0x007B7860(id)` does the same for a
  music.
- `0x007A4CA0(out, id)` gives the handle of the playing sound or music with that id, by the bank's content type
  `+0x48`: 1 for a sound bank, 2 for a music bank.
- `0x007A4BB0(out, id)` gives the handle of the bank that holds the id, under the bank lock (`0x007B24F0`).

### Creating a bank

`0x007A48C0` (from the game's bank loaders `0x00222F20`, `0x00223DA0` and `0x00224C40`) calls `0x007B1660`:

1. It checks the data's tag: `sabf` (`0x007CFF90`) makes a sound bank; `mabf` (`0x007D07A0`) goes to `0x007B18A0`, which
   makes a music bank the same way.
2. It takes a bank block and a node in the least-filled bank list, and writes a kind 1 handle.
3. It builds an `OnMemoryBank` (`0x007E29C0`, over the `Bank` base `0x007D07C0`) and runs its slot 8 with the data and
   the content type, 1 or 2.
4. It adds the bank to the hash table. On failure it gives back the node and the block.

`0x007A4AC0` and `0x007A4B30` do the same for a streaming sound bank (`0x007B1AB0`) and a streaming music bank
(`0x007B1E10`), described on [Sound streaming](sound-streaming.md). `0x007A88F0(bank, nowait)` releases a bank through
`0x007D0A10`; with `nowait` 0 it then sleeps 1 ms at a time until the handle finds nothing. `0x007A8CA0` answers whether a
bank handle still finds its bank, `0x007A89F0` gives its content type, and `0x007A8C30` gives its readiness: slot 3 for
a sound bank and slot 4 for a music bank.

A bank counts its users at `+0x18`: `0x007D0890` adds one and `0x007D0A00`
takes one away, both atomically; `0x007D0810` puts back the base vtables when a bank is destroyed.

### Creating a sound or a music

`0x007A87C0(bank, out, id, ...)` (from `0x00221C70`, `0x007A4A10` and the `Lay` tick `0x007F0820`) looks the bank up and
calls `0x007D0940` for a sound bank or `0x007D08F0` for a music bank; `0x007A86E0` takes only a music bank. `0x007A4A10(out,
id)` first finds the bank by number and asks for the sound with bit 30 set, meaning a sound number rather than an
index (`0x007A4A7C`).

1. `0x007B2CB0` takes a `0x540` block and a node in the sound list; with no block it prints "sound heap empty. could
   not create sound", with no node "using list full. could not create sound".
2. It writes a kind 2 handle with the next serial (`0x02EAD4C4`) and builds the object through the factory `0x007B2F70`
   ([Sound variations](sound-variations.md)).
3. It records the object in its node and, unless the object is waiting for its bank (slot 38), adds it to the sound
   hash table.

`0x007B72B0` does the same for a music through `0x007B7460`. That checks the music number against the bank's count
("music number is out of range"), resolves a number with bit 30 set through `0x007A8EA0`, and adds the music's track
need to `0x02EADBB0`: `0x007B7960` counts it from the music's sections and mode transitions in an in-memory bank, and a
streaming bank gives its stream count `+0x94`. Over the budget `0x02EADBB4`, 32, it prints "track count exceeded
numMusicTracks" and goes on.

### Reading a sound's header

`0x007A8A50(bank, out, id)` copies one sound's or music's header into an info record, fields `+0x100` to `+0x11C`, without playing it: an id
with bit 30 set is a number, found by `0x007A8F40` in a sound bank or `0x007A8EA0` in a music bank. `0x007A6C10` fills the
record from a sound header and `0x007A6AC0` from a music header, reading each field only when the header's version byte
is new enough; `0x007A6990` fills it from an instrument. `0x007A6DB0(handle, out)` fills the same record for a playing
object of kind 2, 8 or 9.

### Posting a command

`0x007AB390` builds 1,024 actions of `0x28` bytes at `0x02EAD0A0` and the two queues `0x02EAD010` and `0x02EAD040`
(`0x007AB240`), and puts every action on the first. Every call that changes a playing object takes an action from the
queue (`0x007AB460`), fills it and appends it (`0x007AB550`); a call on a `Lay` source posts to the `Lay` queue instead (`0x007BAD60`, `0x007BAE50`). A call returns
`0x82000000` for a zero handle and -1 for a handle of the wrong kind. Types `0x0B`-`0x1B` run a `Sound` method on
the driver thread (`0x007AB5C0`):

| Call | Kinds | Type | `Lay` type | Runs |
|---|---|---:|---:|---|
| `0x007A7F70` | 2, 8 | `0x0F` | `0x0B` | slot 8, pitch |
| `0x007A7E90` | 2, 8, 9 | `0x10` | | slot 9, panning (four values) |
| `0x007A8390` | 2, 8 | `0x11` | `0x0C` | slot 18 (`0x007BECD0`): ramps one of the `0x30`-byte values at `+0x248` |
| `0x007A7E00` | 2, 8, 9 | `0x12` | | slot 10 (`0x007BE510`): sets bit 0 of `+0x518` and writes 1 and 5.0 at `+0x1DC`, `+0x20C` and `+0x23C`; 0 clears them |
| `0x007A8300` | 2, 8, 9 | `0x13` | | slot 11 (`0x007BEC70`): sets bit 1 of `+0x518` and writes 1 and 5.0 at `+0xAC`; 0 clears them |
| `0x007A7CC0` | 2, 8, 9 | `0x14` | | slot 12 (`0x007BE3E0`): stores a byte at `+0x3F8` |
| `0x007A7D50` | 2, 8, 9 | `0x15` | | slot 13, low-pass |
| `0x007A7C30` | 2, 8, 9 | `0x16` | | slot 14 (`0x007BE3D0`): stores `+0x508` |
| `0x007A7B10` | 2, 8, 9 | `0x17` | | slot 15 (`0x007BE360`): stores `+0x50C` |
| `0x007A7BA0` | 2, 8, 9 | `0x18` | | slot 16 (`0x007BE3C0`): stores `+0x510` |
| `0x007A8120` | 2, 9 | `0x19` | `0x0E` | slot 17 (`0x007BEAE0`): stores `+0x514` |
| `0x007A77F0` | 7 | | `0x08` | the source's slot 15 with three values: moves it |
| `0x007A8060` | 7 | | `0x07` | the source's slot 14 with three values |

The slot numbers are those of the `Driver::Sound` vtable `0x01CB5A30`; types `0x0B`-`0x0E` (stop, pause, resume,
volume) are on [Sound engine](sound-engine.md). The other posters:

| Call | Type | Does |
|---|---:|---|
| `0x007A4660`, `0x007A4390`, `0x007A4530`, `0x007A45C0` | `0x01`, `0x02`, `0x04`, `0x03` | pause, resume, pitch ramp and volume ramp of a category |
| `0x007A44A0`, `0x007A4410` | `0x07`, `0x08` | store two bytes in a category, at `+0x80` (`0x007AA4E0`) or `+0x82` (`0x007AA4D0`) |
| `0x007A8FE0` | `0x09` | stops every sound, music and instrument of a bank: `0x007D0A20` runs `0x007B4960`, `0x007B7CC0` and `0x007B8230`, which stop each object whose bank (`0x007BD8D0` for a sound) is that one |
| `0x007A93A0` | `0x1C`, or `Lay` 6 | plays a music, or a `Lay` source |
| `0x007A9550`, `0x007A94D0`, `0x007A92C0`, `0x007A9650`, `0x007A95D0`, `0x007A90E0` | `0x1D`, `0x21`, `0x23`, `0x26`, `0x27`, `0x28` | music commands ([Interactive music](interactive-music.md)) |
| `0x007A46F0` | `0x2E` | a mixer bus value; `0x007A47A0` packs the bus and parameter |
| `0x007A5300` | `0x30` | applies an effect preset |
| `0x007A5380` | `0x32` | copies a name into the driver's name buffer (`0x007AE470`) and posts it |
| `0x007A58D0`, `0x007A5670` | `Lay` 1, 2 | a placed request and the listener ([Spatial sound](spatial-sound.md)) |

The category calls reach `0x007AA680`, which pauses every sound, music and instrument of the category only when its
pause count `+0x64` goes from 0 to 1, and `0x007AA3E0`, which resumes them only while the count is 1 and then lowers it, never below 0.

### Reading an object back

The queries look the object up under its kind's lock and ask it through a vtable slot; a `Lay` source answers through
its own slot:

| Query | Sound, music, instrument (slot) | `Lay` source (slot) |
|---|---|---|
| `0x007A7010` | the state, slot 21 (`0x007BD9A0`), as 0, 1, 2 or 3 (3 for state 4) | slot 2 |
| `0x007A67D0` | slot 28, three values (`0x007BD6F0`) | slot 26 |
| `0x007A71F0` | the switch value (`0x007BD9D0`; `0x007CEF00` for an instrument) | slot 24 |
| `0x007A7350` | slot 26 (`0x007BDBB0`) | slot 18 |
| `0x007A74D0` | slot 30, bit 1 of `+0x518` | slot 29 |
| `0x007A6600` | slot 29, bit 0 of `+0x518` | slot 28 |
| `0x007A5FB0` | slot 31, `+0x508` | slot 32 |
| `0x007A76A0` | slot 34 with an index; for a sound `0x007BDD20`, the value of one ramp of `+0x248` | slot 22 |
| `0x007A6130` | `+0x504` of a sound | slot 27 |
| `0x007A6260` | a byte: `0x007BD5B0`, `0x007C5C70`, or an instrument's `+0x204` | slot 30 |
| `0x007A6470` | 1.0 by default: `0x007BD680`, `0x007C5F70` or `0x007CEE80` | slot 31 |

`0x007A91D0` gives a music's play position in seconds (`0x007C6490`) and `0x007A9250` its `+0x650`. The game's bank
classes call `0x007A7010` to ask whether a sound plays ([Audio manager](audio-manager.md)).

### The update passes

The driver thread `0x007A5400` measures the time since its last pass in seconds and runs, in this order:

1. `0x007B1380`, which advances the external-parameter ramps.
2. `0x007B6B00`, which runs each event (`0x007EEA00`) and frees it once its state `+0x08` is 2.
3. The command queue (`0x007AB5C0`), then the master ramps (`0x007AAEA0`).
4. `0x007B2920`, one bank list per pass in turn (`0x02EAD408`), running each bank's slot 10 and retiring a bank once its
   slot 2 answers true: it leaves its lists and the hash table, runs slot 9 and is freed.
5. `0x007B4A70`, every sound: its update (slot 42), and in state 3 it is removed and freed. A sound that was waiting for
   its bank is rebuilt by the factory once the bank is ready, and `0x007BFFA0` carries its settings over.
6. `0x007B52B0` (sequences, freed in state 4), `0x007B5AD0` (tracks, freed in state 5), `0x007B7D60` (music, freed in
   state 7, giving back its track need) and, while instruments exist (`0x007B8220`), `0x007B82D0` (freed in state 7);
   in the shipped game no instrument exists, so `0x007B82D0` does not run.
7. `0x007B6050` (voices, freed in state 3) and `0x007B99B0` (external sources), then the bus ramps (`0x007AD310`).
8. `Sleep(10)` (`0x007A5521`).

The driver's threads start through `0x007A5550`, which calls the function at `+0x08` of its block with the argument at
`+0x10`.

A list walk that meets an empty node prints "sequence NULL!!" and its neighbours (`0x007B4FC0`).

### Ramps

A ramped value holds a start, a target, the time so far and a duration; `0x007A9E00` gives its current value as
`start + curve(time / duration) x (target - start)`, through the curve `0x007A9E50`, or the target once the duration is
0. Category, bus and sound volumes, pitches and pans are all such ramps. `0x007BDAC0` gives a curved ramp's value: with a
curve at `+0x38` the configuration curve shapes it (`0x007AE260`), run backwards when the target is below the start.

### Heap and clock

`0x007AD620` stores the allocate and free functions from the start-up block. `0x007AD550(size, tag)` allocates
`size + 16` bytes with a header of `0x5EAD5EAD`, the tag and the size; `0x007AD4D0` also zeroes the block and
`0x007AD5A0` grows one by copying.

The engine start points the Vorbis decoder's allocation hooks at this heap
(`0x007A4E3E`-`0x007A4E6B`): `0x01F41CF8` (malloc) at `0x007A52E0`, `0x01F41D00` (calloc) at `0x007A52C0`, `0x01F41D08` (realloc)
at `0x007A52F0`, each passing tag 5 to `0x007AD550`, `0x007AD4D0` or `0x007AD5A0`, and the free hook at `0x007A52D0`, a jump to
`0x007AD540` ([Media decoder libraries](../Third-Party-Libraries/media-decoder-libraries.md)).

`0x007AD6D0` reads the performance-counter frequency and start; `0x007AD630` gives counts
since the start and `0x007AD680` microseconds, which seed `srand` (`0x007A5404`).

## Layouts

Every pool's list is an `ObjectList` of `DriverListNode`s, and the command queues are `DriverQueue`s. The offsets are
those of the sequence list `0x02EAD600` and its helpers; the other lists and queues use the same code.

`ObjectList` (`0x30` bytes, offsets from the start of the list):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | the list's class, set by its static initialiser (`0x00169C9A`); its exit handler puts back `0x01CB4470` (`0x008B8B89`) |
| `+0x08` | `i32` | capacity | the nodes the list holds, set by its builder (`0x007B5155`); every lookup bounds the slot with it (`0x007B5088`) |
| `+0x0C` | `i32` | used | nodes in use: an append raises it (`0x007AF459`, `0x007B565C`), `0x007B2880` lowers it (`0x007B2908`), `0x007B6AA0` clears it (`0x007B6AF5`) |
| `+0x10` | `void*` | nodes | the DriverListNode array, allocated by the builder through `0x007AD460` with its count before it (`0x007B518B`) |
| `+0x18` | `void*` | free | first free node; `0x007B6AA0` chains every node into it (`0x007B6AAA`), an append takes the first (`0x007AF41A`) |
| `+0x20` | `void*` | first | first node in use (`0x007AF42A`, `0x007B562B`) |
| `+0x28` | `void*` | last | last node in use (`0x007AF426`, `0x007B564F`) |

`DriverListNode` (`0x28` bytes, offsets from the start of the node):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | the node class, `0x01CB4D98` for the sequence list (`0x007B51A1`) |
| `+0x08` | `void*` | prev | previous node (`0x007B6AD0`, `0x007AF448`) |
| `+0x10` | `void*` | next | next node, in the free chain or in the list (`0x007B6AD9`, `0x007AF440`) |
| `+0x18` | `i32` | slot | the node's index, which a handle carries in its bytes 2-3 (`0x007B6AC4`); -1 until the chain is built (`0x007B51AC`) |
| `+0x1C` | `u32` | flags | bit 0 set while the node holds an object: set by an append (`0x007AF450`), cleared by `0x007B2880` (`0x007B28EA`), tested by every lookup (`0x007B50A0`) |
| `+0x20` | `void*` | object | the object in the slot, stored by an append (`0x007AF455`) and returned by the lookups (`0x007B50A7`) |

`DriverQueue` (`0x30` bytes, offsets from the start of the queue):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | the queue class, set by its static initialiser; its exit handler puts back `0x01CB4470` (`0x008B8779`) |
| `+0x08` | `void*` | cells | the cells, `0x18` bytes each: class `0x01CB45D8`, the queued pointer at +`0x08` and the next cell at +`0x10` (`0x007AB2FE`-`0x007AB317`) |
| `+0x10` | `void*` | free | first free cell (`0x007AB336`) |
| `+0x18` | `void*` | first | first queued cell (`0x007AB371`) |
| `+0x20` | `void*` | last | last queued cell (`0x007AB377`) |
| `+0x28` | `i32` | capacity | cells (`0x007AB2B0`) |
| `+0x2C` | `i32` | count | cells queued (`0x007AB37B`) |

## State

The driver keeps its pools, lists and queues in the globals from `0x02EAD010`. Every one is 0 in the file (the
zero-filled tail of `.data`) until the static initialisers and the driver start `0x007A4D50` fill it; the exit handlers
`0x008B86A0`-`0x008B8E40` clear the lists and queues again. The counts come from the start-up block `0x00210760` fills
(`0x00210855`-`0x0021087B`).

The scalars:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAD098` | `i32` | 0 | the number of command actions, 1,024 (start-up block `+0x30`) | `0x007AB390` (`0x007AB3A1`) | no instruction |
| `0x02EAD0B0` | `void*` | 0 | the allocate function of the driver's heap, `0x00210EC0` (start-up block `+0x00`) | `0x007AD620` (`0x007AD620`), from the driver start (`0x007A4E39`) | called by `0x007AD460` (`0x007AD47F`), `0x007AD4D0` (`0x007AD4F0`), `0x007AD550` (`0x007AD563`) and `0x007AD5A0` (`0x007AD5C4`) |
| `0x02EAD0D0` | `void*` | 0 | the first name buffer in use: `0x110`-byte blocks holding a name at `+0x08` and the next block at `+0x108` | `0x007AE470`, which copies a name into a buffer for `0x007A5380` (`0x007AE524`); `0x007AE550`, which frees the buffer after the command runs (`0x007AE5B4`) | `0x007AE470` (`0x007AE50F`); `0x007AE550` (`0x007AE566`) |
| `0x02EAD0D8` | `void*` | 0 | the first free name buffer | `0x007AE470` (`0x007AE4DD`, `0x007AE4EB`); `0x007AE550` (`0x007AE5D1`) | `0x007AE470` (`0x007AE48F`); `0x007AE550` (`0x007AE5BB`) |
| `0x02EAD400` | `i32` | 0 | the bank count, 1,024 (start-up block `+0x18`) | `0x007B2700` (`0x007B2707`) | `0x007B2700`, which shares it among the bank lists (`0x007B2810`) |
| `0x02EAD404` | `i32` | 0 | the number of bank lists at `0x02EAD410`, 1 (start-up block `+0x1C`) | `0x007B2700` (`0x007B271F`) | `0x007B2700` (`0x007B2752`, `0x007B27F4`, `0x007B283A`); the bank creators `0x007B1660` (`0x007B172D`), `0x007B18A0` (`0x007B194C`), `0x007B1AB0` (`0x007B1C90`) and `0x007B1E10` (`0x007B2006`), which pick the least-filled list; the lookup `0x007B2470` (`0x007B2482`); the update pass `0x007B2920`, which turns to the next list (`0x007B294A`) |
| `0x02EAD40C` | `i32` | 0 | the last serial given to a bank; each new bank's handle takes the next | `0x007B1660` (`0x007B1787`), `0x007B18A0` (`0x007B19A6`), `0x007B1AB0` (`0x007B1CEA`), `0x007B1E10` (`0x007B2063`) | the same four (`0x007B1773`, `0x007B1992`, `0x007B1CD6`, `0x007B204F`) |
| `0x02EAD5A4` | `i32` | 0 | the last serial given to a sequence; each new sequence's handle (kind 3) takes the next | `0x007B4EF0` (`0x007B4F4D`) | `0x007B4EF0` (`0x007B4F42`) |
| `0x02EAD630` | `i32` | 0 | the track count: blocks of the track pool and nodes of the track list | `0x007B5A00` (`0x007B5A62`) | `0x007B5A00`, for the list builder `0x007B5900` (`0x007B5AA5`) |
| `0x02EAD634` | `i32` | 0 | the limit of `0x02EAD63C`, 96 (start-up block `+0x20`) | `0x007B5A00` (`0x007B5A89`) | `0x007B5690`: at the limit it prints "voice overflow" and makes no track, answering 5 (`0x007B56D8`-`0x007B573F`) |
| `0x02EAD638` | `i32` | 0 | the last serial given to a track | `0x007B5690` (`0x007B57EB`) | `0x007B5690` (`0x007B57DF`) |
| `0x02EAD63C` | `i32` | 0 | the live tracks whose third argument's `+0x08` has byte `+1` equal to 1 | `0x007B5690` adds one when it makes such a track (`0x007B5833`); the track pass `0x007B5AD0` takes one away when it frees one whose slot 1 answers 1 (`0x007B5B3A`) | `0x007B5690`, against the limit `0x02EAD634` (`0x007B56DE`) |
| `0x02EAD6C0` | `i32` | 0 | the voice count: blocks of the voice pool and nodes of the voice list | `0x007B5F90` (`0x007B5FF2`) | `0x007B5F90`, for the list builder `0x007B5E90` (`0x007B602C`) |
| `0x02EAD6C4` | `i32` | 0 | the last serial given to a voice; each new voice's handle (kind 5) takes the next | `0x007B5D20` (`0x007B5DA3`) | `0x007B5D20` (`0x007B5DA3`, `0x007B5DB8`) |
| `0x02EAD750` | `i32` | 0 | the running-event count, 64 (start-up block `+0x2C`, `0x007A4FED`) | `0x007B67E0` (`0x007B67F9`) | `0x007B67E0`, for the list builder `0x007B66E0` (`0x007B6991`) |
| `0x02EAD754` | `i32` | 0 | the number of `evt ` elements of the configuration's `EventChunk` (its word `+4`) | `0x007B67E0` (`0x007B6865`); the teardown `0x007B69C0` clears it (`0x007B6A87`) | `0x007B67E0` (`0x007B687D`, `0x007B6969`); `0x007B69C0` (`0x007B6A24`, `0x007B6A5A`) |
| `0x02EAD758` | `i32` | 0 | the last serial given to a running event: command `0x33` (`0x007B6350`) puts the event in the event list and builds its handle from kind byte 2, the node's slot and this serial (`0x007B6592`-`0x007B65B5`) | `0x007B6350` (`0x007B65A6`) | `0x007B6350` (`0x007B6592`) |
| `0x02EAD760` | `void*` | 0 | the table of one `EventData` pointer per `evt ` element, each `0x38` bytes and filed in the hash table `0x01F41460` | `0x007B67E0` (`0x007B6876`); `0x007B69C0` clears it (`0x007B6A7C`) | `0x007B67E0` (`0x007B6941`); `0x007B69C0` (`0x007B6A18`, `0x007B6A53`) |
| `0x02EADBB8` | `i32` | 0 | the last serial given to a music | `0x007B72B0` (`0x007B7352`) | `0x007B72B0` (`0x007B733B`); `0x007B6F70` takes its address only as the end of the table `0x02EAD8B8` (`0x007B701D`) |
| `0x02EADC78` | `i32` | 0 | start-up block `+0x28`, stored by the instrument builder | `0x007B8170` (`0x007B8212`), which runs only when that value is not 0 (`0x007A519B`-`0x007A51A0`); the shipped block holds 0 (`0x00210831`), so the instrument pool and list are never built | no instruction |
| `0x02EADC7C` | `i32` | 0 | the live instruments: the instrument pass `0x007B82D0` takes one away for each instrument that ends in state 7 (`0x007B8351`-`0x007B8364`); no instruction adds one, and with no instrument in the shipped game the pass does not run | `0x007B82D0` (`0x007B8364`) | `0x007B82D0` (`0x007B8364`) |

The fields of the lists and queues ("through the address" names the helpers a function hands the object to):

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAD548` | `i32` | 0 | sound list 1 `+0x08`, capacity: the nodes the list holds | `0x00169C10` (`0x00169C2D`); through the address: `0x007B4670` with `0x007B6AA0` (from `0x007B4770`) | `0x007B2CB0` (`0x007B2EE3`); `0x007B44C0` (`0x007B44D8`); `0x007B4A70` (`0x007B4C8D`); through the address: `0x007B4670` with `0x007B6AA0` (from `0x007B4770`); `0x007B2880` (from `0x007B2CB0` at `0x007B2EAC`, `0x007B4A70` at `0x007B4B3C`) |
| `0x02EAD54C` | `i32` | 0 | sound list 1 `+0x0C`, nodes in use | `0x00169C10` (`0x00169C2D`); `0x007B4840` (`0x007B48B7`); `0x008B8AB0` (`0x008B8AED`); through the address: `0x007AF380` (from `0x007B2CB0`); `0x007B2880` (from `0x007B2CB0`, `0x007B4A70`); `0x007B4670` with `0x007B6AA0` (from `0x007B4770`) | through the address: `0x007AF380` (from `0x007B2CB0`); `0x007B2880` (from `0x007B2CB0`, `0x007B4A70`) |
| `0x02EAD550` | `void*` | 0 | sound list 1 `+0x10`, the `DriverListNode` array | `0x00169C10` (`0x00169C34`); `0x007B4840` (`0x007B48CB`); `0x008B8AB0` (`0x008B8B01`); through the address: `0x007B4670` with `0x007B6AA0` (from `0x007B4770`) | `0x007B2CB0` (`0x007B2EEB`); `0x007B44C0` (`0x007B44E9`); `0x007B4840` (`0x007B486C`); `0x007B4A70` (`0x007B4C95`); `0x008B8AB0` (`0x008B8AB4`); through the address: `0x007B2880` (from `0x007B2CB0`, `0x007B4A70`); `0x007B4670` with `0x007B6AA0` (from `0x007B4770`) |
| `0x02EAD560` | `void*` | 0 | sound list 1 `+0x20`, first node in use | `0x00169C10` (`0x00169C3C`); `0x007B4840` (`0x007B48D3`); `0x008B8AB0` (`0x008B8B10`); through the address: `0x007AF380` (from `0x007B2CB0`); `0x007B2880` (from `0x007B2CB0`, `0x007B4A70`); `0x007B4670` with `0x007B6AA0` (from `0x007B4770`) | `0x007B31A0` (`0x007B3305`, `0x007B3402`); `0x007B48F0` (`0x007B490B`); `0x007B4960` (`0x007B498B`); `0x007B4A00` (`0x007B4A1B`); `0x007B4A70` (`0x007B4A9D`); through the address: `0x007AF380` (from `0x007B2CB0`) |
| `0x02EAD578` | `i32` | 0 | sound list 2 `+0x08`, capacity: the nodes the list holds | `0x00169B50`, 0 with `+0x0C` (`0x00169B6D`); through the address: `0x007B4670` (`0x007B46D5`), from `0x007B4770` | through the address: `0x007B6AA0` (`0x007B6AB1`, `0x007B6AE6`), from `0x007B4670` (`0x007B474C`) and `0x007B31A0`; `0x007B2880` (`0x007B2888`), from `0x007B31A0` |
| `0x02EAD57C` | `i32` | 0 | sound list 2 `+0x0C`, nodes in use; `0x007B31A0` relinks the list empty (`0x007B32F3`) and fills it from sound list 1 (`0x007B334C`, `0x007B344B`) | `0x00169B50` (`0x00169B6D`); `0x007B4840` (`0x007B4876`); `0x008B8A10` (`0x008B8A4D`); through the address: `0x007AF380`, `0x007B2880` and `0x007B6AA0` (from `0x007B31A0`); `0x007B4670` with `0x007B6AA0` (from `0x007B4770`) | `0x007B31A0` (`0x007B3D26`, `0x007B3F38`, `0x007B3F62`, `0x007B3FA7`, `0x007B4004`, `0x007B403B`, `0x007B40AA`, `0x007B410B`, `0x007B4150`, `0x007B4190`, `0x007B41D0`, `0x007B4256`); through the address: `0x007AF380` and `0x007B2880` (from `0x007B31A0`) |
| `0x02EAD580` | `void*` | 0 | sound list 2 `+0x10`, the `DriverListNode` array | `0x00169B50` (`0x00169B74`); `0x007B4840` (`0x007B4883`); `0x008B8A10` (`0x008B8A61`); through the address: `0x007B4670` with `0x007B6AA0` (from `0x007B4770`) | `0x007B4840` (`0x007B4844`); `0x008B8A10` (`0x008B8A14`); through the address: `0x007B2880` (from `0x007B31A0`); `0x007B6AA0` (from `0x007B31A0`); `0x007B4670` with `0x007B6AA0` (from `0x007B4770`) |
| `0x02EAD590` | `void*` | 0 | sound list 2 `+0x20`, first node in use | `0x00169B50` (`0x00169B7C`); `0x007B4840` (`0x007B488B`); `0x008B8A10` (`0x008B8A70`); through the address: `0x007AF380`, `0x007B2880` and `0x007B6AA0` (from `0x007B31A0`); `0x007B4670` with `0x007B6AA0` (from `0x007B4770`) | `0x007B31A0` (`0x007B3475`, `0x007B3559`, `0x007B36BE`, `0x007B37A9`, `0x007B3902`, `0x007B3A40`, `0x007B3B28`, `0x007B3C4E`, `0x007B3D3D`, `0x007B3FBA`, `0x007B41E7`, `0x007B4269`); through the address: `0x007AF380` (from `0x007B31A0`) |
| `0x02EAD608` | `i32` | 0 | sequence list `+0x08`, capacity: the nodes the list holds | `0x00169C90` (`0x00169CAD`); through the address: `0x007B50F0` with `0x007B6AA0` (from `0x007B51F0`) | `0x007B5070` (`0x007B5088`); `0x007B52B0` (`0x007B5339`); through the address: `0x007B50F0` with `0x007B6AA0` (from `0x007B51F0`) |
| `0x02EAD60C` | `i32` | 0 | sequence list `+0x0C`, nodes in use | `0x00169C90` (`0x00169CAD`); `0x007B51F0` (`0x007B523C`); `0x007B52B0` (`0x007B53C4`); `0x008B8B30` (`0x008B8B6D`); through the address: `0x007B5580` (from `0x007B4EF0`); `0x007B50F0` with `0x007B6AA0` (from `0x007B51F0`) | `0x007B52B0` (`0x007B53C4`); through the address: `0x007B5580` (from `0x007B4EF0`) |
| `0x02EAD610` | `void*` | 0 | sequence list `+0x10`, the `DriverListNode` array | `0x00169C90` (`0x00169CB4`); `0x007B51F0` (`0x007B5234`); `0x008B8B30` (`0x008B8B81`); through the address: `0x007B50F0` with `0x007B6AA0` (from `0x007B51F0`) | `0x007B5070` (`0x007B5099`); `0x007B51F0` (`0x007B51FD`); `0x007B52B0` (`0x007B5349`); `0x008B8B30` (`0x008B8B34`); through the address: `0x007B50F0` with `0x007B6AA0` (from `0x007B51F0`) |
| `0x02EAD618` | `void*` | 0 | sequence list `+0x18`, first free node | `0x00169C90` (`0x00169CB4`); `0x007B51F0` (`0x007B5234`); `0x007B52B0` (`0x007B53CD`); `0x008B8B30` (`0x008B8B81`); through the address: `0x007B5580` (from `0x007B4EF0`); `0x007B50F0` with `0x007B6AA0` (from `0x007B51F0`) | `0x007B52B0` (`0x007B53A9`, `0x007B53B4`); through the address: `0x007B5580` (from `0x007B4EF0`) |
| `0x02EAD620` | `void*` | 0 | sequence list `+0x20`, first node in use | `0x00169C90` (`0x00169CBC`); `0x007B51F0` (`0x007B5242`); `0x007B52B0` (`0x007B5368`); `0x008B8B30` (`0x008B8B90`); through the address: `0x007B5580` (from `0x007B4EF0`); `0x007B50F0` with `0x007B6AA0` (from `0x007B51F0`) | `0x007B52B0` (`0x007B52DC`); through the address: `0x007B5580` (from `0x007B4EF0`) |
| `0x02EAD628` | `void*` | 0 | sequence list `+0x28`, last node in use | `0x00169C90` (`0x00169CBC`); `0x007B51F0` (`0x007B5242`); `0x007B52B0` (`0x007B538B`); `0x008B8B30` (`0x008B8B90`); through the address: `0x007B5580` (from `0x007B4EF0`); `0x007B50F0` with `0x007B6AA0` (from `0x007B51F0`) | through the address: `0x007B5580` (from `0x007B4EF0`) |
| `0x02EAD698` | `i32` | 0 | track list `+0x08`, capacity: the nodes the list holds | `0x00169D10` (`0x00169D2D`); through the address: `0x007B5900` with `0x007B6AA0` (from `0x007B5A00`) | `0x007B58C0` (`0x007B58D1`); `0x007B5AD0` (`0x007B5B50`); through the address: `0x007B5900` with `0x007B6AA0` (from `0x007B5A00`); `0x007B2880` (from `0x007B5690` at `0x007B5874`) |
| `0x02EAD69C` | `i32` | 0 | track list `+0x0C`, nodes in use | `0x00169D10` (`0x00169D2D`); `0x007B5A00` (`0x007B5A4C`); `0x007B5AD0` (`0x007B5BDB`); `0x008B8BB0` (`0x008B8BED`); through the address: `0x007B5580` (from `0x007B5690`); `0x007B2880` (from `0x007B5690`); `0x007B5900` with `0x007B6AA0` (from `0x007B5A00`) | `0x007B5AD0` (`0x007B5BDB`); through the address: `0x007B5580` (from `0x007B5690`); `0x007B2880` (from `0x007B5690`) |
| `0x02EAD6A0` | `void*` | 0 | track list `+0x10`, the `DriverListNode` array | `0x00169D10` (`0x00169D34`); `0x007B5A00` (`0x007B5A44`); `0x008B8BB0` (`0x008B8C01`); through the address: `0x007B5900` with `0x007B6AA0` (from `0x007B5A00`) | `0x007B58C0` (`0x007B58DD`); `0x007B5A00` (`0x007B5A0D`); `0x007B5AD0` (`0x007B5B60`); `0x008B8BB0` (`0x008B8BB4`); through the address: `0x007B2880` (from `0x007B5690`); `0x007B5900` with `0x007B6AA0` (from `0x007B5A00`) |
| `0x02EAD6A8` | `void*` | 0 | track list `+0x18`, first free node | `0x00169D10` (`0x00169D34`); `0x007B5A00` (`0x007B5A44`); `0x007B5AD0` (`0x007B5BE4`); `0x008B8BB0` (`0x008B8C01`); through the address: `0x007B5580` (from `0x007B5690`); `0x007B2880` (from `0x007B5690`); `0x007B5900` with `0x007B6AA0` (from `0x007B5A00`) | `0x007B5AD0` (`0x007B5BC0`, `0x007B5BCB`); through the address: `0x007B5580` (from `0x007B5690`); `0x007B2880` (from `0x007B5690`) |
| `0x02EAD6B0` | `void*` | 0 | track list `+0x20`, first node in use | `0x00169D10` (`0x00169D3C`); `0x007B5A00` (`0x007B5A52`); `0x007B5AD0` (`0x007B5B7F`); `0x008B8BB0` (`0x008B8C10`); through the address: `0x007B5580` (from `0x007B5690`); `0x007B2880` (from `0x007B5690`); `0x007B5900` with `0x007B6AA0` (from `0x007B5A00`) | `0x007B5AD0` (`0x007B5AEA`); through the address: `0x007B5580` (from `0x007B5690`) |
| `0x02EAD6B8` | `void*` | 0 | track list `+0x28`, last node in use | `0x00169D10` (`0x00169D3C`); `0x007B5A00` (`0x007B5A52`); `0x007B5AD0` (`0x007B5BA2`); `0x008B8BB0` (`0x008B8C10`); through the address: `0x007B5580` (from `0x007B5690`); `0x007B2880` (from `0x007B5690`); `0x007B5900` with `0x007B6AA0` (from `0x007B5A00`) | through the address: `0x007B5580` (from `0x007B5690`) |
| `0x02EAD728` | `i32` | 0 | voice list `+0x08`, capacity: the nodes the list holds | `0x00169D50` (`0x00169D6D`); through the address: `0x007B5E90` with `0x007B6AA0` (from `0x007B5F90`) | `0x007B5E50` (`0x007B5E61`); `0x007B6050` (`0x007B60C0`); through the address: `0x007B5E90` with `0x007B6AA0` (from `0x007B5F90`) |
| `0x02EAD72C` | `i32` | 0 | voice list `+0x0C`, nodes in use | `0x00169D50` (`0x00169D6D`); `0x007B5F90` (`0x007B5FDC`); `0x007B6050` (`0x007B614B`); `0x008B8C20` (`0x008B8C5D`); through the address: `0x007B5580` (from `0x007B5D20`); `0x007B5E90` with `0x007B6AA0` (from `0x007B5F90`) | `0x007B6050` (`0x007B614B`); through the address: `0x007B5580` (from `0x007B5D20`) |
| `0x02EAD730` | `void*` | 0 | voice list `+0x10`, the `DriverListNode` array | `0x00169D50` (`0x00169D74`); `0x007B5F90` (`0x007B5FD4`); `0x008B8C20` (`0x008B8C71`); through the address: `0x007B5E90` with `0x007B6AA0` (from `0x007B5F90`) | `0x007B5E50` (`0x007B5E6D`); `0x007B5F90` (`0x007B5F9D`); `0x007B6050` (`0x007B60D0`); `0x008B8C20` (`0x008B8C24`); through the address: `0x007B5E90` with `0x007B6AA0` (from `0x007B5F90`) |
| `0x02EAD738` | `void*` | 0 | voice list `+0x18`, first free node | `0x00169D50` (`0x00169D74`); `0x007B5F90` (`0x007B5FD4`); `0x007B6050` (`0x007B6154`); `0x008B8C20` (`0x008B8C71`); through the address: `0x007B5580` (from `0x007B5D20`); `0x007B5E90` with `0x007B6AA0` (from `0x007B5F90`) | `0x007B6050` (`0x007B6130`, `0x007B613B`); through the address: `0x007B5580` (from `0x007B5D20`) |
| `0x02EAD740` | `void*` | 0 | voice list `+0x20`, first node in use | `0x00169D50` (`0x00169D7C`); `0x007B5F90` (`0x007B5FE2`); `0x007B6050` (`0x007B60EF`); `0x008B8C20` (`0x008B8C80`); through the address: `0x007B5580` (from `0x007B5D20`); `0x007B5E90` with `0x007B6AA0` (from `0x007B5F90`) | `0x007B6050` (`0x007B606A`); through the address: `0x007B5580` (from `0x007B5D20`) |
| `0x02EAD748` | `void*` | 0 | voice list `+0x28`, last node in use | `0x00169D50` (`0x00169D7C`); `0x007B5F90` (`0x007B5FE2`); `0x007B6050` (`0x007B6112`); `0x008B8C20` (`0x008B8C80`); through the address: `0x007B5580` (from `0x007B5D20`); `0x007B5E90` with `0x007B6AA0` (from `0x007B5F90`) | through the address: `0x007B5580` (from `0x007B5D20`) |
| `0x02EAD7E8` | `i32` | 0 | event list `+0x08`, capacity: the nodes the list holds | `0x00169E50` (`0x00169E6D`); through the address: `0x007B66E0` with `0x007B6AA0` (from `0x007B67E0`) | `0x007B6350` (`0x007B6692`); through the address: `0x007B2880` (from `0x007B6350`, `0x007B6B00`); `0x007B66E0` with `0x007B6AA0` (from `0x007B67E0`) |
| `0x02EAD7EC` | `i32` | 0 | event list `+0x0C`, nodes in use | `0x00169E50` (`0x00169E6D`); `0x007B69C0` (`0x007B69EF`); `0x008B8CD0` (`0x008B8D0D`); through the address: `0x007B5580` (from `0x007B6350`); `0x007B2880` (from `0x007B6350`, `0x007B6B00`); `0x007B66E0` with `0x007B6AA0` (from `0x007B67E0`) | through the address: `0x007B5580` (from `0x007B6350`); `0x007B2880` (from `0x007B6350`, `0x007B6B00`) |
| `0x02EAD7F0` | `void*` | 0 | event list `+0x10`, the `DriverListNode` array | `0x00169E50` (`0x00169E74`); `0x007B69C0` (`0x007B6A03`); `0x008B8CD0` (`0x008B8D21`); through the address: `0x007B66E0` with `0x007B6AA0` (from `0x007B67E0`) | `0x007B6350` (`0x007B669A`); `0x007B69C0` (`0x007B69C4`); `0x008B8CD0` (`0x008B8CD4`); through the address: `0x007B2880` (from `0x007B6350`, `0x007B6B00`); `0x007B66E0` with `0x007B6AA0` (from `0x007B67E0`) |
| `0x02EAD800` | `void*` | 0 | event list `+0x20`, first node in use | `0x00169E50` (`0x00169E7C`); `0x007B69C0` (`0x007B6A0B`); `0x008B8CD0` (`0x008B8D30`); through the address: `0x007B5580` (from `0x007B6350`); `0x007B2880` (from `0x007B6350`, `0x007B6B00`); `0x007B66E0` with `0x007B6AA0` (from `0x007B67E0`) | `0x007B6B00` (`0x007B6B2A`); through the address: `0x007B5580` (from `0x007B6350`) |
| `0x02EADC18` | `i32` | 0 | music list `+0x08`, capacity: the nodes the list holds | `0x00169FF0` (`0x0016A00D`); through the address: `0x007B7B00` with `0x007B6AA0` (from `0x007B7C10`) | `0x007B72B0` (`0x007B7407`); `0x007B77E0` (`0x007B77F8`); through the address: `0x007B7B00` with `0x007B6AA0` (from `0x007B7C10`); `0x007B2880` (from `0x007B72B0` at `0x007B73D1`, `0x007B7D60` at `0x007B7E8A`) |
| `0x02EADC1C` | `i32` | 0 | music list `+0x0C`, nodes in use | `0x00169FF0` (`0x0016A00D`); `0x007B7C10` (`0x007B7C44`); `0x008B8DB0` (`0x008B8DED`); through the address: `0x007AF380` (from `0x007B72B0`); `0x007B2880` (from `0x007B72B0`, `0x007B7D60`); `0x007B7B00` with `0x007B6AA0` (from `0x007B7C10`) | through the address: `0x007AF380` (from `0x007B72B0`); `0x007B2880` (from `0x007B72B0`, `0x007B7D60`) |
| `0x02EADC20` | `void*` | 0 | music list `+0x10`, the `DriverListNode` array | `0x00169FF0` (`0x0016A014`); `0x007B7C10` (`0x007B7C58`); `0x008B8DB0` (`0x008B8E01`); through the address: `0x007B7B00` with `0x007B6AA0` (from `0x007B7C10`) | `0x007B72B0` (`0x007B740F`); `0x007B77E0` (`0x007B7809`); `0x007B7C10` (`0x007B7C19`); `0x008B8DB0` (`0x008B8DB4`); through the address: `0x007B2880` (from `0x007B72B0`, `0x007B7D60`); `0x007B7B00` with `0x007B6AA0` (from `0x007B7C10`) |
| `0x02EADC30` | `void*` | 0 | music list `+0x20`, first node in use | `0x00169FF0` (`0x0016A01C`); `0x007B7C10` (`0x007B7C60`); `0x008B8DB0` (`0x008B8E10`); through the address: `0x007AF380` (from `0x007B72B0`); `0x007B2880` (from `0x007B72B0`, `0x007B7D60`); `0x007B7B00` with `0x007B6AA0` (from `0x007B7C10`) | `0x007B7860` (`0x007B788E`); `0x007B7CC0` (`0x007B7CEB`); `0x007B7D60` (`0x007B7D91`); through the address: `0x007AF380` (from `0x007B72B0`) |
| `0x02EADCD8` | `i32` | 0 | instrument list `+0x08`, capacity: the nodes the list holds | `0x0016A0A0` (`0x0016A0BD`); through the address: `0x007B8060` with `0x007B6AA0` (from `0x007B8170`) | `0x007B7FD0` (`0x007B7FE8`); through the address: `0x007B8060` with `0x007B6AA0` (from `0x007B8170`); `0x007B2880` (from `0x007B82D0` at `0x007B8378`) |
| `0x02EADCDC` | `i32` | 0 | instrument list `+0x0C`, nodes in use | `0x0016A0A0` (`0x0016A0BD`); `0x007B8170` (`0x007B81A4`); `0x008B8E40` (`0x008B8E7D`); through the address: `0x007B2880` (from `0x007B82D0`); `0x007B8060` with `0x007B6AA0` (from `0x007B8170`) | through the address: `0x007B2880` (from `0x007B82D0`) |
| `0x02EADCE0` | `void*` | 0 | instrument list `+0x10`, the `DriverListNode` array | `0x0016A0A0` (`0x0016A0C4`); `0x007B8170` (`0x007B81B8`); `0x008B8E40` (`0x008B8E91`); through the address: `0x007B8060` with `0x007B6AA0` (from `0x007B8170`) | `0x007B7FD0` (`0x007B7FF9`); `0x007B8170` (`0x007B8179`); `0x008B8E40` (`0x008B8E44`); through the address: `0x007B2880` (from `0x007B82D0`); `0x007B8060` with `0x007B6AA0` (from `0x007B8170`) |
| `0x02EADCF0` | `void*` | 0 | instrument list `+0x20`, first node in use | `0x0016A0A0` (`0x0016A0CC`); `0x007B8170` (`0x007B81C0`); `0x008B8E40` (`0x008B8EA0`); through the address: `0x007B2880` (from `0x007B82D0`); `0x007B8060` with `0x007B6AA0` (from `0x007B8170`) | `0x007B8230` (`0x007B825B`); `0x007B82D0` (`0x007B82FA`) |
| `0x02EAD018` | `void*` | 0 | free-action queue `+0x08`, the cells, 1,024 of them | `0x00169790` (`0x001697B4`); `0x008B8720`, 0 after freeing them (`0x008B8771`); through the address: `0x007AB240` (`0x007AB27C`, `0x007AB332`), from `0x007AB390` (`0x007AB3D4`) | `0x008B8720`, which frees them at exit (`0x008B8724`); through the address: `0x007AB240`, which frees the old cells and chains the new ones (`0x007AB255`, `0x007AB350`) |
| `0x02EAD020` | `void*` | 0 | free-action queue `+0x10`, first free cell | `0x00169790` (`0x001697B4`); `0x007AB390` (`0x007AB409`); `0x007AB460` (`0x007AB528`); `0x007AB5C0` (`0x007ABFC9`); `0x008B8720` (`0x008B8771`); through the address: `0x007AB240` (from `0x007AB390`) | `0x007AB390` (`0x007AB3F5`, `0x007AB442`); `0x007AB460` (`0x007AB515`); `0x007AB5C0` (`0x007ABFB9`) |
| `0x02EAD030` | `void*` | 0 | free-action queue `+0x20`, last queued cell | `0x00169790` (`0x001697BC`); `0x007AB390` (`0x007AB43B`); `0x007AB5C0` (`0x007ABFFB`); `0x008B8720` (`0x008B8780`); through the address: `0x007AB240` (from `0x007AB390`) | `0x007AB390` (`0x007AB42A`); `0x007AB5C0` (`0x007ABFEA`) |
| `0x02EAD038` | `i32` | 0 | free-action queue `+0x28`, capacity: 1,024 cells | `0x00169790`, 0 with `+0x2C` (`0x001697AD`); through the address: `0x007AB240` (`0x007AB2B0`), from `0x007AB390` (`0x007AB3D4`) | no instruction |
| `0x02EAD03C` | `i32` | 0 | free-action queue `+0x2C`, cells queued | `0x00169790` (`0x001697AD`); `0x007AB390` (`0x007AB435`); `0x007AB460` (`0x007AB520`); `0x007AB5C0` (`0x007ABFF5`); `0x008B8720` (`0x008B875D`); through the address: `0x007AB240` (from `0x007AB390`) | `0x007AB390` (`0x007AB435`); `0x007AB460` (`0x007AB520`); `0x007AB5C0` (`0x007ABFF5`) |
| `0x02EAD060` | `void*` | 0 | command queue `+0x20`, last queued cell | `0x00169720` (`0x0016974C`); `0x007AB550` (`0x007AB5A1`); `0x008B86A0` (`0x008B8700`); through the address: `0x007AB240` (from `0x007AB390`) | `0x007AB550` (`0x007AB590`) |
| `0x02EADDA8` | `void*` | 0 | Lay command queue `+0x08`, the cells, 512 of them | `0x0016A110` (`0x0016A134`); `0x008B8EC0`, 0 after freeing them (`0x008B8F11`); through the address: `0x007BAB30` (`0x007BAB6C`, `0x007BAC22`), from `0x007BAC80` (`0x007BACD5`) | `0x008B8EC0`, which frees them at exit (`0x008B8EC4`); through the address: `0x007BAB30`, which frees the old cells and chains the new ones (`0x007BAB45`, `0x007BAC40`) |
| `0x02EADDB0` | `void*` | 0 | Lay command queue `+0x10`, first free cell | `0x0016A110` (`0x0016A134`); `0x007BAE50` (`0x007BAE6F`); `0x007BAEC0` (`0x007BAF5D`); `0x008B8EC0` (`0x008B8F11`); through the address: `0x007BAB30` (from `0x007BAC80`) | `0x007BAE50` (`0x007BAE56`); `0x007BAEC0` (`0x007BAF4C`) |
| `0x02EADDB8` | `void*` | 0 | Lay command queue `+0x18`, first queued cell | `0x0016A110` (`0x0016A13C`); `0x007BAE50` (`0x007BAE87`); `0x007BAEC0` (`0x007BAF45`); `0x008B8EC0` (`0x008B8F20`); through the address: `0x007BAB30` (from `0x007BAC80`) | `0x007BAE50` (`0x007BAE7E`); `0x007BAEC0` (`0x007BAEE9`, `0x007BB560`) |
| `0x02EADDC0` | `void*` | 0 | Lay command queue `+0x20`, last queued cell | `0x0016A110` (`0x0016A13C`); `0x007BAE50` (`0x007BAEA1`); `0x008B8EC0` (`0x008B8F20`); through the address: `0x007BAB30` (from `0x007BAC80`) | `0x007BAE50` (`0x007BAE90`) |
| `0x02EADDC8` | `i32` | 0 | Lay command queue `+0x28`, capacity: 512 cells | `0x0016A110`, 0 with `+0x2C` (`0x0016A12D`); through the address: `0x007BAB30` (`0x007BABA0`), from `0x007BAC80` (`0x007BACD5`) | no instruction |
| `0x02EADDCC` | `i32` | 0 | Lay command queue `+0x2C`, cells queued | `0x0016A110` (`0x0016A12D`); `0x007BAE50` (`0x007BAE9B`); `0x007BAEC0` (`0x007BAF57`); `0x008B8EC0` (`0x008B8EFD`); through the address: `0x007BAB30` (from `0x007BAC80`) | `0x007BAE50` (`0x007BAE9B`); `0x007BAEC0` (`0x007BAF57`) |

`0x007AB390` fills the free-action queue `0x02EAD010` with the 1,024 actions; `0x007AB460` takes one from it, `0x007AB550`
appends a filled one to the command queue `0x02EAD040`, and the command runner `0x007AB5C0` gives each action back to the
free-action queue after running it (`0x007ABFB9`-`0x007ABFFB`). The `Lay` command queue `0x02EADDA0` works the same way
for `0x007BAE50` and the `Lay` runner `0x007BAEC0`.

No other instruction reaches these globals. A function that takes a list's or a queue's address is listed with the helper
it passes it to.

## Modding notes

- At most 92 sounds and 8 music exist at once; a ninety-third sound is refused with "sound heap empty" and plays
  nothing.
- No instrument exists in the shipped game: the pool of 32 is built only when start-up block `+0x28` is not 0, and
  `0x00210760` leaves it 0 (`0x00210831`).
- A sound id with bit 30 set names a sound by its number in the bank, not by its index.
- A handle stays safe to use after its object ends: the serial check makes every call on it do nothing.

## Related

- [Sound engine](sound-engine.md) - the command queue and the voice mixer.
- [Sound engine configuration](sound-engine-config.md) - the categories that size the sound pool.
- [Sound variations](sound-variations.md) - the factory that builds a sound object.
- [Audio manager](audio-manager.md) - the game-side objects that hold these handles.
- [Sound streaming](sound-streaming.md) - streaming banks.
- [Interactive music](interactive-music.md) - the music commands.
