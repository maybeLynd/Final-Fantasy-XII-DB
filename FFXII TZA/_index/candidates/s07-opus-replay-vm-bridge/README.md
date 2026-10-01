# S-07: the script-to-native bridge's stack helpers, result writers and error reporter executed stub-free (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-07's runtime cell rests on EXP-013 and EXP-106, and
AUDIT-SEM notes that there is *"no stub-free closer yet"*. EXP-013 ran the bridge's pops with the error reporter
`008620C0` replaced by a `ret`. This harness runs every entry of `CONTRACT-script-to-native-bridge.md` §2, **and the
reporter itself**, as shipped.

## What was run

`check.py` is standalone. It maps the whole SHA-asserted image.
- **No application stub, no stop boundary, no bridged import.** Every IAT slot points at a trap, and reaching one fails
  the case.
- **Allowed set:** 8 functions. These are the seven entries' static closures plus `0016D6A0`, the reporter's tail-jump
  target; the call graph has no tail-jump edges.
- **Fixtures, planted data only:** a `VmValueStack` (0x284 bytes) and an `ActorStorageRecord` with its wait-slot array.

**8 / 8 pass, and `result.json` is byte-identical over two runs** (md5 `12060bd8f7c13d5816940b9b6aba3a03`).

| case | contract item | observed |
|---|---|---|
| `L_lifo_decrement_then_read` | §4 LIFO | pushes 11, 22, 33 pop back as 33, 22, 11, with depth 2, 1, 0 |
| `K_pops_coerce_by_tag` | §4 coercion | an int 7 popped as float gives 7.0; floats 2.9 and −2.9 popped as int give 2 and −2 (truncation) |
| `W_push_writes_all_four_arrays` | §4, §3 | tag 1 / 2, source kind 6, `+0x84` = 0, the value at `+0x184`. An int push and a float push of the same bits differ **only in the tag byte** |
| `G_push_guard_63_usable_slots` | §3, §4 | at depth `0x3F` neither push writes anything. After 70 pushes the depth is 63 and slots 61 and 62 are tagged; **slot 63 is never written** |
| `U_underflow_int_silent_float_reports` | §4, §10 | on depth 0 the int pop returns 0 **with no call to `008620C0`**, while the float pop calls `008620C0(1)` and returns 0.0. Depth stays 0 in both |
| `T_unknown_tag_int_reports_float_silent` | §10 | with tag 3, the int pop calls `008620C0(1)` and returns 0, while the float pop returns 0.0 **with no call**. Both consume the slot |
| `E_reporter_is_a_no_op_in_the_shipping_image` | §10 | `008620C0` is `lea rdx, msg; xor ecx, ecx; jmp 0016D6A0`, and `0016D6A0` is `ret 0`. Run as shipped, it writes nothing outside the stack. **EXP-013's `ret` stub therefore stood for exactly what ships** |
| `R_result_writers_signed_index_and_phase_byte` | §3, §4 | the entry is `[rec+0xA8] + (int8)[rec+0x11] × 40`. The int writer stores `+0x0C` and `+0x15 = 2`; the float writer stores `+0x0C` and `+0x15 = 3`. With `[rec+0x11] = 0xFF`, read with `movsx` as −1, they write the entry **before** the array |

## Not covered

- the seven spawn verbs' native functions (the far side of each wrapper);
- the interpreter's own reset of the shared depth (`CONTRACT-interpreter-core.md`, executed stub-free by Section11);
- a live game.
