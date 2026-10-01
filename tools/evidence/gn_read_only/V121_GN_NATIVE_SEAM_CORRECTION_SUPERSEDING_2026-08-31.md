# V121 GN — NATIVE-SEAM CORRECTION — SUPERSEDING ADDENDUM — 2026-08-31

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Secondary use:** XIIOnline best-native-seam research  
**Supersedes on the points identified below:** `V121_GN_READ_ONLY_NATIVE_SEAM_ADDENDUM_2026-08-31.md`  
**Intended physical mutation parent:** GM160 recovery-transfer GZF contained in the uploaded handoff ZIP  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. Why this correction exists

The earlier native-seam addendum correctly established that unresolved `00313A00` is downstream derived capability/UI-request policy state.

However, it then overreached by treating canonical CombatAction owner `00313DB0` as though it were a suitable higher native API for reproducing an arbitrary selected-BattleUnit transition.

Further exact-body and persisted CombatAction evidence disproves that implication.

This correction is authoritative over the earlier addendum wherever the two conflict.

It also corrects the earlier exact-body size/hash recorded for `00313DB0`.

No GM160 mutation is claimed here.

Official persistence-certified GM160 state remains:

- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

The two strong GN semantic proposals themselves remain unchanged:
- `00313A00` — `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`
- `002F7380` — `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

---

# 1. Exact correction — `00313DB0` body identity

The earlier addendum recorded an incomplete body extent.

Canonical V120 exact-binary reconstruction establishes the full Ghidra function identity as:

## `00313DB0`
- Ghidra body size: **360 bytes**
- one contiguous range
- full-body SHA-256:  
  `deab0e5353428cc11d9523a47579c3eb82fed2ee1f065ad864449a8f56e22461`
- full body occurs uniquely in the authorized executable
- canonical V120 PrimaryOwner: **CombatAction**

This supersedes the earlier incorrect:
- 356-byte body size
- SHA `62e92b...`

The earlier short extent came from a mechanically truncated executable-boundary pass and must not be used as semantic or exact-current function identity.

---

# 2. `00313DB0` is zero-argument — not an arbitrary BattleUnit-selection API

Complete executable analysis shows `00313DB0` receives **no BattleUnit argument**.

It does not expose an ABI of the form:

`select_this_specific_BattleUnit(BattleUnit*)`

Instead, it consumes an engine-maintained bounded ring of packed BattleUnit IDs.

The consumed ring uses:
- read index at `022BEDA0`
- write index at `022BEDA1`
- data bank beginning at `022BEDA4`
- capacity: **64 entries**

`00313DB0`:
1. checks whether read and write indices differ;
2. consumes the next queued packed BattleUnit ID;
3. advances the read index modulo 64;
4. resolves that local ID through the existing native BattleUnit resolver;
5. applies native unit/current-state changes;
6. publishes the resolved BattleUnit as current state at `02089350`;
7. performs downstream game/audio/state services;
8. calls `00313A00`, thereby reconciling InputGameplay/UI capability policy.

Its clear/release path:
- clears `02089350`;
- performs the native clear transaction;
- reaches `00313A00` again.

Therefore:

**`00313DB0` is a consumer of a pre-existing native queue, not an arbitrary remote selection entry point.**

---

# 3. Do not confuse this ring with `00313CD0`

There are two different bounded mechanisms nearby.

## `00313CD0`
Canonical name:

`BattleUnit_ProcessPendingActionSelectionQueue`

Exact identity:
- **220 bytes**
- SHA-256:
  `adf43795d7d2b8e33dbf407b5470ef61f3ce6220955022efbbc34e933ed8e331`

Persisted evidence states that it:
- drains a bounded pending BattleUnit action-selection queue of up to eight entries;
- clears the queued bit;
- validates BattleUnit state;
- calls the native select/commit-next-action owner;
- is **not** the singular `BattleUnit_CommitAction` authority boundary itself.

This is a different queue and a different transaction from the 64-entry ring consumed by `00313DB0`.

Do not merge them merely because the functions are adjacent.

---

# 4. Source of the 64-entry ring is the standard committed-action presentation lifecycle

The single observed producer of the `022BEDA4` ring occurs at `00304E5C`, inside:

## `00304850`
`BattleUnit_AdvanceStandardActionState`

Exact canonical identity:
- body size: **2,034 bytes**
- SHA-256:
  `48ca39ef20c1bbc3aa4c9edb1c47733de19056fdadbb7bdbbbf90c905b2bd680`

Persisted V40 reconstruction proves this is a **13-phase standard-action pipeline**.

Its phases include:
- effective range computation;
- charge/progress;
- combat navigation/approach;
- presentation-state acquisition/waiting;
- target-set preview/materialization;
- resource preparation/consumption;
- final waiting/cleanup.

This function is **post-commit action execution**.

It is not the native command/AI intent boundary.

Within its later presentation-state handling, the ring producer:
1. obtains the BattleUnit's presentation-slot index;
2. calls `0030CA80`;
3. only when the presentation-slot readiness output is asserted:
   - obtains the ring write index;
   - writes the BattleUnit's packed ID to the 64-entry ring;
   - advances the write index modulo 64;
   - marks the associated BattleUnit flag.

This establishes the queue as a **presentation-ready/action-lifecycle notification ring**, not a command-intent queue.

---

# 5. Exact presentation-slot family

Canonical V120 CombatAction reconstruction independently identifies the relevant native family:

- `0030C970` — `BattleAction_ReleasePresentationSlot`
- `0030CA80` — `BattleAction_CheckPresentationSlotReady`
- `0030CF40` — `BattleAction_ResetPresentationSlotPool`
- `0030CFB0` — `BattleAction_AcquirePresentationSlot`
- `0030D070` — `BattleAction_AllocatePresentationSlot`

The slot runtime records are distinct from BattleUnit command intent.

The readiness check is reached during the committed standard-action state machine's presentation phases.

Thus the strongest conservative name for the 64-entry queue is:

**BattleAction presentation-slot-ready BattleUnit notification ring**

or equivalently:

**presentation-ready/action-lifecycle BattleUnit ID ring**

Do not name it:
- target-selection queue;
- player command queue;
- remote action queue;
- network selection queue.

---

# 6. Revised interpretation of `02089350`

Canonical V120 remains authoritative that:

`02089350`

is **CombatAction current-selected-BattleUnit state**, with:
- `00313DB0` as its CombatAction writer/owner;
- WorldAreaField reset boundary;
- Movement as a read-only consumer in one locomotion/presentation decision.

The new finding does **not** invalidate that ownership.

It refines **how the state is naturally populated**:

a BattleUnit reaches the appropriate committed-action/presentation readiness state  
→ its packed ID enters the 64-entry native notification ring  
→ `00313DB0` consumes that native notification  
→ `02089350` is published  
→ `00313A00` recomputes capability/UI-request inhibition.

So `02089350` is real current-selected-BattleUnit state, but the native producer path is not an arbitrary pointer-taking selection call.

---

# 7. Revised XIIOnline best-native-seam decision

## Previous incorrect implication

The superseded addendum suggested that XIIOnline should prefer `00313DB0` when reproducing a selected-BattleUnit transition.

That is **withdrawn**.

`00313DB0` has no arbitrary-BattleUnit parameter and relies on a prior native committed-action/presentation-ready queue transaction.

Calling it manually would merely consume whatever local queue state happens to exist.

It would not express a stable remote command intent.

## Correct established combat replay seam

Canonical CombatAction reconstruction already states:

**the strongest native replay seam is command/action intent with stable-network-identity translation, followed by singular native action authority.**

The relevant native command family is:

### `00311CF0`
`BattleUnit_IssueCommand`

- exact body: **283 bytes**
- exact canonical SHA-256:
  `774d9502ee5880ce033f0328073eeb6d55772372ace0ad0ca1061ee1add0bc81`

Sibling wrappers:

### `00311CD0`
`BattleUnit_IssueCommandByFocusHandles`
- **26 bytes**
- SHA-256:
  `0ee477c34504c2b35937dc390d0c51847504e06142b3af32e7e505a6eaeee22b`

### `00311B20`
`BattleUnit_IssueCommandByFocusHandlesWithOptionalPartyFanout`
- **426 bytes**
- SHA-256:
  `8ef0373e570480381e12d8c02ca8c9df32ef4e33563b3f8aaca6ba23dbb2ad67`

These command seams use receiver-local focus/BattleStats identities.

Therefore XIIOnline must:

1. carry stable network actor/target identity;
2. resolve that identity to the receiving client's current native BattleUnit/focus/BattleStats representation;
3. enter the appropriate native command-intent seam;
4. allow native target-set, reservation, action commit, timeline, presentation and downstream policy state to proceed naturally.

Raw local focus handles, BattleStats slots and BattleUnit pointers are not valid wire identities.

---

# 8. Relationship to `BattleUnit_CommitAction`

`0030F760`

`BattleUnit_CommitAction`

remains a genuine lower action-commit owner.

It installs:
- order/action context at `BattleUnit+0x708`;
- target focus at `+0x710`;
- action ID at `+0x714`;
- action phase reset at `+0x6B4`;
- additional context/queue/reservation/enmity state depending on action family.

But current evidence does **not** establish `BattleUnit_CommitAction` as one universal human/Gambit/AI/guest/script command funnel.

The command-intent family above remains the stronger known replay boundary for ordinary player-command replication where its ABI applies.

Do not replace that with:
- direct `+0x708/+0x710/+0x714` writes;
- manual ring insertion;
- direct writes to `02089350`;
- forced invocation of `00313DB0`;
- direct `00313A00` calls to repair consequences of lower-level writes.

---

# 9. Correct role of `00313DB0` for XIIOnline

The safe current classification is:

**OBSERVE / ALLOW NATIVE DOWNSTREAM EXECUTION**

rather than:

**INVOKE AS REMOTE COMMAND**

`00313DB0` is useful for understanding and observing:
- which BattleUnit has reached the relevant presentation-ready/current-unit transaction;
- when `02089350` changes;
- why InputGameplay/UI request eligibility changes;
- how action presentation lifecycle feeds current-unit policy.

It may also be a useful telemetry seam.

But it is not currently justified as a receiver-side arbitrary command/selection replay call.

---

# 10. Correct role of unresolved `00313A00`

The GN semantic decision remains intact:

## `00313A00`
`InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

It is a derived-state reconciler.

For the native path discussed here:

committed action  
→ standard-action presentation lifecycle  
→ presentation-slot-ready notification ring  
→ `00313DB0` current-unit publication  
→ `00313A00` capability/UI-request reconciliation.

Therefore XIIOnline should normally let `00313A00` occur as a downstream consequence of native upstream state.

Do not send its individual mask bits over the network as primary game state.

---

# 11. Corrected architectural picture

## Command/action authority

stable network command intent  
→ resolve stable actor/target identity into receiver-local native identities  
→ `BattleUnit_IssueCommand` family  
→ native target selection / availability / reservation  
→ `BattleUnit_CommitAction` where native flow reaches it  
→ `BattleUnit_AdvanceActionState`

## Standard-action presentation/current-unit side transaction

`BattleUnit_AdvanceStandardActionState`  
→ acquire/wait presentation slot  
→ `BattleAction_CheckPresentationSlotReady`  
→ enqueue packed BattleUnit ID in 64-entry presentation-ready ring  
→ `00313DB0` consumes ring  
→ publishes `02089350` current-selected-BattleUnit  
→ `00313A00` rebuilds InputGameplay/UI capability policy

These are related but **not interchangeable authority seams**.

---

# 12. Effect on GFZ GN proposal

This correction does not weaken the semantic closure of `00313A00`.

It strengthens it by establishing a more exact upstream native event:

`00313A00` is downstream of a CombatAction current-unit publication caused by the action/presentation lifecycle, while also receiving independent WorldAreaField/runtime policy inputs.

Strong GN proposal remains:

`InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

No PrimaryOwner is inherited from CombatAction, UI, Input, or WorldAreaField.

---

# 13. Effect on the LegacyPS2GS GN row

None.

`002F7380` remains:

`Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

The earlier Movement-resource upstream/dirty-state analysis remains valid.

This correction supersedes only the incorrect combat replay-seam implication and the bad `00313DB0` body extent/hash.

---

# 14. Current accounting

Applied GN rows: **0**

Persistence-certified GM160 remains:
- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

Prospective two-row GN arithmetic, if exact-current mutation later passes:
- explicit: **38,003**
- unresolved: **158**
- coverage: **99.58596%**

This is not yet a persisted checkpoint.

---

# 15. Supersession rule

When reading:

`V121_GN_READ_ONLY_NATIVE_SEAM_ADDENDUM_2026-08-31.md`

replace its CombatAction seam conclusion with this document.

Specifically, disregard:
- the old 356-byte / `62e92...` body identity for `00313DB0`;
- the implication that `00313DB0` is a preferred arbitrary selected-BattleUnit replay API;
- any downstream recommendation that treats the 64-entry ring as command intent.

Retain from the older addendum:
- `00313A00` is derived capability/UI policy;
- `002F7380` is downstream derived LegacyPS2GS state;
- the general rule to prefer the highest proven native owner transition rather than direct derived-state writes.

For ordinary combat command replication, the current highest proven practical native seam is the **`BattleUnit_IssueCommand` family with stable-to-local identity translation**, consistent with the sealed CombatAction reconstruction.

