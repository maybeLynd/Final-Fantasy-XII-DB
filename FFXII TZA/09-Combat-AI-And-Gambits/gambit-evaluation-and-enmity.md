---
system: Gambit evaluation and enmity
category: 09-Combat-AI-And-Gambits
status: DOCUMENTED — every register row the page names is closed and its prose residue is answered (owner re-status 2026-10-01, OPUS, on SWE2-CONTRACT's DD batch 16) — the one registered residue, GR-9 (what enters the subgroups of 155 enemy order sets that no switch inside the set reaches), answered 2026-09-30; UQ-121 answered 2026-09-26, Z-2 and Z-16 answered 2026-09-17, every other Z row on the page closed; order-flag bit 0x04 is read by the navigation gate 00325D90 (no combat navigation step while it is set; corrected 2026-10-01, DD batch 16)
owner_layer: PrimaryOwner:CombatAI
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-12
registry_slots:
  - "0x02EBF0E0"
  - "0x02EBF160"
audit:
  passes: 3
  last_pass: 2026-09-08
  last_pass_state: GN160-xiionline-61-Z10-framerate-scalar
  crossref_clean: false
  reopened_count: 9
---

# Gambit evaluation and enmity

> FFXII's signature system, in one sentence: **walk the list from the top, and the first gambit
> whose condition is true and whose action can be committed wins.** Plus the thing the game never
> shows you — a **40-entry threat table** on every enemy that decays by **10 every interval**,
> but only while nothing is fighting it.

**PARTIAL.** The selection loop, the enmity decay and the highest-threat scan are read at tier 1
and are exact. The condition evaluator (`AiOrder_EvaluateTargetSelector`, 6,963 bytes) **was read
on 2026-09-02 — see section 8b**: its shape, the highest/lowest opcode bit and the
operand-to-field map are recovered, but the complete opcode numbering is not.

*Reconciled (FABLE, Claude Opus 5.5, 2026-09-30): the paragraph above is the state of 2026-09-02. The complete opcode table was read on 2026-09-12 (Z-1, the table in section 8b), and the one open question is **GR-9** (section 7, the UQ-121 box). Section numbering: two sections are numbered 8f (the relation modes, Z-7; the Z-10 reopening) and two 8i (the weighted action pick; the falsification pass on relation modes 0–10). The numbers are kept because other pages cite them. Related pages are in section 9, at the end.*

## 1. What the player sees

You order your gambits top to bottom, and that order is exactly what happens. **Ally: HP < 70% →
Cure** above **Foe: nearest → Attack** means healing always beats attacking. Drag it below and it
never fires while something is attackable. The game evaluates in list order and stops at the first
one that fires.

A gambit is skipped silently if its condition is false *or* if the action cannot be committed —
no MP, target out of range, silenced. Both look identical from the outside: the line just does
nothing and evaluation moves on.

You each get **three gambit sets** to switch between. The game stores each character's gambit list three times over and remembers which of the three is selected; the menu edits and switches among them.

And there is a whole layer FFXII never displays: **every enemy keeps a running grudge against
every combatant.** Hit something and its threat toward you rises; walk away and stop fighting and
that grudge **drains away by 10 a tick** until it forgets you. While you are still engaged, it
does not forget at all.

## 2. Native mechanism

### The gambit walk — first match wins

`BattleUnit_TrySelectAndCommitAiOrderFromSet(unit, order_set, subgroup_index, resume_mode)`:

```c
action = 0xFFFF;                                  // the evaluator's out: the decoded action id (00301500)
target = 0;                                       // the evaluator's second out: the chosen unit's +8 id (003017E7)
if (order_set == NULL) return 0;

// walk the header's per-subgroup count bytes to find this subgroup's base
for (i = 0; i < subgroup_index - 1; i += 2) {
    a += order_set[i];
    b += order_set[i + 1];
}
if (i < subgroup_index) c = order_set[i];

ctx = unit->pAction_context;
resuming = (resume_mode && ctx && (ctx->wFlags & 0x4000)) ? 1 : 0;

if (order_set[subgroup_index] != 0) {
    order = order_set + 0x20 + (a + b + c) * 0x18;      // 32-byte header, 24-byte records
    do {
        if (resume_mode && ctx == order) return 1;      // reached where we left off

        if ((!resuming || (order->wFlags & 0x40)) &&    // 0x40 = evaluate while resuming
            (!resume_mode || !(order->wFlags & 0x80)))  // 0x80 = skip on resume
        {
            if (AiOrder_EvaluateAndResolveActionTarget(unit, order, &action, &target) != 0
                && BattleUnit_CommitAction(unit, order, action, target, 1) != 0)
            {
                if (resume_mode == 0) return 1;         // committed - done
                ...
            }
        }
        ...
    } while (...);
}
```

Three things this establishes exactly:

**An AI order record is `0x18` = 24 bytes**, and the order set has a **`0x20` = 32-byte header**
whose leading bytes are per-subgroup counts. A subgroup's first order is found by summing the
counts before it.

**Both the condition and the commit must succeed.** `AiOrder_EvaluateAndResolveActionTarget`
returning non-zero is not enough — `BattleUnit_CommitAction` must also succeed, or the loop moves
to the next order. ~~**This is why a gambit with a satisfied condition can still visibly do nothing.**~~ *Corrected
2026-09-26 (FABLE, Claude Opus 5.5): the branch is real, but over the shipped action table it never fires. A matched
line always commits, because the condition arm and the commit test the same action-table bound
([the gambit-walk contract](CONTRACT-gambit-walk.md) §7, measured by OPUS 6/6). It is a control-flow case, not a
game state.*

~~**`0xFFFF` is the no-target sentinel** — the same sentinel the item system uses for "nothing".~~ *Corrected
2026-09-26 (FABLE, Claude Opus 5.5), re-read from the bytes on `OPUS-NOTE-FABLE-GAMBIT-PAGE-FFFF-SLOT-IS-THE-ACTION`.*
The word slot `[rsp+0x70]`, initialised to `0xFFFF` (`00305CCF`–`00305CD6`), is the evaluator's **action** out:
`003014F0` keeps the pointer in `r12`, and `00301500 mov word [r12], ax` stores the decoded action id. The walk passes
it to the commit as `r8w` (`00305DE3`). The dword slot `[rsp+0x30]` is the **target**: the evaluator stores the chosen
unit's `+8` id through it (`003017E7`), and the walk passes it as `r9d` (`00305DDB`). `0xFFFF` is only the value
before anything resolves. The third call's `edx` at `00305E44` is the same action word.

Two flag bits govern resumption after an interrupted action: `0x40` marks an order as still
evaluable while resuming, `0x80` marks it as skipped on resume, and `0x4000` on the action context
says a resume is in progress.

### Three gambit banks

`GambitConfig_InitializeThreeBanksFromBasePairs` (`00326030`) names the count directly, matching
the three sets a player can configure. The surrounding functions form a complete config layer:

| Function | Address | Role | How far this is verified |
|---|---|---|---|
| `GambitConfig_InitializeThreeBanksFromBasePairs` | `00326030` | zero the member's selected-bank index, then copy the stats record's gambit block into all three banks | **complete 224-byte body read 2026-09-30**: `+0x7370 + 4i` = 0 (`00326039`); the 52 bytes at record `+0x88`–`+0xBB` stored at bank `+0x5B10`, `+0x5B44` and `+0x5B78` of the member's `0x9C`-byte group (`00326057`–`00326109`), so the three banks start identical |
| `GambitConfig_CopySelectedBankForStatsIndex` | `00327C40` | **copies one 52-byte bank record out to a caller buffer** | **complete 108-byte body read** |
| `GambitConfig_AdjustAvailableEntryCountByStatsIndex` | `00327930` | **adds a delta to a per-bank entry count and clamps it to `[0, 12]`, for all three banks** | **complete 116-byte body read** |
| `GambitConfig_ClassifyActionTargetPairCompatibility` | `00327A10` | whether an action suits a condition's relation | **complete 388-byte body read 2026-09-30**: `(action, condition, flag)`; 0 for an empty `0xFFFF` slot (`00327B87`) or a fit. The action must be a class-20 id and the condition a class-11 id (`00327A48`, `00327A81`); the condition row's relation byte `+0x10` then needs the action row's `+0xC` bit 3 for `Foe` (1), bit 2 for `Ally` (2), bit 0 or 2 for `Self` (4) (`00327B10`–`00327B7B`). A misfit returns reason `0x1C`–`0x1F`, or `0x20`–`0x23` when the flag is set |
| `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` | `00327CB0` | apply a preset | read 2026-09-11 (§4, the authored presets): copies a `02EBF0E0` row's pairs into the record's `+0x88` block, mask `+0xB8`, count `+0xBA`, then rebuilds |
| `GambitRuntime_RebuildOrderSetForStatsRecord` | `00327DE0` | config -> runtime order set | structure only: one loop (`00327F4B`), calls `ImageAddress_ResolveRuntimePointer` |
| `GambitRuntime_RebuildAllOrderSets` | `00327F80` | rebuild every unit's | structure only: **two nested loops** (`003280F3`, `0032811A`), same resolver |

> **Anchored 2026-09-03, and two roles were sharpened by reading rather than restated from the
> name.** `CopySelectedBankForStatsIndex` does not *switch* anything — it **copies** a 52-byte record
> (`00327C81`-`00327C9D`, three `movups` plus a dword) to the buffer in `rdx`, bounded by
> `00327C46 cmp cl, 0x27` (index ≤ 39). `AdjustAvailableEntryCountByStatsIndex` loops over **three**
> banks (`00327994 cmp rdx, 3`) and clamps each count to twelve — `0032795B lea r11d, [rdx + 0xc]`
> and `00327985 cmovg eax, r11d` — writing back to a byte at record offset `0x32`
> (`0032798C mov byte ptr [rcx + r8 + 0x5b42], al`, against the record base `+0x5B10`).
>
> **Three of the seven rows are still name-derived and are now marked as such.** A role column that
> paraphrases the function name asserts nothing; leaving that visible is the point.
>
> *Updated (FABLE, Claude Opus 5.5, 2026-09-30): `00326030` and `00327A10` are now read whole (rows above). The two rebuild rows are structure-only here; each walks the twelve config slots (`lea r15d, [r12 + 0xc]` at `00327E1A` and `00327FF4`), and their record stores are read in section 8l for the sibling `00328140`.*

**All three of these index the same table — `02EBF190`** (`00327C59`, `00327938`, `0032799A`), which
is the **heaviest slot in the authored-table registry** at ~170 referencing functions. **The gambit
config layer lives inside the registry's biggest table**, a join neither
[`../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
nor this document previously stated.

**And the clamp is a third, independent sighting of twelve.** §8l counts a twelve-slot config, and
[`which-gambit-set-fires-and-how-a-command-switches-it.md`](which-gambit-set-fires-and-how-a-command-switches-it.md)
finds twelve commands mapping to subgroups 0-11. **This one is a hard `0xC` clamp on the entry
count** — a bound on the quantity itself rather than a count of things, which is why it is worth more
than the other two agreeing.

**The editable configuration and the evaluated order set are different structures**, with an
explicit rebuild step between them.

### Enmity — the hidden threat table

Storage is on the *target*: a **40-byte vector** in its BKEI record, one byte per combatant id.

```c
int BattleEnmity_GetHighestRelevant(unit)
{
    best = -1;
    table = &unit->pBkei->bEnmityTableHeader;      // NULL-guarded
    n = BattleUnit_BuildFilteredFourSlotUnitBuffer(&buf, 1);   // the four party slots
    for (i = 0; i < n; i++) {
        id = *(byte *)(*(longlong *)(buf[i] + 0x698) + 4);
        v  = BattleEncodedId_IsValidForClass(2, id) ? table[id + 1] : -1;
        if (best < v) best = v;
    }
    return best;                                   // -1 if no table or no valid ids
}
```

The scan walks the **four party slots** — the same four-slot roster the Party document
establishes — so "who is this enemy angriest at" is answered against the active party only.

### Decay — 10 per interval, held while engaged

```c
void BattleEnmity_UpdatePeriodicDecay(unit)
{
    if (!unit || !unit->pBkbi) return;
    if (*(char *)(&unit->pBkbi->wDefinitionSelector + 1) != 1) return;   // foe-class gate

    timer = &unit->pBkei->bEnmityTableHeader;
    if (!unit->pBkei) return;

    if (BattleUnit_HasActiveEngagementEvidence() == 0) {
        t = *timer + 1;
        if (t < (int)(DAT_01dfe0b8 * DAT_008f8d80)) goto store;   // interval not reached
        BattleEnmity_WriteAllCombatantIds(unit, -10, 0);          // decay everyone by 10
    }
    t = 0;                                                        // reset the timer
store:
    *timer = (byte)t;
}
```

**The decay is exactly `-10`, applied to every combatant id at once**, and the interval is a
product of two configured values.

**Engagement evidence suppresses forgetting entirely.** While `BattleUnit_HasActiveEngagementEvidence()`
is true, the timer is written back as 0 every pass, so it never reaches the interval. Threat only
drains once the fight actually stops.

The first byte of the enmity block is the **timer**, and the per-combatant entries follow it —
`table[id + 1]` in the scan above.

### The same foe gate as the reward system

`*(char *)(&pBkbi->wDefinitionSelector + 1) != 1` is the **third independently-found site** of a
check already documented twice in Rewards (`Reward_ComputeExperienceForRecipient` and
`Reward_ComputeLicensePointsForRecipient`).

So one authored classifier decides **which foes award EXP, which award LP, and which maintain a
threat table.** That was not searched for — it was recognised from a constant recorded exactly in
an earlier block.

## 3. Key addresses

| Address | Name | Size | Verified |
|---|---|---:|---|
| `00305CC0` | `BattleUnit_TrySelectAndCommitAiOrderFromSet` | 422 B | ✅ read |
| `00321530` | `BattleEnmity_UpdatePeriodicDecay` | 142 B | ✅ read |
| `00321630` | `BattleEnmity_GetHighestRelevant` | 175 B | ✅ read |
| `00321840` | `BattleEnmity_HasAnyPositive` | 7 B | ✅ read — wrapper for `AnyAboveThreshold(unit, 0)` |
| `003215C0` | `BattleEnmity_ReadForCombatantId` | 102 B | ✅ read 2026-09-30 — the entry `BKEI + 0x1A + id` for a valid class-2 id, else `-1` (`003215F6`–`0032160D`) |
| `00301AD0` | `AiOrder_EvaluateTargetSelector` | **6,963 B** | ✅ read - see section 8b |
| `003014C0` | `AiOrder_EvaluateAndResolveActionTarget` | 876 B | ✅ read — the eligibility gate (section 8g), the record layout (8l) and, 2026-09-30, the selector chain and the final pick (8l, *the preserved copy*) |
| `00301830` | `AiOrder_CheckActionPreconditions` | 670 B | ✅ read 2026-09-12 (FABLE, AT-6) — the per-id preconditions and the second word's percent roll are on [the handler-table page](../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md) |
| `003087E0` | `AiOrder_SelectFinalTargetFromCandidates` | 940 B | ✅ read 2026-09-30 — keeps the candidates that tie the list's best score and pass `BattleAction_CheckTargetEligibility`; among several, list byte `+2 == 1` picks one with the shared LCG (`00308B13`), otherwise the one nearest the acting unit (`00308B5D`) |
| `0030F130` | `AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` | 408 B | ✅ read 2026-09-30 — the starting candidate list: the unit's perception cache (`+0xBC0`), copied whole when its range `+0x6D0` is 0, else only the entries within that range of the `+0x6C0` point (`0030F239`); then each of the four mapped party members whose status meets the action's authored status mask on `0x80000003` (`0030F28D`–`0030F2A8`) |
| `00305AB0` | `BattleUnit_SelectAndCommitNextAction` | 517 B | ✅ read 2026-09-03 — the tail (the four-set cascade that supplies `subgroup_index`) is in [`which-gambit-set-fires-and-how-a-command-switches-it.md`](which-gambit-set-fires-and-how-a-command-switches-it.md); section 8h below covers its head; its second argument is the walk's resume mode (`00305ABC`, `00305B9C`) |
| `00308610` | `BattleUnit_UpdateCombatFrame` | 461 B | ✅ read 2026-09-30 — with an order current (`+0x708`) it re-walks the gambits in resume mode, `00305AB0(unit, 1)` at `0030874C`; with none it resets the action, sets unit flag `0x20` and queues the unit's id on the 64-slot selection ring (`003086AF`–`003086DA`) |
| `00313CD0` | `BattleUnit_ProcessPendingActionSelectionQueue` | 220 B | ✅ read 2026-09-30 — drains up to eight queued ids per call (`00313CF7`), none while bit `0x20` of `02089340` is set (`00313CD4`); a unit still flagged `0x20` whose status clears `0x8000001B` gets a fresh walk, `00305AB0(unit, 0)` at `00313D89` |
| `0030BD00` | `BattleTarget_MatchesRelationMode` | 339 B | ✅ read — the eleven relation modes, section 8i (falsification pass) |
| `00321850` | `BattleEnmity_WriteForCombatantId` | 381 B | ✅ read 2026-09-30 — adds (mode 0) or sets (mode 1) one foe entry: a positive entry is floored at 1 (`0032191D`–`00321923`); a rise on a foe holding no entry above 1 gets +10 (`0032192B`–`0032193A`); the store clamps to 0–255 (`00321E40`); and an entry that goes from 0 to positive raises every zero entry of the table to 1 (`0032194B`–`003219AD`) |
| `003219D0` | `BattleEnmity_PropagateToPerceivingFoes` | 296 B | ✅ read — section 8e (Z-6) |
| `00321B00` | `BattleEnmity_AdjustOtherRelevantCombatants` | 551 B | ✅ read 2026-09-30 — the same per-entry rule as `00321850`, applied on the target foe to the four party slots other than the source unit (`00321B5E`, `00321B99`) |
| `00321D30` | `BattleEnmity_WriteAllCombatantIds` | 141 B | ✅ read — `00321850` for ids 0–39 (`00321D90`–`00321DA6`) under the `0x80000003` gate (sections 8e, 8k) |
| `00326030` | `GambitConfig_InitializeThreeBanksFromBasePairs` | 224 B | ✅ read 2026-09-30 — section 2's bank table |
| `00327A10` | `GambitConfig_ClassifyActionTargetPairCompatibility` | 388 B | ✅ read 2026-09-30 — section 2's bank table |

### Data addresses cited by this document (FABLE, 2026-09-30)

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01DFE0B8` | frame-rate scalar | `.data` f32 | `1.0`, or `2.0` under FrameLimit 60 (section 8f, Z-10); one decay-interval factor, read at `0032157F` |
| `008F8D80` | — | `.rdata` f32 | `30.0`, the other factor (`00321587`) |
| `02EBF190` | battle-state block pointer | `.data` qword | the three gambit banks per member at `+0x5B10` and the selected-bank index at `+0x7370` ([the battle-state block](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)) |
| `02089378` | runtime party order sets | `.bss` | 40 sets of `0x170` bytes, one per stats index (section 8l) |
| `022BE984` | pending-selection ring | `.bss` | 64 unit ids; write index `022BE981`, read index `022BE980` (`00308610`, `00313CD0`) |

## 4. Data structures and formulas

```
AI order set
  +0x00 .. +0x1F   header, 32 bytes; leading bytes are per-subgroup order counts
  +0x20 ..         array of AI order records, stride 0x18 (24 bytes)

AI order record                     0x18 bytes
  wFlags   bit 0x40   evaluate even while resuming
           bit 0x80   skip when resuming

Action context
  wFlags   bit 0x4000  a resume is in progress

BKEI enmity block
  +0x00        u8      decay timer
  +0x01 ..     u8[40]  enmity per combatant id      (GFZ records BKEI+0x1A..+0x41)

BattleUnit
  +0x698 -> +0x04   u8   this unit's encoded combatant id
```

**Subgroup base index:**

```
base = SUM(order_set[i] for i in 0 .. subgroup_index-1)
first = order_set + 0x20 + base * 0x18
```

**Gambit selection — the whole system in four lines:**

```
for order in orderSet[subgroup]:
    if resumeGated(order): continue
    if EvaluateAndResolveActionTarget(unit, order, &action, &target)
       and CommitAction(unit, order, action, target):
           return committed          <- FIRST match wins
```

**Highest relevant enmity:**

```
highest(unit) = max over the four party slots p of
                  ( IsValidForClass(2, p.id) ? unit.enmity[p.id + 1] : -1 )
                default -1
```

**Enmity decay:**

```
if engaged(unit):            timer = 0
else:
    timer = timer + 1
    if timer >= (DAT_01DFE0B8 * DAT_008F8D80):
        for every combatant id:  enmity -= 10
        timer = 0
```

**Foe-class gate**, shared with EXP and LP award:

```
maintainsEnmity(unit)  iff  unit.pBkbi.wDefinitionSelector[+1] == 1
```

### The authored presets — registry slot `02EBF0E0`, read 2026-09-11

`battle_pack.bin`'s directory entry `+0x24` binds registry slot `02EBF0E0`: **40 rows × 64 bytes**,
one per preset id `0x5000 + row` (class 10 of [the encoded-id space](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)):

```
GambitPresetRow (64 B)
  +0x00 u16 condition[12]   gambit target-condition ids (0x6000 + row of 02EBF0D8), 0xFFFF = empty
  +0x18 u8  zero[8]
  +0x20 u16 action[12]      action ids (rows of 02EBF138), 0xFFFF = empty
  +0x38 u8  zero[8]
```

Decoded through the banks: row 0 is *Foe: party leader's target → Attack*; row 1 *Ally: HP < …
→ Potion; Foe: nearest visible → Attack*; row 3 *Ally: any → First Aid; Foe: nearest visible →
Attack*; row 11 *Foe: flying → Telekinesis; Foe: party leader's target → Attack; Foe: targeting
self → Attack; Foe: targeting ally → Attack; Foe: nearest visible → Attack; Foe: any → Attack*; row
39 ends *Ally: HP < … → Renew*.

**The loader**, `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders(statsRecord, presetId)`
(`00327CB0`): party records only (`+5 == 0`, `00327CC3`–`00327CCE`); validates the id as class 10
(`00327CDF`); resolves the row (`00327CEA`–`00327D28`); copies pairs `i = 0 …` while both the
condition and the action are not `0xFFFF` into the record's **gambit block at `+0x88 + 4i`**
(`u16 condition`, `u16 action`), setting bit `i` of the **enabled mask `+0xB8`** (`00327D42`–`00327D82`);
writes the **count** to `+0xBA` (`00327D84`); fills the remaining slots up to twelve with
`0xFFFFFFFF` and clears their mask bits (`00327D8A`–`00327DC0`); then
`GambitRuntime_RebuildOrderSetForStatsRecord` (`00327DE0`). Its callers: `BattleStats_InitializeDefinitionRecord`
with the **party row's word `+0x14` — the character's default preset** (`0023AEEE`–`0023AEF5`), the
SetSaveData apply with the preset row's `+0xE` ([the presets page](../11-Party/the-setsavedata-presets-test-battle-scenarios.md)),
and `00328BD0` ← **the script verb `resetJobs`** (`05D6`, family 0 index `0x5D6`; its handler `00342230`
pops one int through `00267E10` and passes it as the preset id, `00342234`–`00342242`; it is
reached through the family-0 handler table at `01EF91E0`, which is why no call site names it —
[the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv), FZ-6 answered 2026-09-11).

So the stats record's `+0x88` … `+0xBA` is, for a **party** record, the twelve-slot gambit block —
where the enemy branch of the level grower writes a single byte at `+0x88` (`0030C4B1`): a
kind-discriminated union like the record's `+0x10` … `+0x1F`, which the stats map's single-byte
row for `+0x088` does not yet say. *(It does now: the field map's `+0x088` row records the union, by the kind byte `+0x05`. Note (FABLE, Claude Opus 5.5, 2026-09-30).)*
## 5. Call chain

```
field frame, once per unit (the lifecycle frame 00233F70, section 7's Z-3 box)
  -> BattleUnit_UpdateCombatFrame (00308610)
     -> an order is current : BattleUnit_SelectAndCommitNextAction (00305AB0), resume mode 1   [0030874C]
     -> no order            : set unit flag 0x20, queue the unit id on the 64-slot ring 022BE984
BattleUnit_ProcessPendingActionSelectionQueue (00313CD0), up to 8 queued units per call
  -> BattleUnit_SelectAndCommitNextAction (00305AB0), resume mode 0: a fresh walk            [00313D89]
        -> a pending player command commits first, else (section 8h)
        -> BattleUnit_TrySelectAndCommitAiOrderFromSet (00305CC0), up to four sets    [00305BA5, 00305C1A, 00305C58, 00305C71]
           -> walk order set from subgroup base, in order, up to the subgroup's count byte   [00305DFD-00305E0A]
              -> AiOrder_EvaluateAndResolveActionTarget (003014C0)                            [00305DD2]
                 -> BattleData_ResolveWeightedId (00308EC0)                                   [003014F6]
                 -> AiOrder_CheckActionPreconditions (00301830)                               [003015DA]
                 -> AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus (0030F130)     [00301649]
                 -> AiOrder_EvaluateTargetSelector (00301AD0, 6,963 B), once per non-empty entry [003016A8]
                    -> AiTargetSelector_ResolveOperandValue (00321190)
                    -> BattleEnmity_GetHighestRelevant / HasAnyPositive
                    -> BattleTarget_MatchesRelationMode (0030BD00)
                 -> AiOrder_SelectFinalTargetFromCandidates (003087E0)                        [003017BF]
              -> BattleUnit_CommitAction (0030F760)                                          [00305DF4]
                 -> success : stop. failure : next order.

periodic maintenance
  -> BattleEnmity_UpdatePeriodicDecay (00321530)
     -> foe-class gate
     -> BattleUnit_HasActiveEngagementEvidence
        -> engaged : timer = 0, no decay
        -> idle    : timer++, at interval -> WriteAllCombatantIds(unit, -10)

an action lands
  -> BattleEnmity_ApplyActionParameters (003216E0)
  -> BattleEnmity_PropagateToPerceivingFoes (003219D0)
  -> BattleEnmity_AdjustOtherRelevantCombatants (00321B00)

gambit UI edit
  -> GambitConfig_* -> GambitRuntime_RebuildOrderSet* -> the order set walked above
```

**Upstream:** the per-unit combat frame, which re-walks in resume mode while an order runs, and the pending-selection queue, which gives idle units a fresh walk, at most eight per call (both read 2026-09-30); and the gambit menu, through the banks and the rebuild.
**Downstream:** action commit, which is Combat Action's owner.

**Do not confuse with:** the action *execution* pipeline. This category chooses **what to do and
at whom**; committing and resolving it belong to Combat Action and Combat Formula.

## 6. Modding notes

- **Order is the whole algorithm.** First order whose condition passes *and* whose action commits
  wins. There is no priority field and no scoring — position in the list is the priority.
- ~~**A satisfied condition is not enough.** `CommitAction` must also succeed. A gambit that "should
  fire" but doesn't is usually failing at commit, not at the condition.~~ *Corrected (FABLE, Claude Opus 5.5, 2026-09-30):* the walk does
  test the commit, but over the shipped action table a line whose condition matched is never refused by it
  ([the gambit-walk contract](CONTRACT-gambit-walk.md) §7, measured 6/6; section 2's correction of 2026-09-26). A
  gambit that "should fire" but doesn't is failing inside the evaluate step: the eligibility gate (section 8g),
  the action's preconditions or its percent chance (record `+0x02`, rolled at `0030160F`–`00301637` when non-zero),
  or a target selector that finds nobody. A reimplementation still keeps both calls, in that order.
- **Records are 24 bytes with a 32-byte header** whose leading bytes are per-subgroup counts. A
  tool editing gambit sets must keep those counts consistent or the subgroup base index shifts.
- **Enmity is 40 entries stored on the enemy**, not on the attacker, indexed by encoded combatant
  id. Byte 0 of that block is the decay timer, not enmity.
- **Decay is exactly `-10` to everyone at once**, and only while disengaged. To make enemies hold
  grudges longer, raise the interval factors; to make them forget faster, lower them.
- **Only foes with `wDefinitionSelector[+1] == 1` keep a threat table** — the same classifier that
  decides whether a kill awards EXP and LP.
- **XIIOnline:** enmity is keyed by *native combatant id* and stored receiver-locally. Two clients
  will build different tables from the same fight. Foe AI must advance on a single simulation
  authority, and ownership migration has to transfer or deterministically rebuild the enmity vector
  keyed by a stable identity before AI resumes. Synchronising raw enmity values is not sufficient —
  **engagement evidence must be preserved too**, or threat will decay on one client and not another.

## 7. What is not known

- [x] ~~What `00342230` is — the caller of `00328BD0`, the third path into the preset loader; no static
      caller, presumably the gambit menu.~~ **FZ-6 ANSWERED 2026-09-11:** the script verb `resetJobs`
      (`05D6`) — it pops the preset id and hands it to `00328BD0` (§4).
- [x] ~~The complete outer-opcode table for `AiOrder_EvaluateTargetSelector`.~~ **Z-1 ANSWERED 2026-09-12
      (FABLE):** all 70 opcodes and 31 case bodies read, the two operand sub-tables decoded, the four
      threshold tables read, the self-condition family (54 / 55) traced to the script-variable
      accessors, and every opcode joined to the shipped sets' 50,050 records — the table under §8b.
- [x] ~~**Z-2.** The AI order record's exact **byte offsets**. **Z-2 — fields identified in section 8g**~~
      (`wActionSelector` weighted, `wActionParameter02`, `wFlags` with 7 bits, `targetSelector0[]`);
      offsets still unproven.
      ***ANSWERED 2026-09-17 (FABLE): the 24 bytes, proven from the reader, the writer and the authored files.** `+0x00 u16` the weighted action selector (`AiOrder_EvaluateAndResolveActionTarget` passes the record base to `BattleData_ResolveWeightedId`, `003014EA`..`003014F6`); `+0x02 s16` the action parameter (`movsx` at `0030162F`, compared at `00301608`; not written by the config rebuild, authored only); `+0x04 u16` the flags word (`003015A6`, `003016BE`; the thirteen bits of Z-19); then three six-byte target-selector entries at `+0x06`, `+0x0C`, `+0x12` (`lea rbp, [r14 + 6]`, entry `i` read at `+6 + 6i` by `00301AD0` through `rdi = 3i`, `00301B0B`..`00301B1F`): `u16 operand` (the relation mode; 0 ends the list, `00301685`), `u8 opcode` (`+8`), `u8` (`+9`), `s16 parameter` (`+0xA`). The writer `GambitRuntime_RebuildOrderSetFromConfig` (`00328140`) fills the same offsets from a condition row of table `02EBF0D8`: `+0` from the slot's action word, `+4` from row `+0xE`, the three operands from row bytes `+0x10`/`+0x11`/`+0x12`, the three opcode words from row `+8`/`+0xA`/`+0xC` and the three parameters from row `+0x18`/`+0x1A`/`+0x1C` (`00328226`..`00328273`), at `set + 0x20 + 24k` ([the gambit-set page](which-gambit-set-fires-and-how-a-command-switches-it.md) reads the same writer). [The loader page](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)'s read of all 1,422 authored sets shows the same shape at stride 24 with operand 0 marking an empty entry. Static; the Ghidra type's names (`wActionSelector`, `wActionParameter02`, `wFlags`, `targetSelector0[]`) now sit on proven offsets.*
- [x] ~~What action id `0x414D` *does*.~~ **Z-14 ANSWERED 2026-09-12 (FABLE): it flips the combat stance.** Its order-table slot `01EEC460[0x14D]` is the dedicated handler `002FE840`, which exits or enters the party combat stance by unit flag bit 23 and then waits for the transition flags 50 / 51 to clear; it is the single order of the static re-plan set `01EEC410` that every non-party unit receives at `+0x6E8` on a combat-state reset ([the gambit-set page](which-gambit-set-fires-and-how-a-command-switches-it.md) §7) — `.data` bytes, which no instruction-immediate search sees. The earlier reading that it reaches a `-1` arm concerned the direct-state sub-dispatcher, which the order table does not route it to. *Original entry:* **Z-14 — advanced in section 8h**: it is member 333 of an
      **order**-id band `0x4000`-`0x4166` that two separate gates treat specially; only one
      instruction in the binary references it, so it arrives from authored data. *(Corrected
      2026-09-02: this band is the extended **order** space, not the player-command space — those are
      the ids `<= 0x21E`, split in `BattleUnit_CommitAction`.)*
- [x] ~~**Z-16.** Whether *any* consumer decodes an action-id category. **Z-16 — leans NO** (section 8i): three~~
      action functions show no `>> 0xC` / `& 0xFFF` / `- 0x4000`; the real discriminator is **bit 15**.
      ***ANSWERED 2026-09-17 (FABLE): yes. The three functions §8i checked do not decode a category, but the consumers of the resolved id do, and the category they decode is the top nibble.** A census of the combat range `002F0000`..`00330000` for the three idioms (a right shift by 12, a mask of `0xFFF`, a subtraction of `0x4000`) finds them in 38 functions. Three sit on the gambit path. `00301830`, the function after `AiOrder_EvaluateAndResolveActionTarget`, takes the resolved id, subtracts `0x4000`, bound-checks the result against `0x166` and indexes the order-handler table `01EEC460` ([the gambit-set page](which-gambit-set-fires-and-how-a-command-switches-it.md) names its slots) with it (`003018DD`..`003018FB`), then compares the id with `0x4124`: **the `0x4000` band is decoded as a category and its low 12 bits as an index.** `BattleLocomotion_DecodeOrderGoal` (`00312730`) does the same for goals `0x4000`..`0x4025` (`0031278C`..`003127BA`, a byte and a dword table). `00306340`, called by the two party-list classifiers `002826F0`/`00282A40` on a word from a list entry, switches on `id >> 12` with arms for nibbles 3, 4 and 12, the last resolving `id - 0xC000` in table `02EBF0C8` (`0030635A`..`003063B5`). Nine more functions index the fifteen `0x58`-byte inventory class descriptors at `01EEBCC0` by `id >> 12`, [the encoded-id page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)'s rule. So the selector word carries two discriminators: bit 15 separates a weighted selector from a literal id, and a literal id's top nibble is its category, nibble 0 an action row and nibble 4 an order with a handler slot. Static, census and bodies read.*
- [x] ~~The weighted-table entry format at `DAT_02EBF160` beyond the count header.~~ **Z-18 ANSWERED with AD-1 (2026-09-12, FABLE):** `{u16 count = 826; u16; u32 offset[count + 1]}` bounding runs of 4-byte rows `{u16 actionId, u8 weight, u8 0}` whose weights sum to exactly 100 in every shipped run; the resolver draws one shared-LCG value `% 100` and returns the first row whose cumulative weight exceeds it ([the RNG page](../21-RNG-And-Determinism/rng-streams.md)).
- [x] ~~The status bits `0x20` and `0x08000000` tested outside the `0x80000003` predicate.~~ **Z-17 ANSWERED 2026-09-11:** bit 5 is **Confuse** and bit 27 **Berserk** — [the battle text banks](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md), bank 5 in status-id order; a confused unit, or a berserk foe, does not choose its next action here.
- [x] ~~The five unidentified `wFlags` bits (`0x20`, `0x400`, `0x1000`, and the rest).~~ **Z-19 answered 2026-09-12 (FABLE):** all thirteen bits the shipped sets use, with their readers — the table under section 8g (`0x4000` resumable, `0x800` no re-issue while current, `0x2000` no timeout interrupt, `0x100` / `0x200` locomotion flags, `0x400` / `0x1000` evaluator modes, ~~`0x04` unread~~ `0x04` no combat navigation step while current). *Corrected 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): bit `0x04` has a reader, the navigation gate `BattleUnit_CanAdvanceCombatNavigation` (`00325DF4`); section 8g's table and [the batch record](../_index/candidates/swe2contract-ddres-b16-0930/README.md), checks N4-N6.*
- [x] ~~The **unit** of the decay interval. **Z-3 — values answered in section 8c**
      (`1.0 x 30.0 = 30`); frames vs ticks vs milliseconds still unproven.~~ **Z-3 ANSWERED 2026-09-12 (FABLE):
      one second of maintained field frames.** The counter `BKEI + 0x19` rises by one per call of
      `BattleEnmity_UpdatePeriodicDecay` (`0032158F`–`003215AC`) and is zeroed on engagement or when it reaches
      `(int)(01DFE0B8 × 30.0)`, at which point every one of the 40 enmity entries gets `−10` as a **delta** — a positive entry is floored at **1**, never 0 (`BattleEnmity_WriteForCombatantId`, mode 0: `0032191D`–`00321923`), so a foe keeps a residue of threat toward anyone it was ever angry at
      (`0032159C`–`003215A5`, `BattleEnmity_WriteAllCombatantIds` → `BattleEnmity_WriteForCombatantId` per id).
      Its only caller is `BattleUnit_RunPeriodicCombatMaintenance` (`003112A4`), called once per unit from the
      per-unit lifecycle frame (`00234001`), which runs once per field frame ([the world tick](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)).
      The scalar is `1.0` under FrameLimit 30 and `2.0` under FrameLimit 60 (section on the time base below), so
      the threshold is 30 or 60 frames — **one second either way**. Frames in which the maintenance body exits
      early do not count: no stats record, a special-sequence presentation on screen (`022C2160` 5 or 6,
      `00310E02`–`00310E0E`), a field with the bit-15 permission (`00310E14`–`00310E1B`), or a unit outside the
      active branch of the lifecycle frame (a downed unit, `00233FD8`–`00233FEC`).
- [x] ~~What `BattleUnit_HasActiveEngagementEvidence` tests.~~ **Z-4 ANSWERED in section 8c** — an OR
      of a **global** class-2+ relationship query and a per-unit current-focus check.
- [x] ~~Whether `DAT_01DFE0B8` is the 2x/4x speed-mode scalar.~~ **Z-10 CLOSED 2026-09-08 — NO, it is
      the frame-rate scalar**, and this time on the readers rather than the writer. `01DFE0B4` has
      **212 references in 121 functions**, dominated by `imul <reg>, [01DFE0B4], N` with N = 30, 60,
      90, 150, 240, 900, 1200, 1500, 9000, 30000 — **authored 30 fps durations**. A game-speed
      selector makes durations elapse *faster*; this **multiplies every timeout**, which is
      frame-rate conversion. See the section at the end of this document.
- [x] ~~What the scheduler state block at `0x01DFE0B4`-`0x01DFE0BC` holds.~~ **Z-11 ANSWERED in
      section 8f** — the three fields are written **together by one function**, as an integer mode
      plus a scalar and its reciprocal.
- [x] ~~How much enmity an action generates.~~ **Z-5 ANSWERED in section 8e** — three authored
      per-action fields: `bEnmityDirectParam`, `bEnmityPropagationParam`, and
      `bEnmityRedistributionParam` (applied negated).
- [x] ~~How aggro spreads.~~ **Z-6 ANSWERED in section 8e** — no distance test: it walks the whole
      slot pool and propagates only to foes whose threat toward that character is **already nonzero**.
- [x] ~~The relation modes in `BattleTarget_MatchesRelationMode`.~~ **Z-7 ANSWERED in section 8f** —
      eight modes; mode 1 (`Foe:`) excludes un-provoked enemies, which is why gambits never start
      fights.
- [x] ~~What the `+0x54` key in relation modes 5 and 7 is.~~ **Z-12 ANSWERED 2026-09-12 (FABLE): the
      unit's script-assigned team.** Unit `+0x54` is the byte the script verb **`btlAtelSetBelong`**
      (`0x3006`, thunk `00510280`, [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)) sets through `00239170(actor, isLeader, team)` —
      `+0x54 = team` (`00239189`) and unit flag bit 15 = leader (`00239190` set / `002391A2`
      cleared); the installer and the reset write `0xFF` (`0023AC18`, `00236B3D`), so a unit no
      script has assigned belongs to no team ([the battle-unit field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) `+0x054`). Modes 5 and 7 therefore
      select **"a unit of my own team"** (7 excluding self), and mode 8 **"a unit of another
      team"** — the enemy-side vocabulary for coordinated groups the area scripts declare.
- [x] ~~What `BattleTarget_ClassifyRelationshipClass` returns beyond 1 (friendly) and 2 (hostile).~~
      **Z-13 ANSWERED 2026-09-12 (FABLE): nothing but 0.** `0030AB40` read whole: **0** when either unit is
      missing, either actor's class nibble (`ActorRuntime_GetClassNibble`, `actor + 0x0E & 0xF`) is **5**,
      or either unit lacks flag bit 4 (`0030AB93`–`0030ABB2`); otherwise each unit is put on the party
      side when its stats kind byte `+5` is 0 **or its class nibble is 3** ([the record kind byte](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md)), and the
      result is **1 (friendly) for the same side, 2 (hostile) for different sides — inverted when the
      acting unit is Confused** (status bit 5 of `+0x64 | +0x3C`), unless the caller's third argument has
      bit 0, which ignores confusion (`0030ABB8`–`0030AC25`). So `≠ 2` in the selector's opcode 34-26 means
      "friendly or unrelated".
- [x] ~~What maps to enmity ids beyond the four party slots. **Z-8** — the count itself is now tier 1
      (`< 0x28` loop bound in `BattleEnmity_WriteAllCombatantIds`).~~ **Z-8 ANSWERED 2026-09-12 (FABLE): the id is a
      row of the party definition table, not a slot.** Every write validates it with
      `BattleEncodedId_IsValidForClass(2, id)` (`003218F9`, `00321A6A`), and class 2 is `02EBF130`, the party
      definition table of 40 rows ([the class registry](../00-Engine-Core-Runtime/the-encoded-id-class-registry.md));
      the threat source `003216E0` requires a party-kind stats record (`+5 == 0`, `0032170D`–`00321714`) and passes
      its definition row, `byte [stats + 4]` (`00321723`–`0032172B`). So the 40 entries are threat toward rows 0–16
      (characters and guests), 17–25, 26 (the Chocobo) and 27–39 (the thirteen Espers)
      ([the kind page](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) AL-2) — enemy-kind sources
      raise no enmity through this path.
- [x] ~~The subgroup concept — what distinguishes subgroups within one order set.~~ **Z-9 — answered
      at the mechanism level 2026-09-03.** The subgroup is a **per-unit stored byte at
      `unit + 0x6B5`**, set by twelve direct-command ids `0x4116`-`0x4121` as
      `subgroup = (id & 0xFF) - 0x16`, mapping onto **0-11 with no gap and no overlap**; the walk
      consumes it as both a prefix-sum bound and the index of its own count byte. Full reading in
      [`which-gambit-set-fires-and-how-a-command-switches-it.md`](which-gambit-set-fires-and-how-a-command-switches-it.md).
      **The box is ticked for the mechanism only** — *what each of the twelve subgroups means in
      authored data is not read*, and is carried below as its own question rather than left inside a
      ticked one. *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): answered since. UQ-121, the box below, is ANSWERED 2026-09-26: a subgroup has no table-wide meaning and is a state of its own set's order graph. Its residue, GR-9, is ANSWERED 2026-09-30.)*
- [x] **UQ-121.** *(status restated in the register 2026-09-26, FABLE, Claude Opus 5.5: see the row)* **What each of the twelve subgroups means in authored data.** The selector and its range are
      established; the content is not. **Successor to Z-9.**
      *Narrowed 2026-09-15 (FABLE) from authored data — PARTIAL: a subgroup has no table-wide meaning; it is a state
      of its own order set's authored graph.* The census covers all 166 `.ard` order-set directories: 1,422 sets and
      50,050 records, the loader page's counts.
      - **The switch commands are written inside the sets.** 1,189 sets contain order records whose action selector is
        `0x4116 + n`, the command that stores subgroup `n` into `+0x6B5`. There are 16,960 such records, all direct
        selectors, none reached through a weighted list.
        - 9,564 switch forward, 6,593 back and 803 to the subgroup they sit in.
        - **Every one targets a subgroup that has records in that set.**
        - The most common edges are 0→1 (1,239), 4→5 (978), 3→5 (854) and 3→4 (762), but back-edges such as 4→2 and
          2→0 are common too. The graph is not a fixed escalation ladder.
      - **Subgroups are used as prefixes.** All 1,422 sets populate subgroup 0; usage then falls monotonically, from
        1,187 sets with subgroup 1 to 63 with subgroup 11.
      - **1,267 sets are closed** under their own switches: every populated subgroup is reachable from subgroup 0. Of
        these, 233 have no switch and only subgroup 0.
      - **155 sets are not closed.** Some populated subgroup is never targeted from the set's own reachable part, so
        something outside the set must enter it. ~~Candidates: a unit's other variant set (the unit row names four,
        `+0x50 + 2k`), a direct command, or a script. Which one is not read.~~ **Two of those routes are excluded
        (2026-09-15):**
        - **Not another variant set.** Only three instructions write `+0x6B5`: the reuse reset `00236BA3`, the
          subgroup command `002FE0BB`, and `002FE09F`, which **zeroes** it in the arm for the variant commands
          `0x4112`–`0x4115`. Changing variant restarts at subgroup 0, so no subgroup carries across. As a check, taking
          the union of switch edges over every set that the same unit rows name closes only 1 of the 155
          (`work/FABLE/drift4/uq121_variant_reach.py`).
        - **Not a script literal.** The decompiled `us` corpus contains no integer 16,662–16,673 (`0x4116`–`0x4121`); the
          only near match is the float `16669.9219`. No weighted list contains the commands either.
        - **What remains:** a subgroup command with a computed id, whose source is not read, or subgroups that are
          authored but never entered. Static evidence does not separate the two. **Registered 2026-09-30 as GR-9**, the one residue UQ-121's answer leaves.
          *(Answered 2026-09-30, OPUS `a93fa5c08`; register row GR-9, record [`gr9-order-subgroup-entry-0930`](../_index/candidates/gr9-order-subgroup-entry-0930/README.md): no run-time order id reaches an enemy's subgroup - the only run-time id is the player's battle-menu command for the focus units - so the unreached subgroups are authored and never entered.)*
      - **So "what subgroup *k* means" is a per-set fact.** It is the condition set on the orders that switch into it,
        and reading it means reading each set's selector operands. This census reads the graph, not the conditions.
      ***UQ-121 ANSWERED 2026-09-26 (register row):** subgroups have no table-wide meaning; each one's meaning is the
      per-set condition on the orders that switch into it. What enters the 155 sets' outside-entered subgroups is
      GR-9. Note (FABLE, Claude Opus 5.5, 2026-09-30).*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| First-match-wins evaluation | complete loop in `00305CC0` | 1 |
| Records 24 bytes, header 32 bytes | `(a+b+c) * 0x18 + 0x20` address arithmetic | 1 |
| Condition **and** commit must both succeed | the `&&` chain guarding the `return 1` | 1 |
| ~~`0xFFFF` no-target sentinel~~ `0xFFFF` is the action slot's initial value (the slot is the evaluator's action out) | `local_res8[0] = 0xffff` initialisation; `00301500`, `00305DE3` (*corrected 2026-09-26, FABLE*) | 1 |
| Resume flags `0x40` / `0x80` / `0x4000` | the guard expressions in the loop | 1 |
| Decay is exactly `-10` | `BattleEnmity_WriteAllCombatantIds(unit, -10, 0)` | 1 |
| Engagement suppresses decay | timer written 0 whenever engagement evidence is present | 1 |
| Highest-relevant scans the four party slots | `BattleUnit_BuildFilteredFourSlotUnitBuffer(&buf, 1)` loop | 1 |
| Enmity indexed `table[id + 1]`, byte 0 is the timer | the scan reads `+1`; decay reads/writes byte 0 | 1 |
| 40-entry vector at BKEI `+0x1A..+0x41` | ~~GFZ annotation; the range is consistent with the `+1` indexing read here~~ `lea [rax + 0x19]` on `unit + 0x6A0` (`0032156D`, `00321D61`) and the loop bound `cmp ebx, 0x28` (`00321DA3`), section 8k | ~~3~~ 1 |
| Foe gate shared with EXP/LP | same `wDefinitionSelector[+1] == 1` test, found independently in three functions | 1 |
| Three gambit banks per character, one selected | ~~`GambitConfig_InitializeThreeBanksFromBasePairs` name + the config family~~ the three stores `00326057`–`00326109` (`0x9C` = 3 × `0x34` per member), the three-bank clamp loop `00327994`, the selected-bank read `00327C63` ([the battle-state block](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) `+0x7370`); re-tiered 2026-09-30 | ~~3~~ 1 |
| The complete condition language: 70 opcodes over 31 bodies | jump tables `00303680` / `00303604`, every body read (section 8b, Z-1) | 1 |
| Relation modes 0–10; the idle-foe exclusion is in mode 1 only | complete body of `0030BD00` (sections 8f, 8i) | 1 |
| Mode 0 is unreachable from authored data | an entry whose first word is 0 is skipped (`00301685`–`0030168A`); the 256 gambit conditions and 50,050 enemy records (section 8i, Z-15) | 1 |
| The 24-byte order record: `+0` selector, `+2` percent, `+4` flags, three 6-byte entries | reader `003014F6`, `0030162F`, `003015A6`, `00301681`; writer `00328140` (section 8l, Z-2) | 1 |
| Entries chain only under the flag pair; the pick reads the first entry's buffer | `003016BE`–`0030174E` (the next input is the copy), `00301750`–`00301768` (the next input is the original list, into a buffer of its own), `003016AF` (an entry that finds nobody fails the order), `003017B7` | 1 |
| `0x400` skips targets held by three attackers; `0x1000` returns the cancelled target | `00301E8E`–`00301E9D`; `00301E76`–`00301E88` → `00303598`–`003035BC` | 1 |
| Ties in the final pick go to the shared LCG or to the nearest | `003087E0`: `00308B13`, `00308B5D` | 1 |
| A weighted action is rolled on bit 15 of the selector | `00308EC0` (section 8i) | 1 |
| Enmity writes: delta or set, floor at 1, +10 on a first rise, a first grudge raises every zero entry to 1 | `00321850`: `0032191D`–`003219AD`; clamp `00321E40` | 1 |
| Threat spreads only to foes already holding threat | `003219D0` (section 8e, Z-6) | 1 |
| Engagement is a global OR a per-unit clause | `00307CE0` (section 8c, Z-4) | 1 |
| The decay interval is one second at either frame limit | `0032157F`–`00321598`; the triple `01DFE0B4`–`01DFE0BC` written from FrameLimit by `001EDDC0` (Z-3, Z-10, DH-1) | 1 |
| The threat table is in the keep bank and follows its restore or wipe | `0032156D` on `unit + 0x6A0`; the window compare `002337DE`–`00233801` (section 8k) | 1 |
| Selection runs each frame in resume mode, and fresh from a queue | `0030874C`, `003086AF`–`003086DA`, `00313CF7`, `00313D89` | 1 |
| Preset rows: 40 × 64 bytes at `02EBF0E0` | `00327CB0` (section 4) | 1 |
| Action / condition compatibility | `00327A10`: `00327B10`–`00327B7B` | 1 |
| Opcodes 48 / 49 operands 1–2 test the field's MP regime | `00303043`, `00303052` → `00320160` → `00377BA0` ([the field-record accessors](../03-World-Area-Field/CONTRACT-field-record-accessors.md), C-11) | 1 |

**Superseded readings** *(collected (FABLE, Claude Opus 5.5, 2026-09-30))*: `0xFFFF` as a no-target sentinel (it is the action slot, 2026-09-26); "a satisfied condition can still do nothing" (a matched line always commits, 2026-09-26, and the section 6 bullet, 2026-09-30); an eight-case relation switch (eleven, section 8i); the Z-10 "shutdown restore" (section 8f); "gambits never start fights" (narrowed, section 8i); "each entry narrows the candidate set" (only under the flag pair, section 8l, 2026-09-30); the return window as `30 ×` the window (the scalar multiplies it, section 8k, 2026-09-30).

### The third sighting of one constant

The foe-class gate `wDefinitionSelector[+1] == 1` now appears in three separately-read functions:
EXP award, LP award, and enmity decay. Like the `0x80000003` status mask before it, it was found by
**recognising a constant recorded exactly in an earlier document**, not by searching for it.

That is the second time this has happened, and it is an argument for the house style: recording
`0x80000003` and `wDefinitionSelector[+1] == 1` verbatim rather than paraphrasing them as "a status
check" and "a foe check" is what made both recognisable.

### What is deliberately not claimed

The GFZ annotations on these functions are unusually confident — `V16 VERIFIED`, `PROVEN
LIFECYCLE`, `PROVEN MODE-1 ROLE`. Several assert things this pass did not verify: that mode 1 of
`BattleTarget_MatchesRelationMode` consumes `HasAnyPositive` for a specific pairing rule, and the
exact BKEI offset range.

Those are recorded at **tier 3** and flagged, not promoted. The tier-1 claims here are only what
was read in the bodies. `AiOrder_EvaluateTargetSelector` is 6,963 bytes and **unread** — so nothing
in this document describes the gambit condition language itself, which is the part a reader would
most want. Section 7 says so as **Z-1** rather than filling it from the GFZ's prose. *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): stale. Z-1 is ANSWERED 2026-09-12 and the evaluator is read whole in section 8b; the note below says so.)*

> *Superseded (note (FABLE, Claude Opus 5.5, 2026-09-30)): all three were read later at tier 1 — the mode-1 clause of `BattleTarget_MatchesRelationMode` (section 8f, re-read in 8i), the BKEI offsets (section 8k: base `+0x19`, 40 entries), and the evaluator itself (section 8b; Z-1 answered 2026-09-12).*

## 8b. Reopened 2026-09-02 - Z-1: the condition language, read

`AiOrder_EvaluateTargetSelector` (`00301AD0`, 6,963 bytes) was decompiled. It is not a boolean
condition test - it is a **candidate filter and a running best-of selection**, and its shape
explains the gambit vocabulary directly.

### Signature and dispatch

```c
int AiOrder_EvaluateTargetSelector(FFXII_BattleUnit_Partial *unit,
                                   FFXII_AiOrderRecord_Partial *order,
                                   ushort action_id, int selector_index,
                                   void *input_candidates, void *output_candidates)
{
    relation = order->targetSelector[selector_index].wOperand;
    opcode   = order->targetSelector[selector_index].bSelectorOpcode;
    operand  = <sub-selector byte>;

    seekMin  = ~opcode & 1;
    best     = seekMin ? 0x7FFFFFFF : 0x80000001;    // seed so the first candidate always wins

    if (opcode == 1) return ...;                      // trivial case

    for (each candidate in input_candidates) {        // stride 0x10
        cand = ActorWork_GetBattleUnit(candidate.actor);
        if (!cand) continue;
        if (!BattleTarget_MatchesRelationMode(unit, cand, relation)) continue;
        if (BattleTarget_HasLow16EligibilitySuppression(cand, unit)) continue;
        switch (opcode) { ... switch (operand) { ... } }   // read a field, compare against best
    }
}
```

**This partly answers Z-2.** The AI order record contains an array `targetSelector[]` indexed by
`selector_index`, and each entry has at least a **`wOperand`** (the relation - Ally / Foe / Self)
and a **`bSelectorOpcode`**.

### Why the cases come in pairs - one bit is highest-vs-lowest

The outer switch cases pair up throughout: `2/3`, `6/7`, `8/9`, `0xA/0xB` ... `0x22/0x23`. The
seed line is the whole explanation:

```
seekMin = ~opcode & 1
best    = seekMin ? 0x7FFFFFFF : 0x80000001
```

An **odd** opcode seeds `best` to `INT_MAX`, so every comparison keeps the smaller value -
**lowest**. An **even** opcode seeds `0x80000001`, so every comparison keeps the larger -
**highest**. Confirmed in the case 2/3 body, which rejects a candidate when
`value < best` only on the even path.

**"Foe: highest HP" and "Foe: lowest HP" are the same opcode differing in bit 0.**

### Z-1 answered 2026-09-12 (FABLE) — the complete outer-opcode table, joined to the shipped sets

The selector entry is three words: **`+0` the relation word** (mode 0–10 of §8i; in the self-condition
family its high nibble and low byte are a storage kind and an index instead), **`+2` = `opcode` (high
byte) and `operand` (low byte)**, **`+4` an s16 `threshold`** (`00301B0F`–`00301B1F`). The dispatch is
`opcode == 1` → done; `opcode` 52 / 53 → a slot scan; 54 / 55 with `operand` 0–2 → a self-condition;
everything else → the candidate loop, whose 70-entry jump table (`00303680` indices, `00303604`
targets, image-relative) has **31 case bodies**. Every body was read; the counts are over the 50,050
records of the 166 `in` area files (§7a). **Direction convention:** `r12 = (~opcode) & 1`, so an
**even** opcode is the "true / highest / ≥" reading and its **odd** twin the "false / lowest / <"
reading — except the float families (distance, angle), where even is `<` and odd `≥`. "HP" below is
**`AiOrder_ComputeBoundedSelectorScalar`** (`00308C20`): the candidate's current HP (or MP) **plus the
predicted effect of every action already committed against it** (each slot in its
`committedAttackerSlotMask` `+0xEA4` whose action row has `+0x2C` bit 12 for HP / bit 15 for MP,
through `00308B90`), clamped to the cap — the AI reasons on *predicted* HP, not displayed HP. The cap
is `max(HP, 1)` under Disease, else max HP, doubled under Bubble.

| opcode | records | body | condition |
|---|---:|---|---|
| 0 | 1,024 | `00301ECC` | any — every candidate kept |
| 1, 4, 5, 18, 19, 30, 31, 50, 51 | 0 | default | no filter |
| **2 / 3** | 4,087 / 9,937 | `00301EF7`, sub-table `003036C8` | **highest / lowest** of a value chosen by `operand`: 0 Attack `+0x2E`, 1 Defence `+0x2F`, 3 Magick Resist `+0x30`, 4 predicted HP, 5 predicted MP, 6 level `+0x1C2`, 7 surface distance to the acting unit (float), 8 `committedAttackerCount` `+0xEA8`, 9 the HP cap, 10 max MP (0 with a negative MP layer byte), 12 Strength, 13 Magick Power, 14 Vitality, 15 Speed, 17 **the acting unit's enmity toward the candidate** (`BattleEnmity_ReadForCombatantId`, party-kind candidates only; opcode 2 also requires it non-zero) — 2 / 11 / 16 keep. Shipped: 3-7 "lowest distance" ×8,910, 2-17 "highest enmity" ×3,839, 3-4 "lowest HP" ×826 ([the battle-stats field map](../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md)) |
| **6 / 7** | 280 / 4,160 | `003021A3` | status `operand` **present / absent** in `+0x64 \| +0x3C` ([the thirty-two statuses](../10-Status-Periodic-Terminal/the-thirty-two-statuses.md)). Shipped: 7-23 "not Reflect" ×1,055, 7-13 "not Disable" ×494, 7-18 "not Protect" ×349, 6-13 "Disabled" ×55 |
| 8 / 9 | 0 / 12 | `003021CC` | `definitionTypeByte` `+0x55` == `operand` / ≠ |
| 10 / 11 | 72 / 4 | `003021EC` | `definitionCategoryByte` `+0x56` == `operand` / ≠ |
| 12 / 13 | 0 | `003021F3` | bit `operand` of `definitionWord80` `+0x52` set / clear |
| **14 / 15** | 597 / 3,000 | `00302203` | **predicted HP as a percent of the cap ≥ / < N**, N = `00D102E0[operand]` = 90, 80, 70, 60, 50, 40, 30, 20, 10, 0, 500, 1000 (operand 0 → the threshold word); the candidate is appended with its percent. Shipped: 15-4 "HP < 50 %" ×2,053, 15-7 "< 20 %" ×447, 14-4 "≥ 50 %" ×492 |
| 16 / 17 | 0 | `003022FC` | the HP cap ≥ / < `00D10308[operand]` = 500, 1000, 2000, 5000, 10000, 20000, 30000, 50000, 100, 200, 300, 500 |
| 20 / 21 | 76 / 0 | `003023A5` | affinity byte `+0x40` bit `operand` — **weak to element** / not |
| 22 / 23 | 22 / 84 | `003023C9` | affinity byte `+0x41` bit `operand` — **absorbs element** / not |
| 24 / 25 | 40 / 0 | `003023ED` | stats word `+4` (the definition row index) == `operand` (0xFF → 0xFFFF) / ≠ |
| 26 / 27 | 0 | `00302416` | equipment slot `operand` (0–5, `+0x50`) occupied — neither 0xFFFF nor 0x1000 |
| 28 / 29 | 0 | `00302451` | `BattleUnit_GetPrimaryFormulaResourceByte26` == `operand` / ≠ |
| **32 / 33** | 1,160 / 1,757 | `00302478` | **effect id `operand` set in either 128-bit layer** (`+0x68` / `+0x78`) / clear. Shipped: 53 (×544), 50, 55, 56, 49, 48, 54, 2, 4 |
| **34 / 35** | 11,487 / 10,176 | `003024B0`, sub-table `00303710` | by `operand`: 0 has a group leader (`+0x24`); 1 is the party's focus (`PartyFocus_IsCurrentPackedActorHandle`); 2 is its own group leader (`+8 == +0x24`); 3 party-kind with kind byte 7–25; 4 party-kind with kind byte 27–39 (the Espers); 8 **`BattleEnmity_GetHighestRelevant` ≥ / < threshold**; 9–12 **any unit in the candidate's perception cache** (`+0xBC4` / `+0xBC8`) whose team `+0x54` (9) / status bit (10) / `+0x55` (11) / `+0x56` (12) equals the threshold; 13 enemy-kind whose definition row byte 3 has 0x10; 16 level ≥ / < threshold; **17 distance from the acting unit's own record `+0x50` point** (enemy kind only); 18 distance to the nearest / farthest of the four party members; 19 distance to the party leader; 20 distance to the acting unit's group leader; 21 the party leader's heading toward the candidate (`Vector3_ComputeXZHeadingOrFallback`, `Math_NormalizeAngleDifference`) vs threshold; 24 the candidate's focus `+0x710` is the acting unit's group leader; 25 … is the acting unit; 26 `BattleTarget_ClassifyRelationshipClass(unit, candidate's focus)` ≠ 2; 27 … is the unit with combatant id `threshold`; 28 the acting unit's heading toward the candidate vs threshold; **29 distance between the acting unit and the candidate vs threshold**; 30 / 31 status word `+0x64` masked by the two runtime status masks `0208D320` / `0208D324`; 32 weapon slot's runtime category (`BattleDefinition_GetRuntimeCategoryBySelector`) == 4; 5–7, 14, 15, 22, 23 keep. Shipped: 34-17 ×5,738 (thresholds 40 / 4 / 20 / 1), 35-29 ×2,311 (20 / 6), 35-19 ×1,922, 35-21 ×1,762, 35-28 ×1,738, 34-29 ×1,571 |
| 36 / 37 | 770 / 365 | `00302C8F` | distance from **POSENT entry `operand + 1`** (`FieldData_GetFormat0RecordVectorByIndex`, [the POSENT table](../25-EBP-Script-Container/Sections/section-016.md)) < / ≥ threshold |
| 38 / 39 | 6 / 10 | `00302D1F` | distance from the unit named by **definition selector `operand`** (`BattleUnit_FindByDefinitionSelector`) < / ≥ threshold |
| 40 / 41 | 0 | `00302DB4` | **missing HP** (cap − predicted HP) ≥ / < `00D10328[operand]` = 100, 200, 300, 500, 700, 1000, 2000, 3000, 4000, 5000 |
| 42 / 43 | 0 | `00302E80` | predicted HP ≥ / < `00D10350[operand]` = 100000, 50000, 10000, 5000, 3000, 2000, 1000, 500, 75, 50 |
| 44 / 45 | 0 / 18 | `00302F17` | **predicted MP as a percent of max MP ≥ / <** `00D10370[operand]` = 75, 50, 25, 10, 20, 30, 60, 90, 120 |
| 46 / 47 | 0 / 11 | `00302F7E` | `operand` 0: predicted HP ≥ the cap (**HP full**); 1: predicted MP ≥ max MP (**MP full**) |
| 48 / 49 | 17 / 0 | `00303027` | `operand` 0: `00263E10()` == threshold; 1: `00377BA0()` == threshold; 2: `00377BA0()` ≥ threshold — ~~two global getters, unread~~ *(2026-09-27, FABLE, Claude Opus 5.5: `00263E10` returns the field's **environment class** `02099DA8`, `GB-2`. All 17 shipped records use operand 0 with threshold 0, so they act only while the class is Rain. ~~`00377BA0` reads a per-field table and stays unread~~; no shipped record uses operands 1 or 2)* *(read 2026-09-30, FABLE: `00377BA0`, reached through the thunk `00320160` at `00303043` / `00303052`, returns bits 12–13 of the active field's record, the field's **MP regime** 0–3, or a saved value when the save override is on — [the field-record accessors](../03-World-Area-Field/CONTRACT-field-record-accessors.md) §7, C-11)*; the candidate list is untouched |
| **52 / 53** | 168 / 0 | `00301CFB` | **a slot scan, not a filter**: every in-play unit of kind `operand` with flag bit 4, whose actor record `+0x15` (`handleTag4`) equals the threshold and whose `+0xEA4` is 0, is appended (`00301D20`–`00301D96`) |
| **54 / 55** | 6,214 / 4,337 | `00301C2B` (operand 0–2) / `00303079` (operand 3) | **the self-condition family.** Operand 0–2: `AiTargetSelector_ResolveOperandValue(kind = relationWord >> 12, index = relationWord & 0xFF)` on the **acting unit**, then `== threshold` (0), `≥ threshold` (1) or `bit threshold set` (2); operand 3: bit `threshold` of the **candidate's** `+0xB90` word (kind 10). The kinds are the ten script-variable accessors of [the record behind every actor](../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md): 1 the scratch bank, 2 the persistent bank, 3 the `+0x48` local storage ([the storage-class page](../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md)), 8 a persistent flag, 9 the sixteen-word table `0208D334`, 10 unit `+0xB90`. Shipped: `0x900F` (kind 9, word 15) bit-tests ×2,169, `0x900D` word 13 ×1,242, `0x900C`, `0x900E`, `0x1001` (scratch word 1) ×189, `0x2001` (persistent word 1) ×68 — **enemy scripts and enemy AI share state through these words** |
| 56 / 57 | 254 / 0 | `003030A7` | `operand` 2: the candidate's current action (`+0x714`, ≤ 0x21E) has row byte `+0x1E == 1`; 1: the candidate is the group target focus (`+0x750`) of the acting unit (or of the group leader); 0: `BattleUnit_TestActorViewFrustumAtCurrentPosition` **and** nearest / farthest by distance |
| **58 / 59** | 211 / 1,013 | `003031C4` | **the number of units in the candidate's perception cache matching relation `operand`** (`BattleTarget_MatchesRelationMode(candidate, entry, operand)`) ≥ / < threshold; operand 0 counts the whole cache. Shipped: 59-1 "fewer than 1 foe perceived" ×949, 58-5 "≥ 2 of the same team" ×180 |
| 60 / 61 | 200 / 1 | `0030329B` | team byte `+0x54` == threshold / ≠ (Z-12) |
| 62 / 63 | 104 / 62 | `003032A7` | predicted MP percent ≥ / < **`operand × 10`** |
| 64 / 65 | 0 | `003032C0` | with `operand`: `BattleAction_GetSubtype3Field22OrFFFF(actionId)` through `BattleEncodedId_DispatchQueryMode0Value` ≥ `operand × 10` (cached); when that fails the candidate must be enemy-kind |
| 66 / 67 | 18 / 292 | `00303334` | **someone committed against the candidate** (a slot in its `+0xEA4` mask whose target-buffer entry 0 is the candidate, with a valid class-20 action): `operand` 0 that action == threshold; 1 `BattleAction_ComputeActiveTargetStatusIntersection`; 2 its row `+0x2C` bit 12 (**an HP-affecting action**); 3 bit 15 (**an MP-affecting action**) — true / false. Shipped: 67-0 ×279 "no one is using action N on it" |
| 68 / 69 | 0 | `00303523` | the battle-state block's timer `+0x5AD8` ([the battle-state block](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)) ≥ / < `00D10380[operand]` = 20, 30, 60, 90, 120 — global, list untouched |

Two corrections to the tier-3 table that follows: its "operand" column mixes the **opcode** (the
high byte — 0x0B, 0x15, 0x17 …) with the sub-selector of opcodes 2 / 3, and several rows named
fields that are read by a *different* opcode than the one listed. The table above is the reading
from the bodies; the older table is kept as the history of how the categories were first found.

### The operand vocabulary, mapped to real fields

The inner switch selects *which* field is compared. Read directly from the case bodies:

**Combat stats** (BKBI):

| Operand | Field |
|---|---|
| `0` | `bAttackPower` |
| `1` | `bDefense` |
| `3` | `bMagickResist` |
| `6` | `bLevel` |
| `0x0C` | `bStrength` |
| `0x0D` | `bMagickPower` |
| `0x0E` | `bVitality` |
| `0x0F` | `bSpeed` |

**Identity and affinity:**

| Operand | Field | Player-facing meaning |
|---|---|---|
| `0x07` | `dwStatusMaskMode0_3` | status conditions |
| `0x09` | `bAuthoredClassification` | authored class |
| `0x0B` | `bGenusId` | **creature type** - the "Foe: type" gambit family |
| `0x0D` | `wAuthoredClassAttribute` | class attribute |
| `0x15` | `bElementWeakMask` | **elemental weakness** |
| `0x17` | `bElementAbsorbMask` | **elemental absorption** |
| `0x19` | `wDefinitionSelector` | definition selector |
| `0x1B`, `0x21` | `aStatusParameterDwords` | status parameters |

**State and behaviour:**

| Operand | Field | Player-facing meaning |
|---|---|---|
| `0x01`, `0x02`, `0x39` | `dwFieldId` | which unit / area identity |
| `0x10` | `bLevel` | level |
| `0x15`, `0x1C` | `locomotion` | **movement mode - "flying"** |
| `0x18`-`0x1B` | `dwTarget_focus` | **what the candidate is currently targeting** |
| `0x1E`, `0x1F` | `dwStatusMaskMode0_3` | status again, different comparison |
| `0x20` | `wPrimaryFormulaResourceSelector` | formula resource |
| `0x0C`, `0x3B` | `field_0xbc4` | unidentified |
| `0x3D` | `field_0x54` | unidentified |

Several operand indices appear in more than one outer case with different meanings, so **the
operand namespace is per-opcode-family, not global**.

### What this is in player terms

Every gambit condition FFXII offers is one of these reads plus a direction bit:

- **"Foe: HP = lowest"** - operand on an HP field, odd opcode.
- **"Foe: flying"** - the `locomotion` operand.
- **"Foe: weak to Fire"** - `bElementWeakMask`.
- **"Foe: targeting self"** - `dwTarget_focus`.
- **"Foe: Undead"** - `bGenusId`.
- **"Ally: status = X"** - `dwStatusMaskMode0_3`.

And every one is filtered first by `BattleTarget_MatchesRelationMode(unit, candidate, relation)`,
which is the **Ally: / Foe: / Self:** prefix in the menu.

### What is still not read

*Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): nothing in this subsection is still open. The opcode numbering is the Z-1 table above (ANSWERED 2026-09-12). The threshold is the selector entry's `+4` s16 word (`00301B1F`), compared by that table's bodies. The unidentified fields are named in the note at the end of this subsection.*

The **outer opcode numbering** is not fully mapped - the categories were identified by the fields
they read, not by an authored table naming them. The comparison threshold path (`local_res20` as a
literal rather than a running best) is only partly followed, and several operands land on
unidentified fields.

So **Z-1 is substantially advanced, not closed**: the *shape* of the condition language, the
highest/lowest bit and the operand-to-field map are tier 1; a complete opcode table is not. ~~It stays
OPEN with this progress recorded.~~

> *Historical (note (FABLE, Claude Opus 5.5, 2026-09-30)): Z-1 was ANSWERED on 2026-09-12. The complete outer-opcode table, with its threshold tables and operand sub-tables, is the table under "Z-1 answered 2026-09-12" above. The older operand table's "unidentified" fields are named there: `+0xBC4` / `+0xBC8` is the perception cache (opcodes 34 / 35 operands 9–12, 58 / 59) and `+0x54` the team byte (Z-12). This subsection records the state of 2026-09-02.*

## 8c. Reopened 2026-09-02 - Z-3 and Z-4: the decay interval and the engagement gate

### Z-4 answered - what suppresses forgetting

`BattleUnit_HasActiveEngagementEvidence` (`00307CE0`, 47 bytes) is a two-clause OR:

```c
undefined8 BattleUnit_HasActiveEngagementEvidence(unit)
{
    if (BattleUnit_HasRelationshipClass2PlusInSlotMask() == 0) {
        r = BattleUnit_HasCurrentFocusEngagementEvidence(unit);
        if ((int)r == 0) return r;          // 0 -> not engaged, decay may run
    }
    return 1;                                // engaged -> timer held at 0
}
```

**A unit counts as engaged if either:**

1. `BattleUnit_HasRelationshipClass2PlusInSlotMask()` - **takes no argument**, so it is a global
   query: is *any* class-2-or-higher relationship present in the slot mask? While anything anywhere
   is in that state, **every** foe's threat decay is suppressed.
2. `BattleUnit_HasCurrentFocusEngagementEvidence(unit)` (`0030BB30`, 257 B) - a per-unit check that
   this particular unit is the player's current focus.

The first clause is the load-bearing one and is easy to misread: it is **not** per-unit. A global
engagement state freezes threat decay across the board, not just for the unit being examined.

A third related function exists, `BattleUnit_HasNonPartyEngagementEvidence` (`00308040`, 237 B),
which this gate does not call.

### Z-3 answered - the interval is 30, and it scales with the global time base

```
interval = DAT_01DFE0B8 * DAT_008F8D80
```

Both read directly out of the shipping image:

| Symbol | Section | Bytes | Value |
|---|---|---|---|
| `DAT_008F8D80` | `.rdata` | `0000f041` | **30.0f** - a constant |
| `DAT_01DFE0B8` | `.data` | `0000803f` | **1.0f** - an initialised, writable scalar |

So at the default the interval is **30**, and enmity drops by 10 each time it elapses.

`DAT_01DFE0B8` is not a constant. A scan of `.text` for RIP-relative `MOVSS` against it found:

```
READ  (f3 0f 10 /r)   39 sites
WRITE (f3 0f 11 /r)    1 site   -> 0x001EDDD8, inside FUN_001EDDC0 (CoreRuntimeScheduling)
```

**One writer, thirty-nine readers.** ~~And the writer is the host-timing initialiser - `FUN_001EDDC0`
calls `timeGetDevCaps` and `timeBeginPeriod`.~~ **The writer count holds; the read count and the
identification do not — see section 8f.** `FUN_001EDDC0` has **two branches**, and the write is on
the branch that calls **`timeEndPeriod`**, not the one that calls `timeGetDevCaps` /
`timeBeginPeriod`. The function was identified from the branch that does not contain the write.

So `DAT_01DFE0B8` is a **global scalar owned by the core scheduler and consulted by 45 systems
engine-wide** (39 was a `MOVSS`-only count).

> **Correction, 2026-09-02 (see section 8d).** This section originally continued: *"Enmity decay
> timing is not fixed - it scales with the engine's global time base."* **That was wrong.** The
> single writer sits on a shutdown path, so the scalar holds `1.0f` throughout play and the interval
> is a flat **30**. The sentence is struck rather than deleted, because the reasoning that produced
> it - one writer, 39 readers, therefore "dynamic" - is a mistake worth leaving visible.

**What is still not established: the unit.** 30 of *what* - frames, ticks, milliseconds - is not
proven here. A 30.0f constant multiplied by a time scale is suggestive of a frame count at 30 fps,
which would make the decay one step per second, but nothing read says so. ~~**Z-3 remains OPEN on the
unit only**~~; the operands and their values are now exact. *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): the unit is answered, one second of maintained field frames (Z-3, section 7's box, ANSWERED in the register); see the note below.)*

> *Historical (note (FABLE, Claude Opus 5.5, 2026-09-30)): the unit was answered on 2026-09-12 — one second of maintained field frames (Z-3, section 7's box). Section 8d's "flat 30" was itself superseded by section 8f: 30 frames at FrameLimit 30 and 60 at FrameLimit 60.*

**The inference I am not making:** FFXII: The Zodiac Age has 2x and 4x speed modes, and a single
writable global time scalar read by 39 systems is exactly what such a feature needs. That is a
plausible identification and it is *not* proven - the writer read here does timer-period setup, not
speed selection. Recorded as **Z-10** rather than asserted. *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): Z-10 is CLOSED NO 2026-09-08. The scalar is the frame-rate factor, not a speed mode; section "Z-10 closed" below.)*

## 8d. Reopened 2026-09-02 - Z-10 answered NO, and a correction to section 8c

Chasing Z-10 - whether `DAT_01DFE0B8` is FFXII's 2x/4x speed-mode scalar - **disproved the framing
section 8c had just put on it.**

### The single writer, read in full

```c
void FUN_001eddc0(int param_1)
{
    if (param_1 == 0) {                          // STARTUP
        if (timeGetDevCaps(caps, 8) == 0) {
            DAT_01f82e40 = caps[0];
            timeBeginPeriod(caps[0]);            // raise timer resolution
            DAT_01f82e3c = 1;
        }
    }
    else {                                       // SHUTDOWN / RESET
        DAT_01dfe0b8 = DAT_01cebc08;             // <- the only write, restoring a default
        DAT_01dfe0bc = DAT_01cebb70;
        DAT_01f82e38 = 1;
        _DAT_01dfe0b4 = 2;
        FUN_0033f020();
        if (DAT_01f82e3c != 0) { DAT_01f82e3c = 0; timeEndPeriod(DAT_01f82e40); }
    }
    ...
}
```

It is an **init/shutdown pair for the Windows multimedia timer period**. The write to
`DAT_01DFE0B8` is on the *shutdown* branch and restores a stored default from `DAT_01CEBC08`. It
is not a speed selector, and it does not run during play.

### The write scan, widened

Section 8c scanned only `MOVSS` stores. That was too narrow to support a claim about *all* writes,
so every plausible 32-bit store encoding was checked against the address:

```
movss   f3 0f 11 /r      1 site   -> 0x001EDDD8   (the one above)
movups  0f 11    /r      1 site   -> 0x001EDDD9   (the SAME instruction, matched one byte in)
movsd   f2 0f 11 /r      0
movaps  0f 29    /r      0
movd    66 0f 7e /r      0
mov     89       /r      0
mov     c7       /0      0
```

**Exactly one write instruction exists in the entire `.text`.** The second hit is my own scanner
matching the `0f 11` embedded inside `f3 0f 11` - an artifact, not a second site.

### What follows

- **Z-10: NO.** `DAT_01DFE0B8` is not the speed-mode scalar.
- **During normal play the value is its `.data` initial `1.0f`**, because nothing writes it outside
  teardown. All 39 readers see 1.0.
- **The enmity decay interval is therefore a flat `1.0 x 30.0 = 30`**, not a scaling quantity. The
  "scales with the global time base" statement in section 8c is retracted there.
- `_DAT_01DFE0B4`, `DAT_01DFE0B8` and `DAT_01DFE0BC` are reset together, so they form a small
  scheduler state block at `0x01DFE0B4`, not three unrelated globals. **Z-11.**

> *Superseded by section 8f and the Z-10 closure (note (FABLE, Claude Opus 5.5, 2026-09-30)): the writer runs at startup with the FrameLimit mode, so the scalar is `1.0` or `2.0` for the whole process and the interval 30 or 60 frames, one second either way.*

**The remaining honest caveat:** this proves nothing in `.text` writes the value. A data-driven
initialiser or a `memcpy` from a config blob would not appear in an instruction scan. The claim is
"no code writes it during play", not "the value can never change".

### Why this correction happened

Section 8c reasoned: *one writer, 39 readers, therefore a live dynamic scalar.* The writer count was
right and the conclusion did not follow - **I never checked what the writer does or when it runs.**
"One writer" says nothing about whether that writer executes during gameplay.

That is the same failure shape as the two narrow-test false negatives already on file, inverted: a
too-narrow *observation* supporting a too-broad *claim*. The rule that catches it is the same -
finish the derivation before generalising from it.

## 8e. Reopened 2026-09-02 - Z-5 and Z-6: how threat is generated and spread

### Z-5 answered - three authored parameters per action

```c
void BattleEnmity_ApplyActionParameters(caster, target, action_def)
{
    if (caster && caster->pBkbi
        && caster->pBkbi->wDefinitionSelector[+1] == 0)        // caster must be party-class
    {
        id = (byte)caster->pBkbi->wDefinitionSelector;          // low byte = combatant id

        BattleEnmity_WriteForCombatantId(target, id,
                                          action_def->bEnmityDirectParam, 0);
        BattleEnmity_PropagateToPerceivingFoes(id,
                                          action_def->bEnmityPropagationParam, target, 0);
        BattleEnmity_AdjustOtherRelevantCombatants(target,
                                        -action_def->bEnmityRedistributionParam, caster, 0);
    }
}
```

**Every action carries three authored enmity numbers**, and they do different jobs:

| Field | Applied to | Effect |
|---|---|---|
| `bEnmityDirectParam` | the target | raises the target's threat toward the caster |
| `bEnmityPropagationParam` | other foes | spreads threat outward (see Z-6) |
| `bEnmityRedistributionParam` | other combatants | applied **negated** - *lowers* others' threat |

The third is the interesting one: it is passed as `-(uint)...`, so an action that generates threat on
its target simultaneously **draws threat away from everyone else.** Threat is redistributed, not just
added.

### Z-6 answered - "perceiving" means "already holds a grudge", not proximity

```c
void BattleEnmity_PropagateToPerceivingFoes(combatant_id, value, source_filter, absolute)
{
    for (slot = 0; slot < BattleUnit_GetSlotCount(); slot++) {
        unit = BattleUnit_GetBySlotIndex(slot);
        if (unit && unit->pBkbi
            && unit->pBkbi->wDefinitionSelector[+1] == 1        // foe class only
            && unit != source_filter)                           // skip the direct target
        {
            table = &unit->pBkei->bEnmityTableHeader;
            if (table
                && BattleEncodedId_IsValidForClass(2, combatant_id)
                && table[combatant_id + 1] != 0)                // <-- ONLY IF ALREADY NONZERO
            {
                BattleEnmity_WriteForCombatantId(unit, combatant_id, value, absolute);
            }
        }
    }
}
```

**There is no distance check.** It walks the **entire BattleUnit slot pool** and filters on three
things: foe class, not the direct target, and - decisively - **`table[id + 1] != 0`**.

So threat spreads only to foes that **already** hold nonzero threat toward that character. In player
terms:

> **Hitting one enemy escalates with everything already fighting you, and pulls in nothing new.**
> An enemy that had no grudge stays uninvolved no matter what you do to its neighbour.

That is why attacking one monster in a group does not aggro a whole zone, while a long fight makes
every participant angrier at once.

**The GFZ name is slightly misleading** and worth flagging: "PerceivingFoes" suggests a perception
or line-of-sight test. The body tests neither. Recorded here rather than propagated.

### `wDefinitionSelector` decoded, and the class byte seen from the other side

`combatant_id = (byte)pBkbi->wDefinitionSelector` establishes the layout of a field this database
had been treating as opaque:

```
wDefinitionSelector   u16
  low  byte  combatant id   -> indexes the 40-entry enmity table as table[id + 1]
  high byte  class          -> 0 = party-side, 1 = foe
```

The high byte is the **same discriminator** already documented three times as `== 1`. This block is
the first sighting of its complementary value:

| Test | Meaning | Where |
|---|---|---|
| `[+1] == 1` | foe | awards EXP, awards LP, maintains a threat table, receives propagation |
| `[+1] == 0` | party-side | **generates** enmity as an action's caster |

One byte separates "things that hold grudges and give rewards" from "things that cause grudges".

### The 40-entry table, now tier 1

`BattleEnmity_WriteAllCombatantIds` loops `while ((int)uVar3 < 0x28)` - **ids 0..39, exactly 40
entries.** The table size was previously recorded at tier 3 from a GFZ annotation; it is now read
from a loop bound.

### A fourth sighting of the unified functional predicate

`BattleEnmity_WriteAllCombatantIds` refuses to write when:

```c
((pFVar1->dwStatusMaskMode0_3 | pFVar1->dwStatusMaskMode1_4) & 0x80000003) != 0
&& FieldData_GetActiveFieldRecordBit15() == 0
```

That is the **same `0x80000003` two-layer status mask with the same per-area waiver**, now found in
**four** independently-read functions: combat action eligibility, EXP/LP award, party control
suppression, and enmity write-all.

## 8f. Reopened 2026-09-02 - Z-7: the eight relation modes, and why gambits do not start fights

`BattleTarget_MatchesRelationMode` (`0030BD00`, 339 bytes) is the **`Ally:` / `Foe:` / `Self:`
prefix** every gambit line begins with. It is a switch over the `wOperand` field of the target
selector.

> **Corrected 2026-09-02 (section 8i).** This section originally said *"an eight-case switch"* and
> tabulated modes `0`-`7`. **There are eleven cases, `0`-`10`.** Modes 8, 9 and 10 were missed. The
> table below is superseded by the complete one in section 8i.

```c
bool BattleTarget_MatchesRelationMode(self, candidate, mode)
{
    rel = BattleTarget_ClassifyRelationshipClass(self, candidate, 0);
    switch (mode) {
      case 0: return true;                                       // any target
      case 1: /* hostile, with an idle-foe exclusion - see below */
              return rel == 2;
      case 2: return rel == 1;                                   // friendly
      case 3: return candidate[+0x08] == self[+0x24];            // same group id
      case 4: return candidate == self;                          // self
      case 5: return candidate[+0x54] == self[+0x54];            // same +0x54 key
      case 6: return rel == 1 && candidate != self;              // friendly, excluding self
      case 7: return candidate[+0x54] == self[+0x54]
                     && candidate != self;                       // same key, excluding self
      default: return false;
    }
}
```

| Mode | Rule | Reads as |
|---:|---|---|
| 0 | always true | any target |
| 1 | hostile (`rel == 2`), **plus an idle-foe exclusion** | **`Foe:`** |
| 2 | friendly (`rel == 1`) | **`Ally:`** |
| 3 | `candidate[+0x08] == self[+0x24]` | same group |
| 4 | identity | **`Self:`** |
| 5 | `candidate[+0x54] == self[+0x54]` | same `+0x54` key |
| 6 | friendly and not self | **`Ally:` excluding yourself** |
| 7 | same `+0x54` key and not self | same key, excluding yourself |

Modes 2/6 and 5/7 are pairs differing only by whether the acting unit can target itself - which is
exactly the distinction between an ally gambit that may heal the caster and one that may not.

### Mode 1's hidden clause - the reason your party does not pick fights

Mode 1 returns `rel == 2` **unless all three of these hold**, in which case it falls through to
`false`:

```
self->[0x698][5]      == 0      // the acting unit is party-class
candidate->[0x698][5] == 1      // the candidate is foe-class
BattleEnmity_HasAnyPositive(candidate) == 0   // that foe holds NO positive enmity toward anyone
```

**A party member's `Foe:` gambit does not match an enemy that has never been provoked.**

That is a directly observable rule and it explains a behaviour every FFXII player relies on:

> **Gambits never start fights.** Walk your party past an idle monster with "Foe: nearest ->
> Attack" set, and nothing happens - the idle foe is invisible to the gambit. The moment anything
> gives that enemy a grudge, it becomes a legal target and the gambit fires.

It also closes the loop with the threat system: `BattleEnmity_HasAnyPositive` was documented earlier
as a thin wrapper over `AnyAboveThreshold(unit, 0)`. This is where it is consumed, and why it
exists.

### An independent confirmation of last block's field decoding

Section 8e decoded `wDefinitionSelector` as a `u16` with **low byte = combatant id, high byte =
class**. This function reads the class from a different expression entirely:

```
self->[0x698][5]        // BKBI + 5
```

Section 8e read the id as `*(byte *)(*(longlong *)(buf[i] + 0x698) + 4)` - **BKBI + 4**.

Byte `+4` is the id, byte `+5` is the class, so `wDefinitionSelector` is the `u16` at **BKBI + 4**
and the two halves land exactly where the decoding predicted. Two functions, two different access
patterns, one consistent layout.

## 8g. Reopened 2026-09-02 - Z-2: the order record, and the gate in front of it

`AiOrder_EvaluateAndResolveActionTarget` (`003014C0`) is the function the selection loop calls per
order. Reading it exposes both the record's fields and the eligibility gate that runs before any
condition is evaluated.

### The AI order record - four fields identified by use

| Field | Role - proven by how it is consumed |
|---|---|
| `wActionSelector` | passed to **`BattleData_ResolveWeightedId`** -> the action id |
| `wActionParameter02` | an action parameter, read at 5 sites |
| `wFlags` | control bits; **seven** distinct bits observed |
| `targetSelector0[]` | indexed array; each entry has `wOperand` (relation mode) + `bSelectorOpcode` |

**`wActionSelector` is a *weighted* id, not a plain one.** It goes through
`BattleData_ResolveWeightedId`, which means a single gambit line can carry **several candidate
actions with weights**, resolved at evaluation time. That is a genuine capability of the format
that the gambit UI does not expose.

The seven flag bits seen across the read functions:

```
0x20   0x40   0x80   0x400   0x800   0x1000   0x4000
```

`0x40` and `0x80` are the resume-gating bits from section 2; `0x800` gates a re-entry check against
the unit's stored order pointer. The rest are unidentified.

> **Z-19 answered 2026-09-12 (FABLE): every bit the shipped sets use, with its reader.** An
> image-wide scan of `test` / `and` / `or` / `bt` on a record's `+4` / `+5` bytes, plus the three
> register-masked tests read in context, gives the readers; the census is over the 50,050 order
> records of the 166 `in` area files (§7a). The record the unit is executing is reachable at
> `unit + 0x708` (the pointer `BattleUnit_CommitAction` stores, [the battle-unit field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)), which is how the
> locomotion and interrupt code read the *current* order's bits:
>
> | bit | records | reader | meaning |
> |---|---:|---|---|
> | `0x08` / `0x10` / `0x20` | 2,118 / 8,082 / 8,076 | the evaluator's shifted test `0x20 >> i` (`003016BE`–`003016CC`) | per target-selector entry 2 / 1 / 0 — keep the intermediate candidate set (above) |
> | `0x40` | 3,339 | `00305DB2` | evaluate even while resuming (§2) |
> | `0x80` | 6,528 | `00305DBC` | skip when resuming (§2) |
> | `0x100` | 369 | `BattleUnit_UpdateCombatNavigationStep` `00325CA5`–`00325CB0` | while current: the unit's locomotion flags `+0x170` **bit 1** set (cleared otherwise) |
> | `0x200` | 1,912 | the same, `00325C7E`–`00325C92` | while current: locomotion flags `+0x170` **bit 0** set (cleared otherwise) — the field map's "action row `+4` bit 9 / 8" for those two bits is this word under the `+0x708` pointer |
> | `0x400` | 99 | the evaluator, `00301B79`–`00301BA2` | with a **non-party** evaluating unit (`[+0x698]+5 ≠ 0`) sets the evaluator's local mode word `[rsp+0x44]`; ~~its consumer downstream is not read here~~ **consumer read 2026-09-30:** the candidate loop then skips every candidate whose `committedAttackerCount` `+0xEA8` is 3 or more (`00301E8E`–`00301E9D`), so a non-party unit does not pile onto a target three attackers already hold |
> | `0x800` | 15,084 | `AiOrder_EvaluateAndResolveActionTarget` `003015A6`–`003015C9` | **no re-issue while current**: when this record is the unit's `+0x738` (the record the standard action advance stores), refuse a band order outright and an action while the cancelled block's `+0x730` bit 0 is set |
> | `0x1000` | 82 | the evaluator, `00301B47`–`00301B74` | sets `[rsp+0x40]` when the word argument (`[rsp+0x130]`) equals the unit's `+0x744`, **the last cancelled action id** — a retry-after-cancel mode; ~~consumer not read here~~ **consumer read 2026-09-30:** in that mode the first candidate that passes the relation and suppression filters and whose `+8` id equals the unit's `+0x740`, **the cancelled action's target**, is returned alone and the scan stops (`00301E76`–`00301E88` → `00303598`–`003035BC`): the cancelled action is retried on the same target |
> | `0x2000` | 283 | `BattleAction_CheckCurrentActionInterruptReason` `002FFCA5`–`002FFCB5` | while current: **skip the execution-timeout check** (`BattleAction_CheckAndHandleExecutionTimeout` is not consulted) |
> | `0x4000` | 11,929 | `BattleUnit_TrySelectAndCommitAiOrderFromSet` `00305D74`–`00305D84` | **resumable**: in resume mode the walk resumes at the stored order only when that order carries it; otherwise it restarts from the top with the `0x40` filter off |
> | `0x0004` | 256 | ~~**no reader found** — the shifted test stops at entry 2~~ `BattleUnit_CanAdvanceCombatNavigation` `00325DE8`–`00325DF8`, the gate at the head of `BattleUnit_UpdateCombatNavigationStep` (called at `00325BD0`); the evaluator's shifted test does stop at entry 2 (`003016B5`) | ~~authored but unread~~ while current: **no combat navigation step**. The gate returns 0 (`00325DA5`), and the step then only calls `0033C9B0` on the locomotion block `unit + 0x80` instead of routing and solving a step (`00325BD5`–`00325BE1`). No player gambit carries it: the 256 condition rows' flags word `+0xE` is 0 on every row. *Corrected 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16), record [`swe2contract-ddres-b16-0930`](../_index/candidates/swe2contract-ddres-b16-0930/README.md), checks N1-N7* |
> | `0x0001`, `0x0002`, `0x8000` | 0 | — | never set |
>
> So the "seven bits" were the seven the AI functions test; the shipped data uses thirteen, the extra
> six being read by the locomotion step, the interrupt check and the resolver rather than the evaluator.
>
> *Added 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): bit `0x8000`, which no shipped `.ard` record and none of the engine's static order sets carries, is still read: three sign tests `cmp word ptr [order + 4], 0` on the current order (`00308736` in the combat frame, before its resume walk; `0030AF49`; `00328604`). The row above lists no reader for it. Check N8 of [the batch record](../_index/candidates/swe2contract-ddres-b16-0930/README.md).*

**Byte offsets are still not established.** Ghidra carries a `FFXII_AiOrderRecord_Partial` type, so
the *names* above are GFZ type work (tier 3) while the *roles* are read from use (tier 1). ~~**Z-2
stays OPEN on the exact layout**;~~ what is now known is which fields exist and what they do. *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): stale. The offsets are Z-2, ANSWERED 2026-09-17, and section 8l reads the layout. The Z-2 box the note below cites is in section 7, not section 9.)*

> **Superseded 2026-09-17 (FABLE):** the offsets are proven — `+0 u16` selector, `+2 s16` parameter, `+4 u16` flags, three
> six-byte entries `{u16 operand, u8 opcode, u8, s16 parameter}` at `+6`, `+0xC`, `+0x12` — from the reader, the writer
> `00328140` and the authored sets; see the Z-2 box in §9.

### The gate before any gambit condition runs

```c
action_id = BattleData_ResolveWeightedId(&order->wActionSelector);
*out_action_id = action_id;

if (( action_id == 0xFFFF                                   // nothing resolved
   || (DAT_02089340 & 0x20)                                 // global AI suppression
   || (unit->qwUnitFlags & 0x10) == 0                       // unit not action-eligible
   || unit->pBkbi == NULL
   || ((status0 | status1) & 0x80000003) && !FieldRecordBit15()      // functional predicate
   || (selector[+1] == 1 && (unit->pBkei->lifecycleFlags & 0x30))    // foe: spawn state
   || (selector[+1] == 1 && (unit->pBkei->lifecycleFlags & 0x48))    // foe: spawn state
    ) && action_id != 0x414D)                               // ... unless the action is 0x414D
    return 0;
```

Four things worth carrying:

**A fifth sighting of the functional predicate.** `((status0 | status1) & 0x80000003)` with the
`FieldData_GetActiveFieldRecordBit15()` waiver now appears in **five** independently-read functions.

**`DAT_02089340` is a shared global runtime flags word.** Bit `0x20` suppresses AI action selection
here; bit `0x40` seeds control suppression in `PartyControl_RecomputeSuppressionFromLeaderBattleState`.
Two subsystems, two bits, one word - a cross-link neither document had.

**Foe-class units carry extra spawn gating.** When `wDefinitionSelector[+1] == 1`, two further tests
run against `pBkei->lifecycleFlags` (`& 0x30` and `& 0x48`). So a foe that is mid-spawn or
mid-retirement cannot act even when everything else passes - the spawn lifecycle and the AI share a
gate.

**`0x414D` bypasses the entire gate.** The whole condition is `AND action_id != 0x414D`, so that one
action id is evaluated even for a unit that fails every eligibility test. What it is, is unknown -
recorded as **Z-14**. *(Answered since — `Z-14`, 2026-09-12: it flips the combat stance; §7's struck checkbox.)* It is a striking enough exception that guessing would be worse than naming it.

## 8h. Reopened 2026-09-02 - manual commands beat gambits, and `0x414D` explained

### A player-issued command pre-empts the entire gambit list

`BattleUnit_SelectAndCommitNextAction` (`00305AB0`) runs **before** any gambit is considered:

```c
if ((unit->qwUnitFlags & 0x4000) != 0) {              // a command is pending
    action_id = unit->nIssued_command_id;
    unit->qwUnitFlags &= ~0x4000;                     // consumed on read

    if ( ( (ushort)(action_id + 0xC000) < 0x167       // in the 0x4000-band -> skip availability
        || BattleAction_CheckActionAvailabilityReason(action_id, unit) == 0 )
      && BattleUnit_CommitAction(unit, &unit->nIssued_command_id,
                                 action_id, unit->nIssued_target_focus, 1) != 0 )
        return;                                        // committed - gambits never run
}
/* ... only now does gambit evaluation begin ... */
```

**Flag `0x4000` on `qwUnitFlags` means "the player issued a command", and it is cleared the moment
it is read.** If that command commits, the function returns and **the gambit list is not consulted
at all** for that action.

That is exactly the behaviour players rely on: **a manual order always beats your gambits**, and it
is a one-shot - the flag is consumed whether or not the commit succeeds, so a command that fails to
commit falls through to gambits rather than retrying.

### Z-14 advanced - `0x414D` is not a lone magic number

The range test above is the key:

```
(ushort)(action_id + 0xC000) < 0x167
```

which is `action_id` in **`0x4000` .. `0x4166`** - a band of 359 ids that skips
`BattleAction_CheckActionAvailabilityReason`.

**`0x414D` falls inside it:** `(0x414D + 0xC000) & 0xFFFF = 0x014D = 333`, and `333 < 359`.

So the bypass constant in section 8g is **member 333 of an action-id band based at `0x4000`**, not
an arbitrary sentinel. Two independent gates treat that band specially - one skips availability
checking for issued commands, the other (section 8g) lets `0x414D` past the AI eligibility gate
entirely.

This also matches the **top-nibble category encoding** already proven for item ids, where
`id >> 12` selects a category and the low 12 bits index within it. Here `0x414D >> 12 = 4`, index
`0x14D`. The parallel is strong but the action-id encoding has **not** been proven the way the item
encoding was, so it is recorded as **Z-16** rather than asserted. *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): Z-16 is ANSWERED 2026-09-17, yes. `00301830` subtracts `0x4000` from the resolved id, bounds it by `0x166` and indexes the order-handler table `01EEC460` (`003018DD`–`003018FB`); section 7's Z-16 box.)*

### Precise scan behind the claim

Nine instruction encodings were checked across the whole `.text` for the constant `0x414D`
(`cmp ax/eax/ecx`, `mov ax/eax`, and the `81 /7` forms):

```
mov eax, 0x414D   @ 0x00301576   in AiOrder_EvaluateAndResolveActionTarget
```

**Exactly one instruction in the binary references it.** Since no code *produces* the value, it can
only reach `action_id` from **authored data** via `BattleData_ResolveWeightedId` - so it is a
data-side escape hatch, not an engine-internal state.

**A coincidence worth closing off:** `0x414D` is `"MA"` little-endian, `"AM"` big-endian. It is an
action id in a numeric band based at `0x4000`; the ASCII reading is an accident of the value falling
in the printable range. Noted so a future pass does not chase it.

### Two further status bits in the same gate

The fall-through path tests `dwStatusMaskMode0_3 | dwStatusMaskMode1_4` against **bit `0x20`** and
**bit 27 (`0x08000000`)**, the latter only for foe-class units. Neither is part of the `0x80000003`
functional predicate - they are additional, separate status gates. **Z-17** — named 2026-09-11 from
the status name bank: bit 5 is Confuse, bit 27 Berserk.

## 8i. Reopened 2026-09-02 - a gambit's action can be a random weighted pick

`BattleData_ResolveWeightedId` (`00308EC0`) is what turns `order->wActionSelector` into an action
id, and **bit 15 of that field decides whether the action is fixed or rolled.**

```c
word BattleData_ResolveWeightedId(word *encoded_or_direct_id)
{
    id = *encoded_or_direct_id;

    if (id <= 0x7FFF) return id;                 // bit 15 clear -> DIRECT id, used as-is

    count = *DAT_02EBF160;                        // bit 15 set  -> WEIGHTED table lookup
    if (id <= count + 0x7FFF) {
        index = id - 0x8000;
        if (0 <= index && index <= count - 1) {
            start = ImageAddress_ResolveRuntimePointer(table[index * 2 + 2]);
            end   = ImageAddress_ResolveRuntimePointer(table[(id - 0x7FFF) * 2 + 2]);
            r = RNG_SharedGameplayLCG_NextU32();  // <- the roll
            while (true) {
                if (end <= start) return 0xFFFF;
                ...
            }
        }
    }
}
```

**In player terms:** a gambit line does not have to name one action. Its action field can point at
a **weighted set**, and which action actually fires is **rolled from the shared gameplay RNG** each
time the line triggers. That is how an enemy with one AI order can vary its attacks.

### What is established

**Bit 15 is the discriminator.** `id < 0x8000` is a literal action id; `id >= 0x8000` is
`index = id - 0x8000` into the weighted table.

**The consecutive-entry pattern gives the candidate range.** `entry[index]` and `entry[index + 1]`
are resolved as `start` and `end` pointers, so each table slot delimits a run of candidates -
textbook weighted selection over a contiguous range.

**The table is image-address indirected**, through `ImageAddress_ResolveRuntimePointer` on a dword -
the same mechanism as the equipment definition table and the resource system, and a third sighting
of that pattern.

```
Weighted id table   header at DAT_02EBF160
  +0x00   u16   entry count
  +0x02   dword[]  RVA per entry, resolved at runtime; entry[i]..entry[i+1] bounds the candidates
```

**`0x414D` is a direct id**, since `0x414D < 0x8000` - consistent with section 8h treating it as a
literal.

### Why this matters beyond combat

`RNG_SharedGameplayLCG_NextU32` is the **shared** gameplay LCG. So resolving a weighted action
**consumes shared RNG state**.

**For XIIOnline this is a divergence source with teeth:** two clients that evaluate the same gambit
at slightly different times, or in a different order, will draw different values and can pick
*different actions* - and every subsequent draw shifts for both. Action selection is not a pure
function of game state; it is state-dependent on the RNG stream.

### Z-16 - evidence against, not proof

Three action-handling functions were read (`BattleData_ResolveWeightedId`,
`BattleAction_CheckActionAvailabilityReason`, `BattleAction_CheckUnitActionAvailability`) and
scanned for the item-style category arithmetic - `>> 0xC`, `& 0xFFF`, or a `- 0x4000` base
subtraction. **None appears in any of the three.**

The discriminator that *does* exist in this id space is **bit 15** (direct vs weighted), not a top
nibble. So the resemblance noted in section 8h - `0x414D >> 12 = 4` - is **not** supported by these
functions. **Z-16 leans NO**, and is recorded that way: absence across three functions is evidence,
not proof, and some other consumer could still decode a category. *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): one does. Z-16 is ANSWERED yes on 2026-09-17 (section 7's box), so the lean is superseded.)*

### A sixth sighting of the functional predicate

`BattleAction_CheckActionAvailabilityReason` opens with:

```c
if (((bkbi->dwStatusMaskMode0_3 | bkbi->dwStatusMaskMode1_4) & 0x80000003) != 0
    && FieldData_GetActiveFieldRecordBit15() == 0) return 2;
```

That is now **six** independently-read functions carrying the same predicate.

## 8i. Falsification pass 2026-09-02 - eleven relation modes, not eight

**Attack chosen.** Section 8f asserts a bold, player-facing **universal**: *"Gambits never start
fights."* That universal is only as strong as its enumeration - it rests on mode 1 carrying an
idle-foe exclusion, and section 8f's own listing shows **mode 0 returning `true` unconditionally**
with no enmity check anywhere in modes 3, 5 or 7 either. The killer looked for was therefore a
relation mode that can match a hostile, un-provoked unit. Re-reading the function found something
larger first.

### OVERTURNED: the switch has eleven cases, not eight

`BattleTarget_MatchesRelationMode` was decompiled complete against the current parent:

| Mode | Rule | Reads as |
|---:|---|---|
| 0 | always `true` | any target |
| 1 | `rel == 2`, **minus the idle-foe exclusion** | **`Foe:`** |
| 2 | `rel == 1` | **`Ally:`** |
| 3 | `candidate[+0x08] == self[+0x24]` | same group |
| 4 | `candidate == self` | **`Self:`** |
| 5 | `candidate[+0x54] == self[+0x54]` | same `+0x54` key |
| 6 | `rel == 1 && candidate != self` | `Ally:` excluding self |
| 7 | same `+0x54` key `&& candidate != self` | same key, excluding self |
| **8** | `candidate[+0x54] != self[+0x54]` | **different key - the negation of mode 5** |
| **9** | `candidate[+0x08] == self[+0x710]` | **the unit this action is aimed at** |
| **10** | `candidate[+0x08] == self[+0x748]` | same test against a second focus field |
| default | `false` | |

**Modes 8, 9 and 10 were absent from this document.** Mode 8 is the exact complement of mode 5,
which is the kind of pairing sections 8f already noted for 2/6 and 5/7 - so its absence broke a
pattern the document had itself identified.

### Mode 9 is identifiable from work done elsewhere today

Mode 9 compares the candidate's group id against **`self[+0x710]`**. That offset was independently
established on 2026-09-02, during the unrelated AH-6 pass on
[`../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`](../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md),
by reading `BattleUnit_CommitAction` (`0030F760`):

```c
unit->pAction_context = order_context;   // +0x708
unit->dwTarget_focus  = target_focus;    // +0x710   <-- this field
unit->wAction_id      = action_id;       // +0x714
```

So **mode 9 selects "the unit my current action is targeting"** - a *current-target* relation, which
is a meaningfully different concept from the group and key tests around it. `+0x748` (mode 10) is a
second focus-like field, ~~not yet identified~~ **identified 2026-09-12: the commanded target** — `BattleUnit_IssueCommand`
stores its target-handle argument there, and the engine's own static command set (`01EEC2D0`, one `Attack` record) uses
mode 10 ([the gambit-set page](which-gambit-set-fires-and-how-a-command-switches-it.md) §7).

### The universal must be narrowed - but it survives where it matters

Mode 1's clause was re-read and is **exactly as documented**: the function returns `rel == 2` unless
all three of `self` is party-class, `candidate` is foe-class, and
`BattleEnmity_HasAnyPositive(candidate) == 0` hold, in which case it falls through to `false`.

**But that exclusion exists in mode 1 alone.** Modes 0, 3, 5, 7, 8, 9 and 10 contain no enmity test
of any kind, and mode 0 matches everything unconditionally. The claim as written -

> *"Gambits never start fights."*

- is therefore **over-general**. What is proven is narrower and should be stated as:

> **A `Foe:`-prefixed gambit never starts a fight.** The idle-foe exclusion lives in relation mode 1
> only, which is the mode the `Foe:` prefix uses.

Whether any *other* mode is reachable from authored gambit data is **not established**, and until it
is, the wider claim is not earned. If mode 0 is authorable on a target selector, a mode-0 gambit
would match an idle foe and would start a fight. Registered as **Z-15**. *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): established since. Z-15 is answered for both halves, below and in the register: no authored order, party or enemy, selects a target by mode 0.)*

> *Z-15 answered from the shipped data 2026-09-12 (FABLE), for the player's half.* The 256 gambit
> target-condition rows (`battle_pack.bin` directory `+0x20`, the class-11 table behind `02EBF0D8`,
> [the encoded-id space page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.10) carry, in the three byte-sourced selector members the rebuild widens into
> `record +0x06` / `+0x0C` / `+0x12` (§8l above), only **1, 2 and 4** at `+0x10` — 137 `Foe:` rows,
> 68 `Ally:` rows and 51 `Self` rows by their bank-6 names, one-to-one with the three prefixes —
> and **0, 1, 2 or 4** at `+0x11` (0 on 210 rows, `4` on the *character HP / status / item AMT /
> foes present* conditions, `1` and `2` once each on *Self: targeted by foe / ally*), never 3, 5, 6,
> 7, 8, 9 or 10. That the byte-sourced member is the **operand** — the relation mode — and not the
> opcode follows from the values: they are exactly the mode numbers §8i's switch gives the three
> prefixes. So **no gambit a player can set reaches mode 0 as its primary relation**; the only
> authored 0 is the second selector of rows that have none. What the census does not cover is the
> other author of orders — the enemy AI order sets in `.ard` directory slot 1 ([the area-file loader](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)),
> whose container format ~~is CC-5's residue~~ *(answered 2026-09-12 as the order-set directory; `CC-5` slot 1;
> noted (FABLE, Claude Opus 5.5, 2026-09-26, on OPUS-REQ-FABLE-ARD-TRAILER-READ-BY-NOTHING-PROSE))* — so the narrowed claim stands as the player's guarantee:
> **a party gambit never starts a fight**; whether an enemy's authored order can carry mode 0 is
> a question about that container.
>
> *The enemy half, answered the same day (FABLE, Z-15B).* That container is now read ([the area-file loader](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)
> §7a): the 166 area files hold **1,422 enemy order sets and 50,050 order records**, every record
> the 24-byte shape of §8l with its three selector entries at `+0x06` / `+0x0C` / `+0x12`. Their
> first selector's operand takes **1 (18,206 records), 4 (15,339), 9 (1,576), 7 (1,187), 5 (516),
> 6 (331), 2 (271), 3 (176), 8 (89)** — every relation mode of §8i's switch **except 10** — plus
> encoded-id operands (`0x1001`, `0x1010` / `0x1011`, `0x2001`, `0x9001`–`0x900F`) on the opcodes
> that take an id, and **0 on 8,999 records**. But an operand of 0 is never *evaluated*: the
> selector walk in `AiOrder_EvaluateAndResolveActionTarget` tests each entry's first word and
> **skips the entry when it is zero** (`00301685 cmp word ptr [rbp], 0` / `0030168A je` → the
> `inc ebx / add rbp, 6` advance at `0030176B`–`00301774`), so a 0 is the *empty* entry, not mode
> 0. **Mode 0 is therefore unreachable from authored data on both sides** — the party's 256
> conditions never carry it and the enemies' 50,050 records carry it only as "no selector" — and
> mode 10 is authored nowhere *(in the shipped `.ard` sets and gambits — the engine's static command set `01EEC2D0` does use it, 2026-09-12)*; the seven other modes are the enemies' vocabulary. So the original
> universal survives in a sharper form: **no authored order, party or enemy, selects a target by
> mode 0; `Foe:` (mode 1) is the only relation with the idle-foe exclusion, and it is the one the
> enemies use most.**

**What did not change.** The observable behaviour the section describes - walk past an idle monster
with `Foe: nearest -> Attack` and nothing happens - is still fully supported, because that gambit
uses mode 1. The correction is to the *scope* of the rule, not to the behaviour.

### Why the error was reachable

The original read enumerated the cases from the decompiler's `switch` as printed, and Ghidra emits
`default:` **in source order** - here between `case 1` and `case 2`, because `case 1` falls through
into it. A reader taking the cases in printed order sees `0, 1, default, 2, 3, 4, 5, 6, 7` and can
reasonably conclude the switch ends at 7, when cases 8, 9 and 10 are printed *after* it. **The
`default` label appearing mid-list is the trap**, and it is a decompiler-presentation artefact
rather than anything about the binary.

Added to the instrument-shaped blind spot register in
[`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md): **never take a switch's case
count from reading-order; count the labels.**

## 8f. Z-10 reopened, Z-11 answered — the writer restores nothing, it writes 2.0

Section 8d answered Z-10 **NO** on the reasoning that `DAT_01DFE0B8`'s only writer is *"a shutdown-path
default restore"* leaving *"`1.0f` throughout play"*. **Re-testing with a stronger instrument, the
reason is false in both halves.**

### What the writer actually stores

```asm
001EDDC0  sub  rsp,0x28
001EDDC4  test ecx,ecx
001EDDC6  je   0x1EDE1F              ; ecx == 0 -> the timeBeginPeriod branch
001EDDC8  movss xmm0,[01CEBC08]      ; 2.0f
001EDDD0  movss xmm1,[01CEBB70]      ; 0.5f
001EDDD8  movss [01DFE0B8],xmm0      ; <- the only write to the enmity-decay scalar
001EDDE0  movss [01DFE0BC],xmm1
001EDDE8  mov  dword [01F82E38],1
001EDDF2  mov  dword [01DFE0B4],2
001EDDFC  call 0x33F020
001EDE01  cmp  byte [01F82E35],0
001EDE0A  mov  ecx,[01F82E30]
001EDE17  call [WINMM!timeEndPeriod]
```

| address | shipped in `.data` | what the writer stores |
|---|---|---|
| `0x01DFE0B4` | `1` (u32) | **`2`** |
| `0x01DFE0B8` | **`1.0f`** | **`2.0f`** |
| `0x01DFE0BC` | `1.0f` | **`0.5f`** |

**It does not restore the default — it replaces it.** And `2.0` / `0.5` is a **reciprocal pair**
written in the same breath as an integer `2`.

**Z-11 is answered by this**: the block at `0x01DFE0B4`–`0x01DFE0BC` is a **time-base triple** — an
integer mode, a scale, and its reciprocal — set by a single function in a single store sequence.
(`0x01DFE0B0` also ships `1.0f` and no writer was found for it; whether it belongs to the same
structure is not established.) *(Scoped (FABLE, Claude Opus 5.5, 2026-09-30): nothing on this page reads it. The decay interval reads only `01DFE0B8` and `008F8D80` (`0032157F`, `00321587`); `0x01DFE0B0` has two `mulss` reads in one function and no instruction writer (rip-reference scan), so its place in the block is outside this page's subject.)*

### The identification came from the wrong branch

`FUN_001EDDC0(int)` is **two functions in one**, selected by its argument, and the imports resolve
through the PE import directory rather than by inference:

| branch | calls | writes the scalar |
|---|---|---|
| `ecx == 0` | `timeGetDevCaps` (8-byte `TIMECAPS`), then `timeBeginPeriod` | no |
| `ecx != 0` | `timeEndPeriod` | **yes** |

Section 8d read the function's identity off the `timeGetDevCaps` / `timeBeginPeriod` branch and
attached it to a write that is **not on that branch**. *A function's identity is not uniform across
its branches, and a write belongs to the branch that contains it.*

### Where the argument comes from

The only route into `FUN_001EDDC0` is **one `E9` tail call** — no `E8` call, no address-taken,
no pointer in data — from `FUN_0022BDF0(int argc, char **argv)`:

```asm
0022BE08  call 0x17D8F0             ; returns *(dword*)(*(void**)01F82D20 + 0x48)
0022BE15  cmp  eax,r15d             ; r15d = 1
0022BE18  cmove ebp,r15d            ; ebp = (that field == 1)
0022BE28  lea  r14,[00908BD8]       ; "-nologo\0", compared 8 bytes at a time
0022BE7D  jmp  0x1EDDC0             ; tail call, ecx = ebp
```

So the branch is chosen at startup by a **process-global configuration field**, not by anything in
combat, and not by `-nologo` (that flag sets an unrelated global through a 7-byte setter). **Nothing
writes `0x01DFE0B8` back afterwards.** The value is `1.0f` for the whole process, or `2.0f` for the
whole process.

### What this does and does not license

**It does not make Z-10 a YES.** A reciprocal pair set beside an integer `2` is *consistent* with a 2x
time base, and the enmity-decay interval would be **60 instead of 30** in that mode. But this document
has not read `FUN_0033F020` (**seven** targets: six `call` and one `jmp` tail call), has not identified the configuration field at
`+0x48`, and **has no evidence tying either to a player-facing speed control.** The reading that the
value is a startup-fixed engine time base is equally consistent with everything measured. *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): both are settled. The `+0x48` field is `FrameLimit` (DH-1), and `FUN_0033F020`'s targets include the six 60-fps table initialisers named in the Presentation crossing below; see the note under the separating observation.)*

~~**Z-10 returns to OPEN.**~~ *Separating observation:* identify the object at `0x01F82D20` and read field
`+0x48`; if it is the parsed configuration record, its provenance decides this.

> *Closed since (note (FABLE, Claude Opus 5.5, 2026-09-30)): the separating observation was made — the field is `FrameLimit` (DH-1) — and Z-10 closed NO on 2026-09-08 (section "Z-10 closed" below). `FUN_0033F020`'s callees are the 60-fps table initialisers named in the Presentation crossing below; that answer does not need them.*

### The limits of the instrument, stated

The re-test scanned **every memory operand with a RIP-relative base**, not just `MOVSS` forms, and
classified each by capstone's access role: **45 reads, 1 write.** *The original scan's own base-register
caveat was then tested*, since `0x01DFE0A0 + 0x18` is exactly the target:

```
LEA sites landing in 01DFE000..01DFE160        : 27   (none targets 01DFE0B8 itself)
of those, targeting 01DFE0A0                   :  2
   FUN_001EB930  -- 8 bytes: lea rax,[01DFE0A0] ; ret   (an accessor returning the block)
```

That accessor is reached by **exactly one tail call** (`FUN_00181CD0`), itself reached by **exactly
one call** (`FUN_003829D0`), and **neither writes at `+0x18`**. **The alias route is bounded at two
hops and clean.** It is not *closed*: a pointer stored to memory and written through later would still
be invisible to this scan, and nothing here rules that out.

> **The first instrument returned `totals: {}`** — zero accesses, including the 39 reads this document
> already claimed. It filtered on `mem.base != 0`, but capstone reports RIP-relative operands with
> `base = X86_REG_RIP`, so the filter excluded every operand it was meant to find. **A test whose
> negative contradicts a number you already trust is measuring your instrument, not the binary**, and
> the result was withheld rather than reported.

---

## 8k. Reopened 2026-09-02 — the threat table is a *saved* object, and two GFZ offsets are now tier 1

Reopened by evidence from the spawn-lifecycle pass. This document already said the enmity vector
lives in the target's **BKEI record**. What it did not say is **what a BKEI record is**, and that
turns out to change what the table *is*.

### The BKEI is an entry in the spawn persistence bank

`unit + 0x6A0` — the pointer this document calls `pBkei` — points into
**`btlKeepCharWork1`**, a heap block of **296 entries × 128 bytes** allocated under that authored
name by `BattleStorage_InitializeWorkArrays`. It is the same array
[`spawn-placement-and-retirement.md`](../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)
documents as the spawn *keep* bank. The enmity block at `+0x19 .. +0x41` sits inside those 128
bytes.

Three consequences, none of which this document carried:

- **Threat survives leaving the area and coming back.** On every area transition
  `SpawnKeep_RotatePersistenceBanksForAreaTransition` copies the whole bank, 128 bytes per entry,
  with `movups` — the enmity table included, because the copy is blind to structure. If the area
  you enter is the one you were in *before* the one you just left (the **A → B → A** pattern) and
  you arrive within ~~`30 × g_nSpawnKeepReturnWindow`~~ `(int)(01DFE0B8 × 30.0) × g_nSpawnKeepReturnWindow` raw ticks
  (`002337DE`–`00233801`; *corrected (FABLE, Claude Opus 5.5, 2026-09-30): the frame-rate scalar multiplies it, so it is 30 × the window
  only at FrameLimit 30*) — **300 seconds** by default (the window's native value, `00236A0D`; its unit is L-2 on
  [the spawn page](../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)) — the
  banks are exchanged and **every enemy resumes hating exactly who it hated, at exactly the value
  it held.** Arrive from anywhere else, or later than the window, and the live bank is `memset` to
  zero: **all threat, everywhere, is erased at once.**
- **Threat is written to the save file.** `SpawnKeep_SerializePersistenceBanks` copies both banks
  into a `0x20010`-byte buffer (16-byte header, then `0x10000` reserved per bank) and
  `SpawnKeep_RestorePersistenceBank` copies them back. Nothing filters the enmity range out.
- **Decay only runs for spawn-backed units.** `BattleEnmity_UpdatePeriodicDecay` returns
  immediately unless `pBkbi[+0x05] == 1`. A unit without a keep entry has no table to decay and no
  table to persist.

So "the hidden threat table" is not per-encounter runtime state. **It is persistent world state
with a 300-second forgiveness window and a save slot.**

### Two offsets promoted from tier 3 to tier 1

§4 recorded the block as *"GFZ records BKEI+0x1A..+0x41"* and the entry count as `u8[40]`. Both are
now read from the instruction stream:

```asm
0032156D  lea   rdi, [rax + 0x19]        ; BattleEnmity_UpdatePeriodicDecay, rax = unit[0x6A0]
00321D61  lea   r9,  [rax + 0x19]        ; BattleEnmity_WriteAllCombatantIds, same base

00321DA1  inc   ebx                      ; BattleEnmity_WriteAllCombatantIds, the write loop
00321DA3  cmp   ebx, 0x28                ; 40
00321DA6  jl    0x321d90
```

**The block base is `pBkei + 0x19` and the loop bound is exactly `0x28 = 40`**, so
`timer = BKEI+0x19`, `enmity[id] = BKEI + 0x1A + id` for `id` in `0..39`, ending at `+0x41`. The
GFZ annotation was right; it is simply no longer the reason to believe it.

### A fourth site of the `0x80000003` status predicate

`BattleEnmity_WriteAllCombatantIds` refuses to write anything unless:

```c
if (((bkbi[0x64] | bkbi[0x3C]) & 0x80000003) != 0
    && FieldData_GetActiveFieldRecordBit15() == 0) return;     // 00321D7A - 00321D8E
```

That is the **same predicate, byte for byte**, that gates candidate eligibility in
`Spawn_ValidateCandidateDistanceToPlayers` and range retirement in
`SpawnLifecycle_CheckAndRetireByNativeRange`. One masked pair of status words, with one
field-record escape hatch, decides whether a unit may be measured for spawning, may be retired,
**and may have its threat adjusted.** ~~Its meaning is still unknown — carried as **L-8** in the
spawn document — but it is now a shared gate across three subsystems rather than a local check,
which raises the value of closing it.~~ *It is a shared gate across three subsystems, and its meaning is answered (L-8, 2026-09-11): bits 0, 1 and 31 are KO, Stone and X-Zone, and the escape is the field record's bit-15 permission ([the thirty-two statuses](../10-Status-Periodic-Terminal/the-thirty-two-statuses.md)). Note (FABLE, Claude Opus 5.5, 2026-09-30).*

### What this does not change

The selection loop, the `-10` decay step, the engagement suppression, the four-slot scan, the
interval of `DAT_01DFE0B8 × 30.0` and the foe-class gate are all untouched. Every number in §2 and
§4 was re-checked against the current bodies and holds.

### Modding and XIIOnline consequences

- **Wiping threat is a side effect of walking somewhere new.** Any mod that reasons about enmity
  as per-fight state will be wrong across a zone boundary in both directions — it can persist far
  longer than a fight, or vanish entirely, and which one happens depends on the player's route.
- **Raising `g_nSpawnKeepReturnWindow` extends threat memory**, because it is the same window.
  There is no separate enmity lifetime.
- **XIIOnline:** §6 already warns that engagement evidence must be replicated or threat decays on
  one client and not the other. This is stronger — **the whole table is inside a block that is
  swapped, zeroed or reloaded by area transitions and save/load.** Two clients that take different
  routes between the same two areas will legitimately end up with different threat tables, and
  neither is wrong locally. Any shared-enmity model has to replicate the *bank rotation decision*,
  not just the values.

### Related

- [`../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`](../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)
  — the bank, the rotation rule, the return window and the `0x80000003` predicate (**L-8**)

## 8l. Reopened 2026-09-03 — Z-2 ANSWERED: the exact 24-byte layout, and the switch that makes a line dormant

Section 8g identified the order record's fields **by use** and stated plainly that *"byte offsets are
still not established"*, leaving Z-2 open on the layout. They are established here, from **two
independent directions that meet**: the function that *writes* the record, and the function that
*reads* it.

`GambitRuntime_RebuildOrderSetFromConfig` (`00328140`, 369 B) had **no citing document** before this
pass. It is the config → runtime step section 2 named but did not read.

### The layout, each offset anchored by a use

| offset | size | field | how the offset is fixed |
|---|---|---|---|
| `+0x00` | `u16` | `wActionSelector` | `AiOrder_EvaluateAndResolveActionTarget` passes the **record pointer itself** to `BattleData_ResolveWeightedId` (`00308EC0`) at `003014F6` — the weighted id is the first member |
| `+0x02` | `s16` | `wActionParameter02` | read `movsx ecx, word [r14+2]` at `0030162F` — **signed**, which no other field is |
| `+0x04` | `u16` | `wFlags` | `test word [r14+4], ax` at `003015A6`; and the walk's resume bits are `test byte [rbx+4], 0x40` / `0x80` at `00305DB2` / `00305DBC` |
| `+0x06` | 3 × 6 B | `targetSelector0[]` | `lea rbp, [r14+6]` at `00301681` — the array base, and the loop bound is `cmp ebx, 2` (`003016B5`), so **exactly three entries** |

**24 bytes exactly**: `2 + 2 + 2 + 18`. The three-entry count is independently fixed twice — by the
reader's `cmp ebx, 2`, and by the writer emitting exactly three triples per record.

### Each selector entry is three `u16`, and the rebuild says where they come from

`GambitRuntime_RebuildOrderSetFromConfig` writes eleven members per record. Sorting its stores by
destination (the record sits at `set + 0x20 + i*0x18`, so `[rsi+0x20]` is record `+0x00`):

```
record +0x00  <- config slot word 1
record +0x04  <- definition +0x0E                     (wFlags)
record +0x06  <- definition +0x10  (byte -> word)     selector[0]
record +0x08  <- definition +0x08                     selector[0]
record +0x0A  <- definition +0x18                     selector[0]
record +0x0C  <- definition +0x11  (byte -> word)     selector[1]
record +0x0E  <- definition +0x0A                     selector[1]
record +0x10  <- definition +0x1A                     selector[1]
record +0x12  <- definition +0x12  (byte -> word)     selector[2]
record +0x14  <- definition +0x0C                     selector[2]
record +0x16  <- definition +0x1C                     selector[2]
```

**The authored definition holds three parallel arrays** — bytes at `+0x10…+0x12`, words at
`+0x08…+0x0C`, words at `+0x18…+0x1C` — and the rebuild **interleaves them** into three 6-byte
entries. The member widened from a byte is consistent with section 8g's `bSelectorOpcode` being
byte-valued; **which of the three members is the opcode is not proven here**, only that one of them
is byte-sourced and the other two are word-sourced. *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): proven since; see the note below.)*

> *Answered since (note (FABLE, Claude Opus 5.5, 2026-09-30)): the byte-sourced member, entry `+0`, is the relation word (Z-15, section 8i); entry `+2` holds the opcode (high byte) and operand (low byte), and entry `+4` the s16 threshold (section 8b, Z-1).*

**`record +0x02` is never written by the rebuild.** `wActionParameter02` comes from somewhere else or
is left at whatever the buffer held. That is a fact about this writer, not a claim that nothing writes
it.

### The switch that makes a gambit line dormant

The rebuild loop is the answer to *what makes a line stop firing*, and it is not in the evaluator at
all — **a disabled line never becomes a runtime record**:

```asm
0032817B  lea   rax, [rdx + 0x30]         ; rdx = the 12-slot config array
00328182  mov   [rsp + 0x50], rax
00328187  lea   r15d, [r12 + 0xc]         ; 12 iterations
003281A0  movzx eax, word ptr [rax]       ; the enable mask
003281A3  test  ebx, eax                  ; ebx = 1 << slot
003281A5  je    0x32827c                  ; disabled -> emit nothing
003281AB  movzx ebp,  word ptr [rdi]      ; slot word 0 - the definition id
003281AE  movzx r14d, word ptr [rdi + 2]  ; slot word 1 - the action
003281B3  cmp   bp, cx                    ; 0xFFFF = empty slot
00328285  rol   ebx, 1                    ; next slot's bit
```

- **12 config slots, 4 bytes each** (`add rdi, 4`, twelve iterations) — two `u16` per slot.
- **A 16-bit enable mask sits immediately after them at config `+0x30`**, `12 × 4 = 0x30`, one bit per
  slot, walked with a rotating `ebx`.
- **`0xFFFF` in either slot word means empty**, and is checked separately from the mask.

> **So a gambit line has three ways to be dormant and they are not the same thing:** its mask bit is
> clear (the player's on/off switch), its slot is `0xFFFF` (nothing authored), or it is enabled and
> emitted but its condition never matches. **Only the third is visible to the evaluator** — the first
> two are already gone by the time any condition runs, which is why a disabled line costs nothing.

`r12d` counts what was emitted and `mov byte [r13], r12b` stores it as the **first header byte**,
which is the per-subgroup count the walk in section 2 sums to find a subgroup's base.

### Where the runtime order sets live

```asm
0032814D  movzx eax, byte ptr [rcx + 4]   ; the stats index
00328160  imul  r13, rax, 0x170           ; 368 bytes per set
00328167  lea   rax, [rip + 0x1d6120a]    ; -> 02089378
```

**`0x170` = 368 = the `0x20` header plus fourteen 24-byte records.** The config supplies at most
twelve, so **two record slots of capacity are never filled from this path** — recorded as a fact about
the stride, not as a claim that nothing else uses them.

The authored definition table is reached through a descriptor at `02EBF0D8`:
`entry = resolve(desc+0x0C) + (id − 0x6000) × desc[+0x08]`, so **slot word 0 is an id with a `0x6000`
base** and the stride is data, not a constant in the code.

### Z-19 advanced — three of the five unknown flag bits are one field

*Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): Z-19 is ANSWERED 2026-09-12. Every flag bit's reader is in section 8g's table; bit `0x04`'s reader, the navigation gate, is added there by this batch.*

The evaluator tests `wFlags` against a **shifted** bit, once per selector entry:

```asm
003016BE  movzx edx, word ptr [r14 + 4]   ; wFlags
003016C3  mov   eax, 0x20
003016C8  mov   ecx, ebx                  ; the selector index, 0..2
003016CA  sar   eax, cl                   ; 0x20 >> i
003016CC  test  edx, eax
```

**`0x20`, `0x10` and `0x08` are not three independent flags — they are one three-bit field, one bit
per target-selector entry.** Section 8g listed `0x20` among the unidentified bits; it is the entry-0
bit of that field.

When **both** bit `i` and bit `i+1` are set, the code copies ~~**512 bytes** (`edx = 4` iterations of
`0x80`)~~ **`0x208` bytes** (four `0x80` blocks and a trailing qword; the correction below) *(lead amended 2026-09-30, FABLE, on SWE2-AUDIT-SEM's [review](../_index/candidates/auditsem-review-dd-gameplay-0930/REVIEW.md) N4; record [`dd-gameplay-corrections-fable-0930`](../_index/candidates/dd-gameplay-corrections-fable-0930/README.md))* before evaluating the next entry ~~— the candidate buffer built by
`AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus`. So the three entries run **in index
order, each narrowing the candidate set**, and the flag pair decides whether the intermediate set is
preserved across the step. **What the preserved copy is later used for is not read here.**~~

*Corrected (FABLE, Claude Opus 5.5, 2026-09-30), from the whole of `003014C0`:* the copy is **entry `i`'s own result**, `0x208` bytes (four `0x80` blocks and a trailing qword, `003016E2`–`0030174B`), not the starting list. It becomes the next entry's input (`00301746 lea rsi, [rsp + 0x40]`), and the next entry writes its survivors back over the same buffer. **So entries narrow the set only under the flag pair.** Without it the next entry filters the **original** candidate list (`00301753 mov rsi, r13`) into a buffer of its own (`00301750`–`00301768`), and the final pick never reads that buffer: it reads only the first one (`003017B7`). Every non-empty entry must still find someone, or the order fails (`003016AF`). The target therefore comes from the first non-empty entry, narrowed by any entries chained after it; an unchained later entry is a yes / no test over the whole list.

### What this does not establish

- **Which member of a selector entry is the opcode.** One is byte-sourced and two are word-sourced;
  section 8g's `bSelectorOpcode` / `wOperand` names are not bound to offsets by this pass.
- **What writes `record +0x02`.** Not this function.
- **The remaining flag bits** `0x400`, `0x1000`, `0x4000` — `0x4000` is the action context's
  resume bit in section 2, and whether the record's `0x4000` is the same meaning is not shown.
- **Whether the two spare record slots** in each `0x170` set are used by any other writer.

> *Status of these four (FABLE, Claude Opus 5.5, 2026-09-30):* (1) answered, see the note above; (2) `+0x02` is authored in the order sets and read as a **percent chance**, rolled with the shared LCG when non-zero (`00301608`–`00301637`; Z-2); (3) answered by Z-19 (section 8g's table); (4) bounded: no instruction outside the three rebuilders forms an address in the `02089378` array (rip-reference scan), each rebuilder walks twelve slots (`00327E1A`, `00327FF4`, `00328187`), the one other referencing function only stores a set's base in unit `+0x6E0` (`0023AB9F`), and the walk reads records only below the subgroup's count byte (`00305DFD`–`00305E0A`), so records 12 and 13 are never evaluated.

## `Z-10` closed — 2026-09-08: it is the frame-rate scalar, and the timeouts prove it

**`DAT_01DFE0B8` is not the 2×/4× game-speed scalar.** The reopened question turned on the writer
setting `2.0f` against a shipped `1.0f`; the deciding evidence is not the writer at all but **what
reads the integer beside it.**

### The triple, and its default

| address | image value | written by `001EDDC0` |
|---|---|---|
| `01DFE0B4` | **1** (int) | **2** |
| `01DFE0B8` | **1.0f** | **2.0f** |
| `01DFE0BC` | **1.0f** | **0.5f** |

Read straight from `.data`. A mode, a scalar and its reciprocal, written together.

### What reads it — 212 references, and they are all timeouts

`01DFE0B4` has **212 references in 121 functions**, and the dominant idiom is one shape:

```asm
imul  ecx, dword ptr [01DFE0B4], 0x1E      ; 30
imul  eax, dword ptr [01DFE0B4], 0x3C      ; 60
imul  ecx, dword ptr [01DFE0B4], 0x5A      ; 90
imul  eax, dword ptr [01DFE0B4], 0x96      ; 150
imul  ecx, dword ptr [01DFE0B4], 0xF0      ; 240
imul  ecx, dword ptr [01DFE0B4], 0x384     ; 900
imul  eax, dword ptr [01DFE0B4], 0x4B0     ; 1200
imul  ebx, dword ptr [01DFE0B4], 0x5DC     ; 1500
imul  eax, dword ptr [01DFE0B4], 0x2328    ; 9000
imul  ecx, dword ptr [01DFE0B4], 0x7530    ; 30000
```

**30, 60, 90, 150, 240, 900, 1200, 1500, 9000, 30000 — every one a duration in 30 fps frames**:
half a second, one second, one and a half, two and a half, four, fifteen, twenty, twenty-five, one
hundred and fifty, five hundred.

> **This settles the question by direction of effect.** A 2× *game speed* selector makes the same
> durations elapse **faster**. This multiplies every authored timeout, so a 30-frame wait becomes 60
> — **the same wall-clock time at twice the frame rate.** Speeding the game up and doubling every
> timeout are opposite operations, and the engine does the second.
>
> **`01DFE0B4` is the factor that converts FFXII's PS2-era 30 fps authored durations to the rate the
> game is running at**, and `01DFE0B8` / `01DFE0BC` are the matching float scalar and reciprocal for
> per-frame deltas. **`Z-10` answers NO, on stronger ground than the previous NO, which rested on a
> false premise about the writer restoring a default.**

### How the writer is reached

`001EDDC0` has **no direct callers and no data pointers** — it is reached by a single **`E9` tail
call at `0022BE7D`**, from `0022BDF0` (146 B, tagged `FFXII.CoreRuntimeScheduling`), which passes the
mode in `ecx`. `001EDDC0` tests it and leaves the `{1, 1.0, 1.0}` defaults standing when it is zero.

**Found only because the reachability check covered `jmp` as well as `call`** — a call-only scan
reports this function as unreached, which is what makes it look like dead code.

### What is still open

*Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 16): nothing here is open; both items are answered (DH-1, DH-2).*

- [x] ~~**What decides the mode** — `0022BDF0`'s argument.~~ **`DH-1` ANSWERED.** It is
  **`FrameLimit`**, setting 18 of `GameSetting.ini`, read from `config->[+0x48]` by the 11-byte
  getter `0017D8F0`. Its two value names are `"30"` and `"60"`, and the mode passed on is
  `(FrameLimit == 1)`. Full chain in
  [`../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`](../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)
  section 12. **The separating observation this document itself named — "identify the object at
  `0x01F82D20` and read field `+0x48`" — is exactly what settled it.**
- [x] ~~**Whether any path writes a mode other than 2.**~~ **`DH-2` ANSWERED — no.** Closed from the
  source side rather than by searching for writers: `FrameLimit`'s value-name row is exactly two
  entries, NULL-terminated, and `0022BDF0` reduces even those to a boolean (`xor ebp,ebp` /
  `cmp eax,1` / `cmove ebp,1`), so any value that is not exactly `1` yields `0`. A hand-edited
  `GameSetting.ini` cannot reach a third mode either. **`01DFE0B4` is `1` or `2`, and the engine
  knows no other time base.**

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

**Platform: `FrameLimit` also filters the display-mode list.** The 11-byte getter `0017D8F0` (`DH-1`) has two raw
callers. One is `0022BDF0`, the frame-base selector. The other is the display object's mode-list builder, which the
ledger files under Platform. That builder is reached from the display constructor and from the monitor setter
([the config screen](../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md)).

The builder reads `FrameLimit` at `001DD581` (`sete dil` on `== 1`). It then compacts its array of 28-byte
`DXGI_MODE_DESC`-shaped records (`001DD5A6`–`001DD654`), keeping a record only if all three conditions hold:

1. it is at least **1280 × 720** (`cmp [r8], 0x500`, `cmp [r8+4], 0x2D0`);
2. its refresh denominator is non-zero;
3. its refresh rate `numerator / denominator`, truncated to an integer, is in the set that `FrameLimit` allows.

| `FrameLimit` | refresh rates kept |
|---|---|
| `60` (value 1) | 59 and 60 |
| `30` | 29, 30, 59 and 60 (constants `008F8D80`, `00900A10`, `00900A14`, `008F6D54`) |

Records that fail are swap-removed. So the setting that picks the gambit clock's time base also decides which
fullscreen modes are offered. Which list the options screen shows from this array is not read. *(Scope (FABLE, Claude Opus 5.5, 2026-09-30): what the options screen does with the list is a Platform / UI question, not this page's; [the settings page](../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md) carries the same crossing, and [the config screen](../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md) reads the screen-size row that cycles the display-mode list.)*

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — SERVICE and CLIENT (26 edges).** The target walk and the enmity code resolve units through that layer's unit-table accessors: `ActorWork_GetBattleUnit` `0031B760` (from `003014C0`, `00301AD0`, `003087E0`, `0030F130` and the team setter `00239170`), `BattleUnit_GetBySlotIndex` `00236820` and `BattleUnit_GetSlotCount` `00236850` (from `00301AD0`, `00308C20`, `0030F760`, `003219D0`), `BattleUnit_FindByDefinitionSelector` `002367A0`, `BattleUnit_FindByCombatantId` `0031B770`, `BattleUnit_FindMappedDefinitionSelectorByIndex` `0031B810`, `ActorRuntime_GetClassNibble` `00263C20` (the class-5 test inside `0030AB40`), `ActorRuntime_GetClass3FloatPair` `00265090` (from `0030F130` and `00312730`) and `BattleUnit_BuildFilteredFourSlotUnitBuffer` `0030A880` (from `00321630` and `00321B00`). In the other direction `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` calls the combat frame `00308610`, the unit-release body `00300FC0` (it cancels the current action and tail-jumps into `003138D0`, and on its other arm releases the target relation) calls `003138D0` and `003219D0`, and the `btlAtelSetBelong` thunk `00510280` calls the ActorEntity-owned team setter `00239170`. The relationship is lookup, not ownership: this page's AI and threat code index the unit pool that layer owns, and that layer's per-unit frame and teardown are the callers that run the AI frame and the threat spread.

**CombatAction — SERVICE and CLIENT (42 edges).** Selection hands its choice to the action layer: `003014C0` and `BattleUnit_SelectAndCommitNextAction` `00305AB0` call `BattleAction_CheckActionAvailabilityReason` `002FFCF0`; `00305AB0` and `00305CC0` commit through `BattleUnit_CommitAction` `0030F760`; `003087E0` calls `BattleAction_CheckTargetEligibility` `003083B0`; `00301AD0` calls `BattleTarget_ClassifyRelationshipClass` `0030AB40`, `BattleTarget_HasLow16EligibilitySuppression` `0030B9B0`, `BattleAction_GetSubtype3Field22OrFFFF` `003093D0` and `BattleAction_ComputeActiveTargetStatusIntersection` `0031C500`; `0030F130` calls `BattleAction_ComputeAuthoredStatusMask` `003872D0`; the combat frame `00308610` calls `BattleAction_CheckCurrentActionInterruptReason` `002FFB60`, `BattleUnit_AdvanceActionState` `00307BE0`, `BattleAction_TryContinueComboSequence` `0030FA00`, `BattleUnit_CancelAndResetCurrentAction` `003105D0`, `00308270` and `0030DA30`; `00306340` calls `003064F0` (the per-definition availability and licence test) and `003138D0` calls `BattleUnit_IssueCommand` `00311CF0`. Back into this page: `BattleUnit_ProcessPendingActionSelectionQueue` `00313CD0` calls `00305AB0`; `Battle_ProcessActionTarget` `00307300` and `BattleAction_ResolveSpecialSequenceTargets` `0030EC00` call `BattleEnmity_ApplyActionParameters` `003216E0`; the direct-state order handler `002FDDA0` calls `00321B00` and `0030FED0`; the goal handler `002FDA60` calls `00312730`; `002FE660` calls `00321190`; the eligibility predicates `002FFEF0`, `0030B8E0`, `0030BB10`, `0030BCB0`, `00311B20`, `00312170` call `0030AB40`; and `BattleUnit_ShouldEnterEngagedActionState` `00308010`, `0030FA00` and `BattleUnit_TryCommitEngageAutoAttack` `00312FA0` call page subjects (`00308040`, `0030F760`). The relationship is the gambit-to-action seam: the AI decides which action and target, the action layer validates, commits and runs it, and every landed action calls back into this page's enmity update.

**CombatFormula — SERVICE and CLIENT (8 edges).** `AiOrder_ComputeBoundedSelectorScalar` `00308C20` calls `BattleFormula_QueryResolvedScalarPreview` `00308B90`, which calls `BattleFormula_ResolveTargetResult` `00385F60`; `0030FED0` calls `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` and `BattleStats_FindOwningBattleUnit` `0031B860` and is called by `BattleFormula_ApplyTargetResult` `003112F0`; `BattleStats_InitializeDefinitionRecord` `0023AC80` calls the three gambit-bank initialisers `00326030`, `00327CB0` and `00327DE0`. The AI's predicted-HP operand prices already-committed actions with the formula's own resolver (section 8b), and the stats-record initialiser is what seeds each record's three gambit banks; nothing here computes a formula of its own.

**CoreRuntimeScheduling — DEPENDENCY (5 edges).** The boot fixup body `0022A0B0` calls the frame-base selector `0022BDF0`, which reads `FrameLimit` through `0017D8F0` and tail-calls the host-timing initialiser `001EDDC0`; `001EDDC0` in turn calls `0033F020`. This page depends on that chain only for the value it produces: the global time base that multiplies the enmity-decay interval (Z-3 and the Z-10 closure).

**Gameplay — SERVICE and CLIENT (39 edges).** `Gameplay` is the CodeDomain label of unowned battle helper leaves. The enmity readers and writers `003215C0`, `00321630`, `00321850`, `003219D0`, `00321B00`, the gambit config bodies `00327A10`, `00327CB0` and `0030FED0` call `BattleEncodedId_IsValidForClass` `00322C50`; the target builders `003014C0`, `00301AD0`, `003087E0`, `0030F130`, `0030F760` call `BattleTargetBuffer_ResetPreservingFlag0` `00316CF0` and `BattleTargetBuffer_TryAppendActorWork` `00316CD0`; `00301AD0` also calls `BattleEncodedId_DispatchQueryMode0Value` `00309EC0`, `BattleDefinition_GetRuntimeCategoryBySelector` `0031EA90` and `BattleUnit_GetPrimaryFormulaResourceByte26` `00321320`; `003014C0` calls `WorldActor_GetDefinitionByte12OrMinus1` `002E9C00`; `00301830` and `00312730` call `BattleRuntime_GetModeDependentDistanceThreshold` `00309A90`; `003138D0` calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0`; `00308610` calls `BattleUnit_DispatchActorPresentationEvent` `003299B0`; `002826F0`, `00282A40`, `00328990` and `0035D330` call the encoded-id definition resolver `0031C5D0`. The Z-4 engagement gate is itself filed there: `BattleUnit_HasActiveEngagementEvidence` `00307CE0` calls `0030BB30` and `BattleUnit_HasRelationshipClass2PlusInSlotMask` `0030C210` and is called by `00321530` and `BattleUnit_UpdateEngagementStateFlag` `00307D10`, while `00308040` calls `BattleUnit_HasRelationshipClass2PlusInTrackedActorList` `0030B050` and is called by `WorldActor_QueryCombatStanceState` `0030BFB0`. These are id-validity checks, target-buffer primitives and the engagement predicates this page reads in section 8c; the label is a domain filing, not a separate owner of gambit or threat behaviour.

**Items_Equipment_Shops_License — SERVICE and CLIENT (9 edges).** The equipment setters `BattleStats_SetEquipmentSlotByStatsIndex` `0031A410`, `BattleStats_SetEquipmentSlotByMappedId` `0031A510`, `BattleStats_SetEquipmentSlotDirect` `0031A630` and the licence-node setter `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` call `0030FED0`; `0031A260` calls `0031A410`; `00323600` calls `BattleStats_CheckLicenseNodeAcquireReason` `00323D10`; `00328BD0` calls `0031A260`; the party-list classifiers `002826F0` and `00282A40` call `Equipment_CheckItemEligibleAgainstCurrentLoadoutByStatsIndex` `00317B70`. A change of equipment or licence re-runs the derived-state rebuild that `resetJobs` also runs, and `resetJobs` clears a record's equipment slots through that layer; no gambit logic reads equipment directly.

**Movement — SERVICE (8 edges).** `AiOrder_CheckActionPreconditions` `00301830` calls `BattleLocomotion_DecodeOrderGoal` `00312730` and `BattleLocomotion_IsApproachConstraintActive` `0033A120`; the combat frame `00308610` calls the locomotion step `0033A240`; `00312730` calls `00309B10`, `BattleUnit_GetNavigationClearanceRadius` `0030A130`, the position-table sampler `00312DF0` and the global-flag gate `0031ABE0`; the host-timing initialiser `001EDDC0` calls `00337A00`, which derives two Movement-owned globals from the same frame multiplier (read: the multiplier times 30 and times 240). The AI asks locomotion whether an order's goal is reachable before choosing it, and the combat frame steps that locomotion; the time-base link is only that the initialiser which fixes the enmity clock also seeds that layer's timing globals.

**Party — SERVICE and CLIENT (23 edges).** `00301AD0`, `0030BB30`, `0030F760`, `00312730` and `003138D0` call `BattleUnit_ResolveByFocusHandle` `0031B7E0`; `00301AD0` and `00312730` call `BattleUnit_GetPartyLeader` `003272A0`; `00301AD0` calls `PartyFocus_IsCurrentPackedActorHandle` `003273B0`; the stance order handler `002FE840` calls `BattleUnit_EnterPartyCombatStance` `00313400` and `BattleUnit_ExitPartyCombatStance` `00313480`; `00308610` calls `BattleUnit_UpdatePartyCombatStanceState` `00307DF0`; `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040` calls `003137F0`. The `resetJobs` body `00328BD0`, filed to the Party domain, calls `0030FED0`, `003137F0`, `003138D0`, `00313550`, `0031A260`, `00326030`, `00327CB0`, `00327DE0`, `00328990` and `00559760`, and is called by its verb handler `00342230`. Target modes that name the leader or the player's focus resolve them through the party layer, the Z-14 stance order flips the party combat stance, and the party reset verb is the caller that reloads a record's gambit presets.

**Presentation — SERVICE, CLIENT and OUT-OF-SCOPE (15 edges).** `00301830` calls `BattleUnit_ComputePartyBattleStance` `00308130`; `00301AD0` calls `BattleUnit_TestActorViewFrustumAtCurrentPosition` `00322360`; `0030F760` calls `BattleUnit_BroadcastPartyCombatTargetRelation` `00313B30`. The rest reach bodies this page cites for other reasons: `0033F020` calls the six 60-fps table initialisers `00471100`, `00471330`, `004715F0`, `004718F0`, `00472580` and `00473210`; the encoded-id index resolver `0035D330` is called by `BattlePresentation_EnqueueReactionWithRandomizedVariant` `003BBD00` and the floating-number entry builder `00506700`; `002527B0` is called by the quest-list selection machine `00579420`; `003829D0` (cited only as the one caller on the Z-10 alias route) calls `003CC000` and is called by `CameraSystem_SelectAndPublishActiveView` `00259820` and `003ED8A0`. The first three are real consumers (an on-screen test for a selector, the party stance, and the target-relation broadcast after a commit); the others are fan-in on shared helpers and carry no gambit or threat meaning.

**RNG_Random_Selection — SERVICE, DEPENDENCY (5 edges).** `003014C0`, `00301830`, `003087E0` and `BattleData_ResolveWeightedId` `00308EC0` call `RNG_SharedGameplayLCG_NextU32` `00328370`, and `003014C0` calls `00308EC0`. Every random choice in this page (a weighted action pick, section 8i, and the random target and precondition rolls) draws from the one shared gameplay LCG, so gambit outcomes share its sequence with every other gameplay roll.

**Rewards_Progression_Economy — CLIENT and SERVICE (3 edges).** The level-advance body `0030C470` and `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` call `0030FED0`; `00312730` calls `Loot_FindNearestActivePickupPosition` `00319850`. A level-up re-runs the same derived-state rebuild `resetJobs` runs, and one order-goal kind walks the unit to the nearest active loot pickup.

**Script_VM_Native_Bridge — CLIENT (8 edges).** The verb handlers `summonread` `0034E1F0`, `summontopartyread` `0034FE80` and `btlAtelSetSummonMode` `0050FFB0` call `00313550`; `00348B40` pops two ints and tail-jumps into `GambitConfig_AdjustAvailableEntryCountByStatsIndex` `00327930`; the `resetJobs` handler `00342230` calls `00328BD0`; the `btlAtelSetBelong` thunk `00510280` calls `00239170`; `00342230` and `00510280` pop their arguments through `VMValueStack_PopInt32CoerceFloat32` `00267E10`. Script verbs are how authored events reach this page's state: the team byte, the summon-mode bit, a bank's entry count and the preset reset.

**Spawn_Encounter_Lifecycle — SERVICE and CLIENT (2 edges).** `00308040` calls `Spawn_ValidateCandidateDistanceToPlayers` `00234DA0`, and `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` calls `0030FED0`. The non-party engagement test borrows the spawn layer's distance-to-players test, and a spawned unit's activation runs the derived-state rebuild once.

**Status_Periodic_Terminal — CLIENT and SERVICE (9 edges).** `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls `BattleEnmity_UpdatePeriodicDecay` `00321530` and `003138D0`; the status bodies `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130`, `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, `BattleStats_RemoveAllMode0StatusesAndRecompute` `0030E8F0` and `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690` call `0030FED0`, which calls `0030E130` and `0030E360` back; `00328BD0` calls `0030FED0`. The threat decay of section 8c is driven from the periodic maintenance tick, and `0030FED0` is that layer's derived-state and auto-status rebuild, which this page cites only as one step of `resetJobs`.

**WorldAreaField — DEPENDENCY (12 edges).** `003014C0`, `00301AD0`, `00305AB0` and `0030F760` call `FieldData_GetActiveFieldRecordBit15` `00377C20`, and `00321850`, `00321B00` and `BattleEnmity_WriteAllCombatantIds` `00321D30` call its five-byte jump `00313F60`; `00301AD0` calls `FieldData_GetFormat0RecordVectorByIndex` `00320940`; `BattleSystem_RunFieldFrameOrchestrator` `00234590` calls `003137F0`; the field-byte operand getter `00377BA0` calls `WorldTransition_GetActiveOrPendingFieldId` `003148F0`, `SaveFlags_GetPayload1062Bit7` `00314AA0` and `SaveFlags_GetPayload1063Bits4To5` `00314AC0`. Action selection, commit and every enmity write consult the active field record's bit 15, and one gambit operand reads a field byte that a save flag can replace, so this page's behaviour depends on the field record without owning it.

## The `00328BD0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

The `resetJobs` verb body `00328BD0` (424 B) takes the preset id in `ebx`:
bounded against `5` / `0x27` (`00328BD9`/`00328BEE`), `0031A260` inits the
out-record (`00328C11`), `00328990` ×2 on `[02EBF190]`
(`00328C23`/`00328C35`), `00559760(ebx)` (`00328C3C`), `003137F0`'s result
is compared to `ebx` (`00328C41`–`00328C49`) with `003138D0(1)`
(`00328C52`), then `00313550`, `0030FED0` (`00328C66`), `0020E600` ×2 on
`[02EBF130]` (`00328C7A`/`00328C8E`), `00327CB0` (`00328CAA`).

| member | role | interior |
| --- | --- | --- |
| `0031A260` (153 B) | out-record initializer — `01F44830` cookie, seeds `{qword = -1, word = 0xFFFF}` (`0031A281`–`0031A291`), reads `word[rsi]` (`0031A2B0`) | [`0031A2B0`](../_index/ADDRESS-INDEX.md) |
| `00559760` (90 B) | three-branch dispatch — calls `00282E10` (`00559766`), `002527B0` ×2 (`00559786`/`005597A3`), `ebx` vs `3` bound (`005597AA`) | [`005597AA`](../_index/ADDRESS-INDEX.md) |
| `00282E10` (67 B) | group-slot lookup — `[0209AC30]` base, `rdx ≤ 9` bound (`00282E3E`), `[r10 + rax*8 + 0xAC8]` slot array (`00282E4A`), `0035D330(0x19)` index resolve → `byte[rax+0x20]` (`00282E6B`–`00282E70`), `00323600` (`00282E87`) | [`00282E4A`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00328990`, `003137F0`, `003138D0`,
`00313550`, `0030FED0`, `0020E600`, `00327CB0`, `002527B0`, `0035D330`,
`00323600`. `00282E10` is reached through `00559760`, not from the root.

## 9. Related (FABLE, 2026-09-30)

*Moved here from mid-page, where it sat between the two sections numbered 8i, and extended with the pages the later sections lean on: the walk contract, the set cascade, the keep bank, the bank storage, the gambit menu and the field-record accessors (FABLE, Claude Opus 5.5, 2026-09-30).*

- [`../13-Rewards-Progression-Economy/experience-and-license-point-award.md`](../13-Rewards-Progression-Economy/experience-and-license-point-award.md) — the same foe-class gate, found first
- [`../11-Party/party-roster-and-control-suppression.md`](../11-Party/party-roster-and-control-suppression.md) — the four slots the enmity scan walks
- [`../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md`](../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md) — BattleUnit identity and the pool
- [`../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`](../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md) — what happens after commit
- [`../16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`](../16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md) — `mGambitPositionOffsetX`, the gambit menu's layout
- [`CONTRACT-gambit-walk.md`](CONTRACT-gambit-walk.md) — the walk as a contract; §7 is the commit-reachability measurement
- [`which-gambit-set-fires-and-how-a-command-switches-it.md`](which-gambit-set-fires-and-how-a-command-switches-it.md) — the four-set cascade and the subgroup commands
- [`../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`](../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) — the keep bank that holds the threat table, and the return window
- [`../11-Party/Battle-State-Block/the-battle-state-block-field-map.md`](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) — the three banks and the selected-bank index
- [`../16-UI/Gambit-Screens/the-gambit-screens.md`](../16-UI/Gambit-Screens/the-gambit-screens.md) — the gambit menu that edits and commits the banks
- [`../03-World-Area-Field/CONTRACT-field-record-accessors.md`](../03-World-Area-Field/CONTRACT-field-record-accessors.md) — `00377BA0`, the MP regime opcodes 48 / 49 read
