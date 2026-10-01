# V121 corrected post-CS audit GG persistence seal — 2026-08-31

**Verdict: PERSISTENCE_CERTIFIED**

Latest durable V121 continuation GZF: `FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_CORRECTED_POST_CS_AUDIT_GG_99P54_2026-08-31.gzf`

- GZF size: **82,121,051 bytes**
- GZF SHA-256: `78ebcff5d55306e82ae1fe7e1ed7520c04f224f6029b08c188c5703dee38576c`
- Internal functions: **38,161**
- Explicitly accounted: **37,987 / 38,161 = 99.54404%**
- Unresolved: **174**
- Cross-layer overlap: **0**
- Pre-GG snapshot SHA-256: `3e313e0b05093bd2038cd9279d4a65f5b08402238089e4cc3308ab8115e6ecd4`
- Post-GG snapshot SHA-256: `d5ef2466ec7ae4e3b68e08fbe913824b57622ddc175a557bdf7187fbd3549224`
- Fresh-reopen snapshot SHA-256: `d5ef2466ec7ae4e3b68e08fbe913824b57622ddc175a557bdf7187fbd3549224` — byte-identical
- Fresh residual SHA-256: `9f22b51820012d001ca2d7eade19d282e65004aefe352f12dcb4c6f818b72f94`
- Embedded EXE SHA-256: `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## GG semantic closure

### `00631290` — `Phyre.Reflection.ClassDescriptorRecursiveObjectFieldCopyTraversal`
The Phyre physics object-factory path passes a class-specific static descriptor root, a freshly constructed destination object payload, and a source reflected payload into the adapter that reaches this routine. The complete body walks member lists and inherited descriptors, invokes the per-member copy helper, resolves member type/target descriptors through virtual accessors, honors descriptor flags and element counts, computes member offsets, and recursively traverses eligible nested reflected objects. This proves generic class-descriptor recursive object-field copying rather than Physics ownership or serialization.

Exact body: **542 bytes**, SHA-256 `972be9cd720552f423c3c992fc503c9841e25ee0ce3484aea621f4435fb58c3c`.

### `0063CD20` — `Phyre.Reflection.MemberDescriptorValueCopyDispatch`
This is called directly for each member by the recursive descriptor traversal. It resolves the member's type descriptor and flags, derives the same descriptor-relative offset in source and destination payloads, obtains element count/width through descriptor virtuals, uses raw `memcpy` for simple fixed-width values, and routes complex/array descriptor kinds through their semantic virtual copy/access operations.

Exact body: **343 bytes**, SHA-256 `bf65b498049b0c6c78aff65dbb8f29d481a37cac34276e0359db37c8e370bff5`.

## Mutation proof

Full deterministic comparison across all **38,161 functions** from certified GF to GG:
- changed functions: **2** — `00631290`, `0063CD20`
- comments changed: **2**
- CodeDomain tags added: **2**
- tags removed: **0**
- functions added/removed: **0 / 0**
- immutable changed count: **0**
- all body hashes/ranges, names, prototypes, thunk state and non-target functions unchanged

## Packing / fresh-reopen proof

Separate closed-file pack reported `open=false busy=false changed=false canSave=false` and explicit `PACK_PASS`. A completely new Ghidra project imported that GZF and independently reproduced **37,987 explicit / 174 unresolved / overlap 0**, the authorized EXE hash, and a byte-identical deterministic all-function snapshot (`d5ef2466ec7ae4e3b68e08fbe913824b57622ddc175a557bdf7187fbd3549224`).

## Corrected-lineage rule

No PE exception/unwind/IP-to-state metadata was used for semantic classification. The Physics factory provides independent evidence for the generic reflection mechanism only; no gameplay or Physics PrimaryOwner was propagated.

## Next frontier

The exact fresh-reopened GG residual contains **174 unresolved functions**. `002F7380` and `00313A00` remain protected and unresolved.
