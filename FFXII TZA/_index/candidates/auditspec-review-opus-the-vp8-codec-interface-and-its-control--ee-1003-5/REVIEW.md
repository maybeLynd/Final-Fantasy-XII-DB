# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-vp8-codec-interface-and-its-control--ee-1003-5)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-VP8-CODEC-INTERFACE-AND-ITS-CONTR-7AE9A` · Package: `_index/candidates/opus-the-vp8-codec-interface-and-its-control--ee-1003-5/` · Page: `23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. The row was read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...):
  - `001263AD` exact: nine `movdqu` rows (sign-extended stride) to an aligned stack block; `shl 5` filter addressing for arguments 3 and 4 with no zero-filter branch (always two-pass); horizontal pass over the low 8 bytes and their `psrldq 1` neighbours, `pmullw`/`paddw`/`psraw 7`; vertical pass `h_prev*V0 + h*V1 + 64`, `packuswb`, `movq` 8-byte rows at argument 5 (`0012652F cmp rdi, rcx` with `rcx` = argument 5 + 8 rows); `xmm6`/`xmm7` saved at entry and restored before `ret`. Constants read from the image: `03001000` and `03001060` are eight words of 64; `01CDC060` holds 32-byte word filters (index i: eight words 128-16i, then eight words 16i); `030011F0` holds 16-byte interleaved byte pairs (128-16i, 16i).
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
