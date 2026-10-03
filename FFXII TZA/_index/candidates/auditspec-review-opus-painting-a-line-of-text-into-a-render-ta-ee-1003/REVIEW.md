# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-painting-a-line-of-text-into-a-render-ta-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-PAINTING-A-LINE-OF-TEXT-INTO-A-RENDER-CBBE5` · Package: `_index/candidates/opus-painting-a-line-of-text-into-a-render-ta-ee-1003/` · Page: `99-Unresolved-Residual/Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md` (commit 6a9eb7555)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 1 row, 5 anchors; rejected 0, missing 0; mode `ee`, no family (the family-declaring-page rule does not apply).
- Semantic pass: **every row** (1 of 1) read clause by clause against a capstone decode of the certified image (SHA256 73461D08...), extent `00200BF0`-`00200E51` (609 B, one .pdata entry):
  - `00200BF0`, stated exactly:
    - Open: `F` = `rsp+0x40`, `00597970(&F, [rdx], r8b=1)`, and `r9` is never written in the body. `00597970`'s prologue uses only `rcx`, `rdx` and `r8b`.
    - Size check: `[rsp+0x5c]` (`F+0x1C`) is tested against -1, then `sub` `[rsp+0x58]` (`F+0x18`), `test`/`jle` (signed).
    - Read: `00210EC0(movsxd(n+1))`, then `0059F4A0(rsp+0x60 = &F+0x20, buf, n)` and `buf[n]` = 0. `strlen` follows, then `001A5630` into `s` (`rbp+0x90`).
    - Stream: the vbtables `00900FA8`/`00900FB0` (not named in the sentence; no claim is lost) and the IAT `008C25E0` = `basic_ios` ctor and `008C2520` = `basic_iostream` ctor (import names resolved). `00900FA0` is stored at the `basic_ios` subobject; its RTTI is `basic_stringstream<char>`, which supports "std::stringstream". `008C2798` = `basic_streambuf` ctor, then `00900F20` (RTTI `basic_stringbuf<char>`). `001DF7D0(buf obj, s data, s size, 0)`.
    - Cleanup of `s`: the free uses the same `0x1F`/base/8/0x27 checks that call `_invalid_parameter_noinfo_noreturn` `[008C2DA8]`, then `s` is reset to cap 0xF, size 0, byte 0.
    - `00200E60(rsi = entry rcx, rbp-0x70)` and `00210EB0(buf)`. The stream is destroyed with `001DE280(rbp+0x28)`, then `[008C25E8]` = `basic_ios` dtor.
    - The guard failures branch to `00200E1A`, where both paths call `0059BD40(&F)` and `00598100(&F)`. The cookie is `01F44830`, checked by `00808C40`.
  - Anchors `00200C3B` call, `00200C54` jle, `00200C73` call, `00200D6F` call, `00200DF9` call: all strictly inside with those mnemonics.
- The OPUS correction (three register arguments; no invented fourth argument) is reflected in the applied sentence and matches the bytes.
- Limits hold: body statements only, static evidence. OPUS's re-read is not independent review; this record is.
