# LegacyPs2GsTextureContext +0x40: two nested chunk records, declared; three phantom rows corrected (OPUS, 2026-09-28)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SEM.

**What was wrong in the store.**
- `LegacyPs2GsTextureContext` +0x40..+0x10F held **26 parent rows**. Six of them read "mixed ... overlapping widths ... NOT
  resolved", and each 0x68-byte element's interior was recorded twice, at +0x40 and at +0xA8. The element had no type.
- The ctor-seeded census follows `rbx += 0x68` without bounding the loop. It therefore reported the clear `00231F50` at
  bases +0x110, +0x178 and +0x1E0, three elements that do not exist.
- Two rows, `field0118` (`00231F55`) and `field0148` (`00231F69`), were **TYPE RESOLVED u64 with a phantom as their only
  evidence**. `mixed0110` cited `00231F52` beside the constructor's own store.

**What the image says** ([`lgs_nested68.py`](lgs_nested68.py)).
- **L1: the extent.** `002F6AB0` clears the elements in a loop that runs exactly twice:
  `lea rbx,[rcx+0x40]` / `mov edi,2` / `call 00231F50` / `add rbx,0x68` / `sub rdi,1` / `jne`.
  - It binds `+0x40` (map-ctrl-pack tag 31) and `+0xA8` (tag 17) through `00232380`.
  - Those three calls are the only calls or jumps to either function in `.text`.
- **L2: the layout,** from the binder's six-arm jump table:

| offset | field | from |
|---|---|---|
| +0x00 | `chunk00` void* | tag 0 |
| +0x08 | `tag5Ptr08` void* | tag 5 |
| +0x10 | `tag3Ptr10` void* | tag 3 |
| +0x18 | `tag4Payload18` void* | tag 4, the chunk + 0x10 |
| +0x20 | `tag1Ptr20` void* | tag 1 |
| +0x28 | `tag2Ptr28` void* | tag 2 |
| +0x30 / +0x34 | `product30` / `product34` int32 | tag-0 chunk dword products (`imul`) |
| +0x38 / +0x3C | `halfMinus38` / `halfMinus3C` int32 | a signed half (`cdq` / `sar 1`) minus a chunk dword; read as int32 by `cvtdq2ps` at `00233064` / `00233067` |
| +0x40 | `copied40` u8[4], DISCOVERED | a dword copy, read as a word by `00231AC5`: not resolved |
| +0x44 | `tag4Count44` uint32 | the tag-4 chunk's first dword; width-only |
| +0x48..+0x67 | `zeroedAtBind48`..`60` u8[8] each, DISCOVERED | qword zeroes at the end of every bind; never read |

- **L3** proves the signed arithmetic and the int32 reads.
- **L4:** `00231F50` zeroes +0x00..+0x47 with nine qword stores. The stores at +0x30 / +0x38 / +0x40 span two dword cells
  each, and that is where the "mixed [4, 8]" widths came from.
- **C:** the 16 rows tile 0x68 exactly.

**The changes** (FABLE's rule 0: one description per byte, and the byte belongs to the innermost declared type).
- **New type** `LegacyPs2GsNestedChunkRecord68`, 0x68 bytes. It has two instances, and its route is
  `EMBED LegacyPs2GsTextureContext +0x40 stride=0x68 count=2`.
- **Parent:** the 26 rows become one region row, `chunkRecords040` (`LegacyPs2GsNestedChunkRecord68[2]`, 208 bytes).
  - The absorbed rows are listed verbatim in its evidence.
  - SWE2-STRUCT's `qword0040` and `qword00A8` migrate into the child's +0x00 row, with their evidence verbatim.
- **Phantoms:**
  - `field0118` and `field0148` become DISCOVERED `unobservedSpan` rows. The old text is struck and the old type kept as WAS.
  - `mixed0110` strikes `00231F52`. Its one real access is the constructor's qword store `002F6AEF`, which also covers
    `dword0114`.
- **Meaning** stays on `03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md` §3.5, which already describes `00232380` the
  same way. No page changes.

**Scope of the phantom.**
- The same unbounded loop produces phantom hits at +0x128..+0x220.
- Those rows cite other, real sites (SWE2-STRUCT's route-seeded census), and only the three rows above rest on a phantom.
- The census tool itself is unchanged here. Bounding a loop's trip count is a method change, and it goes to the census
  owner as a finding: a phantom from `add reg, stride` past a counted loop.
- *Later the same day:* the census now marks such sites (`enumerated_sites` in `EMIT_JSON`), and one more row resting on
  one was corrected. See `../census-enumerated-sites/`.

**Run receipt.** Run verified at aef2e3e57:
- `lgs_nested68.py` FAILS 1 (S) before `--patch`, then FAILS 0 after;
- `types_index.py --validate` 0 errors (796 types);
- `check_census_widths.py` 0 disagreements;
- `check_type_refs.py` 0 dangling references;
- `check_embed_overlap`, `check_embed_parent_fields`, `check_ctype_widths`, `check_route_span_overlaps`,
  `check_duplicate_declarations` and `check_zero_width_fields` name neither type.
