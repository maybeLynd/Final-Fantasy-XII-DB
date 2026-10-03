# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-how-the-bigfile-index-loads-and-is-veri-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-HOW-THE-BIGFILE-INDEX-LOADS-AND-I` · Package: `_index/candidates/fable-home-how-the-bigfile-index-loads-and-is-veri-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact. The body initialises the reader handle that its caller `001F4250` takes, and this page's key-address table describes `001F4250` as "takes a free reader handle for the record (or makes a sixteenth)".

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 479, and the row at line 485 matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **`002150B0` (0x1A B):** `mov rax, [rcx+0x28]` / `mov [rcx+0x18], rdx`, then zeroes `[rcx+0x20]`, `[rax+0x10]` and `[rax+8]`, then `mov byte [rcx], 1`. Exact.
- **entered_from.** The raw byte scan finds two references, both in `001F4250`:
  - `001F42B7` (+0x67, cited): the free-slot path. It scans up to 15 slots of 0x30 bytes at `[rsi+0xA8]` for a zero first byte.
  - `001F4313` (+0xC3): the newly made handle, `00214FC0` on a 0x30-byte allocation.
  So the byte `+0` written as 1 is exactly the in-use flag that the scan tests.
- **Host fit.** `001F4250` is cited in a body row of the key-address table (line 266, §7). The body is the handle initialiser that both of its paths run. It fits, and it is cited on no other page (repo-wide grep).
- **Advisory (not a defect).** The row could name the second site, `001F4250` + 0xC3, and say that `[rcx]` is the in-use byte that the slot scan at `001F4290` tests.
- **Advisory (tool).** The applier's caller test is a substring test that the applied row satisfies by itself. Here the caller is also cited at line 266.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
