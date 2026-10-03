---
contract: Change who the player is — a deferred handle swap, and what the new leader's own state suppresses
category: 11-Party
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 11-Party/active-party-reserve-and-the-moment-the-leader-changes.md
entries: ["00358BC0", "003594B0", "003594C0", "00358B40", "003590E0", "003272A0", "0023B040", "0025A6A0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — every rip-relative access to the four focus globals enumerated by **two
    instruments**, one bounded by the function list and one a linear sweep of `.text` that verifies
    each candidate is a real instruction boundary; the commit, both teardown thunks, the shared
    teardown body and the suppression recompute disassembled in full; the leader getter's call sites
    censused and tested for disjointness against the direct-access sites; and the image swept for a
    stored pointer to the kind-2 entry. **This records checks performed on that date, not the method
    of the original derivation**, which is on the leader-change page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-party-focus-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the party focus and control suppression

> **Authored 2026-09-22 by FABLE.** S-28's binding gap is *"slot assignment only, of 4 pages"* — its
> one contract, [`CONTRACT-party-slot-assignment.md`](CONTRACT-party-slot-assignment.md), covers
> putting an actor in a slot. **This takes the focus handle and control suppression**; the five
> parallel slot maps and the battle-state block field map remain uncontracted and this document does
> not claim them.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is eight
> such invariants across bodies in three categories — and **PF-3, PF-5 and PF-6 are orderings no
> single operation's contract can state**, because each is a fact about what another operation is
> guaranteed to find.

## 1. Purpose

Change who the player is controlling, and decide when they are allowed to control anyone at all.

## 2. Interface

| | body | size |
|---|---|---:|
| **request** a change | `PartyFocus_RequestPackedActorHandle` (`003594B0`) | 3 instructions |
| **upgrade** the request to the summon kind | *unnamed*, `003594C0` | 27 B, **absent from the function list** |
| **commit** — the change happens here | `PartyFocus_CommitPendingPackedActorHandle` (`00358BC0`) | **156 B**, reached only via thunk `00358BB0` |
| release the outgoing leader | `PartyFocus_ClearCurrentActorIfEligible` (`00358B40`) | — |
| zero the whole focus block | `PartyFocus_ResetState` (`003590E0`) | — |
| **derive** the leader | `BattleUnit_GetPartyLeader` (`003272A0`) | **55 B**, stores nothing |
| the shared teardown | `0025A6A0`, via thunks `0025A680` / `0025A690` | 395 B |
| **recompute suppression** | `PartyControl_RecomputeSuppressionFromLeaderBattleState` (`0023B040`) | 447 B |

## 3. Types

```
the focus block — four globals, and nothing else is in it
  022C7FE0  u32  the CURRENT packed actor handle   -- the leader
  022C7FE4  u32  the PENDING handle
  022C7FE8  u32  the SECONDARY handle              -- a separate focus, not the leader
  022C7FF8  u8   the request kind: 0 none, 1 normal, 2 summon

the gate word, three bit groups of one global
  02089340  bit 0x10   tested INSIDE the leader getter
            bit 0x40   the suppression seed
            bits 0x600 the party-down bits

read from the leader's BattleUnit
  +0x698  ptr  the stats record  (kind-dependent storage owner -- not this contract's)
  +0x6B4  u8   action state   \
  +0x6B7  u8   combo counter   > all three owned by the combo contract (PF-8)
  +0x714  u16  action id      /
```

## 4. Preconditions · postconditions · invariants

### The eight cross-operation invariants

**PF-1 — The leader handle has exactly THREE writers image-wide, and only ONE of them installs a
value from outside.** Every rip-relative access to `022C7FE0` enumerated by two instruments: **18
accesses, 3 writers, 15 readers.** The writers are `00358C2F` (the commit, storing the pending
handle), `00358B6B` (the clear, storing `0`) and `003590FD` (the reset). *So there is exactly one
instruction in the executable at which a new leader comes into being, and the other two only erase.*

> **The instrument had to be able to see code the function list never had.** A function-bounded sweep
> of the request-kind byte `022C7FF8` returns **5** sites; the linear sweep returns **7**, and the two
> extra are `003594C0` and ~~`003594D4`~~ `003594D3` *(corrected 2026-10-02, OPUS: `003594D3` is the 7-byte `mov byte ptr [rip + …], r8b`; `003594D4` decodes only as its tail with the REX prefix dropped)* — *the only writer of kind 2 and its own read of the byte*, in a
> body absent from the function list. **A caller census of this subsystem bounded by the function list
> is wrong about the one value that selects the alternate teardown.** The same linear instrument
> returns `linear-only = 0` for all three of the other focus globals, so the gap is specific and not
> an artefact of the method.

**PF-2 — The handle is encapsulated by ADDRESS, and the encapsulation is provable rather than
conventional.** All 18 direct accesses lie in `00358A24`–`00359481`. The leader is asked for through
`BattleUnit_GetPartyLeader` at **28 call sites in 25 functions**, spread across six owner categories
over more than two megabytes of `.text` — and **not one of those 25 functions lies inside the
direct-access span.** The two populations are disjoint, tested as sets rather than asserted. *(The
callers' own addresses are deliberately not cited: the fan-in is the finding, and naming any member
of it imports that member's whole edge set for a statement the counts already make.)* *Nothing outside the focus code reads the global; everything
outside it calls the getter, which stores nothing and re-derives on every call.*

> **And the handle's address never escapes:** no `lea` into `022C7FE0` exists, and an image-wide sweep
> for the address as a stored 8- or 4-byte value returns **zero occurrences**. *So the displacement
> census above has no register-base blind spot — the 18 sites are all of them.*

**PF-3 — The change is DEFERRED, and exactly one caller in the image collapses the deferral — a
debug verb.** Requesting writes `022C7FE4` and sets kind 1; the leader does not move until a commit
runs. The commit is reached only through the 5-byte thunk `00358BB0`, which has **7 callers**; the
requester has **3**. Exactly one function calls both, back to back:
`PartyRoster_AssignActorAndCommitFocusWhenEligible` (`0050C610`, `0050C646` then `0050C64B`) — and it
is the script verb **`debug_setpc`** (call id `2021`). *So in shipping gameplay the deferral is
universal: anything reading the leader between a request and the next commit sees the old one, and
the single synchronous path is a developer verb.*

**PF-4 — A commit that changes nothing is NOT a no-op.** `00358BE4 je 0x358c2f` skips **only** the
teardown. The store `00358C2F`, the kind clear `00358C35`, the resolve `00358C3C` and the tail call
`00358C52 jmp 0x2681d0` all still run. *So a redundant request still pushes the leader through the
~~locomotion path~~ roster-role notice, which sets the movement body's cell class, and an implementation that early-returns on `current == pending` drops that push.* *(answered: the push is the notice `002681E0` — O-1, party-roster-and-control-suppression.md §2; 2026-10-02, OPUS)*

**PF-5 — The request is CONSUMED before the new leader is resolved and pushed, and the pending handle
is re-read after the teardown.** The order is fixed: `00358C24` re-read pending → `00358C2F` store
current → `00358C35` clear kind → `00358C3C` resolve → `00358C52` tail-call. *Two consequences that
no single operation can state: a teardown that itself requests a different focus **wins**, because
the pending handle is read after it; and anything the final push calls may request a fresh change
**without being clobbered**, because the kind was already cleared.* This is the ordering
[EXP-051](../_experiments/EXP-051-focus-commit-reentrancy.md) executed with the callees controlled.

**PF-6 — The request kind selects exactly ONE call, at the end of one shared body — and kind 2 is the
SUMMON variant.** `0025A680` and `0025A690` are thunks of 11 and 8 bytes differing only in `r8d`
(`1` and `0`); both `jmp 0x25a6a0`. In `0025A6A0` that flag is tested **once**, at `0025A800`, and
gates a single call `003D9B80(record + 0x10)`. *Everything else the teardown does is identical on
both paths.* The alternate path is taken when the outgoing handle is `0` **or** the kind is `2`
(`00358C01`/`00358C05`).

> **Where kind 2 comes from.** `003594C0` upgrades an **already-pending** request and does nothing
> otherwise (`cmovne`). It has one caller, the 10-byte thunk `0034ED30` (`mov ecx, 2; jmp 0x3594c0`),
> which has **zero direct callers** and **exactly one stored pointer image-wide** — `.data` at
> `01EF17C0`, the **`result` slot of script verb `0205 changetosummonparty`**
> ([verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)). *So the
> alternate teardown exists for summons, it is requested by authored script rather than by any native
> caller, and it can only ever modify a change someone else already asked for.*

**PF-7 — Control suppression tests a WIDER mask than the engine-wide functional rule, and its two
masks differ by exactly one bit.** The shared rule `0x80000003` gates **entry** (`0023B0B6`, and again
for the second unit at `0023B1A8`). The mask actually computed is wider: `0x8800403B` decides
suppression bits 0 and 2 (`0023B166`), `0x8800003B` decides bit 1 (`0023B173`), and
**`0x8800403B ^ 0x8800003B = 0x4000` — bit 14, and nothing else.** *So a status whose only set bit is
14 raises bits 0 and 2 and leaves bit 1 alone*, which is the recorded Immobilize behaviour derived
here from the bytes rather than from the page. Both masks are strict supersets of `0x80000003`.
*Summarising this system as "it tests the same mask as acting and earning" is true of the gate and
false of the result.*

**PF-8 — The recompute loads the leader's `+0x698` three times and null-checks it TWICE.**
`0023B0A2` is checked at `0023B0AB`; **`0023B152` is dereferenced at `0023B15E` with no test at all**;
`0023B196` is checked at `0023B19D`. *The middle load is the fault
[the capability policy](../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md) §11
records, and it is a property of this function, not of the pointer.*

> **And three of the fields it reads belong to another contract.** `0023B124` reads `+0x6B7`,
> `0023B146` reads `+0x6B4` and `0023B13D` compares `+0x714` against `0x21E` — the combo counter, the
> action state and the action id of
> [the combo contract](../07-Combat-Action/CONTRACT-combo-continuation.md). *A combo in progress
> suppresses player control, so that counter is load-bearing outside combat and CB-1's width census
> is what makes reading it here sound.*

## 5. State

**Owned:** the four focus globals. **Read, never written here:** the gate word `02089340`, the
leader's stats record and its three action fields, ~~the manager record the teardown snapshots~~ camera context 0, which the teardown re-seats.
**Written outside the block:** ~~the manager record's~~ camera context 0's two `0xB0` blocks and its `+0x850` float *(corrected 2026-10-02, OPUS: `0025A6BE lea rax, [02097D20]` / `0025A6CB imul r15, rdi, 0x860` — one of two `0x860`-byte camera contexts; active-party-reserve-and-the-moment-the-leader-changes.md §9)*, by the
teardown; and, on the alternate path only, whatever `003D9B80` resets.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-party-slot-assignment.md`](CONTRACT-party-slot-assignment.md) — S-28's contracted quarter, and **one of the three requesters** (`00269C70` → `003594B0` at `00269D34`) |
| **Consumes** | [the combo contract](../07-Combat-Action/CONTRACT-combo-continuation.md) — PF-8's three fields |
| **Driven by** | [the verb dispatch tables](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv) — `changetosummonparty` (PF-6) and `debug_setpc` (PF-3) |
| **Uncontracted** | the five parallel slot maps and the battle-state block field map — S-28's other two pages, not claimed here |

## 7. State transitions

*request → (optionally upgrade to kind 2) → commit.* Within the commit: *teardown the outgoing leader
→ re-read pending → install → consume the request → resolve → push the incoming leader.* The kind
transitions `0 → 1 → (2) → 0`, and only the commit returns it to `0`.

## 8. Script · resource · event interactions

**Two of this subsystem's operations are reached from authored script and from nowhere else**: the
kind-2 upgrade, through a verb's result slot (PF-6), and the synchronous request-then-commit, through
`debug_setpc` (PF-3). Nothing else here is authored.

## 9. Determinism

Deterministic. No generator is drawn on any path.

## 10. Failure paths and edge conditions

- A commit with nothing pending returns immediately (`00358BC4`/`00358BCB`).
- A commit whose **new** handle does not resolve stores the handle anyway and returns without the
  push (`00358C46`/`00358C49`) — *the leader changes even though nothing was pushed.*
- An outgoing handle of `0` takes the alternate teardown, the same path as a summon (PF-6).
- The recompute faults on a null `+0x698` at `0023B15E` (PF-8); whether initialised gameplay can
  reach that state is **not** established here.

## 11. Observable behaviour

Switching character is instant to the player and deferred in the engine; the others follow because
they ask who the leader is every frame rather than being told. Summoning tears the outgoing leader
down differently from an ordinary swap.

## 12. Reproduction formula

Sweep `022C7FF8` **bounded by the function list** and assert **5** sites, then sweep `.text` linearly
and assert **7**, the two extra being `003594C0`/~~`003594D4`~~`003594D3` *(corrected 2026-10-02, OPUS: the store begins at `003594D3`)* (PF-1). Assert the 25 getter callers and
the 18 direct sites are disjoint (PF-2). Request a handle equal to the current one and assert the
push still runs (PF-4). Have a controlled teardown request a *third* handle and assert it wins
(PF-5). Set kind 2 and assert exactly one extra call, `003D9B80` (PF-6). Drive the status words with
**bit 14 only** and assert suppression bits 0 and 2 set and bit 1 clear (PF-7).

## 13. Runtime validation

**One sibling experiment exists**: [EXP-051](../_experiments/EXP-051-focus-commit-reentrancy.md)
executed the commit's body with its callees controlled — ten cases, one detected omission, isolated
execution and **no live timing**. Nothing executes the suppression recompute. S-28's runtime cell is
not addressed by this contract. *Stated rather than left blank so a CONTRACT READY header is not read
as evidence of execution.*

## 14. Unresolved

- What `003D9B80` resetting `record + 0x10` means for a summon, beyond the fields it writes.
- Whether the `0025A6A0` pair of `0xB0` blocks and the `+0x850` float are a blend; `00259510` is
  called twice with the same three pointers and the float is forced to `1.0` between them, which is
  ~~**suggestive and not read**.~~ *(answered: it is a blend — `00259510` is the family's spherical interpolate, §17 of this page, and active-party-reserve-and-the-moment-the-leader-changes.md §9 reads the five steps; 2026-10-02, OPUS)*
- ~~What mode 2 is — **O-4**, and the gate PF-7's entry test depends on.~~ *(answered: the chocobo ride — O-4, the mode ladder page §2c; 2026-10-02, OPUS)*
- The secondary handle `022C7FE8`: 8 accesses, 3 writers~~, and no consumer established here~~ *(answered: the intervention camera's subject, read by the focus update `00358EE0` at `00358F1C` / `00358F2F` — active-party-reserve-and-the-moment-the-leader-changes.md §8b; 2026-10-02, OPUS)*.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| PF-1 — 18/3/15, and the two unlisted sites | every rip-relative access to all four globals enumerated by **two instruments**, with the unlisted `003594C0` pair as the **control** — an instrument that cannot see it is wrong about kind 2, and `linear-only = 0` on the other three globals shows the gap is specific | 1 |
| PF-2 — disjointness, and no escape | the 18 sites and the 25 caller functions compared as sets; **zero** `lea` into the global and **zero** stored occurrences of its address image-wide | 1 |
| PF-3 — the one collapsing caller | `0050C646`/`0050C64B` read in order; `0050C610` identified as `debug_setpc` from the verb table | 1 |
| PF-4, PF-5 — the branch and the order | `00358BE4`, `00358C24`–`00358C52` read as a single instruction sequence | 1 |
| PF-6 — one call, and the verb | both thunks disassembled in full; `0025A800` the flag's **only** test in `0025A6A0`; `0034ED30` swept image-wide for stored pointers — **exactly one**, at `01EF17C0` | 1 |
| PF-7 — the mask arithmetic | `0023B166`/`0023B173` read at their instructions and the two constants XORed | 1 |
| PF-8 — three loads, two checks | `0023B0A2`/`0023B0AB`, `0023B152`/`0023B15E`, `0023B196`/`0023B19D` read in order | 1 |
| the roster/reserve split and the five maps | [the leader-change page](active-party-reserve-and-the-moment-the-leader-changes.md) §§2–3, not re-derived here | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on PF-1 through PF-8. **PF-3 and PF-4 are the two
that a port gets wrong by being tidy**: making the leader change synchronous is the obvious design and
is what the engine does only under a debug verb, and early-returning when the handle has not changed
drops a push the original always performs.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Party — internal.** The focus block and its five operations are this category's own.
- **Input — SERVICE, and it is PF-7's subject.** The suppression recompute publishes into the
  capability masks that layer owns; this contract states what it computes, not what consumes it.
- **ActorEntity — SERVICE.** The handle is resolved through the actor registry and the teardown
  addresses ~~the manager's record~~ camera context 0 *(corrected 2026-10-02, OPUS: `0025A6BE`, the `02097D20` contexts)*; PF-5 and PF-6 are about that seam.
- **Script_VM_Native_Bridge — SERVICE, and PF-3 and PF-6 are the statement.** Two operations here are
  reached only from verb table slots. *The table is cited; the verbs' own bodies are not read.*
- **CombatAction — MECHANICAL, and PF-8's note is its point.** Three fields are read here and written
  there; this contract asserts the sharing, not any behaviour of theirs.
- **CombatAI, Spawn_Encounter_Lifecycle, UI, Movement, Gameplay — MECHANICAL, and their presence IS
  PF-2's subject.** Each is reached only as a *caller of the leader getter*: they ask who the leader
  is and are handed a derived answer. **That fan-in — 28 sites in 25 functions across six owner
  categories — is the finding**, and it is why this contract exists at subsystem scope rather than
  as five operation contracts. *No address is cited for any of them: the statement is made by the
  counts and the disjointness test, and naming a caller would import its edge set for nothing.*
- **CoreRuntimeScheduling — MECHANICAL.** Reached as callers of the commit thunk `00358BB0`; **when
  the commit runs is that layer's business and PF-5 asserts nothing about it.** ~~The leader-change~~
  ~~page leaves the frame position open and this contract does not close it.~~ *(answered: once a frame, from whichever of the three mode frame bodies runs — active-party-reserve-and-the-moment-the-leader-changes.md §9, 2026-09-18; the thunk `00358BB0` has seven callers; 2026-10-02, OPUS)*
- **Presentation — MECHANICAL.** Reached only as a *co-caller* of the teardown's two helpers
  `00259510` and `003D9B80`; those helpers are named in PF-6 and §14 and **their behaviour is
  explicitly unread here**, so this edge is not evidence that the focus path and the presentation
  path share anything but a callee.
- **Rewards_Progression_Economy — MECHANICAL**, through these bodies' own callees.
- **Every other layer reached is MECHANICAL**, through these bodies' own callees. *Their addresses
  are deliberately not cited: each is a hub, and naming one imports its whole edge set.*

## 17. Related

- [Active party, reserve, and the moment the leader changes](active-party-reserve-and-the-moment-the-leader-changes.md) — the mechanism
- [Party roster and control suppression](party-roster-and-control-suppression.md) — PF-7's page
- [Contract — party slot assignment](CONTRACT-party-slot-assignment.md) — S-28's contracted quarter
- [Contract — combo continuation](../07-Combat-Action/CONTRACT-combo-continuation.md) — PF-8's owner

`0025A680` (11 B) is the flag-set entry the focus path uses - `r8d = 1` then a straight `jmp 0025A6A0`, the shared body called with the slot flag raised.

Interior anchor `0025A686` (function `0025A680`).

`0025A280` (61 B) is the slot write `002628B0` and `00359410` call: `ecx` x 0x110 indexes `02097300`, `dword[+0xF4]` is compare-stored with `edx`, and on a change `edx` x 0x860's row in `02098574` is zeroed - the dirty-clearing state write (whose caller `002628B0`'s far-end callees are Audio-side crossings, named at subsystem level, not by address).

Interior anchor `0025A29B` (function `0025A280`).

`0025A180` (243 B) is the record install `0025A6A0` and `00358F90` call: `edx` x 0x860 indexes `02097D20`, `[rcx+0xC0]`'s `+0x138` source is eleven-`movups` copied into `rbx+0x7A0`, `00259510(rbx+0x640, rbx+0x6F0, rbx+0x7A0, [rbx+0x850])` blends it in, `word[+0x690]` becomes 4 - the slot's pose install.

Interior anchor `0025A25C` (function `0025A180`).

`00259800` (25 B) is the single-slot reset `00358BC0`/`003593A0`/`00359410` call - `ecx` x 0x860's `02098574` row is zeroed, the same table `0025A280` clears on change.

Interior anchor `00259811` (function `00259800`).

`00259510` (270 B) is the blend `0025A180`/`00259B30`/`0025A6A0` call: `00861F02` on `rdx` and `rdi`'s `+0x10`/`+0x18` pairs, `003A1C50` wraps the delta, `rbx*(1-t) + rdi*t` writes `rsi`'s first three lanes with `+0xC` = 1.0, then `003A1C50`/`00861F08`/`00861F0E` finish the tail lanes - the family's spherical interpolate.

Interior anchor `0025956E` (function `00259510`).

`00259470` (149 B) is the `0x860`-byte state save `00359410` runs: sixteen `0x80`-block `movups` iterations copy `02098580 -> 02097D20` plus a `0x60` tail - the roster state bank's push direction.

Interior anchor `002594A8` (function `00259470`).

`002593D0` (149 B) is the same copy reversed - `02097D20 -> 02098580`, sixteen `0x80` blocks plus the `0x60` tail - the restore arm the same `00359410` driver pairs with the save.

Interior anchor `0025940C` (function `002593D0`).

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **ActorEntity - CLIENT and SERVICE (25 edges).** `0023B040`, `0025A280` are also called by bodies filed to ActorEntity: `00300FC0`, `002628B0`; `0023B040`, `002628B0` reach bodies filed to ActorEntity: `0031B770`, `0025B070` - shared machinery across the layer boundary, no shared ownership.
- **Audio - CLIENT and SERVICE (5 edges).** `003A1C50` is also called by bodies filed to audio: `00361810`; `002628B0` reaches bodies filed to audio: `00360B50`, `00360DD0`, `003636A0` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT (1 edge).** `003272A0` is also called by bodies filed to combat AI: `00301AD0` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT and SERVICE (4 edges).** `00358BB0` is also called by bodies filed to core runtime: `0022A770`, `0022B8C0`, `0022BC20`; `002628B0` reaches bodies filed to core runtime: `00229EE0` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT (1 edge).** `003272A0` is also called by bodies filed to Gameplay: `00312B40` (CombatAction) - shared machinery across the layer boundary, no shared ownership.
- **Input - SERVICE (1 edge).** `002628B0` reaches bodies filed to input: `0035B5D0` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (28 edges).** `0023B040` is also called by bodies filed to movement: `00234520`; `00259B30`, `002628B0` reach bodies filed to movement: `00380D30`, `00263560`, `0026A1D0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT and SERVICE (8 edges).** `00259510`, `00259B30` are also called by bodies filed to presentation: `00259B30` (CameraSystem), `00259E90`; `002628B0` reaches bodies filed to presentation: `002E65A0` (CharacterRender), `002E8CC0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (1 edge).** `002628B0` reaches bodies filed to resource: `0032E520` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - SERVICE (1 edge).** `002628B0` reaches bodies filed to save/load/settings: `002EF2B0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (9 edges).** `003A1C50` is also called by bodies filed to script VM / native bridge: `00341AB0`, `0034BE50`, `0034CD60` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT (2 edges).** `003272A0` is also called by bodies filed to spawn/encounter lifecycle: `00234AF0`, `002350C0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (1 edge).** `003272A0` is also called by bodies filed to UI: `00318CD0` (BattleMenu) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (10 edges).** `0023B040` is also called by bodies filed to WorldAreaField (world area): `00234590`; `0023B040`, `00259B30`, `002628B0` reach bodies filed to WorldAreaField (world area): `00313F60`, `00377A90`, `00378230` - shared machinery across the layer boundary, no shared ownership.

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives, and both instruments reproduce

**Attack.** PF-1 to PF-8, §2's sizes, §10's two early returns and §14's secondary-handle count became checks. PF-1's
second instrument was rebuilt independently: every 4-byte window of `.text` whose RIP-relative target is a focus global,
confirmed by decoding the instruction that ends there. Script: `Tools/analysis-kit/gfz-scripts/falsify_party_focus.py`,
output `falsify_party_focus.out`, image `73461d08…`, 0 BROKEN. PF-4's and PF-5's executed behaviour is EXP-051's and is
not repeated.

| # | Clause attacked | Result |
|---|---|---|
| F1 | PF-1 | **survives**: 18 accesses to `022C7FE0` on both instruments, writers `00358B6B`/`00358C2F`/`003590FD`; `022C7FF8` 5 bounded against 7 linear, the extra two `003594C0`/~~`003594D4`~~`003594D3` *(corrected 2026-10-02, OPUS: the store begins at `003594D3`)*; linear-only 0 on the other three globals |
| F2 | PF-2 | **survives**: the 18 sites lie in `00358A24`–`00359481`; 28 getter call sites in 25 functions, none in that span; no `lea`, and no stored copy of the address |
| F3 | PF-3 | **survives**: thunk `00358BB0` (5 B) has 7 callers. The requester has 3: calls at `00269D34` and `0050C646`, and the tail-jump `003265F6`. Only `0050C610` calls both |
| F4 | PF-4, PF-5, §10 | **survives**: `00358BE4 je 0x358c2f`, then re-read, store, kind clear, resolve (`call 003588B0`), `jmp 0x2681d0`; both early returns go to `00358C57` |
| F5 | PF-6 | **survives**: thunks `r8d = 1`/`0`. The flag is held in `r14d` and tested only at `0025A800`, before `003D9B80`. The alternate path is taken on `test ebx, ebx` or `cmp kind, 2`. `0034ED30` has no caller and is stored once, at `01EF17C0` |
| F6 | PF-7 | **survives**: `0x80000003` at both entry tests; `0x8800403B`/`0x8800003B`, XOR `0x4000` |
| F7 | PF-8 | **survives**: three `+0x698` loads, two tested; only `mov ecx, ebx; or ecx, 5` separates the middle load from `0023B15E`; `+0x714` is compared with `0x21E` through `eax` (`0023B138`) |
| F8 | §14 | **survives**: `022C7FE8` has 8 accesses, 3 writers |

No correction.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../_index/candidates/fable-contract-party-focus-and-control-suppres-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `003593A0` | 97 B | reads dword `022C7FEC`; when it is 0 and `ecx` is non-zero, calls `0026D6D0` on `003588B0(dword 022C7FE0)` when that is non-null and re-reads `022C7FEC`; then, when the (re-read) dword is non-zero and differs from `ecx`, calls `0026D6D0` on `003588B0(that dword)` when non-null and then `00259800(0)`; on every path finally stores the incoming `ecx` at dword `022C7FEC` | `003593BC`, `003593C9`, `003593D4`, `003593F0`, `003593F5` |
