# RC-25 closed: the party records' definition rows and the silhouette blocks they show (ORACLE, 2026-09-30)

## The question

RC-25 asks which of `char_silhouette.as7`'s 3,096 pages any shipped path indexes. ORACLE's
`../rc22-as7-pages-0930/` narrowed it:
- the silhouette id is the menu member record's word `+0x60`;
- that word is `BattleStatsRecord.definitionRowIndex` (`+0x04`) of the stats record behind the member;
- ids 0 to 5 select the six 516-page blocks, and every other id shows nothing.

The residue: which `definitionRowIndex` values the party stats records carry.

## Method

[`rc25_rows.py`](rc25_rows.py), output [`rc25_rows.out`](rc25_rows.out). Every link is asserted from the shipping
image, and one link comes from the published access census. All checks pass.

| link | fact | evidence |
|---|---|---|
| L1 | `BattleStats_InitializeDefinitionRecord` `0023AC80(rec, id)` clears the record and stores the whole id word at `+4`. Row = low byte, table = high byte; table 0 is the party table `02EBF130`. | `0023AC9E`, `0023ACAA`, `0023AD41`, `0023AD8E` |
| L2 | It has three call sites. Two are loops `k = 0..0x27` over `rec = [02EBF190] + 8 + k*0x1C8` with `id = k`: `00237E26` in `00237DF0` and `00239AC4` in `00239960`. The loop's `cmp k, 0xFF` / `cmovne` never picks `0xFFFF` below `0x28`. The third site, `0023A7A9` in `0023A570`, initialises a SpawnRecord's embedded record. | loop bounds `00237E2D`, `00239ACB` |
| L3 | The published access census (`08-Combat-Formula/Battle-Stats-Record/battle-stats-record-accesses.tsv`) has exactly one write that can cover `+0x04`: `0023AD8E`. | re-read by the script |
| L4 | The member word `+0x60` starts at -1 (`0032925D`). It is then set to `byte [stats + 4]` (`0032946C`/`00329471`) of the record that `00320040` resolves through party slot map 3; rows above `0x27` resolve to no record (`00320058`). | image |
| L5 | `002CEE00` drops ids above 5 (unsigned). The block shown is `T[id]` with `T = {0, 1, 3, 2, 4, 5}`. | image |

## Result

**RC-25: ANSWERED.**
- **Every party stats record carries its own row index.** Record `k` has `definitionRowIndex = k` (table 0),
  `k = 0..39`, and ~~nothing else in the image writes `+0x04`~~ *(narrowed 2026-09-30, SWE2-ORACLE, per `SWE2CONTRACT-CONTRA-ORACLE-RC30-RC25-0930` and SWE2-AUDIT-SEM's N3: that initialiser is the only writer through `02EBF190`. `002EF4A0`, called only from `00235AF0`, overwrites all 40 pages from the mirror `02166480`, whose writers are `00229B76`, `00866A4D` and `00583C00`; the last is an untraced external buffer. So `+0x04 = k` holds provided the mirror carries pages written by the same initialiser)*.
- **The member id is that row.** A menu member's id is therefore its party record's row. Using the published row
  names of the `battle_pack.bin` `+0x44` party table (`battle-record-kind-byte.md` AL-2):

| record / row | character | silhouette |
|---|---|---|
| 0 | Vaan | block 0, pages 0-515 |
| 1 | Ashe | block 1, pages 516-1031 |
| 2 | Fran | block 3, pages 1548-2063 |
| 3 | Balthier | block 2, pages 1032-1547 |
| 4 | Basch | block 4, pages 2064-2579 |
| 5 | Penelo | block 5, pages 2580-3095 |
| 6-16 | guests | none |
| 17-25 | "No name" rows | none |
| 26 | Chocobo | none |
| 27-39 | Espers | none |

- **The menu's own rule matches.** It counts a member as a main character when the id is 0 to 5 and the member is not
  flagged a guest.
- **So each of the six main characters selects a different block, and together they index all 3,096 pages.** A
  session shows a character's 516 pages whenever that character is a menu member.
- **Guests and every other row get no silhouette.**

**Consequence for RC-30 (site `002CEAE0`).** That site requests `0x10 + d`, where `d` is a guest member's id. The id
is a party row, 0 to `0x27`, so the requested id is `0x10`-`0x37`. It cannot be a `loca_*.cl2` id (`0xE2`-`0xE4`).
When no guest is present the byte is 0xFF, but the gate bit is then clear and nothing is requested. See
`../rc30-cl2-request-bounds-0930/`.

## Not claimed

- **Values from a loaded save.** The party block is restored from the save; its `+0x04` words were written by these
  same initialisers, and nothing else writes them. A hand-edited save could carry other values.
- The census's own recall statement is inherited. This record's direct byte-store scan of the functions that hold
  `02EBF190` and use the 0x1C8 stride also found no other writer.
