---
title: "Map sounds: the per-map sound list, the sounds its scripts and emitters play, and the weather ambience"
kind: "format"
category: "Sound and music"
summary: "The SPP1 map sound list carried in each map pack: its header, id list and weather table, how binding it opens every listed sound bank, the two script verbs that play an entry by number, the map's sound emitters, the ambience picked per weather slot with its fades, what unbinding keeps, and the shipped lists with their id ranges."
addresses: ["003635E0", "00363750", "00346260", "00346990", "003638B0", "00363B40", "002DF070", "022CBAF8"]
---

# Map sounds: the per-map sound list, the sounds its scripts and emitters play, and the weather ambience

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
2. takes the pack's bank, or `list + [list + 0x0C]` when none is given;
3. opens every `SeSep` record in `[list + 0x08]` bytes through `002DF070` ([Sound banks](sound-banks.md)), waiting for
   the loads (`002DEE90(-1)`);
4. frees the pack's bank block (`003697F0`);
5. keeps the handle at `022CBA88` and the list at `022CBAF8`, and resets the ambience volume to `0x7F`.

### Playing an entry

| Verb | Id | Body | Plays |
|---|---|---|---|
| `mapsoundplay(i)` | `0x2BA` | `00346260` | entry `i` through `002DF010` at pan `0x40`, volume `0x7F`, unless `00267310` answers non-zero for the actor |
| `mapsoundplay_2bb(i, pan, volume)` | `0x2BB` | `00346990` | entry `i` through `002DEF40` with the given pan and volume |

Both play nothing when no list is bound or `i` is at or past the count, compared unsigned (`00346291`, `003469D5`).

### Emitters

The pack's `SP1` block holds the map's sound emitters. For each one, `003638B0` reads its first word as a list index
and plays the id at the emitter's position, `+0x20`-`+0x28`, through `002DEFA0` (`0036397F`-`00363996`) when:

- the index is in range and the id is not negative;
- `00229EA0` answers 2 and `022CBB2E` is set;
- the emitter's flag byte `+0x08` has bits `0x30` clear, and bit 2 clear or bit 3 set.

### Weather ambience

`00363B40` picks the ambience when the weather is set (`002620E0`):

1. It reads up to three entries of the list's weather table, or of the `SP1` block's table at `+0x04` when the list
   has none, into three selections at `022CBB58`. An index in range whose id is above 0 is kept, and each id is
   added once to a keep list at `022CBB64`.
2. The weather slot is `00265920()` minus one; a slot at or past the table's count picks nothing.
3. A new ambience becomes `022CBA7C`. While `022CBB2D` is set it starts at once through `00363840`. Otherwise a
   playing ambience fades out over 15 frames first (`002DF190(current, 0xF)`), and with none playing `003636A0`
   starts the new one.
4. With no ambience for the slot, the current one fades out over 180 frames (`002DF190(current, 0xB4)`).

### Unbinding

`00363750` releases every listed id through `002DF050`, except an id from 1,000 to 1,999 that is in the keep list
(`00363774`-`003637E4`). It copies the three selections and the keep list to `022CBB38` and releases the handle
(`002DEB40`).

## Layouts

```struct Spp1Header base=file size=0x20
+0x00  char[4]  magic       "SPP1"
+0x04  u32      count       ids in the list
+0x08  u32      bankLength  bytes of SeSep records to open
+0x0C  u32      bankOffset  the records' offset when the pack gives no bank
+0x10  u16      hasMapNo    1 when +0x12 is a map number
+0x12  u16      mapNo       the zone's map number, or 0xFFFF
+0x14  u32      zero14      0
+0x18  u16      padAt       the id list's end rounded up to 16
+0x1A  u16      weatherAt   the weather table's offset, or 0
+0x1C  u32      zero1C      0
```

```struct Spp1Id base=record size=0x4
+0x00  u32  soundId  a six-digit bank id
```

```struct Spp1Weather base=file+weatherAt size=0x10
+0x00  u16     count  entries
+0x02  i16[7]  entry  a list index per weather slot; -1 for none
```

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
