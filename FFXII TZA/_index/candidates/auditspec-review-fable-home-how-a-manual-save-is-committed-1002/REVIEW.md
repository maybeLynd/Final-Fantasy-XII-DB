# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-how-a-manual-save-is-committed-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-HOW-A-MANUAL-SAVE-IS-COMMITTED-10` · Package: `_index/candidates/fable-home-how-a-manual-save-is-committed-1002/` · Page: `19-Save-Load-Settings/how-a-manual-save-is-committed.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 5 anchors; mechanically rejected 3, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `003BB6A0`: `cmp ecx, 0xC7; ja` (unsigned). Then the `[rdx]` qword goes to `02B407C0[ecx]`, a byte loop copies `r8` through its terminator to `02B40E28`, and the stores are `02B40558 = ecx`, 0 to `02B40EC0`/`02B40E18`/`02B40FE4`, 8 to `02B40E1C` and qword 1 to `02B40E10`. Then `003BA720` is called and 1 returned. All as stated.
- Site `00582040 + 0xFF` = `0058213F`, in the queue's per-kind dispatch that the page reads.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
