---
contract: route every gameplay roll to one of four generators and keep their streams apart - which consumer draws from which, what reseeds each, and therefore what can correlate with what   # <- corrected 2026-10-02, OPUS: not every gameplay roll - the CRT rand() (IAT 008C3098, 48 call sites in 30 functions, among them 002FA1A0 at 002FA1BB-002FA1D9) also serves gameplay and is not routed here; see section 2
category: 21-RNG-And-Determinism
scope: subsystem
level: L2
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 21-RNG-And-Determinism/which-roll-is-on-which-generator.md
entries: ["00328370", "00328D80", "002342F0", "00863D30", "00379CF0", "0015BCF0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the generator inventory, both censuses, the reseed paths and the correlation adjudication
    are the page's, carried with their site citations and their corrections. OPUS assembled and
    scoped this contract on 2026-09-20 and did not re-derive the bodies.   # <- corrected 2026-10-02, OPUS - falsification pass 1 (2026-09-29) re-derived every static claim from the shipping image, and EXP-144 executed the routing (section 13)
last_reviewed: 2026-09-29
audit:
  by: OPUS
  date: 2026-09-20
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-falsification-1 - ten claims survive re-derivation from the image; I5's ownership of the graphics
    MT's two index cells is refuted (the twist 0018EE20 resets both) and its census bound corrected to +0x9C0
---

# Contract — which generator serves which roll

> **Why this exists alongside `CONTRACT-gameplay-generators.md`.** That contract is `scope: family`
> and it is correct: it specifies **how the two gameplay generators draw**. This one is
> `scope: subsystem` and specifies **which consumer draws from which, and what follows** — the
> invariants that hold *across* the operations rather than inside one. S-46's second page,
> `which-roll-is-on-which-generator.md`, had no contract at all.
>
> **Provenance**: **[page]** marks that page's reading. **[live]** marks what only a running game
> settles. ~~Nothing here is executed.~~ The routing was executed in `EXP-144` (§13) *(corrected 2026-10-02, OPUS: `EXP-144`, `s46-generator-routing`, 9 cases, superseded §13's nothing-executed line on 2026-09-22)*.

## 1. Purpose

Whether two things in the game can be correlated — whether grinding a fight can shift a loot roll,
whether a reload rerolls your luck — is decided by **which generator each roll comes from**. This
states that routing.

## 2. Interface

~~Four generators~~ Four of the image's generators *(corrected 2026-10-02, OPUS: at least eight exist, and a fifth, the CRT `rand()` — IAT `008C3098`, 48 call sites in 30 functions plus the thunk `00861F38` — also decides gameplay: `002FA1A0` returns `rand() % (900·tb) + 1200·tb` at `002FA1BB`–`002FA1D9`; rng-streams.md §8g. This routing does not cover it)*, and they are not interchangeable **[page]**:

| # | generator | state | seeded by | drives |
|---|---|---|---|---|
| 1 | **Gameplay MT19937** | `02EB3870` (624 dwords), index `02EB4230` | constant **4537** at boot; **the wall clock** on save load | combat formula (53 sites), weather — ~~66 consumer functions~~ 67 consumer functions, 66 through `00379CD0` and the camera-shake sampler `0037D1F0` through `00379CE0` *(corrected 2026-10-02, OPUS: `callers 00379CE0` = 9 sites, all in `0037D1F0`; CONTRACT-gameplay-generators.md §12c)* |
| 2 | **Graphics-noise MT19937** | `01F7F600` (624 dwords); ~~**no index of its own**~~ an index kept as a `u32*` cursor at `+0x9C0` and a `u32` refill count at `+0x9C8`, both set by the twist *(corrected 2026-10-02, OPUS: `0018EECD` `mov dword [r10+0x9c8], 0x270`, `0018EED8` `mov qword [r10+0x9c0], r10`; I5 as corrected 2026-09-29)* — see I5 | time and clock, `0015BCF0` | presentation noise only — **one drawing body, `001946E0`** |
| 3 | **Shared gameplay LCG** | `022C256C` | **a counter**, once per battle-area init | loot, the enemy chain, weighted action selection, spawn placement, AI order |
| 4 | **Presentation bit-feedback PRNG** | `01EF93E8` | constant `0x458DC800` at startup | procedural rendering |

## 3. Types

No type of its own; the states above and the counter at `0208E6B0`.

**Declared in the store 2026-09-21 (OPUS), under the accepted types-MET criterion** (SWE2-AUDIT-SEM, `8f7050694`: a cell cannot reach MET while a contract-named piece of state sits outside the store). Each width and direction is taken from the access instructions, not the name:

| state | declared type | width | what the instructions show |
|---|---|---|---|
| `0208E6B0` | `AreaEntryCounter` | `u32` | two references, both in `002342F0` — read `00234301`, write `00234315` |
| `02089300` | `RngReseedGate` | `u32` | five references; three reads, all comparisons; writes `002368F8` and `00236A44` |
| `01FD4A80` | `TickCounter01FD4A80` | `u32` | `inc` at `0022A59F`; read once at `005843B4` as `imul eax, …, 0x258` |
| `02EB3870` `02EB4230` | `Mt19937State` | `0x9C4` | already declared; `02EB4234` is the byte AFTER it, see below |
| `02EB4234` | `GeneratorInitLatch` | **`u8`** | six references, ALL byte-wide: `cmp byte,0` ×3 and `mov byte,1` ×3 |

**`02EB4234` is a byte, not a dword**, which matters because it sits at `02EB3870 + 0x9C4` — exactly one past `Mt19937State`'s extent. Adjacency is not membership, and the test-then-set pairing in three near-identical functions shows a do-once guard rather than generator state.

## 4. Preconditions · postconditions · invariants

**I1 — TWO MERSENNE TWISTERS, DISJOINT STATE.** Generators 1 and 2 are the same algorithm and
**different instances**: every instruction touching `02EB3870` lives in four functions, and the
graphics pair (`0018D740` / `0018EE20`) **touches none of them** **[page]**.

**I2 — ONE CENSUS METHOD GIVES THE WRONG CONSUMER LIST, IN EITHER DIRECTION.** This is the
subsystem's methodological invariant and it was learned by being wrong:

* Censusing the **multiplier constant** `0x41C64E6D` finds **24 instruction sites — eight draw
  sites**. These are where the recurrence is **written**: the **inliners**.
* Censusing **calls** to `00328370` finds **23 sites in 15 functions**. These are where the stream
  is **drawn** by everyone who did not inline it — spawn placement, the combat AI, the party stance
  timer, weighted-id resolution.
* **The two populations are different, and neither is the consumer list on its own** *(struck and
  corrected 2026-09-14 by OPUS adjudication of `FABLE-CONTRA-WHICHROLL-LCG-CONSUMERS`; the earlier
  text claimed a call census "sees one draw site", wrong in both halves)* **[page]**.

**I3 — ALL LCG CONSUMERS SHARE ONE STREAM, NOT MERELY ONE ALGORITHM.** Every site reads the same
state `022C256C`, so **every draw by any of them moves the others along** **[page]**.

**I4 — THE LCG'S SEED IS A COUNT OF AREAS ENTERED SINCE LAUNCH, AND NOTHING ELSE.**
`RNG_SharedGameplayLCG_SetState` has exactly **one** caller, and the counter at `0208E6B0` is
**touched at exactly two instructions in the whole image** — the read and the write. Nothing
initialises it from a clock, nothing restores it from a save, nothing resets it. **So the LCG is
seeded 0, 1, 2, 3 … once per battle-area initialisation, counting from process start** **[page]**.

**I5 — THE GRAPHICS MT HAS A FIXED STATE ADDRESS, `01F7F600`, ~~AND KEEPS NO INDEX OF ITS OWN~~ AND KEEPS ITS INDEX AS A POINTER AND A COUNT, NOT A `u32`.**
*CORRECTED 2026-09-29 (OPUS, falsification pass 1): the index clause and the ownership paragraph below were wrong; see pass 1.*
*The original reading is corrected here, 2026-09-22 (OPUS).* It was true that
`GraphicsNoiseMT19937_TwistState` (`0018EE20`) has **no rip-relative operand at all**, and the
inference drawn from it — *do not go looking for an address that may not exist* — was wrong,
because it asked what the **callee** names instead of what the **callers** pass. **Every call site
in the image passes one fixed address as a literal `lea`**: `0015BD13` and `0015BD1F` in the seeder
`0015BCF0`, and `0019483B` and `001948C9` in the noise-texture builder `001946E0` — four sites, three
calls, all `lea rcx, [rip -> 01F7F600]`. The types store had this from 2026-09-21; this contract had
not caught up.

**The consumer census is exhaustive and it is two bodies.** Counting every rip-relative operand into
~~`[01F7F600, +0x9C4)`~~ `[01F7F600, +0x9C0)`, the 624-dword array itself, image-wide *(bound CORRECTED 2026-09-29: `+0x9C4` is the
type's extent and contains `01F7FFC0`, which `001946E0` does reference)*: **zero bodies touch the 624-dword array directly**, and exactly two
take its address — `0015BCF0`, which seeds it from two time calls and tail-jumps into the twist, and
`001946E0`, which draws from it. So *presentation noise only* is now backed by a complete count
rather than by the absence of a counter-example: **there is one drawing body in the executable**.

~~**And the two cells above the array are the consumer's, not the generator's** (`CON-155`).~~
**CORRECTED 2026-09-29 (OPUS, falsification pass 1): the two cells above the array are the generator instance's index, as a
pointer and a count, and the twist resets them.** `0018EE20` opens `mov r10, rcx` and ends `mov dword ptr [r10 + 0x9c8], 0x270` /
`mov qword ptr [r10 + 0x9c0], r10` / `ret` (`0018EECD`, `0018EED8`). So every twist sets the count to 624 and the cursor to the
array's start. The consumer then tests the count, twists when it is zero, decrements it, and reads through the cursor. The stores
are register-relative, which is why a rip-relative census missed them. The original text follows, struck where wrong:
`01F7FFC0` is walked as an **8-byte pointer** — `mov rax, qword ptr [01F7FFC0]` / `mov ecx, [rax]` /
`add rax, 4` / `mov [01F7FFC0], rax` at `00194855`–`00194862` — and `01F7FFC8` is a **refill count**
that gates the twist and is then decremented. ~~Neither generator routine touches either: `0018EE20`
has no operand at or above `+0x9A0`, and~~ *(refuted: the twist writes both)* `0018D740` has ~~one operand~~ two operands there, `lea rdx, [rcx + 0x9bc]` and `lea r10, [r9 + 0x9bc]` *(corrected 2026-10-02, OPUS: `0018D761` and `0018D76C`)*, the array's
end sentinel. The gameplay instance is the opposite case — its own seeder writes its index at
`02EB4230`, 4 bytes, across four bodies. **So `Mt19937State`'s `index` field is the gameplay
instance's and not a property of the type**, on the same principle the type row already used to
keep the gameplay lazy-init byte out of it. *That conclusion survives pass 1, for a different reason: both instances keep an
index beside the array, but the gameplay one is a `u32` at `+0x9C0`, and the graphics one is a `u32*` at `+0x9C0` plus a `u32`
count at `+0x9C8`. The layouts differ; the ownership (the generator's, not the consumer's) is the same.*

**I6 — THE CORRELATION ANSWER, AND HALF THE ORIGINAL CLAIM WAS REFUTED.** *Restated 2026-09-14.*

* **On the MT**: hit/miss, damage variance, guard and parry, knockback, poach, the percent gates.
  **A formula outcome cannot move the loot stream** — this half stands.
* **On the LCG, with loot**: AI order evaluation, spawn placement, the party stance timer,
  weighted-id resolution.
* **So fighting DOES shift a loot roll — through the decisions the AI takes, not through the
  numbers the formula produces.** The original "no amount of fighting shifts a loot roll" is
  **refuted** in that half. The converse stands: **the loot path never touches the MT** **[page]**.

## 5. State

`02EB3870` + `02EB4230` (gameplay MT) · `022C256C` (LCG) · `0208E6B0` (the area counter) ·
`01EF93E8` (presentation PRNG) · `01FD4A80` (second input to the save-load seed — **its ROLE is now
established even though its runtime value is not: a monotonic counter**, see §14) ·
`DAT_02089300` (the gate on the LCG reseed).

## 6. Relationships

`CONTRACT-gameplay-generators.md` specifies how generators 1 and 3 draw; **this contract specifies
who draws from them**. The presentation PRNG's own draw law is
`CONTRACT-authored-expression-evaluation.md` (S-10) — **and its startup constant `0x458DC800` is the
seed that contract's fixture uses**. The gameplay MT's boot constant is S-01's `I1`, and its
save-load reseed is S-01's `I2`.

## 7. State transitions

```
boot        : MT <- 4537 (constant)         PRNG <- 0x458DC800 (constant)
area init   : LCG <- counter++ at 0208E6B0, gated on DAT_02089300     (I4)
save load   : MT <- wall clock mixed with 01FD4A80                    (S-01 I2)
every draw  : the LCG's consumers all advance ONE shared stream       (I3)
```

## 8. Script · resource · event interactions

None directly; the consumers are gameplay systems.

## 9. Determinism

**This is the subsystem that decides what "deterministic" means for the whole game**, and the answer
differs per generator: the **PRNG** and the **boot MT** are constant-seeded ~~and reproducible~~ — the boot MT's seed is fixed but its position at the first gameplay draw is not established *(corrected 2026-10-02, OPUS: the boot frame modes draw and discard at `0022B706` / `0022B7EB` once per dispatch, and camera shake's float draws advance the same cursor; CONTRACT-gameplay-generators.md §9, narrowed 2026-09-14, and §12c)*; the
**LCG** is reproducible only for a given count of areas entered since launch (I4); the **MT after a
load** is not reproducible at all, being clock-seeded. **A determinism claim that does not say which
generator it is about is not a claim.**

## 10. Failure paths and edge conditions

* **`DAT_02089300` false** → the LCG reseed is skipped. There **is** an unconditional clear of it in
  `BattleStorage_InitializeWorkArrays`, so the gate is reachable in code; **~~whether it is ever false~~
  ~~in normal play is not established~~** **[page]** *(answered from the code, not observed: `002368D0`, the only clear, is called once, from boot `0022A0B0` at `0022A41A`, and `00236A40`, the only set, once, from boot frame mode 0 `0022B6E0` at `0022B77C` — so the gate is 0 only between boot initialisation and boot mode 0, and 1 for the rest of the process; 2026-10-02, OPUS)*.
* **Counter never resets** (I4), so the LCG's seed grows monotonically for the whole process.

## 11. Observable behaviour

Reloading rerolls to-hit and damage but **not** the loot stream's position. Entering areas changes
where the loot stream starts. Fighting shifts loot **through AI decisions** (I6).

## 12. Reproduction formula

Implement the four generators as **four separate states**, and route each consumer by I2's *two*
censuses — **an implementation that wires consumers from the call census alone will miss the eight
inliners, and one that uses the constant census alone will miss the fifteen callers**. Seed the LCG
from a process-lifetime counter, not from a clock or a save (I4).

## 13. Runtime validation

**None for the routing.** The generator *algorithms* are covered elsewhere —
`CONTRACT-gameplay-generators.md` is `DIFFERENTIAL TESTED` for **the algorithm only**, its own
readiness note saying *"the streams the game actually sees are not"* — and S-10's `EXP-070` executed
the presentation PRNG with no stubs. **Neither executes the routing this contract states.** The
censuses, the reseed paths and the correlation answer are static readings **[page]**.

~~**UNLINKED / nothing-executed, no exemption added**, consistent with today's other contracts.~~
*Superseded 2026-09-22: `EXP-144` (`s46-generator-routing`, 9 cases, stable ×3, published
`4913242bb`) executed the routing this contract states — all four generator states planted
distinguishably, one consumer per route. LCG inliner `003185D0` and call-site consumer `00239210`
both advance `022C256C` identically (I3); MT consumers `0025ABA0(2)`/`0038DB10`/`00389670` advance
only `02EB3870`; presentation PRNG `004005E0` advances only `01EF93E8`; the gfxMT seeder chain
`0015BCF0`→`0018D680`→`0018D740`→`0018EE20` writes only `01F7F600` (I1 natively, and I5 resolved —
the graphics MT state IS fixed); negative control `0025ABA0(1)` touches no generator **[EXP-144]**.
Scripted boundaries are disclosed in the record. Verdict adjudication on I1–I6 remains the
auditor's.*

## 14. Unresolved

* **What `01FD4A80` holds** — its runtime *value* is still not in the image (zero-filled `.data`
  tail) **[page]**, but **its ROLE was established 2026-09-21 (OPUS) and the cell is no longer a
  blank**: it has exactly two references in the whole executable, `0022A59F` `inc dword ptr
  [01FD4A80]` and `005843B4` `imul eax, dword ptr [01FD4A80], 0x258`. One incrementer, one consumer,
  and the consumer scales the count by **600**. Two references image-wide means that producer and
  consumer pair is **complete, not sampled**. So the second seed input is a monotonically rising
  counter read once and multiplied by 600 — *what unit the 600 converts to is not claimed*, and the
  value at any given save still requires runtime observation.
* ~~**Whether `DAT_02089300` is ever false in play** (§10) **[live]**.~~ *(answered from the code, not observed: `002368D0`, the only clear, is called once, from boot `0022A0B0` at `0022A41A`, and `00236A40`, the only set, once, from boot frame mode 0 `0022B6E0` at `0022B77C` — so the gate is 0 only between boot initialisation and boot mode 0, and 1 for the rest of the process; only a live capture would confirm it; 2026-10-02, OPUS)*
* **How often the AI draw paths run during a fight** — the open part of I6, and the thing that would
  quantify how much fighting shifts loot **[page]**.

## 15. Evidence

~~Entirely the page's~~ The page's readings, re-derived from the shipping image in falsification pass 1 (2026-09-29, below) and executed for the routing in `EXP-144` (§13) *(corrected 2026-10-02, OPUS: the pass re-derived every static claim, `falsify_which_generator.py`)*, including its two published corrections — the two-census distinction and the
refuted half of the correlation claim **[page]**. This contract's contribution is I1–I6 stated as a
subsystem contract, §9's rule that a determinism claim must name its generator, and §12's warning
that either census alone wires the wrong consumers.

## 16. Parity plan

For each generator, seed it as §7 says and compare the **state after N draws**. Then the routing:
drive a formula roll and assert **the LCG state is unchanged**; drive a loot roll and assert **the
MT state is unchanged**; drive an AI order evaluation and assert **the LCG state DID change** — that
third assertion is I6's refuted half and the one a plausible implementation gets wrong. Enter two
areas and assert the LCG seed incremented by exactly one each time (I4).

## Falsification pass 1 — 2026-09-29 (OPUS): ten claims hold; I5's ownership of the graphics MT's index is refuted

Every static claim was re-derived from the shipping image (`73461d08…`) by
[`falsify_which_generator.py`](../../Tools/analysis-kit/gfz-scripts/falsify_which_generator.py). Its output is in
[`falsify_which_generator.out`](../../Tools/analysis-kit/gfz-scripts/falsify_which_generator.out). The sweeps decode every
listed body in `.text`, and each check states its killer first.

| check | killer searched for | result |
|---|---|---|
| W0 §3 `02089300` | a sixth access, or a read that is not a comparison | survives: 5 references, the three reads are `cmp`, writes `002368F8` and `00236A44` |
| W1 §3 / I4 `0208E6B0` | a third access | survives: read `00234301`, write `00234315`, both in `002342F0` |
| W2 §3 `01FD4A80` | another access | survives: `inc` at `0022A59F`, `imul …, 0x258` at `005843B4` |
| W3 §3 `02EB4234` | a wider access | survives: six references, all byte-wide, `cmp 0` ×3 and `mov 1` ×3 |
| W4 I1 | a fifth function in the gameplay MT state, or the graphics pair in it | survives: `00863BF0`, `00863C80`, `00866B90`, `00866D60` |
| W5 I2 | another census count | survives: the multiplier at 24 sites in 8 functions; `00328370` from 23 sites in 15 functions |
| W6 I3 | an inliner that does not read `022C256C` | survives: none of the 8 |
| W7 I4 | a second caller of `RNG_SharedGameplayLCG_SetState` | survives: `00328D80` ← `002342F0` (`00234320`) only |
| W8 I5 | another `lea` of `01F7F600`, a reference inside the array, a third toucher of the cells above it | survives: the four cited `lea`s; nothing inside `[01F7F600, +0x9C0)`; `01F7FFC0` and `01F7FFC8` referenced rip-relative only by `001946E0`; the walk at `00194855`–`00194862`; `0018D740`'s sentinel |
| W9 §2 | another boot seed; another consumer count | survives: `mov ecx, 0x11b9` (4537) into `00379CF0`; 66 consumer functions |
| W10 §2 | another presentation seed | survives: `mov [01EF93E8], 0x458DC800` at `00259180` |
| W11 | the refuting check | **the claim "neither generator routine touches either cell; `0018EE20` has no operand at or above `+0x9A0`" is FALSE.** `0018EE20` ends `mov dword ptr [r10 + 0x9c8], 0x270` / `mov qword ptr [r10 + 0x9c0], r10` with `r10 = rcx`, so every twist resets the count to 624 and the cursor to the array's start |

**The correction and why the error happened.** The 2026-09-22 reading, and `CON-155` with it, counted rip-relative operands.
The twist addresses its instance through `rcx`, so its two stores were invisible to that census. An absence claimed from a
census of one addressing form is not an absence. I5 is corrected above: the index is the generator instance's, kept as a
pointer and a count. The types-store rows that inherited the ownership claim (`GraphicsNoiseDrawCursor`,
`GraphicsNoiseRefillCount`, and `Mt19937State`'s `index` note), and `CON-155` itself, are corrected in the same commit.
The consumer record is [`which-generator-falsification-pass-1-0929`](../_index/candidates/which-generator-falsification-pass-1-0929/README.md).

**Also corrected:** I5's census bound, `+0x9C4` to `+0x9C0` (the type extent against the array).

## Cross-subsystem neighbours — SWE2-STRUCT (pass-22 dispositions)

- **ActorEntity - CLIENT and SERVICE (4 edges).** BattleSystem_InitializeAreaState (`002342F0`), RNG_SharedGameplayLCG_NextU32 (`00328370`) are called by bodies filed to ActorEntity: `00236210`, `002394C0`, ActorSystem_InitializeManagerRuntime (`0026CE60`); `00239210` reaches bodies filed to ActorEntity: ActorWork_GetBattleUnit (`0031B760`) - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT (3 edges).** RNG_SharedGameplayLCG_NextU32 (`00328370`) is called by bodies filed to CombatAI: AiOrder_EvaluateAndResolveActionTarget (`003014C0`), AiOrder_CheckActionPreconditions (`00301830`), AiOrder_SelectFinalTargetFromCandidates (`003087E0`) - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - SERVICE (3 edges).** BattleSystem_InitializeAreaState (`002342F0`) reaches bodies filed to CombatAction: `00306570`, BattleActionSnapshot_ResetPool (`0030E010`), BattleAction_ResetPendingQueueBanks (`0030FE60`) - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT (4 edges).** `00389670` is called by bodies filed to CombatFormula: `00388250`, `003889F0`, `00390190`, `00390240` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT (2 edges).** `00259180`, RNG_MT19937_Seed (`00379CF0`) are called by bodies filed to CoreRuntimeScheduling: `0022A0B0` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT (1 edge).** RNG_SharedGameplayLCG_NextU32 (`00328370`) is called by bodies filed to Gameplay: `00312B40` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (10 edges).** RNG_SharedGameplayLCG_NextU32 (`00328370`) is called by bodies filed to Movement: `00239210`, `00312DF0`; BattleSystem_InitializeAreaState (`002342F0`), `00239210` reach bodies filed to Movement: Actor_SetDesiredMovementHeading (`0026A0D0`), Actor_SetFacingHeading_Variant1 (`0026B620`), `0031BD60`, `00322220` (+4 more) - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT (1 edge).** RNG_SharedGameplayLCG_NextU32 (`00328370`) is called by bodies filed to Party: BattleUnit_SeedPartyCombatStanceRecheckTimer (`003081E0`) - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT and SERVICE (4 edges).** GraphicsNoiseMT19937_TwistState (`0018EE20`), Renderer_CreateRandomNoiseTextureFromGraphicsMT19937 (`001946E0`), `004005E0` are called by bodies filed to Presentation: `0018D850`, Renderer_CreateRandomNoiseTextureFromGraphicsMT19937 (`001946E0`), `004010A0`; Renderer_CreateRandomNoiseTextureFromGraphicsMT19937 (`001946E0`) reaches bodies filed to Presentation: `0061E200` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT and SERVICE (2 edges).** Loot_RollNormalSlotChance (`003185D0`) is called by bodies filed to Rewards_Progression_Economy: Loot_RollDropEntries (`003180F0`); BattleSystem_InitializeAreaState (`002342F0`) reaches bodies filed to Rewards_Progression_Economy: Loot_InitializeWorldPickupPool (`00319B10`) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT (1 edge).** RNG_MT19937_Seed (`00379CF0`) is called by bodies filed to Save_Load_Settings: SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG (`00584210`) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (1 edge).** `00239210` is called by bodies filed to Script_VM_Native_Bridge: `00510760` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT and SERVICE (7 edges).** RNG_SharedGameplayLCG_NextU32 (`00328370`) is called by bodies filed to Spawn_Encounter_Lifecycle: Spawn_TrySelectCandidatePosition (`00234AF0`), Spawn_PrepareRandomCandidateForCurrentEntry (`002355A0`), SpawnPoint_GeneratePositionFromAuthoredRegion (`00236450`), SpawnKeep_InitializeEntriesFromDefinitionTable (`002395A0`) (+1 more); BattleSystem_InitializeAreaState (`002342F0`) reaches bodies filed to Spawn_Encounter_Lifecycle: SpawnKeep_RotatePersistenceBanksForAreaTransition (`00233780`), SpawnGroup_ResetLifecycleLedger (`00307090`) - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - SERVICE (1 edge).** BattleSystem_InitializeAreaState (`002342F0`) reaches bodies filed to Status_Periodic_Terminal: BattleStats_RemoveStatusMode0 (`0030E990`) - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (1 edge).** BattleSystem_InitializeAreaState (`002342F0`) is called by bodies filed to World: `00266D10` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (5 edges).** `0025ABA0`, RNG_SharedGameplayLCG_SetState (`00328D80`) are called by bodies filed to WorldAreaField: BattleSystem_InitializeAreaState (`002342F0`), `0025ACA0`; BattleSystem_InitializeAreaState (`002342F0`), `0025ABA0` reach bodies filed to WorldAreaField: `002658B0`, `002FA520`, FieldData_GetActiveFieldRecordBit15 (`00377C20`) - shared machinery across the layer boundary, no shared ownership.
