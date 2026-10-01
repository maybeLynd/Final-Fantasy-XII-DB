# GFZ V121 CONTINUATION REQUIREMENTS — 2026-09-01

## Current physical authority
`FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_GM160_RECOVERY_TRANSFER_99P58_2026-08-31.gzf`

- size: **82,110,895 bytes**
- SHA-256: `381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b`
- snapshot: `d2445517c66513976c83a446f87537a3c1d8c21f5bef033779affe98d7e61a20`
- embedded EXE: `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`
- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**
- current residual SHA: `fa6f614a463bf9981f32cbd4582e31ba23b04e6b803cfbb0139b209dffda5a1a`

## GN read-only work completed
No GM160 mutation has occurred. Two strong proposals are ready for exact-current challenge:

1. `00313A00` — `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`
   - body 289 bytes
   - SHA `c076cfeadbc81442c947e0c749eefbdef7e7c6717297847333a7cbae9289d246`

2. `002F7380` — `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`
   - body 723 bytes
   - SHA `15594f6181100f7fa10ac8a770566d60b963e47c93176fd7d7f33152b3ac8583`

Latest request-map detail for `00313A00`: inhibited requests 1/2/3/5/14/21 = Battle Menu, Party Menu/Menu Screen, party-leader change, free-target actor cycle, unnamed fullscreen slot 14, unnamed generic/transient slot 21.

## Immediate next operation
Fresh-import exact GM160; reproduce certified ledger/snapshot/EXE/residual; exact-current challenge both rows; apply only passing rows with exact expected count; whole-project FAS2 diff; separate closed pack with `PACK_PASS`; fresh reopen; regenerate residual.

If both pass, prospective post-GN arithmetic is **38,003 explicit / 158 unresolved / 99.58596% / overlap 0**, but do not claim that until fresh-reopen persistence certification passes.

## Non-negotiable rules
- Full executable is the scope.
- V120 PrimaryOwner and V121 CodeDomain are orthogonal.
- Never infer owner from caller/address neighborhood.
- Never use `.pdata/.xdata`/unwind/EH/IP-state metadata as semantic registration evidence.
- Exact-current-body fence before mutation.
- Regenerate residual after every mutation.
- Whole-project immutable diff.
- Separate pack invocation; explicit `PACK_PASS`; fresh reopen.
- Preserve unresolved when evidence is insufficient.
- Do not use VM wrappers as XIIOnline replay seams.
- Best native seam wins when stronger evidence exists.
- Never use 7z CLI.
- Always report concrete native behavior, not only counts.
- 100% explicit is not automatically final GFZ completion.
- Final V121 must be deterministically replayed onto fresh canonical V120 SHA `507490534a8bb67e8d3c6deba4d527c23ab9fdd3672494e511db0d9ef0e511a9` before canonicalization.
