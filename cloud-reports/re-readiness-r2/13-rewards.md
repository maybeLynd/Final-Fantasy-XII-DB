# Reconstruction readiness, pass 2 — `FFXII TZA/13-Rewards-Progression-Economy/`

| | |
|---|---|
| Stream | R2 (reconstruction readiness, pass 2), per [`docs/cloud-briefs/re-readiness-r2.md`](../../docs/cloud-briefs/re-readiness-r2.md). Pass 1 did **not** map this system, so this is part B: pass 1's full task ([`re-readiness.md`](../../docs/cloud-briefs/re-readiness.md)) |
| Lane | FABLE (r2-14) |
| Date | 2026-10-03 |
| Snapshot | this repo's text snapshot at `b23bdddd` only; no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item quotes or paraphrases a page and gives its location |

Citation form: `alias:line`. The aliases are the fourteen prose pages of the folder:

| alias | page | lines | status as its front matter states it |
|---|---|---:|---|
| `README` | `README.md` | 45 | category index |
| `DR` | `CONTRACT-defeat-rewards-sequence.md` | 368 | `readiness: CONTRACT READY`, `confidence: PROVEN` (`DR:5`–`6`) |
| `XA` | `CONTRACT-experience-and-licence-award.md` | 648 | `readiness: BEHAVIORALLY UNDERSTOOD` (`XA:5`) |
| `GS` | `CONTRACT-gil-storage-and-movement.md` | 293 | `CONTRACT READY` (`GS:5`) |
| `LA` | `CONTRACT-level-advance-and-growth.md` | 428 | `CONTRACT READY` (`LA:5`) |
| `LR` | `CONTRACT-loot-rolls-and-the-chain.md` | 329 | `CONTRACT READY` (`LR:5`) |
| `WP` | `CONTRACT-world-loot-pickup-pool.md` | 417 | `BEHAVIORALLY UNDERSTOOD` (`WP:5`) |
| `AW` | `experience-and-license-point-award.md` | 357 | `PARTIAL — edge-state reachability (GR-18) partial` (`AW:4`) |
| `HX` | `how-experience-is-computed-and-divided.md` | 240 | `PARTIAL` (function note of `AW`; `HX:4`–`6`) |
| `ED` | `what-happens-when-an-enemy-dies.md` | 432 | `DOCUMENTED` (`ED:4`) |
| `LU` | `what-happens-when-a-character-levels-up.md` | 728 | `AUDITED` (`LU:4`) |
| `GP` | `gil-storage-clamp-and-every-path-that-moves-it.md` | 533 | `AUDITED` (`GP:4`) |
| `LD` | `loot-drops-and-enemy-chain.md` | 781 | `AUDITED` (`LD:4`) |
| `CH` | `the-chain-and-its-sticky-coin.md` | 146 | `AUDITED` (`CH:4`) |
| `PK` | `world-loot-pickups-the-ten-slot-pool-and-the-despawn.md` | 746 | `AUDITED` (`PK:4`) |

The three `.tsv` member files were checked for layout only. They agree with the pages: the pool base `02EC0FA0`,
stride `0x60`, ten slot indices written by `00319B10`, and the presence table `0x022BE7F0 stride=0x20 count=10`.

"Not stated" means no page of this folder says it. Where another category's page or the register says it, the
pointer is given as a path from `FFXII TZA/`. Those pages were read only at the cited lines.

## 1. Interface

The system has five parts:
- the defeat sequence and its two reward computers;
- the level advance;
- gil storage;
- the loot rolls and the enemy chain;
- the world pickup pool.

### 1.1 Entry points (functions, with their callers)

| function | role | callers as the pages state them | cite |
|---|---|---|---|
| `00312280` `BattleUnit_ProcessDefeatRewardsAndLoot`, 857 B | the whole defeat sequence, steps 0–6 | only `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`) at `0030E884` | `ED:322`–`323`, `ED:362`; `DR:59`–`64` |
| `002F8BB0` `Reward_ComputeExperienceForRecipient`, 430 B | EXP for a recipient or NULL | `00312280` per recipient, and with NULL at `003124BE` | `XA:47`, `XA:174`; `HX:44` |
| `002F90C0` `Reward_ComputeLicensePointsForRecipient`, 179 B | LP for a recipient or NULL | `00312280` per recipient, and with NULL at `003124CA` | `XA:47`, `XA:174` |
| `0030C650` `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth`, 570 B | walk a stats record up to a target level | `0030C470` (`0030C56E`, flags 2), `00305960` (`003059CB`, console "Set level to max"), `003112F0` (`003113DF`, `003113FD`), `00312280` (`003124A3`) | `LU:148`; `LU:212`–`219`; `LU:466`–`471`; `LA:51`–`58` |
| `002F9A60` / `002F9B20` / `002F9BD0` | HP, MP and float-stat growth helpers | only `0030C650` | `LU:89`–`94`, `LU:134` |
| `00254EE0` `GameState_SetGil`, 72 B | meter, clamp, store gil | 13 callers, listed | `GP:86`–`100`; `GS:47` |
| `00253690` `GameState_GetGil` (+ thunk `00309BF0`) | read gil | 19 + 3 callers, disjoint | `GS:48`–`49`, `GS:93`–`102` |
| `003004B0` / `00300500` | add-and-notify / set-nonnegative wrappers | `0050FAF0` (script verb), `00316DF0` and others | `GP:287`–`296`; `GP:399`–`400`, `GP:439` |
| `00469E80`, 60 B | gil-change notifier, event `0x26` on positive deltas | `00312566`, `003004E5`, `002FD5D3`, `002FEF02`, `003108CC` | `DR:223`–`233` |
| `003F4AA0` | reward-bundle applier (gil + items) | `00290130` ← thunk `002E1A50` ← `00344C9A` in `00344C60`, verb `037C questresultwindow` | `GS:169`–`184`; `GP:303`–`323` |
| `00317ED0` `EnemyChain_UpdateOnDefeat`, 529 B | chain update on a kill | `00312280`, step 0 | `ED:79`–`81`; `CH:31` |
| `003183D0` `EnemyChain_TryAdvanceRank`, 315 B | chain rank advance | `00317ED0` at `00317FBC`, continued chain only | `LR:56`; `LD:750` |
| `003183A0`, 42 B | chain record reset | `00237DF0` (battle reset), `002342F0` (area init), `002FEAC0` (verb `btladjustsystem` `0x0517`, bit 0) | `LD:719`, `LD:727`, `LD:768`–`781` |
| `00319490`, 148 B | drop gate (could the party leader stand at the death position) | `00312280` (`00312588`–`00312597`) | `ED:226`–`230` |
| `003180F0` `Loot_RollDropEntries`, 641 B | roll the seven drop entries | `00312280`, after the gate | `LR:51`; `ED:358` |
| `00318820`, `003185D0`, `003186F0`, `00318510` | profile pick, slot chance, quantity bucket, extra item | `003180F0` | `LR:51`–`55` |
| `00319530` | chain-bonus outcome selector | `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`) at `00311146`, party unit only | `LR:135`–`138`; `LD:653`–`681` |
| `00319B10` init, `00319CA0` create, `00319600` tick | the ten-slot pickup pool | init: `002341C0` (`WP:401`); create: `00312280` (`ED:358`); tick: **not named in this folder** (gap N-11) | `WP:43` |
| `00319920` / `00319A00` collect, `003197B0` / `00319830` remove | retire a pickup with / without a grant | `00310DB0` (`0031127F`, `00311141`) | `PK:285`–`299` |
| `002FB150` overlap test, `00319850` nearest pickup | find a pickup | `00310DB0` at `00311105`; `00312730` at `003129AF` (order goal `0x4165`) | `PK:263`–`278`; `WP:322`–`330` |
| `0028F000`, 156 B | pickup presentation dispatcher, ops 1–6 | the six call sites in the pool bodies | `WP:118`–`153`; `PK:307`–`321` |
| `003171C0` / `00317090` | achievement counter 4 + species tally / counter 17 | `00312280` (steps 0 and 6) | `ED:82`–`104` |

### 1.2 Inputs and outputs (data read and written, with record layouts)

**The recipient's stats record** (`BattleStats`, a `0x1C8` record, `ED:291`):

| offset | width | role | written by this system? | cite |
|---|---|---|---|---|
| `+0x04` | u8 | id: EXP rejects `0x1B..0x27`; LP admits `0..6`, `0x1A`, `≥0x28`; also the growth-row index | no | `XA:70`, `XA:92`; `LA:65` |
| `+0x05` | u8 | kind: recipient must be 0; non-zero skips growth and the fanfare | no | `XA:70`; `LA:66` |
| `+0x08` / `+0x0C` | i32 / i16 | HP / MP, grown with a random bonus | yes (`0030C650`) | `LA:67`–`68`; `LU:256`–`262` |
| `+0x10`…`+0x1C` | f32 ×4 | Strength, Magick Power, Vitality, Speed; `+g/128` per level, clamped above 100.0 | yes | `LU:141`–`165` |
| `+0x3C`, `+0x64` | u32 | status words, OR'd and tested with `0x80000003` | no | `XA:71`; `AW:85` |
| `+0x69`, `+0x79` | u8 | byte 1 of the two effect layers; bit 4 = effect 12 (LP → gil) | no | `DR:70`; `ED:186`–`196` |
| `+0x6B`, `+0x7B` | u8 | EXP `0x08` doubles then `0x20` zeroes; LP `0x10` doubles | no | `XA:72`; `AW:141`–`145` |
| `+0x18C` | i32 | accumulated EXP, cap 99,999,999 | yes (`00312444`) | `ED:122` |
| `+0x190` | i32 | accumulated LP, cap 99,999 | yes (`0031248F`) | `ED:123` |
| `+0x1C2` | u8 | level, 0–99; `0030C650` is its writer | yes | `LU:45`–`58` |

**The defeated unit** (`BattleUnit`):

| offset | role | cite |
|---|---|---|
| `+0x698` → stats `+0x1C2`, `+0x88`, `+0x05` | its level, the baseline byte (1 from the enemy initializer), kind 1 | `XA:73`–`74`; `AW:139` |
| `+0xE70` | base-row pointer, from registry `02EBF148` by definition `+0x22` | `DR:78`–`81`; `XA:112`–`122` |
| `+0xE78` | per-level-row pointer, from `02EBF140` by definition `+0x24` | same |
| `+0xE68` | the `.ard` class row: `+0x28` bit 1 "does not chain"; `+0x05` type (copied to unit `+0x56`, the chain key); `+0x40` model id | `LD:390`–`404` |
| `+0xE9A` bit 3 | excludes the unit from steps 1–6 | `ED:84`–`87` |

**A reward row** (the two rows `+0xE70` / `+0xE78` point into): `+0x00` u16 counter-17 score (`ED:98`–`101`);
`+0x2F` u8 LP coefficient (`XA:78`); `+0x30` i32 gil coefficient (`DR:116`–`124`); `+0x34` u32 EXP coefficient
(`XA:77`). Every quantity has the form `(level − baseline) × perLevel + base` (`XA:136`–`138`, `XA:160`–`161`,
`DR:118`–`119`, `ED:98`–`101`). The shipped value ranges are on
`04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md` (`AW:228`–`231`).

**Formulas.**
- **EXP:** `A = signed32(D × perLevel[+0x34] + base[+0x34])`, with `D = level − baseline`. In designated mode (`003135C0` nonzero) A is paid whole to the designated member. Otherwise A is divided, `idiv` toward zero, by the passing count among exactly four `0031B810(i)` slots; a count of 0 returns 0 (`XA:136`–`153`). Then `0x08` doubles and `0x20` zeroes (`XA:148`–`149`).
- **LP:** `D × u8 + u8`; `0x10` doubles; no divisor. Any nonzero value of the global byte `0209A2A9` returns 0 first (`XA:160`–`163`, `XA:89`).
- **Gil:** `D × [+0xE78]+0x30 + [+0xE70]+0x30`, plus the effect-12 term `level × LP × 5` (`DR:116`–`133`).
- **The caps:**
  - per award: EXP 999,999 and LP 999, each floored at 0;
  - accumulated: 99,999,999 EXP and 99,999 LP;
  - the per-award caps are applied again to the presentation values (`ED:116`–`127`; `DR:186`–`189`).
- **The experience curve:** `002F8F20`, stated on `04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:375`–`390` (pointer at `ED:142`–`145`).

**Gil storage.** The `i32` at `[02092758] + 0x08`, clamped to `[0, 0x05F5E0FF]` by the setter only (`GS:53`–`56`). The
meter is `00316A50`: kind 6 for a gain, 7 for a spend, the unclamped delta, and nothing for a zero delta (`GS:62`–`91`).
`[02092758]` is the active save buffer (`GP:340`, `GP:355`–`358`). The action reservation is `unit + 0xE58` (`GP:168`).

**The loot inputs.**
- **Spawn row:** five drop words `+0x28`–`+0x30` (`0xFFFF` = none). Two extra triples: chance `+0x42` / `+0x43`, condition `+0x48` / `+0x4C` (a key item the party must hold), loot `+0x4A` / `+0x4E` (`LD:306`–`313`, `LD:442`–`445`).
- **Profile table `02EBF0C0`:**
  - header: `+0x04` count, `+0x08` stride, `+0x0C` RVA;
  - row: `+0x00..+0x04` i8 chances, `+0x05` i8 same-model requirement, `+0x06 + slot × 4` four i8 cumulative weights, `+0x22` selection weight;
  - four shipped rows (`LD:508`–`517`, `LD:688`–`692`, `LD:432`–`437`).

**The loot output.** `out[7]` of `{u16 itemId, u16 pad, u32 quantity}`:
- pre-filled `{0xFFFF, 0}`;
- quantity is the bucket + 1;
- duplicates are merged into the earliest entry, and the function returns 1 if any item remains (`LR:67`–`68`, `LR:152`–`162`).

**The chain tables.**
- rank thresholds: `00D107D4` = 30 / 50 / 80;
- a 3 × 11 rank-up chance table at `00D106F8`;
- the chain-bonus weights at `01EED3B8` (4 × 7, rows sum to 100);
- the variant table at `00D102C0` (`LD:263`–`272`, `LD:628`–`638`, `LD:653`–`681`).

**The pickup node** (`0x60`, ten at `02EC0FA0`):
- `+0x00` slot index (immutable), `+0x04` state 0–7, `+0x08` stamp;
- `+0x0C` padding;
- `+0x10` / `+0x18` prev / next, `+0x20` seven drop entries, `+0x58` handle;
- `+0x5C` padding (`WP:52`–`67`).

The presence table is ten `0x20` entries at `022BE7F0`: byte `+0` present, position `+0x10` (`PK:242`–`244`,
`PK:613`).

**Outputs to other systems.**
- recipient EXP / LP / level / stats; party gil; a world pickup;
- achievement counters 4, 11 and 17, and 6 / 7 through the meter (`ED:367`–`370`; `DR:315`);
- event 4 (level-up message, `0046A690`, `LA:173`–`177`);
- event `0x26` (positive gil delta, `DR:228`–`231`);
- the presentation calls `0028FB80` (EXP / LP) and `0028F000` (pickup);
- the level-up effect `0x71` and sound slot 7 (`LU:221`–`236`, `LU:313`–`358`).

### 1.3 State (globals and objects, with lifetime)

| state | initial value / reset | lifetime | cite |
|---|---|---|---|
| shared gameplay LCG `022C256C` | seeded per area load by `g_uAreaInitLcgSeedSequence++` in `BattleSystem_InitializeAreaState` | session; advanced by 7 inlined consumers here plus every other LCG caller | `LD:214`–`215`; `LR:75`–`81` |
| MT19937 state `02EB3870` | not stated here | HP / MP growth draws | `LA:393` |
| chain record: `022C3158` rank 0–3, `022C315C` count, `022C3160` model streak, `022C3164` break counter, `022C3168` genus (−1 none), `022C316C` model key, `022C3170` base, `022C3174` pickups collected, `022C3178` bit 0 coin | `003183A0` zeroes `3170`/`3160`/`3158` qwords, clears bit 0, sets `3168 = −1` | reset on area init, battle reset and `btladjustsystem`; otherwise across kills | `LD:770`–`781`; `CH:83`–`88`; `LD:745` |
| pickup pool `02EC0FA0`, head `02EC1360`, tail `02EC1368` | `00319B10`: slot i = i, the rest zero, head / tail null, presence bytes cleared | reset by the battle-storage reset `002341C0` | `WP:100`–`104`, `WP:265`, `WP:401` |
| field clock `0208D45C` | BSS, 0 at load | frames; stamps pickups (writer: gap N-12) | `WP:105`; `PK:100` |
| frame scalar `01DFE0B8` | `1.0` (30 fps) or `2.0` (60 fps), set once at startup from `FrameLimit` | process | `PK:139`–`199` |
| gil `[02092758]+0x08` | lives in the active save image | save | `GP:340`–`358` |
| New Game Minus bit 14 of `[[02EBF190]+4]` | set by the preset apply from request bit 2 of `02089344` | save | `ED:235`–`248` |
| recipient scratch `022C1740` | zero-init `.data` | one defeat call | `ED:345` |
| meter counters `[020927C0]+0x3860` / `+0x3864` | saturating dwords | save | `GS:90`–`91` |
| unit reward rows `+0xE70` / `+0xE78` | set once at install; zeroed with manager 0's unload (GR-17 ANSWERED) | unit life | `AW:222`–`224` |

### 1.4 Order (what runs when, and what triggers it)

- **The defeat** is triggered when a status change downs an enemy (`0030E360` → `00312280` at `0030E884`, `ED:299`, `ED:350`–`364`). In order:
  0. chain update `00317ED0`, then counter 4 and the species tally `003171C0`. Steps 1–6 then run only for an enemy-kind record without `+0xE9A` bit 3, killed by the party or by party-applied Poison / Petrify (`ED:79`–`87`).
  1. build the recipient list, at most nine (`ED:88`–`89`, `ED:213`).
  2. per recipient: EXP / LP, clamp, the effect-12 conversion, the EXP add (skipped under New Game Minus), the level walk over `002F8F20`, `0030C650(rec, level, 0)`, LP add, counter 11 (`ED:90`–`93`, `ED:129`–`145`; `DR:109`–`114`).
  3. NULL-recipient recompute, recap, New Game Minus zeroing, `0028FB80` (`ED:94`–`95`, `ED:109`–`114`).
  4. gil: `requested = max(old + award, 0)` → `00254EE0` → `00469E80(requested − old)` (`DR:135`–`146`).
  5. drop: `00319490` gate → `003180F0` → `00319CA0` (`ED:226`–`227`, `ED:358`).
  6. counter 17 (`00317090`). The body retires nothing (`ED:98`–`107`).
- **The level advance** clamps the target, returns if it is not above the current level, then per level: skip at 99, gate on the kind, grow six stats (two MT draws), increment. On the final level only: rebuild derived state, then post event 4, then (if a battle unit owns the record) the forwarding and audio calls (`LA:214`–`218`; `LA:95`–`102`, `LA:167`–`177`, `LA:186`–`196`).
- **The gil setter:** compute the delta → meter it unless zero → floor → cap → store (`GS:127`).
- **The chain update:** on a continued chain, `003183D0` runs at `00317FBC`, before this kill's coin draw (`00317FC1`–`0031800C`) and coin store (`003180C6`). A break never calls it (`LR:56`, `LR:187`; `LD:282`).
- **The loot orchestrator:** pre-fill → profile (rank, or drawn while `022C3164 > 0`) → five slot rolls (with the `+0xE64` keep) → a quantity per kept slot → two guarded extra rolls → merge duplicates → clear → return (`LR:115`–`131`, `LR:145`–`162`, `LR:187`–`188`).
- **The pool:** the tick walks the active list once per field frame, with at most one retirement per tick (`WP:268`). The ladder (`PK:103`–`134`):
  - state 1 → 2 when the visual reports ready;
  - blink steps at `stamp + 1650 … 1770`;
  - expiry at `stamp + 1800` (30 fps units).
- **Collection:** `00310DB0`, per unit per frame. If the unit is the focus or has committed `0x4165`, the overlap test runs. A party record collects and then rolls `00319530`; a non-party record removes without a grant (`PK:285`–`299`; `LD:653`–`681`).

### 1.5 Dependencies (on other systems)

| system | what this one takes from it | cite |
|---|---|---|
| 10-Status-Periodic-Terminal | the trigger (`0030E360`); the periodic tick `00310DB0` that collects pickups and rolls the chain bonus; the derived-state rebuild `0030FED0` | `DR:319`; `LD:725`; `LA:323`–`326` |
| 08-Combat-Formula | stats lookups `00320AB0`, `0031B860`; the result applier `003112F0` (a level and gil caller); Chain Bonus action `0xF5` | `DR:303`; `LA:381`; `LD:660`–`668` |
| 21-RNG-And-Determinism | the shared LCG `022C256C`, stepped inline; the MT19937 thunk `00379CD0` | `LR:75`–`108`; `LA:393` |
| 20-Platform-Online-Achievements | the meter `00316A50` (counters 4, 6, 7, 11, 17) | `GS:67`–`71`; `ED:264`–`269` |
| 12-Items-Equipment-Shops-License | `00300B80` / `003008A0` grant; shops and bundles as gil writers; item category map `0031E9F0` for the pickup tier | `WP:155`; `GS:280`; `PK:420`–`431` |
| 06-Movement-And-Navigation | the drop gate's placement test `003377C0` / `00337700` | `ED:230` |
| 04-Actor-Entity | the reward-row install `0023A570`; positions and radii; the experience curve | `XA:112`–`128`; `PK:266`–`271` |
| 17-Presentation / 16-UI / 18-Audio | `0028FB80`, `0028F000` / `003FA160`…, effect `0x71`, sound slot 7 | `ED:332`; `WP:115`–`153`; `LU:221`–`236` |
| 03-World-Area-Field | field bit 15 (`00377C20`) for recipients and the chain-bonus gather | `DR:323`; `LD:727` |
| 19-Save-Load-Settings / 00-Engine-Core-Runtime | New Game Minus flag; `FrameLimit` → frame scalar; locale id (chain cap 999 / 998) | `ED:233`–`258`; `PK:154`–`199`; `LD:287`–`293` |
| 01-Script-VM | `questresultwindow` → bundle applier; `btladjustsystem` → chain reset; `0050FAF0` → add gil | `GS:181`; `LD:775`–`781`; `GP:439` |
