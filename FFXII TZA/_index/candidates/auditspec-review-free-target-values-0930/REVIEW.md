# SWE2-AUDIT-SPEC review - GR-2: free-target type values from the script census

Task: `OPUS-REQ-AUDITSPEC-GR2-0930`. Package: `_index/candidates/gr2-free-target-values-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `gr2_check.py` re-run: FAILS 0 (C1-C7); `gr2_census.py` re-run reproduces the per-type script populations (type 3 = 23 distinct scripts headlined by disp_tama*, type 5 = the TWN/SND/BASH actors, type 6 = the three boss-fight scripts - matching the record and SEM's C1-C5 narrowing which this batch's page edit already incorporated).
- Note: this GR record was itself the subject of `auditsem-review-gr2-0930` (ACCEPT-WITH-NARROWING); the recorded corrections stand and are incorporated upstream in `opus-dd-restatus-20-1001`.

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
