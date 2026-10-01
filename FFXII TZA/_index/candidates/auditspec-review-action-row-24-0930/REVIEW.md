# SWE2-AUDIT-SPEC review - GR-6: bit-15-clear action-row +0x24 words are effect ids

Task: `OPUS-REQ-AUDITSPEC-GR6-0930`. Package: `_index/candidates/gr6-action-row-24-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `gr6_row24_check.py` re-run: FAILS 0 (G1-G4: effect-id routes at `0030A190`/`0030CA80`->`002FCB40` bit 5/`00310DB0`->`002EACD0`->`003B02A0`; the +0x0C-bit-30 row counts {FFFF,0:43; FFFF,1:25; b15,0:39; clear,0:374; clear,1:62} reproduced).

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
