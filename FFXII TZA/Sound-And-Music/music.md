---
title: "Music: which track plays in an area, the chocobo and summon tracks, the crossfade when the area changes, and the saved track override"
kind: "system"
category: "Sound and music"
addresses: "0x00261F90, 0x003EAA70, 0x00361010, 0x0030D9A0, 0x003614E0, 0x002DEE50, 0x0026A720, 0x0026DE20"
---

## What the player sees

- Entering an area crossfades to its music, or keeps the music when the track is the same.
- Riding a chocobo or calling a summon plays their own track, except over boss music.
- Some story scenes pin a track that stays through area changes until a later scene releases it, and the pin is kept
  in the save.

## How it works

### When the area's music is chosen

The zone setup `0x0025D9E0` calls `0x00261F90` (`0x0025DB8E`) for the zone being entered:

1. It returns when the zone's `+0x28` is not 0 or its done bit, `+0x10` bit 6, is set (`0x00261F96`-`0x00261FA7`).
2. It chooses music only when `+0x17` bit 7 is set (`0x00262000`).
3. It always sets the done bit on the way out (`0x002620D5`), so the music is chosen once per zone.

### Which track

1. The field id is payload `+0x1044` (`0x0026200F`, `0x003148F0`).
2. When payload `+0x1063` bit 6 is set, the track is the saved override at payload `+0x1534`; otherwise it is the
   field's track from the music table, `0x003EAA70` (`0x0026201B`-`0x00262034`).
3. Unless that track is boss music (`0x00361010`, `0x00262041`), the battle mode decides: summon mode makes it `0x5B`,
   chocobo mode `0x5A` (`0x0026204A`-`0x00262063`). Summon mode is `0x0030D9A0` answering 1 and chocobo mode answering 2
   (`0x003135C0`, `0x00303EC0`).

The table, its story ladder and the boss-music bit are on [Music table](music-table.md).

### Starting the track

`0x003614C0(track, 0x78, 1)` starts the track at full volume through `0x003614E0` (`0x002620A8`):

| Case | What happens |
|---|---|
| a music change is already pending, `0x022CBA58` | nothing; answers 0 |
| the track is already playing, `0x0215EF44` (`0x002DEC00`) | answers 2, and `0x002DEE50(current, 0x78, 0x7F)` fades it back to full volume (`0x002620BB`) |
| otherwise | schedules the change as a task with the track, the length and the volume, marks busy bit 6 (`0x003601B0(6)`) and answers 1 |

`0x002DEE50(track, length, volume)` stores the volume at `0x0215EF4D` and passes the fade to the music controller through
`0x001DBCA0`; a negative track with nothing playing does nothing.

### No track

When no track is chosen and one is playing, `0x002DEE50(current, 0x78)` and `0x00361170(current, 0x78, 1)` fade it out
(`0x00262080`, `0x00262090`). When nothing is playing, `+0x17` bit 7 is cleared (`0x00262097`). With bit 7 clear,
`0x00360D30` clears `0x022CBA60` and calls `0x002DE050` when it was set (`0x002620C5`-`0x002620D0`).

### The change task

`0x003614E0` hands the change to one of two tasks, and `0x00361460` ends either one by clearing busy bit 6:

- With `0x022CBA60` clear, `0x00360EE0` loads the track into a slot (`0x00361630`) and waits for it to be ready. With a
  track playing it crossfades to the new one (`0x002DEC30`); with none, it sets the volume (`0x002DEE30`) and starts the
  track. When the task's release flag is set it then schedules the old track's end (`0x00361170`).
- With `0x022CBA60` set, `0x00361340` fades the current track out (`0x002DEE50`, `0x00361170`), waits until no track is
  current, then loads, sets the volume and starts the new one the same way.

The start is fresh (`0x002DED30`) when the top byte of the task word is 0, and from the track's resume point
(`0x002DEDB0`) otherwise; `0x003614C0` passes 0, so area music always starts fresh.

`0x00361170(track, length, release)` marks the track's slot as fading and schedules `0x00361080` after `length` frames.
`0x00361200` does the same for every loaded slot, with a fade of 120 frames for a negative length. When `0x00361080` runs
it calls the stop `0x002DEDE0` with the slot's own index, byte `+0x03`, which names no shipped track. With the release
flag and the fading bit it then stops and frees the slot's track (`0x002DEDE0`, `0x002DEC20`), or marks a slot still
loading for release.

### Track slots

The script music verbs load tracks into four slots at `0x022CB9F0` (layout below):

1. `0x00361630(track)`, from `musicread` `0x229` (`0x00341710`) and the begin of `musicplay` `0x22B` (`0x00342770`), keeps a
   slot already holding the track and clears its two flag bits. A new track takes the first free slot only when that
   is slot 0 or 1 (`0x0036169A`), asks the music controller for a load id (`0x001DBB80`) and sets state 4.
2. The pump `0x00360B50` sets state 5 once the load id is done (`0x002DEE90`), and empties a ready slot whose bit 0 is set:
   it stops the track (`0x002DEDE0`) and frees its bank (`0x002DEC20`, `0x00210960`). States 1 and 2 step to a load.
3. `0x00360DD0` marks every slot except the current track's for release, emptying ready ones at once.

`0x00360C20`, `0x00361480` and `0x00361030` find a track's slot by number and answer its state, its index or its address;
`0x00360C00` answers a slot's state by index. `musicreadsync` `0x22A` waits while its slot's state is neither 0 nor 5
(`0x00341F90`).

### Fresh starts and resume points

The music controller keeps one resume point per track number in the object manager: the position at `+0x3D8` and a
set flag at `+0x7D8`, 256 each ([Audio manager](audio-manager.md)). `0x00222A40` stores the driver's position
(`0x007A91D0`) through `0x00221720`; `0x002228A0` starts from a stored point, read by `0x00221100` and `0x00220DA0`, and clears it
(`0x00221280`). The calls in front of it:

| Call | Does |
|---|---|
| `0x002DEC30(track, length)` | clears the track's point and crossfades to it over `length` (`0x00218AE0`); the other tracks fade out |
| `0x002DEC80(track, section)` | full volume, clears the point and starts from section `section` (`0x00218C10`) |
| `0x002DED30(track)` | clears the point and starts at once (`0x00218C40`) |
| `0x002DED70(track)` | full volume and starts at once, from the point when one is stored |
| `0x002DEDB0(track)` | starts at once, from the point when one is stored |
| `0x002DEDD0()` | stores the current track's point (`0x00218D00`) |
| `0x002DEDE0(track)` | stores the point when the track is current, then stops it (`0x00218D70`) |
| `0x002DEE30(track, volume)` | sets the volume at once (`0x00222B20`) |
| `0x002DEC20(track)` | frees the track's banks (`0x00218A30`) |

Each starting call makes the track current at `0x0215EF44`. A stop with `0x002DEDE0` therefore leaves a point that a
later `0x002DED70` or `0x002DEDB0` continues from.

### Skipped scenes

While an event manager's skip mask is set (`0x00267310`), the music verbs play nothing:

1. They record the track they would leave playing, a second value and the resume flag at `0x022CB9B0`-`0x022CB9B8`
   (`0x00360960`); `musicstop` records no track (`0x00345010`).
2. `skipexec` (`0x00360710`) stores the current track's point (`0x002DEDD0`) and records it with the resume flag set.
   `0x00360880` runs `0x00360710` for the first armed skip of each of managers 1-3 (`0x022CB9C4`).
3. The skip-end stage `0x003608D0` starts the recorded track through `0x003614E0` with a 16-frame change, or only sets its
   volume when it already plays.

### The music version

The Config option for the music version ([Game settings](../Saving-Loading-And-Settings/game-settings.md)) reaches the
manager through `0x002DF530(version, live)`, which clamps it to 0-2. `0x002109F0` keeps it at manager `+0x30`; when it
changes while a track is current and `live` is set, `0x00218DC0` sends each of that track's banks action `0x26` with the
new version and 4.0 (`0x00222AD0`). `0x002228A0` passes manager `+0x30` to the driver's play calls (`0x007A93A0`,
`0x007A92C0`), so every start uses the chosen version.

### The saved override

| Verb | Id | Body | Does |
|---|---|---|---|
| `setnowmapmusicno` | `0x471` | `0x00345E70` -> `0x0026A720` | a track sets payload `+0x1063` bit 6 and `+0x1534`; a negative value clears both |
| `getnowmapmusicno` | `0x470` | `0x00345760` -> `0x0026DE00` | the area's track as chosen above, with the summon and chocobo tracks |
| `getnowmapmusicno_47a` | `0x47A` | `0x00345400` -> `0x0026DE00` | the same; a non-zero argument leaves out the summon and chocobo tracks (`0x0026DE20`) |
| `isbossmusic` | `0x47B` | `0x00349E10` -> `0x00361010` | the track's boss-music bit |

The shipping scripts call `setnowmapmusicno` 1,393 times, 229 of them with -1, `getnowmapmusicno` 1,346 times,
`getnowmapmusicno_47a` 1,925 times and `isbossmusic` 591 times.

### The script music stream

The verbs `bgmstreamread` `0x448` to `getbgmstreamstatus` `0x44F` drive a separate streamed-music player. No shipped
script calls any of the eight; the developer verb `debug_bgmstream` `0x201E` (`0x0050C7F0`) is the only other entry.
`usebgmstream` `0x44D` (`0x003557C0`) sizes its buffer: `0x003EACA0` rounds the request up to 64 KiB, with at least
`0x30000` bytes, allocates it under the name `BGMSTR`, and `0x003EB180` keeps the buffer and the size at `0x02B5E0E8`
and `0x02B5E0F0`.

`bgmstreamplay` `0x44A` is a jump (`0x00354D60`) to `0x003EB150`: while
the stream is armed (byte `0x02B5E111` non-zero) and its state byte `0x02B5E110` is 5, it sets the state to 6; in any
other state it changes nothing.

## Layouts

A track slot, `0x18` bytes, four at `0x022CB9F0` (`0x00360C70` sets them up):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | state | 0 free, 3 load asked, 4 loading, 5 ready (`0x00360B50`) |
| `+0x01` | `u8` | track | the track number |
| `+0x02` | `u8` | flags | bit 0 empty the slot when ready, bit 1 fading out (`0x00361170`) |
| `+0x03` | `u8` | index | the slot's own index, returned by `0x00361630` |
| `+0x14` | `u32` | loadId | the music controller's load id (`0x00361630`) |

## Modding notes

- The crossfade length `0x78` and the volume `0x7F` are immediate operands at `0x0026207C`, `0x00262085`, `0x0026209D` and
  in `0x003614C0`.
- Clearing a zone's done bit, `+0x10` bit 6, makes the next call choose the music again.
- The saved override survives saving and loading, because it is payload bytes `+0x1063` and `+0x1534`.

## Related

- [Music table](music-table.md) - the field-to-track table and the boss-music bit.
- [Audio manager](audio-manager.md) - the music controller and its resume table.
- [Sound banks](sound-banks.md) - the `.mab` track files.
- [Zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md) - the field id and the zone setup.
- [Chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md) - chocobo mode.
