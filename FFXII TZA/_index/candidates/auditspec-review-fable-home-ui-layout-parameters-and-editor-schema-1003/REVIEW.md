# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-ui-layout-parameters-and-editor-schema-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-UI-LAYOUT-PARAMETERS-AND-EDITOR-S` · Package: `_index/candidates/fable-home-ui-layout-parameters-and-editor-schema-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package is unmodified in the working tree) · Page: `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 4 rows are exact against the bytes. Each caller is a layout reader or widget body that this page reads, and two of the bodies touch objects the page discusses (`020927F0` and `[02B62D88]+0xC0`).

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 4 functions, 18 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 1810 and the four rows (lines 1816-1819) match `rows.json` byte for byte.
- **rows.json.** 4 rows, 18 anchors. Rejected 0, skipped 0, missing 0.
- **`00251D20` (0x24 B).** The null path returns the loaded `rax`, which is 0. Then `test byte [rax+0xE8], 1`, which selects `movsx eax, word [rax+0xE6]` or `mov eax, 2`. Exact.
- **`00270880` (0x30 B).** Four `mulss` by `xmm2` from `[rdx+0..0xC]` into `[rcx+0..0xC]`. Exact.
- **`002C5660` (0x89 B).**
  - The loop is `00282DF0(i)` at +0x12 for i = 0..8, with `cmp word [rax+0x60], 0` / `jl` (signed, skip negative) / `or edi, [rax+0x44]`. A zero mask goes to `movsx eax, bp` = 0.
  - Then a 32-step `rol ebx, 1` bit walk: `0035D330(0x1A, i)` at +0x4B, `002B3050(0, [rax+0x10], &w, &x)`, `cmp word w, bp` / `cmovg bp, w`.
  - Exact.
- **`00404D40` (0x2C B).** The null checks on `02B62D88` and `+0xC0` come first, then `cmp ecx, 2` / `jge` (signed) and `movsxd` / `[rdx + rax*8 + 0xC8]`. Exact. A negative `ecx` passes the signed check, and "below 2 (signed compare)" says so.
- **entered_from.**
  - `003EEEC0` + 0x106 = `003EEFC6`.
  - `0028D260` + 0x1AC = `0028D40C`. A second caller is `0028D460` + 0x31D (`0028D77D`).
  - `002C59D0` + 0xEF = `002C5ABF`.
  - `00405310` + 0x302 = `00405612`.
  - Each is the body's only caller apart from the noted second one (raw index).
- **Host fit.**
  - `003EEEC0` has its own homed row on this page (line 1807), and the `020927F0` record's `+0xE4`/`+0xE6`/`+0xE8` fields are read at lines 341 and 1740.
  - `002C59D0` is the page's size-compute (lines 869, 889), and this body measures the widest class-`0x1A` text.
  - `00405310` runs the boss-gauge draw (line 1604), and the page reads the two-slot array at `[02B62D88] + 0xC0` (line 985).
  - `0028D260` is named with `0028D460` as a caller of the layout's range search `0028CB90` (line 1672). `0028D460` is the `2DSideCursorCenter…` reader (lines 217, 328).
  - Apart from `_index/ADDRESS-INDEX.md` and register text, no other page cites these bodies.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC advisories (not defects)

- `00270880`: this page reads `0028D260` only as a co-caller of `0028CB90`. The entered_from could instead name the other site, `0028D460` + 0x31D, whose reader role the page states. The 4-float scale is generic. It is homed by its callers, which is fine.
