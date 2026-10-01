# SWE2-AUDIT-SPEC review of SD-64 (sd64-file-only-names-0930 at 02d334dbe): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS.
Reviewed: `02d334dbe`. Record: [sd64-file-only-names-0930](../sd64-file-only-names-0930/README.md). Shipped-data
census (169 extracted `.phyre` files at `D:/FFXII MP Mod/extracted`) plus a schema join.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD64-0930 | sd64-file-only-names-0930 | 02d334dbe | ACCEPT |

**Re-run.** `sd64_names.py` from its own directory: C1-C4 PASS, `FAILS 0`, identical to the committed `.out`
ignoring CR ([rerun_sd64_names.out](rerun_sd64_names.out)). There are 169 files, 21 names, and the same per-list counts.
The record directory stayed clean.

**Re-derived independently** ([sd64_rederive.py](sd64_rederive.py) / [sd64_rederive.out](sd64_rederive.out)).
- **"In no namespace pool": a gap in the checker, closed.** The checker skips an occurrence when the name is in
  *that file's* pool. So a name that is a pool name in one file and array data in another would still be listed.
  The claim "none of them is in any namespace pool" needs the union of all pools. I tested it: none of the 21 names is
  in any of the 169 files' pools. HOLDS.
- **Control C1 is sensitive to the defect it guards.** I re-placed the lists under the layout the record rejects
  (all lists' objects first, then all arrays):
  - `c1004`'s `PAssetReference` arrays then read `AlphaThreshold`, `AnimNormalSampler1` (shader parameter names),
    not asset ids;
  - its `PString` arrays read binary (`?K0 >`), not node names.

  Under the accepted layout, they read `...c1004.dae#LODNODE_0` and `s0_model`. So C1 separates the two layouts.
- **Placement is layout-dependent, and the accepted layout gives the clean answer.** Under the accepted layout all
  occurrences land in array data of the eight classes the record names. The counts are the author's: 16,455 / 13,133 /
  4,939 program arrays; 568 `PShaderParameterDefinition`; 92 + 92 stream / input-desc; 17 `PMaterialSwitch`; 5
  `PShaderPassInfo`. Under the rejected layout, 1,305 land in `PShaderParameterCaptureBufferLocationTypeConstantBuffer`
  objects, 145 in `PShaderPass` objects and 48 in `PAssetReference` arrays: an incoherent placement. That independently
  supports C2 ("array data, not objects").

**Controls.** C1 is a real control, and it is now shown to be sensitive. C3 checks set membership, which is enough for
"the page's examples are included". C4 checks that each owning class has a `VPString` member of the named name.
It does not show that each string sits at that member's payload. The README says "held by registered PString
members", which C4 supports only at the class level. That is acceptable as labelled; no correction is needed.

**Limits stand as written.** The first pass's exact 27 are not reproducible. The sample is 169 files, not the whole
archive. The program-blob reflection reading is not decoded, and the by-name binding code is not traced.

**Verdict.** ACCEPT. The answer to the row (no file table carries these names; they are string data of
shader-parameter, stream, pass and material-switch objects, and of program blobs) holds.
