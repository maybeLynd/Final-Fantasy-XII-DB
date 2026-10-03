# SWE2-AUDIT-SPEC review — fable-the-ordered-render-command-list-homing-1003

**Target.** `_index/candidates/fable-the-ordered-render-command-list-homing-1003/` (task `FABLE-REQ-AUDITSPEC-FABLE-THE-ORDERED-RENDER-COMMAND-LIST-HOMING`)
**Verdict.** ACCEPT

## What was checked

- **Mechanical checker.** `fable-the-ordered-render-command-list-homing-1003/interior_applier.py` re-run verbatim in place: `FAILS 0`, matching the committed `interior_applier.out`.
- **Semantic pass.** All 29 rows / 127 anchors verified instruction-by-instruction against the certified shipping image (SHA256 `73461D08...D89721F8`, canonical VAs incl. image base). Every named address (call targets, globals, RIP-relative loads/stores, float constants) resolved to the claimed value; every stated offset, bound, sign, stride, arg order and branch polarity matched.

## Per-row notes

29 rows byte-exact. Highlights: 001A1850 dual-path assert+vcall logic; 001B27E0 0xE0 copy, 8x0x1C record loop with double-precision abs trick (mask qword 0x7FFF... at 01CEBD80), unsigned cvtsi2ss, 10.0 (008F8180) gate, self*product/product rewrite clamped 0..1.0 (01CEBBA8); 002228A0 dense S-dispatch (S0 extra calls, S2 ret, S3 reset, +0xF8 word-pair (r8w-1,0) path, +0x113/+0x126 vs 0.0 fifth float); the 002249xx twin family; 00314B80-CD0 byte-field setters on the 002EF2B0 record (+0x1062/+0x1063 bit ops); 003437A0 arg-restore + bit6 clear + +0xC store; 005D8E40 two-level null chain; 00863350 vtable store + dual pointer-slot calls + edx bit0 delete.

## Limits

Body statements only, per the package README — the sentences describe instruction behaviour, not semantics. Cloud-drafted rows stand on FABLE's re-read; this review independently re-derived every row from the image.
