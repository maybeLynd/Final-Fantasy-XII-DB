# Affected-consumer check: EA-3, the shipped values of the shader size word's bits 13-15 (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The ruling** (evidence: `_index/candidates/ea3-shader-size-bits/`). Bits 13-15 of `m_bufferLoc.m_size` are 0 in all
648,027 shipped `PShaderParameterDefinition` records. They are also 0 in all 13,356 `PShaderStreamDefinition`
records. The largest low-13 value is `0x1E00`.

**No accepted knowledge is replaced.** Two prior statements stand:
- the row's PARTIAL disposition: registered whole, loaded from the asset;
- the write-side sweep.

The page's "most plausibly a type or array-rank code" was a guess. The data does not bear it out, and the answer
says so without striking it.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` EA-3 | PARTIAL → ANSWERED, prior status kept as history | revised-here |
| `22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md` EA-3 box | ticked, answer appended | revised-here |
| `_types/fields.tsv` `PShaderParameterCaptureBufferLocationSize` `m_size` | meaning cell: byte count (EA-6's `001945B0` copy) + masked reads; shipped-value note | revised-here |
| `CONTRACT-phyre-packed-namespace.md` (packed layout) | the even-rounded objects region is a candidate note only; not written into the contract here | routed-to-SWE2-AUDIT-SPEC |

**Regression:** `ea3_census.py`. It fails the run if any of these holds:
- a list's objects region is not `count × width` rounded up to even;
- the schema layout varies;
- the mutation is not flagged exactly once;
- the sensitivity control finds nothing.

Run receipt: `ea3_census.py` executed at eba58ca1a (result.json sha256 `363de0e328e295d92f3b65f1bba6a7fea842aa6bdc23ab7b442167293952808d`).
