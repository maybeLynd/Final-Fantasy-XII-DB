# STATE - parked SWE2-AUDIT-SPEC review of the SD-184 pair, 2026-09-30 - NOT a verdict

Measured at HEAD 4b748e8af. Independence: OPUS 50890aa7f and SWE2-ORACLE 8acf79ac7 (13:44 -05:00), both reviewable.

## Done
- OPUS `sd184_range.py`: `rerun_sd184_range.out` identical, FAILS 0.
- ORACLE `sd184_facing_sources.py`: `rerun_sd184_facing_sources.out` identical, FAILS 0 (57 s).
- ORACLE census: run as a COPY (`copy_sd184_setposparty_census.py`) because the original writes its TSV into its own
  folder; `rerun_sd184_setposparty_census.out` and `sd184-setposparty-sites.tsv` identical to the committed ones.
- Both package dirs clean after re-runs (git status empty). ORACLE's img.py does not assert the image sha (note it).

## Observations so far (not yet re-derived)
- The two records agree: OPUS's "|x| > 4pi" is a necessary condition; ORACLE's executed sweep tightens it to the odd bands
  (5pi, 6pi), (7pi, 8pi) ... Consistent arithmetic (fast path returns x mod 2pi in [0, 2pi) for x > 0).
- OPUS S2 cites one writer (002E5E10, movementState +0xA8); ORACLE S9 says 00265200 reads +0xA8 (kind 3) OR +0x38
  (kind 1), writers 002E5E10 and 0026B6A0 - OPUS's S2 may omit the kind-1 branch. Check 00265200.
- SD-193 review (same worker): 003EC040 modes 0/1 return cur +- step UNWRAPPED (executed 3.1 + 0.1 -> 3.2). If that
  result reaches a heading store, it is a writer outside [-pi, pi] neither record lists - check where 003EC040's result
  goes (callers 002E59ED, 00358E61).

## Left
- Own unicorn sweep of 0033CB70 (re-use ../auditspec-review-sd193-0930/rvimg.py), 00334120 early path.
- The +0x160 store census OUTSIDE 002F0000-0033FFFF (image-wide, rip/base-reg displacement 0x160 on BattleUnit bases):
  the assignment's main falsification test. Also jcc callers of 00310920 / 0037D000 / 003003F0.
- Sample-check the census TSV (a few constant facings, the evt_t0505 accumulator).
- Then REVIEW.md with two per-request sections.
