# GFZ V121 Full-Executable Coverage — 99% Persistence Seal
**Date:** 2026-08-29

## Verdict
**PERSISTENCE_CERTIFIED — 99.00422% FULL-EXECUTABLE EXPLICIT COVERAGE**

- Internal functions: **38,161**
- PrimaryOwner: **9,409**
- FinalNoPrimaryOwner: **585**
- V121 CodeDomain: **27,787**
- Explicitly accounted: **37,781**
- Unresolved: **380**
- Explicit coverage: **99.00422%**
- Cross-layer overlap: **0**

## CS transaction
- Exact-current closures: **368 / 368**
- Changed fields: function comment + CodeDomain tag only
- Immutable function drift: **0**
- Function additions/removals: **0 / 0**
- Tag removals: **0**
- 33 initially over-specific Microsoft/EASTL table inferences were adversarially downgraded to the truthful generic `Runtime.OwnerFreeStaticFunctionTable.Member` relation before mutation.
- No V120 PrimaryOwner assignments were changed.

## Persistence proof
- Packed GZF: `FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_CHECKPOINT_99PCT_2026-08-29.gzf`
- Packed bytes: **81,994,519**
- Packed SHA-256: **cd50cea3fa7449e45d6499fa3e0311e467cb497b3f1dddeb4fe256550402c92b**
- Live post-CS FAS2 SHA-256: **319ae46854ecbf0ff79206f98d27121ad5d510255325e02c52b8a484402e90ad**
- Independent fresh-reopen FAS2 SHA-256: **319ae46854ecbf0ff79206f98d27121ad5d510255325e02c52b8a484402e90ad**
- FAS2 byte identity: **PASS**
- Fresh-reopen embedded `FFXII_TZA.exe` SHA-256: **73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8**
- Authorized EXE identity: **PASS**
- Pack precondition: target DomainFile reported `open=false`, `busy=false`, `changed=false`.

## Evidence standard
CS uses broad CodeDomain relations only where the binary evidence supports that exact relation: static callback/function-table membership, owner-registered support, concrete Phyre/Bullet table membership, and WebM/MKV implementation membership. It does not promote support functions to PrimaryOwner or claim source-level method identity where only table/library membership is proven.

The remaining **380** functions are the final V121 residual set and require family/individual semantic closure rather than percentage-driven generic classification.
