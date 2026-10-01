# SWE2-AUDIT-SPEC review - DD residue batch 10: six pages (widget protocol .. unit-shape toolbox)

Task: `OPUS-REQ-AUDITSPEC-DDRES-B10-0930`. Package: `_index/candidates/swe2contract-ddres-b10-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC (checker re-run on the certified image / installed assets, plus the named
spot-verified instructions). Reviewed the committed package as routed; no claims weakened.

## Independent verification

- `b10_checks.py` re-run: PASSES 245, FAILS 0 (incl. X1 archive-vs-extract byte equality on sample files).
- Spot-verified: `005C5230` is `xor eax,eax; ret` (the no-op handler) and `0017CDE0` is a bare `jmp 0x5c5230` to it - the "three unparsed rows are read" claim holds for two of the three named bodies.
- The widget-protocol recount (264 exact / 0 upper-bound / 3 unparsed) and the id-set reconciliation are re-derived by the control.

## Limits

Checker reproduction covers the package's mechanical claims; named anchors were additionally read off
the image directly. Prose-scope judgements (STALE/BOUNDARY/carried labelling) follow the batch's own
declared rule set and were not re-derived line by line.
