# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-dyngeo-instance-family-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-DYNGEO-INSTANCE-FAMILY-1003` · Package: `_index/candidates/fable-home-dyngeo-instance-family-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `e0e99b7c6`; the package is unmodified in the working tree) · Page: `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`

## SWE2-AUDIT-SPEC verdict: REJECT

The four sentences, sites and anchors are exact. **All four hosts are wrong.** The rows belong on `17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md`. That page owns the caller `0062A0A0` as a body: "the GI command-stream interpreter", line 1770, with interior anchor `0062A493`. It already hosts four accessors of the same shape that `0062A0A0` calls from neighbouring arms. This page mentions `0062A0A0` once, as a caller of another accessor. The section heading ("called from this page's functions") is false for all four rows.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 4 functions, 20 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 857 and the four rows (lines 863-866) match `rows.json` byte for byte.
- **rows.json.** 4 rows, 20 anchors. Rejected 0, skipped 0, missing 0.
- **The bodies (all read in full; every clause holds).**
  - `00623EB0`: count `[rcx+0x18]` with `btr 0x1F`, and `cmp edx, eax` / `jae` returns 0 (unsigned). Count `<= 1` (`jbe`) uses the inline base `rcx+0x20`. The `cmove` null for count 0 cannot be reached past the bound check. Index ×2, then ×8, gives a 0x10 stride, field `+0`.
  - `00624040`: count `+0x30`, base `+0x38`, `shl rax, 6` gives 0x40, field `+8`.
  - `00624690`: count `+0x20`, `test byte [rcx+0x74], 1`, base `+0x28`, `lea rax, [r8+r8*8]` ×8 gives 0x48, field `+8`.
  - `006246E0`: count `+0x18`, `test byte [rcx+0x6C], 1`, base `+0x20`, stride 0x48, field `+8`.
- **entered_from.** `0062A0A0` + 0x45D (`0062A4FD`), + 0x276 (`0062A316`), + 0x363 (`0062A403`) and + 0x56D (`0062A60D`) are direct calls. `00624690` has a second site in the same caller, `0062A54A`. The raw index lists no caller outside `0062A0A0` for any of the four.
- **Host fit: the defect.**
  - This page cites `0062A0A0` once (line 749), inside the `00623FA0` paragraph: "`0062A0A0` and `006C8CA0` call it for the dyngeo records". It is not one of this page's functions, and nothing on the page reads its arms.
  - `gi-render-command-family.md` (AUDITED) reads `0062A0A0` as the interpreter. It "dispatches ... through the `006239C0`..`00624730` issue helpers", and all four bodies lie in that range.
  - That page also hosts `006241D0` and `00624730` (the counted 0x58 and 0x48 accessors "`006272C0` and `0062A0A0` share", lines 1814 and 1818), plus `00624180` and `00624220`. `00624730` has the same shape as `00624690` (count `+0x20`, `+0x74` bit 0, 0x48 stride, base `+0x28`); only the returned field differs (`+0x10` against `+8`).
  - In `0062A0A0` these calls sit beside the `00D54EF0` "Invalid constant buffer location" and `00D54E38` render-target diagnostics. That is GI command decoding, not dyngeo.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC repair

1. Remove the four rows from this package and from the section already on the page (the applier prints `ALREADY`). With no rows left, remove the section heading, its intro and the table header too.
2. Re-home all four rows **unchanged** (text, sites and anchors) on `17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md`, which cites `0062A0A0` in its own text, so the applier's caller check passes there. For `00624690`, the entered_from may also name the second site `0062A0A0` + 0x4AA (`0062A54A`).

## SWE2-AUDIT-SPEC advisories (not defects)

- This page's line 749 says `0062A0A0` calls `00623FA0` "for the dyngeo records". `0062A0A0` is the general GI interpreter, so the owner may want to narrow that phrase.
