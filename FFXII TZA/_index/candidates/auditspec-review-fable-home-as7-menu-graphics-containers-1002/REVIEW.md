# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-as7-menu-graphics-containers-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-AS7-MENU-GRAPHICS-CONTAINERS-1002` · Package: `_index/candidates/fable-home-as7-menu-graphics-containers-1002/` · Page: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/as7-menu-graphics-containers.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 5 anchors; mechanically rejected 1, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `00292050`: `mov eax,1; shl eax,cl; movzx eax,ax` limits the test to bits 0-15, as stated. The return address `(ecx+0xD)*2*8` = `o+0xD0+ecx*0x10`.
- Site `00292390 + 0x152` = `002924E2`; the page reads `00292390`.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
