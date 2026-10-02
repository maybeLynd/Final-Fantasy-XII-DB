---
system: How a camera reaches the renderer - eight submissions, one winner, one block of matrices
category: 17-Presentation-Rendering
status: DOCUMENTED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the submit function 003829D0 and the initialiser 00382910 disassembled whole; the camera update 003820C0
    read whole through its selection stage and by its calls and the addresses it hands them afterwards (stated in
    the text); writers of the eight slot flags and of the slot array found by rip-relative sweep; the three submit
    sites read for their priority constants; consumers of the matrices taken from pages that read them
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-camera-renderer-falsification-pass-1
  note: written by FABLE; founded on the matrix identifications made on the character-fade page the same day;
    pending first review
---

# How a camera reaches the renderer

Above this layer the game has cameras of many kinds - the field camera, the scripted camera player, the battle
camera - and [the scripted camera player](the-scripted-camera-player.md) describes how the camera system picks one
of its own records each frame. **This page is the layer underneath**: the renderer-side arbitration that takes
*whatever anyone submits this frame*, keeps the one with the highest priority, and turns it into the block of matrices
that the rest of the engine reads.

## 1. What the player sees

An effect file can carry its own camera, and when it does that camera wins over whatever the game's camera system
chose - priority 100 against 20 - for exactly the frames on which the effect submits it. The moment it stops
submitting, the game camera is back, with no hand-over logic anywhere: **submissions last one frame**.

## 2. Submitting - `003829D0` `(camera, priority)` (373 B)

A camera is a `0xD0`-byte record. The function looks through **eight slots of `0xE0` bytes** at `02AED630` for the first
whose *submitted* dword at `+0xD0` is zero, copies the record in, stores the priority at `+0xD4` and sets `+0xD0` to 1.
If all eight are taken the submission is dropped silently.

Before that, if a shared predicate reports true, it fetches three vectors from three sibling getters, negates one
component of the first and two of the second, and applies them to the caller's camera with `003CC000` - an override of
the submitted camera from a source that was not read. After it, `00259FA0` compares the record's address with the static
default view object `02097B80` and one of two wrappers is called (`001821F0` for the default view, `00182340` otherwise);
what those set is on
[the character transform publish contract](../CONTRACT-character-transform-publish.md).

**Three submitters exist in the image:**

| site | camera | priority |
|---|---|---:|
| `CameraSystem_SelectAndPublishActiveView` (`00259820`) | the active view behind the pointer `020972F0` | `0x14` |
| `00259970` (17 B), called by the frame body before its second draw | the static default view `02097B80` | `0x14` |
| `003ED8A0`, in the effect-file data parse | the effect's camera at `02096D30` | `0x64` |

## 3. Choosing - the first stage of `003820C0`

The camera update (2,125 B; one caller, a five-byte-call wrapper just below the graphics sync routines) first stores the **aspect ratio** from `00229D20` at `02AED4E0` and
`02AED540` (that 33-byte getter returns `1.3333` unless the mode byte `02064AD1` is 1, 2, 3 or 5, when it tail-calls the
device's own ratio - a first draft of this page called it the frame time, which reading the getter corrected), then walks the eight slots in order. For each slot whose *submitted* dword is 1 it **clears the dword** and
keeps the slot if its priority is **strictly greater** than the best so far (the best starts at -1). So the highest
priority wins, the **earliest** submission wins a tie, and every submission is consumed whether it won or not. With no
submission at all the function returns at once and **the matrices of the previous frame stand**.

The winner's `0xD0` bytes are copied into the working camera at `02AED560` (the block at `02AED4A0`, `+0xC0`).

`00382910` (163 B; one caller, the graphics start-up wrapper beside it) is the reset: it zeroes the eight *submitted* dwords, zeroes two offset
vectors at `02AEDF70` and `02AEDF80` and the pair at `02AEDF98` / `02AEDF9C`, sets their fourth components to `1.0`,
initialises two sub-blocks of the working camera (`004679C0`) and sets `02AEDFA0` to -1.

## 4. Building - the rest of `003820C0`

*Read instruction by instruction on 2026-09-19; the first issue of this page had it from its calls only.*

**The shake lands first, and this is what its two scalars are.** `02AEDF9C` is added to the working camera's `+0xC8`
(`02AED568`), and half of that sum goes through `tanf`, whose reciprocal is stored at `+0xD0` (`02AED570`): `+0xC8` is
the **field of view** and `+0xD0` the projection scale `1 / tan(fov / 2)` - oscillator 7 of a shake is a zoom pulse.
`02AEDF98` is added to `+0x184` (`02AED624`), the angle the camera rebuild takes beside eye and target - the **roll**;
oscillator 6. The position offset `02AEDF70` is rotated by the camera's own matrix at `02AED5C0` and added to the **eye**
at `02AED5F0` (the matrix's fourth row); the target offset `02AEDF80` is rotated the same way and added to the vector
that follows the matrix at `02AED600` - the **look-at point**, by the sampler's position / target pairing and the
rebuild that follows; `003CBD60` itself was not read. A
shake is therefore authored in the camera's frame - *left* is the camera's left, wherever it is facing - and
`003CBD60` then rebuilds the camera's matrices from the moved eye and target.

A **second copy** of the winning camera, made on the stack before any of this, gets the same offsets and the same
rebuild with one difference: its field of view is not the record's `+8` but the record's **`+0xC`** float - replaced
by `0.785398` (45 degrees) when that is above 1.0 - plus the shake. Its matrix becomes `02AEDEF0` and its projection
feeds `02AEDD70`, so **the matrix the character code reads as the camera's position and orientation comes from this
second copy, not from the working camera**. Eye, target and roll are treated identically in both, so the two
matrices should agree; what the second field-of-view float is for was not established.

A field-of-view adjustment (`001824E0`) is applied to the working camera and its projection scale recomputed; the
projection is built with the aspect ratio of section 3.

**The small bodies under it, read so that naming them says something.** `003CBA50` `(camera, out, aspect, k)` (114 B) is the
perspective projection: with `s = k x camera[+0x10]` it writes `out[0][0] = s / aspect`, `out[1][1] = s`,
`out[2][2] = -(near + far) / (far - near)`, `out[2][3] = -1`, `out[3][2] = -2 x near x far / (far - near)` and zeroes the
rest - so **the camera record's `+0` is the near plane and `+4` the far plane**. `003CBC40` `(camera, fov, near, far)`
(91 B) stores those and recomputes `+0x10`, writing the field of view to both `+8` and `+0xC`. `003B4150` (15 B) copies a
matrix to `02B40470`, a second classifier matrix beside the one the cull test installs. `00182570` (33 B) returns byte
`+0x1C` of the render device object, and `001824E0` (72 B) forwards the address of the field of view and two zeros to a
method of the same object.

Then, in order:

| matrix | how it is produced | what reads it |
|---|---|---|
| `02AEDDF0` (first) | `003CBB30` from the working camera's parameters at `02AED560` - a projection by its inputs | - |
| `02AEDD70` | the matrix at the head of the working block `02AED4A0` (`003829C0`, 8 B, returns that address) x a **reference projection** of the second copy: `003CBA50` with aspect `1.7778` and a scale multiplier of `1.1547` | - |
| `02AEDD30` | the same head matrix x the projection | the last call of the update hands it to `0024E180` |
| `02AEDE70` | a copy of the working camera's matrix at `02AED580`; **only when the device override predicate of section 2 is true**, eight elements are replaced from the override's own matrix | the view matrix |
| `02AEDEB0` | a copy of the working camera's matrix at `02AED5C0` | - |
| `02AEDEF0` | a copy of the **capped-field-of-view copy's** matrix | **the camera's view-to-world matrix**; its fourth row `02AEDF20` is the camera position |
| `02AEDDF0` (final) | `02AEDE70` x the first `02AEDDF0` | **world-to-clip**; the character cull test and distance |
| `02AEDDB0` | `02AEDE70` x `02AEDD30` | **world-to-clip**; a character's projected origin and sort depth |
| `02AEDE30` | `003CBC40` sets the capped copy up with the working field of view, a near of `1.0` and a **far of `1000`**; its projection x `02AEDE70` | - |
| `02AEDF94` | `atan2f` of the view matrix's third row, first and third elements (`02AEDE90`, `02AEDE98`) | the camera's heading |

**The tail.** A Movement-side object from `0026E500(0)`, when there is one, is handed the camera position (`02AEDEE0`, the
fourth row of `02AEDEB0`) and four of its qwords are copied to `0209A698`..`0209A6B8`. The device receives the matrix
`02AEDEB0`, the aspect, the three parameter floats at `02AED560`..`02AED568` and a flag that is 1 when the object behind
`0209A670` has a non-zero `+0x120` (`00182640`). Unless `00182570` reports true or that flag is up, one more projection is
built with the second aspect value (`02AED540`), multiplied by the working camera's matrix at `02AED500` and installed
through `003B4150`. Last, `02AEDD30` goes to `0024E180`.

The identifications in bold were made from the consumers, on
[how a character fades](../Character-Render-Records/how-a-character-fades-the-ten-channels.md) sections 4b and 4c, and
agree with [the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md), which
already called `02AEDEF0` the camera matrix.

## 4a. Where the offsets come from: the shake table

The offsets of section 4 have **one setter**, `00382B70` (119 B): two pointers to four-float vectors, stored at
`02AEDF70` (position offset) and `02AEDF80` (target offset), and two floats stored at `02AEDF98` and `02AEDF9C`. It has two
callers, and both were read whole.

**The table.** Five records of `0x3D0` bytes from `02ADDA34`, each holding **four channels of `0xF0` bytes**. A channel
carries a position offset (three floats), a target offset (three floats), two scalars, and a **draw tag** - a dword that
is -1 when the channel is idle and otherwise names the draw of the frame (0 or 1,
[what happens between two frames](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) section
4.3) the channel applies to. `0037DB40` `(record, channel, tag)` (35 B) stores a tag; `0037DCC0` `(record, channel)`
(35 B) returns the dword just below it, the channel's status.

**The reset - `0037D890`** (209 B) stores -1 in all twenty draw tags, calls the setter with zero vectors and zero
scalars, and zeroes the two accumulator rows at `02EBF380`.

**The gather - `0037D4C0`** (808 B) runs once per draw. It takes two base scalars from `002563F0`, steps the table with
`0037D970`, reads which draw is being prepared from the pass-mask block's byte `+8`, and walks the five records **from
the last to the first**, channels 0 to 3 in each. For every channel whose draw tag equals the current draw: its two
**scalars are added** to the running pair, and its two **vectors replace** the running vectors. So scalar shakes from
several sources sum, while of several vector shakes only one survives - the one in the lowest-numbered record, highest
channel. If `02EBF3C0` is non-zero the accumulator row for this draw (`02EBF380 + draw x 0x20`: six floats and one scalar)
is added on top. The result goes to the setter. A draw index other than 0 or 1 matches nothing.

### The accumulator row's writer is the Screen Shake option's consumer (2026-09-21, FABLE)

**`0037D970` is not a "table step", and it is what fills the accumulator rows** — both of the items
this section's *Not read* line lists. Read complete (`0xF5` bytes), and the order inside it is the
whole point:

| | |
|---|---|
| `0037D989` | `call 00237420` → `ebx` — an **override** test: that body returns whether pointer `02089350` is non-null |
| `0037D990` | `call 00358320` → the draw being prepared, kept in `rdi` |
| `0037D995`–`0037D9ED` | six floats from `02AED5F0`–`02AED608` into stack temporaries |
| **`0037D9F6`** | **`call 003D83A0` — the candidate calculation, before any option branch** |
| `0037D9FB` | `test ebx, ebx` / `jne` — **the override jumps straight to the copy**, past both flags |
| `0037D9FF` | `cmp dword [02EBF3C4], ebx` / `je` skip |
| `0037DA07` | `cmp dword [02EBF3C0], ebx` / `je` skip |
| `0037DA0F`–`0037DA45` | three scalars and one 16-byte block — **28 bytes** — to `02EBF380 + draw × 0x20` |

*Those two compares are against zero*: the path is only reached when `test ebx, ebx` fell through, so
the code compares each flag with a register it already knows holds zero. The condition to write is
therefore

```text
pointer[02089350] != 0   OR   (dword[02EBF3C4] != 0  AND  dword[02EBF3C0] != 0)
```

and **`02EBF3C4` is the player's Screen Shake setting** — settings command 10, option bit 14 stored
inverted, propagated by `0037DDC0`
([the settings command table](../../19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md)).

**So the setting gates the output copy, not the calculation.** `003D83A0` runs whichever way the
option is set. ***Which matters most for what it forbids:*** a quiet camera, or an OFF setting,
**cannot** be used as evidence that the shake sampler stopped — and that sampler draws the **gameplay**
generator, as the corrected paragraphs further down this section establish, so "shake is off" must
never become "the stream is undisturbed".

**Two further details, both about what the copy does not do.** The row is `0x20` bytes and 28 are
written, so its **last four bytes are never touched here**; and skipping the copy **does not clear
the row** — the previous draw's values simply stand. With the option off the accumulator is *stale*,
not zero. `0037D890` is what zeroes it.

**Bound:** this is a static reading of one body's branches, not an executed truth table. Which branch
a real frame takes, how often `0037D970` runs, what `02089350` is for and what any of it looks like
on screen are not observed here. *(Consumed from `ASTRA-RETURN-FABLE-SHAKE-OPTION-BOUNDARY`, whose
package reached the same condition independently; the bodies were re-read here rather than accepted.)*

*(`ASTRA-RETURN-OPUS-SHAKE-OPTION-BOUNDARY` asks the same question of the OWNED consumers - will they keep `02EBF3C4` distinct from `02EBF3C0`, and separate output-copy suppression from sampler execution and RNG attribution. **Checked 2026-09-21 (OPUS) rather than assumed, and both hold.** This page keeps the two flags as two compares, records `call 003D83A0` as happening before any option branch, and states the inference block outright. The other named consumer, `21-RNG-And-Determinism/CONTRACT-gameplay-generators.md`, holds the same line from the other side - "a finished shake still draws", its §9 determinism rows explicitly NOT revised, and the per-frame count of non-zero drivers routed to ASTRA as a live question rather than inferred. **Nothing moved and nothing needed to**; recorded so the return is not re-raised against records that already answer it. No new harness or live coverage is granted by this note.)*

**The driver - `003DCFB0`** (285 B; one caller, the per-frame camera publish that the character transform contract describes). Its argument is **an actor-manager slot** - the caller tests bit 0 of its `+0x10`, the slot-live bit, and the script
handlers fetch it with the 8-byte getter of the current-slot pointer `02099D70`; an earlier draft of this section called
it a camera-side object - whose `+0x28` is its **record index in the shake table**: five slots, five records. It holds four
`0x18`-byte channel drivers from `+0x170`: an authored data id, a second dword, a state word at `+8`, a time at `+0xC` and
a rate at `+0x10`. It does nothing when the object's `+0xF0` is null. Each frame it (1) sets the draw tags of the two
channels named by the words at `+0x1C` and `+0x1E` (a negative word, or a driver whose state is 0, is skipped) from
that driver's second dword (passed through `003DA190`, which is three bytes and returns its argument);
(2) for each of the four drivers whose state is non-zero, evaluates the channel at the driver's time with `0037D1F0`
`(record, data id, time, channel)`; (3) reads the channel's status back, and when it is 2 - finished - sets the driver's
state to 2; otherwise, unless only bit 1 of the state is set, advances the time by `[02B58190]` x rate x the frame-rate
multiplier. ~~**A shake is an authored curve sampled by time, not noise generated here.**~~

**What a shake is - corrected 2026-09-19.** *The sentence above was wrong, and it was mine: I inferred it from the driver's
`(data id, time)` call shape before reading the sampler.* `0037D1F0` `(record, entry, time, channel)` (712 B, read whole)
is **eight sine oscillators whose speed and amplitude are random every frame**, with authored curves setting the ranges:

1. An entry of -1 marks the channel finished (status 2) and returns.
2. `0037D130` (190 B) loads the channel's 32 parameters - four per oscillator: speed base, speed range, amplitude base,
   amplitude range - from the authored entry (`0x60` bytes; 32 curve numbers from its `+0x30`). A curve number of 0
   gives 0; otherwise curve *n - 1* of the record's curve table is evaluated at the channel's time. The record header
   holds the entry array at `+0` and the curve table at `+8`.
3. Each oscillator's phase advances by `(random x speed range + speed base) x` the frame-rate multiplier, and its
   output is `sin(phase) x (random x amplitude range + amplitude base)`.
4. Oscillators 0, 1, 2 are the **position offset**; oscillators 3, 4, 5, each **added to the matching position
   component**, are the **target offset** - so the target moves with the camera and then wobbles on its own;
   oscillators 6 and 7 are the two scalars.
5. The channel is finished when its time, less 0.5 (less nothing when a shared mode flag is set), exceeds the entry's
   duration word at `+0x28`; otherwise its status is 1.

**It draws from the gameplay generator.** Every random number above is `RNG_MT19937_NextFloatClosed`, which
[the gameplay generators contract](../../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md) shows advancing the
same cursor as the integer draw (its body `00863C80` was checked here: the state block is `02EB3870` and the index
`02EB4230`, the gameplay generator's). **The shake sampler is that entry point's only consumer**: a raw call and jump sweep
finds nine sites reaching the thunk, all nine in `0037D1F0`, and no other reference to the thunk or the body anywhere in
the image. One evaluation takes **sixteen** words from that stream, for every
driver whose state is non-zero

> **CORRECTED 2026-09-20 (OPUS), upholding `ASTRA-CONTRA-OPUS-SHAKE-BOUND-IS-PER-SLOT`. The words
> "once per frame" were doing work the evidence does not support, and the four-driver loop is not the
> outer bound.** The per-frame caller `00314370` is 85 bytes and I re-read all of them (SHA-256
> `3213b13b…`, matching ASTRA's citation exactly). Its shape is a **five-slot loop**, not a single
> slot:
>
> ```asm
> 00314381  xor   ebx, ebx
> 00314383  mov   ecx, ebx
> 00314385  call  00263FF0            ; slot record by index
> 0031438D  test  byte ptr [rax+0x10], 1   ; per-slot eligibility
> 00314391  je    003143A3
> 00314396  call  003DA050            ; channel driver
> 0031439E  call  003DCFB0            ; shake driver
> 003143A3  inc   ebx
> 003143A5  cmp   ebx, 5
> 003143A8  jl    00314383
> ```
>
> **So the four-driver loop runs per ELIGIBLE SLOT, and the caller visits five slots.** The ceiling
> per invocation is therefore up to **20 driver visits, 320 words**, not four drivers and 64 words —
> and every bank, state and entry guard still applies, so the real figure is at or below that and is
> **conditional, not fixed**.
>
> **And "per frame" is not established at all**: `00314370` is reached from several call sites (the
> field frame `0022A770` at three and `MainLoop_UpdateAndRenderFrame` at two, per the character
> transform contract), so the number of invocations in a frame is a scheduling fact nobody has
> measured. **A per-slot conditional quantity was being reported as a frame-wide bound.**
>
> **What survives unchanged**: that one evaluation takes sixteen words; that the sampler is the
> gameplay MT's consumer through `0037D1F0`; that a finished driver (state 2) keeps drawing because
> the sampler only leaves early on an entry of `-1`; and therefore that camera shake is not cosmetic
> for anything reproducing the stream. **What is withdrawn is the rate.**
>
> **A related caution, same adjudication.** A static call-site census — such as the 98 sites over 66
> functions recorded for the MT draw thunk — counts *where* a generator is called from. It is not a
> measurement of *how often*, and it cannot support a claim that one consumer dominates by volume.
> Those are different quantities and only a run distinguishes them. - **including a finished one**: the driver sets state 2 on finish, state 2 is non-zero,
and the sampler only leaves early for an entry of -1. A shake that has run out therefore keeps taking sixteen words a
frame until a script stops or clears it (the shipped scripts do pair their 328 starts with 315 clears and 178 stops).
For anything that must reproduce the stream - a replay, a second machine - **camera shake is not cosmetic**.
Static evidence; no run was made.


*Not read:* the curve evaluator the loader calls, ~~the table step `0037D970`~~, `002563F0`, and ~~who fills the accumulator
rows~~ — *both struck 2026-09-21 (FABLE): they are the same function, and the section above reads it.* **The script side, traced the same day.** Every start form ends in `003DD230` `(object, bank index, time, channel,
draw)` (225 B), ~~reached through the handler of~~ **the two-argument forms through the handler of**
**`camerashakestart_1a3(channel, id)`** (`01A3`, `00349730`) *(corrected 2026-09-29, OPUS falsification pass 1, `CON-184`: a third form, **`camerashakestart_1a2`**
(`01A2`), has its own handler `003492F0`, which pushes nothing and pops the draw from the script as the first of three
arguments; `003DD230` maps only a negative draw and puts no upper bound on a non-negative one. The census below finds no
`1a2` call in the shipped `us` scripts)*, which takes
the current actor-manager slot from the 8-byte getter `002640C0` (it returns the pointer at `02099D70`), masks the id to its low 24 bits, passes a time of `0.0` and a draw
of -1. The shorter form `camerashakestart` (`019C`) pushes -1 for the argument it lacks and jumps to
the same handler. `003DD230` rejects a channel above 3, a missing bank, or an index outside the bank - **the bank is
authored data behind the slot's `+0xF0`**, a count at `+4` and 16-byte entries whose data id is read from
`+0x14 + index x 16` - and otherwise loads the driver: data id, draw tag, state 1, the bank index at `+0xA`, the
time, a rate of `1.0`. A negative draw becomes the return of `005C5230`, a folded stub that returns 0, so ~~**script
shakes always apply to draw 0**~~ **the `1a3` and `019C` forms always apply to draw 0, and so do all the shipped script
shakes; a `1a2` start applies to the draw its script names (corrected 2026-09-29, OPUS falsification pass 1, `CON-184`)**. It zeroes the table channel's working fields (`0037DCF0`, 81 B) and records the channel in the slot's
word `+0x1C + draw x 2` - which is why a draw has at most one tagged channel. `camerashakestop_19e(channel)` (`019E`) reaches `003DD320` (33 B), which zeroes that driver's state and nothing else;
`camerashakeclear` (`01A1`) reaches `003DCF60` (70 B), which sets both per-draw words to -1 and, for all four drivers,
state 0 and bank index -1.

*In the shipped scripts* ([camerashake_census.py](members/camerashake_census.py),
[camerashake-census.tsv](members/camerashake-census.tsv); 842 calls, parsed count equal to a plain substring count):
328 starts, **all in the two-argument form**, 315 clears, 178 stops, 13 syncs, 6 changes. 327 of the 328 ids carry the
top byte `0x0D` and one `0x02`; the handler discards that byte. Channel 0 takes the great majority, bank indices 0, 1
and 2 most of those. The one-argument `camerashakestart` is never called - and as read it would pass a channel of -1,
which `003DD230` rejects.

**The twin.** [The scripted camera player](the-scripted-camera-player.md) has the same shape in the same slot: four
`0x18`-byte channels at `+0x110` over an authored list behind `+0xD8`, run by `003DA050` - which the per-frame caller
invokes immediately before the shake driver - and started by `camerastart` with ids tagged `0x02`. That is what the one
`0x02`-tagged id in the shake census is: a camera id handed to a shake verb. The handler discards the tag, so the call
starts shake bank entry *n*, whatever its author meant.

*Still not read:* the table step, `camerashakechange` / `camerashakeratio` / the two sync verbs, and the
bank's entry layout beyond its data id.

## 5. Behaviour a reimplementation must keep

1. Eight submissions a frame at most; the ninth is dropped.
2. Highest priority wins; ties go to the earliest submitter; all submissions are consumed each update.
3. No submission means no change - the previous frame's matrices are reused.
4. The offset vectors are added after arbitration, so they shake or shift whichever camera won.

## 6. What is not known

- The rest of the `0xD0`-byte camera record. Read so far: `+0` near, `+4` far, `+8` field of view, `+0xC` a second
  field-of-view float, `+0x10` `1 / tan(fov / 2)`, `+0x20` the view matrix, `+0x60` the camera's world matrix (fourth
  row the eye), `+0xA0` the look-at point, `+0xC4` the roll.
- What the matrix at the head of the working block is (the extra factor in `02AEDD30` and `02AEDD70`), what the device
  method behind `001824E0` does to the field of view, what the Movement object of the tail is, and what `0024E180` does
  with `02AEDD30`.
- What the shared predicate of section 2 tests and whose vectors override the submitted camera.
- ~~Who writes the offset vectors.~~ *Answered in section 4a; the scalars, the sampler and the verbs in sections 4 and 4a.*
- Static evidence throughout.

## 7. Where each behaviour is in the bytes

| body | what is there | at |
|---|---|---|
| `003829D0` submit (373 B) | the override test, its three vector fetches, and the apply | `003829EE`, `003829F7`, `00382A15`, `00382A42`, `00382A57` |
| | free-slot search over eight slots; dropped when full | `00382A70`, `00382A79`, `00382A85` |
| | copy, priority, submitted flag | `00382A8A`, `00382B01`, `00382B07` |
| | default-view test and the two wrappers | `00382B18`, `00382B21`, `00382B28` |
| `00382910` reset (163 B) | the eight flags; offsets zeroed and their fourth components; `02AEDFA0` | `0038292A`..`00382954`, `0038295A`, `00382975`, `003829A4` |
| `0037D4C0` shake gather (808 B) | base scalars; table step; current draw | `0037D4EC`, `0037D4F1`, `0037D514` |
| | channel 0: tag test, scalars added, vectors replaced | `0037D557`, `0037D564`, `0037D569`, `0037D573`..`0037D58B` |
| | channels 1, 2, 3 | `0037D5BD`, `0037D644`, `0037D6CB` |
| | previous record; accumulator row; setter | `0037D74D`, `0037D75C`, `0037D765`, `0037D7C4` |
| `0037D890` shake reset (209 B) | twenty tags; zero offsets; accumulators | `0037D8C0`..`0037D8EA`, `0037D910`, `0037D917` |
| `003DCFB0` shake driver (285 B) | record index; the two tagged channels | `003DD01E`, `003DD019`, `003DD026` |
| | four drivers: evaluate, status, finished, time advance | `003DD044`, `003DD06B`, `003DD075`, `003DD07F`, `003DD08B`..`003DD0A5` |
| `0037D1F0` shake sampler (712 B) | entry -1; parameter load | `0037D21F`, `0037D224`, `0037D27C` |
| | eight phase advances, each with a draw | `0037D291`..`0037D2BB` |
| | time bookkeeping; oscillators 0-2 | `0037D2BD`..`0037D2D3`, `0037D2D8`, `0037D2FB`, `0037D326`, `0037D351` |
| | oscillators 3-5 added to the position; 6 and 7 | `0037D37C`, `0037D3AF`, `0037D3E2`, `0037D418`, `0037D449` |
| | duration test and the two statuses | `0037D451`, `0037D47B`, `0037D495`, `0037D4A8` |
| `0037D130` parameter loader (190 B) | eight by four; curve number; evaluate or zero | `0037D14C`, `0037D180`, `0037D1A6`, `0037D1B1` |
| `003DD230` load a driver (225 B) | draw default; the four rejections | `003DD261`, `003DD26C`, `003DD275`, `003DD27A`, `003DD27E` |
| | driver fields; table channel prepared; per-draw word | `003DD293`..`003DD2C7`, `003DD2D5`, `003DD2EC` |

| body | what is there | at |
|---|---|---|
| `003820C0` camera update (2,125 B) | aspect stored; the eight slot tests; nothing submitted | `003820FB`, `00382100`..`00382219`, `00382224` |
| | winner copied; stack copy | `0038222D`, `003822F2` |
| | field-of-view shake and projection scale; roll shake | `00382374`, `00382389`, `003823AF`, `003823CD` |
| | offsets rotated; added to target and eye; rebuild | `003823E2`, `003823F9`, `0038240D`..`0038247E`, `00382486` |
| | the copy: 45-degree cap, same shake, rebuild | `00382491`, `00382496`, `003824F7`, `0038250C`, `00382589` |
| | reference projection; `02AEDD70`; field-of-view adjustment | `003825D4`, `003825F2`, `00382603`, `0038263B` |
| | projection; `02AEDD30`; view matrix; override predicate and its eight stores | `00382651`, `00382667`, `0038267A`, `0038267F`, `003826A9`..`00382712` |
| | `02AEDEB0`, `02AEDEF0`, the two world-to-clip products, heading | `00382728`, `00382738`, `00382752`, `0038276C`, `00382781`, `0038279E` |
| | far-1000 projection into `02AEDE30` | `003827A6`, `003827BB`, `003827D5` |
| | tail: Movement object, device, last projection, final hand-off | `003827DC`, `003827FB`, `00382881`, `003828A9`, `003828CF`, `003828DB` |

## 8. Related

- [The scripted camera player](the-scripted-camera-player.md) - the camera system above this layer.
- [How a character fades](../Character-Render-Records/how-a-character-fades-the-ten-channels.md) - the first consumers
  identified.

## Cross-subsystem neighbours

**Core runtime scheduling - SERVICE.** `00259970`, the 17-byte submit of the static default view, is called by the frame
body `0022A770` just before its second draw of the frame; the frame body owns *when*, this page owns what a submission
is. Generic helpers this page's functions share with many other systems (the override predicate and its getters, the
vector-by-matrix routine, the two graphics wrappers that call the reset and the update) are described by role and not
named, because naming a shared leaf imports every one of its callers.

**Movement - SERVICE, seen only as calls.** Late in its building stage the camera update `003820C0` calls the
Movement-owned `0026E500` and then hands the vector at `02AEDEE0` to the Movement-owned `00233230`. Neither body was
read; what Movement learns from the camera there is not claimed.

**UI - MECHANICAL, seen only as calls.** The shared leaf `00202E10`, cited by this page's `003CBD60`,
is also called by the UI body `005512B0`. What UI asks of the same helper is not claimed; the page owns what the
camera rebuild does with it.

**Audio - MECHANICAL, seen only as calls.** The shared leaf `00202C70`, which this page's `003B4150`
forwards to with the `02B40470` table, is also called by the Audio body `00362850`. What Audio asks of the same
helper is not claimed; this page owns the camera callers' use of the table, not Audio's.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — CLIENT and MECHANICAL (31 edges).** `00263FF0` (21 bytes: the address of entry *index* in the actor-manager slot array, stride `0x288`) is called by the per-frame caller `00314370` at its `00314385` read and by 29 actor bodies, among them `ActorResource_FinalizeManagerRuntimeAfterLoads` `0032F1B0`, `ActorResource_OnDefinitionPayloadLoaded` `0032F850`, `ActorResource_BeginPrimaryPayloadLoad` `00330310`, `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0`, `ActorResource_AllocateAndSubmitEntry` `003DBCF0` and `003306E0`; `003F1E90` calls `00202C70`, a 31-byte copy of four 16-byte rows (a 4×4 matrix). The shake path borrows the actor layer's slot-by-index accessor to reach its slot record, and the matrix copy is a generic leaf; neither edge gives the actor layer a part in the shake.

**Gameplay — MECHANICAL (1 edge).** `BattleAction_FindApproachGeometryAroundTarget` `00339630` calls `00202E10`, a 115-byte leaf that forms the cross product of two 3-float vectors. It is shared vector math the camera matrix rebuild also uses, not a camera crossing.

**Input — OUT-OF-SCOPE and CLIENT (12 edges).** The field frame `0022A770` calls `0017DE60`, `InputGameplay_RebuildFrameSnapshotFromChannelHistory` `002498B0`, `00250180`, `0035AE30`, `0035AF20`, `InputControl_SetOneShotFrameCallback` `0035E9A0`, `0035FF90`, `InputGameplay_RebuildRemappedTransitionMaskState` `0036FDF0`, `InputGameplay_GetRemappedHistoryMask04` `0036FF70` and `InputGameplay_GetRemappedHistoryMask0C` `0036FFD0`; the input bodies `00226BE0` and `002E09A0` call `00263FF0`. This page cites `0022A770` only as the frame body that decides when the camera submission runs; its input refresh is its own business, and two input bodies are further callers of the slot accessor.

**Party — OUT-OF-SCOPE (1 edge).** `0022A770` calls `PartyFocus_CommitPendingPackedActorHandle_Thunk` `00358BB0`. The field frame commits a pending focus change in the same frame; the camera submission neither reads nor causes it.

**PlatformOnlineAchievements — OUT-OF-SCOPE (1 edge).** `0022A770` calls `00316930`. It is one more of the field frame's per-frame duties, unrelated to what a camera submission carries.

**RNG_Random_Selection — SERVICE and DEPENDENCY (3 edges).** The channel evaluator `0037D1F0` calls `RNG_MT19937_NextFloatClosed` `00379CE0`, and the generator body `00863C80` calls `RNG_MT19937_TwistState` `00866B90` and `RNG_MT19937_SeedState` `00866D60`. The shake sampler draws the gameplay MT19937 stream whether or not the Screen Shake option lets its output through, so a shake advances the same state that gameplay rolls use.

**Resource — OUT-OF-SCOPE (1 edge).** `0022A770` calls `00324510`. It is another duty of the field frame and does not touch the camera path.

**Script_VM_Native_Bridge — CLIENT (31 edges).** The shake verbs' handlers are script bodies: `003492F0` (`camerashakestart_1a2`) and `00349730` (`camerashakestart_1a3`, itself called by `00349A60`) pop their arguments with `VMValueStack_PopInt32CoerceFloat32` `00267E10` (and `00349730` pushes a result with `VMValueStack_PushInt32` `00267F90`) and call the start `003DD230`; `00349ED0` and `0034A370` call the stop `003DD320`; `0034B100` calls the clear `003DCF60`; `0034C7E0` calls `00358320`, which returns the current draw index as a signed byte; `00357F00` calls `003DA190`, a 3-byte function that returns its argument; and 20 script bodies call the slot accessor `00263FF0`, among them `0033F7F0`, `00342490`, `0034E460`, `003574B0` and `0050D0C0`. Scripts start, stop and clear shakes through these verbs and read actor slots through the shared accessor; the script layer drives the shake and owns none of the sampler.

**WorldAreaField — OUT-OF-SCOPE and CLIENT (2 edges).** `0022A770` calls `World_UpdateSimulationTick` `00314020`, and `00314020` calls the shake reset `0037D890`. The world tick is one caller of the reset that stores -1 in all twenty draw tags and zeroes the accumulators, so the field layer's tick decides when that shake state is cleared; the field frame's call to the world tick is outside this page's claims.

## SWE2-EC7-50 update (2026-09-19) - `002563F0`

`002563F0` (185 B) is the camera state writer `0037D4C0` reads its two base scalars from - `00256650` single call over the `020964F0`-`02096500` byte band. Interior anchor `00256443` (the `00256650` call).

## SWE2-EC7-53 update (2026-09-19) - `003CBD60`

`003CBD60` (571 B) is the camera matrix rebuild the page describes - `00380190`/`00380650`/`003CBCA0` plus Movement helpers `00202B70`/`00202D50`/`00202E10`, `00182310`, `00D22740` rdata (the page note 'itself was not read' is now read). Interior anchor `003CBE17` (a `00380190` call).


## SWE2-EC7-53 update (2026-09-19) - `00233230`

`00233230` (524 B) is a Movement-owned helper the camera page names - `0022FF10`/`002324F0`/`00233050`/`00382080`/`00808C40`. Interior anchor `00233253` (a `00382080` call).

## SWE2-EC7-54 update (2026-09-19) - `00380650`

`00380650` (427 B) is a call-free vector magnitude - `x*x + y*y + z*z` mulss/addss chain on `[rcx]`/`[rcx+4]`/`[rcx+8]` plus the `[rcx+0xC]` term. Interior anchor `003806B2` (the squares `addss`).

## SWE2-EC7-56 update (2026-09-19) - `0022FF10`

`0022FF10` (201 B) is the `02EBF278` structure's body the camera page names - `0022F050`/`00808C40` plus `008C5B40`/`01F44830`. Interior anchor `0022FF39` (a `0022F050` call).


## SWE2-EC7-56 update (2026-09-19) - `00380190`

`00380190` (198 B) is a camera matrix helper - `00861F08`/`00861F0E`/`00861F14` plus `01CEBB70`/`01CEBBA8`. Interior anchor `003801C1` (a `00861F0E` call).

## SWE2-EC7-57 update (2026-09-19) - `003CBCA0`

`003CBCA0` (178 B) is a call-free SIMD flag-mask writer - `pcmpeqd`/`pandn`/`andps`/`orps` select loop keyed on `r8d` writing `[r10]` rows (camera matrix helper family). Interior anchor `003CBD06` (the `movups` row store).

## SWE2-EC7-60 update (2026-09-19) - `00182640`

`00182640` (157 B) is the `0209A670` `+0x120` probe the camera page names - `00189120`/`001897C0`. Interior anchor `00182663` (a `00189120` call).

## SWE2-EC7-61 update (2026-09-19) - `001897C0`

`001897C0` (1101 B) is the camera-chain body the camera page names - `0018A120` single direct call plus 10 vcall sites, `008C5F78`/`008C5F90`/`008C5FB0`/`01CEBBA8`. Interior anchor `00189AB4` (a `0018A120` call).

## SWE2-EC7-62 update (2026-09-19) - `0018A120`

`0018A120` (505 B) is the `i*0xD8+0x150` camera element body - `001854C0`/`00187460` plus `008C5F80`/`008C5F90`/`008C5FB0`/`008C5FD0`. Interior anchor `0018A237` (a `00187460` call).



## SWE2-EC7-63 update (2026-09-19) - `001854C0`

`001854C0` (830 B) is a call-free SSE vector math body - `movups [r8+0x30]` + `shufps` swizzles, `mulss` against `[rdx+0xC]`/`+0x14`. Interior anchor `001854F2` (the `shufps` swizzle).



## SWE2-EC7-64 update (2026-09-19) - `0024E180`

`0024E180` (140 B) is a `02AEDD30` head-matrix body - `00202D60`/`00808C40` plus `00915518`/`0091551C`/`01F44830`/`02AEEB20`. Interior anchor `0024E1F5` (a `00202D60` call).


## SWE2-EC7-89 update (2026-09-20) - `003B4150` table forward measured

`003B4150` (15 B) is the thin forward the camera callers run:
`00202C70(02B40470, rcx)` - the shared table and the argument,
nothing more.
Interior anchor `003B415A` (the `00202C70` tail).

`004679C0` (173 B) is the view-block initializer `00382910` calls on the camera record: `edx`/`r8d` land at `+0x44`/`+0x48` with `+0x4C` = `1024.0f` and `+0x50` = `0x4B7FFBFF`, `00229D20` primes the base, then the derived block - `+0` = `+0x44` half, `+0x14` = `+0x48` times the `0090030C` constant, `+0x28` = `+0x50 - +0x4C` scaled likewise, `+0x30`/`+0x34` = `2048.0f`, `+0x38` = `+0x50 + +0x4C` halved, `+0x3C` = `1.0f`, `+0x2C`/`+0x40` zeroed

Interior anchor `004679DE` (function `004679C0`).

`00229D20` (33 B) is the ~~speed-mode factor~~ **aspect ratio of section 3 (corrected 2026-09-29, OPUS falsification pass 1, `CON-184`: `003820C0` stores it at `02AED4E0` / `02AED540` and passes it as the projection's aspect)** both `003820C0` and `004679C0` consult: byte `02064AD1` selects the path - values 1, 2, 3 or 5 tail-jump `00182EE0` for ~~the authored answer~~ **the device object's own value (`001DDAB0`, then `001DD120`)**, everything else returns the fixed `1.333f` (`3FAAAAAB` at `00908D54`)

Interior anchor `00229D33` (function `00229D20`).

## Falsification pass 1 — 2026-09-29 (OPUS): arbitration, the build and the shake chain survive; a third start form and one note's label do not

**Attack.** Sections 2 to 4a and the appended notes were turned into checks at their instructions. Every caller set
the page states was re-counted with a raw E8/E9 sweep. As the competing case for section 4a, every `camerashake*`
verb in the verb table was followed to its handler. Script: `Tools/analysis-kit/gfz-scripts/falsify_camera_renderer.py`,
output `falsify_camera_renderer.out`, image `73461d08…`, 0 BROKEN, exit 0. The census is carried; section 6's open
items stay open.

| # | Clause attacked | Result |
|---|---|---|
| W11 | section 4a: "every start form … reached through the handler of `camerashakestart_1a3`"; "script shakes always apply to draw 0" | **refuted** (`CON-184`). `camerashakestart_1a2` (`01A2`, handler `003492F0`) pops the draw from the script, and `003DD230` bounds only a negative draw. Shipped scripts never call it |
| W12 | the note on `00229D20`: "the speed-mode factor", "the authored answer" | **refuted** (`CON-184`). It is the aspect ratio: 4/3, or the device's own value, passed to the projections |
| W0 | sizes | **survives**: all 38 |
| W1 | the caller sets and priorities | **survives**: `0x14` / `0x14` / `0x64`; one caller each for the update, the reset and the driver |
| W2 | section 2: submit | **survives**: eight `0xE0` slots; full means dropped; `+0xD4` / `+0xD0`; the view test either way |
| W3 | section 3: arbitration | **survives**: best starts at -1; strictly greater; the earliest submission wins a tie; every flag is consumed |
| W4 | section 3: the aspect | **survives** |
| W5 | section 4: constants | **survives**: 0.7854, 1.7778, 1.1547, 1000; `003CBA50` divides by the aspect |
| W6 | section 4a: the shake gate | **survives**: `003D83A0` runs before both option compares |
| W7 | section 4a: the MT consumer | **survives**: nine thunk sites, all in `0037D1F0`; `02EB3870` / `02EB4230` |
| W8 | the correction box: `00314370` | **survives**: five slots |
| W9 | section 4a: the loader | **survives**: the four rejections; a negative draw becomes 0; the per-draw word |
| W10 | section 4a: the `1a3` / `019C` forms | **survives** |

Corrected in place: section 4a's script side, and the note on `00229D20`. The consumer record is
`_index/candidates/camera-renderer-falsification-pass-1-0929/`.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-how-a-camera-reaches-the-renderer-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001824E0` | 72 B | when `00189120()` is non-null, calls `00186AB0` with the result of a second `00189120()` call followed by the incoming `rcx`, `rdx` and `r8`; otherwise it does nothing | `001824F8`, `00182500`, `00182502`, `00182513` |
| `00182570` | 33 B | when `00189120()` is non-null, returns byte `+0x1C` (zero-extended) of the object a second `00189120()` call returns; otherwise returns 0 | `00182574`, `0018257C`, `0018257E`, `00182583` |
| `0034A370` | 59 B | calls `00267F90(r9, 0)`, then `002640C0()`, then `00267E10(r9)`, and tail-jumps to `003DD320(002640C0 result, 00267E10 result)` | `0034A37A`, `0034A382`, `0034A387`, `0034A392`, `0034A3A6` |
| `0037DB40` | 35 B | stores `r8d` to the dword at `02ADDA7C` + sign-extended `ecx` x `0x3D0` + sign-extended `edx` x `0xF0` | `0037DB43`, `0037DB4D`, `0037DB5E` |
| `0037DCC0` | 35 B | returns the dword at `02ADDA78` + sign-extended `ecx` x `0x3D0` + sign-extended `edx` x `0xF0` | `0037DCC3`, `0037DCD4`, `0037DCDE` |
| `00382080` | 58 B | zeroes 0x100 bytes from `02EBF278` as 4 iterations of eight qword stores with a 0x40 stride | `00382090`, `0038209F`, `003820AF`, `003820B3`, `003820B7` |
| `003CBA50` | 114 B | with `a` = float `+0` and `b` = float `+4` of `rcx`, `s` = `xmm3` x float `+0x10` of `rcx` and `d` = `b - a`, writes the floats at `rdx`: `+0x14` = `s`, `+0` = `s / xmm2`, `+0x28` = -((`a + b`) / `d`) (sign flip with `01CEBDA0`), `+0x2C` = -1.0 (`0xBF800000`), `+0x38` = `a` x `b` x -2 (`008F3148`) / `d`, and zeroes `+4`..`+0x10`, `+0x18`..`+0x24`, `+0x30`, `+0x34` and `+0x3C`; returns 0 | `003CBA60`, `003CBA7C`, `003CBA89`, `003CBA9F`, `003CBABC` |
| `003CBC40` | 91 B | stores `xmm1` to the floats `+8` and `+0xC` of `rcx`, `xmm2` to `+0` and `xmm3` to `+4`, calls `00861F1A(xmm1 x 0.5)` (0.5 at `01CEBB70`), and stores to float `+0x10` 0 when that result equals 0.0 (ordered compare) and otherwise 1.0 (`01CEBBA8`) divided by it | `003CBC4E`, `003CBC53`, `003CBC67`, `003CBC79`, `003CBC90` |
