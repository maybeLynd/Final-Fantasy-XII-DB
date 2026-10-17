---
title: "Map sounds: the per-map sound list, the sounds its scripts and emitters play, and the weather ambience"
kind: "format"
category: "Sound and music"
addresses: "003635E0, 00363750, 00363E40, 00346260, 00346990, 003638B0, 00363B40, 002DF070, 022CBAF8"
---

## What the player sees

- Each area has its own set of sound effects: doors, machinery, water, wildlife.
- A looping ambience plays in many areas and changes when the weather changes.
- Leaving an area unloads its sounds, except an ambience the next area also uses.

## Where it comes from

Each map pack (`.mpk`) carries its list in slot 10 and its `SeSep` sound-bank records in slot 0
([Map pack](../World-Areas-And-Travel/mpk-map-pack.md)); 545 packs have one. The one loose list,
`ps2data/sound/se/map/position_map/spp/env/env99.spp`, carries its bank after the list.

### Binding

When the map pack binds its sound, `003635E0(list, bank, handle)`:

1. unbinds the previous list (`00363750`);
2. takes the pack's bank, or `list + [list + 0Ch]` when none is given;
3. opens every `SeSep` record in `[list + 08h]` bytes through `002DF070` ([Sound banks](sound-banks.md)) and calls
   `002DEE90(-1)`, which returns at once because the load query answers 0 for a negative id
   ([Audio manager](audio-manager.md));
4. frees the pack's bank block (`003697F0`);
5. keeps the handle at `022CBA88` and the list at `022CBAF8`, and resets the ambience volume to `7F`<sub>h</sub>.

### Playing an entry

| Verb | Id | Body | Plays |
|---|---|---|---|
| `mapsoundplay(i)` | `2BA`<sub>h</sub> | `00346260` | entry `i` through `002DF010` at pan `40`<sub>h</sub>, volume `7F`<sub>h</sub>, unless `00267310` answers non-zero for the actor |
| `mapsoundplay_2bb(i, pan, volume)` | `2BB`<sub>h</sub> | `00346990` | entry `i` through `002DEF40` with the given pan and volume |

Both play nothing when no list is bound or `i` is at or past the count, compared unsigned (`00346291`, `003469D5`).

### Emitters

The pack's `SP1` block holds the map's sound emitters. For each one, `003638B0` reads its first word as a list index
and plays the id at the emitter's position, `+20`<sub>h</sub>-`+28`<sub>h</sub>, through `002DEFA0` (`0036397F`-`00363996`) when:

- the index is in range and the id is not negative;
- `00229EA0` answers 2 and `022CBB2E` is set;
- the emitter's flag byte `+08`<sub>h</sub> has bits `30`<sub>h</sub> clear, and bit 2 clear or bit 3 set.

Each update `00362850` marks every emitter with bit 6, runs the emitters it reaches through `003631B0`, and then
`00363F30(list, area)` stops the handle at `+04`<sub>h</sub> of every emitter still marked or with bit 4 or 5 set (mask
`70`<sub>h</sub>), or of all of them while `022CBB2E` is clear or when `area`, the `00362E50` result, is 0 (`002DF0F0`).
It clears the bit-6 mark of every emitter, and `00362850` then clears bit 3 of every emitter. `00363180(i)` sets
bit 3 of emitter `i` (`00362DC0`), so a bit-2 emitter plays for that pass; the map pack's switch records call it
from `003E8440` and `003E8690`.

### Reverb

`00362850` also sets the reverb level. It takes the value `003631B0` returns from the emitters, or the locked value
`022CBA84` while `022CBA91` is set, and when that differs from `022CBA80` it sends it through `002DF410(1, B4h,
level)`: driver action `2E`<sub>h</sub> for parameter 7 at `level / 127` over 3 s ([Audio manager](audio-manager.md)).

| Verb | Id | Body | Does |
|---|---|---|---|
| `lockreverb` | `1D6`<sub>h</sub> | `003417C0` | locks its one value as the level (`003631A0(1, level)`) and resets the frame count (`00363B20(-1)`) |
| `lockreverb_2a5` | `2A5`<sub>h</sub> | `00341460` | stores one value as the frame count (`00363B20`) and locks the other as the level |
| `unlockreverb` | `1D7`<sub>h</sub> | `00341D00` | unlocks (`003631A0(0, 0)`) and resets the frame count |

`00363B20` stores its count at `022CBB30`, 180 for 0 or less, and the event teardown `00262870` unlocks as well.

### Weather ambience

`00363B40` picks the ambience when the weather is set (`002620E0`):

1. It reads up to three entries of the list's weather table, or of the `SP1` block's table at `+04`<sub>h</sub> when the list
   has none, into three selections at `022CBB58`. An index in range whose id is above 0 is kept, and each id is
   added once to a keep list at `022CBB64`.
2. The weather slot is `00265920()` minus one; a slot at or past the table's count picks nothing.
3. A new ambience becomes `022CBA7C`. While `022CBB2D` is set it starts at once through `00363840`. Otherwise a
   playing ambience fades out over 15 frames first (`002DF190(current, Fh)`), and with none playing `003636A0`
   starts the new one.
4. With no ambience for the slot, the current one fades out over 180 frames (`002DF190(current, B4h)`).

Every update `00362850` also runs the two ambience steps:

- `00362C60` starts a pending ambience (`003636A0`) and resets the volume ramp once the old one has stopped, or once
  the countdown `022CBA78`, run down by 2 per pass, goes below 0. It sends a changed ambience volume
  `022CBA92` to the playing handle `022CBA70` (`002DF150`).
- `00362D20` moves the map sound volume `022CBA94` from `022CBA98` towards `022CBA99` by the step `022CBA9C` per
  pass. Character and effect sounds take their volume byte from `022CBA94` ([Spatial sound](spatial-sound.md)).

`00363E40(frames)` stops the ambience:

- with no playing handle (`022CBA70 == 0`) it runs `003636A0` and resets the ramp: `022CBA9C = 0`,
  `022CBAA0 = 1.0`, and `022CBA94`, `022CBA98` and `022CBA99` to `7F`<sub>h</sub>;
- with `frames > 0` it fades `022CBA7C` out over that many frames (`002DF190(022CBA7C, frames)`), moves the handle
  from `022CBA70` to `022CBA74` and sets the countdown `022CBA78 = frames`;
- otherwise it stops `022CBA7C` at once (`002DF0F0(0, 022CBA7C)`), runs `003636A0`, makes the same resets, clears
  both handles and sets `022CBA78 = -1`.

`envsoundtrans` (`57E`<sub>h</sub>, `00346060`) ramps the ambience bank's volume through `00361730`, which calls
`002DF1E0(022CBA7C, frames, volume)` while a handle is held at `022CBA70`.

### Unbinding

`00363750` releases every listed id through `002DF050`, except an id from 1,000 to 1,999 that is in the keep list
(`00363774`-`003637E4`). It copies the three selections and the keep list to `022CBB38` and releases the handle
(`002DEB40`).

### Event sound lists

A cutscene's sounds come from SPP1 lists in the event's `.snd`, a PKFL pack of 16 sub-files whose `88`<sub>h</sub>-byte
directory the event loader reads into `022C6E98` (`0032FE94`). Each event manager has eight sound slots of `38`<sub>h</sub>
bytes from `02B59360`, indexed `manager x 8 + slot`, and slot `k` reads sub-file `k`:

1. `eventsoundread` `151`<sub>h</sub> (`00344660` -> `003DF3E0`) empties the slot (`003DEC90`), sets its bit in the
   manager's mask at `02B59C20` and asks for the sub-file (`003DF440`, `0032F2F0`). The verb does nothing while the
   manager is skipping (`00267310`), and `003DF440` parks a slot in state 1 instead of reading during a skip.
2. When the read is in, `003DF2C0` splits the sub-file into its two parts (`0036B970`), the list and its `SeSep`
   records, and `003DF360` opens the banks (`002DF070`), keeps the bank handle at slot `+00`<sub>h</sub> and sets state 4.
3. `eventsoundreadsync` `152`<sub>h</sub> waits on `00345250` while the slot is in state 2, 3 or 4 (`003DF0F0`, `003DF0A0`).

`eventsoundplay` `153`<sub>h</sub> (`00345930` -> `003DF200`) plays list entry `word & FFFFFFh` of slot `(word >> 24) - 4`
centred (`002DF010`); `eventsoundplay_16a` `16A`<sub>h</sub> (`00350700` -> `003DF130`) gives a pan and volume (`002DEF40`).
Both need state 1 or 5 and an entry below the count, store the entry's `i16` from the table at list `+18`<sub>h</sub> at
`022C2534` (`00314D50`), or -1 without one, and clear `022C2530` (`00314000`).

`eventsounddispose` `154`<sub>h</sub> (`00347470` -> `003DEC90`) waits out a read or bank load and then releases the slot: in
state 5 it releases every listed id (`002DF050`) and calls `002DEB40` for each of the list's `+10`<sub>h</sub> words from
`+12`<sub>h</sub>; in state 1 `003DEFC0` only frees the blocks and the mask bit. When a list's `+10`<sub>h</sub> is set, `003DF2C0` also
passes `mapNo % 10` to `0032F3A0`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | magic | "SPP1" |
| `04`<sub>h</sub> | `u32` | count | ids in the list |
| `08`<sub>h</sub> | `u32` | bankLength | bytes of SeSep records to open |
| `0C`<sub>h</sub> | `u32` | bankOffset | the records' offset when the pack gives no bank |
| `10`<sub>h</sub> | `u16` | hasMapNo | 1 when `+12`<sub>h</sub> is a map number |
| `12`<sub>h</sub> | `u16` | mapNo | the zone's map number, or `FFFF`<sub>h</sub> |
| `14`<sub>h</sub> | `u32` | zero14 | 0 |
| `18`<sub>h</sub> | `u16` | padAt | the id list's end rounded up to 16 |
| `1A`<sub>h</sub> | `u16` | weatherAt | the weather table's offset, or 0 |
| `1C`<sub>h</sub> | `u32` | zero1C | 0 |

Each id entry, `Spp1Id`, 4 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | soundId | a six-digit bank id |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | count | entries |
| `02`<sub>h</sub> | `i16[7]` | entry | a list index per weather slot; -1 for none |

The magic, `+10`<sub>h</sub>-`+18`<sub>h</sub> and `+1C`<sub>h</sub> are read by none of the binder, the unbinder, the two verbs, the emitter
reader and the weather pick.

## Shipped data

| | |
|---|---|
| lists | 546: slot 10 of 545 packs and `env99.spp` |
| ids per list | 1 to 48; 6,523 in all, 632 distinct |
| the `SeSep` walk | opens exactly the listed ids, in order, in all 546 |
| ids 1,001-1,185 | 1,015 uses of 144 ids |
| ids 10,002-10,313 | 3,398 uses of 257 ids |
| ids 50,001-50,268 | 2,110 uses of 231 ids |
| the most used id | 10,293, in 115 lists |
| `+10`<sub>h</sub>, `+12`<sub>h</sub> | `(1, map number)` in 386 lists, `(0, FFFFh)` in 160 |
| weather tables | 545, with 3 entries in 226, 1 in 189 and 2 in 130; 12 of the 1,127 entries are -1 |

Every id names a shipped bank, `se001/se001NNN`, `se010/se010NNN` or `se050/se050NNN`. Ids from 1,000 to 1,999 are
the ambiences that survive an unbind.

### Event sound lists

| | |
|---|---|
| `.snd` packs | 256 per language folder, identical in all nine; 16 sub-files each |
| lists | 455, in sub-files 0-7: 242, 115, 34, 25, 17, 11, 7 and 4; every pack has 1 to 8 |
| ids per list | 1 to 46; 2,908 in all, 2,820 distinct, from 600,001 to 610,042 |
| the `SeSep` part | opens exactly the listed ids, in order, in 454 lists; slot 6 of `bhm_c0102` has no records part and a `bankOffset` of 0, so its three ids open no bank |
| `+10`<sub>h</sub> | 1 in 319 lists, 0 in 136 |

All but one id name a shipped bank under `se600`-`se610`; `600070` has none.

## Loader behaviour

1. `002DF070` rounds the length up to 16 and stops at a record that is not `SeSep` or is longer than what remains.
2. The verbs bound the index unsigned, the emitter and weather readers after a sign test.
3. The weather pick reads at most three entries, so a table's entries 4-7 change nothing.
4. Only `slot < count` is tested before the selection is read, so a count of 4 with weather slot 4 reads the keep
   list's first cell as a selection; shipped tables have at most 3.

## Modding notes

- A script plays a map sound by its number in the list, so reordering a list changes which sound each script line
  plays.
- To keep an ambience across a map change, give it an id from 1,000 to 1,999 and list it in both maps' weather tables.
- A new id needs its bank record in the pack's slot 0 and its file under `sead_data_win`.

## Related

- [Sound banks](sound-banks.md) - the `SeSep` records and the six-digit banks.
- [Sound effects](sound-effects.md) - the play and stop calls.
- [Map pack](../World-Areas-And-Travel/mpk-map-pack.md) - slots 0, 10 and 16.
- [Weather](../World-Areas-And-Travel/weather.md) - the weather slot.
