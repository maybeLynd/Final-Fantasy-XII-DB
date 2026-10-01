---
contract: decide whether a party member is owed experience or licence points for a kill, and how much
category: 13-Rewards-Progression-Economy
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 13-Rewards-Progression-Economy/how-experience-is-computed-and-divided.md
entries: ["002F8BB0", "002F90C0", "003135C0", "00313800", "0031B810", "0031B860", "00320AB0", "00264150"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 89 addresses cited - 7 data, 12 entry, 68 interior, 2 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-22
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-experience-licence-award-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
production_review:
  section: SECTION-03
  by: external-continuation
  status: "PRODUCTION COMPLETE; independently accepted with a narrowing 2026-10-01 (SWE2-AUDIT-SEM, auditsem-review-section03-1001, GR-16, N1)"
  evidence: _experiments/evidence/continuation-section03-reward-bindings/REVIEW.md
  audit_scope: "Existing audit/annotation metadata is historical, not acceptance of these edits."
---

# Contract — the experience and licence-point award

**Current bounded production review — SECTION-03, 2026-09-22.** The original EXP/LP bodies and
callee chain were re-read, **71 original-instruction controls** passed with an identical repeat,
and six deliberately incorrect private-image variants failed their intended assertions.
An independent reduction also checked **88 retained EXP-081 spans**. This is not a new live
FF12 session, full rerun of the old Unicorn campaign, or formal peer acceptance.
[Review, exact cases and limits](../_experiments/evidence/continuation-section03-reward-bindings/REVIEW.md).

The key correction is at the interface: **NULL recipient does not disable EXP division.** It
skips recipient-only checks/modifiers; shared-mode EXP still counts four roster entries and
performs signed division. **LP is not divided, and does not call the EXP owning-unit finder.**
The old contract and related death pages had conflated these distinct rules.

## 1. Purpose

`002F8BB0` computes experience and `002F90C0` computes licence points for a recipient and a
kind-1 subject unit. These routines compute values; the defeat orchestrator applies them.
A zero result can mean rejection, an actual zero, signed division rounding toward zero, or
an EXP zero modifier. It does not identify which condition occurred.

## 2. Interface

| Boundary | Meaning |
|---|---|
| `RCX` | Recipient `BattleStatsRecord*`, **allowed to be NULL**. |
| `RDX` | Subject/defeated `BattleUnit*`; NULL returns zero after earlier applicable gates. |
| `EAX` | Signed 32-bit computed value; callers must preserve native wrap/divide semantics. |
| Calling convention | Microsoft x64. No output-buffer parameter. |
| Writes | No writes to the supplied records/rows in the selected bodies; stack saves are not persistent state. The native fixture additionally compares all synthetic data bytes. |

These are not interchangeable predicates. In particular, an ownerless but otherwise valid
kind-0 stats record is rejected by EXP and admitted by LP under the tested synthetic setup.
That demonstrates an API distinction, not that the normal defeat caller supplies orphan records.

## 3. Types

| Object and offset | Width / role |
|---|---|
| recipient `+4`, `+5` | ID byte and kind byte. Non-NULL recipients must have kind zero. |
| recipient `+0x3C`, `+0x64` | Status words, OR'd then tested with `0x80000003`. |
| recipient `+0x6B`, `+0x7B` | Modifier bytes: EXP bit `0x08` doubles, then bit `0x20` zeroes; LP bit `0x10` doubles. |
| subject `+0x698` | Stats pointer. Must be non-NULL, with stats kind `+5 == 1`. |
| subject stats `+0x1C2`, `+0x88` | Two unsigned bytes, level and stored rebuild baseline, subtracted as integers. This consumer reads the actual baseline byte; it does not substitute a constant `1`. |
| subject `+0xE70` | Base/addend row pointer, produced through registry slot `02EBF148`. |
| subject `+0xE78` | Per-level/multiplier row pointer, produced through `02EBF140`. |
| each reward row `+0x34` | 32-bit EXP coefficient. |
| each reward row `+0x2F` | Unsigned byte LP coefficient. |

The enemy arm at stats `+0x88` is distinct from the party Gambit interpretation of that region.
The canonical mechanism is
[how a battle unit is built](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md).
No general row lifetime or complete pointee layout follows from these consumer offsets.

## 4. Preconditions · postconditions · invariants

| Test | EXP | LP |
|---|---|---|
| Global licence byte `00264150()` | Not consulted. | Checked first; any nonzero signed-byte result returns zero before dereferencing the arguments. |
| Non-NULL recipient kind | Must be zero. | Must be zero. |
| Owning-unit lookup `0031B860(recipient)` | Must succeed for a non-NULL recipient. | **Not called.** |
| Recipient ID | Reject `0x1B..0x27`. | Admit `0..6`, `0x1A`, or `>=0x28`. |
| Recipient status words | Mask `0x80000003` must be clear. | Same mask. |
| Subject and subject stats | Both non-NULL; stats kind must be one. | Same. |
| Reward-row pointers | No local NULL check once their formula reads are reached. | Same. |

**NULL recipient bypasses only the recipient-specific rows of this table.** It does not bypass
subject checks, the EXP mode decision/count, or the LP global gate.

The LP ID-admission set is a subset of EXP's recipient ID set. That is **not** an implication
that a record earning LP must earn EXP: the latter also has ownership, mode and modifier rules.

## 5. State

Inputs include the subject/recipient records, cached authored-row pointers, mode flags and
roster maps. Stable inputs give deterministic arithmetic; the functions do not take an atomic
snapshot of all those globals. A bracketed read is not proof that no concurrent/intermediate
change can happen. No timing or lifetime guarantee is added here.

## 6. Relationships and row production

The kind-1 installer `0023A570` reads the enemy definition's words `+0x22` and `+0x24` to select
rows via `02EBF148` and `02EBF140`. Original stores are `0023A9A5` and `0023A9F4`.

For each non-NULL descriptor it decodes `[descriptor+0x0C]` with `0020E600`, rejects a zero
decoded base on that path, then combines the unsigned 16-bit index and stride from `+8` with
**32-bit** `imul`/`add` before zero-extending the result into the 64-bit unit field.

```
decoded = (zero_extend_u32(encoded) + relocation_base_u64) modulo 2^64
stored_row = zero_extend_u32(index_u16 * stride_u16 + low32(decoded))
```

A zero encoded value decodes to the relocation base; it is not a universal NULL sentinel.
A decoded address above 4 GiB can lose high bits in the stored row. Descriptor absence, decoded
zero, and arithmetic wrap-to-zero are distinct paths. The complete installer and its earlier
reset/rekey effects are outside a pure row-lookup abstraction; **failure is not transactional**.
See [SECTION-01](../_experiments/evidence/continuation-section01-result-install/REVIEW.md).

`0031B810(i)` is the shared-mode roster lookup. The native fixture uses the original lookup,
unit scan, bounds and mode helpers rather than scripted replacements. Only reached branches
of those helpers are covered; this is not certification of every bounds-dispatch arm.

## 7. State transitions — exact computation

Define `D = u8(subject.stats+0x1C2) - u8(subject.stats+0x88)`.
Let `A` be the **signed interpretation of the low 32 bits** of
`D * u32(perLevelRow+0x34) + u32(baseRow+0x34)`.

**EXP:** after its gates, `003135C0()` selects the two modes.

- Nonzero: call `00313800()`. A non-NULL recipient must equal
  `00320AB0(returned_index, 1)`; NULL skips that comparison. Set the pre-modifier result to `A`.
- Zero: enumerate **exactly four** entries through `0031B810(0..3)`. Count returned members
  whose status mask is clear, excluding kind-zero IDs `0x1A..0x27` through the two separate
  original tests. No member means zero without reading either reward row. Otherwise compute
  `A / count` using signed `idiv`, truncating toward zero.
- For a non-NULL recipient, double the resulting 32-bit value if either modifier byte has
  bit `0x08`, then set it to zero if either has bit `0x20`. NULL skips both modifications.

Consequences: `19 / 2` is `9`; doubling that share yields `18`, not `19`. NULL in the same
shared state also returns `9`. In single-recipient mode NULL returns `19`. A zero roster returns
zero even if the cached reward pointers are NULL, because this branch never reads them.

The roster word-match excludes kind-1 records from ordinary byte selectors. Do **not** strengthen
that into "only kind zero can ever be returned": `0xFF` has a `0xFFFF` comparison special case.
A synthetic descriptor count of 256 plus a kind-`0xFF` record allows that sentinel to be returned
and counted. This does not establish that a shipped initialized roster reaches the condition.

**LP:** after its gates, compute the signed low-32-bit result of
`D * u8(perLevelRow+0x2F) + u8(baseRow+0x2F)`. For a non-NULL recipient, either modifier byte's
bit `0x10` doubles it. There is **no divisor, no designated-recipient test, no owning-unit search,
and no EXP-style zero modifier** in this function.

Neither function clamps negative results or 32-bit arithmetic wrap. The defeat caller's clamps
are separate operations.

## 8. Script · resource · event interactions

The coefficient rows are authored data reached through cached pointers; the level/baseline bytes
are runtime stats. The installer is where those relationships are established. EXP-081 observed
selected initialized bindings, not the installer executing and not a reward event.

The caller `00312280` invokes both computers with NULL recipient at `003124BE` and `003124CA`,
clamps the fresh values, and may zero EXP under `00236780()` before passing values to
`0028FB80` at `00312518`. **That is an unmodified, mode-dependent EXP share—not universally an
undivided pool.** LP is an unmodified computed LP amount because LP was never divided.
No screen rendering or complete defeat transaction was executed in this section.

## 9. Determinism

No RNG draw is made by the selected reward routines. Preserve input widths, modulo-32-bit
arithmetic, signed division, and gate order. Caller/callee state can differ between separate
invocations; "pure computation" is not a global synchronization guarantee.

## 10. Failure paths and edge conditions

- Zero is ambiguous: rejected inputs, a legitimate zero, rounding, and EXP zeroing share it.
- Both subject NULL checks precede row dereferences. LP's global gate is earlier still.
- A valid subject with a NULL multiplier row faults at `0x34` in EXP or `0x2F` in LP once the
  formula is reached. The base-row faults have the same respective displacements. These were
  isolated child-process controls, not crashes induced in FF12.
- Zero roster avoids EXP row dereferences; it does not protect LP.
- An out-of-range reward index against a positive descriptor count causes an early installer
  rejection before later row stores. Earlier reset/rekey effects can already exist. Unsigned
  zero-count underflow and missing-descriptor paths must not be collapsed into that case.
- An LP coefficient `0xFE` is `254`, not `-2`; the original uses `movzx`.
- The caller must not assume all nonzero/negative results represent a reachable gameplay award.

## 11. Observable behaviour and retained binding evidence

The historical EXP-081 samples contain reward-registry words and `BattleUnit+0xE70/+0xE78`
inside the full before/after pools. At the completed-load popup both reward slots are zero and
there are no occupied actor/stats-bound units. In the field, both slots are nonzero and three
kind-1 units have nonzero reward pointers. The observed kind-zero unit's reward pointers are zero.

| Field-stage unit slot | Base selector / cached pointer | Per-level selector / cached pointer |
|---|---|---|
| 4 | `6 / 67483D90` | `4 / 67484050` |
| 5 | `5 / 67483D58` | `3 / 67484018` |
| 7 | `0 / 67483C40` | `0 / 67483F70` |

Registry descriptor words are `67483C20` (base) and `67483F50` (per-level); the retained image
address-base word is zero. All values repeat across both field samples and the reward-pointer
bytes match the pool brackets.

**No reward descriptor bytes or required reward-row prefix bytes were captured.** Selector/row
address differences fit affine spacing `0x38`, with the selector-zero pointers `0x20` after the
descriptor addresses. That is a conditional consistency observation, **not a read of header
stride/count/encoded base, validation of coefficients, or proof of lifetime**. No payout amount,
kill, or row dereference by a reward consumer was observed live in these captures.

## 12. Reproduction formula

The executable reproduction is the [SECTION-03 native fixture](../_experiments/evidence/continuation-section03-reward-bindings/native_controls.c).
It runs the original reward functions and gate callees over synthetic records, without replacing
application callees. Distinguishing controls include:

- Shared roster counts 0..4 with NULL recipient; LP checked against the same states.
- An EXP-doubled recipient versus NULL in a two-member roster: `18` versus `9`, while normal
  EXP is `9`. LP-doubled versus NULL: `38` versus `19`.
- Mode-one designated/mismatched/NULL recipients, including an invalid designation.
- Kind-zero orphan stats: EXP `0`, LP `19` with the LP gate clear.
- Recipient ID `0x1A` admitted for EXP/LP but excluded from the EXP divisor.
- Exact masks/byte width, zero roster, negative division, arithmetic wrap, and NULL row accesses.

All numeric values here belong to declared synthetic fixtures, not sampled authored coefficients.

## 13. Runtime validation

**Three evidence classes remain separate.**

1. Historical reconstruction differential checks and [EXP-090](../_experiments/EXP-090-reward-gate-exec.md)
   are the original campaigns, not rerun here. EXP-090 records 104 cases and ten mutations;
   its scripted-predecessor cases must not be mistaken for initialized-game reachability.
2. SECTION-03 executes 71 bounded controls on original CPU instructions, repeats identically,
   and rejects six private-image variants. Synthetic state only; no application-call stubs.
3. [EXP-081](../_experiments/EXP-081-live-battleunit-bindings.md) is a historical live read-only
   capture. SECTION-03 independently rechecks its 88 spans and ten corrupted-record controls,
   and replays the supplied retained-reward checker unchanged. This consumes existing evidence;
   it does not run a fresh game session or grant formal peer acceptance.

The old wording "live capture absent" was too broad for bindings, while "live reward calculation
validated" would also be false. The observed binding words and unobserved reward contents are
listed separately in §11.

## 14. Unresolved

- Actual reward-header counts/strides/encoded references and row coefficients in the sampled
  session were not retained. New observation would be needed for those contents.
- No continuous binding/allocation lifetime, setter-to-consumer chronology, death timing, or
  rendered amount is established by EXP-081.
- Shipped reachability of zero-count/missing descriptors, high relocation bases, level-zero
  rewards, and the synthetic kind-`0xFF` roster case remains separately unproved.
- Names and producer semantics of the status-mask bits and ID policies remain in their owning
  system pages; reading a shared constant does not prove a shared control variable.
- Full defeat orchestration, notification subscribers and all reward/growth/resource dependencies
  are not certified by these two computers. No S-32 L2 verdict is changed by this production.

The mapped gates are no longer all unknown: EXP-090 and the original chain explain their
bounded decisions, and the selected paths run in SECTION-03. Do not keep assigning those same
static gate questions as "live-only" merely because an old handoff said so.

## 15. Evidence

| Claim | Primary support and scope | Tier |
|---|---|---|
| NULL does not bypass shared EXP division | Original `002F8C34..002F8D24`; count 0..4 native controls and divide-removal mutant. | 1 |
| EXP-only owning-unit search | `002F8BDE` versus whole LP body `002F90C0..002F9173`; orphan control and finder-guard mutant. | 1 |
| EXP and LP coefficient widths / modifiers | Original `+0x34` dword versus `+0x2F` zero-extended byte loads; widening-mask and signed-byte mutants. | 1 |
| Exact four-entry divisor and separate ID `0x1A` exclusion | `002F8CD8`, `002F8CE2`; native member/ID controls and loop-bound mutant. | 1 |
| Original roster does not universally imply kind zero | `002367A0` sentinel comparison; bounded synthetic kind-`0xFF` control. | 1 |
| Cached reward pointers / missing content | Independent parsing of original EXP-081 raw spans, not conclusions copied from its normalizer. | 10 |
| Producer mapping and 32-bit row construction | `0023A965..0023A9FB` plus original decoder `0020E600`; static re-read and prior EXP-075/076 evidence. | 1 |
| Caller uses NULL but does not thereby restore an undivided pool | `003124B4..0031251D` plus original computers; full caller not executed. | 1 |

[Original body identities/disassembly and reproduction](../_experiments/evidence/continuation-section03-reward-bindings/REVIEW.md).
The preceding audit-pass and annotation-transfer records are historical; they do not certify the
new revision. Prior raw experiments/programs remain untouched. No completion score, TEAM claim,
L2 acceptance, or reconstruction implementation is edited here.

## 16. Parity plan

A later implementation should preserve the null-recipient distinction, conditional owner check,
mode-dependent EXP division, LP asymmetry, actual baseline byte, signed arithmetic, mask order,
row-pointer construction, and rejection/zero ambiguity. Do not infer actual coefficients or
lifetime from pointer samples. L3 implementation/parity is later; this package closes bounded
production corrections and leaves ~~formal peer acceptance pending~~ formal peer acceptance to the auditor. *(OPUS, 2026-10-01: independently accepted with a narrowing 2026-10-01 (SWE2-AUDIT-SEM, [review](../_index/candidates/auditsem-review-section03-1001/REVIEW.md), GR-16; N1: `run_review.py` reproduces against the pinned pre-image of the reward-binding checker, and the sealed checker agrees with the preserved observation).)*


## Historical cross-system notes

The following existing ownership/crossing notes are retained, not independently re-censused by SECTION-03.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

`BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`) and the 24-byte mode test `003135C0` are shared lookups:

- **Movement — CLIENT.** `0031B810` is read by `PartyFollow_SolveFormation` and two locomotion bodies (181 B and
  1,028 B). `003135C0` is read by `PartyFollow_SolveFormation` and a 668-byte body.
  `BattleStats_FindOwningBattleUnit` is used by two more locomotion bodies.
- **Presentation — CLIENT.** `0031B810` is read by `PartyCombat_UpdateStanceState` and
  `BattleUnit_BroadcastPartyCombatTargetRelatio…`. The 8-byte `00264150` is read by a 4,810-byte Presentation body.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — SERVICE.** `0023A570` on this page calls `BattleUnit_ResetStateForReuse`, owned by that layer. What it reaches is the reuse reset, and it states the unit's sentinels: `word[+0x695]` becomes `0xFFFF`, `byte[+0x694]` becomes `0xFF`, `dword[+4]` is masked with `0xFFEFFFBB`, and the `+0xBC0` candidate block is cleared; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — CLIENT.** `AiOrder_EvaluateTargetSelector`, owned by that layer, calls `0031B810` on this page. That caller is the selector evaluation, 6,963 bytes of it: it indexes its table at a **six-byte stride** and takes a word at `+6`, two bytes at `+8` and `+9` and a signed word at `+0xA` before deciding anything; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CombatFormula — SERVICE and CLIENT (45 edges).** The `FIND` gate `BattleStats_FindOwningBattleUnit` `0031B860` is called by 35 formula bodies besides this contract's computers, among them `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30`, `BattleStats_ModifyHPAndProcessLethalState` `00300530`, `BattleFormula_ApplyTargetResult` `003112F0`, `BattleFormula_ResolveTargetResult` `00385F60`, `BattleFormula_ApplyPreResolutionTargetGates` `00390AB0` and `BattleFormula_DispatchPostResultEvents` `00469EC0`; `Reward_ComputeExperienceForRecipient` `002F8BB0` calls `0031B860` and `BattleStats_GetByMappedBattleSlot` `00320AB0`, and `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` calls `00320AB0`; the kind-1 installer `BattleUnit_ApplyUnitDefinition` `0023A570` calls `BattleStats_InitializeDefinitionRecord` `0023AC80`, which calls the growth rebuild `0030C470`, and `0030C470` calls `BattleStats_ReconcileCurrentHpToEffectiveMaximum` `0030F340` and `BattleStats_ReconcileResourcesToEffectiveCapacity` `0030F5A0`; `002FEF30` calls `002F9180` (21 bytes: the product of its two arguments divided by 100) and `BattleEncodedId_IsValidForClass` `00322C50`; `00388D50` calls the roster lookup `0031B810`. The award reads the stats record through the formula layer's own accessors and the level-up rebuild re-runs its stat reconciliation, so these edges are shared accessors and the rebuild path, not a second EXP computation.

**Gameplay — SERVICE and CLIENT (12 edges).** `BattleUnit_FindByDefinitionSelector` `002367A0`, `0023A570` and `BattleUnit_FindMappedDefinitionSelectorByIndex` `0031B810` call `BattleEncodedId_IsValidForClass` `00322C50`, which `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` and `0031C5D0` also call, and `00320AB0` calls `0031B9F0`; `002367A0` is called by `00312B40`; `0031B810` is called by `00234150` and `BattleUnit_CollectMappedFourSlotUnitsByFlags` `0030A8A0`; `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0` calls `0030C470`; `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0` is called by `BattleRuntime_GetModeDependentDistanceThreshold` `00309A90` and by the `SINGLE` gate `003135C0`, which returns 1 exactly when `0030D9A0` answers 1. These are the id-validity test, the slot map and the battle-mode query the award's `PARTY`, `RESOLVE` and `SINGLE` gates use, shared with the domain's other slot and distance helpers.

**Party — CLIENT (16 edges).** `PartyFocus_SelectAndRequestDefaultActor` `00326500` and `PartyConfiguration_ReconcileRuntimeRosterFirstThreeFromRequestedSelectors` `00328DB0` call `002367A0`; `00303CC0`, `00303F00` and `00326500` call the mode query `0030D9A0`; `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040` calls `003135C0`; `00304180` calls `00320AB0`; and nine party bodies call `00322C50`, among them `PartyConfiguration_AddSelector07To25ToAvailablePrimaryIndex` `003170E0`, `PartyConfiguration_CollectRuntimeRosterSelectors0To3` `0031B510`, `PartyConfiguration_SetDefinitionSelectorForIndex` `00329080`, `0031AC00` and `00326500`. The roster and focus code asks the same selector lookup, id-validity test and single-mode question the award's gates ask; the party layer consults them and does not take part in the award.

**PlatformOnlineAchievements — SERVICE (1 edge).** `00312280` calls `00316A50`. The defeat path hands the licence points it awards to the achievement-progress body (the auto-status contract reads the call with the LP value and `0xB` as its arguments), so the platform layer counts what this contract computes and feeds nothing back into it.

**Save_Load_Settings — CLIENT (1 edge).** `SaveImage_FinalizeHeaderAndChecksum` `00583D60` calls `00236780`. `00236780` returns bit 14 of the dword at `+4` of the battle-flags block, the flag that zeroes the EXP commit here; the save finaliser reads the same bit for the header it writes.

**Script_VM_Native_Bridge — CLIENT (8 edges).** `0050CC30` calls the licence gate `00264150` and pushes its value; `0050FD00`, `0050FD50`, `0050FDD0`, `0050FE20`, `0050FE80`, `0050FED0` and `0050FF20` call `00320AB0`. `00264150` is the `LGATE` byte read as a signed value, so a script verb can read that gate; `0050FD00` (read) pops a slot index, fetches the mapped stats record and pushes its byte `+4` (or -1), and the six siblings are the same stats-by-slot verb family named from the census.

**Spawn_Encounter_Lifecycle — CLIENT and SERVICE (5 edges).** `Spawn_ApplyScriptSelectedUnit` `0023A3B0` calls `0023A570`, which calls `SpawnKeep_ResolvePrimaryEntry` `00236100`; `002398F0` calls `0030C470`; `Spawn_ValidateCandidateDistanceToPlayers` `00234DA0` and `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` call `0031B810`. The spawn layer installs the kind-1 definition this contract's growth reads and reuses the roster lookup for its player-distance tests.

**Status_Periodic_Terminal — SERVICE and CLIENT (12 edges).** `0030C470` calls `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690` and `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0`; `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` calls `00312280`; `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400`, `0030E360`, `0030F690`, `0030FED0` and `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860` call `0031B860`; `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls `00320AB0` and `00322C50`, as do `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130` and `0030FED0` for `00322C50`. A status change's side-effect processing is what calls the defeat-reward path, and a level-up's rebuild recomputes statuses; the rest is the status code sharing the same stats-to-unit lookups.

**UI — CLIENT (5 edges).** `00295D90`, `002BA310` and `002C1A80` call the licence gate `00264150`; `BattleMenu_BuildCommandEntryList` `0031EB20` calls `003135C0` and `00322C50`. Menus read the same licence byte and the single-mode answer when they build their entries; they display state and do not change the award.

**WorldAreaField — SERVICE and CLIENT (5 edges).** `0023A570` calls `FieldData_GetActiveFieldRecordBit15` `00313F60`; `0030D9A0` and `00312280` call `FieldData_GetActiveFieldRecordBit15` `00377C20`; `0057FB00` calls `00264150`; `BattleSystem_RunFieldFrameOrchestrator` `00234590` calls `003135C0`. The mode query folds in the field record's bit 15 and the defeat path consults it too, and the field frame asks the single-mode question each frame; the field layer supplies one permission bit here and owns nothing in the award.

## Appendix — pre-SECTION-03 evidence retained by the owner (OPUS, 2026-09-25)

> **Historical, and subordinate.** SECTION-03 rewrote this contract; its corrections were ACCEPTED by the owner
> (`_index/candidates/section03-owner-review.md`: R03-1 a NULL recipient still divides in shared mode, R03-3
> recipient admission ≠ divisor admission, R03-4 an empty roster returns 0 before any row read, the NULL effect-
> modifier skip). **Wherever the text above corrects a statement below, the text above governs.** What follows is
> kept verbatim from HEAD (`git show <pre-overlay>:13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md`) because it carries evidence the rewrite
> dropped - 95 citation tokens per `overlay_drop_census.py` - not because its conclusions stand unchanged.

### From HEAD's §15a (kept whole, per the owner review)


**passes: 1 · last_pass: 2026-09-12**

`002F8BB0` (430 B, 120 instructions) and `002F90C0` (179 B, 56) decoded whole. This contract leans on
**negative** claims, so each one's controls are enumerated rather than its absence asserted — and
`test`/`cmp` are excluded from the write detector, a mistake that cost a false write-list elsewhere
in this sweep.

| claim | measured |
|---|---|
| **both functions are pure and write nothing** | **0 writes to any record** in either body. Residue named: **4** stack-frame writes in the experience path, **1** in the licence path, all `[rsp+N]` |
| the licence award has **no division anywhere** | `div`/`idiv` in `002F90C0`: **none** |
| the divided path uses a **signed** divide | `002F8D1C cdq` / `002F8D1D idiv ebp` |
| the mask `0x80000003` gates **both** awards | `002F8C06` and `002F8CAD` in experience, `002F90FD` in licence |
| the licence award reads `+0x2F` of both rows | `002F9132 movzx ecx, byte [rax+0x2F]` and `002F9140`, multiplied then added — **bytes**, and no divide |

### The null-test claim is positional, so it was checked positionally

*"Both reward row pointers may be NULL and neither function checks them — no null test stands between
`+0xE70`/`+0xE78` and the indexed read."* Every load-to-use pair, in order:

```
002F8C73  mov rax,[r14+0xE78]   ->  002F8C7A  imul esi,[rax+0x34]     nothing between
002F8C7E  mov rax,[r14+0xE70]   ->  002F8C85  add  esi,[rax+0x34]     nothing between
002F8D07  mov rcx,[r14+0xE78]   ->  002F8D0E  imul eax,[rcx+0x34]     nothing between
002F8D12  mov rcx,[r14+0xE70]   ->  002F8D19  add  eax,[rcx+0x34]     nothing between
002F912B  mov rax,[rdi+0xE78]   ->  002F9132  movzx ecx,[rax+0x2F]    nothing between
002F9136  mov rax,[rdi+0xE70]   ->  002F9140  movzx ecx,[rax+0x2F]    one imul, no test
```

The bodies do contain null tests — **13** in the experience path, **5** in the licence path — but
every one is on a *different* pointer, and all of them fall after the row reads. **The claim holds,
and the count of unrelated tests is what makes that worth stating.**

### The four bound guards, with the compare that sets each one's flags

They live in `BattleUnit_ApplyUnitDefinition` (`0023A570`, 1,808 B), not in either award function:

| guard | branch | index source |
|---|---|---|
| `0023A6BB` | `ja` — **unsigned** | `movzx eax, word [rsi]` |
| `0023A726` | `jg` — **SIGNED** | `movzx eax, word [rsi+0x50]` |
| `0023A747` | `ja` — unsigned | `movzx eax, word [rsi+0x22]` |
| `0023A768` | `ja` — unsigned | `movzx eax, word [rsi+0x24]` |

**Three unsigned and one signed, exactly as claimed** — and the mechanism is now on the page rather
than implied. Each is `movzx` (so the index is zero-extended, never negative), then `dec ecx` on the
count, then `cmp eax, ecx`. **With a count of zero, `ecx` becomes `0xFFFFFFFF`**: under `ja` nothing
is greater, so *every index passes*; under `jg` that same `ecx` is `−1`, so any index is greater and
*everything is rejected*. The one signed guard is the only one that fails closed on an empty table.

**Not claimed:** no live observation; §13 unchanged.


### From HEAD's 3. Types

| field | width | role here |
|---|---|---|
| `+0x05` | u8 | the kind discriminator. **Recipient must be 0 (party); the corpse must be 1.** |
| `+0x04` | u8 | the id the eligibility filters test, and the two rewards filter it **differently** |
| `+0x3C`, `+0x64` | u32 | two status words, OR'd and masked `0x80000003` |
| `+0x6B`, `+0x7B` | u8 | two parallel modifier banks; bit 3 doubles, bit 5 zeroes |
| `+0x88` | u8 | on a kind-1 record, the enemy arm of the `gambitBlockByKind` union: **the third argument the rebuild stored**, `0030C4B1`, observed as `1` |
| `+0x1C2` | u8 | **the corpse's LEVEL**, `[0, 99]`, zeroed by the rebuild at `0030C496` before growth runs |

**`+0x88` is read here as a single byte off a kind-1 record**, at `002F8C6A` and `002F8CFE`
(`movzx eax, byte ptr [rax + 0x88]`), which is an independent consumer confirming the union declared
in `001668a` from the other side: on a party record those bytes are a `GambitConfig`, and on a
spawn-backed one the first byte is this. Two subsystems, one discriminator.


### From HEAD's 4. Preconditions · postconditions · invariants

| | admitted |
|---|---|
| experience (`002F8BF2`–`002F8BFA`) | everything **except** `0x1B`–`0x27` (`al - 0x1B`, `cmp 0xC`, `jbe` rejects) |
| licence points (`002F90E7`–`002F90F5`) | `0x00`–`0x06`, `0x1A`, and `0x28` upward — so `0x07`–`0x19` **and** `0x1B`–`0x27` are rejected |


### From HEAD's 6. Relationships

  Both use the `AuthoredTableHeader` idiom `CONTRACT-authored-table-row-lookup` specifies —
  `resolve(header +0x0C)` through `0020E600`, stride from the header's `u16` at `+0x08`, index
  times stride plus base (`0023A985`–`0023A9A5` and `0023A9C5`–`0023A9EC`). This confirms the
  unit-definition page's own table from the other side, which records those two words as
  bounds-checked against exactly those slots.


### From HEAD's 7. State transitions — the computation

```
esi = (u8)corpse.level - (u8)corpse[0x88]         002F8C63, 002F8C6A, 002F8C71
esi *= [ unit.rewardPerLevelRow + 0x34 ]          002F8C73, 002F8C7A
esi += [ unit.rewardBaseRow     + 0x34 ]          002F8C7E, 002F8C85
```

```
if (ebp == 0) esi = 0                             002F8CEC
else          esi = (same expression) / ebp       002F8D1C-002F8D1F: cdq / idiv ebp
```

**Then the recipient's own modifiers, in this order and no other** (`002F8D26`–`002F8D40`):

```
002F911B  edx = corpse[+0x1C2] - corpse[+0x88]        ; both through dying unit ->+0x698
002F912B  edx *= byte [unit.rewardPerLevelRow + 0x2F] ; a BYTE, not the dword +0x34
002F9136  edx += byte [unit.rewardBaseRow    + 0x2F]
002F914B  if (recipient[+0x6B] & 0x10) || (recipient[+0x7B] & 0x10) edx += edx   ; double
002F9159  return edx
```

> **CORRECTED 2026-09-12 (`OPUS-CONTRA-LICENCE-PERCENTAGE`), and the error was mine, published the
> same morning.** This paragraph said the tail ends in `002F9180`'s `0x51EB851F` reciprocal — "the
> compiler's signed division by 100, so the licence award is a percentage". **`002F90C0` does not
> contain that instruction and never calls it.** The function's two returns are at `002F9165` and
> `002F9166`–`002F9172`, and `002F9173`–`002F917F` is `int3` padding; `002F9180` begins a **separate
> 21-byte function** ending at its own `ret` at `002F9194`, and a direct-reference sweep finds
> exactly one caller for it image-wide — `002FF090`, which is not this family. There is **no
> division in the licence award at all.**
>
> The shape of the mistake is worth keeping: the cited address was real, the instructions at it were
> exactly what the claim described, and they were in another function. An address is not a citation
> until its containing body is checked.


### From HEAD's 8. Script · resource · event interactions

Neither of the corpse's two inputs is read from authored data by this family, and neither is
authored directly. `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth`'s rebuild (`0030C470`)
zeroes the level at `0030C496` and then grows it, and stores its own third argument into `+0x88`
at `0030C4B1` on the kind-1 branch only. The authored row behind that rebuild sits at registry
slot `02EBF120` for enemies and `02EBF130` for party members; nothing in this family touches
either.


### From HEAD's 10. Failure paths and edge conditions

- **A NULL recipient is legal** and reaches the corpse checks (`002F8BCF` jumps past only the
  recipient block). It then returns whatever the corpse-side expression produces without any
  recipient modifier, because `002F8D21` tests `rdi` again before applying them.
- **The subtraction is unguarded**, see §7.
- **NEITHER REWARD ROW IS NULL-CHECKED HERE, AND BOTH CAN BE NULL.**
  `BattleUnit_ApplyUnitDefinition` writes NULL into them on its failure paths — `xor ecx, ecx`
  at `0023A9A3` and `0023A9EA`. This family then loads `+0xE78` at `002F8C73` and immediately does
  `imul esi, dword ptr [rax + 0x34]` at `002F8C7A`, with nothing between, so a NULL row faults at
  kill time and the failure surfaces far from its cause. **That half stands and was never the
  disputed one.**

**Added 2026-09-12 from `ASTRA-REQ-OPUS-NATIVE-REWARD-DECODE` / `EXP-076`**, which composed the
native decoder with the installer instead of scripting a resolver return. Three conditions had been
treated as one, and they are distinguishable in the instructions:

| condition | what actually happens |
|---|---|
| **the encoded reference is 0** | `0020E600` is `mov eax, ecx` / `add rax, [01F83530]` / `ret`, so it returns **the relocation base**. A zero reference is **not** a null row |
| **the decoded base is 0** | only then is a zero reference a zero address — and `EXP-002` observed the base reading 0 at the title screen, which is what makes the two look identical in practice |
| **the stored row is NULL** | either the store came from `0023A9A3`/`0023A9EA`, the descriptor-missing path above, **or** the 32-bit arithmetic below truncated a real address to zero |

```asm
0023A994  movzx edx, word ptr [rcx + 8]      ; stride, u16
0023A998  movzx ecx, word ptr [rsi + 0x22]   ; index, u16
0023A99C  imul  ecx, edx                     ; 32-bit
0023A99F  add   ecx, eax                     ; 32-bit, over the resolver's LOW 32 only
0023A9A5  mov   qword ptr [rdi + 0xE70], rcx ; stored zero-extended to 64
```

**An out-of-range index with a positive count is rejected EARLY, and no unit is built.** The
installer carries **four** bound guards of one shape, each `index > count − 1 → 0023A63A`, and
`0023A63A` is `xor eax, eax` followed by a jump to the epilogue — **return 0, before any store**:

**And the late NULL stores test the descriptor, not the index.** `0023A97C je 0023A9A3` follows a
`test rax, rax` on **the resolver's return value**, and the slot-null test above it jumps to the same
label. So `0023A9A3` and `0023A9EA` mean *the table is absent or its base did not resolve*, which is
a different failure with a different cause and a different fix.


### From HEAD's 12. Reproduction formula

```c
int Reward_ComputeExperienceForRecipient(BattleStatsRecord *rcp, BattleUnit *corpse)
{
    if (rcp) {
        if (rcp->kind != 0)                       return 0;   /* 002F8BD4 */
        if (!sub_31B860())                        return 0;
        if ((uint8_t)(rcp->id - 0x1B) <= 0x0C)    return 0;   /* 002F8BF2 */
        if ((rcp->w64 | rcp->w3C) & 0x80000003)   return 0;   /* 002F8C00 */
    }
    if (!corpse || !corpse->stats)                return 0;
    if (corpse->stats->kind != 1)                 return 0;   /* 002F8C2A */

    int v;
    if (sub_3135C0()) {
        if (rcp && rcp != sub_320AB0(sub_313800(), 1)) return 0;
        v = award(corpse);
    } else {
        int n = 0;
        for (int i = 0; i < 4; i++) {             /* 002F8C94-002F8CE5 */
            BattleUnit *m = sub_31B810(i);
            if (!m) continue;
            BattleStatsRecord *s = m->stats;
            if ((s->w64 | s->w3C) & 0x80000003) continue;
            if (s->kind == 0 && (uint8_t)(s->id - 0x1B) <= 0x0C) continue;
            n++;
        }
        if (n == 0) return 0;
        v = award(corpse) / n;                    /* SIGNED idiv */
    }
    if (rcp) {
        if ((rcp->b6B | rcp->b7B) & 0x08) v += v;
        if ((rcp->b6B | rcp->b7B) & 0x20) v  = 0;
    }
    return v;
}

static int award(BattleUnit *c)   /* 002F8C63-002F8C85 */
{
    int v = (uint8_t)c->stats->level - (uint8_t)c->stats->b88;  /* level - 1, observed */
    v *= *(int *)((char *)c->rewardPerLevelRow + 0x34);
    v += *(int *)((char *)c->rewardBaseRow     + 0x34);
    return v;
}
```


### From HEAD's 13. Runtime validation

> **One of those six has since been executed on its own — `0031B860`, 2026-09-18 (OPUS, EXP-101).**
> This paragraph stays as written because it records what *this* run stubbed, and that was true. What
> is no longer true is the implication that the stub's behaviour was a fixture choice. Three things
> that matter to a caller are now measured rather than chosen: **the match is a full qword** at
> `unit+0x698` (`cmp qword ptr [rax+0x698], rdi` at `0031B892`, so a low-32 comparison finds the
> wrong unit), **the pool count is re-read every iteration** rather than hoisted, and **there is no
> base-null guard** — the index is guarded on both sides and the base is not, so `base = 0` with a
> count above 1 faults at `0xF50 + 0x698`. Full reading in
> [`CONTRACT-auto-status-rebuild.md`](../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md)
> §13e.

- **The divided path's member filter is not the experience filter.** It rejects a kind-0 member
  whose id is `0x1A` **as well as** `0x1B`–`0x27` — the first of those is the *licence* filter's
  exclusion. Driven at `0x19`, `0x1A`, `0x1B`, `0x27` and `0x28`: a member with id `0x1A` is
  eligible for experience and is still not counted in the divisor.
- ~~**A kind-1 member is counted whatever its id**, because both filter arms test the kind byte first.~~ **CORRECTED 2026-09-18 (OPUS, from `EXP-090`): true of the arms, unreachable on the real chain.** The arms do test `+0x05` first, so *given* a kind-1 member they count it. But a member only reaches them through `BattleUnit_FindByDefinitionSelector` (`002367A0`), which compares the caller's id against **`word [stats+4]`** (`002367DF`), and that word is the encoded definition id whose **high byte is the kind** — so a kind-1 record's word is `>= 0x100`. The roster paths supply a **zero-extended byte**: eight of the eleven call sites are literally `movzx eax, byte ptr […]` then `movzx ecx, al` (e.g. `0031B841`–`0031B849`, `0032659D`–`003265A1`, `00328E3D`–`00328E42`), and the only special case is `0xFF → 0xFFFF` (`002367E3`–`002367EE`), which is kind `0xFF`, not kind 1. **A byte cannot equal a word `>= 0x100`, so the divided path can only count kind-0 members.** The old reading was reachable only by feeding a kind-1 member straight to the arms, which is what the scripted oracle did.
- **The negative pool is real and survives the divide**: a level-0 corpse with `+0x88` of 1 gives a
  negative base, and `idiv` carries the sign into the share.
- **Every refusal returns 0 and none says which**: all six are driven, and each returns the same
  answer a legitimate zero would.


### From HEAD's 14. Unresolved

- ~~What `003135C0`, `00313800`, `0031B860`, `00320AB0` and `00264150` decide. Their return values are
  used as gates here and their own semantics are not established.~~ **MEASURED by [`EXP-090`](../_experiments/EXP-090-reward-gate-exec.md)** (104/104 cases, 10/10 mutants, two stable runs), which reports all six gates' decision rules — `LGATE` a sign-extended byte at `0209A2A9`; `FIND` resolving stats→unit by a `[0208E6A0]`-count scan of `[0208E688] + i*0xF50` on `unit+0x698`; `SINGLE` as `0030D9A0() == 1` over the mode flags at `[[02EBF190]+0x5B04]`; `DESIG` the byte at `+0x5AD5` into a 9-slot low-byte `u16` scan at `+0x5A48`; `RESOLVE` bounding `byte <= 0x27` into `FRAME + 8 + b*0x1C8`; and `PARTY` gating via `00322C50` then `002367A0`. **Provenance, stated because it differs across the six:** `PARTY`'s rule is re-derived here from the bytes (§13); the other five are `EXP-090`'s measurements, cited rather than re-run.
- ~~`BattleUnit +0xE70` and `+0xE78`~~ — **fully resolved**: named by the store, derived by this
  contract's arithmetic (§3), and traced to registry slots `02EBF148` and `02EBF140` with the
  definition-row words that index them (§6). What the rows' own fields mean beyond `+0x34` is
  still open.
- Which statuses occupy bits 0, 1 and 31 of the `0x80000003` mask; the question is already open in
  `03-World-Area-Field`.
- Why the licence filter admits `0x1A` and `0x00`–`0x06` specifically.

**One scope note of my own.** The byte premise behind the kind-1 correction holds on the roster
paths, which are the ones this contract uses. It is **not** universal across `002367A0`'s eleven
callers: two locomotion sites pass `lea ecx, [reg - 0x4026]` / `[reg - 0x4129]`
(`00312970`, `00312C05`), order-goal codes biased down to a small index, and I did not establish
their upper bound. They belong to `BattleLocomotion_DecodeOrderGoal`, not to any award path.


### From HEAD's 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| both functions are pure and write nothing | no store to any record field on any path of either body `002F8BB0`/`002F90C0` | 1 (isolated original-code) | PROVEN |
| a zero return means both "nothing owed" and "not eligible" | the six ways out in §10 all return `eax = 0` and none of them reports which | 1 (isolated original-code) | PROVEN |
| the recipient must be kind 0 and the corpse kind 1 | the `+0x05` tests in both bodies, against the declared discriminator: `002F8BD4`/`002F8C2A` (experience) and `002F90E2`/`002F9115` (licence) | 1 (isolated original-code) | PROVEN |
| the status mask 0x80000003 gates both awards | `(stats[+0x64] \| stats[+0x3C]) & 0x80000003` must be zero — `test eax, 0x80000003` at `002F8C06`/`002F8CAD` and `002F90FD`; the same mask and conjunction as the field-record action gate, a third subsystem using it | 1 (isolated original-code) | PROVEN |
| the two id filters are different, and licence is the narrower | experience rejects `0x1B`–`0x27` (`002F8BF2`–`002F8BFA`); licence admits only `0x00`–`0x06`, `0x1A` and `0x28` upward (`002F90E7`–`002F90F5`) | 1 (isolated original-code) | PROVEN |
| the reward rows supply a per-level multiplier and an addend, both at their +0x34 | `002F8C73`–`002F8C85` multiplies by `[+0xE78 + 0x34]` and adds `[+0xE70 + 0x34]`; this is what upgrades the two row names from propagated to derived | 1 (isolated original-code) | PROVEN |
| the base is the corpse's level minus the byte the rebuild stored at +0x88 | **both operands are the CORPSE's**, bound at `002F8BC9 mov r14, rdx` (the dying unit) and read through `002F8C5C mov rax, [r14+0x698]` as `002F8C63 movzx esi, [rax+0x1c2]` and `002F8C6A movzx eax, [rax+0x88]`; the recipient pointer `rdi` is not read again after the eligibility filters. `+0x1C2` is the declared level `[0, 99]` and `+0x88` the union's enemy arm, observed as `1`. An earlier revision called `+0x1C2` an "award base" and was corrected; a page published 2026-09-12 calls it the **recipient's** level, which is `OPUS-CONTRA-FABLE-REWARD-LEVEL` | 1 (isolated original-code) | PROVEN |
| both reward row pointers may be NULL and neither function checks them | no null test stands between the loads `002F8C73`/`002F8C7E` (and `002F8D07`/`002F8D12`) or `002F912B`/`002F9136` and the indexed reads of `+0xE70`/`+0xE78` | 1 (isolated original-code) | PROVEN |
| a NULL row comes from an ABSENT descriptor or a failed resolution, not from an out-of-range index | `0023A97C je 0023A9A3` follows `test rax,rax` on the resolver's return; the four bound guards at `0023A6BB`/`0023A726`/`0023A747`/`0023A768` reject an out-of-range index into `0023A63A`, which returns 0 before any store. Executed — `EXP-075` drove the whole installer in 14 fixtures and both private guard mutations were detected. **Corrects this contract's own earlier causal claim** | 1 (isolated original-code) | PROVEN |
| a zero ENCODED reference decodes to the relocation base, not to NULL | `0020E600` is `mov eax,ecx` / `add rax,[01F83530]` / `ret`, three instructions read whole. Executed — `EXP-076` composes the native decoder with the installer and its zero-sentinel mutation was detected | 1 (isolated original-code) | PROVEN |
| the stored row pointer is built in 32-BIT arithmetic and zero-extended, so a base above 4 GiB truncates and a non-zero base can store exactly NULL | `0023A99C imul ecx, edx`, `0023A99F add ecx, eax`, `0023A9A5 mov [rdi+0xE70], rcx`. Executed — `EXP-076` drives base `0x100000000` with reference 0 and index 0 as its own control | 1 (isolated original-code) | PROVEN |
| three of the four bound guards are UNSIGNED and one is SIGNED, so a zero count is the only case an index passes | `ja` at `0023A6BB`, `0023A747`, `0023A768` against `jg` at `0023A726`; `dec ecx` on 0 gives `0xFFFFFFFF` | 1 (isolated original-code) | PROVEN |
| the divided path uses a SIGNED divide over a subtraction that can go negative | `cdq` / `idiv ebp` at `002F8D1C`–`002F8D1F`; `level - 1` is `-1` for a level-0 corpse and the rebuild writes level 0 at `0030C496` before growth. Nothing clamps it | 1 (isolated original-code) | PROVEN |
| whether a level-0 unit can be alive at kill time is unknown | that is what decides whether the negative path is reachable — one observation, §13 | none | UNKNOWN |
| the doubling happens after the division, and zero wins over double | `002F8D26`–`002F8D40`, in that order: double adds, then zero assigns | 1 (isolated original-code) | PROVEN |
| either modifier bank carries the effect alone | the two banks `+0x6B` and `+0x7B` are tested with OR — `002F8D2A`/`002F8D2E` and `002F8D36`/`002F8D3A` in `002F8BB0`, `002F914B`/`002F9151` in `002F90C0` | 1 (isolated original-code) | PROVEN |
| licence points are gated globally before any argument is examined | `00264150` at the top of `002F90C0`: a non-zero return means 0 | 1 (isolated original-code) | PROVEN |
| the licence award reads +0x2F of both reward rows and doubles on bit 0x10, with no division anywhere | `002F912B`–`002F9157`. **This row said the award was a percentage truncated toward zero, citing `002F9183`** — an instruction in a separate 21-byte function that begins after this one's `int3` padding and is called only from `002FF090`. Corrected 2026-09-12, `OPUS-CONTRA-LICENCE-PERCENTAGE` | 1 (isolated original-code) | PROVEN |
| the divided path's member filter rejects id 0x1A as well as 0x1B-0x27 | `002F8CB9`–`002F8CDC`: two arms, both testing the kind byte first, the second excluding `0x1A` — which is the LICENCE filter's exclusion, not the experience one this contract names. Executed at `0x19`, `0x1A`, `0x1B`, `0x27` and `0x28` | 1 (isolated original-code) | PROVEN |
| ~~a kind-1 party member is counted whatever its id~~ **the divided path can only count kind-0 members** | the arms do test `+0x05` first (`002F8CB9`, `002F8CD0`) — but the selector `002367A0` compares a **byte** id against `word [stats+4]` (`002367DF`), whose high byte is the kind, so a kind-1 record's word is `>= 0x100` and never matches. The old row's evidence, *"Executed with a kind-1 member carrying `0x1A`"*, is the scripted oracle feeding the arms directly | 1 (isolated original-code, `EXP-090`; selector re-derived by OPUS) | PROVEN |
| the level operand is the CORPSE's, not the recipient's | `002F8BC9 mov r14, rdx` binds the dying unit and `002F8C5C` reads through **its** `+0x698`. Executed with the two levels deliberately different on every case; the control reading the recipient's failed on all 265 lines and could not even complete, because the recipient may be NULL where the corpse may not. Resolves `OPUS-CONTRA-FABLE-REWARD-LEVEL` | 1 (isolated original-code) | PROVEN |
| nothing observed at runtime | — see §13 | none | UNKNOWN |
