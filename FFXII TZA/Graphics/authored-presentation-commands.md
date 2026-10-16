---
title: "Authored presentation commands: the command handlers and their ramp channels"
kind: "system"
category: "Graphics"
summary: "The presentation commands authored in model and motion data and run on a character's render record: how the stream is walked and dispatched through the pair table and the two handler banks, what each registered handler does, and the five ramp channels that commands 0x0D to 0x10 drive on the character's shadow entry, with the tick that advances them and the shadow build that consumes them."
addresses: ["0041DA90", "01EFFAF0", "02CA4410", "02CA4670", "0041D6C0", "0041D6D0", "0041CCA0", "004269A0", "002EA320", "002EA5F0", "00417AD0", "00417C60", "004173D0", "00417440", "00417460", "004174D0", "00426870", "00520800", "02B40528", "003B6890", "003B6A90", "003B69B0", "003B6A10", "003B6950", "003B5890", "003B5C00", "003B5D40", "003B62D0", "02B40524", "003B6930"]
---

# Authored presentation commands: the command handlers and their ramp channels

## What the player sees

As a character's motion plays, small commands authored in the motion data fire at set points:
footstep sounds and dust, character sounds, weapon trails switching on and off, a weapon moving
between hand and sheath, a sway or a rotator speeding up, and the character's shadow sliding,
turning, stretching and fading over a number of frames. These commands are all run by the code on
this page.

## How it works

### Walking the stream

`0041DA90(entry, stream)` runs the commands of the stream's current block. The block is at
`[stream + 0x368] + [entry + 0x90]`; its byte `+2 & 0x3F` is the command count and the commands start
at `+4`. Each command begins with a word whose bits 0 to 6 are the id and bits 7 to 15 the command's
length in bytes, which is how the walk steps to the next (`0041DB6A`). Nothing runs unless bit 20 of
the stream's `+0x0C` is set. With bit 4 of `+0x0C` also set, a command whose pair-table flag is set is
skipped (`0041DB37`).

The id is clamped to `0x4B` (`0041DB25`) and the command is dispatched through the pair table:
`call [01EFFAF0 + id x 16]` with the command in `rcx`, the entry in `rdx` and the stream in `r8`
(`0041DB66`).

### The pair table

`01EFFAF0` holds 76 entries of `{ invoker, flag }`:

| Invoker kind | Ids |
|---|---|
| a generic thunk that loads its own slot of bank `02CA4410` and jumps to it with the render record `[stream + 0x2E0]` in `rcx` and the command in `rdx`; it returns when the slot is empty | `0x11` to `0x16`, `0x18` to `0x1A`, `0x1D` to `0x21`, `0x23` to `0x26`, `0x28` to `0x2A`, `0x2F`, `0x34`, `0x3F`, `0x48` (25) |
| a bespoke invoker | `0x00`, `0x01`, `0x03`, `0x04`, `0x05`, `0x06`, `0x08`, `0x09`, `0x0A`, `0x0B`, `0x0D` to `0x10`, `0x2C` (15) |
| `0016D6A0`, which returns 0 | 33 ids |
| null | `0x49`, `0x4A`, `0x4B` |

Because of the clamp, a command id from `0x49` to `0x7F` calls address 0.

### The two banks

Bank A `02CA4410` and bank B `02CA4670` hold 75 pointers each; `0041CCA0` clears both. `0041D6C0(id, fn)`
stores into bank A and `0041D6D0(id, fn)` into bank B.

`004269A0`, the character render system's start-up, stores 24 handlers in bank A and one, id 5, in
bank B (`00426A12` to `00426B84`). The actor side's `002EA320` and `002EA5F0` store ids 4
(`002E70C0`), 5 (`0016D6A0`), 6 (`002E7090`), `0x0C` (`002E70A0`) and `0x26` (`002E7080`) in bank A.

### The bespoke invokers that use the banks

- Id 4, `00417AD0`, switches on the command's byte `+2`: subtype 1 calls bank-A slot 4 with the actor
  `[stream + 0x2C0]` four times, tagged `0x80` to `0x83`; subtype 2 sets bit 21 and subtype 4 bit 15
  of the stream's `+0x0C` before the call; subtypes 10 and 11 set bits 1 and 0 of the render record's
  `+0x419`; subtype 12 queries the record (`0041F2F0`) and may call `00423F20`. It ends by setting bit
  4 of the stream's `+0x2C8`.
- Id 5, `00417C60`, calls bank-A slot 5 with the actor, then bank-B slot 5 with the render record,
  then sets bit 5 of `+0x2C8`. Bank-A slot 5 is the empty `0016D6A0`, so the command is the
  character sound.
- Id 6, `00417CC0`, calls bank-A slot 6 with the actor and sets bit 6 of `+0x2C8`.
- Slot `0x0C` is not in the pair table; `0041DA90` calls it with the actor and `stream + 0x31C` when
  the motion reaches the time at `+0x34C`.
- Ids `0x0D` to `0x10` are the ramp setters below.

### The registered handlers

Each handler takes the render record and the command:

| Id | Handler | What it does |
|---|---|---|
| `0x05` (bank B) | `00520C50` | plays a sound on the record's emitter `+0x5F0` (`0046CBA0`): word `+2` is mode (bits 12 to 15) and type |
| `0x11` | `00520160` | stores byte `+2` at `+0x3D0` and raises bit 24 of `+0x294`: weapon trails on or off |
| `0x12` | `005207C0` | `003E29F0(003E6DA0(), 4, byte +2 != 0)`: the look-tracking switch of [Character rig and look](character-rig-and-look.md) |
| `0x13` | `00520430` | stores the controller switch (bytes `+2`, `+3`, word `+4` to `+0x3F4` to `+0x3F6`) and broadcasts it (`00429500`), holding bit 9 of `+0x290` meanwhile; byte `+2 & 0xB9 == 0x80` takes the `004288B0` / `0042B580` arm |
| `0x14` | `00520E70` | applies `00521050` to the record's entity and its sub-tree (`00426870`) |
| `0x15` | `00520740` | byte `+2` to bits 0 to 2 and byte `+3` to bits 3 to 5 of `+0x3D1`, and raises bit 23 of `+0x290` |
| `0x16` | `00520BD0` | bit 0 of word `+2` to `+0x3D2`, its upper bits to `+0x3D3`, word `+4` to `+0x3F8`, then `0042B550` |
| `0x18` | `00520C80` | `003B0C50(record index, byte +2)` when `00421E20` finds the record's special bone `0x100` |
| `0x19` | `00520CE0` | a type-1 sound on the emitter, mode 0 (`0046CC70`) |
| `0x1A` | `00520C10` | movement along profile word `+2` (`003E6340`) when the entity has a `+0x370` object |
| `0x1D` | `00520D30` | the pose-sequencer event: byte `+2` low nibble the event, high nibble a record filter, byte `+3` the choice; `0xFD` sets bit 6 of `+0x4B7`, `0xFE` calls `00428B30`, `0xFF` stores byte `+3` in the model instance `+0xB8` |
| `0x1E` | `00520DF0` | with the same filter, calls `003E6A20` with byte `+2 & 0xF` |
| `0x1F` | `00520140` | `003E6710` with bit 0 of word `+2` |
| `0x20` | `005207A0` | `+0x2F4` = `0x303 + (word +2 != 0)` |
| `0x21` | `00520780` | `+0x2F6` = `0x305 + (word +2 != 0)` |
| `0x23` | `00520180` | the fade forwarder `004293C0` with dword `+4`, word `+8` and word `+2` |
| `0x24` | `005201B0` | ramps rotator word `+2` to the speed float `+8` over word `+4` frames (`003DFE70`); word `+6` with bits 7 and 6 sends it to another controller |
| `0x25` | `00520320` | the rotator back to its default speed |
| `0x28` | `00520720` | `003E6AA0`: dword `+4` into bits 27 to 31 of `+0x304`, dirty bit 27 of `+0x294` |
| `0x29` | `00520D00` | the same sound with the volume in word `+2` (`0046CC70`) |
| `0x2A` | `005206B0` | `003E7140` with the three floats `+8` to `+0x10` |
| `0x2F` | `00520E30` | sends event word `+2` with bit `0x2000` set to the child sub-tree (`0042EF90`, `00521000`) |
| `0x34` | `00520800` | the shadow command, below |
| `0x3F` | `00520510` | on a record with no parent, applies `00520E90` to it and its sub-tree with a bone (word `+2`), a direction (floats `+4` to `+0xC`), a preset (word `+0x10 & 0xFFF`, 0 when the bone is -1) and a flag (bit 15 of word `+0x10`) |
| `0x48` | `005205B0` | as `0x3F`, with the target found by name (`00372800`) |

`00426870(index, fn, arg)` calls `fn` on the record at `022C6F28 + index x 0x740` at once and, when
its first child `+8` is not -1, walks the children with `0042EF90`.

### The shadow command, 0x34

`00520800` with byte `+2 = 0xFF` switches both shadow pools: byte `+3` non-zero calls `003AFD30(1)` and
`003B6930(4)`, zero calls `003AFD30(0)` and `003B6930(6)`. Any other byte `+2` acts on the record's
second-pool entry (`+0x118`, through `003AFC10`), one arm per bit:

| Byte `+2` | Effect, value = float `+4`, frames = byte `+3` |
|---|---|
| `0x01`, `0x02`, `0x04` | ramp `+0x24`, `+0x28` or `+0x34` to the value over the frames (below 2: at once) |
| `0x08` | `+0x1F` low bits: 2 when byte `+3` is set, else 1 |
| `0x10` | `+0x1F` high bits: `0x20` when byte `+3` is set, else `0x10` |
| `0x20`, `0x40` | ramp `+0x3C` or `+0x44` the same way |
| `0x80` | byte `+3` = 1: `+0x40` = value; 2: bit 1 of `+0x58` and `+0x56` = `0x40`, `0x80` or `0x100` for values up to 1.5, 2.5 or above; 4: bit 0 of `+0x58` and `+0x50` = value |

### The ramp channels

Commands `0x0D` to `0x10` animate the character's first-pool shadow entry. Their invokers take the
entry's handle from `+0x35C` of the presentation entry and do nothing when it is -1; the step count is
the command's byte `+2`.

| Command | Invoker | Setter | Counter | Value | Step |
|---|---|---|---|---|---|
| `0x0D` | `004173D0` | `003B6A90` | `+0x00` | `+0x50`, `+0x54` | `+0x60`, `+0x64` |
| `0x0E` | `00417440` (tail jump) | `003B69B0` | `+0x01` | `+0x70` | `+0x74` |
| `0x0F` | `00417460` | `003B6A10` | `+0x02` | `+0x58`, `+0x5C` | `+0x68`, `+0x6C` |
| `0x10` | `004174D0` (tail jump) | `003B6950` | `+0x03` | `+0x78` | `+0x7C` |

The pair commands pass the floats `+4` and `+8`; the single ones pass float `+4`. A setter:

1. finds the slot `[02B40528] + (handle & 0xFF) x 0xE0` and returns without writing when its `+0x10`
   is not the handle;
2. with 0 steps, stores the value and clears the counter, which cancels a running ramp;
3. otherwise stores the count and the step `(target - current) x (1 / steps)`, computing the
   reciprocal first (`003B69E8`, `003B69EC`).

A fifth channel, counter `+0x43`, value `+0x98`, step `+0x9C`, is set by `003B5D40(handle, n)` (from
`0041D560`). It copies the slot's last built values `+0xC0` to `+0xD4` into the blend set `+0x80` to
`+0x94`, sets the counter to `n`, the value to 0 and the step to `1 / n`, and takes the first step at
once: a cross-fade from the previous shadow to the new one over `n` steps.

### Advancing the channels

`003B5890`, called once per character-update pass from `00426090` (`00426112`), walks all 160 slots.
A slot advances when bit 0 of `+0x40` is set and bit 0 of `+0x41 | [02B40524]` is clear. It steps the
channels in the order `+0x00`, `+0x02`, `+0x01`, `+0x03`, `+0x43`: each with a non-zero counter adds
its step to its value and decrements the counter. The value is never snapped to the target, so it
ends within float rounding of it. `003B5C00(handle)` applies the same step to one slot without the
pause tests; `0041C850` and `0041D820` call it.

### What the channels drive

`003B62D0` builds the slot's shadow draw record each frame. While counter `+0x43` is non-zero it blends
each channel value with the blend set by a weight from `0046FAE0`. Then:

- `+0x50`, `+0x54` plus `+0x48`, `+0x4C`, times `+0x44`, is an offset from the anchor bone, rotated by
  the character's facing (render record `+0x124`);
- `+0x58`, `+0x5C` multiply the shadow's two extents (out `+0x34`, `+0x38`);
- `+0x70` plus the facing plus `+0xBC` is the shadow's rotation (out `+0x24`);
- `+0x78` multiplies the strength term (out `+0x28`).

The values used are saved at `+0xC0` to `+0xD4` for the next cross-fade.

## Layouts

A command record:

```
+0x00  u16  bits 0-6 id, bits 7-15 length in bytes
+0x02  ...  parameters: subtype bytes at +2/+3, words or floats from +4
```

A first-pool shadow slot (`0xE0` bytes, 160 at `[02B40528]`), the ramp fields:

```
+0x00  u8      counter, channel 0 (pair)
+0x01  u8      counter, channel 1
+0x02  u8      counter, channel 2 (pair)
+0x03  u8      counter, channel 3
+0x10  u32     handle: generation << 8 | slot
+0x40  u8      bit 0 enabled
+0x41  u8      bit 0 paused, bit 1 hidden
+0x43  u8      counter, cross-fade
+0x50  f32[2]  channel 0: anchor offset       +0x60  f32[2]  its step
+0x58  f32[2]  channel 2: extent scales       +0x68  f32[2]  its step
+0x70  f32     channel 1: rotation            +0x74  f32     its step
+0x78  f32     channel 3: strength            +0x7C  f32     its step
+0x80  f32[6]  the cross-fade's previous values
+0x98  f32     cross-fade weight input        +0x9C  f32     its step
+0xC0  f32[6]  the values last built
```

Every access to the slot fields is in
[the ramp-channel access table](authored-presentation-commands-ramp-channel-record-accesses.tsv).

## State

| Address | Holds |
|---|---|
| `01EFFAF0` | the pair table, 76 x 16 bytes |
| `02CA4410`, `02CA4670` | bank A and bank B, 75 pointers each |
| `02B40528` | the first shadow pool, `0x8C00` bytes allocated once by `003B6890` |
| `02B40520` | the pool's generation counter |
| `02B40524` | the pool gate: `003B6930(v)` keeps the gate bits that `v >> 2` keeps and adds `v & 3`; its callers give it 4 or 6, which clear or set bit 1 (hide), so bit 0 stays clear |

## Modding notes

- Keep command ids below `0x49`: higher ids call a null pointer.
- A ramp command does nothing for a character without a first-pool shadow entry.
- A ramp of 0 steps is a jump; up to 255 steps fit the byte counter. Steps are per
  character-update pass, not per frame of wall time, and a paused slot does not advance.
- The id-5 command is the only one served by bank B; registering a handler in bank-A slot 5 adds an
  actor-side call before it.

## Related

- [Character lighting and shadows](character-lighting-and-shadows.md): the two shadow pools these
  commands drive.
- [Model effects and motion commands](model-effects-and-motion-commands.md): where the commands are
  authored.
- [Bone trails](bone-trails.md): what command `0x11` switches.
- [Character rig and look](character-rig-and-look.md): the rotators of `0x24` and `0x25`.
- [Character fades](character-fades.md): the fade forwarder of `0x23`.
- [Animation sounds](../Sound-And-Music/animation-sounds.md): the sounds of `0x05`, `0x19` and `0x29`.
- [Animation-driven movement](../Movement-And-Pathfinding/animation-driven-movement.md): command `0x1A`.
