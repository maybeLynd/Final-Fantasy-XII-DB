---
title: "Movies: the .mh seek index and the movie player's states"
kind: "format"
category: "Graphics"
addresses: "0x01F81218, 0x001B7F20, 0x001B82F0, 0x001B7F30, 0x001B8400, 0x001B83B0, 0x001B82A0, 0x001B7D30, 0x001B7690, 0x001B77B0, 0x001B77E0, 0x00184810, 0x001848A0, 0x001848E0, 0x0035B840, 0x0035B8D0, 0x0035B740, 0x0035B7D0, 0x002DF980, 0x01ECB4D0"
---

## What the player sees

The story's pre-rendered cutscenes play as WebM videos with the voice track in the language set in
the options and the sound at the music volume. A movie asked to stop either ends at once or fades
its sound out over half a second first. Beside the movie paths the game still carries the PS2
seek indexes (`.mh`) of the old movie streams; nothing opens them.

## Where it comes from

Each movie id `m` owns two entries of the resource path kind 28 (`0x002DF980(0x1C, …)`): entry `2m`
is a PS2 `PS2Data\movie_finish\<lang>\<NAME>.md` path, entry `2m + 1` the matching `.mh` path. The
player keeps only the base name of the `.md` entry and opens `<NAME>.webm`; that path build and the
WebM pairing are on [Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md),
and the decoding is on [Media decoder libraries](../Third-Party-Libraries/media-decoder-libraries.md).

The `.mh` files ship under `ps2data/movie_finish/<lang>/`. No `.md` stream ships.

## Layouts

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PMaterialSet` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u8[4]` | pad04 | the four bytes between the material count at `+0x00` (returned by the script accessor getMaterialCount, `0x005C4CC0`) and the material pointer at `+0x08` of the PSharray header; no registered member covers it (`0x00662280` registers the `0x10`-byte class at `0x006622D0`) |

### Movie files and the player

The structures below are the ones the mechanisms above use.

All multi-byte fields are little-endian.

A `.mh` file is a 24-byte header and a table of 12-byte entries. The game never opens one
([the .mh is never read](#the-mh-is-never-read)), so it has no form in memory; the layout is that of the
shipped files:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | ".mhe" in all 43 files |
| `+0x04` | `u8` | field04 | 1 in 3 files, 5 in 34, 9 in 6 |
| `+0x05` | `u8` | field05 | 1 in all 43 |
| `+0x06` | `u16` | field06 | a different value in each file |
| `+0x08` | `u16` | width | 512 in all 43 |
| `+0x0A` | `u16` | height | 352 in 37 files, 448 in 6 |
| `+0x0C` | `u32` | streamBytes | above every entry offset |
| `+0x10` | `u32` | frameCount | 1.000 to 1.049 times the last entry's frame |
| `+0x14` | `u32` | entryCount | file size = `0x18` + 12 x entryCount |

Entry (`0x0C` bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | offset | byte offset into the PS2 stream; never decreases |
| `+0x04` | `u32` | frame | frame number; 0 in the first entry, never decreases |
| `+0x08` | `u32` | flags | 0, 1 or 2 |

The movie player is the singleton `0x01F81218` (getter `0x001B7F20`), `0xBB8` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `i32` | movie id; -1 when idle |  |
| `+0x004` | `i32` | state (0 to 6, below) |  |
| `+0x008` | `u8` | the result of 0x0067A410, refreshed every update |  |
| `+0x009` | `u8` | a frame has been fetched (0x0067ABF0) |  |
| `+0x00C` | `f32` | sound volume: the Music volume option / 100 |  |
| `+0x010` | `f32` | fade-out time left, seconds |  |
| `+0x018` | `u64` | position, from 0x0067A2F0 |  |
| `+0x020` | `u64` | duration, from 0x0067A340 |  |
| `+0x02D` | `u8` | the fade-out also lowers the sound |  |
| `+0x678` | `...` | the PVideoPlaybackWin32 playback object |  |
| `+0xB5D` | `u8` | set by a stop request without fade |  |
| `+0xBAC` | `u8` | a fading stop was requested |  |
| `+0xBB0` | `u32` | audio language flag (+0x678 + 0x538): 1 when the Voice language option bit is set |  |

## Shipped data

| Fact | Value |
|---|---|
| `.mh` files | 43: `us` 35, `in` 7, `jp` 1; 228 to 94,356 bytes (`us/stf.mh` largest) |
| header checks | magic, size formula, ordered entries and last offset below `+0x0C` hold in 43 of 43 |
| entries | 14,589: flags 0 in 8,445, 2 in 6,105, 1 in 39 |
| `.mh` without a `.webm` of the same name | `jp/opd`, `in/bd2`, `in/se1`, `in/se2` |
| `.webm` without a `.mh` | `anx` |
| every `.mh` | one row each in [`movies-mh-rows.tsv`](movies-mh-rows.tsv), 43 rows: language, name, size, SHA-256 prefix, every header field, the entry count, the entries with flags 0, 1 and 2, the last entry's frame, and whether a `.webm` of the same name ships |
| kind-28 entries | slots 0 to 97 hold 45 `.md` and 45 `.mh` paths in pairs; slots 76 to 81 and 92 to 93 are null, so ids 38, 39, 40 and 46 are empty and the array goes on past them |
| `.mh` paths by folder | `us` 36, `in` 8, `jp` 1; `in\ANX.mh` and `us\DLB.mh` have no file |
| `.mhe` in the executable | 0 occurrences |

## Loader behaviour

### The .mh is never read

The only fetch of an odd kind-28 entry is in the script-side start `0x0035B840`
(`0x0035B8AE`, `0x002DF980(0x1C, 2m + 1)`); the next instructions load the movie id into `ecx` and call
`0x001848A0`, which does not use the result. The executable contains no `.mhe` text, so no code checks
the magic.

### Starting a movie

`0x001848A0(m)` calls `0x001B82F0` on the singleton, which:

1. tears down any open playback (`0x0067A9B0` on `+0x678`);
2. stores the id, clears the position and `+0x09`, and sets state 1;
3. sets `+0xBB0` from the Voice language option (`0x002DEBB0`), which makes the decoder pick the
   non-English audio track;
4. stores the Music volume (`0x002DDC70`, at most 100) divided by 100 at `+0x0C`;
5. queues `0x001B7F30` as a job on the `AsyncJobManager` (`0x00199F10`, `0x0019A000`).

The job `0x001B7F30` starts the reading thread (`0x0067A350`), fetches entry `2m`, and opens the WebM. A
null entry resets the player (`0x001B7690`): id -1, position and duration 0, state 0. A failed open
sets state 0 and resets.

### The picture's geometry

The init burst builds the player's drawing side with `0x001B7850`. It loads
`/GameData/D3D11/ArtData/shaders/video.fx.phyre` (`0x0019CB20`) into `+0xD0`, sizes three plane
textures (`0x0060DD70`), Y at `+0x108` at 1920 × 1080 and U and V at `+0x290` and `+0x418` at 960 ×
540, each with four buffers (`0x00628100`), and binds them to the effect's `YChannel`, `UChannel` and
`VChannel` (`0x0018D240`, `0x001B81B0`).

It puts the effect into a one-entry `PMaterialSet` of the
player's cluster `+0x30` (`0x001B80C0`), builds the geometry, keeps the mesh instance at `+0x100`
with the material set at its `+0x20`, and stores 16/9 (1.7777778) at `+0x668`.

`0x001B72B0(player, cluster)` gives the cluster one `PMesh` (`0x02D3A640`) of one segment (`0x0C0`
bytes, `0x001B7210`) unless it already has exactly one, sets the segment's `+0x18` to 2, and fills
two vertex streams of three entries:

| Stream | Data type | Entry | Values |
|---|---|---|---|
| 0 | `Vertex` (`0x02D3AB18`) | 12 bytes | (−1, −1, 1), (3, −1, 1), (−1, 3, 1) |
| 1 | `ST` (`0x02D3AB48`) | 8 bytes | (0, 0), (2, 0), (0, 2) |

The one triangle covers the clip-space square with texture coordinates 0 to 1 across it, so the
movie fills whatever target it is drawn into. Before each write it waits, 1 ms at a time
(`Sleep`), while the buffer it is about to fill is still in use. It then builds the
`PMeshInstance` on the mesh with `0x001B6CE0`.

### The update

`0x001B8400(player, dt)` runs once a frame from the game application's pump
([Game application](../Engine-Core/game-application.md)). First, in every state, when `0x0017D980()`
(`[0x01F7F4B8]`) and `[0x01FD4A68]` are both 0 it releases the kept frames: `0x0067AB40(player + 0x678)` calls
`0x006CC860(q)` with the queue `q` at `+0xA8`, which passes each frame on the list `q + 0x60 + 0x20 x side` (`side =
[q + 0xA0]`) to the free function at `q + 0x58`, empties the list and sets `side = (side == 0)` (`0x001B8411`-`0x001B8429`).
Then, by state:

| State | Meaning | What the update does |
|---|---|---|
| 0 | idle | nothing more |
| 1 | opening | once `+0x08` is set, fetches a frame (`0x0067ABF0`) into `+0x09`; when one arrives it reads the position and duration and calls `0x0067A440` |
| 2 | ready | entered through `0x001B7D30` when `+0x08` and `+0x09` are both set |
| 3 | playing | entered through `0x001B82A0` when `+0x08` is set; keeps fetching frames; moves to state 4 when the position reaches the duration minus `0xE9` |
| 4 | ending | keeps fetching frames |
| 5 | closing | resets the player, tears down playback and calls `0x0017D960(1)`, `0x002E1CA0(1, 0x15)`, `0x00229AE0(1)` |
| 6 | fading out | subtracts `dt` from `+0x10`; while `+0x2D` is set, sets the sound volume to `+0x0C` x `+0x10` x 2 (`0x0067A990`); state 5 when `+0x10` drops below 0 |

In states 3 and 4, an update in which `0x0067A410` returns 0 sends the player to state 5 and resets it.

### Fetching a frame

The player's constructor `0x001B6D90` builds the playback object at `+0x678` with `0x006791B0`, which
sets up its three queues (`+0x000`, `+0xA8`, `+0x150`) and three locks and zeroes its counters and
flags, among them the state `+0x268` and the audio flag `+0x538`.

- Each queue is a `CDataFrameQueue` built by `0x006CC350`: its vtable, two locks (`0x00874D60`), two 0x20-byte frame
  lists and `0x00584730` as its free function. `0x006CC960` builds the `VbfMkvReader` (`0x0067922B`).
- `0x006CC730(queue, keep)` lets go of the frame a queue holds: with `keep` it pushes the frame onto the list at `+0x60`
  (or `+0x80` when `+0xA0` is 0), otherwise it frees it through `+0x58`; then it closes both lock handles
  (`0x005CD700`).
- `0x0067A970(playback, pause)` resets the playback's run event `+0x4D0` to pause it and sets it to run again
  (`0x005CD500`, `0x005CD5E0`); `0x001B82A0` runs it with 0 (`0x001B82D2`) and `0x001B82F0` again (`0x001B835C`).

`0x0067ABF0(playback, y, u, v)`, from the update in states 1, 3 and 4, takes one decoded frame into
the player's three plane textures `+0x108`, `+0x290` and `+0x418`:

- it counts its calls at `+0x530`; while `0x001EDE70()` is set it acts only on every second call;
- it needs the state `+0x268` at 1, and while `+0x4F4` is set it waits until the frame queue
  `+0xA8` holds at least `+0x2EC` frames, then clears `+0x4F4`;
- it takes the oldest frame (`0x006CC4F0`), uploads its three planes, the first at frame `+0x10` and
  the others `+0x524` and `+0x528` bytes further on, counts the frame at `+0x278`, releases it
  (`0x006CC550`) and returns 1.

`0x0067AB50(texture, data)` uploads one plane. It picks the texture's ring record by the counter
`0x01F7F5A0` modulo the ring size, waits 1 ms at a time while that record's in-use count `+0x38` is
above 0, hands the data to `0x0062CC10`, which queues the upload, and stores the record index at
`+0x0C`.

### Stopping

`0x001848E0(flag)` calls `0x001B83B0`. With the flag set (`0x0035B720` passes 1) it sets `+0xBAC` and,
unless the state is 0, 5 or 6, starts a half-second fade: state 6, `+0x10` = 0.5. With the flag
clear (`0x0035B8D0` passes 0) it sets `+0xB5D` unless `+0xBAC` is set, and moves to state 5 when no
fade time is left, so a running fade finishes first.

### The script side

`0x0035B740` polls the state through `0x00184860`: in state 1 it calls `0x001B7D30` (through `0x00184880`)
and returns 1; it returns 2 and 3 for those states and 0 otherwise. `0x0035B7D0` calls `0x001B82A0`
(through `0x001848C0`), which starts play only when `+0x08` is set. `0x0035B840` starts a movie and
`0x0035B8D0` stops it.

`setmoviescreensize(n)` (`0x058C`, `0x00347C40`) stores `n` at `0x02ADD933` through `0x0037B470`, or 3
for a negative `n`, and `getmoviescreensize` (`0x058D`, `0x00347F40`) returns it (`0x0037B370`). The
movie start `0x0035B840` resets it to 3 (`0x0037B470(−1)`), and so does `0x0037B390` from the startup
constants `0x0022A0B0`. The only other reader, the loaded-file play `0x003B1BA0`, discards the value,
so the setting changes nothing on screen.

### The time read-outs

- `0x00184810` returns, in state 3 only, `+0x18 x 29.97 x 0.001` truncated; otherwise -1.
- `0x001B77B0` (through `0x001847B0`) returns `+0x18 x 0.0333667` truncated (`0x008F8D7C`).
- `0x001B77E0` (through `0x001847F0`) returns `+0x20 x 0.0333667 - 30`, clamped at 0; for movie id 43
  (`IVT`) it subtracts 8 instead (`0x01CEBC80`).

## Modding notes

- Editing or deleting a `.mh` changes nothing; replace the `.webm` instead.
- The audio track follows the Voice language option and the volume follows the Music volume option,
  read when the movie starts.
- A movie also closes when `0x0067A410` returns 0 during play, not only after its duration.

## Related

- [Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md): the kind-28
  path, the `.webm` name and the shipped WebM files.
- [Media decoder libraries](../Third-Party-Libraries/media-decoder-libraries.md): the movie open
  `0x0067A480` and the VP8 and Vorbis decode.
- [Game application](../Engine-Core/game-application.md): where `0x001B8400` runs.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): the Voice language and Music volume options.
- [Screen fades](screen-fades.md): the fades around a movie.
