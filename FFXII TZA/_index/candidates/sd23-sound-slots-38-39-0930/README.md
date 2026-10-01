# SD-23: what the `Sound` family's slots 38 and 39 answer, and what callers do with it (OPUS, 2026-09-30)

Register row SD-23 was registered by SWE2-DATA (`f7a3292bd`, sound-variant-selection.md §2). It asks what capability
slots 38 (`+0x130`) and 39 (`+0x138`) mean to their callers, given that the audio-range scan found 16 calls through
`+0x130` and 2 through `+0x138`. This record is static. The checker is `sd23_sound_slots.py` (output
`sd23_sound_slots.out`, `FAILS 0`). It uses `Tools/analysis-kit/gfz-scripts/retool.py`, including its RTTI reader.
**Status proposed: NARROWED.**

## What each class answers (OPUS, F1-F2)

The bodies are `007E57B0` = `xor al, al; ret` (false) and `007E5800` = `mov al, 1; ret` (true). Read from each class's
primary vtable (named by RTTI):

| class | slot 38 | slot 39 |
|---|---|---|
| `Sound`, `RandomSound`, `OrderSound`, `SwitchSound` | false | true |
| `VariationSound` | **true** | true |
| `CycleSound` | false | **false** |

## What the callers do with it (OPUS, F3-F4)

- **Four of the 16 `+0x130` calls are not this slot.** All four are in `007F0820` (`007F0DA8`, `007F0DCD`, `007F0DF5`,
  `007F0E0D`), and they use a float result (`comiss` / `subss` on `xmm0`). That is another class's slot 38. The same
  function's `+0x138` call (`007F0A23`) is therefore not the Sound family's slot 39 either.
- **The other 12 `+0x130` calls test a boolean.** A true answer, which only `VariationSound` gives, makes the caller
  skip work it does for a sound's own record, or take a variation-specific path:

| site | a true answer (a `VariationSound`) makes the caller |
|---|---|
| `007B2F08`, `007B3336`, `007B3435` | skip registering / unregistering it in the lists at `01F40C50` / `02EAD570` |
| `007B31C9` | return 0 at once |
| `007B4BB5` | take the variation path (`007BD8D0`) |
| `007BD53B`, `007BD618` | skip the child / record step (`[obj + 0x38]` / `[obj + 0x20]`) |
| `007BD9EF` | skip the named-parameter lookup (G-11) |
| `007BDBD6` | use zero in place of a computed value (`xmm7 = 0`) |
| `007BE5CC`, `007BEB41`, `007BED8E` | skip the record's flag tests (`[rec + 0x19]` `& 9` / `& 0xA`) and class check (`[rec] == 0xD`) |

- **Slot 39.** The one Sound-family call (`007BF183` in `007BF0A0`) enters state 7 (`[obj + 0x54] = 7`) when the answer
  is true. So `CycleSound`, the only class that answers false, never takes that transition.

**Reading (an interpretation, not claimed as the slots' names):** slot 38 marks a sound that does not play a record of
its own but delegates to a chosen child (`VariationSound`). Slot 39 marks a sound allowed to enter state 7, which
excludes `CycleSound`.

## Limits (OPUS)

- **What state 7 means** in the `007BF0A0` state machine is not read.
- **The `007F0820` class**, whose float slot 38 and slot 39 it calls, is not identified.
- **Shipped data.** The row notes that no `RandomSound` or `CycleSound` is built from shipped data (§12), so the false
  answers of those classes have no shipped effect.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
