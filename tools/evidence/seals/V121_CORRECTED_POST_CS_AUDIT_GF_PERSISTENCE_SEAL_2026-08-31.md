# V121 corrected post-CS audit GF persistence seal — 2026-08-31

**Verdict: PERSISTENCE_CERTIFIED**

Latest durable V121 continuation GZF: `FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_CORRECTED_POST_CS_AUDIT_GF_99P54_2026-08-31.gzf`

- GZF size: **82,116,131 bytes**
- GZF SHA-256: `ef1ab2667efff8e4279d2446a6393e58328586972bf1b01c11049b4a510ba4eb`
- Internal functions: **38,161**
- Explicitly accounted: **37,985 / 38,161 = 99.53880%**
- Unresolved: **176**
- Cross-layer overlap: **0**
- Pre-GF snapshot SHA-256: `d89e38f53d92495a7992943fa317e4ffdc495b8911687c833e41833a65ffa470`
- Post-GF snapshot SHA-256: `3e313e0b05093bd2038cd9279d4a65f5b08402238089e4cc3308ab8115e6ecd4`
- Fresh-reopen snapshot SHA-256: `3e313e0b05093bd2038cd9279d4a65f5b08402238089e4cc3308ab8115e6ecd4` — byte-identical
- Fresh residual SHA-256: `6c95ca3ccc3a466c0302774a9a3824b9ad221d981dffdcf9099f9d3f54fc9d01`
- Embedded EXE SHA-256: `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## GF semantic closure

### `004753B0` — `Presentation.LegacyPS2Effect.GlobalEndpointInterpolationAndParameterDerivation`
Two registered effect callbacks used by already-accounted queued Presentation effect materializers call this helper, and their initializer path carries the legacy VIF-style command stream reconstructed earlier. The complete body derives endpoint deltas from the shared 0x02064Bxx–0x02064Cxx parameter bank, handles zero/sign conditions, computes the selected normalized interpolation ratio, interpolates float4/endpoint values, and republishes the derived parameter state. The label intentionally does not invent a named visual effect.

Exact body: **1,322 bytes**, SHA-256 `62551dc83bc3381b1b1c03c7180204c97d33d6d58c9cea9b18f77eb7257708b7`.

### `004EB910` — `Presentation.LegacyPS2Effect.SixFloat4ParameterRecordAppend`
Its sole semantic caller is a registered Presentation callback whose initializer embeds the proven VIF-style command words. The complete body derives transformed/scaled values from the shared legacy-effect state, appends exactly **six consecutive 16-byte records** into the 0x02064E30 output stream, and increments the shared record count by six. The callback invokes it repeatedly with positional variants. The label deliberately says parameter records rather than asserting vertices.

Exact body: **1,387 bytes**, SHA-256 `c6749d87a32841ce3e31faf29e630a6f6ea6141eff8cea7f184af0f66a839d94`.

## Mutation proof

Full deterministic comparison of all **38,161 functions** from certified GE to GF:
- changed functions: **2** — `004753B0`, `004EB910`
- comments changed: **2**
- CodeDomain tags added: **2**
- tags removed: **0**
- functions added/removed: **0 / 0**
- immutable changed count: **0**
- all body hashes/ranges, names, prototypes, thunk state and non-target functions: unchanged

## Packing / fresh-reopen proof

Separate closed-file pack preconditions reported `open=false busy=false changed=false canSave=false`, followed by explicit `PACK_PASS`. The resulting GZF was imported into a completely new project. The fresh project independently reproduced **37,985 explicit / 176 unresolved / overlap 0**, the exact authorized executable SHA-256, and a deterministic all-function snapshot byte-identical to post-GF (`3e313e0b05093bd2038cd9279d4a65f5b08402238089e4cc3308ab8115e6ecd4`).

## Corrected-lineage rule

No PE exception/unwind/IP-to-state metadata was used as semantic evidence. The protected mixed-context functions `002F7380` and `00313A00` remain unresolved and untouched.

## Next frontier

The exact fresh-reopened GF residual contains **176 unresolved functions**. Strong read-only candidates include the Phyre reflection/object-copy pair `00631290` / `0063CD20`, but their exact descriptor-level roles must be resolved before any next mutation.
