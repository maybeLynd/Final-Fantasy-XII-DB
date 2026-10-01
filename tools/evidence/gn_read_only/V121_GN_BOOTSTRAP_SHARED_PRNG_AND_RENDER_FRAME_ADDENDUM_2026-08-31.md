# V121 GN — BOOTSTRAP SHARED PRNG + RENDER-FRAME ADDENDUM — 2026-08-31

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Secondary use:** XIIOnline weather / Presentation determinism research  
**Intended physical parent:** GM160 recovery-transfer GZF contained in the uploaded handoff ZIP  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. GFZ accounting

No GM160 mutation is claimed.

Persistence-certified GM160 remains:

- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

This document refines the already-observed broad-bootstrap transaction:

`00266D10`
→ `0026D910(1)`
→ `0026D910(1)`

and explains one real non-idempotent consequence of the apparently duplicated Weather/environment application.

It does not change either strong current GN unresolved proposal:

1. `00313A00` — `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`
2. `002F7380` — `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

---

# 1. The two bootstrap Weather applies are literally consecutive

Inside broad Core/Actor/global bootstrap `00266D10`:

```text
00266E42  MOV EBP,1
...
00266E72  MOV ECX,EBP
00266E74  CALL 0026D910
00266E79  MOV ECX,EBP
00266E7B  CALL 0026D910
00266E80  CALL ...
```

There is no semantic caller-side operation between the two `0026D910(1)` calls.

Therefore any difference between the first and second pass arises from:
- state changed inside the first apply;
- transitive side effects of the first apply;
- or both.

Prior work proves that world-transition `bInitializationRestoreState` can make the first pass materialize the previously persisted Weather Slot while the second pass commits baseline slot 1.

---

# 2. Direct environment state from the first pass is overwritten before later frame consumption

`0026D910` publishes slot-specific environment state through:

`00180620`
→ `001A7E40`

The environment object receives:
- slot-indexed scalar lanes;
- a slot-indexed direction vector;
- additional slot-indexed environment parameters.

When enabled, the direction vector is normalized through `001F08A0` and published into globals:

`02CB8420 / 02CB8424 / 02CB8428`

A complete data-reference audit finds one downstream reader of that normalized vector:

`006084B0`

which copies it into a **0x598-byte render-frame descriptor** at:

- `+0x560`
- `+0x564`
- `+0x568`

Adjacent environment globals are copied into neighboring descriptor fields.

The sole higher frame builder `00604750` later double-buffers the resulting 0x598-byte descriptor into current renderer state.

There is no render-frame consumer between the two consecutive `0026D910(1)` calls in `00266D10`.

Thus the restored-slot direction/environment values published by the first call are overwritten by the second slot-1 application before the later renderer-frame snapshot observes the final state.

This rules out treating the first pass's direction vector as a persistent previous-weather history lane.

---

# 3. The environment direction is current render input, not interpolation history

`001F08A0`:

1. transforms the supplied direction convention;
2. stores the current raw direction in the live environment object;
3. normalizes the vector;
4. writes the normalized current vector into `02CB8420..28`;
5. sets an enable state.

The only identified renderer consumer copies that current vector into the current frame descriptor.

No paired previous/current vector storage has been established in this family.

Therefore earlier speculation that the first restored Weather pass exists specifically to seed Weather interpolation/history is **rejected by current evidence**.

Do not rename this vector as:
- previous Weather direction;
- interpolation source;
- Weather history;
- transition blend source.

Its exact physical rendering role — e.g. sun direction, directional-light vector, another environment orientation — remains below the current proof threshold.

---

# 4. `003D8E50` is a shared scaled pseudo-random float helper

The first pass nevertheless has a surviving transitive side effect.

`0026D910`
→ zero-mode `002E3D40`
→ canonical Presentation backend initializer `0040AAD0`

and `0040AAD0` invokes:

`003D8E50`

**twice**.

## `003D8E50`

Executable code range:
- `003D8E50 .. 003D8FF1`
- **418 bytes**

Exact executable-code SHA-256:
`32f4c93324e6c153518b5b42e85597f75495de8f66171fd58daf355e7b9a063a`

Inputs:
- scalar amplitude in `XMM0`.

Exact behavior:

### Zero amplitude
If amplitude compares equal to 0:
- return 0;
- do not enter the random-state update path.

### Nonzero amplitude
The helper uses:
- enable/mode state `022D9138`;
- shared 32-bit state `01EF93E8`;
- constant `1.0f` at `01EF93FC`;
- shared scratch/save-restore support around `36D930 / 36D8E0`.

The recurrence repeatedly performs the same bit-feedback step:

```text
feedback = ((((state >> 18) XOR state) >> 4) & 1)

state =
    ((((state & 0x003FFFFF) | 0x1FC00000) << 1)
     | feedback)
```

The resulting state bits reconstruct an IEEE-754 float with exponent corresponding to the interval:

**[1.0, 2.0)**

The helper uses the state after its fifth recurrence step as the visible sample.

With positive amplitude `A`, the returned scalar is exactly:

**A × (sample - 1.0)**

therefore:

**[0, A)**

After producing that visible value, the helper advances the same shared state **two additional recurrence steps** before returning.

Thus each nonzero `003D8E50` call consumes:

**7 recurrence steps total**
- sample taken after step **5**
- persisted exit state after step **7**

Strong conservative mechanism name:

`SharedProceduralRandom_GenerateScaledFloat01`

or:

`Runtime.Random.SharedBitFeedbackFloatScaled`

Do not identify it with FFXII's gameplay MT19937.

---

# 5. Independent canonical V120 corroboration — `004005E0`

Canonical V120 already classifies:

## `004005E0`

as a:

**shared pseudo-random/scratch-state helper used by procedural rendering**

with **no PrimaryOwner credit**.

Exact canonical body:
- **108 bytes**
- SHA-256:
  `34184564ebd7a36bfe008b7a0b745340079bd80b671844a6284d4b0bb02f5bb0`

Its exact body uses the same:
- `022D9138`
- `01EF93E8`
- bit-feedback recurrence.

Unlike `003D8E50`, `004005E0` advances exactly **one** recurrence step and returns:

**state - 1.0**

which is a shared pseudo-random float in:

**[0, 1)**

This independently validates the random-stream interpretation without assigning Presentation ownership to the numeric helper.

---

# 6. Startup initializes the shared recurrence explicitly

Broad subsystem initializer:

## `00259180`

contains the exact writes:

```text
01EF93E8 = 0x458DC800
022D92E0 = 0x458DC800
022D9138 = 1
```

before continuing subsystem startup.

The recurrence then converts the lower state bits into the normalized `[1,2)` float representation on its first update.

This is a deliberately initialized shared pseudo-random state family, not accidental uninitialized scratch.

Because many other functions also consume the same state, the exact state reaching a later Weather/bootstrap event depends on all prior consumers. A fixed numerical bootstrap random output must therefore **not** be inferred solely from the startup seed unless all intervening draws are accounted for.

---

# 7. `0040AAD0` uses two centered procedural-random orientation offsets

## `0040AAD0`

Canonical role:
**Presentation backend mode/orientation initializer**

The complete executable body contains two calls:

```text
003D8E50(0.3f)
```

The literal amplitude is:

`0.3000000119...`

After each draw the caller subtracts:

`0.1500000059...`

Therefore each call produces a centered random perturbation of approximately:

**[-0.15, +0.15)**

### First perturbation

The first centered random value is added to a mode-dependent base angle and passed into:

`0046D160`

before a matrix/basis multiplication.

### Second perturbation

The second centered random value is combined with another mode/index-dependent angular term and passed into:

`0046D200`

before another basis multiplication.

The resulting basis is then normalized/published by:

`0040B430`.

Thus the random stream contributes to the **Presentation backend orientation/basis construction**.

The exact designer-facing visual purpose of this randomized orientation is not yet named.

---

# 8. One `0040AAD0` consumes 14 recurrence steps

Each `0040AAD0` performs:

- first `003D8E50(0.3)` → **7** recurrence steps;
- second `003D8E50(0.3)` → **7** recurrence steps.

Total:

**14 shared recurrence steps per backend orientation rebuild.**

The two consecutive bootstrap Weather/environment applies each reach this backend rebuild.

Therefore the native pair consumes:

**28 recurrence steps**

through these two Presentation-random calls alone.

A hypothetical implementation that skipped the restore-aware first Weather/environment pass and executed only the final slot-1 pass would finish:

**14 recurrence steps behind native FFXII**

in this shared procedural-random stream.

That is an exact state-machine difference, independent of the unknown starting state.

---

# 9. The duplicate bootstrap is therefore not semantically equivalent to one final apply

Even though the second Weather/environment application overwrites the final visible:
- Weather Slot;
- current environment vector;
- backend mode/basis state;

the first call cannot simply be treated as a dead duplicate.

At minimum it:

1. consumes/clears the world-transition initialization/restore state when active;
2. runs the complete environment/Presentation materialization path;
3. advances the shared procedural-render pseudo-random stream by **14 recurrence steps**.

The exact higher-level designer reason for invoking the full transaction twice remains unresolved.

Do **not** claim that the duplicate exists specifically:
- to advance the PRNG;
- to randomize the final Weather;
- to seed interpolation;
- to render one frame of the restored Weather;
- to perform teardown;

without stronger evidence.

The strong statement is:

**Broad bootstrap performs a restore-aware full environment application followed immediately by a baseline slot-1 full environment application, and the first pass is observably non-idempotent because it changes transition state and advances shared procedural-render random phase even though its direct final environment values are overwritten.**

---

# 10. Separate this pseudo-random stream from gameplay RNG

This shared recurrence is not the Weather decision RNG.

Weather transition decision:

`0025ACA0`
→ gameplay/native MT19937
→ committed Weather Slot.

Presentation backend orientation:

`0040AAD0`
→ `003D8E50`
→ shared bit-feedback procedural-random float stream.

They are distinct native RNG domains.

For XIIOnline:

## Synchronize / make authoritative
- committed logical Weather Slot;
- stable world/map/weather revision.

## Do not treat as shared gameplay truth
- `01EF93E8` procedural-render random state;
- `022D9138`;
- Presentation orientation perturbations;
- per-client renderer basis state.

Normal multiplayer clients should be allowed to regenerate local Presentation randomness unless a later feature explicitly requires deterministic visual/VFX parity.

Synchronizing this Presentation PRNG merely to keep Weather state coherent would be over-networking derived local render state.

---

# 11. Implication for late join / reconnect

A late joiner needs the authoritative logical Weather Slot before native field/environment realization.

It does **not** currently need the authority's shared Presentation pseudo-random recurrence position to reconstruct gameplay/world truth.

Differences in procedural visual random phase are a separate presentation-determinism question.

This matches the broader XIIOnline architecture:

**shared world truth**
→ native receiver realization
→ receiver-local derived presentation.

---

# 12. Effect on current GN closure

No new GM160 residual row is credited by this addendum.

The discovery strengthens surrounding complete-native understanding but does not alter the certified ledger.

Current strong GN unresolved rows remain:

### `00313A00`
`InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

### `002F7380`
`Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

Applied rows: **0**

Certified GM160 remains:

- **38,001 explicit**
- **160 unresolved**
- **99.58072%**
- **overlap 0**

