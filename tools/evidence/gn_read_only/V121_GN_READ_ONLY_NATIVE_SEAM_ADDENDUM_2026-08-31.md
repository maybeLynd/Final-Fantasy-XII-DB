# V121 GN — READ-ONLY NATIVE-SEAM ADDENDUM — 2026-08-31

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Secondary use:** XIIOnline best-native-seam research  
**Intended mutation parent:** GM160 recovery-transfer GZF  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. Hard fence

This document adds native-transition topology around the two strong current GN read-only proposals:

- `00313A00` — `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`
- `002F7380` — `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

It does **not** mutate the GM160 recovery-transfer GZF.

The physical GM160 recovery-transfer GZF is still not exposed in the execution filesystem, so no exact-current-parent enrichment, GN mutation, project diff, closed-file pack, or fresh-reopen certification is claimed.

Official persistence-certified state remains:

- internal functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

The prospective two-row state remains only prospective:
- explicit **38,003**
- unresolved **158**
- coverage **99.58596%**

Do not report that prospective state as persisted.

---

# 1. Combat/Input policy seam — `00313A00` is downstream derived state

## 1.1 Current GN proposal

`00313A00`

`InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

Complete body:
- **289 bytes**
- SHA-256:
  `c076cfeadbc81442c947e0c749eefbdef7e7c6717297847333a7cbae9289d246`

Prior GN work proves that this function rebuilds row 2 of a 16-row × 32-bit capability/inhibition policy. Its output is consumed by gameplay/input eligibility and translated into native UI-request refusal.

The new question was whether this routine is itself the best native transition to invoke when selected-BattleUnit state changes.

It is **not**.

---

# 2. Higher native transaction — `00313DB0`

## Exact executable body

`00313DB0`

Executable body before padding:
- **356 bytes**
- SHA-256:
  `62e92b608e213e94e14d5f637e9c94e0bff2b5e054107fe93675c01d98cb37f9`

Canonical V120 already owns this function as **CombatAction** and independently identifies it as the owner of global `02089350`, the current-selected-BattleUnit state.

## 2.1 Selection path

When no current unit is already selected, `00313DB0`:

1. scans the native candidate source;
2. resolves a candidate through `0031B7E0`;
3. mutates candidate BattleUnit flags;
4. checks the candidate's attached state;
5. applies the existing field eligibility predicate when required;
6. publishes the accepted BattleUnit pointer to `02089350`;
7. performs the existing action/selection transaction;
8. invokes supporting command/action services;
9. calls `002DEE70`;
10. **calls `00313A00` before returning**.

The exact call occurs at:

`00313EA7 -> 00313A00`

Thus native selected-BattleUnit installation already performs capability/UI-request policy reconciliation.

## 2.2 Clear path

When the selected unit is no longer valid or must be released, the same function:

1. validates the current unit and associated field state;
2. clears global `02089350`;
3. invokes the native clear/cancel transaction through `00225CD0`;
4. **tail-jumps directly to `00313A00`**.

Exact tail:

`00313F13 -> 00313A00`

Thus native selected-BattleUnit clearing also performs the same derived policy reconciliation.

## 2.3 Higher-level frame transaction

`00313DB0` itself is called by the high-level field/battle update body at:

`00234538 -> 00313DB0`

That update then continues through other battle/field subsystems.

Separately, another field-frame path calls `00313A00` directly at:

`00234624 -> 00313A00`

This direct policy refresh occurs after field/runtime predicates are updated, showing that `00313A00` is also the native derived-state refresh for policy inputs that can change independently of selected-BattleUnit selection.

---

# 3. Best-native-seam consequence for XIIOnline

For a future XIIOnline feature that needs to reproduce a **native selected-BattleUnit transition**:

### Prefer
the higher CombatAction transaction that owns/selects/clears `02089350` — currently anchored by `00313DB0` — when its complete ABI/preconditions are appropriate.

### Do not prefer
- directly writing `02089350`;
- manually setting/clearing the row-2 policy bits;
- calling `00313A00` merely to compensate for a direct selected-BattleUnit write.

Reason:

`00313DB0`
→ owns selected-BattleUnit transition
→ performs existing action/selection side effects
→ automatically invokes `00313A00`
→ policy/UI eligibility converges through native downstream logic.

Calling `00313A00` after a direct state write would reproduce only the downstream derived policy, not the complete native CombatAction transaction.

### Separate valid use of `00313A00`

If a field/runtime policy input changes through another native owner **without** selected-BattleUnit selection/clear, `00313A00` is the observed native policy reconciliation stage.

That does not mean XIIOnline should invoke it automatically. Prefer the higher native owner transition that changes the relevant upstream field/runtime state when one is known.

This distinction follows the project's “best native seam wins” rule.

---

# 4. Legacy PS2 GS texture-table seam — `002F7380` is also downstream derived state

## Current GN proposal

`002F7380`

`Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

Complete body:
- **723 bytes**
- SHA-256:
  `15594f6181100f7fa10ac8a770566d60b963e47c93176fd7d7f33152b3ac8583`

Prior GN work proves this routine:
- calculates full texture mip-chain GS local-memory footprints;
- uses native GS PSM page geometry;
- applies the retained 4 MiB / 8 KiB GS local-memory model;
- counts active texture references;
- admits multiply referenced texture mip chains under the remaining budget;
- assigns compact slots;
- allocates/zeros 40-byte slot records.

The new question was whether this routine is the correct native seam when the active Movement/resource selector changes.

It is **not**.

---

# 5. Movement resource dirty dispatcher — `0026E290`

## Exact executable body

`0026E290`

Executable body before padding:
- **97 bytes**
- SHA-256:
  `aac93b37c874c23a7b634ae96bab718d3d89d826cc60c4c76bb258b66b023793`

Canonical V120 independently owns this as Movement.

Exact mechanism:

1. load the current Movement/navigation resource object from global `0209A670`;
2. require a non-null current object;
3. require object active state `+0x120 != 0`;
4. inspect Movement dirty flag `0209A708`;
5. when dirty:
   - load the Presentation-side dataset/input pointer from the Movement resource family;
   - call `002F7380(currentResource, dataset)`;
   - clear `0209A708`;
6. invoke the current resource's ordinary callback at `+0x130` when present.

Therefore `002F7380` is explicitly the **dirty-dependent derived Presentation rebuild inside the normal Movement resource dispatch transaction**.

It is not the authoritative Movement state transition.

---

# 6. Higher Movement reconfiguration — `0026E8D0`

## Exact executable body

`0026E8D0`

Executable body before padding:
- **134 bytes**
- SHA-256:
  `68aea8568f166938bb4fcafe30d29ce45f7997b71402fb3ac2ba35d224f95ebc`

Canonical V120 independently owns this as Movement.

Exact mechanics include:

1. store incoming selector/mode into the Movement resource state;
2. set dirty flag `0209A708 = 1`;
3. rebuild the current Movement/navigation resource state through the existing `003ED***` resource family;
4. iterate/reinitialize three 0x30-byte resource descriptors;
5. finalize the resource state;
6. update the related downstream mode through the existing native tail transition.

The important property is not the final authored name of the selector.

The important property is:

**`0026E8D0` changes the upstream Movement resource configuration and deliberately marks the dependent Presentation table dirty.**

The normal dispatcher later observes that dirty state and calls `002F7380`.

---

# 7. Native selector source

Exact executable body `00265920` resolves the selector:

1. query runtime override through `0017D490`;
2. if the override is positive, return/use it;
3. otherwise obtain the current game/save runtime structure through `002EF2B0`;
4. read signed byte `+0x1060`;
5. add one;
6. return the resulting selector.

The selector is therefore derived from existing runtime/persisted state, not invented by the Presentation table builder.

At least two native higher-level paths use this exact pattern:

### `00379290` path
- obtains the current selector through `00265920`;
- tail-calls `0026E8D0`.

### `00379630` path
- clears/rebuilds a surrounding graphics/resource state family;
- obtains the selector through `00265920`;
- calls `0026E8D0`;
- continues materializing related graphics/resource records.

This confirms that `0026E8D0` is the engine's normal selector-driven reconfiguration stage.

---

# 8. Best-native-seam consequence for the GS table

For any future work that needs to change the active upstream resource configuration:

### Prefer
the existing native upstream Movement/resource reconfiguration path — anchored here by `0026E8D0` when its ABI/preconditions match.

That path:
- publishes the selector;
- sets dirty state;
- rebuilds associated Movement resource structures;
- lets `0026E290` dispatch normally;
- lets `002F7380` rebuild the dependent LegacyPS2GS texture/mip table automatically.

### Do not prefer
- direct writes to `0209A6E8`;
- direct dirty-flag writes without the accompanying resource transition;
- direct calls to `002F7380` as a substitute for upstream resource configuration.

A direct `002F7380` call would rebuild only the derived GS local-memory slot table and could leave the Movement resource family out of step.

Again, this is the project's “best native seam wins” rule in concrete executable form.

---

# 9. Architectural result

The two protected GM160 holds now reveal the same engine design pattern in two unrelated subsystems:

## Combat/Input policy

authoritative/owned transition  
`00313DB0` selected-BattleUnit transaction  
→ derived capability reconciliation  
`00313A00`  
→ InputGameplay/UI consumers

## Movement/Legacy GS resource state

authoritative/owned transition  
`0026E8D0` Movement resource reconfiguration  
→ dirty state  
`0026E290` dispatcher  
→ derived Presentation rebuild  
`002F7380`  
→ LegacyPS2GS texture/mip slot table

This is important for XIIOnline architecture:

**prefer synchronizing or invoking the upstream native owner transition and allow downstream derived state to regenerate naturally.**

That reduces:
- direct writes;
- duplicated derived-state forwarding;
- engine-fighting periodic corrections;
- inconsistent downstream caches/policy tables.

It also provides a concrete static example of the project's native-coherence rule.

---

# 10. GFZ decision remains unchanged

These topology findings strengthen the two GN semantic proposals but do not authorize mutation without the physical GM160 GZF.

Strong proposed unresolved rows remain:

1. `00313A00`  
   `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

2. `002F7380`  
   `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

Applied rows: **0**

Official persisted GM160 ledger:
- **38,001 explicit**
- **160 unresolved**
- **99.58072%**
- **overlap 0**

Only after fresh-importing the exact GM160 recovery-transfer GZF and reproducing its certified state may these rows be exact-current enriched, mutated, diffed, packed with `PACK_PASS`, and fresh-reopened.

