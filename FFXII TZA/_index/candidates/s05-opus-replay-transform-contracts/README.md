# S-05: the transform primitives and the workbench save / restore executed stub-free (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-05's runtime cell is MIXED: *"EXP-115 … under isolated
original-code replay … no per-invariant stub-exposure analysis yet"*. Of S-05's three contracts,
`CONTRACT-transform-workbench-save-restore.md` ~~had no execution record at all~~ **(CORRECTED 2026-09-28, OPUS, on
ASTRA-RETURN-OPUS-WORKBENCH-DEPTH-TARGET-ALIAS: wrong. The contract's §13 has recorded an isolated original-code
differential of the pair since 2026-09-12, 3ff76b52b. What this harness adds is a stub-free NATIVE-REPLAY run of the
same two functions, with every IAT slot trapped. It is not their first execution.)** This harness executes both
behavioural contracts in one place.

## What was run

`check.py` is standalone. It maps the whole SHA-asserted image.
- **No application stub, no stop boundary, no bridged import.** Every IAT slot points at a trap, and reaching one fails
  the case.
- **Allowed set:** the static closures of the four entries, 9 functions. These are the four bodies plus the stack-cookie
  check `00808C40` and what it reaches; entering anything else fails the case.
- **Entries:**
  - the point transform `00398F90` (`rcx` = in, `rdx` = out);
  - the composer `00397910` (`rcx` = a, `rdx` = b, `r8` = out);
  - Save `0036D930` (`ecx` = count, then the pointers, variadic);
  - Restore `0036D8E0`.
- **Fixtures, planted data only:** the matrix rows `M[r]` at `022D91B0 + r*0x10`, the vf00 image's `w` lane
  `[01EF93FC]`, and caller buffers.

**9 / 9 pass, and `result.json` is byte-identical over two runs** (md5 `034006f350f151154acf0d3ea76b0dab`).

| case | contract item | observed |
|---|---|---|
| `P1_w_is_the_live_vf00_load_not_the_point` | primitives inv. 1 | The point `(2, 3, 5, w)` gives `(162, 272, 382, 492)` with `in.w = 1` **and with `in.w = 7`**. With `[01EF93FC] = 0` the translation row is not added (a direction); with `= 2` it is added twice |
| `P2_no_perspective_divide` | primitives inv. 2 | all four sums are emitted; the `w` lane is 492, not 1 |
| `P3_four_deposits` | primitives §5 | `022D9300` = the input verbatim (`w = 7` kept); **`022D91A0` = `(62, 72, 82, 92)`, the sum without the translation row**; `022D9310` and `022D8F90` = the result; `[rdx]` = the result |
| `C1_out_is_b_times_a` | primitives §4 | the composer's output equals `b × a` and differs from `a × b` |
| `C2_aliasing_is_safe` | primitives inv. 3 | `out == a` and `out == b` give the same 64 bytes as three distinct buffers |
| `C3_writes_exactly_the_64_bytes_of_out` | primitives postcondition | outside its own stack frame, the composer writes exactly `out`'s 64 bytes |
| `S1_save_is_variadic_and_assigns_depth` | save/restore run-note 1, §7 | 1, 3, 4, 5 and 8 items: 4 and more pass pointers on the stack. Each pointer is recorded at `02EC0A00 + i*8` and its 16 bytes at `02EC0800 + i*16`, and the depth `[022D8F08]` = count |
| `S2_not_a_stack_inner_save_overwrites_the_outer_frame` | save/restore §10, run-note 2 | Save A, B; clobber them; Save C; Restore. **Only C comes back.** A and B keep their clobbers, and saved pointer 0 now holds C's |
| `S3_restore_writes_back_zeroes_depth_and_is_idempotent` | save/restore §4 | Restore puts all three rows back and zeroes depth. **A second Restore writes only the depth word** and leaves the rows as they are |

## Not covered

- `CONTRACT-shared-transform-workbench.md` TW-1..TW-6: layout and ownership statements, byte-verified by AUDIT-SEM
  (2026-09-22) as a census;
- the callers and consumers of the workbench;
- a live game.
