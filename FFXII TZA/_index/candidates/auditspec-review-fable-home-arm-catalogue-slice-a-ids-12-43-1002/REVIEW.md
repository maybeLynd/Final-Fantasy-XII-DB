# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-arm-catalogue-slice-a-ids-12-43-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-ARM-CATALOGUE-SLICE-A-IDS-12-43-1` · Package: `_index/candidates/fable-home-arm-catalogue-slice-a-ids-12-43-1002/` · Page: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-A-ids-12-43.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 2 functions, 10 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 2 rows, 10 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **all 2 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `001BBF40`: `edi = 0x20` countdown over qwords from `rcx+0xA0`; `00183720` only on non-null; `memset(rcx+0xA0, 0, 0x100)`, then a tail `memset(rcx+0x1A0, 0, 0x100)`. Exact. Host: `001BC190` is cited as a reader of the page's *Use normal map* field, which is acceptable.
- `001DE180`: `movsxd rdx, [[rcx-0x90]+4]` is read twice. `00901028` is stored at `rcx-0x90+d` and `d-0x90` at `rcx-0x94+d`; `00900F20` goes to `rcx-0x80`; then `001DF8C0(rcx-0x80)`, the IAT call `[008C27A0](rcx-0x80)` and the IAT tail `[008C2548](rcx-0x78)`. The text is exact.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **`001DE180` (entered from `001DE5D0`): host-fit defect.** The page cites `001DE5D0` (`GameSettingConfig_ParseText`) once, in *"Save_Load_Settings - MECHANICAL ... `0017D280` ... is called by `001DE5D0`/`001DF350` of that layer; the same string helper reused, not a save relationship of the console"*. The body is a stream-object teardown run from the settings parser (site `001DECF0`), and it has nothing to do with console arms. The row's sentence, site and anchors are exact; only its host is wrong, and the section heading (*"called from this page's functions"*) is false for it, because this page says the caller is not one of its functions.
  - **Repair:** remove the `001DE180` row from this package (and from the section already on the page: the applier prints `ALREADY`), and re-home it unchanged on `19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`, which cites `001DE5D0` as `GameSettingConfig_ParseText` (CONTRACT-game-setting-config.md lists it among its entries).
- The `001BBF40` row is exact and stays.
