# V121 GN — INPUTGAMEPLAY UI REQUEST MAPPING ADDENDUM — 2026-09-01

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Secondary use:** XIIOnline player-input / party-leader / free-target / menu native-seam research  
**Intended physical parent:** GM160 recovery-transfer GZF contained in the uploaded handoff ZIP  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. Purpose / accounting fence

This document refines the already-strong unresolved GN proposal:

`00313A00`
→ `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

It closes three previously numeric UI-request identities using the exact authorized executable, canonical V120 Input/UI/Party evidence, and explicitly marked external control-layout corroboration.

No GM160 GZF mutation is claimed.

Official persistence-certified GM160 remains:

- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

Strong current unresolved GN proposals remain:

1. `00313A00`
   `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

2. `002F7380`
   `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

---

# 1. Existing policy → request projection

`00313A00` reconciles row 2 of the shared 16-row × 32-bit gameplay capability/inhibition mask.

Existing exact evidence proves row-2 bits:

`0,1,2,3,4,5,6,7,8,10,11,12,20`

project through `00254500` into inhibited native UI request IDs:

**1, 2, 3, 5, 14, 21**

The current addendum closes the player-facing/mechanism identity of:

- request **1**
- request **3**
- request **5**

Requests **2 / 14 / 21** remain intentionally numeric in this earlier addendum. Later `V121_GN_INPUTGAMEPLAY_UI_REQUEST_MAPPING_SUPERSEDING_2026-09-01.md` supersedes request-2/14/21 portions and closes request 2 as Party Menu / Menu Screen.

---

# 2. Native request router

## `00254B50`

Complete body:
- **263 bytes**
- SHA-256:
  `9ab5c3f609a8b886a1876813c746ce12907c205f8a446d7060411ad74dfd4d78`

Canonical category:
**FFXII.UI**

Mechanism:

1. normalize `requestId = ECX & 0x7FFF`;
2. rebuild the inhibited-request mask from the aggregate gameplay policy;
3. test the requested bit;
4. reject inhibited requests without dispatch;
5. dispatch allowed request IDs 1..24 through the native router.

Relevant routes:

- request 1 → `0035D660`
- request 2 → `00280A00`
- request 3 → `0035D980`
- request 5 → `003C87B0`
- request 14 → `00280A00`
- request 21 → `00280A00`

The generic route does not by itself prove player-facing identity for request 2/14/21.

---

# 3. `DecideButton` is proven from the executable settings serializer

The game-facing input arbiter uses runtime masks:

- `01E0C2A0`
- `01E0C2A4`

These are not arbitrary fixed masks.

The executable settings system contains the authored literal configuration key:

**`DecideButton`**

at settings-entry index **25**.

Getter:

## `0017E210`

returns the corresponding settings field at:

`settings + 0x64`

The same settings entry has the literal value labels:

- `Circle`
- `Cross`

Native mapping:

- DecideButton value `0` → Circle
- DecideButton value `1` → Cross

Initialization swaps the two gameplay masks:

### DecideButton = Circle
- `01E0C2A0 = 0x2000`
- `01E0C2A4 = 0x4000`

### DecideButton = Cross
- `01E0C2A0 = 0x4000`
- `01E0C2A4 = 0x2000`

The associated 14-entry logical command list is:

`[13,12,10,8,11,9,1,2,15,14,7,5,4,6]`

and the same setting swaps entries:

`0 ↔ 9`

which swaps logical command IDs:

`13 ↔ 14`.

Therefore `01E0C2A0` is the current configured **Decide/Confirm face-button mask**.

This is executable-authored configuration evidence, not a control-layout guess.

---

# 4. Request 1 = Battle Menu open/request

## Exact InputGameplay trigger

Inside canonical:

## `00253C70`
`InputGameplay_ArbitrateDigitalInputAndModalState`

- body: **1,599 bytes**
- SHA-256:
  `e6309cd50d266650fbb78a725a5aaaefb69c656a51dffc87c8299f30c15fa093`

the request-1 path tests the current input mask against:

**`01E0C2A0 | 0x8000`**

and, after its normal gameplay/UI eligibility gates, hardcodes:

```text
requestId = 1
call 00254B50
```

Thus request 1 is activated by:

- the currently configured **Decide/Confirm** button;
- or raw button mask `0x8000`.

External PS2 control documentation independently identifies raw `0x8000` as Square in the native pad bit layout, and FFXII field controls document both:
- the Decide/Accept button;
- and Square

as Battle Menu entry controls.

## Native route

Request 1 routes through:

## `0035D660`
working name:
`UI_RequestOpenGate`

- body: **75 bytes**
- SHA-256:
  `f93a32e4bb776b72d0848aa1f3ad971dd20a14e9b5f98a31c00ae50615520a10`

The accepted path uses the existing UI-root pending-mode setter.

## Decision

**PROVEN / STRONG**

Native request:

**1 = Battle Menu open/request**

Strong working request name:

`UIRequest_BattleMenuOpen`

---

# 5. Request 3 = field party-leader selection/change

## Exact InputGameplay trigger

Inside `00253C70`, request 3 is entered from:

raw input mask:

`0x10 | 0x40`

These are the native D-pad **Up/Down** bits in the PS2 control layout.

The path:
1. requires the relevant gameplay policy gates;
2. scans mapping-class-3 BattleStats/party candidates;
3. requires at least two eligible candidates unless the separate story/global condition permits the path;
4. hardcodes `requestId = 3`;
5. calls `00254B50`.

The candidate scan resolves through canonical local mapping machinery:

## `0031B9F0`
`BattleSlotMap_ResolveMappedBattleSlot`

## Native UI route

Request 3 routes through:

## `0035D980`

which enters the UI family containing:

## `0035BC50`

That UI builder obtains canonical PartyFocus state from:

- `PartyFocus_GetPreferredDefinitionSelector`
- `PartyFocus_GetCurrentPackedActorHandle`

and builds the relevant UI/list state through the existing menu/list runtime.

This establishes that request 3's screen/state is explicitly rooted in current/preferred **PartyFocus** identity.

## Exact commit path

The selection-confirm branch later:

1. resolves the selected UI row;
2. reads the row's actor/party selector;
3. invokes `0035BAA0` exactly once to commit the selected controlled leader/focus state;
4. closes/updates the UI state.

Independent XIIOnline native-call research already identifies `0035BAA0` as the one-shot native party-leader setter and rejects repeatedly pinning it.

## Decision

**PROVEN / STRONG**

Native request:

**3 = field party-leader change / leader-selection UI**

Strong working request name:

`UIRequest_FieldPartyLeaderSelection`

---

# 6. Request 5 = field free-target actor cycle / target selection

## Exact InputGameplay trigger

Inside `00253C70`, request 5 is triggered by raw input:

`0x20 | 0x80`

which corresponds to D-pad **Right/Left**.

The branch:
- checks gameplay-policy eligibility;
- checks current UI/modal state;
- enters the request-5 target-selection family.

## Native route

Request 5 enters:

## `003C87B0`

- body: **371 bytes**
- SHA-256:
  `d921651e7539272bfec58a269269082c276414133ef5c84134b0e876e94f7a25`

The function:
1. validates current UI root/state;
2. resolves current target/selection state;
3. selects navigation mode;
4. asks `003C9250` for an actor candidate;
5. commits the selected candidate through `003C9420`;
6. publishes/activates the corresponding UI target-selection state.

---

# 7. Spatial actor target ordering — `0035DCC0`

## `0035DCC0`

Complete body:
- **492 bytes**
- SHA-256:
  `b2a88e3522fe613f1b271bbd2afbeaca323de7f3deb7508e2110ffc143acd7a8`

The function:
1. iterates actor-handle candidates from the target-selection source list;
2. resolves each candidate through the native actor registry;
3. obtains actor positions;
4. computes relative vectors / angular-distance ordering;
5. materializes compact candidate records;
6. sorts them through the native target-ordering helper.

This proves the request-5 family operates on **spatial actor targets**, not ordinary menu rows.

---

# 8. Previous/next actor resolver — `003C9250`

Complete body:
- **280 bytes**
- SHA-256:
  `33c668294798b45c2b01f0e9604e33897880efce9b44df24586b269862e12723`

It resolves previous/next/first/last eligible actor targets according to current target state and ordered candidates.

---

# 9. Selected actor commit — `003C9420`

Complete body:
- **117 bytes**
- SHA-256:
  `d374dc29fca5331126b1bb2fc5c0692c4ebf7500dfb04bc63f61bb0aa411aa8c`

Exact behavior includes:

1. publish selected actor handle into UI root state;
2. send the native selection command for that handle;
3. validate the selected actor handle through the existing actor/target eligibility service;
4. publish the validated active target into the secondary UI-root selected-target field.

Thus request 5 ends in a real **selected actor target**, not a cosmetic cursor-only transition.

## Decision

**PROVEN / STRONG AT MECHANISM LEVEL**

Native request:

**5 = field free-target actor selection / previous-next target cycle**

Strong working request name:

`UIRequest_FieldFreeTargetActorCycle`

---

# 10. Request IDs still intentionally unresolved in this earlier addendum

This earlier addendum kept 2/14/21 numeric. Later superseding evidence closes request 2 and structurally separates 14 from 21. Use `V121_GN_INPUTGAMEPLAY_UI_REQUEST_MAPPING_SUPERSEDING_2026-09-01.md` as current request-map authority.

---

# 11. Refined interpretation of `00313A00`

Current strongest GN proposal remains:

`InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

The exact policy suppresses distinct player operations and is not a generic save flag bank, CombatAction-only state, or UI-only local screen bitset.

---

# 12. PrimaryOwner boundary remains unchanged

These request identities do not grant a V120 PrimaryOwner to `00313A00`.

The evidence spans CombatAction, WorldAreaField, InputGameplay, UI, PartyFocus and actor-target selection. This cross-layer character is precisely why the V121 CodeDomain proposal remains separate from V120 PrimaryOwner taxonomy.

---

# 13. XIIOnline consequence

- Battle Menu request state itself is local UI policy, not shared-world authority.
- Party leader assignment is server/persistent-party policy; use the one-shot native setter when a legitimate local leader transition is required.
- Raw free-target actor handles are process-local. Convert local actor selection to stable network actor identity before transmitting action intent; receiver resolves stable identity to its own local native representation.

---

# 14. Supersession

For the final six-request map, use:

`V121_GN_INPUTGAMEPLAY_UI_REQUEST_MAPPING_SUPERSEDING_2026-09-01.md`

It closes request 2 as Party Menu / Menu Screen and classifies request 14 vs 21 while preserving them unnamed where evidence remains insufficient.
