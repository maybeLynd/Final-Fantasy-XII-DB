# SWE2-AUDIT-SPEC review - GR-10: camera record 2 is the field camera

Task: `OPUS-REQ-AUDITSPEC-GR10-0930`. Package: `_index/candidates/gr10-camera-record-2-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `gr10_camera_check.py` re-run: FAILS 0 (C1-C5: record 2 set each tick by `00358F90`; shown whenever no record 3-7 is active; kind setter callers enumerated with record2->kind1 only at `0035908F`).
- Spot-verified `0035908F` = tail `jmp 0025A500` out of `00358F90`'s epilogue - the kind-1 commit on every path as claimed.

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
