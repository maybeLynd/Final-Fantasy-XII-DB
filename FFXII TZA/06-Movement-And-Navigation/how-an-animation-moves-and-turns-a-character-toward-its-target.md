---
system: How an animation moves and turns a character toward its target - authored command 0x1A, the request pool, the per-frame profiles of the @FRM entry, and the step the actor update takes
category: 06-Movement-And-Navigation
status: AUDITED
owner_layer: PrimaryOwner:Movement
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the command handler 00520C10, the request builder 003E6340 (657 B), the pool routines 003AF2B0 and 003AED70
    (371 B), the per-frame consumer 003AEF90 (655 B) with its wrapper 003AF220 and the record-side door 003E6EF0, the
    record query 0041F2F0 and the FRM lookup window 0041D318..0041D36E disassembled from the authority image and read,
    2026-09-20; the profile format the consumer implies then parsed out of every animation container and every
    authored 0x1A command checked against it
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-anim-move-turn-falsification-pass-1
  crossref_clean: true
  reopened_count: 0
  note: written by FABLE. Static plus one data census. The consumer side - the actor update applying a clamped step and
    a facing pair - was already on the heading page; this page supplies what fills it. NOT read - the battle unit's
    answer to selector bit 3, the FRM entry's other parts, where the record's own profile (mode 0x16) comes from, the
    last 0x50 bytes of the consumer. The census is staged and owed as evidence: a peer holds the evidence tree. First review = the 0929
    promotion sweep: promoted DOCUMENTED -> AUDITED 2026-09-30 by SWE2-AUDIT-SPEC: falsification pass-1
    (opus-anim-move-turn) FAILS 0 reproduced; the A6 refutation is corrected in place at section 2
    (strike + rewrite); four classified neighbour edges dispositioned; zero open boxes
---

# How an animation moves and turns a character toward its target

When a character attacks, it steps in and swings round to face what it is hitting; when it dodges, it slides. None of
that is movement in the navigation sense and none of it is baked into the bone motion. It is **asked for by the
animation** - one authored command, `0x1A`, naming a **profile** - and carried out frame by frame by the actor update,
which adds a small clamped step and a small turn **toward the target** according to curves stored in the character's
animation container.

## 1. The request - command `0x1A`

`00520C10` (61 B) requires the record's active presentation entry to have a motion section, then calls
`003E6340(record, mode)` with the command's word `+2`:

1. **Ask the owner where things are.** `0041F2F0(record, 0x0C, view)` (65 B) zeroes a 64-byte view, stamps it with two
   record fields and hands it to the owning actor's presentation-view request - the battle unit's view builder
   ([the battle-unit field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)), whose selectors are bit
   flags. Bit 2 puts the **world position of the actor behind the unit's packed target handle** into the view while the
   battle-state word's bit 4 is up; bit 3 was not read.
2. **Nothing to do** if the view's reference point equals the record's own position in x and z (`003E6395`..`003E63BB`).
3. **Build the request**: the unit vector from the record's position `+0x140`..`+0x148` toward the target; a
   **distance** (for most modes; zeroed unless the view says there is a target); and a **relative heading** - the
   angle from the record's facing frame `+0x180` to the target (`00424370`). Mode `0x10` and modes 3 and 4 use the
   reference point and a distance of 1; mode `0x0A` with record byte `+0x2AF` = 3 takes the long way round (heading
   minus two pi).
4. **Queue it** on the record's list at `+0x550` (`003E6589`).

## 2. The pool

`003AF2B0`, run by the character render system's initialiser, allocates **128 entries of `0x60` bytes** at
`[02B3F530]` - the block after the light pool - and clears a serial and two off switches. `003AED70(list, request)`
refuses while ~~either switch is up or the list is disabled~~ **the first switch `02B3F53C` is up, the list's `+0x28` is
non-zero or its `+0` is zero (`003AED70`..`003AED83`); the second switch `02B3F540` is not tested here but by the
consumer `003AEF90` (`003AEFA5`), so with it up requests still queue while nothing advances or frees (corrected 2026-09-29, OPUS falsification pass 1, `CON-186`)**, takes
the first free entry, copies the `0x20`-byte request
to `+0x20`, records the **signs** of the two heading floats at `+8` / `+0xC`, arms a *move* byte `+2` and a *turn* byte
`+1`, and links the entry into **the record's own list** - the pool is global, the lists are per character.

## 3. The profiles - the `@FRM` entry

When a presentation entry is set up (`0041D318`..`0041D36E`) it finds the `@FRM` section of its resource - every
animation container has exactly one ([the container](../17-Presentation-Rendering/Model-And-Motion-Formats/frp-object-container.md)) -
and keeps two offsets: the entry body, and **body + the dword at body `+8`**. The second is the **profile table**, and
the record hands it to the consumer as list `+8`:

```
table[mode]   u32   offset of the profile from the table, 0 = none
profile       u32   duration, in frames
              u16   moveFrames      u16  turnFrames
              f32   scale
              u32   offset of the speed curve from the profile   -> u16[moveFrames]
       +0x10  u16 pairs                                          -> the two turn-rate curves, [turnFrames]
```

In one party member's container the table has 24 modes. The speed curves are **bells** (3409, 9427, 14241 ... 21461
... 3409 over twelve frames), **ease-ins** and **decays** (65533 down to 852 over ten); the turn curves ramp to 65534;
six modes turn without moving and six move without turning.

## 4. The step - `003AEF90`, once a frame

The actor update calls `003E6EF0(record, &move, &turn, maxStep)` (84 B), which refreshes the list's table pointers and
calls `003AF220`; that runs `003AEF90` over the list and then **clamps the summed move to `maxStep`**
([the heading page](heading-speed-to-position-delta.md) has the consumer: the step goes to the position, the pair to
the facing and pitch). For each entry:

- the frame counter `+4` goes up; past `duration` the entry is unlinked and freed (`003AF05A`..`003AF088`);
- **while the counter is below `moveFrames`** and the move byte is set: `move += direction x speed[frame] x distance x
  scale x timebase` (`003AF08A`..`003AF0FB`) - so the curve is a *share of the distance to the target* per frame, and a
  lunge covers the same fraction of the gap whatever the gap is;
- **while it is below `turnFrames`** and the turn byte is set: each of the two heading accumulators advances toward the
  request's absolute heading by at most `turnRate[frame] x scale x timebase`, signed by the request, and the increment
  is written to `turn` (`003AF10F`..`003AF1DA`) - the character closes the angle along the curve and stops when it is
  closed;
- **mode `0x16` does not use the table**: its profile is the record's own, list `+0x10`; with none, the entry is
  dropped (`003AEFF4`..`003AF03B`).

## 5. What the files hold

A census of every animation container (staged; its evidence folder is owed - a peer task holds the evidence tree):
**12,876** `0x1A` commands, the total of the authored-command census. **1,652 carry mode `0x16`**, all in monsters'
containers. Of the other **11,224**, **11,200 name a profile that is present in their own container, and every one of
those profiles is sane** - duration 1 to 600, curve inside the file - a reading that could have failed eleven thousand
times. The remaining 24 name a slot that is empty in their own container and filled in a sibling container of the same
character; what the engine plays for those was not settled. Named profiles: 4,923 turn only, 4,154 move and turn,
2,110 move only. Modes authored: 0-7, 9-12, 16, 21, 22; the commonest are 12 (2,344), 16 (2,145) and 6 (1,908). The
command sits in `attack`, `avoid`, `magic`, `ev_treasure` and `ability` blocks.

## 6. What a reimplementation must keep

- The step-in is **proportional to the distance at the moment of the command**, shaped by a curve, clamped per frame
  by the actor update; it is not root motion and the bone data does not contain it.
- The target is whatever the **battle unit** reports when the command fires; a command with no target still turns
  nothing and moves nothing.
- 128 requests exist for the whole scene; a 129th is dropped silently.
- Two global switches and a per-list enable can stop all of it; they were not traced to their setters.
- Position changes here are part of combat spacing - two clients that play different animations diverge in position.

## Evidence

| body | interior anchors |
|---|---|
| `003E6340` request builder (657 B) | `003E636A`, `003E6390`, `003E6395`, `003E63BB`, `003E63DB`, `003E6406`, `003E642E`, `003E648A`, `003E64AA`, `003E64AF`, `003E64F8`, `003E650C`, `003E6541`, `003E6554`, `003E6589` |
| `003AED70` pool take (371 B) | `003AED76`, `003AED81`, `003AED92`, `003AEDA8`, `003AEDBF`, `003AEDD7`, `003AEDE0`, `003AEDF7`, `003AEE12` |
| `003AEF90` per-frame consumer (655 B) | `003AEFA5`, `003AEFD5`, `003AEFF4`, `003AEFF8`, `003AF043`, `003AF054`, `003AF06F`, `003AF08A`, `003AF0A6`, `003AF0B1`, `003AF0CA`, `003AF0FB`, `003AF10F`, `003AF134`, `003AF14F`, `003AF17A`, `003AF18C`, `003AF1A3`, `003AF1D2` |
| `003AF220` clamp (136 B) | `003AF239`, `003AF23E`, `003AF271`, `003AF27F`, `003AF287` |

Under 128 bytes, read whole: `00520C10`, `0041F2F0`, `003E6EF0`, `003AF2B0`.

## Cross-subsystem neighbours

**Presentation - PRODUCER.** The command, its handler, the request builder, the pool and the `@FRM` lookup are the
presentation layer's; this page is filed under movement because what they produce is a position and a facing.

**Actor entity, combat action - DATA.** The target comes from the owning actor's battle unit through its
presentation-view request; read for selector bit 2 only.

**Resource - SERVICE.** Section lookup by tag and name; used by result.

**Core runtime - SERVICE.** The frame-rate word and time base scale the counters and the step.

## Falsification pass 1 — 2026-09-29 (OPUS): the request, the pool, the profiles and the step survive; the two switches gate different stages

**Attack.** Sections 1 to 4 were turned into checks at their instructions. The caller chain was re-counted with a raw
E8/E9 sweep. Script: `Tools/analysis-kit/gfz-scripts/falsify_anim_move_turn.py`, output `falsify_anim_move_turn.out`,
image `73461d08…`, 0 BROKEN, exit 0. The staged profile census is carried; the page's *not read* items stay open.

| # | Clause attacked | Result |
|---|---|---|
| A6 | section 2: "`003AED70` refuses while either switch is up or the list is disabled" | **refuted** (`CON-186`). The take tests `02B3F53C` with the list's `+0x28` / `+0`; the consumer tests `02B3F540` |
| A0 | sizes; the chain | **survives**: all seven. Command → builder → take; door → clamp → consumer |
| A1 | section 1: the request | **survives**: the motion-section gate; the zeroed 64-byte view; the x / z exit; `+0x180`; `+0x2AF`; the queue on `+0x550` |
| A2 | section 2: the pool and the take | **survives**: 128 × `0x60` allocated once; the request copy; the sign pair; the move and turn bytes; the counter starting at -1 |
| A3 | section 3: the `@FRM` window | **survives**: the table sits at body + the dword at body `+8` |
| A4 | section 4: the step | **survives**: duration and move windows × the frame-rate word; the curve indexed by counter / word; mode `0x16` |
| A5 | section 4: the clamp | **survives**: `min(maxStep, |move|)` along the move's own direction |

Corrected in place: section 2's switch sentence. The consumer record is
`_index/candidates/anim-move-turn-falsification-pass-1-0929/`.
