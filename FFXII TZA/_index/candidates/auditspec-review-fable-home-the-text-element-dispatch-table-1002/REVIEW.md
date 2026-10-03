# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-text-element-dispatch-table-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-TEXT-ELEMENT-DISPATCH-TABLE-1` · Package: `_index/candidates/fable-home-the-text-element-dispatch-table-1002/` · Page: `99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 5 anchors; mechanically rejected 3, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `002A2860`: `cmp word [rcx+0x3F0], 0` / `jle` (signed) to the return; the zero stores at `002A2875` (byte `+0x3F3`) and `002A287C` (word `+0x3F0`); `003697F0` is called with `+0x3F8` and then tail-jumped with `+0x400`.
- Site `002A6190 + 0x79A` = `002A692A call 002A2860`, inside the message-window procedure that the page reads; host fit holds.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
