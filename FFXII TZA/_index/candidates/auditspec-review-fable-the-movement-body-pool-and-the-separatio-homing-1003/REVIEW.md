# SWE2-AUDIT-SPEC review — fable-the-movement-body-pool-and-the-separatio-homing-1003

**Target.** `_index/candidates/fable-the-movement-body-pool-and-the-separatio-homing-1003/` (task `FABLE-REQ-AUDITSPEC-FABLE-THE-MOVEMENT-BODY-POOL-AND-THE-SEPARAT`)
**Verdict.** ACCEPT

## What was checked

- **Mechanical checker.** `fable-the-movement-body-pool-and-the-separatio-homing-1003/interior_applier.py` re-run verbatim in place: `FAILS 0`, matching the committed `interior_applier.out`.
- **Semantic pass.** All 8 rows / 40 anchors verified instruction-by-instruction against the certified shipping image (SHA256 `73461D08...D89721F8`, canonical VAs incl. image base). Every named address (call targets, globals, RIP-relative loads/stores, float constants) resolved to the claimed value; every stated offset, bound, sign, stride, arg order and branch polarity matched.

## Per-row notes

0023B2A0 xmm rotation swap; 00347D20 double-00267E10 then 00263770 + conditional 002EBC70; 0034A340/34F210/350C30 the 00267DB0 3- and 4-float gather families with correct xmm ordering (C,B,A / D,C,B then A); 00379240/70 offset tail-jumps with lea-encoded constants (0x12/5); 003DE4C0 the big E=02B58C50+ecx*0x70 record init — byte E+0x20 selector (2/4/1), conditional release, zeroing, E+0x20 header fill (0x100c002 etc.), all dword/qword stores and final rdx back-stores.

## Limits

Body statements only, per the package README — the sentences describe instruction behaviour, not semantics. Cloud-drafted rows stand on FABLE's re-read; this review independently re-derived every row from the image.
