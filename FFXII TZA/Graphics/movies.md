[Home](../../README.md) / [Graphics](README.md) / Movies

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Movies: the .mh seek index and the movie player's states | format | Graphics | Screen effects and movies | The full-motion movie files and the object that plays them: the PS2-era .mh seek index shipped beside the movie paths and never read, how a movie id maps to its path pair, and the movie player singleton's start, update, fade-out and time read-outs that the script layer drives. | 0x01F81218, 0x001B7F20, 0x001B82F0, 0x001B7F30, 0x001B8400, 0x001B83B0, 0x001B82A0, 0x001B7D30, 0x001B7690, 0x001B77B0, 0x001B77E0, 0x00184810, 0x001848A0, 0x001848E0, 0x0035B840, 0x0035B8D0, 0x0035B740, 0x0035B7D0, 0x002DF980, 0x01ECB4D0 |

## What the player sees

The story's pre-rendered cutscenes play as WebM videos with the voice track in the language set in
the options and the sound at the music volume. A movie asked to stop either ends at once or fades
its sound out over half a second first. Beside the movie paths the game still carries the PS2
seek indexes (`.mh`) of the old movie streams; nothing opens them. What each of the 40 shipped movies
shows, with its length and its first subtitle line, is in [`movies-contents.tsv`](movies-contents.tsv).
The same table says, for the five ids whose `.webm` does not ship, which script function opens each.

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
| `+0x000` | `i32` |  | movie id; -1 when idle |
| `+0x004` | `i32` |  | state (0 to 6, below) |
| `+0x008` | `u8` |  | the result of `0x0067A410`, refreshed by every update outside states 0 and 5 (`0x001B84E6`) |
| `+0x009` | `u8` |  | a frame has been fetched (`0x0067ABF0`) |
| `+0x00C` | `f32` |  | sound volume: the Music volume option / 100 |
| `+0x010` | `f32` |  | fade-out time left, seconds |
| `+0x018` | `u64` |  | position, from `0x0067A2F0` |
| `+0x020` | `u64` |  | duration, from `0x0067A340` |
| `+0x02D` | `u8` |  | the fade-out also lowers the sound |
| `+0x678` | `...` |  | the PVideoPlaybackWin32 playback object |
| `+0xB5D` | `u8` |  | set by a stop request without fade |
| `+0xBAC` | `u8` |  | a fading stop was requested |
| `+0xBB0` | `u32` |  | audio language flag (`+0x678` + `0x538`): 1 when the Voice language option bit is set |

## Shipped data

<details>
<summary>Show the shipped data</summary>

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
| movies by id | one row per movie id in [`movies-by-id.tsv`](movies-by-id.tsv), 49 rows: the kind-28 `.md` path, the `.webm` name the player opens and whether it ships (with its size and SHA-256), the `.mh` path and file, and every script step that opens the id |
| opened by a script | 43 of the 45 ids with a path have a `moviestandby` step; 39 of those 43 open a shipped `.webm` |
| title movies | `ttl_a01` and `ttl_a01_e3` choose the logo (44 or 45) and the opening (41 or 47) by `getscreenaspect` (`0x58E`, `0x0050D1C0`), whose `0x0053DD10` always answers 1, so they open 45 and 47; `ttl_c01` opens 41. None of 41, 44, 45 and 47 has a `.webm`, so each of these opens fails and resets the player |
| named by no step | ids 35 (`GRV`) and 37 (`DLB`): no `moviestandby` step of the zone and event scripts names them; `grv.webm` ships and `dlb.webm` does not |
| where each movie plays | one row per movie id and opening step in [`movies-scenes.tsv`](movies-scenes.tsv), 52 rows for the 43 ids a step opens: the step, the scene's event id when the step is in a scene script, the zone script it plays in with its field number, map name and region ([Zone asset list](../World-Areas-And-Travel/zone-asset-list.md)), the story counter value the scene sets, and when in the story it plays (`story_point`): the story counter values it plays between and the step or spot that leads to it, read with the cases of its switch that come first, and the opening of its map ([Zone openings](../World-Areas-And-Travel/zone-openings.tsv)) where no wall stands on the way in; the title screen rows are not tied to the story |
| places | 46 rows fall in 32 zones; 28 of them are steps of a scene script, placed at the zone script that loads the scene, and in 16 of those the scene sets the story counter. The other 6 rows are steps of `ttl_a01_e3`, the `cn` and `kr` title script that `us` lacks |
| scenes placed by their page | `msg_z0001` (id 25, `EPL`) plays in `bhm_d01`, Cannon Superstructure, whose `ボス監督.main` loads it ([Ending message scenes](../Story-Events-And-Hunts/ending-message-scenes.md)); `men_z0005` (id 42, `STF`) plays in field 13, `ttl_b01` ([Tutorials scenes](../Story-Events-And-Hunts/tutorials-scenes.md)) |
| subtitle tracks | the 40 shipped `.webm` files declare a VP8 video track each, 39 of them Vorbis sound, and no file a subtitle track |
| subtitles | the script that opens a movie prints its subtitles: while the movie plays, its functions wait for movie frames (`getmovieframe`, `0x0033F250`, at 29.97 frames a second) and print one line each with `amest`; where a `getff12lang` switch (the voice language, 0 for Japanese voices) picks a second set of functions timed to the Japanese voices, the table follows the English-voice set. 14 movies print 297 lines: `OPN` 31, `ALX` 4, `DRC` 2, `END` 96, `STR_STA` 18, `DIS` 6, `LRF` 16, `EST` 1, `ESC` 4, `EPL` 30, `MEM` 8, `VAD` 17, `VNP` 57 and `WAR` 7. The steps that open the other 29 movies start no function that prints a line against movie frames |
| every subtitle line | one row per line in [`movies-subtitle-lines.tsv`](movies-subtitle-lines.tsv), 297 rows: the movie, the line's order, the frame and second it follows (lines a plain wait apart share the frame), the line and the function that prints it |

### Columns of the movie tables

Every value below matches the shipped `.mh` and `.webm` files; the `.webm` files are in
`gamedata/d3d11/artdata/video/`.

| Column | Holds |
|---|---|
| `sha256_16` | in movies-mh-rows.tsv, the first 16 hex digits of the `.mh` file's SHA-256 |
| `stream_bytes`, `frame_count` | the header's `streamBytes` `+0x0C` and `frameCount` `+0x10` |
| `flags_1`, `flags_2` | how many entries have flags 1 and flags 2; with `flags_0` they add up to `entries` |
| `last_entry_frame` | the frame number of the last entry |
| `md_path` | in movies-by-id.tsv, the kind-28 entry `2m` for movie id m, the PS2 `.md` path; `-` for the empty ids 38, 39, 40 and 46 |
| `webm_ships` | `yes` when `webm` is in the video folder (40 ids), `no` when it is not (5), `-` for the four empty ids |
| `webm_bytes`, `webm_sha256` | the shipped `.webm`'s size in bytes and its full SHA-256 in capitals; `-` when it does not ship |
| `mh_path` | the kind-28 entry `2m + 1`, the `.mh` path; `-` for the empty ids |
| `mh_file` | the shipped `.mh` file at that path, in lower case; `-` for the empty ids and for `us\DLB.mh` (id 37) and `in\ANX.mh` (id 48), which have no file |
| `scene_event_id` | in movies-scenes.tsv, the event id of the scene script when the opening step is in one (28 rows); `-` for a step of a zone script (24 rows) |
| `story_counter_set` | the story counter values the scene sets, each with its name, separated by `/` (16 rows); `-` on the other 36 rows |
| `after_frame` | in movies-subtitle-lines.tsv, the movie frame the printing function waits for before it prints the line (`getmovieframe`) |
| `after_seconds` | that frame divided by 29.97, to two decimal places: `after_seconds = after_frame / 29.97`, rounded to 0.01 |
| `printed_by` | the zone script, the function that prints the line, and the step in that function |
| what each movie shows | one row per movie id with a path in [`movies-contents.tsv`](movies-contents.tsv), 45 rows: the `movie_id`, the `movie` code, the `webm` file, its length in `seconds` (the duration the file states), what it `shows`, written from twelve frames spread evenly over the movie with the seconds of the frames each phrase rests on, and the `first_line` of its subtitles from [`movies-subtitle-lines.tsv`](movies-subtitle-lines.tsv) (`-` for the 26 movies whose opening script prints no line). The five ids whose `.webm` does not ship (37, 41, 44, 45 and 47) have `seconds` and `first_line` `-`, and their `shows` says what opens them |

### Subtitle timing by voice language

Subtitle timing depends on the voice language as well as the movie, so a script may hold one function per language.
`getff12lang` returns 1 for English voices and 0 for Japanese¹. The text locale is separate:
`unkCall_59c` returns the locale id, with `KR`, `CH`, `IN` and `CN` (7, 8, 10 and 11) read as 0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0034B650`, `0x002DEBB0` |
| ² | `0x0034BA00` |

</details>

`Database/Tools/catalogues/voice_recordings.py` writes two tables from the script listings:

- [`movies-subtitle-steps.tsv`](movies-subtitle-steps.tsv): one row per statement, 6,216, of the 165 functions in 30
  scripts that test `getmovieframe` or are started from one that does.
- [`movies-subtitle-dialogue.tsv`](movies-subtitle-dialogue.tsv): one row per line those functions print, 274, in all
  nine locales.

In all 30 scripts the instruction streams of these functions are the same in every language tree that holds them,
with each pushed constant compared by value.

| `kind` | Rows | Statement |
|---|---|---|
| `frame_check` | 545 | a test of `getmovieframe`; in 184 the frame is a variable, and `frame_values` gives what the function stores in it |
| `poll` | 554 | the `wait` inside such a loop |
| `wait` | 593 | any other `wait` of a constant |
| `print` | 359 | a message call; `line_index` is its line |
| `other` | 4,165 | every other statement, verbatim |

| `voice_branch` | Rows | Meaning |
|---|---|---|
| `english` | 1,499 | the blocks around the row, or around the request of its function, select `getff12lang` not 0 |
| `japanese` | 1,481 | they select `getff12lang` 0 |
| `both` | 9 | the function is requested under both |
| `tests_disagree` | 186 | the blocks test the voice language twice with different answers |
| `-` | 3,041 | no block tests it |

Each test reads the option afresh, so a `tests_disagree` row runs only if the option changes between the two tests.

`after_frame` and `waits_since_check` state the timing of a row. A row follows the last frame check by the waits since
it. They are read in listing order, and only a row in the same blocks as that check has a count; the others have `-`.

| column | what it holds |
|---|---|
| steps, text: `script` | the script's path under `plan_master/us`; `ttl_a01_e3` is only in the `cn` and `kr` folders and is read from `cn` |
| steps: `movie_ids` | the `moviestandby` constants of the script |
| steps: `actor`, `function`, `step` | the function and the statement's place in it |
| steps: `started_from` | `-` for a function that tests the frame, else the function that first starts it |
| steps: `statement`, `conditions` | the statement, and the blocks around it, outermost first |
| steps: `frame_test`, `frame`, `frame_values` | the comparison, the frame in decimal or the variable's name, and the values stored in that variable with the blocks around each store |
| steps: `wait` | the frames of a `wait` |
| steps: `message`, `line_index` | the message id in hexadecimal, and the line of section 2 it opens |
| steps: `requested_by` | each function that requests this one, with the blocks around the request |
| steps: `text_tests` | the blocks around the row that test `unkCall_59c`, outermost first |
| text: `line_index` | the line of section 2 |
| text: `us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch` | the line in each language folder, in the text codes of the dialogue tables |
| text: `printed_by`, `voice_branch` | the functions that print it, and the values of `voice_branch` on those rows |

</details>

## Loader behaviour

### The .mh is never read

The only fetch of an odd kind-28 entry is in the script-side start `0x0035B840`
(`0x0035B8AE`, `0x002DF980(0x1C, 2m + 1)`); the next instructions load the movie id into `ecx` and call
`0x001848A0`, which does not use the result. The executable contains no `.mhe` text, so no code checks
the magic.

### Starting a movie

`0x001848A0(m)` calls `0x001B82F0` on the singleton, which:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | tears down any open playback (`0x0067A9B0` on `+0x678`); |   |
| 2 | stores the id, clears the position and `+0x09`, and sets state 1; |   |
| 3 | sets `+0xBB0` from the Voice language option, which makes the decoder pick the non-English audio track; | `0x002DEBB0` |
| 4 | stores the Music volume (`0x002DDC70`, at most 100) divided by 100 at `+0x0C`; |   |
| 5 | calls `0x0067A970(+0x678, 1)` and `0x0017D940(1)`, which raises busy counter 1 of the prefetch manager that the close lowers with `0x0017D960(1)`; | `0x001B8341`-`0x001B835C`<br>`0x001B8366`, `0x001D9F81` |
| 6 | queues `0x001B7F30` as a job on the `AsyncJobManager`, through a tail jump. | `0x00199F10`, `0x0019A000`<br>`0x001B83A3` |

The job `0x001B7F30` starts the reading thread¹, fetches entry `2m`, and opens the WebM.
`0x0067A350` always returns 1² and drops the result of the thread start `0x005CD1E0`³, so
the arm that sets state 0 and returns without a reset⁴ is never taken. A
null entry resets the player⁵: id -1, position and duration 0, state 0. A failed open
sets state 0 and resets⁶, and so does a path with no backslash⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0067A350` |
| ² | `0x0067A3FF` |
| ³ | `0x0067A3F5` |
| ⁴ | `0x001B7F6A`, `0x001B80B5` |
| ⁵ | `0x001B7690` |
| ⁶ | `0x001B8030`-`0x001B803A` |
| ⁷ | `0x001B7FCE` |

</details>

The null-entry reset is an inline copy of `0x001B7690`¹: besides the id, position,
duration and state it clears `+0x09`, tears the playback down (`0x0067A9B0` on `+0x678`) and calls
`0x0017D960(1)`, `0x002E1CA0(1, 0x15)` and `0x00229AE0(1)`, as `0x001B7690` itself does².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001B8070`-`0x001B80B3` |
| ² | `0x001B76A7`-`0x001B76D6` |

</details>

### The picture's geometry

The init burst builds the player's drawing side with `0x001B7850`. It loads
`/GameData/D3D11/ArtData/shaders/video.fx.phyre`¹ into `+0xD0`, sizes three plane
textures², Y at `+0x108` at 1920 × 1080 and U and V at `+0x290` and `+0x418` at 960 ×
540, each with four buffers³, and binds them to the effect's `YChannel`, `UChannel` and
`VChannel`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0019CB20` |
| ² | `0x0060DD70` |
| ³ | `0x00628100` |
| ⁴ | `0x0018D240`, `0x001B81B0` |

</details>

It puts the effect into a one-entry `PMaterialSet` of the
player's cluster `+0x30`¹, builds the geometry, keeps the mesh instance at `+0x100`
with the material set at its `+0x20`, and stores 16/9 (1.7777778) at `+0x668`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001B80C0` |

</details>

`0x001B72B0(player, cluster)` gives the cluster one `PMesh`¹ of one segment (`0x0C0`
bytes, `0x001B7210`) unless it already has exactly one, sets the segment's `+0x18` to 2, and fills
two vertex streams of three entries:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02D3A640` |

</details>

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
[q + 0xA0]`) to the free function at `q + 0x58`, empties the list and sets `side = (side == 0)`¹.
Then, by state:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001B8411`-`0x001B8429` |

</details>

| State | Meaning | What the update does |
|---|---|---|
| 0 | idle | nothing more |
| 1 | opening | once `+0x08` is set and while `+0x09` is 0, fetches a frame (`0x0067ABF0`) into `+0x09`; when one arrives it reads the position and duration and calls `0x0067A440` (`0x001B8573`-`0x001B85C7`) |
| 2 | ready | entered through `0x001B7D30` when `+0x08` and `+0x09` are both set |
| 3 | playing | entered through `0x001B82A0` when `+0x08` is set; keeps fetching frames; moves to state 4 when the position reaches the duration minus `0xE9` |
| 4 | ending | keeps fetching frames |
| 5 | closing | resets the player, tears down playback and calls `0x0017D960(1)`, `0x002E1CA0(1, 0x15)`, `0x00229AE0(1)` |
| 6 | fading out | subtracts `dt` from `+0x10`; while `+0x2D` is set, sets the sound volume to `+0x0C` x `+0x10` x 2 (`0x0067A990`); state 5 when `+0x10` drops below 0, with `+0x10` set to 0 first, so that update sets the volume to 0 when `+0x2D` is set and closes the player at once through the state-5 step (`0x001B8445`-`0x001B8489`) |

In states 3 and 4, an update in which `0x0067A410` returns 0 sends the player to state 5 and resets it.

`0x001B82A0` enters state 3 only when `+0x08` is set; it then calls `0x00229AE0(0)`, sets state 3, calls
`0x0067A440` and `0x0067A970(+0x678, 0)` on the playback, and ends with a tail jump to `0x002E1C20(1, 0x15)`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001B82A6`-`0x001B82E4` |

</details>

### Fetching a frame

The player's constructor `0x001B6D90` builds the playback object at `+0x678` with `0x006791B0`, which
sets up its three queues (`+0x000`, `+0xA8`, `+0x150`) and three locks and zeroes its counters and
flags, among them the state `+0x268` and the audio flag `+0x538`.

- Each queue is a `CDataFrameQueue` built by `0x006CC350`: its vtable, two locks¹, two 0x20-byte frame
  lists and `0x00584730` as its free function. `0x006CC960` builds the `VbfMkvReader`².
- `0x006CC730(queue, keep)` lets go of the frame a queue holds: with `keep` it pushes the frame onto the list at `+0x60`
  (or `+0x80` when `+0xA0` is 0), otherwise it frees it through `+0x58`; then it closes both lock handles
 ³.
- `0x0067A970(playback, pause)` resets the playback's run event `+0x4D0` to pause it and sets it to run again
 ⁴; `0x001B82A0` runs it with 0⁵ and `0x001B82F0` with 1⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00874D60` |
| ² | `0x0067922B` |
| ³ | `0x005CD700` |
| ⁴ | `0x005CD500`, `0x005CD5E0` |
| ⁵ | `0x001B82D2` |
| ⁶ | `0x001B8341`, `0x001B835C` |

</details>

`0x0067ABF0(playback, y, u, v)`, from the update in states 1, 3 and 4, takes one decoded frame into
the player's three plane textures `+0x108`, `+0x290` and `+0x418`:

- it counts its calls at `+0x530`; while `0x001EDE70()` is set it acts only on every second call;
- it needs the state `+0x268` at 1, and while `+0x4F4` is set it waits until the frame queue
  `+0xA8` holds at least `+0x2EC` frames, then clears `+0x4F4`;
- it takes the oldest frame¹, uploads its three planes, the first at frame `+0x10` and
  the others `+0x524` and `+0x528` bytes further on, counts the frame at `+0x278`, releases it
 ² and returns 1.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006CC4F0` |
| ² | `0x006CC550` |

</details>

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
(through `0x001848C0`, its tail jump `0x0035B834`), which starts play only when `+0x08` is set. `0x0035B840` starts a
movie and `0x0035B8D0` stops it.

Each also switches field state ([event scenes](../Scripts-And-Script-Commands/event-scenes.md) lists every call).
`0x0035B7D0` first switches the field systems off (`0x00358750` and its siblings, `0x002E1CD0(0, 0)`, `0x002E1C40(0, 4)`,
`0x00368AA0(0, 0)`, `0x0035B7DB`-`0x0035B82B`).

`0x0035B840` sets action row 0 bits `0x1` and `0x100000`, the arena mode 1
and busy bit `0x10000` before it opens the movie¹. `0x0035B8D0` stops through `0x001848E0(0)`², clears busy bit `0x10000`, switches the field systems back on³ and sets the
arena mode back to 0 through its tail jump to `0x0037B450(0)`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035B861`-`0x0035B881` |
| ² | `0x0035B8D6` |
| ³ | `0x0035B905`-`0x0035B980` |
| ⁴ | `0x0035B98B` |

</details>

A script chooses its movie with `moviestandby` (`0x368`): its result step `0x00356460` passes the
id to `0x0035B840`, the only caller of `0x001848A0`. `movieplay` (`0x36A`, `0x00356D20`) pops an argument
that it does not use and runs `0x0035B7D0`, so it plays whichever movie `moviestandby` opened.

`setmoviescreensize(n)` (`0x058C`, `0x00347C40`) stores `n` at `0x02ADD933` through `0x0037B470`, or 3
for a negative `n`, and `getmoviescreensize` (`0x058D`, `0x00347F40`) returns it¹. The
movie start `0x0035B840` resets it to 3 (`0x0037B470(−1)`), and so does `0x0037B390` from the startup
constants `0x0022A0B0`. The only other reader, the loaded-file play `0x003B1BA0`, discards the value,
so the setting changes nothing on screen.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0037B370` |

</details>

### The time read-outs

- `0x00184810` returns, in state 3 only, `+0x18 x 29.97 x 0.001` truncated; otherwise -1.
- `0x001B77B0` (through `0x001847B0`) returns `+0x18 x 0.0333667` truncated¹.
- `0x001B77E0` (through `0x001847F0`) returns `+0x20 x 0.0333667 - 30`, clamped at 0; for movie id 43
  (`IVT`) it subtracts 8 instead².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008F8D7C` |
| ² | `0x01CEBC80` |

</details>

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**Movement and pathfinding** (explained on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002E1CD0`](../Controls-And-Input/action-availability.md) (on action availability) | is called by | [`0x0026C3E0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze) |

</details>
