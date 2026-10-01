# NavRunStateBlock extent, measured from the shipped packs (OPUS, 2026-09-25)

**Question.** S-51's `types` cell (L2-VERDICTS, S-51) was held on one thing: `NavRunStateBlock`'s
size read `UNRESOLVED`. The verdict treated the type as the whole heap copy of the pack's slot-4
section. That copy's size, `*(uint32*)(section - 0x28)`, differs from map to map.

**Instrument.** `nav_root_extent.py` runs over every `plan_master/map_ctrl/**/*.mpk` in the
extracted shipped data. Its slot-4 parser is the one in
`_experiments/evidence/navigation-dataset-layout/census.py`, whose positive control finds slot 4 in
461 files. Output: `nav_root_extent.out.txt`. The run is static: shipped data only, no live
process.

**Results, 461 of 461 sections:**

| measured | result |
|---|---|
| lowest of the six offsets at `+0x0C..+0x20` | `0x30` in 461 of 461 |
| order of those offsets | always `+0x0C < +0x10 < +0x14 < +0x18 < +0x1C < +0x20` |
| `+0x00` | `1` in 461 of 461 |
| `+0x2C..+0x2F` | zero in 461 of 461 |
| `+0x24` | 0 in 433; otherwise 1 (10), 2 (3), 7 (2), 16 (2), 20 (2) |
| `+0x28` target | inside the section in 364; at its end in 90; 16 bytes past it in 7 (all 97 of these have `+0x24 == 0`) |

**Reading.**
- `Navigation_BindAndRebaseDataset` (`00384160`) adds the block's address to each stored offset, so
  the offsets count from the block's start.
- The first table begins at `+0x30` in every shipped map, so the root block is a fixed
  **0x30-byte header**.
- The heap allocation is the whole section: the header, followed by the tables it names, each of
  which is its own declared type.

That is the variable-size rule, now recorded on the type.

**Not claimed.**
- What `+0x00` means.
- What `+0x24` means. Bytes after `+0x28`'s target run 32, 80, 64, 48 or 34 per unit of `+0x24`,
  so `+0x24` is not established as that table's count.
- What `+0x28` names.

**A correction found while writing the rows.** The 2026-09-22 consumer census (OPUS) attributed
accesses to `+0x00`, `+0x04` and `+0x08`. Re-reading the cited sites:

- `0038302F` and `00383037` (writes of `0xFF`) go through `r8`, the third argument of `00382FF0`
  (`0038301C mov rsi, r8`). Nothing loads `02AEDFB0` before them.
- `00382D7A` reads through `r14`, the first argument of `00382D10` (`00382D50 mov r14, rcx`).

None of these is this block. I re-ran the scan with the rules-hardened `trackscan` (seed
`[02AEDFB0]`, deref mode, whole image) over `+0x00/+0x04/+0x08/+0x24/+0x28/+0x2C`. It finds three
accesses:

- `003832D6` (`+0x00`, flagged suspect): `rax` there is `[rsp+0x78]`, which is `00382FF0`'s second
  argument (`00383027 mov [rsp+0x78], rdx`), so it is not this block.
- `00384160`'s own read and write of `+0x28` (the rebase).

**No code access to `+0x00`, `+0x04`, `+0x08`, `+0x24` or `+0x2C` remains attributed.** `+0x04` (vertex count) and `+0x08` (portal count) are named from shipped data only,
per `navigation-dataset-layout/census.out.txt`, which matches both counts in 461 of 461.

## Block 248 (OPUS, 2026-09-25): the last two references, `+0x1C` and `+0x28`

`refs_nr28b.py`, `refs_nr28c.py` and `refs_nradj.py` (outputs `*.out.txt`) use the same slot-4 parser and the same
461 sections.

- **`+0x1C` → `NavRegionAdjacencyEntry[regionCount²]`.** `00383850` reads `word[base + (a*regionCount + b)*2]`
  (`00383883`–`00383892`). 0 means no portal (cost `0x7FFFFFFF`); otherwise the value is a portal index. Data: the
  `+0x1C..+0x20` gap holds `regionCount² × 2` bytes in 461/461 (slack 8/14/16), and every entry is below
  `portalCount` in 461/461.
- **`+0x28` → `NavTrailerRecord28[+0x24]`, stride 0x20.** The data settles what the `+0x24` count question above
  left open:
  - `+0x24 == 0` exactly when the tail from the `+0x28` target to the section end is all zero (433/433);
  - otherwise the tail is `+0x24 × 0x20` bytes of records, then zero padding to the section's 64-byte alignment
    (28/28, pads 0/16/32/48);
  - the table always sits after every other table (461/461);
  - record `+0` is 0 or 1 in all 240 records.

  The earlier "32, 80, 64, 48 or 34 per unit" figures divided the padding in with the records. No code reads the
  table (the tracked census above), so its meaning is not claimed.
