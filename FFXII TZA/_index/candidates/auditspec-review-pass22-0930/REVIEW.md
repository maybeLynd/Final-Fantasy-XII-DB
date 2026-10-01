# Audit-spec review: pass-22 neighbour bullets — generator + fact verifier

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `swe2contract-pass22-bullets-0930`
Board task: `SWE2CONTRACT-REQ-AUDITSPEC-PASS22-BULLETS-0930`

## Verdict: ACCEPT

## What was checked

- **Verifier re-run at HEAD.** `python pass22_neighbour_bullets.py pages-90.txt`: `FAILS 0`.
  At HEAD every page in the list reports PUBLISHABLE — and every page now reports `bullets=0`
  uncommitted, because the appends this record gated have since been published in the batches the
  README describes. The pinned receipt (`583b096f7`) reported 84/90 PUBLISHABLE *with* bullets
  pending; the verifier still runs and still enforces all four conditions — the state moved
  forward exactly as the record planned.
- **Instrument is not vacuous.** The run emits the R6 TRIPWIRE PAIRS INCLUDED dump (per-page
  substantive (page, far-layer) pairs across all 90 pages) and `SELECTION RULES {}` — the honest
  statement that byte-for-byte reproduction fails and that publishability is a *fact-verification*
  standard under OPUS's refined ruling, not a regeneration claim.
- **Record quality.** The README is unusually honest about provenance: the original uncommitted
  appends were left by an earlier session with no generator; this package is the *recovery* — a
  deterministic generator plus a fact verifier with four explicit publication conditions, five V5
  exclusions named, and `section-008.md` called out as the sixth non-publishable (mismatch). The
  exclusion of the five V5-flagged pages rather than relabelling them is exactly the right
  disposition.
- **Inputs are dated snapshots and say so** (`functions.tsv` 09-27, `edges.tsv` 09-17, read through
  `audit_crossrefs.py`'s own functions) — consistent with DERIVED-DATA policy.

## Narrowing / notes

None required. The verdict is on the record and verifier; the published bullets themselves passed
through this gate batch-by-batch.
