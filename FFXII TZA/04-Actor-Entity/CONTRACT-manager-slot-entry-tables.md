---
contract: bind, clear and re-publish the four-entry tables an actor manager slot keeps for each of two definition sources
category: 04-Actor-Entity
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md
entries: ["003DA400", "003DA370", "003DA4D0", "003DA570", "003DD230", "003DCF60", "003DD320", "003DD350"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 66 addresses cited - 18 entry, 48 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-slot-tables-pass-1   # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the manager slot entry tables

Eight functions: four operations, written twice. `ActorManagerSlot` keeps **two** four-entry tables of
24-byte records, one per definition source. ~~and the two halves are identical code differing in
exactly three constants.~~

> ### ⚠ The symmetry claim was checkable instruction by instruction, and it does not hold — CHECKED 2026-09-11
>
> `OPUS-MGRSLOT-SYMMETRY` normalised all eight bodies — RIP operands resolved to absolute addresses,
> in-body branch targets made relative to the entry — and diffed the four pairs position by
> position, with a control pair that must differ (side A's bind against side A's reset) and does.
>
> | pair | instructions | differing | verdict |
> |---|---|---:|---|
> | clear one word | 9 vs 9 | 2 | **holds** — both are the named substitutions |
> | re-publish lookup | 9 vs 9 | 3 | **holds** — all three are the named substitutions |
> | **bind** | **44 vs 51** | 43 | **fails**, and not on constants |
> | **reset all** | **32 vs 13** | all | **fails** — they are different functions |
>
> **`bind`: side B does something side A does not.** With a negative fifth argument, A clamps it to
> zero (`003DA45A xor ecx,ecx` … `003DA46E cmovns ecx, eax`; *the first address corrected 2026-09-26 from `003DA425`, which is not an instruction start*) while **B calls `005C5230` and uses its result**
> (`003DD25C test ecx,ecx / jns / call 005C5230 / mov ecx, eax`). ~~That is a behavioural difference.~~
> *Corrected 2026-09-26 (FABLE, Claude Opus 5.5): `005C5230` is the three-byte retail stub `xor eax, eax` / `ret` (register `DA-4` lists it under four other identities, and the 2026-09 falsification log records the same), so side B always gets 0, the zero side A substitutes. The slots end up identical; the difference is one call to a stub with no side effects, visible only in a call trace.*
> And after the field writes **the two call different functions** — A `00257230`, B `0037DCF0`.
> B also spills `xmm6` and stages `xmm2` through it where A uses `xmm2` directly.
>
> **`reset all`: A resolves and delegates; B only resets.** A calls `002640C0` to *obtain* the slot
> (B takes it in `rcx`), writes the ten words, and then **tail-jumps to `00257830`**. B writes the
> ten words and returns. A does two things B does not do at all.
>
> **The corrected claim:** *the two four-entry tables are a real mirror in their LAYOUT and in the
> two small accessors; the two larger operations are separate implementations of the same idea and
> differ in behaviour, not only in constants.* Anything that generalised from one side's bind or
> reset to the other's needs re-reading.
>
> **One correction to the check itself.** It reported an "unnamed" difference in each small pair —
> `0x114`/`0x174` and `0x118`/`0x178`. Those *are* the `0x110 → 0x170` substitution, applied to a
> field inside the entry; the instrument matched the constant too literally. The two small pairs are
> fully explained by the three named substitutions, with no residue.

| | side A | side B |
|---|---|---|
| definition pointer | `slot + 0xD8` | `slot + 0xF0` |
| entry table | `slot + 0x110` | `slot + 0x170` |
| reverse lookup | `slot + 0x18` | `slot + 0x1C` |
| bind | `003DA400` | `003DD230` |
| reset all | `003DA370` | `003DCF60` |
| clear one entry's word | `003DA4D0` | `003DD320` |
| re-publish one lookup | `003DA570` | `003DD350` |

## 1. Purpose

A manager slot binds up to four records from each of two authored definition sources, and keeps a
small reverse index so a caller holding a selector can find which of the four entries holds it.

## 2. Interface

| | |
|---|---|
| bind | `rcx` slot, `edx` record index into the definition table, `r8d`/`r9d` entry index and a word, `xmm2` a float, and a fifth integer argument on the stack at `[rsp+0x50]` |
| reset all | `rcx` and further arguments it forwards; it obtains the slot from `002640C0` rather than taking it |
| clear one word | `rcx` slot, `edx` entry index |
| re-publish one lookup | `rcx` slot, `edx` entry index |
| return | none of the four returns anything a caller uses |

## 3. Types

`ActorManagerSlotEntry`, 0x18 — **the stride is proven by the index pre-multiply in all four
operations**, not by the spacing of the fields: each computes `lea reg, [idx + idx*2]` and then
addresses `[slot + reg*8 + base]`, so the effective stride is `3 * 8 = 24`.

**Corroborated 2026-09-11 from a second, independent code path.** The reset operations do not use
the pre-multiply at all — they write four entries with *literal* displacements, and the literals are
24 apart on both sides:

| | entry 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| A (`003DA370`) | `+0x118` | `+0x130` | `+0x148` | `+0x160` |
| B (`003DCF60`) | `+0x178` | `+0x190` | `+0x1A8` | `+0x1C0` |

Two derivations that cannot share a mistake: one from an index calculation, one from eight hard-coded
offsets.

**And the reset shows the entry's own shape.** Each entry gets a **pair** of words: the one at
`entry+0x08` is set to **0** and the one at `entry+0x0A` to **−1**. The reverse lookup is likewise
two words — A resets `+0x18` *and* `+0x1A`, B resets `+0x1C` *and* `+0x1E`, all four to **−1** —
which is why the type store carries each as a 4-byte span of 2-byte elements rather than as a single
value. The table in §0 names each side's base; it is not a single word.

| offset | size | field | meaning | evidence |
|---|---|---|---|---|
| `+0x00` | 4 | `definitionValue` | copied from the definition table row | `003DA456 mov edx, dword ptr [rcx + rax*8 + 0x14]` then `003DA471` |
| `+0x04` | 4 | `lookupIndex` | a caller argument clamped non-negative; the reverse lookup's subscript | `003DA46E cmovns ecx, eax`, read back at `003DA4B1` and `003DA586` |
| `+0x08` | 2 | — | set to 1 on bind, to 0 by reset and by the clear-one operation | `003DA478`/`003DA484`, `003DA3B1`, `003DA4E8` |
| `+0x0A` | 2 | `recordIndex` | the validated definition row index; reset writes `-1` | `003DA462`, `003DA3AA` |
| `+0x0C` | 4 | `clock` | the channel's playback clock; the caller float is `0.0f` from every shipped caller, then the tick advances it by `frameStep × rate` and passes it to the sampler as absolute time | `003DA44D movss`; `xorps xmm2, xmm2` at all four call sites (`0034F33A`/`0034F985`, `0034933A`/`00349785`); advanced at `003DA10D`/`003DD0A0` |
| `+0x10` | 4 | `rate` | playback speed multiplier on the clock step; `1.0f` at bind, settable per channel by the `cameraratio`/`camerashakeratio` verbs | `003DA48C`/`003DD2C7`; setters `003DA2D0`/`003DD1F0`; consumed at `003DA0FB`/`003DD093` |
| `+0x14` | 1 | `clockRunning` | cleared on the A side only; the A tick gates the clock advance on it and sets it on the first positive step | `003DA497`; `003DA0EF`/`003DA108` |
| `+0x15` | 3 | — | **unknown span**, not declared padding | no access |

The two tables tile `0x110..0x1D0` with nothing between them: `0x110 + 4*24 = 0x170`.

## 4. Preconditions · postconditions · invariants

**Preconditions, and all four operations enforce them by returning.**
- the entry index must be `0..3` — `cmp reg, 3` with an **unsigned** `ja` to the exit, so a negative
  index is rejected as a large unsigned value rather than by a sign test;
- the slot's definition pointer for that side must be non-null;
- bind additionally requires the record index to be non-negative (`js` exit) **and** below the count
  at `definitionTable + 4` (`cmp r8d, dword ptr [rcx + 4]` / `jae` exit).

**Postconditions.** Bind fills all seven members of one entry and then, if the definition pointer is
still non-null, writes the entry's own index into `lookup[entry.lookupIndex]`. Reset sets both lookup
words to `-1` and, for all four entries, `+0x08 = 0` and `+0x0A = -1`. The other two touch exactly one
word each.

**Invariants.** The two sides never touch each other's table, pointer or lookup. No operation moves an
entry; the entry index is always the caller's.

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | the side's definition pointer, the definition row, `entry+0x04` | `003DA410`, `003DA456`, `003DA4B1` |
| written | one entry or all four; one or both lookup words | `003DA471`…`003DA497`, `003DA3A2`…`003DA3DB` |
| allocated | none — the tables are interior storage in an image-resident slot | |
| deallocated | none — **no destructor can exist** | |

## 6. Relationships

Bind calls `00257230` after filling the entry and before writing the lookup; reset obtains its slot
from `002640C0` and tail-calls onward. The clear and re-publish operations call nothing.

## 7. State transitions

Per entry: **unbound** (`+0x0A == -1`) → **bound** (bind) → **unbound** (reset). The clear-one
operation does *not* unbind an entry: it zeroes `+0x08` and leaves `+0x0A` and the lookup alone, so an
entry can be in a third state — bound, with its word cleared — that only reset leaves.

## 8. Script · resource · event interactions

The definition table is authored data reached through the slot's own pointer, not through the registry
described in `CONTRACT-authored-table-row-lookup.md`; the row stride here is a hard 16 bytes at
`definitionTable + 0x10` rather than a stride read from a header.

## 9. Determinism

No RNG, no timing, no threading. Fully determined by the arguments and the definition table.

## 10. Failure paths and edge conditions

1. **Every guard returns.** Unlike the authored-table lookup, which falls into a null dereference,
   all four of these operations branch to a clean `ret`. The contrast is worth stating because both
   shapes appear in the same codebase and only one is safe to reproduce literally.
2. **Bind's lookup write is guarded separately.** After filling the entry, bind re-tests the
   definition pointer (`003DA4A7 cmp qword ptr [rbx + 0xd8], 0`) before writing the reverse lookup —
   so a call can leave an entry filled with **no** lookup entry pointing at it, if the pointer became
   null across the intervening call to `00257230`.
3. **The lookup is indexed by a value the caller supplies**, clamped only at the bottom: `cmovns`
   forces it non-negative but nothing bounds it above. The lookup has two words per side; a
   `lookupIndex` above 1 writes past it.
4. **`+0x14` is cleared on the A side and not on the B side.** Evidence of presence on A, not of
   absence on B — the stride is 24 either way.

## 11. Observable behaviour

In memory: after a bind at entry `i`, `slot + 0x110 + 24*i` holds the definition value, the record
index, `clock = 0.0f` at `+0x0C`, `rate = 1.0f` at `+0x10`, and `slot + 0x18 + 2*lookupIndex` holds
`i`. After a reset, all four entries read `+0x08 == 0`, `+0x0A == -1`, and both lookup words are `-1`.

## 12. Reproduction formula

```
bind(slot, recordIndex, entryIndex, word, f, selector, SIDE):
    if (unsigned)entryIndex > 3: return
    defs = *(void**)(slot + SIDE.defPtr);  if defs == 0: return
    if recordIndex < 0: return
    if (unsigned)recordIndex >= *(uint32*)(defs + 4): return
    e = slot + SIDE.table + 24*entryIndex
    *(float*)(e + 0x0C) = f        # clock; every shipped caller passes 0.0f
    *(uint16*)(e + 0x0A) = (uint16)recordIndex
    *(uint32*)(e + 0x00) = *(uint32*)(defs + 0x10 + 16*recordIndex + 4)
    *(int32*) (e + 0x04) = selector < 0 ? 0 : selector
    *(uint16*)(e + 0x08) = 1
    *(uint32*)(e + 0x10) = 0x3F800000   # rate = 1.0f
    if SIDE is A: *(uint8*)(e + 0x14) = 0
    call 00257230(slot->0x28)   # <- corrected 2026-10-02, OPUS - side A only (003DA4A2); side B calls 0037DCF0(slot->0x28) (003DD2D5)
    if *(void**)(slot + SIDE.defPtr) != 0:                    # re-tested, see 10.2
        *(uint16*)(slot + SIDE.lookup + 2*(*(int32*)(e+0x04))) = entryIndex

resetAll(slot, SIDE):
    *(uint16*)(slot + SIDE.lookup)     = -1
    *(uint16*)(slot + SIDE.lookup + 2) = -1
    for i in 0..3:
        *(uint16*)(slot + SIDE.table + 24*i + 0x08) = 0
        *(uint16*)(slot + SIDE.table + 24*i + 0x0A) = -1
```

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent.** (2026-09-12)

Seven of the eight shipped bodies have been executed at their real virtual addresses under Unicorn
against an independent reconstruction. Nothing has run in a live process, which is what still holds
`RUNTIME VALIDATED` open, and §11 remains the description of what a live read would show.

**Instrument:** [`Reconstruction/Tests/Differential/diff_manager_slot.py`](../../../Reconstruction/Tests/Differential/diff_manager_slot.py)
against [`Reconstruction/Game/Actor/manager_slot.c`](../../../Reconstruction/Game/Actor/manager_slot.c).

**Result: 128 commands, 60 compared lines, 0 mismatches** — 15 distinct slot images out of 32 dumps,
3 distinct guard images (so the overrun below was *observed*), and 7 of 23 traces containing the
`005C5230` call.

The four commands beyond the first run are a **record index of zero**, on both sides. Every other
bind in the script uses 1, 2, 4 or 8, and the omission was invisible until the mutation campaign
below turned the signed guard `recordIndex < 0` into `recordIndex < 1` and **nothing failed**: with
no case at zero, *refusing* zero and *accepting* it produce the same 120 lines. The guard is signed
(`test`/`js`) and zero is on the accepted side of it, so the gap was a missing case, not a wrong
reading — but it was a hole in the evidence for a boundary the contract states in §4.

**Seven of eight, and the eighth is named.** Side A's reset resolves its own slot through `002640C0`
and tail-jumps to `00257830`; it is a different function from side B's and is run on the original
side only, not reconstructed.

### What the run added to the symmetry finding

The static check found that the binds differ. Executing them found **a second asymmetry it could not
see, and a consequence neither half of the contract recorded**:

1. **Side B resolves before it validates.** `003DD265 call 005C5230` sits *ahead* of the four checks
   at `003DD26C`–`003DD282`. Side A's `cmovns` at `003DA46E` sits *after* them. So for an input the
   function goes on to **refuse** — a bad entry index, a bad record index, a null definition pointer
   — **side B has already called out and side A has done nothing at all.**

   A state comparison alone calls those two runs identical, because neither writes anything. The
   suite compares the **oracle call trace** as well as the slot, and this is the pair of cases that
   trace exists for.

2. **The reverse-lookup subscript is unbounded, on both sides.** The store is
   `mov word [slot + sub*2 + 0x18]` with `sub` read back from the entry's own `+0x04` — clamped
   non-negative by A, supplied by `005C5230` for B (always 0: the retail stub), and **never capped above** by either. A fifth
   argument of 250 writes at `slot + 0x20C`, ~~outside the `0x200` slot~~ inside the game's `0x288` slot and outside only the harness's `0x200` image *(corrected 2026-10-02, OPUS: `002630AB imul r14, rax, 0x288` over `02098E10`)*. Observed against 64 planted
   guard bytes, not inferred.

   §4 lists three preconditions and this is not among them, because it is not checked: the bound
   that keeps this in range is whatever the *caller* passes. A reimplementation that adds the check
   is safer than the original and different from it. *No shipped script reaches it (2026-09-26, FABLE; owed item 2
   below): the largest fifth argument any shipped call can pass is 110.*

### How far the instrument itself has been tested

A differential suite that passes proves the reconstruction matches on the cases it runs. It says
nothing about the cases it *doesn't*. The mechanically generated mutation campaign asks the second
question — change the reconstruction, and see whether the suite notices.

~~**45 mutants: 34 KILLED · 4 EQUIVALENT · 4 SURVIVED · 3 NO_BUILD · 0 TIMEOUT · 0 INVALID.**~~ *(answered: superseded by the 49-point run below; 2026-10-02, OPUS)*
Production inputs verified stable across the whole campaign.

> **That 45 is a FLOOR, not a total** — recorded the same day it was published, under
> `OPUS-CONTRA-MUTATION-LIT-SUFFIX`. The generator's literal pattern could not match a constant
> carrying a type suffix, so the four suffixed literals in `manager_slot.c` and `manager_slot.h`
> were never mutated. The pattern is fixed; this pilot has **not** been re-run under it, and until
> it is, the right reading of the numbers below is *"of the mutants generated"*, not *"of the
> mutants possible"*. Nothing in the adjudication changes — the four survivors are still the four
> survivors — but the denominator was smaller than the file.

**Every survivor is adjudicated, and none of them is a hole:**

| # | Mutation | Why it cannot be killed |
|---|---|---|
| 5 | `resolved = 0` initialiser → `= 1` | Dead on both paths: `side == MS_B` assigns it before the validations, `side == MS_A` assigns it after. Reachable **only** by a `side` that is neither enumerator, which has no original to be compared against — there are two tables, not three. Equivalent *within the declared domain*, and that qualifier is the honest form. |
| 13 | `fifth >= 0` → `fifth >= 1` | Differs only at `fifth == 0`, where both leave `resolved` at 0. |
| 14 | `fifth >= 0` → `fifth > 0` | Same boundary, same reason. |
| 44 | `MS_B = 1` → `MS_B = 2` | `side` is only ever equality-compared against `MS_A`; it is never an index and never enters arithmetic. Its numeric value is unobservable. |

Survivors 13 and 14 are **demonstrated** equivalent rather than argued: the script's first bind on
each side already passes `fifth = 0` (the case list runs `e * 3` from `e = 0`), so the one input that
could separate `>=` from `>` *is executed* and the two still agree. That is the original's own
property, not a weakness of the suite — `xor ecx,ecx` then `cmovns ecx,eax` yields 0 at `fifth = 0`
exactly as the mutants do. **A boundary the hardware cannot distinguish is not a boundary a test can
be blamed for missing.**

**The three NO_BUILDs are the layout check firing, not a failure to test.** Mutating the stride
(`24 → 25`), the unknown span (`uint8_t unknown15[3]` → `[4]`) or the check's own comparison makes
`ms_entry_size_check` a negative-sized array and the translation unit refuses to compile. A
compile-time refusal is a *stronger* result than a test failure: a wrong entry layout cannot be
built, let alone shipped.

**What the previous campaign cost, and what it bought.** The first run over this pilot produced 73
mutants with 10 survivors. Most of that surface was `memcpy(e + 0x0C, &callerFloat, 4)` — a hex
displacement and a byte count written out by hand at each of nine entry writes. Those literals were
mutation surface belonging to *this file*, not to the original: a wrong `4` there is a defect in the
reconstruction's transcription, and no case in any suite can distinguish "the contract says 4 bytes"
from "someone typed 4". Rewriting the writes to go through the declared packed `MsEntry` — by
`offsetof` and `sizeof`, never a literal — removed 28 mutants outright and left the header as the
single source of truth for the layout. **The right response to a survivor is sometimes to delete the
question rather than to answer it.**

**Instrument:** [`Reconstruction/Tests/mutation_test.py`](../../../Reconstruction/Tests/mutation_test.py)
`manager_slot`.

### What is still owed, and it is live-only

1. ~~**What `005C5230` returns in play**, since it decides where side B's reverse-lookup write lands.~~ *Answered
   2026-09-26 (FABLE), statically: 0, always. The body is `xor eax, eax` / `ret` at `005C5230`, so the write lands
   at subscript 0 on side B, as on side A. This was never live-only.*
2. ~~**Whether any caller ever passes a fifth argument large enough to leave the slot** — the
   difference between a latent defect and a reachable one.~~ *Answered 2026-09-26 (FABLE, Claude Opus 5.5),
   statically: it is latent; no shipped script reaches it.*
   - **The callers.** The binds' only callers are four ScriptVM verb handlers (raw call index). Neither bind's address
     is stored anywhere in the image, and neither has a rip-relative reference.
   - **The two-argument verbs.** `camerastart_7e` (`0034F930`) and `camerashakestart_1a3` (`00349730`) push −1 and
     pass their first pop as the fifth argument, so it is always −1, i.e. subscript 0.
   - **The three-argument verbs.** `camerastart_7d` (`0034F2F0`) and `camerashakestart_1a2` (`003492F0`) take it
     from the script's last argument.
   - **What the shipped scripts pass** (the decompiled `us` corpus):
     - `camerashakestart_1a2` is never called.
     - `camerastart_7d`'s last argument is `getcamerasubframe()` in 37 calls (a shared `mov eax, 1` / `ret` stub, so 1),
       `getcameramainframe()` once (`005C5230`, 0) and the constant 110 once.
     - `camerastart_7e` (3,833 calls) and `camerashakestart_1a3` (328) pass −1.
   - **So the largest subscript is 110**, a store at `+0xF4`, inside the ~~`0x200`~~ `0x288` slot *(corrected 2026-10-02, OPUS: the slot stride, `002630AB`)*. Control:
     `_index/candidates/mgrslot-stub-005C5230/channel_reach.py` (FAILS 0).
   - *Not covered:* scripts outside the shipped `us` set, and code injected at run time.
3. ~~**Whether `002640C0` ever returns a slot other than the one side B would have been handed** —
   the question side A's extra indirection raises and static reading cannot close.~~ *Answered 2026-09-26 (FABLE, Claude Opus 5.5), statically: never, in the shipped code.*
   - **Side B's callers.** Each of side B's four entries is reached only from camera-shake verb handlers: `003DD230` from two, `003DCF60` from `0034B100`, `003DD320` from two and `003DD350` from `0034B610`.
   - **What they pass.** Every handler calls `002640C0` (`mov rax, [02099D70]` / `ret`) and passes that result as
     `rcx`.
   - **Nothing in between can change it.** Between the call and the transfer, the handlers only pop script
     arguments. The pop routine calls one CRT helper, and neither writes `02099D70`.
   - **So B's slot is always the one A's reset would obtain.** A's extra indirection is a difference in *where*
     `002640C0` is called, not in *which* slot results.
   - Control: `_index/candidates/mgrslot-stub-005C5230/slot_identity.py`, FAILS 0, with a known writer of
     `02099D70` as the positive.

Queued; the live-automation pause stands.

**What `OPUS-MGRSLOT-SYMMETRY` was, and was not.** It is a **static** check — eight bodies
normalised and diffed, with a control pair that must differ and does. It is not an execution and
this contract's evidence class does not change. It is worth saying plainly because the finding is
substantial: *a claim can be falsified by reading, if the reading is mechanical and carries a
control.* The symmetry claim had been stated as checkable for as long as the contract existed; what
it lacked was the check, not an experiment.

**What execution would still add**, in the order it would pay:

1. ~~**`bind`'s negative-fifth-argument path.** Side B calls `005C5230`; side A substitutes zero. An
   isolated original-code run over both binds with that argument negative would show what the two
   slots actually end up holding — this is the one asymmetry with a visible consequence, and it is
   the obvious next pilot for this family.~~ *Not needed (2026-09-26, FABLE): the callee is the stub
   returning 0, so both slots hold the same thing; the asymmetry has no visible consequence.*
2. **The reset's ten-word pattern**, which is a fixed pattern and the easiest thing here to compare
   as resulting memory.
3. ~~**Whether `002640C0` ever returns a slot other than the one B would have been handed** — the
   question A's extra indirection raises and static reading cannot close.~~ *Not needed (2026-09-26, FABLE): answered
   statically in the owed list above.*

<!-- OPUS-MUT-S13-RESTATE -->
### Mutation campaign, re-run 2026-09-12 on the full literal surface

**49 generated points: 38 KILLED · 4 SURVIVED · 4 EQUIVALENT · 3 NO_BUILD · 0 TIMEOUT · 0 INVALID. Verdict `FAIL`.**
Receipts: `Database/Tools/work/OPUS/litsuffix/manager_slot2` (ignored path). Instrument: `Reconstruction/Tests/mutation_test.py`. The table for every pilot, and the four kinds a survivor can be, are on [`MUTATION-CAMPAIGNS.md`](../../../Reconstruction/MUTATION-CAMPAIGNS.md).

**The 45-mutant line above is superseded.** Two of its four survivors were a REAL GAP and are now killed: `entryIndex > 3u` mutated to `> 4u` in the clear and in the republish, which the script could not distinguish because it drove those operations at index 1 and index 9 and 9 is refused by both bounds. Index 4 is now driven, and it is the meaningful one rather than an arbitrary out-of-range value — `0x110 + 4 × 24 = 0x170`, side B's entry 0, so the mutant writes the other side's table. The four that remain are all **kind A, provably equivalent**: the `resolved = 0` initialiser (both arms assign before any read), `fifth >= 0` at both `>= 1` and `>` (they differ only at 0, where `resolved` is 0 either way), and `MS_B = 1 → 2` (the enum's value is never read — `entry_at`, `defptr` and `lookup_base` each compare `side == MS_A` and nothing else). The three `NO_BUILD` are the header's own `ms_entry_size_check` refusing a wrong stride at compile time, which is a stronger guard than a test.

## 14. Unresolved

1. ~~**What the two sides mean** — which definition source each serves. The layout is identical and
   nothing in these eight functions distinguishes them beyond the three constants.~~ **Verified
   owner-side 2026-09-22 (SWE2-CONTRACT): FABLE's note stands.** An E8/E9 rel32 census over all
   35,713 `.pdata` bodies finds exactly **13 call sites** for the eight functions, every owner a
   verb handler, and the partition is total — A side: `003DA400` ← `camerastart_7d`/`_7e`
   (`0034F2F0`/`0034F930`), `003DA370` ← `resumebehindcamera_289`/`_1e4` (`00343DB0`/`003442D0`),
   `003DA4D0` ← `camerastop_54`/`_53` (`003502E0`/`00350660`), `003DA570` ← `camerachange`
   (`00351C00`); B side: `003DD230` ← `camerashakestart_1a2`/`_1a3` (`003492F0`/`00349730`),
   `003DCF60` ← `camerashakeclear` (`0034B100`), `003DD320` ← `camerashakestop_19e`/`_19d`
   (`00349ED0`/`0034A370`), `003DD350` ← `camerashakechange` (`0034B610`). Receipts:
   `Tools/work/SWE2-CONTRACT/slotentry_callers.json`. The setters verify too: `0026CE00` is
   `movsxd`/`imul 0x288`/`mov [rcx+02098EE8], rdx` (`0026CE0A`) and `0026D3A0` the same against
   `02098F00` (`0026D3AA`) — the `+0xD8`/`+0xF0` table-pointer fields. So: **A = the camera-shot
   definition table, B = the camera-shake definition table.**
   > *Settled from the callers 2026-09-12 (FABLE, M-A; a note only — the contract text is the
   > owner's).* Nothing inside the eight functions distinguishes the sides, but their **callers**
   > do, completely: the A side (`003DA400`, `003DA370`, `003DA4D0`, `003DA570`) is called only by
   > the **camera verbs** — `0x007D` / `0x007E` `camerastart`, `0x0053` / `0x0054` `camerastop`,
   > `0x0055` `camerachange`, `0x01E4` / `0x0289` `resumebehindcamera` — and the B side (`003DD230`,
   > `003DCF60`, `003DD320`, `003DD350`) only by the **camera-shake verbs** — `0x01A2` / `0x01A3`
   > `camerashakestart`, `0x019D` / `0x019E` `camerashakestop`, `0x01A1` `camerashakeclear`, `0x019F`
   > `camerashakechange` (`edges.tsv` against [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv), every caller a verb handler). So the
   > table at `+0x110` behind `+0xD8` is the slot's **camera definition table** and the one at
   > `+0x170` behind `+0xF0` its **camera-shake definition table**; the pointers are installed by the
   > two 22-byte setters `0026CE00(slot, blob)` and `0026D3A0(slot, blob)` (`0x288`-stride slot
   > arithmetic, `0026CE0A`, `0026D3AA`), which take the definition blob from the loaded container.
2. ~~**What `+0x0C` and `+0x10` are**, beyond a caller float and a `1.0f` initial value.~~
   > *Settled 2026-09-22 (SWE2-CONTRACT), confirming the names the type store carried since
   > 2026-09-12 (FABLE): `+0x0C` is the channel's playback **`clock`** and `+0x10` its **`rate`**.*
   > **`+0x0C` is written `0.0f` by every shipped bind**: the parameter survives in the
   > signature but all four verb wrappers zero it (`xorps xmm2, xmm2` at `0034F33A`,
   > `0034F985`, `0034933A`, `00349785`). It is the clock the per-frame ticks advance:
   > `003DA050` (A) walks `rbx` at `entry+0x0C` over the four channels and, for a playing
   > channel (`+0x08` state `1`; `2` skips the advance but still samples), computes
   > `step = frameStep(02B4E4B0) × rate(+0x10) × const(01DFE0BC)` at `003DA0F3`–`003DA100`
   > and adds it into `[rbx]` (`003DA10A`–`003DA111`), then hands the value to the player
   > (`movss xmm2, [rbx]` at `003DA133` → `002555A0`/`00257A00`/`002567B0`) as the shot's
   > absolute time. `003DCFB0` (B) does the same at `entry+0x08`+`0x18` stride:
   > `frameStep(02B58190) × rate(+0x10) × const` added into `+0x0C` (`003DD08B`–`003DD0A5`)
   > and passed to the shake sampler `0037D1F0` (`003DD05D`). **`+0x10` is a per-channel
   > playback speed**: `1.0f` at bind (`003DA48C`/`003DD2C7`), then settable — A side
   > `003DA2D0(slot, ch, rate)` stores `movss [slot + (ch+0xC)*24], xmm2` under
   > `cameraratio`/`cameraratio_115`; B side `003DD1F0(slot, ch, rate)` stores
   > `(ch+0x10)*24` under `camerashakeratio`/`camerashakeratio_1a6`. *Census caveat:* a
   > displacement scan does **not** find these consumers — the ticks park a walking pointer
   > at `entry+0x0C`/`entry+0x08` and use small offsets, and the setters fold the field
   > offset into the index (`(ch+0xC)*24`, displacement `0`). The chain above was found by
   > following the named consumers on the sibling pages and reading the bodies.
3. ~~**Whether `lookupIndex` can exceed 1 in practice** (§10.3). If it can, the lookup is larger than
   the two words the reset clears.~~ **Yes — verified owner-side 2026-09-22 (SWE2-CONTRACT): the
   mechanism admits it and FABLE's corpus note shows it exercised.** The binder clamps the fifth
   argument only *below* — `003DA46E cmovns ecx, eax` (A) and `003DD265 call 005C5230` (B; the
   resolver is a three-byte `xor eax,eax/ret` stub, so both sides land on `max(arg,0)` by different
   means) — and stores it into `entry+0x04` with **no upper bound**: `003DA4B9` writes
   `word [slot + 0x18 + 2×lookupIndex]` and `003DD2EC` writes `word [slot + 0x1C + 2×lookupIndex]`,
   each indexed by a value the caller fully controls. `0034F930` (`camerastart_7e`) verifies the
   `−1` path — `or edx, 0xFFFFFFFF` at `0034F944` pushes `−1` onto the VM stack (`00267F90`) and the
   first `00267E10` pop returns it as arg5, so 2-arg calls bind index `−1 → 0`; `0034F2F0`
   (`camerastart_7d`) has no push — its arg5 is the script's own last pop, so an authored value
   (FABLE's corpus: literal **110** in one call, `getcamerasubframe` results in 38 of 39) lands at
   `slot + 0x18 + 2×110` = `+0xF4`, far past the two reset-cleared words. **The "lookup" is a
   per-sub-frame word table the reset only partly clears** — which was the residual, and the reset
   vs. stray-write question below is answered: the writes past `+0x1B` are real, caller-driven
   stores, not strays.
   > *Answered from the callers 2026-09-12 (FABLE, M-B; a note only).* The A side's fifth argument
   > is the **first value the `camerastart` handlers pop**: `camerastart_7e` (`0034F930`) first
   > **pushes `−1`** (`or edx, 0xFFFFFFFF` → `00267F90`, `0034F944`–`0034F94D`) and pops it back, so
   > all **3,833** two-argument calls in the shipped scripts bind with index `−1 → 0` after the
   > `cmovns`; `camerastart_7d` (`0034F2F0`) takes it from the script's own last push, which in
   > 38 of its 39 calls is the result of the preceding `CALL getcamerasubframe` and in the one
   > literal call is **110**. The binder stores the entry index at `word [slot + 0x18 + 2 ×
   > index]` (`003DA4B9`), so an authored 110 lands at `slot + 0xF4` — far outside the two words the
   > reset clears, and past the B side's word at `+0x1C` for any index ≥ 2. **So yes: the index can
   > and does exceed 1 in shipped scripts**, and the "lookup" is a per-sub-frame word table the
   > reset only partly clears (or the reset is right and those writes are stray); which, and the
   > ~~runtime range of `getcamerasubframe`, is the residue for the contract's owner.~~ *(answered: see the 2026-09-12 note above — the writes past `+0x1B` are real stores, and `getcamerasubframe` is a `mov eax, 1` / `ret` stub; 2026-10-02, OPUS)*

## 15. Evidence

> ### ⚠ One row of this table was the falsified claim, and it stood here for a day after the prose above it was corrected
>
> ~~| the two sides are otherwise identical | instruction-for-instruction comparison of
> `003DA400`/`003DD230` and `003DA370`/`003DCF60` | PROVEN |~~
>
> `OPUS-MGRSLOT-SYMMETRY` falsified exactly that, **using exactly that comparison** — bind is 44
> instructions against 51 and reset is 32 against 13. The correction box at the top of this contract
> was written the same day and this row was left standing underneath it, marked `PROVEN`, citing the
> method that disproves it.
>
> **A correction that does not reach the evidence table has not landed.** The row is withdrawn here
> rather than reworded, because there is no version of "otherwise identical" that survives: the two
> binds differ in behaviour and the two resets are different functions. What replaces it is the pair
> of asymmetry rows below, which are testable and are tested.
>
> The tier column is also reworded, as in the other executed contracts: `static` means decoded,
> `executed` means run and compared against a reconstruction. Until 2026-09-12 every row read
> "static, isolated original code" while §13 read "Empty", which was only consistent because the
> phrase meant *the shipped bytes, read*.

| claim | evidence | tier | confidence |
|---|---|---|---|
| the 24-byte record stride | `lea reg,[idx+idx*2]` then `[slot+reg*8+base]` in all four A-side operations — `003DA446`, `003DA4E2`, `003DA582` — and `003DD28C` on the B side; corroborated by the resets' eight literal displacements 24 apart; **executed** over every entry index with the whole slot compared | 1 (static + **executed**) | PROVEN |
| the four-entry tables tile 0x110..0x1D0 | `0x110 + 4*24 = 0x170`, the B-side base, with nothing between them; **executed** by binding entry 3 on A and entry 0 on B and comparing all 0x200 bytes | 1 (static + **executed**) | PROVEN |
| the entry index is rejected by an UNSIGNED compare | `cmp reg, 3` with `ja` in each index-taking operation — `003DA41A`/`003DA41D`, `003DA4D0`/`003DA4D3`, `003DA570`/`003DA573` on A and `003DD26C`/`003DD26F`, `003DD320`/`003DD323`, `003DD350`/`003DD353` on B; **executed** at 4 and at `0xFFFFFFFF` on both sides, where a signed test would accept the second | 1 (static + **executed**) | PROVEN |
| bind requires a non-negative record index below the count | `003DA42C test edx,edx / js` — a SIGNED test — and `003DA434 cmp r8d, [rcx+4] / jae`; **executed** with each failing alone | 1 (static + **executed**) | PROVEN |
| the definition pointer must be non-null | tested at entry and **re-tested at `003DA4A7`** after the call at `003DA4A2`, because the callee could have cleared it; **executed** with each side's pointer null in turn | 1 (static + **executed**) | PROVEN |
| **both sides compute the SAME value — `(x >= 0) ? x : 0`** | **found 2026-09-12 (§15a)**: side B's resolver `005C5230` is a **three-byte retail stub**, `xor eax, eax / ret`. Side A is `003DA45A xor ecx, ecx` + `003DA46E cmovns ecx, eax`. The clamp/resolve distinction is real in the **mechanism** and absent from the **result** | 1 | PROVEN |
| **the two sides validate the record index ~~differently~~ the same way** | ~~**re-read 2026-09-12**: side A uses one unsigned compare, `003DA434 cmp r8d, [rcx+4]` / `jae`, which rejects negatives by itself;~~ side A also uses two, `003DA42C test edx, edx` / `js` then `003DA434 cmp r8d, [rcx+4]` / `jae` *(corrected 2026-10-02, OPUS: both are in `003DA400`, with `r8` from `003DA417 movsxd r8, edx`)*; side B uses **two**, `003DD27A test ebp, ebp / js` then `003DD27E cmp ebp, [r14+4] / jae`. Same rejections, different instructions | 1 | PROVEN |
| side A clamps a negative fifth argument and side B resolves it | `003DA46E cmovns ecx, eax` against `003DD265 call 005C5230` / `mov ecx, eax`; **executed** with the same negative value on both sides — ~~the entry's `+0x04` and the call trace both differ~~ only the call trace differs; the entry's `+0x04` is 0 on both *(corrected 2026-10-02, OPUS: `005C5230` is `xor eax, eax` / `ret`; side A `003DA45A xor ecx, ecx` / `003DA46E cmovns ecx, eax`)* | 1 (static + **executed**) | PROVEN |
| side B resolves BEFORE validating and side A clamps after | `003DD265` precedes the checks at `003DD26C`–`003DD282`; `003DA46E` follows them. **Executed on refused inputs, where neither side writes anything and only the trace separates them** | 1 (static + **executed**) | PROVEN |
| the reverse-lookup subscript is unbounded | `003DA4B9 mov word [rbx + rax*2 + 0x18], si` with `rax` from the entry's own `+0x04`, clamped below and never capped above; **executed** with a fifth argument of 250, which writes at `slot + 0x20C` — ~~outside the `0x200` slot and~~ inside the game's `0x288` slot, outside the harness's `0x200` image and into its planted guard bytes *(corrected 2026-10-02, OPUS: `002630AB`)* | 1 (static + **executed**) | PROVEN |
| `entry+0x0C` is the channel playback clock, `entry+0x10` the rate multiplier | all four bind callers pass `xmm2 = 0.0f` (`xorps` at `0034F33A`/`0034F985`/`0034933A`/`00349785`); the ticks advance `clock += frameStep × rate × const` — A `003DA050` at `003DA0F3`–`003DA111` over `rbx = entry+0x0C`, B `003DCFB0` at `003DD08B`–`003DD0A5` over `rbx = entry+0x08` — and pass it to the samplers (`003DA133` → `002555A0`, `003DD05D` → `0037D1F0`); rate setters `003DA2D0`/`003DD1F0` write `+0x10` under the `cameraratio*`/`camerashakeratio*` verbs | 1 | PROVEN |
| side A is the camera-shot table, side B the camera-shake table | E8/E9 census over all `.pdata` bodies: 13 call sites for the eight functions, **every owner a verb handler** — A: `camerastart_7d`/`_7e`→`003DA400`, `resumebehindcamera_289`/`_1e4`→`003DA370`, `camerastop_54`/`_53`→`003DA4D0`, `camerachange`→`003DA570`; B: `camerashakestart_1a2`/`_1a3`→`003DD230`, `camerashakeclear`→`003DCF60`, `camerashakestop_19e`/`_19d`→`003DD320`, `camerashakechange`→`003DD350`; table pointers installed by `0026CE00`→`02098EE8` (`+0xD8`) and `0026D3A0`→`02098F00` (`+0xF0`), both `imul 0x288` | 1 (static) | PROVEN |
| `lookupIndex` exceeds 1 in shipped play | the mechanism admits it — clamped only below (`003DA46E` cmovns; B resolves negatives via stub `005C5230`), stored unbounded at `003DA4B9`/`003DD2EC` (`slot + 0x18`/`+0x1C + 2×idx`); the exercise is authored — FABLE's script corpus: literal `110` in one `camerastart_7d` call, `getcamerasubframe` results in 38 of 39 | 1 (static) + authored corpus | PROVEN |
| any runtime observation | **none exists** | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED

Every claim was checked at the instruction it cites, and every one holds.

| claim | what the bytes say |
|---|---|
| the tables tile `0x110`..`0x1D0` | corroborated **from the addressing, not the arithmetic**: `003DA446 lea rdi, [rsi + rsi*2]` then `003DA471 mov dword ptr [rbx + rdi*8 + 0x110], edx` — `3 × index × 8` is a **24-byte stride from `0x110`**, and `0x110 + 4×24 = 0x170` |
| the entry index is rejected by an **unsigned** compare | `003DA41A cmp esi, 3` / `003DA41D **ja**`, and `003DA4D0 cmp edx, 3` / `003DA4D3 **ja**`. A signed `jg` would accept `0xFFFFFFFF` |
| bind requires a non-negative record index below the count | side A `003DA434 cmp r8d, [rcx+4]` / `jae`; side B `003DD27A test ebp, ebp / js` then `003DD27E cmp ebp, [r14+4] / jae` |
| the definition pointer must be non-null | `003DA423 test rcx, rcx`; side B `003DD275 test r14, r14` |
| side B resolves **before** validating, side A clamps **after** | exact. `003DD261 test ecx, ecx / jns 0x3DD26C / 003DD265 call 0x5C5230` sits **above** the checks at `003DD26C`–`003DD282`; side A's `003DA46E cmovns` sits **below** its own |
| the reverse-lookup subscript is unbounded | `003DA4B1 movsxd rax, dword ptr [rbx + rdi*8 + 0x114]` then `003DA4B9 mov word ptr [rbx + rax*2 + 0x18], si`, with **nothing between them** but the unrelated `003DA4A7 cmp qword ptr [rbx+0xd8], 0`. Note `0x114` is `0x110 + 4` — the entry's own `+0x04`, as claimed |

### What the pass found: the A/B asymmetry is in the mechanism, not the value

*"Side A clamps a negative fifth argument and side B resolves it"* reads as though the two sides do
**different things to the value**. They do not.

```asm
003DA45A  xor    ecx, ecx          ; side A
003DA45C  mov    eax, [rsp + 0x50]
003DA460  test   eax, eax
003DA46E  cmovns ecx, eax          ; ecx = (eax >= 0) ? eax : 0

003DD261  test   ecx, ecx          ; side B
003DD263  jns    0x3dd26c
003DD265  call   0x5c5230          ; <- and 005C5230 is `xor eax, eax / ret`, THREE BYTES
003DD26A  mov    ecx, eax          ; ecx = (ecx >= 0) ? ecx : 0
```

**`005C5230` is a retail stub that always returns zero.** Both sides therefore compute
`(x >= 0) ? x : 0` — branchless on A, through a conditional call to a no-op on B. **The difference a
reimplementation has to preserve is the CALL, not the value**, and the call is observable only in a
trace, which is exactly what this contract's pilot compares on refused inputs.

> **A stub in the ORIGINAL is worth as much care as a stub in a fixture.** The rule this database
> keeps is *"a stub is not proof of its native effects"*; the mirror image is that a shipped no-op
> is not proof of an absent mechanism either. `005C5230` may have resolved something in a debug
> build. What can be said is what it does in **this** image: nothing, and it returns zero.

**Mechanical:** no stated body size drifts from the current census; a banned-evidence sweep for
`.pdata`, `.xdata`, unwind, EH-map and IP-to-state found nothing; all eight entries resolve, every
one of them in `Script_VM_Native_Bridge` by caller.

> **This pass read instructions.** The claims it checked were already `static + executed` by this
> contract's own pilot and were not re-run; what is added is corroboration from the addressing modes
> and the identification of `005C5230`.

## 16. Parity plan

`STRUCTURAL` — the two tables and their adjacency at `0x170`.
`CONTRACT` — bind entry 3 and assert the lookup word, then bind with entry index 4 and assert nothing
changes.
`STATE-TRANSITION` — bind, clear-one, reset, asserting the third state in §7 exists (`+0x08 == 0`
while `+0x0A != -1`).
`EDGE-CASE` — a negative entry index, which the unsigned compare must reject, and a record index equal
to the definition count, which `jae` must reject.

**All four are done offline** — see §13. `CALCULATION`, `STRUCTURAL`, `STATE-TRANSITION`,
`EDGE-CASE` **and `CONTRACT`** are covered; `INTEGRATION` is not, because the definition tables are
planted and the three callees supplied; `FULL-SUBSYSTEM` is not, because side A's reset is a
different function and runs on the original side only.

`CONTRACT` was carried as `NOT COVERED` with the reason *"derived from the map below"* — a
placeholder left behind when the harness was written and never reconciled after the map filled in.
`parity_status.py` derives this verdict from `CONTRACT_MAP` and flags a declaration that disagrees,
and it had been flagging this one. All eight behavioural rows are `EXERCISED`; the ninth, *"any
runtime observation"*, is an `OPEN QUESTION` and is excluded from the denominator by the tool's
documented rule, by name and in public. **Nothing about the live gap changed** — that is the
evidence *class* in §13, which is still `isolated original-code`, and this pilot still owes
`FULL-SUBSYSTEM`.

`EDGE-CASE` now also covers a record index of **zero** — the accepted side of the signed guard. It
was added because a mutation survived without it (§13), which is the only reason the gap was visible.

**The suite has been mutation-tested: ~~45 mutants, 34 killed~~ 49 points, 38 killed *(answered: §13's 49-point run supersedes the 45-mutant line; 2026-10-02, OPUS)*, 4 proven byte-identical, 4 adjudicated
equivalent with reasons, 3 refused at compile time by the entry-size check. No unexplained
survivor.** §13 has the table. A reimplementer can therefore treat a disagreement with this
reconstruction as a real difference rather than as a possible gap in the comparison.

**Five things a reimplementer must take from this contract:**

1. **Do not write one bind with a side parameter.** The two differ in *when* they resolve the fifth
   argument, ~~in *what* they resolve it to,~~ *(corrected 2026-10-02, OPUS: both resolve a negative one to 0 — `005C5230` is `xor eax, eax` / `ret`)* in whether they clear the entry's `+0x14`, and in which
   function they call afterwards. Only `clear-one` and `republish` are genuinely one operation twice.
2. **Side B calls out before it validates.** ~~A refused bind is not side-effect-free on the B side.~~ On a refused bind its one extra effect is the call itself, visible only in a call trace *(corrected 2026-10-02, OPUS: `005C5230` is `xor eax, eax` / `ret`)*.
3. **The reverse-lookup subscript is not bounded above.** Reproducing that faithfully reproduces ~~an~~
   ~~out-of-slot write~~ writes past the lookup words into the slot's later fields, and past the `0x288` slot only from subscript 312 *(corrected 2026-10-02, OPUS: a subscript of 250 lands at `+0x20C`, inside the slot)*; adding the bound is a deliberate divergence and must be recorded as one.
4. **`republish` takes two arguments, not three.** The value written into the lookup is the entry
   index itself — `mov word [rcx + rax*2 + 0x18], dx` with `dx` the index. A three-argument
   signature invents a parameter.
5. **Let the entry layout be declared once and derive every access from it.** The offsets and widths
   in §7 are a *struct*, not nine independent facts to retype at each write. Deriving them
   (`offsetof`/`sizeof` over a packed, size-checked declaration) makes a wrong layout a compile
   error instead of a runtime difference — see the three NO_BUILDs in §13.

## 17. Related

- `04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md` §2.4 — the layout.
- `_types/types.tsv` — `ActorManagerSlotEntry`.
- `02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md` §10 — the opposite guard
  discipline in the same codebase.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Script_VM_Native_Bridge — CLIENT, 38 edges: the camera verbs drive the slot entries.** This contract's A-side and
B-side setters (`003DA370`, `003DA400`, `003DA4D0`, `003DA570`, `003DA2D0`; `003DD230`, `003DCF60`, `003DD320`,
`003DD350`, `003DD1F0`) are called only by script-VM verb handlers:
- camera start `camerastart_7d` / `_7e`;
- `resumebehindcamera`;
- camera stop `camerastop_54` / `_53`;
- `camerachange`;
- camera-shake start `camerashakestart_1a2` / `_1a3`;
- camera-shake stop `camerashakestop_19e` / `_19d`;
- `camerashakeclear`;
- `camerashakechange`;
- the two ratio verbs.

Each handler pops its arguments through the native bridge's `VMValueStack_*` accessors. The caller list and what the
shipped scripts pass are in the slot-entry sections above. How a script verb is dispatched is owned by the script VM
pages; this contract owns the entries the verbs write.

**Presentation — SERVICE, seven edges.**
- The A-side tick `003DA050` hands the shot's absolute time to the camera player (`002555A0`, `00257A00`,
  `002567B0`), which in turn calls `00258350`.
- The B-side tick `003DCFB0` passes its accumulated time to the shake sampler `0037D1F0`.

What the camera player renders belongs to the presentation layer's pages.

**RNG_Random_Selection — SERVICE, one edge.** The shake sampler `0037D1F0` draws `RNG_MT19937_NextFloatClosed`: shake
jitter comes from the Mersenne generator, whose draws are mapped in `which-roll-is-on-which-generator`.

**CoreRuntimeScheduling — MECHANICAL, one edge.** `0037D1F0` also calls `001EDDA0`, the shared
mode-flag-and-suppressor predicate of `CONTRACT-boot-fixups`, which gates many unrelated bodies.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page and the cited pages read them; no new body read
(OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-contract-manager-slot-entry-tables-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `0037DD50` | 99 B | `003DCFB0` + 0xA8 | forms the entry `02ADD990 + ecx*0x3D0 + r8d*0xF0` (both indexes sign-extended); when `edx` is -1 stores 2 in its dword `+0xE8`; otherwise reads the zero-extended word `+0x28 + edx*0x60` of the qword at `02ADD980 + ecx*0x3D0`, converts it to float, adds 1.0 (`01CEBBA8`) and stores the result at the entry's float `+8` | Interior anchor `0037DD53`; Interior anchor `0037DD5D`; Interior anchor `0037DD76`; Interior anchor `0037DD98`; Interior anchor `0037DDAC` |
