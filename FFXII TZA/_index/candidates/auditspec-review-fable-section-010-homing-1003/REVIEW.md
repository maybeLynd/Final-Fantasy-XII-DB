# SWE2-AUDIT-SPEC review — fable-section-010-homing-1003

**Target.** `_index/candidates/fable-section-010-homing-1003/` (task `FABLE-REQ-AUDITSPEC-FABLE-SECTION-010-HOMING-1003`)
**Verdict.** ACCEPT

## What was checked

- **Mechanical checker.** `fable-section-010-homing-1003/interior_applier.py` re-run verbatim in place: `FAILS 0`, matching the committed `interior_applier.out`.
- **Semantic pass.** All 3 rows / 13 anchors verified instruction-by-instruction against the certified shipping image (SHA256 `73461D08...D89721F8`, canonical VAs incl. image base). Every named address (call targets, globals, RIP-relative loads/stores, float constants) resolved to the claimed value; every stated offset, bound, sign, stride, arg order and branch polarity matched.

## Per-row notes

0034E220 dual tail-jump dispatch (non-zero -> 002E64E0(rdx) / zero -> 002EBE50(rdx,0,0)); 003B7A30 null-gated head call then signed-bounded loop over 02EBCAC0 with per-iteration re-read of dword 02EBCBC0; 003B7AB0 same loop over 02EBCA80/02EBCAA0 without the null check. All globals and the 00263F40 pre-call confirmed.

## Limits

Body statements only, per the package README — the sentences describe instruction behaviour, not semantics. Cloud-drafted rows stand on FABLE's re-read; this review independently re-derived every row from the image.
