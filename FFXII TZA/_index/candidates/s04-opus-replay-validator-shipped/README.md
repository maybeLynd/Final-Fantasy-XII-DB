# S-04: the class validator executed over the SHIPPED tables for all 32 classes (OPUS, 2026-09-25, block 328)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-04's section review (N05) ran the validator
`00322C50` stub-free over **synthetic** states and lists *"all authored records"* among what it does not claim. This
harness runs it over the **authored counts**, bound from `battle_pack.bin` by shipped code, at every class's range
edges.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` from block 327. There is no application stub and no
stop boundary.

**Binding.** `battle_pack.bin` (us, sha256 `d1bb89aa…2cbc98`) is copied raw, and `003846F0` relocates the directory.
Then **every binding call `00236C30` makes is made again with the same arguments, read from its own instruction
stream**: 39 in all (the `003845F0` / `003846F0` calls, the inner binders `00238160`, `00238660` and `003847B0`, and
`00237FC0`'s first call).

**Not made:**
- `00238880`: the gambit table, slot `02EBF0D8`;
- the tail of `00237FC0`.

Both allocate from engine heap 6, which halts unbuilt. The codec base stays at 0 (block 324).

**4 / 4 pass, and `result.json` is byte-identical over three runs** (md5 `fcef47565353dc42722173f402e13864`).

| case | contract item | observed |
|---|---|---|
| `bind_every_shipped_slot` | — | 39 binding calls made, the two heap-dependent ones skipped |
| `arms_2_to_32_at_their_edges` | I2, §2 | For every class 2..32 the validator accepts exactly `lo .. lo+count-1` of the table its arm reads. Each class is probed at `lo−1`, `lo`, `hi−1` and `hi`. See the ranges below |
| `class1_redispatch_every_family` | I2 | Class 1 on an id answers what the class named by `00309440` (the id's family code 5..19) answers, **for every family 0..14**. Family 15 has no code (−1), and class 1 refuses it |
| `I2_validator_vs_inventory_count` | I2 | The shipped equipment table has **557 rows** and the inventory family counts **420**. Id `0x11A4` passes the validator (classes 6 and 1) although the inventory registry's range ends before it |

### The validator's ranges

These ranges are the validator's answers over the shipped bindings.

| class | range | class | range |
|---|---|---|---|
| 2 | 0..27 | 17 | C000..C01F |
| 5 | 0..3F | 18 | D000..D07F |
| 6 | 1000..122C | 19 | E000..**EFFE** (constant) |
| 7 | 2000..21FF | 20 | 0..21E |
| 8 | 3000..3050 | 21 | 0..14 |
| 9 | 4000..4017 | 22 | 0..3 (constant) |
| 10 | 5000..5027 | 23 | 0..8 (constant) |
| 13 | 8000..81FF (the sum of four counts) | 24 | 0..4 |
| 14 | 9000..91FF | 25, 32 | 0..168 |
| 15, 30, 31 | A000..A0FF | 26 | 0..1F (bound by `003847B0`) |
| 16 | B000..B07F | 27 | 0..7 |
| | | 28 | 0..1F |
| | | 29 | 0..80 |

**Empty classes:** 3 (`02EBF120`), 4 (`02EBF150`) and 12 (`02EBF0D0`), whose slots no `battle_pack` call binds, and
11 (`02EBF0D8`, the heap-built gambit table).

## What the execution adds

1. **The validator's 32 arms over the authored counts.** Class 19 is `E000..EFFE`, as the contract says. Classes 30
   and 31 share class 15's arm, and class 32 shares class 25's.
2. **I2 ("three validation domains must not be collapsed") is shown on shipped data.** The validator's equipment range
   (557 rows, to `0x122C`) is wider than the inventory registry's (420, to `0x11A3`). Ids `0x11A4..0x122C` are valid ids
   the inventory will not count.
3. **Class 1 is the family code's class** for every family, measured, not only for equipment (block 323).

## I1, I3, I4, I5 and I6 executed (OPUS, 2026-09-26, `i1_i6.py`)

`i1_i6.py` imports `check.py`, whose four cases run first and unchanged (`result.json` keeps md5 `fcef4756…`). **5 / 5
pass, and `i1_i6_result.json` is byte-identical over two runs (md5 `514e0e92…`). No application stub**; memset is
bridged by name. The I3 / I4 calls rewrite the shipped descriptors, and they are put back before I5 / I6.

| case | observed |
|---|---|
| `I1_tag_selects_the_input_lane_class12_reads_neither` | the fill `0031C5D0` on a record whose DWORD+4 and WORD+6 differ. A read hook on `+4..+7` shows the **first lane read**: WORD+6 for classes 1, 5–11, 13–18, 30 and 31; DWORD+4 for 2–4, 19–29 and 32; **class 12 reads neither and returns −2**. All 32 classes match the contract's partition |
| `I3_rebase_stores_u32_sums_zero_keeps_high_half_selects` | the rebase `0030B6A0` over the **fifteen shipped descriptors** at `01EEBCC0`, with the state at `0x1_23450000`. Every non-zero offset gives `u32(low32(offset) + low32(state))`, and the shipped high halves are all zero. **Synthetic:** a high-half-only offset `0x1_00000000` still writes (`0x23450000`), a zero offset keeps its destination (`0xBEEF`), and `0xFFFFFFF0` wraps (`0x2344FFF0`) |
| `I4_rebase_resets_state_through_the_full_pointer_and_repeats` | through the **above-4 GiB** state pointer, the rebase zeros exactly `+0x57C8..+0x59C7` and ANDs `+0x59C8..+0x5A47` with `F8`; the sentinels on either side survive. `+0x40` holds the exclusive prefix sum of `+0x3C` (0, 64, 484, … 2797). A second call recomputes the same pointers and prefixes and resets again |
| `I5_direct_clears_only_18_wrappers_clear_all` | on a `0xCC`-filled record, class 12 through the direct fill returns −2 and **only `+0x18` is cleared**. Both wrappers, on the same refusal, **clear the whole 0x98 record** |
| `I6_wrappers_return_static_aliased_records` | `0035D330` returns `022CA520` both times (class 2, ids 0 then 1), and the second result overwrites the first in place; `0035D380` returns `022CA480` both times (class 16, `B000` then `B001`). The two records are distinct |

## Classes 3, 4, 11, 12 over real data and I6's text pointers (OPUS, 2026-09-26, `c3_4_11_12_text.py`)

**Correction.** The "Not covered" list above this section used to say that I6's text pointers were not covered because
*"the text banks behind `02EBF170` are not bound in this world"*. **That was wrong.** `00236C30` binds `02EBF170`
itself (`00236FD6`: `003846F0(02EBF170, dir+0xF8, 1)`), and block 328 re-makes that call.

`c3_4_11_12_text.py` runs over this world through `i1_i6.py`: block 328's cases and `i1_i6`'s run first, unchanged.
**No application stub. 5 / 5 pass; `c3_4_11_12_text_result.json` is byte-identical over two runs (md5 `801a7ecc…`).**

**Data bound by shipped code:**
- **Classes 3 and 4.** The shipped `rsn_b.ard` is bound by the game's own binder `003EA710`, as block 343 binds it. That
  is what fills `02EBF120` and `02EBF150`.
- **Class 11.** The gambit slot `02EBF0D8` is bound by `00238880`'s **first** call, `003845F0(02EBF0D8, dir entry 0x20)`.
  This is the same treatment block 328 gives `00237FC0`'s first call. The rest of `00238880` allocates from heap 6.

| case | observed |
|---|---|
| `T_I6_text_pointers_resolve_into_the_bound_pack` | for classes 2, 8, 9, 13, 17, 18, 20, 21 and 24–29, the fill's `+0x18` points **inside the relocated battle_pack**, not into the record: resolved storage, not a copy. *Observed:* the storage is shared. Class 25 ids 0 and 1 return the same pointer, and class 8 id `0x3000` and class 20 id 0 point at the same bytes |
| `C3_class3_over_the_shipped_area_table` | 22 rows: the validator accepts exactly 0 .. 0x15 (probed at −1, 0, 0x15, 0x16) |
| `C4_class4_over_the_shipped_area_table` | 6 rows: accepts exactly 0 .. 5 |
| `C11_class11_over_the_bound_gambit_table` | 256 rows: accepts exactly `0x6000 .. 0x60FF` |
| `C12_class12_slot_has_no_writer_in_the_image` | `02EBF0D0` has **one** reference in `.text`, the validator's own read at `00322DFE`, and no copy as data. **Nothing in the image binds it.** The validator refuses `0x7000` and `0x7001` over the image's null, and the fill returns −2 without a lane read |

## Not covered

- a live game.
