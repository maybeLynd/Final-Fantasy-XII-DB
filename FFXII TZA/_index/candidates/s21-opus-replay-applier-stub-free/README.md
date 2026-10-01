# S-21: the result applier executed with its real setters and callees over the shipped tables (OPUS, 2026-09-25, block 332)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-21's binding gap reads *"the setters are
stubbed"*. EXP-060 stubbed five setters, and EXP-149 ran the whole applier with scripted callees. Block 288 ran
`00385BA0` real inside EXP-149's harness. This harness runs `003112F0` with **no application stub**:
- the status operation `0030E360`;
- the recompute `0030FED0`;
- the owner resolver `0031B860`;
- the numeric setters `00300520` / `00300530` / `00300C90` / `00300CE0`;
- the inventory handlers.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` from block 331. `world.py` gains a faithful **UCRT
`rand` / `srand`** bridge (seed 1, `x = 214013·x + 2531011`, returns `(x >> 16) & 0x7FFF`), which the status operation
draws from. `shipped_pack.py` binds the `battle_pack` tables by shipped code (blocks 324 / 326 / 328):
- the directory relocation `003846F0`;
- `00236C30`'s own binding calls, except the two that need heap 6.

**Fixtures:**
- **Four idle objects** as zeroed blocks: `[0209BE80]`, `[01F7FFE0]`, `[0215E6E0]` and the battle-text object
  `[0209CC40]`.
- **The unit pool** `[0208E688]` (count `[0208E6A0]`, stride `0xF50`) with two units whose `+0x698` are the two planted
  stats records. `0031B860` walks it.
- **The result record, field-neutral** (§3):
  - per-bit parameters −1;
  - item dword −1;
  - layer bytes `0xFF`;
  - foe stat words −1.

**Stop boundary** (recorded, nothing substituted): `002B4090`, where a source HP write posts its damage display into
the battle-text layer (S-37 / S-38). The setter's call and arguments are recorded before it.

**4 / 4 pass, and `result.json` is byte-identical over three runs** (md5 `baf273eed8456affb82e9801548d657b`).

| case | contract item | observed |
|---|---|---|
| `I2_copy_through_without_masks` | I2 | With both masks zero, the applier copies each non-negative `+0x5C` dword to target `+0xBC` and each non-negative `+0xDC` word to `+0x13C`. A negative value preserves the destination, and zero is present. **No status call and no outer recompute** |
| `I1_I3_apply_bit_mode3_and_outer_recompute` | I1, I3 | `+0x54` bit 5 calls `0030E360(target, source, 5, 100, 3, 0x200, mode 3)` with that bit's parameters, and target `+0x64` bit 5 is set. The outer `0030FED0(target, 0)` at `00311AC5` follows with caller flags 0 and is skipped with `0x200` |
| `I1_remove_bit_mode0` | I1 | `+0x58` bit 5 calls `0030E360(target, source, 5, 0, 0, 0x200, mode 0)` |
| `I5_I6_I7_numeric_dispatch` | I5, I6, I7 | See the setter table below |

### The numeric dispatch

| record bits | setter | outgoing flags / note |
|---|---|---|
| target HP alone | `00300530` | **`0x50`** |
| target HP + bit 3 | `00300520` | `0x50` |
| target HP + A19, A10, A18, A6 | `00300530` | **`0x120`**: bits 8 and 5 on, 6 and 4 off |
| target MP | `00300CE0` | |
| target MP + bit 4 | `00300C90` | |
| source HP (A7) | `00300530` | |
| source HP + bit 1 | `00300520` | |
| source HP, null source | none | no setter is called |

The target writes run to completion. The source HP writes reach the damage display, which is the recorded boundary.

## What the execution adds

1. **The setters and the status / recompute callees run real.** I1, I2, I3, I5, I6 and I7 hold, which answers the gap
   "the setters are stubbed".
2. **The status operation's flags argument is `0x200` whatever the caller passes**, for both the apply mask and the
   remove mask. I1's signature shows it as `flags`; the value is fixed by the applier. Routed to FABLE.
3. **§3's "layer bytes use `0xFF`" has an exact extent:** `+0x3C..+0x3D` (the loop at `00311788`, two bytes) and
   `+0x3E..+0x41` (the loop at `003117E4`, four bytes). A zeroed record reads as six present layers. It makes six
   `0030E130` calls and **sets the outer dirty flag**, so a zero-filled record is not neutral. Routed to FABLE.

## I8's foe paths executed (OPUS, 2026-09-26, `i8_foe.py`)

`i8_foe.py` imports `check.py`, whose cases run first and unchanged (`result.json` keeps md5 `baf273ee…`). It runs the
whole applier `003112F0` with its real callees. **No application stub.**
- **Planted data only.**
  - The target unit (pool slot 1) gets `+0x6A0` = a spawn block and `+0xE60` = a definition block, whose words at
    `+0x32` are the steal ids `0x3001`, `0xFFFF` and `0x4002`.
  - The target stats' kind byte `+5`.
  - A fifth idle object behind `[020927C0]`, which the steal tail reads through `002536A0`.
- **Recorded stop boundary (disclosed):** `002FEF30`, S-26's foe arm, which the kind-1 tail reaches. Every asserted
  write lands before it.

**4 / 4 pass; `i8_foe_result.json` is byte-identical over two runs (md5 `e4c419e0…`).**

| case | observed |
|---|---|
| `M_member_adds_only_on_foe_stats` | with target stats `+5 = 1`, record `+0x11E` / `+0x120` / `+0x122` / `+0x124` = 20 / 30 / 40 / 50 turn stats `+0x08` / `+0x0A` / `+0x12` / `+0x14` from 5 / 7 / 9 / 11 into **24 / 35 / 46 / 57**: each adds (word − the base byte `+0x2A` / `+0x2B` / `+0x2F` / `+0x30`). With `+5 = 0`, nothing changes |
| `E_effect_bytes_or_and_not_and_flag_only_for_kind1` | with the owning unit's stats kind 1, record `+0x128..+0x12B` OR into spawn `+0x7B` / `+0x79` / `+0x78` / `+0x7A`, and `+0x12C..+0x12F` AND-NOT the same four bytes. From `0x55` everywhere they become `+0x78..+0x7B` = `55 71 55 0F`, and the spawn's leading dword gains `0x80`. With kind 0 nothing is touched |
| `S_steal_ids_from_p_E60_skip_FFFF_kind1_only` | with kind 1 and record `+0x32..+0x34` all set, the ids at `p_E60 + 0x32` and `+0x36` (`0x3001`, `0x4002`) go to the item write `003008A0`, each followed by `00253770(3, 1)`. **Slot 1's `0xFFFF` is skipped** although `+0x33` is set. With kind 0 there is no item write |
| `G_the_gate_clears_availability_for_every_steal_byte_either_kind` | **not in I8's wording.** The availability byte `spawn + 0x14` is cleared by the gate `00385BA0` (`00385C17` / `00385C41` / `00385C6B`: `0x07 → 0x03 → 0x01 → 0x00`, one bit per steal byte `+0x34` / `+0x33` / `+0x32`). This happens **before the steal loop and for either kind**, so a steal byte aimed at a non-foe target uses up the availability and grants nothing. The steal loop's own clear (`0031146F`) then finds the bit already clear |

## I4 on the numeric path executed (OPUS, 2026-09-26, `i4_numeric.py`)

`i4_numeric.py` imports `check.py`, whose cases run first and unchanged. **Disclosed harness change:** block 332's damage
display boundary `002B4090` is lifted. `check.on_display` is neutralised and the display's closure joins the allowed set,
so the display body runs as shipped over the world's idle battle-text object. **No application stub. 3 / 3 pass;
`i4_numeric_result.json` is byte-identical over two runs (md5 `5ea37e87…`).**

| case | observed |
|---|---|
| `N1_target_hp_numeric_no_outer_recompute` | target HP only (A bit 8, value 40): `00300530` runs (HP 500 → 540), the display runs, and the applier returns. **The outer `0030FED0` at `00311AC5` is not called** |
| `N2_target_mp_numeric_no_outer_recompute` | target MP only (A bit 14): `00300CE0` runs and the applier returns. **No outer recompute** |
| `C_status_result_reaches_the_outer_recompute` | control, in the same world: a status result (`+0x54` bit 5) reaches the outer recompute once |

## The item scalar `+0x38` executed into real storage (OPUS, 2026-09-26, `item38.py`)

**The contract clause** (CONTRACT-apply-result-to-target §3): *"The item scalar at +0x38 is absent when its dword equals
-1 (the dispatched item ID is the low word)."*

`item38.py` imports `check.py`, whose cases run first and unchanged (`result.json` md5 `baf273ee…`, the same before and
after). It lifts the display boundary `002B4090` as `i4_numeric.py` does (disclosed). **No application stub.** It adds
two things, both run as shipped rather than planted:
- **The inventory storage.** The shipped rebase `0030B6A0` binds the class descriptors into the battle-state block
  `[02EBF190]`, as in `s29-opus-replay-inventory-storage`. The grant goes through the real mutate `003008A0` and is read
  back through the query entry `00309F30(item, 1)`.
- **The derived index.** The owned count going 0 → 1 fires `00325F40` → `00252E60`, which keeps its lists in the
  image-backed state block `*(020927C0)`. Two binders run:
  - `00253970`'s prefix, up to `00253997`. That is `00249840`, then `002EF640() + 0x8200` stored at `00253990`
    (`0216C480`).
  - The list initialiser `00253480`, which calls `00253240(list, 1)` for the twelve lists. `00253970` reaches it
    through `0035C560`.
  - The encoded base `[01F83530]` keeps its load-time zero (the encoded-id contract's `01F83530` residual).

**The item site:** `0031148D cmp dword [rbx+0x38], -1` / `je` skips it. Otherwise `003114A8` calls
`003008A0(movzx word [rbx+0x38], 1, 0 = add, 1 = owned channel)`. The grant's arguments are captured at `003114A8`.

**8 / 8 pass; `item38_result.json` is byte-identical over two runs (md5 `286b39b3…`).**

| case | observed |
|---|---|
| `item_scalar_grants_one_of_the_item` | `+0x38 = 0x00000001`: one grant call `(1, 1, 0, 1)`; item 1's owned count goes **0 → 1** |
| `only_the_low_word_is_dispatched` | `+0x38 = 0xABCD0002`: the grant is `(2, 1, 0, 1)` and item 2 goes 0 → 1. The high word is dropped by the `movzx` |
| `dword_minus_1_is_absent_no_grant` | `+0x38 = 0xFFFFFFFF`: no grant call, no count changes |
| `low_word_FFFF_with_zero_high_word_is_not_absent` | `+0x38 = 0x0000FFFF`: the absent test is on the whole dword, so the grant **is called**, with `(FFFF, 1, 0, 1)`. Items 1 and 2 and the index are unchanged |
| `storage_bound_by_the_shipped_rebase` | the rebase returns, `00253970` stops at `00253997` with `[020927C0] = 0216C480`, and `00253480` returns, in every run |
| `derived_index_appends_on_0_to_1` | after the grant, list 0 (items) has count 1 at `+0x47B8`, and its head at `+0x38CC` is `0001` (or `0002` for the high-word case) |
| `category_flag_bit4_set_by_list0` | `002CD650` sets `+0x3244` bit 4 (list 0 non-empty) → `0x10` |
| `absent_leaves_the_index_empty` | for `-1`: list 0's count is 0, its head is the initialiser's `FFFF`, and the flags are `00` |

## Where the lethal chain stops, measured (OPUS, 2026-09-26, `lethal_boundary.py`)

**A boundary record, not a closer.** The lethal chain had been listed as blocked on `[02AEE870]`, the table `0039BA00`
indexes. That table is `fontpack_it`'s directory entry 2 (the special-character table), and only the pack's load callback
`0039C150` binds it ([loader-bound-bin-families](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md)).

**What was run.** The shipped `us/fontpack_it.bin` (sha256 `21a32423…`) is bound by that callback:
- The pack is copied raw and its pointer stored at `[02AEE868]`, which is what the registrar `0039C3F0` does at `0039C467`
  once the file is read.
- `0039C150` then runs as shipped up to `0039C277`: the directory slots and the TIM2 relocator `0039BF50`. The texture
  upload `0017FBC0` at `0039C27C` needs the graphics context (below).
- Over block 332's world (its cases first, unchanged), with the display boundary lifted as in `i4_numeric.py`, a lethal
  target-HP result is applied (`-600` against HP 500).

**5 / 5 pass; `lethal_boundary_result.json` is byte-identical over two runs (md5 `fdc7f281…`).**

**What was observed:**
- **The font table read now succeeds.** The chain runs `0028F1F0` → the death credit `00469BB0` → `0032A150` → the
  battle-message display `002B4090` (message `0x180`). That display reaches the glyph emitter `002AC5F0`, which reads the
  font table through `0039BA00`.
- **The emitter then calls the graphics context `[01F811F8]`** (`001B5FA0` → `005C52D0` reads `+0x28`), and nothing in
  this world constructs it.
- **Control:** with a zeroed cell at `[01F811F8]`, the fault only moves deeper into the graphics layer (`001B51C0`).
- **Every contract step of the lethal chain comes after that display:** `0030E360(bit 0, mode 3)`, the `00312280` arm,
  `003299B0`, the killer id at `+0x30`, and `d64`. None of them is reached. HP 0 is the only write that lands.

So the lethal chain needs the graphics context, the same PhyreEngine layer the texture upload needs. Binding the font pack
is not enough.

## I4 on the source numeric paths, run to the applier's end (OPUS, 2026-09-26, `i4_source.py`)

`i4_source.py` imports `check.py`, whose cases run first and unchanged (`result.json` keeps md5 `baf273ee…`). It lifts the
display boundary `002B4090` exactly as `i4_numeric.py` does (disclosed). **No application stub.** No font and no graphics
object are needed on these paths.

**The source arms read their own record fields** (`00311700`–`0031177B`, read from the image):

| arm | selected by | value | setter |
|---|---|---|---|
| source HP | `A` bit 7 | `dword [rec + 0x20]` (`0031172F`) | `00300530`, or `00300520` with `A` bit 1 (`00311732`) |
| source MP | `A` bit 13 | `word [rec + 0x28]` (`0031174F`) | `00300CE0`, or `00300C90` with `A` bit 2 (`00311771`) |

The earlier harnesses set only `+0x24`, the target amount. So the source setter ran with a delta of 0, and against a source at
HP 0. That is where the old "its display reaches the text interpreter and the font" came from.

**4 / 4 pass; `i4_source_result.json` is byte-identical over two runs (md5 `4428a081…`).**

| case | observed |
|---|---|
| `S1_source_hp_numeric_runs_to_the_end_no_outer_recompute` | `A` bit 7 with `+0x20 = 40`: `00300530` is called with the source's stats record, and the source's HP goes 500 → **540**. The display runs, the applier returns, and the outer recompute site `00311AC5` is **never reached** |
| `S2_source_mp_numeric_runs_to_the_end_no_outer_recompute` | `A` bit 13 with `+0x28 = 30`: `00300CE0` is called with the source's record, and MP goes 100 → **130**. The applier returns with no outer recompute |
| `S3_the_target_is_untouched` | both runs leave the target at HP 500 / MP 100, and neither calls a target setter |
| `C_status_result_reaches_the_outer_recompute` | control, same world: a status result (`+0x54` bit 5) reaches the outer recompute once |

With `i4_numeric.py`, I4 is now executed on all four numeric arms: target HP, target MP, source HP and source MP.

## Not covered

- ~~a source-HP numeric result run to the end: its display reaches the text interpreter and the font (S-37's not-covered);~~
  *executed 2026-09-26 in `i4_source.py`.* The source amount is its own field, `[rec + 0x20]`, which the earlier runs never set.
  With a live source, the result runs to the applier's end (section below);
- the lethal chain (EXP-149's). **Measured, not assumed (`lethal_boundary.py`, below):** the boundary is the graphics
  context, not the font table;
- a live game.
