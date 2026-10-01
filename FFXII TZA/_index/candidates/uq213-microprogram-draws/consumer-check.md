# Affected-consumer check: FABLE's VU1-page counts and tag readings corrected by UQ-213 (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md (§2.3 the program count and call sites, §2.4c the tag rate and the element-type table, §2.4d the hand-read builders)

run: uq213_programs.py at bbd3af82a (worktree = that HEAD plus this package), 4 checks, FAILS 0; U1–U3 measure the
count correction. The tag corrections were re-read at the cited stores; `vif1-gif-tags.tsv` holds the `0x6A` and
`02AE9D50` tags.

| consumer | what it says | state |
|---|---|---|
| §2.3 (FABLE, 2026-09-13) | "76 call sites register 29 programs"; "Together: 47 distinct microprograms" | revised-here: 72 call sites; 57 programs (the ten through `003A33B0` / `003A2F70` named) |
| §2.4c (FABLE, 2026-09-20) | "45 of the 74 builders carry at least one tag" | revised-here: sixteen more do |
| §2.4c element-type table, `0xA6` / `0xA8` and `'j'` `0x6A` rows | "whatever PRIM the GS already holds"; "none found" | revised-here: a triangle fan through `02AE9D50`'s A+D PRIM `0x5D`; `0x6A`'s tag is in co-template `02AE9140` |
| §2.4d (FABLE, 2026-09-20) | "nothing tag-shaped in any of them" | revised-here: `00476C80`'s fill loop writes an A+D tag (PRIM `0x5D`) |
| the page status line and the UQ-213 box | "the 47 microprograms" | the box and status wait for `FABLE-REQ-FRONTIER-CHECKLISTS-SKIP-RETAINED-PREIMAGES`; five retained copies carry the same box |
| §2.4a (SWE2-DATA, 2026-09-16) | "`004A8860`, `004C3610` are never hub-called" | routed-to-FRONTIER (`FABLE-REQ-FRONTIER-UQ213-PEER-ITEMS`): the hubs tail-jump to them (`0037E0E3`, `0037E33F`) |
| `members/vu1-region-functions.tsv` (FRONTIER) | the ten programs rowed "VU-state-toucher, not installed" | routed-to-FRONTIER in the same request |
| `_index/candidates/uq204-element-type-emits/uq204-element-type-emits.tsv` | one program per type for `0x80`, `0x82`, `0x83`, `0x86`, `0x87` | revised (queued publish `uq204`): the second POINT program is listed |

Grep of "47 distinct", "76 call sites", "45 of the 74", "nothing tag-shaped" and "none found" across the database,
2026-09-27.
