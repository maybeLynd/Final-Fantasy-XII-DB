# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-handbook-screen-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-HANDBOOK-SCREEN-CLOUDINT-1003-D2F80` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-the-handbook-screen-cloudint-1003/` · Page: `16-UI/Handbook/the-handbook-screen.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 2 functions, 9 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 2 rows, 9 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- Semantic pass: **all 2 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 2, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `001B1F80`: there is no frame, so `[rsp+0x28]` is the fifth argument. It goes to `+0x3a58`, and `edx`/`r8d`/`r9d` go to `+0x3a4c`/`+0x3a50`/`+0x3a54`. Exact.
  - `003A7E80`: `p` = `rcx+4`. Byte `[rcx+2]` goes to `p+0xc2`, and the zero-extended byte `[rcx]` goes as a word to `p+0xc0`. `[[02EBEFA0]][byte [rcx]*8]` = `p`. The call is `004FF270(p, dword 02EBB738 + ecx)`, with `ecx` = the low dword of `p`. The return is `p + movsxd edx`. Exact.
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.
