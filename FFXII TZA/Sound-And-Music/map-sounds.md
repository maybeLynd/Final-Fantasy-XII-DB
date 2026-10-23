---
title: "Map sounds: the per-map sound list, the sounds its scripts and emitters play, and the weather ambience"
kind: "format"
category: "Sound and music"
addresses: "0x003635E0, 0x00363750, 0x00363E40, 0x00346260, 0x00346990, 0x003638B0, 0x00363B40, 0x002DF070, 0x022CBAF8"
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

When the map pack binds its sound, `0x003635E0(list, bank, handle)`:

1. unbinds the previous list (`0x00363750`);
2. takes the pack's bank, or `list + [list + 0x0C]` when none is given;
3. opens every `SeSep` record in `[list + 0x08]` bytes through `0x002DF070` ([Sound banks](sound-banks.md)) and calls
   `0x002DEE90(-1)`, which returns at once because the load query answers 0 for a negative id
   ([Audio manager](audio-manager.md));
4. frees the pack's bank block (`0x003697F0`);
5. keeps the handle at `0x022CBA88` and the list at `0x022CBAF8`, and resets the ambience volume to `0x7F`.

### Playing an entry

| Verb | Id | Body | Plays |
|---|---|---|---|
| `mapsoundplay(i)` | `0x2BA` | `0x00346260` | entry `i` through `0x002DF010` at pan `0x40`, volume `0x7F`, unless `0x00267310` answers non-zero for the actor |
| `mapsoundplay_2bb(i, pan, volume)` | `0x2BB` | `0x00346990` | entry `i` through `0x002DEF40` with the given pan and volume |

Both play nothing when no list is bound or `i` is at or past the count, compared unsigned (`0x00346291`, `0x003469D5`).

### Emitters

The pack's `SP1` block holds the map's sound emitters. For each one, `0x003638B0` reads its first word as a list index
and plays the id at the emitter's position, `+0x20`-`+0x28`, through `0x002DEFA0` (`0x0036397F`-`0x00363996`) when:

- the index is in range and the id is not negative;
- `0x00229EA0` answers 2 and `0x022CBB2E` is set;
- the emitter's flag byte `+0x08` has bits `0x30` clear, and bit 2 clear or bit 3 set.

Each update `0x00362850` marks every emitter with bit 6, runs the emitters it reaches through `0x003631B0`, and then
`0x00363F30(list, area)` stops the handle at `+0x04` of every emitter still marked or with bit 4 or 5 set (mask
`0x70`), or of all of them while `0x022CBB2E` is clear or when `area`, the `0x00362E50` result, is 0 (`0x002DF0F0`).
It clears the bit-6 mark of every emitter, and `0x00362850` then clears bit 3 of every emitter. `0x00363180(i)` sets
bit 3 of emitter `i` (`0x00362DC0`), so a bit-2 emitter plays for that pass; the map pack's switch records call it
from `0x003E8440` and `0x003E8690`.

### Reverb

`0x00362850` also sets the reverb level. It takes the value `0x003631B0` returns from the emitters, or the locked value
`0x022CBA84` while `0x022CBA91` is set, and when that differs from `0x022CBA80` it sends it through `0x002DF410(1, 0xB4,
level)`: driver action `0x2E` for parameter 7 at `level / 127` over 3 s ([Audio manager](audio-manager.md)).

| Verb | Id | Body | Does |
|---|---|---|---|
| `lockreverb` | `0x1D6` | `0x003417C0` | locks its one value as the level (`0x003631A0(1, level)`) and resets the frame count (`0x00363B20(-1)`) |
| `lockreverb_2a5` | `0x2A5` | `0x00341460` | stores one value as the frame count (`0x00363B20`) and locks the other as the level |
| `unlockreverb` | `0x1D7` | `0x00341D00` | unlocks (`0x003631A0(0, 0)`) and resets the frame count |

`0x00363B20` stores its count at `0x022CBB30`, 180 for 0 or less, and the event teardown `0x00262870` unlocks as well.

### Weather ambience

`0x00363B40` picks the ambience when the weather is set (`0x002620E0`):

1. It reads up to three entries of the list's weather table, or of the `SP1` block's table at `+0x04` when the list
   has none, into three selections at `0x022CBB58`. An index in range whose id is above 0 is kept, and each id is
   added once to a keep list at `0x022CBB64`.
2. The weather slot is `0x00265920()` minus one; a slot at or past the table's count picks nothing.
3. A new ambience becomes `0x022CBA7C`. While `0x022CBB2D` is set it starts at once through `0x00363840`. Otherwise it
   waits in `0x022CBA7C` until `0x003633B0` or `0x00363410` sets `0x022CBB2D`, which starts it through `0x00363840`: a
   playing ambience fades out over 15 frames (`0x002DF190(current, 0xF)`), and with none playing `0x003636A0` releases
   the previous map's kept ambiences (below).
4. With no ambience for the slot, the current one fades out over 180 frames (`0x002DF190(current, 0xB4)`).

Every update `0x00362850` also runs the two ambience steps:

- `0x00362C60` releases the previous map's kept ambiences (`0x003636A0`), resets the volume ramp and clears the fading
  handle `0x022CBA74` once the old one has stopped, or once the countdown `0x022CBA78`, run down by 2 per pass, goes
  below 0. It sends a changed ambience volume
  `0x022CBA92` to the playing handle `0x022CBA70` (`0x002DF150`).
- `0x00362D20` moves the map sound volume `0x022CBA94` from `0x022CBA98` towards `0x022CBA99` by the step `0x022CBA9C` per
  pass. Character and effect sounds take their volume byte from `0x022CBA94` ([Spatial sound](spatial-sound.md)).

`0x00363E40(frames)` stops the ambience:

- with no playing handle (`0x022CBA70 == 0`) it runs `0x003636A0` and resets the ramp: `0x022CBA9C = 0`,
  `0x022CBAA0 = 1.0`, and `0x022CBA94`, `0x022CBA98` and `0x022CBA99` to `0x7F`;
- with `frames > 0` it fades `0x022CBA7C` out over that many frames (`0x002DF190(0x022CBA7C, frames)`), moves the handle
  from `0x022CBA70` to `0x022CBA74` and sets the countdown `0x022CBA78 = frames`;
- otherwise it stops `0x022CBA7C` at once (`0x002DF0F0(0, 0x022CBA7C)`), runs `0x003636A0`, makes the same resets, clears
  both handles and sets `0x022CBA78 = -1`.

`envsoundtrans` (`0x57E`, `0x00346060`) ramps the ambience bank's volume through `0x00361730`, which calls
`0x002DF1E0(0x022CBA7C, frames, volume)` while a handle is held at `0x022CBA70`.

### Unbinding

`0x00363750` releases every listed id through `0x002DF050`, except an id from 1,000 to 1,999 that is in the keep list
(`0x00363774`-`0x003637E4`). It copies the three selections, the keep list and its count, `0x022CBB58`-`0x022CBB77`, over
`0x022CBB38`-`0x022CBB57` (`0x003637F0`-`0x00363810`) and releases the handle (`0x002DEB40`).

### The previous map's keep list

The copy keeps the previous map's ambiences loaded until the next ambience is picked. `0x003636A0` then releases
(`0x002DF050`) each of the previous ids at `0x022CBB44` that is above 0 and not in the current keep list `0x022CBB64`
(count `0x022CBB70`) (`0x003636A6`-`0x00363716`), so an ambience both maps keep stays loaded. It runs from the weather
pick (`0x00363D47`, `0x00363DE1`), `0x00362C60` (`0x00362C8C`), `0x00363E40` (`0x00363E93`, `0x00363EE9`), `0x002628B0`
(`0x00262920`), `0x003601D0` (`0x00360317`) and `0x00363560` (`0x0036359B`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022CBB50` | `i32` | 0 (zero-filled tail) | the count of the previous map's keep list at `0x022CBB44` | the map-sound initialiser `0x00362F70`, 0 (`0x00363036`), after setting both lists to -1 (`0x00363020`-`0x00363064`); `0x00363750`, the copy of `0x022CBB70` (`0x00363810`) | `0x003636A0` (`0x003636A6`, `0x00363700`) |

These are all its accesses among the RIP-relative references; no image-base-relative reference or disp32
displacement names it.

### Event sound lists

A cutscene's sounds come from SPP1 lists in the event's `.snd`, a PKFL pack of 16 sub-files whose `0x88`-byte
directory the event loader reads into `0x022C6E98` (`0x0032FE94`). Each event manager has eight sound slots of `0x38`
bytes from `0x02B59360`, indexed `manager x 8 + slot`, and slot `k` reads sub-file `k`:

1. `eventsoundread` `0x151` (`0x00344660` -> `0x003DF3E0`) empties the slot (`0x003DEC90`), sets its bit in the
   manager's mask at `0x02B59C20` and asks for the sub-file (`0x003DF440`, `0x0032F2F0`). The verb does nothing while the
   manager is skipping (`0x00267310`), and `0x003DF440` parks a slot in state 1 instead of reading during a skip.
2. When the read is in, `0x003DF2C0` splits the sub-file into its two parts (`0x0036B970`), the list and its `SeSep`
   records, and `0x003DF360` opens the banks (`0x002DF070`), keeps the bank handle at slot `+0x00` and sets state 4.
3. `eventsoundreadsync` `0x152` waits on `0x00345250` while the slot is in state 2, 3 or 4 (`0x003DF0F0`, `0x003DF0A0`).

`eventsoundplay` `0x153` (`0x00345930` -> `0x003DF200`) plays list entry `word & 0xFFFFFF` of slot `(word >> 24) - 4`
centred (`0x002DF010`); `eventsoundplay_16a` `0x16A` (`0x00350700` -> `0x003DF130`) gives a pan and volume (`0x002DEF40`).
Both need state 1 or 5 and an entry below the count, store the entry's `i16` from the table at list `+0x18` at
`0x022C2534` (`0x00314D50`), or -1 without one, and clear `0x022C2530` (`0x00314000`).

`eventsounddispose` `0x154` (`0x00347470` -> `0x003DEC90`) waits out a read or bank load and then releases the slot: in
state 5 it releases every listed id (`0x002DF050`) and calls `0x002DEB40` for each of the list's `+0x10` words from
`+0x12`; in state 1 `0x003DEFC0` only frees the blocks and the mask bit. When a list's `+0x10` is set, `0x003DF2C0` also
passes `mapNo % 10` to `0x0032F3A0`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "SPP1" |
| `+0x04` | `u32` | count | ids in the list |
| `+0x08` | `u32` | bankLength | bytes of SeSep records to open |
| `+0x0C` | `u32` | bankOffset | the records' offset when the pack gives no bank |
| `+0x10` | `u16` | hasMapNo | 1 when `+0x12` is a map number |
| `+0x12` | `u16` | mapNo | the zone's map number, or `0xFFFF` |
| `+0x14` | `u32` | zero14 | 0 |
| `+0x18` | `u16` | padAt | the id list's end rounded up to 16 |
| `+0x1A` | `u16` | weatherAt | the weather table's offset, or 0 |
| `+0x1C` | `u32` | zero1C | 0 |

Each id entry, `Spp1Id`, 4 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | soundId | a six-digit bank id |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | count | entries |
| `+0x02` | `i16[7]` | entry | a list index per weather slot; -1 for none |

The magic, `+0x10`-`+0x18` and `+0x1C` are read by none of the binder, the unbinder, the two verbs, the emitter
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
| `+0x10`, `+0x12` | `(1, map number)` in 386 lists, `(0, 0xFFFF)` in 160 |
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
| `+0x10` | 1 in 319 lists, 0 in 136 |

All but one id name a shipped bank under `se600`-`se610`; `600070` has none.

## Loader behaviour

1. `0x002DF070` rounds the length up to 16 and stops at a record that is not `SeSep` or is longer than what remains.
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
