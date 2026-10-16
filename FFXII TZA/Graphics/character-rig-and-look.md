---
title: "Character rig and look: the seventeen procedural controllers, the staged look command and the focus point"
kind: "system"
category: "Graphics"
addresses: "003E1350, 003E1610, 00370E20, 003E6DA0, 003E00C0, 00427DE0, 0042DD90, 0042EE90, 002E8570, 002EDF30, 002EE0D0, 002EDE70, 002EDDC0, 002E75A0, 0042BDE0, 004718D0, 00471640, 004716A0, 00471150, 00427320, 00518F50, 003DFE70, 0042BED0, 00520430, 0051A890, 003E37F0, 00429920, 003E37E0, 002EC3F0, 003E2FD0, 003E3200, 003E2F30, 003E3340, 003E0910, 003E2810, 003E3D70, 00426220, 003E43D0, 003E5ED0, 003E5FA0, 003E6070, 003E5810, 004288E0, 0042C410"
---

## What the player sees

- A talking character flaps its mouth, nods and shakes its head; scripts switch these on and off around message
  windows, and a third of the script corpus does so.
- Heads turn toward a point or a person over a number of frames and relax back; eyes move on their own.
- A Confused character sways, and stops while it is also Asleep; an Immobilized character has its own motion; a
  Floating character bobs up and down and settles when Float ends.
- A character hit without dying is shoved for eight frames.
- Monsters and summons can have bones that spin at a speed that ramps up or down.
- When another character or the camera aims at a character, it aims at a point the model places, which slides
  instead of jumping when its source changes.

## How it works

### The rig and its two switches

The rig is the encoded pointer at `+0x94` of a character's resource entry (`00370E20`); `003E6DA0` returns it for a
render record. Its first seventeen dwords are encoded pointers, one per controller, resolved through `0020E600` on
every use: controller *n* is the dword at `+4n`.

`003E1350(rig, n)` switches controller *n* off and `003E1610(rig, n)` switches it on. Both refuse `n > 16`
(`003E1350`, `003E1610`: `cmp edx, 0x10`), jump through a seventeen-entry table (`003E15C8`, `003E1888`), resolve the
controller and tail-jump to its own off or on routine. Entry 4 of both tables goes straight to the exit: slot 4 has no
controller.

| n | Offset | Controller | On, off | Switched by |
|---:|---|---|---|---|
| 0 | `+0x00` | per-model oscillators, updated by `0040B180` | `004158E0`, `0040EE90` | - |
| 1 | `+0x04` | bone physics | `00512C00`, `00512A80` | `denybonephysical` |
| 2 | `+0x08` | the look controller | `00515600`, `00513150` | request bit 1 of the staged look |
| 3 | `+0x0C` | Confuse motion | `00515FE0`, `00515610` | the Sleep and Confuse arms |
| 4 | `+0x10` | none | - | - |
| 5 | `+0x14` | bone turn that the shadow follows | `0051B110`, `0051A370` | the rig rebind |
| 6 | `+0x18` | Float bob | `004718D0`, `00471640` | the Float arm |
| 7 | `+0x1C` | Immobilize motion | `004715D0`, `00471380` | the Immobilize arm |
| 8 | `+0x20` | solve `00516220`, apply `00516970` | `00517590`, `00516200` | the rig rebind |
| 9 | `+0x24` | lip flap | `00518820`, `005175C0` | `setkutipakustatus`; authored command `0x13` |
| 10 | `+0x28` | eyes | `007A3A90`, `005188B0` | `eyemove_381`, `eyemovediff_383` |
| 11 | `+0x2C` | rotators | `00519870`, `00519720` | authored command `0x13` |
| 12 | `+0x30` | hit flinch | `00471310`, `00471140` | HP events `0x2005`, `0x2006` |
| 13 | `+0x34` | nod | `00472550`, `004719A0` | `setunazukistatus`; authored command `0x13` |
| 14 | `+0x38` | bone physics, second | `0051A320`, `00519A20` | `denybonephysical` |
| 15 | `+0x3C` | head shake | `00472950`, `00472810` | `setkubifuristatus` |
| 16 | `+0x40` | body shake | `0051B950`, `0051B840` | `setbodyshake` |

The status arms are on [Character status visuals](character-status-visuals.md): Float switches 6, Immobilize 7, and
Confuse switches 3 on unless the Sleep flag is set, while Sleep switches it off for a Confused character and back on
when it ends. Each also sets bits 1 (asleep) and 2 (confused) of the look controller's byte `+0x1C`.

### Record flags and the dirty pass

Scripts do not call the switches. A verb's service sets a bit in render record `+0x304`, raises a dirty bit in
`+0x290`, and the record pass `00427DE0` later calls one wrapper per bit:

| `+0x304` bit | Dirty bit | Controller | Setter |
|---|---|---|---|
| 6 | 13 | 9 lip flap | `002E8570`; timed `002EDF30` |
| 7 | 14 | 13 nod | `002EE0D0`; timed `002EE130` |
| 15 | 15 | 15 head shake | `002EDE70`; timed `002EDED0` |
| 8 | 17 | 10 eyes | `002E75A0`, from the `eyemove_381` and `eyemovediff_383` handlers |
| 16 | 16 | 16 body shake | `002EDDC0`, which also stores the amount at `+0x4BC` |

Each setter refuses a record whose `+0x284` is 0. The plain forms zero the timer; the timed forms store
`frames / [01DFE0BC]` at `+0x640` (lip flap), `+0x644` (nod) or `+0x648` (head shake).

The division happens in the actor-side wrappers the timed verbs call: `setkutipakustatus_4a2`
(`00352B90`) uses `002E85E0`, `setunazukistatus_4a3` (`00352F20`) `002E8B80` and
`setkubifuristatus_4a4` (`0034F9B0`) `002ED320`. Each takes the render index from the first dword
of the actor's `+0xC0` object, does nothing when it is −1, and passes `frames / [01DFE0BC]` to the
timed setter.

The wrapper (`0042DD90` for the
lip flap, `0042E690`, `0042D8B0`, `0042DCD0`, `0042BDE0` for the others) runs on the record, its first child and the
child's subtrees, skips records `00426220` rejects, and switches the controller on when the owner's bit is set and off
when it is clear. The body-shake wrapper first copies `+0x4BC` into the controller's `+0x38`. After the walk the sync
routine (`00429C40` for bit 6) copies the bit into byte `+0x40B` (bits 5, 6, 7 for the three talking-head bits).

`00426220(record, owner)` returns 1, and the wrapper skips the record, when the record is not the owner, its `+0x284`
bit 26 is clear and its word `+0x2F8` is -1; when its bit 27 is set, its word `+0xCC` is below `0x1000` and `004232D0`
answers 0; or, for a record that is not the owner, when its byte `+0x3C` is not `'h'` and the owner's is `'b'`, or when
it is `'h'` and its bytes `+0x3D`-`+0x41` differ from the owner's `+0x3C`-`+0x40`.

### The countdown

`00428F80` walks the active-record list (head at `[022C6F28] + 0x48800`, next at each record's word `+4`) and calls
`0042EE90` on each. Unless bit 1 of `+0x290` is set, for each timer whose `+0x40B` bit is set and whose value is not 0,
it subtracts `[01DFE0BC]`; at 0 or below it clears the `+0x304` bit, zeroes the timer and calls the same sync routine.
A timed lip flap ends exactly as `setkutipakustatus(0)` would, and a zero timer never counts down.

### The Float bob

On (`004718D0`) sets the active byte `+0` and the running byte `+3` and remaps the counter `+2` through `01F227A0`; off
(`00471640`) clears `+0` and remaps `+2` through `01F22760`. The update `004716A0`:

- active: the envelope `+0x10` rises by `0.125 × [01DFE0BC]` to 1.0; the phase `+1` steps round the 60-entry cycle
  `01F223B0`; the height `+0x14` = cycle[phase] × envelope; `+0x18` = 0.3 × the 28-entry rise curve `01F22590` at
  `+2`, held at its last entry;
- inactive: the envelope falls at the same rate, the phase holds, `+0x18` = 0.3 × the 30-entry settle curve
  `01F22670`, and the running byte clears when `+2` reaches 30.

### The hit flinch

The record event handler `00427320` switches controller 12 on for event `0x2005`, which the HP write posts for a target
that survives ([HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)), when the argument record's byte `+1` is 0 and the
motion word `+0xCC` is not `0x2009` or `0x2031`, nor `0x2001` with `+0x2A0` equal to 0 or 14. For `0x2006` it switches it
on when `00422DE0` puts the motion word in class 3.

The update `00471150` steps a counter `+0xD` through the eight-entry
curves `01F22130` and `01F22170`, scales them by `+0x10` and turns them by the heading `+0x124` into the offset
`+0x20`, `+0x28`; at the end of the curves it stops the controller.

### Rotators and authored commands

The update `00518F50` walks `0x60`-byte entries (count at controller `+4`). For each enabled entry, while its counter
is non-zero it counts down and adds the acceleration to the speed (at 60 fps only on odd counts); the angle advances by
`speed × [01DFE0BC]`, wraps at ±2π, and becomes a 2 × 2 rotation through the sine table `01F004E0`.

Two authored presentation commands of the bank `0041D6C0` registers drive the rig
([Authored presentation commands](authored-presentation-commands.md)):

- `0x13` (`00520430`) copies command bytes `+2`-`+5` to render record `+0x3F4`-`+0x3F6`. With bit `0x40` of `+0x3F4`
  set, the dirty-pass wrapper `0042BED0` switches controller 11 by bit 0 when the target word `+0x3F6` is 1, the lip
  flap when it is 2, and the nod when it is 4 and `+0x3F5` is 0 or the record's piece number plus 1.
- `0x24` (`005201B0`) calls `003DFE70(rig, index, target, frames)`, which sets the entry's counter to
  `frames × [01DFE0B4]` and the acceleration to `(target - speed) / frames`, or the speed itself when frames is 0.

- `0x25` (`00520320`) calls `003DFF20(rig, index, frames)`, which does the same toward the entry's
  default speed `+0x0C`: counter `+0x10` = `frames × [01DFE0B4]`, step `+0x14` = `(default − speed) /
  frames`, or the speed `+0x08` set to the default at once when frames is 0.

The lip flap and the nod of the `0x40` branch go through `003E12A0`, which `0041DD40` also calls for
both with 1.
Without bit `0x40`, `0042BED0` switches on `+0x3F4 & 0xB9`. In the first four cases `n` is
`+0x3F5 & 0x1F`, the value is word `+0x3F6`, and the top three bits of `+0x3F5` must be 0 or the
record's piece number (`+0x413`) plus 1:

| Case | Call | What it does |
|---|---|---|
| 0 | `003E0B50(rig, n, entry)` | for `n` = 0 switches oscillator entry `entry` off (see [model oscillators](model-oscillators-and-pose-sequencer.md)); for `n` = 11 clears rotator entry `entry`'s `+0x18` |
| 1 | `003E0F00(rig, n, entry)` | the same, switching on |
| 8 | `003E0E70(rig, n, id)` | case 0 for the entry whose id matches: `0040DB00` for oscillator entries (word `+0x2A >> 4`), `00519100` for rotators |
| 9 | `003E1210(rig, n, id)` | case 1 by id |
| `0x10` | `003E1950(rig, 0)`, or `003E1350(rig, 0)` | every oscillator entry off when the broadcast's `+0x70` is set, otherwise controller 0 off |
| `0x11` | `003E1950(rig, 1)`, or `003E1610(rig, 0)` | the same, on |
| `0x20` | inline | rig `+0x58` = `1 / +0x3F5` (1.0 for 0); the low nibble of rig byte `+0x5E` = `+0x3F6` when it is below 3, else 3; its high nibble from `+0x3F7`; sets bit 0 of rig `+0x5F` |
| `0x80` | `003E6F90` / `003E7040` | on the source record itself stores `003E6F90(record, byte +0x40A)` at the broadcast's `+0x6C`; on another record passes that value to `003E7040` |

`003E0860(rig)`, from `002E4150`, calls one routine of each of five controllers that exist: 2
(`005154B0`), 10 (`00518E60`), 13 (`004719F0`), 15 (`00472820`) and 9 (`005175F0`).

### Look parameters from the motion

The look controller (slot 2) also keeps a table of `0x60`-byte entries (pointer `+0x00`, count byte
`+0x04`) and two float pairs, `+0x20`/`+0x24` and `+0x28`/`+0x2C`. When the authored motion command
`0x09` (`00417F40`) starts a motion whose header has bits 24–25 of `+0x04` equal to 2, it loads them
from the header's block for the header kind (`+0x04 & 3`): kind 0 reads byte `+0xBE`, floats from
`+0x44` and the pairs `+0x30`/`+0x34` and `+0x3C`/`+0x38`; kind 1 reads byte `+0xEE`, floats from
`+0x74` and `+0x60`/`+0x64`, `+0x6C`/`+0x68`.

Bit 7 of the byte sets bit 0 of the render record's `+0x66D`.

- `003E2D20(rig, n)`, with the byte's low three bits, stores `n` at the controller's `+0x06` when it
  changes. With the high nibble of `+0x05` clear each entry's `+0x08` takes its value `+0x50 + 4n` at
  once; otherwise the entry counts `+0x1C` = 6 × `[01DFE0B4]` steps of `(+0x08 − value) ×
  [01DFE0BC] / 6` at `+0x0C`.
- `003E2EA0(rig, floats)` copies one float per entry into the entry's `+0x04`.
- `003E3460(rig, a, b)` ramps `+0x28` and `+0x2C` toward `a` and `b`, and `003E3590` ramps `+0x20` and
  `+0x24`: each changed value gets a step of `(target − current) × [01DFE0BC] / 8` and a counter
  of 8 × `[01DFE0B4]` (`+0x48`, `+0x4C`, `+0x3A`, `+0x3B`; `+0x40`, `+0x44`, `+0x38`,
  `+0x39`).

`003E3400(rig, m)`, from the look switch `003E29F0`, puts `m` in the low nibble of `+0x1D`.
`003E2CD0(rig)`, from `00422940`, returns source A's first dword when the controller is on (low
nibble of `+0x05`) and source A is of kind 1, or −1. `003E1C10(rig, v)`, from `00372710`, stores `v`
at rig `+0x60` when the oscillator record's byte `+0x06` is set.

### Controller 5 and the shadow

`0051A890` runs after controller 5's solve when bit 1 of the controller's byte `+0x17` is set, the render record has a
shadow (`+0x114`) and the controller's byte `+0x14` is set. It stores `-(angle × weight)` of the first entry into the
shadow's `+0xBC` (`003B6B60`) and writes into the look controller's byte `+7` whether the controller's dword `+4` is
non-zero. The rig frame zeroes the shadow's `+0xBC` first every frame.

### The rig frame

`003E00C0(rig)`:

1. Slot 0's update `0040B180` runs when its byte `+6` is set, with the rig's flag byte `+0x63` ORed with `02B59D60`,
   which the image only reads. Its time input is the rig's `+0x58`, or 0 while slot 0's byte `+7` is set.
2. When that OR is non-zero, nothing else runs. Otherwise it calls `003E29F0(rig, 2, 1)` and `003E3C30`, and zeroes the
   shadow's `+0xBC`.
3. Solve, each behind its controller's own active field: 10, 8 (only when `00181DD0` is 0 and `001EDE80` is not), 1, 2,
   9, 11, 13, 15, 14, 5 and `0051A890`, 16, 6, 7, 12, 3, then `0051B330` (16), `00519170` (11) and `00518D50` (10).
4. Apply 2, 9, 13, 15 while bit 1 of the rig's `+0x5F` is clear; then 8, 1, 14, 5, 12 while also the rig's byte `+0x62`
   (bone physics denied) is 0 and `02B59D64` is 0.
5. Apply 7, 3 and 6 (`004717E0`) while `02B59D68` is 0. Only the display-deny latch `003E7C70` writes `02B59D68`.

The nod and the Confuse motion share the apply `00471E40`; the flinch and the Immobilize motion share `00471230`.

`004717E0`, the Float bob's apply, writes nothing while `001ED1E0` answers 1: in 60 fps mode
(`01F82E38`), during an event (`001EC560`), at story progress `0x14B7` (`00265270`) with the count
of the marked event slot (`01DFE40C`, `01F832B0`) at 4.

### Solve bodies

| Controller | Solve | What it does |
|---|---|---|
| 1 bone physics | `005121A0` | with byte `+0x35` bit 2: an angle step wrapped at ±3.14, its rate `+0x1C` below 0.03 rad or `+0x24` above, clamped, turned into an axis-angle rotation for each of the `+0x34` entries |
| 7 Immobilize | `004713A0` | an envelope `+0xC` that falls by `0.375 × [01DFE0BC]`; while active, the cycle `01F221C0` / `01F222B0` (length `01F221B0`); the offset turned by the heading `+0x124` into `+0x20`, `+0x28` |
| 13 nod | `00471B60` | an envelope `+0x2C` moving by `0.125 × [01DFE0BC]`; pattern `+0x10` (0 to 7, 8 fading out) plays per-bone curves picked by `004723E0` and rebuilds each bone's rotation with `0046D560` |
| 15 head shake | `00472970` | the same envelope on three bones; patterns 0 to 4 from `01F24160`, `01F24870`, `01F24F80`, `01F25690` and `01F25DA0`, state 5 a countdown, state 6 a fade that then picks one of eight next patterns at random (`003A6E60(8)`) |
| 14 bone physics, second | `00519B60` | normalises its direction `+0x70` and classifies the motion against it into a state in byte `+0x32` |
| 16 body shake | `0051B150` | rebuilds its rotation (`0046D560`) and steps a counter `+0x30` that wraps at `30 × [01DFE0B4]` |

Controller 14's apply `0051A280` (`003E0624`) multiplies the rotations of three bones, named by
`+0xC0`, `+0xC4` and `+0xC8`, by the controller's three 3 × 3 matrices at `+0x00`, `+0x40` and `+0x80`
through `00519880`.

- `003E12A0(rig, n, on)` fades controller 9 or 13 instead of cutting it: off sets bit 6 of byte `+1`
  (`00517610` keeps the lip flap's current values at `+0x88` and `+0x8C`; `00471B20` clears the
  nod's byte `+8`), and on restarts a controller that was fading. Its callers are `0041DD40` and
  `0042BED0`.
- `003E0740` resets the talking-head controllers of every active record; the lip flap's reset is
  `005175F0`.
- `0051A780(controller, mode, angle)` and `0051A920(controller, which)` set controller 5's target
  angle: each entry ramps from its current value to the target over its frame count times
  `[01DFE0B4]`; `0051A920` takes one of four stored angles (words `+0x08`–`+0x0E`, in hundredths).
- `00519100(controller, id)` returns the index of the rotator entry with that id (`+0x1C` of each
  `0x60`-byte entry), or `0xFFF`; authored command `0x24` (`005201B0`) uses it.
- `00512EC0(controller)` returns `002E9B80(+0x08)` when the low nibble of `+0x0F` is 1, else −1.
  `00512EF0`, run with `0040DB70` from `003E0720`, numbers the 32 entries of the table at
  `02CA81FC` and clears `02CA83F0`, `02EBA480` and `02EBA481`.

- `002E7C10(actor, target, …, keep)` aims an actor's record at another's: it hands
  `{3, own index, own index, target index}` to `00512F30` on the record's `+0x650` block, which for
  kind 3 stores the three values there and sets the low bits of `+0x65F` to 3 unless the target is
  the record itself, and it stores the target in word `+0x24C` when `keep` is set, else −1. Its
  record form `003E6C10(record, target, …, keep)` does the same.

### Binding the rig

`003E1C50(rig)`, run through `003713C0` whenever a model's rig section is bound, resolves the two
render records the rig names (words `+0x68`, `+0x6C`) and then fixes the controllers' stored
offsets. The rig keeps its own address at `+0x84`:

- when `+0x84` is 0, each controller's offset becomes an encoded pointer and the controller's own
  inner offset is rebased: `004719B0` (controllers 2, 3, 10, 11, 13; inner `+0x00`), `00512A90`
  (1; inner `+0x30`) and `0051A380` (5; inner `+0x10`), while `0051B850` only stores the pointer
  (6 to 9, 12, 14 to 16);
- when `+0x84` holds another address, the rig has moved and the inner pointers get the difference
  added: `00512C50` (1), `0051B120` (5) and `005161D0` (the others with an inner pointer).

### At 60 fps

When the frame rate is 60, `0033F020` doubles the length of each controller curve table and
refills it with the original entries at even positions and the midpoints of neighbours at odd
positions (`0033E310` for float tables, `0033E990` for byte tables, and the variants `0033E5E0`
and `0033ECE0`):

| Routine | Tables |
|---|---|
| `00471330` | the flinch curves `01F22130`, `01F22170` (length `01F22120`) |
| `004715F0` | the Immobilize cycle `01F221C0`, `01F222B0` (length `01F221B0`) |
| `004718F0` | the Float cycle `01F223B0`, rise `01F22590`, settle `01F22670` and the remap tables `01F22760`, `01F227A0` |
| `00472580` | the nod: doubles the lengths at `01F227E0` (copied as bytes to `01F240F0`), halves the per-pattern scales from `01F23FF0`, and stretches the sixteen curves from `01F22800` to `01F23E88` |
| `00473210` | the head shake: doubles the lengths at `01F24100` (copied to `01F264A8`), halves the scales from `01F24118`, and stretches the patterns from `01F24160` to `01F26250` |

### The staged look command

A request to turn a character's head or eyes is staged in a `0x50`-byte command at render record `+0x580`. Eighteen
forwarders, each `add rcx, 0x580` then a jump, lead to eighteen builders that set a request bit in the dword `+0`, set or
clear its value bit, clear the bits of the same group and store a payload
([character-rig-and-look-look-command-census.tsv](character-rig-and-look-look-command-census.tsv)).

`00429920` applies it: for the record, its first child and the child's two subtrees (callback `0042D970`), it skips
records `00426220` rejects, takes the rig from `003E6DA0` and calls `003E37F0(rig, command)`. Then `003E37E0` zeroes the
command, so a request lasts one pass and an attached piece looks where its owner looks.

| Request bit | Value or payload | What `003E37F0` does | Builder, verb |
|---|---|---|---|
| 0 | bit 22 | `003E0910(rig, value)` | `003E0B20`, `denybonephysical` |
| 1 | bit 23 | look controller `+0x1C` bit 0 := value; on `00515600`, off `00513150` | `003E33E0` |
| 2 | bit 24 | low nibble of `+0x1D` := value | `003E3440` |
| 4 | bit 26 | low nibble of `+0x1E` := value | `003E37C0`, `lookat_maxangle_limit_lock` and `_unlock` |
| 5, 6 | - | `+0x8C` := 1, 0 | no builder |
| 9 with 10 or 11 | `+0x20`-`+0x28` | `+0x60`-`+0x68`, source kind `+0x6C` := 0 (three dwords) or 1 (two) | `003E36F0`; `003E36C0`, `lookatsrcboneid` |
| 12 with 13 or 14 | `+0x30`-`+0x38` | `+0x50`-`+0x58`, source kind `+0x5C` := 0 or 1 | the same two builders |
| 15, 17 | floats `+4`-`+0xC` | angles: `003E2FD0`, or `003E30A0` with a minimum duration | `003E31E0`, `003E3120` |
| 16, 18 | floats `+4`-`+0xC` | direction from an angle: `003E3200`, or `003E3140` | `003E3320`, `003E31C0` |
| 19, 20 | float `+4` | blend: `003E2F30`, or `003E3340` | `003E33C0`, `003E33A0` |
| 27, 28 | floats `+0x40`-`+0x48` | eyes: `003E2810`, `003E28F0` | `003E29D0` `eyemove_381`, `003E29B0` `eyemovediff_383` |
| 29 | - | zeroes the eye object's `+0x2C`, `+0x14`, `+0x18` | `003E2800`, `eyemovereset` |
| 30 | bit 31 | `003E3720`: look `+0x1C` bit 5 := value; set with bit 0 clear starts the neutral return | `003E37A0` |

Bits 15 to 20 are one group, tested in the order 15, 17, 16, 18, 19, 20; the first set one runs. `003E36A0` (bit 7) and
`003E3570` (bit 8) are staged only from the bind path `002E28E0`, and `003E37F0` does not test them.

### Angles, blends and the eyes

- `003E2FD0(rig, frames, a, b)` stores the two angles at `+0x50`, `+0x54` and sets both source kinds to 2. `003E3200`
  sets them to 3 and stores the direction `(sin a, 0, cos a)` from the sine table at `+0x60`-`+0x68`.
- Both, and the plain blend `003E2F30`, set `+0x88` = 1, zero the progress `+0x70`, set the rate `+0x74` = 1 / frames
  (`[01DFE0BC]` when frames is 0), set `+0x3C` when `01F82E38` is set, clear the high nibble of `+0x1E` and copy
  `+0x10`, `+0x14` to `+0x78`, `+0x7C`.
- The minimum-duration forms (`003E3340`, `003E30A0`, `003E3140`) first raise frames to `[01DFE0B8] × controller +0x18`.
- The on routine `00515600` sets byte `+5` to `0x11`. The off routine `00513150` does nothing when the low nibble of
  `+5` is clear; otherwise it clears it and the low nibble of `+0x1D`, sets `+0x1E` to `0x11`, zeroes the progress, sets
  the rate to `[01DFE0BC] / +0x18` (`[01DFE0BC]` when that is 0) and copies the current angles to `+0x78`, `+0x7C`.
- `003E2810(rig, frames, x, y)` writes the eye object (slot 10): timer `+0x2C` = frames, velocity `+0x1C`, `+0x20` =
  (target − current) / frames, current at `+0x14`, `+0x18`. Frames under 1 become `[01DFE0B8]`; the timer is stored
  negated when `01F82E38` is set. `003E28F0` takes the pair as a displacement.

### Where head-look requests come from

`002EC3F0(actor)` turns the steering record `[[actor + 0xB8] + 0xF0]` into a staged look for an actor whose byte `+3`
has `0x60` in its top three bits ([Facing and steering](../Movement-And-Pathfinding/facing-and-steering.md)). The
shape is bits 0-2 of the record's byte `+0x62` and the selector bits 3-5; selector 2 becomes 1 when bit 0 of `+0x6A`
is set, and that bit is cleared.

| Shape | Selector 1 | Selector 2 |
|---|---|---|
| 0, 1 | `002E7650`, bit 19 | `002E79A0`, bit 20 |
| 2 | `002E7720`, bit 15 | `002E77F0`, bit 17 |
| 3 | stages bit 16 with 0 frames and the angle pair `+0x10`, `+0x14` (`003E6B90`), then bits 9/11 and 12/14 with the pair (the actor's record index, `0x30B`) (`003E6C00`); raises dirty bit 11 | stages bit 18 with 1 frame and the angle pair (`003E6B70`); raises dirty bit 11 |

### Bone physics and the rebind

`003E0910(rig, deny)` stores the flag at rig byte `+0x62`. Only when the value changes to 0 does it reset and
re-initialise the two bone-physics slots (`00512AD0`, `00512C00`; `00519A30`, `0051A320`), so physics resumes from
rest.

`00372350(entry, record)` stores the record index at rig `+0x68` and calls `003E3D70`, which re-resolves the rig's two
linked records (`+0x68`, `+0x6C` into `+0x70`, `+0x74`) and their bone arrays (`00421D20`, into `+0x78`, `+0x7C`), resets
the additive bone matrices, calls each slot's reset and then its second-phase initialiser, and resets the rig's
`+0x5C`-`+0x60`. It also calls `003E3C30`.

### The focus point

`004288E0` walks the active-record list and calls `003E43D0` on every record whose `+0x290` bit 1 is clear:

1. `003E5ED0` picks a local offset. When the record's resource (`+0xF0`) has an `@FRM` chunk with a non-zero sub-block
   (`004234B0`), it is kind 1 and the offset is the block's `+0x3C`; otherwise kind 0 and the three floats at `+0xD4`
   of the model block (record `+0x400`, entered through its word `+2`). In kind 1 the height still comes from the model
   block unless bit 0 of `+0x66D` is set.
2. `003E5FA0` gives the frame: for kind 1 with a model block of version 3 or later naming a bone (the first of the words
   `+0x3A`, `+0x3C`, `+0x3E` that is not `0xFFFF`), that bone's matrix; otherwise the record's matrix `+0x180`. Only its
   translation is kept, the rows come from `+0x180`, and the height is replaced by `+0x1B4` unless bit 0 of `+0x66D` is
   set. The result goes to `+0x670`.
3. Byte `+0x66C` holds two countdowns, the high nibble for kind 1 and the low for kind 0. While the current kind's is
   non-zero, the point is pulled toward the other kind's last point (`+0x690` for kind 1, `+0x660` for kind 0) by
   `ease(n / (8 × [01DFE0B4]))` from the 60-entry table `01F20C80` (`0046FAA0`).
4. It saves the point as this kind's last and reloads the other kind's nibble with `8 × [01DFE0B4]` truncated to four
   bits: 8 at 30 fps, 0 at 60 fps, so at 60 fps a change of kind jumps. `0042C410`, from the record pass, lowers each
   non-zero nibble by 1.
5. `003E6070` fetches a second vector (`@FRM` block `+0x60`; else the `@FRM` chunk of the resource behind `+0x69C`, or
   behind `+0x430` when the motion word's low twelve bits are `0x36`; else model block `+0xEC`; else 0), and `+0x680`
   follows it by `sqrt(0.12)`, about 0.35, a frame; bit 1 of `+0x66D` snaps it once. `+0x6A8` gets 0.

`003E5810(record, out)` returns `+0x670` plus `+0x680` turned by the record's matrix. Its callers are `003A4290`, which
also copies the view matrix at `02AEDEF0`, `003A56F0`, and the actor service `002E9A90`. The record initialiser
`0041F730` zeroes `+0x66C` and sets the snap bit.

## Layouts

Rig (resource entry +`0x94`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32[17]` | slots | encoded controller pointers, slot 4 empty |
| `58` | `u32` | time | slot 0's time input |
| `5F` | `u8` | flags | bit 1 skips the look and physics applies |
| `62` | `u8` | denyPhys | bone physics denied |
| `63` | `u8` | sway | non-zero runs slot 0 only |
| `68` | `i16[2]` | linked | record indices |
| `70` | `u32[2]` | linkedRec | encoded record pointers |
| `78` | `u32[2]` | linkedBones encoded bone arrays |  |

Staged look command (render record +`0x580`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | request | bits as in the table above |
| `04` | `f32[3]` | target | frames, a, b |
| `20` | `u32[3]` | sourceA |  |
| `30` | `u32[3]` | sourceB |  |
| `40` | `f32[3]` | eyes | frames, x, y |

Look controller (rig slot 2):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `05` | `u8` | mode | low nibble; `0x11` when on |
| `10` | `f32[2]` | angles | current |
| `18` | `f32` | duration | minimum blend frames |
| `1C` | `u8` | state | bit 0 on, 1 asleep, 2 confused, 5 neutral |
| `1D` | `u8` | modes | low nibble from request bit 2 |
| `1E` | `u8` | limits | low nibble the angle lock |
| `50` | `f32[3]` | sourceB |  |
| `5C` | `u32` | kindB | 0 vector, 1 bones, 2 angles, 3 direction |
| `60` | `f32[3]` | sourceA |  |
| `6C` | `u32` | kindA |  |
| `70` | `f32` | progress |  |
| `74` | `f32` | rate |  |
| `78` | `f32[2]` | start |  |
| `88` | `u32` | blending |  |

Render-record fields:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `304` | `u32` | flags | bits 6, 7, 8, 15, 16 the controller requests |
| `40B` | `u8` | timedOn | bits 5-7 copies of the talking-head bits |
| `4BC` | `f32` | shake | body-shake amount |
| `640` | `f32[3]` | timers | lip flap, nod, head shake |
| `660` | `f32[3]` | lastKind1 |  |
| `66C` | `u8` | slide | high nibble kind 1, low nibble kind 0 |
| `66D` | `u8` | focusFlags bit 0 keep the source height, bit 1 snap |  |
| `670` | `f32[4]` | focus |  |
| `680` | `f32[4]` | second |  |
| `690` | `f32[3]` | lastKind0 |  |

## Shipped data

Counts of the talking-head verbs in the 1,114 decompiled `us` scripts
([character-rig-and-look-rig-verbs-census.tsv](character-rig-and-look-rig-verbs-census.tsv)), and tables from the
executable image.

| Fact | Value |
|---|---|
| `setkutipakustatus` | 28,035 calls in 354 scripts; 14,201 with 1 and 13,834 with 0 |
| `setunazukistatus` | 26,389 calls in 347 scripts |
| `setkubifuristatus` | 1,179 calls in 164 scripts |
| timed forms `_4a2`, `_4a3`, `_4a4` | 160, 122 and 6 calls; the commonest lengths 150, 210 and 90 frames |
| staged-look forwarders | 18, found by pattern over every function |
| Float bob cycle `01F223B0` | 60 entries, a sine of amplitude 0.067 |
| Float rise `01F22590`, settle `01F22670` | 28 entries from 0.09 to 1.0 with a peak of 1.03; 30 entries from 1.0 to 0 |
| flinch curves `01F22130`, `01F22170` | 8 entries each, 0 at both ends, at most 0.08 |
| focus ease `01F20C80` | 60 entries from 0.0097 to 1.0 |

## State

- `02B59D60`: the slot 0 override, read only.
- `02B59D64`: suppresses the physics applies.
- `02B59D68`: set during status-display denial; suppresses the status-motion applies.
- `022C6F28 + 0x48800`: the head of the active-record list both per-record phases walk.

## Modding notes

- A script's lip flap, nod or head shake takes effect at the next dirty pass; a timed form ends through the same path
  as the plain off.
- A staged look is consumed by one pass; staging two requests of one group before the pass keeps the second.
- The look and status-motion requests reach every attached piece through the record hierarchy.
- At 60 fps the focus-point slide is skipped, because `8 × 2` does not fit the countdown nibble.

## Related

- [Character status visuals](character-status-visuals.md): the status arms that switch controllers 3, 6 and 7.
- [Character render records](character-render-records.md): the record, its hierarchy and the dirty pass.
- [Authored presentation commands](authored-presentation-commands.md): commands `0x13` and `0x24`.
- [Model oscillators and pose sequencer](model-oscillators-and-pose-sequencer.md): slot 0.
- [Model files](model-files-cm-ca.md): the model block at record `+0x400` and the `@FRM` chunk.
- [Facing and steering](../Movement-And-Pathfinding/facing-and-steering.md): the steering record.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): the verbs and their handlers.
- [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md): events `0x2005` and `0x2006`.
