# SWE2-AUDIT-SPEC review - GR-12: actions 0x9C/0x9D are effect-free category-13 rows

Task: `OPUS-REQ-AUDITSPEC-GR12-0930`. Package: `_index/candidates/gr12-actions-9c-9d-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `gr12_actions_check.py` re-run: FAILS 0 (S1-S18: the 0xFFFF handle/dead-preset analysis, the 50050-record order census showing no 0x9B/0x9C/0x9D, the order-set cascade `003014C0`/`00305CC0`).

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
