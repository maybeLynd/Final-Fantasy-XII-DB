---
system: How a status shows on a character - one look at a time, by priority
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the status push 003E7650 read for its change detection, its two dispatch chains and its per-record tail; all
    forty-two non-empty arms summarised by script (field written, block, index, worker) and eight read whole; the two
    workers of each block, the first block's update 0046FD00 with its jump table decoded from the image, the tint
    installer, the tint step, the HP Critical installer, the pulse lookup and its sixty-entry table, the record mode
    setter and the second block's update 0051E3A0 read whole
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-status-look-falsification-pass-1
  crossref_clean: true
  reopened_count: 0
  note: written by FABLE; static throughout - the colours are constants read from the image, not colours seen on a
    screen; six look bodies are named and not read, and the page says which; first review = the 0929 promotion sweep: promoted DOCUMENTED -> AUDITED
    2026-09-30 by SWE2-AUDIT-SPEC: falsification pass-1 (opus-status-look) FAILS 0 reproduced,
    all seven clauses (H0-H6) survive with no correction; four classified neighbour edges
    dispositioned (incl. the EC7 mechanical-crossing note); zero open boxes
---

# How a status shows on a character

A character can carry many statuses at once, but its body shows **one colour look at a time**. This page is the
machinery that decides which, and what each look is made of. It is the presentation side of
[the thirty-two statuses](../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md): nothing here changes a rule of
the game.

## 1. What the player sees

- A character with several ailments shows the look of the **most important** one, by a fixed order: Stone, Petrify,
  Berserk, Doom, Blind, Poison, Silence, Sap, Oil, Disable, Disease, HP Critical. Cure the top one and the next shows.
- **Poison, Silence, Sap, Disable and Disease share one look**: the same pulsing colour offset, `(-0.2, -0.7, 0.0)` -
  green pulled down hardest, blue untouched. Blind is a pulsing darkening, `(-0.5, -0.5, -0.5)`. Oil is `(-2, -2, -2)`.
- The pulse is a raised cosine, **one beat every thirty frames**, swinging the offset between half and all of its
  strength; a look fades in over ten frames and **fades out over ten frames before the next one may start**.
- Four statuses show through a second, independent mechanism and can be seen together with a colour look:
  Immobilize, Slow, Invisible and Stop.
- Float, Immobilize and Confuse also move the body - [the rig](the-rig-of-seventeen-controllers.md) section 4.
- Ten statuses show nothing on the body through this machinery: Reverse, Lure, Protect, Shell, Haste, Bravery, Faith,
  Reflect, Regen, Libra.
- **While status *control* is denied** (the `...ctrldenystatus` verbs, by their name - the pick-up message idiom calls one) **the colour
  look holds still**: it neither pulses nor leaves. While status *display* is denied (the `...dispdenystatus` verbs) the
  status lights are switched off and the dimming lifted (section 4a), the record mode is forced to 0 and the second
  mechanism is reset.

## 2. The push

`003E7650` (1,566 B) walks **thirty-two presentation-parameter records of `0x150` bytes at `02B59D80`**, one per battle
unit slot. For each live record it fetches the unit's status word (the OR of the two status dwords of the unit's stats
record), compares it with the copy at `+8`, stores the **set** bits at `+0x140` and the **cleared** bits at `+0x144`,
and runs one call per changed bit. Then, changed or not, it runs the two block updates of sections 3 and 4.

**The record keeps one flag dword per status at `+0xC0 + 4 x bit`** - KO at `+0xC0`, Stone at `+0xC4`, ... Float at
`+0x128`, HP Critical at `+0x134` - and every arm begins by storing 1 or 0 there. After that an arm does one of five
things (the ~~forty-two~~ forty-four non-empty arms *(corrected 2026-10-02, OPUS: bit 31's pair `0051E7A0` / `0051E7B0` too, `003E7650`+0x318 and +0x580)*, summarised by script from their bodies):

| what the arm does | statuses (bit) and the index they pass |
|---|---|
| nothing more | KO (0), Bubble (28) |
| adds or removes an entry of **the colour-look list** (block `+0x20`) | Stone (1) **0**, Petrify (2) **1**, Berserk (27) **2**, Doom (6) **3**, Blind (7) **4**, Poison (8) **5**, Silence (9) **6**, Sap (10) **7**, Oil (11) **8**, Disable (13) **9**, Disease (16) **10**, HP Critical (29) **13** |
| adds or removes an entry of **the second block** (`+0x70`) | Immobilize (14) **0**, Slow (15) **1**, Invisible (24) **3**, Stop (3) **4** |
| switches a rig controller | Sleep (4) and Confuse (5) controller 3, Immobilize (14) controller 7, Float (26) controller 6 - [the rig](the-rig-of-seventeen-controllers.md) |
| also sets or clears **bit 5 of the render record's `+0x304`** (`00428F10`, 31 B, which raises dirty bit 28 of `+0x290`) | Stone and Stop - the two statuses under which a body does not move. What the bit does was not read |

Indices 11 and 12 of the colour-look list and index 2 of the second block have no status arm; index 12 has a look
(section 3) that nothing in this push selects.

## 3. The colour-look list: fourteen entries, the lowest index wins

Block `+0x20` of the record. The two workers, `0046FFA0` (85 B, add) and `00470050` (97 B, remove), are mirror images:
set or clear bit *index* of the mask dword `+0`, count the entries in the upper bits of byte `+7`, and store **the
index of the lowest set bit** in byte `+5` - `0xFF` when the mask is empty. *That byte is the look the character
should show.* The order of section 1 is nothing more than the index order.

**The update (`0046FD00`, 615 B)** is a small state machine with a rule: *a look must finish leaving before another may
arrive.*

1. It records the render record (`+0x28`) and a *hold* byte: `+0x3A` := the global byte `02B59D70`, or 0 while status
   display is denied. **`02B59D70` is the control-deny latch**: its one writer `003E7CC0` (7 B) is called with 1 or 0 by
   the requester set `002EA8E0` (46 B) as its byte `0215FD44` becomes non-zero or zero - the twin of the display-deny set,
   and the one [the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md)
   section 3.1 names from the `...ctrldenystatus` verbs.
2. If the wanted look `+5` differs from the shown look `+4`, it copies it over and raises the *changing* bit, bit 0 of
   `+7`.
3. It calls the current look's **step callback** (`+0x18`) - or, with none installed, takes the changing bit as the
   answer. A step returns non-zero only when its look has fully left.
4. Only then, and only if the list is not empty, it switches on the shown index and installs the new look.
5. While status display is denied it also zeroes the render record's byte `+0x5E0` and sets the record mode to 0.

Installing a look always clears the changing bit, releases the block's two effect handles (`+8`, `+0xC`), sets the
**record mode** - `00428CD0` (269 B) gives the mode to the record's model instance and to every record attached under
it; the leaf it calls, `00504D20` (7 B, read), is one store, **the model instance's byte `+0xBA`** - and stores a step
callback.

**The mode is a variant index** (added 2026-09-19). `005044D0` (65 B, read whole) takes an entry number `n` and returns,
from a table inside the model instance - base at the instance's `+0x1F8` plus the offset at `+0x21C`, count at the
table's `+0xC`, sixteen-byte entries from its `+0x30` - the address `table + entry[n].offset + mode x entry[n].stride`
(the stride is the word at entry `+2`, the offset the dword at entry `+0xC`): **the mode picks one of several
equal-sized blocks per entry.**The model draw, a 9,695-byte body not read, reads the byte at three sites, and at one of them compares it with
3 and skips a block of commands per draw group. So **Stone is variant 3 of the model's per-entry parameter blocks, and
the flash frames of Doom and HP Critical are variant 2**; what the blocks hold and what the skipped pass draws were not
read.

**How a variant gets bound - `00504D30` (310 B, read whole 2026-09-19).** The same table has a second reader, called
with an instance, an entry number, a variant number and a request block. It refuses when the instance has no table,
when the entry is at or past the table's count, or when **entry or variant is 16 or more**. Each entry has a storage
handle at instance `+0x140 + 4 x entry`, **allocated on first use and sized from the entry's stride word** (a zero
result is put back to -1, which refuses). The pair is keyed by one byte, `entry << 4 | variant`, and the instance has
**twenty binding slots**: key bytes at `+0x180`, binding handles at `+0x194`. A key already present ends the call -
binding is idempotent; otherwise the first free slot (`0xFF`) takes the pair, the request's dword `+4` is pointed at
the entry's storage, and a second routine turns the request into the slot's handle. **When all twenty are taken it
does nothing, and says nothing.** Its one caller is the record-side routine that ensures a character's bindings, not
read; what the two allocator-side routines are was not established either.

| body | anchors |
|---|---|
| `00504D30` variant binder (310 B) | `00504D4B`, `00504D57`, `00504D60`, `00504D6A`, `00504D73`, `00504D7C`, `00504D99`, `00504DA7`, `00504DB3`, `00504DC5`, `00504DCA`, `00504DDD`, `00504DED`, `00504E00`, `00504E16`, `00504E38`, `00504E3C`, `00504E41`, `00504E48` |

The looks:

| index | status | what is installed |
|---:|---|---|
| 0 | Stone | **record mode 3** (every other look sets 0); step `00470AA0` (208 B, read after the rest): a phase that rises once over thirty frames and stays at 1; every frame the render record's byte `+0x5E0` := 2, `+0x5DC` := `1 + 0.3 x pulse(phase / 2)` - 1.0 climbing to 1.3 and holding - `+0x5EC` := 0.4, and mode 3 again. **Stone does not fade out**: when the look changes the step sets mode 0, releases both handles and reports *left* in the same frame. It obeys the hold byte like the tint |
| 1 | Petrify | step `00470780` (798 B): Stone's picture from the third frame, with a dip of the ambient each time the countdown ticks, section 3a |
| 2 | Berserk | `00470660` (280 B) and step `00470EB0`: a red ambient and a negative light from the viewer's side, section 3a |
| 3 | Doom | `00470590` (202 B) and step `00470B70`: a dull red glow that flashes when the countdown ticks, section 3a |
| 4 | Blind | the tint, offset `(-0.5, -0.5, -0.5)` |
| 5, 6, 7, 9, 10 | Poison, Silence, Sap, Disable, Disease | the tint, offset `(-0.2, -0.7, 0.0)` - **one arm of the jump table serves all five** |
| 8 | Oil | the tint's step with offset `(-2, -2, -2)`, and an effect request of its own (`0x0100BE01`, with a second vector `(0, -1, 0)`) in place of the tint's |
| 12 | *no status* | the tint, offset `(1.5, 2.0, 2.0)` - a brightening that no arm of the push selects |
| 13 | HP Critical | `004704C0` (195 B, read): the tint's light request with a different step, `00470230` (448 B): a red flash on a thirty-frame cycle, section 3a |
| 11 | - | nothing |

## 3a. Three more looks, read (added 2026-09-19)

All three are made of the same private status light as the tint (type 6, priority `0xBF`, one character, class 5,
exempt from that character's ambient mode and light scale) and obey the hold byte. They share **two curve tables,
`01F21F40` and `01F22030`**, indexed by a frame counter at block `+6` and filled at start-up (their values were not
read), and one *flash* recipe:

```
light colour    = (a colour) x curve1[frame]           (plus a steady part, for Doom)
record +0x5EC   = 1 - curve2[frame]                    the scale on the world's lights
frames 3..10    : model mode 2, record colour +0x5D0 = (0.84, 0.84, 0.84);   otherwise mode 0 and (1, 1, 1)
frames  0..20   : ambient mode 1 with amount +0x5DC = curve1[frame]          (blend ambient toward the record colour)
```

Frame numbers are multiplied by the frame-rate word `01DFE0B4`.

**HP Critical - step `00470230` (448 B), read whole.** The flash runs on a fixed **thirty-frame cycle** with the colour
`(0.64, 0, -0.32)` - red up, blue down. From frame 21 to the end of the cycle the ambient mode is 0 and **the light
carries the *skip* bit**, so for the last nine frames of every second the character looks normal. The look checks
whether it should leave only when the counter wraps: **it always finishes its beat.**

**Doom - installer `00470590` (202 B) and step `00470B70` (827 B), read whole.** Two states. *Steady:* an envelope rises
at `0.33 x [01DFE0BC]` a frame to 1 (and falls at that rate when the look is leaving; at zero both handles are released
and the step reports *left*); the light is a dim red, `envelope x 0.4 x (0.9, -0.2, -0.2)`; ambient mode 0, light
scale 1.0, model mode 0. **Every steady frame, unless the look is leaving, it asks the unit for its Doom count** - the
unit is reached through the object at the render record's `+0x108`, and the accessor (by role: it answers only for
statuses 2 and 6, Petrify and Doom, and only while the status is set) returns the dword
[the battle-stats field map](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) lists at
`+0xBC + 4 x status` - **and compares it with the value it remembered at block `+0x39`; when the number has changed it
switches to the flash.** *Flash:* twenty-one frames of the recipe above with the colour
`(0.6 x curve1 + 0.4 x envelope) x (0.9, -0.2, -0.2)`; at its end it clears the ambient mode, remembers the new counter
value and returns to steady. **So a Doomed character glows dull red and flashes each time its countdown ticks.**

**Berserk - installer `00470660` (280 B), read whole; its step `00470EB0` was not.** It registers **two** private
lights: the status ambient into handle `+8`, and a directional light (`0x0100BE01`, space mode 1 at request `+6`, scale
exemption only) into handle `+0xC` - the one look that uses both handles.

**Petrify - step `00470780` (798 B), read whole: it already looks like Stone, and it ticks.** Four states at block
`+0x38`:

| state | frames | what it does |
|---|---|---|
| 0, arriving | 6 | ambient mode 2 with amount `+0x5DC = 1 - 0.7 x pulse(t)`, `t` rising by 1/6 a frame - a dip of the ambient to 0.3 and back; model mode 0 and light scale 1.0 for the first three frames, **model mode 3 and light scale 0.4 from the third**. Then it remembers the unit's Petrify count and goes steady |
| 1, steady | - | ambient mode 0, model mode 3, light scale 0.4 - **the same picture as Stone**. Every frame it reads the Petrify count (the accessor Doom uses, with status 2); **a changed, non-zero count starts a tick**. When the look must leave: if Stone's bit is already in the list's mask it releases and reports *left* at once - **Petrify runs into Stone with no flash** - otherwise it goes to state 3 |
| 2, tick | 20 | ambient mode 2 with amount `1 - 0.3 x pulse(t)`, `t` rising by 0.05 a frame; mode 3 and 0.4 throughout; back to steady |
| 3, leaving | 6 | the arrival reversed - mode 3 and 0.4 for three frames, then mode 0 and 1.0 - then release and *left* |

It creates no light of its own: Petrify's look is made entirely of the model mode and the character's two lighting
adjustments.

**Berserk - step `00470EB0` (581 B), read whole: red, and dark from the front.** The tint's phase and envelope, and
with `w = (0.5 + 0.5 p) x envelope`:

```
the status ambient light      colour = ( 2 w,  0,  0 )                    red added
the second, directional light colour = (-3.5 w, -3.5 w, -3.5 w)           light taken away
                              vector = normalise( a point of the character - camera position )
record +0x5EC                        = 1 - (0.85 + 0.15 p) x envelope     the world's lights nearly off
```

The vector is rebuilt every frame from a point the record is asked for (a shared record routine, described by role,
given the code `0x100`; which point that is was not read) and the camera position `02AEDF20`: **a negative light that always comes from the viewer's side**, so the
face the player sees is the darkened one and the red shows round it. **Under control denial the step still re-aims
that light every frame and does nothing else** - the one look whose hold is not a complete standstill.

**The tint.** `004703F0` (198 B) stores the offset at `+0x40`, zeroes the phase and envelope, installs the step
`004700E0`, and creates ~~an effect object~~ **a light** from an `0x50`-byte request, keeping its handle at `+8`.

> **Corrected 2026-09-19, the same night: the "effect objects" of this page are lights.** `003AB960` (506 B; its head
> read) takes a free entry of a **128-entry, `0x70`-stride light pool** (`[02B3F528]`), makes the handle
> `counter << 8 | index` and copies the request to entry `+0x20`; `003ABD00` (26 B) turns a handle back into that
> block. It is the block the light selector of section 4a reads, so the request's bytes have names: `+0` type, `+1`
> priority, `+2` subtype, `+3` / `+4` scope, `+5` and `+7` flags, `+8` target id, `+0x10` colour. **The tint's request
> `0x0100BF06` is therefore an ambient light (type 6) of priority `0xBF`, scoped (`+3` = 1, `+4` = 2) to the one
> character whose id it carries**, with `+7` = `0x80` - *light class 5* - and `+5` = `0x90`: bit 4 exempts it from the
> ambient mode of section 4a, and a value of `0x80` or more exempts it from the per-character scale. The colour the
> step writes every frame is the light's colour: **a status tint is a private ambient light with a negative colour.**
> Oil's request `0x0100BE01` is a type-1 light of priority `0xBE`, same scope and class, carrying the vector
> `(0, -1, 0)` at request `+0x30` and the colour `(-2, -2, -2)`; its byte `+5` is `0x80`, exempt from the scale only.

**The tint's step (`004700E0`, 332 B)** - the arithmetic of section 1. If the hold byte is set it returns at once, reporting *not left*. The
phase `+0x20` advances by `[01DFE0BC] / 30` and wraps at 1. The envelope `+0x24` rises by `0.1 x [01DFE0BC]` a frame
to 1 - or, while the changing bit is up, **falls** at that rate, and at zero the step releases its effect handle,
removes itself and reports that the look has left. With `p` = the pulse table at the phase (`0046FBB0`, 60 B, a
sixty-entry raised cosine at `01F20AA0`: 0 -> 1 at entry 29 -> 0):

```
colour of the effect object  = offset x (0.5 + 0.5 p) x envelope        (alpha 1.0)
render record +0x5EC         = 1 - (0.8 + 0.2 p) x envelope
```

What the renderer does with `+0x5EC` was not read here.

## 4. The second block: two more channels and a flag

Block `+0x70`. Its workers `0051DBF0` (109 B, add) and `0051DDC0` (remove) keep a mask at `+0x10` and derive three
bytes from it:

| byte | value | from |
|---|---|---|
| `+0x19`, channel A wanted | 2 if mask bit 2, else **3 if Invisible**, else `0xFF` | bit 2 has no status arm |
| `+0x31`, channel B wanted | **0 if Immobilize, else 1 if Slow**, else `0xFF` | Immobilize hides Slow |
| `+0x33` | 1 while **Stop** | |

**The update (`0051E3A0`, 362 B)** runs the same *wanted / shown / changing / step callback* protocol as section 3,
once for each channel: channel A installs `0051E0A0` for 2 and `0051DC90` for 3 (Invisible); channel B installs
`0051DE30` for 0 (Immobilize) and `0051E170` for 1 (Slow) - ~~three~~ all four are read in section 4b *(corrected 2026-10-02, OPUS: Immobilize `0051DE30` was read the same night)*. While the Stop flag
is up it calls a render-record routine every frame - *named 2026-09-19 (FABLE): it raises the pose sequencer's
event 0 with choice 0, only-if-changed, which holds the character at that event's resting value and stops the
random blinking; [the pose sequencer](../Model-And-Motion-Formats/the-pose-sequencer.md) §4b*. **While status display is denied the whole update is replaced by a reset**: a record routine with mode 5
and scale 1.0, and the scalar 1.0 to the record's side object at `+0x114`. *The "record routine with mode 5" is the fade-channel
forwarder with channel 5: denial makes an Invisible character fully opaque again.*

## 4b. The second block's looks, read (added 2026-09-19)

~~Three~~ All four of the step bodies were read whole *(corrected 2026-10-02, OPUS: Immobilize's the same night, below)*. They use the block's phase and envelope the way the tint does - a
thirty-frame phase, an envelope that moves `0.1 x [01DFE0BC]` a frame and must reach zero before the step reports
*left* - and the pulse table of section 3.

**Invisible - `0051DC90` (300 B).** It writes **fade channel 5 of the character**
([how a character fades](how-a-character-fades-the-ten-channels.md)) through the forwarder `00428940`, at once:

```
channel 5 = 1 - (0.60 + 0.20 p) x envelope        a pulsing 20 to 40 percent opacity
channel 5 = 1 - (0.88 + 0.08 p) x envelope        when the block's dword +0x14 is non-zero: 4 to 12 percent
```

and sets ~~a two-bit field of the render record~~ two flag bits (17 and 18) and a byte field (bits 19 to 26) of the render record's `+0x304` (`00428AF0`, arguments 1, 1 and the mask byte `0x60`, which lands in bits 24 and 25) *(corrected 2026-10-02, OPUS: `00428AF0`+0x0 clears `0xF801FFFF`, ten bits; `00428AF0`+0xE `movzx eax, r9b` takes the whole byte, unmasked; `00428AF0`+0x1E `shl eax, 0x11`)*. Leaving, it puts
the channel back to 1.0 and clears that field. **Invisibility is an opacity, not a material**; and because fade
selector `0x0B` leaves channel 5 out, anything that asks for `0x0B` - the alpha of effect containers tied to the
character, for one - does not fade with it. What sets the block's `+0x14` was not found in the bodies read.

**Index 2 of the same channel - `0051E0A0` (145 B)** - takes channel 5 to `1 - envelope`: a plain fade to nothing over
ten frames, and back. No status arm of the push selects it.

**Slow - `0051E170` (549 B).** It works on **the character's shadow** - the object behind the render record's handle
`+0x114` is an entry of the shadow-object pool (`02B40528`, 160 x `0xE0`;
[the authored-command ramp channels](../CONTRACT-authored-command-ramp-channels.md), `UQ-191`) - and does nothing
visible when the handle is zero. With `s = (0.5 + 0.3 p) x envelope` it gives the shadow the integer colour
`(128 s, 32 s, 8 s)` and a vector `(1 + q, 1 - q, 1 - q)`, `q` being the pulse times ~~a double constant not converted~~ 0.1
~~here~~ *(answered: see the Immobilize paragraph below - the two double constants are 0.1 and 0.3; 2026-10-02, OPUS)*, and raises a per-record flag through `0051E510`. Leaving, it restores the scalar 1.0, a zero colour and a unit
vector and drops the flag. **Slow is shown on the ground: the character's shadow pulses orange-red.** What the shadow
draw does with that colour and vector was not read here.

**Immobilize - `0051DE30` (621 B), read whole the same night: Slow's twin, redder and stronger.** Same shadow, same
protocol. The colour is `(128 s, 16 s, 4 s)` with `s = (0.7 + 0.3 p) x envelope`; the vector is `(1 + q, 1 - q, 1 - q)`
with `q = 0.3 p` (Slow's `q` is `0.1 p` - the two double constants are 0.1 and 0.3); and - which Slow does not do - it
**raises the shadow's float `+0xC` to `1 + (1.5 + 0.5 p) x envelope`**, 2.5 to 3.0 at full envelope. That float is a
factor of the shadow's gain term in the ramp-channels contract (whose best-fit reading of that term is opacity or
strength), so an Immobilized character stands on a shadow that is red, pulsing, and - if that reading holds - darker.
Leaving restores 1.0, zero colour, the unit vector.

*The setters, read:* `003B6B10` (28 B) stores the shadow's `+0xC` and `003B6B30` (45 B) its three ints at `+0x20`, each
after checking the whole handle against the entry's `+0x10`. *The vector's destination:* both looks hand it to a
graphics-layer routine and then call `0051E510` (110 B, read), which walks the record and every record attached under
it and calls **virtual slot 25 of each piece's render object** (record `+0x6B8`) with 1, or 0 on leaving. What that slot
does with the vector - a colour scale on the model is the natural reading of `(1 + q, 1 - q, 1 - q)` - was not read.

## 4a. Where the three record fields go: they are the character's lighting (added 2026-09-19)

The looks write three fields of the render record - `+0x5DC`, the byte `+0x5E0` and `+0x5EC` - and an image-wide sweep
for those displacements finds **two readers, both in the lighting layer**. (A third match, in the draw-side body
`0045E930`, takes the address of `+0x5E0` of a *different* object - an effect with curve blocks - and is not a reader of
the record.)

**The per-character light gather, `003ABD50` (950 B, read whole).** Called with the render record, an output block and
the character's matrices, it:

1. takes the caller's colour scale, or `(1, 1, 1, 1)` when the caller's flag is zero; clears the `0xE0`-byte output and
   sets its dword `+0xD0` to -1;
2. **stores the record's `+0x5EC` in the global `02B3F518`**, then calls the light selector with the light
   list held in the global `02B3F508` (what fills it was not read), the record and its id. The selector returns how many lights it chose and fills the output's `+0xC0` - the
   ambient term - itself;
3. hands the chosen lights to an ordering routine (called with the bounds 0 and n - 1; a sort by its shape, not read),
   then walks them **in runs that end when the next light's priority byte (`+1`) is lower**: for each light it installs
   one of two matrices (by bits 1 to 3 of the light's byte `+5`), evaluates it by kind - **five kinds, one evaluator
   each** - and keeps it only if the evaluated record's float `+0x1C` is non-zero; a run of two or more that still fits
   under the cap is handed to a second ordering routine;
4. writes the survivors into the output, **six at most**: colours at `+0x60 + 0x10 x i`, and the negated, normalised
   directions as structure-of-arrays - lights 0 to 2 at `+0x00` / `+0x10` / `+0x20`, lights 3 to 5 at `+0x30` / `+0x40` /
   `+0x50`. A direction whose squared length is still 0.5 or less after the normalising call - in effect a zero vector -
   has its middle component set to -1 first. The index of the **last** written light whose `+0x20` is non-zero goes to
   `+0xD0`.

**Two conditions on the scale (added with the correction above).** The ambient evaluator `003ACAA0` (358 B, read
whole) multiplies by `02B3F518` only while the enable byte `02B3F502` is set **and** the light's byte `+5` is below
`0x80`; the selector also clears that enable around every ambient entry of a character's *own* light list. So the
scale dims the world's lights and never the status light itself. (*Checked since for the directional and the point kind -
[how a character is lit](../Character-Rendering/how-a-character-is-lit.md) section 5a; the other three kinds' multiply
sites were found by sweep, not read.*)

**What status display denial really does.** Its latch routine `003E7C70` calls the enable's setter with 0 and ORs
`0x20` into the selector's class filter `02B3F501` (`003ACA80`, 7 B): a light is skipped when its class bits - byte
`+7` shifted right by two - meet the filter. Class 5 is the status lights. **So denial hides a tint by switching its
light off and lifting the dimming, and the looks' steps go on running underneath**; leaving denial restores both.

**`02B3F518` is a multiplier on light colour.** Every one of the five light evaluators, and the ambient evaluator the
selector calls, multiplies its colour by it (rip-relative sweep: fourteen read sites in six bodies and no other kind of
read; besides the gather, one body stores 1.0 there and one small setter writes it). So:

| look | `+0x5EC`, the scale on every light that reaches the character |
|---|---|
| none | 1.0 (a record initialiser stores it) |
| the tint (Blind, Poison, Silence, Sap, Oil, Disable, Disease) | `1 - (0.8 + 0.2 p) x envelope` - **between 0 and 0.2 once the look is fully in**: the world's lights on the character are all but off, and its private status light (exempt from this scale) supplies the pulsing negative colour |
| Stone | 0.4 |

**The byte `+0x5E0` is a mode for the ambient entries, and `+0x5DC` its amount.** In the light selector (`003ACC10`,
2,342 B, *read in part and therefore not anchored here*), an ambient entry that does not carry bit 4 of its byte `+5`
has its colour changed before it is summed: **mode 2 multiplies it by `+0x5DC`** - Stone's 1.0 climbing to 1.3 - and
**mode 1 blends it toward the record's own colour at `+0x5D0` by `+0x5DC`**; any other value leaves it alone. Mode 1 is
what HP Critical's step writes (section 3's table; ~~that step was not read, so the colour it blends toward is not on~~
~~this page~~ *(answered: see section 3a - step `00470230` read whole, record colour `+0x5D0` = (0.84, 0.84, 0.84); 2026-10-02, OPUS)*).

*The whole of the lighting layer these fields feed - which lights reach a character, how ambient is settled, what a
light's request bytes mean - is on its own page: [how a character is lit](../Character-Rendering/how-a-character-is-lit.md).*

## 5. Behaviour a reimplementation must keep

- The look shown is a function of the *set* of statuses, not of the order they were inflicted in.
- A change of look is never a cut: the old look's step must report that it has left, which for the tint takes ten
  frames at 30 fps.
- Five ailments are indistinguishable by colour.
- The colour list and the second block are independent; a Poisoned, Slowed character shows both.
- Control denial freezes the colour look where it is - the step returns before it advances anything, so a look can
  neither pulse nor leave, and a change of look waits. Display denial does not freeze it; it forces record mode 0.

## 6. What is not known

- ~~Petrify's look and Berserk's step~~ (*read; every look of the colour list is now read*), and the four step bodies of the second block ~~- named,~~
  ~~not read. So what Slow, Stop, Immobilize and Invisible *look like* is not on this page.~~ *(answered: see section 4b - all four read; Stop has no step and holds the pose sequencer's event 0 (section 4); 2026-10-02, OPUS)*
- What the model's variant blocks hold (the mode selects among them; section 3), and what pass the model draw skips for variant 3. ~~What the renderer does with `+0x5DC`, `+0x5E0` and `+0x5EC`.~~ *Read
  the same night: they are lighting parameters, section 4a.* The light selector itself - which of the area's lights
  reach which character - was read only in part.
- ~~What the two effect requests (`0x0100BF06`, `0x0100BE01`) create.~~ *Lights; decoded in section 3.* ~~What light kind~~
  ~~1 is (directional, point, spot) was not read.~~ *(answered: see how-a-character-is-lit.md section 5a - kind 1 is a directional light, `003AD540` read whole; 2026-10-02, OPUS)*
- Whether anything selects look 12 or the second block's index 2 from outside the push.
- Nothing here was observed running; "green pulled down" is arithmetic on constants.

## 7. Where each behaviour is in the bytes

| body | what | anchors |
|---|---|---|
| `003E7650` the push (1,566 B) | record walk; status word; set and cleared masks; first test of each chain; the two block updates; stride | `003E7673`, `003E768A`, `003E76F0`, `003E7703`, `003E770C`, `003E7712`, `003E7718`, `003E7C26`, `003E7C42`, `003E7C49` |
| `0046FD00` colour-look update (615 B) | hold byte; wanted against shown; step call; ready and non-empty tests; table jump; Stone arm and mode 3; Blind, shared and Oil vectors; index 12; denial tail | `0046FD38`, `0046FD42`, `0046FD4B`, `0046FD64`, `0046FD72`, `0046FD8F`, `0046FD9A`, `0046FDD4`, `0046FE34`, `0046FE50`, `0046FE59`, `0046FEED`, `0046FF0C`, `0046FF3A` |
| `004703F0` tint installer (198 B) | step stored; offset stored; request word; handles released; effect created | `00470408`, `00470413`, `00470425`, `00470454`, `00470477`, `0047048D`, `0047049B` |
| `004700E0` tint step (332 B) | hold; phase; envelope down and the leaving path; envelope up; pulse; `+0x5EC`; colour | `004700E6`, `00470114`, `0047013A`, `00470166`, `00470184`, `00470192`, `004701AD`, `004701ED`, `004701F7`, `00470215` |
| `00470AA0` Stone step (208 B) | hold; phase to 1; `+0x5E0`; half-phase pulse; `+0x5DC`; `+0x5EC`; mode 3; the leaving path | `00470AA6`, `00470AC3`, `00470AE1`, `00470AF5`, `00470B13`, `00470B1F`, `00470B2D`, `00470B32`, `00470B3E`, `00470B5D` |
| `00470230` HP Critical step (448 B) | hold; cycle end and the leaving test; curve 1 to the light colour; curve 2 to `+0x5EC`; frames 3 to 10; frames below 21; the skip bit; counter | `00470236`, `00470254`, `00470266`, `004702AA`, `004702FF`, `0047030C`, `0047031E`, `00470330`, `0047039F`, `004703AE`, `004703CA`, `004703D7`, `004703DB` |
| `00470780` Petrify step (798 B) | hold; state switch; leaving flash; tick flash and its length; steady: mode, scale, count poll, tick start; the Stone test and the direct release; to state 3; arriving flash; mode switch at frame 3; to steady with the count | `00470786`, `00470797`, `004707C3`, `004707E4`, `0047082A`, `00470870`, `00470898`, `004708D3`, `0047090C`, `00470917`, `00470955`, `00470968`, `00470980`, `00470985`, `004709BB`, `004709C5`, `00470A2C`, `00470A43`, `00470A72`, `00470A89` |
| `00470EB0` Berserk step (581 B) | both lights fetched; hold path: re-aim only; phase; envelope down and leaving; envelope up; pulse; `+0x5EC`; red ambient; negative directional; the point; minus camera; normalise | `00470ED7`, `00470EE2`, `00470EE7`, `00470F01`, `00470F45`, `00470F51`, `00470F8A`, `00470FB6`, `00470FD8`, `00470FF3`, `00471049`, `0047105C`, `00471061`, `0047107B`, `0047108A`, `004710BF` |
| `00470590` Doom installer (202 B) | step stored; state zeroed; request; class byte; create | `004705A8`, `004705AC`, `004705C5`, `004705ED`, `004705EA`, `00470631` |
| `00470B70` Doom step (827 B) | hold; state switch; flash envelope; flash end and the counter re-read; flash colour; `+0x5EC`; frames 3 to 10; ambient mode 1; steady envelope down and the leaving path; steady colour; the counter poll and compare | `00470B76`, `00470B8B`, `00470BA3`, `00470BD1`, `00470BF7`, `00470C0A`, `00470C3F`, `00470CC7`, `00470CD9`, `00470D69`, `00470D95`, `00470DC1`, `00470E13`, `00470E78`, `00470E8B`, `00470E94`, `00470E98` |
| `00470660` Berserk installer (280 B) | step stored; ambient request; directional request; two creates; two handles | `00470685`, `00470689`, `004706C1`, `004706FA`, `00470705`, `0047072C`, `00470734`, `00470744`, `0047074F` |
| `004704C0` HP Critical installer (195 B) | its own step; the tint's request | `004704D8`, `004704DC`, `00470521`, `0047055A` |
| `003ABD50` light gather (950 B) | colour scale default; output cleared; `+0x5EC` to the global; selector call; first sort; matrix choice; kind switch; keep test; run boundary; six-light cap; colour and direction stores; short-direction fix | `003ABDA9`, `003ABDDD`, `003ABDF3`, `003ABE0F`, `003ABE29`, `003ABE48`, `003ABE80`, `003ABEEF`, `003ABF54`, `003ABF76`, `003ABF90`, `003ABFDC`, `003ABFFA`, `003AC025`, `003AC043`, `003AC097` |
| `0051DC90` Invisible step (300 B) | phase; envelope down and the leaving path; channel back to 1.0; field cleared; envelope up; the variant test; the two opacity formulas; channel write; field set | `0051DC96`, `0051DCDA`, `0051DCF5`, `0051DD0A`, `0051DD1B`, `0051DD30`, `0051DD4B`, `0051DD55`, `0051DD6C`, `0051DD7C`, `0051DD96`, `0051DDAA` |
| `0051E0A0` fade-to-nothing step (145 B) | changing test; envelope down; leaving; envelope up; channel write | `0051E0A4`, `0051E0C2`, `0051E0EE`, `0051E0FD`, `0051E113`, `0051E125` |
| `0051E170` Slow step (549 B) | phase; envelope down and the leaving path; restore scalar, colour, vector, flag; envelope up; handle test; pulse to colour; pulse to vector; flag | `0051E18A`, `0051E1C9`, `0051E1EC`, `0051E207`, `0051E21B`, `0051E26E`, `0051E27C`, `0051E28B`, `0051E2A5`, `0051E2B7`, `0051E319`, `0051E365`, `0051E376` |
| `0051DE30` Immobilize step (621 B) | phase; envelope down and the leaving path; restores; envelope up; handle test; gain; colour; shadow colour store; shadow gain store; vector; piece walk | `0051DE4D`, `0051DE8C`, `0051DEAF`, `0051DECA`, `0051DEDE`, `0051DF31`, `0051DF3F`, `0051DF4E`, `0051DF68`, `0051DF94`, `0051DFB7`, `0051E007`, `0051E019`, `0051E03C`, `0051E065`, `0051E076` |
| `00428CD0` record mode (269 B) | own instance; attached record; the two subtree walks | `00428D1F`, `00428D3C`, `00428D82`, `00428D9D`, `00428DB8` |
| `0051E3A0` second block update (362 B) | denial test; channel A; channel B; Stop call; reset | `0051E3CF`, `0051E3DB`, `0051E3FA`, `0051E40E`, `0051E42A`, `0051E45F`, `0051E480`, `0051E494`, `0051E4BD` |

## 8. Related

- [The thirty-two statuses](../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md) - the bits.
- [The rig of seventeen controllers](the-rig-of-seventeen-controllers.md) - the three status motions, and the bit-to-arm
  table.
- [How a position becomes a single number](../Position-To-Scalar/how-a-position-becomes-a-single-number.md) section 12 -
  the display-deny latch.

## Cross-subsystem neighbours

**World / area / field - SERVICE.** `World_UpdateSimulationTick` (`00314020`), filed under that layer, calls the push once
a simulation tick. The tick owns *when* the statuses are looked at; this page owns what is done with them.

**Status / battle unit - SHARED RECORD.** The push reads each unit's two status dwords through a unit accessor
described here by role. What a status *does* belongs to the status pages; this page owns only what it looks like.

**Shared helpers - by role.** The unit accessor, the light release routine, the model
instance resolver and the hierarchy walker are described by role and not named, because naming a shared leaf imports
every one of its callers.

**Resource - SERVICE.** `003E55B0` on this page — a callee of the record-mode body `00428CD0` — calls a body in that
layer's census. The crossing is that call, not a shared responsibility. MECHANICAL accounting (SWE2-EC7, 2026-09-19).

**Core runtime scheduling - CLIENT.** `003E5D60`, one of the two fade arms the forwarder `00428940` dispatches
into, calls `001EDE70` in that layer's census. The arm consults the scheduler; it does not share ownership of it.
MECHANICAL accounting (SWE2-EC7, 2026-09-19).

**Audio / Party - MECHANICAL (SWE2-EC7, 2026-09-20).** `00537410` — cited in the `0051E510` section only to name
the `+0x284`-gated record family it reads — calls `00361CF0` (Audio) and `003590D0` (Party). The edges belong to
the ownerless evaluator's own page; the mention here is a record-family cross-reference, not a claim.

**Movement - CLIENT (SWE2-EC7, batch 166).** `001F1590` — a body this page's EC7-109 section measures — is
reached from Movement's `003ED190`/`003ED3F0`, and batch-166's `003E7500` (the `02B59D80` slot init) is reached
from `002E28E0` on that layer; movement bodies consult the status-show machinery, not a shared responsibility.

## SWE2-EC7-43 update (2026-09-19) - `00470660`

`00470660` (280 B) is the Berserk status-show sibling - `00470EB0`/`01F44830`, `003AB960`/`003ABCA0`/`00428CD0`/`00808C40`/`00861EC0`. Interior anchor `004706A7` (a `003AB960` call).

## SWE2-EC7-44 update (2026-09-19) - `00428CD0`

`00428CD0` (269 B) is the record-mode body - `word[rcx]` index with -1 short-circuit, `003E55B0`/`00426220`/`0042EF90`/`00504D20`/`00808C40`. Interior anchor `00428D1F` (a `003E55B0` call).

## SWE2-EC7-52 update (2026-09-19) - `0045E930`

`0045E930` (2053 B) is the +0x5E0 status-effect body - `byte[rcx]` gate publishes `[rcx+0x230]`/`[+0x240]` quats to `02AE8E70`/`02AE8E80` plus `1.0f` to `02AE8E7C`, `004314E0`/`004309C0` calls. Interior anchor `0045E9AF` (a `004314E0` call).

## SWE2-EC7-68 update (2026-09-19) - `0046FBB0` status-float table sampler

`0046FBB0` (60 B) is the scalar-to-table sampler every status-arm
reader (`004700E0`/`00470AA0`/`00470EB0`/`0051DC90`/`0051DE30`/
`0051E170`) calls: `dword[01F20538]` is the table count (60),
`cvtsi2ss(count-1) * xmm0` truncates to `eax`, clamps into
`[0, count-1]` (`cmovns` for the low side, `count-1` reload for the
high), and the return is `float[01F20AA0 + eax*4]` - a unit-float
to one of 60 tabled status weights. Call-free. Interior anchor
`0046FBE6` (the table load). *(Qualified 2026-09-29, OPUS, on SWE2-AUDIT-SPEC's [batch-6 review](../../_index/candidates/auditspec-review-opus-batch6-0929/REVIEW.md) section 3: the count is 60 in the image, the `FrameLimit=30` state. Under `FrameLimit=60`, `001EDDC0` calls `0033F020`, whose first callee `0046FBF0` doubles `01F20538` and `01F2053C` (`add eax, eax`, `0046FC29`..`0046FC3F`) and has `0033E5E0` rewrite `01F20AA0` and `01F20C80` in place to 120 entries; each has exactly 120 floats of room. The index is `t * (count - 1)`, so `t * 59` or `t * 119`.)*

## SWE2-EC7-69 update (2026-09-19) - `003ABD00` handle-to-record measured

`003ABD00` (26 B) measured - **the page's handle-decode is exact**: it
indexes `[02B3F528] + (ecx & 0xFF) * 0x70` and returns `record + 0x20` only
when the record's leading dword echoes the full handle (`dword[rax] ==
ecx`); a stale or forged handle returns NULL. Call-free - the index byte is
the slot and the echo-check is the generation counter.
Interior anchor `003ABD0E` (the `cmp dword[rax], ecx` echo-check).

## SWE2-EC7-70 update (2026-09-19) - `00428940` fade forwarder measured

`00428940` (20 B) measured - the forwarder the page names on the
how-a-character-fades path: `r9d <= 1` tails `003E5D00`, `rcx != 0` tails
`003E5D60`, otherwise returns - the channel-count dispatch into the two
fade arms.
Interior anchor `00428944` (the `jle 003E5D00` arm select).

## SWE2-EC7-72 update (2026-09-19) - `00428AF0` two-bit field setter measured

`00428AF0` (50 B) measured - the page's "sets a two-bit field" claim is
exact and slightly wider: `+0x304` is masked `0xF801FFFF`, then
`((r9b << 1 | r8 & 1) << 1 | edx & 1) << 0x11` is folded in - three
flag bits at `+0x304`[17..19] - and `+0x294` gets `0x4000000`.
Interior anchor `00428B0E` (the `shl eax, 0x11` fold).

## SWE2-EC7-73 update (2026-09-19) - `003B6B30` conditional record copy measured

`003B6B30` (45 B) is the `02B40528`-table conditional copy: `r9 =
02B40528 + cl * 0xE0`, and only when `dword[r9+0x10] == ecx` it copies
twelve bytes `[rdx]`/`[rdx+4]`/`[rdx+8]` into `r9+0x20`/`+0x24`/`+0x28`
- a generation-checked field commit.
Interior anchor `003B6B4A` (the first `+0x20` store).

## SWE2-EC7-82 update (2026-09-20) - `0051E510` record-tree walk measured

`0051E510` (110 B) is the recursive traversal the status callers
drive: `cx` indexes `022C6F28 + cx*0x740` (the same `+0x284`-gated
record family `00537410` reads), a live record runs
`0017F240([rbx+0x6B8], edx)`, then `word[+8]` recurses and
`word[+0xA]` iterates siblings - the `-1`-terminated child/sibling
tree walk.
Interior anchor `0051E54E` (the `0017F240` per-node call).

## SWE2-EC7-90 update (2026-09-20) - `003AE9C0` keyed quicksort measured

`003AE9C0` (499 B) is the sort the status callers run over a
pointer array: a recursive quicksort on the `+0x1C` float key of
each pointed record, partitioning around the
`(lo + hi) >> 1`-rounded pivot and falling to an unrolled
insertion pass under span 10 - the ordering `+0x1C` carries.
Interior anchor `003AEA81` (the recursive call).

## SWE2-EC7-109 update (2026-09-20) - `001F1600` and `001F1590` measured

`001F1600` (148 B) is the lazy
`01F82EA8` store `0051DE30` and
`0051E170` run: the singleton
allocates once (`0xB08` bytes via
`00210EC0`, constructed by
`001EF2D0`), then the four
floats at `rcx` land verbatim at
`02CB8390`..`02CB839C` - the
shared vec4 the status display
reads back.
Interior anchor `001F1657` (the
first `02CB8390` store).

`001F1590` (99 B) is the vec3
submit `003ED190` and
`003ED3F0` run on the same
`01F82EA8` singleton: after the
identical lazy-allocate, the
three floats at `rcx` stage on
the stack and
`001F08A0(obj, &vec3, 0)`
consumes them - the position
hand-off the map-ctrl pack
drives.
Interior anchor `001F15E9` (the
`001F08A0` call).

Mechanical neighbours introduced by
this section's citations: `001F1590`
carries Movement caller fan-in
(`003ED190`, `003ED3F0`, 2 edges) -
the map-ctrl pack reaches the same
singleton. Those are edges of the
helper, not of the status display -
noted so the audit accounts for
them.

## SWE2-EC7-110 update (2026-09-20) - `001EF2D0` measured

`001EF2D0` (462 B) is the
`01F82EA8` singleton
constructor behind the
`001F1600` / `001F1590`
vec4-store / vec3-submit pair -
the same function `001F0810`
and `001F0850` reach for their
parameter block. `byte[rcx]`
latches 1, `+8`..`+0x40` and
`+0xD8`/`+0xEC`/`+0xF4` zero,
`qword[+0x18]` and `+0x30`
latch `0xFF`, `+0x138` arms 4,
and `00808FE4(rcx + 0x148,
0xD8, 8, 001EF280)` builds an
8-element sub-object array with
`001EF280` as the element
constructor and `001EF4A0`
staged at `[rsp + 0x20]`. The
defaults that follow are the
weather/display block:
`+0x808`/`+0x80C`/`+0x810` =
5.0/10.0/30.0, `+0x828`/`+0x830`
= 20.0/5.0, `+0x844`/`+0x848`/
`+0xB00`/`+0xB04` = `0x400`,
`+0x86C` = 1.0, `+0x870`/
`+0x874`/`+0x878` =
`0x3C03126F`/`0x3C83126F`/
`0x3D0F5C29`, `+0x890`/`+0x894`
= 7/3, `+0x898` = `0x3951B717`,
`+0x8A0`/`+0x8B0`/`+0x8B4` =
1/1/3, `+0x8A4` = 0.1, `+0x140`/
`+0x144` = 0.6/0.7, `+0x13C` =
3, `+0x130`/`+0x134` = 6.
Interior anchor `001EF393` (the
`+0x870` float default).

`003E7500` (149 B) is the `02B59D80` `0x150`-row init this page's `003E7650` walk consumes (the script-names page lists it as that table's slot init): row `ecx*0x150` gets `word[+0] = 1`, `dword[+4] = edx`, `dword[+8] = 0`; a non-`-1` `edx` also writes itself into the `022C6F28` row's `dword[+0x6A4]` backlink (live-gated on `+0x284`); `00861EC0` zeroes `0x80` bytes at `+0xC0`, then `004700C0(rbx+0x20, edx)` and `0051E140(rbx+0x70, edx)` init the two sub-records.

Interior anchor `003E7570` (function `003E7500`).

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives, and the appended notes check out

**Attack.** Section 7's sizes, section 3's list rule and latch, section 4a's gather, and three appended SWE2-EC7 notes
became checks. The latch's writer census ran on both instruments. Script:
`Tools/analysis-kit/gfz-scripts/falsify_status_look.py`, output `falsify_status_look.out`, image `73461d08…`, 0 BROKEN,
exit 0. The per-status arms' arithmetic is carried.

| # | Clause attacked | Result |
|---|---|---|
| H0 | section 7 and the notes' sizes | **survives**: all twenty-six |
| H1 | section 3 | **survives**: both list workers scan bits 0..13 upward and store the first set index in `+5`, or `0xFF` (`cmove`): fourteen entries, lowest index wins |
| H2 | section 3 (the control-deny latch) | **survives**: `02B59D70` has one writer, `003E7CC0` (7 B), on both instruments; `002EA8E0` reads `0215FD44` and reaches it |
| H3 | the EC7-68 note | **survives**: `0046FBB0` reads the dword count `01F20538` (60) and the table `01F20AA0` |
| H4 | the EC7-69 note | **survives**: `[02B3F528] + (ecx & 0xFF) × 0x70`, the echo compare, `+0x20` returned |
| H5 | the EC7-70 note | **survives**: `jle 003E5D00` on `r9d <= 1`, `jne 003E5D60` when `rcx != 0` |
| H6 | section 4a | **survives**: the gather copies `+0x5EC` to `02B3F518` and compares against the six-light cap |

No correction.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-how-a-status-shows-on-a-character-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001EF280` | 65 B | calls a 182-byte helper (`rcx + 8`), stores the address `00902ED8` at qword `+0x0` of `rcx` and the dword `0x3F800000` at `+0xC8` and `+0xD0`, calls a 202-byte helper (`rcx`) and returns `rcx` | `001EF28D`, `001EF299`, `001EF2A6`, `001EF2A9`, `001EF2B3` |
