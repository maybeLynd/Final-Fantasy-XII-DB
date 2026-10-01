# SWE2-AUDIT-SPEC review - GR-9: subgroup byte +0x6B5 set only from the committed order id

Task: `OPUS-REQ-AUDITSPEC-GR9-0930`. Package: `_index/candidates/gr9-order-subgroup-entry-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `gr9_subgroup_check.py` re-run: FAILS 0 (K1-K5: `+0x6B5` non-zero only from the committed order id at `002FE0BB`; `+0x714`'s run-time id source identified).

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
