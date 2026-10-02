---
system: The staged look command - how a request to turn a character's head or eyes reaches the look controller
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the applier 003E37F0, the dirty-state caller 00429920, the dispatcher 002EC3F0, the four angle setters
    and the two blend starters disassembled whole; the eighteen builders read (17 to 48 bytes each);
    the eighteen forwarders found by pattern over every listed function (control - the search returns exactly
    18); forwarder to service to verb joined by a members script over direct call and jump edges and the verb
    table
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-staged-look-falsification-pass-1
  note: written by FABLE from the uncredited-body breakdown (003E37F0, 909 bytes, was uncited and
    unresolved); first review = the 0929 promotion sweep: promoted DOCUMENTED -> AUDITED 2026-09-29 by SWE2-AUDIT-SPEC (promotion sweep): falsification pass-1 (opus-staged-look) FAILS 0 reproduced, all seven clauses survive with no correction; five classified neighbour edges dispositioned; no standing killer observation; zero open boxes
  crossref_clean: true
  reopened_count: 0
---

# The staged look command

Nothing that wants a character to look somewhere touches the look controller directly. A request - from a script
verb, from the steering record, from the bind path - is **staged** as bits and a few values in a `0x50`-byte command
record inside the character's render record (at `+0x580` of the `0x740`-byte record of
[the character render record array](the-character-render-record-array.md)). The render records' dirty-state pass
then applies the record to the look controller of the character **and of every record attached beneath it**, and
zeroes it. One request word, thirty-two bits, each with a fixed meaning.

## 1. What the player sees

A head that turns toward a point over a number of frames and relaxes again; eyes that move on their own
(`eyemove_381`); a head that refuses to turn past its limit while a script holds the lock
(`lookat_maxangle_limit_lock`). All of these are this one record.

## 2. The three stages

**Stage.** Eighteen record-level forwarders - each exactly `add rcx, 0x580` / `jmp builder` - stand between the
actor-service layer and eighteen builders of 17 to 48 bytes. A builder ORs a **request bit** into the dword at
`+0`, sets or clears the **value bit** that goes with it, clears the request bits it excludes, and stores its payload.
([look_command_census.py](members/look_command_census.py), [look-command-census.tsv](members/look-command-census.tsv).)

**Apply.** `00429920` (299 B), reached from `RenderRecords_ProcessDirtyState`, looks the record up by its own index
(word `+0`), skips it if `00426220` reports it busy, fetches its look controller with `003E6DA0`, and calls the
applier `003E37F0` with the command record. (`003E6DA0`, 67 B: the controller is `00370E20` of the record's resource
entry - index `+0x18` in the table at `+0xD98` of the record's resolved base - and null when the index is -1 or the
entry does not resolve, in which case the record is skipped.) It does the same for the record's first child (`+8`), then walks that
child's two chains (`+8` and `+0xA`) depth-first with the callback `0042D970` (72 B: the same busy test, controller
fetch and apply, taking the command from the owner passed in its context), so the same command reaches every record
it visits. **An attached piece looks where its owner looks.**

**Clear.** `003E37E0` (11 B) zeroes the `0x50` bytes. A command is consumed by one pass.

## 3. The request word

Read from the applier `003E37F0` (909 B) branch by branch, and matched to the builder that sets each bit:

| request bit | value / payload | what the applier does | staged by |
|---|---|---|---|
| 0 | bit 22 | `003E0910` `(controller, value)` | `003E0B20` - verb **`denybonephysical`** |
| 1 | bit 23 | controller `+0x1C` bit 0 := value; value 1 calls `RelationLook_SetAcceptedRelationState`, value 0 `RelationLook_BeginNeutralReturn` - **look on / look off** | `003E33E0` |
| 2 | bit 24 | low nibble of controller `+0x1D` := value | `003E3440`. *The immediate, unstaged writer of the same nibble is `003E3400` (57 B, read whole 2026-09-19): it resolves the controller from the encoded pointer at `+8` of its first argument and replaces the nibble at once, doing nothing when the controller does not resolve* |
| 4 | bit 26 | low nibble of controller `+0x1E` := value | `003E37C0` - verbs **`lookat_maxangle_limit_lock`** / **`_unlock`** |
| 5 / 6 | - | controller `+0x8C` := 1 / := 0 | no builder among the eighteen |
| 9 with 10 | three dwords at `+0x20` | controller `+0x60`, `+0x64`, `+0x68`; source kind `+0x6C` := 0 | `003E36F0` (bits only) |
| 9 with 11 | two dwords at `+0x20` | controller `+0x60`, `+0x64`; `+0x6C` := 1 | `003E36C0` - verb **`lookatsrcboneid`** |
| 12 with 13 | three dwords at `+0x30` | controller `+0x50`, `+0x54`, `+0x58`; source kind `+0x5C` := 0 | `003E36F0` (bits only) |
| 12 with 14 | two dwords at `+0x30` | controller `+0x50`, `+0x54`; `+0x5C` := 1 | `003E36C0`, the same two values as above |
| 15 | floats `+4`, `+8`, `+0xC` | `003E2FD0` `(controller, frames, a, b)` | `003E31E0` |
| 17 | same | `003E30A0` - the same, with a minimum duration | `003E3120` |
| 16 | same | `003E3200` `(controller, frames, a, b)` | `003E3320` |
| 18 | same | `003E3140` - the same as 16, with a minimum duration | `003E31C0` |
| 19 | float `+4` | `CharacterRender_BeginRelationLookBlend(controller, frames)` | `003E33C0` |
| 20 | float `+4` | `CharacterRender_BeginRelationLookBlendWithMinimumDuration` | `003E33A0` |
| 27 | floats `+0x40`..`+0x48` | `003E2810` `(controller, x, y, z)` | `003E29D0` - verb **`eyemove_381`** |
| 28 | same | `003E28F0` | `003E29B0` - verb **`eyemovediff_383`** |
| 29 | - | zeroes `+0x2C`, `+0x14`, `+0x18` of the object at controller `+0x28` | `003E2800` - verb **`eyemovereset`** |
| 30 | bit 31 | `003E3720` `(controller, value)`: bit 5 of controller `+0x1C` := value; if it is now up and bit 0 (look on) is down, `RelationLook_BeginNeutralReturn` | `003E37A0` |

Bits 15 to 20 are one group - the applier tests them in the order 15, 17, 16, 18, 19, 20 and takes the first - and
each of their builders clears the others. Bits 27 and 28 exclude each other the same way. Two builders stage bits the
applier never tests: `003E36A0` (bit 7, floats at `+0x10` / `+0x14`) and `003E3570` (bit 8, floats at `+0x18` /
`+0x1C`), both called only from the bind path `002E28E0`; their reader, if any, is not this applier.

**The angle setters.** `003E2FD0` stores the two angles at controller `+0x50` / `+0x54` and sets both
source kinds to **2**; `003E3200` sets them to **3** and converts: the first angle, divided by 2 pi and scaled to
`0x8000`, indexes the engine's sine table at `01F004E0` for controller `+0x60` and (offset by a quarter turn) `+0x68`,
with `+0x64` zeroed - a unit direction in the horizontal plane. Both set the blend rate `+0x74` to `1 / frames` (or to
`[01DFE0BC]` when frames is 0), raise `+0x88`, clear the high nibble of `+0x1E`, save the controller's `+0x10` / `+0x14`
to `+0x78` / `+0x7C`, and set `+0x3C` when the global `01F82E38` is non-zero. So the source kind is
**0 a vector, 1 a pair of bone ids, 2 a pair of angles, 3 a direction made from an angle**.

**The blend starters and the minimum duration.** `CharacterRender_BeginRelationLookBlend` (`003E2F30`, 147 B) changes no
source: it raises `+0x88`, zeroes the progress at `+0x70`, sets the rate `+0x74` and does the same saving and clearing as
the angle setters - *blend to whatever the controller is already aimed at, over this many frames*. The three
*minimum-duration* variants - `003E3340` for the plain blend, `003E30A0` for kind 2, `003E3140` for kind 3 - are one
line each around their plain sibling: `frames = max(frames, [01DFE0B8] * controller[+0x18])`. **That is the whole
difference between selector 1 and selector 2 of section 4: selector 2 will not let a look be quicker than the
controller's own floor.**

## 4. Where the head-look requests come from

`002EC3F0` (263 B) turns the actor's **steering record** into a staged look. It runs only for an actor whose byte `+3`
has `0x60` in its top three bits, reads the steering record `[[actor + 0xB8] + 0xF0]`, takes the look shape from bits
0-2 of its byte `+0x62` and a selector from bits 3-5 (a selector of 2 becomes 1 when bit 0 of `+0x6A` is up; that bit
is then cleared), and tail-jumps to one of six services, passing the frame count from the word `+0x60` and, for the
angle shapes, the pair at `+0x10` / `+0x14`:

| shape (bits 0-2) | selector 1 | selector 2 |
|---|---|---|
| 0 or 1 | `002E7650` - request bit 19, plain blend | `002E79A0` - bit 20, the same with a minimum duration |
| 2 | `002E7720` - bit 15, two angles | `002E77F0` - bit 17, the same with a minimum duration |
| 3 | `002E78D0` - bit 16, direction from an angle | `002E7860` - bit 18, the same with a minimum duration |

Any other selector does nothing. Its five callers are the bind and resume chain of
[the two steering slots](../../06-Movement-And-Navigation/Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md)
(`002E28E0`, `002E3110`, `002E64E0`, `002EAAA0`, `002EBE50`), which is where the `lookat*` verbs arrive. So **the body
turn and the head look are two consumers of one steering record**: the resume switch that page describes ignores
shapes 2 and 3, and this function is where those shapes are used.

## 4a. What the command is applied to: the character's rig of controllers

The object `003E6DA0` returns - the applier's first argument, called *controller* in the table above for brevity - is
not the look controller itself. It is a **rig**: a small table of 32-bit encoded pointers, one per per-character
controller, each resolved with `ImageAddress_ResolveRuntimePointer` every time it is used. The **look controller is the
rig's slot `+8`** (every `controller +0x..` offset in section 3 is an offset into that object) and the **eye object is
slot `+0x28`** (request bits 27 to 29 go there).

`CharacterRender_RebindCombatLookAndSkeletonResources` (`003E3D70`, 961 B; one caller, `00372350`) shows the whole rig,
because it resets every slot in turn:

| rig offset | reset called | what is known of the slot |
|---|---|---|
| `+0x00` | `0040F390`, then `0040B5D0` with mode 1 (mode 4 when the global `02B59D64` is non-zero) | - |
| `+0x04` | `00512AD0`, then `00512C00` | **bone physics** - one of the two slots `denybonephysical` restarts |
| `+0x08` | `RelationLook_ResetControllerState` | **the look controller** |
| `+0x0C` | `00515DA0` | - |
| `+0x14` | `0051AFD0`, then `0051B110` | - |
| `+0x18`, `+0x1C` | `00471660`, `004715B0` | - |
| `+0x20` | `005173B0`, then `00517590` | - |
| `+0x24` | `005175F0` | - |
| `+0x28` | `00518E60` | **the eye object** |
| `+0x2C` | `00519730`, then `00519870` | - |
| `+0x30`, `+0x34` | `004712F0`, `004719F0` | - |
| `+0x38` | `00519A30`, then `0051A320` | **bone physics**, the other slot `denybonephysical` restarts |
| `+0x3C`, `+0x40` | `00472820`, `0051B870` | - |

*Named further 2026-09-19:* [the rig of seventeen controllers](the-rig-of-seventeen-controllers.md) follows who
*enables* each slot and names five more - `+0x0C` the Confuse motion, `+0x18` the Float bob, `+0x1C` the Immobilize
motion, `+0x24` the lip flap, `+0x34` the nod, `+0x3C` the head shake - and `+0x00` is the per-model sway.

Before the resets it re-resolves the rig's two linked render records: the record indices at `+0x68` and `+0x6C` become
encoded record pointers at `+0x70` / `+0x74` (null for index -1 or a dead record) and their skeleton bone arrays
(`CharacterRenderRecord_ResolveSkeletonBoneArray`) at `+0x78` / `+0x7C`; then
`Skeleton_ResetConfiguredAdditiveBoneMatrices`. After them it restores the rig's own state: `+0x58` := 0, `+0x5C` :=
`0x0101`, `+0x5E` := 0, bit 0 of `+0x5F` cleared, `+0x60` := 0 - and then `+0x60` := 30 if slot 0's mode call
returned non-zero.

**Where the rig hangs, and the small resets, read.** The rig is the encoded pointer at **`+0x94` of the character's
resource entry** (`00370E20`, 11 B, is that one load and a resolve), with a count at `+0x90`. The rebind's only caller,
`00372350` (84 B), is given a resource entry and a render-record index: if the count is positive and the rig resolves it
stores the index in the rig's `+0x68` - the first linked record - and calls the rebind. Of the slot resets, the ones
under 128 bytes were read so that naming them here says something: `00512C00` (slot `+4`, second phase) captures a rest
state once - if bit 0 of its byte `+0x35` is clear it copies a vector from `+0x140` and three dwords from `+0x120` of the
bone object behind its `+0x38`, then sets bits 0-2 of `+0x35`; `0051A320` (slot `+0x38`) sets its byte `+0x30`, zeroes
four fields and copies `+0x140` and `+0x148` of its bone object to `+0xB0` / `+0xB4`; `0051B110`, `00519870` and
`00517590` are one-store *re-initialise me* flags (bit 0 of `+0x15`; byte `+6`; word `+0xA6` and byte `+0xA4`);
`00471660`, `004715B0` and `004712F0` zero a handful of fields and store the constant `{0, 0, 0, 1}` from `01EF93F0` at
`+0x20` - an identity rotation - the first also setting `+4` to `1.0` and its byte `+2` to `[01F223A8] - 1`; `005175F0`
clears the high nibble of its byte `+1` and five fields.

**`denybonephysical` - `003E0910`** `(rig, deny)` (154 B) stores the flag in the rig's byte `+0x62` and does nothing more
when the value is unchanged or is being set. **When the deny is lifted** it resets and re-initialises the two bone-physics
slots (`+4`: `00512AD0`, `00512C00`; `+0x38`: `00519A30`, `0051A320`) - physics resumes from rest, not from wherever the
bones were frozen.

**`eyemove_381` - `003E2810`** `(rig, frames, x, y)` (215 B) writes the eye object: the timer `+0x2C` := frames, and a
per-frame velocity `+0x1C`, `+0x20` := (target - current) / frames, the current pair being `+0x14`, `+0x18`. A frame count
under 1 becomes `[01DFE0B8]`, and when the global `01F82E38` is non-zero the timer is stored **negated**.
**`eyemovediff_383` - `003E28F0`** (184 B) is the same with the pair taken as a displacement instead of a destination
(no subtraction of the current pair). `eyemovereset` (request bit 29) zeroes the timer and the current pair.

**The controller's reset - `005154B0` (329 B, read whole 2026-09-19).** It clears the request side of the controller -
the mode nibble of `+0x1D`, the qword `+0x10`, the dword `+0x8C`, the qword `+0x38`, the word `+5`, the bytes `+7` and
`+0x1C` - and sets the word `+0x1E` to `0x11`, **1 in both nibbles of the byte the limit verbs write**. Then it rewinds
every **bone entry** (count in byte `+4`; array at the resolved pointer of `+0`, plus 8; stride `0x60`): the entry's
byte `+0x14` is cleared, **its first dword becomes one of the values it stores from `+0x48` on, picked by the
controller's byte `+6`**, and its three vectors at `+0x18`, `+0x28` and `+0x38` are zeroed. So a reset returns each bone
to the stored value of the current variant and forgets what it had accumulated. Four callers, none read here: two
small bodies, a third near the appliers, and the rebind of the combat look and skeleton resources. *What the three
vectors accumulate, and what byte `+6` selects between, were not established.*

| body | anchors |
|---|---|
| `005154B0` look controller reset (329 B) | `005154BA`, `005154C0`, `005154C7`, `005154CD`, `005154D4`, `005154DA`, `005154DE`, `005154E4`, `00515598`, `0051559A`, `0051559F`, `005155B0`, `005155B8`, `005155BE`, `005155C2`, `005155C5`, `005155D0`, `005155DB`, `005155E6` |

## 5. Behaviour a reimplementation must keep

1. Requests are staged and applied once per dirty-state pass; a second request of the same group before the pass
   replaces the first, because each builder clears its group.
2. The applied command fans out to every attached record beneath the owner.
3. A busy record (`00426220`) is skipped, not deferred - the command is cleared regardless.
4. `look off` is not an absence of look: it starts the controller's neutral return.

## 6. What is not known

- What the look controller and the eye object do each frame with the state these setters leave.
- What thirteen of the rig's sixteen slots are (section 4a names the look controller, the eye object and the two
  bone-physics slots; the reset functions of the others were not read), what the rig's own fields `+0x58`..`+0x62`
  mean beyond the deny flag, and what the global `02B59D64` selects.
- What the controller's `+0x18` (the minimum-duration floor) and the global scale `01DFE0B8` are.
- What bits 2, 5, 6 and 30 mean in the game's vocabulary (bit 30's effect is read - a second way into the neutral
  return - its name is not); bits 5 and 6 have no stager among the eighteen builders.
- Who reads staged bits 7 and 8.
- What `00426220` tests, and what the global `01F82E38` is.
- Static evidence throughout.

## 7. Evidence

| claim | source | tier |
|---|---|---|
| the request word | `003E37F0` read whole; the eighteen builders read | 1 |
| eighteen forwarders | pattern search over 38,161 listed bodies returns 18 | 1 |
| the verb names | members census joined to `scriptvm-verb-table.tsv` | 1 |
| the fan-out to children | `00429920` read whole | 1 |
| the shape / selector table | `002EC3F0` read whole | 1 |

## 7a. Where each behaviour is in the bytes

| body | what is there | at |
|---|---|---|
| `003E37F0` applier (909 B) | bit 4 and its value bit 26 into `+0x1E` | `003E3811`, `003E381A`, `003E3837` |
| | bit 9: three dwords (bit 10) or two (bit 11) | `003E384E`, `003E3872`, `003E38AF` |
| | bit 12: three dwords (bit 13) or two (bit 14) | `003E38BF`, `003E38E3`, `003E3920` |
| | the target group, tested 15, 17, 16, 18, 19, 20 | `003E393A`, `003E395C`, `003E397B`, `003E399A`, `003E39B9`, `003E39CE` |
| | bits 5 and 6 into `+0x8C` | `003E39E3`, `003E39FF`, `003E3A27` |
| | bit 2 / 24 into `+0x1D`; bit 0 / 22 | `003E3A30`, `003E3A55`, `003E3A5F`, `003E3A6D` |
| | bit 1 / 23: `+0x1C`, accepted state or neutral return | `003E3A74`, `003E3A9C`, `003E3ABF`, `003E3AD6` |
| | bit 30 / 31; bits 27, 28; bit 29 | `003E3AE2`, `003E3AFA`, `003E3B19`, `003E3B38`, `003E3B55` |
| `00429920` apply and fan-out (299 B) | owner record, busy test, controller, apply | `0042995F`, `00429970`, `0042997C`, `00429995` |
| | first child; the two depth-first walks; clear | `004299E3`, `004299FE`, `00429A19`, `00429A2D` |
| `002EC3F0` dispatcher (263 B) | actor class test; shape and selector; the `+0x6A` rule | `002EC3F9`, `002EC40F`, `002EC424`, `002EC433` |
| | six tail jumps | `002EC47B`, `002EC481`, `002EC4AD`, `002EC4B3`, `002EC4D7`, `002EC4F1` |
| `003E2FD0` angles, kind 2 (195 B) | kinds, rate, the global, saved pair | `003E301B`, `003E3023`, `003E3053`, `003E3058`, `003E3068` |
| `003E3200` direction, kind 3 (280 B) | sine-table lookups, kinds, rate | `003E3291`, `003E32AA`, `003E3259`, `003E3265`, `003E32D8` |
| `003E3D70` rig rebind (961 B) | the two linked records and their bone arrays | `003E3D7E`, `003E3DB9`, `003E3DC4`, `003E3DD5`, `003E3E0D`, `003E3E25` |
| | additive-bone reset; first slot resets | `003E3E2B`, `003E3E46`, `003E3E63`, `003E3E80` |
| | rig state defaults; slot 0 mode 1 or 4 | `003E4000`, `003E4013`, `003E4027`, `003E4042`, `003E4050` |
| | second-phase initialisers | `003E407E`, `003E40A8`, `003E40D2`, `003E40FC`, `003E4126` |
| `003E0910` deny bone physics (154 B) | flag compare and store; only the lift does work | `003E0925`, `003E0929`, `003E092C` |
| | the two slots restarted | `003E0948`, `003E0965`, `003E0982`, `003E099F` |
| `003E2810` eye move (215 B) | frame floor, the global, timer, the two velocities | `003E285B`, `003E286C`, `003E2884`, `003E28A4`, `003E28CA` |
| `003E28F0` eye move by displacement (184 B) | the same without the subtraction | `003E2937`, `003E2948`, `003E2960`, `003E297A`, `003E2987` |
| `003E2F30` plain blend (147 B) | active flag, progress zeroed, rate, the global, saved pair | `003E2F60`, `003E2F6D`, `003E2F8E`, `003E2F93`, `003E2FA3` |

## 8. Related

- [The character render record array](the-character-render-record-array.md)
- [How a character fades - the ten channels](how-a-character-fades-the-ten-channels.md) - the neighbouring bytes of
  the same record, and the same global `01F82E38`.
- [The two steering slots](../../06-Movement-And-Navigation/Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md)

## Cross-subsystem neighbours

**Movement - SHARED RECORD.** `002EC3F0` reads the steering record this page links to; the steering page owns the
record and its writers, this page owns what the head look makes of its shape.

**Script VM - SERVICE.** The verbs named in section 3 reach the builders through the actor-service layer; they are
named here by verb, and nothing on this page calls back into the script layer.

**Core runtime scheduling - SERVICE.** The angle setters `003E2FD0` and `003E3200`, the blend starter and the eye
functions `003E2810` / `003E28F0` each call the getter `001EDE70`, which returns the global dword `01F82E38`; a one-way
read of one value, the same one the fade channels read.

**Resource - SERVICE.** The controller getter `003E6DA0` resolves its object through
`ResourceTable_ResolveEntryByIndex` (`002ED570`); when the entry does not resolve the getter returns null and
`00429920` skips the applier for that record.

**World / area / field - INCIDENTAL.** The bind path `002E28E0`, cited here only as a caller of the dispatcher and of
three builders, also calls the field-owned `00377C20`. That call is the bind path's business and no part of the look
command; the edge is recorded because the caller is named.

**Gameplay - CLIENT.** `00203170`, ~~the per-slot visitor this page's `003E3C30` section names~~ *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's auditsem-review-p22-fable-0930 §2 N1 / AUDITSEM-CONTRA-FABLE-STAGED-LOOK-00203170-0930:)* the 44-byte identity-matrix store (four 16-byte identity rows to `[rcx]`..`[rcx+0x30]`) that this page's per-slot visitor `003E3C30` applies once per slot (`003E3C7A`), is also
called by `00339630`, a Gameplay-layer body. The page uses `00203170` only as the staged-look record's
~~per-slot routine~~ per-slot identity-matrix store; the Gameplay call is that layer's business.

**UI - CLIENT.** The same `00203170` is called by seven UI-layer bodies (`00247AE0`, `002D2600`,
`002D28E0`, `00368010`, +3 more) - one shared ~~per-slot routine~~ *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's auditsem-review-p22-fable-0930 §2 N1:)* identity-matrix store serving the UI's own record walks; no UI
state is owned here.

## SWE2-EC7-49 update (2026-09-19) - `002E7650`

`002E7650` (196 B) is the request-bit-19 plain-blend body - `003E6BB0`/`003E6C00`. Interior anchor `002E76A0` (an `003E6BB0` call).

## SWE2-EC7-52 update (2026-09-19) - `0040F390`

`0040F390` (2900 B) is the staged-look stage-0 head - `byte[rcx+5]` gate, `and byte[rcx+0x3F],0xF`, `0020E600` sextuple plus `00861EC0`, `022D91D0`/`022D91E0`/`01EF93F0` tables. Interior anchor `0040F3A6` (a `0020E600` call).

## SWE2-EC7-53 update (2026-09-19) - `00515DA0`

`00515DA0` (574 B) is the staged-look `+0x0C` slot body - `0020E600` plus `01EF93E8`/`01EF93F0`/`022D8F90`/`022D9138`/`022D915C` state. Interior anchor `00515DAB` (a `0020E600` call).


## SWE2-EC7-53 update (2026-09-19) - `005173B0`

`005173B0` (465 B) is the staged-look `+0x20` slot reset, call-free - `+0xA0=1.0f`, `+0xA5` masked `0xC1`, `+0x80`/`+0xA4`/`+0xA6` cleared, `01EF93F0` vector published into `022D91B0`-`022D91DC` component-wise. Interior anchor `005173DE` (the first `022D91BC` store).


## SWE2-EC7-53 update (2026-09-19) - `0040B5D0`

`0040B5D0` (428 B) is the staged-look mode-1/mode-4 update the dispatch names - `0020E600`/`0040ED90`. Interior anchor `0040B5FE` (a `0020E600` call).

## SWE2-EC7-54 update (2026-09-19) - `00519730`

`00519730` (306 B) is the staged-look `+0x2C` slot body - `0020E600` plus `01EF93F0`/`022D91B0`-band state. Interior anchor `005197F3` (a `0020E600` call).


## SWE2-EC7-54 update (2026-09-19) - `0051AFD0`

`0051AFD0` (305 B) is the staged-look `+0x14` slot body - `0020E600` plus `01EF93F0`/`022D91B0`-band state. Interior anchor `0051AFEA` (a `0020E600` call).


## SWE2-EC7-54 update (2026-09-19) - `00472820`

`00472820` (302 B) is the staged-look `+0x3C`/`+0x40` slot reset, call-free - `01EF93F0` vector published into `022D91B0`-`022D91DC` component-wise (sibling skeleton of `005173B0`). Interior anchor `00472839` (the `022D91B0` store).


## SWE2-EC7-54 update (2026-09-19) - `00519A30`

`00519A30` (298 B) is the staged-look `+0x38` bone-physics slot reset, call-free - `01EF93F0` vector published into `022D91B0`-`022D91DC` component-wise (sibling skeleton of `005173B0`). Interior anchor `00519A49` (the `022D91B0` store).


## SWE2-EC7-54 update (2026-09-19) - `00512AD0`

`00512AD0` (297 B) is the staged-look `+0x04` bone-physics slot body - `0020E600` plus `01EF93F0`/`022D91B0`-band state. Interior anchor `00512AE9` (a `0020E600` call).


## SWE2-EC7-54 update (2026-09-19) - `004719F0`

`004719F0` (291 B) is the staged-look `+0x30`/`+0x34` slot body - `0020E600` plus `01EF93F0`/`022D91B0`-band state. Interior anchor `004719FB` (a `0020E600` call).

## SWE2-EC7-55 update (2026-09-19) - `00518E60`

`00518E60` (237 B) is the staged-look `+0x28` eye-object slot reset, call-free - `022D91B0`-`022D91DC` band republished component-wise into `[rcx+0x30]`+. Interior anchor `00518E85` (the `022D91B0` store).

## SWE2-EC7-56 update (2026-09-19) - `0040ED90`

`0040ED90` (219 B) is the staged-look bone-flag selector the page names (`+28A`/`+28B` bytes) - `0020E600` single call. Interior anchor `0040EDA8` (a `0020E600` call).


## SWE2-EC7-56 update (2026-09-19) - `0051B870`

`0051B870` (217 B) is the staged-look `+0x3C`/`+0x40` slot reset, call-free - `022D91B0`-`022D91DC` band republished component-wise into `[rcx]`/`+0x10`/`+0x30`. Interior anchor `0051B8AC` (the `022D91B0` load).


## SWE2-EC7-72 update (2026-09-19) - `0051A320` + `00512C00` context-snapshot inits measured

`0051A320` (72 B) resolves `0020E600([+0x34])` -> `[rax]` and snapshots:
`+0x30` = 1, `+0x70`/`+0x78`/`+0x3C`/`+0xCC` zeroed, `[rdx+0x140]` ->
`+0xB0`, `[rdx+0x148]` -> `+0xB4` - the staged-look record's init.
Interior anchor `0051A34A` (the `[rdx+0x140]` copy).

`00512C00` (79 B) is the lazy sibling: `0020E600([+0x38])` -> `[rcx]`,
and only when `byte[+0x35]` bit 0 is clear copies the `[+0x140]` 16-byte
row to `[rbx]`, `[+0x120..+0x128]` to `+0x10..+0x18`, and sets
`+0x35 |= 7`.
Interior anchor `00512C24` (the `+0x35 |= 7` flag commit).

## SWE2-EC7-73 update (2026-09-19) - `003E3C30` indexed-table sweep measured

`003E3C30` (109 B) is the per-index table sweep: `0020E600([+0x88])`
yields the index array `rbx`; for `edi` under `[+0x8C]` it resolves
`0020E600([+0x78])`, computes `rax + 0x230 + [rbx] * 0x290`, and calls
`00203170` on it, stepping `rbx` by 4 - the staged-look record's
bounded per-slot visitor.
Interior anchor `003E3C7A` (the `00203170` per-slot call).

## SWE2-EC7-82 update (2026-09-20) - `00517590` flag pair measured

`00517590` (19 B) is the two-field setter the staged-look caller
runs: `word[rcx+0xA6] = 1` and `byte[rcx+0xA4] = 1` - the mark pair,
no calls.
Interior anchor `00517595` (the `+0xA6` store).

## SWE2-EC7-87 update (2026-09-20) - `003E37E0` fixed-arg forward measured

`003E37E0` (11 B) is the fixed-arg tail the staged-look callers
run: `00861EC0(rcx, 0, 0x50)` - the record, a zero mode and a
0x50 size forwarded unchanged.
Interior anchor `003E37E6` (the `00861EC0` tail).

## SWE2-EC7-107 update (2026-09-20) - `002435C0` measured

`002435C0` (664 B) is the
tagged-entry dispatch loop
`00245E60`, `002D28E0` and
`00562850` run: `word[rdx + 0x58]`
gates the pass, the `dword[rcx]` field must have
`& 0x3FFFC` nonzero and
`(dword[rcx] >> 2) & 0xFFFF`
counts the `[rcx + 0x10]` entries,
and each entry's `dword[+8] >> 2 &
0xF` selects an arm - `0029F5D0`,
`0029ED30`, `0029FBD0`, `0029ED50`,
or the `0xC`-count `002D9C40` /
`002D9380` record path (class 9 also
swaps `word[rsi + 0x5A]` for `0x80`
around its `0029F5D0` call) that decodes
`dword[+8]`'s packed halves into the
`[+0x20]`-indexed word table and the
`byte[+0x39]` nibble table
(`byte[rsi + 0x5C]` written exactly
as `00244070` writes it) - the
staged emit list the look-command
walks.
Interior anchor `00243626` (the
`dword[+8]` tag test).

## SWE2-EC7-108 update (2026-09-20) - `0029FBD0` measured

`0029FBD0` (591 B) is the
`002D8910`-emitting record composer
`002435C0`'s class-5 arm and
`00276D30` run: `[rcx + 0x18]` null
short-circuits; `byte[+0x2D]` /
`[+0x2F]` / `(dword[+8] << 0x10) >>
0x16` / `dword[+0x28]` / `byte
[+0x2C]` stage into `+0x64`..`+0x66`
/ `+0x60` / `+0x5C`, `dword[+0x24]`
mirrors to `+0x90` when `[rdx+0x5C]
& 0x40000` is clear, and `byte[+8]
& 2` posts `0x80` to `word[+0x5A]`.
`byte[+0x2D] & 0x38` swaps the width
source to `word[+0xA]`, and `& 4`
runs the glyph-box pass -
`0020E600(dword[+0x20])` then
`002D8B00([+0x18], &rect, table,
&rect2, ebx)`, the result clamped
against the `word[+0xC..+0x12]` /
`[rsi + 0x48..0x4E]` fields scaled
by `float[+0x28]`, `00249FD0` on a
non-empty clip, and a `0208F574`-
seeded `& 0xFFC0` xor-fold into
`dword[+8]` when the computed width
overflows `word[+0x10]` - before
`002D8910(rsi, ebx, [+0x18],
table, word[+0xE])` emits and
`byte[+0x2D] & 4` tails
`002D8530(rsi)`.
Interior anchor `0029FC8C` (the
`002D8B00` call).

`002D9380` (1915 B) is the sprite-quad record composer behind `002435C0`'s class-9 record path and the licence-board `0055AB20`/`0055AE80` draws: `[arg]+0x0..0x6` sign-extended `{x, y, w, h}` split into the three corner sums; `[r15+0x5C]` bit 0x10 picks between a masked `0x6878...`-OR'd header and the `[rsi+0x38] & 0x3F00` class switch — class `0x1400` emits a type-6 record packing `(flags>>4 & 0xF) << 0x25 | (+0x30 & ~0x2C00000 | 0x1300000)` plus a type-0x16 record carrying `+0x5C & 0xF << 0x38`, class `0x1300` packs `+0x5C` bit 0x13 into the same type-6 slot, anything else emits `+0x30` raw; then a type-8 record packs the four edge coords `{(y+h-1), y, (x+w-1), x}` at 10-bit fields shifted left 4 with tag `0xA` (`(((y+h-1)<<0xA | y)<<0xA | (x+w-1))<<0xA | x)<<4 | 0xA`), four `{r,g,b,a}` byte-quads are lifted from the `[r9]` 16-byte table interleaved with `{r9d, r11d, +0x70}` triples, and the back half builds the 8-corner vertex block — each corner `00202B70`-transformed with UVs `divss`-normalized by the `+0x6C`/`+0x7C` divisors — before `00181890` emits and `002D9AAF`/`001813F0` close. One call draws one textured quad end to end.

Interior anchor `002D943D` (function `002D9380`).

`003E3340` (86 B) is the clamped-scale forwarder `003E29F0`/`003E37F0` call: `0020E600([rbx+8])` resolves twice, `1.0f * [rdi+0x18]` is `maxss`-floored at the caller's xmm argument, then `003E2F30` runs - the look command's scale-clamp shim.

Interior anchor `003E3381` (function `003E3340`).

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives

**Attack.** Sections 2 to 4 and section 7a's sizes became checks at their instructions. The eighteen forwarders were
found by an image-wide pattern search, and the dispatcher's callers by a raw E8/E9 sweep. Script:
`Tools/analysis-kit/gfz-scripts/falsify_staged_look.py`, output `falsify_staged_look.out`, image `73461d08…`, 0 BROKEN,
exit 0. The per-bit applier table beyond the target group, and the verb joins, are carried.

| # | Clause attacked | Result |
|---|---|---|
| L0 | section 7a sizes | **survives**: all fourteen |
| L1 | section 2 | **survives**: exactly eighteen `add rcx, 0x580; jmp` forwarders, to eighteen distinct builders |
| L2 | section 2 | **survives**: the clear zeroes `0x50` bytes through the memset |
| L3 | section 3 | **survives**: the target group is tested 15, 17, 16, 18, 19, 20 (`bt`) at the six cited sites |
| L4 | section 3 | **survives**: kinds 2 and 3 at `+0x5C` / `+0x6C`, the sine table `01F004E0`, the rate `+0x74` and `01DFE0BC`; `+0x3C` is set behind the 7-byte getter `001EDE70` (`mov eax, [01F82E38]`) |
| L5 | section 3 | **survives**: all three minimum-duration variants read `[01DFE0B8]` and controller `+0x18` and take a max |
| L6 | section 4 | **survives**: six tail-jumps (two conditional) to exactly the six services; the five callers as named |

No correction.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-staged-look-command-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00372350` | 84 B | when the signed dword `+0x90` of `rcx` is greater than 0 and `0020E600(dword +0x94)` is non-null, stores `edx` to dword `+0x68` of the object a second `0020E600(dword +0x94)` call returns and then calls `003E3D70` with the result of a third `0020E600(dword +0x94)` call; otherwise it does nothing | `0037235A`, `00372366`, `00372376`, `00372383`, `00372394` |
| `003E0B20` | 19 B | replaces bit 22 of dword `[rcx]` with bit 0 of `edx`, sets bit 0 and stores the dword back | `003E0B25`, `003E0B2D`, `003E0B30` |
| `003E29B0` | 28 B | clears bit 27 and sets bit 28 of dword `[rcx]`, then stores `xmm1`, `xmm2` and `xmm3` to the floats at `+0x40`, `+0x44` and `+0x48` | `003E29B6`, `003E29BC`, `003E29C1`, `003E29C6` |
| `003E29D0` | 28 B | clears bit 28 and sets bit 27 of dword `[rcx]` and stores `xmm1`, `xmm2` and `xmm3` to the floats at `+0x40`, `+0x44` and `+0x48` | `003E29D2`, `003E29DB`, `003E29E4`, `003E29D6`, `003E29E6` |
| `003E30A0` | 122 B | calls `0020E600(dword +8 of rcx)` twice and, when the second result is non-null, calls `003E2FD0(rcx, x, xmm2, xmm3)` where `x` is the larger of `xmm1` and float `+0x18` of the first result multiplied by 1.0 (`01DFE0B8`); when the second result is null it does nothing | `003E30DD`, `003E30EA`, `003E30F5`, `003E30FA` |
| `003E3140` | 122 B | calls `0020E600(dword +8 of rcx)` twice and, when the second result is non-null, calls `003E3200(rcx, x, xmm2, xmm3)` where `x` is the larger of `xmm1` and float `+0x18` of the first result multiplied by 1.0 (`01DFE0B8`); when the second result is null it does nothing | `003E317D`, `003E318A`, `003E3195`, `003E319A` |
| `003E33C0` | 19 B | clears bits 15 to 18 and 20 of dword `[rcx]` (AND `0xFFE87FFF`), sets bit 19 and stores the dword back, and stores `xmm1` to the float at `+4` | `003E33C2`, `003E33CC`, `003E33D0`, `003E33C7` |
| `003E3400` | 57 B | when `0020E600(dword +8 of rcx)` is non-null, replaces the low nibble of byte `+0x1D` of the object a second `0020E600(dword +8)` call returns with the low nibble of `edx` (high nibble kept); otherwise it does nothing | `003E341A`, `003E3424`, `003E3427`, `003E342B` |
| `003E3570` | 17 B | sets bit 8 of dword `[rcx]` and stores `xmm1` and `xmm2` to the floats at `+0x18` and `+0x1C` | `003E3576`, `003E357B` |
| `003E36A0` | 17 B | sets bit 7 of dword `[rcx]` and stores `xmm1` and `xmm2` to the floats at `+0x10` and `+0x14` | `003E36A6`, `003E36AB` |
| `003E36C0` | 46 B | when `edx` is 0, clears bit 10 and sets bits 9 and 11 of dword `[rcx]` and stores `r8d` and `r9d` to dwords `+0x20` and `+0x24`; otherwise clears bit 13 and sets bits 12 and 14 and stores `r8d` and `r9d` to dwords `+0x30` and `+0x34` | `003E36C4`, `003E36CA`, `003E36CE`, `003E36DE`, `003E36E2` |
| `003E36F0` | 48 B | when `edx` is 0, sets bits 9 and 10 and clears bit 11 of dword `[rcx]` and copies the 16 bytes at `r8` to `+0x20`; otherwise sets bits 12 and 13, clears bit 14 and copies the 16 bytes at `r8` to `+0x30` | `003E36F4`, `003E36F6`, `003E3705`, `003E370B`, `003E371A` |
| `003E3720` | 115 B | calls `0020E600(dword +8 of rcx)` twice and, when the second result is non-null, replaces bit 5 of byte `+0x1C` of the first result with bit 0 of `dx`; when that bit is then set, bit 0 of the byte is clear and a third `0020E600(dword +8)` call is non-null, it calls `00513150` with a fourth call's result; every other path does nothing more | `003E374B`, `003E3759`, `003E375F`, `003E3764`, `003E377E` |
| `003E37A0` | 27 B | rewrites dword `[rcx]` with bit 31 replaced by bit 0 of `dx` and bit 30 set (bits 0 to 29 kept) | `003E37A6`, `003E37AB`, `003E37B2`, `003E37B7` |
| `003E37C0` | 21 B | replaces bit 26 of dword `[rcx]` with bit 0 of `dx`, sets bit 4 and stores the dword back | `003E37C3`, `003E37C8`, `003E37CF`, `003E37D2` |
| `0042D970` | 72 B | calls `00426220(rcx, qword +8 of rdx)` and, when it returns 0 and `003E6DA0(rcx)` is non-null, calls `003E37F0` with that result and qword `+8` of `rdx` plus `0x580`; otherwise it does nothing | `0042D984`, `0042D98B`, `0042D998`, `0042D9A1`, `0042D9A8` |
| `004712F0` | 24 B | zeroes word `+2`, byte `+0` and qword `+0x18` of `rcx`, stores the four floats 0, 0, 0, 1.0 (`01EF93F0`) to `+0x20`..`+0x2C`, and returns 0 | `004712F9`, `004712FD`, `00471301`, `00471303` |
| `004715B0` | 23 B | zeroes word `+0` and qword `+0x10` of `rcx` and stores the four floats 0, 0, 0, 1.0 (`01EF93F0`) to `+0x20`..`+0x2C` | `004715B9`, `004715BE`, `004715C2` |
| `00471660` | 49 B | zeroes byte `+3`, qword `+0x14`, dword `+0x10` and word `+0` of `rcx`, stores the four floats 0, 0, 0, 1.0 (`01EF93F0`) to `+0x20`..`+0x2C` and `0x3F800000` (1.0) to dword `+4`, and stores byte `01F223A8` (0x1E in the image) minus 1 to byte `+2` | `00471669`, `0047166D`, `00471674`, `0047167D`, `0047168D` |
| `005175F0` | 23 B | clears the high nibble of byte `+1` of `rcx`, zeroes dwords `+0x10`, `+0x40` and `+0x4C`, and zeroes bytes `+2` and `+0` | `005175F6`, `005175F9`, `005175FC`, `005175FF`, `00517603` |
