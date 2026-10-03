# SWE2-AUDIT-SPEC review: FABLE cloud-drafted F-homing rows (fable-pkfl-package-container-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-PKFL-PACKAGE-CONTAINER-HOMING-1003` · Package: `_index/candidates/fable-pkfl-package-container-homing-1003/` · Page: `26-PKFL-Package-Container/Container/pkfl-package-container.md` (commit `b7c6eb07d`, reviewed at HEAD `81a9fa56d`; the package is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`, and wrote nothing. The section is on the page at line 514, and the sentence is on the page verbatim.
- **rows.json.** 1 row, 5 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **Semantic pass.** The row was read clause by clause against `disr.py` output of the certified image.
  - `003DF2C0`:
    - `movsxd rbx, ecx`, then `0036B970([rbx+0x18], rsp+0x20, 2)` at +0x18. `test eax, eax` / `je` returns.
    - The two local qwords go to `+0x18` and `+0x20`. `test rbx, rbx` / `je` returns.
    - The `+0x18` null test and the `cmp word [+0x10], 0` gate lead to `0032F3A0(movsx byte +0x11, r)`. The remainder r comes from `0x66666667` / `sar 2` / sign fix, then `r8 − 10q`, so it is a signed remainder of 10.
    - Then `003DF360(movsx +0x11, movsx +0x12, [+0x18], [+0x20])` at +0x83, qword `+0x18` = 0 and byte `+0x10` = 4.
    - Exact. The sentence also correctly says that `rbx` is the sign-extended `ecx` used as a base.
- Limits: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
