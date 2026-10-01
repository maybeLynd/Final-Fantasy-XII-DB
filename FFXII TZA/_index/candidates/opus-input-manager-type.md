# InputManager (0x40) declared: camera inversion, the mouse-wheel accumulator and debounce, the poll gate and the input-mode bits (OPUS, 2026-09-26)

**Evidence class: STATIC**, from a receiver-proven census plus bodies read in full, in the shipping image (sha256
`73461d08…21f8`). Independent review is requested (author OPUS).

**Why.** `InputManagerPointer` (the cell `01F7FFE0`) has been declared for some time, but its one field read
"`void*`, the input manager singleton (type not yet declared)". Every binding poll goes through this object.

## Identity and extent

- **Allocation.** `InputManager_CreateSingleton` `00198750` calls `operator new(0x40)` (`00198767` `mov ecx, 0x40`,
  `0019876C` `call 00210EC0`) and stores the result at `01F7FFE0` (`00198784`). The getter is `00198790`.
- **Constructor `00195060`.**
  - It installs the vtable `008F3640`, whose only slot is `001955F0`.
  - It zeroes `+0x08`..`+0x37` and the bytes `+0x3A`/`+0x3B`, and stores the word `0x100` at `+0x38`, so `+0x39`
    starts at 1.
  - It then loads the binding profiles (`00196550` / `001965E0`) and republishes them (`00195DF0`).
- **Census.** `census_receiver_fixpoint.py` was run from three seeds with extent 0x40: `SEED=cell 01F7FFE0`,
  `SEED=call 00198790` and `SEED=ctor 00195060` (`EMIT_JSON` outputs in `opus-input-manager-census/`). The union
  reaches `+0x00`..`+0x3B`.
- **What the census missed.** The seeds do not follow the thin wrappers that fetch the singleton and tail-jump into a
  one-instruction method. The setter strip `00198670`-`001989F0` was therefore read in full, which adds `001989D0`
  (`+0x39`), `001989E0` (`+0x08`), `001989F0` (`+0x09`) and `00198700` (word `+0x3A`).

## Layout

| off | field | what fixes it |
|---|---|---|
| `+0x00` | vtable | `00195073` |
| `+0x08` | cameraXInverted (u8) | The translator multiplies right-stick X (axis 2) by −1.0 always, and once more when this byte is set (`0019740B`-`00197415`). Setter `001989E0` ← `001E0FF0` ← options-word bit 9. That is settings command 13, "Camera X-Axis", Normal 0 / Inverted 1 (`002DE160`), re-applied at load by `002DDA30` (`002DDB7C`) |
| `+0x09` | cameraYInverted (u8) | The same for right-stick Y (axis 3). Setter `001989F0` ← `001E1020` ← bit 8, command 12, "Camera Y-Axis" (`002DE190`, `002DDB68`) |
| `+0x0C` | wheelNotchTotal (i32) | The translator's kind-3 arm reads axis 3 of `[0x796E20()+0xDF8]+0x150` (vtable `+0x20`, `edx` 3), divides by **120.0** (`008F3A28`), which is `WHEEL_DELTA`, and adds the notches here (`0019739A`). `001E0A10` takes the total (`005C3A30`) and zeroes it (`001986D0`); eleven bodies call it |
| `+0x10` | wheelNotchesLastPoll (i32) | written after the debounce runs (`001973A4`), so the debounce compares against the previous poll |
| `+0x14` / `+0x15` | wheelActive / wheelArming (u8) | `00196480` (see below) |
| `+0x18` / `+0x20` | wheelStopTime / wheelIdleElapsed (f64) | off-delay |
| `+0x28` / `+0x30` | wheelArmTime / wheelArmElapsed (f64) | on-delay |
| `+0x38` | analogueAxisMoved (u8) | set when a translated axis value is non-zero (`0019743C`-`0019744B`). Read by `00197780` (via `001E0C10`, 8 callers, and `001E1120`). There is no clearing store besides the constructor's. What the UI does with it is not claimed |
| `+0x39` | pollEnabled (u8) | The poll `00196FF0` does nothing while it is 0 (`0019701D`). Its only setter is `001989D0` (slot 15 `0017D1A0`; `001E0FB0` with 0 after a fade) |
| `+0x3A` | inputModeBits (u8) | three bits, one per system-stop slot (below) |
| `+0x3B` | profilesDirty (u8) | set by every `+0x3A` change and by `00195DF0` (`00195FE0`). The poll tests it, calls `00196680` and clears it (`00197032`-`00197073`) |
| `+0x0A`, `+0x16`, `+0x3C` | unobserved spans (2, 2 and 4 bytes) | declared gaps |

**The wheel debounce `00196480(mgr, notches)`.** Time comes from `005CC930`, a QueryPerformanceCounter clock in
seconds, minus the base at `02CB60E8`.
- **When notches arrive:**
  - if the previous poll had none and the wheel is neither active nor arming, it sets `+0x15` and records the start
    time at `+0x28`;
  - while arming, `+0x30` = now − `+0x28`;
  - at ≥ 0.03 s (`01DF0970`), the word store at `+0x14` sets active and clears arming;
  - `+0x20` is zeroed.
- **When none arrive:**
  - right after a poll that had notches, it records `+0x18` = now;
  - otherwise `+0x20` = now − `+0x18`;
  - at ≥ 0.3 s (`008F3A20`), active is cleared.

## DD-4, which the register still carries as PARTIAL

DD-4 asks what `mgr[+0x39]`, `[+0x3A]` and `[+0x3B]` are.
- **`+0x3B`.** The register already has it as a dirty flag.
- **`+0x3A`.** It was answered on 2026-09-25 by FABLE under UQ-143 (the keymap page). The three bits follow
  system-stop slots:
  - bit 1 is slot 0 (the Battle Menu's stop);
  - bit 0 is slot 12 (`settutorial00timestop`);
  - bit 2 is slot 13 (the full-screen menus).

  This read confirms the setters and clearers:
  - the setters (`00198690` / `001986B0` / `00198670`) are called only from the stop record builder `00227680`;
  - the clearers (`00198710` / `00198730` / `001986E0`) are called only from `00225CD0` / `00225EB0`;
  - `00198700` (via `00182D80`) clears all three.
- **`+0x39`.** The poll-enable byte, on the input-stack page.

So DD-4 is answered by cross-reference. The staged register cell is in the OPUS inbox; it is not re-answered here.

## Not claimed

- which device class the kind-3 arm's `+0x150` object is (axis 3 divided by `WHEEL_DELTA` reads as the wheel, but the
  class was not identified);
- what the UI does with `+0x38`;
- who calls `GameApplication` slot 15.
