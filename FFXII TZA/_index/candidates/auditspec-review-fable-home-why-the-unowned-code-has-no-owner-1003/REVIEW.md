# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-why-the-unowned-code-has-no-owner-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-WHY-THE-UNOWNED-CODE-HAS-NO-OWNER` · Package: `_index/candidates/fable-home-why-the-unowned-code-has-no-owner-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `e0e99b7c6`; the package is unmodified in the working tree) · Page: `99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact against the bytes. The body tears down the name-keyed descriptor records that this page's "Skin" section reads: the `02E9FD60` list, `01F32110 + k*0x80` and the registrar `006D5A60`. Its caller `008B75A0` is cited in that same discussion, so the host fits.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 1535 and the row (line 1541) matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 0, skipped 0, missing 0.
- **`006D5940` (0xAE B), read in full.**
  - The walk starts at `02E9FD60`. The test is `lea rax, [rdx+8]` / `cmp rax, r9` with `r9 = rcx+8`, which is the same as node == `rcx`. On a hit, `mov rax, [rdx+8]` / `mov [rcx], rax` (the head cell or the predecessor's `+8`) / `mov [rdx+8], 0`.
  - Then two arms, each `shr eax, 0x1F` / `not al` / `test al, 1`. So the call runs when bit 31 is clear and the qword is non-null: `call 00584730` at +0x74 (`006D59B4`) for `+0x20`/`+0x28`, and at +0x96 (`006D59D6`) for `+0x10`/`+0x18`. Each arm then zeroes its qword and its dword on both paths.
  - Every clause holds. All 5 anchors are on these instructions.
- **entered_from.** `008B75A0` + 0x7 = `008B75A7`, a tail `jmp 006D5940` after `lea rcx, [01F32190]` (`SkinLocal`). The raw index gives 14 such two-instruction thunks, `008B75A0`-`008B75E0` and `008B7610`-`008B7690`. Their `rcx` values are the 5 `Skin*` records at `01F32110`-`01F32310` and the 9 records at `02E9FEF0`-`02EA0570`. That is exactly the 14 that `006C45F0` registers.
- **Host fit.** The page's §18 section establishes the registry: the list head `02E9FD60` (pseudo-code at line 1258), the five `Skin*` records (table at line 1238) and the 14 registrations. Line 1108 cites `008B75A0`-`008B75E0` against those records. The body removes a record from that list and frees its two arrays. Apart from `_index/ADDRESS-INDEX.md`, no other page cites it.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC advisories (not defects)

- Page line 1108 (the older §17 text) calls `008B75A0`-`008B75E0` "five per-record accessors". They are teardown thunks (`lea rcx, record` / `jmp 006D5940`), and there are 14 of them, which matches the 14 registrations. The owner may want to correct that sentence now that this row is on the page.
- The unlink loop in this body duplicates `006D6F90` (the unlink that `006C4750` uses). `006D6F90` is hosted on `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`, and a cross-reference would help.
