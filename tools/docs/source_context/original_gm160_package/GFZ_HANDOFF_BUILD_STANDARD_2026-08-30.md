# GFZ NEXT-CHAT HANDOFF BUILD STANDARD — 2026-08-30

This succeeds the 2026-08-29 standard and preserves every prior requirement.

## 1. Handoff = sealed continuation package
A new chat must be able to identify the latest durable artifact, hashes, canonical parent, current ledger, superseded branches, analyzed-but-not-applied work, exact next operation, tooling and persistence rules without guessing. Newer filenames are not authority unless their persistence state is proven.

## 2. Required package layout
Include the main handoff, compact continuation requirements, latest build standard, external-dependencies file, current-state JSON, next-frontier JSON, package seal, SHA256 manifest, selected evidence, necessary source context, and only small directly relevant tools.

## 3. Never bundle
Do not place the game EXE, any GZF, giant Ghidra projects, installers, or disposable temp logs in the handoff ZIP. Hash-bind required external artifacts instead.

## 4. Full-GFZ scope
The primary target is the **entire 38,161-function FFXII_TZA executable**. XIIOnline relevance affects research priority but is not the stopping condition. Explicit CodeDomain accounting is not identical to deep source-level understanding.

## 5. Evidence / anti-contamination
PrimaryOwner follows exact state/resource/lifecycle authority, never adjacency. CodeDomain may classify library/runtime/mechanism/support semantics without changing PrimaryOwner. Strong evidence: exact current body + complete decompilation, authored strings, qualified symbols, real MSVC RTTI/vftables, exact-body clones, coherent source-library matches, genuine non-EH data/function-pointer registration, actual address-taking/reference context, ff12-script/VBF/EBP corroboration. Call graph is corroboration, not sole ownership proof.

**Never use PE `.pdata`, `.xdata`, unwind records, EH maps, IP-to-state maps or `_IMAGE_RUNTIME_FUNCTION_ENTRY` records as callback/vtable/static-registration semantic evidence.**

## 6. Mutation / persistence
Start mutation only from a fresh import of the latest sealed GZF. Exact-body-enrich candidate manifests. Semantic seal before mutation. After mutation emit a whole-project FAS2 delta: zero unexpected/missing functions, no tag removals, immutable drift 0 unless separately authorized. Mutation/save and pack are separate invocations. Pack only when target DomainFile reports `open=false`, `busy=false`, `changed=false`; require explicit `PACK_PASS` and a plausible final size/hash. Fresh-import every pack into a new project and re-run coverage, FAS2 and embedded-original verification.

## 7. Timeout/hang recovery rule
A UI/tool timeout is **not evidence that work failed**. Before rollback or rerun, inspect filesystem/project outputs. A process may have completed after the UI cut off, or may have produced a partial pack. Verify FAS2, logs, `PACK_PASS`, file size/hash and fresh-reopen state. If a GZF is truncated, delete only the incomplete pack; preserve a valid mutated working project if its exact post-mutation FAS2 is intact, then repack cleanly. Never duplicate a mutation merely because the response timed out.

## 8. Script invocation traps learned
- `DecompileAddressFileBounded.java`: arguments are **output file, address file, timeout seconds**.
- `DumpUnresolvedMechanismFeatures.java`: requires **output file and maxInsns**.
- `ApplyCurrentBodyCodeDomainBatch.java`: requires **manifest, batchId, expectedCount, summary** and should reject before mutation if arguments/preconditions are wrong.
- Fresh Ghidra project parent directories must exist before import.
- Extracted Ghidra ZIP scripts may need executable permissions restored in a disposable environment.
- Use **system libarchive**, never the 7z CLI, for supplied multipart Ghidra archives.

## 9. Progress reporting requirement
Every continuation response and handoff must tell the user **what native behavior was uncovered**, not just percentages or generic labels like “movement owner,” “presentation routine,” or “explicit/unresolved.” Report concrete algorithms/state transitions/resources/APIs and why they matter.

## 10. Supersession accuracy
Physical persistence can remain valid while semantic interpretation is superseded. Preserve old artifacts as history but never use a semantically superseded artifact as continuation parent. Correctness outranks percentage.

## 11. Final V121 canonicalization
EW and successors remain noncanonical V121 WIP. When intended V121 full-executable closure/audit is complete, deterministically replay the proven V121 delta onto a fresh import of canonical V120 SHA-256 `507490534a8bb67e8d3c6deba4d527c23ab9fdd3672494e511db0d9ef0e511a9`, then pack/fresh-reopen/verify independently before claiming canonical V121.

## 12. Package seal
Hash every bundled payload except `SHA256SUMS.txt` and the package seal. The package seal records manifest SHA, payload count, external GZF/EXE identities, canonical parent, current ledger, superseded branch and `HANDOFF_READY`. Extract the completed ZIP to a fresh temp directory and verify every manifest hash before delivery.
