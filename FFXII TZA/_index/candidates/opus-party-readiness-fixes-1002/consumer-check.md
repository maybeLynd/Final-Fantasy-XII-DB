# Consumer check: 11-Party contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-11-VALUES-1002. Cloud wave 3 mapped `11-Party/` from a text snapshot (session
`session_01FJpNGAfhZw9eGS9RVWrAn5`; report `cloud-reports/re-readiness/11-party.md` in maybeLynd/Final-Fantasy-XII-DB,
68343d98; rated NOT YET). Its 27 value-changing contradictions were page-text only. A local read-only pass decided all
of them at the shipping image or the shipped data, and OPUS re-checked a sample (`party_check.py`).

Two of them go against the side the map favoured:
- C-V17: the bit is read negated.
- C-V19: the board loop runs only when the leader word is not `0xFFFF`. The three-to-one majority on the pages is
  wrong.

Two more refutations fall outside the map's list:
- `0023B040` ends at `0023B1FF`. The `0036FFE0` calls belong to `0023B200`.
- The descriptors are not inside the battle-state block.

The pass drafted 109 strike edits (`apply_11party.py`). OPUS applies 57 of them, on six pages
(`apply_by_owner.py OPUS`). The other 52 are held or routed:
- 12 on OPUS's roster page are held, because SWE2-AUDIT-SPEC is auditing a record that names that page
  (OPUS-REQ-AUDITSPEC-RECORD-EIGHT-PASS6-SIGNATURES-1001). OPUS applies them after that request closes
  (`apply_by_owner.py OPUS-HELD`).
- 20 go to FABLE.
- 13 go to SWE2-EC7.
- 2 go to SWE2-FRONTIER.
- 5 go to SWE2-DATA. These are rows of the generated roster census, so the fix is a regeneration, not a hand edit.

- **Affected:** 11-Party/Battle-State-Block/the-battle-state-block-field-map.md, 11-Party/CONTRACT-party-slot-assignment.md, 11-Party/README.md, 11-Party/active-party-reserve-and-the-moment-the-leader-changes.md, 11-Party/the-five-parallel-slot-maps.md, 11-Party/the-setsavedata-presets-test-battle-scenarios.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the six OPUS-led and shared 11 pages (OPUS lines) | revised-here |
  | `party-roster-and-control-suppression.md` (OPUS-led, under SPEC audit) | routed-to-OPUS (held; `apply_by_owner.py OPUS-HELD`, 12 edits, after the SPEC request closes) |
  | the five-maps contract, the battle-state contract and FABLE's lines | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 20 edits) |
  | the party-focus contract and EC7's lines | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 13 edits) |
  | FRONTIER's subtree lines on the roster page | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py SWE2-FRONTIER`, 2 edits) |
  | the generated census `party-roster-slots-accesses.tsv` (four `0209A210` stores counted as roster writes) | routed-to-SWE2-DATA (regenerate the census; the drafted row notes are in `apply_by_owner.py SWE2-DATA`) |
  | RE repo `docs/readiness/11-party.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-party-readiness-fixes-1002/party_check.py, verified at 3e0fc5be9: 15 instructions decode as cited, FAILS 0 ([`party_check.out`](party_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (57), FAILS 0.
