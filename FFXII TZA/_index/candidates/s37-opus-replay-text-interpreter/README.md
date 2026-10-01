# S-37: the text control-code interpreter, its parsers and the DynGeo draw executed as shipped code (OPUS, 2026-09-25, block 313)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-37's runtime cell is NOT MET with the gap "runtime
evidence". `CONTRACT-text-control-codes-and-dyngeo-draw.md` has no execution. This narrow OPUS harness runs its
interpreter, its escape parsers and its shared DynGeo draw.

## What was run

`check.py`:
- **Image.** It maps the whole SHA-asserted image. **No application stub.**
- **Allowed set.** The static closures of the entries (403 functions); entering anything else fails a case.
- **Imports.** The import directory is parsed from the image, **every IAT slot points at a unique trap**, and only
  `memcpy` / `memmove` are bridged by name.
- **One fixture callback.** The DynGeo draw's render target (its `rdx`) is a planted object whose vtable slots
  0 / 1 / 4 / 8 are recording callbacks: slot 0 returns a buffer, slot 1 returns a token, slots 4 and 8 record their
  arguments. This is an in-scope callback fixture for the device-side target, which has no statically constructible
  instance.
- **Fixtures** are planted data only: the text context, the painter `[0209CC40]`, the parsers' lookup base
  `[02AEE870]`, the sink singleton `[01F811F8]` (`0017FAE0(x)` stores `x` at `+0x28`), and the DynGeo instance.

**6 / 6 pass, and `result.json` is byte-identical over three runs.**

| case | contract item | observed |
|---|---|---|
| `A_ordinary_bytes_I1_I7` | I-1, I-7 | all 240 bytes `>= 0x10`, plus `0x0B`–`0x0D` (243 calls): **return 0, the cursor is not advanced**, `*out2 = 0`, and **`[0209CC60]` / `[0209CC68]` are zeroed on entry** (preset `0xDEADBEEF`) |
| `B_end_of_run` | §2 return semantics | a zero byte, and a match of the painter's `+0x10C8` terminator word, both return 0 |
| `C_lead_tokens_observed` | I-1 | `0x08` returns 1 and skips 3 bytes; `0x09` returns 1 and skips 1; `0x03` returns 0 after one byte; `0x0E` returns 0 after five. The other lead tokens stop at the first unplanted object (listed in `result.json`). **Every completed call returns 0 or 1** |
| `D_escape_selectors_I3_I6` | I-3, I-6 | all 256 selectors after `0x0F`. **Outside `0x20`–`0x70`, and for `0` and `_`: return 1 having consumed ONLY the `0x0F` byte.** The next call then returns 0 at the selector byte. In range, 34 of 81 selectors complete under the fixture; the rest stop at the first unplanted object |
| `E_parsers_I2` | I-2 | `003FFAB0`, `003FFB90`, `003FFC60`, `003FFDA0`, `003FFEE0` return **3** on every payload; `003FFCE0` and `003FFF10` return **4**; `003FFD70` returns **`(byte 2 & 0x7F) + 3`** (8, 8, 130, 3). The computed ones: `003FFB00` returned 4 / 3, `003FFBC0` returned 3 / 9. `003FFDF0` (the scanned length) did not run under this argument convention |
| `F_dyngeo_draw_layout` | §3 DynGeo layout | ten layers. A layer with a source **binds once** (slot 8 with the source); **a layer with a null source is skipped even with a count**; a zero count binds and draws nothing. Counts split into **batches of at most 480**: 1000 → 480 + 480 + 40, 481 → 480 + 1. Each batch copies **count × 48 bytes** from `base + done × 48` and then **draws with `edx = 2`** and `r9d = n` |

## What the execution adds to the contract

1. **I-6 has a visible consequence the text does not state.** "Outside `0x20`–`0x70` the escape is consumed and the
   run continues" is exact about the `0x0F` byte and silent about the selector. The selector byte is **not**
   consumed: the cursor stops on it (`002AD01A`–`002AD029`), so **the next call renders it as an ordinary
   character**. The same holds for the two do-nothing selectors `0` and `_` (I-3): an escape with an unknown or
   do-nothing selector prints its selector.
2. **The end of the run is a sink call**, not a bare return. `002AE31C` calls `0017FAE0(0)`, which stores into the
   `[01F811F8]` singleton's `+0x28`. So does `0x03`'s arm.
3. **I-2 is measured** for ten of the eleven parsers.

## Extension (OPUS, 2026-09-26): I-5, I-9, I-10, I-11, I-13 (`i5_i9_i13.py`)

`i5_i9_i13.py` imports `check.py` (its six cases run first, unchanged) and runs the DynGeo variants, the slot-11 thunks,
the deleting destructors and the interpreter with two painters. **7 / 7 pass; `i5_i9_i13_result.json` is byte-identical
over two runs (md5 `6e0bf5d9…`).** No application stub.

**Harness changes, disclosed:**
- **The allowed set** grows by the static closures of `00214210`, `00214540`, `002143E0`, `00214890`, `002148B0`,
  `00214860`, `00213AD0`, `00213AA0` and `00213B00`. The call graph has no tail-jump edges, so the shipped targets
  reached by `jmp` join too: `00183280` (from `00229DE0`), `00182EB0` / `00182E80` (from `00186AA0` / `00186A90`),
  `00225680` / `002256A0` and `0019C590` (the `free` thunk). Nothing is substituted.
- **`check.on_code`** is replaced by the same hook plus two additions:
  - **one more named import bridge, `free`**, which records its argument and returns. Any other unbridged import
    still fails by name.
  - **three more recording slots on the planted render target** (the fixture `check.py` already declares): slot 6
    (`+0x30`, with the 64 bytes at `rdx`), slot 15 (`+0x78`, with the three stack arguments) and slot 35 (`+0x118`).
    Entry into the base `002142A0` is logged in order with them.
- **Planted data only:** the display object behind `[01F82D18]` (`+0x00` mode, `+0x10` width, `+0x14` height), read by
  the prefix predicate `00182F50` and the float source `00229DE0` → `00183280`; and a second painter for I-5.

| case | contract item | observed |
|---|---|---|
| `I9_final_runs_prefix_then_enters_base_with_identical_draws` | I-9 | `Final` calls slot 6, then enters `002142A0`; its binds, maps, copies and draws **equal a direct base call** on the same ten layers, with the predicate true (two display sizes) and false |
| `I9_shadow_sets_state_then_enters_base_with_identical_draws` | I-9 | `Shadow` calls slot 15 with `(dl=1, 6, 7, [6, 7, 9])`, then enters the base; the draws equal the base's |
| `I9_shadowfinal_never_enters_base_and_draws_layer0_only` | I-9 | `ShadowFinal` **never enters `002142A0`**. It runs slot 6 (predicate true only), slot 15 `(1, 6, 7, [6, 7, 10])`, then one bind of layer 0's source, **one map of the whole count (1000, no 480 batching)**, one copy of 1000 × 48 bytes, unmap, and **draw `(3, token, 1000)`**. Layers 1–9 are not drawn |
| `I10_final_matrix_rows_from_pool_row0_x_is_aspect` | I-10 | slot 6 receives rows `008C5F80/90/B0/D0` **except row 0's first float**, which is `00229DE0`'s result: `height × 1.7777778 (008C5B38) / width`. **Identity on 1920×1080; `(1.4222223, 0, 0, 0)` in row 0 on 1280×1024.** With the predicate false (display mode ≠ 1), slot 6 is not called and the base still runs |
| `I11_thunks_shift_into_slot35_differ_only_in_third` | I-11 | for `r8b` ∈ {0, 1, 0x80, 0xFF} with junk in `r8`'s upper bits: each thunk calls slot 35 once, `rcx` = the target, `edx` = `r8b`. The third argument is **0** (`00214890`), **`r8b != 0`** (`002148B0`), and **`2 × (r8b != 0)` in `r8w`** (`00214860`) |
| `I13_destructors_stamp_one_vtable_and_differ_by_free_size` | I-13 | each destructor stamps `00906DE8` and returns the object. **With `dl = 1`, `00809950` receives size 0x160 / 0x170 / 0x168** and `free` receives the object; with `dl = 0`, there is no free |
| `I5_painter_is_read_through_the_global` | I-5 | the same four arguments on the same text `ABC`: with `[0209CC40]` → a painter whose `+0x10C8` word is `AB`, the call takes the end-of-run exit (`0017FAE0` entered, sink `+0x28` written); with `[0209CC40]` → a painter with no terminator, it does not; that painter given `AB`, it does again. **The painter is an input the signature does not carry.** (An ordinary byte and a stop both return 0 with the cursor unmoved, so the exit's sink store is the observable) |

### What the extension adds to the contract (OPUS)

1. **I-10's "literal identity matrix" holds only on a 16:9 display.** Row 0's first element is overwritten after the
   pool load (`0021426C movss [rsp+0x20], xmm0`) with `height × (16/9) / width`, from `00229DE0` → `00183280`
   (`00182EB0` = width `[disp+0x10]`, default 0x780; `00182E80` = height `[disp+0x14]`, default 0x438). The prefix is
   an **aspect correction**, which is the identity only on 1920×1080 and other 16:9 sizes. Routed to FABLE as a
   correction candidate for the contract's I-10 wording; this page does not edit it.
2. **ShadowFinal's layer-0 draw is not the base's layer walk inlined.** It draws with primitive `3`, not `2`; it maps
   the whole count at once, with no 480-vertex batches; and it does not skip a null source (layer 0 with a null
   source still binds 0, maps 0 and draws 0). Its slot-15 call passes `10` where `Shadow` passes `9`.
3. **I-11's shared third implementation `00214860` passes `2 × (r8b != 0)`**, and writes only `r8w`.

## I-4 executed (OPUS, 2026-09-26): the interpreter re-enters itself through `002B2150` (`i4.py`)

`i4.py` imports `check.py`, whose six cases run first and unchanged (`result.json` keeps md5 `e1bc61cc…`). **4 / 4 pass,
and `i4_result.json` is byte-identical over two runs (md5 `a58c5ffc…`). No application stub.**
- **Planted data only:** the singleton `[01F81200]`, queried through `001B5FB0` → `001B51C0` (a map lookup at
  `+0x30` / `+0x40`), as an object with an empty map. Block 313's lead-token arms stopped on its absence (a read of `0x40`);
  with it, tokens `01`, `04`, `06` and `07` complete, and `02`, `05` and `0A` reach `002B2150`.
- **Observation hooks** record each entry of `002AC5F0`, `002B2150` (with its text argument as an offset into the input) and
  `002A9F00`, with `rsp`.

| case | observed |
|---|---|
| `S_static_mutual_calls` | from the image: `002AC5F0` calls `002B2150` at 7 sites and `002A9F00` at 4; `002B2150` calls `002AC5F0` at `002B2393`, and `002A9F00` calls it too (`002AA6A8`) |
| `R1_token_splices_cursor_plus_1_and_the_interpreter_reenters` | tokens `02`, `05`, `0A` followed by `09 00`: the interpreter calls `002B2150` on the text after the token (cursor + 1), and `002B2150` calls the interpreter again one frame deeper on the `09`. Everything returns |
| `R4_mutual_recursion_to_depth_four` | `02 05 0A 09 00`: **interpreter → `002B2150` → interpreter → `002B2150` → interpreter → `002B2150` → interpreter**, strictly nested, with `rsp` decreasing at each level and every level returning. The spliced text is interpreted by the machinery that is interpreting it |
| `T_a_02_in_the_splice_ends_it_without_an_inner_call` | `002B2150` stops its splice at a `0x02` (as at `0x00` and at the painter's terminator word): `02 02 09 00` gives no inner call |

**Not covered for I-4:** `002A9F00`'s re-entry. Its loop reaches the glyph measure `002AC2F0` first, which needs the font
object that `0039C4A0` returns, and that object is not planted. Printable spliced bytes stop at the font in the same way.

## Why `002A9F00`'s re-entry stays unexecuted, measured (OPUS, 2026-09-26, `font_boundary.py`)

**A boundary record, not a closer.** I-4's remaining half was recorded as *"needs the font object `0039C4A0` returns (not
planted)"*. Here the shipped `us/fontpack_it.bin` (sha256 `21a32423…`) is bound by its own load callback `0039C150`:
- the pack is copied raw, and its pointer is stored at `[02AEE868]`, as the registrar `0039C3F0` stores it at `0039C467`;
- block 313's harness is used (`check.py`, whose cases run first; `result.json` keeps md5 `e1bc61cc…`), with `i4.py`'s
  planted `[01F81200]`.

**4 / 4 pass; `font_boundary_result.json` is byte-identical over two runs (md5 `2d671f3b…`).**

| case | observed |
|---|---|
| `F1_callback_binds_the_slots_then_the_render_enqueue_gets_no_command_slot` | the directory slots bind (`02AEE810` glyph sheet at pack `+0x40`, `02AEE870` special characters at `+0x168C0`, …) and the TIM2 relocator `0039BF50` runs. The callback then queues the glyph sheet's render commands: `0017FBC0` → `001B6510` → `001BA860`, which takes a slot from the render-state manager's command pool. The planted manager has no pool, no slot comes back, and the write at `001B6530` faults |
| `F2_the_font_object_cache_stays_null` | `0039C4A0(0)` returns `[02AEE800]`, which the callback caches at `0039C2AA`. That is **after** the render enqueue, so it stays 0 |
| `F3_measure_faults_on_the_null_font_object_with_or_without_the_pack` | `02 41 00` goes interpreter → `002B2150` → the glyph measure `002AC2F0` → `0039C4A0`, and faults reading the null font object. The same happens with or without the pack; `002A9F00` is never entered |
| `S_measure_calls_render_state_right_after_the_getter` | from the image: after the getter (`002AC330`), the measure calls `0017FD30` at `002AC34E` / `002AC363`. That is render state: its `dl != 0` arm calls `001B5FA0`, the graphics context `[01F811F8]` |

**So the font object sits behind the render layer twice over.** Its cache is written after a render enqueue, and its first
user calls render state. Binding the pack does not reach `002A9F00`. The same graphics context stops S-21's lethal chain
(`s21-opus-replay-applier-stub-free/lethal_boundary.py`).

## Not covered

- `002A9F00`'s re-entry into the interpreter and every printable-glyph path. The font object behind `0039C4A0` is cached only
  after the glyph sheet's render enqueue, and the measure calls render state next (`font_boundary.py`);
- the in-range escape selectors that still stop at an unplanted object;
- `003FFDF0`;
- the emitter and line-layout readers of `[0209CC40]` (I-5 is executed for the interpreter only);
- what the render target's slots 6 / 15 / 35 do with their arguments (they are the device side);
- the Phyre font draw the callers do for printable glyphs;
- a live game.

I-8 is executed by `B_end_of_run` (the `+0x10C8` terminator word stops the run with 0), and I-12 by
`F_dyngeo_draw_layout` (ten layers; a null source is skipped even with a count; a zero count binds and draws nothing).
