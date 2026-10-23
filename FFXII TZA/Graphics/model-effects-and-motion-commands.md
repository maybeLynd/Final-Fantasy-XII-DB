---
title: "Model effects and motion commands: @FEF and the motion entries"
kind: "format"
category: "Graphics"
addresses: "0x00504F00, 0x00504E70, 0x00504940, 0x0016D6A0, 0x0040A230, 0x00409F80, 0x02B64380, 0x0041F340, 0x003B3550, 0x0041D220, 0x0041CA70, 0x004090D0, 0x0041CD30, 0x0041BEE0, 0x0041B4E0, 0x00409190, 0x00370E00, 0x0041B550, 0x0041B650, 0x00409170, 0x00409150, 0x0041A470, 0x00418650, 0x00418700, 0x004186A0, 0x0041FCF0"
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
The motion entries are read when a presentation entry is set up to play a motion (`0x0041D220`).

## Layouts

### @FEF

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `'@FEF',` | u32 | kind 0, u32 length, u32 1 |
| `+0x10` | `char[32]` | the container's name |  |
| `+0x30` | `a` | complete | EFX0010 effect file: u32 +`0x08` = 1.0f, u32 +`0x0C` = entry length - `0x30` |

### @FMC, the command block

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u32` | 1 (0x10001 in 405 of the 32,151 entries) |  |
| `+0x0C` | `u32` | record count |  |
| `+0x10` | `char[32]` | the command block's name (weapon_ready, treasure_open, ...) |  |
| `+0x30` | `records,` | each: |  |
| `+0x00` | `u8` | 1 for the block's main record |  |
| `+0x03` | `u8` | sub-record count |  |
| `+0x04` | `u16` | record length |  |
| `+0x06` | `sub-records:` | u16 | key, u16 (length << 6 \| command count), then the commands |

A key of `0xFFFF` marks the block of commands that `0x0041CD30` runs before the keyed ones; the other
keys are motion frames. The commands themselves are the authored presentation commands
([authored-presentation-commands.md](authored-presentation-commands.md)).

### @FMN, the bone channel list

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u32` | kind: 0x02001111 or 0x02001011 |  |
| `+0x0C` | `u32` | record count |  |
| `+0x10` | `char[32]` | the motion's name |  |
| `+0x50` | `u16` | duration in frames |  |
| `+0xF0` | `records` | (the | start `0x00409190` picks for both kinds), 22 bytes each: |
| `+0x00` | `u16` | node key |  |
| `+0x02` | `u16` | bits 0-8 channel mask, bits 9-14 record length (22) |  |
| `+0x04` | `u16[9]` | channel numbers in the paired @FMW; 0x8000 \| n where the mask bit is clear |  |

### @FMW, the channel data

```
+0x0C  u32  channel count
+0x30  u32  offset of the value streams, from the entry
+0x34  u32  1 = packed form (u16 channel table, 0x00409170); otherwise the u32 table form (0x00409150)
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
| `+0x0C` | `u32` | 1 |  |
| `+0x10` | `char[32]` | the .ca file's name |  |
| `+0x30` | `payload:` | byte | +`0x01` to `0x003E18D0`, byte +`0x02` low six bits to skeleton +`0xA4`, u32 +`0x08` offset of a second region, from the payload (0 = none) |

### The version-1 .ca slot table

`+0x30` holds 80 (the columns) and `+0x34` the rows. `0x004090D0(container, row, column)` returns the
entry at slot `row × 80 + column` when the row is below `+0x34`, otherwise slot `column`; an empty
slot gives NULL. The `@FMC` blocks fill the first `80 × rows` slots and `@FRM` is the last slot.

## Shipped data

| Fact | Value |
|---|---|
| `@FEF` | 144 `.cm` files: 82 monsters, 27 NPCs, 26 summons, 9 gadgets; always entry 6 of 7; all start `EFX0010` with the size word equal to the entry length − `0x30` |
| `0x02B64380` paths | 144, set by `0x0040A230`; each slot is the fold of its file's name, and the 144 paths are exactly the 144 `@FEF` files |
| `.cm` motion entries | 45 files (29 weapons, 16 treasures); 209 `@FMC`, 111 `@FMN`, 111 `@FMW` |
| `.cm` command block names | every weapon: `weapon_shot`, `weapon_deact`, `weapon_active`, `weapon_ready`, `weapon_rlx_ready`; every treasure: `treasure_dead`, `treasure_ready`, `treasure_open`, `treasure_opened` |
| `.ca` entries | 31,942 `@FMC`, 18,303 `@FMN`, 18,303 `@FMW`, 3,164 `@FRM` (one per file, named after it) |
| version-1 `.ca` | 1,195; 80 columns in all; 1 row in 1,150, 3 in 45; `@FRM` in the last slot in all |
| `@FMN` records | 746,592, all 22 bytes, bit 15 clear, mask bits matching the `0x8000` markers in all; no stream runs past its entry |
| `@FMW` form | packed in 110 `.cm` and 17,576 `.ca` entries, table form in 1 `.cm` and 727 `.ca` |
| frame counts | the first byte of each of the 1,446,602 packed channel descriptors equals the paired `@FMN` duration's low byte |
| `@FRM` payload | byte `+0x01` 1 in 2,977, 2 in 169, 4 in 18; second region present in 2,847 |

## Loader behaviour

### Binding @FEF

- `0x00504F00` binds the `@FEF` section at model row `+0x228` with `0x00504E70`, which falls back to a
  bank-wide search by tag and name when the model's own entry has none.
- `0x00504940` stores the section pointer at row `+0x230` and calls `0x0016D6A0(ticket, section + 0x30)`
  with the bank entry's ticket `+0x44` (`0x005049BD`). `0x0016D6A0` is a bare `ret`: binding the row does
  nothing with the embedded effect.
- `0x0041F340` makes the render record's effect context: when the record's `+0x288` is −1 and the row's
  `@FEF` bank index is set, it calls `0x003B3550(record, ticket)` and stores the result at record `+0x288`
  and row `+0x240`.

- `0x0041F340` takes its blocks in arena 6 through `0x003AB8B0(size, mode)` (`0x0036A100` for mode 0,
  `0x0036B160` for mode 1) and returns them through `0x003AB910`, which calls `0x0036C620` for a null or
  4-byte-aligned pointer and `0x0036C5D0` otherwise.

### The record's effect handle

The handle at record `+0x288` names a `0x38`-byte slot at `0x02EBD480 + (handle & 0x3F) × 0x38`; every
helper below first checks that the slot's id equals the handle and does nothing otherwise. The slot's
`+0x10` is the effect instance and its byte `+0x30` holds three flags.

- `0x003B3400`, from `0x003B3550`, takes the head of the free list `0x02EBDBA0`, appends the slot to the
  used list (`0x02EBDB98` / `0x02EBDBA8`) and writes a new serial (`0x02EBDBB4`) into bits 6–27 of the id.
- `0x003B3300(handle)`, from `0x0041E860`, ends the instance (`0x0024EE60`), moves the slot back to the
  free list, keeps only bits 0–5 and 28–31 of the id and clears `+0x10`.
- `0x003B3080(handle)` sets bit 0 of `+0x30`. The update pass `0x0024B9B0` holds a kind-3 instance on any
  step the bit is clear in the slot its dword `+4` names, and clears the bit when it is set; `0x0042D830` sets it each time
  it processes the record, so a model's effect advances only while its character does.
- `0x003B33A0(handle, b)` sets bit 1 of `+0x30` and stores `b` in bit 2; `0x0042D830` passes the
  result of `0x00420FB0` when `0x004210D0` allows it.
- `0x003B3AA0(handle, v)` stores the vector at instance `+0x320` with w = 1, or 1, 1, 1, 1 when the
  instance's `+0x368` bit `0x4000` is set; `0x0042D830` passes the vector from `0x003E5710`.
- `0x003B30D0(handle, a, b)` sets the instance's two tint colours `+0x398` (from `a`) and `+0x334`
  (from `b`) with their red, green and blue at `0x80`, and raises `+0x368` bit `0x8`; when the
  instance's `+0x36A` bit `0x8` is set, it also puts both alphas at `0x80` and drops the bit again.
- `0x003B30A0(handle, v)` stores `v` at instance `+0x08`, and `0x003B3CA0(handle, v)` runs `0x003A9490(v)`
  on the instance, then makes the previous instance current again.

- The registration that makes the ticket indexes the pointer table `0x02B64380` by the fold of the name.
  `0x0041E3A0` calls `0x00409F80` at start-up (`0x0041E40B`), which calls `0x0040A230`: 144 stores of
  `PS2Data\obj_finish\in\<folder>\...\<name>.cm` paths, so every shipped `@FEF` model has its entry.

### The @FEF path table

`0x02B64380` is a table of 8-byte path pointers indexed by a fold of a model's name. For a name that ends in a letter
and four digits, the slot is `0x500` times the letter's character code plus the four digits read as a decimal
number: `m1006` folds to `0x500 × 0x6D + 1006` = 140,526, the slot `0x02C76AF0`. `0x0040A230` stores each of the 144
`.cm` paths of the shipped `@FEF` models in the slot its name folds to.

The registration `0x00409FE0`
([resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md)) reads it. For a file with an
`@FEF` section it folds the last five characters of the file's name (`0x0040A0C0`-`0x0040A129`) and loads that slot
(`0x0040A12C`). It passes the path to `0x001D6EC0` (`0x0040A17F`), which returns the character-effect path that the
async-load manager keeps for the same `.cm` (`0x001A09E0`); the number after `chara\h` in that path goes into the
ticket (`0x003B3B10`, `0x0040A1C4`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| each row of [model-effects-and-motion-commands-state.tsv](model-effects-and-motion-commands-state.tsv): the 144 filled slots of `0x02B64380` | `void*` | 0 (zero-filled tail of `.data`) | the `.cm` path of the model whose name folds to the slot: the row's `index`, `name`, `folder` and `path`, with `literal` the address of the string | `0x0040A230`, once at start-up, at the site in `set_by` | `0x00409FE0` (`0x0040A12C`), for the model being registered |

### Selecting a motion

`0x0041D220(entry, descriptor)` sets up a presentation entry:

- `+0x31C` takes the motion number (descriptor `+0x20`) and `+0x31A` the record's signed byte
  `+0x413` (descriptor `+0x24`);
- the `@FMC` section goes to `+0x320`, or `@FRP` when the entry has no `@FMC`;
- when an `@FRM` exists and is longer than its header, `+0x378` gets its payload offset and `+0x37C`
  the second region's offset;
- `0x0041CA70` picks the command block `0x004090D0(container, +0x31A, +0x31C & 0xFFF)` into `+0x368`, and
  `0x0041CD30` positions each track on its first record, keeping the `0xFFFF` block apart.

The model binder `0x0041FCF0` also keeps the model's own first `@FMC` index at record `+0x2FA`
(`0x0041FE83`), which the event map in [model files](model-files-cm-ca.md) adds to.

### Reading the channels

- `0x0041BEE0` binds `@FMN` (or `@FRP`) and `@FMW` by tag and name into a track descriptor (`+0x54`,
  `+0x58`), and `0x0041B4E0` resolves the entries.
- It walks the `@FMN` records from the start `0x00409190` gives, advancing by each record's length.
  `0x00370E00` turns the node key into a bone, and `0x0041B550` sets up the record's nine channels in a
  `0x108`-byte row (count at owner `+0x2BC`).
- The `@FMN` duration goes to the descriptor's `+0x16`, and to `+0x18` unless state `+0x96` bit 6 is
  set.
- `0x0041B650` starts a channel and `0x0041A470(slot, @FMW, frame)` moves its pair of keys forward until
  the next key's frame is past the requested frame.
- The values are written to the bone and every bone linked through `+0x278`: `0x00418650` into bone
  `+0x190`, `0x00418700` into `+0x1B0` and `0x004186A0` into `+0x1D0`, the last skipped while bone byte
  `+0x280` bit 1 is set.

### Stepping a channel

A channel slot keeps the current key's frame at `+0x04`, the next key's frame at `+0x06`, the
previous and next values at `+0x08` and `+0x0C`, and two stream cursors, one for frames (`+0x10`)
and one for values (`+0x16`): byte offset in the stream, element in the run, stream number and step
count. A stream's flag byte also gives the run length in its low six bits: a run holds that many
literals, or one when bit 6 is set, of one or two bytes by bit 7, and the cursor moves past the run
when its element reaches the length.

- In the packed form `0x0041BA10` steps the frame cursor and `0x0041BC40` the value cursor, moving to
  the next stream of the channel at the end of one; in the table form `0x0041B920` and `0x0041BB00` do
  the same, with `0x0041B460` decoding a frame delta and `0x0041B3A0` a value (`literal × scale +
  previous`).
- `0x0041A7F0(slot, @FMW)` reads the first frame delta of a channel; a delta of 0 marks the channel as
  a single key (`+0x04` = `0xFFFF`).
- `0x0041A8E0(slot, @FMW, frame)` moves the key pair forward until the next key is past `frame`, and
  also marks the channel single when its two key frames meet.

### Applying a frame

`0x0041ADA0(stream, …, entry, frame)`, from the seek `0x0041C850`, puts an entry at a frame: the frame
modulo the `@FMN` duration (`+0x50`) becomes the entry's `+0x0C`, every channel moves there
(`0x0041A8E0`), and the bones are written. `0x00418880(stream, entry)`, from the walker, does the same
work each frame for a playing entry (bit 1 of `+0x08`) whose word `+0x0A` is 1. Both take the bones
from the model's bone array (`0x0020E600` of model `+0x84`, `0x290` bytes a bone) and the channel rows
from the owner's `+0x2B8` block (`0x108` bytes a row, count `+0x2BC`).

`0x00418880` adds `0x001ED020(name, …)` to the frame it applies, `name` being the text at `+0x3C` of
the block the stream's `+0x2E0` points to. The answer is 0 except in 60 fps mode (`0x01F82E38`)
during an event (`0x001EC560`): 0.5 at story progress `0x15AE` (`0x00265270`) with the marked event
slot's count (`0x01DFE40C`, `0x01F832B0`) at 1 and `g0111` in the name, and −1.0 at progress `0x15E0`
with the count at 15 and `c1006` in the name.

`0x00418880` also rounds the frame down to a whole frame (`floorf`, `0x004192FE`) in two cases, both only in 60 fps
mode (`0x01F82E38`):

- `0x001ED240(name, motion, id, frame)` answers 1 (`0x004192C9`), with `motion` the stream's text `+0x2EC`. Outside
  an event (`0x001EC560`) it does so at frame 10.5 of `n1120_32` or a `n1129` name and at frame 21 of `m1072_10`.
  During one it checks a fixed list of story progress values (`0x00265270`: `0x177`, `0x222`, `0x262`, `0x33E`,
  `0x560`, `0x6DC`, `0x7C2`, `0x7CE`, `0xD48`, `0xD70`, `0x15AE`, `0x15E0`, `0x1AF4`).
- With those it checks the event slot counts (`0x01DFE40C`, `0x01F832B0`, `0x01F832C4`), names and frames, and, in the
  progress-0 field `0x112` and elsewhere, the effect names `mrm_g0100`, `bds_f0100`, `sum_j0001`, `sum_a0001`,
  `sum_f0001` and `sum_i0001` (`0x001C50C0`).
- The frame is one frame step (`0x01DFE0BC`) before the end `+0x16` and `0x001EC6B0(motion)` finds `m1009`, `m1266`,
  `m1222`, `m1223`, `m1151` or `m1267` in the motion's name.

At frame 0 `0x00418880` writes, for each row with a bone, the first value of each of the nine
channels the record's mask names and that has data (`0x0041A7F0`, then `0x00418650`, `0x00418700` or
`0x004186A0`), or the channel's bias from the `@FMW` table at `+0x54` when it has none, after clearing bit 0 of
the bone's byte `+0x28A`; it clears that bit on the non-zero-frame path too (`0x004194B7`).

A bone whose byte `+0x28A` is 0 takes its rest pose from the skeleton
instead (`0x0041D6F0`: `0x00409270` finds the node for the bone's `+0x27E` and `0x00409300` reads it, all
of it into `+0xC0` when bone `+0x28B` bit 2 is set, else only the translation into `+0xF0`).

`0x0041D180` copies the 48-byte template `0x02CA43D0` into a bone's `+0xC0` block; both appliers use
it before rebuilding a pose. For a packed motion, `0x0041BDC0` restarts, in every row, each channel
the mask names through `0x0041B650` at frame 0, and clears bit 7 of the entry's `+0x96`. With the entry's `+0x96` bit 4 set, `0x0041C260` (from `0x0041BEE0`) keeps each bone's current
rotation `+0xC0` (through `0x0046D730`) at `+0x120` and the 32 bytes from `+0xF0` at `+0x130`, or
only clears bit 10 of the descriptor when that bit is set; with bit 5 set, `0x0041C200` clears bit 4
of each bone's word `+0x280`.

### Blending into a new motion

While the entry's `+0x96` bit `0x10` is set, `0x00418880` cross-fades each bone whose `+0x28B` bit `0x2`
is set. The progress `+0x98` advances each frame by `[0x01DFE0BC]` × `+0x9C`, and the blend ends (bit `0x10`
cleared) once it passes 1.0. The weight is `+0x98` itself when the stream's word `+0x358` is 16 (the value
authored command `0x08` stores); otherwise it is `+0x98` through the easing curve that the words `+0x358`
and `+0x35A` (stored by command `0x2C`) select: `0x0046FAE0(+0x98, +0x358, +0x35A)` (`0x004189A4`) reads
`0x01F20E60 + ((a × 3 + b) × 0x1E0)`, 120 floats per curve at 60 fps.

It turns the rotation channels into a matrix (`0x0046D380`, three angles through the sine table
`0x01F004E0`, 32,768 entries) and that into a quaternion at bone `+0x110` (`0x0046D730`, normalised by
`0x00476E70`, which falls back to (0.57735, 0.57735, 0.57735, 0) for a zero quaternion).

It interpolates from the pose kept at `+0x120` toward it with `0x00476F40`, a spherical interpolation
that takes the shorter arc. It copies the start instead when the sine-table value for the angle is 0
or the dot product exceeds 1. It writes the result as the rotation of `+0xC0` (`0x00477130`) and mixes
the translation: `+0xF0` = weight × `+0x1B0` + (1 − weight) × `+0x130`, with w = 1.

With the entry's `+0x96` bit 5 set instead, the quaternion goes to bone `+0x1A0` and bit 4 of the
bone's word `+0x280` is raised. Otherwise the channels build the matrix `0x02CA43D0`, which
`0x0041D180` copies into the bone's `+0xC0`, with the translation copied from `+0x1B0`.

The other matrix helpers of this code are `0x0046D120` (identity), `0x0046D2A0(m, a)` (identity with
the 2 × 2 rotation by `a` in its first two rows), `0x0046D360` (`0x00202B90`, then w = 1),
`0x0046D950(m, axis, a)` (rotation by `a` about an axis), and `0x0046D8E0` / `0x0046D920`, which store a
vector times the matrix's `+0x3C` into its translation row, with or without w.

## Modding notes

- An `@FEF` model also needs its path in the `0x02B64380` table; that table is filled by code, so a new
  `@FEF` model has no entry.
- Binding the model row passes the embedded `EFX0010` only to the empty routine `0x0016D6A0`.
- Keep each `@FMN` paired with an `@FMW` of the same name; the track binds both by name.
- Keep every `@FMN` record 22 bytes and its mask bits matching the `0x8000` markers.
- A packed channel's frame count byte equals the motion's duration in every shipped file; keep them
  equal.
- In a version-1 `.ca`, the command block for motion n of row r sits at slot `80 × r + n`.

## Related

- [Model files](model-files-cm-ca.md): the containers, the model row and the event map.
- [Resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md): effect tickets and effect contexts.
- [Resource sections](../Game-Files-And-Data-Tables/resource-sections.md): the `@FRP` child selector `0x004090D0`.
- [Authored presentation commands](authored-presentation-commands.md): the commands inside `@FMC`.
- [Effect files](effect-files-efx-efb.md): the `EFX0010` format.
