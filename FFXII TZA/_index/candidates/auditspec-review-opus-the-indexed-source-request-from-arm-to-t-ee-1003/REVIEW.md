# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-indexed-source-request-from-arm-to-t-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-INDEXED-SOURCE-REQUEST-FROM-ARM-T-14DEA` · Package: `_index/candidates/opus-the-indexed-source-request-from-arm-to-t-ee-1003/` · Page: `02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md` (commit b0c7c5a57)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors; rejected 0, missing 0.
- Semantic pass: **every row and every callee whose inputs or result the row names** read against raw capstone output of the certified image (SHA256 73461D08...):
  - `003DF440` exact: `movsxd` of `r8d` and `ecx`; `n` = `0032F2F0(a, c)`; `0036C1D0(5, 5)`; `jle` (signed) to the tail `jmp 0036C140` (`003DF541`); `k` = `0032F2C0(a, c)`; `0032F170(a, b, &[rsp+0x68], &[rsp+0x20])`; `0036A100(n)`, null -> `0036C1D0(6, 5)`, `0036A190(n)`, `0036C140()`; `cmp ebx, 7` / `ja` (unsigned) else `r` = 0; `r` = `02B59360` + (`c` + 8`a`) * 0x38 (`003DF4CD`/`003DF4D1`); the seven stores at `+0x2C`, `+0x18`, `+0x2E` (w2 + 2), `+0x20` (0), `+0x28` (word `b`), `+0x30`, `+0x34` exactly as listed; `00267310(a)` non-zero -> byte `+0x10` = 1, else `003DF550(r)`; tail `jmp 0036C140`.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
