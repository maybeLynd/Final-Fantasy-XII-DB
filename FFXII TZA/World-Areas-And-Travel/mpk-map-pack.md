---
title: "MPK map pack: the sections of a map file, the two packs a field loads, how the loader splits and binds them, and what each section holds"
kind: "format"
category: "World, areas and travel"
addresses: "0x00331990, 0x00378A60, 0x00378030, 0x0036B980, 0x00378BC0, 0x003775D0, 0x00378120, 0x00378230, 0x002F6AB0, 0x003E8940, 0x003E8230, 0x00363B40, 0x003631B0, 0x00379870, 0x003C63A0, 0x0037AA90"
---

## What the player sees

Walking into a new area loads its map pack: the area's sound bank and positional sounds, its world
data (the models, their placement, the lighting and the weather-dependent look), its navigation
mesh, its lights, the switch-driven objects a script controls, and the picture and coordinates the
minimap uses to show where you are. An area that shares a sound bank with its neighbours loads that
bank once from a second, sound-only pack. A section a pack does not carry simply supplies nothing.

## Where it comes from

Each pack is `ps2data/plan_master/map_ctrl/<area>/<zone>/bin/<zone>.mpk`, 550 files. A zone's own
pack is `<zone>.mpk`; the block pack of an area is the one named `<area>00.mpk`, and all 89 of them
carry only the sound sections (slots 0, 1 and 10) or nothing at all.

The packs are namespace-4 resources. `map_ref.bin` names both packs of a field: the field row's
first word is the field's own pack index (`0x00264F10`), and the first word of the row's 16-byte block
record is the block pack index (`0x00264F40`); the block record's second word plus 500 is the sound
map number stored at `0x02ADD078` (`0x00264FD0`, `0x00378030`). The row and block layouts are on the
weather page, which reads the same two tables.

## Layouts

### The pack

`MpkHeader` (`0xC0` bytes, offsets from the start of the file):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count | 32 in all 550 packs; `0x0036B980` rejects a count above 32 |
| `+0x04` | `u32[32]` | size | section size per slot in slot order; 0 means the slot is absent |
| `+0x84` | `u8[60]` | pad | the header is padded to a multiple of `0x40` |

The header length is `((count + 1) * 4 + 0x3F) & ~0x3F`, 0xC0 for 32 slots. After it, for each slot
whose size is non-zero and in slot order, come a 0x40-byte slot (zero in the file; the loader
overwrites it with an arena block header) and the section's bytes. There are no offsets: a section's
position is the running sum, and `0x0036B980` refuses the pack when the sum does not equal the loaded
block's size (`0x0036BA30`-`0x0036BA45`).

| slot | magic | section | kept by | consumer |
|---|---|---|---|---|
| 0 | `SeSe` | the `SeSep` sound-effect bank | mode 0 (`0x02ADD080`) | `0x003635E0` walks it with `0x002DF070` and frees it |
| 1 | `WD` | a wave bank | neither mode | freed unread (`0x00378BC0`) |
| 4 | u32 1 | the navigation dataset | mode 1 (`0x02ADCFE8`, copied) | `0x00384160` binds it (the navigation mesh page) |
| 8 | `YM00` | world data | mode 1 (`0x02ADCFE0`), mode 0 (`0x02ADCFF0`) | `0x0026E760`, `0x0026E7D0` build the 0x240-byte world object through `0x002F6AB0` |
| 9 | `ACTL` | the actor-control table | both (`0x02ADD0B8`) | `0x003E8940` publishes it at `0x02B5D080` |
| 10 | `SPP1` | the map sound list | mode 0 (`0x02ADD068`) | `0x003635E0` keeps it at `0x022CBAF8` (the map sound list page) |
| 13 | `EFB0` | a map effect bank | neither mode | freed; the loose `PS2Data\efb\<zone>.efb` is loaded instead (`0x00377DC0`) |
| 15 | `MRP` | a menu resource package | both (`0x02ADD058`) | `0x00377B90` returns it to `initgauge` (`0x0034DC70`) |
| 16 | `SP1` | the sound-emitter block | both (`0x02ADD060`) | `0x003635C0` keeps it at `0x022CBAF0` |
| 17 | `LGT2` | the light set | both (`0x02ADD090`) | `0x0037AA90(block, 0)` |
| 24 to 27 | `TIM2` | map pictures, one per sub-location | both (`0x02ADD010` + 8i) | `0x003C63A0` uploads picture 0 |
| 28 to 31 | `NPS2` | each picture's placement | both (`0x02ADD030` + 8i) | `0x00379870` applies placement 0 |

Slots 2, 3, 5 to 7, 11, 12, 14 and 18 to 23 are never read by `0x00378BC0` (slot 12 is freed), and no
shipped pack fills them.

### YM00, the world data

`Ym00Header` (`0x14` bytes, offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[4]` | magic | "YM00" |
| `+0x04` | `u8[4]` | stamp | an export value; read by none of `0x002F6AB0` (which starts at +`0x10`), the world-object builders `0x0026E760` and `0x0026E7D0` that hand it the section, or the pack walker `0x00378BC0`; nothing fixes its width |
| `+0x08` | `u8[8]` | author | an export tag; not read by `0x002F6AB0` |
| `+0x10` | `u32` | count | 17 in all 461 sections; `0x002F6AB0` reads it at [base + `0x10`] |
| `+0x14` | `u32[]` | index | count + 1 entries of {u24 offset in 16-byte units from +`0x10`, u8 tag}; the last is the end sentinel with tag `0xFF` |

Before the walk `0x002F6AB0` sets `+0x120` to 1 and `+0x110` to 0, and clears the first 0x48 bytes of
the two 0x68-byte sub-records at `+0x40` and `+0xA8` with `0x00231F50`, nine qword stores of 0
(`0x002F6AEA`-`0x002F6B14`).

`0x002F6AB0(object, kind)` walks the index: an entry whose offset equals the next entry's is skipped,
otherwise its tag selects an arm (`cmp eax, 0x21`, a 34-case jump table). The arms that store or
parse a chunk:

| tag | what 0x002F6AB0 does with the chunk |
|---|---|
| 0 | `[+0x16C]` = first dword (a count), `[+0x188]` = chunk + 0x10: the 0x40-byte placement rows `0x002F5550` composes |
| 1 | `[+0x170]` = count, `[+0x190]` = chunk + 0x10, `[+0x1C8]` = an allocation of `count * 4` |
| 9 | `0x003ED3F0(chunk)`: the three 0x180-byte environment records at `0x02B5ED94` |
| 11 | `0x0026E8C0` stores it at `0x0209A660`; dword 0 to `0x022D8ED8` unless 0xFFFFFFFF; dword 1 unpacked by `0x00466140` into the colour `0x0209A3A0`-`0x0209A3AC` (scaled by 1/128); dwords 2 and 3 to `0x0209A6EC` and `0x0209A6F0` |
| 12 | `0x00468160(chunk, [+0x150], [+0x1B8])` |
| 14, 26 | `0x003EC910(6, 0x20, 0x00467D00)` then `0x00467D20(buffer, chunk)`; `[+0x150]` = buffer, `0x00467BF0(buffer, 0)` appends it to the buffer list at `0x02EBB6A0`; tag 26 also sets `[+0x230]` = 1 |
| 17, 31 | `0x00232380(object + 0xA8 or + 0x40, chunk)`: a six-tag sub-container into the two 0x68-byte sub-records |
| 22 | `[+0x180]` = chunk |
| 23 | `0x00466E70(chunk)`: the map animation slots at `[0x02EBB6F0]` (below) |
| 24 | `[+0x220]` = count, `[+0x198]` = chunk + 0x10, `[+0x1D0]` = an allocation of `count * 0xE0` |
| 25 | `0x003ED190(chunk)`: field-dependent environment setup |
| 27 | `0x003ED840(chunk)` |
| 28, 29, 32 | `[+0x1A8]`, `[+0x1B0]`, `[+0x1B8]` = chunk |
| 30 | `[+0x174]` = count, `0x001806F0(count)`, `[+0x178]` = chunk + 0x10: the 0x30-byte instance records |
| 33 | `0x002F6740(object, chunk)` |

Every shipped section carries exactly the 17 tags 0, 1, 11, 12, 17, 22 to 33 and the sentinel, so the
skipped tags 2 to 8, 10, 13, 15, 16 and 18 to 21 never occur. After the walk the constructor
allocates `count30 * 0x70` at `[+0x1C0]`, fills each entry from the tag-30 records (colour from the
record's `+0xC` or from the tag-0 row through the `+0x40` sub-record's transform, `0x00231A90`) and
links the records that carry bit 30 of their `+0xC` word to their tag-24 entry (`word +0x14`).

`0x003ED190` (tag 25) also sends a light direction to the shadow object through `0x001F1590`, which
creates the 0xB08-byte shadow object at `0x01F82EA8` on first use (`0x001EF2D0`) and stores the direction
with `0x001F08A0`. The direction is (0.0001, 1, 0) in field `0x11A` (`0x003148F0`); otherwise the
vector at `+0x10` of the tag-11 chunk (`0x0209A660`) when it is non-zero; otherwise the chunk's three
angles at `+0x90` to `+0x98` turned into a direction, or x 0.0001 and y 1.0 when all three are 0.
`0x003ED3F0` (tag 9) also passes a direction to `0x001F1590`, the same (0.0001, 1, 0) in field `0x11A`.

The tag-28 chunk is published when a map binds: `0x003ED870`, called by `0x0026E960`, stores the world
object's `[+0x1A8]` at `0x02B5F1A8` when the chunk's first word is positive, and `0x003ED820` (from
`0x0026E640` and `0x0036F4D0`) clears `0x02B5F1A0`, `0x02B5F1A8` and `0x02B5F1B0`.

### Tag 23, the map animation slots

Tag 23 holds the map's animation clips: moving and turning map parts, colour pulses, texture frames
and the area's ambient colour. `0x00466E70(chunk)` builds one 0x50-byte slot per clip into an array at
`[0x02EBB6F0]` (count `0x02EBB6E0`, chunk `0x02EBB6F8`). The chunk is a count at `+0x10` and an offset
table from `+0x14` in 16-byte units from `+0x10`; slot `i` has a clip when entries `i` and `i + 1`
differ.

`MapAnimClip` (`0x30` bytes, offsets from the start of the clip):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[32] name` | "ambient" makes the slot's +0x34 = 0 |  |
| `+0x20` | `f32` | start | first frame (`0x00466C40`) |
| `+0x24` | `f32` | end | last frame (`0x00466BB0`) |
| `+0x28` | `i16` | targets | target count |
| `+0x2A` | `u16` | group | model group the clip belongs to |
| `+0x2C` | `i16` | mapCount | 0, or the count of 16-byte map entries from +`0x30` that replace +`0x28` |
| `+0x2E` | `u8` | flags | bit 0: `0x02EBB6E4` = this slot |

After the clip header (and its map entries) comes a track list: a count and one offset per track,
again in 16-byte units. A track starts with its own header and then its keys:

`MapAnimTrack` (`0x20` bytes, offsets from the start of the track):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | keyCount |  |
| `+0x04` | `u8` | channel | the target field the track drives (`0x00466420`) |
| `+0x08` | `i16` | targetId | stored at the target's +`0x46` |
| `+0x0A` | `i16` | targetId2 | stored at the target's +`0x44` |
| `+0x0C` | `i32` | target | the target's index in the slot |
| `+0x10` | `f32[4] key0` | time, value, in-slope, out-slope; keyCount keys of 16 bytes from here |  |

`0x00466E70` allocates the slot's track records (0x18 bytes each: key data, time `+0x08`, value
`+0x0C`, key index `+0x10`) and its 0x130-byte targets, and sets bit `channel` of each target's
`+0x40`. It then binds the tracks (`0x004677A0`), resets the slots (`0x00467420`) and runs one update
(`0x004668C0`).

`MapAnimSlot` (`0x50` bytes, offsets from the start of the [0x02EBB6F0]+i*0x50):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | clip |  |
| `+0x08` | `void*` | clipActive | non-null for a live slot; every accessor tests it |
| `+0x10` | `void*` | mapEntries | when clip +`0x2C` is non-zero |
| `+0x18` | `void*` | trackList |  |
| `+0x20` | `void*` | tracks | `0x18` bytes each |
| `+0x28` | `void*` | targets | `0x130` bytes each |
| `+0x30` | `i16` | trackCount |  |
| `+0x32` | `i16` | targetCount |  |
| `+0x34` | `i16` | ambient | 0 for the clip named "ambient", else -1 |
| `+0x38` | `f32` | rate | 1.0 after a reset (`0x00467700` sets it, `0x004735D0` too) |
| `+0x3C` | `f32` | rangeStart | clamped to the clip's start (`0x00467660`) |
| `+0x40` | `f32` | rangeEnd | clamped to the clip's end |
| `+0x44` | `f32` | time |  |
| `+0x48` | `f32` | step | dt * rate, added each frame by `0x004678E0`, zeroed after the update |
| `+0x4C` | `u32` | flags | bit 0 playing, bit 1 loop, bit 2 finished, bit 3 update once, bit 4 relink |

`0x00466E70` gives every slot the loop bit and, when it has a clip, bits 0 and 4. `0x00467420` resets
each live slot: the range becomes the clip's start and end, bit 2 is cleared and bit 3 set, the time
and every track's time become the start, the rate 1.0, and every target gets an identity matrix
(`0x00203170`), colour 1.0 at `+0x50` to `+0x5C`, rotation and translation 0 and scale 1.0.

`0x004677A0` binds each track's value to its target through `0x00466420(target, channel, &value)`;
with map entries, entry `+0x02` names the track, `+0x04` the channel and `+0x06` the target. The
channels are:

| Channel | Target field |
|---|---|
| 0 to 2 | translation `+0xE8`, `+0xF0`, `+0xF8` |
| 3 to 5 | rotation in degrees `+0xD0`, `+0xD8`, `+0xE0` |
| 6 to 8 | scale `+0x100`, `+0x108`, `+0x110` |
| 9 | `+0x90`, the texture frame the draw pass reads |
| 10, 11 | `+0x98`, `+0xA0` |
| 12, 13, 14 | colour red, green, blue `+0xB0`, `+0xB8`, `+0xC0`; 15 sets all three |
| 16 | `+0xA8`, which the draw pass scales by 0.01 |
| 17 | colour alpha `+0xC8` |
| 18 to 20 | rotation in radians `+0x118`, `+0x120`, `+0x128` |

Each world step `0x004668C0` (reached through the thunk at `0x0036F400`) advances every slot with bit 0 whose bit 3 is set or
whose step's absolute value exceeds 0.001 (`|+0x48| > 0.001`, `0x00466969`-`0x0046697B`):

1. bits 2 and 3 are cleared and the time moves by the step;
2. with `lo` = `+0x3C`, `hi` = `+0x40` and `span = hi - lo`, the loop bit and `span >= 1.0` the
   time `t` becomes `t - span` when `t >= hi` and `t + span` when `t < lo` (`0x004669A7`-`0x004669CA`);
   otherwise `t >= hi` stores `hi`, `t < lo` stores `lo`, and either sets bit 2 (finished)
   (`0x004669D1`-`0x004669EA`);
3. unless the clip's group is above 0x100 with its bit in the hidden-model set (`0x0026E5F0`),
   `0x00466240` advances each track and `0x00466550` rebuilds each target;
4. the step is zeroed.

`0x00466240(slot, track)` sets the track's time `t = t + step` for the slot's step, and with
`lo = max(+0x3C, first key time)`, `hi = min(+0x40, last key time)` and `span = hi - lo`
(`0x00466251`-`0x0046629E`) checks only the side it moves toward: for a step above 0, `t >= hi` stores
`t - span` (loop bit and `span >= 1.0`, key index 0) or `hi`; for a step of 0 or less, `t < lo`
stores `t + span` (key index the last) or `lo` (`0x004662A2`-`0x004662F6`).

`0x00466240` then finds the key pair around the time and interpolates with a cubic Hermite curve (each key's value, the first key's out-slope and the second
key's in-slope) into the track's value. The slopes are per unit of time: with u = (t - t0) / (t1 - t0),
the value is h00(u) v0 + h01(u) v1 + (t1 - t0) (h10(u) out0 + h11(u) in1).

`0x00466550(slot, target)` reads the bound channels: translation into `+0x70` to `+0x78`, degrees
turned into radians and wrapped into `+0x60` to `+0x68` (the radian channels overwrite them), scale
into `+0x80` to `+0x88`. It rebuilds the target's matrix at `+0x00` from the three rotations, each
applied only when it is not 0 (`0x00202E90`, `0x00202F00`, `0x00202F70`), and the translation, scales its four rows by `+0x80` to `+0x8C`
(`0x00202FE0`) and, for the `ambient` slot, copies the colour `+0x50` to `+0x5C` to `0x0209A370` to
`0x0209A37C`, the ambient colour of the map's lights.

The slot accessors take a slot number and test it against `0x02EBB6E0` and `+0x08`:

- `0x00466C80(slot)` returns the time `+0x44` (0 for a bad slot) and `0x00466AD0(slot)` the finished bit 2 (1 for a bad
  slot, the test `0x004735E0` of the actor-control table uses);
- `0x00473490(slot)` returns the time less the clip's start (`0x00466C40`), the verb `getbganimeframe` (`0x0AD`,
  `0x0034FEE3`); `0x004734C0(slot)` returns the clip's end (`0x00466BB0`) less its start, `getbganimelastframe` (`0x0AE`,
  `0x00350393`);
- `0x00467730(slot, t)` seeks: it clears bit 2, sets bit 3, stores `t` as the time of the slot and of every track and
  zeroes the step and each track's `+0x10`; the rewind `0x00473500`, called by `bganimeplay` (`0x09D`, `0x003477B0`),
  `bganimeplay_9e` (`0x09E`, `0x00347CD0`) ([verb table](../Scripts-And-Script-Commands/verb-table.md)), `0x003E8440`,
  `0x003E8690` and `0x003E8990`, and `0x00466DD0` use it;
- `0x00466DD0()` sends every playing slot that does not loop and has a non-zero rate to its range end and marks it
  finished; it runs from the script skip's start `0x00360710` and end `0x00360A50`, and from `0x003486A0` and `0x00355300`.

The draw code reaches targets through the tag-30 instances. `0x00466CB0(slot, idB, idA, mask)`
returns the slot's first target when the clip's group is below 0x100 and its bit is in the
instance's group mask, else the target whose `+0x46` (or map entry `+0x00`) equals `idB`, else the
one whose `+0x44` equals `idA`. `0x002F6AB0` and `0x002F5550` call it with the instance record's `+0x02`
and `+0x08` words and its group mask `+0x20`.

When a slot's bit 4 is set, `0x002F5550` clears it and
stores the target in each matching instance's 0x70-byte entry at `+0x50` while the slot plays
(`0x00466B80`, bit 0), or 0 when it does not.

### ACTL, the actor-control table

`ActlHeader` (`0x10` bytes, offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[4]` | magic | "ACTL" |
| `+0x04` | `u16` | version | must be 1: `0x003E8940` clears the pointer otherwise |
| `+0x06` | `u16` | recordSize | `0x16` in all 270 sections; `0x003E8230` and the two walkers advance by it |
| `+0x08` | `u16` | idBound | `0x003E8230` refuses an id at or above it |
| `+0x0A` | `u8[2]` | reserved | 0; read by none of `0x003E8230`, `0x003E7EC0`, `0x003E8D50` and `0x003E8940`; nothing fixes its width |
| `+0x0C` | `u16` | indexOffset | `0x10`: the bucket index {u16 bucketCount; {u16 bound, u16 recordOffset}[bucketCount]} |
| `+0x0E` | `u16` | auxOffset | the aux table `0x003E7EC0` and `0x003E8D50` pass to the record handlers |

`0x003E8230(id)` returns the record of an id:

- bucket = `id / 100`, slot = `id % 100`;
- a miss when the id reaches `idBound`, the bucket reaches `bucketCount` or the slot reaches the
  bucket's bound;
- a hit is `section + recordOffset[bucket] + slot * recordSize`.

`0x003E7EC0` and `0x003E8D50(mode)` walk every bucket's records in the same arithmetic and hand each to
`0x003E8020` or `0x003E8C50` with the aux table and the weather slot (`0x00265920`); `0x003E8D50` skips
records whose byte `+0x15` differs from a non-negative mode.

`0x003E8020` keeps the record's state in its first word: bit 0 processed (set on first touch, when the
low nibbles of bytes `+0x13` and `+0x14` are copied into their high nibbles and the high nibble of
`+0x12` becomes 3), bit 1 the alternator, bits 2 and 3 an override, bit 4 "was active". A first word
of 0xFFFF is a tombstone that every walker skips.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | state | the state bits above |
| `+0x02` | `i16` | animation | map animation slot, -1 for none (`0x004735D0` sets its rate) |
| `+0x08` | `i16` | light | `LGT2` light id, -1 for none; bit 14 routes it through the aux table (`0x003E8190`) |
| `+0x0E` | `i16` | effect | map effect channel, -1 for none |
| `+0x10` | `i16` | sound | map sound emitter below 1000 |
| `+0x12` | `u8` | mode | high nibble 0 runs `0x003E8440`, 1 runs the test `0x003E8350` |
| `+0x13` | `u8` | gate | a non-zero high nibble skips the mode step |
| `+0x14` | `u8` | soundMode | the high nibble feeds `0x00363A90` |
| `+0x15` | `i8` | effectArg | third argument of `0x0026FAD0`, negatives as 0; the walker's mode filter |

On first touch `0x003E8020` runs `0x003E8990`, which clears state bits 3 and 4, rewinds the animation
slot (`0x00473500(slot, -1.0, -1.0)`), sets its rate to 0 (`0x004735D0`) and sets the sound emitter's
flags with `0x00363A90`. A toggle with bit 1 clear runs `0x003E85B0` and sets the bit; with bit 1 set it
runs `0x003E8690` and clears it:

- `0x003E85B0` sets the animation slot's rate to 0, turns the light's loop off and stops its animation
  (`0x0037A310`, `0x0037A130`, or `0x003E8A10` and `0x003E8A40` through the aux table), starts the effect
  channel (`0x0026FAD0`) and clears its flag (`0x002700F0(channel, 0)`), and sets bit 4 of the sound
  emitter's flag byte (`0x00363AD0(id, 1)`);
- `0x003E8690` sets the rate to 1.0, resets, turns on and restarts the light (`0x0037A270`, `0x0037B190`,
  `0x0037A1D0`, `0x0037A310`), sets the channel's flags (`0x002700F0`, `0x00270130`) and starts it, and
  clears the emitter's bit 4.

In mode 1 `0x003E8020` sets state bit 4 when `0x003E8350` finds that `0x004735E0` (the animation slot), `0x0037B030` (the light,
or the callback `0x003E82A0` through the aux table) and `0x00362E30` (the emitter's bit 0) all return 0
and `0x0026FDB0` does not return 2 for the channel.

### SP1, the sound emitters

`Sp1Header` (`0x20` bytes, offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[4]` | magic | "SP1" |
| `+0x04` | `u32` | listOffset | `0x20` in all 456 sections: `0x00363B40` reads the weather-slot list here when the SPP1 list is absent |
| `+0x08` | `u32` | areasOffset | the listener grid `0x00362E50` searches |
| `+0x0C` | `u32` | indexOffset | {u16 bound; u16 recordOffset[]}: the emitter index `0x00362850` passes to `0x003631B0` |
| `+0x10` | `u32` | emittersOffset | a u16 prefix list terminated by bit 15, then the emitter records |
| `+0x14` | `u32` | reserved14 | 0 |
| `+0x18` | `u16` | reserved18 | 0 |
| `+0x1A` | `u16` | reserved1A | 0 |
| `+0x1C` | `u32` | reserved1C | 0 |

`0x003631B0(listener, list, index, current)` walks a list of index entries, resolves each through the
index into a record at `0x022CBAF0 + recordOffset`, dispatches on the record's shape byte `+9`
(`& 0x7F`: 0, 1, 2, other), evaluates the volume through `0x00361810` and starts or updates the voice
through `0x003638B0`. The emitter record itself is on the map sound list page.

`0x00363B40` builds the per-weather-slot ambient list from the `SPP1` section's `u16 +0x1A` offset
when it is non-zero, which it is in all 545 shipped lists, else from this header's `+4` list; the
current slot (`0x00265920`) picks the entry.

### LGT2, the light set

`0x0037AA90(block, group)` accepts the block when its first dword is `LGT2` (`0x3254474C`) and stores
it in group `group` (0 to 4) of the `0x50`-byte group table at `0x02EBF420`. It walks the chunk chain
at `block + u16[+4]` (`{u16 size, u16 kind}` chunks, kinds 0 to 3 and 5 to 7 stored to the group's
slots) and remaps a byte of each of the `u16[+0xA]` 0x70-byte records through `0x01EF94E4`. The
section's own format is on the section-014 page.

### TIM2 pictures and NPS2 placements

`0x003C63A0(picture)` registers picture 0 as a texture (`0x0024A480(picture, "navi_Load", 2, …, 0x200)`)
and keeps its width and height (`u16 +0x14` and `+0x16` of the texture header) at `0x02B457F8` and
`0x02B457FC`. `0x00379870(i)` applies placement `i`:

`Nps2Placement` (`0x40` bytes, offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[3]` | magic | "NPS" |
| `+0x03` | `u8` | version "2" in all 577 shipped records; 0x00379870 treats "1" as a 256 x 256 picture |  |
| `+0x04` | `u8[12]` | pad | zero |
| `+0x10` | `f32` | x | world position of the picture (`0x00379870` -> `0x003C6360`) |
| `+0x14` | `f32` | y |  |
| `+0x18` | `f32` | width | picture extent (`0x00379870` -> `0x003C6380`), read only for version "2" |
| `+0x1C` | `f32` | height |  |
| `+0x20` | `u8[32]` | pad2 | zero |

### WD and MRP, carried but unread

Slot 1 is a wave bank: a `WD` magic, `u16 +2` bank id (46 distinct values, 0x1FA to 0x251), `u32 +4`
trailing data size (its start is 0x40-aligned), `u32 +8` and `+0xC` record counts (equal in all 46),
`u32 +0x14` flags (0, 0x8000 or 0x10000), an offset table of `count` dwords at `+0x20` with a record
stride of 0x20. `0x00378BC0` frees the slot in both modes (`0x00378DBA`, `0x00378E19`), so nothing reads it.

Slot 15 is an `MRP` relocated-pointer package (the menu resource package page). The pointer
`0x02ADD058` has four references: the store (`0x00378F04`), the teardown (`0x003782EB`, `0x003782FC`) and the
getter `0x00377B90`, whose only caller is `initgauge` (`0x0034DC70`). That verb passes it to `0x003E9020`,
which passes it as a 32-bit integer to `0x00408300`, where it becomes the second create parameter of
the gauge task `0x00406E80`. Only two packs, `rwg0201` and `rwg0202`, carry the slot, with identical
bytes.

## Shipped data

| quantity | value |
|---|---|
| packs | 550; count 32 and a 0xC0 header in every one; the sizes sum to the file length in every one |
| slots used | 0 (545), 1 (46), 4 (461), 8 (461), 9 (270), 10 (545), 13 (387), 15 (2), 16 (456), 17 (212), 24 to 27 (421, 136, 32, 17), 28 to 31 (396, 133, 31, 17) |
| commonest slot sets | {0, 4, 8, 10, 13, 16, 24, 28} 113 packs; with 9 added 48; with 9 and 17 48; with 9, 17, 25, 29 47; {0, 1, 10} 46; {0, 10} 41 |
| block packs | the 89 `<area>00` packs: 46 carry {0, 1, 10}, 41 {0, 10}, 2 nothing; no other pack is sound-only |
| YM00 | 461 sections, median 2.9 MB; count 17 and the same 17 tags in every one; 441 stamps are float-shaped values between 1 and 1000 |
| ACTL | 270 sections, 64 to 1,792 bytes; version 1 and record size 0x16 in all; the index ends where the first record begins and the records end at the aux offset in all 270; 1,822 records, 101 of them tombstones |
| SP1 | 456 sections, 704 to 9,792 bytes; `listOffset` (`+0x04`) 0x20 in all; the three regions tile areas, emitters, index in 454 (two sections have no emitter index) |
| SPP1 | 545 lists of 1 to 8 entries; the `+0x1A` list offset is non-zero in all 545 |
| TIM2 and NPS2 | one picture per section (`u16 +6` = 1); 577 placements, all version "2" |
| WD | 46 sections, all in `<area>00` packs; record stride 0x20 in the 27 with more than one record |

## Loader behaviour

### Two requests per field

`0x00331990(field)` requests the block pack in mode 0 and the field's own pack in mode 1 through
`0x00378A60(field, index, mode)`:

1. Mode 0 returns at once when `0x02ADD0E0` is non-negative and equals `0x02ADD0DC`: the block pack
   already bound is kept. Otherwise `0x00378230(1)` tears the previous packs down (when no load is
   pending, `0x0032F3D0(0)`) and `0x003784A0` releases the sound sections.
2. Mode 1 drops the minimap texture (`0x003C63A0(0)`), stores the index at `0x02ADD0DC` and tears down
   with `0x00378230(keep)`, keeping the mode-1 world object only when the same index is loaded again
   with `0x02ADD0EA` clear.
3. When no load is pending, `0x00377DC0` requests the loose effect bank `PS2Data\efb\<zone>.efb`
   (completions `0x003788F0` in mode 1 to `0x02ADD050`, `0x003789A0` in mode 0 to `0x02ADD098`, bind bits
   5 and 6) and `0x00378030` requests the pack: `0x0032E400(4, index)` sizes it, `0x0036A190` allocates an
   arena block tagged `MapNo`, and `0x0032E620` submits the load with the completion `0x00378BC0` and
   the argument `block | mode`.
4. Mode 1 names the scene from the pack's path (`0x00379A10(4, index)`, with five alias pairs at
   `0x01EF9490`), which `0x001805D0` receives.

The debug verb `mapload` (0x2001, `0x0050D4D0`) requests one pack in mode 1 with field 0. Around
the pack's allocation `0x0036C1A0` and `0x0036C110` push and pop the current arena number (`0x022D8E1C`,
stack at `0x022D8DD0`).

### The split

`0x00378BC0` first calls `0x0036B970(block, slots, 32)`, which is `0x0036B980`:

1. A count above 32 returns 0 (`0x0036B9BB`).
2. The header length plus the sum of every non-zero size plus 0x40 must equal the arena block's own
   size, and the arena must have a free handle per extra section (`0x0036BA78`-`0x0036BAA2`); otherwise
   0 is returned and nothing is split.
3. Each non-zero section's 0x40 slot is overwritten with a copy of the arena block header (owner
   bytes, size `+0x18`, tag) and registered as a block of its own; a zero size yields a null slot.

### The dispatch

With the 32 slot pointers, `0x00378BC0` keeps or frees each section and marks the kept ones in the
pending word `0x02ADD0EC` and the bind word `0x02ADD0F0`:

| slots | mode 1 (the field's own pack) | mode 0 (the block pack) |
|---|---|---|
| 24 to 27, 28 to 31 | stored at `0x02ADD010 + 8i` and `0x02ADD030 + 8i`, bits 9 + i and 13 + i | the same |
| 4 | copied into a block of the same size (`0x0036C100` reads it from the block header) tagged `IdMapNo` at `0x02ADCFE8`, the original freed | neither stored nor freed |
| 8 | `0x02ADCFE0`, bit 3 | `0x02ADCFF0`, bit 3 |
| 0, 10 | freed | `0x02ADD080` and `0x02ADD068`, bit 0 |
| 1 | freed | stored at `0x02ADD070` and freed at once |
| 12, 13 | freed | freed |
| 16 | `0x02ADD060`, bit 7 | the same |
| 17 | `0x02ADD090`, bit 8 | the same |
| 9 | `0x02ADD0B8`, bit 4 | the same |
| 15 | `0x02ADD058`, bit 18 | the same |

It then clears pending bits 0 to 18 one by one and, when the pending word is empty, calls the binder
`0x003775D0`; `0x00214B70` ends the completion.

### The bind

`0x003775D0` consumes the bind word: bit 7 stores the `SP1` block at `0x022CBAF0` (`0x003635C0`); bit 0
walks the `SeSep` bank with `0x002DF070`, frees it and keeps the `SPP1` list at `0x022CBAF8` with the
sound map number (`0x003635E0`); bit 4 publishes the `ACTL` block (`0x003E8940`, cleared again when its
version is not 1); bit 8 binds the lights (`0x0037AA90(block, 0)`) and refreshes with `0x003DE920(0, 1)`;
bit 3 runs `0x00378120`, which:

1. makes the mode-1 `YM00` current (`0x02ADCFF8`) and uploads picture 0 (`0x003C63A0`) and placement 0
   (`0x00379870`);
2. hands the mode-0 `YM00` to `0x0026E7D0` (its object at `0x0209A668`, the pack pointer kept at
   `0x02ADD000`) and the mode-1 one to `0x0026E760` (its object at `0x0209A670`), both built by
   `0x002F6AB0` from a 0x240-byte allocation;
3. binds the navigation copy (`0x02ADD008`, `0x00384160`) and copies the current environment record to
   `0x02ADD10C`-`0x02ADD114`; the verb `seteventfogcolor` (`0x0120`, `0x00351AA0`) later replaces the four bytes at
   `0x02ADD114` with its four arguments, each clamped to 0 to 255 (`0x00379950`);
4. applies the world object's tag-11 colour (`0x003AFD40`) and calls `0x00332130(0)`.

The teardown `0x00378230(releaseWorld)` frees every stored section, unbinds the lights
(`0x0037AA50(0)`), the `ACTL` (`0x003E8940(0)`) and the navigation data (`0x00384160(0)`), drops the
pictures and placements and resets the ambient colour; `0x003784A0` frees the block pack's world
object, the loose effect bank and the two sound sections.

The world objects go through two helpers. `0x0026EAC0`, called by `0x00378230` while a mode-1 `YM00` is
current, releases the mode-1 object `0x0209A670`, runs `0x003ECF70` and clears the model block
(`0x0026E640`); `0x0026EAF0`, called by `0x003784A0`, does the same and then releases the mode-0 object
`0x0209A668`. Each release is `0x003EC860(slot, 0x0026EDB0)`: when the slot holds an object, `0x0026EDB0`
runs the object's callback at `+0x128`, the block is freed (`0x003697F0`) and the slot zeroed. The
teardown also runs `0x00363730`, which zeroes `0x022CBA90`, the `SP1` pointer `0x022CBAF0` and `0x022CBA9A`.

`0x002F6AB0` sets that callback to `0x002F5450`. It frees the object's own tables (`[+0x1C0]` to
`[+0x218]` and the tag-24 entries' `+0xC0`), removes the tag-14 buffer from the buffer list
(`0x00468060`), frees the animation slots of tag 23 (`0x00466B10`: both arrays of every slot, then the
slot array; `0x02EBB6E0` and `0x02EBB6F8` become 0) and releases the paletted textures of tag 12
(`0x004680D0`).

The buffer list at `0x02EBB6A0` is set up at boot by `0x00467BB0` (from `0x0036F4D0`, through `0x00536120`)
with 0x28-byte entries: the last path component of a name, at most 31 characters, then the buffer
at `+0x20`. `0x00467BF0` appends an entry (`0x005360C0`, which allocates the node and counts it at
`+0x14`). `0x00468060` unlinks every entry of a buffer with `0x00536140`, whose release callback
`0x00467B20` runs `0x00467B30` on the buffer (its callback at `+0x10`, then its 0x60-byte entry array at
`+0x08` is freed) and frees the buffer.

The area initialisation `0x00266D10` resets the loader once through `0x00377CC0`: every section pointer
and world object pointer is zeroed, `0x02ADD0E0` becomes -1, `0x02ADD118` 1 and `0x02ADD130` the text
`none`, the start-up tables are requested again (`0x00378540`), and the pending and bind words
(`0x02ADD0EC`, `0x02ADD0F0`) and `0x02ADD0EA` are cleared.

## Modding notes

- A pack is valid when its 32 sizes plus the 0xC0 header and one 0x40 slot per present section add
  up to the file length; the loader checks nothing else about the container.
- A section placed in an unused slot (2, 3, 5 to 7, 11, 14, 18 to 23) stays allocated with no owner;
  slot 13 is always freed, so an edited embedded effect bank changes nothing and the loose `.efb` is
  the file to edit.
- A field's `YM00`, navigation, pictures and lights come from its own pack; its sound bank and map
  sound list come from the block pack, so two fields of one block share them.
- `YM00` must carry its 17 chunks in the tag order the index gives; the parser accepts any order but
  skips a chunk whose offset equals the next one's.
- An `ACTL` with a version other than 1 is dropped silently at bind.

## Related

- [Weather: the three weather slots of an area, the change roll on entering, the setweatherslot verb, the MWeather table, what the slot does to the sky, the map and combat, and the environment variant it selects](weather.md)
- [Zone changes: mapjump and the other jump verbs, the loading flags, the moment the new zone is ready and what names a map](zone-changes-and-mapjump.md)
- [Doors, gates and map changes: the override table the setmapid verbs write, what its floor, wall and mj bits block, the show and hide model masks and when a new map clears them](doors-gates-and-map-changes.md)
- [How a unit finds its way across the navigation mesh](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md)
- [The map sound list](../Sound-And-Music/map-sounds.md)
- [The menu-map container](../Game-Files-And-Data-Tables/menu-map-files.md)
- [section_014, the LGT2 light set](../EBP-Script-Files/ebp-lighting-lgt2.md)
- [The EFX and EFB effect containers](../17-Presentation-Rendering/effect-files-efx-efb.md
)
- [MRP menu resource packages](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md)
