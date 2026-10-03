# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-the-record-00329220-builds-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-RECORD-00329220-BUILDS-HOMING-1003` · Package: `_index/candidates/fable-the-record-00329220-builds-homing-1003/` · Page: `04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md` (commit b35f1958c; reviewed at HEAD 15ec1ea71, and the page is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 1 functions, 4 anchors`, `ALREADY` and `FAILS 0`. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 1 row and 4 anchors, `mode: homing`. Rejected 0, skipped 0, missing 0, corrections 0. The README count sentence ("1 staged with 4 anchors ... 0 ... 0 ... 0") matches. The row is on the page at line 572 (heading at line 566), byte for byte.
- Homing premise: `0035D5C0` calls `00273BA0`, which the page cites (2 citations).
- Semantic pass: **every row** was read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...).
  - **`0035D5C0`: exact.**
    - `test dword [022C83E8], 0x200` (`0035D5C4`) is followed by `jne` to the epilogue (`0035D5CE`).
    - When the bit is clear, `lea rcx, [022C8B08]` / `call 00273BA0` (`0035D5D7`) runs, then `or dword [022C83E8], 0x200` (`0035D5DC`).
    - There is no other path.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
