# Consumer check: DD batch 10 corrections on six pages (SWE2-CONTRACT for OPUS, owner re-status pending, 2026-09-30)

SWE2-CONTRACT's batch 10 (this folder's README) answered the six pages' residue in place and struck their superseded
statements. No status word was moved; OPUS re-statuses after its owner read.

- **Corrects:**
  - in the-widget-message-protocol.md: the §7 items "Any meaning for ids 8, 9, 11, 17, 21–23, 26, 29, 30, 53, 285,
    287, 289", "That the 11 upper-bound handlers answer the ids their bound spans" and "That the 24 unparsed handlers
    answer nothing", and the §10 note "Not read: whether the other receivers (002D2DB0, 005691E0) return non-zero";
  - in efx-and-efb-effect-containers.md: §2's "The chunk handlers' own retention, and the lifetime of the EFB buffers
    the borrowed pointers name, are not read", the §4 cell "What 00333C80 (889 B) and 004FF270 (55 B) do to the
    records is not read", and the §7 items "FUN_003A7E80 and FUN_003A79C0 are the handlers and neither was read",
    "The version split across the shipped corpus", "That +0x08..+0x0F is engine-wide inert", "That 0x003EDAD0 and
    0x0026FB90 are the only entry points" and "Anything about .efb's internal structure beyond its header";
  - in fte-fct-texture-colour-tables.md: the three Residue bullets (FTE +0x10 and the cache key; FCT +0x08 and the
    page-1/2 bindings; "UQ-218 stays PARTIAL");
  - in fef-and-motion-entries.md: "0x12 beyond name/callees" and "02B64380 row meaning stays open (first bullet)";
  - in ftr-node-table.md: the flag-table cells "a fixed fan of ~16 u16 aux indices" and "Whether shipped records set
    them is the census's to say";
  - in the-unit-shape-distance-primitives.md: the §3 question "Whether the shape record's +0x10/+0x50 pair is
    authored data or filled per-query …" and "their full contents are cited from the authority image, not
    reproduced here".
- **Affected:** 16-UI/Widget-Object-Model/the-widget-message-protocol.md, 17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md, 17-Presentation-Rendering/Model-And-Motion-Formats/fte-fct-texture-colour-tables.md, 17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md, 17-Presentation-Rendering/Model-And-Motion-Formats/ftr-node-table.md, 06-Movement-And-Navigation/the-unit-shape-distance-primitives.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the six pages' own sections and status lines | revised-here |
  | CONTRACT-widget-object.md §15c (the 56-id recount) | agrees (no id count changes; the three unparsed rows are read) |
  | widget-message-handlers.tsv (its 002985C0 note calls the jump a genuine open edge) | routed to its owner; the page answers the edge (003EE420 answers 1, 2, 4) |
  | effect-element-type-dispatch.md and type_census.py (the full-stream walk) | agrees (the 0xD0 count 1,437 is this batch's control) |
  | fef-and-motion-entries.md op 0x28 (lane map at def +0xA, request slots at def +0x2C) | agrees (00333C80 recomputes the lane nibble over the same eleven bytes) |
  | the-map-ctrl-pack.md (00377DC0 and its two completions) | agrees on the path and the arms; gives 00378230 as 114 B against the v4 extent of 619 B (routed) |
  | how-a-status-shows-on-a-character.md (record modes 0, 2, 3) | agrees |
  | the-element-types-40-42-a0-ab-d0-d1.md (00465CD0 passes byte +0x235) | agrees; this batch adds that the byte is definition +0x146, gated by +0x144 bit 2 |
  | the-authored-presentation-command-handlers.md (command 0x16 census, value 0xFFFF in all 373) | agrees and is cited |
  | fdm-and-for-entries.md (the w2/w4/w6 source) | agrees and is cited |
  | EXP-139 (names one plant of 0022DE60) | routed; this batch finds a second, 0023126A |
  | heading-speed-to-position-delta.md (calls 00381450 the heading delta's length arm) | disagrees with the box-primitive reading this page and its falsification pass hold (routed) |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2contract-ddres-b10-0930/b10_checks.py (245 checks, FAILS 0,
  including the corpus walks of all 3,698 effect files and 1,066 models, and control X1 against the archive).
- run: b10_checks.py at 59ec09a95 (245 PASS, FAILS 0, re-run by OPUS on the worktree)
