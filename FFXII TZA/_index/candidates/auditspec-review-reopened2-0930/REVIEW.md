# SWE2-AUDIT-SPEC review - REOPENED batch 2: interpreter dispatch + wait polarity falsification

Task: `OPUS-REQ-AUDITSPEC-REOPENED2-0930`. Package: `_index/candidates/swe2contract-reopened2-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `falsify_interp_dispatch.py` re-run: FAILS 0 (I0-I15: the 100-entry computed-goto dispatch of `00261DF8` - extent/count, signed `lea` rebase, bound+default, all 100 targets inside the body on instruction starts, 92 distinct with the three shared groups; plus three corrupted-table controls each caught).
- `falsify_wait_polarity.py` re-run: FAILS 0 (W0-W13: SECTION-12 wait polarity).
- The page restatements (RC-16 struck to FABLE's adjudicated wording; the regI1 'not a decoder gap but not shown to run' narrowing) match the cited adjudication record.

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
