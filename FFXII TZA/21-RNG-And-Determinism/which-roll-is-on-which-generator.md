---
system: Which roll is on which generator, and what reseeds each
category: 21-RNG-And-Determinism
status: AUDITED
owner_layer: PrimaryOwner:RNG_Random_Selection
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN159 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN159 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-03   # <- corrected 2026-10-02, OPUS: the last whole-page review, not the last change - the body carries dated edits through 2026-09-26
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-rng-generators-pass-1
  crossref_clean: true
  reopened_count: 0   # <- corrected 2026-10-02, OPUS: not advanced for the two adjudicated corrections of 2026-09-14 (sections 3 and 5)
---

# Which roll is on which generator, and what reseeds each

> **Combat rolls and loot rolls are on different generators, and only one of them is reseeded from
> the clock.** Reloading a save gives you a fresh set of combat outcomes and *the same* loot stream
> position — because the save-load path reseeds the Mersenne Twister from `_time64` and never touches
> the LCG at all.

## 1. What the player sees

Reload before a boss and the fight goes differently — different misses, different criticals.
Reload before opening the same chest and the sequence of loot behaves as though nothing was
rerolled. Both are consequences of §4 and §5, and they are **different mechanisms**, not one
mechanism seen twice.

## 2. ~~Four generators~~ Four of at least eight generators *(corrected 2026-10-02, OPUS: the table omits the CRT `rand()` — IAT `008C3098`, 48 call sites in 30 functions — which also decides gameplay (rng-streams.md §8g), and the presentation-only stream 5, the PPFX xorshift128 and the Bullet solver LCG)*

| # | Generator | State | Seeded by | Drives |
|---|---|---|---|---|
| 1 | **Gameplay MT19937** | `02EB3870` (624 dwords), index `02EB4230` | constant `4537` at boot; **`_time64` on save load** | combat formula (53 sites), weather, and more — ~~**66 consumer functions**~~ **67 consumer functions**: 66 through `00379CD0` and the camera-shake sampler through the float thunk *(corrected 2026-10-02, OPUS: `callers 00379CD0` = 98 sites in 66 functions, callers of the float thunk = 9 sites, all in the camera-shake sampler; CONTRACT-gameplay-generators.md §12c)* |
| 2 | **Graphics-noise MT19937** | separate instance | time and clock, via `GraphicsNoiseMT19937_SeedFromTimeAndClock` (`0015BCF0`) | presentation noise only |
| 3 | **Shared gameplay LCG** | `022C256C` | a **counter**, once per battle-area init | loot, the enemy chain, weighted action selection |
| 4 | **Presentation bit-feedback PRNG** | `01EF93E8` | constant `0x458DC800` at startup | procedural rendering |

Generators 3 and 4 were established in [`rng-streams.md`](rng-streams.md) and are not re-derived
here. **This document adds the census, the reseed paths, and the correlation answer.**

**Generators 1 and 2 are both MT19937 and they are different instances.** Every instruction that
touches the gameplay state array `02EB3870` lives in exactly ~~three~~ **four** functions
*(corrected 2026-09-13, §13 — the slash below hides that `TwistState` and `SeedState` are two
separate functions, `00866B90` and `00866D60`)* — `RNG_MT19937_NextU32` (`00863BF0`),
`RNG_MT19937_NextFloatClosed` (`00863C80`), `RNG_MT19937_TwistState` (`00866B90`)/`SeedState` — and the graphics pair
(`0018D740` / `0018EE20`) touches none of them. **Two Mersenne Twisters, disjoint state, different
seeding policies.**

## 3. The LCG has eight draw sites and seven of them are inlined

`RNG_SharedGameplayLCG_NextU32` (`00328370`) steps the ANSI-C LCG three times per draw
(`state * 0x41C64E6D + 0x3039`). Censusing **the multiplier constant** rather than the call finds
**24 instruction sites — three per draw, so eight draw sites**:

| Function | Owner |
|---|---|
| `RNG_SharedGameplayLCG_NextU32` (`00328370`) | RNG |
| `EnemyChain_UpdateOnDefeat` (`00317ED0`) | Rewards |
| `EnemyChain_TryAdvanceRank` (`003183D0`) | Rewards |
| `Loot_RollAdditionalItemChance` (`00318510`) | Rewards |
| `Loot_RollNormalSlotChance` (`003185D0`) | Rewards |
| `Loot_RollNormalSlotQuantityBucket` (`003186F0`) | Rewards |
| `Loot_SelectChanceProfileByWeight` (`00318820`) | Rewards |
| `FUN_00319530` | **Rewards** — the chain-rank bonus roll (`AD-6` / `CQ-1`; §13) |

**Seven of the eight never call the generator — they inline it.** *(Struck 2026-09-14 by OPUS
adjudication of `FABLE-CONTRA-WHICHROLL-LCG-CONSUMERS`: the sentence that followed here said a
census keyed on `call` "sees one draw site and would conclude the LCG is barely used". It is
**wrong in both halves**, and the correction is the more interesting fact.)*

**A census keyed on `call` sees FIFTEEN caller functions, and they are a different population from
the eight.** The constant census finds where the recurrence is *written*; the call census finds
where the stream is *drawn* by everyone who did not inline it — spawn placement, the combat AI,
the party stance timer, weighted-id resolution. Neither census is the consumer list on its own,
and the eight-row table above is the inliners, not the users.

> **All eight read the same state global, `022C256C`.** Loot rolls, enemy-chain rolls and the
> weighted action selector are not merely on the same *algorithm*; they are on the same *stream*, and
> every draw by any of them moves the others along.

> **⚠ Challenged 2026-09-14 (FABLE, FINAL-AUDIT pass 22) — the eight sites are where the recurrence is *written*,
> not where the stream is *drawn*.** The one non-inlined body, `00328370`, is **called from 23 sites in 15 functions**.
> That count comes from the raw call index. It is the same 15 that [rng-streams](rng-streams.md) lists by owner. So a
> `call` census does not see "one draw site": it sees every consumer this table leaves out.
>
> - **Spawn_Encounter_Lifecycle.** The consumers are `Spawn_TrySelectCandidatePosition` (`00234AF0`, 2 sites),
>   `Spawn_PrepareRandomCandidateForCurrentEntry` (`002355A0`), `SpawnPoint_GeneratePositionFromAuthoredRegion`
>   (`00236450`, 6 sites), `SpawnKeep_InitializeEntriesFromDefinitionTable` (`002395A0`, 2 sites) and `002398F0`.
> - **ActorEntity.** The consumers are `00236210`, which supplies a float height to the spawn-placement path, and
>   `002394C0`, which draws before `BattleStats_AddStatusMode3`.
> - **Movement.** The consumers are `00239210`, a random yaw in `[0, 360)`, and `00312DF0`, the randomised avoidance
>   case.
> - **Combat AI and battle data.** The consumers are `AiOrder_EvaluateAndResolveActionTarget` (`0030160F`),
>   `AiOrder_CheckActionPreconditions` (`0030193F`), `AiOrder_SelectFinalTargetFromCandidates` (`00308B13`),
>   `BattleUnit_SeedPartyCombatStanceRecheckTimer` (`003081FF`), `BattleData_ResolveWeightedId` (`00308F61`) and
>   `00312B40`.
>
> Every one of them steps `022C256C`, the state the seven inlined loot and chain rolls use. The table's eight
> functions stand. The sentence *"a census keyed on `call` sees one draw site"* does not, and §6's first bullet leans on
> it (see the note there). Filed as `FABLE-CONTRA-WHICHROLL-LCG-CONSUMERS`.

### The census is complete — `AD-2` (FABLE, Claude Opus 5.5, 2026-09-26)

The two populations above are the whole consumer set of `022C256C`:
- the nine functions that touch the state: the eight writers of the recurrence and the reseed;
- the fifteen functions that call the generator `00328370`, at 23 sites.

The earlier censuses were a multiplier census and a raw call index, and each could miss a route. An image-wide sweep
over the whole `.text` section, listed bodies or not, now closes the routes they could not see.
Control: [`members/lcg_census_complete.py`](members/lcg_census_complete.py) (5 checks, FAILS 0).
- **Every rip-relative operand into the state dword**, at any width and with any mnemonic including `lea`, is one of
  the 17 sites in [the accesses table](shared-gameplay-lcg-state-accesses.tsv). The sweep is a raw `disp32` sweep,
  confirmed by decoding.
- **No pointer reaches the state by displacement.** No data word points into its 0x100-byte neighbourhood. The one
  `lea` to a base below it forms a four-entry pointer array, sized from its filler's loop bound, that ends 0x8C
  bytes short of the state.
- **Every branch into the generator is one of the 23 calls.** There is no `jmp` or `jcc` into it, and nothing takes
  its address: no rip-relative `lea`/`mov` and no absolute qword. So no indirect call can reach it.
- *Control:* the same decoder reproduces the published 24 multiplier sites in the eight writer functions.

*Note on §13 below:* its list of four rows that "read ANSWERED" includes `AD-2`, but the register carried `AD-2` as
REVISED until this section.

## 4. What reseeds the LCG: a counter, once per area

`RNG_SharedGameplayLCG_SetState` (`00328D80`) has exactly **one** caller,
`BattleSystem_InitializeAreaState` (`002342F0`):

```c
if (DAT_02089300 == 0) return;
seed = DAT_0208E6B0;          // a plain counter
DAT_0208E6B0 = seed + 1;
RNG_SharedGameplayLCG_SetState(seed);
```

**The counter at `0208E6B0` is touched at exactly two instructions in the whole image** — the read
and the write above. Nothing initialises it from a clock, nothing restores it from a save, nothing
resets it.

> So the LCG is seeded `0, 1, 2, 3, …` — **once per battle-area initialisation, counting from process
> start.** The loot stream's starting point is a function of *how many areas you have entered since
> launching the game*, and of nothing else.

## 5. What reseeds the MT: a constant at boot, and the wall clock on save load

The seeder is reached through a **5-byte `jmp` thunk** (`00379CF0` → `00863D30`), and it has **two**
callers:

```asm
; boot, 0022A40B
mov ecx, 0x11B9          ; 4537 -- an immediate, no entropy
call 0x379CF0

; SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG, 005843D3
call qword ptr [008C3060] ; -> api-ms-win-crt-time-l1-1-0.dll ! _time64
lea  ecx, [rax + 0x2B5A5]
sar  rax, 0x20
imul ecx, ecx, 0x21
add  ecx, eax
imul eax, dword ptr [01FD4A80], 0x258
btr  ecx, 0x1F           ; clear the sign bit
add  ecx, eax
jmp  0x379CF0            ; RNG_MT19937_Seed(ecx)
```

On first use before any seeding, the generator lazily self-seeds with `0x1571` = **5489**, which is
`std::mt19937::default_seed` — the constant that identifies the algorithm.

**So the gameplay Mersenne stream carries the same SEED on every launch — until a save is loaded,
at which point it is reseeded from the wall clock**, mixed with a global at `01FD4A80` (`× 600`)
and both halves of the 64-bit time value.

**Same seed is not the same position.** *(Narrowed 2026-09-14 by OPUS adjudication of
`FABLE-CONTRA-WHICHROLL-LCG-CONSUMERS`; this paragraph previously said the stream is "identical on
every launch".)* The boot frame modes draw the MT once per dispatch and throw the value away -
mode 0 `0022B6E0` at `0022B706`, mode 1 `0022B7E0` at `0022B7EB`, each a bare `call` whose `eax`
is never read - so the first gameplay draw reads the 4537 sequence **offset by the number of
boot-mode dispatches**. Verified from the shipping bytes 2026-09-14 (OPUS). How many dispatches
each mode takes, and whether that count is fixed, is a runtime question.

> That distinction is the whole player-facing result. **"Same seed from boot", "same position from
> boot" and "deterministic across a reload" are three claims, and only the first is established.**

> **⚠ The fresh-boot stream is already advanced at gameplay start — FINAL-AUDIT pass 22 (FABLE, 2026-09-14).** "Identical on
> every launch" holds for the seed, not for the position. The boot frame modes each draw the MT once per dispatch and
> discard the value. Mode 0 `0022B6E0` draws at `0022B706`, and mode 1 `0022B7E0` draws at `0022B7EB`. Both modes wait
> on load conditions before handing on, as the mode table in
> [between two frames](../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) shows. The first
> gameplay draw therefore reads the 4537 sequence offset by the number of boot-mode dispatches. Whether that number is fixed is a
> runtime question; see [the contract](CONTRACT-gameplay-generators.md) §6.

## 6. The correlation answer

- **Combat FORMULA outcomes and loot outcomes cannot be correlated; combat AI DECISIONS and loot
  are on one stream.** *(Restated 2026-09-14 by OPUS adjudication of FABLE-CONTRA-WHICHROLL-LCG-
  CONSUMERS; the original bullet said "no amount of fighting shifts a loot roll" and that half is
  **refuted**.)* The split is by generator, not by subject matter:

  - **On the Mersenne Twister:** hit/miss, damage variance, the guard and parry rolls, knockback,
    poach, the percent gates. A formula outcome cannot move the loot stream, and this half of the
    original claim stands.
  - **On the shared gameplay LCG, with loot:** AI order evaluation, spawn placement, the party
    stance timer and weighted-id resolution. **`RNG_SharedGameplayLCG_NextU32` has fifteen distinct
    caller functions**, and two of them are `AiOrder_CheckActionPreconditions` (`0030193F`) and
    `AiOrder_EvaluateAndResolveActionTarget` (`0030160F`), each reducing its draw `% 100` through
    the `0x51EB851F` divide-by-100 idiom. Verified from the shipping bytes 2026-09-14 (OPUS),
    independently of the report that raised it.

  **So fighting DOES shift a loot roll** - through the decisions the AI takes, not through the
  numbers the formula produces. The converse half, that looting does not shift a to-hit roll,
  stands: the loot path never touches the MT.

  How often those AI draw paths run during a fight is not established statically and is the one
  open part of this.

  > **Attacked and survived 2026-09-13 (§13).** The eighth LCG draw site is called from
  > `BattleUnit_RunPeriodicCombatMaintenance`, which looks at first like a combat function
  > stepping the loot stream. It is not: `AE-3` establishes it runs **when a party unit collects
  > a world pickup**, so the trigger is looting and the generator it moves is the loot LCG. The
  > bullet holds in both directions.
- **Loot, the enemy chain and weighted action selection are perfectly correlated.** One state, eight
  draw sites. Whether that was intended is not knowable from the code; **that it is the case is.**
- **Reloading a save rerolls the MT-driven outcomes** — hit/miss, damage variance, poach, the percent
  gates — because the reseed reads the clock.
- **Reloading a save does not reseed the LCG.** `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (`00584210`)
  touches the MT and nothing in the LCG's state or its counter.

> **⚠ Challenged 2026-09-14 (FABLE, FINAL-AUDIT pass 22): "no amount of fighting shifts a loot roll" is not supported by
> the static evidence.** The loot LCG's state `022C256C` is also stepped by the combat AI and the party stance timer:
>
> - `AiOrder_CheckActionPreconditions` rolls `% 100` on it at `0030193F`–`0030195F`;
> - `AiOrder_EvaluateAndResolveActionTarget` rolls `% 100` on it at `0030160F`–`0030162C`;
> - `BattleUnit_SeedPartyCombatStanceRecheckTimer` draws on it at `003081FF`.
>
> Spawn placement draws on it too (§3 note). So a gambit or foe action decision taken during a fight moves the stream the
> next loot roll reads, whenever those draw paths run. How often they run in play is not established statically.
>
> The supportable bullet is narrower: combat *formula* outcomes cannot shift a loot roll, because they are on the MT,
> while combat *AI decisions*, spawn placement and loot share one stream. The converse half, that looting does not shift
> a to-hit roll, stands. The attack recorded in §13 tested only the eighth inlined site, which is why it did not catch
> this.

**On a fixed stream, draw *ordering* is the entire source of variation** — so anything that draws
conditionally is a variance amplifier for everything downstream of it on the same generator. That
applies with full force to the eight LCG sites, which share one state.

## 7. Key addresses

| Address | Name | Role |
|---|---|---|
| `00863BF0` | `RNG_MT19937_NextU32` | gameplay MT draw; lazy default seed `5489` |
| `00863C80` | `RNG_MT19937_NextFloatClosed` | float draw, same state |
| `00866B90` | `RNG_MT19937_TwistState` | twist |
| `00866D60` | `RNG_MT19937_SeedState` | seed |
| `00863D30` | *(the seeder body)* | checks the init flag, then seeds |
| `00379CF0` | `RNG_MT19937_Seed` | **the 5-byte `jmp` thunk the callers actually use** |
| `00379CD0` | `RNG_MT19937_NextU32_Thunk` | 66 callers, 53 in CombatFormula |
| `0022A0B0` | boot | `RNG_MT19937_Seed(4537)` |
| `00584210` | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` | reseeds from `_time64` |
| `00328370` | `RNG_SharedGameplayLCG_NextU32` | the one non-inlined LCG draw |
| `00328D80` | `RNG_SharedGameplayLCG_SetState` | one caller only |
| `002342F0` | `BattleSystem_InitializeAreaState` | seeds the LCG from the counter |
| `022C256C` | — | LCG state, shared by all eight draw sites |
| `0208E6B0` | — | the area-init counter; two instructions touch it |
| `02EB3870` / `02EB4230` / `02EB4234` | — | MT state, index, init flag |

**The other subsystems these rows touch — FINAL-AUDIT pass 22 (FABLE, 2026-09-14).** The seeding functions are
initialisers, and their other callees sit beside the seed call rather than consuming a generator. No path from any of
them reaches a draw or seed body within six levels of the call graph; indirect calls were not followed.

- **Boot, `0022A0B0`.**
  - It calls into **Resource**: `00379D20`, `0032EAE0`, `00259DF0` and `00379E90`. The last two prime `0032E400` and
    `0032E620` ([game application](../00-Engine-Core-Runtime/Application-Root/game-application.md)).
  - It also calls `002DF9A0`, which opens the `PS2Data\image\FF12\…\in_sdver` menu images.
  - It calls **ActorEntity** `BattleStorage_InitializeWorkArrays` (`002368D0`), which clears the reseed gate `02089300`
    (§13). That function in turn calls **Movement** `Navigation_ClearDataset` (`00383A20`) and **Resource** `003843F0`.
- **Area initialisation, `BattleSystem_InitializeAreaState` (`002342F0`).**
  - ~~Its caller is~~ Its callers are **ActorEntity** `ActorSystem_InitializeManagerRuntime` (`0026CE60`) and the broad bootstrap (FABLE's record readiness-apply-fable-1002), which also advances the counter *(corrected 2026-10-02, OPUS: `callers 002342F0` = the broad bootstrap and `0026CE60`, one site each)*.
  - Around the LCG reseed it calls **Spawn_Encounter_Lifecycle** `SpawnKeep_RotatePersistenceBanksForAreaTransition`
    (`00233780`) and `SpawnGroup_ResetLifecycleLedger` (`00307090`).
  - It calls **Movement** `Navigation_GetWorldBoundsXZ` (`00383740`), the `MapGrid` builder `003924B0`, and `00327360`,
    `00322220`, `0031BD60` and `0033A380`.
- **Save load, `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (`00584210`).** It calls **PlatformOnlineAchievements**
  `00316810` at `00584398`, just before the MT reseed. That function normalises the achievement counters after a load
  ([the contract](CONTRACT-gameplay-generators.md) §6 note). Neither generator is touched there.
- **The LCG's consumers in Spawn, ActorEntity and Movement** are listed in the §3 note.

## 8. Data structures and formulas

```
LCG draw   : s = s*0x41C64E6D + 0x3039, three times; 31-bit result from the high bits of each
LCG seed   : counter at 0208E6B0, post-incremented once per battle-area init
MT seed    : boot -> 4537
             save load -> (((uint32)t + 0x2B5A5)*0x21 + (t>>32)) & 0x7FFFFFFF
                          + [01FD4A80]*600,  where t = _time64()
                          (the mask is applied BEFORE the timer term is added: btr at 005843BE,
                          add at 005843C2 -- the final seed may have bit 31 set; EXP-056)
MT default : 5489 (std::mt19937::default_seed), used only if a draw precedes any seeding
```

## 9. Modding notes

**To make loot reproducible, pin the counter at `0208E6B0`** — it is the only input to the LCG's
starting state, and only two instructions touch it.

**To make combat reproducible across reloads, neutralise the `_time64` mix** in
`SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (`00584210`); the boot path is already constant.

**Do not assume a `call` census finds RNG use.** Seven of the eight LCG draw sites are inlined (§3).

## 10. What is not known

- ~~**What `01FD4A80` holds**~~ **Its runtime value** *(answered: what `01FD4A80` holds is the dispatched-frame counter, `inc` in the frame dispatcher — CONTRACT-gameplay-generators.md §14 and CONTRACT-which-generator-serves-which-roll.md §14; 2026-10-02, OPUS)* — the second input to the save-load seed; it is in the zero-filled tail of
  `.data`, so its runtime value is not in the image.
- [x] ~~**What `FUN_00319530` rolls for.** It is the eighth LCG draw site and is unnamed.~~
  **This was already answered elsewhere and stayed open here — struck 2026-09-13 (OPUS, §13).**
  `AD-6` answered it on **2026-09-02**, the day *before* this document's `last_reviewed`:
  it is the **chain-rank outcome selector**, one draw reduced `% 100` against a cumulative walk
  of the 4 × 7 byte weight table at `01EED3B8`, indexed by the chain rank `022C3158`
  ([loot drops and the enemy chain](../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md)
  §8d). `CQ-1` and `AE-3` then named the caller and the outcomes on **2026-09-12**: it runs from
  `BattleUnit_RunPeriodicCombatMaintenance` at `00311146` when a party unit **collects a world
  pickup**, and applies the *Chain Bonus* pseudo-action `0xF5`. **Nothing here is new; the
  question should have been closed when `AD-6` was.**
- **The graphics MT's state address and consumer census** — established here only as *disjoint* from
  the gameplay MT, not enumerated. *Narrowed 2026-09-13 (§13):* **~~there may be no fixed address to~~
  ~~find.~~** *(answered: there is one, `01F7F600` — every call site passes it as a literal `lea`, `0015BD13` and `0015BD1F` in `0015BCF0`, two sites in the procedural-noise generator (FABLE's record readiness-apply-fable-1002); CONTRACT-which-generator-serves-which-roll.md I5 and `EXP-144`; 2026-10-02, OPUS)* `GraphicsNoiseMT19937_TwistState` (`0018EE20`) has **no `rip`-relative operand at all**,
  so it works on a state the caller hands it — structurally unlike the gameplay MT, which names
  `02EB3870` directly. The seeder's three globals were **not** adopted as the state: one of them,
  `01F44858`, is referenced by 14 functions including `__isa_available_init`, so it is shared CRT
  machinery and not an MT array.
- **Whether `DAT_02089300`, the gate on the LCG reseed, is ever false** in normal play.
  *Answered in the code 2026-09-13 (§13), not in play:* **there is an unconditional clear.**
  `BattleStorage_InitializeWorkArrays` (`002368D0`) does `xor ebx, ebx` at `002368E1` and stores
  `ebx` to the gate at `002368F8`; `FUN_00236A40` stores a literal `1` at `00236A44`. So the
  answer to *"can it be false"* is **yes, by construction**; ~~whether that path precedes an area~~
  ~~init in normal play is a runtime question and is not established.~~ *(answered from the code, not observed: `002368D0`, the only clear, is called once, from the boot routine, and the only set, once, from boot frame mode 0 (boot frame, FABLE's record readiness-apply-fable-1002) — so the gate is 0 only between boot initialisation and boot mode 0, and 1 for the rest of the process; 2026-10-02, OPUS)* **And it is not only the
  reseed gate** — three functions read it: `BattleSystem_InitializeAreaState`,
  `BattleUnit_ApplyUnitDefinition` (`0023A5B5`) and `BattleStats_InitializeDefinitionRecord`
  (`0023ACE4`).
- **How many draws precede a given roll** — the ordering question, which on a fixed stream is the
  only remaining variable, is not traced here.
- Whether any generator is stepped from a thread other than the main one.

## 11. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Eight LCG draw sites, seven inlined | census of the multiplier `0x41C64E6D`: 24 instruction sites, 3 per draw | 1 |
| All eight share state `022C256C` | the rip-relative target of each draw's first `imul`, resolved individually | 1 |
| The LCG has one reseed caller | caller census of `00328D80` | 1 |
| The area counter has exactly two instructions | image-wide rip-relative sweep of `0208E6B0` | 1 |
| Boot seeds the MT with 4537 | `mov ecx, 0x11B9 ; call 0x379CF0` at `0022A40B` | 1 |
| Save load reseeds from `_time64` | IAT slot `008C3060` resolved through the PE import descriptors to `api-ms-win-crt-time-l1-1-0.dll!_time64` | 1 |
| `0x1571` = 5489 is the MT default seed | the constant in the lazy-init path | 1 |
| Two disjoint MT instances | every instruction touching `02EB3870` enumerated: ~~three functions~~ four functions — `00863BF0`, `00863C80`, `00866B90`, `00866D60` *(corrected 2026-10-02, OPUS: `refs 02EB3870..02EB4233` = 4 + 4 + 11 + 3 instructions, the 22 rows of `mt19937-state-accesses.tsv`; §13 and §2's correction)*, none of them the graphics pair | 1 |
| MT has ~~66 consumers, 53 in CombatFormula~~ 67 consumer functions: 66 on the draw thunk (53 in CombatFormula) and the camera-shake sampler on the float thunk *(corrected 2026-10-02, OPUS: callers of the float thunk = 9 sites, all in the camera-shake sampler)* | caller census of the draw thunk `00379CD0` | 1 |

### A correction, and why three methods failed together

**This document's first draft was going to state that the MT is never explicitly seeded.** Three
checks agreed: a caller census of `00863D30` returned zero; an unbounded scan for `E8` call
encodings targeting `00863D30` returned zero; and a scan for 8-byte pointers to it anywhere in the
image returned zero.

**All three were wrong, and they were wrong together.** The seeder is reached through a `jmp` thunk
at `00379CF0`, and **the name `RNG_MT19937_Seed` (`00863D30`) is attached to the thunk, not to the body** — so the
call graph indexes the callers under the thunk's address. Querying the body finds nothing.

> **Three methods that share an assumption are one method.** Each asked "what *calls* `00863D30`",
> and the answer was that nothing does — the thunk *jumps* to it. **Independence has to be
> independence of the question, not just of the technique.**

Following the thunk finds **two** callers, and the second one — the save-load reseed — is the more
interesting of the two. The corrected census scans for `E8` **and** `E9` displacements against both
the body and every thunk that targets it, and that is what §5 rests on.

`check_already_answered.py` was run before this block was started.

## 12. Related

- [`rng-streams.md`](rng-streams.md) — the ~~three streams~~ generators, at least eight *(corrected 2026-10-02, OPUS: rng-streams.md's opening line and §10, the PPFX xorshift128)*, this builds on, and the presentation PRNG's step accounting.
- [`loot-drops-and-enemy-chain.md`](../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md) — five of the eight LCG draw sites are its rolls.
- [`what-the-engine-fixes-at-boot.md`](../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md) — the boot seed in its wider context.

## 13. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

### The censuses reproduce, to the instruction

| claim | measured |
|---|---|
| 24 instruction sites carry `0x41C64E6D`, three per draw → 8 draw sites | **24 / 8**, and the eight functions are exactly the eight §3 names |
| all eight read the same state `022C256C` | each one's `imul` reads it and its `mov` writes it back |
| `0208E6B0` is touched at exactly two instructions in the image | **`00234301`** read, **`00234315`** write, both in `BattleSystem_InitializeAreaState` |
| `RNG_SharedGameplayLCG_SetState` has exactly one caller | **1** |
| the seed thunk `00379CF0` has two callers; the body `00863D30` has none | **2 and 0** — one in `CoreRuntimeScheduling`, one in `Save_Load_Settings` |
| the draw thunk `00379CD0` has 66 callers, 53 in CombatFormula | **66**, and **53** are `CombatFormula` |
| boot: `mov ecx, 0x11B9` at `0022A40B` | exact, and `0x11B9` is 4537 |
| the save-load mix, and `btr` at `005843BE` before `add` at `005843C2` | exact, including `imul eax, [01FD4A80], 0x258` at `005843B4` and the tail `jmp 0x379CF0` at `005843D3` |

§11's caller figures all come from `Tools/work/graph/edges.tsv`; they are ledger-graph counts, which
is worth saying here because [the thunk page](../00-Engine-Core-Runtime/duplicated-function-names-and-how-to-resolve-them.md)
§9 measured the same figures three other ways and got three other answers.

### ⚠ The eighth draw site was answered twelve days ago, and this page still calls it unknown

§10 lists *"What `FUN_00319530` rolls for"* as unknown and §3's table gives it no owner. I decoded it
from the image — three LCG steps at `00319530` / `00319545` / `0031955F` with the state written back
at `00319582`, the three high chunks XOR-folded, reduced `% 100`, then a cumulative walk of a
**4 × 7 byte weight table at `01EED3B8`** indexed by `022C3158` and bounded `≤ 3`, returning the first
index whose running total exceeds the roll and `0` if none. The table is in the image and **every row
sums to exactly 100**: `100 0 0 0 0 0 0`, `80 10 10 0 0 0 0`, `50 20 20 5 0 5 0`, `40 25 25 0 5 0 5`.

**None of that is new.** `AD-6` answered it on **2026-09-02** — the day *before* this page's
`last_reviewed` — with the same table and the same `% 100` cumulative reading, in
[loot drops and the enemy chain](../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md) §8d.
`CQ-1` and `AE-3` finished it on **2026-09-12**: the caller is
`BattleUnit_RunPeriodicCombatMaintenance` at **`00311146`**, it fires **when a party unit collects a
world pickup**, and the seven outcomes are the *Chain Bonus* (`0xF5`) — nothing, HP, MP, Protect and
Shell, collector-only or party-wide. My re-derivation is a **control on theirs**, not a finding:
same table, same bound, same caller, same call site.

> **So the correction is the staleness.** Four register rows — `AD-2`, `AD-6`, `AE-3`, `CQ-1` — read
> **ANSWERED** while this document, which cites the same address, carries the question open and the
> row unowned. That is an answer stranded beside an obsolete specification, and it is the kind this
> database keeps producing: the answer landed in the *consumer's* page and never walked back to the
> *generator's*.

#### And I nearly published the re-derivation as a finding

`check_already_answered.py` **did** fire. I ran it with three arguments at once, it printed a
37-document list, and I read the output through `head -14` — which cut off the register section, where
all four rows were. The draft of this section claimed the caller refuted §6's first bullet; `AE-3`
says the trigger is a **pickup collection**, so the thing being moved is the loot generator by a
looting action, and §6 was right all along. **The draft was retracted before publication only because
the register was read on the second attempt.**

> **The gate prints its register rows last.** Truncating its output defeats it exactly as a
> name-keyed census is defeated by a thunk — the instrument worked and the reading did not. Recorded
> in [`EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md) beside the amendment it belongs to.

### ⚠ `02089300` is not only the reseed gate, and it is demonstrably cleared

§10 asks whether the gate is ever false. In the code it is: `BattleStorage_InitializeWorkArrays`
(`002368D0`) zeroes `ebx` at `002368E1` and stores it to the gate at `002368F8`, unconditionally on
entry; `FUN_00236A40` stores a literal `1` at `00236A44`. **~~Whether that clear precedes an area init~~
~~in normal play is a runtime question and is not answered here~~** *(answered from the code, not observed: the clear runs once, from the boot routine, and the set once, from boot frame mode 0; 2026-10-02, OPUS)* — but "can it be false" no longer is.
And the gate has **three readers**, not one: the LCG reseed, `BattleUnit_ApplyUnitDefinition`
(`0023A5B5`) and `BattleStats_InitializeDefinitionRecord` (`0023ACE4`), so calling it *"the gate on
the LCG reseed"* names one of its three jobs.

### ⚠ Four functions touch the MT state, not three

`02EB3870` is addressed from `00863BF0`, `00863C80`, `00866B90` **and** `00866D60`. §2 writes the last
two as `` `RNG_MT19937_TwistState` (`00866B90`)/`SeedState` `` — one slash hiding two functions — and
§11's evidence row then says "three functions". The disjointness claim is untouched: the graphics
pair is in neither set.

### What the graphics MT does differently — §10's third unknown, narrowed

**`GraphicsNoiseMT19937_TwistState` (`0018EE20`) has no `rip`-relative operand at all**, so it twists
a state its caller supplies. The gameplay twist names `02EB3870` directly. That is a structural
difference, and it means the unknown may be mis-stated: ~~there may be~~ **~~no fixed graphics state~~
~~address to enumerate.~~** *(answered: the fixed address is `01F7F600`, passed as a literal `lea` at all four call sites — CONTRACT-which-generator-serves-which-roll.md I5 and `EXP-144`; 2026-10-02, OPUS)* The seeder's three globals were deliberately **not** adopted as the answer —
`01F44858` is referenced by 14 functions including `__isa_available_init`, so it is shared CRT
machinery, not an MT array.

**Not claimed.** The `FUN_00319530` reading is a re-derivation of `AD-6` / `CQ-1` / `AE-3`, not an
independent result, and the *Chain Bonus* semantics are FABLE's, cited not re-tested. How often
the guarded path at `00311146` fires. `00319A00`, called immediately before it, was not read. Whether `01F44858` is the graphics state under some other
reading — it was excluded, not identified. The runtime value of `01FD4A80` (§10's first unknown) is
still not in the image. Everything here is static disassembly plus `edges.tsv`; **nothing was
executed and no roll was observed.**

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT and SERVICE.** Cited functions are called by `BattleUnit_RunPeriodicCombatMaintenance` (2) and `BattleFormula_AdvanceStatusTimersAndBuildResult`, and call `BattleStats_RemoveStatusMode0` and `BattleStats_AddStatusMode3`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Script_VM_Native_Bridge — CLIENT (8 edges through 7 of this page's functions).** The Script_VM_Native_Bridge layer reaches this page at `00379CD0`, `00239210`, `002394C0`, `002395A0` and 3 more. `FUN_00354bf0` is the worked example, read in full - it is a 57-byte scaled draw: the operand becomes a bound, a Mersenne draw is multiplied by it and the **high 32 bits taken**, which is a range reduction without a modulo; **2 of the 8 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

## SWE2-EC7-49 update (2026-09-19) - `0018EE20`

`0018EE20` (192 B) is `GraphicsNoiseMT19937_TwistState` - call-free MT twist: ~~`(mt[i]&0x7FFFFFFE | mt[i+1]&1) >> 1 ^ (odd ? 0x9908B0DF : 0) ^ mt[i+0x18C]`, a 227-iteration loop then a 396-iteration loop~~ `y = (mt[i]&0x80000001) | (mt[i+1]&0x7FFFFFFE)`, `mt[i] = partner ^ (y >> 1) ^ (mt[i+1]&1 ? 0x9908B0DF : 0)`, with partner `mt[i+397]` (`[+0x634]`) for 227 iterations, then `mt[i-227]` (`[-0x38C]`) for `0x18C` = 396 iterations, then the last element against `mt[0]` — standard MT19937 *(corrected 2026-10-02, OPUS: checked at `0018EE30`–`0018EECA`; the old text swapped the split masks and used the second loop's count `0x18C` as the partner offset; CONTRACT-gameplay-generators.md §7)*, no `rip`-relative operand (verifies the page's claim). Interior anchor `0018EE30` (the twist loop head).

## SWE2-EC7-95 update (2026-09-20) - `00322220` + `003209C0` measured

`00322220` (84 B) is the triple install `002342F0` and `0026E760`
call: `0026E500(0)` and `0026E500(2)` land in `02EBF169`/
`02EBF165`, then `ebx` 1..0 fetches `0026E500(ebx)` into
`02EBF108` until one comes back nonzero - the three-handle acquire
the roll path holds.
Interior anchor `00322237` (the `0026E500(2)` call).

`003209C0` (29 B) is the boolean inverter `00234AF0`, `00236450`
and `00237460` wrap around `003DFD00(0, edx, r8)`: the
`neg`/`sbb`/`neg`/`dec` chain maps a nonzero result to 0 and a zero
result to -1 - the `result ? 0 : -1` error-shape the callers
return.
Interior anchor `003209CB` (the `003DFD00` call).
