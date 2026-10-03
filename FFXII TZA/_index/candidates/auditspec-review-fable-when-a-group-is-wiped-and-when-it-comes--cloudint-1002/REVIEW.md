# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-when-a-group-is-wiped-and-when-it-comes--cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-WHEN-A-GROUP-IS-WIPED-AND-WHEN-IT-COME` · Package: `_index/candidates/fable-when-a-group-is-wiped-and-when-it-comes--cloudint-1002/` · Page: `05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 5 rows, 23 anchors; rejected 0, missing 0.
- Semantic pass: **all 5 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 5 exact, including the re-read bound of `00234990`, the bit-31/bit-28 rewrite order of `002EDCC0` and the exchange sort of `0035DEB0` (n-1 outer passes, signed `jle`, 12-byte swap as qword+dword).
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
