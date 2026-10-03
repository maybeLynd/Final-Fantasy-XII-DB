# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-contract-manager-slot-entry-tables-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CONTRACT-MANAGER-SLOT-ENTRY-TABLE` · Package: `_index/candidates/fable-home-contract-manager-slot-entry-tables-1002/` · Page: `04-Actor-Entity/CONTRACT-manager-slot-entry-tables.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 5 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `0037DD50`: both indexes `movsxd`; entry = `02ADD990 + ecx*0x3D0 + r8d*0xF0`; the `edx == -1` arm stores 2 at `+0xE8`. Otherwise it reads `movzx word [[02ADD980 + ecx*0x3D0] + edx*0x60 + 0x28]`, then `cvtdq2ps`, adds 1.0 (`01CEBBA8` = 0x3F800000) and stores to entry `+8`.
- Site `003DCFB0 + 0xA8` = `003DD058`, in the page's B-side tick.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
