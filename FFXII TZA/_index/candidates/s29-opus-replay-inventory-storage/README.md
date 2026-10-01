# S-29: the inventory class storage's §4 executed over the shipped binding, with no stub (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**

**The gap.** S-29's runtime cell reads: *"`CONTRACT-inventory-class-storage`'s mutate cap/handler-ratio invariants rest on
EXP-064's stubbed path"*. EXP-064 stubs the ±1 entry `003008A0` itself.

**What this harness runs.**
- The ±1 entry `003008A0`, the query entry `00309F30`, and all four storage handlers the descriptors dispatch to: the
  mutators `002FD150` (packed) and `002FD420` (bitset) through `+0x48`, and the queries `002FD8D0` / `002FD970` through
  `+0x50`.
- The storage those handlers use is bound by the **shipped** rebase `0030B6A0`, exactly as the game binds it.

## What was run

`check.py` uses block 355's `world.py` (in `../s29-opus-replay-inventory-rebase/`, imported from there). Its real
initialisers build the world, and the descriptor table `01EEBCC0` is the image's own `.data`.

**No application stub and no stop boundary.** The allowed set grows by the static closures of `003008A0`, `00309F30` and
`0030B6A0`, plus the four handlers and their closures. The handlers are reached through the descriptor's pointers, so the
static graph does not have them.

**Order.**
1. P3 runs first, in the unbound image state.
2. A zeroed `0x7410` block is bound by `0030B6A0`.
3. Everything else runs over that binding. Values are planted into the bound arrays only where a case needs a starting
   count.
- **One disclosed perturbation, the control for I:** class 3's `+0x48` / `+0x50` are swapped to the packed pair for one
  call, then restored.

**16 / 16 pass, and `result.json` is byte-identical over two runs** (md5 `8e348e44493244bf2fd33b76c6e385f5`).

| case | §4 item | observed |
|---|---|---|
| `P3_image_pointers_null_for_all_15_classes` | P3 | `+0x08`, `+0x20` and `+0x30` are 0 in all fifteen rows of the built world |
| `P3_every_query_and_mutate_returns_without_fault_while_unbound` | P3 | 104 calls in total. For the eight storage classes: `00309F30` × kinds 0–4, and `003008A0` × channels 0–3 × modes add/absolute. **All return, with no fault** |
| `P3_no_store_outside_the_image_while_unbound` | P3 | no store lands in unmapped or low memory: every handler null-tests |
| `bind_by_shipped_rebase_returns` | — | `0030B6A0` binds `+0x08` for every storage class |
| `P1_nibble_15_rejected_by_both_entries` | P1 | `0xF000`, `0xF001` and `0xF1FF` → `-1` from both entries; `0xFFFF` → `-1` |
| `P1_nibble_12_accepted` | P1 | `0xC000` is accepted |
| `X_mutate_entry_refuses_0x1000_query_entry_reads_it` | **not in §4** | `003008A0(0x1000)` → `-1`, with no store and the word still 5. `00309F30(0x1000, kind 1)` → **5**. `003008A0(0x1001)` → 1. The ±1 entry refuses `0x1000` (`003008D8`–`003008E0`) and the query entry does not. Added to the contract's §2 |
| `P2_last_id_accepted_first_past_rejected_no_store` | P2 | for all eight storage classes, the id `count − 1` is accepted. The id `count` gets `-1` from the ±1 entry and 0 from the query entry, **with no store** |
| `P2_count_0_classes_reject_every_id` | P2 | classes 5, 7 and 11 (count 0) refuse index 0: the signed compare against `count − 1 = −1` |
| `Q_every_mutate_returns` | Q | 168 mutates on packed classes 0, 1 and 2 (channels 0–3 × add/absolute × deltas 100, 200, 98+1, 99+1, 50+49, 1023, 0x7FFF) all return |
| `Q_stored_owned_and_reserved_and_byte_at_most_99` | **Q** | across 126 word stores and 14 byte stores, owned, reserved and the count byte are all ≤ 99 |
| `Q_the_cap_is_reached` | Q | owned reaches 99 (for example 0 + 100 → 99, and absolute 1023 → 99), and so does the byte |
| `I_every_storage_class_first_and_last_id_write_inside_own_region` | **I** | for every storage class, the first and the last id write only inside the region the descriptor's own counts allocate: `+0x08` × 2·`+0x10`, `+0x20`, and `+0x30`, where class 0's bit per id is `+0x57C0`..`+0x57C7` |
| `I_last_id_writes_the_last_element` | **I** | the last id writes element `+0x10 − 1`: packed index `count − 1`; bitset `(count − 1) >> 4`, which is 5, 1, 15, 31 and 1 for classes 3, 4, 6, 8 and 12. The handler's packing and the `+0x10 : +0x3C` ratio agree for all eight |
| `control_mismatched_handler_writes_outside_its_region_unchecked` | I, "nothing enforces" | with class 3 given the packed handlers, id 80 writes `+0x4FB0`: outside class 3's `+0x4F10`..`+0x4F1C`, past every class's region. **The call succeeds (returns 1)** |
| `control_restored` | — | class 3's handlers are back |

## What the channels store (observation, `result.json` → `detail.Q`)

These are channels of `003008A0`'s fourth argument, not query kinds.

| channel | add | absolute |
|---|---|---|
| **1 (owned)** | owned + delta, clamped to [reserved, 99] | `min(value, 99)` |
| **3 (the count byte)** | class 2: byte + delta, clamped to 99. Classes 0 and 1: **no store** (their `+0x20` stays NULL after binding, and the handler null-tests it) | class 2: `min(value, 99)`; classes 0 and 1: no store |
| **2 (reserved)** | from reserved 0: reserved becomes the delta, **bounded by owned** (owned 0: 100 → 0; owned 98: 1 → 1; owned 50: 49 → 49). Every start had reserved 0, so add and set are **not distinguished** here | the same results as add, for these starts |
| **0 (available)** | returns owned, no change | reserved := owned − value, **truncated to six bits**: owned 98, value 1 → reserved 33, available 65 |

*The channel-0 absolute truncation follows from §7's six-bit reserved field. It is recorded, not claimed as a §4 item.*

## Not covered

- the clear-all `003047F0`;
- the non-storage classes' writers `002FD530`, `002FD640`, `002FD780` and `002FD880` (classes 9, 10, 13 and 14);
- the discovery-state update and the range checks in `003008A0` past the handler call;
- a live game.
