# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-arm-catalogue-slice-h-ids-236-267-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-ARM-CATALOGUE-SLICE-H-IDS-236-267` · Package: `_index/candidates/fable-home-arm-catalogue-slice-h-ids-236-267-1002/` · Page: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-H-ids-236-267.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 4 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 4 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `00183260`: `00189120` is called, null-tested, called again, and `byte [rax+2] = 1` stored; `rax` is left with the second result. The text is exact.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **`00183260` (entered from `0079C140`): host-fit defect.** The page cites `0079C140` once, in *"Input - CLIENT (1 edge). 1 inbound (Input bodies `0079C140` call page-cited `00182DE0`)"*. `0079C140` is the PApplication slot-28 per-frame update, and the body is the `00189120`-lookup-then-flag pattern on a game-application subsystem object. It is not a console arm in ids 236-267. The row's sentence, site and anchors are exact; only its host is wrong, and the section heading (*"called from this page's functions"*) is false for it, because this page says the caller is not one of its functions.
  - **Repair:** remove the `00183260` row from this package (and from the section already on the page: the applier prints `ALREADY`), and re-home it unchanged on `00-Engine-Core-Runtime/Application-Root/game-application.md`, which reads `0079C140` (slot 28) and tables the same `00189120` lookup / `byte [rax] = 1` pattern for slots 8-10.
- With the only row re-homed, nothing remains in this package. Withdraw it.
