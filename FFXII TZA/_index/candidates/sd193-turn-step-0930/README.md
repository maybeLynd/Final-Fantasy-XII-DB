# SD-193: the "eased" turn is a constant-rate step, not a curve (OPUS, 2026-09-30)

Register row SD-193 was registered by SWE2-DATA (DD owner read batch 5, `b92561451`) on
[setting-the-movement-mode-and-which-way-a-character-turns.md](../../../06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md)
section 9. It asks what curve `003EC040` computes for mode 3's eased turn.

The evidence is of two kinds:

- **Static:** the certified image. Checker `sd193_turn.py`, output `sd193_turn.out`, `FAILS 0`.
- **A Python model (M1):** the three helpers' arithmetic, re-computed from their instruction semantics and checked on
  sample angles. It is a model, not an execution.

## The answer (OPUS)

**There is no easing curve.** `003EC040(record index, target heading, mode, fast)` turns the character's current
heading (render record `+0x124`) toward the target at a constant angular step per call. The step is
`01DFE0BC × rate`:

- the multiplier `01DFE0BC` is 1.0 in the file and set to 0.5 by the boot fixups (`001EDDE0`);
- the rate comes from the record `003E56C0` resolves: `+0x24` normally, `+0x28` when the fourth argument is non-zero.

| case | result |
|---|---|
| fourth argument non-zero | `003A1AD0(current, target, step at +0x28)`: the constant-rate approach the shortest way round |
| mode 2 | `003A1AD0(current, target, step at +0x24)` |
| mode 0 | turn by `+step` (the positive way round, forced by `003EC510`), and snap to the target once within one step |
| mode 1 | turn by `−step` (the negative way round), with the same snap |
| mode < 0 or > 2, or no rate record | the target, at once |
| animation id (`+0xCC & 0xFFF`) `0x0D`, `0x35` or `0x36` in render-object state 1 | the current heading, held |
| invalid record, or a hidden record that is parked | 0 |

The helpers:

- **H2: `003A1AD0`.** It wraps `target − current` into [−π, π], moves `min(|d|, step)` toward the target, and wraps
  the result. `003A1980` is `min(|x|, s)`.
- **H3: `003EC510`.** It forces the delta into one direction: direction 0 lifts a negative delta by 2π, and
  direction 1 drops a positive delta by 2π.

**For modding:** a turn in these modes has a fixed angular speed per frame, half the record's rate after the boot
fixup. It stops exactly on the target. Modes 0 and 1 always turn the named way round, even past half a revolution.

## Limits (OPUS)

- **What the rate record is.** `003E56C0`'s record (its `+0x24` and `+0x28` rates) is named here only by those two
  reads. Which authored table it comes from is not traced.
- **Which argument is which.** The row reads the frame index `+0x78` as an input. The mode and fast arguments here are
  `003EC040`'s third and fourth; which caller values feed them (`002E5750`, `00358CB0`) is the row's reading and was
  not re-traced.
