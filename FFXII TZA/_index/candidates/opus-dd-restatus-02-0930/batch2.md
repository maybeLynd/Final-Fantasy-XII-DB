# OPUS owner re-status, `02` batch 2: eleven pages (OPUS, 2026-09-30)

These pages had been reconciled by SWE2-CONTRACT's DD residue batches (their rows answered by SWE2-DATA's
`rc22-34-resource-readers-0930` and the round records). Where a table or section still says "no reader found", the page
already carries SWE2-CONTRACT's *Superseded readings* note naming it. The status word was left for OPUS's owner read.

| page | change | rule |
|---|---|---|
| `as7-menu-graphics-containers.md` | re-status; the superseded-readings note covers §2/§3 | READY |
| `btm-exfont-bitmaps.md` | re-status; the note covers §2–§4 | READY |
| `chse-character-se-tables.md` | re-status, plus two stale lines pointed at their answers ("SB-2 is open"; the Audio helper `003A1650` "not read") | READY |
| `cl2-menu-colour-tables.md` | re-status; the note covers §3 | READY |
| `lst-menuquest-list.md` | re-status; the note covers §2 | READY |
| `mg-worldmap-mesh.md` | re-status; the note covers §2 | READY |
| `lmap-menumap-location-graph.md` | re-status; §10.5's items are answered in place | READY |
| `mrp-menu-resource-packages.md` | re-status; two §3 rows get pointers to §2.3 / §7; `unk2C` is a declared limit | READY |
| `cmap-menumap-common-sublocation-directory.md` | re-status (layout and loader read; ~~nothing carried as open~~ the entry `+2` auxId and section 2's value semantics are declared unbound limits) | READY |
| `wmap-menumap-world-map-graph.md` | re-status (~~the same~~ layout and loader read; the area `+8` aux i16 and the `B2` sub-table are declared unbound limits) | READY |
| `the-source-block-mover-and-separate-consumer-refresh.md` | re-status. OV-45/46 are answered, OV-47 SUPERSEDED, OV-48/49 NOT A QUESTION. The SECTION-07 content is accepted by `FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929` | READY-WITH-POINTER |

**The one new fact (OPUS, static).** The MRP header relocator `002A00F0` reads `+0x24` and `+0x28` (`002A011E`,
`002A0137`, `002A0156`) and never `+0x2C`. So `unk2C` has no reader on the header path.

**A-drift.** `adrift_report.py` after this batch shows no new refused row (still 10). Two new A members fall in rows already
refused and routed to SWE2-EC7: `0050E300` (verb adapters) and `001FFF00` (JsonBox). The report file EC7 reads is
refreshed.

*(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-dd-02-b2-0930/REVIEW.md): corrections 1-6 are applied on the pages (as7, btm, lst and mg stale rows annotated; lmap's two PARTIAL sentences marked; a "What this document does not claim" section on cmap and wmap). The cmap / wmap status-line wording is a status-line edit and is proposed for OPUS in [swe2struct-awn-wave-b-1001](../swe2struct-awn-wave-b-1001/README.md). The optional source-block-mover front-matter items are not applied.)*
