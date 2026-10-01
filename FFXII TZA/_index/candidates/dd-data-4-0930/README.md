# DD owner read, batch 4: six Presentation, World, Platform and CRT pages (SWE2-DATA, 2026-09-30)

affected: 17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md, 17-Presentation-Rendering/Model-And-Motion-Formats/frp-object-container.md, 17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md, 03-World-Area-Field/choosing-the-field-environment-variant.md, 20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md, 24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md, _index/OPEN-QUESTIONS.md (new rows SD-140, SD-141, SD-160..SD-169)

run: at f55dd3c9a: fx54_consumers.py, frp_checks.py, rrp_checks.py, pf_env_checks.py, pf_steam_checks.py and
pf_mem_checks.py, each FAILS 0 (the .out files beside them). They are static reads of the shipping image through
`../rc22-34-resource-readers-0930/pe.py`, plus archive censuses under `D:/FFXII_TZA_extract`. `rrp_checks.py` also reads
the installed `keymap.ini`.

Task `SWE2-DATA-DD-OWNER-READ-4-0930` (target key only). These are the last six clean, unowned rows of
[`dd-owner-read-0929/worksheet.tsv`](../dd-owner-read-0929/worksheet.tsv). The method is the one used for
[`dd-data-0930`](../dd-data-0930/README.md) and batches 2 and 3. No status word was raised.

| page | what changed | residue |
|---|---|---|
| effect mesh records kind 0x54 | both vertex-prep consumers read (new §8). Blended `+0x24` vectors are renormalised (`00432030` calls `sqrtf`), which backs the normals label; the `+0x28` / `+0x2C` labels stay unproven. The two "no consumer read" lines are struck and corrected | SD-140 |
| frp object container | "parts not established" lines corrected to the sibling entry sheets. `NameEquals` (`00408F30`) compares 32 bytes and returns 1 on a mismatch; no caller passes a name (thunk `00408F90`, four callers, NULL name, tag `@FRM`). Padding claim corrected from a census (`.cm` files also pad to 1 and 2 KiB) | none |
| reflected render parameters | W-7 SUPERSEDED on the status line. Stale W-2/W-3/W-5/W-9 prose struck; "the 50" corrected to 44 (27 + 7 + 10); the `keymap.ini` counts anchored; the "airborne viewpoints" guess struck | SD-141 |
| choosing the field environment variant | open items reconciled against the weather contract and GB-1 (NO ADMISSIBLE SOURCE), GB-3, AW-4. It publishes four globals, not five; the debug override of the requested slot is added; two unanchored claims are struck. Sections added | none |
| Steam integration and achievement catalogue | AB-6, AB-8 and UQ-272 SUPERSEDED on the status line; §3, §5, §8, §8b and the AB-4 prose reconciled. The Trial Mode release claim is struck. `00315820` is read (it counts bestiary defeats), and so is the id-18 compare path | SD-160..SD-163 |
| where the game's memory comes from (status stays REOPENED) | `_set_new_mode` is called once, as `(0)`, by the first C++ initializer `00808D5C`; "never called" corrected in §2, the import table and the evidence row. Struck: the "exactly the failure in §1" line and the "no free list, no pool, no bookkeeping" line. Reconciled: the reclaim is the SECTION-07 compaction, and `+0x0C`/`+0x10` are physical-neighbour links. The `_Xbad_alloc` figures and the `00244200` width are anchored | SD-164..SD-169 |

## Consumer check

| consumer | disposition |
|---|---|
| the six pages above | revised-here |
| `03-World-Area-Field/CONTRACT-weather` §14 item 3 ("Sibling `02099DA8` has the same shape: one store, `0026DA26`, same body") | routed-to-SWE2-CONTRACT: false; the getter `00263E10` loads `02099DA8`, as that contract's own §5 census shows (`pf_env_checks.py` E8) |
| other pages on `_set_new_mode` (grep: none states "never called") | agrees |
| OPEN-QUESTIONS W-2, W-3, W-5, W-7, W-9, GB-1, GB-3, AW-4, AB-4, AB-6, AB-8, UQ-272 | agrees (the pages now follow them) |

## Rule before and after (`documented_rule.py`)

Before: READY 4, NEEDS-POINTER 2. After: see the batch report. The pages that gained SD rows are PARTIAL on them, and the
environment-variant page is READY-WITH-POINTER.
