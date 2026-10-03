# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-the-return-value-adapter-family-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-RETURN-VALUE-ADAPTER-FAMILY-HOMING` · Package: `_index/candidates/fable-the-return-value-adapter-family-homing-1003/` · Page: `24-Compiler-And-CRT-Runtime/Generated-Adapters/the-return-value-adapter-family.md` (commit b35f1958c; reviewed at HEAD 15ec1ea71, and the page is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 1 functions, 5 anchors`, `ALREADY` and `FAILS 0`. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 1 row and 5 anchors, `mode: homing`. Rejected 0, skipped 0, missing 0, corrections 0. The README count sentence ("1 staged with 5 anchors ... 0 ... 0 ... 0") matches. The row is on the page at line 913 (heading at line 907), byte for byte.
- Homing premise: `006B2A60` calls `00683B10`, which the page cites (3 citations).
- Semantic pass: **every row** was read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...).
  - **`006B2A60`: exact.**
    - It runs `mov rcx, rdx` / `call 00683B10` (`006B2A6C`) and keeps the incoming `r8` in `rbx`.
    - It then makes 16 dword moves from the returned pointer to `[rbx]`, covering `+0` (`006B2A74` / `006B2A76`) through `+0x3C` (`006B2ACC` / `006B2ACF`). From `+0x1C` on it reads through `rdx`, which holds the same pointer.
- Advisory (not a defect): the row states no return value, and the body leaves `eax` = the copied dword `+0x3C` (`006B2ACC`). On a page about return-value adapters a reader might want that stated, but omitting it makes no false claim.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
