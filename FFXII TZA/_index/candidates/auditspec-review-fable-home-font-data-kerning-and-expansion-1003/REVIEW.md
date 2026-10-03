# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-font-data-kerning-and-expansion-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-FONT-DATA-KERNING-AND-EXPANSION-1` · Package: `_index/candidates/fable-home-font-data-kerning-and-expansion-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `c6de67245`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact. Its caller `001B58E0` is this page's font-session creator, and the page cites it in body statements.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 1118, and the row at line 1124 matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **`001FDE60` (0x55 B):**
  - `xor eax, eax`, then `mov [rdx], rax`, `[rdx+8]` and `[rdx+0x10]`.
  - `lea rdx, [rcx+0x118]` / `lea rcx, [rdi+0x18]` / `001FDE8C call 001EDF00` (= +0x2C).
  - `rcx = rdi`, `rdx = [rbx+0x100]`, `r8 = [rbx+0x108]` / `001FDEA2 call 001A4BF0` (= +0x42).
  - `mov rax, rdi`: it returns the incoming `rdx`. Exact.
- **entered_from.** The raw byte scan finds two references: `001B5AF9` = `001B58E0` + 0x219 (cited), and `001B6134` in `001B6110` + 0x24, which no page cites. At the cited site, `rcx` = `[rbx+0x28]` and `rdx` = `rbp-0x28`; the result's first qword goes to `001A1E40` with `rsi+0x20`.
- **Host fit.** This page cites `001B58E0` in body statements:
  - line 184, the font lookup in the `001B4D70` subtree;
  - line 554, "**`001B58E0(lib, key)`** — session creation";
  - line 758, "`001B58E0(lib, fileId)` to mint the font's session";
  - and lines 512 and 522.
  The body builds the record that the session creator files. It fits.
- **Advisory (not a defect).** Before the first call the body also stores dword 0 at `[rsp+0x20]` (`001FDE88`), the 5th-argument slot. The sentence does not mention it. Add ", with 0 as a fifth argument" after "`rcx+0x118`" only if `001EDF00` is shown to read a 5th argument.
- **Advisory (tool).** The applier's caller test is a substring test that the applied row satisfies by itself. Here the caller is also cited five times outside the section.
- `001FDE60` is cited on no other page (repo-wide grep).
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
