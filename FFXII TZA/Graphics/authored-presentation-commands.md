---
title: "Authored presentation commands: the command handlers and their ramp channels"
kind: "system"
category: "Graphics"
addresses: "0041DA90, 01EFFAF0, 02CA4410, 02CA4670, 0041D6C0, 0041D6D0, 0041CCA0, 004269A0, 002EA320, 002EA5F0, 00417AD0, 00417C60, 004173D0, 00417440, 00417460, 004174D0, 00426870, 00520800, 02B40528, 003B6890, 003B6A90, 003B69B0, 003B6A10, 003B6950, 003B5890, 003B5C00, 003B5D40, 003B62D0, 02B40524, 003B6930"
---

## What the player sees

As a character's motion plays, small commands authored in the motion data fire at set points:
footstep sounds and dust, character sounds, weapon trails switching on and off, a weapon moving
between hand and sheath, a sway or a rotator speeding up, and the character's shadow sliding,
turning, stretching and fading over a number of frames. These commands are all run by the code on
this page.

## How it works

### Walking the stream

`0041DA90(entry, stream)` runs the commands of the stream's current block. The block is at
`[stream + 368h] + [entry + 90h]`; its byte `+2 & 3Fh` is the command count and the commands start
at `+4`. Each command begins with a word whose bits 0 to 6 are the id and bits 7 to 15 the command's
length in bytes, which is how the walk steps to the next (`0041DB6A`). Nothing runs unless bit 20 of
the stream's `+0C`<sub>h</sub> is set. With bit 4 of `+0C`<sub>h</sub> also set, a command whose pair-table flag is set is
skipped (`0041DB37`).

The id is clamped to `4B`<sub>h</sub> (`0041DB25`) and the command is dispatched through the pair table:
`call [01EFFAF0 + id x 16]` with the command in `rcx`, the entry in `rdx` and the stream in `r8`
(`0041DB66`).

### The pair table

`01EFFAF0` holds 76 entries of `{ invoker, flag }`:

| Invoker kind | Ids |
|---|---|
| a generic thunk that loads its own slot of bank `02CA4410` and jumps to it with the render record `[stream + 2E0h]` in `rcx` and the command in `rdx`; it returns when the slot is empty | `11`<sub>h</sub> to `16`<sub>h</sub>, `18`<sub>h</sub> to `1A`<sub>h</sub>, `1D`<sub>h</sub> to `21`<sub>h</sub>, `23`<sub>h</sub> to `26`<sub>h</sub>, `28`<sub>h</sub> to `2A`<sub>h</sub>, `2F`<sub>h</sub>, `34`<sub>h</sub>, `3F`<sub>h</sub>, `48`<sub>h</sub> (25) |
| a bespoke invoker | `00`<sub>h</sub>, `01`<sub>h</sub>, `03`<sub>h</sub>, `04`<sub>h</sub>, `05`<sub>h</sub>, `06`<sub>h</sub>, `08`<sub>h</sub>, `09`<sub>h</sub>, `0A`<sub>h</sub>, `0B`<sub>h</sub>, `0D`<sub>h</sub> to `10`<sub>h</sub>, `2C`<sub>h</sub> (15) |
| `0016D6A0`, which returns 0 | 33 ids |
| null | `49`<sub>h</sub>, `4A`<sub>h</sub>, `4B`<sub>h</sub> |

Because of the clamp, a command id from `49`<sub>h</sub> to `7F`<sub>h</sub> calls address 0.

### The two banks

Bank A `02CA4410` and bank B `02CA4670` hold 75 pointers each; `0041CCA0` clears both. `0041D6C0(id, fn)`
stores into bank A and `0041D6D0(id, fn)` into bank B.

`004269A0`, the character render system's start-up, stores 24 handlers in bank A and one, id 5, in
bank B (`00426A12` to `00426B84`). The actor side's `002EA320` and `002EA5F0` store ids 4
(`002E70C0`), 5 (`0016D6A0`), 6 (`002E7090`), `0C`<sub>h</sub> (`002E70A0`) and `26`<sub>h</sub> (`002E7080`) in bank A.

### The bespoke invokers that use the banks

- Id 4, `00417AD0`, switches on the command's byte `+2`: subtype 1 calls bank-A slot 4 with the actor
  `[stream + 2C0h]` four times, tagged `80`<sub>h</sub> to `83`<sub>h</sub>; subtype 2 sets bit 21 and subtype 4 bit 15
  of the stream's `+0C`<sub>h</sub> before the call; subtypes 10 and 11 set bits 1 and 0 of the render record's
  `+419`<sub>h</sub>; subtype 12 queries the record (`0041F2F0`) and may call `00423F20`. It ends by setting bit
  4 of the stream's `+2C8`<sub>h</sub>.
- Id 5, `00417C60`, calls bank-A slot 5 with the actor, then bank-B slot 5 with the render record,
  then sets bit 5 of `+2C8`<sub>h</sub>. Bank-A slot 5 is the empty `0016D6A0`, so the command is the
  character sound.
- Id 6, `00417CC0`, calls bank-A slot 6 with the actor and sets bit 6 of `+2C8`<sub>h</sub>.
- Slot `0C`<sub>h</sub> is not in the pair table; `0041DA90` calls it with the actor and `stream + 31Ch` when
  the motion reaches the time at `+34C`<sub>h</sub>.
- Ids `0D`<sub>h</sub> to `10`<sub>h</sub> are the ramp setters below.

### The motion invokers

Five more bespoke invokers act on the presentation entry (`rdx`) and the stream (`r8`) directly,
without the banks. "Starting the entry" means: state word `+04`<sub>h</sub> = 1, bit 1 of `+08`<sub>h</sub>, and the
speed `+20`<sub>h</sub> = the stream's `+340`<sub>h</sub>.

| Id | Invoker | What it does |
|---|---|---|
| `00`<sub>h</sub> | `00417810` | plays the motion from frame 0: moves `+324`<sub>h</sub> to `+326`<sub>h</sub> and stores the motion number `+31C`<sub>h</sub> at `+324`<sub>h</sub> when its top nibble is 1 or 2 (else `FFFF`<sub>h</sub>), clears the entry's `+14`<sub>h</sub> and `+1C`<sub>h</sub>; a negative word `+2` sets the end and loop frames `+16`<sub>h</sub> / `+18`<sub>h</sub> to `7FFF`<sub>h</sub> and clears `+96`<sub>h</sub> bit 2, otherwise both become word `+2` − 1 with `+96`<sub>h</sub> bit 2 set and, for a non-zero end, `+1C`<sub>h</sub> = (end − `[01DFE0BC]`) / end; starts the entry, clears bit 12 of `+2C8`<sub>h</sub> and bit 9 of `+0C`<sub>h</sub>, and jumps to the slot at `[[02CA4668] + 2F8h]` |
| `03`<sub>h</sub> | `00417A80` | loops: on the stream's own entry (`+18`<sub>h</sub>) it only sets bit 3 of `+0C`<sub>h</sub>; otherwise it copies `+14`<sub>h</sub> to the loop frame `+18`<sub>h</sub>, sets `+96`<sub>h</sub> bit 6 and, when no count is running (`+5E`<sub>h</sub> = −1), sets the count to word `+2` × `[01DFE0B4]`, or −1 for a word of −1 |
| `08`<sub>h</sub> | `00417D00` | arms a blend unless bit 17 or 14 of `+0C`<sub>h</sub> is set: byte `+3` to bit 0 of `+2E8`<sub>h</sub>; byte `+2` of `FF`<sub>h</sub> sets bit 1 and a step `+354`<sub>h</sub> of 0, otherwise the step is `1 / (byte + 1)` (0 for 0); `+358`<sub>h</sub> = 16; bit 11 of `+0C`<sub>h</sub>, and bit 14 too when bit 13 is set; clears bit 10 of the word `002ED570([+330h])` returns when `+338`<sub>h</sub> is not −1 |
| `0A`<sub>h</sub> | `00418600` | copies bytes `+2` to `+5` to the stream's `+2DC`<sub>h</sub>–`+2DF`<sub>h</sub> and starts the entry |
| `2C`<sub>h</sub> | `00417DE0` | arms a blend chosen by the previous motion, unless bit 17 or 14 of `+0C`<sub>h</sub> is set. Word `+2` of `FFFF`<sub>h</sub> matches any motion (rank 1); otherwise it must equal `+326h & FFFh`, and the byte list at `+8` (count byte `+7`, two bytes an item) must hold `FF`<sub>h</sub> (rank 2) or the stream's byte `+329`<sub>h</sub> (rank 3). A rank not below the stream's `+32A`<sub>h</sub> wins and is stored there; byte `+4` sets the step as in `08`<sub>h</sub> (`1 / byte`), byte `+5` bit 7 goes to bit 0 of `+2E8`<sub>h</sub>, the rest of byte `+5` to `+358`<sub>h</sub> and byte `+6` to `+35A`<sub>h</sub> |

### The keyed records and the motion clock

Besides the current block, an entry walks the keyed sub-records of its motion's command block
(cursor `+8C`<sub>h</sub> from the track start `+84`<sub>h</sub>, restart point `+88`<sub>h</sub>). `0041E000(stream, entry,
frame)` runs every sub-record whose key is at most `frame`, clearing the stream's `+32A`<sub>h</sub> before
each. With a frame of −1 it runs all remaining sub-records but only their commands `04`<sub>h</sub>, `11`<sub>h</sub>,
`15`<sub>h</sub> and `1F`<sub>h</sub> (mask `80220010`<sub>h</sub>).

Past the end of the track it rewinds the cursor to `+88`<sub>h</sub>
and sets `+96`<sub>h</sub> bit 7, after which it does nothing. When a `08`<sub>h</sub> or `2C`<sub>h</sub> ran, it clears bit 17
of the stream's `+0C`<sub>h</sub>.

After the block, an entry in state 2 with `+96`<sub>h</sub> bit 2 clear gets `0041E1D0` when it had ended
before the block and `0041E000` with −1 when the block ended it; `0041E1D0` runs only the commands
`06`<sub>h</sub>, `11`<sub>h</sub>, `15`<sub>h</sub> and `1F`<sub>h</sub> (mask `80220040`<sub>h</sub>). `0041DA90` then calls `0041E000` with the
entry's frame `+0C`<sub>h</sub>. The entry's word `+0A`<sub>h</sub>
then picks the clock: 0 runs `00418750`, 1 runs the channel reader `00418880` of
[model effects and motion commands](model-effects-and-motion-commands.md).

`00418750` advances a playing entry (bit 1 of `+08`<sub>h</sub>, state 1) unless bit 18 of the stream's
`+0C`<sub>h</sub> is set: the frame `+0C`<sub>h</sub> and the time `+10`<sub>h</sub> (capped at 2,592,000) grow by the speed
`+20`<sub>h</sub> divided by word `+1A`<sub>h</sub>. At the end frame `+16`<sub>h</sub> the frame goes back to the loop frame
`+18`<sub>h</sub>. A loop (loop frame below the end, or `+96`<sub>h</sub> bit 6) counts down `+5E`<sub>h</sub>, −1 meaning for
ever, and sets state 2 at 0. Otherwise the frame stays at the end minus `[01DFE0BC]` and the
entry ends (state 2), unless the stream's `+2E8`<sub>h</sub> bit 0 and the entry's `+96`<sub>h</sub> bit 4 are both set.

When a timed entry passes the time at `+34C`<sub>h</sub>, or an ended entry with `+96`<sub>h</sub> bit 2 finishes, the
walker sets state 2, flushes the keyed records (`0041E000` with −1), sets bit 12 of `+2C8`<sub>h</sub> and
runs `0041C6C0`: for motion number `2008`<sub>h</sub>, while bit 21 of `+0C`<sub>h</sub> is clear, it calls bank-A slot
4 (`[02CA4430]`) with the actor `+2C0`<sub>h</sub> and an argument block whose word `+2` is 2, then sets
bit 21.

### The registered handlers

Each handler takes the render record and the command:

| Id | Handler | What it does |
|---|---|---|
| `05`<sub>h</sub> (bank B) | `00520C50` | plays a sound on the record's emitter `+5F0`<sub>h</sub> (`0046CBA0`): word `+2` is mode (bits 12 to 15) and type |
| `11`<sub>h</sub> | `00520160` | stores byte `+2` at `+3D0`<sub>h</sub> and raises bit 24 of `+294`<sub>h</sub>: weapon trails on or off |
| `12`<sub>h</sub> | `005207C0` | `003E29F0(003E6DA0(), 4, byte +2 != 0)`: the look-tracking switch of [Character rig and look](character-rig-and-look.md) |
| `13`<sub>h</sub> | `00520430` | stores the controller switch (bytes `+2`, `+3`, word `+4` to `+3F4`<sub>h</sub> to `+3F6`<sub>h</sub>) and broadcasts it (`00429500`), holding bit 9 of `+290`<sub>h</sub> meanwhile; byte `+2 & B9h == 80h` takes the `004288B0` / `0042B580` arm |
| `14`<sub>h</sub> | `00520E70` | applies `00521050` to the record's entity and its sub-tree (`00426870`) |
| `15`<sub>h</sub> | `00520740` | byte `+2` to bits 0 to 2 and byte `+3` to bits 3 to 5 of `+3D1`<sub>h</sub>, and raises bit 23 of `+290`<sub>h</sub> |
| `16`<sub>h</sub> | `00520BD0` | bit 0 of word `+2` to `+3D2`<sub>h</sub>, its upper bits to `+3D3`<sub>h</sub>, word `+4` to `+3F8`<sub>h</sub>, then `0042B550` |
| `18`<sub>h</sub> | `00520C80` | `003B0C50(record index, byte +2)` when `00421E20` finds the record's special bone `100`<sub>h</sub> |
| `19`<sub>h</sub> | `00520CE0` | a type-1 sound on the emitter, mode 0 (`0046CC70`) |
| `1A`<sub>h</sub> | `00520C10` | movement along profile word `+2` (`003E6340`) when the entity has a `+370`<sub>h</sub> object |
| `1D`<sub>h</sub> | `00520D30` | the pose-sequencer event: byte `+2` low nibble the event, high nibble a record filter, byte `+3` the choice; `FD`<sub>h</sub> sets bit 6 of `+4B7`<sub>h</sub>, `FE`<sub>h</sub> calls `00428B30`, `FF`<sub>h</sub> stores byte `+3` in the model instance `+B8`<sub>h</sub> |
| `1E`<sub>h</sub> | `00520DF0` | with the same filter, calls `003E6A20` with byte `+2 & Fh` |
| `1F`<sub>h</sub> | `00520140` | `003E6710` with bit 0 of word `+2` |
| `20`<sub>h</sub> | `005207A0` | `+2F4`<sub>h</sub> = `303h + (word +2 != 0)` |
| `21`<sub>h</sub> | `00520780` | `+2F6`<sub>h</sub> = `305h + (word +2 != 0)` |
| `23`<sub>h</sub> | `00520180` | the fade forwarder `004293C0` with dword `+4`, word `+8` and word `+2` |
| `24`<sub>h</sub> | `005201B0` | ramps rotator word `+2` to the speed float `+8` over word `+4` frames (`003DFE70`); word `+6` with bits 7 and 6 sends it to another controller |
| `25`<sub>h</sub> | `00520320` | the rotator back to its default speed |
| `28`<sub>h</sub> | `00520720` | `003E6AA0`: dword `+4` into bits 27 to 31 of `+304`<sub>h</sub>, dirty bit 27 of `+294`<sub>h</sub> |
| `29`<sub>h</sub> | `00520D00` | the same sound with the volume in word `+2` (`0046CC70`) |
| `2A`<sub>h</sub> | `005206B0` | `003E7140` with the three floats `+8` to `+10`<sub>h</sub> |
| `2F`<sub>h</sub> | `00520E30` | sends event word `+2` with bit `2000`<sub>h</sub> set to the child sub-tree (`0042EF90`, `00521000`) |
| `34`<sub>h</sub> | `00520800` | the shadow command, below |
| `3F`<sub>h</sub> | `00520510` | on a record with no parent, applies `00520E90` to it and its sub-tree with a bone (word `+2`), a direction (floats `+4` to `+C`<sub>h</sub>), a preset (word `+10h & FFFh`, 0 when the bone is -1) and a flag (bit 15 of word `+10`<sub>h</sub>) |
| `48`<sub>h</sub> | `005205B0` | as `3F`<sub>h</sub>, with the target found by name (`00372800`) |

`00426870(index, fn, arg)` calls `fn` on the record at `022C6F28 + index x 740h` at once and, when
its first child `+8` is not -1, walks the children with `0042EF90`.

### The shadow command, `34`<sub>h</sub>

`00520800` with byte `+2 = FFh` switches both shadow pools: byte `+3` non-zero calls `003AFD30(1)` and
`003B6930(4)`, zero calls `003AFD30(0)` and `003B6930(6)`. Any other byte `+2` acts on the record's
second-pool entry (`+118`<sub>h</sub>, through `003AFC10`), one arm per bit:

| Byte `+2` | Effect, value = float `+4`, frames = byte `+3` |
|---|---|
| `01`<sub>h</sub>, `02`<sub>h</sub>, `04`<sub>h</sub> | ramp `+24`<sub>h</sub>, `+28`<sub>h</sub> or `+34`<sub>h</sub> to the value over the frames (below 2: at once) |
| `08`<sub>h</sub> | `+1F`<sub>h</sub> low bits: 2 when byte `+3` is set, else 1 |
| `10`<sub>h</sub> | `+1F`<sub>h</sub> high bits: `20`<sub>h</sub> when byte `+3` is set, else `10`<sub>h</sub> |
| `20`<sub>h</sub>, `40`<sub>h</sub> | ramp `+3C`<sub>h</sub> or `+44`<sub>h</sub> the same way |
| `80`<sub>h</sub> | byte `+3` = 1: `+40`<sub>h</sub> = value; 2: bit 1 of `+58`<sub>h</sub> and `+56`<sub>h</sub> = `40`<sub>h</sub>, `80`<sub>h</sub> or `100`<sub>h</sub> for values up to 1.5, 2.5 or above; 4: bit 0 of `+58`<sub>h</sub> and `+50`<sub>h</sub> = value |

### The ramp channels

Commands `0D`<sub>h</sub> to `10`<sub>h</sub> animate the character's first-pool shadow entry. Their invokers take the
entry's handle from `+35C`<sub>h</sub> of the presentation entry and do nothing when it is -1; the step count is
the command's byte `+2`.

| Command | Invoker | Setter | Counter | Value | Step |
|---|---|---|---|---|---|
| `0D`<sub>h</sub> | `004173D0` | `003B6A90` | `+00`<sub>h</sub> | `+50`<sub>h</sub>, `+54`<sub>h</sub> | `+60`<sub>h</sub>, `+64`<sub>h</sub> |
| `0E`<sub>h</sub> | `00417440` (tail jump) | `003B69B0` | `+01`<sub>h</sub> | `+70`<sub>h</sub> | `+74`<sub>h</sub> |
| `0F`<sub>h</sub> | `00417460` | `003B6A10` | `+02`<sub>h</sub> | `+58`<sub>h</sub>, `+5C`<sub>h</sub> | `+68`<sub>h</sub>, `+6C`<sub>h</sub> |
| `10`<sub>h</sub> | `004174D0` (tail jump) | `003B6950` | `+03`<sub>h</sub> | `+78`<sub>h</sub> | `+7C`<sub>h</sub> |

The pair commands pass the floats `+4` and `+8`; the single ones pass float `+4`. A setter:

1. finds the slot `[02B40528] + (handle & FFh) x E0h` and returns without writing when its `+10`<sub>h</sub>
   is not the handle;
2. with 0 steps, stores the value and clears the counter, which cancels a running ramp;
3. otherwise stores the count and the step `(target - current) x (1 / steps)`, computing the
   reciprocal first (`003B69E8`, `003B69EC`).

A fifth channel, counter `+43`<sub>h</sub>, value `+98`<sub>h</sub>, step `+9C`<sub>h</sub>, is set by `003B5D40(handle, n)` (from
`0041D560`). It copies the slot's last built values `+C0`<sub>h</sub> to `+D4`<sub>h</sub> into the blend set `+80`<sub>h</sub> to
`+94`<sub>h</sub>, sets the counter to `n`, the value to 0 and the step to `1 / n`, and takes the first step at
once: a cross-fade from the previous shadow to the new one over `n` steps.

### Advancing the channels

`003B5890`, called once per character-update pass from `00426090` (`00426112`), walks all 160 slots.
A slot advances when bit 0 of `+40`<sub>h</sub> is set and bit 0 of `+41h | [02B40524]` is clear. It steps the
channels in the order `+00`<sub>h</sub>, `+02`<sub>h</sub>, `+01`<sub>h</sub>, `+03`<sub>h</sub>, `+43`<sub>h</sub>: each with a non-zero counter adds
its step to its value and decrements the counter. The value is never snapped to the target, so it
ends within float rounding of it. `003B5C00(handle)` applies the same step to one slot without the
pause tests; `0041C850` and `0041D820` call it.

### What the channels drive

`003B62D0` builds the slot's shadow draw record each frame. While counter `+43`<sub>h</sub> is non-zero it blends
each channel value with the blend set by a weight from `0046FAE0`. Then:

- `+50`<sub>h</sub>, `+54`<sub>h</sub> plus `+48`<sub>h</sub>, `+4C`<sub>h</sub>, times `+44`<sub>h</sub>, is an offset from the anchor bone, rotated by
  the character's facing (render record `+124`<sub>h</sub>);
- `+58`<sub>h</sub>, `+5C`<sub>h</sub> multiply the shadow's two extents (out `+34`<sub>h</sub>, `+38`<sub>h</sub>);
- `+70`<sub>h</sub> plus the facing plus `+BC`<sub>h</sub> is the shadow's rotation (out `+24`<sub>h</sub>);
- `+78`<sub>h</sub> multiplies the strength term (out `+28`<sub>h</sub>).

The values used are saved at `+C0`<sub>h</sub> to `+D4`<sub>h</sub> for the next cross-fade.

## Layouts

A command record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | bits 0-6 id, bits 7-15 length in bytes |  |
| `02`<sub>h</sub> | `...` | parameters: subtype bytes at +2/+3, words or floats from +4 |  |

A first-pool shadow slot (`E0`<sub>h</sub> bytes, 160 at `[02B40528]`), the ramp fields:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | counter, channel 0 (pair) |  |
| `01`<sub>h</sub> | `u8` | counter, channel 1 |  |
| `02`<sub>h</sub> | `u8` | counter, channel 2 (pair) |  |
| `03`<sub>h</sub> | `u8` | counter, channel 3 |  |
| `10`<sub>h</sub> | `u32` | handle: generation << 8 \| slot |  |
| `40`<sub>h</sub> | `u8` | bit 0 enabled |  |
| `41`<sub>h</sub> | `u8` | bit 0 paused, bit 1 hidden |  |
| `43`<sub>h</sub> | `u8` | counter, cross-fade |  |
| `50`<sub>h</sub> | `f32[2]` | channel 0: anchor offset | +`60`<sub>h</sub>  f32[2]  its step |
| `58`<sub>h</sub> | `f32[2]` | channel 2: extent scales | +`68`<sub>h</sub>  f32[2]  its step |
| `70`<sub>h</sub> | `f32` | channel 1: rotation | +`74`<sub>h</sub>  f32     its step |
| `78`<sub>h</sub> | `f32` | channel 3: strength | +`7C`<sub>h</sub>  f32     its step |
| `80`<sub>h</sub> | `f32[6]` | the cross-fade's previous values |  |
| `98`<sub>h</sub> | `f32` | cross-fade weight input | +`9C`<sub>h</sub>  f32     its step |
| `C0`<sub>h</sub> | `f32[6]` | the values last built |  |

Every access to the slot fields is in
[the ramp-channel access table](authored-presentation-commands-ramp-channel-record-accesses.tsv).

## State

| Address | Holds |
|---|---|
| `01EFFAF0` | the pair table, 76 x 16 bytes |
| `02CA4410`, `02CA4670` | bank A and bank B, 75 pointers each |
| `02B40528` | the first shadow pool, `8C00`<sub>h</sub> bytes allocated once by `003B6890` |
| `02B40520` | the pool's generation counter |
| `02B40524` | the pool gate: `003B6930(v)` keeps the gate bits that `v >> 2` keeps and adds `v & 3`; its callers give it 4 or 6, which clear or set bit 1 (hide), so bit 0 stays clear |

## Modding notes

- Keep command ids below `49`<sub>h</sub>: higher ids call a null pointer.
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
- [Bone trails](bone-trails.md): what command `11`<sub>h</sub> switches.
- [Character rig and look](character-rig-and-look.md): the rotators of `24`<sub>h</sub> and `25`<sub>h</sub>.
- [Character fades](character-fades.md): the fade forwarder of `23`<sub>h</sub>.
- [Animation sounds](../Sound-And-Music/animation-sounds.md): the sounds of `05`<sub>h</sub>, `19`<sub>h</sub> and `29`<sub>h</sub>.
- [Animation-driven movement](../Movement-And-Pathfinding/animation-driven-movement.md): command `1A`<sub>h</sub>.
