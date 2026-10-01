---
contract: Pay out a kill — local sequencing and mode-dependent presentation inputs
category: 13-Rewards-Progression-Economy
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md
entries: ["00312280"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — the 857-byte body read in control-flow order, all four caps located by their
    immediates, the display calls' argument registers read at their instructions, the level walk's
    loop bound and its callee resolved, the conversion's multiply decomposed, and **the gil path
    followed from its own clamp through the setter to the second reporter**. **This records checks
    performed on that date, not the method of the original derivation**, which is on the death page;
    see §15.
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-30
  last_pass_kind: falsification
  last_pass_state: opus-defeat-rewards-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
production_review:
  section: SECTION-03
  status: locally validated; peer acceptance pending
  scope: original reward consumers, selected caller instructions and retained binding observations
  new_live_session: false

---

# Contract — the defeat rewards sequence

> **SECTION-03 production review, 2026-09-22; independent peer acceptance pending.**
> Corrected against original EXE instructions, 71 bounded native controls and independent review
> of four retained EXP-081 samples. The historical audit/provenance metadata below/above is not
> a new audit pass. No new live game session or complete defeat-orchestrator execution was performed.
> [Evidence, changed claims and limitations](../_experiments/evidence/continuation-section03-reward-bindings/REVIEW.md).

> **Authored 2026-09-22 by FABLE.** S-32's binding gap is *"EXP/LP division only, of 5 pages"*. The
> loot rolls were taken at `8cfdf3851` and the gil paths at `68135b186`; **this takes the death
> sequence.** The level-up page remains uncontracted and this document does not claim it.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is six
> such invariants. SECTION-03 corrects DR-2 and DR-6: they require following both caller and
> callee, but the earlier undivided-NULL and differing-delta deductions were false.

## 1. Purpose

Turn one dead enemy into experience, licence points, levels, money and an item, for everyone who
qualifies.

## 2. Interface

**One body does all of it.** `00312280`, **857 B**. *It carries two names in the database* — the
function table and [the loot page](loot-drops-and-enemy-chain.md) call it
`BattleUnit_ProcessDefeatRewardsAndLoot`, while [the death page](what-happens-when-an-enemy-dies.md)
calls it `…AndRetire`. **One body.** ~~and both names describe part of it~~ `…AndLoot` is the
function table's name; `…AndRetire` is a misnomer — the body retires nothing (its last calls are
`00317090`, an achievement counter, and the cookie check; `pkg-gp-hp-lethal/hp_lethal_checks.py` R).

## 3. Types

```
recipient (BattleStats)
  +0x069 / +0x079  u8   the two status layers; bit 4 of byte 1 is status id 12 (DR-5)
  +0x18C           i32  accumulated experience
  +0x1C2           u8   the level -- read by the walk and by DR-5 (00312415); ~~AND by the gil term~~
                        (corrected 2026-09-25: the gil term reads the DEFEATED unit's level, below)

defeated unit
  +0x698  ptr  its stats record; the gil term reads its +0x1C2 (the level) minus +0x88
               (0031251D-00312532, corrected 2026-09-25)
  +0xE70  ptr  the FLAT-TERM table   \  gil at +0x30, experience at +0x34 (DR-4)
  +0xE78  ptr  the MULTIPLIER table  /
  (set once by the unit install: +0xE70 = the row of table [02EBF148] indexed by definition +0x22,
   +0xE78 = the row of table [02EBF140] indexed by definition +0x24; 0023A965-0023A9F4, added 2026-09-25)
```

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**DR-1 — Local orchestration order, not a global non-reentrancy proof.** Build the recipient
list → per recipient compute, clamp, award, re-derive level, notify → recompute presentation
inputs with NULL recipients → gil → item placement → retirement. The visible order in this
body is established. Callback re-entry and every external consequence have not been excluded.
**One external consequence is now named** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 344](../_index/candidates/s32-opus-replay-defeat-rewards/README.md), which executed it 6/6; `0031251D`–`00312546`, `0023A965`–`0023A9F4` and the level advance's event post re-read.)*. Inside the recipient loop, when the level advance
changes a party-class record's level, it posts **event 4** carrying the record and its new level. The advance
tests `+0x05 == 0` and calls a 68-byte poster, which loads `+0x1C2` and hands the event to a shared post routine
(`0030C7D3`–`0030C7E4`). *Who consumes event 4 is not traced here.*

**DR-2 — NULL removes recipient-specific checks/modifiers, not shared EXP division.** After the
loop at `003124AE`, the body zeroes ECX at `003124BC` and `003124C6` for calls to `002F8BB0`
and `002F90C0`. The EXP callee still selects its branch through `003135C0`: in shared mode it
counts exactly four lookup slots and divides if the count is positive. LP has no corresponding
division or designated-mode gate. The caller clamps the fresh results and additionally suppresses
EXP via the flag tested at `00312505/00312513` before `0028FB80`.

A synthetic raw award 19 with two passing slots returns `EXP(NULL)=9` and `LP(NULL)=19`; an
EXP-doubled recipient gets 18 while NULL still gets 9. The designated-mode NULL result is 19.
These are native consumer checks plus static caller-argument checks, **not a fresh observed
on-screen payout**. The presentation value can equal or differ from an individual's gain.

**DR-3 — Levelling is a SEARCH, not an increment.** The walk reads the level at `+0x1C2` and the
accumulated experience at `+0x18C` and steps while the next threshold is reachable
(`00312432`–`00312460`), then calls
`BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`003124A3`). *So one kill can raise a
character several levels in a single step; a threshold table returning zero terminates the walk; and
the callee re-derives growth rather than merely storing a number.*

**DR-4 — Gil and experience read the SAME two tables, four bytes apart.** The gil term is
`[unit + 0xE78] + 0x30` as multiplier and `[unit + 0xE70] + 0x30` as flat term (`0031253B`,
`00312546`). **What it multiplies is the DEFEATED unit's level span** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 344](../_index/candidates/s32-opus-replay-defeat-rewards/README.md), which executed it 6/6; `0031251D`–`00312546`, `0023A965`–`0023A9F4` and the level advance's event post re-read.)*: gil =
`(defeated.stats[+0x1C2] − defeated.stats[+0x88]) × mult + flat + (a term carried from earlier in the body)`,
added to the party's gil and floored at 0. OPUS measured `8 + 3 × span`: 8, 23 and 23 at spans 0, 5 and 5, with
recipients at levels 10, 10 and 50. So **the recipients' levels do not enter gil**, except through DR-5. The two
rows are the definition's rows in two authored tables, set once at install (§3). 1,004 of the 1,146 shipped `in/`
area definitions have both gil terms zero; the experience formula uses `+0x34` of the same two records. *Identical shape, identical
inputs, one field apart — which is what makes `+0x30` gil and `+0x34` experience rather than a
guess.*

**DR-5 — Status id 12 CONVERTS a recipient's licence points into party gil, and it is not a bonus.**
When bit 4 is set in either status layer (`00312409`, `0031240F`), the body computes
`level × LP` and adds **five times** it to the gil accumulator — as `x + 4x`, via
`lea eax, [r12 + rcx]` then `lea r12d, [rax + rcx*4]` (`00312421`, `00312425`) — and **replaces the
recipient's LP with zero**, so that recipient receives none. The converted amount lands in the same
accumulator the gil award uses (`00312549`). *So one character's status changes what the whole party
is paid.*

**DR-6 — Two reporting paths can both exceed the stored gain; a cap does not make their
arithmetic deltas different.** The caller forms `requested = max(signed32(old + award), 0)`
at `00312553`–`00312558` (`00312556 test edx, edx` / `00312558 cmovns`), and passes requested to the setter at `0031255D`. `00254EE0` computes
`requested - current` before its own clamp to `[0, 99,999,999]`. It routes a positive magnitude
to the increase meter, the negated magnitude of a negative delta to the decrease meter, or skips a zero delta.
The caller then computes `requested - old` at `00312562` and calls `00469E80`.

With no intervening balance change between those reads, both arithmetic differences are the
same. The caller does **not** reload the upper-capped stored total before reporting. For old
99,999,995 and award 10, both differences are 10 but stored gain is 4. For old 5 and award -10,
requested is already zero: the setter meters a spend of 5 and the notifier receives -5.
The notifier dispatches event `0x26` only for a positive argument; it is not a second ledger.

These conclusions follow the original caller, setter and notifier instructions. No full gil
orchestration/event runtime is executed by SECTION-03, and no global non-interference or
subscriber-side interpretation is asserted.

## 5. State

**Owned:** nothing persistent. **Written:** each recipient's experience, licence points and level;
the party's gil, through the setter. **Read, never written:** the two reward tables and the
recipient status layers.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-experience-and-licence-award.md`](CONTRACT-experience-and-licence-award.md) — the distinct EXP/LP gates and mode-dependent NULL calls in DR-2 |
| **Sibling** | [`CONTRACT-loot-rolls-and-the-chain.md`](CONTRACT-loot-rolls-and-the-chain.md) — the drop this sequence places |
| **Calls** | [`CONTRACT-gil-storage-and-movement.md`](CONTRACT-gil-storage-and-movement.md) — DR-6 compares requested, metered, notified and actually stored values |
| **Uncontracted** | the level-up page — S-32's last, not claimed here |

## 7. State transitions

*recipients → per recipient: award, clamp, walk the level table, notify → fresh mode-dependent presentation inputs → gil
(floor, set, report) → drop → retire.* A recipient transitions level once per kill, by a walk rather
than a step (DR-3).

## 8. Script · resource · event interactions

The two reward tables and the experience-threshold table are authored. Nothing here is scripted.

## 9. Determinism

The inspected reward arithmetic is deterministic for fixed inputs. The drop path has its own
[loot contract](CONTRACT-loot-rolls-and-the-chain.md), including `LC-4`. SECTION-03 has not ruled
out randomness or state changes inside every growth/event/drop dependency, so the old universal
"only randomness a kill involves" sentence is not retained as a proved invariant.

## 10. Failure paths and edge conditions

- Every clamp is two-sided: a negative computed award is written as **0**, not as itself.
- The caps are `999,999` experience and `999` LP per award, `99,999,999` and `99,999` accumulated
  (`003123ED`, `003123FF`, `00312438`, `0031247C`) — and the per-award cap is applied **again**
  before the display call (`003124B4`).
- A recipient carrying status 12 receives **no** licence points at all (DR-5).

## 11. Observable behaviour

The published EXP input is a fresh mode-dependent computation without recipient modifiers; it
is not universally an undivided total or different from every recipient's gain. This review does
not follow the rendering beyond the call boundary. The inherited status-12 conversion path
replaces that recipient's LP with its gil contribution (DR-5).

## 12. Reproduction formula

With fixed synthetic raw values 19 and two passing roster slots, assert NULL EXP 9 and LP 19,
then EXP 18 for a doubled recipient and NULL EXP 19 in designated mode. These controls are in
SECTION-03. A future full-path test must also account for caps, field-flag suppression and
presentation/event consumers rather than equating a computed return with an observed display.

DR-3/DR-5 still need their own complete-path acceptance. For the static DR-6 upper-bound example,
old 99,999,995 plus award 10 predicts equal pre-cap differences 10 and stored gain 4, not two
different reporting deltas. Test subscriber behavior separately from argument arithmetic.

## 13. Runtime validation

**Superseded in part 2026-09-25:** [OPUS block 344](../_index/candidates/s32-opus-replay-defeat-rewards/README.md) executed the defeat sequence (6/6), including the gil term and the
level advance's event post. The evidence class is native replay, not live. The paragraph below is kept as history.

**No complete execution of `00312280` is supplied by SECTION-03.** The new 71 original-instruction
controls execute its EXP/LP consumers and their real gate closure under synthetic state. The
caller, gil setter and notifier are inspected statically; EXP-081 is retained historical live
observation of bindings, not reward payout. Formal peer acceptance and full S-32 obligations
remain open. A CONTRACT READY header is not a whole-sequence execution claim.

## 14. Unresolved

- ~~What `00469E80` does with the delta it is handed, and whether anything compares it against the
  setter's meter (DR-6).~~ **Read 2026-09-22 (SWE2-CONTRACT); stack-relative payload count/offset corrected by
  SECTION-03.** `00469E80(ecx=delta)` builds a
  zeroed six-qword payload on its stack, stores the delta at **payload `+0x10`**
  (`[rsp+0x30]` while the payload begins at `[rsp+0x20]`), and — only when the delta
  is positive (`00469EA5 test` / `00469EA7 jle` skips the call) — dispatches event `0x26` through `0046AB10`
  (`ecx=0`, `edx=0x26`, `r8=&payload`; `0046AB10` matches `{id word, key qword}` subscribers in a
  runtime-built table at `02EFB560`). The payload is **transient** — it dies with the frame, and
  `00469E80` stores nothing, so the second report is a notification, not a second ledger. It is
  the shared gil-change notifier with five callers: the death sequence here (`00312566`), the
  `GameState_AddGilClampedAndNotify` wrapper (`003004E5`), `002FD5D3`, `002FEF02` and `003108CC`.
  **Whether anything compares it against the meter:** the two reports are both one-way writes
  into different sinks — the meter's totals persist in the `0020CE00` counter object, the event
  delta does not persist at all — and per the gil contract's census, the six bodies calling the
  counter accessors are disjoint from every `GetGil` reader, so no body holds both numbers.
  Residual: event-`0x26` subscribers register into a `.data` BSS table at runtime, so the
  subscriber set is not statically enumerable; a subscriber that independently reads the meter
  counters cannot be excluded by this census and is not claimed either way.
- ~~Why the per-award experience cap is applied a second time before the display call.~~
  **Answered 2026-09-22 (SWE2-CONTRACT): because it is a different value.** At `003124B4`–
  `00312518` the display path calls `Reward_ComputeExperienceForRecipient` (`002F8BB0`) and
  `Reward_ComputeLicensePointsForRecipient` (`002F90C0`) — the same uncapped evaluators the award
  loop used — on `r14`, and clamps *their fresh results* (`edi` to `0xF423F` at `003124E6`,
  `ebx` to `0x3E7` at `003124FB`–`00312502`) before `0028FB80`. The first cap bounded what was
  accumulated into `[rdi+0x190]`; this one bounds an independent recomputation for display. It is
  not redundant: the evaluators return raw row-derived amounts, so without the second clamp the
  display could show a number above the stored cap.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| DR-2 — mode-dependent null recipient | Caller `003124BC/003124C6` plus complete original EXP/LP bodies and SECTION-03 synthetic controls; NULL is not proof of bypassed division | static original + isolated original execution |
| DR-3 — the walk | `00312432`–`00312460` read in order; the callee resolved to `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` | 1 |
| DR-4 — the four-byte offset | `0031253B` and `00312546` against the experience formula's `+0x34` on the same two records | 1 |
| DR-5 — the conversion and the ×5 | `00312409`/`0031240F` for both layers; the multiply decomposed from the two `lea`s at `00312421`/`00312425`; the accumulator joined at `00312549` | 1 |
| DR-6 — equal stable-input differences, stored upper clamp, positive-only notification | the gil path followed instruction by instruction from `00312553` through `0031255D` to `00312566`, **with the setter's own pre-clamp meter as the comparison** | 1 |
| DR-1, the caps and the recipient rule | [the death page](what-happens-when-an-enemy-dies.md), falsified 2026-09-03 | 1 |
| `00469E80` is the shared gil-change notifier — transient event-`0x26` post, positive deltas only | `00469E80`–`00469EBB` read whole; five callers censused (`002FD5D3`, `002FEF02`, `003004E5`, `003108CC`, `00312566`) | 1 |
| the display-side second cap bounds a fresh recompute, not the stored amount | `003124B4`–`00312518` read; `002F8BB0`/`002F90C0` = the uncapped per-recipient evaluators; `cmovg`/`0xF423F` and `0x3E7` at their instructions | 1 |

[SECTION-03 review and exact production limitations](../_experiments/evidence/continuation-section03-reward-bindings/REVIEW.md).

## 16. Parity plan

L3 is out of scope. Preserve the locally established order and each claim's evidence boundary.
Do not introduce a NULL-recipient "undivided total" special case into EXP or an EXP-style divisor
into LP. Do not substitute actual clamped balance movement for the pre-cap reporting delta
without acknowledging that this changes native behavior. Full event/display and callback
interactions need their own evidence before a whole-subsystem parity claim.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Rewards_Progression_Economy — internal.** The sequence, the reward formulas and the gil award
  are this category's own.
- **CombatFormula — SERVICE.** The recipient's stats record, its status layers and the level the
  walk reads belong to that layer; **this contract asserts which fields are read and in what order,
  not what any of them means elsewhere.**
- **PlatformOnlineAchievements — SERVICE, through the setter.** DR-6's first report reaches that
  layer's meter; its stable-input delta can equal the notifier argument while exceeding stored gain.
- **Presentation — MECHANICAL.** One callee of this body belongs to that layer. **DR-2 is about which
  arguments the display calls receive, not about what draws the result**, and nothing here follows the
  number past the call.
- **Every other layer reached is MECHANICAL**, through this body's own callees — the actor position
  lookup and the drop placement among them. *Their addresses are deliberately not cited: each is a
  hub, and naming one imports its whole edge set.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — SERVICE (2 edges).** `Reward_ComputeExperienceForRecipient` (`002F8BB0`) calls `BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`), and `00312280` calls `Actor_GetWorldPosition` (`00265020`). The evaluator uses the selector to walk the lookup slots it counts for the shared-EXP division (DR-2), and the defeat body reads the victim's world position once, as the input to the loot-placement step; neither call writes actor state.

**CombatAction — CLIENT (3 edges).** `BattleAction_PrepareExecutionResources` (`0030EF20`), `BattleAction_ConsumeExecutionResources` (`00305640`) and `BattleAction_RefundReservedExecutionResources` (`00300280`) all call `GameState_SetGil` (`00254EE0`). They are the action-cost path reserving, spending and refunding gil through the same clamped, metered setter the gil award uses, so a gil-cost action and a defeat award meet in one setter and nothing else.

**CombatFormula — SERVICE and CLIENT (6 edges).** `002F8BB0` calls `BattleStats_FindOwningBattleUnit` (`0031B860`) and `BattleStats_GetByMappedBattleSlot` (`00320AB0`); `00312280` calls `00320AB0` to walk the battle slots when it builds the recipient list; the event poster `0046AB10` calls `0031B860` on its payload; `BattleFormula_DispatchPostResultEvents` (`00469EC0`) calls `0046AB10`, and `BattleFormula_ApplyTargetResult` (`003112F0`) calls `00254EE0`. The contract reads recipients through that layer's stats-record lookups, and that layer uses the same event poster for its post-result events and the same setter when a result moves gil; the reward formulas stay this category's own.

**CoreRuntimeScheduling — MECHANICAL (1 edge).** The event poster `0046AB10` calls `GameClock_GetRawTickCounter` (`0032A150`), a 7-byte clock read, to timestamp a post in its ten-entry recent-post ring and drop a repeat of the same event and key inside a tick window; it is a clock read, not scheduling.

**Gameplay — SERVICE (1 edge).** The mode predicate `003135C0` calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`) and answers whether the mode is 1, which the mode ladder reads as an Esper being out; that is how the EXP evaluator of DR-2 chooses its designated-mode branch.

**Items_Equipment_Shops_License — CLIENT (7 edges).** `InventoryBundleClass09_ApplyGilAndNestedItems` (`002FD530`), `InventoryEncodedGilClass0E_ApplyGilDelta` (`002FD880`), `Shop_CommitPurchaseItemAndGil` (`002FEEB0`) and `Shop_CommitSaleItemAndGil` (`00310870`) call `GameState_SetGil` (`00254EE0`), and `002FD530`, `002FEEB0` and `00310870` also call the gil-change notifier `00469E80`. Bundles, encoded gil grants and shop purchases and sales move gil through the same setter and notifier pair as the defeat award, which is why DR-6's two reports are not specific to battle.

**Movement — SERVICE and CLIENT (4 edges).** `00312280` calls the 148-byte helper `00319490`, which resolves the party-focus actor and hands the victim position to a movement-side position routine before a loot bundle is placed; the mode predicate `003135C0` is also called by `0031BAC0` and by `PartyFollow_SolveFormation` (`00338490`); and `00469A50`, a 160-byte poster that builds a two-unit payload and posts event 8 (or 10 when the first unit is the party leader), calls the poster `0046AB10`. The first is a placement query this contract passes a position to; the others are movement bodies asking the same "Esper out?" question or using the same event poster, and none of them touches the reward sequence.

**Party — CLIENT (1 edge).** `PartyControl_RecomputeSuppressionFromLeaderBattleState` (`0023B040`) calls the mode predicate `003135C0`: the party-suppression recompute asks whether an Esper is out, the same question the EXP evaluator asks, and shares nothing else with this sequence.

**PlatformOnlineAchievements — SERVICE and CLIENT (5 edges).** `00254EE0` and `00312280` both call `00316A50`, the achievement-counter updater (the setter meters gil gained and spent; the defeat body passes each recipient's experience award as counter 11 inside the recipient loop); and the page's `0020CE00`, that layer's 8-byte achievement-manager getter, is called by the three thunks `00863240` (award by id), `00863280` (already-achieved query by index) and `008632B0` (award by index), each of which returns when the manager is null. The reward sequence writes that layer's counters one way and reads nothing back from it (DR-6).

**Presentation — SERVICE (1 edge).** `00312280` calls `Reward_PublishExpLpPresentation` (`0028FB80`), which pushes the EXP and LP floating-text entries; DR-2 is about the arguments that call receives, and nothing here follows the numbers into the text queue.

**Status_Periodic_Terminal — CLIENT (1 edge).** `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`) calls `00312280` at the end of its defeat arm, right after the death presentation event: the status change that knocks a unit out is what starts this sequence, and the sequence itself does not change status.

**UI — CLIENT (1 edge).** `BattleMenu_BuildCommandEntryList` (`0031EB20`) calls the mode predicate `003135C0`: the battle-menu builder asks whether an Esper is out while it builds the command list, a reader of the same mode bit with no role in rewards.

**WorldAreaField — SERVICE and CLIENT (2 edges).** `00312280` calls `FieldData_GetActiveFieldRecordBit15` (`00377C20`) while building the recipient list, to decide whether a slot whose record carries the incapacity flags still qualifies; and `BattleSystem_RunFieldFrameOrchestrator` (`00234590`) calls the mode predicate `003135C0` in its per-frame leader test. The first is a field-permission bit this contract depends on for who is paid; the second is the frame asking the Esper question, outside this contract.

## 17. Related

- [What happens when an enemy dies](what-happens-when-an-enemy-dies.md) — the mechanism
- [Contract — gil storage and movement](CONTRACT-gil-storage-and-movement.md) — DR-6's other half
- [Contract — loot rolls and the chain](CONTRACT-loot-rolls-and-the-chain.md) — the drop
- [Contract — experience and licence award](CONTRACT-experience-and-licence-award.md) — the division DR-2 bypasses

## Falsification pass 1 — 2026-09-30 (OPUS): every clause tested survives

**Attack.** The contract's addressed clauses were turned into checks at their instructions: §2's body, DR-2 to DR-6, the
§10 caps, §14's notifier and §3's install. OPUS block 344's execution is carried, not re-run. Script:
`Tools/analysis-kit/gfz-scripts/falsify_defeat_rewards.py`, output `falsify_defeat_rewards.out`, image `73461d08…`,
0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| D1 | §2 one body of 857 B; its last calls are `00317090` and the cookie check | **survives**. The extent is 857 B, and the last two direct calls are `00317090` and `00808C40` |
| D2 | DR-2 ECX zeroed for the two evaluators; a flag before `0028FB80` | **survives**. `003124BC` and `003124C6` are `xor ecx, ecx` before `002F8BB0` and `002F90C0`. `00312505`–`00312513` test `00236780`'s result (`cmovne edi, ebp`), and `0028FB80` is called at `00312518` |
| D3 | DR-3 the walk reads `+0x1C2` / `+0x18C`, then calls the level advance | **survives**. The walk accumulates `[rdi + 0x18c]` under the 99,999,999 cap, and `003124A3 call 0030C650` |
| D4 | DR-4 gil = (defeated level − `+0x88`) × `[+0xE78]+0x30` + `[+0xE70]+0x30` | **survives**. `[r14 + 0x698]` → `movzx edi, [rax + 0x1c2]`, `movzx eax, [rax + 0x88]`, `sub`; `imul edi, [[r14 + 0xe78] + 0x30]`; `add edi, [[r14 + 0xe70] + 0x30]` |
| D5 | DR-5 status 12 in either layer; the ×5 as `x + 4x` | **survives**. `00312409 test byte [rdi + 0x69], 0x10`, `0031240F test byte [rdi + 0x79], 0x10`; `00312421 lea eax, [r12 + rcx]`, `00312425 lea r12d, [rax + rcx*4]` |
| D6 | DR-6 requested, setter, notifier | **survives**. `00312556 test edx, edx` / `00312558 cmovns ebp, edx`; `0031255D call 00254EE0`; `00312562 sub ebp, ebx`; `00312566 call 00469E80` |
| D7 | §10 the caps and the second display clamp | **survives**. 999,999, 999, 99,999,999 and 99,999 are loaded at `003123ED`, `003123FF`, `00312438` and `0031247C`. The display clamps: `003124B4 mov esi, 0xf423f` held to `003124E6 cmp edi, esi` / `cmovg`, and `0x3e7` at `003124FB`–`00312502` |
| D8 | §14 the notifier | **survives**. `[rsp + 0x30] = ecx`; `00469EA5 test` / `00469EA7 jle` skips non-positive values; `lea edx, [rax + 0x26]` (with `rax` = 0), then `call 0046AB10` |
| D9 | §3 the install of `+0xE70` / `+0xE78` | **survives**. `0023A965`–`0023A9F4` read `02EBF148` and `02EBF140`, index them by definition `+0x22` / `+0x24`, and store `+0xE70` / `+0xE78` |
| D10 | DR-6 the setter clamps to 99,999,999 | **survives**. `00254EE0` carries `0x5F5E0FF` |

**Verdict.** The contract's addressed clauses hold. Tier 1 (static).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22, the falsification pass's new cites (SWE2-FRONTIER, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER), with the stamp of OPUS's falsification pass 1: its rows D2 and D3 cite `00236780`
and `0030C650`, which bring two layers the pages above do not name. Both edges were read at their instructions.*

**Audio — SERVICE (2 edges).** The level advance `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0030C650`),
which the recipient walk calls at `003124A3` (DR-3), calls `003A1180` with ECX = 7 (`0030C831`). That resolves the
current packed sound-bank handle to a sound id. When the id is not −1, `002DF220(id, 0x40, 0x7F)` plays it
(`0030C840`–`0030C84B`). The battle-unit construction contract reads this as the level-up sound. This sequence
reaches Audio only through that call, and no audio state feeds back into the award.

**Save_Load_Settings — CLIENT (1 edge).** `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`) calls `00236780`, the
17-byte getter of bit 14 of the dword at `+4` of the block `[02EBF190]`. That is the flag DR-2 tests at
`00312505`–`00312513`. The save finaliser copies the bit into its header as byte `+0x57` bit 2 (`00583F67`–`00583F70`).
It reads the flag and writes nothing this sequence reads.
