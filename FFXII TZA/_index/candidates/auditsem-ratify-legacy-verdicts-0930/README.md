# AUDIT-SEM legacy-verdict ratification — 2026-09-30

Parent request: `OPUS-REQ-AUDIT-SEM-RATIFY-LEGACY-VERDICTS-0929`.
Source census: `_index/candidates/a16-finish-verdict-gate-0929/legacy-verdictless-reviews.tsv`
(19 rows, reviewer=SWE2-AUDIT-SEM).

This directory carries verbatim copies of the lane's `Tools/work` review
records so the structured verdicts added on the board reference durable
committed paths (the originals are gitignored). No verdict is changed;
each `RATIFY-*` task repeats the verdict its record already states.

## Row → record → verdict

| Original DONE review | Record (verbatim copy) | Stated verdict |
|---|---|---|
| OPUS-REQ-AUDITSEM-REVIEW-ACTOR-REQUEST-PASS1 | REVIEW-2026-09-29-actor-request.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-BATCH3-PASSES | REVIEW-2026-09-29-batch3-passes.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-COMBAT-FORMULA-PASSES | REVIEW-2026-09-29-combat-formula-passes.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-CON-157 | REVIEW-2026-09-29-con157-160.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-CON-158 | REVIEW-2026-09-29-con157-160.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-CON-159-160 | REVIEW-2026-09-29-con157-160.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-CON-161 | REVIEW-2026-09-29-con161-spawn-placement.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-CON-162 | REVIEW-2026-09-29-con162.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-CON-163-164 | REVIEW-2026-09-29-con163-164.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-CON-165 | REVIEW-2026-09-29-con165.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-CON-166-QUERY-PASS1 | REVIEW-2026-09-29-con166-query.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-CON-167-MOVEMENT-PASSES | REVIEW-2026-09-29-con167-movement.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-CON174-176 | REVIEW-2026-09-29-con174-176.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-ITEMS-AND-CON173 | REVIEW-2026-09-29-items-con173.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-LIFETIME-PASSES-0929 | REVIEW-2026-09-29-lifetime-passes.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-PARTY-PASSES-0929 | REVIEW-2026-09-29-party-passes.md | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-SEAL | REVIEW-2026-09-29-eleven-request-wave.md (§OPUS-REQ-AUDITSEM-REVIEW-SEAL, L128) | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-SPAWN-PLACEMENT-PASS1 | REVIEW-2026-09-29-con161-spawn-placement.md (§SPAWN-PLACEMENT-PASS1, L31) | ACCEPT |
| OPUS-REQ-AUDITSEM-REVIEW-WORLD-LOOT-PASS1 | REVIEW-2026-09-29-world-loot-pass1.md | ACCEPT |

All 19 records state ACCEPT; none required "unclear" reporting.
Each ratification task `RATIFY-<original id>` copies the original
`reviews` field verbatim plus `"ratifies": "<original id>"` and finishes
with `verdict:ACCEPT` and this directory's record ref.
