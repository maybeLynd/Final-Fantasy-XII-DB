# SD-22: the options-screen rows that send the volume commands 0x13 / 0x14 / 0x15 (OPUS, 2026-09-30)

Register row SD-22 was registered by SWE2-DATA (`f7a3292bd`, sqex-sd-sound-driver-architecture.md §7 G-3). It asks which
rows of the options screen send settings commands `0x13` / `0x14` / `0x15`, the Music, Sound Effect and Voice Category
volumes. The row noted that the answer is "the authored or constructed row table, not read". This record reads that
table. It is static. The checker is `sd22_volume_rows.py` (output `sd22_volume_rows.out`, `FAILS 0`). It uses
`Tools/analysis-kit/gfz-scripts/retool.py`.

## The answer (OPUS)

**Three rows, one per command. The options menu tree is static data in the image, and each row sends its own node id
as its command id.**

- **F1: the menu tree.** The row builder `0023ED80` reads it from a table of 45 node pointers at `01E0BF60`, indexed by
  a row's id byte `+0xC0`. Each node holds:
  - a type byte, and its own id at `+1`;
  - a child count at `+2`;
  - 6-byte child entries from `+4`, each starting with the child's id.
- **F3: where the three rows sit.** Nodes `0x13`, `0x14` and `0x15` are type-6 rows. Each is a child of the three root
  menus `0x00`, `0x01` and `0x02`, in that order, after node `0x12`, and of no other node. Their child entries carry
  the label and help fields `fc04 000d`, `fd04 010d` and `fe04 020d`.
- **F2: the handler.** Type 6 selects handler `0023EBE0`, through the arm table at `0023EE78`.
- **F4: how the id reaches the row.** The builder passes the child's id as the creation payload's `+8`, and
  `0023EBE0` stores it into the row's `+0xC0` (`0023ECBD` → `0023D4F0`, `0023D504`).
- **F5: the command.** When the row's value changes, `0023EBE0` calls `00240750` with that byte as the command id
  (`0023EC6E` / `0023EC7A`).

So in every options menu: row `0x13` sends command `0x13` (Music), row `0x14` sends `0x14` (Sound Effect), and row
`0x15` sends `0x15` (Voice Category). The rows are not handled by `0023D6B0`, the procedure the page names for other
rows; they are type-6 rows under `0023EBE0`.

**For the player:** these are the three volume sliders in the options menu. Each exists once in each of the three
option-menu roots, and changing one sends its own volume command.

## Limits (OPUS)

- **Labels.** The label and help text ids in the child entries (`0x04FC`–`0x04FE`, `0x0D00`–`0x0D02` if read as
  little-endian words) are not decoded against the menu text banks here.
- **The three roots.** Which in-game screen each root menu `0x00` / `0x01` / `0x02` is was not read.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
