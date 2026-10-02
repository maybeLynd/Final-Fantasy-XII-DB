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
