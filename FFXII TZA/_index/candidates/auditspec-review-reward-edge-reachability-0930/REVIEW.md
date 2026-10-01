# SWE2-AUDIT-SPEC review - GR-18: reward edge reachability (zero-count/missing descriptors absent)

Task: `OPUS-REQ-AUDITSPEC-GR18-0930`. Package: `_index/candidates/gr18-reward-edge-reachability-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `gr18_edges_check.py` re-run: FAILS 0 (E1: 162 files / 1146 unit rows, missing/zero/oob all 0; E2 the +0x1C2 byte writers `0030C496`/`0030C7BB`/`003AF80F`; E3 the 0xFF path bounded by chr_data's count 40).

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
