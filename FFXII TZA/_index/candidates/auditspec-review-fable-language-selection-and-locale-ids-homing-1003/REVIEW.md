# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-language-selection-and-locale-ids-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-LANGUAGE-SELECTION-AND-LOCALE-IDS-HOMI` · Package: `_index/candidates/fable-language-selection-and-locale-ids-homing-1003/` · Page: `19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md` (commit b7c6eb07d)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 4 functions, 18 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 4 row(s), 18 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...), call offsets resolved:
  - `002CFE40` exact: two `0035D330(1, word << 16)` lookups; dword `+0x38` difference returned when non-zero (`002CFE81`); else two more lookups, dword `+0x30` difference, `cmovne` falling back to word `rcx+8` - word `rdx+8`.
  - `002D0070` exact: record dword `+0` == 6 -> `jmp 002CFE40` at `+0x36` with `rcx`/`rdx` restored; else the `+0x30` / word comparison.
  - `002D5C30` exact: `movsx` byte `+0x13` of qword `+0x150` (0 when null), `0035BB20(movsx word +0x140)`, `jmp 002D5500` at `+0x44` with `edx` = that byte and `r8d` = record byte `+0x87`.
  - `0056D870` exact: three signed dword indices at `r8`; entry 1: bit 0 of dword `+8` = `setne` (byte `rcx+0xA` != 0xFF), byte stored as word `+0xA`, byte `[[+0x20] + b*8 + 7]` to `+0x39`; entry 2: qword `[rcx]` to `+0x18`, `0020E620(0)` at `+0x6C` to dword `+0x20`; `0029FF60(entry 3, 0, 0, dword +0x10 & 0x7FFFFFFF, 0, 0)`; `jmp 0029FB50` at `+0xC4` with entry 3.
- Limits hold: body statements only, static evidence; the draft and FABLE's re-read are not independent review, this record is.
