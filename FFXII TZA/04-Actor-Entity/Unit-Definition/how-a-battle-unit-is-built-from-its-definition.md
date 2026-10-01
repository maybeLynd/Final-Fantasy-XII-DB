---
system: How a battle unit is built from its definition — the two tables, the two paths, and every field the installer writes
category: 04-Actor-Entity
status: DOCUMENTED
owner_layer: PrimaryOwner:ActorEntity (the installer) — the stats-record initialiser is CombatFormula
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: BattleUnit_ApplyUnitDefinition (1,808 B) and BattleStats_InitializeDefinitionRecord (717 B)
    read to every ret from the shipping EXE with every RIP target computed by a tool; the writers of
    unit +0x698 / +0x6A0 / +0xE68 enumerated by a from-entry displacement sweep with a positive
    control; caller counts checked with check_caller_claims (control memcpy 632)
last_reviewed: 2026-09-22
registry_slots:
  - "0x02EBF120"
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-how-a-battle-unit-is-built-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
production_review: "SECTION-01 corrections; prior audit metadata is historical, current T2 peer review pending."
---

# How a battle unit is built from its definition

> A battle unit becomes *something* — a party member with her equipment, licences and gambits, or
> an enemy with its spawn record, steal slots and spawn count — in one function, from one 16-bit
> definition id. The id's high byte picks which of two authored tables the unit is built from and
> where its stats record lives; the low byte is the row. This page reads both paths and every
> field they write.

> **SECTION-01 (2026-09-22):** current corrections and bounded execution are recorded in
> [the contract](CONTRACT-battle-unit-construction.md) and
> [the review](../../_experiments/evidence/continuation-section01-result-install/REVIEW.md).
> In particular: tracked writes are conditional on nonzero code or a negative slot;
> class 1's float is unscaled; both cited failure masks clear bit26. EXP-150's local
> case names do not override the party=0/enemy=1 mapping.

## 1. What the player sees

The moment a character joins the party, or an enemy appears in a zone, its stats, equipment,
licences, gambits, steal table and enemy-history counter are populated from authored data. **A
definition id is a class byte and a row**: ids `0x0000`–`0x00FF` are party characters, built from
the party table and kept in the save image; ids `0x0100`–`0x01FF` are enemies, built from the
area's enemy table into a spawn record. The same installer serves both, and the same 456-byte stats
record is the result — which is why every later system can test one byte, `[+0x698] + 5`, to know
which kind it is holding.

## 2. Native mechanism

### 2.1 The entry, the reset, and the class split

`BattleUnit_ApplyUnitDefinition(BattleUnit *unit /*rcx*/, uint16_t id /*edx*/)` (`0023A570`,
1,808 B; three callers, section 5). It splits the id at once — `esi = id >> 8`, `r12d = id & 0xFF`
(`0023A580`–`0023A594`) — remembers the unit's previous id (`+0x698` word `+4`, `0023A5A1`–`0023A5A8`,
`0xFFFF` when the unit has no record), and **resets the unit** with `BattleUnit_ResetStateForReuse`
(`00236A60`, at `0023A5B0`), which among much else nulls `+0x698`, `+0x6A0`, `+0xE60` and `+0xE68`
(`00236AB4`–`00236AC9`). With the battle system down (`02089300 == 0`, `0023A5B5`) it returns `0`.
Rekey is broader than a change on the current selection: the selected-teardown path
can bypass it (`0023A5CD`–`0023A5F2`); otherwise a nonzero incoming class byte, or a
saved old ID differing from both the incoming ID and `0xFFFF`, selects `00322050(unit)`
before the class validity branch. A class-2 request can rekey and then return 0.
The wrapper is 44 B — **read 2026-09-11 (ASTRA-REQ-FABLE-RESET-WRAPPERS)**:
it zeroes the unit's attacker mask `+0xEA4` and attacker count `+0xEA8` (`00322059`–`00322063`),
calls `003220E0` with the unit's actor `[unit+0x10]` (`0032206A`–`0032206E`) and stores what comes
back into the unit's `+0x08` handle (`00322073`). `003220E0` (`003220E0`–`0032218F`) encodes the
actor's current handle (`003589B0`), advances the actor's `+0x16` discriminator (`002659D0` at
`00322107` — [the slot-pool page](../battleunit-slot-pool-and-actor-class.md) §11), encodes the
new handle, and, if the party-focus record's `+0x08` held the old one (`00327150`, `00322129`–
`0032212E`), re-points the leader selector at `02EBF190 + 0x5AA4` to the re-keyed unit's type byte
(`00322139`–`00322179`); it returns the new handle. The actor-side twin `00322080` does the same
through the actor's back-pointer and tail-calls the delegate when there is no unit. So a definition
change can **re-key its handle and forget tracked attackers before a later rejection**;
this is not a claim that every external handle copy is rewritten. ASTRA's
EXP-047 executed the two wrappers' local stores in isolation; the delegate's effects are the static
reading above.

```
0023A626  test esi, esi / je 0023AA49          high byte 0  -> the PARTY path (2.3)
0023A62E  cmp esi, 1 / je 0023A641             high byte 1  -> the ENEMY path (2.2)
0023A633  and [unit], ~(1<<26) ; return 0      anything else -> nothing installed
```

Both paths end at the same store sequence (section 2.4). `BattleUnit_TeardownAndDespawn` calls the
installer with `0xFFFF` (`00300F6D`–`00300F75`), which is the third case: **tear-down is
"apply no definition"**.

### 2.2 The enemy path — a row in the area's enemy table, a spawn record, a `+0x80` page

> *CB-4 answered 2026-09-12 (FABLE):* the index that selects the `.ard` slot-2 (enemy) row is
> **`r12d = id & 0xFF`** from the split in §2.1 — the definition id the callers pass (`Spawn_ApplyScriptSelectedUnit`
> at `0023A3F1` with the script-selected id, `BattleGroup_RefreshFourActorDefinitions` with 0) — bounded at
> `0023A65F` by the table's count dword at `+4` (`0023A656`), and the chosen row's word `+0` then indexes
> the slot-0 class table `02EBF150` under the same count check (`0023A6B4`–`0023A6BB`).

| step | site | what |
|---|---|---|
| gate | `0023A641`–`0023A648` | unit flags bit 26 must be set |
| the row | `0023A64A`–`0023A69F` | `row = 02EBF120.base + r12 × stride` — registry slot `02EBF120`, the `.ard` enemy table [the ARD loader](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md) §4 owns; bounds-checked against its count at `+4` (`0023A65F`) |
| four cross-references | `0023A6A1`–`0023A76E` | the row's words `+0x00`, `+0x50`, `+0x22`, `+0x24` are each compared against another slot's count — `02EBF150` (dword `+4`), `02EBF168` (**word `+0`**), `02EBF148`, `02EBF140` (dword `+4`) — as `index > count − 1` → return `0` (`0023A6BB`, `0023A726`, `0023A747`, `0023A768`). **Qualified 2026-09-12 (ASTRA-CONTRA-FABLE-REWARD-COUNTZERO, EXP-075):** three of the four are **unsigned** (`ja`), so for a **positive** count they reject `index ≥ count` before the spawn lookup and before any reward store — but at **count 0, or with the descriptor missing** (a null slot reads as count 0), `dec` wraps `count − 1` to `0xFFFFFFFF` and no 16-bit index is above it: the guard passes everything and the row address is then computed unchecked (`base + index × stride`), or stored as `0` when the descriptor / resolver is absent (the late branches at `0023A96F` / `0023A97C` and `0023A9B6` / `0023A9C3` test the descriptor pointer and `0020E600`'s result, **not** the index). The `+0x50` guard is the odd one: a **signed** `jg` against a **16-bit** count (`CB-2`), so at count 0 it does the opposite and rejects every index. "Any failure returns 0" therefore holds for positive counts only; a zero count or a missing table is a different case and must not be described as the same rejection. EXP-075 executed the two reward guards (`+0x22`, `+0x24`) at `index = count`, `count = 0`, `count = 65535 / 65536` and with the descriptor missing (fourteen controls, both `JA→JB` mutants detected); the `+0x00` and `+0x50` count-zero instruction readings also have later retained EXP-150 fixture coverage. SECTION-01 did not rerun that full campaign. These are the five ARD categories the loader page decodes; the row references all four siblings |
| the spawn record | `0023A76E`–`0023A781` | `rbp = SpawnKeep_ResolvePrimaryEntry(unit->p_40, unit->b_57)` (`00236100`, the lane map and the lane byte the bind wrote) — **the `0x250` spawn record**; none → return `0` |
| the page | `0023A787`–`0023A795` | `page = record + 0x80`, kept at `[rsp+0x90]` |
| fresh record only | `0023A791`–`0023A7E4` | if the record's byte `+0` has neither bit 0 nor bit 2: `BattleStats_InitializeDefinitionRecord(page, id)` (`0023A7A9`, section 2.5), then **the steal bits**: record `+0x14 = 0`, bit 0 if the row's word `+0x32 != 0xFFFF`, bit 1 for `+0x34`, bit 2 for `+0x36` (`0023A7B2`–`0023A7E4`) |
| the spawn counter | `0023A7E7`–`0023A840` | if the row's byte `+2 != 0xFF`: `bx = *(u16*)(02089340 + 0x4014 + ((byte 0208D454 << 6) + byte2) × 2)`; if `bx < SpawnHistory_GetCounterWrapThreshold()` the word becomes `bx + 1`; **record `+0x12 = (u8)bx`** — a per-area (the byte at `0208D454`), per-row-byte-2 counter of 64 words each, incremented on every fresh spawn until the wrap threshold, its pre-increment value kept on the record |
| the definition object | `0023A843`–`0023A8E1` | `+0xE60`-bound: through `02EBF120` again and the row's word `+8 >> 11` into `02EBF170` (`0023A88A`–`0023A89D`), then `002B58B0(that)` → `r14` — an unread resolver (`FB-1`) |
| six fields read | `0023A8E6`–`0023A910` | ~~from the **page** (`r15 = [rsp+0x90]`)~~ **corrected 2026-09-12 (FABLE): from the `.ard` slot-0 class row** — `r15 = 02EBF150's base + stride × the spawn row's word +0x00` (`0023A6F0`–`0023A6FC`; `[rsp+0x90]` is reloaded into `r15` only later, at `0023AA15`): bytes `+4` (type), `+5` (kind — the unit's `+0x56`), `+0x22`, `+0x23`, `+0x27`, word `+6` |
| the two pointers | `0023A915`–`0023A91C` | **`+0xE60 = row`** (the spawn row, `rsi`), **`+0xE68 = ~~page~~ the slot-0 class row`** (`r15`; corrected 2026-09-12 — the page reaches `+0x698` at `0023ABFA` after `0023AA15` reloads `r15`) |
| `+0x6E0` | `0023A92F`–`0023A95E` | `02EBF168` row selected by the row's word `+0x50`, relocated — or `0` *(variant 0 of the four set indices at `+0x50`–`+0x56`; `btlAtelSetDefaultLogic` and direct commands `0x4112`–`0x4115` reselect by `k` — CB-1, 2026-09-12)* |
| `+0xE70` | `0023A965`–`0023A9A5` | `02EBF148` row selected by word `+0x22` — or `0` |
| `+0xE78` | `0023A9AC`–`0023A9F4` | `02EBF140` row selected by word `+0x24` — or `0` |
| `00328FF0` | `0023A9EC`–`0023AA04` | `(0, row byte +3 & 3, unit byte +0xEA9)` — registers the unit in the two-entry tracked-HP table `02EC1380` (§2.9) |
| bit 43 | `0023AA09`–`0023AA44` | row byte `+3 & 3` or byte `+0x15 & 4` → unit bit 43 **set**, else **cleared**; `r15 = page` reloaded for the stores |

> *The class row's word `+0x52` (2026-09-12, FABLE):* the installer copies it to unit `+0x52`
> (§2.4), and `0031B9A0` returns it as the unit's **Clan Primer entry id** — 0–376 over the shipped
> rows, `0xFFFF` on 107 of 954 — the index of the bestiary's 512-byte sighting / defeat block at save
> payload `+0xB404` ([event memory at actor bind](../../14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md) §3).

### 2.3 The party path — a row in the party table, a state-block element, no spawn record

| step | site | what |
|---|---|---|
| gate | `0023AA49`–`0023AA60` | `BattleEncodedId_IsValidForClass(2, r12, 1)` (`00322C50`) must hold |
| the row | `0023AA66`–`0023AAA8` | `row = 02EBF130.base + r12 × stride` — registry slot `02EBF130`, the party table (the registry page records its 456-byte rows and declines to name it) |
| **the stats record** | `0023AAAA`–`0023AAC1` | **`r15 = *(02EBF190) + 8 + r12 × 0x1C8`** — element `r12` of the battle-state block's 40-element array; **`rbp = 0`** (`0023AAB1`): no spawn record |
| the definition object | `0023AAC4`–`0023AB5A` | through `02EBF130` and the row's word `+0x30 >> 11` into `02EBF170` (`0023AB03`–`0023AB16`), then `002B58B0` → kept at `[rsp+0x90]` and loaded into `r14` |
| `+0x6E0` | `0023AB64`–`0023AB9F` | **`02089378 + index × 0x170`** — a per-character block outside the registry |
| `+0x6F0` | `0023ABA6`–`0023ABB5` | the constant address `01E09350` |
| the pointers | `0023ABC3` | **`+0xE60 = row`**; `+0xE68` is not written on this path |
| the floats | `0023AB6B`–`0023ABD6` | `+0x64 = 2π` (`01CEBC78`, not divided on this path), `+0x6C = row byte +0x2B × 1.5` (`00901B3C`), `+0x68 = (float)row byte +0x2B` |

### 2.4 The common stores

At `0023ABCA`–`0023AC58` both paths write, in order: `+0x64`, `+0x6C` (enemy: `byte +0x22 × 2π / 360`
and `float(byte +0x27)` without the scale, `0023A927`–`0023A93D`; `0023ABAD`'s ×1.5 is on the party branch), **`+0x48 = 0`** (`0023ABDB` — the HP
floor the HP write clamps to, zeroed at every definition apply), `+0x55 = byte +4` (the type),
**`+0x698 = r15`** and **`+0x6A0 = rbp`** (`0023ABFA`, `0023AC01`), `+0x18 = r14`, `+0x68`,
`+0x56 = byte +5 (or −1)`, `+0x52 = word +6 (or −1)`, `+0x54 = 0xFF`, then `00237040()` — the
engaged-state decision, flag bit 23 — and `002FEAB0(unit)` — the HP-stage pulse reset (both §2.9), and the terminal test: a record whose `(+0x64 | +0x3C) & 0x80000003` is
set without the accepting terminal gate gets unit bit 26 cleared and bit 1 set (`0023AC29`–`0023AC52`); bit 2 is
set for everyone (`0023AC56`); return `1`.

~~**So `BattleUnit +0x698` is the same thing on both paths — a `0x1C8`-byte stats record — with two
homes**: inside the enemy's spawn record at `+0x80` (`0x80 + 0x1C8 = 0x248 ≤ 0x250`), or in the
save-image state block's array.~~ *Reworded 2026-09-13 (FABLE) so it cannot be read as one interchangeable record:* `+0x698` always points at a `BattleStatsRecord`, and **which record is fixed by the definition kind**: kind 0 (party) → the BattleSystemState element `*(02EBF190) + 8 + slot × 0x1C8`; kind 1 (spawn-backed) → the record embedded in that unit's own SpawnKeep entry at `+0x80` (`0x80 + 0x1C8 = 0x248 ≤ 0x250`). These are **different records belonging to different units**, not one record reachable from two places, and `+0xE68` is a third, unrelated object — the `.ard` slot-0 class row. `+0x6A0` is the enemy-only pointer to the enclosing spawn record.
This is what `OPUS-CONTRA-BU698` asked; [the kind byte page](../Battle-Record-Kind/battle-record-kind-byte.md)
§2 now carries the correction.

### 2.5 `BattleStats_InitializeDefinitionRecord` — what a fresh stats record gets

`0023AC80(page /*rcx*/, id /*edx*/)` (717 B; callers `BattleSystem_ResetRuntimeState`,
`00239960`, and the enemy path above):

| step | site | what |
|---|---|---|
| zero | `0023ACA4`–`0023ACBD` | `memset(page, 0, 0x1C8)` — **the stats record is 456 bytes** |
| sentinels | `0023ACC2`–`0023ACDD` | `+0x50 = -1` (qword), `+0x58 = 0xFFFF`, `+0x1C3 = 0xFFFF`, `+0x1C5 = 0xFF` |
| the row | `0023ACF3`–`0023AD79` | kind 1 → `r14 = 02EBF120` row; kind 0 → `rbp = 02EBF130` row; else return `0` |
| the id | `0023AD8E` | **`page +4 = id` (u16)** — the low byte is the type, **the high byte is the kind byte every gate tests** |
| level | `0023AD7B`–`0023AD96` | `0030C470(page, level, kind)` with `level = row byte +0x2E` for kind 0 (min 1), `1` for kind 1; `kind` is `r12d` = 1 on the enemy branch (`0023AD37`–`0023AD3C`), 0 otherwise (`0023ACB5`) — **section 2.6** |
| equipment, enemy | `0023ADA8`–`0023ADFA` | `BattleStats_SetEquipmentSlotDirect(page, 0, row word +0x1C, 0)` then slots 1–3 with `0xFFFF` — **an enemy has one equipment slot, from its row's `+0x1C`** |
| equipment, party | `0023AE8C`–`0023AEE9` | slots 0–4 from the row's words `+0x0A`, `+0x0C`, `+0x0E`, `+0x10`, `+0x12` |
| `00323790` | `0023AE04` | `(page, row word +0x44)`, party only — **the LP setter**: `+0x190 = clamp(+0x190 + delta, 0, 99,999)` (section 2.6) |
| **licences, party** | `0023AE10`–`0023AE8A` | for party index `esi ≤ 6`: over every entry of the table at registry slot `02EBF038` (count at `+4`), if the entry's byte `+7` has bit `esi`: `BattleStats_SetLicenseNodeStateAndApplySideEffects(page, entry, 1, 1)` — **each licence node carries a 7-bit "owned from the start" mask, one bit per character** |
| gambits, party | `0023AEEE`–`0023AF1D` | `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders(page, row word +0x14)`, `GambitConfig_InitializeThreeBanksFromBasePairs(state, index)`, `GambitRuntime_RebuildOrderSetForStatsRecord(state + 8 + index × 0x1C8)` |
| flag | `0023AF22`–`0023AF28` | row byte `+0x2C` bit 6 → page `+0` bit 2 |

### 2.6 The level grower — `0030C470(page, level, kind)`

432 B; six call sites in six functions (`check_caller_claims`, control 632): this initialiser
(`0023AD96`), the area-state party walk `00239960` (`00239BED`, with `kind = 0`), `002398F0`,
`BattleAction_UpdateSpecialPresentationSequence` (`00306760`), `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects`
(`00316DF0`) and `00317480`. It is the function that turns an authored row into a levelled stats
record, and it does it by **resetting the level to zero and growing back up**:

| step | site | what |
|---|---|---|
| reset | `0030C488`–`0030C4A2` | reads `+4` (row index, `r14`) and `+5` (kind, `esi`); **`+0x1C2 = 0`** — the level byte [the level-up page](../../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md) §2 identifies as the authority |
| kind 1 | `0030C4A8`–`0030C4B8` | **`+0x88 = kind` (u8)** — the third argument, stored on the enemy branch only — then straight to the growth |
| kind ≥ 2 | `0030C4AB` | return; nothing is grown |
| kind 0: base stats | `0030C4BD`–`0030C54F` | `row = 02EBF130 + stride × +4` (the party table again, this time by the record's own index); **`+0x08 (u32) = row.w_16`; `+0x0C (u16) = row.w_1A`; `+0x10`, `+0x14`, `+0x18`, `+0x1C` (floats) = `(float) row.b_1E`, `row.b_21`, `row.b_24`, `row.b_27`; `+0x20 (u8) = row.b_46`** — the four float stats sit three bytes apart in the row, and the level-up page's growth bytes are `+0x1F`, `+0x22`, `+0x25`, `+0x28`: **each stat is a (base, growth) byte pair** |
| the licence rank | `0030C552`–`0030C55F` | `BattleStats_ComputeLicenseDerivedRank(page)` (`00324100`, 198 B, this is its only caller): starts from `BattleStats_CountLicenseBits00To17(page)` (`00324020`), then for licence nodes `0x12`–`0x1E` present in the record's ownership bitmap at **`+0x194`** (`00324147`), takes the largest `BattleAction_ComputeSecondaryResourceMultiplier(0, entry.w_08)` (`00308FF0`) over the `02EBF038` entries (`00324150`–`00324197`); `+0x20 = max(row.b_46, that)` (`0030C557`–`0030C55F`) |
| growth | `0030C562`–`0030C56E` | **`BattleStats_AdvanceLevelToTargetAndRecomputeGrowth(page, level, 2)`** (`0030C650`) — from level 0 to `level`, growing `+0x08`–`+0x1C` per level as the level-up page §4 reads; the third argument **2 has bit 1 set, which that page's §5 decodes as the silence flag** — so the initial growth plays no fanfare. That page's "both known callers pass 0" was written before this third caller was read |
| the experience total | `0030C573`–`0030C586` | **`+0x18C = min(002F8F20(level − 1), 99,999,999)`** — the accumulated-experience field the death page walks, set to exactly the threshold of the level just reached (section 4 for the curve) |
| strip every status | `0030C58C`–`0030C59D` | `mask = [0208D320] \| [0208D324]`; if non-zero, `BattleStats_RemoveStatusesFromMaskAndRecompute(page, mask)` (`0030F690`, 196 B): for every set bit *s*, `0030E360(page, 0, s, 0, 0, 0x217, 0)` — the same removal shape as [the status write](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md)'s cascade — and, for *s* = 0 on a unit whose status words carry none of bits 0 / 1 / 31 or where `FieldData_GetActiveFieldRecordBit15` (`00377C20`) is clear, **unit flag bit 26 cleared** (`0030F6C5`–`0030F6FC`); then `0030FED0(page, 0x217)` (`0030F72D`–`0030F735`). The two masks are built once by `00237CA0` (186 B, reached by a jump thunk from `00236A40`) from `status_data` rows 0–31: a row whose word `+6` has bit `0x2000` goes to `0208D320`, every other row to `0208D324` (`00237CF0`–`00237D3D`) — so the OR is **every status that has a definition row** |
| HP to capacity | `0030C5A2` | `BattleStats_ReconcileCurrentHpToEffectiveMaximum(page)` (`0030F340`, 172 B): `target = bit 16 of (+0x3C \| +0x64) ? max(+0x48, 1) : +0x24, doubled when bit 28 is set` (`0030F34E`–`0030F37C`); if `+0x48` differs, a kind-0 unit of type `0x1B`–`0x27` at `+0x48 ≤ 0` first gets `003243F0(owning unit)` (`0030F383`–`0030F3A7`), then **`00300530(page, target − +0x48, 0, 0x217)`** (`0030F3CD`–`0030F3DC`) — [the HP write](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md) |
| MP to capacity | `0030C5AD` | `BattleStats_ReconcileResourcesToEffectiveCapacity(page)` (`0030F5A0`, 233 B): `cap = (+0x6C ≥ 0 && +0x7C ≥ 0) ? +0x28 : 0`; `+0x4C` brought to `cap` through `BattleStats_ModifyPrimaryResource(page, cap − +0x4C, 0x217)` (`00300CE0`; `0030F5CE`–`0030F5FD`), `+0x06` raised to `cap` if below it (`0030F602`–`0030F617`), then `+0x06` brought to `cap × (+0x37 ≠ 0 ? +0x37 : 1)` through `BattleStats_ModifySecondaryResource(page, Δ, 0x217)` (`00300BC0`; `0030F621`–`0030F679`) — [where MP comes from](../../10-Status-Periodic-Terminal/where-mp-comes-from.md) names `+0x4C` live MP and `+0x28` capacity |
| the starting MP | `0030C5B2`–`0030C5F9` | after the reconcile: **kind 1: `+0x4C = +0x28`**; **kind 0: `+0x4C = +0x28 × row.b_47 / 100`** (`imul` by `0x51EB851F`, `sar 5`: the ÷100 idiom, `0030C5E5`–`0030C5F9`); in both, `+0x28` reads as 0 when either layer byte `+0x6C` / `+0x7C` is negative — **a party character starts with an authored percentage of its MP** |
| recompute | `0030C5FD`–`0030C602` | `BattleStats_RecomputeDerivedStateAndAutoStatuses(page, 0)` (`0030FED0`) — [the auto-status rebuild](../../08-Combat-Formula/the-auto-status-rebuild.md) |

**What `003243F0` (95 B; callers `0030F340`, `00324450`) does for a party unit revived by the
reconcile:** `003105D0(unit)`; if the unit's stats carry none of status bits 0 / 1 / 31 (or
`00313F60` returns 0) and unit flag bit 1 is clear, `BattleUnit_TeardownAndDespawn(unit, 0)`
(`00300E40`, `00324420`–`0032442A`); then `002E42D0`, `002699D0` and `002ECEC0` on the actor at
unit `+0x10`. Its meaning beyond the call list is not read.

**The second caller, `00239960`** (1,187 B, unnamed; called from `BattleSystem_InitializeAreaState`,
`002342F0`): walks the table at registry slot `02EBF028` (count at `+4`, `00239B70`–`00239BB5`);
for a row whose byte `+0` equals its argument, byte `+1` selects the stats record through
`BattleStats_GetByBattleSlotIndex` (`00320A40`, `00239BC9`–`00239BD7`), **`0030C470(page, row.b_02, 0)`**
(`00239BE3`–`00239BED`) and **`00323790(page, row.w_20)`** (`00239C40`–`00239C44`) — a second
authored table that carries a starting level and a starting LP grant. What else that row holds is
not read here.

### 2.7 The name reference — `002B58B0` and the two-level text table at `02EBF170`

Both paths end their row work the same way (`0023A88A`–`0023A8E1` enemy, `0023AB03`–`0023AB57`
party): a 16-bit word from the row — enemy `+0x08`, party `+0x30` — is split **5 : 11**.
`word >> 11` indexes the dword table at `02EBF170` (entries from `+4`), the dword is resolved
through `ImageAddress_ResolveRuntimePointer` (`0020E600`) to a **bank**; `word & 0x7FF` indexes
that bank's dwords (from `+4`) and resolves again to a **text block**; then `002B58B0(block, 0)`.

`002B58B0` (62 B; 91 call sites in 59 functions, three more by jump thunk — almost all of them in
the `0027xxxx`–`0057xxxx` UI and presentation range) is a **packed-string-list indexer**: null → 0;
if the block's first two bytes are both zero, it skips *n* NUL-terminated strings from `block + 2`
and returns the *n*-th (`002B58C3`–`002B58E9`); otherwise it returns the block itself
(`002B58EA`). With *n* = 0 the installer stores **the first string of the block at unit `+0x18`**.
That the return is a C string has a positive control: `00309E70` (79 B) returns either
`002B58B0(entry, 0)` or the empty string at `01CEB638` when its lookup fails (`00309E9C`,
`00309EB2`). So the two row words are **text references**, and `02EBF170` is a table of at most 32
banks of up to 2,048 text blocks. Which reader consumes unit `+0x18` — and therefore whether it is
the unit's display name — is `FB-6`.

### 2.8 What the row does not carry — the foe's statuses and augments come from its script

Nothing in the enemy row or the installer writes the two masks the recompute reads for a foe
(`unit + 0xE80`, the innate augment source; `unit + 0xE90`, ~~the permanent statuses~~ the scripted status immunities — corrected 2026-09-15). A displacement
sweep finds their only battle-unit writers in the tails of two script verbs — **`btlAtelSetAbility`**
(`0x3000` → `002390B0`) and **`btlAtelSetStatus`** (`0x3002` → `002394C0`) — read in
[the auto-status rebuild](../../08-Combat-Formula/the-auto-status-rebuild.md), "The foe's two masks are
written by script verbs". The status verb also **applies** its code-2 statuses once and its code-1
statuses on a coin flip, but only while the spawn record is fresh (`+0` `& 5 == 0`) — the same
freshness test this installer uses for the steal bits and the spawn counter (§2.2). So a foe's
initial statuses are three-sourced: the row (nothing), the script (`0x3002`), and the recompute
(~~mode 5 re-adds every code-3 bit on every rebuild~~ — corrected 2026-09-15: mode 5 installs every code-3 bit
as an **immunity** in `+0x38` on every rebuild, so code 3 is not a status the foe carries;
[the auto-status rebuild](../../08-Combat-Formula/the-auto-status-rebuild.md)).

**The spawn counter, corrected.** The byte at `0208D454` is not an area id: it is a **bank selector**,
0 or 1. `SpawnKeep_RotatePersistenceBanksForAreaTransition` (`00233780`, one caller,
`BattleSystem_InitializeAreaState` `002342F0`) flips it on an area transition (`00233933`, or
`002339B5`–`002339C6`) and, on the second path, **fills the newly selected bank's 64 words with 1**
(`002339CC`–`002339E2`: `rep stosw` from `0208D354 + bank × 0x80`); `BattleSystem_ResetRuntimeState`
(`00237DF0`) zeroes the selector (`00237E6B`). So `0208D354` holds **two banks of 64 `u16` counters**
(`0x100` bytes; the next global, the selector itself, sits at `+0x100`), each counter starting at 1
per area visit and incremented per fresh spawn of a row with that byte `+2`; the previous area's bank
survives one transition. No other function references the table (absolute-address scan over
`0208D354`–`0208D453`, control `02089340` with 126 references), so **the only readers are this
installer and the rotation** — the reader of the spawn record's `+0x12` copy is still open (`FB-3`).

### 2.9 Extension 2026-09-11 — the three callees read (FB-4)

**`00328FF0(0, row byte +3 & 3, unit byte +0xEA9)` registers the unit in a two-entry tracked-HP
table.** The table is `02EC1380`, two 24-byte entries `{+0 slotIndex, +4 code, +8 HP, +0xC maxHP,
+0x10 MP, +0x14 stats +0x28}`; the call writes entry 0's `+0` (the unit's own slot index, `+0xEA9`)
and `+4` (the row's `+3 & 3`) only when **code is nonzero OR slot index is negative**,
with a signed `row < 2` guard (`00328FFE`–`00329011`). The installer's slot is a
zero-extended byte, so code zero does not write. SECTION-01 verifies the real table
address `02EC1380`; EXP-150's `02E81380` observation is a wrong-address capture. `BattleSystem_InitializeAreaState` resets both
entries to code −1 (`003221B0`). The one reader, `0031B690` (← `004050C0`, `00405100`, `00406A60`),
walks the two entries, and for each whose code is non-zero resolves the unit by slot
(`BattleUnit_GetBySlotIndex`) and copies its current HP, max HP and the two words `+0x4C` / `+0x28`
of its stats record into the entry (`0031B6C0`–`0031B720`), returning how many it refreshed and the
table's address. **The enemy row's `+3 & 3` is therefore a "track this unit's HP" code** — the
shape of a boss gauge, read by presentation code in the `00405…` range that this page does not
name.

**`00237040(unit)` decides, at apply time, whether the unit is engaged.**
`BattleUnit_ShouldEnterEngagedActionState(unit, 1)` (`00308010`): a party record (kind 0) goes to
`BattleUnit_ComputePartyBattleStance` (`00308130`); an enemy goes to
`BattleUnit_HasNonPartyEngagementEvidence` (`00308040`): the spawn record's byte 0 bit 5 → no
(`00308075`); bits 3 or 6 set → **no, when called from the apply** (`00308083`; on later calls, the
record's float `+4` must be below a constant and
`BattleUnit_HasRelationshipClass2PlusInTrackedActorList` must hold with the distance test
`Spawn_ValidateCandidateDistanceToPlayers(unit + 0xE0, (+4)²)` failing, `0030808B`–`003080EB`);
otherwise unit flag bit 40 → yes, else `HasRelationshipClass2PlusInTrackedActorList` — any
actor in the unit's tracked list (`+0xBC4` count, `+0xBC8` entries) whose relationship class is ≥ 2
(`0030B056`–`0030B0A0`). Then `BattleUnit_SetupEngagedActionState(unit, 1)` (`002FED60`) sets
flag **bit 23**, zeroes `+0xDCC` (the stance-recheck deadline) and sets `+0x6E8` to the static
gambit set A of the record's kind (`01EEC3C0` party, `01EEC410` enemy — the same two blocks the
stance enter / exit functions use), then notifies the actor's render-side record through
`002ECF10(unit + 0x10, 1, 0)`; or `002FEDC0(unit, 1)` clears bit 23 and `+4` bits 9, 10 and 16,
writes the same `+0x6E8`, and notifies with 0. The same pair is what
`BattleUnit_ActivateAppliedDefinitionRuntime` and `SpawnUnit_FinalizeSpawnEntryActivation` call
later, so **bit 23 is the engaged flag and this is its first write**.

**`002FEAB0(unit)` zeroes `+0xEAC` / `+0xEB0`** — the HP-stage pulse phase and the stage reached
([the unit map](../Battle-Unit/the-battle-unit-field-map.md) `+0xEAC`): the pulse restarts at
every definition apply.

**Flag bit 26**, the enemy path's gate, is the spawn side's "placement chosen" mark: the unit
access census finds it set by `SpawnEntry_SetCurrentCandidateState` (`0023946D`, once the
candidate's spawn record resolves), `Spawn_SelectPreviousMapEntry` (`0023557E`), `00238FA0`
(`00238FAE`, a unit by handle) and `00311F70` (`003120A0`, after the position is written into the
spawn record), and cleared by `BattleUnit_ActivateAppliedDefinitionRuntime` (`00233AFB`),
`SpawnUnit_SetLaneCandidateTable`, `BattleStats_RemoveStatusesFromMaskAndRecompute` and
`BattleGroup_RefreshFourActorDefinitions`; no reader other than this installer's gate. **Bit 43**
(set from the row's `+3 & 3` — the tracked-HP code — or `+0x15 & 4`) has **no accessor with an
immediate anywhere in `.text`**: a whole-image decode of every function (2026-09-11) finds no
`test` / `and` / `or` / `bt` of byte `+5` bit 3 or dword `+4` bit 11 on any base register, where
the same scan does find bit 40 (byte `+5` bit 0) and the dword's other bits — so the installer's
register-path write is the only known access and the bit is, as far as the image shows, unread.
## 3. Key addresses

| address | size | what |
|---|---:|---|
| `0023A570` | 1,808 B | `BattleUnit_ApplyUnitDefinition(unit, id)` |
| `0023AC80` | 717 B | `BattleStats_InitializeDefinitionRecord(page, id)` |
| `00236A60` | 452 B | `BattleUnit_ResetStateForReuse` |
| `00236100` | 56 B | `SpawnKeep_ResolvePrimaryEntry(map, lane)` → the spawn record |
| `00322C50` | 1,025 B | `BattleEncodedId_IsValidForClass` |
| `0031A630` | 209 B | `BattleStats_SetEquipmentSlotDirect` |
| `00323910` | 665 B | `BattleStats_SetLicenseNodeStateAndApplySideEffects` |
| `00327CB0`, `00326030`, `00327DE0` | 298 / 224 / 401 B | the three gambit initialisers |
| `0030C470` | 432 B | the level grower (section 2.6); six call sites |
| `0030C650` | 570 B | `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` — grown from level 0 with the silence flag |
| `002F8F20` | 122 B | the experience curve (section 4); four call sites in three functions, `00312280` among them |
| `00324100` | 198 B | `BattleStats_ComputeLicenseDerivedRank` — one caller |
| `0030F690` | 196 B | `BattleStats_RemoveStatusesFromMaskAndRecompute` — three call sites |
| `00237CA0` | 186 B | builds the two status masks at `0208D320` / `0208D324`; reached by jump thunk from `00236A40` |
| `0030F340`, `0030F5A0` | 172 / 233 B | the HP and MP reconcilers — three call sites each (`0030C470`, `0030F3F0`, `0030F4D0`) |
| `003243F0` | 95 B | the party-revive hook in the HP reconcile; two callers |
| `00323790` | 43 B | the LP setter, `[0, 99,999]`; two call sites |
| `002B58B0` | 62 B | the packed-string-list indexer; 91 call sites |
| `00309E70` | 79 B | the positive control for `002B58B0`'s string return |
| `00239960` | 1,187 B | the area-state party walk over `02EBF028` |
| `00233780` | 672 B | `SpawnKeep_RotatePersistenceBanksForAreaTransition` — flips the counter bank and fills it with 1 |
| `002390B0`, `002394C0` | 190 / 222 B | the tails of `btlAtelSetAbility` / `btlAtelSetStatus` (`00510440` / `005103B0`) — the foe's masks (section 2.8) |
| `00254A40` | 6 B | `SpawnHistory_GetCounterWrapThreshold` |
| `0020E600` | 10 B | `ImageAddress_ResolveRuntimePointer` — every registry row goes through it |
| `00328FF0` | | the tracked-HP registration (§2.9) |
| `00237040` | | the engaged-state decision at apply (§2.9) |
| `002FEAB0` | | the HP-stage pulse reset (§2.9) |
| `02EC1380` | | the two-entry tracked-HP table; reader `0031B690`, reset `003221B0` |
| `00322050`, `00303EC0`, `00304630`, `003105D0`, `00313F60` | | callees named by address |
| `0023A3B0`, `00300E40`, `003266C0` | | the three callers: the script-selected spawn, teardown (`0xFFFF`), the four-actor refresh |
| `00300FC0` | 371 B | reads `+0x698` byte `+5` and `+4` the same way (the party-type shortcut) |

### Data

| address | what |
|---|---|
| `02EBF120` | enemy definition table (ARD slot 2); rows by low byte; words `+0x00`, `+0x22`, `+0x24`, `+0x50`, `+0x08`, `+0x1C`, `+0x32`–`+0x36`; bytes `+2`, `+3`, `+4`, `+5`, `+0x15`, `+0x22`, `+0x23`, `+0x27` read here |
| `02EBF130` | party definition table, 456-byte rows; words `+0x0A`–`+0x12`, `+0x14`, `+0x16`, `+0x1A`, `+0x30`, `+0x44`; bytes `+0x1E`, `+0x21`, `+0x24`, `+0x27`, `+0x2B`, `+0x2C`, `+0x2E`, `+0x46`, `+0x47` read here |
| `02EBF140`, `02EBF148`, `02EBF150`, `02EBF168` | the sibling tables the enemy row cross-references |
| `02EBF170` | the text bank table: ≤ 32 banks (dwords from `+4`) of ≤ 2,048 text blocks, addressed by a row word split 5 : 11 (section 2.7) |
| `02EBF028` | the area-state party table `00239960` walks: byte `+0` class, `+1` battle slot, `+2` starting level, word `+0x20` starting LP |
| `0208D320`, `0208D324` | the two status masks: statuses whose `status_data` word `+6` has bit `0x2000`, and the rest; written only by `00237CA0` |
| `009153EC` | `0.4f` (`0x3ECCCCCD`), the cubic coefficient of the experience curve |
| `02EBF038` | the licence table; entry byte `+7` = per-character initial-ownership bits |
| `02EBF190` | the battle-state block; `+8` begins 40 × `0x1C8` stats records — **a pointer into the save image** (added 2026-09-10): `SaveRuntime_RebindImageBackedGameplayState` (`00238A80`, `00238A89`–`00238A92`) sets it to `SaveImage_GetActiveRuntimeBuffer() + 0x4E68C`, payload `+0x4E48C`, so a party character's stats record is saved in place ([the save-payload field map](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) §2.2) |
| `02089340 + 0x4014` = `0208D354` | the spawn-history counters: two banks of 64 `u16`, selected by the byte at `0208D454` (rotated by `00233780`, zeroed by `00237DF0`) — section 2.8 |
| `02089378` | per-character `0x170` blocks (party `+0x6E0`) |
| `01CEBC78`, `00902438`, `00901B3C` | `2π`, `360.0`, `1.5` |

## 4. Data structures and formulas

**The definition id**: `kind = id >> 8` (0 party, 1 enemy, other = none), `row = id & 0xFF`; written
whole to stats record `+4`, so `stats->b_05 == kind`.

**The stats record** (`BattleStatsRecord`, `0x1C8`): enemy copy at `spawnRecord + 0x80`; party copy at
`*(02EBF190) + 8 + row × 0x1C8`. `+4` u16 id; `+0x50` qword `-1`; `+0x58`, `+0x1C3` `0xFFFF`;
`+0x1C5` `0xFF` at init; then equipment, licences, level, gambits by the initialiser; `+0x38`,
`+0x3C`, `+0x64` status words, `+0x48` HP, `+0x24` max HP, `+0xBC[32]`, `+0x13C[32]` per the status
and HP pages.

**The steal bits**: `spawnRecord->b_14 = (row.w_32 != 0xFFFF) | (row.w_34 != 0xFFFF) << 1 | (row.w_36 != 0xFFFF) << 2`.

**The spawn counter**: `k = (bank << 6) + row.b_02` with `bank = byte 0208D454 ∈ {0, 1}`; `c = counters[k]`; `if (c < threshold) counters[k] = c + 1`; `spawnRecord->b_12 = (u8)c`; every counter of a bank is set to 1 when the bank is selected for a new area.

**The experience curve** (`002F8F20(n)`, called with `n = level − 1`; four call sites, the award
path `00312280` among them, so this is the death page's `ExpForLevel`): `n < 1 → 0`; `n > 98 → −1`
(the caller's unsigned clamp turns that into 99,999,999); otherwise

```
exp(level) = Σ_{k=2}^{level} trunc( float32(k³) × 0.4f + float32(12k²) )     ; 002F8F50–002F8F90
```

— the ~~`k × (22 + 12(k − 2))`~~ **`k × (24 + 12(k − 2)) = 12k²`** term is carried in `edx` (`002F8F46`, `002F8F87`), the cubic in
single precision (`009153EC`). **A reconstruction must use `float` arithmetic and truncation,
not doubles**: ~~level 2 is 47~~ **level 2 is 51**, and every later threshold depends on the float rounding of the cubic.
*Corrected 2026-09-29 (FABLE, Claude Opus 5.5): `lea edx, [rcx + 0x16]` at `002F8F46` runs after `mov ecx, 2`, so the
linear coefficient starts at 24, not 22. The original bytes, executed under unicorn for every input 0..100, give level 2 = 51,
level 10 = 5,814, level 50 = 1,165,318 and level 99 = 13,741,148, and the old reading disagrees at all 98 levels
([`_index/candidates/exp-curve-fable/`](../../_index/candidates/exp-curve-fable/README.md), `curve.py` X B F K; every threshold in `curve.tsv`).*

**The LP setter** (`00323790(page, delta)`): `v = +0x190 + delta; +0x190 = v < 0 ? 0 : min(v, 99,999)`
(`00323790`–`003237BA`; `0x1869F`) — the accumulated-LP cap the death page reports.

**The starting MP**: `+0x4C = (+0x6C ≥ 0 && +0x7C ≥ 0 ? +0x28 : 0) × (kind 0 ? row.b_47 / 100 : 1)`.

**The status masks**: `0208D320 = Σ bit s where status_data[s].w_06 & 0x2000`; `0208D324` = the
complement over the 32 rows.


## 5. Call chain

```
Spawn_ApplyScriptSelectedUnit 0023A3B0        (the script verb path)
BattleGroup_RefreshFourActorDefinitions 003266C0
BattleUnit_TeardownAndDespawn 00300E40        (id 0xFFFF: unapply)
  -> BattleUnit_ApplyUnitDefinition(unit, id)
       -> BattleUnit_ResetStateForReuse
       -> kind 1: 02EBF120 row -> SpawnKeep_ResolvePrimaryEntry -> page = record + 0x80
                  -> BattleStats_InitializeDefinitionRecord(page, id)   [fresh records]
                  -> steal bits, spawn counter, +0xE60/+0xE68/+0x6E0/+0xE70/+0xE78, bit 43
          kind 0: 02EBF130 row -> stats = *(02EBF190) + 8 + row*0x1C8 ; +0xE60, +0x6E0, +0x6F0
       -> common: +0x64/+0x68/+0x6C, +0x48 = 0, +0x55/+0x56/+0x52/+0x54, +0x698, +0x6A0, +0x18
       -> 00237040 (ShouldEnterEngaged -> Setup: bit 23, +0xDCC = 0, +0x6E8 = set A | Leave) ; 002FEAB0 (+0xEAC/+0xEB0 = 0) ; terminal test -> clear bit26 / set bit1 ; bit2

BattleSystem_ResetRuntimeState 00237DF0 / 00239960
  -> BattleStats_InitializeDefinitionRecord(state element, id)          [party records]
       -> equipment (5 words) ; licences (02EBF038 byte +7 bit index) ; level ; gambit preset +0x14
       -> 0030C470(page, level, kind)   [the level grower]
            -> +0x1C2 = 0 ; kind 0: base stats from the 02EBF130 row ; 00324100 (licence rank)
            -> 0030C650(page, level, 2)  silent growth
            -> +0x18C = 002F8F20(level-1)  ; 0030F690(page, all statuses) ; 0030F340 ; 0030F5A0
            -> +0x4C = +0x28 x row.b_47 / 100 (kind 0) ; 0030FED0(page, 0)
       -> 00323790(page, row.w_44)      [starting LP]
BattleSystem_InitializeAreaState 002342F0 -> 00239960 -> 02EBF028 rows -> 0030C470 ; 00323790
```

## 6. Modding notes

- **A character's starting equipment is the party row's five words at `+0x0A`–`+0x12`**, its
  starting licences are the licence table's byte `+7` bit for that character, its gambit preset is
  word `+0x14`, its level byte `+0x2E`. Editing the party table changes what a character joins with.
- **An enemy's steal table is its row's three words at `+0x32`, `+0x34`, `+0x36`** (`0xFFFF` = no
  slot); the availability bits are set at spawn and consumed by the applier once each. An enemy has
  **one** equipment slot, from `+0x1C`.
- **The spawn-history counter** is authored by the row's byte `+2` (`0xFF` = not counted) and kept
  per area visit in one of two banks (section 2.8); the pre-increment value is on the spawn record at
  `+0x12`. What reads that copy is `FB-3`.
- **A foe's innate augments and starting statuses are in its AI script**, not in the row: edit the
  `btlAtelSetAbility` / `btlAtelSetStatus` calls in the `.ebp`, remembering the bit reversal and the
  two-bit codes (section 2.8).
- **A character's starting level is the party row's byte `+0x2E`, its starting LP the word `+0x44`,**
  **its starting MP the percentage byte `+0x47`, and its base stats the words `+0x16` / `+0x1A` and
  the bytes `+0x1E`, `+0x21`, `+0x24`, `+0x27`** (each followed by its growth byte). The level is
  always re-grown from zero, so a modded base is grown by the modded growth — there is no stored
  "stats at level N" to edit.
- **The experience curve is code, not data** (`002F8F20`): a mod that wants different thresholds
  must patch the function, and any patch must keep `+0x18C` consistent with the walk the death page
  describes, or a character joins mid-threshold.
- **`+0x48` is zeroed on every apply** (`0023ABDB`, cited 2026-09-11 — OPUS). A mod that raises a
  unit's HP floor must do it after the definition is applied, or it is lost; the only thing that
  raises it is the script verb `btlAtelSetHpLowLimit` (`3061`), which two shipped scripts use with
  a non-zero value ([the field map](../Battle-Unit/the-battle-unit-field-map.md) §10).
- **Re-applying a definition resets the unit first** (`00236A60`) — the same reset that
  teardown uses, since teardown is an apply of `0xFFFF`.

## 7. What is not known

> **`CB-2` answered 2026-09-14 (FABLE): the `jg` is C integer promotion of a 16-bit count, not a signed index.**
> - **What the four joins compare.** In `BattleUnit_ApplyUnitDefinition` all four load the row's index word with
>   `movzx eax, word`, so the index is always 0–65535 (`0023A6B4`, `0023A71E`, `0023A73F`, `0023A760`).
>   - Three counts are `u32` dwords at descriptor `+4` (`0023A6AD`, `0023A738`, `0023A759`). `count − 1` is then an
>     `unsigned int`, the comparison is unsigned, and it compiles to `ja`.
>   - The slot-1 count is a **`u16`** at `[02EBF168]+0` (`0023A717 movzx ecx, word ptr [rax]`). A `u16` promotes to
>     `int`, so `count − 1` is a signed `int` compared with an `int` index, and it compiles to `jg` (`0023A722`–`0023A726`).
> - **What it changes.** For a count of 1 or more the two forms reject exactly the same indices, because both operands are
>   non-negative. They differ only when `count − 1` is −1 (a zero count or an absent table): `jg` rejects every index and
>   `ja` accepts every index. That is the asymmetry the cross-reference row above already records.
> - **So no index is treated as signed.** The signed compare follows from slot 1 being the only join with a 16-bit count,
>   the fifth asymmetry `CB-1` listed. It needs no separate explanation.

- [x] **UQ-97.** **Whether a zero reward count or a missing reward table ever occurs in shipped data** — the
  guards' wrap-around at count 0 (§2.2, corrected 2026-09-12) is a property of the code; the 2,292-row
  reward census is authored data with positive counts, so nothing here says the unchecked path is
  reachable in play. Live reachability is EXP-075's stated limit. (`FB-5`)
  **ANSWERED 2026-09-15 (FABLE) for shipped data — no: the guarded path is never fed.** This is an authored-data census of
  both `.ard` copies, 166 areas each (`work/FABLE/drift4/uq97_reward_counts.py`); nothing was executed.
  - **No table is missing.** Directory slots 2, 5 and 6 are present in every file: the enemy-definition table and the
    two reward-row tables (`02EBF120` / `02EBF148` / `02EBF140`).
  - **Empty reward tables exist in exactly four areas**: `asp_a`, `dor_f`, `mrm_a` and `slm_a`, identically in both copies.
    **In those same four areas the enemy table is empty too** (slot 2 count 0), so no row exists to index them. They are
    also the four areas with no order sets.
  - **Everywhere else every index lands inside its table.** All 2,292 enemy rows' words `+0x22` (into slot 5) and `+0x24`
    (into slot 6) are below their table's count, matching the 2026-09-12 survey above.
  - So the count-0 wrap-around in the guards is a property of the code that the shipped data never exercises. A runtime
    table not loaded from these files would be a different question, and none is known.

- [x] ~~**What `002B58B0` resolves** from the `02EBF170` row selected by the definition's `+8` (enemy)~~
  ~~or `+0x30` (party) word `>> 11`, stored at unit `+0x18`.~~ `FB-1` — ANSWERED 2026-09-10: the first
  string of a text block addressed bank : entry (5 : 11) through `02EBF170` (section 2.7).
- [x] ~~**What the level grower `0030C470(page, level, kind)` writes**, and what `00323790(page,~~
  ~~row +0x44)` is for party rows.~~ `FB-2` — ANSWERED 2026-09-10: section 2.6; `00323790` is the LP
  setter with the `[0, 99,999]` clamp.
- [x] ~~**Who reads the spawn-history counters** at `02089340 + 0x4014` and the spawn record's `+0x12`
  copy.~~ **FB-3 ANSWERED 2026-09-12 (FABLE):** the table has exactly two references (this installer
  and the bank rotation, §2.8); the `+0x12` copy is read once, by
  `BattleUnit_RefreshActorRuntimeFromDefinition` (`00238EA9`, through the unit's `+0x6A0` spawn
  record) and handed with the text pointer to `00269F20(actor, text, n)`, which stores it at the
  actor's `+0x100`. That word has one reader, the instance-number getter `00263A10` (word `+0x100`
  when `+0x102 ≥ 0`), called by `00272C80`, `00272CE0` and the battle event poster `005369C0` —
  so the per-area spawn count becomes the byte [the post-result events page](../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) §2 sees beside the source's name in a
  battle message, next to `Actor_GetDisplayName` (`00263990`, [the NPC name dictionary](../Actor-Names/the-npc-name-dictionary.md)).
- [x] ~~**The three unread installer callees** `00328FF0`, `00237040`, `002FEAB0`~~ read 2026-09-11
  (§2.9: the tracked-HP registration, the engaged-state decision, the HP-stage pulse reset; `00322050`
  the re-key wrapper). Bit 26 is the spawn side's placement-chosen mark (§2.9); bit 43 has no immediate accessor anywhere in the image (§2.9). `FB-4` — closed to that negative.
- [x] ~~**The row fields read but not named**~~ **ANSWERED 2026-09-12 (FABLE) — the two notes below:** enemy `+0x00`, `+0x22`, `+0x24`, `+0x50` (the four
  sibling-table selectors), `+0x03`, `+0x15`, `+0x22`, `+0x23`, `+0x27`; party `+0x2B`, `+0x2C`,
  `+0x30`, `+0x44`. `FB-5`. *Narrowed 2026-09-11:* enemy `+3 & 3` is the tracked-HP code (§2.9);
  enemy `+0x27` and party `+0x2B` are the same integer — the perception range the unit map names at
  `+0x68` (13 for every human row, 30 for the Chocobo, 20 for every Esper in the party table); enemy
  `+0x22` is the facing in degrees (`× 2π / 360` into `+0x64`); party `+0x30` is the name reference
  (§2.7).
  **Surveyed 2026-09-12 (FABLE) over every shipped area file — 332 `.ard`, 2,292 enemy rows of
  ard slot 2 ([the ARD loader](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)):** the three selectors are indices, and every shipped value is in
  bounds — `+0x00` into ard slot 0 (`02EBF150`, the area's unit-definition site; 15 distinct values,
  2,292 / 2,292 in range), `+0x22` into slot 5 (`02EBF148`; 0–21, 2,292 / 2,292), `+0x24` into slot 6
  (`02EBF140`; 0–8, 2,292 / 2,292), `+0x50` into the gambit order-set directory (`02EBF168`; 0–23).
  Row `+0x15` is a **flags byte**: bit 0 set on 2,240 rows, bit 4 on 616, bit 1 on 252, bit 2 on 52,
  bit 3 on 32, nothing above bit 4. **Row `+0x23`, `+4` and `+5` are 0 in all 2,292 rows** and `+0x27`
  is 0 or `0xFF` (66 / 2,226) — so the type, kind, facing and perception the installer uses come
  from the *page*, not the row, and the row's copies are unexercised in the shipped data. `+2`
  (the spawn-counter lane) is 0–11 or `0xFF` (938 rows). The name word `+8` is bank 8 on every row.
  **Slots 5 and 6 are the reward rows** — [the battle-unit field map](../Battle-Unit/the-battle-unit-field-map.md) §7 already names the unit's copies
  `rewardBaseRow` (`+0xE70`, slot 5 via `+0x22`) and `rewardPerLevelRow` (`+0xE78`, slot 6 via
  `+0x24`), and the four readers take the same offsets from both, each as
  `base + perLevel × (the *dying foe's* level +0x1C2 − its stats +0x88)` — both operands from the corpse's stats record `[r14 + 0x698]` (`002F8C5C`–`002F8C71`; corrected 2026-09-12 on OPUS's counter-evidence, the recipient is not read there): **word `+0`** into game counter `0x11`
  (`00317090` → `00253770(0x11, n)`), **byte `+0x2F` the licence points** (`Reward_ComputeLicensePointsForRecipient`,
  `002F912B`–`002F9144`, doubled by effect id 12 in either layer), **dword `+0x30` the gil**
  (`BattleUnit_ProcessDefeatRewardsAndLoot`, `00312534`–`0031254C`), **dword `+0x34` the experience**
  (`Reward_ComputeExperienceForRecipient`, `002F8C73`–`002F8C85`). Over the 2,238 base rows: EXP
  0–27,404, LP 0–255 (1 on 1,024 rows), gil 0–297, the counter 0–65,000; over the 1,238 per-level
  rows: EXP 0–666, gil 0–10, the counter 0–520, and **LP 0 on every row** — licence points never
  scale with level. So `+0x22` chooses an enemy's reward line and `+0x24` its per-level growth,
  and stats `+0x88` on an enemy is the level those lines are quoted at.
- [x] ~~**Who reads unit `+0x18`** (the text pointer), stats `+0x20` (the licence-derived rank byte)
  and stats `+0x88` (the kind byte the grower stores on the enemy branch); and what `003243F0`'s
  four callees and `003105D0` / `00313F60` do.~~ **FB-6 closed 2026-09-12 (FABLE):** unit `+0x18`
  was answered 2026-09-10; stats `+0x20` has one reader, the stat rebuild
  (`BattleStats_RebuildEffectiveStatsAndAffinityState`, `002FF0AA`, into its `[rsp+0x60]` input);
  stats `+0x88` is the union [the battle-stats map](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) decodes (the party gambit block, or the enemy branch's
  byte). `003243F0` (95 B) is the **unit retire helper**: `BattleUnit_CancelAndResetCurrentAction`
  (`003105D0`), then `BattleUnit_TeardownAndDespawn(unit, 0)` unless the unit is down (a terminal
  status without the `FieldData_GetActiveFieldRecordBit15` waiver, `00313F60`) or already torn
  down (flag bit 1), then on the actor work: `002E42D0` (the render record's `00427280`, and actor
  `+0xEC = 0`), `002699D0` (`002ECA00(actor, 1)`, `002E8060`, and the actor-event reset `002EB430`
  on the record or its `003587C0` owner, [the actor storage map](../Actor-Storage-Record/the-actor-storage-record-field-map.md)) and `002ECEC0` (the render record's
  `+0x550` to `003AEEF0`). `00427280` and `003AEEF0` are unread.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The class split and the third case | `0023A580`–`0023A594`, `0023A626`–`0023A63C`; `00300F6D` | 1 | PROVEN |
| The enemy path's row, cross-references, spawn record and page | `0023A64A`–`0023A795` | 1 | PROVEN |
| The steal bits from `+0x32`/`+0x34`/`+0x36` | `0023A7B2`–`0023A7E4` | 1 | PROVEN |
| The spawn counter and its wrap | `0023A7E7`–`0023A840` | 1 | PROVEN |
| `+0xE60`, `+0xE68`, `+0x6E0`, `+0xE70`, `+0xE78`, bit 43 | `0023A915`–`0023AA44` | 1 | PROVEN |
| The party path's row, state element, null `+0x6A0` | `0023AA49`–`0023ABC3` | 1 | PROVEN |
| The common stores incl. `+0x48 = 0`, `+0x698`, `+0x6A0` | `0023ABCA`–`0023AC58` | 1 | PROVEN |
| The stats record is `0x1C8` and carries the id at `+4` | `0023ACA4`–`0023ACBD`, `0023AD8E` | 1 | PROVEN |
| Equipment, licences, level, gambits at init | `0023AD7B`–`0023AF28` | 1 | PROVEN |
| Writers of `+0x698`/`+0x6A0`/`+0xE68` on the unit | from-entry displacement sweep, control `00306E60` read; the two battle-unit writers `00236A60`, `0023A570` | 1 | PROVEN |
| Three callers each for `0023A570` and `0023AC80`; one for `00236100` | `check_caller_claims --addr`, control 632 | 1 | PROVEN |
| The level grower: reset, base stats, silent growth, experience, status strip, reconcile, starting MP, recompute | `0030C488`–`0030C602`; callees `0030F690`, `0030F340`, `0030F5A0`, `00324100`, `00237CA0` read to their rets | 1 | PROVEN |
| The experience curve and its float coefficient | `002F8F20`–`002F8F99`; `009153EC` = `0x3ECCCCCD` | 1 | PROVEN |
| `00323790` clamps `+0x190` to `[0, 99,999]` | `00323790`–`003237BA` | 1 | PROVEN |
| `002B58B0` is a packed-string-list indexer and its return is a string | `002B58B0`–`002B58ED`; control `00309E70` with the empty string at `01CEB638` | 1 | PROVEN |
| Call-site counts for the ten functions of section 2.6–2.7 | `check_caller_claims --addr`, control 632 | 1 | PROVEN |
| The counter table's two banks, its rotation and fill, and its only two referencing functions | `00233933`, `002339B5`–`002339E2`, `00237E6B`; `data_xref_scan --range 0x0208D354 0x02091354`, control `02089340` (126 refs) | 1 | PROVEN |
| The foe's masks are script-written, not row-written | displacement sweep `+0xE80`/`+0xE90` (control `003103E0`); `002390B0`, `002394C0` | 1 | PROVEN |
| The per-kind bindings hold in a running game | **EXP-081 (ASTRA), re-derived by FABLE from the raw ReadProcessMemory spans, not the normaliser:** two samples of one loaded field, four units, the pool stride `0xF50` and the three `st2e` table headers read raw. Kind 0 (slot 0): `+0x698 = *(02EBF190) + 8`, `+0x6A0 = 0`, `+0xE60` = party row 0, `+0xE68 = 0`. Kind 1 (slots 4 / 5 / 7): `+0x698 = +0x6A0 + 0x80` exactly, primary keep entries 0 / 1 / 3 at stride `0x250`, the 456 stats bytes identical to that keep slice; `+0xE60` = enemy rows 6 / 5 / 0 (the definition ids' low bytes); `+0xE68` = class rows **4 / 3 / 0 — each enemy row's u16 `+0`, not its own index**, which is the observation that separates this reading from any mapping of `+0xE68` to the spawn record; every class pointer lies outside both keep banks ([EXP-081](../../_experiments/EXP-081-live-battleunit-bindings.md)) | C | OBSERVED (one field, four units) |
| What the remaining unread callees and unnamed row fields are | **not established** | — | UNKNOWN |

## 9. Related

- [`../Battle-Record-Kind/battle-record-kind-byte.md`](../Battle-Record-Kind/battle-record-kind-byte.md)
  — the kind byte, now identified as the id's class byte.
- [`../battleunit-slot-pool-and-actor-class.md`](../battleunit-slot-pool-and-actor-class.md) — the
  bind that precedes this and writes the lane byte `+0x57`.
- [`../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md`](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)
  — the enemy table and its four sibling slots.
- [`../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
  — the registry and the party table's shape.
- [`../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)
  — the spawn record this fills.
- [`../../07-Combat-Action/applying-a-result-to-a-target.md`](../../07-Combat-Action/applying-a-result-to-a-target.md)
  — the steal slots' consumer.
- [`../../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md`](../../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md)
  — the growth the level grower drives, and the silence flag it passes.
- [`../../13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md`](../../13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md)
  — the threshold walk over `+0x18C` that the curve in section 4 feeds.
- [`../../10-Status-Periodic-Terminal/where-mp-comes-from.md`](../../10-Status-Periodic-Terminal/where-mp-comes-from.md)
  — `+0x4C` and `+0x28`, the fields the starting-MP step writes.
- [`../../08-Combat-Formula/the-auto-status-rebuild.md`](../../08-Combat-Formula/the-auto-status-rebuild.md)
  — the recompute every path here ends in, and the `+0x194` licence bitmap.
- [`../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md`](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)
  and [`../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md`](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md)
  — what the stats record is used for.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Five claims recomputed from the bytes. **All five exact.**

| claim | measured |
|---|---|
| the experience curve's coefficient, `009153EC` = `0x3ECCCCCD` | bytes `CD CC CC 3E` — `0x3ECCCCCD`, which is **0.4f** |
| `00323790` clamps `+0x190` to **`[0, 99,999]`** | `add r8d, edx` / `jns` → store **`0`** on negative; else `mov eax, 0x1869F` (**99,999**) / `cmp` / `cmovg` — **both bounds, and the clamp is the `cmovg`** |
| the stats record is **`0x1C8`** | `0023ACA4 mov r8d, 0x1c8` feeding `call 00861EC0` |
| three callers each for `0023A570` and `0023AC80` | **3 and 3**, each in 3 distinct functions |
| one caller for `00236100` | **1** |

### The control reproduces for the third time

§ cites `check_caller_claims --addr` with **control 632**. An independently built counter — decoded
`call` instructions with an immediate target, over 38,161 function bodies — gives `memcpy`
**632 call sites in 359 functions**.

> **That is the same 632 this sweep measured while auditing `CONTRACT-battle-target-buffer`**, where
> it is also the stated control. Two documents, two purposes, one number, reproduced twice from the
> image. A control that holds across unrelated documents is worth more than a control that holds once
> — it is evidence about the *instrument*, not just about the claim it guards.

The clamp is worth one further note: the negative branch stores **literal zero**, not the clamped sum,
so a negative running total is *reset* rather than floored at its own value. The claim says `[0,
99,999]` and that is exactly what the two paths implement.

**Not claimed:** nothing here was executed or observed live; the `+0xE70`/`+0xE78` rows this page
lists are the reward-row pointers examined separately in the battle-unit field map's pass.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `002376F0` | 1445 | definition-field batch init on `[rcx+0x1E]`: `0020E600` x20 — repeated field-set calls over the unit-definition record |

### The `002342F0` exclusive subtree — all 12 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the area-transition initializer **12 frontier functions**.
Every member body was disassembled from the shipping image within its declared extent
(2026-09-14). `002342F0` is a single gate plus a reset battery: it returns early unless the
battle flag `02089300` is set (`002342F4`), bumps the seed counter `0208E6B0` and stores it into
the shared gameplay LCG (`00328D80`), masks the battle state word `02089340`
(`& 0xFFFFC01E | 0x10`, `00234343`) and stores `0x1C` at `0208D458`, then walks the 40-record
`0x1C8`-stride unit array at `02EBF190` clearing status mode 0 per record
(`BattleStats_RemoveStatusMode0`, `0023437E`). It fetches world bounds via
`Navigation_GetWorldBoundsXZ` (`00383740`), computes the map area `w*h` and picks a density
scale from the `.rdata` thresholds at `009146E8`–`009146FC` ~~before handing it to `003924B0`~~
~~(`0023441E`)~~ — 8.0 up to an area of 20000, 12.0 up to 30000, else 16.0 — and passes it in `xmm0` to `003924B0`
(`0023441E`), the grid rebuild below. **The builder never reads it** *(2026-09-27, FABLE, Claude Opus 5.5)*: its
first `xmm0` access is a write (`00392575`), after the getter call (`003924E4`) has already clobbered the register,
and `0023441E` is its only caller, with no address-taken reference. So in this build the tiers change nothing, and
the cell budget is a constant ([record](../../_index/candidates/navgrid-unit-definition/README.md)). The tail is a chain of subsystem resets
(`SpawnKeep_RotatePersistenceBanksForAreaTransition`, `SpawnGroup_ResetLifecycleLedger`,
`Loot_InitializeWorldPickupPool`, a `FieldData_GetActiveFieldRecordBit15`-gated `003183A0`)
followed by the six member resets in the table, ending with `002FA520`'s field-id snapshot.

| cluster | members | role | interior |
|---|---|---|---|
| initializer | `002342F0` (390 B) | the battery itself — gate, LCG seed, state-word mask, 40-record status clear, bounds query + grid rebuild, reset chain | `00234360` (`mov rcx,[02EBF190]` — unit-array loop head) |
| LCG seed | `00328D80` (7 B) | `RNG_SharedGameplayLCG_SetState` — stores `ecx` as the state dword at `022C256C` | `00328D80` (the store — 7-byte leaf) |
| field snapshot | `002FA520` (20 B) | tail store — `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) → `022BE940` | `002FA529` (`mov [022BE940], eax`) |
| flag pool | `0030E010` (67 B) | `BattleActionSnapshot_ResetPool` — an eight-step `btr` chain clears bits 0–7 of flag byte `022BEFB0` | `0030E02C` (`btr ecx,3`) |
| block wipes | `0030C3F0` (20 B), `0031A8F0` (11 B), `00322190` (31 B) | `memset(022C1DB0, 0, 0x180)` tail-jump; zero `022C314C`; zero `0208D334`–`0208D34C` | `0030C3F2` (`lea` of `022C1DB0`) / `0031A8F0` (the store — 11-byte leaf) / `00322199` |
| state-struct resets | `003221B0` (77 B), `00327360` (77 B) | `02EC1380`–`02EC13A8`: head/tail pointers + two `-1` id dwords; `022C25A0`–`022C2644`: bit-0 clear plus four `0x30`-stride slots (`0xFF`/`0xFFFF` sentinels + zeroed dwords) | `003221D6` (`mov dword [02EC1398], -1`) / `00327381` (`mov byte [022C25A4], 0xFF`) |
| slot-array reset | `0033A380` (68 B), `004696A0` (284 B) | `0033A380` zeroes six qwords at `022C7CE0`–`022C7D08` and the dword at `022C7D10`, calling `004696A0`, which resets six `0x28`-stride slots at `02EBB560`–`02EBB688` (`0xFFFF` sentinels, zeroed qwords) plus tail dword `02EBB54C` | `0033A3B0` (`call 004696A0`) / `004696F8` (`mov word [02EBB5C0], 0xFFFF`) |
| grid rebuild | `003924B0` (607 B), `00384580` (104 B) | `003924B0` sets `02AEE0B8=0x24` (n) — before the getter, so a zero bounds return skips everything but that store — ~~divides `0x2800/(n+1)` for the cell budget, `sqrtf`s `w*h/budget` into a cell size,~~ *(corrected 2026-09-27, FABLE, Claude Opus 5.5, on ASTRA-RETURN-FABLE-NAV-GRID-QUANTIZATION; bytes re-read)* takes the budget `(0x2800 − n)/(n+1)` = 275 cells, a first size `c0 = sqrtf(w*h/275)`, refines it to `max(w/trunc(w/c0), h/trunc(h/c0))` and stores `floorf` of that `+ 1.0` as `NavGridParams.cellSize`; *(qualified 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-RETURN-FABLE-NAV-GRID-INITIAL-TRUNCATION: `trunc(w/c0)` (`003925A9`) or `trunc(h/c0)` (`003925CE`) is 0 when that side is shorter than `c0`, and the divide at `003925E9` / `003925FC` then gives +infinity under masked exceptions, so `maxss` and `floorf` receive +infinity. ASTRA's thin case, 1 × 400 with `c0` = 3F9A5FB2, gives nx 0, ny 331 and +infinity (the original prefix run under an emulator with a supplied `sqrtf` value; re-derived in `_index/candidates/navgrid-thin-rectangle-consumer/`). Positive extents alone therefore do not guarantee a finite cell size; whether any loaded map has such a shape is not shown.)* the origins and maxima are the getter's rectangle; it derives `cols*rows` as `trunc((w + cell − 1)/cell)` by `trunc((h + cell − 1)/cell)` (`02AEE060`/`02AEE064`), allocates ~~`ebx` bytes~~ `cols*rows*(n+1) + n` bytes via `00384580` and memsets it — base/extent at `02AEE0A0`/`02AEE0A8`/`02AEE0B0`. `00384580` is its synchronized alloc+init: `0036C1D0`/`0036C1A0` enter, `0036A190` allocates, `0036C660` initializes, `0036C110`/`0036C140` leave | `00392590` (`movss [02AEE070], xmm6` — store min_x) / `003845C6` (`call 0036C660`) |

The bounds query and grid math are why a *battle-unit* page owns this family: the transition
rebuilds the spatial index the units are indexed by, and `02EBF190` — the array the loop scrubs —
is the same registry row the authored-table census attributes 170 consumers to.

**One authored case, worked as arithmetic** *(2026-09-27, FABLE, Claude Opus 5.5, from ASTRA's two returns)*. The
formula is ASTRA's ([`nav-grid-quantization`](../../_experiments/evidence/nav-grid-quantization/README.md)). One
authored header gives it a real input ([`authored-grid-shape`](../../_experiments/evidence/authored-grid-shape/README.md)):
an extracted `alc0102.mpk`, identified by its SHA-256, whose slot-4 header describes a 50 × 50 rectangle. Put through the
row above, that is cell 4, a 13 × 13 grid, and an allocation argument of 6,289 bytes. Without the `floorf` it would be
cell 4.125, 12 × 12 and 5,364 bytes, so the case tells the two formulas apart.
- **This is arithmetic over an authored header, not an execution.** Nothing ran the builder, the imported `sqrtf` /
  `floorf` or the allocator on it.
- **Not shown:** that the game loads this copy, and how common the shape is in other areas.
- **The regression is [`navgrid_unitdef.py`](../../_index/candidates/navgrid-unit-definition/navgrid_unitdef.py).** It checks the
  budget, the floor-plus-one and the unread scale against the image, with a planted `xmm0`-read control.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — CLIENT (41 edges through 30 of this page's functions).** The Gameplay layer reaches this page at `00377C20`, `00300530`, `00308010`, `00308040` and 26 more. `FUN_00234150` is the worked example, read in full - it is a 104-byte registration helper that takes the `.text` address `002FED60` as a callback and gates on `byte[+0] & 0x10` of what `0031B810` returns; **11 of the 20 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — SERVICE.** `00312280` on this page calls `FUN_00316a50`, owned by that layer. What it reaches is a 411-byte achievement routine bounded at **`0x1E` ids**; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 43 edges).** A unit being built gets a
locomotion state: `002342F0` calls `Navigation_GetWorldBoundsXZ`, `0033A380`, `0031BD60`,
`00327360`, `00322220` and `003924B0`; `00236A60` calls `Navigation_ResetPathPredecessors`/`003839C0`;
`00311F70` calls `Actor_SetDesiredMovementHeading`, `Actor_SetFacingHeading_Variant1`, `0026B0C0`,
`00336E40` (interior read 2026-09-17, SWE2-FRONTIER — a locomotion-state commit body:
`002646C0` at [`00336ED3`](../../_index/ADDRESS-INDEX.md), then `00265090` ×3 / `004687F0` ×2 /
`0032A790` ×2 / `00265200` ×2), `00392170`; `003105D0` calls `BattleLocomotion_ResetPathAndSetTargets`/`0033C9B0`; and
`00300FC0` calls `Actor_SetMovementSpeed`. The inbound half is the usual shared-accessor fan-in
(`00313F60`, `00377C20`, `003589B0`, `003587C0`, `00322C50` callers) — the build path writes the
unit's first movement state, the crossing is real.

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 25 edges).** 19 edges are
`ImageAddress_ResolveRuntimePointer` fixups inside the page's bodies; the rest is
`GameClock_GetRawTickCounter` (the build timestamps the unit) plus the `0022B6E0`/`00229ED0`/
`0032A160` frame neighbourhood.

**CombatAction — CLIENT.** `00300280`/`0030EF20` on the combat-action layer call `003008A0`, the body `00300BA0` forwards into.

**CombatFormula — CLIENT.** `003112F0` on the combat-formula layer calls `003008A0`.

**Items — CLIENT and SERVICE.** `00300BA0` is itself an items-layer lane — caller `0023AF50`, callee `003008A0` — and `003008A0` is called across that layer (`0030FAA0`, `00300B80`, `0030B180`, `0030C410`, `0030F9A0`, `0030FBE0`, `00310870`, `002FD530`, `002FD640`, `002FD780`, `002FEEB0`) while calling `00309F30` on it — the unit-build shim is items-graph work the definition page records.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Audio — SERVICE and CLIENT (4 edges).** The level-set `0030C650` calls `003A1180` and `002DF220`. The first resolves the current sound-bank handle to its bank-local slot 7, and the second is the sound play entry. `00261F90` reads the field-id getter `WorldTransition_GetActiveOrPendingFieldId` `003148F0`, and `00362850` reads the focus getter `PartyFocus_GetCurrentPackedActorHandle` `003590D0`; both are Audio bodies that were not read here. The level-set plays the level-up sound, and two audio bodies read the same field id and focus handle that this page cites; nothing audio-side feeds the build.

**CombatAI — CLIENT and SERVICE (40 edges).** Five AI bodies walk the unit array through `BattleUnit_GetBySlotIndex` `00236820` and `BattleUnit_GetSlotCount` `00236850`: `AiOrder_EvaluateTargetSelector` `00301AD0`, `AiOrder_ComputeBoundedSelectorScalar` `00308C20`, `BattleEnmity_PropagateToPerceivingFoes` `003219D0`, `BattleUnit_RebuildPerceptionCandidateCache` `003247F0` and `00324F20`. Ten call the validator `00322C50`: `00301AD0`, the seven enmity bodies and two gambit bodies. Five call the field predicate thunk `00313F60`, among them `BattleEnmity_WriteForCombatantId` `00321850` and `BattleEnmity_WriteAllCombatantIds` `00321D30`. The rest are single edges. `0030F130` reads `ActorRuntime_GetClass3FloatPair` `00265090`, `00301830` reads the stance predicates `00308040` and `00308130`, `00308610` calls the unlink `003105D0`, and `00301AD0` reads the party leader `003272A0`. In the service direction, the initializer `0023AC80` seeds the gambit banks through `00326030`, `00327CB0` and `00327DE0`. The area-state party walk `00239960` reloads the preset through `00327CB0`, and `00300FC0` calls the enmity propagation `003219D0`. A built unit gets its gambit banks from the AI layer's own initializers, and the AI layer's evaluators are readers of the unit-slot accessors, validator and field predicate that this page documents.

**Input and InputGameplay — CLIENT (6 edges).** `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70` calls four page subjects. `00303EC0` tests whether the battle-runtime mode is 2, and `003135E0` returns bit 0 of the battle-state block's `+0x5B04` word. The other two are the bit-15 predicate `00377C20` and its thunk `00313F60`. `00226BE0` (Input) reads the focus getter `003590D0`, and `00313A00` (InputGameplay) reads `00377C20`. The input arbiter consults the battle mode, the battle-state flag and the area's action-permission bit that this page cites, and it writes nothing the build reads.

**Party — CLIENT and SERVICE (67 edges).** The party layer's roster, focus and stance bodies use the unit accessors from both sides. Six party bodies read the focus getter `003590D0`, among them `PartyRoster_GetActorBySlotOrCurrentFocus` `00263770` and `PartyRoster_AssignActorToSlot` `00269C70`. Nine `PartyConfiguration_*` and focus bodies call the validator `00322C50`, and five compose handles through `003589B0`. `PartyConfiguration_ReconcileRosterFromCurrentSelectors` `003261D0` and `PartyConfiguration_SetSelectorsAndReconcileRoster` `003273D0` call the slot accessors `00236820`, `00236850` and `00263E30` and the group refresh `003266C0`. `BattleUnit_EnterPartyCombatStance` `00313400` and `BattleUnit_ExitPartyCombatStance` `00313480` call the render-record resolve `002ECF10`, and `PartyControl_ApplyAnalogLocomotionToActor` `00358CB0` reads the float getter `00265200`. In the service direction, the area-state party walk `00239960` calls `PartyConfiguration_SetDefinitionSelectorForIndex` `00329080`, and `003266C0` calls `PartyRoster_GetActorBySlot` `00263750`, `00326500` and `003272F0`. `00300FC0` calls `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040`, `00304630` wraps `PartyFocus_GetPreferredDefinitionSelector` `003271D0`, and `00304680` reads `PartyRoster_GetActorBySlot` `0031ABF0`. Building and resetting units reads and re-points the party roster and focus through the party layer's own bodies, and those bodies are the main other users of the slot accessors, focus getter and validator.

**Presentation — CLIENT, SERVICE and MECHANICAL (61 edges).** Twelve render bodies read the focus getter `003590D0`, among them `RenderSystem_UpdateCharacterRecords` `00426090`, `CharacterRenderSystem_UpdateLODAndRenderState` `004264A0` and `003A4290`, and five compose handles through `003589B0`. Four read `00377C20`, and `002B0280` reads the display-name getter `00263990`. `WorldActor_TestBoundsAgainstViewFrustumAtPosition` `003223C0` reads `00265090`, `003C29A0` reads `00265200` and `00506700` reads the string selector `002B58B0`. In the service direction, the teardown `00300E40` calls `BattleUnit_ComputePresentationSuppressionMask` `003125E0`, and the defeat path `00312280` calls `Reward_PublishExpLpPresentation` `0028FB80`. Seventeen presentation bodies, among them `003A7460`, `0044A620` and `0052E430`, call `0036A190`. That is a two-instruction allocation entry (`edx = 1`, then a jump into the allocator), and it is MECHANICAL. The edges around `00426130`, `00427280` and `00427320` are the render and animation object's own internals, with callees `00426C90`, `00422C20`, `003E55F0` and `0042F310` and callers `00426520`, `00426560` and `00521000`. The page cites those three only as the tails of its `[+0x284]`-gated resolves, and they are OUT-OF-SCOPE here. Presentation renders the units this page builds by reading their focus handle, names and field bit, and it is told about teardown and rewards, but it contributes nothing to a unit's definition.

**RNG_Random_Selection — SERVICE (3 edges).** The area initializer `002342F0` stores the bumped seed counter into the shared gameplay LCG through `RNG_SharedGameplayLCG_SetState` `00328D80`. The status-mask tail `002394C0` and `002398F0` draw from that LCG through `RNG_SharedGameplayLCG_NextU32` `00328370`. The build's random draws come from the shared gameplay generator that the area transition reseeds. They do not come from a private stream.

**Resource — MECHANICAL (15 edges).** Seven Resource-filed bodies call the allocation entry `0036A190`, among them `00249210`, `0024A1D0`, `00259DF0` and `00384420`. `00259DF0` and `00384420` also call `0036C1A0`, which pushes a byte onto a 31-deep selector stack, and `0036C110`, which pops it. `00384420` also calls `0036C660`, which writes a tag into a block whose header carries the `0xFF12` marker. `00406A60` calls `0024A440` and `0024A680`; both are Resource bodies that were not read here. `00427320` resolves an entry through `ResourceTable_ResolveEntryByIndex` `002ED570`. These are allocator, allocator-bank and table-lookup machinery shared with the resource layer, and no unit-definition data crosses them.

**Rewards_Progression_Economy — CLIENT and SERVICE (63 edges).** The level grower `0030C470` of §2.6 and the level-set `0030C650` are progression-filed. The initializer `0023AC80`, the party walk `00239960`, `002398F0`, `BattleAction_UpdateSpecialPresentationSequence` `00306760` and `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0` all call `0030C470`. The defeat path `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` calls `GameState_GetGil` `00253690`, `GameState_SetGil` `00254EE0`, `Reward_ComputeExperienceForRecipient` `002F8BB0`, `Reward_ComputeLicensePointsForRecipient` `002F90C0`, `EnemyChain_UpdateOnDefeat` `00317ED0`, `Loot_RollDropEntries` `003180F0` and `Loot_CreateWorldPickup` `00319CA0`. The gil apply `GameState_AddGilClampedAndNotify` `003004B0` is called by `00316DF0`, `0032A7F0` and `0050FAF0`, and `00469E80` is its delta-report arm. `002342F0` calls `Loot_InitializeWorldPickupPool` `00319B10`. This page documents how a unit's level, LP and gil state are first written, and the progression layer owns the growers and gil accessors it writes them with, which the defeat rewards call again later.

**Save_Load_Settings — CLIENT and SERVICE (5 edges).** `SaveRuntime_RebindImageBackedGameplayState` `00238A80` calls `BattleSystem_ResetRuntimeState` `00237DF0`. It also reads `SaveImage_GetActiveRuntimeBuffer` `002EF640` and is called by `SaveRuntime_ResetActiveImageAndRebindState` `002EF650`. The field-id getter `003148F0` calls `SaveImage_GetPersistentPayloadBase` `002EF2B0` and is read by `SaveImage_FinalizeHeaderAndChecksum` `00583D60`. Rebinding a save image resets battle runtime state through this page's reset, and the active field id lives in the save payload. Neither edge carries unit-definition data.

**Script_VM_Native_Bridge — CLIENT (95 edges).** Native verb bodies pop their arguments from the VM value stack and call this page's functions. `0050FAF0`, `005103B0` and `00510440` call `VMValueStack_PopInt32CoerceFloat32` `00267E10`. `00510440` and `005103B0` are the `btlAtelSetAbility`/`btlAtelSetStatus` verbs that tail into `002390B0`/`002394C0`, `0050F910` pops two ints and jumps to `002398F0`, and `VM_Spawn_ApplySelectedUnit` `00510160` calls `0023A3B0`. The script interpreter `WorldActorScriptVM_InterpretBytecode` `0025E4C0` and `ScriptVM_SubmitActorRuntimeRequest` `00268850` call `003587C0`. The rest of the edges are other verb bodies calling page accessors. Fourteen read the focus getter `003590D0` and twelve compose through `003589B0`. Eleven read `00265200`, ten call `002ECF10` and six call the actor-event reset `002EB430`. Seven read `BattleStats_GetByMappedBattleSlot` `00320AB0`, for example `0050FD00` and `0050FF20`. Four read `00377C20`, and `0050D8F0` and `0050DAD0` call the allocator bank pair `0036C110` and `0036C1A0`. §2.8's point that a foe's statuses and augments come from its script is exactly this crossing. The script layer drives unit build and edit through native verbs. The page's functions are the verbs' targets and hold no script state.

**Spawn_Encounter_Lifecycle — CLIENT and SERVICE (25 edges).** Spawn bodies call into the page's build and teardown functions. `Spawn_ApplyScriptSelectedUnit` `0023A3B0` calls `0023A570`. `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` calls `00308010`, `0030FED0`, `BattleUnit_SetupEngagedActionState` `002FED60` and `002FEDC0`. `SpawnGroup_TeardownAllGroupedSpawnUnits` `00234880`, `SpawnGroup_TeardownUnitsByGroupMask` `00234990`, `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` and `SpawnGroup_TeardownAllUngroupedSpawnUnits` `00237690` call the teardown `00300E40`, and `Spawn_CountActiveCapTrackedActors` `00308D90` walks the slot accessors. In the other direction, `0023A570` resolves `SpawnKeep_ResolvePrimaryEntry` `00236100`, `0023A3B0` calls `Spawn_PrepareRandomCandidateForCurrentEntry` `002355A0`, and `002342F0` calls `SpawnKeep_RotatePersistenceBanksForAreaTransition` `00233780` and `SpawnGroup_ResetLifecycleLedger` `00307090`. The spawn layer is what builds and retires enemy units through this page's apply and teardown, and the area transition rotates that layer's persistence banks in the same battery.

**Status_Periodic_Terminal — CLIENT and SERVICE (61 edges).** The area initializer's 40-record status clear is `BattleStats_RemoveStatusMode0` `0030E990`, called from `002342F0`. The `btlAtelSetStatus` tail `002394C0` adds statuses through `BattleStats_AddStatusMode3` `0030EAE0`, and `002348E0` calls `BattleUnit_ResetActionControlForStatusTransition` `00300140`. The reset `00236A60` calls `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` `00320450`. `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` calls four page bodies: `0026DC60`, `002E8060`, `002ECF10` and `00311F70`. The per-bit core `0030E360`, the recompute `0030FED0` and `0030F690` call and are called by the status bodies as on the contract page, and `0030E360` calls `00300FC0` and the defeat path `00312280`. `BattleFormula_ApplyGlobalPeriodicDrainModes` `00385CA0` reads the mask test `0031A900`. Statuses written at build time, including a foe's script-given ones, go through the status layer's own add, remove and recompute bodies, and a terminal status reaches this page's teardown and defeat path from that layer.

**Story_Event_Quest_Hunt — SERVICE (1 edge).** `Actor_GetDisplayName` `00263990` calls `PersistentFlag_QueryBank2048` `0032A930`, and the result picks which of the two authored names is displayed. That is the name-dictionary mechanism: a story flag can switch an actor's shown name. The build does not write the flag.

**UI — CLIENT and SERVICE (39 edges).** Fourteen UI bodies call the string selector `002B58B0` of §2.7, among them `00273E30`, `002986E0` and `00560210`. `BattleMenu_BuildCommandEntryList` `0031EB20` reads six page accessors: `00236820`, `00236850`, `00263E30`, `0030B0E0`, `00313F60` and `00322C50`. Five UI bodies read the field-id getter `003148F0`, among them `0029C530` and `003F9720`, and `002AC5F0` reads the display name `00263990`. `002BFD20` calls `00272CE0`, and `00405310` calls `00405100`. In the service direction, `BattleSystem_ResetRuntimeState` `00237DF0` calls the UI-filed `00313840`. That body clears bit 0 of the battle-state `+0x5B04` word, calling `0035C620` when the bit was set, and resets the fields at `+0x5AD0`..`+0x5AD8`. `00306760` also calls `0035C620`. The UI reads names, strings and units that this page builds, and the runtime reset clears the battle menu's state words through a UI body.

**WorldAreaField and World — CLIENT, SERVICE and MECHANICAL (79 edges).** The area-transition initializer `BattleSystem_InitializeAreaState` `002342F0` is WorldAreaField-filed and runs the reset battery of the residual-placements section. It calls `00307FF0`, `0030C3F0`, `0030E010`, `003183A0`, `0031A8F0`, `00322190`, `003221B0`, `00327360`, `00328D80`, `0033A380`, `00383740`, `003924B0`, `00239960` and `00233780`, and it is called by the World body `00266D10`. Twelve world bodies read the field-id getter `003148F0`, among them `WorldField_InitializeCurrentFieldRuntimeParameters` `0026D910`, `WorldPersistence_ResetBanksForFieldTransition` `0026DB30` and `00377C70`. `003148F0` also reads the save payload base (see Save_Load_Settings above) and is read by `005369C0`, which also calls `MapRef_GetAreaArdFieldResourceIndex` `00264ED0`. `BattleSystem_RunFieldFrameOrchestrator` `00234590` calls `00313F60` and `003272A0`. `003266C0` calls `00313F60`, `00377C20` and `00377C70`. The allocator entries `0036A190`, `0036C110`, `0036C1A0` and `0036C660` are called by `MapRef_BeginLoadResources` `00268750`, `AreaArd_BindLoadedRootAndBattleSections` `003EA710`, `AreaArd_LoadOrUnloadFieldResource` `003EA820` and the World body `00378540`; that part is MECHANICAL. The world layer triggers this page's area-transition reset and supplies its field id and bit-15 permission, and the map and ARD loaders are other clients of the same allocator.

## The `0023A570` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`0023A570` (1,808 B) is `BattleUnit_ApplyUnitDefinition` — §50 has the
signature, §94 the spawn-record fetch, §259 the engaged decision. The subtree
owns the three helpers: `00236100` at `0023A776`, `00254A40` at `0023A814`,
`00237040` at `0023AC1C`.

| member | role | interior |
| --- | --- | --- |
| `00236100` (56 B) | `SpawnKeep_ResolvePrimaryEntry` — `rcx` is a byte-counted table (`[rcx]` count, `byte[rcx+1+i]` lane ids); `edx` bounds-checked, entry ≠ `0xFF` → `id × 0x250` into `[0208E690]` (`00236126`–`0023612D`) | [`00236126`](../../_index/ADDRESS-INDEX.md) |
| `00237040` (55 B) | the engaged-state fork — `00308010(rcx, 1)` test, then `cmovne` picks tail `002FED60` or `002FEDC0` (`0023705C`–`00237074`) | [`00237068`](../../_index/ADDRESS-INDEX.md) |
| `00254A40` (6 B) | `SpawnHistory_GetCounterWrapThreshold` — returns `0x34` | [`00254A40`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00236A60`, `00303EC0`, `00304630`,
`00308010`, `002FED60`, `002FEDC0`, plus the apply battery this page's
walk-through already enumerates.

## The `0030C650` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0030C650`, 570 B):
target `r14d = min(edx, 0x63)` — 99 (`0030C65B`/`0030C682`); the silence
flag is `r13d = ~(r8d >> 1) & 1` (`0030C660`–`0030C676`); current level
`ecx = byte[rcx + 0x1C2]` (`0030C66F`) seeds `esi` and the loop exits at
`esi >= r14d` (`0030C686`); when `r13d` is set, `esi == r14d - 1` short-
circuits before the last step (`0030C6A3`–`0030C6AE`). Each iteration
resolves the owner through `0031B860` (`0030C6BC`).

| member | role | interior |
| --- | --- | --- |
| `002F9BD0` | growth-formula evaluator — `mulss xmm1, [008C5B34]` ≈ 0.7778 (`002F9BD7`), `comiss` vs `[008F3134]` (`002F9BE3`), `word[rax+0x50]` vs `0xFFFF` sentinel (`002F9C90`–`002F9C99`), `0031A900` + `0020E600` ×2 on `[02EBF0F8]` (`002F9C69`–`002F9CBE`), `[01F44830]` read (`002F9C0A`) | [`002F9BD7`](../../_index/ADDRESS-INDEX.md) |
| `00329210` | recompute battery — `lea 0208D328` (`00329213`), `00861EC0` free, `00236850`/`00236820` pair, `[rax+0x698]` vs `r14` compare (`00329293`), `003590D0`, `02089340` bit-4 test (`003292B4`), `003588B0`/`00263E30`/`003135E0`/`00313800` chain (`003292BF`–`003292EA`) | [`00329213`](../../_index/ADDRESS-INDEX.md) |
| `0046A690` | per-stat lookup walker — `byte[rcx+0x1C2]` again (`0046A6BF`), `0046AB10` probes against indices `0x37`/`0x38`/`0x39` (`0046A741`–`0046A772`) | [`0046A6BF`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0031B860`, `0031A900`, `0020E600`,
`00861EC0`, `00236850`, `00236820`, `003590D0`, `003588B0`, `00263E30`,
`003135E0`, `00313800`, `0046AB10`.

## The `00237DF0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00237DF0` = `BattleSystem_ResetRuntimeState` (~270 B): member
`0023AF50` (`00237DF6`), `0xFFFF` mask + `ebx` vs `0xFF`/`0x28`
bounds (`00237E00`/`00237E08`/`00237E2D`), `[02EBF190]` block
(`00237E18`), `0023AC80`/`0030DA10`/member `0032A160`/
`003183A0`/`00329CC0`/`00313840`/`00304680` (`00237E26`–`00237E4B`),
then the global zeroes — `dword[02089374] = 0`, `word[02089372] =
word[02089370] = ax`, `byte[0208D454] = 0` (the spawn-history bank
selector this page counts, `00237E6B`) — `002FA230`/`002FA260`/
`002FA210`, `00229ED0`, `dword[0208E6B4] = 0` (`00237E8D`), and a
`003272A0` roster walk reading `[rax+0x698]` `byte[+4]`/`byte[+5]`
against `0x12` (`00237EC3`/`00237ED2`).

| member | role | interior |
| --- | --- | --- |
| `0023AF50` (203 B) | id lookup — `002370C0` (`0023AF56`), `[02EBF048]` context (`0023AF70`), `ebx` vs `dword[rax+4]` bound (`0023AF80`), `dword[rax+0xC]` → `0020E600` (`0023AF8C`) | [`0023AF8C`](../../_index/ADDRESS-INDEX.md) |
| `0032A160` (11 B) | global zeroer — `dword[0208D45C] = 0; ret` (the `0032A174`+ `[0208CD18]`/`0026DC60` body is a sibling) | [`0032A160`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0023AC80`, `0030DA10`, `003183A0`,
`00329CC0`, `00313840`, `00304680`, `002FA230`, `002FA260`,
`002FA210`, `00229ED0`, `003272A0`, `002370C0`, `0020E600`.

## The `00236A40` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00236A40` (28 B) — the apply trigger: `dword[02089300] = 1`
(`00236A44`), `call 002376F0` (`00236A4E`), tail `jmp 00237CA0`
(`00236A57`).

| member | role | interior |
| --- | --- | --- |
| `002376F0` (1,445 B) | the definition write-battery — iterates `qword[02EBF138]` scratch rows through `0020E600` and stores each field into the `0208CD20`–`0208CE58`/`02089340` staging cells (`00237731` publishes `0208CEC0` to `0208CD20`; `00237B6E`/`00237B85`/`00237BEE`/`00237C00`/`00237C17`/`00237C88` are representative word/qword stores) | [`00237B85`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0020E600`, `00237CA0`.

## The `00300CE0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00300CE0` (`BattleStats_ModifyPrimaryResource`, ~30 B) — resource write
under a six-register save.

| member | role | interior |
| --- | --- | --- |
| `002FA540` | `00320450(rcx)` resolve, `xorps xmm1` clear (`002FA549`/`002FA54E`) | [`002FA549`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00320450`.

## The `00317480` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00317480` (~193 B) — six-register body (`00317480`/`00317489`).

| member | role | interior |
| --- | --- | --- |
| `003237C0` | helper under a `rsi` save (`003237C0`) | [`003237C0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hub `00265200` (2026-09-17, SWE2-EC7)

`00265200` — 55 B, 10 A-measured callers at census. Interior verified: a variant-field float
getter. `byte [rcx+3] >> 5` selects the shape (`shr edx,5` at
[`0026520C`](../../_index/ADDRESS-INDEX.md)): 1 -> `[[rcx+0xB8]+0x38]`, 2 -> `[[rcx+0xB8]+0xA8]`,
anything else or null -> `+0.0f`. The two floats live at different depths of the same `+0xB8`
sub-record — a discriminated stat read, not two unrelated fields.


## Interior citation — frontier hub `002646C0` (2026-09-18, SWE2-EC7)

`002646C0` — 141 B, 10 callers (Movement); the context position read the build path
invokes. Interior verified: `byte[rcx+3] >> 5` selects the record class (`002646C9`–`002646D6`);
class 1 and 2 both read the `[+0xB8]` context's `+0`/`+4`/`+8` into the three out-dwords
([`002646E9`–`002646FD`](../../_index/ADDRESS-INDEX.md)); when context bit `+0x107 & 1` is
set the `+0x40`/`+0x44` offset pair is added into the first two out values
(`00264709`–`00264720`); other classes zero all three outs. The base-plus-offset read the
steering rows consume.


### Interior citation — frontier hub `00324020` (2026-09-18, SWE2-EC7)

`00324020` — 218 B, 7 callers, `BattleStats_CountLicenseBits00To17`. Read from
the shipping image: a popcount over the license bitmask at `[rbx+0x194]` —
`rol dl` walks the bit position and `shr r8/rcx/rax, 3` picks the byte, each
`test byte [rN + rbx + 0x194], dl` + `cmove` pair
([`0032404F`](../../_index/ADDRESS-INDEX.md)) conditionally skips the increment
so the accumulator `r9` counts only set bits, six bits per iteration over three
loop passes. Returns the count in `eax`.

### Interior citation — frontier hub `002ECF10` (2026-09-18, SWE2-EC7)

`002ECF10` — 65 B, 20 callers: the fourth `+0x284`-gated render-record resolve —
`[rcx+0xC0]` null-gate, `dword[rax]`/`word[rax]` `-1` sentinels, `imul rcx, rax,
0x740` ([`002ECF33`](../../_index/ADDRESS-INDEX.md)) into the render array, and a
tail to `00426130` only while the record's `[+0x284]` word is zero. Sibling of
`002E73C0`/`002ECEC0` — same idiom, different consumer tail.

### Interior citation — frontier hub `002E42D0` (2026-09-18, SWE2-EC7)

`002E42D0` — 89 B, 7 callers: the fifth `+0x284`-gated resolve's caller-side
arm. `[rcx+0xC0]` null/`dword == -1`/`word == -1` gates fall through to
`dword[rbx+0xEC] = 0`; the live arm resolves the `0x740` record at `022C6F28`
requiring `[+0x284]` non-zero and calls `00427280` on it at
[`002E4314`](../../_index/ADDRESS-INDEX.md) — the field-clear either way.

### Interior citation — frontier hubs `00392170`, `002699D0` (2026-09-18, SWE2-EC7)

`00392170` — 132 B, 5 callers: deferred registration — appends `rcx` to a
`0x80`-capped pointer table under `[05EE1xxx]` globals, resolves two
out-params via `002646C0` + `00265090`, takes `maxss` of the two floats at
[`003921CB`](../../_index/ADDRESS-INDEX.md), then calls `00392200` with the
counter and bumps it.

`002699D0` — 66 B, 4 callers: resolve-substitute-forward — `002ECA00(rcx,1)`
+ `002E8060(rcx)`, then when `byte[rbx+0x18] == 1` the result of
`003587C0(movsx byte[+0x19], word[+0x1A])` substitutes the record at
[`002699F9`](../../_index/ADDRESS-INDEX.md) before tailing `002EB430`.
### Interior citation — frontier hub 00308010 (2026-09-18, SWE2-EC7)

**00308010** (`BattleUnit_ShouldEnterEngagedAction`, 33 B, 4 A-measured callers) — the engaged-check predicate the transition chain consumes. `[rcx+0x698]` (the unit's command record) null → 0; else `byte[record+5] & 1` → `00308040` (unary engaged path) or `00308130` (targeted path). Two of the four callers feed the action-state transitions the unit-definition build sets up. In-scope: `+0x698` fetch [`0030801A`](../../_index/ADDRESS-INDEX.md); mode-byte test [`00308021`](../../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## SWE2-EC7-25 update (2026-09-18) — `0033C9B0` two-call build compose

`0033C9B0` (75 B) is the cookie-checked compose (`0x148` frame, `00808C40`
guard): `00336710` marshals `rcx` into `rsp+0x20`, then `0033E1F0` consumes
the staged record — the build step the unit-definition and combat callers
share. Interior anchor `0033C9D4` (the `00336710` call).

## SWE2-EC7-36 update (2026-09-19) - `00392200`

`00392200` (679 B) is the nav obstacle grid rasterizer - see
[how-a-unit-finds-its-way-across-the-navigation-mesh.md](../../06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md)
section 10. `00392200(id, x, z, r)` tests each grid cell under the square
`x ± r, z ± r` against the circle `004690B0` and on a hit sets bit `id` in the
cell's 0x24-byte record and increments its occupancy byte
(`_index/candidates/nav-obstacle-grid/`, obstacle_grid.py R1).
*(Label corrected 2026-09-28, FABLE-REQ-FRONTIER-CARRIER-00392200-LABEL: the
"battle-unit definition reader" reading was wrong.)* Interior anchor
`003923CD` (an `00808C40` call).

## SWE2-EC7-43 update (2026-09-19) - `0033E1F0`

`0033E1F0` (278 B) is a battle-unit-build body - three `call [rip->008C3098]` (tick-clock import `01CCEF20`) folded into `/100`, `/3`, `/10` magic-multiply steps that write `[rdi+0x10]`/`[+0x38]`/`[+0x3c]` flags and `[rbx+0x108]->+0x108` float. Interior anchor `0033E22A` (the first import call).

## SWE2-EC7-45 update (2026-09-19) - `00426130`

`00426130` (238 B) is the `[+0x284]`-zero-gated tail body - `00427320` single call on the `0x740`-stride animation object. Interior anchor `0042617F` (the `00427320` call).

## SWE2-EC7-49 update (2026-09-19) - `0030F4D0`

`0030F4D0` (195 B) is an HP/MP reconciler call site - `0030B0E0`/`0030F340`/`0030F5A0`/`0030F690`/`00320A40`. Interior anchor `0030F50A` (a `0030B0E0` call).

## SWE2-EC7-49 update (2026-09-19) - `0030F3F0`

`0030F3F0` (190 B) is an HP/MP reconciler call site - `0030F340`/`0030F5A0`/`0030F690`/`00320AB0`. Interior anchor `0030F437` (a `0030F340` call).

## SWE2-EC7-55 update (2026-09-19) - `004690B0`

`004690B0` (237 B) is a call-free bounds containment test - `comiss` checks on `[rcx]`/`+8`/`+0x10`/`+0x18` against point ranges, boolean return. Interior anchor `004690D4` (the `[rcx+0x10]` bound add).


## SWE2-EC7-96 update (2026-09-20) - `00307FF0` + `003004B0` measured

`00307FF0` (17 B) is the two-field reset `002342F0` and
`002348E0` run: `02CD1F51` loses bits 1-2 (`& 0xF9`) and the
`02CD1F40` qword zeroes - the paired clear the build path applies
before reuse.
Interior anchor `00307FF9` (the qword clear).

`003004B0` (76 B) is the clamped apply `00316DF0`, `0032A7F0`
and `0050FAF0` call: `00253690` supplies the base, `ebx = max(0,
base + ecx)` feeds `00254EE0`, and `dil` bit 0 additionally hands
`ebx - base` to `00469E80` - the delta-report arm the callers
toggle.
Interior anchor `003004C3` (the `00253690` call).

`00300BA0` (28 B) is the always-variant shim: forces `r8d = r9d = 1`, passes the fifth stack arg through, and calls `003008A0` - the fixed-flags lane the unit-build callers share.

Interior anchor `00300BB2` (function `00300BA0`).
