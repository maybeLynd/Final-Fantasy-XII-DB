# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-ui-request-router-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-UI-REQUEST-ROUTER-HOMING-1003` · Package: `_index/candidates/fable-ui-request-router-homing-1003/` · Page: `16-UI/Request-Router/ui-request-router.md` (commit `c29c5b85e`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 2 functions, 6 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 2 row(s), 6 anchors. **Every row** read clause by clause against raw capstone output of the certified image (SHA256 73461D08...); every relative call (`fn`+0xNN) resolved to its target:
  - `002E1660` exact: `dec eax` / `cmp eax, 1` / `cmovbe` - 1 for results 1 and 2.
  - `002E2320` exact: `0028F5F0()` then `jmp 002E0E30` with the result in `ecx`.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
