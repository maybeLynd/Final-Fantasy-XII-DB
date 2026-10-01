---
system: The count, walk and bank recipes — four recipes whose damage is a streak, the leader's walked distance, or a banked share of earlier hits
category: 08-Combat-Formula
status: AUDITED
owner_layer: PrimaryOwner:CombatFormula
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the 109 recipe lists at 01EF96C0 decoded (two -1-terminated slot lists each) and joined to action_data.bin's
    recipe byte; the five calculator slots read whole; the accumulator's feeder and the three echoes' writers and
    readers read at every cited site
corpus_validated: "recipes 16 / 17 / 56 / 60 are the only recipes naming slots 121 / 122 / 49+144 / 146; actions 0x90, 0x91, 0xB0, 0xB4, 0xC4, 0xC5 are the only rows using them"
last_reviewed: 2026-09-11
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-count-clock-recipes-pass-1
  last_pass_kind: falsification
  crossref_clean: true
  reopened_count: 0
---

# The count, walk and bank recipes

> Four recipes do not compute damage from stats. One doubles a streak, one reads how far the leader
> has walked, and a pair banks a third of every hit and pays it out later. They are the reason the
> battle-state block carries three "result echoes" and a walked-distance accumulator, and they are
> the answer to `FO-2` and `FO-3`.

## 1. What the player sees

A technick whose number keeps doubling while it keeps landing and collapses when it misses; one
whose damage depends on how far you have walked since you last used it; and a pair where one use
stores up a share of the damage and the other releases the store.

## 2. Native mechanism

### 2.1 Which actions

The recipe pointer table at `01EF96C0` (109 entries, each two `-1`-terminated slot lists — preview,
then committed) names these five calculator slots in exactly four recipes; the action table's
recipe byte `+0x08` names the recipes in exactly six of its 543 rows:

| recipe | committed slots | actions (`action_data.bin`) | what it does |
|---|---|---|---|
| 56 (`01EFA230`) | `[49, 144]` | `0xB0` | **the streak**: roll to extend a count, deal `2^count` |
| 60 (`01EFA278`) | `[146]` | `0xB4` | **the walk**: a multiplier from the leader's distance walked since the last use |
| 16 (`01EF9C40`) | `[121]` | `0x91`, `0xC4` | **the bank's deposit**: HP-fraction damage, a third of it banked |
| 17 (`01EF9C50`) | `[122]` | `0x90`, `0xC5` | **the bank's withdrawal**: deal the banked sum, empty it |

> **FU-1 answered 2026-09-12 (FABLE) — the names, from bank 0 of `battle_pack.bin` by row index** *(checked 2026-09-12:
> names are looked up by the row's `+0x34` word, which differs from the row index only on rows 128–142 —
> [the action definition row](../../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md); none of the six rows below is in
> that window, so the names stand)*
> ([the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md)), with each row's recipe byte re-read:** `0xB0` (176) **Numerology** (recipe 56), `0xB4`
> (180) **Traveler** (recipe 60) — the two inferences were right; `0x91` (145) **Knot of Rust** and `0xC4`
> (196) **Devour Soul** share recipe 16, the deposit; `0x90` (144) **Dark Matter** and `0xC5` (197) **Soul
> Purge** share recipe 17, the withdrawal. So the "Souleater-shaped pair" is not Souleater (row 165,
> recipe 45) — it is the **Knot of Rust / Dark Matter** item pair, whose damage grows with use, and its
> enemy-ability twins Devour Soul / Soul Purge; exactly these six rows carry recipes 16, 17, 56 or 60.

No preview segment in any of the four — **confirmed 2026-09-13: all four lists begin with the
`-1` terminator, so the preview segment is empty in every one** (§9). ~~The rows' names are not
in this database (text banks are unread); by mechanism they are the technicks the game calls
Numerology, Traveler and the Souleater-shaped pair — an inference from behaviour, stated as
such.~~ **Superseded by `FU-1` above, which names all six rows from bank 0** — and which
retired the "Souleater-shaped pair" guess. This paragraph was left standing beside the answer
that replaced it.

### 2.2 The streak — slot 49 (`00389C60`) then slot 144 (`0038EAF0`)

Slot 49 reads the current count from block `+0x5B0E` (**echo B**, `00389CC4`) and, when the
source's 64-byte record has a stored preview (bit 0 of `+0x12`, `00389D24`) and the count is
below 17 (`00389D2A`), rolls `mt19937 % 100` against **`row[+0x12] − count² / 4`** — the action's
hit chance less the square of the count over four (`00389D0B`–`00389D19`, the threshold written
back over the hit chance `02AEDFE0` at `00389D19`; the compare at `00389D48`): success writes
`count + 1` into result `+0x138` (`00389D58`); a failed roll, or a count of 17, writes `0`
(`00389D72`) and **marks the action a miss** (`02AEDFBC = 1`, `02AEDFB8 = 1`, `00389DA4`–
`00389DAE`). Without a stored preview the slot misses outright at count 0 and otherwise rolls the
same threshold to hit or miss without touching the count (`00389D7E`–`00389DA2`). Slot 144 then sets the damage word
`02AEE004 = 2 ^ echo B` — `pow(2.0, +0x5B0E)` with the double `2.0` at `01CEBC10`
(`0038EAF4`–`0038EB1B`). `BattleFormula_ApplyResultMetadata` copies result `+0x138` into
`+0x5B0E` after the hit (`00385BAF`–`00385BD1`), so the next use sees the new count. **A streak
runs 1, 2, 4 … 65,536** (the count caps at 17 → `2^17` is never dealt: at 17 the roll is skipped
and the count resets), and the chance to extend it falls by `n² / 4` percent per step.

### 2.3 The walk — slot 146 (`0038EBE0`)

The block's accumulator `+0x5AC8` (float) / `+0x5ACC` (integer) is **the focus actor's walked
distance**: every presentation frame `PartyFocus_ProcessActorControlPresentationState` (`00358F90`)
takes the kind-3 focus actor's movement context, measures the distance between its position and
its previous position (`003A1920(ctx, ctx + 0x10)`, `00358FFF`–`00359010`) and, when it is
positive, adds it through `00317230` (`0035904F`–`00359052`; carry into the integer part, cap
`99,999,999`). Slot 146 reads the total (`00320D50`, `0038EC49`), takes it modulo 1000, subtracts
**echo A** (`+0x5B00`, `0038EC70`) and re-reduces modulo 1000 — the distance walked since the last
use, in thousandths — stores the current total modulo 1000 into result `+0x13C` (`0038ECBC`; the
metadata applier moves it into `+0x5B00`, `00385BD7`–`00385BEA`, so it becomes the new "last
use"), and deals **that distance times 10 at ≥ 990, times 3 at ≥ 500, times 2 at ≥ 100, times 1
below** (`0038ECC3`–`0038ED01`), writing the product into the source's record `+0` and into
`02AEE004`. A source without a stored preview just deals the record's value again
(`0038ED17`–`0038ED31`). The feeder's distance is the full 3-D length between the context's
position and its previous position (`003A1920`: three squared differences, then `sqrtf`).

### 2.4 The bank — slot 121 (`0038D970`) and slot 122 (`0038DA00`)

Slot 121 takes the source's HP — current HP (`stats +0x48`, floored at 1) when the merged flags
have bit 16, otherwise max HP (`+0x24`), doubled under bit 28 (`0038D976`–`0038D99A`) — divides it by `mt19937 % 10 + 1`
(`0038D99C`–`0038D9BE`), writes the quotient to the damage word `02AEE004` (`0038D9CA`) and adds
**a third of it to echo C** `+0x5B0C`, capped at 60,000 (`0038D9D0`–`0038D9F2`). Slot 122 moves
echo C into the source's 64-byte record `+0` and zeroes the echo (`0038DA49`–`0038DA61`, only when
the record has a stored preview), then deals the record's value (`0038DA68`–`0038DA6A`). The
record is the source's, so the bank is per attacker.

## 3. Key addresses

| address | role |
|---|---|
| `01EF96C0` | the recipe pointer table; entries 16 / 17 / 56 / 60 |
| `01EFA5C0` | the calculator table; slots 49, 121, 122, 144, 146 |
| `00389C60` / `0038EAF0` | the streak roll / `2 ^ count` |
| `0038EBE0` | the walk multiplier |
| `0038D970` / `0038DA00` | the bank's deposit / withdrawal |
| `00358F90` → `00317230` | the walked-distance feeder |
| `00385BA0` | `BattleFormula_ApplyResultMetadata` — result `+0x138` / `+0x13C` → block `+0x5B0E` / `+0x5B00` |

## 4. Data structures and formulas

```
streak:   p(extend) = hit% - count^2 / 4        damage = 2 ^ count      count in 0..16 (17 resets)
walk:     d = (steps - lastSteps) mod 1000       x10 (d >= 990) | x3 (>= 500) | x2 (>= 100) | x1
bank:     deposit = HP / (rand % 10 + 1)         echoC += deposit / 3 (cap 60,000)
          withdrawal = echoC -> record +0 -> damage ; echoC = 0
block:    +0x5AC8/+0x5ACC walked distance   +0x5B00 echo A (steps mod 1000 at last use)
          +0x5B0C echo C (the bank)         +0x5B0E echo B (the streak count)
```

## 5. Call chain

```
BattleFormula_ResolveTargetResult 00385F60 -> recipe 56: slot 49 -> slot 144 ; recipe 60: slot 146 ;
                                              recipe 16: slot 121 ; recipe 17: slot 122
  -> result +0x138 / +0x13C -> BattleFormula_ApplyResultMetadata -> block +0x5B0E / +0x5B00
PartyFocus_ProcessActorControlPresentationState 00358F90 -> 00317230 -> block +0x5AC8 / +0x5ACC (every frame)
```

## 6. Modding notes

- **The streak cap is the compare at `00389D2A`** (`0x11`); the doubling base is the double at
  `01CEBC10`; the extension penalty is the `count² / 4` at `00389D11`–`00389D17`.
- **The walk's thresholds** are the three immediates at `0038ECC3` / `0038ECE8` / `0038ECF5`.
- **The bank's share** is the `÷ 3` at `0038D9D0` and its cap the `60,000` at `0038D9E8`.

## 7. What is not known

- [x] ~~**The four actions' names** — the text banks are unread; the technick identities above are
  inferred from behaviour.~~ **FU-1 ANSWERED 2026-09-12 (FABLE):** Numerology, Traveler, Knot of Rust /
  Devour Soul (deposit), Dark Matter / Soul Purge (withdrawal) — the note under the recipe table.
- [x] ~~**What `00329E40` sets the walked-distance accumulator from** (the save?), and whether
  `+0x5B00` / `+0x5B0C` / `+0x5B0E` survive a save.~~ **FU-2** — ANSWERED 2026-09-11: the block
  lives inside the save image (payload `+0x4E48C`; the accumulator is payload `+0x53F54` /
  `+0x53F58`), so the accumulator and the three echoes are saved and loaded as bytes with
  everything else. `00329E40` (one caller) is the load normaliser's **restore** path: it puts the
  header stash `+0x7C` into `+0x5ACC` and zeroes `+0x5AC8` (`00329E47`–`00329E54`), undoing the
  mode-3 stash path's `00322200` (both zeroed, `00322209`–`00322216`) — the round trip on
  [the normalise page](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md)
  §4. `00320D50` (`int(+0x5AC8) + +0x5ACC`) is the total; `00254E80` mirrors it into the save
  header `+0x0C`, which `002536D0` reads back capped at 99,999,999 for two achievement checks
  (`003162E0`, `00316760`: `total − threshold[0] ≥ threshold[1]`) and the UI (`00281AE0`,
  `0057B890` — interior read 2026-09-17, SWE2-FRONTIER: 1,107 B — `002497E0` first at [`0057B906`](../../_index/ADDRESS-INDEX.md), `00291D80`/`002470D0` ×3 + `002CA110`/`00285F20` ×2, `002CF940`).

### 2.6 Recipe 61 — the gil throw (action `0xB5`)

The only recipe whose cost is computed at **preview** and charged at **consume**. Its preview
list is slot 18 (`00388D50`) and its committed list slot 147 (`0038ED40`); the action row is
kind 2 with `+0x0A = 0` and `+0x10 = 0`, so the MP and Mist costs are nothing and the gil is
everything:

- **Preview, slot 18** (`00388D50`, [the result page](../../07-Combat-Action/Result-Record/the-result-record-field-map.md)
  `+0x08`): the four slot-map units' current HP summed, capped at 10,000, into the preview
  record's `+0x08`, with flag C bit 11 when that is more than the party has (`00388E1A`–
  `00388E4F`). `BattleAction_EvaluateTargetPreviews` then hands the preview record to
  `004698C0`, which posts "Technick failed. Not enough gil." (`0x3A`) on bit 11, and copies
  `+0x08` into the unit's `+0xE54` (`00303950`–`00303954`).
- **Consume** deducts `+0xE54` from the party's gil (`00305712`–`0030572B`,
  [the item page](../../12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md) §4)
  — this is where the gil goes.
- **Committed, slot 147** (`0038ED40`, 207 B): takes the source's 64-byte record (`0208D480` +
  `slot × 64`; the `+0` word the preview stashed, §2.5 of [the scratch page](../Scratch-Block/the-formula-scratch-block.md)),
  divides it by the source's target count (`+0x77C`, `0038EDB4`–`0038EDD9`) and writes the
  quotient as the target-HP loss `02AEE004` (`0038EDDF`) — or, with no owner, no targets or a zero
  quotient, sets `02AEDFBC` (failed) instead (`0038EDFF`). It never writes result `+0x08`, so the
  applier's own gil deduction (`00311A84`) does not charge the throw a second time.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the four recipes and six actions | `01EF96C0` decoded, `action_data.bin` joined | 1 (image + authored data) | PROVEN |
| the streak's roll, cap and power | `00389C60`, `0038EAF0` read whole; `01CEBC10` = 2.0 | 1 | PROVEN |
| the accumulator is walked distance | `00358F90` `00358FFF`–`00359052`; `00317230` | 1 | PROVEN |
| the walk's modulus and thresholds | `0038EBE0` `0038EC49`–`0038ED01` | 1 | PROVEN |
| the bank's deposit and withdrawal | `0038D970`, `0038DA00` read whole | 1 | PROVEN |

## 9. Related

- [`../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md`](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) — the echoes and the accumulator.
- [`../Scratch-Block/the-formula-scratch-block.md`](../Scratch-Block/the-formula-scratch-block.md) — `02AEE004` and the source's 64-byte record.
- [`../../07-Combat-Action/Result-Record/the-result-record-field-map.md`](../../07-Combat-Action/Result-Record/the-result-record-field-map.md) — `+0x138` / `+0x13C`.
- [`ranged-weapon-recipes.md`](ranged-weapon-recipes.md) — the recipe table's shape.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

§2.1 is a chain of uniqueness claims, and every link was re-derived — the recipe table from the
image, the action rows from the shipped `battle_pack.bin`.

| claim | measured |
|---|---|
| the four list pointers | **`01EFA230`, `01EFA278`, `01EF9C40`, `01EF9C50`** — all four exact |
| the committed segments | **`[49, 144]`, `[146]`, `[121]`, `[122]`** — all four exact |
| "no preview segment in any of the four" | every one of the four lists **opens with the `-1` terminator**: the preview segment is empty in all four |
| "these five slots in exactly four recipes" | decoding all 109 lists, each of slots **49, 144, 146, 121, 122 is named by exactly one recipe**, and always in the *committed* segment |
| "exactly six of the 543 rows" | the action table's `+0x08` holds 16, 17, 56 or 60 on exactly **`0x90`, `0x91`, `0xB0`, `0xB4`, `0xC4`, `0xC5`** |
| `FU-1`'s pairing | `0x91`→16 and `0xC4`→16 (deposit); `0x90`→17 and `0xC5`→17 (withdrawal); `0xB0`→56; `0xB4`→60 — each as stated |

### The `+0x34` caveat holds exactly

`FU-1`'s parenthetical — that names are looked up by the row's `+0x34` word, which equals the row
index *except* on rows 128–142 — is exact on both halves. Over the 543 rows the word is `0`–`542`,
**all 543 distinct**, and it differs from the row index on **exactly fifteen rows, 128 through 142**,
whose values are

```
136, 137, 128, 129, 130, 138, 139, 140, 141, 135, 142, 131, 132, 133, 134
```

in that order — the list [the action definition row](../../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md)
gives, value for value. None of the six rows above falls in that window, so the six names stand.

### The streak's damage, from the bytes

```asm
0038EAFB  movsd    xmm0, qword ptr [01CEBC10]   ; the double is 2.0
0038EB03  movzx    ecx, byte ptr [rax + 0x5b0e] ; echo B, the count
0038EB0E  cvtdq2pd xmm1, xmm1
0038EB12  call     0x861f80                     ; pow
0038EB17  cvttsd2si eax, xmm0
```

`2 ^ echoB`, with the constant at the address §2.2 names and the value it says. Exact.

### ⚠ A paragraph left standing beside the answer that retired it

§2.1 ended *"The rows' names are not in this database (text banks are unread) … the technicks the
game calls Numerology, Traveler and the Souleater-shaped pair — an inference from behaviour"* —
directly beneath the `FU-1` block that **names all six rows from bank 0** and says in its own text
that the pair is *not* Souleater. Struck; the answer above it stands.

**Not claimed:** slots 49, 121, 122 and 146 were not re-read — only slot 144's damage line. The
accumulator's feeder, the three echoes' writers and readers, and the threshold arithmetic
`row[+0x12] − count²/4` were taken as given. Nothing was executed or observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

- **PlatformOnlineAchievements — SERVICE and CLIENT.** The count clock's save-header mirror is read by the achievement
  side. The mirror writer `00254E80` and the capped reader `002536D0` are both called by the two achievement checks
  `003162E0` (345 B) and `00316760` (169 B).
  - `003162E0` is called by a 287-byte body. It calls a 172-byte helper and two 44-byte helpers.
  - `00316760` is called by three bodies of 101–519 bytes, one of which is the 281-byte post-load counter pass that
    [the generator contract](../../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md) §6 names. It also calls the
    counter read.

  **So the recipe count clock feeds two achievement checks, and the post-load counter pass reaches one of them.**
- **Story_Event_Quest_Hunt — SERVICE.** The UI reader `00281AE0` gates on
  `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate`.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Resource — SERVICE, not read.** A cited recipe body calls two small Resource helpers (60 and 75 bytes).
- **Status_Periodic_Terminal — CLIENT.** `BattleUnit_RunPeriodicCombatMaintenance` calls a cited function.

**Script VM — CLIENT.** `0034C170` on the script bridge calls `002FAE40`, the bank-recipe row read — the recipe table is script-driven.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Apart from the walk feeder and the two rolls, these edges come from bodies the appended interior notes cite — the recipe-page widget code, the fade-schedule body `0035CA70` and the probes they share — and belong to those notes, not to the recipe mechanics of section 2.*

**ActorEntity — SERVICE (2 edges).** The walk feeder `PartyFocus_ProcessActorControlPresentationState` (`00358F90`) calls `ActorHandle_ResolveRegistryEntryByPackedId` (`003588B0`) to reach the focus actor whose walked distance it measures, and the preview slot 18 `00388D50` calls `BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`); both are lookups, and the recipes own no actor state.

**Audio — OUT-OF-SCOPE (26 edges).** The fade-schedule body `0035CA70` calls eight music-track helpers — the current-track read `002DEC00`, the track set `002DECE0`, the target-volume write `002DEE50`, `002DEDE0`, `00360C20`, `00360D70`, `00360E50` and `00361630` — and the helpers' own audio neighbours make up the rest (`002DECE0` calling `001DBBD0`, `001DBC10` and `001DBC70`; `002DEDE0` calling `001DBC30` and `001DBC50` and called by `00360B50`, `00360DD0` and three more; `002DEE50` calling `001DBCA0` and called by `00261F90`, `00361200` and `00361340`; `002DEC00` called by `003614E0` and three more). The page cites `0035CA70` only as a caller of the presence predicate its interior note reads; the music track it fades plays no part in the count, walk or bank recipes.

**CoreRuntimeScheduling — MECHANICAL (1 edge).** `00254A10`, the source picker the mode-table create consults, calls `00229E40`, a 7-byte getter of the language id, and answers 1 for five of the ids; it is a global read, unrelated to the recipes' arithmetic.

**Gameplay — MECHANICAL (2 edges).** `BattleIdClassD_GetRuntimeFlagBit2` (`0030B4B0`) and `BattleIdClassD_SetRuntimeFlagBit2` (`0030B630`), which the recipe widget's precheck `0057B6F0` calls, both call `BattleEncodedId_IsValidForClass` (`00322C50`) to validate the id before touching its flag; that validator is shared id machinery.

**Input — CLIENT, OUT-OF-SCOPE (17 edges).** The probe `00228480` — 13 bytes that answer whether the dialog object pointer at its global is non-null — is called by `InputManager_TranslateBindingProfileToControlState` (`00197160`), `00197990` and `InputFeedback_DispatchViaManagerGate` (`001E1120`); those three are cited only as its other callers, and their own input neighbours are the rest: `00196480`, `InputBackend_GetFilteredAnalogAxisValue` (`0079D1D0`) and the code-range tests `0079E650`, `0079E6A0`, `0079E6D0` below them, `InputManager_PollAndBuildControlState` (`00196FF0`) and `00197980` above them, and `InputManager_GetSingleton` (`00198790`), `InputManager_DispatchFeedbackToDeviceById` (`00198E80`), `00197780` and `InputFeedbackBridge_DispatchTwoBytePair` (`008628F0`) around the feedback gate. Input asks the same "is a dialog up" question the recipe widget's release route asks; no recipe state is involved.

**Items_Equipment_Shops_License — SERVICE (5 edges).** The recipe widget's entry fill `002FA920` calls `ItemDefinition_ClassifyEncodedItemCategory` (`002FABD0`) and `BattleIdClassD_GetRuntimeFlagBit1` (`0030B510`); the precheck `0057B6F0` calls `0030B4B0` and `0030B630`; and `0056E410`, called from the mode-table create, calls `0030B4B0`. The recipe page's widget classifies and flags class-D ids through that layer's accessors when it lists entries; the recipes of section 2 do not use them.

**Movement — SERVICE and CLIENT (10 edges).** `00358F90` calls `002640E0`, which returns a float from a kind-3 actor's movement context (zero for any other kind), and the distance leaf `003A1920` it measures the step with is also called by `Movement_UpdateSteeringTowardTarget` (`002E45E0`), `002E5180`, `00334220`, `00336AE0`, `Navigation_TestSegmentAgainstAuxObstaclesXZ` (`00391410`) and `00391D90`; the UI bodies `00281AE0` and `00281E00` call `00326BB0` and `00326D60`, and `0035CA70` calls `0026C3C0`. The walk recipe depends on movement's per-frame position and previous position (section 2.3); the other edges are movement using the same distance leaf and UI or fade code calling movement bodies.

**Party — CLIENT and SERVICE (4 edges).** `00358F90` — that layer's focus processing, called by `PartyFocus_UpdatePrimarySecondaryActorProcessing` (`00358EE0`) — calls the distance leaf `003A1920` and the accumulator `00317230` every presentation frame, and `0035CA70` calls `PartyConfiguration_SetSelectorsAndReconcileRoster` (`003273D0`). The walk recipe's distance total is written by the party focus's per-frame pass (section 2.3); the roster call belongs to the fade-schedule body, not to the recipes.

**Presentation — CLIENT, OUT-OF-SCOPE (22 edges).** The widget helpers the interior notes cite are called by large UI and render bodies — the release route `002470D0` by `002BAF80` and `00579420`, the widget register `00249410` and create `00249580` by `002B7B80` and `002BAF80`, the mode-byte setter `002DD7E0` by ten bodies such as `002455A0`, `003FBA80` and `00506700`, the text measure `002B3050` by `00506700`, `002526F0` by `00579420`, and the language test `00254A10` by `002B0280` and `002D2DB0` — while `00358F90` calls `CameraSystem_SetCameraActive` (`0025A520`) and the per-kind count-clock answer `003166F0` is called by `001CD0E0`. The count clock is read by one presentation body; the rest is shared widget machinery the notes describe and the recipes do not use.

**RNG_Random_Selection — DEPENDENCY (2 edges).** The streak roll slot 49 (`00389C60`) and the bank deposit slot 121 (`0038D970`) call `RNG_MT19937_NextU32_Thunk` (`00379CD0`): the streak's extend chance and the bank's `% 10 + 1` divisor (section 2.4) draw from the single gameplay MT19937 through that thunk.

**WorldAreaField — CLIENT and SERVICE, OUT-OF-SCOPE (2 edges).** `World_UpdateSimulationTick` (`00314020`) calls the dialog probe `00228480`, and `0035CA70` calls `0026DE00`, a 27-byte field-layer body: the world tick asks the same "is a dialog up" question, and the fade-schedule body reaches the field layer; neither edge touches the recipes.

## Interior citation — frontier hub `002470D0` (2026-09-17, SWE2-EC7)

`002470D0` — 93 B, 28 frontier callers at census; the shared detach/release route this page sees
inside `0057B890`. Crossing: the probe it delegates to, `00228480`, is also called by Input-layer
bodies `00197160`/`00197990`/`001E1120` — a shared predicate, not a recipe-system relationship.
Interior verified: null-guard, then `00228480(rcx)` probes the object; on
success **and** `[0209AC30]+0x308` being null it tail-jumps `002286B0(rcx)`. Otherwise, unless
`rbx == [0208EBC0]`, it runs `00244640(rcx)` then `00244830([0208EBC0], rbx, 0)`
([`00247104`](../../_index/ADDRESS-INDEX.md) is the branch into that arm). A two-route handoff:
one path for the probed state, one for the registry-owned object.

NOT claimed: which object family `0208EBC0`/`021990F0` anchor.


## Interior citation — frontier hub `002CA110` (2026-09-18, SWE2-EC7)

`002CA110` — 51 B, 16 callers; the `0209AC30` record's `+0x2D8` field teardown the
`0057B890` read above invokes. Interior verified: `[0209AC30]` loads the record
(`002CA114`), its `[+0x2D8]` pointer is freed through `00244F00` when non-null
([`002CA127`](../../_index/ADDRESS-INDEX.md)), and the field is then cleared to 0
(`002CA133`). Single-owner free-and-null — the sibling of `002CA150`'s rebuild arm.

## SWE2-EC7-19 update (2026-05-15) — `00316760` threshold-compare fragment

`00316760` (169 B) is the per-kind count-clock query the achievements path calls (`00316C60` → `00316760`): `bl = cl` selects the kind and `003166F0` answers most kinds directly — a non-`-1` result returns immediately (`00316774`..`00316777`). Kind `5` delegates to the `00254E80` + `002536D0` pair (`003167E6`..`003167EB`); kind `8` runs a 9-slot tally over `00282DD0(i)` records (`0031679F`..`003167D2`) — each record must have `word[+0x60] >= 0`, `byte[+0] & 2` clear, and pass `00282FA0`, contributing `byte[+0xBA]` to `r14d` — and returns `r14d / count` only when at least 6 records qualify (`003167D9`..`003167E4`), else `-1`. Other kinds fall through to the `-1` `003166F0` gave.

## SWE2-EC7-30 update (2026-09-18) — `00285F20` `+0xDE0` store + `00282FA0` slot predicate

`00285F20` (19 B) is the `+0xDE0` word write the `0057B890` interior
read names twice: `word[[0209AC30]+0xDE0] = cx` then a tail
`jmp 0027F210` runs the dependent update — store-and-notify, no
return value. Interior anchor `00285F2E` (the `jmp 0027F210` tail).

`00282FA0` (24 B) is exactly the predicate `00316760`'s kind-8 tally
already describes: returns true when `word[rcx+0x60] >= 0`,
`byte[rcx] & 2` is clear, and the word is `<= 5` — the enabled,
kind-in-range test every 9-slot scan in this family applies.
Interior anchor `00282FB0` (the `cmp dx, 5` bound).

## SWE2-EC7-102 update (2026-09-20) - `00292140` + `00283980` measured

`00292140` (75 B) is the `+0x168` flag-word rewrite
`00281E00` and `0057B890` call on the
`[0209AC30]+0x300` object: `+0x168 &= 0xFFF5FFFF`
then `|= 0x50000`, then `btr eax, 0x17` and
`|= 0x700000` - the mode-bits rewrite the recipe
walks post.
Interior anchor `00292153` (the `and`).

`00283980` (37 B) is the presence predicate
`0035CA70` and `0057B890` call: a null
`[0209AC30]+0x318` returns 1; otherwise the return
is `dword[rcx + 0xE4] == 0` - the empty-check the
count-clock arms run.
Interior anchor `00283995` (the `+0xE4`
compare).

Cross-subsystem note: the `0035CA70` citation above
also reaches 8 Audio-layer callees (`002DEC00`,
`002DECE0`, `002DEDE0`, `002DEE50` and four more in
`edges.tsv`). `0035CA70` is a shared fade-schedule
body consulted by both this layer and the Audio
side - the crossing is fan-in on one helper, not an
Audio relationship this page owns. (MECHANICAL,
SWE2-EC7-102, `edges.tsv`.)

`0057C070` (193 B) is the recipe-page mode switch `0057B890` calls: returns 0 unless `[rcx + mode*4 + 0x138]` is live; then writes `mode` to `+0xC4`, sets `[+0x148]->+0xE0 |= 0x20000`, and unless `mode == 2` runs `002CBDA0`/`002CC2A0` on `[[02CA9790]+0x158]`; it then `0057BEE0`s the object, `0056DD50`s `([+0xC0], [00D23920 + mode*4])` (the `{0x5AF,0x5A2,...}` mode table), stores the result to `02CA9798` with a `+0x188` back-link, and tail-calls `0057BD40` — returns 1.

Interior anchor `0057C0EB` (function `0057C070`).

`0057BD40` (404 B) is the three-slot recipe refresh `0057B400`/`0057B890`/`0057C070` tail into: a `0057B6F0` precheck ORs `[this+0x150]` bit 1 when it passes; then for `i` in 0..2 it `002CD420(i)`s a widget, computes `0056E880([+0xC0], tableA[i], tableB[i])` into `[this+0x138+i*4]` (with `i==0` substituting `i+1`), picks a message id from the `{0xC67,0xC68,0xC69}`/`{0xC67,0xCAB,0xCAC}` tables by `+0xC4`-mode (`0xFF` vs matched index), `002F9860`s it into `[widget+0x18]`, then `002DD7E0`s the mode byte and `002C9F20`s the widget — a per-slot text+value repopulate. (The unmeasured `0057B6F0` precheck's own `0030B4B0`/`0030B630` callees sit on the items/shops side and forward into the shared gameplay hub — fan-in on the precheck, not a relationship this page owns.)

Interior anchor `0057BE35` (function `0057BD40`).

`0057B780` (128 B) is the sub-widget create `0057B890` runs: `00249580()` makes the object, `003933F0(obj, 00D238E0, this+0x158, 1)` initializes it against the parent's `+0x158` table, then `002920C0`/`002CBD50(obj,2)`/`00292190` configure it; `002F8040(0x16)` gates a `002491B0(obj, 0x16)` plus `[this+0x150] |= 1`, and the tail-jump `00249410(obj)` registers it — a create-init-register pipeline.

Interior anchor `0057B7AC` (function `0057B780`).

`0057B4A0` (89 B) is the labeled-field init `0057B890` calls: builds a `{0,0,0, byte=3, dword|0x188}` stack record, `002F9860(0x805)`s the label text, calls `003949B0(this, text, &rec)`, then `00249C60(0x27)` — a one-shot caption setter.

Interior anchor `0057B4E4` (function `0057B4A0`).

`0057B400` (153 B) is the recipe-widget create `0057B890` calls: `002CD4D0(this+0xC8, this+0xD8, 3)` allocates the trio, three `002CD3C0` calls bind ids `0x48B`/`0x48C`/`0x48D` to message ids `0xC67`/`0xC68`/`0xC69`, then `002C9BF0(this, this, this+0xC8, 0, 1.0f, [01E0C3B0])` produces the `[this+0x148]` object and the tail-jump `0057BD40` performs the refresh — create, bind, populate.

Interior anchor `0057B430` (function `0057B400`).

`0057BEE0` (294 B) is the measure loop `0057C070` runs on the recipe object: `0057B660()` supplies the entry count; for each index `0057B500(this, mode-dl, i, &rec)` fills a record whose `[+0x30]` word list (count `[+0x38]`) is walked inner-loop — `00292B70` packs each word with `rec[+0x3B]` into a key and `002B3050` measures it, tracking the max in `di`; the tail call `002932F0(di)` consumes the widest measured extent. A per-entry max-width pass feeding the slot layout.

Interior anchor `0057BF50` (function `0057BEE0`).

`0057B6F0` (141 B) is the precheck `0057BD40` ORs `[this+0x150]` bit 1 on: `002FAD30(byte[+0xC0], 2, 0)` counts the entries and `002FA920` fills the `[+0x168]` u16 array; each word is `0030B4B0`-looked-up and, when absent, `0030B630(word, 1)`-registered with the success flag set — returns 1 iff at least one entry needed (re)registration.

Interior anchor `0057B743` (function `0057B6F0`).

`0057B660` (29 B) is the mode-to-slot-count map `0057BEE0` reads before its measure loop: `dl` 0 -> 9, 1 -> 6, 2 -> 1, anything else -> 0.

Interior anchor `0057B674` (function `0057B660`).

`0057B500` (337 B) is the per-slot record fetch `0057BEE0` calls inside the loop: rejects a null out-record, `r8b >= 3`, and `r9b` beyond the same 9/6/1 mode limit; zeroes `[rdi+8]`; modes 0/2 take a table byte (`00120000+0xC038F8` / `+0xC03901`, indexed `r9`) into `[+0xA]`, `002FAD30(byte[rbx+0xC0], ebp, byte)` counts into `[+0x8]`, and a nonzero count makes `002FA920` fill the `[rbx+0x160]` array which lands in `[rdi]`; mode 1 instead resolves `0056E860()` -> `00252FA0` for the count and `00252F40`/`0020E600` for `[rdi]`; `[+0xB]` takes `0056E840([+0xA])` in every live path. Returns `[+0x8] != 0`.

Interior anchor `0057B5E7` (function `0057B500`).

`0056E880` (331 B) is the any-member availability scan `0057BD40` computes per recipe slot (also `0057A4E0`/`0056E5D0`): `edx == 0xFF` is the scan form — `0057D600(ecx)` counts members, `0057D5E0(r8d, i)` resolves each id, and a 12-entry jump table on `(edi ? (member | ebp << 16) - 0x14 : member - 8)` picks `edx` in {0x18, 0x11, 0x12, 0} for `0057D610(member, edx)` — the first nonzero returns 1, exhaustion 0. The non-`0xFF` form tail-calls `0056E9A0(edx + (edi ? 0x14 : 8), ebp)` — the single-row variant.

Interior anchor `0056E8EC` (function `0056E880`).

`0056E860` (23 B) is the mode-1 subkind map `0057B500` resolves before `00252FA0`: returns `00D235C8[ecx]` (the `0B09080004030201` table) for `ecx < 0xB`, else -1.

Interior anchor `0056E872` (function `0056E860`).

`0056E840` (23 B) is the `+0xB` byte map `0057B500` stores on every live path: returns `00D235D8[ecx]` (the `0906070802050301` table) for `ecx < 0xC`, else -1.

Interior anchor `0056E852` (function `0056E840`).

`0056DD50` (372 B) is the mode-table object create `0057C070` stores to `02CA9798`: `00564AC0(0, 0x1C0, arg, 0056E140)` builds a `0x1C0` record with handler `0056E140` and the arg byte at `+0x190`; `00564780(rec, rec[+0x192], 0)` primes it; `00254A10()` picks the source — set takes `0057B680(0)`, else `[0209AC30]+0x48` — and `00567190(src, 6-or-9, [rdi+0xE8], rdi+0xF0)` builds the child into `[+0xC8]`; `00244960` initializes; the `+0x180 << 6 >> 0x1B + 0x1E` index selects the `rdi + idx·8` slot `005674B0([+0xC8], slot)` fills; `0056DC30(byte[+0xF7] or 1)` lands in `[+0x191]`; an `arg` in `[0x597, 0x59D]` or `[0x59F, 0x5A1]` sets `[+0x194]` bit 0; then `0056C950`, `0056E410`, `0056E5D0(rec, 1)`, `002CF890` and `002C9490(01E0C3DC, 01E0C3BC, 01E0C3E8)` finish the layout. Returns the record.

Interior anchor `0056DE1A` (function `0056DD50`).

`0057D600` (16 B) is the member-count constant `0056E880` reads at scan open: returns `ecx ? 9 : 6` — matching the `6-or-9` child size `00567190` is called with.

Interior anchor `0057D607` (function `0057D600`).

`00564780` (729 B) is the member-populate `0056DD50` primes the created record with (also `00564010`): `dl` lands in `+0x17E`/`+0x17F`, `01F2CB90[dl]` seeds `+0xE8`, `+0x180` clears bit 0x1B / sets 0x1A / ORs `r8b` / masks `0xDFE0FFFF`, and `+0x17C` = 0xFFFF. Per `i < [tbl]`: the `dl <= 7` arm requires `00252D10(word[ent+4] + 9)` == 1 then `0057D610((arg3 << 16) | byte[+0x17F], word[ent+6])` == 1 — on pass `+0x180` bits 16-20 increment (the member count fold), `00252D40(word[ent+4] + 9, 1)` marks, and the `rbx + count·8` slot takes `+0xF7` = `byte[ent+4]`, `+0xF6` = i, `+0xF2`/`+0xF4` = 0xFFFF, `+0xF0` = `002526F0(8, movsx byte[ent+4])` or 0xFFFF; the `dl > 7` arm instead maps `+0x17F` byte 0x20 -> `0057D5E0(1, i)`, 0x13 -> `0057D5E0(0, i)`, else sign-extends it — a nonzero `0057D610` fills the same slot without the `00252D40` mark. After the loop `+0xF6` of the count slot is written 0xFF (the terminator), `+0x180` bits 0x3E00000 clear, and the `dl <= 7` form finishes `002526F0(8, byte[+0x17E] + 0x40)` then scans the filled slots for the matching `+0xF7` byte, folding its index into `+0x180` bits 21-25.

Interior anchor `0056499A` (function `00564780`).

`0056DC30` (109 B) is the kind-to-channel jump table `0056DD50`/`0056DED0` consult: `ecx <= 0x1F` selects through the `+0x44DCD4` byte table into the `+0x44DCA0` arm table — twelve arms returning constants 0..0xB; `ecx > 0x1F` returns 0xFF. The `0056DD50` create stores its result into `+0x191`.

Interior anchor `0056DC50` (function `0056DC30`).

`00567190` (99 B) is the child-object factory `0056DD50` runs for `[+0xC8]` (also `003FD6B0`/`003FD860`): a stack-cookie-bracketed `00244F50(0x158, 00567200, &ctx)` creates a `0x158` record with handler `00567200` and context `{rcx, edx, 0, r8, r9}` — the `6-or-9` count and the `[rdi+0xE8]`/`rdi+0xF0` pair the create passes.

Interior anchor `005671DC` (function `00567190`).

`00566FE0` (259 B) is the paired flag-write `005674B0` runs on `[+0xC0]`'s record: `byte[+0x150]` <= 1 clears bit 0 of `+8` on both `[+0x60]`-indexed objects (`+0xDA` then `+0xD8`); a value > 1 sets both bits, then `[+0x150]` bit 0x1C writes `[+0xC0]+0xE6` = `(byte[+0x150] - 1)·arg`, else `+0xE6` = `(arg - byte[+0x152])·([+0x150] >> 24 & 0xF) - (byte[+0x150] - 1)·arg` — the offset compute behind the slot fill.

Interior anchor `00567051` (function `00566FE0`).

`00566B70` (156 B) is the timer-start writer `005674B0` runs on the slot record: gated on `[+0xE8]` bit 0 and `[+0xE0]` != `dx`, it writes `+0xC4` = `word[+0xD4]`, `+0xC8` = `r8w - word[+0xD4]`, `+0xC0` masked to `((r9 & 0xF) << 2) | 1`, `+0xC6`/`+0xCA` = `word[+0xD6]`, `+0xD0` = `0208F570`, `+0xE0` = `dx`, and `+0xCC` = `stack arg·60/1000` via the `0x10624DD3` magic multiply — the milliseconds-to-ticks conversion.

Interior anchor `00566BAB` (function `00566B70`).

`00564300` (115 B) is the `+0x180` index-step `0056DED0`/`00564E10`/`003FDAD0` run on the same record `00564780` populates: the bits-21-25 index is decremented and compared against the bits-26-31 field — `field >= index - 1` clears the index bits to 0, else the field increments by one (`+0x200000` folded under `0x3E00000`); `[0209AC30]+0xDE9` is stamped 4 and 1 returns on both arms.

Interior anchor `00564337` (function `00564300`).

`00563EC0` (74 B) is the decrement sibling of `00564300`: `(+0x180 & 0xFFE00000) << 6` positive keeps `eax` on the `0xFFE00000` field alone, otherwise `eax` = `(+0x180 & 0xFFFF0000) << 5`; `eax - 1` then folds back into the `+0x180` bits-21-25 index under the `0x3E00000` mask; `[0209AC30]+0xDE9` is stamped 8 and 1 returns.

Interior anchor `00563EF0` (function `00563EC0`).

`002FAE40` (114 B) is the bank-recipe row read: `edi` bounds-checks `word[02EBF158 + 6]`, the row address is `word[+4] * edi` atop the `0020E600(+8)`-resolved base, and the body returns `word[row]` (0 on any out-of-range or empty descriptor) - the element getter the flag-bank and recipe callers share.

Interior anchor `002FAE9F` (function `002FAE40`).

`002CBDA0` (158 B) is the get-or-create `0057C070` runs on `[0209AC30]+0x2E0`: an empty slot builds a `0x170` widget through `00244F50` with proc `002CBF80` and packet `{rcx, edx, 1, 7}` and caches it; a live slot whose `[+0x7C]` bit `0x20` is set instead `00246AD0`-frees `[0208EA28]`

Interior anchor `002CBE02` (function `002CBDA0`).
