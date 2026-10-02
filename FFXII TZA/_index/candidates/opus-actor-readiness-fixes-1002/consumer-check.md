# Consumer check: 04-Actor contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-04-VALUES-1002. Cloud wave 3 mapped `04-Actor-Entity/` from a text snapshot (session
`session_01CyCFGXs9kPwVXaq5BmAkb1`; report `cloud-reports/re-readiness/04-actor.md` in maybeLynd/Final-Fantasy-XII-DB,
68343d98; rated NOT YET). Its 52 value items and its count items were page-text only. OPUS decided 15 of them at the
shipping image, and a local read-only pass decided the rest (`actor_check.py`). In 50 of the 52 the bytes refute one
side; C-V40 and C-V49 hold no conflict.

Some findings overturn dated text:
- The region map gives `0xA0` when the sub flag is 1. The 2026-09-16 text has the select reversed.
- The initialiser itself fills the `+0xC8` override array with `0xFFFF`.
- Side A really does test the index twice, so the dated 2026-09-12 "one unsigned compare" re-read is wrong.
- The slot stride is `0x288`, not `0x200`.
- The `0x860` presentation array is two elements at `02097D20`.
- The table base is `02ADD980`, and the global is `02EBF1A0`.

The pass drafted 182 strike edits (`apply_04actor.py`). OPUS applies the 102 on its own lines across 11 pages
(`apply_by_owner.py OPUS`). The rest are held or routed:
- 11 edits on OPUS's battle-unit field map are held, because SWE2-AUDIT-SPEC is auditing a record that names it
  (OPUS-REQ-AUDITSPEC-RECORD-EIGHT-PASS6-SIGNATURES-1001). OPUS applies them later with `apply_by_owner.py OPUS-HELD`.
- 33 go to SWE2-FRONTIER: 29 on the overlay carriers plus 4 of its own lines.
- 23 go to SWE2-EC7.
- 11 go to FABLE.
- 2 go to SWE2-STRUCT.

- **Affected:** 04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md, 04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md, 04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md, 04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md, 04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md, 04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md, 04-Actor-Entity/CONTRACT-field-runtime-pass.md, 04-Actor-Entity/CONTRACT-manager-slot-entry-tables.md, 04-Actor-Entity/README.md, 04-Actor-Entity/battleunit-slot-pool-and-actor-class.md, 04-Actor-Entity/the-definition-record-flag-pair.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the eleven OPUS-led and shared 04 pages (OPUS lines) | revised-here |
  | `Battle-Unit/the-battle-unit-field-map.md` (OPUS-led, under SPEC audit) | routed-to-OPUS (held; `apply_by_owner.py OPUS-HELD`, 11 edits, after the SPEC request closes) |
  | the field-runtime-pass page and the two battle-unit construction pages (overlay carriers), and FRONTIER's lines | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py SWE2-FRONTIER` and `FRONTIER`, 33 edits) |
  | the manager field map, the names page and the display record | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 23 edits) |
  | the storage-initialisation contract and FABLE's lines | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 11 edits) |
  | STRUCT's two census-page lines | routed-to-SWE2-STRUCT (request with `apply_by_owner.py SWE2-STRUCT`, 2 edits) |
  | RE repo `docs/readiness/04-actor.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-actor-readiness-fixes-1002/actor_check.py, verified at aac0489ac: 24 instructions decode as cited, FAILS 0 ([`actor_check.out`](actor_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (102), FAILS 0.
