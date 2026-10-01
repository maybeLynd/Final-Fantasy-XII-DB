# SWE2-AUDIT-SPEC review - GR-19: the drop gate asks the shared spot test

Task: `OPUS-REQ-AUDITSPEC-GR19-0930`. Package: `_index/candidates/gr19-drop-position-gate-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `gr19_drop_gate_check.py` re-run: FAILS 0 (D1-D5: `003377C0` spot test, group-exclusion via +0x138/+0x119 bytes, the `00337700` predicate chain, and the defeat body gating the drop roll on a non-zero answer at `00312588`-`00312597`).
- Consistent with SEM's earlier GR-19 review (`auditsem-review-gr19-gr11-0930`, ACCEPT-WITH-NARROWING) whose corrections are applied on the page.

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
