# S-38: the character render object's constructor, transform publish and teardown executed (OPUS, 2026-09-25, block 353)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
[`CONTRACT-character-render-object.md`](../../../17-Presentation-Rendering/CONTRACT-character-render-object.md) §13 reads
*"None. No experiment executes these four bodies."* This harness runs three of the four:
- the constructor `001F4DA0`;
- the transform publish `001FB120`;
- the teardown `001F51E0`.

It tests R-1..R-3 and R-5..R-7.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 347. **No application stub
and no stop boundary.**

**Fixtures:**
- six idle objects at `0x76300000`, plus the frame singleton `[01F7F598]` (a zeroed block whose `+0x1C` byte selects the
  bank);
- a 0x668-byte object buffer, filled `0xCC` before construction;
- a record-array vector (`+0x58`) holding one 0x318-byte element, whose first qword points at a zeroed object;
- three 64-byte source matrices.

**The ready latch `+0x4B4` is set to 1 by fixture** for the publish cases. Its setter, the 2,328-byte finish-setup method
`001F6E70`, is **not** executed.

**6 / 6 pass, and `result.json` is byte-identical over three runs** (md5 `b9eb1a1cd9b9902ff3cf2746a23642d7`).

| case | contract item | observed |
|---|---|---|
| `R2_R3_construct` | R-2, R-3 | Over the `0xCC` fill, `001F4DA0` installs vtable `00903B68` and clears the latch with **one byte store at `001F4EC9`** |
| `R7_clear_latch_publishes_nothing` | R-7 | With the latch at 0, `001FB120` returns at `001FB13A` with **no store** to the object or the element. Both banks keep their previous bytes |
| `R5_selector_picks_one_bank` | R-5 | With the latch at 1, selector `[01F7F598]+0x1C` = 0 puts the three source matrices in bank **A** (`+0x4C4`) and leaves bank B untouched; = 1 puts them in bank **B** (`+0x584`) and leaves A untouched |
| `R6_publish_has_no_loops` | R-6 | Static: 105 instructions, 48 `movups`, no backward jump |
| `R1_one_size_both_ends` | R-1 | Static: the allocation at `001BD527` and the sized delete at `001F5309` both load `0x668` |
| `R2_teardown_vtable_chain` | R-2 | `001F51E0` stores the class vtable `00903B68` at `001F51F9` (the class's second and last reference). The base destructor then installs the base vtable `00906D10` at `00212C87`. The latch is not cleared |

## What the execution adds

1. **The bank choice lives outside the object, and it is named:** the byte `+0x1C` of the singleton `[01F7F598]`, read
   through the one-instruction accessor `00189120`.
2. **The publish also writes the element.** Beside the bank, it stores two floats into the record-array element: `+0x8` /
   `+0x10` for bank A, `+0xC` / `+0x14` for bank B. So the element carries a per-bank pair as well.
3. **The teardown ends on the base vtable.** An object after `001F51E0` carries `00906D10`, not the class's `00903B68`.
   R-2's "two references" still holds.

Routed to FABLE (§13 can cite this block).

## R-4 executed (OPUS, 2026-09-26): the latch's sixteen readers (`r4.py`)

`r4.py` imports `check.py`, whose six cases run first and unchanged (`result.json` keeps md5 `b9eb1a1c…`). It executes
every reader of the ready latch `+0x4B4` on an object built by the shipped constructor. The latch is 0 as constructed, or 1
written by fixture; the setter `001F6E70` is not run.

**6 / 6 pass, and `r4_result.json` is byte-identical over two runs (md5 `09961ce4…`; `19813b73…` before case P2 was added). No application stub.**
- **Observation stop (disclosed).** A run with the latch set is stopped when it reaches the gate's WORK successor. The
  body past the gate is outside R-4 and reads state this world does not plant.
- **Planted data only.** The singletons behind `[01F811C8]` (`001AD440`), `[01F81168]` (`001A9930`), `[01F81428]`
  (`001D50D0`'s lazy cell) and `[01F7F5E0]` (`0018B4E0`), plus slot 16's one-entry list, record, element and pass bytes.

| case | observed |
|---|---|
| `C_census_17_reads_16_functions_2_writes` | re-derived from the image: every one-byte operand at displacement `0x4B4` over the graph's whole function table. **17 reads in 16 functions**, and exactly the two byte writes of R-3 (`001F4EC9`, `001F7729`) |
| `E_entry_readers_skip_when_clear_and_proceed_when_set` | **13 functions gate at entry**: the 11 methods in slots 3, 8, 9, 10, 12, 13, 14, 19, 20, 24 and 30, plus the non-virtual `001F89E0` and `001FAD50`. With the latch clear, each returns through its SKIP successor, never reaches WORK, and calls nothing but the epilogue's cookie check `00808C40`. With it set, WORK is reached. **`001F89E0` (ResetState) writes `+0x480` (its `edx`) at `001F89E7` before its gate**, so it is not a pure "may I run at all" |
| `G_getter_returns_the_latch` | slot 27 `001F86D0` returns the byte (0 / 1); **it has no gate** |
| `P_1F5D70_reads_latch_after_its_scene_test` | `001F5D70`'s first read is instruction 30. It comes after three lookups and the scene test `[001AD440()+0xA8] >= -1 → skip`. With the scene test passing, the latch clear skips to `001F68A0` and the latch set reaches `001F5E14`. Its second read is case P2 |
| `P2_1F5D70_second_read_clears_4B5_when_set` | run to the end, **with no stop**. With the frame byte `[01F7F598]+0xC34`, `+0x4B6`, `+0x4A8` ≥ 0.75 and `+0x480 = -1` planted, the body jumps (`001F5E4B`) to the second read `001F688E`. **With the latch set, it clears `+0x4B5` (`001F6899`, the run's only object write) and returns.** With the latch clear, the first read already skips to `001F68A0` and `+0x4B5` is kept |
| `L_slot16_latch_is_a_per_element_term_not_an_entry_gate` | slot 16 `001FA3D0` with the latch **clear** runs its setup calls and its submission loop. It reaches `001FA5C3` for the element and skips it (`001FA61E`), then **completes, calling `001F8D10`, `001FA0E0`, `001F8C00` and `001FB120` — each of which skips at its own entry gate**. With the latch set, the element proceeds (`001FA5CF`) to a second term, the record's `+0x10` bit 0. **With the mode word `001A9930()+0x2CC` = 2, the loop bypasses the per-element test altogether** (`001FA5C1 → 001FA5E4`, the emit path) |

### What R-4 execution adds (OPUS)

1. **"Twelve entry preconditions" counts the getter.** Of the thirteen vtable readers, eleven gate at entry, the getter
   returns the byte with no condition, and slot 16 tests it per element. The non-virtual `001F89E0` and `001FAD50` gate at
   entry too, and `001F5D70` gates its body only after a scene test. So there are **13 entry gates over 16 functions**.
2. **ResetState's store precedes its gate:** `+0x480` is written whatever the latch.
3. **Slot 16 applies the per-element test only when the mode word is not 2.** With the mode at 2, the element goes
   straight to the emit path `001FA5E4`, skipping both the latch term and the record's `+0x10` bit-0 term. That path calls
   the object's slot 14 (`+0x70`, `001FA0A0`), which is itself latch-gated at entry (read statically; not executed past
   `001FA5E4`).

Routed to FABLE, the contract's author (`OPUS-NOTE-FABLE-S38-R4-READERS-MEASURED`).

## Not covered

- the finish-setup method `001F6E70` (the latch's only setter);
- the bodies past each gate (outside R-4);
- a live game.
