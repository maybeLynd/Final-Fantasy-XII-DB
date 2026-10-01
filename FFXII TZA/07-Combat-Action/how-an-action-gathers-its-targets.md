---
system: How an action gathers its targets - the area radius, the cone and the line, the side rule, and the two action-row bytes that carry them
category: 07-Combat-Action
status: DOCUMENTED
owner_layer: PrimaryOwner:CombatAction
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: Battle_BuildActionTargetSet 0030D160 (1,004 B), its per-candidate predicates 002FFEF0, 0030BB10 and 0030BCB0,
    and the shape-descriptor builder 0031A990 (154 B) disassembled from the authority image and read whole, 2026-09-19;
    the relationship classifier 0030AB40 re-read against the 2026-09-12 answer on the gambit page; the bytes and bits
    the code reads then tallied over all 543 shipped action rows with four predictions that could have failed
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-action-targets-falsification-pass-1
  note: written by FABLE while placing two of FRONTIER's uncited bodies (0030BB10, 002FFED0). Static plus one data
    census. Corrects my own 2026-09-18 sentence on the action-row page that the flag-word immediates 0x200000 and
    0x3000000 "are not the action row's" - they are, and this routine is where they are read. NOT read - the
    eligibility mask builder beyond its result, the three callers of the shape descriptor's wrapper, what the
    action state machine does around the call. Pending first review
---

# How an action gathers its targets

The player, a gambit or a foe's AI picks **one** target. Everything else an action hits is decided later, in one
routine, from two bytes and four bits of [the action's definition row](Action-Definition-Row/the-action-definition-row.md):
a **radius**, an **angle or width**, and flags that say whether the area is a circle on the target, a circle on the
actor, a cone or a line. Who inside the area is hit is decided **by which side the primary target is on** - not by
which side the actor is on - and confusion is deliberately left out of that judgement.

## 1. When, and with what

`Battle_BuildActionTargetSet(actor, actionId, focusHandle, buffer)` - `0030D160` - has one caller, the standard action
state machine, at `00304EE2`: the action id is the unit's *effective* id, the focus handle is the action context's
`+0x60`, and the buffer is the context's target buffer at `+0xC8`
([the target buffer contract](CONTRACT-battle-target-buffer.md)). It returns the buffer's count.

1. The **primary target** is resolved from the focus handle; if it does not resolve the routine returns 0 and the
   buffer is left alone (`0030D18A`..`0030D195`).
2. The buffer is reset - its header bit 0 survives - and the primary is appended first (`0030D1F3`..`0030D200`).
3. The action row is `table + stride x id` off `02EBF138` (`0030D19B`..`0030D1E9`).

## 2. The area

Nothing more happens unless the row's byte **`+0x06`, the radius**, is non-zero (`0030D255`..`0030D26B`). It is compared
squared, against the squared distance in the ground plane (`0030D2BD`, `0030D3A3`..`0030D3AC`).

| row field | meaning | where read |
|---|---|---|
| `+0x06` u8 | **radius**; 0 = the primary target only | `0030D255` |
| `+0x0C` bit 21 | the circle is centred on the **actor**; clear = on the **primary target** | `0030D271`..`0030D28F` |
| `+0x0C` bit 24 | **cone**: a candidate must also lie within the half-angle of the heading from the actor to the primary target | `0030D3B1`..`0030D3E1` |
| `+0x0C` bit 25 | **line**: the candidate's offset from the actor is rotated into that heading and its sideways component must not exceed the half-width | `0030D3E3`..`0030D419` |
| `+0x07` u8 | cone: **half-angle in degrees** (converted with 2 pi / 360 at `0030D300`); line: **half-width** in the radius's units | `0030D2EC` |

The heading is computed once (`0030D2D2`..`0030D2E7`), from the actor's position to the primary target's, falling back
to the actor's own facing when the two coincide.

Every live unit slot is a candidate (`0030D313`..`0030D339`). A candidate is skipped if it **is** the primary; if it
fails the ordinary target eligibility test, asked with the actor as the relation context (`002FFEF0`, 85 B: it
classifies actor against candidate and hands the eligibility mask builder "hostile" or "not hostile" -
`0030D353`..`0030D366`); if it is on the wrong side (section 3); if it is outside the radius; or if it is outside the
cone or the line.

## 3. The side rule

Row word `+0x36` carries two bits of it (`0030D36C`..`0030D391`):

| `+0x36` | who in the area is hit | predicate, called as `(primary, candidate, 1)` |
|---|---|---|
| bit 3 set | **everyone** - no side test | - |
| bits 2, 3 clear | units **on the primary target's side** | `0030BB10` (27 B): skip when the class is 0 or 2 |
| bit 2 set | units **on the other side from the primary target** | `0030BCB0` (24 B): skip when the class is 0 or 1 |

Both predicates are one-line wrappers of the relationship classifier `0030AB40`
([what it returns](../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md): 0 unrelated, 1 friendly, 2 hostile,
inverted when the *first* unit is Confused unless the third argument has bit 0). Two things follow from how they are
called here:

- The first unit is the **primary target**, not the actor. Fira thrown at a foe spreads to that foe's allies; Cura on
  a party member spreads to the party; and either, aimed at the other side, spreads on the other side. The actor's
  side never enters.
- The third argument is **1**, so the classifier ignores confusion. A Confused primary target does not turn the
  splash inside out. (The eligibility test of section 2 passes 0, with the **candidate** as the first unit, so there a Confused
  candidate's relation to the actor *is* inverted - one classifier, two different questions.)

`002FFED0` (23 B) belongs with `002FFEF0`: it is the same eligibility question with no relation context - "is the
eligibility mask empty" - and its one caller is the manager predicate 00322490
([the availability page](Action-Availability/battle-command-availability-and-reason-codes.md)), which asks it of a
unit with arguments `(unit, 0, 3)`.

## 4. The two tails

**Slot targets.** When the actor's pending-result count `+0x6B6` is already non-zero - the action was committed against
a battle *slot* rather than a unit ([the field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)) - none
of the above runs. If the row has a radius, the routine rebuilds the slot list instead: every mapped slot 4..8 of kind
3 that resolves contributes its stats byte `+4` to `+0x6B9[]`, and the new count goes to `+0x6B6`
(`0030D205`..`0030D250`). With no radius the committed single slot stands.

**The whole party.** After the area pass, if the row's flag bit 1 is set, the four party positions are walked and every
member that has a stats record and is not KO, Stone or Vanished (`0x80000003`, waived by the active field record's bit
15) is appended unless already present (`0030D461`..`0030D50A`).

## 5. What the files hold

[`census.py`](../_experiments/evidence/action-area-bytes/census.py) ->
[`census.out.txt`](../_experiments/evidence/action-area-bytes/census.out.txt), all 543 rows.

| test | result |
|---|---|
| rows with a radius | **247**: 3 (9), 4 (8), 5 (2), 6 (46), 8 (63), 10 (98), 15, 18, 20 (6), 100 (13) |
| P1 `+0x07` non-zero only with bit 24 or 25 | holds for 52 of the 53 rows with a non-zero `+0x07`; the exception is *Remora Strike* (6, 180) with neither bit - its angle is never read |
| P1 a cone or line always has a radius | **all 54** |
| P2 bits 24 and 25 never together | **none** |
| P3 radius-0 rows carry none of bits 21, 24, 25 | **none do** |
| P4 single / area pairs | Fire 0, Fira 8, Firaga 8, **Firaja 100**; Blizzard / Thunder the same; Cure 0, **Cura 10**, Curaga 0, **Curaja 10**; Protect 0, Protectga 10; Haste 0, Hastega 10; Dispel 0, Dispelga 10; Esuna 0, Esunaga 10 |

- **Centred on the actor (bit 21), 26 rows:** Screech, Scream, Wail, the Soundwaves, Angelsong and the other songs,
  Rage - the cries and songs, radius 8 or 10.
- **Cones (bit 24), 49 rows:** Darkness, Ice Break, Water Spout, Shining Ray, Tremor, Tempest, Sandstorm, Pyromania,
  the Gazes, Flash, the Bubbles, Breath - half-angles of 40, 45, 60, 75, 80, 120 and 180 degrees; **180 on 32 of them, which makes the "cone"
  a full circle around the actor**, and 0 on two, which leaves the primary target alone in practice.
- **Lines (bit 25), 5 rows:** Gust (3, 2), Gale (5, 3), Judgment, Innocence, Mach Wave (20, 10).
- **Side rule:** 245 of the 247 area rows hit the primary target's side; **Self-Destruct** has bit 2 (the primary is
  the bomb itself, so: the other side) and **Mass Destruct** has bit 3 (everyone).
- **Whole party (bit 1):** set on 13 rows, all of them the unnamed *Reserve* placeholders - **no shipped action uses
  it**.

**A second reader agrees on the shapes.** `0031A990(row, out)` (154 B) turns the same fields into a descriptor:
shape **0** single, **1** circle on the target, **2** circle on the actor, **3** cone (radius, half-angle in radians),
**4** line (radius), **5** whole party. It adds one thing the gatherer does not know: flag **bit 12** makes it report
"no area" even when the row has a radius. The 18 rows with bit 12 and a radius are the Quickenings and the Espers'
finishers (Red Spiral, White Whorl, Pyroclasm, Fires of War ...), radius 10 - they *do* splash, by section 2, but
whatever consumes the descriptor is told they do not. Its wrapper (which also reports the action's default target side from flag bit 11 and the
actor's own side) has three callers; one of them is among the battle menu's entry helpers
([the selection the menu publishes](../16-UI/the-selection-the-menu-publishes.md)), so the descriptor feeds target
selection in the menu at least. The other two were not read.

## 6. What a reimplementation must keep

- One chosen target; the rest gathered from **positions at the moment the state machine makes the call**, not at the
  moment the target was chosen. *Which step of the action that is - before or after the charge - was not read.*
- Distance in the ground plane only; a radius of 100 (the -ja spells) is "everything on the map" in practice.
- Side by the **primary target**, confusion ignored; eligibility by the **actor**, confusion seen.
- Cone and line are measured **from the actor toward the primary target**, while the radius is measured from
  whichever centre bit 21 selects.

## Evidence

| body | interior anchors |
|---|---|
| `0030D160` gatherer (1,004 B) | `0030D18A`, `0030D195`, `0030D19B`, `0030D1E9`, `0030D1F3`, `0030D200`, `0030D205`, `0030D20E`, `0030D227`, `0030D23A`, `0030D249`, `0030D255`, `0030D271`, `0030D28F`, `0030D2BD`, `0030D2C0`, `0030D2E7`, `0030D2EC`, `0030D300`, `0030D313`, `0030D339`, `0030D34A`, `0030D35F`, `0030D36C`, `0030D37C`, `0030D38D`, `0030D3A3`, `0030D3AC`, `0030D3B1`, `0030D3D9`, `0030D3E3`, `0030D3FF`, `0030D419`, `0030D422`, `0030D461`, `0030D482`, `0030D4A1`, `0030D4A9`, `0030D4EB`, `0030D4FF`, `0030D51C` |
| `0031A990` shape descriptor (154 B) | `0031A995`, `0031A99E`, `0031A9A5`, `0031A9AC`, `0031A9B2`, `0031A9C2`, `0031A9CF`, `0031A9E5`, `0031A9EC`, `0031A9F4`, `0031AA13`, `0031AA19` |

Under 128 bytes, read whole: `002FFEF0`, `002FFED0`, `0030BB10`, `0030BCB0`.

## Cross-subsystem neighbours

**Combat AI - SHARED HELPER.** The relationship classifier and its two wrappers are filed with the gambit evaluation,
which owns the definition of "friendly" and "hostile"; this page uses them by result.

**Actor / battle unit - DATA.** The candidates are battle-unit slots and the positions are the unit's `+0xE0`; the
pending-result fields `+0x6B6` / `+0x6B9` are the field map's.

**World / field - SERVICE.** The field record's bit 15 waiver is the same one every `0x80000003` test in the engine
consults.

**Combat formula - SERVICE.** The effective action id the caller passes comes from the formula layer's effective-id
getter, and the slot tail resolves stats records through that layer's mapped-slot getter; both used by value and
named by role, because naming their addresses would import every other caller they have.

**Gameplay, Movement - IMPORTED BY CITATION.** Citing the call site `00304EE2` names the standard action state machine,
whose other callees sit in the Gameplay and Movement layers, and the classifier `0030AB40` has Gameplay
callers of its own. None of those edges is part of gathering targets; they are recorded because the citation imports
them.

**UI - CLIENT.** The manager predicate 00322490, named in section 3 as the one caller of `002FFED0`, is itself called
from the UI layer; not read here.

**Presentation - MECHANICAL (SWE2-EC7-96, 1 edge).** `002FFF50` — the apply this page's `002FFEF0`
section cites — calls `003125E0` on the Presentation layer. Shared-helper fan-out; no Presentation
relationship to target gathering.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Party - SERVICE (2 edges).** `Battle_BuildActionTargetSet` (`0030D160`) calls `BattleUnit_ResolveByFocusHandle` (`0031B7E0`), a 42-byte Party-filed body that, only while bit `0x10` of `02089340` is set, resolves the packed focus handle through the actor registry and returns that actor's battle unit (else 0); and the manager predicate `00322490` starts by calling `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) to get the player's current focus actor. Target gathering turns the focus handle it is given into a battle unit through the party layer's resolver, and the manager predicate tests the party's focused unit; the party layer owns the focus handle, this page only consumes it.

## SWE2-EC7-96 update (2026-09-20) - `0030BB10` + `002FFEF0` measured

`0030BB10` (27 B) is the narrow predicate `0030D160` and
`003230E0` wrap: `0030AB40` masked by `~2` - true only when the
raw result is 0 or 2, the "empty or exactly-paired" answer the
availability path asks for.
Interior anchor `0030BB14` (the `0030AB40` call).

`002FFEF0` (85 B) is the gated apply `0030D160` and `003247F0`
run: both pointers non-null plus `0030AB40` above 1 upgrades
`edx` to 1 for `002FFF50`, and the return is `eax == 0` - the
success-when-zero convention the gather path reports.
Interior anchor `002FFF14` (the `0030AB40` call).

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives, including the indirect side-predicate call

**Attack.** Sections 1 to 5 and the appended notes were turned into checks at their instructions. The competing case
for section 3: a raw E8/E9 sweep finds **no** direct call from the gatherer to either side predicate. That would
refute the page if the calls were direct. They are not. The gatherer loads `0030BB10` with `lea`, keeps `0030BCB0` in
`rbp`, picks one by `+0x36` bit 2 (`cmovne`) and calls it through `rax` at `0030D38D`. Script:
`Tools/analysis-kit/gfz-scripts/falsify_action_targets.py`, output `falsify_action_targets.out`, image `73461d08…`,
0 BROKEN, exit 0. The 543-row census is carried, not re-run.

| # | Clause attacked | Result |
|---|---|---|
| T0 | sizes and callers | **survives**: all six. The gatherer's caller is `00304EE2`; `002FFED0` is called as `(unit, 0, 3)`; the shape wrapper has three callers |
| T1 | section 2: the area fields | **survives**: radius `+0x06`, squared; bit 21 for the centre; `+0x07` × 2π / 360; bits 24 and 25 |
| T2 | sections 2 / 3: the eligibility call | **survives**: `002FFEF0(candidate, actor, 1)`, whose classifier call is `(candidate, actor, 0)` |
| T3 | section 3: the side rule's predicates | **survives** (the competing case above): an indirect call with `(primary, candidate, 1)`; bit 3 bypasses it |
| T4 | section 3: the two predicates | **survives**: 0 or 2 → skip; 0 or 1 → skip |
| T5 | section 4: the two tails | **survives** |
| T6 | section 5: the shape descriptor | **survives**: shapes 0–5, and bit 12 means no area |
| T7 | the SWE2-EC7-96 notes | **survives** |

No correction. Instrument lesson, recorded: a raw E8/E9 caller sweep does not see `call rax`. An absence of callers
from it cannot refute a stated call without a read of the calling window.
