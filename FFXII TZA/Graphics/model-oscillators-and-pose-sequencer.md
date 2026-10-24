---
title: "Model oscillators and the pose sequencer: per-model procedural motion"
kind: "system"
category: "Graphics"
addresses: "0x003703A0, 0x003DFFE0, 0x0040ACF0, 0x0040D890, 0x0040F390, 0x0040AA20, 0x0040B3B0, 0x01EFFA30, 0x02CA4390, 0x0040ABF0, 0x00520510, 0x00520E90, 0x0054A9C0, 0x0054B1F0, 0x0052B5E0, 0x0052BBD0, 0x0040DBB0, 0x0040B780, 0x003E6F50, 0x003E7450, 0x003E6A20, 0x004772E0, 0x00477370, 0x00477480, 0x004776D0, 0x00477670, 0x00477610, 0x00477750, 0x00477B10, 0x02CA6CA0, 0x00520D30, 0x00520DF0"
---

## What the player sees

Hair, cloth and hanging gear keep swaying after the animation has set the pose, more strongly where
the map is windy, and a caster's robes can be blown along one direction while a spell is readied.
Faces blink at random intervals and open or close their eyes on cue. Neither movement is in a motion
file: the sway is simulated from a section of the model's rig, and the blinking is a short authored
sequence that picks a pose group and a texture patch.

## How it works

### Where the sway runs

`0x003703A0`, the final-pose pass of a skeleton, calls `0x003DFFE0` with the rig at skeleton `+0x94`
(`0x003705F9`) when skeleton flag `0x200` is set and the rig is not empty. The rig is the copy of the
model's `@FCP` section 2 (see [model files](model-files-cm-ca.md)); its first slot leads to the
oscillator record. `0x003DFFE0`:

1. stops when the record's byte `+0x06` is 0;
2. when the rig's word `+0x60` is non-zero, resets the record (`0x0040F390`), runs that many sub-steps
   (`0x0040D890`) and clears the word;
3. calls `0x0040ACF0(record, rig byte +0x63, rig byte +0x5E low nibble, high nibble)`.

### The two phases

Each frame `0x0040ACF0` advances two phase and speed pairs, adding `speed × [0x01DFE0BC]` and wrapping at
2π. On each wrap it draws a new speed and amplitude: a base plus a random amount up to a range
(`0x003D8E50`). For the global pair `+0x24 = [0x02CA4398] + 0x003D8E50([0x02CA439C])` and
`+0x28 = [0x02CA4380] + 0x003D8E50([0x02CA4384])`; for the per-record pair, with `r` the preset row at `+0x2C`,
`+0x34 = r[+0x0C] + 0x003D8E50(r[+0x10])` and `+0x38 = r[+0x04] + 0x003D8E50(r[+0x08])` (`0x0040ACF0`).

- The global pair (`+0x20` phase, `+0x24` speed, `+0x28` amplitude) runs only while the byte
  `0x02CA4390` is set. `0x0040B3B0(preset)` sets that byte and copies preset row `preset − 1` of
  `0x01EFFA30` into the bases and ranges `0x02CA4380`–`0x02CA439C`; the map wind sets the preset (see
  [weather](../World-Areas-And-Travel/weather.md)).

- While any requester bit of `0x02099DA6` is set, the wind is off. `0x00267D40(bit, on)`, which
  `denybonephysicalall` (`0x03D5`, `0x03EA`) calls, saves the wind when the first bit goes up
  (`0x002EAB40`) and stops it with `0x0040AAD0(0, 0, 0)`; when the last bit drops, `0x002EAA60` restores the
  saved values through `0x0040AAD0`.
- The save is `0x0040AAB0`: it copies the preset byte `0x02CA4390`, the azimuth `0x02CA4391` and the
  elevation `0x02CA4392` into a one-entry stack at `0x0215FD48` (count `0x0215FD47`).

- The per-record pair (`+0x30`, `+0x34`, `+0x38`) runs only while the record's byte `+0x3E` is set,
  and draws from the preset row the record keeps at `+0x2C`.

### The entries

After the phases it walks the record's `0x30`-byte entries (count byte `+0x04`), skipping one whose
byte `+0x02` is 0:

- the three simulation stages `0x0040FF30`, `0x00413C80` and `0x00411650` run when the rig byte `+0x63` is
  0; the single stage `0x00413340` replaces them when the record's byte `+0x07` is set and `0x02B59D68`
  is 0;
- with the entry's `+0x29` low nibble set, the weight `+0x20` passes through `0x0046FAE0` (mode from the
  rig nibble: 0 → 0, 1 → 2, 2 → 1); a weight between 0 and 1 applies through `0x0040B780`, a weight of
  1 or more through `0x0040DBB0`;
- with the low nibble clear, `+0x2A` bit 0 alone applies through `0x0040DBB0`.

The apply works on the linked bones' pose matrices: `0x0040DBB0` loads bone `+0x80` into the VU0
register bank (`0x0040DC93`) and computes the sway from it.

### Reset and settle

`0x0040F390` resets the record: it keeps only the low nibble of `+0x3F` and, for each entry, sets the
weight to 0 when `+0x2A` bit 0 is clear before resetting the entry's lists. `0x0040D890(record, n)` then
runs `n` passes of the phase step and the three stages, with the frame factor left out, and applies
`0x0040DBB0` to the entries with `+0x2A` bit 0 on every eleventh pass.

### Switching entries on and off

Entries come in groups: the low five bits of an entry's byte `+0x01` give the number of `0x30`-byte
entries in its group (1, 2, or 3 for any other value), and its top three bits must share a bit with
the record's byte `+0x1A` for the entry to be switched at all.

- `0x0040B5D0(record, mask)`, when the mask differs from `+0x1A`, disables in each group the first
  member that met the old mask and marks its bones as `0x0040ED90` does with 1; it then sets each
  member's enable byte `+0x02` to whether it meets the new mask, unmarks the bones of the enabled
  ones (`0x0040ED90` with 0) and stores the mask at `+0x1A`. The rig set-up calls it (`0x003E09B0`, `0x003E18D0`, `0x003E3D70`).
- `0x003E0B50(rig, 0, index)` switches the group at entry `index` off: for each member whose bit 0 of
  `+0x2A` is set, it clears that bit, sets the low nibble of `+0x29` to 1 and calls
  `0x0040ED90(record, entry, 1)`; `0x003E0F00` switches on the same way, setting the bit, the nibble to 2
  and calling `0x0040ED90` with 0. Either clears the nibble again when `+0x2A` bit 0 equals the high
  nibble of `+0x29`.
- `0x003E0E70` and `0x003E1210` do the same for the group whose word `+0x2A >> 4` equals an id
  (`0x0040DB00`, which returns `0xFFF` for none), and `0x003E1950(rig, on)` for every group whose state
  differs.

`0x0040ED90(record, entry, flag)` walks the entry's chains (count byte `+0x00`, `0x40` bytes a chain)
and, for every bone named after a chain's first link (`0x50` bytes a link, `0xFFFF` skipped), sets bit 1 of the bone's
`+0x28A` to the flag and clears bit 2 of its `+0x28B`.

`0x003E4140(rig, x, y, z)`, from `0x0042C410` and `0x0042C8F0` with the record's three scale factors
(`0x003E5770`, `0x003E5790`, `0x003E57B0`), gives the oscillator record their mean through `0x004158F0`,
which stores it at `+0x10` and its reciprocal at `+0x14` and scales values kept in the entries' chains by it;
it gives `z` to controller 8 (`0x005175B0`) and `y` to controller 6 (`0x004717D0`).

At start-up `0x003E0720` calls `0x00512EF0` and `0x0040DB70`, which clears `0x02CA4390` and sets the global direction
through `0x0040B430`. `0x00415A80(record, delta)` adds a delta to every encoded pointer of the record,
for the rig's rebase `0x003E1C50`.

### Directed sway from an authored command

The handler registered for authored command `0x3F`, `0x00520510` (installed at `0x00426B6B`), acts only
on a root record (word `+6` is −1). For the record and its sub-tree (`0x00426870`), `0x00520E90` reaches
the rig's oscillator record and calls `0x0040ABF0(record, preset, direction, bone, flag)`:

- the preset is the low twelve bits of command word `+0x10`, forced to 0 when the bone word `+0x02`
  is −1; the flag is bit 15 of the same word, and the direction is the three floats `+0x04`–`+0x0C`;
- `+0x3E` takes the preset, so preset 0 stops the per-record pair;
- otherwise `+0x40` takes the direction, `+0x50` a second vector built from it, `+0x2C` preset row
  `preset − 1`, `+0x3C` the bone, and `+0x3F` bit 1 is raised so the pair re-draws at once.

`0x0041DD40` calls `0x00520100(record)`, which runs the same walk for a root record with the preset and
the flag set to 0, so every record of the sub-tree stops its per-record pair.

### Effect elements with a sway section

An effect element whose set-up is `0x0052BBD0` copies a sway section from its effect data into its own
buffer and prepares it with `0x0054A9C0`, which passes it to `0x0040EEA0` and gives the record a random
global phase.

`0x0054B1F0` installs the element's parameter block into that section, resets its scale with
`0x004158F0(h, 1.0)` (`0x0054B23B`), runs the global phase step `0x0040AA20` (`0x0054B339`), a second time when its third
argument is non-zero and `0x001EDDA0()` returns 0 (`0x0054B33E`-`0x0054B34E`), and, depending on its flags, one pass of
the three stages (`0x0040FEF0`). `0x0052BBD0` calls it 32 times in a row with that argument 1 (`0x0052BF43`);
`0x0052B5E0` calls it once (`0x0052BB30`).

### The pose sequencer

Section 7 of a model's `@FCP` block holds eight events. A render record whose model has section 7
gets a sequencer entry at bind time: `0x0041FCF0` calls `0x004772E0(record, record byte +0x5C)`, which
takes a free entry of the 32 at `0x02CA6CA0`, stores the number minus one as the entry's variant and
returns the handle `serial << 8 | entry`, kept at record `+0x450`.

The record-system initialiser `0x004269A0` empties the 32 entries and the counts `0x02CA6C90` and
`0x02CA6C94` through `0x004778A0`. The record teardown `0x0041E860` frees the record's entry through
`0x00477640(handle)`, which checks the handle's serial against the entry, clears it and decrements
`0x02CA6C90`.

- `0x00477370(handle, event, choice, section, onlyIfChanged)` starts an event. It does nothing for a
  record with `rel` `0xFFFF` or the enabled byte 0. Choice `0xFF` picks one at random (`0x003A6E60`
  with the record's pick byte) and marks the slot to re-pick at each end; a choice at or above the
  count is refused.
- With `onlyIfChanged` and the same event on the slot, a random request is dropped while the slot is
  re-picking, and a forced one when it is the choice playing.
- `0x00477480(handle, section)` steps the eight slots when `0x001EDE80` returns non-zero, the entry's word
  `+0x00` is set and its word `+0x02` and `0x02CA6C98` are 0. A slot counts ticks and moves to the next
  frame when the frame's duration is reached.
- Past the last frame it re-picks when marked, otherwise follows the last frame's end action: 0 stops
  the slot, 1 holds the last frame, 2 loops to frame 0.
- `0x004776D0(handle, section, slot)` returns the current frame's value, or −1 for an idle slot; kind 1
  add-motion tracks apply the group with that id (see [add-motion tables](add-motion-tables.md)).
- `0x00477670(handle, event, section)` clears the slot the event drives.

The record-side doors `0x003E7450` (start) and `0x003E6A20` (reset) pass the record's handle and section.
`0x003E7450` has three callers:

| Caller | Event | When |
|---|---|---|
| authored command `0x1D`, `0x00520D30` | low nibble of byte `+2`, choice byte `+3` | byte `+2`'s high nibble is 0 or equals the record's byte `+0x413` plus one |
| `0x0041DD40` (`0x0041DF95`) | 2, random, only if changed | a presentation entry's pending state is activated |
| `0x0051E3A0` (`0x0051E494`) | 0, choice 0, only if changed | every update with a third argument of 0 while the block's byte `+0x33` is set |

Command `0x1E`, `0x00520DF0`, resets the event in byte `+2`'s low nibble with the same filter. Command
`0x1D` with byte `+2` = `0xFF` stores byte `+3` in the model row's `@FOR` key `+0xB8` and calls
`0x00477610(handle, n)`; that routine looks the entry up with `n` in place of the handle, so it never
finds it and the sequencer's variant never changes.

### The texture patch

The model draw `0x0053AB50` calls `0x00477750` and `0x00477B10` with the record's sequencer. For each active
slot whose two texture slots (the first two bytes of the event's choice table) are loaded
(`0x005047C0`), `0x00477750` reserves 128 bytes, and `0x00477B10` copies a rectangle of the first texture,
at the position listed for the slot's value, onto the second texture's fixed rectangle.

The copy is a GS transfer inside GS memory, built by `0x00505150(packet, transfer)` and called from
`0x00477B10` and `0x004778D0`: a GIF tag, `TEXFLUSH` (`0x3F`), `BITBLTBUF` (`0x50`), `TRXPOS` (`0x51`),
`TRXREG` (`0x52`), `TRXDIR` (`0x53`) set to 2, and `TEXFLUSH` again, `0x80` bytes in all.

## Layouts

### The oscillator record

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | encoded pointer to the 0x30-byte entries |  |
| `+0x04` | `u8` | entry count |  |
| `+0x05` | `u8` | non-zero: +0x0C must resolve to a live object first |  |
| `+0x06` | `u8` | 0 disables the record |  |
| `+0x07` | `u8` | selects the single stage while 0x02B59D68 is 0 |  |
| `+0x10` | `f32` | copied to the VU0 bank at 0x022D9390 |  |
| `+0x20` | `f32` | global phase | +`0x24`  f32  speed      +`0x28`  f32  amplitude |
| `+0x2C` | `u32` | encoded pointer to the record's preset row |  |
| `+0x30` | `f32` | per-record phase | +`0x34`  f32  speed      +`0x38`  f32  amplitude |
| `+0x3C` | `u16` | bone (command 0x3F) |  |
| `+0x3E` | `u8` | per-record preset, 0 = off |  |
| `+0x3F` | `u8` | bit 0 / bit 1 re-draw the global / per-record pair; bit 3 the command's flag |  |
| `+0x40` | `f32[4]` | direction (command 0x3F) |  |

```
entry +0x02  u8   0 skips the entry
entry +0x20  f32  weight
entry +0x29  u8   low nibble: weighted apply
entry +0x2A  u8   bit 0: apply at full weight
```

### Section 7 of @FCP

Section 7 starts at payload `+ [+0x0E]` (`0x003E6F50`); offsets below are from the section unless noted.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16[8]` | offset of each event's records |  |

Event record (6 bytes, at the event's offset + 6 x variant):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | slot |  |
| `+0x01` | `u8` | pick byte for a random choice |  |
| `+0x02` | `u16` | rel: 0xFFFF = no choices; the choice table starts at record + 2 + rel |  |
| `+0x04` | `u8` | 0 = disabled |  |

Choice table (offsets from its start):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | source texture slot | +`0x01`  u8   destination texture slot |
| `+0x0C` | `u16` | offset of the rectangle table, from +0x0C |  |
| `+0x0E` | `u16` | choice count |  |
| `+0x10` | `u16[count]` | choice c's sequence is at +0x10 + 2c + this value |  |

```
sequence:  u16 frame count, then per frame {u16 duration in ticks, u8 end action, u8 value}
rectangle table:  +0 / +2 destination x, y; +4 / +6 width, height; +0x0E + 4v / +0x10 + 4v source x, y for value v
```

### A sequencer entry (0x40 bytes at 0x02CA6CA0)

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | in use | +`0x02`  u16   non-zero stops stepping (`0x004775E0`) |
| `+0x04` | `u32` | handle | +`0x08`  u32   render record |
| `+0x0C` | `u32` | variant |  |
| `+0x10` | `u8[8] active` | +0x18 | u8[8] re-pick    +`0x20`  u8[8] event (`0xFF` none) |
| `+0x28` | `u8[8] choice` | +0x30 | u8[8] frame      +`0x38`  u8[8] ticks in the frame |

The record's functions are listed in
[model-oscillators-and-pose-sequencer-model-oscillator-subsystem.tsv](model-oscillators-and-pose-sequencer-model-oscillator-subsystem.tsv).

## Shipped data

| Fact | Value |
|---|---|
| sway presets | six rows at `0x01EFFA30`; the values are listed on [weather](../World-Areas-And-Travel/weather.md) |
| section 7 | in all 1,066 `.cm` blocks |
| blocks with an enabled event | 67: 54 NPCs and 13 `chara` models; events 0, 1 and 2 in each, all on slot 0 |
| choices per enabled event | 2 in 67, 3 in 122, 4 in 12 |
| sequences | 548, of 1, 3, 4, 5 or 6 frames; none past its entry |
| durations | 1, 3, 10, 60 and 250 ticks; values 0 to 3 |
| last frame's end action | stop 67, hold 414, loop 67 |
| the NPC events (54 blocks) | event 0: snap to 0, 2→1→0 over three ticks each, or 0→2→0; event 1: snap to 2, or 0→1→2; event 2: wait 10, 60 or 250 ticks, then 0→2→0 one tick a step |

## Operations

Per frame and model: two phase steps and, per enabled entry, the stages and one apply. A settle of `n`
sub-steps costs `n` passes of the stages. The sequencer steps eight slots per entry; the value read is
one lookup.

## State

The wind byte `0x02CA4390` and the parameters `0x02CA4380`–`0x02CA439C`; each model's oscillator record in
its rig; the 32 sequencer entries at `0x02CA6CA0` with the serial `0x02CA6C94`, and the record's handle
`+0x450`.

## Modding notes

- The sway of a model is the sway section of its `@FCP` section 2 rig; a model with no sway section
  does not sway.
- Calm maps (wind preset 0) leave the global phase still; command `0x3F` sways a model on any map.
- Authored command `0x3F` with preset 0, or with a bone word of −1, turns the directed sway off.
- A section 7 event with `rel` `0xFFFF` or the enabled byte 0 does nothing; give every enabled event
  at least one choice.
- End actions other than 0, 1 and 2 leave the slot on its last frame, counting ticks.
- The sequencer variant is fixed when the model is bound; command `0x1D` with byte `0xFF` changes only
  the model row's `@FOR` key.
- Sequencer values are the ids of add-motion groups and rectangle columns; keep them below the
  rectangle table's length.

## Related

- [Model files](model-files-cm-ca.md): `@FCP`, section 2 and section 7.
- [Add-motion tables](add-motion-tables.md): the pose groups the slot values select.
- [Weather](../World-Areas-And-Travel/weather.md): the map wind preset and the preset table.
- [Authored presentation commands](authored-presentation-commands.md): commands `0x1D`, `0x1E` and `0x3F`.
- [Subsystem update flags](../Engine-Core/subsystem-update-flags.md): the 60 fps predicate `0x001EDE80`.
