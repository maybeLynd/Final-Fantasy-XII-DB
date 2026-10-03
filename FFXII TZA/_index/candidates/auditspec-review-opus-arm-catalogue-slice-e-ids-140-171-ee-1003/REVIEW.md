# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-arm-catalogue-slice-e-ids-140-171-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-ARM-CATALOGUE-SLICE-E-IDS-140-171-EE-3C372` · Package: `_index/candidates/opus-arm-catalogue-slice-e-ids-140-171-ee-1003/` · Page: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-E-ids-140-171.md` (commit 6a9eb7555)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 1 row, 5 anchors; rejected 0, missing 0; mode `ee`, no family (the family-declaring-page rule does not apply).
- Semantic pass: **every row** (1 of 1) read clause by clause against a capstone decode of the certified image (SHA256 73461D08...), extent `001DC9D0`-`001DCB88` (440 B, one .pdata entry):
  - `001DC9D0` exact: `o` = `rcx` (`rdi`); two `memset` (`00861EC0`) calls zero 0x100 bytes at `rsp+0x60` (`A`) and `rsp+0x160` (`B`). `e` = qword `[o+0x78]` + dword `[o+0x48]`*0x140 (`lea rdx,[rax+rax*4]; shl rdx,6`). The `B` format is `001A1E40(B, 00900950 '(%ws)' .rdata, [e+0x138] + (dword [o+0x60]-1)*0x60)`. `dec eax` then `lea r8,[rax+rax*2]; shl r8,5` zero-extends, so the stated 2^32 - 1 wrap is right. The 0x5C/0x2E strip loop at `001DCA80` compacts `B` in place and writes the terminator. `V` = `rsp+0x28` (`0020D2B0`). `0020D9F0(&V, dword [e+0x104], A)`, then `test al, al` / `jne` at `001DCACD`: on 0 it formats `00900958 '%ws'` with `e` into `A`. `008F80F0 '%s%s'` gives `(A, A, B)`. The copy loop `001DCB20` includes the terminator into `rdx` (`rbx`). `[rsp+0x38]` (`V+0x10`) null-test, then `001CD050(&V+0x10, it, ([rsp+0x48] - it)/12)` by `0x2AAAAAAAAAAAAAAB` `imul`/`sar 1`/sign add (signed, truncating). The cookie is `01F44830` (.data), checked by `00808C40`. No return value is claimed and none is set.
  - Anchors `001DCA5C` call, `001DCA83` cmp, `001DCAC8` call, `001DCB0A` call, `001DCB62` call: all strictly inside the extent with those mnemonics.
- Both OPUS corrections (32-bit zero-extended decrement; byte result in `al`) are present in the applied sentence and match the bytes.
- Limits hold: body statements only, static evidence. OPUS's re-read is not independent review; this record is.
