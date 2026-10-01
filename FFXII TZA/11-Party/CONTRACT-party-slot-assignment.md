---
contract: put an actor in one of the four active party slots, displace whoever was there, and keep the record's own back-reference in step
category: 11-Party
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 11-Party/party-roster-and-control-suppression.md
entries: ["00269C70", "00266530", "0026DB30", "002695A0", "0025BFB0", "00263750", "00263770"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 68 addresses cited - 3 data, 12 entry, 53 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-party-slot-pass-1    # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — party slot assignment

Four pointers at `0x0209A1F0` say who is in the active party. Each occupant carries its own slot
number back in its record at `+0x12`. Those two representations of one fact are written by different
instructions in different functions, and **the whole of this contract is about when they agree.**

The first contract in `11-Party`.

## 1. Purpose

To move an actor into a slot, evict whoever held it, and update both the array and the record —
while leaving a reconstruction in no doubt about the one operation that updates the array and
**deliberately does not** update the records.

## 2. Interface

| operation | entry | parameters | returns |
|---|---|---|---|
| assign to slot | `00269C70` `PartyRoster_AssignActorToSlot` | `rcx` = actor record or NULL, `edx` = slot (signed) | none |
| assign during record init | `00266530` `ActorStorage_InitializeRecord`, block `00266740`–`00266792` | `al` = slot byte, `0xFF` to skip | — |
| clear the whole roster | `002695A0`, `0026DB30` | none | none |
| **consume the pending area-request mask** | **`0025BFB0`** | none - reads `[02099ABC]` | none. **Clears the roster only on the bit-0 arm**; see §7 |
| read a slot | `00263750` `PartyRoster_GetActorBySlot` | slot | the record or NULL |
| read a slot or the focus | `00263770` `PartyRoster_GetActorBySlotOrCurrentFocus` | slot, **negative means current focus** | the record or NULL |

Microsoft x64. **The writer set is complete and was measured, not assumed** — see §15, including the
one function this measurement does not follow.

## 3. Types

`PartyRosterSlots` — `ActorStorageRecord*[4]` at `0x0209A1F0`, image storage, never freed.

`ActorStorageRecord` supplies the back-reference:

| field | width | meaning |
|---|---|---|
| `+0x12` `partySlot` | `int8` | the record's own slot, `0..3`, `0xFF` when unassigned |
| `+0x0F` | `uint8` | `2` while the record holds a slot `0..3`, `3` otherwise |
| `+0xC0` `secondaryContextPtr` | `void*` | consulted when an occupant is evicted |

**`partySlot` is signed and the sign is load-bearing.** Both writers read it with `movsx` and then
bound it with an **unsigned** compare — `movsx ecx, byte ptr [rdi+0x12]` / `cmp ecx, 3` / `ja` at
`00269CB7`–`00269CBE`, and `movsx edx, byte ptr [rbx+0x12]` / `cmp edx, 3` / `ja` at
`00266744`–`00266752`. The `0xFF` sentinel sign-extends to `-1`, which is `0xFFFFFFFF` unsigned, so
it fails the bound. Declare the field unsigned and the guard stops working; declare the compare
signed and `-1` passes it.

## 4. Preconditions · postconditions · invariants

**Precondition.** None is checked beyond the bounds below. A null actor is legal at `00269C70`
(`test rdi, rdi` / `je` at `00269CB2`) and skips the record half entirely.

**THE INVARIANT, and the exception is the point of this contract:**

> For every slot `i` in `0..3`, `roster[i]` is either NULL or a record whose `+0x12` equals `i`;
> and every record whose `+0x12` is `0..3` is the occupant of that slot.

~~Both per-slot writers maintain it, in the same shape, which is what makes it an invariant rather
than two coincidences.~~ **Neither per-slot writer maintains it on eviction** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 338, which executed it (`check_roster.py`); `00269C70` and `00266738`–`00266792` re-read.)*. Both vacate the INCOMING
record's old slot and reset the record found there. That record is normally the incoming one itself, and step 6
then re-stamps it. **Neither resets the occupant it overwrites at the new slot.** `00269C70` only notifies that
occupant's context (`+0x152 = 1`, `002681E0`, `00269C91`–`00269CAD`). The init path does not even notify it. The
displaced record keeps `+0x12 = i` and its `+0x0F`, while `roster[i]` names another record. OPUS measured
`roster[2] = record 4` while record 2 kept `+0x12 = 2`. **So a displacement breaks the invariant exactly as a bulk
clear does, but for one record.** **The three bulk clears break it and repair nothing.** They zero the 32-byte
array and touch no record: all three are `xorps xmm0,xmm0` / `xorps xmm1,xmm1` / two `movdqu` stores
(`0025C017`/`0025C01F`, `002695AF`/`002695B7`, `0026DB52`/`0026DB5A`), and disassembling all three
shows no access at any record's `+0x12` or `+0x0F`. After a clear, **every former member still
believes it is in the party** and the array says the party is empty. Nothing reconciles them until
each record is assigned again.

## 5. State

All of it: the four pointers, and `+0x12` and `+0x0F` on each record that has ever held a slot.
Nothing else in the record is touched by either assignment path.

## 6. Relationships

- **Consumers of `partySlot`:** ten `movsx` readers, including
  `ActorSystem_BindBattleUnitsForEligibleRecords` and `Movement_SetRequestedSpeed` — so party
  membership is read by both the battle-unit binding and the movement path. Those readers see the
  stale value described in §4 after a bulk clear.
- **`PartyRoster_GetActorBySlotOrCurrentFocus`** implements the negative-index "current focus"
  convention documented in `party-roster-and-control-suppression.md`.
- **Eviction reaches the secondary context:** `00269C70` loads the outgoing occupant's `+0xC0`,
  stores `1` at `[ctx + 0x152]` and calls `002681E0` (`00269C9A`–`00269CAD`).

## 7. State transitions

**Assign — `00269C70`.**

1. `rbx = (int32)edx`, the requested slot, sign-extended. `rsi = roster`.
2. If `rbx <= 3` unsigned and `roster[rbx]` is non-NULL: take the occupant's `+0xC0`; if that is
   non-NULL, set `[+0x152] = 1` and call `002681E0`. **This is the eviction notice, and it fires
   before anything is unlinked.**
3. If the actor is NULL, stop.
4. Read the actor's own `+0x12`. If it is `0..3` unsigned: `old = roster[thatSlot]`;
   `roster[thatSlot] = 0`; and if `old` was non-NULL, `old->+0x12 = 0xFF` **and `old->+0x0F = 3`**
   (`00269CD5`–`00269CD9`). **The actor vacates its
   previous slot before taking the new one**, and ~~the record it displaces there is marked
   unassigned~~ the record found in that old slot is marked unassigned. That record is normally the actor
   itself, which step 6 then re-stamps. The occupant of the NEW slot is not touched *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 338, which executed it (`check_roster.py`); `00269C70` and `00266738`–`00266792` re-read.)*.
5. If `ebx >= 0`: `roster[rbx] = actor` (`00269CE1`). **Only the sign is tested here.** The `cmp ebx, 3` / `ja`
   guards only the eviction block, so a slot of 4 or more is stored past the four-entry array. OPUS stored slot 7
   at `roster[7]`, which is `0209A228` *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 338, which executed it (`check_roster.py`); `00269C70` and `00266738`–`00266792` re-read.)*.
6. `actor->+0x12 = bl`; `actor->+0x0F = (bl > 3 unsigned) ? 3 : 2` (`seta al` / `add al, 2` at
   `00269CEE`–`00269CF3`).
7. Continue at `00269CF6` with a further pass over `roster[rbx]` — outside this contract.

**Assign during record init — `00266530`, `00266740`–`00266792`.** The same protocol with two
differences. The requested slot arrives as a byte and `0xFF` means *leave the party state alone*
(`cmp al, 0xff` / `je` at `00266740`). Bit 7 of that byte is cleared before use (`btr ecx, 7` at
`0026674B`). Steps 4, 5 and 6 are then identical, including the displaced occupant's `+0x12 = 0xFF`
at `0026676D` — and this path **also** sets the displaced occupant's `+0x0F = 3` at `00266771`,
~~which `00269C70` does not do~~ **as `00269C70` does at `00269CD9`** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 338, which executed it (`check_roster.py`); `00269C70` and `00266738`–`00266792` re-read.)*. Two further points, both read here:
- **A byte without bit 7 also leaves the party state alone.** `0026673E jns` skips the block before the `0xFF`
  test. So only bytes `0x80`–`0xFE` assign.
- **The slot is `byte & 0x7F`, which is never negative, so step 5 always stores.** A byte above `0x83` writes
  `roster[4..126]`, past the array (`00266775`–`0026677C`).

~~**That asymmetry is real and is not resolved here.** Two functions implement one protocol and one of
them leaves the evicted record's `+0x0F` saying it is still in the party.~~ **There is no such asymmetry.** Both
writers set `+0x0F = 3` on the record they reset. Both also leave the occupant of the new slot believing it is in
the party *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 338, which executed it (`check_roster.py`); `00269C70` and `00266738`–`00266792` re-read.)*.

**Clear — `002695A0`, `0026DB30`.** Zero all four pointers. Both call `003590E0` immediately
beforehand.

> **`0025BFB0` was in this list and does not belong in it.** Corrected 2026-09-13 on
> `ASTRA-CONTRA-OPUS-MANAGER-QUEUE`; the sentence "no record is touched" was **never separately
> established for `002695A0` and `0026DB30` either** — it was one claim over three functions and only
> one of them has now been read closely. Treat the remaining two as **inherited and unverified**.

### ✖ `0025BFB0` is a gated request consumer, not an unconditional clear

**ASTRA is right** (`ASTRA-CONTRA-OPUS-MANAGER-QUEUE`), and the body is 179 bytes:

```
0025BFB4  eax = [02099ABC]                 ; a pending-request mask
0025BFBA  test eax, eax / je -> ret        ; EARLY RETURN when nothing is pending
0025BFD6  test bl, al                      ; bit 0
0025BFD8  je  -> the unload sweep          ; skips everything below
          ; ---- bit-0 arm ----
0025BFF0  for i in 4..0: if mask & (1<<i): 0026CE60(i); mask = [02099ABC]   ; INIT callbacks
0025C017  movdqu [0209A1F0], 0             ; 16 bytes
0025C01F  movdqu [0209A200], 0             ; 16 more  -> the 32-byte roster clear
          ; ---- always, when the mask is non-zero ----
0025C030  for i in 4..0: if mask & (1<<i): 0026CE60 -> no; 002628B0(i); mask &= ~(1<<i)  ; UNLOAD
```

Three things the old sentence got wrong:

1. **It is gated.** A zero mask returns without doing anything at all.
2. **The roster clear is gated again**, on bit 0. With mask `0x10` the function runs **only** the
   unload callback for index 4 and **leaves the roster alone**.
3. **It touches records.** Each set bit calls `0026CE60` (init) and/or `002628B0` (unload), and
   **`002628B0` is the sole caller of `ActorSystem_ReleaseManagerRecords` `0025B070`** — which this
   database already records, in `_types/types.tsv` under `ActorStorageRecord`. **My own type store
   contradicted this contract and I did not notice.**

Only the unload sweep clears bits, so a request survives in the mask until unload handles it.

> **What is NOT claimed here.** That the roster survives a clear-less path: **absence of a direct
> record store in this body is not record survival**, which is exactly the inference ASTRA asked me
> not to make. The native callbacks' real effects, the load-to-area ordering and the queue's own
> scheduling are **not established** — ASTRA's evidence is isolated original-code execution with
> controlled callbacks, not a live run.

## 8. Script · resource · event interactions

None directly. `0026DB30` is the field-transition path, so the roster is cleared whenever the world
changes, which is when the staleness in §4 is widest.

## 9. Determinism

Fully deterministic. The slot a record ends in is exactly the slot requested; there is no search and
no fallback.

## 10. Failure paths and edge conditions

- **Out-of-range slot at `00269C70`:** steps 2 and 5 are skipped but **step 6 still runs**, so the
  record's `+0x12` is set to the out-of-range value and `+0x0F` to `3`. The record ends up believing
  it holds a slot that does not exist, and no array entry points at it. Nothing reports this.
- **Negative slot:** `test ebx, ebx` / `js` at `00269CDD` skips the install. This guard **is
  reachable** here, because `edx` is sign-extended at `00269C7F`.
- **⚠ Slot `-1` is the exception to the paragraph above, added 2026-09-12 by falsification pass 1.**
  The install is skipped *and* `00269CEB mov byte ptr [rdi+0x12], bl` writes **`0xFF`** — which §2's
  claim 1 names as **"none"**, not as an out-of-range slot. With `+0x0F` set to `3` by the `seta`,
  the actor ends in **byte-for-byte the state the vacate path writes** at `00269CD5`/`00269CD9`. So
  **assigning slot `-1` removes an actor from the party consistently**, where slot `100` leaves it
  believing it holds a slot that does not exist. One out-of-range value is a clean removal and the
  rest are corruption, and the difference is only visible if you notice that `bl` of `-1` *is* the
  sentinel.
- **The same guard in the constructor is not reachable.** At `00266775` the value came from
  `movzx ecx, al` (`0..255`) and then `btr ecx, 7` (`0..127`), so `test ecx, ecx` / `js` can never
  be taken. The two paths guard the same step and only one of them can fire. Recorded as an
  observation about the emitted code, not a claim about intent.
- **Null actor** at `00269C70`: legal, and the roster is left alone.
- **Eviction with a null `+0xC0`:** the notice is skipped silently.

## 11. Observable behaviour

Not established; everything above is static. What would be observable:

- moving a character into an occupied slot displaces the occupant and the displaced character stops
  responding to party-slot queries;
- after a field transition the party appears empty to anything reading the array, while anything
  reading a record's own `+0x12` still sees the old slot, until the records are re-assigned.

## 12. Reproduction formula

```c
/* roster = (ActorStorageRecord **)0x0209A1F0 */
void PartyRoster_AssignActorToSlot(ActorStorageRecord *actor, int32_t slot)
{
    if ((uint32_t)slot <= 3 && roster[slot]) {              /* 00269C8C, 00269C91 */
        void *ctx = roster[slot]->secondaryContextPtr;      /* +0xC0, 00269C9A */
        if (ctx) { *((uint8_t *)ctx + 0x152) = 1; sub_2681E0(); }
    }
    if (!actor) return;                                     /* 00269CB2 */

    int32_t old = actor->partySlot;                         /* movsx, 00269CB7 */
    if ((uint32_t)old <= 3) {                               /* UNSIGNED: 0xFF -> -1 fails */
        ActorStorageRecord *prev = roster[old];
        roster[old] = 0;                                    /* 00269CC8 */
        if (prev) prev->partySlot = (int8_t)0xFF;           /* 00269CD5 */
    }
    if (slot >= 0) roster[slot] = actor;                    /* 00269CE1 */

    actor->partySlot = (int8_t)slot;                        /* 00269CEB */
    actor->f0F = (uint32_t)slot > 3 ? 3 : 2;                /* 00269CEE-00269CF3 */
}
```

The unsigned compares are not a tidying: written signed, `0xFF` passes the bound at `00269CBB` and
the function clears `roster[-1]`.

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent.** (2026-09-12)

The assignment `00269C70` and both readers `00263750` and `00263770` run at their real virtual
addresses under Unicorn, with the four-slot roster at `0209A1F0`, because all three reach it
rip-relatively and none takes it as an argument.

**Instrument:** [`diff_party_slots.py`](../../../Reconstruction/Tests/Differential/diff_party_slots.py)
against [`party_slots.c`](../../../Reconstruction/Game/Party/party_slots.c).

**Result: 173 commands, 97 compared lines, 0 mismatches** — 10 distinct roster images, 14 distinct
record images, and **17 traces in which two different records are notified**, which is the
raise-then-lower pair below.

### The bug this found in the reconstruction, and it is the reason to run rather than read

The state byte at `record+0x0F` is written as `(slot > 3) + 2`, and the comparison is **unsigned even
though the value was just sign-extended**: `00269CE5 movsx eax, bl` then `00269CE8 cmp eax, 3` then
`00269CEE seta al`. `seta` is the *above* condition. So a negative slot becomes `0xFFFFFFFF`, which
**is** above 3, and the state byte is **3**.

A reconstruction written with a signed comparison — which is what the sign-extension invites — gives
**2** for every negative slot, and the suite caught it on the one case that drives one. *A `movsx`
followed by an unsigned `set` is a shape worth recognising; the widening and the comparison disagree
on purpose.*

### The marker is raised and lowered on DIFFERENT records

`roster[slot]` is inspected twice — once before anything moves (`00269CA6`, writing `1`) and once
after (`00269D10`, writing `0`) — with a notify each time. On a displacement the first sees the
**outgoing** actor and the second the **incoming** one. A state comparison alone sees only the final
`0` and cannot tell the two apart; the trace is what does, and 17 of the cases exercise it.

### The two readers disagree about a negative slot, on purpose

`00263750` bounds unsigned (`cmp ecx,3 / ja`), so `-1` is a huge value and returns NULL.
`00263770` tests the sign **first** (`test ecx,ecx / js`) and sends a negative slot to the current
focus instead, then bounds the rest **signed** (`cmp ecx,4 / jge`). Both are driven at `-1`, which is
the case where handing the wrong one a negative slot is the difference between NULL and the focused
actor.

### How far the instrument itself has been tested

**28 mutants: 26 KILLED · 2 EQUIVALENT · 0 INVALID · 0 SURVIVED · 0 TIMEOUT · 0 NO_BUILD.** (Re-run 2026-09-12 under the repaired harness — `OPUS-CONTRA-HARNESS-LINECOUNT-INVALID`: the single INVALID was a mutant the suite had caught and the instrument could not read)
Production inputs verified stable, all four hashes checked against the working tree afterwards.

**Zero survivors, and getting there took two rounds — both about bounds without inputs on them.**

| round | survivors | what was missing |
|---:|---:|---|
| first | **5** | the fixture's roster was exactly four slots, so nothing stood at slot **4** for a bound widened from `3` to `4` to find. Both readers and the marker helper read a slot that was NULL on either side and agreed |
| second | **1** | every swap case moved an actor out of slot 0, 1 or 2, so the *vacate* bound's upper edge had no input on it and `old <= 3` widened to `old < 3` was invisible |
| third | **0** | — |

The roster array is now deliberately **longer than the four slots the operations accept**, with the
extras planted with real records, and a reassignment **from slot 3** is driven to every other slot.
*A bound is only tested by an input sitting on the wrong side of it* — the third time this session
that the same sentence has been the fix, and the reason the case list here now starts from the
bounds rather than from the happy path.

**The two `EQUIVALENT` rows are the roster's base address and the slot count**, which this file
carries as documentation — the operations take the roster as a parameter — and which the tool proves
byte-identical. **The one `INVALID`** mutates the `+0xC0` marker-pointer offset, so the mutant reads
a pointer from the middle of a record and dereferences it; the reference does not crash and the
mutant does.

### What is still owed, and it is live-only

Unchanged: the three checks below. Nothing here observes a real roster — the four records and their
marker objects are this fixture's.

The three checks worth making, in the order they would pay:

1. **§4's staleness.** After a field transition, read the four pointers and each former member's
   `+0x12`. If they disagree, the invariant really is suspended across transitions and every
   consumer in §6 is reading a stale value for that window. One read of 32 bytes plus four record
   bytes settles it, and it is the claim the rest of this contract most depends on.
2. ~~**The `+0x0F` asymmetry in §7.** Evict an occupant through `00269C70` and read its `+0x0F`: `2`
   confirms that path leaves it stale, `3` means something else repairs it.~~ **Settled statically, no live read
   needed** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 338, which executed it (`check_roster.py`); `00269C70` and `00266738`–`00266792` re-read.)*. There is no asymmetry: `00269CD9` sets `+0x0F = 3` on the record it resets, as the
   [roster page](party-roster-and-control-suppression.md) already said. The displaced occupant of the NEW slot
   keeps both bytes in both paths (§4).
3. **The out-of-range write in §10.** Nothing static shows a caller that passes a slot above 3, so
   whether that path is ever taken is unknown.

Requested from ASTRA; not claimed by me.

## 14. Unresolved

- What `+0x0F`'s two values select. Two writers, no reader observed.
- What `[secondaryContext + 0x152] = 1` means, and what `002681E0` does with it.
- The identity of `002695A0`. **`0025BFB0` is no longer "a bulk clear"** - it is the pending-request consumer described in §7 - but what its five request bits *mean*, and what `0026CE60` and `002628B0` do natively, are open.
- Whether `00263770` writes the roster in a callee — see §15.

## 15. Evidence

Static, from the shipping image (`73461D08…`).

**Claim table added 2026-09-12 (`OPUS-PARTYSLOT-ISOLATED`).** The prose below states the method and
is kept; this enumerates the claims so `diff_party_slots.py` can map to them.

| claim | evidence | tier | confidence |
|---|---|---|---|
| the roster is four qword slots at 0209A1F0 | the rip-relative base in all three bodies. Executed — all four read back after every operation, and a slot past the fourth shows the roster is not written there | 1 (isolated original-code) | PROVEN |
| an actor carries its occupied slot at +0x12, with 0xFF meaning none | `00269CB7 movsx ecx, byte [rdi+0x12]` then an UNSIGNED bound. Executed at 0xFF, at a real slot, and at an out-of-range value that is not 0xFF | 1 (isolated original-code) | PROVEN |
| assigning an actor already in the party vacates its old slot first | `00269CC8` clears the old slot before `00269CE1` fills the new one. Executed across pairs of slots | 1 (isolated original-code) | PROVEN |
| the state byte at +0x0F is (slot > 3) + 2 | `00269CE5 movsx` / `00269CE8 cmp` / `00269CEE seta` — **sign-extended then compared UNSIGNED**, so a negative slot gives 3. Executed at 0, 3, 4, 100 and −1 | 1 (isolated original-code) | PROVEN |
| the marker at [record+0xC0]+0x152 is raised to 1 before the swap and lowered to 0 after | `00269CA6` and `00269D10`, each followed by a notify, and on a displacement they apply to **different records**. Executed, and the trace is what distinguishes them | 1 (isolated original-code) | PROVEN |
| a NULL marker pointer skips the marker write and the notify | `00269CA1` and `00269D0B`. Executed on both the raise and the lower | 1 (isolated original-code) | PROVEN |
| the two readers disagree about a negative slot | `00263753 ja` bounds unsigned; `00263776 js` tests the sign first. Executed at −1 on both | 1 (isolated original-code) | PROVEN |
| the focus follow-up runs only for a real slot and only when the focus index is zero | `00269D1C` then `00269D28`. Executed at both focus values and at a slot past the fourth | 1 (isolated original-code) | PROVEN |
| any runtime observation | — see §13 | none | UNKNOWN |

**The writer set was measured and the first measurement was wrong.** An image-wide sweep matching
direct references — rip-relative into the array, or the image-base-relative displacement
`0x1F7A1F0` — reported eighteen referencing functions and four writers. It filed
`PartyRoster_AssignActorToSlot`, the function *named* for this job, as a reader, because its only
direct reference is `lea rsi, [rip + …]` at `00269C82`; it then writes through `rsi` at `00269CC8`
and `00269CE1`. **Thirteen of the eighteen take the address that way**, so the completeness claim
was worthless. The sweep was rebuilt to follow the register a `lea` loads — killing it on any other
write and dropping only the volatile registers at a call, since every one of these functions parks
the roster in a callee-saved register — and re-run with two controls chosen to catch exactly that
blind spot: `00266530` writing through the image-base-relative form, and `00269C70` writing through
its `lea`-loaded register. Both fire. The answer is **five writers of eighteen referencing
functions**, as listed in §2 and §7.

**The limit that remains.** The taint does not follow the address into a callee.
`PartyRoster_GetActorBySlotOrCurrentFocus` (`00263770`) passes the roster to a call, and what that
callee does with it is not covered here. It is the only such case.

## 15a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED

**A thorough contract — every claim held at the instruction it cites, including the two that a pass
usually catches.** What follows is what was attacked and what it cost.

| claim | what the bytes say |
|---|---|
| the state byte at `+0x0F` is `(slot > 3) + 2` | `00269CE5 movsx eax, bl` / `00269CE8 cmp eax, 3` / `00269CEE **seta** al` / `00269CF1 add al, 2`. **`seta` is unsigned** and the operand was **sign-extended**, so a negative slot compares above and lands on `3` |
| assigning an actor already in the party vacates its old slot first | `00269CC8 mov qword ptr [rsi+rax*8], 0` precedes `00269CE1 mov qword ptr [rsi+rbx*8], rdi`, and the vacated actor gets `+0x12 = 0xFF` and `+0x0F = 3` |
| a NULL marker pointer skips the marker write **and** the notify | `00269C9A mov rax, [rcx+0xC0]` / `test rax, rax` / `je 0x269CB2` jumps past **both** `00269CA6` and `00269CAD call 0x2681E0` |
| the two readers disagree about a negative slot | **exact, and it is a one-instruction difference.** `00263753 **ja**` bounds unsigned, so `-1` returns NULL. `00263776 **js**` tests the sign first and sends `-1` to `00263797 call 0x3590D0` then `jmp 0x3588B0` — **the current focus** |

> **Both readers index the same roster.** `00263758` and `00263780` resolve to `0209A1F0`, as does
> the assigner's `00269C82`. That is the same address
> [the field runtime pass](../04-Actor-Entity/CONTRACT-field-runtime-pass.md) names for its
> four-iteration party walk — **three contracts, one table, no disagreement.**

### The refinement: slot `-1` is a clean removal, not corruption

§10 says an out-of-range slot leaves the record *"believing it holds a slot that does not exist"*.
**That is true of `100` and false of `-1`.** `00269CEB` writes `bl`, and `bl` of `-1` is **`0xFF`** —
the very sentinel §2 defines as "none". With `+0x0F = 3` from the `seta`, the result is
**byte-for-byte identical to what the vacate path writes**.

So **one out-of-range value removes the actor cleanly and every other one corrupts it.** The three
facts were each already in the document — the skipped install, the `bl` store, the `seta` — and
nothing put them together. §10 now does.

**Mechanical:** no body-size drift; banned-evidence sweep clean; all nine entries resolve, and
`00263750 PartyRoster_GetActorBySlot` carries **43 callers across five subsystems**, which is why a
reader disagreement here is worth reading at the byte rather than trusting.

## 16. Parity plan

A reconstruction must reproduce: the unsigned bound on a signed field, the vacate-then-install order
in step 4, the eviction notice firing before the unlink, the `2`/`3` rule for `+0x0F`, and — most
easily missed — the fact that clearing the roster does **not** clear the records.

## 17. Related

- `11-Party/party-roster-and-control-suppression.md` — the roster, the focus convention and control
  suppression.
- `_types` — `PartyRosterSlots`, `ActorStorageRecord +0x12` and `+0x0F`.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

- **Audio — SERVICE.** The area unload `002628B0` calls three small Audio-filed bodies (128, 136 and 173 bytes) in
  its teardown sequence. By their filing they are sound-side teardown; they are not read here.
- **Core and CoreRuntimeScheduling — SERVICE.**
  - `002695A0` calls a 62-byte helper filed under Core and a 7-byte getter.
  - `002628B0` calls a 9-byte core getter.
  - `ActorStorage_InitializeRecord` and `ActorSystem_InitializeManagerRuntime` reach tables through
    `ImageAddress_ResolveRuntimePointer`, which is MECHANICAL.
- **Actor - SERVICE (1 edge).** `00266530` reaches bodies filed to Actor: `00265B60` (PresentationState) - shared machinery across the layer boundary, no shared ownership.
- **ActorEntity - SERVICE (46 edges).** `0025B070` reaches bodies filed to ActorEntity: `00234200`, `002693D0`, `002E3AF0` - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (2 edges).** `00263750` is also called by bodies filed to input: `00226BE0` (ActorControlMaskPropagationRuntime); `002628B0` reaches bodies filed to input: `0035B5D0` - shared machinery across the layer boundary, no shared ownership.
- **Movement - SERVICE (14 edges).** `0025B070`, `002628B0` reach bodies filed to movement: `002E3D00`, `00263560`, `0026A1D0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (1 edge).** `002628B0` reaches bodies filed to resource: `0032E520` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - SERVICE (2 edges).** `002628B0`, `0026DB30` reach bodies filed to save/load/settings: `002EF2B0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (23 edges).** `00263750` is also called by bodies filed to script VM / native bridge: `003415D0`, `00341CB0`, `00342250` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (1 edge).** `0026DB30` is also called by bodies filed to World: `00266D10` (NativeSupport) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (10 edges).** `0025BFB0` is also called by bodies filed to WorldAreaField (world area): `00314020`; `002628B0` reaches bodies filed to WorldAreaField (world area): `00378230`, `003DFA50`, `003EAA00` - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Presentation — CLIENT (4 edges, one fan-in).** All 4 edges are Presentation bodies reaching `002628B0` on this page. `FUN_002e8cc0` is the worked example - it is **32 bytes** that set or clear **bit 0 of `dword[[022C6F28] + 0x48818]`** according to one global byte at `0215FD56` - a mirror, not a decision. The crossing is **one shared subject with 4 callers on that layer**, not 4 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — SERVICE.** `0026CE60` on this page calls `FUN_00253a30`, owned by that layer. What it reaches is a 67-byte teardown: eight calls in fixed order, `[020927C8]` and `[020927CC]` zeroed, and a tail-jump to a ninth; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).
