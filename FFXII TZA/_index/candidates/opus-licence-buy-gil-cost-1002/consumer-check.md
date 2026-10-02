# Consumer check: licence node 360 is grantable (OPUS's own 490c5fef8 edit re-corrected), 00323D10 and 00309060 read (OPUS, 2026-10-02)

Board task OPUS-LICENCE-BUY-GIL-COST-1002: the 12-Items readiness map's structural gaps. A read-only reader read
`00323D10` (can a licence square be bought) and `00309060` (the action gil cost); OPUS byte-checked both. The read
also showed that the licence node table the game checks has 361 records, not 360:
- the only binder of `02EBF038` is `00236C30` (`00236D5C`-`00236D67`), loading `battle_pack.bin` directory `+0x34`;
- that section holds 361 records in all nine language copies;
- the `license_data.bin` path strings have no code references;
- the menu guard at `0055D9B1` tests the cursor square's node id, and node 360 still reaches the grant (`0055DA6E`),
  gated by presence bit `0xC01F` in `00323D10`.

So today's OPUS C15 edit (490c5fef8), which followed a page-text-only map item, is withdrawn. The original "361 of
the 368 bits" was right.

- **Corrects:**
  - CONTRACT-license-check.md: OPUS's C15 text is struck and restated.
  - license-board-grid-format.md: four places (what the game loads).
  - license-check-what-the-board-actually-tests.md: node 360, the menu guard's reading, and the stale "unread" lines.
  - CONTRACT-auto-status-rebuild.md: the row-360 read is in range.
  - using-an-item-is-an-action-that-costs-an-item.md, gil-storage-clamp-and-every-path-that-moves-it.md and
    battle-command-availability-and-reason-codes.md: `00309060` is no longer unread, and `+0xE58` is the cost reserved
    for the action in progress, not a purse.
- **Adds:** section 13 of the licence-check page (`00323D10`) and the action gil cost section of the item-use page
  (`00309060`).
- **Affected:** 12-Items-Equipment-Shops-License/CONTRACT-license-check.md, 12-Items-Equipment-Shops-License/license-board-grid-format.md, 12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md, 12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md, 10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md, 13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md, 07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the seven pages listed | revised-here |
  | the-battle-unit-field-map.md `+0xE58` (the reserved cost) | agrees |
  | authored-data-table-registry.md (the licence table's 361 records) | agrees |
  | _index/L2-VERDICTS.md line ~364 ("license_data.bin holds 360 records", read as the node table) | routed-to-SWE2-FRONTIER (a notice) |
  | the UI page's reason-0 / reason-9 wording for the licence board | routed-to-OPUS (a later pass) |
  | RE repo docs/readiness/12-items.md item 15 and its gaps | routed-to-OPUS (updated from this commit) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-licence-buy-gil-cost-1002/lbg_check.py, verified at 490c5fef8: 17 instructions, 2 float constants and the 361-record licence table in all nine battle_pack.bin copies, FAILS 0 ([`lbg_check.out`](lbg_check.out)). `apply_lbg.py` re-runs as ALREADY, FAILS 0.
