---
title: "Movies: the .mh seek index and the movie player's states"
kind: "format"
category: "Graphics"
addresses: "01F81218, 001B7F20, 001B82F0, 001B7F30, 001B8400, 001B83B0, 001B82A0, 001B7D30, 001B7690, 001B77B0, 001B77E0, 00184810, 001848A0, 001848E0, 0035B840, 0035B8D0, 0035B740, 0035B7D0, 002DF980, 01ECB4D0"
---

## What the player sees

The story's pre-rendered cutscenes play as WebM videos with the voice track in the language set in
the options and the sound at the music volume. A movie asked to stop either ends at once or fades
its sound out over half a second first. Beside the movie paths the game still carries the PS2
seek indexes (`.mh`) of the old movie streams; nothing opens them.

## Where it comes from

Each movie id `m` owns two entries of the resource path kind 28 (`002DF980(1Ch, …)`): entry `2m`
is a PS2 `PS2Data\movie_finish\<lang>\<NAME>.md` path, entry `2m + 1` the matching `.mh` path. The
player keeps only the base name of the `.md` entry and opens `<NAME>.webm`; that path build and the
WebM pairing are on [Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md),
and the decoding is on [Media decoder libraries](../Third-Party-Libraries/media-decoder-libraries.md).

The `.mh` files ship under `ps2data/movie_finish/<lang>/`. No `.md` stream ships.

## Layouts

A `.mh` file is a 24-byte header and a table of 12-byte entries:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | magic | ".mhe" in all 43 files |
| `04`<sub>h</sub> | `u8` | field04 | 1 in 3 files, 5 in 34, 9 in 6 |
| `05`<sub>h</sub> | `u8` | field05 | 1 in all 43 |
| `06`<sub>h</sub> | `u16` | field06 | a different value in each file |
| `08`<sub>h</sub> | `u16` | width | 512 in all 43 |
| `0A`<sub>h</sub> | `u16` | height | 352 in 37 files, 448 in 6 |
| `0C`<sub>h</sub> | `u32` | streamBytes | above every entry offset |
| `10`<sub>h</sub> | `u32` | frameCount | 1.000 to 1.049 times the last entry's frame |
| `14`<sub>h</sub> | `u32` | entryCount | file size = `18`<sub>h</sub> + 12 x entryCount |

Entry (`0C`<sub>h</sub> bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | offset | byte offset into the PS2 stream; never decreases |
| `04`<sub>h</sub> | `u32` | frame | frame number; 0 in the first entry, never decreases |
| `08`<sub>h</sub> | `u32` | flags | 0, 1 or 2 |

The movie player is the singleton `01F81218` (getter `001B7F20`), `BB8`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `i32` | movie id; -1 when idle |  |
| `004`<sub>h</sub> | `i32` | state (0 to 6, below) |  |
| `008`<sub>h</sub> | `u8` | the result of 0067A410, refreshed every update |  |
| `009`<sub>h</sub> | `u8` | a frame has been fetched (0067ABF0) |  |
| `00C`<sub>h</sub> | `f32` | sound volume: the Music volume option / 100 |  |
| `010`<sub>h</sub> | `f32` | fade-out time left, seconds |  |
| `018`<sub>h</sub> | `u64` | position, from 0067A2F0 |  |
| `020`<sub>h</sub> | `u64` | duration, from 0067A340 |  |
| `02D`<sub>h</sub> | `u8` | the fade-out also lowers the sound |  |
| `678`<sub>h</sub> | `...` | the PVideoPlaybackWin32 playback object |  |
| `B5D`<sub>h</sub> | `u8` | set by a stop request without fade |  |
| `BAC`<sub>h</sub> | `u8` | a fading stop was requested |  |
| `BB0`<sub>h</sub> | `u32` | audio language flag (`+678`<sub>h</sub> + `538`<sub>h</sub>): 1 when the Voice language option bit is set |  |

## Shipped data

| Fact | Value |
|---|---|
| `.mh` files | 43: `us` 35, `in` 7, `jp` 1; 228 to 94,356 bytes (`us/stf.mh` largest) |
| header checks | magic, size formula, ordered entries and last offset below `+0C`<sub>h</sub> hold in 43 of 43 |
| entries | 14,589: flags 0 in 8,445, 2 in 6,105, 1 in 39 |
| `.mh` without a `.webm` of the same name | `jp/opd`, `in/bd2`, `in/se1`, `in/se2` |
| `.webm` without a `.mh` | `anx` |
| kind-28 entries | slots 0 to 97 hold 45 `.md` and 45 `.mh` paths in pairs; slots 76 to 81 and 92 to 93 are null, so ids 38, 39, 40 and 46 are empty and the array goes on past them |
| `.mh` paths by folder | `us` 36, `in` 8, `jp` 1; `in\ANX.mh` and `us\DLB.mh` have no file |
| `.mhe` in the executable | 0 occurrences |

## Loader behaviour

### The .mh is never read

The only fetch of an odd kind-28 entry is in the script-side start `0035B840`
(`0035B8AE`, `002DF980(1Ch, 2m + 1)`); the next instructions load the movie id into `ecx` and call
`001848A0`, which does not use the result. The executable contains no `.mhe` text, so no code checks
the magic.

### Starting a movie

`001848A0(m)` calls `001B82F0` on the singleton, which:

1. tears down any open playback (`0067A9B0` on `+678`<sub>h</sub>);
2. stores the id, clears the position and `+09`<sub>h</sub>, and sets state 1;
3. sets `+BB0`<sub>h</sub> from the Voice language option (`002DEBB0`), which makes the decoder pick the
   non-English audio track;
4. stores the Music volume (`002DDC70`, at most 100) divided by 100 at `+0C`<sub>h</sub>;
5. queues `001B7F30` as a job on the `AsyncJobManager` (`00199F10`, `0019A000`).

The job `001B7F30` starts the reading thread (`0067A350`), fetches entry `2m`, and opens the WebM. A
null entry resets the player (`001B7690`): id -1, position and duration 0, state 0. A failed open
sets state 0 and resets.

### The picture's geometry

The init burst builds the player's drawing side with `001B7850`. It loads
`/GameData/D3D11/ArtData/shaders/video.fx.phyre` (`0019CB20`) into `+D0`<sub>h</sub>, sizes three plane
textures (`0060DD70`), Y at `+108`<sub>h</sub> at 1920 × 1080 and U and V at `+290`<sub>h</sub> and `+418`<sub>h</sub> at 960 ×
540, each with four buffers (`00628100`), and binds them to the effect's `YChannel`, `UChannel` and
`VChannel` (`0018D240`, `001B81B0`).

It puts the effect into a one-entry `PMaterialSet` of the
player's cluster `+30`<sub>h</sub> (`001B80C0`), builds the geometry, keeps the mesh instance at `+100`<sub>h</sub>
with the material set at its `+20`<sub>h</sub>, and stores 16/9 (1.7777778) at `+668`<sub>h</sub>.

`001B72B0(player, cluster)` gives the cluster one `PMesh` (`02D3A640`) of one segment (`0C0`<sub>h</sub>
bytes, `001B7210`) unless it already has exactly one, sets the segment's `+18`<sub>h</sub> to 2, and fills
two vertex streams of three entries:

| Stream | Data type | Entry | Values |
|---|---|---|---|
| 0 | `Vertex` (`02D3AB18`) | 12 bytes | (−1, −1, 1), (3, −1, 1), (−1, 3, 1) |
| 1 | `ST` (`02D3AB48`) | 8 bytes | (0, 0), (2, 0), (0, 2) |

The one triangle covers the clip-space square with texture coordinates 0 to 1 across it, so the
movie fills whatever target it is drawn into. Before each write it waits, 1 ms at a time
(`Sleep`), while the buffer it is about to fill is still in use. It then builds the
`PMeshInstance` on the mesh with `001B6CE0`.

### The update

`001B8400(player, dt)` runs once a frame from the game application's pump
([Game application](../Engine-Core/game-application.md)):

| State | Meaning | What the update does |
|---|---|---|
| 0 | idle | nothing |
| 1 | opening | once `+08`<sub>h</sub> is set, fetches a frame (`0067ABF0`) into `+09`<sub>h</sub>; when one arrives it reads the position and duration and calls `0067A440` |
| 2 | ready | entered through `001B7D30` when `+08`<sub>h</sub> and `+09`<sub>h</sub> are both set |
| 3 | playing | entered through `001B82A0` when `+08`<sub>h</sub> is set; keeps fetching frames; moves to state 4 when the position reaches the duration minus `E9`<sub>h</sub> |
| 4 | ending | keeps fetching frames |
| 5 | closing | resets the player, tears down playback and calls `0017D960(1)`, `002E1CA0(1, 15h)`, `00229AE0(1)` |
| 6 | fading out | subtracts `dt` from `+10`<sub>h</sub>; while `+2D`<sub>h</sub> is set, sets the sound volume to `+0C`<sub>h</sub> x `+10`<sub>h</sub> x 2 (`0067A990`); state 5 when `+10`<sub>h</sub> drops below 0 |

In states 3 and 4, an update in which `0067A410` returns 0 sends the player to state 5 and resets it.

### Fetching a frame

The player's constructor `001B6D90` builds the playback object at `+678`<sub>h</sub> with `006791B0`, which
sets up its three queues (`+000`<sub>h</sub>, `+A8`<sub>h</sub>, `+150`<sub>h</sub>) and three locks and zeroes its counters and
flags, among them the state `+268`<sub>h</sub> and the audio flag `+538`<sub>h</sub>.

- Each queue is a `CDataFrameQueue` built by `006CC350`: its vtable, two locks (`00874D60`), two `20`<sub>h</sub>-byte frame
  lists and `00584730` as its free function. `006CC960` builds the `VbfMkvReader` (`0067922B`).
- `006CC730(queue, keep)` lets go of the frame a queue holds: with `keep` it pushes the frame onto the list at `+60`<sub>h</sub>
  (or `+80`<sub>h</sub> when `+A0`<sub>h</sub> is 0), otherwise it frees it through `+58`<sub>h</sub>; then it closes both lock handles
  (`005CD700`).
- `0067A970(playback, pause)` resets the playback's run event `+4D0`<sub>h</sub> to pause it and sets it to run again
  (`005CD500`, `005CD5E0`); `001B82A0` runs it with 0 (`001B82D2`) and `001B82F0` again (`001B835C`).

`0067ABF0(playback, y, u, v)`, from the update in states 1, 3 and 4, takes one decoded frame into
the player's three plane textures `+108`<sub>h</sub>, `+290`<sub>h</sub> and `+418`<sub>h</sub>:

- it counts its calls at `+530`<sub>h</sub>; while `001EDE70()` is set it acts only on every second call;
- it needs the state `+268`<sub>h</sub> at 1, and while `+4F4`<sub>h</sub> is set it waits until the frame queue
  `+A8`<sub>h</sub> holds at least `+2EC`<sub>h</sub> frames, then clears `+4F4`<sub>h</sub>;
- it takes the oldest frame (`006CC4F0`), uploads its three planes, the first at frame `+10`<sub>h</sub> and
  the others `+524`<sub>h</sub> and `+528`<sub>h</sub> bytes further on, counts the frame at `+278`<sub>h</sub>, releases it
  (`006CC550`) and returns 1.

`0067AB50(texture, data)` uploads one plane. It picks the texture's ring record by the counter
`01F7F5A0` modulo the ring size, waits 1 ms at a time while that record's in-use count `+38`<sub>h</sub> is
above 0, hands the data to `0062CC10`, which queues the upload, and stores the record index at
`+0C`<sub>h</sub>.

### Stopping

`001848E0(flag)` calls `001B83B0`. With the flag set (`0035B720` passes 1) it sets `+BAC`<sub>h</sub> and,
unless the state is 0, 5 or 6, starts a half-second fade: state 6, `+10`<sub>h</sub> = 0.5. With the flag
clear (`0035B8D0` passes 0) it sets `+B5D`<sub>h</sub> unless `+BAC`<sub>h</sub> is set, and moves to state 5 when no
fade time is left, so a running fade finishes first.

### The script side

`0035B740` polls the state through `00184860`: in state 1 it calls `001B7D30` (through `00184880`)
and returns 1; it returns 2 and 3 for those states and 0 otherwise. `0035B7D0` calls `001B82A0`
(through `001848C0`), which starts play only when `+08`<sub>h</sub> is set. `0035B840` starts a movie and
`0035B8D0` stops it.

`setmoviescreensize(n)` (`058C`<sub>h</sub>, `00347C40`) stores `n` at `02ADD933` through `0037B470`, or 3
for a negative `n`, and `getmoviescreensize` (`058D`<sub>h</sub>, `00347F40`) returns it (`0037B370`). The
movie start `0035B840` resets it to 3 (`0037B470(−1)`), and so does `0037B390` from the startup
constants `0022A0B0`. The only other reader, the loaded-file play `003B1BA0`, discards the value,
so the setting changes nothing on screen.

### The time read-outs

- `00184810` returns, in state 3 only, `+18h x 29.97 x 0.001` truncated; otherwise -1.
- `001B77B0` (through `001847B0`) returns `+18h x 0.0333667` truncated (`008F8D7C`).
- `001B77E0` (through `001847F0`) returns `+20h x 0.0333667 - 30`, clamped at 0; for movie id 43
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
