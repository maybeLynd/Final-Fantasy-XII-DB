[Home](../../README.md) / [Graphics](README.md) / Model oscillators and the pose sequencer

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Model oscillators and the pose sequencer: per-model procedural motion | system | Graphics | Character models / Animation And Motion | The two kinds of motion a model makes beyond its authored motions: the oscillator record (the sway section of a model's rig) that 0x0040ACF0 steps every frame with a wind-driven phase and a directed per-record phase, its reset and sub-stepped settle, the authored command and the effect element that drive it; and the pose sequencer, eight slots per character that play authored (duration, value) sequences from @FCP section 7 and feed the add-motion pose groups and a texture patch copy, with counts over the shipped files. | 0x003703A0, 0x003DFFE0, 0x0040ACF0, 0x0040D890, 0x0040F390, 0x0040AA20, 0x0040B3B0, 0x01EFFA30, 0x02CA4390, 0x0040ABF0, 0x00520510, 0x00520E90, 0x0054A9C0, 0x0054B1F0, 0x0052B5E0, 0x0052BBD0, 0x0040DBB0, 0x0040B780, 0x003E6F50, 0x003E7450, 0x003E6A20, 0x004772E0, 0x00477370, 0x00477480, 0x004776D0, 0x00477670, 0x00477610, 0x00477750, 0x00477B10, 0x02CA6CA0, 0x00520D30, 0x00520DF0 |

## What the player sees

Hair, cloth and hanging gear keep swaying after the animation has set the pose, more strongly where
the map is windy, and a caster's robes can be blown along one direction while a spell is readied.
Faces blink at random intervals and open or close their eyes on cue. Neither movement is in a motion
file: the sway is simulated from a section of the model's rig, and the blinking is a short authored
sequence that picks a pose group and a texture patch.

## How it works

### Where the sway runs

`0x003703A0`, the final-pose pass of a skeleton, calls `0x003DFFE0` with the rig at skeleton `+0x94`¹ when skeleton flag `0x200` is set and the rig is not empty. The rig is the copy of the
model's `@FCP` section 2 (see [model files](model-files-cm-ca.md)); its first slot leads to the
oscillator record. `0x003DFFE0`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003705F9` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | first re-stores `vf00` and zeroes the VU0 rows `0x022D91B0` to `0x022D942F` through `0x0036D9E0`, then returns when the rig or its oscillator record is null; | `0x003DFFE9`<br>`0x003DFFF1`, `0x003E0002` |
| 2 | stops when the record's byte `+0x06` is 0, after clearing the high nibble of `+0x3F` through its tail jump to `0x0040ED80`; otherwise `0x0040EE70` adds `0x10` to `+0x3F` and keeps its low nibble; | `0x003E0017`, `0x003E00B4`<br>`0x003E002C` |
| 3 | when the rig's word `+0x60` is non-zero, resets the record, runs that many sub-steps and clears the word; | `0x0040F390`<br>`0x0040D890` |
| 4 | calls `0x0040ACF0(record, rig byte +0x63, rig byte +0x5E low nibble, high nibble)` as a tail jump; the second argument is the rig byte `+0x63` ORed with the word `0x02B59D60`, which lies in the zero-filled data and which the image only reads. | `0x003E00A9`<br>`0x003E0079` |

### The two phases

Each frame `0x0040ACF0` advances two phase and speed pairs, adding `speed × [0x01DFE0BC]` and wrapping at
2π. On each wrap it draws a new speed and amplitude: a base plus a random amount up to a range¹. For the global pair `+0x24 = [0x02CA4398] + 0x003D8E50([0x02CA439C])` and
`+0x28 = [0x02CA4380] + 0x003D8E50([0x02CA4384])`; for the per-record pair, with `r` the preset row at `+0x2C`,
`+0x34 = r[+0x0C] + 0x003D8E50(r[+0x10])` and `+0x38 = r[+0x04] + 0x003D8E50(r[+0x08])`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003D8E50` |
| ² | `0x0040ACF0` |

</details>

- The global pair (`+0x20` phase, `+0x24` speed, `+0x28` amplitude) runs only while the byte
  `0x02CA4390` is set. `0x0040B3B0(preset)` sets that byte and copies preset row `preset − 1` of
  `0x01EFFA30` into the bases and ranges `0x02CA4380`–`0x02CA439C`; the map wind sets the preset (see
  [weather](../World-Areas-And-Travel/weather.md)).

- `0x0040B3B0` stores the preset byte even when it is 0, and preset 0 copies nothing, leaving the old bases
  and ranges in place¹. A row's words `+0x00` to `+0x18` go to `0x02CA4388`,
  `0x02CA4380`, `0x02CA4384`, `0x02CA4398`, `0x02CA439C`, `0x02CA438C` and `0x02CA4394`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0040B3B0`, `0x0040B3B8` |
| ² | `0x0040B3C8`-`0x0040B41F` |

</details>

- While any requester bit of `0x02099DA6` is set, the wind is off. `0x00267D40(bit, on)`, which
  `denybonephysicalall` (`0x03D5`, `0x03EA`) calls, saves the wind when the first bit goes up
 ¹ and stops it with `0x0040AAD0(0, 0, 0)`; when the last bit drops, `0x002EAA60` restores the
  saved values through `0x0040AAD0`.
- The save is `0x0040AAB0`: it copies the preset byte `0x02CA4390`, the azimuth `0x02CA4391` and the
  elevation `0x02CA4392` into a one-entry stack at `0x0215FD48` (count `0x0215FD47`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EAB40` |

</details>

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
- with the low nibble clear, `+0x2A` bit `0x1` alone applies through `0x0040DBB0`.

The apply works on the linked bones' pose matrices: `0x0040DBB0` loads bone `+0x80` into the VU0
register bank¹ and computes the sway from it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0040DC93` |

</details>

### Reset and settle

`0x0040F390` resets the record: it keeps only the low nibble of `+0x3F` and, for each entry, sets the
weight to 0 when `+0x2A` bit `0x1` is clear before resetting the entry's lists. `0x0040D890(record, n)` then
runs `n` passes of the phase step and the three stages, with the frame factor left out, and applies
`0x0040DBB0` to the entries with `+0x2A` bit `0x1` on every eleventh pass.

`0x0040D890` returns at once when the record's byte `+0x05` is set and the object its `+0x0C` leads to is
null¹. Otherwise it loads the VU0 bank: `+0x10` into `0x022D9390`,
`Q = [0x01EF93FC] / +0x10` into `0x022D9198`, `Q + [0x01EF93F4]` into the lane `0x022D9394`, and the sign-extended
`+0x1C` into `0x022D8FB0` and `0x022D9350`; it calls `0x0036DDA0` when that lane is 0 and `0x0036DD90` when it is
negative². With `n` = 0 it stops there³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0040D89A`-`0x0040D8B7` |
| ² | `0x0040D8BD`-`0x0040D92F` |
| ³ | `0x0040D938` |

</details>

Each pass steps the per-record pair while `+0x3E` is set, then the global pair while `0x02CA4390` is set:
`+0x30 += +0x34` and `+0x20 += +0x24`, each wrapping at 6.28318¹ and re-drawing its speed and
amplitude as `0x0040ACF0` does².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x009002E0` |
| ² | `0x0040D958`-`0x0040DA40` |

</details>

On every entry each pass then sets the high nibble of
`+0x29` to `+0x2A` bit `0x1`¹, and on each entry whose byte `+0x02` is set it runs
`0x0040FF30`, `0x00413C80` and `0x00411650`². The pass counter runs from 1 to 11 and
starts again at 1³, so the apply comes on passes 11, 22, 33 and on⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0040DA60`-`0x0040DA6E` |
| ² | `0x0040DA71`-`0x0040DA93` |
| ³ | `0x0040DABC`-`0x0040DAC1` |
| ⁴ | `0x0040DA9E` |

</details>

### Switching entries on and off

Entries come in groups: the low five bits of an entry's byte `+0x01` give the number of `0x30`-byte
entries in its group (1, 2, or 3 for any other value), and its top three bits must share a bit with
the record's byte `+0x1A` for the entry to be switched at all.

- `0x0040B5D0(record, mask)`, when the mask differs from `+0x1A`, disables in each group the first
  member that met the old mask and marks its bones as `0x0040ED90` does with 1; it then sets each
  member's enable byte `+0x02` to whether it meets the new mask, unmarks the bones of the enabled
  ones (`0x0040ED90` with 0) and stores the mask at `+0x1A`. The rig set-up calls it¹.
- `0x003E0B50(rig, 0, index)` switches the group at entry `index` off: for each member whose bit `0x1` of
  `+0x2A` is set, it clears that bit, sets the low nibble of `+0x29` to 1 and calls
  `0x0040ED90(record, entry, 1)`; `0x003E0F00` switches on the same way, setting the bit, the nibble to 2
  and calling `0x0040ED90` with 0. Either clears the nibble again when `+0x2A` bit `0x1` equals the high
  nibble of `+0x29`.
- `0x003E0E70` and `0x003E1210` do the same for the group whose word `+0x2A >> 4` equals an id
  (`0x0040DB00`, which returns `0xFFF` when no group matches), and `0x003E1950(rig, on)` for every group whose state
  differs.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003E09B0`, `0x003E18D0`, `0x003E3D70` |

</details>

`0x0040ED90(record, entry, flag)` walks the entry's chains (count byte `+0x00`, `0x40` bytes a chain)
and, over the chain's links except the last, up to the first whose bone is `0xFFFF` (`0x50` bytes a link,
`0x0040EDDE`-`0x0040EE3B`), sets bit `0x2` of the bone's
`+0x28A` to the flag and clears bit `0x4` of its `+0x28B`.

`0x0040B180(record, -, step)`, slot 0's update in the rig frame, returns at once on the same test as `0x0040D890`, made
through `0x0020E600`¹; it ignores its second argument. It walks the entries, skipping one whose
byte `+0x02` is 0 (the handle `+0x00`, `0x0040B1B2`-`0x0040B229`, `0x0040B349`-`0x0040B358`), and ends the fades `0x003E0B50`
and `0x003E0F00` start. With the low nibble of `+0x29` at 1 the weight `+0x20` falls, with any other non-zero value it
rises, by `step * [0x01DFE0BC]`, or by `step` alone when the weight is exactly 0 or exactly 1.0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0040B189`-`0x0040B1AC` |
| ² | `0x0040B22F`-`0x0040B259` |

</details>

A weight that falls to 0 or below becomes 0 and one that rises to 1.0 or above becomes 1.0, and the nibble is cleared¹. Bones are marked only in the call where a rising weight reaches 1.0, and for an entry with
the nibble clear and `+0x2A` bit `0x1` set².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0040B25B`-`0x0040B29A` |
| ² | `0x0040B29D`-`0x0040B2A3` |

</details>

Over the entry's chains (at the handle `+0x08`; each with its link count `+0x03` and its links at the handle `+0x04`),
each chain whose first link's bone has bit `0x4` of `+0x28B` clear gets that bit set on the bone of every link but the
last, a link whose bone is `0xFFFF` passed over; the bones are the `0x290`-byte records of the array the record's
`+0x08` leads to, each handle resolved through `0x0020E600`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0040B2A9`-`0x0040B343` |

</details>

`0x003E4140(rig, x, y, z)`, from `0x0042C410` with the record's three scale factors¹
and from `0x0042C8F0` with the same three products as set out below, gives the oscillator record their mean through
`0x004158F0`, which stores it at `+0x10` and its
reciprocal at `+0x14` and scales values kept in the entries' chains by it, except that the innermost `0x50`-byte
elements take `1 + (mean - 1) × 0.3` of their `+0x0C`; it gives `z` to controller 8² and `y` to controller
6³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003E5770`, `0x003E5790`, `0x003E57B0` |
| ² | `0x005175B0` |
| ³ | `0x004717D0` |

</details>

`0x0042C8F0` takes the three products from the record's parent when the record has one and byte `+5` of the block the
rig's first handle names¹ is set, and otherwise from the record, each times the record's `+0x170`,
`+0x174` or `+0x178` when it has a parent and its byte `+0x3C` is `0x77`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0020E600` |
| ² | `0x0042CADD`-`0x0042CB53` |

</details>

At start-up `0x003E0720` calls `0x00512EF0` and `0x0040DB70`, which clears `0x02CA4390` and sets the global direction
through `0x0040B430`. `0x00415A80(record, delta)` adds a delta to every encoded pointer of the record,
for the rig's rebase `0x003E1C50`.

### Directed sway from an authored command

The handler registered for authored command `0x3F`, `0x00520510` (installed at `0x00426B6B`), acts only
on a root record (word `+6` is −1). For the record and its sub-tree¹, `0x00520E90` reaches
the rig's oscillator record and calls `0x0040ABF0(record, preset, direction, bone, flag)`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00426870` |

</details>

- the preset is the low twelve bits of command word `+0x10`, forced to 0 when the bone word `+0x02`
  is −1; the flag is bit `0x8000` of the same word, and the direction is the three floats `+0x04`–`+0x0C`;
- `+0x3E` takes the preset, so preset 0 stops the per-record pair;
- otherwise `+0x40` takes the direction, `+0x50` a second vector built from it, `+0x2C` preset row
  `preset − 1`, `+0x3C` the bone, and `+0x3F` bit `0x2` is raised so the pair re-draws at once.
- whatever the preset, `+0x3F` bit `0x8` takes bit `0x1` of the flag¹;
- for a non-zero preset the direction is copied as 16 bytes², and the second vector
  is the unit cross product `(0, 1.0, 0.00001) × direction`³,
  normalised by `0x00380800`, which gives a zero vector for a length below 0.000001⁴;
  `+0x2C` holds the row encoded through `0x0020E620`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0040AC0E`-`0x0040AC28` |
| ² | `0x0040AC36`-`0x0040AC41` |
| ³ | `0x00D108A0`, `0x00202E10`, `0x0040AC46`-`0x0040AC99` |
| ⁴ | `0x00908E10`, `0x0040AC9E` |
| ⁵ | `0x0040ACB4` |

</details>

`0x00520510` returns 0 for a record that is not a root and 1 after the walk¹.
`0x00520E90` finds the model through `0x002ED570` with the record's id `+0x18`, and skips a record whose id is
−1 or whose model, rig `+0x94` or oscillator record is null². It passes the
direction as `x, y, z` and 1.0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00520521`, `0x00520599` |
| ² | `0x00520EAC`-`0x00520F6A` |
| ³ | `0x00520F23`-`0x00520F55` |

</details>

Before the call `0x00520E90` copies bit `0x1` of the walk's byte `+0x1A` into `+0x3F` bit `0x4`¹, and after every record, skipped or not, it sets that byte to 1².
`0x00520510` starts it at 0³ and `0x00426870` visits the root first⁴, so the root's
oscillator record gets bit `0x4` clear and every record below it gets bit `0x4` set.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00520F86`-`0x00520F94` |
| ² | `0x00520FD6` |
| ³ | `0x00520551` |
| ⁴ | `0x004268A3` |

</details>

`0x0041DD40` calls `0x00520100(record)`, which runs the same walk for a root record with the preset and
the flag set to 0, so every record of the sub-tree stops its per-record pair.

### Effect elements with a sway section

An effect element whose set-up is `0x0052BBD0` copies a sway section from its effect data into its own
buffer and prepares it with `0x0054A9C0`, which passes it to `0x0040EEA0` and gives the record a random
global phase.

`0x0054A9C0` takes the record from element `+0x148`, gives it to `0x0040EEA0`¹ and draws the
phase `+0x20` up to 6.2831², raising `+0x3F` bit `0x1` so the global pair re-draws³. It zeroes the speed and amplitude `+0x24` and `+0x28`, the preset `+0x3E` and
the byte `+0x07`; it stores `0xFF` at `+0x05`, 1 at `+0x06`, 1.0 at `+0x10`, `+0x14` and `+0x1C` and 1
at `+0x1B`, and encoded null pointers at `+0x08` and `+0x0C`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0054A9DA` |
| ² | `0x00D11788`, `0x003D8E50` |
| ³ | `0x0054A9DF`-`0x0054A9FE` |
| ⁴ | `0x0054A9F0`-`0x0054AA2F` |

</details>

The first entry gets `+0x2A` bit `0x1` and `0xF` in the low nibble of `+0x29`¹.
The element gets `+0x13C = 1 / (+0x12C - 1)`, with `+0x12C` read as a 32-bit count, and
`+0x140 = 1 / +0x13C`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0054AA3B`, `0x0054AA5A` |
| ² | `0x0054AA5E`-`0x0054AA7B` |

</details>

`0x0054B1F0` installs the element's parameter block into that section, resets its scale with
`0x004158F0(h, 1.0)`¹, runs the global phase step `0x0040AA20`², a second time when its third
argument is non-zero and `0x001EDDA0()` returns 0³, and, depending on its flags, one pass of
the three stages⁴. `0x0052BBD0` calls it 32 times in a row with that argument 1⁵;
`0x0052B5E0` calls it once⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0054B23B` |
| ² | `0x0054B339` |
| ³ | `0x0054B33E`-`0x0054B34E` |
| ⁴ | `0x0040FEF0` |
| ⁵ | `0x0052BF43` |
| ⁶ | `0x0052BB30` |

</details>

The install writes the block `p` into the first entry's first chain `c` (the entry's `+0x08`) and its
links. `c + 0x30` and `c + 0x38` take `[p + 0x10]`¹. Unless the first link already
holds them, every link of the chain's count byte `+0x03` takes `[p + 0x00]` at `+0x3C`, `[p + 0x04]` at
`+0x40` and `+0x4C`, and `[p + 0x08]` at `+0x2C`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0054B243`, `0x0054B249` |
| ² | `0x0054B256`-`0x0054B2B3` |

</details>

The list at the entry's `+0x0C` takes `[p + 0x0C]` at `+0x18` in its first `count - 1` records of `0x20`
bytes, `count` being that chain byte, unless its first record already holds it¹.
The first link's `+0x20`, `+0x24` and `+0x28` take the three floats `[p + 0x18]` points to². The stage pass `0x0040FEF0(h, entries)` runs unless `0x001EDDA0()` returns 0, the
third argument is 0 and bit `0x1` of the fourth is set³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0054B2C5`-`0x0054B2F3` |
| ² | `0x0054B2F5`-`0x0054B334` |
| ³ | `0x0054B353`-`0x0054B374` |

</details>

### The pose sequencer

Section 7 of a model's `@FCP` block holds eight events. A render record whose model has section 7
gets a sequencer entry at bind time: `0x0041FCF0` calls `0x004772E0(index, record byte +0x5C)` with the record's
index, its signed word `+0x00`¹, which
takes a free entry of the 32 at `0x02CA6CA0`, stores the number minus one as the entry's variant and
returns the handle `serial << 8 | entry`, kept at record `+0x450`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0041FEB3` |

</details>

An entry is free while its word `+0x00` is 0; with no free entry `0x004772E0` returns 0¹.
It adds 1 to the count `0x02CA6C90`, and the serial `0x02CA6C94` goes up by 1 and back to 1 past `0xFFFFFF`². The entry gets 1 at `+0x00`, the handle at `+0x04`, the index at `+0x08`, the variant at
`+0x0C`, zeros at `+0x10`-`+0x1F` and -1 at `+0x20`-`+0x2F`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004772F6`-`0x00477309` |
| ² | `0x0047730A`-`0x00477338` |
| ³ | `0x00477331`-`0x0047735F` |

</details>

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
- A start sets the slot's active byte to 1, its event, frame 0 and tick 0; a forced choice is stored with
  the re-pick mark cleared, and a random pick goes in as `0x003A6E60` returns it¹. A
  handle whose serial differs from the entry's makes `0x00477370` do nothing².
- `0x00477480(handle, section)` steps the eight slots when `0x001EDE80` returns non-zero, the entry's word
  `+0x00` is set and its word `+0x02` and `0x02CA6C98` are 0. A slot counts ticks and moves to the next
  frame when the frame's duration is reached.
- Past the last frame it re-picks when marked, otherwise follows the last frame's end action: 0 stops
  the slot, 1 holds the last frame, 2 loops to frame 0.
- A stop clears the active and re-pick bytes and sets the event and choice to `0xFF`
 ³; a re-pick goes back to frame 0 with a new `0x003A6E60` choice
 ⁴. The tick count goes up before the duration test, and the frame byte moves on and
  the ticks restart at 0 before the end action is read⁵.
- `0x00477480` also skips an entry whose serial differs from the handle, and a null section
 ⁶.
- `0x004776D0(handle, section, slot)` returns the current frame's value, or −1 for an idle slot; kind 1
  add-motion tracks apply the group with that id (see [add-motion tables](add-motion-tables.md)).
- `0x004776D0` also returns -1 when the entry the handle's low byte names, `0x02CA6CA0 + 64 x` that byte, holds another
  handle at `+0x04` or is free (word `+0x00` 0); an idle slot is one whose active byte, `+0x10` plus the slot, is 0
 ⁷.
- Otherwise it follows the section's offset words for the slot's event (`+0x20` plus the slot), the entry's variant
  `+0x0C` and the slot's choice (`+0x28` plus the slot) to the choice's record, and returns its byte
  `+5 + 4 x frame`, the frame being the slot's byte `+0x30` plus the slot⁸.
- The sums in `0x004776D0` are formed in 32-bit registers, so only the low 32 bits of the section address are kept
 ⁹.
- `0x00477670(handle, event, section)` clears the slot the event drives: active and re-pick to 0, event and
  choice to `0xFF`, with the frame and ticks kept¹⁰. It takes the slot byte from the
  event's record for the entry's variant without reading `rel` or the enabled byte¹¹,
  and does nothing for a handle whose serial differs¹².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00477428`-`0x0047746A` |
| ² | `0x0047738C`-`0x00477397` |
| ³ | `0x004775A5`-`0x004775B4` |
| ⁴ | `0x00477564`-`0x00477573` |
| ⁵ | `0x0047752A`-`0x0047755B` |
| ⁶ | `0x004774BA`-`0x004774CD` |
| ⁷ | `0x004776D0`-`0x00477701` |
| ⁸ | `0x00477703`-`0x0047773B` |
| ⁹ | `0x00477710`, `0x00477727`, `0x00477731`-`0x00477733` |
| ¹⁰ | `0x004776A3`-`0x004776C5` |
| ¹¹ | `0x00477693`-`0x004776A3` |
| ¹² | `0x00477684`-`0x0047768F` |

</details>

The record-side doors `0x003E7450` (start) and `0x003E6A20` (reset) pass the record's handle and section.
The section is `[record + 0x400] + u16 [+0x0E]`, added in 32 bits and sign-extended, or 0 when `+0x400` is
null or that word is 0¹; a handle of −1 makes both return². `0x003E7450(record, event, choice, onlyIfChanged)` passes its arguments on, and
`0x003E6A20(record, event)` reaches `0x00477670` by a tail jump³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003E6A2D`-`0x003E6A55`, `0x003E7464`-`0x003E7493` |
| ² | `0x003E6A2B`, `0x003E7462` |
| ³ | `0x003E6A4D`, `0x003E6A58` |

</details>

`0x003E7450` has three callers:

| Caller | Event | When |
|---|---|---|
| authored command `0x1D`, `0x00520D30` | low nibble of byte `+2`, choice byte `+3`, not only if changed (`0x00520DD6`) | byte `+2`'s high nibble is 0 or equals the record's byte `+0x413` plus one, `+0x413 + 1` (`0x00520DB5`-`0x00520DCF`), for a byte `+2` other than `0xFD`, `0xFE` and `0xFF` |
| `0x0041DD40` (`0x0041DF95`) | 2, random, only if changed | a presentation entry's pending state is activated |
| `0x0051E3A0` (`0x0051E494`) | 0, choice 0, only if changed | every update with a third argument of 0 while the block's byte `+0x33` is set |

Command `0x1E`, `0x00520DF0`, resets the event in byte `+2`'s low nibble with the same filter. Command
`0x1D` with byte `+2` = `0xFF` stores byte `+3` in the model row's `@FOR` key `+0xB8` and calls
`0x00477610(handle, n)`; that routine looks the entry up with `n` in place of the handle, so it never
finds it and the sequencer's variant never changes. The `0xFF` branch does nothing when `0x003E55B0` finds
no model row, and skips the call for a handle of −1¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00520D6B`, `0x00520D80` |

</details>

Command `0x1D` with byte `+2` = `0xFD` sets bit `0x40` of the record's `+0x4B7`¹, and with
`0xFE` calls `0x00428B30(record word +0x00, 1)`²; neither reaches the sequencer.
Command `0x1E` has no such cases: every byte `+2` goes through the filter³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00520D48` |
| ² | `0x00520D9B`-`0x00520DA3` |
| ³ | `0x00520DF4`-`0x00520E16` |

</details>

### The texture patch

The model draw `0x0053AB50` calls `0x00477750` and `0x00477B10` with the record's sequencer. For each active
slot whose two texture slots (the first two bytes of the event's choice table) are loaded¹, `0x00477750` counts 128, and `0x00477B10` copies a rectangle of the first texture,
at the position listed for the slot's value, onto the second texture's fixed rectangle.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005047C0` |

</details>

`0x00477750` reserves nothing itself: it returns `v = 128 × n` for the `n` such slots¹, and 0 for
a handle whose serial differs or a free entry². A slot counts only when
the entry's render record `+0x08` is not −1, that record (`[0x022C6F28] + 0x740 × index`) has a non-zero
`+0x284` and `0x003E55B0` returns a model row for it³. The draw makes room for
`(v + 1) × 16` bytes in its packet buffer and starts a new buffer through `0x00504450` and `0x005044B0` when
they do not fit⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0047788C` |
| ² | `0x0047776F`-`0x0047777B`, `0x00477786` |
| ³ | `0x004777DD`-`0x00477813` |
| ⁴ | `0x0053C0F9`-`0x0053C12C` |

</details>

The copy is a GS transfer inside GS memory, built by `0x00505150(packet, transfer)` and called from
`0x00477B10` and `0x004778D0`: a GIF tag, `TEXFLUSH` (`0x3F`), `BITBLTBUF` (`0x50`), `TRXPOS` (`0x51`),
`TRXREG` (`0x52`), `TRXDIR` (`0x53`) set to 2, and `TEXFLUSH` again, `0x80` bytes in all.

## Layouts

<details>
<summary>Show the memory layouts</summary>

### The oscillator record

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` |  | encoded pointer to the `0x30`-byte entries |
| `+0x04` | `u8` |  | entry count |
| `+0x05` | `u8` |  | non-zero: `+0x0C` must resolve to a live object first |
| `+0x06` | `u8` |  | 0 disables the record |
| `+0x07` | `u8` |  | selects the single stage while `0x02B59D68` is 0 |
| `+0x10` | `f32` |  | copied to the VU0 bank at `0x022D9390` |
| `+0x20` | `f32` |  | global phase |
| `+0x24` | `f32` | speed |  |
| `+0x28` | `f32` | amplitude |  |
| `+0x2C` | `u32` |  | encoded pointer to the record's preset row |
| `+0x30` | `f32` |  | per-record phase |
| `+0x34` | `f32` | speed |  |
| `+0x38` | `f32` | amplitude |  |
| `+0x3C` | `u16` |  | bone (command `0x3F`) |
| `+0x3E` | `u8` |  | per-record preset, 0 = off |
| `+0x3F` | `u8` |  | bit `0x1` / bit `0x2` re-draw the global / per-record pair; bit `0x8` the command's flag; bit `0x4` clear on the command's root record (`0x00520F94`); high nibble: `0x003DFFE0` adds 1 each call (`0x0040EE70`) and clears it when `+0x06` is 0 (`0x0040ED80`) |
| `+0x40` | `f32[4]` |  | direction (command `0x3F`), fourth float 1.0 (`0x00520F55`) |

```
entry +0x02  u8   0 skips the entry
entry +0x20  f32  weight
entry +0x29  u8   low nibble: weighted apply
entry +0x2A  u8   bit 0x1: apply at full weight
```

### The oscillator tree in a model file

`0x0040EEA0` turns these offsets into encoded pointers. Each is an offset from the oscillator record.

Record   `+0x00` u32 entries      `+0x04` u8 entry count entry    `0x30` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | chains | at [`+0x08`], `0x40` bytes each |
| `+0x03` | `u8` | pairs | at [`+0x0C`], `0x20` bytes each |
| `+0x04` | `u8` | list a | at [`+0x10`], `0x40` bytes each |
| `+0x05` | `u8` | list b | at [`+0x14`], `0x50` bytes each |
| `+0x06` | `u8` | list c | at [`+0x18`], `0x50` bytes each |
| `+0x07` | `u8` | list d | at [`+0x1C`], `0x60` bytes each |
| `+0x28` | `u8` | list e | at [`+0x24`], `0x40` bytes each |

```
chain    +0x03 u8 links   at [+0x04], 0x50 bytes each; link +0x00 u16 bone (0x0040ED90)
a, b, c, e   +0x03 u8 sub-records      at [+0x08], 0x10 bytes each
d            +0x0C u32 sub-records     at [+0x08], 0x10 bytes each
```

### Section 7 of @FCP

Section 7 starts at payload `+ [+0x0E]`¹; offsets below are from the section unless noted.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003E6F50` |

</details>

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16[8]` |  | offset of each event's records |

Event record (6 bytes, at the event's offset + 6 x variant):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | slot |  |
| `+0x01` | `u8` |  | pick byte for a random choice |
| `+0x02` | `u16` |  | rel: `0xFFFF` = no choices; the choice table starts at record + 2 + rel |
| `+0x04` | `u8` |  | 0 = disabled |

Choice table (offsets from its start):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` |  | source texture slot |
| `+0x01` | `u8` |  | destination texture slot |
| `+0x0C` | `u16` |  | offset of the rectangle table, from `+0x0C` |
| `+0x0E` | `u16` |  | choice count |
| `+0x10` | `u16[count]` |  | choice c's sequence is at `+0x10` + 2c + this value |

```
sequence:  u16 frame count, then per frame {u16 duration in ticks, u8 end action, u8 value}
rectangle table:  +0 / +2 destination x, y; +4 / +6 width, height; +0x0E + 4v / +0x10 + 4v source x, y for value v
```

### A sequencer entry (0x40 bytes at 0x02CA6CA0)

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` |  | in use |
| `+0x02` | `u16` |  | non-zero stops stepping (`0x004775E0`) |
| `+0x04` | `u32` | handle |  |
| `+0x08` | `u32` |  | render record |
| `+0x0C` | `u32` | variant |  |
| `+0x10` | `u8[8]` | active |  |
| `+0x18` | `u8[8]` | re-pick |  |
| `+0x20` | `u8[8]` | event (0xFF no event) |  |
| `+0x28` | `u8[8]` | choice |  |
| `+0x30` | `u8[8]` | frame |  |
| `+0x38` | `u8[8]` | ticks in the frame |  |

The record's functions are listed in
[model-oscillators-and-pose-sequencer-model-oscillator-subsystem.tsv](model-oscillators-and-pose-sequencer-model-oscillator-subsystem.tsv).

### Columns of model-oscillators-and-pose-sequencer-model-oscillator-subsystem.tsv

One row per function, 39 rows, in address order.

| Column | Holds |
|---|---|
| `address` | the function's start address |
| `size` | its length in bytes, as the disassembly's function list gives it (equal on all 39 rows) |
| `role` | what the function does in the oscillator and sequencer code, with the callers, callees and record fields that show it |
| `evidence` | how much of the function the role rests on: `full body` (the whole body read, 7 rows, four with the size in bytes); `head + call shape` or `head + store map` (the opening read, then its calls or its stores, 7 rows, one also with the float constants it loads); `call-signature` (its calls and the fields it touches, 19 rows); `body read in full` with the size in bytes (3 rows) or `body read at call sites` (`0x00415EE0`); `named` (by its function name, `0x001EDE70`); `non-function` (`0x00861F56`, a data row inside a math family) |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

| Fact | Value |
|---|---|
| sway presets | six rows at `0x01EFFA30`; the values are listed on [weather](../World-Areas-And-Travel/weather.md) |
| section 7 | in all 1,066 `.cm` blocks |
| blocks with an enabled event | 67: 54 NPCs and 13 `chara` models; events 0, 1 and 2 in each, all on slot 0 |
| choices per enabled event | 2 in 67, 3 in 122, 4 in 12 |
| sequences | 548, of 1, 3, 4, 5 or 6 frames; no sequence past its entry |
| durations | 1, 3, 10, 60 and 250 ticks; values 0 to 3 |
| last frame's end action | stop 67, hold 414, loop 67 |
| the NPC events (54 blocks) | event 0: snap to 0, 2→1→0 over three ticks each, or 0→2→0; event 1: snap to 2, or 0→1→2; event 2: wait 10, 60 or 250 ticks, then 0→2→0 one tick a step |

The counts above are for variant 0. Up to 12 variants are stored per event, by the spacing of the event offsets, and
67 models have an enabled record. Only variants 0 to 7 are enabled:
variants 1 to 7 in 34, 34, 29, 7, 4, 1 and 1 models.

| Table | Rows | One row per |
|---|---|---|
| [`model-oscillators-and-pose-sequencer-events.tsv`](model-oscillators-and-pose-sequencer-events.tsv) | 10,200 | event record of each model and variant, enabled or not |
| [`model-oscillators-and-pose-sequencer-sequences.tsv`](model-oscillators-and-pose-sequencer-sequences.tsv) | 1,408 | choice of a record with a choice table |
| [`model-oscillators-and-pose-sequencer-rectangles.tsv`](model-oscillators-and-pose-sequencer-rectangles.tsv) | 524 | rectangle table of a record with a choice table |

| Column | Table | Meaning |
|---|---|---|
| `path`, `event`, `variant` | all | the `.cm`, the event 0 to 7, and the variant, which the record's sequencer entry keeps |
| `offset` | events, sequences, rectangles | where the item starts, from the `@FCP` payload |
| `slot`, `pick`, `rel`, `enabled`, `raw` | events | record bytes `+0x00`, `+0x01`, word `+0x02`, byte `+0x04` and the whole 6 bytes |
| `source_slot`, `destination_slot`, `choice_table_bytes`, `rectangles`, `choices` | events | the choice table's two texture slots, its bytes `+0x02` to `+0x0B`, the rectangle table's offset from the choice table, and the choice count; `-` when `rel` is 0 or `0xFFFF` |
| `choice`, `frames`, `steps`, `after` | sequences | the choice, its frame count, each frame as `duration:end action:value`, and the two bytes after the last frame |
| `destination_x`, `destination_y`, `width`, `height` | rectangles | the rectangle's first four words |
| `raw_08_0d`, `sources` | rectangles | bytes `+0x08` to `+0x0D`, and the source position of each value the choices use, as `x,y` |

`Database/Tools/catalogues/pose_records.py` writes these tables.

</details>

## Operations

Per frame and model: two phase steps and, per enabled entry, the stages and one apply. A settle of `n`
sub-steps costs `n` passes of the stages. The sequencer steps eight slots per entry; the value read is
one lookup.

## State

<details>
<summary>Show the state it keeps</summary>

The wind byte `0x02CA4390` and the parameters `0x02CA4380`–`0x02CA439C`; each model's oscillator record in
its rig; the 32 sequencer entries at `0x02CA6CA0` with the serial `0x02CA6C94`, and the record's handle
`+0x450`.

</details>

## Modding notes

- The sway of a model is the sway section of its `@FCP` section 2 rig; a model with no sway section
  does not sway.
- Calm maps (wind preset 0) leave the global phase still; command `0x3F` sways a model on any map.
- Authored command `0x3F` with preset 0, or with a bone word of −1, turns the directed sway off.
- A section 7 event with `rel` `0xFFFF` or the enabled byte 0 does nothing; give every enabled event
  at least one choice.
- End actions other than 0, 1 and 2 leave the slot's frame at the frame count, one past the last frame
 ¹, counting ticks, so each later step reads its duration and end
  action from the bytes after the sequence².
- The sequencer variant is fixed when the model is bound; command `0x1D` with byte `0xFF` changes only
  the model row's `@FOR` key.
- Sequencer values are the ids of add-motion groups and rectangle columns; keep them below the
  rectangle table's length.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00477549`-`0x00477553`, `0x0047758A` |
| ² | `0x0047753E`-`0x00477542` |

</details>

## Related

- [Model files](model-files-cm-ca.md): `@FCP`, section 2 and section 7.
- [Add-motion tables](add-motion-tables.md): the pose groups the slot values select.
- [Weather](../World-Areas-And-Travel/weather.md): the map wind preset and the preset table.
- [Authored presentation commands](authored-presentation-commands.md): commands `0x1D`, `0x1E` and `0x3F`.
- [Subsystem update flags](../Engine-Core/subsystem-update-flags.md): the 60 fps predicate `0x001EDE80`.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 3 calls with 3 other topics</summary>

**Gameplay** (explained on [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00202E10`](model-oscillators-and-pose-sequencer.md) | is called by | [`0x00339630`](../Battle-Actions/action-phases.md) (on action phases) |

**Controls and input** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001EDE70`](../Menus-And-HUD/map-screens.md) (on map screens) | is called by | [`0x00253C70`](../Controls-And-Input/controls.md) (on controls) |

**Party** (explained on [player movement](../Movement-And-Pathfinding/player-movement.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00380800`](model-oscillators-and-pose-sequencer.md) | is called by | [`0x004742A0`](../Damage-And-Battle-Formulas/damage-formula.md) (on damage formula) |

</details>
