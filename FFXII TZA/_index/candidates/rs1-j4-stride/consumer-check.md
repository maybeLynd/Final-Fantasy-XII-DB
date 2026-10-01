# RS-1 / J-4 consumer check (FABLE, Claude Opus 5.5, 2026-09-26)

**Corrected claim.** The J-4 box on `resource-section-addressing.md` called the row stride `+0x48` "data-defined"
and said the layout "needs a shipped descriptor instance". The register's RS-1 row carried OPUS's 2026-09-15
narrowing that the extent is "AUTHORED DATA, not a compiled constant". SWE2-DATA's census on the same page
(2026-09-16, *RS-1 answered*) falsified both. `0051F9F0` is the only complete geometry writer, and it takes the stride
from `.text` immediates. Three descriptors exist, at render root `+0x000`, `+0x060` and `+0x0F0`, with strides
`0x50`, `0xC0` and `0x260`; `rowMask` is derived, and it is `0x1F` everywhere.

**Regression:** `_index/candidates/rs1-j4-stride/j4_stride_path.py` (3 checks, FAILS 0: the `+0xD98` store, the `+0x84` read, the three wrapper strides), and SWE2-DATA's `Database/Tools/work/DATA/rs1/census_rowstride.py` for the stride census.

**Added evidence for J-4.** `002ED610` takes the descriptor from `[resolved + 0xD98]`. `0041E3E5` stores
`root + 0x60` at `root + 0xD98`, the `0xC0` descriptor. The path reads the row's `+0x84` (`002ED670`), which rules
out the `0x50` family. The `0xC0` row type is fully declared as `RenderStrideC0Element`.

| Consumer | What it says | Disposition |
|---|---|---|
| `resource-section-addressing.md` J-4 box | "data-defined `+0x48`"; "needs a shipped descriptor instance" | Struck and corrected; box ticked with the answer in this publish |
| same page, *RS-1 answered* section | three compiled strides | Agrees: the source of the correction. Unchanged |
| `OPEN-QUESTIONS.md` RS-1 | OPUS narrowing: "The extent is therefore AUTHORED DATA" | Restated ANSWERED in this publish; the narrowing is kept below as history |
| `OPEN-QUESTIONS.md` J-4 | "the stride comes from a shipped descriptor or not at all" | Restated ANSWERED in this publish |
| `register-triage/register_triage.tsv` J-4, RS-1 | triage notes quoting the authored reading | FABLE's own triage snapshot; superseded by this publish, and not re-edited |
| `authored-data-table-registry.md` lines 503 / 610 / 1281 | "mutable runtime state rather than authored data", about the registry | Different objects; they already say "not authored". Unchanged |
| `_types/types.tsv` `RenderStrideC0Bank` / `RenderStrideC0Element` | root `+0x60`; `0xC0` rows | Agrees. Unchanged |
