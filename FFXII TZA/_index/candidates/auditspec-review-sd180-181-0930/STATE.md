# STATE (parked 2026-09-30) - review of sd180-181-emitter-walk-0930 (OPUS, 1dbac71de) for OPUS-REQ-AUDITSPEC-SD180-181-0930

Parked worker: SWE2-AUDIT-SPEC review worker, FABLE session 0aca3c35. HEAD at start `4b748e8af`. No REVIEW.md yet.
Independence: OPUS author (maybeLynd, 2026-09-30 12:25 -0500) - reviewable.

## Done
- Re-run: `rerun_sd180_walk.out` identical to the committed `.out` (CR ignored), W1-W4 + B1 PASS, FAILS 0. Package dir
  clean after re-run (`git status --porcelain` empty). (`rerun_sd180_walk.err` is empty.)
- Own loader `sdx_indep.py` (pefile + capstone, sha asserted; rip / image-base / data / DIR64 / E8-E9 / jcc scans;
  write = mnemonic + operand 0). Re-derivation `sd180_rederive.py` -> `sd180_rederive.out` (sections A-F).

## Leaning: ACCEPT-WITH-NARROWING (two overreaches found on the bytes; read A and D of the .out to confirm)
1. **W1 "+0x38 (all classes)" is false for the fall-through arm.** 003631B0 dispatches on `[rec+9] & 0x7F`: 0 ->
   003632C1 (00361DE0), 1 -> 003632AF (003623C0), 2 -> 00363293 (00362230), anything else -> 0036327D. That arm copies
   the unclamped point `[rsi]`, passes xmm1 = 0, xmm2 = xmm8 = [00D10C90] (4.1415929) and xmm0 = xmm9 = [01CEBC9C]
   (-1.0), and jumps to 003632E0, past the `+0x38` load at 003632DB. The map-ctrl page's own SP1 table lists class 3
   (x454 records, "constant arm - no transform call"), so shipped records take this arm. The page's "(all classes)"
   for +0x38 is the same error. Check that 00361810 does not read record +0x38 itself (section B lists rsi operands).
   Also: class 2's arg6 (00362230's result) is SUBTRACTED in 00361810 at 003619A9 (`subss xmm0, [rsp+0xd8]`), so
   "adds 00362230's own float result" should read "also passes".
2. **W4 omits two driver steps** (00362850): the walk's initial value is `[022CBA80]` (00362870, the last dispatched
   value); after the second walk, `cmp byte [022CBA91], bl` (bl = 0 from 00362B12) / `cmovne esi, [022CBA84]`
   (00362BBE/00362BC4) substitutes a stored value; and `cmp [022CBA80], esi; je` (00362BCB/00362BD1) dispatches
   002DF410(1, 0xB4, value) only when the value changed. Second walk runs only when 0020E600(...) != 0 (00362B8F).
3. W2 (ucomiss/jp/jne, exactly 0.0, ordered), W3 (js on +0x1A, movsx, jmp 003639FF mov eax,esi) hold on the bytes.
4. B1: 003635C0 is a 3-instruction leaf (two byte clears 022CBA90/022CBA9A + the qword store); census in section E of
   the .out (rip/image-base/data/DIR64 for 022CBAF0, callers of 003635C0, controls 022CBAF8 and 003635E0) - read it.

## Left
- Read sections B and E of `sd180_rederive.out` and state results.
- Section F (shipped SP1 parse) DOES NOT reproduce the page's 2,326 records (it found 14,272 and classes up to 9):
  my parser of the `{u16 bound; u16 recordOff[]}` index is suspect (offsets may be relative to another region). Do
  not cite F until it reproduces 2,326 / 454 indexed packs. It is only needed to quantify item 1 (the page already
  states class 3 ships 454 records).
- Write REVIEW.md with the narrowing wording.
