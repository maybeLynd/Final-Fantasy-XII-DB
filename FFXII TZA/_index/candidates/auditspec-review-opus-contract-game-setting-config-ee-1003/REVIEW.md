# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-contract-game-setting-config-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-GAME-SETTING-CONFIG-EE-1003-B9BCC` · Package: `_index/candidates/opus-contract-game-setting-config-ee-1003/` · Page: `19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md` (commit 6a9eb7555)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 1 row, 5 anchors; rejected 0, missing 0; mode `ee`, no family (the family-declaring-page rule does not apply).
- Semantic pass: **every row** (1 of 1) read clause by clause against a capstone decode of the certified image (SHA256 73461D08...), extent `001E0100`-`001E0358` (600 B, one .pdata entry):
  - `001E0100`, stated exactly:
    - `rbx` = `rdx`, and it returns `rbx` on every path (`001E033D`).
    - The mode is dword `[rcx+0x70]`. `test dl, 2` / `jne` goes to the second test, and so does a null `[[b+0x40]]`.
    - The first case: `r8` = `[b+0x68]`, `cmp r8, r9; cmovb r8, r9` (unsigned max with `[[b+0x40]]`), minus `rdx` = `[[b+0x20]]`.
    - The second case: `test dl, 4` and a null `[[b+0x38]]`, then `movsxd r8, dword [[b+0x50]]` plus `[[b+0x38]]`, minus `[[b+0x18]]`.
    - The third case builds an empty stack string.
    - Each case initialises the stack string (cap 0xF, size 0, byte 0), calls `001A5630(stack, base, len)` (except the empty case), sets the result to cap 0xF, size 0 and byte 0, then calls `001A4C90(rbx, &stack)`.
    - Free: `cmp cap, 0x10; jb` skips. `cap+1 >= 0x1000` frees `[ptr-8]` (`001E0335 mov rcx, rax`). The checks are `test cl, 0x1f`, base `jb` below ptr, gap `jae 8` and `jbe 0x27`. Each failure calls `[008C2DA8]` = `_invalid_parameter_noinfo_noreturn` (IAT resolved from the import name).
    - The cookie is `01F44830`, checked by `00808C40`.
  - Anchors `001E0128` jne, `001E014E` cmovb, `001E016B` call, `001E0209` movsxd, `001E0338` call: all strictly inside with those mnemonics.
- The OPUS correction (no role names; base qword at pointer - 8 freed) is reflected in the applied sentence and matches `001E01BB`/`001E0335`.
- Limits hold: body statements only, static evidence. OPUS's re-read is not independent review; this record is.
