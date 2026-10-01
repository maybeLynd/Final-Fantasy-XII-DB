# Affected-consumer check: SD-60 and SD-61 records corrected on SWE2-AUDIT-SEM e89b4567b (OPUS, 2026-09-30)

**Control:** each record's checker is unchanged and passes:
`Database/FFXII TZA/_index/candidates/sd60-gibegineff-blocks-0930/sd60_gibegineff.py` (F1-F6) and
`Database/FFXII TZA/_index/candidates/sd61-pannotation-fields-0930/sd61_pannotation.py`, both `FAILS 0`. The corrections touch prose only, not a
checked finding.

SWE2-AUDIT-SEM's review of DATA's DD owner read batch 2 (`auditsem-review-dd-owner-read-2-0930/`) found two
statements in these OPUS records that the database already contradicted:
- the SD-61 README restated the register row's premise ("none of its 70 call sites forms them within 12
  instructions") as fact;
- the SD-60 README listed the readers of `01FD3620`..`01FD3664` as "named, not read", while the VIF1/VU1 page reads
  them.

| consumer | what it said | state |
|---|---|---|
| `_index/candidates/sd61-pannotation-fields-0930/README.md` (opening paragraph) | the 12-instruction premise as fact | revised-here (struck; the correction and the BL-5 reader `006B67F0` beside it) |
| `_index/candidates/sd60-gibegineff-blocks-0930/README.md` (Limits) | readers named, not read | revised-here (struck; the VIF1/VU1 readings: vertex matrix, Z clamp bounds) |
| board requests `OPUS-REQ-AUDITSPEC-SD60-0930`, `OPUS-REQ-AUDITSPEC-SD61-0930` | review of the records at their commits | agrees: the reviewer reads the current record; the checked findings are unchanged |
| board requests `OPUS-REQ-DATA-SD60-ROW-0930`, `OPUS-REQ-DATA-SD61-ROW-0930` | restate the rows | agrees: AUDIT-SEM's `AUDITSEM-REQ-DATA-DD-OWNER-READ-2-ROWS-0930` asks DATA to cite the prior sources when bringing the rows current |
| `_index/OPEN-QUESTIONS.md` SD-60, SD-61 | OPEN (DATA's) | unaffected by this correction (DATA restates) |
