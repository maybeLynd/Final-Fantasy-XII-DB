# SWE2-AUDIT-SPEC review - registry slot 0x02EBF200 (field +0x11C raw pack index)

Task: `OPUS-REQ-AUDITSPEC-SLOT-200-1001`. Package: `_index/candidates/opus-registry-slot-200-1001/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `slot200_check.py` re-run: FAILS 0 (S1-S3 plus controls: `00237630`/`00238260`/`00328990` bound cl/r8d <= 0xB).
- `00236C30` verified head: computes `movsxd` indices off `rcx` and stores into the `02EBF1xx` registry band, consistent with the write-once/no-reader claim.

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
