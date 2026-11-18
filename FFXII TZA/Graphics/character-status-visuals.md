[Home](../../README.md) / [Graphics](README.md) / Character status visuals

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Character status visuals: how a status changes a character's colour, light, opacity and shadow | system | Graphics | Character models / Character Rendering | The per-frame push that turns each battle unit's status word into presentation: the colour-look list where the lowest index wins, the tint, Stone, Petrify, Doom, Berserk and HP Critical looks made of private lights and the character's lighting fields, the second block that fades an Invisible character and colours the shadow under Slow and Immobilize, the rig switches for Sleep, Confuse, Immobilize and Float, and the two denial latches. | 0x003E7650, 0x02B59D80, 0x00320BB0, 0x0046FD00, 0x0046FFA0, 0x00470050, 0x004703F0, 0x004700E0, 0x0046FBB0, 0x00470AA0, 0x00470780, 0x00470590, 0x00470B70, 0x00470660, 0x00470EB0, 0x004704C0, 0x00470230, 0x0051E3A0, 0x0051DBF0, 0x0051DDC0, 0x0051DC90, 0x0051E0A0, 0x0051E170, 0x0051DE30, 0x00428CD0, 0x005044D0, 0x00428F10, 0x003ABD50, 0x003ACC10, 0x003ACAA0, 0x003E7CC0, 0x003E7C70, 0x02B59D70, 0x02B59D71, 0x01F20AA0, 0x01F21F40, 0x01F22030 |

## What the player sees

- A character with several ailments shows one colour look at a time, by a fixed order: Stone, Petrify, Berserk, Doom,
  Blind, Poison, Silence, Sap, Oil, Disable, Disease, HP Critical. Curing the top one brings up the next.
- Poison, Silence, Sap, Disable and Disease share one look, a pulsing darkening that pulls green down most. Blind is a
  plain pulsing darkening and Oil a much deeper one.
- A look must finish leaving before the next one appears. Blind, the shared look, Oil and Berserk fade in and out
  over ten frames.
- The other looks keep their own timing: Stone appears and goes at once, Petrify arrives and leaves over six
  frames (and goes at once when Stone replaces it), Doom has its own faster glow and flash, and HP Critical leaves
  only at the end of its beat.
- These frame counts are at 30 fps; at 60 fps they double and keep their length in seconds.
- Doom glows a dull red and flashes each time its count ticks; Petrify looks like Stone with a dip of the light on
  each tick; HP Critical flashes red once a second; Berserk turns red and dark on the side facing the camera.
- Invisible makes a character see-through, and an enemy more so than a party member. Slow and Immobilize colour the
  character's shadow orange-red and red. These show alongside a colour look.
- Sleep, Confuse, Immobilize and Float also move the body ([Character rig and look](character-rig-and-look.md)).
- Reverse, Lure, Protect, Shell, Haste, Bravery, Faith, Reflect, Regen and Libra change nothing on the body through this
  mechanism; KO, Bubble and X-Zone only set a flag.
- While a script or a menu turns the status display off (`setstatuserrordispdenystatus` and its `_by_menu` form), and
  in towns, the colour looks and the Invisible fade are hidden; while one turns on `setstatuserrorctrldenystatus`, the
  looks hold still.

Once per game tick the game reads each battle unit's status flags. For every status that has just started or ended it
switches a colour look, a shadow or see-through change, or a body motion on or off for that unit's character model,
and then updates the looks.

## How it works

### The push

`0x003E7650` runs once per simulation tick from the world tick `0x00314020`
([Frame update order](../Engine-Core/frame-update-order.md)). It walks 32 presentation records of `0x150`
bytes at `0x02B59D80`, one per battle-unit slot, skipping records whose word `+0` is 0. `0x003E7500` sets a record up: word
`+0` = 1, `+4` = the character's render-record index, both blocks initialised with that index (`0x004700C0`, `0x0051E140`).

Two readers give other code a record's dwords from `+0xC0`. `0x003E7D10(slot, n)` answers 0 while the byte `0x02B59D71` is
set (`0x003E7D10`-`0x003E7D17`), for slot -1 (`0x003E7D1C`-`0x003E7D1F`) and for a slot whose record has word `+0` at 0
(`0x003E7D35`-`0x003E7D39`). Callers pass a render record's dword `+0x6A4` as the slot (among them `0x0041C479`, `0x0041C677`,
`0x00421446`, `0x00423CD6`, `0x00424DDA`, `0x0042506C`, `0x0042508C`, `0x004257E9`, `0x0042735C`, `0x0042C46A`, `0x00516499`), which the
clear `0x0041F730` sets to -1 (`0x0041FB4E`).

`0x003E7CD0(index, n)`, from `0x003B0C50` and `0x0046CC70`, answers 0 for the same byte (`0x003E7CD5`-`0x003E7CDB`) and
otherwise walks the 32 records (`0x003E7CF9`-`0x003E7CFC`) for the first in use (word `+0` set, `0x003E7CE4`-`0x003E7CE8`)
whose `+4` is the render-record index (`0x003E7CEA`-`0x003E7CEE`), answering 0 when none has it (`0x003E7CFE`). Both return
dword `+0xC0 + 4n`.

For each record it reads the unit's status word through `0x00320BB0`: the OR of the stats record's `+0x64` and `+0x3C`
([Statuses](../Status-Effects-And-KO/statuses.md)). Stop is left out of the word while the unit's action id
`+0x714` is `0x21E` or lower and its action phase `+0x6B4` is 9 or more, or while bit `0x1000000` of its flag word is set
(`0x00320C10`-`0x00320C37`). `0x00320BB0` also writes whether the stats record's kind byte `+5` is 1 (an enemy) to the record's
`+0x84`.

`0x00320BB0(slot, &word, &enemy)` takes the unit from `0x00236820`, which gives 0 for a slot outside 0 to
`[0x0208E6A0]` − 1. It returns 0 and writes neither output when there is no unit, when bit `0x10` of the unit's flag
word is clear or when its stats record `+0x698` is null (`0x00320BC0`-`0x00320BDC`); the push then uses a zero word
and stores 0 in `+0x84` (`0x003E768F`-`0x003E769B`). Every other path returns 1 (`0x00320C0B`).

The record keeps the rig of the character's render record at `+0x10` (`0x003E6DA0`); with no rig, nothing else runs for
that record. When the word differs from the copy at `+8`, the push stores the bits that were set at `+0x140` and the
bits that were cleared at `+0x144`, then calls one arm per changed bit, cleared bits first. Every arm stores 1 or 0 in
the record's flag dword `+0xC0 + 4 × bit`. Then, changed or not, it runs the two block updates `0x0046FD00` (block
`+0x20`) and `0x0051E3A0` (block `+0x70`).

### What each status does

| Status (bit) | What the arm does beyond the flag dword |
|---|---|
| Stone (1) | colour look 0; bit `0x20` of render record `+0x304` through `0x00428F10`, which raises dirty bit `0x10000000` of `+0x290` |
| Petrify (2), Berserk (27), Doom (6), Blind (7) | colour looks 1, 2, 3, 4 |
| Poison (8), Silence (9), Sap (10), Oil (11), Disable (13), Disease (16) | colour looks 5, 6, 7, 8, 9, 10 |
| HP Critical (29) | colour look 13 |
| Stop (3) | second-block index 4; `+0x304` bit `0x20` as for Stone; `0x003E1310(rig, 0, 1 or 0)` stores the value in byte `+7` of rig slot 0, which makes the rig frame pass that slot a time input of 0 |
| Immobilize (14) | second-block index 0; rig controller 7 on or off |
| Slow (15), Invisible (24) | second-block indexes 1 and 3 |
| Sleep (4), Confuse (5) | rig controller 3 and the look controller's byte `+0x1C` bits `0x2` and `0x4` |
| Float (26) | rig controller 6 on or off |
| KO (0), Bubble (28), X-Zone (31) | nothing |
| mask `0x42FE1000` | no arm |

The arms are `0x0051E580`-`0x0051ECF0`, one pair per bit. The rig switches are on
[Character rig and look](character-rig-and-look.md).

The rig arms keep a word per status in the block they are given and reach the rig through the
block's `+0x10`, the look controller (rig slot 2) for its byte `+0x1C`:

| Status | Enter | Leave |
|---|---|---|
| Confuse | `0x0051E670`: `+0xD4` = 1; controller 3 on unless `+0xD0` (asleep); look byte `+0x1C` bit `0x4` set | `0x0051E620`: `+0xD4` = 0; controller 3 off; bit `0x4` cleared |
| Sleep | `0x0051EA10`: `+0xD0` = 1; controller 3 off when confused; bit `0x2` set | `0x0051E9C0`: `+0xD0` = 0; controller 3 on when confused; bit `0x2` cleared |
| Immobilize | `0x0051E740`: `+0xF8` = 1, `0x0051DBF0` on the block's `+0x70`, controller 7 on | `0x0051E700`: `+0xF8` = 0, `0x0051DDC0`, controller 7 off |
| Float | `0x0051E840`: `+0x128` = 1, controller 6 on | `0x0051E800`: `+0x128` = 0, controller 6 off |

### The colour-look list

Block `+0x20` keeps a fourteen-bit mask at `+0`. The add worker `0x0046FFA0` and the remove worker `0x00470050` set or clear
one bit, keep the entry count in the upper seven bits of byte `+7`, and store the lowest set index in byte `+5`, or
`0xFF` when the mask is empty. Byte `+5` is the wanted look; the order in the table above is the index order.

Both workers take a look index `n` and change the bit value `1 << n`. An add of a bit already set, or a remove of a
bit already clear, returns at once with nothing changed (`0x0046FFB4`, `0x00470066`), and the lowest set index is looked
for among bits `0x1` to `0x2000` only (`0x0046FFD4`-`0x0046FFF0`, `0x00470090`-`0x004700AC`).

The update `0x0046FD00(block, render record, display deny, control deny)` runs each tick:

1. It stores the render record at `+0x28` and the hold byte `+0x3A`: the control-deny byte, or 0 while display is
   denied.
2. When the wanted look `+5` differs from the shown look `+4`, it copies it over and sets the changing bit, bit `0x1` of
   `+7`.
3. It calls the step at `+0x18`; with no step, the changing bit is the answer. A step returns 1 only when its look has
   fully left.
4. Only then, with a non-empty list (an entry count in byte `+7`, `0x0046FD72`) and a shown look of 13 or less, it
   installs the shown look by a switch on `+4` (`0x0046FD7B`-`0x0046FD9A`).
5. While display is denied it also zeroes render record byte `+0x5E0` and sets the record mode to 0.

Installing a look clears the changing bit, releases the block's two light handles `+8` and `+0xC`, sets the record
mode and stores the look's step. Indexes 11 and 12 have no arm in the push; index 12 has a look, the tint with offset
`(1.5, 2.0, 2.0)`.

The switch entry for index 11 jumps to its end (`0x0046FF20`): nothing is installed and the changing bit stays set.
Stone and Petrify are installed in the switch itself: the step `0x00470AA0` or `0x00470780`, the phase `+0x20`, the
frame `+6` and the state `+0x38` zeroed, and mode 3 or 0 (`0x0046FD9C`-`0x0046FE22`); so is Oil
(`0x0046FE59`-`0x0046FF00`). Blind, the shared look and index 12 go to the tint `0x004703F0`, Berserk to `0x00470660`,
Doom to `0x00470590` and HP Critical to `0x004704C0`.

`0x003E75A0` resets every block in use of the 32 from `0x02B59D80`, and `0x003E7D50` one block. Each
reset runs `0x00470000` on the block's `+0x20`, which clears the mask and the bits of byte `+7`
above bit `0x1`, sets the shown and wanted looks (`+4`, `+5`) to `0xFF` and releases the two lights
`+8` and `+0xC` (`0x003ABCA0`), and then `0x0051DC60` on `+0x70`.

### The record mode

`0x00428CD0(render record, mode)` stores the mode in byte `+0xBA` of the model instance (`0x00504D20`) of the record and of
every record attached under it, skipping those `0x00426220` rejects. `0x005044D0(instance, n)` uses it to pick entry `n`'s
parameter block: `table + entry.offset + mode × entry.stride`, with the table at instance `+0x1F8` plus `+0x21C`,
sixteen-byte entries from table `+0x30`, the stride the word at entry `+2` and the offset the dword at entry `+0xC`.

Stone and Petrify set mode 3 (Petrify in the states its table below names), the flash frames of Doom
and HP Critical mode 2, every other look mode 0.

`0x00428CD0` reaches the records through their index words: it takes the record again from its own word `+0`,
returning at once when that is −1, then takes the first child `+0x08` and hands that child's `+0x08` and `+0x0A`
chains to `0x0042EF90` with the body `0x0042E4F0` (`0x00428CE9`-`0x00428DB8`). A record without a model instance
(`0x003E55B0` gives 0 while word `+0x64` is −1) is skipped as well.

`0x005044D0` returns 0 when `+0x21C` is −1 or `n` is not below the dword at table `+0xC` (`0x005044D9`, `0x005044ED`).
The table address is summed in 32 bits and the mode is read as a signed byte (`0x005044E1`-`0x0050450D`).

### The tint

`0x004703F0` stores the offset at `+0x40`, zeroes the phase and envelope, installs the step `0x004700E0` and creates a light
(`0x003AB960`) from an `0x50`-byte request: type 6 (ambient), priority `0xBF`, byte `+3` = 1 and `+4` = 2, target id the
block's `+0x10`, byte `+5` = `0x90` and `+7` = `0x80`. Its handle goes to `+8`.

Each frame `0x004700E0` returns 0 at once while the hold byte is set. Otherwise the phase `+0x20` rises by
`[0x01DFE0BC] × 0.0333` and goes back to 0 when it reaches 1 (`0x00470133`). The envelope `+0x24` rises by
`0.1 × [0x01DFE0BC]` to 1, or falls at that rate while
the changing bit is set; at zero it releases the light, zeroes `+8`, clears the step and returns 1
(`0x00470166`-`0x00470184`). Every other path returns 0.

`0x0046FBB0(t)` returns entry `t × (count − 1)` of the table, truncated and clamped to 0 to count − 1, with the count
`0x01F20538` (`0x0046FBB0`-`0x0046FBE6`). With `p` the pulse at the phase
(`0x0046FBB0`, the table `0x01F20AA0`):

```python
light colour = offset × (0.5 + 0.5p) × envelope, alpha 1.0
record +0x5EC = 1 - (0.8 + 0.2p) × envelope
```

Blind's offset is `(-0.5, -0.5, -0.5)`, the shared look's `(-0.2, -0.7, 0)`. Oil installs the same step with
`(-2, -2, -2)` and its own light: type 1 (directional), priority `0xBE`, byte `+5` = `0x80`, byte `+6` = 1, vector
`(0, -1, 0)` at request `+0x30`.

### Stone and Petrify

Stone's step `0x00470AA0` raises its phase by `[0x01DFE0BC] × 0.03333` a frame and holds it at 1
(`0x00470AB3`-`0x00470AD6`): the phase is 0.9999 after 30 frames at 30 fps and after 60 frames at 60 fps, and
reaches 1 on the next frame. Each frame it sets render record byte
`+0x5E0` = 2, `+0x5DC` = `1 + 0.3 × pulse(phase / 2)`, `+0x5EC` = 0.4 and mode 3. When the look changes it sets mode
0, releases both handles and returns 1 in the same frame. It creates no light.

While the hold byte is set Stone's step returns 0 and writes nothing (`0x00470AAD`); leaving also zeroes both
handles and the step (`0x00470B53`-`0x00470B59`).

Petrify's step `0x00470780` has four states in byte `+0x38`; frame counts below are multiplied by `[0x01DFE0B4]`:

| State | What it does |
|---|---|
| 0, arriving | ambient mode 2 with `+0x5DC = 1 - 0.7 × pulse(t)`, `t` rising by `[0x01DFE0BC] / 6`; mode 0 and light scale 1.0 for the first three frames, then mode 3 and 0.4; after six frames it reads the Petrify count and goes to state 1 |
| 1, steady | ambient mode 0, mode 3, scale 0.4; a changed, non-zero count starts state 2. When the look must leave: if Stone's bit is in the mask it releases and returns 1 at once, otherwise it goes to state 3 |
| 2, tick | ambient mode 2 with `1 - 0.3 × pulse(t)`, `t` rising by `0.05 × [0x01DFE0BC]`; mode 3, 0.4; back to state 1 after twenty frames |
| 3, leaving | state 0's dip with mode 3 and 0.4 for three frames, then mode 0 and 1.0; releases and returns 1 after six frames |

The count comes from `0x00320CF0(unit, status)`, which returns the stats record's `+0xBC + 4 × status` for Petrify and Doom
while the status is set ([Status timers](../Status-Effects-And-KO/status-timers.md)), and -1 otherwise. The unit
is the byte `+0xEA9` of the object behind render record `+0x108` (`0x00263E50`).

### Doom, HP Critical and Berserk

Doom's installer `0x00470590` creates the tint's ambient light and installs `0x00470B70`, zeroing the phase, the
envelope, the frame `+6` and the state `+0x38` with `+0x39` (`0x004705BA`-`0x004705C5`). In the steady state the envelope
moves by `0.33 × [0x01DFE0BC]` a frame, the light colour is `envelope × 0.4 × (0.9, -0.2, -0.2)`, the light scale is 1.0
and the mode 0. Every steady frame that is not leaving, a Doom count different from the one remembered at `+0x39`
starts a flash; the installer zeroes `+0x39`, so the look starts with one. The flash runs 21 frames:

```python
light colour = (0.6 × curve1[f] + 0.4 × envelope) × (0.9, -0.2, -0.2)
record +0x5EC = 1 - curve2[f]
frames 3-10    : mode 2, record colour +0x5D0 = (0.84, 0.84, 0.84); otherwise mode 0 and (1, 1, 1)
frames 0-20    : ambient mode 1 with +0x5DC = curve1[f]
```

HP Critical's installer `0x004704C0` creates the same light with the step `0x00470230`, zeroing the phase and the frame
`+6` but not the envelope (`0x004704EC`-`0x004704F3`); the step runs the same recipe with the
colour `curve1[f] × (0.64, 0, -0.32)` on a 30-frame cycle. From frame 21 to the end of the cycle it sets bit `0x2` of
the light's byte `+7`, which makes the light selector skip it, and clears ambient mode. It checks whether to leave only
when the cycle wraps, so it always finishes its beat.

Berserk's installer `0x00470660` creates two lights: the tint's ambient into `+8` and Oil's directional request into
`+0xC`, without Oil's vector: request `+0x30` stays zero, and the step aims the light every frame
(`0x004706E6`-`0x00470744`). The installer zeroes the phase and envelope (`0x0047069B`).
Its step `0x00470EB0` uses the tint's phase and envelope; with `w = (0.5 + 0.5p) × envelope`:

```python
ambient colour = (2w, 0, 0)
directional colour = (-3.5w, -3.5w, -3.5w)
directional vector = normalise(point - camera position 0x02AEDF20)
record +0x5EC = 1 - (0.85 + 0.15p) × envelope
```

The point is the translation of the matrix `0x00421E20` returns for bone code `0x100`. While the hold byte is set the step
still re-aims the light every frame and does nothing else.

### Where the lighting fields go

The per-character light gather `0x003ABD50` copies render record `+0x5EC` to `0x02B3F518` before it calls the light selector
`0x003ACC10`. The ambient evaluator `0x003ACAA0` multiplies a light's red, green, blue and strength by `0x02B3F518`, and
sets its alpha to `0x02B3F518` itself, while the enable byte `0x02B3F502`
is set and the light's byte `+5` is below `0x80`, so the status lights (`0x90`, `0x80`) are never dimmed by it
(`0x003ACB7A`-`0x003ACC00`).

In the selector, an ambient light without bit `0x10` in byte `+5` is changed before it is summed: render record byte `+0x5E0`
= 2 multiplies it by `+0x5DC`, and 1 blends it toward the record colour `+0x5D0`-`+0x5D8` by `+0x5DC`. A light is skipped
when its byte `+7` shifted right by two meets the class filter `0x02B3F520 | 0x02B3F501`, or when byte `+7` has bit `0x2`.
The lighting itself is on [Character lighting and shadows](character-lighting-and-shadows.md).

### The second block

Block `+0x70` keeps a mask at `+0x10`. Its workers `0x0051DBF0` (add) and `0x0051DDC0` (remove) take an index `n`,
set or clear the bit value `1 << n`, return at once when it is already set or clear (`0x0051DC06`, `0x0051DDD6`), and
derive three bytes:

| Byte | Value |
|---|---|
| `+0x19`, channel A | 2 when mask bit `0x4`, else 3 when bit `0x8` (Invisible), else `0xFF` |
| `+0x31`, channel B | 0 when bit `0x1` (Immobilize), else 1 when bit `0x2` (Slow), else `0xFF` |
| `+0x33` | mask bit `0x10` (Stop) |

`0x0051E3A0` returns at once while control is denied and display is not. Otherwise it runs the wanted, shown, changing
and step protocol for each channel: channel A installs `0x0051E0A0` for 2 and `0x0051DC90` for 3, channel B `0x0051DE30` for
0 and `0x0051E170` for 1. While the Stop byte is set and display is not denied it calls `0x003E7450(render record, 0, 0, 1)`
every frame. While display is denied it then writes fade channel 5 = 1.0 (`0x00428940`), the shadow's `+0xC` = 1.0
(`0x003B6B10`) and the shadow's colour = 0 (`0x003B6B30`), after the steps have run.

`0x0051E3A0` stores the render record at `+0x08` before that return (`0x0051E3C0`). Installing a step clears the
channel's changing byte and zeroes its phase and envelope (`0x0051E41E`-`0x0051E426`, `0x0051E46F`-`0x0051E477`); a shown
value without a step above installs nothing.

These steps use a phase stepping by `0.033 × [0x01DFE0BC]` and an envelope moving by `0.1 × [0x01DFE0BC]`:

- Invisible, `0x0051DC90`: fade channel 5 = `1 - (0.6 + 0.2p) × envelope`, or `1 - (0.88 + 0.08p) × envelope` when the
  block's `+0x14` (the record's enemy flag) is set; `0x00428AF0(record, 1, 1, 0x60)` sets `+0x304` bits `0x20000`, `0x40000` and the
  byte at the bits under mask `0x7F80000`, and raises bit `0x4000000` of `+0x294` (`0x00428B17`).
- Leaving Invisible restores 1.0 and clears the two bits through `0x00428AF0(record, 0, 0, 0x60)`, which writes `0x60`
  to the byte again; it clears the step and returns 1 (`0x0051DCF5`-`0x0051DD20`; [Character fades](character-fades.md)).
- Index 2, `0x0051E0A0`: fade channel 5 = `1 - envelope`. No status selects it. Leaving restores 1.0, clears the step
  and returns 1 (`0x0051E0D8`-`0x0051E0F3`); it keeps no phase and leaves `+0x304` alone.
- Slow, `0x0051E170`, while render record `+0x114` holds a shadow: with `s = (0.5 + 0.3p) × envelope`, the shadow's
  colour = `(128s, 32s, 8s)` as integers, and the vector `(1 + 0.1p, 1 - 0.1p, 1 - 0.1p, 1)` goes to `0x001F1600`, which
  stores it at `0x02CB8390`; then `0x0051E510(word +0 of the record, 1)`.
- Slow's phase goes back to 0 when it reaches 1
  (`0x0051E1AC`-`0x0051E1B6`); its envelope rises to 1 while byte `+0x32` is 0 (`0x0051E28B`-`0x0051E29A`) and falls while it
  is set, the leaving path below running at 0 or below (`0x0051E1D2`-`0x0051E1E6`).
- Immobilize, `0x0051DE30`: the same with `s = (0.7 + 0.3p) × envelope`, colour `(128s, 16s, 4s)`, vector
  `(1 + 0.3p, 1 - 0.3p, 1 - 0.3p, 1)`, and the shadow's `+0xC` = `1 + (1.5 + 0.5p) × envelope`.
- Leaving, Slow and Immobilize restore the shadow's `+0xC` to 1.0, its colour to 0, store `(0, 0, 0, 1)` at
  `0x02CB8390`, call `0x0051E510(word +0 of the record, 0)`, clear the step `+0x40` and return 1 (`0x0051E1EC`, `0x0051E281`; `0x0051DEAF`,
  `0x0051DF44`).

`0x0051E510(index, flag)` takes the render-record index (`0x0051E529`-`0x0051E536`), walks that record and every record
attached under it and calls the method at offset `0xC8` of each render
object (record `+0x6B8`) with 1 or 0. The shadow pool is 160 entries of `0xE0` bytes at `[0x02B40528]`; `0x003B6B10` and
`0x003B6B30` write only when the handle matches the entry's `+0x10`.

### The denial latches

- `0x02B59D70`, control deny, is written only by `0x003E7CC0`. `0x002EA8E0(bit, on)` keeps the requester bits in
  `0x0215FD44` and sets the latch while any is set.
- `0x02B59D71`, display deny, is written only by `0x003E7C70`. Setting it ORs `0x20` into the class filter `0x02B3F501`, clears
  the enable byte `0x02B3F502` and sets `0x02B59D68`; clearing reverses all three. `0x002EA8B0` keeps its requester bits in
  `0x0215FD45`.

Bit `0x1` of the requester bytes comes from the `ctrldenystatus` and `dispdenystatus` verbs
([Time stop and freeze](../Engine-Core/time-stop-and-freeze.md)), bit `0x4` from the town flag
([Party control modes](../Engine-Core/party-control-modes.md)). Class 5 (byte `+7` = `0x80`) is the status
lights, so display denial switches them off and lifts the dimming while the steps keep running.

### Stretching the tables for 60 fps

The pulse table, the two curves and the other frame tables from `0x01F20530` to `0x01F264AC` hold one entry per
frame at 30 fps. When the game switches to the 60 fps time base (`0x001EDDC0`), `0x0033F020` doubles each
table's frame count and resamples the table in place to twice its entries (`0x0046FBF0`, `0x00471100`,
`0x00471330`, `0x004715F0`, `0x004718F0`, `0x00472580`, `0x00473210`).

Four resamplers do the work. Each takes the table, the new entry count `n` and the number of channels per entry, copies the
first `n / 2` entries aside, and writes entry `2k` as source entry `k` and entry `2k + 1` as the mean of
source entries `k` and `k + 1`:

| Resampler | Values | Past the last source entry |
|---|---|---|
| `0x0033E310` | `f32` | wraps to entry 0 (`(k + 1) mod n/2`) |
| `0x0033E5E0` | `f32` | stops at `n − 1`; the last entry copies source entry `(n − 1) / 2` |
| `0x0033E990` | signed bytes | wraps |
| `0x0033ECE0` | unsigned bytes | stops, as `0x0033E5E0` |

- `0x0046FBF0` doubles the counts `0x01F20530` to `0x01F2053C` and `0x01F20A98` and resamples the pulse table
  `0x01F20AA0` among others with `0x0033E5E0`; `0x00471100` stretches the two curves `0x01F21F40` and `0x01F22030`
  to 60 entries with `0x0033E310`.
- `0x00471330`, `0x004715F0` and `0x004718F0` double their counts and resample their float tables with
  `0x0033E310` and `0x0033E5E0`, and `0x004718F0` two byte tables with `0x0033ECE0`.

The first of those counts, `0x01F20530` (50 in the file), sizes a curve of three floats per entry at
`0x01F20540`. `0x0046FB40(t, out)` samples it at `t` from 0 to 1 (entry `t × (count − 1)`, clamped).

Its one caller, `0x0042F030`, from the character pass `0x00426090`, walks 32 records of `0x30` bytes at
`0x02CA48D0`, each live while its handle `+0x04` is set (`0x0042F190(handle)` clears it, and `0x0042F000`
clears them all at start-up): a set trigger `+0x1C` starts a run of `30 × [0x01DFE0B4]` steps with the strength
`trigger × [0x01DFE0BC]`, each step adds strength × the curve sample to the three floats `+0x20`–`+0x28`,
and the record named by the word `+0x00` gets them at `+0x260`–`+0x268`, its per-axis scale.

- `0x00472580` and `0x00473210` double eight and five counts, copy each to a byte beside the tables
  (`0x01F240F0`, `0x01F264A8`), halve the floats beside them, and resample three-channel byte tables with
  `0x0033E990`.

## Layouts

Presentation record, `0x02B59D80` + slot × `0x150`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u16` | live | 1 when set up by `0x003E7500` |
| `+0x004` | `i16` | record | the render-record index |
| `+0x008` | `u32` | shown | the status word last pushed |
| `+0x010` | `void*` | rig | `0x003E6DA0` of the render record, 0 = no rig |
| `+0x020` | `0x50` | colourList | block 1 |
| `+0x070` | `0x48` | second | block 2 |
| `+0x0C0` | `u32[32]` | flags | one per status bit |
| `+0x140` | `u32` | setBits |  |
| `+0x144` | `u32` | clearedBits |  |

Colour-look block (record `+0x20`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | mask | mask `0x3FFF` |
| `+0x04` | `u8` | shown |  |
| `+0x05` | `u8` | wanted | lowest set bit, `0xFF` = no bit set |
| `+0x06` | `u8` | frame | flash and cycle counter |
| `+0x07` | `u8` | flags | bit `0x1` changing, mask `0xFE` entry count |
| `+0x08` | `u32` | light0 | handle |
| `+0x0C` | `u32` | light1 | handle |
| `+0x10` | `u32` | target | the render-record index the lights belong to |
| `+0x18` | `void*` | step |  |
| `+0x20` | `f32` | phase |  |
| `+0x24` | `f32` | envelope |  |
| `+0x28` | `void*` | renderRecord |  |
| `+0x38` | `u8` | state | Petrify and Doom |
| `+0x39` | `u8` | count | the remembered Petrify or Doom count |
| `+0x3A` | `u8` | hold | control deny |
| `+0x40` | `f32[4]` | offset | the tint's colour offset |

Second block (record `+0x70`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `void*` | renderRecord |  |
| `+0x10` | `u32` | mask |  |
| `+0x14` | `u32` | enemy |  |
| `+0x18` | `u8` | shownA |  |
| `+0x19` | `u8` | wantedA |  |
| `+0x1A` | `u8` | changingA |  |
| `+0x1C` | `f32` | phaseA |  |
| `+0x20` | `f32` | envelopeA |  |
| `+0x28` | `void*` | stepA |  |
| `+0x30` | `u8` | shownB |  |
| `+0x31` | `u8` | wantedB |  |
| `+0x32` | `u8` | changingB |  |
| `+0x33` | `u8` | stop |  |
| `+0x34` | `f32` | phaseB |  |
| `+0x38` | `f32` | envelopeB |  |
| `+0x40` | `void*` | stepB |  |

Render-record fields the looks write:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x5D0` | `f32[3]` | colour | the ambient blend target |
| `+0x5DC` | `f32` | amount | ambient mode amount |
| `+0x5E0` | `u8` | ambientMode | 1 blend, 2 multiply |
| `+0x5EC` | `f32` | lightScale | copied to `0x02B3F518` |

## Shipped data

Measured from the executable image.

| Fact | Value |
|---|---|
| pulse table `0x01F20AA0` | 60 floats, a raised cosine from 0.0027 to 1.0 at entry 29 and back to 0; count `0x01F20538` = 60 |
| curve 1 `0x01F21F40` | 0.33, 0.66, then 1.0 to entry 11, falling by 0.1 to 0 at entry 21 |
| curve 2 `0x01F22030` | 0.5, 0.85, then 1.0 to entry 16, falling by 0.2 to 0 at entry 21 |
| frame values at 30 fps | `0x01DFE0BC` 1.0, `0x01DFE0B8` 1.0, `0x01DFE0B4` 1, `0x01F82E38` 0 |
| frame values at 60 fps | `0x001EDDC0` stores 0.5, 2.0, 2 and 1, then `0x0033F020` doubles the pulse table's count (`0x0046FBF0`) and stretches the two curves over twice the frames (`0x00471100`) |
| Immobilize constants | 1.5 (`0x00901B3C`), 0.5 (`0x01CEBB70`), 0.3 (`0x0091523C`), 0.7 (`0x008F3104`) |

[`status-visual-curves.tsv`](status-visual-curves.tsv) lists every stored sample of the six float tables above, with
raw bits and addresses. [`status-visual-curves-60fps.tsv`](status-visual-curves-60fps.tsv) lists what the two
resamplers compute from them. Those values are worked out from the code and are not stored in the executable.

| `table` | Address | Channels | Stored entries | Read at |
|---|---|---|---|---|
| `pulse` | `0x01F20AA0` | 1 | 60 | `0x0046FBB0` |
| `curve1` | `0x01F21F40` | 1 | 30 | the steps `0x00470230` and `0x00470B70` |
| `curve2` | `0x01F22030` | 1 | 30 | the steps `0x00470230` and `0x00470B70` |
| `scale` | `0x01F20540` | 3 | 50 | `0x0046FB40` |
| `0x01F209F0` | `0x01F209F0` | 1 | 21 | named only by `0x0046FBF0` (`0x0046FC5E`) |
| `0x01F20C80` | `0x01F20C80` | 1 | 60 | `0x0046FACF` |

Columns of the first table:

| Column | Meaning |
|---|---|
| `table`, `table_address`, `channels` | the table, as above |
| `entry`, `channel` | the sample's entry and its channel within the entry |
| `address` | the sample's address in the image |
| `f32_bits` | its raw 32-bit float |
| `value` | the same number to nine significant digits |

The 60 fps table has the same `table`, `entry`, `channel`, `f32_bits` and `value` columns, then:

| Column | Meaning |
|---|---|
| `resampler` | `0x0033E5E0` for four tables, `0x0033E310` for `curve1` and `curve2` |
| `from` | the source entry, the two source entries of the mean, or the source entry the last entry copies |

The samples come from the executable with sha256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## State

- `0x02B59D80`: the 32 presentation records.
- `0x02B59D70`, `0x02B59D71`: the control-deny and display-deny latches; `0x0215FD44`, `0x0215FD45` their requester bits.
- `0x02B3F518`: the light scale of the character being lit; `0x02B3F501` the class filter; `0x02B3F502` the scale enable.
- `0x02CB8390`: the vector Slow and Immobilize store.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F20534` | `u32` | 21 | the entry count of the one-float table at `0x01F209F0` (0.75, 0.5, 0.25, 0, 0.33, 0.67, nine entries of 1.0, 0.67, 0.33, 0, 0.25, 0.5, 0.75), the second of the four counts from `0x01F20530`; `0x0046FBF0` doubles it and resamples the table to the new count with `0x0033E5E0` (`0x0046FC58`-`0x0046FC6B`) | `0x0046FBF0` (`0x0046FC23`) | `0x0046FBF0` (`0x0046FC15`, `0x0046FC58`) |
| `0x02CA4ED0` | `u32` | 0 (zero-filled tail) | the dword just past the 32 records of `0x30` bytes at `0x02CA48D0`; the start-up clear `0x0042F000` stores 0 in it before it clears each record's handle | `0x0042F000` (`0x0042F009`) | no instruction names it apart from that store |

## Modding notes

- The order of the colour looks is the bit order of the list; moving a status means changing the index its arm passes.
- The look colours of the switch in `0x0046FD00` and the steps' colour factors are `.rdata` constants (`0x0046FE34`,
  `0x0046FE50`, `0x00470C50`, `0x004702B3`, `0x00471041`); the flash frames' `+0x5D8` value is an immediate (`0x00470CF9`,
  `0x0047033E`).
- A status light is exempt from the light scale only while its byte `+5` is `0x80` or more.
- Durations are frame counts scaled by `0x01DFE0B4`, so they keep their length in seconds at 60 fps.

## Related

- [Statuses](../Status-Effects-And-KO/statuses.md): the 32 status bits and the two status words.
- [Status timers](../Status-Effects-And-KO/status-timers.md): the Petrify and Doom counts.
- [Character rig and look](character-rig-and-look.md): the controllers Sleep, Confuse, Immobilize and Float switch.
- [Character fades](character-fades.md): fade channel 5.
- [Character lighting and shadows](character-lighting-and-shadows.md): the light gather and the shadow pool.
- [Character render records](character-render-records.md): the render record.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): the status-denial verbs.
- [Party control modes](../Engine-Core/party-control-modes.md): the town flag.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat AI: `0x00236820` is called by `0x00301AD0`, `0x00308C20`, `0x003219D0`, `0x003247F0`, `0x00324F20`; those functions are
  documented on [glossary](../Engine-Core/glossary.md),
  [gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md).
- Combat action: `0x00236820` is called by `0x00306760`, `0x003083B0`, `0x0030F760`, `0x003105D0`.
- Combat action: those functions are documented on
  [party control modes](../Engine-Core/party-control-modes.md),
  [gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md),
  [identifier spaces](../Engine-Core/identifier-spaces.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Combat formula: `0x00236820` is called by `0x0031B860`, `0x0031E800`; those functions are documented on
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
- Gameplay: `0x00236820` is called by `0x0030C210`; those functions are documented on
  [enmity](../Enemy-AI-And-Gambits/enmity.md).
- Items equipment shops license: `0x00236820` is called by `0x0031A300`; those functions are documented on
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Spawn encounter lifecycle: `0x00236820` is called by `0x00308D90`; those functions are documented on
  [battle units](../Characters-And-Objects/battle-units.md).
- UI: `0x00236820` is called by `0x0031EB20`, `0x00322A80`; those functions are documented on
  [action definition row](../Battle-Actions/action-definition-row.md),
  [target selection](../Battle-Actions/target-selection.md).
