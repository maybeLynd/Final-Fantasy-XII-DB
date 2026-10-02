---
system: The battle stats record (BattleStatsRecord / BKBI, 0x1C8) — a field map from every reached accessor
category: 08-Combat-Formula
status: AUDITED
owner_layer: PrimaryOwner:CombatFormula — the fields belong to the pages that read their writers
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: a typed field scan over every function in functions.tsv, seeded by loads of unit +0x698
    and by the party array *(02EBF190)+8+k*0x1C8, propagated through call arguments and
    record-returning callees for three hops, control the HP write's read of +0x48 (found);
    every access row is published beside this page in battle-stats-record-accesses.tsv
last_reviewed: 2026-09-10
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-battle-stats-record-field-map-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# The battle stats record — a field map from every reached accessor

> Every number that makes a combatant what it is — level, HP, MP, the seven stats, the three
> status words, the two 128-bit layers, the affinity bytes, the equipment words, the timers, the
> experience — lives in one 456-byte record. Eleven pages read the functions that write it; the
> type store has no rows for it. This page puts every offset any reached function touches in one
> table, with its writers and readers, the name the owning page established, and the bytes nobody
> reaches.

## 1. What the player sees

The status screen is this record: the level and the seven stats, the HP and MP bars and their
maxima, the equipment, the statuses and the augments. What the screen does not show is also here —
the per-status parameters and timers, the licence bitmap, the affinity bytes, the charge count —
and all of it is one `0x1C8` block that an enemy carries inside its spawn record and a party
character in the battle-state array.

## 2. Native mechanism

### 2.1 How the accessors were found

The record is never addressed through a global of its own: a function either follows **unit
`+0x698`**, indexes **the party array** at `*(02EBF190) + 8 + k × 0x1C8`, or **receives the
record as an argument** from a function that did. `hop_scan.py` follows all three: a register
loaded from either seed is tracked through `mov` / `lea` / `add` until it is overwritten (or a
call, for volatile registers); every `[reg + disp]` it performs is a row; a tracked pointer sitting
in `rcx` / `rdx` / `r8` / `r9` at a `call` queues the callee with that argument pre-tracked; a
function that returns a tracked pointer in `rax` seeds its callers' `rax`. Three propagation hops
were run.

| | count |
|---|---|
| access rows | ~~1280 (807 at a seed, 473 through propagation)~~ 1,286 in the published TSV *(corrected 2026-10-02, OPUS: counted in battle-stats-record-accesses.tsv)* |
| functions reached | ~~284~~ 285 *(corrected 2026-10-02, OPUS: distinct functions in the published TSV)* |
| offsets touched | ~~85~~ 87 *(corrected 2026-10-02, OPUS: distinct displacements in the published TSV)* |
| control | `BattleStats_ModifyHPAndProcessLethalState` (`00300530`) reads `+0x48` — reached through `arg0`, found |
| excluded | `001CA600` (8,186 B), whose own `+0x698` is a different type |

**What the enumeration cannot see** (and the table therefore does not claim): accesses where the
record is the *index* register (`[rax + rbx + 0x194]` in the recompute's licence walk, `00310146`);
writers reached only from a route the seeds do not cover — `BattleStats_InitializeDefinitionRecord`
(`0023AC80`) takes the record from the spawn record's `+0x80` page and writes `+4`, `+0x50`,
`+0x58`, `+0x1C3`, `+0x1C5` ([the unit-definition page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.5); `00323790` writes `+0x190`
([the unit-definition page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.6); and anything below the third hop. The table's
"0 writers" therefore means *no writer on an enumerated route*, and the pages named in the name
column supply the rest.

> **What a census like this cannot see (2026-09-11, OPUS-NOTICE-CENSUSWRITES).** Seeds: loads of unit `+0x698`; the growers that build the record from the definition (`0030C470`, `0030C650`) are reached through the unit, but anything that fills the record before it is bound to a unit is not.
> A scan seeded on *accessors* reaches *consumers*: a constructor that builds the record before
> any accessor can return it is reached only if it is seeded on its own. So the **reads** below are
> the well-covered side and the **writes** are under-covered wherever a constructor or an
> index-derived writer sits outside the seeds — do not rest an absence-of-writer claim on this
> TSV alone; pair it with a displacement scan of the candidate writers.
>
> **The kind-1 home now has its own census path (2026-09-17, SWE2-STRUCT).** `SpawnRecord +0x80`
> is declared as one typed `battleStats` field in the store, and `check_census_widths.py`'s
> `SUBOBJECT_CENSUS` rebases `spawn-record-accesses.tsv` by `0x80` onto this type — the accesses
> the spawn census recorded inside the keep entry's stats page are checked against these same
> rows, alongside this page's own TSV. A type carried in two census tables is checked twice,
> once per home, so the blind spot above narrows to writers neither census seeds.

### 2.2 The field map

Width is the most common operand size at that offset; "w / r" counts distinct functions.

| offset | width | type | name (owning page) | w / r | writers | readers |
|---|---|---|---|---|---|---|
| `+0x000` | 4 |  | *not named by any page* | 1 / 4 | `00328FB0` (`00328FD5` +1) | `BattleUnit_SelectAndCommitNextAction` `00305AB0` (`00305BFB`); `0030BCD0` (`0030BCE9`); +2 more |
| `+0x004` | 1 | u8 | **definition row index (the id's low byte)** ([page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)) | 0 / 73 |  | `00233A20` (`00233A60`); `00235A70` (`00235A92`); +71 more |
| `+0x005` | 1 | u8 | **kind byte = the id's class byte (0 party, 1 spawn-backed)** ([page](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md)) | 0 / 172 |  | `00233A20` (`00233A58`); `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (`00233B9B`); +170 more |
| `+0x006` | 2 | s16 | **the secondary resource `00300BC0` moves; cap `+0x28 × (+0x37 or 1)`** ([page](../../10-Status-Periodic-Terminal/where-mp-comes-from.md)) | 2 / 8 | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310594`); `BattleStats_ModifySecondaryResource` `00300BC0` (`00300C6A`) | `0030D550` (`0030D5E3`); `0030D810` (`0030D87A`); +6 more |
| `+0x008` | 4 | u32 | **base HP stat, from party row `w_16`; grown per level** ([page](../../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md)) — the party arm of a union by `+0x05`: spawn-backed → **i16 Strength modifier** at `+0x08`, added to `.ard` column `+0x26` (`002FF245`), with the Magick Power modifier at `+0x0A` ([where a stat number comes from](../where-a-stat-number-comes-from.md), `CB-5`) | 4 / 4 | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE156`); `0030C470` (`0030C500`); `BattleFormula_ApplyTargetResult` `003112F0` (`003118BB`); +1 more | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE132`); `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`00306A65`); +2 more |
| `+0x00A` | 2 | i16 · u32 high half | spawn-backed → **i16 Magick Power modifier** (`002FF265`, [where a stat number comes from](../where-a-stat-number-comes-from.md) `CB-5`); party → the high half of the u32 at `+0x08` | 2 / 2 | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE1CE`); `BattleFormula_ApplyTargetResult` `003112F0` (`003118D9`) | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE1AA`); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF265`) |
| `+0x00C` | 2 | ~~u16~~ s16 *(corrected 2026-10-02, OPUS: the rebuild sign-extends it, `002FF084` `movsx ecx, word ptr [rdi + 0xc]`)* | **base MP stat, from row `w_1A`; grown per level** ([page](../../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md)); spawn-backed → **i16 Vitality modifier** (`002FF27C`, `CB-5`) | 3 / 3 | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE222`); `0030C470` (`0030C507`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C753`) | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE1FE`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C735`); +1 more |
| `+0x00E` | 2 | i16 | spawn-backed → **i16 Speed modifier** (`002FF293`, [where a stat number comes from](../where-a-stat-number-comes-from.md) `CB-5`); party → not read by the rebuild | 1 / 2 | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE276`) | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE252`); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF293`) |
| `+0x010` | 4 / 2 | f32 · i16 | **union, by the kind byte `+0x05` alone** (`002FEFFB`, `test ecx, ecx` at `002FF026`; the type range `0x1B`–`0x27` tested beside it at `002FF007`–`002FF00F` is a separate flag — see `+0x24`): party → ~~float stat 1~~ **f32 stat 1 - the base Strength** (stored to `+0x2A` by the stat rebuild, capped at 99; `_index/candidates/exp-level-stats-fable/`, 2026-09-29 FABLE) from row `b_1E`, grown by `002F9BD0` with row `b_1F` ([page](../../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md)), read `cvttss2si` at `002FF0C2`; spawn-backed → **i16 Attack modifier** read `movsx` at `002FF2E6` — CORRECTED 2026-09-11 (OPUS-CONTRA-STATUNION) | 3 / 3 | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE3CB`); `0030C470` (`0030C516`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C760`) | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE3A6`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C74B`); +1 more |
| `+0x012` | 2 | i16 · f32 high half | spawn-backed → **i16 Defence modifier** (`002FF2C1`; `BattleFormula_ApplyTargetResult` adds the result's `+0x122` delta here, `003118F7`); party → the high half of the f32 at `+0x10` | 2 / 2 | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE31F`); `BattleFormula_ApplyTargetResult` `003112F0` (`003118F7`) | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE2FA`); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF2C1`) |
| `+0x014` | 4 / 2 | f32 · i16 | union: party → **f32 stat 2 - the base Magick Power** (stored to `+0x2B` by the stat rebuild, capped at 99; `_index/candidates/exp-level-stats-fable/`, 2026-09-29 FABLE) from row `b_21`, growth `b_22` ([page](../../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md)), `cvttss2si` `002FF0CD`; spawn-backed → **i16 Magick Resist modifier** `movsx` `002FF2E0` (the applier adds the result's `+0x124` delta here, `00311915`) | 4 / 3 | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE375`); `0030C470` (`0030C526`); `BattleFormula_ApplyTargetResult` `003112F0` (`00311915`); +1 more | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE350`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C76C`); +1 more |
| `+0x016` | 2 | i16 · f32 high half | spawn-backed → **i16 innate evade modifier** (`002FF2AA`); party → the high half of the f32 at `+0x14` | 0 / 1 |  | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF2AA`) |
| `+0x018` | 4 / 2 | f32 · i16 | union: party → **f32 stat 3 - the base Vitality** (stored to `+0x2C` by the stat rebuild, capped at 99; `_index/candidates/exp-level-stats-fable/`, 2026-09-29 FABLE) from row `b_24`, growth `b_25` ([page](../../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md)), `cvttss2si` `002FF099`; spawn-backed → **i16 parry modifier** `movsx` `002FF20A` | 3 / 3 | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE420`); `0030C470` (`0030C536`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C78C`) | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE3FC`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C782`); +1 more |
| `+0x01A` | 2 | i16 · f32 high half | spawn-backed → **i16 block modifier** (`002FF20F`); party → the high half of the f32 at `+0x18` | 1 / 2 | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE474`) | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE450`); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF20F`) |
| `+0x01C` | 4 / 2 | f32 · i16 | union: party → **f32 stat 4 - the base Speed** (stored to `+0x2D` by the stat rebuild, capped at 99; `_index/candidates/exp-level-stats-fable/`, 2026-09-29 FABLE) from row `b_27`, growth `b_28` ([page](../../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md)), `cvttss2si` `002FF0B7`; spawn-backed → **i16 magick evade modifier** `movsx` `002FF23D` | 3 / 3 | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE4C8`); `0030C470` (`0030C546`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C7A2`) | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE4A4`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C798`); +1 more |
| `+0x01E` | 2 | i16 · f32 high half | spawn-backed → **i16 total-evade modifier** (`002FF2D6`, feeds `+0x35`); party → the high half of the f32 at `+0x1C`; `BattleFormula_DispatchPostResultEvents` compares the byte at `+0x1E` with 2 (`0046A444`) on the action row, not here | 1 / 3 | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE2CA`) | `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (`002FE2A6`); `BattleFormula_DispatchPostResultEvents` `00469EC0` (`0046A444` +2); +1 more |
| `+0x020` | 1 | u8 | **`max(row.b_46, licence-derived rank)`** ([page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)) — party arm; spawn-backed → **i16 total-magick-evade modifier** over `+0x20`–`+0x21` (`002FF2F1`, feeds `+0x36`; `CB-5`) | 1 / 1 | `0030C470` (`0030C54F` +1) | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF0AA` +1) |
| `+0x024` | 4 | s32 | **max HP (the rebuild's output block starts here)** — `clamp(sum, 1, cap)`: cap **9,999** for party records, ~~**999,999,999**~~ **1,000,000,000** for the rest *(corrected 2026-10-02, OPUS: checked at `002FF7BB`–`002FF7C8`, `mov eax, 0x3b9aca00` / `cmove eax, r8d`; CONTRACT-stat-derivation.md D-3)* (`002FF7B1`–`002FF7E2`), and **32,767 for party rows `0x1B`–`0x27`** (the flag from `002FF007`–`002FF00F`, re-clamped at `002FF7E5`–`002FF805`) — the thirteen rows above the guest range 7–25 ([party page](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) §3): by count, the Espers ([page](../Current-HP/the-hp-write-and-the-lethal-transition.md)) | 1 / 18 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FEFB9` +2) | `002FE950` (`002FE988`); `AiOrder_EvaluateTargetSelector` `00301AD0` (`00302246` +1); +16 more |
| `+0x028` | 2 | s16 | **MP capacity (max MP)** ([page](../../10-Status-Periodic-Terminal/where-mp-comes-from.md)) | 1 / 20 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF824`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`0030200E` +2); `BattleAction_ConsumeExecutionResources` `00305640` (`00305704`); +18 more |
| `+0x02A` | 1 | u8 | **Strength** ([page](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md)) | 1 / 2 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF840`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`00302020`); `BattleFormula_ApplyTargetResult` `003112F0` (`003118AE`) |
| `+0x02B` | 1 | u8 | **Magick Power** ([page](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md)) | 1 / 2 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF85A`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`00302048`); `BattleFormula_ApplyTargetResult` `003112F0` (`003118CC`) |
| `+0x02C` | 1 | u8 | **Vitality** ([page](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md)) | 1 / 3 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FEFBC` +1) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`00302070`); `BattleAction_CheckUnitActionAvailability` `00306480` (`00306495`); +1 more |
| `+0x02D` | 1 | u8 | **Speed** ([page](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md)) | 1 / 2 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF88E`) | `BattleAction_ComputeChargeLimitTicks` `002F8410` (`002F869F`); `AiOrder_EvaluateTargetSelector` `00301AD0` (`00302098`) |
| `+0x02E` | 1 | u8 | **Attack** ([page](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md)) | 1 / 1 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF8F2`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`00301F16`) |
| `+0x02F` | 1 | u8 | **Defence** ([page](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md)) | 1 / 2 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF90C`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`00301F56`); `BattleFormula_ApplyTargetResult` `003112F0` (`003118EA`) |
| `+0x030` | 1 | u8 | **Magick Resist** ([page](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md)) | 1 / 2 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF921`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`00301F76`); `BattleFormula_ApplyTargetResult` `003112F0` (`00311908`) |
| `+0x031` | 1 | u8 | **innate evade, 0–100** — the roller's third band (`02AEDFEC`, `003890AB`; [the scratch block](../Scratch-Block/the-formula-scratch-block.md) §2.3): the party definition's byte `+0x2A` (`002FF095`) or the `.ard` column `+0x2A` (`002FF2A1`–`002FF2B4`), (area units add the modifier word `+0x16`); clamped at `002FF936` | 1 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF936`) |  |
| `+0x032` | 1 | u8 | **weapon evade (parry), 0–100** — the roller's second band (`02AEDFF4`, `003890A1`): every kind-1 item's row byte `+0x1D` (`002FF48E`–`002FF4A4`), or `.ard` column `+0x2E` under definition `+0x15` bit 0, (area units add the modifier word `+0x18`); clamped at `002FF949` | 1 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF949`) |  |
| `+0x033` | 1 | u8 | **shield evade (block), 0–100** — the roller's first band (`02AEDFF0`, `00389097`): every kind-2 item's row byte `+0x18` (`002FF477`–`002FF483`), or `.ard` column `+0x02` under definition `+0x15` bit 1, (area units add the modifier word `+0x1A`); clamped at `002FF95B` | 1 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF95B`) |  |
| `+0x034` | 8 | u8 | **magick evade, 0–100** — kind-2 (shield) row byte `+0x19` (`002FF486`–`002FF48A`) or `.ard` column `+0x03` under `+0x15` bit 1, (area units add the modifier word `+0x1C`); clamped at `002FF96D` (the width 8 is the rebuild's zeroing of `+0x34`–`+0x3B` at `002FEFC0`) | 1 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FEFC0` +1) |  |
| `+0x035` | 1 | u8 | **total evade, 0–100** — shield + weapon + innate evade (area units add the modifier word `+0x1E`) (`002FF79A`–`002FF7A5`, clamp `002FF8B6`); written, not read by the roller | 1 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF8B6`) |  |
| `+0x036` | 1 | u8 | **total magick evade, 0–100** — magick evade (area units add the modifier word `+0x20`) (`002FF7A7`–`002FF7AE`, clamp `002FF8D2`) | 1 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF8D2`) |  |
| `+0x037` | 1 | u8 | **the MP multiplier (bars); 0 reads as 1** ([page](../../10-Status-Periodic-Terminal/where-mp-comes-from.md)) | 1 / 6 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF89F`) | `BattleSpecialSequence_BuildRandomizedCandidateActions` `002F88B0` (`002F895E`); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031054F` +1); +4 more |
| `+0x038` | 4 | u32 | **status word 3 (mode-2 clear; refuses when set)** ([page](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md)) | 2 / 1 | `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (`0030E564`); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF0D3` +1) | `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (`0030E513` +2) |
| `+0x03C` | 4 | u32 | **status word 2; presence = `+0x3C | +0x64`** ([page](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md)) | 2 / 126 | `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (`0030E50E` +1); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FEFC4` +2) | `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (`00233BBA`); `00233D70` (`00233D9C`); +124 more |
| `+0x040` | 1 | u8 | **affinity: weak (×2)** ([page](../elemental-affinity-and-the-five-bytes.md)) | 2 / 3 | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310443`); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF2FE` +1) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`003023AE`); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310480`); +1 more |
| `+0x041` | 1 | u8 | **affinity: absorb** ([page](../elemental-affinity-and-the-five-bytes.md)) | 2 / 3 | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310451`); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF306` +1) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`003023D2`); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031048E`); +1 more |
| `+0x042` | 1 | u8 | **affinity: resist (×0.5)** ([page](../elemental-affinity-and-the-five-bytes.md)) | 2 / 2 | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031045F`); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF30E` +1) | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031049C`); `00329220` (`003294D2`) |
| `+0x043` | 1 | u8 | **affinity: immune** ([page](../elemental-affinity-and-the-five-bytes.md)) | 2 / 2 | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031046D`); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF316` +1) | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`003104AA`); `00329220` (`003294DD`) |
| `+0x044` | 1 | u8 | **affinity: the source's ×1.5** ([page](../elemental-affinity-and-the-five-bytes.md)) | 2 / 2 | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031047B`); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FEFC8` +2) | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`003104B8`); `00329220` (`003294E8`) |
| `+0x048` | 4 | s32 | **current HP** ([page](../Current-HP/the-hp-write-and-the-lethal-transition.md)) | 2 / 22 | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310508`); `BattleStats_ModifyHPAndProcessLethalState` `00300530` (`00300749`) | `002FE950` (`002FE995`); `AiOrder_EvaluateTargetSelector` `00301AD0` (`00301FDE` +5); +20 more |
| `+0x04C` | 2 | s16 | **live MP; starts at `+0x28 × row.b_47 / 100` for a party character** ([page](../../10-Status-Periodic-Terminal/where-mp-comes-from.md)) | 3 / 13 | `0030C470` (`0030C5CB` +1); `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`0031053D`); `BattleStats_ModifyPrimaryResource` `00300CE0` (`00300E00`) | `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400` (`002F94FD`); `BattleAction_CheckExecutionResourceAvailability` `00303BD0` (`00303C20`); +11 more |
| `+0x04E` | 1 | u8 | **charge count `+0x06 / +0x28`** — the whole max-MP units the secondary pool holds; a kind-5 / 6 action needs its row `+0x0A` of them (availability reason `0x14`, `00303C4B`) and Consume takes `max × +0x0A` from `+0x06` (`0030570D`) (0 when `+0x37` is 0; stored on every reconcile even when unchanged, `0030E111`; the reaction publisher fires on a change only under flags `0x400` without `0x10`) ([page](../the-auto-status-rebuild.md), [MP](../../10-Status-Periodic-Terminal/where-mp-comes-from.md)) | 1 / 5 | `0030E060` (`0030E111`) | `BattleSpecialSequence_BuildRandomizedCandidateActions` `002F88B0` (`002F895A`); `BattleAction_CheckExecutionResourceAvailability` `00303BD0` (`00303C4B`); +3 more |
| `+0x050` | 2 | u16[5] | **equipment slots 0–4 (`0xFFFF` empty); `+0x50 = −1` qword at init** ([page](../../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md)) | 0 / 15 |  | `BattleAction_ComputeChargeLimitTicks` `002F8410` (`002F84BF` +1); `BattleAction_ComputeChargeProgressStep` `002F9C00` (`002F9C90`); +13 more |
| `+0x052` | 2 |  | inside `+0x50` — equipment slots 0–4 (`0xFFFF` empty) ([page](../../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md)) | 0 / 4 |  | `BattleAction_ComputeChargeProgressStep` `002F9C00` (`002F9CF9`); `0031BDC0` (`0031BE0B`); +2 more |
| `+0x054` | 2 |  | inside `+0x50` — equipment slots 0–4 (`0xFFFF` empty) ([page](../../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md)) | 0 / 3 |  | `BattleAction_ComputeChargeProgressStep` `002F9C00` (`002F9D62`); `AiOrder_EvaluateTargetSelector` `00301AD0` (`00302620`); +1 more |
| `+0x056` | 2 |  | inside `+0x50` — equipment slots 0–4 (`0xFFFF` empty) ([page](../../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md)) | 0 / 2 |  | `BattleAction_ComputeChargeProgressStep` `002F9C00` (`002F9DCB`); `00329220` (`0032971C`) |
| `+0x058` | 2 |  | inside `+0x50` — equipment slots 0–4 (`0xFFFF` empty) ([page](../../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md)) | 0 / 2 |  | `BattleAction_ComputeChargeProgressStep` `002F9C00` (`002F9E39`); `00329220` (`0032972A`) |
| `+0x05A` | 2 |  | *not named by any page* | 0 / 1 |  | `00329220` (`00329738`) |
| `+0x05C` | 4 | u32 | ~~**written and read only by `BattleFormula_AdvanceStatusTimersAndBuildResult`**~~ *(Corrected 2026-09-27, FABLE, Claude Opus 5.5: no stats-record access. The three census rows are `[r14 + r12 − 0x60]` = the result record's `+0x5C + 4i`, FE-3. With `+0x60`–`+0x63`, `+0x5C`–`+0x63` is an 8-byte region no code touches, FE-4.)* | 1 / 1 | `BattleFormula_AdvanceStatusTimersAndBuildResult` `00386C70` (`00386E43` +1) | `BattleFormula_AdvanceStatusTimersAndBuildResult` `00386C70` (`00386E56`) |
| `+0x064` | 4 | u32 | **status word 1 (mode-0 clear / mode-3 set)** ([page](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md)) | 1 / 124 | `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (`0030E4F8` +1) | `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (`00233BB7`); `00233D70` (`00233D99`); +122 more |
| `+0x068` | 0 | u8[16] | **the mutable status layer (128 bits)** ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 1 |  | `00329220` (`0032942C` +1) |
| `+0x069` | 1 |  | inside `+0x68` — the mutable status layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 2 |  | `00329220` (`0032948E`); `003202F0` (`00320364`) |
| `+0x06A` | 1 |  | inside `+0x68` — the mutable status layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 3 |  | `BattleAction_ComputeTargetPrimaryResourceGainFromHpDamage` `002F91A0` (`002F9204`); `BattleAction_ComputeCasterPrimaryResourceGainFromHpDamage` `002F9240` (`002F9330` +1); +1 more |
| `+0x06B` | 1 |  | inside `+0x68` — the mutable status layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 2 |  | `002FAFD0` (`002FB05D` +1); `00329220` (`003294A4`) |
| `+0x06C` | 1 |  | inside `+0x68` — the mutable status layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 17 |  | `BattleUnit_TryTriggerNearbyAuthoredFieldAction` `002F8060` (`002F80DA`); `BattleAction_ComputeModifiedResourceCostAmount` `002F95D0` (`002F9674` +1); +15 more |
| `+0x06E` | 1 |  | inside `+0x68` — the mutable status layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 2 |  | `BattleAction_ComputeChargeLimitTicks` `002F8410` (`002F85A6` +1); `BattleAction_ComputeModifiedResourceCostAmount` `002F95D0` (`002F97A3`) |
| `+0x072` | 1 |  | inside `+0x68` — the mutable status layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 1 |  | `BattleAction_ComputeCasterPrimaryResourceGainFromHpDamage` `002F9240` (`002F92C1`) |
| `+0x073` | 1 |  | inside `+0x68` — the mutable status layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 2 |  | `BattleAction_ComputeChargeLimitTicks` `002F8410` (`002F8731` +1); `BattleAction_ComputeModifiedResourceCostAmount` `002F95D0` (`002F9688` +2) |
| `+0x074` | 1 |  | inside `+0x68` — the mutable status layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 1 |  | `BattleAction_ComputeChargeLimitTicks` `002F8410` (`002F8803`) |
| `+0x076` | 1 |  | inside `+0x68` — the mutable status layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 1 |  | `BattleAction_ComputeAuthoredStatusMask` `003872D0` (`00387412` +2) |
| `+0x078` | 1 | u8[16] | **the derived augment layer (128 bits)** ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 2 |  | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310303` +2); `00329220` (`00329480`) |
| `+0x079` | 1 |  | inside `+0x78` — the derived augment layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 3 |  | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`00310319`); `00329220` (`0032948A`); +1 more |
| `+0x07A` | 1 |  | inside `+0x78` — the derived augment layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 3 |  | `BattleAction_ComputeTargetPrimaryResourceGainFromHpDamage` `002F91A0` (`002F920A`); `BattleAction_ComputeCasterPrimaryResourceGainFromHpDamage` `002F9240` (`002F9336` +1); +1 more |
| `+0x07B` | 1 |  | inside `+0x78` — the derived augment layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 2 |  | `002FAFD0` (`002FB063` +1); `00329220` (`003294A0`) |
| `+0x07C` | 1 |  | inside `+0x78` — the derived augment layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 17 |  | `BattleUnit_TryTriggerNearbyAuthoredFieldAction` `002F8060` (`002F80E4`); `BattleAction_ComputeModifiedResourceCostAmount` `002F95D0` (`002F967E` +1); +15 more |
| `+0x07E` | 1 |  | inside `+0x78` — the derived augment layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 2 |  | `BattleAction_ComputeChargeLimitTicks` `002F8410` (`002F85AC` +1); `BattleAction_ComputeModifiedResourceCostAmount` `002F95D0` (`002F97C7`) |
| `+0x082` | 1 |  | inside `+0x78` — the derived augment layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 1 |  | `BattleAction_ComputeCasterPrimaryResourceGainFromHpDamage` `002F9240` (`002F92C7`) |
| `+0x083` | 1 |  | inside `+0x78` — the derived augment layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 2 |  | `BattleAction_ComputeChargeLimitTicks` `002F8410` (`002F8747` +1); `BattleAction_ComputeModifiedResourceCostAmount` `002F95D0` (`002F968E` +2) |
| `+0x084` | 1 |  | inside `+0x78` — the derived augment layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 1 |  | `BattleAction_ComputeChargeLimitTicks` `002F8410` (`002F8809`) |
| `+0x086` | 1 |  | inside `+0x78` — the derived augment layer (128 bits) ([page](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) | 0 / 1 |  | `BattleAction_ComputeAuthoredStatusMask` `003872D0` (`00387419` +2) |
| `+0x088` | 52 / 1 | `GambitConfig` · u8 | **union, by the kind byte `+0x05` alone** (`00327CC3`, `movzx eax, byte ptr [rcx + 5]` / `test eax, eax` / `jne` - the loader does nothing when it is non-zero): party -> **the gambit block**, a `GambitConfig` - twelve 4-byte slots from `+0x88` (`00327D57`, `00327D64`), a u16 enable mask at `+0xB8` maintained with `bts` (`00327D6C`-`00327D78`), a **u8** filled-count at `+0xBA` (`00327D84`), twelve bound at `00327D8A`; the base is confirmed a second way by the tail clear's `lea rcx, [rdi + (i + 0x22)*4]` at `00327D8F`, since `(i + 0x22) * 4 == i*4 + 0x88`. Read back by the runtime rebuild `00327DE0`, which indexes `02089378` by the record's `+0x04` at stride `0x170` and so rebuilds an `AiOrderSet` from it. Spawn-backed -> **the level grower's third argument (1 on the enemy branch)** ([page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)), and nothing is established about `+0x89`-`+0xBB` on that arm - ADDED 2026-09-11 (FABLE-REQ-OPUS-STATS88), verified against the binary before recording | 1 / 5 | `0030C470` (`0030C4B1`) | `Reward_ComputeExperienceForRecipient` `002F8BB0` (`002F8C6A` +1); `Reward_ComputeLicensePointsForRecipient` `002F90C0` (`002F9122`); +3 more |
| `+0x0BC` | 4 | u32[32] | **per-status remaining duration — or the Petrify / Doom count** (modes 0 / 3; default `00387730`: `status_data +8` × Vitality factor × frame base × 300, or 11); spent by the periodic tick's stage 2 `00386C70` through a record-relative address the typed scan cannot follow, `−10` per tick, written back through the result record's `+0x5C`; the two listed readers and the display record show `count − 1` for ids 2 / 6 ([page](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) §2.4a) | 1 / 4 | `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (`0030E594`) | `0031FC70` (`0031FCC4`); `00320CF0` (`00320D2D`); +2 more |
| `+0x13C` | 2 | u16[32] | **per-status beat timer, modes 0 / 3** — `status_data +9` × frame base × 30, `−10` per tick in `00386C70` (record-relative, not in the typed scan); on expiry Poison / Sap / Regen land and the Petrify / Doom count steps; written back through the result record's `+0xDC` ([page](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) §2.4a) | 1 / 0 | `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (`0030E5AF`) |  |
| `+0x17C` | 2 | s16[8] | **~~the status duration timers~~ the eight effect-slot timers (stage 3's countdown, keyed by the effect table; not the 32 statuses' durations, which are `+0xBC`), which the applier copies from its `+0x42`–`+0x50`** *(renamed 2026-09-29, FABLE; `_index/candidates/pkg-gp-status-poison/timers.md`)* ([page](../../07-Combat-Action/applying-a-result-to-a-target.md)) | 2 / 1 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311824`); `BattleStats_UpdateStatusAuxiliaryValue` `0030EA40` (`0030EAB9`) | `BattleFormula_AdvanceStatusLinkedAuxTimers` `00385570` (`00385625`) |
| `+0x17E` | 2 |  | inside `+0x17C` — ~~the status duration timers~~ the effect-slot timers the applier copies from its `+0x42`–`+0x50` ([page](../../07-Combat-Action/applying-a-result-to-a-target.md)) | 1 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311834`) |  |
| `+0x180` | 2 |  | inside `+0x17C` — ~~the status duration timers~~ the effect-slot timers the applier copies from its `+0x42`–`+0x50` ([page](../../07-Combat-Action/applying-a-result-to-a-target.md)) | 1 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311844`) |  |
| `+0x182` | 2 |  | inside `+0x17C` — ~~the status duration timers~~ the effect-slot timers the applier copies from its `+0x42`–`+0x50` ([page](../../07-Combat-Action/applying-a-result-to-a-target.md)) | 1 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311854`) |  |
| `+0x184` | 2 |  | inside `+0x17C` — ~~the status duration timers~~ the effect-slot timers the applier copies from its `+0x42`–`+0x50` ([page](../../07-Combat-Action/applying-a-result-to-a-target.md)) | 1 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311864`) |  |
| `+0x186` | 2 |  | inside `+0x17C` — ~~the status duration timers~~ the effect-slot timers the applier copies from its `+0x42`–`+0x50` ([page](../../07-Combat-Action/applying-a-result-to-a-target.md)) | 1 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311874`) |  |
| `+0x188` | 2 |  | inside `+0x17C` — ~~the status duration timers~~ the effect-slot timers the applier copies from its `+0x42`–`+0x50` ([page](../../07-Combat-Action/applying-a-result-to-a-target.md)) | 1 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311884`) |  |
| `+0x18A` | 2 |  | inside `+0x17C` — ~~the status duration timers~~ the effect-slot timers the applier copies from its `+0x42`–`+0x50` ([page](../../07-Combat-Action/applying-a-result-to-a-target.md)) | 1 / 0 | `BattleFormula_ApplyTargetResult` `003112F0` (`00311894`) |  |
| `+0x18C` | 4 | u32 | **accumulated experience, `[0, 99,999,999]`** ([page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)) | 1 / 1 | `0030C470` (`0030C586`) | `00329220` (`003296B9`) |
| `+0x190` | 4 | u32 | **accumulated LP, `[0, 99,999]`, setter `00323790`** ([page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)) | 0 / 1 |  | `00329220` (`003296DA`) |
| `+0x1C2` | 1 | u8 | **level, `[0, 99]`** ([page](../../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md)) | 2 / 14 | `0030C470` (`0030C496`); `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` (`0030C7BB`) | `Reward_ComputeExperienceForRecipient` `002F8BB0` (`002F8C63` +1); `Reward_ComputeLicensePointsForRecipient` `002F90C0` (`002F911B`); +12 more |
| `+0x1C3` | 1 | u8 | **licence-board selector A**, `[0, 0xB]`, `0xFF` = none — party only (§2.3b) | 3 / 2 | `BattleStats_SetLicenseBoardSelectorAAndActive` `00323740` (`00323772`); `BattleStats_InitializeDefinitionRecord` `0023AC80` (`0023ACD5`, the `0xFFFF` sentinel over `+0x1C3`–`+0x1C4`); `00328BD0` (`00328D52`, same sentinel) | `BattleStats_GetLicenseBoardSelectorA` `00323670` (`0032369B`); `BattleStats_ReconcileActiveLicenseBoardSelector` `003242F0` (`0032431B`) |
| `+0x1C4` | 1 | u8 | **licence-board selector B**, same domain and guards | 1 / 2 | `BattleStats_SetLicenseBoardSelectorBAndActive` `003236F0` (`00323722`) | `BattleStats_GetLicenseBoardSelectorB` `00323630` (`0032365B`); `003242F0` (`0032432A`) |
| `+0x1C5` | 1 | u8 | **the active selector** — which of A / B the board shows | 5 / 2 | both setters (`00323779`, `00323729`); `BattleStats_ReconcileActiveLicenseBoardSelector` `003242F0` (`00324341`, `0032434B`); the initialisers `0023AC80` (`0023ACDD`) and `00328BD0` (`00328D5D`), both `0xFF` | `BattleStats_GetActiveLicenseBoardSelector` `003236B0` (`003236DB`); `003242F0` (`00324336`) |

> **CORRECTED 2026-09-11 (OPUS-CONTRA-STATUNION).** The span `+0x10`–`+0x1F` is **not four fixed
> f32 fields**. `BattleStats_RebuildEffectiveStatsAndAffinityState` (`002FEF30`) reads the kind byte
> `+0x05` at `002FEFFB` and, when it is 0 (party — `test ecx, ecx` / `jne` at `002FF026`–`002FF028`;
> the discriminator is the kind byte **alone**, corrected 2026-09-11, OPUS-REQ-FABLE-UNION2),
> takes the arm that converts **four f32** at `+0x10` / `+0x14` / `+0x18` /
> `+0x1C` (`cvttss2si`, `002FF099`–`002FF0CD`); every other record takes the arm that sign-extends
> **eight i16** at `+0x10` … `+0x1E` (`002FF20A`–`002FF2F1`). The growers `0030C470` / `0030C650`
> write the floats on the party path only (kind 0, §"kind 0: base stats" of the definition page);
> **Both arms re-read 2026-09-19 (FABLE), on `OPUS-REQ-FABLE-STATSREC-BASEHP-PAIR`.** The rebuild loads the kind byte and
> branches on it (`002FF026`). **Kind 0:** the *dword* `+0x08` goes to the HP growth routine with the party row's two
> growth bytes (`002FF078`), and its writer `0030C500` stores the party row's word `+0x16` zero-extended **as a dword** -
> base HP is there from a write. **Any other kind:** the sign-extended *words* `+0x08` and `+0x0A` are added to the
> Strength and Magick Power sums (`002FF245`, `002FF265`). The -99..+99 clamp belongs to the modifiers' writers:
> direct-state command `0x4158` adds the action's signed word to `+0x08`, `0x4159` to `+0x0A`, and the jump table at
> `002FE628` shows `0x4159`..`0x4162` are a run of such arms `0x54` bytes apart (the next two land on `+0x0C` and `+0x0E`).
> ~~*Neither those arms nor the result applier's deltas test the kind - `FE-6` stays open.*~~ *Corrected 2026-09-26 (FABLE, Claude Opus 5.5): the applier's deltas do test it. `0031189B` `cmp byte ptr [rdi + 5], 1` / `jne` skips all four adds unless the kind is 1, which is `FE-6`'s answered first half. The direct-state arms do not: `0x4158`–`0x415C` and `0x4160`–`0x4162` add a clamped signed word to `+0x08`, `+0x0A`, `+0x0C`, `+0x0E`, `+0x1E`, `+0x18`, `+0x1A` and `+0x1C` and recompute, with no kind test. Whether an order can reach a party record, whose dword `+0x08` is base HP, is a separate question, `FE-7`. Control: `_index/candidates/fe6-kind-gates/kind_gates.py`.*
> *`FE-7` answered 2026-09-27 (FABLE, Claude Opus 5.5): no shipped path reaches a party record.*
> - *The arms change the committing unit's own record; they have no target.*
> - *A party unit's order sets are three static sets plus its rebuilt gambit set, and the shipped gambit presets carry
>   no order id.*
> - *The eight orders ship in only three records, all in one enemy set (`bhm_d.ard` set 0).*
> - *Not read: the candidate lists of the gambit editor and the battle menu, and whether a restored save's gambit block
>   is checked. An order id arriving through either would be applied to a party record unchecked, and `0x4158` would
>   add into half of its base HP.*
>
> *Detail: `FE-7` in the register; control `_index/candidates/fe7-order-reach/fe7_order_reach.py`.*
>
> `BattleUnit_ExecuteDirectStateCommandOrder` (`002FDDA0`) reads and writes the span as words. The
> rows above now carry both shapes; a reconstruction must switch on the kind before touching them.
> One consumer to audit: `BattleFormula_ApplyTargetResult` adds i16 deltas at `+0x0A` / `+0x12` /
> `+0x14` (`003118D9`, `003118F7`, `00311915`) ~~with no kind test in sight (`FE-6`)~~ behind the kind test `0031189B` (`cmp byte ptr [rdi + 5], 1` / `jne`), so on foe records only *(corrected 2026-10-02, OPUS: checked at `0031189B`–`0031189F`; the `FE-6` correction above)*. The
> accesses TSV was right throughout — the instruction forms are the evidence. The type-range test
> beside the kind byte (`+0x04 − 0x1B ≤ 0xC`, `002FF007`–`002FF00F`) is **not** part of the
> discriminator: both of its outcomes fall into the same `test ecx, ecx`. It sets a stack flag
> (`[rsp+0x5C]` = 1 at `002FF011`, 0 at `002FF021`) that the max-HP clamp reads at `002FF7E5`
> (row `+0x24`).

### 2.3 What nobody reaches

Offsets with no access on any enumerated route, once the named arrays (`+0x50` ×5 words, the two
layers, `+0xBC[32]`, `+0x13C[32]`, `+0x17C[8]`, the `+0x194` bitmap of 361 bits) are counted as
covered — **as this section originally read them, by exact displacement**: `+0x21`–`+0x23` (3 B),
`+0x45`–`+0x47` (3 B), `+0x4F` (1 B), `+0x60`–`+0x63` (4 B), `+0x89`–`+0xBB` (51 B),
`+0x1C3`–`+0x1C7` (5 B). **Four of the six are not untouched** — §2.3a shows two from this page's own accesses file
(`+0x21` is the high half of the i16 at `+0x20`; `+0x45`–`+0x47` is the tail of a 36-byte zero-fill)
and §2.3b shows two more (`+0x89`–`+0xBA` is the gambit block; `+0x1C3`–`+0x1C5` are the
licence-board selectors). **Of the 67 bytes these six ranges claim, 10 are actually unaccounted**,
in five alignment gaps. ~~Two of the survivors are known from a direct read: `+0x1C3`
(u16 `0xFFFF`) and `+0x1C5` (u8 `0xFF`) are sentinels the initialiser writes~~ *(FE-4 part 2, OPUS 2026-09-27): `+0x1C3`–`+0x1C5` are
not survivors - they are the three u8 licence-board selectors of §2.3b. The initialiser's `0xFFFF` is one word store
over the two selector bytes `+0x1C3`/`+0x1C4`, and its `0xFF` goes into `+0x1C5`*
([the unit-definition page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.5).
~~The rest are either padding or reachable only by a route the scan does not follow.~~ *The rest are four alignment
paddings and one 8-byte region no route touches (§2.3b, FE-4).*

### 2.3a Those ranges re-read by overlapping byte range — 2026-09-17 (OPUS), `FE-4` clause 2

`FE-4` asked for exactly one thing: *"re-run the field scan counting stores by overlapping byte range
instead of by exact displacement — bounded mechanical work, and it would answer all six at once."*
**No re-scan was needed.** `battle-stats-record-accesses.tsv`, published beside this page, already
carries every access with its instruction text, and an operand's width is in that text. So this is a
re-aggregation of **this page's own evidence**, and anyone holding the file can check it:
`Tools/work/OPUS/p1-scratch/fe4_ranges.py`.

**Method.** For each of the 1,280 published rows, take `disp` and read the width from the
instruction (`byte`/`word`/`dword`/`qword`/`xmmword` `ptr`), then mark every byte in
`[disp, disp+width)`. 9 rows carry no readable width and were counted as 1 byte, which can only
*under*-state coverage. Counting by exact displacement marks **85 distinct offsets**; counting by
range marks **149 bytes**.

| range | by exact displacement | by overlapping byte range | what covers it |
|---|---|---|---|
| `+0x21`–`+0x23` | untouched | **`+0x21` touched**, `+0x22`–`+0x23` survive | `movsx eax, word [rdi+0x20]` (`002FF2F1`) — a 2-byte read at `+0x20` |
| `+0x45`–`+0x47` | untouched | **all 3 bytes written** | `mov dword [rsi+0x20], ecx` (`002FEFC8`), `rsi` = record `+0x24` |
| `+0x4F` | untouched | **untouched** | — |
| `+0x60`–`+0x63` | untouched | **untouched** | — |
| `+0x89`–`+0xBB` | untouched | untouched *by the scan's rows* — **but `+0x89`–`+0xBA` are written**, §2.3b | the gambit block, through `[rdi + rdx*4 + 0x88]` |
| `+0x1C3`–`+0x1C7` | untouched | untouched *by the scan's rows* — **but `+0x1C3`–`+0x1C5` are written**, §2.3b | the licence-board selectors |

**`+0x45`–`+0x47` is the tail of a 36-byte clear.** `BattleStats_RebuildEffectiveStatsAndAffinityState`
(`002FEF30`) sets `rsi = record + 0x24` (`002FEFAB`) and `ecx = 0` (`002FEFAF`), then writes
`qword [rsi]`, `[rsi+8]`, `[rsi+0x10]`, `[rsi+0x18]` and `dword [rsi+0x20]`
(`002FEFB9`–`002FEFC8`) — **`+0x24` through `+0x47` inclusive, zeroed before the rebuild recomputes.**
These three bytes are the end of the effective-stats block, not padding after it.

**`+0x21` is half of a field, not a byte.** `+0x20` is read as `word` and sign-extended, so `+0x21` is
its high half. It was only ever "untouched" because a 2-byte access was recorded at one displacement.

### The prediction that did not hold, which is the useful part

`FE-4` named **the block write** as the shape that would decide these six, having measured
displacement-generically that 8-byte-and-wider stores are as common as scalar ones at precisely these
offsets. **For this record that is not what decided them.** The published rows contain **four** stores
of 8 bytes or more in the entire record — `+0x24`, `+0x2C`, `+0x34`, `+0x3C`, all `qword`, all from
the one clear above — and **no 16-byte store at all**. What actually moved two ranges was an ordinary
2-byte read and an ordinary 4-byte write whose **tails** were never counted. The instrument defect was
real and the diagnosis of its cause was wrong here: *any* access wider than one byte hides its tail
from a per-displacement census, and the common widths do the damage, not the rare wide ones.

### What this does not settle

`FE-4` and `UQ-119` have a second clause — **the routes the scan does not follow**: record-as-index
forms, pointers stored into other objects, and writers beyond the third hop. **Nothing here touches
it**, and the four surviving ranges are untouched *on the enumerated routes only*. The checkbox below
is therefore **left unticked on purpose**: one of its two clauses is answered, and ticking it would
move a readiness rung without the evidence to justify it.

### 2.3b `FE-4` clause 1 — and a correction to §2.3a above (2026-09-17, OPUS)

§2.3a settled clause 2 from the accesses file and left four ranges standing. **Two of those four do
not stand, and finding out why answers clause 1.** §2.3a's limit was that it re-aggregated only the
rows the scan produced; it could not see a field the scan never entered. This section is the
correction, and the correction is larger than the thing it corrects.

**Depth is not the blind spot.** Re-running the page's own instrument at greater depth
(`hop_scan.py --hop 0x698 --array 0x02EBF190:0x1C8:8 --size 0x1C8 --control 00300530:0x48`, control
FOUND at every depth):

| depth | accesses | functions | propagated pairs |
|---:|---:|---:|---:|
| 3 (as published) | 1,374 | 291 | 139 |
| 4 | 1,378 | 291 | 143 |
| 5 | 1,378 | 291 | 144 |
| 6 | 1,378 | 291 | 144 |

It **saturates at 5 and adds no new access site after 3** — not one byte of the six ranges changes
between depth 3 and depth 6. *"Writers beyond the third hop"* is an empty set here, and that sub-clause
of `FE-4` can be closed.

**The blind spot is the array seed.** Forty-six functions form this record's address themselves in
exactly the shape the seed describes — `*(0x02EBF190) + 8 + k*0x1C8` — and **41 of the 46 never
appear in the scan's output at all.** They are not obscure: `BattleStats_*`, `GambitConfig_*`,
`PartyConfiguration_*`, `Equipment_*`, `BattleSlotMap_*`. `BattleStats_GetByBattleSlotIndex`
(`00320A40`, 33 bytes) *is* the accessor — `imul rcx, rax, 0x1c8` (`00320A4B`), the global
(`00320A52`), `add rax, 8` (`00320A59`), `add rax, rcx` (`00320A5D`), `ret` — and it returns the
record in `rax`, which is the shape `--retseed` exists for. The scan learned **5** record-returning
functions.

### What those 41 functions put back

**`+0x89`–`+0xBA` is the gambit block, and this page already said so.**
`GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` (`00327CB0`) writes
`word [rdi + rdx*4 + 0x88]` (`00327D57`) and `word [rdi + rdx*4 + 0x8a]` (`00327D64`) for
`rdx` = 0…11 — covering `+0x88`–`+0xB7` — then the u16 enable mask at `+0xB8`
(`00327D6C`–`00327D78`, `bts`) and the u8 filled-count at `+0xBA` (`00327D84`). **The `+0x088` row of
the field table above already names those instructions.** §2.3 called the same 51 bytes untouched,
so the page contradicted its own table; the scan recorded `+0x88` only as the **u8 arm of the union**
(`movzx … byte ptr [X + 0x88]`) and never entered `00327CB0`. This is `FE-4`'s *record-as-index*
route, concretely: the write carries a scaled index, and the census recorded its base displacement.
**Only `+0xBB` survives** — one byte of alignment before `+0xBC`.

**`+0x1C3`–`+0x1C5` are the licence-board selectors.** Same array base, guarded by the kind byte:

| offset | field | writers | readers |
|---|---|---|---|
| `+0x1C3` | licence-board selector **A** (`0xFF` = none) | `BattleStats_SetLicenseBoardSelectorAAndActive` (`00323772`); the initialisers `0023ACD5`, `00328D52` write the `0xFFFF` sentinel over `+0x1C3`–`+0x1C4` | `BattleStats_GetLicenseBoardSelectorA` (`0032369B`) |
| `+0x1C4` | licence-board selector **B** | `BattleStats_SetLicenseBoardSelectorBAndActive` (`00323722`) | `BattleStats_GetLicenseBoardSelectorB` |
| `+0x1C5` | the **active** selector | both setters (`00323729`, `00323779`), `BattleStats_ReconcileActiveLicenseBoardSelector` (`00324341`, `0032434B`), initialisers `0023ACDD` / `00328D5D` (`0xFF`) | `BattleStats_GetActiveLicenseBoardSelector` |

Both setters test `byte [r8+5] == 0` — **party only** — and `byte [r8+4] <= 6`, and refuse a value
above `0xB`. All five accessors share those guards and a slot bound of `0x27`, and every one returns
`0xFF` on refusal. **Only `+0x1C6`–`+0x1C7` survive.**

**The reconciler is a toggle, which is what fixes the meaning of the three.**
`BattleStats_ReconcileActiveLicenseBoardSelector` (`003242F0`) reads A into `eax` (mapping `0xFF` to
`-1`, `00324322`–`00324327`) and B into `ecx`; **if B is set and the active currently equals A it
writes B into `+0x1C5`** (`0032433E`–`00324341`), and **otherwise it writes A** (`00324348`,
`0032434B`). So with both set it alternates the active between them, and with only A set it pins the
active to A.

**The supported reading: A and B are the character's two licence boards.** Three things agree and
none of them is a name read off a register — the value domain is `[0, 0xB]`, **twelve**, refused
above that by both setters; the structure is *two selectors plus one active*, reconciled by a toggle;
and the third writer of this triple is reached from the script verb **`resetJobs`** (`05D6`), which
`FZ-6` established as the sole caller of `00328BD0` — the function that writes the `0xFFFF` over
`+0x1C3`–`+0x1C4` and `0xFF` into `+0x1C5`. *A verb called `resetJobs` clearing exactly these three
bytes is the strongest naming evidence available without a string.* What is **not** established here
is which board id means which job: the ids are a domain of twelve, and nothing in this record maps
them to authored rows.

### The six ranges, finally

| range | claimed | actually unaccounted |
|---|---:|---:|
| `+0x21`–`+0x23` | 3 B | **2 B** (`+0x22`–`+0x23`; `+0x21` is the high half of the i16 at `+0x20`) |
| `+0x45`–`+0x47` | 3 B | **0** (the 36-byte clear) |
| `+0x4F` | 1 B | **1 B** |
| `+0x60`–`+0x63` | 4 B | **4 B** - *with `+0x5C`–`+0x5F`, which the struck `+0x05C` row had counted as covered (FE-3), an 8-byte region (FE-4 part 2, OPUS 2026-09-27)* |
| `+0x89`–`+0xBB` | 51 B | **1 B** (`+0xBB`) |
| `+0x1C3`–`+0x1C7` | 5 B | **2 B** (`+0x1C6`–`+0x1C7`) |
| **total** | **67 B** | **10 B** |

**67 bytes of "nobody reaches this" are 10**, in five gaps of one to four bytes. ~~every one of them
sitting exactly where a compiler pads to the next field's alignment. There is no unexplained region
in this record.~~ *(FE-4 part 2, OPUS 2026-09-27, on FABLE's FE-4 record `_index/candidates/fe4-untouched-ranges/`): four of the five
are alignment padding - `+0x22`–`+0x23`, `+0x4F`, `+0xBB`, `+0x1C6`–`+0x1C7`. `+0x60`–`+0x63` is not: with
`+0x5C`–`+0x5F`, freed when the stale `+0x05C` row was struck (FE-3), it is an 8-byte region after the u16 at `+0x5A`
that the PC build allocates and no followed route touches (`_types/fields.tsv` `BattleStatsRecord` `+0x05C`
`unobservedSpan005C` u8[8], 6d2b04a07). What it held, if anything, is not claimed.*

### What this costs the page, stated plainly

The field map's own frontmatter says *"a field map from every reached accessor"*, and that is still
true — but **41 functions that address this record directly were never reached**, so "every reached
accessor" is a much smaller set than a reader would assume. The rows in the table are not wrong; the
**absences** were, and every absence on this page inherits that limit. ~~`UQ-119` stays unticked.~~ *(answered: see §7 — `UQ-119` / `FE-4` ANSWERED 2026-09-27, the seed repaired and the stored pointer followed; 2026-10-02, OPUS)*

### 2.4 What the map says that no single page did

- **The seven stat bytes `+0x2A`–`+0x30` and the six after them (`+0x31`–`+0x36`) have exactly one
  writer** on every route — `BattleStats_RebuildEffectiveStatsAndAffinityState` (`002FEF30`) — and
  ~~`+0x31`–`+0x36` have **no reader** the enumeration reaches: six output bytes the rebuild computes~~
  ~~that nothing on a battle unit consumes.~~ `+0x31`–`+0x33` are read by every outcome roll: the threshold loaders `00388FB0` and `00389040` load target `+0x33`, `+0x32` and `+0x31` into the bands `02AEDFF0`, `02AEDFF4` and `02AEDFEC` *(corrected 2026-10-02, OPUS: checked at `00388FB0`–`00388FC8` and `00389093`–`003890AB`; this page's own rows for `+0x31`–`+0x33` and the-formula-scratch-block.md §2.2)*.
- **`BattleUnit_ExecuteDirectStateCommandOrder` (`002FDDA0`) reads and writes every base stat
  `+0x08`–`+0x1E`** — a script-facing writer of the *base* numbers beside the level grower and the
  level-up, which is what makes a "set stat" order possible without a level.
- **`BattleFormula_ApplyTargetResult` (`003112F0`) writes `+0x08`, `+0x0A`, `+0x12`, `+0x14`** — ~~a~~
  ~~result can raise base HP, base MP and two stat words directly~~ on foe records only: `0031189B` `cmp byte ptr [rdi + 5], 1` / `jne` skips all four adds unless the kind is 1, so a result cannot change a party record's base stats *(corrected 2026-10-02, OPUS: checked at `0031189B`–`0031189F`; §2.2, the `FE-6` correction of 2026-09-26)* (the applier page's decode names
  the record bytes).
- **The status words have three writers in total** — the status write for `+0x38` / `+0x3C` /
  `+0x64`, and the rebuild for `+0x38` and `+0x3C` — against **126 readers of `+0x3C`** and **124
  of `+0x64`**: presence is read everywhere, changed in two places.
- ~~**`+0x5C` is private to `BattleFormula_AdvanceStatusTimersAndBuildResult` (`00386C70`)**.~~ *(FE-4 part 2, OPUS 2026-09-27): struck -
  those accesses are the result record's `+0x5C + 4i` (FE-3); `+0x5C`–`+0x63` is untouched (FE-4).*
- **`+0x18C` and `+0x190` are read by one function on the unit side, `00329220`** — the same
  unnamed builder that copies the spawn counter and the affinity bytes ([the spawn-keep entry](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) `FD-4`).

## 3. Key addresses

| address | size | what |
|---|---|---|
| `002FEF30` | 2,859 B | `BattleStats_RebuildEffectiveStatsAndAffinityState` — the sole enumerated writer of `+0x24`–`+0x37` and a writer of `+0x38`, `+0x3C`, `+0x40`–`+0x44` |
| `0030E360` | 1,323 B | `BattleStats_ChangeStatusAndProcessSideEffects` — `+0x38`, `+0x3C`, `+0x64`, `+0xBC[]`, `+0x13C[]` |
| `0030FED0` | 1,787 B | `BattleStats_RecomputeDerivedStateAndAutoStatuses` — `+0x06`, `+0x40`–`+0x44`, `+0x48`, `+0x4C` |
| `00300530` | | `BattleStats_ModifyHPAndProcessLethalState` — `+0x48` |
| `00300CE0`, `00300BC0` | 351 / 207 B | `BattleStats_ModifyPrimaryResource` (`+0x4C`), `BattleStats_ModifySecondaryResource` (`+0x06`) |
| `0030C470`, `0030C650` | 432 / 570 B | the level grower and the level-up — `+0x08`–`+0x1C`, `+0x20`, `+0x88`, `+0x18C`, `+0x1C2` |
| `002FDDA0` | 1,937 B | `BattleUnit_ExecuteDirectStateCommandOrder` — `+0x08`–`+0x1E` |
| `003112F0` | | `BattleFormula_ApplyTargetResult` — `+0x08`, `+0x0A`, `+0x12`, `+0x14`, `+0x17C`–`+0x18A` |
| `0030E060` | 200 B | the `+0x4E` charge count |
| `00386C70`, `0030EA40`, `00385570` | | the status-timer functions around `+0x5C` and `+0x17C` |
| `00329220` | 1,933 B | the unnamed unit-record builder that reads `+0x42`–`+0x44`, `+0x52`–`+0x5A`, `+0x68`–`+0x7B`, `+0x18C`, `+0x190` |
| `00328FB0` | | the only enumerated writer of `+0x00` (`00328FD5`) |

## 4. Data structures and formulas

```
BattleStatsRecord (BKBI), 0x1C8
  +0x00 u32  ?            +0x04 u8 row index   +0x05 u8 kind      +0x06 s16 secondary resource
  +0x08 u32  base HP      +0x0C u16 base MP    +0x10..+0x1F  UNION by kind +0x05: party (kind 0) f32[4]; else i16[8]   (+0x0A/0E words: rebuild inputs)   <- corrected 2026-10-02, OPUS: +0x0C is s16 (002FF084 movsx)
  +0x20 u8   rank         +0x24 s32 max HP     +0x28 s16 MP capacity
  +0x2A..+0x30 u8  Str Mag Vit Spd Atk Def MRes      +0x31..+0x36 rebuild outputs (unread)   +0x37 u8 MP bars   <- corrected 2026-10-02, OPUS: +0x31..+0x33 are read as the outcome bands (00388FB0-00388FC8, 00389093-003890AB)
  +0x38 +0x3C +0x64 u32 status words      +0x40..+0x44 u8 affinity     +0x48 s32 HP   +0x4C s16 MP   +0x4E u8 charges
  +0x50 u16[5] equipment   +0x5C u8[8] untouched (FE-4)   +0x68 u8[16] mutable layer   +0x78 u8[16] derived layer
  +0x88 u8 grower arg      +0xBC u32[32] status param   +0x13C u16[32] status timer word
  +0x17C s16[8] effect-slot timers (was: duration timers)   +0x18C u32 EXP   +0x190 u32 LP   +0x194 bitmap[361]   +0x1C2 u8 level   +0x1C3 / +0x1C4 u8 selectors A / B, +0x1C5 u8 active selector (0xFFFF / 0xFF at init)
```

## 5. Call chain

The writers, by the page that reads them: the rebuild → [the single stat rebuild](../../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md); the
status write and layers → [the status write](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) and [the two-layer model](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md); the HP write →
[the HP write](../Current-HP/the-hp-write-and-the-lethal-transition.md); MP → [where MP comes from](../../10-Status-Periodic-Terminal/where-mp-comes-from.md); the recompute → [the auto-status rebuild](../the-auto-status-rebuild.md);
the grower and the level-up → [the unit-definition page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.6 and [the level-up](../../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md);
the applier → [applying a result](../../07-Combat-Action/applying-a-result-to-a-target.md).

## 6. Modding notes

- **To change what a combatant *is*, write the base stats `+0x08`–`+0x1E` and recompute** — the
  seven effective bytes are rebuilt from them and overwritten by `002FEF30` on every recompute;
  writing `+0x2A` directly is undone by the next status change.
- ~~**`+0x31`–`+0x36` are free to repurpose on the unit side** — nothing enumerated reads them — but~~
  ~~the rebuild rewrites them, so a mod must write after it or hook it.~~ **`+0x31`–`+0x33` are not free to repurpose**: every outcome roll reads them as its evade bands, so a port that reuses them breaks every hit roll; the rebuild rewrites all six, so a mod must write after it or hook it *(corrected 2026-10-02, OPUS: checked at `00388FB0`–`00388FC8` and `00389093`–`003890AB`)*.
- **The status words are read from 126 places**; a mod that flips a status must go through the
  status write or every one of them sees an inconsistent presence.

## 7. What is not known

- [x] **FE-1.** *(status restated in the register 2026-09-26, FABLE, Claude Opus 5.5: see the row)* **What `+0x00` holds** — one enumerated writer (`00328FB0`, `00328FD5`) and four readers,
  none read. **FE-1.**
  *PARTIAL 2026-09-14 (FABLE), corrected twice the same day:* a flags word. Bit 0 is the battle-member lock and
  bit 2 drives the member like a non-party unit (below). **No reader of any other bit exists in the census, and
  that is now the stronger statement: no other bit is read OR WRITTEN on this path at all.**
  ~~which was wrong: `BattleUnit_HasNonPartyEngagementEvidence` tests bit 5 (`00308075`) and bits 3 / 6
  (`0030807E`), and `BattleUnit_ComputePresentationSuppressionMask` tests bits 4 (`003126C0`) and 3
  (`003126C8`). OPUS's enumeration below adds writers for bit 1 (`00233BA8`) and bit 5 (`00237DD7`).~~
  **Both of those corrections are withdrawn 2026-09-14 — FABLE's at FABLE's own request
  (`FABLE-NOTICE-OPUS-FE1-SECOND-SWEEP-AND-CONCURRENCE`, landed by OPUS), and OPUS's by OPUS.** All six
  instructions load `[unit + 0x698]`, test the kind byte, and then load **`[unit + 0x6A0]` into the same
  register** before the bit work, so they are accesses to the spawn-keep entry, whose word `+0x00` is `AL-10`
  and already answered. Two identities made the same register-redefinition error within hours of each other,
  which is why the enumeration at the page tail states its instrument. What bits 1 and 3–6 of **this** word mean
  is not open: nothing touches them.
  *Narrowed 2026-09-14 (FABLE, FE-1): **a flags word, and two of its bits are placed.*** The route census
  ([`battle-stats-record-accesses.tsv`](battle-stats-record-accesses.tsv)) has one writer and four readers.
  - **Bit 0 is the battle-member lock.** The writer `00328FB0(selector, on)` finds the unit by definition selector and sets or
    clears bit 0 of its stats record (`00328FD5` / `00328FDE`). Its only caller is script verb `0x035A` **`setbattlememberlock`**
    (`00351A40`, which pops member and flag). The roster reconcile `PartyConfiguration_ReconcileRuntimeRosterFirstThreeFromRequestedSelectors`
    (`00328DB0`) records each locked member in its bitmask (`00328E5B`–`00328E60`).
  - **Bit 2 is a party-only flag.** `BattleUnit_SelectAndCommitNextAction` skips a party-kind unit (`+5 == 0`) whose bit 2 is
    set (`00305BF3`–`00305C03`). The predicate `0030BCD0` returns bit 2 for a party-kind unit and 1 for anyone else
    (callers `00325D90`, `00328530`). The status-view builder `00329220` copies bit 2 into bit 7 of its display record
    (`00329694`–`003296A1`). ~~**No writer of bit 2 is in the census**, so what sets it, and so what it means, stays open.~~
    *Corrected 2026-09-14 (FABLE, UQ-123): the census could not see bit 2's writers, which store through a register
    at displacement 0.*
    - `BattleStats_InitializeDefinitionRecord` sets bit 2 from the party row's byte `+0x2C` bit 6 (`0023AF28`).
    - The area-state party walk `00239960` sets or clears it from bit 0 of a preset byte (`00239D89` / `00239D94`).
    - A whole-image sweep of `or 4` / `and 0xFFFFFFFB` on `[reg]` finds these two on stats records.
      `BattleUnit_ApplyUnitDefinition`'s `or dword [rdi], 4` (`0023AC56`) is the battle unit's own flag word.
    - ~~The meaning stays open.~~ **Behaviour read 2026-09-14 (FABLE): bit 2 makes a party member be driven like a
      non-party unit.**
      - **Action choice.** `BattleUnit_SelectAndCommitNextAction` tries the switched order set `[unit+0x6F8]` only for
        a party-kind unit with bit 2 clear (`00305BE7`–`00305C1A`). With bit 2 set it goes where non-party units go:
        the order set `[unit+0x6E0]` with subgroup byte `+0x6B5`, clearing `+0x6F8` (`00305C34`–`00305C58`). Both
        branches then fall through to `[unit+0x6F0]`.
      - **Navigation.** `BattleUnit_CanAdvanceCombatNavigation` (`00325D90`) refuses the party focus unit unless
        `0030BCD0` is non-zero (`00325E02`–`00325E4A`), when neither status mask `0x8000020` nor action
        `0x414E` applies. So a focused party member with bit 2 clear is not advanced
        by combat navigation, and one with bit 2 set is, unless unit flag bit 18 is set.
      - **The authored default.** It comes from row byte `+0x2C` bit 6 of the party table, `battle_pack.bin`
        directory `+0x44`: 40 × 128-byte rows at `+0x20`, read from the shipped archive
        (`ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin`). Bit 6 is **set** for Fran, Balthier,
        Basch and Penelo (rows 2–5), every guest and unnamed row (7–25) and all thirteen Espers (27–39). It is
        **clear** for Vaan, Ashe, Reks and the Chocobo (rows 0, 1, 6, 26). The area-state party walk
        (`00239D83`–`00239D94`) then sets or clears it per member.

      The designer's name for the flag is not in any shipped artefact. "AI-driven member" describes what the two
      readers do with it, not a recovered label.
  - **Bit 1 and bits 3–31 have no accessor at all in the census.** *Corrected 2026-09-14 (FABLE)* read bits 3–6
    into this word from `00308040` and `003125E0`; *that correction is withdrawn 2026-09-14 (OPUS)* — both
    bodies load `[unit + 0x698]`, check the kind byte, and then load a **second record at `[unit + 0x6A0]`**
    into the same register before the bit test. The bits they test are that record's, not this one's. The
    statement is now stronger than when it was first written: no instruction in `.text` reads *or writes*
    any bit of this word except bits 0 and 2. See the enumeration at the page tail.
- [x] ~~**FE-2.** **What `+0x31`–`+0x36`, `+0x0A` / `+0x0E` / `+0x12` / `+0x16` / `+0x1A` / `+0x1E` are** —
  the rebuild's six unread outputs and its six word inputs beside the four float stats.~~
  **FE-2 ANSWERED 2026-09-14 (FABLE).**
  - *The outputs.* The rows for `+0x31`–`+0x36` in §2.2 name them by what they are built from: innate, weapon
    and shield evade (the roller's three bands), magick evade, total evade and total magick evade. ~~That nothing~~
    ~~enumerated reads them is a separate fact, and it stands.~~ The three bands are read: `00388FB0` and `00389040` load `+0x33` / `+0x32` / `+0x31` into `02AEDFF0` / `02AEDFF4` / `02AEDFEC` *(corrected 2026-10-02, OPUS: checked at `00388FB0`–`00388FC8` and `00389093`–`003890AB`)*.
  - *The words, spawn-backed arm.* Each word is the record term of one `.ard` column's
    `growth·K + base + word` sum ([where a stat number comes from](../where-a-stat-number-comes-from.md), `CB-5`): `+0x0A` Magick Power, `+0x0E` Speed, `+0x12`
    Defence, `+0x16` innate evade and `+0x1A` block. `+0x1E` joins no column; it is a term of total evade.
  - *The words, party arm.* `+0x0A` is the high half of the u32 at `+0x08`, and the rebuild does not read `+0x0E`.
    The other four are f32 high halves.
- [x] ~~**What `+0x5C` is** — private to `00386C70`.~~ **FE-3 ANSWERED 2026-09-13 (FABLE), with OPUS's correction:** there is no stats-record `+0x5C` access. OPUS's type correction of 2026-09-12 (`_types/fields.tsv`, `OPUS-TYPEFIX-RESULTREC`) showed the three cited instructions address the result record, and the loop confirms it: `00386C90` sets `r14 = stats + 0xBC` (the status's `statusParameterA` element), `00386CC6` sets `r12 = result − stats`, the loop steps `r14` by 4 over 32 statuses (`00386F65`, `00386F6F`), so `[r14 + r12 − 0x60]` is `result + 0x5C + 4·i` — `BattleResultRecord.parameterA[i]`. The step writes the stats timer minus 1 there (`00386E3E`–`00386E43`), or minus 10 for rows whose table byte `+8` is not `0xFF` (`00386EE4`–`00386EEC`), and for statuses 2 and 6 tests whether it reached 1 (`00386E48`–`00386E5C`). The address was a census artefact of dropping `r12`.
- [x] ~~**Whether `BattleFormula_ApplyTargetResult`'s i16 deltas at `+0x0A` / `+0x12` / `+0x14`**
  (`003118D9`, `003118F7`) are ever applied to a party record — where the same bytes are the low /
  high halves of f32 stats — or whether the result words `+0x11E`–`+0x124` stay `-1` for party
  targets; and the meaning of the eight i16 stats individually.~~ **FE-6** — answered 2026-09-11:
  the applier's step 16 runs only when the target stats' kind byte is 1
  ([the applier](../../07-Combat-Action/applying-a-result-to-a-target.md) §2 step 16), so the deltas
  are foe-only by construction; the eight i16's meanings stay with `FE-2`.
- [x] **UQ-119.** **The routes the scan does not follow**: record-as-index forms, pointers stored into other
  objects, and writers beyond the third hop; a fourth hop or a stored-pointer follow would say
  whether the 6 untouched ranges are real. **FE-4.** *(Clause 2 — "are the six ranges real" — is **answered**: §2.3a and §2.3b
  reduce the six ranges from 67 unaccounted bytes to 10. Of clause 1, *writers beyond the third hop*
  is **closed** — the scan saturates at depth 5 and gains nothing after 3 — and *record-as-index* is
  **demonstrated** on the gambit block. Deliberately still unticked: the real blind spot, that the
  array seed missed 41 of the 46 functions forming this record's address, is now named but not
  repaired, and *pointers stored into other objects* is still untested.)*
  ***ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5): the seed is repaired, the stored pointer is followed, and the last
  bytes are four paddings and one unused region.*** The repaired seed is the 68 functions that form this record's address
  or call its getter. The unit's `+0x698` pointer and every getter result (604 sources) are followed into callees to
  depth 3, and the getter's result is never stored elsewhere. None of them reaches `+0x5C`–`+0x63`; the controls
  `+0x24` and `+0x64` are found. `+0x22`–`+0x23`, `+0x4F`, `+0xBB` and `+0x1C6`–`+0x1C7` are alignment padding.
  `+0x5C`–`+0x63` is not: once the stale `+0x05C` row is struck (FE-3), it is an 8-byte region after the u16 at `+0x5A`
  that the PC build allocates and never touches. This refines §2.3b's "every one of them sitting exactly where a
  compiler pads", which is routed to OPUS. [The FE-4 record](../../_index/candidates/fe4-untouched-ranges/README.md),
  control `fe4_ranges.py`, 5 checks.
- [x] ~~**What `00329220` builds** from twelve of these fields (with `FD-4`).~~ **FE-5** — ANSWERED
  2026-09-10: the party member status view, a 0xC0-byte snapshot for the UI
  ([the status-view page](../../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md)).

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| Every row of the table | `battle-stats-record-accesses.tsv` beside this page; `hop_scan.py --hop 0x698 --array 0x02EBF190:0x1C8:8 --size 0x1C8 --depth 3`, control `00300530:0x48` found | 1 | PROVEN |
| The names in the name column | the linked pages, each reading the writer from the bytes | 1 | PROVEN (by reference) |
| The untouched ranges | ~~absence on every enumerated route with a passing control~~ **corrected §2.3a and §2.3b**: computed by exact displacement over a scan that never entered 41 of the 46 functions forming this record's address. Four of the six fall; 67 claimed bytes are 10 | 1 | PROVEN only for the 10 bytes, and only on the enumerated routes |
| What the untouched bytes and the unnamed fields are | ~~**not established**~~ *(answered for the bytes: see §7, `FE-4` ANSWERED 2026-09-27 — four paddings and the unused region `+0x5C`–`+0x63`; 2026-10-02, OPUS)* | — | UNKNOWN |

## 9. Related

- [`../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md`](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) — initialisation of the record on both paths.
- [`../../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md`](../../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md) — the rebuild that writes the effective block.
- [`../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md`](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) — the status words and the per-status arrays.
- [`../Current-HP/the-hp-write-and-the-lethal-transition.md`](../Current-HP/the-hp-write-and-the-lethal-transition.md), [`../../10-Status-Periodic-Terminal/where-mp-comes-from.md`](../../10-Status-Periodic-Terminal/where-mp-comes-from.md) — HP and MP.
- [`../the-auto-status-rebuild.md`](../the-auto-status-rebuild.md) — the recompute and the affinity handshake.
- [`../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md`](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) — the record's enemy-side home at `+0x80`, mapped the same way.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every cited access site in this map was disassembled and its displacement compared with the offset of
the row citing it, by
[`check_field_citations.py`](../../../Tools/analysis-kit/gfz-scripts/check_field_citations.py):
**215 sites across 85 rows**.

| outcome | sites |
|---|---:|
| displacement **is** the row's offset | 180 |
| resolved through an embedded sub-object base | 31 |
| indexed form, indeterminate by displacement alone | 2 |
| cites the source object of a cross-object copy | 1 |
| cites a datum rather than an instruction | 0 |

**Nothing failed to decode, and no site contradicts its row.**

**The sub-object bases, counted for the first time** (5 distinct): `+0x24` x23, `+0x68` x5, `+0x7` x1, `+0x50` x1, `+0x78` x1.

**83.7 % of citations land on their row's offset directly** - the highest direct rate of the six maps checked, and a sign that this record is accessed from its own base rather than through embedded sub-objects.

**Not claimed:** this checks what the map *says* — that each citation touches the offset it is filed
under. It says nothing about fields the census never reached, and the document's own coverage limits
stand unchanged.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

- **Movement — SERVICE and CLIENT.**
  - `BattleUnit_ActivateAppliedDefinitionRuntime` (`00233AD0`) calls a 448-byte locomotion helper.
  - `002FE950` (`sinf` ×2) calls a 38-byte movement helper.
  - `00328530` calls a 40-byte movement helper.
  - `BattleUnit_CanAdvanceCombatNavigation` (`00325D90`) is called by `BattleUnit_UpdateCombatNavigationStep` and reads
    `0030BCD0`.
  - `00233D70` and `BattleAction_ComputeChargeProgressStep` (`002F9C00`) are called by movement bodies of 475 and
    442 bytes.

  **The charge-progress step is reached from locomotion.**
- **PlatformOnlineAchievements — SERVICE.** On its Esper-attack arm, `BattleAction_ConsumeExecutionResources`
  (`00305640`) calls the 55-byte helper that tests awarded bit 13 and pokes Steam index `0x13`
  ([where MP comes from](../../10-Status-Periodic-Terminal/where-mp-comes-from.md), crossings).

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Rewards_Progression_Economy — CLIENT and SERVICE, 23 edges.** Cited stats functions are called by `BattleUnit_ProcessDefeatRewardsAndLoot` (3), `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (2) and two rewards bodies (432 and 488 bytes). They call `GameState_GetGil` (3), `GameState_SetGil` (2), `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (2), a 432-byte rewards body (2) and a 122-byte helper (2).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**RNG_Random_Selection — SERVICE.** `002F8060` on this page calls `RNG_MT19937_NextU32_Thunk`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00863BF0` - onto the CRT's Mersenne Twister next-u32; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Story_Event_Quest_Hunt — SERVICE.** `002F8060` on this page calls `PersistentFlag_SetBank512Low`, owned by that layer. What it reaches is the low-512 bank setter, and it states its range: an id above **`0xFF`** is refused before the bank is touched; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — SERVICE on three edges, CLIENT on one (4 edges, every body read).** Three
Presentation bodies read this page's functions. `00470780` and `00470B70` both call `00320CF0`: each
is a draw routine that returns immediately unless `byte[this+0x3A]` says it is live, then branches
on the mode byte `byte[this+0x38]`, and `00320CF0` is where it gets its number — that function
resolves the unit through `00236820`, needs `byte[unit] & 0x10` and the action block at
`[unit+0x698]`, tests the requested index as a bit in `dword[+0x64] | dword[+0x3C]`, **accepts only
indices 2 and 6** (`lea eax, [rbx-2] / test al, 0xFB`), and returns `dword[block + index*4 + 0xBC]`.
`001C6C00` calls `001CA600`, which reads the named layout parameters `mScrollListHeight` and
`mCommandTitleFontHeight` out of the parameter registry at `01F81318`. The one edge in the other
direction is CLIENT: `AiOrder_EvaluateTargetSelector` on this page calls `00322360`
`BattleUnit_TestActorViewFrustumAtCurrentPosition`, which takes the unit's `[+0x10]` object, reads a
position triple through `00265020`, zeroes the fourth component and hands it to `003223C0`. In every
case the crossing is the call; nothing here is a shared responsibility. Read from the shipping bytes
2026-09-14 (OPUS).

**Input — MECHANICAL (SWE2-EC7-96, 1 edge).** `00377C20` — the re-check this page's `0030D600`
section cites — is reached through `00253C70` on the Input layer. Shared-helper fan-in; no Input
relationship to the stats record.

**InputGameplay — MECHANICAL (SWE2-EC7-96, 1 edge).** The same `00377C20` is reached through
`00313A00` on the InputGameplay layer. Shared-helper fan-in; no InputGameplay relationship to the
stats record.

**Items_Equipment_Shops_License — SERVICE (SWE2-EC7, batch 165).** `00239960` — the same
`00263E30`-resolver family this page's `00320640` section cites — calls `00300BA0`,
`0031A630` and `00323910` on that layer. Shared-helper fan-in over the inventory lanes; no
Items_Equipment_Shops_License relationship to the stats record beyond those calls.

**Party — CONSULTED BOTH DIRECTIONS (SWE2-EC7, batch 165).** `00233A20` calls `003273B0`,
`00239960` calls `00329080`, and `00265020` is reached from `00303CC0` on that layer — the
Party roster and the stats record consult each other's accessors; mechanical consultation,
no shared ownership.

**Status_Periodic_Terminal — CONSULTED BOTH DIRECTIONS (SWE2-EC7, batch 165).** `002F8060`
reaches `00310DB0` and `002F9400` calls `00320450`/`00329A20` on that layer while
status-layer bodies call back into this page's readers — the periodic-status tick and the
stats record share the unit block, not ownership.

**ActorEntity — CONSULTED BOTH DIRECTIONS (SWE2-EC7, batch 165).** `00233A20` is reached
from `00236300`, `00233AD0` calls `00238BF0`/`00239E10`/`0031B76x` on that layer, and the
`resetJobs`-lane `0031A260` cites the actor-side probes (`0031A410`) — the actor record and
the stats record share the unit block; consultation both directions, no shared ownership.
Edge detail from `edges.tsv`.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Every function below is a caller or callee of a function this map lists as a reader or writer of the stats record; the map claims the fields and the offsets, and these edges are other layers using the same accessors.*

**Audio — SERVICE and CLIENT (5 edges).** The level-set `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` and the result sink `BattleFormula_ApplyTargetResult` `003112F0` call the sound-id resolver `003A1180` and the sound-play entry `002DF220`; the 3D positional audio body `00362850` calls `Actor_GetWorldPosition` `00265020`. Two record writers play a sound after they change the record (the level-up plays bank-local sound 7), and positional audio reads an actor's position through the same getter; no audio code touches a stats field.

**CombatAI — CLIENT and SERVICE (30 edges).** The record initialiser `BattleStats_InitializeDefinitionRecord` `0023AC80`, `00239960` and the equipment-clearing `00328BD0` call `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030`, `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` `00327CB0` and `GambitRuntime_RebuildOrderSetForStatsRecord` `00327DE0`, and `00327CB0` and `00327DE0` call each other; `AiOrder_EvaluateTargetSelector` `00301AD0` calls `AiOrder_ComputeBoundedSelectorScalar` `00308C20`, `BattleTarget_MatchesRelationMode` `0030BD00`, `BattleTarget_ComputeSurfaceDistanceBetweenUnits` `0031E6F0`, `BattleTarget_ComputeSurfaceDistanceToPosition` `0031E760`, `AiTargetSelector_ResolveOperandValue` `00321190`, `BattleEnmity_ReadForCombatantId` `003215C0` and `BattleEnmity_GetHighestRelevant` `00321630`, and calls `BattleUnit_FindMappedDefinitionSelectorByIndex` `0031B810` and `BattleUnit_TestActorViewFrustumAtCurrentPosition` `00322360`, and is called by `AiOrder_EvaluateAndResolveActionTarget` `003014C0`; `BattleUnit_SelectAndCommitNextAction` `00305AB0` calls `BattleUnit_TrySelectAndCommitAiOrderFromSet` `00305CC0` and is called by `BattleUnit_UpdateCombatFrame` `00308610`; `AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` `0030F130` calls `ActorRuntime_GetClass3FloatPair` `00265090`, `0031B810` and `BattleAction_ComputeAuthoredStatusMask` `003872D0`; and `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` calls `BattleEnmity_AdjustOtherRelevantCombatants` `00321B00`, while `AiOrder_CheckActionPreconditions` `00301830` calls `BattleUnit_HasNonPartyEngagementEvidence` `00308040`, `BattlePerception_TestCachedSpatialVisibilityPair` `0032A4D0` calls `00263940`, and `003014C0`, `00301AD0` and `00305AB0` call `FieldData_GetActiveFieldRecordBit15` `00377C20`. The stats record carries the unit's gambit banks and runtime order sets, which the record initialiser and the equipment reset rebuild through the gambit layer, and the AI's selection reads the record's fields through the accessors this map lists.

**CoreRuntimeScheduling — DEPENDENCY (1 edge).** The HP write `BattleStats_ModifyHPAndProcessLethalState` `00300530` calls `GameClock_GetRawTickCounter` `0032A150`. On the lethal path the HP write stamps the raw game tick into the record as the death time.

**Gameplay — CLIENT and SERVICE (34 edges).** The id validator `BattleEncodedId_IsValidForClass` `00322C50` is called by `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30`, `00301AD0`, `0030FED0`, `0031B810`, `00322560`, `00327CB0` and `PartyConfiguration_ReconcileRuntimeRosterFirstThreeFromRequestedSelectors` `00328DB0`; `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0`, `00300530`, `BattleAction_UpdateSpecialPresentationSequence` `00306760` and `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` call `BattleUnit_DispatchActorPresentationEvent` `003299B0`; `002FEF30` and `0030E360` call `BattleUnit_UpdateEngagementStateFlag` `00307D10`; `00301AD0` also calls `BattleEncodedId_DispatchQueryMode0Value` `00309EC0`, `BattleTargetBuffer_ResetPreservingFlag0` `00316CF0`, `BattleDefinition_GetRuntimeCategoryBySelector` `0031EA90` and `BattleUnit_GetPrimaryFormulaResourceByte26` `00321320`; `00239960` calls `BattleSystem_ResetRuntimeState` `00237DF0`, which calls `0023AC80`; `00265020` is called by `0031ADB0` and `BattleAction_FindApproachGeometryAroundTarget` `00339630`; `00300530` calls `BattleTargetBuffer_FindActorWorkIndex` `00316D70`; `00308040` calls `BattleUnit_HasRelationshipClass2PlusInTrackedActorList` `0030B050` and is called by `WorldActor_QueryCombatStanceState` `0030BFB0`; the level-set `0030C470` is called by `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0`; `BattleUnit_ComputePresentationSuppressionMask` `003125E0` calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0` and is called by `BattleUnit_IsPresentationEnabled` `003126E0`, which `00328530` calls; `0031B810` is called by `00234150` and `BattleUnit_CollectMappedFourSlotUnitsByFlags` `0030A8A0`; and `00307D10`, `0030A8A0`, `BattleUnit_HasRelationshipClass2PlusInSlotMask` `0030C210` and `0030D9A0` call `00377C20`. These are the shared battle-runtime helpers (id validation, presentation-event dispatch, engagement tests, the battle-mode query) that the record's writers call and that other gameplay bodies call too; none of them owns a stats field.

**Script_VM_Native_Bridge — CLIENT (34 edges).** 23 verb bodies call `00265020`, among them `0033FD60`, `00345180`, `003478A0`, `0050E060` and `0050F6E0`; `00344740` and `003509E0` call `00233D70`; `0050F360` calls `00235A70`; `0050FAF0` calls `002FAFD0`; `00342230` calls `00328BD0`; `00351A40` calls `00328FB0` and pops its argument with `VMValueStack_PopInt32CoerceFloat32` `00267E10`; and `00344740`, `00352FA0`, `003537D0` and `00355680` call `00377C20`. Script verbs reach the record's accessors directly: they read actor positions, call writers such as `00233D70`, `00235A70`, `002FAFD0`, `00328BD0` and `00328FB0`, and ask the field predicate.

**Spawn_Encounter_Lifecycle — CLIENT and SERVICE (9 edges).** `Spawn_TrySelectCandidatePosition` `00234AF0`, `Spawn_ValidateCandidateDistanceToPlayers` `00234DA0` and `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` call `00265020`, and `00234DA0` and `002350C0` also call `0031B810`; `00300530` calls `SpawnGroup_RecordMemberDeathAndHandleCompletion` `00306F00`; `00308040` calls `00234DA0`; `002398F0` calls `0030C470`; and `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` calls `0030FED0`. A spawn sets a new unit's level and recompute through two of the record's writers, a death recorded by the HP write reaches the spawn group, and the spawn range tests read positions and definition selectors through the same accessors.

**UI — CLIENT and SERVICE (26 edges).** `BattleMenu_BuildCommandEntryList` `0031EB20` calls `BattleAction_ComputeModifiedResourceCostAmount` `002F95D0`, `BattleAction_CheckUnitActionAvailability` `00306480` and `00322360`, and `00322A80` also calls `00322360`; 12 licence-board screen bodies from `00557B90` to `005618E0` (19 edges; among them the node check `005587E0`, `00560210` and `005618E0`) call the board-selector getters `BattleStats_GetLicenseBoardSelectorB` `00323630`, `BattleStats_GetLicenseBoardSelectorA` `00323670` and `BattleStats_GetActiveLicenseBoardSelector` `003236B0`; `003C5130` calls `00265020`; `00306760` calls the propagation step `0035C620`; and `00328BD0` calls the mode-bit setter `00313550`. The battle menu prices and gates each command from record fields through this map's readers, and the licence-board screens read which board a member is on from the record's selector fields.

## `FE-1` — every instruction that reaches the flags word: five, on two bits (OPUS, 2026-09-14, corrected)

**This section replaces an enumeration published earlier the same day that was wrong.** The first
version is quoted below with the defect that produced it, because a census that was wrong once is
only trustworthy again if the reason it was wrong is on the page.

The record is reached as `qword [unit + 0x698]`, so every access to the flags word is findable. Read
from the shipping image at the authority hash `73461D08…9721F8`.

### The census

| site | function | what |
|---|---|---|
| `00328FD5` | `FUN_00328FB0` | `or dword [rax], 1` — **set bit 0** |
| `00328FDE` | `FUN_00328FB0` | `and dword [rax], 0xFFFFFFFE` — **clear bit 0** |
| `00328E5B` | `PartyConfiguration_ReconcileRuntimeRosterFirstThreeFromRequestedSelectors` | `test byte [rax], 1` — **read bit 0** |
| `00305BFB` | `BattleUnit_SelectAndCommitNextAction` | `mov eax, dword [rcx]` → `shr 2` / `and 1` — **read bit 2** |
| `0030BCE9` | `FUN_0030BCD0` | the same three instructions — **read bit 2** |

**Five instructions, four functions, two bits.** Bit 0 has one writer pair and one reader; bit 2 has
two readers ~~and no writer~~ in this census; its writers store through a register at displacement 0 (`0023AF28`, `00239D89` / `00239D94`) *(answered: see §7, `UQ-123`, 2026-09-14; whether this sweep should see them is the open `FE-1` reconcile below; 2026-10-02, OPUS)*. No other bit is touched at all — not read, not written.

**What that census is a census OF, stated before anyone has to ask.** It is the `+0x698` access
path, which §2.1 calls *“the access path 82 readers use”* — every instruction reaching the word
through a pointer loaded from `[unit + 0x698]` **in the same function**. The record has at least two
other homes, and this sweep sees neither: the kind-`0` record is an element of the battle-state
array at `*(02EBF190) + 8 + slot × 0x1C8`, reachable by walking the array, and the kind-`1` record is
`spawnkeep + 0x80`. A function that indexes the array directly, or that receives the record as an
argument, is outside the sweep by construction. **That is where `UQ-123`'s bit-2 writers have to be**,
and saying so is the point of writing the bound down rather than letting *“no writer anywhere”* stand
as if the whole of `.text` had been read.

### What the flags word is, from the gate its readers share

Both bit-2 readers take the same shape, and it says which side of the game the word belongs to:

```
00305BE7  mov   rcx, qword [rbx + 0x698]   ; the stats record
00305BF3  movzx eax, byte  [rcx + 5]       ; the kind byte
00305BF7  test  eax, eax
00305BF9  jne   <skip>                     ; kind != 0 -> not this path
00305BFB  mov   eax, dword [rcx]           ; kind 0 (party) -> read the flags word
```

Kind `0` is the party arm (§2.2's kind byte; the applier's step 16 runs on kind `1`). So **the flags
word at `+0x00` is read only for party-kind records**, which is what makes FABLE's reading of bit 2 —
a party-only flag — structurally rather than incidentally true, and why bits 1 and 3–31 having no
accessor is unsurprising rather than suspicious.

### The four instructions withdrawn, and where they actually live

`00233BA8`, `00237DD7`, `00308073` and `003126BE` were published as touching this word. **They do not.**
All four sit in bodies with this exact idiom:

```
00308052  mov rax, qword [rcx + 0x698]     ; the stats record
0030805C  je  <out>
00308062  cmp byte [rax + 5], 1            ; kind 1 -> the FOE arm
0030806C  mov rax, qword [rcx + 0x6A0]     ; A SECOND RECORD, into the SAME register
00308073  mov ecx, dword [rax]             ; the bit work is on THAT record
```

The `+0x698` load is a guard; the bit work is on `[unit + 0x6A0]`, reached only after the kind byte
reads `1`. **That record is already identified, and its bits are already answered.**
[The battle-record kind byte](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md)
establishes that `unit + 0x6A0` is the **spawn-keep entry** (`SpawnRecord`, `0x250` bytes) and that
`unit + 0x698` is that entry `+0x80` for a kind-`1` unit — and **NULL at `+0x6A0` for a kind-`0`
party unit**, which is exactly why all four sites test the kind byte before dereferencing it. Its
word `+0x00` is `AL-10`, answered 2026-09-12 from its writers: bit 0 range-retired, **bit 1
`ACTIVATION_COMMITTED`**, bit 2 slot released, bits 3 / 6 lifecycle point mode, bit 4
`RANGE_RETIRE_INHIBITED`, **bit 5 category-4 mode**, bit 7 affinity dirty.

So every withdrawn instruction lands on a bit that already has a name, and the names corroborate the
reattribution rather than merely permitting it:

| withdrawn from `FE-1` | on the spawn-keep word | already answered as |
|---|---|---|
| `00233BA8` `or dword [rax], 2` in `BattleUnit_ActivateAppliedDefinitionRuntime` | bit 1 | `ACTIVATION_COMMITTED` — the function's own name |
| `00237DD7` `and dword [rax], 0xFFFFFFDF` | bit 5 | category-4 mode, cleared |
| `00308075` `test cl, 0x20` / `0030807E` `test cl, 0x48` | bits 5, 3\|6 | category-4 mode; lifecycle point mode |
| `003126C0` `test cl, 0x10` / `003126C8` `test cl, 8` | bits 4, 3 | `RANGE_RETIRE_INHIBITED`; lifecycle point mode |

**`FE-1`'s bits 1 and 5 do not gain writers**, and FABLE's *"bits 3, 4, 5 and 6 are read"* was reading
answered spawn-lifecycle bits as unexplained stats-record ones. The word at `[unit + 0x6A0] + 0x00`
has **51 accesses at 109 load sites**; it sits `0x80` bytes before this record on the kind-`1` path
and has no relationship to it at all on the kind-`0` path.

### The defect, exactly

The earlier sweep bound the destination register of the `+0x698` load and then looked for the next
`dword [reg]` access — but **never killed the binding when the register was redefined**. In all four
bodies the second load targets the *same* register (`rax` → `rax`), so the sweep carried the name of
one record onto the contents of another. Shape and register agreed; only the dataflow disagreed.

The replacement kills a register on redefinition, follows a `mov rD, rS` copy, and refuses to walk
past the end of the owning function (`functions.tsv` entry + `body_bytes`). Two controls:

- **Copy-following changes nothing.** The census is five sites with and without it, so the earlier
  sweep's blindness to copies was not also hiding a site.
- **The boundary guard removed two more.** Without it the walk ran from `0031C580` into the next
  function's prologue and reported `0031C5EA` — a different function's `rcx`.

### The one exclusion, and why it is not special pleading

`001CC348` (`mov dword [rcx], eax`, `rcx` from `[rbx + 0x698]`) matches on every mechanical test and is
**not** a stats-record access. `FUN_001CA600` walks a contiguous stride-8 run of pointer slots from
`+0x600` to `+0x6F8` — thirty-four of them — feeding each a named value from the parameter registry at
`01F81318`; the slot at `+0x698` is fed `"NobuMessageSelectOffsetY"`. `+0x698` there is slot 19 of a
settings table, not a battle unit. This page's own neighbours section already reads that function and
that registry for the Presentation crossing, so the exclusion is checkable against material that was
on the page before this section existed.

### What the first version said, for the record

> *Every instruction in the image that touches `dword [[actor + 0x698]]`* — eight, including
> `00233BA8` setting bit 1, `00237DD7` clearing bit 5, and four readers `00305BFB` `00308073`
> `0030BCE9` `003126BE` “**confirmed as exactly four**”, plus one alignment `nop`. *“Two bits that had
> no named writer now have one.”*

Four of those seven were the wrong record; the `nop` was the operand-shape defect showing itself and
being explained away instead of taken as the warning it was.

### What stays open

`FE-1`'s bit 2 still has no writer on this pointer. FABLE's `UQ-123` narrowing puts its writers in
stats init and the area-state party walk “at displacement 0 that the census could not see” — but a
displacement-0 store through a pointer loaded from `+0x698` is exactly what this sweep does see, and
there is none. So either those writers reach the record by a pointer that never passes through
`unit + 0x698` in the same function, or the narrowing needs the same treatment this section just gave
its own predecessor. That is the next read, and it is bounded.

*(Read by OPUS 2026-09-14, correcting OPUS 2026-09-14 and withdrawing FABLE's correction of the same
day on the same four instructions. `FE-1`'s answer — a flags word, bit 0 the battle-member lock, bit 2
the AI-driven-member flag — is unchanged and better supported: the word is now known to be a two-bit
field on the party arm rather than a word with unexplained neighbours.)*

## The `0031BDC0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0031BDC0` (~157 B) — `movsxd rdi, edx`, `edi < 8` bound
(`0031BDCA`/`0031BDD0`).

| member | role | interior |
| --- | --- | --- |
| `00322560` | `movzx word[rcx]` + `r8d = 0`, `edx = edi` (`0032256A`/`00322570`) | [`0032256A`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-25 update (2026-09-18) — `00322360` stats-record compose

`00322360` (89 B) is cookie-checked (`00808C40`): pulls `[rcx+0x10]`,
`00265020`-queries it into three stack outs, zeroes `xmm0` at `+0x2C`,
then `003223C0` composes — the record-into-stat marshal. Interior anchor
`0032238B` (the `00265020` call).

## SWE2-EC7-35 update (2026-09-19) - `00470780`

`00470780` (798 B) is a stats record processor - `byte[rcx+0x3A]` gate, `01DFE0BC`/`01DFE0B4` state, six `00428CD0` plus `003ABCA0`/`0046FBB0`/`00320CF0`/`00263E50`. Interior anchor `004707F0` (a `00428CD0` call).

## SWE2-EC7-50 update (2026-09-19) - `003223C0`

`003223C0` (180 B) is the record-into-stat marshal - `00263940`/`00265090`/`0046C0D0`/`00808C40`. Interior anchor `003223E9` (a `00263940` call).

## SWE2-EC7-96 update (2026-09-20) - `0030D600` measured

`0030D600` (273 B) is the two-pass slot collector `00309C40`,
`0030D550` and `0030D810` call: `esi` 0-3 feeds `0031B810`, each
hit's `[+0x698]` is gated by `+0x64 | +0x3C` against `0x80000003`
with a `00377C20` re-check, `byte[+5] == 0` and `byte[+4] <= 6`
admit up to four into the `02CD1790` staging table; the second
pass re-filters on the `0x8800203B` mask plus `00324020 > 0` and
writes survivors into the `rbp`-rooted out array, `[r15]` taking
the count.
Interior anchor `0030D636` (the first `0031B810` call).

## SWE2-EC7-105 update (2026-09-20) - `00263E50` measured

`00263E50` (22 B) is the guarded trampoline
`00470780` and `00470B70` call: when `rcx`
and `[rcx + 0x30]` are both non-null it
tails `0031B750` with the `[+0x30]` record;
either null answers `-1` - the
presence-check in front of the shared
resolver.
Interior anchor `00263E55` (the `+0x30`
load).

`003203B0` (160 B) is the `0x1000`-biased table probe: `dword[rdx]` presets -1, the `02EBF0F8` descriptor's `(cx - 0x1000) * word[+8]` row is taken only when `byte[+7] < 0x20` (else `edx` stays -1), then `02EBF180`'s byte matrix at `word[*] * edx + 4` supplies the written value - the secondary-index read the stats, state-block and save callers share.

Interior anchor `003203F9` (function `003203B0`).

`0031A260` (153 B) is the five-lane probe `00328BD0` (the `resetJobs` verb's result handler) runs: a stack sentinel pair `{qword -1, word 0xFFFF}` seeds the scan, then `0031A410(ecx = arg, edx = i, r8d = word[rsi+i*2], r9d = 1)` is tried for `i` in 0..4; `ebx` latches on any non-negative return and the body returns `0` when at least one lane passed, `-1` otherwise.

Interior anchor `0031A2BB` (function `0031A260`).
