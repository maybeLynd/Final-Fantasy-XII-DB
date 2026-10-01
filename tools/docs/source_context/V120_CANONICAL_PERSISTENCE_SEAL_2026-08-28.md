# GFZ/GZF V120 — Canonical Persistence Seal

**Date:** 2026-08-28  
**Semantic branch:** `761B`  
**Status:** `PASS_CANONICAL_V120`

## Canonical artifact

**Artifact:** `FFXII_TZA_XIIOnline_Gfz9_V120_CANONICAL_761B_2026-08-28.gzf`  
**Size:** 75,017,534 bytes  
**SHA-256:** `507490534a8bb67e8d3c6deba4d527c23ab9fdd3672494e511db0d9ef0e511a9`

Canonical V120 now **exists**. It was not obtained by renaming BZ. It was produced by deterministic replay from the freshly reconstructed/fresh-reopen-verified V119 canonical-equivalent parent.

## Parent

- V119R artifact: `FFXII_TZA_XIIOnline_Gfz9_V119_RECONSTRUCTED_CANONICAL_EQUIVALENT_2026-08-28.gzf`
- V119R SHA-256: `db851ef4c1a1b3b8dcccb5f87acea09647f2f5dd94ffd1b2986d8ca977e3b46a`
- V119R FAS2: `c989a5f33292622afda1d8b3c47c6e7ee4f2cb6626f9726c1769cbd398acd49e`
- V119R functions: **38,160**

The lost historical V119 container SHA `3233684f...e65826` remains provenance only. The superseding parent proof is explicit state-equivalence reconstruction, consistent with the surviving V119 milestone's own prior reconstruction history.

## Deterministic replay

The exact reconstructed-V119 → final-V120 delta is sealed in `V119_RECONSTRUCTED_TO_V120_CANONICAL_EXACT_DELTA_2026-08-28.json` (`a4835787fbbb2542c5612cfaa30bbb5a59c81471e956a7c8c6809aac97cacc82`).

Actual replay transaction:
- **1** function created: `008A4BAB Catch_All_008A4BAB`;
- **1** semantic rename: `0037CF50` → `VMEventContext_InitializeActorOperation`;
- **10,103** existing function comments advanced to their sealed V120 target;
- **54,006** tag associations added;
- **4** obsolete parent associations removed;
- **0** body changes and **0** no-return changes were needed because exact-current structural hygiene was retained in V119R;
- **13,837** flow overrides already matched at the instruction level;
- Run-2 applied **1** Save/Load symbol rename and **2** instruction pre-comments.

## Final invariants

- Internal functions: **38,161**
- FAS2 SHA-256: `2f2ae19e3fad6ea56dea82d6ca399af662f5b8a31fbc213bd207edf903a693fb`
- Flow snapshot SHA-256: `d680426c1eae6c5595ad037e2dca576fe911ea6e9558120121a8cbbb01d2a758`
- Primary owners: **9,409**
- Primary-owner categories: **22**
- Primary-owner overlap: **0**
- Intentional final-no-primary-owner: **585**
- ScriptVM external corroboration: **1,838**
- Flow overrides: **13,837**
- Run-2 symbol/listing state: **PASS**
- Program: `FFXII_TZA.exe`, ImageBase `0x00120000`
- Embedded authorized EXE SHA-256: `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, byte-identical **PASS**

## Pack and fresh reopen

Packing occurred in a separate invocation with the target DomainFile reported `open=false`, `busy=false`, `changed=false`. The resulting GZF was imported into another clean Ghidra 12.1.2 project and independently reproduced:

- final verifier: **PASS**;
- exact FAS2 target: **byte-identical PASS**;
- exact flow target: **byte-identical PASS**;
- embedded original EXE: **byte-identical PASS**.

## Verdict

**V120 is canonical and persistence-certified. V121 lineage may proceed from this GZF.**
