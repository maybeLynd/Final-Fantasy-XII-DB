# SWE2-AUDIT-SPEC review: OPUS homing rows (opus-the-lua-loader-and-what-it-accepts-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-LUA-LOADER-AND-WHAT-IT-ACCEPTS-HOMING-1` · Package: `_index/candidates/opus-the-lua-loader-and-what-it-accepts-homing-1002/` · Page: `23-Third-Party-Libraries/Lua-Core/the-lua-loader-and-what-it-accepts.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh (verify mode) -> exit 0, `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0`.
- `rows.json`: 1 row, 5 anchors; rejected 0, missing 0.
- **Entry.** The row states none, and the class file lists no direct callers. The raw census agrees: no branch site reaches the body. Its only reference is the `.rdata` qword `00D58A30` = `0063C450`, a pointer-table entry, which fits "reached by table or pointer dispatch".
- **Host fit.** The body calls `008113D0` and `00811130`, and the page documents both, so the homing premise holds.
- **Semantic pass, all 1 row (68 B).** Exact.
  - `0063C468 or edx, -1` gives `008113D0(rdx, -1)`.
  - `setne bl` at `0063C47A` keeps the flags from `test eax,eax`; the interleaved `mov` instructions leave the flags alone.
  - `00811130(rdx, 0xFFFFFFFE = -2)`.
  - `0063C482 mov byte ptr [rsi], bl`, with `rsi` = incoming `r8`.
