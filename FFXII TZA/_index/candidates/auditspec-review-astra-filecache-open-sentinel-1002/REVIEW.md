# SWE2-AUDIT-SPEC review: ASTRA filecache open sentinel

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-FILECACHE-OPEN-SENTINEL-1002` · Package: `_experiments/evidence/filecache-open-sentinel/`
(publisher commit `446a56af9`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

The formula is exact. The "eight equality classes" are a predicate proof, not eight native tests.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- `0059D920` (27 bytes) is three `cmp qword` tests: `[+28h],-1`, `[+30h],0`, `[+40h],-1`. All three equal gives
  `xor al,al`; any one differing gives `mov al,1`.
  - So AL = !(q28==-1 && q30==0 && q40==-1), and only AL is assigned.
  - q28=-1, q30=0, q40=0 therefore returns AL=1, the "open" verdict for a zero view.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` re-run: exit 0, result **byte-identical** to `result-01.json`.
- `control.py`: three refusals identical to retained (failed getter capture, missing retained zero result, missing
  getter source).

## SWE2-AUDIT-SPEC note

The retained constructor/resolver zero-view linkage remains conditional on ABI, private frame, no alias and no
opaque interference. The page's backing-bound prose should carry that qualification, as the request says.
