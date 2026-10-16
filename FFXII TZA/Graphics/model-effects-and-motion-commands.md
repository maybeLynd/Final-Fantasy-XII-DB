---
title: "Model effects and motion commands: @FEF and the motion entries"
kind: "format"
category: "Graphics"
summary: "The entries of the .cm and .ca containers that are behaviour rather than shape: the @FEF section that embeds an EFX0010 effect in 144 models, how the model row binds it and the start-up table that names the 144 files, and the motion entries @FMC (command blocks), @FMN (bone channel lists), @FMW (keyed channel data) and @FRM, with the readers that select and decode them and the shipped census."
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
| `00` | `'@FEF',` | u32 | kind 0, u32 length, u32 1 |
| `10` | `char[32]` | the container's name |  |
| `30` | `a` | complete | EFX0010 effect file: u32 +`0x08` = 1.0f, u32 +`0x0C` = entry length - `0x30` |

### @FMC, the command block

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `04` | `u32` | 1 (0x10001 in 405 of the 32,151 entries) |  |
| `0C` | `u32` | record count |  |
| `10` | `char[32]` | the command block's name (weapon_ready, treasure_open, ...) |  |
| `30` | `records,` | each: |  |
| `00` | `u8` | 1 for the block's main record |  |
| `03` | `u8` | sub-record count |  |
| `04` | `u16` | record length |  |
| `06` | `sub-records:` | u16 | key, u16 (length << 6 \| command count), then the commands |

A key of `0xFFFF` marks the block of commands that `0041CD30` runs before the keyed ones; the other
keys are motion frames. The commands themselves are the authored presentation commands
([authored-presentation-commands.md](authored-presentation-commands.md)).

### @FMN, the bone channel list

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `04` | `u32` | kind: 0x02001111 or 0x02001011 |  |
| `0C` | `u32` | record count |  |
| `10` | `char[32]` | the motion's name |  |
| `50` | `u16` | duration in frames |  |
| `F0` | `records` | (the | start `00409190` picks for both kinds), 22 bytes each: |
| `00` | `u16` | node key |  |
| `02` | `u16` | bits 0-8 channel mask, bits 9-14 record length (22) |  |
| `04` | `u16[9]` | channel numbers in the paired @FMW; 0x8000 \| n where the mask bit is clear |  |

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
| `0C` | `u32` | 1 |  |
| `10` | `char[32]` | the .ca file's name |  |
| `30` | `payload:` | byte | +`0x01` to `003E18D0`, byte +`0x02` low six bits to skeleton +`0xA4`, u32 +`0x08` offset of a second region, from the payload (0 = none) |

### The version-1 .ca slot table

`+0x30` holds 80 (the columns) and `+0x34` the rows. `004090D0(container, row, column)` returns the
entry at slot `row × 80 + column` when the row is below `+0x34`, otherwise slot `column`; an empty
slot gives NULL. The `@FMC` blocks fill the first `80 × rows` slots and `@FRM` is the last slot.

## Shipped data

| Fact | Value |
|---|---|
| `@FEF` | 144 `.cm` files: 82 monsters, 27 NPCs, 26 summons, 9 gadgets; always entry 6 of 7; all start `EFX0010` with the size word equal to the entry length − `0x30` |
| `02B64380` paths | 144, set by `0040A230`; each slot is the fold of its file's name, and the 144 paths are exactly the 144 `@FEF` files |
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

- `00504F00` binds the `@FEF` section at model row `+0x228` with `00504E70`, which falls back to a
  bank-wide search by tag and name when the model's own entry has none.
- `00504940` stores the section pointer at row `+0x230` and calls `0016D6A0(ticket, section + 0x30)`
  with the bank entry's ticket `+0x44` (`005049BD`). `0016D6A0` is a bare `ret`: binding the row does
  nothing with the embedded effect.
- `0041F340` makes the render record's effect context: when the record's `+0x288` is −1 and the row's
  `@FEF` bank index is set, it calls `003B3550(record, ticket)` and stores the result at record `+0x288`
  and row `+0x240`.
- The registration that makes the ticket indexes the pointer table `02B64380` by the fold of the name.
  `0041E3A0` calls `00409F80` at start-up (`0041E40B`), which calls `0040A230`: 144 stores of
  `PS2Data\obj_finish\in\<folder>\...\<name>.cm` paths, so every shipped `@FEF` model has its entry.

### Selecting a motion

`0041D220(entry, descriptor)` sets up a presentation entry:

- `+0x31C` takes the motion number (descriptor `+0x20`) and `+0x31A` the record's signed byte
  `+0x413` (descriptor `+0x24`);
- the `@FMC` section goes to `+0x320`, or `@FRP` when the entry has no `@FMC`;
- when an `@FRM` exists and is longer than its header, `+0x378` gets its payload offset and `+0x37C`
  the second region's offset;
- `0041CA70` picks the command block `004090D0(container, +0x31A, +0x31C & 0xFFF)` into `+0x368`, and
  `0041CD30` positions each track on its first record, keeping the `0xFFFF` block apart.

The model binder `0041FCF0` also keeps the model's own first `@FMC` index at record `+0x2FA`
(`0041FE83`), which the event map in [model files](model-files-cm-ca.md) adds to.

### Reading the channels

- `0041BEE0` binds `@FMN` (or `@FRP`) and `@FMW` by tag and name into a track descriptor (`+0x54`,
  `+0x58`), and `0041B4E0` resolves the entries.
- It walks the `@FMN` records from the start `00409190` gives, advancing by each record's length.
  `00370E00` turns the node key into a bone, and `0041B550` sets up the record's nine channels in a
  `0x108`-byte row (count at owner `+0x2BC`).
- The `@FMN` duration goes to the descriptor's `+0x16`, and to `+0x18` unless state `+0x96` bit 6 is
  set.
- `0041B650` starts a channel and `0041A470(slot, @FMW, frame)` moves its pair of keys forward until
  the next key's frame is past the requested frame.
- The values are written to the bone and every bone linked through `+0x278`: `00418650` into bone
  `+0x190`, `00418700` into `+0x1B0` and `004186A0` into `+0x1D0`, the last skipped while bone byte
  `+0x280` bit 1 is set.

## Modding notes

- An `@FEF` model also needs its path in the `02B64380` table; that table is filled by code, so a new
  `@FEF` model has no entry.
- Binding the model row passes the embedded `EFX0010` only to the empty routine `0016D6A0`.
- Keep each `@FMN` paired with an `@FMW` of the same name; the track binds both by name.
- Keep every `@FMN` record 22 bytes and its mask bits matching the `0x8000` markers.
- A packed channel's frame count byte equals the motion's duration in every shipped file; keep them
  equal.
- In a version-1 `.ca`, the command block for motion n of row r sits at slot `80 × r + n`.

## Related

- [Model files](model-files-cm-ca.md): the containers, the model row and the event map.
- [Resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md): effect tickets and effect contexts.
- [Resource sections](../Game-Files-And-Data-Tables/resource-sections.md): the `@FRP` child selector `004090D0`.
- [Authored presentation commands](authored-presentation-commands.md): the commands inside `@FMC`.
- [Effect files](effect-files-efx-efb.md): the `EFX0010` format.
