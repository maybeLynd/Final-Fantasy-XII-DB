---
system: The rig - a character's seventeen procedural controllers, and who switches each one
category: 17-Presentation-Rendering
status: DOCUMENTED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the two controller switches 003E1350 / 003E1610 read (the first whole, its jump table decoded from the image; the
    second by its seventeen arms); the per-frame update 003E00C0 read for its order of calls and the flag each apply call
    is gated on; the timed-state countdown 0042EE90, the three verb chains down to the record setters, one record-to-rig
    wrapper and eight arms of the status presentation push read whole; the status push's bit-to-arm map extracted from
    its body by script; the controllers' small enable / disable leaves and two update bodies read whole; verbs joined
    through scriptvm-verb-table.tsv and counted in the 1,114 decompiled us scripts
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-rig-controllers-falsification-pass-1
  note: written by FABLE; static throughout. Nine of the seventeen controllers are named from what switches them; what
    the large update bodies compute was not read, and the page says so per row; pending first review
---

# The rig: a character's seventeen procedural controllers

A character's pose is not only its animation. After the motion is sampled, a small set of **procedural controllers**
adds to it: the head turns to look at someone, the mouth flaps while a line is spoken, the head nods, cloth sways, a
floating character bobs. This page is the table of those controllers - the *rig* - and, for each one that could be
named, **the thing in the game that switches it on**.

[The staged look command](the-staged-look-command.md) section 4a met the rig first, from its reset routine, and could
name four of its slots. This page names nine *(scope named 2026-10-02, OPUS: nine by this road; section 2's table now describes fifteen of the seventeen, the rest from their bodies in sections 3a and 5 - only slot 8 is unnamed and slot 4 empty)*, by a different road: not by reading what each controller computes, but by
following **who enables it**.

## 1. What the player sees, and how much of it there is

Counted in the shipped `us` scripts ([rig_verbs_census.py](members/rig_verbs_census.py),
[rig-verbs-census.tsv](members/rig-verbs-census.tsv); 55,891 calls, the parsed count equal to a plain substring count):

| verb | what it is | calls | scripts |
|---|---|---:|---:|
| `setkutipakustatus(on)` | *kuchi-paku*, the lip flap of a speaking character | 28,035 | 354 |
| `setunazukistatus(on)` | *unazuki*, the nod | 26,389 | 347 |
| `setkubifuristatus(on)` | *kubi-furi*, the head shake | 1,179 | 164 |
| `setkutipakustatus_4a2(on, frames)` | the lip flap, switched off again by a timer | 160 | 22 |
| `setunazukistatus_4a3(on, frames)` | the nod, timed | 122 | 20 |
| `setkubifuristatus_4a4(on, frames)` | the head shake, timed | 6 | 3 |

**These three controllers are most of what a talking character in this game does with its head**: a third of the script
corpus switches the lip flap and the nod on and off around its message windows, about fourteen thousand times each way.
The timed forms are rare; their commonest durations are 150, 210 and 90 frames.

## 2. The table

The rig hangs at `+0x94` of a character's resource entry (the look-command page, section 4a). Its first seventeen
dwords are encoded pointers, one per controller, resolved each time they are used. **Controller *n* is the dword at
`+4n`.**

*Where the rig comes from (added 2026-09-26, (FABLE, Claude Opus 5.5)):*
- **The rig is authored data: it is section 2 of the model's `@FCP` block.** It is copied verbatim into the tail of
  the `@FTR` allocation, at the resource entry's `+0x94` ([the FCP block](../Model-And-Motion-Formats/fcp-character-parameter-block.md),
  `UQ-220`).
- **Each slot starts as a byte offset into the section.** At load, the rig's slot initialiser turns each populated
  slot into the encoded pointer this table describes, calling that controller's own init on it. It initialises
  slots 0–3 and 5–16.
- **Slot 4 is authored in 52 files** (every `chara`, 24 `npc`, 11 `monster`), yet nothing initialises it.
- **The format has two more slots, 17 and 18**, at `+0x44` and `+0x48`. They are empty in all 1,066 files.
- Control: [`uq220_section2_rig.py`](../../_index/candidates/uq220-section2-rig/uq220_section2_rig.py).

| n | rig offset | what it is | how it was named |
|---:|---|---|---|
| 0 | `+0x00` | **sway** - the per-model oscillators that keep cloth, hair and hanging gear moving | [the per-model oscillator subsystem](../Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md): the *skeleton-side record* that page is handed **is this rig**; its `+0x5E`, `+0x60` and `+0x63` are rig fields |
| 1 | `+0x04` | **bone physics** | the look-command page: one of the two slots `denybonephysical` restarts |
| 2 | `+0x08` | **the look controller** | the look-command page, section 3 |
| 3 | `+0x0C` | **the Confuse motion** - on while the character is Confused and not Asleep | the status push, section 4 |
| 4 | `+0x10` | *nothing* - neither switch has an arm for it | section 3 |
| 5 | `+0x14` | **an eased turn of a set of bones about an axis, which the character's shadow is made to follow** - not named further | its small per-frame body, section 3a |
| 6 | `+0x18` | **the Float bob** | the status push, section 4; its update read, section 5 |
| 7 | `+0x1C` | **the Immobilize motion** | the status push, section 4 |
| 8 | `+0x20` | not named | - |
| 9 | `+0x24` | **the lip flap** | `setkutipakustatus`, section 3 |
| 10 | `+0x28` | **the eyes** | the look-command page (request bits 27 to 29; the `eyemove` verbs); record flag bit 8, section 3 |
| 11 | `+0x2C` | **rotators** - bones spun at a ramped speed | its update read, and authored command `0x13`, section 3a |
| 12 | `+0x30` | **the hit flinch** - a two-component offset turned by the character's heading; its update read, section 5 | the HP write's alive events `0x2005` / `0x2006`, section 3a |
| 13 | `+0x34` | **the nod** | `setunazukistatus`, section 3 |
| 14 | `+0x38` | **bone physics**, the second slot | the look-command page |
| 15 | `+0x3C` | **the head shake** | `setkubifuristatus`, section 3 |
| 16 | `+0x40` | **the body shake** | `setbodyshake`, section 3a |

## 3. The two switches, and the record flags in front of them

`003E1350(rig, n)` (629 B) **switches controller *n* off** and `003E1610(rig, n)` **switches it on**. Both reject
`n > 16`, jump through a seventeen-entry table, resolve the rig's dword `+4n`, return if it is null, and tail-jump to
that controller's own small *off* or *on* routine. The off table, decoded from the image, sends index 4 straight to the
exit, and the on switch has no arm that touches `+0x10` either - **the rig has room for a fifth controller that this
build does not have**.

A script does not call the switches. It sets a bit in the character's **render record**, and the record's dirty-state
pass carries it over:

| record `+0x304` | dirty bit in `+0x290` | controller | set by |
|---|---|---:|---|
| bit 6 | bit 13 | 9 lip flap | `setkutipakustatus`: handler `00352370` -> service `002E8570` (110 B); timed: `00352B90` -> `002E85E0` -> `002EDF30` (89 B) |
| bit 7 | bit 14 | 13 nod | `setunazukistatus`: `003528A0` -> `002E8B60` -> `002EE0D0` (91 B); timed: `00352F20` -> `002E8B80` -> `002EE130` |
| bit 15 | bit 15 | 15 head shake | `setkubifuristatus`: `0034F430` -> `002ED300` -> `002EDE70` (91 B); timed: `0034F9B0` -> `002ED320` -> `002EDED0` |
| bit 8 | - | 10 eyes | not traced here |

Each setter finds the record from the actor (`+0xC0` -> record index -> the `0x740`-stride array), refuses a free record,
sets or clears the flag bit, raises the dirty bit, and stores the timer: **the plain forms zero it, the timed forms store
`frames / [01DFE0BC]`** in `+0x640` (lip flap), `+0x644` (nod) or `+0x648` (head shake).

The dirty-state pass then calls one wrapper per flag - `0042DD90` (186 B, read whole) for the lip flap, and three of the
same shape for bits 7, 8 and 15 - which resolves the record's resource entry, takes its rig from `+0x94`, and calls the on
switch if the flag bit is set and the off switch if it is clear.

**Who runs the countdown (added 2026-09-19; read whole).** `00428F80` (82 B) is a system phase: it walks the
**active-record list** - head index at the record system's `+0x48800`, next at each record's word `+4`, -1 ends it -
and calls the countdown below on every record in it. And the rig's neighbour in the resource entry: `00421D20`
(70 B) resolves a record's **bone array** - the record's resource entry (owner `+0x10`, index `+0x18`), then the
encoded pointer at entry **`+0x84`**, sixteen bytes before the rig's `+0x94`; it returns null when the record has no
entry.

**The countdown.** `CharacterRenderRecord_UpdateTimedPresentationStates` (`0042EE90`, 254 B) runs unless bit 1 of the
record's `+0x290` is up. For each of the three timers, if its bit of the record's byte `+0x40B` is up (bits 5, 6 and 7; ~~what raises them was~~
~~not read~~ *(answered: see the SWE2-EC7-83 section below - `00429C40`, `0042BBB0` and `00429B40` copy `+0x304` bits 6, 7 and 15 into them; 2026-10-02, OPUS)*) and the timer is non-zero, it subtracts `[01DFE0BC]`; when the timer reaches zero or below it
**clears the flag bit, zeroes the timer and calls the same wrapper-caller the dirty pass uses** - so a timed lip flap
ends exactly as `setkutipakustatus(0)` would end it. A timer of zero is never counted, which is what makes the plain
form permanent.

## 3a. Three more controllers, named the same way (added 2026-09-19)

**Controller 16 is the body shake - the script verb `setbodyshake(amount)` (`0495`).** Its service reaches the record
setter `002EDDC0` (95 B, read whole): a non-zero amount sets **bit 16 of `+0x304`**, stores the amount at the record's
`+0x4BC` and raises dirty bit 16 of `+0x290`; zero clears the flag bit. The dirty pass's wrapper `0042BDE0` (230 B, read
whole) is the lip-flap wrapper with one more step - before switching controller 16 on it copies `+0x4BC` into the
controller's `+0x38`. *This is the row the table above left as "its enable copies the record's `+0x4BC`".*

**Controller 12 is the hit flinch.** Section 5 read its update - an eight-frame pair of curves turned by the
character's heading into a two-component offset. Its one enabler is the record's event handler `00427320` (1,315 B;
only the two windows round the enables were read), which switches it on for **the HP write's alive events**
([the HP write](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)): on `0x2005` - when the
event brings an argument record whose byte `+1` is zero - unless the record's current motion word `+0xCC` is `0x2009`
or `0x2031`, or is `0x2001` with `+0x2A0` equal to 0 or 14; and on
`0x2006` - the knockback variant - when the motion class of `+0xCC` is 3, through the record's own resource entry.
**A character that is hit and survives is shoved for eight frames.**

**Controller 11 is a list of rotators - update `00518F50` (418 B), read whole.** The controller holds a count and an
array of `0x60`-byte entries. For each entry with a non-zero enable dword: while a frame counter is non-zero it is
decremented and an acceleration is added to the entry's angular speed (on alternate counts only while the engine's
half-rate predicate is true); the angle advances by `speed x [01DFE0BC]` and is wrapped at plus or minus two pi; and
the engine's sine table turns the angle into **a two-by-two rotation** stored in the entry. *Bones that spin, at a speed
that can be ramped.* Two things switch it, neither a script verb: **authored presentation command `0x13`**
([the authored command handlers](../Authored-Commands/the-authored-presentation-command-handlers.md)) stages a request
on the record - flags at `+0x3F4`, a piece selector at `+0x3F5`, a target word at `+0x3F6` - which the wrapper
`0042BED0` (1,163 B; its first third read) applies: **target 1 switches controller 11 by the flags' bit 0, target 2 the
lip flap, target 4 the nod**, the last two through a rig routine that takes the on / off value. So a scene's authored
stream can make one piece of a character talk or nod without a script verb. The other switch is a site in the
event-effect interpreter. **What ramps them is authored command `0x24`** *(added 2026-09-20, FABLE)*: its handler calls
`003DFE70(rig, index, target, frames)` (171 B, read whole), which writes the entry's frame counter and the
acceleration `(target - speed) / frames`, or the speed itself when the length is 0 - 1,493 authored, in monsters' and
summons' blocks, 185 of them with a target of 0.0, a stop
([the authored command handlers](../Authored-Commands/the-authored-presentation-command-handlers.md), row `0x24`). What
the rotators are attached to in shipped models was not looked up.

**Controller 5, from its small half.** The rig's frame calls two bodies for slot `+0x14`. Of the 958-byte update only
the head was read: each entry has a frame counter, and while it runs a weight is taken from the engine's ease table
and scaled and offset by entry constants; the weight times a base angle, about **the entry's own axis**, is built into
a rotation through the sine table. The second body, `0051A890` (140 B, read whole), runs when bit 1 of the
controller's byte `+0x17` is set, the character has a shadow (record `+0x114`) and the controller has entries: it
stores **minus (the first entry's angle x its weight) into the shadow object's `+0xBC`** - the term
[the ramp-channels contract](../CONTRACT-authored-command-ramp-channels.md) shows being added to the shadow's rotation -
and writes into **the look controller's byte `+7`** whether the controller's dword `+4` is non-zero. The rig's frame
zeroes that shadow term at its start every frame. *So whatever turns the bones also turns the shadow back under them,
and the look controller is told.* Nothing found switches it: by raw call and conditional-jump sweeps its on-routine is
reached only from the rig's rebind and the generic on-switch, and none of that switch's fifteen call sites passes 5.

**Switching the look controller off is not a snap.** `RelationLook_BeginNeutralReturn` (`00513150`, 108 B, read whole),
the *off* routine of controller 2, does nothing if the controller's mode nibble is already clear; otherwise it clears
the mode, zeroes a progress float, sets the step to `[01DFE0BC] / duration` (the duration is the controller's `+0x18`;
zero means one step), and **remembers the current two angles as the start of the return**.

## 4. The status push: three controllers belong to status ailments

`003E7650` (1,566 B) walks the characters' presentation-parameter records. For each it fetches the unit's status word -
the OR of the two status dwords of the unit's stats record, the thirty-two bits of
[the thirty-two statuses](../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md) - compares it with the word it
saw last, and stores **the bits that were cleared at `+0x144` and the bits that were set at `+0x140`**. Then it runs two
chains of ~~thirty-one~~ thirty-two tests *(corrected 2026-10-02, OPUS: bit 31 too, at `003E7650`+0x318 and +0x580)*, one call per changed bit. [The world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
lists the forty-four arms by their shape; extracted from the body by script, **the index of an arm is the status bit**:

| bit | status | cleared -> | set -> | | bit | status | cleared -> | set -> |
|---:|---|---|---|---|---:|---|---|---|
| 0 | KO | `0051E780` | `0051E790` | | 13 | Disable | `0051E6C0` | `0051E6E0` |
| 1 | Stone | `0051EAE0` | `0051EB40` | | 14 | Immobilize | `0051E700` | `0051E740` |
| 2 | Petrify | `0051E940` | `0051E960` | | 15 | Slow | `0051EAA0` | `0051EAC0` |
| 3 | Stop | `0051EBA0` | `0051EC10` | | 16 | Disease | `0051E880` | `0051E8A0` |
| 4 | Sleep | `0051E9C0` | `0051EA10` | | 24 | Invisible | `0051E5E0` | `0051E600` |
| 5 | Confuse | `0051E620` | `0051E670` | | 26 | Float | `0051E800` | `0051E840` |
| 6 | Doom | `0051EC90` | `0051ECB0` | | 27 | Berserk | `0051ECD0` | `0051ECF0` |
| 7 | Blind | `0051E580` | `0051E5A0` | | 28 | Bubble | `0051E5C0` | `0051E5D0` |
| 8 | Poison | `0051E900` | `0051E920` | | 29 | HP Critical | `0051E7C0` | `0051E7E0` |
| 9 | Silence | `0051E980` | `0051E9A0` | | | | | |
| 10 | Sap | `0051EA60` | `0051EA80` | | | | | |
| 11 | Oil | `0051E8C0` | `0051E8E0` | | | | | |

**Bits 12, 17 to 23, 25 and 30 - Reverse, Lure, Protect, Shell, Haste, Bravery, Faith, Reflect, Regen and Libra - call an
empty stub in both chains**: those ten statuses change nothing on the body through this push. ~~Bit 31 is not tested.~~ Bit 31 is tested: cleared calls `0051E7A0`, which stores 0 to the record's `+0x13C`, and set calls `0051E7B0`, which stores 1 *(corrected 2026-10-02, OPUS: `003E7650`+0x318 `cmp dword ptr [rbx + 0x144], 0x80000000` / `jb`, +0x580 the same on `+0x140`; so 44 non-empty arms, the world tick's count)*.

Eight of the arms were read whole, because they reach the rig:

- **Float (26).** Set: the record's `+0x128` := 1 and **controller 6 on**. Cleared: `+0x128` := 0, controller 6 off.
- **Immobilize (14).** Set: `+0xF8` := 1, the parameter block at `+0x70` is given index 0 through its *set* worker, and
  **controller 7 on**. Cleared: the mirror image.
- **Confuse (5) and Sleep (4) share controller 3.** The record keeps a Sleep flag at `+0xD0` and a Confuse flag at
  `+0xD4`. Confuse set: flag := 1, **controller 3 on unless the Sleep flag is up**. Confuse cleared: flag := 0,
  controller 3 off. Sleep set: flag := 1, controller 3 off *if the Confuse flag is up*. Sleep cleared: flag := 0,
  controller 3 back on if the Confuse flag is up. **So a Confused character that falls asleep stops its Confuse motion
  and resumes it on waking.** All four also tell the look controller: bit 1 of its byte `+0x1C` is *asleep*, bit 2 is
  *confused*.

What the other thirty-six arms push is on its own page now:
[how a status shows on a character](how-a-status-shows-on-a-character.md) - a priority list of colour looks, and a second
block for Immobilize, Slow, Invisible and Stop.

## 5. The per-frame update, and two controllers read

`CharacterRender_UpdateCombatLookAndAuxControllers` (`003E00C0`, 1,631 B) is the rig's frame. Sway runs first, with the
rig's flag byte `+0x63` ORed with a global override (`02B59D60` - never written on PC, so always 0; the
[oscillator page](../Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md) section 6b), and **the rest of the frame is skipped whenever that OR is
non-zero**. Otherwise the look controller is fed, the additive bone matrices are reset, and the controllers are *solved*
in this order: 10, 8, 1, 2, 9, 11, 13, 15, 14, 5 (two calls), 16, 6, 7, 12, 3, 16 again. Then each is *applied* to the
bones, each behind its own has-output test: 11, 10, 2 (`RelationLook_ApplyBoneMatrices`), 9, 13, 15, 8, 1, 14, 5, 12, 7, 3,
6 (the Float bob's apply `004717E0`, added 2026-09-29 - the list above had stopped at 3).
**The nod (13) and the Confuse motion (3) are applied by the same routine**, and so are controller 12 and the Immobilize
motion (7). The look apply also needs bit 1 of the rig's byte `+0x5F`. ~~**The last two applies - Immobilize and Confuse,
the two status motions - are both skipped**~~ **Corrected 2026-09-29 (FABLE, GI-12): the last three applies - Immobilize,
Confuse and the Float bob (`004717E0` at `003E070A`, behind the bob's running byte `+3`) - are all skipped while the
global `02B59D68` is non-zero** (`003E0680`; slot-by-slot map and regression in the oscillator page's section 6b,
`oscillator_gi12.py` check C1): that is the dword the
status-error *display-deny* latch writes, and nothing else writes it
([how a position becomes a single number](../Position-To-Scalar/how-a-position-becomes-a-single-number.md), section 12).

**The Float bob (controller 6), read whole.** On (`004718D0`, 31 B): if off, sets the active byte `+0` and the running
byte `+3` and remaps the attack index `+2` through a table so that a bob interrupted while settling rises from where it
was. Off (`00471640`, 27 B): clears the active byte and remaps `+2` the other way. Update (`004716A0`, 290 B): while
active, the envelope `+0x10` rises by `0.125 x [01DFE0BC]` a frame to 1.0, the phase `+1` steps round a **sixty-entry
cycle** (`01F223B0`), the height `+0x14` := cycle[phase] x envelope, and a second output `+0x18` follows a 28-entry
rise curve (`01F22590`) x 0.3, holding its last entry. While inactive the envelope falls at the same rate, the height
keeps its phase, the second output follows a 30-entry settle curve (`01F22670`), and at its end the running byte is
cleared. The three curves are filled at start-up by a table builder that the frame-rate setup calls; their values were
not read.

**Controller 12, read whole** (`00471150`, 220 B): a frame counter `+0xD` steps through an **eight-entry** pair of curves
(`01F22130`, `01F22170`) and stops the controller at the end; the two samples, scaled by the amplitude `+0x10`, are
rotated by the character's heading (record `+0x124`, through the engine's sine table) into a two-component offset at
`+0x20` / `+0x28`. An eight-frame shove in a direction relative to the character; ~~what triggers it was not traced~~ *(answered: see section 3a - the event handler `00427320` switches it on for the HP write's alive events `0x2005` / `0x2006`; 2026-10-02, OPUS)*.

## 6. Behaviour a reimplementation must keep

- A script's lip flap, nod or head shake takes effect at the next dirty-state pass, not at the verb.
- The plain verb forms never time out; a timed form ends through the same path as the plain *off*.
- The Confuse motion yields to Sleep and returns after it; the two flags are kept separately for that purpose.
- Ten of the thirty-two statuses have no arm in the status push.
- A rig frame with the flag byte `+0x63` (or the global override) non-zero runs sway only.
- Controller index = rig offset / 4; index 4 is absent.

## 7. What is not known

- Controller 8: what it is - its update is 1,857 bytes of register-bank arithmetic on the character's heading and
  position, not read; no enabler found. Controller 5: what starts its eased turn, and what the turn is for (section
  3a has what its small half shows).
  ~~Controllers 11, 12 and 16.~~ *Named the next day, section 3a.* What the body shake's two update bodies (472 and
  1,294 bytes) do with the amount was not read.
- What the lip flap, nod, head shake, Confuse and Immobilize controllers **compute** - their update bodies (4,173, 733,
  860, 1,841 and 520 bytes) were not read; they are named by their switches alone.
- ~~What thirty-six of the forty-four status arms push.~~ *Read the same day:*
  [how a status shows on a character](how-a-status-shows-on-a-character.md).
- The units of the timed forms: the setter divides the frame count by `[01DFE0BC]` and the countdown subtracts the same
  float each frame; ~~how that float moves with the frame rate was not established here~~ *(answered: see effect-element-type-dispatch.md - `001EDDC0`, the frame-rate switch, stores 2.0 to `01DFE0B8` (+0x18), 0.5 to `01DFE0BC` (+0x20) and 1 to `01F82E38` (+0x28) on its non-zero arm; the image holds 1.0, 1.0 and 0; 2026-10-02, OPUS)*.
- Nothing on this page was observed running.

## 8. Where each behaviour is in the bytes

| body | what | anchors |
|---|---|---|
| `003E1350` controller off (629 B) | bound; table jump; the seventeen arms, index 4 to the exit | `003E1353`, `003E136A`, `003E1374`, `003E1376`, `003E1395`, `003E13BB`, `003E1407`, `003E142D`, `003E1453`, `003E1479`, `003E14C5`, `003E14EB`, `003E1537`, `003E1559`, `003E157B`, `003E159D` |
| `003E00C0` the rig's frame (1,631 B) | sway and the override OR; the early exit; look fed; matrices reset; first solve; look solve; look apply gate; display-deny gate; last apply | `003E011D`, `003E0132`, `003E0146`, `003E0156`, `003E015E`, `003E019B`, `003E0234`, `003E04D3`, `003E0503`, `003E0680`, `003E0687`, `003E06B3`, `003E06DF` |
| `002EDDC0` body-shake setter (95 B) | free-record test; zero test; bit 16 cleared; bit 16 set; amount stored; dirty bit | `002EDDDA`, `002EDDE6`, `002EDDED`, `002EDE02`, `002EDE0C`, `002EDE14` |
| `0042BDE0` body-shake wrapper (230 B) | resource entry; guard; rig; flag bit 16; amount to the controller; on; off | `0042BE13`, `0042BE26`, `0042BE38`, `0042BE52`, `0042BE74`, `0042BE7A`, `0042BE9F`, `0042BEB1` |
| `00518F50` rotators update (418 B) | count; enable test; ramp counter; half-rate predicate; speed; angle; wrap; sine table; rotation stores; stride | `00518F69`, `00518FE4`, `00518FF4`, `00518FF8`, `0051900B`, `0051901D`, `00519027`, `0051906A`, `00519089`, `005190A3` |
| `0051A890` controller 5, shadow half (140 B) | flag bit; shadow test; entry test; angle x weight; negate; shadow store; look controller byte | `0051A8AD`, `0051A8B6`, `0051A8BF`, `0051A8DD`, `0051A8E8`, `0051A8ED`, `0051A8F4`, `0051A903` |
| `00513150` look off (108 B) | mode test; mode cleared; progress; step from the duration; angles remembered | `00513154`, `00513175`, `00513178`, `00513195`, `005131AA`, `005131B8` |
| `0042EE90` timed states (254 B) | skip bit; three timers, each: rig-has-it bit, non-zero, subtract, expire, clear flag, call | `0042EE96`, `0042EEA6`, `0042EEC6`, `0042EEDB`, `0042EEEC`, `0042EEF1`, `0042EF1E`, `0042EF35`, `0042EF3A`, `0042EF67`, `0042EF7E` |
| `0042DD90` lip-flap wrapper (186 B) | resource entry; guard; rig at `+0x94`; flag bit 6; on or off with index 9 | `0042DDC3`, `0042DDD6`, `0042DDE4`, `0042DDFE`, `0042DE0F`, `0042DE23`, `0042DE30`, `0042DE35` |
| `004716A0` Float bob update (290 B) | envelope down and up; cycle; rise and settle curves; x 0.3 | `004716C4`, `004716D9`, `004716FC`, `0047171B`, `00471732`, `0047174C`, `0047176F`, `0047178E`, `004717AA` |
| `00471150` controller 12 update (220 B) | counter and stop; two curve samples; heading to table index; rotation | `00471164`, `0047116B`, `00471193`, `004711AF`, `004711E3`, `00471203`, `0047121C` |
| `00515FE0` Confuse motion on (486 B) | already-on test; five inlined steps of the presentation generator when the global asks; seeds `+0x14`, `+0x1C`; on | `00515FE0`, `00515FED`, `0051608D`, `005160FE`, `0051614E`, `005161A6`, `005161C1` |

## 9. Related

- [The staged look command](the-staged-look-command.md) - the rig's reset, controllers 1, 2, 10 and 14.
- [The per-model oscillator subsystem](../Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md) - controller 0.
- [The thirty-two statuses](../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md) - the bits of section 4.

## Cross-subsystem neighbours

**Script VM native bridge - SERVICE.** The six verb handlers named in section 3 pop one or two arguments and tail-jump
into the actor-presentation services; the bridge owns the popping, this page owns what the record bits mean.

**Status / battle unit - SHARED RECORD.** The status push reads the unit's two status dwords through a unit accessor
described here by role; the statuses themselves, and everything they do to the rules, belong to the status pages. This
page owns only the thirty-two-way fan-out onto the body.

**Movement - CLIENT.** `002E3110`, a Movement-filed body that
[the party read-in state machine](../../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md)
describes as the step that applies a read-in model element, is a second, native user of the three talking-head states:
one of its arms sets the lip-flap bit with a zero timer inline, and another clears the lip flap inline and calls the
plain nod setter `002EE0D0` and the plain head-shake setter `002EDE70` with 0 - the three states dropped together when
a character's model element is applied. Only that window of the body was read.

**Core runtime scheduling - INCIDENTAL.** In its eye stage the rig's frame `003E00C0` calls `001EDE80` (61 B), a
scheduling-owned getter: it returns 1, or - when `01F82E38` is non-zero and `01DFE0C0` is zero - the sum of two frame-body
counters. It reads like *how many frames this update stands for*; what the eye stage does with the number was not read.

**Shared helpers - by role.** The encoded-pointer resolver, the VM pop routines, the unit accessor, the resource-table
lookup and the record dirty-state pass are described by role and not named, because naming a shared leaf imports every
one of its callers.

**Audio / Gameplay - MECHANICAL (SWE2-EC7, 2026-09-20).** Two `005131C0` callees are shared helpers with foreign
fan-in: `003326C0` is called by the Audio body `00332C40`, and `0046F460` is called by the Gameplay body `00339630`.
Shared-helper fan-in through the pass's own call list; no audio or gameplay relationship to the rig.


**Input — MECHANICAL (SWE2-EC7-156, 1 edge).** `00253C70` of that layer calls `001EDE70`, the gate batch-121's `0051B150` also runs — shared-helper fan-in, not a shared responsibility.

**WorldAreaField - CLIENT (1 edge; FABLE 2026-09-29).** `World_UpdateSimulationTick` (`00314020`), owned by that layer, is the only caller of the status push `003E7650` (one raw call site, `00314341`). The world tick drives section 4's status fan-out once per tick; which bits changed comes from the unit's stats record, and the tick contributes only the cadence ([the world simulation tick contract](../../00-Engine-Core-Runtime/Battle-Frame/CONTRACT-world-simulation-tick.md)). Read from the shipping bytes.

## SWE2-EC7-52 update (2026-09-19) - `0042BED0`

`0042BED0` (1163 B) is the controller-11 flag dispatcher - target-1 switches on flags bit 0, `0020E600`/`002ED570`/`00426220` calls. Interior anchor `0042BEF0` (a `0020E600` call).

## SWE2-EC7-82 update (2026-09-20) - `0051B110` + `005131C0` measured

`0051B110` (5 B) is the one-flag setter: `byte[rcx+0x15] |= 1` and
return.
Interior anchor `0051B114` (the `ret`).

`005131C0` (7,506 B, stack-cookie + full xmm save) is the large
presentation pass the rig callers drive: `0020E600` five times,
the `003E` cluster (`003E56A0`/`003E5700`/`003E5B30`x2/`003E5FA0`x2),
the `0046` cluster (`0046D0C0`x3/`0046D2A0`/`0046D360`/`0046F460`x2/
`0046FAA0`x2/`0046FAE0`), `0017D2E0` three formats, `00861F14` twice
and `004234B0`/`003326C0`/`00513150` once each across ~300 rip-based
data refs - a multi-stage per-element build.
Interior anchor `0051323A` (the first `0020E600` call).

## SWE2-EC7-83 update (2026-09-20) - `0042BBB0` + `00429C40` + `00429B40` flag-sync siblings measured

`0042BBB0` (252 B, stack-cookie) is the first of three record-flag
syncs the rig callers drive: `word[rcx]` chains `022C6F28 + ax*0x740`
records through `0042E690`, `word[+8]` recurses the same way, and
live `+8`/`+0xA` links run `0042EF90(rdi, rip-string, &stack)`; then
`dword[+0x304] bit7` folds into `byte[+0x40B] bit6` and `+0x290`
loses `0x4000`.
Interior anchor `0042BC02` (the first `0042E690` call).

`00429C40` (252 B) is the bit5 sibling: `0042DD90` record walks,
`0042EF90` child/sibling runs, `dword[+0x304] bit6` -> `byte[+0x40B]
bit5`, `+0x290` loses `0x2000`.
Interior anchor `00429C92` (the first `0042DD90` call).

`00429B40` (250 B) is the bit7 sibling: `0042DCD0` record walks,
`0042EF90` runs, `dword[+0x304] bit15` -> `byte[+0x40B] bit7`,
`+0x290` loses `0x8000` - completing the three-bit mirror of the
record's flag word.
Interior anchor `00429B92` (the first `0042DCD0` call).

## SWE2-EC7-87 update (2026-09-20) - `003E12A0` two-case mode dispatch measured

`003E12A0` (109 B) is the `edx`-keyed dispatch the rig callers
run: `9` resolves `[rbx+0x24]` through `0020E600` and forwards to
`00517610(record, r8d)`; `0xD` resolves `[rbx+0x34]` the same way
and tails `00471B20(record, r8d)`; every other value returns
untouched.
Interior anchor `003E12FD` (the `00517610` call).

## SWE2-EC7-89 update (2026-09-20) - `003B6B60` indexed float store measured

`003B6B60` (31 B) is the keyed scalar write the rig callers run:
`ecx` selects the 0xE0-stride slot in `[02B40528]`, and only when
the slot's `dword[+0x10]` key matches does `xmm1` land at `+0xBC`
- a generation-checked float publish.
Interior anchor `003B6B76` (the `movss` write).

`00516970` (2610 B) is the table walk `003E00C0` runs per rig element: `0020E600([rcx+0xAC])` resolves the record, then 27 more `0020E600` calls walk the resolved table - a pure table-resolution body, no other helper in the loop.

Interior anchor `00516E8F` (function `00516970`).

`00517650` (4173 B) is the gated field step `003E00C0` runs: `byte[rcx]` gates the whole body; `+0xC` loses `01DFE0BC * 0.125` each pass, then `003D8E50` x5 workbench calls, `003A6E60` expression evals and the `00517F83`/`005185A2` local arms - the rig element's timed field update.

Interior anchor `00517E6F` (function `00517650`).

`00516220` (1857 B) is the phase-table eval `003E00C0` runs: `0020E600([rcx+0xA8])` resolves the record, `[rdi+0x124]` divided by `01CEBC78` and scaled by `00D10820` folds to a `& 0x7FFF` index into `01F004E0`, then `0036DD80` x3 (shared emit machinery - it is also driven by UI-side callers outside this page's scope), `003E7D10`, `0026E350` x2 and `0046F460` x2 under `00861F14` - the controller's phase-driven compute.

Interior anchor `0051628D` (function `00516220`).

`00515660` (1841 B) is the fade-and-sweep `003E00C0` runs: `byte[rcx+8]` gates an `+0x38 -= 1.0 * 0.125` decay that clears `word[+0xA]` when it underflows, `0020E600([rcx])` resolves, then a `[rbx+4]`-counted SSE loop walks `01F004E0`/`00D10820`/`00D10828` constants - the second controller arm, call-light.

Interior anchor `005156DD` (function `00515660`).

`00519B60` (1762 B) is the proximity eval `003E00C0` runs: `0020E600([rcx+0x34])` resolves, `+0x70`/`+0x78` and `+0xB0`/`+0xB4` absorb `[rbx+0x140]`/`+0x148` deltas, `00380800` normalizes the `+0x70` pair, `dx^2 + dz^2` compares against the `01DFE0BC * 00D22C30` bound, and `0046FAE0` runs twice - the distance-checked arm.

Interior anchor `00519B7F` (function `00519B60`).

`00519170` (1447 B) is the record walk `003E00C0` runs: fifteen `0020E600` resolves over the `[rsi+4]`-bounded table, `[rbx+0x18]` nonzero gating the second half - the rig's heaviest resolve loop.

Interior anchor `00519187` (function `00519170`).

`005124D0` (1441 B) is the sibling walk `003E00C0` runs: `byte[rbx+0x34]` gates the body and fifteen `0020E600` resolves walk the record table - the flag-gated twin of `00519170`.

Interior anchor `005124E3` (function `005124D0`).

`00471E40` (1434 B) is the counted walk `003E00C0` runs: `dword[rbx+4]` bounds the loop and fifteen `0020E600` resolves step the records - the count-driven sibling.

Interior anchor `00471E57` (function `00471E40`).

`00514F20` (1409 B) is the eighth-count walk `003E00C0` runs: `byte[rbx+4]` gates, eight `0020E600` resolves - the half-size sibling of the resolve family.

Interior anchor `00514F37` (function `00514F20`).

`00472CD0` (1329 B) is the walk `003E00C0` runs: fourteen `0020E600` resolves back-to-back over the record fields - the near-call-free sibling.

Interior anchor `00472D36` (function `00472CD0`).

`0051B330` (1294 B) is the `+0x32`-keyed walk `003E00C0` runs: `word[rbx+0x32]` supplies each step's key and twelve `0020E600` resolves walk the table - the keyed sibling.

Interior anchor `0051B374` (function `0051B330`).

`005188C0` (1153 B) is the transform evaluator `003E00C0` runs: xmm6-xmm15 spill frame and cookie, `[rcx+0x2C]` `comiss` against zero takes the early path, `1.0f` and `0x80000000` rdata constants feed the math, `00203170` x2 runs the dual-channel compute - the rig's float-heavy per-controller evaluator.

Interior anchor `005189CE` (function `005188C0`).

`0051A3C0` (958 B) is the resolve-and-step body `003E00C0` runs: `byte[rdi+0x14]` and `byte[rdi+0x15]` gate the arm, `0020E600` resolves the record's head, then `0046FAE0` and `0051A780` step the controller - the rig's flagged resolve-step helper.

Interior anchor `0051A47A` (function `0051A3C0`).

`0051A780` (258 B) is the rig step `0051A3C0` and `0041DD40`/`005201B0` call: `mulss xmm0` scales by the `rip`-relative constant, `byte[rbx+0x17]` is read-modify-written, `dword[rbx+4]` compares the count, and `0020E600` resolves the field - the rig's flagged float-adjust helper.

Interior anchor `0051A7DA` (function `0051A780`).

`00472970` (860 B) is the rig body `003E00C0` calls: `0046D560` x2 and `003A6E60` x3 run the controller steps - the rig dispatcher's two-helper worker.

Interior anchor `004729ED` (function `00472970`).

`005121A0` (806 B) is the rig body `003E00C0` calls: just `0020E600` x2 across 806 bytes - a long field-copy/resolve pass over the controller record with almost no helper traffic.

Interior anchor `005121BB` (function `005121A0`).

`003E0B50` (797 B) is the controller apply `0042BED0` and `003E0E70` call: `0020E600` x17 with `0040ED90` x6 - the rig's resolve-heavy record walker, one of the pair.

Interior anchor `003E0B70` (function `003E0B50`).

`003E0F00` (770 B) is the sibling `0042BED0`/`003E1210` call beside `003E0B50`: identical `0020E600` x17 + `0040ED90` x6 shape - the second resolve-heavy walker of the pair.

Interior anchor `003E0F20` (function `003E0F00`).

`00471B60` (733 B) is the rig body `003E00C0` calls: `0020E600` x6, `0046D560` x2, `003A6E60` and `004723E0` run the controller steps - the dispatcher's resolve-and-helper worker.

Interior anchor `00471BAD` (function `00471B60`).

`003E1950` (702 B) is the flag-rewrite pass the controller-11 dispatcher `0042BED0` calls: `0020E600` resolves the `byte[+4]`-counted table, per 0x30-stride record (pairs stride 0x60) `byte[+1]&0x1F` switches, `byte[table+0x1A]` bit-tests, `word[+0x2A]`/`+0x5A` bit-0 flips against the argument, `byte[+0x29]`/`+0x59` flag bits set, `0040ED90` applies, high nibble cleared - the controller's per-element flag rewrite.

Interior anchor `003E1962` (function `003E1950`).

`0040B180` (554 B) is the pose-slot evaluator `003E00C0` fans out to: `[rcx+5]` gates a `0020E600([rcx+0xC])` -> `0020E600(*)` double resolve, `0020E600([r15])` once more for the slot base, then `[rbp+2]`-counted entries take `[rbp+0x29] & 0xF` mode arms with `ucomiss`/`mulss` on the `xmm6` input x `01DFE0BC` - the rig's per-slot blend.

Interior anchor `0040B19D` (function `0040B180`).

`004713A0` (520 B) is a pose-slot evaluator `003E00C0` fans out to: `0020E600([rcx+4])` resolves, `[rbx]` gates, then `[rbx+0xC]` counts down by `01DFE0BC` x `3E000000` x `008F311C`, clears `byte[+1]` at zero, and `+0x14`/`+0x10` = `+0xC` x `+0x1C`/`+0x18` while `[r9+0x124]` divides into the `01CEBC78`/`00D10828`/`00D10820` angle constants with `ecx = 0x2000` - the rig's decay-and-rotate slot.

Interior anchor `004713AC` (function `004713A0`).

`0051B150` (472 B) is the table evaluator `003E00C0` fans out to: `001EDE70` gates, `word[rbx+0x30]` splits bit0->xmm5 (`* 0x5`) and `>>1 *3` strides into the `01F2A160` word table, `movsx` triples load, then xmm6/xmm7/xmm8 (`0x38000100`, `1.0f`) run the `0046D560` blend - the rig's triple-table pose arm.

Interior anchor `0051B171` (function `0051B150`).

`003E29F0` (469 B) is the setter `003E00C0` and `005207C0` call: `0020E600([rbx+8])` resolves, `esi-1` dispatches three cases - `2` copies `bpl<<7` into `byte[+0x1C]` bit 7, `1` runs `[rbx+0x70]` through `0020E600` into the `+0x650` record with `003E3340`/`003E3400`/`00512D80`/`00513150`/`00515600`, `3` falls to `0046D560`-side work - the rig's per-kind option write.

Interior anchor `003E2A19` (function `003E29F0`).

`005186A0` (371 B) is the state publish `003E00C0` calls: `[rcx + 0x80] == 0xFFFF` skips; `movups` copies `[rcx + 0x50]`/`[+0x60]`/`[+0x70]` into the `022D9200`/`022D9210`/`022D9220` globals, then eleven `0020E600` resolves drive an `imul rdx, rcx, 0x290` record walk - the rig's vector push.

Interior anchor `005186DD` (function `005186A0`).

`004723E0` (331 B) is the class picker `00471B60` calls: an 8-way jump table on `dword[rcx+0x10]` (<=7) selects one of eight `01F22xxx` constant pairs into `[rsp+0x20]`/`[rsp+0x28]` - the controller-record GUID pair the rig binds per class index.

Interior anchor `004724F6` (function `004723E0`).

`0042DCD0` (189 B) is the flag-selected pair commit `00429B40` runs for flag `0x8000`: `[rcx+0x18]`'s `-1`-guarded index `0020E600` -> `[rax+0xD98]` -> `002ED570`-resolves the partner record `rbx`; `00426220(rcx, [rsi+8])` must pass and `rbx` must resolve through its `[rbx+0x94]` index, then `[rsi+8]`'s `+0x304` flag byte picks the emit - bit `0x8000` set tail-jumps `003E1610` with `edx = 0xF`, clear calls `003E1350` with the same code

Interior anchor `0042DD3E` (function `0042DCD0`).

`0042D8B0` (189 B) is the identical commit `00429830` runs for flag `0x100`: same `+0x18` index resolve through `0020E600`/`[rax+0xD98]`/`002ED570`, same `00426220` gate on `[rsi+8]`, but `+0x304` bit `0x100` selects `003E1610` over `003E1350` and the pair is committed with command code `edx = 0xA`

Interior anchor `0042D91E` (function `0042D8B0`).

`0042E690` (186 B) is the third sibling `0042BBB0` runs for flag `0x80`: the shared resolve-and-gate frame, `+0x304` bit `0x80` choosing `003E1610` versus `003E1350`, command code `edx = 0xD` - three `+0x304` flag bits driving the same two-entry resolve pair under three different command ids

Interior anchor `0042E6FE` (function `0042E690`).

`003E6F90` (173 B) is the stat commit `0042BED0` runs per controller record: `[rcx+0x18]` `0020E600`-resolves then `002ED570` on `[rax+0xD98]` gives the target row `rsi`; a second `0020E600` on `[rcx+0x10]` feeds `0046E420` keyed by `+0x18`; when `+0x284 & 0x20000` was armed, `[rsi+0x94]`'s resolve contributes `+0x64` into `ebx`, `00372710(rsi, ebx)` commits it, and both `+0x284` bit `0x20000` and the `+0x40A` byte clear

Interior anchor `003E6FC2` (function `003E6F90`).

`003E7040` (170 B) is the conditional child-resolve `0042BED0` runs: a non`-1` `[rcx+0x18]` id looks up through `0020E600` and resolves a record via `002ED570` on `[rax+0xD98]`; when the record exists with `+0x290` bit `0x200` set and `+0x284` bit `0x20000` clear it adds `0020E600([rdi+0x94])->+0x64` into `esi` and commits `00372710(rec, esi)`, then clears both bits and the `+0x40A` byte either way

Interior anchor `003E7072` (function `003E7040`).

`00372710` (80 B) is the gated commit sink `003E6F90` and `003E7040` both finish through: when the record's `[rcx]` flags carry `0x200` and `[rcx+0x90]` is positive it resolves `[rcx+0x94]` through `0020E600` twice (probe then arg) and runs `003E1C10(obj, edi)` - the stat value the callers accumulate lands only under those two gates

Interior anchor `00372750` (function `00372710`).

`003E6E60` (139 B) is the handle resolver `003E6340`/`003E68B0`/`003E6A70`/`003E6EF0` call on the render record: `00422D50` gates, `+0xE0` and `+0xF8` are resolved through `0020E600` with `+0xE8`/`+0x100` added and cached into `+0x558`/`+0x560`, and the result returned is `base + dword[+0xE8]` or 0 when the gate or a resolve fails - the address fix-up the rig's `+0x550`-region consumers share.

Interior anchor `003E6EA0` (function `003E6E60`).

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives

**Attack.** Sections 3 and 5's structural claims, and section 8's sizes, became checks at their instructions and tables.
Script: `Tools/analysis-kit/gfz-scripts/falsify_rig_controllers.py`, output `falsify_rig_controllers.out`, image
`73461d08…`, 0 BROKEN, exit 0. Carried:
- section 2's rig-from-`@FCP` census (`uq220_section2_rig.py`);
- section 4's status-push bit map;
- section 5's solve and apply order.

| # | Clause attacked | Result |
|---|---|---|
| R0 | section 8 sizes | **survives**: all twenty-one |
| R1 | section 3 (the switches) | **survives**: both bound `n` by `cmp edx, 0x10`; both 17-entry tables (`003E15C8`, `003E1888`) send index 4 to the exit, and the other sixteen arms are distinct |
| R2 | section 3 (the setters) | **survives**: each timed service divides by `[01DFE0BC]` and tail-jumps to the setter that stores `+0x640` / `+0x644` / `+0x648`; the lip-flap wrapper reads the rig at `+0x94` and tests `+0x304` bit 6 |
| R3 | section 3 (the countdown) | **survives**: the `+0x290` and `+0x40B` gates and the `01DFE0BC` subtraction; the phase walks the list at `+0x48800` |
| R4 | section 5 (the frame) | **survives**: `02B59D68` is tested at `003E0680`; the rig bytes `+0x63` and `+0x5F` are read |
| R5 | section 5 (two controllers) | **survives**: the Float bob's three tables `01F223B0` / `01F22590` / `01F22670` (image base plus displacement) and the time base; controller 12's curves `01F22130` / `01F22170` and the heading `+0x124` |

No correction.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-rig-of-seventeen-controllers-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002E8570` | 110 B | returns at once when `rcx` is null, when qword `rcx+0xC0` is null, when the dword it points to is -1 or when its word is -1; otherwise forms the record `movsx(word) * 0x740 + qword 022C6F28` and, when that is non-null and dword `+0x284` is non-zero, zeroes dword `+0x640` and then clears bit `0x40` of dword `+0x304` when `edx` is 0 or sets it when `edx` is non-zero, ORing `0x2000` into dword `+0x290` on both paths | `002E8593`, `002E85A3`, `002E85AC`, `002E85BA`, `002E85CC` |
| `002E85E0` | 39 B | returns when `rcx` is null, when qword `rcx+0xC0` is null or when the dword it points to is -1; otherwise divides `xmm2` by 1.0 (`01DFE0BC`) and tail-jumps `002EDF30` with `ecx` = the zero-extended word at that pointer, `edx` and `xmm2` passed through | `002E85E5`, `002E85F1`, `002E85F6`, `002E85FE`, `002E8601` |
| `002E8B80` | 39 B | returns when `rcx` is null, when qword `rcx+0xC0` is null or when the dword it points to is -1; otherwise divides `xmm2` by 1.0 (`01DFE0BC`) and tail-jumps `002EE130` with `ecx` = the zero-extended word at that pointer, `edx` and `xmm2` passed through | `002E8B85`, `002E8B91`, `002E8B96`, `002E8B9E`, `002E8BA1` |
| `002ED320` | 39 B | returns when `rcx` is null, when qword `rcx+0xC0` is null or when the dword it points to is -1; otherwise divides `xmm2` by 1.0 (`01DFE0BC`) and tail-jumps `002EDED0` with `ecx` = the zero-extended word at that pointer, `edx` and `xmm2` passed through | `002ED325`, `002ED331`, `002ED336`, `002ED33E`, `002ED341` |
| `002EDE70` | 91 B | returns when `cx` is -1; otherwise forms the record `movsx(cx) * 0x740 + qword 022C6F28` and, when that is non-null and dword `+0x284` is non-zero, zeroes dword `+0x648`, then clears bit `0x8000` of dword `+0x304` when `edx` is 0 or sets it when `edx` is non-zero, ORing `0x8000` into dword `+0x290` on both paths | `002EDE7A`, `002EDE8A`, `002EDE93`, `002EDEA1`, `002EDEB6` |
| `002EDED0` | 95 B | returns when `cx` is -1; otherwise forms the record `movsx(cx) * 0x740 + qword 022C6F28` and, when that is non-null and dword `+0x284` is non-zero: when `edx` is 0 clears bit `0x8000` of dword `+0x304` and stores `edx` (0) at dword `+0x648`, else sets that bit and stores the float `xmm2` at `+0x648`; both paths OR `0x8000` into dword `+0x290` | `002EDEDA`, `002EDEF7`, `002EDF01`, `002EDF1C`, `002EDF24` |
| `002EDF30` | 89 B | returns when `cx` is -1; otherwise forms the record `movsx(cx) * 0x740 + qword 022C6F28` and, when that is non-null and dword `+0x284` is non-zero: when `edx` is 0 clears bit `0x40` of dword `+0x304` and stores `edx` (0) at dword `+0x640`, else sets that bit and stores the float `xmm2` at `+0x640`; both paths OR `0x2000` into dword `+0x290` | `002EDF3A`, `002EDF57`, `002EDF5E`, `002EDF76`, `002EDF7E` |
| `002EE0D0` | 91 B | returns when `cx` is -1; otherwise forms the record `movsx(cx) * 0x740 + qword 022C6F28` and, when that is non-null and dword `+0x284` is non-zero, zeroes dword `+0x644`, then clears bit `0x80` of dword `+0x304` when `edx` is 0 or sets it when `edx` is non-zero, ORing `0x4000` into dword `+0x290` on both paths | `002EE0DA`, `002EE0EA`, `002EE0F3`, `002EE101`, `002EE116` |
| `002EE130` | 95 B | returns when `cx` is -1; otherwise forms the record `movsx(cx) * 0x740 + qword 022C6F28` and, when that is non-null and dword `+0x284` is non-zero: when `edx` is 0 clears bit `0x80` of dword `+0x304` and stores `edx` (0) at dword `+0x644`, else sets that bit and stores the float `xmm2` at `+0x644`; both paths OR `0x4000` into dword `+0x290` | `002EE13A`, `002EE157`, `002EE161`, `002EE17C`, `002EE184` |
| `003E0E70` | 132 B | when `edx` is 0, returns if `0020E600(dword [rcx])` is null and otherwise takes `eax = 0040DB00(0020E600(dword [rcx]), r8d)`; when `edx` is `0xB`, does the same with dword `+0x2C` and `00519100`; in both cases returns without further work when `eax` is `0xFFF`, else calls `003E0B50(rcx, edx, eax)`; any other `edx` calls `003E0B50(rcx, edx, 0)` directly | `003E0E8D`, `003E0EAC`, `003E0ECB`, `003E0ED0`, `003E0EDF` |
| `003E1210` | 132 B | when `edx` is 0, returns if `0020E600(dword [rcx])` is null and otherwise takes `eax = 0040DB00(0020E600(dword [rcx]), r8d)`; when `edx` is `0xB`, does the same with dword `+0x2C` and `00519100`; in both cases returns without further work when `eax` is `0xFFF`, else calls `003E0F00(rcx, edx, eax)`; any other `edx` calls `003E0F00(rcx, edx, 0)` directly | `003E122D`, `003E124C`, `003E126B`, `003E1270`, `003E127F` |
| `003E3400` | 57 B | when `0020E600(dword rcx+8)` is non-null, resolves it again and replaces the low nibble of byte `+0x1D` of the result with the low nibble of `edx` (AND `0xF0`, then OR `dl` AND `0xF`); otherwise returns untouched | `003E3412`, `003E341F`, `003E3424`, `003E3427`, `003E342B` |
| `00428F80` | 82 B | reads the qword `022C6F28` once as the base and walks a list rooted at its dword `+0x48800`: while the index is not -1 it calls `0042EE90(qword 022C6F28 + index * 0x740, entry base)`, re-reading qword `022C6F28` after each call for the element address and for the next index, which is the sign-extended word `+4` of that `0x740`-byte element; it stops at -1 (an initial dword -1 returns at once) | `00428F90`, `00428FA6`, `00428FB1`, `00428FBD`, `00428FC5` |
| `0046D360` | 27 B | calls `00202B90(rcx)` and then stores the dword `0x3F800000` at `rcx+0xC` | `0046D369`, `0046D36E` |
| `00471640` | 27 B | when byte `[rcx]` is non-zero, clears it and replaces byte `+2` with the byte of the table `01F22760` indexed by the old byte `+2`; when it is 0, returns untouched | `00471643`, `00471649`, `00471650`, `00471653`, `00471657` |
| `004718D0` | 31 B | when byte `[rcx]` is 0, stores 1 in byte `+3` and in byte `[rcx]` and replaces byte `+2` with the byte of the table `01F227A0` indexed by the old byte `+2`; when it is non-zero, returns untouched | `004718D3`, `004718D9`, `004718E0`, `004718E4`, `004718EB` |
| `00517610` | 52 B | clears bits 6 and 7 of byte `rcx+1` (AND `0x3F`); when `edx` is non-zero, tail-jumps `00518820` (`rcx`, `edx` passed through) if byte `+1` AND `0x30` is non-zero and otherwise returns; when `edx` is 0, sets bit `0x40` of byte `+1`, copies dword `+0x10` to `+0x88` and dword `+0x4C` to `+0x8C`, zeroes byte `+0` and stores the dword `0x3F800000` at `+0xC` | `00517618`, `0051761E`, `00517626`, `0051762A`, `0051763C` |
