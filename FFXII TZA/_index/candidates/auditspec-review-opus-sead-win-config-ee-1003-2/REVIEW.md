# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-sead-win-config-ee-1003-2)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SEAD-WIN-CONFIG-EE-1003-2-9D1BB` · Package: `_index/candidates/opus-sead-win-config-ee-1003-2/` · Page: `18-Audio/Sound-Bank-And-Voice-Formats/sead-win-config.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. Output: `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`, exit 0. `git status` on the page and the package was clean afterwards (HEAD b5028e7e9).
- `rows.json`: 2 rows, 10 anchors. Rejected 0, skipped 0, missing 0, corrections 1. The correction holds: the sentence now states only the arguments passed to the IAT imports.
- Semantic pass: **every row** was read clause by clause against a full capstone listing of the certified image (SHA256 73461D08...), with IAT names resolved.
  - `007DD2B0` (162 B; leaf, no `.pdata`), exact and complete.
    - -1 goes to the qwords `+0x40/+0x48/+0x50/+0x58`.
    - `01CB81C8`→`+0` and `01CB81D8`→`+8`, both `.rdata` addresses stored by `lea` (`007DD2B8`).
    - Qword zeros: `+0x10/+0x18/+0x20/+0x28/+0x30/+0x60/+0x68/+0x84/+0x98/+0xA8/+0xB8/+0xC8/+0xD8`.
    - Dword zeros: `+0x38/+0xA0/+0xB0/+0xC0/+0xD0/+0xE0`.
    - There are no other stores and no calls, and `rax`=`rcx` (`007DD34E`).
  - `007DE8D0` (608 B), exact.
    - Config `+0x24`→`+0x70`, `+8`→`+0x60`, `+0x10`→`+0x68`.
    - Three `CreateEventExW` calls through IAT `008C2320` with (0,0,1,0x1F0003) go to `+0x40/+0x48/+0x50` (`007DE919`). A null result → 0x80004005 (`007DE928`).
    - `InitializeSRWLock` (`008C22F0`) is called on `+0xF0`, `+0x90` and `+0xE8`, in that order.
    - `CreateThread` (`008C21C8`, `007DE9B2`) gets `rcx`=0, `rdx`=0, `r8`=`007DD950`, `r9`=object, flag dword 4 and a null qword. Its result goes to `+0x58`.
    - A null handle stores -1, then calls `GetLastError` (`008C20A8`). If the code is >0 (`jle`), it becomes 0x80070000|low word. The message is `01CB81E0` through `0019C5D0`, with the newline and `jae 0x100` guard, then `008C2120` and `007A5570(2)`, and the code is returned.
    - `SetThreadPriority` (`008C21E0`, `007DEA45`) with config `+0x1C` returning 0 takes the same path with `01CB8180`.
    - `SetThreadAffinityMask` (`008C2200`) is skipped when `movsxd +0x20`==-1.
    - Config `+0/+4/+0x18/+0x1C/+0x24` and the sign-extended `+0x20` are copied.
    - `007DD9F0(obj)`: `js` → return. Otherwise `ResumeThread` (`008C2330`, `007DEAF6`) on `+0x58`, then `+0x38`=1, and the result is returned.

Limits: these are body statements read from static evidence. The draft and OPUS's re-read are not independent review; this record is.
