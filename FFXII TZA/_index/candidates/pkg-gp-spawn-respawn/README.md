# PKG-GP-SPAWN-RESPAWN: first corrections (FABLE, Claude Opus 5.5, 2026-09-29)

affected: `05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md` (l.95–103, §13, the §14 runtime row),
`05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md` (§3 "`+0x10` not seen
written", §5b "EE-12 a live question"), `04-Actor-Entity/battleunit-slot-pool-and-actor-class.md` (`00236A60` row)

The package is [`PKG-GP-SPAWN-RESPAWN`](../../completion-packages/PKG-GP-SPAWN-RESPAWN.md). An explorer pass mapped the stages,
and each correction below was re-checked from the image or the record it cites.
[`respawn_checks.py`](respawn_checks.py) ([output](respawn_checks.out)) runs N and W, FAILS 0, static.

- **P1 (N).** The contract reasoned from the three accessors (`00235F50` / `00235FB0` / `002366E0`, script-only) to "no native
  code reads the fields". That is a getter's callers taken for the data's readers.
  - The automatic spawn selector `00235720` reads limit `+0x0A` against count `+0x08` (`002358AB`), and `seconds − stamp
    +0x0C` against cooldown `+0x10` (`002358D1`–`002358D7`).
  - It re-admits at elapsed **≥** cooldown. The scripts check **>**.
  - The model: a 10 s cooldown admits at t+10, not at t+9.
- **P2.** §13's "callees stubbed" was superseded on 2026-09-26 by the s17 replay (callees real). The record
  [`s17-opus-replay-group-completion`](../s17-opus-replay-group-completion/README.md) quotes that sentence as the gap it
  closed.
- **P3.** The §14 row "any runtime observation: none exists" contradicted the contract's own §13 citation of EXP-019 (live,
  pre-kill).
- **P4 (W).** The entry initialiser `002395A0` writes `+0x10` = the row's base + `rand % (range + 1)`, or 0 (`00239628`–`00239652`).
  The group page's "not seen written … EE-1 stands" predates the field map's reading.
- **P5.** EE-12 is ANSWERED (the contract §14, whose EE-12 handlers were verified live).
- **P6.** The slot-pool page now points to the unit-definition page for `00236A60`.

| consumer | action | agreement |
|---|---|---|
| the group contract l.95–103 | struck; the native gate stated (N) | revised-here |
| the group contract §13 "stubbed" | struck; the s17 replay cited | revised-here |
| the group contract §14 runtime row | struck; EXP-019 named (pre-kill only) | revised-here |
| the group page §3 "`+0x10` not seen written" | struck; the writer stated (W) | revised-here |
| the group page §5b "EE-12 a live question" | struck; answered | revised-here |
| the slot-pool page, the `00236A60` row | pointer added | revised-here |
| `spawn-placement-and-retirement.md` l.297 and the keep-entry field map l.88–91 (the native reads) | already right | agrees |
| `OPEN-QUESTIONS.md` EE-1 / EE-12 rows | ANSWERED already | agrees |

Regression: respawn_checks.py N W. N rejects "no native reader" and fixes the ≥ boundary; W rejects "`+0x10` not written".
run: respawn_checks.py at d22ad1b95, FAILS 0.
