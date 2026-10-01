---
contract: take a collision body from a fixed pool of 128, or quietly do without one
category: 06-Movement-And-Navigation
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md
entries: ["003DA8A0", "003DAD00", "002E3500", "00269EC0", "002681D0", "002682D0",
          "002685F0", "00268380"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 46 addresses cited - 3 data, 9 entry, 33 interior, 1 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-body-pool-pass-1     # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the movement body pool

128 collision bodies, one free list, and **an allocator that returns NULL without saying so**. What
saves this from being a crash is that every consumer in the creation sequence re-loads the chain and
guards each hop — so the 129th actor does not fault, it simply has no body and stops colliding.

That is the contract: **exhaustion is a silent behavioural change, not a failure.**

## 1. Purpose

To state what a caller owes, what the pool guarantees, and what happens when it runs out — because
the page this implements establishes the mechanism and the lifetime, and a reimplementer also needs
to know that the failure is invisible.

## 2. Interface

| | |
|---|---|
| allocate | `003DA8A0` — no arguments, returns the body or **NULL** |
| release | `003DAD00` — the body |
| create for a record | `002E3500` — `rcx` = the `ActorStorageRecord` |

## 3. Types

| | |
|---|---|
| the body array | `0x02B4E4C0`, **128 entries of `0x130`** |
| the free head | `0x02B57CC4`, a `u16`; `0xFFFF` is null |
| the link fields | entry `+0` prev, `+2` next, `+4` own index |
| where a body is held | `secondaryContext + 0x138` |

**The count is confirmed by the layout, not assumed.** `0x02B4E4C0 + 128 × 0x130 = 0x02B57CC0`, and
the free head sits at `0x02B57CC4` — four bytes past the end of the array. The stride comes from
`imul rdi, rax, 0x130` at `003DA8D8`.

## 4. Preconditions · postconditions · invariants

**Precondition of `002E3500`: the record must have a secondary context.** It loads `record + 0xC0`
and returns immediately if it is NULL (`002E3506`–`002E3513`). By
`CONTRACT-actor-record-pool-and-region-map`, `+0xC0` is planted by only **one** of the region map's
four arms, so **records of the other three layouts can never have a collision body at all** — and
that is a layout fact, not a runtime one.

**Invariant: at most one body per record.** `002E3500` releases any existing body and clears
`+0x138` before allocating (`002E3515`–`002E352D`), so create is idempotent in the sense that
matters: calling it twice leaves one body, not two.

**Postcondition:** `+0x138` holds the allocation's result — **whatever it is**, including NULL.

## 4a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED

**The central claim of this contract is a universal** — *every* consumer re-loads the chain and
guards each hop — and a universal is the most attackable thing a document can say. It was attacked
by walking the creation sequence at `002E3500` and reading each callee's first dereference.

| claim | the killer | what the binary says |
|---|---|---|
| the allocator returns **NULL** on exhaustion, silently | it faults, returns a sentinel, or sets a flag on the way out | **holds.** `003DA8A6` reads the free head as a **word** from `02B57CC4`; `003DA8B5 cmp dx, r9w` against `0xFFFF` jumps to `003DA9DF`, which is `mov rax, rsi` — and `rsi` was zeroed at `003DA8AD`. Then `ret`. **No flag, no global, no other write.** `int3` padding begins at `003DA9E8`, confirming the 328-byte extent |
| the pool is 128 × `0x130` at `02B4E4C0` | the arithmetic does not land on the free head | **holds.** `0x02B4E4C0 + 128 × 0x130 = 0x02B57CC0`, and the head is four bytes past at `0x02B57CC4`. The base is `003DA8C2 lea r10, [rip → 02B4E4C0]` and the stride `003DA8D8 imul rdi, rax, 0x130`, both as cited |
| the `+0xC0` precondition | the test is on another field, or it continues past it | **holds** at exactly `002E3506`–`002E3513` |
| create releases any existing body first | it leaks, or clears before releasing | **holds** at exactly `002E3515`–`002E352D`: release, **re-load `+0xC0`**, then store `0` |
| `+0x138` holds the result **whatever it is** | the result is tested before the store | **holds.** `002E3538 call 003DA8A0` then `002E3546 mov [rcx+0x138], rax` with **no test in between** |
| **every consumer guards each hop** | one of them dereferences `+0x138` without testing it | **holds for every consumer**, and the guards are explicit: `00269EC0` tests `+0xC0` then `+0x138`; `002682D0` tests `rcx`, `+0xC0`, `+0x138` *and* `+0x30`; `002685F0` tests both and substitutes `xorps xmm0, xmm0` on the miss; `00268380` tests both at `002683AD`/`002683BD` |

### Two things the pass added

**1. There are FIVE consumers, not four.** `002E3558 call 002681D0` sits between `00269EC0` and
`002682D0`, and `002681D0` was **absent from `entries` and unmentioned anywhere in this document**.
It is ten bytes — `test rcx, rcx / jne / ret` — tail-jumping to a body that re-loads `+0xC0` and
tests it. **The omission hid evidence *for* this contract's central claim, not against it**, which is
the easiest kind of gap to leave and the least likely to be noticed. It is now in `entries`.

**2. "Guards each hop" is exact for the first dereference and generous for the rest.** `00268380`
tests `+0xC0` and `+0x138` at `002683AD`–`002683C7`, and then **re-loads both three more times —
`002684BB`/`002684C5`, `002684D1`/`002684DB`, `002684E7` — without re-testing**. That is safe: every
path into those loads passes the earlier `je 0x26851E`, and the only branch from before it,
`00268391 jne 0x2683AD`, lands *on* the guard. So they are **dominated, not re-guarded**, and a
reimplementation that re-tested each time would be correct but would not be this code.

> **What was tried and did not break it:** every stated body size re-checked against the current
> census (**no drift**); a banned-evidence sweep for `.pdata`, `.xdata`, unwind, EH-map and
> IP-to-state (**nothing**); the pool arithmetic recomputed rather than accepted; and the allocator's
> extent confirmed from its `int3` padding rather than from the census alone.

> **Still unexecuted.** No pilot drives any of these eight functions, so this pass establishes that
> the document says what the instructions say — not that the instructions do what anyone expects.
> `crossref_clean` stays **false**: `audit_crossrefs.py` has not been run clean against this document
> and this pass did not do it.

## 5. State

The pool array, the free head, and one pointer per secondary context. Nothing else.

## 6. Relationships

- **Lifetime is the actor's presentation's.** The page establishes the two releasers and their
  reachability from the per-type presentation release and
  `ActorSystem_ReleaseManagerRecords`; a body lives exactly as long as its actor's presentation, and
  that account is cited rather than re-derived.
- **`00268380` sizes the shape only for kind 3** — `(record[+3] & 0xE0) == 0x60` at
  `00268386`–`00268391`, and `0x60 >> 5` is 3. Note this reads the **kind** nibble of
  `packedKindAndSequence` while the region map reads the **sequence** nibble of the same byte; they
  are different fields and a reconstruction must not conflate them.

## 7. State transitions

**Allocate**, `003DA8A0`:

```
esi = 0                                  003DA8AD
head = u16 [02B57CC4]                    003DA8A6
if (head == 0xFFFF) return rsi           003DA8B5-003DA8B9, and 003DA9DF: mov rax, rsi
entry = 02B4E4C0 + head * 0x130          003DA8D8
... unlink from the free list, link onto the live list, return the entry
```

**Create**, `002E3500`:

```
ctx = record[0xC0];  if (!ctx) return              002E3506-002E3513
if (ctx[0x138]) { release(ctx[0x138]); ctx[0x138] = 0; }   002E3515-002E352D
body = allocate()                                  002E3538
ctx[0x138] = body                                  002E3546   <- NO NULL TEST
layer(record, 0); flags(record); weight(record); shape(record)
```

## 8. Script · resource · event interactions

None. The radii, height and heading come from the secondary context and the character parameter
block, per the referenced page.

## 9. Determinism

Deterministic given the free list's order — and that order is **history-dependent**: the free head
is a LIFO, so which entry an actor receives depends on the order of every prior create and release.
A reconstruction that allocated lowest-index-first would be observationally different in any state
that can see a body's index.

## 10. Failure paths and edge conditions

**The allocator returns NULL on exhaustion and says nothing.** `esi` is zeroed at entry and the
exhausted path is `mov rax, rsi` (`003DA9DF`). There is no diagnostic, no counter and no flag.

**The creator stores that NULL without testing it** (`002E3546`).

**And then nothing crashes, because every consumer guards.** This was checked rather than assumed —
all four functions the creation sequence calls re-load the chain and test each hop:

| | |
|---|---|
| `00269EC0` | tests `+0xC0`, then `+0x138`, before `mov byte ptr [rax+6], dl` |
| `002682D0` | tests the record, `+0xC0` **and** `+0x138` — a three-level chain |
| `002685F0` | tests `+0xC0` twice, and substitutes `xorps xmm0, xmm0` when it is absent |
| `00268380` | gates on the kind nibble before reading `+0xB8` at all |

**So the 129th body is a behavioural change, not a fault:** that actor has no collision body and
drops out of the separation pass, silently, for as long as the pool stays full. **That is the single
most important thing in this contract for a reimplementer**, because a reimplementation that asserted
or threw on exhaustion would be louder than the original and one that skipped the guards would be a
crash the original does not have.

## 11. Observable behaviour

Not established. What would be observable: with 128 bodies live, a further actor passes through
others instead of separating from them.

## 12. Reproduction formula

```c
#define BODY_COUNT 128                     /* 02B4E4C0 + 128*0x130 == 02B57CC0, and the free */
                                           /* head lives at 02B57CC4, four bytes past it     */
Body *Body_Allocate(void)                  /* 003DA8A0 */
{
    uint16_t head = free_head;
    if (head == 0xFFFF) return NULL;       /* silent */
    Body *e = &bodies[head];
    /* unlink from free, link onto live */
    return e;
}

void Body_CreateFor(ActorStorageRecord *r) /* 002E3500 */
{
    SecondaryContext *c = r->secondaryContextPtr;
    if (!c) return;                        /* three of four layouts never get here */
    if (c->body) { Body_Release(c->body); c->body = NULL; }
    c->body = Body_Allocate();             /* stored even when NULL */
    SetLayer(r, 0); SetFlags(r); SetWeight(r); SizeShape(r);
}
```

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent.** (2026-09-12)

> **ADDED 2026-09-16 (OPUS) — and unlike the other three corrections made at this HEAD, THIS ONE
> CONTRADICTS NOTHING.** [`EXP-087`](../_experiments/EXP-087-movement-body-pool-guards.md)
> (SWE2-ORACLE, 2026-09-13, method B, isolated original-code under Unicorn against the shipping EXE)
> reports **49/49 cases pass, 9/9 byte-level mutants detected** over the creator `002E3500` and five
> consumers — `00269EC0`, `002681D0`/`002681E0`, `002682D0`, `002685F0`, `00268380`.
>
> **That is a different function set and a different method from the run recorded below**, which
> compares the allocator `003DA8A0` and the release `003DAD00` against a *reconstruction* through
> `diff_body_pool.py`. So EXP-087 is additive: it executes the guard surface this section does not
> cover, rather than refuting anything in it. Recorded because `check_experiments.py` listed it under
> **NOT CITED — a RUN experiment its contract never names**, and because saying which of the five
> back-links was merely missing matters as much as saying which four were hiding a false claim.
>
> **WHAT EXP-087 ESTABLISHED, consumed 2026-09-16 (OPUS) from SWE2-ORACLE's findings. Nothing here
> refutes this contract — every item either confirms a claim it already makes or measures something
> it left open, which is the rarer and less interesting outcome, and is therefore worth stating
> plainly rather than dressing up.**
>
> - **Exhaustion is quiet loss, end to end.** The allocator returns NULL, the creator stores it
>   **untested** at `actor+0x138`, and all five consumers then run with every write gated. With the
>   `edx == 0` predicate path armed the whole chain still executes: the predicates run and the stores
>   are suppressed. *Confirms* §7 rather than extending it.
> - **A released body is always the first recycled.** Release pushes its own index to the free head
>   and the very next allocation pops it straight back, with the slot zeroed in between at
>   `002E352D`. The contract said the free list has stack discipline; this says which body you get.
> - **The creator guards the actor and NOT the context.** `ctx+0xC0` is tested; `ctx` is not, so a
>   null context faults at virtual address `0xC0` — measured, not inferred.
> - **Consumer 2 is the only one guarding `rcx` at its own head**, and its `edx` dispatch on
>   `actor+0x152` is `{0: chain, 2: 3, 3: 5, else: 2}` with the non-zero arms skipping the predicate
>   chain entirely. Both its writes, `body+0x80` and `actor+0x153`, sit behind the single body-reload
>   guard.
> - **`002685F0`'s `xorps` zero-substitution on a null actor is DEAD** — the second test rejects
>   `rax` before any store can reach it. A path that exists in the bytes and cannot be taken.
> - **`00268380`'s chain reloads are dominated rather than re-tested**, which is what this contract
>   already claims; it is now executed rather than read.
> - **Measured interiors left open until now:** consumer 3 preserves `body+0x90`'s upper bits
>   (`0xCCCCCCC8 | (a151 & 3)`), and consumer 5's kind arms are kind 1 → `pb+0x68`/`pb+0x38` with rgb
>   defaults `0x25`/`0x32`/`0x25`, kind 3 → `pb+0xC0 * pb+0x24` / `pb+0xA8` with rgb from
>   `pb+0x104..106`, and zero for every other kind.
>
> **ONE FINDING IS NOT CONSUMED BECAUSE IT HAS NO TARGET HERE, and the check is recorded so nobody
> repeats it.** ORACLE's finding (7) corrects a codec/row table base to `02098E10`, *"NOT
> `02649E10`"*. **This contract never states that base**, and `02649E10` appears **nowhere in the
> database** — a DB-wide grep finds only `02098E10`, used consistently in eight places. The value
> ORACLE gives is right and OPUS verified it independently rather than taking the arithmetic on
> trust: `00263FF3 lea rcx, [rip + 0x1E34E16]` with rip after the instruction at `0x263FFA` gives
> `0x02098E10`, and the following `imul rax, rax, 0x288` matches the stated stride. So the correction
> is **already satisfied corpus-wide and targets nothing in this contract** — most likely it corrects
> ORACLE's own working note. Recorded rather than silently dropped, because a routed correction that
> turns out to have no target is a fact about the routing, not about the corpus.

The allocator `003DA8A0` and the release `003DAD00` run at their real virtual addresses under
Unicorn, with the body array at `02B4E4C0` and both list heads at `02B57CC4` and `02B57CC0`, because
all three are reached rip-relatively and neither function takes them as arguments.

**Instrument:** [`diff_body_pool.py`](../../../Reconstruction/Tests/Differential/diff_body_pool.py)
against [`body_pool.c`](../../../Reconstruction/Game/World/body_pool.c).

**Result: 158 commands, 124 compared lines, 0 mismatches** over a fixture pool of eight — 74
allocations of which 2 returned `NULL` at exhaustion, 9 distinct link images, and every one of the
eight bodies returned at least once.

### A pool's behaviour is its ORDER, and that is what is compared

Every body's `prev`, `next` and `self` word is read back after every operation, and the **whole
`0x130` bytes** of a body after an allocate — because allocate's initialisation is half its work, and
a reconstruction that linked correctly and initialised wrongly would pass a link-only comparison.

Driven: allocation to exhaustion **and one past it**; release in the same order as allocation and in
the reverse order, with reallocation after each, so the free list's stack discipline is shown rather
than asserted; the three different unlink arms — the **active head**, a **middle** body and the
**tail**; a pool of one; a null release; and a **double release**, which the original does not guard
against.

### The body knows its own index, and that is load-bearing

`release` never receives an index, only a pointer, and it pushes onto the free list using the word at
**`+0x04`** (`003DADCD` and `003DADD8`). A reimplementation that recomputed the index from the
pointer would agree on every case here and diverge the moment it were handed a body from anywhere
else. The suite compares that word on every body after every operation, so a reconstruction that
failed to maintain it fails immediately.

### One divergence, named rather than hidden

Release decides whether the body is the active head with `cmp ecx, r8d` at `003DAD33` — a comparison
of the **low 32 bits** of two pointers. Every body in the shipped pool shares its high half, so the
truncation cannot change an answer there, and the reconstruction compares whole pointers. No case in
this suite can distinguish them.

### How far the instrument itself has been tested

**66 mutants: 49 KILLED · 8 EQUIVALENT · 9 SURVIVED · 0 INVALID · 0 TIMEOUT · 0 NO_BUILD.** (Re-run 2026-09-12: the six INVALID were mutants this suite HAD caught and the instrument could not read, because the harness raised on a line-count difference instead of reporting it — `OPUS-CONTRA-HARNESS-LINECOUNT-INVALID`. All six are kills.)
Production inputs verified stable, all four hashes checked against the working tree afterwards.

**All nine survivors are one phenomenon, and it belongs to the original rather than to the suite.**
The initialisation block writes **overlapping and duplicated zeros**: `body+0x10`, `+0x18` and
`+0x20` are three adjacent eight-byte clears, and `body+0x100` and `+0x108` are written **twice** —
once before the `003DA830` call and once after. So a one-byte or one-slot shift in any single one of
those writes lands on a byte a neighbour or its own duplicate already zeroes, and no input can
distinguish the result.

**The control that proves this is a property and not an excuse:** the *third* of the three adjacent
clears, `memset(body+0x20, 0, 8)`, widened to nine bytes writes `+0x28` — which nothing else
covers, since the big clear starts at `+0x30` — and that mutant **was KILLED**. The reasoning
predicts exactly which member of the family is reachable, and the campaign agrees.

**One limit this exposes, and it is worth a reimplementer's attention.** Whether the *pre-call*
writes at `+0x100` and `+0x108` do anything depends on whether `003DA830` reads them. This suite
answers that callee, so it cannot tell — and neither can the mutation, for the same reason. They
look redundant; establishing that they are needs `003DA830` read, which this contract has not done.

**The six INVALIDs are wild-pointer crashes, not inconclusive tests.** Each mutates the `0xFFFF`
sentinel, the `0x130` stride, or a header offset, so the mutant resolves an index the original never
would and dereferences it. The reference does not crash and the mutant does; the campaign cannot
score that as a kill, but it is a difference the suite reached.

**An input-drift run was discarded rather than cited.** A first campaign returned the same outcome
counts, but its `production_inputs_stable` was **False**: the harness's `CONTRACT_MAP` was edited
while it ran. The numbers above are from a clean re-run whose four input hashes match the working
tree. *The harness is a campaign input, and a documentation edit inside `Reconstruction/` is still
an edit.*

### What is still owed, and it is live-only

Unchanged from the previous revision: read the free head in a populated field and see whether
ordinary play comes near the 128 limit, which decides whether §10 is a live concern or an
architectural note. Nothing above bears on it — a fixture of eight says nothing about how many the
game uses.

One check, and it is cheap because it needs no exhaustion: **read the free head at `0x02B57CC4`** in
a populated field and confirm it is a plausible index rather than `0xFFFF`. That alone tells us
whether ordinary play comes anywhere near the 128 limit, which decides whether §10 is a live concern
or an architectural note. A count of live bodies would be better still and is the same read plus a
list walk.

Requested from ASTRA; not claimed by me — and it belongs in **class B** of
`OPUS-REQ-ASTRA-TRIAGED-QUEUE`: one read, no particular game state.

## 14. Unresolved

- Whether ordinary play ever approaches 128 bodies.
- The separation pass itself — its geometry and cost are the referenced page's, not this contract's.
- What the live list's order means to the pass, given §9's history dependence.

## 15. Evidence

Static, from the shipping image (`73461D08…`). The allocator, the creator and all four consumers were
disassembled and read; the pool's 128-entry extent was **computed** from the stride and the free
head's address rather than taken from the page, and it agrees with it. The lifetime account and the
shape-sizing detail are cited from the referenced page.

**Claim table added 2026-09-12 (`OPUS-BODYPOOL-ISOLATED`).** The paragraph above states the method;
this enumerates the claims so `diff_body_pool.py` can map to them.

| claim | evidence | tier | confidence |
|---|---|---|---|
| the pool is 128 bodies of 0x130 at 02B4E4C0 | the stride from `imul rax, idx, 0x130` and the extent computed from the free head's address. **The extent is NOT exercised** — the suite drives a fixture pool of eight, which says nothing about 128 | 1 (static) | PROVEN by computation, not by a run |
| the list links are 16-bit indices with 0xFFFF as null | `movzx ... word` on every link (e.g. `003DA8A6`, `003DA8E7`, `003DAD38`/`003DAD43`) and `mov r9d, 0xFFFF` as the sentinel at `003DA8AF` and `003DAD19` in both functions. Executed — both lists read back after every operation | 1 (isolated original-code) | PROVEN |
| a body carries its own index at +0x04, and release reads it rather than recomputing | `003DADCD` and `003DADD8`. Executed — the word is compared on every body after every operation | 1 (isolated original-code) | PROVEN |
| allocate moves a body from the free list to the ACTIVE list | `003DA903` pops the free head, `003DA91F`–`003DA940` push onto the active head and link the old head back. Executed, with both heads compared | 1 (isolated original-code) | PROVEN |
| allocate returns NULL when the free list is empty | `003DA8B9` then `003DA9DF`. Executed — allocation to exhaustion and one past it | 1 (isolated original-code) | PROVEN |
| release unlinks from whichever list the body is on, then pushes onto the free list | `003DAD33`–`003DAD90` then `003DAD93`–`003DADD8`. Executed on the active head, a middle body and the tail | 1 (isolated original-code) | PROVEN |
| release accepts a NULL body and does not guard a double release | `003DAD03` tests for null and returns; nothing tests whether the body is already free. Executed, both | 1 (isolated original-code) | PROVEN |
| any runtime observation | — see §13 | none | UNKNOWN |

## 16. Parity plan

Reproduce: the LIFO free list (§9), the NULL-on-exhaustion with no diagnostic, the store of NULL into
`+0x138`, and — most easily lost — the guards in all four consumers, which are what turn exhaustion
into a quiet loss of collision rather than a crash.

## 17. Related

- `06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md`
- `04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md` — why `+0xC0` exists on only one
  of the four record layouts

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Party — CLIENT.** The pool consumer `002681D0` (§ "five consumers") is called by four party-control functions:

- `PartyControl_ApplyAnalogLocomotionToActor`;
- `PartyFocus_CommitPendingPackedActorHandle…`;
- `PartyFocus_ClearCurrentActorIfEligible`;
- `PartyRoster_AssignActorAndCommitFocus…`.

So changing which actor the player controls passes through one of this contract's pool consumers. The four callers use
that consumer and do not change it.
