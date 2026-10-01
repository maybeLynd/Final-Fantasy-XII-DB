# S-15: the field runtime pass executed over real actor records, with no scripted callee (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**

**The gap.** S-15's runtime cell rests on EXP-106, which scripted about fifty of the pass's callees: the interpreter,
audio, the deferred request, the init core's external chain, the lifecycle helpers, the slot-0 post-chain, and the wait
predicates and arm checkers. Block 299's exposure note found that none of them reaches an S-15 invariant. This harness
runs the pass with **no application stub**.

## What was run

`check.py` runs `0025D9E0` with its whole static closure allowed. Its world is the S-13 stub-free closer
(`../s13-opus-replay-record-pool-stub-free/check.py`), executed first with its eleven cases unchanged and its md5
`f11ac855…` reproduced. Manager slot 0 therefore holds **five real records**, built by `002679F0` / `00266530` with every
callee real.

**Fixtures (planted data, disclosed):**
- slot 0's record-table pointer `+0x08` = the pool block (its caller `0026CE60` keeps it there), and the slot flag bytes
  per case;
- **slot 1 is a copy of slot 0's block**, with the same records. The drive loop is reached directly for any slot but 0
  (`0025DAC7 test r14d, r14d` / `jne 0025DB22`); for slot 0 it is gated on the global predicate `00377DB0`;
- the party-focus cell `022C7FE0`, which `003590D0` reads, set per case;
- **one disclosed perturbation, for the I1/I2 control only:** record 0's `+0x14` low nibble is set, which the shipped
  image never does.

**8 / 8 pass, and `result.json` is byte-identical over two runs** (md5 `6e31aaeb9c4a3a26c4965a86008de580`).

| case | contract item | observed |
|---|---|---|
| `P_fold_every_actor_driven_counters_up_publish_current` | postconditions | slot 0 with `+0x10 = 0x01`: the wait resolver `0025DF00` drives **each of the five records once** (59 functions entered). `+0x24` and `+0x38` are 1. `02099D70` = slot 0. `+0x11` bit 0 = `+0x10` bit 7 (0) |
| `P_drive_counters_up_publish_current_bit0_equals_bit7` | postconditions | slot 1 with `+0x10 = 0x81`: the counters go to 1, `02099D70` = slot 1, and `+0x11` bit 0 = `+0x10` bit 7 = 1 |
| `I1_drive_loop_runs_once_repeat_zero_times_exit_B` | I1 | with `+0x12` = 1 or 3 and the shipped nibble clear: **one drive, no repeat**, exit B (no `+0x12` publish, no init core `002620E0`) |
| `I2_control_nibble_set_repeats_without_bound_until_the_replay_budget` | I1 (control), I2 | with the nibble set: `0025DB51 test cl, 0xF` → `003DB280` → drive again, **7,500 times**. The loop is still running when the replay's 3,000,000-instruction budget stops it. The nibble stays `1`, bit 6 is never set, and nothing in the loop bounds it |
| `I3_no_focus_and_unresolved_handle_both_publish_null_indistinguishably` | I3 | focus 0 (no party focus), and handle `0x200000` (slot 0, ordinal 0, generation 2 against the record's 1): **both publish `02099D78 = 0`, with identical slot state** |
| `I3_control_valid_handle_publishes_the_record` | I3 (control) | handle `0x100000` (generation 1) publishes record 0 (`75000520`) |
| `I4_success_reported_with_no_actor_driven` | I4 | four early arms each **return 1 with no actor driven** and the counters untouched: `+0x17` bit 4 (through `0025E400`), `+0x11` bit 2, `+0x10` bit 0 clear, and slot 0 on the `≥ 0x80` path with `00377DB0` false |
| `no_fence_no_fault` | — | every run returns, except the control, which is deliberately budget-stopped |

**EXP-106's scripted callees that ran real here:** `001ED180`, `0025B250`, `0025B600`, `0025B740`, `0025B820`,
`0025C170`, `0025E400`, `002681E0`, `002E5030` and `002E5750`.

## The other arms: the `+0x12 == 0` branch and the slot-0 deferred request (OPUS, 2026-09-26, `arms.py`)

`arms.py` runs `check.py`'s world and cases from its own source. Its `result.json` is not rewritten (md5 `6e31aaeb…` is
unchanged).

**4 / 4 pass; `arms_result.json` is byte-identical over two runs (md5 `8a0a93f9…`).**

| case | observed |
|---|---|
| `T1_two_init_core_call_sites_one_audio_site` | static. The pass calls `002620E0` at **two** sites: `0025DB7D` (exit A, after the `+0x12` publish at `0025DB79`) and **`0025DC27`**. The second is on the branch `0025DB25 cmp byte [rbx+0x12], dil` / `0025DB29 je 0025DB87`, that is `+0x12 == 0`. `00261F90` has one call site, `0025DB8E` |
| `F1_plus12_zero_audio_then_init_core_from_0025DC27_no_drive_loop` | slot 1 with `+0x10 = 0x81` and `+0x12 = 0`: **`00261F90` runs as shipped, then the init core**, returning to `0025DC2C`. The resolver then drives all five records, the counters go to 1, and the pass returns |
| `F2_control_plus12_one_no_audio_no_init_core` | control, `+0x12 = 1`: neither `00261F90` nor the init core runs, and one record is driven |
| `F3_deferred_arm_entered_1_D4_boundary_resource_pipeline` | slot 0, with the ready word `[02ADD0D8]` planted to 1 (its writers are the map binder `003775D0`, `00377CC0` and `00378230`). `WorldSimulation_ProcessDeferredModeRequest` `0032FC30` is entered with **`(1, 0xD4)`**. After the resource-path lookup `002DF960` (reached through a tail jump and admitted) and the main-thread check (`00368ED0`'s own store of `GetCurrentThread()`, run as its prefix; the import is bridged by name to `-2`), the area-resource loop `003E9780` is entered and **does not return** within the budget. `+0x10` bit 3 (`0025DAF2`, after the call) is not set. **Recorded boundary: the resource pipeline** |

**A correction to my contract follows from T1 and F1.** §6 said the init core runs *"only when the driven actor came
back settled"* and that *"every pass takes exactly one of exit A or exit B"*. Both hold only inside the drive loop, and a
`+0x12 == 0` pass reaches the init core from `0025DC27`. The contract is corrected; the consumer check is
[`../s15-field-pass-init-core-consumer-check.md`](../s15-field-pass-init-core-consumer-check.md).

> **F3's boundary reading corrected 2026-09-26 (OPUS).** F3 did not stop "in the resource pipeline". A profiled re-run of
> the same case finds the following:
> - The request `0032FCA0` enters the loader's free-slot wait `0032E870`. That wait spins while the request free list
>   `[022C51D0]` is empty: 1,865 re-tests of `0032E8BB` in 3,000,000 instructions, and the list is still 0 afterwards.
> - The pump it calls on each spin runs `003E9780` once and returns every time.
> - The free list is empty because this world never built the loader pool: `003692D0` did not run.
>
> F3's recorded facts (the entry with `(1, 0xD4)`, the path lookup, the main-thread store, `+0x10` bit 3 not set) are
> unchanged. Only the word "boundary" was wrong.
> [`../s15-opus-replay-boot-world/`](../s15-opus-replay-boot-world/) runs the deferred arm with the pool built, from a
> script's own request.

## Not covered

- ~~**the interpreter `0025E4C0`**: no record's wait list selects its arm here.~~ **Executed** in
  [`../s15-opus-replay-boot-world/`](../s15-opus-replay-boot-world/), over shipped field scripts bound by the real loader
  (X1).
- ~~exit A itself~~ **Executed** there (X2): a shipped script's driven actor settles through its own entries.
  ~~the init core `002620E0`~~ runs in `arms.py` F1, from its second call site.
- ~~the audio path~~ executed (F1). The slot-0 deferred request `0032FC30` is entered, and F3 stops at the loader's
  free-slot wait (corrected above).
- a live game.

I2 ("no iteration cap") is a statement about an absence. The control shows that nothing in the loop stops it, up to the
replay's budget. It does not prove an absence of every possible exit.
