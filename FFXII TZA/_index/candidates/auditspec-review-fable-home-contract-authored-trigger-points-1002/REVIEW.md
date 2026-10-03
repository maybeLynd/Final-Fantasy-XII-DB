# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-contract-authored-trigger-points-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CONTRACT-AUTHORED-TRIGGER-POINTS` · Package: `_index/candidates/fable-home-contract-authored-trigger-points-1002/` · Page: `03-World-Area-Field/CONTRACT-authored-trigger-points.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 2 functions, 10 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 2 rows, 10 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **all 2 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `0035E500`: `cmp r10w, 3; jge` (signed) to the return. The slot is `rcx + n*8 + 0xC`. `edx == 0` stores dword 0 plus words `r8w`/`r9w` at `+0x10`/`+0x12`; `edx == 1` stores dword `edx` (1) and `r8d` at `+0x10`; any other value falls through to the increment, so all three paths increment.
- `0035E560`: `and dword +8, 0xFFFFFFFC`, word `+4 = 0`, and qwords `+0xC`/`+0x14`/`+0x1C` zeroed, under a null guard.
- Host: `0050FAF0` is read on the page as `btlAtelOpenTreasureMessage`'s end thunk.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
