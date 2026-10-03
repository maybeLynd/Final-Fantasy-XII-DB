# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-how-a-gamepad-becomes-a-controller-obje-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-HOW-A-GAMEPAD-BECOMES-A-CONTROLLE` · Package: `_index/candidates/fable-home-how-a-gamepad-becomes-a-controller-obje-1002/` · Page: `15-Input/how-a-gamepad-becomes-a-controller-object.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 5 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `00797460` (547 B) read in full: six `0x48`-stride nodes at `o+0x30`..`o+0x198` (the last at `r8+0x168`), each unlinked only when `[node+0x10] == o`. The node at `o+8` is relinked before `01F401F8` with `01F40200` updated (`007975C8`), and `02EA537A = 1`.
- COM-style chain: slot `+0x18` (`js` exits), `+0x58` with `01CC7130` (`js`), `+0x68` with `[02EA5248]` and 6 (exits on `== 0x80004001`), then `+0x38`. The 0x10-byte block holds `bl` (still 0) and the object; the 0x1F8 allocation is null-checked before `00792870`, and `rbx` (0 when null) is stored to `02EA58B8`.
- Site `00796230 + 0x3C` = `0079626C call 00797460`, inside the page's enumeration callback; host fit holds.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
