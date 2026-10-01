---
contract: Roll what a dead enemy drops — one shared stream, seven inlined draws, a variable number of them
category: 13-Rewards-Progression-Economy
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md
entries: ["003180F0", "00318510", "003185D0", "003186F0", "00318820", "00317ED0", "003183D0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — every rip-relative access to the shared generator state enumerated by **two
    instruments**, one bounded by the function list and one a linear sweep of `.text` verifying each
    candidate at a real instruction boundary; one inlined draw compared **opcode by opcode** against
    the canonical generator body; the orchestrator's four draw sites read in control-flow order with
    each one's guard; and the generator function's own callers censused as the **control** on the
    inlining claim. **This records checks performed on that date, not the method of the original
    derivation**, which is on the loot page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-loot-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — loot rolls and the enemy chain

> **Authored 2026-09-22 by FABLE.** S-32's binding gap is *"EXP/LP division only, of 5 pages"* — its
> one contract,
> [`CONTRACT-experience-and-licence-award.md`](CONTRACT-experience-and-licence-award.md), covers the
> experience and licence division. **This takes the loot rolls and the chain**; the death sequence,
> the gil paths and the level-up remain uncontracted and this document does not claim them.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is seven
> such invariants, and **LC-1, LC-4 and LC-5 are statements about a shared stream that no single
> roll can make.**

## 1. Purpose

Decide what falls off a dead enemy, and how the kill streak changes the odds.

## 2. Interface

| | body | draws |
|---|---|---|
| **the orchestrator** | `Loot_RollDropEntries` (`003180F0`), 641 B | calls all four, ~~2–13~~ **0–13** times total (LC-4; `CON-175`) |
| pick the chance profile | `Loot_SelectChanceProfileByWeight` (`00318820`) | 1, conditional |
| roll one slot | `Loot_RollNormalSlotChance` (`003185D0`) | 1 per non-empty slot |
| roll its quantity | `Loot_RollNormalSlotQuantityBucket` (`003186F0`) | 1 per kept slot |
| roll an extra item | `Loot_RollAdditionalItemChance` (`00318510`) | 1, twice, each guarded |
| chain on a kill | `EnemyChain_UpdateOnDefeat` (`00317ED0`) → `EnemyChain_TryAdvanceRank` (`003183D0`) | 1 each |
| the chain-rank outcome | `00319530` | 1, **from the periodic tick** (LC-5) |

## 3. Types

```
022C256C  u32   the shared gameplay LCG state -- the ONLY state this subsystem's randomness has
022C3158  u32   the current chain rank 0..3; also the DEFAULT loot chance-profile index (LC-6)
022C3160  u32   the same-model kill counter -> the quantity profile
022C3164  u32   when > 0, the chance profile is drawn instead of taken from the rank (LC-6)

out[7]    7 x 8 B  { u16 itemId (0xFFFF = none), u16 pad, u32 quantity }
                   entries 0..4 the five authored slots, +0x28 and +0x30 the two extras (LC-7)
```

## 4. Preconditions · postconditions · invariants

### The seven cross-operation invariants

**LC-1 — Every loot and chain decision advances the shared LCG, and NOT ONE of them calls the
generator.** The state `022C256C` has exactly **17 rip-relative accesses image-wide — 9 writers and
8 readers** — measured by two instruments that agree exactly (`linear-only = 0`, so no unlisted code
touches it). One reader/writer pair is the canonical `RNG_SharedGameplayLCG_NextU32` (`00328370`);
a ninth writer is its setter. **The other seven pairs are inlined copies**, in
`EnemyChain_UpdateOnDefeat`, `EnemyChain_TryAdvanceRank`, the four `Loot_*` rolls and `00319530` —
**all seven in this subsystem.**

> **CORRECTED 2026-09-22, SAME DAY, BY ITS AUTHOR (FABLE).** This sidebar first read that
> [the gameplay-generators contract](../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md)
> *"cannot see these seven and undercounts the shared LCG's consumers by seven"*. **That was wrong
> and unfair, and it is withdrawn.** Its page
> [`rng-streams.md`](../21-RNG-And-Determinism/rng-streams.md) §"the named function is one draw site
> of eight" already states *"The LCG is inlined — `0x41C64E6D` appears in **8 functions across 24
> sites**"* and tabulates all seven of these by address and owner; the contract's own §6 table
> **says on its face that it is a call-site census**, so it is not claiming to be the consumer list.
> *I checked the answer's addresses only after publishing a claim about them.*
>
> **What survives is corroboration, not correction.** A caller census of `00328370` returns 23 sites
> in 15 functions and **none of those seven** — so the two populations really are disjoint, and this
> contract's census reaches the same eight functions **from the other direction**: `rng-streams.md`
> found them by sweeping the *multiplier constant*, this one by sweeping every access to the *state*
> `022C256C`. **Two unrelated instruments, the same eight bodies.** *That is worth more than either
> alone, and it is all this paragraph claims.*

**LC-2 — The inlined copies are instruction-for-instruction identical to the canonical body, so the
stream is ONE stream.** *(Precision, 2026-09-29, OPUS falsification pass 1. The copy at `00318540` has one extra
register move, `mov ecx, eax` at `00318589`, which it keeps for its own result composition. The three multiply-adds,
the composition and the single writeback are identical, so the step is the same.)* Compared opcode by opcode, `00318540`–`0031858B` against
`00328370`–`003283B9`: the same three `imul 0x41C64E6D` / `add 0x3039` pairs in the same order, the
same `shr 0x10` / mask / `shl 0xa` / `xor` composition, the same single writeback. *An inlined draw
and a called draw are the same step — so interleaving loot with every other LCG consumer is the
design, not a hazard, and a reimplementation that gives loot its own generator changes every
outcome.*

**LC-3 — One draw advances the state THREE times and yields 31 bits.** Three multiply-adds, only the
last stored; the result is `((a>>16 & 0x7FF) << 10 ^ (b>>16 & 0x3FF)) << 10 ^ (s>>16 & 0x3FF)` —
11 + 10 + 10 bits. The `% 100` every roll applies is compiled as a magic-number division
(`00318594 mov eax, 0x51eb851f` / `003185A4 sar edx, 5`). *Three steps per decision, not one.*

**LC-4 — The number of draws per kill is VARIABLE, and depends on authored data AND on the outcomes
of earlier draws in the same kill.** In control-flow order:

| draw | guard |
|---|---|
| profile | only when `[022C3164] > 0` (`0031815C jle`) |
| slot chance ×5 | skipped when the slot's authored id is `0xFFFF` (`003181F8`) |
| quantity | **only for a slot that was kept** (`0031820A`/`00318213`). This includes an **empty** slot: `003181FC` sends a `0xFFFF` slot to the `+0xE64` override at `0031820C`, and a matching index keeps it, storing `0xFFFF` and drawing a quantity (`00318220`) (2026-09-29, OPUS falsification pass 1, `CON-175`) |
| extra item ×2 | each returns without drawing when its id or condition is `0xFFFF`, or the condition query fails (`0031851E`, `00318527`, `0031853A`) |

*So one kill advances the shared state ~~between 2 and 13 draws~~* **by P + C + Q + E draws in the orchestrator** (2026-09-29, OPUS falsification pass 1, `CON-175`):
- P: 1 only when `[022C3164] > 0`;
- C: one per slot whose id is not `0xFFFF`;
- Q: one per kept slot;
- E: 0–2.

Every term can be 0, so the orchestrator's range is **0 to 13**. The chain's own two draws are separately conditional.
*The stream position afterwards is
not a function of the kill alone — it is a function of what the kill rolled.*

**LC-5 — The loot stream is advanced by the PERIODIC TICK, not only by kills.** `00319530` — an
inlined-draw function by LC-1 — has one caller, and it is
`BattleUnit_RunPeriodicCombatMaintenance` at `00311146`, gated two instructions earlier on the unit's
`stats[+0x05]` being zero (`00311130`/`00311136`). *So how many qualifying units are alive and how
long a fight runs both move the generator that decides loot.* This is the same maintenance body
[the periodic tick contract](../10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md) covers, and
the same `stats[+0x05]` selector that
[equipment compatibility](../12-Items-Equipment-Shops-License/CONTRACT-equipment-compatibility.md)
EQ-6 and [enmity](../09-Combat-AI-And-Gambits/CONTRACT-enmity.md) branch on.

**LC-6 — The chain rank IS the default chance profile, and a failed slot can still drop.**
`00318116 mov r12d, dword ptr [rip …]` seeds the profile index from the chain rank `022C3158`, and
`Loot_SelectChanceProfileByWeight` overwrites it **only** when `[022C3164] > 0`. Separately, a slot
whose chance roll fails is not immediately lost: `0031820C` calls a 20-byte accessor reading a
global's `+0xE64` and the slot is kept when that value equals the slot index. *Two ways into a drop,
and only one of them is a roll.*

**LC-7 — The output is seven fixed entries, pre-filled with the null sentinel before any draw, and
quantity is the bucket PLUS ONE.** `0031811D`–`00318158` writes `{0xFFFF, 0}` into all seven before
the first roll; `00318225 inc eax` turns the bucket index into a count. *So bucket 0 means one item,
not none, and a slot that never rolls is left explicitly empty rather than stale.*
**LC-7a — After the rolls, duplicate item ids are MERGED, so a slot that rolled can also end empty** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 349](../_index/candidates/s32-opus-replay-loot-rolls/README.md), which executed it 6/6; `00318290`–`00318370` re-read.)*.
- **Merge.** `003182A0`–`003182D5` walks the seven entries from the last back to the first. Each one's id is
  searched among the entries before it, nearest first. On a match, its quantity is added to that earlier entry and
  its id is overwritten with `0xFFFF`. Walking backwards cascades, so every duplicate ends in the **earliest**
  entry with that id.
- **Clear.** `003182D7`–`0031834F` then zeroes the quantity of every `0xFFFF` entry.
- **Return.** The body returns 1 if any entry still holds an item, and 0 otherwise.

OPUS measured grm_e definition 1 over 400 kills: in 11 of them slots 0 and 2 (id `2074`) were both kept, and entry 0
then held quantity 2 while entry 2 was empty. The static census of the shipped `in` area files has **12**
definitions that repeat a slot id, and **27** that carry an extra whose id repeats a slot. *A port that reports the
seven rolled slots as seven drops shows duplicates the game folds together.*

## 5. State

**Owned:** nothing persistent — the chain globals belong to the chain half and are read here.
**Advanced:** `022C256C`, shared with the whole engine (LC-1, LC-2). **Written:** the caller's seven
entries.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-experience-and-licence-award.md`](CONTRACT-experience-and-licence-award.md) — S-32's contracted fifth |
| **Advances** | [the gameplay-generators contract](../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md)'s shared LCG — **by inlining**, which [`rng-streams.md`](../21-RNG-And-Determinism/rng-streams.md) already records and LC-1 reproduces from the state side |
| **Shares a tick** | [the periodic tick](../10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md) — LC-5 |
| **Shares the selector** | equipment compatibility and enmity, on `stats[+0x05]` (LC-5) |
| **Uncontracted** | the death sequence, the gil paths and the level-up — S-32's other three pages, not claimed here |

## 7. State transitions

Per kill: *chain update → rank advance → profile (rank, or drawn) → five slot rolls → a quantity roll
per kept slot → two guarded extra-item rolls.* The chain rank transitions `0..3` upward only, by
`EnemyChain_TryAdvanceRank`.

## 8. Script · resource · event interactions

The five drop words and the two extra-item ids and conditions are authored on the spawn row; the
chance and quantity profiles are the four authored rows behind `02EBF0C0`; the per-rank chain
thresholds are authored. Nothing here is scripted.

## 9. Determinism

**Deterministic given the stream position** — and the stream position is not local to this
subsystem. LC-4 makes the number of draws outcome-dependent and LC-5 makes it tick-dependent, so
*reproducing a drop requires reproducing everything that drew before it*, not just the kill.

## 10. Failure paths and edge conditions

- A null chance-profile table leaves the slot count at zero and the loop is skipped
  (`00318174`/`00318177`).
- An extra-item entry with either id or condition `0xFFFF` is skipped **without drawing** — so a
  disabled extra does not shift the stream (LC-4).
- The fifth authored slot's chance is 100 in every shipped profile, per
  [the page](loot-drops-and-enemy-chain.md) §8b; this contract does not re-derive the table.

## 11. Observable behaviour

Killing the same enemy repeatedly makes it drop more, and better, and in larger stacks — and two
players who kill the same monster at the same chain rank can still get different loot, because the
generator has been moving all fight.

## 12. Reproduction formula

Sweep `022C256C` image-wide and assert **17 accesses, 8 readers, 9 writers**; then census callers of
`00328370` and assert **none** of the eight reader functions appears (LC-1). Diff `00318540`–
`0031858B` against `00328370`–`003283B9` opcode by opcode and assert equality (LC-2). Kill one enemy
whose slots are all `0xFFFF` and both extras disabled, and assert the state advances ~~**at most once**~~ **at most
twice**: the profile draw when `[022C3164] > 0`, and one quantity draw when the `+0xE64` override names one of the
empty slots. With neither, it does not advance at all (2026-09-29, OPUS falsification pass 1, `CON-175`)
(LC-4). Run a fight with no kills at all and assert `022C256C` still moves (LC-5).

## 13. Runtime validation

~~**None of this subsystem's bodies is executed by an experiment.**~~ **Superseded 2026-09-25:** [OPUS block 349](../_index/candidates/s32-opus-replay-loot-rolls/README.md) executed the loot rolls over a shipped foe with the real gameplay LCG (6/6; 1,881 LCG writes, all exactly three
steps apart), including LC-4's owned-condition guard for extras. The extra-item draw itself is not covered, and the
evidence class is native replay, not live. *The historical sentence continues:* The generators contract records 768
executed draws of `00328370` itself, which is the canonical body and **not** any of the seven inlined
copies; that evidence supports LC-3's step count and nothing else here. S-32's runtime cell is not
addressed by this contract. *Stated rather than left blank so a CONTRACT READY header is not read as
evidence of execution.*

## 14. Unresolved

- What object the `+0xE64` slot override in LC-6 reads, and whether it is a developer facility.
- Whether `[022C3164]` is ever positive in shipped play, which decides if the chance profile is ever
  drawn rather than taken from the rank.
- The three uncontracted pages of S-32.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| LC-1 — 17 / 8 / 9, and the seven inliners | every access to `022C256C` enumerated by **two instruments** agreeing exactly, with a caller census of `00328370` as the **control** — an instrument that saw the seven would contradict the inlining claim, and it returns none of them | 1 |
| LC-2 — identical bodies | `00318540`–`0031858B` and `00328370`–`003283B9` disassembled and compared instruction by instruction | 1 |
| LC-3 — three steps, 31 bits | the three `imul`/`add` pairs and the mask/shift/xor chain read in order; the `% 100` magic constant at `00318594`/`003185A4` | 1 |
| LC-4 — the variable draw count | all four call sites read **with their guards**: `0031815C`, `003181F8`, `0031820A`, and `0031851E`/`00318527`/`0031853A` | 1 |
| LC-5 — the tick advances it | `00319530` censused to one caller; `00311130`/`00311136`/`00311146` read in order | 1 |
| LC-6 — rank as default profile, and the override | `00318116` against `0031815C`–`0031816A`; `0031820C`–`00318213` with the 20-byte accessor disassembled in full | 1 |
| LC-7 — seven entries and bucket + 1 | the fourteen pre-fill stores `0031811D`–`00318158` counted; `00318225` | 1 |
| the four shipped profile rows and the chain thresholds | [the loot page](loot-drops-and-enemy-chain.md) §8b, corrected 2026-09-12, and §8d | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on LC-1 through LC-7. **LC-2 is the one that decides
whether a port can ever match a recording**: giving loot its own generator, or calling a shared one
where the original inlines it, is invisible in a single roll and wrong from the second draw onward.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Rewards_Progression_Economy — internal.** The orchestrator, the four rolls and the chain are this
  category's own.
- **RNG_And_Determinism — SERVICE, and LC-1 and LC-2 are the statement.** The shared state and the
  canonical generator belong to that layer; this contract asserts only how this subsystem reaches
  them — by inlining, which that layer's own page already records — and reproduces its eight-function
  result from the state side. *It asserts nothing about the generator's other consumers, and it
  makes no claim that that layer's census is deficient.*
- **CombatAction — SERVICE.** The periodic maintenance body LC-5 names belongs to that layer; this
  contract states only that it calls `00319530` under the `stats[+0x05]` gate.
- **ActorEntity, Movement, Party, Spawn_Encounter_Lifecycle, CombatAI — MECHANICAL, and their
  presence IS LC-1's subject.** Every one of them is reached as a *caller of the generator
  `00328370`*. **That fan-in is precisely the population a call census finds — and the seven inlined
  consumers are not in it**, which is the whole of LC-1. *No caller's address is cited: the claim is
  carried by the census counts and by the seven names, and naming a member would import its edge set
  for a statement already made.*
- **CombatFormula, CoreRuntimeScheduling, WorldAreaField — MECHANICAL, through the maintenance
  body.** LC-5 reads **three instructions** of `BattleUnit_RunPeriodicCombatMaintenance` — the
  `stats[+0x05]` gate and the call that follows it — and that body is a hub whose other callees
  reach these layers. **This contract asserts nothing about any of them, or about the rest of the
  tick**; the tick's own behaviour belongs to
  [its contract](../10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md). *The three instructions
  are cited because LC-5 rests on them; nothing else in that body is.*
- **Every other layer reached is MECHANICAL**, through these bodies' own callees. *Their addresses
  are deliberately not cited: each is a hub, and naming one imports its whole edge set.*

## 17. Related

- [Loot drops and enemy chain](loot-drops-and-enemy-chain.md) — the mechanism
- [Contract — experience and licence award](CONTRACT-experience-and-licence-award.md) — S-32's contracted fifth
- [Contract — the gameplay generators](../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md) — LC-1's stream
- [Contract — the periodic tick](../10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md) — LC-5's caller

## Falsification pass 1 — 2026-09-29 (OPUS): the stream survives; the draw-count bounds do not

**Attack.** LC-1 to LC-7, §2 and §10 became checks at their instructions. LC-1's census ran on both instruments:
function-bounded, and a linear sweep of every 4-byte window of `.text`. Script:
`Tools/analysis-kit/gfz-scripts/falsify_loot.py`, output `falsify_loot.out`, image `73461d08…`, 0 BROKEN. LC-7a's merge
is OPUS block 349's execution and is not repeated.

| # | Clause attacked | Result |
|---|---|---|
| L1 | LC-1 | **survives**: 17 accesses on both instruments (linear-only 0), 9 writers; the seven inliners plus the generator and its setter; the generator has 23 call sites in 15 functions, none of the seven |
| L2 | LC-2 | **survives in substance**: 16 instructions identical after resolving RIP targets. The copy adds one register move, `mov ecx, eax` at `00318589`; a precision note was added |
| L3 | LC-3 | **survives**: three `imul 0x41c64e6d` and three `add 0x3039`; `% 100` through `0x51eb851f` / `sar 5` |
| L4 | LC-4's guards | **survives**: all six guards; the chance, quantity and profile rolls draw before any branch |
| K1 | §2 / LC-4 "2 to 13 draws"; §12 "at most once" | **refuted** (`CON-175`): the orchestrator's draws are P + C + Q + E, 0 to 13. An empty slot reaches the `+0xE64` override, and a match draws a quantity |
| L5 | LC-5 | **survives**: one call site, `00311146`, behind the `stats + 5` test |
| L6 | LC-6 | **survives**: `r12d` is written only at `00318116` (rank) and `0031816A` (the drawn profile); the 20-byte accessor reads `+0xE64` |
| L7 | LC-7 | **survives**: fourteen pre-fill stores; `inc eax` |
| L8 | §10, §2 | **survives**: the null table gives a zero count; 641 B |

Corrected in place: §2, LC-4 and §12. The consumer record is `_index/candidates/loot-falsification-pass-1-0929/`.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names each edge.*

**ActorEntity, CombatAI, Movement, Party, RNG_Random_Selection and Spawn_Encounter_Lifecycle — DEPENDENCY (14 edges).** The loot stream `RNG_SharedGameplayLCG_NextU32` `00328370` is also drawn by the actor bodies `00236210` and `002394C0`; by the AI's `AiOrder_EvaluateAndResolveActionTarget` `003014C0`, `AiOrder_CheckActionPreconditions` `00301830` and `AiOrder_SelectFinalTargetFromCandidates` `003087E0`; by the Movement-filed `00239210` and `00312DF0`; by the party's `BattleUnit_SeedPartyCombatStanceRecheckTimer` `003081E0`; by `BattleData_ResolveWeightedId` `00308EC0`; and by the spawn layer's `Spawn_TrySelectCandidatePosition` `00234AF0`, `Spawn_PrepareRandomCandidateForCurrentEntry` `002355A0`, `SpawnPoint_GeneratePositionFromAuthoredRegion` `00236450`, `SpawnKeep_InitializeEntriesFromDefinitionTable` `002395A0` and `002398F0`. Every one of these draws advances the same shared LCG state that the loot rolls step inline (LC-1), so the value a loot roll draws depends on how many draws AI targeting, spawning and stance timers made before it; the other layers share the stream and do not read or change loot state.

**CoreRuntimeScheduling — SERVICE (1 edge).** `EnemyChain_UpdateOnDefeat` `00317ED0` calls `00229E40`, a 7-byte getter of one scheduling global, three times; when it answers non-zero the chain count handed on to the chain display is increased by one. It changes what is shown, not the chain state this contract describes.

**Gameplay — SERVICE and DEPENDENCY (2 edges).** `Loot_RollAdditionalItemChance` `00318510` calls `BattleEncodedId_QueryMode0Positive` `0030B0E0` on the item id before it draws, and skips the draw when the query answers 0; the domain-filed `00312B40` is one more caller of `00328370`. The extra-item roll therefore consumes a draw only for an item id the encoded-id query accepts, and `00312B40` is another consumer of the shared stream.

**Status_Periodic_Terminal — CLIENT (1 edge).** `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls the chain-rank outcome selector `00319530`. This is LC-5: the periodic tick, not only a kill, advances the loot stream through `00319530`, so the status layer's tick is a caller of this contract's roll.
