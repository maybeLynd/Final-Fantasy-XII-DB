# Consumer-check record — catalogue chained-tails ruling (SWE2-FRONTIER, 2026-09-29)

Affected: `Database/FFXII TZA/_index/candidates/register-triage/batch-K-scope-rulings.md`
(Extension 2026-09-29 — chained-tail ruling appended; no other file touched).

**What the ruling decides:** the executable view extends to each listed root's chained `.pdata`
union as executable definition v3 with a recorded series break; the authored catalogue does not
change; corrections land as mechanical `underrun-extend` rows in `FUNCTION-EXTENT-ERRATA.tsv`;
`.pdata` is extent evidence only, never semantic.

**Consumers:**
- `OPUS-REQ-FRONTIER-CATALOGUE-CHAINED-TAILS` — the request the ruling answers; consumer is OPUS's
  `uc1_band.apply`/`population_cover` path plus the errata consumers named in the ruling
  (`program_coverage.py`, `receiver_flow_census.py`, `field_disp_scan.py`).
- `FUNCTION-EXTENT-ERRATA.tsv` — the ledger the ruling routes the 270 corrections into
  (158 underrun-extend rows already applied at `906d5480a`).
- Evidence: `624e3534e`, `_index/candidates/fragment-size-sweep-0929/` (sweep.tsv, tail-recheck.txt).
- Precedent register: `underrun-errata-apply-0929/consumer-check.md` records that no current
  loader honours `underrun-extend` — the ruling's consumer-wiring condition exists precisely because
  that is true.

**Not claimed:** that any errata row, extent change, or consumer wiring has been applied — this
record covers the ruling text only; the v3 apply is OPUS's task under the stated conditions.
