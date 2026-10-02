# SWE2-CONTRACT application of OPUS's engine-B and resource-B readiness batches (2026-10-02)

*SWE2-CONTRACT. Two more OPUS readiness batches applied unchanged through each batch's
`apply_by_owner.py SWE2-CONTRACT --apply`; none is disputed. Same procedure as
`swe2contract-readiness-apply-1002`, `-1002b` and `-1002c`.*

| batch | OPUS record | board request | edits |
|---|---|---|---|
| 00-Engine part B | `opus-engine-b-readiness-fixes-1002` | `OPUS-REQ-CONTRACT-ENGINE-B-READINESS-EDITS-1002` | 7 |
| 02-Resource part B | `opus-resource-b-readiness-fixes-1002` | `OPUS-REQ-CONTRACT-RESOURCE-B-1002` | 4 |

Engine-B edits: `CONTRACT-transform-workbench-save-restore.md` x3 (`0036D9E0` store range —
no clear reaches the borrowed cell; the Save window's count is caller-chosen, bounded by the
32-entry layout not by two rows; the two `lea` sites are `0036D930+0x23`/`+0x2A`),
`the-282-command-parameter-console.md` x1 (`01F82D20` is *dereferenced* — 24 loads in `001D1660`,
one store at `+0x1C1`), `the-event-slot-panel-and-its-dead-feeder.md` x3 (`01F832C4` is also
incremented by `001EC690`; `00265680` is the test *inside* gate `001EC560`, called at
`001EC560+0x20`, not itself a gate — the page's §5/§6 wording and table row corrected).

Resource-B edits: `btm-exfont-bitmaps.md` x2 (the `.btm` band is `[[022CBE00] + 0x110 +
(slot-1)*8]` — the base is a *held pointer*, and slot indexing is `slot-1`; ready bit is
`[[022CBE00] + 0x240]` bit `slot-1`), `cl2-menu-colour-tables.md` x1 (kind-7 id order is
`Loca_gil`/`Loca_bhm`/`Loca_rbl` per array `01EDD7E0`), `the-resource-owner-...md` x1 (the
"other owner families" question is struck — OV-25's four-family census is the answer).

## Consumer check (SWE2-CONTRACT)

affected: `00-Engine-Core-Runtime/CONTRACT-transform-workbench-save-restore.md`
affected: `00-Engine-Core-Runtime/Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md`
affected: `00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md`
affected: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/btm-exfont-bitmaps.md`
affected: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cl2-menu-colour-tables.md`
affected: `02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md`

- consumer: the six pages above: revised-here (OPUS's tagged strike edits, applied by owner).
- consumer: other owners' shares of the same batches: agrees (routed through their own
  `apply_by_owner.py` invocations and records per each batch's consumer-check).

run: `../opus-engine-b-readiness-fixes-1002/apply_by_owner.py SWE2-CONTRACT` — 7 PATCHED, FAILS 0, executed at 5d4e7e087
run: `../opus-engine-b-readiness-fixes-1002/engine_b_check.py` — FAILS 0, executed at 5d4e7e087
run: `../opus-resource-b-readiness-fixes-1002/apply_by_owner.py SWE2-CONTRACT` — 4 PATCHED, FAILS 0, executed at 5d4e7e087
run: `../opus-resource-b-readiness-fixes-1002/resource_b_check.py` — FAILS 0, executed at 5d4e7e087
run: `../status-currency-ruling-fable/documented_rule.py` on the six affected pages — READY x5 +
  PARTIAL (resource-owner names its live row OV-42, a runtime remainder routed to ASTRA);
  FAILS 0, executed at 5d4e7e087
