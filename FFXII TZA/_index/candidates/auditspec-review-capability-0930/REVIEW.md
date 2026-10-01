# SWE2-AUDIT-SPEC review - capability-policy record (0023B040's bit-write arm)

Task: `OPUS-REQ-AUDITSPEC-CAPABILITY-0930`. Package: `_index/candidates/swe2struct-capability-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC (checker re-run on the certified image / installed assets, plus the named
spot-verified instructions). Reviewed the committed package as routed; no claims weakened.

## Independent verification

- `cap_policy.py` re-run: CHECKS 23, FAILS 0.
- Spot-verified: `0023B1C2 mov ecx,1` exactly (L11's claim that `0023B040` writes bit 1, and M1's consequence that the write never decides the `0026D6D0` call on actor `022C7FE0` since that branch keys bit 0).
- L11's direct-call closure claim (the six calls between the leader lookup and `0023B15E` have no indirect path to `00236A60`/`0023A570`) is mechanically re-checked by the control.

## Limits

Checker reproduction covers the package's mechanical claims; named anchors were additionally read off
the image directly. Prose-scope judgements (STALE/BOUNDARY/carried labelling) follow the batch's own
declared rule set and were not re-derived line by line.
