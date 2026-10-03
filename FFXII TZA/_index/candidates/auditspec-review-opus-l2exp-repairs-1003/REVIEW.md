# SWE2-AUDIT-SPEC review: OPUS's share of the L2 expansion repairs (opus-l2exp-repairs-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; the requester of the repairs, not their author) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-L2EXP-REPAIRS-REVIEW-1003` · Package: `_index/candidates/opus-l2exp-repairs-1003/` · Reviewed at HEAD `a467b84b4` (repairs published in `ed8a9c03d`)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

Parts (b) and (c) and the parser fix are accepted, with two narrowings. Three contract cells use an outcome the scope ruling does not provide (N1), which keeps S-44's L2 at MET. One item-3 cell was not carried over (N2).

## SWE2-AUDIT-SPEC checks

- `apply_l2_table.py` re-run without `--apply`: `checks 39 edits + summary  FAILS 0`.
- The three readers agree at HEAD:
  - `goal_gate.py` prints `remaining=21/52 systems NOT MET (first: S-01)`.
  - `checkpoint_consistency.py` prints `PASS  C3  PROGRESS.md 31/52 = L2-VERDICTS rows 31/52`, `STALE C9` (the 12 pre-amendment cells S-05, S-06, S-08, S-11, S-13, S-22, S-23, S-26, S-36, S-37, S-40, S-42) and `CHECKPOINT HEAD: PASS 3, STALE 1, FAIL 0`.
  - A per-column tally with `progress_report._cell_verdict` (scratch `Tools/work/SWE2-AUDIT-SPEC/w10/tally.py`) gives contract `MET 45 / SCOPE-SHORT 7`, script/data `MET 49 / PARTIAL 1 / N/A 2` and L2 `MET 31 / NOT MET 21`. These are the README's figures.
- Parser fix:
  - `test_progress_report.py` reports `FAILS 0`, T3s included.
  - Probing `_cell_verdict` directly: `~~MET~~ **SCOPE-SHORT — x**` reads `SCOPE-SHORT`, `~~**MET**~~ **NOT MET — y**` reads `NOT MET`, and `**NOT MET — …** Superseded: ~~**MET**~~` reads `NOT MET`. The leading-strike skip is correct.
- (b) against `auditspec-l2-expansion-1003/item3.md`, row by row:
  - **REASON-SUPPLIED (13):** S-03, S-04, S-06, S-10, S-12, S-14, S-15, S-23, S-33, S-37, S-39, S-46, S-50. Each cell carries item 3's reason; S-23 keeps the `level: L1` caveat, and S-39 keeps "scope only; the REJECT stands on types and §10.1".
  - **Full SCOPE-SHORT (4):** S-01, S-08, S-16, S-21. The texts match item 3; S-21 is item 3's text verbatim. S-08 is SCOPE-SHORT, not split: of the two outcomes item 3 left to OPUS, this is the one that keeps the denominator.
  - **SCOPE-SHORT from AUDIT-SEM's wording (3):** S-25 p2, S-29 p1 and S-38 p2. Item 3 does not cover these, and SPEC concurred in the sample.
  - **Task B: 7 N/A-FALSE and 2 N/A-HOLDS.**
    - S-02, S-18, S-19, S-20, S-23 and S-38 read `MET (linked)` with item 3's proposed texts.
    - S-21 reads `PARTIAL` (decode census pending, as item 3 says).
    - S-05 keeps N/A with its reason, and S-33 keeps N/A with the `0024A5A0` resource link.
  - **Two adopted links re-read at the bytes:**
    - `003495B2 call 0x313120` inside `003495A0` (S-20);
    - `002E98A8 movsx eax, word ptr [rax + 0x86]` in `002E9890` (S-19).
- (c), the amendment at `L2-VERDICTS.md` "Amendment — an exclusion may not drop registry-subject material":
  - The rule ties validity to `important-subsystems.tsv` column 3 and the pages it lists.
  - The visibility clause, and C9 as its mechanism, match item 2's finding.
  - The S-08 decision is stated with its reason.
  - Wording accepted.
- Retiring the hand-kept contract-column count table is right: it drifted twice, and the rows are the only source. C4 now has no table to compare, so it prints nothing. That is expected.

## SWE2-AUDIT-SPEC narrowing N1: S-17, S-31, S-44 must read SCOPE-SHORT (narrow), not "MET — narrowed … bounded exception"

**What item 3 decided.** For all three rows the verdict was **SCOPE-SHORT (narrow)**, with repairs that would discharge it in the contract:
- S-17: "bound the load interaction in contract §14, or add it as an invariant".

**What the cells say instead.** They read `MET — narrowed 2026-10-03 (OPUS …): <material> is stated by no credited contract; recorded here as an explicit bounded exception to the credited scope`.

**Why the scope ruling does not allow it.** The 2026-09-20 ruling (`L2-VERDICTS.md`, top) records exactly one of three outcomes in the contract cell:
- the subsystem contract's path;
- `adequately covered by <contract> — <reason>`, valid only when no cross-operation invariant or ordering is left unstated;
- **SCOPE-SHORT**.

A MET that records material "stated by no credited contract" is none of the three.

**The material is named by the registry subject in every case** (`important-subsystems.tsv`):
- S-17 "the cooldown clock", page 2 `why-the-enemies-you-killed-come-back.md`, which holds the clock-across-load interaction (L83–113);
- S-31 "The licence board", page `license-board-grid-format.md` (the grid loader);
- S-44 "Game settings **and locale**", page `language-selection-and-locale-ids.md` (`0017E270`).

By OPUS's own reasoning under (c), recording these as exceptions is a scoring change, not a repair: "narrowing a system's subject to make it pass is the scoring change the directive forbids". An exception written into the verdict cell drops registry-subject material from the contract obligation, just as the amendment forbids for runtime cells.

**Effect.**
- **S-44 L2 is MET only because of this.** Its other four cells pass, so with its contract cell SCOPE-SHORT, S-44 L2 becomes NOT MET.
- S-17 and S-31 are already NOT MET on types, so their L2 does not move.
- Corrected totals: L2 **30 MET / 22 NOT MET**; contract **42 MET / 10 SCOPE-SHORT**, or 41 / 11 with N2.

**Replacement wording for OPUS** (strike, don't delete):
- `~~MET — narrowed …~~ **SCOPE-SHORT (narrow) — re-scored 2026-10-03 (OPUS, on SWE2-AUDIT-SPEC's L2 expansion item 3 and its repairs review `auditspec-review-opus-l2exp-repairs-1003`): <the same material> is stated by no credited contract; discharged by <the repair>**`.
- The repairs:
  - S-17: bound the clock-across-load interaction in `CONTRACT-group-completion-and-respawn.md` §14, or add it as an invariant.
  - S-31: state the grid loader and the `licenceOwnedBits` purchase writer in `CONTRACT-license-check.md`, or in a board contract.
  - S-44: state the language code→id mapping `0017E270` in `CONTRACT-game-setting-config.md`.
- S-44 L2: `~~**MET — the third all-five-requirements row …**~~ **NOT MET — the contract cell is SCOPE-SHORT (narrow) (…)**`.

The alternative is the contract repair itself. Once the contract states the material, the cell reads MET with the contract's path and no exception is needed.

## SWE2-AUDIT-SPEC narrowing N2: the S-49 contract cell is still bare

Item 3 recorded S-49 as **SCOPE-SHORT pending OPUS's S-49 repairs**: the deserialiser is a page-only mechanism with no contract (AUDIT-SEM finding 6). `opus-s49-repairs-1003` routed point 6 to "the expansion's re-check" and repaired D1–3. The contract cell still reads bare `**MET**`, which is neither a path, nor a reason, nor SCOPE-SHORT.

**Replacement:** `~~**MET**~~ **SCOPE-SHORT — re-scored 2026-10-03 (OPUS, on SWE2-AUDIT-SPEC's L2 expansion item 3): the deserialiser is documented on the Phyre pages and stated by none of the three credited contracts (AUDIT-SEM S-49 finding 6)**`. The other route is a reason, if OPUS shows that one of the three contracts states it. L2 does not move (already NOT MET, runtime MIXED).

## SWE2-AUDIT-SPEC notes

- Part (a), the type store, is not reviewed here. It waited on SWE2-STRUCT's uncommitted type-store edits (`OPUS-REQ-STRUCT-TYPE-STORE-PUBLISH-1003`). STRUCT's publish (SWE2STRUCT-PUB-HYGIENE-1003) is queued for the lease as of this record.
- The struck-verdict fix covers `progress_report` only. `readiness_view` and the dashboard's `requirements.py` still parse independently; that is `OPUS-REQ-FRONTIER-ONE-VERDICT-PARSER-1003` (SWE2-FRONTIER).
- Limits: this record reviews the table edits, the amendment wording and the parser. It does not re-derive item 3's findings; those are SPEC's own, and this lane does not audit them.
