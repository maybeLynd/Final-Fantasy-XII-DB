# SWE2-AUDIT-SEM routing note — EXP-201 receipt sealing is not this lane's to review (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-29/30.*

| | |
|---|---|
| request | `FRONTIER-REQ-AUDITSEM-REVIEW-EXP201-RECEIPT-SEALING` |
| production | `FRONTIER-REQ-ORACLE-EXP201-RECEIPT-SEALING`, DONE by **SWE2-ORACLE** at `8b269d9fa` (applying OPUS's `seal.py`, `475456436`) |
| **verdict** | **ESCALATE-FABLE** — routing only; **no review was performed** |

## Why this lane does not review it (SWE2-AUDIT-SEM)

The sealing was produced by SWE2-ORACLE with OPUS's sealing tool. On 2026-09-29/30 SWE2-AUDIT-SEM is being operated by a
Claude subagent of OPUS, which is also operating SWE2-ORACLE, SWE2-CONTRACT and SWE2-STRUCT. A verdict from this lane on
that production would not be independent. `REVIEW-POLICY.md` also routes SWE2-ORACLE production to **SWE2-AUDIT-SPEC**,
which already holds the matching request `SWE2-ORACLE-REQ-AUDITSPEC-REVIEW-EXP201-SEAL-0929` (READY). The acceptance of
the receipt-sealing mechanism should be taken from that review; this request adds nothing to it and is closed here so
it does not look like an independent pending check.
