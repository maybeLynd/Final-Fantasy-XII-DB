---
system: How experience is computed and divided
category: 13-Rewards-Progression-Economy
status: PARTIAL — edge-state reachability (GR-18) partial; owner re-status 2026-10-02 (FABLE) from REOPENED: the reopening is resolved, SECTION-03 independently accepted with a narrowing 2026-10-01 (SWE2-AUDIT-SEM, auditsem-review-section03-1001, GR-16, N1); documented_rule reads PARTIAL on live GR-18, whose case (c) is this function's; graph audit 0 findings (_index/candidates/rewards-restatus-fable-1002); converted to a function note of the award page 2026-09-30 (FABLE)
note_kind: function
parent: experience-and-license-point-award.md
owner_layer: PrimaryOwner:Rewards_Progression_Economy
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: "additive-annotation across GN159 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN159 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30"
    verified: "re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS"
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-22
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: true
  reopened_count: 0
production_review:
  section: SECTION-03
  status: locally validated; independently accepted with a narrowing 2026-10-01 (SWE2-AUDIT-SEM, auditsem-review-section03-1001, GR-16, N1)
  scope: original reward consumers, selected caller instructions and retained binding observations
  new_live_session: false

---

# How experience is computed and divided

> **SECTION-03 production review, 2026-09-22; ~~independent peer acceptance pending~~** (registered as GR-16, 2026-09-30). *(OPUS, 2026-10-01: independently accepted with a narrowing 2026-10-01 (SWE2-AUDIT-SEM, [review](../_index/candidates/auditsem-review-section03-1001/REVIEW.md), GR-16; N1: `run_review.py` reproduces against the pinned pre-image of the reward-binding checker, and the sealed checker agrees with the preserved observation).)*
> Corrected against original EXE instructions, 71 bounded native controls and independent review
> of four retained EXP-081 samples. The historical audit/provenance metadata below/above is not
> a new audit pass. No new live game session or complete defeat-orchestrator execution was performed.
> [Evidence, changed claims and limitations](../_experiments/evidence/continuation-section03-reward-bindings/REVIEW.md).

`Reward_ComputeExperienceForRecipient` is **`002F8BB0`**, 430 bytes. Each invocation recomputes its
result. The same body is used for nonnull recipients and for the caller's NULL-recipient
presentation input; **NULL is not an unconditional undivided-total request**.

## Scope (FABLE, 2026-09-30)

*(Note structure added 2026-09-30 (FABLE), under the NOTE template: this page is SECTION-03's production-review
rewrite of one function, so it carries evidence for a parent rather than being the system write-up.)*

This note establishes what the experience computer `002F8BB0` returns, and why, for every input the defeat caller
gives it. That covers its gates, its two modes, its four-slot divisor, its modifiers, and what a NULL recipient
changes. The player view, the key-address table, the call chain and the modding notes live on the parent,
[Experience and License Point award](experience-and-license-point-award.md). The defeat sequence that calls this
function is [what happens when an enemy dies](what-happens-when-an-enemy-dies.md). The licence-point computer is
compared here only where it differs.

## Findings (FABLE, 2026-09-30)

The body was read whole (430 bytes, `0x1AE`: the function table's extent, ending in the `ret` at `002F8D5D`). Its
answer is `(level − baseline) × perLevelRow[+0x34] + baseRow[+0x34]`, taken from the defeated unit. In shared mode
that is divided by the number of passing members among exactly four lookup slots. In designated mode it is paid
whole to the one designated member. Recipient modifiers double it or zero it. Each subsection below gives its
instruction anchors.

### Original arithmetic (FABLE, 2026-09-30)

```asm
002F8CF7  movzx eax, byte ptr [rcx+0x1C2]  ; current subject level
002F8CFE  movzx ecx, byte ptr [rcx+0x88]   ; current baseline
002F8D05  sub   eax, ecx
002F8D07  mov   rcx, qword ptr [r14+0xE78]
002F8D0E  imul  eax, dword ptr [rcx+0x34]
002F8D12  mov   rcx, qword ptr [r14+0xE70]
002F8D19  add   eax, dword ptr [rcx+0x34]
002F8D1C  cdq
002F8D1D  idiv  ebp
```

The shared branch computes `(level-baseline)*perLevel+base` in 32-bit width, then performs signed
division by the eligible-slot count. `+0x1C2` and `+0x88` are **0x13A bytes apart**; the two
load instruction starts are seven bytes apart. Those are different measurements.

The undivided branch uses the same expression but is selected by the current mode, not by NULL.
The consumer does not replace the current baseline with constant 1. The 1 is what the enemy branch of `BattleStats_InitializeDefinitionRecord` supplies (`0023AD37`, `mov edx, 1`), and the grower stores it at `+0x88` (`0030C4B1`); this computer reads whatever the byte holds *(address restored 2026-09-25, FABLE, Claude Opus 5.5)*. Negative synthetic inputs are
not clamped here; `-9 / 2` returns `-4`. The caller's payout caps are another operation.

### Gates and exactly four candidate slots (FABLE, 2026-09-30)

A nonnull recipient needs kind 0, an owning unit, ID outside `0x1B..0x27`, and a clear
`(status[+0x3C] OR status[+0x64]) & 0x80000003`. NULL skips those recipient checks. Both cases
require a subject with nonnull stats of kind 1 before entering the mode-specific path.
*(Anchors added 2026-09-30 (FABLE):* kind 0 `002F8BD4`–`002F8BD8`; owning unit `002F8BDE`–`002F8BE6`, through
`BattleStats_FindOwningBattleUnit`; ID `002F8BF2`–`002F8BFA`; status mask `002F8C00`–`002F8C0B`; NULL goes straight to
the subject checks, `002F8BCF`–`002F8BD2` to `002F8C11`; subject and stats kind 1, `002F8C11`–`002F8C2E`. Each
failure jumps to the zero return at `002F8D46`.*)*

When `003135C0()` is zero, the original loop reads **exactly four** `0031B810(i)` results (`002F8CE0 inc ebx` / `002F8CE2 cmp ebx, 4`). Its
member filter omits masked records and kind-0 IDs `0x1A` (`002F8CD8`) and `0x1B..0x27` (`002F8CC5`, `sub al, 0x1b` / `cmp al, 0xc` / `jbe`). A fifth candidate in
the defeat caller is not a fifth iteration of this loop. With zero passing members it returns 0
before row dereferences/division (`002F8CEC test ebp, ebp` / `je`) *(address restored 2026-09-25, FABLE, Claude Opus 5.5)*.

Ordinary selector-byte lookup cannot select a kind-1 identity word. However the special `0xFF`
selector can match `0xFFFF` when its bounds descriptor permits it. SECTION-03 executes that
synthetic case through the original lookup; it does not claim such a unit is normally created.

### Designated mode and NULL recipients (FABLE, 2026-09-30)

When `003135C0()` is nonzero, `00313800()` supplies the designated index. A **nonnull** recipient
must match `00320AB0(index,1)`. NULL skips that comparison, but does not alter the mode itself.
The linked [award page](experience-and-license-point-award.md) preserves the prior summoner/Esper
interpretation and its asset references; the new controls establish numeric behavior.

| Synthetic state, raw amount 19 | Original EXP result |
|---|---:|
| Shared mode, NULL, 0 passing slots | 0 |
| Shared mode, NULL, 1 passing slot | 19 |
| Shared mode, NULL, 2 passing slots | 9 |
| Shared mode, NULL, 3 passing slots | 6 |
| Shared mode, NULL, 4 passing slots | 4 |
| Designated mode, NULL | 19 |
| Shared mode, doubled nonnull recipient, 2 slots | 18 |

Thus neither "computed once" nor "total remains constant" is guaranteed. Rounding discards the
remainder; recipient modifiers, admission, and state changes can alter the accumulated sum.

### Recipient modifiers (FABLE, 2026-09-30)

For a nonnull recipient, bit `0x08` in either `+0x6B` or `+0x7B` doubles the computed result (`002F8D34`, `add esi, esi`).
Bit `0x20` then zeros it and wins over doubling: it is tested afterwards (`002F8D36`) and writes 0 (`002F8D40`) *(address restored 2026-09-25, FABLE, Claude Opus 5.5)*. NULL skips both. These bytes belong to effect
layers; they are not the status words used by the earlier mask test.

LP is not this algorithm with narrower row fields. It has no owner lookup, designated mode, or
four-slot divisor, has a separate global gate, and doubles on `0x10`. See the
[shared EXP/LP contract](CONTRACT-experience-and-licence-award.md).
*(Anchors added 2026-09-30 (FABLE), `002F90C0` read whole, 179 bytes:* the global gate is its first call, `00264150`,
which returns the signed byte `0209A2A9`; any nonzero value returns 0 (`002F90D0`–`002F90D7`). The row reads are the
unsigned bytes `+0x2F` (`002F912B`–`002F9144`). The doubling is `002F914B`–`002F9157`, on the effect-layer bytes
`+0x6B` / `+0x7B`, bit `0x10`: effect id 28.*)*

### Caller and retained observations (FABLE, 2026-09-30)

The defeat caller passes NULL at `003124BC/003124C6`, then applies fresh caps and an additional
EXP suppression flag before `0028FB80`. In shared mode its recomputed EXP input is still divided.
The old September3 conclusion that zeroing ECX proves an undivided display is **withdrawn**.
Only call-boundary semantics are established here, not rendering or a fresh gameplay payout.

EXP-081 retained field captures bind the subject's working stats and reward pointers, but capture
no actual reward header or coefficient-row bytes. The observed pointer spacing is only consistent
with the producer layout; it does not reveal coefficient values or prove lifetime.

## Evidence (FABLE, 2026-09-30)

SECTION-03's original-instruction controls, mutants, raw-byte review and exact provenance are in
the [review](../_experiments/evidence/continuation-section03-reward-bindings/REVIEW.md). Earlier audit metadata and the crossings below remain historical.
Fresh game-session evidence, complete orchestration and peer acceptance remain separate.
*(Table added 2026-09-30 (FABLE); on the last sentence, see Limits.)*

| claim | evidence | tier |
|---|---|---|
| `002F8BB0` is 430 bytes and recomputes on each call | the function table's extent `0x1AE`; body read whole, no store to a record (the contract's §15a purity measurement) | 1 |
| shared result `((level − baseline) × perLevel + base) / n`, 32-bit, signed division | `002F8CF0`–`002F8D1F` | 1 |
| designated result undivided | `002F8C5C`–`002F8C88` | 1 |
| nonnull recipient gates; NULL skips them | `002F8BCF`–`002F8C0B` (anchors under Gates) | 1 |
| subject must be a kind-1 stats record | `002F8C11`–`002F8C2E` | 1 |
| exactly four slots; `0x1A` and `0x1B..0x27` not counted; zero members returns 0 before any row read | `002F8C94`–`002F8CE5`, `002F8CD8`, `002F8CC5`–`002F8CC9`, `002F8CEC`–`002F8CEE` | 1 |
| mode chosen by `003135C0`, not by NULL; designated equality for a nonnull recipient | `002F8C34`–`002F8C56` | 1 |
| `0x08` doubles, `0x20` zeroes and wins; NULL skips both | `002F8D21`–`002F8D40` | 1 |
| LP's different gate, widths and doubling | `002F90C0` read whole (anchors under Recipient modifiers) | 1 |
| the synthetic numeric table (raw 19 across modes and member counts) | SECTION-03 `native_controls.c`, running the original bytes at the preferred base; six code mutants rejected | 1 (original instructions executed) |
| the defeat caller passes NULL to both computers | `003124BC`, `003124C6` (`xor ecx, ecx`) | 1 |
| retained EXP-081 bindings carry no reward-row bytes | SECTION-03's independent reduction of 88 retained spans | 10 (historical capture) |

## Method (FABLE, 2026-09-30)

- **The body.** Disassemble `002F8BB0` over its function-table extent in the certified image (`exe_sha256` above, image
  base `0x00120000`). Each claim above names its instruction range.
- **The native controls.** Run the SECTION-03 driver from its evidence directory, as the
  [review](../_experiments/evidence/continuation-section03-reward-bindings/REVIEW.md) §7 gives it: `python run_review.py
  --exe … --database … --output …`, under Python 3.10+, Linux x86-64 and GCC (WSL works). It pins 24 original bodies by
  hash before running the 71 controls.
- **Positive control.** The six rejected code variants, for example "skip XP division" and "only three roster slots",
  must each fail a control, which shows the controls can see the change they test.
- **Extent read.** `002F8BB0` whole, and `002F90C0` whole for the comparison. The callees `0031B810`, `003135C0`,
  `00313800` and `00320AB0` are executed by the controls and read on the parent.

## Limits (FABLE, 2026-09-30)

*(Section added 2026-09-30 (FABLE); it replaces the last sentence of Evidence as the statement of what stays open.)*

- **Peer acceptance:** SECTION-03 has the owner's review
  ([`section03-owner-review.md`](../_index/candidates/section03-owner-review.md)) ~~but no independent auditor~~
  ~~verdict. That is GR-16.~~ *(answered: see the banner at the top — independently accepted with a narrowing 2026-10-01, SWE2-AUDIT-SEM, GR-16; 2026-10-02, OPUS)*
- **Complete orchestration:** the whole defeat body is now read statically on
  [what happens when an enemy dies](what-happens-when-an-enemy-dies.md). No run executed it end to end.
- **Fresh game-session evidence:** none. The claims above are tier-1 static, and the native controls ran the original
  instructions, so a live payout would re-observe them rather than settle anything. None is queued.
- **Rendering:** out of scope for this note. This function returns a number, and `0028FB80`'s presentation arms
  belong to the parent's call chain.
- **Reachability of the synthetic edge states** (zero-count descriptors, level-zero rewards, the `0xFF` selector case):
  GR-18, on the parent.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

`BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`) and the 24-byte mode test `003135C0` are shared lookups:

- **Movement — CLIENT.** `0031B810` is read by `PartyFollow_SolveFormation` and two locomotion bodies (181 B and
  1,028 B). `003135C0` is read by `PartyFollow_SolveFormation` and a 668-byte body.
- **ActorEntity — SERVICE.** `Reward_ComputeExperienceForRecipient` (`002F8BB0`) maps a definition selector
  (`BattleUnit_FindMappedDefinitionSelectorByIndex`), and `0031B810` in turn asks `BattleUnit_FindByDefinitionSelector`.
- **Presentation — CLIENT.** `PartyCombat_UpdateStanceState` and `BattleUnit_BroadcastPartyCombatTargetRelatio…` read
  `0031B810`.
- **Spawn_Encounter_Lifecycle — CLIENT.** `SpawnLifecycle_CheckAndRetireByNativeRange` and
  `Spawn_ValidateCandidateDistanceToPlayers` read `0031B810`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `AiOrder_EvaluateTargetSelector`, owned by that layer, calls `0031B810` on this page. That caller is the selector evaluation, 6,963 bytes of it: it indexes its table at a **six-byte stride** and takes a word at `+6`, two bytes at `+8` and `+9` and a signed word at `+0xA` before deciding anything; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `FUN_00388d50`, owned by that layer, calls `0031B810` on this page. That caller is a 298-byte target predicate made on the same two-table resolution as the effective-action-id query - `byte[+5] == 0` indexes the `0x40`-byte rows at `0208D480` by `byte[+4]`, anything else the rows at `0208DE80` by the owning unit's `byte[+0xEA9]` - which it then compares against the handle in the unit's `dword[+0x710]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT.** `BattleMenu_BuildCommandEntryList`, owned by that layer, calls `003135C0` on this page. That caller is the command-list build, and the ceiling is in the first instruction: the menu kind is bounded at **`0x22`** into a jump table, after which `dword[+0x40]` is zeroed and `dword[+0x44]` set to `-1` before any entry is written; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Gameplay — SERVICE and CLIENT (5 edges).** The mode test `003135C0` calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0` and answers whether that mode is 1; `BattleUnit_FindMappedDefinitionSelectorByIndex` `0031B810` calls the id validator `BattleEncodedId_IsValidForClass` `00322C50` and is called by the four-slot cleanup `00234150` and `BattleUnit_CollectMappedFourSlotUnitsByFlags` `0030A8A0`; `BattleStats_GetByMappedBattleSlot` `00320AB0` calls `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0`. The experience split's two gates are built on that layer's battle-mode query and slot map, and the same slot lookups are shared with that layer's four-slot walkers.

**Items_Equipment_Shops_License — CLIENT (6 edges).** `Inventory_QueryOwnedCountIncludingReservedActionItems` `00309FB0` calls `0031B810`; `Equipment_BuildRecommendedLoadoutForMappedStats` `002F9F20`, `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` `0030A4E0`, `InventoryEquipment_RestoreTemporarySnapshotAndClearBackup` `0030FAA0`, `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` and `Equipment_UnequipEncodedItemFromActiveRoster` `0030FD10` call `00320AB0`. The inventory and equipment code resolves party members through the same slot lookups the experience loop uses; nothing there touches the experience split.

**Party — CLIENT (2 edges).** `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040` calls `003135C0`, and the main-member collector `00304180` calls `00320AB0`. The party code asks the same mode-1 question and uses the same mapped-slot lookup; it shares the lookups, not the award.

**Script_VM_Native_Bridge — CLIENT (7 edges).** The verb handlers `0050FD00`, `0050FD50`, `0050FDD0`, `0050FE20`, `0050FE80`, `0050FED0` and `0050FF20` call `00320AB0`. Script verbs read a party member's stats record through the lookup: `0050FD00` (read) pops a slot number, looks the record up and pushes its byte `+4`, or -1 when there is none; `0050FF20` is the five-outcome record classifier the actor-type page cites; the other five handlers are not read here.

**Status_Periodic_Terminal — CLIENT (1 edge).** The periodic tick `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls `00320AB0`. The tick resolves a mapped slot's stats record through the same lookup.

**WorldAreaField — CLIENT (1 edge).** `BattleSystem_RunFieldFrameOrchestrator` `00234590` calls `003135C0`. The field-frame orchestrator asks the same mode-1 question; it is another consumer of the test, not part of the experience split.
