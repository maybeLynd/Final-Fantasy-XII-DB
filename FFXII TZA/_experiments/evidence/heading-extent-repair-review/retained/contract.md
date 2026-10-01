---
contract: Turn a heading, a pitch and a speed into a position delta, behind an actor-class gate that refuses in silence
category: 06-Movement-And-Navigation
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 06-Movement-And-Navigation/heading-speed-to-position-delta.md
entries: ["002E4380", "00265020"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants read from the
    shipping bytes — **both class gates taken at their instructions and compared as idioms**, and
    **both refusal paths followed to what they write**, which is the fact §4's third invariant turns
    on. **This records checks performed on that date, not the method of the original derivation**,
    which is on the locomotion page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-heading-delta-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — heading, speed and the position delta

> **Authored 2026-09-22 by FABLE.** S-18's contract column carries one contract over three pages.
> **This takes the locomotion page.**
>
> Written against FRONTIER's adequacy test. **`LD-2` and `LD-3` are why this is not
> operation-scoped:** two functions test the *same field* with *different idioms* and accept
> *different sets*, and both refuse by writing a plausible value instead of a status — a pair of
> facts neither body can state alone.

## 1. Purpose

Convert where an actor is facing and how fast it is going into how far it moves this frame.

## 2. Interface

| | body | note |
|---|---|---|
| **the delta** | `Movement_ComputeDeltaFromHeadingSpeed` (`002E4380`), 601 B | yaw + pitch + speed → a 4-vector |
| **the position** | `Actor_GetWorldPosition` (`00265020`), 61 B | the wider gate, and the one that lies most quietly |

**Two arms this table did not state** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 307, which executed both bodies; bytes re-read.)*:
- **`r8d != 0` is a pass-through.** The output is the caller's vector `r9` with W = 1.0 (`002E43EE`–`002E4409`), and
  the movement context's `+0xF8` becomes `sqrt(|v|²)` through the square-root helper (`002E43B7`–`002E43E6`). No yaw, pitch or speed is
  consulted.
- **Speed 0 short-circuits to `{0, 0, 0, 1}`**, the same output as the refusal (`LD-2`). This one rests on OPUS's
  execution.

## 3. Types

```
WorldActor
  +0x03   u8     top three bits are the actor class (LD-1)
  +0xB8   ptr    the movement / position block

movement state
  +0xA0   f32    pitch
  +0xA4   f32    yaw
  +0xD0   f32    speed
```

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**LD-1 — One actor-class gate, and it is a precondition of the whole API rather than a quirk of one
function.** `002E439A`–`002E43A2` reads `byte [actor + 3]`, masks `0xE0` and requires `0x60` —
class 3. The same gate stands in `Movement_SetRequestedSpeed`,
`Actor_SetDesiredMovementHeading`, this body, and **twice** in `Movement_UpdateActorFrame`.

**LD-2 — `Actor_GetWorldPosition` tests the SAME field with a DIFFERENT idiom and accepts a WIDER
set.** `00265025`–`00265038` does `shr r10d, 5` — taking the class as a *value* `0..7` — then
`sub 1` / `je` and `cmp 2` / `jne`, which admits classes **1 and 3**. It also **null-checks the
actor first** (`00265020`), which the movement gate does not.

> *So the field has two readings in the same subsystem: a masked equality that admits one class, and
> a shifted value compared twice that admits two.* **A reimplementation that unifies them is wrong in
> one direction or the other**, and which direction depends on which body it standardises on.

**LD-3 — BOTH refusals are silent and BOTH write a plausible value. Neither returns a status.**
`00265052` writes **zero into all three position outputs** and returns — *a refused position is the
world origin, which is a legal coordinate.* `002E45C9` writes `0x3F800000` — **`1.0f`** — into the
delta's W and returns. **So a caller that ignores the class receives well-formed data rather than an
error**, and the two failure values are exactly the ones that look least like failures.

**LD-4 — The delta is a SPHERICAL decomposition, not a planar one — except under the flat-movement condition**
(the page's §4). There the pitch term is dropped: Y = 0, and X / Z are not scaled by `cos(pitch)`. OPUS executed
both branches *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 307, which executed both bodies; bytes re-read.)*. Otherwise: pitch both supplies the
vertical term and foreshortens the horizontal one:

```
X = sin(yaw) · cos(pitch) · speed
Y = sin(pitch)            · speed
Z = cos(yaw) · cos(pitch) · speed
```

*A port that treats movement as planar and adds Y separately agrees on flat ground and diverges on
every slope, because it loses the `cos(pitch)` factor on X and Z.*

**LD-5 — The output is FULLY INITIALISED even when refused, and the two halves are written in
different places.** `002E438E`/`002E4394` zero X, Y and Z **before the gate is tested** — a qword
and a dword, twelve bytes — and W is written **on the exit path**. *So the refused result is
`{0, 0, 0, 1.0}` and not a partially written vector, which is why `LD-3`'s silence is survivable and
also why it is hard to notice.*

**LD-6 — Both angles are wrapped into ~~`(−π, π]`~~ `[−π, π]` before use** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 307, which executed both bodies; bytes re-read.)*. The shipped wrap
(`002E4464`–`002E44EF`) adds `±π` by sign, subtracts a truncated multiple of `2π`, then subtracts the `±π` again.
That maps `+π → −π` and `−π → +π`, so both endpoints are reachable. It uses the truncating-`fmod` idiom the
page describes in §4. *Carried, not re-derived here.*

## 5. State

**Read:** the actor class byte, and the movement block's pitch, yaw and speed. ~~**Written:** only the
caller's output vector.~~ **Written:** the caller's output vector, **and the movement block's `+0xF8`** - `sqrtf(|v|²)` on the pass-through (`002E43E6`), and the speed when `+0xF8` is negative on the
decomposition path (`002E445C`). *This body owns nothing.* *(Corrected 2026-09-29, OPUS, falsification pass 1, `CON-167`.)*

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-facing-and-steering.md`](CONTRACT-facing-and-steering.md) — S-18's first |
| **Producers of `+0xA4` / `+0xD0`** | the combat-side movement intent, and the animation-state override |
| **Same gate** | the speed setter, the heading setter and the frame driver (`LD-1`) |

## 7. State transitions

*class gate → wrap both angles → decompose → write the delta.* On refusal: *zero X/Y/Z, write
W = 1.0, return.*
*(Made exact 2026-09-29, pass 1: gate → pass-through when `r8d != 0`; otherwise the `+0xF8` sentinel repair → wrap →
`00424080`, when `[actor+0xC0]` is live, which may change the wrapped yaw and the speed → speed-0 test → decompose.)*

## 8. Script · resource · event interactions

None directly. The angles and speed arrive from the combat-side intent or the animation-state
override.

## 9. Determinism

Deterministic. No generator is drawn.

## 10. Failure paths and edge conditions

- A wrong actor class yields `{0,0,0,1.0}` with no status (`LD-3`, `LD-5`).
- A null actor, or a class other than 1 or 3, yields the world origin from the position getter
  (`LD-2`, `LD-3`).
- The two gates disagree about class 1 by construction (`LD-2`).

## 11. Observable behaviour

An actor of the wrong class simply does not move, and anything that asked where it was is told the
world origin — which is why a mis-classed actor reads as standing at the map's zero point rather
than as an error.

## 12. Reproduction formula

Call the delta with a class byte whose top bits are not `0x60` and assert the output is exactly
`{0,0,0,1.0}` (`LD-3`, `LD-5`). Call the position getter with class 1 and assert it **succeeds**,
then with class 2 and assert `(0,0,0)` (`LD-2`). Call it with a null actor and assert the same
`(0,0,0)` (`LD-2`). Feed a non-zero pitch and assert X and Z are scaled by `cos(pitch)` (`LD-4`).

## 13. Runtime validation

~~**None.** No experiment executes these bodies.~~ **Superseded 2026-09-25:** OPUS's replay executes both bodies
(block 307; `_index/candidates/s18-opus-replay-delta-and-position/`), and that is the source of the four
additions above. S-18's runtime cell is not addressed by this
contract — *and that cell's gap is separately recorded as 92 bodies executed across `EXP-132`–`137`
whose records name no contract, which is a different half of S-18 and is not claimed here.*

## 14. Unresolved

- [ ] Whether any caller depends on the refused `{0,0,0,1.0}` rather than merely tolerating
      it. **REOPENED, narrowed (2026-09-29, OPUS, `CON-172`, on ASTRA `2ada8a5a0`).** What stands:
      - `002E4380`'s only call edge is `002E50CB`;
      - the caller's own class-3 gate at `002E5077` dominates it.

      What fell is the premise that closed the rest. The body run between the two gates is
      `Movement_UpdateSteeringTowardTarget`. It is called at `002E50B8` with the same actor, when the movement
      mode byte `[[+0xB8]+0xF0]+0x29` is 1–4.
      - It is **963 B, eight chained unwind fragments**. The 40 bytes read as "a leaf" are its prologue
        fragment, which has no `ret`; the only `ret` is `002E49A2`.
      - It makes **21 calls**.
      - The body itself has no direct `+0x03` operand. Whether any callee can change the actor's class byte
        is not established, so **neither is "the refusal never executes"**.

      Closing this needs the 21 callees' effects on `[actor+3]`, or an execution that shows the class across
      the call.
      Regression: `falsify_heading_delta.py` H8 validates the extent through the chain before counting calls.
      ~~**CLOSED 2026-09-23 (SWE2-CONTRACT): nobody can observe it.** `002E4380` has exactly
      one call edge image-wide — `002E50CB`, inside `Movement_UpdateActorFrame` (`002E5030`,
      pdata fragments `002E5030`–`002E5085` + `002E5085`–`002E515C`; the second fragment has
      **zero inbound edges**, it is fallthrough-only). The call is dominated by the caller's own
      identical gate: `002E5077` tests `byte[rbx+3] & 0xE0 == 0x60` (after the lifecycle/`+0xC0`/
      `+0x14F` checks) and every failure exits before `002E50CB`. The one body executed between
      the two gates, `002E45E0`, is a 40-byte leaf — no `+3` writes, no calls — so the class
      cannot change in between. **The refusal never executes in shipped code; it is callee-side
      defence for a caller that does not exist.** "Depends" never arises because "tolerates"
      never arises.~~
- [x] ~~Why the position getter admits class 1 when nothing that moves an actor does
      (`LD-2`).~~ **CLOSED 2026-09-23 (SWE2-CONTRACT), mechanism level:** class 1 is the
      **placed-object** class (K-2/BV-4) — it carries a `+0xB8` block with a readable position
      but no steering record. `00265020` reads `[actor+0xB8] +0/+4/+8` through the *same* path
      for both admitted classes (`0026503A`–`00265051` is shared) — so the wider gate is not a
      different opinion about the field, it is the correct one for a **read-only** query: a
      placed object has a position, it just cannot be steered. `sub 1/je` + `cmp 2/jne` admits
      exactly {1,3} by construction — class 1 is a deliberate operand, not sloppiness. The two
      gates guard different operations: movement writes/steers (class 3 only, because only class
      3 owns a movement context), position reads (classes 1+3, because both own a position).
      *Residual: which of the getter's ~100 call sites actually hand it a class-1 actor is a
      runtime data-flow question, not statically bounded.*

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| `LD-1` — the mask and value | `002E439A`–`002E43A2` read at the instructions | 1 |
| `LD-2` — the wider, differently-written gate | `00265020`–`00265038` read in full: the null test, `shr 5`, `sub 1`/`je`, `cmp 2`/`jne` | 1 |
| `LD-3` — both silent refusals | `00265052`–`0026505C` and `002E45C9`–`002E45D8` followed to their stores and returns | 1 |
| `LD-5` — the split initialisation | `002E438E`/`002E4394` shown to precede the gate test at `002E43A2` | 1 |
| `LD-4`, `LD-6` | [the locomotion page](heading-speed-to-position-delta.md) §§2 and 4, falsified 2026-09-02 | 1 |
| the delta's sole call edge is `002E50CB` in `Movement_UpdateActorFrame`, dominated by the caller's own class-3 gate at `002E5077`; the `002E5085` fragment has zero inbound edges (fallthrough-only) ~~and `002E45E0` between the gates is a 40-byte leaf with no `+0x03` writes~~; **`002E45E0` between the gates is 963 B with 21 calls, so the class's stability between them is not established** (`CON-172`; `falsify_heading_delta.py` H8) | image-wide call/jmp/`lea`/disp32 census + both bodies decoded whole, 2026-09-23 | 1 |
| `00265020` serves classes {1,3} through one shared read path (`0026503A`–`00265051`); class 1 is the placed-object class — readable position, no steering record | `00265020`–`0026505C` decoded whole; class semantics per K-2/BV-4 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on `LD-1` through `LD-6`. **`LD-4` is the one that
decides numerical parity** — dropping `cos(pitch)` from X and Z agrees on flat ground. **`LD-3` is
the one a port improves into a bug**: returning a status from either refusal is better engineering
and changes what every existing caller sees. **`LD-2` is the one a port unifies**, and it must pick
a direction knowingly.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Movement — internal.** The delta, the gate and the movement block are this category's own.
- **ActorEntity — SERVICE, and `LD-1`/`LD-2` are the statements.** The `WorldActor` class byte and
  the `+0xB8` block belong to that layer. **This contract asserts only which bits are read, which
  values each gate accepts, and what each refusal writes** — all visible at the two bodies' own
  instructions — and nothing about what an actor class means.
- **Audio, CombatAction, CombatFormula, Gameplay, Party, Presentation,
  Rewards_Progression_Economy, Spawn_Encounter_Lifecycle and UI — ALL CLIENTS, and all of one
  body.** `Actor_GetWorldPosition` is a hub: bodies across those nine layers call it. **This
  contract asserts nothing whatever about its callers** — `LD-2` and `LD-3` are statements about
  the 61 bytes of the getter itself, which is read in full, and `LD-3`'s point is precisely that
  a caller cannot tell a refusal from a result. *That every one of those layers silently receives
  the world origin on a refusal is the CONSEQUENCE being recorded, not a claim about any of
  them.*
- **Every other layer reached is MECHANICAL**, through these two bodies' own callees — the
  trigonometric helpers among them. *Their addresses are deliberately not cited: `LD-4` is carried
  from the page as a formula and this contract does not re-derive the transcendentals.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun. *"Movement" would otherwise be cleared by the word
> alone.*

## 17. Related

- [Heading, speed and the position delta](heading-speed-to-position-delta.md) — the mechanism
- [Contract — facing and steering](CONTRACT-facing-and-steering.md) — S-18's first

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **ActorEntity - CLIENT (8 edges).** `00265020` is also called by bodies filed to ActorEntity: `00236300`, `0037B4D0`, `003B73B0` - shared machinery across the layer boundary, no shared ownership.
- **Audio - CLIENT (1 edge).** `00265020` is also called by bodies filed to audio: `00362850` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (3 edges).** `00265020` is also called by bodies filed to combat action: `002F8060`, `00307300`, `00320E10` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT (1 edge).** `00265020` is also called by bodies filed to combat formula: `00384F40` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT (2 edges).** `00265020` is also called by bodies filed to Gameplay: `0031ADB0` (CombatAction), `00339630` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (4 edges).** `00265020` is also called by bodies filed to party: `00303CC0`, `00304180`, `00359150`; `002E45E0` reaches bodies filed to party: `003590D0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (7 edges).** `00265020` is also called by bodies filed to presentation: `002B7B80` (UI), `00322360`, `0037AD40` (EffectConstraint) - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT (2 edges).** `00265020` is also called by bodies filed to rewards/progression: `002FB150`, `00312280` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (23 edges).** `00265020` is also called by bodies filed to script VM / native bridge: `0033FD60`, `00344AF0`, `00345180` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT (3 edges).** `00265020` is also called by bodies filed to spawn/encounter lifecycle: `00234AF0`, `00234DA0`, `002350C0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (1 edge).** `00265020` is also called by bodies filed to UI: `003C5130` - shared machinery across the layer boundary, no shared ownership.

## Falsification pass 1 — 2026-09-29 (OPUS): §5's "writes only the output" refuted; the modifier hook added

**Attack.** Every clause of §2-§10 became a check that fails if the shipping image says otherwise. The checks decode every
listed body in `.text`. Script: `Tools/analysis-kit/gfz-scripts/falsify_heading_delta.py`, output
`falsify_heading_delta.out`, image `73461d08…`, 0 BROKEN.

| # | Clause attacked | Result |
|---|---|---|
| H0 | §2 sizes; LD-1 one gate, five sites | **survives**: 601 B / 61 B; `and al, 0xe0` then `cmp al, 0x60` once in the speed setter, once in the heading setter, twice in the frame driver, once here |
| H1 | LD-2 | **survives**: null first, then `shr 5 / sub 1 / je / cmp 2 / jne` (classes 1 and 3); a refusal zeros all three outputs |
| H2 | LD-3 / LD-5 | **survives**: X, Y, Z zeroed before the gate; the refusal exit writes W = 1.0 and returns |
| H3 | §5 "Written: only the caller's output vector" | **REFUTED** (below) |
| H4 | §7 the order of operations | **incomplete** (below) |
| H5 | LD-4's flat branch | **survives**: `00267260 != 0 && 00264460 == 0` leaves Y = 0 and X / Z unscaled |
| H6 | LD-6 | **survives**: two truncating wraps, over `2π` with `±π` added and removed |
| H7 | §9 | **survives**: the 14-body closure reaches no generator and no gameplay-LCG reference |
| H8 | §14's first closure and its §15 row: `002E45E0` is a 40-byte leaf | **REFUTED, added later on 2026-09-29** (`CON-172`, ASTRA `2ada8a5a0`): eight chained fragments tile 963 B; 21 calls; one `ret`. The closure is reopened and narrowed. This pass's H0–H7 never tested §14, so their PASS did not cover it |

* **H3: the body writes the movement block.** `+0xF8` of the movement block (`actor+0xB8`) is written on both live paths:
  * the pass-through stores `sqrtf(|v|²)` at `002E43E6`, as §2's 2026-09-25 note says;
  * the decomposition path repairs a negative `+0xF8` to the speed at `002E445C`.

  So §5's "Written: only the caller's output vector. *This body owns nothing.*" is false. It owns nothing, but it writes
  one field it does not own. [The page](heading-speed-to-position-delta.md) documents both writes. `CON-167`.
* **H4: a modifier runs between the wrap and the decomposition.** When `[actor+0xC0]` is non-null and its first dword is
  not `-1`, `Movement_ModifyHeadingSpeedForObjectState` (`00424080`) receives that record's first word and the wrapped yaw
  and the speed **by address** (`002E4510`). The speed-0 test and the decomposition see its results. §7's
  *"gate → wrap → decompose"* is now *"gate → pass-through or: sentinel repair → wrap → modifier → speed-0 test →
  decompose"*. The page documents the modifier (its `00424080` row).

Consumer record: [`_index/candidates/heading-delta-falsification-pass-1-0929/`](../_index/candidates/heading-delta-falsification-pass-1-0929/README.md).
Contradiction: `CON-167`.
