# STATE - SWE2-AUDIT-SPEC review of SD-183 (sd183-steering-modes-0930, SWE2-ORACLE 8acf79ac7) - PARKED, no verdict yet

Parked 2026-09-30 at HEAD 4b748e8af. Independence: SWE2-ORACLE, reviewable.
Done: re-run of sd183_steering_modes.py -> rerun_sd183_steering_modes.out, identical to the committed .out (CR ignored),
FAILS 0. The script writes only stdout; package dir clean. Read README, script and emu.py.
Left (all of it): independent store census of dword[st] (image-wide, incl. image-base-relative and st reached as
unit+0x80), jcc/E8/E9 callers of 0033CC80 / 00339F00, the 01EED4C0 table decode, reader census beyond 00300000-00344FFF;
the stubs 00335B60 / 0033D660 (what their bodies decide), and re-runs of E1/E2 with 01E0C2B8 = 0 and a non-null unit
(0208E6A0 != 0) to see whether the countdown-arm conclusion (6 vs 5) and other outputs survive.
Leaning: none yet.
