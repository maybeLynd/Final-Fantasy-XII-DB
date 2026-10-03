# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-vp8-codec-interface-and-its-control--ee-1003-7)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-VP8-CODEC-INTERFACE-AND-ITS-CONTR-48ACF` · Package: `_index/candidates/opus-the-vp8-codec-interface-and-its-control--ee-1003-7/` · Page: `23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. The row was read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...):
  - `00126E10` exact: the same two zero tests (`00126E40`, `00126E66`); `shl 4` filter addressing into `030011F0`; `punpcklbw` of each byte with its right neighbour, `pmaddubsw`, +64 (`03001060`), `psraw 7`, `packuswb`; the vertical-only arm stores two rows per iteration (`00126FFE` `[rdi]`, `0012701C` `[rdi+rdx]`), the horizontal-only arm two (`001270B3`, `001270DD`), the two-pass loop one (`00126F56`); all `movdqa`; `xmm6`/`xmm7` restored. Constants read from the image: `03001000` and `03001060` are eight words of 64; `01CDC060` holds 32-byte word filters (index i: eight words 128-16i, then eight words 16i); `030011F0` holds 16-byte interleaved byte pairs (128-16i, 16i).
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
