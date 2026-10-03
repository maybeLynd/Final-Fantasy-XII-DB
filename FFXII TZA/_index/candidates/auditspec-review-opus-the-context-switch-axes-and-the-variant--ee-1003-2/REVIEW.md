# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-context-switch-axes-and-the-variant--ee-1003-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-CONTEXT-SWITCH-AXES-AND-THE-VARIA-C1C7C` · Package: `_index/candidates/opus-the-context-switch-axes-and-the-variant--ee-1003-2/` · Page: `22-Middleware-PhyreEngine/Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. The row was read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...):
  - `006B9630` exact: `006B8DE0(L, S, rdx, r8d)` (`006B9678`); `lea r12d, [rax*2+1]`; reallocation only when dword `[r9]` differs: `0017D260(m*8, 8)`, null -> 0xD, the zeroing loop, old entries freed through `00584730` only when bit 0 is clear, the old array freed only when it differs, is non-null and bit 31 of the count is clear; `[r9+8]`/`[r9]` stores. Strings read from the image: `00D81068` = '-D', `00D81070` = '-DLIGHTTYPE_', `00D81080` = '-DSHADOWTYPE_', `01CEBB4C` = '='. Slot 0 = '-D' + `[rcx+8]` + '=' + n (`0067AD60`/`0067AF00`/`0067AEA0`), heap copy `0017D260(len+1, 2)` + `memcpy` (`00861EBA`), null for an empty string, a failed copy -> 0xD (`006B97BA`); per i: `006BFC40(L[i])` (null skips the value append, `006B9821`), `006C2300(S[i])` only when S[i] is non-zero (`006B98D0`); old slot strings freed when bit 0 is clear; `006BA590(r9, filled)` (`006B99E6`); cookie `01F44830` / `00808C40`.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
