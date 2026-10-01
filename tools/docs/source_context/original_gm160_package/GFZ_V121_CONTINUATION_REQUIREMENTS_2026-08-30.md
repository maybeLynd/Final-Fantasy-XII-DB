# GFZ V121 CONTINUATION REQUIREMENTS — 2026-08-30

## Current authority
- Latest durable checkpoint: **EW**.
- External GZF: `FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_CORRECTED_POST_CS_AUDIT_EW_99P31_2026-08-29.gzf`
- size: **82,064,424 bytes**
- SHA-256: `ab08c4473f949453181dd40d368ee92a64553e87b4b385a081b043cecd862682`
- exact/fresh-reopen FAS2 SHA-256: `7ad529d76c311bc7121700cf82d0c16507de8d5c48b6c76efb3ee9a678555ec8`
- authorized EXE SHA-256: `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`
- canonical V120 final-replay parent SHA-256: `507490534a8bb67e8d3c6deba4d527c23ab9fdd3672494e511db0d9ef0e511a9`
- V121 remains **noncanonical WIP** until final deterministic replay onto canonical V120.

## Exact current ledger
- internal functions: **38,161**
- PrimaryOwner: **9,409 across 22 categories**
- FinalNoPrimaryOwner: **585**
- V121 CodeDomain: **27,905**
- explicit: **37,899 / 38,161 = 99.31344%**
- unresolved: **262**
- overlap: **0**

## Exact current residual facts
- exact-byte clone shortcuts: **0**
- qualified Phyre/std/EASTL shortcuts: **0**
- unresolved functions with direct owner refs: **26** / **53 refs**
- incoming data refs: **591**
- direct string-reference functions: **1**
- EX analyzed-not-applied strong candidates: `00370890`, `0037AD40`
- withheld ambiguous candidates: `00313A00`, `002F7380`
- **No EX mutation has occurred.**

## Non-negotiable rules
- Read the complete main handoff before acting.
- Full GFZ means the entire executable; XIIOnline is priority only.
- Fresh-import and verify exact EW before mutation.
- Do not use the old 99.00422% CS GZF (`cd50cea3fa7449e45d6499fa3e0311e467cb497b3f1dddeb4fe256550402c92b`) as parent.
- Do not restore the 182 rejected CS rows without new independent proof.
- Do not use `.pdata/.xdata`/EH/unwind/IP-state metadata as semantic registration evidence.
- Owner follows exact authority, never caller adjacency.
- Use CodeDomain for proven runtime/library/mechanism semantics without contaminating PrimaryOwner.
- Exact-current body/hash and semantic proof before mutation.
- Whole-project FAS2 diff after every mutation; immutable drift 0.
- Mutation/save and pack separate; pack closed target only; require `PACK_PASS`.
- Fresh-reopen every packed GZF into a new project and verify full FAS2, coverage, overlap and embedded EXE.
- Never use 7z CLI; use libarchive.
- Preserve unresolved status when evidence is insufficient; never force 100%.
- Report concrete discoveries, not only coverage counts.
- 100% explicit accounting would still not equal final deep GFZ completion.

## Immediate next work
1. Verify handoff manifest and external EW GZF.
2. Fresh-import EW and reproduce 99.31344% / 262, FAS2 `7ad529d76c311bc7121700cf82d0c16507de8d5c48b6c76efb3ee9a678555ec8`, embedded EXE `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
3. Read `evidence/V121_EX_ANALYZED_NOT_APPLIED_2026-08-30.md`.
4. Re-decompile and adversarially validate `00370890` and `0037AD40`.
5. Exact-body-enrich a two-row EX manifest only if both still pass.
6. Apply only passing rows, snapshot all 38,161 functions, exact-diff, coverage report.
7. Pack closed target separately, require `PACK_PASS`, fresh-reopen and verify before calling EX durable.
8. Regenerate the residual from post-EX state and continue semantic reconstruction family-by-family.
9. Keep `00313A00` and `002F7380` unresolved until stronger semantics exist.
10. At intended V121 completion: whole-project adversarial audit, deterministic replay onto canonical V120, independent fresh-reopen, then canonicalize.
