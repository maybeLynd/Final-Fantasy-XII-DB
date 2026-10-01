# S-15 runtime: per-invariant stub exposure for EXP-048 / EXP-049 / EXP-106 (OPUS, 2026-09-25, block 299)

**Row:** S-15, the field runtime pass. The runtime cell is MIXED with the qualifier "no per-invariant stub-exposure
analysis yet". The binding gap reads "contract spans the system exactly; nothing live, and BattleUnit is 4 of 177 rows
type-resolved". The contract is `04-Actor-Entity/CONTRACT-field-runtime-pass.md`. This note scores nothing.

## Substitutions per record

| record | real | substituted |
|---|---|---|
| **EXP-048**, **EXP-049** | resolver `003588B0` with its encoder / family bodies (6 and 10 bodies) | **none** ("no callee is stubbed"). EXP-049 stops before the native refresh `00326500` and never executes it |
| **EXP-106** | the pass `0025D9E0` (1,297 B), the wait resolver `0025DF00` (1,228 B), the init core `002620E0`, the focus chain `003590D0` → `003588B0` / `00358940` / `00263FF0`, every gate and head leaf reader, the mode chain, the wait checkers, the settle / preamble leaves, `00269860`, the cookie check | the interpreter `0025E4C0`, audio `00261F90`, the deferred mode request `0032FC30`, the init-core external chain (10), lifecycle helpers (8), slot-0 post-chain helpers (15), the WRES predicate closures (5), the WRES arm checkers and settle notifies. The `record+0x38` settle callback is planted |

## Per invariant

| contract item | executed by | can a substitution reach it? |
|---|---|---|
| postcondition: `+0x11` bit 0 = `+0x10` bit 7 | EXP-106: the pass body's bit-7 republish | **no** (pass body) |
| postcondition: `02099D70` / `02099D78` current | EXP-106: the focus chain, all real | **no** |
| postcondition: every actor of the slot driven at least once | EXP-106: the drive loop calls the **real** `0025DF00` per actor | **no** for "driven". *What* each drive resolves (wait kinds, settle) passes through the scripted WRES predicates and arm checkers. No S-15 invariant claims that |
| postcondition: `+0x24` / `+0x38` one higher | EXP-106: the pass body | **no** |
| **I1** the drive repeats zero times (gated on a nibble nothing sets) | EXP-106: the repeat gate in the real body | **no**. "Nothing sets it" is an image-wide static census, which covers the scripted callees' bodies too; execution only shows the gate reading 0 |
| **I2** the drive loop has no iteration cap | static (the caps of the other three loops positively identified) | n/a: an absence is not executable |
| **I3** `02099D78` null two ways, indistinguishable | EXP-106 focus chain + EXP-048 / 049 resolver cases (advance / renewal, stale handles) | **no** |
| **I4** the pass reports success when it does nothing | EXP-106: the pass body's early-return arms | **no** |
| precondition: the slot index is unchecked | static (`imul`, no bound) | n/a |

## For the scorer

- **No application stub reaches an S-15 invariant or postcondition.** The scripted set is the per-actor work below
  `0025DF00`'s dispatch and the slot-0 post-chain. Its effects are per-actor outcomes, and the contract makes no claim
  about them.
- **The binding-gap text is not a runtime reason.** "BattleUnit is 4 of 177 rows type-resolved" is types debt, and the
  types cell is MET. "Nothing live" is the live half, which no replay supplies.
- `live_game` is false.
