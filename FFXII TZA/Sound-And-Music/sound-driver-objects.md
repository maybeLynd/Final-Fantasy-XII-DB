---
title: "Sound driver objects: the handles, fixed pools and calls through which the game creates, finds, commands and queries banks, sounds and music"
kind: "system"
category: "Sound and music"
addresses: "007B2CB0, 007B1660, 007B72B0, 007B2200, 007A87C0, 007A7010, 007A9160, 007DF790"
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

`007B2CB0` writes all three for a sound (`007B2E49`-`007B2E4F`), `007B1660` for a bank, `007B5690` for a track,
`007B5D20` for a voice and `007B72B0` for a music. A lookup takes the slot, checks it is live (bit 0 of the list node's
`+1C`<sub>h</sub>) and compares the whole handle with the object's own copy, so a handle of an object that has ended finds
nothing:

| Kind | Object | Lookup | Its copy of the handle |
|---:|---|---|---|
| `1` | `Bank` | `007B2470` | `+10`<sub>h</sub> |
| `2` | `Sound` | `007B44C0` | slot 22, `007BD5D0` (`+18`<sub>h</sub>) |
| `3` | `Sequence` | `007B5070` | `007E71B0` |
| `4` | `Track` | `007B58C0` | `+08`<sub>h</sub> |
| `5` | `Voice` | `007B5E50` | `+40`<sub>h</sub> |
| `7` | `Lay` source | `007BC2B0` | `+08`<sub>h</sub> |
| `8` | `Magi::Music` | `007B77E0` | slot 22 |
| `9` | `Magi::Instrument` | `007B7FD0` | slot 22 |

`007A9160` turns a kind 7 handle into the driver handle its `Lay` source plays (source slot 4) and passes a kind 8
handle through; the music calls below use it, so they accept either. The handle helpers `007A4380` (-1), `007A5F10`
(0), `007A46E0`, `007A4C40`, `007A4C70`, `007A47A0`, `007A9060` and `007A9080` build or copy a handle value, and
`007A59E0`, `007A59F0`, `007A5B20`, `007A5B00` and `007A5660` do the same for the four-byte `Lay` handles.

### Pools and lists

`007A4D50` builds every pool when the driver starts. A pool is a fixed-block heap (`007DF790` builds it, `007DF750`
takes a block, `007DF8D0` gives one back, `007DF910` gives a block's index, `007DF890` frees it), and each kind has
a list of `28`<sub>h</sub>-byte nodes that its handles index:

| Objects | Builder | Block | Count | List |
|---|---|---:|---:|---|
| banks | `007B2700` | `158`<sub>h</sub> | 1,024 | the bank lists at `02EAD410`, one in the shipped start-up block (`007B2500`), and the streaming-bank list (`007B2600`) |
| sounds | `007B4770` | `540`<sub>h</sub> | 92 | `02EAD540` and `02EAD570` (`007B4670`); torn down by `007B4840` |
| sequences | `007B51F0` | `C8`<sub>h</sub> | 184 | `02EAD600` (`007B50F0`) |
| tracks | `007B5A00` | `3D0`<sub>h</sub> | 184 | `02EAD690` (`007B5900`) |
| voices | `007B5F90` | `470`<sub>h</sub> | 128 | `02EAD720` (`007B5E90`) |
| events | `007B67E0` | `38`<sub>h</sub> | 64 | `02EAD7E0` (`007B66E0`); torn down by `007B69C0` |
| music | `007B7C10` | `8D8`<sub>h</sub> | 8 | `02EADC10` (`007B7B00`) |
| instruments | `007B8170` | `208`<sub>h</sub> | 32 | `02EADCD0` (`007B8060`) |

The counts are the shipped ones: the sound count is the categories' sum plus 32 and the sequences and tracks twice
that (`007A4ECC`, `007A4ED7`), the voice count is the three start-up counts of
[Sound engine configuration](sound-engine-config.md), the bank and event counts come from the start-up block
`00210760` fills (`400`<sub>h</sub>, `40`<sub>h</sub>), and the music and instrument counts are constants of their builders. `007B6AA0`
links a fresh list's nodes into its free chain.

`007AF380` puts a node at the front of a list and `007B5580` at the
back; both print "list append error full!" when no node is free. `007B2880` takes a node out, and `007B14C0` empties a bank list.

### Finding by number

Banks and sounds are also kept in hash tables of 257 buckets (`007E27B0`): banks at `01F40440`, sounds at
`01F40C50`. `007E2880` adds an object, `007E2910` removes it and `007E27F0` moves a found one to the front of its
bucket.

- `007B2200(id)` finds the bank whose number is the id's high 16 bits, in bucket `(id >> 16) % 257`
  (`007B2251`); a bank with a sound table must also hold the id's low 16 bits as a sound number.
- `007B4540(id)` finds a playing sound by its sound number and its bank's number; `007B7860(id)` does the same for a
  music.
- `007A4CA0(out, id)` gives the handle of the playing sound or music with that id, by the bank's content type
  `+48`<sub>h</sub>: 1 for a sound bank, 2 for a music bank.
- `007A4BB0(out, id)` gives the handle of the bank that holds the id, under the bank lock (`007B24F0`).

### Creating a bank

`007A48C0` (from the game's bank loaders `00222F20`, `00223DA0` and `00224C40`) calls `007B1660`:

1. It checks the data's tag: `sabf` (`007CFF90`) makes a sound bank; `mabf` (`007D07A0`) goes to `007B18A0`, which
   makes a music bank the same way.
2. It takes a bank block and a node in the least-filled bank list, and writes a kind 1 handle.
3. It builds an `OnMemoryBank` (`007E29C0`, over the `Bank` base `007D07C0`) and runs its slot 8 with the data and
   the content type, 1 or 2.
4. It adds the bank to the hash table. On failure it gives back the node and the block.

`007A4AC0` and `007A4B30` do the same for a streaming sound bank (`007B1AB0`) and a streaming music bank
(`007B1E10`), described on [Sound streaming](sound-streaming.md). `007A88F0(bank, nowait)` releases a bank through
`007D0A10`; with `nowait` 0 it then sleeps 1 ms at a time until the handle finds nothing. `007A8CA0` answers whether a
bank handle still finds its bank, `007A89F0` gives its content type, and `007A8C30` gives its readiness: slot 3 for
a sound bank and slot 4 for a music bank.

A bank counts its users at `+18`<sub>h</sub>: `007D0890` adds one and `007D0A00`
takes one away, both atomically; `007D0810` puts back the base vtables when a bank is destroyed.

### Creating a sound or a music

`007A87C0(bank, out, id, ...)` (from `00221C70`, `007A4A10` and the `Lay` tick `007F0820`) looks the bank up and
calls `007D0940` for a sound bank or `007D08F0` for a music bank; `007A86E0` takes only a music bank. `007A4A10(out,
id)` first finds the bank by number and asks for the sound with bit 30 set, meaning a sound number rather than an
index (`007A4A7C`).

1. `007B2CB0` takes a `540`<sub>h</sub> block and a node in the sound list; with no block it prints "sound heap empty. could
   not create sound", with no node "using list full. could not create sound".
2. It writes a kind 2 handle with the next serial (`02EAD4C4`) and builds the object through the factory `007B2F70`
   ([Sound variations](sound-variations.md)).
3. It records the object in its node and, unless the object is waiting for its bank (slot 38), adds it to the sound
   hash table.

`007B72B0` does the same for a music through `007B7460`. That checks the music number against the bank's count
("music number is out of range"), resolves a number with bit 30 set through `007A8EA0`, and adds the music's track
need to `02EADBB0`: `007B7960` counts it from the music's sections and mode transitions in an in-memory bank, and a
streaming bank gives its stream count `+94`<sub>h</sub>. Over the budget `02EADBB4`, 32, it prints "track count exceeded
numMusicTracks" and goes on.

### Reading a sound's header

`007A8A50(bank, out, id)` copies one sound's or music's header into an info record, fields `+100`<sub>h</sub> to `+11C`<sub>h</sub>, without playing it: an id
with bit 30 set is a number, found by `007A8F40` in a sound bank or `007A8EA0` in a music bank. `007A6C10` fills the
record from a sound header and `007A6AC0` from a music header, reading each field only when the header's version byte
is new enough; `007A6990` fills it from an instrument. `007A6DB0(handle, out)` fills the same record for a playing
object of kind 2, 8 or 9.

### Posting a command

`007AB390` builds 1,024 actions of `28`<sub>h</sub> bytes at `02EAD0A0` and the two queues `02EAD010` and `02EAD040`
(`007AB240`), and puts every action on the first. Every call that changes a playing object takes an action from the
queue (`007AB460`), fills it and appends it (`007AB550`); a call on a `Lay` source posts to the `Lay` queue instead (`007BAD60`, `007BAE50`). A call returns
`82000000`<sub>h</sub> for a zero handle and -1 for a handle of the wrong kind. Types `0B`<sub>h</sub>-`1B`<sub>h</sub> run a `Sound` method on
the driver thread (`007AB5C0`):

| Call | Kinds | Type | `Lay` type | Runs |
|---|---|---:|---:|---|
| `007A7F70` | 2, 8 | `0F`<sub>h</sub> | `0B`<sub>h</sub> | slot 8, pitch |
| `007A7E90` | 2, 8, 9 | `10`<sub>h</sub> | | slot 9, panning (four values) |
| `007A8390` | 2, 8 | `11`<sub>h</sub> | `0C`<sub>h</sub> | slot 18 (`007BECD0`): ramps one of the `30`<sub>h</sub>-byte values at `+248`<sub>h</sub> |
| `007A7E00` | 2, 8, 9 | `12`<sub>h</sub> | | slot 10 (`007BE510`): sets bit 0 of `+518`<sub>h</sub> and writes 1 and 5.0 at `+1DC`<sub>h</sub>, `+20C`<sub>h</sub> and `+23C`<sub>h</sub>; 0 clears them |
| `007A8300` | 2, 8, 9 | `13`<sub>h</sub> | | slot 11 (`007BEC70`): sets bit 1 of `+518`<sub>h</sub> and writes 1 and 5.0 at `+AC`<sub>h</sub>; 0 clears them |
| `007A7CC0` | 2, 8, 9 | `14`<sub>h</sub> | | slot 12 (`007BE3E0`): stores a byte at `+3F8`<sub>h</sub> |
| `007A7D50` | 2, 8, 9 | `15`<sub>h</sub> | | slot 13, low-pass |
| `007A7C30` | 2, 8, 9 | `16`<sub>h</sub> | | slot 14 (`007BE3D0`): stores `+508`<sub>h</sub> |
| `007A7B10` | 2, 8, 9 | `17`<sub>h</sub> | | slot 15 (`007BE360`): stores `+50C`<sub>h</sub> |
| `007A7BA0` | 2, 8, 9 | `18`<sub>h</sub> | | slot 16 (`007BE3C0`): stores `+510`<sub>h</sub> |
| `007A8120` | 2, 9 | `19`<sub>h</sub> | `0E`<sub>h</sub> | slot 17 (`007BEAE0`): stores `+514`<sub>h</sub> |
| `007A77F0` | 7 | | `08`<sub>h</sub> | the source's slot 15 with three values: moves it |
| `007A8060` | 7 | | `07`<sub>h</sub> | the source's slot 14 with three values |

The slot numbers are those of the `Driver::Sound` vtable `01CB5A30`; types `0B`<sub>h</sub>-`0E`<sub>h</sub> (stop, pause, resume,
volume) are on [Sound engine](sound-engine.md). The other posters:

| Call | Type | Does |
|---|---:|---|
| `007A4660`, `007A4390`, `007A4530`, `007A45C0` | `01`<sub>h</sub>, `02`<sub>h</sub>, `04`<sub>h</sub>, `03`<sub>h</sub> | pause, resume, pitch ramp and volume ramp of a category |
| `007A44A0`, `007A4410` | `07`<sub>h</sub>, `08`<sub>h</sub> | store two bytes in a category, at `+80`<sub>h</sub> (`007AA4E0`) or `+82`<sub>h</sub> (`007AA4D0`) |
| `007A8FE0` | `09`<sub>h</sub> | stops every sound, music and instrument of a bank: `007D0A20` runs `007B4960`, `007B7CC0` and `007B8230`, which stop each object whose bank (`007BD8D0` for a sound) is that one |
| `007A93A0` | `1C`<sub>h</sub>, or `Lay` 6 | plays a music, or a `Lay` source |
| `007A9550`, `007A94D0`, `007A92C0`, `007A9650`, `007A95D0`, `007A90E0` | `1D`<sub>h</sub>, `21`<sub>h</sub>, `23`<sub>h</sub>, `26`<sub>h</sub>, `27`<sub>h</sub>, `28`<sub>h</sub> | music commands ([Interactive music](interactive-music.md)) |
| `007A46F0` | `2E`<sub>h</sub> | a mixer bus value; `007A47A0` packs the bus and parameter |
| `007A5300` | `30`<sub>h</sub> | applies an effect preset |
| `007A5380` | `32`<sub>h</sub> | copies a name into the driver's name buffer (`007AE470`) and posts it |
| `007A58D0`, `007A5670` | `Lay` 1, 2 | a placed request and the listener ([Spatial sound](spatial-sound.md)) |

The category calls reach `007AA680`, which pauses every sound, music and instrument of the category only when its
pause count `+64`<sub>h</sub> goes from 0 to 1, and `007AA3E0`, which resumes them only while the count is 1 and then lowers it, never below 0.

### Reading an object back

The queries look the object up under its kind's lock and ask it through a vtable slot; a `Lay` source answers through
its own slot:

| Query | Sound, music, instrument (slot) | `Lay` source (slot) |
|---|---|---|
| `007A7010` | the state, slot 21 (`007BD9A0`), as 0, 1, 2 or 3 (3 for state 4) | slot 2 |
| `007A67D0` | slot 28, three values (`007BD6F0`) | slot 26 |
| `007A71F0` | the switch value (`007BD9D0`; `007CEF00` for an instrument) | slot 24 |
| `007A7350` | slot 26 (`007BDBB0`) | slot 18 |
| `007A74D0` | slot 30, bit 1 of `+518`<sub>h</sub> | slot 29 |
| `007A6600` | slot 29, bit 0 of `+518`<sub>h</sub> | slot 28 |
| `007A5FB0` | slot 31, `+508`<sub>h</sub> | slot 32 |
| `007A76A0` | slot 34 with an index; for a sound `007BDD20`, the value of one ramp of `+248`<sub>h</sub> | slot 22 |
| `007A6130` | `+504`<sub>h</sub> of a sound | slot 27 |
| `007A6260` | a byte: `007BD5B0`, `007C5C70`, or an instrument's `+204`<sub>h</sub> | slot 30 |
| `007A6470` | 1.0 by default: `007BD680`, `007C5F70` or `007CEE80` | slot 31 |

`007A91D0` gives a music's play position in seconds (`007C6490`) and `007A9250` its `+650`<sub>h</sub>. The game's bank
classes call `007A7010` to ask whether a sound plays ([Audio manager](audio-manager.md)).

### The update passes

The driver thread `007A5400` measures the time since its last pass in seconds and runs, in this order:

1. `007B1380`, which advances the external-parameter ramps.
2. `007B6B00`, which runs each event (`007EEA00`) and frees it once its state `+08`<sub>h</sub> is 2.
3. The command queue (`007AB5C0`), then the master ramps (`007AAEA0`).
4. `007B2920`, one bank list per pass in turn (`02EAD408`), running each bank's slot 10 and retiring a bank once its
   slot 2 answers true: it leaves its lists and the hash table, runs slot 9 and is freed.
5. `007B4A70`, every sound: its update (slot 42), and in state 3 it is removed and freed. A sound that was waiting for
   its bank is rebuilt by the factory once the bank is ready, and `007BFFA0` carries its settings over.
6. `007B52B0` (sequences, freed in state 4), `007B5AD0` (tracks, freed in state 5), `007B7D60` (music, freed in
   state 7, giving back its track need) and, while instruments exist (`007B8220`), `007B82D0` (freed in state 7).
7. `007B6050` (voices, freed in state 3) and `007B99B0` (external sources), then the bus ramps (`007AD310`).
8. `Sleep(10)` (`007A5521`).

The driver's threads start through `007A5550`, which calls the function at `+08`<sub>h</sub> of its block with the argument at
`+10`<sub>h</sub>.

A list walk that meets an empty node prints "sequence NULL!!" and its neighbours (`007B4FC0`).

### Ramps

A ramped value holds a start, a target, the time so far and a duration; `007A9E00` gives its current value as
`start + curve(time / duration) x (target - start)`, through the curve `007A9E50`, or the target once the duration is
0. Category, bus and sound volumes, pitches and pans are all such ramps. `007BDAC0` gives a curved ramp's value: with a
curve at `+38`<sub>h</sub> the configuration curve shapes it (`007AE260`), run backwards when the target is below the start.

### Heap and clock

`007AD620` stores the allocate and free functions from the start-up block. `007AD550(size, tag)` allocates
`size + 16` bytes with a header of `5EAD5EAD`<sub>h</sub>, the tag and the size; `007AD4D0` also zeroes the block and
`007AD5A0` grows one by copying. `007AD6D0` reads the performance-counter frequency and start; `007AD630` gives counts
since the start and `007AD680` microseconds, which seed `srand` (`007A5404`).

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
