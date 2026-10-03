# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-console-command-names-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CONSOLE-COMMAND-NAMES-1002` · Package: `_index/candidates/fable-home-console-command-names-1002/` · Page: `00-Engine-Core-Runtime/Developer-Tuning-Console/console-command-names.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 5 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `001C0400`: `imul` by `0x6666666666666667`, then `sar rdx, 4` and the sign-bit add, is a signed divide by 40. The low-dword test (`test edx, edx`) and the `+0x10` null test both lead to `mov eax, 1`; otherwise it returns `[[rcx+0x18]+0x38]`.
- Site `001CD0E0 + 0x8B8` = `001CD998`, inside the page's row renderer.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
