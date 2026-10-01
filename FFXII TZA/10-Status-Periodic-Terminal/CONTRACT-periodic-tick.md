---
contract: Run one periodic maintenance pass over a battle unit — gates, five stages, one result
category: 10-Status-Periodic-Terminal
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: Periodic-Tick/what-the-periodic-tick-does.md, where-mp-comes-from.md
entries: ["00310DB0", "00385DF0", "003848E0", "00386C70", "00385570", "00385CA0", "00386860"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and the spine of §4 re-measured from
    the shipping bytes rather than from the pages — the sequencer's five targets and its tail call,
    the per-stage displacement matrix with stage 3 as its own positive control, and the result
    record's extent. **This records checks performed on that date, not the method of the original
    derivation**, which was FABLE's reading on the periodic-tick page; see §15.
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-30
  last_pass_kind: falsification
  last_pass_state: opus-periodic-tick-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the periodic tick

> **Authored 2026-09-21 by FABLE.** S-27's contract cell read **NOT MET** with the binding gap
> *"credited with S-26's contract; its own subject is uncontracted"*, and its index row said
> `contracts: none`. [`CONTRACT-status-write.md`](CONTRACT-status-write.md) is `scope: operation`
> over *changing a status*; it names this page in its `implements:` list but states none of the
> invariants that hold **across** the tick's five stages. Those invariants are the subject here.
>
> **The test this document is written against** is FRONTIER's: *a narrower contract is adequate
> exactly when the system's operations have no cross-operation invariant or ordering it leaves
> unstated.* §4 is seven such invariants, and each is one the operation contract cannot express
> because it is a statement about two or more stages at once.

## 1. Purpose

One **periodic maintenance pass** over one battle unit, run from the battle frame. It is the engine's
only place where a unit's condition changes because *time passed* rather than because something acted
on it: statuses count down and expire, MP drains on a beat, HP is credited out of combat, and the
per-status damage of Poison and Sap lands.

**The five stages change nothing themselves.** Every stage writes a stack-local result record, and
the pass ends by handing that record to the ordinary damage-application path. *Poison damage is not a
special case anywhere in this engine; only the builder differs from a sword swing.* **The tick around
them is not side-effect-free**: once gate 1 passes it recomputes two of the unit's own fields and may
clear a timed flag, all before the stages run — see §4's postcondition and I-1.

> **Corrected 2026-09-22 (FABLE) on SWE2-AUDIT-SEM's second return (rev 27511).** This paragraph said
> *"It changes nothing itself"*, and §7 still opened with *"deadline check → six gates"*. Both were
> pre-repair claims that the I-1 fix at `50fb65cf8` should have carried and did not. *The repair
> corrected the invariant and the postcondition and left the prose that had been written from the
> wrong invariant — which is the propagation half of a correction, and it is the half I missed.*

## 2. Interface

| | |
|---|---|
| **Entry** | `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`, **1,338 bytes**), one unit per call |
| **Builder** | `BattleFormula_BuildPeriodicStatusResult` (`00385DF0`, **83 bytes**) — a pure sequencer, no logic of its own |
| **Sink** | `BattleFormula_ApplyTargetResult` (`003112F0`), called at `00310FAC` with `(result, 0, bkbi, 0xFFFF, 0)` |

The builder's whole body is five calls in a fixed order, the last a **tail call** — re-read from the
bytes for this contract:

| | stage | address | call site |
|---|---|---|---|
| 1 | `BattleFormula_InitializeResultRecord` | `003848E0` | `00385E08` |
| 2 | `BattleFormula_AdvanceStatusTimersAndBuildResult` | `00386C70` | `00385E13` |
| 3 | `BattleFormula_AdvanceStatusLinkedAuxTimers` | `00385570` | `00385E1E` |
| 4 | `BattleFormula_ApplyGlobalPeriodicDrainModes` | `00385CA0` | `00385E29` |
| 5 | `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` | `00386860` | `00385E3E` (**`jmp`**) |

## 3. Types

**The result record** is `0x148` bytes, zeroed on the tick's own stack before the builder runs —
`mov r8d, 0x148` at `00310F6C`, `memset` (`00861EC0`) at `00310F7A`, builder at `00310F8B`. Its
fields, and **which stage owns each**, measured by sweeping all five bodies for each displacement:

| field | meaning | written by |
|---|---|---|
| `+0x24` | the **HP delta accumulator** | stages **2** (11 sites), **4** (4), **5** (3) |
| `+0x2A` | the per-interval MP drain delta | stage **4** only |
| `+0x2C` | flag word | stages 1, 2, 4, 5 |
| `+0x3E` | the **list of status ids that expired this tick** | stages 1, 3 |
| `+0x42 + slot*2` | the expired timers' new values | stages 1, 3 |
| `+0x140` | second flag word | stage **2** only |

**Two independent timer families exist and no stage touches both** — the single most load-bearing
fact in this subsystem:

| family | where it lives | keyed by | advanced by | rate |
|---|---|---|---|---|
| **status-word timers** | stats record `+0xBC[s]` (duration) and `+0x13C[s]` (beat) | the status's own bit `s` in the two status words | ~~**stage 2**~~ **computed by stage 2** into the result record (next beat `result + 0xDC + 2s`, next duration `result + 0x5C + 4s` at `00386E43`) and committed downstream *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 310; bytes re-read.)* | 10 per tick; beat `status_data +9 × frame base × 30` |
| **effect-slot timers** | stats record `+0x17C + slot*2`, `u16`, eight slots | the byte at `+6` of the status's **authored record** (`0xFF` = never expires) | ~~**stage 3**~~ **computed by stage 3**: it reads `+0x17C` (`00385625`) and writes the decremented value to `result + 0x42 + 2·slot` (`00385645`), committed downstream *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 310; bytes re-read.)* | **one per tick, unconditionally** |

## 4. Preconditions · postconditions · invariants

**Preconditions.** Six gates, all of which must pass, in `00310DB0`'s first ninety instructions, and
**their order is load-bearing** (see I-1):

| | gate | site |
|---|---|---|
| 1 | the unit has a stats block — `cmp qword ptr [unit + 0x698], 0` | `00310DCB`, exiting at `00310DD6` |
| 2 | a global mode is not 5 or 6 | `00310E08`–`00310E0E` |
| 3 | the field permits action | `00310E14` |
| 4–5 | neither the global nor the per-unit eligibility mask is set | — |
| 6 | unit flag bit `0x1000000000` is clear | — |

**Postcondition.** The result record has been built and passed to `003112F0`. **The unit is not
untouched**: between gate 1 and gate 2, and unconditionally once gate 1 passes, the tick recomputes
two of the unit's own fields — `00310DE4` stores `00305E70`'s result into `[unit + 0x24]` and
`00310DEC` stores `002E8100([unit + 8])`'s into `[unit + 0x60]` — and I-1's deadline check may clear a
flag bit. Everything else the unit receives comes through `003112F0`.

### The seven cross-operation invariants

**I-1 — The deadline expiry sits *after gate 1 and before gates 2–6*, so it runs for a unit the rest
of the tick refuses — but not for one without a stats block.** `00310DEF` reads the raw tick counter,
`00310DF4` compares it against `[unit + 0xDD0]`, and on expiry `00310DFC` clears flag bit
`0x40000000`. Gate 1 at `00310DCB` jumps straight to the epilogue at `003112D1`, so **a unit with no
stats block never reaches the deadline check and its timed flag is never cleared.**

> **Corrected 2026-09-21 (FABLE), on SWE2-AUDIT-SEM's finding against commit `60dedcfa0`.** This
> invariant first read *"before any gate … runs whether or not they pass"*, and §10 said *"I-1 has
> already run"* for a stats-less unit. Both were wrong, and wrong in the direction that matters: the
> only gate that precedes the deadline check is the one whose failure makes the expiry never happen.
> **The claim was structural, and I asserted it without reading the twelve instructions between the
> function's first byte and `00310DEF`** — the same "read to the end, and to the start" failure this
> contract's own §4 warns about for stage 2. *Re-reading those instructions for the fix is also what
> turned up the two unit-field writes now in the postcondition, which the original draft's "the unit
> is unchanged" denied.*

*It remains a cross-operation statement, and a sharper one than the draft claimed: the expiry is
sequenced between gate 1 and gate 2, so its precondition is a strict subset of the tick body's.*

**I-2 — All five stages run, in that order, for every eligible unit, every tick.** There is no
per-status dispatch table and no "does this unit have poison" short-circuit at the builder level; the
stages themselves decide. The order is fixed in the 83 bytes of `00385DF0` and the last stage is
entered by `jmp`, so **stage 5 cannot be followed by anything**.

**I-3 — Stage 1 initialises the whole record.** ~~`003848E0` touches
`+0x2C`, `+0x3E`, `+0x42` and `+0x13C` and nothing else.~~ *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 310; bytes re-read.)* `003848E0` zeroes all 320 bytes `+0x08`–`+0x147`
through `memset` (`003848EF`–`003848F5`). That write is invisible to a displacement sweep, which is how the old sentence
arose. It then plants `−1` sentinels: `+0x30`, `+0x38`, `+0x3C`, `+0x3E`, `+0x42`–`+0x50`, `+0x11C`–`+0x124`, the 32 dwords
from `+0x5C` and the 32 words from `+0xDC`, plus `+0x130` and `+0x138`. It sets `+0x2C` bit 0. *An implementation that skipped stage 1 for
a unit with no statuses would hand `003112F0` an uninitialised expiry list.*

**I-4 — The two timer families are disjoint, and each has exactly one ~~advancer~~ computing stage.** Stage 3 is the only
body in the pipeline that ~~touches~~ **reads** `+0x17C`; stage 2 is the only one that reaches `+0xBC` / `+0x13C`. *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 310; bytes re-read.)*
**No stage writes the stats block.** Each stage writes the next values into the result record, and the sink commits
them downstream.
- *Latent defect, measured by OPUS:* stage 3's expiry list at `+0x3E` has **no bound**. Its write index increments per
  expiry (`0038563C`–`00385640`). A fifth simultaneous effect-slot expiry therefore lands on `+0x42`, slot 0's new
  value (measured 6 instead of 0).
Stage 2 reaches its pair through a computed base (`00386CA9` forms `rcx = target − record + 0x60`;
`00386C90` forms `r14 = target + 0xBC + 4s`), so **no instruction in it carries the displacement**, and
a scan looking for one will report a clean, wrong zero. *This invariant is the reason the periodic
page carries a published correction, and it is why it belongs in a contract.*

**I-5 — The result record is the only channel between the stages.** No stage calls another; they
communicate solely by accumulating into `+0x24` and setting bits in `+0x2C` / `+0x140`. Three stages
add to one accumulator, and the sum does not depend on the order in which they do — *but the
generator's stream position does*, because stage 2 draws (§9) and stages 4 and 5 do not. **An
implementation may not reorder the stages even though the arithmetic would survive it.**

**I-6 — Expiry detects; it never removes.** Stage 3 appends the expired id to `+0x3E` and writes the
zeroed timer to `+0x42 + slot*2`; removal is `003112F0`'s. **This is why a status wearing off and a
status being cured are indistinguishable downstream** — both arrive as the same record through the
same function.

**I-7 — One global word sets every rate in the subsystem.** `01DFE0B4`, the `FrameLimit` **frame
base** (1 at 30 fps, 2 at 60), scales stage 4's drain interval (`[01DFE0B4] × 30 / 3` = ten ticks at
30 fps, twenty at 60 — *a third of a second either way*), stage 2's durations and beats, and stage 5's
once-a-second ramp. **There is no per-stage rate tunable.** *A reimplementation that hard-codes any
of the three independently will desynchronise them at one frame rate and not the other.*

## 5. State

**Owned by the pass:** the `0x148` result record, which lives on `00310DB0`'s stack and does not
outlive the call.

**Read and not written:** the unit's two status words (`+0x3C` and `+0x64` on the stats record), the
stats record's max MP `+0x28`, max HP `+0x24` and current HP `+0x48`, the perception candidate cache
(`+0xBC4` count, `+0xBC8` entries of 16 bytes), and the authored status records.

**Written outside the record:** `[unit + 0x24]` and `[unit + 0x60]`, recomputed at `00310DE4` and
`00310DEC` once gate 1 passes and before gate 2 is tested; `[unit]`'s flag bit `0x40000000` under
I-1; and stage 5's per-unit tick counter in the 64-byte record selected from `0208D494` / `0208DE94`
(incremented at `00386A27`, zeroed by any failed gate at `00386A2C`).

> **A hazard this subsystem's own bodies contain, stated because an implementer will meet it.**
> `+0x24` appears on **two different structures** inside one function: `[rbx+0x24]` and `[r13+0x24]`
> are the result accumulator, `[rsi+0x24]` and `[rdi+0x24]` are the stats record's max HP. They are
> told apart only by which register is live.

## 6. Relationships

| | |
|---|---|
| **Upstream** | the battle frame, which calls `00310DB0` per unit |
| **Downstream** | `003112F0`, shared with every damage source in the game |
| **Sibling** | [`CONTRACT-status-write.md`](CONTRACT-status-write.md) — *application*; this contract is *maintenance*. The two meet only at `003112F0` |
| **Shared predicate** | `0030B9B0` / `0030B8E0` are one 110-byte shape over the two halves of a packed 16-bit-pair eligibility mask; the tick tests the **low** half directly |

## 7. State transitions

Per tick, per eligible unit: *gate 1 → recompute `[unit+0x24]` and `[unit+0x60]` → deadline check
(I-1) → gates 2–6 → zero the record → stage 1..5 → apply*.
A status transitions `present → expired` only by its timer reaching zero in stage 3 (effect-slot) or
its duration running out in stage 2 (status-word), and `expired → absent` only inside `003112F0`.

## 8. Script · resource · event interactions

Three authored inputs, none of them written here: `status_data.bin` (`+8` duration factor, `+9` beat
factor, `+6` effect-timer slot index, `0xFF` meaning none), the effect table at `02EBF040` that keys
stage 3's eight slots, and the forty 64-byte records at `0208D494` (with `0208DE94` for the
owner-indexed case) whose first word is stage 5's per-unit counter.

## 9. Determinism

**Deterministic given the raw tick counter and the frame base, with exactly one exception, and the
exception is Regen.**

Stage 2 draws the shared **MT19937** generator at `00386D27`, in one arm and one arm only — the one
reached when the status id under consideration is `0x19`, which
[the status table](the-thirty-two-statuses.md) names **Regen**:

```asm
00386D17  cmp   edi, 0x19                    ; the status id
00386D1A  jne   00386e48
00386D20  or    dword ptr [rbx + 0x2c], 0x100
00386D27  call  RNG_MT19937_NextU32_Thunk    ; 00379CD0 -> 00863BF0
00386D2C  movzx ecx, byte ptr [rsi + 0x1c2]
00386D35  div   ecx
00386D37  lea   eax, [rdx + 1]               ; (rand mod byte[stats+0x1C2]) + 1
00386D3A  add   dword ptr [rbx + 0x24], eax  ; ADDED, not subtracted
00386D3D  or    dword ptr [rbx + 0x2c], 0x400
```

**So Regen's per-beat heal is a random 1..`byte[stats + 0x1C2]`**, and it is the only quantity in the
whole subsystem that is not a fixed function of the unit's stats and the clock. The `add` is the
point: every other accumulator write in this pipeline is a loss stored negative, and this one is a
gain.

*Sweeping all five stage bodies for a generator call returns exactly this one site* — stages 1, 3, 4
and 5 draw nothing, so **Poison, Sap, the MP drain and the out-of-combat credit are all exact.**

> **This subsystem is therefore an unlisted consumer of the gameplay generator**, which matters to
> S-46's routing question rather than to this contract. Routed, not resolved here.

Stage 4 fires only when the tick counter is an exact multiple of the interval, so the beat's phase is
global, not per unit — **two units gain and lose MP on the same frame.**

## 10. Failure paths and edge conditions

- A unit with **no stats block** fails gate 1 at `00310DCB` and jumps to the epilogue at `003112D1`:
  the pass does nothing **and neither does I-1**, so its `0x40000000` flag stays set however long the
  deadline is past. *This is the one case where the subsystem leaves stale state behind, and it is
  reachable only for a unit the rest of the tick has no work for.*
- A status whose authored slot byte is `0xFF` **never expires** through stage 3.
- A timer already `<= 0` is skipped, not decremented past zero.
- Stage 4's drain source below 50 takes a **fallback** written from a different register rather than a
  drain rounding to zero.
- Stage 5 refuses outright on Sleep or Disease, on any perceived foe, and when HP is already at target.
- `byte[stats + 0x1C2]` is a **divisor** in §9's Regen arm with no guard ahead of it in that arm; what
  keeps it non-zero is not established here and is listed in §14.

## 11. Observable behaviour

~~Poison and Sap tick on a beat a third of a second wide at either frame rate~~ **Poison, Sap and Regen each tick on their own
beat, `status_data +9` / 10 seconds at either frame rate: Poison every 12 s, Sap every 0.1 s, Regen every 1.5 s.** The third of a
second is the stage-4 drain's interval, not theirs. *(Corrected 2026-09-29, FABLE, Claude Opus 5.5;
`_index/candidates/pkg-gp-status-poison/beat.py` S D M. The seconds rest on the tick running once per unit per frame.)* Poison
and Sap hurt for an exact amount; **Regen, alone among them, heals a different amount every beat**; ~~MP creeps back at max
MP / 50 per beat~~ **on a field whose word `022C314C` has bit 2, MP drains by max MP / 50 per beat (at least 1)**; on one with
bit 1, HP drains by 1 % of max HP per beat *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 310; bytes re-read.)*. Stage 4 (`00385CA0`, gated by bits 1 and 2 of the active field's word) stores
`+0x2A = maxMP / −50` (`00385DBC`–`00385DCD`) and `+0x24 = maxHP / −100` (`00385D51`–`00385D62`). The sink adds both:
`00311673` passes `+0x2A` to `BattleStats_ModifyPrimaryResource`, which adds the delta to the current MP,
and `00311620` passes `+0x24` to the HP write. The positive heal of stage 5 (`00386A12`–`00386A23`) is the control; a disengaged enemy out of anyone's sight heals 1 %, then 2 %, then 5 % of its max HP
per second as its counter climbs; and a status expiring looks exactly like one being dispelled.

## 12. Reproduction formula

Run `00385DF0`'s five stages in order against a zeroed `0x148` record and a stats record with known
status words and timers; assert the §3 ownership matrix holds — that ~~stage 3 alone moved `+0x17C`~~ stage 3 alone computed the next `+0x17C` values into `+0x42` *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 310; bytes re-read.)*,
that `+0x24` is the sum of stages 2, 4 and 5, and that no stage wrote the unit.

## 13. Runtime validation

~~**None.** No experiment in `_experiments/` executes any of these five bodies. S-27's runtime cell
reads **NOT MET** and this contract does not change that; the gap is execution, and it is ASTRA's and
SWE2-ORACLE's, not this document's.~~ **Native replay, not live** *(corrected 2026-09-29, FABLE, Claude Opus 5.5;
`PKG-GP-STATUS-POISON` Q5)*:
- OPUS's builder replay executes the five stages as shipped code: `_index/candidates/s27-opus-replay-periodic-builder/`,
  6/6, every write attributed.
- The tick-entry replay runs the whole per-unit tick with no application stub: gates, deadline, builder and sink.
  `_index/candidates/s27-opus-replay-periodic-tick-entry/`, 4/4.

S-27's runtime cell reads MET. **Not executed:** stage 2's Poison, Sap and expiry arms, since the replays drove Regen
only. That replay is requested as FABLE-REQ-OPUS-POISON-ARM-REPLAY. No live observation exists. *Stated rather than left blank so that a reader does not take a
CONTRACT READY header as evidence of execution.*

## 14. Unresolved

- The other 62 bytes of stage 5's 64-byte records.
- What values above 1 `0030AB40` returns — this caller reduces it to `> 1`, which constrains `Z-13`
  without answering it.
- Whether the `+0x2C` and `+0x140` flag bits are read anywhere but `003112F0`.
- What `byte[stats + 0x1C2]` is — it bounds Regen's random heal and divides without a guard in that
  arm. Named here as a field, not as a meaning.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| The builder is 83 bytes, five calls in fixed order, last a tail call | its whole body disassembled; targets resolved and matched against the five stage names | 1 |
| The per-stage field ownership in §3 | every one of the five bodies swept for each displacement, **with stage 3's `+0x17C` as a positive control** — a run reporting zero everywhere would be measuring nothing | 1 |
| The record is `0x148` bytes and stack-local | `mov r8d, 0x148` at `00310F6C` into the `memset` at `00310F7A`, on the tick's own frame | 1 |
| Stage 2 reaches its timers through a computed base | `00386CA9` and `00386C90` form the bases; no displacement appears in the instruction stream | 1 |
| `01DFE0B4` is the `FrameLimit` frame base | [the boot page](../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md) and `EXP-001`; *this contract's author mis-named this cell once on 2026-09-21 and the correction is in the boot contract's §13d* | 1 |
| I-1's position between gate 1 and gate 2, and the two unit-field writes | `00310DB0`'s first twenty-six instructions read in order; gate 1's `je 003112D1` is the epilogue. **Found by SWE2-AUDIT-SEM against commit `60dedcfa0`; the second defect surfaced while fixing the first** | 1 |
| Stage 2 draws MT19937 for status `0x19` and no other stage draws at all | the arm disassembled in full; all five bodies swept for a generator call, one site returned. **This contract's own draft asserted the opposite** — "no generator is drawn in any of the five stages" — and the neighbour pre-check surfaced the edge before publication | 1 |
| Status `0x19` is Regen | [the thirty-two statuses](the-thirty-two-statuses.md), row 25 | 1 |
| The remaining mechanism | [the periodic-tick page](Periodic-Tick/what-the-periodic-tick-does.md), read from the shipping bytes 2026-09-03 and corrected 2026-09-12 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on I-1 through I-7: the deadline check **sequenced
between gate 1 and gate 2**, the fixed five-stage order with a tail call, stage 1's initialisation,
the two disjoint timer families with one advancer each, the record as sole channel, detect-not-remove,
and one frame-base word driving every rate. **I-1 is the one to test first** — it is the invariant
this contract got wrong on its first publication, and the failing case is a unit with no stats
block.

## 16a. Crossings into other layers (FABLE, 2026-09-21)

Seven layers are reached by this contract's citations, and **six of the seven through exactly two
addresses** — the tick entry `00310DB0`, which calls broadly, and the shared sink `003112F0`, which
every damage source in the game calls.

- **CombatFormula — SERVICE, and the only one that is a real relationship.** `003112F0` is that
  layer's, and this subsystem exists to hand it a record; the shared eligibility predicates `0030B8E0`
  and `0030B9B0` also have callers there. Stated in §2 and §6; it is the contract's subject, not an
  incidental edge.
- **ActorEntity, CombatAI, Party, Items_Equipment_Shops_License, Audio — MECHANICAL.** Each is
  reached only as a *callee of the tick entry or of the sink*, or as another caller of the two shared
  eligibility predicates. *Their addresses are deliberately not cited here: each is a hub, and citing
  one imports its whole edge set into this contract for a one-line accessor note.* What the sink does
  after it is handed the record — including playing a sound — is below this contract's boundary.
- **Rewards_Progression_Economy — MECHANICAL, and worth one sentence.** Bodies in that layer call the
  **same** `00379CD0` generator thunk this subsystem draws at `00386D27` (§9). That is fan-in on one
  shared generator, which is exactly the routing question S-46 owns; **this contract claims no stream
  relationship between them.**

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names each edge.*

**ActorEntity — CLIENT and SERVICE (7 edges).** `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` calls the tick entry `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0`, and `00310DB0` calls `BattleUnit_FindByCombatantId` `0031B770`; the two helpers whose results the tick stores (section 4) call into that layer: `00305E70` walks the unit table through `BattleUnit_GetSlotCount` `00236850` and `BattleUnit_GetBySlotIndexIfUnitFlag4Set` `00321170`, and `002E8100` resolves the actor through `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0` before reading its presentation event id; `0030AB40` calls `ActorRuntime_GetClassNibble` `00263C20`; `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860` calls `ActorWork_GetBattleUnitRaw` `00263E30`. The unit's per-frame lifecycle is what runs the tick, and the tick reads units and actors only through that layer's accessors.

**Audio — SERVICE, OUT-OF-SCOPE (2 edges).** The shared sink `BattleFormula_ApplyTargetResult` `003112F0` calls the Audio-owned bodies `002DF220` and `003A1180`. Section 16a already places what the sink does after it takes the record, sound included, below this contract's boundary; what those two bodies play is not read here.

**CombatAI — CLIENT and SERVICE (4 edges).** `AiOrder_EvaluateTargetSelector` `00301AD0` and `BattleTarget_MatchesRelationMode` `0030BD00` call the relationship classifier `0030AB40`, and `00301AD0` calls the eligibility predicate `0030B9B0`; the tick entry `00310DB0` calls `BattleEnmity_UpdatePeriodicDecay` `00321530`. The AI shares the two target predicates this contract cites, and the tick is the caller that decays threat once per maintenance pass.

**CombatAction — CLIENT and SERVICE (23 edges).** `0030AB40` is called by the action layer's eligibility tests `BattleTarget_PassesEligibilityWithRelationContext` `002FFEF0`, `0030B8E0`, `0030B9B0`, `BattleTarget_IsRelationshipClass0Or2` `0030BB10`, `BattleTarget_IsRelationshipClass0Or1` `0030BCB0`, `BattleUnit_CommitAction` `0030F760`, `BattleUnit_IssueCommandByFocusHandlesWithOptionalPartyFanout` `00311B20` and `00312170`; `0030B8E0`, `0030B9B0` and `00310DB0` call `BattleTarget_ComputeGlobalEligibilityMask` `0030B770` and `BattleTarget_ComputeUnitEligibilityMask` `0030B7F0`; `00310DB0` calls `BattleUnit_TryTriggerNearbyAuthoredFieldAction` `002F8060`; `Battle_ProcessActionTarget` `00307300` and `Battle_ProcessActionTargetEntry` `003191B0` call `0030B9B0`, and `00307300` calls the sink `003112F0`; `002F8060` and `002FA740` call the generator thunk `00379CD0`. The eligibility predicates and the sink are shared with every action, so the tick's periodic result goes through the same target test and the same sink as an attack.

**CombatFormula — SERVICE and CLIENT (75 edges).** The sink `003112F0` calls `BattleStats_SetCurrentHP` `00300520`, `BattleStats_ModifyHPAndProcessLethalState` `00300530`, `BattleStats_ModifySecondaryResource` `00300BC0`, `BattleStats_SetPrimaryResourceAbsolute` `00300C90`, `BattleStats_ModifyPrimaryResource` `00300CE0`, `BattleStats_FindOwningBattleUnit` `0031B860` and `BattleFormula_ApplyResultMetadata` `00385BA0`; the tick entry calls `00300CE0`, `003112F0`, `BattleStats_GetOwningActorHandle` `0031E800`, `BattleStats_GetByMappedBattleSlot` `00320AB0` and `BattleFormula_ResolveTargetResult` `00385F60`; `BattleFormula_InitializeResultRecord` `003848E0` is called by `BattleFormula_EvaluateTargetPreview` `00385680`, `00385F60` and the three status builders `00386A50`, `00386A70`, `00386AE0`; `00300530` calls `0030B8E0` and `0030B9B0`; `00386860` calls `0031B860`; and 53 formula rolls call the generator thunk `00379CD0` (among them `BattleFormula_BuildCandidateStatusMask` `003851F0`, `BattleFormula_RollKnockback` `00388440` and `BattleFormula_RollAndStoreComboCount` `00388660`). Section 16a states it: this subsystem builds a result record for that layer's sink, and the 53 roll sites share the one generator the tick draws from at `00386D27`.

**CoreRuntimeScheduling — MECHANICAL (4 edges).** `00310DB0` and `BattleFormula_ApplyGlobalPeriodicDrainModes` `00385CA0` call `GameClock_GetRawTickCounter` `0032A150`; the frame bodies `0022B6E0` and `0022B7E0` call the generator thunk `00379CD0`. The tick reads the raw game clock, and two frame bodies are further callers of the same generator (the fan-in S-46 owns).

**Gameplay — CLIENT and SERVICE (4 edges).** The engagement predicates `BattleUnit_HasRelationshipClass2PlusInTrackedActorList` `0030B050` and `0030C210` and `BattleUnit_HasCurrentFocusEngagementEvidence` `0030BB30` call `0030AB40`; `00310DB0` calls `BattleEncodedId_IsValidForClass` `00322C50`. These are the domain-filed engagement tests sharing the relationship classifier, and the tick's id-validity check.

**Items_Equipment_Shops_License — SERVICE (1 edge).** The sink `003112F0` calls `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` `003008A0`. The sink can change an inventory item for whatever result carries one; this contract's periodic records reach that call only as inputs to the shared sink.

**Party — CLIENT and SERVICE (2 edges).** `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040` calls `002E8100`, and `00310DB0` calls `PartyFocus_IsCurrentPackedActorHandle` `003273B0`. The party-suppression recompute reads the same presentation-event id the tick stores, and the tick asks whether the unit is the player's focus.

**RNG_Random_Selection — SERVICE, DEPENDENCY (3 edges).** `BattleFormula_AdvanceStatusTimersAndBuildResult` `00386C70` calls `RNG_MT19937_NextU32_Thunk` `00379CD0`, and `RNG_MT19937_NextU32` `00863BF0` calls `RNG_MT19937_TwistState` `00866B90` and `RNG_MT19937_SeedState` `00866D60`. The tick's one draw (section 9) comes from the shared MT19937 stream, which reseeds and twists inside that layer.

**Rewards_Progression_Economy — SERVICE and CLIENT (8 edges).** `00310DB0` calls `Loot_FindOverlappingPickupIndex` `002FB150`, `Loot_RemoveWorldPickupByIndexWithoutGrant` `00319830` and `Loot_CollectWorldPickupByIndex` `00319A00`; the sink `003112F0` calls `GameState_GetGil` `00253690`, `GameState_SetGil` `00254EE0` and `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650`; the growth rolls `002F9A60` and `002F9B20` call `00379CD0`. The maintenance tick also collects world pickups a unit overlaps, the sink applies gil and level results, and the growth rolls share the generator (fan-in, as section 16a says).

**Script_VM_Native_Bridge — CLIENT (2 edges).** The verb bodies `00354BF0` and `00355140` call `00379CD0`. Script verbs draw from the same generator; that is shared-stream fan-in, not a script route into the tick.

**WorldAreaField — DEPENDENCY and CLIENT (3 edges).** `00310DB0` calls `FieldData_GetActiveFieldRecordBit15` `00377C20`; the weather bodies `0025ABA0` and `0025ACA0` call `00379CD0`. The tick consults the field record's action-permission bit, and the weather roll is another caller of the shared generator.

## 17. Related

- [The periodic tick](Periodic-Tick/what-the-periodic-tick-does.md) — the mechanism this states
- [Where MP comes from](where-mp-comes-from.md)
- [Contract — the status write](CONTRACT-status-write.md) — the operation this subsystem ends in
- [The thirty-two statuses](the-thirty-two-statuses.md)

## Falsification pass 1 — 2026-09-30 (OPUS): every clause tested survives; one wording to narrow

**Attack.** The contract's clauses were turned into checks at their bytes: the sequencer, the record, the gates, I-1, the
postcondition, I-3, I-4, §9's single draw, I-7, stage 5's counter and §11's drain arms. The replays in §13 are carried,
not re-run. Script: `Tools/analysis-kit/gfz-scripts/falsify_periodic_tick.py`, output `falsify_periodic_tick.out`, image
`73461d08…`, 0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| T1 | §2 the builder is 83 bytes, five calls in order, the last a tail call | **survives**. The extent is 83 B. The calls are `00385E08` → `003848E0`, `00385E13` → `00386C70`, `00385E1E` → `00385570` and `00385E29` → `00385CA0`, then `00385E3E` `jmp` → `00386860`. There is no conditional branch |
| T2 | §3 the record is `0x148` bytes, zeroed, then built and sunk | **survives**. `00310F6C mov r8d, 0x148`, `00310F7A call 00861EC0`, `00310F8B call 00385DF0` and `00310FAC call 003112F0` |
| T3 | §4 gate 1 and its exit | **survives**. `00310DCB cmp qword [rcx + 0x698], 0`; `00310DD6 je 003112D1` |
| T4 | I-1 the deadline between gate 1 and gate 2 | **survives**. `00310DEF call 0032A150` (the raw tick counter), `00310DF4 cmp [rsi + 0xdd0], eax`, `00310DFA jae` and `00310DFC and dword [rsi], 0xbfffffff` |
| T5 | §4 the two unit-field writes | **survives**. `00310DDC call 00305E70` then `00310DE4 mov [rsi + 0x24], eax`, and `00310DE7 call 002E8100` then `00310DEC mov [rsi + 0x60], eax` |
| T6 | §2 the entry is 1,338 bytes | **survives** (extent 1,338) |
| T7 | I-3 stage 1 zeroes `+0x08`..`+0x147` | **survives**. `003848EB add rcx, 8`, `003848EF mov r8d, 0x140`, `003848F5 call 00861EC0` with `edx = 0` |
| T8 | I-4 stage 3 reads `+0x17C` and writes `+0x42`; its expiry index has no bound | **survives**. `00385625 movzx ecx, word [r14 + rdx*2 + 0x17c]` and `00385645 mov word [rsi + rdx*2 + 0x42], cx`. The index is `rdi` (`mov byte [rdi + rsi + 0x3e], bl` / `inc rdi`), and no `cmp` on `rdi` against 4, 5 or 8 exists in the body |
| T9 | §9 one generator draw, for status `0x19` | **survives**. `00386D17 cmp edi, 0x19`, `00386D27 call 00379CD0` and `00386D3A add [rbx + 0x24], eax`. It is the only generator call in the five stage bodies |
| T10 | I-7 the frame base `01DFE0B4` drives stages 2, 4 and 5 | **survives**. Stages 2, 4 and 5 read it; stages 1 and 3 do not |
| T11 | §5 stage 5's counter records and their update | **survives**. The stage references `0208D494` and `0208DE94`; `00386A27 inc word [rbx]`, `00386A2C mov word [rbx], r15w` |
| T12 | §11 the drain arms: MP by max MP / −50, HP by max HP / −100, gated by the field word `022C314C` | **survives**. Each arm is gated by `0031A900` (`test [022C314C], ecx; setne al`). The HP arm's gate passes mask **1** (`00385CCE`), and the MP arm's passes mask **2** (`00385D6A`). The divisions are the compiler's reciprocal multiply: `0xAE147AE1` = −`0x51EB851F`, with `sar 5` (÷ −100) at `00385D51`–`00385D62` into `+0x24`, and `sar 4` (÷ −50) at `00385DBC`–`00385DCD` into `+0x2A` |

**Narrowing (T12).** §11's "bit 2" (MP) and "bit 1" (HP) are the mask values **2** and **1** that `0031A900` tests.
Counting from zero, those are bits 1 and 0. The claim stands; a reader who takes "bit 2" as mask 4 would test the wrong
bit. Tier 1 (static).
