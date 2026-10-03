# SWE2-AUDIT-SPEC review — fable-the-map-ctrl-pack-homing-1003

**Target.** `_index/candidates/fable-the-map-ctrl-pack-homing-1003/` (task `FABLE-REQ-AUDITSPEC-FABLE-THE-MAP-CTRL-PACK-HOMING-1003`)
**Verdict.** ACCEPT

## What was checked

- **Mechanical checker.** `fable-the-map-ctrl-pack-homing-1003/interior_applier.py` re-run verbatim in place: `FAILS 0`, matching the committed `interior_applier.out`.
- **Semantic pass.** All 31 rows / 143 anchors verified instruction-by-instruction against the certified shipping image (SHA256 `73461D08...D89721F8`, canonical VAs incl. image base). Every named address (call targets, globals, RIP-relative loads/stores, float constants) resolved to the claimed value; every stated offset, bound, sign, stride, arg order and branch polarity matched.

## Per-row notes

Largest package in the wave; every row byte-exact. Highlights: 0026FEC0 key-lookup (byte2/word cx key, 0024F680, +0x130 chain); the three 0209C4C8-gated lazy registrations (002A1D40/1EB0/7E20 — same block layout, code lea at stated offsets, word 2/0/1 variant); 002D7840 dual lazy init on 0209AC30 fields; the 00267310/00267E10 predicate family (15 rows) with correct return polarities; 00345930/34AB50/350700 arg-pack decode (bits24-31 minus 4/0x10 bound, v&0xFFFFFF, p+0x28, stack float); 0035DAF0 dense dispatch (s=022C806C, t=record+8, all five sub-cases); 003DF360 8x7 table entry fill; 00474070 block build with self-pointer at +0x10; 00536140 unlink+decrement+callback+free; 0053EB30 lazy-init + 00244F00 dispatch.

## Limits

Body statements only, per the package README — the sentences describe instruction behaviour, not semantics. Cloud-drafted rows stand on FABLE's re-read; this review independently re-derived every row from the image.
