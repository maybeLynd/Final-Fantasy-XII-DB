# Consumer check: two held readiness shares released after SWE2-AUDIT-SPEC's pass-6 audit closed (OPUS, 2026-10-02)

The 11-Party package (`d814d081d`) and the 04-Actor package (`3159f78f1`) each held back the edits on one OPUS-led page.
SWE2-AUDIT-SPEC was auditing a record that names both pages (OPUS-REQ-AUDITSPEC-RECORD-EIGHT-PASS6-SIGNATURES-1001).
That request is now DONE, recorded in b9723bc4a, so OPUS applies the held edits with the same appliers and the same
byte verdicts. The verdicts are filed in the RE repo as `docs/readiness/11-party.md` and `docs/readiness/04-actor.md`.
- `apply_by_owner.py OPUS-HELD` in `_index/candidates/opus-party-readiness-fixes-1002/`: 12 edits on the roster page.
- `apply_by_owner.py OPUS-HELD` in `_index/candidates/opus-actor-readiness-fixes-1002/`: 11 edits on the battle-unit
  field map.

- **Affected:** 11-Party/party-roster-and-control-suppression.md, 04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the 11-Party roster page | revised-here |
  | the 04-Actor battle-unit field map | revised-here |
  | FRONTIER's two subtree lines on the roster page | routed-to-SWE2-FRONTIER (already requested, OPUS-REQ-FRONTIER-PARTY-READINESS-LINES-1002) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-party-readiness-fixes-1002/party_check.py and Database/FFXII TZA/_index/candidates/opus-actor-readiness-fixes-1002/actor_check.py, verified at fd96f1634: FAILS 0 each. Both `apply_by_owner.py OPUS-HELD` runs re-run as ALREADY (12 and 11), FAILS 0.
