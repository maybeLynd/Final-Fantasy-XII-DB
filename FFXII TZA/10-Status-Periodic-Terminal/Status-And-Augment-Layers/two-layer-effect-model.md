---
system: Two-layer status / augment effect model
category: 10-Status-Periodic-Terminal
status: DOCUMENTED
owner_layer: PrimaryOwner:CombatFormula (formula side) / Status (state side)
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  previous_parent: 381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: reverification-against-current-parent
  crossref_clean: true
  reopened_count: 1
---

# Two-layer status / augment effect model

> FFXII keeps *two* effect bitmaps per combatant at the same bit positions, then merges them
> before any damage formula runs. That merge is the source of several long-standing
> "why does that work?" oddities.

## 1. What the player sees

Equipping an Agate Ring grants Weatherproof. Equipping a Cameo Belt grants Accuracy Boost.
Neither is a "status effect" you can be hit with — they come from gear. But the damage
formula reads them from the *same* bit positions as Petrify and Disease, because it merges
both layers first.

## 2. Native mechanism

Each BKBI carries two 128-bit effect layers:

- **`+0x68` — ordinary, mutable status effects.** What spells and attacks inflict.
- **`+0x78` — derived, automatic effects.** Rebuilt from equipment, passives and licenses.

`0030E130` mutates either layer given a numeric ID `n`:
```
byteIndex = n >> 3
bit       = 1 << (n & 7)
```
The two layers deliberately share bit positions but **do not share a name namespace**.

`0030FED0` rebuilds the derived layer:
1. for each accepted equipped record, resolve the equipment definition, read one raw
   augment/effect ID byte, and if not the sentinel set that bit in a desired bitmap;
2. traverse authored passive/licence records, importing up to eight numeric effect IDs each;
3. reconcile the desired bitmap against current `+0x78` — add missing, clear stale.

`003847C0` then builds the formula context: for every ID `0..127` it tests the bit in **both**
caster layers and ORs the result into the merged bitmap at `FormulaEvaluationContext+0x1A`.

**After that merge, a calculator testing bit *n* cannot tell which layer it came from.**

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0030E130` | `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` | 553 B | mutate either layer |
| `0030FED0` | `BattleStats_RecomputeDerivedStateAndAutoStatuses` | 1,787 B | rebuild `+0x78` |
| `003847C0` | `BattleFormula_BuildEvaluationContext` | 273 B | merges both layers |

## 4. Data structures

```
BKBI
  +0x68  u8[16]  mutable status layer     (128 bits)
  +0x78  u8[16]  derived augment layer    (128 bits)

FormulaEvaluationContext
  +0x1A  u8[16]  MERGED effect bitmap     (caster +0x68 OR +0x78)

Equipment definition
         u8      Augment                  raw numeric augment ID
```

### Namespace map — same index, different meaning

| Bit | Mutable status (`+0x68`) | Derived augment (`+0x78`) | Formula role |
|---:|---|---|---|
| 2 | Petrify | **AccuracyBoost** (Cameo Belt) | ranged severe-weather accuracy bypass |
| 16 | Disease | **Weatherproof** (Agate Ring) | weather/terrain element-scaling bypass |
| 17 | Lure | Thievery | none established |

This is a namespace map, **not** a claim that the paired names are related.

### Observable consequence

Because the layers merge, a combatant with **Disease** (status bit 16) satisfies the same
early-out as one with **Weatherproof** (augment bit 16). The intended identity is
Weatherproof; the alias is a real, observable engine property.

## 5. Call chain

```
equipment / licence / passive change
  -> 0030FED0  rebuild derived layer  -> BKBI +0x78

spell / attack inflicts an effect id (the result record's effect-id bytes, the applier's step 14)
  -> 0030E130  -> BKBI +0x68

action resolution
  -> 003847C0  merge both -> FormulaEvaluationContext +0x1A
     -> 0038B220   tests merged bit 16   (weather/terrain bypass)
     -> 003895D0 / 00389610  test merged bit 2  (ranged accuracy bypass)
```

**"Status" here is an effect id, not one of the 32 battle statuses.** *(Clarified 2026-09-29, FABLE, Claude Opus 5.5;
`_index/candidates/pkg-gp-status-poison/layers.py` N C A.)* The 32 battle statuses, Poison among them, live in the status
words `+0x64` / `+0x3C`. [The status write](../Status-Write/the-status-write-and-its-side-effects.md) writes them, and it never
calls the layer mutator. An inflicted Poison never enters `+0x68`.

**Do not confuse with:** the target-side tests in `0038B220`, which read the two BKBI layers
*directly* rather than the merged context.

## 6. Modding notes

- **To add an augment to gear:** write the raw `Augment` byte in the equipment definition.
  `0030FED0` will bit it into `+0x78` automatically.
- **Regenerates itself:** `+0x78` is fully derived. Never write it directly — the next
  rebuild will overwrite you.
- **XIIOnline:** never network the merged bitmap or either layer as ad-hoc flags. Synchronise
  the *owners* — statuses through the native status transaction, equipment/licence/passive
  state through their own owners — then let each receiver run `0030FED0` locally.
- **Mod compatibility:** unusually good here. A mod may change equipment augment bytes,
  passive sources, augment behaviour or formula logic and the native rebuild still feeds the
  formula coherently. Do not hardcode vanilla augment IDs into networking.

## 7. What is not known

- [x] ~~Whether the same-bit aliases are intentional design shortcuts or incidental collisions
      (open question **E-1**).~~ **Closed 2026-09-12 as intent residue** on [the namespaces README](../../08-Combat-Formula/Status-And-Augment-Namespaces/README.md): Petrify and Disease casters fire the AccuracyBoost and Weatherproof bypasses through the merged context; Lure's alias is inert.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Two layers at `+0x68` / `+0x78`, shared bit arithmetic | complete body of `0030E130` (553 B, `f985df17…af95`) | 1 |
| `+0x78` is derived from equipment/passives | complete body of `0030FED0` (1,787 B / 0x6FB, `01a49b97…e853`) | 1 |
| Context merges both layers for IDs 0..127 | complete body of `003847C0` (273 B, `a6b21a9e…b536`) | 1 |
| Augment 2 / 16 / 17 names | Xeavin public Workshop `Helpers/EnumHelper.cs` — `AccuracyBoost=0x4`, `Weatherproof=0x10000`, `Thievery=0x20000` | 6 |
| Status 2 / 16 / 17 names | same source, separate status enum — `Petrify=0x4`, `Disease=0x10000`, `Lure=0x20000` | 6 |
| The same three names, and all 32 status names, from the game's data | bank 5 of [the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md), in id order; the augment descriptions 2 / 16 / 17 from the augment table's references into `listhelp_ability.bin` match AccuracyBoost / Weatherproof / Thievery (2026-09-11) | data |
| Equipment stores a raw augment byte | Workshop `Formats/Battlepack/EquipmentAndAttributes.cs` — `public byte Augment` | 6 |
| Agate Ring = Weatherproof, Cameo Belt = Accuracy Boost | external FFXII mechanics + Xeavin Forge post | 10 |

**Superseded readings:**
- *Old:* all bits in the `+0x68`/`+0x78` family are one undifferentiated status namespace.
  *New:* two namespaces at shared positions, merged only at context construction.

## 9. Related

- [`../../08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md`](../../08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md)
- [`../../08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md`](../../08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md)

## Re-verification 2026-09-02 (AH-9)

Stamped against parent `381d2aea...`; re-checked against the current `2ed8affb...`.

**Addresses:** 6 cited, **6 resolve as function entries**, 0 unresolved.

**Central claim corroborated seven times over.** The headline is *"FFXII keeps two effect bitmaps per
combatant at the same bit positions, then merges them before any damage formula runs."*

That merge is `(layer0 | layer1)`, and this session read it **independently in seven functions**
while working on unrelated subsystems - and three more were added on 2026-09-02 during the AH-6 re-verification, bringing the count to **ten**:

| Function | Subsystem |
|---|---|
| combat action eligibility gate | Combat Action |
| `Reward_ComputeExperienceForRecipient` | Rewards |
| `Reward_ComputeLicensePointsForRecipient` | Rewards |
| `PartyControl_RecomputeSuppressionFromLeaderBattleState` | Party |
| `BattleEnmity_WriteAllCombatantIds` | Combat AI |
| `AiOrder_EvaluateAndResolveActionTarget` | Combat AI |
| `BattleAction_CheckActionAvailabilityReason` | Combat Action |
| `BattleUnit_IssueCommand` | Combat Action - **added 2026-09-02** |
| `FUN_00313DB0` presentation-ready ring consumer | Combat Action - **added 2026-09-02** |
| `BattleUnit_ProcessPendingActionSelectionQueue` | Combat Action - **added 2026-09-02** |
| `Reward_ComputeExperienceForRecipient` / `Reward_ComputeLicensePointsForRecipient` | Rewards - **added 2026-09-02**, and at a **new offset pair** `+0x6B`/`+0x7B` rather than the status masks' `+0x3C`/`+0x64`, showing the two-layer test is a convention applied at several field pairs |

Every one computes `(dwStatusMaskMode0_3 | dwStatusMaskMode1_4)` before testing it. **The two-layer
merge is not a local detail of the status system - it is the engine-wide convention**, and this
document called it correctly before any of those seven were read.

None of the seven was sought out to confirm this document; each was read for its own subsystem and
recognised afterwards.

**Independently corroborated by census 2026-09-02.** A caller census over all 478 functions with
≥ 20 callers ranked every function by how many distinct **owner subsystems** call it. Excluding CRT
and runtime plumbing, `FieldData_GetActiveFieldRecordBit15` — the accessor in this predicate — has
the **widest subsystem reach of any gameplay function in the executable** (13 subsystems). The ten
sightings below were gathered one function at a time; this is a quantitative result from an
unrelated method reaching the same conclusion. See
[`../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md) §9.

**Stamp advanced on the strength of seven independent sightings** (now ten), which is stronger evidence than a
single re-read would have been.

## 11. The other half of `0030E130` — 2026-09-03, session `repos-78`

Section 2 reads `0030E130` for its bit arithmetic and section 8 cites *"complete body … tier 1"*. **The
bit arithmetic is confirmed exactly.** But the function is named
`BattleStats_ModifyStatusLayerStateAndProcessSideEffects`, and **the side-effect half is not described
anywhere above** — 553 bytes for `byteIndex = n >> 3` is a great deal of code. It is read here.

**This is a third shape of cut entry**, distinct from *read-but-uncited* and *cited-by-an-index*:
**read for one purpose, with the rest of the body unexamined.**

### Four modes, and applying a status you already have does nothing

The mode argument selects layer and direction, and **each mode aborts if the bit is already in the
requested state**:

| mode | layer | action | aborts when |
|---:|---|---|---|
| 0 | `+0x68` | **clear** | the bit is already clear |
| 1 | `+0x78` | **clear** | already clear |
| 2 | `+0x68` | **set** | already set |
| 3 | `+0x78` | **set** | already set |

```asm
0030E217  movzx eax, byte ptr [rbx + 0x68]
0030E21B  test  esi, eax
0030E21D  jne   0x30e32e          ; already set -> return, no side effects at all
0030E223  bts   eax, r15d
```

> **Re-applying a status a unit already has is a complete no-op** — the function returns before the
> auxiliary update, before the transition result, and before every side effect below. **Only a change
> of state does anything.**

### The side effects run only when combined presence changes

After the write, the function recomputes whether the id is set in **either** layer and compares that
against the value from before:

```asm
0030E269  test  byte ptr [rbx + 0x68], sil
0030E26F  test  byte ptr [rbx + 0x78], sil     ; present in EITHER layer?
0030E27B  cmp   r13d, dword ptr [rsp + 0x30]
0030E280  je    0x30e32e                       ; unchanged -> stop
```

**So the two layers gate side effects by their union, not individually.** Setting an id in layer 0
while layer 1 already carries it changes the stored bit and fires nothing — which is the behavioural
consequence of the same-bit aliasing this document raises as open question **E-1**.

### It builds a transition result and hands it to the ordinary applier

```asm
0030E28D  mov   r8d, 0x148
0030E293  call  memset                                   ; the 0x148 result record
0030E29C  lea   rcx, [rip + …]   -> 00386AE0             ; BuildRandomElementStatusTransitionResult
0030E2A9  lea   rax, [rip + …]   -> 00386A50             ; BuildInactiveStatusTransitionResult
0030E2B0  cmovne rax, rcx                                ; set -> random-element, clear -> inactive
0030E2BC  call  rax
0030E2DA  call  BattleFormula_ApplyTargetResult          ; 003112F0
```

**The same `0x148` result record and the same applier as the periodic tick.** Status application,
status expiry and the periodic drain all converge on `BattleFormula_ApplyTargetResult` — see
[`../Periodic-Tick/what-the-periodic-tick-does.md`](../Periodic-Tick/what-the-periodic-tick-does.md).

**The builder is chosen by function pointer with `cmovne`**, so a scan for `call <literal>` finds
neither of the two builders at this site.

### Status ids `0x68`–`0x71` change how many gambit lines the unit can use

```asm
0030E303  sub   r14b, 0x68
0030E307  cmp   r14b, 9
0030E30B  ja    0x30e31c                ; outside 0x68..0x71 -> skip
0030E30D  lea   edx, [rbx*2 - 1]        ; set -> +1, clear -> -1
0030E317  call  GambitConfig_AdjustAvailableEntryCountByStatsRecord
```

> **Ten consecutive status ids — `0x68` to `0x71`, 104 to 113 — each adjust the unit's available
> gambit-slot count by one**, up when the status is set and down when it is cleared. Nothing else in
> the id space touches that counter.

That is the mechanical link between the status system and
[`../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md):
the gambit config holds **twelve slots and a 16-bit enable mask**, and **the count of usable entries is
what these ten statuses move.**

Finally, `BattleStats_RecomputeDerivedStateAndAutoStatuses` runs **unless bit 9 of the flags word is
set** — so a caller can suppress the derived-layer rebuild. **Who sets it (read 2026-09-12, FABLE):**
the flags word is the function's sixth argument (`[rsp+0x28]` at the call, `[rsp+0x228]` inside;
[the status-write page](../Status-Write/the-status-write-and-its-side-effects.md) §4 lists bits 0, 1, 4 and 9). Bit 9 is a **"recompute once" contract**: the function
sets it on its own cascade self-call (`bts eax, 9` at `0030E6AE` before `0030E6C7`, once per bit of
the status row's clear-mask `+0x0C`), so the statuses a status clears are removed without a rebuild
each and the outer call rebuilds once at `0030E828`; and `BattleStats_RemoveStatusesFromMaskAndRecompute`
passes the literal `0x217` (bits 0, 1, 2, 4, 9; `0030F721`) for every status in its mask and recomputes
once itself. Of the fourteen call sites in the graph no other passes a value with bit 9: the mode
wrappers, the HP-lethal path, the direct-state order and the special sequence pass 0 or forward a
caller's word, and `BattleFormula_ApplyTargetResult` forwards its own flags (`0031153A`). The word is
also forwarded whole to `BattleFormula_ApplyTargetResult` as its fifth argument when the status's
extra effect fires (`0030E61A`–`0030E638`). Bit 2, which only the `0x217` literal carries, is tested
nowhere in this function.

### The three "0x10-stride" sightings are one fact

A cross-check raised `+0x6B`/`+0x7B` and `+0x6E`/`+0x7E` alongside this document's `+0x68`/`+0x78` as a
0x10 stride seen in three subsystems. **They are the same two layers.** Each layer is 16 bytes, so
every byte inside them is `0x10` apart by construction:

| offsets | byte of each layer | status ids |
|---|---:|---|
| `+0x68` / `+0x78` | 0 | 0–7 |
| `+0x6B` / `+0x7B` | 3 | 24–31 |
| `+0x6E` / `+0x7E` | 6 | 48–55 |

**One structure, three windows into it — not three structures with a shared stride.** And the
arithmetic pays: a test of **bit `0x10` at `+0x6E`/`+0x7E`** is `byte 6, bit 4`, which by this
document's own `n >> 3` / `1 << (n & 7)` rule is **status id 52**.

### What is not established

- [x] ~~What status id 52 is, and what the ten ids `0x68`–`0x71` are individually.~~ **Read
      2026-09-12 (FABLE) from the augment table's texts** (`02EBF040` row `+2` → bank 10,
      [the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md)): rows 104–113 (`0x68`–`0x71`) all carry *"Adds an additional gambit slot."* —
      ten identical augments, one slot each, which is exactly what the adjuster above does with
      them; row 52's text is *"NOT USED"* — an unused augment id in the shipped data, tested here
      as byte 6 bit 4 of the layers but granted by nothing the tables ship.
- [x] ~~What the second function-pointer pair (`0046A720` / `0046A790`) does.~~ **Read 2026-09-12
      (FABLE):** each maps the status id `dx` — `0x37`, `0x38`, `0x39` — to a battle-message id and
      posts it through `0046AB10(unit, id, &ctx)`: `0046A720` posts `0x3F` / `0x41` / `0x43`, `0046A790`
      `0x3E` / `0x40` / `0x42` — the rise and fall lines of Paling, Magick Shield and White Wind
      ([the post-result events page](../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) §2).
- [x] ~~What flags-word bit 9 means, beyond suppressing the derived rebuild.~~ **Answered 2026-09-12
      (FABLE):** nothing beyond it — it is the recompute-once marker the cascade self-call and the
      mask remover set so a chain of status changes rebuilds the derived layer a single time (§11,
      the recompute paragraph; call-site census over all fourteen sites).
- [x] ~~What `BattleEncodedId_IsValidForClass(0x1D, …)` gates at the top of the side-effect block.~~
      **Read 2026-09-12 (FABLE):** class `0x1D` = 29 is the augment table `02EBF040` ([the encoded-id space page](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)
      §2.10), so the gate is "the id names a shipped augment row" — `0 ≤ id < 129`, the table's
      count at `+4`; a null table fails every id.

## 12. Five new namespace entries, from the MP economy — 2026-09-07, session `xiionline-61`

**An extension, not an audit pass.** This document's own claims were not attacked here; it remains in
the `CQ-3` cohort. What follows is five effect ids whose *function* was proven while reading the MP
system, mapped through **this document's own** `byteIndex = n >> 3, bit = 1 << (n & 7)` convention.
Source: [`../where-mp-comes-from.md`](../where-mp-comes-from.md).

| effect id | byte | mask | what it does |
|---:|---|---|---|
| **20** | `+0x6A` / `+0x7A` | `0x10` | grants MP for **dealing** damage — but only on actions whose definition row sets `+0x2C` bit 4 |
| **21** | `+0x6A` / `+0x7A` | `0x20` | grants MP for **taking** damage |
| **23** | `+0x6A` / `+0x7A` | `0x80` | grants a **kill bonus** of `max(targetLevel / 4, 1)` MP |
| **39** | `+0x6C` / `+0x7C` | `0x80` | **pins MP to zero** — the capacity becomes 0, so no path can raise the value |
| **86** | `+0x72` / `+0x82` | `0x40` | the *other* "MP for dealing damage" route, paired with action row `+0x2C` bit 3 |

Every one is tested as `(layer0[k] & m) || (layer1[k] & m)`, so **the alias property this document
establishes applies to all five**: a temporary status and a derived augment are interchangeable at
these ids, exactly as Disease aliases Weatherproof at id 16.

> **Two of them sit in bytes this document had not reached.** `+0x6C`/`+0x7C` is byte 4 and
> `+0x72`/`+0x82` is byte 10 — the namespace map so far covers only byte 0 (id 2) and byte 2 (ids 16,
> 17). **The layers are used far wider than the three named entries suggest**, and id 86 shows the
> upper half is populated too.

**Their licence-board names are not established** *(answered since — `CS-1`, 2026-09-12, on
[where MP comes from](../where-mp-comes-from.md))* — filed as `CS-1` in
[`../../_index/OPEN-QUESTIONS.md`](../../_index/OPEN-QUESTIONS.md). Naming them from FFXII's augment
list by matching descriptions would be exactly the kind of plausible guess this database does not
accept: the *behaviour* is proven, the *label* is not.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

- **Audio.** `BattleFormula_ApplyTargetResult` (`003112F0`) plays its sound directly through the sound resolver and
  player, bypassing the gated wrapper ([applying a result to a target](../../07-Combat-Action/applying-a-result-to-a-target.md)).
- **Spawn_Encounter_Lifecycle.** The recompute `0030FED0` is called from `SpawnUnit_FinalizeSpawnEntryActivation`, so
  a spawned unit's augment-driven auto-statuses are rebuilt when its activation finishes.
- **Movement.** The battle event poster `0046AB10` is also called by a Movement-filed body in the `00469xxx` poster
  client group ([the gambit walk](../../09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md), crossings).

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Input — SERVICE.** A 360-byte function this page cites calls a 1,936-byte Input body.
- **InputGameplay — SERVICE.** The same 360-byte function calls the single function labelled InputGameplay (289 bytes, inside the Input layer).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CombatAction — CLIENT and SERVICE (4 edges).** The direct-state handler `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` calls `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130` and `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0`; `Battle_ProcessActionTarget` `00307300` calls the ordinary applier `BattleFormula_ApplyTargetResult` `003112F0`, which calls `BattleTarget_HasLow16EligibilitySuppression` `0030B9B0`. An action handler can write a layer directly through the two entries this page describes, and every action result reaches the layers through the applier after the eligibility test.

**CombatFormula — SERVICE and CLIENT (24 edges).** `0030E130` calls `003112F0`, `BattleFormula_BuildInactiveStatusTransitionResult` `00386A50` and `BattleFormula_BuildRandomElementStatusTransitionResult` `00386AE0`, and is called back by `003112F0`; `0030FED0` calls `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` and `BattleStats_FindOwningBattleUnit` `0031B860` and is called by `003112F0`; `003112F0` calls `BattleStats_SetCurrentHP` `00300520`, `BattleStats_ModifyHPAndProcessLethalState` `00300530`, `BattleStats_ModifySecondaryResource` `00300BC0`, `BattleStats_SetPrimaryResourceAbsolute` `00300C90`, `BattleStats_ModifyPrimaryResource` `00300CE0`, `0031B860` and `BattleFormula_ApplyResultMetadata` `00385BA0`; `BattleFormula_BuildEvaluationContext` `003847C0` (called by `BattleFormula_EvaluateTargetPreview` `00385680` and `BattleFormula_ResolveTargetResult` `00385F60`), `00386AE0`, `0038B220` and `0046AB10` call `0031B860`; `00386A50` and `00386AE0` call `BattleFormula_InitializeResultRecord` `003848E0`, and `00386AE0` calls `00384B10`; `BattleFormula_DispatchPostResultEvents` `00469EC0` calls the battle-message poster `0046AB10`. This is the page's own mechanism seen from the formula side: a layer change is built as a transition result and handed to the ordinary applier, which writes HP and resources and calls back into the layer entries, while the evaluation context and the weather / terrain stage `0038B220` read the merged layers.

**CoreRuntimeScheduling — SERVICE (1 edge).** `0046AB10` calls `GameClock_GetRawTickCounter` `0032A150`. The poster that carries the rise and fall lines of Paling, Magick Shield and White Wind keeps a ten-entry ring of recent posts (message id, unit, tick) and, for a message whose table row has flag bit 0 set, drops a repeat for the same unit that arrives within a fixed tick window; the clock is read only for that window.

**Gameplay — SERVICE (3 edges).** `0030E130` and `0030FED0` call `BattleEncodedId_IsValidForClass` `00322C50`, and the presentation-ready ring consumer `00313DB0` calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0`. The layer entries validate encoded ids before they act on them, and the ring consumer reads the battle runtime mode; both are shared ownerless helpers.

**Items_Equipment_Shops_License — CLIENT and SERVICE (5 edges).** `BattleStats_SetEquipmentSlotByStatsIndex` `0031A410`, `BattleStats_SetEquipmentSlotByMappedId` `0031A510`, `BattleStats_SetEquipmentSlotDirect` `0031A630` and `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` call `0030FED0`; `003112F0` calls `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` `003008A0`. Changing equipment or a License node rebuilds the derived layer (equipment and Licenses grant auto-statuses), and a result that carries an item change goes to the inventory through the applier.

**Party — CLIENT and SERVICE (2 edges).** `00328BD0` calls `0030FED0`, and `00313DB0` calls `BattleUnit_ResolveByFocusHandle` `0031B7E0`. The party stats reset support rebuilds the derived layer, and the ring consumer resolves each entry's focus handle through the party layer.

**Rewards_Progression_Economy — CLIENT and SERVICE (5 edges).** `0030C470` and `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` call `0030FED0`; `003112F0` calls `GameState_GetGil` `00253690`, `GameState_SetGil` `00254EE0` and `0030C650`. A level-up rebuilds the derived layer, and the applier also carries gil and level results; the reward layer and the status layers share the applier, not state.

**WorldAreaField — SERVICE (1 edge).** `00313DB0` calls `FieldData_GetActiveFieldRecordBit15` `00377C20`. The ring consumer re-checks a status-bearing unit against the area's action-permission bit; this page's layers are not read there.
