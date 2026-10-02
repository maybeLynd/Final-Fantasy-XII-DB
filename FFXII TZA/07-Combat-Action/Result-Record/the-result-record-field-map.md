---
system: The result record — the 0x148-byte to-do list a formula resolution produces and the applier consumes, field by field
category: 07-Combat-Action
status: AUDITED
owner_layer: PrimaryOwner:CombatAction (the record's life is resolve → apply → dispatch) — its writers are CombatFormula
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: a typed field scan (hop_scan) seeded at the record's argument registers in the initialiser 003848E0,
    the resolver 00385F60, the applier 003112F0, the metadata applier 00385BA0 and the dispatcher 00469EC0, and
    at the evaluation context in all 152 calculator slots with the record loaded from context +0x10; depth 2;
    control 00385BA0's read at +0x138 found; 245 accesses in 39 functions over 52 offsets; the initialiser
    read to its ret for the defaults and the extent
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-result-record-field-map-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# The result record — what a resolution writes and the applier reads

> Every action against a target produces one record: `BattleFormula_InitializeResultRecord` fills it
> with `-1`s, the resolver and the recipe's calculator slots write the numbers, masks and flags into
> it, `BattleFormula_ApplyTargetResult` walks it as a to-do list, and the metadata applier and the
> post-result dispatcher read what is left. This page is the record itself — 52 offsets with a
> writer or a reader, their types, and the sentinel that means "leave this alone".

## 1. What the player sees

Nothing directly — the record lives for one resolution. But every number the player does see
passes through it: the HP that comes off, the status that lands or lifts, the item stolen, the line
in the battle log. A modder who wants to change what an action *does* after its formula has run
changes this record's fields; a reconstruction must produce the same record for the same formula.

## 2. Native mechanism

### 2.1 Life of a record

| step | function | what it does to the record |
|---|---|---|
| create | `BattleFormula_InitializeResultRecord` (`003848E0`, 205 B) | `memset(+8, 0, 0x140)` (`003848EF`–`003848F5`), then the sentinels: `+0x30` and `+0x11C` = `0xFFFF`, `+0x38`, `+0x3C`–`+0x41`, `+0x42`–`+0x50`, `+0x11E`–`+0x124`, `+0x130`, `+0x138`, `+0x13C` = `-1`, the ~~33~~ **32** dwords from `+0x5C` and the ~~33~~ **32** words from `+0xDC` = `-1` *(corrected 2026-09-29, FABLE: the loop count is `-1 + 0x21` = 32; 33 dwords from `+0x5C` would run into `+0xDC`; `pkg-gp-status-poison/refresh.py` I)* (`00384950`–`00384963`), `+0x2C |= 1` (`0038498D`) — so the record is **at least 0x148 bytes** |
| fill | `BattleFormula_ResolveTargetResult` (`00385F60`) and the recipe's committed calculator slots (reached through the evaluation context's `+0x10`) | the kind `+4`, the flag words `+0x18` / `+0x2C` / `+0x140`, the numbers, the masks, the steal slots, the echoes |
| apply | `BattleFormula_ApplyTargetResult` (`003112F0`) | reads 30 of the 52 offsets — [the applier](../applying-a-result-to-a-target.md) walks them in 20 steps |
| after | `BattleFormula_ApplyResultMetadata` (`00385BA0`), `BattleFormula_DispatchPostResultEvents` (`00469EC0`) | `+0x1C` gates the dispatch; `+0x138` / `+0x13C` go to the battle-state block; `+0x32`–`+0x34` clear the steal bits again; `+0x08`, `+0x24`, `+0x2A`, `+0x2C`, `+0x38`, `+0x58`, `+0x140` pick the battle-log lines |

**`-1` is "leave this alone"** ([the applier](../applying-a-result-to-a-target.md) §"The record is a to-do list"): the
initialiser's sentinels are what an untouched field looks like, and every applier step tests for
them before acting.

> **What a census like this cannot see (2026-09-11, OPUS-NOTICE-CENSUSWRITES).** Seeds: the initialiser's argument registers — a constructor seed — and the resolver's; a record built anywhere else would be outside.
> A scan seeded on *accessors* reaches *consumers*: a constructor that builds the record before
> any accessor can return it is reached only if it is seeded on its own. So the **reads** below are
> the well-covered side and the **writes** are under-covered wherever a constructor or an
> index-derived writer sits outside the seeds — do not rest an absence-of-writer claim on this
> TSV alone; pair it with a displacement scan of the candidate writers.

### 2.2 The field map

| offset | width | type | what | w / r | writers (sites) | readers (sites) |
|---|---:|---|---|---|---|---|
| `+0x000` | 1 | u8 | flag byte: **bit 5** — set by the caller, the resolver clears it when the action row's `+0xC` bit 11 is clear (`00386079`–`00386082`) and, when it survives, skips `BattleFormula_UpdateLowHpThresholdStatusMask` `00385B10` and clears it after (`00386836`–`00386846`); `003908A0` reads the byte | 1 / 3 | `BattleFormula_ResolveTargetResult` `00385F60` (`00386082`) | `BattleFormula_ResolveTargetResult` `00385F60` (`00386029`); `003908A0` (`003908BB`); +1 more |
| `+0x004` | 1 | u8 | **the result kind**: `0` resolved, `6` failed / immune-by-class (`02AEDFBC`, row `+4` bit; `003860A7`, `00386347`, `003866CA`), `9` also runs the slot loop (`0038610B`–`0038611D`), `0xA` immune-by-kind (row `+8` bit, `02AEDFC0`; `00386303`, `003866D7`), **7** the target's defensive layer absorbed it — action `+0xC` bit 14 against Paling (layer id 55) or bit 13 against Magick Shield (layer id 56); `BattleFormula_ApplyPreResolutionTargetGates` `00390AB0` (`00390EF2`) and `BattleFormula_ApplyTargetStatusActionPostModifiers` `00390F20` (`003910A5`), each setting roll-over `02AEDFB8 = 1` (added 2026-09-27, UQ-107), **8** bounced by Reflect — target status 23 with bit 16, source lacking layer id 31, target neither KO nor Stone: `00390AB0` (`00390E35`), the reflected target written to `+0x10`; the outcome rollers `BattleFormula_RollAvoidGuardParryOutcome` `003896B0` and `BattleFormula_RollSpecialGuardOutcome` `00387FD0` write it — **1 / 2** band B evade (plain / with ~~parry~~ counter), **3 / 4** band A evade (plain / with ~~parry~~ counter) *(corrected 2026-10-02, OPUS: `02AEDFC4` is the counter flag, rolled by `003884F0` against `00388490`'s counter chance, which only augment ids 6 "automatically counter" and 7 "Improves chance to counter" make nonzero; combat-formula-step-table.md, the section "The hit pipeline's odds: knockback, counter, combo, the ranged critical and the post-modifiers")*, **5** band C evade, `0xB` special guard ([the scratch block](../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) §2.3) | 5 / 2 | `BattleFormula_ResolveTargetResult` `00385F60` (`003860A7` +1); `BattleFormula_RollSpecialGuardOutcome` `00387FD0` (`0038823B`); `BattleFormula_RollAvoidGuardParryOutcome` `003896B0` (`00389717` +1); +2 more | `BattleFormula_ResolveTargetResult` `00385F60` (`0038610B`); `BattleFormula_DispatchPostResultEvents` `00469EC0` (`00469FFF` +5) |
| `+0x008` | 4 | u32 | **the gil amount the applier deducts** (`GameState_SetGil` `00254EE0` of `max(GameState_GetGil` `00253690` `() − value, 0)`, `00311A84`–`00311A9E`; the dispatcher hands it to the battle log as context `+0x10`, `00469EF7`): `00388D50` charges the **four slot-map units' current HP summed** (stats `+0x48`, `00388DEE`–`00388E18`, capped at 10,000, refused with `02AEDFBC` / `02AEDFB8` and `+0x140` bit 11 when above the party's gil, `00388E1A`–`00388E4F`); `0038F6F0` (step slot 163, the whole committed list of recipe 99 — action `0x103` "gil bug", the "… Your pockets feel lighter" trap) rolls `(mt19937 % actionRow[+0x10] + 1) × (mt19937 % targetLevel + 1)` with the level at target stats `+0x1C2` (`0038F70C`–`0038F7CD`; `n` named 2026-09-12), 0 when the party has no gil (`0038F7D0`–`0038F7E1`) | 2 / 2 | `00388D50` (`00388E57` +1); `0038F6F0` (`0038F7E9`) | `BattleFormula_ApplyTargetResult` `003112F0` (`00311A84`); `BattleFormula_DispatchPostResultEvents` `00469EC0` (`00469EF7` +1); the preview evaluators copy the *preview* record's value to unit `+0xE54` (`00303950`–`00303954`, `00303B2E`) for Consume to deduct — recipe 61's committed slot `0038ED40` never writes `+0x08`, so the gil throw is charged once, by Consume, and the applier's deduction here serves the other writer `0038F6F0` |
| `+0x010` | 8 | unit ptr | **the reflected target's unit pointer** — written only on the Reflect bounce: kind `8` at `00390E35` pairs with `mov qword [result+0x10], 00384F40(source, target, ctx)` at `00390E42`, the nearest eligible unit within the action row's `+0x05`/10 reach (`0038503B`–`003851AF`); initialised `0` by `BattleFormula_InitializeResultRecord`'s `00861EC0` fill over `+8..+0x148` (added 2026-09-27, UQ-107 — `00390E42` is the only writer located) | 1 / 0 | `BattleFormula_ApplyPreResolutionTargetGates` `00390AB0` (`00390E42`) |  |
| `+0x018` | 4 | u32 | **flag word B** — bit 0 ~~the mode-2 resource reaction chance rolled~~ the ranged critical rolled (`003891D9`) *(corrected 2026-10-02, OPUS: `00389140` sets result `+0x18` bit 0 when the weapon row's `+0x1C` exceeds `mt() % 100` (`003891B7`–`003891D9`), and slot 98 `0038BE00` doubles `02AEE054` on that bit: the ranged critical, rolled only by recipes 25–27; combat-formula-step-table.md, the section "The hit pipeline's odds: knockback, counter, combo, the ranged critical and the post-modifiers")*, **bit 1 the combo continues** (`0038887A`), **bit 2 ~~parry rolled~~ counter rolled** (`02AEDFC4`, `00385A2D`) *(corrected 2026-10-02, OPUS: `02AEDFC4` is the counter flag, rolled by `003884F0` against `00388490`'s counter chance, which only augment ids 6 "automatically counter" and 7 "Improves chance to counter" make nonzero; combat-formula-step-table.md, the section "The hit pipeline's odds: knockback, counter, combo, the ranged critical and the post-modifiers")*, **bit 3 knockback rolled** (`02AEDFC8`, `00389741` / `00389805`) ([the scratch block](../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) §2.4); bits 1–3 are memoised at preview in the *source's* 64-byte record byte `+0x12` and copied back by the resolver (`003860DF`–`00386108` — "the target's" here before 2026-09-11 was wrong, the record is chosen from the source stats at `003856D3`); kind 6 clears bits 0, 2, 3 and kind `0xA` bit 0 (`003866E3`–`003866EB`); `BattleFormula_RollAndStoreComboCount` `00388660` and `BattleFormula_RollPrimaryFormulaResourceReactionMode2Chance` `00389140` write it; bit 3 gates the knockback scale (`0038680F`) | 5 / 3 | `BattleFormula_ResolveTargetResult` `00385F60` (`003860EC` +2); `BattleFormula_RollAndStoreComboCount` `00388660` (`003886F1` +1); `BattleFormula_RollPrimaryFormulaResourceReactionMode2Chance` `00389140` (`003891D9`); +2 more | `BattleFormula_ResolveTargetResult` `00385F60` (`003860E3` +1); `BattleFormula_RollAndStoreComboCount` `00388660` (`00388891`); +1 more |
| `+0x01C` | 1 | u8 | **the resolved mark** — `1` at `00386855`; `BattleFormula_ApplyResultMetadata` dispatches the post-result events only when it is 1 (`00385C6F`) | 0 / 1 |  | `BattleFormula_ApplyResultMetadata` `00385BA0` (`00385C6F` +1) |
| `+0x01D` | 1 | s8 | a multiplier the applier applies as `target[+0x28] × value` (`003116A6`); the resolver writes `low8(N(02AEDFFC) − N(02AEDFF8))` (`00386655`; scratch §2.7) | 0 / 1 |  | `BattleFormula_ApplyTargetResult` `003112F0` (`003116A6`) |
| `+0x020` | 4 | u32 | the **source's** HP number (`0031172F`; applier step 13) — `N(gain 02AEE018) − N(loss 02AEE014)`, or the absolute `02AEE024` with bit 1 (scratch §2.7) | 0 / 1 |  | `BattleFormula_ApplyTargetResult` `003112F0` (`0031172F`) |
| `+0x024` | 4 | u32 | the target's **HP value** (delta or absolute by `+0x2C` bit 3; `00311620`); the dispatcher's `|delta|` (`00469F01`) — the delta is `N(gain 02AEE008) − N(loss 02AEE004)`, damage negative; the absolute `02AEE02C` (scratch §2.7) | 0 / 2 |  | `BattleFormula_ApplyTargetResult` `003112F0` (`00311620`); `BattleFormula_DispatchPostResultEvents` `00469EC0` (`00469F01` +7) |
| `+0x028` | 2 | u16 | the source's MP number (`0031174F`) — `low16(N(02AEE020) − N(02AEE01C))`, or the absolute `02AEE028` with bit 2 (scratch §2.7) | 0 / 1 |  | `BattleFormula_ApplyTargetResult` `003112F0` (`0031174F`) |
| `+0x02A` | 2 | s16 | the target's **MP value** (`00311673`; absolute by `+0x2C` bit 4) — `low16(N(02AEE010) − N(02AEE00C))`, or the absolute `02AEE030` (scratch §2.7) | 0 / 2 |  | `BattleFormula_ApplyTargetResult` `003112F0` (`00311673`); `BattleFormula_DispatchPostResultEvents` `00469EC0` (`0046A0AC` +5) |
| `+0x02C` | 4 | u32 | **flag word A** — bit 0 set by the initialiser (`0038498D`); bits the applier reads: 1 / 2 absolute source HP / MP, 3 / 4 absolute HP / MP, 7 / 13 source HP / MP present, 8 / 14 HP / MP present, 6 / 10 / 18 / 19 into the target's HP call, 12 / 16 its MP call, 5 / 9 / 17 the source's HP call, 11 / 15 its MP call (corrected 2026-09-11 — the page said 6, 10, 11, 18, 19; [the applier](../applying-a-result-to-a-target.md) steps 10–13), 19 → unit `+0xE9A`, 23 nothing-to-steal (`0039048E`); the resolver ORs bits 5–18 from the formula scratch words (`00386486`–`00386595`, `0038678B`–`0038679C`) — bits 5 / 7 / 9 from the source-HP words, 6 / 8 / 10 the target-HP words, 11 / 13 / 15 the source-MP words, 12 / 14 / 16 the target-MP words, 18 ~~any HP or stat-modifier word~~ **the target-HP loss `02AEE004` or any stat-modifier word `02AEE034`–`02AEE040` only** (`00386564`–`00386595`; corrected 2026-09-11, EXP-059), each `−1` meaning absent; an absolute override then sets 3 / 1 / 4 / 2 and clears 6 / 5 / 12 / 11; **bit 17 = the source's HP present without a gain** (bit 7 set and bit 9 clear, `0038678B`–`0038679C`) — the source's own HP call keeps its alive event only then; **bit 19 = the target is taken, not struck**: set beside a zeroed target-HP absolute by recipe 88's slot 162 (`0038F6DA`, "feeds on"), recipe 9's slot 190 (`0039017E`) and the poach selector (`003907C8`), turned by the applier into unit `+0xE9A` bit 3 (`0031138D`) and the HP write's death event `0x200E`; bit 18 is also set after the status loop (`003866EF`–`00386784`) when **every status the apply mask `+0x54` adds has `status_data` word `+6` bit 13 set and at least one is added** — the same class the unit-definition page's mask `0208D320` collects (the loop walks the 32 bits with `si = 0x2000`, `00386711`–`0038675D`; `r12d` = one in the class, `r15d` = one outside; `00386779`–`00386784`) ([the scratch block](../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) §2.2) | 7 / 2 | `BattleFormula_InitializeResultRecord` `003848E0` (`0038498D` +1); `0038D6B0` (`0038D6E9` +1); `0038EAB0` (`0038EAD5`); +4 more | `BattleFormula_ApplyTargetResult` `003112F0` (`00311384` +5); `BattleFormula_DispatchPostResultEvents` `00469EC0` (`0046A08F` +7) |
| `+0x030` | 2 | u16 | **unused**: initialised to `0xFFFF` (`0038490B`) and touched by nothing else — an image-wide sweep of every instruction addressing `+0x30` over the formula (`00384000`–`00391000`), post-result (`00469EC0`–`0046A0D0`) and target-processing (`00307300`–`00307B30`) code finds the initialiser and three byte reads that belong to the *stats record* (`00389F50`, `0038A446`, `0038E920`, the base the applier carries in `rdi`); the same sweep is the control: it lists the initialiser. FP-3 closed 2026-09-11 | 1 / 0 | `BattleFormula_InitializeResultRecord` `003848E0` (`0038490B` +1) |  |
| `+0x032` | 1 | u8 | **steal slot 0** (common) — the resolver's copy of `02AEE04C` (`003867F8`); the applier adds the item and clears the availability bit; the metadata applier clears the bit again | 0 / 3 |  | `BattleFormula_ApplyTargetResult` `003112F0` (`00311423` +1); `BattleFormula_ApplyResultMetadata` `00385BA0` (`00385C45` +1); +1 more |
| `+0x033` | 1 | u8 | steal slot 1 (uncommon) | 0 / 2 |  | `BattleFormula_ApplyResultMetadata` `00385BA0` (`00385C1B` +1); `0046A870` (`0046A8F6`) |
| `+0x034` | 1 | u8 | steal slot 2 (rare) | 0 / 2 |  | `BattleFormula_ApplyResultMetadata` `00385BA0` (`00385BF0` +1); `0046A870` (`0046A905`) |
| `+0x038` | 4 | i32 | **the poach reward item** — scratch `02AEE050` when flag B bit 3 (`0038680F`–`00386819`); initialised to `-1` (`00384907`); the applier reads it (`0031148D`); the dispatcher passes it as context `+0x20` (`00469F2B`) — the realiser's slot kind 7 | 1 / 2 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384907` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`0031148D` +1); `BattleFormula_DispatchPostResultEvents` `00469EC0` (`00469F2B` +1) |
| `+0x03C` | 1 | u8 | **the first status-layer effect the action adds** (`0xFF` = none; the applier's step 14 sends `+0x3C` / `+0x3D` to the status write in mode 2 = *set*, [the applier](../applying-a-result-to-a-target.md)) — recipe 79's slot 187 `0038FF20` copies the action row's `+0x10` here (`0038FF72`–`0038FF7A`); actions `0x12A`, `0x135`–`0x141`; corrected 2026-09-11 from "statuses to remove" | 2 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384941` +1); `0038FF20` (`0038FF7A`) | `BattleFormula_ApplyTargetResult` `003112F0` (`00311788` +1) |
| `+0x03D` | 1 | u8 | **the second status-layer effect the action adds** — the row's `+0x11` (`0038FFC3`–`0038FFCC`); the same slot then derives both effects' timers into `+0x42` / `+0x44` from the slot-29 parameter table row × 30 (`0038FFD6`–`00390096`) | 1 / 0 | `0038FF20` (`0038FFCC`) |  |
| `+0x03E` | 1 | u8 | **the first of four status-layer effects the action clears** (`0xFF` = none; step 14, mode 0) — recipe 80's slot 188 `003900C0` copies the row's `+0x10` here (`00390110`–`00390118`); recipe 80 is bound to no action in the shipped table; corrected 2026-09-11 from "statuses to remove, high dword" | 2 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384946` +1); `003900C0` (`00390118`) | `BattleFormula_ApplyTargetResult` `003112F0` (`003117E4` +1) |
| `+0x03F` | 1 | u8 | **the second effect to clear** — the row's `+0x11` (`00390157`–`00390164`), by the same action-less slot | 1 / 0 | `003900C0` (`00390164`) |  |
| `+0x042` | 2 | s16[8] | **~~the eight status duration timers~~ the eight effect-slot timers (stage 3's countdown, keyed by the effect table; not the 32 statuses' durations, which are `+0xBC`)** *(renamed 2026-09-29, FABLE; `_index/candidates/pkg-gp-status-poison/timers.md`)* written straight into the target's `+0x17C` array (`0031181B`–`0031188B`); `0038FF20` sets the first | 2 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384965` +1); `0038FF20` (`00390083`) | `BattleFormula_ApplyTargetResult` `003112F0` (`0031181B`) |
| `+0x044` | 2 | s16 | timer 1 | 1 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`0038496A` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`0031182B`) |
| `+0x046` | 2 | s16 | timer 2 | 1 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`0038496F` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`0031183B`) |
| `+0x048` | 2 | s16 | timer 3 | 1 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384974` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`0031184B`) |
| `+0x04A` | 2 | s16 | timer 4 | 1 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384979` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`0031185B`) |
| `+0x04C` | 2 | s16 | timer 5 | 1 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`0038497E` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`0031186B`) |
| `+0x04E` | 2 | s16 | timer 6 | 1 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384983` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`0031187B`) |
| `+0x050` | 2 | s16 | timer 7 | 1 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384988` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`0031188B`) |
| `+0x054` | 4 | u32 | **the apply mask** — 32 statuses to add, with parameters at `+0x5C` / `+0xDC` (`0038FCE0` writes, `003114F2` reads) | 1 / 2 | `0038FCE0` (`0038FE25`) | `BattleFormula_ApplyTargetResult` `003112F0` (`003114F2` +1); `0038FCE0` (`0038FEE0`) |
| `+0x058` | 4 | u32 | **the remove mask** (the applier page's correction) — `BattleFormula_CalcRemoveEligibleCandidateStatuses` `0038FC10` writes it *(and so does the periodic tick's builder, stage 2, for the statuses whose duration ran out and for HP Critical — outside this census's slot seeds, §2.3; added 2026-09-29, FABLE, `_index/candidates/pkg-gp-status-poison/cure.py` W)*; the applier (`0031156A`) and the dispatcher's cured / fades messages read it (`0046A208`, `0046A30A`) | 1 / 2 | `BattleFormula_CalcRemoveEligibleCandidateStatuses` `0038FC10` (`0038FC83`) | `BattleFormula_ApplyTargetResult` `003112F0` (`0031156A` +1); `BattleFormula_DispatchPostResultEvents` `00469EC0` (`0046A208` +3) |
| `+0x05C` | 0 | ~~i32[33]~~ i32[32] *(2026-09-29, FABLE: 32, see the initialiser row; AUDIT-SEM's Q2 review)* | per-status parameter A — the status's **duration** (or the Petrify / Doom count) as the applier hands it to the status write and copies it into the target's `+0xBC` — one dword per bit of the masks, all `-1` at init (`00384950`); the periodic tick's stage 2 writes the decremented values here through a record-relative address ([the status write](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) §2.4a) | 1 / 2 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384950` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`003114FB` +3); `BattleFormula_InitializeResultRecord` `003848E0` (`003848FE` +1) |
| `+0x060` | 0 | i32 | parameter A[1] | 0 / 1 |  | `BattleFormula_InitializeResultRecord` `003848E0` (`00384953` +1) |
| `+0x0DC` | 2 | ~~s16[33]~~ s16[32] *(2026-09-29, FABLE: 32)* | per-status parameter B — the status's **beat timer** (target `+0x13C`), one word per bit, all `-1` at init (`00384957`); stage 2 writes the decremented or reloaded beat here (same page) | 1 / 2 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384957` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`00311507` +4); `BattleFormula_InitializeResultRecord` `003848E0` (`00384916` +3) |
| `+0x0DE` | 0 | s16 | parameter B[1] | 0 / 1 |  | `BattleFormula_InitializeResultRecord` `003848E0` (`0038495B` +1) |
| `+0x11C` | ~~2~~ 1 | ~~u16~~ s8 | **the target's new level** ~~in the low byte~~ (`0xFF` = none): scratch `02AEE044` (`003867DE` `mov byte ptr [rbx + 0x11c], al`; ~~the high byte keeps the initialiser's `0xFF`~~ the byte above is `+0x11D`, the source's level, written at `003867EB`; only the initialiser's word store `0038490F` spans both) *(corrected 2026-10-02, OPUS: the applier reads one byte and sign-extends it, `003113CB`, `003113D2 cmp al, 0xff`, `003113D6 movsx edx, al`)* → `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0030C650`) `(targetStats, level, 0)` (`003113CB`–`003113DF`); initialised to `0xFFFF` (`0038490F`) | 1 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`0038490F` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`003113CB`) |
| `+0x11D` | 1 | u8 | **the source's new level** (`0xFF` = none): scratch `02AEE048` (`003867EB`) → `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth(sourceStats, level, 0)` (`003113E9`–`003113FD`) | 0 / 1 |  | `BattleFormula_ApplyTargetResult` `003112F0` (`003113E9`) |
| `+0x11E` | 2 | s16 | **foe stat delta 0 = the strength modifier** `02AEE034` (`003867A6`) → target `w_08 += v − b_2A` (applier step 16, gated by the target stats' kind byte `+5 == 1`) | 1 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`0038491D` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`003118A1`) |
| `+0x120` | 2 | s16 | foe stat delta 1 = the magick-power modifier `02AEE038` (`003867B4`) → `w_0A += v − b_2B` | 1 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384929` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`003118BF`) |
| `+0x122` | 2 | s16 | foe stat delta 2 = the defense modifier `02AEE03C` (`003867C2`) → `w_12 += v − b_2F` | 1 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384931` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`003118DD`) |
| `+0x124` | 2 | s16 | foe stat delta 3 = the magick-resist modifier `02AEE040` (`003867D0`) → `w_14 += v − b_30` | 1 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384939` +1) | `BattleFormula_ApplyTargetResult` `003112F0` (`003118FB`) |
| `+0x128` | 1 | u8[4] | **affinity bytes OR-ed** into the spawn record's `+0x7B`, `+0x79`, `+0x78`, `+0x7A` (applier step 17) | 0 / 1 |  | `BattleFormula_ApplyTargetResult` `003112F0` (`0031193C`) |
| `+0x129` | 1 | u8 | OR byte 1 | 0 / 1 |  | `BattleFormula_ApplyTargetResult` `003112F0` (`00311964`) |
| `+0x12A` | 1 | u8 | OR byte 2 | 0 / 1 |  | `BattleFormula_ApplyTargetResult` `003112F0` (`0031198C`) |
| `+0x12B` | 1 | u8 | OR byte 3 | 0 / 1 |  | `BattleFormula_ApplyTargetResult` `003112F0` (`003119B4`) |
| `+0x12C` | 1 | u8[4] | **affinity bytes AND-NOT-ed** out of the same four (`003902F0` writes three of them) | 1 / 1 | `003902F0` (`0039031E`) | `BattleFormula_ApplyTargetResult` `003112F0` (`003119DC`) |
| `+0x12D` | 1 | u8 | AND-NOT byte 1 | 1 / 1 | `003902F0` (`0039032F`) | `BattleFormula_ApplyTargetResult` `003112F0` (`00311A06`) |
| `+0x12E` | 1 | u8 | AND-NOT byte 2 | 0 / 1 |  | `BattleFormula_ApplyTargetResult` `003112F0` (`00311A30`) |
| `+0x12F` | 1 | u8 | AND-NOT byte 3 | 1 / 1 | `003902F0` (`00390340`) | `BattleFormula_ApplyTargetResult` `003112F0` (`00311A5A`) |
| `+0x130` | 2 | u16 | **`row +0x10 × 100 + row +0x11`** — recipe 101's slot 200 `003907E0` packs the action row's two parameter bytes for actions `0x6F`–`0x7A` (`00390877`–`00390893`); initialised to `-1` (`00384991`); **read by nothing** — the sweep over `00300000`–`00470000` lists exactly the two writers and no read through any base (other `+0x130` hits in that range are locomotion and presentation structures), so the packed parameter of actions `0x6F`–`0x7A` is computed and never consumed by the shipped code; FP-3 closed 2026-09-11 | 2 / 0 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384991` +1); `003907E0` (`00390893`) |  |
| `+0x138` | 4 | i32 | **echo B — the streak count** (recipe 56, slot 49 `00389C60`: `count + 1` on a passed roll at `00389D58`, `0` on a miss or at 17, [the streak](../../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md) §2.2); the metadata applier copies it, when not `-1`, into the battle-state block's `+0x5B0E` (`00385BAF`–`00385BD1`) | 2 / 1 | `BattleFormula_InitializeResultRecord` `003848E0` (`00384999` +1); `00389C60` (`00389D58`) | `BattleFormula_ApplyResultMetadata` `00385BA0` (`00385BAF` +3) |
| `+0x13C` | 4 | i32 | **echo A — the walked distance modulo 1000 at this use** (recipe 60, slot 146 `0038EBE0` at `0038ECBC`, [the walk](../../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md) §2.3); the applier also writes it (`003115F8`); the metadata applier copies it into the block's `+0x5B00` (`00385BD7`–`00385BEA`) | 3 / 1 | `BattleFormula_ApplyTargetResult` `003112F0` (`003115F8`); `BattleFormula_InitializeResultRecord` `003848E0` (`003849A0` +1); `0038EBE0` (`0038ECBC`) | `BattleFormula_ApplyResultMetadata` `00385BA0` (`00385BD7` +1) |
| `+0x140` | 4 | u32 | **flag word C**: bits 8 / 9 / 11 / 10 → technick notices `0x36` / `0x38` / `0x3A` / `0x3D` (the dispatcher, `00469F68`–`00469FDB`); bit 14 → sound `0x34` (applier step 2); bit 4 → the status loop's flag; ten writers, the outcome and element functions (`00388990`, `003889C0`, `00388D50`, …); the resolver clears bits 4–7 at the end (`00386849`) | 10 / 3 | `00388990` (`003889AF`); `003889C0` (`003889E2`); `00388D50` (`00388E45`); +7 more | `BattleFormula_ApplyTargetResult` `003112F0` (`00311394` +2); `0038E080` (`0038E224`); +1 more |

### 2.3 What the scan does not reach

The record is passed by register and through the evaluation context; the scan seeds cover the
five named holders and all 152 calculator slots, and follows one further hop. What it cannot see:
fields written through pointers the slots store elsewhere, and anything a slot reaches through a
second context hop. The untouched ranges — `+0x0C`–`+0x17`, `+0x61`–`+0xDB` (parameter A entries
2–32 are reached by index, so they show at `+0x5C` / `+0x60`), `+0xDF`–`+0x11B` (parameter B
likewise), `+0x132`–`+0x137`, `+0x144`–`+0x147` — are stated with that limit. ~~**The record's true
allocation is not established**; `0x148` is the initialiser's reach (`FP-2`).~~ **The record is a
`0x148`-byte stack local, every time (FP-2, answered 2026-09-11).** All five callers of the
resolver pass a frame slot in `r9` — `Battle_ProcessActionTarget` `rsp + 0x50` (`00307408`,
`00307563`; frame `0x1C8`), `BattleFormula_QueryResolvedScalarPreview` `rsp + 0x20` (`00308BD5`;
frame `0x180`), `BattleUnit_RunPeriodicCombatMaintenance` `rsp + 0x40` (`00311223`; frame
`0x1E0`), `BattleUnit_HandleActorTimelineEvent` `rsp + 0x20` (`0031A0BE`; frame `0x180`),
`BattleAction_ResolveSpecialSequenceTargets` `rsp + 0x20` (`0030EC95`; frame `0x198`) — as do
the two callers of the preview evaluator (`003038FB` `rsp + 0x30`, `00303AC2` `rsp + 0x50`), and
three of them `memset` exactly `0x148` bytes first (`00308BBD`, `00311214`, `0030EC83`), as the
status write does for its own record ([the status write](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md)
step 1). No heap allocation and no global instance exist; nothing lives above `+0x147`.

## 3. Key addresses

| address | size | what |
|---|---:|---|
| `003848E0` | 205 B | `BattleFormula_InitializeResultRecord` — the defaults and the extent |
| `00385F60` | 2,302 B | `BattleFormula_ResolveTargetResult` — kind, flag words, the steal copy, the resolved mark |
| `003112F0` | 2,040 B | `BattleFormula_ApplyTargetResult` — the consumer |
| `00385BA0` | 250 B | `BattleFormula_ApplyResultMetadata` — echoes, steal bits, the dispatch gate |
| `00469EC0` | 1,904 B | `BattleFormula_DispatchPostResultEvents` — the battle-log reader |
| `0038FCE0` / `0038FC10` | | the apply mask writer / `BattleFormula_CalcRemoveEligibleCandidateStatuses` |
| `0038FF20` / `003900C0` | | the ~~remove-status writers~~ layer-effect writers: `0038FF20` the two to add (`+0x3C`, `+0x3D`, timer 0), `003900C0` the first two to clear (`+0x3E`, `+0x3F`) *(corrected 2026-10-02, OPUS: the applier sends `+0x3C`–`+0x3D` in mode 2 and `+0x3E`–`+0x41` in mode 0, `00311788`–`00311819`)* |
| `00388660` | | `BattleFormula_RollAndStoreComboCount` — writes `+0x18` |
| `003896B0` / `00387FD0` | | `BattleFormula_RollAvoidGuardParryOutcome` / `BattleFormula_RollSpecialGuardOutcome` — write the kind |

## 4. Data structures and formulas

```
ResultRecord (>= 0x148 B; -1 / 0xFFFF = untouched)   # <- corrected 2026-10-02, OPUS - exactly 0x148 B, a stack local at every call site (FP-2, section 2.3)
  +0x00  u8   flag byte (bit 5 low-HP pass skip)   +0x54  u32  apply mask (statuses to add)
  +0x04  u8   kind: 0 ok, 6 failed, 7 Paling/Magick Shield,
              8 Reflect-bounced, 9, 0xA immune      +0x58  u32  remove mask
  +0x08  u32  (context +0x10)                      +0x5C  i32[32] parameter A per status bit   # <- corrected 2026-10-02, OPUS - +0x08 is the gil amount the applier deducts (FP-1, row +0x008)
  +0x10  unit ptr  reflected target (kind 8)
  +0x18  u32  flag word B (bits 1-3 from prefix)   +0xDC  s16[32] parameter B per status bit
  +0x1C  u8   resolved mark                        +0x11C u16, +0x11D u8   # <- corrected 2026-10-02, OPUS - +0x11C is one byte (s8, 0xFF = none), written at 003867DE and read at 003113CB; the word is only the initialiser's 0038490F
  +0x1D  s8   multiplier                           +0x11E s16[4] foe stat deltas (foe only)
  +0x20  u32  source HP; +0x24 u32 target HP       +0x128 u8[4] affinity OR; +0x12C u8[4] affinity AND-NOT
  +0x28  u16  source MP; +0x2A s16 target MP       +0x130 u16
  +0x2C  u32  flag word A (bit 23 nothing to steal) +0x138 i32 echo B -> block +0x5B0E
  +0x30  u16  0xFFFF                               +0x13C i32 echo A -> block +0x5B00
  +0x32  u8[3] steal slots                         +0x140 u32 flag word C (bits 8-11 technick notices, 14 sound)
  +0x38  i32  (context +0x20)   # <- corrected 2026-10-02, OPUS - the poach reward item, -1 = none (row +0x038)
  +0x3C  u16 + u8, +0x3E u32 + u8  statuses to remove   # <- corrected 2026-10-02, OPUS - six bytes, not statuses; +0x3C-+0x3D two layer effects to add (mode 2, the loop of 2 at 00311788) and +0x3E-+0x41 four to clear (mode 0, the loop of 4 at 003117E4), 0xFF = none (00384941, 00384946)
  +0x42  s16[8] effect-slot timers -> target +0x17C   (renamed 2026-09-29 from "status duration timers")
```

## 5. Call chain

```
action commit -> BattleFormula_InitializeResultRecord 003848E0 (defaults)
  -> BattleFormula_ResolveTargetResult 00385F60 (kind +4, flags +0x18/+0x2C, +0x1C = 1)
     -> calculator slots [01EFA5C0] via context +0x10: numbers, masks, timers, deltas, echoes, +0x140
  -> BattleFormula_ApplyTargetResult 003112F0: 20 steps over the record
     -> BattleFormula_ApplyResultMetadata 00385BA0: +0x138/+0x13C -> block, +0x32..+0x34 -> spawn record +0x14, +0x1C -> dispatch
        -> BattleFormula_DispatchPostResultEvents 00469EC0: +0x2C / +0x58 / +0x140 / +0x24 / +0x2A / +0x08 / +0x38 -> battle-log events
```

## 6. Modding notes

- **Change the effect, not the formula**: every applier step tests a field against `-1`; a hook
  that edits the record between resolve and apply changes what lands without touching a formula.
- **Two 32-bit masks and two parameter arrays of ~~33~~ 32** *(corrected 2026-10-02, OPUS: `00384925 lea edx, [r8 + 0x21]` with `r8 = -1` sets the loop count to 32, `00384950`–`00384963`)* — the status space the record can express
  is 32 adds with a dword and a word each, and 32 removes.
- **The foe-only fields** (`+0x11E`–`+0x12F`) are applied only when the target stats' kind byte
  is 1; on a party target they are ignored, which is why the stats union at `+0x10` is safe there.
- ~~**The record is at least 0x148 bytes**; allocate more only if the allocation site says so.~~ *(answered: FP-2 - a `0x148`-byte stack local at every call site, nothing above `+0x147`, section 2.3; 2026-10-02, OPUS)*

## 7. What is not known

- [x] ~~**What `+0x08` is**~~ — **FP-1 ANSWERED 2026-09-11**: the gil amount the applier deducts
  (step 18 of [the applier](../applying-a-result-to-a-target.md)); `00388D50` charges the four
  active units' current HP summed and refuses when the party cannot pay, `0038F6F0` rolls an
  action-scaled random amount. Which actions reach ~~the two writers~~ `00388D50` is not enumerated *(answered for `0038F6F0`: step slot 163, the whole committed list of recipe 99, action `0x103` - the `+0x008` row above and the applier's step 18; 2026-10-02, OPUS)*.
- [x] ~~**The record's allocation size and site** — `0x148` is the initialiser's reach; the caller
  that owns the storage is not read.~~ **FP-2** — ANSWERED 2026-09-11 (§2.3): a `0x148`-byte stack
  local at all seven resolver / preview call sites, three of them zeroed by an explicit `0x148`
  `memset`; no heap or global instance.
- [x] ~~**The meaning of `+0x30`, `+0x11C` / `+0x11D`, `+0x3D` / `+0x3F` and the consumer of `+0x130`**~~ —
  **FP-3 ANSWERED 2026-09-11:** `+0x11C` / `+0x11D` are the new levels, `+0x3D` / `+0x3F` the second
  effect to add / to clear, and the last two are controlled negatives: `+0x30` is initialised and never
  read, `+0x130` is packed by recipe 101 and never read (the rows carry the sweeps and their controls).
- [x] ~~**Flag word A's bits 5, 6, 9–12, 15–18** and **flag word B's bits 1–3** by name — set from the
  scratch words and the prefix record, read by the applier as raw bits.~~ **FP-4** — B's bits and the scratch-word mapping
  were answered 2026-09-11; **the remainder ANSWERED 2026-09-13 (FABLE):** **the applier turns them into the side-effect flags of the four resource writes**, whose meanings [the HP write](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md) §2 tabulates (flag 4 suppresses the reaction publisher `003283D0`, flag 5 makes a zero delta count as a heal for that publisher, flag 6 suppresses the alive event); `BattleStats_ModifyPrimaryResource` reads flags 4, 5 and 7 the same way (`00300D0A`–`00300D3E`, `00300DA6`–`00300DBA`). By call: **target HP** (step 10) — bit 6 set = publish the reaction (`!b6 → 4`), bit 18 set = allow the alive event (`!b18 → 6`), bit 10 = zero counts as a heal (`b10 → 5`), bit 19 = death event `0x200E`; **target MP and the secondary pool** (steps 11–12) — bit 12 = publish the reaction (`!b12 → 4`), bit 16 = zero is a heal; **source HP** (step 13) — bit 5 = publish the reaction, bit 17 = allow the alive event, bit 9 = zero is a heal; **source MP** — bit 11 = publish the reaction, bit 15 = zero is a heal. So bits 5, 6, 11, 12 are per-number *show the reaction* switches, 17 and 18 *show the alive event* switches, and 9, 10, 15, 16 *a zero change is a heal*; which formula scratch word sets each is the mapping rows `+0x018` and `+0x02C` already carry.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The defaults and the 0x148 reach | `003848E0` read to its ret: `003848EF`–`003848F5`, `00384902`–`003849A0` | 1 | PROVEN |
| The kind's writers and values | `003860A7`, `00386303`, `00386347`, `003866CA`, `003866D7`; `0038823B`, `00389717` | 1 | PROVEN |
| The resolved mark gates the dispatch | `00386855`; `00385C6F`–`00385C85` | 1 | PROVEN |
| The applier's readings of each field | [the applier page](../applying-a-result-to-a-target.md) steps 1–20, sites as cited there | 1 | PROVEN |
| Every row of the table | [`result-record-accesses.tsv`](result-record-accesses.tsv) (245 rows), control found | 1 | PROVEN, with the scan's stated limits |

## 9. Related

- [`../applying-a-result-to-a-target.md`](../applying-a-result-to-a-target.md) — the consumer, step by step.
- [`../Post-Result-Events/the-post-result-events-and-the-battle-message-table.md`](../Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) — what the dispatcher makes of the record.
- [`../../08-Combat-Formula/Steal/the-steal-roll.md`](../../08-Combat-Formula/Steal/the-steal-roll.md) — one slot's writes (`+0x2C` bit 23, `+0x32`–`+0x34` via the resolver).
- [`../../08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md`](../../08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md) — the slots that fill it.
- [`../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md`](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) — where the two echoes go.
- [`../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md`](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) — the target the deltas land on.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every cited access site in this map was disassembled and its displacement compared with the offset of
the row citing it, by
[`check_field_citations.py`](../../../Tools/analysis-kit/gfz-scripts/check_field_citations.py):
**151 sites across 52 rows**.

| outcome | sites |
|---|---:|
| displacement **is** the row's offset | **135** (89.4 %) |
| resolved through an embedded sub-object base | 6 |
| other — indexed, a cited datum, or control flow | 10 |

**Nothing failed to decode, and no site contradicts its row.** Sub-object bases (2 distinct):
`+0x5C` x3, `+0xDC` x3.

Six citations name a **datum in `.data`** rather than an instruction — a table this record is read against, not an access to the record. They are citations of the right kind in the wrong column for a displacement check, and are counted apart rather than as failures.

**Not claimed:** this checks that each citation touches the offset it is filed under. It says nothing
about fields the census never reached; the document's own coverage limits stand unchanged.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings (the image-address resolver, the audio request chain) are recorded in the registry, not here.*

- **Items_Equipment_Shops_License — CLIENT and SERVICE.**
  - `GameState_GetGil` / `GameState_SetGil` are called by the gil-class inventory appliers and by both shop commits.
  - `BattleFormula_ApplyTargetResult` grants items through `Inventory_ModifyEncodedItemAndUpdateDiscoveryState`.
- **PlatformOnlineAchievements — SERVICE.** `GameState_SetGil` calls the achievement counter updater (counters 6 and 7,
  [the achievement catalogue](../../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md)
  AB-7). **A result that moves gil advances an achievement counter.**

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — SERVICE.** `003283D0` on this page calls `FUN_00263c20`, owned by that layer. What it reaches is **16 bytes** returning `byte[+0xE] & 0xF` - four bits with an accessor of their own, and zero when the pointer is null; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer, calls `00254EE0` on this page. That caller is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — PRODUCER.** This page's record is written by that layer's bodies: `003848E0` initialises it, `00385F60` resolves it (kind `+0x04`, flag words `+0x18`/`+0x2C`, resolved mark `+0x1C`), `00390AB0` and `00390F20` write kinds 7/8 on the Paling / Magick Shield / Reflect paths, `003112F0` applies it, and `00384F40` picks the Reflect retarget. `003112F0` in turn calls `00253690`/`00254EE0` (gil) and the level-up recompute `0030C650` cited at `+0x11C` is called by `003112F0` and itself calls `0031B860` (`BattleStats_FindOwningBattleUnit`). The crossing is the producer/consumer split - the layer writes the record, this page owns its shape. Added 2026-09-27 (SWE2-EC7, UQ-107 follow-up).

**Movement — SERVICE.** `00384F40` (the Reflect retarget picker cited at `+0x10`) calls `00334790` and `00334A70` - that layer's position/reach helpers - while it walks the unit slots for the nearest eligible unit. The crossing is those two calls. Added 2026-09-27 (SWE2-EC7, UQ-107 follow-up).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Presentation — SERVICE (1 edge).** The reaction publisher `003283D0` (the one result flag 4 suppresses) calls `BattlePresentation_EnqueueReactionWithRandomizedVariant` (`003BBD00`). The record's flags decide whether a reaction is published; the presentation layer only queues the chosen reaction animation, and reads nothing of the record itself.

**RNG_Random_Selection — SERVICE (8 edges).** Eight of the record's writers call `RNG_MT19937_NextU32_Thunk` (`00379CD0`): the outcome rollers `BattleFormula_RollSpecialGuardOutcome` (`00387FD0`) and `BattleFormula_RollAvoidGuardParryOutcome` (`003896B0`) that write the kind, `BattleFormula_RollAndStoreComboCount` (`00388660`) and `BattleFormula_RollPrimaryFormulaResourceReactionMode2Chance` (`00389140`) that write `+0x18`, the streak slot `00389C60` behind `+0x138`, `0038EAB0`, the gil-trap roll `0038F6F0` and the affinity AND-NOT writer `003902F0`. Every one of these fields is decided by a draw from the gameplay Mersenne Twister stream, so the record's content depends on that stream's position.

**Status_Periodic_Terminal — CLIENT and SERVICE (10 edges).** The applier `BattleFormula_ApplyTargetResult` (`003112F0`) calls `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (`0030E130`), `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`) and `BattleStats_RecomputeDerivedStateAndAutoStatuses` (`0030FED0`), and `0030E130`, `0030E360` and `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`) call it back; the level-up recompute `0030C650` (behind `+0x11C`) calls `0030FED0`; `BattleFormula_BuildPeriodicStatusResult` (`00385DF0`) calls the initialiser `003848E0` and `00310DB0` calls the resolver `00385F60`; and the apply-mask writer `0038FCE0` calls `BattleStatus_ComputeDefaultDwordParameter` (`00387730`) for the parameters at `+0x5C`/`+0xDC`. The status layer both consumes the record (the applier's status mask lands in its change and recompute bodies) and produces records of its own through this record's initialiser, resolver and applier on the periodic tick.
