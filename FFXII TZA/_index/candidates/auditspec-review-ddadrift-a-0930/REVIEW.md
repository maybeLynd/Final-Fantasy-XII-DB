# Audit-spec review: EC7 DD A-drift pairing (the F-jump census)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `ec7-dd-adrift-pairing-0930`
Board task: `SWE2-EC7-REQ-AUDITSPEC-DDADRIFT-A-0930`

## Verdict: ACCEPT

## What was checked

- **Pairing table.** `pairing.tsv` (39 rows) verified cite-by-cite at HEAD: every interior cite is
  present on its citing page — zero missing. Sample checked row-level detail: e.g.
  `ScriptVM.VerbAdapter` member `0050E300` cited at `0050E318` inside
  `the-source-block-mover-and-separate-consumer-refresh.md`, cause "page re-statused to
  evidence-bearing" at `9bda44687`.
- **Claim structure.** The core claim — the F jump 4,765→9,955 was *entirely* rows refused whole
  because a member became A (linkage drift 5,227 + pre-existing undeclared frontier 4,728), with
  **semantic loss 0** (A lost 0, gained 83) — is the falsifiable core and is stated with explicit
  baselines (`50890aa7f` vs `06c849caf`, `fbucket.py` calling `check_dispositions.evaluate`
  directly). The "every cause is a page re-status" claim is consistent with the pairing table's
  own cause column.
- **Mechanism honestly described.** "A row is refused whole when one member is A" and "A beats a
  declaration" — this is the known refuse-whole semantics of `check_dispositions`, and the record
  correctly identifies the +5,190 as an accounting effect, not a knowledge loss.

## Narrowing / notes

None required.
