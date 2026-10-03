# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-vp8-codec-interface-and-its-control--ee-1003-6)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-VP8-CODEC-INTERFACE-AND-ITS-CONTR-529AF` · Package: `_index/candidates/opus-the-vp8-codec-interface-and-its-control--ee-1003-6/` · Page: `23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. The row was read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...):
  - `001260E7` exact: `cmp rax, 0` on argument 3 (`00126117` -> vertical-only arm `0012627F`) and on argument 4 (`00126141` -> horizontal-only arm `00126321`); 16 rows (`rcx` = argument 5 + 16 strides); each arm ends in a `movdqa` 16-byte aligned store (`00126267`, `00126310`, `00126388`); low/high halves unpacked, `pmullw` with the word filters, +64, `psraw 7`, `packuswb`; `xmm6`/`xmm7` restored. Constants read from the image: `03001000` and `03001060` are eight words of 64; `01CDC060` holds 32-byte word filters (index i: eight words 128-16i, then eight words 16i); `030011F0` holds 16-byte interleaved byte pairs (128-16i, 16i).
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
