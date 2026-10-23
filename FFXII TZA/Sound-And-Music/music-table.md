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
(`0x00360C70`), and its completion `0x00360B40` keeps the pointer at `0x022CBA50`. `0x00361010(track)` answers bit 0 of the
track's first byte, or 0 for a negative track or no file.

## Layouts

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
| `+0x00` | `u8` | flags | bit 0 boss music |
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

## Loader behaviour

1. Neither loader checks the magic or the sizes.
2. A page has no end marker: a lookup that runs past a page's last run reads the next page's first run, whose first
   field is above every id of the page, and stops there. On the last page the last run is field 1,311, and the header
   refuses anything above it.
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
