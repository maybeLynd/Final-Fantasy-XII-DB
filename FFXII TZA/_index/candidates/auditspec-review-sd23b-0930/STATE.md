# STATE (parked 2026-09-30) - review of sd23-state7-dynamicsound-0930 (OPUS, 9af526c00) for OPUS-REQ-AUDITSPEC-SD23B-0930

Parked worker: SWE2-AUDIT-SPEC review worker, FABLE session 0aca3c35. HEAD at start `4b748e8af`. No REVIEW.md yet.
Independence: OPUS author (maybeLynd, 2026-09-30 14:22 -0500) - reviewable. The earlier SD-23 review
(`../auditspec-review-sd23-0930/`, acb04148d, ACCEPT) was read; it does not cover state 7 or 007F0820.

## Done
- Re-run: `rerun_sd23b_check.out` identical to the committed `.out` (CR ignored), S1-S3 + D1 PASS, FAILS 0. Package
  dir clean after re-run. (`rerun_sd23b_check.err` is empty.)

## Left (no independent re-derivation done yet)
- S3's state-7 census is a regex over retool's function list in 007A0000..00800000 (`[r?? + 0x54], 7` only). Re-do
  independently: raw sweep of all .text for `C7 4x 54 07 00 00 00` / `C7 8x 54 00 00 00 07..` (mov dword [reg+0x54],7,
  disp8 and disp32), plus `cmp dword [reg+0x54], 7` / `cmp reg, 7` after a +0x54 load, image-wide; check state-7
  writes by register (mov [reg+0x54], eax where eax may be 7) - list +0x54 dword writes in the audio range with
  non-constant sources. Control: the known 007BF18D / 007BD13F / 007BD16D must be found.
- S2 polarity: read 007BF16A..007BF18D (states 2..4 skip, count +0x4C == 0, state 6 -> 7 direct, else slot 39 call;
  check the test/jcc after `call [rax+0x138]` is `test al,al; je` skip).
- D1: RTTI walk of the vtable holding 007F1670 (independent COL read); callers of 007F0820 (E8/E9, jcc, data/DIR64).
- Leaning: none yet.
