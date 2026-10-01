# SWE2-AUDIT-SPEC review - DD residue batch 12: render-record array, FCP block, table registry

Task: `OPUS-REQ-AUDITSPEC-DDRES-B12-0930`. Package: `_index/candidates/swe2struct-ddres-b12-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC (checker re-run on the certified image / installed assets, plus the named
spot-verified instructions). Reviewed the committed package as routed; no claims weakened.

## Independent verification

- `b12_struct.py` re-run: FAILS 0 (incl. R4: `003DC330` stores `02B58188` - verified byte-exact `003DC332 mov [rip+0x277BE4F],rax` -> `02B58188`; `003DCF00`/`003DCF10` caller sets reproduced).
- The two residue answers (special-bone roles by consumer, `+0x414` write-only on PC) and the three corrected rows in the table registry are all mechanically re-checked; `consumer-check.md` exists for the strikes.

## Limits

Checker reproduction covers the package's mechanical claims; named anchors were additionally read off
the image directly. Prose-scope judgements (STALE/BOUNDARY/carried labelling) follow the batch's own
declared rule set and were not re-derived line by line.
