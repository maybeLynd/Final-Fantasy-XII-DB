# GFZ NEXT-CHAT HANDOFF / BUILD STANDARD — 2026-09-01

This supersedes the 2026-08-30 handoff build standard while preserving its evidence, mutation, persistence and timeout rules.

## 1. Scope
GFZ scope is the complete 38,161-function FFXII_TZA executable. XIIOnline priority does not limit final coverage.

## 2. Authority
Always identify the exact physical continuation GZF by filename, size, SHA, snapshot and embedded EXE. Never silently substitute an older checkpoint. Distinguish historical provenance from the actual transferable parent.

## 3. Corrected GZF packaging rule
For GFZ continuation, the latest usable persistence-certified GZF **must be included in the handoff ZIP**. This supersedes the older blanket “never bundle GZF” rule. If platform limits prevent bundling, supply the exact GZF as a same-response artifact with explicit hash binding. Do not bundle the game EXE.

## 4. Required handoff contents
Include: main handoff; GZF; persistence seal; current-state/frontier JSON; exact residual/evidence; mutation/diff/pack/fresh-reopen evidence; current build standard; continuation requirements; source context; necessary scripts/tools; relevant research source; SHA256 manifest; package seal; supersession index when interpretations changed.

## 5. PrimaryOwner vs CodeDomain
PrimaryOwner follows exact state/resource/lifecycle authority. CodeDomain describes implemented mechanism/library/runtime behavior. Never infer ownership from callers, address ranges, neighborhood, owner refs, or convenience. Cross-layer overlap remains 0.

## 6. Evidence hierarchy
Prefer complete exact-current body; authored strings; qualified symbols; genuine RTTI/vtables; exact-body clones; coherent source-library matches; non-EH typed registration/address-taking; actual data refs; ff12-script/EBP/VBF; runtime/LiveLab/CE; call graph only as corroboration.

## 7. Forbidden semantic shortcuts
Never use PE `.pdata`, `.xdata`, unwind, EH maps, IP-state maps or `_IMAGE_RUNTIME_FUNCTION_ENTRY` records as callback/vtable/registration semantic proof. Never force generic classifications to hit 100%.

## 8. Mutation fence
Fresh-import latest sealed GZF. Regenerate residual. Exact-current body/hash every candidate. Enrich current body. Apply exact expected count only. Reject drift.

## 9. Whole-project proof
After mutation snapshot all 38,161 functions and diff against the exact parent. Require no unexpected/missing functions, tag removals 0, immutable/body/range/name/prototype/thunk drift 0 unless separately authorized.

## 10. Persistence
Mutation/save and pack are separate invocations. Pack only with target closed/not busy/not changed; require explicit `PACK_PASS`. Fresh-import every pack into a new project and reproduce coverage, snapshot, overlap and embedded EXE.

## 11. Residual rule
Regenerate unresolved residual after every mutation/fresh reopen. Never reuse an old address list after semantic mutation.

## 12. Timeout/hang rule
Timeout is not evidence of failure. Inspect project/files/logs/snapshots/pack before rerun. Preserve a valid completed mutation and rerun only failed pack/reopen steps. Partial packs are invalid.

## 13. Tooling
Ghidra 12.1.2 / Java 21; GhidraMCP/Bethington as useful; independent challenge tools allowed. Read `tools/README_GFZ_TOOL_USE_2026-08-30.md`.

## 14. Archive rule
Never use the 7z CLI. Use standard ZIP or system libarchive.

## 15. ff12-script / VM wrapper rule
Use ff12-script/EBP/VBF for authored intent/schema corroboration. ScriptVM wrappers do not grant ownership and should not be used as XIIOnline replay seams; descend to the lower native owner transition.

## 16. Best native seam wins
Known calls are starting points. Prefer evidence-backed higher native transitions that minimize direct writes and maximize downstream coherence/mod compatibility. Document substitutions.

## 17. Progress reporting
Every response/handoff must state concrete native discoveries plus count/coverage. Generic category movement alone is not acceptable.

## 18. 100% is not automatically finished
After explicit closure, deep-audit the whole V121 delta and replay it deterministically onto fresh canonical V120 before canonicalizing V121.
