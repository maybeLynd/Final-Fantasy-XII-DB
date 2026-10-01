# STATE - SWE2-AUDIT-SPEC review of SD-190 (sd190-tween-turn-bit-0930, OPUS 8de16e58c) - PARKED, no verdict yet

Parked 2026-09-30 at HEAD 4b748e8af. Independence: OPUS, reviewable.
Done: re-run of sd190_tween.py -> rerun_sd190_tween.out, identical to the committed .out (CR ignored), FAILS 0 (T1-T6;
the commit message says T1-T5, the README and script carry T6). retool.py writes its cache in the ignored work tree;
package dir clean. Read README and script.
Left (all of it): read 003E6A70 / 003AEF50 / 003AED70 / 003AEF90 / 003E6340 / 003E65E0 in full; raw E8/E9 + jcc + stored
pointer callers of 003AED70 / 003AEF90 / 003E6A70; every writer of node byte +1 (other than 003AED70 / 003AEF90);
check that 003E6340 is command 0x1A on the cited page.
Leaning: none yet.
