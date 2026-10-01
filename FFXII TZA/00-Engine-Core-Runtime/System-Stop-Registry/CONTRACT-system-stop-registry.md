---
contract: Stop parts of the world for a while — twenty-eight requests intersected into one permission mask, applied once per dirty frame
category: 00-Engine-Core-Runtime
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md
entries: ["00226280", "00226BE0", "00225CD0", "00226640", "00227680"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — the apply step's combine loop disassembled and its cursor arithmetic reduced to
    a slot count and both record bases, every branch of its fade selection traced to which stores it
    reaches, the whole body swept for a read of the active bitset as the **control** on SS-1, the
    dirty byte's test and clear located, and the manager-breadth expression decoded from its four
    instructions. **This records checks performed on that date, not the method of the original
    derivation**, which is on the registry page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-system-stop-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the system stop registry

> **Authored 2026-09-22 by FABLE.** S-02's binding gap leaves two of its three pages uncontracted —
> its one contract, [`../CONTRACT-per-frame-update-gate.md`](../CONTRACT-per-frame-update-gate.md),
> covers the per-frame update gate. **This takes the time stop and the system stop registry**; the
> world tick and field frame remains uncontracted and this document does not claim it.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is seven
> such invariants — and **SS-1 and SS-6 are the two that make starting a request and applying it
> separate operations with a contract between them.**

## 1. Purpose

Let twenty-eight different parts of the game each ask for the world to hold still, and work out what
that means together.

## 2. Interface

| | body | role |
|---|---|---|
| **apply** | `00226280`, 952 B | intersects all 28 slots and drives everything (SS-1) |
| start a request | `00226BE0`, 1,936 B | builds the records, marks every actor, raises dirty |
| cancel | `00225CD0` | writes all-ones back — which is how the apply learns (SS-1) |
| build one id's records | `00227680` | a 28-case switch |
| the per-actor pass | `00226640` | folds seven pending pairs into seven live sets |

## 3. Types

```
28 slots, stride 0x18, walked 01FD4410 .. 01FD46B0   (the cursor's own bounds, SS-3)
  record A      01FD4160 + id*0x18       first qword = the permission mask that is ANDed
  record B      01FD4400 + id*0x18       first qword likewise
  record B +0x10  i32                    this request's fade length; -1 = none (SS-4) -- but 0 at process start, see note

01FD46D4  u32   the active-request bitset  -- NOT read by the apply step (SS-1)
01FD46D0  u8    the dirty byte             -- the only start-to-apply coupling (SS-6)
01FD46A0..01FD46C8   the combined masks and fade the last apply computed
```

## 4. Preconditions · postconditions · invariants

### The seven cross-operation invariants

**SS-1 — The combined restriction is an AND over ALL TWENTY-EIGHT slots, and the active-request
bitset is never consulted.** The loop walks `01FD4410` to `01FD46B0` in steps of `0x18` — **28
slots** — ANDing record A (`002262E4`, at cursor `− 0x2B0` = `01FD4160`) and record B (`002262EB`,
at cursor `− 0x10` = `01FD4400`) into two accumulators that begin as all-ones (`002262BA`,
`002262C2`). **`01FD46D4` is read zero times in the whole 952-byte body.**

> *So "active" has two representations and the apply trusts only one of them.* A slot is inert
> because its record holds all-ones — the identity of the AND — not because its bit is clear. **That
> is why cancelling must write all-ones back** (`00225CD0`): a cancel that only cleared the bitset
> would leave a restriction in force that nothing in the bitset shows. The control for this claim is
> the sweep itself: an apply that consulted the bitset would have to read that address, and it does
> not.

**SS-2 — A SET bit is an EXEMPTION, not a restriction.** Throughout the records: record A bit `c`
exempts category `c` from set 1, record B bit `c` from set 4, and so on. *The natural reading — a
bit means "this is stopped" — is backwards, and inverts every one of the 28 records at once.*

**SS-3 — Only each record's FIRST qword takes part in the intersection.** The slot is `0x18` bytes;
the combine reads one qword from each record (`002262E4`, `002262EB`) and the `i32` fade at the
cursor. *The remainder of the slot is carried per request and never intersected, so a permission
expressed there would not compose.*

**SS-4 — The fade length is the MINIMUM over non-negative slots, and the one-shot reset is
conditional on being one of them.** `002262EE` loads the slot's fade; `002262F2 js` skips a negative
one entirely; the first non-negative is taken (`002262F8`) and later ones keep the smaller
(`002262FE cmovg`); then **`00226301` resets that slot to `-1`** — a store the `js` path never
reaches. *So the shortest fade any pending request asked for wins, and it is consumed: a second
apply in the same state fades over nothing.*

**The initial value is 0, not -1 — aligned 2026-09-25 (FABLE, Claude Opus 5.5), on `OPUS-NOTE-FABLE-SYSTEM-STOP-INIT-FADE-IS-ZERO`.**
The type block's "-1 = none" is the steady state, not the start state.
- **The initialiser does not write the fade.** `00226B30` walks both record arrays in one run (`01FD4160` to
  `01FD46A0`, 56 records). It writes only the first qword (`-1`, `00226B80`) and byte `+0x14` (`0`, `00226B87`),
  and never touches `+0x10`.
- **So the field holds its start-up value.** The records lie past `.data`'s file-backed end (`01F7E400`), so every
  record B fade is **0** when the process starts.
- **What the first apply does with that.** It finds 28 non-negative slots. It takes the minimum, **0**, as the
  frame's fade, and resets every slot to `-1` (`00226301`). From then on a slot is `-1` until a start writes a
  request's length into it (`00226C4B`).
- **The combined fade is different.** Its last-computed value (`01FD46B0` / `01FD46C8`) is set to `-1` by the
  initialiser itself (`00226B6D`).

*Not read here:* whether a 0-length fade behaves differently from none for the consumer of the combined value.
Static; the initialiser's body was read in full.

**SS-5 — Bit 41 is OR-ed into EVERY slot's record B on EVERY apply, unconditionally.**
`00226307 or r8, r10` with `r10 = 0x20000000000` is reached both by falling through the fade path
and by the `js` that skips it, and the loop covers all 28 slots. *So bit 41 does not mark "this
request had a fade"; it marks "this slot has been through an apply" — and after the first apply
every slot carries it, including the twenty-odd that were never started.*

**SS-6 — The dirty byte is the ONLY coupling between starting a request and applying it.** A start
sets the id's bit (`00226C7A`) and raises dirty (`00226C87`); the apply refuses to run when it is
clear (`00226287`) and clears it at the end (`0022660A`). *So a start changes the registry and stops
nothing by itself. Most wrappers tail-jump to the apply; one that did not would leave the world
running with a request recorded, until some unrelated start or cancel dirtied the registry again.*

**SS-7 — How many actor managers a request reaches is a BIT IN ITS OWN RECORD.**
`00226C77`–`00226C91` computes `(~(A >> 30) & 2) | 1` from record A's low dword — **3 managers when
bit 31 is clear, 1 when it is set.** *The breadth of a stop is authored per request alongside its
permissions, not derived from what it stops.*

## 5. State

**Owned:** the 28 slots, the active bitset, the dirty byte and the combined result. **Written per
actor:** the seven pending-set / pending-clear word pairs, folded into seven live sets by the
per-actor pass. **Read, never written:** the party roster and focus, consulted to resolve the
exemption categories.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`../CONTRACT-per-frame-update-gate.md`](../CONTRACT-per-frame-update-gate.md) — S-02's contracted third |
| **Uncontracted** | the world tick and field frame — S-02's remaining page, not claimed here |
| **Exempts by** | the party focus handle and the roster slots — [the focus contract](../../11-Party/CONTRACT-party-focus-and-control-suppression.md) supplies category 0's answer |
| **Drives** | movement, script execution, presentation visibility and a character fade, through the seven live sets |

## 7. State transitions

*start (records built, actors marked, exemptions cleared, bit set, dirty raised) → apply (intersect
28 slots, choose the minimum fade, consume it, drive the per-actor and global effects, clear dirty)
→ cancel (all-ones written back, bit cleared, dirty raised).* A slot transitions
`inert → restricting → inert` only through those writes, never through the bitset alone (SS-1).

## 8. Script · resource · event interactions

The 28 permission records are built in code, by a 28-case switch, not loaded from data. Which ids
scripts raise is on [the page](the-time-stop-and-system-stop-registry.md) §6 and is not re-derived
here.

## 9. Determinism

Deterministic. No generator is drawn. *But not idempotent*: SS-4's fade and SS-5's bit 41 both make
a second apply differ from the first in the same state.

## 10. Failure paths and edge conditions

- A start for an id whose bit is already set is **refused** (`00226C08`), so a request cannot be
  raised twice.
- An apply with nothing dirty returns immediately and leaves the previous combined mask standing
  (SS-6).
- Every slot's fade is `-1` after the first apply that consumed it, so a fade is available exactly
  once per start (SS-4).

## 11. Observable behaviour

When a cutscene or a summon stops the world, the party's leader often keeps moving and the rest
freeze — that is SS-2's per-category exemptions, decided per request.

## 12. Reproduction formula

Sweep the apply body for a read of `01FD46D4` and assert **none** (SS-1). Cancel a request by
clearing only its bit, leaving its record, and assert the restriction persists. Give two pending
requests fades of 30 and 10 and assert the apply uses **10**, then re-apply in the same state and
assert **no fade** (SS-4). Read record B of a never-started slot after one apply and assert bit 41
is set (SS-5). Set record A bit 31 and assert one manager is walked instead of three (SS-7).

## 13. Runtime validation

**EXP-191** ([record](../../_experiments/EXP-191-s02-world-tick-stop-registry-exec.md) ·
[harness](../../_experiments/evidence/s02-world-tick-stop-registry-exec/check.py) · 37/37, stable ×3)
executes `00226B30`/`00225CD0`/`00225EB0`/`00226280` as shipped bytes under Unicorn with disclosed
synthetic registry contents — NATIVE-REPLAY, `live_game: false`. (The earlier
[probe](../../_experiments/evidence/stop-registry-permission-records/probe.py) remains §3.1
evidence, separate.)

- **SS-1 executed — twice**: a `UC_HOOK_MEM_READ` watch on `01FD46D4` records **zero** reads for
  the entire apply body, and bitset `0` vs `0xFFFFFFFF` produce identical combined masks/fade
  (`ss-apply-bitset-invariance`). The combined result is the AND over all 28 slots.
- **SS-2 executed**: all-ones banks → combined `~0`; any zero lane → 0 (`ss-apply-full`).
- **SS-3 executed**: the cursor's own bounds `01FD4410..01FD46B0` stride `0x18`; only each record's
  first qword enters the intersection.
- **SS-4 executed**: fades `0x55`/`0x30` → callee `226640` receives `edx=0x30`; every consumed
  slot's `d10` is reset to `-1` in the same pass (`-1` slots skipped by `js`).
- **SS-5 executed**: `q[recB] |= bit41` writeback on every apply, unconditionally.
- **SS-6 executed**: `b[01FD46D0]==0` → immediate `ret`, zero calls/writes; start `00225CD0` and
  stop-sweep `00225EB0` both set it. Note: `00225CD0` also **clears** the request's bitset bit and
  stamps `recB d10=fade`; `00225EB0` sweeps only *set* bits, resetting records (`q0=-1`,
  `d10=-1`) + idx dispatch (`0`→`2DDC30`/`182DA0`, `0xC`→`182D60`, `0xD`→clears recB bit41 then
  `182D40`, `0xF`→`182D40`).
- **SS-7 partial**: the start/stop fan-out walks all 3 manager slots (gate `b[obj+0x10]&1`, rows
  via `358940`); the per-request reach bit was not isolated — the all-28 AND covers the apply side.
- Correction on record: `263FF0` resolves the manager slot array at **`02098E10`** (stride `0x288`),
  not `0208E688`.

## 14. Unresolved

- ~~Why bit 41 is set on slots that were never started (SS-5) — a marker whose reader is not
  established here.~~ **CLOSED 2026-09-23 (SWE2-CONTRACT): the reader is the apply's own tail.**
  `002264D8` tests `0x20000000000` against the accumulated all-slots AND — set → `ebp = 0`,
  clear → `or` it in and `ebp = 1`, feeding the `002DF370` calls at `0022651F`/`00226560`/
  `0022659C`. Since the reset clears bit 41 on **slot 13 only** (`0022603A`,
  `and [recB], ~0x20000000000`) while the apply re-sets it on all 28, bit 41 in the
  accumulated mask means "every slot has been through an apply since the last reset" — the
  tail's `ebp` is a **first-apply-after-reset flag**, not a per-request marker.
- ~~Whether any wrapper starts a request without reaching the apply (SS-6).~~ **CLOSED
  2026-09-23 (SWE2-CONTRACT): yes — at least ten.** The apply `00226280` has exactly 25
  call/jmp edges, all synchronous wrappers — **no frame poll exists** (`00226BE0`'s own tail
  never calls it). Start-only bodies that return with dirty raised: `002273B0`, `002273E0`,
  `002274A0`, `002274E0`, `00227610`, `0026B980` (start-B), `00252D90`, `002544C0`,
  `002630FD`, `00313EB1` (start-A), `0026326C` (start-B mid-body); none of their callers apply
  either. *SS-6's stated hazard is real: a start-only path leaves the request recorded and
  dirty until the next combined wrapper runs.* (`00227640` looks like a start-only wrapper but
  is a helper — both its callers `0026C527`/`0026C7D2` apply immediately after.)
- ~~What the rest of each `0x18` slot carries, given SS-3 shows it is never intersected.~~
  **PARTIAL 2026-09-23 (SWE2-CONTRACT):** observed fields beyond `+0x00` are **`+0x10` dword —
  the fade duration** (written at start `00226C4B` from the wrapper's stack arg, reset to `-1`,
  read-and-consumed by the apply at `002262EE`) and **`+0x14` byte — zeroed** at start/reset in
  both records (`00225E30`/`00226003`/`00226008`). The remaining bytes — `+0x08` qword and
  `+0x15`–`+0x17` — are still unobserved.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| SS-1 — 28 slots, both bases, and the unread bitset | the cursor's bounds and stride reduced arithmetically to **28** and to `01FD4160` / `01FD4400`; the 952-byte body swept for `01FD46D4` — **zero hits**, which is the control | 1 |
| SS-3 — one qword each | `002262E4` and `002262EB` are the loop's only record reads | 1 |
| SS-4 — minimum, and the conditional reset | `002262EE`–`00226301` traced branch by branch, with the `js` at `002262F2` shown to bypass the reset store | 1 |
| SS-5 — unconditional bit 41 | `00226307` reached from both the fade path and the `js` skip; `0x20000000000` resolved to bit 41 | 1 |
| SS-6 — the only coupling | `00226C7A`/`00226C87` against `00226287`/`0022660A` | 1 |
| SS-7 — the breadth bit | `00226C77`–`00226C91` decoded, including the zero-extension that makes `shr rax, 0x1e` read bits 30–31 | 1 |
| SS-2, and the seven live sets | [the registry page](the-time-stop-and-system-stop-registry.md) §§3–5, falsified 2026-09-12 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on SS-1 through SS-7. **SS-1 is the one that
decides whether the port is correct at all**: keying the combined mask off the active bitset is the
obvious design, it agrees with the original in every ordinary case, and it diverges exactly when a
record is left restricting after its bit is cleared — which is the state the cancel path exists to
prevent. **SS-2's polarity** is the one that will be inverted, and it inverts all 28 records at once.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **CoreRuntimeScheduling — internal.** The registry, the apply step and the per-actor pass are this
  category's own.
- **ActorEntity — SERVICE, and SS-7 is about it.** The start walks one or three actor managers and
  marks every actor's pending words; this contract asserts **how many managers and which words**,
  not the managers' own behaviour.
- **Party — SERVICE.** Exemption categories 0 and 1 are resolved by asking for the focus handle and
  the roster slots. *That is a consumer relationship with
  [the focus contract](../../11-Party/CONTRACT-party-focus-and-control-suppression.md); this
  contract asserts that the answer is asked for, not how it is derived.*
- **Movement, Presentation, Audio, Script_VM_Native_Bridge — MECHANICAL, and their presence is
  the point of the seven live sets.** Each is driven by one combined bit or one live set; **what
  each of them then does is its own**, and the page tabulates the consumers this contract does not
  re-derive.
- **InputGameplay — MECHANICAL, on two unrelated edges.** The cancel path makes per-id side calls
  into that layer, and the apply's bit-pair write that the page reads as a UI effect resolves to an
  **owner in that layer, not UI** — a correction to my own first draft of this paragraph, which
  said UI. *This contract asserts that the apply drives one bit pair from one combined bit and that
  the cancel dispatches per id; neither callee is read here and the page does not tabulate the
  cancel's id dispatch either.*
- **CombatAction — MECHANICAL.** One body in that layer calls the start, the cancel and the apply
  all three. **That is a caller relationship**: it raises and drops stops like any other requester,
  and this contract asserts nothing about which id it uses or why.
- **Every other layer reached is MECHANICAL**, through these bodies' own callees. *Their addresses
  are deliberately not cited: each is a hub, and naming one imports its whole edge set.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document, so words like *party*, *movement* and *audio* in
> ordinary prose can clear a layer nothing here dispositions — the defect measured in
> `_index/candidates/fable-crossings-prose-false-clears.tsv`. The paragraphs above are what
> discharge these, not those words.

## 17. Related

- [The time stop and the system stop registry](the-time-stop-and-system-stop-registry.md) — the mechanism
- [Contract — the per-frame update gate](../CONTRACT-per-frame-update-gate.md) — S-02's contracted third
- [Contract — the party focus and control suppression](../../11-Party/CONTRACT-party-focus-and-control-suppression.md) — category 0's supplier

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** SS-1 to SS-7 and SS-4's initial-value note became checks at their instructions. Script:
`Tools/analysis-kit/gfz-scripts/falsify_system_stop.py`, output `falsify_system_stop.out`, image `73461d08…`, 0 BROKEN.

| # | Clause attacked | Result |
|---|---|---|
| R0 | §2 sizes | **survives**: 952 / 1,936 B |
| R1 | SS-1 / SS-3 | **survives**: two all-ones accumulators; 28 slots from `01FD4410` to `01FD46B0`, record A at `cursor − 0x2B0`, record B at `cursor − 0x10`; `01FD46D4` has **zero** references in the apply |
| R2 | SS-4 | **survives**: `js` over a negative fade, the first non-negative taken, `cmovg` keeps the smaller, `mov [rax], -1` on that path only |
| R3 | SS-5 | **survives**: `or r8, r10` (bit 41) and the store back, on both paths |
| R4 | SS-6 | **survives**: the apply exits on a clear `01FD46D0` and clears it at `0022660A`; a start ORs `01FD46D4` and sets `01FD46D0` |
| R5 | SS-7 | **survives**: `(~(A >> 30) & 2) | 1` |
| R6 | SS-4's initial-value note | **survives**: `00226B30`'s inner loop never resets `rax`, so two outer passes cover all 56 records. Each gets `-1` in its first qword and `0` at `+0x14`, and `+0x10` is untouched. The combined fades at `01FD46B0` and `01FD46C8` are set to `-1` |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. §16a above states the same classes in prose under a numbered heading, which the crossings gate does not read; this section names the edges.*

**ActorEntity — SERVICE, CLIENT (23 edges).** The start `00226BE0`, the cancel `00225CD0`, the area-unload sweep `00225EB0` and the per-actor pass `00226640` each call the slot-block getter `00263FF0`, `ActorManager_GetRecordByOrdinal` (`00358940`) and `00359B80` (which follows an entry's `+0x30` pointer and tail-jumps on); the start and the per-actor pass also call `ActorHandle_ResolveRegistryEntryByPackedId` (`003588B0`), and the per-actor pass calls `00238B40` and `00312130`, the hooks that set the battle unit's stop flag word and flag bit 36 (live sets 6 and 7); in the other direction `00263230` (an event script taking an actor) calls the start, the entry removal `00263050` calls the cancel, the unload `002628B0` calls the sweep, and `00263660` and `0026C5D0` call the apply `00226280` and the wrapper `00227640`. A request walks one or three actor managers and marks each actor (SS-7), and the actor layer raises and drops id 6 around event scripts and runs the apply; this contract asserts which managers and words, not the actor layer's behaviour.

**Audio — SERVICE, CLIENT (4 edges).** The apply `00226280` calls `002DF370`, the audio group-mask setter, which calls `001DBA90` and is also called by `00229AB0` and `00229AF0`. A combined bit of the stop drives one audio group mask through the same setter other audio code uses; what the mask silences is the audio layer's.

**CombatAction — CLIENT (3 edges).** `00313DB0` calls the start `00226BE0`, the cancel `00225CD0` and the apply `00226280`. One action-layer body raises, drops and applies a stop like any requester; this contract asserts nothing about which id it uses or why.

**Input — SERVICE, CLIENT (19 edges).** The census files the start `00226BE0` to the input layer (its code domain is the input layer's actor mask propagation runtime), so the calls into it from the start wrappers `002273B0` (id 11), `002273E0`, `002274A0`, `002274E0`, `00227610` and `00227640` and from `talkfadeout` (`0026B980`) count here, as does its call of the record builder `00227680`; the cancel `00225CD0` and the sweep `00225EB0` call `00182D40`, `00182D60` and `00182DA0`, and the builder `00227680` calls `00182CD0`, `00182CF0` and `00182D10` - each a 21-byte thunk that fetches the input manager singleton and tail-jumps into one of its methods; and the apply `00226280` calls `0035B4B0` and `0035B510`, the bit pair that marks entries of an input-owned table (`0035B4B0` ORs its argument into a mask word and promotes each matching entry's state byte from 2 to 3). The registry's entry points sit in the input layer's census family and its records adjust input-manager state per id; the invariants here are about the registry's own words, not those input methods.

**Movement — CLIENT, SERVICE (6 edges).** `0026A1D0` calls the start, the cancel and the apply; `0026C3E0` calls the apply and the wrapper `00227640`; and the per-actor pass `00226640` calls `Actor_StopRequestedMovement` (`0026D6D0`). Movement code raises and applies stops, and a stopped actor's requested movement is halted from the live set; how movement then behaves is the movement pages'.

**Party — SERVICE (2 edges).** The start `00226BE0` calls `PartyRoster_GetActorBySlot` (`00263750`) and `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`). Exemption categories 0 and 1 are resolved by asking for the roster slots and the focus handle; the party layer's answer is consumed, not derived, here.

**Presentation — SERVICE (1 edge).** The apply `00226280` calls `CharacterRenderSystem_SetDistanceCullEnableByRequester` (`002EBBF0`). One combined bit toggles the character renderer's distance cull for the registry as a requester; the renderer's use of it is not claimed.

**SaveLoad — CLIENT (1 edge).** `00280140` calls `00252D90`, the UI close path, which maps the closing UI request through the UI-id map and cancels its stop with `00225CD0`. The save/load screen closes a UI request like any other screen, and the registry sees only the cancel.

**Script_VM_Native_Bridge — CLIENT (3 edges).** Script verbs `0034DC30` and `00343CE0` call the start wrappers `002273B0` and `00227610`, and `00345E50` calls `talkfadeout` (`0026B980`). Scripts raise stops through the per-id wrappers and the id-6 verb; which scripts raise which ids is the page's §6.

**UI — CLIENT (5 edges).** `00279E20`, `0035CF50`, `0035D6B0`, `003C8990` and `003C8B70` call the UI close path `00252D90`. Closing a UI request cancels the stop that its opening raised; the screens own the requests, the registry only the slots.

**World — CLIENT (3 edges).** `00266D10` calls the start `00226BE0`, the cancel `00225CD0` and the apply `00226280`. That world-layer body is one of the nine direct requesters the page counts, raising, dropping and applying stops itself.

**WorldAreaField — SERVICE (1 edge).** `talkfadeout` (`0026B980`) calls `00377700` when its second argument is negative; `00377700` reads bit 0 of the active field record's byte and one more field test, and the answer picks an argument of the id-6 start. The field record decides one parameter of that request; the registry stores it like any other.
