# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-game-settings-ini-and-runtime-config-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-GAME-SETTINGS-INI-AND-RUNTIME-CON` · Package: `_index/candidates/fable-home-game-settings-ini-and-runtime-config-1002/` · Page: `19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 2 functions, 10 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 2 rows, 10 anchors; mechanically rejected 2, skipped 0, missing 0.
- Semantic pass: **all 2 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `002287A0`: two `00229EA0` calls, the first compared to 6 and the second to 5; either match returns 1.
- `0029FAD0`: `shl 16; sar 22` is bits 6-15 as signed 10 bits. `a`/`b` are the home slots `rsp+0x40`/`rsp+0x48`, and `[rsp+0x20]` is the fifth argument (after `push rdi; sub rsp,0x30`). Then the word `+0xA` store, `and 0xFFFF003F`, and `or byte +0x2D, 4`.
- Host: `002507C0` (present interval) and `0023B6F0` (Config-screen row) are read on the page.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
