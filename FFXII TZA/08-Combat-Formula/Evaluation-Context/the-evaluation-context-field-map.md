---
system: The evaluation context — the 0x30-byte record (0x2A of named fields) every calculator slot receives, and which status / augment ids each slot tests in it
category: 08-Combat-Formula
status: AUDITED
owner_layer: PrimaryOwner:CombatFormula
evidence_tier: 1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: BattleFormula_BuildEvaluationContext 003847C0 read to its ret; a typed field scan seeded at its output and
    at the third argument of all 152 calculator slots (hop_scan --argseed), depth 1, control 00390390's read at
    +0x1C found; 209 accesses in 77 functions over 12 offsets; every layer-byte test's immediate decoded to an id
last_reviewed: 2026-09-11
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-evaluation-context-pass-1
  last_pass_kind: falsification
  crossref_clean: true
  reopened_count: 0
---

# The evaluation context — what a calculator slot is handed

> Before a recipe's slots run, the resolver builds a small record on its stack: the action id, the
> source's and the target's merged flags, the result record's address, one byte of the target unit,
> and — the part that matters most — **the source's status and augment layers merged into 128
> bits**. Every slot that "checks for an accessory" or "checks for a status" is a bit test on those
> sixteen bytes. This page maps the record and lists which id each slot tests.

## 1. What the player sees

The Thief's Cuffs make Steal roll three times; a Cameo Belt ignores the weather's accuracy
penalty; an Agate Ring ignores weather scaling. None of those is checked against the inventory —
they are bits in a 16-byte field the formulas read, filled once per resolution from the source's
two effect layers, where a status and an augment with the same id are indistinguishable.

## 2. Native mechanism

### 2.1 The builder

`BattleFormula_BuildEvaluationContext` (`003847C0`, 273 B) — `(ctx, result, sourceStats, targetStats,
actionId)`, called by the resolver at `003860D5` with the context at `[rsp+0x48]`:

| site | what |
|---|---|
| `003847D8`–`003847F3` | zeroes `+0x00`, `+0x08`, `+0x18`, `+0x20`, `+0x28` (qwords) — so bytes `0x00`–`0x0F` and `0x18`–**`0x2F`**; `+0x10` is skipped because the result pointer is written at `003847FF`. **The last store reaches `+0x2F`, six bytes past the named fields — the record is `0x30`, see §9** |
| `003847F7`–`003847FF` | `+0x00` = the action id (word), `+0x10` = the result record |
| `00384808`–`00384818` | `+0x04` = source `+0x64 \| +0x3C` when there is a source |
| `00384820`–`00384858` | **the merge**: for `id` in 0..127, if bit `id & 7` of source byte `+0x68 + (id >> 3)` or of `+0x78 + (id >> 3)` is set, set bit `id & 7` of `+0x1A + (id >> 3)` |
| `0038485F`–`00384885` | `+0x08` = target `+0x64 \| +0x3C`; `+0x18` = the target unit's byte `+0x55` or `-1` |
| `00384889`–`0038489D` | no target unit → `+0x08 &= ~bit 12`, id 15 cleared |
| `003848A1`–`003848B8` | result `+0` bit 5 → `+0x08 &= ~(bits 12, 16, 23)`, `+0x18` forced 0 when it was `0xD`, id 15 cleared |

> **What a census like this cannot see (2026-09-11, OPUS-NOTICE-CENSUSWRITES).** Seeds: the builder's output register and the slots' argument — the constructor is the seed here, so this census is the exception: its writes are as covered as its reads.
> A scan seeded on *accessors* reaches *consumers*: a constructor that builds the record before
> any accessor can return it is reached only if it is seeded on its own. So the **reads** below are
> the well-covered side and the **writes** are under-covered wherever a constructor or an
> index-derived writer sits outside the seeds — do not rest an absence-of-writer claim on this
> TSV alone; pair it with a displacement scan of the candidate writers.

### 2.2 The field map

| offset | width | type | what | w / r | writers (sites) | readers (sites) |
|---|---:|---|---|---|---|---|
| `+0x00` | 2 | u16 | **the action id** — the resolver's `cx` (`00385F9A`), stored at `003847FC`; `BattleFormula_BuildCandidateStatusMask` `003851F0` and `00390190` read it | 1 / 3 | `BattleFormula_BuildEvaluationContext` `003847C0` (`003847D8` +1) | `00390190` (`003901B3`); `BattleFormula_BuildCandidateStatusMask` `003851F0` (`0038522A` +4); +1 more |
| `+0x04` | 4 | u32 | **the source's merged flags** — stats `+0x64 | +0x3C` (`00384808`–`00384818`); fourteen slots read it | 1 / 14 | `BattleFormula_BuildEvaluationContext` `003847C0` (`00384818`) | `00388990` (`00388990`); `003891F0` (`003891F0`); +12 more |
| `+0x08` | 4 | u32 | **the target's merged flags** — stats `+0x64 | +0x3C` (`0038485F`–`00384868`); the resolver clears bit 12 when the target has no unit and bits 12 / 16 / 23 when the result's byte `+0` has bit 5 (`00384896`, `003848A6`); thirty-one slots read it | 1 / 31 | `BattleFormula_BuildEvaluationContext` `003847C0` (`003847DE` +3) | `BattleFormula_RollSpecialGuardOutcome` `00387FD0` (`00388065`); `00388250` (`00388274`); +29 more |
| `+0x10` | 8 | ptr | **the result record** — the resolver's `rdx` (`003847FF`); the slots write their outcomes through it ([the result record](../../07-Combat-Action/Result-Record/the-result-record-field-map.md)) | 1 / 34 | `BattleFormula_BuildEvaluationContext` `003847C0` (`003847FF`) | `BattleFormula_RollSpecialGuardOutcome` `00387FD0` (`0038822D`); `BattleFormula_RollAndStoreComboCount` `00388660` (`003886E8` +2); +32 more |
| `+0x18` | 2 | i16 | **the target unit's byte `+0x55`**, or `-1` without a unit (`0038487C`–`00384885`); forced to 0 when it is `0xD` and the result's `+0` bit 5 is set (`003848AD`–`003848B4`) | 1 / 11 | `BattleFormula_BuildEvaluationContext` `003847C0` (`003847E5` +2) | `BattleFormula_BuildEvaluationContext` `003847C0` (`003848AD`); `00387F70` (`00387F76`); +9 more |
| `+0x1A` | 1 | u8[16] | **the source's merged status / augment layers**, ids 0–127 as bits: for every id, bit `id & 7` of byte `+0x1A + (id >> 3)` when either the stats record's `+0x68` (status) or `+0x78` (augment) layer has it (`00384820`–`00384858`); this byte holds ids 0–7 — id 2 (Petrify / **AccuracyBoost**) is tested by `00389370`, `003895D0`, `00389610` (the weather accuracy slots) | 0 / 3 |  | `00389370` (`00389548`); `003895D0` (`003895D4`); +1 more |
| `+0x1B` | 1 | u8 | ids 8–15: 8 (`00389290`, `0038AF90`, `0038B150`), 9 (`0038A680`), 10 / 11 (`0038BC00`), 13 (`BattleFormula_ComputeComboChance` `00388550`), 14 (`00389650`, `0038C920`, `0038E2D0`), 15 (sign tests at `00387CB0`, `003889F0`, `0038DD20`, `0038DF00`, `00390190`, `00390240`); the builder clears id 15 in the two forced cases (`0038489D`, `003848B8`) | 1 / 15 | `BattleFormula_BuildEvaluationContext` `003847C0` (`0038489D` +1) | `BattleFormula_ComputeComboChance` `00388550` (`0038855F`); `003889F0` (`00388A22`); +13 more |
| `+0x1C` | 1 | u8 | ids 16–23: 16 (Disease / **Weatherproof**, `0038B220`), **17 (Lure / Thievery — the steal's three-roll branch, `00390390` at `003904A5`)**, 18 (`00388F20`) | 0 / 3 |  | `00388F20` (`00388F2A`); `0038B220` (`0038B23D`); +1 more |
| `+0x20` | **1** | u8 | ids 48–55, read as a byte by `BattleFormula_ApplyTargetHpPostMultipliers` `0038F890` (`movzx ecx, byte ptr [r8 + 0x20]`). ~~8~~ — the `8` was the *zeroing* qword's width, not the field's (2026-09-13) | 1 / 1 | `BattleFormula_BuildEvaluationContext` `003847C0` (`003847EC`) | `BattleFormula_ApplyTargetHpPostMultipliers` `0038F890` (`0038F890`) |
| `+0x26` | 1 | u8 | ids 96–103: 103 (sign tests at `00389290`, `0038AF90`, `0038B150`) | 0 / 3 |  | `00389290` (`003892C5`); `0038AF90` (`0038AFC7`); +1 more |
| `+0x28` | 1 | u8 | ids 112–119: 116 / 117 / 118 (`BattleFormula_BuildCandidateStatusMask` `003851F0`), 119 (`0038DD20`) | 1 / 2 | `BattleFormula_BuildEvaluationContext` `003847C0` (`003847F3`) | `0038DD20` (`0038DD43`); `BattleFormula_BuildCandidateStatusMask` `003851F0` (`0038541E` +2) |
| `+0x29` | 1 | u8 | ids 120–127: 120 / 121 (`0038DD20`), 122 / 123 / 124 (`0038DF00`), 125 / 126 / 127 (`0038E2D0`) | 0 / 3 |  | `0038DD20` (`0038DD98` +1); `0038DF00` (`0038DF23` +2); +1 more |

### 2.3 Which slot tests which id

Decoded from the immediates of every `test` on `+0x1A`–`+0x29` in the scan (id = 8 × (byte − 0x1A)
+ bit). Names are [the namespace table](../Status-And-Augment-Namespaces/README.md)'s where it has
them; the merge does not distinguish the status from the augment of the same id.

| id | status / augment | tested by |
|---:|---|---|
| 2 | Petrify / **AccuracyBoost** (Cameo Belt) | `00389370` (`00389548`), `003895D0` (`003895D4`), `00389610` (`00389614`) — the weather accuracy slots |
| 8 | **Poison** (status; augment 8 "Raises magick power when HP Critical") | `00389290` (`00389290`), `0038AF90` (`0038AF90`), `0038B150` (`0038B15A`) |
| 9 | **Silence** (status; augment 9 "Increases physical damage dealt while empty-handed") | `0038A680` (`0038A6B1`) |
| 10, 11 | **Sap**, **Oil** (statuses; augments 10 / 11 "Raises strength when HP Critical" / "… when character has full HP") | `0038BC00` (`0038BC0F`, `0038BC54`) |
| 13 | ~~**Disable** (status;~~ **the combo augment** (augment 13 "Improves chance of scoring multiple hits", Genji Gloves `0x1164`) *(corrected 2026-10-02, OPUS: `00388550` tests context `+0x1B` bit 5, merged id 13, to scale the combo rate by 1.8f instead of 0.7f (`0038855F`); augment 13 is "Improves chance of scoring multiple hits.", carried by Genji Gloves `0x1164`, and the 32 statuses are in neither layer (the-thirty-two-statuses.md, `BattleFormula_BuildEvaluationContext`), so the status reading is unsupported; combat-formula-step-table.md, the section "The hit pipeline's odds: knockback, counter, combo, the ranged critical and the post-modifiers")* | `BattleFormula_ComputeComboChance` `00388550` (`0038855F`) |
| 14 | **Immobilize** (status; augment 14 "Improves potency of restorative items") | `00389650` (`00389650`), `0038C920` (`0038C920`), `0038E2D0` (`0038E40C`) |
| 15 | **Slow** (status; augment 15 "Reverses effects of restorative items") | sign tests on the byte: `00387CB0` (`00387D0D`), `003889F0` (`00388A22`), `0038DD20`, `0038DF00`, `00390190` (`003901BE`), `00390240` (`0039024F`) |
| 16 | Disease / **Weatherproof** (Agate Ring) | `0038B220` (`0038B23D`) |
| **17** | Lure / **Thievery** (Thief's Cuffs) | `00390390` (`003904A5`) — the steal's three-roll branch |
| 18 | **Protect** (status; augment 18 "Improves chance to strike with magicks") | `00388F20` (`00388F2A`) |
| 103 | augment 103 "Increases magick power when HP is full" (no status of that id) | sign tests: `00389290` (`003892C5`), `0038AF90` (`0038AFC7`), `0038B150` (`0038B19C`) |
| 116, 117, 118 | — | `BattleFormula_BuildCandidateStatusMask` `003851F0` (`0038541E`, `0038547E`, `003854DE`) |
| 119 | — | `0038DD20` (`0038DD43`, sign) |
| 120, 121 | — | `0038DD20` (`0038DD98`, `0038DDE3`) |
| 122, 123, 124 | — | `0038DF00` (`0038DF23`, `0038DF78`, `0038DFC3`) |
| 125, 126, 127 | — | `0038E2D0` (`0038E32D`, `0038E383`, `0038E3CE`) |
| 48–55 | — | read as a byte by `BattleFormula_ApplyTargetHpPostMultipliers` `0038F890` (`0038F890`) |

Twenty-two ids. **Named 2026-09-11 from the data** ([the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md)):
the status names are bank 5 in id order, the augment descriptions come from the 129-row augment
table's name references into `listhelp_ability.bin`; **augments 116–127 carry no name — they are
parameter-only rows** (`0, 0, 0, 40, 30, 20, 30, 20, 10, 10, 10, 10`), so those slots test hidden
augments. Because the context merges the layers, each row above names both readings of the id.
Which slot belongs to which recipe is the recipe page's table; the slot's *test* is here.

## 3. Key addresses

| address | size | what |
|---|---:|---|
| `003847C0` | 273 B | `BattleFormula_BuildEvaluationContext` |
| `00385F60` | 2,302 B | `BattleFormula_ResolveTargetResult` — builds it at `003860BA`–`003860D5`, passes `&ctx` as every slot's third argument (`003863C5`) |
| `01EFA5C0` | | the calculator table — 202 slots, 152 distinct functions, all seeded |

## 4. Data structures and formulas

```
EvaluationContext (0x30 B allocated, 0x2A of named fields, on the resolver's stack at rsp+0x48)
  +0x00  u16   action id            +0x18  i16   target unit +0x55 (or -1)
  +0x04  u32   source +0x64|+0x3C   +0x1A  u8[16] source layers merged: bit (id&7) of byte +0x1A+(id>>3)
  +0x08  u32   target +0x64|+0x3C          = status(+0x68) | augment(+0x78)
  +0x10  ptr   result record
has(id) = ctx[0x1A + (id >> 3)] >> (id & 7) & 1
  +0x2A..+0x2F  tail padding - written (zeroed) by the builder, never read as a field
```

> **Allocate `0x30`.** The builder's last store is `mov qword ptr [rcx + 0x28], rax`, and the
> resolver's next stack slot is `rsp+0x78` — exactly `rsp+0x48 + 0x30`. A record sized `0x2A`
> gets six bytes of whatever follows it zeroed (§9, 2026-09-13).

## 5. Call chain

```
BattleFormula_ResolveTargetResult 00385F60 -> BattleFormula_BuildEvaluationContext 003847C0(&ctx, result, source, target, id)
  -> recipe's committed slots: slot(source, target, &ctx) -> ctx+0x10 = the result ; ctx+0x1A.. = the source's layers
     e.g. 00390390 (steal): ctx+0x1C bit 1 = id 17 -> three rolls ; 003895D0 / 00389610 (weather): ctx+0x1A bit 2 = id 2 -> bypass
```

## 6. Modding notes

- **An augment is a bit here**: granting an accessory's effect without the accessory is setting the
  source's `+0x78` layer bit; the formulas cannot tell.
- **Status and augment collide by id**: the Lure status and the Thievery augment are both id 17 —
  a Lured character steals like one wearing Thief's Cuffs, by construction of the merge.
- **The context is per resolution and lives on the stack**: ~~nothing persists it~~ the context itself is not persisted, but its builder caches the target unit in `02EBF188` (`00384870`) *(corrected 2026-10-02, OPUS: §9, "The builder is not side-effect-free")*.

## 7. What is not known

- [x] ~~**The names of ids 8–11, 13–15, 18, 103, 116–127** the slots test — the namespace table names
  2, 16 and 17 only; the slots that test the rest are the way in.~~ **FQ-1 ANSWERED 2026-09-11** from
  the battle text banks and the augment table (§2's table): statuses Poison, Silence, Sap, Oil,
  Disable, Immobilize, Slow, Protect; augment 103 "Increases magick power when HP is full";
  augments 116–127 are unnamed parameter-only rows.
- [x] **FQ-2.** **What the target unit's `+0x55` byte is** (`+0x18`), and why `0xD` is forced to 0 under the
  result's `+0` bit 5. **FQ-2.** PARTIAL 2026-09-11: it is the definition's **type byte** — the
  installer copies the definition row's `+4` into unit `+0x55` (`BattleUnit_ApplyUnitDefinition`
  `0023ABF0`; [the definition page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md));
  the gambit target selector compares it with a selector operand (`003021CC`–`003021DC`),
  `BattleFormula_BuildRandomElementStatusTransitionResult` carries it (`00386B71`), and `0038D400`
  swaps two scratch words when the *source's* is `0xD` (`0038D4D9`–`0038D505`). What type `0xD` is,
  and the meaning of the values, is the remainder.
  ***ANSWERED 2026-09-18 (FABLE), DATA from the text banks: the byte is the enemy class, and `0xD` is Undead.** The installer copies the `.ard` class row's byte `+4` into unit `+0x55` ([the definition page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md), §2.4), and that byte's vocabulary is battle text bank 13, sixteen names in id order: 0 Hume, 1 Humanoid, 2 Giant, 3 Dragon, 4 Beast, 5 Insect, 6 Plant, 7 Avion, 8 Amorph, 9 Fiend, 10 Elemental, 11 Warmech, 12 `???`, **13 Undead**, 14 Construct, 15 Ichthian (`battle_pack.bin`, banks at `+0xF8`, bank 13 has exactly 16 entries; the class names the bestiary shows). Both compare sites test the whole byte (`cmp byte ptr [rax+0x55], 0xD` at `0038D4D9`; `movzx eax, byte ptr [r15+0x55]` against the selector operand at `003021CC`), so `0xD` is class 13 and nothing else; the party table's own `+4` (`0xD0 + 3k` for the six, `0xA0 + 2k` for the thirteen Espers, 0 for the guests) lies outside 0..15 and is a different field, never equal to `0xD`. *What the two uses do.* `0038D400` swaps the two result-slot pairs when the **source** is Undead: `02AEE004` ↔ `02AEE008` (target HP loss ↔ gain, AJ-9) and `02AEE014` ↔ `02AEE018` (source HP loss ↔ gain, the scratch-block page), the reversal an Undead attacker's drains suffer. The context builder `003848A1`..`003848B8` runs under the result's `+0` bit 5 (`test byte ptr [rsi], 0x20`) and there clears bits 12, 16 and 23 of the merged flags (bit 12 is status Reverse) and forces `+0x18` to 0 when the target is Undead, so bit 5 is the result's no-reversal gate: under it the target is evaluated as class 0 (Hume) and its Reverse is ignored, the same treatment for both reversing conditions. Which authored results carry bit 5 is the action table's business, not this page's. DATA and static, every site named.*

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The builder's fields and the merge | `003847C0` read to its ret (`003847D8`–`003848B8`) | 1 | PROVEN |
| Which slot tests which id | the scan's `test` immediates on `+0x1A`–`+0x29`, decoded; control `00390390` at `+0x1C` found | 1 | PROVEN |
| Every row of the table | [`evaluation-context-accesses.tsv`](evaluation-context-accesses.tsv) (209 rows) | 1 | PROVEN, with the scan's stated limits |

## 9. Related

- [`../Recipe-System/ranged-weapon-recipes.md`](../Recipe-System/ranged-weapon-recipes.md) — the slots and the recipes.
- [`../Steal/the-steal-roll.md`](../Steal/the-steal-roll.md) — id 17 in use.
- [`../Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md`](../Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md) — ids 2 and 16 in use.
- [`../Status-And-Augment-Namespaces/README.md`](../Status-And-Augment-Namespaces/README.md) — the id namespace.
- [`../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md`](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md) — the two layers the merge reads.
- [`../../07-Combat-Action/Result-Record/the-result-record-field-map.md`](../../07-Combat-Action/Result-Record/the-result-record-field-map.md) — what `+0x10` points at.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

Every behavioural claim in §2.1 and §2.2 reproduces from the builder's 273 bytes, and the scan's own
headline reproduces from the TSV beside the page: **209 access rows, 77 distinct functions, 12
distinct displacements**, no duplicate `(function, site, displacement)` triple.

| claim | measured |
|---|---|
| the merge runs `id` over `0..127` | `cmp r10d, 0x80` / `jl` — **128** iterations, with `dl` rotated one bit per pass (`rol dl, 1`) as the `id & 7` mask |
| it reads the status layer `+0x68` **or** the augment layer `+0x78` | `test byte ptr [r9 + r11 + 0x68], dl` / `test byte ptr [r9 + r11 + 0x78], dl`, either setting `r8d = 1` |
| it writes bit `id & 7` of `+0x1A + (id >> 3)` | `and ecx, 7` / `shl r8b, cl` / `or byte ptr [r9 + rbx + 0x1a], r8b` |
| `+0x04` and `+0x08` are `+0x64 \| +0x3C` | `mov eax, [r8+0x64]` / `or eax, [r8+0x3c]`, and the same pair on `rdi` |
| "clears bit 12" and "bits 12 / 16 / 23" | `and dword ptr [rbx+8], 0xffffefff`; `and dword ptr [rbx+8], 0xff7eefff` — complement `0x00811000` = bits **12, 16, 23** |
| `+0x18` is the unit's `+0x55` or `-1`, forced 0 when `0xD` | `movzx ecx, byte ptr [rax+0x55]` / `or ecx, 0xffffffff`; `cmp word ptr [rbx+0x18], 0xd` / `mov word ptr [rbx+0x18], bp` |
| the builder clears id 15 in both forced cases | `and byte ptr [rbx + 0x1b], 0x7f` at `0038489D` **and** `003848B8` — bit 7 of byte `+0x1B` is `8×1 + 7 = 15` |
| the result's byte `+0` bit 5 is the gate | `test byte ptr [rsi], 0x20` |
| every row's id range | `+0x1A`→0–7, `+0x1B`→8–15, `+0x1C`→16–23, `+0x20`→48–55, `+0x26`→96–103, `+0x28`→112–119, `+0x29`→120–127 — all consistent with `8 × (byte − 0x1A) + bit` |

### ⚠ The record is `0x30` bytes, not `0x2A`

The five zeroing stores are **qwords**. The last is `003847F3 mov qword ptr [rcx + 0x28], rax`, which
writes `+0x28` through **`+0x2F`** — six bytes past the last named field (`+0x29`). That is not an
overrun, because the caller reserves the space:

```
003860BA  lea rcx, [rsp + 0x48]      ; the context
resolver stack slots in use: rsp+0x40, rsp+0x48, rsp+0x50, then nothing until rsp+0x78
                                                                              ^ 0x48 + 0x30
```

**The next thing on the resolver's stack begins exactly where the builder's last write ends.** So
`0x2A` is the extent of the *named fields* and `0x30` is the record: `+0x2A`–`+0x2F` is tail padding
that the builder zeroes as a side effect of storing the last two layer bytes with a qword.

> A reimplementation that allocates `0x2A` — which the title, §4 and the field map all invited —
> has the builder zero six bytes of whatever it put next.

### ⚠ The builder is not side-effect-free: it writes a global

```asm
00384862  mov rcx, rdi
0038486B  call 0x31b860
00384870  mov qword ptr [rip + 0x2b3a911], rax     ; -> 02EBF188
```

The resolved target-unit pointer is **cached in a global at `02EBF188`**. §2.1 describes the builder
purely as filling a stack record, and §6 says "the context is per resolution and lives on the stack;
nothing persists it" — true of the *context*, but the builder leaves this pointer behind. Anything
that reads `02EBF188` sees the last resolution's target.

**And `0031B860` is called twice with the same argument** — `00384862`/`0038486B` for the `+0x55`
byte, then `00384889`/`0038488C` for the presence test at `00384894`. Only the first result is
cached.

### With no source, every `has(id)` is false rather than unknown

`00384803 test r8, r8` / `je 0x38485a` skips the merge **and** the `+0x04` store, so a source-less
resolution leaves `+0x04` and all sixteen layer bytes at the zeroes from the prologue. Not a defect —
worth stating, because "the source has no statuses" and "there is no source" are indistinguishable to
every slot.

### Two bookkeeping corrections to §2.2's columns

- **The `w / r` column counts distinct *functions*, not sites.** `+0x08` is read at **45** sites in
  **31** functions, `+0x10` at **76** sites in **34** functions, `+0x29` at **8** sites in **3**. The
  prose ("thirty-one slots read it") is right; the column header reads as a site count and is not.
- **It counts an `rw` as a write at `+0x1B` but not at `+0x08`.** `+0x1B` has **no** pure write in
  the TSV — both builder touches are `and byte ptr [rbx + 0x1b], 0x7f`, read-modify-writes — yet the
  row says `1 / 15`; `+0x08` has two pure writes and two `and` masks and the row also says `1`. One
  convention or the other, not both.
- **The `width` column mixes field width with widest access.** `+0x20` was given `8`, which is the
  zeroing qword; the only read is `movzx ecx, byte ptr [r8 + 0x20]`. `+0x00` is given `2` although it
  too is zeroed as a qword. Corrected `+0x20` to `1`.

**Not claimed:** §2.3's id-to-name mapping and the twenty-two per-slot test sites were not
re-derived — this pass checked the record, not the slot table. `FQ-2` is untouched. Nothing was
executed or observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

`BattleStats_FindOwningBattleUnit` (`0031B860`) is a shared owner lookup. Its other callers are:

- the three equipment-slot setters and `BattleStats_SetLicenseNodeStateAndApplySideEffects` (**Items_Equipment_Shops_License**);
- the level-up path and `Reward_ComputeExperienceForRecipient` (**Rewards_Progression_Economy**);
- two locomotion bodies, of 89 and 706 bytes (**Movement**).

Each of them is a **CLIENT** that finds a stats record's unit, and none of them bears on this page's formula.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **ActorEntity — SERVICE.** A cited function calls `BattleUnit_GetBySlotIndex` and `BattleUnit_GetSlotCount`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**RNG_Random_Selection — SERVICE.** `003851F0` on this page calls `RNG_MT19937_NextU32_Thunk`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00863BF0` - onto the CRT's Mersenne Twister next-u32; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

`00384C30` (542 B) is the twin-bank row resolver the evaluation context runs for field `si`: both `02EBF138` and `02EBF0F8` hold headers whose `+8` word is the row stride and whose `+C` offset resolves through `0020E600` into the row array, indexed as `base + index*stride`; a set `+8` byte on the `02EBF138` row short-circuits to that row's `+0x18`, otherwise the `02EBF0F8` bank's `+4` base count shifted by `0x1000` gates range tests on the record's `[rdi+0x50]`/`[+0x52]` words, rows whose `+0x11` byte lies inside `0x17..0x1A` yield `[row+0x20]`, and the fallback returns `[row+0x18]` or 0.

Interior anchor `00384D6B` (function `00384C30`).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Status_Periodic_Terminal — CLIENT (6 edges).** `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` (`002F9400`), `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`), `BattleStats_RemoveStatusesFromMaskAndRecompute` (`0030F690`), `BattleStats_RecomputeDerivedStateAndAutoStatuses` (`0030FED0`) and `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` (`00386860`) call the shared owner lookup `BattleStats_FindOwningBattleUnit` (`0031B860`), and `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`) calls `BattleFormula_ResolveTargetResult` (`00385F60`). The status bodies are further clients of the owner lookup the context uses for `+0x55`, and the periodic tick runs the resolver that builds this evaluation context, so a periodic result is evaluated with the same context an attack gets.
