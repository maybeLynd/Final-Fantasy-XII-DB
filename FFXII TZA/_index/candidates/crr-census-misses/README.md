# CharacterRenderRecord: three DISCOVERED spans the access census missed (OPUS, 2026-09-27, BT-2)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**Why look.** The `+0x6C8` correction (7703e21cf) showed that `character-render-record-accesses.tsv` (OPUS, 734d34df6)
tracks registers linearly. It drops `002EDF90`'s four literal `+0x6C8` stores, because rcx is re-defined on the
fall-through path. It also records a false `+0x6E7` "addr" row, because it carries the fall-through `rdx` into a branch.
So its "no censused access" is not proof that a span is untouched.

**Scan.** Every access in the image that lands in one of CharacterRenderRecord's 40 DISCOVERED spans, on a base with no
displacement at or past `0x740` that also addresses `+0x284`. Candidates were then kept only after a per-site receiver
proof.

**Kept (the control's M1–M3):**
- `+0x4B8`–`+0x4BB`: the class-`0x0B` selector-choice cache, one byte per selector kind (0 / 2 / `0x0A` / `0x10`).
  `00417110` writes the record's byte and, for an attached record (`+0x284` bit 27, parent at `+6`), reads the parent's.
  The record is `[entry + 0x2E0]`; the parent is pool-formed. FABLE's page §6 already described this.
- `+0x6D8` / `+0x6DC`: entry bit 13, and the selector result (choice in the low word, addend in the high word).
  `00417110` writes both.
- `+0x110`: `00429140` zeroes it with `sourceBindingPtr` `+0x108`.

**Rejected (X1–X3, kept in the control):**
- `00417110`'s `+0x60` and `+0x8C` qword stores come after `004172A6 lea rbx, [rdi + 0x30]`, a 0xA0-stride entry array.
- `002E6BD0`'s `+0xEC` store is on an actor (it reads `[rdi + 0xC0]`).
- `002EE1D0`'s `+0x60` read is on `rax*9`.
- `+0x62E` was already documented as carried by a 16-byte block store.

**Effect.** DISCOVERED in CharacterRenderRecord goes from 192 bytes in 40 spans to 176 bytes in 37.

**Not done here.** A flow-aware re-census of the whole record. The census file is kept as a dated result, and its
defect is recorded here and on BT-2. The re-census is OPUS's next step.

**Run receipt:** `crr_census_misses.py`:
- FAIL (S) on the store at HEAD before the patch;
- PASS M1–M3, X1–X3 and S on the patched copy, with all 5 mutants rejected (2026-09-27);
- `types_index --validate` on the patched copy: 0 errors, 0 gaps.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` CharacterRenderRecord `+0x4B8`, `+0x6D8` (split into `+0x6D8` / `+0x6DC`), `+0x110` | replaced; the old rows are kept in the evidence cells | revised-here |
| `_index/OPEN-QUESTIONS.md` BT-2 | narrowing prepended; row stays OPEN | revised-here |
| `17-Presentation-Rendering/Character-Render-Records/how-a-presentation-entry-picks-its-track.md` §6 | already describes `+0x4B8`–`+0x4BB` and `+0x6D8` / `+0x6DC` | agrees |
| `17-Presentation-Rendering/Character-Render-Records/character-render-record-accesses.tsv` | a dated census with a flow-insensitivity defect; not rewritten | follow-up (OPUS re-census) |
