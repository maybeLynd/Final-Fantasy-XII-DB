# SD-1: which force-fight consumers act on enemy units (OPUS, 2026-09-30)

Register row SD-1 was registered by SWE2-DATA ([r2-force-fight-toggle.md](../../../15-Input/Modal-Toggles/r2-force-fight-toggle.md)
section 7). It asks which of the force-fight flag's consumers act on enemy units, and so what the `FLEEING` state
changes for enemies.

`FLEEING` is the flag `01E0C2B8` at 0 ("force fight off"). ~~The flag has two readers (UQ-152)~~ The flag has two consumer readers (UQ-152); the second writer `00252C80` also reads its old value at `00252C94` *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd1-0930/REVIEW.md) item 2)*:

- `00253B90`, which returns 1 when the flag is 0. It is also reached through the jump thunk `0030C0D0`.
- `00253BA0`.

This record is static. The checker is `sd1_consumers.py` (output `sd1_consumers.out`, `FAILS 0`). It classes all
18 call sites of the three entry points:

- 8 of `00253B90`, the thunk among them;
- 8 of the thunk;
- 2 of `00253BA0`.

**The method.** For each site, the containing function's block graph is built. Any **kind test** that gates the site
is found. A kind test is a read of byte `+5` of the stats record a unit holds at `+0x698`: 0 is a party unit, 1 is a
spawned unit ([the battle-unit field map](../../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)).

A breadth-first walk of direct calls, up to 9 calls deep, then starts at the per-unit frame
`BattleUnit_UpdateLifecycleAndCombatFrame` (`00233F70`). That frame is the callback every bound battle unit runs,
party and spawned alike ([the world tick](../../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
section 2.4). The walk skips every call site that only kind-0 units can reach. It reaches 2,763 functions.

## The answer (OPUS)

**With the flag off, enemies (spawned units) are affected in four ways.** In each case the flag check has no kind
test, and the walk reaches it from a spawned unit's frame (P1):

| consumer | what force fight **off** does | route from the unit's frame |
|---|---|---|
| combo gate, `BattleUnit_UpdateCombatFrame` (`00308610`, check `0030877D`) | a unit without Confuse / Berserk skips the combo continuation (AN-4) | `00233F70` → `00308610` directly |
| combo continuation, `0030C010` (check `0030C02E`) | the same answer: the combo may not continue | `00308610` → `BattleAction_TryContinueComboSequence` `0030FA00` → `0030C010` |
| engagement, `BattleUnit_UpdateEngagementStateFlag` (`00307D10`, check `00307D63`) | the unit's engaged bit (`+4` bit 16) and bits 9–10 are cleared, `+0xDCC` is zeroed, and the globals `022C1F48` (bits 1–2) and `022C1F40` are cleared (`00307D6C`–`00307D7C`) | `00233F70` → `00310DB0` → `003112F0` → the status-change path `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` → `00307D10` |
| AI distance threshold, `BattleRuntime_GetModeDependentDistanceThreshold` (`00309A90`) | the threshold's value is chosen by the flag. The function takes no unit, but its caller here is a spawned unit's order check | `00308610` → `BattleUnit_SelectAndCommitNextAction` `00305AB0` ~~(a kind-1-only branch at `00305BA5`)~~ (`00305BA5`, reached by both kinds; the test at `00305B7D` diverts only a kind-1 unit whose status word has bit 27 set) *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd1-0930/REVIEW.md) item 1; the route stands)* → `00305CC0` → `003014C0` → `AiOrder_CheckActionPreconditions` `00301830` |
| locomotion: the step-distance divisor (via the thunk) | movement divisors ÷1.5 vs ÷3, ×0.25 vs ÷5 ([force-fight-mode.md](../../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md)) | six sites: `003368FD`, `00339D52`, `00339D7E`, `0033B02D`, `0033C3EA`, `0033D1A1`, reached through the spawned-unit movement branch (`00233F70` at `00234076` → `0033A240`) or the action path (`00308610` → `00307BE0` → …) |

**Four consumers act on party units only** (P2, P3):

- **Reason `0x24`** in the availability cascade (`002FFCF0`). The check sits behind `cmp byte [rdi+5], 0` at
  `002FFDAE`.
- **Stance** (`00308130`, `BattleUnit_ComputePartyBattleStance`). Each of its three callers first tests the same
  unit's kind for 0: `00301A6E`, `00307E0A` and `0030BFED`.
- **One locomotion site**, `00339C2C`, behind the kind test at `00339C24`.

**Four consumers are not on any unit's frame** (P4):

- the capability policy `00313A00` (the player's input);
- the field-frame orchestrator `00234590`;
- the command-menu readers of `00253BA0` (`00276650`, `00276D30`).

**For modding:** turning force fight off does not only stop the party.

- Every unit without Confuse or Berserk stops chaining combos, enemies included.
- A spawned unit's status change clears its engaged bit.
- Enemy AI order checks read the other distance threshold.
- Enemy movement takes the other step divisors.

What stays party-only is the action lock (reason `0x24`, which leaves only Dismiss and Dismount) and the party stance.

## Limits (OPUS)

- **Reachability is a static over-approximation.** A path shows that a spawned unit's frame *can* reach the check.
  It does not show that the path runs on a given frame, or how often.
- **The walk follows direct calls and tail jumps only.** Indirect calls and vtables are not followed, so a consumer
  reached only that way would read "not reached".
- **The kind tests are matched by pattern**: a `+5` byte of a register last loaded from `[.. + 0x698]`. The P3
  callers were read by hand. A kind test on a different unit's record than the one passed down would be misread.
- **What the combat difference looks like in play** (for example, whether enemies visibly stop comboing while the
  label shows) is a run-time observation and was not made. The static reading is enough to answer the row.
