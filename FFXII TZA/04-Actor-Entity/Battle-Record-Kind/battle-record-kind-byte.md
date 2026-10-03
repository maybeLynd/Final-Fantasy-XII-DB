---
system: Battle record kind byte
category: 04-Actor-Entity
status: DOCUMENTED — what the kind byte means answered 2026-09-10 (AL-1: which of the two definition tables the unit was built from, 0 party, 1 enemy); the record's map (AL-8, evidence tracked 2026-10-01) and the +0x000 flag byte and its bits (AL-9, AL-10) answered; what each free-target type value denotes as authored (§7) answered 2026-09-30 (GR-2) and narrowed under SWE2-AUDIT-SEM's review (six writers; 1 hostile combatant, 3 allied or event combatant, 4 interactable object, 5 non-combatant, 6 three boss-fight scripts' value; no writer produces 2) (owner re-status 2026-10-01, OPUS)
owner_layer: none — tested across eleven subsystems, owned by none of them
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
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-30
audit:
  passes: 4
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
---

# Battle record kind byte

> One byte at `+5` of every battle record, tested at **104 sites across 82 functions in eleven
> subsystems** — and the obvious explanation for it is wrong.

~~**PARTIAL — deliberately.**~~ **DOCUMENTED.** *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`, and the note below records GR-2 answered)* The census is exact and the two code paths it selects are read. ~~**What
the byte means is not established**, and~~ the reading that first suggests itself is contradicted by
the evidence. This document records the fact and refuses the story.

*Corrected 2026-09-30 (FABLE): the byte's meaning was established on 2026-09-10 (`AL-1`, §2's corrected block,
§7). It is the high byte of the unit's definition id: the table the unit was built from, 0 the party table and 1 the
enemy table. ~~The page stays PARTIAL for the residue in §7 (`GR-2`), not for the meaning.~~ GR-2 is answered (§7) and the page is DOCUMENTED (2026-10-01, OPUS).*

## 1. What the player sees

Nothing directly. But almost everything that distinguishes *one unit from another* passes through
this byte: whether a defeat pays experience and licence points, whether loot drops, whether the enemy
chain advances, how enmity propagates, whether a formation slot is solved, and what the battle menu
offers.

It is worth documenting precisely because it is a **single byte the whole battle system consults**,
and because getting its meaning wrong would quietly corrupt any reasoning built on top of it.

## 2. Native mechanism

### The field

```
BattleUnit + 0x6A0   ->  per-unit battle record            (0x250 = 592 bytes)
BattleUnit + 0x698   ->  the same record + 0x80            ("raw", the access path 82 readers use)
                          +5   byte   the kind selector    = record byte +0x85
```

> ### CORRECTED 2026-09-10 — `+0x698` points at one record *type* whose storage depends on the definition kind, and the kind byte is the id's class byte
>
> *Observed live 2026-09-13 ([EXP-081](../../_experiments/EXP-081-live-battleunit-bindings.md), re-derived by FABLE from the raw spans): the party unit's `+0x698` is the block element `+8`, three spawned units' are their keep entries' `+0x80`, each record's kind byte matching its path (0 / 1); `+0xE68` is a class row on the spawned units and 0 on the party unit.*
>
> *Heading reworded 2026-09-13:* `+0x698` always points at a `BattleStatsRecord`, and **which record is fixed by the definition kind**: kind 0 (party) → the BattleSystemState element `*(02EBF190) + 8 + slot × 0x1C8`; kind 1 (spawn-backed) → the record embedded in that unit's own SpawnKeep entry at `+0x80` (`0x80 + 0x1C8 = 0x248 ≤ 0x250`). These are **different records belonging to different units**, not one record reachable from two places, and `+0xE68` is a third, unrelated object — the `.ard` slot-0 class row.
>
> The block above holds for **kind 1 only**. `BattleUnit_ApplyUnitDefinition` (`0023A570`) splits on
> the definition id's high byte at `0023A626`/`0023A62E`: **1** resolves the spawn record from the lane
> map (`0023A776 call 00236100`), keeps `record + 0x80` (`0023A787 sub rax, -0x80`) and stores it at
> `+0x698` ~~and `+0xE68`~~ (corrected 2026-09-12, FABLE: `+0xE68` takes the `.ard` slot-0 **class row**
> `r15` computed at `0023A6F0`–`0023A6FC`, [the unit-definition page](../Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.1), the record itself at `+0x6A0`; **0** stores `*(02EBF190) + 8 + index*0x1C8` —
> an element of the battle-state array — at `+0x698` and **NULL** at `+0x6A0`
> (`0023AAAA`–`0023AAC1`, `0023AAB1 xor ebp, ebp`; both paths converge on the stores at `0023ABFA` /
> `0023AC01`). Both homes are the same `0x1C8`-byte stats record type: `BattleStats_InitializeDefinitionRecord`
> (`0023AC80`) opens with `memset(page, 0, 0x1C8)` (`0023ACA4`, `0023ACBD`) and writes **the whole
> definition id into the page's `+4` word** (`0023AD8E`), so **the byte at `+5` is the id's high byte by
> construction**: `0` for the party table (`02EBF130`), `1` for the enemy table (`02EBF120`). That is
> the "two kinds, type-keyed and owner-keyed" of §2 and §3 with the meaning attached, and it answers
> `AL-1`. Raised as `OPUS-CONTRA-BU698` from `0031B770`'s equality test against the array element
> (`0031B7B1`), which this page's reading could not explain; resolved by reading the installer. The
> `0x80` relation, the 104-site census and §10–§11 stand for kind-1 units; §2's *"records live in an
> array at `*(0208E690)`"* is the kind-1 half only.

Records live in an array at `*(void **)0x0208E690`, indexed by a one-byte id resolved through a
spawn keep (section 11). **49 of its 72 observed fields carry no scalar store at their
displacement on the censused paths, and 23 do** — it is per-unit state initialised from a pool
slot, not a shared read-only definition (section 12). *("Never written" is refuted: at least six
of the forty-nine are written, section 12a. The conclusion here is unchanged and strengthened.)*

*(The `+0x698` view was named before its origin was traced; section 11 establishes that it is a
window into the authored definition, not a separate object.)*
*(Corrected 2026-09-30 (FABLE): §12 withdrew "authored definition". The kind-1 record is the stats block of the
unit's spawn-keep entry, and the kind-0 record is an element of the battle-state array (§2's corrected block,
`AL-8`).)*

### The census

Every function in the image was disassembled and every `cmp`/`test` against `record[5]` collected —
**but only where the register holding the record was provably loaded from `[X + 0x698]` within the
same function.** That filter matters: an unfiltered scan for `[reg+5]` also matches libvpx video
code and is meaningless.

| | |
|---|---:|
| comparison sites | **104** |
| distinct functions | **82** |
| subsystems | **11** |
| values compared against | **`1`, and only `1`** |

Owner spread: 27 unowned, Movement 15, CombatAI 14, CombatAction 12, ActorEntity 10, CombatFormula
10, Spawn/Encounter 7, Rewards 5, UI 2, Presentation 1, Party 1.

**The filter is conservative and under-counts.** Taint is dropped at every `call`, so a comparison
after an intervening call is missed even when it is genuine — `002FFDAE` in
`BattleAction_CheckActionAvailabilityReason` is exactly such a site, and it compares against **`0`**.
So the value domain is at least `{0, 1}`; what the census establishes is the **scale and spread** of
the `== 1` test, not that `1` is the only value ever compared.

### The two paths it selects

`FUN_002F8E90` (`002F8E90`, 131 B) branches on this byte to classify a unit, and the two branches do
structurally different things:

```c
kind = unit[5];
if (kind == 0)   return ((byte)(unit[4] - 0x1B) <= 0xC) ? 2 : 1;   /* keyed off a TYPE ID */
if (kind != 1)   return 0x10;
                                                                    /* kind == 1: */
owner = BattleStats_FindOwningBattleUnit(unit);                     /* keyed off an OWNER */
v = FUN_00263C20(owner ? owner[0x10] : 0);
if (v == 3)               return 4;
if (v - 1 <= 1 || v == 7) return 8;
return 0x10;
```

- **kind 0** is classified from a **type id** at `unit[4]`, tested against the contiguous range
  `0x1B .. 0x27` (13 values).
- **kind 1** is classified by **resolving an owning BattleUnit** and querying it.

That asymmetry — *type-keyed* versus *owner-keyed* — is the sharpest structural fact available about
the byte.

## 3. The reading that does not survive

The consumer names invite an immediate conclusion: `record[5] == 1` means **party-side**, `0` means
**foe-side**. Several names support it:

- `Reward_ComputeExperienceForRecipient`, `Reward_ComputeLicensePointsForRecipient` — a recipient of
  EXP and LP is a party member
- `PartyFollow_SolveFormation`, `PartyFollow_LookupDestination`
- `BattleUnit_HasNonPartyEngagementEvidence`

**But the same `== 1` test appears in functions that are unambiguously about enemies:**

- `SpawnGroup_TeardownAllGroupedSpawnUnits`, `SpawnGroup_SetUnitFlag800ByGroupMask`,
  `SpawnGroup_RecordMemberDeathAndHandleCompletion`
- `EnemyChain_UpdateOnDefeat`
- `Spawn_SetAllSpawnBackedUnitsCurrentHPZero`

A single value cannot mean "party" in one and "enemy" in the other. **The party/foe reading is
therefore not supported**, and this document does not adopt it.

What the evidence does support is weaker and less satisfying: `record[5]` distinguishes **two kinds
of battle record**, one identified by a type id and one identified by an owner. Whether that maps to
party/foe, to summoned/spawned, to persistent/transient, or to something else entirely ~~is **open**~~.

*Corrected 2026-09-30 (FABLE): answered (`AL-1`, 2026-09-10; §2's corrected block). The kinds map to the
**definition table** the unit was built from: `0` the party table `02EBF130`, `1` the enemy table `02EBF120`. The
type id is the party-table row (the thirteen Espers are rows `0x1B`–`0x27`, `AL-2`). The owner-keyed kind is the
enemy-table record embedded in a spawn-keep entry. The refutation above stands for what it refuted: `1` does not
mean "party".*

> **Sharpened 2026-09-02.** Section 10 shows the byte is **authored definition data**, installed with
> the record and never written afterwards. That explains the contradiction rather than resolving it:
> a *definition kind* can be shared by units that behave differently in play, so a reader-side census
> was never going to separate party from foe. The question is what the authoring distinguishes.

*(This is the second time in one day that a tempting reading was built from surrounding evidence
rather than from the mechanism — the first was a set of multiplier constants that looked elemental.
Function names are evidence about intent, not a definition.)*

## 4. Do not confuse this with actor class

The database already documents **a different class field**:
[`../battleunit-slot-pool-and-actor-class.md`](../battleunit-slot-pool-and-actor-class.md) describes
`actor->bActor_class_flags >> 5`, a **three-bit** class in the **actor** object, with values 1 and 3
controlling positioning and movement.

| | actor class | this byte |
|---|---|---|
| object | the **actor** | the **battle record** at `unit + 0x698` |
| location | top 3 bits of `bActor_class_flags` | whole byte at `+5` |
| known values | 1, 3 | 0, 1 |

They are different fields on different objects. Conflating them would be easy and wrong.

## 5. Key addresses

| Address | Role |
|---|---|
| `002F8E90` | branches on the byte; returns a one-hot category `1/2/4/8/0x10` |
| `0031B860` | `BattleStats_FindOwningBattleUnit` — the kind-1 resolution path |
| `00263C20` | the sub-query kind 1 feeds into |
| `002FFCF0` | `BattleAction_CheckActionAvailabilityReason` — gates on both `0` and `1` |
| `002F9820` | `BattleUnit_UsesGilActionCostChannel` — returns early when the byte is `1` |
| `00303BD0` | `BattleAction_CheckExecutionResourceAvailability` — its third pool is gated on `0` |
| `0023A570` | `BattleUnit_ApplyUnitDefinition` — installs the record and splits on the id's table byte (`0023A626`/`0023A62E`) |
| `0023AC80` | `BattleStats_InitializeDefinitionRecord` — stores the whole definition id into `+4` (`0023AD8E`): **the owner transition of the byte** (§5a; §12a's three-route sweep finds no other store to it) |
| `00237DF0` | `BattleSystem_ResetRuntimeState` — initialises the forty party-table records with ids `0`–`0x27`, so each has kind 0 |
| `00236100` | `SpawnKeep_ResolvePrimaryEntry` — finds the spawn-keep entry that holds a kind-1 record |
| `0031B760` | `ActorWork_GetBattleUnit` — the unit accessor most readers of the byte go through |
| `0031B770` | `BattleUnit_FindByCombatantId` — the combatant-id accessor |

## 5a. Call chain (FABLE, 2026-09-30)

*Added 2026-09-30 (FABLE). Call sites and counts come from the raw call index
(`Database/Tools/work/FABLE/pub140-scratch/tools/rawcalls.json`), and each named call site was read in its body.*

```
upstream: the byte is fixed once, when a stats record is initialised
  kind 1 (spawn-backed):
    Spawn_ApplyScriptSelectedUnit 0023A3B0 --call 0023A3F1--> BattleUnit_ApplyUnitDefinition 0023A570
        (0023A570 has 3 call sites in 3 functions; the other two are a despawn path and a
         four-actor group definition refresh)
      -> SpawnKeep_ResolvePrimaryEntry 00236100 (0023A776): entry = *(0208E690) + id * 0x250
      -> record = entry + 0x80 (0023A787); if the entry's flag byte has neither bit 0 nor bit 2
         (0023A791 test byte ptr [rbp], 5):
         BattleStats_InitializeDefinitionRecord 0023AC80 (call 0023A7A9, edx = the definition id)
           -> mov word ptr [rdi + 4], r15w (0023AD8E): +4 = row, +5 = table = 1     <- OWNER transition
      -> unit +0x698 = entry + 0x80 (0023ABFA), unit +0x6A0 = entry (0023AC01)
  kind 0 (party table):
    BattleSystem_ResetRuntimeState 00237DF0: for id = 0 .. 0x27,
        0023AC80(*(02EBF190) + 8 + id * 0x1C8, id)   (loop 00237E00-00237E30, call 00237E26)
        -> +5 = 0 on all forty party-table records                                 <- OWNER transition
    (0023AC80 has 3 call sites in 3 functions; the third is the area-state party walk)
    0023A570's kind-0 arm points unit +0x698 at that array element (0023AAAA-0023AAC1)

downstream: readers only; nothing writes the byte after install (section 10, AL-5)
  unit -> record accessors:
    ActorWork_GetBattleUnit 0031B760           72 call sites in 61 functions
    BattleUnit_FindByCombatantId 0031B770      16 call sites in 10 functions
    BattleStats_FindOwningBattleUnit 0031B860  136 call sites in 62 functions
  -> the 104 "== 1" comparisons in 82 functions (section 2)
  -> the classifier 002F8E90 (17 call sites in 11 functions): one-hot category 1/2/4/8/0x10
  -> BattleUnit_UsesGilActionCostChannel 002F9820, called by 00309060, 00309110 and the battle-menu builder
  -> BattleAction_CheckActionAvailabilityReason 002FFCF0 (7 call sites in 7 functions)
       -> BattleAction_CheckExecutionResourceAvailability 00303BD0 (call 002FFEB0, its only call site)
```

**Upstream (who causes this):** the owner transition is the one store at `0023AD8E`. Two things trigger it: a
battle runtime reset, which initialises every party-table record, and a script-selected or spawn-backed unit being
applied, which initialises the record embedded in its spawn-keep entry.

**Downstream (what this causes):** the classification, cost-channel and availability decisions above, and every
`== 1` test of §2. None of them writes the byte.

**Do not confuse with:** the actor class bits (§4), the actor's free-target nibble `00263C20` (`AL-3`), and the
`.ard` class row at unit `+0xE68` (`AL-7`).

## 6. Modding notes

- **Do not treat this byte as a side flag.** Section 3 shows why. Anything keyed on "is this an
  enemy" needs a different signal until this one is settled.
  *Updated 2026-09-30 (FABLE): it is settled (`AL-1`). The byte says which definition table built the unit: 0 the
  party table (including the guests and the Espers), 1 the enemy table. Whether that matches hostility in every
  battle is not claimed here. Hostility is what `BattleTarget_ClassifyRelationshipClass` (`0030AB40`) computes,
  and it reads the free-target type (`AL-3`).*
- **It is consulted very widely.** 82 functions across 11 subsystems test it, so changing it at
  runtime would alter rewards, spawning, enmity, formation and menu behaviour at once.
- **It is not the actor class field** — see section 4.
- **XIIOnline:** because rewards, loot and chain progression all branch on it, two clients that
  disagree about this byte for the same unit will disagree about payout. It is authored/derived
  state, not something to synchronise directly — synchronise whatever sets it.
  *(2026-09-30: what sets it is the unit's definition id, the `u16` that `0023AC80` stores at `+4`, §5a.)*

## 7. What is not known

- [x] **What the byte means.** ~~Two kinds are distinguished; the party/foe reading is refuted.~~
      **AL-1.** ANSWERED 2026-09-10: the high byte of the encoded definition id, written whole into the
      stats record's `+4` word by `BattleStats_InitializeDefinitionRecord` (`0023AD8E`); 0 = party table
      `02EBF130`, 1 = enemy table `02EBF120` (`0023A626`, `0023A62E`). See the CORRECTED block in §2.
- [x] ~~What `unit[4]`'s type ids `0x1B .. 0x27` enumerate — the 13-value range that classifies kind 0.~~
      **AL-2 ANSWERED 2026-09-11 (data):** they are **the thirteen Esper rows of the party table**.
      Registry slot `02EBF130` is `battle_pack.bin`'s directory entry at the blob's `+0x44`
      (`00236D99`–`00236DAB`): an `st2e` table of 40 rows × 128 bytes whose `+0x30` name references
      ([the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) §5)
      decode as rows 0–5 Vaan, Ashe, Fran, Balthier, Basch, Penelo; ~~6–16 the guests (Reks,~~ 6 Reks, inside the roster span *(corrected 2026-10-02, OPUS: `002F90EF cmp al, 6` / `002F90F1 jbe` accept row 6 with rows 0–5)*; 7–16 the guests (Amalia,
      three Basch variants, Lamont, two Vosslers, Larsa, two Reddases); 17–25 "No name"; 26 Chocobo;
      **27–39 (`0x1B`–`0x27`) Belias, Mateus, Adrammelech, Hashmal, Cúchulainn, Famfrit, Zalera,
      Shemhazai, Chaos, Zeromus, Exodus, Ultima, Zodiark**. So `FUN_002F8E90`'s class 2 is "an
      Esper", class 1 "any other party-table unit".
- [x] ~~What `FUN_00263C20` returns for kind 1, whose values `1, 2, 3, 7` select the categories
      `4`, `8` and `0x10`.~~ **AL-3 ANSWERED 2026-09-12 (FABLE): the actor's free-target type.**
      `ActorRuntime_GetClassNibble` (`00263C20`) is `actor[+0x0E] & 0xF` (0 for a null actor). Two
      writers give the nibble its authored names: the script verb **`setfreetargettype`** (`0x0265`,
      `003528C0`) pops an integer and stores it through `00269FE0(actor, v)` (`0026A033`–`0026A03B`;
      for a kind-3 actor `v == 4` also raises `+0x1C` bits 8 and 13, any other value clears them,
      `00269FFE`–`0026A02B`); and `BattleUnit_RefreshActorRuntimeFromDefinition` copies the unit's
      **runtime category mode** ([the battle-unit field map](../Battle-Unit/the-battle-unit-field-map.md) `+0x058`) into it at every refresh
      (`00238E0D`–`00238E3E`), that byte being what the verb **`btlAtelSetUnitType`** (`0x3005`,
      `00510340` → `BattleUnit_SetRuntimeUnitCategoryMode`) sets through the table `{1, 5, 3, 4}` at
      `01E09EE8` for arguments 0–3. The refresh adds two derived values: **4** when the spawn
      record's flag bit 5 is set (`00238D98`–`00238DA0`, `00267CC0`) and **7** when the definition is
      an enemy row whose byte `+0x03` carries bit 4 (`00238DEF`–`00238E02`); a mode of 4 without the
      spawn flag falls back to 1 (`00238DBD`–`00238DC3`). Before any unit binds them, records
      initialise to **4** (kind 1, `002663A3`) or **5** (kind 3, `002660D3`–`002660DE`) in
      `00265FF0`. What the readers make of the values: `BattleTarget_ClassifyRelationshipClass`
      returns 0 — neither friendly nor hostile — when either side is **5** (`0030AB93`–`0030ABA0`);
      the field cursor's helpers accept **1–2** (`00273750`), **1–3** (`002734F0`), **3** with
      `003229A0 == 0` (`00273910`) and **5** (`00273A00`); this page's `002F8E90` maps **3 → 4** and
      **1, 2, 7 → 8** for enemy-table units, which is why the loot thief message keys on 8. The
      per-value authored meaning beyond that use is not read. *(Narrowed 2026-09-30, FABLE, on SWE2-AUDIT-SEM's [review](../../_index/candidates/auditsem-review-dd-gameplay-0930/REVIEW.md) C3; record [`dd-gameplay-corrections-fable-0930`](../../_index/candidates/dd-gameplay-corrections-fable-0930/README.md))*: the census the row planned is done: SD-160's record decodes all 63,432 calls of both verbs, and every argument is a pushed constant - `btlAtelSetUnitType` 0 / 1 / 2 / 3 (59,814 / 234 / 297 / 369 sites), `setfreetargettype` 1 / 3 / 4 / 6 (18 / 315 / 2,340 / 45 sites) - and it joins value 3 to its scripts (allied third parties and event combatants). ~~Open:~~ *(answered: see `GR-2` below, 2026-09-30; 2026-10-02, OPUS)* joining the other values, including 6 (which no reader listed here tests), to the kinds of actor their scripts target ([SD-160's record](../../_index/candidates/sd160-free-target-type3-0930/README.md)). *(Registered 2026-09-30 (FABLE) as `GR-2`,
      below.)*
- [x] ~~The full value domain. The filtered census sees only `1`; a known `== 0` site is excluded by
      the filter's conservatism, and values above 1 have not been ruled out.~~ **AL-4 ANSWERED
      2026-09-12 (FABLE): `{0, 1}`, from the writer.** The byte is the high half of the `u16` at
      `+4` that `BattleStats_InitializeDefinitionRecord` stores (`0023AD8E mov word ptr [rdi + 4],
      r15w`, the id it was passed), and that store is reached only through the initializer's
      two-way switch on the id's high byte (`0023ACF3`–`0023ACFA`: `0` → the party arm, `1` → the
      enemy arm, anything else → `xor eax, eax` and return without the store, `0023ACEC`); the
      record was `memset` to zero first (`0023ACBD`), so a refused kind leaves `+5 = 0`, and the
      grower likewise diverts every kind but 0 and 1 to its epilogue (`0030C4A4`–`0030C4AB` →
      `0030C607`). Values above 1 are therefore unreachable in a stored record; the `0xFF` the
      rebuild uses is a local sentinel for a null record, never written to one.
- [x] ~~What writes the byte, and when.~~ **ANSWERED 2026-09-02** — **nothing** writes it through
      `unit + 0x698`. The record is installed by `BattleUnit_ApplyUnitDefinition` (`0023ABFA`) and
      `BattleUnit_ResetStateForReuse` (`00236AB4`); the byte is ~~**authored definition data**~~ definition data *(answered: see "CORRECTED: this is not a shared authored definition" — only the word "authored" was too strong; 2026-10-02, OPUS)*, set
      once. Section 10. **AL-5.**
- [x] ~~What the 16-bit field at `record + 4` identifies, of which `+4` is a type id and `+5` this
      kind. In definition terms this is the word at **`+0x84`**.~~ **AL-6 ANSWERED 2026-09-11:** it is
      the **definition selector** `BattleStats_InitializeDefinitionRecord` receives in `edx` and
      stores whole (`0023AC9E`, `0023AD8E`): the low byte is the **row index** into the selected table
      (`0023ACAA`, the multiplier of the row stride at `0023AD30`), the high byte the **table** — 0 the
      party table, 1 the enemy table (`0023ACB2`, `0023ACF3`–`0023ACFA`). A "type id" of `0x1B`–`0x27`
      is therefore a party-table row number, and the rows are the Espers (AL-2).
- [x] What the **592-byte per-unit battle record** contains. **MAPPED 2026-09-02** — 72 offsets,
      917 accesses, 49 with no scalar store at their displacement and 23 with one — **not**
      "never written", and at least six of the forty-nine are written (section 12a); full map in
      `Tools/work/rtti/unit_record_fields.tsv`. ~~What most individual fields *mean* is still open.~~ *(answered: see the note below — 69 of the 72 observed offsets have a name or meaning, and `FE-1` was answered 2026-09-26; 2026-10-02, OPUS)*
      **AL-8.** *ANSWERED 2026-09-18 (OPUS) by prior art, closed 2026-09-25 (FABLE, Claude Opus 5.5):* the 592-byte
      record is the SpawnKeep entry, and its `+0x80`..`+0x247` is the embedded `0x1C8` `BattleStatsRecord`. So two maps
      cover it: [the spawn-keep entry field map](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md)
      below `+0x80` and [the battle stats record field map](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md)
      from `+0x80`. All 72 observed offsets have a row, and 69 have a name or meaning. The last unnamed one,
      `+0x080` (stats `+0x00`), is `FE-1`'s question (a flags word: bit 0 the battle-member lock, bit 2 the party
      AI flag), and it is tracked there. *(`FE-1` was ANSWERED 2026-09-26.)*
- [x] What field `+0x000` is. **CHARACTERISED 2026-09-02** — an **8-bit flag byte**; all bits 0–7
      individually set, six individually cleared, seven distinct test masks. `0x30` = bits 4|5,
      `0x48` = bits 3|6. Consumers point at spawn lifecycle, retirement, target eligibility and
      derived-state recomputation. Section 13. **AL-9.** *(ANSWERED in the register 2026-09-26, FABLE, Claude Opus 5.5:
      the field is the spawn-keep entry's lifecycle flag byte, and `AL-10` below names every bit from its writer.)*
- [x] ~~What the **individual bits** of `+0x000` mean. Deliberately not named from consumers — see
      section 13.~~ **AL-10 ANSWERED by the writers (2026-09-12, FABLE, by reference):** the record at
      unit `+0x6A0` is **the spawn-keep entry** (`SpawnRecord`, `0x250` bytes, table `0208E690`, the
      stats record embedded at `+0x80`), and [the spawn-keep entry field map](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) §2.3 names every bit from what sets it —
      0 range-retired, 1 `ACTIVATION_COMMITTED`, 2 slot released, 3 / 6 lifecycle point mode
      (positive / negative float), 4 `RANGE_RETIRE_INHIBITED`, 5 category-4 mode, 7 affinity dirty.
      The table is repeated at the end of §13.
- [x] ~~Why the record is stored at **both** `unit + 0x698` and `unit + 0xE68`, and whether readers
      use the two interchangeably. This document's census counted only the former.~~ **AL-7 ANSWERED
      2026-09-12 (FABLE):** the premise was wrong — `+0xE68` is the `.ard` slot-0 class row (the
      correction above), a different object with its own readers; the `+0x698` census is complete.
- [x] **`GR-2` — what each free-target type value denotes as authored.** *(Answered 2026-09-30, FABLE, [record](../../_index/candidates/gr2-free-target-types-fable-0930/README.md): by the scripts that set each value (every shipped call of `setfreetargettype`, stored as is, and of `btlAtelSetUnitType`, mapped through `{1, 5, 3, 4}` at `01E09EE8`; `gr2_join.py`): **1** = a hostile combatant (59,832 sites: the `monster_*`, `unique_monster_*`, trial, notorious-monster and boss scripts); **3** = an allied or event combatant, plus the five `disp_tama` objects of seven `rbl` zones (35 of the 68 distinct sites; C5) (612: `THIRD_*` guests, `DAL_SOLDIER_*`, `npc_battle_*`, the `disp_tama*` scripts); **4** = an object the player interacts with (2,709: `system_crystal_actor` save crystals, `system_anchor_actor`, treasure, quest objects; ~~369 of them are monster scripts in 18 zones that park a monster as type 4~~ `btlAtelSetUnitType(3)` gives type 4 only while the unit's spawn record has bit 5, else the next refresh turns mode 4 into 1 (C3); type 4's largest authored source is `npc_to_gimmick`, 2,036 us-copy sites, nearly all `treasure_NN` (C1)); **5** = a non-combatant standing in a battle scene, neither friendly nor hostile (234: townspeople `TWN_*` / `SND_*`, prisoners `PRISON_*`, five `COCKATRICE_*`, and `BASH` / `DAL_SOLDIER_A` in one scene); **6** = ~~a stationary boss part~~ the type three boss-fight scripts set (45: `BOSS_Dウォール`, whose script also sets 1, `STAY_ボス武器` and `STAY_ダイダロス`; "stationary" is the `STAY_` naming of two of them, C5). ~~No script passes 0, 2 or 7: those arise only from the unit refresh (AL-3's other writer).~~ *(Narrowed 2026-10-01, OPUS, on SWE2-AUDIT-SEM's ACCEPT-WITH-NARROWING [review](../../_index/candidates/auditsem-review-gr2-0930/REVIEW.md), C1-C5:)* The nibble has six writers: `setfreetargettype`, `npc_to_gimmick` (`0x048E`, stores 4), `gimmick_to_npc` (`0x048F`, stores 5, unused), the unit refresh, the battle-unit binder `00265A20` (stores 1) and the record initialiser `002666F8` (0, then 4 for kind 1 or 5 for kind 3). No script passes 0, 2 or 7: 7 is the refresh's, 0 the initialiser's (and the getter's answer for a null actor), and no writer read produces 2. The table is what the scripts ask for; the refresh rewrites the nibble from the unit's mode, so a live value can differ. Every count is nine language copies of the same sites. The kind names are read from the script names, a naming reading of shipped data.)* Registered 2026-09-30 (FABLE). `AL-3`
      answered what the nibble *is*: the actor's free-target type, `actor[+0x0E] & 0xF`, set by the verb
      `setfreetargettype` and by the unit refresh. The item above lists what its readers do with each value. Value 5 is
      neither friendly nor hostile to the relationship classifier. The field cursor helpers accept 1–2, 1–3, 3 and 5.
      This page's classifier maps 3 to 4 and 1, 2, 7 to 8. [The record behind every actor](../Actor-Storage-Record/the-record-behind-every-actor.md)
      shows a further reader that groups the values as {1, 2, 7}, {3} and the rest for the time-stop sweep. ~~No reading
      so far names the values themselves.~~ The values the verbs pass are named by SD-160's census (above, C3), and GR-2's answer (the box's note) joins each resulting type value to the kind of actor its scripts set up.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 104 comparison sites across 82 functions | full-image disassembly, filtered to registers provably loaded from `[X + 0x698]` in the same function | 1 |
| The eleven-subsystem spread | those functions joined to `functions.tsv` owners | 1 |
| The filter under-counts | `002FFDAE` compares against `0` and is excluded because a `call` intervenes — verified by reading that function | 1 |
| An unfiltered `[reg+5]` scan is meaningless | it also matches `vp8_decode_frame` and `vp8_peek_si_internal` | 1 |
| kind 0 is type-keyed, kind 1 is owner-keyed | full body of `FUN_002F8E90` (131 B) | 1 |
| The party/foe reading fails | the same `== 1` test appears in `PartyFollow_SolveFormation` and in `SpawnGroup_*` / `EnemyChain_UpdateOnDefeat` | 1 |
| This is not the actor class field | [`../battleunit-slot-pool-and-actor-class.md`](../battleunit-slot-pool-and-actor-class.md) documents a 3-bit field on a different object | 2 |
| The call chain of §5a | raw call index (`tools/rawcalls.json`), with each named call site read: `0023A3F1`, `0023A776`, `0023A7A9`, `00237E26`, `002FFEB0` | 1 |
| Every party-table record is initialised with ids `0`–`0x27`, so its byte is 0 | `00237DF0` loop `00237E00`–`00237E30`: `edx = ebx` (the loop counter), record `*(02EBF190) + 8 + ebx × 0x1C8`, call `00237E26` | 1 |
| Bit 7 of `+0x000` is set at eight sites, and bits 0–6 at one each | re-run 2026-09-30 (FABLE) of §13's rule (an `or` with an immediate on a register loaded from `[X + 0x6A0]` or `[X + 0x698]` in the same function, taint dropped at calls): fifteen sites. The positive control is the eight bit-7 sites of the AL-10 table, found 8 of 8. Script: `record_flag_or_sites.py` in the [2026-09-30 DD record](../../_index/candidates/dd-content-fable-0930/) | 1 |
| `+0x019` of the entry is written | full body of `00321810` (47 B): `lea rcx, [rax + 0x19]` at `00321824`, store at `00321834`; its only call site is `00239358` | 1 |
| The 110-byte function that draws from the RNG is `002398F0` | full body of `002398F0` (110 B) | 1 |

**Scope honesty:** ~~this document deliberately stops at "two kinds, one type-keyed and one
owner-keyed". Every candidate meaning considered so far is contradicted by at least one consumer.~~
*Corrected 2026-09-30 (FABLE): the page no longer stops there. The writer names the two kinds (`AL-1`, §2's
corrected block). Type-keyed is a party-table record whose low byte is the row (`AL-6`); owner-keyed is an
enemy-table record embedded in a spawn-keep entry. The consumer-side readings of §3 remain refuted as consumer
readings.*

## 9. Related

- [`../battleunit-slot-pool-and-actor-class.md`](../battleunit-slot-pool-and-actor-class.md) — the **other** class field, not this one
- [`../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`](../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md) — gates on both `0` and `1`
- [`../../08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md`](../../08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) — where `FUN_002F8E90`'s category selects a damage multiplier
- [`../../13-Rewards-Progression-Economy/experience-and-license-point-award.md`](../../13-Rewards-Progression-Economy/experience-and-license-point-award.md) — two of the 82 consumers

## 10. Falsification pass 2026-09-02 — AL-5, and the byte is authored

**Attack chosen.** Section 3 refused every reader-side reading of this byte. When the readers cannot
settle a field's meaning, the writers usually can — so this pass ran the census section 7 said had
never been run.

### AL-5 answered: nothing writes it through the record pointer

A full-image scan for byte writes to `[reg+5]`, filtered to registers provably loaded from
`[X + 0x698]`, returns **zero**. Widening to *any* function that both writes a byte at `[reg+5]` and
mentions `+0x698` returns exactly **one** (`BattleUnit_AdvanceStandardActionState`), and that write
is not to a register carrying the record.

**The byte is never modified through the access path all 82 readers use.** It is set when the record
is installed and not touched again.

### Who installs the record

Scanning for 8-byte writes to `[reg + 0x698]` gives **17** sites, of which only two are on the
battle-unit path:

| Site | Function |
|---|---|
| `00236AB4` | `BattleUnit_ResetStateForReuse` (ActorEntity) |
| `0023ABFA` | **`BattleUnit_ApplyUnitDefinition`** (ActorEntity) |

The other 15 are Audio-owned or unowned functions writing offset `0x698` on **a different
structure** — the same contamination pattern that made the unfiltered `[reg+5]` scan useless. They
share no call path with the battle-unit code.

**So the record arrives with a unit definition.** `BattleUnit_ApplyUnitDefinition` installs it, and
in the same function reads a cluster of small fields from it — `[r15+4]`, **`[r15+5]`**, `[r15+6]`,
`[r15+0x22]`, `[r15+0x23]`, `[r15+0x27]` — the shape of an authored record being unpacked.

**That reframes AL-1.** The byte is not runtime state that something decides; it is **authored data
attached to a unit definition**. A definition-level category can perfectly well be shared by units
that behave differently in play, which is exactly why the party/foe reading failed — the
contradiction was never in the evidence, it was in assuming the field described a *side* rather than
a *kind of definition*.

### New: `+4` and `+5` are one 16-bit field

`BattleUnit_ApplyUnitDefinition` also contains:

```
0023A5A1  mov   rax, qword ptr [rcx + 0x698]
0023A5A8  movzx ebx, word ptr [rax + 4]        <- a WORD at +4, spanning bytes 4 and 5
```

And `FUN_002F8E90` reads them as two bytes with distinct roles — `unit[4]` as a **type id** tested
against `0x1B .. 0x27`, `unit[5]` as the **kind**. Together:

```
record + 4   u16   read whole in ApplyUnitDefinition
   +4  byte   type id   (kind 0 tests it against 0x1B..0x27)
   +5  byte   kind      (the subject of this document)
```

**The kind is the high byte of a 16-bit identifier whose low byte is a type.** That is a much more
specific structure than "a byte at +5", and it is consistent with the classifier's asymmetry: for
kind 0 the low byte is meaningful as a type, for kind 1 it is not consulted at all.

### Also: the record is reachable by two pointers

```
0023A91C  mov qword ptr [rdi + 0xe68], r15
0023ABFA  mov qword ptr [rdi + 0x698], r15
```

~~The same record is stored at **`unit + 0x698` and `unit + 0xE68`**. Any census keyed only on `+0x698`
— including this document's — therefore under-counts by construction. Recorded as a caveat on the
104-site figure, which remains correct for what it measured.~~ **Withdrawn 2026-09-13 (FABLE, re-verified from the bytes):**
the two stores write **different values** — `r15` is reassigned between them. `BattleUnit_ApplyUnitDefinition` (`0023A570`) splits on the definition id's high byte (`0023A626`/`0023A62E`). **Kind 1 (spawn-backed):** `+0xE60` = the `02EBF120` definition row (`0023A915`), **`+0xE68` = the `.ard` slot-0 class row** — `02EBF150` indexed by the definition row's `u16 +0` (`0023A6F0`–`0023A6FC`, stored `0023A91C`) — **`+0x698` = the SpawnKeep entry `+ 0x80`** (`0023A787` `sub rax, −0x80`, kept at `[rsp+0x90]` `0023A795`, reloaded into `r15` `0023AA15`/`0023AA2F`, stored `0023ABFA`), a `0x1C8`-byte `BattleStatsRecord` embedded in the `0x250` entry, and `+0x6A0` = the entry (`rbp`, `0023A77B` → `0023AC01`). **Kind 0:** `+0xE60` = the `02EBF130` row (`0023ABC3`), **`+0x698` = `*(02EBF190) + 8 + slot × 0x1C8`**, an element of the BattleSystemState array (`0023AAAA`–`0023AAC1`), `+0x6A0` = NULL (`0023AAB1`), and `+0xE68` is not written (the reset `00236AC2` leaves 0). So the `+0x698` census
does not under-count this record; `+0xE68` readers see the class row (§2's corrected block, `AL-7`).

### Status

**AL-5 is answered.** ~~AL-1 remains open but is now better posed: the question is what an authored
definition kind distinguishes, not what a runtime flag means.~~ AL-4's value domain is unchanged.
*Corrected 2026-09-30 (FABLE): AL-1 was answered on 2026-09-10. The kind is the table byte of the definition id
(§2's corrected block). AL-4 was answered on 2026-09-12 (`{0, 1}`, §7).*

## 11. Falsification pass 2026-09-02 (second) — where the record comes from

**Attack chosen.** Pass 37 established the byte is authored and installed by
`BattleUnit_ApplyUnitDefinition`. That leaves one question that can actually settle **AL-1**: where
does `ApplyUnitDefinition` *get* the record? Traced.

### The provenance chain, read

```
0023A76E  movsx edx, byte ptr [rdi + 0x57]   ; an index byte on the unit
0023A772  mov   rcx, qword ptr [rdi + 0x40]  ; a "spawn keep" on the unit
0023A776  call  0x236100                     ; SpawnKeep_ResolvePrimaryEntry
0023A787  sub   rax, -0x80                   ; record = definition + 0x80
0023A795  mov   qword ptr [rsp + 0x90], rax
...
0023AC01  mov   qword ptr [rdi + 0x6a0], rbp ; the definition base
0023ABFA  mov   qword ptr [rdi + 0x698], r15 ; the record = base + 0x80
```

`SpawnKeep_ResolvePrimaryEntry` (`00236100`, 56 B) is short enough to give whole:

```c
void *SpawnKeep_ResolvePrimaryEntry(byte *keep, int index)
{
    if (keep == NULL || index < 0)      return NULL;
    if (index > (int)keep[0] - 1)       return NULL;   /* keep[0] = entry count */
    id = keep[1 + index];                              /* the entry's definition id */
    if (id == 0xFF || (int8)id < 0)     return NULL;   /* 0xFF marks an empty slot */   /* <- corrected 2026-10-02, OPUS - the sign test reads a zero-extended byte (0023611F movzx eax, dl; 00236122 test eax, eax; js), so it never rejects: ids 0x00-0xFE all resolve */
    return *(void **)0x0208E690 + id * 0x250;
}
```

### What that settles

| Fact | Value |
|---|---|
| unit definition table pointer | **`0x0208E690`** (`.data`, filled at runtime) |
| definition record stride | **`0x250` = 592 bytes** |
| definition id | a **single byte**, `0x00`–`0xFE`; `0xFF` means empty |
| spawn keep format | `[0]` = entry count, `[1..]` = id bytes |
| `unit + 0x6A0` | the definition record base |
| `unit + 0x698` | the same record **+ 0x80** |

So the "battle record" this document has been describing is **not a separate object**. It is a
**view into the authored unit definition**, 0x80 bytes in. Which means:

```
record[5]        =  definition byte  +0x85
record[4] / [5]  =  definition word  +0x84
```

**`record[5]` is byte `0x85` of a 592-byte authored unit-definition record.** That is as close to the
authoring side as this chain goes without the data files themselves, and it re-poses **AL-1** in its
final form: *what does field `+0x85` of a unit definition record enumerate?* — a question about a
data table, not about code.

*Corrected 2026-09-30 (FABLE): AL-1 did not need the data table. It was answered from code on 2026-09-10 by
reading the installer (§2's corrected block): the byte is the table byte of the definition id that `0023AC80`
stores whole. §12 had already withdrawn "authored" for this record, which is the spawn-keep entry (`AL-8`).*

### A second document is sharpened by this

[`../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`](../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md)
records `unit->[0x6A0][0]` tested with masks `0x30` and `0x48`, and asks what they are (**AI-6**).
`unit + 0x6A0` is now identified: it is the **definition record base**, so that test reads **byte 0
of the authored definition**. The question is unchanged but is now known to be about authored data.

### Why the naming in this document is imprecise, and stays

The name "battle record" came from the access path (`unit + 0x698`) before its origin was known. It
is really *the tail two-thirds of a unit definition record*. The document keeps the term, because 82
functions reach the field through `+0x698` and renaming it would make every citation harder to
follow — but the offsets above give the true frame of reference.

### Where this does not reach

Nothing here says what any definition field **means**. The table's contents are runtime-loaded (the
pointer at `0x0208E690` is null in the file image), so enumerating actual `+0x85` values needs the
authored data, not the executable. ~~**AL-1 stays open, and is now known to be unanswerable from the
binary alone.**~~ *Corrected 2026-09-30 (FABLE): wrong. AL-1 was answered from the binary on 2026-09-10 (§2's
corrected block, §7). The table's values are loaded at runtime, but the code that writes the byte fixes what it
means.*

## 12. Falsification pass 2026-09-02 (third) — AL-8, and a correction to pass 11

**Attack chosen.** Pass 11 called the 592-byte object an *authored unit definition record*. That
claim was made from its **provenance** (a table lookup by id) without checking whether anything
writes it. AL-8 asked what the record contains; answering it also tests pass 11's label.

### The field map

Both access paths were censused together — registers tainted from `[X + 0x6A0]` (bias 0) and
`[X + 0x698]` (bias `0x80`) — and every field access recorded with its size:

| | |
|---|---:|
| distinct offsets observed | **72** |
| total accesses | **917** |
| offsets with **no scalar store at their displacement** | **49** |
| — of those, **known written** (section 12a) | **≥ 6** |
| offsets with **a scalar store at their displacement** | **23** |
| span | `+0x000` … `+0x242`, inside the `0x250` record |

Full map: `Tools/work/rtti/unit_record_fields.tsv` — `def_offset / record_offset / sizes / reads /
writes / subsystems`.

### CORRECTED: this is not a shared authored definition

**Twenty-three of the seventy-two fields are written**, `+0x000` most heavily — **54 reads and 26
writes** across six subsystems. A record shared by every unit of a given id could not be mutated
without corrupting all of them.

So the earlier label was wrong in an important way. What the evidence supports:

> `*(void **)0x0208E690` is an array of **592-byte per-unit battle records**. The spawn keep at
> `unit + 0x40` maps a unit's index to its record id, and `SpawnKeep_ResolvePrimaryEntry` returns
> that record. Some fields are **initialised and never written again** (identity), others are **live
> state**.

The provenance chain in section 11 is unchanged and correct — only the word "authored" was too
strong. **A lookup by id proves indexing, not immutability**; that had to be tested separately, and
pass 11 did not test it.

### The read-only core

The four most-read fields are all in the no-scalar-store group, and two of them are already documented:

| def offset | record offset | reads | writes | what |
|---|---|---:|---:|---|
| **`+0x085`** | `+5` | **228** | 0 | the kind byte — this document |
| `+0x0E4` | `+0x64` | 158 | 0 | **status layer 1** |
| `+0x0BC` | `+0x3C` | 155 | 0 | **status layer 0** |
| `+0x084` | `+4` | 76 | 0 | the type id |

**That is an independent confirmation of the `+0x80` relation.** The two-layer status pair, sighted
fourteen times across the database at `record +0x3C` / `+0x64`, lands at definition `+0xBC` / `+0xE4`
— exactly where the arithmetic predicts, and as the second and third most-read fields in the whole
record. If the `+0x80` offset were wrong, that coincidence would have to be manufactured.

*(Their zero write counts are an artefact of the census: it follows only these two access paths and
drops taint at calls, and statuses plainly do change. The counts measure **these** paths, not all
mutation — the same limitation already recorded twice on this document's figures.)*

### The kind byte in context

`+0x085` is **the single most-read field in the record**, at 228 accesses — more than either status
layer — and **carries no store of any width on any of the three routes swept in section 12a**.
Everything this document says about it is consistent with an identity field fixed at record
initialisation. *(Section 12a refutes the "never written" phrase for six other offsets and leaves
this one standing — under an instrument with perfect recall on the census's own 23 positives, which
is the strongest check this claim has had.)*

### What this does not change

~~**AL-1 remains bounded.**~~ The record's *values* are still runtime-loaded and unavailable from the
executable. Knowing the field is identity rather than live state narrows what it could mean~~, but does
not name it~~. *Corrected 2026-09-30 (FABLE): the writer names it. AL-1, answered 2026-09-10: it is the table
byte of the definition id (§2's corrected block).*

## 12a. Falsification pass 2026-09-17 (OPUS) — "never written" is refuted, and it contradicted a sibling page

**Why this section exists.** FABLE refuted the phrase *never written* on 2026-09-16 with a witness and
filed the propagation as a notice, because this page was dirty at the time. The phrase labels one of
this page's headline numbers and appeared on it five times, so it is re-derived here rather than
relayed, and then measured.

### 1. FABLE's witness, re-derived from the entry

Decoded from the **entry** `002355A0` `Spawn_PrepareRandomCandidateForCurrentEntry`, so the
instruction boundaries are real rather than assumed:

| address | instruction | what it establishes |
|---|---|---|
| `00235668` | `imul rsi, rdx, 0x250` | the record stride this page names |
| `0023566F` | `add rsi, qword [0208E690]` | the record table this page names |
| `002356D5` | `movups xmmword [rsi + 0x60], xmm0` | covers `+0x60`…`+0x6F` |
| `002356DE` | `movups xmmword [rsi + 0x50], xmm0` | covers `+0x50`…`+0x5F` |

`rsi` is **not redefined** between `0023566F` and `002356DE` — checked instruction by instruction; the
restore `mov rsi, [rsp+0x70]` is at `002356EE`, after both stores.

**The one way this could have been wrong, checked.** The field map has two views, and a store
displacement matched against the wrong one would mean nothing. All 54 rows carrying both give
`record_offset = def_offset − 0x80` exactly, and `def_offset` is the offset **within the 592-byte
record** — its span `+0x000`…`+0x242` fits `0x250`, and `AL-1` fixes `record[5]` as field `+0x85`.
`rsi` holds the record base, so `[rsi+0x60]` lands on def rows `+0x060`/`+0x064`/`+0x068`. **The
identification survives the check that could have broken it.**

### 2. A base-attributed sweep, and what warrants it

The earlier `FE-4` sweep was displacement-generic across the whole image and deliberately attributed
nothing. This one counts a store **only** when the destination register provably holds a pointer to
*this* record — formed in the same function and not redefined before the store — across all three
routes: the table (`*(0208E690) + i*0x250`), `[X + 0x6A0]` (bias 0) and `[X + 0x698]` (bias `0x80`).
Selectors: `Tools/work/OPUS/p1-scratch/al8_blocksweep.py`, `al8_unitroute.py`, `al8_intersect.py`.

**Recall control: 23 of 23.** Every row the census records as written is independently reproduced by
the sweep — including all ten `CombatAction` two-byte rows `+0x08A`…`+0x09E` at exactly one store
each. An instrument that reproduces *all* of a census's positives has earned the right to be believed
about its negatives.

*(That control also caught a defect in the sweep itself: capstone prints small displacements in
decimal, so `inc word [rax + 8]` was first binned at `+0x000`. Recall was 21/23 until the parser read
decimal displacements; it is 23/23 after. The figures below are the corrected run.)*

### 3. Result — six of the forty-nine are written

| def offset | how it is written | why the census missed it |
|---|---|---|
| `+0x008` | `inc word [rax+8]` — `00300801` | taint dropped at a call |
| `+0x012` | `mov byte [rbp+0x12], bl` — `0023A840` | taint dropped at a call |
| `+0x060` | block `movups` `+0x60`…`+0x6F` — `002356D5`, `00239490`, `00234291` | block store **and** untracked route |
| `+0x064` | the same block, **and** a scalar `movss [rax+0x64]` — `0023A4D5` | block store **and** taint dropped |
| `+0x068` | the same block | block store **and** untracked route |
| `+0x070` | scalar `movss [rax+0x70]` — `0023929C`, `0030046E`, `00307A4F` | taint dropped at a call |

**Three of the six are not block stores at all.** `+0x008`, `+0x012` and `+0x070` are ordinary scalar
stores at the very displacement the census reports as unwritten, on a **censused** path. In each the
pointer register came back from a call — `ActorWork_GetBattleUnit` (`0031B760`) at `0023922A`, and
`0023A41B` for `+0x064` — and section 12's census **drops taint at calls**, so it never tainted the
register and never saw the store. **The block-store defect alone does not account for these figures.**

**So the instrument has three separate blind spots, not one:** a store is counted by its displacement
(a 16-byte store marks one offset and covers sixteen); taint is dropped at calls; and the table route
`*(0208E690) + i*0x250` was never censused at all — it is how `002355A0` and `00239490` reach the
record. Only the first was named on 2026-09-16.

### 4. The part that matters most — this contradicted a sibling page

Seven of the forty-nine lie below `+0x80`, inside the spawn record proper:
`+0x008`, `+0x012`, `+0x019`, `+0x060`, `+0x064`, `+0x068`, `+0x070`.
[The spawn-keep entry field map](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md)
§2.2 **already documents six of those seven as named, written fields, with their writers** —
`wDeathCount` `+0x08`, the spawn-history counter copy `+0x12`, `candidateStateSecondary`
`+0x60`…`+0x6F`, and `flPersistedFacingYaw` `+0x70`. The writer addresses it lists are the same ones
this sweep found independently, `+0x70`'s three among them. **Only `+0x019` (the enmity decay timer)
survives, and that page lists no writer for it either.**

*Answered 2026-09-30 (FABLE): `+0x019` has a writer. `00321810` (47 B, read whole) loads unit `+0x6A0`, forms
`lea rcx, [rax + 0x19]` (`00321818`–`00321824`) and stores **`0`** there at `00321834`. `dl` was cleared at
`0032181F`; the `setne dl` after the store is the argument of the tail jump at `00321839`. That jump goes to a fill
helper, which writes the same 0 or 1 into the forty bytes `+0x1A`…`+0x41`, one for each combatant id the id
validator accepts. The only call site of `00321810` is in `002392D0` (`00239358`, raw call index). The sweep missed
it for a fourth reason: the address is formed by `lea` and the store is at displacement 0. So all seven offsets
below `+0x80` are written.*

That is the real defect. The figure was not merely unsupported in principle — it stood in direct
contradiction with a sibling page describing **the same `0x250` bytes**, and the sibling page was
right. The remaining 42 of the 49 lie at or above `+0x80`, inside the embedded `0x1C8`
`BattleStatsRecord`, which is a different object with its own page; nothing here speaks to them.

### 5. What the block stores turn out to mean

- **`+0x060`, `+0x064`, `+0x068` are one three-float vector** — the candidate position, `x`/`y`/`z`.
  `SpawnUnit_FinalizeSpawnEntryActivation` reads `[rax+0x60]` and `[rax+0x68]`, passes
  `lea r8, [rax+0x64]` (`0023A4AE`–`0023A4B7`), then adds unit `+0x188` — **the candidate-position y
  adjustment** — into `+0x64` (`0023A4C8`–`0023A4D5`). One `movups` covers exactly these three rows
  because they are one field.
- **The kind byte gates a write, at two independent sites.** `BattleUnit_PublishLocomotionPosition`
  tests `byte [rax + 5] == 1` before `movups [rax+0x50], xmm0` (`003003BE`–`003003CE`), and
  `ActorSystem_ReleaseBattleUnitSlotForActor` tests the same byte before copying unit `+0xE0` into
  `+0x60` (`0023425D`–`00234291`). `record +5` **is the kind byte this document is about**, and
  `+0x6A0` is NULL for kind 0 — so the kind test is the null-guard for the record pointer. That is a
  use of the byte this page had not recorded.

### 6. Scope, stated as a limit

The sweep resolves three routes and **44 of the 49 remain uncovered by it**. That is **not** evidence
they are unwritten: a register-relative writer defeats it exactly as the block store defeated the
census — `SpawnKeep_InitializeEntriesFromDefinitionTable` writes `+0x08` at `0023965C` through
`[rdi + rcx + 8]` with `add rdi, 0x250` advancing the row, and this sweep does not see that store
either. It found `+0x008` by the other writer.

The honest reading of the figure is **"49 offsets with no scalar store at their displacement on the
censused paths, of which at least 6 are written"** — a floor, not a count.

**What survives.** Every conclusion this page draws from the figure stands, and two are strengthened:
the record is per-unit mutable state rather than a shared authored definition (block writes make it
*more* mutable, not less), and the kind byte `+0x085` still carries **no store of any width on any of
the three routes** — now checked by an instrument with perfect recall on the census's own positives.

## 13. Falsification pass 2026-09-02 (fourth) — AL-9: record field `+0x000`

**Attack chosen.** Pass 12 found `+0x000` is the record's most heavily mutated field — 54 reads, 26
writes, six subsystems — and the same field the availability cascade masks with `0x30` and `0x48`
(**AI-6**). A field that is both widely written and widely tested is a flag word; the way to read one
is to census its **masks**, not its value.

### It is an eight-bit flag byte, and every bit is live

Immediates used against `record[0]` through the two tainted access paths:

| operation | distinct masks | detail |
|---|---:|---|
| `or` (bit **set**) | 8 | `0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80` — **every bit 0–7** |
| `and` (bit **cleared**) | 6 | complements of `0x01, 0x04, 0x08, 0x10, 0x20, 0x40` |
| `test` | 7 | see below |

**All eight low bits are individually set, and six are individually cleared.** Nothing touches bits
above 7 through these paths, so `+0x000` behaves as a one-byte flag field.

### AI-6 answered structurally

The two masks the availability cascade uses decompose cleanly:

```
0x30  =  bit 4 | bit 5
0x48  =  bit 3 | bit 6
```

They are **not** two opaque constants — each is a pair of bits that other code sets, clears and tests
individually. So the cascade's two `return 2` refusals are "any of these lifecycle bits is raised".

### Which code cares about which bit

Recording consumers rather than inventing names:

| mask | bits | tested by |
|---|---|---|
| `0x05` | 0, 2 | `SpawnEntry_ConfigureFreshLifecycleFloatMode`, `FUN_002392D0`, `FUN_002398F0` |
| `0x10` | 4 | `SpawnLifecycle_CheckAndRetireByNativeRange`, `AiOrder_EvaluateTargetSelector` |
| `0x20` | 5 | `BattleTarget_ComputeEligibilityBlockMask`, `BattleUnit_RefreshActorRuntimeFromDefinition` |
| `0x30` | 4, 5 | `BattleAction_CheckActionAvailabilityReason`, `AiOrder_EvaluateAndResolveActionTarget` |
| `0x40` | 6 | `BattleTarget_ComputeEligibilityBlockMask`, `FUN_0031FE10` |
| `0x48` | 3, 6 | `BattleAction_CheckActionAvailabilityReason`, `AiOrder_EvaluateAndResolveActionTarget` |
| `0x80` | 7 | `BattleStats_RecomputeDerivedStateAndAutoStatuses` |

The pattern in those names is consistent: **spawn lifecycle** (bits 0, 2), **retirement and
targeting** (bit 4), **target eligibility** (bits 5, 6), and **derived-state recomputation** (bit 7).
Bit 7 is also the most-written — `or 0x80` appears at **eight** sites, more than every other bit
combined.
*(Sites re-derived 2026-09-30 (FABLE) with the census's rule: a register loaded from `[X + 0x6A0]` or `[X + 0x698]`
in the same function, taint dropped at calls. The rule finds fifteen `or` sites. Eight are `0x80`, all
`or dword ptr [rax], 0x80` in `BattleFormula_ApplyTargetResult`: `0031195E`, `00311986`, `003119AE`, `003119D6`,
`00311A00`, `00311A2A`, `00311A54` and `00311A7E`. Bits 0–6 have one site each, and they are the seven writers of
the AL-10 table below.)*

So `+0x000` is best described as a **per-unit lifecycle and target-eligibility flag byte**. That is
as specific as the evidence goes: the consumers are named, ~~the individual bits are not~~ *(answered on the spawn side: see AL-10 below; 2026-10-02, OPUS)*.

### Why the bits are not named here

Each bit could be given a plausible name from its consumers — bit 4 "retired", bit 5 "untargetable",
and so on. **Two readings were killed today by exactly that move** (multiplier constants that looked
elemental; a byte whose consumers looked party-side). A consumer tells you what a bit *gates*, not
what it *means*, and one function testing two bits together cannot distinguish them. Naming waits
until something sets a bit for a reason that can be read.

> **That condition was met on the spawn side (2026-09-12, FABLE, AL-10).** The census above reached
> the byte only through the unit's `+0x6A0` pointer, which is why it saw tests and no sets: the
> writers reach the same record through the table base `0208E690` (`base + index × 0x250`) — the
> record is **the spawn-keep entry**, not a copy of the authored definition, and its second block
> `+0x80` is the stats record `+0x698` also points at. [the spawn-keep entry field map](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) §2.3 read every writer:
>
> | bit | set by (the reason) | name |
> |---|---|---|
> | 0 `0x01` | `SpawnLifecycle_CheckAndRetireByNativeRange` retires the unit out of native range (`002352A6`) | **range-retired** |
> | 1 `0x02` | `BattleUnit_ActivateAppliedDefinitionRuntime` commits a kind-1 activation (`00233BA8`) | **`ACTIVATION_COMMITTED`** |
> | 2 `0x04` | `ActorSystem_ReleaseBattleUnitSlotForActor` releases the unit's slot (`0023429B`) | **slot released** |
> | 3 `0x08` | `SpawnEntry_ConfigureFreshLifecycleFloatMode`, lifecycle float `> 0` (`0023A282`) | **lifecycle point mode, positive** |
> | 4 `0x10` | `SpawnEntry_SetRangeRetireInhibitTag` with a non-zero tag at `+0x15` (`002391FD`) | **`RANGE_RETIRE_INHIBITED`** |
> | 5 `0x20` | `BattleUnit_SetRuntimeUnitCategoryMode` when the mode byte `+0x58` becomes 4 (`002396F9`) | **category-4 mode** |
> | 6 `0x40` | `SpawnEntry_ConfigureFreshLifecycleFloatMode`, lifecycle float `< 0` (`0023A2AC`) | **lifecycle point mode, negative** |
> | 7 `0x80` | `BattleFormula_ApplyTargetResult` once per affinity byte changed (`0031195E`–`00311A7E`) | **affinity dirty** (the recompute's `0031043A` test) |
>
> So the availability cascade's `0x30` refusal is "range-retire-inhibited or in category-4 mode" and
> its `0x48` refusal "in a lifecycle point mode, either sign"; the target-eligibility tests on bits
> 5 / 6 are the same two modes; bit 7 is the affinity recompute's dirty flag. The kind byte `+5`
> this page is about is unaffected — it lives in the stats block at `+0x85` of the entry.

### What this changes elsewhere

**AI-6 moves from "unknown constants" to "known bit pairs"** in
[`../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`](../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md).
The reason-2 refusals are lifecycle/eligibility gates, which is consistent with that document's
reading of reason 2 as *"unit not in a state that can act at all"* — arrived at independently, from
the cascade's structure rather than from this field.

## 11. The `+4` band census — 2026-09-03, session `repos-78`

Section 2 censuses the **`+5`** byte: 104 comparison sites across 82 functions. This is the companion
census of the **conjunction** that section 7 leaves open as *"what `unit[4]`'s type ids `0x1B .. 0x27`
enumerate"* — how widely that band is actually consulted.

Scanning `.text` for the exact encoding `2C 1B 3C 0C` (`sub al, 0x1B` ; `cmp al, 0x0C`):

| | |
|---|---:|
| occurrences | **26** |
| distinct functions | **22** |
| testing `byte ptr [<reg> + 4]` | **23 of 26** (on nine different base registers) |
| preceded by a `[+5]` test within six instructions | **21 of 26** |

**So the idiom is a two-byte discriminator, not a lone range check:**

```c
if (rec[5] == 0 && (uint8_t)(rec[4] - 0x1B) <= 0x0C) { ... }   /* 13 kinds */
```

The 22 functions span spawn (`00233A20`, `00235AB0`, `00237EA0`), rewards
(`Reward_ComputeExperienceForRecipient`, twice), stats
(`BattleStats_RebuildEffectiveStatsAndAffinityState`, `BattleStats_ChangeStatusAndProcessSideEffects`,
`BattleStats_ReconcileCurrentHpToEffectiveMaximum`), AI (`AiOrder_EvaluateTargetSelector`), action
availability (`BattleAction_CheckDefinitionCategoryAvailability`, twice), the periodic tick
(`BattleUnit_RunPeriodicCombatMaintenance`), and the formula layer
(`BattleFormula_ResolveTargetResult`, `BattleFormula_ApplyPreResolutionTargetGates`).

> **Eight subsystems test the same thirteen-value band on the same byte, under the same `+5 == 0`
> guard, and none of them says what it is.** That is the same shape as the `0x80000003` predicate — a
> set membership consulted by many questions — and it strengthens **AL-2** and **N-4** ~~without~~
> ~~answering either~~ *(answered: both on 2026-09-11 — see the correction below; 2026-10-02, OPUS)*: the band is not a local convention in the reward path where it was first seen.

**What this does not establish** is ~~any of the thirteen values' meaning, or~~ whether the band is an
inclusion or an exclusion — **the sense differs by call site.** In
`BattleUnit_RunPeriodicCombatMaintenance` the `ja` skips the guarded block, so in-band records take the
extra path; a reader must check the branch at each site rather than assume one polarity.

*Corrected 2026-09-30 (FABLE): `AL-2` and `N-4` were both answered on 2026-09-11. The thirteen values are the party
table's Esper rows, Belias to Zodiark (§7), and the reward test excludes them from EXP and LP. The per-site polarity
caveat stands.*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **RNG_Random_Selection — SERVICE.** A 110-byte function this page cites draws from `RNG_SharedGameplayLCG_NextU32`.
  *Named 2026-09-30 (FABLE), body read whole: it is `002398F0`. It resolves the unit (`00239904`) and returns −1
  when there is none, or when the spawn-keep entry's flag byte has bit 0 or bit 2 set (`00239918 test byte ptr
  [rax], 5`). Otherwise it draws once (`0023991D`) and passes `draw % (arg2 + 1) + arg3` to the level grower
  `0030C470` as its level argument, with `arg3` as its third (`00239934`). Its only call site is in the native verb
  body `0050F910` (`0050F94E`).*

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

*Most subjects here are the accessors that reach the record: `ActorWork_GetBattleUnit` `0031B760`, `BattleUnit_FindByCombatantId` `0031B770` and `BattleStats_FindOwningBattleUnit` `0031B860`, the classifier `002F8E90` and the kind-dependent action checks. §2's census found the `== 1` test in 82 functions across 11 subsystems, so a layer that reaches the record through these accessors is a reader of the kind byte's product. None of them is an owner of the byte, which is authored through the definition id (§2, corrected block).*

**CombatAI — CLIENT and SERVICE (11 edges).** Five AI bodies resolve units through `0031B760`: `BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit` `00239040`, `AiOrder_EvaluateAndResolveActionTarget` `003014C0`, `AiOrder_EvaluateTargetSelector` `00301AD0`, `AiOrder_SelectFinalTargetFromCandidates` `003087E0` and `AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` `0030F130`. `00301AD0` also resolves through `0031B770`. `003014C0` and `BattleUnit_SelectAndCommitNextAction` `00305AB0` call the availability check `002FFCF0`, whose `002FFDAE` compare against 0 is the census's under-count example. In the service direction, the stats initializer `0023AC80` seeds the gambit banks through `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030`, `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` `00327CB0` and `GambitRuntime_RebuildOrderSetForStatsRecord` `00327DE0`. AI target selection reads units, and through them the kind byte, via this page's accessors, and it asks the kind-aware availability check whether an action is allowed.

**CombatAction — CLIENT and SERVICE (22 edges).** `BattleTarget_ClassifyRelationshipClass` `0030AB40` reads the free-target nibble `00263C20`, which returns 0 when either side is 5 (AL-3). `BattleAction_ComputeGilCost` `00309060` and `BattleAction_ComputePrimaryResourceCost` `00309110` call `BattleUnit_UsesGilActionCostChannel` `002F9820`, which returns early when the byte is 1. The availability check `002FFCF0` is called by `BattleAction_CheckCurrentActionInterruptReason` `002FFB60`, `Battle_ProcessActionTarget` `00307300`, `0030DB70` and `00317BC0`. It calls `00303BD0`, `BattleAction_CheckUnitActionAvailability` `00306480` and `BattleAction_CheckGlobalCategoryDisableReason` `0031A7B0`. `00303BD0` in turn calls `003037A0`, `BattleAction_ComputeSecondaryResourceMultiplier` `00308FF0`, `00309060` and `00309110`. Previews and special sequences reach units through `0031B760` and `0031B860`: `BattleAction_EvaluateTargetPreviews` `00303830`, `BattleAction_EvaluateTargetPreviewRecursive` `00303A00`, `00306010`, `BattleAction_ResolveSpecialSequenceTargets` `0030EC00`, `BattleAction_CheckDefinitionCategoryAvailability` `003060E0` and `003879C0`. The kind byte decides which cost channel an action draws on and gates the resource-availability pools, and the action layer owns those cost and availability bodies.

**CombatFormula — CLIENT and SERVICE (42 edges).** Thirty-five formula and stats bodies map a stats record back to its unit through `0031B860`, among them `BattleFormula_ApplyTargetResult` `003112F0`, `BattleFormula_ResolveTargetResult` `00385F60` and `BattleFormula_ApplyPreResolutionTargetGates` `00390AB0`. The classifier `002F8E90` of §2 is called by five formula bodies: `00384F40`, `00388320`, `00389370`, `0038B150` and `0038BC00`. Its kind-1 arm is the owner resolve `0031B860`. `0023A570` calls the formula-filed initializer `BattleStats_InitializeDefinitionRecord` `0023AC80`, which writes the whole definition id into `+4` and so fixes the byte. The formula layer is the main consumer of the kind-dependent classification, since the Esper, other-party and owner-keyed categories come from `002F8E90`, and it owns the initializer that writes the byte.

**Gameplay — CLIENT and SERVICE (8 edges).** `BattleUnit_HasRelationshipClass2PlusInTrackedActorList` `0030B050`, `WorldActor_HasActiveBattleActionOrUnitFlag14` `0030BA30` and `WorldActor_QueryCombatStanceState` `0030BFB0` resolve units through `0031B760`, and `CombatantId_HasActiveBattleActionOrUnitFlag14` `0030BA80` does the same through `0031B770`. `BattleSystem_ResetRuntimeState` `00237DF0` calls `0023AC80`. `0023A570` and `002FFCF0` call the Gameplay-filed validator `BattleEncodedId_IsValidForClass` `00322C50`, and `002FFCF0` also calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0`. These are battle-state predicates that resolve a unit through this page's accessors, plus the id validator and mode read that the installer and the availability check consult. They do not interpret the kind byte themselves.

**Items_Equipment_Shops_License — SERVICE and CLIENT (6 edges).** `0023AC80` installs equipment and licences through `BattleStats_SetEquipmentSlotDirect` `0031A630` and `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910`. Those two, together with `BattleStats_SetEquipmentSlotByStatsIndex` `0031A410` and `BattleStats_SetEquipmentSlotByMappedId` `0031A510`, map the record back to its unit through `0031B860`. Record initialization writes equipment and licence state with the items layer's own setters, which find the owning unit through the same owner scan that the kind-1 path uses.

**Movement — CLIENT and SERVICE (12 edges).** `00335760` and `PartyFollow_SolveFormation` `00338490` read the free-target nibble `00263C20`. `00239210`, `00326D60`, `0033CB10` and `0033D890` resolve units through `0031B760`, `0031B770` and `0031B860`. In the service direction, the actor-record initializer `00265FF0`, which seeds the nibble to 4 or 5 (AL-3), calls five movement setters: `0026AA60`, `Movement_SetRequestedSpeed` `0026D6F0`, `003DA830`, `003DA860` and `003DA890`. `00237EA0`, one of the `+4`-band functions of §11, calls `002E64E0`. Movement reads unit identity and the target nibble through this page's accessors, and actor-record initialization also seeds movement defaults. Neither side changes the kind byte.

**Party — CLIENT and SERVICE (6 edges).** `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040` and `PartyFocus_SelectAndRequestDefaultActor` `00326500` resolve units through `0031B770`, and `0030BEB0` resolves through `0031B760`. The `+4`-band spawn functions of §11 ask the party layer about the leader and focus: `00233A20` calls `PartyFocus_IsCurrentPackedActorHandle` `003273B0`, and `00235AB0` and `00237EA0` call `BattleUnit_GetPartyLeader` `003272A0`. Party focus code reads units through these accessors, and the spawn-side band tests measure against the party leader.

**Rewards_Progression_Economy — SERVICE and CLIENT (5 edges).** `0023AC80` and `002398F0` level the record through the grower `0030C470`. The resource-availability check `00303BD0`, whose third pool the reader table on this page shows gated on kind 0, reads `GameState_GetGil` `00253690`. `Reward_ComputeExperienceForRecipient` `002F8BB0` and `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` resolve owners through `0031B860`. The kind byte gates which pools an action cost is checked against, one of the pools that check reads is the party's gil, and experience and levelling find a record's unit through the page's owner scan.

**Script_VM_Native_Bridge — CLIENT (7 edges).** The `btlAtelSetUnitType` verb `VM_BattleUnit_SetRuntimeUnitCategoryMode` `00510340` and `003528C0` pop their arguments through `VMValueStack_PopInt32CoerceFloat32` `00267E10`. `003528C0` stores the popped value through `00269FE0`, the nibble writer of AL-3. `0050F320` calls `00235AB0`, `00510300` calls `002392D0`, `0050F910` calls `002398F0` and `005102D0` calls `0031B760`. Script verbs set the free-target nibble and the runtime category mode that this page's readers classify, and they reach units through the same accessor. They do not write the kind byte, which is fixed at install.

**Spawn_Encounter_Lifecycle — CLIENT and SERVICE (28 edges).** Twenty-four spawn bodies resolve a unit through `0031B760`. Among them are `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0`, `SpawnEntry_GetDeathLimit` `00235EF0`, `SpawnEntry_GetCandidateUnitId` `00236030`, `SpawnUnit_BindEntryAndMarkCapTracked` `00239840` and `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410`. `Spawn_ApplyScriptSelectedUnit` `0023A3B0` calls the installer `0023A570` and `Spawn_PrepareRandomCandidateForCurrentEntry` `002355A0`, whose decode §12a starts from. `002355A0` calls `SpawnPoint_GeneratePositionFromAuthoredRegion` `00236450`, and `0023A570` resolves `SpawnKeep_ResolvePrimaryEntry` `00236100`. Kind-1 records live in spawn-keep entries, so the spawn layer is where they come from: its entry accessors are the main users of `0031B760`, and its script-selected apply is what installs a kind-1 unit.

**Status_Periodic_Terminal — CLIENT (7 edges).** `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860` calls the classifier `002F8E90`. `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` resolves through `0031B770`, and it is also one of §11's band readers, where in-band records take the extra path. Five status bodies resolve owners through `0031B860`: `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400`, `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690`, `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` and `00386860`. The periodic tick and the status mutators are readers of the classification and the owner resolve, and they write nothing to the byte.

**UI — CLIENT (18 edges).** Seven UI bodies read the free-target nibble `00263C20`, among them `BattleMenu_RecordSelectedTargetAndCursorContext` `0027D330`, `002C7660`, `003C5130` and `003C8B70`. The field-cursor helpers `002734F0`, `00273910` and `00273A00`, which accept nibble values 1 to 3, 3 and 5 as the AL-3 answer lists, are called by `002BFD20` and `002C0870`. `002734F0` itself calls `0035BAF0`, `0035BB00` and `0035BB60`, and `002C7660` calls `003229A0`. `BattleMenu_BuildCommandEntryList` `0031EB20` calls `002F9820` and `002FFCF0`, and `003C5130` calls `0031FE10`. Target cursors filter on the nibble, and the battle menu greys commands through the kind-aware cost and availability checks. The UI reads, never writes.

**WorldAreaField — SERVICE and CLIENT (3 edges).** `0023A570` calls the bit-15 predicate thunk `00313F60`, and `002FFCF0` calls `00377C20` itself. `BattleSystem_RunFieldFrameOrchestrator` `00234590` resolves a unit through `0031B770`. The area's action-permission bit enters the availability check next to the kind-dependent pools. The field frame is one more reader of the combatant-id resolve.

**CoreRuntimeScheduling and Save_Load_Settings — SERVICE and CLIENT (3 edges; added 2026-09-30, FABLE, for §5a).**
`BattleSystem_ResetRuntimeState` `00237DF0` (173 B) is the kind-0 owner transition of §5a.
- It calls two scheduling leaves. `00229ED0` (7 B) stores its argument to the global `01FD4A98` (`00237E83`), and
  `0032A160` (11 B) zeroes `0208D45C` (`00237E37`).
- It is entered from `SaveRuntime_RebindImageBackedGameplayState` `00238A80` (39 B). That function points `02EBF190`
  at the active save buffer + `0x4E68C` (`00238A92`), rebases the inventory, and tail-jumps into the reset
  (`00238AA2`).
So the forty party-table records whose kind byte the reset sets to 0 live in the save image, and rebinding a loaded
save re-runs the reset. None of the three edges reads or writes the kind byte.

## The `00233A20` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00233A20` (43 B) — gated float getter: `0030BE80(rcx)` zero →
`float[rbx+0x180]` (`00233A29`/`00233A32`), nonzero → the fallthrough
arm.

| member | role | interior |
| --- | --- | --- |
| `0030BE80` (~50 B) | eligibility predicate — `rcx` null → 0; `[rcx] & 8` clear → 0; `qword[+0x698]` null → 0; else `byte[+5]`-derived (`0030BE87`/`0030BE97`) | [`0030BE97`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-battle-record-kind-byte-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00235AB0` | 61 B | calls `003272A0()` and returns 0 when the result is null, when its qword `+0x698` is null, when byte `+5` of that record is non-zero, or when byte `+4` minus `0x1B` is above `0xC` as an unsigned byte; otherwise (byte `+5` zero and byte `+4` in `0x1B`-`0x27`) returns 1 | `00235AB4`, `00235ABE`, `00235ACA`, `00235AD8`, `00235ADC` |
| `0026AA60` | 97 B | takes the float `xmm1` and picks 3.141593 (`01CEBC50`) when it is at least 0.0, else -3.141593 (`00915620`); only when byte `+3` of `rcx` AND `0xE0` equals `0x60` it adds that offset, subtracts the truncated-to-integer quotient by 6.283185 (`01CEBC78`) times 6.283185, subtracts the offset again and stores the float at `+0xB0` of the object at qword `+0xB8` of `rcx`; otherwise it returns without a store | `0026AA6B`, `0026AA87`, `0026AA96`, `0026AAB0`, `0026AAB8` |
| `00273910` | 56 B | calls `00263C20` on the result of the call at `00273910` + 0x8 (made with the incoming `rcx` still in place) and returns 0 unless it returns 3; when it is 3, returns 1 if `003229A0` called with the incoming `ecx` returns 0, else 0 | `00273918`, `00273920`, `00273925`, `00273934`, `0027393D` |
| `0030BA80` | 67 B | calls `0031B770(rcx)` and returns 0 when it is null; returns 1 when bit 14 of the result's dword `+0` is set; otherwise returns 1 when its qword `+0x708` is non-zero and its word `+0x714` is at most `0x21E` (unsigned), else 0 | `0030BA84`, `0030BA93`, `0030BAA4`, `0030BAB3`, `0030BABC` |
| `003528C0` | 44 B | calls `00267E10(r9)` and `00269FE0(rdx, that result)`, then tail-jumps at `003528C0` + 0x27 with `ecx` = byte `+0x15` and `edx` = word `+0` of the incoming `rdx` object, both read after the two calls | `003528CC`, `003528D6`, `003528DB`, `003528DE`, `003528E7` |
