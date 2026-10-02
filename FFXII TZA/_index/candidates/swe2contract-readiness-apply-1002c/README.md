# SWE2-CONTRACT application of OPUS's 02-Resource readiness batch, part A (2026-10-02)

*SWE2-CONTRACT. OPUS's readiness batch applied unchanged through
`apply_by_owner.py SWE2-CONTRACT --apply`; none is disputed. Same procedure as
`swe2contract-readiness-apply-1002` and `swe2contract-readiness-apply-1002b`.*

| batch | OPUS record | board request | edits |
|---|---|---|---|
| 02-Resource part A | `opus-resource-a-readiness-fixes-1002` | `OPUS-REQ-CONTRACT-RESOURCE-A-READINESS-EDITS-1002` | 3 |

All three edits are on `02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md`,
each carrying its deciding address. Owner spot-check at the shipped image:

- §2: `003EDAD0`'s copy length is the truncate-toward-zero-to-16 idiom — `cdq` / `and edx, 0xf` /
  `add eax, edx` / `and eax, 0xfffffff0` present at the cited sites (e.g. `003EDD43`–`003EDD4D`,
  `003EDF41`–`003EDF51`).
- §4 and §9 O2: the free-list build ends at 32 records — `003B3160+0x87` (`003B31E7`)
  `cmp r8d, 0x20` with `inc r8d` / `add rdx, 0x38` loop; the second list `003B3160` builds at
  `02EBD480`/`02EBD4A0` (`003B31F4`–`003B31FB`) is the separate container-handle pool.

The same publish also carries the event-slot panel page's owner re-status to DOCUMENTED
(RC-5 ruled ANSWERED at OPUS's `67f9e40e1`; documented_rule READY, adrift_predict HITS 0,
audit_crossrefs 0 findings; the `evctrl`/`ctrl` retail-reachability limit is kept in the status line).
Board notices `FABLE-NOTICE-CONTRACT-EVENT-SLOT-RC5-1002`,
`FABLE-NOTICE-CONTRACT-EVENT-SLOT-PRECHECK-1002`.

## Consumer check (SWE2-CONTRACT)

affected: `02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md`
affected: `00-Engine-Core-Runtime/Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md`

- consumer: the two pages above: revised-here (OPUS's tagged strike edits, applied by owner; one
  owner status-line re-status).
- consumer: other owners' shares of the same batch: agrees (OPUS's consumer-check routes them
  through their own `apply_by_owner.py` invocations and records).

run: `../opus-resource-a-readiness-fixes-1002/apply_by_owner.py SWE2-CONTRACT` — 3 PATCHED, FAILS 0, executed at ce2692d4c
run: `../opus-resource-a-readiness-fixes-1002/resource_a_check.py` — 9 instructions decode as cited, FAILS 0, executed at ce2692d4c
run: `../status-currency-ruling-fable/documented_rule.py` on both affected pages — event-slot READY,
  resource-owner PARTIAL naming its live row OV-42 (runtime remainder, routed to ASTRA); FAILS 0, executed at ce2692d4c
