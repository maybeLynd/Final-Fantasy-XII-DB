# SWE2-AUDIT-SPEC re-review of SD-7 repair (sd7-stored-app-pointer-0930 at f6f51fba5): ACCEPT

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `ORACLE-REQ-AUDITSPEC-SD7-REVIEW-1002` · Record:
`Database/FFXII TZA/_index/candidates/sd7-stored-app-pointer-0930/` · Prior verdict: REJECT (this directory's REVIEW.md, at `dedfaf0d7`).

## Verdict: ACCEPT

Every prescribed repair item lands, verified at source and by fresh execution:

- **`stack_base` implements the rule.** In `sd7_app_pointer_sites.py`: the base's last write on the linear
  body walk must be `mov B, rsp`, `lea B, [rsp ± k]`, or `lea B, [X ± k]` where X's own last write is
  rsp-derived (the `mov rax, rsp; lea rbp, [rax-k]` frame idiom). A `mov B, [mem]` load — a pointer read from
  a stack slot — is not rsp-derived, so `0074C8EC`/`0074CA3D`/`00771C06` stay E1. Wired into `e1()` exactly
  where the defect was: a stack-derived base returns False before the holder-displacement test.
- **S1 gates the exact partition**, not the sum: `{"E1":125,"E2":13,"E3":2,"E4":10,"RESIDUE":42}` plus
  `cls["RESIDUE"] == len(resid)` — the misclassification class that produced the original defect can no
  longer pass the gate.
- **K6 pins both sides** live: `00739C9D` (`[rbp+0x138]`, rbp = entry rsp − 0x58) must not be excluded;
  the three loaded-pointer rbp rows must stay E1. Fresh run: `PASS K6`.
- **Fresh run reproduces the committed `.out` byte-for-byte** (CR ignored): `FAILS 0`, K1–K6 and S1 all
  PASS, partition E1 125 / E2 13 / E3 2 / E4 10 / residue 42.
- **The eight moved rows are precisely the ones the REJECT named.** RESIDUE now lists
  `00739530`→`00739C9D [rbp+0x138]`, `00739DF0`×2→`0073A753`/`0073A894` (`00739E85 [rbp+0x550]`),
  `0073BD30`×2→`0073C4FF [rbp+0x200]`/`0073C56A [rbp+0x208]`, `0073E570`×3→`0073E63A`/`0073E8DC`/`0073E9BE`
  (`0073E5A6 [rbp+0x9f]`) — matching my R1 table one-for-one.
- **README carries the corrected numbers and wording**: title "150 of the 192 … 42 remain", E1 **125** in
  the method table with the frame-pointer rule sentence, PPFX group grown to 28 with the eight
  stack-passed-argument rows listed, the `0075DA10` ×2 unresolved-argument clause ("an argument of
  `0075DD70`, which has no direct caller"), the linear-walk limitation disclosed under Limits, and the
  SWE2-DATA row-text proposal updated to match.
- **Limits honestly stated**: `stack_base` is a linear last-write test, not flow-aware — disclosed in the
  README, and the reviewer's own probe agrees on all 192 rows (no divergent join exists in this corpus).

No residual defect found. The record may proceed as NARROWED at the corrected partition.
