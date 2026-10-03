# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-scriptvm-verb-dispatch-and-parameter-enc-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-SCRIPTVM-VERB-DISPATCH-AND-PARAMETER-E` · Package: `_index/candidates/fable-scriptvm-verb-dispatch-and-parameter-enc-cloudint-1002/` · Page: `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 8 rows, 40 anchors; rejected 0, missing 0.
- Semantic pass: **all 8 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 8 exact, including `00264B50`'s argument shift (incoming stack args at `[rsp+70h]`/`[rsp+78h]` become the callee's 6th/7th, `r9` its 5th) and the float-pop orderings of `0034A940` (f4/f3/f2 into xmm1/2/3) and `0034EBC0` (c/b/a).
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
