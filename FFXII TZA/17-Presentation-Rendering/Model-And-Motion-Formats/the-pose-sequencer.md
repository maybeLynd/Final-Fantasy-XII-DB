---
system: The pose sequencer - how FCP section 7 scripts which add-motion pose group and which texture patch a character is showing
category: 17-Presentation-Rendering
status: DOCUMENTED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the three render-record accessors of FCP section 7 (003E6F50, 003E7450, 003E6A20) and the four sequencer
    bodies they reach (00477370 start, 00477480 step, 004776D0 value, 00477670 reset) disassembled from the authority
    image and read whole, 2026-09-19; the one consumer of the value, inside the add-motion pose applier, read over the
    window 00371F2E..00371FD4 only; the section format the code implies then parsed out of all 1,066 FCP blocks of an
    extracted copy of the game with every structural test passing
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-pose-sequencer-falsification-pass-1
  note: written by FABLE. Grew out of correcting my own "FCP sections 2, 3, 6, 7 have no reader" (UQ-220) - section 7
    has three direct readers. Static plus one data census. A first hypothesis (texture animation) was refuted by the
    value's one consumer; the draw side was then read and shows the same value selecting a texture patch, so both are true. Not read - the rest of the pose applier and one of the
    other functions that address the slot table. Added the same day - the three raisers of events (authored command
    0x1D, pending-state activation, the Stop status), where the variant comes from, and a variant setter whose two
    arguments are crossed in the shipped code so that it can never store; pending first review
---

# The pose sequencer

Some of a character's movement is not in any motion file. The add-motion tables ([the `.adm` tables](adm-add-motion-tables.md))
hold **additive bone poses in numbered groups**, and for one kind of track *which* group is showing at a given moment is
decided by a tiny sequencer: eight slots per character, each playing a list of **(duration, value)** frames authored in
**section 7 of the character's FCP block** ([the FCP block](fcp-character-parameter-block.md)). An event starts a
sequence - optionally one picked at random from several - the sequencer steps it on simulation ticks, and the add-motion
pose applier asks each frame "what is slot *n* showing?" and applies the pose group with that number - while the
model-instance draw uses the same number to copy a patch of one texture into another.

## 1. Section 7, as the code reads it

`S` = payload + the section-offset word at payload `+0x0E`. The three accessors - `003E6F50` (32 B, returns `S` or 0),
`003E7450` (88 B, start an event) and `003E6A20` (62 B, reset a slot) - all load the render record's payload pointer
`+0x400` themselves and pair it with the record's **phase-entry handle `+0x450`**.

```struct FcpSection7 base=section7
+0x00          u16[8]   eventOffset     from S, one per event; 8 in 1,066 of 1,066 blocks
eventOffset[e] + 6 x variant:
  +0  u8   slot          which of the entry's eight slots this event drives
  +1  u8   pickParam     handed to the random pick when no choice is forced
  +2  u16  rel           0xFFFF = the event does nothing; else the choice table T is at (record + 2 + rel + 0x10)
  +4  u8   enabled       0 = the event does nothing
  +5  u8   (not read)
T - 0x10       u8, u8   source and destination sub-object ids of the model instance (the draw side, section 4)
T - 4          u16      offset (from T - 4) of the rectangle table R (section 4)
T - 2          u16      choiceCount
T + 2 x c      u16      offset of choice c: its sequence is at T + offset + 2 x c
sequence:      u16 frameCount, then frameCount x { u16 durationTicks, u8 endAction, u8 value }
```

`variant` is the phase entry's dword `+0xC`: one event can carry several 6-byte records and the entry chooses among
them. **The variant is fixed when the entry is made**: the record's set-up (0041FCF0, at `0041FEAC`..`0041FEB8`), for a
model that has a section 7, calls the allocator `004772E0(recordIndex, n)` (139 B) with `n` = record byte `+0x5C` - the
model-variant number the record initialiser stores from its fifth argument, floored at 1 - and the allocator stores
`n - 1`. The entry table is 32 entries; a handle is `serial << 8 | slot`, serial never 0. *A second writer exists and
cannot work*: `00477610(handle, n)` (38 bytes), called only by the authored command of section 4b, indexes the table
with the low byte of **`n`** and compares the entry's handle with **`n`** - its two arguments are crossed in the shipped
code (`0F B6 CA`, `movzx ecx, dl`, where every sibling has `cl`) - so with `n` a small number and every handle at least
`0x100` it never matches and never stores. The census below parses variant 0.

## 2. The slot table

The phase entries are `0x40` bytes each at `02CA6CA0`, indexed by the low byte of the handle and checked against the
entry's dword `+4`. After the header come **eight parallel byte arrays, one byte per slot**:

| offset | per slot |
|---|---|
| `+0x10` | active |
| `+0x18` | "re-pick at random when the sequence ends" |
| `+0x20` | the event playing, `0xFF` = none |
| `+0x28` | the choice playing, `0xFF` = none |
| `+0x30` | frame index |
| `+0x38` | ticks spent in the frame |

## 3. Start, step, value, reset

- **Start - `00477370(handle, event, choice, S, onlyIfChanged)`** (265 B). Finds the event's record for the entry's
  variant; does nothing if `rel` is `0xFFFF` or `enabled` is 0. With `onlyIfChanged` set and the same event already on that slot, a random
  request is dropped if the slot is already in random mode, and a forced choice is dropped if it is the one playing. It then marks the slot active, stores the event, zeroes the
  frame index and tick count, and either stores the forced choice or - when `choice` is `0xFF` - sets the re-pick flag
  and takes a random choice through the picker with the record's `pickParam`. A forced choice at or past `choiceCount`
  is refused.
- **Step - `00477480(handle, S)`** (347 B), called from the root record's animation-presentation phase. It runs only on
  frames whose **simulation step count is non-zero**, and only while the entry's word `+0` is non-zero and its word `+2`
  and the global `02CA6C98` are zero - **word `+2` is the freeze system-stop set 3 uses**, and the global freezes every
  character at once ([the time-stop page](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md),
  which found this step routine from the other side on 2026-09-17). For each active slot it adds a tick; when the ticks reach the frame's duration it
  moves to the next frame; **past the last frame**: with the re-pick flag, a new random choice and frame 0; otherwise by
  the last frame's `endAction` - **0 stop** (the slot goes inactive, event and choice back to `0xFF`), **1 hold** the last
  frame, **2 loop** to frame 0.
- **Value - `004776D0(handle, S, slot)`** (117 B): the current frame's `value` byte, or -1 for an inactive slot.
- **Reset - `00477670(handle, event, S)`** (92 B): clears the slot that event drives.

## 4. Who reads the value

One caller: the add-motion pose applier (`AddMotion_ApplyBonePose`; window 00371F2E..00371FD4 read, ~~the rest of its~~
~~3,387 bytes not~~ *(answered: see adm-add-motion-tables.md - the full disassembly of this function; 2026-10-02, OPUS)*). For an add-motion **track of kind 1**, the track's first word is a **slot number**; the applier takes
the phase-entry handle and section-7 pointer from the model instance (`+0x1E4`, `+0x1E8` - the fade page has the record
publishing its `+0x450` there), asks `004776D0` for the slot's value, and **searches the track's groups for the one
whose id equals that value** (group stride `0x28`, id at `+0x18`). That group's records are what it then applies; no
matching group, nothing applied. *This corrects the add-motion page's "for each track it takes group 0": that holds for
the other track kinds.*

**A second, draw-side reader - `00477750(handle, S)`** (330 B, read whole). For each active slot it takes the **two id
bytes at the head of the slot's choice table** (`T - 0x10`, `T - 0x0F`), asks the entry's model instance for the
sub-object with each id (the instance's word table at `+0x100`), and counts the slots for which **both** exist and are
flagged live; it returns that count x 128. Its caller is the model-instance draw, which uses the figure to reserve
command space before it goes on.

**What the draw then does - `00477B10`** (889 B, read whole), called by the model-instance draw right after the count,
with the reserved command space. For each active slot whose two sub-objects exist it reads a **rectangle table** `R`
(at the choice-table head `+0x0C` plus the word stored there) and emits one copy:

| field | meaning |
|---|---|
| head `+0`, `+1` | **source** and **destination** sub-object ids on the model instance - both have a pixel width and height, so: textures. *(The value-indexed coordinates are stored beside the first object and divided by its size; the fixed rectangle beside the second and by its size.)* |
| head `+2`, `+4`, `+8` | three more words that feed the copy descriptor; not decoded |
| `R + 0`, `R + 2` | destination x, y |
| `R + 4`, `R + 6` | width, height |
| `R + 0x0E + 4 x value`, `R + 0x10 + 4 x value` | **source x, y for the slot's current value** |

The pixel figures go into a copy descriptor, and the same rectangles, divided by each texture's own width and height
(`00477E90`, 76 B, returns them packed), go out as normalised coordinates. **So one sequencer value picks an add-motion
group for the bones and a patch of a source texture for the surface** - a face that moves in both. The "texture
animation" reading this page first set aside is therefore right, on the draw side; what was wrong was taking the
value's *one getter caller* for its only consumer.

## 4b. Who raises the events (added the same day)

`003E7450(record, event, choice, onlyIfChanged)` (88 B) is the record-side door to the start routine, and it has three
callers:

| caller | raises | when |
|---|---|---|
| authored presentation command **`0x1D`**, `00520D30` (190 B, read whole) | event = low nibble of the command's byte `+2`, choice = byte `+3` (`0xFF` = random), unconditional | when the byte's high nibble is 0, or equals the record's byte `+0x413` plus one - a filter that lets one authored stream address one of several records |
| the embedded presentation record's pending-state activation, at `0041DF83`..`0041DF95` | **event 2**, random choice, only-if-changed, on the record indexed by its word `+0x364` | when a pending state is activated |
| the status block's update `0051E3A0`, at `0051E47B`..`0051E494` ([how a status shows](../Character-Render-Records/how-a-status-shows-on-a-character.md)) | **event 0, choice 0**, only-if-changed, every frame | while the block's **Stop** flag `+0x33` is up, on updates whose third argument is 0 and that are not the reset |

**The reset has an authored door too:** command `0x1E` (`00520DF0`, 50 B, read whole) takes the event from the low
nibble of byte `+2`, applies the same high-nibble record filter, and resets that event's slot through `003E6A20`.

Command `0x1D` has three other arms on byte `+2`: `0xFD` sets bit 6 of record `+0x4B7` - *named 2026-09-20 (FABLE): command `0x09` consumes that bit and starts the next motion
without a blend ([the authored-command page](../Authored-Commands/the-authored-presentation-command-handlers.md))*; `0xFE` calls 00428B30 with the
record's index and 1; `0xFF` stores byte `+3` in the model instance's byte `+0xB8` and then calls the variant setter
that cannot work (section 1) - so the instance byte changes and the sequencer's variant does not.

**What the three events are, from the data** ([the census output](../../_experiments/evidence/fcp-section7-pose-sequencer/census.out.txt)
lists every distinct one; frames are `duration:endAction:value`). In the 54 NPC blocks that share one authoring:

```
event 0   choice 0   1:1:0                          snap to 0
          choice 1   3:1:2 3:1:1 3:1:0              2 -> 1 -> 0, three ticks each
          choice 2   1:1:0 1:1:1 1:1:2 1:1:1 1:1:0  0 -> 2 -> 0
event 1   choice 0   1:1:2                          snap to 2
          choice 1   3:1:0 3:1:1 3:1:2              0 -> 1 -> 2
event 2   choice 0   10:2:0 1:2:1 1:2:2 1:2:1 1:2:0    wait 10,  then 0 -> 2 -> 0
          choice 1   60:0:0 1:0:1 1:0:2 1:0:1 1:0:0    wait 60,  ...
          choice 2   250:1:0 1:1:1 1:1:2 1:1:1 1:1:0   wait 250, ...
```

The party-member blocks are the same with one more step (values to 3). Event 0 ends at 0, event 1 ends at the top
value, event 2 waits a random long time and then runs up and back in four or five ticks. **That is the shape of an
eyelid - open, close, and blink at random intervals - and it fits the three raisers**: activation starts the idle
blinking, a Stopped character is held at event 0's choice 0 (value 0, no blinking), and a cutscene can open or close
on command. *It is still an inference: which bones the add-motion groups move and which texture the patches land on was
not looked at, so "eyelid" is the data's shape, not something seen.*

## 5. What the files hold

[`census.py`](../../_experiments/evidence/fcp-section7-pose-sequencer/census.py) →
[`census.out.txt`](../../_experiments/evidence/fcp-section7-pose-sequencer/census.out.txt). The layout above is from
code; the files could have refuted it and do not:

| test | result |
|---|---|
| section 7 present, eight event offsets | **1,066 of 1,066** blocks |
| any event offset, record, choice table or sequence outside the section | **none** |
| slot byte of a live record | 0 in all 201 |
| choices per live record | 2 (67), 3 (122), 4 (12) |
| sequences parsed | 548; frame counts 1, 3, 4, 5 or 6 |
| `endAction` of the last frame | 0 (67), 1 (414), 2 (67) - **only the three values the stepper acts on** |
| durations | 1, 3, 10, 60 and 250 ticks; values 0-3 |

Live records exist in **67 blocks - 13 under `chara`, 54 under `npc`** - and only for events 0, 1 and 2; every other
block's eight records are disabled. One party member's event 0 (`pickParam` 4): choice 0 `[(3 ticks, value 0)]`; choice 1
`3, 2, 1, 0` at 3 ticks each; choice 2 `[(1, value 1)]`; choice 3 `0, 2, 3, 2, 1, 0` at 1 tick each - short runs through
four pose numbers, the shape a mouth or an eyelid would need - *an observation about the data, not a reading*. Section 4b
reads the three raisers and lays the three events side by side.

## 6. What a reimplementation must keep

- Eight slots per character, stepped only on simulation-step frames, so the sequencer pauses with the simulation.
- Random choice among 2-4 authored sequences when the caller forces none, and again at the end of each sequence.
- End actions stop / hold / loop; a disabled record or `rel` = `0xFFFF` makes an event a no-op, which is the case for
  every non-humanoid block.
- The value selects an add-motion **group id**, not a frame of a motion.

**Not read:** the two routines the draw-side copy hands its descriptor and coordinates to; the rest of the three raisers beyond the windows section 4b cites; the freeze-word setter 004775E0, the release
00477640, the table reset 004778A0 (read, 39 to 46 bytes each, one store apiece) and the 571-byte 004778D0, which
also addresses `02CA6CA0` and was not read; the random picker; the rest of the pose applier.

## Evidence

| body | interior anchors |
|---|---|
| `00477370` start (265 B) | `0047738C`, `0047739D`, `004773AD`, `004773BB`, `004773CD`, `004773E3`, `00477400`, `00477431`, `00477435`, `0047744A`, `00477453`, `00477466` |
| `00477480` step (347 B) | `0047748F`, `004774BA`, `004774D3`, `004774E3`, `004774F0`, `00477500`, `00477526`, `0047752A`, `00477542`, `00477557`, `0047755D`, `0047756E`, `00477579`, `00477598`, `004775A5` |
| `00477B10` draw-side texture patch copy (889 B) | `00477B51`, `00477B84`, `00477B96`, `00477BB5`, `00477BCB`, `00477BDE`, `00477C2D`, `00477C87`, `00477CA2`, `00477CB9`, `00477CC2`, `00477D10`, `00477D21`, `00477D2F`, `00477D8F`, `00477E2E` |
| `00477750` draw-side slot count (330 B) | `0047776F`, `004777B0`, `004777BB`, `004777E4`, `0047780B`, `0047781B`, `00477828`, `00477860`, `00477869`, `0047788C` |
| `00520D30` authored command `0x1D` (190 B) | `00520D3A`, `00520D44`, `00520D48`, `00520D5C`, `00520D71`, `00520D85`, `00520D97`, `00520DB5`, `00520DC4`, `00520DDC` |
| `004772E0` allocator (139 B) | `004772F6`, `0047730A`, `00477334`, `00477347`, `0047734C`, `00477357` |

Under 128 bytes, read whole: `004776D0`, `00477670`, `003E6F50`, `003E7450`, `003E6A20`, `00477610`, `00520DF0`.

## Cross-subsystem neighbours

**Core runtime scheduling - SERVICE.** The step routine `00477480` asks the scheduling layer for the frame's simulation
step count and does nothing when it is zero - the accessor the settings page describes under its half-rate section.
A shared getter; by role.

**Resource - SERVICE.** The pose applier whose window `00371F2E`..`00371FD4` this page reads belongs to a larger body
(003714A0) that also calls a Resource-layer routine (004780B0) outside that window; not read here, and recorded because
citing the window imports the edge.

The other nine bodies named are Presentation-layer and their edges stay inside it; the pose applier and the random
picker are described by role.

## SWE2-EC7-81 update (2026-09-20) - `003E7450` sequence-index dispatch measured

`003E7450` (88 B) is the `+0x450`-indexed dispatch the pose callers
run: a `-1` index early-outs; else `r9` is computed from
`[rcx+0x400] + word[+0xE]` when that block and its length word are
live (0 otherwise), and `00477370(r10d, r9, &arg)` runs with `r9d`
passed on the stack.
Interior anchor `003E7489` (the `00477370` call).

## SWE2-EC7-84 update (2026-09-20) - `00428B30` bit-3 propagate measured

`00428B30` (265 B) is the `+0x4B7` bit-3 rewrite the sequencer
callers run: bit 3 of the root record's `+0x4B7` is compared to
`edx`, and on mismatch the `word[+0]`/`word[+8]`/`word[+0xA]`
0x740-stride children take `edx << 3` into their own `+0x4B7`
(and-preserve the rest) before `0042EF90(0042D810, &stack)` runs per
child word - stack-cookie framed.
Interior anchor `00428BF9` (the first `0042EF90` call).

`0040AA20` (138 B) is the oscillator tick `0054B1F0` calls while `02CA4390` is armed: `+0x20` accumulates `+0x24` each pass and wraps past the `009002E0` threshold by setting `+0x3F` bit 0; when that bit is consumed the `+0x24`/`+0x28` rates are reseeded from `003D8E50` random draws ~~over the `02CA4380`/`02CA4398` ranges~~ over the ranges `02CA439C` / `02CA4384` added to the bases `02CA4398` / `02CA4380` *(corrected 2026-10-02, OPUS: `0040AA20`+0x50..+0x7F)* - the accumulate-wrap-reseed loop the per-model sway rides.

Interior anchor `0040AA63` (function `0040AA20`).

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives; two appended notes are sharpened

**Attack.** Sections 1 to 4b and the appended notes were turned into checks at their instructions. Every caller set the
page states was re-counted with a raw E8/E9 sweep. Script: `Tools/analysis-kit/gfz-scripts/falsify_pose_sequencer.py`,
output `falsify_pose_sequencer.out`, image `73461d08…`, 0 BROKEN, exit 0. The 1,066-block census is carried, not re-run.

| # | Clause attacked | Result |
|---|---|---|
| Q0 | sizes; the caller sets | **survives**: all 21 sizes. The caller sets are three raisers of `003E7450`, one value caller, one setter caller, one patch-copy caller, one `0x1E` door and one allocator call |
| Q1 | sections 1–2: accessors, table, handles | **survives**: `S` = `+0x400` plus word `+0x0E`, handle `+0x450`; 32 × `0x40` entries at `02CA6CA0`; `serial << 8 \| slot` with the wrap to 1; `n − 1` at `+0xC` |
| Q2 | the crossed setter `00477610` | **survives**: bytes `0F B6 CA` (`movzx ecx, dl`); it compares with and stores from `edx`. Its siblings use `cl` |
| Q3 | the value walk | **survives**: `T` = record + 2 + `rel` + `0x10`; sequence = `T` + off + 2c; value at `+5 + 4f`; -1 when inactive |
| Q4 | start | **survives**: the gates, both only-if-changed drops, `choiceCount` at `T − 2`, the random pick with re-pick |
| Q5 | step | **survives**: the step-count gate (`001EDE80` is 1 outside half-rate), the freeze words, and end actions 0 stop, 1 hold, 2 loop |
| Q6 | section 4: the applier window | **survives**: kind 1; `+0x1E4` / `+0x1E8`; the id search over `0x28`-stride groups |
| Q7 | section 4: the draw side | **survives**: count × 128. `00477E90` tail-jumps to `00504800`, which returns `width << 16 \| height` from the `+0x100` table. The source x / y are indexed by value |
| Q8 | section 4b: commands `0x1D` / `0x1E` | **survives**: all four arms and the `+0x413 + 1` filter |
| Q9 | section 4b: the raisers and the set-up | **survives** |
| Q10 | the appended notes | **survives, sharpened**. `00428B30` writes bit 3 on the record named by word `+0`, and on that record's `+8` child. It then walks that child's `+8` and `+0xA` words through `0042EF90(0042D810)`, rather than writing all three directly. `0040AA20` adds `+0x24 × [01DFE0BC]`, a time factor the note omits |

No correction.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-pose-sequencer-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00477670` | 92 B | takes the entry at `02CA6CA0` + zero-extended `cl` * 0x40 and does nothing unless its dword `+4` equals `ecx`; otherwise reads byte `b` at (word `[r8 + edx*2]` + `r8d`, a 32-bit sum) + dword `+0xC` of the entry * 6 and stores 0 at entry bytes `+0x10 + b` and `+0x18 + b` and 0xFF at `+0x20 + b` and `+0x28 + b` | `00477684`, `00477688`, `0047769C`, `004776A7`, `004776BB` |
| `00504800` | 59 B | calls the callee at `00504800` + 0xF with `ecx` = word `+0x100 + edx*2` of `rcx` (`edx` sign-extended) and returns 0 when it returns null or bit 0 of its byte `+0x1C` is clear; otherwise returns its word `+0x1E` shifted left 16 OR its word `+0x20` | `00504807`, `0050480F`, `0050481C`, `0050482A`, `0050482D` |
