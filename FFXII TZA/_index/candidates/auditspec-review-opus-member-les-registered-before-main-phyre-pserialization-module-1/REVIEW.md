# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PSerialization module (opus-member-les-registered-before-main-phyre-pserialization-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-LES-REGISTERED-BEFORE-MAIN-PHYRE-PSE` · Package: `_index/candidates/opus-member-les-registered-before-main-phyre-pserialization-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 399ce7caf)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 18 functions, 77 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 18 rows, mode `member`, family `Phyre PSerialization module`; rejected 0, skipped 0, missing 0. There are six correction entries over four functions (`005A0120` is listed three times).
- Corrections checked at the bytes, all right:
  - `0059D4B0`: `test rcx,rcx; jle` at 0059D4FD/0059D500 is signed, so -1 does not reach `001D6CA0`.
  - `0059FD10`: `test; jle` at 0059FD77/0059FD7A is signed.
  - `005A0120`: `js` at 005A01DB and `cmp; jge` at 005A01E3/005A01E6 are signed. `div r8d` at 005A01ED is unsigned. `&p` = `[rsp+0x40]` is passed as `r8`, and 005A021B re-reads `[rsp+0x40]` after the call before storing it to `[rcx+0x30]`.
  - `005A0250`: `test; jle` at 005A02A1/005A02A4 is signed.
- Semantic pass: **all 18 rows** were read clause by clause against `disr.py` output of the certified image. Import thunks were resolved through the IAT: 008C2140 `ReadFile`, 008C2150 `SetFilePointer`, 008C2158 `WriteFile`. Names and strings were resolved from `.rdata`. All 18 are exact:
  - `001D6CE0` (argument shuffle into `0020C180(x, rcx, edx, r8d)`), `0020C180` (`or eax,-1` on a null `rdx`), `00217AD0` (origins 0/1/2; the clamp is an unsigned `jbe`, as the row says).
  - `005981B0`, `00598210`, `00598280`, `005982F0`. In the last three, `not al; test al,1; je` skips the buffer free when bit 0 is SET. Bit 4 of `edx` selects `0016D6A0(rcx, 0x18 / 0x50)` over `00584730(rcx)`.
  - `00598C50`: names `m_indexBufferSize` / `m_vertexBufferSize` / `m_maxTextureBufferSize` at 00D26D08 / 00D26D20 / 00D26D38; `n` 0x48/0x4C/0x50 at `[rsp+0x20]`, zeros at `+0x28/+0x30/+0x38`; tail `jmp 00639450`.
  - `0059D4B0`: the first return is 0 because `eax` still holds the null qword `[rcx+0x30]`. `ReadFile`'s count slot is pre-zeroed (0059D4CA), and `rdx`/`r8` pass through to `001D6CA0`.
  - `0059D550`, `0059D920` (returns `al`), `0059EE10` (`sete al` on `n`; the free / store happens when `rdx` is null or `s` is non-null), `0059F490`, `0059FDA0`.
  - `0059FD10`: backend arguments `00215220(q, edx, 1)`, `SetFilePointer(h, edx, 0, 1)`, `001D6CE0(q, edx, 1)`. `r8d` is pre-set to -1, so with no backend the `cmovne` returns 0.
  - `0059FE20`: the walk finds the head on its first step, so the head is unlinked and its next link zeroed. Release order: `+0x70`/`+0x68`, then `00598040(n+0x18)`, then `+0x10`/`+0x8`, then the node. Then `0067F580(01F2CDA0)` and the two byte clears.
  - `005A0120`: fifth argument at `[rsp+0x60]` (0x38 of frame + 0x28); `b` uses `movsxd` of `[t+0xF8]`; for `e` not found, `rcx`/`rdx` = 0 give the `[t+0x38]` / `[t+0xF8]` fallbacks; call `0059BED0(rsi=s, e, &p, a mod w, [rsp+0x20] = qword [rcx+0x28])`.
  - `005A0250` (returns `al`; `WriteFile` result compared with 1 by `sete`).
- Advisory, not a defect: in `005A0250` the format string at 00D27970 is `"can't write to file by file cache (%d)!\n"`. The row quotes it without the trailing newline. Behaviour is unaffected.
- Limits hold: body statements only, static evidence. The drafting agent, the second local reader and OPUS's re-read are not independent review; this record is.
- Batch-wide sentence, not this record's rows: the README's "262 stood, 10 clauses in 8 functions were corrected" (shared by all 11 records of 399ce7caf) does not match the `rows.json` corrections, which total 12 entries in 10 functions across the 11 records. The narrowing is recorded once, in `auditspec-review-opus-phyre-members-399ce7caf`.
