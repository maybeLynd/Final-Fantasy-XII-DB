# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-font-painters-public-api-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-FONT-PAINTERS-PUBLIC-API-1003` · Package: `_index/candidates/fable-home-the-font-painters-public-api-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `99-Unresolved-Residual/Glyph-Run-Rendering/the-font-painters-public-api.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact. The body is the tail of `0017FC50`, one of the band entry points that this page's OPUS corrections add to the public surface.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 374, and the row at line 380 matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **`001E9380` (0x33 B):** `lea rbx, [rcx+0x1500]` / `mov edi, 0x40`, then a loop of `mov rcx, rbx` / `001E9399 call 00213090` (+0x19) / `add rbx, 0x38` / `sub rdi, 1` / `jne`. That is 0x40 elements of 0x38 bytes from `rcx+0x1500`. Exact.
- **entered_from.** The raw byte scan (E8/E9, `0F 8x`, absolute pointers) finds one reference: `0017FC60 jmp 001E9380` = `0017FC50` + 0x10. `0017FC50` is `call 001B5FA0` (the painter singleton), then `mov rcx, rax` and the tail jump.
- **Host fit.**
  - `0017FC50` is cited on this page in two corrections, at line 31 ("a rel32 sweep finds 25 call sites of `001B5FA0` … including `0017FC00`, `0017FC50` and `0017FC70`") and at line 76.
  - Both corrections name it as a member of the public entry band. They do not merely list it. The body is that entry's whole effect on the painter object. It fits.
  - `001E9380` is cited on no other page (repo-wide grep).
- **Advisory (not a defect).** The §2 table still lacks `0017FC50` (line 76 says so). With this row, the entry's effect is now on the page, and a one-line table entry would close the gap.
- **Advisory (tool).** The applier's caller test is a substring test that the applied row satisfies by itself. Here the caller is also cited at lines 31 and 76.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
