[Home](../../README.md) / [World, areas and travel](README.md) / Weather

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Weather: the three weather slots of an area, the change roll on entering, the setweatherslot verb, the MWeather table, what the slot does to the sky, the map and combat, and the environment variant it selects | system | World, areas and travel | Chests, traps and weather | Every area has three authored weather slots; entering a map rolls whether the current slot is kept, using the probabilities the zone script authors, after the zone's setup script has had the chance to choose the slot itself; the result is kept in the save. Applying a slot publishes the area's environment variant from map_ref.bin (the combat environment class and the terrain boolean), the 9-bit MWeather entry that sets the map wind's preset, azimuth and elevation (the model sway, not the sky) and the strong-wind combat class, and the per-slot map models, textures and effects. | 0x0026D910, 0x0025ACA0, 0x0025ABA0, 0x002658B0, 0x002620E0, 0x00265920, 0x003565C0, 0x003777C0, 0x002E3D40, 0x0040AAD0, 0x0026E8D0, 0x00264F10 |

## What the player sees

Some areas are always clear, some are always raining, and some change: the Ozmone Plain between sunshine,
a sky with no drawn weather and heavy rain with strong wind, the Paramina Rift between sunshine and
snowstorm. The Giza Plains' Dry and Rains are
not weather: they are two separate sets of maps, and the exit you take into the plains picks the set
from the story and the play clock (see [the Giza Plains seasons](#the-giza-plains-seasons)).

The weather is decided each time you arrive on a map, before you can move, and it never changes while you
stay there; some cutscenes and one boss ending change the map wind, which sways hair, cloth and hanging
gear, for the rest of the visit. The sky stays as the weather slot drew it.

Arriving on another map decides again, but not always by chance: 430 maps always use their first
weather, maps whose script picks the weather choose again only when you arrive from certain maps and
otherwise keep the weather you came with, and the other maps roll starting from the weather you came
with. The game remembers one weather, the last map's; it is kept in the save, and loading a save
normally decides again starting from it.

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
`%s%s %d %s, Weather Slot:%d (Triangle/Cross to toggle)` at `0x008FFC80`. The singleton's constructor
`0x001CCB20` zeroes it with the qword store at `+0xAA8` (`0x001CCBA3`). No instruction in the image stores to
`[reg + 0xAAC]`: the two reads are its only references through that offset.

### The probabilities the zone script authors

`0x002658B0(slot)` returns the retention probability of a slot:

1. The slot is clamped to 0 to 2 after subtracting one (`0x002658B8`-`0x002658C8`).
2. The zone's script container must be loaded: bit `0x1` of `0x02098E20` set, the pointer `0x02098E10` non-null
   and the container's first word above 6 (10,036 of the 10,045 shipped scripts have version 11; the nine
   language copies of the developer event `evt_t0020` have version 7).
3. The dword at container `+0x64` is resolved through `0x0020E600` and the signed byte at
   `section + 1 + slot` is returned. The section is a count byte, always 3 in the shipped scripts, then
   one byte per slot: the high-level `option weatherProbability = {a, b, c}`.
4. The section is the container plus the low 32 bits of the resolved value, sign-extended
   (`0x002658F8`-`0x002658FA`). The count byte is never read, so the clamp of step 1 (`s = slot - 1`, 0 when
   negative, 2 when above 2: `jns`, `cmovg`, `0x002658B8`-`0x002658C8`) is the only bound on the read
   `byte [section + 1 + s]` (`0x00265900`).
5. When the container is not loaded, or its `+0x64` dword is 0 so that `0x0020E600` gives null (`0x002658F6`), the
   answer is 33 for every slot (`0x00265910`).

### The roll when a zone starts

`0x002620E0(managerRecord)` runs once per zone start, from the field runtime pass `0x0025D9E0`. It
returns at once unless the manager index at `+0x28` is 0 (the zone's own manager), and it skips its
body when bit `0x4` of the byte at `+0x10` is already set; it sets that bit itself at the end
(`0x002621A4`).

The manager bind `0x0026C8C0`, run on every zone load when the zone's script arrives
(`0x003304A0` → `0x0032F850`, `0x0032F966`), clears it again (`0x0026CD3F`), so the body runs on every map
entry, including a return to the area the game keeps in memory. Before it, the start pass runs the
zone's setup actor (`0x0025DB31`-`0x0025DB74`), which may already have chosen the slot. The body:

1. `0x00259B30()` and `0x003E8980(0)`.
2. `0x0025ACA0()`, the roll, which tail-calls the apply.
3. `0x0026FAD0(0, slot, 0)` and `0x0026FAD0(0x1F, slot, 0)`: the field's effect rows for channels 0 and
   `0x1F` are instantiated for the slot (see the map section).
4. `0x00379860(slot)`, `0x00379290()`, `0x003DE920(0, 1)`, `0x00363B40()`.
5. Bit `0x4` of `+0x10` is set.
6. `0x003601C0(0xB)` and `0x003601C0(0xC)` run on every pass, latched or not (`0x002621AD`, and the tail jump at
   `0x002621BC`); they clear bits `0x800` and `0x1000` of the flag word the world tick page names.

The slot passed in steps 3 and 4 is read fresh each time: the override when positive, else
`payload[0x1060] + 1` (`0x0026210E`-`0x00262187`).

`0x0025ACA0` decides whether the current slot `s` is kept:

```c
s = (0x0017D490() > 0) ? 0x0017D490()                   // the debug override, 0x0025ACAA-0x0025ACB8
                     : payload[0x1060] + 1;          // signed byte of 0x002EF2B0(), 0x0025ACBC-0x0025ACC8
p = 0x002658B0(s);
if (p == 0)                       keep = false;      // 0x0025ACD4
else if (p >= 100)                keep = true;       // 0x0025ACD8 cmp edi, 0x64
else {
    u = MT19937_NextU32();                           // 0x00379CD0 -> 0x00863BF0, 0x0025ACDD
    r = (uint64(u) * 100) >> 32;                     // 0 to 99, 0x0025ACE4-0x0025ACE8
    keep = (r < uint64(int64(p)));                   // 0x0025ACEC jb: unsigned, so a negative p keeps
}
next = keep ? s : 0x0025ABA0(s);
0x0026D910(next);                                      // tail jump at 0x0025AD06
```

The generator is the gameplay Mersenne Twister (random number generators page), so a weather roll
moves every later combat roll on that stream. The scaling is a multiply-high, not a modulo.

`0x0025ABA0(s)` picks the slot to move to. Only a probability above 0 makes a slot eligible (a signed test, so a
negative one does not: `0x0025ABDB`, `0x0025ABED`, `0x0025AC37`, `0x0025AC4C`, `0x0025AC68`, `0x0025AC8D`); the values
are not weighted:

| from | order tried | draws the generator |
|---|---|---|
| 1 | 2, then 3, then stay at 1 | no |
| 3 | 2, then 1, then stay at 3 | no |
| 2, or any value other than 1 and 3 (only the debug override can give one, `0x0025ABAA`-`0x0025ABB6`) | `r < 50`: 3, then 1, then stay at 2; `r >= 50`: 1, then 3, then stay at 2 | yes, once, before any probability is read (`0x0025ABB8`) |

Three consequences follow. With `{0, 0, 0}` nothing is eligible and the roll never changes the weather. From
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
   section are published, when the table is bound. While `0x02099D88` or `0x02099D90` is null, or the row or lane
   address is null, it goes to step 7 (`0x0026D9C6`-`0x0026DA0E`): `0x02099DA8`, `0x02099DAC` and `0x02099DB0` keep their
   values, and `0x02099DBC` keeps the 0 of step 3.
7. `payload[0x1061]` is cleared (`0x0026DA92`) on every path, including the bail-out when the table is
   not bound.
8. The tail jump `0x002E3D40(0, 0, 0, 0)` (`0x0026DAAD`) refreshes the map wind ([below](#the-map-wind)).

Two slots can be in play inside one call. The gameplay wind class of step 6 is extracted with the
requested slot `req + 1` (`0x0026DA2C`-`0x0026DA31`), while the model selection of step 5, the two table
lookups and the map wind refresh use the committed slot re-read from the payload. They differ only when
the restore flag dropped the request: after the setup actor's `setweatherslot` arms the flag, the roll
of the same zone start, when it lands elsewhere, publishes one slot's combat wind under another slot's
sky.

Shipped data reaches this: 41 zone scripts author `100, 0, 0` and call `setweatherslot`, and 40 of them can set
slot 2 or 3. The roll then asks for slot 1 (`0x0025ABA0`), the request is dropped, slot 2 or 3 stays with its sky,
and the wind class is read from slot 1's entry.

### The environment variant in map_ref.bin

The map_ref loader `0x00268750` files two reads of resource kind 9: file 4, `map_ref.bin`, into a block
tagged `MapRef` with the completion `0x002678A0` (`0x00268803`); then file 2, `in/common/test_area_ref.bin` (the
`ch` copy for Korean and the two Chinese languages; 642 bytes, the two identical), into a block from `0x00267930`
with no completion (`0x00268838`). That block's pointer goes to `0x02099D98` (`0x00268829`, cleared at `0x00268772`),
and no instruction reads `0x02099D98` by its address.

`test_area_ref.bin` is 321 `u16` values, one per area index 0 to 320: value n is the first field whose
`map_ref.bin` row has area n. The fields of each area are consecutive, so value n + 1 minus 1 is area n's last
field, and area 320 ends at field 1,314. An area holds 1 to 28 fields.

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
| `0x02099DB0` | `lane[2]` | `0x0026DA5B` | no reader (the store is the global's only reference) |
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
| `0x003777A0` | 3 to 6 | 4 | wind azimuth sector, 16 sectors |
| `0x003777B0` | 7 to 8 | 2 | wind elevation class |

The file is sized for 776 by 3 zero-based entries (2,627 bytes needed, 2,628 shipped), which is
the reading the `-10` produces.

### The map wind

`0x002E3D40(mode, preset, azimuth, elevation)` sets the map wind. It drives the sway of hair, cloth and hanging
gear ([Model oscillators](../Graphics/model-oscillators-and-pose-sequencer.md)) and does not
reach the sky, which the weather slot chooses ([What the sky is](#what-the-sky-is)). With `mode` 0 it computes
the three values
itself from the current field (`0x003148F0`), its selector (`0x00264F10`) and the committed slot
(`0x00265920`) through the three wrappers; with a non-zero mode it passes its arguments through. Either
way it tail-calls `0x0040AAD0(preset, azimuth, elevation)`:

1. The azimuth and elevation bytes are stored at `0x02CA4391` and `0x02CA4392` (`0x0040AAFA`, `0x0040AB01`), and
   `0x0040B3B0(preset)` stores the preset byte at `0x02CA4390` (`0x0040B3B0`) and copies row `preset - 1` of the
   32-byte table at `0x01EFFA30` to `0x02CA4380`-`0x02CA439C` (preset 0 copies nothing).
2. The wind direction starts as the unit Z axis `{0, 0, 1}`, the 16 bytes at `0x009155F0` (`0x0040AB0C`), and is
   rotated about X by `elev + (r1 - 0.15)` and about Y by `(r2 - 0.15) - azimuth * 0.3926991`, where `elev` is 0
   for class 0, +0.5235988 (30 degrees) for class 1 and -0.5235988 for class 2 or 3 (`0x0040AB18`-`0x0040AB32`), and
   each sector is 22.5 degrees.
3. `r1` and `r2` are two draws of `0x003D8E50(0.3)` from the presentation generator (`0x0040AB43`, `0x0040AB7F`).
   `0x0046D160` builds the X rotation (`0x0040AB5E`) and `0x0046D200` the Y rotation (`0x0040ABA8`), and `0x00202B90`
   applies each to the vector in place (`0x0040AB72`, `0x0040ABBC`).
4. `0x0040B430` normalises the vector into `0x02CA43A0` and publishes its tangent with the almost-up
   reference `{0, 1, 1e-5}` into `0x02CA43B0`.

`0x0040B430`, called from `0x0040AAD0` (`0x0040ABC6`) and `0x0040DB70` (`0x0040DB97`), builds the tangent from the reference
and the direction with `0x00202E10` (`0x0040B522`). It scales the result by 1 over its length, `v * (1.0 / len)` with
`len = sqrt(x * x + y * y + z * z)`, or by 0 when the length is below the constant at `0x00908E10`
(`0x0040B542`-`0x0040B57C`), and stores three floats (`0x0040B581`-`0x0040B592`). The model simulation stage
`0x0040FF30` reads the tangent as one 16-byte value (`0x0041008A`), copies it to `0x022D91E0` (`0x004100D1`) and takes its
third float (`0x004100E0`):

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA43A4` | `f32` | 0 (zero-filled tail of `.data`) | the normalised direction's second float | `0x0040B430` (`0x0040B510`) | `0x00202E10`, through the address of `0x02CA43A0` that `0x0040B430` passes (`0x0040B4C4`, `0x0040B522`) |
| `0x02CA43A8` | `f32` | 0 (zero-filled tail of `.data`) | the normalised direction's third float | `0x0040B430` (`0x0040B519`) | `0x00202E10`, as for `0x02CA43A4` |
| `0x02CA43B4` | `f32` | 0 (zero-filled tail of `.data`) | the tangent's second float | `0x0040B430` (`0x0040B58A`) | `0x0040FF30`, within the 16-byte read of `0x02CA43B0` (`0x0041008A`) |
| `0x02CA43B8` | `f32` | 0 (zero-filled tail of `.data`) | the tangent's third float | `0x0040B430` (`0x0040B592`) | `0x0040FF30`, within the 16-byte read of `0x02CA43B0` (`0x0041008A`) |

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

### What the sky is

The sky is part of each map's remastered scene. Each piece is an ordinary mesh instance `nodename<N>`
with the mesh `nodename<N>Shape`, attached to YM00 instance N
([Map art](map-art.md#matching-models-to-instances)). A piece belongs to the sky when its instance's
flag word `+0x0C` has `0x10000000`. This is the set the script verb `setskyonly` keeps: while
`0x0209A704` is set, the draw-list build `0x002F5550` skips every instance without that bit
(`0x002F5E03`-`0x002F5E10`).

- In each of the 195 map packs with sky instances, they are instances 0 to n-1. None of these packs has
  an instance with `0x400`.
- 11 of the 999 sky instances have no mesh instance `nodename<N>` in their scene, so no mesh instance is matched
  to them and no render object is made for them ([Map art](map-art.md#matching-models-to-instances)): instance 1 of
  `frs0111`, `naf0102` and `var0102` to `var0104`, instances 0 and 1 of `naf0101`, and instance 2 of `rbn0101`,
  `rbn0104`, `rbn0201` and `rbn0301`. The other 988 are the pieces below.
- Every piece has one material, a `PhyreDefaultLitShader` variant. Its `TextureSampler` texture is the
  picture: sky domes, cloud layers, stars, moons and distant mountains.
- 971 of the 988 pieces use a material group named with `sky`. The other 17 are the distant mountains
  of `sav01` and `sav02`.
- A piece is drawn only in the weather slots whose bits it carries: `0x1000000`, `0x2000000` and
  `0x4000000` for slots 1 to 3, tested against `0x0209A6E8` (`0x002F5DF9`). So a weather change swaps sky
  pieces in and out.
  - 488 pieces are in all three slots, 177 only in slot 1, 39 only in slot 2 and 93 only in slot 3.
  - 81 are in slots 1 and 2, and 110 in slots 2 and 3. So every piece carries at least one slot bit.
- The draw pass `0x002F4520` draws at once every instance up to the last one with `0x10000000` or `0x400`
  (`0x002F4804`), then posts the map's opaque command ([Map art](map-art.md#drawing-an-instance)). So
  the sky is drawn before the rest of the map.
- The same bit sets the object's flag `+0xC1` (`0x002F4D3C`, `0x001E69A0`). `0x001E2AF0` then draws the piece
  with a pass chosen by its mode `+0x78` (`0x001E30BD`):
  - mode 0: `DefaultMapRenderPassNztNzwAtNoBlending`;
  - mode 1: the linear blend (source alpha over inverse source alpha);
  - mode 2: the additive blend;
  - mode 3: the subtractive blend.
- All four passes test depth with ALWAYS and write no depth, so the map drawn afterwards covers the sky.
  The mode starts from the flag word's `(flag >> 1) & 7` (`0x002F4A72`-`0x002F4A9C`): it is 0 on 402 sky
  instances, 1 on 403 and 2 on 194.
- A mode from 4 to 7 matches none of the four passes: `0x001E3107`-`0x001E310B` jump past the four stores, so the
  pass pointer `+0x80` keeps the value it already holds. No shipped sky instance has a mode above 2.
- Neither the direction `0x02CA43A0` nor the tangent `0x02CA43B0` reaches the sky. Their only readers are
  `0x0040B430` (`0x0040B4C4`) and the model simulation stage `0x0040FF30` (`0x00410083`, `0x0041008A`), so
  `setmapwind` and the wind presets do not change how the sky is drawn.
- `sky_spec` is the specular companion of `nal0102`'s `tex/sky.dds`, and both of its asset lists name
  it. `0x001A7F10` pairs it with that texture, and `0x001E6110` binds it as `SpecularMap` of the sky piece
  (`m_extraFlag` `0xC`). `sky_n` is bound as `NormalMap` by `0x001E55C0` in the same way.
- `Sky_mirror.dds` of `rbn5101` is the `TextureSampler` of the upper-floor material
  `_collada_rbn5101_Upper_floor__phong49`. Two floor instances draw it. The map's sky piece binds
  `alc0200_sky.dds`.

### What combat reads

Three readers take the published classes into combat:

- The combat stage `0x0038B220` multiplies the pending damage factor `0x02AEE054` by 0.5 or 1.2 when a
  bit of the action row's byte `+0x13` matches the environment class (`0x00263E10`), the target's
  terrain class (`0x003210E0`) or the wind class 2 (`0x00263E20`); the weather and terrain element
  scaling page gives the rule table.
- `0x003895D0` scales `0x02AEDFE0` by 0.8 and `0x00389610` by 0.5 when the wind class is 2 and bit `0x4` of
  the wielder's formula context `+0x1A` (augment 2, Accuracy Boost) is clear (`0x003895D4`;
  [Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md)).
- The AI selector `0x00301AD0` compares the environment class with an operand for equality
  (`0x00303059`-`0x00303063`).

`0x02099DBC` is read by `0x002E9D90` at four sites. Class 4, the value 246 of the 279 shipped lanes
select, matches no arm of `0x0038B220` and so scales nothing.

### What the slot does to the map

Only the roll path rebinds the map, through step 4 of `0x002620E0`; the verb path ends at the map wind
refresh. Because the verb works only before `0x002620E0` in the same start pass, the rebind always uses
the slot the setup script chose. `0x00379290` sets `0x02ADD0E9` to 1 and calls
`0x0026E8D0(0x00265920())` when the area runtime `0x02ADD090` exists, else clears it and runs the preset
rebuild `0x00379630`. `0x0026E8D0(slot)`:

- stores the slot in `0x0209A6E8` and sets the dirty flag `0x0209A708`;
- recomputes the lighting constants `0x0209A2D0` to `0x0209A370` through `0x003ED0B0`, `0x003ED020` and
  `0x003ECFD0`, from the environment record of slot `[0x0209A6E8]` - 1 in `[0x02EBB7F0]`: `0x0209A2D0` takes
  `0x003ED0B0()`, the record's `+0x04` dword or -1 while `[0x02EBB7F0]` is 0 (`0x0026E8F1`-`0x0026E8F6`);
- runs `0x003ED020(i, 0x0209A2F0 + 0x30 × i, 0x0209A300 + 0x30 × i)` for lights 0 to 2 (`0x0026E910`-`0x0026E927`) and
  `0x003ECFD0(0x0209A370)`, which copies the record's `+0xF0`-`+0xFC` there, or nothing while `[0x02EBB7F0]` is 0
  (`0x0026E930`);
- `0x003B6BA0(0x003ED140())` stores the record's `+0x08` scale at `0x01EFE314`, or 1.0 while `[0x02EBB7F0]` is 0
  (`0x0026E935`-`0x0026E93A`);
- `0x003ED7B0(slot - 1)`, the tail jump at `0x0026E951`, copies the slot's 0x180-byte environment record of
  `[0x02EBB7F0]` (`+0x10`, `+0x14`, `+0x1C`) to `0x02EBB7F8`, `0x02EBB7FC` and `0x02EBB804`, which `0x003ECCA0` reads each
  frame; it copies nothing while `[0x02EBB7F0]` is 0 (`0x003ED7BA`).

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
`0x0026E290` runs once while the dirty flag is set, and by the five lighting passes above. `0x00379860` stores `slot - 1`
at `0x02EBF408` when `0x02ADD090` exists and the slot is 1 to 3 (`0x00379F50`-`0x00379F5B`; any other slot leaves the value as
it was), and `0x0037AD40` uses it to pick the slot's effect preset rows (`+4 + slot * 8` and the three at
`+6 + slot * 8`) of each 0x50-byte preset bank.

`0x0026FAD0(channel, slot, manager)` instantiates effect rows through `0x0026F470`: a row of the field's
effect table (`0xA0` bytes, type 3 or others at `+0`) is created only when its byte `+7 + slot` is
non-zero, so each row carries three per-slot enable bytes at `+8`, `+9` and `+0xA`.

[`weather-slot-effects.tsv`](weather-slot-effects.tsv) follows those rows for every map and slot of
[`weather-maps.tsv`](weather-maps.tsv). For each it gives:

- the banks the field loads (`fields_own` and `fields_block` of
  [effect files](../Graphics/effect-files-efx-efb.md));
- the rows of channels 0 and 31 that the slot makes, and how many of them some other slot does not make;
- the element types their records play, as `0x002FBA60` names them;
- the pictures those elements draw, and the screen surfaces they sample;
- the slot's chance from `weather_probability`. A slot whose chance is 0 is never selected by the roll; it
  occurs only when the zone's setup script sets it with `setweatherslot`, which happens for 87 slots in 84 maps
  (The verbs).

The chain from a row to its pictures is on
[effect element runtime](../Graphics/effect-element-runtime.md).
[`weather-class-effects.tsv`](weather-class-effects.tsv) counts the slot-limited rows per combat class and wind class,
over all slots, over the slots the roll can move to (chance above 0), and over the slots of chance 0 that the
zone's setup script sets with `setweatherslot`, which the roll then leaves in place:

- Combat class 0 (fire x0.5, lightning x1.2): 82 of its 90 slots play `NhElementType_VRAIN2`, 67 of the 75 the roll
  can move to and all 4 of chance 0 that a setup script sets. It is drawn as untextured lines, 48, 100, 200 or 300
  drops an element. The other 8 slots belong to fields that load no bank. 11 slots (10 the roll can move to) also
  draw four thin white jagged branching vertical lines on black.
- Combat class 1 (earth x1.2): all 11 play `TsElementType_VMODEL02` with a grey cloudy blotch (8 the roll can move
  to; no setup script sets one of chance 0).
- Combat class 2 (ice x1.2): all 20 play `TsElementType_SPRITE`: 9 the roll can move to, and 9 of chance 0 that
  setup scripts set. Those 18 draw scattered white and grey specks and a grey-white cloudy blotch.
- Combat class 3 (water x1.2): 253 of 352 slots play `TsElementType_VMODEL03` and `TsElementType_VMODEL04` with
  orange, blue and black marbled swirls, 187 of the 199 the roll can move to; no setup script sets one of chance
  0. 88 slots make no zone-start element, 10 of them with a chance above 0.
- Combat class 4 (no rule): 266 of 1,651 slots have a slot-limited element, 197 of them `TsElementType_VLENSFLARE`.
  Among the 666 the roll can move to, it is 177, with 142; among the 74 of chance 0 that setup scripts set, 34, all
  `TsElementType_VLENSFLARE`.
- Wind class 2 (fire x1.2, water x0.5, wind x1.2): 131 of 203 slots have a slot-limited element,
  `TsElementType_SPRITE` in 77 and `NhElementType_VRAIN2` in 65. Among the 149 the roll can move to, it is 99, with
  58 and 58; all 13 of chance 0 that setup scripts set have one, `TsElementType_SPRITE` in 11 and
  `NhElementType_VRAIN2` in 4.
- Wind classes 0 and 1 (no rule): 2 of 504 and 508 of 1,417 slots; 2 of 176 and 349 of 632 the roll can move to;
  0 of 13 and 34 of 61 of chance 0 that setup scripts set.

None of the 410 shipped banks names 90 of the 708 fields in `fields_own` or `fields_block`, so those fields' slots
make no zone-start element.

The models a slot draws are a separate test (`0x002F5616`, above), read on every map pack:
[weather-slot-models.tsv](weather-slot-models.tsv) gives each pack's models that are drawn in some slots only, one
row per slot pattern and scene group, with the zones that load the pack, the record count and the textures.

- 461 of the 550 packs hold model records (764,018); the other 89 have no model record. 761,479 records are drawn in
  all three slots.
- 501 sky pieces (flag `0x10000000`) in 126 packs are drawn in some slots only, so those maps change their sky with
  the slot.
- 2,038 other models in 50 packs are as well, in Archades, the Cerobi Steppe, Mt Bur-Omisace, the Nabreus Deadlands,
  the Phon Coast, the Ridorana Cataract and the Tchita Uplands. 671 of the 2,038 records have no mesh instance of
  their record number in the remaster scene.
- Most of their scene groups come in pairs, a set for slot 1 and a set for slots 2 and 3: shadows (`kage_slot1` and
  `kage_slot2`, `tree_shadow` and `tree_shadow2`, `shadow` and `shadow2`), plants (`plants_s` and `plants_s2`), the
  sea (`sea1` and `sea2`) and stairs (`kaidan` and `kaidan2`).
- In Archades (`alc5001`) `shadow1` is drawn in slot 1 and its `shadow2` in slot 2 only. `hamon` is drawn in slot 3
  (136 records; 1 more, in `srb0104`, in slot 1) and `mizuzoko` (21) in slots 1 and 2.
- Some groups named for the sky (`sky`, `sky2`, `cloud`, `kumo`) carry no sky flag and are counted with these.
- `pbc0101` (772 records) and `ozm0101` (1,976), read first, have 5 slot-limited records each, all sky pieces.

### The verbs

| id | name | handler | what it does |
|---|---|---|---|
| 0x21A | `setweatherslot(n)` | `0x003565C0` | when the running manager (`0x002640C0()`) has `+0x28` = 0, byte `+0x12` non-zero and the actor's word matches `[manager] + 0x50`: clamps `n` to 1 to 3, calls `0x0026D910(n)` and then `0x0026D8F0()`, which sets `payload[0x1061]` to 1 so the roll that follows in the same start pass keeps it. Byte `+0x12` is set by the bind (`0x0026CD28`, when header word `+0x50` names a setup actor) and cleared at `0x0025DB79`, just before `0x002620E0`, so the verb acts only while the setup actor runs its start functions |
| 0x40C | `getweatherslot()` | `0x00356250` | returns `0x00265920()` |
| 0x481 | `setmapwind(preset, azimuth, elevation)` | `0x0034B6C0` | `0x002E3D40(1, preset, azimuth, elevation)`: the map wind from the operands, the table bypassed |
| 0x482 | `defaultmapwind()` | `0x0034BD10` | `0x002E3D40(0, 0, 0, 0)`: the map wind from the table for the committed slot |
| 0x3DD | `changeenvsoundweather(n)` | `0x0034D900` | `0x00363A20(n)`, the environment sound |
| 0x2024 | `debug_setweather` | `0x0050C7F0` | pops one operand and returns |
| 0x209F | `debug_setlockweatherslot(n)` | `0x00510720` | pops one operand (`0x00267E10`) and jumps to the `ret` stub `0x0016D6A0` (`0x00510732`); writes nothing |

The verb's guard means a call from any actor other than the zone's setup actor, or any call after the
zone has started, does nothing, without any report. In the shipped `us` scripts all 1,744 calls are in
actor `setup` of 122 zone scripts and none of the 345 event scripts calls it, so the weather slot never
changes during a visit. Cutscenes change the map wind instead: 152 event scripts call `setmapwind` 168
times, and zone `wdl_b01` calls it after its boss; that sets the wind preset and direction through
`0x002E3D40` mode 1 and leaves the slot and the combat classes alone.

366 of the 1,744 calls set a slot whose chance is 0 in their zone, in 85 zone scripts. 135 of them cannot run:
127 sit under two tests of one value that exclude each other, and 8 under a test of `nowmap()` against another
map's id. The other 231, in 84 scripts, set 87 slots of chance 0 in 84 maps (for example Fading Vale, field 463,
`pbc_a01`, chances 30, 50, 0: `setweatherslot(3)` at offset `0x036C0` when the story counter is outside `0x079E`
to `0x07B8`, the party comes from one of four maps and a draw of 1 to 100 is above 70).

Such a slot stays for the visit: the verb arms the restore flag, so the roll that follows is dropped.

Only the first `setweatherslot` of a zone start takes effect. `0x0026D910` stores a request only while the restore
flag is 0 (`0x0026D951`-`0x0026D95E`), applies the slot the payload holds (`0x0026D96F`) and clears the flag
(`0x0026DA92`); the verb's `0x0026D8F0` then sets it again (`0x0026D8F9`). A later call in the same start pass therefore
keeps the first call's slot, and the roll after it does the same. The later call still reads the wind class for
the slot it asked for itself (`0x0026DA2C`-`0x0026DA31`, `0x00377850`) and publishes that class at `0x02099DAC`
(`0x0026DA3C`, `0x0026DA4E`).

[`weather-forced-slots.tsv`](weather-forced-slots.tsv) reads the 366 calls with their tests in words. Of the 231
that can run, 169 decide the slot, 59 decide it only when no earlier call ran on that visit, and 3 never decide.
[`weather-calls.tsv`](weather-calls.tsv) gives all 1,744 calls with the tests they sit under: 1,737 in the
setup actor's `map` function and 7 in its `event` function.

The setup actor's functions run in the order the script image files them (`0x00266C50`), all inside the start pass:
a function's return picks the next filed one in the same opcode (`0x003DB2A0`, `0x003DB6E0`), and manager `+0x12`
is cleared only when none is left (`0x0025DB79`). `map` is filed before `event` in all 32 of the 122 calling
scripts that file both. `bul_a02` is the one script with calls in both: its `map` calls on every path, so the
two calls of its `event` (:59, :62) never decide.

In `srb_a04` the call at :1373 stands under a local flag that `map` clears at its start (:1193) and sets only on
the lines after its calls, so an earlier call has always run and it never decides.

In the `tests` column a draw keeps its number, so two tests of `draw 1` read one draw. The carried weather slot
is the global word `mp_last_weather`. The map-exit functions store `getweatherslot()` in it before the map change
(2,806 stores in 575 scripts), and a setup script stores its call's argument in it on the line after the call
(1,593 stores), so a carried slot of -1 is the argument of a call that leaves slot 1.

### The Giza Plains seasons

The Giza Plains' Dry and Rains are two sets of fields, not weather slots: fields 236 to 249 are the Dry
and author `100, 0, 0`, and fields 253 to 270 are the Rains and author `30, 50, 20`, with `sav_e01`
and `sav_f01` to `sav_f03` choosing the slot in `setup`. 26 zone scripts compute `mp_sav季節` (payload
`+0x988`) in their `mapjump` functions and jump to the Dry field on 1 and the Rains field on 0 (for
example `rbn_a18` to 236 or 253, `ozm_a01` to 247 or 264). The rule:

- Before the first Rains visit is recorded (`+0x984` = 0): a story counter below 1,475 (`0x5C3`) gives
  the Dry; 1,620 (`0x654`) and above gives the Rains and records `getplayhour()` (verb `0x2ED`) mod 3
  at `+0x986`/`+0x985`; in between gives the Rains.
- Recording it: entering `sav_d01`, `sav_f01`, `sav_f02` or `sav_f03` with the counter at 1,620 or
  above sets `+0x984` to 1; `sav_d01` resets it to 0 below that.
- After that the season is `(getplayloophour() - offset) % 3`: 0 gives the Rains and anything else the
  Dry, so the Rains come back for one play-time hour in three. `getplayloophour` (`0x0034A0E0` →
  `0x002542B0`) is the hours of the frame counter at `[0x020927C0] + 0x47E8`, modulo 9,999.
- The exits set map-jump group flag `0x107` for the Rains or `0x108` for the Dry and release the
  other. The scripts test the story counter directly, and `mapjumpgroupflagrom.bin` plays no part,
  because these ids lack bit `0x4000`.

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
| `+0x10` | `i32` | table10Off | count dword then u32[count]: the environment class per environment index (`0x0026DA10`-`0x0026DA26`) |
| `+0x14` | `i32` | table14Off | offset of a count dword then u32[count], the terrain class per field group: the load completion `0x002678A0` adds it to the base (`0x002678A7`) and keeps the sum at `0x02099D90`, which `0x00263DD0` indexes by the unit's group word without a bound check (`0x00263E00`) |
| `+0x18` | `i32` | table18Off | count dword then u8[count]: the terrain boolean per environment index (`0x0026DA66`-`0x0026DA7D`) |
| `+0x1C` | `u8[20]` | unused2 | zero in the shipped file; read and written by no function: no instruction of the nine functions that load the image pointer `0x02099D88` (`0x00264ED0`, `0x00264F10`, `0x00264F40`, `0x00264F90`, `0x00264FD0`, `0x002678A0`, `0x00268750`, `0x0026D910`, `0x0026DB30`) reads or writes `+0x1C` to `+0x2F`; nothing fixes its width |

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

The bits follow from `+8`: entry `3 * selector + slot - 1` occupies 9 bits, low bit first; bits `0x7`
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

The three files row by row, decoded with the layouts above:

| table | rows | what each row holds |
|---|---:|---|
| [`weather-fields.tsv`](weather-fields.tsv) | 1,315 | one field of `map_ref.bin` (row n is field n): its selector, block, area and group, the group's terrain class, and for each weather slot the lane's four bytes, its environment index, the combat class and terrain flag the two lookup tables give it (0 out of range, as the code reads), and the MWeather wind preset, wind class, azimuth sector and elevation class of that selector and slot |
| [`weather-maps.tsv`](weather-maps.tsv) | 708 | one map with a zone script, by field id: its map and region name, the script, its three chances (`weatherProbability`, the same in all ten language copies), what the roll on entering does from each slot (`0x0025ACA0`, `0x0025ABA0`), each slot's environment index, combat class and wind class from the field's row, and what those classes do to magick damage by element in that slot ([Elements](../Damage-And-Battle-Formulas/elements.md#weather-and-terrain-scaling), before the target's terrain class, and not with Weatherproof). The roll columns give the roll alone: a slot the zone's setup actor sets stays, whatever its chance, because the roll after it is dropped (`0x0026D951`) |
| [`weather-mweather-entries.tsv`](weather-mweather-entries.tsv) | 2,328 | every selector 0 to 775 and slot 1 to 3 of `gramap_weatherinfo.bin`: the entry number, its 9 bits, the wind preset, the azimuth sector and the elevation class |
| [`weather-test-area-ref.tsv`](weather-test-area-ref.tsv) | 321 | one value of `test_area_ref.bin`: the area index, its offset, the area's first and last field and its field count |
| [`weather-terrain-groups.tsv`](weather-terrain-groups.tsv) | 32 | the `+0x14` table, the terrain class per field group: 0 for 17 groups, 1 for one, 2 for two, 3 for three and 4 for nine |
| [`weather-sky-instances.tsv`](weather-sky-instances.tsv) | 999 | one sky instance (flag `0x10000000`) of a map pack, over 195 packs: the scene drawn (five packs use another map's scene through `0x01EF9490`), the instance number, flag word and weather slots, the mesh instance and mesh, segments, indices and indexed vertices, `m_extraFlag`, material, effect variant, `TextureSampler` texture and the file it loads; 11 instances have no mesh instance in the scene |
| [`weather-sky-textures.tsv`](weather-sky-textures.tsv) | 1,052 | one texture binding of a material that a sky instance draws or that binds a texture named `sky`: the scene, material, effect variant, parameter, texture, the file it loads, and how many sky and other instances draw the material |
| [`weather-slot-effects.tsv`](weather-slot-effects.tsv) | 2,124 | one map of [`weather-maps.tsv`](weather-maps.tsv) and slot: the slot's chance, its environment index, combat and wind class, the effect banks the field loads, the rows of channels 0 and 31 the slot makes and how many other slots do not make, the element types they play with a count (and, for types without a picture, how they draw), the pictures drawn with a count, and the screen surfaces sampled |
| [`weather-class-effects.tsv`](weather-class-effects.tsv) | 8 | one combat class (0 to 4) or wind class (0 to 2): its combat rule, its slots, how many make a zone-start element and a slot-limited one, and per element type and picture the number of slots whose slot-limited rows play or draw it; then the same four counts (slots, those with a zone-start element, those with a slot-limited one, and the element types of those) for the slots the roll can move to (chance above 0) and for the slots of chance 0 that the zone's setup script sets |
| [`weather-slot-names.tsv`](weather-slot-names.tsv) | 2,124 | one map of [`weather-maps.tsv`](weather-maps.tsv) and slot, named from what the slot draws and what combat reads: `weather` (rain at 48 to 200 drops an element, heavy rain at 300, rain with lightning, sandstorm, snow, snowstorm, Mist, sunlight, each with `strong wind` for wind class 2, or `no drawn weather`: 1,325 slots), `element_rule` (the damage factors of its combat and wind class), the classes, the elements, and the sky textures and map model groups that, among the map's slot-limited pieces, only this slot draws |
| [`weather-calls.tsv`](weather-calls.tsv) | 1,744 | one `setweatherslot` call of a zone script: the script, the listing line, the actor and function, the slot argument and the tests the call sits under, with each draw numbered |
| [`weather-forced-slots.tsv`](weather-forced-slots.tsv) | 366 | one call that sets a slot of chance 0: the field, map, the slot the call leaves (an argument of -1 or 0 gives slot 1) and its name, the three chances, the script, line and function, `takes_effect` (`decides`, `decides unless an earlier call ran` with the lines of the earlier calls that can come first, `never decides` with the reason, or `cannot run`) and the tests in words |
| [`weather-gated-spawns.tsv`](weather-gated-spawns.tsv) | 159 | one row of [`enemy-placement-conditions.tsv`](../Enemy-Spawning/enemy-placement-conditions.tsv) whose test reads `getweatherslot()` (68 placements in 28 maps): the placement, the map, the enemy and its kind, the slots the test allows with their names, and the test in words; 130 rows allow all three slots, because the weather term sits inside a negated pair with a hunt mark's presence |

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
| 30, 50, 0 or 30, 50, 20 | 9 each | slot 1 kept 30 %, else 2; 2 kept 50 % |
| 80, 10, 5 | 5 | slot 1 kept 80 %, else 2; 2 kept 10 %, else the draw between 3 and 1 |
| 1, 1, 1 | 4 | all three eligible, each kept 1 % |
| six others | 1 to 4 | 0, 70, 30 (4); 0, 40, 60; 0, 20, 80; 90, 10, 0; 30, 10, 40; 30, 10, 10 |

A roll that starts in slot 1 can keep it by a draw under seven triples, those whose first chance is 1 to 99:
30, 50, 0; 30, 50, 20; 80, 10, 5; 1, 1, 1; 90, 10, 0; 30, 10, 40 and 30, 10, 10.

296 zones give slot 1 a probability below 100, so the roll can leave slot 1 in them. Of the 473 that give it
100, 40 of the `100, 0, 0` zones can set slot 2 or 3 from their setup script, and the 43 of `100, 100, 100` keep
whatever slot they are entered with (25 of them also set slots from `setup`). The table gives what the roll does;
a slot the setup script sets stays, whatever its triple.

## Operations

Entering an area with the triple 0, 30, 70 while the saved slot is 2:

1. `0x002620E0` passes its gates and calls `0x0025ACA0`.
2. `0x002658B0(2)` returns 30; a draw gives `r`; the slot is kept when `r < 30`.
3. Otherwise `0x0025ABA0(2)` draws again: `r < 50` tries 3 (eligible, 70) and returns 3; `r >= 50`
   tries 1 (0, not eligible) then 3 and returns 3.
4. `0x0026D910(3)` commits slot 3, publishes the lane-3 variant and the wind class of selector's entry
   3, and refreshes the map wind from the same entry.
5. `0x002620E0` instantiates the effect rows enabled for slot 3, binds the slot's models, textures and
   lighting through `0x00379290`, and sets its latch bit.

A zone script choosing the weather:

1. The bind sets manager `+0x12`; the start pass runs `setup`, whose `map()` picks a slot (from
   `lastmap()`, the story counter and the save global `mp_last_weather`, payload `+0x940`) and calls
   `setweatherslot(n)`.
2. `0x0026D910(n)` commits slot n, publishes its combat classes and refreshes the map wind; `0x0026D8F0` arms
   the restore flag.
3. `0x0025DB79` clears `+0x12`, and `0x002620E0` rolls: the result is dropped (`0x0026D951`), slot n stays,
   the flag is cleared (`0x0026DA92`), and effects, models, textures and lighting are bound to slot n, so the flag the
   verb armed is 0 once the zone has started.
4. A later `setweatherslot` in that visit fails the `+0x12` test (`0x003565E2`) and does nothing.

## State

| address | contents | written by |
|---|---|---|
| payload `+0x1060` | committed slot 0 to 2 | `0x0026D910` (`0x0026D95E`) |
| payload `+0x1061` | restore flag | `0x0026D8F0` sets (`0x0026D8F9`); `0x00268320` sets it after a load when `0x0209AC10` is 0 (`0x0026836C`; the load screen sets `0x0209AC10` at `0x00582E98`, so a normal load leaves the flag as loaded, 0 in any save made in the field); `0x0026D910` clears (`0x0026DA92`); the store of 0 at `0x00280213` never runs, because `0x0020E5A0()` returns `0x005C5230()` = 0, not 5 |
| `0x02099D88`, `0x02099D90` | the `map_ref.bin` image and the address of its `+0x14` table | the map_ref loader `0x00268750` and its completion `0x002678A0` |
| `0x02ADD0B0` | the MWeather image | `0x00378F70`, `0x00378540` (zeroed) |
| `0x02099DA8`, `0x02099DAC`, `0x02099DB0`, `0x02099DBC` | the published variant | `0x0026D910`; `0x0026AB40` for the last |
| `0x0209A6E8`, `0x0209A708` | the map's slot and dirty flag | slot: `0x0026E8D0` (`0x0026E8E1`), 1 from `0x0026E640` (`0x0026E653`); flag: set by `0x0026E8D0` (`0x0026E8E7`) and the map bind `0x0026E960` (`0x0026E9B0`), cleared by `0x0026E290` (`0x0026E2C9`) and `0x0026E1D0` (`0x0026E22B`) |
| `0x02EBF408` | the effect preset slot | `0x00379860` through `0x00379F50` (`0x00379F5B`); 0 from `0x00379F70` (`0x0037A0C0`), called by `0x00266D10` (`0x00266E85`) and `0x00379D00` (`0x00379D0D`) |
| `0x02CA4380`-`0x02CA439C`, `0x02CA43A0`, `0x02CA43B0` | wind preset row, wind direction, tangent | `0x0040B3B0`, `0x0040B430` |
| debug `+0xAAC` | slot override | no writer in the image |

The map's lights are three records of `0x30` bytes from `0x0209A2E0`, light i at `0x0209A2E0` + i × `0x30`, after the
count `0x0209A2D0`:

- `+0x00`, the light's direction: each world step `0x0026EB30` turns the vector (0, 0, -1, 1) by the three angles at
  `+0x10`, converted from degrees to radians and wrapped into -π to π, and stores the 16-byte result
  (`0x0026EB79`-`0x0026EC88`); `0x00379630` files it at the light request's `+0x30` (`0x003796F0`).
- `+0x10`, three angles in degrees, read by `0x0026EB30` (`0x0026EBBA`, `0x0026EBF9`, `0x0026EC39`).
- `+0x20`, a vector that `0x00379630` files at the light request's `+0x10` (`0x003796EA`); `0x0026EB30` sets its fourth
  float `+0x2C` to 1.0 each step (`0x0026EC8D`).

`0x003ED020(i, &light[i] + 0x10, &light[i] + 0x20)` fills `+0x10` and `+0x20` with 16 bytes each from the environment
record of slot `[0x0209A6E8]` - 1 in `[0x02EBB7F0]` (`0x180` bytes a record): its `+0x90` + i × `0x20` and `+0xA0` + i ×
`0x20` (`0x003ED054`-`0x003ED0A5`). It does nothing while `[0x02EBB7F0]` is 0. `0x0026E8D0` (`0x0026E919`) and `0x0026E960`
(`0x0026EA79`) call it for lights 0 to 2. The map reset `0x0026E640` zeroes `+0x10` and `+0x20` of each light with 16-byte
stores and sets `0x0209A2D4` to 1.0:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209A2D4` | `f32` | 0 (zero-filled tail) | 1.0 after a map reset | `0x0026E640` (`0x0026E728`) | no instruction at this address |
| `0x0209A2F0` | `f32[4]` | 0 | light 0 `+0x10`: the angles | `0x0026E640`, 0 (`0x0026E6F1`, 16 bytes); `0x003ED020` (`0x003ED05C`-`0x003ED080`) | `0x0026EB30` |
| `0x0209A300` | `f32[4]` | 0 | light 0 `+0x20` | `0x0026E640`, 0 (`0x0026E6F9`, 16 bytes); `0x003ED020` (`0x003ED08B`-`0x003ED0A5`); `0x0026EB30`, 1.0 in `+0x2C` (`0x0026EC8D`) | `0x00379630` (`0x003796EA`) |
| `0x0209A320` | `f32[4]` | 0 | light 1 `+0x10`: the angles | `0x0026E640`, 0 (`0x0026E701`); `0x003ED020` | `0x0026EB30` |
| `0x0209A330` | `f32[4]` | 0 | light 1 `+0x20` | `0x0026E640`, 0 (`0x0026E709`); `0x003ED020`; `0x0026EB30`, 1.0 in `+0x2C` | `0x00379630` |
| `0x0209A350` | `f32[4]` | 0 | light 2 `+0x10`: the angles | `0x0026E640`, 0 (`0x0026E711`); `0x003ED020` | `0x0026EB30` |
| `0x0209A360` | `f32[4]` | 0 | light 2 `+0x20` | `0x0026E640`, 0 (`0x0026E719`); `0x003ED020`; `0x0026EB30`, 1.0 in `+0x2C` | `0x00379630` |

`0x00379630` files light requests for the first `0x0209A2D0` lights only, a signed count raised to 0 when negative and
capped at 3, `n < 0 ? 0 : n > 3 ? 3 : n` (`0x003796A7`-`0x003796C4`); `0x0026EB30` steps all three lights.

Nothing on this path allocates, and no lock or thread check appears in any body named here. The
in-image routes to `0x0026D910` are the boot setup, the field runtime pass and the script verb.

## Modding notes

- The three slots of an area are authored twice: the probabilities in the zone script's
  `weatherProbability` option, and the look in `map_ref.bin` (lane per slot) and
  `gramap_weatherinfo.bin` (9 bits per selector and slot). Changing one without the other gives a
  weather that never rolls or a roll that never shows.
- A probability of 0 does not force a change; it makes the slot ineligible when coming from another
  slot and sends the roll to the alternates when it is current. `{0, 0, 0}` stops the roll. A slot the setup
  script sets stays even at 0, because the roll after it is dropped.
- Slot requests saturate silently: `setweatherslot(0)` and `setweatherslot(1)` both select slot 1,
  `setweatherslot(9)` slot 3.
- The strong-wind combat class is any wind preset of 4 or more; editing a preset across that line
  changes damage, not only the sway of hair, cloth and hanging gear.
- The combat class comes from the requested slot and the sky from the committed one, so a lane edit
  that changes only one of them shows up as mismatched combat and sky after a forced weather.
- `0x02099DB0` (lane byte `+2`) has no reader and is 0 in every shipped lane.
- A sky piece is a YM00 instance with flag `0x10000000` whose scene holds the mesh instance `nodename<N>`. It
  shows only in the weather slots whose bits it carries (`0x1000000`, `0x2000000`, `0x4000000`), and
  `(flag >> 1) & 7` picks its blend, 0 to 3. It is drawn before the map with depth test ALWAYS and no depth write,
  so the map covers it.
- `test_area_ref.bin` restates `map_ref.bin`'s areas: value n is area n's first field. Its block is kept at
  `0x02099D98`, which no instruction reads by its address; keep its values matching `map_ref.bin` when fields are
  added or moved between areas.
- `map_ref.bin`'s readers take the field number as the row (`0x00264F26`, `0x0026D987`) and the row's block word as the
  block (`0x0026D9ED`) without a bound. The shipped rows cover fields 0 to 1,314, past the highest field number 1,311
  ([Zone asset list](zone-asset-list.md)), and every row's block is below the 93 blocks, so a replacement that drops
  rows or blocks makes those reads land past its tables.

## Related

- [Weather and terrain element scaling](../Damage-And-Battle-Formulas/elements.md)
- [Random number generators: the gameplay Mersenne Twister, the shared gameplay LCG, the graphics-noise Mersenne Twister, the C runtime rand, the presentation bit-feedback generator, the emulated VU1 generator, the counter hash and the PPFX xorshift, with their constants, seeds and states](../Random-Numbers/random-number-generators.md)
- [Zone changes: mapjump and the other jump verbs, the loading flags, the moment the new zone is ready and what names a map](zone-changes-and-mapjump.md)
- [Doors, gates and map changes: the override table the setmapid verbs write, what its floor, wall and mj bits block, the show and hide model masks and when a new map clears them](doors-gates-and-map-changes.md)
- [The map ctrl pack](mpk-map-pack.md)
- [Script verb dispatch and parameter encoding](../Scripts-And-Script-Commands/verb-dispatch.md)
- [The world tick and the field frame](../Engine-Core/frame-update-order.md)
- [Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps](../Saving-Loading-And-Settings/save-file-format.md)
- [`map-ref-image-header-accesses.tsv`](map-ref-image-header-accesses.tsv): every access to the
  `map_ref.bin` header (`MapRefHeader`) through the image pointer `[0x02099D88]` (15 rows).
- [`map-ref-field-row-accesses.tsv`](map-ref-field-row-accesses.tsv): every access to its field rows
  (`MapRefFieldRow`), found from the header's `+0x04` (18 rows).
- [`map-ref-weather-block-accesses.tsv`](map-ref-weather-block-accesses.tsv): every access to its weather
  blocks (`MapRefWeatherBlock`), found from `+0x08` (4 rows).
- [`map-ref-weather-lane-accesses.tsv`](map-ref-weather-lane-accesses.tsv): every access to the four lanes
  of a weather block (4 rows).

In the `route` cells of these tables, `MapRefImageHeader` names the `map_ref.bin` header and `MapRefWeatherBlock` a
weather block.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Platform: `0x001CCB20` calls `0x005CC930`; those functions are documented on
  [game application](../Engine-Core/game-application.md).
- Save load settings: `0x0020E5A0` is called by `0x00280140`; `0x00268320` is called by `0x00280140`; `0x002EF2B0` is called by
  `0x00280140`; those functions are documented on
  [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md).
- Story event quest hunt: `0x0026C8C0` calls `0x00377440`; `0x002EF2B0` is called by `0x0032A8A0`, `0x0032A930`, `0x0032A9A0`,
  `0x0032AA00`, `0x0032AA60`, `0x0032AAD0`, `0x0032AB60`, `0x0032ABF0`, `0x0032AC70`, `0x0032ACF0`, `0x0032AD70`, `0x0032ADF0`.
- Story event quest hunt: those functions are documented on [actor managers](../Characters-And-Objects/actor-managers.md),
  [identifier spaces](../Engine-Core/identifier-spaces.md),
  [story flags](../Story-Events-And-Hunts/story-flags.md),
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Story event quest hunt: and on [story flag ids](../Story-Events-And-Hunts/story-flag-ids.md),
  [chocobos and airships](chocobos-and-airships.md), [npc names](../Characters-And-Objects/npc-names.md).
