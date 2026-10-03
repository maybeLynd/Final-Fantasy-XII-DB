# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-r2-force-fight-toggle-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-R2-FORCE-FIGHT-TOGGLE-EE-1003-4BA90` · Package: `_index/candidates/opus-r2-force-fight-toggle-ee-1003/` · Page: `15-Input/Modal-Toggles/r2-force-fight-toggle.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 1 row, 5 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against a full linear decode of the certified image (SHA256 73461D08..., capstone, function-list extent 191 B):
  - `007A5E50` exact: byte `02EACFE9` (.data) tested at entry, `jne` to the epilogue (`007A5E5D`), so a non-zero byte returns at once. Loop head `007A5E80` calls `007AD630`; `sub rcx, [02EACFF0]` (.data qword), `cvtsi2sd` then `jns` over `addsd xmm6, xmm7` where `xmm7` is the .rdata double at `00D27A68` = 0x43F0000000000000 = 2^64 (the sign tested is the subtraction's, since no flag-writing instruction sits between); the `007AD670` result gets the same `test`/`jns`/`addsd` treatment; `divsd` at `007A5EB6`; `007A5EBA` stores the saved `007AD630` result (`rbx`) to `02EACFF0`; `cvtpd2ps` narrows; `xmm0` = quotient before each of `007BAEC0`, `007BB670`, `007BB780`, `007BC4F0`; `mov ecx, 0x20` then `call [008C21B0]` (.rdata IAT slot) at `007A5EEA`; the byte is re-read and `je 007A5E80` (`007A5EF9`) repeats while it is zero; the exit falls to the epilogue and `ret`.
  - Anchors: all five are instruction boundaries strictly inside the body and decode to the recorded mnemonics (`call`, `divsd`, `mov`, `call`, `je`).
- Limits hold: body statements only, static evidence; the cloud draft and OPUS's re-read are not independent review, this record is.
