# SD-184 narrowed: the normaliser's defect needs |heading| > 4π, and the traced unnormalised writers are bounded (OPUS, 2026-09-30)

Register row SD-184 was registered by SWE2-DATA (DD owner read batch 5, `b92561451`) on
[battle-locomotion-steering-and-recovery.md](../../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md)
(typed census of `st+0xE0` / `st+0xBC` / `st+0xEC`). It asks two things: whether any heading writer stores a value
outside [−π, π], and whether the heading normaliser's defective fast path then fires.

The evidence is of two kinds:

- **Static:** the certified image. Checker `sd184_range.py`, output `sd184_range.out`, `FAILS 0`.
- **A Python model (M1):** the normaliser's two paths, taken from its instructions. It is a model, not an execution.

## What the record establishes (OPUS)

- **N1 and M1: when the defect fires.** `Angle_NormalizeRadiansPi` (`0033CB70`, 55 callers) has a fast path for
  |x| > 4π (`00D10B0C` / `00D10B20` = ±12.566): `x − trunc(x / 2π) · 2π`, returned with no further wrap. Its result
  lies in (−2π, 2π):
  - 16.0 → 3.43, and −16.0 → −3.43, both outside [−π, π];
  - 13.0 → 0.43, which happens to land in range.

  For |x| ≤ 4π the loops always reach [−π, π]. **So the defect can fire only for an input beyond 720°.**
- **S1: the facing publish's callers.** `003003F0` has three call sites:
  - `00325BB0` passes `st+0xE0` itself, a re-publish of the current heading;
  - `00326D60` passes facings from its party snapshot at `022C25A0` (two sites).
- **S2: where the snapshot's facings come from.** `00326BB0` fills the four `0x30`-byte entries with each member's
  position and facing, read by `00265200` from `movementState + 0xA8`. That field's single writer, `002E5E10`,
  re-runs the sign-biased wrap into [−π, π] on every store
  ([heading-speed-to-position-delta.md](../../../06-Movement-And-Navigation/heading-speed-to-position-delta.md)
  "The single writer, and it is a wrap"). So the snapshot replays in-range values.
- **S3: the mode-1/4 fallbacks.** `0033CEF0`'s fallbacks store the dispatcher's desired heading, which is
  `004687F0`'s yaw-from-direction result. It is bounded by construction.

So **every unnormalised route traced here carries a value that is in range by its source**, and none can reach 4π.

## What remains open (OPUS)

- **The facing argument of the other publish routes.** Two routes are not traced:
  - `00310920`, whose one caller is `0037D000` at `0037D0D8` (`xmm1 = xmm6`);
  - `00311F70`, whose seven call sites are in `00233AD0`, `00301140`, `00305430` (two), `00307300`, `00313670` and
    `00326D60`.
- **`Angle_ApproachWrappedRadians`'s early path.** At `00334187` it returns its `target` argument raw. Its targets
  are desired headings, but not every caller was traced.

Tracing those sources, together with an execution of `0033CB70` at the 4π boundary, is the rest of SD-184.
