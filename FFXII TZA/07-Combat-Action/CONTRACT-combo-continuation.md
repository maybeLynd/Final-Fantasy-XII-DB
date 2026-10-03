---
contract: Continue a combo — roll once, memoise the count, re-commit the same action until it is spent
category: 07-Combat-Action
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: how-a-combo-continues-and-what-it-blocks.md
entries: ["0030FA00", "00388660", "003105D0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — every access at `+0x6B7` and `+0x6B8` image-wide **classified by access
    width**, the roll branch and the memoisation read at their instructions, and the generator calls
    counted in the rolling body. **This records checks performed on that date, not the method of the
    original derivation**, which is on the combo page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-combo-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — combo continuation

> **Authored 2026-09-22 by FABLE.** S-20's binding gap is *"2 contracts over 4 pages"*. This takes
> **combos**; the native command seam and the handler table ~~remain uncontracted~~ *(answered: contracted since, CONTRACT-native-command-seam.md and CONTRACT-battle-action-handler-table.md; 2026-10-02, OPUS)* and this document
> does not claim them.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is six
> such invariants across three bodies that never call one another.

## 1. Purpose

Decide how many times a committed action repeats, and repeat it.

## 2. Interface

| | body | size |
|---|---|---:|
| roll and memoise the count | `BattleFormula_RollAndStoreComboCount` (`00388660`) | 602 B |
| continue, once | `BattleAction_TryContinueComboSequence` (`0030FA00`) | 146 B |
| reset | `BattleUnit_CancelAndResetCurrentAction` (`003105D0`) | 418 B |

## 3. Types

```
BattleUnit
  +0x6B4  u8    action state
  +0x6B7  u8    the combo counter — progress
  +0x6B8  u8    its partner, preserved across the re-commit (CB-6)
  +0x708  ptr   the committed context   \
  +0x710  u32   the target focus         > re-used verbatim by the continue path
  +0x714  u16   the action id           /

per-kind record   0208D480 + kind * 0x40   # <- corrected 2026-10-02, OPUS - the index is the stats record's byte +4 (003886A7), and only for a kind-0 stats record (0038869F-003886A5); otherwise 0208DE80 + unit[+0xEA9]*0x40 (003886CF-003886E1)
  +0x12  u8   high nibble = the memoised combo count (CB-3)
```

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**CB-1 — `+0x6B7` and `+0x6B8` are TWO one-byte fields, and the one word store is not evidence
otherwise.** Measured image-wide by access width: `+0x6B7` has **seven** accesses of which **exactly
one is word-wide** — the reset's `mov word ptr [rbx + 0x6b7], bp` at `003106EB`, which clears both
bytes at once — and **all six others are byte-wide**. *A `word` store bounds the bytes touched, not
the field.*

> **And the partner's census is mostly not the partner.** `+0x6B8` returns **64 accesses image-wide,
> of which only FOUR are byte-wide** — two reads and two writes, in `0030FA00` and one other body *(not cited: it is a hub whose callee set spans five further layers this contract says nothing about)*. The
> other sixty are `qword` and `dword` on entirely unrelated structures that happen to have something
> at that displacement; one function alone contributes about twenty-five. *A census of this field
> that does not filter by width overstates it sixteenfold.*

**CB-2 — The continue path re-commits the IDENTICAL action, and advances only on success.**
`0030FA00` reads the context `+0x708`, the focus `+0x710` and the action id `+0x714` straight back
out of the unit and hands the same three to `BattleUnit_CommitAction`. **The counter is incremented
after the commit returns success** (`0030FA6C inc dil`, `0030FA79` stores it); ~~a failed commit
returns 0 with the counter untouched~~. **The failure has two cases** *(narrowed 2026-09-26, FABLE, Claude Opus 5.5,
on `OPUS-NOTE-FABLE-S20-CB2-FAILED-RECOMMIT`; bytes re-read)*:
- **The gate refuses.** The eligibility gate `0030FA00` calls first returns 0, and `0030FA27` falls through to return 0 at `0030FA29`. Nothing has been
  written, so the counter `+0x6B7` and the partner `+0x6B8` are untouched.
- **The re-commit itself fails.** `0030FA00` calls the commit with its fifth argument 1 (`0030FA54`), so the commit
  first runs the cancel `003105D0`. The cancel's `mov word [rbx+0x6B7], bp` (`003106EB`,
  `bp` zeroed at `00310649`) clears the counter and the partner together. If the commit then refuses, it returns 0
  and `0030FA63 je 0030FA29` returns 0 **without restoring them**. The values `0030FA00` saved at
  `0030FA0F`/`0030FA19` are written back only on the success path (`0030FA65`, `0030FA79`).
- Executed on the original code with no stub: `candidates/s20-opus-replay-commit/cb26.py`, case F (OPUS).

*A combo is not a special action — it is the same action committed again.*

**CB-3 — The roll happens ONCE PER COMBO, on the first hit, and the first hit draws the generator
~~TWICE.~~ once or twelve times.** *(corrected 2026-10-02, OPUS: one draw at `003886FD`; a failed gate `0038871D jbe 0038887E` stops there, a passed one runs the 11-pass loop `003887DA`–`00388807` around `003887E3`)* `00388660` reads the counter off the owning unit (`0038868A`) and branches on it at
`003886F5`/`003886F7`: **non-zero jumps straight past every draw**. On the zero path it calls the
MT19937 thunk at `003886FD` **and again at `003887E3`** — ~~two draws~~ two call **sites** — and stores the result in the
**high nibble of `record + 0x12`** (`0038885D and …, 0xf` then `00388865 or …, r14b`).
**The draw count is 1 or 12, not 2** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 346](../_index/candidates/s20-opus-replay-combo-roll/README.md), which executed it against an independent model, 4/4; `003886C3`–`00388869` re-read.)*.
1. The first draw is a **percent gate**: `draw % 100 < [02AEDFE4]` (`00388716`). If it fails, there is no combo.
2. The second site, `003887E3`, is inside an **11-iteration loop** (`r14d = ebp = 0xB`, `00388803`–`00388807`).
   Each iteration adds 1 to the count, which starts at 1, when `draw % 100` is below a per-hit threshold.
3. The threshold is an **HP band**: 64 below max HP / 16, then 32 below / 8, 16 below / 4, and 8 otherwise
   (`00388723`–`003887D6`). Status bit 16 (`0x10000`) substitutes current HP for max, and bit 28 doubles max. The
   statuses' names are not claimed.
4. The count is capped: for a foe-class record at its class record's `+0x20` minus 1 (`00388833`–`0038884D`),
   and always at 11 (`00388850`–`00388853`).

*So a first hit that passes the gate advances the shared generator by 12, and one that fails advances it by 1.*

**CB-4 — The counter is progress against that memoised nibble, and the comparison ends the combo.**
`0038886B` reloads `record + 0x12`, `0038886F shr eax, 4` recovers the count decided on hit one,
`00388872 cmp ebx, eax` compares progress against it and `00388874 jae` ends the combo; otherwise
another hit is requested. *So the number of hits is fixed at the first swing and cannot change
mid-combo, however the unit's stats move.*

**CB-5 — Two objects, one offset apart in the reader's mind.** In `00388660`, `rdi` is the **64-byte
per-kind record** at ~~`0208D480 + kind * 0x40`~~ `0208D480 + stats[+4] × 0x40` *(corrected 2026-10-02, OPUS: the index is `003886A7 movzx edi, byte ptr [rsi + 4]`, not the kind byte `+5`, which only selects the table at `0038869F`–`003886A5`)* *(for a party record only; a foe's record is
`0208DE80 + unit[+0xEA9] × 0x40`, `003886CF`–`003886E1`, a second table — *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 346](../_index/candidates/s20-opus-replay-combo-roll/README.md), which executed it against an independent model, 4/4; `003886C3`–`00388869` re-read.)*)* and `rax` is the **BattleUnit** returned by
`BattleStats_FindOwningBattleUnit`. *The memoised nibble lives on the record and the progress counter
on the unit* — they are different objects with different lifetimes, and reading `+0x12` and `+0x6B7`
as fields of one structure is the error the combo page's §6 exists to correct.

**CB-6 — The partner byte is preserved across the re-commit, not updated by it.** `0030FA19` reads
`+0x6B8` before the two calls and `0030FA65` writes the same value back after them. *Its effect is to
survive a commit that would otherwise clear it; nothing in this path changes it.*

## 5. State

**Owned:** the unit's `+0x6B7`, `+0x6B8` and `+0x6B4`. **Owned elsewhere, read here:** the per-kind
record's `+0x12` nibble. **Read and re-used verbatim:** the committed context, focus and action id.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-commit-action.md`](CONTRACT-commit-action.md) — the commit CB-2 calls again |
| **Sibling** | [`CONTRACT-battle-target-buffer.md`](CONTRACT-battle-target-buffer.md) |
| **~~Uncontracted~~ Sibling** | the native command seam and the handler table — S-20's other two pages, not claimed here *(answered: see CONTRACT-native-command-seam.md and CONTRACT-battle-action-handler-table.md; 2026-10-02, OPUS)* |
| **Shares the generator** | [the periodic tick](../10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md) and [the trigger points](../03-World-Area-Field/CONTRACT-authored-trigger-points.md), which draw the same `00379CD0` |

## 7. State transitions

*first hit → roll ~~twice~~ once, or twelve times when the percent gate passes → memoise the count → counter 0.* *(corrected 2026-10-02, OPUS: `003886FD`, `0038871D`, `003887DA`–`00388807`)* Then per continuation: *check progress
against the nibble → re-commit the same action → on success, counter + 1.* The reset clears both
bytes together (CB-1).

## 8. Script · resource · event interactions

The per-kind record at `0208D480` is ~~authored data~~ runtime state the roll writes *(corrected 2026-10-02, OPUS: `0038885D and byte ptr [rdi + 0x12], 0xf` and `00388865 or byte ptr [rdi + 0x12], r14b` rewrite it on every first hit that passes the gate)*; the roll's distribution is ~~not read here~~ read in CB-3 *(answered: see CB-3 items 1-4; 2026-10-02, OPUS)*.

## 9. Determinism

**Not deterministic on the first hit** — ~~two generator draws decide~~ one draw, or twelve when the gate passes, decides the count *(corrected 2026-10-02, OPUS: `003886FD`, `0038871D jbe 0038887E`, the loop `003887E3`–`00388807`)* — and **fully
deterministic afterwards**, because CB-3's branch skips the draws entirely once the counter is
non-zero. *A replay that reproduces the first hit reproduces the whole combo.*

## 10. Failure paths and edge conditions

- ~~A failed re-commit returns 0 and leaves the counter where it was (CB-2) — the combo simply stops.~~ A refusal
  by the gate returns 0 and leaves the counter where it was. A re-commit that fails after its cancel-first returns 0
  with the counter **and** partner zeroed (CB-2, narrowed 2026-09-26). Either way the combo stops.
- A unit with no owner reads a counter of 0 (`0038868A` after a null-guarded lookup), so it rolls.
- The reset clears the counter and its partner together, and does not touch `+0x6B7` by name — it
  reaches it through `003105D0`.

## 11. Observable behaviour

A character's follow-up swings are decided the instant the first one lands; nothing that happens
during the combo can lengthen or shorten it.

## 12. Reproduction formula

Set the counter to 0 and assert `00388660` draws the generator ~~**twice**~~ **once** when the percent gate fails and **twelve** times when it passes *(corrected 2026-10-02, OPUS: `0038871D jbe 0038887E`, the loop `003887DA`–`00388807`)* and writes the high nibble
of `record + 0x12` (CB-3). Set it non-zero and assert **no draw at all**. Fail the inner commit and
assert the counter did not move (CB-2) ~~.~~ *when the refusal comes from the eligibility gate; when it comes from
the commit after its cancel, assert `+0x6B7` and `+0x6B8` both read 0 (narrowed 2026-09-26).* Sweep `+0x6B8` image-wide and assert **four** byte-wide
accesses, not sixty-four (CB-1).

## 13. Runtime validation

~~**None.** No experiment executes these three bodies. S-20's runtime cell is not addressed by this
contract.~~ **Superseded 2026-09-25:** [OPUS block 346](../_index/candidates/s20-opus-replay-combo-roll/README.md) executed the combo roll with the real gameplay MT against an
independent model (4/4); the evidence class is native replay, not live. *The historical note continues:* *Stated rather than left blank so a CONTRACT READY header is not read as evidence of
execution.*

## 14. Unresolved

- ~~What the second draw at `003887E3` contributes that the first does not.~~ *(answered: see CB-3 items 1-3 - the first draw is the percent gate, `003887E3` the 11-pass HP-band loop that sets the count; 2026-10-02, OPUS)*
- ~~What `+0x6B8` is, beyond being preserved (CB-6).~~ *(answered: the combo's running hit tally, UQ-115 in how-a-combo-continues-and-what-it-blocks.md; 2026-10-02, OPUS)*
- ~~The native command seam and the handler table — S-20's other two pages.~~ *(answered: see CONTRACT-native-command-seam.md and CONTRACT-battle-action-handler-table.md, both authored 2026-09-22; 2026-10-02, OPUS)*

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| CB-1 — one word store, six byte accesses; and 60 of 64 at `+0x6B8` are other objects | every access at both displacements enumerated image-wide **and classified by width**, with the single word store as the control | 1 |
| CB-3 — the branch, both draws, the nibble | `003886F5`/`003886F7`, the thunk calls at `003886FD` and `003887E3`, and `0038885D`/`00388865` | 1 |
| CB-4 — progress against the nibble | `0038886B`–`00388874` read in order | 1 |
| CB-2, CB-5, CB-6 | [the combo page](how-a-combo-continues-and-what-it-blocks.md) §§2.2–2.4 and §6, read from the shipping bytes and corrected 2026-09-12 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on CB-1 through CB-6. **CB-3 is the one to test
first** — rolling per hit instead of per combo is the natural design and produces a different
distribution with the same code shape.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **CombatAction, CombatFormula — internal and SERVICE.** The continue path and the reset are this
  category's; the rolling body is the formula layer's, and CB-3 through CB-5 are about the seam
  between them.
- **RNG_Random_Selection — SERVICE.** The generator thunk is that layer's; CB-3 and §9 are about it.
- **ActorEntity, CombatAI — MECHANICAL.** Both are reached as *callers* of the reset `003105D0` and
  the continue path `0030FA00` — the AI and the actor layer are who ask for a combo to continue or
  be cancelled. Callers, not shared responsibility.
- **CoreRuntimeScheduling, Rewards_Progression_Economy — MECHANICAL, through the GENERATOR.** Both
  are simply other callers of `00379CD0`; a shared generator's callers are the rest of the engine.
- **Gameplay, Movement — MECHANICAL.** Both are reached only as *callees of the reset* `003105D0`:
  cancelling an action stops what the actor was doing. **That is the reset's business, not the
  combo's** — this contract cites `003105D0` for CB-1's word store and for nothing it does
  afterwards.
- **Every other layer reached is MECHANICAL**, through these bodies' own callees. *Their addresses
  are deliberately not cited: each is a hub, and naming one imports its whole edge set.*

## 17. Related

- [How a combo continues and what it blocks](how-a-combo-continues-and-what-it-blocks.md) — the mechanism
- [Contract — commit action](CONTRACT-commit-action.md) — what CB-2 calls again
- [Contract — the battle target buffer](CONTRACT-battle-target-buffer.md)

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** CB-1 to CB-6 became checks that fail if the shipping image says otherwise. CB-1's census is image-wide over every
listed body. Script: `Tools/analysis-kit/gfz-scripts/falsify_combo.py`, output `falsify_combo.out`, image `73461d08…`,
0 BROKEN. The draw-count and failure-path results are OPUS blocks 346 and cb26's executions, and are not re-run.

| # | Clause attacked | Result |
|---|---|---|
| C0 | §2 sizes | **survives**: 602 / 146 / 418 B |
| C1 | CB-1 by access width | **survives**: `+0x6B7` has seven accesses, one word-wide (`003106EB`). `+0x6B8` has 64, four of them byte-wide. The 64 counts three `lea` sites; without them it is 61 |
| C2 | CB-2 / CB-6 | **survives**: saves at `0030FA0F` / `0030FA19`, commit argument 1, `inc dil`, write-back only on success at `0030FA65` / `0030FA79` |
| C3 | CB-3 | **survives**: two `call 00379CD0` draw sites (`003886FD`, `003887E3`), an 11-iteration loop, the nibble stored with `and [rdi+0x12], 0xf` then `or [rdi+0x12], r14b` |
| C4 | CB-4 | **survives**: reload `+0x12`, `shr eax, 4`, `cmp ebx, eax`, `jae` |
| C5 | CB-5 | **survives**: the party records at `0208D480` and the foe records at `0208DE80` |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Two of this page's subjects are shared: the generator `00379CD0` (every caller of it draws from the same Mersenne Twister stream the combo count draws from) and the reset `003105D0` (every caller of it can clobber CB-1's word).*

**ActorEntity — SERVICE and CLIENT (6 edges).** The reset `003105D0` calls `BattleUnit_GetBySlotIndex` `00236820` and `BattleUnit_GetSlotCount` `00236850`, and is called by `BattleUnit_ResetStateForReuse` `00236A60`, `BattleUnit_TeardownAndDespawn` `00300E40`, the defeat-condition check `00300FC0` and `BattleGroup_RefreshFourActorDefinitions` `003266C0`. The actor layer's unit lifecycle (reuse, teardown, defeat, group refresh) runs the same reset the continuation path runs, so any of them also rewrites the word at `+0x6B7` that CB-1 is about; the unit-table getters are used by the reset's own slot scan.

**CombatAI — CLIENT (2 edges).** `BattleUnit_UpdateCombatFrame` `00308610` calls both the continue path `0030FA00` and the reset `003105D0`. The AI layer's combat frame is where a combo is asked to continue each frame, and where the reset is run outside a combo.

**CombatFormula — CLIENT (55 edges).** The owning-unit lookup `BattleStats_FindOwningBattleUnit` `0031B860` is called by the count roll `00388660`; `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` calls the reset `003105D0`; and 53 formula bodies call the generator `00379CD0`, among them `BattleFormula_RollSpecialGuardOutcome` `00387FD0`, `BattleFormula_RollGuardParryMode` `003884F0`, `BattleFormula_RollKnockback` `00388440`, `BattleFormula_RollAvoidGuardParryOutcome` `003896B0`, `BattleFormula_PrepareStrengthAttackVsDefense` `0038AAF0` and `BattleFormula_SelectPoachRewardItem95_5` `00390680`. Damage, guard, knockback and reward rolls draw from the same stream as the combo count, so the count a first hit gets depends on how many draws the formula layer made before it (section 9's determinism holds for a replay of the whole draw sequence, not of this path alone); the owner lookup is how `00388660` reads the counter off the unit (CB-5), and a stats rebuild is one more caller of the reset.

**CoreRuntimeScheduling — CLIENT (2 edges).** The main-loop bodies `0022B6E0` (the state-0 arm) and `0022B7E0` call the generator `00379CD0`. They advance the shared stream outside battle code; the combo count sees their draws only as a shifted position in that stream.

**Gameplay — SERVICE (1 edge).** The reset `003105D0` calls `BattleTargetBuffer_ResetPreservingFlag0` `00316CF0`, the ownerless target-buffer helper. Resetting a unit's action also resets its target buffer; this contract cites the reset only for CB-1's word store, which does not depend on the buffer.

**Movement — SERVICE (2 edges).** The reset `003105D0` calls `BattleLocomotion_ResetPathAndSetTargets` `003291B0` and `0033C9B0`. Cancelling an action releases the unit's locomotion path; the combo's own state is not in those bodies.

**RNG_Random_Selection — SERVICE (1 edge).** The count roll `00388660` calls `RNG_MT19937_NextU32_Thunk` `00379CD0` ~~twice~~ from two call sites, once or twelve times, on a unit whose counter is zero (CB-3) *(corrected 2026-10-02, OPUS: `003886FD`, and `003887E3` inside the 11-pass loop `003887DA`–`00388807`)*. This is the combo's only source of randomness, and it is the shared Mersenne Twister, not a private generator.

**Rewards_Progression_Economy — CLIENT (2 edges).** The per-level stat folds `002F9A60` and `002F9B20` call the generator `00379CD0`. Level-up growth draws from the same stream, so a level-up between two combo hits changes where the next zero-counter roll lands in it.

**Script_VM_Native_Bridge — CLIENT (2 edges).** The native verb bodies `00354BF0` and `00355140` call the generator `00379CD0`. Script random verbs share the stream with the combo roll.

**Status_Periodic_Terminal — CLIENT (3 edges).** `BattleUnit_ResetActionControlForStatusTransition` `00300140` and `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` call the reset `003105D0`, and `BattleFormula_AdvanceStatusTimersAndBuildResult` `00386C70` calls the generator `00379CD0`. A status transition can reset the unit mid-combo, and the periodic status tick draws from the same stream (the page's Relationships row names the periodic tick as a sharer of the generator).

**WorldAreaField — CLIENT (2 edges).** The weather resolver `0025ABA0` and the weather roll `0025ACA0` call the generator `00379CD0`. Weather transitions draw from the same Mersenne Twister stream; the combo count is one more consumer of it.
