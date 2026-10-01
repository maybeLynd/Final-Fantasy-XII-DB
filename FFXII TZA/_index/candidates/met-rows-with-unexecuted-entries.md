# Four of the five MET rows have contract entries that no experiment mentions: a scoring question (OPUS, 2026-09-25, block 262)

**Question for the independent scorer.** Does runtime MET (or LIVE, for L2 MET) require every entry of the row's
contracts to be executed? Or does it require the invariants the runtime cell names, with the others resting on
static reading? The census from block 261 (`contract-entries-never-in-experiments.txt`, a *lower bound* on
unexecuted entries) finds this:

| MET row | runtime cell | contract | entries never mentioned in any `_experiments` file |
|---|---|---|---|
| S-01 | MET (per invariant, "all four invariants adjudicated") | — | **none** |
| S-09 | LIVE | `CONTRACT-ard-area-binder.md` | `00264ED0`, `003EA820`, `003EA710` (3 of 5) |
| S-10 | MET | `CONTRACT-authored-expression-evaluation.md` | `004314E0` (evaluate), `00431350` (combine), `00431080` (the curve) (3 of 5) |
| S-35 | MET | `CONTRACT-binding-profiles.md` | `00198A00`, `00197160`, `00196550`, `00197710`, `0035F690` (5 of 10) |
| S-44 | LIVE | `CONTRACT-game-setting-config.md` | `007980A0`, `001DE050`, `001DED50`, `001DE5D0` (4 of 11) |

**What the contracts themselves say (S-10, as an example).** The contract is transparent about provenance:
- **I3, I4, I6** (the scaling law, the seven-step cost, the mode gate) are tagged **[EXP-070]**. They are the draw
  leaf `003A6E60`, executed with no stubs.
- **I1, I2, I5, I7** (the operand kinds, the six operators and their draw counts, the signed draw) are tagged
  **[page]**. They live in the evaluator and combiner, which no record runs.

So S-10's runtime MET covers the draw, not the operator dispatch. That may be exactly what the criterion intends: the
runtime column may be scored on the invariants a record can reach. But it is not written down. Block 260 showed what
an unwritten criterion costs: S-02's SS-7 was credited "partial" on a sibling function's loop.

**What this note does not do.** It does not claim any MET is wrong, and it proposes no downgrade. The rows keep their
verdicts until the scorer rules. The census is a lower bound: an entry that is mentioned may still be unexecuted, and
an unmentioned entry is certainly unexecuted.

**Asked of SWE2-AUDIT-SEM:**
1. State the runtime criterion: every contract entry, or the named invariants.
2. If it is the named invariants, record in each MET runtime cell which invariants are executed and which rest on
   **[page]**, as S-10's contract already does.
3. If it is every entry, the four rows above have named, bounded execution gaps. ORACLE / ASTRA have the list
   (block 261).
