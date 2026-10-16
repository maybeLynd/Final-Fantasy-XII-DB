---
title: "Movies: the .mh seek index and the movie player's states"
kind: "format"
category: "Graphics"
summary: "The full-motion movie files and the object that plays them: the PS2-era .mh seek index shipped beside the movie paths and never read, how a movie id maps to its path pair, and the movie player singleton's start, update, fade-out and time read-outs that the script layer drives."
addresses: "01F81218, 001B7F20, 001B82F0, 001B7F30, 001B8400, 001B83B0, 001B82A0, 001B7D30, 001B7690, 001B77B0, 001B77E0, 00184810, 001848A0, 001848E0, 0035B840, 0035B8D0, 0035B740, 0035B7D0, 002DF980, 01ECB4D0"
---

## What the player sees

The story's pre-rendered cutscenes play as WebM videos with the voice track in the language set in
the options and the sound at the music volume. A movie asked to stop either ends at once or fades
its sound out over half a second first. Beside the movie paths the game still carries the PS2
seek indexes (`.mh`) of the old movie streams; nothing opens them.

## Where it comes from

Each movie id `m` owns two entries of the resource path kind 28 (`002DF980(0x1C, …)`): entry `2m`
is a PS2 `PS2Data\movie_finish\<lang>\<NAME>.md` path, entry `2m + 1` the matching `.mh` path. The
player keeps only the base name of the `.md` entry and opens `<NAME>.webm`; that path build and the
WebM pairing are on [Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md),
and the decoding is on [Media decoder libraries](../Third-Party-Libraries/media-decoder-libraries.md).

The `.mh` files ship under `ps2data/movie_finish/<lang>/`. No `.md` stream ships.

## Layouts

A `.mh` file is a 24-byte header and a table of 12-byte entries:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `char[4]` | magic | ".mhe" in all 43 files |
| `04` | `u8` | field04 | 1 in 3 files, 5 in 34, 9 in 6 |
| `05` | `u8` | field05 | 1 in all 43 |
| `06` | `u16` | field06 | a different value in each file |
| `08` | `u16` | width | 512 in all 43 |
| `0A` | `u16` | height | 352 in 37 files, 448 in 6 |
| `0C` | `u32` | streamBytes | above every entry offset |
| `10` | `u32` | frameCount | 1.000 to 1.049 times the last entry's frame |
| `14` | `u32` | entryCount | file size = `0x18` + 12 x entryCount |

Entry (`0x0C` bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | offset | byte offset into the PS2 stream; never decreases |
| `04` | `u32` | frame | frame number; 0 in the first entry, never decreases |
| `08` | `u32` | flags | 0, 1 or 2 |

The movie player is the singleton `01F81218` (getter `001B7F20`), `0xBB8` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000` | `i32` | movie id; -1 when idle |  |
| `004` | `i32` | state (0 to 6, below) |  |
| `008` | `u8` | the result of 0067A410, refreshed every update |  |
| `009` | `u8` | a frame has been fetched (0067ABF0) |  |
| `00C` | `f32` | sound volume: the Music volume option / 100 |  |
| `010` | `f32` | fade-out time left, seconds |  |
| `018` | `u64` | position, from 0067A2F0 |  |
| `020` | `u64` | duration, from 0067A340 |  |
| `02D` | `u8` | the fade-out also lowers the sound |  |
| `678` | `...` | the PVideoPlaybackWin32 playback object |  |
| `B5D` | `u8` | set by a stop request without fade |  |
| `BAC` | `u8` | a fading stop was requested |  |
| `BB0` | `u32` | audio language flag (+0x678 + 0x538): 1 when the Voice language option bit is set |  |

## Shipped data

| Fact | Value |
|---|---|
| `.mh` files | 43: `us` 35, `in` 7, `jp` 1; 228 to 94,356 bytes (`us/stf.mh` largest) |
| header checks | magic, size formula, ordered entries and last offset below `+0x0C` hold in 43 of 43 |
| entries | 14,589: flags 0 in 8,445, 2 in 6,105, 1 in 39 |
| `.mh` without a `.webm` of the same name | `jp/opd`, `in/bd2`, `in/se1`, `in/se2` |
| `.webm` without a `.mh` | `anx` |
| kind-28 entries | slots 0 to 97 hold 45 `.md` and 45 `.mh` paths in pairs; slots 76 to 81 and 92 to 93 are null, so ids 38, 39, 40 and 46 are empty and the array goes on past them |
| `.mh` paths by folder | `us` 36, `in` 8, `jp` 1; `in\ANX.mh` and `us\DLB.mh` have no file |
| `.mhe` in the executable | 0 occurrences |

## Loader behaviour

### The .mh is never read

The only fetch of an odd kind-28 entry is in the script-side start `0035B840`
(`0035B8AE`, `002DF980(0x1C, 2m + 1)`); the next instructions load the movie id into `ecx` and call
`001848A0`, which does not use the result. The executable contains no `.mhe` text, so no code checks
the magic.

### Starting a movie

`001848A0(m)` calls `001B82F0` on the singleton, which:

1. tears down any open playback (`0067A9B0` on `+0x678`);
2. stores the id, clears the position and `+0x09`, and sets state 1;
3. sets `+0xBB0` from the Voice language option (`002DEBB0`), which makes the decoder pick the
   non-English audio track;
4. stores the Music volume (`002DDC70`, at most 100) divided by 100 at `+0x0C`;
5. queues `001B7F30` as a job on the `AsyncJobManager` (`00199F10`, `0019A000`).

The job `001B7F30` starts the reading thread (`0067A350`), fetches entry `2m`, and opens the WebM. A
null entry resets the player (`001B7690`): id -1, position and duration 0, state 0. A failed open
sets state 0 and resets.

### The update

`001B8400(player, dt)` runs once a frame from the game application's pump
([Game application](../Engine-Core/game-application.md)):

| State | Meaning | What the update does |
|---|---|---|
| 0 | idle | nothing |
| 1 | opening | once `+0x08` is set, fetches a frame (`0067ABF0`) into `+0x09`; when one arrives it reads the position and duration and calls `0067A440` |
| 2 | ready | entered through `001B7D30` when `+0x08` and `+0x09` are both set |
| 3 | playing | entered through `001B82A0` when `+0x08` is set; keeps fetching frames; moves to state 4 when the position reaches the duration minus `0xE9` |
| 4 | ending | keeps fetching frames |
| 5 | closing | resets the player, tears down playback and calls `0017D960(1)`, `002E1CA0(1, 0x15)`, `00229AE0(1)` |
| 6 | fading out | subtracts `dt` from `+0x10`; while `+0x2D` is set, sets the sound volume to `+0x0C` x `+0x10` x 2 (`0067A990`); state 5 when `+0x10` drops below 0 |

In states 3 and 4, an update in which `0067A410` returns 0 sends the player to state 5 and resets it.

### Stopping

`001848E0(flag)` calls `001B83B0`. With the flag set (`0035B720` passes 1) it sets `+0xBAC` and,
unless the state is 0, 5 or 6, starts a half-second fade: state 6, `+0x10` = 0.5. With the flag
clear (`0035B8D0` passes 0) it sets `+0xB5D` unless `+0xBAC` is set, and moves to state 5 when no
fade time is left, so a running fade finishes first.

### The script side

`0035B740` polls the state through `00184860`: in state 1 it calls `001B7D30` (through `00184880`)
and returns 1; it returns 2 and 3 for those states and 0 otherwise. `0035B7D0` calls `001B82A0`
(through `001848C0`), which starts play only when `+0x08` is set. `0035B840` starts a movie and
`0035B8D0` stops it.

### The time read-outs

- `00184810` returns, in state 3 only, `+0x18 x 29.97 x 0.001` truncated; otherwise -1.
- `001B77B0` (through `001847B0`) returns `+0x18 x 0.0333667` truncated (`008F8D7C`).
- `001B77E0` (through `001847F0`) returns `+0x20 x 0.0333667 - 30`, clamped at 0; for movie id 43
  (`IVT`) it subtracts 8 instead (`01CEBC80`).

## Modding notes

- Editing or deleting a `.mh` changes nothing; replace the `.webm` instead.
- The audio track follows the Voice language option and the volume follows the Music volume option,
  read when the movie starts.
- A movie also closes when `0067A410` returns 0 during play, not only after its duration.

## Related

- [Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md): the kind-28
  path, the `.webm` name and the shipped WebM files.
- [Media decoder libraries](../Third-Party-Libraries/media-decoder-libraries.md): the movie open
  `0067A480` and the VP8 and Vorbis decode.
- [Game application](../Engine-Core/game-application.md): where `001B8400` runs.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): the Voice language and Music volume options.
- [Screen fades](screen-fades.md): the fades around a movie.
