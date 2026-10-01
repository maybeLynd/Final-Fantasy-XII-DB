---
contract: Drive one manager slot's field actors for one frame
category: 04-Actor-Entity
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: the-field-runtime-pass.md
entries: ["0025D9E0", "0025DF00", "00583920", "003590D0", "003588B0", "00358940", "002620E0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 108 addresses cited - 19 data, 31 entry, 58 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-12
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-field-runtime-pass-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — drive one manager slot's field actors for one frame

> **Authored 2026-09-12 by OPUS**, answering the second item of
> `FABLE-REQ-OPUS-CONTRACTS-S26-S15-S03`. The mechanism is FABLE's, on
> [the field runtime pass](the-field-runtime-pass.md), including the correction that the drive
> loop's inner repeat is **dead code**. What this adds is the interface, the state, the exits and
> the failure paths as an implementable unit — with the entry, the drive loop and **both of its
> exits** re-read from the image.
>
> **Two things that re-reading added, and they are in §6 and §10:** the loop's two exits do
> **not** go to the same place, and **at least two different refusals both return `1`**.

## 1. Purpose

Every actor in the field — a townsperson, a door, a cutscene trigger, a party member — carries a
small script, and this is the function that runs them, once per frame, for one manager slot. It is
also the reason a scripted event can start, run several statements and reach a wait **all in the
frame you triggered it**: the actor is driven, asked whether it settled, and driven again.

## 2. Interface

| | |
|---|---|
| entry point | `0025D9E0` `ActorManager_RunFieldRuntimePass`, 1,297 B, 364 instructions, ends `ret` at `0025DEF0`, **no `jmp` leaves the extent** |
| calling convention | Microsoft x64, `ecx` = slot index (sign-extended at `0025D9EC`), `uint32_t` out |
| parameter | the slot index. **Five slots exist**; each owns a `0x288` = 648-byte block based at `02098E10` (`0025D9EF` `lea rdi, [→02098E10]`, `0025D9F6` `imul rbx, r14, 0x288`) |
| return | **not a status.** `1` on every early refusal; otherwise `r12d`, the conjunction the two later folds accumulate. A caller cannot tell "ran and everything settled" from "declined" |
| the middle piece | `0025DF00` `WorldActor_UpdateRuntimeAndScriptExecutionState`, 329 instructions, ends `ret` at `0025E3CB`, also with no `jmp` out. `rcx` = the slot block, `rdx` = the actor record |

## 3. State

| location | width | meaning |
|---|---|---|
| `02098E10 + slot·0x288` | 648 | the slot block; everything below is relative to it |
| `+0x10` | 1 | slot status. **Bit 0 gates the whole pass** (§10); bit 7 is republished each frame |
| `+0x11` bit 0 | — | **a republished copy of `+0x10` bit 7**, rewritten every frame at `0025DA09`–`0025DA17`. The two bytes are not independent and a reader of one alone sees a stale copy of the other |
| `+0x12` | 1 | ~~written `r12b` **only on the settled exit** (§6)~~ *Corrected 2026-09-26 (OPUS), with a regression and consumer check in [`s15-opus-replay-boot-world`](../_index/candidates/s15-opus-replay-boot-world/).* **"Drive the named actor": the bind sets it and exit A clears it.** `ActorManager_BindLoadedDefinition` stores `(word [definition + 0x50] >= 0)` here (`0026CD1A cmp word [r15+0x50], bx` / `0026CD25 setge al` / `0026CD28 mov [rdi+0x12], al`). That word is the driven actor's ordinal, the same one the drive loop reads at `0025DB31`. The settled exit stores `r12b` (`0025DB79`), which is 0 on that path (`0025DB2E mov r12d, edi`, with `edi` zeroed at `0025DA98`), so exit A clears it. Shipped field scripts: `ttl_b01.ebp` carries −1 (so `+0x12 = 0`); `byu_w01.ebp` carries 0 (so `+0x12 = 1`); 430 of the 499 namespace-5 field scripts on disk carry a non-negative ordinal |
| `+0x13` | 1 | tested at `0025DA1A` |
| `+0x17` | 1 | tested against `0x80` and for bit 2 |
| `+0x20` | 4 | the slot's **actor count**, the bound of both fold loops |
| `+0x24`, `+0x38` | 4 each | incremented once per completed pass, at `0025DED5`/`0025DED8` — per-slot frame counters |
| `+0x200` bit 1 | — | cleared when the roster loop has collected all four members |
| `02099D70` | 8 | published each pass: the slot block |
| `02099D78` | 8 | published each pass: the focus actor's registry entry, **and legitimately null** |
| `0209A1F0` | 8×4 | the party roster the four-iteration loop walks |
| `02CA99E8` | 4 | the save-write busy global |

**The actor record's `+0x14` is a status byte with four live bits and a dead nibble** — bit 4 drives
the bound battle unit, bit 5 is read by seven sites and unexplained, bit 6 is **settled**, bit 7 is
battle-unit-eligible. **Bits 0–3 are never written by any instruction in the image**, which is what
makes the inner repeat dead (§6).

## 4. Preconditions · postconditions · invariants

**Preconditions.** The slot index is in range — **nothing checks it**, and `imul` with a large index
addresses past the five blocks. The slot block is static, so there is no pointer to be null.

**Postconditions on a completed pass.** `+0x11` bit 0 equals `+0x10` bit 7; `02099D70` and
`02099D78` are current; every actor of the slot has been driven at least once; `+0x24` and `+0x38`
are one higher.

**Invariants.**

1. **An actor is driven repeatedly within one frame, not once** — the loop exists — **but in the
   shipped build it repeats zero times**, because the repeat is gated on a nibble nothing sets.
2. **There is no iteration cap on the drive loop.** The absence is measured, not assumed: the same
   reading positively identifies the caps on the other three loops (`cmp r15d, 4` and two
   `cmp edi, [rbx+0x20]`).
3. **`02099D78` can be null two different ways** — no party focus, or a packed handle that does not
   resolve — and a reader **cannot tell them apart**.
4. **The pass reports success when it does nothing.** See §10.

## 5. Relationships

**49 distinct callees over 59 call sites.** The ones that shape the contract: `00583920` (the busy
flag, seven bytes over one global), `003590D0` → `003588B0` (the focus handle and its resolver),
`00358940` (record by ordinal), `0025DF00` (the wait resolver, **five call sites**), `002620E0` (the
field-runtime init core — **gated**, §6; *two call sites, corrected 2026-09-26 (OPUS): exit A's `0025DB7D`, and
`0025DC27` on the `+0x12 == 0` branch, §6*), `00261F90` (audio), `003148F0`, `0032FC30` (the deferred
mode request, issued once for slot 0 with index `0xD4` = 212).

**A hook on `0025DF00` is called several times per actor per frame** — once from each loop that names
the actor — and **never** from the drive loop's inner repeat, which is dead.

## 6. The drive loop, and the two exits that are not the same exit

```asm
0025DB35  call 00358940                    ; record by ordinal
0025DB43  call 0025DF00                    ; drive it
0025DB48  movzx ecx, byte [rdi + 0x14]
0025DB4C  test cl, 0x40
0025DB4F  jne  0025DB76                    ; SETTLED   -> exit A
0025DB51  test cl, 0x0F
0025DB54  je   0025DECB                    ; NOTHING PENDING -> exit B
0025DB5A  call 003DB280                    ; (dead: the nibble is never set)
0025DB68  call 0025DF00                    ; (dead) drive it again, same frame
0025DB74  je   0025DB51                    ; (dead) loop
```

| exit | taken when | what it does |
|---|---|---|
| **A** `0025DB76` | the record's `+0x14` bit 6 is **set** | `mov byte [rbx+0x12], r12b` — ~~publishes the running conjunction into the slot block~~ *(corrected 2026-09-26, OPUS: in the drive loop `r12d` was just set from `edi` = 0 at `0025DB2E`, so this CLEARS `+0x12`, ending the drive request the bind raised; executed in `s15-opus-replay-boot-world` X2)* — then **calls `002620E0`**, then falls into the common tail |
| **B** `0025DECB` | bit 6 clear and the low nibble clear | **straight to the common tail.** Neither the `+0x12` publish nor `002620E0` happens |

> **The page reads as though both exits merely stop the loop. They do not.** ~~`002620E0` — the
> field-runtime init core — and the `+0x12` publish run **only when the driven actor came back
> settled**.~~ **Within the drive loop**, `002620E0` (the field-runtime init core) and the `+0x12`
> publish run only when the driven actor came back settled. A reimplementation that writes the loop
> as one `break` runs the init core on a frame where the original does not, and that is the kind of
> divergence no per-function differential would catch because the function is the same on both sides.
>
> And because the nibble is dead, this is not a three-way choice: ~~**every pass takes exactly one of
> exit A or exit B**~~ **every pass that enters the drive loop takes exactly one of exit A or exit B**,
> decided by one bit of one byte.
>
> **Corrected 2026-09-26 (OPUS, owner), measured in
> [`candidates/s15-opus-replay-field-pass-stub-free/arms.py`](../_index/candidates/s15-opus-replay-field-pass-stub-free/arms.py)
> (T1, F1, F2).** The two struck sentences held only for the drive loop.
> - **The drive loop is entered only when the slot's `+0x12` is non-zero.** A pass with `+0x12 == 0` takes
>   `0025DB25 cmp byte [rbx+0x12], dil` / `0025DB29 je 0025DB87`, skips the loop, and takes neither exit.
> - **That branch calls the audio routine and the init core itself.** It calls `00261F90` (audio, `0025DB8E`).
>   Then, when `+0x17 < 0x80` and `+0x10` bit 5 is clear (`0025DC10`–`0025DC1E`), it calls the init core from a
>   **second call site, `0025DC27`**.
> - **Executed:** a slot with `+0x10 = 0x81` and `+0x12 = 0` runs `00261F90`, then `002620E0`, returning to
>   `0025DC2C`. The resolver then drives all five records.
> - So the init core runs on frames where no actor settled at all, whenever the slot has nothing pending in
>   `+0x12`.

**The common tail** (`0025DECB`): if `r14d` is zero, call `0025B600`; increment `+0x24` and `+0x38`;
return `r12d`.

## 7. Four loops, three shapes

| loop | bound | what it accumulates |
|---|---|---|
| the drive loop | **none** | — |
| `0025DC61`–`0025DCCF` | `cmp r15d, 4`, `rol ebp, 1` | the **party roster** at `0209A1F0`: drives each occupied member, folds its settled bit, collects members whose `+0x10` is zero; at `r14d == 0xF` clears the slot's `+0x200` bit 1 and, on slot 0, runs `00233AA0` |
| `0025DD10`–`0025DD67` | `cmp edi, [rbx+0x20]` | `r12d &= record[+0x14]` over every actor |
| `0025DE80`–`0025DEB1` | `cmp edi, [rbx+0x20]` | `r12d &= record[+0x14] >> 6` — **"is bit 6 set on every actor"**, a whole-field settled test computed by conjunction rather than by a counter |

## 8. Script · resource · event interactions

The pass drives authored actor scripts through `0025DF00` and `0025E4C0`. **The wait kinds do
not share the polarity previously stated here.** Kinds3/5/6/7 hold while their entry/channel
predicate is active. Kind4 holds while its matching detached notification is ABSENT. On completion,
the driver sets kind1 and retries in the same invocation under the current service gates.

`0025E127` is the blocked/no-interpreter exit; `0025E0BE` is the interpreter arm. The request's
+0x14 is distinct from the actor's +0x14. Found kind4 notifications are removed in the caller,
then execution can continue without an imposed extra frame. List cursors are monotonic within
these helper calls and do not recheck entries already passed.

[SECTION-12](../_experiments/evidence/continuation-section12-actor-request-waits/REVIEW.md) executes
this behavior with original arming, list and entry operations and the original interpreter.
It does not execute the whole outer field pass or validate live timing.

Resource side: slot 0 issues `WorldSimulation_ProcessDeferredModeRequest(0, 0xD4)` **once**, latching
`+0x10` bit 3 so it is not repeated, when `00377DB0()` is non-zero and `+0x10` bit 4 is clear.

## 9. Determinism

No RNG. **Ordering is the whole contract**: the pass is per-slot and per-frame, the roster loop
precedes the two folds, and the folds read a byte the drive loop may have changed. Single-threaded.

## 10. Failure paths and edge conditions

| # | condition | result |
|---:|---|---|
| 1 | `SaveWrite_GetBusyFlag()` non-zero | **the entire pass does nothing and returns `1`** (`0025DA07` → `0025DA3F`) |
| 2 | the slot block's `+0x10` bit 0 is **clear** | **the same: nothing, and return `1`** (`0025DA4D test byte [rbx+0x10], 1` / `je 0025DA3F`) |
| 3 | no party focus, or a handle that does not resolve | `02099D78` is published **null**, and the two causes are indistinguishable |
| 4 | the slot index is out of range | **unchecked.** `imul rbx, r14, 0x288` addresses past the five blocks |
| 5 | an actor never settles | the drive loop cannot spin — the repeat is dead — so the pass ends and the actor is simply not settled this frame |

> **Rows 1 and 2 are the contract's sharpest edge.** *Two different refusals return the same value a
> successful pass can return*, and `1` is also a perfectly ordinary conjunction result. **The return
> value carries no information about whether the pass ran.** A caller that needs to know must read
> `+0x24` or `+0x38` before and after — they increment only on the completed path.
>
> Row 2 is **not** on the page, which describes only the save-busy refusal.

## 11. Observable behaviour

In memory: `+0x24` and `+0x38` advancing once per completed pass; `02099D70` / `02099D78`; `+0x11`
bit 0 tracking `+0x10` bit 7; each actor record's `+0x14` bit 6. In play: a scripted event running
several statements in the frame it was triggered; everything in the field standing still while a
save is written.

## 12. Reproduction formula

```c
uint32_t ActorManager_RunFieldRuntimePass(int slot)
{
    uint8_t *b = (uint8_t *)0x02098E10 + (int64_t)slot * 0x288;   /* unchecked */
    if (SaveWrite_GetBusyFlag())            return 1;             /* refusal 1 */
    b[0x11] = (b[0x11] & 0xFE) | (b[0x10] >> 7);                  /* republish, every frame */
    ...
    if (!(b[0x10] & 1))                     return 1;             /* refusal 2 */

    *(void **)0x02099D70 = b;
    *(void **)0x02099D78 = ActorHandle_ResolveRegistryEntryByPackedId(
                               PartyFocus_GetCurrentPackedActorHandle());   /* may be null */

    rec = ActorManager_GetRecordByOrdinal(b, *(uint16_t *)(actor + 0x50));
    WorldActor_UpdateRuntimeAndScriptExecutionState(b, rec);
    if (rec[0x14] & 0x40) {                 /* exit A */
        b[0x12] = (uint8_t)conj;
        call_002620E0(b);
    }                                       /* exit B falls straight to the tail */
    /* ... the roster loop and the two folds, both bounded by *(uint32_t *)(b + 0x20) ... */
    if (r14 == 0) call_0025B600();
    ++*(uint32_t *)(b + 0x24);
    ++*(uint32_t *)(b + 0x38);
    return conj;
}
```

## 13. Runtime validation

**Evidence class: isolated original-code, for the ENTRY GATE only — the first 120 bytes of a
1,297-byte pass. There is no live evidence and the pass itself is still unexecuted.**

| what | pilot | cases | mismatches |
|---|---|---:|---:|
| the entry gate and republish, `0025D9E0`–`0025DA5A`, **and all six callees it can reach** | [`diff_field_gate.py`](../../../Reconstruction/Tests/Differential/diff_field_gate.py) — the **42nd** | 54 | **0** |
| the pass from `0025DA5C` on — the drive loop, the publish, the 49 callees | — | — | **not executed** |

### It needed no scripted anything, and this section had said otherwise

**What was written here was "over a planted slot block and a SCRIPTED BUSY FLAG."** That was too
pessimistic. Every callee the gate can reach is a leaf or reaches only leaves, so **all six run**:

| callee | size | what it does |
|---|---:|---|
| `00583920` `SaveWrite_GetBusyFlag` | 7 B | `mov eax, [02CA99E8]` |
| `0032F6E0` | 15 B | a **sign-extended** byte from the table at `022C6D20`, indexed by the slot |
| `003603C0` | 8 B | a **sign-extended** byte from `022CB726` |
| `0026A5F0` | 74 B | ORs `1 << (slot & 31)` into `02099ABC` — **and RECURSES for slot 0** |
| `002E15D0` | 28 B | clears `0215F1A0` `+0x00`, `+0x01`, `+0x04`, `+0x08` |
| `002E1690` | 8 B | sets `0215F1A1` — **the byte `002E15D0` has just cleared** |

**Three of those six are named nowhere else in this contract.** They were inside its "49 distinct
callees over 59 call sites" and nothing said what they did.

### What the trace measured

**The suite compares the CALL TRACE as well as the bytes** — which callee ran, in what order, with
what argument — because a gate that calls the right things in the wrong order leaves identical bytes
behind.

- **`0026A5F0` RECURSES, and only for slot 0.** One call on slot 0 produces **fourteen** trace
  entries: it drives slots 1, 2 and 3 to completion *before* doing its own work, so the mark ends
  with bits 0–3 set and the `002E15D0`/`002E1690` pair runs **four times**. Any other slot produces
  three entries and one bit. **A static reading of a recursive function does not give you the
  ordering; running it does.**
- **The shift count is masked.** Slot 32 sets bit 0 and slot 33 sets bit 1 — not bit 32, not bit 33,
  and not nothing. Driven against a zeroed mark so each bit is visible on its own.
- **Four of the six callees take NO ARGUMENT**, and the trace is how that was established rather
  than assumed. At `003603C0`'s call site the register holds `022C6D20` — **the table base
  `0032F6E0` returned in `rcx`** — because a volatile register survives a call only by accident. A
  reconstruction that "passed the slot" to it would be inventing an ABI.
- **The republish is a copy, not an accumulation.** All sixteen combinations of `+0x10` bit 7 and
  `+0x11` bits 0 and 3 were driven: `+0x11` bit 0 afterwards **equals** `+0x10` bit 7 in every one,
  `01 → 00` included, and bit 3 is preserved throughout. Only the `1 → 0` cases can tell a copy from
  a sticky OR, and half a case set would have contained none of them.
- **The index is sign-extended and unchecked, and slot 5 is worse than out of range**: its block
  starts at ~~`02099A88`~~ **`02099AB8`** (*corrected 2026-09-12, §15a — a digit transposition;
  `02098E10 + 5 × 0x288 = 02099AB8`*) and therefore **contains `02099ABC`, the very global the
  mark writes**, at offset **`+0x4`** rather than `+0x34`. The fixture plants slots `-1` through `5`
  as one region for exactly that reason. **Slot 4's block ends at `02099AB7`, immediately before
  the global**, so the mark lies outside every valid slot and just inside the first invalid one.

**Mutation campaign: 82 points — 67 KILLED, 14 SURVIVED,
1 EQUIVALENT, 0 TIMEOUT, 0 INVALID. Status `FAIL`.**

### Every non-kill, adjudicated

- **It found a REAL GAP — a kind D — and it is worth naming.** `FG_SLOTBYTE_VA` could be moved one
  byte and nothing noticed, because the fixture had filled `0032F6E0`'s whole table with **one
  repeated value**. The table's base address was pinned by nothing at all. Every index now carries a
  distinct byte and that mutant dies.
- **1 is kind A**, and it says something about the original: `002E15D0`'s clear of `0215F1A1` is
  **dead whenever `0026A5F0` is the caller**, because the tail jump to `002E1690` sets that same
  byte to 1 immediately afterwards.
- **13 are kind B, the fixture's address-space model and its capacities**, which the six
  originals have no counterpart for — they read a flat process. Most are unkillable by construction:
  any case that makes the model refuse is already a mismatch.
- **1 EQUIVALENT** compiled to byte-identical code.
- **Three survivors died once cases put an access on a region edge** — a gate-byte region ending on
  the byte `003603C0` reads, and a latch described as three adjacent pieces cut after two of
  `002E15D0`'s stores. **A bound no case touches is a bound nothing checks**, the third pilot in a
  row to pay for that.
- **Two mutants recursed without end** and took the process down rather than showing a difference,
  so they scored `INVALID`. The mark's recursion is now bounded by the same `FG_MAX_CALLS` that
  bounds the trace — which a faithful run can never reach, its maximum being fourteen — and both are
  kills. **The harness also trusted the printed call count past that bound and walked off the end of
  its own trace; it now parses to the delimiter and compares the count.**

**No kind D remains.**

Receipts: `Database/Tools/work/OPUS/litsuffix/field_gate`, `field_gate2`, `field_gate3` and
`field_gate4` (ignored path), and the counts row in
[`MUTATION-CAMPAIGNS.md`](../../../Reconstruction/MUTATION-CAMPAIGNS.md).

**The live half, queued with the state it needs, and none of it performed:** read `+0x24` on slot 0
across two frames and confirm it advances once per frame; write a non-zero `02CA99E8` and confirm it
stops; read `02099D78` on a frame with no party focus and confirm null.


### The whole path from a frame to a verb, counted 2026-09-12

**Five of its six links have exactly one caller.** Counted over `edges.tsv`, not asserted:

| # | function | subsystem | calling functions | call sites |
|--:|---|---|---:|---:|
| 1 | `0022B8C0` `MainLoop_UpdateAndRenderFrame` | CoreRuntimeScheduling | — | — |
| 2 | `00314020` `World_UpdateSimulationTick` | WorldAreaField | 3 | 3 |
| 3 | `0025D9E0` `ActorManager_RunFieldRuntimePass` | ActorEntity | **1** | 2 |
| 4 | `0025DF00` `WorldActor_UpdateRuntimeAndScriptExecutionState` | Movement | **1** | 5 |
| 5 | `0025E4C0` `WorldActorScriptVM_InterpretBytecode` | Script VM bridge | **1** | 1 |
| 6 | `002621D0` `VMNativeCommand_ExecuteLifecycle` | Script VM bridge | **1** | **3** |

**The two columns are different questions and the second one caught the first.** `edges.tsv` has one
row per caller/callee *pair*, so a count taken from it is a count of **functions**; the image has
`0025DF00` reached from **five sites** inside that one function and `002621D0` from **three**. A
table that printed only the left column would have said "one caller" about a function entered from
five places.

> **And three is not a coincidence.** The verb-dispatch contract's §2.1 says `0x5E` has no
> dispatcher call of its own — it jumps into `0x5D`'s body at `00261ABF` — *"which is why a caller
> census over direct calls finds three sites and not four"*. **The mechanical site count agrees with
> a claim the document made before anyone counted it.** All five links are now in
> `check_caller_claims.py`, so the next run re-checks them rather than trusting this table.

**Every authored script in FFXII reaches the engine down this one wire.** A cutscene moving a
character, a trigger opening a door, a battle script setting a floor — each is a frame arriving at
`00314020`, a slot passing the gate at `0025D9E0`, an actor being driven by `0025DF00`, an opcode
decoded by `0025E4C0`, and a lifecycle run by `002621D0`.

> **Two ends of it are executed and the middle is not.** Link 3 is the 42nd pilot and the three
> accessors under link 6 are the 40th. **Historically, links 4 and 5 — the 1,228-byte drive and the interpreter —
> had not been run at the time of this paragraph**, and a chain whose ends are proved is not a proved chain.

> **Found by the cross-reference audit, not by reading.** It reported this as one unaccounted
> Movement edge on the verb-dispatch contract. Neither document had said the other was on the same
> wire, and the single-caller counts are what make the path worth stating at all: there is no second
> route to a verb to be missed.

**Experiment records that name this contract** — found by `OPUS-CONTRACT-RUNTIME-AUDIT`, 2026-09-13. Each names this
contract in its own `contract:` frontmatter while this section did not cite it back.

- [`EXP-048`](../_experiments/EXP-048-handle-discriminator-advance.md) — **method B**, isolated original-code execution.
- [`EXP-049`](../_experiments/EXP-049-handle-renewal-focus.md) — **method B**, isolated original-code execution.

**None of these is a live run**, so none of them changes the evidence-class statement at the
top of this section. They are listed because a reader auditing what has been executed against
this contract should not have to find them from the experiment side only.

### 13a. The pass body, the wait resolver and the init core, executed — 2026-09-18 (OPUS, consuming EXP-106)

**Fifty-two bodies from shipped bytes** — 58/58 cases, 46/46 mutants, three processes. §6 and §13
described a static reading of the drive loop; this is what runs.

**THE PASS READS THE SAVE PAYLOAD DIRECTLY, and this contract did not say so.** `gefb` and `gf64`
are not opaque globals:

```
002EF640  lea rax, [02164280] ; ret        the save image's active runtime buffer
002EF2B0  call 002EF640 ; add rax, 0x200   ... + 0x200 = the SAVE PAYLOAD base
```

That is the same pair `CONTRACT-save-image-buffers` and the type store's `SavePayload` row describe
— *"`SaveImage_GetPersistentPayloadBase()` = `SaveImage_GetActiveRuntimeBuffer()` + 0x200"* — and the
mode chain's `d[gefb+0x1054]` therefore reads **payload `+0x1054`**, which the `SavePayload` field
map places inside `persistentFlagPayloadRegion`.

> **Three independent sources agree and none knew about the others:** the type store's route, an
> accessor-aware census of the buffer run the same day (which found buffer `+0x1254` — the same
> byte, 1 read and 1 write, at `005842AB`), and this execution. **A per-frame field pass consults
> the persistent save flags**, which is a dependency neither contract had recorded.

**The two exits are confirmed and now distinguished by what they do**, which §6 named but could not
measure: exit A (`cl & 0x40`) clears `+0x12` and initialises the core; exit B (`!(cl & 0xF)`) runs
the epilogue and returns `r12d`. They are not two ways out of the same state.

Other semantics adopted, each pinned by a mutant to a branch or immediate: the slot block is
`[0x2098E10] + slot*0x288`, the same `0x288` stride the family table at `263FF0` indexes;
`G_DFA`/`G_DFB` **alias slot 1's own block** at `+0x10`/`+0x13` rather than being independent
globals; the deferred arm runs `dreq(1,0xD4)` → `b10 |= 8` → epilogue **before** the
`(dfa&1)|dfb` early exit, so the order is not the one a reader infers from the test's position;
kind dispatch is `cmp eax, 7 / ja`, with kinds 0–8 all armed; the interpreter arm **always** funnels
to settle via `+0x14 = 1`; and the init core re-arms only when `b10 & 4` is clear, with the `ice`
return compared **signed** (`jle`).

> **The boundary.** Fifty-two bodies is the pass, the resolver and the core — not the subsystems the
> pass drives into, and not a frame. §11's observation is unchanged.

## 14. Unresolved

*Renumbered 2026-09-14 (FABLE, `OPUS-REQ-FABLE-QUESTION-ID-INTEGRITY`): these ids were `FP-1`…`FP-4`, which the question register already uses for different questions (the result-record field questions). The register keeps its ids; this list moved, and the rows are registered under the new ids.*

1. **`FRP-1`** — what bit 5 of the actor record's `+0x14` means. Seven readers, no reading.
   ***ANSWERED 2026-09-18 (FABLE).** Bit 5 of `+0x14` is the actor entry's script *enable* flag. Its only writer in the image is the unlisted 24-byte setter `00269E00` (`and byte [rcx+0x14], 0xDF`, then `(dl & 1) << 5` or-ed back), reached by the thunks of script verbs `001E enable` (`00353630`, `edx = 1`) and `001F disable` (`00353A50`, `edx = 0`); on disable the setter tail-jumps `0025B500`, the entry removal that releases system-stop id 18. All seven readers gate work on an entry: the per-kind pass `0025C170` builds an entry through `0025C830` only when bit 5 and `+0x08` bit 0 (the line/rect enable) are both set (`0025C1C0`) and runs `0025C230` over the second ordinal range only when bit 5 is set (`0025C1FB`); the line pass `0025B250` requires bit 5, `+0x08` bit 0 and `+0x1C` bit 6 (`0025B29A`); `0025B820` tests it twice (`0025B919` before `002EA6A0`, `0025BA2D`); `002675C0` requires it, then kind 3, once `02099DB4` is zero (`0026760E`); and `003DF6F0` requires it with `+0x08` bit 0 on the entry `003588B0(0)` returns, before `002E9FE0` (`003DF709`). So a disabled entry is skipped by every pass that would build, line-test or step it, and `disable` also drops its build hold. Static: an image-wide sweep of `test` / `and` / `or` on `byte [r+0x14]` with `0x20` / `0xDF` (one writer, seven readers) and the verb dispatch table.*
2. ~~**`FRP-2`** — which map row 636 of resource namespace 5 names, for the slot-0 `0xD4` request. The
   path tables are built at boot, so the stem is not in the image.~~
   **ANSWERED 2026-09-22 (FABLE): it names NOTHING, and the premise that the stem is not in the
   image is false.** The tables are built at boot **from `lea` constants in `002DF9A0`**, so each
   array is a link-time address with static contents. Ten arrays are installed at namespace 5
   (`0215F028`), one per language; **in all ten, rows 636/637/638 are three NULL pointers** — map
   212's `.ebp`/`.mot`/`.fpk` triple is unauthored. Not an out-of-bounds read: the arrays hold at
   least **2,127** non-NULL rows up to map index **1,311**. Control: rows 0/1/2 are `tst_a01.ebp`,
   `.mot`, `.fpk` — one stem, three extensions, which is what proves `row = index × 3`. **With
   `AB-2`, the slot-0 `0xD4` request therefore resolves to a NULL path for all three of the
   triple.**
3. **`FRP-3`** — whether refusal 2 (`+0x10` bit 0 clear) is a disabled slot, an uninitialised one, or
   something else. The bit's writers are not read here. **Executing the gate did not touch this**:
   a fixture can plant the bit either way and watch the gate obey it, which says what the gate does
   and nothing about what the bit means.
   ***ANSWERED 2026-09-19 (SWE2-CONTRACT).** Bit 0 of block `+0x10` is the slot's **live flag** — not
   a disable toggle, and not exactly "uninitialised" either: it reads *not-live*, covering both the
   never-initialised and the already-unloaded cases with no way to tell them apart at the gate. The
   writer census was widened past §13's immediate-write count to every byte-write form: inside the
   58 operand-verified `02098E10` base-takers the only `+0x10` writes are `or …,1` at `0026D305`
   (`ActorSystem_InitializeManagerRuntime`), `and …,0xFE` at `00262DA8` (unload `002628B0`), and
   flag-bit writes on other bits (`or 8` / `or 0x10` / `and 0xDF` / `and 0x7F` + `shl bpl,7` + `or
   bpl` — the ≥`0x80` flag `002659F0` tests — all in the pass itself). The three apparent extra
   candidates dissolve on context: `0025DE6F`'s `or [rbx+0x10], bpl` writes bit 7 only
   (`bpl<<7`); `00265A17`'s and `00268C08`/`00268CB0`'s `inc byte [r+0x10]` increment a counter on
   the *entry* object (`rcx`/`rbx`, whose `+0x15` is the manager index), not the block. Outside the
   base-takers, all 93 callers of the block getter `00263FF0(m)` = `base + m×0x288` were read for
   `+0x10` writes — only `003B7770`/`003B7880`/`003B8090` contain any, and all three write `+0x10` on
   `002E97B0`'s entry result (bit 1), never on the block. The reading side confirms the name: every
   indexed accessor fails closed on the bit — `00264610`, `00263C30`, `00263B50`, `00263C50` and the
   enumerator `003B8090` all `test [block+0x10], 1; je → return 0` — so *live* is the pervasive
   precondition, and refusal 2 means the slot's manager runtime is not up (init not run, or unload
   `002628B0` landed). "Disabled" is excluded by construction: no writer produces a
   live-but-disabled form.*
4. **`FRP-4`** — **what the three newly named callees are for.** `0032F6E0`'s per-slot byte table at
   `022C6D20`, `003603C0`'s single byte at `022CB726`, and the mark word at `02099ABC` with its
   `0215F1A0` latch pair are now described *mechanically* by §13. **Nothing here names their
   purpose**, and the recursion over slots 1–3 for slot 0 is a strong hint about what those slots
   are to each other that this pilot cannot cash.

   > **`FRP-4` consumed — 2026-09-13 (`FABLE-REQ-OPUS-FP4`). FABLE's reading is accepted with one
   > name changed, and the gap FABLE declared is closed statically rather than deferred to a live
   > watch.**
   >
   > FABLE proposes: `02099ABC` is the actor-manager request mask drained by the world tick's
   > every-mode prologue `0025BFB0`; `022C6D20[m]` is the per-manager **deferred-unload** byte set
   > only by `00332190` and turned into a request by this pass when no save is being written; and
   > `0026A5F0`'s recursion for manager 0 means *unloading the area manager also unloads the three
   > event managers*, which matches the stage order `(1, 2, 3)` and requeue order `(1, 2, 3, 0)`.
   > **Nothing in §13 contradicts any of it, and the setter census reproduces independently** —
   > `edges.tsv` gives `00332190` exactly the five callers FABLE names, `00356D40` being
   > `eventdispose_f2` itself rather than a sixth.
   >
   > ### The declared gap: “no clear of `022C6D20` found, and a block memset would escape it”
   >
   > Four independent routes to a clear were tested, **each with its own positive control**,
   > because a zero is a property of the filter until a control says otherwise:
   >
   > | route to a clear | result | positive control |
   > |---|---|---|
   > | a direct RIP-relative store | **none.** In `[022C6D20 − 0x800, +0x20)` the only address-takers are `0032F6E0` (`lea rcx` at `0032F6E3`, then `movsx eax, byte ptr [rax+rcx]`, read-only) and `00332190` (`lea rdx` at `003321B6`, then `mov byte ptr [rbx+rdx], 1`). **One store to this table exists in the whole image and it writes `1`** | the census sees both known address-takers, and sees `0032F430`'s `write` to the neighbour `022C6D1D` |
   > | the neighbour store spilling into the table | **cannot.** `0032F6A6` is `mov byte ptr [rip+0x1F97670], bpl` — **byte-wide**, and `022C6D1D` is a *different* deferred byte, read by `WorldSimulation_ProcessDeferredModeRequest` at `0032FC42` | the same decode shows the width directly |
   > | a pointer to the table held in initialised data | **none.** **0 of 114,962 DIR64 relocations** hold any address in `[022C6D00, 022C6D40)` | the same search finds the stored pointer to `006709D0` in 1 slot, so it can see stored pointers |
   > | a block clear (FABLE's memset worry) | **none spans it.** Decoding every `rep stos` and every 3-argument fill whose destination is a RIP-relative global yields **93 spans image-wide**; **none covers `022C6D20`**. The two nearest end `0x1130` and `0x1230` short | the decoder finds `0032EB10`'s own `lea rdi,[022C59F0]; mov ecx,0x100; rep stosb` — the exact shape FABLE feared, **bounded, in this very neighbourhood** |
   >
   > A fifth route the mechanism in §13 opens by itself — `0032F6E0` **leaks the table base in
   > `rcx`**, so a caller could clear the table with no `lea` of its own — is also empty: none of
   > the getter's call sites writes through `rcx` after the call.
   >
   > **Correction to the first pass of this note:** the nearest `lea`-produced address below the
   > table is `022C5C00`, `0x1120` below, **not `0x8000`+ as written earlier**.
   >
   > ### Why the byte does not need a clear — and what that costs FABLE's name for it
   >
   > Decoding the gate rather than paraphrasing it, `ActorManager_RunFieldRuntimePass(m)` raises
   > the request at `0025DA3A` only when **all four** hold:
   >
   > ```
   > 00583920() == 0                       ; no save being written
   > [block+0x13] != 0  OR  [block+0x10] & 1   ; 0025DA1A / 0025DA20   (bit 0 = live)
   > ([block+0x11] & 8) == 0               ; 0025DA25
   > 0032F6E0(m) != 0                      ; 0025DA2E  -- the byte
   > ```
   >
   > **So the repeat is stopped by the manager block, not by the byte.** Of the 59 functions that
   > take the block base `02098E10`, the immediate byte writes to `+0x10`/`+0x11` are 13, and among
   > them **`+0x10` bit 0 is set only by `ActorSystem_InitializeManagerRuntime` (`0026D305`,
   > `or byte ptr [rbx+0x10], 1`) and cleared only by the unload `002628B0` (`00262DA8`,
   > `and byte ptr [rbx+0x10], 0xFE`)**. Once the unload lands the gate goes false and the still-set
   > byte asks for nothing — no consumption required.
   >
   > **The reload case is covered by the other guard, and by exactly the guard one would want.**
   > `[block+0x11]` bit 3 is set at **two** sites in the whole image, one of them
   > `ActorResource_BeginPrimaryPayloadLoad` at `003303DF`, applied to the block that `00263FF0`
   > (a base-taker) returns; it is cleared by the load-completion family, including
   > `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (`003306AF`) and
   > `ActorResource_OnDefinitionPayloadLoaded` (`0032F9AA`). **While a payload load is in flight the
   > pass cannot tear the manager down**, which is why a mark that is never cleared is survivable
   > at all.
   >
   > **Therefore: accept FABLE's mechanism, reject the word *deferred*.** A deferred request is one
   > that is consumed; this one never is. `022C6D20[m]` reads as a **sticky “this manager has been
   > asked to dispose” mark**, and every one-shot property people would attribute to it lives in
   > `+0x10` bit 0 and `+0x11` bit 3 instead. §13's mechanism is unchanged; only the name is.

   > ### CORRECTION 2026-09-21 (OPUS), on `ASTRA-CONTRA-OPUS-MGRMARK-HAS-CLEAR`: The mark IS cleared, in two places
   >
   > **ASTRA is right and the word *sticky* is withdrawn.** The paragraph above concludes that
   > `022C6D20[m]` is never cleared and that every one-shot property therefore lives in the block
   > bits. The first half is false. Verified here against the image rather than taken on report:
   >
   > `0032F14B` is `mov byte ptr [rdi + r14 + 0x21a6d20], bpl`, inside `0032ED80`. It writes
   > **zero**, and the register roles are fixed by the function's own prologue:
   > `0032ED9A movsxd rdi, ecx` makes **`rdi` the index argument `m`**; `0032EDBB
   > lea r14,[rip-0x20edc2]` makes **`r14` the image base `0x120000`**; and `0032EDC2 xor ebp,ebp`
   > is the **only** write to `rbp` in the whole 1,001-byte body before the store — the next is the
   > restore at `0032F153`. So `bpl` is zero and the store is `byte[0x120000 + 0x21a6d20 + m] = 0`,
   > which is `byte[022C6D20 + m] = 0`. That is this table, at this index, set to zero.
   >
   > **And there is a second clear the contradiction does not name:** `0032F4A2`, the same
   > instruction shape inside `0032F430`.
   >
   > ### Why five routes with five passing controls all said no
   >
   > They are all still true. No RIP-relative store to the table exists; no neighbour spills into
   > it; no DIR64 relocation holds its address; no block fill spans it; no call site writes through
   > the leaked `rcx`. **Every one of those routes assumes that reaching the table requires
   > materialising its ADDRESS somewhere.** The clear never does. It holds the **image base** in
   > `r14` and reaches the table by its **image OFFSET**, `0x21a6d20`, as an instruction
   > displacement. The value `0x022C6D20` appears nowhere in the instruction, in any relocation, or
   > in any `lea`. A census of address-takers cannot see this addressing form, and the controls
   > could not warn, because each control tested only that its own route was working.
   >
   > This is now recorded as a census blind spot in its own right: **an absence argued from
   > address-takers is an absence of address-takers, not of accesses.** Image-base-relative
   > addressing is common in this executable — `lea r14,[rip-...]` materialising `0x120000` and
   > then indexing every global by offset — so this is not an exotic escape.
   >
   > ### What the table actually is, which is the more useful half
   >
   > `022C6D20` is not a standalone byte array. It is **one column of a structure-of-arrays**
   > spanning `022C6C00..022C6E70` — `0x270` bytes, **18 columns**, indexed by the same manager
   > index `m`:
   >
   > | columns | width | addresses |
   > |---|---|---|
   > | 7 | qword | `022C6C00`, `C28`, `C50`, `C78`, `CA0`, `CC8`, `CF0` |
   > | 2 | byte | `022C6D18`, `022C6D20` |
   > | 2 | dword | `022C6D28`, `022C6D40` |
   > | 7 | qword | `022C6D58`, `D80`, `DA8`, `DD0`, `DF8`, `E20`, `E48` |
   >
   > **There are 5 rows, established twice independently.** Every qword column is `0x28` = 5x8
   > apart, every dword column `0x18` = 5x4 rounded to 8, every byte column `0x08` = 5 rounded to
   > 8 — one consistent row count across all three widths. And `0032F430` is a loop whose own
   > bound is `0032F4F5 cmp rax, 5 / jl`, with `mov edi, 5` immediately after it. The block's upper
   > edge is corroborated from outside: `022C6E70` is a **separate** 4-entry pointer table, bounded
   > by `cmp ecx, 3 / jg` at `0032F260`.
   >
   > So the two functions are not special cases that happen to touch the mark:
   >
   > * **`0032F430` is the whole-block initialiser.** It walks all five rows and zeroes every
   >   column, setting the two dword columns to `0xFFFFFFFF` rather than `0` — 18 stores per row.
   > * **`0032ED80` is the per-row teardown.** It takes `m`, releases what the row's pointers own,
   >   then zeroes that row's columns — 16 of the 18, leaving the two `-1` id columns alone.
   >
   > **The mark is cleared because the whole row is cleared.** It is not an exception to a sticky
   > rule; it is one column of a uniform row reset, and the clear was always going to be there.
   >
   > A related reading falls out of the same pass: `022C6D18` is a **presence flag**, not a second
   > mark. `0032F240` is `cmp byte [rax+rcx+0x21a6d18], 0; je → return -1; else return
   > dword[022C6D28 + m*4]` — the byte guards the id column and the accessor fails closed to `-1`.
   >
   > ### What survives
   >
   > The gate decode is untouched: `0025DA3A` still raises the request only on those four
   > conditions, `+0x10` bit 0 is still set only by `0026D305` and cleared only by `00262DA8`, and
   > `+0x11` bit 3 still holds the pass off while a payload load is in flight. §13's mechanism is
   > unchanged. **What changes is the lifetime claim**: the mark is per-row state cleared on
   > teardown and on init, so "a mark that is never cleared is survivable at all" is answering a
   > question that does not arise, and the forced-reload dilemma built on permanent stickiness
   > goes with it. FABLE's rejected word *deferred* is not thereby restored — nothing here shows
   > the mark being **consumed** by the pass, only reset by teardown and init, and the exact
   > ordinary-reload timing remains unobserved.

   >
   > > **“Sticky” is withdrawn — 2026-09-21 (ASTRA's clear, consumed by FABLE).** The word was
   > > chosen *because* nothing consumed the byte, and something does:
   > > `0032F14B mov byte ptr [rdi+r14+0x21A6D20], bpl` in `ActorResource_ResetManagerLoadState`.
   > > **The mechanism below still stands** — the one-shot behaviour does live in `+0x10` bit 0 and
   > > `+0x11` bit 3, and the pass's four-part gate is untouched — but the mark is cleared on the
   > > load-reset path rather than never. *What does not follow, and is not claimed:* that the reset
   > > runs on every reload, which ASTRA left as a separate question, or that the clear is executed
   > > rather than read, which it is not. **And this correction is about the per-manager byte only;
   > > `02099ABC`'s request mask is a different object and is untouched.**
   >
   > ### The one consequence that is not closed, stated so it can fail
   >
   > If the mark is truly never cleared, then a manager disposed once by a script and **later
   > re-loaded** becomes live with bit 3 clear, and the very next pass requests its unload again.
   > Either something clears the byte by a route no static method reaches, **or a re-loaded manager
   > is torn down on the pass after its load completes.** The second is observable and cheap:
   > `OPUS-REQ-ASTRA-MGRMARK-RELOAD` asks for `022C6D20[0..4]` read once before and once after an
   > area change that re-enters a previously disposed manager. **This note does not assume which
   > way it falls**, and the four negatives above are what make the question worth one attach.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| slot block base `02098E10`, stride `0x288`, index sign-extended and unchecked | **re-read 2026-09-12**: `0025D9EC movsxd r14, ecx`, `0025D9EF lea rdi,[→02098E10]`, `0025D9F6 imul rbx, r14, 0x288` | 1 | PROVEN |
| the save-busy refusal returns 1 | **EXECUTED**: driven at four non-zero busy values, and the call trace shows **nothing else is called** — which is the part of this row that matters and the part bytes cannot show | 1 | PROVEN |
| a **second** refusal, `+0x10` bit 0 clear, returns the same 1 | **EXECUTED**; and a THIRD way to return 1 is now on the record: `003603C0`'s byte being non-zero. **Not on the source page** | 1 | PROVEN |
| `+0x11` bit 0 is republished from `+0x10` bit 7 every frame | **EXECUTED** over all sixteen combinations of the source bit and the target byte: the result EQUALS bit 7, `1 -> 0` included, so it is a copy and not a sticky OR, and bit 3 survives it | 1 | PROVEN |
| **`0026A5F0` RECURSES for slot 0, marking slots 1, 2 and 3 before itself** | **EXECUTED**: one call on slot 0 makes fourteen trace entries, sets bits 0–3 of `02099ABC` and runs the `002E15D0`/`002E1690` pair four times. Any other slot makes three entries | 1 | PROVEN |
| **the mark's shift count is masked to five bits** | **EXECUTED**: slot 32 sets bit 0 and slot 33 sets bit 1, driven against a zeroed mark | 1 | PROVEN |
| **`0032F6E0` and `003603C0` sign-extend their bytes, and four of the six callees take NO argument** | **EXECUTED**: bytes `0x80` and `0xFF` drive the first, and the trace shows `003603C0` entered with `022C6D20` in `ecx` — the table base `0032F6E0` returned | 1 | PROVEN |
| **`002E1690` sets the byte `002E15D0` has just cleared** | **EXECUTED**: `0215F1A1` ends at `1` after every mark, and the campaign's kind-A survivor is that clear being dead | 1 | PROVEN |
| **slot 5's block CONTAINS the mark global** | ~~`02098E10 + 5·0x288 = 02099A88`, and `02099ABC` is `0x34` into it~~ **corrected §15a: `02098E10 + 5×0x288 = 02099AB8`, and `02099ABC` is `+0x4` into it** — the conclusion is unchanged and sharper. **EXECUTED** with both planted as one region | 1 | PROVEN |
| the drive loop's two exits are different continuations | **re-read**: `0025DB4F jne 0025DB76` against `0025DB54 je 0025DECB`; `0025DB79 mov [rbx+0x12], r12b` and `0025DB7D call 002620E0` exist only on the first. **Not on the source page**, which reads as though both stop the loop | 1 | PROVEN |
| the tail increments `+0x24` and `+0x38` and returns `r12d` | **re-read**: `0025DED5`, `0025DED8`, `0025DEE0` | 1 | PROVEN |
| bits 0–3 of the record's `+0x14` are never written, so the inner repeat is dead | the page's §4 correction: every byte write at `+0x14` in `.text` listed (80 sites), each attributed to its base structure, with the sweep naming all five census writers as its control | 1 | PROVEN |
| no iteration cap on the drive loop | the page's §9, with the other three loops' caps as the positive control | 1 | PROVEN |
| `02099D78` is null two ways | the page's §3: the caller's zeroed `rdi`, and the resolver's own two `xor eax,eax; ret` | 1 | PROVEN |
| `[rbx+0x20]` is the actor count and is folded by AND twice | the page's §5, `0025DD64` and `0025DEAE` | 1 | PROVEN |
| the four-iteration loop walks the party roster at `0209A1F0` | the page's §5, `lea r13,[0209A1F0]` at `0025DC4D` with `add r13, 8` | 1 | PROVEN |
| the wait dispatch marks the WAIT SLOT's `+0x14`, not the record's | the page's §11, `0025E04B` / `0025E04F` | 1 | PROVEN |
| the entry gate executed in isolation | **EXECUTED**: `diff_field_gate.py`, the 42nd pilot — 54 cases, 0 mismatches, and **nothing scripted** | 1 | PROVEN |
| any execution of the PASS, or any live observation | **none**; §13. This is the first 120 bytes of 1,297 | none | UNKNOWN |
| what `+0x14` bit 5 means | **the script enable flag** — `FRP-1`, answered 2026-09-18 (FABLE): written only by `00269E00` behind verbs `001E enable` / `001F disable`, read by the seven pass sites that skip a clear entry (item 1 of §the open items) | 1 | PROVEN |
| ~~`022C6D20[m]` has **no clear anywhere in the image**~~ **REFUTED 2026-09-21 (ASTRA; consumed by FABLE)** — the clear is `0032F14B mov byte ptr [rdi+r14+0x21A6D20], bpl` in `0032ED80 ActorResource_ResetManagerLoadState`, with `r14 = 00120000` from `0032EDBB lea r14,[rip-0x20EDC2]`, `rdi` the sign-extended manager index and `bpl` zeroed at `0032EDC2`, behind the `0032F107 cmp rdi,5` / `jae` valid-index check | the four routes below were **sound and scoped**, not wrong: this store hides the table base in a register holding the **image base** with a `table − imagebase` displacement, so a RIP-store census, a DIR64 relocation scan and a block-clear decoder all miss it by construction — *which is the blind spot this row already declared*. Cross-checked by the getter: `0032F6E0`'s own `0032F6E3 lea rcx,[rip+0x1F97636]` resolves the **same** table and loads a signed byte by the same index, so base, width and stride agree rather than an address sum landing somewhere plausible; slots 1 and 4 separate the byte stride from the neighbouring stride-8 table | 2 | **the negative is withdrawn**; the clear is Method A, and is conditional on native cleanup returning normally, which ASTRA did not execute |
| the pass's request needs **all four** of no-save, `+0x13 != 0` or `+0x10` bit 0, `+0x11` bit 3 clear, and the byte | **re-read 2026-09-13**: `0025DA1A`, `0025DA20`, `0025DA25`, `0025DA2E`, `0025DA3A` | 1 | PROVEN |
| the one-shot behaviour lives in the block bits, not the byte | **MEASURED**: `+0x10` bit 0 set only at `0026D305` (`ActorSystem_InitializeManagerRuntime`) and cleared only at `00262DA8` (`002628B0`); `+0x11` bit 3 set at only 2 sites image-wide, one `ActorResource_BeginPrimaryPayloadLoad` `003303DF`, cleared by the load-completion family (`003306AF`, `0032F9AA`) | 2 | PROVEN |
| whether a **re-loaded** manager whose mark is still set is unloaded on the next pass | **DISSOLVED rather than answered, 2026-09-21** — the premise fails: a manager that goes through `ActorResource_ResetManagerLoadState` does **not** have its mark still set. *Whether that reset always runs on reload is a separate question ASTRA explicitly did not close*, so nothing here says a reload is safe by construction | — | premise withdrawn |
| what `+0x10` bit 0 means — disabled, uninitialised, or other | **the slot live flag** (`FRP-3`, 2026-09-19): set only at `0026D305` (init), cleared only at `00262DA8` (unload `002628B0`) under a census widened to all byte-write forms in the 58 base-takers plus all 93 `00263FF0` getter callers (whose only `+0x10` writes land on `002E97B0` entries); five indexed accessors fail closed on it — refusal 2 = *not live* | 2 | PROVEN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### Corrected: a digit transposition in slot 5's block address, and the offset that rode on it

Both operands were re-read from the image — `0025D9EF lea rdi, [rip → 02098E10]` and
`0025D9F6 imul rbx, r14, 0x288` — so the arithmetic can be done rather than quoted:

| | stated | **measured** |
|---|---|---|
| slot 5's block start | `02099A88` | **`02099AB8`** |
| `02099ABC`'s offset into it | `0x34` | **`+0x4`** |

`0x288` is 648; `5 × 648 = 0xCA8`; `02098E10 + 0xCA8 = `**`02099AB8`**. The stated `02099A88` is a
transposition of the same digits, and the `0x34` offset was computed *from* it, so one slip produced
two wrong numbers.

> **The claim survives and gets sharper.** Slot 5's block runs `02099AB8`–`02099D3F` and does contain
> `02099ABC` — at **four bytes in**, not fifty-two. And **slot 4's block ends at `02099AB7`,
> immediately before the global**, so the mark word sits outside every valid slot and just inside the
> first invalid one. "Slot 5 is worse than out of range" is right; it is worse than the document said.

### Confirmed where it stands

| claim | image |
|---|---|
| index sign-extended and unchecked | `0025D9EC movsxd r14, ecx`, then `imul`/`add` with no compare |
| the four-iteration party loop at `0209A1F0` | `0025DC4D lea r13, [rip → 0209A1F0]`; the loop closes on `0025DCCF jl` after `cmp r15d, 4` |
| the tail increments `+0x24` and `+0x38` and returns `r12d` | `0025DED5 inc [rbx+0x24]`, `0025DED8 inc [rbx+0x38]`, `0025DEE0 mov eax, r12d` |
| the wait dispatch marks the **wait slot's** `+0x14` | `0025E04B mov byte [rsi+0x14], 1` and `0025E04F mov byte [rsi+0x27], 1` — **in `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`), the neighbouring function, not the pass** |

### The "no iteration cap" negative, with its controls listed

Every backward branch in the pass's 364 instructions, and what sets its flags:

```
0025DA51 je  <- test byte [rbx+0x10], 1      0025DCCF jl  <- cmp r15d, 4          (capped at 4)
0025DA5A jne <- test eax, eax                0025DD67 jl  <- cmp edi, [rbx+0x20]  (capped by count)
0025DA7F jne <- test byte [rbx+0x11], 4      0025DEB1 jl  <- cmp edi, [rbx+0x20]  (capped by count)
0025DB74 je  <- test cl, 0x40                <-- THE DRIVE LOOP: a bit test, no counter
```

**Three loops carry a compare against a limit and the drive loop carries none** — the positive
controls are in the same function, which is what makes the absence meaningful.

### Clarified: `[rbx+0x20]` bounds the loops; the `AND` folds the result

§15 reads *"`[rbx+0x20]` is the actor count and is folded by AND twice"*, which puts two different
things in one sentence. `0025DD64`/`0025DEAE` are `cmp edi, [rbx+0x20]` — the **loop bound**. The
`AND` beside them (`0025DEAB and r12d, eax`, after `shr eax, 6`) folds each actor's **result** into
the accumulator returned as `r12d`. Both happen twice; they are not the same operation.

**Not claimed:** no live observation, and the pass itself is still unexecuted — §13's "this is the
first 120 bytes of 1,297" stands; `FRP-1` closed 2026-09-18 (the script enable flag, item 1 above).

## 16. Parity plan

**Constructible offline, and only in one bite:** `STATE-TRANSITION` and `EDGE-CASE` over the entry
gate — the two refusals, the republish and the return-`1` convergence — plus `STRUCTURAL` for the
slot block's stride and the fields §3 names.

**Not constructible offline, and why:** `CALCULATION` — the conjunctions are over records the fixture
would have to invent; `INTEGRATION` — 49 callees, and the pass's meaning *is* the integration;
`TIMING` — per-frame ordering is exactly what an isolated run removes; `PRESENTATION`; `RNG` and
`SERIALIZATION` — none; `FULL SUBSYSTEM` — no.

**This is the contract in the set whose parity plan is most honestly negative**, and that is a fact
about the operation rather than about the effort available: a per-frame driver over fifty callees has
almost nothing an isolated differential can hold still.

## 17. Related

- [`the-field-runtime-pass.md`](the-field-runtime-pass.md) — the mechanism this formalises, including
  the dead-nibble correction and the `0025DF00` wait resolver read in full.
- [`../11-Party/CONTRACT-party-slot-assignment.md`](../11-Party/CONTRACT-party-slot-assignment.md)
  — the roster the four-iteration loop walks.
- [`../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md`](../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md)
  — what runs once this pass decides an actor may proceed.
- [`../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md`](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md)
  — the save write that raises the busy flag in §10 row 1.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — SERVICE.** `003065D0` on this page calls `BattleStats_ModifyHPAndProcessLethalState`, owned by that layer. What it reaches is the HP-modification entry point: it resolves the owning unit for both the source and the target, reads the target unit's `dword[+0x48]`, and decodes its flags argument bit by bit - bits 0, 1, 2, 4 and 5 each select a separate behaviour; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT.** `FUN_0031adb0`, owned by that layer, calls `003590D0` on this page. That caller is a 1,790-byte routine with a stack cookie and a `0x80`-byte frame; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — CLIENT.** `FUN_003160c0`, owned by that layer, calls `003148F0` on this page. That caller is a 212-byte walk of the table at `[022C2550]` from `+8`, the same table the equipment-slot eligibility test walks; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (8 edges through 3 of this page's functions).** The UI layer reaches this page at `003148F0`, `003590D0`, `002E09A0`. `FUN_00254b50` is the worked example, read in full - it is a 263-byte entry that masks its id to `0x7FFF` and takes one of two paths on `[02092734] == 1`; **5 of the 8 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — MECHANICAL (SWE2-CONTRACT 2026-09-15, 16 edges).** The field pass shares generic
accessors, not input state: `Input.ActorControlMaskPropagationRuntime` `00226BE0` reaches the shared
`00263FF0`/`00358940`/`003590D0` helpers this contract cites (3 edges), `Input.CommandGateBoundarySupport`
`002E09A0`/`0036FD90` shares `00263FF0`/`00314020`, `0022B8C0` calls the input-rebuild family
(`InputGameplay_RebuildFrameSnapshotFromChannelHistory`, `InputControl_SetOneShotFrameCallback`,
`0035AE30`/`0035AF10`/`0035AF20`/`0035FF90`/`0017DE60`/`00182D40`/
`InputGameplay_RebuildRemappedTransitionMaskState`, 9 edges) on the same frame tick the pass runs
on, and `002628B0` shares `0035B5D0`. Frame-cadence and shared-accessor fan-in only.

**CombatAction — CLIENT (SWE2-CONTRACT 2026-09-15, 9 edges).** `BattleAction_InitializeGlobalSpecialSequenceMode`
`00306BD0` calls `0032F6E0`/`0032FC30` (2 edges); `BattleUnit_TryTriggerNearbyAuthoredFieldAction`
and `002FA740` reach `003148F0`; `003065D0`/`00306570` reach `00332190`; `00317E60`/`00319090` and
`00313DB0` share `003590D0`/`00226BE0`. The action layer consults the field pass's helpers when it
initializes special-sequence mode and triggers authored field actions — the layer consults this
page's functions, not shared ownership.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Audio — SERVICE, CLIENT (22 edges).** The pass `0025D9E0` calls `00261F90`, the area-music select, which reads the field id `003148F0` and the save image `002EF2B0` and starts the chosen track through `002DEC00`, `002DEE50`, `00360D30` and `00361170`; the init core `002620E0` calls `00363B40`; the slot unload `002628B0` calls `00360B50`, `00360DD0` and `003636A0`; `00313DB0` calls a 13-byte audio body; the tick `00314020` calls `002DEBA0` and `00362850`, and `00362850` calls the focus-handle getter `003590D0`; and seven audio bodies (`002DEF40`, `002DEFA0`, `002DF010`, `002DF120`, `002DF220`, `002DF2C0`, `002DF560`) call `003603C0`, the 8-byte getter that returns one signed byte of a global. Loading, unloading and running a slot starts and stops area audio, and audio code reads two of the same small getters; the contract's drive-loop claims involve no audio state.

**CoreRuntimeScheduling — CLIENT, SERVICE, MECHANICAL (25 edges).** The frame bodies `0022A770`, `0022B8C0` and `0022BC20`, with `0022AF50` and `0022B000`, call the pass-set bodies `0035AE30` (the deferred-pair drain), `0035AF10` (a 16-byte clear) and `0035AF20` (the tick accumulator), and three of them call the tick `00314020`; the dispatcher `0022A580` calls `0022B8C0`, which calls `00374FD0`; `0022A770` also calls `00264610` (the slot's `+0x48` table pointer, 0 unless the slot's live bit is set) and `003603C0`; `0025DF00` calls the veto predicate `001EDDA0` and the readiness sum `001EDE80`; the unload `002628B0` calls `00229EE0`; and `0022A0B0` calls the path-table installer `002DF9A0`. The scheduling layer's frame bodies are what run the tick and the pass set every frame, and the pass's wait resolver asks that layer's two readiness questions; the contract's order claims begin at the tick and take the frame bodies as given.

**Movement — SERVICE, CLIENT (48 edges).** The pass `0025D9E0` calls `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`), which the census files to Movement and which calls `Movement_UpdateActorFrame` (`002E5030`), `002E5750`, `Movement_SetRequestedSpeed` (`0026D6F0`), `002E4A10` and `002E6310` as well as the interpreter `0025E4C0`; the unload `002628B0` calls `00263560`, `0026A1D0`, `00379070`, `003791C0`, `003792D0` and `003DAA20`; `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) calls `Movement_SetRequestedSpeed`; `00233AA0` calls `00311E10` and `00311E20`; `0022B8C0` calls `00263560` and `0037CF00`, and the tick calls `00234520`, `003DAA20`, `003DAA40`, `003DAC70` and `0046AFA0`; and movement bodies call this page's accessors - `003590D0` from eleven (such as `Movement_UpdateSteeringTowardTarget`, `002E45E0`, and `BattleUnit_CanAdvanceCombatNavigation`, `00325D90`), the slot-block getter `00263FF0` from `002E28E0` and `00392740`, `00263B50`, `00263C50` and `00358940` from `00392740`, `002E97B0` from `0025DF00` and `0026A490`, `002E9FE0` from `002E6330` and `002EA7F0`, `00313DB0` from `00234520`, `003148F0` from three, and `00377DB0` from `002E4A40`. The pass drives each actor's script and then hands it to the locomotion step, binding and unloading set and clear movement state, and movement code reads slots, records and the focus actor through the contract's accessors; the pass decides when locomotion runs, never how.

**Party — SERVICE, CLIENT (21 edges).** The pass `0025D9E0`, `0025B600` (the common tail's call), `0026C8C0` and the party's own roster bodies (`PartyRoster_GetActorBySlotOrCurrentFocus`, `00263770`; `PartyRoster_AssignActorToSlot`, `00269C70`; `BattleUnit_GetPartyLeader`, `003272A0`; `PartyFocus_IsCurrentPackedActorHandle`, `003273B0`; `00327270`; `003272F0`) call `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`); `0022B8C0` and `0025C830` call `PartyFocus_CommitPendingPackedActorHandle_Thunk` (`00358BB0`); `00233AA0` calls `PartyFocus_SelectAndRequestDefaultActor` (`00326500`); the unload `002628B0` calls `PartyFocus_ClearCurrentActorIfEligible` (`00358B40`) and `PartyControl_SetMovementSuppressionBit` (`00359200`), as does `0026C8C0` for the latter; `00313DB0` calls `BattleUnit_ResolveByFocusHandle` (`0031B7E0`); the tick calls `PartyControl_UpdateControlledActorLocomotion` (`00358C60`) and `PartyFocus_UpdatePrimarySecondaryActorProcessing` (`00358EE0`); and `PartyFocus_ProcessActorControlPresentationState` (`00358F90`) and `PartyFocus_TryGetCurrentActorWorldPosition` (`00359150`) call the entry readers `002E97B0`, `002E9FE0` and `002EA6A0`. The contract's published focus entry is the party layer's focus handle resolved each pass, unloading a slot clears a focus actor that belongs to it and sets movement suppression, and the party layer reads the focus actor's entry through this page's readers; the party owns the handle and the roster.

**Presentation — SERVICE, CLIENT (69 edges).** `0022B8C0` calls the frame's render work (`RenderSystem_RunCharacterUpdatePipeline`, `003323D0`; `VFXSystem_RenderSpecialPassWithGraphicsFence`, `002590F0`; the two `GraphicsSync_*` bodies; `002512B0` and six more); `0025DF00` calls the three sub-record wrappers `003E68B0`, `003E6A70` and `003E6EF0`; `002620E0` calls `00259B30`; the unload `002628B0` calls `002E65A0`, `CharacterRenderSystem_RefreshDistanceCullEnable` (`002E8CC0`), `003EB500` and `003EB5F0`; `0026C8C0` calls the eight `CharacterRenderSystem_*`/`CharacterRenderConfig_*` fade getters and setters (such as `CharacterRenderSystem_SetFadeStartDistance`, `002EBC30`, and `CharacterRenderConfig_GetDefaultFadeWidth`, `002EDA40`); the tick calls `CameraSystem_GetActiveMask` (`00259AF0`) and `003E7650`; `003B7770`, `003B7880` and `003B8090`, the only bodies the contract found writing an entry's `+0x10`, call `Actor_RefreshPresentationVisibility` (`002E8FD0`); and render bodies call the contract's accessors - the effect-element dispatch fronts `003A4290` and `003A56F0` with `00465120` and `00465690` call `00263C30`, `00263FF0` and `00358940`, twelve bodies such as `RenderSystem_UpdateCharacterRecords` (`00426090`) call `003590D0`, `003DD4C0` calls `00263FF0`, `0032F240` and `0032F260`, the UI input consumers `002B7B80` and `002BAF80` call `003148F0`, `CameraRecord_CopyViewState` (`0025A2C0`) calls `00377DB0`, `0037D4C0` calls `00382B70`, and `0046E990`/`0046EE70` call `0035B1A0`. The pass binds a definition's fade distances into the character renderer, unload refreshes culling, and render code reads slots, records and the focus actor through the same accessors; the contract states no render behaviour.

**Resource — SERVICE (6 edges).** `0022B8C0` calls the message-buffer state machine `00324510`; the unload `002628B0` calls `0032E520`; `0032F430` calls `0032E400`, `0032E520` and `0032E620`; and `002A7A40` calls `0024A680`. These are the resource-set load and release calls around a slot's lifetime and one release helper; §8 records the pass's resource interactions as requests, and the loads are the resource layer's.

**Save_Load_Settings and SaveLoad — SERVICE, CLIENT (29 edges).** The pass calls `SaveImage_GetPersistentPayloadBase` (`002EF2B0`) and `SaveWrite_GetBusyFlag` (`00583920`); `00261F90`, `002620E0`, `002628B0`, `0026C8C0` and `003148F0` also call `002EF2B0`, which calls `SaveImage_GetActiveRuntimeBuffer` (`002EF640`); `002EF640` is called by 18 save bodies (such as `SaveRuntime_RebindImageBackedGameplayState`, `00238A80`, `SaveWrite_PrepareAndSubmitFullImage`, `0057E310`, and `00580CD0`) and, with `002EF2B0`, by the SaveLoad-domain `00280140`; and `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`) calls `003148F0`. The pass declines while the save-write busy flag is set and reads persistent fields from the save image, and the save writer reads the field id for the header; the save layer owns the image and the flag.

**Script_VM_Native_Bridge — SERVICE, CLIENT (115 edges).** `0025DF00` calls `WorldActorScriptVM_InterpretBytecode` (`0025E4C0`), the two `ScriptVM_WaitList_*` tests (`00267420`, `002674B0`) and the state pair `00357760`/`00357770`; the interpreter calls `0025B400`, `VMNativeCommand_ExecuteLifecycle` (`002621D0`), `VMValueStack_PopNumericDiscard` (`00267DB0`) and 14 more, and calls `0025B500` and `002659F0`; `002621D0` calls the three `VMNativeCommandDispatch_Get*Callback` getters (`003DC240`, `003DC270`, `003DC2A0`); `00356D40` calls `VMValueStack_PopInt32CoerceFloat32` (`00267E10`) and is called by `0033F710`; and script verbs call the contract's accessors - `00263FF0` from 20 (such as `0033F7F0`, `00342490` and `00348130`), `00358940` from 17, `003590D0` from 14, `002E97B0` from eight, `002EA6A0` from seven, `0032F240` from four, `0032FC30` from four (`003522C0`, `00353080`, `00353590`, `0050D0C0`), `0026A5F0` from `0050D0C0` and `0050D240`, `002E1690` from `003462D0` and `003470D0`, and `00263C30`, `003148F0`, `00332190`, `0035FED0`, `00377DB0` and `00382B50` from one or two each. The pass is the interpreter's driver and the resolver of its waits, and script verbs read the manager slots, records, focus actor and entries through this contract's accessors and raise the requests it services; what each verb does belongs to the script-VM pages.

**Spawn_Encounter_Lifecycle — CLIENT (1 edge).** `SpawnKeep_RotatePersistenceBanksForAreaTransition` (`00233780`) calls `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`). The spawn keep reads the same active-or-pending field id at an area transition that the pass's music select reads; it is a second consumer of the getter.

**Story_Event_Quest_Hunt — SERVICE, CLIENT (13 edges).** `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) calls `EventMemory_QueryDefinitionIdAbsent` (`00377440`), and all twelve `PersistentFlag_*` bodies (such as `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate`, `0032A8A0`, and `PersistentFlag_SetBank64A`, `0032AC70`) call `SaveImage_GetPersistentPayloadBase` (`002EF2B0`). Binding a loaded definition consults event memory for whether that definition id is absent, and the story flags are stored in the persistent payload the contract reads through the same getter; no story flag is read by the pass.

## Interior citation — frontier hub `0026A5F0` (2026-09-18, SWE2-EC7)

`0026A5F0` — 74 B, 6 callers; this page's documented recursion confirmed byte-for-byte:
`ecx == 0` recurses as `self(1)`, `self(edi+2)`, `self(edi+3)` ([`0026A60C`](../_index/ADDRESS-INDEX.md)),
then unconditionally `or dword [02099ABC], 1 << cl`, calls `002E15D0` (clears the
`0215F1A0`–`0215F1A8` router latch) and tail-jumps `002E1690` (sets `0215F1A1`). The four
trace entries per slot-0 request the contract cites are this exact shape.


### Interior citation — frontier hubs `0035AE30`, `0035AF20` (2026-09-18, SWE2-EC7)

`0035AE30` — 203 B, 5 callers. The field pass's deferred-pair service: when
`dword[02EC0B3C]` holds, two `0035FED0` calls per slot arm (`edx=1`, then
`edx=0`) push an 8-byte-stride pair table's entries; the clear arm does the same
with zeros. Then an 8-iteration sweep over the `022C8030` dword cells — each
nonzero cell decodes a `(cl-1)*0x20` row, and where `word[+2] == ecx>>8` and
`byte[+1] == 4` it calls `0035B1A0` ([`0035AEDD`](../_index/ADDRESS-INDEX.md)) and
clears the cell. A drain of tagged pending requests.

`0035AF20` — 636 B, 5 callers. The tick accumulator: `r14d = dword[021C804C] +
cvttss2si(float[00DFE0C8] * float[0095FAF4])`, and once the running count crosses
`0x2710` the body walks the `0x2DA0B80`-family records — `0xD1B71759` magic-div
derives the slot, each record's byte-range interpolator `([+7] - [+5]) * progress
/ [+4] + [+5]` is divided at [`0035B043`](../_index/ADDRESS-INDEX.md) and the
min-clamped result stored to `dword[0x2DA0B50 + idx*8]` while advancing the
record's position/counter bytes. The periodic ramp the pass runs on elapsed
ticks.
## SWE2-EC7-19 update (2026-05-15) — `0035AF10` field-pass fragment

`0035AF10` (12 B) is one of the `0035AExx`/`0035AFxx`/`0035FFxx` bodies this contract lists in the pass set: its whole body is `xorps xmm0,xmm0` + `movdqu [02EC0B50], xmm0` + `ret` (`0035AF10`..`0035AF1B`) — a 16-byte clear of the `02EC0B50` global quadword pair, the reset leaf the pass's field-scan arms call.

## SWE2-EC7-51 update (2026-09-19) - `00356D40`

`00356D40` (172 B) is a `00332190` caller - `0016D6A0`/`002640C0`/`00267E10`/`00332190`/`00382B50`. Interior anchor `00356D55` (an `0016D6A0` call).

## SWE2-EC7-78 update (2026-09-20) - `0079AE90` bounded clear-and-report measured

`0079AE90` (71 B) is the slot-table clear: `r8d < 7` selects
`[rcx + r8d*8 + 0x118]`; `edx - 0x1C < 0x100` bounds the index; if
`byte[rdx + rec + 0x30]` is set it is zeroed and 1 returns, else 0 -
a test-and-clear with strict bounds.
Interior anchor `0079AEB1` (the `+0x30` byte test).

## SWE2-EC7-85 update (2026-09-20) - `00404DC0` paired flag clear measured

`00404DC0` (66 B) is the two-object flag maintenance the runtime
callers run: on global object A, `[+0xC8]` bit 3 clears unless bit
1 is set; on global object B, `[+0xC8]` bit 7 clears unless bit
`0x20` is set - call-free.
Interior anchor `00404DD7` (the `and ecx, 0xFFFFFFF7` clear).

## SWE2-EC7-86 update (2026-09-20) - `003E91D0` conditional sub-object release measured

`003E91D0` (47 B) is the guarded release the field-pass callers
run: when `[rcx+0xB8]` is live it calls `002A7A40([rcx+0xC0])`
on the attached sub-object and then clears `+0xB8` to null -
release-then-unlink.
Interior anchor `003E91E9` (the `002A7A40` release call).

## SWE2-EC7-92 update (2026-09-20) - `00382B50` scalar publish measured

`00382B50` (21 B) is the three-word publish `00356D40` calls from
the field pass: `xmm2` lands at `02A1A39A`, `ecx` at `02A1A388`,
`edx` at `02A1A386` — adjacent slots in the same global block as the
`00382B70` vec4 writes.
Interior anchor `00382B58` (the `ecx` store).

## SWE2-EC7-98 update (2026-09-20) - `002E24B0` measured

`002E24B0` (12 B) is the clear-and-delegate `002628B0` and
`0026C8C0` call: `byte[022CF1B3]` is zeroed, then the tail
`jmp 00404DC0` runs the real pass - the one-flag preamble
the runtime pass's callers go through.
Interior anchor `002E24B7` (the `00404DC0` tail jmp).


### SECTION-12 evidence incorporation — 2026-09-24

The selected cross-actor request path now runs through original interpreter arming, original
entry selection/start/removal and full `0025DF00` entry. [The review](../_experiments/evidence/continuation-section12-actor-request-waits/REVIEW.md)
establishes 139 bounded assertions and eight rejecting variants, including all driver kind targets
0..8 in controlled states. These do not establish every branch of every kind or outer-frame timing.
Earlier EXP-106 remains valid at its own explicit scripted-interpreter boundary. Update11 and this
section provide separate original-code evidence rather than changing that historical program.
Current notification-capacity/recovery, arbitrary reentrancy, request-identity reuse and authored
input bounds remain open. No full-system L2 or formal acceptance is awarded here.
