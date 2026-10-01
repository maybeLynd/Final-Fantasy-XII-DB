# NEXT CHAT HANDOFF — GFZ/GZF V121 WIP 761B — FULL-EXECUTABLE COVERAGE — GM160 RECOVERY TRANSFER — 160 FUNCTIONS REMAIN

**Date:** 2026-08-31  
**Project:** For Xeavin — FFXII TZA authoritative GFZ/GZF reconstruction  
**Semantic branch:** `761B`  
**Status:** **PERSISTENCE_CERTIFIED_RECOVERY_TRANSFER / NONCANONICAL V121 WIP / FULL-EXECUTABLE SEMANTIC CLOSURE CONTINUES**

# 0. READ THIS FIRST — EXACT CONTINUATION CONTRACT

This handoff supersedes EW/FA/FB/.../GG/visible-GH day-to-day continuation instructions while preserving all prior seals as provenance. The project target remains **full practical reverse-engineering coverage of the entire 38,161-function FFXII_TZA executable**. XIIOnline remains the priority ordering mechanism because gameplay/networking seams are immediately useful, but XIIOnline coverage is not the final scope or stopping condition.

**The handoff ZIP now intentionally includes the usable continuation GZF itself.** This corrects the earlier packaging rule that omitted GZFs. A GFZ next-chat handoff is not considered self-contained unless it includes the latest usable persistence-certified GZF (or, if a platform transfer limit genuinely prevents bundling, provides that exact GZF as a separate same-response artifact with explicit hash binding). The EXE remains excluded.

Current physical continuation artifact inside this package:

`FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_GM160_RECOVERY_TRANSFER_99P58_2026-08-31.gzf`

- size: **82,110,895 bytes**
- SHA-256: `381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b`
- fresh deterministic snapshot SHA-256: `d2445517c66513976c83a446f87537a3c1d8c21f5bef033779affe98d7e61a20`
- embedded original: exact authorized `FFXII_TZA.exe`, SHA-256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`
- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

This artifact is a **recovery transfer at the same ledger depth as historical GM**, not a claim of byte-identity with the inaccessible historical GM GZF. Historical GM remains provenance authority for its documented rows. The recovery transfer is the actual usable continuation parent shipped to the next chat.

# 1. VERSION / AUTHORITY RULES

## 1.1 Current physical WIP authority

Use the bundled GM160 recovery-transfer GZF for all next mutation work unless the exact historical GM GZF becomes available and independently verifies against its published SHA-256 `7b637b471ec66f3fc44efca88f956b52230599cb5d8dff0452743187e1b0d1b0`, size **82,126,436 bytes**, and snapshot `b4491ebbf9dc40a49830fd04c4c4754679ce8e120f3c8bc6bbab041204cf2cff`. Do not silently substitute any older checkpoint.

## 1.2 Historical GM distinction

Historical GM was genuinely persistence-certified at **38,001 explicit / 160 unresolved / 99.58072% / overlap 0**. The original binary was not available to place into this handoff. This transfer therefore replays eleven known sealed/verified post-GD rows and independently re-proves nine other functions from the exact GD body state. It preserves the same number of explicit functions but **does not claim that those nine recovery rows are the same nine functions historical GI→GK closed**. Preserve this distinction in all future provenance.

## 1.3 Canonical parent

V121 remains noncanonical WIP. Canonical V120 remains SHA-256 `507490534a8bb67e8d3c6deba4d527c23ab9fdd3672494e511db0d9ef0e511a9`. When V121 whole-executable closure and deep audit are genuinely complete, replay the complete proven V121 delta deterministically onto a fresh import of canonical V120 and independently pack/reopen/verify. Never declare canonical V121 by renaming this WIP/recovery artifact.

## 1.4 Superseded CS branch

The old 99.00422% CS artifact `cd50cea3fa7449e45d6499fa3e0311e467cb497b3f1dddeb4fe256550402c92b` is semantically superseded and forbidden as a parent. Corrected audit proved PE `.pdata`, `.xdata`, unwind and EH/IP-to-state metadata had been overread as semantic registration evidence. Of 368 CS functions, 186 were independently re-proven and 182 rejected. Do not restore rejected rows without new independent proof.

# 2. EXACT CURRENT MACHINE STATE — GM160 RECOVERY TRANSFER

| Item | Certified current value |
|---|---:|
| Internal functions | **38,161** |
| PrimaryOwner | **9,409** |
| PrimaryOwner categories | **22** |
| FinalNoPrimaryOwner | **585** |
| V121 CodeDomain | **28,007** |
| Explicitly accounted | **38,001** |
| Unresolved | **160** |
| Explicit coverage | **99.58072%** |
| Cross-layer overlap | **0** |

PrimaryOwner counts remain the V120 authoritative owner layer: ActorEntity 235; Audio 2,064; CombatAI 43; CombatAction 134; CombatFormula 198; CoreRuntimeScheduling 73; Input 1,047; Items/Equipment/Shops/License 70; Movement 485; Party 79; Platform/Online/Achievements 59; Presentation 1,564; RNG 18; Resource 572; Rewards/Progression/Economy 38; Save/Load/Settings 87; Script/VM Native Bridge 1,900; Spawn/Encounter/Lifecycle 52; Status/Periodic/Terminal 24; Story/Event/Quest/Hunt 15; UI 544; WorldAreaField 108.

## 2.1 Fresh current hard-residual scan

The exact 160-current residual was regenerated from the **fresh-reopened transfer GZF**, not inherited from GM/GL/EW:

- **160** unresolved addresses in `evidence/GM160_CURRENT160_ADDRS.txt`
- address-list SHA-256: `fa6f614a463bf9981f32cbd4582e31ba23b04e6b803cfbb0139b209dffda5a1a`
- exact-byte clone hits: **0**
- qualified Phyre/std/EASTL symbol hits: **0**
- direct string-reference functions: **0**
- unresolved functions with direct PrimaryOwner references: **2**
- owner references into them: **4**
- incoming data references: **382**

The only owner-referenced holdouts are `002F7380` and `00313A00`. Do not use the owner references as semantic proof.

# 3. WHAT THIS CONTINUATION ACTUALLY UNCOVERED

The user requires progress reports to explain **what native behavior was learned**, not just counts/categories. EW→historical GM moved **37,899 → 38,001 explicit**, **262 → 160 unresolved**, **+102 semantic closures**, and **99.31344% → 99.58072%** whole-executable explicit coverage. The recovery transfer maintains that same ledger depth. Major discoveries include:

## 3.1 Presentation / UI / CharacterRender / camera

- linked Presentation template/resource graph rebuild and parameter propagation; actor-scoped effect/constraint collection;
- UI screen double-buffering, relation collection, transition/fade state machines, transform-history animation, list/equipment row construction and packed-element dispatch;
- native actor-overlap-driven CharacterRender transparency/occlusion fading; pending-record flush/rematerialization and masked record rebuild;
- HUD command-row progress/palette/pulse/fade updates and full-screen transition overlays;
- Phyre active-camera snapshot/derived matrix commit, cubemap/capture camera face parameters, and screen-capture geometry;
- Quest list metadata/detail-resource resolution and Quest selection/detail state machine;
- paired camera-input state initialization and derived-matrix rebuild;
- CharacterRender four-channel contribution normalization/resource binding.

## 3.2 D3D11 / Phyre rendering

- dynamic vertex/index buffers, Map/copy/Unmap upload, SRV/UAV creation, dirty subresource updates, input-layout construction and six-face mip uploads;
- DXGI adapter/output inventory and display-mode filtering/deduplication/desktop-nearest selection;
- Phyre fullscreen-triangle materialization for WebM/YUV presentation; render-thread default checkerboard fallback textures; native Depth-of-Field and Screen-Space-Reflection target initialization;
- asynchronous PTexture2D mip upload, 3D volume-mip upload, PTexture2D CPU-write mapping, shader-parameter capture-buffer layout construction;
- D3D11 vertex-stream CPU repack and IASetVertexBuffers/InputLayout cache update; PrimitiveRenderer dirty-state commit;
- texture-format descriptor registry teardown.

## 3.3 Legacy PS2 VIF/VU Presentation architecture

The PC executable retains a genuine PS2 VIF/VU compatibility path: VIF command interpreter, UNPACK decoder, multiple authored VIF state/program initializers, endpoint/parameter update callbacks and record emission. The recovery transfer independently adds two more exact-body VIF program-state initializers (`004F4F80`, `0048CE70`) with literal UNPACK/MSCALF/FLUSHA command words.

## 3.4 Physics / math / runtime / standard library

- Bullet DBVT/pair-cache/Voronoi/rigid-body/sequential-impulse mechanisms and Phyre-to-Bullet rigid-body materialization/reset;
- Phyre `PPhysicsWorld` deep-copy assignment and reflection-driven recursive object-field copy engine;
- 4x4 inverse/multiply, affine transform palette, transformed-box frustum test, clip outcodes, DCT forward/inverse pixel reconstruction;
- red-black tree insertion/erase/fixups, vector insertion/reallocation, 544-byte and 24-byte record fill-inserts, multiple sort/heap specializations;
- native image-address arena allocation/split/reclamation retry;
- encoded-message formatting interpreter, control/template expansion and recovery-transfer control-usage pre-scan.

# 4. RECOVERY-TRANSFER DELTA — DO NOT CONFUSE WITH HISTORICAL GM

Twenty functions were added to certified GD to create this transferable 160-current artifact. Eleven are known sealed/verified post-GD semantics; nine are independently re-proven replacements for transfer continuity because the hidden historical GI→GK identities were unavailable.

### 4.1 Replayed sealed/verified rows

- `00692AC0` — `Phyre.PPhysics.PPhysicsWorld.DeepCopyAssignment`
- `00626120` — `Phyre.PRendering.PTexture2DD3D11.BufferSlotMipChainMapForCPUWrite`
- `004753B0` — `Presentation.LegacyPS2Effect.GlobalEndpointInterpolationAndParameterDerivation`
- `004EB910` — `Presentation.LegacyPS2Effect.SixFloat4ParameterRecordAppend`
- `00631290` — `Phyre.Reflection.ClassDescriptorRecursiveObjectFieldCopyTraversal`
- `0063CD20` — `Phyre.Reflection.MemberDescriptorValueCopyDispatch`
- `00607990` — `Phyre.PRendering.ShaderParameterCaptureBufferLayoutDescriptorBuild`
- `00183320` — `Phyre.PRendering.PTexture2D.FormatCodeBlockRepackChannelScaleAndUpdate`
- `001E6480` — `Presentation.CharacterRender.FourChannelContributionNormalizeAndParameterBind`
- `001897C0` — `Presentation.Rendering.PairedCameraInputStateInitializeAndDerivedMatrixRebuild`
- `0037F1F0` — `Runtime.Resource.AsyncAssetSlotPollFinalizeNotifyOrRetry`

### 4.2 Independently re-proven transfer rows

- `002481C0` — `Runtime.Callback.LinkedFlagGatedNotificationDispatch`
- `00248030` — `Runtime.Callback.HierarchyGenerationBitTraversalAndCallbackReconciliation`
- `002465F0` — `Runtime.Callback.GenerationBoundRecordInitializeAndInitialNotify`
- `00393240` — `Runtime.Record.Kind2FourSlotOrKind5ModeValueMaterialization`
- `00392FC0` — `Runtime.RecordCollection.Kind2OrKind5ModeValuePropagation`
- `002B4810` — `Presentation.Text.EncodedMessageControlUsageScanAndSlotClassification`
- `001E2250` — `CxxStandardLibrary.Vector.MapOrderedObject24ByteFillInsertReallocation`
- `004F4F80` — `Presentation.LegacyPS2Effect.VIFProgramStateBlockInitializer`
- `0048CE70` — `Presentation.LegacyPS2Effect.VIFProgramStateBlockInitializer`

The exact evidence sentences and current body hashes are preserved in `evidence/GM160_RECOVERY_TRANSFER_ENRICHED_MANIFEST.tsv` and the persistence seal.

# 5. PRIMARYOWNER / CODEDOMAIN BOUNDARY — DO NOT CONTAMINATE

V120 PrimaryOwner answers **which subsystem owns the state/resource/lifecycle transaction**. V121 CodeDomain answers **what code/mechanism/library behavior a function implements**. They are orthogonal; overlap must remain 0. A caller being Presentation, Movement, CombatAction or WorldAreaField does not grant that owner to a callee. Generic math, containers, middleware, callbacks and platform routines receive conservative CodeDomain labels when proven.

# 6. EXACT STOPPING POINT / NEXT WORK — GN IS READ-ONLY FIRST

There is **no GN mutation in this handoff**. Start from the bundled recovery-transfer GZF and regenerate/verify its 160-current residual before any mutation. The first next-chat task is body-driven **GN read-only semantic analysis**. There is no pre-authorized GN manifest.

Exact order:

1. Verify `SHA256SUMS.txt` and `V121_HANDOFF_PACKAGE_SEAL_2026-08-31.json`.
2. Verify the bundled GZF size/SHA.
3. Import it into a brand-new writable Ghidra project with auto-analysis disabled.
4. Reproduce **38,161 / 38,001 explicit / 160 unresolved / 99.58072% / overlap 0**.
5. Reproduce embedded EXE SHA `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
6. Regenerate or verify the exact 160-current address list and residual structure/owner/data/string/clone/symbol/mechanism/neighborhood scans.
7. Confirm `002F7380` and `00313A00` remain unresolved unless stronger complete-body evidence now exists.
8. Rank the tail by complete-body mechanism evidence and genuine class/vtable/source evidence, not address range or owner adjacency.
9. Decompile/challenge a small coherent family.
10. Build GN pre-enrichment rows only for semantics that survive complete-body, caller/callee, actual data references, genuine RTTI/vtables, strings/resources, ff12-script/VBF/EBP/runtime/upstream-source challenge as applicable.
11. Exact-current-body enrich. Reject any body/classification drift.
12. Apply exact expected count only.
13. Generate complete post-GN deterministic snapshot and diff. Required: only intended comments/tags; functions +/− 0; tag removals 0; immutable/body/range/name/prototype/thunk drift 0.
14. Tell the user **what native mechanisms were learned**, not only count/percentage.
15. Close target. Pack in separate headless invocation using `PackClosedDomainFile.java`; require `open=false`, `busy=false`, `changed=false`, preferably `canSave=false`, and explicit `PACK_PASS`.
16. Fresh-import pack into a completely new project. Reproduce deterministic snapshot, ledger, overlap and exact EXE before claiming persistence.
17. Regenerate residual from fresh post-GN state. Never reuse the 160 list after mutation.
18. Repeat family-by-family; preserve unresolved when evidence is insufficient.

# 7. EVIDENCE HIERARCHY / RESEARCH RULES

Prefer: (1) complete exact-current body/decompilation/disassembly + typed mechanics; (2) authored/runtime strings; (3) qualified symbols; (4) real MSVC RTTI/vftable/class-descriptor index; (5) exact-body clone with unanimous interpretation; (6) coherent upstream source/library match; (7) genuine typed pointer/vtable/static registration **after excluding exception metadata**; (8) actual code address-taking/data references; (9) ff12-script/VBF/EBP/LiveLab/runtime corroboration; (10) call graph/neighborhood only as supporting context.

Best-native-seam-wins remains active for XIIOnline-relevant discoveries: known addresses/calls are starting points, not sacred. Prefer a higher-level native transition with fewer direct writes and better downstream native coherence when concrete evidence supports it, and document the substitution.

# 8. ABSOLUTE FORBIDDEN SHORTCUTS

- No owner assignment from caller adjacency.
- No semantics from PE `.pdata`, `.xdata`, unwind, EH/IP-to-state tables.
- No address-range ownership without independent boundaries.
- No generic filler classifications merely to force 100%.
- No restoration of rejected CS rows without new proof.
- No stale residual list after mutation.
- No assuming timeout means success or failure; inspect outputs.
- No 7z CLI. Use libarchive/standard ZIP handling.
- No claiming packed GZF from file existence; require `PACK_PASS`, sane hash/size, fresh reopen.
- No persistence claim from a working Ghidra project alone.
- No treating 100% explicit accounting as semantic completion.
- No claiming this recovery transfer is byte-identical to historical GM.

# 9. TIMEOUT / HANG RECOVERY

On interruption: inspect projects/manifests/logs/snapshots/packs/seals first; audit any newer checkpoint before rolling back; partially written packs are invalid; if post-mutation snapshot proves mutation completed, rerun only failed pack/reopen/evidence step; deterministic recovery is allowed only from a certified parent with explicit replay provenance and a new full diff/pack/reopen; clear stale Ghidra locks only after confirming no process owns them; always finish a human-readable persistence seal.

# 10. TOOLING

Baseline Ghidra **12.1.2**, Java **21**, GhidraMCP/Bethington **6.0.0** when useful. Continuation scripts and the ff12-script research ZIP are bundled under `tools/`. Independent challenge tools may include radare2, LIEF, Capstone, angr, DynamoRIO and LiveLab when they materially improve certainty. Ghidra exact-current body identity and persisted annotation state remain authoritative for GFZ mutation. Read `tools/README_GFZ_TOOL_USE_2026-08-30.md` because positional argument order differs across scripts. If Ghidra must be reconstructed from multipart sources, use system libarchive/standard ZIP tools; **do not use the 7z CLI**.

# 11. COMPLETED / DO-NOT-RESTART WORK

- V120 x0 full-project audit/canonical V120 are historical completed provenance.
- Old V111 Presentation restoration / old residual fronts are not current.
- Corrected CS audit complete: 186 re-proven / 182 rejected.
- CV→EW and EW→GM-family semantic closure are historical completed work.
- Do not replay visible EX/FA/.../GG batches onto this artifact; they are already represented by its parent lineage or recovery transaction.
- Do not treat older clone/string/symbol scan counts as current; use the bundled 160-current scans.
- Established families—Bullet/Tremor/Vorbis/zlib/VP8/Lua/math/container, PS2 VIF/VU effect path, Phyre texture/stream machinery, Bullet rigid-body materialization and Phyre reflection copy—may be used as context but should not be reclassified from scratch absent contradictory evidence.

# 12. STATIC VS RUNTIME PROOF

GFZ semantic reconstruction is static/native-code understanding. It can improve XIIOnline seam selection and LiveLab test design, but static GFZ proof is not a substitute for real linked multiplayer certification. Runtime observations may corroborate/challenge static semantics but must be reconciled with exact code evidence.

# 13. FINAL V121 CONDITION

Even if unresolved reaches zero, do **not** automatically call GFZ finished. Run a deep whole-executable audit for stronger names/signatures/fields/state machines/call chains/native transitions; adversarially audit the complete V121 delta for owner inheritance, EH contamination, stale evidence, overbroad middleware labels and conflicts; confirm overlap 0; then deterministically replay the complete proven V121 delta onto fresh canonical V120 and independently pack/reopen/verify before claiming canonical V121.

# 14. FILES TO OPEN FIRST IN THE NEXT CHAT

1. This main handoff.
2. `V121_CORRECTED_POST_CS_GM160_RECOVERY_TRANSFER_PERSISTENCE_SEAL_2026-08-31.md`.
3. `V121_CURRENT_STATE_GM160_RECOVERY_TRANSFER_2026-08-31.json`.
4. `V121_NEXT_FRONTIER_GM160_SEMANTIC_CLOSURE_2026-08-31.json`.
5. The **bundled GZF**.
6. `evidence/GM160_CURRENT160_ADDRS.txt`.
7. Current structure/owner/data/string/clone/symbol/mechanism/neighborhood scans.
8. `evidence/GM160_RECOVERY_TRANSFER_ENRICHED_MANIFEST.tsv` and exact-delta JSON.
9. `GFZ_V121_CONTINUATION_REQUIREMENTS_2026-08-30.md` and `GFZ_HANDOFF_BUILD_STANDARD_2026-08-30.md`.

# 15. USER-FACING PROGRESS REQUIREMENT

Always explain actual discoveries: e.g. “this is Phyre PTexture2D CPU-write mip mapping,” “this constructs a Bullet btRigidBody,” “this interprets VIF UNPACK,” “this updates CharacterRender overlap transparency.” Do not report only generic category movement or percentages. Counts plus concrete native meaning are required.

# 16. CORRECTED HANDOFF PACKAGING RULE

**For GFZ continuation, the latest usable persistence-certified GZF must be included in the handoff ZIP.** This package deliberately includes the recovery-transfer GZF. Do **not** include the EXE. Include the main handoff, persistence seal, current-state/frontier JSON, residual evidence, mutation/diff evidence, scripts/research source, hashes and package seal. If future platform limits make bundling impossible, supply the exact same GZF as a separate same-response artifact and make the handoff explicitly point to it; never leave the next chat with only a hash for an unavailable GZF.

# 17. NEXT-CHAT STARTUP PROMPT

`We are continuing the For Xeavin FFXII_TZA GFZ/GZF V121 full-executable reconstruction from the attached GM160 recovery-transfer handoff. Read the complete handoff and persistence seal before acting. Use the GZF included in the ZIP as the physical continuation parent; do not silently substitute an older artifact. First verify hashes, fresh-import it into a brand-new Ghidra project, reproduce 38,161 functions / 38,001 explicit / 160 unresolved / 99.58072% / overlap 0 and the authorized embedded EXE hash, then regenerate/verify the exact 160-current residual evidence. Begin GN read-only semantic analysis; there is no pre-authorized GN mutation. Preserve 002F7380 and 00313A00 unresolved unless stronger complete-body proof resolves them. Follow exact-current-body fencing, full-project immutable-drift diff, closed-file PACK_PASS and independent fresh-reopen certification for every mutation batch, and always tell me what native behavior was actually learned.`
