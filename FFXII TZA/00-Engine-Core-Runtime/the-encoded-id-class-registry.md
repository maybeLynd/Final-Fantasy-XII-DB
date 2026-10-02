---
system: The encoded-id class registry
category: 00-Engine-Core-Runtime
status: "DOCUMENTED — the SECTION-05 validator/filler reopening is resolved (SECTION-05 accepted by a non-author review 2026-09-29); row layouts SUPERSEDED under UQ-80's class-1 ruling; which classes code passes is answered (RC-1: 26 named; 4, 16, 22 and 27 by no caller); prior audit historical; owner read 2026-09-30 (OPUS, _index/candidates/dd-owner-read-b1-0930/)"
owner_layer: CodeDomain — shared; no PrimaryOwner
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: "snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30"
    verified: "re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS"
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-22
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-encoded-id-class-registry-pass-1
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# The encoded-id class registry

> **A class number is an identity, not a description** — so here is the table that turns each of the
> **32 classes** into the thing it validates against. Four documents in this database cite a class
> number; none of them could see the others' numbers, because the mapping was only ever in a jump
> table.

## Current validator versus filler boundary — SECTION-05

The validator's all-class coverage exists in EXP-143. The new section independently reconciles its
246 traced retained records and four summary-only returns; no new full historical emulator run is
claimed. Class 19 ends at `0xEFFE`. `01EEBCC0+38` and `01EEBCF8+0` are the same class word, not competing
layouts. The descriptor index is the top nibble; its shipped class is that value plus 5.

The validator admits class 12 with a suitable loaded count, but the query filler rejects it directly.
It does not fall through from `0031C650` into the class 2 arm `0031C65A`. Class 13's validator sums four
descriptors; the filler chooses only three fixed row intervals. This is why validating an ID is not
proof that every desired output field will be assigned. Direct fill, static-wrapper failure clearing,
rebase side effects and current tagged layouts are specified in
[the query mechanism](the-query-record-from-initialization-to-reuse.md) and
[Section05 evidence](../_experiments/evidence/continuation-section05-encoded-query/REVIEW.md).

*The trigger this page was reopened for is resolved (2026-09-30, SWE2-CONTRACT, cited, not re-run).* SECTION-05 is
accepted by a non-author review: SWE2-AUDIT-SEM re-executed `continuation-section05-encoded-query/run_review.py` on the
certified image (200 native assertions, an identical repeat, 7 mutants refused, 246 retained traces, 8 negative
controls) and returned `verdict:ACCEPT` on the contract (`FRONTIER-REVIEW-AUDITSEM-OV-ACCEPTANCE-0929`, record
`Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-ov-acceptance.md`, OV-3), and the same review accepts the
query-record page (OV-9). The carrier `FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929` is DONE. Tier 1 (isolated
original-code execution, reviewed).

## What the player sees (SWE2-CONTRACT, 2026-09-30)

Nothing directly. Every item, piece of equipment, loot, magick, technick, key item, licence square, status, gambit
and battle command in the game has a number, and before the game uses one of those numbers it asks this registry
whether the number is real for its kind. That check is why a corrupted or hand-edited save that names an item or a
licence that does not exist is quietly ignored rather than showing garbage. The counts behind most kinds come from the
game's battle data file, so a mod that adds rows to one of those tables changes which numbers the game accepts. Three
kinds have their limits built into the program instead and cannot be changed by data.

## 1. Why this exists

`BattleEncodedId_IsValidForClass(class, id)` is consulted before an id is used as an index almost
everywhere — the License check, the party configuration, the slot maps, the actor layer. Documents
have recorded the class they observed and stopped there, because **nothing in the corpus mapped a
class number to a table**. This does.

## 2. The dispatch

```asm
00322C5A  lea  eax, [rcx - 1]                       ; class - 1
00322C5F  cmp  eax, 0x1F
00322C62  ja   fail                                 ; valid classes are 1..32
00322C72  mov  ecx, [00120000 + rax*4 + 0x203054]   ; jump table at 00323054
00322C7C  jmp  rcx
```

**A 32-entry jump table at `00323054`, indexed by `class − 1`.** Most arms load a table descriptor and
compare the id against the count at its `+4`; three arms do something else (§4).

## 3. The registry

| class | descriptor | class | descriptor | class | descriptor |
|---:|---|---:|---|---:|---|
| **1** | *derives the class from the id* (§4) | 12 | `02EBF0D0` | 23 | *literal bound 9* → ids **0–8** (§4) |
| 2 | `02EBF130` | **13** | `02EBF090` **+ `02EBF088` + `02EBF080` + `02EBF078`** — four counts summed (§9) | 24 | `02EBF110` |
| 3 | `02EBF120` | 14 | `02EBF070` | 25 | `02EBF038` |
| **4** | `02EBF150` | 15 | `02EBF068` | 26 | `02EBF118` |
| 5 | `02EBF100` | 16 | `02EBF060` | 27 | `02EBF050` |
| 6 | `02EBF0F8` | 17 | `02EBF0C8` | 28 | `02EBF0B0` |
| 7 | `02EBF098` | 18 | `02EBF058` | 29 | `02EBF040` |
| 8 | `02EBF0F0` | **19** | *range `0xE000`–`0xEFFE`* (§4) | 30 | `02EBF068` |
| 9 | `02EBF0E8` | **20** | `02EBF138` | 31 | `02EBF068` |
| 10 | `02EBF0E0` | 21 | `02EBF128` | 32 | `02EBF038` |
| 11 | `02EBF0D8` | **22** | *literal bound 4* → ids **0–3** (§4) | | |

**Classes 30 and 31 share class 15's arm; class 32 shares class 25's.** Confirmed by decoding the
table: **29 distinct arm addresses for 32 classes** — `00322EBB` serves 15 / 30 / 31 and `00322FCB`
serves 25 / 32. Two shared arms over five classes, not three separate tables.

## 4. The three arms that are not a table bound

- **Class 1 — dynamic.** `movzx ecx, bx ; call FUN_00309440 ; dec eax ; cmp eax, 0x1F ; jbe` — it
  **derives a class from the id and re-enters the switch**. A caller passing class 1 is saying *"work
  out what this id is"* rather than naming a class.
- **Class 19 — a compiled-in count.** `mov edx, 0xE000 ; mov ecx, 0xEFFF` — and the shared tail
  rejects `id > ecx - 1`, so validity is `[0xE000, `**`0xEFFE`**`]`, **not** ~~`[0xE000, 0xEFFF]`~~
  (corrected 2026-09-13). That is exactly `0xFFF` ids, which is the capacity the kind table records
  for nibble `0xE` — so class 19 follows the same `lo ≤ id < lo + count` rule as the table arms,
  with the count compiled in rather than read. §9.
- **Class 23 — a literal bound of 9.** `mov ecx, 9`. No table; the count is compiled in → ids `0–8`.
- **Class 22 — a literal bound of 4.** `mov ecx, 4 ; xor eax, eax ; jmp 0x32302C`, the same shape as
  class 23 sitting immediately before it → ids `0–3`. **Added 2026-09-13** — §3 recorded only "no
  global read" and this section missed it.

> **Four of the thirty-two do not consult a table** — 1, 19, **22** and 23 — so "the class picks a
> table" is the rule and not the definition. A reader who assumed a descriptor for every class would
> be wrong ~~three~~ **four** times. *(Corrected 2026-09-13: class 22 is a literal bound of 4.)*

## 5. What this settles across existing documents

| Class | Cited by | Confirmed |
|---|---|---|
| **20 (`0x14`)** | [the License check](../12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md) — actions | → `02EBF138`, **the same action table that document reads** |
| **23 (`0x17`)** | [the party configuration](../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) — configuration indices | → **literal bound 9**, and that document independently found **nine** configuration slots |
| **1** | the same License document — equipment | → **not an equipment class**; the dynamic arm. Refined there. |
| **4** | the slot-map frontier | → `02EBF150` |

**Two of these are independent confirmations.** The action table and the nine-slot bound were each
established by reading a *consumer*; this document reaches them from the *validator*, which shares no
code with either.

> **The one it corrects is the more useful.** A document had recorded class 1 as "the equipment class"
> because equipment passes it. **Class 1 names no class at all** — and that is invisible from any call
> site, because a call site only shows the number going in.

## 5b. Naming the descriptors — 14 of 25, by who reads them

A descriptor carries no identity; **the functions that walk its rows do**. Censusing every
rip-relative reference to each descriptor and keeping the *named* referrers gives:

| class | descriptor | named by | reading | named referrers |
|---:|---|---|---|---:|
| **20** | `02EBF138` | `BattleAction_*` ×many, `AiOrder_EvaluateTargetSelector` (`00301AD0`) | **action definitions** — the most-referenced table in the game | 128 refs |
| **6** | `02EBF0F8` | `Equipment_SelectPreferredCandidateByAuthoredStats` (`002F7A10`), `ItemDefinition_ClassifyEncodedItemCategory` (`002FABD0`) | **equipment definitions** | 42 refs |
| **2** | `02EBF130` | `BattleUnit_ApplyUnitDefinition` (`0023A570`), `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0030C650`) | **character/unit growth definitions** | 23 refs |
| **26** | `02EBF118` | `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`), `BattleFormula_BuildCandidateStatusMask` (`003851F0`), `BattleStatus_ComputeDefaultShortTimer` (`003876D0`) | **status definitions** | 18 refs |
| **25** | `02EBF038` | `LicenseData_BuildPrerequisiteNodeMaskForRequirement` (`002F8FA0`), `BattleStats_SetLicenseNodeStateAndApplySideEffects` (`00323910`) | **License board nodes** | 15 refs |
| **29** | `02EBF040` | `BattleStatus_ComputeDefaultAuxiliaryTimer` (`00387020`), `BattleFormula_AdvanceStatusLinkedAuxTimers` (`00385570`), `BattleAction_ComputeChargeLimitTicks` (`002F8410`) | **status auxiliary / timer parameters** | 15 refs |
| **11** | `02EBF0D8` | five `Gambit*` functions | **gambit definitions** | 7 refs |
| **3** | `02EBF120` | `BattleUnit_ApplyUnitDefinition` (`0023A570`), `BattleData_SetAreaArdSectionCategory` (`0023A160`) | a **unit-definition** table | 7 refs |
| **18** | `02EBF058` | `BattleIdClassD_*` ×3, `InventoryBundleClass0D_ApplyNestedItems` (`002FD780`) | **item class `0xD`** entries | 8 refs |
| **4** | `02EBF150` | `BattleUnit_ApplyUnitDefinition` (`0023A570`), `BattleStats_RebuildEffectiveStatsAndAffinityState` (`002FEF30`) | a **unit-definition** table | 5 refs |
| **8** | `02EBF0F0` | `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (`003008A0`) | **inventory item** entries | 5 refs |
| **10** | `02EBF0E0` | `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` (`00327CB0`) | **gambit presets** | 4 refs |
| **15** | `02EBF068` | `InventoryBundleClass0A_ApplyNestedItems` (`002FD640`) | **item class `0xA`** entries | 4 refs |
| **14** | `02EBF070` | `InventoryBundleClass09_ApplyGilAndNestedItems` (`002FD530`) | **item class `0x9`** entries | 4 refs |

## 5c. The other eleven are not unnamed — they have no *specialised* consumer

Classes 5, 7, 9, 12, 13, 16, 17, 21, 24, 27 and 28 have no named referrer, and following their
anonymous ones explains why: **they are all referenced by the same two functions and nothing else.**

| function | what it is | reach |
|---|---|---|
| `FUN_00236C30` (1,037 B) | calls **`AreaData_BindAndRebaseSectionDescriptor` (`003845F0`) 33 times** — the authored-table loader | **36 distinct descriptors** |
| `FUN_0031C5D0` (8,136 B) | calls `ImageAddress_ResolveRuntimePointer` (`0020E600`) **168 times**, `BattleEncodedId_IsValidForClass` (`00322C50`) **26 times**, plus the `BattleEncodedId_DispatchQuery*` family — a **generic per-class query** | **26 distinct descriptors** |

> **So the eleven are bound by the loader and reachable through the generic query path, and no
> specialised code consumes them.** The fourteen in §5b have those two referrers *as well* — what
> makes them nameable is the specialised consumers they have in addition. **"No named referrer" was a
> statement about this database's naming, not about the engine; the engine's answer is "generic
> access only".**

**Class 12 (`02EBF0D0`) has neither.** Its descriptor is referenced by **the validator alone** — the
loader does not bind it and the generic query does not reach it. Of the 32 classes it is the only one
with no consumer of any kind — `02EBF0D0`.

The loader is the caller that
[`authored-data-table-registry.md`](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
records as populating the slots at area load; **this document reaches the same function from the class
side**, which is why the two were never linked.

> **Three of the classes line up with the item-id top nibble.** Classes 14, 15 and 18 are read by
> `InventoryBundleClass09_ApplyGilAndNestedItems`, `…Class0A` and `…Class0D` respectively — so the encoded-id class space and
> the item-category nibble of
> [`item-id-encoding-and-equipment-compatibility.md`](../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md)
> **meet here**. That is a correspondence across two numbering schemes and is **not** an identity: no
> code was read that converts one into the other.

**These names are inferences from referrer names, not decodes of table contents.** The referrer sets
are tier-1 measurements; the *reading* in each row is what those referrers imply. A row with one
named referrer is weaker than a row with fifty, which is why the count is shown.

## 6. Key addresses

| Address | Role |
|---|---|
| `00322C50` | `BattleEncodedId_IsValidForClass` |
| `00323054` | the 32-entry jump table, indexed by `class − 1` |
| `00309440` | class 1's id → class derivation: descriptor `[01EEBCC0 + (id >> 12) × 0x58].+0x38` = 5 + nibble (§10) |
| `02EBF038`–`02EBF150` | the descriptor globals; count at `+4` |

**The registry's code sits inside the Gameplay layer, and the layer uses it both ways**
(16 edges): `00322C50` itself is Gameplay-owned — called by `0031B9F0`/`0031C5D0` and called
*from* `00301AD0`, ~~`00309440`,~~ `00323910`, `00327CB0` *(corrected 2026-10-02, OPUS: `00309440` runs the other way: `00322C50+0x31` calls it, and its 30 bytes call nothing)*; `00301AD0` additionally calls
`00309EC0`, `0031EA90`, `00316CF0`, `00321320`; `0030E360` calls `003299B0`/`00307D10`; and
`0023A570`/`002FEF30` call `00322C50`/`00307D10`. The class registry is not a runtime-isolated
table — it is queried by, and its validator itself belongs to, gameplay code.

The remaining crossings are the same shape at lower volume: **rewards**/economy on 8 edges
(`002FD530` → `00254EE0`/`00253690`; `0030C650` is called by `0030C470`/`00312280` and calls
`002F9A60`/`002F9BD0`/`002F9B20`; `0030E360` → `00312280` — economy code resolves encoded ids
through the same descriptors); **audio** on 2 (`0030C650` → `003A1180`/`002DF220`);
**movement** on 2 (`00322C50` ← `0031BAC0`/`00326BB0`); **spawn**-lifecycle on 2
(`0023A570` ← `0023A3B0`, `0023A570` → `00236100`); **presentation** on 1 (`00301AD0` →
`00322360`); **RNG** on 1 (`003851F0` → `00379CD0`).

## Call chain (SWE2-CONTRACT, 2026-09-30)

```
area load: 00236C30 binds the battle_pack.bin sections into the descriptor slots 02EBF038..02EBF150
           (four slots come from other loaders; UQ-80's slot table)
registry:  01EEBCC0, fifteen 0x58-byte nibble records; 0030B6A0 rebases their pointers and prefix sums
             (the query record page, OV-9 accepted)
 -> 71 caller functions (Tools/work/graph/edges.tsv), among them the generic query 0031C5D0 (26 calls),
    AiOrder_EvaluateTargetSelector 00301AD0, BattleUnit_ApplyUnitDefinition 0023A570,
    BattleStats_RebuildEffectiveStatsAndAffinityState 002FEF30, the licence node setter 00323910,
    the gambit preset loader 00327CB0
    -> BattleEncodedId_IsValidForClass 00322C50 (class, id)         <- THIS SYSTEM (the owner transition)
         class - 1 > 0x1F -> fail
         jump table 00323054 -> the class's arm
           class 1: 00309440 derives class = nibble + 5, re-enters the switch
           classes 19, 22, 23: compiled-in bounds; the rest: descriptor count at +4
         shared tail 0032302C: lo <= id <= lo + count - 1 -> 1, else 0
    -> the caller indexes the descriptor's rows, or the generic query fills a query record
```

**Upstream (who causes this):** any code about to use an encoded id as a table index; the class is chosen by the
caller, and class 1 means "derive it from the id".

**Downstream (what this causes):** nothing on its own — it is a leaf that returns 0 or 1 (the validator and `00309440`
are leaf code, EXP-143). The consequence is the caller's: an id that fails is not used.

**Do not confuse with:** the query filler `0031C5D0`, which can refuse an id the validator accepts (class 12, the
SECTION-05 note above), and the mode dispatcher `00309EC0`, which routes by nibble to a record's ~~mutate or query~~ query
handler *(corrected 2026-10-02, OPUS: it always tail-jumps the row's `+0x50` handler with `edx = 0`, `00309EC0+0x51`–`+0x60`; no mutate path)* rather than validating against a class.

## Modding notes (SWE2-CONTRACT, 2026-09-30)

- **Best intervention point:** the `st2e` count of the authored table. Table classes validate against the count at
  the descriptor's `+4`, so rows added to a `battle_pack.bin` table become valid ids when the count covers them (§2,
  §9's shared tail).
- **Cannot be changed by data:** class 19 (`0xE000`–`0xEFFE`), class 22 (0–3) and class 23 (0–8) are bounds in the
  instructions (§4). Class 13 sums four counts, so a mod that fills the empty fourth key-item table extends class 13
  (§10). Ids at or above the nibble record's own count `+0x3C` still fail the mode dispatcher `00309EC0`.
- **Regenerates itself:** the descriptor pointers are rebound at every area load by `00236C30`, and the registry's
  resolved pointers and prefix sums are recomputed by `0030B6A0` (the query record page §2), so writing them directly
  does not persist.
- **Multiplayer / XIIOnline:** the ids are authored-data identity. Two clients agree on validity only if they load the
  same `battle_pack.bin`.
- **Mod compatibility:** table mods that change a count change validity for every caller of the class at once; there
  is no per-caller bound.

## 7. What is not known

- ~~**What the eleven generic-access-only classes hold** (section 5c). They are bound and queried, so
  they are live data; nothing specialised reads them, so nothing names them.~~ **Named 2026-09-11
  from their tables (§10)** — ten of the eleven; class 16 stays unnamed.
- **Why class 12 exists at all**, given that not even the loader binds it.
  *Answered at the mechanism level (2026-09-30, SWE2-CONTRACT, cited from existing evidence):* the classes 5–19 are
  generated from the fifteen `0x58`-byte nibble records at `01EEBCC0` (class = nibble + 5, §9 below), so class 12
  exists because nibble `7` exists. That record ships empty: count `+0x3C` = 0 and a null mutate handler (§9's note on
  nibbles 5, 7 and B). Its descriptor slot `02EBF0D0` has exactly one reference in `.text`, the validator's own read at
  `00322DFE`, and no copy as data, so nothing binds it and the validator refuses `0x7000`/`0x7001` over the null
  (control `C12_class12_slot_has_no_writer_in_the_image`,
  [s04-opus-replay-validator-shipped](../_index/candidates/s04-opus-replay-validator-shipped/README.md)). The query
  filler returns −2 for class 12 without reading either input lane (`0031C650`,
  [the query record](the-query-record-from-initialization-to-reuse.md) §3/§4, OV-9 accepted). So class 12 is a
  reserved id kind with no table in the shipped image. Tier 1.
- **What any descriptor's rows actually contain.** Section 5b names tables by their consumers; **no
  table's row layout is decoded here.** *Narrowed 2026-09-11:* every row word the query filler
  copies, per class, is listed on the encoded-id space page (§10); the layouts are still partial.
  *Carried by UQ-80, SUPERSEDED under FRONTIER's class-1 ruling (2026-09-30 pointer, SWE2-CONTRACT):*
  `uq80_coverage.py` measures all 23 `st2e` tables of the shipped `battle_pack.bin` field by field. 15 are fully
  mapped, and the residue of 60 unmapped bytes in 8 tables is printed offset by offset in `uq80_manifest.tsv`
  ([record](../_index/candidates/uq80-table-field-coverage/README.md);
  [the authored-data table registry](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md) UQ-80). The four
  class slots that are not pack entries (`02EBF150`, `02EBF120`, `02EBF0D8`, `02EBF0D0`) are named there and not
  measured. Typed rows: `StatusDefinitionRecord` (class 26), `EquipmentDefinitionRecord` (class 6) and
  `LicenseNodeRecord` (class 25) in `_types/types.tsv`.
- ~~**What `FUN_00309440` uses to derive a class** from an id (30 bytes, unread).~~ **Read 2026-09-11 (§10):** `id >> 12` indexes the inventory class descriptors at `01EEBCC0`; the class is the record's `+0x38`, 5 + nibble.
- **Why classes 30, 31 and 32 alias other arms** rather than having their own.
  *Answered at the mechanism level (2026-09-30, SWE2-CONTRACT, cited):* they have no tables of their own. The slot map
  binds `02EBF068` (`questreward_data`) to classes 15, 30 and 31 and `02EBF038` (`license_data`) to classes 25 and 32
  ([the authored-data table registry](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md), UQ-80's
  slot table), and the validator only needs a table's count, so one arm serves every class over one table. The classes
  can be distinct in the query filler instead: class 32 adds the record's `BYTE +0x36` and does not assign its
  description at `+0x10` ([the query record](the-query-record-from-initialization-to-reuse.md) §6). They are extra
  query views over existing tables. Tier 1.
- **Whether every class is reached in practice.** This is the validator's own table; it says which
  classes *exist*, not which are *used*. What is already known: class 12 has no table (above), class 16 is bound
  and validated but consumed by nothing (FY-2, answered as a negative), and EXP-143 executes all 32 arms in
  isolation, which shows they run, not that a shipped caller reaches them.
  *The call-site half is measured (OPUS, 2026-09-30, static; record
  [`rc1-static-census-0930`](../_index/candidates/rc1-static-census-0930/README.md), `rc1_census.py`):* a raw `E8`/`E9`
  index finds 110 call or tail-jump sites to `00322C50` in the same 71 functions. 84 pass a constant class, naming
  eleven classes directly: 1, 2, 6, 10, 11, 18, 20, 21, 23, 25 and 29 (class 10 once more on `00327CDF`'s only path).
  The other 26 are one per arm of the query-record dispatcher `0031C5D0`, which validates the record's own class
  (`mov ecx, [rbx]`) through its 32-entry jump table at `0031E598`; classes 4, 22 and 23 share an arm, and 15, 30 and
  31 share another. Class 1 is resolved through `00309440` and re-dispatched, and class 12's arm has no validator
  call, which agrees with "class 12 has no table". Tier 1. So every other class reaches the validator only through a
  query record, and which classes those records carry is the remaining question.
  *The record half is measured too (OPUS, 2026-09-30, static, the same record's "second half";
  `rc1_records.py`, `rc1_census.py`):* through the dispatcher's 17 direct callers and the 159 + 15 callers of the
  record-building wrappers `0035D330` / `0035D380`, **code names 25 classes**: 1, 2, 3, 5–11, 13, 14, 17, 18, 20, 21,
  23–26 and 28–32. The mapper `003933B0` (table `00D113B8`) can also request class 12, which has no table. **Never named
  by any path read: 4, 15, 16, 19, 22 and 27** — 16 is consumed by nothing (FY-2), and 15 and 19 lie in class 1's
  derived range (`00309440` maps a nibble to classes 5–19). Tier 1.
- [x] **RC-1.** Which classes a shipped caller passes to the validator.
  **ANSWERED 2026-09-30 (SWE2-CONTRACT, on OPUS's static census, record
  [`rc1-static-census-0930`](../_index/candidates/rc1-static-census-0930/README.md), commit `fe5dec46e`):** every remaining
  source was read to its end — `002CFEE0` / `002D0100` pass class 1, `002C38B0` / `002C4720` class 2, `0057DAD0`'s
  six sites classes 5, 7 and 13, `0035E070` class 1, and the six MULTI sites resolve path by path — and the four entry
  points (`00322C50`, `0031C5D0`, `0035D330`, `0035D380`) have no 8-byte pointer anywhere in the image and no RVA
  reference but their own `.pdata` entries, the scan's positive control. **Code names 26 classes: 1–3, 5–14 (12 is
  requested through the table `00D113B8` and has no table), 17, 18, 20, 21, 23–26 and 28–32. Classes 15 and 19 arise
  only through class 1's derivation (`00309440`). Classes 4, 16, 22 and 27 are passed by no caller in the image** —
  their validator and dispatcher arms exist and run in isolation (EXP-143), but no code path supplies them; 16 agrees
  with FY-2. Tier 1. *Limit, not an open question of this page:* which of the named call sites a given session runs is
  not claimed; before any part of that goes to ASTRA it has to name the site and the fact static evidence cannot
  settle.

## 10. Extension 2026-09-11 — the eleven named from their tables, and what `FUN_00309440` reads (FABLE)

[The encoded-id space page](the-encoded-id-space-and-the-query-record.md) reads the two things
this document could not: **`FUN_00309440`** indexes a fifteen-record table at `01EEBCC0` by
`id >> 12` and returns record `+0x38`, which holds classes 5 … 19 in order — so class 1's dynamic
arm computes **class = nibble + 5**, and the item-category nibble of §5c's "correspondence" is this
class number by construction. And the query-record filler `FUN_0031C5D0` names, for twenty-one
arms, which row word is the class's *name*; resolving that word through the text banks in the `us`
`battle_pack.bin` names the tables themselves:

| class | descriptor | rows × stride | what the names say |
|---:|---|---|---|
| 5 | `02EBF100` | 64 × 12 | **items** — Potion, Hi-Potion … Knot of Rust |
| 7 | `02EBF098` | 512 × 10 | **loot** — Teleport Stone … Empty Bottle (a packed-count class) |
| 8 | `02EBF0F0` | 81 × 8 | **magicks** — Cure … Graviga |
| 9 | `02EBF0E8` | 24 × 8 | **technicks** — First Aid … Gil Toss |
| 13 | `02EBF090` / `02EBF088` / `02EBF080` / `02EBF078` | 64 / 32 / 416 / **0** × 10 | **key items** in ~~three~~ **four** sub-tables (`0x8000`, `0x8040`, `0x8060`, `0x8200`) — area maps, area names, objects, and a fourth that ships **empty** (corrected 2026-09-12, `OPUS-CONTRA-CLASS13-FOURTH-TABLE`; see below the table) |
| 17 | `02EBF0C8` | 32 × 8 | **quickenings** — Red Spiral, White Whorl, Pyroclasm … |
| 21 | `02EBF128` | 21 × 4 | **the battle command list** — Attack, Magicks, Technicks, Items … Mist |
| 24 | `02EBF110` | 5 × 4 | **magick schools** — White, Black, Time, Green, Arcane |
| 27 | `02EBF050` | 8 × 2 | **elements** — Fire, Lightning, Ice, Earth, Water, Wind, Holy, Dark |
| 28 | `02EBF0B0` | 32 × 4 | **equipment categories** — Unarmed, Sword (1H) … Incendiaries |
| 29 | `02EBF040` | 129 × 8 | **the augment table** (bank 10 holds its texts: [the encoded-id space page](the-encoded-id-space-and-the-query-record.md)'s row for class 29, name field `+0x02` resolved in bank 10; [battle text banks](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md)) |
| 14 | `02EBF070` | 512 × 12 | **reward packages** — `{gil, item, count, item, count}`, applied by its handler (that page §2.8) |
| 15 | `02EBF068` | 256 × 12 | **package selectors** — two triples of ids, rows 128–172 wrap the reward table |
| 16 | `02EBF060` | 128 × 4 | headers only — one `u32` per row, no handler, no name field. *Named by its authored file (2026-09-30 pointer, SWE2-CONTRACT):* `price_data`, `battle_pack.bin` directory `+0x74` ([the authored-data table registry](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md), UQ-80 slot table; `_index/candidates/ag2-slot-identity/ag2-slot-identity.tsv`). It is bound and validated but consumed by no gameplay code (FY-2, answered as a negative with class 15 as the positive control) |

**Class 13 has four sub-tables, and the fourth has no rows (corrected 2026-09-12).** The pack binder
`00236C30` binds consecutive `battle_pack.bin` sections into the key-item slots: header `+0x88` →
`02EBF090`, `+0x8C` → `02EBF088`, `+0x90` → `02EBF080`, **`+0x94` → `02EBF078`** (`00236EDA`), then
`+0x98` → the reward packages `02EBF070`. In the shipped `us` `battle_pack.bin` that fourth section
(index 36, offset `0x1FFA0`) is a well-formed `st2e` header of 40 bytes with **count 0, stride 10** —
the key-item stride — and no rows. `BattleEncodedId_IsValidForClass` sums all four counts into class
13's bound (`00322E28`–`00322E8A`), so the fourth contributes nothing today; its first id would be
`0x8200`. The image references `02EBF078` twice, the binder and the validator, so no filler or
consumer reads its rows. **Reading:** a key-item sub-table the authored data leaves empty, not a
different kind of table. Only the `us` pack was decoded; other language packs are not checked here.

The §5b readings hold: class 6 is equipment (557 rows behind a 420-id descriptor — the encoded-id space page's row
for class 6, `557 × 52` against ids `0x1000`–`0x11A3`), 18 the bazaar
goods, 20 the actions, 25 the licence nodes, 26 the statuses, 11 the gambit conditions, 10 the
gambit presets, 2 the party table. Class 12 still has no consumer and, in the descriptor table,
no count, region or handler — it is a hole in the nibble space (`0x7000`), like classes 10 and 16.
**Row layouts** are given there store by store for every class the filler copies from (§4 of that
page); the name-field offsets are: 2 `+0x30`, 3 `+0x08`, 5 `+0x08`, 6 `+0x02`, 7 `+0x06`, 8 `+0x04`,
9 `+0x04`, 11 `+0x14`, 13 `+0x08`, 17 `+0x00`, 18 `+0x00`, 20 `+0x34`, 21 `+0x02`, 24 `+0x02`,
25 `+0x00`, 26 `+0x00`, 27 `+0x00`, 28 `+0x02`, 29 `+0x02`.
## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 32 classes, indexed `class − 1` | `lea eax,[rcx-1]` / `cmp eax,0x1F` / `ja` at `00322C5A` | 1 |
| The jump table's address | `mov ecx,[rdi + rax*4 + 0x203054]` with `rdi = 0x120000` | 1 |
| Every class → descriptor row | all 32 table entries resolved and each arm's first rip-relative operand decoded | 1 |
| Class 1 re-enters the switch | `call 0x309440 ; dec eax ; cmp eax,0x1F ; jbe` back to the dispatch | 1 |
| Class 19 is a range | `mov edx,0xE000 ; mov ecx,0xEFFF` | 1 |
| Class 23's bound is the literal 9 | `mov ecx, 9` | 1 |
| The referrer set of each descriptor | one pass over every listed function, collecting rip-relative references | 1 |
| The eleven share exactly two referrers | the same pass, with the validator excluded; both referrers decoded for their call profile | 1 |
| Class 12 is referenced by the validator alone | the same pass; zero other referrers | 1 |
| Class 12 is a reserved id kind with no table (nibble 7 record count 0, null mutate handler; slot never bound; filler returns −2) | §9's registry read; control `C12_class12_slot_has_no_writer_in_the_image` (s04-opus-replay-validator-shipped); the query record page §3/§4 (OV-9 accepted) | 1 |
| Classes 30/31 and 32 share their table and therefore their validator arm; the filler still distinguishes class 32 | UQ-80's slot table (authored-data table registry); the query record page §6 | 1 |
| Class 16 is `price_data` | UQ-80 slot table, directory `+0x74`; ag2-slot-identity.tsv | 1 + 11 (authored data) |
| Class 13's shipped total is 512 in the `us` pack | §10's section read; [the encoded-id contract](CONTRACT-encoded-id-space-and-class-registry.md), the class-13 fourth range | 1 + 11 (authored data) |
| 71 functions call the validator | `Tools/work/graph/edges.tsv`, distinct callers of `00322C50` (re-counted 2026-09-30) | 1 |

**Address review flag — dispositioned.** `verify_doc_addresses` reports `00323054` as a `.text`
non-function address. **It is the jump table**, which sits in `.text` immediately after the
validator's last arm — the case the checker's own note names as legitimate. It is cited because it is
the datum this document is about.

**Controls.** The registry is read from the **validator**, not from call sites — so it is independent
of every document that recorded a class number, and the two agreements in §5 are corroborations
rather than restatements. The extraction takes each arm's **first** rip-relative operand; that is
correct for the 29 table arms, which load their descriptor first, and it is why the three arms in §4
appear as "no global read" rather than being silently misfiled.

## 9. Related

- [`license-check-what-the-board-actually-tests.md`](../12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md) — classes 1 and 20.
- [`active-party-reserve-and-the-moment-the-leader-changes.md`](../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) — class 23.
- [`the-five-parallel-slot-maps.md`](../11-Party/the-five-parallel-slot-maps.md) — the slot maps, validated through class 23.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

The jump table was decoded from the image, entry by entry, and every arm read to its join:

| | |
|---|---:|
| entries at `00323054`, target = `entry + 00120000` | **32** |
| descriptors this page lists that reproduce | **29 / 29** |
| distinct arm addresses | **29** (`00322EBB` → 15/30/31, `00322FCB` → 25/32) |

The dispatch is as described — `lea rdi, [rip - 0x202c6b]` resolves `rdi` to `00120000`, the table is
`rdi + 0x203054`, and `cmp eax, 0x1F / ja` admits classes 1–32.

### The shared tail is `lo ≤ id ≤ hi − 1`

Every arm converges on `0032302C`:

```asm
0032302C  mov edx, eax            ; lo := 0   (arms with a base jump to 0032302E instead)
0032302E  cmp ebx, edx / jl fail
00323036  lea eax, [rcx - 1]      ; hi - 1
00323039  cmp ebx, eax / jg fail
00323041  mov eax, 1 / ret
```

So a "bound" is a **count**, and the valid set is `[lo, lo + count)`. That is what makes class 19's
range off by one on this page: `ecx = 0xEFFF` yields `0xEFFE` as the last accepted id.

### The shipped class is the top nibble PLUS FIVE — validator and mapper views

> **⚠ Retraction, same day.** This section first ran under the heading *"the page never says
> so"*, and said the encoding was unstated. **That was wrong, and wrong about my own work.**
> [The encoded-id space page](the-encoded-id-space-and-the-query-record.md) §2.1 already states
> `class = nibble + 5`, derives `FUN_00309440` instruction by instruction, and gives the descriptor
> layout — and I audited that page myself in an earlier pass (`bf0d33b`). **The encoding below is
> not a discovery of this pass.** What this pass adds is the *independent* confirmation from the
> other side — the fifteen arms' id bases, which the registry's own dispatch carries — and the
> observation that **§3 of this page omits every id base** even though the sibling establishes the
> space. The original wording is left struck rather than deleted.

§4 calls class 1 "dynamic" and stops. `FUN_00309440`, the function it calls, is 30 bytes:

```asm
00309440  movzx eax, cx
00309443  shr   eax, 0xc          ; the id's TOP NIBBLE
00309446  cmp   eax, 0xe / ja     ; nibbles above 0xE are invalid
0030944B  imul  rcx, rax, 0x58    ; a 0x58-byte record per nibble
0030944F  lea   rax, [rip + 0x1be28a2]   ; -> 01EEBCF8
00309456  mov   eax, dword ptr [rcx + rax]   ; the class
```

**`01EEBCF8` is not the table.** The descriptor table begins at **`01EEBCC0`** and the class field
is at record **`+0x38`** — `01EEBCC0 + 0x38 = 01EEBCF8`, which is why the function can index with a
bare `nibble × 0x58`. ~~the record's first dword~~ **Corrected same day**; the full `0x58`-byte
layout, including `+0x3C` **id count**, `+0x40` cumulative id base, `+0x48` **mutate** handler and
`+0x50` **query** handler, is
[the encoded-id space page](the-encoded-id-space-and-the-query-record.md) §2.2.

Reading those fifteen records out of the image:

| nibble | `0` | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9` | `A` | `B` | `C` | `D` | `E` |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **class** | **5** | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | **19** |

**`class = (id >> 12) + 5`, for the fifteen classes 5–19.** And the arms agree independently — each
of those classes' arms carries the matching id base, in lockstep:

| class | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **id base** | `0` | `1000` | `2000` | `3000` | `4000` | `5000` | `6000` | `7000` | `8000` | `9000` | `A000` | `B000` | `C000` | `D000` | `E000` |

> **The id bases are this pass's contribution, not the mapping.** An encoded id is
> `(kind << 12) | index` and the kind is the class minus five — established on the sibling page. What
> the arms add is that **the validator itself carries the base for each of the fifteen**, which is an
> independent route to the same structure. **§3's registry gives none of it**: it lists a descriptor
> per class and leaves every id base unstated, so a reader of this page alone would take class 15's
> ids to start at 0 when they start at `0xA000`.

**And this page carries the rule in three of its own rows without stating it.** §5b names class 14
by `InventoryBundleClass09_ApplyGilAndNestedItems`, class 15 by `InventoryBundleClass0A_…`, and
class 18 "item class `0xD`" by `InventoryBundleClass0D_…`. Those nibbles are `9`, `A`, `D` — exactly
`class − 5`. The records agree: record `+0x48`, the **mutate handler**, holds `002FD530` for nibble
`9`, `002FD640` for `A` and `002FD780` for `D` — **the very three functions §5b names.**

*(Record `+0x3C` is the **id count**, not a guess: nibble `0xE` holds `0xFFF`, exactly class 19's
compiled-in span, and the sibling page derives the field from the rebaser. Nibbles `5`, `7` and `B`
— classes 10, 12 and 16 — hold **zero** there and a **null** mutate handler, which sits beside §5c's
finding that 12 and 16 have no specialised consumer and 12 none at all, without being offered as its
explanation.)*

### ⚠ Class 22 is a fourth arm without a table

§3 recorded class 22 as "*no global read*" and §4 counted **three** non-table arms. Class 22 is the
fourth, and it is the twin of the one §4 did document, sitting nine bytes before it:

```asm
00322FA6  mov ecx, 4 / xor eax, eax / jmp 0x32302c    ; class 22 -> ids 0..3
00322FAF  mov ecx, 9 / xor eax, eax / jmp 0x32302c    ; class 23 -> ids 0..8
```

### ⚠ Class 13 is four tables, not one

Its arm is 105 bytes where the others are 42, because it reads **four** descriptors' counts and sums
them before the bound check:

```asm
00322E28  mov rcx, [rip + 0x2b9c261]   ; 02EBF090   <- the only one this page lists
00322E44  mov rcx, [rip + 0x2b9c23d]   ; 02EBF088
00322E59  mov rcx, [rip + 0x2b9c220]   ; 02EBF080
00322E6E  mov rcx, [rip + 0x2b9c203]   ; 02EBF078
00322E80  lea ecx, [r9 + 0x8000] ; 00322E8A add ecx, eax   ; 0x8000 + c1 + c2 + c3 + c4
```

Each is NULL-guarded independently, so a missing table contributes zero rather than faulting. **The
total is a runtime sum and is not claimed here** — the four pointers are filled at load.
*The shipped value is now read (2026-09-30 pointer, SWE2-CONTRACT):* in the shipped `us` `battle_pack.bin` the four
counts are 64 + 32 + 416 + 0 = **512**, which equals the nibble-8 registry count `+0x3C = 0x200`, so ids at or above
`0x8200` never validate (§10's class-13 note; [the encoded-id contract](CONTRACT-encoded-id-space-and-class-registry.md), the class-13 fourth range). Other language packs are not checked.

> A census that takes the *first* global a function reads — which is how §3 was built, and how my own
> first pass reproduced it — sees one descriptor and stops. Reading the arm to its join is what shows
> the other three.

**Not claimed:** §5b's naming census and §5c's two-referrer argument were not re-derived. What each
descriptor *contains* is untouched; this pass read the validator, not the tables. Nothing was executed
or observed live.

*(Pass 22 live-graph completion, 2026-09-15: `00254EE0` and `00312280` call
`Platform_Online_Achievements` `00316A50`, and `00309EC0` is called by `00315E90` (3 edges) —
the id-space consumers include the achievement layer, which reads encoded ids to credit
progress.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Resource — SERVICE.** A cited function calls a 36-byte Resource helper.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT (53 edges, one fan-in).** All 53 edges are CombatFormula bodies calling `00379CD0` on this page: the five-byte thunk onto the CRT's Mersenne Twister ~~that this page documents~~ *(misattribution corrected 2026-09-30, SWE2-CONTRACT: this page cites the thunk only here; it is documented as `RNG_MT19937_NextU32_Thunk`, 66 callers, 53 in CombatFormula, in [which roll is on which generator](../21-RNG-And-Determinism/which-roll-is-on-which-generator.md))*. `BattleFormula_RollGuardParryMode` is the worked example - it reduces its draw modulo 100 against the threshold at `[02AEDFDC]`. The crossing is **one shared primitive with 53 callers**, not 53 separate relationships, and naming a single body would say less than the count does. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Script_VM_Native_Bridge — CLIENT.** `FUN_00354bf0`, owned by that layer, calls `00379CD0` on this page. That caller is a 57-byte scaled draw: the operand becomes a bound, a Mersenne draw is multiplied by it and the **high 32 bits taken**, which is a range reduction without a modulo; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (9 edges through 5 of this page's functions).** The UI layer reaches this page at `0031C5D0`, `00322360`, `00326BB0`, `00309EC0` and 1 more. `BattleMenu_BuildCommandEntryList` is the worked example, read in full - it is the command-list build, and the ceiling is in the first instruction: the menu kind is bounded at **`0x22`** into a jump table, after which `dword[+0x40]` is zeroed and `dword[+0x44]` set to `-1` before any entry is written; **2 of the 7 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — MECHANICAL (SWE2-EC7-36, 1 edge).** `00313F60` — the shared callee this page cites inside `0031BAC0` — is called by a body on the Input layer. Shared-helper fan-in; no input relationship to the class registry.
- **ActorEntity — CLIENT and SERVICE (44 edges).** 23 inbound (ActorEntity bodies `BattleGroup_RefreshFourActorDefinitions` (003266C0), `BattleUnit_ApplyUnitDefinition` (0023A570), `BattleUnit_ActivateAppliedDefinitionRuntime` (00233AD0) call page-cited `FieldData_GetActiveFieldRecordBit15` (00313F60), `BattleEncodedId_IsValidForClass` (00322C50), `ActorRuntime_GetClassNibble` (00263C20)); 21 outbound (page-cited `AiOrder_EvaluateTargetSelector` (00301AD0), `00326BB0`, `Spawn_ApplyScriptSelectedUnit` (0023A3B0) call ActorEntity bodies `Actor_GetWorldPosition` (00265020), `ActorWork_GetBattleUnit` (0031B760), `BattleUnit_GetBySlotIndex` (00236820)). Substantive edges include `SpawnKeep_ResolvePrimaryEntry` (00236100) is called by `BattleUnit_ApplyUnitDefinition` (0023A570); `Spawn_ApplyScriptSelectedUnit` (0023A3B0) calls `BattleUnit_ApplyUnitDefinition` (0023A570); `BattleUnit_ApplyUnitDefinition` (0023A570) is called by `BattleUnit_TeardownAndDespawn` (00300E40); `BattleUnit_ApplyUnitDefinition` (0023A570) is called by `BattleGroup_RefreshFourActorDefinitions` (003266C0); the remaining edges run through shared helpers the page cites.
- **CombatAI — CLIENT and SERVICE (37 edges).** 28 inbound (CombatAI bodies `AiOrder_EvaluateTargetSelector` (00301AD0), `AiOrder_EvaluateAndResolveActionTarget` (003014C0), `BattleEnmity_AdjustOtherRelevantCombatants` (00321B00) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `FieldData_GetActiveFieldRecordBit15` (00313F60), `BattleTargetBuffer_ResetPreservingFlag0` (00316CF0)); 9 outbound (page-cited `AiOrder_EvaluateTargetSelector` (00301AD0), `00236C30`, `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` (00327CB0) call CombatAI bodies `GambitTargetDefinition_BindAndBuildMenuLookup` (00238880), `BattleTarget_MatchesRelationMode` (0030BD00), `BattleEnmity_ReadForCombatantId` (003215C0)). Substantive edges include `00236C30` calls `GambitTargetDefinition_BindAndBuildMenuLookup` (00238880); `AiOrder_EvaluateTargetSelector` (00301AD0) is called by `AiOrder_EvaluateAndResolveActionTarget` (003014C0); `AiOrder_EvaluateTargetSelector` (00301AD0) calls `BattleTarget_MatchesRelationMode` (0030BD00); `AiOrder_EvaluateTargetSelector` (00301AD0) calls `BattleEnmity_ReadForCombatantId` (003215C0); the remaining edges run through shared helpers the page cites.
- **CombatAction — CLIENT and SERVICE (63 edges).** 51 inbound (CombatAction bodies `BattleAction_PrepareExecutionResources` (0030EF20), `BattleAction_RefundReservedExecutionResources` (00300280), `BattleUnit_AdvanceStandardActionState` (00304850) call page-cited `BattleUnit_DispatchActorPresentationEvent` (003299B0), `BattleEncodedId_IsValidForClass` (00322C50), `GameState_GetGil` (00253690)); 12 outbound (page-cited `AiOrder_EvaluateTargetSelector` (00301AD0), `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360), `00236C30` call CombatAction bodies `BattleAction_LookupPrimaryResourceGainFactorByHpDamage` (002FB6C0), `BattleTarget_HasLow16EligibilitySuppression` (0030B9B0), `00237FC0`). Substantive edges include `00236C30` calls `00237FC0`; `GameState_GetGil` (00253690) is called by `BattleAction_CheckExecutionResourceAvailability` (00303BD0); `GameState_GetGil` (00253690) is called by `BattleAction_ConsumeExecutionResources` (00305640); `GameState_GetGil` (00253690) is called by `BattleAction_PrepareExecutionResources` (0030EF20); the remaining edges run through shared helpers the page cites.
- **Items — SERVICE (1 edge).** 1 outbound (page-cited `00236C30` call Items bodies `00238660`). Substantive edges include `00236C30` calls `00238660`.
- **Items_Equipment_Shops_License — CLIENT and SERVICE (60 edges).** 47 inbound (Items_Equipment_Shops_License bodies `Shop_CommitPurchaseItemAndGil` (002FEEB0), `InventoryBundleClass09_ApplyGilAndNestedItems` (002FD530), `Shop_CommitSaleItemAndGil` (00310870) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (003008A0), `GameState_GetGil` (00253690)); 13 outbound (page-cited `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` (0030A4E0), `BattleStats_SetLicenseNodeStateAndApplySideEffects` (00323910), `Equipment_SelectPreferredCandidateByAuthoredStats` (002F7A10) call Items_Equipment_Shops_License bodies `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (003008A0), `Equipment_ComputeComparisonMetricWithCompatiblePartner` (002F7C80), `Inventory_QueryEncodedItemStateByClass` (00309F30)). Substantive edges include `GameState_GetGil` (00253690) is called by `Shop_CommitPurchaseItemAndGil` (002FEEB0); `GameState_GetGil` (00253690) is called by `InventoryBundleClass09_ApplyGilAndNestedItems` (002FD530); `GameState_GetGil` (00253690) is called by `Shop_CommitSaleItemAndGil` (00310870); `GameState_GetGil` (00253690) is called by `InventoryEncodedGilClass0E_ApplyGilDelta` (002FD880); the remaining edges run through shared helpers the page cites.
- **Party — CLIENT and SERVICE (19 edges).** 12 inbound (Party bodies `0031AC00`, `PartyControl_RecomputeSuppressionFromLeaderBattleState` (0023B040), `PartyConfiguration_CollectSelectorsOutside07To25` (00320800) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `FieldData_GetActiveFieldRecordBit15` (00313F60), `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` (00327CB0)); 7 outbound (page-cited `AiOrder_EvaluateTargetSelector` (00301AD0), `003272F0`, `0031BAC0` call Party bodies `PartyFocus_GetCurrentPackedActorHandle` (003590D0), `PartyFocus_IsCurrentPackedActorHandle` (003273B0), `BattleUnit_GetPartyLeader` (003272A0)). Substantive edges include `AiOrder_EvaluateTargetSelector` (00301AD0) calls `PartyFocus_IsCurrentPackedActorHandle` (003273B0); `0031BAC0` calls `003272F0`; `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` (00327CB0) is called by `00328BD0`; the remaining edges run through shared helpers the page cites.
- **PlatformOnlineAchievements — CLIENT and SERVICE (17 edges).** 3 inbound (PlatformOnlineAchievements bodies `00315E90`, `00316A50`, `00316930` call page-cited `00315E90`, `BattleEncodedId_DispatchQueryMode0Value` (00309EC0)); 14 outbound (page-cited `00315E90`, `00316A50`, `GameState_SetGil` (00254EE0) call PlatformOnlineAchievements bodies `00316A50`, `003165C0`, `008632B0`). Substantive edges include `GameState_SetGil` (00254EE0) calls `00316A50`; `BattleEncodedId_DispatchQueryMode0Value` (00309EC0) is called by `00315E90`; `00315E90` is called by `00316A50`; `00315E90` is called by `00316930`; the remaining edges run through shared helpers the page cites.
- **Status_Periodic_Terminal — CLIENT and SERVICE (38 edges).** 28 inbound (Status_Periodic_Terminal bodies `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360), `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0), `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` (00386860) call page-cited `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360), `BattleStats_FindOwningBattleUnit` (0031B860), `BattleEncodedId_IsValidForClass` (00322C50)); 10 outbound (page-cited `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360), `0030C470`, `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (0030C650) call Status_Periodic_Terminal bodies `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0), `BattleStats_RemoveStatusesFromMaskAndRecompute` (0030F690), `BattleUnit_RecoverFromTerminalStatusSetIfClear` (00301140)). Substantive edges include `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30) is called by `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0); `0030C470` calls `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0); `0030C470` calls `BattleStats_RemoveStatusesFromMaskAndRecompute` (0030F690); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (0030C650) calls `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0); the remaining edges run through shared helpers the page cites.
- **World — CLIENT and SERVICE (3 edges).** 2 inbound (World bodies `003847B0`, `00238640` call page-cited `AreaData_BindAndRebaseSectionDescriptor` (003845F0)); 1 outbound (page-cited `00236C30` call World bodies `003847B0`). Substantive edges include `00236C30` calls `003847B0`; the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT and SERVICE (21 edges).** 9 inbound (WorldAreaField bodies `00238850`, `AreaArd_BindLoadedRootAndBattleSections` (003EA710), `AreaArd_LoadOrUnloadFieldResource` (003EA820) call page-cited `BattleData_SetAreaArdSectionCategory` (0023A160), `RNG_MT19937_NextU32_Thunk` (00379CD0), `AreaData_BindAndRebaseSectionDescriptor` (003845F0)); 12 outbound (page-cited `00236C30`, `BattleData_SetAreaArdSectionCategory` (0023A160), `AiOrder_EvaluateTargetSelector` (00301AD0) call WorldAreaField bodies `FieldData_GetActiveFieldRecordBit15` (00377C20), `003846F0`, `AreaData_BindAndRebaseSectionDescriptor` (003845F0)). Substantive edges include `00236C30` is called by `00238850`; `00236C30` calls `003846F0`; `BattleData_SetAreaArdSectionCategory` (0023A160) is called by `AreaArd_BindLoadedRootAndBattleSections` (003EA710); `BattleData_SetAreaArdSectionCategory` (0023A160) is called by `AreaArd_LoadOrUnloadFieldResource` (003EA820); the remaining edges run through shared helpers the page cites.
- **PlatformOnlineAchievements — CLIENT and SERVICE (17 edges).** 3 inbound (PlatformOnlineAchievements bodies `00315E90`, `00316A50`, `00316930` call page-cited `00315E90`, `BattleEncodedId_DispatchQueryMode0Value` (00309EC0)); 14 outbound (page-cited `00315E90`, `00316A50`, `GameState_SetGil` (00254EE0) call PlatformOnlineAchievements bodies `00316A50`, `003165C0`, `008632B0`). Substantive edges include `GameState_SetGil` (00254EE0) calls `00316A50`; `BattleEncodedId_DispatchQueryMode0Value` (00309EC0) is called by `00315E90`; `00315E90` is called by `00316A50`; `00315E90` is called by `00316930`; the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — CLIENT (1 edge).** 1 inbound (Save_Load_Settings bodies `SaveRuntime_RebindImageBackedGameplayState` (00238A80) call page-cited `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (0030B6A0)).
## The `002FEF30` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`002FEF30` `BattleStats_RebuildEffectiveStatsAndAffinityState` — the
derived-stats rebuild; `(rcx = unit, rdx = out stats, r8 = equipment
record)` per its `0030A4E0` call site (`0030A6B7`). The page's table-4
row names it as the `02EBF150` unit-definition-table accessor.

| member | role | interior |
| --- | --- | --- |
| `002F8E50` (30 B) | scaled-percent helper — `imul r8d, ecx; imul r8d, edx` over `inc r8d`, then the `0x51EB851F` signed magic divide → `ecx*edx*(r8+1) / 100` (`002F8E53`–`002F8E6D`) | [`002F8E53`](../_index/ADDRESS-INDEX.md) |
| `002F9180` (21 B) | `ecx*edx / 100` signed-percent helper — same `0x51EB851F` divide (`002F9183`–`002F9194`) | [`002F9183`](../_index/ADDRESS-INDEX.md) |

Both members are the stat-scaling arithmetic the rebuild applies; the
`0031B860`/`00263C20`/`02EBF138` work seen nearby belongs to siblings
`002F8E70`, `002F8E90`, `002F91A0` and `002F9240`
`BattleAction_ComputeCasterPrimaryResourceGainFromHpDamage`, not to
these bodies. Shared callees outside the census: none — the members are
leaf arithmetic.

## The `003008A0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`003008A0` (`Inventory_ModifyEncodedItemAndUpdateDiscoveryState`, ~124 B)
— `eax = 0xFFFF`, `r14d = r9d` under a five-register save
(`003008AF`/`003008B4`).

| member | role | interior |
| --- | --- | --- |
| `00309F30` | `cx == 0xFFFF` guard + `movzx` index (`00309F30`/`00309F3C`) | [`00309F30`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `003851F0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`003851F0` (`BattleFormula_BuildCandidateStatusMask`, ~542 B) —
`r9 = [02EBF138]` battle-record bank (`003851F9`).

| member | role | interior |
| --- | --- | --- |
| `00384C30` | same `02EBF138` base — sibling formula helper (`00384C3F`) | [`00384C3F`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.


### Interior citation — frontier hub `00309EC0` (2026-09-18, SWE2-EC7)

`00309EC0` — 102 B, 14 callers, `BattleEncodedId_DispatchQueryMode0…`. The
encoded-id class dispatch the registry names: `cx == 0xFFFF` or
`(cx & 0xF000) > 0xE000` return `-1`; the class nibble `cx >> 12` selects a
0x58-stride row in the `01EEBCC0` table, `cx & 0xFFF` is bounds-checked against
`[row+0x3C]`, and on success `jmp qword[row+0x50]`
([`00309F20`](../_index/ADDRESS-INDEX.md)) tail-dispatches the row's mode-0
handler with `(edx=0, ecx=cx)`. Out-of-range ids return 0.

## SWE2-EC7-25 update (2026-09-18) — `0031C500` masked property test

`0031C500` (49 B) null-guards both args, calls `003872D0(rcx, rdx, 0)`,
and ANDs the result with `[rdx+0x64] | [rdx+0x3C]` — the masked
property check `00301AD0` and the command-lifecycle callers run.
Interior anchor `0031C516` (the `003872D0` call).

## SWE2-EC7-36 update (2026-09-19) - `0031BAC0`

`0031BAC0` (668 B) is an id-class registry body - `00D10820`-`00D10840` rdata run, `00322C50` pair plus `003272F0`/`00325E60`/`00313F60`/`00808C40`. Interior anchor `0031BBA0` (an `00322C50` call).

## SWE2-EC7-74 update (2026-09-19) - `00323890` mode-to-enum jump table measured

`00323890` (83 B) is the class-map decoder: `003241D0()` minus `0x15`
indexes a 9-entry jump table at `002038E4` returning 0/1/2/3; outside
the range returns -1 - the mode-to-class fold the registry callers
share.
Interior anchor `003238B4` (the `jmp rcx` dispatch).
