# SWE2-AUDIT-SPEC review - DD residue batch 11: four pages, closed registers vs open prose

Task: `OPUS-REQ-AUDITSPEC-DDRES-B11-0930`. Package: `_index/candidates/swe2struct-ddres-b11-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC (checker re-run on the certified image / installed assets, plus the named
spot-verified instructions). Reviewed the committed package as routed; no claims weakened.

## Independent verification

- `b11_struct.py` re-run: FAILS 0 (incl. S5: counter 14 = ACH_COUNT_SELL_EVITEM "Privateer", counter 19 = ACH_SPECIAL_HORIDASHI "Collector", and the slot-19 control at 01E00258).
- The four pages' dispositions (STALE/RESIDUE/carried) are checked line-by-line by the control; the 'Hits' glyph identification (battle_4_c, sub-image 0x0001 frame 14) is re-derived.

## Limits

Checker reproduction covers the package's mechanical claims; named anchors were additionally read off
the image directly. Prose-scope judgements (STALE/BOUNDARY/carried labelling) follow the batch's own
declared rule set and were not re-derived line by line.
