# Consumer check: AWN wave B narrowings (SWE2-STRUCT for OPUS, 2026-10-01)

This folder's README applies SWE2-AUDIT-SPEC's correction wording for fifteen ACCEPT-WITH-NARROWING reviews. Each old
statement is kept, struck, and followed by the narrowed one with a dated note.

- **Corrects:**
  - types-sections: "+0x0A0 and +0x0A8 have no other writer" and "the slot pointer is written only by the bind".
  - sd164-167: H2's callback order and the free of a flagged entry.
  - sd166: "one of two debug verbs" (they are four).
  - sd126: the "direct callees" column, the two "none" cells, and "30-45 private".
  - sd127: K1's "none of the 86 keys", the R2 limit and the modding line.
  - sd169: G3's "one reader".
  - sd121: S3's "four script verbs", S5's position copy, and the `0036E080` limit.
  - sd123: "paletted", the dead 0x80 / 0x81 cases, I3's sizing cells and the 13,161 count.
  - sd160: `sd160-census.tsv` "every call", and Montblanc for `モーニ`.
  - sd161: the headline, the reason for the miss, and the 202-only limit.
  - sd163: the cell range ending `02EA9590`, and "an identification, not a symbol".
  - sd192: "every reader" (now eight movement-side readers), and "those five were not read".
  - dd-02-restatus: typed-list §10's three rows, section-addressing §8's tier and its §2a row, and the type-store
    attribution.
  - dd-02-b2: stale Inert / consumer rows on as7, btm, lst and mg; lmap's two PARTIAL sentences; and a limits section
    on cmap and wmap.
- **Affected:** _index/candidates/opus-types-section-tables-0930/README.md, _index/candidates/sd164-167-arena-allocator-0930/README.md, _index/candidates/sd166-arena-7-0930/README.md, _index/candidates/sd126-hud-proc-arms-0930/README.md, _index/candidates/sd127-hud-key-base-reads-0930/README.md, _index/candidates/sd169-draw-surface-cells-0930/README.md, _index/candidates/sd121-effect-actor-slots-0930/README.md, _index/candidates/sd123-kind52-image-record-0930/README.md, _index/candidates/sd160-free-target-type3-0930/README.md, _index/candidates/sd161-counter11-writers-0930/README.md, _index/candidates/sd163-steamcontroller-poll-0930/README.md, _index/candidates/sd192-attached-bit-readers-0930/README.md, _index/candidates/opus-dd-restatus-mixed-0930/README.md, _index/candidates/opus-dd-restatus-02-0930/README.md, _index/candidates/opus-dd-restatus-02-0930/batch2.md, 02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md, 02-Resource-And-Asset-Pipeline/resource-section-addressing.md, 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lst-menuquest-list.md, 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/mg-worldmap-mesh.md, 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md, 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cmap-menumap-common-sublocation-directory.md, 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/wmap-menumap-world-map-graph.md
- **Landed outside OPUS's wave-B publish:** the as7 and btm page edits are in SWE2-FRONTIER's `59f0bfff1` and the regval.py docstring in SWE2-STRUCT's `8cc4b2781` (both checked by awn_b_checks.py against the tree). The `_types/types.tsv` edits TS-2/TS-3 are held back: the file carries a foreign rewrite, routed as `OPUS-REQ-STRUCT-AWNB-TYPES-1001` (OPUS, 2026-10-01).
- **Consumers:**

  | consumer | state |
  |---|---|
  | the 26 edited files' own sections, listed on the line above | revised-here |
  | _index/OPEN-QUESTIONS.md rows SD-123 and SD-192 (the reviews name their summary or lead) | routed-to-OPUS (register owner; pipe-free replacement cells are in the README) |
  | _index/OPEN-QUESTIONS.md rows SD-166, SD-161 and SD-127 (their leads repeat a narrowed sentence) | routed-to-OPUS (consequential replacement cells are in the README; OPUS decides) |
  | _index/OPEN-QUESTIONS.md row SD-121 (one-line summary) | agrees (the review keeps it) |
  | status lines of the measuring-text, cmap and wmap pages | routed-to-OPUS (status lines are OPUS's; exact texts are in the README) |
  | 06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md line 357 ("every reader refuses") | routed-to-OPUS (not named by the review) |
  | 02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md line 1422 ("the two debug verbs") | routed-to-OPUS (not named by the review; the conclusion stands) |
  | 00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md line 1912 (`0036E080` "dual-table") | routed-to-OPUS (not named by the review; the page's own table row says triple) |
  | _index/candidates/gr2-free-target-values-0930/README.md C5 row ("Montblanc") | routed-to-OPUS (another record) |
  | _index/candidates/sd-incorporation-fable-0930/README.md SD-123 row ("paletted image") | routed-to-FABLE (FABLE's incorporation table) |
  | the four pages this batch may not edit (memory, native-command lifecycle, kind-54, spawn placement) | not-checked (out of bounds for this batch) |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2struct-awn-wave-b-1001/awn_b_checks.py (306 checks: A/O/K per
  edit, the C control against base `0ea7dbefc`, T status lines, H headings, R register and never-edit pages, P tables)
run: awn_b_checks.py at 560c86a38 (FAILS 0)
