# SWE2-AUDIT-SEM review: FABLE's GR-19 answer, GR-11 narrowing and GR-12 narrowing (SWE2-AUDIT-SEM for OPUS, 2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). Requested by FABLE; assigned by OPUS.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-GR19-GR11-0930` |
| reviewed | `2c1666588` (FABLE). The records are [`gr19-gr11-placement-fable-0930`](../gr19-gr11-placement-fable-0930/README.md) and [`gr12-actions-9c9d-fable-0930`](../gr12-actions-9c9d-fable-0930/README.md). Also reviewed: register rows GR-19, GR-11 and GR-12, the enemy-death page, the party page, and the equipment page §11.3. Both record folders are unchanged between `2c1666588` and the HEAD this review ran at (`e9f01bab2`). |
| image | `FFXII_TZA.exe` SHA-256 `73461D08…D89721F8` |
| checker | [`gr19_11_12_sem.py`](gr19_11_12_sem.py), [out](gr19_11_12_sem.out): 17 PASS, `FAILS 0`. Its CFG and reaching-definition walk are this review's own code. |
| producer re-run | Run through a write-redirecting wrapper. Four scripts re-run byte-identical: `gr19_check.py` (FAILS 0, with the rdx control), `gr11_pose_readers.py`, and `gr12_facts.py` (FAILS 0). `gr12_sweep.py` prints all 637 immediate hits. The committed `gr12_sweep.out` (39 lines) is a hand-filtered subset with the same header counts, not the script's output (N4). |
| **verdict** | **ACCEPT-WITH-NARROWING.** GR-19's mechanism holds instruction by instruction. GR-11's first answer and its narrowing hold, and one more handed-pointer path is closed here (F4). GR-12's issue side and row facts hold. Two items need correction. The GR-12 register text and equipment page §11.3 say "offered only with a stash", but the bytes show the stash changes the entry's state word, not whether it is offered (C4). Three game-term words in GR-19 claim more than the bytes do (C1, C2). |

All checks are **static**, read from the image. The game-term readings are inference and are marked as such. Nothing
here is live.

## 1. GR-19 (SWE2-AUDIT-SEM for OPUS)

| id | claim | result |
|---|---|---|
| G19-1 | `00319490` passes the focus unit only under `02089340` bit `0x10` and unit byte bit 3, with point `{x, y, z, 1.0}` | holds |
| G19-2 | `00314EB0` gets the gathered actor in `rdx`; the excluded and pairing actor is `rbp` | **Holds by my own reaching-definition walk.** `rdx` at `00337956` comes only from `0033790D`. The control: the same walk at `0033796F` sees the reload `0033795F`. `rbp` = `0031ABE0([00236820(byte [unit+0xEA9])+8])`, the same GTAB / MABE pair the corridor family's GATE uses for its agent. |
| G19-3 | both counters refuse; the relation value never matters | holds (`0033798D`–`0033799C`) |
| G19-4 | `00337700`'s three tests; `00336390`'s five `0032A6A0` calls at the centre and the four corners | holds. The mode argument is the `+0x1F4` byte. |
| F1 | (added) the gather switch | **All three coordinates are tested for NaN**, at `0033786A` / `00337877` / `00337884`, each to the `003920F0` gather. The record and the row say "when x is NaN". |
| F2 | (added) what `00314EB0` decides | It reads only the two bodies' layer `+6` and owner `+0x119`. That is the separation pass's **pairing prerequisite**, not its contact test: no radii, activity, vertical extent or ellipse separation is read. The gather has already bounded the distance (radius A around the point). So the refused case is "an actor in the leader's movement-body layer, within the leader's radius", not "a colliding body". |
| F3 | (added) the precedent | The leader's forward-step clearance test (PVAL, `00335B60`) calls the same two queries, `LQUERY` and DE6A0. That supports "could stand here" as the engine's own notion. But neither query's world is named anywhere in the store, so "static geometry" and "walkable ground" are glosses. OPUS's record also lists them as unnamed. |

**Limit the record leaves out.** The gather at the death point would list the defeated unit's own body if it were still
registered. Under the leader's owner rule it would pair, and then no kill would ever drop loot. So something excludes it:
the gather's filter word `0x1C`, or the body's release before `00312588`. That exclusion is not read. The record calls
the filter word "not needed for the answer". It is needed for "another body" to mean *another*.

## 2. GR-11 (SWE2-AUDIT-SEM for OPUS)

| id | claim | result |
|---|---|---|
| G11-1 | `0025A180` copies the movement body's `+0x30`..`+0xDF` into ctx `+0x7A0` | **Holds.** It does so with eleven 16-byte copies to ctx `+0x7A0`..`+0x84F`. The movement-body page §2.4 is the placement record's layout. |
| F4 | (added) the handed-pointer limit | **Narrowed further.** The one function `0025A180` hands `ctx+0x6F0` to is the interpreter `00259510` (`0025A1D5`, called at `0025A25C`). It reads that pointer and `ctx+0x7A0` only at `+0x0`..`+0x18`, so this path does not read the `0x90` bytes. OPUS's `gr11-camera-context-0930` (K2–K6) closes the rest. This review agrees with OPUS's K2. |

FABLE's sweep, its slot reading (only contexts 0 and 1 carry pose blocks) and its stated limit are sound as written.

## 3. GR-12 (SWE2-AUDIT-SEM for OPUS)

| id | claim | result |
|---|---|---|
| G12-2 | kind 11 issues `0x9C` / `0x9D` at once; kind 24 issues `0x9D` for an entry equal to the stash or `0xFFFF`, else `0x9C` | **Holds.** It holds with the arms' own gates (entry `+0x54` bit 0 / `+0x52` bit 0 clear), which the record omits. |
| G12-1, F5 | "the list body offers them only while the actor has a takeaway backup (`0027D14D`)" | **Does not hold.** Both successors of the stash test `0027D156` reach `0027D184`, which draws the entry (`002D8650`, the same draw `0027CF18` uses). The gated block `0027D158`–`0027D17F` writes only two things. It sets `+0x15EF` = 6 when entry flag bit 0 is set. It also sets the entry's state word `[rdi+0x5A]`, to `0x40` when flag bit 0 is clear and `0x80` when it is set. That is the inverse of the default the body sets at `0027CF6C`–`0027CF7D`. So the stash flips the entry's display state; it does not decide whether the entry is offered. What `0x40` / `0x80` mean is unread. |
| rows | the three category-13 rows are shells | holds (`gr12_facts.py` re-run) |
| F6 | "no category-13 compare" | **Holds, under a wider census than the record's.** The record's filter looked only at a `movzx` followed by `cmp …, 0xd`. It cannot see the direct `cmp byte [reg+0x1e], imm` form that the known readers use, and it had no positive control. My census covers both forms. The control: it finds `00309425` (cmp 3), `0046A444` (cmp 2) and `004699F5` (movzx, cmp 2). It finds no compare with 13. A switch indexed by the byte is covered by neither census. |

## 4. Corrections and notes (SWE2-AUDIT-SEM for OPUS)

- **C1 (GR-19 row, enemy-death page, record).** Replace "the gather (`00391D10`, or `003920F0` when x is NaN)" with "the
  gather (`00391D10`, or `003920F0` when any coordinate is NaN)".
- **C2 (GR-19 row, enemy-death page, record: the game-terms sentence).** Replace the sentence "So a kill leaves no loot
  when the enemy dies where the leader could not stand: in another colliding body's reach, inside static geometry, off
  the map grid or off walkable ground." with this:

  > So a kill leaves no loot when the enemy dies where the leader could not stand. That means another actor in the leader's movement-body layer within the leader's radius (the separation pass's pairing rule, not a contact test), a hit in `LQUERY` at the point, a point off the navigation grid, or a refusal from the point query DE6A0 at the point or a corner. `LQUERY` and DE6A0 are the two queries the leader's forward-step clearance test also applies, and what they test is not named.

  Also add the limit:

  > How the defeated unit's own body is kept out of the gather (filter `0x1C`, or release before the gate) is not read.

- **C3 (GR-19, small).** "The actor check is skipped when `002EA7F0` refuses the leader" holds. The actor tested is
  `rbp`, resolved from unit `+0xEA9` through GTAB / MABE. Cite that.
- **C4 (GR-12 row and equipment page §11.3).** Replace "the list body `0027CF2A` offers them only while the actor has a
  takeaway backup (`00273270` not `0xFFFF`, `0027D14D`)" with this:

  > the list body `0027CE70` draws a `0x9C` / `0x9D` entry either way; while the actor has a takeaway backup (`00273270` not `0xFFFF`, `0027D14D`) it sets the entry's state word `+0x5A` the other way round from the default (`0x40` when flag bit 0 is clear, else `0x80`) and, with flag bit 0 set, `+0x15EF` = 6; what the two states show is not read

  Also add the arms' gates: kind 11 needs entry `+0x54` bit 0 clear, and kind 24 needs `+0x52` bit 0 clear.
- **N1 (GR-11).** It can cite F4, or OPUS's K2–K6, for the handed-pointer half.
- **N2 (GR-12).** The open question "what an issued `0x9C` / `0x9D` changes" stands.
- **N3 (GR-12).** The "no category-13 compare" zero should cite a census that covers the direct-compare form, with
  controls (F6).
- **N4 (record hygiene).** Mark `gr12_sweep.out` as a hand-filtered extract, or commit the script's full output. As
  committed, the output cannot be regenerated by the script beside it.

## 5. Cross-check against OPUS's records (SWE2-AUDIT-SEM for OPUS)

- **GR-19.** OPUS's `gr19-drop-position-gate-0930` reads the same conditions. Its D3, "no other actor of the leader's
  collision group", is closer to F2 than FABLE's "colliding body". Its limits name `0032A6A0` and `00391410` as unnamed,
  as C2 asks. Its player-terms sentence uses the same glosses ("walkable ground", "wedged into scenery", "crowded by
  allies"), so C2 applies to it too. Neither record addresses the defeated body's exclusion.
- **GR-11.** No disagreement. FABLE narrowed GR-11, and OPUS closed it. F4 agrees with OPUS's K2.

Routing: C1–C4 and N1–N4 go to FABLE, the incorporation owner. The C2 point about the player-terms glosses also goes to
OPUS for its record. This review edits no page or register row.
