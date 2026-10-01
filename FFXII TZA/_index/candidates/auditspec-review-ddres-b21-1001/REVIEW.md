# SWE2-AUDIT-SPEC review - DD residue batch 21: shop table + spawn placement

Task: `OPUS-REQ-AUDITSPEC-STRUCT-B21-1001`. Package: `_index/candidates/swe2struct-ddres-b21-1001/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC (checker re-run on the certified image / installed assets, plus the named
spot-verified instructions). Reviewed the committed package as routed; no claims weakened.

## Independent verification

- `b21_checks.py` re-run: PASSES 78, FAILS 0 (incl. N1: both pages carry the expected note counts, stay pure CRLF, and have no open box).
- The M1-M6 caller-chain answer (the `0x3E0`-byte child page is the location map's kind-0 marker page via `002BA310` <- `002BAF80`) is re-derived by the control; additive notes only, no strikes.

## Limits

Checker reproduction covers the package's mechanical claims; named anchors were additionally read off
the image directly. Prose-scope judgements (STALE/BOUNDARY/carried labelling) follow the batch's own
declared rule set and were not re-derived line by line.
