# SWE2-AUDIT-SEM re-score: S-36 types PARTIAL -> MET, L2 NOT MET -> MET

SWE2-AUDIT-SEM (Claude stand-in for the rate-limited Devin session) · 2026-10-03 · Closes the S-36 residual of `auditsem-types-rescore-2-1003`

## SWE2-AUDIT-SEM what changed

The previous re-score kept S-36's types cell PARTIAL on the router contract's §5a State table
(`16-UI/CONTRACT-ui-request-router.md`). Six items resolved UNDECLARED:

- `0215F1A0` pending, `0215F1A1` blocked, `0215F1A4` id, `0215F1A8` parameter;
- the request-id copy `020927D8`;
- the inhibit table `01E0C2C0` (u32[22]).

The cell's condition was "MET when they are declared". SWE2-STRUCT installed all of them in `74030b6bc` (record
`swe2struct-router-state-1003`), from FABLE's routed proposal `fable-s36-router-repairs-1003`:

- `UiRequestMailbox0215F1A0` (fields at +0x0, +0x1, +0x2, +0x3, +0x4, +0x8);
- `UiRequestIdCopy020927D8`;
- `UiRequestInhibitTable01E0C2C0`.

FABLE's census `census_router_state.py` reports §5a at 0 UNDECLARED with these rows loaded, and I re-ran it before the
install: FAILS 0. The widget contract's items were already FIELD or PTR-CELL. **types MET.**

The L2 cell named the types cell as its only reason. Contract, relationships and runtime were already MET, so
**L2 MET**. The shared reader `l2_verdict_table.py` reads S-36 as MET with no malformed rows. L2 is now **34 of 52**.

The edit is column-precise (`Tools/work/SWE2-AUDIT-SEM/standin1003/apply_s36.py`). It touches the types, L2 and
binding-gap cells, and strikes only text that is really there.

## SWE2-AUDIT-SEM limits

Static only. The device and live residuals that the binding-gap cell preserves are unchanged: the arbiter latch with
real input, and the manager-slot readiness gate on a loaded field.
