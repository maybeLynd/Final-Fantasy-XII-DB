---
title: "Music table: the file that names each area's music track, how the story changes it, and the boss-music flags"
kind: "format"
category: "Sound and music"
addresses: "0x00379D20, 0x003EAB60, 0x003EAB90, 0x003EAA70, 0x02B5E0D0, 0x00360C70, 0x022CBA50, 0x00361010"
---

## What the player sees

- Each area has its own music, and areas next to each other often share a track.
- Some areas change their music as the story moves on, or fall silent for a stretch of it.
- Boss music keeps playing while riding a chocobo or with a summon out; other tracks give way to the chocobo or
  summon music.

## Where it comes from

### The music control file

`musicctrl.bin` is kind 9 file `0x20`, `PS2Data\image\ff12\in\common\musicctrl.bin` in the `in` path table
(`0x01E12660`); a `ch` copy holds the same bytes. The boot loader `0x00379D20` reaches `0x003EAB60` with a jump
(`0x00379D32`), and `0x003EAB60` requests the whole file and keeps the pointer at `0x02B5E0D0`. The completion
`0x003EAB90` adds the file's own address to every non-zero page offset (`0x003EAB90`-`0x003EABD6`).

### The track flag file

`musicinfo.bin` is kind 9 file 6 (`PS2Data\image\ff12\in\common\musicinfo.bin`). `0x00360C70` requests it into heap 5
(`0x00360C70`), and its completion `0x00360B40` keeps the pointer at `0x022CBA50`. `0x00361010(track)` answers bit `0x1` of
the track's first byte, or 0 for a negative track or no file.

`0x00360C70` first sets up the four track slots and clears `0x022CBA50` ([Music](music.md)), then asks the size table
for the file (`0x0032E400(9, 6)`, `0x00360CA9`). A negative size requests nothing and leaves the pointer 0
(`0x00360CC6`); otherwise it allocates that size in heap 5 (`0x0036C1D0(5, 5)`, `0x0036A190`, `0x0036C140`) and requests
the file through `0x0032E620` with the completion `0x00360B40` (`0x00360CC8`-`0x00360D19`).

## Layouts

All multi-byte fields are little-endian. The two-byte fields of runs and rungs are read a byte at a time, byte
`+1` shifted above byte `+0` (`0x003EAAA5`-`0x003EAAB4`, `0x003EAAD6`-`0x003EAAE5`, `0x003EAB20`-`0x003EAB2A`), so they need
no alignment.

Offsets in each table below are from the start of its own structure: the header, a run, a rung or a
`musicinfo.bin` entry. A page offset is from the start of `musicctrl.bin`: `0x003EAB90` adds the file's address to
each one that is not 0 (`0x003EABB6`-`0x003EABC1`), and there are `(maxField + 127) / 128` of them
(`0x003EAB9A`-`0x003EABA7`). A page's first run is at its offset. A run's rungs follow its 4 bytes, 3 bytes each
(`0x003EAB07`, `0x003EAB39`), and the next run starts at the run plus `4 + 3 * rungs` (`0x003EAACB`-`0x003EAAD3`). Track
*t*'s entry in `musicinfo.bin` is at file offset `2 * t` (`0x00361023`).

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "MUS0" |
| `+0x04` | `u32` | maxField | 1311, the highest field id |
| `+0x08` | `u32[11]` | pageOffset | one page per 128 field ids; 0 for a page with no runs |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | fields | mask `0x7FF` the first field id, mask `0xF800` how many more follow |
| `+0x02` | `u8` | rungs | ladder steps after the run |
| `+0x03` | `u8` | track | the track, 0 for no track |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | above | a story counter value |
| `+0x02` | `u8` | track | the track once the counter is above it, 0 for no track |

`musicinfo.bin` is 256 entries of two bytes, one per track:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | flags | bit `0x1` boss music |
| `+0x01` | `u8` | b01 | read by no code: `0x00361010` is the only reader of the file's pointer |

### The lookup

`0x003EAA70(field)` gives the track for a field id:

1. A field above `maxField` gives -1 (no track).
2. The page is `field / 128`; a page offset of 0 gives -1.
3. It walks the page's runs while their first field is not above the id, skipping each run's rungs, and stops at the
   run that covers the id; no run gives -1.
4. It starts from the run's track and walks the rungs in order: while the story counter is above a rung's value, the
   rung's track replaces it.
5. Track 0 becomes -1.

The story counter is read through `FieldData_GetVariable0` (`0x003EAA78`).

## Shipped data

| | |
|---|---|
| runs | 291 in 11 pages; 122 cover more than one field, the largest 23 |
| field ids covered | 726 of 0-1,311; 19 of them have no zone, and two zones have no run, field 0 `tst_a01` and 869 `alc_z04` |
| runs with a ladder | 48, with 133 rungs, at most 6 on one run |
| ladders ending in `above 11000: no track` | 41 |
| distinct tracks | 69, every one a shipped `musicNNN.win.mab` |
| runs with no track | 41 |
| boss-music tracks in `musicinfo.bin` | 18: 10, 11, 33, 36, 51, 69, 70, 71, 95, 96, 97, 101, 102, 113, 205, 206, 207, 213 |

One shipped ladder does not rise: field 866, `alc_z01`, has `above 1950: no track; above 1658: 75; above 1973: 22`, so its
1,658 rung acts only once the counter is past 1,950.

[`music-table.tsv`](music-table.tsv) lists every run. One example, `bul_b02` (field 742), plays track 75, then no
track above story counter 1,976, 39 above 1,982, no track above 2,200, 31 above 2,250, 59 above 2,350 and no track
above 11,000.

The `track_titles` and `zone_names` columns name each run's tracks and maps: the example run's tracks are 75 (52_FinalFantasyXII-SeekingPower), 39 (62_FinalFantasyXII-AbandoningPower), 31 (04_FinalFantasyXII-AuditoryHallucination), 59 (65_FinalFantasyXII-TheWhiteRoom).

### Columns of music-table.tsv

| Column | Meaning |
|---|---|
| `first_field`, `last_field` | the field ids the run covers |
| `zones` | one zone name per field id, in order, from the `us` zone path table at `0x01EE23A0`; `-` for an id with no zone |
| `track` | the run's track, or `no track` |
| `ladder` | the rungs as `above <counter>: <track>`, in order |
| `kept_in_modes` | the run's boss-music tracks, which chocobo and summon music do not replace |
| `offset` | the run's file offset in `musicctrl.bin` |
| `page` | the page whose offset leads to the run |
| `track_titles` | each track the run and its ladder name, with the title in section 0 of its music file ([Sound banks](sound-banks.md), [`sound-music-bank-files.tsv`](sound-music-bank-files.tsv)); `-` for a run with no track |
| `zone_names` | the map and region of each zone in `zones`, in order ([Zone asset list](../World-Areas-And-Travel/zone-asset-list.md)); the region alone where the zone has no map name; `-` for an id with no zone |

### Each area's track by story stage and mode

[`music-resolved.tsv`](music-resolved.tsv) gives every field id's track for each stretch of the story counter, as
`0x003EAA70` resolves the table: 869 rows for the 726 field ids. The counter is read signed (`0x003EAB10`), so `end` is
32,767 and a negative counter plays what 0 plays. Field 742 `bul_b02` plays 75 to 1,976, no track to 1,982, 39 to
2,200, no track to 2,250, 31 to 2,350, 59 to 11,000 and no track after; field 866 `alc_z01` plays no track to 1,950,
75 to 1,973, 22 to 11,000 and no track after.

The music that plays is decided at `0x00261F90`: the saved override replaces the table's track while payload `+0x1063`
bit `0x40` is set (`0x0026201B`-`0x00262029`). A boss-music track stays (`0x00262041`). Any other track, and no track
(`0x0026203D`), gives way to the summon track 91 (`0x5B`, `0x00262053`) in summon mode, or else to the chocobo track
90 (`0x5A`, `0x00262063`) in chocobo mode. 12 rows keep a boss track: fields 357, 552, 777, 933-936, 1150, 1246, 1291,
1302 and 1311.

### Columns of music-resolved.tsv

| Column | Meaning |
|---|---|
| `field` | the field id |
| `zone` | the field id's zone, as in [`music-table.tsv`](music-table.tsv); `-` for an id with no zone |
| `counter_from`, `counter_to` | the first and last story counter value of the stretch; `end` is 32,767 |
| `track` | the track the table gives, or `no track` |
| `on_chocobo` | the track in chocobo mode and the instruction that picks it |
| `with_summon` | the track in summon mode and the instruction that picks it |

### Zone-script music calls

[`music-script-overrides.tsv`](music-script-overrides.tsv) lists the 21,825 music verb calls in the `us` zone
scripts, in 327 of the 769 zones. It leaves out the helper actors many zones share, which are on
[Shared zone-script actors](../Story-Events-And-Hunts/shared-zone-script-actors.md). 21,503 calls sit under
a story counter, flag or other test, 2 only inside an endless loop and 320 under no test; 18,700 are the 187 calls of
each of the 100 Trial Mode zones. Every track number of 0 or more that a call passes is a shipped `musicNNN.win.mab`.

For `musicstop`, `musicclear`, `musicfadeout`, `musicfadeout_231` and `musictrans`, a track of -1 is the current
track (`0x002DEC00`). `musicread` and `musicplay` with -1 load nothing (`0x00361639`), and `musicreadsync` with -1 does
not wait (`0x00341FA3`). `setnowmapmusicno` is called 1,363 times; its 229 calls with -1 clear the saved override
(`0x00345E70` -> `0x0026A720`).

| Verb | Call id | Calls | What it does |
|---|---|---|---|
| `musicread` | `0x229` | 4,097 | loads a track into a music slot (`0x00341710` -> `0x00361630`) |
| `musicreadsync` | `0x22A` | 2,296 | waits until the track's slot is loaded (`0x00341F90`) |
| `musicplay` | `0x22B` | 3,081 | loads and starts a track (`0x00342770`, `0x00342F80`) |
| `musicstop` | `0x22C` | 2,189 | stops a track and keeps its resume point (`0x00345010` -> `0x002DEDE0`) |
| `musicclear` | `0x22D` | 2,083 | frees a track's slot (`0x00345600` -> `0x00360E50`) |
| `musiccrossplay` | `0x22E` | 42 | changes the music to a track (`0x00347A50`) |
| `musiccrossplay_22f` | `0x22F` | 99 | changes the music to a track with a length and release (`0x00346C00`) |
| `musicfadeout` | `0x230` | 2,063 | fades a track out (`0x00346460`) |
| `musicfadeout_231` | `0x231` | 348 | fades a track out and ends it (`0x00345B60` -> `0x002DEE50`, `0x00361170`) |
| `musicclearall` | `0x240` | 107 | frees every music slot (`0x0034BB00` -> `0x00360D70`) |
| `musictrans` | `0x2C7` | 338 | sets a track's volume over a length (`0x00340260` -> `0x002DEE50`) |
| `getnowmusicno` | `0x363` | 413 | reads the current track (`0x003549D0`) |
| `musicreplay` | `0x364` | 1 | plays a track again (`0x00344410` -> `0x00342770`) |
| `musicplaysync` | `0x3A2` | 114 | waits while a track plays (`0x003508E0`) |
| `getnowmapmusicno` | `0x470` | 647 | reads the area's track (`0x00345760` -> `0x0026DE00`) |
| `setnowmapmusicno` | `0x471` | 1,363 | saves or clears the area's override (`0x00345E70` -> `0x0026A720`) |
| `getnowmapmusicno_47a` | `0x47A` | 331 | reads the area's track, mode tracks left out for a non-zero argument (`0x00345400` -> `0x0026DE00`) |
| `isbossmusic` | `0x47B` | 86 | reads a track's boss-music bit (`0x00349E10` -> `0x00361010`) |
| `musicphraseplay` | `0x50E` | 4 | plays a track from a section (`0x003437A0`) |
| `musicfadeoutsync` | `0x536` | 2,123 | waits for the music fades to end (`0x003466F0`) |

### Columns of music-script-overrides.tsv

| Column | Meaning |
|---|---|
| `zone` | the zone's place and field id |
| `script` | the zone script |
| `function` | the actor and function of the call; actors that share their code are named by the first of them |
| `verb` | the music verb |
| `track` | the track the call passes: a number, -1, the expression the script passes, or `-` for a verb without one |
| `condition` | the tests around the call, outermost first, joined with `and`; `not (...)` for an else branch; `always` for a call under no test |
| `effect` | what the call does, with the verb's instruction addresses |

### Pages

| Page | Field ids | Offset | Runs |
|---|---|---|---|
| 0 | 0-127 | `0x34` | 12 |
| 1 | 128-255 | `0x6A` | 28 |
| 2 | 256-383 | `0x104` | 39 |
| 3 | 384-511 | `0x1EB` | 29 |
| 4 | 512-639 | `0x274` | 30 |
| 5 | 640-767 | `0x316` | 33 |
| 6 | 768-895 | `0x400` | 35 |
| 7 | 896-1,023 | `0x4CB` | 18 |
| 8 | 1,024-1,151 | `0x531` | 29 |
| 9 | 1,152-1,279 | `0x5B7` | 27 |
| 10 | 1,280-1,407 | `0x623` | 11 |

Each page's runs end where the next page's begin, and the last run ends at `0x64F`, the end of the 1,615-byte file.
Four runs start in one page and end in the next: 253-256, 380-387, 767-768 and 1,009-1,031. Each is stored once,
as the first run of the later page.

### Track entries

[`music-track-flags.tsv`](music-track-flags.tsv) lists all 256 entries of `musicinfo.bin`; 122 are not zero.

| | |
|---|---|
| flags `0x06` | 86 tracks |
| flags `0x07`, boss music | 12 |
| flags `0x02` | 10 |
| flags `0x04` | 6 |
| flags `0x03`, boss music | 4 |
| flags `0x01`, boss music | 2: tracks 10 and 11 |
| flags `0x80` | 2: tracks 0 and 12 |
| flags `0x00` | 134 |
| byte `+1` | the entry's own track in 96; another track in 8 (101: 36, 102: 61, 104: 73, 106: 95, 111: 44, 112: 44, 114: 72, 116: 83); 0 in 152 |

Each of the 116 shipped `musicNNN.win.mab` has an entry that is not zero. Six entries that are not zero name a
track with no shipped bank: 0, 10, 11, 12, 93 and 130.

### Columns of music-track-flags.tsv

| Column | Meaning |
|---|---|
| `track` | the track, the entry's index |
| `offset` | the entry's file offset, 2 x track |
| `flags` | byte `+0` |
| `boss` | `yes` when bit `0x1` of the flags is set, the bit `0x00361010` answers |
| `b01`, `b01_is` | byte `+1`, and whether it is 0, the entry's own track or another track |
| `runs`, `rungs` | the runs and rungs of `musicctrl.bin` that name the track; for track 0, those with no track |
| `bank_file` | the track's shipped `music/magi_data/win/musicNNN.win.mab`, or `-` when no file ships |

## Loader behaviour

1. Neither loader checks the magic or the sizes.
2. A page has no end marker: a lookup that runs past a page's last run walks on into the next page's runs. For the
   four runs that cross a page boundary (above), that is how the earlier page's ids reach their run. Every other
   page's next first run starts above every id of the page, and the walk stops there. On the last page the last run
   is field 1,311, and the header refuses anything above it.
3. A track number is the `NNN` of `music/magi_data/win/musicNNN.win.mab` ([Sound banks](sound-banks.md)).
4. `0x00361010(t)`, the boss-music test, returns 0 for a negative `t` and reads entry `t` with no upper bound
   (`0x00361010`-`0x00361027`), so a `t` of 256 or more reads past the file's 256 entries.
5. Four callers of `0x00361010` pass the track of the run lookup `0x003EAA70` (`0x0025DBCE`, `0x00262041`, `0x0026DE59`,
   `0x0026DF03`), a byte or -1. The fifth is `isbossmusic` (`0x47B`, `0x00349E10`), which passes the script's value
   unchecked; all 591 of its calls in the `us` scripts pass `getnowmapmusicno_47a(1)`.

## Modding notes

- To change an area's music, edit its run's track byte; to change it at a story point, add or edit a rung, keeping
  the run's rung count in step.
- Rungs are tested in file order and stop at the first value the counter is not above, so keep them rising.
- Setting a track's boss-music bit keeps it playing through chocobo and summon music.
- The page offsets are rebased in place with a 32-bit add (`0x003EABBE`) and read back sign-extended (`0x003EAA9C`), so
  the file must stay at an address below 2 GB.

## Related

- [Music](music.md) - when the table is read and how the track starts.
- [Story counter values](../Story-Events-And-Hunts/story-counter-values.md) - the values the ladders compare.
- [Zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md) - the field id.
