# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-contract-per-frame-update-gate-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-CONTRACT-PER-FRAME-UPDATE-GATE-HOMING` · Package: `_index/candidates/fable-contract-per-frame-update-gate-homing-1003/` · Page: `00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md` (commit b35f1958c; reviewed at HEAD 89538d085, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

This is an interior package: it ships `interior_applier.py` and no `homing_applier.py`. Only the sentences were reviewed. It has 2 rows, fewer than 15, so I read both clause by clause against the full listings. All 10 anchors are correct and both rows hold as written.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 2 functions, 10 anchors`, `ALREADY` and `FAILS 0`, exit 0. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 2 rows, 10 anchors, `mode: homing`; rejected 0, skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `0028E070` correct.
    - `[0209BE80]` null -> return (`0028E07E`). Otherwise `or dword [rax+0x10F68], 0x40` (`0028E080`).
    - `002BDB60([0209BE80] + 0x8FA0)` (`0028E095`), with the global reloaded before the call.
    - It reloads again and tests for null (`0028E0A4`). If non-null: `jmp 002BDCA0` with `rcx = [0209BE80] + 0x8FA0` and `edx = 0` (`0028E0B3`), a tail jump. If null: return.
  - `0028E0C0` correct. It has the same shape, with `and dword [+0x10F68], 0xFFFFFFBF` (`0028E0D0`), then `002BDC00` (`0028E0E5`), then `jmp 002BDCA0` with `edx = 1` (`0028E106`).
- README count sentences checked against `rows.json`: "named 2 F-frontier functions", "2 staged with 10 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): neither function belongs to an accepted family, so the base rule applies.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
