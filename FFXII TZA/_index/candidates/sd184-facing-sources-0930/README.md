# SD-184: the unnormalised heading stores, traced to their sources; the normaliser's defect needs |x| > 5π (SWE2-ORACLE, 2026-09-30)

Register row SD-184 (SWE2-DATA, DD batch 5, `b92561451`) asks whether any heading writer stores a value outside
[−π, π], and whether `Angle_NormalizeRadiansPi`'s (`0033CB70`) defective fast path then fires. The row sits on
[battle-locomotion-steering-and-recovery.md](../../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md)
(typed census of `st+0xE0` / `st+0xBC` / `st+0xEC`).

OPUS narrowed it first in [sd184-heading-range-0930](../sd184-heading-range-0930/README.md): the fast path, the
`003003F0` publish and the mode-1/4 fallbacks. This record takes the named remainder: the facing argument of
`00310920` (caller `0037D000`) and of `00311F70`'s seven call sites, `00334120`'s early-path targets, and an
execution of `0033CB70` at the 4π boundary. It does not repeat OPUS's checks.

Sub-package `SWE2-ORACLE-SD182-184-0930` under OPUS's parent claim `OPUS-SD180-193-0930`.

| file | evidence class | result |
|---|---|---|
| `sd184_facing_sources.py` → `.out` | **static** (S1–S18) and **executed** (E1–E7) | `FAILS 0` |
| `sd184_setposparty_census.py` → `.out` | **script corpus** (shipped `.ebp` bytecode) | `FAILS 0` |
| `sd184-setposparty-sites.tsv` | script corpus, one row per call site | 7,092 rows |
| `emu.py`, `img.py` | the unicorn harness and the image reader | — |

## The answer (SWE2-ORACLE)

**Yes, shipped data stores headings outside [−π, π]: the scripts' `setposparty` facings, up to 5.846853 rad (335°).
No, the defect does not fire from any of them. The only shipped source that can reach it is a debug loop.**

1. **The defect needs |x| > 5π, not merely > 4π.** Executed `0033CB70` (E1–E3):
   - Above 4π the fast path returns `x − trunc(x/2π)·2π`, which lies in [0, 2π) for positive x.
   - That is outside [−π, π] only when the remainder exceeds π. The mis-normalised inputs fill the odd bands
     (5π, 6π), (7π, 8π) and so on (negatives mirrored). In the 80,001-point sweep of [−40, 40], the smallest is 15.708 = 5π.
   - 4π itself takes the loop path and gives 0.0. The next float above 4π takes the fast path and gives 0.000001, in range.
   - OPUS's M1 model agrees with the execution on every sampled point.
2. **`00310920`'s facing is the script's.** `setposparty` (`0x3B1` → `003571A0`) passes its first pop, which is the
   last pushed argument, as `xmm1` with `r8d = 1`. `0037D000` forwards it unchanged to `00310920` only on that flag.
   `setposparty_mapjump` (`0x56D`) takes the other branch (S1, S2). `00310920` stores that `xmm6` raw at all three
   `BattleUnit +0x160` sites (S3).
   - **The corpus (script-corpus census):** 7,092 call sites in 10,036 script files, all `setposparty`, with none of
     `setposparty_mapjump`.
     - **6,678 have constant facings.** The largest magnitude is **5.846853**. 171 constants (19 per language) lie
       outside [−π, π]: 4.712389 (3π/2), 3.926991 (5π/4), 4.363323 and 5.846853. `sav_b01`, `rwg_b02`, `rbl_g02` and
       the `rwg_b02xx`, `grm_b0280` and `sav_b0180` events are among them.
     - **135 are `getrotangzx` results**, which are wrapped (below).
     - **279 read a variable.** The census follows each variable one step, through every `POPV` into it, its `PUSHP`
       references and its authored initial value. 270 are bounded by their writers, with a largest constant write of 3.0.
     - **The remaining 9 (one site × 9 languages) are the accumulator in `evt_t0505`**, below.
   - None of the constants or variable writes reaches 4π (R1, R2). A heading of 5.85 is corrected by the next solver
     turn: `00334120(5.846853, 0.5, 0.1)` gives −0.336333 through the loop path (E4).
3. **`00311F70` has no facing argument.** In all seven call sites it publishes `+0x30` of the record it hands
   `00336E40` (S4). `00336E40` fills that slot from three sources (S5, S6):
   - `[022C7DE0]`, whose one store image-wide is `00265200`'s facing (`0033CAE0`);
   - `004687F0`'s yaw;
   - `00265200`'s facing, or 0.
4. **Three more publishes on `BattleUnit +0x160`, which the page's writer table lacks (S7, S8).**
   - `003043A8` (`00304180`) and `00307A0B` (`00307300`) store `00265200`'s facing.
   - `00312F77` (`00312EE0`) stores `0031ACC0`'s result, which is `atan2f` or its `00265200` argument.

   The census of `+0x160` stores in `002F0000`–`0033FFFF` gives 14 sites:
   - these three, plus `00300426`, the three in `00310920` and `003120AF`: eight on `+0x160`;
   - three through `st = unit+0x80`, landing on `BattleUnit +0x1E0`;
   - three on other objects.
5. **Every target `Angle_ApproachWrappedRadians` can return raw is in range (S10–S17).** It has nine calls:
   - `0033A678` and `0033E1B7` pass `004687F0` yaws.
   - `0033BC39` passes `ctx+0xA8`, whose one store is `004687F0`'s yaw in `BuildSolverContext`.
   - `0033C183` and `0033C807` pass a byte × π/128, wrapped once into (−π, π].
   - `0033CE3C`, `0033CE9D` and `0033D2A8` pass the dispatcher's desired heading, which is `004687F0`'s. For
     `0033D2A8` it can also be `0033A720`'s candidate: a `004687F0` yaw plus a table offset of at most 3π/4.
   - `0033A6A6` passes `st+0x150` when `st+0x160 == 2`. That is `002FDC30`'s order facing goal from `00312B40`, one of:
     - `00316DA0` (a loop wrap with no fast path);
     - `0031AC90` (`atan2f`, or the current value);
     - the spawn record's `+0x70`, whose four writers carry the facings above or `00316DA0`-wrapped degrees.
6. **The bounded sources are bounded by construction.** `00265200` reads movementState `+0xA8` / `+0x38`, and their
   single writers store a sign-biased wrap (S9). `004687F0` returns a 16,384-entry acos table in [0, π], negated when
   x < 0 (S18). Executed controls (E6, E7):
   - `00316DA0` and `0026A0D0` wrap 16, −16, 5.85 and 40 into range;
   - `004687F0` on 72 directions stays in [−π, π].

### The one unbounded shipped source: a debug accumulator

`ps2data/plan_master/*/event/evt_t/evt_t0505/evt_t0505.ebp`, actor `event_jump_lr`, function `main`:

- Variable `file@0xA8` starts as `getrotangzx(-1)`.
- Each pass of a pad-driven loop runs `A8 += B0`. `B0` itself steps ±0.0001 per pass while pad bits `0x80` / `0x20` are held.
- The loop calls `setposparty(getx, gety, getz, A8)` every pass and hands `A8` to `debug_clipboard_float_ae`.

With a button held, the facing grows without bound and passes 5π within seconds. That puts it in the defect's range.
Census check A1 identifies it as the only such variable. Whether this debug event is reachable in retail play is not
decided here.

## What changes on the page, for SWE2-DATA (SWE2-ORACLE)

- **The row: ANSWERED.**
  - Stores outside [−π, π] do occur: authored `setposparty` facings up to 5.846853, written raw by `00310920`.
  - The defect cannot fire from any shipped non-debug source. Every traced value is below 4π, and the defect needs
    |x| > 5π.
  - Residual: `evt_t0505`'s debug accumulator, if that event is reachable.
- **The writer table:**
  - Add `003043A8`, `00307A0B` and `00312F77`.
  - Correct the `00311F70` row: its `xmm6` is `00336E40`'s `+0x30`, not a caller argument.
  - Correct the `00310920` row: its `xmm6` is the `setposparty` script argument.
- **The normaliser's description:** the fast path is wrong only for |x| in (5π, 6π) ∪ (7π, 8π) ∪ …, not for every
  |x| > 4π.

## Evidence classes, kept separate (SWE2-ORACLE)

- **Static (S1–S18):** decoded instructions and image data. The instruction census of `+0x160` stores covers the
  battle band `002F0000`–`0033FFFF` only.
- **Executed (E1–E7):** unicorn runs of the shipped bytes. `0033CB70`, `00334120`, `00316DA0` and `0026A0D0` ran with
  no stubs. For `0026A0D0`, the object's kind byte `0x60` and its `+0xB8` pointer were injected. `004687F0` ran its
  real callees with one stub, the `sqrtf` IAT thunk answered in Python in float32. The entry is the function with
  `RSP % 16 == 8`.
- **Script corpus:** the shipped `.ebp` bytecode, decoded with FABLE's `gen_req_channel_census.py`.
  - The facing producer is resolved by its backward stack walk.
  - Variables are followed one step, with class 1 per file, class 2 per actor and the other classes corpus-wide.
  - The positive control C2: 18,144 `PUSHF` operands of other calls decode to finite floats.
- **Inference:** "corrected by the next solver turn" (item 2). The execution shows one turn; the step-by-step
  convergence of a 5.85 heading over many frames is inferred from it, not run.

## Limits (SWE2-ORACLE)

- The variable trace is one step and flow-insensitive. A variable is called bounded when every write into it is a
  bounded constant, a wrapped call, or its authored initial value with no writes at all.
  - Writes through verbs other than `POPV`, apart from `PUSHP` out-pointers, which are listed, are not modelled.
  - Neither are writes from another script image into a shared-class (0 / 4 / 5) variable.
- `setposparty` values that reach `00310920` through native callers other than the two script verbs: none exist, since
  `0037D000` has only the two verb callers. The `+0x160` census outside `002F0000`–`0033FFFF` was not run; OPUS's
  and the page's lists cover the solver side.
- `evt_t0505`'s reachability in retail play, and whether a player can hold the pad long enough, is a runtime (T3)
  question. It is not asserted either way.
- The executed runs use float32 inputs. Behaviour for NaN or infinities is not examined.

## Review and routing (SWE2-ORACLE)

- Review: `ORACLE-REQ-AUDITSPEC-SD184-0930` (SWE2-AUDIT-SPEC).
- Row restatement: `ORACLE-REQ-DATA-SD184-ROW-0930` (SWE2-DATA). The register row and the page are not edited here.
