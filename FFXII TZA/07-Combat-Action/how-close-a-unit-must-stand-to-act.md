---
system: How close a unit must stand to act - the three range bands of an action, where each number comes from, and what locomotion does with them
category: 07-Combat-Action
status: DOCUMENTED
owner_layer: PrimaryOwner:CombatAction
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the band builder 002FEB80, its two leaves 00309300 and 00320D70, and the two locomotion bodies that consume
    the bands (00338140, 00337A50) disassembled from the authority image and read whole, 2026-09-19; the bytes they read
    then tallied over the 543 action rows and 557 equipment rows of the shipped us battle_pack.bin, with three
    predictions the reading makes checked against them
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-range-bands-falsification-pass-1
  note: written by FABLE while placing one of FRONTIER's uncited bodies (00309300). The three floats were already placed
    as storage on the battle-unit field map (unit +0x6D4..+0x6DC, copied to the locomotion block); what they MEAN was
    not written anywhere, and three bytes of the action definition row were listed as having no reader. Static, plus one
    data tally. Not read - the back-off step's own helpers and the avoidance manoeuvre; pending first review
---

# How close a unit must stand to act

When a battle unit starts a standard action, the setup step works out **three distances to its target** and hands them
to locomotion. They are not one "range": they are a **near band** (closer than this and I back off), a **middle band**
(the distance I settle at), and the **reach** (further than this and I cannot act). This page says where each number
comes from and what the mover does with it. Where they are stored is on
[the battle unit field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) (`+0x6D4` / `+0x6D8` / `+0x6DC`,
copied to the locomotion block's `+0x120` / `+0x124` / `+0x128`).

## 1. The builder - `002FEB80` (476 B)

`(actor, target, actionRow, outReach, outMiddle, outNear)`.

1. **The weapon.** The actor's stats record carries its equipped weapon id at `+0x50`; if that id is inside the
   equipment table, its row is resolved.
2. **The bodies.** Each actor has a pair of collision radii; the builder takes the larger of the actor's pair and the
   larger of the target's pair and **adds the two**. Every band below is measured centre to centre, so this sum is added
   to all three.
3. **The inner components** `a` and `b` come from `00320D70` with component 0 and 1 (section 3).
4. **The reach** `R` comes from `00309300` (section 2).
5. **If both components are non-zero** the bands are authored: near = `a`, middle = `a + b`, reach = `a + b + R`.
   **If either is zero** they are proportions of the reach: **near = `0.6 R`, middle = `0.8 R`, reach = `R`.**
   *(CORRECTED 2026-09-29, OPUS, CON-187: this read "if either component is non-zero". `002FECAA` skips the test of
   `b` when `a` is 0, so one zero component is enough for the fallback.)*
6. Each is stored with the radii sum added.

## 2. The reach - `00309300` (169 B)

`(actionRow, weaponId)`. The action row's flag word `+0x0C` **bit 26** decides whose number it is:

- **bit 26 clear - the action's own reach:** the row's byte **`+0x05`, divided by 10**;
- **bit 26 set - the weapon's reach:** the weapon id is checked as an equipment id, its row resolved, and the row's byte
  **`+0x18`, divided by 10** is returned (0 when there is no such row).

So a magick reaches 10.0 because its row says `100`; **Attack-like actions reach as far as what the attacker holds.**

## 3. The inner components - `00320D70` (146 B)

`(actor, actionRow, equipmentRow, component)`, prior art on
[the FCP character parameter block](../17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md)
(section 6.1), restated here because the two halves belong together:

- **bit 26 clear:** the action row's byte **`+0x02 + component`, divided by 10** - so `+0x02` is the near component and
  `+0x03` the middle one;
- **bit 26 set:** the equipment row's **kind byte `+0x25`** picks a pair of per-character tunables - the character's own
  reach with that kind of weapon, read from its parameter block and scaled by its size. **Kind 2, and any kind above 5,
  has no pair: the answer is 0**, and section 1 falls back to `0.6 R` / `0.8 R`. A **null** equipment row (the empty
  `0xFFFF` hand fails the builder's bound) is read as **kind 0** and still gets a pair (falsification pass 1, B7).

## 4. What the data says

[`census.py`](../_experiments/evidence/action-range-bands/census.py) →
[`census.out.txt`](../_experiments/evidence/action-range-bands/census.out.txt), over the shipped `battle_pack.bin`. The
reading makes three predictions and the data could have refuted each:

| prediction | result |
|---|---|
| equipment kind 2, the one kind with no per-character bands, is the long-range kind | its 52 rows have `+0x18` of **100-250** (10.0-25.0) |
| the kinds that do have bands are close-range | kinds 1, 3, 4, 5 (200 rows): `+0x18` of **10-30** (1.0-3.0) |
| an action row with authored inner bytes never has bit 26, which would leave them unread | 6 rows have non-zero `+0x02` / `+0x03` (`1, 20` x 3, `1, 15` x 2, `20, 20` x 1); **none has bit 26** |

35 of the 543 action rows have bit 26. Without it, `+0x05` is `100` on 212 rows, `0` on 121, `30` on 50, `255` on 39.
*The 35 bit-26 rows still carry a `+0x05` (`20` on 19 of them); this body does not read it for them, and what does was
not established.*

**This names three bytes of [the action definition row](Action-Definition-Row/the-action-definition-row.md)** that its
reader census could not: `+0x02` and `+0x03` are read through a computed index (`row + component + 2`), which the census's
one idiom does not follow, and `+0x05` is read two calls away from where the row is resolved.

## 5. What locomotion does with them - `00338140` (839 B)

The target-spacing step of the locomotion solver. With `d` the XZ distance to the target:

- **too far** when `d > min(middle + 2.0, reach)` → the *approach* flag;
- **too close** when `d < near + 0.05` and a further test passes → the *back-off* flag;
- each flag is then dropped again if `d` is already on the right side of the block's approach stop distance (`+0xD0`), so
  a unit at its stop distance is left alone; a failed pair-clearance test forces *approach*.
- **Two units targeting each other** do not fight over the gap: if the target's own focus is this unit and this unit's
  middle band is the larger, the *near* band used is **the target's**, not its own.
- Neither flag: face the target and stand. *Approach*: the pacing routine below. *Back-off*: a clearance-tested step
  away at speed A.

## 6. Pacing an approach to the charge - `00337A50` (442 B)

Runs only while the solver's output flag `0x100` is up and a predicate holds for the actor and not for whoever the
target is focused on. It aims at **`middle + 0.7 x (reach - middle)`** - inside the reach, outside the settle distance -
and compares two times: the charge time the action still needs (`+0x76C - +0x768`, in charge steps) and the time to walk
the remaining distance. If even the fast speed B cannot get there before the charge completes, pacing is abandoned (the
flag is cleared) and the unit just goes. Otherwise it **stands still** for the first 30 steps of the charge and for as
long as it could still arrive on time at speed A, **then walks at speed A** - so a caster ambles into range just as the
spell is ready instead of sprinting there and waiting.

## 7. What a reimplementation must keep

- Three bands per action start, all centre-to-centre: the larger radius of each body is added to every band.
- Bit 26 of the action flags switches BOTH the reach (weapon `+0x18` instead of action `+0x05`) and the inner bands
  (per-character, per-weapon-kind instead of action `+0x02` / `+0x03`).
- Unless both inner bands are non-zero - every ranged weapon, every ordinary magick - near and middle are `0.6` and
  `0.8` of the reach (CON-187: one zero component is enough).
- Spacing uses `min(middle + 2.0, reach)` as "too far" and `near + 0.05` as "too close", with the mutual-target rule.

**Not read:** the further test of the back-off arm, the avoidance manoeuvre, the predicate of section 6, and the clearance
tests; what reads `+0x05` on a bit-26 row.

## Evidence

Every body below was read whole.

| body | interior anchors |
|---|---|
| `002FEB80` band builder (476 B) | `002FEBC3`, `002FEBCA`, `002FEC34`, `002FEC5C`, `002FEC7E`, `002FEC83`, `002FEC9A`, `002FECB3`, `002FECC6`, `002FECD2`, `002FECDF`, `002FECEA`, `002FECFB`, `002FED0F`, `002FED21`, `002FED32` |
| `00309300` reach (169 B) | `00309319`, `0030932E`, `00309355`, `00309377`, `00309380`, `0030938B`, `0030939B` |
| `00320D70` inner component (146 B) | `00320D74`, `00320D93`, `00320D9D`, `00320DB1`, `00320DBC`, `00320DC8`, `00320DE9`, `00320DF5` |
| `00338140` target spacing (839 B) | `0033817F`, `0033818E`, `003381A6`, `00338201`, `00338225`, `0033822E`, `00338253`, `0033825B`, `00338266`, `0033827D`, `00338292`, `0033829B`, `003382B6`, `003382D1`, `003382F2`, `0033830F`, `00338382`, `003383AD`, `003383C5`, `003383E4`, `0033843D`, `00338475` |
| `00337A50` approach pacing (442 B) | `00337A74`, `00337A88`, `00337AA3`, `00337ADF`, `00337AF3`, `00337AFF`, `00337B0F`, `00337B32`, `00337B3A`, `00337B4D`, `00337B75`, `00337B8A`, `00337BB4`, `00337BCC`, `00337BE6` |

Constants: `0.6` at `008F3100`, `0.8` at `008F3108`, `0.7` at `008F3104`, `10.0` at `008F8180`, `2.0` at `01CEBC08`,
`0.05` at `008F30E8`.

## Cross-subsystem neighbours

**Movement - CLIENT.** `00338140` and `00337A50` are locomotion-solver bodies owned by the Movement layer
([battle locomotion](../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md)). They
are this page's consumers: they read the three bands the builder produced and own nothing of how the bands are made.

**ActorEntity - SERVICE.** The builder asks the actor layer for each body's pair of collision radii, and the spacing step
asks it for a battle unit by slot index. Getters only; described by role.

**Party - SERVICE.** Both locomotion bodies resolve the target's focus handle to a unit through the party layer's
resolver - that is how the mutual-target rule of section 5 learns who the target is looking at. Described by role.

**Gameplay - SERVICE.** The reach getter `00309300` asks the Gameplay layer's encoded-id validity test whether the
weapon id is a class-6 (equipment) id before it resolves the row. A shared leaf of the encoded-id space
([the encoded id space](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)); described by role.

**Core runtime scheduling - SERVICE.** The builder and the reach getter turn the equipment table's stored offset into a
pointer through the image-address resolver, as every authored-table reader does.

`003343D0` (955 B) is the band worker `00338140` runs: `003588B0`, `004686D0` x2, `00335760`, `003357B0`, `00265200`, `00203080` x2, `004687F0` x2, `0033CB70` x2, `00334AB0` x2, `00335B60` x2, `00334C30` and `0031EA90` under the cookie check - the locomotion band's per-step evaluation; its closing helpers are shared well outside combat, with `0031EA90` answering to CombatAI-side callers and `00265200` called from Presentation, Script_VM_Native_Bridge, Spawn_Encounter_Lifecycle and UI bodies.

Interior anchor `00334553` (function `003343D0`).

**Rewards_Progression_Economy - CLIENT (1 edge; FABLE 2026-09-29).** `Loot_FindOverlappingPickupIndex` (`002FB150`), owned by that layer, calls the collision-extent pair getter `00265090` that the band builder uses. Only for a class-3 actor are the two outs filled: the getter tail-jumps into a reader with `+0x50` of the object behind `+0xB8` (`00265090`-`002650A5`). The loot test fetches the actor's position, then the pair (`002FB1C1`), and for each of the ten present pickups compares the XZ distance with the larger of the two plus its second argument (`002FB1E5`-`002FB209`); a hit returns the slot index. It borrows the same body radii this page's bands start from, and nothing it computes feeds a reach band. The pickup pool and this search belong to [the world loot pickups page](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md). Read from the shipping bytes.

## Falsification pass 1 — 2026-09-29 (OPUS): section 1's "either component" refuted (CON-187); two additions

**Attack.** Sections 1, 2, 3, 5 and 6 were turned into checks at their instructions, together with the six constants.
Script: `Tools/analysis-kit/gfz-scripts/falsify_action_range_bands.py`, output `falsify_action_range_bands.out`, image
`73461d08…`, 0 BROKEN after the correction, exit 0. The data census of section 4 is carried, not re-run.

| # | Clause attacked | Result |
|---|---|---|
| B0 | sizes, and where the bands land | **survives.** The one builder call is `00304AB9`. It passes reach to unit `+0x6DC`, middle to `+0x6D8` and near to `+0x6D4` (`rsi` = unit + `0x6B0`). The block the copies go to is unit + `0x80`, so block `+0x120` / `+0x124` / `+0x128` are unit `+0x1A0` / `+0x1A4` / `+0x1A8` |
| B1 | section 1.1: the weapon row | **survives, with an addition.** The weapon word is stats `+0x50`. The builder's own bound is one-sided: id < count + `0x1000`, otherwise a null row. The empty sentinel `0xFFFF` fails it. An id below `0x1000` is not tested here |
| B2 | section 1.2: the bodies | **survives.** Two `00265090` pairs, the larger of each, added |
| B3 | sections 1.3 and 1.4 | **survives** |
| B4 | section 1.5: when the bands are authored | **REFUTED (CON-187).** The flag is set only when **both** components are non-zero. `a == 0` jumps past the test of `b` (`002FECAA`), and `b == 0` jumps too (`002FECB1`). An unordered (NaN) compare counts as non-zero |
| B5 | sections 1.5 and 1.6: the formulas | **survives.** Each out pointer is null-tested before its store |
| B6 | section 2: the reach | **survives.** A null action row also gives 0 |
| B7 | section 3: the inner components | **survives, with an addition.** A **null** equipment row (for example the `0xFFFF` hand of B1) is treated as **kind 0**, so it still reads a per-character pair. It is not the "no pair" case. [The FCP page](../17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md) section 6.1 already says "no equipment → 0" |
| B8 | section 5: target spacing | **survives.** The mutual rule reads the target unit's `+0x1A4` / `+0x1A0`, its own copies (B0). Also read: two early exits stop the step, the slot-identity test at `0033818E` and an XZ distance under `0.1` (`008C5F6C`) at `003381AF`. With neither flag set, the avoidance attempt `003343D0` runs before the stand-and-face tail |
| B9 | section 6: approach pacing | **survives, qualified.** A further gate: the step also needs speed `+0xB0` non-zero. The stand window is `30 × [01DFE0B4]`, an `imul` and not a literal. `01DFE0B4` is the frame limit ([boot fixups](../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md)): 1 as shipped, and 2 at 60 fps. So "the first 30 steps" holds at the 30 fps setting and is 60 at the 60 fps one |

**The correction, in player terms.** A weapon kind whose character tunables give one inner band of 0 and the other
non-zero does **not** get authored bands. It falls back to `0.6` / `0.8` of the reach. The six authored action rows of
section 4 all have both bytes non-zero, so no shipped action row changes. The per-character pairs under bit 26 are the
case where the two readings differ, and their values were not tallied here.
