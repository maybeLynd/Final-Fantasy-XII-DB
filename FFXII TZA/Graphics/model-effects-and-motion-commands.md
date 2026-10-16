---
title: "Model effects and motion commands: @FEF and the motion entries"
kind: "format"
category: "Graphics"
addresses: "00504F00, 00504E70, 00504940, 0016D6A0, 0040A230, 00409F80, 02B64380, 0041F340, 003B3550, 0041D220, 0041CA70, 004090D0, 0041CD30, 0041BEE0, 0041B4E0, 00409190, 00370E00, 0041B550, 0041B650, 00409170, 00409150, 0041A470, 00418650, 00418700, 004186A0, 0041FCF0"
---

## What the player sees

Some monsters, NPCs, summons and gadgets carry an effect authored into their model file. Weapons that
draw, fire and reload, and treasure chests that open, play short command blocks stored in their own
`.cm`. Every other motion a model plays comes from its `.ca` files: each motion is a list of bone
channels with keyed values, plus a command block that runs on the motion's frames.

## Where it comes from

All of these are entries of the `@FRP` containers described in [model files](model-files-cm-ca.md):
`@FEF` only in `.cm` files, `@FRM` only in `.ca` files, and `@FMC`, `@FMN` and `@FMW` in both. The
effect section is registered with the rest of the file in the render resource bank; the bank makes
the model's effect ticket and effect context, as
[resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) describes.
The motion entries are read when a presentation entry is set up to play a motion (`0041D220`).

## Layouts

### @FEF

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `'@FEF',` | u32 | kind 0, u32 length, u32 1 |
| `10`<sub>h</sub> | `char[32]` | the container's name |  |
| `30`<sub>h</sub> | `a` | complete | EFX0010 effect file: u32 +`08`<sub>h</sub> = 1.0f, u32 +`0C`<sub>h</sub> = entry length - `30`<sub>h</sub> |

### @FMC, the command block

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `04`<sub>h</sub> | `u32` | 1 (`10001`<sub>h</sub> in 405 of the 32,151 entries) |  |
| `0C`<sub>h</sub> | `u32` | record count |  |
| `10`<sub>h</sub> | `char[32]` | the command block's name (weapon_ready, treasure_open, ...) |  |
| `30`<sub>h</sub> | `records,` | each: |  |
| `00`<sub>h</sub> | `u8` | 1 for the block's main record |  |
| `03`<sub>h</sub> | `u8` | sub-record count |  |
| `04`<sub>h</sub> | `u16` | record length |  |
| `06`<sub>h</sub> | `sub-records:` | u16 | key, u16 (length << 6 \| command count), then the commands |

A key of `FFFF`<sub>h</sub> marks the block of commands that `0041CD30` runs before the keyed ones; the other
keys are motion frames. The commands themselves are the authored presentation commands
([authored-presentation-commands.md](authored-presentation-commands.md)).

### @FMN, the bone channel list

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `04`<sub>h</sub> | `u32` | kind: `02001111`<sub>h</sub> or `02001011`<sub>h</sub> |  |
| `0C`<sub>h</sub> | `u32` | record count |  |
| `10`<sub>h</sub> | `char[32]` | the motion's name |  |
| `50`<sub>h</sub> | `u16` | duration in frames |  |
| `F0`<sub>h</sub> | `records` | (the | start `00409190` picks for both kinds), 22 bytes each: |
| `00`<sub>h</sub> | `u16` | node key |  |
| `02`<sub>h</sub> | `u16` | bits 0-8 channel mask, bits 9-14 record length (22) |  |
| `04`<sub>h</sub> | `u16[9]` | channel numbers in the paired @FMW; `8000`<sub>h</sub> \| n where the mask bit is clear |  |

### @FMW, the channel data

```
+0x0C  u32  channel count
+0x30  u32  offset of the value streams, from the entry
+0x34  u32  1 = packed form (u16 channel table, 00409170); otherwise the u32 table form (00409150)
+0x40  u16[count] or u32[count]  channel descriptor offsets, from the entry
packed descriptor:  +0x00 u8 frame count, +0x01 u8 n, +0x04 u32[n] frame-stream offsets,
                    then per key {u32 value-stream offset (low 17 bits), f32 bias, f32 scale}
```

A stream element starts with a flag byte: bit 7 means a 16-bit little-endian literal follows, bit 6
means the stream's element 0 is reused, and otherwise a signed byte follows. A value is
`literal × scale + bias` for the first key and `literal × scale + previous value` after it; frame
literals add to the previous key's frame.

### @FRM

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0C`<sub>h</sub> | `u32` | 1 |  |
| `10`<sub>h</sub> | `char[32]` | the .ca file's name |  |
| `30`<sub>h</sub> | `payload:` | byte | +`01`<sub>h</sub> to `003E18D0`, byte +`02`<sub>h</sub> low six bits to skeleton +`A4`<sub>h</sub>, u32 +`08`<sub>h</sub> offset of a second region, from the payload (0 = none) |

### The version-1 .ca slot table

`+30`<sub>h</sub> holds 80 (the columns) and `+34`<sub>h</sub> the rows. `004090D0(container, row, column)` returns the
entry at slot `row × 80 + column` when the row is below `+34`<sub>h</sub>, otherwise slot `column`; an empty
slot gives NULL. The `@FMC` blocks fill the first `80 × rows` slots and `@FRM` is the last slot.

## Shipped data

| Fact | Value |
|---|---|
| `@FEF` | 144 `.cm` files: 82 monsters, 27 NPCs, 26 summons, 9 gadgets; always entry 6 of 7; all start `EFX0010` with the size word equal to the entry length − `30`<sub>h</sub> |
| `02B64380` paths | 144, set by `0040A230`; each slot is the fold of its file's name, and the 144 paths are exactly the 144 `@FEF` files |
| `.cm` motion entries | 45 files (29 weapons, 16 treasures); 209 `@FMC`, 111 `@FMN`, 111 `@FMW` |
| `.cm` command block names | every weapon: `weapon_shot`, `weapon_deact`, `weapon_active`, `weapon_ready`, `weapon_rlx_ready`; every treasure: `treasure_dead`, `treasure_ready`, `treasure_open`, `treasure_opened` |
| `.ca` entries | 31,942 `@FMC`, 18,303 `@FMN`, 18,303 `@FMW`, 3,164 `@FRM` (one per file, named after it) |
| version-1 `.ca` | 1,195; 80 columns in all; 1 row in 1,150, 3 in 45; `@FRM` in the last slot in all |
| `@FMN` records | 746,592, all 22 bytes, bit 15 clear, mask bits matching the `8000`<sub>h</sub> markers in all; no stream runs past its entry |
| `@FMW` form | packed in 110 `.cm` and 17,576 `.ca` entries, table form in 1 `.cm` and 727 `.ca` |
| frame counts | the first byte of each of the 1,446,602 packed channel descriptors equals the paired `@FMN` duration's low byte |
| `@FRM` payload | byte `+01`<sub>h</sub> 1 in 2,977, 2 in 169, 4 in 18; second region present in 2,847 |

## Loader behaviour

### Binding @FEF

- `00504F00` binds the `@FEF` section at model row `+228`<sub>h</sub> with `00504E70`, which falls back to a
  bank-wide search by tag and name when the model's own entry has none.
- `00504940` stores the section pointer at row `+230`<sub>h</sub> and calls `0016D6A0(ticket, section + 30h)`
  with the bank entry's ticket `+44`<sub>h</sub> (`005049BD`). `0016D6A0` is a bare `ret`: binding the row does
  nothing with the embedded effect.
- `0041F340` makes the render record's effect context: when the record's `+288`<sub>h</sub> is −1 and the row's
  `@FEF` bank index is set, it calls `003B3550(record, ticket)` and stores the result at record `+288`<sub>h</sub>
  and row `+240`<sub>h</sub>.

- `0041F340` takes its blocks in arena 6 through `003AB8B0(size, mode)` (`0036A100` for mode 0,
  `0036B160` for mode 1) and returns them through `003AB910`, which calls `0036C620` for a null or
  4-byte-aligned pointer and `0036C5D0` otherwise.

### The record's effect handle

The handle at record `+288`<sub>h</sub> names a `38`<sub>h</sub>-byte slot at `02EBD480 + (handle & 3Fh) × 38h`; every
helper below first checks that the slot's id equals the handle and does nothing otherwise. The slot's
`+10`<sub>h</sub> is the effect instance and its byte `+30`<sub>h</sub> holds three flags.

- `003B3400`, from `003B3550`, takes the head of the free list `02EBDBA0`, appends the slot to the
  used list (`02EBDB98` / `02EBDBA8`) and writes a new serial (`02EBDBB4`) into bits 6–27 of the id.
- `003B3300(handle)`, from `0041E860`, ends the instance (`0024EE60`), moves the slot back to the
  free list, keeps only bits 0–5 and 28–31 of the id and clears `+10`<sub>h</sub>.
- `003B3080(handle)` sets bit 0 of `+30`<sub>h</sub>. The update pass `0024B9B0` holds a kind-3 instance on any
  step the bit is clear in the slot its dword `+4` names, and clears the bit when it is set; `0042D830` sets it each time
  it processes the record, so a model's effect advances only while its character does.
- `003B33A0(handle, b)` sets bit 1 of `+30`<sub>h</sub> and stores `b` in bit 2; `0042D830` passes the
  result of `00420FB0` when `004210D0` allows it.
- `003B3AA0(handle, v)` stores the vector at instance `+320`<sub>h</sub> with w = 1, or 1, 1, 1, 1 when the
  instance's `+368`<sub>h</sub> bit `4000`<sub>h</sub> is set; `0042D830` passes the vector from `003E5710`.
- `003B30D0(handle, a, b)` sets the instance's two tint colours `+398`<sub>h</sub> (from `a`) and `+334`<sub>h</sub>
  (from `b`) with their red, green and blue at `80`<sub>h</sub>, and raises `+368`<sub>h</sub> bit `8`<sub>h</sub>; when the
  instance's `+36A`<sub>h</sub> bit `8`<sub>h</sub> is set, it also puts both alphas at `80`<sub>h</sub> and drops the bit again.
- `003B30A0(handle, v)` stores `v` at instance `+08`<sub>h</sub>, and `003B3CA0(handle, v)` runs `003A9490(v)`
  on the instance, then makes the previous instance current again.

- The registration that makes the ticket indexes the pointer table `02B64380` by the fold of the name.
  `0041E3A0` calls `00409F80` at start-up (`0041E40B`), which calls `0040A230`: 144 stores of
  `PS2Data\obj_finish\in\<folder>\...\<name>.cm` paths, so every shipped `@FEF` model has its entry.

### Selecting a motion

`0041D220(entry, descriptor)` sets up a presentation entry:

- `+31C`<sub>h</sub> takes the motion number (descriptor `+20`<sub>h</sub>) and `+31A`<sub>h</sub> the record's signed byte
  `+413`<sub>h</sub> (descriptor `+24`<sub>h</sub>);
- the `@FMC` section goes to `+320`<sub>h</sub>, or `@FRP` when the entry has no `@FMC`;
- when an `@FRM` exists and is longer than its header, `+378`<sub>h</sub> gets its payload offset and `+37C`<sub>h</sub>
  the second region's offset;
- `0041CA70` picks the command block `004090D0(container, +31Ah, +31Ch & FFFh)` into `+368`<sub>h</sub>, and
  `0041CD30` positions each track on its first record, keeping the `FFFF`<sub>h</sub> block apart.

The model binder `0041FCF0` also keeps the model's own first `@FMC` index at record `+2FA`<sub>h</sub>
(`0041FE83`), which the event map in [model files](model-files-cm-ca.md) adds to.

### Reading the channels

- `0041BEE0` binds `@FMN` (or `@FRP`) and `@FMW` by tag and name into a track descriptor (`+54`<sub>h</sub>,
  `+58`<sub>h</sub>), and `0041B4E0` resolves the entries.
- It walks the `@FMN` records from the start `00409190` gives, advancing by each record's length.
  `00370E00` turns the node key into a bone, and `0041B550` sets up the record's nine channels in a
  `108`<sub>h</sub>-byte row (count at owner `+2BC`<sub>h</sub>).
- The `@FMN` duration goes to the descriptor's `+16`<sub>h</sub>, and to `+18`<sub>h</sub> unless state `+96`<sub>h</sub> bit 6 is
  set.
- `0041B650` starts a channel and `0041A470(slot, @FMW, frame)` moves its pair of keys forward until
  the next key's frame is past the requested frame.
- The values are written to the bone and every bone linked through `+278`<sub>h</sub>: `00418650` into bone
  `+190`<sub>h</sub>, `00418700` into `+1B0`<sub>h</sub> and `004186A0` into `+1D0`<sub>h</sub>, the last skipped while bone byte
  `+280`<sub>h</sub> bit 1 is set.

### Stepping a channel

A channel slot keeps the current key's frame at `+04`<sub>h</sub>, the next key's frame at `+06`<sub>h</sub>, the
previous and next values at `+08`<sub>h</sub> and `+0C`<sub>h</sub>, and two stream cursors, one for frames (`+10`<sub>h</sub>)
and one for values (`+16`<sub>h</sub>): byte offset in the stream, element in the run, stream number and step
count. A stream's flag byte also gives the run length in its low six bits: a run holds that many
literals, or one when bit 6 is set, of one or two bytes by bit 7, and the cursor moves past the run
when its element reaches the length.

- In the packed form `0041BA10` steps the frame cursor and `0041BC40` the value cursor, moving to
  the next stream of the channel at the end of one; in the table form `0041B920` and `0041BB00` do
  the same, with `0041B460` decoding a frame delta and `0041B3A0` a value (`literal × scale +
  previous`).
- `0041A7F0(slot, @FMW)` reads the first frame delta of a channel; a delta of 0 marks the channel as
  a single key (`+04`<sub>h</sub> = `FFFF`<sub>h</sub>).
- `0041A8E0(slot, @FMW, frame)` moves the key pair forward until the next key is past `frame`, and
  also marks the channel single when its two key frames meet.

### Applying a frame

`0041ADA0(stream, …, entry, frame)`, from the seek `0041C850`, puts an entry at a frame: the frame
modulo the `@FMN` duration (`+50`<sub>h</sub>) becomes the entry's `+0C`<sub>h</sub>, every channel moves there
(`0041A8E0`), and the bones are written. `00418880(stream, entry)`, from the walker, does the same
work each frame for a playing entry (bit 1 of `+08`<sub>h</sub>) whose word `+0A`<sub>h</sub> is 1. Both take the bones
from the model's bone array (`0020E600` of model `+84`<sub>h</sub>, `290`<sub>h</sub> bytes a bone) and the channel rows
from the owner's `+2B8`<sub>h</sub> block (`108`<sub>h</sub> bytes a row, count `+2BC`<sub>h</sub>).

`00418880` adds `001ED020(name, …)` to the frame it applies, `name` being the text at `+3C`<sub>h</sub> of
the block the stream's `+2E0`<sub>h</sub> points to. The answer is 0 except in 60 fps mode (`01F82E38`)
during an event (`001EC560`): 0.5 at story progress `15AE`<sub>h</sub> (`00265270`) with the marked event
slot's count (`01DFE40C`, `01F832B0`) at 1 and `g0111` in the name, and −1.0 at progress `15E0`<sub>h</sub>
with the count at 15 and `c1006` in the name.

At frame 0 `00418880` writes, for each row with a bone, the first value of each of the nine
channels the record's mask names and that has data (`0041A7F0`, then `00418650`, `00418700` or
`004186A0`), or the channel's bias from the `@FMW` table at `+54`<sub>h</sub> when it has none, after clearing bit 0 of
the bone's byte `+28A`<sub>h</sub>. A bone whose byte `+28A`<sub>h</sub> is 0 takes its rest pose from the skeleton
instead (`0041D6F0`: `00409270` finds the node for the bone's `+27E`<sub>h</sub> and `00409300` reads it, all
of it into `+C0`<sub>h</sub> when bone `+28B`<sub>h</sub> bit 2 is set, else only the translation into `+F0`<sub>h</sub>).

`0041D180` copies the 48-byte template `02CA43D0` into a bone's `+C0`<sub>h</sub> block; both appliers use
it before rebuilding a pose. For a packed motion, `0041BDC0` restarts, in every row, each channel
the mask names through `0041B650` at frame 0, and clears bit 7 of the entry's `+96`<sub>h</sub>. With the entry's `+96`<sub>h</sub> bit 4 set, `0041C260` (from `0041BEE0`) keeps each bone's current
rotation `+C0`<sub>h</sub> (through `0046D730`) at `+120`<sub>h</sub> and the 32 bytes from `+F0`<sub>h</sub> at `+130`<sub>h</sub>, or
only clears bit 10 of the descriptor when that bit is set; with bit 5 set, `0041C200` clears bit 4
of each bone's word `+280`<sub>h</sub>.

### Blending into a new motion

While the entry's `+96`<sub>h</sub> bit `10`<sub>h</sub> is set, `00418880` cross-fades each bone whose `+28B`<sub>h</sub> bit `2`<sub>h</sub>
is set. The progress `+98`<sub>h</sub> advances each frame by `[01DFE0BC]` × `+9C`<sub>h</sub>, and the blend ends (bit `10`<sub>h</sub>
cleared) once it passes 1.0. The weight is `+98`<sub>h</sub> itself when the stream's word `+358`<sub>h</sub> is 16 (the value
authored command `08`<sub>h</sub> stores); otherwise it is `+98`<sub>h</sub> through the easing curve that the words `+358`<sub>h</sub>
and `+35A`<sub>h</sub> (stored by command `2C`<sub>h</sub>) select: `0046FAE0(+98h, +358h, +35Ah)` (`004189A4`) reads
`01F20E60 + ((a × 3 + b) × 1E0h)`, 120 floats per curve at 60 fps.

It turns the rotation channels into a matrix (`0046D380`, three angles through the sine table
`01F004E0`, 32,768 entries) and that into a quaternion at bone `+110`<sub>h</sub> (`0046D730`, normalised by
`00476E70`, which falls back to (0.57735, 0.57735, 0.57735, 0) for a zero quaternion).

It interpolates from the pose kept at `+120`<sub>h</sub> toward it with `00476F40`, a spherical interpolation
that takes the shorter arc. It copies the start instead when the sine-table value for the angle is 0
or the dot product exceeds 1. It writes the result as the rotation of `+C0`<sub>h</sub> (`00477130`) and mixes
the translation: `+F0`<sub>h</sub> = weight × `+1B0`<sub>h</sub> + (1 − weight) × `+130`<sub>h</sub>, with w = 1.

With the entry's `+96`<sub>h</sub> bit 5 set instead, the quaternion goes to bone `+1A0`<sub>h</sub> and bit 4 of the
bone's word `+280`<sub>h</sub> is raised. Otherwise the channels build the matrix `02CA43D0`, which
`0041D180` copies into the bone's `+C0`<sub>h</sub>, with the translation copied from `+1B0`<sub>h</sub>.

The other matrix helpers of this code are `0046D120` (identity), `0046D2A0(m, a)` (identity with
the 2 × 2 rotation by `a` in its first two rows), `0046D360` (`00202B90`, then w = 1),
`0046D950(m, axis, a)` (rotation by `a` about an axis), and `0046D8E0` / `0046D920`, which store a
vector times the matrix's `+3C`<sub>h</sub> into its translation row, with or without w.

## Modding notes

- An `@FEF` model also needs its path in the `02B64380` table; that table is filled by code, so a new
  `@FEF` model has no entry.
- Binding the model row passes the embedded `EFX0010` only to the empty routine `0016D6A0`.
- Keep each `@FMN` paired with an `@FMW` of the same name; the track binds both by name.
- Keep every `@FMN` record 22 bytes and its mask bits matching the `8000`<sub>h</sub> markers.
- A packed channel's frame count byte equals the motion's duration in every shipped file; keep them
  equal.
- In a version-1 `.ca`, the command block for motion n of row r sits at slot `80 × r + n`.

## Related

- [Model files](model-files-cm-ca.md): the containers, the model row and the event map.
- [Resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md): effect tickets and effect contexts.
- [Resource sections](../Game-Files-And-Data-Tables/resource-sections.md): the `@FRP` child selector `004090D0`.
- [Authored presentation commands](authored-presentation-commands.md): the commands inside `@FMC`.
- [Effect files](effect-files-efx-efb.md): the `EFX0010` format.
