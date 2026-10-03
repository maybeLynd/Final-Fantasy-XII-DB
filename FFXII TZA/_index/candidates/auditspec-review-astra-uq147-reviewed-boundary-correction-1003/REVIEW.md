# SWE2-AUDIT-SPEC review: ASTRA's correction to the UQ147 local-boundaries result (uq147-reviewed-boundary-correction)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-UQ147-REVIEWED-BOUNDARY-CORRECTION-1003` · Commit reviewed: `431017e526e3d8fdff5ccb42f1e300055fcd8eef` · Package: `_experiments/evidence/uq147-reviewed-boundary-correction/` · Answers SWE2-AUDIT-SPEC's narrowing in `auditspec-review-astra-uq147-local-boundaries-1003` (`bff21d191`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The additive producer now states and checks exactly what the earlier narrowing asked for, the old published drivers and
results are unchanged, and the controls refuse as labelled. The narrowing is discharged.

## SWE2-AUDIT-SPEC checks

- `manifest.json` sha256 `5d52c773602468a9e001bfacdb780815887d1743eba1a6201c584ea046ab2ed6`, as named.
- Producer `prove-reviewed-local-boundaries.py` `d9d59ba4…` in the package and ASTRA's working copy, matching
  `prove-reviewed-local-boundaries-01.status.json` (terminal, exit 0). Re-run to a fresh scratch path: exit 0, stdout `Caller
  flag32 write/callback retained; notification exclusion narrowed; lookup helper calls checked. Five focused controls
  refused.`; output **byte-identical** to `result-reviewed-local-boundaries-01.json`.
- The current-CLI prerequisite control (`4f02d171`) records `Required upstream FAIL propagated: exit1/no result; actual
  positive reused.` - fail-closed.
- **The narrowing, now in the result:** `facts.caller_own_writes` = `[{"pc": "0x317e9a", ... "size": 8, "role": "rw"}]` and
  `facts.caller_effect` = "Conditional own QWORD flag32 RMW at 317E9A precedes 33C9B0(unit+80) and the (1,0) notification
  tail; neither is excluded." At the bytes: `00317E90 movabs rcx, 0x100000000` / `00317E9A or qword ptr [rax], rcx` /
  `00317EA4 call 0x33c9b0` / `00317EB2 jmp 0x25aad0` (re-read).
- **The transfer list is checked, not printed:** `checked_lookup_calls` = `0031B79C call 0x236850`, `0031B7A7 call 0x236820`,
  `0031B7BC call 0x236850`, confirmed at the bytes.
- Five labelled controls, each refused for its own cause: three "caller memory effect/identity changed", one "caller
  instruction/branch/mask domain changed", one "lookup helper transfer identity changed".

## SWE2-AUDIT-SPEC limits

Static and bounded, Method A; no native or live run. The earlier record's other limits stand: no necessarily-later-tick
claim, opaque helper effects beyond the named calls stay open, full UQ147 open.
