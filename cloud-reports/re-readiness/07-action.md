# Reconstruction readiness: 07-Combat-Action

- **System folder:** `FFXII TZA/07-Combat-Action/` (every `.md` page in the folder and its subfolders; member `.tsv` files consulted only to confirm layouts and counts)
- **Board task:** OPUS-CLOUD-R-READINESS-07-1002
- **Date:** 2026-10-02
- **Brief:** `docs/cloud-briefs/re-readiness.md` (stream R). This is a draft written from the text snapshot only. Nothing here was checked against the executable.

## Counts

*(Filled in when the report is complete; see the end of this section.)*

## How to read the citations

Every citation is `page:line`, where `page` is the path **below `FFXII TZA/07-Combat-Action/`** exactly as the table
below lists it, and `line` is the line number in that file at the snapshot this branch was cut from (`main` at
`c3aec14d`). A range `:a-b` covers lines a to b. "Not stated" means no page in the folder says it.

## Pages read, with the status each page states

| page | status, as the page states it |
|---|---|
| `README.md` | no status line (category README); its own system list gives per-page statuses (`README.md:13-40`) |
| `the-moment-an-action-is-committed.md` | `status: AUDITED`, `evidence_tier: 1`, `falsification_passes: 1` (`:4-6`, `:19`) |
| `CONTRACT-commit-action.md` | `level: L1`, `readiness: BEHAVIORALLY UNDERSTOOD`, `confidence: PROVEN`, `crossref_clean: false` (`:5-7`, `:22`) |
| `CONTRACT-the-moment-an-action-is-committed.md` | `level: L2`, `readiness: CONTRACT READY`, `confidence: PROVEN`, `crossref_clean: false` (`:5-7`, `:24`) |
| `Command-And-Action-Seam/native-command-seam.md` | `status: DOCUMENTED`, `evidence_tier: 1`, `reopened_count: 2` (`:4-6`, `:25`) |
| `CONTRACT-native-command-seam.md` | `level: L2`, `readiness: CONTRACT READY`, `confidence: PROVEN`, `crossref_clean: false` (`:5-7`, `:24`) |
| `Action-Dispatch/battle-action-handler-table.md` | `status: DOCUMENTED`, `evidence_tier: 1`, `passes: 4` (`:4-6`, `:24`) |
| `CONTRACT-battle-action-handler-table.md` | `level: L2`, `readiness: CONTRACT READY`, `confidence: PROVEN`, `crossref_clean: false` (`:5-7`, `:24`) |
| `Action-Availability/battle-command-availability-and-reason-codes.md` | `status: AUDITED — … every box ticked, status line brought up to date 2026-09-18 (FABLE)` (`:4`); the body opens "**PARTIAL.**" (`:32`) |
| `Action-Definition-Row/the-action-definition-row.md` | `status: DOCUMENTED — GR-4, GR-5, GR-6, GR-7 and UQ-107 are ANSWERED and UQ-106 is SUPERSEDED …` (`:4`) |
| `how-an-action-gathers-its-targets.md` | `status: DOCUMENTED`, one falsification pass 2026-09-29 (`:4`, `:15-18`); its note still says "Pending first review" (`:23`) |
| `how-close-a-unit-must-stand-to-act.md` | `status: AUDITED` (`:4`), "promoted: 2026-10-01 DOCUMENTED -> AUDITED" (`:24`) |
| `how-a-combo-continues-and-what-it-blocks.md` | `status: DOCUMENTED — GR-3 is ANSWERED …` (`:4`), `crossref_clean: false` (`:25`) |
| `CONTRACT-combo-continuation.md` | `level: L2`, `readiness: CONTRACT READY`, `confidence: PROVEN`, `crossref_clean: false` (`:5-7`, `:24`) |
| `CONTRACT-battle-target-buffer.md` | `level: L1`, `readiness: DIFFERENTIAL TESTED`, `confidence: PROVEN`, `crossref_clean: false` (`:5-7`, `:22`) |
| `Result-Record/the-result-record-field-map.md` | `status: AUDITED`, `level: L1`, `readiness: BEHAVIORALLY UNDERSTOOD` (`:4`, `:7-8`) |
| `applying-a-result-to-a-target.md` | `status: DOCUMENTED` (`:4`); `production_review: "… current T2 peer review pending."` (`:26`) |
| `CONTRACT-apply-result-to-target.md` | `level: L2`, `readiness: BEHAVIORALLY UNDERSTOOD`, `review_status: "Production correction; T2 peer review and canonical acceptance remain pending."` (`:5-6`, `:14`) |
| `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md` | `status: AUDITED`, `level: L1`, `readiness: BEHAVIORALLY UNDERSTOOD` (`:4`, `:7-8`) |

**Member files consulted** (layouts and counts only):

- `Post-Result-Events/battle-message-rows.tsv`: 102 data rows (`id`, `row_bytes`, `text_us`). Slot-0 kind bytes are
  `02` ×34, `01` ×33, `00` ×29, `07` ×4, `03` ×1, `08` ×1, and 28 rows have a non-zero byte `+4`. All three figures
  match the page (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:567`, `:606-608`, `:655`).
- `Result-Record/result-record-accesses.tsv`: 245 data rows, as stated (`Result-Record/the-result-record-field-map.md:225`).
  It holds **40** distinct functions and **53** distinct displacements, against the page's "39 functions over 52
  offsets" (`:15`). See contradiction C7.
- `Action-Definition-Row/members/action-row-reader-hops.tsv`: 232 data rows, as stated
  (`Action-Definition-Row/the-action-definition-row.md:48`). It has 23 rows at offset `0x0C` and 40 at `0x2C`.
- `Action-Definition-Row/members/action-row-0x2C-bit-readers.tsv`: 40 data rows, as stated (`:199`).
- `Action-Definition-Row/members/action-row-0x0C-bit-readers.tsv`: 25 data rows. Its own header says it covers "the 23
  sites" and that it is "SUPERSEDED as a census 2026-09-27 … 23 of the 60 provenance-verified reads" (tsv line 1).
  See contradiction C8.

---

## 1. Interface

The folder documents eight connected parts:

1. **Intent and commit.** The command seam, the commit, the cancel and the command block.
2. **The two rings.** The presentation-ready ring and the pending action-selection ring.
3. **Dispatch.** The 13-phase standard pipeline and the 359-slot order handler table.
4. **Availability.** The reason-code cascade and the menu builder.
5. **Action data and geometry.** The 60-byte action definition row, target gathering and range bands.
6. **Combos.**
7. **Targets and results.** The battle target buffer, the 0x148-byte result record and the applier.
8. **Messages.** The post-result events and the battle message table.

### 1.1 Entry points (functions, with their callers)

**Intent, commit and cancel**

| function | size | what it is | callers | cite |
|---|---:|---|---|---|
| `00311CF0` `BattleUnit_IssueCommand` | 283 B | the intent seam. Records the command at `+0xBA0` and the target at `+0xBB8`, and marks them pending with `+0xBA4` bit 15 and unit bit 14. Never writes `+0x708`/`+0x710`/`+0x714`. Returns 0 for both refusal and success, −2 for a null stats record or the `0x80000003` gate | `00311B20` (fan-out) and `003138D0` (defeat cleanup) | `CONTRACT-native-command-seam.md:66-79`, `:240` |
| `00311CD0` / `00311B20` | 26 B / 426 B | the by-focus-handles wrappers; UI enters through them | `BattleMenu_UpdateCommandSelectionAndDispatch` `002778C0`, `0027C3D0` | `Command-And-Action-Seam/native-command-seam.md:43-48`, `:574` |
| `0030F760` `BattleUnit_CommitAction` | 570 B | `(unit, actionData, u16 actionId, u32 targetId, int alsoPrepare)` → 1 committed / 0 refused | `00305AB0` `BattleUnit_SelectAndCommitNextAction` (issued command, or the gambit / AI order sets via `00305CC0`), `0030FA00` (combo), `00312FA0` (engage auto-attack) | `the-moment-an-action-is-committed.md:54-57`; `CONTRACT-commit-action.md:41-47`; `Command-And-Action-Seam/native-command-seam.md:95-101` |
| `003105D0` `BattleUnit_CancelAndResetCurrentAction` | 418 B | the cancel. Gated on a null unit and on a null `+0x698` (both no-ops); turns the shadow into the cancelled record | the commit (fifth argument), `00236A60`, `00300E40`, `00300FC0`, `003266C0`, `00300140`, `00301140`, `002FEF30`, `00308610` | `the-moment-an-action-is-committed.md:109-135`; `CONTRACT-the-moment-an-action-is-committed.md:105-108`, `:269`, `:271`, `:273`, `:289` |
| `00308610` `BattleUnit_UpdateCombatFrame` | 461 B | the per-unit combat frame. Calls select-and-commit, the interrupt check `002FFB60`, the advance `00307BE0`, the combo continue, the cancel and `00308270` | `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` | `CONTRACT-the-moment-an-action-is-committed.md:269`, `:271`; `how-a-combo-continues-and-what-it-blocks.md:206` |

**Advancing and dispatching an action**

| function | size | what it is | callers | cite |
|---|---:|---|---|---|
| `00307BE0` `BattleUnit_AdvanceActionState` | 137 B | returns −1 when `+0x708` is null. Splits on `+0x714 > 0x21E` into extended / standard, bumps `+0x75C` when `+0x768 ≥ +0x76C`, and calls `004697C0` on `r == 1` | `00308610` | `Action-Dispatch/battle-action-handler-table.md:575-598`; `CONTRACT-the-moment-an-action-is-committed.md:271` |
| `00304850` `BattleUnit_AdvanceStandardActionState` | 2,034 B | the 13-phase machine on `byte [unit+0x6B0+4]` | `00307BE0` | `Command-And-Action-Seam/native-command-seam.md:189-217` |
| `00305080` `BattleUnit_AdvanceExtendedActionState` | 249 B | posts event `0x2001` (`0x2010` in one case), then tail-jumps to `01EEC460[id − 0x4000]`; −1 out of range or empty | `00307BE0` | `Action-Dispatch/battle-action-handler-table.md:69-95`; `CONTRACT-battle-action-handler-table.md:77-106` |
| eight order handlers | — | `002FDDA0` ×249, `002FDA60` ×57, `002FDC30` ×25, `002FE660` ×6, then `002FE7D0`, `002FE840`, `002FE8D0`, `002FE910` ×1 each | the extended dispatcher's `jmp rdx` | `CONTRACT-battle-action-handler-table.md:228`; `Action-Dispatch/battle-action-handler-table.md:120-129` |
| `00301830` `AiOrder_CheckActionPreconditions` | — | the availability half of the order table. Same bound and emptiness test, then per-id preconditions | `AiOrder_EvaluateAndResolveActionTarget` `003014C0` | `Action-Dispatch/battle-action-handler-table.md:97-107`, `:218-244` |

**Availability**

| function | size | what it is | callers | cite |
|---|---:|---|---|---|
| `002FFCF0` `BattleAction_CheckActionAvailabilityReason` | 479 B | `(u16 actionId, unit)` → 0 or one of nineteen reason codes. Every caller tests only zero / non-zero | seven: `002FFB60`, `003014C0`, `00305AB0`, `00307300`, `0030DB70`, `00317BC0`, `0031EB20` | `Action-Availability/battle-command-availability-and-reason-codes.md:75-113`, `:531-542`, `:552-562` |
| `0031EB20` `BattleMenu_BuildCommandEntryList` | 4,182 B | `ctx` has the kind at `+0`, the handle at `+8`, the id at `+0x1C`, entries at `+0x50`, the count at `+0x40` and the default at `+0x44`. Kinds `0xC`–`0x10` redirect to kind `0x1B` | 16 UI sites | `Action-Availability/battle-command-availability-and-reason-codes.md:58-60`, `:331-379` |

**Action geometry and combos**

| function | size | what it is | callers | cite |
|---|---:|---|---|---|
| `0030D160` `Battle_BuildActionTargetSet` | 1,004 B | `(actor, actionId, focusHandle, buffer)` → count | `00304EE2` (phase 9) | `how-an-action-gathers-its-targets.md:36-44` |
| `0031A990` | 154 B | the shape descriptor, shapes 0–5 | a wrapper with three callers, one of them a menu helper | `how-an-action-gathers-its-targets.md:132-140` |
| `002FEB80` | 476 B | the range-band builder `(actor, target, row, outReach, outMiddle, outNear)` | `00304AB9` (phase 3) | `how-close-a-unit-must-stand-to-act.md:36-51`, `:179` |
| `00309300` / `00320D70` | 169 B / 146 B | the reach, and the inner band components | `002FEB80` | `how-close-a-unit-must-stand-to-act.md:53-74` |
| `0030FA00` `BattleAction_TryContinueComboSequence` | 146 B | re-commits the same action, then increments `+0x6B7` | `00308610` at `0030879F`, only when target-buffer entry 0 has bit 10 | `how-a-combo-continues-and-what-it-blocks.md:79-100`, `:280-284` |
| `0030C010` | 179 B | the combo continue gate (six tests) | `0030FA00`; `0031ADB0` | `how-a-combo-continues-and-what-it-blocks.md:151-167` |
| `00388660` `BattleFormula_RollAndStoreComboCount` | 602 B | rolls once per combo and memoises the count | calculator slot 10 of `01EFA5C0`, from the resolver loop `003863D0` and the preview loop `003859FF` | `how-a-combo-continues-and-what-it-blocks.md:285-289`; `CONTRACT-combo-continuation.md:98-113` |

**Target buffer, rings and presentation slots**

| function | size | what it is | callers | cite |
|---|---:|---|---|---|
| `00316CD0` / `00316CF0` / `00316D70` / `00316D30` | 24 / 57 / 47 / 60 B | target buffer append / reset (keeps flag bit 0) / find / reset-and-set-bit-0 | 19 sites in 10 functions (§15a); `00316D30` from `00236A85` and `003087C6` | `CONTRACT-battle-target-buffer.md:44-48`, `:556-572`, `:370-375` |
| `00313DB0` | 360 B | the presentation-ready ring drain, no arguments; publishes `02089350` and calls `00313A00` | `00234520` (every call) | `Command-And-Action-Seam/native-command-seam.md:56-75`; `CONTRACT-native-command-seam.md:263` |
| `00313CD0` `BattleUnit_ProcessPendingActionSelectionQueue` | 220 B | pops up to 8 per call from a 64-entry ring and hands each unit to `00305AB0` | `00234520` (only with the navigation dataset) | `CONTRACT-native-command-seam.md:91-103`, `:255`, `:263` |
| `0030CA80` `BattleAction_CheckPresentationSlotReady` | 352 B | the ready check (return) and should-play (out-parameter) | `00304850` only | `Command-And-Action-Seam/native-command-seam.md:357-414`, `:470-471` |
| `0030CFB0` / `0030D070` / `0030C970` / `0030CF40` / `0030A250` | — | presentation slot acquire / allocate / release / reset / pool reset | phases 3 and 6, the cancel and others | `the-moment-an-action-is-committed.md:263-272`; `Command-And-Action-Seam/native-command-seam.md:118`, `:591` |
| `0030CBE0` | 556 B | the slot walker that advances the three track states | `BattleSystem_RunFieldFrameOrchestrator` `00234590` | `Command-And-Action-Seam/native-command-seam.md:440-441`, `:576` |

**Results and messages**

| function | size | what it is | callers | cite |
|---|---:|---|---|---|
| `003848E0` `BattleFormula_InitializeResultRecord` | 205 B | the result-record defaults | the resolver's callers; `00386A50` / `00386A70` / `00386AE0` | `Result-Record/the-result-record-field-map.md:48`; `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:456-457` |
| `003112F0` `BattleFormula_ApplyTargetResult` | 2,040 B | `(record, sourceStats, targetStats, u16 id, u32 callerFlags)`, `void` | `Battle_ProcessActionTarget` `00307300`, periodic maintenance `00310DB0`, `0030E130`, `0030E360` | `CONTRACT-apply-result-to-target.md:45-54`; `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:440-444` |
| `00385BA0` `BattleFormula_ApplyResultMetadata` | 250 B | the echoes, the steal-bit clears and the dispatch gate | `003112F0` at `0031137A` (only caller) | `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:49-59` |
| `00469EC0` `BattleFormula_DispatchPostResultEvents` | 1,904 B | builds the event context, then posts by two "worlds" | `00385BA0` | `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:61-142` |
| `0046AB10` | 371 B | the poster: drop, filter, rate limit, ring, realise | 48 sites in 18 functions | `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:144-156`, `:571`, `:580-590` |
| `00469570` / `005369C0` / `00536410` / `0035B990` | 303 / 1,000 / 1,420 B / — | the filter, the realiser, the slot formatter, and the hand-off to the HUD | `0046AB10` chain | `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:158-247` |

### 1.2 Inputs and outputs (data read and written, with record layouts)

**BattleUnit fields this folder writes or reads.** The base layout is owned by
`04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` (`CONTRACT-commit-action.md:8`).

| offset | type | meaning | cite |
|---|---|---|---|
| `+0x00` | flags | bit `0x10` live/can act; bit 12 (`0x1000`) queued in the presentation ring; bit 13 (`0x2000`) shown; bit 14 player-issued; bit 22 engage auto-attack in progress; bit 23 engaged; bit 24 suspend refusal; bit 46 set in phase 9 | `Action-Availability/battle-command-availability-and-reason-codes.md:217`; `Command-And-Action-Seam/native-command-seam.md:467-481`, `:342`; `how-a-combo-continues-and-what-it-blocks.md:169-178`; `CONTRACT-commit-action.md:46`; `Command-And-Action-Seam/native-command-seam.md:207-208` |
| `+0x690` | u8 | `animationEventFlags`; bits 1 and 3 gate the phase-10 clear | `Command-And-Action-Seam/native-command-seam.md:208` |
| `+0x694` / `+0x695` / `+0x696` | u8 ×3 | the three stages of one presentation-slot handle, `0xFF` = empty | `the-moment-an-action-is-committed.md:263-272` |
| `+0x698` / `+0x6A0` | ptr | the stats record (kind byte `+5`: 0 party table, 1 enemy table) / the spawn-keep entry (flag byte `0x30`, `0x48`) | `Action-Availability/battle-command-availability-and-reason-codes.md:305-324`; `Action-Dispatch/battle-action-handler-table.md:379-394` |
| `+0x6B0` | context base | bit 1 = a slot was parked for this command; `+0x6B0 + 4` = `+0x6B4` | `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:478-481`; `Command-And-Action-Seam/native-command-seam.md:190-194` |
| `+0x6B4` | u8 | phase 0–12 | `Command-And-Action-Seam/native-command-seam.md:196-210` |
| `+0x6B6` / `+0x6B9[]` | u8 / u8[] | the pending slot-target count and the slot list | `how-an-action-gathers-its-targets.md:97-101` |
| `+0x6B7` / `+0x6B8` | u8 / u8 | combo progress / the combo's running hit tally | `how-a-combo-continues-and-what-it-blocks.md:59-72`, `:349-366` |
| `+0x6D4` / `+0x6D8` / `+0x6DC` | float | near / middle / reach (copied to `+0x1A0` / `+0x1A4` / `+0x1A8`) | `how-close-a-unit-must-stand-to-act.md:33-34`, `:179` |
| `+0x700` / `+0x708` / `+0x710` / `+0x714` | u32 / ptr / u32 handle / u16 | the command block: flags (low two bits cleared), order record, target focus, action id | `CONTRACT-the-moment-an-action-is-committed.md:53-62`; `CONTRACT-native-command-seam.md:51-59` |
| `+0x718..+0x72F` | 24 B | the shadow of `+0x700..+0x717` | `CONTRACT-commit-action.md:86-101` |
| `+0x730..+0x747` | 24 B | the cancelled record (`+0x740` target, `+0x744` id) | `the-moment-an-action-is-committed.md:122-142` |
| `+0x750` / `+0x754` | u32 | the group target (follower copy / leader broadcast) | `CONTRACT-commit-action.md:143-165` |
| `+0x75C` / `+0x760` / `+0x764` / `+0x768` / `+0x76C` | — | the action age counter; a phase-1 accumulator and its limit (not named); the charge pair | `Action-Dispatch/battle-action-handler-table.md:198-199`, `:587`; `Command-And-Action-Seam/native-command-seam.md:216`; `how-close-a-unit-must-stand-to-act.md:113` |
| `+0x770` | — | the re-commit latch | `CONTRACT-commit-action.md:333-341` |
| `+0x778` / `+0xBC0` | `BattleTargetBuffer` 0x208 | the action target buffer / the perception candidate cache | `CONTRACT-battle-target-buffer.md:36-38` |
| `+0x988` | 32 × 16 B | redirected entries, paired with the buffer entries, used for code 8 | `CONTRACT-battle-target-buffer.md:427-432` |
| `+0xB88` | ptr | the suspend-slot pointer; the snapshot / restore range is `[+0x6B0, +0xBA0)` | `CONTRACT-commit-action.md:354` |
| `+0xBA0` / `+0xBA4` / `+0xBB8` | — | the issued command id / its flags / its target | `CONTRACT-native-command-seam.md:72-73` |
| `+0xE58` | — | the gil cost reserved for the action in progress | `Action-Availability/battle-command-availability-and-reason-codes.md:303` |
| `+0xE9A` | u8 | bit 2 = Poison tick, bit 3 = taken not struck (transient during apply) | `applying-a-result-to-a-target.md:168`, `:185` |
| `+0xEA0` / `+0xEA4` / `+0xEA8` / `+0xEA9` | u32 / u32 / u8 / u8 | the mask cleared by cancel / the attacker mask / its cardinality / the unit's slot | `the-moment-an-action-is-committed.md:192-250`; `CONTRACT-commit-action.md:119-135` |

**`BattleTargetBuffer`** (0x208 B, packed):

| offset | field | cite |
|---|---|---|
| `+0x00` | u8 flags; bit 0 survives a reset; on `+0xBC0` it is the "cache current" gate | `CONTRACT-battle-target-buffer.md:57-59`, `:351-369` |
| `+0x01` | keyType: 0 none, 1 int, 2 float | `:60`, `:441-443` |
| `+0x02` | pickRule: 0 nearest, 1 random, 2 min, 3 max | `:61`, `:441-443` |
| `+0x03` | unwritten | `:62` |
| `+0x04` | i32 count, signed | `:63` |
| `+0x08` | 32 × 16-byte entries: `{+0 actorWork*, +8 outcome word, +0xC unknown}` | `:64-72` |

The outcome word holds byte 0 = the target-entry code, then bits 8 / 9 / 10 / 11 (`:413-417`). The cap is 32, and
append returns the count, not a status (`:157-191`). The pseudo-code is at `:207-226`.

**Action definition row** (60 B, 543 rows, `battle_pack.bin` directory `+0x3C`; registry slot `02EBF138` with header
`{+4 count 543, +8 stride 60, +0xC rows}`). Every offset with its reader and meaning is at
`Action-Definition-Row/the-action-definition-row.md:55-90`. The header is at `:122`, and the row idiom at `:38-46`.
Three byte ranges have no reader by statement: `+0x0B`, `+0x21`, and `+0x0C` bits 15, 18 and 20 (`:192-194`,
`:203-204`).

**Order handler table.**
- The table is `01EEC460`, 359 qwords, index `id − 0x4000`, bounded at `0x166`. It has 341 live slots, 18 empty
  slots and 8 handlers (`Action-Dispatch/battle-action-handler-table.md:54-65`). The empty ids are at `:141-145`.
- The order record's second word `[order+2]` is the wait count `n` for `0x4021` (`:197-200`). For the rolled band it is
  the percent chance (`:229`, `:242-244`).

**Presentation slot** (32 × 0x30 at `022C17B0`; `Command-And-Action-Seam/native-command-seam.md:517-527`):

| offset | field |
|---|---|
| `+0x00` / `+0x08` | the next / previous links |
| `+0x10` / `+0x14` / `+0x18` | three track states, `1 → 2 → 3` |
| `+0x1C` | u16 action id, `0xFFFF` = free |
| `+0x1E` | padding |
| `+0x20` | the owner's focus handle |
| `+0x24` / `+0x28` | two resource handles |
| `+0x2C` | flags |

**The two rings.** Both are `{u8 read, u8 write, 64 × 8-byte packed IDs}`: the presentation ring at
`022BEDA0` / `022BEDA1` / `022BEDA4`, and the pending action-selection ring at `022BE980` / `022BE981` / `022BE984`.
The advance is `(read+1) & 0x3F`, and the ring is empty when `read == write`
(`Command-And-Action-Seam/native-command-seam.md:124-135`).

**Result record** (0x148 B, a stack local in every caller; `Result-Record/the-result-record-field-map.md:131-140`).
- The field map is at `:66-120`.
- The initialiser's sentinels are at `:48`.
- Absence is field-specific: masks use zero, layer and level bytes use `0xFF`, the item dword uses −1, copies skip
  negatives (`CONTRACT-apply-result-to-target.md:81-94`).

**Reason codes.** There are nineteen codes, listed at
`Action-Availability/battle-command-availability-and-reason-codes.md:463-482`. The status-to-code mapper `0030E9C0`
is at `:436-447`, and the resource leg at `:489-499`.

**Battle message table.** `battle_message.bin` is an `st2e` table: 102 rows × 8 B in `us`, 100 in `ch` / `cn` /
`in` / `kr` (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:249-263`, `:299-304`).

| offset | field |
|---|---|
| `+0`, `+1`, `+2`, `+5` | the four slot kinds |
| `+3` | bit 7 = always show; bits 2–6 = category |
| `+4` | bit 0 = rate-limited |
| `+6` | u16, zero |

Also on that page:
- The event context is at `:66-71`.
- A ring entry is `{+0 u16 event, +4 u32 tick, +8 stats*}`, 32 B × 10 at `02EBB560` (`:384`, `:155`).
- A log line node is 0x198 B (`:386`).

**Combo count record.** A 64-byte record, with the count in the high nibble of `+0x12`:
- for a party unit, at `0208D480 + byte[+4] × 0x40`;
- for a foe, at `0208DE80 + unit[+0xEA9] × 0x40`.

See `CONTRACT-combo-continuation.md:121-123` and `Action-Dispatch/battle-action-handler-table.md:642-664`. Contradiction
V3 covers the pages that give only the first table.

**Outputs to other systems.**
- The target's `+0xEA4` / `+0xEA8` and the enmity notify `00313B30`. The notify sends the dispatch record
  `{+0 kind, +1 flag, +4 uid, +8 aid, +0xC tid}` to `002ED2A0` (`CONTRACT-commit-action.md:342-347`).
- Presentation events `0x2001` / `0x2010` (`CONTRACT-battle-action-handler-table.md:100-106`).
- Sound `0x34` (`applying-a-result-to-a-target.md:168`).
- Gil, items, levels and status changes through the applier (`CONTRACT-apply-result-to-target.md:164-170`).
- Battle-log lines (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:186-247`).
- The battle-state block's `+0x5B00` / `+0x5B0E` (`:54`).

### 1.3 State (globals and objects, with lifetime)

**Tables and pools**

| state | lifetime / initial value | cite |
|---|---|---|
| `01EEC460` order handler table | static `.data`; the qword after it is `0000000400000002` | `CONTRACT-battle-action-handler-table.md:65-68` |
| `022C17B0` presentation slot pool, list heads `022BE978` / `022BEB88` | zero-initialised `.data`; the pool reset `0030A250` is a single call with no clear of the array | `Command-And-Action-Seam/native-command-seam.md:515`, `:591` |
| the rings `022BEDA0` and `022BE980` | emptied by `0030FE60` from `002341C0` (the battle-state reset) and `BattleSystem_InitializeAreaState` `002342F0`. Load-time value: not stated | `CONTRACT-native-command-seam.md:257`, `:273`; `Command-And-Action-Seam/native-command-seam.md:313` |
| `02EBF138` action table | bound once at boot from the STATIC blob and never rebound | `Action-Definition-Row/the-action-definition-row.md:176-179`, `:220` |
| `02EBF018` message table | bound by `002368D0` → `003843F0(0x13, 00238850, "STATIC")` → `00236C30` → `003845F0` | `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:283-299` |
| `0208D480` / `0208DE80` 64-byte records | `00386C10` clears only the first 32 bytes; "what survives is not established" | `Action-Dispatch/battle-action-handler-table.md:642-664` |
| `022C1DB0` (12-byte rows per slot) | written by `IssueCommand` (the parked slot at row `+8`) and by the engage auto-attack (save of `+0xDC8` / `+0xE58`); no single row layout | `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:478-481`; `how-a-combo-continues-and-what-it-blocks.md:173`, `:220` |

**Globals and scratch**

| state | lifetime / initial value | cite |
|---|---|---|
| `02089350` current presentation unit | written by area-state init and by `00313DB0`'s publish and clear | `Command-And-Action-Seam/native-command-seam.md:137`, `:315` |
| `02089340` battle flags | bits `0x10`, `0x200` / `0x400`, `0x3080` read. Owner and initial value: not stated in this folder | `Command-And-Action-Seam/native-command-seam.md:419-430`, `:506-510`; `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:152` |
| `02EBB560` / `02EBB54C` event ring; `02EBB540` steal list | process globals. Initial value: not stated | `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:155`, `:326` |
| `02EBF188` | write-only scratch, 93 stores, no reader | `how-a-combo-continues-and-what-it-blocks.md:389-402` |
| `02AEDFD4` parked action id | stored by the resolver at `00385FE4`; read by the dispatch | `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:58-59` |
| `022C2160` special-sequence state | read by the combo gate (0 or 7) and phase 10 (5 or 6). Owner: not stated in this folder | `how-a-combo-continues-and-what-it-blocks.md:163`; `Command-And-Action-Seam/native-command-seam.md:208` |
| `01DFE0B4` frame base | 1 as shipped, 2 at 60 fps; one writer `001EDDF2` | `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:610-619` |
| `01EEBAF0` / `022BE930` debug override | `FFFFFFFF` file value. The copy into `022BE930` happens only in `002F79E0` | `Action-Availability/battle-command-availability-and-reason-codes.md:706-714` |

**Per-unit and per-call state**

| state | lifetime / initial value | cite |
|---|---|---|
| result record | stack local per resolve / apply call, 0x148 B, `memset` by three callers | `Result-Record/the-result-record-field-map.md:131-140` |
| unit `+0xBC0` flag bit 0 | born 1 (`00172CA1`); no clearer found | `CONTRACT-battle-target-buffer.md:356-369` |
| unit `+0x694`–`+0x696` | `0xFF` from `BattleUnit_ResetStateForReuse` | `the-moment-an-action-is-committed.md:272` |
| unit `+0x718` / `+0x730` | stamped from the live block by `00236A60` | `CONTRACT-the-moment-an-action-is-committed.md:177-178` |

At spawn: not stated for the other unit fields this folder uses: `+0x6B4`, `+0x6B7`, `+0x770`, `+0x750` / `+0x754`,
`+0xEA0` / `+0xEA4` / `+0xEA8`, and `+0x760` / `+0x764`.

### 1.4 Order (what runs when, and what triggers it)

1. **Per frame, world level.**
   - `00234520` (the tick's slot-0 step) runs the party suppression recompute. It then drains the presentation ring
     on every call, and the action ring only when the navigation dataset is present (`CONTRACT-native-command-seam.md:263`;
     `README.md:68`).
   - `BattleSystem_RunFieldFrameOrchestrator` `00234590` runs the slot walker `0030CBE0` and `00313A00`
     (`Command-And-Action-Seam/native-command-seam.md:576`).
   - **Not stated:** the order of `00234520` and `00234590` relative to each other and to the per-unit frames.
2. **Per unit.** `00233F70` → `BattleUnit_UpdateCombatFrame` `00308610` (`CONTRACT-the-moment-an-action-is-committed.md:269`).
   That frame reaches:
   - select-and-commit `00305AB0`;
   - the advance `00307BE0`;
   - the combo continue at `0030879F`, gated on target-buffer entry 0 bit 10 (`how-a-combo-continues-and-what-it-blocks.md:280-284`);
   - `00308270`;
   - the cancel.

   **Not stated:** the order of those calls inside `00308610`.
3. **Intent to commit.** `IssueCommand` records `+0xBA0` / `+0xBB8` only. A later `00305AB0` commits the issued command
   from those fields (`CONTRACT-native-command-seam.md:71-76`; `Command-And-Action-Seam/native-command-seam.md:95-98`).
4. **Inside the commit:**
   1. the optional cancel;
   2. resolve the target;
   3. the two-band id test;
   4. band one only: reset and append the target buffer;
   5. the block and its shadow;
   6. `+0x770`;
   7. band one only: the propagation walk;
   8. the mask and the notify.

   See `CONTRACT-commit-action.md:167-185`. Contradiction V1 covers the §12 formula that does not match this order.
5. **Standard action, phases 0–12** (`Command-And-Action-Seam/native-command-seam.md:196-217`).
   - Phase 3 is setup: the band builder at `00304AB9` (`how-close-a-unit-must-stand-to-act.md:179`) and the release of
     the three slots.
   - Phase 4 is the approach and charge.
   - Phase 6 acquires the presentation slot.
   - Phase 7 is the ready check and the enqueue.
   - Phase 9 builds the target set at `00304EE2` and dispatches the presentation event.
   - Phases 10–12 wait and finish.
   - Re-entry points: `2` (direct-state orders) and `5` (combo, engage) (`how-a-combo-continues-and-what-it-blocks.md:403-421`).
6. **Extended action.** `00307BE0` → `00305080` posts the event, then tail-calls the handler. The handler re-reads
   `+0x714` (`CONTRACT-battle-action-handler-table.md:77-98`).
7. **Result.**
   1. Per target entry, `Battle_ProcessActionTarget` `00307300` (called "from the two timeline-event handlers") runs.
   2. It initialises and resolves, then applies.
   3. The applier runs 20 steps (`applying-a-result-to-a-target.md:164-186`; contract order at
      `CONTRACT-apply-result-to-target.md:182-198`).
   4. Then the metadata, the dispatch, the poster and the realiser run
      (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:398-408`, `:443`).

   **Not stated in this folder:** which timeline event triggers `00307300`, and in which phase.
8. **The combo loop.** The roll sets flag B bit 1, which becomes entry bit 10. The frame then calls continue, which
   re-commits at phase 5 (`how-a-combo-continues-and-what-it-blocks.md:291-294`).

### 1.5 Dependencies (on other systems)

| system | what this folder relies on | cite |
|---|---|---|
| CombatAI (09) | the selectors that call the commit; the order-set walk; the 249-id handler's arm map | `CONTRACT-native-command-seam.md:255`; `how-a-combo-continues-and-what-it-blocks.md:240-243` |
| CombatFormula (08) | the resolver `00385F60`, the recipes and the calculator slot table `01EFA5C0`; the effective-action-id pair `00387090` / `00387A50`; the HP / MP setters | `how-a-combo-continues-and-what-it-blocks.md:267-273`; `the-moment-an-action-is-committed.md:346` |
| Status (10) | `0030E360`, `0030E130`, `0030FED0`; the effect-slot timers `+0x17C` | `CONTRACT-apply-result-to-target.md:263-273` |
| Movement (06) | the locomotion path reset, approach, spacing and pacing; the order-goal decoder `00312730` | `how-close-a-unit-must-stand-to-act.md:96-117`; `Action-Dispatch/battle-action-handler-table.md:344-407` |
| Party (11) | the focus-handle resolver `0031B7E0`; the leader `003272A0`; the battle-state block `+0x5AE0` / `+0x5B00` / `+0x5B0E` | `CONTRACT-battle-action-handler-table.md:100-106`; `how-an-action-gathers-its-targets.md:189` |
| ActorEntity (04) | the unit table `00236820` / `00236850`; the field map; the kind byte | `CONTRACT-commit-action.md:8` |
| WorldAreaField (03) | `FieldData_GetActiveFieldRecordBit15` `00377C20` | `CONTRACT-commit-action.md:507-512` |
| RNG (21) | the MT19937 thunk `00379CD0` (combo, formula); the shared LCG `00328370` (order precondition, candidate pick) | `CONTRACT-combo-continuation.md:269`; `Action-Dispatch/battle-action-handler-table.md:229` |
| Items / License (12) | the item write `003008A0`; the licence check `00323EC0` | `CONTRACT-apply-result-to-target.md:277-281`; `Action-Availability/battle-command-availability-and-reason-codes.md:117-129` |
| UI / HUD (16) | the menu; the combo popup `0028AAA0`; the log widget; the text engines `002B49F0` / `002B40C0` | `how-a-combo-continues-and-what-it-blocks.md:425`; `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:186-247` |
| Resource (02) | the STATIC battle pack; the registry slots | `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:283-304` |
| Presentation / Audio | `003299B0`; `002ED2A0`; the sound pair `003A1180` / `002DF220`; `002DEE70` | `CONTRACT-native-command-seam.md:253`; `CONTRACT-apply-result-to-target.md:331` |

---

## 2. Gaps

### 2.1 Open or partly open items the pages themselves list

**No live evidence anywhere**

1. **Commit and target buffer.**
   - "**Evidence class: isolated original-code, over the whole function. Live capture: still absent.**"
     (`CONTRACT-commit-action.md:241`).
   - The caller has not been executed: "it still holds for the **caller**, which nothing has executed"
     (`CONTRACT-commit-action.md:326`).
   - The target buffer is the same: "Live capture: still absent." (`CONTRACT-battle-target-buffer.md:230`), with four
     live-only questions (`:277-300`).
2. **The other four contracts are native replay, not live.**
   - The seam, the handler table and the combo roll each say "the evidence class is native replay, not live"
     (`CONTRACT-native-command-seam.md:179-180`; `CONTRACT-battle-action-handler-table.md:159-160`;
     `CONTRACT-combo-continuation.md:187-188`).
   - The applier contract withholds "live-game reachability, and whole-system L2 acceptance"
     (`CONTRACT-apply-result-to-target.md:250-253`, `:299-305`).
3. **The message table binding has no live read.** "the runtime confirmation is still owed (`FL-2`)"
   (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:314-317`, `:542`).

**Commit, seam and rings**

4. **The commit's callees in a live game.** "nothing here shows what a real cancel, a real target-buffer reset or a real
   notify does with what this function hands it" (`CONTRACT-commit-action.md:302-305`).
5. **Rings.** "Whether the pending-selection ring can hold an entry that the commit funnel then rejects, and what happens
   to it if so." (`CONTRACT-native-command-seam.md:184-185`).
6. **Reset frequency.** "The frequency of these resets in live fights and the delegate's full effects are not
   established here" (`the-moment-an-action-is-committed.md:219-220`).
7. **What a presentation slot presents.** "**Not claimed:** what a slot record presents, why only the special-sequence
   update advances into `+0x696`, and whether a stage is ever skipped live" (`the-moment-an-action-is-committed.md:274-276`).

**Standard machine and presentation slots**

8. **13-phase machine.** "**Not read:** the called bodies beyond their names. `+0x760` / `+0x764` are `rsi`-relative
   `+0xB0` / `+0xB4`, and what they count was not named. Nothing was executed."
   (`Command-And-Action-Seam/native-command-seam.md:216-217`).
9. **Presentation slot.**
   - "**Not named:** which asset kind the `+0x10` loader and the `+0x14` event table hold" (`:465-466`).
   - "What codes `1` and `3` mean was not read." (`:537`).
   - "the `+0x2C` bits above bit 4" (`:540`).

**Order handlers and the order space**

10. **Order handlers.** "**What the eight handlers do.** Two are opened here only far enough to establish `HT-3`"
    (`CONTRACT-battle-action-handler-table.md:164-165`). Four handlers have no name
    (`Action-Dispatch/battle-action-handler-table.md:125-129`).
11. **The 64-byte records' surviving half.** "**what survives is not established here.**"
    (`Action-Dispatch/battle-action-handler-table.md:663-664`).

**Availability**

12. **The cost side.** "`FUN_003037A0`, `FUN_00309110`, `FUN_00308FF0`, … and `FUN_00253690` are unread …, so the
    *cost* side of the resource check is still opaque" (`Action-Availability/battle-command-availability-and-reason-codes.md:518-519`).
13. **Other availability items.**
    - "Which reason code a failed frustum test yields is not read here" (`:598`).
    - "the kind names are structural …; the four filter predicates in the rebuild are read only as calls" (`:377-379`).
    - OV-42: "Other action-id producers, natural action selection and whole OV-42 stay OPEN" (`:734-735`).

**Target gathering and range bands**

14. **Target gathering.**
    - "NOT read - the eligibility mask builder beyond its result, the three callers of the shape descriptor's wrapper,
      what the action state machine does around the call" (`how-an-action-gathers-its-targets.md:21-23`).
    - "The other two were not read." (`:140`).
15. **Range bands.**
    - "**Not read:** the further test of the back-off arm, the avoidance manoeuvre, the predicate of section 6, and the
      clearance tests; what reads `+0x05` on a bit-26 row." (`how-close-a-unit-must-stand-to-act.md:128-129`).
    - The per-character pairs under bit 26 "were not tallied here" (`:192-193`).

**Combo and target buffer**

16. **Combo.** The flag-bit-22 sweep: "A whole-qword store to the flag word is not covered by this sweep."
    (`how-a-combo-continues-and-what-it-blocks.md:187-188`).
17. **Target buffer.**
    - Bit 0's clearer: "either that arm is dead-in-ship, or a clearer hides behind a route the census cannot see"
      (`CONTRACT-battle-target-buffer.md:366-368`).
    - "`+0x0C` | 4 | — | — | **unknown span**" (`:72`).
    - "*Not established:* the value of `02F973B8`" (`:501`).

**Results and messages**

18. **Result record coverage.** "What it cannot see: fields written through pointers the slots store elsewhere"; the
    untouched ranges are listed (`Result-Record/the-result-record-field-map.md:124-129`).
19. **Applier.**
    - "Recursive/nested applier behavior"; "Authored origin/availability of the steal IDs"
      (`CONTRACT-apply-result-to-target.md:302-303`).
    - "Nested re-entry was not driven" (`:252-254`).
20. **Messages.**
    - "**Residue (narrower):** the escape grammar of the two format engines (`002B49F0`, `002B40C0`), the runtime-filled
      style table `020BE610` and palette `0215E6C8`" (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:430-431`).
    - "Whether class 1 ever lists a member without a unit is not read here" (`:498`).
    - "Which menu entries carry category `0x12` is not read" (`:501`).
    - Locomotion posts messages, but "Which messages it posts is not read" (`:682-683`).
    - The other languages' row bytes "were not decoded" (`:662`).

### 2.2 Structural gaps (a function, formula or format a port needs that no page states)

1. **The per-target execution step has no page.** `Battle_ProcessActionTarget` (`00307300`) resolves and applies each
   entry of the target buffer. The two timeline-event handlers that call it (`BattleUnit_HandleActorTimelineEvent`
   `00319F50`, and the timeline handler `00325260`) are named but not described. The folder has only fragments:
   - the outcome-word write (`CONTRACT-battle-target-buffer.md:402`, `:407-417`);
   - the combo tally (`how-a-combo-continues-and-what-it-blocks.md:352-356`);
   - the retaliation handle (`:182-183`);
   - the result record's stack frame (`Result-Record/the-result-record-field-map.md:132-133`);
   - the reserve-slot walk (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:487-492`).

   A port cannot tell from this folder which timeline event, in which phase, applies a hit, or how many targets one
   event processes. **Not stated.**
2. **Frame scheduling.**
   - The folder names the per-frame drivers: `00234520` (both rings, `CONTRACT-native-command-seam.md:263`),
     `00234590` (the slot walker, `Command-And-Action-Seam/native-command-seam.md:576`), and `00233F70` → `00308610`
     (`CONTRACT-the-moment-an-action-is-committed.md:269`).
   - **Not stated:** their order relative to each other, or the call order inside `00308610`. That is the order of
     select-and-commit, the advance, the combo continue, `00308270` and the cancel.
3. **Five of the eight order handlers are not decoded here.**
   - `002FDDA0` (249 ids, 1,937 B) has its arm map on a 09 page (`how-a-combo-continues-and-what-it-blocks.md:240-243`).
     This folder gives only the status-change runs (`Action-Dispatch/battle-action-handler-table.md:476-491`).
   - `002FE660` has three real bodies, listed but not described (`:493-496`).
   - `002FE840` has the stance calls only (`CONTRACT-battle-action-handler-table.md:247`).
   - `002FE8D0`: nothing.
   - `002FE910` has one fragment (`Action-Dispatch/battle-action-handler-table.md:742-747`).

   What a handler's return value means is stated only for the wait handler (`:197-200`). `00307BE0` treats 1 as
   finished (`:588`).
4. **The order record's format.** Only `+0` (the id) and the second word `+2` are stated
   (`Action-Dispatch/battle-action-handler-table.md:198`, `:242-244`; `:742-743`). Nothing else in the record the
   handlers read through `+0x708` is stated (`CONTRACT-battle-action-handler-table.md:57`).
5. **The presentation side of an action.**
   - The slot walker `0030CBE0` is described only by the state writes it makes (`Command-And-Action-Seam/native-command-seam.md:440-464`).
   - The resources its three tracks load are unnamed (`:465-466`).
   - The special-sequence update `00306760` and the state word `022C2160` are used but not described.
   - Phase 8's callee: "one call on the `+0x6B0` block" (`:206`).
   - The consumers of events `0x2001` / `0x2010`: only "stores it in unit `+0x5C` and forwards it to the object at unit
     `+0x10`" (`CONTRACT-battle-action-handler-table.md:104-106`).
6. **Callees named with no description in this folder:**
   - `BattleUnit_ReleaseTargetRelationAndActionState` `00310780`;
   - `BattleAction_RefundReservedExecutionResources` `00300280` (`the-moment-an-action-is-committed.md:113-117`);
   - `0033C9B0`, stubbed in EXP-091 (`CONTRACT-commit-action.md:366-367`);
   - the enmity delegate `003220E0` (`the-moment-an-action-is-committed.md:212-218`);
   - `002ED2A0` (`CONTRACT-commit-action.md:347`);
   - `00313120`, "Only one caller is unnamed (`FUN_00313120`)" (`CONTRACT-battle-target-buffer.md:579`);
   - the interrupt check `002FFB60`;
   - `0030DB70`;
   - `003065D0`, `00300060`, `00309990` (`the-moment-an-action-is-committed.md:268-270`).
7. **The text format engines.** The engines' escape grammar is "not read", and "What the line looks like on screen" is
   PARTIAL (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:219-220`, `:545`). A port can
   choose the row and the arguments, but not render the line.
8. **Initial values.** Not stated for the rings, the event ring `02EBB560` and its index, `02089340`, or the unit
   fields listed in §1.3. A port has to pick them.
9. **The `022C1DB0` per-slot row (12 bytes) has no layout.** Three pages each name a different part of it (V17), and no
   page puts them together.
10. **Effective action id.** Phase 0 "resolves and caches the effective action id"
    (`Command-And-Action-Seam/native-command-seam.md:198`). The resolver pair `00387090` / `00387A50` is given one
    paragraph (`the-moment-an-action-is-committed.md:346`), with no formula for what is "effective".

### 2.3 Fields written by documented functions but left unexplained

- **Target buffer.** Entry `+0x0C`, "unknown span, not declared padding" (`CONTRACT-battle-target-buffer.md:72`), and
  the header byte `+0x03`, "never separately written" (`:62`).
- **Presentation slot.** The `+0x2C` bits above bit 4, and the meanings of 2-bit codes 1 and 3
  (`Command-And-Action-Seam/native-command-seam.md:537`, `:540`).
- **Unit `+0x760` / `+0x764`.** The phase-1 accumulator and its limit (`Command-And-Action-Seam/native-command-seam.md:199`, `:216`).
- **What the cancel clears.**
  - `+0x1F0` bit 5 (`the-moment-an-action-is-committed.md:134`).
  - The flag masks `0xFFFFBFF75FFFCFFF` on `[unit]` and `0xFFDFFF7F` on `+4` (`CONTRACT-commit-action.md:506-507`).
    Which of those bits mean what is not stated here.
- **Unit `+0xEA0`.**
  - "`+0xEA0` records a relationship *from* each unit *to* the cancelling one" (`the-moment-an-action-is-committed.md:244-246`).
  - The teardown's compare value: "this document does not claim it is zero" (`:250`).
- **Unit `+0x6C0` / `+0x6D0`.** Written by the `0x4022` precondition (`Action-Dispatch/battle-action-handler-table.md:228`);
  nothing on the page says what reads them.
- **Result record.**
  - `+0x40` / `+0x41`, the third and fourth "effects to clear": no writer is listed. Only `+0x3E` / `+0x3F` have
    writers (`Result-Record/the-result-record-field-map.md:87-88`).
  - `+0x30` and `+0x130` are written and never read, by statement (`:80`, `:117`).
- **The 64-byte records.** The second half of each `0208D480` / `0208DE80` record survives a reset; its content is not
  stated (`Action-Dispatch/battle-action-handler-table.md:661-664`).
- **Action row.** `+0x0B` and `+0x21` are authored and read by nothing, and `+0x0C` bits 15, 18 and 20 "are authored and
  never read" (`Action-Definition-Row/the-action-definition-row.md:192`, `:203-204`, `:77`). These are safe to carry
  unread.
- **Message row.** `+6` / `+7` are zero on all 102 rows (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:626-627`).
- **Candidate pick.** The positive-extreme float `02F973B8` is outside the file image (`CONTRACT-battle-target-buffer.md:500-502`).

### 2.4 Contradictions between or within pages

A re-implementer has to choose a side in each of these.

- **Group A** holds the items that change a value a port would compute or hard-code. Every one is marked
  **page-text only - needs local check**, because this session cannot see the executable.
- **Group B** holds counts, sizes and caller sets that disagree. They are values too, so they carry the same mark.
- **Group C** holds stale "not read / open" claims that another page or a later dated section answers, and corrected
  claims still repeated unstruck.
- **Group D** holds status banners against front matter.

A favoured side is named only where a dated correction on the pages settles it.

#### A. Value-changing contradictions (each: page-text only - needs local check)

**A1. The commit's reproduction formula against its own ordering.**
- One side: `CONTRACT-commit-action.md:221-226` gives
  "`if not twoBandIdTest(actionId): return 0` … `resetTargetBuffer(actor)  /* 00316CF0 */` … `consult actor+0x770
  (stats kind byte) and actor+0x744 (last cancelled id)` … `updateAttackerMask(target)`".
  - The reset is unconditional.
  - There is no propagation walk.
  - The `+0x6B0` bit-1 / `022C1DB8` copy is missing.
  - `+0x770` is labelled the stats kind byte.
- Other side: `CONTRACT-commit-action.md:179-185` says "**Corrected 2026-09-12 …: step 4 does not happen on every
  commit.** … A band-two action commits with the previous action's target buffer still in place. The same `ja` at
  `0030F8B2` skips the entire propagation walk for band two". It agrees with the step list at `:167-177` and with
  `CONTRACT-the-moment-an-action-is-committed.md:85-89` (CM-3).
- **Favoured:** the 2026-09-12 correction (`:179-185`), which §13 also executed ("51 buffer resets across 62 commits",
  `:253-255`). §12 was written from the old §7: "§7's ordering is the source of the formula above" (`:236-237`).

**A2. Does a band-two (order) commit update the target's attacker mask?**
- One side: `the-moment-an-action-is-committed.md:65-67` gives "`0030F8B2  cmp  di, r13w ; actionId vs 0x21E … JA refuses
  ids above it` / `0030F8B6  ja   0030F97A`". `CONTRACT-commit-action.md:47` and `:127` make `0030F97A` the "return 1"
  exit after the mask block (`0030F937`–`0030F975`). Read together, a band-two id jumps past the mask.
- Other side: `CONTRACT-commit-action.md:184-185` says "a band-two commit writes the block, settles `+0x770`, and goes
  straight to the mask". Its step list agrees: "8. update the target's attacker mask" (`:177`).
- No dated correction decides it. The 2026-09-11 note at `the-moment-an-action-is-committed.md:66` corrects only the
  compared constant.

**A3. The `+0x770` re-commit latch.**
- One side: "a re-issued action that matches what was just cancelled keeps `+0x770`, any other clears it (`0030F85F`)"
  (`the-moment-an-action-is-committed.md:139-140`; also `:47`).
- Other side: "**When it is nonzero it is preserved iff** the stats kind byte `[+0x698]+5` is **1** … **or** the kind
  byte is **0** *and* the committed id … *and* the committed param … the kind-1 shortcut preserves the latch regardless
  of id and param" (`CONTRACT-commit-action.md:335-341`; executed, `:291-294`, `:416`).
- **Favoured:** `CONTRACT-commit-action.md` §13a, dated 2026-09-18 and "re-derived from the bytes".

**A4. Which table holds the memoised combo count.**
- One side:
  - "`rdi` is the 64-byte record (`0208D480 + kind * 0x40`)" (`how-a-combo-continues-and-what-it-blocks.md:127`);
  - "**The combo length lives in the high nibble of `0208D480 + kind * 0x40 + 0x12`**" (`:337`);
  - "per-kind record   0208D480 + kind * 0x40" (`CONTRACT-combo-continuation.md:61`).

  The index the combo page actually shows is `byte ptr [rsi + 4]`, not the kind byte (`how-a-combo-continues-and-what-it-blocks.md:314`).
- Other side: "*(for a party record only; a foe's record is `0208DE80 + unit[+0xEA9] × 0x40`, `003886CF`–`003886E1`, a
  second table …)*" (`CONTRACT-combo-continuation.md:121-123`; falsification C5, `:249`). This matches
  `Action-Dispatch/battle-action-handler-table.md:648-654`.
- **Favoured:** CB-5's 2026-09-25 qualification, which OPUS block 346 executed.

**A5. How many generator draws a first combo hit makes.**
- One side:
  - "*first hit → roll twice → memoise the count*" (`CONTRACT-combo-continuation.md:148`);
  - "two generator draws decide the count" (`:158`);
  - "assert `00388660` draws the generator **twice**" (`:178`);
  - "calls `RNG_MT19937_NextU32_Thunk` `00379CD0` twice on a unit whose counter is zero" (`:269`).
- Other side: "**The draw count is 1 or 12, not 2** *(2026-09-25 …)*" (`:103`): one percent gate, then an
  11-iteration loop (`:104-113`).
- **Favoured:** `:103`, dated 2026-09-25 and executed. It changes every later draw on the shared MT stream.

**A6. Capacity of the pending action-selection ring.**
- One side: "| `00313CD0` is a different 8-entry queue |" (`Command-And-Action-Seam/native-command-seam.md:226`);
  "Pending action-selection queue (`00313CD0`, up to 8 entries)" (`README.md:47`).
- Other side: "It is a **64-entry** ring, not an 8-entry one" (`Command-And-Action-Seam/native-command-seam.md:78-79`),
  with the dated correction "CORRECTED: the pending action-selection queue is 64 entries, not 8" (`:268-288`). See also
  `CONTRACT-native-command-seam.md:91`.
- **Favoured:** 64, from the 2026-09-02 correction. The evidence row at `:226` was not updated.

**A7. Whether the two ring drains behave alike.**
- One side: "same paired byte indices, same 8-byte stride, same mod-64 advance, same resolve-then-act loop"
  (`Command-And-Action-Seam/native-command-seam.md:80-81`).
- Other side: "~~and the same resolve-then-act drain loop~~" (`CONTRACT-native-command-seam.md:93`); "**The action drain
  pops up to eight entries per call, whatever they resolve to.** … **The presentation drain stops at the first entry
  that does not resolve.**" (`:98-101`, restated 2026-09-26 and executed). See also
  `Command-And-Action-Seam/native-command-seam.md:130-133`.
- **Favoured:** `CONTRACT-native-command-seam.md:96-103`, dated 2026-09-26.

**A8. The target buffer's `+0x01` word: is it read?**
- One side: "**`+0x01` has no reader anywhere in the image, and that is now measured, not assumed** (OPUS 2026-09-16) …
  **The field stays UNRESOLVED on purpose.**" (`CONTRACT-battle-target-buffer.md:283-295`).
- Other side: "the reader `AiOrder_SelectFinalTargetFromCandidates` switches on `byte [rsi+1]` at `00308813`. So `+0x01`
  = `keyType` …, `+0x02` = `pickRule`" (`:440-442`, "**Verified owner-side 2026-09-22**", `:435`). The §3 table at
  `:60-61` agrees.
- **Favoured:** the 2026-09-22 verification. A port that drops the recipe changes target selection.

**A9. Where the target buffer type lives.**
- One side: "`BattleTargetBuffer`, total size **0x208**, never independently allocated — it exists only inline, twice,
  inside `BattleUnit`" (`CONTRACT-battle-target-buffer.md:53-54`). `:285-286` reasons from this: "The buffer is never
  independently allocated, so any outside reader must reach the word through an inline base".
- Other side: "`AiOrder_EvaluateAndResolveActionTarget` (`003014C0`) builds the candidates into a **stack** buffer
  (`[rsp+0x460]`) and calls `003087E0(unit, candidates, out = [rsp+0x40], actionId)`" (`:486-488`).
- No dated correction addresses the allocation sentence.

**A10. Length of the result record's two parameter arrays.**
- One side: "**Two 32-bit masks and two parameter arrays of 33**" (`Result-Record/the-result-record-field-map.md:193`).
- Other side: "the ~~33~~ **32** dwords from `+0x5C` and the ~~33~~ **32** words from `+0xDC` … *(corrected 2026-09-29,
  FABLE …)*" (`:48`); also `:99`, `:101`.
- **Favoured:** 32, from the 2026-09-29 correction.

**A11. Layout of result `+0x3C`–`+0x41`.**
- One side: "`+0x3C  u16 + u8, +0x3E u32 + u8  statuses to remove`" (`Result-Record/the-result-record-field-map.md:174`).
- Other side:
  - `+0x3C` and `+0x3D` are one byte each, "the first … / second status-layer effect the action adds", and `+0x3E` /
    `+0x3F` are effects to clear ("corrected 2026-09-11 from 'statuses to remove'", `:85-88`);
  - "two layer effects to add and four to remove" (`applying-a-result-to-a-target.md:180`);
  - "`+0x3C`–`+0x3D` (two bytes …, mode 2 with `-1`) and `+0x3E`–`+0x41` (four bytes …, mode 0 with `0`)"
    (`CONTRACT-apply-result-to-target.md:90-93`).
- **Favoured:** the 2026-09-11 row correction and the 2026-09-25 contract statement. The §4 block was not updated.

**A12. Width of the item field at result `+0x38`.**
- One side: "record `+0x38` (`u16`, `-1` = none)" (`applying-a-result-to-a-target.md:171`).
- Other side:
  - "the item dword uses `-1`" (`:55`);
  - "`+0x038` | 4 | i32" (`Result-Record/the-result-record-field-map.md:84`);
  - "The item scalar at `+0x38` is absent when its **dword** equals `-1` (the dispatched item ID is the low word)"
    (`CONTRACT-apply-result-to-target.md:82-83`).
- **Favoured:** the SECTION-01 contract (2026-09-22): a dword absence test, and the low word dispatched.

**A13. Type of result `+0x11C`.**
- One side: "record `+0x11C` (s8, `-1` = none)" (`applying-a-result-to-a-target.md:169`).
- Other side: "`+0x11C` | 2 | u16 | **the target's new level** in the low byte (`0xFF` = none) … the high byte keeps the
  initialiser's `0xFF`" (`Result-Record/the-result-record-field-map.md:103`).
- Not settled by a dated correction. The two agree only if the applier reads the low byte signed.

**A14. Who clears the steal-availability bit, and for which targets.**
- One side: "Three effects run **only when the target's record byte `+0x05` is `1`** … on a hit the engine clears the
  matching bit in `targetActor[+0x6A0][+0x14]`" (`applying-a-result-to-a-target.md:122-127`). Step 4 says "then **bit
  *i* of the spawn record's `+0x14` is cleared** (`0031145C`–`0031146F`)" (`:170`).
- Other side: "**the slot clear is made by the gate `00385BA0`, not by the steal loop, and it is not gated on kind 1.** …
  So a steal byte aimed at a target whose stats are not kind 1 still consumes the availability, and grants nothing."
  (`CONTRACT-apply-result-to-target.md:152-158`, sharpened 2026-09-26, executed stub-free). The same is said at
  `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:55` (restated 2026-09-25).
- **Favoured:** the 2026-09-25 / 2026-09-26 statements.

**A15. The approach-pacing stand window.**
- One side: "it **stands still** for the first 30 steps of the charge" (`how-close-a-unit-must-stand-to-act.md:115`).
- Other side: "The stand window is `30 × [01DFE0B4]` … So 'the first 30 steps' holds at the 30 fps setting and is 60 at
  the 60 fps one" (`:188`, falsification B9, 2026-09-29).
- **Favoured:** B9. §6 was not amended.

**A16. Which events `004697C0` posts.**
- One side: "| `004697C0` | `0x06` | "Action interrupted. … cancels …." |"
  (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:340`).
- Other side: "`bp != 0x96` falls to `edx=6` … The alternate arm … maps `esi` 1/2/3 → `edx` 5/7/6 … before the same
  `0046AB10` post" (`:843-847`, SWE2-EC7-21, 2026-09-18). So `004697C0` can post `0x05`, `0x06` or `0x07`.
- **Favoured:** the dated 2026-09-18 section, read at the instructions. The §2.7 row was not updated.

**A17. What the `022C1DB8` byte is.**
- One side:
  - "**The posture byte is re-picked only when bit 1 of `+0x6B0` is set, and that bit is consumed**; the byte comes from
    `022C1DB8 + slot * 12`" (`CONTRACT-commit-action.md:295-296`; also `:418`);
  - "posture row `0x22C1DB0 + ea9*12`" (`:353`).
- Other side: "`BattleUnit_IssueCommand` sees handle 0. It sets `+0x6B0` bit 1 and parks the slot at
  `022C1DB8[unit +0xEA9 × 12]` … `BattleUnit_CommitAction` finds bit 1, copies the parked slot to `+0x6B9` and sets
  `+0x6B6 = 1` (`0030F865`–`0030F894`)" (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:478-481`,
  answered 2026-09-14).
- A third reading of the same row base: "saves `+0xDC8` / `+0xE58` into a 12-byte per-slot table at `022C1DB0`"
  (`how-a-combo-continues-and-what-it-blocks.md:173`).
- **Favoured** for the byte's meaning: the 2026-09-14 answer, a slot-target index that feeds the slot-target path of
  §2.2 item 1. A port that treats it as a "posture" byte and omits `+0x6B6 = 1` breaks reserve-member commands. The
  row's full layout stays unstated (§2.2 item 9).

#### B. Counts, sizes and caller sets that disagree (each: page-text only - needs local check)

**B1. Size of `0030CA80`.** "`BattleAction_CheckPresentationSlotReady` (`0030CA80`, 352 B)"
(`Command-And-Action-Seam/native-command-seam.md:359`; "104 instructions, ends `ret` at `0030CBDF`", `:363`) against
"`0030CA80` (`BattleAction_CheckPresentationSlotReady`, ~21 B)" (`:580`).

**B2. Size of `003083B0`.** "`BattleAction_CheckTargetEligibility` (`003083B0`, 596 B)"
(`Action-Dispatch/battle-action-handler-table.md:600`; "the 596-byte body", `:672-673`) against "`003083B0`
`BattleAction_CheckTargetEligibility` (307 B)" (`:725`).

**B3. Size of `002FE910`.** "| 1 | `002FE910` | — | 52 B |" (`Action-Dispatch/battle-action-handler-table.md:129`)
against "`002FE910` (~55 B)" (`:742`).

**B4. Writers of `+0x714`.**
- One side: "`BattleUnit+0x714` has exactly **three** writers image-wide … Four other `[reg+0x714]` writes exist"
  (`Action-Dispatch/battle-action-handler-table.md:456-459`), seven in all.
- Other side: "A whole-image sweep for writes at `+0x714` returns **eight bodies**, of which only three are battle-unit
  bodies; the other five …" (`CONTRACT-native-command-seam.md:123-125`).
- The three battle-unit writers agree. The outside count is 4 against 5.

**B5. Sites at `+0x6B8`.** "`+0x6B8` has 65 sites image-wide" (`how-a-combo-continues-and-what-it-blocks.md:460`)
against "`+0x6B8` returns **64 accesses image-wide**" (`CONTRACT-combo-continuation.md:75`) and "The 64 counts three
`lea` sites; without them it is 61" (`:245`).

**B6. Functions addressing the slot array.** In one paragraph of `Command-And-Action-Seam/native-command-seam.md`:
"the seven functions that address the array" (`:513`), "The eight functions that reference the slot array" (`:515`),
and "**no access found** in any of the nine functions" (`:523`).

**B7. Size of the result-record census.**
- The page says "245 accesses in 39 functions over 52 offsets" (`Result-Record/the-result-record-field-map.md:15`),
  "52 offsets with a writer or a reader" (`:32`) and "reads 30 of the 52 offsets" (`:50`).
- The §2.2 table now has 53 offset rows: `+0x010` was "added 2026-09-27" (`:71`).
- The member file `result-record-accesses.tsv` has 40 distinct functions and 53 distinct displacements.
- The header figures predate the 2026-09-27 addition.

**B8. The `+0x0C` bit-reader file.** `action-row-0x0C-bit-readers.tsv` has 25 data rows. Its own comment and
`Action-Definition-Row/the-action-definition-row.md:198` speak of "the 23 sites". The same page later says "the census
has 60 reads, not 23" (`:198`, correction of 2026-09-27).

**B9. Callers of `IssueCommand`.**
- Two callers: "reached through two callers only — the by-focus-handles fan-out and the defeat-cleanup step"
  (`CONTRACT-native-command-seam.md:66-67`), and "`00311CF0` is 283 B, called from `00311B20` and `003138D0`" (`:240`).
- Three callers: "The issuer's other caller, `00311CD0` (five call sites), always passes slot 0, and the defeat step
  `003138D0` passes a handle" (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:476-477`).
  `Command-And-Action-Seam/native-command-seam.md:43-48` lists `00311CD0` as a wrapper of the seam.
- Whether `00311CD0` reaches `00311CF0` by `call`, by `jmp` or not at all is not stated.

#### C. Stale "not read / open" claims, and corrected claims still repeated

**Category index**

- **C1. The README's "Not yet documented" list.**
  - "The 13-phase standard-action pipeline", "Presentation slot pool", "`BattleUnit_CommitAction` (`0030F760`) and the
    action context …", "Pending action-selection queue (`00313CD0`, up to 8 entries)", "Target set materialization,
    reservation, enmity" (`README.md:42-48`).
  - All of these are documented: the phases at `Command-And-Action-Seam/native-command-seam.md:189-217`; the slot pool
    at `:511-540` and `the-moment-an-action-is-committed.md:263-276`; the commit on three pages; target gathering at
    `how-an-action-gathers-its-targets.md`. The "8 entries" is A6.

**Availability**

- **C2. The scope note.** "The enumerated table is therefore **not** the complete reason-code set"
  (`Action-Availability/battle-command-availability-and-reason-codes.md:396-398`) against the completed table of the
  same day (`:461-485`).
- **C3. AI-1.** "**AI-1 remains fully open** — nothing here maps a code to on-screen text"
  (`Action-Availability/battle-command-availability-and-reason-codes.md:520-521`) against "**ANSWERED 2026-09-02 —
  they never reach a screen.**" (`:283-286`) and §11 (`:548-579`).
- **C4. The per-unit pool.** "a **global** amount with a per-unit fallback" (`:501-502`) and "a party-wide pool checked
  before a per-unit one" (`:505`) against the 2026-10-02 correction: "`+0xE58` is the gil cost reserved for the action
  in progress, not a purse" (`:303`, `:480`, `:627`).
- **C5. A dated section that predates the program.** "## SWE2-EC7-19 update (2026-05-15)"
  (`Action-Availability/battle-command-availability-and-reason-codes.md:639`). Every other section is dated September
  2026.

**Target gathering**

- **C6. When targets are gathered.** "*Which step of the action that is - before or after the charge - was not read.*"
  (`how-an-action-gathers-its-targets.md:145`) against UQ-108, answered 2026-09-14: phase 4 runs the charge progress
  step and phase 9 runs `Battle_BuildActionTargetSet` (`Command-And-Action-Seam/native-command-seam.md:202`, `:207`).

**Commit and seam**

- **C7. Is the commit executed?** "not as execution of the commit itself, which is unexecuted"
  (`CONTRACT-the-moment-an-action-is-committed.md:157-160`) against "`0030F760` as shipped bytes under Unicorn … **1309
  commands, 704 compared lines, 0 mismatches**" (`CONTRACT-commit-action.md:244-253`) and EXP-091 (`:319-326`).
- **C8. The second shadow.** "a second verbatim shadow exists at `+0x730`–`+0x747`; its readers were not in this
  census's band and stay unenumerated" (`CONTRACT-the-moment-an-action-is-committed.md:177-179`) against "the cancelled
  record at `+0x730` is written by the cancel and read by the next commit" (`the-moment-an-action-is-committed.md:141-142`;
  the reads at `0030F84E`–`0030F857`, `:137-139`).
- **C9. Does the commit raise an event?** "it does not read a script, touch a resource, or raise an event of its own"
  (`CONTRACT-commit-action.md:191-193`) against "**`00313B30` is notify** … handed to `002ED2A0(uid, &rec)` per unit"
  (`:342-347`). The README's crossing paragraph calls it a broadcast to the character renderer
  (`the-moment-an-action-is-committed.md:380`).
- **C10. The commit page's "not claimed" list.**
  - "Is the `0x718` block a second live copy rather than a shadow? | **Not established either way, and left that way.**"
    (`the-moment-an-action-is-committed.md:313`) against the cancellation section of the same page (`:107-142`).
  - "Is `0x80000003` explained here? | **No.** … its *meaning* is not." (`:317`) against "none of KO, Stone, X-Zone"
    (`how-a-combo-continues-and-what-it-blocks.md:161`) and "not KO, Stone or Vanished (`0x80000003` …)"
    (`how-an-action-gathers-its-targets.md:104`).
  - "**What this document does not claim:** what `0030AB40` classifies, what `00313B30` does …, or what the byte table at
    `022C1DB8` … holds" (`the-moment-an-action-is-committed.md:319-321`) against the same page's interior citation of
    `0030AB40` (`:388-398`), `CONTRACT-commit-action.md:342-347`, and
    `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:478-481`.
- **C11. What carries the command into the funnel.** "what carries `+0xBA0` into the funnel is not read here"
  (`CONTRACT-native-command-seam.md:75-76`) against "`BattleUnit_SelectAndCommitNextAction` … commits the **issued
  command** — `+0xBA0` id and `+0xBB8` handle … (`00305AE4`–`00305B2F`)"
  (`Command-And-Action-Seam/native-command-seam.md:95-98`, settled 2026-09-12).
- **C12. Does the seam call the commit?** "`-> 00311CF0 BattleUnit_IssueCommand  (or a wrapper)` / `-> native target
  selection / availability / reservation` / `-> 0030F760 BattleUnit_CommitAction`"
  (`Command-And-Action-Seam/native-command-seam.md:152-154`) against "**The seam records INTENT only; it does not reach
  the commit funnel**" (`CONTRACT-native-command-seam.md:71`, 2026-09-25).

**Standard machine and presentation slots**

- **C13. Slot bytes `+0x1E`–`+0x1F`.** "**no access found** in any of the nine functions" (`:523`) and "**Still open:**
  `+0x1E`–`+0x1F`" (`:540`) against "***ANSWERED 2026-09-18 (FABLE): `+0x1E`..`+0x1F` is alignment padding***" (`:515`),
  all in `Command-And-Action-Seam/native-command-seam.md`.

**Order handlers and the order space**

- **C14. The handler-table contract's open items.** "What the eight handlers do … the rest is its open work" and "Why 18
  slots are empty, and whether any id in those gaps is ever issued" (`CONTRACT-battle-action-handler-table.md:164-166`)
  against AT-2, closed 2026-09-12 ("rejected everywhere and never authored", `Action-Dispatch/battle-action-handler-table.md:152-167`),
  AT-3 (the `0x4021` wait handler, `:191-203`) and AT-4 (`:471-496`).
- **C15. Naming the action ids.** "*id → player-visible command name cannot be completed*" and "**AT-9 is blocked on the
  same join.**" (`Action-Dispatch/battle-action-handler-table.md:558-559`, `:563`, dated 2026-09-02) against AT-8,
  answered 2026-09-14 ("`+0x34` names each row through bank 0", `:264-270`), AT-9, answered 2026-09-11 (`:271-275`),
  and AI-2 (`Action-Availability/battle-command-availability-and-reason-codes.md:287-290`).
- **C16. The handler page's "not claimed" list.**
  - "**Not what lies above id 542.** `AT-8` remains open" (`Action-Dispatch/battle-action-handler-table.md:668-669`)
    against EI-2, answered 2026-09-12 (`:69-79`).
  - "**Not what `FUN_004697C0` does**" (`:671`) against
    `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:838-848`.
  - "the 596-byte body past `003083FF` is unread" (`:672-673`) against the subtree read at `:725-737`.

**Combo**

- **C17. The combo contract's stale items.**
  - "the native command seam and the handler table remain uncontracted" (`CONTRACT-combo-continuation.md:30-31`; also
    `:143`, `:195`) against `CONTRACT-native-command-seam.md` and `CONTRACT-battle-action-handler-table.md`, both
    authored 2026-09-22.
  - "What the second draw at `003887E3` contributes" (`:193`) against CB-3 (`:104-111`).
  - "What `+0x6B8` is" (`:194`) against UQ-115, answered 2026-09-14 ("the combo's running hit tally",
    `how-a-combo-continues-and-what-it-blocks.md:349-366`).
  - "The per-kind record at `0208D480` is authored data" (`CONTRACT-combo-continuation.md:154`) against "rewritten on
    the first hit of every combo" (`how-a-combo-continues-and-what-it-blocks.md:337-338`) and the reset of its first 32
    bytes (`Action-Dispatch/battle-action-handler-table.md:642-664`).

**Action definition row**

- **C18. The row's layout block.**
  - "`+0x1E u8 messageKind`", "`+0x22 u16 linkedMenuId`", "`+0x28 u8 quickeningIndex (120..153, reader not found)`"
    (`Action-Definition-Row/the-action-definition-row.md:136-139`) against the field map: the id-class byte, renamed
    2026-09-30 (`:76`); "an id whose space `+0x1E` names" (`:78`); and GR-4, answered (`:81`, `:151`).
  - The falsification table still says "`+0x28` — 26 Esper attacks" (`:267`) against the 2026-09-27 correction to the
    "26 Quickening-family rows" (`:81`).

**Results and messages**

- **C19. The result record's stale lines.**
  - "ResultRecord (>= 0x148 B …)" (`Result-Record/the-result-record-field-map.md:159`) and "**The record is at least
    0x148 bytes**; allocate more only if the allocation site says so" (`:197`) against FP-2, answered 2026-09-11: "a
    `0x148`-byte stack local, every time … nothing lives above `+0x147`" (`:130-140`).
  - "`+0x08 u32 (context +0x10)`" and "`+0x38 i32 (context +0x20)`" (`:163`, `:173`) against the gil amount (`:70`)
    and the poach reward item (`:84`).
  - "Which actions reach the two writers is not enumerated." (`:203-204`) against "**Only one recipe reaches it**
    (2026-09-12): step slot 163 … recipe 99, action `0x103`" (`applying-a-result-to-a-target.md:184`).
- **C20. The status-layer modes.** "What that function's modes do is not read here"
  (`applying-a-result-to-a-target.md:196`) against "**Mode 2 sets and mode 0 clears the mutable layer `+0x68`**" (`:180`)
  and `CONTRACT-apply-result-to-target.md:263-268`.
- **C21. The target-buffer contract's stale items.**
  - "**something else fills it** and this contract does not say what" (`CONTRACT-battle-target-buffer.md:280-282`)
    against "**THE WRITER IS KNOWN**" (`:402`, folded 2026-09-13).
  - "no opcode, verb or authored table reaches it" (`:142-143`) against "`003495A0` calls the append-and-reset caller
    `00313120`" (`:699-700`) and "a script body can run it directly" (`the-moment-an-action-is-committed.md:382`).
  - "bits 8 / 9 / 10 knockback / parry / combo-continues and bit 11 the result's flag word B bit 0 — the mode-2
    resource-reaction chance rolled" (`CONTRACT-battle-target-buffer.md:415-417`) against "bit 0 ~~the mode-2 resource
    reaction chance rolled~~ the ranged critical rolled … **bit 2 ~~parry rolled~~ counter rolled**"
    (`Result-Record/the-result-record-field-map.md:72`, corrected 2026-10-02).
- **C22. FL-2's checkbox.** "- [x] **FL-2.** … *(closed — the register row is WITHDRAWN.)*"
  (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:432`) against "**The row stays open**: no
  process was read" (`:438-439`), "the runtime confirmation is still owed (`FL-2`)" (`:317`), and the evidence row "the
  live read is still owed (`FL-2`)" (`:542`).

#### D. Status banners against front matter

- **D1. The README's statuses disagree with the pages.**
  - The combo page is listed "**PARTIAL, tier 1.**" (`README.md:23`); its front matter says `status: DOCUMENTED`
    (`how-a-combo-continues-and-what-it-blocks.md:4`).
  - The range-band page is listed "**DOCUMENTED, tier 1.**" (`README.md:19`); its front matter says `status: AUDITED`
    (`how-close-a-unit-must-stand-to-act.md:4`, promoted 2026-10-01, `:24`).
  - The post-result page and the result-record page are listed "**DOCUMENTED, tier 1.**" (`README.md:30`, `:36`);
    both front matters say `status: AUDITED` (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:4`;
    `Result-Record/the-result-record-field-map.md:4`).
- **D2. The README lists six of the eleven mechanism pages** (`README.md:11-40`). It omits:
  - `the-moment-an-action-is-committed.md`;
  - `applying-a-result-to-a-target.md`;
  - `Action-Availability/battle-command-availability-and-reason-codes.md`;
  - `Action-Dispatch/battle-action-handler-table.md`;
  - `Action-Definition-Row/the-action-definition-row.md`.

  It names none of the seven contracts.
- **D3. The availability page's banner and body disagree.** The front matter says "`status: AUDITED — … every box
  ticked`" (`Action-Availability/battle-command-availability-and-reason-codes.md:4`). The body opens "**PARTIAL.** … the
  numeric reason codes are recovered but **not mapped to the on-screen messages**" (`:32-34`).
- **D4. "Pending first review" survives after the review.**
  - `how-an-action-gathers-its-targets.md:23` says "Pending first review", next to a falsification pass dated
    2026-09-29 (`:14-18`, `:205-227`).
  - `how-close-a-unit-must-stand-to-act.md:24` says "pending first review" in the same note that records the promotion
    to AUDITED.
- **D5. Review flags (stated, not contradictions).**
  - `crossref_clean: false` on six contracts and on the combo page: `CONTRACT-commit-action.md:22`,
    `CONTRACT-the-moment-an-action-is-committed.md:24`, `CONTRACT-native-command-seam.md:24`,
    `CONTRACT-battle-action-handler-table.md:24`, `CONTRACT-combo-continuation.md:24`,
    `CONTRACT-battle-target-buffer.md:22`, `how-a-combo-continues-and-what-it-blocks.md:25`.
  - Peer review pending on the applier pair: `applying-a-result-to-a-target.md:26` and
    `CONTRACT-apply-result-to-target.md:14`.
