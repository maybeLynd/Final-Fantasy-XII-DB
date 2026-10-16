---
title: "Music: which track plays in an area, the chocobo and summon tracks, the crossfade when the area changes, and the saved track override"
kind: "system"
category: "Sound and music"
addresses: "00261F90, 003EAA70, 00361010, 0030D9A0, 003614E0, 002DEE50, 0026A720, 0026DE20"
---

## What the player sees

- Entering an area crossfades to its music, or keeps the music when the track is the same.
- Riding a chocobo or calling a summon plays their own track, except over boss music.
- Some story scenes pin a track that stays through area changes until a later scene releases it, and the pin is kept
  in the save.

## How it works

### When the area's music is chosen

The zone setup `0025D9E0` calls `00261F90` (`0025DB8E`) for the zone being entered:

1. It returns when the zone's `+28`<sub>h</sub> is not 0 or its done bit, `+10`<sub>h</sub> bit 6, is set (`00261F96`-`00261FA7`).
2. It chooses music only when `+17`<sub>h</sub> bit 7 is set (`00262000`).
3. It always sets the done bit on the way out (`002620D5`), so the music is chosen once per zone.

### Which track

1. The field id is payload `+1044`<sub>h</sub> (`0026200F`, `003148F0`).
2. When payload `+1063`<sub>h</sub> bit 6 is set, the track is the saved override at payload `+1534`<sub>h</sub>; otherwise it is the
   field's track from the music table, `003EAA70` (`0026201B`-`00262034`).
3. Unless that track is boss music (`00361010`, `00262041`), the battle mode decides: summon mode makes it `5B`<sub>h</sub>,
   chocobo mode `5A`<sub>h</sub> (`0026204A`-`00262063`). Summon mode is `0030D9A0` answering 1 and chocobo mode answering 2
   (`003135C0`, `00303EC0`).

The table, its story ladder and the boss-music bit are on [Music table](music-table.md).

### Starting the track

`003614C0(track, 78h, 1)` starts the track at full volume through `003614E0` (`002620A8`):

| Case | What happens |
|---|---|
| a music change is already pending, `022CBA58` | nothing; answers 0 |
| the track is already playing, `0215EF44` (`002DEC00`) | answers 2, and `002DEE50(current, 78h, 7Fh)` fades it back to full volume (`002620BB`) |
| otherwise | schedules the change as a task with the track, the length and the volume, marks busy bit 6 (`003601B0(6)`) and answers 1 |

`002DEE50(track, length, volume)` stores the volume at `0215EF4D` and passes the fade to the music controller through
`001DBCA0`; a negative track with nothing playing does nothing.

### No track

When no track is chosen and one is playing, `002DEE50(current, 78h)` and `00361170(current, 78h, 1)` fade it out
(`00262080`, `00262090`). When nothing is playing, `+17`<sub>h</sub> bit 7 is cleared (`00262097`). With bit 7 clear,
`00360D30` clears `022CBA60` and calls `002DE050` when it was set (`002620C5`-`002620D0`).

### The change task

`003614E0` hands the change to one of two tasks, and `00361460` ends either one by clearing busy bit 6:

- With `022CBA60` clear, `00360EE0` loads the track into a slot (`00361630`) and waits for it to be ready. With a
  track playing it crossfades to the new one (`002DEC30`); with none, it sets the volume (`002DEE30`) and starts the
  track. When the task's release flag is set it then schedules the old track's end (`00361170`).
- With `022CBA60` set, `00361340` fades the current track out (`002DEE50`, `00361170`), waits until no track is
  current, then loads, sets the volume and starts the new one the same way.

The start is fresh (`002DED30`) when the top byte of the task word is 0, and from the track's resume point
(`002DEDB0`) otherwise; `003614C0` passes 0, so area music always starts fresh.

`00361170(track, length, release)` marks the track's slot as fading and schedules `00361080` after `length` frames.
`00361200` does the same for every loaded slot, with a fade of 120 frames for a negative length. When `00361080` runs
it calls the stop `002DEDE0` with the slot's own index, byte `+03`<sub>h</sub>, which names no shipped track. With the release
flag and the fading bit it then stops and frees the slot's track (`002DEDE0`, `002DEC20`), or marks a slot still
loading for release.

### Track slots

The script music verbs load tracks into four slots at `022CB9F0` (layout below):

1. `00361630(track)`, from `musicread` `229`<sub>h</sub> (`00341710`) and the begin of `musicplay` `22B`<sub>h</sub> (`00342770`), keeps a
   slot already holding the track and clears its two flag bits. A new track takes the first free slot only when that
   is slot 0 or 1 (`0036169A`), asks the music controller for a load id (`001DBB80`) and sets state 4.
2. The pump `00360B50` sets state 5 once the load id is done (`002DEE90`), and empties a ready slot whose bit 0 is set:
   it stops the track (`002DEDE0`) and frees its bank (`002DEC20`, `00210960`). States 1 and 2 step to a load.
3. `00360DD0` marks every slot except the current track's for release, emptying ready ones at once.

`00360C20`, `00361480` and `00361030` find a track's slot by number and answer its state, its index or its address;
`00360C00` answers a slot's state by index. `musicreadsync` `22A`<sub>h</sub> waits while its slot's state is neither 0 nor 5
(`00341F90`).

### Fresh starts and resume points

The music controller keeps one resume point per track number in the object manager: the position at `+3D8`<sub>h</sub> and a
set flag at `+7D8`<sub>h</sub>, 256 each ([Audio manager](audio-manager.md)). `00222A40` stores the driver's position
(`007A91D0`) through `00221720`; `002228A0` starts from a stored point, read by `00221100` and `00220DA0`, and clears it
(`00221280`). The calls in front of it:

| Call | Does |
|---|---|
| `002DEC30(track, length)` | clears the track's point and crossfades to it over `length` (`00218AE0`); the other tracks fade out |
| `002DEC80(track, section)` | full volume, clears the point and starts from section `section` (`00218C10`) |
| `002DED30(track)` | clears the point and starts at once (`00218C40`) |
| `002DED70(track)` | full volume and starts at once, from the point when one is stored |
| `002DEDB0(track)` | starts at once, from the point when one is stored |
| `002DEDD0()` | stores the current track's point (`00218D00`) |
| `002DEDE0(track)` | stores the point when the track is current, then stops it (`00218D70`) |
| `002DEE30(track, volume)` | sets the volume at once (`00222B20`) |
| `002DEC20(track)` | frees the track's banks (`00218A30`) |

Each starting call makes the track current at `0215EF44`. A stop with `002DEDE0` therefore leaves a point that a
later `002DED70` or `002DEDB0` continues from.

### Skipped scenes

While an event manager's skip mask is set (`00267310`), the music verbs play nothing:

1. They record the track they would leave playing, a second value and the resume flag at `022CB9B0`-`022CB9B8`
   (`00360960`); `musicstop` records no track (`00345010`).
2. `skipexec` (`00360710`) stores the current track's point (`002DEDD0`) and records it with the resume flag set.
   `00360880` runs `00360710` for the first armed skip of each of managers 1-3 (`022CB9C4`).
3. The skip-end stage `003608D0` starts the recorded track through `003614E0` with a 16-frame change, or only sets its
   volume when it already plays.

### The music version

The Config option for the music version ([Game settings](../Saving-Loading-And-Settings/game-settings.md)) reaches the
manager through `002DF530(version, live)`, which clamps it to 0-2. `002109F0` keeps it at manager `+30`<sub>h</sub>; when it
changes while a track is current and `live` is set, `00218DC0` sends each of that track's banks action `26`<sub>h</sub> with the
new version and 4.0 (`00222AD0`). `002228A0` passes manager `+30`<sub>h</sub> to the driver's play calls (`007A93A0`,
`007A92C0`), so every start uses the chosen version.

### The saved override

| Verb | Id | Body | Does |
|---|---|---|---|
| `setnowmapmusicno` | `471`<sub>h</sub> | `00345E70` -> `0026A720` | a track sets payload `+1063`<sub>h</sub> bit 6 and `+1534`<sub>h</sub>; a negative value clears both |
| `getnowmapmusicno` | `470`<sub>h</sub> | `00345760` -> `0026DE00` | the area's track as chosen above, with the summon and chocobo tracks |
| `getnowmapmusicno_47a` | `47A`<sub>h</sub> | `00345400` -> `0026DE00` | the same; a non-zero argument leaves out the summon and chocobo tracks (`0026DE20`) |
| `isbossmusic` | `47B`<sub>h</sub> | `00349E10` -> `00361010` | the track's boss-music bit |

The shipping scripts call `setnowmapmusicno` 1,393 times, 229 of them with -1, `getnowmapmusicno` 1,346 times,
`getnowmapmusicno_47a` 1,925 times and `isbossmusic` 591 times.

### The script music stream

The verbs `bgmstreamread` `448`<sub>h</sub> to `getbgmstreamstatus` `44F`<sub>h</sub> drive a separate streamed-music player. No shipped
script calls any of the eight; the developer verb `debug_bgmstream` `201E`<sub>h</sub> (`0050C7F0`) is the only other entry.
`usebgmstream` `44D`<sub>h</sub> (`003557C0`) sizes its buffer: `003EACA0` rounds the request up to 64 KiB, with at least
`30000`<sub>h</sub> bytes, allocates it under the name `BGMSTR`, and `003EB180` keeps the buffer and the size at `02B5E0E8`
and `02B5E0F0`.

## Layouts

A track slot, `18`<sub>h</sub> bytes, four at `022CB9F0` (`00360C70` sets them up):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | state | 0 free, 3 load asked, 4 loading, 5 ready (`00360B50`) |
| `01`<sub>h</sub> | `u8` | track | the track number |
| `02`<sub>h</sub> | `u8` | flags | bit 0 empty the slot when ready, bit 1 fading out (`00361170`) |
| `03`<sub>h</sub> | `u8` | index | the slot's own index, returned by `00361630` |
| `14`<sub>h</sub> | `u32` | loadId | the music controller's load id (`00361630`) |

## Modding notes

- The crossfade length `78`<sub>h</sub> and the volume `7F`<sub>h</sub> are immediate operands at `0026207C`, `00262085`, `0026209D` and
  in `003614C0`.
- Clearing a zone's done bit, `+10`<sub>h</sub> bit 6, makes the next call choose the music again.
- The saved override survives saving and loading, because it is payload bytes `+1063`<sub>h</sub> and `+1534`<sub>h</sub>.

## Related

- [Music table](music-table.md) - the field-to-track table and the boss-music bit.
- [Audio manager](audio-manager.md) - the music controller and its resume table.
- [Sound banks](sound-banks.md) - the `.mab` track files.
- [Zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md) - the field id and the zone setup.
- [Chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md) - chocobo mode.
