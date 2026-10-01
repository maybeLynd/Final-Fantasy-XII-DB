---
system: How an animation makes a sound - the two authored commands, the character's sound emitter, the twelve sound types, which variation is picked and where it is heard from
category: 18-Audio
status: DOCUMENTED
owner_layer: PrimaryOwner:Audio
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the two command handlers 00520C50 and 00520D00, the emitter's play routine 0046CC70 (1,069 B), its variation
    picker 0046C250 (1,090 B) with both jump tables read out of the image, its emission-point routine 0046C6E0 (438 B),
    the descriptor build 0046C8F0 (626 B) and the actor-side sound lookup 002E9D90 (586 B) disassembled from the
    authority image and read whole, 2026-09-20; the two commands then tallied over every animation container of an
    extracted copy of the game, with totals that had to match the authored-command census and did
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-anim-sound-falsification-pass-1
  note: written by FABLE. Static plus one data census. Names for the twelve types come from WHERE each is authored and
    are labelled as readings of the data. Scopes - does not overturn - the sound driver's round-robin finding on the
    variation page. NOT read - the spatial descriptor builders and the play call beyond their arguments, the bank
    resolvers, the ground table, the three non-positional bank getters. Pending first review
---

# How an animation makes a sound

A footstep, the swish of a sword, a grunt of effort, a cry of pain: none of these is asked for by the battle system or
by a script. They are **authored into the animation**. Two of the commands in a character's command stream
([where the commands are authored](../17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md))
say "make a sound of *type n* now", and everything else - which sample, which variation, from which point of the body,
how loud - is worked out at that moment by the character's **sound emitter**, a small object inside its render record.

## 1. The two commands

| command | handler | what it passes to the emitter's play routine `0046CC70(emitter, mode, type, volume)` |
|---|---|---|
| `0x05` | `00520C50` (43 B), through bank B | word `+2` = `mode << 12 \| type`; volume 0, which means full |
| `0x29` | `00520D00` (37 B) | mode 0, **type 1**, volume = the signed word `+2` out of 128 |

The emitter is the render record's sub-object at `+0x5F0`. (`0x19`, a sibling of `0x29` that passes the same word with a
different mode, is never authored.)

**What is authored** ([`census.py`](../_experiments/evidence/character-sound-commands/census.py),
[output](../_experiments/evidence/character-sound-commands/census.out.txt); totals match the authored-command census
exactly - 23,783 and 47,472 in the animation containers):

| type | commands | authored in blocks named | emitted from (section 3) | a reading of the data |
|---:|---:|---|---|---|
| 1 (`0x29`) | 47,472 | `ready`, `attack`, `turn`, `field_attack`, `c_turbo` | bone `0x101` | a **footstep** - volume 128 on 45,968, 64 / 32 for soft steps, 255 on 386 |
| 10 | 4,330 | `ready`, `attack`, `turn`, `ev_walk`, `c_turbo` | the body | movement noise |
| 9 | 3,530 | `ready`, `attack`, `magic`, `ability` | the body | effort |
| 5 | 3,437 | `damage`, `knockback_s`, `poach`, `dead` | bone `0x0C` | a **hurt voice** |
| 6 | 2,405 | `knockback_l`, `dead`, `poach` | bone `0x0C` | a heavy hurt / death voice |
| 2 | 2,092 | `attack` | the `0x200` attachment | a **weapon swing** |
| 3 | 1,931 | `field_attack`, `attack` | the `0x200` attachment | a second swing sound |
| 8 | 1,914 | `knockback_l`, `dead` | bone `0x101` | the body hitting the ground |
| 7 | 1,542 | `ready`, `c_turbo` | bone `0x0C` | an **idle voice** |
| 11 / 12 | 743 / 699 | `active` / `deact` | the body | drawing and sheathing the weapon |
| 4 | 608 | `attack` | bone `0x0C` | an **attack voice** |
| mode 4: 101-104 | 552 | monster blocks only | the body | an explicit sound number (below) |

No mode-0 type outside 1..12 is authored, and no mode other than 0 and 4.

## 2. Which variation - `0046C250`

The picker turns a type into a **bank group** (emitter byte `+5`) and a **variant** (byte `+6`). Where it chooses, it
chooses with ~~the **gameplay random number generator**~~ **the presentation bit-feedback PRNG, `003A6E60` on
`01EF93E8` (CORRECTED 2026-09-29, OPUS, CON-190)**, and it keeps the last choice of each family in a nibble of
emitter bytes `+1`..`+3` so that **the same variation is never picked twice running** (a repeat is stepped down by
one, wrapping).

| type | group | variant |
|---:|---:|---|
| 1 | 1 | 0 - **fixed**; the footstep does not roll here (section 4 is where it varies) |
| 2 | 0 | by the *kind* of the character's `0x200` attachment (its weapon): kind 1 -> one of 0-2; kind 2 -> 3-5; kind 3 -> 6-7; kind 4 -> a pair of its own; kind 5 -> `0x0C`; kind 6 -> `0x0D`. No attachment, no sound |
| 3 | 0 | `0x0A` |
| 4 | 2 | needs the `0x400` attachment's info: kind 1 -> draw 0-3, **0 is silence**, else 0-2; kind 2 -> draw 0-4, 0 is silence, else 6-7; any other kind is silence |
| 5 | 2 | draw 0-3, **0 is silence**, else 3-5 |
| 6 | 2 | 8 or 9 |
| 7 | 2 | a **countdown** in emitter byte `+4`: nothing until it reaches zero, then it is reloaded with 3-11 and a draw of 0-3 decides - 0 is silence, else `0x0A`-`0x0C` |
| 8 / 9 / 10 | 2 | `0x15` / `0x17` / `0x19` |
| 11 / 12 | 0 | `0x0E` / `0x0F` |

So silence is authored into the odds: **an attack cry is skipped one time in four or five, a cry of pain one time in
four, and the idle voice speaks on roughly one request in seven and then holds its tongue a quarter of the time.**

**This scopes a sentence on [the variation page](which-variation-of-a-sound-you-hear.md).** That page reads the sound
driver and finds that a trigger with several variations cycles them by a stored cursor - "no draw, no seed" - and
concludes that repeated footsteps and hits are identical on every playthrough. For **footsteps** the picker agrees:
type 1 never rolls. For **weapon swings and voices** there is a second layer above the driver that does roll. ~~It
draws from the same generator as combat, so those are not reproducible and each one consumes a gameplay random number.~~
**It draws from the presentation stream that procedural rendering and authored expressions share, not from combat's
generators (CORRECTED 2026-09-29, OPUS, CON-190).**

## 3. Where it is heard from - `0046C6E0`, `0046C8F0`

Both routines resolve the same point by type, through the same twelve-entry table: types **1 and 8** take bone id
`0x101`; **2 and 3** the `0x200` attachment, falling back to `0x100`; **4 to 7** bone `0x0C`, falling back to `0x100`;
**9 to 12** `0x100`. The source's radius is half the character's FCP length property `0x9001D1E`
([the FCP block](../17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md)), so a big
monster is a big sound source. The position and radius go to the spatial descriptor builders
([the spatial audio object model](the-spatial-audio-object-model.md), which already lists `0046C8F0` and `0046CC70`
among the four bodies that originate a descriptor). Type 1 alone uses the builder that takes one more float, looked
up in a table by the model instance's byte `+0xB5`; what that byte classifies was not established.

`0046C6E0` runs first and can veto the sound (for type 1 it does so when the builder hands back zero); `0046C8F0`
then builds the descriptor for real,
scales its volume byte by `volume / 128` (rounded toward zero, capped at `0x7F`), **plays nothing if that comes to
zero**, and calls the play routine.

## 4. Which sample - `002E9D90(actor record, group, variant, footstep flag)`

Nothing is looked up unless audio is up, two enable bytes are set and the actor's manager allows it. The actor record
owns a **sound set** at `+0xC0`; group 0 reads its common half, groups 1 and 2 the set itself; the bank is the set's
`group`-th handle and the sample index starts as the variant.

- **Group 1, the footstep:** ~~the index becomes a per-actor base plus a ground term~~ ***corrected 2026-09-20 (FABLE), an
  hour after publishing: there is no per-actor base.*** The word read at `002E9F29` is the movement body's **ground
  type** (`+0x8A`, what `getmapgroundtype` returns -
  [the movement body](../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md)), and the
  table is `soundfoottable.bin`: index = *set* + *surface*, *set* being the table's header count, 32, when the
  caller's flag and the field-environment variant are both non-zero; the byte at `+0x10 + index` is the bank-local
  sound, and the variant is added once more when the flag is set. I decoded this on 2026-09-17 on
  [the five small tables](../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md) and did not
  find my own answer because I searched this category and not the database for the address. The flag is up for
  sound types 1, 8, 9 and 10. So the sample changes with the surface, which is the behaviour
  [sound variant selection](Sound-Selection/sound-variant-selection.md) describes from the driver's side.
- **The footstep's visible half is a separate command.** `0x18` (28,222 authored, in the same blocks) spawns a
  footstep *effect* chosen by the same ground type under the same gate -
  [the authored-command page](../17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md), row `0x18`.
- **Group 2 with a variant below 10:** when the actor record carries a voice id and that id's class is 3, the sound
  number is built directly from it - a per-character voice - instead of going through the bank.
- Otherwise the bank and index are resolved to a handle.

## 5. The play routine - `0046CC70`

Refuses unless the emitter is enabled (byte `+0` = 1), a global mute test passes, and the owner record is live with
bit 4 of its `+0x284`. Then by **mode**:

- **0** - the chain above: picker, lookup, audibility test, descriptor, play. Footsteps (type 1) are dropped while a
  record test with argument `0x1A` holds; types `0x0B` / `0x0C` only for the party's focus actor; type 7 not while the
  previous voice still plays. **Voices interrupt voices:** for types 4 to 7 the emitter remembers the playing handle
  (`+0x18`) and type (`+0x1C`), and a new one stops it first.
- **1, 2, 3** - the "type" is a direct id resolved through one of three bank getters and played **without a
  position**, centred, at `volume x 64 / 128`. Not authored in any shipped block.
- **4** - an explicit sound number (types below `0x100` get bit 31) played at the character with the same radius. The
  552 authored uses are monsters' own ids 101-104.
- **5** - with type 1, only stores `0xC00` in the emitter's word `+5`.

## 6. What a reimplementation must keep

- Sounds are **events of the animation**, not of the action: an interrupted animation never reaches its later
  commands, and its sounds are not heard.
- One emitter per character; voices are exclusive, footsteps and swings are not.
- The weapon decides the swing sample; the ground decides the footstep sample; the character decides the voice.
- Swings and voices ~~**consume gameplay random numbers**~~ **advance the presentation PRNG** when they are picked
  (CON-190). ~~animation playback is therefore part of the random stream, and two clients that animate differently
  will diverge.~~ Two clients that animate differently diverge in that stream (later visual randomness), not in combat
  rolls.
- A volume that scales to zero is not played at all.

## Evidence

| body | interior anchors |
|---|---|
| `0046CC70` play (1,069 B) | `0046CC9A`, `0046CCAE`, `0046CCF1`, `0046CD04`, `0046CD21`, `0046CD4D`, `0046CD5F`, `0046CD86`, `0046CD9D`, `0046CDC3`, `0046CDD9`, `0046CDF7`, `0046CE0F`, `0046CE1F`, `0046CE4A`, `0046CE54`, `0046CE5E`, `0046CEE1`, `0046CF71`, `0046CF84`, `0046CFCA`, `0046CFD6`, `0046CFDF`, `0046CFE8`, `0046D03B`, `0046D051` |
| `0046C250` variation picker (1,090 B) | `0046C273`, `0046C290`, `0046C29C`, `0046C2C0`, `0046C2C5`, `0046C2CF`, `0046C2F1`, `0046C303`, `0046C332`, `0046C372`, `0046C3E3`, `0046C3F6`, `0046C409`, `0046C42B`, `0046C451`, `0046C473`, `0046C4BD`, `0046C522`, `0046C56D`, `0046C5A5`, `0046C5BC`, `0046C5C9`, `0046C606`, `0046C61B`, `0046C630`, `0046C645`, `0046C659` |
| `0046C6E0` audibility and point (438 B) | `0046C702`, `0046C74B`, `0046C75D`, `0046C76A`, `0046C79D`, `0046C7B9`, `0046C7D3`, `0046C7F6`, `0046C80B`, `0046C81E`, `0046C84F`, `0046C861` |
| `0046C8F0` descriptor and play (626 B) | `0046C91E`, `0046C97F`, `0046C98C`, `0046C9BF`, `0046C9DB`, `0046C9F5`, `0046CA18`, `0046CA2D`, `0046CA4F`, `0046CA64`, `0046CA79`, `0046CA9B`, `0046CAAE`, `0046CB1D` |
| `002E9D90` sample lookup (586 B) | `002E9DAB`, `002E9DB8`, `002E9DC5`, `002E9E24`, `002E9E4F`, `002E9E8D`, `002E9EA3`, `002E9EEB`, `002E9F35`, `002E9F50`, `002E9F62`, `002E9F73`, `002E9F81`, `002E9F90`, `002E9FB2` |

Under 128 bytes, read whole: `00520C50`, `00520D00`, `0046CBA0`.

## Cross-subsystem neighbours

**Presentation - CLIENT.** The commands, their handlers and the emitter's home in the render record are the
presentation layer's; the bone and attachment lookups and the FCP property read are its services, used by result.

**Actor entity - DATA.** The sound set, the voice id and the manager flags the lookup tests are fields of the actor
record and its manager.

**Gameplay - SHARED GENERATOR.** The picker draws from the gameplay random number generator; that is the crossing this
page exists to record.

**Party - READ-ONLY GETTER.** The play routine asks for the party's focus actor to gate two types.

**World / field - SERVICE.** The ground term comes from a table the field layer supplies.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Script_VM_Native_Bridge — CLIENT (3 edges).** Three script verb bodies, `0034B7C0`, `0034C210` and `0034CA40`, pop their arguments off the value stack, call the actor-side sound lookup `002E9D90` for the actor's sample (`0034B7C0` with group 1), and hand the result to the play path unless a check on the actor's byte `+0x15` refuses. Scripts ask for an actor's sample through the same lookup the animation command uses, so the sound set on the actor record answers both a script's request and an animation's; the verbs own only their argument popping.

## SWE2-EC7-93 update (2026-09-20) - `00361BF0` + `00361750` measured

`00361BF0` (242 B) is the staged-record call `0046C6E0` runs: four
`02CDC0xx` vec4 lanes plus `xmm3` and a `divss` ratio fill a 0x50
stack record, `00361810` consumes it, and `[rbx]`'s dword is then
rescaled by the `0x81020409` magic-multiply rounding division.
Interior anchor `00361CA6` (the `00361810` call).

`00361750` (91 B) is the sibling record builder `0046C8F0` runs:
four `02CDC0xx` vec4 lanes land at `r9`, byte `+0x19` comes from
`02CDCE84`, `+0x10` holds the divisor and `+0x1C` holds the `divss`
ratio - the compact form of the same staging contract.
Interior anchor `0036179A` (the `divss`).

## Falsification pass 1 — 2026-09-29 (OPUS): the picker's generator refuted (CON-190); every other section survives

**Attack.** Sections 1, 2, 3 and 5 were turned into checks at their instructions, including both jump tables. Script:
`Tools/analysis-kit/gfz-scripts/falsify_animation_sound.py`, output `falsify_animation_sound.out`, image `73461d08…`,
0 BROKEN after the correction, exit 0. The authored-command census of section 1 is carried, not re-run.

| # | Clause attacked | Result |
|---|---|---|
| S0 | sizes | **survives**: all seven |
| S1 | section 1: the two commands | **survives**. `0x05` reaches the play routine through `0046CBA0`, which zeroes the volume argument |
| S2 | sections 2 and 6: "the gameplay random number generator", "the same generator as combat" | **REFUTED (CON-190).** Every draw in the picker is `003A6E60`, and the picker calls nothing else that could draw. `003A6E60` steps the **presentation bit-feedback PRNG**: state `01EF93E8`, mode word `022D9138` (generator 4 of [which generator serves which roll](../21-RNG-And-Determinism/CONTRACT-which-generator-serves-which-roll.md); the same leaf serves [authored expressions](../02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md)). No gameplay generator is touched |
| S3 | section 2's table | **survives, with an addition.** Types 4 and 5 are also silent when `003326C0` finds nothing for emitter word `+8` (`0046C433`, `0046C50F`) |
| S4 | section 3's point table and radius | **survives**: 1 and 8, 2 and 3, 4 to 7, 9 to 12; the radius is `0x9001D1E` × 0.5 |
| S5 | section 5's gates | **survives** |

**The correction, in player terms.**
- Which swing or voice variation plays is random, but it comes from the presentation stream, which procedural
  rendering and authored expressions share, not from combat's dice.
- An animation that plays differently on two machines can change later visual randomness, but **not** a combat roll.
- The "reload and get the same result" behaviour of combat is unaffected by sounds.
