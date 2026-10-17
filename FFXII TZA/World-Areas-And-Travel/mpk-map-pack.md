---
title: "MPK map pack: the sections of a map file, the two packs a field loads, how the loader splits and binds them, and what each section holds"
kind: "format"
category: "World, areas and travel"
addresses: "00331990, 00378A60, 00378030, 0036B980, 00378BC0, 003775D0, 00378120, 00378230, 002F6AB0, 003E8940, 003E8230, 00363B40, 003631B0, 00379870, 003C63A0, 0037AA90"
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
first word is the field's own pack index (`00264F10`), and the first word of the row's 16-byte block
record is the block pack index (`00264F40`); the block record's second word plus 500 is the sound
map number stored at `02ADD078` (`00264FD0`, `00378030`). The row and block layouts are on the
weather page, which reads the same two tables.

## Layouts

### The pack

`MpkHeader` (`C0`<sub>h</sub> bytes, offsets from the start of the file):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | count | 32 in all 550 packs; `0036B980` rejects a count above 32 |
| `04`<sub>h</sub> | `u32[32]` | size | section size per slot in slot order; 0 means the slot is absent |
| `84`<sub>h</sub> | `u8[60]` | pad | the header is padded to a multiple of `40`<sub>h</sub> |

The header length is `((count + 1) * 4 + 3Fh) & ~3Fh`, `C0`<sub>h</sub> for 32 slots. After it, for each slot
whose size is non-zero and in slot order, come a `40`<sub>h</sub>-byte slot (zero in the file; the loader
overwrites it with an arena block header) and the section's bytes. There are no offsets: a section's
position is the running sum, and `0036B980` refuses the pack when the sum does not equal the loaded
block's size (`0036BA30`-`0036BA45`).

| slot | magic | section | kept by | consumer |
|---|---|---|---|---|
| 0 | `SeSe` | the `SeSep` sound-effect bank | mode 0 (`02ADD080`) | `003635E0` walks it with `002DF070` and frees it |
| 1 | `WD` | a wave bank | neither mode | freed unread (`00378BC0`) |
| 4 | u32 1 | the navigation dataset | mode 1 (`02ADCFE8`, copied) | `00384160` binds it (the navigation mesh page) |
| 8 | `YM00` | world data | mode 1 (`02ADCFE0`), mode 0 (`02ADCFF0`) | `0026E760`, `0026E7D0` build the `240`<sub>h</sub>-byte world object through `002F6AB0` |
| 9 | `ACTL` | the actor-control table | both (`02ADD0B8`) | `003E8940` publishes it at `02B5D080` |
| 10 | `SPP1` | the map sound list | mode 0 (`02ADD068`) | `003635E0` keeps it at `022CBAF8` (the map sound list page) |
| 13 | `EFB0` | a map effect bank | neither mode | freed; the loose `PS2Data\efb\<zone>.efb` is loaded instead (`00377DC0`) |
| 15 | `MRP` | a menu resource package | both (`02ADD058`) | `00377B90` returns it to `initgauge` (`0034DC70`) |
| 16 | `SP1` | the sound-emitter block | both (`02ADD060`) | `003635C0` keeps it at `022CBAF0` |
| 17 | `LGT2` | the light set | both (`02ADD090`) | `0037AA90(block, 0)` |
| 24 to 27 | `TIM2` | map pictures, one per sub-location | both (`02ADD010` + 8i) | `003C63A0` uploads picture 0 |
| 28 to 31 | `NPS2` | each picture's placement | both (`02ADD030` + 8i) | `00379870` applies placement 0 |

Slots 2, 3, 5 to 7, 11, 12, 14 and 18 to 23 are never read by `00378BC0` (slot 12 is freed), and no
shipped pack fills them.

### YM00, the world data

`Ym00Header` (`14`<sub>h</sub> bytes, offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8[4]` | magic | "YM00" |
| `04`<sub>h</sub> | `u32` | stamp | an export value; not read by `002F6AB0`, which starts at +`10`<sub>h</sub> |
| `08`<sub>h</sub> | `u8[8]` | author | an export tag; not read by `002F6AB0` |
| `10`<sub>h</sub> | `u32` | count | 17 in all 461 sections; `002F6AB0` reads it at [base + `10`<sub>h</sub>] |
| `14`<sub>h</sub> | `u32[]` | index | count + 1 entries of {u24 offset in 16-byte units from +`10`<sub>h</sub>, u8 tag}; the last is the end sentinel with tag `FF`<sub>h</sub> |

Before the walk `002F6AB0` sets `+120`<sub>h</sub> to 1 and `+110`<sub>h</sub> to 0, and clears the first `48`<sub>h</sub> bytes of
the two `68`<sub>h</sub>-byte sub-records at `+40`<sub>h</sub> and `+A8`<sub>h</sub> with `00231F50`, nine qword stores of 0
(`002F6AEA`-`002F6B14`).

`002F6AB0(object, kind)` walks the index: an entry whose offset equals the next entry's is skipped,
otherwise its tag selects an arm (`cmp eax, 21h`, a 34-case jump table). The arms that store or
parse a chunk:

| tag | what 002F6AB0 does with the chunk |
|---|---|
| 0 | `[+16Ch]` = first dword (a count), `[+188h]` = chunk + `10`<sub>h</sub>: the `40`<sub>h</sub>-byte placement rows `002F5550` composes |
| 1 | `[+170h]` = count, `[+190h]` = chunk + `10`<sub>h</sub>, `[+1C8h]` = an allocation of `count * 4` |
| 9 | `003ED3F0(chunk)`: the three `180`<sub>h</sub>-byte environment records at `02B5ED94` |
| 11 | `0026E8C0` stores it at `0209A660`; dword 0 to `022D8ED8` unless `FFFFFFFF`<sub>h</sub>; dword 1 unpacked by `00466140` into the colour `0209A3A0`-`0209A3AC` (scaled by 1/128); dwords 2 and 3 to `0209A6EC` and `0209A6F0` |
| 12 | `00468160(chunk, [+150h], [+1B8h])` |
| 14, 26 | `003EC910(6, 20h, 00467D00)` then `00467D20(buffer, chunk)`; `[+150h]` = buffer, `00467BF0(buffer, 0)` appends it to the buffer list at `02EBB6A0`; tag 26 also sets `[+230h]` = 1 |
| 17, 31 | `00232380(object + A8h or + 40h, chunk)`: a six-tag sub-container into the two `68`<sub>h</sub>-byte sub-records |
| 22 | `[+180h]` = chunk |
| 23 | `00466E70(chunk)`: the map animation slots at `[02EBB6F0]` (below) |
| 24 | `[+220h]` = count, `[+198h]` = chunk + `10`<sub>h</sub>, `[+1D0h]` = an allocation of `count * E0h` |
| 25 | `003ED190(chunk)`: field-dependent environment setup |
| 27 | `003ED840(chunk)` |
| 28, 29, 32 | `[+1A8h]`, `[+1B0h]`, `[+1B8h]` = chunk |
| 30 | `[+174h]` = count, `001806F0(count)`, `[+178h]` = chunk + `10`<sub>h</sub>: the `30`<sub>h</sub>-byte instance records |
| 33 | `002F6740(object, chunk)` |

Every shipped section carries exactly the 17 tags 0, 1, 11, 12, 17, 22 to 33 and the sentinel, so the
skipped tags 2 to 8, 10, 13, 15, 16 and 18 to 21 never occur. After the walk the constructor
allocates `count30 * 70h` at `[+1C0h]`, fills each entry from the tag-30 records (colour from the
record's `+C`<sub>h</sub> or from the tag-0 row through the `+40`<sub>h</sub> sub-record's transform, `00231A90`) and
links the records that carry bit 30 of their `+C`<sub>h</sub> word to their tag-24 entry (`word +14h`).

`003ED190` (tag 25) also sends a light direction to the shadow object through `001F1590`, which
creates the `B08`<sub>h</sub>-byte shadow object at `01F82EA8` on first use (`001EF2D0`) and stores the direction
with `001F08A0`. The direction is (0.0001, 1, 0) in field `11A`<sub>h</sub> (`003148F0`); otherwise the
vector at `+10`<sub>h</sub> of the tag-11 chunk (`0209A660`) when it is non-zero; otherwise the chunk's three
angles at `+90`<sub>h</sub> to `+98`<sub>h</sub> turned into a direction, or x 0.0001 and y 1.0 when all three are 0.
`003ED3F0` (tag 9) also passes a direction to `001F1590`, the same (0.0001, 1, 0) in field `11A`<sub>h</sub>.

The tag-28 chunk is published when a map binds: `003ED870`, called by `0026E960`, stores the world
object's `[+1A8h]` at `02B5F1A8` when the chunk's first word is positive, and `003ED820` (from
`0026E640` and `0036F4D0`) clears `02B5F1A0`, `02B5F1A8` and `02B5F1B0`.

### Tag 23, the map animation slots

Tag 23 holds the map's animation clips: moving and turning map parts, colour pulses, texture frames
and the area's ambient colour. `00466E70(chunk)` builds one `50`<sub>h</sub>-byte slot per clip into an array at
`[02EBB6F0]` (count `02EBB6E0`, chunk `02EBB6F8`). The chunk is a count at `+10`<sub>h</sub> and an offset
table from `+14`<sub>h</sub> in 16-byte units from `+10`<sub>h</sub>; slot `i` has a clip when entries `i` and `i + 1`
differ.

`MapAnimClip` (`30`<sub>h</sub> bytes, offsets from the start of the clip):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[32] name` | "ambient" makes the slot's `+34`<sub>h</sub> = 0 |  |
| `20`<sub>h</sub> | `f32` | start | first frame (`00466C40`) |
| `24`<sub>h</sub> | `f32` | end | last frame (`00466BB0`) |
| `28`<sub>h</sub> | `i16` | targets | target count |
| `2A`<sub>h</sub> | `u16` | group | model group the clip belongs to |
| `2C`<sub>h</sub> | `i16` | mapCount | 0, or the count of 16-byte map entries from +`30`<sub>h</sub> that replace +`28`<sub>h</sub> |
| `2E`<sub>h</sub> | `u8` | flags | bit 0: `02EBB6E4` = this slot |

After the clip header (and its map entries) comes a track list: a count and one offset per track,
again in 16-byte units. A track starts with its own header and then its keys:

`MapAnimTrack` (`20`<sub>h</sub> bytes, offsets from the start of the track):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i32` | keyCount |  |
| `04`<sub>h</sub> | `u8` | channel | the target field the track drives (`00466420`) |
| `08`<sub>h</sub> | `i16` | targetId | stored at the target's +`46`<sub>h</sub> |
| `0A`<sub>h</sub> | `i16` | targetId2 | stored at the target's +`44`<sub>h</sub> |
| `0C`<sub>h</sub> | `i32` | target | the target's index in the slot |
| `10`<sub>h</sub> | `f32[4] key0` | time, value, in-slope, out-slope; keyCount keys of 16 bytes from here |  |

`00466E70` allocates the slot's track records (`18`<sub>h</sub> bytes each: key data, time `+08`<sub>h</sub>, value
`+0C`<sub>h</sub>, key index `+10`<sub>h</sub>) and its `130`<sub>h</sub>-byte targets, and sets bit `channel` of each target's
`+40`<sub>h</sub>. It then binds the tracks (`004677A0`), resets the slots (`00467420`) and runs one update
(`004668C0`).

`MapAnimSlot` (`50`<sub>h</sub> bytes, offsets from the start of the [02EBB6F0]+i*`50`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | clip |  |
| `08`<sub>h</sub> | `void*` | clipActive | non-null for a live slot; every accessor tests it |
| `10`<sub>h</sub> | `void*` | mapEntries | when clip +`2C`<sub>h</sub> is non-zero |
| `18`<sub>h</sub> | `void*` | trackList |  |
| `20`<sub>h</sub> | `void*` | tracks | `18`<sub>h</sub> bytes each |
| `28`<sub>h</sub> | `void*` | targets | `130`<sub>h</sub> bytes each |
| `30`<sub>h</sub> | `i16` | trackCount |  |
| `32`<sub>h</sub> | `i16` | targetCount |  |
| `34`<sub>h</sub> | `i16` | ambient | 0 for the clip named "ambient", else -1 |
| `38`<sub>h</sub> | `f32` | rate | 1.0 after a reset (`00467700` sets it, `004735D0` too) |
| `3C`<sub>h</sub> | `f32` | rangeStart | clamped to the clip's start (`00467660`) |
| `40`<sub>h</sub> | `f32` | rangeEnd | clamped to the clip's end |
| `44`<sub>h</sub> | `f32` | time |  |
| `48`<sub>h</sub> | `f32` | step | dt * rate, added each frame by `004678E0`, zeroed after the update |
| `4C`<sub>h</sub> | `u32` | flags | bit 0 playing, bit 1 loop, bit 2 finished, bit 3 update once, bit 4 relink |

`00466E70` gives every slot the loop bit and, when it has a clip, bits 0 and 4. `00467420` resets
each live slot: the range becomes the clip's start and end, bit 2 is cleared and bit 3 set, the time
and every track's time become the start, the rate 1.0, and every target gets an identity matrix
(`00203170`), colour 1.0 at `+50`<sub>h</sub> to `+5C`<sub>h</sub>, rotation and translation 0 and scale 1.0.

`004677A0` binds each track's value to its target through `00466420(target, channel, &value)`;
with map entries, entry `+02`<sub>h</sub> names the track, `+04`<sub>h</sub> the channel and `+06`<sub>h</sub> the target. The
channels are:

| Channel | Target field |
|---|---|
| 0 to 2 | translation `+E8`<sub>h</sub>, `+F0`<sub>h</sub>, `+F8`<sub>h</sub> |
| 3 to 5 | rotation in degrees `+D0`<sub>h</sub>, `+D8`<sub>h</sub>, `+E0`<sub>h</sub> |
| 6 to 8 | scale `+100`<sub>h</sub>, `+108`<sub>h</sub>, `+110`<sub>h</sub> |
| 9 | `+90`<sub>h</sub>, the texture frame the draw pass reads |
| 10, 11 | `+98`<sub>h</sub>, `+A0`<sub>h</sub> |
| 12, 13, 14 | colour red, green, blue `+B0`<sub>h</sub>, `+B8`<sub>h</sub>, `+C0`<sub>h</sub>; 15 sets all three |
| 16 | `+A8`<sub>h</sub>, which the draw pass scales by 0.01 |
| 17 | colour alpha `+C8`<sub>h</sub> |
| 18 to 20 | rotation in radians `+118`<sub>h</sub>, `+120`<sub>h</sub>, `+128`<sub>h</sub> |

Each world step `004668C0` (reached through the thunk at `0036F400`) advances every slot with bit 0 whose bit 3 is set or
whose step exceeds 0.001:

1. bits 2 and 3 are cleared and the time moves by the step;
2. with the loop bit and a range of at least 1.0 the time wraps within the range; otherwise it
   clamps and bit 2 (finished) is set;
3. unless the clip's group is above `100`<sub>h</sub> with its bit in the hidden-model set (`0026E5F0`),
   `00466240` advances each track and `00466550` rebuilds each target;
4. the step is zeroed.

`00466240(slot, track)` moves the track's time by the slot's step, clamps or wraps it the same way
within the range and the track's own first and last key, finds the key pair around the time and
interpolates with a cubic Hermite curve (each key's value, the first key's out-slope and the second
key's in-slope) into the track's value. The slopes are per unit of time: with u = (t - t0) / (t1 - t0),
the value is h00(u) v0 + h01(u) v1 + (t1 - t0) (h10(u) out0 + h11(u) in1).

`00466550(slot, target)` reads the bound channels: translation into `+70`<sub>h</sub> to `+78`<sub>h</sub>, degrees
turned into radians and wrapped into `+60`<sub>h</sub> to `+68`<sub>h</sub> (the radian channels overwrite them), scale
into `+80`<sub>h</sub> to `+88`<sub>h</sub>. It rebuilds the target's matrix at `+00`<sub>h</sub> from the three rotations, each
applied only when it is not 0 (`00202E90`, `00202F00`, `00202F70`), and the translation, scales its four rows by `+80`<sub>h</sub> to `+8C`<sub>h</sub>
(`00202FE0`) and, for the `ambient` slot, copies the colour `+50`<sub>h</sub> to `+5C`<sub>h</sub> to `0209A370` to
`0209A37C`, the ambient colour of the map's lights.

The slot accessors take a slot number and test it against `02EBB6E0` and `+08`<sub>h</sub>:

- `00466C80(slot)` returns the time `+44`<sub>h</sub> (0 for a bad slot) and `00466AD0(slot)` the finished bit 2 (1 for a bad
  slot, the test `004735E0` of the actor-control table uses);
- `00473490(slot)` returns the time less the clip's start (`00466C40`), the verb `getbganimeframe` (`0AD`<sub>h</sub>,
  `0034FEE3`); `004734C0(slot)` returns the clip's end (`00466BB0`) less its start, `getbganimelastframe` (`0AE`<sub>h</sub>,
  `00350393`);
- `00467730(slot, t)` seeks: it clears bit 2, sets bit 3, stores `t` as the time of the slot and of every track and
  zeroes the step and each track's `+10`<sub>h</sub>; the rewind `00473500` and `00466DD0` use it;
- `00466DD0()` sends every playing slot that does not loop and has a non-zero rate to its range end and marks it
  finished; it runs from the script skip's start `00360710` and end `00360A50`, and from `003486A0` and `00355300`.

The draw code reaches targets through the tag-30 instances. `00466CB0(slot, idB, idA, mask)`
returns the slot's first target when the clip's group is below `100`<sub>h</sub> and its bit is in the
instance's group mask, else the target whose `+46`<sub>h</sub> (or map entry `+00`<sub>h</sub>) equals `idB`, else the
one whose `+44`<sub>h</sub> equals `idA`. `002F6AB0` and `002F5550` call it with the instance record's `+02`<sub>h</sub>
and `+08`<sub>h</sub> words and its group mask `+20`<sub>h</sub>.

When a slot's bit 4 is set, `002F5550` clears it and
stores the target in each matching instance's `70`<sub>h</sub>-byte entry at `+50`<sub>h</sub> while the slot plays
(`00466B80`, bit 0), or 0 when it does not.

### ACTL, the actor-control table

`ActlHeader` (`10`<sub>h</sub> bytes, offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8[4]` | magic | "ACTL" |
| `04`<sub>h</sub> | `u16` | version | must be 1: `003E8940` clears the pointer otherwise |
| `06`<sub>h</sub> | `u16` | recordSize | `16`<sub>h</sub> in all 270 sections; `003E8230` and the two walkers advance by it |
| `08`<sub>h</sub> | `u16` | idBound | `003E8230` refuses an id at or above it |
| `0A`<sub>h</sub> | `u16` | reserved | 0 |
| `0C`<sub>h</sub> | `u16` | indexOffset | `10`<sub>h</sub>: the bucket index {u16 bucketCount; {u16 bound, u16 recordOffset}[bucketCount]} |
| `0E`<sub>h</sub> | `u16` | auxOffset | the aux table `003E7EC0` and `003E8D50` pass to the record handlers |

`003E8230(id)` returns the record of an id:

- bucket = `id / 100`, slot = `id % 100`;
- a miss when the id reaches `idBound`, the bucket reaches `bucketCount` or the slot reaches the
  bucket's bound;
- a hit is `section + recordOffset[bucket] + slot * recordSize`.

`003E7EC0` and `003E8D50(mode)` walk every bucket's records in the same arithmetic and hand each to
`003E8020` or `003E8C50` with the aux table and the weather slot (`00265920`); `003E8D50` skips
records whose byte `+15`<sub>h</sub> differs from a non-negative mode.

`003E8020` keeps the record's state in its first word: bit 0 processed (set on first touch, when the
low nibbles of bytes `+13`<sub>h</sub> and `+14`<sub>h</sub> are copied into their high nibbles and the high nibble of
`+12`<sub>h</sub> becomes 3), bit 1 the alternator, bits 2 and 3 an override, bit 4 "was active". A first word
of `FFFF`<sub>h</sub> is a tombstone that every walker skips.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | state | the state bits above |
| `02`<sub>h</sub> | `i16` | animation | map animation slot, -1 for none (`004735D0` sets its rate) |
| `08`<sub>h</sub> | `i16` | light | `LGT2` light id, -1 for none; bit 14 routes it through the aux table (`003E8190`) |
| `0E`<sub>h</sub> | `i16` | effect | map effect channel, -1 for none |
| `10`<sub>h</sub> | `i16` | sound | map sound emitter below 1000 |
| `12`<sub>h</sub> | `u8` | mode | high nibble 0 runs `003E8440`, 1 runs the test `003E8350` |
| `13`<sub>h</sub> | `u8` | gate | a non-zero high nibble skips the mode step |
| `14`<sub>h</sub> | `u8` | soundMode | the high nibble feeds `00363A90` |
| `15`<sub>h</sub> | `i8` | effectArg | third argument of `0026FAD0`, negatives as 0; the walker's mode filter |

On first touch `003E8020` runs `003E8990`, which clears state bits 3 and 4, rewinds the animation
slot (`00473500(slot, -1.0, -1.0)`), sets its rate to 0 (`004735D0`) and sets the sound emitter's
flags with `00363A90`. A toggle with bit 1 clear runs `003E85B0` and sets the bit; with bit 1 set it
runs `003E8690` and clears it:

- `003E85B0` sets the animation slot's rate to 0, turns the light's loop off and stops its animation
  (`0037A310`, `0037A130`, or `003E8A10` and `003E8A40` through the aux table), starts the effect
  channel (`0026FAD0`) and clears its flag (`002700F0(channel, 0)`), and sets bit 4 of the sound
  emitter's flag byte (`00363AD0(id, 1)`);
- `003E8690` sets the rate to 1.0, resets, turns on and restarts the light (`0037A270`, `0037B190`,
  `0037A1D0`, `0037A310`), sets the channel's flags (`002700F0`, `00270130`) and starts it, and
  clears the emitter's bit 4.

In mode 1 `003E8020` sets state bit 4 when `003E8350` finds that `004735E0` (the animation slot), `0037B030` (the light,
or the callback `003E82A0` through the aux table) and `00362E30` (the emitter's bit 0) all return 0
and `0026FDB0` does not return 2 for the channel.

### SP1, the sound emitters

`Sp1Header` (`20`<sub>h</sub> bytes, offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8[4]` | magic | "SP1" |
| `04`<sub>h</sub> | `u32` | listOffset | `20`<sub>h</sub> in all 456 sections: `00363B40` reads the weather-slot list here when the SPP1 list is absent |
| `08`<sub>h</sub> | `u32` | areasOffset | the listener grid `00362E50` searches |
| `0C`<sub>h</sub> | `u32` | indexOffset | {u16 bound; u16 recordOffset[]}: the emitter index `00362850` passes to `003631B0` |
| `10`<sub>h</sub> | `u32` | emittersOffset | a u16 prefix list terminated by bit 15, then the emitter records |
| `14`<sub>h</sub> | `u32` | reserved14 | 0 |
| `18`<sub>h</sub> | `u16` | reserved18 | 0 |
| `1A`<sub>h</sub> | `u16` | reserved1A | 0 |
| `1C`<sub>h</sub> | `u32` | reserved1C | 0 |

`003631B0(listener, list, index, current)` walks a list of index entries, resolves each through the
index into a record at `022CBAF0 + recordOffset`, dispatches on the record's shape byte `+9`
(`& 7Fh`: 0, 1, 2, other), evaluates the volume through `00361810` and starts or updates the voice
through `003638B0`. The emitter record itself is on the map sound list page.

`00363B40` builds the per-weather-slot ambient list from the `SPP1` section's `u16 +1Ah` offset
when it is non-zero, which it is in all 545 shipped lists, else from this header's `+4` list; the
current slot (`00265920`) picks the entry.

### LGT2, the light set

`0037AA90(block, group)` accepts the block when its first dword is `LGT2` (`3254474C`<sub>h</sub>) and stores
it in group `group` (0 to 4) of the `50`<sub>h</sub>-byte group table at `02EBF420`. It walks the chunk chain
at `block + u16[+4]` (`{u16 size, u16 kind}` chunks, kinds 0 to 3 and 5 to 7 stored to the group's
slots) and remaps a byte of each of the `u16[+Ah]` `70`<sub>h</sub>-byte records through `01EF94E4`. The
section's own format is on the section-014 page.

### TIM2 pictures and NPS2 placements

`003C63A0(picture)` registers picture 0 as a texture (`0024A480(picture, "navi_Load", 2, …, 200h)`)
and keeps its width and height (`u16 +14h` and `+16`<sub>h</sub> of the texture header) at `02B457F8` and
`02B457FC`. `00379870(i)` applies placement `i`:

`Nps2Placement` (`40`<sub>h</sub> bytes, offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8[3]` | magic | "NPS" |
| `03`<sub>h</sub> | `u8` | version "2" in all 577 shipped records; 00379870 treats "1" as a 256 x 256 picture |  |
| `04`<sub>h</sub> | `u8[12]` | pad | zero |
| `10`<sub>h</sub> | `f32` | x | world position of the picture (`00379870` -> `003C6360`) |
| `14`<sub>h</sub> | `f32` | y |  |
| `18`<sub>h</sub> | `f32` | width | picture extent (`00379870` -> `003C6380`), read only for version "2" |
| `1C`<sub>h</sub> | `f32` | height |  |
| `20`<sub>h</sub> | `u8[32]` | pad2 | zero |

### WD and MRP, carried but unread

Slot 1 is a wave bank: a `WD` magic, `u16 +2` bank id (46 distinct values, `1FA`<sub>h</sub> to `251`<sub>h</sub>), `u32 +4`
trailing data size (its start is `40`<sub>h</sub>-aligned), `u32 +8` and `+C`<sub>h</sub> record counts (equal in all 46),
`u32 +14h` flags (0, `8000`<sub>h</sub> or `10000`<sub>h</sub>), an offset table of `count` dwords at `+20`<sub>h</sub> with a record
stride of `20`<sub>h</sub>. `00378BC0` frees the slot in both modes (`00378DBA`, `00378E19`), so nothing reads it.

Slot 15 is an `MRP` relocated-pointer package (the menu resource package page). The pointer
`02ADD058` has four references: the store (`00378F04`), the teardown (`003782EB`, `003782FC`) and the
getter `00377B90`, whose only caller is `initgauge` (`0034DC70`). That verb passes it to `003E9020`,
which passes it as a 32-bit integer to `00408300`, where it becomes the second create parameter of
the gauge task `00406E80`. Only two packs, `rwg0201` and `rwg0202`, carry the slot, with identical
bytes.

## Shipped data

| quantity | value |
|---|---|
| packs | 550; count 32 and a `C0`<sub>h</sub> header in every one; the sizes sum to the file length in every one |
| slots used | 0 (545), 1 (46), 4 (461), 8 (461), 9 (270), 10 (545), 13 (387), 15 (2), 16 (456), 17 (212), 24 to 27 (421, 136, 32, 17), 28 to 31 (396, 133, 31, 17) |
| commonest slot sets | {0, 4, 8, 10, 13, 16, 24, 28} 113 packs; with 9 added 48; with 9 and 17 48; with 9, 17, 25, 29 47; {0, 1, 10} 46; {0, 10} 41 |
| block packs | the 89 `<area>00` packs: 46 carry {0, 1, 10}, 41 {0, 10}, 2 nothing; no other pack is sound-only |
| YM00 | 461 sections, median 2.9 MB; count 17 and the same 17 tags in every one; 441 stamps are float-shaped values between 1 and 1000 |
| ACTL | 270 sections, 64 to 1,792 bytes; version 1 and record size `16`<sub>h</sub> in all; the index ends where the first record begins and the records end at the aux offset in all 270; 1,822 records, 101 of them tombstones |
| SP1 | 456 sections, 704 to 9,792 bytes; list offset `20`<sub>h</sub> in all; the three regions tile areas, emitters, index in 454 (two sections have no emitter index) |
| SPP1 | 545 lists of 1 to 8 entries; the `+1A`<sub>h</sub> list offset is non-zero in all 545 |
| TIM2 and NPS2 | one picture per section (`u16 +6` = 1); 577 placements, all version "2" |
| WD | 46 sections, all in `<area>00` packs; record stride `20`<sub>h</sub> in the 27 with more than one record |

## Loader behaviour

### Two requests per field

`00331990(field)` requests the block pack in mode 0 and the field's own pack in mode 1 through
`00378A60(field, index, mode)`:

1. Mode 0 returns at once when `02ADD0E0` is non-negative and equals `02ADD0DC`: the block pack
   already bound is kept. Otherwise `00378230(1)` tears the previous packs down (when no load is
   pending, `0032F3D0(0)`) and `003784A0` releases the sound sections.
2. Mode 1 drops the minimap texture (`003C63A0(0)`), stores the index at `02ADD0DC` and tears down
   with `00378230(keep)`, keeping the mode-1 world object only when the same index is loaded again
   with `02ADD0EA` clear.
3. When no load is pending, `00377DC0` requests the loose effect bank `PS2Data\efb\<zone>.efb`
   (completions `003788F0` in mode 1 to `02ADD050`, `003789A0` in mode 0 to `02ADD098`, bind bits
   5 and 6) and `00378030` requests the pack: `0032E400(4, index)` sizes it, `0036A190` allocates an
   arena block tagged `MapNo`, and `0032E620` submits the load with the completion `00378BC0` and
   the argument `block | mode`.
4. Mode 1 names the scene from the pack's path (`00379A10(4, index)`, with five alias pairs at
   `01EF9490`), which `001805D0` receives.

The debug verb `mapload` (`2001`<sub>h</sub>, `0050D4D0`) requests one pack in mode 1 with field 0. Around
the pack's allocation `0036C1A0` and `0036C110` push and pop the current arena number (`022D8E1C`,
stack at `022D8DD0`).

### The split

`00378BC0` first calls `0036B970(block, slots, 32)`, which is `0036B980`:

1. A count above 32 returns 0 (`0036B9BB`).
2. The header length plus the sum of every non-zero size plus `40`<sub>h</sub> must equal the arena block's own
   size, and the arena must have a free handle per extra section (`0036BA78`-`0036BAA2`); otherwise
   0 is returned and nothing is split.
3. Each non-zero section's `40`<sub>h</sub> slot is overwritten with a copy of the arena block header (owner
   bytes, size `+18`<sub>h</sub>, tag) and registered as a block of its own; a zero size yields a null slot.

### The dispatch

With the 32 slot pointers, `00378BC0` keeps or frees each section and marks the kept ones in the
pending word `02ADD0EC` and the bind word `02ADD0F0`:

| slots | mode 1 (the field's own pack) | mode 0 (the block pack) |
|---|---|---|
| 24 to 27, 28 to 31 | stored at `02ADD010 + 8i` and `02ADD030 + 8i`, bits 9 + i and 13 + i | the same |
| 4 | copied into a block of the same size (`0036C100` reads it from the block header) tagged `IdMapNo` at `02ADCFE8`, the original freed | neither stored nor freed |
| 8 | `02ADCFE0`, bit 3 | `02ADCFF0`, bit 3 |
| 0, 10 | freed | `02ADD080` and `02ADD068`, bit 0 |
| 1 | freed | stored at `02ADD070` and freed at once |
| 12, 13 | freed | freed |
| 16 | `02ADD060`, bit 7 | the same |
| 17 | `02ADD090`, bit 8 | the same |
| 9 | `02ADD0B8`, bit 4 | the same |
| 15 | `02ADD058`, bit 18 | the same |

It then clears pending bits 0 to 18 one by one and, when the pending word is empty, calls the binder
`003775D0`; `00214B70` ends the completion.

### The bind

`003775D0` consumes the bind word: bit 7 stores the `SP1` block at `022CBAF0` (`003635C0`); bit 0
walks the `SeSep` bank with `002DF070`, frees it and keeps the `SPP1` list at `022CBAF8` with the
sound map number (`003635E0`); bit 4 publishes the `ACTL` block (`003E8940`, cleared again when its
version is not 1); bit 8 binds the lights (`0037AA90(block, 0)`) and refreshes with `003DE920(0, 1)`;
bit 3 runs `00378120`, which:

1. makes the mode-1 `YM00` current (`02ADCFF8`) and uploads picture 0 (`003C63A0`) and placement 0
   (`00379870`);
2. hands the mode-0 `YM00` to `0026E7D0` (its object at `0209A668`, the pack pointer kept at
   `02ADD000`) and the mode-1 one to `0026E760` (its object at `0209A670`), both built by
   `002F6AB0` from a `240`<sub>h</sub>-byte allocation;
3. binds the navigation copy (`02ADD008`, `00384160`) and copies the current environment record to
   `02ADD10C`-`02ADD114`;
4. applies the world object's tag-11 colour (`003AFD40`) and calls `00332130(0)`.

The teardown `00378230(releaseWorld)` frees every stored section, unbinds the lights
(`0037AA50(0)`), the `ACTL` (`003E8940(0)`) and the navigation data (`00384160(0)`), drops the
pictures and placements and resets the ambient colour; `003784A0` frees the block pack's world
object, the loose effect bank and the two sound sections.

The world objects go through two helpers. `0026EAC0`, called by `00378230` while a mode-1 `YM00` is
current, releases the mode-1 object `0209A670`, runs `003ECF70` and clears the model block
(`0026E640`); `0026EAF0`, called by `003784A0`, does the same and then releases the mode-0 object
`0209A668`. Each release is `003EC860(slot, 0026EDB0)`: when the slot holds an object, `0026EDB0`
runs the object's callback at `+128`<sub>h</sub>, the block is freed (`003697F0`) and the slot zeroed. The
teardown also runs `00363730`, which zeroes `022CBA90`, the `SP1` pointer `022CBAF0` and `022CBA9A`.

`002F6AB0` sets that callback to `002F5450`. It frees the object's own tables (`[+1C0h]` to
`[+218h]` and the tag-24 entries' `+C0`<sub>h</sub>), removes the tag-14 buffer from the buffer list
(`00468060`), frees the animation slots of tag 23 (`00466B10`: both arrays of every slot, then the
slot array; `02EBB6E0` and `02EBB6F8` become 0) and releases the paletted textures of tag 12
(`004680D0`).

The buffer list at `02EBB6A0` is set up at boot by `00467BB0` (from `0036F4D0`, through `00536120`)
with `28`<sub>h</sub>-byte entries: the last path component of a name, at most 31 characters, then the buffer
at `+20`<sub>h</sub>. `00467BF0` appends an entry (`005360C0`, which allocates the node and counts it at
`+14`<sub>h</sub>). `00468060` unlinks every entry of a buffer with `00536140`, whose release callback
`00467B20` runs `00467B30` on the buffer (its callback at `+10`<sub>h</sub>, then its `60`<sub>h</sub>-byte entry array at
`+08`<sub>h</sub> is freed) and frees the buffer.

The area initialisation `00266D10` resets the loader once through `00377CC0`: every section pointer
and world object pointer is zeroed, `02ADD0E0` becomes -1, `02ADD118` 1 and `02ADD130` the text
`none`, the start-up tables are requested again (`00378540`), and the pending and bind words
(`02ADD0EC`, `02ADD0F0`) and `02ADD0EA` are cleared.

## Modding notes

- A pack is valid when its 32 sizes plus the `C0`<sub>h</sub> header and one `40`<sub>h</sub> slot per present section add
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
