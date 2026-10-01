# S-36: the UI request router executed as shipped code — the three refusals, the mailbox and the scheduler (OPUS, 2026-09-25, block 327)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-36 is the one NOT MET row with **no per-invariant
exposure analysis**. Its runtime cell rests on EXP-069 (request feedback) and EXP-091 (commit callees). This harness
runs `CONTRACT-ui-request-router.md`'s own entries in the built world. The next table gives the stop boundaries used
instead of stubs.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` from block 326. These bodies run as shipped:
- the router `00254B50`, with its policy aggregate `002E0FA0`;
- the post `002E1B10`;
- the generic scheduler `00280A00`;
- the request-word setter `00252B40`, with its per-id prelude through the stop registry;
- the widget mount `00244F50`, and the first widget's proc `0027FB70`.

**Two more idle singletons** are planted as zeroed blocks, the same convention as the world's nine:
- the HUD object `[0209BE80]`, which `002904B0` reads inside the aggregate's `00360360`;
- `[01F7FFE0]`, `00198790`'s object, which a stop callback of the prelude flags.

**Stop boundaries** (the run ends there, arguments recorded, nothing substituted):

| boundary | why |
|---|---|
| `001DBA90` | The audio call a prelude stop-callback makes for some requests. The audio registry `01FD36A0` is the sound layer's lazily built object (S-41) |
| `002909F0` | The first widget's first UI-internal call. The UI system's own init `00247AE0` does not build in this world (it stops at `00217150`) |

**No application stub.** The only import reached is `memset`, bridged by name.

**8 / 8 pass, and `result.json` is byte-identical over three runs** (md5 `06dae736ed922c9ecf4ba8e7e29ae5e2`).

| case | contract item | observed |
|---|---|---|
| `Ra_latch_before_policy` | R-a, §4 | With latch `02092734` = 1 the router returns 0 **without entering the aggregate `002E0FA0`** |
| `Rb_policy_bit_table` | R-b, §4 | Every aggregate bit alone, against ids 1, 2, 3, 5, 14, 21 (the ids the 22-entry table at `01E0C2C0` gates) and 7, all with bit 15 set. The router refuses exactly when that bit's table entry holds the **masked** id's bit: **13 refusals in 154**, decided at the router's own branch after `bt r10d, ebx` |
| `Rc_R3_busy_root_refuses_after_dispatch` | R-c, R-3, R-6 | An occupied root `+0xB8` or `+0xC0`: the router passes the request to `00280A00`, which returns 0 **before `00252B40`**. The request word stays 0 |
| `R3_R6_accepted_request` | R-3, R-6, §3 | Request `0x8007`. The scheduler receives the **raw** `0x8007` (bit 15 kept). `00252B40` writes the **masked** id 7 to `02092730` and `020927D8`, and the latch 1, **before** the first mount. The first mount is a `0xD8` widget with proc `0027FB70`, whose create message runs |
| `R6_prelude_audio_split` | R-6 | The word is written for every accepted id. For ids 2, 6, 15 and 17 the prelude's stop callbacks reach the audio layer before any mount. For 7 and 8 the first widget mounts |
| `R1_single_slot_silent_replace` | R-1, §5 | Two posts before a drain both return 1. The slot holds only the second (id 9, parameter `0x22`) |
| `R2_post_policy_narrower` | R-2 | The post refuses **only id 2 under aggregate bit 0**. Id 7 posts under the same aggregate, and bit 1 does not stop id 2 |
| `R1b_blocked_byte_refuses` | §5 | `0215F1A1` non-zero: the post returns 0 and writes nothing |

## What the execution adds

1. **R-a, R-b, R-c, R-1, R-2 and R-3 are executed** over shipped bodies. R-b is checked against the image's own table
   for every aggregate bit.
2. **§3's raw-versus-masked split is measured on both sides.** The scheduler receives the raw dword with bit 15. The
   request word `02092730` / `020927D8` holds the masked id.
3. **Some generic requests touch the sound layer before any widget.** For ids 2, 6, 15 and 17, the prelude (`00254740`
   → stop registry → a stop callback → `002DF370`) reaches audio before the first mount. For 7 and 8 it does not. This
   is an ordering fact the contract's R-6 does not state.

## R-4 and R-5 executed (OPUS, 2026-09-26, `r45.py`)

`r45.py` imports `check.py`, whose eight cases run first and unchanged (`result.json` keeps md5 `06dae736…`). **8 / 8
pass, and `r45_result.json` is byte-identical over two runs (md5 `dfbdc1d9…`). No application stub.**
- **Allowed set.** It grows by the closures of the release `00252D90` and the hard reset `00252DE0`, plus the
  tail-jump targets `00226BA0` (from `0036D830`) and `0028F2A0`.
- **Stops.** Block 327's two stops remain. A third is recorded: `0036C000`, the `jmp $` in `0036BFE0` taken when bit
  `ecx` of `[022D89B8]` is clear. Request 12's mount reaches it in this world.
- **Planted data only:** the mailbox, the request word and latch, the eight slot records at `0215F200`, manager slot 0
  (`02098E10`, `+0x10` / `+0x11`) and the two transition words `020D46A0` / `020D46B8`.

| case | observed |
|---|---|
| `C4_latch_three_readers_three_writers` | from the image: `02092734` is read at `00254B71` (router), `00253FE3` (arbiter) and `003F4FD7` (mirror), and written at `00252B46` (set), `00252DCB` (release) and `00252E05` (hard reset). Exactly three of each |
| `L4_release_and_hard_reset_clear_latch_and_word` | `00252D90` and `00252DE0` each run to completion and leave the latch and the request word at 0 |
| `D0_drain_dispatches_the_pending_request_to_the_router` | pending id 7, parameter `0x22`, word 0, empty slots, manager slot 0 ready: the drain calls `00254B50(7, 0x22, 0)` |
| `DW_request_word_must_be_0_or_5` | word 5 → dispatched; word 3 → not dispatched |
| `DP_no_pending_no_dispatch` | pending byte 0 → not dispatched |
| `DS_slot_guard_is_38_or_3E_bit0` | a live slot with `+0x38` set → not dispatched; `+0x3E = 0x01` → not dispatched; **`+0x3E = 0x80` → dispatched**. The test is `+0x3E` **bit 0** (`002E0C8D`–`002E0C99`: `shl al, 7` / `sar al, 7` / `or +0x38`) |
| `DT_transition_clause_never_blocks_here` | id 7 dispatches with a transition running, and so does id 12. The clause blocks only when a transition runs **and** `0053DD10` returns 0, and **`0053DD10` is `mov eax, 1; ret`** in this build |
| `DM_manager_slot0_not_ready_discards_the_request` | **not in the contract.** When `00267360(0)` reports manager slot 0 as inactive (`+0x10` bit 0 clear) or busy (`+0x11` bit 0, or `+0x10` bit 7), the drain **zeroes all four mailbox cells** (`002E0B94`–`002E0BA3`) and calls no router. The request is discarded, not deferred |

### What R-5's execution corrects (OPUS; routed to FABLE, the contract's author)

1. **The slot guard is `+0x3E` bit 0, not bit 7.**
2. **The device term is constant.** `0053DD10` returns 1, so on this build the transition clause can never hold a
   request.
3. **A fifth guard discards instead of deferring.** Manager slot 0 not ready → the mailbox is zeroed.

## Not covered

- **R-6's second widget** (proc `00280140`) and the root store. Both need the UI init `00247AE0`.
- **R-4's arbiter half:** `00253C70` reaching its latch read at `00253FE3` needs input state this world does not plant.
  That half is census-only here.
- **R-5's "same tick":** the drain's one call site `0031427D` in the world tick's fixed tail is a static fact.
- A live game.
