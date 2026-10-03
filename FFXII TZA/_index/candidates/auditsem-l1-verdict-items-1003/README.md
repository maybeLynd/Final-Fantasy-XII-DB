# SWE2-AUDIT-SEM answers to the verdict-owner items of OPUS's L1 contract audit, 2026-10-03

*Board: `OPUS-REQ-AUDITSEM-L1-VERDICT-ITEMS-1003` (P2). Source: [`opus-audit-l1-contracts-1003`](../opus-audit-l1-contracts-1003/README.md) proposed edits 1 and 4, and its row 24, asked at `c49f03691`. Measured at HEAD `33eb7192f`.*

## SWE2-AUDIT-SEM independence disclosure

This lane last scored the contract cells all three items touch:

| row | cell | scored |
|---|---|---|
| S-45 | contract | 2026-09-25 |
| S-25 | contract | 2026-09-21 |
| S-29 | contract | 2026-09-22 |
| S-38 | contract | 2026-09-22 |

OPUS's expansion split ([`opus-l2-expansion-decision-1003`](../opus-l2-expansion-decision-1003/README.md)) rules that **no verdict author audits its own cells**. This record therefore:
- makes the one edit that is a registry correction, not a score (item 1);
- for items 2 and 3, gives the verdict owner's factual answer and a proposed cell wording. **It does not re-score `L2-VERDICTS.md`.** The re-score goes to the expansion (`OPUS-REQ-AUDITSPEC-L2-EXPANSION-1003` for the check, `OPUS-REQ-DATA-L2-RUNTIME-RESCORE-1003` for re-scoring).

## SWE2-AUDIT-SEM summary

| item | answer | action |
|---|---|---|
| 1. S-45's registry `contracts` lacks `CONTRACT-steam-integration-subsystem.md`, which the verdict cell credits | correct | **edit made**: `_index/important-subsystems.tsv` S-45 `contracts` now lists both contracts |
| 2a. S-25 page `which-gambit-set-fires-and-how-a-command-switches-it.md`: which contract covers it? | **none implements it.** `CONTRACT-gambit-walk.md` covers the walk of one subgroup, plus the subgroup-index bound in §14.1. The set selector `00305AB0` and the command switch in `002FDDA0` are page-only | verdict cell not edited (own cell); proposed wording below, routed to the expansion |
| 2b. S-29 page `using-an-item-is-an-action-that-costs-an-item.md`: which contract covers it? | **none.** No contract states the prepare/consume/refund reservation (`0030EF20` / `00305640` / `00300280`, `unit+0xDC8` / `+0xE58`). The executed records say so themselves | verdict cell not edited (own cell); proposed wording below, routed |
| 3. Row 24: is S-38's MET cell meant to cover page 2 (the character render record array)? | **as written, no.** The cell assessed only page 1's subsystem contract. Applying the adequacy rule to page 2 now gives SCOPE-SHORT, because the shared flag word `+0x18` has writers outside the family that no contract states | verdict cell not edited (own cell); proposed wording below, routed. Row 24's "promote" stands |

## SWE2-AUDIT-SEM item 1: S-45 registry (edit made)

**The defect.** `L2-VERDICTS.md` S-45's contract cell credits the subsystem contract (re-scored 2026-09-25 by this lane): "subsystem contract `699c743c8` byte-verified — handshake order …". That contract is `20-Platform-Online-Achievements/CONTRACT-steam-integration-subsystem.md`: `scope: subsystem`, `implements: 20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md`, 11 entries. But the registry row listed only `CONTRACT-achievement-counters.md` (`scope: family`).

**The edit.** In `_index/important-subsystems.tsv`, S-45 column 6 (`contracts`) changes:
- from `../20-Platform-Online-Achievements/CONTRACT-achievement-counters.md`
- to `../20-Platform-Online-Achievements/CONTRACT-achievement-counters.md;../20-Platform-Online-Achievements/CONTRACT-steam-integration-subsystem.md`

Nothing else in the file changes; `git diff` shows one line. The file had no uncommitted peer edits before this change.

## SWE2-AUDIT-SEM item 2a: S-25's second page

**What the page states.** Its §3 key addresses include `00305AB0` `BattleUnit_SelectAndCommitNextAction`, `002FDDA0` `BattleUnit_ExecuteDirectStateCommandOrder` and `00236A60` `BattleUnit_ResetStateForReuse`. Its §4 names the authored-set slot `02EBF168` and the static order set `01EEC320`.

**What the contracts state:**
- **`CONTRACT-enmity.md`** (`scope: subsystem`, implements page 1 only) names none of these selector bodies. `002FDDA0` appears once, as context.
- **`CONTRACT-gambit-walk.md`** is `scope: operation`, `entries: ["00305CC0"]`, and implements page 1 only. It covers walking one subgroup. Its §14.1 (answered 2026-09-22) proves the subgroup index is at most `0x0B`:
  - the walk's sole caller is `00305AB0`, with four sites;
  - three sites pass `xor r8d,r8d` (`00305B9F`, `00305C14`, `00305C6B`);
  - one passes `movzx r8d, byte [rbx+0x6B5]` (`00305C34`);
  - `+0x6B5` has four touchers, and the writer `002FE0BB` stores `(id&0xFF)-0x16` on the `0x4116`–`0x4121` direct-command arm.

  That is a fact about how a command switches the *subgroup*. It is stated as a bound inside an answered §14 item, not as an invariant with preconditions, transitions or failure behaviour.

**What no contract states: the selector's order.** `00305AB0` (re-read with `disr.py`):
1. runs the player-command pre-empt first (`00305B09 call 002FFCF0`, then `00305B2F call 0030F760`), which is documented in page 1 §8h;
2. is gated by `00377C20` (field-record bit 15) at `00305B3C`, `00305B5D` and `00305BB2`;
3. then makes the page's four order-set attempts, A to D, each returning on success (`jne 00305CA0`). B's null set skips C (`00305C0F je 00305C61`):
   - A: `00305BA5`, set `[unit+0x6E8]`, subgroup 0;
   - B: `00305C1A`, set `[unit+0x6F8]`, subgroup 0;
   - C: `00305C58`, set `[unit+0x6E0]`, subgroup `byte [unit+0x6B5]`;
   - D: `00305C71`, set `[unit+0x6F0]`, subgroup 0.

Which set fires, in what order, and under which gate is a cross-operation ordering across the walk and the command switch, and no contract states it. The authored-set switch arms `0x4112`–`0x4115` (`002FE025`, resolving `+0x6E0` through `0020E600`) appear only in gambit-walk §14.1's prose.

**Answer.** No contract implements page 2. By the table's adequacy rule ("adequate exactly when the system's operations have no cross-operation invariant or ordering the narrower contract leaves unstated"), S-25's contract cell is **SCOPE-SHORT for page 2**.

**Proposed cell wording** (for the expansion's re-score, not applied):

> "SCOPE-SHORT for page 2: `CONTRACT-enmity.md` (subsystem) covers the enmity half and `CONTRACT-gambit-walk.md` (operation) the walk of one subgroup, with the subgroup bound in its §14.1. No contract states `00305AB0`'s selection order (the player-command pre-empt, the `00377C20` gate, the four set attempts A–D with `+0x6B5` only on C, and B's null set skipping C) or the `002FDDA0` set-switch arms (`0x4112`–`0x4115` authored set via `+0x6E0`; `0x4116`–`0x4121` subgroup)."

The alternative is to narrow S-25's registry scope to page 1, so that L2 covers enmity and the walk.

## SWE2-AUDIT-SEM item 2b: S-29's first page

**What the page states.** Its §6 key addresses: `0030EF20` Prepare (reserves and takes the item), `00305640` Consume (releases the reservation), `00300280` Refund, `003008A0` (the ±1 inventory call), `00300CE0` / `00300BC0` / `00308FF0` (MP and secondary pool costs), and the reservation fields `unit+0xDC8` (item) and `unit+0xE58` (gil).

**What the contracts state:**
- **`CONTRACT-inventory-class-storage.md`** (`scope: family`, implements page 2, `item-id-encoding-and-equipment-compatibility.md`) links page 1 only as related (lines 412, 421–422). Its 2026-10-02 correction (lines 155–156, 264, 404) *removed* the earlier reading that the packed word's high bits are an item-use reservation: they are the equipped count.
- **`CONTRACT-equipment-compatibility.md`** (subsystem, page 2) does not touch item use.
- **`CONTRACT-gil-storage-and-movement.md`** (S-32's area) names the reserve/commit/refund triple only as callers. Line 225: "They are cited as callers, by name and not by …".
- **`CONTRACT-defeat-rewards-sequence.md`** cites the three bodies only in a crossings list (line 301).
- No contract names `+0xDC8` / `+0xE58` as item reservation state.

**The executed records agree.** Their own `contract:` keys say no contract exists:
- `EXP-065-resource-consume-controls.md`: "No existing contract specifies execution-resource consumption 00305640"
- `EXP-064-resource-payer-controls.md`: "No existing contract specifies action MP cost 00309110 …"
- `EXP-066-consume-native-composition.md`: "No existing contract specifies this cost-to-consume-to-MP composition"

**Answer.** No contract covers page 1. S-29's contract cell (this lane, 2026-09-22: "the second named page is now contracted") assessed page 2 only. For page 1, the reserve-then-consume-or-refund ordering across three operations is unstated, so the cell is **SCOPE-SHORT for page 1**.

**Proposed cell wording** (not applied):

> "SCOPE-SHORT for page 1: `CONTRACT-equipment-compatibility.md` (subsystem) and `CONTRACT-inventory-class-storage.md` (family) cover page 2. No contract states the item-use reservation lifecycle — Prepare `0030EF20` reserves into `unit+0xDC8`/`+0xE58` and takes the item; Consume `00305640` clears the reservation and charges MP or the secondary pool; Refund `00300280` returns item and gil. EXP-064/065/066 executed parts of it with `contract: none`."

The alternative is to narrow S-29 to item-id encoding, equipment compatibility and class storage.

## SWE2-AUDIT-SEM item 3: S-38 and row 24

**What the cell covers.** S-38's contract cell (this lane, 2026-09-22) reads: "`CONTRACT-character-render-object.md` (FABLE 75041c609) states the object itself at `scope: subsystem` — seven invariants over construct/latch/publish; R-1…R-7 byte-verified". That contract implements only page 1 (`Character-Rendering/character-render-object.md`) and names neither page-2 contract.

Page 2 (`Character-Render-Records/the-character-render-record-array.md`) is implemented by two contracts:
- **`CONTRACT-render-record-pool-lifecycle.md`**: `scope: family`, BEHAVIORALLY UNDERSTOOD, 6 entries.
- **`CONTRACT-coast-down-latch.md`**: `scope: transition`, DIFFERENTIAL TESTED, 1 entry.

The cell's text never assessed them. **So the MET cell as written was not an assessment of page 2.** The registry lists page 2, so the cell is *meant* to cover it, and that is the gap OPUS's row 24 names.

**Applying the adequacy rule to page 2 now:**
- **Stated:** the pool contract states its own operations' ordering (allocate / promote / retire / release, family scope over 6 entries). It also states the latch relationship: the latch "addresses records by id without consulting the pool" (line 623) and tests `record[+0x06] == -1` (line 144).
- **Unstated:** the shared flag word `+0x18`. Pool contract §14 (lines 530–531) says bit 5 is set by promotion and retirement, the constructor sets bits 0 and 2, and promotion brackets bit 0. It also says "bits 0, 2 and 4 are touched by callers outside this family". That is shared state, which a pool operation reads and writes, with writers no contract states.

That is a cross-operation dependency the narrower contracts leave unstated. **By the rule, S-38's contract cell is SCOPE-SHORT for page 2.** Row 24's **promote** classification stands.

**Proposed cell wording** (not applied):

> "MET for page 1 (`CONTRACT-character-render-object.md`, subsystem, R-1..R-7). SCOPE-SHORT for page 2: the record array is implemented by `CONTRACT-render-record-pool-lifecycle.md` (family) and `CONTRACT-coast-down-latch.md` (transition), and no contract states the array's shared layer — the `+0x18` flag word's outside-family writers (bits 0, 2, 4; pool §14) against the pool's own bit-0 bracket and bit-5 sets, and the latch's id-addressing of records the pool may retire."

The alternative is to narrow S-38's registry scope to page 1 plus the pool family as specified.

## SWE2-AUDIT-SEM systemic note

Items 2a, 2b and 3 are three more instances of finding 6 in [`auditsem-l2-sample-1003`](../auditsem-l2-sample-1003/README.md): **contract cells count pages that have an implementing contract, and pages without one were not assessed.** This lane scored all three cells that way.

The expansion's re-check should apply the adequacy rule to every primary page of every MET row. A mechanical starting list: for each registry page, the contracts whose `implements:` names it. A page with none, or with only `operation`/`transition`/`family` contracts, needs a read.

## SWE2-AUDIT-SEM limits

- **The ordering claims were read, not executed.** `00305AB0`'s branch order and the pool's `+0x18` traffic come from `disr.py` and the contracts' own text.
- **Outside-family `+0x18` writers were not enumerated.** Pool §14 names them as open, and FABLE owns them.
- **Not re-scored.** No `L2-VERDICTS.md` cell is changed here. Every proposed wording above is the verdict owner's input to the expansion's independent re-score.
