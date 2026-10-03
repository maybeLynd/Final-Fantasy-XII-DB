# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-vp8-codec-interface-and-its-control--ee-1003-8)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-VP8-CODEC-INTERFACE-AND-ITS-CONTR-2B5D0` · Package: `_index/candidates/opus-the-vp8-codec-interface-and-its-control--ee-1003-8/` · Page: `23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. The row was read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...):
  - `00127104` exact: nine-row copy to a realigned stack block (`and rsp, -16`, the old `rsp` pushed and popped at `001274B6`); zero tests at `001271BC`/`001271DD`; the vertical-only arm is unrolled to eight `movq` stores (`00127352`-`001273D0`), the horizontal-only arm stores four rows per iteration (`00127485`-`0012749F`), the two-pass loop one `movq` per row (`0012726F`); `pmaddubsw` with `030011F0` pairs, +64, `psraw 7`, `packuswb`; `xmm6`/`xmm7` restored. Constants read from the image: `03001000` and `03001060` are eight words of 64; `01CDC060` holds 32-byte word filters (index i: eight words 128-16i, then eight words 16i); `030011F0` holds 16-byte interleaved byte pairs (128-16i, 16i).
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
