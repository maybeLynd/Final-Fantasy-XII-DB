---
title: "Music: which track plays in an area, the chocobo and summon tracks, the crossfade when the area changes, and the saved track override"
kind: "system"
category: "Sound and music"
summary: "How the area's music is chosen and changed: the once-per-zone step and its done bit, the four sources in order (the saved override, the field-to-track table with its story ladder, then the summon and chocobo tracks unless the track is boss music), the crossfade's one length and one volume, what happens when no track is chosen, the script verbs that set, read and test the area music, and the script music stream no shipped script uses."
addresses: ["00261F90", "003EAA70", "00361010", "0030D9A0", "003614E0", "002DEE50", "0026A720", "0026DE20"]
---

# Music: which track plays in an area, the chocobo and summon tracks, the crossfade when the area changes, and the saved track override

## What the player sees

- Entering an area crossfades to its music, or keeps the music when the track is the same.
- Riding a chocobo or calling a summon plays their own track, except over boss music.
- Some story scenes pin a track that stays through area changes until a later scene releases it, and the pin is kept
  in the save.

## How it works

### When the area's music is chosen

The zone setup `0025D9E0` calls `00261F90` (`0025DB8E`) for the zone being entered:

1. It returns when the zone's `+0x28` is not 0 or its done bit, `+0x10` bit 6, is set (`00261F96`-`00261FA7`).
2. It chooses music only when `+0x17` bit 7 is set (`00262000`).
3. It always sets the done bit on the way out (`002620D5`), so the music is chosen once per zone.

### Which track

1. The field id is payload `+0x1044` (`0026200F`, `003148F0`).
2. When payload `+0x1063` bit 6 is set, the track is the saved override at payload `+0x1534`; otherwise it is the
   field's track from the music table, `003EAA70` (`0026201B`-`00262034`).
3. Unless that track is boss music (`00361010`, `00262041`), the battle mode decides: summon mode makes it `0x5B`,
   chocobo mode `0x5A` (`0026204A`-`00262063`). Summon mode is `0030D9A0` answering 1 and chocobo mode answering 2
   (`003135C0`, `00303EC0`).

The table, its story ladder and the boss-music bit are on [Music table](music-table.md).

### Starting the track

`003614C0(track, 0x78, 1)` starts the track at full volume through `003614E0` (`002620A8`):

| Case | What happens |
|---|---|
| a music change is already pending, `022CBA58` | nothing; answers 0 |
| the track is already playing, `0215EF44` (`002DEC00`) | answers 2, and `002DEE50(current, 0x78, 0x7F)` fades it back to full volume (`002620BB`) |
| otherwise | schedules the change as a task with the track, the length and the volume, marks busy bit 6 (`003601B0(6)`) and answers 1 |

`002DEE50(track, length, volume)` stores the volume at `0215EF4D` and passes the fade to the music controller through
`001DBCA0`; a negative track with nothing playing does nothing.

### No track

When no track is chosen and one is playing, `002DEE50(current, 0x78)` and `00361170(current, 0x78, 1)` fade it out
(`00262080`, `00262090`). When nothing is playing, `+0x17` bit 7 is cleared (`00262097`). With bit 7 clear,
`00360D30` clears `022CBA60` and calls `002DE050` when it was set (`002620C5`-`002620D0`).

### The saved override

| Verb | Id | Body | Does |
|---|---|---|---|
| `setnowmapmusicno` | `0x471` | `00345E70` -> `0026A720` | a track sets payload `+0x1063` bit 6 and `+0x1534`; a negative value clears both |
| `getnowmapmusicno` | `0x470` | `00345760` -> `0026DE00` | the area's track as chosen above, with the summon and chocobo tracks |
| `getnowmapmusicno_47a` | `0x47A` | `00345400` -> `0026DE00` | the same; a non-zero argument leaves out the summon and chocobo tracks (`0026DE20`) |
| `isbossmusic` | `0x47B` | `00349E10` -> `00361010` | the track's boss-music bit |

The shipping scripts call `setnowmapmusicno` 1,393 times, 229 of them with -1, `getnowmapmusicno` 1,346 times,
`getnowmapmusicno_47a` 1,925 times and `isbossmusic` 591 times.

### The script music stream

The verbs `bgmstreamread` `0x448` to `getbgmstreamstatus` `0x44F` drive a separate streamed-music player. No shipped
script calls any of the eight; the developer verb `debug_bgmstream` `0x201E` (`0050C7F0`) is the only other entry.

## Modding notes

- The crossfade length `0x78` and the volume `0x7F` are immediate operands at `0026207C`, `00262085`, `0026209D` and
  in `003614C0`.
- Clearing a zone's done bit, `+0x10` bit 6, makes the next call choose the music again.
- The saved override survives saving and loading, because it is payload bytes `+0x1063` and `+0x1534`.

## Related

- [Music table](music-table.md) - the field-to-track table and the boss-music bit.
- [Sound banks](sound-banks.md) - the `.mab` track files.
- [Zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md) - the field id and the zone setup.
- [Chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md) - chocobo mode.
