# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-force-fight-mode-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-FORCE-FIGHT-MODE-CLOUDINT-1003-AAC0A` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-force-fight-mode-cloudint-1003/` · Page: `00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 3 functions, 13 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 3 rows, 13 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- Semantic pass: **all 3 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 3, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `002734B0`: `test eax, eax; jle` on the first count and `cmp ebx, eax; jl` after re-calling `0035BB60` each step, both signed; `test byte [rax], 4; jne` to the tail jump `0035BB20(i)`; `xor eax, eax` otherwise. Exact.
  - `0050EEA0` / `0050F0A0`: `003BB420` is called with the incoming `rcx` unchanged, and `n` (`ebx`) goes to `edx` for `0017D280` (`00D22AD8` / `00D22860` by `lea`) and `0026B4E0`. The call orders (`00254CB0(0)` first vs. tail-jumped last) match the bytes. Exact.
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.
