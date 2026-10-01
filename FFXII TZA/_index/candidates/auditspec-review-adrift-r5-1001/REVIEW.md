# Audit-spec review: OPUS A-drift round 5

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `opus-adrift-round5-1001`
Board task: `OPUS-REQ-AUDITSPEC-ADRIFT-R5-1001`

## Verdict: ACCEPT

## What was checked

- **Guard comment at HEAD.** `round5_guard_comment.py "Database/FFXII TZA"` → `already` — the
  guard comment the round installed on `select_documented_global_leafs.py` is in place.
- **`check_family_forms.py --db` on the live tree:** `MATCH 96 families / 6938 bodies`,
  `MISMATCH 0` — exactly matching the retained `check_family_forms-after.txt` claim.
- **Pairing table cite-by-cite.** All 21 rows of `pairing-round5.tsv`: every interior cite is
  present on its citing page at HEAD — 18 literal cites (e.g. `00340000` on
  `capability-inhibition-policy.md`) and 3 prose-form cites whose embedded targets (`02B58C50`,
  `002E9660`, `003DCD00`) are on the named pages. 21/21.
- **Disposition drift is forward motion.** `check_dispositions.py` at HEAD reports A=9746
  (receipt: 9629) and families accepted 335 (receipt: 336). The +117 A and the −1 family are the
  expected consequences of pages re-statusing to evidence-bearing since 10-01, not regression:
  refused stays 0. The tool's output layout has grown (342→377 lines), so byte-diff against the
  receipt is not meaningful; headline semantics reproduce.
- **Practice change.** The record's own process fix — "each OPUS re-status publish now carries its
  own A-drift pairing, so F no longer dips between a re-status and its repair" — is the right
  structural response to the drift class EC7 documented.

## Narrowing / notes

None required.
