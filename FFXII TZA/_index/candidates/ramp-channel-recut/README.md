# RampChannelRecord: 17 "mixed" spans re-cut, 15 scalar rows re-typed float (OPUS, 2026-09-28)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SEM.

**What was wrong in the store.**
- `RampChannelRecord` (0xE0 bytes, 160 records in the block at `*(void**)02B40528`) carried 18 rows reading
  "mixed ... overlapping widths [4, 8, 4] ... NOT resolved". They came from the 2026-09-25 cell census.
- The same census typed 15 scalar rows `uint32` (for example `+0x08`, `+0x2C`, `+0x44`, `+0x9C`). Yet every typed
  access to them is SSE single-precision: `mulss`, `movss`, `addss`.
- The 2026-09-27 flow re-cut held this type out, because its accesses reach past one 0xE0 record
  (`type-flow-census/README.md`, "Held out").

**Where the 8-byte widths come from.** The allocator's pointer walk (`003B56D0`, `add rbx, 0xe0` per record)
initialises the record with **qword stores that span two 4-byte cells**:
- `mov qword ptr [rbx+0x14], 0x3f800000` writes 1.0f at `+0x14` and 0 at `+0x18`;
- `+0x5C`, `+0x78` and `+0x8C` are initialised the same way;
- `+0x1C`, `+0x24`, `+0x50`, `+0x64`, `+0x70` and `+0x80` are zeroed the same way;
- `mov dword ptr [rbx], esi` zeroes the four counter bytes `+0x00..+0x03`.

Those are store merges, not 8-byte fields. Every read of these cells is 4 bytes wide, or 1 byte for the counters.

**Method** ([`ramp_recut.py`](ramp_recut.py)). Three access sources are unioned by site. Each site's kind comes from
`reg_tracking.op_kind` on the certified image.

| source | what it adds |
|---|---|
| [`ramp-flow-accesses.tsv`](ramp-flow-accesses.tsv) | `type_flow_census.py`, `POOL=02B40528 CELLS=02B40528 TYPE_SIZE=0xE0`. This is the `index * 0xE0 + block` pattern of every accessor the contract lists. |
| [`ramp-cell-sites.json`](ramp-cell-sites.json) | `census_receiver_fixpoint.py 02B40528 0 0xE0`, `SEED=cell`, `EMIT_JSON`. This adds the allocator's walk, which the flow census cannot hold. |
| direct decode | `003B6950` (class 0x10) and `003B69B0` (class 0x0E). These are the two setters outside `functions.tsv`, so no census reaches them. |

- **Widths.** `cpe_partial_recut.py`'s rule:
  - reads of 8 bytes or less define fields, and must not overlap;
  - every other access is a 16-byte move or lies on the new boundaries;
  - unread bytes stay DISCOVERED.
- **Types (rule T).** Taken from every access that carries a type:
  - SSE single-precision: `float`;
  - `movsx`: signed;
  - other integer instructions: unsigned;
  - a plain `mov` / `movd` / `movq` carries **width only**.

  A cell moved only by plain moves keeps the store's `uintN` width convention, and its meaning says so. Float mixed
  with integer evidence is not typed.

**Result.**

| before | after |
|---|---|
| 17 `mixed` spans | 37 rows: 34 fields, 3 DISCOVERED remainders (`+0x06` u8[2], `+0x1C` u8[4], `+0x42` u8[1]) |
| 15 scalar rows `uint32` | `float`, with the old type kept as WAS |

- `+0x30` stays DISCOVERED: nothing reads it. The contract calls it a published snapshot with no reader.
- `+0xD8` stays DISCOVERED: nothing touches it.
- `+0x20` / `+0x24` / `+0x28` are moved only by plain `mov`, so they are **width-only** `uint32`. The contract reads
  them as a vec3 that `003B62D0` multiplies; this record does not claim that representation.

**Agreement with the contract.** The cut matches `17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md`
§2 and §14 item 5 (check K):
- four counter bytes;
- `+0x14` and `+0x18` separate;
- `+0x1C` unread;
- three cells at `+0x20..+0x28`;
- `+0x30` unread.

Meaning stays in the contract. The store rows claim width and type only.

**Checks** (`python ramp_recut.py`; add `--receipt` to regenerate both receipts):
- **R:** every site decodes at its width.
- **A:** the allocator stores.
- **D:** the unlisted setters.
- **C:** the controls: `+0x30`, `+0xD8`, a hand float+integer pair rejected, plain moves width-only.
- **K:** the contract agreement.
- **S:** the regression. It FAILED before the patch (17 spans, 15 re-types) and passes after.

**Found on the way: a producer regression, fixed.** `census_receiver_fixpoint.py`'s `EMIT_JSON` per-site
`[read, write]` flags had been `[0, 0]` for every site since 6b6a423db. The access label and the per-site key shared
one variable name. The printed totals were right. The receipt here was produced after the fix; see the correction in
`access-flag-producers/README.md`.

**Run receipt.** Run verified at daec30974:
- `ramp_recut.py --receipt` FAILS 1 (S) before `--patch`, then FAILS 0 after;
- `types_index.py --validate` 0 errors;
- `check_census_widths.py` 0 disagreements;
- `typing_check.py` FAILS 0;
- `test_access_policy_producers.py` FAILS 0.
