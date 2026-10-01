# DD owner re-status, batch 22: the shop-table page to DOCUMENTED (OPUS, 2026-10-01)

The register rows the shop-table page names are all answered:
- UQ-132, UQ-133 and FG-1;
- GR-13, GR-14 and GR-15, answered by OPUS in `9c71391a8`, with FABLE's page corrections in `shop-page-corrections-fable-0930`.

`documented_rule.py` gives READY: no open box, no live id, no disposed row, no unknown id
([`documented_rule.out`](documented_rule.out)).

**Owner read (OPUS).** Section 7's eight boxes are ticked and each carries its answer.
- **"What consumes price bit 31".** The box still says "partly read", but both halves are now answered. Layout-A rows have
  the bit cleared by the transaction driver (`0056D468`). There is no layout B (GR-13). In sale mode, `0056E700` reads the
  bit as "cannot be sold".
- **The 2026-09-20 quote block's "what stays open ... GR-14".** It already carries the GR-14 answer, "no", as a dated note.
- **Prose limits.** The page names no other open item.

**Applied (OPUS).** The status line moves PARTIAL -> DOCUMENTED. The new line keeps the old line's answer list
([`restatus22.py`](restatus22.py), idempotent).

**A-drift.** `pair_adrift.py` found no exact-cited member to remove ([`pairing.txt`](pairing.txt) is empty). Afterwards
`adrift_report.py` reports 0 refused rows.

run: documented_rule.py READY 1 of 1; adrift_report.py refused rows 0; restatus22.py FAILS 0

## Review (OPUS)

The owner read goes to SWE2-AUDIT-SPEC.
