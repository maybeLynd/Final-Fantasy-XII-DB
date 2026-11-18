[Home](../../README.md) / [Graphics](README.md) / Authored presentation commands

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Authored presentation commands: the command handlers and their ramp channels | system | Graphics | Character models / Animation And Motion | The presentation commands authored in model and motion data and run on a character's render record: how the stream is walked and dispatched through the pair table and the two handler banks, what each registered handler does, and the five ramp channels that commands 0x0D to 0x10 drive on the character's shadow entry, with the tick that advances them and the shadow build that consumes them. | 0x0041DA90, 0x01EFFAF0, 0x02CA4410, 0x02CA4670, 0x0041D6C0, 0x0041D6D0, 0x0041CCA0, 0x004269A0, 0x002EA320, 0x002EA5F0, 0x00417AD0, 0x00417C60, 0x004173D0, 0x00417440, 0x00417460, 0x004174D0, 0x00426870, 0x00520800, 0x02B40528, 0x003B6890, 0x003B6A90, 0x003B69B0, 0x003B6A10, 0x003B6950, 0x003B5890, 0x003B5C00, 0x003B5D40, 0x003B62D0, 0x02B40524, 0x003B6930 |

## What the player sees

As a character's motion plays, small commands authored in the motion data fire at set points:
footstep sounds and dust, character sounds, weapon trails switching on and off, a weapon moving
between hand and sheath, a sway or a rotator speeding up, and the character's shadow sliding,
turning, stretching and fading over a number of frames. These commands are all run by the code on
this page.

Each command in the motion data carries a number; the game looks it up in a table and runs the handler that the
character render system or the actor code put there at start-up. The four shadow commands store a target and a number
of frames, a step once per character update moves the shadow toward it, and the shadow drawing reads the result every
frame.

## How it works

### Walking the stream

`0x0041DA90(entry, stream)` runs the commands of the stream's current block. The block is at
`[stream + 0x368] + [entry + 0x90]`; its byte `+2 & 0x3F` is the command count and the commands start
at `+4`. Each command begins with a word whose bits `0x7F` are the id and the bits under mask `0xFF80` the command's
length in bytes, which is how the walk steps to the next¹. Nothing runs unless bit `0x100000` of
the stream's `+0x0C` is set. With bit `0x10` of `+0x0C` also set, a command whose pair-table flag is set is
skipped².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0041DB6A` |
| ² | `0x0041DB37` |

</details>

The id is clamped to `0x4B`¹ and the command is dispatched through the pair table:
`call [0x01EFFAF0 + id x 16]` with the command in `rcx`, the entry in `rdx` and the stream in `r8`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0041DB25` |
| ² | `0x0041DB66` |

</details>

### The pair table

`0x01EFFAF0` holds 76 entries of `{ invoker, flag }`:

| Invoker kind | Ids |
|---|---|
| a generic thunk that loads its own slot of bank `0x02CA4410` and jumps to it with the render record `[stream + 0x2E0]` in `rcx` and the command in `rdx`; it returns when the slot is empty | `0x11` to `0x16`, `0x18` to `0x1A`, `0x1D` to `0x21`, `0x23` to `0x26`, `0x28` to `0x2A`, `0x2F`, `0x34`, `0x3F`, `0x48` (25) |
| a bespoke invoker | `0x00`, `0x01`, `0x03`, `0x04`, `0x05`, `0x06`, `0x08`, `0x09`, `0x0A`, `0x0B`, `0x0D` to `0x10`, `0x2C` (15) |
| `0x0016D6A0`, which returns 0 | 33 ids |
| null | `0x49`, `0x4A`, `0x4B` |

Because of the clamp, a command id from `0x49` to `0x7F` calls address 0.

### The two banks

Bank A `0x02CA4410` and bank B `0x02CA4670` hold 75 pointers each; `0x0041CCA0` clears both. `0x0041D6C0(id, fn)`
stores into bank A and `0x0041D6D0(id, fn)` into bank B.

`0x004269A0`, the character render system's start-up, stores 24 handlers in bank A and one, id 5, in
bank B (`0x00426A12` to `0x00426B84`). The actor side's `0x002EA320` and `0x002EA5F0` store ids 4¹, 5², 6³, `0x0C`⁴ and `0x26`⁵ in bank A.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E70C0` |
| ² | `0x0016D6A0` |
| ³ | `0x002E7090` |
| ⁴ | `0x002E70A0` |
| ⁵ | `0x002E7080` |

</details>

### The bespoke invokers that use the banks

- Id 4, `0x00417AD0`, switches on the command's byte `+2`: subtype 1 calls bank-A slot 4 with the actor
  `[stream + 0x2C0]` four times, tagged `0x80` to `0x83`; subtype 2 sets bit `0x200000` and subtype 4 bit `0x8000`
  of the stream's `+0x0C` before the call; subtypes 10 and 11 set bits `0x2` and `0x1` of the render record's
  `+0x419`; subtype 12 queries the record¹ and may call `0x00423F20`;
  - while bank-A slot 4 (`[0x02CA4430]`) is empty it skips the switch and only sets the end bit²;
  - the switch goes through the jump table `0x00417C2C`³; subtypes 3 and 5 to 9, and 0 or
    above 12, make the plain call, the actor in `rcx` and the command in `rdx`⁴, as do
    subtypes 2 and 4 after their bit⁵; subtypes 10 to 12 make no slot call;
  - subtype 1 passes a copy of the command's first four bytes with byte `+2` replaced by the tag
   ⁶;
  - subtype 12 fills a `0x40`-byte block with `0x0041F2F0(record, 0x10, block)`, the record being
    `[stream + 0x2E0]`; when bit `0x2` of the block's byte `+0x3C` is set it calls
    `0x00423F20(record, signed word +0xCC)` and sets bit `0x1` of the record's word `+0x5E`⁷;
  - the handler ends by setting bit `0x10` of the stream's `+0x2C8`.
- Id 5, `0x00417C60`, calls bank-A slot 5 with the actor, then bank-B slot 5 with the render record,
  then sets bit `0x20` of `+0x2C8`. Bank-A slot 5 is the empty `0x0016D6A0`, so the command is the
  character sound.
  - Both calls pass the command in `rdx`, each is skipped while its slot is empty⁸, and
    the render record is `[stream + 0x2E0]`⁹.
- Id 6, `0x00417CC0`, calls bank-A slot 6 with the actor and sets bit `0x40` of `+0x2C8`.
  - Slot `0x0C` is not in the pair table; `0x0041DA90` calls it with the actor and `stream + 0x31C` when the motion
    reaches the time at `+0x34C` (not −1), and also for an entry with `+0x96` bit `0x4` whose word `+0x04` is 2.
    Either call needs stream `+0x0C` bit `0x100000` set, bits `0x20000200` clear, and byte `0x01EFFBB8` zero when bit
    `0x10` is set; it then sets bit `0x200`.
- Ids `0x0D` to `0x10` are the ramp setters below.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0041F2F0` |
| ² | `0x00417AFC` |
| ³ | `0x00417B02`-`0x00417B25` |
| ⁴ | `0x00417BC5`-`0x00417BCC` |
| ⁵ | `0x00417C00`, `0x00417BBE` |
| ⁶ | `0x00417B27`-`0x00417B80` |
| ⁷ | `0x00417B88`-`0x00417BB7` |
| ⁸ | `0x00417C77`, `0x00417C8F` |
| ⁹ | `0x00417C94` |

</details>

### The motion invokers

Five more bespoke invokers act on the presentation entry (`rdx`) and the stream (`r8`) directly,
without the banks. "Starting the entry" means: state word `+0x04` = 1, bit `0x2` of `+0x08`, and the
speed `+0x20` = the stream's `+0x340`.

| Id | Invoker | What it does |
|---|---|---|
| `0x00` | `0x00417810` | plays the motion from frame 0: moves `+0x324` to `+0x326` and stores the motion number `+0x31C` at `+0x324` when its top nibble is 1 or 2 (else `0xFFFF`), clears the entry's `+0x14` and `+0x1C`; a negative word `+2` sets the end and loop frames `+0x16` / `+0x18` to `0x7FFF` and clears `+0x96` bit `0x4`, otherwise both become word `+2` − 1 with `+0x96` bit `0x4` set and, for a non-zero end, `+0x1C` = (end − `[0x01DFE0BC]`) / end; starts the entry, clears bit `0x1000` of `+0x2C8` and bit `0x200` of `+0x0C`, and jumps to the slot at `[[0x02CA4668] + 0x2F8]` |
| `0x03` | `0x00417A80` | loops: on the stream's own entry (`+0x18`) it only sets bit `0x8` of `+0x0C`; otherwise it copies `+0x14` to the loop frame `+0x18`, sets `+0x96` bit `0x40` and, when no count is running (`+0x5E` = −1), sets the count to word `+2` × `[0x01DFE0B4]`, or −1 for a word of −1 |
| `0x08` | `0x00417D00` | arms a blend unless bit `0x20000` or `0x4000` of `+0x0C` is set: byte `+3` to bit `0x1` of `+0x2E8`; byte `+2` of `0xFF` sets bit `0x2` and a step `+0x354` of 0, otherwise the step is `1 / (byte + 1)` (0 for 0); `+0x358` = 16; bit `0x800` of `+0x0C`, and bit `0x4000` too when bit `0x2000` is set; clears bit `0x400` of the word `0x002ED570([+0x330])` returns when `+0x338` is not −1 |
| `0x0A` | `0x00418600` | copies bytes `+2` to `+5` to the stream's `+0x2DC`–`+0x2DF` and starts the entry |
| `0x2C` | `0x00417DE0` | arms a blend chosen by the previous motion, unless bit `0x20000` or `0x4000` of `+0x0C` is set. Word `+2` of `0xFFFF` matches any motion (rank 1); otherwise it must equal `+0x326 & 0xFFF`, and the byte list at `+8` (count byte `+7`, two bytes an item) must hold `0xFF` (rank 2) or the stream's byte `+0x329` (rank 3). A rank not below the stream's `+0x32A` wins and is stored there; byte `+4` sets the step as in `0x08` (`1 / byte`), byte `+5` bit `0x80` goes to bit `0x1` of `+0x2E8`, the rest of byte `+5` to `+0x358` and byte `+6` to `+0x35A` |

### The keyed records and the motion clock

Besides the current block, an entry walks the keyed sub-records of its motion's command block
(cursor `+0x8C` from the track start `+0x84`, restart point `+0x88`). `0x0041E000(stream, entry,
frame)` runs every sub-record whose key is at most `frame`, clearing the stream's `+0x32A` before
each. With a frame of −1 it runs all remaining sub-records but only their commands `0x04`, `0x11`,
`0x15` and `0x1F` (mask `0x80220010`).

Past the end of the track it rewinds the cursor to `+0x88`
and sets `+0x96` bit `0x80`, after which it does nothing. When a `0x08` or `0x2C` ran, it clears bit `0x20000`
of the stream's `+0x0C`.

After the block, an entry in state 2 with `+0x96` bit `0x4` clear gets `0x0041E1D0` when it had ended
before the block and `0x0041E000` with −1 when the block ended it; `0x0041E1D0` runs only the commands
`0x06`, `0x11`, `0x15` and `0x1F` (mask `0x80220040`). `0x0041DA90` then calls `0x0041E000` with the
entry's frame `+0x0C`. The entry's word `+0x0A`
then picks the clock: 0 runs `0x00418750`, 1 runs the channel reader `0x00418880` of
[model effects and motion commands](model-effects-and-motion-commands.md).

`0x00418750` advances a playing entry (bit `0x2` of `+0x08`, state 1) unless bit `0x40000` of the stream's
`+0x0C` is set: the frame `+0x0C` and the time `+0x10` (capped at 2,592,000) grow by the speed
`+0x20` divided by word `+0x1A`. At the end frame `+0x16` the frame goes back to the loop frame
`+0x18`. A loop (loop frame below the end, or `+0x96` bit `0x40`) counts down `+0x5E`, −1 meaning for
ever, and sets state 2 at 0. Otherwise the frame stays at the end minus `[0x01DFE0BC]` and the
entry ends (state 2), unless the stream's `+0x2E8` bit `0x1` and the entry's `+0x96` bit `0x10` are both set.

When a timed entry passes the time at `+0x34C`, or an ended entry with `+0x96` bit `0x4` finishes, the walker sets
state 2, flushes the keyed records (`0x0041E000` with −1), sets bit `0x1000` of `+0x2C8` and runs `0x0041C6C0`: for motion
number `0x2008`, while bit `0x200000` of `+0x0C` is clear, it calls bank-A slot 4 (`[0x02CA4430]`) with the actor
`+0x2C0` and an argument block whose byte `+2` is 2, then sets bit `0x200000`.

### The registered handlers

Each handler takes the render record and the command:

| Id | Handler | What it does |
|---|---|---|
| `0x05` (bank B) | `0x00520C50` | plays a sound on the record's emitter `+0x5F0` (`0x0046CBA0`): word `+2` is mode (mask `0xF000`) and type |
| `0x11` | `0x00520160` | stores byte `+2` at `+0x3D0` and raises bit `0x1000000` of `+0x294`: weapon trails on or off |
| `0x12` | `0x005207C0` | `0x003E29F0(0x003E6DA0(), 4, byte +2 != 0)`: the look-tracking switch of [Character rig and look](character-rig-and-look.md) |
| `0x13` | `0x00520430` | stores the controller switch (bytes `+2`, `+3`, word `+4` to `+0x3F4` to `+0x3F6`) and broadcasts it (`0x00429500`), holding bit `0x200` of `+0x290` meanwhile; byte `+2 & 0xB9 == 0x80` takes the `0x004288B0` / `0x0042B580` arm |
| `0x14` | `0x00520E70` | applies `0x00521050` to the record's entity and its sub-tree (`0x00426870`) |
| `0x15` | `0x00520740` | byte `+2` to bits `0x7` and byte `+3` to bits `0x38` of `+0x3D1`, and raises bit `0x800000` of `+0x290` |
| `0x16` | `0x00520BD0` | bit `0x1` of word `+2` to `+0x3D2`, its upper bits to `+0x3D3`, word `+4` to `+0x3F8`, then `0x0042B550` |
| `0x18` | `0x00520C80` | `0x003B0C50(record index, byte +2)` when `0x00421E20` finds the record's special bone `0x100` |
| `0x19` | `0x00520CE0` | a type-1 sound on the emitter, mode 0 (`0x0046CC70`) |
| `0x1A` | `0x00520C10` | movement along profile word `+2` (`0x003E6340`) when the entity has a `+0x370` object |
| `0x1D` | `0x00520D30` | the pose-sequencer event: byte `+2` low nibble the event, high nibble a record filter, byte `+3` the choice; `0xFD` sets bit `0x40` of `+0x4B7`, `0xFE` calls `0x00428B30`, `0xFF` stores byte `+3` in the model instance `+0xB8` |
| `0x1E` | `0x00520DF0` | with the same filter, calls `0x003E6A20` with byte `+2 & 0xF` |
| `0x1F` | `0x00520140` | `0x003E6710` with bit `0x1` of word `+2` |
| `0x20` | `0x005207A0` | `+0x2F4` = `0x303 + (word +2 != 0)` |
| `0x21` | `0x00520780` | `+0x2F6` = `0x305 + (word +2 != 0)` |
| `0x23` | `0x00520180` | the fade forwarder `0x004293C0` with dword `+4`, word `+8` and word `+2` |
| `0x24` | `0x005201B0` | ramps rotator word `+2` to the speed float `+8` over word `+4` frames (`0x003DFE70`); word `+6` with bits `0x80` and `0x40` sends it to another controller |
| `0x25` | `0x00520320` | the rotator back to its default speed |
| `0x28` | `0x00520720` | `0x003E6AA0`: dword `+4` into bits `0xF8000000` of `+0x304`, dirty bit `0x8000000` of `+0x294` |
| `0x29` | `0x00520D00` | the same sound with the volume in word `+2` (`0x0046CC70`) |
| `0x2A` | `0x005206B0` | `0x003E7140` with the three floats `+8` to `+0x10` |
| `0x2F` | `0x00520E30` | sends event word `+2` with bit `0x2000` set to the child sub-tree (`0x0042EF90`, `0x00521000`) |
| `0x34` | `0x00520800` | the shadow command, below |
| `0x3F` | `0x00520510` | on a record with no parent, applies `0x00520E90` to it and its sub-tree with a bone (word `+2`), a direction (floats `+4` to `+0xC`), a preset (word `+0x10 & 0xFFF`, 0 when the bone is -1) and a flag (bit `0x8000` of word `+0x10`) |
| `0x48` | `0x005205B0` | as `0x3F`, with the bone found by the low 16 bits of dword `+0x10` (`0x00372800`), and the preset (low 12 bits) and flag (bit `0x8000`) in word `+2` |

`0x00426870(index, fn, arg)` calls `fn(record, arg)` on the record at `[0x022C6F28] + index x 0x740` at once¹ and, when its first child `+8` is not -1, walks the children with `0x0042EF90`, which
calls `fn` on each child, descends into that child's children `+8` and moves on to its next sibling `+0xA`². An index of -1 calls nothing³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00426880`-`0x004268A3` |
| ² | `0x0042EFB0`-`0x0042EFE7` |
| ³ | `0x00426874` |

</details>

### The shadow command, 0x34

`0x00520800` with byte `+2 = 0xFF` switches both shadow pools: byte `+3` non-zero calls `0x003AFD30(1)` and
`0x003B6930(4)`, zero calls `0x003AFD30(0)` and `0x003B6930(6)`. Any other byte `+2` acts on the record's
second-pool entry (`+0x118`, through `0x003AFC10`), one arm per bit:

| Byte `+2` | Effect, value = float `+4`, frames = byte `+3` |
|---|---|
| `0x01`, `0x02`, `0x04` | ramp `+0x24`, `+0x28` or `+0x34` to the value over the frames (below 2: at once) |
| `0x08` | `+0x1F` low bits: 2 when byte `+3` is set, else 1 |
| `0x10` | `+0x1F` high bits: `0x20` when byte `+3` is set, else `0x10` |
| `0x20`, `0x40` | ramp `+0x3C` or `+0x44` the same way |
| `0x80` | byte `+3` = 1: `+0x40` = value; 2: bit `0x2` of `+0x58` and `+0x56` = `0x40`, `0x80` or `0x100` for values up to 1.5, 2.5 or above; 4: bit `0x1` of `+0x58` and `+0x50` = value |

### The ramp channels

Commands `0x0D` to `0x10` animate the character's first-pool shadow entry. Their invokers take the
entry's handle from `+0x35C` of the stream, the walker's `r8`¹, and do nothing when it is -1; the step count is the command's byte `+2`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004173E3`, `0x00417440`, `0x00417473`, `0x004174D0` |

</details>

| Command | Invoker | Setter | Counter | Value | Step |
|---|---|---|---|---|---|
| `0x0D` | `0x004173D0` | `0x003B6A90` | `+0x00` | `+0x50`, `+0x54` | `+0x60`, `+0x64` |
| `0x0E` | `0x00417440` (tail jump) | `0x003B69B0` | `+0x01` | `+0x70` | `+0x74` |
| `0x0F` | `0x00417460` | `0x003B6A10` | `+0x02` | `+0x58`, `+0x5C` | `+0x68`, `+0x6C` |
| `0x10` | `0x004174D0` (tail jump) | `0x003B6950` | `+0x03` | `+0x78` | `+0x7C` |

The pair commands pass the floats `+4` and `+8`; the single ones pass float `+4`. The pair invokers build the
16-byte block {float `+4`, float `+8`, 0, 1.0} on the stack and pass its address, of which the setters read the
first two floats¹; the single ones pass
float `+4` in `xmm2` with a tail jump. A setter:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004173EF`-`0x00417421`, `0x003B6AC5`-`0x003B6AE0`, `0x003B6A46`-`0x003B6A61` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | finds the slot `[0x02B40528] + (handle & 0xFF) x 0xE0` and returns without writing when its `+0x10` is not the handle; |   |
| 2 | with 0 steps, stores the value and clears the counter, which cancels a running ramp; |   |
| 3 | otherwise stores the count and the step `(target - current) x (1 / steps)`, computing the reciprocal first. | `0x003B69E8`, `0x003B69EC` |

A fifth channel, counter `+0x43`, value `+0x98`, step `+0x9C`, is set by `0x003B5D40(handle, n)` (from
`0x0041D560`), which returns without writing when the slot's `+0x10` is not the handle¹. It copies
the slot's last built values `+0xC0` to `+0xD4` into the blend set `+0x80` to
`+0x94`, sets the counter to `n` and the value to 0, and takes the first step at
once²: a cross-fade from the previous shadow to the new one.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B5D52` |
| ² | `0x003B5D5C`-`0x003B5E0B` |

</details>

The step is not `1 / n`. `0x003B5D40` stores 1.0 at `0x022D914C`, the integer `n` at `0x022D9148` and the qword
`0x3F800000` at `0x022D8F90`, then divides 1.0 by the dword `0x022D9148` read as a float, `divss xmm0, [0x022D9148]`
at `0x003B5DD7`, and stores the quotient at `+0x9C`¹.
`0x0041D560` gives an `n` of at least 1²; an integer from 1 to 255 read as a float is a
denormal, so the quotient overflows and the step and, after the first step, the value are +infinity.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B5DBF`-`0x003B5DEF` |
| ² | `0x0041D5B6`-`0x0041D5BC` |

</details>

The builder's weight `0x0046FAE0(+0x98, 1, 2)` reads entry `(int)(value x (count - 1))` of its curve, clamped to
the curve¹. For +infinity the conversion gives `0x80000000`,
which the clamp `i < 0 ? 0 : i > count - 1 ? count - 1 : i` turns into entry 0 (`cmovs eax, r9d` at `0x0046FB1F`),
0.1746 at `0x01F21418`; the 60 fps resampling `0x0033E5E0` keeps entry 0 as it is².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B6528`-`0x003B6539`, `0x0046FB10`-`0x0046FB2E` |
| ² | `0x0033E690`-`0x0033E6EF` |

</details>

So while the counter is non-zero, `n - 1` passes, each blended value is a fixed mix of 0.1746 of the new values
and 0.8254 of the previous ones¹, and then it shows the new values.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B6546`-`0x003B65EC` |

</details>

### Advancing the channels

`0x003B5890`, called once per character-update pass from `0x00426090`¹, walks all 160 slots.
A slot advances when bit `0x1` of `+0x40` is set and bit `0x1` of `+0x41 | [0x02B40524]` is clear. It steps the
channels in the order `+0x00`, `+0x02`, `+0x01`, `+0x03`, `+0x43`: each with a non-zero counter adds
its step to its value and decrements the counter. The value is never snapped to the target, so it
ends within float rounding of it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00426112` |

</details>

`0x003B5C00(handle)` applies the same step to one slot without the
pause tests; `0x0041C850` and `0x0041D820` call it¹. It returns without writing when the
slot's `+0x10` is not the handle or bit `0x1` of its `+0x40` is clear².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0041C8E6`, `0x0041D9C6` |
| ² | `0x003B5C11`-`0x003B5C1E` |

</details>

### What the channels drive

`0x003B62D0(handle, out)` builds the slot's shadow draw record each frame and returns 1¹. It
returns 0 instead:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B67A0` |

</details>

- with nothing written, when the slot's `+0x10` is not the handle¹, when the slot's
  word `+0x04` is `0xFFFF`², when the render record's dword `+0x284` is 0
 ³, when `0x00421FF0` gives null for bone `+0x3C` or bone `+0x3E`⁴, or when `0x003B6BF0` gives null⁵;
- after out `+0x14`, `+0x6C`, `+0x10`, `+0x30` and `+0x20` are written⁶, when out
  `+0x10` is below 4 or above `0x64`⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B62EE`-`0x003B62FB` |
| ² | `0x003B6310`-`0x003B6314` |
| ³ | `0x003B632F`-`0x003B633D` |
| ⁴ | `0x003B6357`, `0x003B6374` |
| ⁵ | `0x003B6391`-`0x003B6394` |
| ⁶ | `0x003B63C6`-`0x003B641D` |
| ⁷ | `0x003B6425`-`0x003B642F` |

</details>

While counter `+0x43` is non-zero it blends
each channel value with the blend set by a weight from `0x0046FAE0`. Then:

- `+0x50`, `+0x54` plus `+0x48`, `+0x4C`, times `+0x44`, is an offset from the anchor bone, rotated by
  the character's facing (render record `+0x124`);
- `+0x58`, `+0x5C` multiply the shadow's two extents: out `+0x34 = s[+0x18] x [+0x08] x [+0x44] x [+0x58]`
  and `+0x38` the same with `s[+0x1C]` and `+0x5C`, `s` being the shadow record `0x003B6BF0` returns
 ¹;
- `+0x70` plus the facing plus `+0xBC` is the shadow's rotation (out `+0x24`);
- `+0x78` multiplies the strength term: out `+0x28 = [+0x0C] x s[+0x0C] x [0x01EFE314] x [+0x2C] x 0.5 x [+0x78]`
  (0.5 at `0x01CEBB70`; `0x003B64FA`-`0x003B6519`, `0x003B671A`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B64D2`-`0x003B64F5`, `0x003B6707`-`0x003B670C` |

</details>

The values used are saved at `+0xC0` to `+0xD4` for the next cross-fade.

## Layouts

<details>
<summary>Show the memory layouts</summary>

A command record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` |  | mask `0x7F` id, mask `0xFF80` length in bytes |
| `+0x02` | `...` |  | parameters: subtype bytes at +2/+3, words or floats from +4 |

A first-pool shadow slot (`0xE0` bytes, 160 at `[0x02B40528]`), the ramp fields:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` |  | counter, channel 0 (pair) |
| `+0x01` | `u8` |  | counter, channel 1 |
| `+0x02` | `u8` |  | counter, channel 2 (pair) |
| `+0x03` | `u8` |  | counter, channel 3 |
| `+0x10` | `u32` |  | handle: generation << 8 \| slot |
| `+0x40` | `u8` |  | bit `0x1` enabled |
| `+0x41` | `u8` |  | bit `0x1` paused, bit `0x2` hidden |
| `+0x43` | `u8` |  | counter, cross-fade |
| `+0x50` | `f32[2]` |  | channel 0: anchor offset |
| `+0x60` | `f32[2]` |  | its step |
| `+0x58` | `f32[2]` |  | channel 2: extent scales |
| `+0x68` | `f32[2]` |  | its step |
| `+0x70` | `f32` |  | channel 1: rotation |
| `+0x74` | `f32` |  | its step |
| `+0x78` | `f32` |  | channel 3: strength |
| `+0x7C` | `f32` |  | its step |
| `+0x80` | `f32[6]` |  | the cross-fade's previous values |
| `+0x98` | `f32` |  | cross-fade weight input |
| `+0x9C` | `f32` |  | its step |
| `+0xC0` | `f32[6]` |  | the values last built |

`0x003B56D0` takes the first of the 160 slots whose `+0x40` bit `0x1` is clear and returns 0 when no slot is free¹; it gives the slot the next generation from `0x02B40520`, wrapping to 1 above `0xFFFFFF`², and stores `generation << 8 | slot` at `+0x10`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B56F0`-`0x003B5707` |
| ² | `0x003B5719`-`0x003B5744` |
| ³ | `0x003B574A`-`0x003B5756` |

</details>

`0x003B6890` sets the generation to 0 when it allocates or resets the pool¹. It runs from the
start-up `0x004269A0`² and allocates only while `[0x02B40528]` is null, under arena 6 (`0x0036C1D0(6, 6)`,
`0x0036A100(0x8C00)`, `0x0036C140`; `0x003B689E`-`0x003B68BD`). Every call also zeroes the gate `0x02B40524`³; when
the pool exists it clears bit `0x1` of `+0x40` in all 160 slots, two a step⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B68C9`-`0x003B68CB` |
| ² | `0x00426C25` |
| ³ | `0x003B68D7` |
| ⁴ | `0x003B68DD`-`0x003B68F7` |

</details>

The pool pointer is stored untested¹. When both of `0x0036A100`'s attempts give 0 (`0x0036BC60`, then
`0x0036BFE0`), it returns 0², `[0x02B40528]` stays 0, and the first clear writes address `0x40`³, which faults.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B68B6` |
| ² | `0x0036A151`-`0x0036A154` |
| ³ | `0x003B68E2` |

</details>

[The ramp-channel access table](authored-presentation-commands-ramp-channel-record-accesses.tsv) lists every slot
field access of the 23 functions that load the slot base `0x02B40528`, among them the two ramp setters `0x003B6950`
(channel 3: `+0x03`, `+0x78`, `+0x7C`) and `0x003B69B0` (channel 1: `+0x01`, `+0x70`, `+0x74`).

The slot's other fields, from the take `0x003B56D0`, the builder `0x003B62D0`, the motion override keeper `0x003B5E20` and the setters `0x003B6B10`-`0x003B6BD0`:

`RampChannelRecord` (`0xE0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u16` | renderRecordId | the owner's character render record id: the take `0x003B56D0` stores it (`0x003B5726`); the builder `0x003B62D0` finds the record [`0x022C6F28`] + id * `0x740` (`0x003B62FC`-`0x003B6328`) and its shadow record `0x003B6BF0` (`0x003B637D`); `0x003B5980` reads it for the camera distance (`0x003B59AC`) |
| `+0x08` | `f32` | extentScale | a scale on both shadow extents: the builder's out `+0x34` = s[`+0x18`] * this * `+0x44` and out `+0x38` the same with s[`+0x1C`] (`0x003B64D2`-`0x003B64F5`); 1.0 at take (`0x003B573D`) |
| `+0x0C` | `f32` | opacity | a factor of the shadow's strength term, out `+0x28` = this * s[`+0x0C`] * [`0x01EFE314`] * `+0x2C` * 0.5 (`0x003B64FA`-`0x003B6519`); 1.0 at take (`0x003B574F`); `0x003B6B10` sets it (`0x003B6B26`), as the status visuals do with 1.0 while display is denied |
| `+0x14` | `f32` | fade | the shadow's fade level, 0 to 1: 1.0 at take (`0x003B572E`); `0x00426340` sets it through `0x003B6B80` (`0x003B6B96`) to record `+0x27C` or the camera-distance fade `0x003B5980`; the builder interpolates the shadow record's level ranges and size with it (`0x003B63A2`-`0x003B6404`) |
| `+0x18` | `f32` | offsetBias | an offset added to the anchor offset's first axis before the facing rotation (`0x003B6789`-`0x003B678C`, `0x003B67C2`); 0 from the take's qword store at `+0x14` (`0x003B572E`) |
| `+0x20` | `u32` | colourR | first component of the shadow colour: `0x003B6B30` copies it from its argument (`0x003B6B48`-`0x003B6B4A`); the builder copies it to out `+0x60` (`0x003B64C0`-`0x003B64C3`); 0 at take (`0x003B575F`) |
| `+0x24` | `u32` | colourG | second component of the shadow colour (`0x003B6B51`; to out `+0x64` at `0x003B64C6`); 0 at take (`0x003B575F`) |
| `+0x28` | `u32` | colourB | third component of the shadow colour (`0x003B6B58`; to out `+0x68` at `0x003B64CC`); 0 at take (`0x003B5765`) |
| `+0x2C` | `f32` | strengthScale | a factor of the strength term out `+0x28` (`0x003B650C`); `0x003B6BB0` sets it (`0x003B6BC6`), called by `0x0042D050`; 1.0 at take (`0x003B5769`) |
| `+0x38` | `u16` | anchorBone | the anchor bone in use, `+0x3C` or `+0x3E`: `0x003B5CE0` picks it (`0x003B5D22`-`0x003B5D32`) and the take starts it at `+0x3C` (`0x003B583D`-`0x003B5841`); while the cross-fade runs the builder blends from the previous anchor's bone to this one (`0x003B65FB`-`0x003B6662`) |
| `+0x3A` | `u16` | previousAnchorBone | the anchor bone before the last `0x003B5CE0` (`0x003B5D08`-`0x003B5D0D`); the builder blends from it while `+0x38` differs (`0x003B65FF`) |
| `+0x3C` | `u16` | boneA | the model's special bone `0x104` (`0x003E5AD0`, `0x003B57FA`-`0x003B5804`): the builder's first bone matrix through `0x00421FF0` (`0x003B6343`-`0x003B634F`) |
| `+0x3E` | `u16` | boneB | the model's special bone `0x106` (`0x003B582F`-`0x003B5839`): the builder's second bone matrix (`0x003B6360`-`0x003B636C`) |
| `+0x40` | `u8` | flags | bit `0x1` in use (set by the take `0x003B56D0` at `0x003B5759`-`0x003B57D0`, cleared by the free `0x003B6000` at `0x003B6016`); mask `0x1E` the overrides a motion keeps at `+0xA0`-`+0xB8` (`0x2` offset, `0x4` rotation, `0x8` extent scales, `0x10` base offset; `0x003B5E3F`-`0x003B5EF0`); bit `0x20` keeps the offset out of the cross-fade blend (`0x003B6549`-`0x003B6562`) and gives the bone blend a weight of 1 (`0x003B65F1`-`0x003B65F8`); bit `0x40` takes the shadow's height from element `+0x34` of the first bone's matrix instead of the ground (`0x003B645F`-`0x003B64A3`, read `0x003B647B`): with the bit set the builder writes out `+0x54` from that element (`0x003B647F`), out `+0x44` = 0 and out `+0x40` = shadow record `+0x14` plus `+0x10` (`0x003B6482`-`0x003B6490`); with it clear it writes out `+0x54` = `0x00264670`(render record `+0x108`) (`0x003B6497`-`0x003B64A3`), out `+0x40` = shadow record `+0x10` and out `+0x44` = shadow record `+0x14` (`0x003B64A8`-`0x003B64B1`); the bits under mask `0x7E` come from the motion block's word `+0x32` (`0x003B5F58`-`0x003B5FF4`) |
| `+0x44` | `f32` | offsetScale | a multiplier of the anchor offset and of both extents: `0x003B6BD0` sets it (`0x003B6BE6`), called by `0x0042D050`; the builder multiplies by it (`0x003B64DC`, `0x003B64F0`, `0x003B66E3`, `0x003B66E8`); 1.0 at take (`0x003B5770`) |
| `+0x48` | `f32` | baseOffsetX | the base offset's first axis, added to channel 0's value before the scale (`0x003B66C1`): `0x003B5CE0` stores it (`0x003B5D12`) after keeping the old one at `+0x30`; `0x003B5E20` restores a kept one from `+0xB4` (`0x003B5EE5`); 0 at take (`0x003B5848`) |
| `+0x4C` | `f32` | baseOffsetY | the base offset's second axis (`0x003B66CE`; `0x003B5D18`; restored from `+0xB8` at `0x003B5EF0`); 0 at take (`0x003B5848`) |
| `+0xA0` | `f32` | keptOffsetX | the anchor offset a motion keeps (block `+0x4C`, `0x003B5EFB`-`0x003B5EFE`), written back into `+0x50` and `+0x80` by the next motion while flag bit `0x2` is set (`0x003B5E49`-`0x003B5E67`) |
| `+0xA4` | `f32` | keptOffsetY | the kept offset's second axis (block `+0x50`, `0x003B5F08`; restored at `0x003B5E52`-`0x003B5E70`) |
| `+0xA8` | `f32` | keptExtentScaleA | the first extent scale a motion keeps (block `+0x10`, `0x003B5F47`), restored into `+0x58` and `+0x88` while flag bit `0x8` is set (`0x003B5EA4`-`0x003B5EC2`) |
| `+0xAC` | `f32` | keptExtentScaleB | the second kept extent scale (block `+0x54`, `0x003B5F51`; restored at `0x003B5EAD`-`0x003B5ECB`) |
| `+0xB0` | `f32` | keptRotation | the rotation a motion keeps, the block word `+0x32` >> 6 in degrees times 0.0174533 (`0x003B5F0F`-`0x003B5F27`), restored into `+0x70` and `+0x90` while flag bit `0x4` is set (`0x003B5E82`-`0x003B5E91`) |
| `+0xB4` | `u32` | keptBaseOffsetX | the base offset a motion keeps (block `+0x58`, `0x003B5F30`-`0x003B5F33`), restored into `+0x48` while flag bit `0x10` is set (`0x003B5EDE`-`0x003B5EE5`); moved as a dword, used as the f32 `+0x48` |
| `+0xB8` | `u32` | keptBaseOffsetY | the kept base offset's second axis (block `+0x5C`, `0x003B5F3D`; restored into `+0x4C` at `0x003B5EE9`-`0x003B5EF0`) |
| `+0xBC` | `f32` | lookRotation | a rotation added to the shadow's rotation after the facing (`0x003B6712`): `0x003B6B60` sets it (`0x003B6B76`) from the look controller; 0 at take (`0x003B5850`) |

</details>

## State

<details>
<summary>Show the state it keeps</summary>

| Address | Holds |
|---|---|
| `0x01EFFAF0` | the pair table, 76 x 16 bytes |
| `0x02CA4410`, `0x02CA4670` | bank A and bank B, 75 pointers each |
| `0x02B40528` | the first shadow pool, `0x8C00` bytes allocated once by `0x003B6890` |
| `0x02B40520` | the pool's generation counter |
| `0x02B40524` | the pool gate: `0x003B6930(v)` keeps the gate bits that `v >> 2` keeps and adds `v & 3`; its callers give it 4 or 6, which clear or set bit `0x2` (hide), so bit `0x1` stays clear |

### Every use of these commands

[`fmc-resource-occurrences-1.tsv`](fmc-resource-occurrences-1.tsv) has one row for each use of the commands that
name something else: 224,124 rows. `decoded` spells the operand, `link_kind` and `link` give what it names, and
`owner_status` and `owners` give the playing models, as for the [sound rows](../Sound-And-Music/animation-sounds.md).

| `id` | Rows | `link_kind` | `link` |
|---|---|---|---|
| `0x09` | 155,855 | `fmn_slot` | the `@FMN` slot the command starts; `finish_flag` in `decoded` is bit `0x1` of the word (`0x004185AA`) |
| `0x11` | 10,617 | `bone_trail_commands` | the file's rows in [`bone-trail-commands.tsv`](bone-trail-commands.tsv) |
| `0x18` | 30,769 | `effect_by_ground` | the table from ground type to effect id, because the effect follows the ground |
| `0x1A` | 12,876 | `profile_row` | the row of the file's movement profile table for the mode |
| `0x3F`, `0x48` | 7,617 | `preset_row` | the row of the table at `0x01EFFA30` (`0x0040ACA3`) |
| `0x48` | 6,390 | `no_preset` | preset 0, which sets nothing (`0x0040AC2E`) |

The effect ids of `0x18` (`0x64` to `0x67` and `0x94`) are not joined to files, and the ground under the actor picks
among them while the game runs. `0x09`'s `finish_flag` is the word the playback page uses for bit `0x4` of `+0x96`.

</details>

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 4 calls with 2 other topics</summary>

**Scripts and script commands**

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0036A100`](../Game-Files-And-Data-Tables/resource-lifecycle.md) (on resource lifecycle) | is called by | [`0x0050D8F0`](../Game-Files-And-Data-Tables/resource-lifecycle.md) (on resource lifecycle) |

**World, areas and travel** (explained on [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md), [frame update order](../Engine-Core/frame-update-order.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0036A100`](../Game-Files-And-Data-Tables/resource-lifecycle.md) (on resource lifecycle) | is called by | [`0x00267930`](../Compiler-And-C-Runtime/memory-and-allocation.md) (on memory and allocation)<br>[`0x003319D0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x003EA820`](../Game-Files-And-Data-Tables/ard-area-battle-data.md) Area ard: load or unload field resource (on ard area battle data) |

</details>
