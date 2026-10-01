# S-11: the field-environment variant executed — the tail call, the band and the one pre-clear (OPUS, 2026-09-25, block 352)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
[`CONTRACT-field-environment-variant.md`](../../../03-World-Area-Field/CONTRACT-field-environment-variant.md) §13 reads *"None.
No experiment executes this body."*
- Its body `WorldField_InitializeCurrentFieldRuntimeParameters` (`0026D910`) is S-12's weather apply. Block 303
  (`s12-opus-replay-weather-apply/`) executed it end to end, and that already covers EV-2 (the saturation case), EV-3 (the
  gated discard and the single clear) and part of EV-4 / EV-5.
- This block covers EV-1 and EV-6, plus EV-5 across a field's three slots.

## What was run

`check.py` is **block 303's harness**, with the same image, world, fixtures, shipped files and stop point, plus two
additions:
- published globals can be pre-planted;
- the registers are captured at the tail-call target `002E3D40`.

**Block 303's setup:**
- The whole SHA-asserted image is mapped, and **no application stub** is used.
- The run **stops at the entry of the presentation body `0040AAD0`**, a recorded stop boundary, not a stub.
- It uses `map_ref.bin` and `gramap_weatherinfo.bin` from the shipped extract (`in` locale); their sha256 values are in
  `result.json`.
- The field is 464 (selector 351), chosen from the data by block 303's rule.

**4 / 4 pass, and `result.json` is byte-identical over three runs** (md5 `19dc837c3961e869f3069840eec88bc2`).

| case | contract item | observed |
|---|---|---|
| `EV1_tail_call_with_zero_arguments` | EV-1 | The body leaves through `jmp 002E3D40` with **rcx = rdx = r8 = r9 = 0**. The presentation body is entered later with `(5, 0, 1, −1)`, which `002E3D40`'s own chain computes |
| `EV6_only_DBC_is_pre_cleared` | EV-6 | With all four globals planted `DEAD000x`, the first write of the call is `02099DBC` = 0 (`0026D946`), **before any lookup**. `02099DA8` / `DAC` / `DB0` are written once each, later, and `02099DBC` a second time |
| `EV6_unloaded_table_keeps_stale_values` | EV-6 | See the EV-6 consequence below |
| `EV5_band_from_the_preset` | EV-5 | Over the field's slots 1 / 2 / 3, with presets 2 / 4 / 5, `02099DAC` = **1 / 2 / 2**: 0 when the extraction returns 0, otherwise (preset ≥ 4) + 1 (`0026DA44` `cmp ecx, 4` / `setge`) |

**EV-6, the consequence.** The map_ref loaded guard `[02099D90]` is set to 0, a disclosed fixture flip standing for "not yet
loaded".
- The body skips from `0026D9D3` to `0026DA83`.
- `02099DBC` ends **0**.
- `02099DA8` / `DAC` / `DB0` **keep the stale `DEAD0001` / `2` / `3`**.

## What the execution adds

1. **EV-6's asymmetry, in execution.** A field entered before its table is loaded publishes a zero terrain byte
   (`02099DBC`) next to **the previous field's** environment class, weather band and lane byte.
2. **The skip conditions are the table's pointer and loaded guard.** The only branches that skip the three writes test
   `[02099D88]` and `[02099D90]` (`0026D9C6`, `0026D9D3`), plus two computed-pointer null tests.
   - In the shipped `map_ref.bin` no row has a negative block index. The row path therefore cannot skip, and the stale
     case needs an unloaded table.
3. **EV-1 as a measurement.** The tail call really receives four zeros. The non-zero arguments the presentation body sees
   are `002E3D40`'s own.

Routed to FABLE (§13 can cite blocks 303 and 352).

## Not covered

- EV-4's `(selector + 1) × 4` offset as a separate case (block 303's extraction calls exercise it);
- the fifth published global the variant page counts (a register-based write; see the contract's reconciliation note);
- a live game.
