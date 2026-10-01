# S-18: the heading/speed delta and the position getter executed as shipped code (OPUS, 2026-09-25, block 307)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
- The contract is `06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md`. Its §13 reads "None. No
  experiment executes these bodies".
- This is a narrow OPUS harness, not an ORACLE EXP.

## What was run

`check.py`:
- **Image.** It maps the whole SHA-asserted image. **No application stub.**
- **Real helpers.** `00267260` → `003B7730` and `00264460` (the planar predicate), and `003A1D30`
  (`sqrtf(fabs(x))`).
- **Failure rule.** Entering anything else fails a case.
- **Three import bridges**, through their real IAT slots (PE import directory): `00861F0E` → `008C2BB0` `sinf`,
  `00861F08` → `008C2BA8` `cosf`, and `00861F14` → `008C2BB8` `sqrtf`. Each returns `float32(math.fn(x))` and
  **records its argument**, which is how the angle wrap is measured.
- **Not executed:** the object-state override `00424080`. The harness takes the body's own skip:
  `[actor+0xC0]` null, or `dword [[actor+0xC0]] == −1`.
- **Fixtures** are planted data only: the actor, the movement block, the context, and `003B7730`'s two globals.

Every output is compared **bit-exactly** with a single-precision decode (struct round-trip; exact for single IEEE
operations). **5 / 5 cases pass, and `result.json` is byte-identical over three runs.**

| case | contract item | n | observed |
|---|---|---|---|
| `delta_class_gate_LD1_LD3_LD5` | LD-1, LD-3, LD-5 | 256 class bytes | only `0x60`–`0x7F` pass. The refused output over a `0xAA`-filled buffer is **exactly `{0, 0, 0, 1.0}`**, with no bridge call |
| `delta_spherical_LD4_LD6_grid` | LD-4, LD-6, the `+0xF8` repair | 3,200 (20 yaws × 20 pitches × 4 speeds × 2 `+0xF8` values) | `X = sin(yaw')·cos(pitch')·speed`, `Y = sin(pitch')·speed`, `Z = cos(yaw')·cos(pitch')·speed`, bit-exact. Speed 0 leaves `{0, 0, 0, 1}` with no trig call. A negative `+0xF8` is repaired to speed |
| `delta_planar_branch` | LD-4's scope (page §4) | 144 predicate combinations | **exactly one** combination is planar (`00267260` ≠ 0 and `00264460` = 0), and it gives **Y = 0 and no `cos(pitch)`** on X / Z |
| `delta_vector_arm_r8_nonzero` | not in the contract (page §8) | 4 | `r8d ≠ 0`: the output is the caller's vector with W = 1.0, and `+0xF8` = `sqrtf(|x² + y² + z²|)` via `003A1D30` |
| `getpos_LD2` | LD-2 | 256 class bytes + null | classes **{1, 3}** read `+0xB8` +0 / +4 / +8; every other class, and a null actor, gives `(0, 0, 0)` |

## What the execution adds to the contract

| item | observed |
|---|---|
| **LD-6's range is `[−π, π]`, not `(−π, π]`** | the recorded `sinf` / `cosf` arguments: yaw **`+π` → `−π`** and **`−π` → `+π`**. The wrap (`002E4464`–`002E44EF`) adds ±π chosen by the sign, applies a truncating fmod by 2π and subtracts it again, so it swaps the two endpoints. A port wrapping to `(−π, π]` differs at exactly `±π` |
| **LD-4 is conditional** | the contract states the spherical decomposition unconditionally. The shipped body drops the pitch term when `00267260(actor) ≠ 0 && 00264460(actor) == 0`. The page's §4 says so; the contract does not |
| **the `r8d ≠ 0` arm is not in the contract** | its §2 gives "yaw + pitch + speed → a 4-vector". The body also has a vector-copy arm that writes `+0xF8` |
| **speed 0 short-circuits** | `002E451E`: with speed `== 0.0` no trig is evaluated and the output is `{0, 0, 0, 1}`, **the same vector as a refusal** |

## Not covered

- the override `00424080` (its render-record world);
- the one caller, `Movement_UpdateActorFrame` (`002E50CB`);
- a live game.
