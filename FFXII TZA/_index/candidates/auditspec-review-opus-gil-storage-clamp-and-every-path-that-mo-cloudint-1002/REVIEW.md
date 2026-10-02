# Audit-spec review: OPUS cloudint interior citations (opus-gil-storage-clamp-and-every-path-that-mo-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-GIL-STORAGE-CLAMP-AND-EVERY-PATH-THAT-MO-CL` · Package: `_index/candidates/opus-gil-storage-clamp-and-every-path-that-mo-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 20 rows applied, 82 anchors, rejected/skipped/missing 0.
- Semantic pass: all 20 rows exact vs the certified image, incl. 0020CB50 (seven 12-byte entries 00906294..E8, signed index, +0x190/+0x194 writes, i==6 fan-out to records 0x3168..0x3C90, dual vtable +0x38/+0x50 calls when rcx+0x18!=0), 002494A0 (lazy 0208F578->02090910 init + 0x780 clear + unconditional 0x180 clear of 02090790), 0024A660 (tail 00861EC0(0208F580,0,0x1208)), 00272470 (zero +0/+0x10, ecx+edx at +0x18, 0x10-roundup at +0x20), 00274840 (002446E0->002473B0->002482E0), 002800F0 (lazy init + 0xE00 clear), 00290430 (+0xAA44 store), 00290DF0 (tail 00273B40 with qword+0x10FC0 of 0209BE80), 002BE490 (dword[rdx]==2 gate, 001EDEC0->002BF4F0 zero-word path, 002BE290(rcx+0xAC0), ret 0; else tail 005C5230), 00300500 (cmovns clamp, returns clamped value not call result), 0034C9A0 (00267E10 pop, 00863240(0032F240(dword+0x28 of 002640C0()),a), tail 0026B750), 0035C560 (00861EC0(022C8060,0,0x23C8) + or 0x20 + 0028F8B0+00253480+00290430(1) + 003C5E40 store to 022C83B8), 00365DD0 (004745D0(0xA00), 0x40 x 0x28 linked records, +0x220/+0x228/+0x230 stores incl. p+0x9D8 last record, first-prev/last-next zeroed), 0039BB30 (00861EC0(02AEE810,0,0xF0) + tail 0039C3F0), 003F30A0 (+0x70 chain walk, next read before callback, rdx-gated indirect call), 003F4BD0 (stack block byte0/qword rdx/dword ecx + record dword0/&blk/qword0 + 00244F50(0x100,003F4E70,&rec) + 00808C40 cookie), 003FA760 (00275550(rcx,0x26C0) + word+0x249A=0xFFFF), 00863240 (0020CE00 non-null -> 0020CB50(0020CE00(),ecx,edx) else no second call).
- Limits hold: body statements only.
