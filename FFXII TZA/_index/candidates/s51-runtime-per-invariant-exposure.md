# S-51 runtime: the EXP-130..137 chain's stub residue is resolved statically; §14.1 closed (OPUS, 2026-09-25)

**Row:** S-51 navigation mesh and corridor query. The runtime cell is REPLAY, *"no per-invariant stub-exposure analysis
yet"*. The contract is `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` (OPUS). This note scores
nothing.

## The records form a promotion chain

EXP-130..137 each execute the previous record's scripted leaves as shipped bytes. Every one is `contract: none`, a
consumer anchor for the family's entries (`PVAL 00335B60`, `GATE 003357B0`, `PATHW 0033A3D0`, `BLKCHK 00335F90`,
`00391410`). The scripted lists per record:

| record | scripted, traced not executed |
|---|---|
| EXP-130 | `0033D3E0`, `00383F10`, `00384130` (+ CRT `00861F14`) |
| EXP-132 | `00318CA0` (+ CRT) |
| EXP-133 | `00318CA0` (+ CRT) |
| EXP-134 | `0026E100`, `00318CA0`, `0032A6A0`, `003357B0` (+ CRT) |
| EXP-135 | fifteen leaves, including `00263E30`, `002E9FE0`, `00313F60`, `003588B0` |
| EXP-136 | `00231400`, `002315E0`, `00231820`, `00231900`, `00263FF0`, `00314F50`, `00377C20` |
| EXP-137 | **`0022F430`, `002324F0`, `002EF2B0`, `00381EB0`, `003DA5A0`**: the residue |

**The residue is five one-hop leaves, and the contract already resolves each statically** (§14.4, SWE2-CONTRACT
body reads):
- `EF2B0` returns a constant;
- `F4F0` is a nearest-edge selector that overwrites its context per edge;
- `F430` is a context writer plus walk driver; the fixture planted only the write half;
- `EB0` is point-in-unit-shape;
- `D5A0` is a horizontal-only capsule distance.

Where a fixture diverged from the bytes, §14.4 says so and gives the shipped behaviour.

## Per invariant (§4) and per failure path (§10)

| claim | depends on a scripted leaf? | owner reading |
|---|---|---|
| **§4: no global write on any returning path** | a static census over the 102-body closure, not an execution claim | **no execution exposure** |
| **§4: no verdict depends on a random draw** | static (§9) | **no execution exposure** |
| **§4: BLKCHK re-reads the mode byte** (`00335FB5`, then a reload at `00335FE4`/`00335FEB`) | body-local; the claim is the reload itself | **not reachable** |
| §4 preconditions (null guards on `OBJD`, `O1F2/3`, `MABESP`) | leaf bodies, real from EXP-135/136 on | **not reachable** |
| §10.1–10.7 (ordered compares, `cvttss2si` overflow, `angB == 0`, the GATE early return, PATHW asymmetry, stale handle, the LQUERY mask header) | the named bodies run real in the chain | **not reachable** |
| anything behind the five residue leaves | their shipped behaviour is read statically in §14.4 | **exposed to execution only; statically closed** |

## §14.1 closed in the same package

§14.1 said *"the agent's `+0x108` sub-record has no declared type"*. It needs none: **it is `BattleUnit` seen from
`+0x80`**.

The three proven fields are `collisionExtentA` (`+0x18C`), `collisionExtentB` (`+0x190`) and `placementMode`
(`+0x1F4`).

The source is either the live unit, or **an edited 0x610-byte snapshot** that
`AiOrder_CheckActionPreconditions` `00301830` builds on its stack and queries with instead of the unit. The contract
text is §14.1. The `CorridorNavAgent` `+0x108` row is corrected: its "on every path" was wrong.

## For the scorer

S-51's chained executions leave no application stub whose behaviour is unknown. The five residue leaves are statically
read in the contract. What the table's no-stub qualifier makes of "executed as a chain, residue read statically" is
the scorer's ruling. `live_game` is false throughout, and §13's live table is empty by the contract's own statement.
