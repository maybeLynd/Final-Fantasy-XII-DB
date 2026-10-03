# SWE2-AUDIT-SPEC review — fable-spawn-placement-height-and-authored-tuna-homing-1003

**Target.** `_index/candidates/fable-spawn-placement-height-and-authored-tuna-homing-1003/` (task `FABLE-REQ-AUDITSPEC-FABLE-SPAWN-PLACEMENT-HEIGHT-AND-AUTHORED-TU`)
**Verdict.** ACCEPT

## What was checked

- **Mechanical checker.** `fable-spawn-placement-height-and-authored-tuna-homing-1003/interior_applier.py` re-run verbatim in place: `FAILS 0`, matching the committed `interior_applier.out`.
- **Semantic pass.** All 1 rows / 5 anchors verified instruction-by-instruction against the certified shipping image (SHA256 `73461D08...D89721F8`, canonical VAs incl. image base). Every named address (call targets, globals, RIP-relative loads/stores, float constants) resolved to the claimed value; every stated offset, bound, sign, stride, arg order and branch polarity matched.

## Per-row notes

00235DD0 signed ecx selects 003272A0 vs the +0x2E call; -1.0 (01CEBC9C) on null; (xmm1,0.0,xmm2) stack vector; +0xE0/vector/+0x160 into the +0x6E call, 0031A930(xmm0,+0x160), then *360.0 (00902438) / 6.283185 (01CEBC78). All three image floats verified.

## Limits

Body statements only, per the package README — the sentences describe instruction behaviour, not semantics. Cloud-drafted rows stand on FABLE's re-read; this review independently re-derived every row from the image.
