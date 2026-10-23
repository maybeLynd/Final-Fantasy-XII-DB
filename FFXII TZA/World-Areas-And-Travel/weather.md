---
title: "Weather: the three weather slots of an area, the change roll on entering, the setweatherslot verb, the MWeather table, what the slot does to the sky, the map and combat, and the environment variant it selects"
kind: "system"
category: "World, areas and travel"
addresses: "0x0026D910, 0x0025ACA0, 0x0025ABA0, 0x002658B0, 0x002620E0, 0x00265920, 0x003565C0, 0x003777C0, 0x002E3D40, 0x0040AAD0, 0x0026E8D0, 0x00264F10"
---

## What the player sees

Some areas are always clear, some are always raining, and some change: the Giza Plains flip between
dry and rains, the Ozmone Plain between clear, rain and heavy rain, the Paramina Rift between calm and
snowstorm. The weather is decided at the moment you enter the area and never changes while you stay
there. Leaving and coming back rolls again. The weather you left an area in is kept in the save, and
story events can force one.

The weather is more than the sky. Strong wind, rain, snow and sand each change the damage of some
elements, which is why Fire is weaker in the rain and Wind is stronger in a storm, and the map itself
changes with the weather: puddles, snow cover and dust appear or vanish, the light and fog change, and
some map models exist in only one weather.

## How it works

### An area has three weather slots

The durable state is one byte in the save payload, `+0x1060`: the committed slot, 0 to 2. Every
runtime query returns it as 1 to 3: `0x00265920` returns `payload[0x1060] + 1`, unless the debug
override is positive, in which case it returns the override instead. The byte next to it, `+0x1061`,
is the restore flag that makes the next apply keep the committed slot (see the apply below).

The debug override is the dword at `+0xAAC` of the debug singleton `0x001D50D0()`, read by `0x0017D490`.
Its two readers are `0x0017D490` and the overlay `0x001CD0E0`, which prints it with the format
`%s%s %d %s, Weather Slot:%d (Triangle/Cross to toggle)` at `0x008FFC80`. No instruction in the image
stores to `[reg + 0xAAC]` (instruction search over the whole program: the two reads only), so the
shipped build never sets it.

### The probabilities the zone script authors

`0x002658B0(slot)` returns the retention probability of a slot:

1. The slot is clamped to 0 to 2 after subtracting one (`0x002658B8`-`0x002658C8`).
2. The zone's script container must be loaded: bit 0 of `0x02098E20` set, the pointer `0x02098E10` non-null
   and the container's first word above 6 (every shipped script has version 11).
3. The dword at container `+0x64` is resolved through `0x0020E600` and the signed byte at
   `section + 1 + slot` is returned. The section is a count byte, always 3 in the shipped scripts, then
   one byte per slot: the high-level `option weatherProbability = {a, b, c}`.
4. When the container is not loaded the answer is 33 for every slot (`0x00265910`).

### The roll when a zone starts

`0x002620E0(managerRecord)` runs once per zone start, from the field runtime pass `0x0025D9E0`. It
returns at once unless the manager index at `+0x28` is 0 (the zone's own manager), and it skips its
body when bit 2 of the byte at `+0x10` is already set; it sets that bit itself at the end. The body:

1. `0x00259B30()` and `0x003E8980(0)`.
2. `0x0025ACA0()`, the roll, which tail-calls the apply.
3. `0x0026FAD0(0, slot, 0)` and `0x0026FAD0(0x1F, slot, 0)`: the field's effect rows for channels 0 and
   `0x1F` are instantiated for the slot (see the map section).
4. `0x00379860(slot)`, `0x00379290()`, `0x003DE920(0, 1)`, `0x00363B40()`.
5. Bit 2 of `+0x10` is set.
6. `0x003601C0(0xB)` and `0x003601C0(0xC)` run on every pass, latched or not; they clear bits 11 and
   12 of the flag word the world tick page names.

The slot passed in steps 3 and 4 is read fresh each time: the override when positive, else
`payload[0x1060] + 1` (`0x0026210E`-`0x00262187`).

`0x0025ACA0` decides whether the current slot `s` is kept:

```c
p = 0x002658B0(s);
if (p == 0)                       keep = false;      // 0x0025ACD4
else if (p >= 100)                keep = true;       // 0x0025ACD8 cmp edi, 0x64
else {
    u = MT19937_NextU32();                           // 0x00379CD0 -> 0x00863BF0, 0x0025ACDD
    r = (uint64(u) * 100) >> 32;                     // 0 to 99, 0x0025ACE4-0x0025ACE8
    keep = (r < p);                                  // 0x0025ACEC
}
next = keep ? s : 0x0025ABA0(s);
0x0026D910(next);                                      // tail jump at 0x0025AD06
```

The generator is the gameplay Mersenne Twister (random number generators page), so a weather roll
moves every later combat roll on that stream. The scaling is a multiply-high, not a modulo.

`0x0025ABA0(s)` picks the slot to move to. Only a non-zero probability makes a slot eligible; the values
are not weighted:

| from | order tried | draws the generator |
|---|---|---|
| 1 | 2, then 3, then stay at 1 | no |
| 3 | 2, then 1, then stay at 3 | no |
| 2 | `r < 50`: 3, then 1, then stay at 2; `r >= 50`: 1, then 3, then stay at 2 | yes, once, before any probability is read (`0x0025ABB8`) |

Three consequences follow. With `{0, 0, 0}` nothing is eligible and the weather never changes. From
slot 1 or 3 the choice is deterministic and slot 2 wins whenever it is eligible. The draw count per
roll is 0, 1 or 2 depending on the branch, and a reimplementation must draw the same number of times.

### Applying a slot

`0x0026D910(requested)` is the only apply. Its callers are the roll (`0x0025AD06`), the verb
`setweatherslot` (`0x0035660E`) and the boot initialiser `0x00266D10`, which calls it twice with slot 1
(`0x00266E74`, `0x00266E7B`). In order:

1. When the override is positive the request is replaced by it (`0x0026D921`, `0x0026D92A`).
2. `req = clamp(requested - 1, 0, 2)` (`0x0026D936`-`0x0026D943`): an out-of-range request saturates and
   nothing reports it.
3. `0x02099DBC` is zeroed (`0x0026D946`).
4. When `payload[0x1061]` is 0 the request is committed: `payload[0x1060] = req` (`0x0026D95E`).
   Otherwise the request is dropped and the committed slot is kept.
5. `0x00180620(payload[0x1060])` selects the shadow parameter set of the committed slot (the lighting
   pages own it).
6. The area's `map_ref.bin` row is read for the field `0x003148F0()` and the four globals of the next
   section are published, when the table is bound.
7. `payload[0x1061]` is cleared (`0x0026DA92`) on every path, including the bail-out when the table is
   not bound.
8. The tail jump `0x002E3D40(0, 0, 0, 0)` (`0x0026DAAD`) refreshes the sky.

Two slots can be in play inside one call. The gameplay wind class of step 6 is extracted with the
requested slot `req + 1` (`0x0026DA2C`-`0x0026DA31`), while the model selection of step 5, the two table
lookups and the sky refresh use the committed slot re-read from the payload. They differ only when
the restore flag dropped the request: after a scripted `setweatherslot` arms the flag, the next zone
entry whose roll lands elsewhere publishes one slot's combat wind under another slot's sky.

### The environment variant in map_ref.bin

`map_ref.bin` is bound at `0x02099D88`; `0x02099D90` is the address of its `+0x14` table, which the load completion
`0x002678A0` sets, so it also serves as the loaded test (both tested at
`0x0026D98F`, `0x0026D9CC` and by `0x00264F10`). The field's row is at `header[+4] + field * 8`; its first
word is the MWeather selector (`0x00264F10` returns it) and its `+2` is a block index. The block is at
`header[+8] + block * 16`, and lane `committed + 1` of the block, 4 bytes, is the variant for the
slot. Lane 0 is never read because the slot index is biased by one.

| global | value | written at | reader |
|---|---|---|---|
| `0x02099DA8` | `u32 table10[lane[0]]`, the combat environment class 0 to 4; 0 when `lane[0]` is not below the table's count dword | `0x0026DA26` | `0x00263E10` (thunk `0x00321490`) |
| `0x02099DAC` | the wind class: 0 when the MWeather preset is 0, 1 for presets 1 to 3, 2 for presets 4 and up | `0x0026DA3C`, `0x0026DA4E` | `0x00263E20` (thunk `0x003214A0`) |
| `0x02099DB0` | `lane[2]` | `0x0026DA5B` | none (the store is the global's only reference) |
| `0x02099DBC` | `u8 table18[lane[0]]`, 0 or 1; 0 when out of range | `0x0026D946`, `0x0026DA7D` | `0x00264D50`; also written by `0x0026AB40` as `(arg != 0)` |

The two lookup tables are the count-prefixed arrays at `header[+0x10]` and `header[+0x18]`; the
bound is a signed compare against each count dword, so a patched table moves it. The lane byte `+0`
also drives the target-local terrain class `0x00263DD0`, which reads `[0x02099D90] + 4 + group * 4` with
the group word `+0x8A` of the unit's field record.

### The MWeather table

The resource `MWeather` is bound by `0x00378540` (kind 9, id `0x27`) and its completion `0x00378F70`
stores the image at `0x02ADD0B0`. The image is `GRMI01` plus a `u16` selector count at `+6` (776 in the
shipped file) and packed bits from `+8`: nine bits per (selector, slot) pair. `0x003777C0(selector,
slot, bitOffset, width)` extracts a field:

```c
if (record == 0 || selector >= u16(record[+6])) return 0;    // 0x003777D3; no test on the slot
p = 9 * (3 * selector + slot) + bitOffset + width - 10;      // the -10 is -9 for the 1..3 slot and -1 for the walk
v = 0;
for (i = 0; i < width; i++) {                                // most significant bit first
    v = (v << 1) | ((record[8 + (p >> 3)] >> (p & 7)) & 1);
    p -= 1;
}
return v;
```

| wrapper | bits | width | field |
|---|---|---|---|
| `0x00377850` | 0 to 2 | 3 | wind preset, 0 to 7 |
| `0x003777A0` | 3 to 6 | 4 | sun azimuth sector, 16 sectors |
| `0x003777B0` | 7 to 8 | 2 | sun elevation class |

The file is sized for 776 by 3 zero-based entries (2,627 bytes needed, 2,628 shipped), which is
the reading the `-10` produces.

### The sky

`0x002E3D40(mode, preset, azimuth, elevation)` feeds the sky. With `mode` 0 it computes the three values
itself from the current field (`0x003148F0`), its selector (`0x00264F10`) and the committed slot
(`0x00265920`) through the three wrappers; with a non-zero mode it passes its arguments through. Either
way it tail-calls `0x0040AAD0(preset, azimuth, elevation)`:

1. The preset and elevation bytes are stored at `0x02CA4391` and `0x02CA4392`, and `0x0040B3B0(preset)`
   copies row `preset - 1` of the 32-byte table at `0x01EFFA30` to `0x02CA4380`-`0x02CA439C` (preset 0
   copies nothing).
2. The sun direction starts as the unit X axis and is rotated about X by `elev + (r1 - 0.15)` and
   about Y by `(r2 - 0.15) - azimuth * 0.3926991`, where `elev` is 0 for class 0, +0.5235988 (30
   degrees) for class 1 and -0.5235988 for class 2, each sector is 22.5 degrees, and `r1`, `r2` are
   two draws of `0x003D8E50(0.3)` from the presentation generator (`0x0046D160`, `0x0046D200`).
3. `0x0040B430` normalises the vector into `0x02CA43A0` and publishes its tangent with the almost-up
   reference `{0, 1, 1e-5}` into `0x02CA43B0`.

The six wind presets (`0x01EFFA30`, floats then a mode dword):

| preset | +0 | +4 | +8 | +0xC | +0x10 | +0x14 | mode |
|---|---|---|---|---|---|---|---|
| 1 | 0.002 | 0.005 | 0.004 | 0.15 | 0.2 | 1.0 | 1 |
| 2 | 0.005 | 0.015 | 0.002 | 0.05 | 0.3 | 2.0 | 1 |
| 3 | 0.015 | 0.015 | 0.002 | 0.15 | 0.22 | 1.5 | 1 |
| 4 | 0.025 | 0.042 | 0.002 | 0.15 | 0.22 | 2.0 | 1 |
| 5 | 0.095 | 0.092 | 0.002 | 0.25 | 0.12 | 2.0 | 2 |
| 6 | 0.0999 | 0.0999 | 0.05 | 0.3 | 0.9 | 6.0 | 2 |

Presets 7 cannot occur in the shipped data; the table has six rows and the qwords after row 6 are
code pointers.

### What combat reads

Three readers take the published classes into combat:

- The combat stage `0x0038B220` multiplies the pending damage factor `0x02AEE054` by 0.5 or 1.2 when a
  bit of the action row's byte `+0x13` matches the environment class (`0x00263E10`), the target's
  terrain class (`0x003210E0`) or the wind class 2 (`0x00263E20`); the weather and terrain element
  scaling page gives the rule table.
- `0x003895D0` scales `0x02AEDFE0` by 0.8 and `0x00389610` by 0.5 when the wind class is 2 and bit 2 of
  the action's `+0x1A` is clear.
- The AI selector `0x00301AD0` compares the environment class with an operand for equality
  (`0x00303059`-`0x00303063`).

`0x02099DBC` is read by `0x002E9D90` at four sites. Class 4, the value 246 of the 279 shipped lanes
select, matches no arm of `0x0038B220` and so scales nothing.

### What the slot does to the map

The roll path, and only the roll path, rebinds the map to the slot through step 4 of `0x002620E0`;
the verb path ends at the sky refresh. `0x00379290` sets `0x02ADD0E9` to 1 and calls
`0x0026E8D0(0x00265920())` when the area runtime `0x02ADD090` exists, else clears it and runs the preset
rebuild `0x00379630`. `0x0026E8D0(slot)`:

- stores the slot in `0x0209A6E8` and sets the dirty flag `0x0209A708`;
- recomputes the lighting constants `0x0209A2D0` to `0x0209A370` through `0x003ED0B0`, `0x003ED020`,
  `0x003ECFD0`, `0x003ED140` and `0x003B6BA0`;
- `0x003ED7B0(slot - 1)` copies the slot's 0x180-byte environment record of `[0x02EBB7F0]` (`+0x10`,
  `+0x14`, `+0x1C`) to `0x02EBB7F8`, `0x02EBB7FC` and `0x02EBB804`, which `0x003ECCA0` reads each frame.

The preset rebuild `0x00379630`, for an area without a light set, makes the map's lights from those
constants:

1. it frees the three light handles at `0x02ADD120` to `0x02ADD128` and the handle `0x02ADD11C`
   (`0x003ABCA0`) and applies the slot with `0x0026E8D0`;
2. for each of the first `0x0209A2D0` records at `0x0209A2E0` (at most three, 0x30 bytes apart) it files a
   light request of type 1 (first dword `0x1002001`, the record's `+0x20` vector at request `+0x10`
   and its `+0x00` vector at `+0x30`) through `0x003AB960` and keeps the handle at `0x02ADD120` onwards;
3. `0x00379760` files a type-6 request (`0x1042006`) whose colour is `0x0209A370` to `0x0209A378` times the
   three floats at `0x02EBF460`, the `+0x40` of light group 0 (`0x0037AD10`), with `0x0209A37C` as the
   fourth value, and keeps it at `0x02ADD11C`.

`0x0037ACA0(group)`, run from the refresh `0x003DE920`, clears the group's byte `+0x4C`; for group 0
while `0x02EBF420` is empty it tail-jumps to `0x003774C0`, which frees the same four handles.

`0x0209A6E8` is read by the draw-list build `0x002F5550` (a model is drawn only when bit `23 + slot` of
its flag word is set, `0x002F5616`), by the texture page rebuild `0x002F7380` (`0x002F738E`), which
`0x0026E290` runs once while the dirty flag is set, and by the five lighting passes above. `0x00379860`
stores `slot - 1` at `0x02EBF408` when `0x02ADD090` exists, and `0x0037AD40` uses it to pick the slot's
effect preset rows (`+4 + slot * 8` and the three at `+6 + slot * 8`) of each 0x50-byte preset bank.

`0x0026FAD0(channel, slot, manager)` instantiates effect rows through `0x0026F470`: a row of the field's
effect table (`0xA0` bytes, type 3 or others at `+0`) is created only when its byte `+7 + slot` is
non-zero, so each row carries three per-slot enable bytes at `+8`, `+9` and `+0xA`.

### The verbs

| id | name | handler | what it does |
|---|---|---|---|
| 0x21A | `setweatherslot(n)` | `0x003565C0` | when the running manager (`0x002640C0()`) has `+0x28` = 0, byte `+0x12` non-zero and the actor's word matches `[manager] + 0x50`: clamps `n` to 1 to 3, calls `0x0026D910(n)` and then `0x0026D8F0()`, which sets `payload[0x1061]` to 1 so the next zone entry keeps this slot |
| 0x40C | `getweatherslot()` | `0x00356250` | returns `0x00265920()` |
| 0x481 | `setmapwind(elevation, azimuth, preset)` | `0x0034B6C0` | `0x002E3D40(1, preset, azimuth, elevation)`: the sky from the operands, the table bypassed |
| 0x482 | `defaultmapwind()` | `0x0034BD10` | `0x002E3D40(0, 0, 0, 0)`: the sky from the table for the committed slot |
| 0x3DD | `changeenvsoundweather(n)` | `0x0034D900` | `0x00363A20(n)`, the environment sound |
| 0x2024 | `debug_setweather` | `0x0050C7F0` | pops one operand and returns |
| 0x209F | `debug_setlockweatherslot(n)` | `0x00510720` | pops one operand and runs a guard check; writes nothing |

The verb's guard means a script running on an actor other than the zone's own calls
`setweatherslot` and nothing happens, without any report.

### Boot and the first apply

`0x0022A0B0`, the first boot frame, runs `0x00266D10`, which calls `0x0026D910(1)` twice (`0x00266E74`,
`0x00266E7B`). When the restore flag is armed, the first call publishes the saved slot and consumes the
flag and the second commits slot 1; otherwise both commit slot 1. `0x0026E1D0` and `0x0026E960` reset
the map-side globals, and `0x002628B0` (`0x00262B53`) sets `0x0209A6FC` to 1 at the zone's start.

## Layouts

`MapRefHeader` (`0x30` bytes, offsets from the start of the mapref):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[4]` | magic | "MRF" and the version byte 2 |
| `+0x04` | `i32` | rowsOff | image-relative offset of the field rows, 8 bytes each (`0x0026D910`, `0x00264F10`) |
| `+0x08` | `i32` | blocksOff | offset of the 16-byte weather blocks (`0x0026D910`) |
| `+0x0C` | `u8[4]` | unused | zero in the shipped file; read and written by no function: the image pointer `0x02099D88` is loaded by `0x00264ED0`, `0x00264F10`, `0x00264F40`, `0x00264F90`, `0x00264FD0`, `0x002678A0`, `0x00268750`, `0x0026D910` and `0x0026DB30`, and no instruction of the nine reads or writes it; nothing fixes its width |
| `+0x10` | `i32` | table10Off count dword then u32[count]: the environment class per environment index (0x0026DA10-0x0026DA26) |  |
| `+0x14` | `i32` | table14Off offset of a count dword then u32[count], the terrain class per field group: the load completion 0x002678A0 adds it to the base (0x002678A7) and keeps the sum at 0x02099D90, which 0x00263DD0 indexes by the unit's group word without a bound check (0x00263E00) |  |
| `+0x18` | `i32` | table18Off count dword then u8[count]: the terrain boolean per environment index (0x0026DA66-0x0026DA7D) |  |
| `+0x1C` | `u8[20] unused2` | zero in the shipped file; read and written by no function: no instruction of the nine functions that load the image pointer 0x02099D88 (0x00264ED0, 0x00264F10, 0x00264F40, 0x00264F90, 0x00264FD0, 0x002678A0, 0x00268750, 0x0026D910, 0x0026DB30) reads or writes +0x1C to +0x2F; nothing fixes its width |  |

`MapRefFieldRow` (`0x8` bytes, offsets from the start of the row):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | selector | the MWeather selector, 1 to 775 in the shipped file (`0x00264F10`) |
| `+0x02` | `i16` | block | index of the 16-byte weather block, 0 to 92 (`0x0026D9BB`) |
| `+0x04` | `u16` | area | the area index (`0x00264EF9`; the map pack page) |
| `+0x06` | `u16` | group | the field group (`0x00264FB9`) |

`MapRefWeatherBlock` (`0x10` bytes, offsets from the start of the block):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[4]` | lane0 | never read by the weather functions (the slot index is biased by one) |
| `+0x04` | `u8[4]` | slot1 | lane for weather slot 1: +0 environment index, +1 not read here, +2 published to `0x02099DB0`, +3 not read here |
| `+0x08` | `u8[4]` | slot2 | lane for weather slot 2, same layout |
| `+0x0C` | `u8[4]` | slot3 | lane for weather slot 3, same layout |

`MWeatherImage` (`0x8` bytes, offsets from the start of the mweather):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[6]` | magic | "GRMI01" |
| `+0x06` | `u16` | count | selector count, 776 shipped; `0x003777C0` refuses a selector at or above it |

The bits follow from `+8`: entry `3 * selector + slot - 1` occupies 9 bits, low bit first; bits 0 to 2
the wind preset, 3 to 6 the azimuth sector, 7 to 8 the elevation class.

`WindPreset` (`0x20` bytes, offsets from the start of the 0x01EFFA30):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | a | copied to `0x02CA4388` by `0x0040B3B0` |
| `+0x04` | `f32` | b | copied to `0x02CA4380` |
| `+0x08` | `f32` | c | copied to `0x02CA4384` |
| `+0x0C` | `f32` | d | copied to `0x02CA4398` |
| `+0x10` | `f32` | e | copied to `0x02CA439C` |
| `+0x14` | `f32` | f | copied to `0x02CA438C` |
| `+0x18` | `u32` | mode | copied to `0x02CA4394` |
| `+0x1C` | `u8[4]` | pad | read by neither `0x0040B3B0` nor `0x0040ABF0`, the two functions that address the table; nothing fixes its width |

## Shipped data

`map_ref.bin` (`ps2data/image/ff12/<lang>/common/`, the `in` and `ch` copies byte-identical, 12,288
bytes) decoded with the header offsets above:

| quantity | value |
|---|---|
| field rows | 1,315; 531 distinct selectors, 1 to 775; block indices 0 to 92 |
| weather blocks | 93, so 279 lanes |
| table at `+0x10` | 16 entries: 4, 4, 4, 0, 0, 1, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0 |
| table at `+0x18` | 16 entries: 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0 |
| lane environment index | 0 on 163 lanes, 1 on 64, 2 on 19, 3 on 7, 4 on 4, 5 on 1, 6 on 2, 7 on 2, 8 on 16, 9 on 1 |
| `0x02099DA8` reachable | 4 on 246 lanes, 3 on 16, 0 on 12, 2 on 4, 1 on 1 |
| `0x02099DBC` reachable | 1 on 12 lanes, 0 on 267 |
| lane byte `+1` | 0 on 183 lanes, 1 on 74, 2 on 22; bytes `+2` and `+3` are 0 on all 279 |

`gramap_weatherinfo.bin` (same folders, 2,628 bytes, `in` and `ch` identical) has 776 selectors.
Over its 2,328 entries the wind preset is 0 on 1,180, 1 on 550, 2 on 420, 4 on 153, 5 on 24 and 6
on 1, so the strong-wind class 2 covers 178 entries; the elevation class is 0 on 1,865, 1 on 214 and
2 on 249; sector 0 holds 1,603 of the azimuths and sector 8 (180 degrees) 217.

The zone scripts (`ps2data/plan_master/us/plan_map/<area>/<zone>/global/<zone>.ebp`, 769 files,
the script section at `+0x80`, its `+0x64` section a count of 3 then three bytes) author 17
distinct probability triples:

| triple | zones | what it means |
|---|---|---|
| 100, 0, 0 | 430 | slot 1 is kept; the roll draws nothing |
| 0, 100, 0 | 118 | slot 1 moves to slot 2 without a draw, then slot 2 is kept |
| 0, 30, 70 | 73 | slot 1 moves to 2; from 2 a 30 % keep, else 3; from 3 a 70 % keep, else 2 |
| 100, 100, 100 | 43 | every slot is kept: the weather is whatever was last forced or saved |
| 0, 0, 100 | 35 | slots 1 and 2 move to 3 |
| 0, 60, 30 | 24 | from 2 a 60 % keep, else 3; from 3 a 30 % keep, else 2 |
| 0, 50, 50 | 10 | from 2 and 3, a coin toss between keeping and the other |
| 30, 50, 0 or 30, 50, 20 | 9 each | the only triples where slot 1 can be kept by a draw |
| 80, 10, 5 | 5 | slot 1 kept 80 %, else 2; 2 kept 10 %, else the draw between 3 and 1 |
| 1, 1, 1 | 4 | all three eligible, each kept 1 % |
| seven others | 1 to 4 | 0, 70, 30 (4); 0, 40, 60; 0, 20, 80; 90, 10, 0; 30, 10, 40; 30, 10, 10 |

296 zones give slot 1 a probability below 100, so about two in five areas can be in a weather other
than their first slot.

## Operations

Entering an area with the triple 0, 30, 70 while the saved slot is 2:

1. `0x002620E0` passes its gates and calls `0x0025ACA0`.
2. `0x002658B0(2)` returns 30; a draw gives `r`; the slot is kept when `r < 30`.
3. Otherwise `0x0025ABA0(2)` draws again: `r < 50` tries 3 (eligible, 70) and returns 3; `r >= 50`
   tries 1 (0, not eligible) then 3 and returns 3.
4. `0x0026D910(3)` commits slot 3, publishes the lane-3 variant and the wind class of selector's entry
   3, and refreshes the sky from the same entry.
5. `0x002620E0` instantiates the effect rows enabled for slot 3, binds the slot's models, textures and
   lighting through `0x00379290`, and sets its latch bit.

A story script forcing the weather:

1. `setweatherslot(1)` on the zone's own actor applies slot 1 and arms the restore flag.
2. The sky and the combat classes change at once; the map models and effects do not, because the
   verb path never reaches `0x00379290`.
3. On the next zone entry the roll's result is dropped, slot 1 stays committed, the flag is cleared,
   and the map is bound to slot 1.

## State

| address | contents | written by |
|---|---|---|
| payload `+0x1060` | committed slot 0 to 2 | `0x0026D910` (`0x0026D95E`) |
| payload `+0x1061` | restore flag | `0x0026D8F0` sets; `0x0026D910` clears (`0x0026DA92`) |
| `0x02099D88`, `0x02099D90` | the `map_ref.bin` image and the address of its `+0x14` table | the map_ref loader `0x00268750` and its completion `0x002678A0` |
| `0x02ADD0B0` | the MWeather image | `0x00378F70`, `0x00378540` (zeroed) |
| `0x02099DA8`, `0x02099DAC`, `0x02099DB0`, `0x02099DBC` | the published variant | `0x0026D910`; `0x0026AB40` for the last |
| `0x0209A6E8`, `0x0209A708` | the map's slot and dirty flag | `0x0026E8D0`; `0x0026E290` clears the flag |
| `0x02EBF408` | the effect preset slot | `0x00379860` |
| `0x02CA4380`-`0x02CA439C`, `0x02CA43A0`, `0x02CA43B0` | wind preset row, sun direction, tangent | `0x0040B3B0`, `0x0040B430` |
| debug `+0xAAC` | slot override | no writer in the image |

Nothing on this path allocates, and no lock or thread check appears in any body named here. The
in-image routes to `0x0026D910` are the boot setup, the field runtime pass and the script verb.

## Modding notes

- The three slots of an area are authored twice: the probabilities in the zone script's
  `weatherProbability` option, and the look in `map_ref.bin` (lane per slot) and
  `gramap_weatherinfo.bin` (9 bits per selector and slot). Changing one without the other gives a
  weather that never rolls or a roll that never shows.
- A probability of 0 does not force a change; it makes the slot ineligible when coming from another
  slot and sends the roll to the alternates when it is current. `{0, 0, 0}` freezes the weather.
- Slot requests saturate silently: `setweatherslot(0)` and `setweatherslot(1)` both select slot 1,
  `setweatherslot(9)` slot 3.
- The strong-wind combat class is any wind preset of 4 or more; editing a preset across that line
  changes damage, not only the sky.
- The combat class comes from the requested slot and the sky from the committed one, so a lane edit
  that changes only one of them shows up as mismatched combat and sky after a forced weather.
- `0x02099DB0` (lane byte `+2`) has no reader and is 0 in every shipped lane.

## Related

- [Weather and terrain element scaling](../Damage-And-Battle-Formulas/elements.md)
- [Random number generators: the gameplay Mersenne Twister, the shared gameplay LCG, the graphics-noise Mersenne Twister, the C runtime rand, the presentation bit-feedback generator, the counter hash and the PPFX xorshift, with their constants, seeds and states](../Random-Numbers/random-number-generators.md)
- [Zone changes: mapjump and the other jump verbs, the loading flags, the moment the new zone is ready and what names a map](zone-changes-and-mapjump.md)
- [Doors, gates and map changes: the override table the setmapid verbs write, what its floor, wall and mj bits block, the show and hide model masks and when a new map clears them](doors-gates-and-map-changes.md)
- [The map ctrl pack](mpk-map-pack.md)
- [Script verb dispatch and parameter encoding](../Scripts-And-Script-Commands/verb-dispatch.md)
- [The world tick and the field frame](../Engine-Core/frame-update-order.md)
- [Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps](../Saving-Loading-And-Settings/save-file-format.md)
