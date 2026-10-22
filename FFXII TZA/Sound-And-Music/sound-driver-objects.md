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
| instruments | `0x007B8170` | `0x208` | 32 | `0x02EADCD0` (`0x007B8060`) |

The counts are the shipped ones: the sound count is the categories' sum plus 32 and the sequences and tracks twice
that (`0x007A4ECC`, `0x007A4ED7`), the voice count is the three start-up counts of
[Sound engine configuration](sound-engine-config.md), the bank and event counts come from the start-up block
`0x00210760` fills (`0x400`, `0x40`), and the music and instrument counts are constants of their builders. `0x007B6AA0`
links a fresh list's nodes into its free chain.

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
   state 7, giving back its track need) and, while instruments exist (`0x007B8220`), `0x007B82D0` (freed in state 7).
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

## Modding notes

- At most 92 sounds, 8 music and 32 instruments exist at once; a ninety-third sound is refused with "sound heap
  empty" and plays nothing.
- A sound id with bit 30 set names a sound by its number in the bank, not by its index.
- A handle stays safe to use after its object ends: the serial check makes every call on it do nothing.

## Related

- [Sound engine](sound-engine.md) - the command queue and the voice mixer.
- [Sound engine configuration](sound-engine-config.md) - the categories that size the sound pool.
- [Sound variations](sound-variations.md) - the factory that builds a sound object.
- [Audio manager](audio-manager.md) - the game-side objects that hold these handles.
- [Sound streaming](sound-streaming.md) - streaming banks.
- [Interactive music](interactive-music.md) - the music commands.
