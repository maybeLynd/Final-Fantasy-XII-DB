# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-post-processing-effect-catalogue-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-POST-PROCESSING-EFFECT-CATALOGUE-63A15` · Package: `_index/candidates/opus-the-post-processing-effect-catalogue-ee-1003/` · Page: `17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 3 functions, 15 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 3 row(s), 15 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `0070B780` exact: slot +0x1C0 of `[rcx+0x20]` with edx/r8/r9 untouched; fifth/sixth arguments at `[rsp+0xA0]`/`[rsp+0xA8]` after the 0x80-byte frame; `comiss 0, v` / `jbe` (NaN and v >= 0 keep v), byte +0xCCC choosing 0 or 1.0 (`01CEBBA8`); `+0x4C8` -> `+0x4D8`; `00722900(0x1F, 0, 0, 0, 0, 1.0, 0, 0, 0)` and `+0x4D8 = +0x4CC + n` for a non-negative n, `02EA1900` zeroed; `0075BFC0(o, +0x594, 0x7FFFFFFF)` after `[o+0xA0] = +0x4D8`; the +0x147 / +0x60 refusal with `006DF480(00D91070, 0x2728)` / `006DF480(00D91160)` behind the two `jb 1` tests and 0x80004005; `0075CD90` with all ten arguments as stated (the `cmovne` 0x30000/0x10000 on bit 0x10000000 of f); the negative-r logging (`00D91238`, 0x273D; `00D91280`, r, `0071B3C0(r)`); byte [rcx] = 1 and 0.
  - `0070BA00` exact: both refusals with their message pairs (`00D96DB0`/0x6D03, `00D96E40`; `00D97210`/0x6D1C, `00D97250`) and 0x80004005; `0070B780(rcx, 0, 0, xmm3 = [00902EF8], 0, -1)` with r9 untouched, result ignored; float bits read from the image: `00902EF8` = 0xFF7FFFFF; `cmovs` keeps a negative `0070B990(rcx, edx, 0)`, else 0.
  - `0078A240` exact: null r9 -> 0x80070057; `[r9]` zeroed; `007157A0(&A, rdx)`, `00716020(&A)`, `00717350(&A, &B, 0)`; `t` = `00790790(rdx, [rcx+0x30])`, null -> 0x80004005; `006DA880([01F3BA68], 0xE8, 00DAEFD0, 0x675, 0)` - string read from the image: '..\src\GPU\GPUInterfaceEffect.cpp'; `00789900(e, rcx)` result stored when e is non-null; `007897D0(e, t)` unchecked, `0078A4F0(t)`; the negative-r logging (`00DAF020`, 0x67C; `00DAF070`, r, `0071B3C0(r)`), else 0; `00715C70` on B then A.
- Advisory, not a defect: in `0070B780`, the path with byte +0x147 non-zero and qword +0x60 non-null is left implicit - the code (`0070B8A2 jne 0x70b915`) falls to the sign test on the `r` already held, which the sentence's closing clauses describe.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
