# S-25: the enmity operations executed over shipped foes, shipped party rows and shipped actions (OPUS, 2026-09-25, block 345)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** Block 305's exposure note for S-25 says "enmity
unexecuted". This harness runs the enmity bodies of
[`CONTRACT-enmity.md`](../../../09-Combat-AI-And-Gambits/CONTRACT-enmity.md) and tests E-1..E-8:
- apply `003216E0`;
- write `00321850`;
- propagate `003219D0`;
- adjust `00321B00`;
- decay `00321530`;
- write-all `00321D30`.

It runs them over:
- two foes installed by the shipped installer `0023A570` from `rsn_b.ard`, bound by `003EA710`. Each foe's threat vector
  lives in its own spawn record (`unit+0x6A0` = BKEI);
- three party members on shipped battle-state rows;
- the **shipped action rows** at registry slot `[02EBF138]`: 543 rows of 60 bytes, of which 165 carry all three enmity
  parameters.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 344. **No application stub
and no stop boundary.**

**Fixtures:**
- six idle objects at `0x76300000`;
- units 0–1: foes installed by class 1, each with its own spawn;
- units 2–4: party members owning rows 0–2;
- slot map 0 = {0, 1, 2}, with maps 1–4 built by the refresher `003266C0`;
- planted vector contents, per case;
- foe 1's list at `+0xBC4` / `+0xBC8` (E-5 only).

The FrameLimit scale `[01DFE0B8]` is 1.0 from the world's boot. It is set to 2.0 for E-7's second run, then restored.

**8 / 8 pass, and `result.json` is byte-identical over three runs** (md5 `4966247139f13378ff06423d2324f37c`).

| case | contract item | observed |
|---|---|---|
| `E4_three_parameters_third_negated` | E-4 | Shipped action 0 (`+0x1D` / `+0x1F` / `+0x20` = 12 / 2 / 4): `003216E0` makes exactly three calls — write, propagate, and adjust with **edx = −4** |
| `E2_threat_is_stored_on_the_target` | E-2 | Member 0 hits foe 0. **Foe 0's** vector gains id 0 (0 → 12), and its entries for members 1 / 2 fall 30 → 26. The timer byte is untouched |
| `E5_grudge_alone_does_not_propagate` | E-5 | Foe 1 holds 5 for member 0 but does **not** gain from the hit on foe 0 |
| `E5_propagation_needs_grudge_and_perception` | E-5 | See the E-5 table below |
| `first_grudge_seeds_the_vector` | (new) | A foe with no grudge, and write id 0 += 12: the entry becomes **22** (+10 at `0032193A`), and the other valid ids' zero entries become **1** |
| `E3_class_gates` | E-3 | A **foe-class caster** makes no call at all: the gate at `0032170D` reads the caster's stats `+5`. A write aimed at a **party** unit returns without a table write (`003218D0`) |
| `E8_suppression_gates_the_write` | E-8 | See the E-8 table below |
| `E6_E7_decay_interval_and_step` | E-1, E-6, E-7 | See the decay list below |

**E-5.** `003219D0(id 0, 2, …)`:

| foe 1's state | direct target | foe 1 after |
|---|---|---|
| grudge 5, and lists foe 0's handle | foe 0 | **5 → 7** |
| grudge 0, and lists foe 0's handle | foe 0 | stays 0 |
| grudge 5 | null (the list is not consulted) | **5 → 7** |

**E-8.** `00321850` writing id 0's entry:

| target status | entry written |
|---|---|
| 0 | yes (22) |
| bit 0 | nothing |
| bit 31 | nothing |

**The decay (E-1, E-6, E-7).**
- It fires write-all with **edx = −10** on calls **30 / 60 / 90 / 120** at FrameLimit scale 1.0, and **60 / 120** at 2.0.
- Entries 25 / 12 / 5 become 15 / 2 / **1**, then 5 / **1** / 1, then **1 / 1 / 1**.
- The counter is byte 0 of the same vector (E-1).

## What the execution adds

1. **Propagation needs perception as well as a grudge.**
   - E-5 says *"'Perceiving' is a grudge already held, not proximity"*.
   - Measured: with a direct target, `003219D0` also requires the other foe's list at **`+0xBC8`** (count `+0xBC4`,
     16-byte entries) to hold the target's handle `[target + 0x10]` (`00321A82`–`00321AB4`). A grudge alone does not
     propagate.
   - With a null direct target the list is skipped.
   - What fills `+0xBC8` is not claimed.
2. **A held grudge never decays to zero.**
   - E-6 says *"a foe left alone forgets ten a second"*.
   - Measured: the write floors a previously positive entry at **1** (`0032191D`–`00321923`: a result ≤ 0 with a positive
     old value becomes `r12d` = 1).
   - So decay drives every held grudge to 1 and holds it there. Such a foe stays eligible for E-5's propagation
     indefinitely.
3. **The first grudge is special.**
   - Going from no grudge to a grudge adds **+10** to the increase (`0032193A`, taken when `00321770` returns 0). With other
     entries held (E-2's 30 / 30) it is not added.
   - It then walks the vector and sets every other valid id's zero entry to **1** (`0032194B`–`003219A5`, validator class 2).
   - So after one hit a foe holds a minimal grudge against the whole party.
4. **E-3's caster gate is the caster's stats `+5`.** The contract says "`003216E0`'s gate on the definition selector's high
   byte". The byte read at `0032170D` is `[caster + 0x698] + 5`. That is the same byte D-1 reads, which E-3's own conclusion
   already states.

Routed to FABLE.

## Not covered

- the engagement hold (E-6's second half): `0030C210` / `0030BB30` returned 0 for these units, so the hold was not taken;
- the query side (the four-party-slot scan);
- which engine code fills `+0xBC8`;
- a live game.
