# SWE2-AUDIT-SPEC review - GR-8: per-unit 64-byte record touched only at +0x00..+0x1F

Task: `OPUS-REQ-AUDITSPEC-GR8-0930`. Package: `_index/candidates/gr8-unit-record-64-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `gr8_record_census_check.py` re-run: FAILS 0 (the `0208D480`/`0208DE80` + i*0x40 census; all touches confined to the +0x00..+0x1F band as recorded).

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
