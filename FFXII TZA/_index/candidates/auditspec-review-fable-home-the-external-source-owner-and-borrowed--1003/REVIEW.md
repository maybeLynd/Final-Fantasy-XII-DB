# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-external-source-owner-and-borrowed--1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-EXTERNAL-SOURCE-OWNER-AND-BOR` · Package: `_index/candidates/fable-home-the-external-source-owner-and-borrowed--1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package is unmodified in the working tree) · Page: `02-Resource-And-Asset-Pipeline/the-external-source-owner-and-borrowed-view-lifetime.md`

## SWE2-AUDIT-SPEC verdict: REJECT

The sentence, site and anchors are exact. **The host is wrong.**

- `003AED50` initialises the character render record's embedded sub-object at `+0x550`. `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md` names that sub-object `embeddedTweenObj` (line 952), with the list link `+0x570` (its `+0x20`) and methods in the `003AExxx` family.
- This page cites the caller `0041FCF0` only for its borrowed-view bracket, the view taken at `0041FFA0` and ended at `0041FFF8` (line 176).
- The tween object has nothing to do with source ownership or view lifetime.

The only row is mis-homed.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 4 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 291 and the row (line 297) matches `rows.json` byte for byte.
- **rows.json.** 1 row, 4 anchors. Rejected 0, skipped 0, missing 0.
- **`003AED50` (0x17 B).** `xor eax, eax` / `mov dword [rcx], 1` / `mov [rcx+0x18], rax` / `mov [rcx+0x20], rax` / `mov [rcx+0x28], eax` / `mov [rcx+4], edx`. Exact.
- **entered_from.** `0041FCF0` + 0x210 = `0041FF00`, `call 003AED50`, with `rcx = rdi + 0x550` and `edx` = `movsx word [rdi]` (the record's id). It is the only caller (raw index). The surrounding code is the render-record setup (`+0x450`, `+0x4B7`, `+0x5D0..+0x5EC`, the `@FMC` section lookup `0x444C4640`).
- **Host fit: the defect.** This page (readiness BEHAVIORALLY UNDERSTOOD) reads `0041FCF0` only as an original consumer of the borrowed view. The body writes none of the owner, queue, bank or view state the page covers.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC repair

1. Remove the row from this package and from the section already on the page (the applier prints `ALREADY`). With no rows left, remove the section heading, its intro and the table header too.
2. Re-home the row **unchanged** on `17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md` (DOCUMENTED). That page reads `0041FCF0` as a writer of the record's own fields (lines 450-451), so the applier's caller check passes there. `the-character-render-record-array.md` names the field but does not cite `0041FCF0`; to home the row there, that page must cite the caller first. Optionally, add "(the record's `+0x550` `embeddedTweenObj`)" to the sentence.
