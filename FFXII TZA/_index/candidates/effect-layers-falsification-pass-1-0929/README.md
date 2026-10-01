# Consumer check: falsification pass 1 on CONTRACT-effect-layers (OPUS, 2026-09-29)

corrects: 10-Status-Periodic-Terminal/CONTRACT-effect-layers.md (L-1, its section 15 row, section 12: CON-176)

## What was corrected

- **L-1 said the rebuild never touches the mutable layer.** Its census counted the layers' first displacements only.
- A byte-range census over each 16-byte layer, on the record register, finds the rebuild reading **id 39 in both
  layers**: mutable `+0x6C` twice, derived `+0x7C` four times. Either one zeroes the clamp bound for current MP `+0x4C`
  and for `+0x06`.
- **What stands:** the rebuild writes neither layer directly. Its reconcile loop writes only stack buffers, and the
  derived layer changes through the mutate body in modes 3 and 1. So L-1's consequence (re-equipping never cures an
  inflicted status) holds.
- **L-6 is now measured, not carried:** diff = desired XOR current, then add with mode 3 and remove with mode 1.
- **What survives.**
  - §2's sizes; every chain union equals its catalogue size.
  - The addressing and the mode-to-layer map.
  - L-2's 5 / 6 and the either-layer recompute.
  - L-3's loop to `0x80` and its OR.
  - L-5's two revocation conditions as quoted.
  - §5's store to `02EBF188`.

## Current consumers

- consumer: [CONTRACT-auto-status-rebuild.md](../../../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md) agrees. Its
  §7a lists `+0x6C` and `+0x7C` among the record bytes the rebuild reads, and clamps current MP under those gates.
- consumer: [two-layer-effect-model.md](../../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)
  agrees: its id-39 row, "pins MP to zero", `+0x6C` / `+0x7C`.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-176`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_effect_layers.py` K1, V2 and V7.
- K1 fails unless the rebuild's record-based layer accesses are exactly the two `+0x6C` reads and the five derived
  accesses.
- V2 fails on any direct store into either layer.

run: verified at feb631dd4 (BROKEN 0), against the certified image `73461d08…`.
