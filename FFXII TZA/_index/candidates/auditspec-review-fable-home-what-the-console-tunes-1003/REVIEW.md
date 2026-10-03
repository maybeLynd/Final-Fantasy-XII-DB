# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-what-the-console-tunes-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-WHAT-THE-CONSOLE-TUNES-1003` · Package: `_index/candidates/fable-home-what-the-console-tunes-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `c6de67245`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact.

The body is the array arm of the value-variant teardown `002001F0`. It destroys each 16-byte element and frees the block through the allocator at `+0x18`.

This page documents that variant: line 159 has `001FF6B0` "ensures the variant is a map", lines 371–380 discuss the map find, and line 1277 has the interior row in which `001FF6B0` calls `002001F0`. So the body sits inside the page's own coverage of the variant. A library-level home exists; that is recorded as an advisory.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 1283, and the row at line 1289 matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 1 (`001EF540`, "already cited by" this page). Skipped 0, missing 0, corrections 0.
- **`001C36F0` (0x68 B):**
  - `mov rdi, [rcx+8]` / `mov rbx, [rcx]` / `cmp rbx, rdi` / `jae` skips the loop. Inside the loop: `001C371B call 001FEA00` (+0x2B) on `rbx`, `add rbx, 0x10`, `cmp` / `jb`. That is an unsigned half-open walk, `[rcx]` up to but not including `[rcx+8]`.
  - Then `mov rdx, [rsi]` / `test` / `je` returns. Otherwise `lea rcx, [rsi+0x18]`, `r8 = ([rsi+0x10] - rdx) AND ~0xF`, and `call [vtable+0x18]`.
  - The sentence is exact clause by clause.
- **entered_from.** The raw byte scan finds three references: `00200297 call` = `002001F0` + 0xA7 (cited), and two `jmp` from the 7-byte stubs `00897F6C` and `008990B5`, which no page cites.
  - In `002001F0`, the `+0xA7` call is the arm for one of the six jump-table kinds: `rbx = [rcx+8]`, null skips, then `001C36F0(rbx)` and `edx = 0x20` into the tail `jmp 00809950`.
- **Host fit.**
  - `002001F0` is cited on this page in OPUS's interior row for `001FF6B0` (line 1277). That row says it "calls `002001F0` with the incoming registers, stores 3 to `[rcx]`", which is the variant reset before the variant becomes a map.
  - The console's value store is this variant (lines 159, 371–380, 908). The array teardown is part of the same type. It fits, though it is generic within that type.
  - `001C36F0` is cited on no other page (repo-wide grep).
- **Advisory (not a defect).** `002001F0` is also named on `23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md` (line 314, "the value builders `002001F0` / …"). `third-party-middleware-inventory.md` line 1151 names `001FEA00` as the EH-guard wrapper that calls `002001F0` (the JsonBox row). If FABLE gives the JSON variant a library-level home, this row and its caller should move there together.
- **Advisory (tool).** The applier's caller test is a substring test that the applied row satisfies by itself. Here the caller is also cited at line 1277, outside the section.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
