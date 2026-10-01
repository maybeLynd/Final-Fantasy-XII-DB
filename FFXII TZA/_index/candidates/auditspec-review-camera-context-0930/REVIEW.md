# SWE2-AUDIT-SPEC review - GR-11: camera contexts 0/1 read their 0xB0 pose blocks only at +0x00..+0x1F

Task: `OPUS-REQ-AUDITSPEC-GR11-0930`. Package: `_index/candidates/gr11-camera-context-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `gr11_check.py` re-run: FAILS 0 (K1-K8: pose-block read band, the tick blend `00259620`, reset `00259B30` field list, whole-context copies `002593D0`/`00259470`, first-level displacement bounds named as the recorded limit).

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
