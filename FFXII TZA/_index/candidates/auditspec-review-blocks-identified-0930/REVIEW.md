# SWE2-AUDIT-SPEC review - battle-HUD blocks + GR-3 (five blocks by layout keys/strings/requesters)

Task: `OPUS-REQ-AUDITSPEC-HUD-BLOCKS-GR3-0930`. Package: `_index/candidates/hud-blocks-identified-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `hud_blocks_check.py` re-run: FAILS 0 (A1-A5 gate/draw/pass + pool producers; G1-G4 the chain recorder and keyframes; C1-C4 the request word census `hud+0x7C7C`/`+0x7C82` and EnemyChain requesters; K1-K7 the shuffle strip incl. K7's measured LIMIT; S1-S4 the side-cursor block; N1-N4 the partytop_8_c minimap labels).

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
