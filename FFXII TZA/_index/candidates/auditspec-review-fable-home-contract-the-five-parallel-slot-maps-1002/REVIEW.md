# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-contract-the-five-parallel-slot-maps-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CONTRACT-THE-FIVE-PARALLEL-SLOT-M` · Package: `_index/candidates/fable-home-contract-the-five-parallel-slot-maps-1002/` · Page: `11-Party/CONTRACT-the-five-parallel-slot-maps.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 5 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `00273800`: the loop calls `0035BB20(ebx)` for `ebx = 0..3` (`cmp ebx, 4; jl`), matches dword `+4` against the incoming `ecx`, and returns `((~byte[rax]) >> 3) & 1`. Exact.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **`00273800` (entered from `0035BC50`): host-fit defect.** The page cites `0035BC50` once, in *"UI - CLIENT (3 edges). ... are also called by bodies filed to UI: `00273880`, `0035BC50`, `0031EB20` - shared machinery across the layer boundary, no shared ownership"*. The body does not touch the five nine-entry maps; it scans the four battle-menu member slots `0035BB20(0..3)`. The row's sentence, site and anchors are exact; only its host is wrong, and the section heading (*"called from this page's functions"*) is false for it, because this page says the caller is not one of its functions.
  - **Repair:** remove the `00273800` row from this package (and from the section already on the page: the applier prints `ALREADY`), and re-home it unchanged on `16-UI/the-selection-the-menu-publishes.md`, which documents `0035BB20(k)` as the k-th member slot that the battle-menu walk `0035BC50` accepted, and its sibling four-slot find `002732E0`.
- With the only row re-homed, nothing remains in this package. Withdraw it.
