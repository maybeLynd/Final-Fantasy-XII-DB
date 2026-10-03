# SWE2-AUDIT-SPEC review — fable-the-bazaar-recipe-unlock-and-purchase-homing-1003

**Target.** `_index/candidates/fable-the-bazaar-recipe-unlock-and-purchase-homing-1003/` (task `FABLE-REQ-AUDITSPEC-FABLE-THE-BAZAAR-RECIPE-UNLOCK-AND-PURCHASE`)
**Verdict.** ACCEPT

## What was checked

- **Mechanical checker.** `fable-the-bazaar-recipe-unlock-and-purchase-homing-1003/interior_applier.py` re-run verbatim in place: `FAILS 0`, matching the committed `interior_applier.out`.
- **Semantic pass.** All 1 rows / 5 anchors verified instruction-by-instruction against the certified shipping image (SHA256 `73461D08...D89721F8`, canonical VAs incl. image base). Every named address (call targets, globals, RIP-relative loads/stores, float constants) resolved to the claimed value; every stated offset, bound, sign, stride, arg order and branch polarity matched.

## Per-row notes

003FEE40 dense dispatch verified in full: [rdx]-1 case1 / 0x12 ret 0 / others tail 005C5230; s=movsxd rdx+8, G=0209AC30, Pn=null-guarded rcx+0x60 slots; calls +0x51/+0x93/+0xCE resolve (002432B0, 00247570 w/ 00D12050, 0027F1A0 w/ word G+s*0x20+0xd48); 0x4a9a-0x4a9e selector chain exact; P30 vtable+0x18 store, 0020E620(0) at +0x20, 0029FB50(P30); L+8==0xffff -> clear bit0 of P20+8 and P28+8; else byte[qword P20+0x20 + b*8 + 7]->P20+0x39, b=byte L+0xa->word P20+0xa, L->P28+0x18, 0020E620(0)->P28+0x20; returns 0 on all arms.

## Limits

Body statements only, per the package README — the sentences describe instruction behaviour, not semantics. Cloud-drafted rows stand on FABLE's re-read; this review independently re-derived every row from the image.
