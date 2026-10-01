# STATE (parked 2026-09-30) - review of sd181-sp1-loader-0930 (OPUS, 2e1bb015e) for OPUS-REQ-AUDITSPEC-SD181-0930

Parked worker: SWE2-AUDIT-SPEC review worker, FABLE session 0aca3c35. HEAD at start `4b748e8af`. No REVIEW.md yet.
Independence: OPUS author (maybeLynd, 2026-09-30 14:05 -0500) - reviewable.

## Done
- Re-run: `rerun_sd181_check.out` identical to the committed `.out` (CR ignored), L1-L5 PASS, FAILS 0. Package dir
  clean after re-run. (`rerun_sd181_check.err` is empty.)
- Read on the bytes (capstone, via ../auditspec-review-sd180-181-0930/sdx_indep.py): 003780B1 `lea rax,[rip+0xb08]`
  (-> 00378BC0); 00378BDD..00378BF3 = 0036B970(rcx & ~3, rsp+0x20, 0x20); 00378E95 `mov rcx,[rsp+0xa0]` /
  00378E9D `mov [rip+..],rcx` stored unconditionally, bit 7 marked only when non-null (00378EA4..00378EB2);
  00378C40/00378C48 slots[24+i] -> `[r9+r11+0x29bd010]` with r11 = 0x120000 (00378C06); 003775D0: `test al,al; jns`
  (bit 7 of 02ADD0F0) then `mov rcx,[02ADD060]; call 003635C0`. All consistent with L1-L4.

## Left (nothing written yet for these)
- 02ADD060 census, independent: `X.rip_refs(0x02ADD060, 0x02ADD068)`, `X.imagebase_refs(...)` (disp 0x29BD060 with any
  base, incl. the r11 = 0x120000 form), a WINDOW image-base sweep 02ADD000..02ADD100 for indexed accesses
  ([r9+r11+0x29bd0xx] loops whose index can reach +0x60), `X.data_refs` + `X.reloc_in` (stored pointers), and lea of
  nearby bases. Controls: 02ADD058 (page names 4 rip refs: 00378F04, 003782EB, 003782FC, 00377B90) and 02ADD010+.
- Check L3's rsp is stable between 00378BF3 and 00378E95 (no push / rsp change) and no other write to [rsp+0xa0].
- Callers of 00378BC0: rel32 / jcc / data / DIR64 (L1 says lea is the only reference).
- Leaning: ACCEPT if the census matches L5 (writers 00378BC0 + teardown 00378230, reader 003775D0).
