# SWE2-AUDIT-SPEC review — fable-ta-texture-animation-lists-homing-1003

**Target.** `_index/candidates/fable-ta-texture-animation-lists-homing-1003/` (task `FABLE-REQ-AUDITSPEC-FABLE-TA-TEXTURE-ANIMATION-LISTS-HOMING-1003`)
**Verdict.** ACCEPT

## What was checked

- **Mechanical checker.** `fable-ta-texture-animation-lists-homing-1003/interior_applier.py` re-run verbatim in place: `FAILS 0`, matching the committed `interior_applier.out`.
- **Semantic pass.** All 5 rows / 24 anchors verified instruction-by-instruction against the certified shipping image (SHA256 `73461D08...D89721F8`, canonical VAs incl. image base). Every named address (call targets, globals, RIP-relative loads/stores, float constants) resolved to the claimed value; every stated offset, bound, sign, stride, arg order and branch polarity matched.

## Per-row notes

0019D420 strided 0x130 record loop: null-skip, 0x100 copy in two 0x80 passes, 0019D8D0(+0x100,+0x100), +0x120/+0x128 tail fields, fixed r8 source. 0019D970 single-record twin. 001AAE70 release through vcall +0x18 with magic-divide (r8 = ((+0x10 - +0)/0x30 signed)*0x30). 001AD0C0 bump-allocate-or-001AB8A0. 001B6A70 dual list walk (00185A90/0016D6D0 then 00220390 + vcall+0x18 size 0x28), sentinel re-point, +0x60==0 return.

## Limits

Body statements only, per the package README — the sentences describe instruction behaviour, not semantics. Cloud-drafted rows stand on FABLE's re-read; this review independently re-derived every row from the image.
