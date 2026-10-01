# SWE2-AUDIT-SPEC review - residue batch 3 (MS-4 record + section-8 copy readers)

Task: `OPUS-REQ-AUDITSPEC-RESIDUE3-0930`. Package: `_index/candidates/swe2struct-residue3-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `residue3_check.py` re-run: FAILS 0 (P1-P9 section-8 copy readers via the four +0x300 accessors; G1-G9 the `0055CD40` UI-state byte; W7-W9 the container's link-call closure and masked-xor persistence).
- Spot: W8's census finds exactly `00292ACD`/`003CB85F` for id 14, consistent with ms4_check's M5 senders (`00292AB2`, `003CB835` built sends).

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
