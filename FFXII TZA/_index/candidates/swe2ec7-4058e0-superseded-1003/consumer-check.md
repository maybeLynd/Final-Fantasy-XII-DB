# Consumer check: the EC7-206 `004058E0` paragraph on the spawn page (SWE2-EC7, 2026-10-03)

Batch EC7-206 (`e548b7679`) appended a `004058E0` paragraph to spawn-placement-and-retirement.md that
asserted a spawn-record field-apply role. The same page already carries FABLE's 2026-09-30 measurement
of the body, which read it whole and corrected it to a per-frame `+0x178`/`+0x130` step with no spawn
state. The batch-172 frontier snapshot still listed `004058E0` because the FABLE row's interior anchors
sit in a table cell, which the frontier's `Interior anchor` line test does not see.

- **Corrects:** in 05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md, the EC7-206 paragraph
  "`004058E0` (827 B) is the spawn-record field apply `004061F0` runs...". It is struck and marked
  superseded by the FABLE row at the `004058E0` measured-table entry (counter `+0x178` vs `+0x17A`,
  `+0x130` completion bits, child `[+0xD0]` extents `+0x4A`/`+0x48` and scale `+0x98`).
- **Affected:** 05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md (one paragraph; the
  `00405AC5` interior anchor is retained).
- **Consumers:**

  | consumer | state |
  |---|---|
  | the page's 2026-09-30 FABLE row (`004058E0`, 828 B, read whole) | agrees - it is the authority this strike defers to |
  | the page's correction-table row at `004058E0` ("not a spawn function") | agrees - same correction, earlier |
  | the raw call index that placed `004058E0` on this page | superseded - `dd-content-fable-0930` row 17 already dispositioned it ("the body, read whole") |
  | _index/AUDIT-LOG.md EC7-206 entries | revised-here - the addendum records that the batch carried two stale-frontier artifacts |
  | _index/knowledge.sqlite | derived; regenerated from the pages, never hand-edited |

- **Regression:** `check_interior_anchors.py` (boundary-verifies the FABLE row's anchors
  `004059A9`/`004059CC`/`00405A18`/`00405BDB`-`00405BFC` inside `004058E0`'s body - the measurement the
  strike defers to) run 2026-10-03 at `f88367583`: 6,433 anchors, 0 mid-instruction, 0 outside-body;
  `verify_doc_addresses.py` on the page: ok. Both checks re-runnable on the live tree at an ancestor of
  this publish's HEAD.
