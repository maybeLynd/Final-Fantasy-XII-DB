# SWE2-AUDIT-SPEC review: ASTRA filecache source-key initialization

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-FILECACHE-SOURCE-KEY-INITIALIZATION-1002` · Package: `_experiments/evidence/filecache-source-key-initialization/`
(publisher commit `50dd4cc33`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

Scoped as written: the initial-construction prior value is narrowed to zero, and a rebind carries the prior value,
under normal ABI and no interference. It is not an all-writer, lifetime or natural empty-hit proof.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- Source constructor `00597930`: `mov dword [rcx+28h],eax` with eax = 0 (`00597951`) comes before the guarded
  `call 59EE90` (`0059795D`).
- Reader constructor `00597970`: `mov dword [rcx+48h],ebp` with ebp = 0 (`005979A3`) comes before
  `add rcx,20h / call 59EE90` (`005979B2`/`005979B6`). The +20h receiver bias puts reader+48h at receiver+28h, the
  out-key field of the resolver record.
- Rebind `0059ED70`: its first call is `59EE90(rcx+20h)` (`0059ED97`).
  - Its own full-width writes are `[+8]` dword, `[+10h]` qword, `[+1Ch]` dword twice and `[+18h]` dword. None
    touches `48h..4Ch`, so there is no direct key reset.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` (prove-02, current driver) re-run: exit 0, stdout identical, output **byte-identical** to
  `result-02.json`.
- `control.py` (control-01) re-run: exit 0, stdout identical. The three cases (failed capture, missing source, coherent
  non-zero key initializer → "original byte mismatch") are identical to retained, each with its result absent.
