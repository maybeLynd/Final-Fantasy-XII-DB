# S-13: the actor record pool built and every record initialised, with no scripted callee (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**

**The gap.** S-13's runtime cell rests on two experiments with scripted boundaries:
- **EXP-107** scripted the per-record constructor `00266530`, and planted a fake allocator callback.
- **EXP-112** scripted five of the constructor's callees: `00265FF0`, `00265B60`, `00268380` ×2, `002681E0` and
  `003DBB60` ×4.

The exposure note (block 296) mapped which invariants those substitutions could reach. **This harness removes them all.**

## What was run

`check.py` runs `ActorStorage_AllocateAndInitializeRecords` (`002679F0`) end to end, over block 355's world
(`../s29-opus-replay-inventory-rebase/world.py`, whose real initialisers build it):

- **The allocator callback is the game's own.** `q[mgr+0x88]` is planted with `00267930`, the default the slot
  configuration installs (`0026C8E3 lea r12, [00267930]`, then `0026CAE6 mov [rdi+0x88], r12`; a caller-supplied
  override is taken instead when it is non-zero). `00267930` allocates through the real resource-arena path
  (`0036C1D0` / `0036C750` / `0036A100` / `0036C660` / `0036C140`) from arena 5.
- **Arena 5** is built by the shipped initialiser `00369D30(5, base, 0x400000, 32)`, over a region poisoned `0xA5`.
- **The constructor `00266530` runs for every record with all of its callees real**, including the five that EXP-112
  scripted.
- **Imports.** `memset` and `strncpy` are bridged by name, with library semantics. `strncpy` is reached by the arena
  name-tag `0036C660`, and SECTION-06/07 bridge it the same way. **There is no application stub and no stop boundary.**
- **Planted data.** Manager slot 0 at `02098E10` (the real BSS slot) holds the descriptor pointer, record count 5, flag
  1 and the allocator callback. The descriptor has 8 groups with record counts 1,1,1,0,0,1,0,1, so the records are
  kinds 0, 1, 2, 5 and 7. Record 3 carries a valid kind link (`0x81`); the rest carry `0xFF`. The command table is
  empty.
- **The kind table** `01E0C328` is the image's own (record sizes `0x328` … `0x668`).

**11 / 11 pass, and `result.json` is byte-identical over two runs** (md5 `f11ac85561c1cee9ced590d32cf403f2`).

| case | item | observed |
|---|---|---|
| `AR1_memset_of_the_whole_block_by_the_caller` | AR-1 | `memset(block = 750004C0, 0, 0x17C0)` covers the header and all five records |
| `AR1_every_record_zero_when_its_ctor_runs_except_+3` | AR-1 | at each constructor entry, every byte of its record is zero except `+0x03`, though the arena was poisoned `0xA5` |
| `AR3_+3_set_by_the_carve_and_never_written_by_the_ctor_tree` | AR-3 | `+0x03 & 0x1F` equals the group (= kind) at entry. **No write from the constructor or any callee covers `+0x03`**, and it is unchanged after |
| `AR4_each_record_stores_its_slot_index_and_the_table_indexes_records` | AR-4 | the count at block `+0` is 5; `block + 8 + i·8` holds five distinct record pointers; record `i`'s `+0x00` is `i`; the constructor is called with `idx = i` |
| `POOL_second_region_published_to_mgr_1F0_and_records_follow_the_header` | pool | `mgr + 0x1F0 = block + align16(5·8 + 0x17)`. The records start past both header regions |
| `POOL_region_map_pointers_point_inside_each_record` | pool | `+0xA0` / `+0xA8` / `+0xB8` / `+0xC0` are 0 or point inside their own record, and `+0xA0` is always set |
| `AR5_callees_not_the_ctor_body_write_+24_+60_+88_+89` | AR-5 | all four are written by **`003DB580`** (SINIT), never by `00266530`'s own instructions |
| `AR5_gaps_+84_+8A_+9C_+B0_not_written` | AR-5 | none of the four gap offsets is written by anything in the call tree |
| `AR5_the_call_tree_writes_past_+11C_inside_the_allocation` | AR-5 | every record is written at `+0x120` (the region-map area). `+0x11C` is a lower bound |
| `all_five_formerly_scripted_callees_executed` | — | `00265FF0`, `00265B60`, `00268380`, `002681E0` and `003DBB60` all entered and returned. `00268380` and `002681E0` need a kind-5 or kind-7 record with an `+0xC0` block, and a valid link: both are present |
| `AR2_masked_bytes_keep_poison_bits_in_the_control_…` | AR-2 | a control re-runs the constructor over a copy of record 0 poisoned `0xA5`. The masked bytes keep poison bits: `+0x08` 5 vs 1, `+0x0B` `0x80` vs 0, `+0x13` `0x24` vs 0. **The masks preserve what is there, so on the caller-zeroed memory they preserve nothing** |

## Notes

- **AR-5's amended wording** (FABLE, `77ba37a1e`) names `003DB580` and `003DBCF0` as the writers of
  `+0x24` / `+0x60` / `+0x88` / `+0x89`. Here `003DB580` writes all four. `003DBCF0`'s byte store to `+0x60`
  (`003DBD7E`) is not reached for these five records. That is consistent with AR-5, which says what the callees can
  write, not that both always do.
- **The allocator's third-argument override** (`0026C8FA cmovne r12, r8`) is not exercised. The default is the one
  planted.

## The three residuals (OPUS, 2026-09-26, `residuals.py`)

`residuals.py` re-runs `check.py` in two variants, changing only environment variables. `check.py`'s default run and its
`result.json` (md5 `f11ac855…`) are unchanged. It adds one static read.

**Group → layout class** comes from the image's own table `01E0C328` (byte 0): `0, 1, 1, 2, 2, 3, 3, 3`. The published
run's groups 0, 1, 2, 5 and 7 never reach **class 2**, the region-map arm that groups 3 and 4 take.

**3 / 3 pass; `residuals_result.json` and the three variant results are byte-identical over two runs** (md5 `aa917ce4…`).

| case | observed |
|---|---|
| `R1_all_groups_every_layout_class_carved_class2_pointers_inside` | a descriptor with one record in each of the 8 groups, kinds 0–7 (the link is on record 5, a kind-5 record, so the two link callees still run). All 11 of `check.py`'s cases pass over eight records, and every layout class 0–3 is carved. The class-2 records (groups 3 and 4) get `+0xA0` at `+0x140`, `+0xB8` at `+0x120`, and `+0xC0 = 0` |
| `R2_fcount_0xA_takes_site1_on_every_ctor_call_default_never` | the published descriptor with `w[desc] = 0xA`: all 11 cases pass. The instruction past the `>= 0xA` gate (`002668EC`) runs on **every** constructor call (6: five records and the AR-2 control). With the default `w[desc] = 4` it never runs |
| `R3_the_only_caller_supplies_the_default_allocator` | static. `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` installs `00267930` unless `r8` is non-zero (`0026C8FA cmovne r12, r8`). **Its only caller**, `0032F850`, passes `r8 = lea [rip - 0xC8031]` at `0032F95A`, which is **`00267930` itself**. So the caller-supplied arm resolves to the allocator `check.py` runs |

## Not covered

- ~~descriptors with `w[desc] >= 0xA` (`003DBB60`'s site 1);~~ executed in `residuals.py` R2;
- ~~a caller-supplied allocator;~~ its only caller supplies `00267930`, the allocator run here (R3);
- ~~the region-map arms for kinds 3, 4 and 6;~~ executed in `residuals.py` R1 (layout class 2 was the missing arm);
- a live game.
