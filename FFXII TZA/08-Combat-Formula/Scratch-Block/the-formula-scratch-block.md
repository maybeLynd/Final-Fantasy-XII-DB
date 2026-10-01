---
system: The formula scratch block — 44 globals at 02AEDFB8–02AEE05F that every calculator slot writes and the resolver reads back
category: 08-Combat-Formula
status: AUDITED
owner_layer: PrimaryOwner:CombatFormula
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every rip-relative reference into 02AEDFB8–02AEE05F across .text (912 instructions), the reset
    function read whole, the resolver's copy-out read whole, the outcome roller, the preview evaluator and the
    two per-unit-record mirrors read at every cited site; the census is published beside this page
corpus_validated: "the block's extent from BattleFormula_ResetScratchState's 42 stores"
last_reviewed: 2026-09-11
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-formula-scratch-block-pass-1
  last_pass_kind: authored
  crossref_clean: false
  reopened_count: 0
---

# The formula scratch block

> The combat formula does not pass numbers between its slots — it leaves them in **44 global
> words at `02AEDFB8`–`02AEE05F`**. A reset zeroes the flags and sets the numbers to `−1`; the
> calculator slots write chances, rolls and magnitudes into them; the resolver reads them back into
> the result record, turning every `−1` into "absent" and every non-`−1` into a flag bit. This page
> is the map of those words, the outcome roller that decides hit / miss through them, and the
> per-unit 64-byte record that carries three of their bits from the preview to the real resolution.

## 1. What the player sees

A swing that misses, is parried, is blocked, or lands and knocks the target back — and a combo
that stops on the first evaded hit. All of it is decided in these words before any damage number
exists.

## 2. Native mechanism

### 2.1 Extent and reset

`BattleFormula_ResetScratchState` (`003849B0`, 340 bytes, called at the start of every preview
`0038585E` and every resolution `00386001`) writes 42 stores over 43 of the 44: `0` into `02AEDFB8`–`02AEE000`
(`003849BC`–`00384A16`), `0xFFFFFFFF` into the seventeen number words `02AEE004`–`02AEE048`
(`003849B2`, `00384A3B`–`00384AF9`), `0` into the steal bytes and the three attack-defense words
(`00384A1C`–`00384A35`). **`02AEDFD4` — the action id — is the one word it does not touch.**

> **What a census like this cannot see (2026-09-11, OPUS-NOTICE-CENSUSWRITES).** This census is different in kind — every rip-relative reference in .text, writers included — but it cannot see a word reached through a pointer to the block (none is known).
> A scan seeded on *accessors* reaches *consumers*: a constructor that builds the record before
> any accessor can return it is reached only if it is seeded on its own. So the **reads** below are
> the well-covered side and the **writes** are under-covered wherever a constructor or an
> index-derived writer sits outside the seeds — do not rest an absence-of-writer claim on this
> TSV alone; pair it with a displacement scan of the candidate writers.

### 2.2 The words

| word | reset | w / r | what it holds | writers | readers |
|---|---|---|---|---|---|
| `02AEDFB8` | 0 | 53 / 24 | **roll over** — the calculator-slot loop stops when this reads 1 (preview `00385A07`; resolver `003863D7`); every deciding slot sets it (the roller `0038971B` / `00389745` / `003897E3`, the steal `00390584`, …); the resolver re-derives it at `0038625E`–`00386278` | `BattleFormula_ResetScratchState` `003849B0` (`003849BC`); `BattleFormula_ResolveTargetResult` `00385F60` (`00386278` +1); `BattleFormula_ResolveCandidateStatusApplications` `00387CB0` (`00387F0D`); +41 more | `BattleFormula_EvaluateTargetPreview` `00385680` (`003859AC` +1); `BattleFormula_ResolveTargetResult` `00385F60` (`0038625E` +2); `00388250` (`00388288` +4); +5 more |
| `02AEDFBC` | 0 | 41 / 2 | **failed** — read once into result kind `6` (`003866C1`–`003866CA`); the miss path of the roller (`003897D9`) and 39 other refusals | `BattleFormula_ResetScratchState` `003849B0` (`003849C2`); `BattleFormula_ResolveTargetResult` `00385F60` (`0038629B`); `BattleFormula_ResolveCandidateStatusApplications` `00387CB0` (`00387EF5`); +36 more | `BattleFormula_EvaluateTargetPreview` `00385680` (`00385A3A`); `BattleFormula_ResolveTargetResult` `00385F60` (`003866C1`) |
| `02AEDFC0` | 0 | 7 / 2 | **immune by kind** — read once into result kind `0xA` (`003866CE`–`003866D7`); the preview also sets bit *targetIndex* of the per-unit record's `+8` (`00385A82`–`00385AC0`, §2.5) | `BattleFormula_ResetScratchState` `003849B0` (`003849C8`); `BattleFormula_ResolveCandidateStatusApplications` `00387CB0` (`00387F03`); `00387F40` (`00387F4C`); +4 more | `BattleFormula_EvaluateTargetPreview` `00385680` (`00385A82`); `BattleFormula_ResolveTargetResult` `00385F60` (`003866CE`) |
| `02AEDFC4` | 0 | 3 / 3 | **parry rolled** — `BattleFormula_RollGuardParryMode` `003884F0`: `draw % 100 < [02AEDFDC]` when the target's flags have bit 23 (`00388537`); read by the roller to pick kind 4 over 3 and 2 over 1 (`0038970A`, `00389779`) and by the preview into flag word B bit 2 (`00385A21`–`00385A2D`); an accepted combo clears it (`003888A1`) | `BattleFormula_ResetScratchState` `003849B0` (`003849CE`); `BattleFormula_RollGuardParryMode` `003884F0` (`00388537`); `BattleFormula_RollAndStoreComboCount` `00388660` (`003888A1`) | `BattleFormula_EvaluateTargetPreview` `00385680` (`00385A21`); `BattleFormula_RollAvoidGuardParryOutcome` `003896B0` (`0038970A` +1) |
| `02AEDFC8` | 0 | 3 / 8 | **knockback rolled** — `BattleFormula_RollKnockback` `00388440` against `[02AEDFD8]` (`0038846E`–`0038847E`); the roller copies it into flag word B bit 3 (`00389734`–`00389741`, `003897F8`–`00389805`); an accepted combo clears it (`003888AB`) | `BattleFormula_ResetScratchState` `003849B0` (`003849D4`); `BattleFormula_RollKnockback` `00388440` (`0038847E`); `BattleFormula_RollAndStoreComboCount` `00388660` (`003888AB`) | `BattleFormula_RollKnockback` `00388440` (`0038846E`); `BattleFormula_RollAvoidGuardParryOutcome` `003896B0` (`00389734` +1); `00389820` (`00389882` +1); +2 more |
| `02AEDFCC` | 0 | 3 / 4 | element affinity, first word — `BattleFormula_ApplyActionElementAffinity` `0038B6A0` / `BattleFormula_ApplyEquipmentElementAffinity` `0038BE30` write, `BattleFormula_FinalizeTargetHpMagnitude` `0038D280` reads | `BattleFormula_ResetScratchState` `003849B0` (`003849DA`); `BattleFormula_ApplyActionElementAffinity` `0038B6A0` (`0038B717`); `BattleFormula_ApplyEquipmentElementAffinity` `0038BE30` (`0038C016`) | `BattleFormula_FinalizeTargetHpMagnitude` `0038D280` (`0038D2A3`); `0038D6B0` (`0038D6B0`); `0038DB50` (`0038DBA1`); +1 more |
| `02AEDFD0` | 0 | 3 / 6 | element affinity, second word — same writers; read back by them and by the finaliser | `BattleFormula_ResetScratchState` `003849B0` (`003849E0`); `BattleFormula_ApplyActionElementAffinity` `0038B6A0` (`0038B8D1`); `BattleFormula_ApplyEquipmentElementAffinity` `0038BE30` (`0038C75F`) | `BattleFormula_ApplyActionElementAffinity` `0038B6A0` (`0038B8C8`); `BattleFormula_ApplyEquipmentElementAffinity` `0038BE30` (`0038C756`); `BattleFormula_FinalizeTargetHpMagnitude` `0038D280` (`0038D2CC`); +3 more |
| `02AEDFD4` | — | 4 / 106 | **the action id under evaluation** — not reset; the preview (`003857EC`) and the resolver (`00385FE4`) store it; **id `0x9F` is a placeholder for a random draw** — replaced by the source's 64-byte record `+0x10` (`003857F3`–`00385806`, `00385FEA`–`00385FFB`), which `BattleRuntime_ResolveAndCacheEffectiveActionId` `00387A50` fills once per commit from `00387130` (§2.5); 106 reads, the most-read word | `BattleFormula_EvaluateTargetPreview` `00385680` (`003857EC` +1); `BattleFormula_ResolveTargetResult` `00385F60` (`00385FE4` +1) | `00384F40` (`0038502D`); `BattleFormula_EvaluateTargetPreview` `00385680` (`0038583C` +1); `BattleFormula_ApplyResultMetadata` `00385BA0` (`00385C75`); +51 more |
| `02AEDFD8` | 0 | 3 / 1 | **knockback chance** — `BattleFormula_ComputeKnockbackChance` `00388350` (`00388430`); consumed by `RollKnockback` (`00388474`) | `BattleFormula_ResetScratchState` `003849B0` (`003849E6`); `BattleFormula_ComputeKnockbackChance` `00388350` (`00388430`); `00388B50` (`00388BFB`) | `BattleFormula_RollKnockback` `00388440` (`00388474`) |
| `02AEDFDC` | 0 | 4 / 1 | **parry chance** — `BattleFormula_ComputeParryChanceFromSpeed` `00388490` (`003884CB`); consumed by `RollGuardParryMode` (`0038852D`) | `BattleFormula_ResetScratchState` `003849B0` (`003849EC`); `BattleFormula_ComputeParryChanceFromSpeed` `00388490` (`003884CB` +2) | `BattleFormula_RollGuardParryMode` `003884F0` (`0038852D`) |
| `02AEDFE0` | 0 | 22 / 29 | **hit chance** — the action row's byte `+0x12` (`BattleFormula_LoadHitAvoidGuardThresholds` `00389040` at `0038908D`) or a recipe family's own number (22 writers in all); the roller's modulus and its final percentage (`003896E3`, `003897D0`) | `BattleFormula_ResetScratchState` `003849B0` (`003849F2`); `BattleFormula_RollSpecialGuardOutcome` `00387FD0` (`0038806C`); `00388E80` (`00388F0C`); +14 more | `BattleFormula_RollSpecialGuardOutcome` `00387FD0` (`00388206` +1); `003891F0` (`003891FA`); `00389230` (`00389238`); +12 more |
| `02AEDFE4` | 0 | 2 / 1 | **combo chance** — `BattleFormula_ComputeComboChance` `00388550` (`00388648`) → `RollAndStoreComboCount` (`00388716`) | `BattleFormula_ResetScratchState` `003849B0` (`003849F8`); `BattleFormula_ComputeComboChance` `00388550` (`00388648`) | `BattleFormula_RollAndStoreComboCount` `00388660` (`00388716`) |
| `02AEDFE8` | 0 | 5 / 2 | **percent gate** — `0038F970` / `0038F9D0` write; `BattleFormula_RollPercentGateAndMarkResolved` `0038FB80` and `…SetResultFlag1000` `0038FBC0` roll against it | `BattleFormula_ResetScratchState` `003849B0` (`003849FE`); `0038F970` (`0038F9B4` +1); `0038F9D0` (`0038FB48` +1) | `BattleFormula_RollPercentGateAndMarkResolved` `0038FB80` (`0038FBA8`); `BattleFormula_RollPercentGateAndSetResultFlag1000` `0038FBC0` (`0038FBE2`) |
| `02AEDFEC` | 0 | 8 / 6 | **outcome band C threshold** — stats `+0x31` (`003890AB`); the roller's third band → kind 5 (`003897A5`) | `BattleFormula_ResetScratchState` `003849B0` (`00384A04`); `00388FB0` (`00388FC8`); `BattleFormula_LoadHitAvoidGuardThresholds` `00389040` (`003890AB`); +3 more | `00389310` (`00389341`); `00389370` (`0038939D` +2); `BattleFormula_RollAvoidGuardParryOutcome` `003896B0` (`003897A5`); +1 more |
| `02AEDFF0` | 0 | 20 / 8 | **outcome band A threshold** — stats `+0x33` (`00389097`); the roller's first band → kinds 3 / 4 (`00389702`); `RollSpecialGuardOutcome` `00387FD0` rewrites it seven times | `BattleFormula_ResetScratchState` `003849B0` (`00384A0A`); `BattleFormula_RollSpecialGuardOutcome` `00387FD0` (`00388080` +6); `00388FB0` (`00388FB4`); +4 more | `BattleFormula_RollSpecialGuardOutcome` `00387FD0` (`003881F3` +1); `00389370` (`003893C7` +2); `BattleFormula_RollAvoidGuardParryOutcome` `003896B0` (`00389702`); +2 more |
| `02AEDFF4` | 0 | 8 / 4 | **outcome band B threshold** — stats `+0x32` (`003890A1`); the roller's second band → kinds 1 / 2 (`00389771`) | `BattleFormula_ResetScratchState` `003849B0` (`00384A10`); `00388FB0` (`00388FBE`); `BattleFormula_LoadHitAvoidGuardThresholds` `00389040` (`003890A1`); +3 more | `00389370` (`00389587`); `BattleFormula_RollAvoidGuardParryOutcome` `003896B0` (`00389771`); `00389820` (`003898BF`); +1 more |
| `02AEDFF8` | 0 | 7 / 1 | resolver-private — read `00386621` (`−1` → 0, `00386630`), the **subtrahend of result `+0x1D`**; written back normalised `00386645` (§2.7); **the charge-count loss** — calculator slot 129 `0038E080` writes it five times: `0` when it refills, the target's charges `+0x4E` when it drains (§7 `FT-4`) | `BattleFormula_ResetScratchState` `003849B0` (`00384A59`); `BattleFormula_ResolveTargetResult` `00385F60` (`00386645`); `0038E080` (`0038E11C` +4) | `BattleFormula_ResolveTargetResult` `00385F60` (`00386621`) |
| `02AEDFFC` | 0 | 7 / 1 | resolver-private — read `0038660E` (`−1` → 0), the **minuend of result `+0x1D`**; written back normalised `0038662A` (§2.7); **the charge-count gain** — slot 129 `0038E080` five times: MP bars `+0x37` − charges `+0x4E` when it refills, `0` when it drains (§7 `FT-4`) | `BattleFormula_ResetScratchState` `003849B0` (`00384A63`); `BattleFormula_ResolveTargetResult` `00385F60` (`0038662A`); `0038E080` (`0038E127` +4) | `BattleFormula_ResolveTargetResult` `00385F60` (`0038660E`) |
| `02AEE000` | 0 | 1 / 1 | read once (`00386542`): forces flag word A bit 12 with the target-MP words — **never non-zero in the static image**: the reset's `0` is its only writer, so the force is dead (§7 `FT-4`) | `BattleFormula_ResetScratchState` `003849B0` (`00384A16`) | `BattleFormula_ResolveTargetResult` `00385F60` (`00386542`) |
| `02AEE004` | −1 | 66 / 12 | **target HP loss** (subtracted; §2.7) — the damage pipeline's output (`0038CB00` … 28 writers; the attack-defense page); resolver `0038646D`: A bits 6 / 8 / 18 | `BattleFormula_ResetScratchState` `003849B0` (`003849B2`); `BattleFormula_ResolveTargetResult` `00385F60` (`003865E5`); `0038CB00` (`0038CB3C` +2); +26 more | `BattleFormula_ComputeKnockbackImpulseScale` `00385E50` (`00385F13`); `BattleFormula_ResolveTargetResult` `00385F60` (`0038646D`); `0038CB00` (`0038CBDC`); +6 more |
| `02AEE008` | −1 | 45 / 8 | **target HP gain** (added; §2.7) — 20 writers, `FinalizeTargetHpMagnitude` reads it (`0038D324`); resolver `00386467`: A bits 6 / 8 / 10 | `BattleFormula_ResetScratchState` `003849B0` (`00384A3B`); `BattleFormula_ResolveTargetResult` `00385F60` (`003865AB`); `0038CB00` (`0038CBE2`); +17 more | `BattleFormula_ResolveTargetResult` `00385F60` (`00386467`); `BattleFormula_FinalizeTargetHpMagnitude` `0038D280` (`0038D324`); `0038D400` (`0038D4A1` +2); +3 more |
| `02AEE00C` | −1 | 6 / 2 | **target MP loss** (subtracted; §2.7) — resolver `003864E8`: A bits 12 / 14 | `BattleFormula_ResetScratchState` `003849B0` (`00384A45`); `BattleFormula_ResolveTargetResult` `00385F60` (`003865FF`); `0038CE40` (`0038CF0F`); +3 more | `BattleFormula_ResolveTargetResult` `00385F60` (`003864E8` +1) |
| `02AEE010` | −1 | 8 / 2 | **target MP gain** (added; §2.7) — resolver `003864DA`: A bits 12 / 14 / 16 | `BattleFormula_ResetScratchState` `003849B0` (`00384A4F`); `BattleFormula_ResolveTargetResult` `00385F60` (`003865C8`); `0038D000` (`0038D0CF`); +3 more | `BattleFormula_ResolveTargetResult` `00385F60` (`003864DA`); `0038DF00` (`0038E047`) |
| `02AEE014` | −1 | 15 / 6 | **source HP loss** (subtracted; §2.7) — resolver `00386446`: A bits 5 / 7 | `BattleFormula_ResetScratchState` `003849B0` (`00384A6D`); `BattleFormula_ResolveTargetResult` `00385F60` (`003865F2`); `0038CB00` (`0038CB5E`); +5 more | `BattleFormula_ResolveTargetResult` `00385F60` (`00386446`); `0038CB00` (`0038CBA8`); `0038D400` (`0038D4AD` +2); +1 more |
| `02AEE018` | −1 | 14 / 3 | **source HP gain** (added; §2.7) — resolver `0038643F`: A bits 5 / 7 / 9 | `BattleFormula_ResetScratchState` `003849B0` (`00384A77`); `BattleFormula_ResolveTargetResult` `00385F60` (`003865B9`); `0038D400` (`0038D46B` +7); +3 more | `BattleFormula_ResolveTargetResult` `00385F60` (`0038643F`); `0038D400` (`0038D4DF` +1) |
| `02AEE01C` | −1 | 2 / 1 | **source MP loss** (subtracted; §2.7) — resolver `00386453`: A bits 11 / 13 | `BattleFormula_ResetScratchState` `003849B0` (`00384A81`); `BattleFormula_ResolveTargetResult` `00385F60` (`00386617`) | `BattleFormula_ResolveTargetResult` `00385F60` (`00386453`) |
| `02AEE020` | −1 | 3 / 1 | **source MP gain** (added; §2.7) — resolver `0038644C`: A bits 11 / 13 / 15 | `BattleFormula_ResetScratchState` `003849B0` (`00384A8B`); `BattleFormula_ResolveTargetResult` `00385F60` (`003865D7`); `0038D630` (`0038D65E`) | `BattleFormula_ResolveTargetResult` `00385F60` (`0038644C`) |
| `02AEE024` | −1 | 2 / 1 | **source HP absolute** (overrides the difference into result `+0x20`, A bit 1 set / 5 cleared, `0038667D`–`0038668E`; §2.7) — resolver `0038645A`: A bit 7 | `BattleFormula_ResetScratchState` `003849B0` (`00384A95`); `BattleFormula_ResolveTargetResult` `00385F60` (`00386424`) | `BattleFormula_ResolveTargetResult` `00385F60` (`0038645A`) |
| `02AEE028` | −1 | 4 / 1 | **source MP absolute** (overrides into result `+0x28`, A bit 2 set / 11 cleared, `003866A9`–`003866BE`; §2.7) — resolver `00386460`: A bit 13; `0038F800` writes it | `BattleFormula_ResetScratchState` `003849B0` (`00384A9F`); `BattleFormula_ResolveTargetResult` `00385F60` (`0038641D`); `0038F800` (`0038F85B` +1) | `BattleFormula_ResolveTargetResult` `00385F60` (`00386460`) |
| `02AEE02C` | −1 | 40 / 2 | **target HP absolute** (overrides into result `+0x24`, A bit 3 set / 6 cleared, `00386669`–`0038667A`; §2.7) — zeroed (an outright kill, with A bit 19) by slot 162 `0038F630` (`0038F64D`) and recipe 9's slot 190 `00390170` (`00390174`, actions `0x32` / `0x89` / `0xC2`); written 40 times by `BattleFormula_ResolveCandidateStatusApplications` `00387CB0` and `00387F70`; counted with the target-HP words for A bit 8 (`0038647E`) and read again at `0038664B` (`FT-4`) | `BattleFormula_ResetScratchState` `003849B0` (`00384AA9`); `BattleFormula_ResolveCandidateStatusApplications` `00387CB0` (`00387E93`); `00387F70` (`00387FA5` +1); +17 more | `BattleFormula_ResolveTargetResult` `00385F60` (`0038647E` +1) |
| `02AEE030` | −1 | 19 / 1 | **target MP absolute** (overrides into result `+0x2A`, A bit 4 set / 12 cleared, `00386691`–`003866A6`; §2.7) — `0038E080` writes it nine times, `00389BE0` once; counted with the target-MP words for A bit 14 (`003864E1`) (`FT-4`) | `BattleFormula_ResetScratchState` `003849B0` (`00384AB3`); `00389BE0` (`00389C29`); `0038E080` (`0038E0B5` +8); +4 more | `BattleFormula_ResolveTargetResult` `00385F60` (`003864E1`) |
| `02AEE034` | −1 | 3 / 2 | **strength modifier** — `BattleFormula_ReduceStrengthTo70Percent` `0038E870` / `BattleFormula_BoostStrengthByActionPercent` `0038EE40`; resolver `00386571` (A bit 18), `0038679F` → result `+0x11E` (foe stat delta 0) | `BattleFormula_ResetScratchState` `003849B0` (`00384AD1`); `BattleFormula_ReduceStrengthTo70Percent` `0038E870` (`0038E89A`); `BattleFormula_BoostStrengthByActionPercent` `0038EE40` (`0038EEBC`) | `BattleFormula_ResolveTargetResult` `00385F60` (`00386571` +1) |
| `02AEE038` | −1 | 3 / 2 | **magick power modifier** — `…ReduceMagickPowerTo70Percent` `0038E8B0` / `…BoostMagickPowerByActionPercent` `0038EED0`; resolver `0038657A` (A bit 18), `003867AD` → result `+0x120` (delta 1) | `BattleFormula_ResetScratchState` `003849B0` (`00384ADB`); `BattleFormula_ReduceMagickPowerTo70Percent` `0038E8B0` (`0038E8DA`); `BattleFormula_BoostMagickPowerByActionPercent` `0038EED0` (`0038EF4C`) | `BattleFormula_ResolveTargetResult` `00385F60` (`0038657A` +1) |
| `02AEE03C` | −1 | 2 / 2 | **defense modifier** — `BattleFormula_ReduceDefenseTo90Percent` `0038E8F0`; resolver `00386583` (A bit 18), `003867BB` → result `+0x122` (delta 2) | `BattleFormula_ResetScratchState` `003849B0` (`00384AE5`); `BattleFormula_ReduceDefenseTo90Percent` `0038E8F0` (`0038E919`) | `BattleFormula_ResolveTargetResult` `00385F60` (`00386583` +1) |
| `02AEE040` | −1 | 2 / 2 | **magick resist modifier** — `BattleFormula_ReduceMagickResistTo90Percent` `0038E920`; resolver `0038658C` (A bit 18), `003867C9` → result `+0x124` (delta 3) | `BattleFormula_ResetScratchState` `003849B0` (`00384AEF`); `BattleFormula_ReduceMagickResistTo90Percent` `0038E920` (`0038E949`) | `BattleFormula_ResolveTargetResult` `00385F60` (`0038658C` +1) |
| `02AEE044` | −1 | 2 / 1 | **the target's new level** — recipe 87's slot 161 `0038F5B0` (actions `0x13F` "…'s level doubles", `0x161`): `min(99, level + level × row[+0x10] / 100)` from the target stats' `+0x1C2` (`0038F5F9`–`0038F620`); the resolver copies it to result `+0x11C` (`003867D7`), the applier hands it to `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0030C650`) | `BattleFormula_ResetScratchState` `003849B0` (`00384AC7`); `0038F5B0` (`0038F620`) | `BattleFormula_ResolveTargetResult` `00385F60` (`003867D7`) |
| `02AEE048` | −1 | 3 / 1 | **the source's new level** — recipe 88's slot 162 `0038F630` (action `0x144` "… feeds on …"): the same growth on the *source's* level (`0038F691`–`0038F6D4`), after zeroing the target's HP absolute `02AEE02C` (`0038F64D`) and setting A bit 19 (`0038F6DA`); the resolver copies it to result `+0x11D` (`003867E4`) | `BattleFormula_ResetScratchState` `003849B0` (`00384ABD`); `BattleFormula_ResolveTargetResult` `00385F60` (`00386430`); `0038F630` (`0038F6D4`) | `BattleFormula_ResolveTargetResult` `00385F60` (`003867E4`) |
| `02AEE04C` | 0 | 3 / 2 | **steal — common tier won** ([the steal roll](../Steal/the-steal-roll.md)); resolver `003867F1` → result `+0x32` | `BattleFormula_ResetScratchState` `003849B0` (`00384A23`); `00390390` (`0039055B` +1) | `BattleFormula_ResolveTargetResult` `00385F60` (`003867F1`); `00390390` (`00390563`) |
| `02AEE04D` | 0 | 3 / 3 | **steal — uncommon tier won**; resolver `003867FB` → result `+0x33` | `BattleFormula_ResetScratchState` `003849B0` (`00384A1C`); `00390390` (`00390527` +1) | `BattleFormula_ResolveTargetResult` `00385F60` (`003867FB`); `00390390` (`00390519` +1) |
| `02AEE04E` | (with 4D) | 2 / 3 | **steal — rare tier won**; resolver `00386805` → result `+0x34` | `00390390` (`003904EB` +1) | `BattleFormula_ResolveTargetResult` `00385F60` (`00386805`); `00390390` (`003904DD` +1) |
| `02AEE050` | 0 | 8 / 2 | **poach reward item** — `BattleFormula_SelectPoachRewardItem95_5` `00390680`; resolver `00386813` | `BattleFormula_ResetScratchState` `003849B0` (`00384AF9`); `BattleFormula_SelectPoachRewardItem95_5` `00390680` (`003906D9` +6) | `BattleFormula_ResolveTargetResult` `00385F60` (`00386813`); `BattleFormula_SelectPoachRewardItem95_5` `00390680` (`0039079D`) |
| `02AEE054` | 0 | 64 / 63 | **the multiplier** `((L + Stat) × Stat) / 256 + 1` ([attack vs defense](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md)); 64 writers, 63 readers | `BattleFormula_ResetScratchState` `003849B0` (`00384A29`); `00389DD0` (`00389E14`); `00389F80` (`00389FB8`); +27 more | `0038AF20` (`0038AF37`); `0038AF50` (`0038AF5A`); `0038AF90` (`0038AFA9` +1); +25 more |
| `02AEE058` | 0 | 17 / 14 | **attack + variance** (same page) | `BattleFormula_ResetScratchState` `003849B0` (`00384A2F`); `00389DD0` (`00389F60`); `00389F80` (`0038A0FD`); +13 more | `0038CB00` (`0038CB0F`); `0038D0E0` (`0038D0E0`); `BattleFormula_FinalizeTargetHpMagnitude` `0038D280` (`0038D280`); +8 more |
| `02AEE05C` | 0 | 15 / 10 | **the target's defensive stat** (same page) | `BattleFormula_ResetScratchState` `003849B0` (`00384A35`); `00389DD0` (`00389F6F`); `00389F80` (`0038A0E8`); +12 more | `0038CB00` (`0038CB1A`); `0038D0E0` (`0038D0EB`); `BattleFormula_FinalizeTargetHpMagnitude` `0038D280` (`0038D28B`); +4 more |

"w / r" counts instructions, not functions. The full listing is
[`formula-scratch-block-accesses.tsv`](formula-scratch-block-accesses.tsv). *Kind `rw` (2026-09-25, FABLE, Claude Opus 5.5, on OPUS's relabel request): the eight `add dword ptr [02AEDFF0], eax` read-modify-writes are labelled `rw` rather than `w`. They count in both columns, which is how `02AEDFF0`'s `20 / 8` above already counted them (§ "Eight reads that are also eight writes").*

### 2.3 The outcome roller, band by band

`BattleFormula_RollAvoidGuardParryOutcome` (`003896B0`) is the standard hit / miss decision. Its
second argument is the target's stats record (the preview passes `rdx = rsi`, its own `r8`,
`003859F9`); the **three evade bands run only when the target unit's flag bit 23 is set**
(`003896C0`–`003896DD`, else straight to the hit roll), each roll `mt19937 % [02AEDFE0]` (the hit
chance) unless the chance is zero:

| step | roll | against | outcome | kind written to result `+4` |
|---|---|---|---|---|
| band A — **block** | `003896F3`–`00389702` | `[02AEDFF0]` = stats `+0x33`, the **shield's evade** | evaded — with parry (`[02AEDFC4]`) → kind **4**, else kind **3** and flag word B bit 3 if `[02AEDFC8]` | `00389717`, `00389730`, `00389741` |
| band B — **parry** | `00389762`–`00389771` | `[02AEDFF4]` = stats `+0x32`, the **weapon's evade** | evaded — with parry → kind **2**, else kind **1** (+ bit 3 as above) | `00389786`, `0038978C` |
| band C — **innate evade** | `00389796`–`003897A5` | `[02AEDFEC]` = stats `+0x31`, the **record's own evade** | evaded → kind **5** | `003897B1` |
| the hit | `003897B7`–`003897D0` | `[02AEDFE0]` vs `mt19937 % 100` | chance ≤ roll → **miss**: `02AEDFBC = 1`, `02AEDFB8 = 1` (`003897D9`, `003897E3`); else hit, flag word B bit 3 if `[02AEDFC8]` (`003897F8`–`00389805`) | — (kind stays 0; the resolver makes `6` of the miss at `003866CA`) |

Every decided outcome sets `02AEDFB8 = 1` — the slot loop ends. The three band thresholds are the
target's stats `+0x31` / `+0x32` / `+0x33`, three percentages the stats rebuild clamps to
`[0, 100]` (`002FF936`, `002FF949`, `002FF95B`). **Their sources (read 2026-09-11, `FT-1`):** band A
is the **shield's evade** — every equipped item of kind 2 adds its row byte `+0x18` (`002FF477`–
`002FF483`) — so the first roll is a *block*; band B is the **weapon's evade** — kind 1 adds row byte
`+0x1D` (`002FF48E`–`002FF4A4`) — a *parry*; band C is the **record's own evade** — the party
definition's byte `+0x2A` (`002FF095`–`002FF09F`) or, for area units, the `.ard` growth / base
column `+0x2A` (`002FF2A1`–`002FF2B4`). Area units take their block and parry from `.ard` columns
`+0x02` and `+0x2E` instead of equipment when the definition's byte `+0x15` has bit 1 / bit 0
(`002FF325`–`002FF3C0`), and add the stats record's own modifier words (`+0x1A`, `+0x18`,
`+0x16`; party records do not). The roller's order is therefore **block, then parry, then innate evade, then the hit
roll**; the shield's magick evade (row `+0x19`) goes to stats `+0x34` and is not one of these bands. `RollSpecialGuardOutcome`
(`00387FD0`) is the variant that writes kind `0xB` (`0038823B`).

### 2.4 Flag word B, bit by bit — and where the bits go

Result `+0x18` ([the result record](../../07-Combat-Action/Result-Record/the-result-record-field-map.md)):

| bit | set by | meaning |
|---|---|---|
| 0 | `BattleFormula_RollPrimaryFormulaResourceReactionMode2Chance` `00389140` (`003891D9`) | the mode-2 resource reaction chance rolled true |
| 1 | `BattleFormula_RollAndStoreComboCount` `00388660`: cleared `003886F1`, set `0038887A` when the combo's progress is below the stored count | **the combo continues** |
| 2 | the preview, from `[02AEDFC4]` (`00385A1C`–`00385A2D`); `ResolveCandidateStatusApplications` clears it when status 13 lands (`00387E89`) | **parry rolled** |
| 3 | the roller, from `[02AEDFC8]` (`00389741`, `00389805`) | **knockback rolled** — the knockback scale reads it (`0038680F`) |

The bits travel: `Battle_ProcessActionTarget` `00307300` copies bits 3 / 1 / 2 into the target
buffer entry's outcome bits **8 / 10 / 9** (`003075CB`, `003075E0`, `003075EC`; [the unit map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)
§2.4), bit 10 withheld when the target unit's `+0x4` has bit 21 (`003075D7`). Entry bit 10 is what
`BattleUnit_UpdateCombatFrame` tests before `BattleAction_TryContinueComboSequence` `0030FA00` (`00308790`,
`0030C045`) — **a combo continues only on a hit that rolled to continue** — and entry bit 8 is the
one the HP event reads to turn `0x2005` into `0x2006` and `0x2008` into `0x2007`
(`0030071A`–`00300726`; [the HP write](../Current-HP/the-hp-write-and-the-lethal-transition.md))
— **the knockback variant of the hit and death events.**

### 2.5 The per-unit 64-byte record: the preview's memo

`0208D480 + kind × 0x40` (party, by stats `+4`) or `0208DE80 + unit[0xEA9] × 0x40` (everyone else)
— the tables [the handler page](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md)
found the reset for. The record is the **source's** (chosen from the source stats' `+5` / `+4`,
`003856D3`–`003856EB`). `BattleFormula_EvaluateTargetPreview` (`00385680`: `cx` the action id,
`rdx` the source stats, `r8` the target stats, `r9` a stack result — `0038569D`–`003856A8`; run
from the target-preview walk before the action executes) leaves these in it, and the real
resolution reads them back:

| field | preview writes | resolver / others read |
|---|---|---|
| `+0x00` ~~u64~~ u32 (only the clears are qword) | zeroed (`003857AB`); `0038DA00` later parks block echo C here when bit 0 is set (`0038DA49`–`0038DA61`) | ~~—~~ the recipes that parked it: `00388E60` (the gil throw), `0038DA68` (echo C), `0038ED17` (the walk), `0038EDD6` (the gil throw's payout, divided by the target count) *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr8-unit-record-64-0930`](../../_index/candidates/gr8-unit-record-64-0930/README.md); record [`gr8-page-corrections-fable-0930`](../../_index/candidates/gr8-page-corrections-fable-0930/README.md))* |
| `+0x04` u32 | bit *targetIndex* set when the preview failed on that target (`[02AEDFBC]`, `00385A3A`–`00385A7F`) | ~~—~~ the resolver `00385F60`: `0038633F` loads it for a `bt`, and a set bit stores result kind 6, miss / failed (`00386347`) *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr8-unit-record-64-0930`](../../_index/candidates/gr8-unit-record-64-0930/README.md); record [`gr8-page-corrections-fable-0930`](../../_index/candidates/gr8-page-corrections-fable-0930/README.md))* |
| `+0x08` u32 | bit *targetIndex* set when the target was immune by kind (`[02AEDFC0]`, `00385A82`–`00385AC0`) | ~~—~~ the resolver `00385F60`: `003862FB` loads it for a `bt`, and a set bit stores result kind `0xA` (`00386303`) *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr8-unit-record-64-0930`](../../_index/candidates/gr8-unit-record-64-0930/README.md); record [`gr8-page-corrections-fable-0930`](../../_index/candidates/gr8-page-corrections-fable-0930/README.md))* |
| `+0x10` u16 | ~~**the previewed action id** (`003857E1`)~~ **not the previewed id**: the preview saves the word (`003857A3`), clears `+0x10`..`+0x13` (`003857B2`) and writes the saved word back (`003857E1`); the previewed id goes to `02AEDFD4` (`003857EC`) *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr8-unit-record-64-0930`](../../_index/candidates/gr8-unit-record-64-0930/README.md); record [`gr8-page-corrections-fable-0930`](../../_index/candidates/gr8-page-corrections-fable-0930/README.md))*. Only for id `0x9F` is an id stored here: **the random draw** `BattleRuntime_ResolveAndCacheEffectiveActionId` `00387A50` caches here (`00387ADE`) | replaces id `0x9F` (`00385FF7`); `BattleRuntime_GetEffectiveActionId` `00387090` returns it in place of `0x9F` (`00387100`–`0038710E`) |
| `+0x12` bit 0 | **a preview is stored** (`003857DD`) | cleared by the resolver (`00386402`); tested by `00389D24`, `0038DA49` |
| `+0x12` bits 1–3 | **flag word B bits 1–3 of the previewed result** (`00385AC3`–`00385AF2`) | the resolver copies them into the real result's `+0x18` (`003860DF`–`00386108`) |
| `+0x12` bits 4–7 | the combo count ([combos](../combos-and-the-guard-parry-flag.md)) | `RollAndStoreComboCount` (`0038886B`) |
| `+0x0C` u32 | not the preview: `00387B00` sets bit *n* for a marked target (`00387B97` `or dword ptr [rbx + 0xc], eax`; 15 direct call sites); cleared at each preview (`003857AE`, qword) and at activation (`00386C5E`) | `002FA290` (`002FA352`, `bt`): a per-source set of marked targets that lasts one action *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr8-unit-record-64-0930`](../../_index/candidates/gr8-unit-record-64-0930/README.md); record [`gr8-page-corrections-fable-0930`](../../_index/candidates/gr8-page-corrections-fable-0930/README.md))* |
| `+0x14` u16 | not the preview: the periodic HP-credit tick counter, written by `00386860` (`003869E0`, `00386A27` `inc`, `00386A2C`) through its `0208D494` / `0208DE94` anchors (`00386885`, `003868AD`) | `00386860` (`003869A2`) *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr8-unit-record-64-0930`](../../_index/candidates/gr8-unit-record-64-0930/README.md); record [`gr8-page-corrections-fable-0930`](../../_index/candidates/gr8-page-corrections-fable-0930/README.md))* |
| `+0x18` f32 | not the preview: the walking-MP carry, written by `002F9400` (`002F95A6`); cleared at activation (`00386C66`) | `002F9400` (`002F9474`) *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr8-unit-record-64-0930`](../../_index/candidates/gr8-unit-record-64-0930/README.md); record [`gr8-page-corrections-fable-0930`](../../_index/candidates/gr8-page-corrections-fable-0930/README.md))* |
| `+0x1C` u32 | not the preview: movement flags. Bit 0 is set by `0033CB10` (`0033CB60` `or dword ptr [rax + 0x1c], 1`); bit 1 is the kind-2 solver's own latch (`0033DA73` `or dword ptr [rbx + 0x1c], 2`); both clear only at activation (`00386C66`) | the solver `0033D890`: bit 0 at `0033D953`, bit 1 at `0033DA77` *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr8-unit-record-64-0930`](../../_index/candidates/gr8-unit-record-64-0930/README.md); record [`gr8-page-corrections-fable-0930`](../../_index/candidates/gr8-page-corrections-fable-0930/README.md))* |
| `+0x20`..`+0x3F` | **nothing**: the activation reset `BattleRuntime_ResetPersistentStatePrefix` `00386C10` clears exactly `+0x00`..`+0x1F` with four qword stores (`00386C5B`-`00386C66`), and OPUS's GR-8 census finds no access past `+0x1F` | nothing: the record is 32 bytes of data in a `0x40` stride *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr8-unit-record-64-0930`](../../_index/candidates/gr8-unit-record-64-0930/README.md); record [`gr8-page-corrections-fable-0930`](../../_index/candidates/gr8-page-corrections-fable-0930/README.md))* |

So the parry and knockback outcomes are **rolled once, at preview, and replayed at resolution**
for the same action — the reason a live observer sees the miss decided before the swing.

**Action id `0x9F` is not an action but a draw.** `00387130` walks all `0x21F` rows of the action
table (registry slot `02EBF138`), counts the rows whose byte `+0x1E` is 1 and whose `+0x2C & 7` is
1 (`0038718C`–`003871DA`), and picks one uniformly (`mt19937 % count`, `003871E8`–`003871FA`) —
in the shipped `action_data.bin` that pool is **25 rows**: ids `0x12`–`0x21`, `0x23`, `0x39`, `0x3B`–`0x41`.
`ResolveAndCacheEffectiveActionId` (`00387A50`) stores the pick in the source's record `+0x10`
(`00387ADE`) when the committed id is `0x9F`; `GetEffectiveActionId` (`00387090`) and the two
formula entry points then read `+0x10` instead of `0x9F`, so preview and resolution agree on the
same draw. `BattleUnit_AdvanceStandardActionState` sets unit flag bit 35 when the committed id is
`0x9F` (`00304DA5`–`00304DBA`). What the 25 rows are in the game's words, and who commits `0x9F`,
is `FT-3`. *(2026-09-15: the rows are seventeen black-magick rows and eight status-magick rows, and `0x9F` is technick 1, "Shades of Black" — §7 `FT-3`.)*

### 2.6 From result kind to what the target shows

`BattleFormula_MapOutcomeToTargetEntryCode` (`0030DAE0`) turns result `+4` into the entry's code
byte, and `Battle_EmitReactionPresentationForSlot` (`003176E0`) turns the code into a unit event
(`0031778D`–`003177C8`; the inverse map is `BattleFormula_MapTargetEntryCodeToOutcome` `002FEE20`):

| result kind | meaning (§2.3) | entry code | reaction event |
|---|---|---|---|
| 0 | hit | 0 | — |
| 5 | band C evade | 1 | `0x2037` |
| 1 | band B evade | 2 | `0x2039` |
| 3 | band A evade | 3 | `0x203A` |
| 2 | band B evade, parry | 4 | `0x203B` |
| 4 | band A evade, parry | 5 | `0x203C` |
| 6 | miss / failed | 6 | — |
| 7, 8 | — | 7, 8 | — |
| `0xB` (special guard) | — | 10 | `0x203A` |
| `0xA` (immune by kind) | — | 9 | — |
| 9 | — | 11 | — |

What each `0x203x` event draws is `FT-2`.

### 2.7 The copy-out: loss, gain, absolute — and what the sentinel's destruction hides

Read whole 2026-09-11 against ASTRA's [EXP-059](../../_experiments/EXP-059-formula-copyout-controls.md)
(the 642-byte segment `0038643F`–`003866C0` of the resolver executed in isolation over thirteen
fixtures; no callee runs inside it). Every number word is read as a dword and `N(x)` means 0 when
`x == 0xFFFFFFFF`, else `x` unchanged — **only the exact `−1` is absent; an explicit 0 and `−2`
are present.** The four groups:

| result | = `N(gain) − N(loss)` | absolute override | width |
|---|---|---|---|
| target HP `+0x24` | `N(02AEE008) − N(02AEE004)` (`00386635`, `00386658`) | `02AEE02C` (`0038666E`; A bit 3 set, bit 6 cleared) | dword |
| source HP `+0x20` | `N(02AEE018) − N(02AEE014)` (`00386642`, `0038665B`) | `02AEE024` (`00386688`; bit 1 set, 5 cleared) | dword |
| target MP `+0x2A` | `low16(N(02AEE010) − N(02AEE00C))` (`00386638`, `0038665F`) | `02AEE030` (`0038669D`; bit 4 set, 12 cleared) | word |
| source MP `+0x28` | `low16(N(02AEE020) − N(02AEE01C))` (`00386651`, `00386664`) | `02AEE028` (`003866B5`; bit 2 set, 11 cleared) | word |

So a hit's damage is a *negative* `+0x24` (loss 100, gain 25 → `−75`), an absolute — present
even when zero or negative — replaces the difference outright, and MP keeps only its low 16 bits
(nothing rejects or saturates a wide input here). **Flag word A** is ORed from the *original*
inputs before any of this (`00386474`–`00386595`): per group, any of the three present → bits
8 / 7 / 14 / 13 (target HP / source HP / target MP / source MP), the gain present → 10 / 9 /
16 / 15, either difference input present → 6 / 5 / 12 / 11; `02AEE000` non-zero also forces
bit 12 (`00386542`) — it never is, see §7 `FT-4`; and **bit 18 is set only by the target-HP loss `02AEE004` or by any of the
four stat-modifier words `02AEE034`–`02AEE040`** (`00386564`–`00386595`) — not by the gain, not
by the source words. Existing bits survive: this segment neither resets A nor freshens a used
record. Then the eight difference words are **written back normalised** (`003865AB`–`00386617`):
an absent word is now 0, and a snapshot of the block after the copy-out can no longer tell
"absent" from "explicitly zero" — the presence bits in A are the only record of that. The two
private words `02AEDFFC` / `02AEDFF8` normalise the same way (`0038661E`, `00386630`; the
fallback for `02AEDFF8` is the resolver's `r12`, zeroed at `00385F7F` and parked in
`[rsp + 0x38]`, so it is 0) and their difference's low byte is result `+0x1D` (`00386640`,
`00386655`) — the multiplier the applier uses on the target's `+0x28` word (`003116A6`); what
feeds the two words is calculator slot 129 `0038E080` (five writes each), read under §7 `FT-4`. Not in this reading: the
suppression branch before `0038643F`, the failure kinds after `003866C1`, and what any authored
recipe puts into a given word. ASTRA's [EXP-062](../../_experiments/EXP-062-mp-composition.md)
then feeds this segment's *actual* output buffer into the applier's dispatch and the native MP
writers in one retained memory state (nine cases; a sign-extension mutant at `00311673` changes
the final MP): the three contracts agree at their boundaries under injected frame roles — the
intervening resolver and applier paths are skipped, so it is composition evidence, not a captured
action.

## 3. Key addresses

| address | name | role |
|---|---|---|
| `003849B0` | `BattleFormula_ResetScratchState` | the reset (§2.1) |
| `00385680` | `BattleFormula_EvaluateTargetPreview` | the preview: runs the slots into a stack result, memoises in the per-unit record |
| `00385F60` | `BattleFormula_ResolveTargetResult` | the resolution: the same slots, then the copy-out into the real result (`0038641D`–`00386813`) |
| `003896B0` | `BattleFormula_RollAvoidGuardParryOutcome` | the outcome roller (§2.3) |
| `00389040` | `BattleFormula_LoadHitAvoidGuardThresholds` | the four thresholds from the action row and stats `+0x31`–`+0x33` |
| `003884F0` / `00388440` | `RollGuardParryMode` / `RollKnockback` | the two pre-rolls |
| `0030DAE0` / `002FEE20` | the two code maps | §2.6 |
| `0208D480` / `0208DE80` | the per-unit 64-byte records | §2.5 |

## 4. Data structures and formulas

```
FormulaScratch (globals, 0xA8 B)
  02AEDFB8 u32 rollOver      02AEDFBC u32 failed        02AEDFC0 u32 immuneByKind
  02AEDFC4 u32 parryRolled   02AEDFC8 u32 knockbackRolled
  02AEDFCC/D0 u32 elementAffinity[2]     02AEDFD4 u32 actionId (not reset)
  02AEDFD8 u32 knockbackChance   02AEDFDC u32 parryChance   02AEDFE0 u32 hitChance
  02AEDFE4 u32 comboChance   02AEDFE8 u32 percentGate
  02AEDFEC/F0/F4 u32 bandC/A/B threshold (stats +0x31/+0x33/+0x32)
  02AEDFF8..02AEE000 u32[3] resolver-private
  02AEE004..02AEE030 i32[12] numbers, -1 = absent; each group is loss / gain / absolute:
                     target HP 004 / 008 / 02C, target MP 00C / 010 / 030,
                     source HP 014 / 018 / 024, source MP 01C / 020 / 028   (see 2.7)
  02AEE034..02AEE040 i32[4] stat modifiers     02AEE044/048 u8 (two bytes)
  02AEE04C/4D/4E u8 steal tiers   02AEE050 u32 poachItem
  02AEE054/58/5C f32 multiplier / attack / defense
PerUnitFormulaRecord (0x40 B, two tables)
  +0x00 u64 echoStash   +0x04 u32 failedTargetsMask   +0x08 u32 immuneTargetsMask   +0x10 u16 lastActionId
  +0x12 u8  bit0 previewStored | bits1-3 flagWordB[1..3] | bits4-7 comboCount
  (+0x14..+0x3F: the reset clears +0x00..+0x1F; nothing enumerated here touches the rest)
```

*In the block above, `+0x00` is a u32 (only the clears are qword), `+0x10` holds only the `0x9F` draw, not the last action id, and "nothing touches the rest" is true only of `+0x20`..`+0x3F`: `+0x0C`, `+0x14`, `+0x18` and `+0x1C` are used (§2.5)* *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr8-unit-record-64-0930`](../../_index/candidates/gr8-unit-record-64-0930/README.md); record [`gr8-page-corrections-fable-0930`](../../_index/candidates/gr8-page-corrections-fable-0930/README.md))*.

## 5. Call chain

```
preview:    Battle_BuildActionTargetSet 0030D160 -> BattleAction_EvaluateTargetPreviews 00303830
              -> BattleFormula_EvaluateTargetPreview 00385680 -> ResetScratchState -> slots -> record +0x12
resolution: Battle_ProcessActionTargetEntry 003191B0 -> Battle_ProcessActionTarget 00307300
              -> BattleFormula_ResolveTargetResult 00385F60 -> ResetScratchState -> slots
                 -> record +0x12 bits 1-3 -> result +0x18 -> copy-out 0038641D..00386813
              -> entry.outcome (code byte, bits 8-11) -> reaction event / combo gate / HP event variant
```

## 6. Modding notes

- **Change a chance, not a roll.** `02AEDFE0` (hit), `02AEDFDC` (parry), `02AEDFD8` (knockback)
  and `02AEDFE4` (combo) are read exactly where the tables above say; a hook that writes them after
  their producer and before their consumer changes the odds without touching the RNG stream.
- **The three evade bands are stats `+0x31`–`+0x33`** — innate, weapon and shield evade; set them on a
  unit's stats record and the roller uses them next swing (the rebuild overwrites them).
- **Do not zero `02AEDFD4`**: it survives the reset on purpose; and id `0x9F` is a random draw
  cached in the source's record `+0x10`, not a real row — a hook that inspects the action id must
  read the cache (`BattleRuntime_GetEffectiveActionId` `00387090`) to see what will be executed.

## 7. What is not known

- [x] ~~**Where stats `+0x31` / `+0x32` / `+0x33` come from**~~ — **FT-1 ANSWERED 2026-09-11** (§2.3):
  shield evade (kind-2 row `+0x18`), weapon evade (kind-1 row `+0x1D`) and the record's own evade
  (definition / `.ard` column `+0x2A`); area units add the stats modifier words and substitute
  `.ard` columns `+0x02` / `+0x2E` under the definition's `+0x15` bits 1 / 0.
- [x] **UQ-120.** **What the reaction events `0x2037`, `0x2039`–`0x203C` draw** (§2.6) — the unit event poster *(closed — the register row is WITHDRAWN.)*
  `003299B0` receives them; the presentation is unread. **FT-2.**
- [x] **FT-3.** **What the 25-row pool behind action id `0x9F` is, and who commits `0x9F`** — the id is a
  uniform draw over the action rows with byte `+0x1E == 1` and `+0x2C & 7 == 1` (`0x12`–`0x21`, `0x23`, `0x39`, `0x3B`–`0x41`),
  resolved once per commit (§2.5); the rows' names and the committer (a gambit, an AI order, a
  script verb) are the remainder. **FT-3** — narrowed 2026-09-11 (it was read as "repeat the last
  action"; the cache made it look so).
  **Narrowed again 2026-09-15 (FABLE), still PARTIAL.** This is static and authored-data evidence; nothing was executed.
  - **The 25 rows, by their authored names** ([recipe users](../Recipe-System/recipe-users.tsv), which reads the action
    table's name word):
    - `0x12`–`0x21` and `0x23`: Fire, Thunder, Blizzard, Aqua, Aero, Fira, Thundara, Blizzara, Bio, Aeroga, Firaga,
      Thundaga, Blizzaga, Shock, Scourge, Flare, Scathe. These are all recipe 7.
    - `0x39` and `0x3B`–`0x41`: Blind, Poison, Silence, Sleep, Blindga, Toxify, Silencega, Sleepga. These are recipe 3.
  - **`0x9F` itself is authored as a technick.** Its own row is "Shades of Black" (recipe 39, the only user). Row 1 of
    the technick table (registry `02EBF0E8`, battle-pack directory `+0x7C`, 24 × 8) carries `u16 +0x04 = 0x9F`.
    `+0x04` is the word the query filler names technicks by, so rows 0–23 are action ids `0x9E`–`0xB5`.
  - **The commit callers do not single it out.** `BattleUnit_CommitAction` `0030F760` has five raw call sites:
    - `BattleUnit_SelectAndCommitNextAction` `00305AB0`, twice;
    - the order-set walk `00305CC0`;
    - combo continuation `0030FA00`;
    - engage auto-attack `00312FA0`.
    None of them tests `0x9F`. An image-wide immediate census finds it used as an action id at exactly five sites:
    `00304DA5` (flag 35), the preview `003857F3`, the resolver `00385FEA`, and the effective-id pair `00387100` /
    `00387ACB`. The other ten hits are six `and al, 0x9f` masks, an argument to `00174470` outside the battle code, a
    log call and two library compares.
  - **The authored gambit presets do not carry it.** No action slot of the 40 preset rows (`02EBF0E0`, directory
    `+0x24`) holds `0x9F` or the encoded technick `0x4001`.
  - **Remainder:** whether any foe order set or script verb commits `0x9F`. The technick row makes the party route
    authored, but which producer supplies it at run time is not read.
  **ANSWERED 2026-09-15 (FABLE), authored data plus static code — the remainder closes negative:**
  - **No enemy order reaches `0x9F`.** An order record's selector goes through `BattleData_ResolveWeightedId` `00308EC0`:
    below `0x8000` it is the action id itself; from `0x8000` it indexes a weighted table `[02EBF160]`, bound from the battle
    pack's directory `+0x2C` (826 lists of 4-byte `{u16 id, u8 weight}`, drawn `% 100`).
    - Over all 166 `.ard` order-set directories (1,422 sets, 50,050 records, which reproduces the loader page's counts),
      **0 records carry `0x9F` directly, no weighted list contains it, and so 0 records reach it through one**.
    - Controls: id `0x1` is found 40 times directly; id `0x1AD` 46 times directly and 2,025 times through weighted lists.
  - **No shipped script passes it.** In the decompiled `us` corpus the literal 159 / `0x9F` appears only as an argument
    to movement, wait, quest-flag and name verbs. `btlAtelSetAbility` (6,746 uses) takes bitmasks. A value computed at
    run time is not covered.
  - With the gambit-preset negative above, **the only authored carrier of `0x9F` is technick 1, Shades of Black**: a
    party member uses it from the Technicks command or from a gambit the player sets.
  - **Not traced:** which of `BattleUnit_CommitAction`'s five callers the command menu reaches.
- [x] **FT-4.** **The unnamed words** — `02AEDFF8` / `02AEDFFC` (what `0038E080` writes into the two words
  whose difference is result `+0x1D`), `02AEE000` (the forced bit 12). ~~`02AEE044` / `02AEE048`
  (two bytes)~~ — the target's / source's new level (§2.2, 2026-09-11). ~~Which of `02AEE004` / `02AEE008` is the delta and which the absolute~~ — neither:
  loss, gain and a separate absolute per group (§2.7). **FT-4** — narrowed 2026-09-11.
  **ANSWERED 2026-09-15 (FABLE).** This is a static reading of the shipping image. Nothing was executed.
  - **The two words are the charge count's loss and gain, and one step writes them.** A `.text` census of
    `02AEDFF8`–`02AEDFFF` finds 14 writes and 2 reads. The writes are the reset (2), the resolver's normalised write-back
    (2) and `0038E080` (5 each). `0038E080` is **calculator slot 129** (`[01EFA5C0 + 129×8]` = `01EFA9C8`). It has no
    direct caller, and the only one of the 109 shipped recipes (`01EF96C0`) that names it is **recipe 33, whose committed
    list is `[129]` alone**. [Recipe users](../Recipe-System/recipe-users.tsv) gives recipe 33 two authored action
    rows: `0x57` "Elixir" and `0x67` "Megalixir".
  - **The body** (`0038E080`–`0038E2C1`). `rdx` is the target's [stats record](../Battle-Stats-Record/the-battle-stats-record-field-map.md)
    and `r8` the [evaluation context](../Evaluation-Context/the-evaluation-context-field-map.md). It has two outcomes:
    - **Refill** (`0038E0C1`–`0038E12D`):
      - target HP absolute `02AEE02C` = the same cap slots 111 / 119 use: `max(1, HP +0x48)` under status 16, `2 × max HP +0x24`
        under status 28, else `+0x24`;
      - target MP absolute `02AEE030` = capacity `+0x28`, or `0` when either layer holds id 39;
      - **loss `02AEDFF8` = 0, gain `02AEDFFC` = MP bars `+0x37` − charges `+0x4E`**;
      - result `+0x140` bit 13 set.
    - **Drain** (`0038E145`–`0038E168`, `0038E1F3`–`0038E216`):
      - **loss = charges `+0x4E`, gain = 0**;
      - HP and MP absolutes = `1`;
      - bit 13 cleared, so the step ends in `BattleRuntime_MarkTargetHistoryBit` (`0038E23B`).
    - **Which one runs:** drain exactly when **the target's Reverse** (context `+8` bit 12) **XOR the source's merged
      layer id 15** (context `+0x1B` bit 7, copied from the source's `+0x68 | +0x78` at `00384820`–`00384858`). The first
      store is always the refill. Reverse overwrites it with the drain (`0038E137`), and id 15 flips it back (`0038E172`);
      without Reverse, id 15 alone selects the drain (`0038E1EC`). The context builder clears both inputs in the same two
      cases (`00384896` / `0038489D`, `003848A6` / `003848B8`).
    - **Two early exits.** When the target's layers hold id 1 (Stone, `+0x68` / `+0x78` bit 1): refill values, roll-over
      `02AEDFB8 = 1`, no drain test (`0038E240`–`0038E2B3`). When context `+0x18` is `0xD` (the unit byte `FQ-2` leaves
      unnamed): the history bit is marked and both absolutes are `0`, with no charge words written (`0038E09E`–`0038E0B5`).
  - **Where they land.** The resolver stores `low8(gain − loss)` in result `+0x1D` (§2.7). The applier calls
    `BattleStats_ModifySecondaryResource(target, +0x28 × (s8)+0x1D)` (`003116B4`–`003116E0`). That moves the charge pool
    `+0x06` by whole capacities, so a refill tops charges up to the bar count and a drain empties them (`EZ-3`). **So
    result `+0x1D` is non-zero only through slot 129**; among the shipped recipes, only recipe 33 reaches it.
  - **`02AEE000` is never non-zero.** Its only store is the reset's `mov [02AEE000], eax` with `eax` zeroed at
    `003849B0` (`00384A16`). All the absence searches came back empty, with controls:
    - A register-tracked `lea` base plus displacement found 0 sites (`leabase_reach.py`; its control `002479B0` →
      `0208ED68` passes).
    - An image-base displacement (`0x29CE000`) and raw `u32` constants `02AEE000` / `029CE000` found 0.
    - OPUS's `check_literal_base_access.py --all` (control PASS) lists no function in the formula range.
    So the `00386542` test never forces bit 12: flag word A bit 12 comes from the target-MP difference words alone.
  - **`02AEE044` / `02AEE048`** were named 2026-09-11 (§2.2).
  - **The row's "caller mask" is not the caller's.** `r12d = 1` at `0030746E` in `Battle_ProcessActionTarget`.
    No write to `r12` follows before `003075F4`, and no jump enters `0030746E`–`003075F4` from outside: the eleven
    arms of the table at `0030762E` all land later. So `test r12b, al` tests **flag word B bit 0**, and entry bit 11
    (`003075F9`) is **the mode-2 resource reaction chance rolled** (`003891D9`), beside bits 8 / 9 / 10.
  - **Not claimed:** which augment shares merged id 15 with Slow, what the history bit is for, and whether any
    non-recipe route invokes slot 129.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the block is 44 words from `02AEDFB8` and the reset touches 41 | `003849B0` read whole; the census's 912 references | 1 | PROVEN |
| the copy-out's arithmetic, overrides, flag bits and normalisation (§2.7) | `0038643F`–`003866C1` read; EXP-059 (thirteen isolated cases, exact write sequences, a zero-as-absent mutant rejected) | 1 + isolated original code | PROVEN for the segment |
| the roller's bands, thresholds and kinds | `003896B0` read whole; `00389040`'s four stores | 1 | PROVEN |
| flag word B bits 1 / 2 / 3 = combo continues / parry / knockback | `0038887A`; `00385A21`–`00385A2D` with `003884F0`; `00389741` with `00388440` | 1 | PROVEN |
| the per-unit record mirrors bits 1–3 both ways | `00385AC3`–`00385AF2`; `003860DF`–`00386108` | 1 | PROVEN |
| entry bit 8 = knockback, bit 10 = combo continues | `00307300`'s copies; `00308790` / `0030C045`; `0030071A`–`00300726` | 1 | PROVEN |
| the kind → code → event maps | the two jump tables at `0030DB40` and `003177E4` decoded | 1 | PROVEN |

## 9. Related

- [`../../07-Combat-Action/Result-Record/the-result-record-field-map.md`](../../07-Combat-Action/Result-Record/the-result-record-field-map.md) — the result record the copy-out fills.
- [`../combos-and-the-guard-parry-flag.md`](../combos-and-the-guard-parry-flag.md) — the combo count in the same byte, and `02AEDFC4`.
- [`../Steal/the-steal-roll.md`](../Steal/the-steal-roll.md) — `02AEE04C`–`02AEE04E` and the "roll over" word.
- [`../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md`](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) — `02AEE054`–`02AEE05C` and the damage words.
- [`../Battle-Stats-Record/the-battle-stats-record-field-map.md`](../Battle-Stats-Record/the-battle-stats-record-field-map.md) — stats `+0x31`–`+0x33`.
- [`../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) — the target buffer entry the bits end up in.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

§2.2 carries **eighty-eight numbers** — a write count and a read count for each of 44 words — plus
three totals. All of it was recomputed by disassembling every body in `functions.tsv` and taking
every rip-relative reference landing in `02AEDFB8`–`02AEE05F`. **The table was parsed out of this
page rather than retyped**, so the comparison is against what the page actually says.

| claim | measured |
|---|---|
| **912** referencing instructions in `.text` | **912** |
| **44** words, and no others | **44 distinct addresses touched** — none outside the table, no row without a reference |
| the 88 per-word counts | **44 of 44 write counts exact; 43 of 44 read counts exact** — the one difference is a counting convention, below |
| `003849B0` is **340 bytes** with **42 stores** covering **43 of the 44** | **340 B, 42 stores**, and 43 of 44 covered |
| `02AEDFD4` is the one word the reset does not touch | **confirmed** — it is the only genuinely untouched entry |
| `02AEDFF0` has **20** writers | **20**, once the two `cmp dword ptr [rip], …` are excluded |

### Three counts in this document, three different units

**44 words over 168 bytes.** `02AEDFB8`–`02AEE05F` is 168 bytes, which is **42** dwords, not 44. The
count is right because **three of the entries are single bytes** — `02AEE04C`, `02AEE04D`,
`02AEE04E`, the steal tiers. 41 dwords + 3 bytes = 44. *(`02AEE04F`, the fourth byte of that dword,
is referenced by nothing in the image.)*

**42 stores covering 43 entries.** Only **42 distinct addresses** are stored by the reset, yet it
covers 43 of the 44. The extra entry comes from one instruction being wider than its neighbours:

```asm
00384A1C  mov  word ptr [rip+0x276962a], ax     ; -> 02AEE04D  AND 02AEE04E
```

A **2-byte** store spanning the uncommon and rare steal bytes — which is exactly why §2.2 records
`02AEE04E`'s reset as *"(with 4D)"* rather than giving it a value of its own. The page was already
right; this is the instruction that makes it right.

**Eight reads that are also eight writes.** The single disagreement in 88 numbers is `02AEDFF0`,
where the page says 8 reads and a census that counts a read-modify-write on both sides says 16.
Both are defensible; the page's convention is that **an RMW counts as a write only**, and §2.2's
note that *"`w / r` counts instructions, not functions"* does not say which. It matters in exactly
one row, because:

### `02AEDFF0` is the only word of the 44 that is ever read-modify-written

Every other one of the 912 references is a pure load or a pure store. This word takes **eight
`add dword ptr [rip], eax`** — four in `BattleFormula_RollSpecialGuardOutcome` (`003880F0`,
`00388148`, `003881A0`, `003881ED`) and four in `00389370` (`00389435`, `0038948D`, `003894E5`,
`00389532`).

So §2.2's *"`RollSpecialGuardOutcome` `00387FD0` rewrites it seven times"* is **exact as a count** —
3 `mov` + 4 `add` = 7 — **and misleading as a verb**: four of the seven do not rewrite the threshold,
they **accumulate into it**. The avoid threshold is a *running total* built across the function, and
`00389370` has the identical 3-`mov`-plus-4-`add` shape. A modder who reads "rewrites" and
substitutes a `mov` for one of those `add`s changes the outcome of the roll.

**Not claimed:** nothing here was executed or observed live. The pass re-measured the census and the
reset; the semantic readings in §2.3–§2.7 (band ordering, flag-bit destinations, the copy-out) were
not re-derived, and `FT-4` remains open.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

- **Gameplay — SERVICE.**
  - `Battle_ProcessActionTarget` (`00307300`) dispatches presentation events and submits a reaction mode
    (`BattleUnit_SubmitResultReactionMode`).
  - `0030D160` resets the battle target buffer, appends to it and searches it.
  - `Battle_EmitReactionPresentationForSlot` (`003176E0`) is called by a 552-byte body and calls the presentation
    dispatcher.
- **Movement — SERVICE.**
  - `00307300` steers through `Actor_SetDesiredMovementHeading`, `Actor_SetFacingHeading_Variant1` and four helpers.
  - `00384F40` calls two movement helpers of 36 and 58 bytes.
  - The dispatcher is also called by the stance-bit setter.
- **Spawn_Encounter_Lifecycle — CLIENT.** `SpawnGroup_RecordMemberDeathAndHandleCompletion` also calls the presentation
  dispatcher.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer, calls `0030C650` on this page. That caller is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Audio — SERVICE (2 edges).** `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` calls `003A1180` and `002DF220`, the resolve-then-play sound pair. The level-advance routine that receives the scratch block's level word through the applier plays a sound through the audio layer; the scratch block does not reach it.

**CombatAI — CLIENT and SERVICE (10 edges).** `BattleUnit_UpdateCombatFrame` `00308610` calls `BattleUnit_SelectAndCommitNextAction` `00305AB0`, `BattleAction_TryContinueComboSequence` `0030FA00` and `BattleUnit_DispatchActorPresentationEvent` `003299B0`; `00305AB0` calls the order-set walk `BattleUnit_TrySelectAndCommitAiOrderFromSet` `00305CC0`, and both call `BattleUnit_CommitAction` `0030F760`; `00305CC0` calls `AiOrder_EvaluateAndResolveActionTarget` `003014C0`, which calls `BattleData_ResolveWeightedId` `00308EC0`; `Battle_ProcessActionTarget` `00307300` calls `BattleEnmity_ApplyActionParameters` `003216E0`. These are the commit callers §7 lists (none tests action `0x9F`) and the order selector whose weighted-id resolution §7 uses to show no enemy order reaches `0x9F`; the AI decides the action, the scratch block is filled only after it resolves.

**Party — SERVICE (3 edges).** `Battle_BuildActionTargetSet` `0030D160`, `0030F760` and the engage auto-attack `BattleUnit_TryCommitEngageAutoAttack` `00312FA0` call `BattleUnit_ResolveByFocusHandle` `0031B7E0`. The target-set builder and the two commit paths resolve units through the party's focus handle; no scratch word depends on the party layer.

**RNG_Random_Selection — SERVICE, DEPENDENCY (22 edges).** Twenty-one scratch writers draw from `RNG_MT19937_NextU32_Thunk` `00379CD0`: the action-id draw `00387130` (§2.5, action `0x9F`), `BattleFormula_RollSpecialGuardOutcome` `00387FD0`, `BattleFormula_ComputeKnockbackChance` `00388350`, `BattleFormula_RollKnockback` `00388440`, `BattleFormula_RollGuardParryMode` `003884F0`, `BattleFormula_RollAndStoreComboCount` `00388660`, `BattleFormula_RollAvoidGuardParryOutcome` `003896B0`, the steal roll `00390390`, `BattleFormula_SelectPoachRewardItem95_5` `00390680`, the percent-gate rolls `0038FB80` and `0038FBC0`, and ten more; and `BattleData_ResolveWeightedId` `00308EC0` draws instead from `RNG_SharedGameplayLCG_NextU32` `00328370`. Every rolled scratch word — knockback, parry, guard band, combo count, steal tier, poach item, the attack variance words — is a draw from the gameplay MT19937 stream, so their values depend on the stream's position; the AI's weighted-id pick uses the separate shared gameplay LCG.

**Status_Periodic_Terminal — CLIENT and SERVICE (4 edges).** `0030C650` calls `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0`; `003299B0` is called by `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` and `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`; `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls the resolver `BattleFormula_ResolveTargetResult` `00385F60`. The periodic tick runs the same resolver that writes and reads the scratch block, a level change ends in the status recompute, and the unit-event dispatcher that receives the result kinds of §2.6 is shared with the status paths.

**WorldAreaField — DEPENDENCY (7 edges).** `00305AB0`, `00307300`, `0030D160`, `0030F760` and `00312FA0` call `FieldData_GetActiveFieldRecordBit15` `00377C20`, and `Battle_EmitReactionPresentationForSlot` `003176E0` and `00384F40` call it through its thunk `00313F60`. Selection, targeting, commit and the reaction presentation consult the current field's bit 15, the per-area waiver for disabling statuses; the scratch words themselves are not field state.
