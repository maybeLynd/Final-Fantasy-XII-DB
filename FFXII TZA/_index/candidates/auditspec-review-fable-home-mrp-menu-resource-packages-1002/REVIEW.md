# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-mrp-menu-resource-packages-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-MRP-MENU-RESOURCE-PACKAGES-1002` · Package: `_index/candidates/fable-home-mrp-menu-resource-packages-1002/` · Page: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/mrp-menu-resource-packages.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 5 anchors; mechanically rejected 2, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `003F4690` (330 B) read in full. State 0 goes to the 0x128 arm when `byte [rcx+0xD0] & 1` or `word +0xD8` is set, and otherwise falls to the `+0xDA` test. State 1 enters at the `+0xDA` test, and any other state returns 0.
- 0x128 arm: stack array `[rsp+0x20..0x40]` = `+0xC8`, `rcx+0xD0`, `rcx+0xF8`, `rcx`, `+0x128`; block `[rsp+0x48]` dword 0, `[rsp+0x50]` = &array, `[rsp+0x58]` 0. The code address is `003F4330`. The result goes to `+0x110`, then `00246AD0(rcx, result)` runs, then `+0xC0 = 1`. The 0xF0 arm is the same with the code address `003F4060`, three array entries, result to `+0x118`, and `+0xC0 = 2`. All six call offsets check out.
- Host: `003F4840` is the shop row of the page's `.mrp` loader table.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
