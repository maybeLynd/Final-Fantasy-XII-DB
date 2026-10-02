# OV-25 record corrected with ASTRA's name-binding and stale-lane results - consumer check (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148). The corrections themselves are struck and restated in place in
[FABLE's OV-25 record](../ov25-queue-clients-fable/README.md) (family S and two "not claimed" obligations). This record is
their consumer check.*

affected: `Database/FFXII TZA/_index/candidates/ov25-queue-clients-fable/README.md`

- consumer: FABLE's OV-25 record, family S: revised-here (bit 2 is conditional; the removal 002EAEB0 is a mark-only delete under two flags; the cleanup drain releases the record).
- consumer: the same record's stale-lane obligation: revised-here (an already-requested lane's stale completion returns before any write or call).
- consumer: the OV-25 register cell: agrees (it does not carry family S's deletion policy or the stale-lane question; ANSWERED unchanged).
- consumer: OPUS's per-frame update gate contract: agrees (OPUS consumed both packets there, ff1ce806f and 8db70f9f2).
- regression: run: [`ov25_astra_check.py`](../ov25-queue-clients-fable/ov25_astra_check.py) at 5b8ffef20 (FAILS 0).
