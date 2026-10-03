# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-vbf-archive-and-st2e-tables-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-VBF-ARCHIVE-AND-ST2E-TABLES-1003` · Package: `_index/candidates/fable-home-vbf-archive-and-st2e-tables-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md`

## SWE2-AUDIT-SPEC verdict: REJECT

All three sentences are exact, but all three rows are mis-homed.

- Their only caller is `0035C630`, a 38-byte UI routine in the battle-log path: `00253780` calls it. It lazily creates three UI objects: `[0209BE80]+0x10F80`, and two `00244F50` widgets stored at `02B47740` and `02B47758`.
- This page names `0035C630` only in its pass-22 UI crossing list (line 1226: "page-cited … `00253780` call UI bodies … `0035C630`"). OPUS's interior row for it (line 1302) itself calls every callee a "UI-layer helper".
- Nothing in the three bodies touches the VBF archive or the st2e tables.

So 3 of 3 rows fail host fit.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 3 functions, 13 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 1304, and the rows at lines 1310–1312 match `rows.json` byte for byte.
- **rows.json.** 3 rows, 13 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **`0028FF80` (0x58 B): exact.**
  - `cmp qword [[0209BE80]+0x10F80], 0` / `jne`.
  - Otherwise `0028FF9A call 00271420` (+0x1A) with `ecx` = 0x1D90, and the result is stored at `+0x10F80`. Then `0028FFBB call 002C63D0` (+0x3B) on the stored qword.
  - Both paths return `setne` of `+0x10F80`.
- **`003C98E0` (0x1F B): exact.** `cmp qword [02B47740], 0` / `jne ret`. Otherwise `r8d` = 0, `rdx` = `003C9A30`, `ecx` = 0xD8, and `003C98F9 jmp 00244F50` (+0x19). The callee is the widget factory.
- **`003CA280` (0x30 B): exact.** `mov rax, [02B47758]` / `jne` keeps it. Otherwise `00244F50(0xAA0, 003CA860, 0)` at +0x1F, and the result is stored at `02B47758`. It returns `rax`, which is the existing or the new pointer.
- **entered_from.** The raw byte scan finds one reference to each, all in `0035C630`: `0035C639` (+0x9), `0035C643` (+0x13) and `0035C63E` (+0xE). `0035C630` has one caller, `002537E6` = `00253780` + 0x66.
- **Host fit (the defect).**
  - `0035C630` is `call 0028E220` (a thunk to `002BDCE0`, the battle-log layout reader), then the three bodies, then `jmp 00290450` with `ecx` = 1.
  - On this page its only mentions are the pass-22 crossing sentence at line 1226 and OPUS's interior row at line 1302 ("calls four UI-layer helpers in order … then tail-jumps a 27-byte UI-layer body"). The page's own use of `00253780` is a constant-request table row (line 1157, `menumap_area.bin`). It is not this setup.
  - Elsewhere, the objects are UI state:
    - `02B47758` is a presentation object with flag dword `+0xA90`. `battle-runtime-mode-ladder.md` covers it at line 898 ("presentation objects (`0209E5C0`, `02B47730`/`58`/`60`)") and line 1466 (`003CA1E0`, which "clears bit 1 and sets bit 0 of its dword `+0xA90`"). The `0xAA0` object size fits a `+0xA90` field.
    - `the-resource-request-queue.md` line 390 has `003CA2F0`, which refreshes `[02B47758]`.
    - `0209BE80` is the per-frame update-gate singleton.
  - `16-UI/Message-Windows/the-message-window-layout-readers.md` names this exact chain: line 70, "`002BDCE0` (→`0028E220`→`0035C630`→`00253780`, the battle log)", and line 50, the battle-log family `00253780`.
- **Advisory (tool).** The applier's caller test is a substring test. A crossing-list mention and the interior row it spawned were enough to qualify this page.

## SWE2-AUDIT-SPEC repair

1. Remove the section from `vbf-archive-and-st2e-tables.md`: the heading at line 1304, its intro and the three rows.
2. Re-home the three rows, text unchanged, to `16-UI/Message-Windows/the-message-window-layout-readers.md`, entered from `0035C630` + 0x9 / + 0x13 / + 0xE. That page cites `0035C630` (line 70), so the applier passes there. A one-line lead naming `0035C630` as the battle-log setup that `00253780` + 0x66 runs would help.
3. Optionally cross-reference `battle-runtime-mode-ladder.md` lines 898 and 1466 for the `02B47758` object.
4. Regenerate `homing_applier.out` and correct the README.

Limits: static evidence only. A cloud draft plus FABLE's re-read is not independent review; this record is.
