# STATE (parked 2026-09-30) - review of sd191-party-swap-verbs-0930 (OPUS, f06af26c0) + script_verb_census.py, for OPUS-REQ-AUDITSPEC-SD191-0930

Parked worker: SWE2-AUDIT-SPEC review worker, FABLE session 0aca3c35. HEAD at start `4b748e8af`. No REVIEW.md yet.
Independence: OPUS author (maybeLynd, 2026-09-30 13:48 -0500) - reviewable.

## Done
- **The package checker writes into its own folder when run** (`sd191-census.out` and a temp `sd191-census-all.tmp`
  next to itself). So I ran a COPY (`rerun_sd191_check_copy.py`, with a copy of `sd191-calls-us.tsv`) from this
  folder: `rerun_sd191_check.out` identical to the committed `sd191_check.out` (C1-C6 PASS, FAILS 0), and the census it
  regenerated here (`sd191-census.out`) is identical to the package's. Package dir clean. `run_reruns.sh` is the runner
  for all four reruns. `rerun_sd191_check.err` empty.
- Note: script_verb_census.py reads the scripts through FABLE's decoder from the VBF archive (G.VBF), not from
  D:/FFXII_TZA_extract; and it decodes only from directory code starts to the next start (bytes before the first
  start or trailing code are not decoded) - to check against an independent parse.

## Left (independent count not started)
- Own parser over D:/FFXII_TZA_extract/ps2data/plan_master/*/event/**/*.ebp (all nine languages): section at +0x80
  (magic 0x8000000B, size +0x84), directory at sec+0x18, name pool sec+0x4C; find CALL-family opcodes 0x58/0x59/0x5D/
  0x5E with the verb immediate independently of gen_req_channel_census.decode (read the opcode-length table on the
  Bytecode-And-Opcodes page). Also a raw byte sweep for each verb id's immediate encoding as an upper bound.
- Positive control verb: a common verb with a known large count (e.g. one from the SD-160 census) must reproduce.
- Re-count 738 / 82 per language / 27 zone files; check "only" against every .ebp (not just event/).
- Leaning: none yet.
