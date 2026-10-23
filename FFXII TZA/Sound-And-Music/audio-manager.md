---
title: "Audio manager: the five bank controllers, their bank pools, the sound objects and how a game request reaches a bank"
kind: "system"
category: "Sound and music"
addresses: "0x00210AF0, 0x002105E0, 0x00212710, 0x0021E570, 0x00221D60, 0x00211840, 0x00212970, 0x00210FF0"
---

## What the player sees

- Every sound effect, music track, battle voice and spoken line is loaded and played through one audio manager.
- At most 96 sound-effect blocks, 256 single sound banks, two music tracks, six battle-voice banks and four spoken
  lines can be loaded at one time.
- Sounds can be paused by kind, music apart from effects, and come back with a short fade when resumed.

## How it works

### The manager

`0x00210AF0` allocates the manager, `0x40` bytes, once and keeps it at `0x01FD36A0`; `0x00210B30` returns that pointer to
every caller. Its builder `0x002105E0` creates one controller per bank family:

| Manager offset | Controller | Built by | Bank class | Bank size | Pool |
|---|---|---|---|---|---:|
| `+0x00` | `MusicAudioController` | `0x00217FD0` | `MusicAudioBank` | `0x58` | 2 |
| `+0x08` | `SebAudioController` | `0x0021A9F0` | `SebAudioBank` | `0xA0` | 96 |
| `+0x10` | `SepAudioController` | `0x00219400` | `SepAudioBank` | `0x68` | 256 |
| `+0x18` | `StreamAudioController` | `0x0021CC10` | `StreamAudioBank` | `0x48` | 4 |
| `+0x20` | `ShoutAudioController` | `0x0021BDB0` | `ShoutAudioBank` | `0x68` | 6 |

The pool counts are immediate operands of the five builders. The bank families and their files are on
[Sound banks](sound-banks.md).

### Controllers and the live list

Every controller starts from the base `0x00212710`, which installs the `AudioController` vtable `0x00906CD0` and an empty
EASTL list at `+0x08`. That list holds the controller's loaded banks, and every per-bank request walks it:

- `0x00212910` asks each bank to drop its finished sounds (`0x00222050`);
- `0x00212B80` stops the sound with one handle in each bank over 0.1 s (`0x00222390`);
- `0x00212BD0`, `0x00212AE0`, `0x00212A90` and `0x00212B30` call bank vtable slot 0, 3, 4 or 5, the four pause groups below.

### Bank pools

Each controller owns a pool at `+0x20`: an EASTL vector of its bank objects and two EASTL sets of bank pointers. The
reserve step puts every bank in the first set, the free set (`0x00218990`). Taking a bank moves the set's first node to
the second set and rebuilds the bank in place: `0x0021C280` does this for battle voices and calls the
`ShoutAudioBank` builder `0x00224BF0` on it. Each pool is its own template instance:

| Bank class | Pool build, reserve, resize, insert, erase | Element copies, fill and destroy |
|---|---|---|
| `MusicAudioBank` | `0x00217E10`, `0x00218990`, `0x00218E80`, `0x00218380`, `0x00218880` | `0x00217BA0`, `0x00217C30`, `0x00217CC0`, `0x00217D70`, `0x00218100` |
| `SepAudioBank` | `0x00219300`, `0x00219B20`, `0x00219CA0`, `0x002196A0`, `0x00219A70` | `0x00218F40`, `0x00219000`, `0x002190B0`, `0x00219170`, `0x00219240` |
| `SebAudioBank` | `0x0021A820`, `0x0021B160`, `0x0021B350`, `0x0021AC90`, `0x0021B030` | `0x0021A340`, `0x0021A4E0`, `0x0021A5A0`, `0x0021A670`, `0x0021A750` |
| `ShoutAudioBank` | `0x0021BCB0`, `0x0021C450`, `0x0021C4F0`, `0x0021BFD0`, `0x0021C330` | `0x0021B8F0`, `0x0021B9B0`, `0x0021BA60`, `0x0021BB20`, `0x0021BBF0`, `0x0021BE80` |
| `StreamAudioBank` | `0x0021CB10`, `0x0021D440`, `0x0021D580`, `0x0021CE30`, `0x0021D330` | `0x0021C8D0`, `0x0021C960`, `0x0021C9F0`, `0x0021CA90`, `0x0021CCE0` |

Every bank class starts from `AudioBank`: `0x00221780` builds it with a family number at `+0x34` and an empty sound
list at `+0x08`. `0x00217F10` copies one, appending its list through `0x00217B10`, and the element copies assign one
list to another through `0x002181A0`. The class builders are `0x002226A0` (music, family 1), `0x002235F0` (block, 2),
`0x00222CB0` (six-digit, 4), `0x00225160` (spoken line, 6) and `0x00224BF0` (battle voice, 8). The block bank's destructor
`0x00223730` frees its slot map at `+0x58` through `0x002236B0`.

### The object manager

`0x002216B0` builds the object manager, `0x8D8` bytes at `0x01FD4138`, from the sound start-up `0x00210760` with 1,024 bank
objects and 1,024 sound objects (`0x0021088E`); `0x00221710` returns it. Its constructor `0x0021E570` lays out five pools of
the same vector-and-sets shape:

| Offset | Holds | Element | Count | Taken by |
|---|---|---|---:|---|
| `+0x008` | `AudioSeadObjectBank` | `0x30` | 1,024 | `0x00220CE0`, under the lock at `+0x300` |
| `+0x0A0` | `AudioSeadObjectSound` | `0x30` | 1,024 | `0x00220D30` |
| `+0x138` | slot nodes of block banks | 10 bytes | 2,048 | `0x00220CD0` |
| `+0x1D0` | `MemoryStreamingReader` | `0x28` | 32 | `0x00220D40`, under the lock at `+0x350` |
| `+0x268` | `MusicStreamingReader` | `0x218` | 5 | `0x00220C70`, under the lock at `+0x378` |

The resume table of [Music](music.md) follows at `+0x3D8` and `+0x7D8`. Each pool's template code:

| Pool | Build | Insert, erase | Element copies and destroy |
|---|---|---|---|
| bank objects | `0x0021E190` | `0x0021F440`, `0x00220860` | `0x0021D990`, `0x0021DD40`, `0x0021E020` |
| sound objects | `0x0021E280` | `0x0021F790`, `0x00220960` | `0x0021DA50`, `0x0021DAD0`, `0x0021DDD0`, `0x0021DEE0` |
| slot nodes | `0x0021E090` | `0x0021F130`, `0x002207E0` | `0x0021E730`, `0x0021EBC0` |
| memory readers | `0x0021E370` | `0x0021FB20`, `0x00220A00` | `0x0021DA00`, `0x0021DE80` |
| music readers | `0x0021E470`, reserve `0x00221060`, resize `0x002215D0` | `0x0021FEF0`, `0x00220AE0` | `0x0021DB50`, `0x0021DBE0`, `0x0021DC60`, `0x0021DF70` |

### Bank objects and sound objects

A bank keeps its driver bank object at `+0x20`. `0x00221D10` returns it, taking one from the pool on first use, and
`0x00221C70` does the same and passes it to the driver with a sound object and its slot (`0x007A87C0`). A sound object
is the game's handle on one driver `Sound`, kept in the bank's sound list:

1. `0x00221D60` takes a sound object (`0x00220D30`) and appends it to the bank's list. When the pool is empty it first
   sweeps finished sounds from every bank of the block, six-digit and battle-voice controllers (`0x00210A60`) and tries
   once more.
2. `0x00221E60`, `0x00221ED0` and `0x00221F40` find a bank's sound by slot `+0x14`, handle `+0x18` or id `+0x24`.
   `0x00221E00` sweeps, then returns the sound for a slot or takes a new one.
3. `0x00222050` sweeps the bank's list and the pending list at `0x01FD4140`; `0x00222280` returns each sound in state 0 or 2
   to the pool (`0x00221210`).
4. `0x00222080` and `0x002225B0` stop every sound of a bank, over 0.1 s or `frames / 60` s, and park them on the pending
   list until they finish; `0x00222410` stops only the sounds with one id over 0.1 s.

`0x002256B0` resets a sound object to slot -1, volume `0x7F`, pan `0x40` and state 2. `0x002255B0` and `0x00225CC0` store a
bank object's two data pointers and a memory reader's data and size.

### Bank methods

Every bank class answers the same requests through its own methods:

| Class | Methods |
|---|---|
| `MusicAudioBank` | play `0x002228A0`, is playing `0x00222A20` (driver state 2), keep the position `0x00222A40`, stop with a fade `0x00222A80`, music version `0x00222AD0`, volume `0x00222B20`, volume over frames `0x00222B70` |
| `SepAudioBank` | start `0x00223190` through `0x00223030` and `0x00223160`, stop `0x00223300`, volume `0x00223410`, pan `0x00223060`; every sound's pan `0x00222490` and volume `0x002224F0` |
| `SebAudioBank` | start `0x00224570` through `0x00223EB0` and `0x00224540`, stop `0x00224870`, position `0x00224890`, volume `0x002249D0` |
| `ShoutAudioBank` | language `0x00224C40`, keep one language's data `0x00224DC0`, play at a point `0x00224E40` (kind 9), play `0x00224F10` (kind 8), stop `0x00225000`, release `0x00225030` |
| `StreamAudioBank` | open `0x002251B0`, play or resume `0x002252C0` (kind 6), pan `0x00225280`, is playing `0x002253D0`, volume `0x00225400` |

The kind is stored at sound `+0x2C` (`0x002256E0`). For a six-digit or block bank, `0x00222170` answers whether a handle,
or with 0 any sound, still plays; `0x0021B2F0` asks it of every bank of one controller. A battle-voice bank holds both
language copies, at `+0x50` (language 0) and `+0x48`, and `0x00224C40` loads the chosen one into its driver bank.
`0x00225030(bank, language)` releases the driver bank and keeps fresh copies of the other language, or of both for
-1. A music bank's reader opens its file and keeps its name through `0x00225C40`.

### How a request reaches a bank

The play calls of [Sound effects](sound-effects.md) reach the manager through one-line forwarders, each of which
fetches the manager with `0x00210B30` and calls one method:

| Forwarder | Manager method | Goes to | Does | Caller |
|---|---|---|---|---|
| `0x001DBE00` | `0x00210BE0` | block `0x0021B200` or six-digit `0x00219BC0` | plays a placed sound with a new handle | `0x002DEFA0` |
| `0x001DBED0` | `0x00210CD0` | block, then six-digit `0x0021B720` | moves a playing sound (`0x007A77F0`) | `0x002DF120` |
| `0x001DBFA0` | `0x00210E10` | block `0x0021B870`, then six-digit `0x0021A2C0` | sets a volume over frames | `0x002DF1A0`, `0x002DF1E0` |
| `0x001DC000` | `0x00210F60` | the spatial layer | posts `Lay` action 1 with a position and a target | `0x002DF2C0` |
| `0x001DC390` | `0x00211340` | the spatial layer | posts `Lay` action 2, the listener ([Spatial sound](spatial-sound.md)) | `0x002DF560` |
| `0x001DC040` | `0x002110C0` | the mixer | posts driver action `0x2E` for parameter 0 with two values over 127 | `0x002DE360` |
| `0x001DC090` | `0x00211140` | the mixer | posts action `0x2E` for parameter 7 at `volume / 127` over `frames / 60` s | `0x002DF410` |
| `0x001DC190` | `0x00211200` | battle voice `0x0021C760` | plays a battle-voice line at a point | `0x002DF460` |
| `0x001DC1E0` | `0x00211210` | battle voice `0x0021C7E0` | plays a battle-voice line | `0x002DF4D0` |
| `0x001DC2E0` | `0x00211270` | spoken line `0x0021D770` | opens a line's stream | `0x002DF660` |
| `0x001DC280` | `0x00211230` | spoken line `0x0021D6B0` | plays a line at a pan and volume | `0x002DF680` |
| `0x001DC2C0` | `0x00211260` | spoken line `0x0021D700` | answers whether a line still plays | `0x003E9A10` |
| `0x001DC330` | `0x00211280` | spoken line `0x0021D840`, then battle voice `0x0021C870` | stops | `0x002DF690`, `0x003A0E80` |
| `0x001DC240` | `0x00211220` | spoken line `0x0021D640` | pans a line | `0x002DF610` |
| `0x001DC350` | `0x002112C0` | spoken line `0x0021D920` | sets a line's volume | `0x002DF6A0` |
| `0x001DBB00` | `0x002112D0` | category volume | sets a category to 1.0 or 0 at once (action 3) | `0x001D1660` |
| `0x001DBE60` | `0x00210C40` | six-digit `0x0021A040` | loads a six-digit bank | `0x002DF070` |
| `0x001DBE90` | `0x00210C50` | with a handle, every block and six-digit bank (`0x00212B80`); by id, block `0x0021B640` or six-digit `0x0021A100` | stops | `0x002DF0F0`, `0x002DEE70` |

A request that two families can own asks the block controller first and the six-digit one only when no block bank
takes it (`0x00210CD0`, `0x00210E10`). The six-digit stop `0x0021A100` stops every sound of
the bank with that id, of every bank for -1 and -3, and runs bank slot 1 on every bank for -4 (`0x00223300`). `0x00210710`, called by both starts, runs bank slot 6 over every six-digit bank and,
when none answered, over every block bank (`0x0021B0D0`, slot 2 of both controllers' vtables `0x00907BA8` and `0x00907DE0`); the block bank's slot 6 is `0x002238F0`, the one-at-a-time fade
of flag bit 6.

### Load ids

A load is tracked by an id in the 128-entry table `0x01FD36C0`, eight bytes per entry: the id and a count:

1. `0x002129F0(out, count)` asks `0x00212970` for an entry. It takes the next id from `0x01FD36B0`, 1 to `0x7FFFFFFF`
   and then 1 again, writes it to out and stores it in the first free entry from the rotating cursor `0x01E027D0`.
   With no free entry out is 0.
2. `0x00212A70(index)` frees the entry, for example once a battle-voice bank's data is in (`0x00224DC0`); an index of
   128 or more is ignored.
3. `0x00212A10(id)` answers the entry's index plus one while id is pending and 0 once it is done. Id 0 answers the
   highest pending entry plus one. A negative id answers 0 even while loads are pending (`0x00212A56`-`0x00212A5F`).

`0x002DEE90(id)` is that query through `0x00210AE0`. With -1 it calls `0x00212A10(-1)` once, gets 0 and returns without
waiting.

### The file load thread

The `AudioFileLoadManager` object, `0x158` bytes at `0x01FD36A8`, reads bank files on its own thread:

1. `0x00211840` builds it with 1,024 request records of `0x128` bytes (`0x002116B0`), and `0x00212130` starts the thread
   named `AudioFileLoadManager`.
2. `0x002120E0` takes a free record and `0x002121C0` queues it, or runs it at once.
3. The thread `0x00212600` takes the request at the tail of the queue, the one queued last, or sleeps 1 ms when there
   is none.
4. `0x00212050` runs it: kind 1 reads the whole file named at `+0x20` into a new buffer (`0x00212260`), then the record's
   callback runs and the record goes back to the free set.
5. A bank's callback `0x00222200` calls bank slot 8 when the bank is still loading (`+0x30` = 1). Otherwise it cancels
   the bank's other queued requests (`0x00212300`) and releases the bank.

The request vector's own code is `0x002123E0`, `0x00211BC0`, `0x00211530`, `0x00211600`, `0x00211480` and `0x002113D0`, and
`0x002118E0`, `0x00211A60` and `0x00211AC0` tear it down.

### Pausing by kind

`0x002DF370(mask, on, force)` keeps the paused kinds at `0x0215EFD8` and passes a change to `0x00210FF0`
(through `0x001DBA90`), which stores the mask at manager `+0x3C` and the switch at `+0x38`:

| Mask bit | Pauses |
|---|---|
| `0x01` | music banks, bank slot 0 |
| `0x02` | every block and six-digit bank, slot 0 |
| `0x04` | every spoken line and battle-voice bank, slot 0 |
| `0x08`, `0x10`, `0x20` | without `0x02`: block and six-digit banks' slots 3, 4 and 5 |

Slot 0 of the other classes, `0x00222550`, runs slot 9 on each sound, `0x00222340`: pause (`0x007A8590`) or resume with a
0.1 s fade (`0x007A7A20`). The music bank's slot 0, `0x00222C00`, does the same with 0.1 s both ways. The block bank's
slot 9, `0x00223F40`, never pauses slots 2 and `0x59` of block 0. `0x00229AB0(on)` pauses or resumes all six bits.

`0x00224B30` pauses a new block sound at once when the switch is on, the game mode `0x00229EA0` is 5 or 6 (`0x002287A0`)
and the bank is not block 0. `0x02` pauses it; `0x08`, `0x10` and `0x20` pause it by its slot's flag byte (copy `+9`):

| Bit | Function | Pauses when |
|---|---|---|
| `0x08` | `0x00224290` | flag bit 0 set and bits 3, 5 and 6 clear |
| `0x10` | `0x002240B0` | flags `0x69` all clear |
| `0x20` | `0x00224470` | flag bit 0 clear and the sound id over 1,000 is 150 |

The id test reads sound `+0x24`, which a block sound holds with bit 31 set (`0x002245ED`, `0x00224789`). Divided by 1,000
as a signed number (`0x00224493`-`0x002244A5`) it is never 150, so bit `0x20` pauses no new block sound, and the id test
of bits `0x08` and `0x10` never excludes one.

## Layouts

The sound object, `AudioSeadObjectSound`, `0x30` bytes, in the object manager's pool at `+0x0A0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | `AudioSeadObjectSound` |
| `+0x08` | `void*` | sound | the driver `Sound` the play, stop and ramp calls act on |
| `+0x10` | `i32` | state | 1 once started, 2 when the start fails; `0x00222280` returns states 0 and 2 to the pool |
| `+0x14` | `i32` | slot | the block slot, or 0 for a line (`0x002257D0`) |
| `+0x18` | `i32` | handle | the play handle (`0x00225580`) |
| `+0x1C` | `i32` | volume | 0-127 |
| `+0x20` | `i32` | pan | the pan byte (`0x002256F0`) |
| `+0x24` | `i32` | id | the sound id (`0x002257C0`) |
| `+0x2C` | `i32` | kind | 6 line, 8 battle voice, 9 placed battle voice (`0x002256E0`) |

The manager, `0x40` bytes at `0x01FD36A0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `MusicAudioController*` | music | |
| `+0x08` | `SebAudioController*` | block | |
| `+0x10` | `SepAudioController*` | sixDigit | |
| `+0x18` | `StreamAudioController*` | line | |
| `+0x20` | `ShoutAudioController*` | battleVoice | |
| `+0x28` | `void*` | callback | the `AudioCallback` vtable the driver reports to |
| `+0x30` | `i32` | musicVersion | -1 when built; 0-2 from the Config option ([Music](music.md)) |
| `+0x38` | `u32` | pauseOn | the last pause switch |
| `+0x3C` | `u32` | pauseMask | the paused kinds |

## State

The pending list at `0x01FD4140` is a two-way list with its own head node: `+0x00` the first node, `+0x08` the last,
then its allocator at `0x01FD4150`, named "EASTL list" (`0x001601C0`). Each node holds the next node, the previous node
and the sound object (`+0x10`), `0x18` bytes. `0x00222080` and `0x002225B0` put each stopped sound at the end
(`0x002220D4`-`0x00222110`, `0x00222604`-`0x00222640`); `0x00222280`, the sweep, unlinks a node through the list address it
is given (`0x002222EF`-`0x00222318`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01FD4148` | `void*` | 0 | the pending list's last node, the head node itself when the list is empty | `0x001601C0`, the head (`0x001601DB`, `0x001601FC`); `0x00222080` (`0x00222110`); `0x002225B0` (`0x00222640`); `0x00222280` when it unlinks the last node (`0x00222307`), through the address `0x00221E00` (`0x00221E1D`) and `0x00222050` (`0x0022205F`) pass | `0x00222080` (`0x002220FB`, `0x00222106`); `0x002225B0` (`0x0022262B`, `0x00222636`); `0x00222280` (`0x002222F2`), the same way |
| `0x0215EFDC` | `i32` | 0 | a running number given to each spoken-line stream as it opens: `0x002DF660` passes it through `0x001DC2E0`, `0x00211270` and `0x0021D770` to the stream bank's open `0x002251B0`, which keeps it at the bank's `+0x3C` (`0x002251F7`), and adds 1 (`0x002DF660`-`0x002DF673`) | `0x002DF660` (`0x002DF673`) | `0x002DF660` (`0x002DF660`), from `0x003B9136`, `0x003E9CEC` and `0x003EAE9B` |

No other instruction reaches these two. The list's address is taken by `0x001601C0`, `0x00221E00`, `0x00222050`, `0x00222080`,
`0x002225B0` and `0x008A80F0`, which frees its nodes at exit.

## Modding notes

- The pool counts are the second argument to each pool builder in `0x00217FD0`, `0x0021A9F0`, `0x00219400`, `0x0021BDB0` and
  `0x0021CC10`; the bank vector is sized once from it.
- A script or map that needs more than 96 sound-effect blocks loaded at once runs out of `SebAudioBank` objects.
- Waiting on load id -1 does not wait; wait on a bank's own id.

## Related

- [Sound effects](sound-effects.md) - the play calls in front of the manager.
- [Sound banks](sound-banks.md) - the bank families and their files.
- [Sound engine](sound-engine.md) - the driver behind the bank and sound objects.
- [Music](music.md) - the music bank's version and resume table.
- [Voices](voices.md) - the spoken-line streams.
