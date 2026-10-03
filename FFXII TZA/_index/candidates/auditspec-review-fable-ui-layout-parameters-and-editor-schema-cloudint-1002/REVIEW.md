# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-ui-layout-parameters-and-editor-schema-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-UI-LAYOUT-PARAMETERS-AND-EDITOR-SCHEMA` · Package: `_index/candidates/fable-ui-layout-parameters-and-editor-schema-cloudint-1002/` · Page: `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 11 rows, 52 anchors; rejected 0, missing 0.
- Semantic pass: **all 11 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Ten of the 11 rows are exact (`0024B100`, `0024B120`, `002716F0`, `00296600`'s three word tables at `009161F0`/`00916200`/`00916218` with the 0x11-0x1A and out-of-range zero returns, `0029F580`'s two-level index, `002C98C0`, `002CB8D0`'s 9-record loop and `002CAFE0` call, `002D5030`, `00345B60`, `003FE5D0`). Row `003EEEC0` (read in full, 0x184 bytes) states one byte-`+0xC8` arm wrongly: see the defect below.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.

## SWE2-AUDIT-SPEC narrowing / notes

**Defect (row `003EEEC0`).** The row says the byte-`+0xC8` state **3 calls `003EEEC0`+0xB4 with `rcx`**. The bytes dispatch `movzx ecx,byte [rbx+0C8h]` / `test ecx,ecx` (0 -> `003EEFC6`) / `sub ecx,1; je` (1 -> `003EEF9A`) / `sub ecx,1; je` (2 -> `003EEF86`, stores 3) / `cmp ecx,2; jne 003EF037` at `003EEF68`. Since `ecx` = state-2 there, the call `00244F00(rcx)` at `003EEF74` (+0xB4) runs for state **4**. State 3, like any state of 5 or above, goes to `003EF037` and returns 0 with no call. **Repair:** replace "3 calls `003EEEC0`+0xB4 with `rcx`" with "4 calls `003EEEC0`+0xB4 with `rcx`; 3 and any other state return 0", and re-run `interior_applier.py`. Every other clause of the row is exact: the dword switch 1/2/0xF/0x12/other, the `+0xCC` countdown, state 0's `>2` signed test, state 1's `(0x3E8, 8, 0)` call and the 0x13 re-entry into the `+0x55` call, and the `+0x37` tail jump. The producer repairs its own row; nothing in this review edits the page.
