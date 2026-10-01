# S-31: the licence check executed as shipped code over the SHIPPED licence, ability and party-slot tables (OPUS, 2026-09-25, block 326)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** EXP-140 (SWE2-ORACLE) executed the licence bodies over
**planted descriptors**, and its own caveat is that it *"claims nothing about which states an initialised game
reaches"*. This harness runs the same bodies over the **shipped tables**, bound from `battle_pack.bin` by shipped
code. It answers from the data the two questions `CONTRACT-license-check.md` §14 leaves open.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` from block 325. There is no application stub and no
stop boundary. The only import reached is `memset`, bridged by name.

**The tables are the shipped ones.** `battle_pack.bin` (us, sha256 `d1bb89aa…2cbc98`) is copied raw. Then:
1. `003846F0(&[0208E680], blob, 0)` relocates the directory. This is the first call of the delivery stub `00238850`.
2. The three slots this path reads are bound by **the same shipped call `00236C30` makes for them**,
   `003845F0(slot, dir[off])`:

| slot | directory entry | call site | table |
|---|---|---|---|
| `02EBF038` | `+0x34` | `00236D67` | licence records, 361 × 24 |
| `02EBF130` | `+0x44` | `00236DAB` | party-slot rows, 40 × 128 |
| `02EBF138` | `+0x3C` | `00237FDE`, the first call of `00237FC0` | ability rows, 543 × 60 |

`00236C30` is not run whole: `00237FC0` and `00238880` go on to allocate from engine heap 6, which halts unbuilt. The
codec base stays at the image's 0 (block 324).

**Fixtures:** the `BattleStatsRecord` (`+4` slot, `+5` kind, the 46-byte owned mask at `+0x194`) and the mask
buffer.

**6 / 6 pass, and `result.json` is byte-identical over three runs** (md5 `b406b55f8badddd8563e8517e630dd33`).

| case | contract item | observed |
|---|---|---|
| `bind_shipped_tables` | §3, §15 | licence records **361 × 24** (node ids 0..360, as `_types` bounds them), ability rows **543 × 60**, party-slot rows **40 × 128** |
| `builder_every_ability_matches_model` | §13's builder | `002F8FA0(1, id)` over **all 543 ability ids** agrees with an independent decode of the raw licence records every time: the mask bits and the returned count. 118 ids are granted by at least one record |
| `I3_escape_bit_census` | I3 | With nothing owned, exactly the **98** rows whose `+0x2C` has bit `0x2000` are licensed (Quickening ids aside). This is the page's 98 of 543, now through the shipped ask |
| `I4_any_single_square` | I4 | For 40 granted ids, owning **any one** of the records that list the id licenses it. Owning an unrelated record does not |
| `I5_quickenings_counted_over_shipped_rows` | I5, §10, §14 | See below |
| `licence_records_0_17` | §14 | Licence records **0..17**, the bits `00324020` counts, are all **kind 19** and **list no id**. No kind-1 mask over the 543 ids sets any of them |

### I5 over the shipped rows

- **Slots 0..5 each name three Quickening ids**, and together they cover `0xD0..0xE1` exactly:

  | slot | ids |
  |---|---|
  | 0 | `D0 D1 D2` |
  | 1 | `DC DD DE` |
  | 2 | `D3 D4 D5` |
  | 3 | `D6 D7 D8` |
  | 4 | `D9 DA DB` |
  | 5 | `DF E0 E1` |

- **Slot 6's row is `00 00 00`.**
- The *k*-th id of a slot's row is licensed once *k + 1* of bits 0..17 are owned. This holds for every slot 0..5 and
  every count 0..3.
- **The signed `setl` edge is concrete on shipped data.** An id from another slot's row is absent from this slot's row:
  `0030A330` returns 3. It is refused with 3 counted bits and **licensed with 4**, for **every** slot, slot 6 included.

## What the execution adds

1. **§14's first question has a data answer.** It asks whether bits 0–17 are exclusively the Quickening squares.
   - In the shipped licence table, records 0..17 are a block of 18 kind-19 records with no ids.
   - The mask builder never sets them for any ability, so they have no role except `00324020`'s count.
   - 18 records match the 18 Quickening ids that slots 0..5 name.

   The label "Quickening squares" remains the contract's; what is measured is that nothing else reads those bits.
2. **The over-permission edge is a cross-character edge in the shipped data.** With 4 or more of bits 0..17 owned, a
   character is licensed for the Quickenings of other slots' rows, because they are absent from its own row. Slot 6
   has no row entries and is licensed for all 18 at 4 bits.

   Whether an initialised game lets one record own 4 of those bits depends on the board-purchase rules, which are not
   in these tables. It stays open, and the question is now sharper.
3. **I3's 98 and the builder's census are now shipped-state facts**, not planted-descriptor results.

## Not covered

- whether 4 of bits 0..17 are reachable (the licence board grid and purchase rules);
- the gambit and ability-lookup allocations of `00238880` / `00237FC0` (heap 6);
- a live game.

## I1 and I2 executed (OPUS, 2026-09-26)

`i1i2.py` runs over this harness (imported unchanged; its cases run first). It calls the ask `00323EC0(rec, actionId)` over
the shipped tables. A read hook over the licence records and the record's owned mask (`+0x194`, 46 bytes) counts every
board access.

| case | result (value, board reads) |
|---|---|
| I1 exit 1, invalid id `0xFFFF` | (0, 0); and with a null record too, (0, 0): the id test comes first |
| I1 exit 2, null record | (1, 0) |
| I1 exit 3, kind 1 | (1, 0) |
| I1 exit 4, slot 7 and slot `0xFF` (unsigned) | (1, 0) each |
| control, kind 0 slot 6, same ability | (0, 1176): past the exits, the board is read and the ability refused |
| I2 | over all 543 shipped abilities, kind 1 and slot 7 are licensed for every one. 445 are unlicensed on an empty kind-0 board |

**Runs.** 6/6, and two runs give an identical `i1i2_result.json` (md5 `9dd2886caa352c2a7f0bb9953759dccf`).
