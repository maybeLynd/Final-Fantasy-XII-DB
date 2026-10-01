# STATE - parked SWE2-AUDIT-SPEC review of SD-193 (OPUS, 79ba50e5c), 2026-09-30 - NOT a verdict

Measured at HEAD 4b748e8af. Independence: OPUS, reviewable.

## Done
- Re-run: `rerun_sd193_turn.out` identical to the committed `.out` (CR ignored), FAILS 0. Package dir clean (git status empty).
- `rvimg.py` (own loader, sha asserted, unicorn harness), `dump.py`, `sd193_rederive.py` -> `sd193_rederive.out`.
- Unicorn execution of the ORIGINAL bytes of 003EC040 (injected record table at [022C6F28], rate record via +0x400/+0x12),
  003A1AD0, 003EC510, 003A1980: constant-rate step confirmed (X4, X9: 12 steps of 0.1 then 0.05 onto the target);
  modes 0/1 forced direction + snap, mode 2 / fast via 003A1AD0, modes 3 / -1 / no rate record -> target, 0 cases (X5),
  hold ids 0x0D/0x35/0x36 with 00422D50 stubbed (X8). 003EC510 (9003 points) and 003A1980 (2000) match the decode bit-for-bit.

## Findings so far (leaning ACCEPT-WITH-NARROWING)
1. Case table lacks a row: `+0x290 & 0x100000 == 0` and `word +6 != -1` (and +0x284 bit 0x8000000 clear) returns the
   TARGET at once in every mode (003EC10C..003EC115 -> 003EC124; executed X6). Turning only happens when bit 0x100000 is
   set or +6 == -1.
2. 01DFE0BC = 0.5 only on 001EDDC0's ecx != 0 arm (the 60-fps FrameLimit == 1 branch, CONTRACT-boot-fixups.md 13b);
   at the default it stays 1.0. "set to 0.5 by the boot fixups" / "half the record's rate after the boot fixup" overreach.
3. Modes 0/1 return `cur +- step` unwrapped (D2, X7: 3.1 + 0.1 -> 3.2 > pi) - not claimed otherwise, worth one line.

## Left
- The 3 FAILs in sd193_rederive.out are MY instrument's, not the package's: (a) W sweep's rip condition excludes
  next_ip == site+4 (`0 <` should be `0 <=`), so W1/W2 found 0 references - fix and re-run (control W2 must pass);
  (b) X1's one mismatch is my fixed sample (0.0, 0.1, 0.25) whose target was not float32-rounded in the reference.
- Then write REVIEW.md with the narrowing text.
