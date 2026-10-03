---
contract: Tick the world once — five slots, sixteen sub-steps, and a mode argument consulted five times rather than branched on once
category: 00-Engine-Core-Runtime
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: 00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md
entries: ["00314020", "00314960", "0025BFB0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — the tick's 845-byte body swept for **every** `ret` and every non-local `jmp` as
    the control on WT-3, all five mode tests and all six loop bounds located by their immediates,
    the three tick-state globals censused image-wide by two instruments, their image bytes read
    through a section-aware offset, and the guard's single reader disassembled in full. **This
    records checks performed on that date, not the method of the original derivation**, which is on
    the world-tick page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-world-tick-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the world simulation tick

> **Authored 2026-09-22 by FABLE.** S-02's binding gap left two of its three pages uncontracted. The
> stop registry was taken at `3d654bb7d`; **this takes the world tick**, so all three of S-02's pages
> now have a contract.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is six
> such invariants — and **WT-2 is the one the page's own structure hides**, because it is a fact
> about what happens *before* the mode is first consulted.

## 1. Purpose

Advance the simulation by one frame, for whichever kind of frame is being drawn.

## 2. Interface

| | body | role |
|---|---|---|
| **the tick** | `World_UpdateSimulationTick` (`00314020`), **845 B** | three callers, one per interactive frame mode |
| is a tick running? | `00314960` | **7 B** — `mov eax, [022C2548]; ret` |
| the manager request queue | `0025BFB0` | drained **before** the mode matters (WT-2) |

## 3. Types

```
022C2548  u32  tick in progress -- 3 accesses image-wide, and it cannot leak (WT-3)
01EED060  i32  \  deferred mode request; BOTH are 0xFFFFFFFF in the image, so
01EED064  i32  /  "-1 = none" is a static initialiser, not a run-time one (WT-4)

02098E10  the actor-manager slot array, stride 0x288 -- FIVE slots, compiled in (WT-5)
```

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**WT-1 — The frame mode is a PARAMETER consulted five times, not a branch taken once.** `00314042`
copies `ecx` into `r14d`, and the body tests it at **`003140CF`, `003140DC`, `00314103`/`00314108`
and `00314249`/`0031424E`**. *So this is one tick with five mode-dependent decisions, not three
tick variants; an implementation that dispatches once at the top has to re-derive which of the five
it is standing in.*

**WT-2 — The manager request queue is drained BEFORE the mode is consulted at all.** `0025BFB0` is
called at `00314078`; the first mode test is `003140CF`, **eighty-nine bytes later**. *So a menu
frame does not stop queued area preparation, the party-roster clear, or the deferred mode request —
only the slot loops depend on the mode. A reimplementation that early-outs on "this frame is a menu"
loses the one part of the tick that must run in every mode.*

**WT-3 — The tick-in-progress word has exactly THREE accesses image-wide, and it cannot leak
structurally.** `022C2548`, by two agreeing instruments: **two writers, both inside the tick** —
`00314047` sets it to `1`, `0031435D` clears it — and **exactly one reader**, the 7-byte getter
`00314960`. And the 845-byte body contains **exactly one `ret`** (`0031436C`), with its only three
`jmp`s targeting addresses inside itself. *The clear is three instructions before that single exit,
so the guard is reset on every path by construction and not by discipline — there is no path that
could forget.*

**WT-4 — The deferred mode request is a one-shot with two producers and one consumer, and its
"none" value is static.** `01EED064` has 16 rip-relative accesses — **4 writers, 12 readers**. The
writers are the tick's own clear (`003140BF`), two `WorldTransition_*` stagers, and the reset. The
tick consumes it once and writes `-1` back. **Both `01EED060` and `01EED064` hold `0xFFFFFFFF` in
the image**, so the sentinel is an initialised datum rather than something a boot path must
establish. *A request staged twice between two ticks is consumed once.*

**WT-5 — Five slots and sixteen sub-steps, and both bounds are IMMEDIATES repeated at every loop.**
`cmp ebx, 5` at `00314132`, `003141E9`, `00314218` and `00314270`; `cmp ebp, 5` at `0031425D`;
`cmp esi, 0x10` at `0031421F`. **No count is read from the slot array.** *So the five is compiled in
at five separate sites, and a port that reads the array's own count diverges from the original
wherever the two disagree — including if the array is ever sized differently.*
**"Five slots" is the mode-0 shape. In mode 1 the loops START AT SLOT 3** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 318, which executed it; `003140D9`–`00314273` re-read.)*. Both mode-1 loops, the
four-call loop at `00314112` and the single-call loop at `00314254`, begin from `ebp`. `003140FF lea ebp, [r13 + 3]` sets
it to 3, because `r13d` is zeroed at `003140D9`. The mode-0 loops begin from `r13d`, which is 0. So a mode-1 frame makes
per-slot calls for **slots 3 and 4 only**, once each, with no sub-steps. The same `cmp …, 5` bounds end all of them.
OPUS's stub-free run agrees: `00314132` and `0031425D` each ran twice in mode 1. In mode 0 the counts were `0031421F`
×16, `003141E9`/`00314218` ×80 and `00314270` ×5.
**What mode 1 is.** The raw call index has three calls to the tick. Two pass `1`: one in the main loop's frame
update and one in a second frame routine. The third passes `0` (`xor ecx, ecx`).
[The world-tick page](the-world-tick-and-the-field-frame.md) §2.2 labels mode 1 "menu / capture" and says "behind the full
menu only slots 3 and 4 tick, once". This contract does not re-derive which screen each caller serves. *Which actor managers slots 3 and 4 hold is not established here.*

**WT-6 — Two of the three per-slot calls do real work only for slot 0.** Carried from
[the page](the-world-tick-and-the-field-frame.md) §§2.2–2.3 and **not re-derived here**: the field
frame orchestrator and `00234520` are no-ops for any slot but `0`, while the actor drive pass runs
for all five. *So the sub-step loop's cost is not five times slot 0's; it is slot 0's work once plus
the drive pass five times.*
**WT-6 describes mode 0** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 318, which executed it; `003140D9`–`00314273` re-read.)*. Mode 1 never passes slot 0, so the orchestrator and `00234520` do nothing in
a mode-1 frame. There the drive pass and the per-record post-pass run for slots 3 and 4, both inside one
per-slot loop. Mode 0 puts the post-pass in a second loop after the first.

## 5. State

**Owned:** the tick-in-progress word and the deferred-request pair. **Read, never written here:**
the actor-manager slot array. **Reset every tick:** the movement-body pool's cell masks and the
five-field block the group-completion lock writes — both on
[the page](the-world-tick-and-the-field-frame.md) and not claimed here.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`../CONTRACT-per-frame-update-gate.md`](../CONTRACT-per-frame-update-gate.md) — S-02's first |
| **Sibling** | [`../System-Stop-Registry/CONTRACT-system-stop-registry.md`](../System-Stop-Registry/CONTRACT-system-stop-registry.md) — S-02's second |
| **Called by** | the frame dispatcher's three interactive modes |
| **Drains** | the manager request queue, before the mode matters (WT-2) |

## 7. State transitions

*guard = 1 → fixed prologue → drain the manager queue → consume any deferred mode request → the
mode-dependent slot loops → fixed tail → guard = 0 → return.* The guard transitions `0 → 1 → 0`
within one call and nothing else writes it (WT-3).

## 8. Script · resource · event interactions

None directly. The deferred mode request is staged by world-transition code, not by script.

## 9. Determinism

Deterministic. No generator is drawn in the tick's own body.

## 10. Failure paths and edge conditions

- The field frame reaches its call only past three gates; **those gates are unread** *(answered: see the world-tick page's EX-6, ANSWERED 2026-09-12 (FABLE), and the 2026-09-22 notes below; 2026-10-02, OPUS)* and this
  contract does not claim what they test.
- A deferred request staged while a tick is running is consumed by the **next** tick, since the
  consume happens once, early, and the slot is cleared immediately (WT-4).
- There is no failure exit: the body has one `ret` and no error return (WT-3).

## 11. Observable behaviour

None directly; this is the frame's spine. What it looks like when it goes wrong is the world
continuing to run under a menu, or stopping under one.

## 12. Reproduction formula

Sweep the 845-byte body for `ret` and assert **one**, and for non-local `jmp` and assert **none**
(WT-3). Census `022C2548` and assert **3 accesses, 2 writers, 1 reader**. Call the tick with mode 1
and assert `0025BFB0` still runs (WT-2). Read `01EED060`/`01EED064` from the image and assert
`0xFFFFFFFF` in both (WT-4). Count the `cmp … 5` sites and assert **five** (WT-5).

## 13. Runtime validation

**EXP-191** ([record](../../_experiments/EXP-191-s02-world-tick-stop-registry-exec.md) ·
[harness](../../_experiments/evidence/s02-world-tick-stop-registry-exec/check.py) · 37/37, stable ×3)
executes `00314020` as shipped bytes under Unicorn with disclosed synthetic statics and ~50
entry-intercepted subsystem callees — NATIVE-REPLAY, `live_game: false`.

- **WT-1 executed**: mode consulted at five sites; mode 0/1/2 produce the three predicted call sets
  (`358C60`/`3DF760` edx 1..5/substep loops vs slots-3..4 block vs neither), `358EE0(mode)` tail.
- **WT-2 executed**: `0025BFB0` drains before the first mode test — observed live under mode 1
  with mask `0x5` → `26CE60(2),(0)` + `2628B0(2),(0)`, mask cleared.
- **WT-3 executed (in-body)**: `d[022C2548]=1` on entry, `=0` before `ret`, all modes. The
  image-wide 3-access census remains a static claim (not re-censused here).
- **WT-4 executed**: `d[01EED060]` latched request consumed once → `cmovns`→`-1`; `d[01EED064]>=0`
  → `17D280`×2 + `32FC30(edx=req)` then `-1`; `00314410` first-writer-wins verified both arms.
- **WT-5 executed**: `cmp ebx,5`/`cmp esi,0x10` immediates; gated slot calls reach 80=16×5
  (gate=1) or 5 (gate=0 — substep 0 is ungated). **Correction to the static read**: the `267310`
  gate is inverted — `test eax; je` *skips* the slot calls.
- **WT-6 executed** (EXP-191 second pass — the five slot bodies run real with a stubbed leaf
  layer): `234590` and `234520` early-ret on `ecx!=0` (9-insn epilogues — slot-0-only);
  `25D9E0` works every slot but still carries slot-0-only arms (`25B740` in the row loop,
  `25B600` tail); `3DB1F0` calls `3DB6E0` per row unconditionally (`b[+0x63]` gates only an
  inner `1→2` byte-scan). In-context: bodies entered 80× each while slot-0 chains fire 16×;
  `267310` resolved to leaf `b[02098E10+i*0x288+0x201]` (the gate flag byte).
- Also measured: `2E0D90`/`268D00` fire only at substep 0; `228480`/`362DA0` `eax!=0` skip the
  `36FD90` resp. `362DB0`+minss timing blocks.

## 14. Unresolved

- ~~The three gates that can skip the field frame's call entirely — unread, and named as unread on
  the page.~~ **Struck 2026-09-22 (SWE2-CONTRACT): stale — the page's `EX-6` (FABLE, 2026-09-12)
  already read them, and an owner-side pass reproduces every mechanism byte-exact.**
  `001800E0` = `byte[001A9930() + 0x41A] != 0` — `001A9930` is the 8-byte getter
  `mov rax, [rip+0x1DD7831]` returning `*(01F81168)`, the `0x520`-byte map-art (`.ta`
  texture-animation) context built by `001A98B0` ([game application](../Application-Root/game-application.md));
  **corrected 2026-09-22 on FABLE's contra — the strike's `*(01F68168)` "console singleton"
  was a digit transposition plus a stale gloss propagated from the page's own `EX-6` text;
  `01F68168` has zero image references, `01F81168` has ten, and the object does supply console
  state, which is the kernel of truth in the old name**;
  `001800C0` = ring-non-empty — `001BDAB0()` returns singleton `*(01F81248)` and
  `001BD620` returns `+0xFC == +0x100` (head==tail), inverted by `sete`; `001EC560` =
  `01F832B0[dword[01DFE40C]] != 0` (index bounded ≤4) **and** `00265680() == 0`. The pump's
  shape at `0022ABB9`–`0022ABD2` is exactly `!A && (!B || !C)`, with the skip arm calling
  `002F1770` and returning mode 2 — all verified against the shipped bytes.
- ~~Whether ordinary callbacks can change the manager request mask during a pass — the page's
  `EX-9`.~~ **Struck 2026-09-22 (SWE2-CONTRACT): answered by `EX-9` on the page (FABLE,
  2026-09-18) — no.** The drain `0025BFB0`'s 3,108-function closure reaches the producer
  `0026A5F0` only via the gated-impossible `00332190(3)` route; the `+0x108` hook is null on
  every shipped path (verified here: `00262F0F` is a read-call-clear storing `rbp` zeroed at
  `0026292A`, and the slot array `02098E10` sits in `.data`'s uninitialised tail — born zero);
  no script dispatch is reachable inside the pass.
- ~~What the single reader of the tick-in-progress word is for.~~ **CLOSED 2026-09-23
  (SWE2-CONTRACT): it is the engine's reentrancy deferral gate.** The getter `00314960` fans the
  flag out to **12 call sites in 12 bodies** (the word itself still has exactly one reader — the
  getter — so WT-3 stands). The dominant shape, at 8 sites (`002F3E41`, `00333978`, `003A8C24`,
  `00449021`, `0046F22A`, `004FF15E`, `005269C8`, `00528B08`), is
  `if (ticking && !001EDDA0())` — the flag paired with the shared
  `[01DFE0C0] != 0 || [01F82E38] == 0` predicate — taking a deferred or diverted path. The
  other four sites: `00246753` stamps `[rdi+0xB4] = 1` while ticking (a deferred-work flag);
  `003D912F` tail-jumps to `00259240` while ticking (diverted continuation); `003D96C8` selects
  a different indexing path while ticking; `0052BB4A` stamps `[rbx+0x3FC] = 1` only when **not**
  ticking. *A body asked to mutate world state mid-tick defers, diverts or flags — nothing calls
  the getter and proceeds blindly.*

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| WT-3 — 3 accesses, and one exit | `022C2548` censused by two agreeing instruments; the body swept for **every** `ret` and `jmp`, with the three internal jump targets checked against the body's own extent — the control, since a second `ret` would break the claim | 1 |
| WT-1 — five mode tests | all five located by their immediates against `r14d`, which `00314042` loads from `ecx` | 1 |
| WT-2 — drained before the mode | `00314078` against the first mode test at `003140CF` | 1 |
| WT-4 — 16 / 4 / 12, and the static sentinel | the census, plus both dwords read from the image through a section-aware offset | 1 |
| WT-5 — the six bounds | each `cmp` located and its immediate read | 1 |
| WT-6, the prologue's fixed calls and the slot array | [the world-tick page](the-world-tick-and-the-field-frame.md) §§2.1–2.3 | 1 |
| the getter is a deferral gate | `00314960` caller census — 12 call sites in 12 bodies — each decoded at the call: 8 pair it with `001EDDA0`, 4 flag or divert | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on WT-1 through WT-6. **WT-2 is the one a port gets
wrong by structuring the code sensibly**: putting the mode test first and the queue drain inside the
field-mode arm is the obvious shape, and it stops area preparation whenever a menu is open.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **CoreRuntimeScheduling — internal.** The tick, its guard and its getter are this category's own.
- **ActorEntity — SERVICE.** The slot array, the drive pass and the manager runtime belong to that
  layer; **this contract asserts the loop bounds and the call order, not what any pass does.**
- **MovementAndNavigation, Party — SERVICE, through the prologue.** The movement-body pool's tick
  reset and the roster clear both run before the mode test, which is WT-2's subject. *What either
  reset does is on its own page and is not re-derived here.*
- **WorldAreaField — SERVICE.** The two stagers of WT-4's deferred request belong to that layer;
  **this contract asserts that there are two of them and that the tick consumes once**, nothing
  about the transition they stage.
- **Audio, InputGameplay, CombatAction — MECHANICAL, through the tick's own callees.** The tick
  calls into most of the engine by design; **this contract asserts the ORDER and the BOUNDS of those
  calls (WT-1, WT-2, WT-5) and nothing about any callee.** *Their addresses are deliberately not
  cited: naming any one imports its whole edge set for a statement the call order already makes.*
- **Presentation — MECHANICAL on two distinct edges, and one of them narrows §14.** The tick calls
  into that layer like any other; separately, **two bodies in it are callers of the tick-in-progress
  getter `00314960`.** That does not weaken WT-3 — WT-3 counts readers of the *word* `022C2548`, of
  which there is exactly one, the getter — but it does mean the question §14 leaves open, *what the
  single reader is for*, has its first answer on that side. *(§14 now closed 2026-09-23: the getter
  has 12 call sites image-wide — this layer holds two of them — and every consumer uses the flag as
  a reentrancy deferral gate.)*
- **Every other layer reached is MECHANICAL**, through this body's own callees.

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document, so *party*, *world*, *field* and *movement* in
> ordinary prose can clear a layer nothing here dispositions — the defect measured in
> `_index/candidates/fable-crossings-prose-false-clears.tsv`. The paragraphs above are what
> discharge these.

## 17. Related

- [The world tick and the field frame](the-world-tick-and-the-field-frame.md) — the mechanism
- [Contract — the per-frame update gate](../CONTRACT-per-frame-update-gate.md) — S-02's first
- [Contract — the system stop registry](../System-Stop-Registry/CONTRACT-system-stop-registry.md) — S-02's second

`00526D80` (844 B) is the first per-tick shake/offset channel on the battle-frame object: while `[rdi+0x2C2]` is armed (`rdi = [rcx+0x20]`), a tick counter at `[rbx+0x230]` scaled by the `01DFE0B4` divisor retriggers `0044B960` into `[rbx+0x234]` on expiry; the body then accumulates `[rbx+0x60]` into the `022D92E0` scratch column, optionally transforms it through `[rbx+0x10]` via `0039AF70`/`00398F90` and stores it at `[rbx+0x70]`; when `[rdi+0x2C1]` is set a second accumulate+transform feeds the `[rdi+0x2C4]`/`+0x2C8` pair against the `02AEDF20` basis and produces a clamped distance falloff `(1 - d/dmax)` - abs via the `01CEBD80` mask plus `00861F14` - written to `[rbx+0x238]` (1.0f when the second channel is idle).

Interior anchor `00526E7D` (function `00526D80`).

`00528F00` (691 B) is the sibling channel of `00526D80` keyed on the dword gate `[rdi+0x2F8]`: the same tick-counter/`001EDDA0`-divisor/`0044B960` reseed drives `[rbx+0x234]`, the same `022D92E0` accumulate plus conditional `0039AF70`/`00398F90` transform refreshes `[rbx+0x70]`, and the second half of the body repeats the falloff computation on the record's matching field pair. Both channels run out of the world-tick's per-frame update.

Interior anchor `00528FE4` (function `00528F00`).

`003A3E30` (373 B) is the marker-id resolver `003337B0` and `00332750` consult on singleton `02F97348`: when word `+0x368` is at least `0x8000` it bounds-checks `ecx` against byte `+0x372` and returns the `+0x10`-indexed dword (-1 above); the legacy arm (bit `0x200` of `+0x378` clear) bounds-checks the same table and on `byte[r8] == 1` entries whose `+0x90`-lane shadow is empty runs `003229E0`/`00322760`/`003B02A0`/`003B0FD0`/`0024ED80` to instantiate the object, swaps the resolved id into `+0x10` and the old id into `+0x90` (`+0x374` counting retries, -1 on overflow), while the `0x200`-set arm maps `ecx` (-1 treated as 0) through the `02096A24` id table bounded by `02096B24`.

Interior anchor `003A3F03` (function `003A3E30`).

## Cross-subsystem neighbours — batch-145 addition (SWE2-EC7)

**Presentation — CLIENT.** The two per-tick shake/offset channels this page hosts (`00526D80`, `00528F00`) are Presentation-owned bodies, and the shared helpers they call (`0039AF70`, `00398F90`, `0044B960`, `00861F14`, `001EDDA0`) draw their remaining call traffic from Presentation callers - the tick is a host site for Presentation-owned channel code plus its shared helper library, not a consumer of presentation output.

**ActorEntity and CombatAction — SERVICE.** `003A3E30`'s instantiate arm calls `003229E0` and `00322760`, which reach ActorEntity-owned helpers (`00263E30`, `003588B0`, `003589B0`) - and `003229E0` separately calls CombatAction-owned `002FFA60`/`00306BB0` - the resolver borrows the actor/action-side construction chain for the object it instantiates; the tick owns neither layer's behaviour.

**UI — shared helper.** The same instantiate path's `0024ED80` is also called from `0024B9B0` in UI - a shared utility callee, nothing more.

**Audio — SERVICE.** `00332750` (named on this page as the marker executor's caller side) calls Audio-owned `00332C40` for its `0x30`-stride marker probes, and shared `001EDDA0`/`00314020` entries carry Audio call traffic (`003B99D0`, `002DEBA0`, `00362850`) - the tick borrows Audio helpers through the executor, no audio state lives here.


`003229E0` (150 B) is the gated instantiate-helper `003A3E30`'s arm runs (the ActorEntity/CombatAction borrowing noted in this page's crossing section): gated twice on `byte[02089340] & 0x10`, it resolves `003588B0(ecx)` then `00263E30` twice (arg `edx` and the resolved `word[rbx+0x714]`), calls `00306BB0` on the first record's `+0x714` word - nonzero returns `1`, else it tail-jumps `002FFA60(bx, rdi)` - a borrow-then-dispatch construction step.

Interior anchor `00322A64` (function `003229E0`).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names each edge.*

**Input — SERVICE and CLIENT (4 edges).** `World_UpdateSimulationTick` `00314020` calls `002E09A0` (1,002 bytes) and `0036FD90`, which zeroes six words of a two-entry Input-filed table for one index (range-checked); `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70` and `002E09A0` call `00265680`, a 149-byte predicate that walks a table of `0x288`-byte records starting near `02098E20` and, when every live entry is in state 3, defers to two further tests (its meaning is not named on this page). The tick runs an input body and resets those words each pass, and the input arbiter tests the same predicate the pump's `001EC560` requires to be zero; the predicate's table is not input state, and the input decisions are that layer's.

**Movement — SERVICE and CLIENT (8 edges).** `00314020` calls `00234520`, `003DAA20` (which zeroes the qwords at `02B57CC8` and `02B57CD0`), `003DAA40`, `003DAC70` and `0046AFA0`; `00234520` calls `Navigation_HasDataset` `00383C80`; `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` calls the deferral flag `001EDDA0`; `0026C3E0` calls `00265680`. The tick schedules the movement layer's per-pass resets and updates (the bodies past `003DAA20` are named from the census only), the actor drive pass pairs with the same deferral flag as the tick, and navigation availability is asked inside the slot-0 step `00234520`.

**Party — SERVICE and CLIENT (5 edges).** `00314020` calls `PartyControl_UpdateControlledActorLocomotion` `00358C60` and `PartyFocus_UpdatePrimarySecondaryActorProcessing` `00358EE0`; `00234520`, on slot 0 only, calls `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040`; `PartyControl_ApplyAnalogLocomotionToActor` `00358CB0` and `PartyFocus_ProcessActorControlPresentationState` `00358F90` call `00265680`. The tick drives the party's steering and focus updates once per pass, and the party's analog-locomotion and presentation steps test the same predicate `00265680` the pump does.

**Script_VM_Native_Bridge — CLIENT (5 edges).** The verb bodies `0050D0C0` and `0050D240` call the request producer `0026A5F0` (which ORs a bit into the request mask at `02099ABC`, and for request 0 raises 1, 2 and 3 as well), `0050D0C0` also calls `00314410` (a first-writer-wins store of a field id that raises request 4), `00356D40` calls `00332190` (which marks a slot and raises its request when the slot's flags allow), and the 29-byte verb `00343690` calls `00265680`. Script verbs are producers of manager requests; EX-9 on this page shows no script dispatch is reachable inside the drain's pass, so their requests land between passes.

**Status_Periodic_Terminal — CLIENT (1 edge).** `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls `00265680`. The periodic maintenance tick tests the same predicate the pump requires to be zero; the predicate only reads its table.

**StoryEvent — CLIENT (1 edge).** `001ED240`, the 2,192-byte cutscene-override table, calls the pump predicate `001EC560`. The story layer's override lookup reuses the test the pump evaluates (the story word selected by `01DFE40C` out of `01F832B0` is non-zero and `00265680` answers zero); the test is shared, and the override table is that layer's.

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** WT-1 to WT-5 became checks at their instructions; WT-3 and WT-4's access counts are whole-image. Script:
`Tools/analysis-kit/gfz-scripts/falsify_world_tick.py`, output `falsify_world_tick.out`, image `73461d08…`, 0 BROKEN. WT-6
is carried from the page, and mode 1's call counts are OPUS block 318's execution.

| # | Clause attacked | Result |
|---|---|---|
| T0 | §2 size, callers, getter | **survives**: 845 B; three call sites, two passing 1 (`mov edx, 1` / `mov ecx, edx`) and one `xor ecx, ecx`; `00314960` is `mov eax, [022C2548]; ret` |
| T1 | WT-1 | **survives**: the mode is held in `r14d` and tested at the four cited sites |
| T2 | WT-2 | **survives**: the queue drain at `00314078` precedes every mode test |
| T3 | WT-3 | **survives**: exactly three accesses to `022C2548` image-wide (writes at `00314047` and `0031435D`, the read in the getter), and one `ret`, at `0031436C` |
| T4 | WT-4 | **survives**: `01EED064` has 16 accesses, 4 of them writes; both cells hold `0xFFFFFFFF` in the image |
| T5 | WT-5 | **survives**: every bound is an immediate at the cited sites; mode 1 starts at slot 3 (`lea ebp, [r13 + 3]` after `xor r13d, r13d`) |

No correction.

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-contract-world-simulation-tick-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
