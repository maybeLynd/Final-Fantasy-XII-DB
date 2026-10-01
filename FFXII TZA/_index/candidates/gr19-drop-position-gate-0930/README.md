# GR-19 answered: a kill drops loot only where the party leader could stand at the death spot (OPUS, 2026-09-30; glosses corrected 2026-10-01)

Register row GR-19 asks what the defeat body's drop gate decides about the death position. `00319490` passes the party
focus unit and the defeated unit's position to `003377C0`, and the drop is rolled only on a non-zero answer
(`00312588`-`00312597`). The page is [what happens when an enemy dies](../../../13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md).
Static, the certified image. Checker `gr19_drop_gate_check.py` (output `gr19_drop_gate_check.out`, **`FAILS 0`**).

## The answer (OPUS)

`003377C0` is not drop-specific: it is the shared "is this spot free and standable for this unit" test that movement also
uses (its other callers are `00334E00`, `00339630`, `0033BD70`, as SWE2-AUDIT-SEM noted). The drop gate asks it about the
**party leader** at the **death position**:

| step | condition (all must hold for a drop) | evidence |
|---|---|---|
| D1 | a party focus unit is resolvable: byte `02089340` bit 4 (the gate every focus-handle resolver uses) is set and the unit's flag byte bit 3 is set; otherwise the unit is NULL and the answer is 0 | `003194A8`-`003194D4` |
| D2 | the unit has an actor (`+0x10`); its collision extent pair (`ActorRuntime_GetClass3FloatPair` `00265090`) sets the radius | `003377E3`-`00337832` |
| D3 | **no other actor of the leader's collision group stands within that radius of the spot**: of up to 0x1C gathered actors (`00391D10` / `003920F0`), any one for which `00314EB0` holds (the two actors' `+0xC0` -> `+0x138` records share byte `+6` and do not share a non-zero `+0x119`) makes the answer 0; a class-1 actor is ignored when the leader is class 4 | `00337900`-`0033799A`, `00314EB0` |
| D4 | the spot is placeable: `00391410` accepts it, `Navigation_FindRegionForPositionXZ` `00384130` finds a navigation region (not `0xFF`), and `00336390` accepts - `0032A6A0` with the leader's movement-class byte `+0x1F4` at the spot and at the four points one radius away in x and z | `00337700`, `00336390` |

`00313F80`'s relation result only splits the tally of D3; every counted actor blocks the drop either way. When `002EA7F0`
refuses the leader, D3 is skipped and D4 alone decides.

~~**In player terms:** an enemy only leaves loot where your party leader could walk up to it - on the walkable ground of the
area, not wedged into scenery, and with nobody from the leader's side standing right on the spot. Kill it somewhere the
leader could not stand (a ledge off the navigation mesh, inside a blocker, crowded by allies) and the drop is not even
rolled.~~ *Corrected 2026-10-01 (OPUS) under SWE2-AUDIT-SEM's C2
([`auditsem-review-gr19-gr11-0930`](../auditsem-review-gr19-gr11-0930/REVIEW.md)): "walkable ground", "wedged into
scenery" and "crowded by allies" name what the bytes only test.*

**In player terms (corrected, OPUS):** an enemy only leaves loot where your party leader could stand. Kill it where the
leader could not, and the drop is not even rolled. "Could not stand" means one of four things. Another actor of the
leader's movement-body layer is within the leader's radius; this is the separation pass's pairing rule (`00314EB0`, layer
and owner), not a contact test. Or `00391410` reports a hit at the point. Or the point is off the navigation grid. Or
`0032A6A0` refuses the point or one of its four corners. `00391410` and `0032A6A0` are the two queries the leader's
forward-step clearance test also applies, and what they test is not named.

## Limits

- What byte `+6` / `+0x119` of the `+0x138` record name (the collision group and subgroup) and what `0032A6A0` and
  `00391410` test inside are read as conditions, not named; `02089340` bit 4's meaning is the focus-resolver gate's.
- Which actor classes 1 and 4 (`+0xE68` byte `+0x18` bits 1-3) are is not re-derived here.
- How the defeated unit's own body is kept out of the gather is not read: the gather's filter `0x1C`, or a release before
  the gate (SWE2-AUDIT-SEM C2, added 2026-10-01 by OPUS). The gather takes `003920F0` when any coordinate is NaN, not
  only x (C1).

## Consumers (routed, not edited here)

- The enemy-death page (FABLE's) and register row **GR-19**, via a DATA restatement request.
