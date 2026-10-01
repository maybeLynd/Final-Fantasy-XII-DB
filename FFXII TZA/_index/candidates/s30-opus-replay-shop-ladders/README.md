# S-30: the shop stock ladders executed as shipped code over the shipped table (OPUS, 2026-09-25, block 324)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-30's exposure note (block 301) found the whole of
`CONTRACT-shop-stock-ladders.md` (SG-1..SG-7) **unexecuted**, and its §13 says "None". The bazaar half of the row is
EXP-092's. This harness runs the ladders **over the shipped shop table, bound by shipped code**.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` from block 323. There is no application stub and no
stop boundary. The only import reached is `memset`, bridged by name.

**The tables are the shipped ones.** `battle_pack.bin` (us, sha256 `d1bb89aa…2cbc98`, `Tools/work/repos-2d/vbf/…`) is
copied raw to `0x76100000`. Then the delivery path's own steps run:

1. `003846F0(&[0208E680], blob, 0)`, the first call of the delivery stub `00238850`: the directory's 71 offsets
   become pointers.
2. The two inner binders `00236C30` calls for these tables:
   - `00238160` on `+0x38`, the equipment rows → `[02EBF0F8]`. The listing's category test reads them.
   - `00238660` on `+0xA0`, the shop table → `[02EBF158]`.

`00236C30` is not run whole: its gambit binder `00238880` allocates from engine heap 6, whose allocator halts unbuilt
(measured here; see block 321).

**The codec base `[01F83530]` stays at the image's 0.** The delivery path is self-consistent only with 0:
- `00238850` stores the **encoded** blob address in `[0208E680]`;
- `00236C30` dereferences that cell as a raw pointer.

With a base of 0, resolve is the identity.

**Fixtures** (planted data only):
- the story operand: the u16 array behind `[02098E58]`, which `00264640` reads for query class 3, enabled by
  `[02098E20]` bit 0;
- the clan-rank block behind `[020927C0]`, zeroed;
- the object behind `[02092758]`, into whose `+0x0C` the rank path writes (`00316930` → `00254E80`);
- synthetic ladders for SG-4, SG-5, SG-7 and SG-3. SG-5b patches shipped row 0's section field for one listing, then
  restores it.

**10 / 10 pass, and `result.json` is byte-identical over three runs** (md5 `33d18201487fa2d0ab6099b4c7ee4618`).

| case | contract item | observed |
|---|---|---|
| `bind_shipped_table` | §3, the page's corpus | The shipped binders produce header `{0x64, 8, 57}`. Row 3 opens with story ≥ 200 (Longsword `0x1002`, Cypress Pole `0x1037`) and ends in Mace `0x108B`. Row 0's base entry is Eye Drops, Potion, Onion Bolts. **267 entries and 2,512 ids**, the page's census |
| `SG2_every_row_gate_matches_model` | SG-2 | **All 57 shipped rows at story 0, 200 and 6000** (clan rank as computed: 1). The gate returns the first passing entry, else the **last** entry through the exhausted loop. The entry and the exit index (`esi` at `002FAE28`) match an independent walk every time |
| `SG1_one_gate_then_pointer_walk` | SG-1 | Each listing call enters `002FAD40` **once**. Across all categories it returns exactly the ids of the chosen entry and every entry after it (rows 0, 3, 24, 43; row 24 starts at its 15th line) |
| `SG6_rank_floor_row2_not_all_gated` | SG-6, §14 | With zero inputs the rank is **1**: rung 1 of `00D105D0` is `{0, 0, 0}` and the fallback is also 1. **Row 2's last line is kind 3 at 1, and it passes on its own gate** (exit index 11 of 12) |
| `S10_negative_operand_fails_threshold_0` | §10 | Row 17 ends in kind 2 at 0. Story 0 passes it on its own gate. **Story `0x8000` is sign-extended** (`003211EC movsx`) to −32768 and falls through. The same entry is returned either way |
| `SG4_kind1_kind2_one_argument` | SG-4 | With element 0 = 100, element 5 = 900 and threshold 500: kind 1 queries `(3, 0, 5)` and passes. Kind 2 with the same operand byte queries `(3, 0, 0)` and fails to the next line |
| `SG5_unknown_kind_skipped` | SG-5 | Ladder `[story ≥ 50, kind 4, kind 0]`: below 50 the gate skips the kind-4 line and stops at the kind-0 line. At 50 or more it stops at line 0 |
| `SG5b_unknown_kind_listed_when_above` | SG-5, §12 | Through the listing: below the gate only the kind-0 line is offered. **Above it the kind-4 line's ids are offered** |
| `SG7_bound_not_snapshotted` | SG-7 | Three failing lines. Cutting the count to 1 after the first pass makes the gate exit with line 0, not line 2: the count at `+6` is re-read every pass |
| `SG2b_SG3_null_section_and_null_data` | SG-2, SG-3 | A section field of 0 gives count 0 and returns NULL. A section with entries and a data field of 0 takes `002FADC3` and **faults reading address 0**. No shipped section has entries and a null data field |

## What the execution adds

1. **SG-1 through SG-7 are executed**, and SG-2 is executed over every shipped row.
2. **§14's "12 truly all-gated rows" is 11.** Measured at story 0 and rank 1, the rows that fall through are 21, 22,
   26, 27, 43, 44, 48, 49, 51, 54 and 55.
   - **Row 2 is not among them.** `00315390` never returns below 1: rung 1 is `{0 points, 0, 0}`, and the fallback
     at `003153E1` is also 1.
   - So row 2's rank-1 line is an always-pass tail, like rows 17 / 18's `k2@0`.
   - The same count appears on the shop-table page (§2 footnote) and in §15's row. Routed to FABLE.
3. **§12's SG-5 step needs a condition.** *"Author a gate kind of 4 and assert exactly that entry vanishes"* holds
   only when the gate stops **below** the unknown line. When an earlier line passes, the listing's pointer walk
   copies every later line, the unknown one included. The gate skips the line; the listing does not. Routed to
   FABLE.
4. **§10's negative-operand edge is real, and it reaches threshold 0.** The operand is sign-extended from 16 bits, so
   a story word of `0x8000` or more fails even `k2@0`. The shipped maximum story value is far below that (5,350 is
   the table's highest gate).
5. **The delivery model.** The shop table and equipment rows bind by shipped code from the raw file, with the codec
   base at 0, which the path requires. The whole `00236C30` cannot run without engine heap 6 (`00238880`).
6. **SG-3 is reachable only through an authored zero.** With the base at 0, a section whose data field is 0 faults. No
   shipped section is like that.

## Not covered

- clan ranks above 1: they need the menuhandbook blob behind `[022C2550]` for `00316480`'s count;
- the save-header consumer of the rank (SG-6's third caller);
- the bazaar mode of the listing: EXP-092, not re-run;
- a live game.
