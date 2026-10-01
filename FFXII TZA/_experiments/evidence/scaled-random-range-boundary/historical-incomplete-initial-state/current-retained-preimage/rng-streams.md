---
system: RNG streams
category: 21-RNG-And-Determinism
status: AUDITED
owner_layer: PrimaryOwner:RNG_Random_Selection / CodeDomain:Runtime.Random
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  previous_parent: 381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 2
  last_pass: 2026-09-07
  last_pass_state: GN160-xiionline-61-shared-lcg-body-and-draw-sites
  last_pass_kind: attack
  prior_pass_kind: reverification
  crossref_clean: true
  reopened_count: 3
---

# RNG streams

> FFXII has **at least seven** distinct random sources. Conflating them is how you end up
> networking render state or desyncing combat.
>
> **Corrected 2026-09-02 (section 8).** This line originally said "two". Six families are recorded
> in the GFZ and a seventh - the presentation recurrence below - is proven separately here.

## 1. What the player sees

Damage variance, weather changes and drops come from one stream. Small visual randomness - the
slight per-client variation in environment orientation - comes from a completely different one.
Two players standing in the same weather can legitimately see slightly different visual variation
while agreeing exactly on the gameplay outcome.

> **Corrected 2026-09-02 (see section 8).** This paragraph originally included *"and AI choices"*
> in the first stream. **That was wrong.** Enemy and gambit action selection is rolled from a
> *third* stream - a separate LCG - not from the Mersenne Twister. And there are **six** RNG
> families in the binary, not two.

## 2. Native mechanism

### Gameplay: MT19937

The real Mersenne Twister. Used by weather transition rolls (`0025ACA0` scales a draw to
`0..99`), alternate-slot selection, and combat attack variance (`Random(1..1.125)`).

**It is *an* authoritative gameplay stream, not *the* one.** The original wording here claimed
exclusivity; section 8 documents a second gameplay-affecting stream (the shared LCG) that drives
action selection.

### Gameplay: the shared LCG - `RNG_SharedGameplayLCG_NextU32` (`00328370`)

```c
uint RNG_SharedGameplayLCG_NextU32(void)
{
    a     = g_uSharedGameplayLcgState * 0x41C64E6D + 0x3039;
    b     = a                         * 0x41C64E6D + 0x3039;
    state = b                         * 0x41C64E6D + 0x3039;
    g_uSharedGameplayLcgState = state;

    return  (state >> 16 & 0x3FF)
         ^ ((b     >> 16 & 0x3FF) ^ ((a >> 16 & 0x7FF) << 10)) << 10;
}
```

**`0x41C64E6D` = 1103515245 and `0x3039` = 12345 are the ANSI C `rand()` constants**, exactly. The
routine steps that LCG **three times per call** and assembles a **31-bit** result from the high bits
of each iterate - 11 bits from the first, 10 from the second, 10 from the third - which is the
classic "use bits 16 and up, they have the longest period" idiom applied three times.

State lives at `g_uSharedGameplayLcgState` = **`0x022C256C`**, with a setter at `00328D80`.

**Its consumer matters:** `BattleData_ResolveWeightedId` calls it to resolve a weighted action id,
so **every gambit or enemy AI order whose action field has bit 15 set rolls on this stream**, not on
MT19937.

### Presentation: shared bit-feedback PRNG

A separate recurrence with shared state at `01EF93E8` and enable/mode state `022D9138`:

```
feedback = ((((state >> 18) ^ state) >> 4) & 1)
state    = ((((state & 0x003FFFFF) | 0x1FC00000) << 1) | feedback)
```

The resulting bits reconstruct an IEEE-754 float in `[1.0, 2.0)`.

`003D8E50(amplitude)`:
- amplitude == 0 -> return 0 **without touching the state** (a NaN amplitude is not zero: the `jp` at `003D8E60`
  continues);
- otherwise take the sample after recurrence step **5**, return ~~`A * (sample - 1.0)` i.e.~~
  ~~`[0, A)`~~ `f32(sample × A) − f32(A × vf00.w)`, then advance **two more** steps. *(Corrected 2026-09-27, FABLE, Claude Opus 5.5; bytes re-read, on ASTRA's
  [scaled-random-float-order](../_experiments/evidence/scaled-random-float-order/README.md).)* The instructions
  are `mulss` at `003D8F52`, `mulss` by `01EF93FC` at `003D8F5D` and `subss` at `003D8F6D`. `01EF93FC` is
  `vf00.w`, which both of its writers set to 1.0. So the value lies in `[0, A)` like the factored form, but it is
  not bit-identical to `A × (sample − 1)`. ASTRA's original-code window gives `3D1999A0` where the factored form
  gives `3D1999A4`.
- **Total: 7 recurrence steps per nonzero call** *- when the procedural mode word `022D9138` is nonzero (qualified
  2026-09-27, FABLE, Claude Opus 5.5; bytes re-read, on ASTRA's [procedural-mode-cost](../_experiments/evidence/procedural-mode-cost/README.md)).*
  The word is read at `003D8E7D`, after the call to `0036D930`. Mode 0 skips both step blocks (`003D8E8F`,
  `003D8F7C`), so the state does not advance and the result is `A − A × vf00.w`. The scratch writes and the call
  to `0036D8E0` still happen. Every rip-relative store to `022D9138` writes 1: the startup seed `00259220`, and
  `0044BBE1` / `0044C6F6`.

`004005E0` is the sibling: advances exactly **one** step and returns `state - 1.0`, i.e.
`[0, 1)`; it stores the sample at `022D92E0` and copies the 16 bytes there to `022D8F90` even when
the mode word disables the step (EXP-070, 2026-09-11). The bounded helper's own arithmetic —
`trunc(f32(v × B) − f32(B))`, not `trunc((v − 1) × B)` — is on
[the authored-expression page](../02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md) §5. Canonical V120 already classifies it as a shared pseudo-random helper for
procedural rendering with **no PrimaryOwner credit**.

Startup (`00259180`) seeds it explicitly:
```
01EF93E8 = 0x458DC800
022D92E0 = 0x458DC800
022D9138 = 1
```

Because many consumers share the state, you cannot predict a later value from the seed alone
without accounting for every intervening draw.

### Worked consequence

`0040AAD0`, the Presentation backend orientation initializer, calls `003D8E50(0.3)` twice and
subtracts `0.15` each time - two centred perturbations of about `+/-0.15 rad` (+/-8.59 deg).
**One backend rebuild therefore consumes 14 recurrence steps** *(with the mode word nonzero, as above)*.

Broad bootstrap `00266D10` calls `0026D910(1)` twice consecutively, each reaching that
rebuild - **28 steps**. An implementation that "optimised away" the apparently redundant
first apply would end up **14 steps behind** native FFXII in this stream. That is an exact,
observable state-machine difference regardless of the starting state.

> **Anchoring pass 2026-09-03 — partial, and deliberately so.** This document named twenty functions
> in prose and cited none of them by address, which made its own subject matter unreachable from its
> own text. **Nine have been anchored: the ones whose addresses were independently measured** while
> writing
> [`which-roll-is-on-which-generator.md`](which-roll-is-on-which-generator.md) — the LCG's draw sites,
> its state setter, the area-init seed, and the MT draw thunk.
>
> **The remaining eleven are left unanchored on purpose.** `BattleLocomotion_*`,
> `BulletSequentialImpulseSolver_ResetRandomSeed`, `LuaMath_Random*`,
> `RNG_D_Phyre_GenerateRandomFloat01`, `Renderer_CreateRandomNoiseTextureFromGraphicsMT19937` and the
> rest were **not read by the session that added these anchors**, and an address supplied from a name
> lookup is a transcription, not a citation.
>
> **A bulk anchor would have cleared the checker and asserted eleven readings nobody had made.** The
> gap is real and is better left visible.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| *(MT19937 thunk)* | `RNG_MT19937_NextU32_Thunk` (`00379CD0`) | - | gameplay stream |
| `003D8E50` | `SharedProceduralRandom_GenerateScaledFloat01` | 418 B | 7 steps, returns `[0, A)` |
| `004005E0` | shared procedural random helper | 108 B | 1 step, returns `[0, 1)` |
| `00259180` | subsystem init | - | seeds `01EF93E8` / `022D9138` |
| `0040AAD0` | Presentation backend orientation init | 286 B | two `003D8E50(0.3)` calls |
| `0025ACA0` | weather retention roll | 107 B | MT19937 consumer |

## 4. Data structures

```
01EF93E8  u32   shared procedural recurrence state   (seed 0x458DC800)
022D92E0  u32   paired seed value   <- SUPERSEDED 2026-09-26: not a stream global. It is slot A of the shared
                                        transform workbench, a scratch row (see note below)
022D9138  u32   enable/mode
01EF93FC  f32   constant 1.0
```

### The complete consumer census — `UQ-276` ((FABLE, Claude Opus 5.5), 2026-09-26)

**The stream has 114 consumers, not the three functions section 3 tabulates.** Control:
[`members/procedural_stream_census.py`](members/procedural_stream_census.py) (5 checks, FAILS 0). It sweeps the
whole `.text` section, listed bodies or not.
- **Ten functions touch the state `01EF93E8` directly.** They are the seeder, the two helpers above, and seven
  more that step the same recurrence inline. Two of those seven are shared helpers in their own right, each with 36
  caller functions.
- **104 more functions call or tail-jump into one of the ten.** The seven-step helper alone has 49 caller functions
  and 220 call sites.
- **Nothing else reaches the state.** No accessor's address is taken, no data word points near the state, and no
  `lea` forms a base below it. So the list is closed under direct and indirect calls, one hop out.
- **Controls, from this page's own figures:** the seed `0x458DC800` is stored at `00259216`; `0040AAD0` calls the
  seven-step helper twice; the one-step helper has exactly one caller.

*Consequence for determinism:* every visual draw through these 114 functions advances one shared phase. Any
deterministic-visual-parity feature has to replay all of them in order, or give up on phase parity. Section 6's
advice, to regenerate render randomness locally, is the one that scales.

> *Corrected 2026-09-26 (FABLE, Claude Opus 5.5), the "paired seed" at `022D92E0`.* Section 4 called it a stream global. It is
> slot A of [the shared transform workbench](../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-shared-transform-workbench.md),
> which that page already describes as a scratch row with about 250 writers. The census counts 113 functions that
> store or load a whole `xmm` register there. The seeder writes `0x458DC800` into it, and the one-step helper stores
> its sample there, both as scratch; nothing reads it back as stream state.

## 5. Call chain

```
gameplay decision
  -> 0025ACA0 weather roll -> MT19937
  -> combat attack variance -> MT19937

presentation
  -> 0026D910 apply -> 002E3D40 -> 0040AAD0
     -> 003D8E50(0.3)  x2   -> 14 recurrence steps
     -> 0046D160 / 0046D200 -> basis rotation
     -> 0040B430 normalise/publish -> 02CB8420/24/28
        -> 006084B0 -> render-frame descriptor +0x560/564/568
           -> 00604750 double-buffer into current renderer state
```

## 6. Modding notes

- **Never treat `01EF93E8` as world RNG.** It is render-local.
- **Do not remove apparently redundant environment applies.** They advance this stream.
- **XIIOnline:** make the *gameplay* stream's outcomes authoritative - synchronise committed
  results (Weather Slot, damage), not the draws. Let each client regenerate its own
  procedural render randomness. Synchronising `01EF93E8` merely to keep weather coherent is
  over-networking derived local state. A late joiner needs the authoritative Weather Slot; it
  does **not** need the authority's render PRNG phase.

## 7. What is not known

- [x] **UQ-276.** Complete consumer census of the shared procedural stream (needed before any
      deterministic-visual-parity feature).
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): 114 functions, listed in
      [`procedural-stream-consumers.tsv`](procedural-stream-consumers.tsv).** See "The complete consumer census" in
      section 4.
- [x] ~~Designer purpose of the duplicate bootstrap environment apply (open question **D-2**).~~
      **Closed 2026-09-12 as intent residue** on
      [the weather apply page](../03-World-Area-Field/Weather/weather-apply-and-environment-materialization.md)
      §7: the pair is "honour a pending restore, then commit slot 1"; with no restore armed the
      second pass repeats the first, which is where the 14 PRNG steps come from.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Recurrence and 7-step cost | complete executable code `003D8E50..003D8FF1` (418 B, `32f4c933...063a`) | 1 |
| 1-step sibling returning `[0,1)` | complete body of `004005E0` (108 B, `34184564...5bb0`) sharing `022D9138` / `01EF93E8` | 1 |
| Explicit seeding | exact writes in `00259180` | 1 |
| 14 steps per backend rebuild | two `003D8E50(0.3)` calls in `0040AAD0` (286 B, `ace98b94...dd9b`), literal `0.3000000119`, `-0.1500000059` | 1 |
| Duplicate bootstrap apply is real | exact disassembly `00266E72..00266E7B` - two `CALL 0026D910` with no intervening semantic call | 1 |
| Weather roll uses MT19937 | complete body of `0025ACA0` | 1 |

**Superseded readings:** the idea that the first bootstrap environment apply exists to seed
weather interpolation/history is **rejected** - a complete data-reference audit found only one
downstream reader of the normalized vector, and no paired previous/current storage.

## 8. Reopened 2026-09-02 - six families, and a correction

### The correction

Section 1 originally read *"Damage variance, weather changes, drops **and AI choices** come from one
stream"*, and section 2 called MT19937 *"the authoritative gameplay stream"*.

**Both were wrong**, and the same evidence corrects them: `BattleData_ResolveWeightedId`
(`00308EC0`) - the function that turns a gambit's `wActionSelector` into an actual action - calls
**`RNG_SharedGameplayLCG_NextU32` (`00328370`)**, a different generator with its own state at `0x022C256C`.

So AI action choice does **not** come from the Mersenne Twister, and MT19937 is not the sole
gameplay authority. Both statements are struck in place above rather than deleted.

### Six RNG families, not two

The GFZ records a proven partition, and this block confirms family 1 at tier 1 by reading it:

| # | Family | State | Status here |
|---:|---|---|---|
| 1 | **Shared gameplay LCG** | `g_uSharedGameplayLcgState` @ `0x022C256C` | ✅ **read** - see section 2 |
| 2 | Global gameplay MT19937 | 624-word state @ `0x02EB3870` | documented (section 2) |
| 3 | Process-global CRT `rand`/`srand` | external | external mixed authority |
| 4 | Graphics / noise MT19937 | separate 624-word, time-seeded | `Renderer_CreateRandomNoiseTextureFromGraphicsMT19937` |
| 5 | Phyre `PRandomGenerator` | counter/hash state @ `0x02E50260` | `RNG_D_Phyre_GenerateRandomFloat01` |
| 6 | Bullet solver LCG | per-solver seed at `+0xC8`, reset to zero | `BulletSequentialImpulseSolver_ResetRandomSeed` |

Families 3-6 are recorded from GFZ annotation and function naming (tier 3); families 1 and 2 are
tier 1.

> *Family 4 read 2026-09-14 (FABLE, `AD-3`): **it cannot reach gameplay state except as texels.*** Its 624-word state is the
> block `01F7F600`, with index words `01F7FFC0` / `01F7FFC8`. A RIP-relative census of that block finds exactly two
> functions. The seeder `GraphicsNoiseMT19937_SeedFromTimeAndClock` (`0015BCF0`) mixes two time/clock imports, seeds, and
> twists; it has no direct caller and one pointer, in the CRT dynamic-initialiser table at `008C3200`, so it runs once at
> static initialisation. The consumer is `Renderer_CreateRandomNoiseTextureFromGraphicsMT19937` (`001946E0`), whose draws
> (`00194831`–`001948D0`) go into data it hands to the renderer (`0060DD70`, `0062BCB0`, `0063A990`). The twist
> `0018EE20` has no other caller. The builder is reached from `0018D850` ← `0017CF30`, GameApplication's device and
> viewport setup (slot 3). **So family 4 is seeded from the clock once and read once, into a noise texture.** Gameplay
> could only depend on it by reading that texture back, which nothing here was found to do (a texture-readback census was
> not run). The **presentation bit-feedback PRNG** documented in section 2 is a seventh distinct
recurrence and is not in the GFZ's list - it is separately proven here.

> **Crossing into Platform — FINAL-AUDIT pass 22 (FABLE, 2026-09-14).** `0060DD70` is not specific to noise. It is a
> 134-byte texture-description setter.
>
> - Given a mip argument (the fifth), it returns 3 when `1 << mips` exceeds the larger side.
> - Otherwise it stores width, height, a pointer argument and the mip argument at `+0x28`, `+0x2C`, `+0` and `+0x10`.
> - When bit 1 of `+0x18` is set, it recomputes the level count at `+0x14` (`0060DD70`–`0060DDF5`).
>
> Its other caller is the D3D11 device set-up `00625830`, which the ledger files under Platform. That call is at
> `00625C82`, on the object at `+0x2F8`. The shared call means only that the noise texture is described the same way as
> the device's own textures. It adds no path from the graphics MT to gameplay.

### Why this matters more than the correction

**Determinism is per-stream, and the streams have different sensitivities.**

- MT19937 has a 624-word state - reproducing it requires the whole array.
- The **shared LCG has 32 bits of state**, is trivially reproducible, and advances **three
  multiplications per draw**. Anything that calls it once puts every later consumer out of phase.
- Bullet's solver LCG is reset to zero per solve, so physics is not a divergence source through RNG.

**For XIIOnline:** the previous guidance - *"make the gameplay stream's outcomes authoritative"* -
was written as though there were one gameplay stream. There are at least two, and **the LCG is the
one combat action selection depends on**. A shared-world model must account for both, and the LCG is
the easier of the two to synchronise precisely because its state is a single `u32`.

### What is not claimed

The bit-assembly returns 31 bits, but **nothing here establishes the value range consumers expect**
or how `ResolveWeightedId` maps the draw onto its candidate range - that loop was not fully read.
The constants and the state location are exact; the downstream mapping is not. **AD-1.**

> *AD-1 answered 2026-09-12 (FABLE) — the loop read whole, and the tables it walks censused.*
> `BattleData_ResolveWeightedId(record)` (`00308EC0`, 298 B) takes the record's first word: below
> `0x8000` it is **returned as it is** (`00308ED4`–`00308ED7` → `00308FDC`). Otherwise
> `index = word − 0x8000` must lie below the count `u16` at the head of the weighted directory
> `[02EBF160]` (`00308EE9`–`00308F1C`; `0xFFFF` on any miss), and the directory's `u32 offset[index]`
> and `offset[index + 1]`, each resolved through `0020E600`, bound a **run of 4-byte rows
> `{u16 actionId, u8 weight, u8 0}`** (`00308F2C`–`00308F56`). The draw is one call of
> `RNG_SharedGameplayLCG_NextU32` (`00308F61`) reduced **`% 100`** (`00308F69`–`00308F7E`), and the
> walk adds each row's weight and **returns the first row whose cumulative weight exceeds the
> roll** (`00308F90`–`00308FB9`; `0xFFFF` if the run ends first). The shipped directory
> (`battle_pack.bin` directory `+0x2C`, bound to `02EBF160` by the STATIC binder at `00236D35`)
> holds **826 runs of 1–12 rows, and every run's weights sum to exactly 100** — so the `% 100`
> draw always lands and the miss branch is dead for shipped data; every row's id is a plain action
> id ([the action definition row](../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md); run 0, for instance, is 30 % action 427 / 70 % action 150). The 31-bit
> assembly therefore maps onto the range through one modulus and an authored cumulative
> distribution — the enemy order sets carry 5,021 such `0x8xxx` selectors ([the gambit page](../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) §8i).

## 8b. Reopened 2026-09-02 - AD-2 and AD-4: who draws, and what seeds

### The two gameplay streams split cleanly by *what they decide*

Full reverse-edge census over all 38,161 functions:

| Stream | Distinct callers | Owners |
|---|---:|---|
| **Shared LCG** `00328370` | **15** | Spawn 5, CombatAI 3, ActorEntity 2, Movement 2, Party 1, RNG 1, unowned 1 |
| **MT19937** `00379CD0` | **66** | **CombatFormula 53**, CoreRuntime 2, WorldAreaField 2, CombatAction 2, Rewards 2, ScriptVM 2, Status 1, unowned 2 |

Named LCG consumers:

```
Spawn_TrySelectCandidatePosition                 Spawn_PrepareRandomCandidateForCurrentEntry
SpawnPoint_GeneratePositionFromAuthoredRegion    SpawnKeep_InitializeEntriesFromDefinitionTable
AiOrder_EvaluateAndResolveActionTarget           AiOrder_CheckActionPreconditions
AiOrder_SelectFinalTargetFromCandidates          BattleUnit_SeedPartyCombatStanceRecheckTimer
BattleData_ResolveWeightedId
```

Named MT19937 consumers are almost entirely `BattleFormula_*`:

```
BattleFormula_RollGuardParryMode        BattleFormula_RollKnockback
BattleFormula_RollAndStoreComboCount    BattleFormula_RollSpecialGuardOutcome
BattleFormula_RollAvoidGuardParryOutcome BattleFormula_ComputeKnockbackChance
BattleFormula_PrepareStrengthAttackVsDefense   (and 46 more)
```

**The split looked functional:**

> ~~**The LCG decides *decisions*. MT19937 decides *outcomes*.**~~

> **Overstated - corrected in section 8c.** That boundary was drawn from a **call-edge** census,
> which cannot see consumers the compiler **inlined**. Seven loot and enemy-chain functions run the
> LCG recurrence inline and never appear as callers. Loot rolls are outcomes, and they are on the
> LCG. The sentence is struck rather than deleted because the reasoning error - treating a call
> census as a consumer census - is the point.

### AD-4 answered - the LCG seed is a counter, not entropy

`RNG_SharedGameplayLCG_SetState` (`00328D80`) has **exactly one caller** in the entire binary:
`BattleSystem_InitializeAreaState` (`002342F0`) (`002342F0`, WorldAreaField). And what it passes is:

```c
state = g_uAreaInitLcgSeedSequence;
g_uAreaInitLcgSeedSequence = g_uAreaInitLcgSeedSequence + 1;
RNG_SharedGameplayLCG_SetState(state);
```

**The shared gameplay LCG is seeded from a monotonically incrementing counter** - the number of area
initialisations so far. No clock, no `time()`, no entropy source anywhere in the path.

Three consequences, and they are large:

**1. The stream is fully deterministic and reproducible.** Given the same number of prior area
initialisations and the same call order, spawn placement and AI action selection replay *exactly*.

**2. It is trivially synchronisable.** Reproducing this stream needs **one `u32` counter plus a
draw count** - not a 624-word Mersenne state. For XIIOnline that makes the LCG far cheaper to keep
in lockstep than MT19937, which is fortunate, because it is the stream that decides *what enemies
do*.

**3. Seeding is per area load.** The stream restarts on every area initialisation, so divergence
cannot accumulate indefinitely - it resets at each transition. Equally, any client that loads a
different number of areas is immediately out of phase.

### Scope of these claims

The caller counts are a **static** reverse-edge census: they are call sites, not call frequency, and
one unowned caller of each stream remains unidentified. The seeding claim is stronger - `SetState`
has exactly one caller and that body was read in full.

**Not established:** whether anything writes `g_uSharedGameplayLcgState` directly rather than
through `SetState`. The setter is the only *named* path; a direct store would not appear in this
census. **AD-5.**

## 8c. Reopened 2026-09-02 - AD-5: seven inlined consumers the call census could not see

A multi-encoding scan for **writes** to `g_uSharedGameplayLcgState` (`0x022C256C`) found **nine**
write instructions, not the two the call census implied:

| Site | Function | Owner |
|---|---|---|
| `0x003283B9` | `RNG_SharedGameplayLCG_NextU32` (`00328370`) | RNG - the recurrence itself |
| `0x00328D80` | `RNG_SharedGameplayLCG_SetState` | RNG - the setter |
| `0x0031800C` | `EnemyChain_UpdateOnDefeat` (`00317ED0`) | **Rewards** |
| `0x00318496` | `EnemyChain_TryAdvanceRank` (`003183D0`) | **Rewards** |
| `0x0031858B` | `Loot_RollAdditionalItemChance` (`00318510`) | **Rewards** |
| `0x00318641` | `Loot_RollNormalSlotChance` (`003185D0`) | **Rewards** |
| `0x00318761` | `Loot_RollNormalSlotQuantityBucket` (`003186F0`) | **Rewards** |
| `0x00318883` | `Loot_SelectChanceProfileByWeight` (`00318820`) | **Rewards** |
| `0x00319582` | `FUN_00319530` | **Rewards** — CQ-1 answered 2026-09-12 (FABLE): the **chain-rank bonus roll**. Its one caller is `BattleUnit_RunPeriodicCombatMaintenance` (`00311146`, raw `E8` index), right after `Loot_CollectWorldPickupByIndex`; it draws three LCG steps, mixes them into a 0–99 roll, and walks the 7-entry weight row for the chain rank `022C3158` (0–3) in the table at `01EED3B8` — `{100}`, `{80,10,10}`, `{50,20,20,5,0,5}`, `{40,25,25,0,5,0,5}` — returning the first index whose cumulative weight exceeds the roll (0 = no bonus). Kinds 1–2 go to every party slot, 3–6 only to the collecting character (`003111DD`–`003111F1`), each applied as pseudo-action `0xF5` through `BattleFormula_ResolveTargetResult` / `ApplyTargetResult` with the kind's flag word from `013F02C0 + kind·4` (`00311228`–`0031126C`). Not adjacency: read from the caller and the consumer. |

**Seven functions write the LCG state without calling `NextU32`.** They contain the recurrence
**inlined** - which is exactly why section 8b's 15-caller census missed them: an inlined consumer
produces no call edge.

### What this changes

**Loot drops and enemy chain run on the shared LCG.** Not MT19937. So the "decisions vs outcomes"
boundary in section 8b is wrong as stated: whether an extra item drops, which chance profile is
picked, and how the chain rank advances are all **outcomes**, and all on the LCG.

The corrected statement is narrower and still useful:

> **MT19937 is the combat-formula stream** - 53 of its 66 callers are `BattleFormula_*`.
> **The shared LCG carries everything else that matters**: spawn placement, AI target and action
> choice, stance timers, **loot rolls and enemy chain**.

**For XIIOnline this raises the stakes considerably.** Section 8b argued the LCG is cheap to
synchronise because its state is one `u32`. That is still true, and now it matters more: **loot is
on that stream.** Two clients out of phase on the LCG will disagree about what drops, not merely
about where a monster spawned.

It also means loot is **fully deterministic per area seed** - the seed is `g_uAreaInitLcgSeedSequence++`
(section 8b), so a given area load produces a fixed draw sequence, and drop outcomes follow from how
many draws precede them.

### The methodology error, named

Section 8b built a consumer census from **call edges** and presented it as complete. A call-edge
census answers *"who calls this function"*, not *"who uses this state"* - and for a 91-byte
arithmetic routine, the compiler inlines it freely.

**The right question for a shared global is "who writes it", not "who calls its accessor."** The
write scan is what found the seven. This is the same failure class already recorded twice in this
database: a narrow instrument reported as a complete answer. The correction cost one scan; the claim
had already been published.

**AD-2 is revised accordingly**, and `FUN_00319530` - an unowned function that writes gameplay RNG
state - is flagged as **AD-6**.

## 8g. A third random source — and it is not peripheral (2026-09-02)

This document describes **two** RNG streams. There is a **third**: the **CRT `rand()`**, imported
from `api-ms-win-crt-utility-l1-1-0.dll` through IAT slot `0x008C3098`.

> **This section was first written the same day claiming `rand()` was used only by the sound
> driver.** That was wrong, and wrong in the direction that matters — it is used across gameplay.
> The census below replaces it.

### Where it is actually used: 48 call sites across 30 functions

Counted by scanning `.text` for `FF 15` indirect calls resolving to the `rand` import slot:

| Subsystem | Functions | Notable |
|---|---:|---|
| **Movement** | 7 | `BattleLocomotion_TryStartRandomizedAvoidanceManeuver`, `BattleLocomotion_TryChooseReachable…`, `BattleLocomotion_ResetAvoidanceStateRandomized`, `PartyFollow_SolveFormation` |
| **Audio** | 7 | `RandomSound`/`CycleSound` selection and siblings |
| **Combat Action** | 3 | **`BattleAction_ComputeChargeLimitTicks`**, `BattleSpecialSequence_BuildRandomised…` |
| **Presentation** | 2 | `BattlePresentation_EnqueueReaction…` |
| **Combat Formula** | 1 | |
| **UI** | 1 | |
| **Lua** | 2 | **`LuaMath_Random`, `LuaMath_RandomSeed`** |
| unowned | 7 | |

**Two facts change the picture:**

1. **`rand()` decides gameplay.** Charge-limit ticks, locomotion randomisation and party formation
   are not cosmetic. "The two gameplay RNG streams" understates what randomises this game.
2. **Lua's `math.random` is `rand()`.** `LuaMath_Random` and `LuaMath_RandomSeed` call it directly,
   so any script randomness shares this stream — and `math.randomseed` reseeds it **process-wide**.

### There are two `rand` entry points

| | Address | Callers |
|---|---|---|
| **imported** `rand` | IAT `0x008C3098` → `api-ms-win-crt-utility-l1-1-0.dll` | **48 sites / 30 functions** |
| **statically linked** `rand` | `0x00861F38` | 1 site, from `00149610` |

A census that counts only direct `E8` calls to `0x00861F38` finds **one** caller and misses all 48.
That is how this was nearly missed twice.

### What it means for determinism

`rand()` carries **no seed in the save image** and is not part of the transition record, so unlike
the counter-seeded shared LCG it is **not reproducible across runs** from saved state. In the UCRT
its state is **per-thread**; whether the audio, movement and combat consumers here share a thread is
**not established**, so no claim is made about whether a sound draw perturbs a locomotion draw.

**For XIIOnline:** anything routed through `rand()` — locomotion randomisation, charge-limit ticks,
reaction enqueue, and all script `math.random` — will **diverge between clients** and cannot be
synchronised by sharing a gameplay seed. That is a materially different exposure from the LCG and
MT19937 paths.

## 9. Related

- [`../03-World-Area-Field/Weather/weather-probability-and-transition-roll.md`](../03-World-Area-Field/Weather/weather-probability-and-transition-roll.md)

## Re-verification 2026-09-02 (AH-13)

Stamped against parent `381d2aea...`; the stamp is advanced to `2ed8affb...` on work already
performed against that parent **today**, not on a fresh pass.

This document was **reopened and corrected twice in one session**:

1. `RNG_SharedGameplayLCG_NextU32` (`00328370`) was read in full against the current parent, confirming the
   ANSI C `rand()` constants `0x41C64E6D` / `0x3039`, the three-step recurrence and the
   bit-interleaved draw assembly.
2. Section 8b's consumer census was **retracted** - it was built from call edges, which cannot
   see inlined consumers, and a write-instruction scan then found seven Loot/EnemyChain
   functions inlining the recurrence directly.

The second is the stronger provenance evidence of the two: a document that has been falsified
against the current parent and then repaired against it has been tested more severely than one
that merely passed a re-read.

**Stamp advanced. No new claim is made here** - this section records why the stamp is earned
rather than restamped.

## 9. Independent falsification pass 2026-09-07 — `xiionline-61`

**First genuine attack on this document.** Its only prior stamp was
`last_pass_state: reverification-against-current-parent` — a provenance check, not a pass. Program
state **GN160** `fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708`; everything below
re-derived by disassembling the authorized EXE.

### Survived — the LCG reproduces exactly, to the bit

The published body of `RNG_SharedGameplayLCG_NextU32` (`00328370`, 91 B) was checked instruction by
instruction against the disassembly. **Every element holds:**

| claim | verified |
|---|---|
| constants `0x41C64E6D` / `0x3039` | ✅ both, at all three steps |
| **three** LCG iterations per call | ✅ `imul` at `00328370`, `0032837F`, `00328399` |
| 11 bits from the first iterate | ✅ `and edx, 0x7ff` |
| 10 bits from the second | ✅ `and r8d, 0x3ff` |
| 10 bits from the third | ✅ `and eax, 0x3ff` |
| the XOR/shift assembly as printed | ✅ `edx <<= 10`, `r8d ^= edx`, `r8d <<= 10`, `eax ^= r8d` |
| a **31-bit** result | ✅ the highest occupied bit is 30 |
| state at `0x022C256C` | ✅ on both the load and the store |

**This is the most precisely correct formula this session has audited.** It is published in a form a
reader can execute, and it executes.

### The finding — the named function is one draw site of eight

**The LCG is inlined.** The multiplier `0x41C64E6D` appears in **8 functions across 24 sites** — three
per function, the complete three-step sequence each time — and only **one** of those functions is
`RNG_SharedGameplayLCG_NextU32`:

| function | owner | sites |
|---|---|---:|
| `EnemyChain_UpdateOnDefeat` (`00317ED0`) | Rewards | 3 |
| `EnemyChain_TryAdvanceRank` (`003183D0`) | Rewards | 3 |
| `Loot_RollAdditionalItemChance` (`00318510`) | Rewards | 3 |
| `Loot_RollNormalSlotChance` (`003185D0`) | Rewards | 3 |
| `Loot_RollNormalSlotQuantityBucket` (`003186F0`) | Rewards | 3 |
| `Loot_SelectChanceProfileByWeight` (`00318820`) | Rewards | 3 |
| `FUN_00319530` | — | 3 |
| **`RNG_SharedGameplayLCG_NextU32`** (`00328370`) | RNG | 3 |

Each inline copy **reads and writes `0x022C256C` directly** — confirmed by the state census: **nine
write-form and eight read-form references**, seven of the writers being the inlined copies, plus the
named function and the setter `RNG_SharedGameplayLCG_SetState` (`00328D80`).

> **Hooking `RNG_SharedGameplayLCG_NextU32` intercepts one draw site in eight.** Every loot roll and
> every chain update advances the shared gameplay stream **without calling it**. A mod that redirects
> the named function to synchronise randomness across clients would leave **loot and the enemy chain
> — the two things players most notice diverging — completely unsynchronised**, while appearing to
> work everywhere else.

**The single intercept point that does work is the state word itself**, `0x022C256C`: all eight
copies read and write it, so a watch or a hook on the memory catches every draw, and
`RNG_SharedGameplayLCG_SetState` is the one place that sets it from outside.

**And it says something about the engine, not just about hooking it:** every inline site is
**Rewards/Loot**. The shared gameplay LCG's heaviest consumers are drops and the chain, and the
compiler inlined it into each of them because each calls it exactly once in a hot path.

### Not examined

The MT19937 stream, the presentation bit-feedback PRNG's recurrence, the "six RNG families" count,
§8b's seed-is-a-counter argument, and the call chain in §5. **This pass attacked the shared LCG
body and its draw sites only** — everything else in this document remains unaudited and must not be
recorded as having passed.

## 10. Extension 2026-09-07 — `CQ-2`: the other streams, and MT19937 is standard after all

`xiionline-61`, GN160. **Same method as section 9, same positive control** — the shared LCG's
defining constant re-censused first and returning its known 8 functions / 24 sites before any other
result was believed.

### The contrast that matters for hooking

| stream | defining constant | functions | sites | inlined? |
|---|---|---:|---:|---|
| shared gameplay LCG | `0x41C64E6D` | **8** | 24 | **yes — 7 inline copies** |
| MT19937 twist | `0x9908B0DF` | **2** | 6 | **no** |
| MT19937 seed | `0x6C078965` | 3 | 6 | no |

> **MT19937 is not inlined and the shared LCG is.** So `RNG_MT19937_NextU32` *is* a real intercept
> point — hooking it catches every gameplay Mersenne draw — while hooking
> `RNG_SharedGameplayLCG_NextU32` catches one draw in eight. **Two streams in one engine with
> opposite hookability, and nothing in either name tells you which.**

### There are two Mersenne Twisters, with separate state

The two twist functions are **not** one function inlined twice — they are two instances:

| instance | role | address | name |
|---|---|---|---|
| **gameplay** | twist | `00866B90` | `RNG_MT19937_TwistState` |
| **gameplay** | seed | `00866D60` | `RNG_MT19937_SeedState` |
| **graphics noise** | twist | `0018EE20` | `GraphicsNoiseMT19937_TwistState` |
| **graphics noise** | seed | `0018D740` | `GraphicsNoiseMT19937_SeedState` |

*(One address, one name, one row — a combined row cross-pairs under `check_consistency.py`, which is
a defect this database recorded earlier the same day and which this section then committed.)*

The **gameplay** instance is reached from `RNG_MT19937_NextU32`, `RNG_MT19937_NextFloatClosed` and
`RNG_MT19937_Seed`; the **graphics noise** instance only from `GraphicsNoiseMT19937_SeedFrom…` and
`Renderer_CreateRandomNoiseTextureFromGraphicsMT19937`.

**A noise texture and a damage roll do not share a stream**, and the graphics instance is reachable
only from renderer code.

### ⚠ The tempering constants are absent from the image, and the tempering is present anyway

**A byte-level absence, verified with a control, that would have produced a false finding.**

`0x9D2C5680` and `0xEFC60000` — the standard MT19937 tempering masks — occur **zero times in the
entire 32 MB image**, as immediates *or* as data. The control: `0x9908B0DF` occurs 10 times,
`0x6C078965` 10, `0x41C64E6D` 24. **The zero is real.**

**And MT19937's tempering is exact.** `RNG_MT19937_NextU32` (`00863BF0`) ends:

```c
y = state[i] ^ (state[i] >> 11);
y = y ^ ((y & 0xFF3A58AD) << 7);
y = y ^ ((y & 0xFFFFDF8C) << 15);
return y ^ (y >> 18);
```

The compiler rewrote `(y << s) & M` as `(y & (M >> s)) << s` — a legal strength reduction, since the
bits the mask would have cleared are exactly the bits the shift discards:

```
0x9D2C5680 >> 7  = 0x013A58AD   and   0xFF3A58AD & 0x01FFFFFF = 0x013A58AD   ✔
0xEFC60000 >> 15 = 0x0001DF8C   and   0xFFFFDF8C & 0x0001FFFF = 0x0001DF8C   ✔
```

**Verified by execution, not by inspection:** both forms evaluated over **200,000 random 32-bit
inputs — zero mismatches**, plus the edge cases `0`, `1`, `0xFFFFFFFF`, `0x80000000`.

> **This is textbook MT19937, and searching for its most famous constants finds nothing.** Stopping
> at the census would have published *"the game's Mersenne Twister omits the tempering step"* — false,
> and ruinous for anyone reproducing the stream for a deterministic client. **The absence is real at
> the byte level and false at the semantic level**, and only reading the body separates the two.

### Not examined

The presentation bit-feedback PRNG. Its recurrence masks `0x1FC00000` and `0x003FFFFF` are **not
discriminating** — they return **39 functions and 1,076 sites**, which is a common bit pattern rather
than a signature. **That census is reported as an instrument failure, not a result**; the question of
whether the presentation stream is inlined remains open as `CQ-5`.

### ✅ The third seed site is not a Mersenne Twister (`CQ-6`, answered 2026-09-13, FABLE)

The table's third `0x6C078965` function is `0074BDE0`, with four of the six sites. It is **Marsaglia's xorshift128**, seeded
with MT19937's initialisation recurrence, inlined into a routine in the Yebis / PPFX object (a member of `ppfx-span.tsv`; the
"unowned" of `CQ-6` predates that row). No 624-word state, no twist and no tempering are involved.

```text
0074BFE0..0074BFF5  c = ++[01F3CD6C]                       ; .data counter, initial value 1
0074BFFC..0074C04F  x = K*(c ^ c>>30) + 1                  ; K = 0x6C078965, the four imul sites
                    y = K*(x ^ x>>30) + 2
                    z = K*(y ^ y>>30) + 3
                    w = K*(z ^ z>>30) + 4
0074C0A7..0074C0C4  t = x ^ (x << 11);  x,y,z = y,z,w;  w = w ^ (w >> 19) ^ t ^ (t sar 8)   ; drawn twice per sample
```

**Reproduction detail:** the `t >> 8` is an **arithmetic** shift (`sar`, `0074C0BD` / `0074C108`). Marsaglia's reference
uses an unsigned shift, so a textbook xorshift128 diverges from this one whenever `t`'s top bit is set.

**What it generates: stratified unit-disk sample kernels.** Each draw becomes `u = (v & 0x7FFFFFFF) · 2⁻³¹`
(`00DA5E24`). For an `N × N` grid, the sample in stratum `(i, j)` is

```text
r = 0.01 + 0.99 · sqrt((u₁ + i) / N)          ; 008F30E4 = 0.01, 008F3110 = 0.99
θ = 2π · (u₂ + j) / N                          ; 01CEBC08 = 2, 00D11784 = π
entry = { r·cos θ, r·sin θ, 0, 0 }             ; 16 bytes
```

The kernels are written to `02EA24A0`, one `0x400`-byte level per grid size (64 entries). The first call builds levels
0–5 (`N` = 3…8) and sets the flag `02EA3CA4`. A later call rebuilds only the level it uses, when its byte argument
`[rbp+0x1F8]` is non-zero. **The counter advances once per level built**, so a rebuilt kernel is not the one first built. The routine
first scans the 64-word array based at `this + 0x764C` from its index argument upward for a non-zero word (`0074BE40`–`0074BE5A`).
If it finds none, it returns `E_NOTIMPL` `0x80004001` (`0074BE5C`). Otherwise, with `k` the index found, it uploads the level for
`N = trunc(sqrt(k))` through the device's slot `0x98` (`0074C2AA`).

**Scope of the "graphics only" reading, and how it was checked:** a capstone rip-relative census of all of `.text` finds the
counter `01F3CD6C` read and written **only** in `0074BDE0` (two sites), and the table `02EA24A0`–`02EA3CA7` referenced
only there (8 sites). The generator state (`x, y, z, w`) lives in locals and registers. **Nothing this stream produces can reach a
gameplay generator.** Which PPFX effect consumes the kernel is narrowed one hop (interior read 2026-09-17,
SWE2-FRONTIER): `0074C4D0`'s one caller is `00741680` (2,577 B, call at [`00741971`](../_index/ADDRESS-INDEX.md)) — a
PPFX-span worker (`ppfx-span.tsv`) reached only from `006F61F0`; the body runs `007422F0` ×2 ahead of
the kernel pull, then the `007224C0`/`007231A0`/`00740BE0` particle-helper triple afterward. Which
effect owns `006F61F0` remains unestablished. The third member of the triple is now read (interior
2026-09-17, SWE2-FRONTIER): `00740BE0` (1,694 B) is a **particle constant-committer** — it takes a
parameter-table object whose `[rdi+0x48..0x54]` fields hold buffer-slot ids and `[rdi+0x100..0x10C]`
hold constant-register indices, stages float4 rows into the scratch vectors `02EA1C50` and
`02EA1A50`, then pushes them through `[rdi+0x38]`'s vtable — `+0x98` set-constant-vector ×4
(first at [`00740D85`](../_index/ADDRESS-INDEX.md)), `+0xB8` set-buffer ×4 on the slot ids,
`+0x70`/`+0x68` get/set-count pairs — after normalising `ebx = [rsi+0xB0]` through the
`00713D70`/`00713820` type-tag queries and clamping a count to ≤8 at `00740C5B`. The
`007422F0` double-call ahead of the kernel pull is also read (2026-09-17): a 1,460-B
particle-parameter sub-computer chaining `00731DB0` ([`007423CD`](../_index/ADDRESS-INDEX.md)),
`006E9C20` (interior: `00861F4A` string/format helper ×4 beginning `006E9D05`, then
`006E9A90` ×2 at `006E9EAA`/`006E9EC4` — a diagnostic-emitting leaf), `007233F0`, `00722E80`,
`007231A0`, `00735B70`, `00735720` (interior: `007233F0` at `00735791`, `006DF480` ×2,
`00735E40`/`00734EB0` tail — a mid-level combiner; `00735E40` itself read: `007233F0` at
`00735EDF`, `00732D80`/`00735720`/`00808C40` — another combiner-level member) — the same
`0072xxxx`/`0073xxxx` helper family the post-kernel triple belongs to.

## 11. The state layouts, and the step count that decides determinism (2026-09-10)

§4 lists four globals and calls itself *"Data structures"*. It has no layout for either Mersenne
state and no step contract for the shared LCG — which are the two things a parity test actually
needs. Both are recovered here and promoted to `_types/`.

### `Mt19937State` — `0x9C4`, and the two halves are proven adjacent

`RNG_MT19937_SeedState` (`00866D60`) is nine instructions of textbook MT19937:

```asm
00866D60  mov   dword ptr [02EB3870], edx        ; mt[0] = seed
00866D73  mov   edx, [rax - 4]                   ; loop: mt[i-1]
00866D7A  shr   edx, 0x1e                        ;       >> 30
00866D7D  xor   edx, [rax - 8]
00866D80  imul  ecx, edx, 0x6c078965
00866D86  add   ecx, r8d                         ;       + i
00866D8C  mov   [rax - 4], ecx
00866D8F  cmp   r8d, 0x270                       ; 624
00866D98  mov   dword ptr [02EB4230], 0x270      ; index = exhausted
```

`0x02EB3870 + 624 * 4 = 0x02EB4230` **exactly**, so the cursor is not placed next to the vector by
assumption — the seed's own final store lands on the byte after it.

**The index convention is the part worth getting right.** Seeding leaves it at **624**, meaning
*exhausted*, so the first draw after a seed twists before returning anything. An implementation that
initialises the cursor to 0 returns 624 values from the un-twisted seeded vector before it ever
agrees with the original.

**Two instances, separate state.** The gameplay stream's vector is static at `02EB3870`; the
graphics-noise stream's is **caller-supplied** — `0018D740` takes it in `rcx` and runs the identical
loop, with `0018D761 lea rdx,[rcx+0x9BC]` reaching `mt[623]`. Same type, two storage classes. A
noise texture and a damage roll cannot influence each other.

**The SIMD branch is not a behavioural one.** Both twist functions test the dword at `01F44858`
against 2 and take a vectorised path when it is at least that, a scalar path otherwise. Both compute
the same recurrence, so it is a CPU-feature switch — but a reimplementation that reproduces only one
path still has to match the *other* path's results, not merely its own.

### `SharedGameplayLcgState` — one word, and **three steps per draw**

The shared stream is the stock MSVC `rand()` recurrence, `state = state * 0x41C64E6D + 0x3039`.
`Loot_RollNormalSlotChance` (`003185D0`) shows the shape that matters:

```asm
003185E4  imul  eax, dword ptr [022C256C], 0x41c64e6d   ; step 1, reads the global
003185EA  add   eax, 0x3039
00318601  imul  r8d, eax, 0x41c64e6d                    ; step 2
00318621  imul  eax, r8d, 0x41c64e6d                    ; step 3
00318641  mov   dword ptr [022C256C], eax               ; ONE writeback, after all three
```

**A draw advances the shared LCG by three steps, not one.** Each step contributes bits 16 upward —
11 bits from one, 10 from another — shifted and XORed together, and the result is reduced with the
compiler's divide-by-100 idiom (`0x51EB851F`, `sar 5`) into a 0–99 percentage.

> **This is the single fact most likely to break a reconstruction's determinism.** Every roll on
> this stream consumes three LCG steps. Step once per draw and the very first loot roll agrees by
> luck at best, and every subsequent roll on the stream is wrong.

The three-step-one-writeback shape repeats at `00318510`, `003186F0`, `00318820`, `00319530`,
`00328370` and in `EnemyChain_TryAdvanceRank` (`003183D0`). `00328D80` writes the word without
reading it — that is the reset.

### Why the two streams need different reconstruction strategies

| | shared LCG | gameplay MT19937 |
|---|---|---|
| state | one word at `022C256C` | `0x9C4` at `02EB3870` |
| inlined? | **yes**, 8 functions / 24 sites | **no** |
| single point to reimplement? | **no** — every consumer carries its own copy of the three-step draw | **yes** |
| single point to hook? | no — hooking the one out-of-line copy catches one draw in eight | yes |

**Nothing in either stream's name tells you which it is**, and the difference decides whether a
reimplementation can swap one function or must touch every consumer.

### Limits

- **Static only.** No runtime observation confirms a live state vector or a draw sequence, and none
  of the per-consumer bit extractions has been compared against the original's output.
- **`Mt19937State.index` is proven for the gameplay instance.** The graphics-noise seed returns
  without writing a cursor, so who initialises that instance's index is **not** established.
- Which stream each *individual* roll uses is §9 and §10's census, not re-derived here.
- The three-step count is proven for the eight sites named above. It is not a claim about every
  consumer of the stream.

## 12. Streams 4 and 5, the bodies read whole (2026-09-19, FABLE)

**Stream 5 is a counter hash - `006B05E0` (76 B).** Not a recurrence: the state `02E50260` is a plain counter.

```
c = ++[02E50260]
x = (c ^ 0x00BC602F) * 0x9E3779B9
y = ((x << 6) ^ (x >> 26) ^ x) * 0x9E3779B9
r = ((y << 5) ^ (y >> 12)) + y
result = (float) r * 2^-32            in [0, 1)
```

A rip-relative sweep of `02E50260` finds this body as the state's **only reader and only writer**, and the state is
zero-initialised. **So nothing seeds it: the k-th call returns the same float in every run of the game.** Any
divergence between two machines in this stream is a difference in *how many times* it was called, never in a seed.
The body has no call or jump site in `.text`; it is reached through a pointer, and who holds that pointer was not
established.

**Stream 4's seed mixer - `0018D680` (179 B).** It folds the eight bytes of its first argument and the four bytes
of its second with fixed multipliers - chains of `x 0x101` and the constants `0x23150701`, `0x140F0601`, `0x0A0A0501`,
`0x04060401` - then adds a **call counter** kept at `01F7FFD0` to the first fold, xors in the second, and increments
the counter: two seedings inside the same clock tick still produce different seeds. Its one caller is the
time-and-clock seeder of the graphics-noise twister. *Which bytes of the two arguments are the time and which the
clock was not traced.*

| body | anchors |
|---|---|
| `0018D680` noise seed mixer (179 B) | `0018D68A`, `0018D6A2`, `0018D6AF`, `0018D6BA`, `0018D6C4`, `0018D6D2`, `0018D6E0`, `0018D6F4`, `0018D706`, `0018D70C`, `0018D723`, `0018D729`, `0018D72C` |

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CoreRuntimeScheduling — CLIENT.** `FUN_0022b6e0`, owned by that layer, calls `00379CD0` on this page. That caller is boot frame mode 0: a fixed sequence of six calls - one of them a **Mersenne draw whose value is discarded** - and then a spin on `[02EBA3F8]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — CLIENT (28 edges through 3 of this page's functions).** The Input layer reaches this page at `0063A990`, `0022B6E0`, `00266D10`. `FUN_00226be0` is the worked example, read in full - it is a 1,936-byte channel step whose first act is to test `1 << channel` against the mask at `[01FD46D4]`; **1 of the 28 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — SERVICE (SWE2-CONTRACT 2026-09-15, 1 edge, R3-visible).** The same boot-mode-0 body
`0022B6E0` also calls `0032E520`, the resource-request-queue drain (`arg 0` pumps until idle,
non-zero only asks whether anything is outstanding — per the resource-request-queue page). One
small call beside the discarded Mersenne draw, not a shared responsibility.

## SWE2-EC7-36 update (2026-09-19) - `0062BCB0`

`0062BCB0` (647 B) is an RNG stream body - `01F7F590`/`01F7F5B8` state, `0062EC70`/`0062B870`/`0062B100`/`00584730`. Interior anchor `0062BCBE` (an `0062EC70` call).

## SWE2-EC7-44 update (2026-09-19) - `0018D740`

`0018D740` (263 B) is `GraphicsNoiseMT19937_SeedState` - call-free MT19937 init-by-seed: `mt[0]=edx` then `0x6C078965*(mt[i-1]^(mt[i-1]>>30))+i` to `i`=624, SIMD 8-unrolled `pmulld`/`psrld`/`pxor` path under the `01F44858` feature gate plus a scalar tail. Interior anchor `0018D820` (the scalar recurrence loop).

## SWE2-EC7-56 update (2026-09-19) - `0062EC70`

`0062EC70` (204 B) is an RNG stream body - `0016D6D0`/`0016DA60` plus one vcall. Interior anchor `0062ED08` (a `0016D6D0` call).

