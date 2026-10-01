# S-46 runtime: per-invariant stub exposure for EXP-056 / EXP-111 / EXP-144. No application stub reaches an RNG invariant (OPUS, 2026-09-25, block 295)

**Row:** S-46, RNG streams. The runtime cell is MIXED, with the qualifier "no per-invariant stub-exposure analysis
yet". The binding gap reads "the routing is unexecuted; only the algorithms are tested". The contracts are
`21-RNG-And-Determinism/CONTRACT-gameplay-generators.md` and `CONTRACT-which-generator-serves-which-roll.md`. This
note scores nothing.

## Substitutions per record

| record | runs as shipped | substituted |
|---|---|---|
| **EXP-144** routing (`evidence/s46-generator-routing/check.py`) | every consumer and generator body: `003185D0`, `00239210` → `00328370`, `0025ABA0` (and its probability call `002658B0`), `0038DB10`, `00389670`, `004005E0`, `0015BCF0` → `0018D680` → `0018D740` → `0018EE20`, the gameplay seeder `00863D30`. The harness only **logs** entry to these (`on_code`) | the `_time64` / `clock` **IAT imports** inside `0015BCF0` (fixed returns), plus the generic IAT boundary. No application function is scripted |
| **EXP-111** twist | `00866B90`, 463 B: a self-contained leaf | nothing |
| **EXP-056** save normalization + seed arithmetic | all 456 bytes of `00584210`..`005843D7`, stopping at the tail `00379CF0` | every outgoing **application** callee is a no-effect stub: accumulator reset/set, field transition, substructure cleanup, common normalization. `_time64` (IAT `008C3060`, resolved in that record) is controlled. It does not run the MT seeder |

## Per invariant

| invariant | executed by | can a substitution reach it? |
|---|---|---|
| generators §4: **one LCG draw = three multiply-add steps** | EXP-144 `lcg-loot-inliner` / `lcg-yaw`: `0x11111111 → 0x15EAB4E4`, bit-identical to three ANSI-C rounds, with `00328370` real | **no** |
| generators §7: **the MT seed expression** (`time_term`, `+ 0x258·timer`, `BTR` before `ADD`) | EXP-056: local arithmetic, then the tail argument at `00379CF0` | **no**. The expression takes only the `_time64` import (import-class) and the timer dword. The no-effect stubs feed save-normalization bytes, not the seed |
| the MT seeder and twist | EXP-144: `00863D30(0xACE1)` real every case, first draw `624 → 1` with a full twist. EXP-111: the SIMD twist under both gates | **no** |
| which-generator **I1** two disjoint MTs | EXP-144 `gfxmt-seed` / `gfxmt-draw`: `01F7F600` only, and `02EB3870` never touched | **no**. The time imports choose the seed value, not the state address |
| **I2** census method | static by nature; EXP-144 confirms both populations advance one stream | n/a |
| **I3** all LCG consumers share one stream | EXP-144 inliner and call-site consumers | **no** |
| **I4** the LCG seed counts areas entered | **not executed**: the LCG is planted, and the seeding caller `BattleSystem_InitializeAreaState` `00234320` does not run | coverage, not exposure |
| **I5** fixed graphics-MT address | EXP-144 `0015BCF0`'s `lea` of `01F7F600` for the init and twist calls | **no** |
| **I6** the correlation split: formula rolls on the MT, loot / AI on the LCG | EXP-144: each consumer advances exactly one generator | **no** |

## For the scorer

- **The exposure set holds no application stub on any RNG invariant.**
  - EXP-144's and EXP-056's time sources are CRT imports.
  - EXP-056's application stubs are downstream of, or beside, the seed arithmetic it claims.
- **One invariant is unexecuted:** I4, the area-count seeding.
- **The binding gap is stale.** EXP-144 executes the routing for every claimed route (9 cases, ×3 stable).
- `live_game` is false.
