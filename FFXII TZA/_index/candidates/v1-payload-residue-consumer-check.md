# Affected-consumer check: V-1, the save payload's measured tiling and all-routes residue (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The ruling** (evidence: `_index/candidates/v1-payload-residue/`):
- The register's "~470 bytes mapped" is history. The store tiles all 353,424 bytes with no gap.
- 13,953 B are UNKNOWN. 12,018 of them are eight top-level spans that no entry route reaches: the getters, the
  slots, and absolute operands into all four buffers. This is reserved space in AA-5's sense.
- The remaining 1,935 B lie inside five embedded types and keep V-1 open.

**No accepted knowledge is replaced.** The earlier absence rows and the 2026-09-19 bulk-clear section stand. This
adds the routes they did not cover.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` V-1 | ADVANCED → NARROWED; prior status kept as history | revised-here |
| `_types/fields.tsv`, eight SavePayload residue rows | evidence cell gains the all-routes result; meaning/confidence unchanged (UNKNOWN) | revised-here |
| `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md` | new section with the tiling table and the census | revised-here |
| the five embedded types' UNKNOWN rows | untouched; they are V-1's residue | routed-to-SWE2-AUDIT-SPEC (review only) |

**Regression:** `v1_residue_census.py`. It fails if any of the following happens:
- the store's SavePayload tiling stops closing at `0x56490` (K0);
- any control goes empty;
- the planted access is missed;
- the raw sweep misses `00229B81`.

It reports any residue offset a route reaches.

Run receipt: `v1_residue_census.py` executed at 5d41f8a5c (result.json sha256 `93f2382a9142206750f67dfe7d919bfb86bca9941bd5a17268c9a82e937dd5f2`).
