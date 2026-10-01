# V121 GN — READ-ONLY INPUTGAMEPLAY POLICY ADDENDUM — 2026-08-31

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Intended mutation parent:** GM160 recovery-transfer GZF  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. Purpose / hard fencing

This addendum strengthens the GN read-only semantic reconstruction for protected unresolved function:

`00313A00`

It does **not** mutate the GM160 recovery-transfer GZF.

The physical GM160 recovery-transfer GZF is still not exposed in the current execution filesystem. Therefore:
- no exact-current-parent Ghidra enrichment is claimed;
- no comment/tag mutation is claimed;
- no GN checkpoint exists;
- no deterministic post-mutation diff exists;
- no `PACK_PASS` exists for GN;
- no fresh-reopen certification exists for GN.

The official persistence-certified state remains unchanged:

- internal functions: **38,161**
- explicitly accounted: **38,001**
- unresolved: **160**
- explicit coverage: **99.58072%**
- cross-layer overlap: **0**
- certified current residual SHA-256: `fa6f614a463bf9981f32cbd4582e31ba23b04e6b803cfbb0139b209dffda5a1a`

No PrimaryOwner is inferred from callers or input-state ownership.

No PE `.pdata`, `.xdata`, unwind, EH or IP-to-state metadata is used as semantic proof.

---

# 1. Refined proposed row — `00313A00`

## Strongest current read-only CodeDomain proposal

`InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

**Previous conservative proposal:**  
`InputGameplay.FieldBattleOperationInhibitMaskReconciliation`

**Complete body:** 289 bytes  
**Exact authorized-EXE body SHA-256:**  
`c076cfeadbc81442c947e0c749eefbdef7e7c6717297847333a7cbae9289d246`

The new `CapabilityAndUIRequest` wording is justified by the complete aggregate-policy consumer graph and by an exact static policy-bit → UI-request mapping table. It does **not** assign player-facing names to those request IDs.

---

# 2. Central multi-row capability/inhibition policy

The complete `00313A00` body reconciles **row 2** of a central **16-row × 32-bit** policy/inhibition table.

Exact sibling primitives establish direction:

- `002E1C20(row, bit)` — set requested bit in selected row;
- `002E1CA0(row, bit)` — clear requested bit in selected row;
- `002E0FA0()` — OR-reduce all 16 rows into the final effective capability/inhibition mask.

`00313A00` explicitly reconciles row-2 policy bits:

`0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 20`

Most are selected from whether `02089350` is non-null.

Persisted V120 authority independently identifies `02089350` as the **CombatAction current-selected-BattleUnit state** published by `00313DB0`. That establishes an input to the policy decision; it does not transfer CombatAction PrimaryOwner to `00313A00`.

Bit 10 is selected separately from `00377C20`. The exact helper resolves the current indexed field record and returns the high bit of a two-byte field. Canonical V120 places that source helper in **WorldAreaField**. Its authored field-bit name remains unproven.

Bit 1 also depends on `00253B90`, whose exact body is only a null predicate over `01E0C2B8`. No authored meaning is assigned to that global.

The no-selected-BattleUnit path also incorporates shared runtime/gameplay flags and reconciles an additional gate.

This proves a **field/battle contribution to a shared capability policy**, not a local CombatAction state machine.

---

# 3. Aggregate mask is consumed across InputGameplay and UI

Exact executable xref analysis finds **29 direct call sites across 25 functions** to aggregate reader `002E0FA0`.

Observed direct consumers test individual policy bits including:

`0, 4, 5, 6, 9, 10, 11, 18, 21`

Representative mechanically observed use:
- bit 21 gates a high-level gameplay/input path;
- bit 10 repeatedly blocks UI request/transition paths;
- bit 4 participates in actor/field-interaction eligibility;
- bit 5 participates in another gameplay eligibility path;
- bit 18 suppresses a persistent UI-screen transition/toggle path.

Canonical V120 independently reconstructs:

`00253C70` — `InputGameplay_ArbitrateDigitalInputAndModalState`

- body: **1,599 bytes**
- exact body SHA-256: `e6309cd50d266650fbb78a725a5aaaefb69c656a51dffc87c8299f30c15fa093`
- canonical category: **FFXII.Input**

The aggregate policy is therefore not merely a UI state word and not merely a raw input mask. It is a shared **gameplay capability/inhibition policy** consumed by the InputGameplay arbiter and multiple canonical UI owners.

---

# 4. Exact policy-bit → UI-request translation — `00254500`

A second exact body materially sharpens the semantics.

## `00254500`

**Complete body:** 67 bytes  
**Exact code-byte SHA-256:**  
`7b993dc50d7e9d5d075182b2bc3e4693b40cf9d2e27174dc2b16ccc8b07f4dcd`

Mechanically, the function:

1. calls aggregate policy reader `002E0FA0`;
2. iterates the 22 low aggregate policy bits;
3. for each set policy bit, ORs a 32-bit value from static table `01E0C2C0`;
4. returns the resulting derived mask.

Static table:
- address: `01E0C2C0`
- entries: **22 × 32-bit**
- bytes: **88**
- exact SHA-256:  
  `eadec033c5635a6d9375347f46ff568904bd02c1fc465c931bc9f12d714bfd49`

The exact mapping is:

| Aggregate policy bit | Derived inhibited UI request bits |
|---:|---|
| 0 | 2 |
| 1 | 1, 3, 5 |
| 2 | 3 |
| 3 | 2 |
| 4 | — |
| 5 | 5 |
| 6 | 14 |
| 7 | — |
| 8 | 1, 21 |
| 9 | 5, 14 |
| 10 | 3 |
| 11 | — |
| 12 | — |
| 13 | — |
| 14 | — |
| 15 | — |
| 16 | — |
| 17 | — |
| 18 | — |
| 19 | — |
| 20 | — |
| 21 | — |

This table is a strict native translation layer. It proves that some capability-policy bits are also used to suppress specific native UI request IDs.

The zero entries do **not** mean those policy bits have no effect elsewhere. Several are consumed directly outside this UI-request translation path.

---

# 5. Exact UI request router — `00254B50`

## Identity

`00254B50`

**Complete body:** 263 bytes  
**Exact body SHA-256:**  
`9ab5c3f609a8b886a1876813c746ce12907c205f8a446d7060411ad74dfd4d78`

Canonical V120 classifies this function as **FFXII.UI**.

## Exact request/refusal mechanism

The complete body:

1. normalizes the incoming request ID with `requestId = ECX & 0x7FFF`;
2. rebuilds the same derived inhibited-request mask from:
   - `002E0FA0`;
   - policy table `01E0C2C0`;
3. tests the requested bit with native `BT`;
4. if the corresponding request bit is inhibited, returns failure without dispatch;
5. otherwise dispatches request IDs 1..24 through a native switch.

This is therefore a central **UI request router with gameplay-policy refusal**, not merely a generic bit-test helper.

---

# 6. Direct caller closure of the UI request router

Exact executable analysis finds only **three direct CALL sites** to `00254B50`.

Two occur inside canonical Input root:

`00253C70` — `InputGameplay_ArbitrateDigitalInputAndModalState`

One of those explicitly prepares request ID 3 before calling the router. The other supplies an input-arbitrated request value.

The third call occurs in a shared request-dispatch path that forwards a stored request ID and parameter from runtime UI state.

This directly connects:

**InputGameplay arbitration**
→ **shared gameplay capability mask**
→ **derived UI request inhibit mask**
→ **canonical UI request router**

That is the key evidence for the refined CodeDomain wording.

---

# 7. Exact native request dispatch table

The `00254B50` switch covers request IDs 1..24.

Mechanically recovered dispatch:

| Request ID | Native route |
|---:|---|
| 1 | `0035D660` |
| 2 | `00280A00` |
| 3 | `0035D980` |
| 4 | `0035D660` |
| 5 | `003C87B0` |
| 6 | `00280A00` |
| 7 | `00280A00` |
| 8 | `00280A00` |
| 9 | `00280A00` |
| 10 | `00280A00` |
| 11 | `00280A00` |
| 12 | `0028E970` |
| 13 | `00280A00` |
| 14 | `00280A00` |
| 15 | `00280A00` |
| 16 | `00280A00` |
| 17 | `00280A00` |
| 18 | `00280A00` |
| 19 | `00280A00` |
| 20 | `00280A00` |
| 21 | `00280A00` |
| 22 | `00280A00` |
| 23 | `00280A00` |
| 24 | `0035D080` |

The exact player-facing names of IDs 1..24 are **not** established by the currently available authored/source evidence and are intentionally not invented.

---

# 8. Canonically reconstructed request-open path

One special route does have stronger independent semantics.

## `0035D660`

Canonical runtime-test provenance reconstructs this as:

`UI_RequestOpenGate`

**Complete body:** 75 bytes  
**Exact body SHA-256:**  
`f93a32e4bb776b72d0848aa1f3ad971dd20a14e9b5f98a31c00ae50615520a10`

Independent frozen testing established that it:
- blocks on world/runtime policy bit 10;
- blocks on modal-state conditions;
- applies a special gate for requested mode 1;
- on acceptance mutates pending UI state;
- leaves rejected state unmodified.

Its accepted path calls:

`0028FD50` — `UIRoot_PendingModeSetter`

which independently stores:
- the low-16 requested mode;
- pending flag `0x10`.

`00254B50` routes request IDs **1 and 4** through `UI_RequestOpenGate`.

This validates the word **UIRequest** in the `00313A00` CodeDomain proposal without requiring a guessed player-facing menu label.

---

# 9. Other special routes remain intentionally mechanism-level

## Request 3 → `0035D980`
**Body:** 251 bytes  
**SHA-256:** `419a8ea3ba878f82a571a80cf0109f11f8efcc38a3e3633433c749f59a0b0bbb`

Exact body:
- checks aggregate policy bit 10;
- handles refusal/fallback UI/audio feedback;
- inspects current UI/modal state;
- performs UI transition/reset operations;
- forwards a request/command through existing UI services.

The exact designer-facing screen/action name is not proven.

## Request 5 → `003C87B0`
**Body:** 371 bytes  
**SHA-256:** `d921651e7539272bfec58a269269082c276414133ef5c84134b0e876e94f7a25`

Exact body:
- validates current UI root/state;
- checks modal conditions;
- reconciles a previous handle;
- resolves current UI selection/route state;
- forwards the request;
- transitions a UI child into the active mode.

The exact screen/action name is not proven.

## Generic route → `00280A00`
**Body:** 193 bytes  
**SHA-256:** `02c2b4d20035ce1f8a9459ee04cbe2e66e6ae564132fe3e8a3b60680bf02d228`

Exact body:
- refuses when conflicting root state is already occupied;
- materializes a request descriptor;
- publishes/forwards the requested command;
- schedules the existing UI callback/transition machinery.

This is a generic UI request scheduling/materialization path.

## Request 12 → `0028E970`
Mechanically manages a UI-owned runtime object/handle, releases an old one when present, forwards the request and installs the resulting new object. Exact player-facing meaning remains unproven.

## Request 24 → `0035D080`
Mechanically schedules a UI callback transaction with a fixed native request/event code and passes the command parameter onward. Exact player-facing meaning remains unproven.

---

# 10. Exact subset controlled by `00313A00`

`00313A00` publishes row-2 policy bits:

`0,1,2,3,4,5,6,7,8,10,11,12,20`

Applying the exact native policy→UI-request table gives the union:

**UI request IDs inhibited by the row-2 contribution:**

`1, 2, 3, 5, 14, 21`

Exact contributions:

| `00313A00` row-2 bit | UI request IDs influenced |
|---:|---|
| 0 | 2 |
| 1 | 1, 3, 5 |
| 2 | 3 |
| 3 | 2 |
| 4 | — |
| 5 | 5 |
| 6 | 14 |
| 7 | — |
| 8 | 1, 21 |
| 10 | 3 |
| 11 | — |
| 12 | — |
| 20 | — |

This does **not** exhaust the function's semantics.

Row-2 bits with no derived UI-request entry still participate in direct gameplay/Input/UI eligibility tests elsewhere.

Thus `00313A00` reconciles a **capability policy** that has both:
- direct gameplay/input consumers; and
- a deterministic UI-request-inhibition projection.

---

# 11. ff12-script challenge

The bundled ff12-script research material was checked for authored/native names corresponding to this numeric UI request family.

It did **not** provide a defensible direct mapping from request IDs `1..24` to authored FFXII screen/action names.

Therefore this addendum deliberately preserves:
- exact numeric request IDs;
- exact native routes;
- exact state-transition mechanics;

while refusing to invent labels such as map, inventory, battle menu, target, talk, examine, etc.

A later authored-resource, string-table, runtime or stronger native-state proof may refine individual request IDs.

---

# 12. Refined semantic decision

## `00313A00`

**Strong read-only CodeDomain proposal:**

`InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

### Why this is now stronger than the prior name

Complete evidence proves that the function:
1. reconciles field/battle state into one row of a multi-source gameplay capability mask;
2. affects direct InputGameplay eligibility consumers;
3. affects canonical UI consumers;
4. deterministically projects into specific inhibited native UI request IDs;
5. participates in the same transaction consumed by the canonical high-level Input arbiter and UI request router.

This is more precise than generic “operation inhibit mask” while remaining below unproven player-facing labels.

### Explicit negative boundaries

Do **not** claim:
- `FFXII.Input` PrimaryOwner from the canonical Input consumer;
- `FFXII.UI` PrimaryOwner from the UI request router;
- `CombatAction` PrimaryOwner from current-selected-BattleUnit input state;
- `WorldAreaField` PrimaryOwner from the field-policy input;
- player-facing names for request IDs 1/2/3/5/14/21;
- exact meanings for every policy bit;
- save/load state;
- multiplayer/network semantics;
- that this is automatically a safe XIIOnline replay seam.

This is a V121 **CodeDomain** proposal only.

---

# 13. GN read-only state after this addendum

Current strong proposed unresolved rows:

1. `00313A00`  
   `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

2. `002F7380`  
   `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

**Applied rows: 0**

Official persisted parent remains:
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

If both later pass exact-current GM160 fencing and the full mutation/persistence gate, the prospective arithmetic would be:

- explicit: **38,003**
- unresolved: **158**
- coverage: **99.58596%**

That prospective state is **not** a checkpoint and must not be reported as current.

---

# 14. Required mutation gate

Only after the physical GM160 recovery-transfer GZF is actually accessible:

1. Verify GZF size/SHA.
2. Fresh-import into a brand-new Ghidra project with auto-analysis disabled.
3. Reproduce:
   - 38,161 functions;
   - 38,001 explicit;
   - 160 unresolved;
   - 99.58072%;
   - overlap 0;
   - deterministic snapshot SHA `d2445517c66513976c83a446f87537a3c1d8c21f5bef033779affe98d7e61a20`;
   - authorized embedded EXE SHA `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
4. Regenerate the exact current residual.
5. Verify `00313A00` remains unresolved.
6. Recompute exact-current complete body and require SHA:
   `c076cfeadbc81442c947e0c749eefbdef7e7c6717297847333a7cbae9289d246`.
7. Re-run current data/caller/callee challenge.
8. Reject on any semantic/body/classification drift.
9. Apply only exact expected rows.
10. Require complete-project deterministic diff:
    - intended comment/tag changes only;
    - functions added/removed = 0/0;
    - tag removals = 0;
    - body/range/name/prototype/thunk drift = 0;
    - immutable drift = 0.
11. Close target DomainFile.
12. Pack in a separate headless invocation with explicit `PACK_PASS`.
13. Fresh-import the pack into a completely new project.
14. Reproduce snapshot, ledger, overlap and embedded EXE.
15. Regenerate residual from the fresh post-GN state.
16. Only then claim a persistence-certified GN checkpoint.

