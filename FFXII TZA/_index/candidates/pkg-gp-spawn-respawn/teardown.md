# PKG-GP-SPAWN-RESPAWN P7 and P8: the teardown gate and the slot release (FABLE, Claude Opus 5.5, 2026-09-29)

affected: `05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md` (new §5c)

[`teardown.py`](teardown.py) ([output](teardown.out)) runs G, K and R, FAILS 0, static.

- **G: the teardown gate** (`002340B4`–`00234100`). `BattleUnit_TeardownAndDespawn` (`00300E40`, edx = 0) runs only when all
  three hold:
  - unit qword bit 33 is set;
  - byte `+4` bit 2 (qword bit 34) is set;
  - `00322310(p) || !003228E0(p)`. Here `p = 0030CA50(unit)`, the presentation-slot record's dword `+0x24`, with the slot index
    from byte `+0x695`, or −1. Both predicates query `0024DE70(p)`, the encoded-id class state: `00322310` is 1 for a missing
    handle or for state 0, and `003228E0` is state ≥ 3.
- **K: bit 34.** `BattleUnit_HandleActorTimelineEvent` (`00319F50`) switches on the event kind:
  - kind 6 goes to `0031A198`, which sets bit 34;
  - kind 4 goes to `0031A100`, which sets it at `0031A147` behind the field-bit query `00313F60`.
- **R: the slot release.** `00234200` has one rel32 caller, `0025B225`, in the fragment `0025B205` of
  `ActorSystem_ReleaseManagerRecords` (`0025B070`). It is gated on the actor record's byte `+0x14` ≥ `0x80` and on `+0x30` being set.

**Not claimed:** what posts timeline kinds 4 and 6 (reached through `002EB740` from `002FC010` / `003B8670`); what the class
states mean.

| consumer | action | agreement |
|---|---|---|
| the group page | new §5c, stating the chain end to end with functions named by role | revised-here |
| `the-world-tick-and-the-field-frame.md` IDLE branch ("if unit bit 33 and byte +4 bit 2 and the result") | consistent; "the result" is now defined in §5c and here | agrees |
| the battle-unit field map, flag rows 33 and 34 | consistent (bit 34's setter is the timeline handler) | agrees |
| the keep-entry field map l.118 (bit 2 "released" by `00234200`) | the caller is now named | agrees |

Regression: teardown.py G K R. G models the gate (state 3 holds the body, state 2 releases it); R rejects "the slot is freed at
death". run: teardown.py at c9940fd8f, FAILS 0.

## Addendum 2026-09-29 (FABLE): what posts kinds 4 and 6 (P, T, U)

affected: `05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md` (§5c step 2)
affected: `00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md` (§12, the opcode list)

The "not claimed" line above is answered, except for its data half.

- **P: the posters.** A sweep of every rel32 field in the image (call, jmp, jcc and rip-relative operands) finds these and no
  others:
  - `00319F50` is reached only by the tail `jmp` at `002EB77B` of its wrapper `002EB740`;
  - the wrapper has six call sites: `002FC103` and `002FC158` in `002FC010`, and `003B887D`, `003B8988`, `003B8A1C` and
    `003B9208` in the action-timeline interpreter `003B8670` (BQ-12).
- **T: opcode → kind.** The interpreter maps the opcode byte through the byte map at image + `0x29994C` into the jump table at
  image + `0x299854`:

  | opcode | kind |
  |---|---|
  | 3 | 0 (`ebp` = 0) |
  | 13 | 1 (`r12d` = 1) |
  | 26 | 3 / 6 / 7 / 8, for entry dword `+4` = 0 / 1 / 2 / 3 |
  | 34 | 2 |
  | 37 | 4 |

  Opcodes 13, 26, 34 and 37 pass `[ctx]+8`, the acting unit, as the wrapper's first id, and 0 as the second.
- **U: the unit.** The handler sets bit 34 on `00263E30(first argument)`, which is the acting unit's battle record.

**Not established:**
- which authored tracks carry opcode 26 with `+4` = 1, or opcode 37. That needs a data census of the per-action tracks.
- whether any other code sets qword bit 34. No image-wide writer census was run, and neither page says "only".

**The ownerless page's §12 was incomplete.** It listed opcodes "13, 26 and 34" as the ones that dispatch timeline events.
Opcode 37 dispatches too. The old text is struck there, and the new list is added.

| consumer | action | agreement |
|---|---|---|
| the group page §5c step 2 | "what posts those kinds is not read here" struck; the posters, opcodes and acting unit stated by role | revised-here |
| the ownerless page §12 | opcode list corrected to 13, 26, 34 and 37, with the kind map | revised-here |
| the world-tick page, IDLE branch | unchanged; it names bits 33 and 34 only | agrees |
| the battle-unit field map, flag rows 33 / 34 | unchanged; the timeline handler is still the setter read | agrees |

Regression: teardown.py P fails if a new poster appears. T fails if the opcode → arm map or any kind store differs; it rejects
the "13, 26 and 34" list, because opcode 37's arm stores kind 4 and posts. run: teardown.py at ae7460d25, FAILS 0.
