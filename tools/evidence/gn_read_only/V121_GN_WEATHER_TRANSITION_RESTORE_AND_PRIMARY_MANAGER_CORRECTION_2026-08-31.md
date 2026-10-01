# V121 GN — WEATHER TRANSITION RESTORE + PRIMARY ACTORMANAGER CORRECTION — 2026-08-31

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Secondary use:** XIIOnline persistent-world weather / transition native-seam research  
**Intended physical parent:** GM160 recovery-transfer GZF contained in the uploaded handoff ZIP  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. Purpose and supersession

This document corrects and narrows prior weather notes, especially:

- `V121_GN_READ_ONLY_WEATHER_SLOT_TRIGGER_ADDENDUM_2026-08-31.md`
- `V121_GN_WEATHER_PROBABILITY_NATIVE_APPLY_CORRECTION_2026-08-31.md`
- `V121_GN_WEATHER_RUNTIME_VS_FIELD_INIT_RESOURCE_SPLIT_2026-08-31.md`

The prior identification of persistent payload byte `+0x1061` as a narrowly weather-owned
“preserve Weather Slot on next apply” latch is **superseded**.

Exact historical GFZ evidence proves that byte participates in a broader **world-transition initialization/restore policy**. Weather application consumes that policy, but does not own it.

This file also records two new complete-body conclusions:

1. native Weather Slot rolling is tied to the **primary ActorManager field-runtime initialization transaction**, not a free-running weather timer and not one roll per actor;
2. broad bootstrap performs a deliberate **two-pass `0026D910(1)` environment application**, where a restore-aware first pass can materialize the prior Weather Slot before a baseline slot-1 second pass.

The exact designer-facing reason for the first bootstrap pass remains unresolved and is deliberately not guessed.

No GM160 mutation is claimed.

Persistence-certified GM160 remains:

- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

---

# 1. Canonical identity of persistent payload `+0x1061`

Historical V31/V40 Function Evidence already reconstructs:

## `00268320`
**Canonical name:**  
`WorldPersistence_ResetBanksAndMarkInitializationState`

**Exact body size:** **88 bytes**

**Exact body SHA-256:**  
`b209df734281e24b61e364f1e5cf6e6f26504132a3db0dc8cdf84707b6ad0bef`

Canonical semantic record:

> Clears transition scratch bank; conditionally clears group-persistent bank based on native global mode state; sets world transition `bInitializationRestoreState` when the controlling mode is zero.

The exact body:

1. checks global runtime/transition mode;
2. conditionally clears the 0x200-byte group-persistent bank;
3. always clears the 0x200-byte transition scratch bank;
4. when the controlling mode is zero:
   - obtains the SaveImage persistent payload;
   - writes `payload+0x1061 = 1`.

This is authoritative evidence that:

**`payload+0x1061` = world-transition `bInitializationRestoreState`**

at the level needed for current reverse engineering.

It is not a Weather-owned variable.

---

# 2. `00268320` has three native transition/reset callers

Canonical V40 Function Evidence records **three direct callers**:

- `00280140` — callsite `002801FF`
- `0036FCC0` — callsite `0036FD17`
- `00394130` — callsite `00394257`

These callers are not all one Weather subsystem.

Observed contexts include:

### `00280140`
A native transition-state path:
- clears/updates transition object flags;
- calls `00268320`;
- evaluates another runtime transition predicate;
- in one branch explicitly clears the initialization-restore byte again;
- continues native transition services.

### `0036FCC0`
A broad sequential reset transaction:
- dispatches multiple unrelated reset/rebind services;
- calls `00268320`;
- continues into additional transition/runtime resets.

### `00394130`
A separate state/materialization path:
- copies a bounded state payload;
- calls `00268320`;
- continues transition/runtime reconciliation.

Therefore the state belongs to **world initialization/restore policy**, not to Weather alone.

---

# 3. `0026D8F0` writes the same broader restore state

## `0026D8F0`

**Complete body:** **21 bytes**

**Exact body SHA-256:**  
`499500bffe0d777a7af19365b59aa692f72c2587bf4fbe5ca71f59b7ccf7c8ae`

Mechanically:

1. obtain SaveImage persistent payload;
2. write `payload+0x1061 = 1`;
3. return.

Authored ScriptVM `setweatherslot(int)` invokes this helper immediately after lower native Weather Slot application.

Earlier working name:

`WorldField_SetPreserveCurrentWeatherSlotOnNextApply`

is now too narrow.

Stronger conservative working name:

**`WorldPersistence_MarkInitializationRestoreState`**

or:

**`WorldTransition_MarkInitializationRestoreState`**

until exact canonical naming is replayed/audited.

The effect inside `0026D910` is indeed to preserve the current Weather Slot for one restore-aware pass, but that does not make the flag itself Weather-owned.

---

# 4. How `0026D910` consumes world initialization/restore state

## `0026D910`

Canonical owner: **WorldAreaField**

Complete body:
- **418 bytes**
- SHA-256:
  `1703f5dce9c22c84928f9e45874590c6080de584cb58296018a9138c7a13b4d2`

Strong current semantic:

**`WorldField_ApplyWeatherSlotAndDerivedEnvironmentState`**

The Weather Slot input is in the authored 1..3 domain.

Relevant exact behavior:

1. use positive debug Weather Slot override when active;
2. convert/clamp requested slot into the native three-slot domain;
3. obtain persistent payload;
4. inspect `payload+0x1061 = bInitializationRestoreState`;
5. when restore state is clear:
   - commit the requested zero-based slot into `payload+0x1060`;
6. when restore state is set:
   - **preserve the already persisted `payload+0x1060` Weather Slot instead of replacing it**;
7. materialize the selected Weather Slot's authored environment/MapRef state;
8. clear `bInitializationRestoreState`;
9. continue the native WorldAreaField→Presentation refresh.

Thus Weather consumes a broader transition policy as:

**restore-aware environment materialization**

rather than owning a private weather latch.

---

# 5. Durable Weather Slot and transition state must remain distinct

Current strongest state split:

## Durable logical Weather state
`payload+0x1060`

- zero-based Weather Slot `0..2`
- queried to the authored/runtime domain as Weather Slot `1..3`
- read by native `00265920`
- changed by native Weather Slot application.

## Broader world transition/restore state
`payload+0x1061`

- `bInitializationRestoreState`
- set by world persistence/reset paths;
- consumed/cleared by Weather/environment application;
- can preserve the previously committed Weather Slot during a restore-aware pass;
- not itself the Weather Slot;
- not proven to be durable multiplayer Weather identity.

For XIIOnline world snapshots, do not elevate `+0x1061` into a permanent Weather field merely because Weather reads it.

---

# 6. Exact Weather roll owner remains `0025ACA0`

## `0025ACA0`

Canonical owner: **WorldAreaField**

Complete body:
- **107 bytes**
- SHA-256:
  `1b3c8438f6d17865bce2ef73931846e5e684d188879e680eec1de93f74fdc464`

Mechanism remains:

1. query current Weather Slot;
2. read authored EBP/script `weatherProbability`;
3. probability `0`:
   - select another eligible slot;
4. probability `>=100`:
   - retain current slot;
5. probability `1..99`:
   - consume native MT19937;
   - scale to 0..99;
   - retain when `roll < probability`;
   - otherwise select another eligible slot;
6. tail-enter `0026D910(finalSlot)`.

This is the native Weather transition decision.

What changed is our understanding of **when that decision is invoked**.

---

# 7. Native Weather roll occurs in primary ActorManager field-runtime initialization

## `002620E0`

Complete body:
- **231 bytes**
- SHA-256:
  `7605a77072bf9d04cf0330b8b662aa627d791dfa16dde5dd68f6d304127f182f`

Exact entry gates:

1. require `managerRecord+0x28 == 0`;
2. test initialization/status bit:
   `managerRecord+0x10 & 0x04`;
3. if the bit is already set:
   - skip the core initialization transaction;
4. otherwise:
   - execute the Weather roll/apply through `0025ACA0`;
   - publish resulting Weather Slot into field/resource channels;
   - publish the slot into additional environment state;
   - run field-resource/Movement initialization;
   - set `managerRecord+0x10 |= 0x04`.

Thus the Weather core is a **one-shot initialization transaction per qualifying manager-record lifecycle**.

---

# 8. `managerRecord+0x28 == 0` means primary ActorManager index 0

Broad Actor/Core bootstrap initializes a bounded ActorManager record bank.

Exact initialization pattern:

- each record stride: **0x288 bytes**;
- record is cleared;
- loop index `edi` is written into record field `+0x28`;
- initialization iterates the manager records.

Therefore:

`managerRecord+0x28`

is the **ActorManager index**.

`002620E0` requires:

`managerRecord+0x28 == 0`

before running its Weather/resource initialization core.

This proves:

**native Weather Slot transition rolling occurs only in the primary ActorManager (index 0) field-runtime initialization transaction.**

It does **not** roll:
- once per actor;
- once per arbitrary ActorManager;
- continuously every frame;
- from a free-running Weather timer in this path.

---

# 9. Canonical caller context

`002620E0` is called from canonical:

## `0025D9E0`
`ActorManager_RunFieldRuntimePass`

The two observed callsites are inside manager/runtime readiness and initialization branches.

The function is part of the ActorManager field-runtime lifecycle, while the Weather decision itself remains WorldAreaField-owned.

This is another cross-layer boundary where caller category must not transfer PrimaryOwner.

---

# 10. Weather transition timing consequence

The strongest current static model is:

field/runtime activation reaches the primary ActorManager initialization boundary  
→ initialization bit is not yet set  
→ `002620E0` runs  
→ native EBP/script Weather transition decision occurs once  
→ committed Weather Slot is published into dependent field/resource state  
→ initialization bit is set  
→ subsequent passes skip the Weather/resource initialization core until that manager lifecycle is reset/recreated.

This is very different from a generic “Weather periodically rerolls over time” model.

No separate free-running persistent Weather timer has been established in this state family.

---

# 11. Field initialization vs runtime scripted Weather remains split

## Field initialization

`002620E0`
→ `0025ACA0`
→ `0026D910`
→ publish committed Weather Slot
→ field/environment channels
→ WorldAreaField→Movement field-resource bridge
→ Movement weather/resource-bank reconfiguration
→ dirty dispatch
→ `002F7380`
→ local LegacyPS2GS texture/mip table rebuild.

## Authored runtime `setweatherslot`

ScriptVM wrapper:
`003565C0`

delegates to:

`0026D910(slot)`
→ `0026D8F0()`
→ return.

There is no direct immediate call from the authored runtime setter to:
- `00379290`;
- `0026E8D0`;
- `0026E290`;
- `002F7380`.

Therefore:

**runtime Weather changes and field-resource initialization are separate native transactions.**

Do not force the field-init Movement/GS rebuild after every synchronized runtime Weather change.

---

# 12. Broad bootstrap deliberately calls `0026D910(1)` twice

A broad Core/Actor/bootstrap initializer performs:

```text
mov ebp, 1
...
mov ecx, ebp
call 0026D910
mov ecx, ebp
call 0026D910
```

There is no intervening semantic call and no argument difference.

The two calls are genuine.

This is important because `0026D910` is **not** side-effect free.

---

# 13. Restore-aware two-pass bootstrap behavior

Suppose before bootstrap:

- `bInitializationRestoreState == 1`;
- saved Weather Slot at `payload+0x1060` is not slot 1.

Then:

## First `0026D910(1)`

Because restore state is set:

1. requested slot 1 is **not** committed;
2. existing saved Weather Slot is preserved;
3. the saved slot's environment state is materialized;
4. slot-specific runtime parameters are published;
5. Presentation/environment refresh runs;
6. restore state is cleared.

## Second `0026D910(1)`

Now restore state is clear:

1. requested slot 1 is committed;
2. slot-1 environment state is materialized;
3. Presentation/environment refresh runs again.

Therefore the first call can have real, distinct effects even though the final persistent slot after the second call is 1.

This is a deliberate **two-pass environment/bootstrap transaction**.

---

# 14. First-pass environment publication is substantive

The first Weather/environment apply calls:

## `00180620(slotIndex)`

which obtains an environment/Presentation singleton and forwards to:

## `001A7E40(singleton, slotIndex)`

`001A7E40` selects a slot-specific parameter bank and copies values into the live runtime object, including:

- one dword lane from a per-slot table into runtime `+0x144`;
- another dword lane into `+0x140`;
- a three-float vector from a slot-indexed bank;
- three additional slot-indexed scalar lanes into runtime `+0x870/+0x874/+0x878`;
- conditional downstream vector application.

Thus a restore-aware first `0026D910` pass materially publishes the **previous slot's live environment/Presentation parameter bank** before the second baseline pass.

It is not a redundant store to `payload+0x1060`.

---

# 15. Exact purpose of the duplicate first pass remains unresolved

Current evidence proves:

- the two calls are identical at the callsite;
- restore state can make their effective Weather Slots differ;
- the first pass can publish the restored slot's live environment parameters;
- the first pass clears restore state;
- the second pass then applies baseline slot 1.

Current evidence does **not** yet prove the designer-facing reason.

Do not claim, without stronger evidence, that the first pass is specifically:
- teardown;
- destruction;
- interpolation history seeding;
- fade-source setup;
- backend swap preparation;
- old-environment cleanup;
- a save-load bug workaround.

Conservative statement:

**broad bootstrap performs a deliberate restore-aware environment materialization pass followed by a baseline slot-1 environment application.**

The exact higher-level purpose remains an open proof obligation.

---

# 16. Correction to earlier XIIOnline Weather-state model

Previous wording risked treating `payload+0x1061` as a Weather-specific multiplayer field.

That is withdrawn.

## Durable authoritative Weather truth

Current best candidate remains:

**committed Weather Slot 1..3**

with stable map/world/revision fencing.

## World-transition restore policy

`bInitializationRestoreState` is a broader local/native transition state.

It may affect how Weather/environment application proceeds during restoration or bootstrap.

It should not automatically be serialized as a permanent Weather field.

If XIIOnline must reproduce an in-flight world-transition restore transaction, synchronize the higher semantic transition/lifecycle state rather than treating the raw byte as Weather ownership.

---

# 17. Refined XIIOnline Weather architecture

## Authority Weather generation

Allow the authoritative native instance to reach the normal:

primary ActorManager field-runtime initialization  
→ `002620E0`  
→ `0025ACA0`

Weather decision.

This preserves:
- EBP/script `weatherProbability`;
- native MT19937;
- native alternative-slot eligibility;
- modded authored Weather configuration.

Observe the resulting committed Weather Slot.

## Network world state

Synchronize:
- world/map identity;
- Weather Slot;
- weather/world revision as needed by protocol.

Do not synchronize:
- local MT19937 draw as the authoritative outcome;
- Movement dirty state;
- LegacyPS2GS allocations;
- raw Presentation parameter banks.

## Receiver

For an already-loaded runtime Weather change:
- use the highest proven safe non-VM WorldAreaField apply transition;
- currently `0026D910(slot)` is the strongest lower candidate;
- allow native WorldAreaField/Presentation consequences;
- do not force field-init Movement resource rebuild.

For field load / late join:
- authoritative Weather Slot must be known before the receiver reaches the primary field-runtime/resource initialization boundary;
- allow native field-resource initialization to consume it and build receiver-local Movement/Presentation/LegacyPS2GS state.

## Restore/reconnect

Do not blindly reproduce raw `bInitializationRestoreState`.

Determine whether the receiver is actually performing the corresponding native world-transition restore transaction.

Prefer reproducing the higher native transition that causes the engine to manage this state itself.

---

# 18. Spawn / Rare Game ordering remains

Weather is an input to native conditional spawn eligibility.

For authoritative/shared world behavior:

authoritative Weather Slot settles  
→ receiver/world Weather revision settles  
→ native conditional spawn eligibility evaluates  
→ spawn-controller/member realization proceeds  
→ existing XIIOnline reconciliation synchronizes the resulting authoritative world population.

This preserves native rare/conditional eligibility instead of replacing it.

---

# 19. Effect on unresolved GN proposal `002F7380`

No rename.

Strong read-only proposal remains:

`Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

This correction makes its upstream context more precise:

- Weather Slot participates in **field-resource initialization** that selects a Movement resource bank;
- Movement dirty dispatch then reaches `002F7380`;
- runtime Weather Slot application alone does not directly force `002F7380`.

Weather is an upstream resource-selection input, not the GN function's own semantic domain.

---

# 20. GFZ state remains unchanged

Applied GN rows: **0**

Strong current GM160 unresolved proposals remain:

1. `00313A00`  
   `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

2. `002F7380`  
   `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

Persistence-certified GM160 remains:

- **38,001 explicit**
- **160 unresolved**
- **99.58072%**
- **overlap 0**

Prospective two-row arithmetic, if later exact-current GZF mutation and full persistence certification pass:

- **38,003 explicit**
- **158 unresolved**
- **99.58596%**

That prospective state is not a checkpoint.

---

# 21. Remaining proof debt

1. Explain the exact higher-level purpose of broad bootstrap's two consecutive `0026D910(1)` calls.
2. Determine whether the first restore-aware environment pass seeds interpolation/history, performs a teardown/rebind prerequisite, or serves another native lifecycle purpose.
3. Verify production-safe ABI/thread/state preconditions for receiver-side lower native Weather Slot apply.
4. Search for a higher non-VM WorldAreaField apply transaction that gives more complete runtime coherence than calling `0026D910` directly.
5. Live-test runtime Weather Slot synchronization.
6. Live-test late-join field load with authoritative Weather preinstalled before primary ActorManager initialization.
7. Verify Rare Game/weather-dependent native spawn eligibility ordering in linked sessions.
8. Keep world initialization/restore state separate from durable Weather identity in protocol design.

