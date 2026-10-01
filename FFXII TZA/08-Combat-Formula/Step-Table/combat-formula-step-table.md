---
system: CombatFormula step table
category: 08-Combat-Formula
status: AUDITED
owner_layer: PrimaryOwner:CombatFormula
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
last_reviewed: 2026-09-02
audit:
  passes: 2
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
---

# CombatFormula step table

> The 202 numbered steps FFXII's combat maths is assembled from — guard rolls, element affinity,
> the damage finalizer, Poach — addressable by id from authored data.

**PARTIAL.** The table itself is read exactly: its base, stride, extent and every target.

> **Corrected 2026-09-02.** The first version of this document said the interpreter "has not been
> located" and raised it as a new open question. **The database had already answered it** —
> [`../Recipe-System/ranged-weapon-recipes.md`](../Recipe-System/ranged-weapon-recipes.md)
> documents the recipe pointer table, the `-1`-separated slot lists and the dispatcher. It also
> corrects this document's original base derivation, which was weaker than it looked. See section
> 10.

## 1. What the player sees

FFXII actions behave very differently from one another — one attack can combo, another cannot; one
ignores Defence; one applies a status only sometimes; Poach yields one of two things. Yet the damage
numbers all feel like they come from the same game.

Both halves of that are true, and this table is why. **The arithmetic is shared; the *sequence* is
per-action.** An action does not carry its own damage code — it names numbered steps from one fixed
catalogue, and the engine runs them.

That is what makes FFXII's combat data-driven rather than hardcoded: adding an action means writing
a list of step numbers, not writing maths.

## 2. Native mechanism

### The table

```
base   = 0x01EFA5C0        (.data)
stride = 8 bytes           (one function pointer per slot)
extent = 202 slots         ids 0 .. 201 (0x00 .. 0xC9)
```

Every one of the 202 entries is a valid `.text` pointer; there are **no null slots**.

Full mapping: `Tools/work/rtti/formula_steps.tsv` — 202 rows, `slot / slot_hex / target / name /
owner / noop`.

**The base is confirmed by an eleven-element recipe** — see section 10 for why the original
two-point derivation given here was not the confirmation it appeared to be.

[`../Recipe-System/ranged-weapon-recipes.md`](../Recipe-System/ranged-weapon-recipes.md) records the
Bow family's committed calculator list as `[29, 66, 96, 97, 98, 99, 125, 165, 171, 176, 182]`.
Resolved against this table at base `0x01EFA5C0`, every entry lands on a step whose recovered name
fits its position in a damage pipeline:

| slot | step |
|---:|---|
| 29 | `RollPrimaryFormulaResourceReactionMode2Chance` |
| 66 | `PrepareSpeedStrengthAttackVsDefense` — the Bow's own formula |
| 96–99 | the element-affinity family, ending in `ApplyEquipmentElementAffinity` |
| **125** | **`FinalizeTargetHpMagnitude`** — the damage equation |
| 165 | `ApplyTargetHpPostMultipliers` |
| 176 | `RollPercentGateAndSetResultFlag1000` |
| 182 | `CalcApplyCandidateStatusesOptional` |

Eleven independent constraints, all satisfied, in pipeline order. A wrong base would have to place
*every one* of them on a plausible step by chance.

**Slots 60–79 are all named (2026-09-11)** — the preparation family, sixteen functions in twenty
slots, decoded on [the attack-defence page](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md)
§5.1 with the recipes, weapons and actions that reach each: 60 / 63 magick power on an action power
with no defence (Cure …), 61 / 64 / 75 the action power as the multiplier (Raise, Gravity …), 62
magick power vs magick resist (the attack magicks), 65 Strength (swords, spears, rods, crossbows),
66 Speed (daggers, ninja swords, bows), 67 Magick + Strength (katana, staves), 68 Vitality (axes,
hammers, hand-bombs), 69 Strength vs magick resist (poles), 70 Attack × Attack with no defence
(guns, measures), 72 unarmed with the Brawler branch, 74 the action row's two bytes (potions,
ethers), 77 Strength on an action power from base 2 (enemy technicks), 78 Strength × 1.5 (monster
basic attacks), 79 magick power on Attack (maces). **Slots 71 and 73 have no shipped user.**

### 152 distinct targets, and 42 slots that do nothing

| | count |
|---|---:|
| slots | **202** |
| distinct target addresses | **152** |
| slots pointing at a bare `ret` | **42** |
| slots with a recovered `BattleFormula_*` name | 35 |
| slots still `FUN_*` | 125 |

The 42 no-op slots all point at `0016D6A0`, whose entire body is:

```
0016D6A0  c2 00 00    ret 0
          cc cc cc…   int3 padding
```

**A slot pointing there is a step that does nothing when called.**

Ghidra names that address `_guard_check_icall`, which is consistent rather than contradictory: this
image has **CFG compiled but disabled** (see
[`../../24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`](../../24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md)),
so the guard check *is* a bare `ret`. **The likely explanation is identical-COMDAT folding**
(`/OPT:ICF`): every function whose body is just `ret` folds to one address, so distinct source-level
no-op steps and the disabled CFG stub end up sharing it. *That is an inference from the linker
behaviour, not read from the binary — what is read is that the slot's body is a bare return.*

### Steps reachable by more than one id

152 distinct targets across 160 populated non-`ret` slots means some functions are reachable by
several ids. The clearest cases:

| ids | target |
|---|---|
| **65**, **76** | `BattleFormula_PrepareStrengthAttackVsDefense` |
| **113**, **125** | `BattleFormula_FinalizeTargetHpMagnitude` |
| 61, 64, 75 | `FUN_0038AA90` |
| 60, 63 | `FUN_00389F80` |
| 40, 45, 46 | `FUN_00389670` |
| 23, 24 | `FUN_00388FE0` |

So an id is **not** an identity — two ids can name the same behaviour. Anything mapping ids to
weapon or action types must allow for that.

### The named catalogue

35 slots carry a recovered name, and together they describe the shape of FFXII combat resolution:

| Slot | Step |
|---:|---|
| 2 | `RollSpecialGuardOutcome` |
| 5, 6 | `ComputeKnockbackChance`, `RollKnockback` |
| 7, 8 | `ComputeParryChanceFromSpeed`, `RollGuardParryMode` |
| 9, 10 | `ComputeComboChance`, `RollAndStoreComboCount` |
| 25 | `LoadHitAvoidGuardThresholds` |
| 29 | `RollPrimaryFormulaResourceReactionMode2Chance` |
| 41 | `RollAvoidGuardParryOutcome` |
| **65–69, 76, 78, 79** | the seven **attack-vs-defence preparations** |
| 95, 99 | `ApplyActionElementAffinity`, `ApplyEquipmentElementAffinity` |
| **113, 125** | **`FinalizeTargetHpMagnitude`** — the damage equation |
| 136–139 | `ReduceStrengthTo70Percent`, `ReduceMagickPowerTo70Percent`, `ReduceDefenseTo90Percent`, `ReduceMagickResistTo90Percent` |
| 149, 150 | `BoostStrengthByActionPercent`, `BoostMagickPowerByActionPercent` |
| 165 | `ApplyTargetHpPostMultipliers` |
| 175, 176 | `RollPercentGateAndMarkResolved`, `RollPercentGateAndSetResultFlag1000` |
| 180–182 | `CalcRemoveEligibleCandidateStatuses`, `CalcApplyCandidateStatusesRequired`, `CalcApplyCandidateStatusesOptional` |
| 196 | `SelectPoachRewardItem95_5` |

> **Six more bodies, ten more ids, read 2026-09-12 (FABLE, AK-3 / E-3) — working names are FABLE's,
> from the bytes; the scratch cells are [the formula scratch block](../Scratch-Block/the-formula-scratch-block.md)'s, the row is [the action definition row](../../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md) resolved
> from `02EBF138` by the id under evaluation (`02AEDFD4`):**
>
> | Slot | Body | What it does |
> |---:|---|---|
> | **0** | `00387F40` (33 B) — *ImmuneWhenTargetIsStone* | if the target's status layer `+0x68` or augment layer `+0x78` has **id 1 (Stone)**, set **immune by kind** (`02AEDFC0`) and **roll over** (`02AEDFB8`); otherwise nothing (`00387F40`–`00387F60`) *(corrected the same day: "bit 1" is id 1)* |
> | **11** | `003888C0` (34 B) — *FailWhenTargetIsPartyTable* | if the target record exists and its `+5` is 0 (a party-table unit), set **failed** (`02AEDFBC`) and roll over — the "enemies only" gate |
> | **31** | `00389230` (83 B) — *AdjustHitChanceByShellAndFaith* | the third argument is [the evaluation context](../Evaluation-Context/the-evaluation-context-field-map.md), not the row *(corrected the same day)*: target merged flags `+8` bit 19 (**Shell**) → **hit chance** (`02AEDFE0`) `= max(1, hit / 2)` (`00389240`–`0038924F`); source merged flags `+4` bit 22 (**Faith**) → `= min(100, hit × 1.5)` (`0038925F`–`0038927C`, constant `00901B3C`) |
> | **40, 45, 46** | `00389670` (63 B) — *RollPlainHitChance* | `r = RNG(00379CD0) % 100`; unless **hit chance** `> r`, set **failed** and roll over (`0038968D`–`003896A0`) — the hit roll without the avoid / guard / parry bands of slot 41 |
> | **61, 64, 75** | `0038AA90` (92 B) — *LoadActionPowerAsMultiplier* | **the multiplier** (`02AEE054`) `= (float) row +0x10`, the action's power byte, straight — the fixed-power preparation |
> | **170** | `0038F970` (96 B) — *LoadActionPercentGate* | **percent gate** (`02AEDFE8`) `= row +0x14` (the byte that is 100 on Bio / Scourge / Meteorite…, 35 on the *-ja* spells), for slots 175 / 176 to roll against |
> | **47** | `00389AB0` (289 B) — *RollLevelDifferenceHitChance* | `hit = row +0x12 + (Lsource − Ltarget) × k`, `k = 3` when the source's level (`+0x1C2`) is at or above the target's, `1` when below (`00389AC4`–`00389B75`), clamped to `[1, 100]` (`00389B77`–`00389B92`); then `r = RNG % 100` and unless `hit > r`, **failed** + roll over (`00389B98`–`00389BC0`) — the level-gap hit roll |
> | **21** | `00388F20` (141 B) — *LoadMagickHitChance* | if the source carries **id 18** (augment "Improves chance to strike with magicks", ctx `+0x1C` bit 2) → **hit chance** `= 100` (`00388F37`); else `= row +0x12 + source Magick Power (+0x2B) − target Vitality (+0x2C)` (`00388F8C`–`00388FA1`) |
> | **32** | `00389290` (123 B) — *DoubleHitChanceByCasterHpAugments* | source carries **id 8** (augment "Raises magick power when HP Critical", ctx `+0x1B` bit 0) **and** has status **29 HP Critical** (ctx `+4` bit 29) → hit `= min(100, hit × 2)` (`003892A7`–`003892B7`); source carries **id 103** ("Increases magick power when HP is full", ctx `+0x26` bit 7) and its HP `+0x48` equals its cap — `max(1, HP)` under **Disease** (bit 16), `2 × max HP` under **Bubble** (bit 28), else max HP `+0x24` — → hit `= min(100, hit × 2)` (`003892C5`–`00389304`) |
> | **93** | `0038B150` (199 B) — *ScaleMultiplierByCasterHpAugments* | the same two conditions on **the multiplier** (`02AEE054`): HP Critical + id 8 → `× 2.0` for a unit `002F8E90` classes as 1 / 2 / 4 (a party-table unit, or an enemy-table unit of actor class 3), `× 1.7` otherwise (`0038B171`–`0038B194`; constants `01CEBC08`, `00D112C0`); full HP + id 103 → `× 1.5` / `× 1.4` by the same split (`0038B1CD`–`0038B204`; `00901B3C`, `00901B38`) |
> | **92** | `0038B010` (310 B) — *ApplyStatusMagickModifiers* | source **Faith** (ctx `+4` bit 22) → multiplier `× 1.3` (`00901B34`); target **Sleep** (ctx `+8` bit 4) → `× 1.5`; target **Shell** (bit 19) → `× 0.75` (`009155D8`); target **Oil** (bit 11) with the row's `+0x13` bit 0 → `× 3.0` (`008F311C`); target **Float** (bit 26) with row `+0x13` bit 3 → **failed** + roll over (`0038B0E3`–`0038B131`) |
> | **119** | `0038D6B0` (296 B) — *FinalizeTargetHpPercentOfMaximum* | the percent-of-max-HP finaliser: with the element-affinity word `02AEDFCC` set (immune) → **immune by kind**, HP loss `02AEE004 = −1`, result flag C `+0x140` bit 0 (`0038D6BC`–`0038D6DB`); with `02AEDFD0` set (absorb) → result flag A `+0x2C` bit 10, and **HP gain** `02AEE008 = cap × multiplier / 100` where the cap is `max(1, HP)` under **Disease**, `2 × max HP` under **Bubble**, else max HP `+0x24` — unless the target has **Reverse** (ctx `+8` bit 12), which turns it into the loss and clears bit 10 (`0038D6E5`–`0038D760`); otherwise **HP loss** `= cap × multiplier / 100`, or the gain under Reverse (`0038D761`–`0038D7C2`); then `BattleRuntime_MarkTargetHistoryBit(source, target)` when the value is not `−1` (`0038D7CA`–`0038D7D2`; [the result record](../../07-Combat-Action/Result-Record/the-result-record-field-map.md)) — the Gravity-shaped damage, a fraction of the *target's* maximum |
>
> *Nine more, read later the same day (FABLE, AK-3 D) — the single-recipe bodies behind named actions:*
>
> | Slot | Body | Recipe → actions | What it does |
> |---:|---|---|---|
> | **4** | `00388320` (48 B) — *FailUnlessTargetIsKoPartyUnit* | 6, 36 → Raise, Arise, Phoenix Down | unless the target has **status 0 KO** (ctx `+8` bit 0) **and** `002F8E90(target)` returns 1 (a party-table unit outside the `0x1B`–`0x27` band), set **failed** + roll over (`00388324`–`00388341`) |
> | **112** | `0038D230` (77 B) — *GainPercentOfTargetMaximumHp* | 6 → Raise, Arise | **target HP gain** `02AEE008 = max(1, cap × multiplier / 100)`, the cap being `max(1, HP)` under Disease, `2 × max HP` under Bubble, else max HP (`0038D230`–`0038D276`) — the revive amount as a percent of the target's own maximum |
> | **142** | `0038EA60` (80 B) — *SetTargetHpToMaximumIfKo* | 54 → Revive | with target KO (ctx `+8` bit 0) and source ≠ target, **target HP absolute** `02AEE02C = cap` (the same Disease / Bubble cap); otherwise **failed** + roll over |
> | **148** | `0038EE10` (33 B) — *DrainTargetHpToSource* | 67 → Leech | `v = (int)(multiplier × (attack + variance))`; **target HP loss** `02AEE004 = v` and **source HP gain** `02AEE018 = v` |
> | **151** | `0038EF60` (74 B) — *GainAttackMinusDefenseToBoth* | 71 → no shipped action row | `v = (attack + variance − target defensive stat) × multiplier`; if the difference is not positive, roll over with both gains 0, else **source HP gain** and **target HP gain** `= v` |
> | **157** | `0038F380` (26 B) — *EndChainOnSelfTarget* | 83 → Self-Sacrifice, Self-Destruct, Mass-Destruct, Kamikaze | sets **roll over** when source == target — the self entry of the blast ends the slot loop; other targets continue |
> | **124** | `0038DB10` (60 B) — *RollMeteorDamage* | 19 → Meteorite, Meteor | `r = RNG % 20000`; **target HP loss** `= r` when `r ≤ 9999`, else **30,000** (`0038DB14`–`0038DB40`) — an even chance of a 0–9,999 hit or a flat 30,000 |
> | **133** | `0038E720` (76 B) — *HorologyLevelTimesClockDigitSquared* | 40 → Horology | `d = (playClockSeconds / 60) % 10` (the play clock through `002536B0`, [the save-image page](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md)) and **target HP loss** `= source level (+0x1C2) × d × d` (`0038E729`–`0038E760`) |
> | **134** | `0038E770` (72 B) — *ChargeMpByLevel* | 43 → Charge | **target MP gain** `02AEE010 = L` for `L < 2`, else `L + (RNG % L) / 2` with `L` the target's level |
> | **105** | `0038CCF0` (99 B) — *LossPowerTimesSourceLevel* | 93 → Inferno, Cataclysm, Torrent, Windburst (the Esper ultimates) | **target HP loss** `= row power (+0x10) × source level (+0x1C2)` |
> | **26** | `003890C0` (113 B) — *LoadUnavoidableHitChance* | 66 → Temblor, Judgment, Cyclone, Bitter End | **hit chance** `= row +0x12` and the three outcome-band thresholds (`02AEDFF0` / `F4` / `EC`) `= 0` — no block, parry or evade band |
> | **123** | `0038DA90` (117 B) — *RollUpToSourceMaximumHp* | 18 → Meteorite, Comet | **target HP loss** `= RNG % cap` with `cap` the *source's* `max(1, HP)` under Disease, else max HP (`2 ×` under Bubble); 0 when the cap is 0 |
> | **140** | `0038E950` (120 B) — *BonecrusherGamble* | 48 → Bonecrusher | `r = RNG % 100`; `r < 55` → **target HP absolute** `02AEE02C = 0` (the target drops to 0) and **source HP loss** `02AEE014 = RNG % source HP` (both 0 when the source has no HP); otherwise **source HP loss** `= source HP` — the user falls instead |
> | **154** | `0038F120` (133 B) — *SetTargetMpToPercentOfMaximum* | 76 → Fog, Magick Ballad | `m = target max MP (+0x28)` unless the target's status or augment layer holds **id 39** (`+0x6C` / `+0x7C` bit 7, then `m = 0`); **target MP absolute** `02AEE030 = row power × m / 100` |
> | **12** | `003888F0` (150 B) — *FailWhenSourceWeaponKindBit2* | 50 → Telekinesis | resolves the source's slot-0 equipment row (`+0x50 − 0x1000` in `02EBF0F8`, [the equipment compatibility page](../../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md)) and, when the row's kind byte `+7` has **bit 2**, sets **failed** + roll over |
> | **141** | `0038E9D0` (137 B) — *TelekinesisAttackTimesRandomLevel* | 50 → Telekinesis | `f = (RNG % (Ltarget × 100)) / 100` (0 when the target's level is 0) and **target HP loss** `= source Attack (+0x2E) × f` — a random fraction of the target's level |
> | **135** | `0038E7C0` (168 B) — *SouleaterStrikeAtTenthOfOwnHp* | 45 → Souleater | `v = attack + variance − target defensive stat` (≤ 0 → loss 0); when the context's source type word `+0x18` is `0xD` → **target HP gain** `= 2.0 × multiplier × v`, else **target HP loss** `= 1.7 × multiplier × v` (`01CEBC08`, `00D112C0`); then **source HP loss** `= cap / 10` with the Disease / Bubble cap of the source's own maximum |
> | **111** | `0038D180` (174 B) — *SetTargetHpToMaximumOrOne* | 5 → Renew | **target HP absolute** `= cap` (the target's Disease / Bubble cap), or `1` when the source's type word `+0x18` is `0xD`; target **Reverse** (ctx `+8` bit 12) swaps the two; the history bit is marked when the value differs from the cap (`0038D180`–`0038D228`) |
> | **114** | `0038D340` (187 B) — *LossEqualToSourceMissingHp* | 8, 108 → Balance, Reflectga Mote, Gravity Well, Big Bang | `v = (source cap − source HP) × multiplier`, floored at 0 — the user's missing HP; **target HP loss** `= v`, or **target HP gain** `= v` with the history bit under target Reverse |
> | **132** | `0038E590` (398 B) — *FirstAidRandomHealIfCritical* | 38 → First Aid | **failed** unless the target has **HP Critical** (ctx `+8` bit 29); `r = RNG % 100`; **target HP gain** `= RNG % target cap` when `r < row +0x12`, else a fifth of that (`0038E601`–`0038E712`); 0 when the cap is 0 |
> | **145** | `0038EB30` (171 B) — *LossRowPowerTimesRowByte11* | 59, 107 → 1000 Needles, Dark Energy, Final Eclipse | **target HP loss** `= row +0x11 × row +0x10` — two authored bytes multiplied, no stat |
> | **152** | `0038EFB0` (174 B) — *SwapTargetHpAndMp* | 74 → Invert | **target MP absolute** `= target HP`, capped at max MP (`+0x28`, or 0 when the target's layers hold id 39); **target HP absolute** `= target MP (+0x4C)`, capped at the Disease / Bubble cap |
> | **153** | `0038F060` (191 B) — *LossPercentOfTargetMaxMp* | 75 → Fear, Fearga, Annul | **failed** when the target's MP is 0; **target MP loss** `02AEE00C = min(9,999, row power × max MP / 100)` (max MP 0 under id 39) and result flag A `+0x2C` bit 18 |
> | **156** | `0038F2D0` (171 B) — *GainRowPowerTimesRowByte11* | 78 → Charge | **target HP gain** `= row +0x10 × row +0x11` |
> | **158** | `0038F3A0` (276 B) — *GainPercentOfTargetMaxHp* | 84 → Restore, Renew, Joyous Soundwave, Breath of Life | **target HP absolute** `= HP + row power × cap / 100`, capped at the cap |
> | **159** | `0038F4C0` (222 B) — *GainPercentOfTargetMaxMp* | 85 → Focus, Meditate, Now Enkidu, Crimson Vortice | **target MP absolute** `= MP + row power × max MP / 100`, capped at max MP (0 under id 39) |
> | **118** | `0038D680` (41 B) — *DoubleTargetHp* | *no shipped recipe* | **failed** when the source's type word is `0xD`; else **target HP absolute** `= 2 × target HP` |
> | **131** | `0038E480` (270 B) — *FinalizeTargetHpPercentOfMaximumB* | *no shipped recipe* | the twin of slot 119: immune → immune by kind and loss `−1`; absorb → gain `cap × multiplier / 100` (loss under Reverse); else loss (gain under Reverse); history bit when the value is not `−1` |
>
> Recipe use, from the 109 shipped lists: slot 0 ×16, 47 ×14, 40 ×11, 11 ×11, 21 ×9, 32 ×9, 31 ×7,
> 170 ×7, 64 ×5, 93 ×5, 92 ×5, 119 ×4, 45 ×2, 46 / 61 / 75 ×1. Slot 62 (`00389DD0`, ×4) was already
> named on [the attack-defense page](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) §5.1 — `PrepareMagickPowerActionPowerVsMagickResist` — and is not residue.
> Slot 94 (`0038B220`, ×7) is **not** unread either: it is
> `BattleFormula_ApplyWeatherTerrainElementScalingUnlessWeatherproof`, read whole on [the weather / terrain scaling page](../Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md)
> (corrected the same day). An exact census — every slot a shipped recipe names whose body no page
> cites — left **seventeen**; eight more read later the same day (AK-3 E) and the last nine after
> that (AK-3 F), **so every slot a shipped recipe names is now read or named on a page.** Of the 160
> populated non-no-op slots, 42 are the folded `ret 0`, and only two bodies are named by no shipped
> recipe — 118 and 131, read above. The "125 still `FUN_*`" of §2 counts GFZ symbol names, not
> pages: the bodies behind those ids are described here, on the attack-defense, weather / terrain,
> steal, count-clock and status pages. `002F8E90(stats)` is the unit-class splitter the two augment slots
> share: 2 for a party-table unit of type `0x1B`–`0x27`, 1 for another party-table unit, 4 for an
> enemy-table unit of actor class 3, 8 for classes 1 / 2 / 7, else `0x10`.

**The ordering is meaningful.** Preparation sits at 65–79, the modifiers between 95 and 165, and the
finalizer at 113 — so a recipe that prepares, modifies and finalises walks the table roughly
upward. That is consistent with, but does not prove, ids being allocated in pipeline order.

### The no-caller members, bound to their slots (NOCALLER-INSTALLERS group `01EFA5C0`, 2026-09-15)

Fifty-two of the table's 152 distinct targets have **no direct caller anywhere in `.text`** — the
authored slot list is their only reachability, so the table is their installer and the slot number
is their name. The table below binds each to its slot id(s). Roles marked *italic* are the working
names read in the catalogue above; `§5.1` roles come from [the attack-defence
page](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md); the rest are signature
roles read for this pass — which scratch fields the body touches and under what guard. The interior
cite is one instruction strictly inside the body.

| body | slot(s) | role | interior cite |
|---|---|---|---|
| `003888C0` | 11 | *FailWhenTargetIsPartyTable* — party-table target `+5`==0 ⇒ failed + roll over | `003888CD` writes `02AEDFBC` (failed) |
| `003888F0` | 12 | *FailWhenSourceWeaponKindBit2* — source slot-0 equipment kind `+7` bit 2 ⇒ failed (Telekinesis) | `003888FF` reads `02EBF0F8` (equipment table) |
| `00388C10` | 17 | source-level prime/divisibility gate — builds the 25-prime list {2…97} on the stack, fails + rolls over unless the source level `+0x1C2` is in it or a nonzero multiple of the row-derived product | `00388CC0` the prime-list compare loop |
| `00388FE0` | 23, 24 | hit chance `02AEDFE0` = action row `+0x12` byte, under the `02EBF138`-row-resolved guard | `00388FE4` reads `02EBF138` |
| `003890C0` | 26 | *LoadUnavoidableHitChance* — hit = row `+0x12`, all three outcome bands 0 | `003890C4` reads `02EBF138` |
| `00389650` | 37 | doubles hit chance `02AEDFE0` when ctx `+0x1B` bit 6 (the augment flag slot 32 also tests by id) | `00389657` reads `02AEDFE0` |
| `00389950` | 43 | banded outcome roll — `RNG % hit` against the `02AEDFF0` band, writes outcome byte `[rec]+4 = 3`, gated on `0031B860` record bit 23 | `00389960` calls `0031B860` |
| `00389A50` | 44 | plain `RNG % 100` hit roll (miss ⇒ failed + roll over); on a hit with `02AEDFC8` set, ORs `+0x18` bit 3 into the target's record | `00389A59` calls `00379CD0` (RNG) |
| `0038A110` | 66 | `BattleFormula_PrepareSpeedStrengthAttackVsDefense` | `0038A14B` `divss` by `00D112D0` |
| `0038A1F0` | 67 | `BattleFormula_PrepareMagickStrengthAttackVsDefense` | `0038A22B` `mulss` by `009088D8` |
| `0038A2D0` | 68 | `BattleFormula_PrepareVitalityStrengthAttackVsDefense` | `0038A30B` `mulss` by `009088D8` |
| `0038A590` | 71 | conditional multiplier scaling (`02AEE054`/`58`/`5C`) under augment-flag checks; float consts `00915508`, `009088D8` — **no shipped user** | `0038A5C3` `mulss` by `00915508` |
| `0038A820` | 73 | row-driven multiplier step: six `0020E600` field reads + RNG + float consts — **no shipped user** | `0038A84A` reads `02EBF138` |
| `0038A9D0` | 74 | the action row's two bytes (potions, ethers) — §5.1 | `0038A9D6` reads `02EBF138` |
| `0038AA90` | 61, 64, 75 | *LoadActionPowerAsMultiplier* — multiplier = `(float)` row `+0x10` | `0038AA94` reads `02EBF138` |
| `0038AAF0` | 65, 76 | `BattleFormula_PrepareStrengthAttackVsDefense` | `0038AB27` `mulss` by `009088D8` |
| `0038ABC0` | 77 | Strength on an action power from base 2 (enemy technicks) — §5.1 | `0038ABEA` reads `02EBF138` |
| `0038AD70` | 78 | `BattleFormula_PrepareStrengthAttackVsDefenseScaled150` | `0038ADA7` `mulss` by `009088D8` |
| `0038AE50` | 79 | `BattleFormula_PrepareMagickPowerAttackVsDefense` | `0038AE87` `mulss` by `009088D8` |
| `0038B950` | 96 | element-affinity multiplier chain (the 96–99 family): eight field reads, repeated `02AEE054` rewrites | `0038B95A` `movss` from `008F8180` |
| `0038BE00` | 98 | multiplier `×1.7` (`01CEBC08`) when the context sub-record `+0x18` bit 0 is set | `0038BE0A` reads `02AEE054` |
| `0038C920` | 101 | multiplier `×1.5` (`00901B3C`) under ctx `+0x1B` bit 6 — the multiplier twin of slot 37 | `0038C927` reads `02AEE054` |
| `0038C940` | 102 | row-driven multiplier/fail step — four field reads, consts `00901B3C`, `009155D8`, ends failed + roll over | `0038C950` `movss` from `008F8180` |
| `0038CC10` | 104 | rolled target HP loss `02AEE004` — two RNG calls + four field reads | `0038CC28` calls `00379CD0` |
| `0038CCF0` | 105 | *LossPowerTimesSourceLevel* — Esper ultimates; loss = row `+0x10` × source level | `0038CCF6` reads `02EBF138` |
| `0038CD60` | 106 | rolled target HP loss `02AEE004`, same shape as slot 104 | `0038CD7B` calls `00379CD0` |
| `0038CF20` | 108 | rolled target HP gain `02AEE008` — the gain twin of 106 | `0038CF3B` calls `00379CD0` |
| `0038D340` | 114 | *LossEqualToSourceMissingHp* — loss = user's missing HP × multiplier | `0038D353` calls `00387B00` |
| `0038D680` | 118 | *DoubleTargetHp* — fails when source type word is `0xD`, else HP `×2`; no shipped recipe | `0038D688` writes `02AEDFBC` |
| `0038D7E0` | 120 | target HP absolute `02AEE02C` set from row fields — three write paths, failed/roll-over exits | `0038D7EA` reads `02EBF138` |
| `0038DA90` | 123 | *RollUpToSourceMaximumHp* — loss = `RNG %` source cap (Disease/Bubble cap) | `0038DAD6` writes `02AEE004` |
| `0038E480` | 131 | *FinalizeTargetHpPercentOfMaximumB* — slot 119's twin; no shipped recipe | `0038E495` writes `02AEDFC0` (immune-by-kind) |
| `0038E770` | 134 | *ChargeMpByLevel* — MP gain `= L` or `L + (RNG%L)/2` | `0038E789` writes `02AEE010` |
| `0038E7C0` | 135 | *SouleaterStrikeAtTenthOfOwnHp* — ×2.0 gain on `0xD`, ×1.7 loss else; source pays cap/10 | `0038E7CB` `subss` `02AEE05C` |
| `0038E950` | 140 | *BonecrusherGamble* — `r<55` ⇒ target to 0 HP, source loses `RNG % HP`; else source falls | `0038E959` calls `00379CD0` |
| `0038E9D0` | 141 | *TelekinesisAttackTimesRandomLevel* — loss = source Attack × (`RNG % (L×100)`)/100 | `0038E9E4` `movss` from `008F30E4` |
| `0038EA60` | 142 | *SetTargetHpToMaximumIfKo* — KO + source≠target ⇒ HP absolute = cap | `0038EA85` writes `02AEE02C` |
| `0038EB30` | 145 | *LossRowPowerTimesRowByte11* — loss = `row+0x11` × `row+0x10` | `0038EB3A` reads `02EBF138` |
| `0038EE10` | 148 | *DrainTargetHpToSource* — target loss `= v`, source gain `= v` | `0038EE18` `mulss` `02AEE058` |
| `0038EF60` | 151 | *GainAttackMinusDefenseToBoth* — no shipped action row | `0038EF6B` `subss` `02AEE05C` |
| `0038EFB0` | 152 | *SwapTargetHpAndMp* — the Invert step | `0038EFBD` writes `02AEE030` |
| `0038F060` | 153 | *LossPercentOfTargetMaxMp* — fails at MP 0; loss `= min(9999, power × maxMP/100)` | `0038F070` writes `02AEDFBC` |
| `0038F120` | 154 | *SetTargetMpToPercentOfMaximum* — MP absolute = `power × maxMP / 100`, 0 under layer id 39 | `0038F13E` reads `02EBF138` |
| `0038F1B0` | 155 | the second MP-percent step — `row +0x10` byte × target max MP `+0x28` / 100 → MP absolute `02AEE030`, then the Disease/Bubble cap chain | `0038F1D8` reads `02EBF138` |
| `0038F2D0` | 156 | *GainRowPowerTimesRowByte11* — gain = `row+0x10` × `row+0x11` (Charge) | `0038F2DA` reads `02EBF138` |
| `0038F380` | 157 | *EndChainOnSelfTarget* — source == target ⇒ roll over | `0038F393` writes `02AEDFB8` |
| `0038F3A0` | 158 | *GainPercentOfTargetMaxHp* — HP absolute `= HP + power × cap/100` | `0038F3D8` reads `02EBF138` |
| `0038F4C0` | 159 | *GainPercentOfTargetMaxMp* — MP absolute `= MP + power × maxMP/100` | `0038F4E1` reads `02EBF138` |
| `0038F890` | 165 | `BattleFormula_ApplyTargetHpPostMultipliers` | `0038F895` reads `02AEE004` |
| `0038F8E0` | 166 | post-multiplier HP-loss adjustment — reads and rewrites `02AEE004`, const `008F3134` | `0038F8E4` reads `02AEE004` |
| `0038FCC0` | 181 | `BattleFormula_CalcApplyCandidateStatusesRequired` — `r9d=1` stub tail-jumping `00387CB0` | `0038FCC6` `jmp 00387CB0` |
| `0038FCD0` | 182 | `BattleFormula_CalcApplyCandidateStatusesOptional` — `r9d=0` stub tail-jumping `00387CB0` | `0038FCD3` `jmp 00387CB0` |

### How this answers the damage pipeline's shape

[`../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md`](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md)
establishes `damage = trunc((attack − defence) × multiplier)` and flags that 45 functions rewrite the
shared scratch record between preparation and the finalizer. **This table is why that chain is not
fixed control flow.** The preparation step, the modifier steps and the finalizer are separate table
entries, so the sequence — and therefore which modifiers apply — is **authored per action**, not
compiled in.

Neither the `Prepare*` functions nor the finalizer has a single direct caller anywhere in `.text`:
they are reached **only** through this table.

## 3. Key addresses

| Address | Role |
|---|---|
| `0x01EFA5C0` | **step table base** (`.data`), 8-byte stride, 202 slots |
| `0016D6A0` | the shared `ret 0` no-op that 42 slots point at |
| `0038AAF0` | slot 65 and 76 — `PrepareStrengthAttackVsDefense` |
| `0038A110` | slot 66 — `PrepareSpeedStrengthAttackVsDefense` |
| `0038D280` | slot 113 and 125 — `FinalizeTargetHpMagnitude` |
| `0038B6A0` | slot 95 — `ApplyActionElementAffinity` |
| `0038BE30` | slot 99 — `ApplyEquipmentElementAffinity` |
| `00390680` | slot 196 — `SelectPoachRewardItem95_5` |
| `02AEE054`–`5C` | the shared scratch record the steps read and write |

## 4. Data structures and formulas

```
stepTable  = (void (**)()) 0x01EFA5C0
step(id)   = stepTable[id]                 /* id in 0 .. 201 */

populated  = 202          all slots are valid .text pointers
distinct   = 152          some ids share a target
no-op      = 42           slots whose target body is `ret 0`
```

## 5. Call chain

```
authored action data  ->  a recipe: a sequence of step ids   [interpreter NOT read]
                              |
                              v
                       stepTable[id]  @ 01EFA5C0 + id*8
                              |
      .-----------------------+------------------------.
      v                       v                        v
  65..79 preparation    95..165 modifiers        113/125 finalize
  writes 02AEE054/58/5C   rewrite the same slots   reads them -> damage
```

## 6. Modding notes

- **This is the primitive catalogue.** Any change to how an action computes damage is a change to
  which step ids it names, not to code — provided the behaviour you want already has a slot.
- **An id is not an identity.** Six targets are reachable by two or three ids each; do not assume a
  one-to-one mapping when reading authored data.
- **42 ids are no-ops.** A recipe naming one of them is well-formed and does nothing. That is a
  plausible way authored data disables a step without restructuring a list.
- **The table is in `.data`, not `.rdata`** — it is writable at runtime. A step can therefore be
  repointed in memory without patching call sites, which makes this the single highest-leverage
  hook point in the combat maths.
- **XIIOnline:** step selection is authored data and identical across clients; the *rolls* inside
  the steps are not. Steps named `Roll*` consume RNG, so two clients diverge unless the stream is
  shared. Synchronise the RNG, not the outcome.

## 7. What is not known

- [x] ~~The interpreter.~~ **ALREADY ANSWERED, in the database, before this document was written** —
      `ranged-weapon-recipes.md` records the dispatcher `BattleFormula_ResolveTargetResult`
      (`00385F60`) and the recipe format. Raising it here was an error. **AK-1.**
- [x] ~~Where recipes are stored.~~ **ALREADY ANSWERED** — recipe pointer table `0x01EF96C0`,
      109 entries, each two `-1`-separated lists of signed 32-bit slot ids. **AK-2.**
- [x] ~~How the recipe path resolves a slot id to a pointer.~~ **ANSWERED 2026-09-02** —
      `call qword ptr [rbx + slotId*8 + 0x1DDA5C0]` inside `BattleFormula_ResolveTargetResult`,
      with `rbx` = image base `00120000`, so the displacement is the table's **RVA**. Section 11.
      **AK-7.**
- [x] ~~What the remaining `FUN_*` steps do. 44 of 202 slots carry a recovered name (35, plus the nine preparation variants named 2026-09-11).~~ **AK-3 ANSWERED 2026-09-12 (FABLE):** every body a shipped recipe names is read or named on a page (the catalogue note and the pages it cites), and the two bodies no recipe names (118, 131) are read there too; what remains `FUN_*` is the GFZ symbol table, not the database. **AK-3.**
      *Narrowed 2026-09-12 (FABLE):* eleven more bodies / fifteen more ids read — 0, 11, 21, 31, 32,
      40 / 45 / 46, 47, 61 / 64 / 75, 92, 93, 170 (the note under the catalogue); with the 2026-09-12
      chain reads (22, 33, 34, 96–99, 166, 171, 176, 182) the recipe-used residue is 94, 62 and 119 —
      *and later:* 119 read (the percent-of-max-HP finaliser), 62 already named on the attack-defense
      page; 94 is on the weather / terrain page; nine single-recipe bodies read (4, 112, 124, 133, 134,
      142, 148, 151, 157); the exact residue is seventeen recipe-used bodies no page cites (listed
      under the catalogue).
- [x] ~~Whether ids are allocated in pipeline order, or the apparent ordering is coincidence.~~
      **AK-4 answered 2026-09-18 (OPUS) — the ordering is not coincidence, and two independent
      lines say so.** See §12b.
- [x] ~~Whether the 42 no-op slots were authored as no-ops or are folded distinct functions.
      `/OPT:ICF` is the likely cause but is inferred, not read.~~ **AK-5 closed 2026-09-12 (FABLE) —
      undecidable from the image, and here is exactly why.** All 42 no-op slots hold the **same**
      pointer, `0016D6A0`, the three-byte `ret 0` that the linker folded some 273 empty bodies onto
      (BQ-27); a table authored with one shared `Nop` function and a table of 42 distinct empty
      functions folded by `/OPT:ICF` produce byte-identical output, so no static reading can separate
      them. What the bytes do settle: **four of the no-op ids are live** — the shipped recipes
      (`01EF96C0`, [the count-clock page](../Recipe-System/the-count-clock-and-bank-recipes.md)) name slot **28 ten times** and slots 193, 198 and 199 once each — so
      a reconstruction must keep those ids as callable no-ops, whatever their history.
- [x] ~~Why `FinalizeTargetHpMagnitude` and `PrepareStrengthAttackVsDefense` each have two ids.~~
      **AK-6 answered as far as the image can 2026-09-12 (FABLE): both ids of every pair are live
      aliases.** The 202-slot table has 152 distinct targets; seven targets carry two or three ids —
      `00388FE0` (23, 24), `00389670` (40, 45, 46), `00389F80` (60, 63), `0038AA90` (61, 64, 75),
      `0038AAF0` (65, 76), `0038D280` (113, 125), `0038F5A0` (115, 160) — and the 109 shipped recipes
      reference **every one of those ids** (23 ×2 / 24 ×1; 40 ×11 / 45 ×2 / 46 ×1; 60 ×3 / 63 ×1;
      61 ×1 / 64 ×5 / 75 ×1; 65 ×3 / 76 ×3; 113 ×6 / 125 ×12; 115 ×1 / 160 ×1). So none is a dead
      renumbering: the recipes were authored against both numbers, and the step function behind each
      pair is the same body. The *why* (a renumbering that kept old ids, or deliberate aliases) is
      authoring history the image does not carry.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Base `0x01EFA5C0`, 8-byte stride | solved independently from two previously documented bindings (slot 65 and slot 66) which agree; reading the table reproduces both | 1 |
| 202 consecutive populated slots, no nulls | qword walk from the base until the first non-`.text` value | 1 |
| 152 distinct targets, 42 no-ops, 35 named | attribution of every slot against `functions.tsv` | 1 |
| The no-op target is a bare return | disassembly of `0016D6A0`: `c2 00 00` = `ret 0`, then `int3` padding | 1 |
| The `Prepare*` family and the finalizer are reached **only** via this table | `.text` byte scan: **0** `E8` call sites and **0** `E9` thunks to `0038AAF0` or `0038D280`; their addresses appear only as `.data` qwords | 1 |
| The named catalogue and its slot ids | direct read of the table, joined to `functions.tsv` | 1 |
| CFG is compiled but disabled in this image | [`../../24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`](../../24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md) | 2 |

**Scope honesty:** this document establishes **what can be called and by which id**. It does not
establish that anything walks a list of ids at runtime — the interpreter is unread, and the word
"recipe" is carried over from the ranged-weapon document, which established two bindings but not the
execution model.

## 9. Related

- [`../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md`](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) — the steps at 65–79 and the finalizer at 113
- [`../Recipe-System/ranged-weapon-recipes.md`](../Recipe-System/ranged-weapon-recipes.md) — the two slot bindings that fixed this table's base
- [`../Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md`](../Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md) — scaling applied in the same pipeline
- [`../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md) — where authored action data lives

## 10. Falsification pass 2026-09-02 — two errors, both mine

**Attack chosen.** This document was written in the previous tick and makes a strong structural
claim. The obvious attacks are its **base derivation** and its assertion that the sequence is
authored rather than compiled. Both were run. The base survives — but not for the reason the
document gave — and the surrounding claims needed real correction.

### CORRECTED: the original base derivation was numerology

The document argued the base was confirmed because two bindings agreed:

```
01EFA7C8 - 65*8 = 01EFA5C0
01EFA7D0 - 66*8 = 01EFA5C0
```

**Those are not two independent constraints.** The two functions are adjacent in the array (8 bytes
apart) and their ids differ by exactly 1. Any two such points solve to the same base **by
construction** — the agreement was guaranteed before any data was looked at, and would have appeared
identically for a wrong base. It is one equation written twice.

The base *is* right, and section 2 now says why: the Bow recipe's **eleven** slot ids all resolve to
semantically appropriate steps, in pipeline order. That is a genuine over-determination.

**The lesson is the one the evidence standard already carries about positive controls:** two
measurements that cannot disagree are not corroboration. Before citing agreement, ask whether
disagreement was possible.

### CORRECTED: the interpreter was already documented

This document said the interpreter "has not been located" and raised **AK-1** and **AK-2** as new
open questions. Both were substantially answered in a sibling document already in the database:
`ranged-weapon-recipes.md` records a **recipe pointer table at `0x01EF96C0` with 109 entries**, each
recipe holding **two `-1`-separated lists of signed 32-bit slot numbers** (preview and committed),
dispatched from `BattleFormula_ResolveTargetResult` (`00385F60`).

**Failing to check the database's own contents before declaring something unknown is a defect**, and
a more embarrassing one than a wrong number: it manufactures work and it understates what the
database knows. AK-1 and AK-2 are corrected accordingly.

### CONFIRMED, and sharper than claimed: two access paths, not one

A full disassembly-level scan of every known function for references into the table's 202-slot range
finds exactly **24 instructions**: **22 `call qword ptr [rip+disp]`** and **2 `jmp qword ptr
[rip+disp]`**, across **six** functions — and **zero indexed accesses** of the form
`[reg*8 + base]`.

| Function | Slots it names |
|---|---|
| `FUN_00388250` | 0, 20, 31, 32, 40 |
| `FUN_003889F0` | 0, 24, 37, 46 |
| `FUN_00390190` | 24, 37, 46, 180, 181 |
| `FUN_00390240` | 24, 37, 46, 180, 181 |
| `BattleFormula_ResolveCandidateStatusApplications` | 118 |
| `FUN_0038FCE0` | 118 |

So the array is reached **two different ways**:

1. **Compiled fixed sequences.** These six functions call specific slots at fixed displacements —
   `FUN_00388250` runs slots 0, 20, 31, 32, 40 in order with an abort check between each. That
   sequence is in the code, not in data.
2. **Recipe-driven**, per the sibling document — which must resolve slots dynamically, and therefore
   through a path that does *not* appear as a RIP-relative reference to the array.

The document's original claim that the sequence is "authored per action, not compiled in" was
therefore **half right**: it is true of the recipe path and false of these six. Both exist.

### Why the indirection is the point

Every one of the 24 sites is an **indirect** call or jump through a writable `.data` pointer, even
where the slot is fixed at compile time. Combined with the array being in `.data` rather than
`.rdata`, that means a step can be repointed at runtime and *every* caller follows — the fixed
sequences included. The original document's modding note stands, and this strengthens it.

### Not changed

The table's base, stride, extent, 152 distinct targets, 42 `ret 0` no-ops and the named catalogue
were all re-derived and are unchanged.

## 11. Falsification pass 2026-09-02 (second) — AK-7 answered, and the base finally over-determined

**Attack chosen.** Pass 33 left a sharp anomaly: recipes are lists of slot ids, yet a full
disassembly scan found **zero** indexed accesses to the table. Either the recipe model was wrong or
the scan was blind. **The scan was blind**, and finding out why is the useful part.

### The interpreter, read

> **A second interpreter site (added 2026-09-14, FABLE, `AS-11`).** The step table is also run by
> `BattleFormula_EvaluateTargetPreview` (`00385680`), which is reached from `BattleAction_EvaluateTargetPreviews` (`00303830`)
> and `BattleAction_EvaluateTargetPreviewRecursive` (`00303A00`). Its loop is the same indirect call through the image
> base, `call [r12 + rax*8 + 0x1DDA5C0]` at `003859FF`, with the same argument shape (`rcx`, `rdx`, a scratch pointer in
> `r8`) and the same abort flag `02AEDFB8` (`00385A07`). **Two differences:**
> - **The count.** It is found by scanning the slot list to its `-1` terminator (`003859C5`–`003859DB`) rather than
>   passed in.
> - **What follows.** Afterwards it writes bit 2 of `+0x18` from `02AEDFC4` (`00385A1C`–`00385A2D`).
>
> So the recipe executes on two paths: the committed result below, and a preview of the same recipe for target
> evaluation.

Inside `BattleFormula_ResolveTargetResult` (`00385F60`):

```
003863A3  lea    r13, [r9 + rax*4]                  ; r13 = &slotList[0]   (int32 entries)
003863AB  test   r8d, r8d / jle  done               ; r8d = entry count
003863B0  lea    rbx, [rip - 0x2663b7]              ; rbx = 00120000  <- the IMAGE BASE
  loop:
003863C0  movsxd rax, dword ptr [r13 + rbp*4]       ; slotId = slotList[i]   (SIGNED)
003863C5  lea    r8,  [rsp + 0x48]                  ; arg3 = result/scratch
003863CA  mov    rdx, rsi                           ; arg2
003863CD  mov    rcx, r14                           ; arg1
003863D0  call   qword ptr [rbx + rax*8 + 0x1dda5c0]  ; stepTable[slotId](arg1, arg2, arg3)
003863D7  cmp    dword ptr [rip + 0x2767bda], 1     ; 02AEDFB8 — abort flag
003863DE  je     done                               ; a step set it: stop the recipe
003863E0  inc    rbp
003863E3  cmp    rbp, r12 / jl loop
  done:
003863F8  call   0x390f20                           ; ApplyTargetStatusActionPostModifiers
```

Five things follow directly:

1. **Every step has the same signature** — three arguments in `rcx`, `rdx`, `r8`, reloaded before
   each call. A step is a uniform plug-in, which is what makes one flat table workable.
2. **Slot ids are signed** (`movsxd`), consistent with the `-1` list terminator the recipe format
   uses.
3. **Steps can abort the recipe.** After every call the loop tests a global at `02AEDFB8` for `1`
   and stops if set. A miss, a guard, or an immunity therefore ends the pipeline early rather than
   running the remaining steps and discarding the result.
4. **One step runs unconditionally afterwards** —
   `BattleFormula_ApplyTargetStatusActionPostModifiers` (`00390F20`), outside the loop and outside
   the abort check.
5. The same abort convention appears in the compiled fixed sequences found in pass 33
   (`cmp dword ptr [rip+…], 0 ; jne`), so both access paths share one early-out protocol.

### The base, over-determined at last

```
rbx        = 003863B0 + 7 - 0x2663B7 = 00120000        (the image base)
effective  = rbx + slotId*8 + 0x01DDA5C0
base       = 00120000 + 01DDA5C0     = 01EFA5C0        MATCH
```

This is the third derivation and the first two were unequal in quality:

| # | Source | Independent? |
|---|---|---|
| 1 | two adjacent slot bindings, ids differing by 1 | **No** — agreement guaranteed by construction (pass 33) |
| 2 | the Bow recipe's eleven ids all landing on apt steps | Yes |
| 3 | **the dispatcher's own addressing arithmetic** | Yes, and exact |

### Why the earlier scan found nothing — a third instrument blind spot

The address is assembled as **image base (in a register) + RVA (as the displacement)**:

```
call qword ptr [rbx + rax*8 + 0x1DDA5C0]
                             ^^^^^^^^^^ an RVA, not a VA
```

Pass 33 searched for RIP-relative targets inside the table, and for `[reg*8 + disp]` where the
displacement was the **virtual address**. This form is neither. Nothing was wrong with the logic;
the pattern simply was not in the search space.

That is now the **third** distinct blind spot this database has recorded in its own tooling:

- an edge list that sees `E8` but not `E9` (battle-runtime-mode ladder)
- a caller census blind to address-taken references (action availability)
- **an address scan blind to base-register + RVA addressing** (here)

All three share a shape: *a census that answers a narrower question than the one being asked.* The
standing rule that follows is to state, when reporting a zero, **which encodings were searched**.

### Status

The table's structure, the recipe format and the interpreter are now all read. **AK-7 is closed**;
the document moves to `DOCUMENTED`. What remains open is the meaning of the 125 unnamed steps
(**AK-3**), not the mechanism.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

`RNG_MT19937_NextU32_Thunk` (`00379CD0`), the gameplay MT draw this page cites, has callers in three other layers:

- **CoreRuntimeScheduling — SERVICE, with a determinism consequence.** The boot frame modes 0 and 1 (255 B and 219 B)
  each draw once per dispatch and discard the value. The formula rolls therefore start from a stream that boot has
  already advanced ([the generator contract](../../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md) §6 note).
- **Rewards_Progression_Economy — CLIENT.** The HP and MP growth functions (178 B and 171 B) draw it for the level-up
  bonus ([what happens when a character levels up](../../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md)).

The remaining CoreRuntimeScheduling edges are the image-address resolver fan-out, which is MECHANICAL.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatAction — CLIENT and SERVICE, 17 edges.** The step table's functions are called by `BattleAction_EvaluateTargetPreviews` (3), `BattleAction_EvaluateTargetPreviewRecursive` (3), `BattleUnit_AdvanceStandardActionState` and two action bodies (140 and 722 bytes). They call `BattleAction_EvaluateTargetPreviewRecursive` (2).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Movement — CLIENT.** `FUN_0033cb10`, owned by that layer, calls `0031B860` on this page. That caller is an 89-byte row resolution on the same two definition tables the combat layer uses - `0208D480` by `byte[+4]` when `byte[+5] == 0`, the owning unit's table otherwise - reached from the movement side; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — SERVICE (4 edges).** The unit-class splitter `002F8E90` calls `ActorRuntime_GetClassNibble` `00263C20`; `BattleAction_EvaluateTargetPreviews` `00303830` calls `ActorWork_GetBattleUnit` `0031B760`; `BattleStats_FindOwningBattleUnit` `0031B860` walks the unit table through `BattleUnit_GetBySlotIndex` `00236820` and `BattleUnit_GetSlotCount` `00236850`. The step table's helpers read actors only through that layer's accessors: the splitter needs the actor class to tell an enemy-table unit of class 3 from the rest (slots 4 and 93 above), and the owner resolver finds which battle unit holds a stats record.

**Items_Equipment_Shops_License — CLIENT (4 edges).** `BattleStats_SetEquipmentSlotByStatsIndex` `0031A410`, `BattleStats_SetEquipmentSlotByMappedId` `0031A510`, `BattleStats_SetEquipmentSlotDirect` `0031A630` and `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` call `0031B860`. Equipping an item and learning a licence node locate the stats record's owning battle unit through the same resolver the no-caller step members use; nothing in that layer reaches the step table itself.

**Script_VM_Native_Bridge — CLIENT, OUT-OF-SCOPE (2 edges).** The script verb bodies `00354BF0` and `00355140` call `RNG_MT19937_NextU32_Thunk` `00379CD0`. Script verbs draw from the same shared MT19937 stream the hit and damage rolls use; that is fan-in on the generator, not a script route into any step.

**Status_Periodic_Terminal — CLIENT and SERVICE (9 edges).** `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860` calls the splitter `002F8E90` and `0031B860`; `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400`, `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690` and `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` call `0031B860`; `BattleFormula_AdvanceStatusTimersAndBuildResult` `00386C70` calls `00379CD0`; the periodic tick `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls the interpreter `BattleFormula_ResolveTargetResult` `00385F60`; and the id-118 caller `0038FCE0`, which writes the result's apply mask, calls `BattleStatus_ComputeDefaultDwordParameter` `00387730`. The status layer shares this table's machinery in both directions: its tick resolves a periodic result through the same interpreter that runs the step recipes, its bodies use the same owner resolver and generator, and the status-adding step asks that layer for a status's default parameter.

**WorldAreaField — CLIENT, OUT-OF-SCOPE (2 edges).** The weather bodies `0025ABA0` and `0025ACA0` call `00379CD0`. The weather roll is another caller of the shared generator; it shares the stream with the step rolls and nothing else.

## 12b. AK-4 — the ids are the pipeline order, read from the table and from the recipes (2026-09-18, OPUS)

**The question.** *Whether ids are allocated in pipeline order, or the apparent ordering is
coincidence.* Two things had to be separated: the order the bodies were **written** and the order
they are **run**. The table answers the first, the recipes answer the second, and only together do
they settle the question — a file authored in pipeline order and a file whose ids merely track its
own layout produce the same table.

### Line 1 — the table is one translation unit emitted in order

Reading the 202 slots at `0x01EFA5C0`:

| measurement | value |
|---|---|
| slots holding the folded `ret 0` at `0016D6A0` | **42** |
| live entries | **160** |
| Spearman ρ(id, body address) over the 160 | **0.9963** |
| adjacent id pairs ascending in address | **152** of 157 |
| random assignments of the same addresses reaching \|ρ\| ≥ 0.9963 | **0 of 20,000** |
| body address span | `00387F40`–`003908A0`, 35,168 bytes |
| functions in that span | **151**, of which **foreign: 0** |

**The control is the 42.** That figure is AK-5's, published 2026-09-12, and reproducing it from the
bytes is what establishes this is the right table read the right way before anything is concluded
from it.

The span contains **no function that is not a step body**, so this is a single translation unit laid
out in order. All five inversions — where the id ascends and the address goes backwards — are
re-references to an earlier body in the same unit, and two of the five are the duplicate-id pairs
this page already documents (`PrepareStrengthAttackVsDefense`, `FinalizeTargetHpMagnitude`).

### Line 2 — the shipped recipes execute the ids in ascending order

The 109 recipes at `0x01EF96C0` are pointer entries to **two `FFFFFFFF`-terminated `u32` lists**
each, naming **563** step ids in execution order. Adjacent pairs within a list:

| | count |
|---|---|
| ascending | **421** |
| descending | **10** |
| equal | 0 |

**97.68 % ascending.** The ten descents are not noise and are listed rather than averaged away —
recipe 30 `[16, 6]`, recipe 36 `[15, 4, 130, 180]`, recipe 63 `[… 95, 89 …]`, recipes 65 and 66
`[77, 102, 97, 95, …]`. A pipeline with a few deliberate back-edges is exactly what that looks like.

**So the ordering is not coincidence.** The ids are the pipeline sequence, and the bodies were
authored in that sequence in one file.

### What the counts do NOT establish, checked rather than assumed

The recipes name **160 distinct ids** and there are **160 live slots**, and it is tempting to read
that as "every live step is used". **It is not the same set.**

- Four recipe ids land on **no-op** slots: **28, 193, 198, 199** — exactly the four this page's AK-5
  note already records as live no-ops, reproduced here independently.
- Four **live** slots are named by **no recipe at all**: **37, 73, 118, 131**.

Equal counts are not an identity, and the four live bodies no recipe names are a reachability
question this page did not previously ask.

### 12b.1 — corrected the same day (2026-09-18, OPUS): two of the four are reached, and by a third route

~~the four unreached live bodies~~ — **the word *unreached* was mine and it was wrong for half of
them.** Sweeping every rip-relative `call`/`jmp` whose target lands anywhere **inside** the table
body (`0x01EFA5C0` … `+0x650`), rather than at its base:

| slot | reached by | sites |
|---|---|---|
| **37** | direct hardcoded calls only, **no recipe** | `00388A9B` and `00388B0D` in `003889F0`; `003901DD` in `00390190`; `0039029B` in `00390240` |
| **118** | direct hardcoded calls only, **no recipe** | `00387EAE` in `BattleFormula_ResolveCandidateStatusApplication` (`00387CB0`); `0038FEC1` in `0038FCE0` |
| **73**, **131** | ~~neither a recipe nor a direct call~~ **REFUTED 2026-09-19, see §12b.2** — both are reachable by the INDEXED dispatch at `003859FF` and `003863D0`, which forms the table as image-base + `0x1DDA5C0` and so can reach any slot | `003859FF`, `003863D0` |

~~**So the residue is two, not four**~~ — **the residue is ZERO as a reachability claim; see §12b.2, which refutes this line.** And there is a **third dispatch route into this table** that
the page did not model: **eleven slots are reached by a direct hardcoded `call`/`jmp` from six
functions**, alongside the recipes and the second interpreter site (`AS-11`).

**Why the first sweep missed it, stated because it is the reusable part.** x86-64 cannot encode an
index register together with a rip-relative operand, so an *indexed* dispatch must first materialise
the table base in a register — and here it never does. There is **no `lea` to `0x01EFA5C0` anywhere
in the image**, and the literal address occurs **zero** times as a 4-byte or 8-byte constant. Every
reference into this table is a rip-relative `call` or `jmp` at a **fixed slot**. Searching for the
base therefore found two functions; the correct population is operands landing anywhere **inside**
the table.

**This vindicates the bound rather than overturning it.** §12b scoped its absence explicitly to the
recipe population — *"no recipe names it" is an absence over the recipe population only* — and the
direct-call route is exactly what that scope was protecting against. The claim was right; the word
around it was not.

*Evidence tier 1 throughout: the step table, the recipe table and the function extents are read from
the shipping image (`73461d08…21f8`). The null model is a permutation test over the same 160
addresses, stated so the correlation is not quoted bare.*

### 12b.2 — corrected again (2026-09-19, OPUS): the base IS materialised, and 73 and 131 are reachable

§12b.1 concluded that slots **73** and **131** are reached by "neither a recipe nor a direct
call", and rested that on a premise stated in the same section:

> x86-64 cannot encode an index register together with a rip-relative operand, so an *indexed*
> dispatch must first materialise the table base in a register — and here it never does. There is
> **no `lea` to `0x01EFA5C0` anywhere in the image**, and the literal address occurs **zero**
> times as a 4-byte or 8-byte constant.

**Both halves of that observation are true. The conclusion drawn from them is false.**

The base is materialised — as the **image base**, with the table's *file-relative* offset riding
in the instruction's displacement:

```
BattleFormula_EvaluateTargetPreview   003859E2  lea  r12, [rip - 0x2659e9]      ; r12 = 00120000
                                      003859FF  call qword ptr [r12 + rax*8 + 0x1dda5c0]

BattleFormula_ResolveTargetResult     003863B0  lea  rbx, [rip - 0x2663b7]      ; rbx = 00120000
                                      003863D0  call qword ptr [rbx + rax*8 + 0x1dda5c0]
```

`0x00120000 + 0x01DDA5C0 = 0x01EFA5C0` — the step table — and
`0x01EFA5C0 − 0x01DDA5C0 = 0x120000` is exactly the image base, which is why no `lea` to
`0x01EFA5C0` and no such constant exist. **They cannot: the address is never formed as a whole.**

So there is an **indexed dispatch into this table after all**, from two functions, with `rax` as
the slot index — and an indexed dispatch can reach **any** slot. The reachability claim for 73
and 131 is refuted, and with it §12b.1's "the residue is two".

**What is refuted and what is not.** Refuted: *"reached by neither a recipe nor a direct call"*
as a statement that nothing reaches them. Not claimed: that any input actually selects 73 or 131.
Whether those indices ever arise is a question about the values `rax` takes, which is a different
instrument and is **not** answered here. "A path exists" and "the path is taken" are different
claims and this section makes only the first.

**This idiom was already documented, three days before §12b.1 was written.**
[`16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`](../../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md) retracted an
identical conclusion on **2026-09-15** (FABLE), on the same instruction shape —
`call qword ptr [rdi + r9*8 + 0x7F64D0]`, `0x00120000 + 0x7F64D0 = 0x009164D0` — and stated the
lesson outright: *"Every one of them looks for the target address… This idiom never materialises
the target: it materialises the image base and reaches everything else by displacement… The fault
was not in any one instrument; it was in believing that five instruments sharing one assumption
are five instruments."* **§12b.1 is dated 2026-09-18.**

So this is **not a new discovery — it is a propagation failure**: a known blind spot, written down
with its own retraction attached, was not applied to the next absence claim three days later.
That is the part worth fixing, and it is why `check_imagebase_relative_refs.py` now exists. The
caveat was documented but not **checkable**, and a caveat nobody can run is one that gets
forgotten.

*A figure that does not reconcile, recorded rather than smoothed over.* The UI page counts **594
functions, 1,411 accesses, 971 distinct addresses**. Re-measuring the same idiom — non-RIP memory
operands with a base or index and a positive displacement that, added to the image base, lands
outside `.text` — gives **254 functions, 1,394 accesses, 485 addresses**. The access counts agree
to about 1 %; the function and address counts differ by roughly two. The likeliest cause is what
an *indexed* operand counts as — one address, or the whole range it spans — but the UI page does
not state its method and I have not reconstructed it, so **neither figure is called wrong here**.
The conclusion both support is unaffected: the idiom is common, and an address-based sweep cannot
see it.

**The reusable part**, and it is the second time today the same shape has appeared: an absence was
established by sweeping one way in. §12b.1 corrected §12b by widening from the table's base to its
whole body; this corrects §12b.1 by noticing that the base can be reached without the base
address ever existing. A sweep for a constant cannot see an address that is computed, and on this
binary — where the image base sits in a register and file-relative displacements are ordinary —
computed is the normal case.
