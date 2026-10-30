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
(`0x00360C70`), and its completion `0x00360B40` keeps the pointer at `0x022CBA50`. `0x00361010(track)` answers bit `0x1` of the
track's first byte, or 0 for a negative track or no file.

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
| `+0x00` | `u16` | fields | bits 0-10 the first field id, bits 11-15 how many more follow |
| `+0x02` | `u8` | rungs | ladder steps after the run |
| `+0x03` | `u8` | track | the track, 0 for none |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | above | a story counter value |
| `+0x02` | `u8` | track | the track once the counter is above it, 0 for none |

`musicinfo.bin` is 256 entries of two bytes, one per track:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | flags | bit `0x1` boss music |
| `+0x01` | `u8` | b01 | read by no code: `0x00361010` is the only reader of the file's pointer |

### The lookup

`0x003EAA70(field)` gives the track for a field id:

1. A field above `maxField` gives -1 (none).
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
| ladders ending in `above 11000: none` | 41 |
| distinct tracks | 69, every one a shipped `musicNNN.win.mab` |
| runs whose track is none | 41 |
| boss-music tracks in `musicinfo.bin` | 18: 10, 11, 33, 36, 51, 69, 70, 71, 95, 96, 97, 101, 102, 113, 205, 206, 207, 213 |

One shipped ladder does not rise: field 866, `alc_z01`, has `above 1950: none; above 1658: 75; above 1973: 22`, so its
1,658 rung acts only once the counter is past 1,950.

[`music-table.tsv`](music-table.tsv) lists every run. One example, `bul_b02` (field 742), plays track 75, then none above story counter
1,976, 39 above 1,982, none above 2,200, 31 above 2,250, 59 above 2,350 and none above 11,000.

### Columns of music-table.tsv

| Column | Meaning |
|---|---|
| `first_field`, `last_field` | the field ids the run covers |
| `zones` | one zone name per field id, in order, from the `us` zone path table at `0x01EE23A0`; `-` for an id with no zone |
| `track` | the run's track, or `none` |
| `ladder` | the rungs as `above <counter>: <track>`, in order |
| `kept_in_modes` | the run's boss-music tracks, which chocobo and summon music do not replace |
| `offset` | the run's file offset in `musicctrl.bin` |
| `page` | the page whose offset leads to the run |

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
| `runs`, `rungs` | the runs and rungs of `musicctrl.bin` that name the track; for track 0, those whose track is none |
| `bank_file` | the track's shipped `music/magi_data/win/musicNNN.win.mab`, or `-` when none ships |

## Loader behaviour

1. Neither loader checks the magic or the sizes.
2. A page has no end marker: a lookup that runs past a page's last run walks on into the next page's runs. For the
   four runs that cross a page boundary (above), that is how the earlier page's ids reach their run. Every other
   page's next first run starts above every id of the page, and the walk stops there. On the last page the last run
   is field 1,311, and the header refuses anything above it.
3. A track number is the `NNN` of `music/magi_data/win/musicNNN.win.mab` ([Sound banks](sound-banks.md)).

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
