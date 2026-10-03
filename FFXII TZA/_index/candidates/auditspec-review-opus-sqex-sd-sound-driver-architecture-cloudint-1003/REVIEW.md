# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-sqex-sd-sound-driver-architecture-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SQEX-SD-SOUND-DRIVER-ARCHITECTURE-CLO-665A4` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-sqex-sd-sound-driver-architecture-cloudint-1003/` · Page: `18-Audio/sqex-sd-sound-driver-architecture.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 2 functions, 10 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 2 rows, 10 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- **Package choice.** `tasks_C2.tsv` names the `-ee-1003` package for this task, but the board question (`2 cloud-drafted, OPUS-verified interior citations ... at 33eb7192f`) matches this `-cloudint-1003` package (`session: opus-self`, 2 rows). The `-ee-1003` package has 8 rows and already has its own review (`auditspec-review-opus-sqex-sd-sound-driver-architecture-ee-1003/`). This record reviews the package the board asks about.
- Semantic pass: **all 2 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 2, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `001DBA60`: `edx` is saved in `ebx` and `xmm0` in `xmm6` across `00210B30(rcx, rdx)` (`rcx`/`rdx` untouched before the call); the tail jump to `00210ED0` has `rcx` = result, `xmm1` = incoming `xmm0` and `r8d` = incoming `edx`. Exact.
  - `003456E0`: `n` = the pop (`edi`), `m` = `00473B90(n)` (`ebx`), `002E1CD0(0, 3)`, `test ebx, ebx; jns` (replace only when negative) with `00473B90(0)`, `003601B0(0xd)`, then a tail jump to `0017E7D0(n, m)`. Exact.
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.
