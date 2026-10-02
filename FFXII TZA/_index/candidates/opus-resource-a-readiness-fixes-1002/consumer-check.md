# Consumer check: 02-Resource contradictions (part A) from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-02-VALUES-1002, part A. A cloud session mapped `02-Resource-And-Asset-Pipeline/` from a
text snapshot (report `cloud-reports/re-readiness/02-resource.md` in maybeLynd/Final-Fantasy-XII-DB). Its value items
were page-text only. A local read-only pass decided the 60 items in report lines 624-1008 at the shipping image and in
the shipped data, and OPUS re-checked a sample (`resource_a_check.py`). The pass covered four groups:
- the file-size table, request queue and read path;
- arena, tree, handles and image addresses;
- section addressing;
- the authored data registry and row lookup, plus archive, st2e and text.

Corrected at the bytes:
- `0032E620`'s fourth argument is the byte count (`0032E870+0xBC`), capped at `0x80000` (`0032E620+0xF3`).
- `0046DD50` is dormant, and its state 2 rounds up (`0046DD50+0x96`).
- `002DF6C0` serves kind `0xFF` only (`0032E070+0x67`).
- The two rebase loops repoint 767 and 319 entries (`003A9BA0+0xD`..`+0x50`).
- The handle range is exactly [-2^31, 2^31).
- The external-source release removes the node after a generation check (`003AB880` -> `0036A000`).
- `0024D540` has three callers.
- `0036BC60` is 887 B. There are two pools of 32 records, not one of 64.
- The resource entry is the `[+0xD90]` row, `0x50` bytes (`00409F10+0x13`).
- Section addressing:
  - `00409780` is 429 B, and its fifth argument receives the offset.
  - The walk is over a DWORD table.
- The registry:
  - It holds 64 slots, ending at `02EBF200` (`00236C30+0x401`).
  - There are five inner binders (`00236C30+0x164`).
  - There are twelve setters.
  - Action rows are 60 bytes.
  - Slot `02EBF138` has 723 references.
  - The `003845F0` / `003846F0` call and jump census is corrected.
- Five `.ard` categories.
- The `word.bin` directory ends at 292.

The pass drafted 92 strike edits (`apply_02resource_a.py`). OPUS applies the 42 on its own lines across ten pages
(`apply_by_owner.py OPUS`). The rest are held or routed:
- 13 on the entry-tree and row-lookup contracts are held until their F-interior sections publish
  (`apply_by_owner.py OPUS-HELD`). When the hold lifts, one line goes to SWE2-EC7 and one to FRONTIER.
- 11 go to SWE2-EC7.
- 8 go to SWE2-FRONTIER: the EFX rebase contract, which is an overlay carrier, and two bigfile rows.
- 7 go to SWE2-STRUCT.
- 6 go to FABLE.
- 3 go to SWE2-CONTRACT.
- 2 go to FRONTIER.

Left without an edit:
- C-V11, C-V121: labels the code does not decide.
- C-V15, C-V118: both sides hold.
- C-V120: the count is right.

- **Affected:** 02-Resource-And-Asset-Pipeline/CONTRACT-resource-section-addressing.md, 02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md, 02-Resource-And-Asset-Pipeline/README.md, 02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/README.md, 02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md, 02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md, 02-Resource-And-Asset-Pipeline/authored-data-table-registry.md, 02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md, 02-Resource-And-Asset-Pipeline/resource-section-addressing.md, 02-Resource-And-Asset-Pipeline/the-resource-request-queue.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the ten OPUS-led 02 pages (OPUS lines) | revised-here |
  | the entry-tree and row-lookup contracts | routed-to-OPUS (held; `apply_by_owner.py OPUS-HELD`, 13 edits) |
  | the external-source page and SWE2-EC7's lines | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 11 edits) |
  | the EFX rebase carrier and two bigfile rows | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py SWE2-FRONTIER`, 8 edits) |
  | the registry's `0x02EBF198` lines | routed-to-SWE2-STRUCT (request with `apply_by_owner.py SWE2-STRUCT`, 7 edits) |
  | the path page and FABLE's lines | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 6 edits) |
  | the resource-owner page | routed-to-SWE2-CONTRACT (request with `apply_by_owner.py SWE2-CONTRACT`, 3 edits) |
  | FRONTIER's two lines | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py FRONTIER`, 2 edits) |
  | RE repo `docs/readiness/02-resource.md` | routed-to-OPUS (filed after part B) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-resource-a-readiness-fixes-1002/resource_a_check.py, verified at 73a856c52: 9 instructions decode as cited, FAILS 0 ([`resource_a_check.out`](resource_a_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (42), FAILS 0.

**Pass-22 neighbours (2026-10-02, OPUS).** `check_publish_neighbours.py` refused the first form of these edits. Some corrections cited another layer's function by address, and that adds an unaccounted crossing. Those functions are now named by role or by their ledger name on the page, with the offset kept. The applier's `ROLE_NAMES` pass makes the same change to its NEW text, so re-runs stay idempotent. The full deciding addresses remain in the applier's comments and in this record. `Tools/work/OPUS/nb_page.py` shows no new hit.
