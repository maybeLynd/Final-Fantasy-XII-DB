# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-the-battle-unit-field-map-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-BATTLE-UNIT-FIELD-MAP-HOMING-1003` · Package: `_index/candidates/fable-the-battle-unit-field-map-homing-1003/` · Page: `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` (commit b35f1958c; reviewed at HEAD 15ec1ea71, and the page is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 2 functions, 10 anchors`, `ALREADY` and `FAILS 0`. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 2 rows and 10 anchors, `mode: homing`. Rejected 0, skipped 0, missing 0, and 1 correction (`0026BE00`: the tail jump is conditional on the re-test). The README count sentence ("2 staged with 10 anchors ... 0 ... 0 ... 0") matches. Both rows are on the page at lines 1949-1950 (heading at line 1943), byte for byte.
- Homing premise: `00239370` calls `0026BB50`, and `0026BE00` tail-jumps `002E86B0`. Each of those leads its own row on the page.
- Semantic pass: **every row** was read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...).
  - **`00239370`: exact.**
    - With `xmm6` = 0.0, it tests `comiss xmm3` (`00239386`), then `xmm8` = the incoming `xmm2` (`002393A0`), then `xmm7` = the incoming `xmm1` (`002393B2`), each followed by `jb`. Below or unordered skips, so a NaN skips.
    - The calls are `0026BB50(rcx, xmm3)` (`0023939B`), +0x3D = `0026BA00(rcx, xmm2)` (`002393AD`) and +0x4D = `0026B940(rcx, xmm1)` (`002393BD`). Each passes the saved `rcx`, and the float goes in `xmm1`.
  - **`0026BE00`: exact.**
    - It takes `(byte [rcx+3] & 0xE0) == 0x60` (`0026BE06`), otherwise returns, and stores `xmm1` at float `[qword rcx+0xB8] + 0xE4` (`0026BE11`).
    - It re-tests (`0026BE1F` / `jne 0026BE37` ret), reloads the float (`0026BE2A`) and runs `jmp 002E86B0` (`0026BE32`), a tail jump with `rcx` unchanged.
    - FABLE's correction (conditional tail) is right.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
