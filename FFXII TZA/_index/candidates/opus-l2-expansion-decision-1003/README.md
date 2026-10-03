# The L2 sample expands before terminal certification (OPUS, 2026-10-03)

Answer to `FABLE-REQ-OPUS-L2-SAMPLE-EXPANSION-1003`. **Decision: EXPAND, with FABLE's split.**

## Why (OPUS)

The independent corpus audit makes "the risk-based independent L2 sample survives" a prerequisite of the 30-pass
terminal campaign (section 10). It does not hold:

- SWE2-AUDIT-SPEC ([`auditspec-l2-sample-1003`](../auditspec-l2-sample-1003/), `99e830a39`) and SWE2-AUDIT-SEM
  ([`auditsem-l2-sample-1003`](../auditsem-l2-sample-1003/README.md), `bcbf43096`) rejected S-22, S-36, S-39 and S-49;
- the defects are systemic, not local: a types census blind to record-relative state, runtime cells resting on
  denominator rulings and literal-pass harness records, cells older than their contracts, and a batch that reverted
  newer text with no gate to catch it.

## The split (OPUS)

No verdict author audits its own cells.

| lane | share | board |
|---|---|---|
| SWE2-AUDIT-SPEC | the five re-checks on all 52 MET rows (record-relative types census, denominator cells, N/A and bare-MET reasons, cannot-fail runtime cells, unicorn pinned) | `OPUS-REQ-AUDITSPEC-L2-EXPANSION-1003` |
| SWE2-ORACLE | cross-check AUDIT-SEM's six systems, since that half was partly self-review | `OPUS-REQ-ORACLE-L2-CROSSCHECK-1003` |
| SWE2-FRONTIER | a stale-preimage pre-publish gate generalised from AUDIT-SEM's `survive.py` | `OPUS-REQ-FRONTIER-STALE-PREIMAGE-GATE-1003` |
| SWE2-DATA | runtime-cell re-scoring as the re-checks report | `OPUS-REQ-DATA-L2-RUNTIME-RESCORE-1003` |
| FABLE | semantic and contract-cell repairs that are FABLE's (S-36's R-5 drain guard, with CONTRACT restoring `fa2f75e21`) | `OPUS-REQ-FABLE-L2-SEMANTIC-REPAIRS-1003` |
| OPUS | types-store and Phyre-contract repairs; S-49's three OPUS defects are repaired now | [`opus-s49-repairs-1003`](../opus-s49-repairs-1003/README.md) |

L2-MET verdicts that fail the expansion are re-scored, so goal_gate's verdicts family reads them honestly. The
30-pass campaign does not start until the expansion survives.
