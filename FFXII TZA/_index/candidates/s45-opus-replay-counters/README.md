# S-45: the achievement counters' unexecuted items, over the real image-backed block (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**

**The gap.** S-45's runtime cell rests on EXP-089. That record plants the save image and the Steam manager. The exposure note
([`../s45-runtime-per-invariant-exposure.md`](../s45-runtime-per-invariant-exposure.md)) lists what EXP-089 does not drive:
- the read's and the store's id bound;
- kind 4's saturation, since no update case uses a kind-4 id.

## What was run

`check.py` runs over block 332's world (`../s21-opus-replay-applier-stub-free/check.py`, whose cases run first;
`result.json` keeps md5 `baf273ee…`). **No application stub, and the cases reach no import.**
- **The image-backed block is bound by its own binder,** not planted. `00253970`'s prefix runs up to `00253997`:
  `00249840`, then `002EF640() + 0x8200`, stored at `00253990` into `[020927C0]` (`0216C480`), as in
  `item38.py`.
  - The counters sit at `block + 0x384C + descriptor +1`, and the award bitmap at `block + 0x3844`.
- **The Steam manager cell `[01F83450]` is left as the image leaves it.** ~~Its one writer~~ Its one non-null writer, `0020CD30`, does not run. *(Corrected 2026-09-29, OPUS, `CON-177`: the destructor
`0020CD80` also writes it, with 0.)* That is
  the state the Steam contract's I-1 describes after a failed Init.
- **`003165C0` returns 0 for every id in this world**, because its inputs are runtime tables left at zero. So mode 0's
  threshold falls back to the descriptor's `+4`, which is also 0, and any counter completes. K6 relies on that; no case
  claims a real threshold.

**8 / 8 pass; `result.json` is byte-identical over two runs (md5 `a383fe13…`).**

| case | contract item | observed |
|---|---|---|
| `K1_kind4_saturates_on_every_kind4_id` | the no-wrap invariant, kind 4 | ids 6, 7, 11 and 17 (every shipped kind-4 id): stored `0x7FFFFFF0`, then `+0x100`, gives **`0x7FFFFFFF`**. Below the limit the add is exact (100 + 5 → 105) |
| `K2_kind2_saturates_and_leaves_the_neighbour` | the no-wrap invariant, kind 2 | id 0: `0x7FF0 + 0x100` → **`0x7FFF`**. Id 1's word beside it keeps `0x1234` |
| `K3_store_writes_kind_bytes_at_block_plus_384C_plus_offset` | §3, the store `00316BF0` | id 0 writes **2 bytes at `+0x384C`** (`00316C45`); id 6 writes **4 bytes at `+0x3860`** (`00316C30`) |
| `K4_ids_30_31_255_rejected_by_read_store_and_update` | the id bound, in the read and the store | for ids 30, 31 and 255 the read returns **`-1`**, the store writes nothing, and the update enters neither evaluate nor store and writes nothing |
| `K5_update_evaluates_before_it_stores` | the §2 order box | the update calls evaluate, then the store |
| `K6_award_bit_set_then_null_manager_returns_no_steam_call` | the award tail; Steam I-1's consequence | a completed id 1 sets **bit 1 of the award bitmap** (`00316069`). `008632B0` then reads the null manager through `0020CE00` and returns. No send, and no Steam import is reached. **The award is recorded in the save even though Steam is never told** |
| `B_manager_builder_registers_1101_1102_1103_then_needs_the_steam_interface` | boundary record | `0020CD30` → `0020C730` registers callbacks **1101, 1102 and 1103** through `SteamAPI_RegisterCallback` (bridged by name for this case only, recording the id). It then calls `SteamInternal_ContextInit`, the Steam library's interface object, which is not bridged. So the manager is not built |
| `world_bound_by_the_shipped_binder` | — | `[020927C0]` = `0216C480` = `02164280 + 0x8200` |

## Not covered

- **The Steam side with a built manager**: I-2's send, I-3's already-achieved entry, I-4's receipt handlers. They need the
  Steam library's interface objects (`SteamInternal_ContextInit` and the vtable at `+0x38` / `+0x50`), which EXP-089 models
  and this world does not.
- **I-5 and I-6** (the pump census and `RestartAppIfNecessary` → `exit(1)`): static.
- **The unclamped fall-through for another kind**: no shipped descriptor has one.
- **A real threshold** (`003165C0`'s inputs), and with it the "awarded one update late" consequence of K5's order.
- A live game.
