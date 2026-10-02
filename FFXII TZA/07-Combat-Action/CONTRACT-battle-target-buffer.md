---
contract: hold an ordered set of up to 32 actor references for one action or one AI evaluation
category: 07-Combat-Action
scope: family
level: L1
readiness: DIFFERENTIAL TESTED   # the three operations; no consumer runs and `memset` is supplied — see §13
confidence: PROVEN
implements: 04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md
entries: ["00316CD0", "00316CF0", "00316D70"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 124 addresses cited - 1 data, 26 entry, 97 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-battle-target-buffer-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the battle target buffer

Three functions, twenty-four, fifty-seven and forty-seven bytes long, that between them define a
bounded ordered set. They are a `family` rather than three operations because they share one
structure and one invariant and are meaningless apart: nothing else writes the count, and nothing
else advances the entries.

## 1. Purpose

A battle unit needs to name the actors an action applies to, and the AI needs to name the actors it
is choosing between. Both are "up to thirty-two actors, in the order they were found, with no
duplicates rejected and no growth beyond the cap". Every unit carries two of these buffers: the
action target buffer at `+0x778` and the perception candidate cache at `+0xBC0`.

## 2. Interface

| | |
|---|---|
| entry point(s) | `00316CD0` append (24 B) · `00316CF0` reset (57 B) · `00316D70` find (47 B) |
| calling convention | Microsoft x64; `rcx` = buffer in all three, `rdx` = actor work pointer in append and find |
| parameters | append: `rcx` buffer, `rdx` actor work pointer (never inspected, only stored) · reset: `rcx` buffer · find: `rcx` buffer, `rdx` actor work pointer to match |
| return type | `int32` in all three |
| return semantics | **append** returns the count *after* the call — and this does **not** distinguish success from refusal, see §10 · **reset** returns nothing meaningful · **find** returns the entry index, or `-1` (`00316D97 or eax, 0xffffffff`) when the actor is not present |
| callbacks / indirect dispatch | none; all three are called directly, never through a table |

## 3. Types

`BattleTargetBuffer`, total size **0x208**, ~~never independently allocated — it exists only inline,~~
~~twice, inside `BattleUnit`.~~ inline twice inside `BattleUnit` (`+0x778`, `+0xBC0`) and also as stack locals *(corrected 2026-10-02, OPUS: `AiOrder_EvaluateAndResolveActionTarget` resets a candidate buffer at `[rsp+0x460]` (`00301674`–`0030167C call 00316CF0`) and hands `003087E0` an out buffer at `[rsp+0x40]` (`003017AF`–`003017BF`), which it resets at `0030880E`)*. Layout complete: every byte is either a named field or one of the 32
entries.

| offset | size | field | type | meaning | evidence |
|---|---|---|---|---|---|
| `+0x00` | 1 | `flags` | `uint8` | bit 0 survives a reset; nothing else in the byte does. On `+0xBC0` it is the **"cache current — skip refresh"** gate, read by `00324F32` (`test byte ptr [rdi], 1`, early-return 0 in `00324F20`), born set (`00172CA1` `mov qword [rbx+0xbc0], 1`), re-armed by `00316D30`, never cleared in the verified population | `00316CFA` `movzx ebx, byte ptr [rcx]`, `00316D05` `and ebx, 1`, `00316D10` `and byte ptr [rdi], 0xfe`, `00316D16` `or byte ptr [rdi], bl` |
| `+0x01` | 1 | `keyType` | `uint8` | candidate-buffer selection recipe, high byte: 0 none, 1 int key, 2 float key — meaningful only in the `+0xBC0` selector buffer | `00301ECC` `mov word ptr [r14 + 1], 0x100` (single-entry arm), `003022C7` `mov byte ptr [r14 + 1], 1` |
| `+0x02` | 1 | `pickRule` | `uint8` | candidate-buffer selection recipe, low byte of the second: 0 nearest, 1 random, 2 minimum, 3 maximum | `003022CE` `mov byte ptr [r14 + 2], al` (`setne`/`add 2`), `00301ECC` `0x100` |
| `+0x03` | 1 | — | — | never separately written; the `0x100`/keyed stores and the reset's `word [rdi+1], 0` cover `+0x01..+0x02` only | `00316D1D` `mov word ptr [rdi + 1], 0` |
| `+0x04` | 4 | `count` | `int32` | entries in use; **signed** | `00316CD0` `movsxd rax, dword ptr [rcx + 4]`, `00316D70` same with `test r10, r10 / jle` |
| `+0x08` | 512 | `entries` | `BattleTargetEntry[32]` | 32 × 16 bytes | stride from `00316CD9 add rax, rax` before `[rcx + rax*8 + 8]`, and from `00316D8E add rax, 0x10` |

`BattleTargetEntry`, 0x10:

| offset | size | field | type | meaning | evidence |
|---|---|---|---|---|---|
| `+0x00` | 8 | `actorWork` | `void*` | the stored actor reference; the only part either operation examines | `00316CDC` store, `00316D83` `cmp qword ptr [rax], rdx` |
| `+0x08` | 4 | `entryFlags` | `uint32` | **bit 8 selects the event variant** the HP write dispatches — alive `0x2005`/`0x2006`, dead `0x2007`/`0x2008` | `0030071A mov r13d, dword ptr [rbp + rax*8 + 0x788]` then `shr r13d, 8` / `and r13d, 1` |
| `+0x0C` | 4 | — | — | **unknown span**, not declared padding | no access |

**The three numbers close on each other**: `8 + 32*16 = 0x208`. The size is a literal
(`00316CFF mov r8d, 0x208`), the cap is a literal (`00316CD4 cmp eax, 0x20`), the stride is read two
ways. None of the three is inferred from the others — that they agree is the check, not the method.

## 4. Preconditions · postconditions · invariants

**Preconditions.** `rcx` must point at a `BattleTargetBuffer`. None of the three validates it; there
is no null check in any of the three bodies. `count` is *trusted* by append — it indexes with it
without a lower-bound check, so a negative count would write before the entries (see §10).

**Postconditions.**
- append, accepted: `entries[count'].actorWork == rdx` where `count' = count`, and `count` is one
  greater. Nothing else in the buffer changes — the entry's remaining 8 bytes are **not** written,
  so they hold whatever the last reset or the last occupant left.
- append, refused: **the buffer is completely unchanged.**
- reset: all 0x208 bytes are zero except bit 0 of `flags`, which holds its prior value.
- find: the buffer is unchanged in every case.

**Invariants.** `0 <= count <= 32` holds after any sequence of these three operations starting from a
reset. Entries `[0, count)` are the ones written, in insertion order; entries `[count, 32)` are
whatever the last reset left. The order is insertion order and there is no sort anywhere in the
family.

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | `buffer+0x00`, `buffer+0x04`, `entries[i].actorWork` | `00316CFA`, `00316CD0`/`00316D70`, `00316D83` |
| written | `buffer+0x00` (bit 0 preserved), `buffer+0x01`, `buffer+0x04`, `entries[count].actorWork`, and all 0x208 bytes by reset | `00316D10`/`00316D16`, `00316D1D`, `00316CE1`, `00316CDC`, `00316D0B` |
| allocated | none — the buffers are interior storage inside `BattleUnit` | |
| deallocated | none — **no destructor can exist**; the storage belongs to the unit | |

No globals are touched by any of the three. That is unusual enough to state: the family is entirely a
function of its two arguments.

## 6. Relationships

**Callers of append (7):** `Battle_BuildActionTargetSet` (three sites),
`AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` (two), `BattleUnit_CommitAction`,
`FUN_00313120`.
**Callers of reset (8):** `AiOrder_EvaluateAndResolveActionTarget`, `AiOrder_EvaluateTargetSelector`,
`AiOrder_SelectFinalTargetFromCandidates`, `Battle_BuildActionTargetSet`,
`AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus`, `BattleUnit_CommitAction`,
`BattleUnit_CancelAndResetCurrentAction`, `FUN_00313120`.
**Callers of find (4):** `BattleStats_ModifyHPAndProcessLethalState`, `Battle_BuildActionTargetSet`,
`BattleUnit_HandleActorTimelineEvent` (two sites).

**The perception instance has its own consumer:** `AiOrder_EvaluateAndResolveActionTarget` takes the
address of the `+0xBC0` buffer directly (`00301599 lea r13, [rdi + 0xbc0]`) while evaluating a gambit
condition — so the two instances are used by different halves of combat, the action buffer by the
commit path and the perception cache by the condition path.

**Callees:** only the fill routine `00861EC0`, called by reset. Append and find call nothing.

## 7. State transitions

The buffer has two states that matter to its users, and one edge each way.

| from | to | condition | exact test |
|---|---|---|---|
| any | empty | a reset runs | unconditional inside `00316CF0` |
| accepting | full | the 32nd append is accepted | `00316CD4 cmp eax, 0x20 / jge` refuses from then on |

`BattleUnit_CancelAndResetCurrentAction` resets the action buffer without appending anything, which
is the one caller that uses the empty state as its result rather than as a starting point.

## 8. Script · resource · event interactions

None directly. The buffer is populated from actor queries and consumed by action dispatch; ~~no opcode,~~
~~verb or authored table reaches it.~~ a script verb body reaches it *(corrected 2026-10-02, OPUS: `003495A0` calls `00313120` (`003495B2`), which resets the buffer and appends to it at `0031325F` / `0031328C`; the-moment-an-action-is-committed.md, the Script_VM crossing)*.

## 9. Determinism

**RNG** — none; no path in the family draws.
**Ordering** — entries are in the order the *caller* discovered them, so the family is deterministic
but the buffer's contents are only as deterministic as the query that filled it. **A reimplementation
that sorts, deduplicates, or iterates a set in a different order will diverge here even though this
family is reproduced exactly.**
**Threading** — no synchronisation of any kind, and the buffers are interior to a unit, so the family
assumes it runs on whichever thread owns that unit.

## 10. Failure paths and edge conditions

1. **Append when full.** `count >= 32` returns immediately, changing nothing.
2. **The return value cannot distinguish that refusal from success.** The refused path falls through
   to the shared `ret` with `eax` still holding the count from the `movsxd`, so it returns 32; an
   accepted append into the last free slot increments 31 to 32 and returns 32 as well. **A caller
   cannot tell "I filled the last slot" from "I was refused" by the return value alone** — it must
   compare against the count it had before, or re-`find` the actor. Any reimplementation returning a
   boolean, or `-1` on refusal, is wrong and will silently change caller behaviour.

   **REFINED 2026-09-11 by executing it.** ~~so it returns 32~~ — it returns **whatever the count
   currently is**, which is 32 only when the count is exactly 32. Measured on the shipped body:

   | count on entry | outcome | returns |
   |---:|---|---:|
   | 31 | accepted | **32** |
   | 32 | refused | **32** ← the indistinguishable pair |
   | 33 | refused | **33** |
   | 40 | refused | **40** |
   | 100 | refused | **100** |

   Nothing in the family can produce a count above 32, so the distinction never arises in the
   shipped game — but "no caller can produce it" is a statement about callers, and this is a
   contract about a function. A reimplementation that returns a literal `32` on refusal is wrong
   in a way the original is not.

3. **Negative count.** Append does not check the lower bound and indexes with a sign-extended value,
   so a negative count writes *before* the entry array. No caller produces one — only these three
   functions write the count and none can make it negative — but the protection is the family's
   closure, not a check, and a reimplementation that exposes the count to anything else loses it.

   **And the append is ACCEPTED, not refused** — verified 2026-09-11 by executing it with the 32
   bytes in front of the buffer planted and compared. A count of `−1` passes the upper-bound test,
   stores the actor sixteen bytes before `entries[0]`, increments to `0`, and **returns 0**. So a
   single append both corrupts memory outside the structure *and* silently repairs the count, which
   is the worst of the two possible behaviours for anyone trying to detect it afterwards: the
   buffer looks empty and consistent, and the damage is somewhere else.
4. **Find on an empty or negative buffer** returns `-1` without touching memory (`test r10, r10 / jle`).
5. **Duplicate appends are accepted.** Nothing in append consults `find`; the same actor can occupy
   several entries. The set is ordered and bounded, not unique.
6. **Find matches on the pointer only** and ignores `state`, so it returns the *first* entry holding
   that actor.

## 11. Observable behaviour

From outside the process, in memory: after a reset the 0x208 bytes at `unit+0x778` (or `unit+0xBC0`)
are zero except bit 0 of the first byte; after N accepted appends the dword at `+0x77C` reads N and
the qwords at `+0x780 + 16*i` hold the appended pointers in order. A test can drive an action that
targets more than 32 actors and confirm that the 33rd is absent and the count stops at 32.

## 12. Reproduction formula

```
append(buf, actor):
    n = (int32)buf[0x04]
    if n >= 32: return n              # unchanged, and see §10.2
    *(void**)(buf + 8 + 16*n) = actor # only the first 8 bytes of the entry
    buf[0x04] = n + 1
    return n + 1

reset(buf):
    keep = buf[0x00] & 1
    memset(buf, 0, 0x208)
    buf[0x00] = keep                  # the code also re-clears bit 0 and re-zeroes +0x01; both
                                      # are redundant after the fill and change nothing
find(buf, actor):
    n = (int32)buf[0x04]
    if n <= 0: return -1
    for i in 0 .. n-1:
        if *(void**)(buf + 8 + 16*i) == actor: return i
    return -1
```

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent.** (2026-09-11)

All three shipped bodies have been executed at their real virtual addresses under Unicorn against an
independent reconstruction. **No live process has been involved at any point**, which is what still
holds `RUNTIME VALIDATED` open. This section previously read *"Empty"* and said that nothing here
had been seen in a running game; that is still true of the live class and is now false of the
isolated class. The superseded wording is quoted in full at the end of this section, and **not
here** — for a reason worth reading, because it caught this contract mis-classifying itself.

**Instrument:** [`Reconstruction/Tests/Differential/diff_target_buffer.py`](../../../Reconstruction/Tests/Differential/diff_target_buffer.py)
against [`Reconstruction/Game/Combat/target_buffer.c`](../../../Reconstruction/Game/Combat/target_buffer.c).

**Result: 156 commands, 124 compared lines, 0 mismatches.** The comparison is mostly **memory**:
27 dumps of all **0x208 bytes** (20 of them distinct) and 16 dumps of the 32 bytes in front of the
buffer (3 distinct — so the out-of-bounds write in §10.3 was *observed*, not merely permitted),
alongside 66 append returns and 15 find results.

**One call is supplied, and it is `memset`.** The reset calls `00861EC0`, which the function table
names `memset` in six bytes — a jump thunk. It is hooked and performed by the harness rather than
emulated: the CRT's real `memset` is a hand-written SIMD routine whose behaviour is not this game's,
and emulating it would be testing Unicorn. The reconstruction calls the C library's. Both sides get
"the region is zeroed", which is what §5 claims, and neither gets to disagree about how.

| what was executed | outcome |
|---|---|
| the whole accepting range, 0 → 32 appends, with the buffer dumped at each edge | **agrees** |
| the cap refusal, and that it changes **none** of the 520 bytes | **agrees** — which the return value could not have shown |
| §10.2's indistinguishable return, and its refinement above at counts 33/40/100 | **agrees** |
| §10.3's negative count, with the 32 bytes in front compared | **agrees**, and the append is *accepted* — see §10 |
| §10.4 find on empty and on `−3`, with the dump proving nothing moved | **agrees** |
| §10.5 duplicates accepted, §10.6 find returning the **first** | **agrees** |
| reset preserving `flags` bit 0 and nothing else, over five flag patterns from a `0xCD`-filled buffer | **agrees** — 518 of 520 bytes zero, bit 0 surviving |

**Claims about the bytes, re-derived on every run:** the cap `0x20` as a literal in the append body,
the size `0x208` as a literal in the reset body, the stride `0x10` as a literal in the find body,
and that `8 + 32*16` is `0x208`. The contract's §3 says these three close on each other and that
their agreement is the check rather than the method; the harness re-checks it rather than
inheriting it.

**One layout trap worth naming.** The `+0x01` field is **unaligned** — `00316D1D` is a 16-bit store
at offset one. A naturally-aligned C struct puts it at `+0x02`, moving the count to `+0x06`, the
entries to `+0x0A`, and making the structure `0x20A`. Every byte comparison in this test would then
compare the wrong bytes and still pass, because both sides would be self-consistent. The
reconstruction is packed and asserts `sizeof == 0x208` at compile time.

### What is still owed, and it is live-only

1. **Does any caller ever hand this family a count it did not write?** §10.3's protection is the
   family's closure, not a check. A watchpoint on one unit's `+0x77C` across a battle would show
   whether anything outside the three functions writes it.
2. **`entryFlags` bit 8, and the `+0x0C` span.** Bit 8 is read by the HP write to select the event
   variant; nothing in this family writes it, so **something else fills it** ~~and this contract does~~
   ~~not say what.~~ *(answered: `Battle_ProcessActionTarget` ORs `0x100` into the entry's `+8` at `003075CB` when the result's flag word B bit 3, knockback, is set - see THE WRITER IS KNOWN below; 2026-10-02, OPUS)* `+0x0C` has no access anywhere at all.
3. ~~**`+0x01` has no reader anywhere in the image, and that is now measured, not assumed**~~ **`+0x01` has a reader, on a stack instance** *(corrected 2026-10-02, OPUS: `00308813 movzx edx, byte ptr [rsi + 1]` in `003087E0`, where `rsi` is `003014C0`'s stack candidate buffer `[rsp+0x460]`; item 3 of the list verified owner-side 2026-09-22 below)*
   (OPUS 2026-09-16). §5 lists the word as written and never read; the open question was
   whether something *outside* this family reads it. ~~It does not. The buffer is never~~
   ~~independently allocated, so any outside reader must reach the word through an inline base~~ *(corrected 2026-10-02, OPUS: stack instances exist, `[rsp+0x460]` and `[rsp+0x40]` in `003014C0`, so this scan's inline bases could not see the reader at `00308813`)*
   — `unit+0x779` or `unit+0xBC1`. Decoding every one of the **38,161** function bodies for
   any access whose byte range overlaps that word, at either base and **at any size**, gives
   **zero** 2-byte accesses at `+0x779`/`+0xBC1` and 32 wider overlaps at
   `+0x770`/`+0x778`/`+0xBBC`/`+0xBC0`. The 32 are a **false-positive class**: the 21
   functions holding them are *disjoint* from the 9 that demonstrably form a battle-unit
   buffer address — the scan's positive control, 20 `lea` sites including
   `BattleUnit_CommitAction` (`0030F7A7`) and `AiOrder_BuildCandidateTargetBuffer`
   (`0030F163`) — and they `movss`/`movups`/`movq` the same displacement in unrelated
   structures. ~~**The field stays UNRESOLVED on purpose.**~~ *(answered: resolved, the candidate buffer's selection recipe - see item 3 of the list verified owner-side 2026-09-22 below; 2026-10-02, OPUS)* A field with no reader has no role
   to name, and a gap is a question, never a label. What would resolve it is a reader.

4. **Which of the two instances is which, in a running unit.** §6 says the action buffer serves the
   commit path and the perception cache the condition path; that is a reading of the callers, not
   an observation.

Queued; the live-automation pause stands.

### ⚠ The superseded wording, and why it is down here

This section used to begin: *"Empty — nothing in this contract has been **observed live**."*

When the executed result was written above it, that sentence was kept as struck-through text at the
top — the ordinary way to show a correction. **`check_gate26.py` then classified this contract as
`live or controlled experiment`,** and the runtime-validated count went from 5 to 6.

`LIVE_RE` searches the first 400 characters of §13 for phrases including `observed live`, and it is
tested **before** `ISOLATED_RE`. The struck-through denial contained the trigger. Markdown
strike-through is a visual convention; a regex does not see it.

**So a correction that was honest to a reader claimed live evidence to the instrument** — in a
contract that has none, for a subsystem nothing has ever observed running. That is the dangerous
direction: the same instrument's earlier under-count merely hid work, and this would have inflated
the one number that gates a phase change.

Two rules follow, and they are general:

- **Do not leave a superseded evidence phrase in the first 400 characters of §13.** Put it below the
  new result, as here.
- **Re-run `check_gate26.py` after editing any §13 and read the class it lands in**, not just the
  totals. A contract moving into the wrong class is invisible in a total that went up by one.

<!-- OPUS-MUT-S13-RESTATE -->
### Mutation campaign, re-run 2026-09-12 on the full literal surface

**21 generated points: 10 KILLED · 1 SURVIVED · 5 EQUIVALENT · 5 NO_BUILD · 0 TIMEOUT · 0 INVALID. Verdict `FAIL`.**
Receipts: `Database/Tools/work/OPUS/litsuffix/target_buffer` (ignored path). Instrument: `Reconstruction/Tests/mutation_test.py`. The table for every pilot, and the four kinds a survivor can be, are on [`MUTATION-CAMPAIGNS.md`](../../../Reconstruction/MUTATION-CAMPAIGNS.md).

The single survivor is **kind A, provably equivalent**: `count <= 0` → `count < 0` differs only at `count == 0`, where the early return and a zero-iteration loop both return `-1`. The guard is redundant with the loop, which is a fact about the original worth having rather than a gap — the comment claiming *“one test covers empty and negative”* is right about coverage and beside the point about this mutant. The five `NO_BUILD` are comparison flips the compiler rejects.

**Experiment records that name this contract** — found by `OPUS-CONTRACT-RUNTIME-AUDIT`, 2026-09-13. Each names this
contract in its own `contract:` frontmatter while this section did not cite it back.

- [`EXP-043`](../_experiments/EXP-043-target-buffer-boundary.md) — **method B**, isolated original-code execution.
- [`EXP-046`](../_experiments/EXP-046-target-buffer-reset.md) — **method B**, isolated original-code execution.

**None of these is a live run**, so none of them changes the evidence-class statement at the
top of this section. They are listed because a reader auditing what has been executed against
this contract should not have to find them from the experiment side only.

## 14. Unresolved

1. ~~**What `flags` bit 0 means** — the bit the reset deliberately preserves. Resolving it needs the
   readers outside this family; it is the only piece of buffer state that survives a reset, so it is
   the only place a reimplementation can go wrong across action boundaries.~~ **CORRECTED
   2026-09-22 (SWE2-CONTRACT) — the note below's "one setter and no reader" is wrong on both
   counts; the bit is a live gate.** Bit 0 is the perception cache's **"generation is current —
   skip the refresh"** flag, and it is consumed: `BattlePerception_RefreshCandidateCacheGeneration`
   (`00324F20`, the refresh's only caller path is `003247F0` behind the `01EED154` global gate)
   tests it at **`00324F32 test byte ptr [rdi], 1`** — `rdi = unit+0xBC0` from `00324F2B` — and
   returns `0` without touching the cache when set. **There are two setters, not one:**
   `00316D30`'s `or byte ptr [rcx], 1` (called only on `+0xBC0` by `BattleUnit_ResetStateForReuse`
   `00236A85` and `BattleUnit_UpdateCombatFrame` `003087C6` — both verified) **and the unit
   initializer `00172C30`** (called from `0016F2A0`), which writes `mov qword ptr [rbx + 0xbc0],
   1` at `00172CA1` — the bit is **born set** on the perception buffer, with recipe `0` and
   `count 0` beside it. **No clearer exists** in the verified population: every reset is
   preserve-shaped (`00316CF0`, `00316D30`, the `0032483F` inline reset, and `00324F20`'s own
   tail at `00324FD7`–`00324FF3` all do `movzx`/`and 1`/memset/`and 0xFE`/`or`), every `+0xBC0`
   displacement site image-wide is enumerated (leas, the ctor store, non-unit objects' `+0xBC0`
   pointer fields), and every function holding the buffer pointer was scanned for a byte-0 write —
   none. So on the shipped path the bit stays 1 from construction and `00324F20`'s work arm never
   runs — either that arm is dead-in-ship, or a clearer hides behind a route the census cannot see
   (a second-hop or stored pointer; named as the residual). On `+0x778` the bit is born `0`, never
   set, never read — inert.
   > *Answered by census 2026-09-12 (FABLE, E-6; a note only).* The bit has **one setter and no
   > reader**. A second reset variant, `00316D30` (60 B, the twin of `00316CF0` with `or byte ptr
   > [rcx], 1` in front of the same preserve-fill-restore sequence, `00316D3A`–`00316D60`), sets it
   > and is called only by `BattleUnit_ResetStateForReuse` (`00236A85`, on the `+0xBC0` buffer) and
   > `BattleUnit_UpdateCombatFrame` (`003087C6`, `+0xBC0`); `BattleUnit_RebuildPerceptionCandidateCache`
   > inlines the preserving reset on `+0xBC0` (`0032485E`–`00324879`). An image-wide displacement
   > census of both buffers' header bytes (unit `+0x778`, `+0xBC0`; [the battle-unit field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)) finds only
   > `lea`s that pass the buffer, and no `test` of bit 0 anywhere — neither through the unit nor
   > through the buffer pointer in the family or in the four functions that receive one
   > (`BattleStats_ModifyHPAndProcessLethalState`, `BattleAction_UpdateSpecialPresentationSequence`,
   > `00309990`, the selector evaluator). So bit 0 is a **"has been reset by the reuse / frame path"
   > marker that nothing consumes** in the shipped image; a reimplementation may carry it for
   > fidelity but cannot diverge on it.
2. ~~**What `entries[i].state` holds and who writes it.** No instruction reached through the unit
   census touches entry `+0x08` on its own; the entries are read whole with a 16-byte `movups`. The
   writer is somewhere the unit census does not reach.~~ **Verified owner-side 2026-09-22
   (SWE2-CONTRACT): the folded answer stands — `+0x08` is the outcome word, written through the
   entry pointer.** Confirmed at the image: `003075BA call 0030DAE0` (MapOutcomeToTargetEntryCode)
   then `003075BF mov byte ptr [r14 + 8], al`, `r14` = the entry handed down in `r9` from
   `Battle_ProcessActionTargetEntry`'s per-entry call — exactly the folded-offset shape every
   displacement census misses — followed by the flag-bit ORs (`003075CB or dword [r14+8],0x100`
   under `test al,8`, et seq.).
   > *Narrowed 2026-09-12 (FABLE, E-7; a note only).* Three readers, all through the unit and the
   > entry index (`[unit + i*16 + 0x788]`): `Battle_EmitReactionPresentationForSlot` maps states
   > **1–10** through a ten-arm jump table onto five battle-message ids — `0x2037`, `0x2039`,
   > `0x203A`, `0x203B`, `0x203C` — and posts one through `003299B0(unit, id, entry.+8)`
   > (`00317783`–`003177CF`); `00322760` treats **8** as "result ready" and only then encodes the
   > paired handle at `[unit + i*16 + 0x988]` (`00322810`–`00322827`); and `0031ADB0` turns state
   > **10** into bit 4 of a display word `[+0x3C]` (`0031B44F`–`0031B463`). Writers: none by unit
   > displacement (the image-wide census of `[base + idx*8 + 8]` byte stores finds only unrelated
   > records), so the state is written through the buffer pointer or by whole-entry copies; the one
   > immediate store of a state-sized value in the battle range (`0033F3A6`, `mov byte ptr [rdi+8], 1`
   > in `0033F330`) belongs to a record whose identity is not established. **THE WRITER IS KNOWN, and the reason every census missed it is the finding.** `+0x08` is written through the **ENTRY POINTER**, never through a unit displacement, which is exactly why an image-wide census of `[base + idx*8 + 8]` byte stores found nothing: `Battle_ProcessActionTargetEntry` (`003191B0`) takes ONE entry in `rdx` — its callers walk `unit + 0x780` in 16-byte steps — and hands it to `Battle_ProcessActionTarget` (`00307300`, `r14 = r9` at `00307337`), which stores `BattleFormula_MapOutcomeToTargetEntryCode(result kind)` at **`003075BF`**, `mov byte ptr [r14 + 8], al`, then the flag bits 8-11 above it at `003075CB`-`003075F9`. **So a census keyed by displacement cannot see a field written through a pointer the caller already holds, and absence in such a census is not absence in the image.** Folded from FABLE's E-7 note by OPUS 2026-09-13.
   > *Answered 2026-09-12 (FABLE, E-7). **FOLDED INTO THE CONTRACT BY OPUS 2026-09-13** — no longer a note awaiting revision; the item above carries it.* **The writer
   > was already on two other pages and the ledger was never reconciled with them.** The byte is
   > written through the **entry pointer**, which is why every census by unit displacement or by
   > `[base + idx*8 + 8]` misses it: `Battle_ProcessActionTargetEntry` (`003191B0`) receives one
   > entry in `rdx` (its callers walk `unit + 0x780` in 16-byte steps) and hands it on in `r9` to
   > `Battle_ProcessActionTarget` (`00307300`, `r14 = r9` at `00307337`), which reads the old code
   > (`00307552`, through `BattleFormula_MapTargetEntryCodeToOutcome` `002FEE20`), resolves the
   > target through `BattleFormula_ResolveTargetResult` (`00307577`), and stores
   > `BattleFormula_MapOutcomeToTargetEntryCode(result kind)` at **`003075BF`** (`mov byte ptr
   > [r14 + 8], al`), then the flag bits 8–11 above it (`003075CB`–`003075F9`). So `+0x08` is the
   > **outcome word**: byte 0 the *target-entry code* (result kind 0 → 0, 5 → 1, 1 → 2, 3 → 3,
   > 2 → 4, 4 → 5, 6 → 6, 7 → 7, 8 → 8, `0xB` → 10, `0xA` → 9, 9 → 11; `0030DAE0`), bits 8 / 9 / 10
   > knockback / ~~parry~~ counter / combo-continues and bit 11 the result's flag word B bit 0 — the
   > ~~mode-2 resource-reaction chance rolled~~ ranged critical rolled *(corrected 2026-10-02, OPUS: bit 9 is `0x200` from flag B bit 2 at `003075E8`–`003075EC`, the counter flag; bit 11 is flag B bit 0, which `00389140` sets on the ranged critical, `003891B7`–`003891D9`; Result-Record/the-result-record-field-map.md row `+0x018`)* (`test r12b, al` at `003075F4`, `r12d` pinned
   > to 1 at `0030746E`, ORs `0x800` at `003075F9`; FT-4) — as [the battle-unit field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) (`+0x788`,
   > *entries[0].outcome*) and [the formula scratch block](../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) §2.6 already record. A second census today of every
   > store width and mnemonic to `+0x788` / `+0x790` displacements, every unscaled `[base + idx +
   > 0x788]` shape, every 16-byte store into an entry with its feeding load, and every byte store
   > through a `lea`'d entry pointer in `002F0000`–`003A0000` finds no other writer of the code
   > byte; the 16-byte copies in `AiOrder_EvaluateTargetSelector` and
   > `AiOrder_SelectFinalTargetFromCandidates` move whole entries between buffers, and the reset
   > zeroes the word. Two corrections to the narrowing note above: the reaction reader's third
   > argument is the **unit's** `+8` (`003177C8 mov r8d, [rdi + 8]`, `rdi` = the unit), not the
   > entry's; and code **8 is result kind 8**, which §2.6 leaves unnamed — on it
   > `Battle_ProcessActionTargetEntry` finds the entry's index by pointer (`003192E3`–`00319301`),
   > requires a non-null qword at **`unit + 0x988 + 16·idx`** and re-enters itself on that
   > 16-byte record as the entry (`0031931A`–`0031932E`, second-pass flag `r14d = 1`, which skips
   > the resource consumption), while `00322760` encodes the same qword as an actor handle only when
   > the code is 8 (`00322810`–`00322827`). So `+0x988` is a **32 × 16-byte array of redirected
   > entries paired 1:1 with the buffer's entries**, consulted only for code 8; what kind 8 is in
   > the game's words stays with §2.6. The name `state` should become `outcome` (byte 0 `code`).
3. ~~**What the `uint16` at `+0x01` holds.** Written only by the reset, which zeroes it.~~
   **Verified owner-side 2026-09-22 (SWE2-CONTRACT): the folded answer stands — it is the
   candidate buffer's selection recipe, two bytes.** Confirmed at the image: the single-entry arm
   writes `mov word ptr [r14 + 1], 0x100` (`00301ECC` — `keyType` 0, `pickRule` 1); a keyed arm
   writes `byte [r14+1] = 1` then `setne`/`add 2`/`mov [r14+2]` (`003022C7`–`003022CE`) and stores
   the sort key by the displacement-0 `mov dword [r14 + rax*8], ecx` with `rax = 2·(count+1)`
   (`003022E5`–`003022EF`); the reader `AiOrder_SelectFinalTargetFromCandidates` switches on
   `byte [rsi+1]` at `00308813`. So `+0x01` = `keyType` {0 none, 1 int, 2 float}, `+0x02` =
   `pickRule` {0 nearest, 1 random, 2 minimum, 3 maximum} — meaningful only in the candidate
   buffer, where entry `+8` is the sort key, not an outcome.
   > *Narrowed 2026-09-12 (FABLE, E-8; a note only).* It is written outside the resets: the target
   > selector evaluator `AiOrder_EvaluateTargetSelector` stores its running candidate index
   > `r13w` there at **twelve** exits (`00301C40`, `00301CFE`, `00301F48`, `00302119`, `00302199`,
   > `003021C2`, `003021E2`, `00303017`, `0030306F`, `00303556`, `003035AC`, …) and the literal
   > **`0x100`** in one arm (`00301ECC`), and `BattleUnit_RebuildPerceptionCandidateCache` stores the
   > same register into the `+0xBC0` buffer's word (`0032487C`); `BattlePerception_RefreshCandidateCacheGeneration`
   > zeroes it (`00324FF7`). The `0x100` store says the field is **two bytes, not one number**: byte
   > `+1` and byte `+2` — **and what this contract said they held was WRONG.**
   >
   > **CORRECTED 2026-09-13 (OPUS, folding FABLE's E-8 note and re-verifying it at the image).** This
   > text called `+1` "the index the walk reached". It is not an index: `r13` is the ZERO REGISTER —
   > `00301B41 xor r13d, r13d`, and `00301B55 lea ebp, [r13 + 1]` uses it as a zero base — so the
   > twelve `mov word ptr [r14 + 1], r13w` stores write **0, not a running index**. They mark a
   > **non-keyed filter**.
   >
   > The word is the candidate buffer's **selection recipe**, and the keyed arms write its two bytes
   > separately: `byte [r14+1] = 1` for an **integer key**, `= 2` for a **float key**; then `byte
   > [r14+2] = 2 + polarity`, **2 take the minimum, 3 take the maximum**, from the selector row's
   > inverted bit (`00301B44 not r12d` / `00301B4C and r12d, 1`). Its one reader is
   > `AiOrder_SelectFinalTargetFromCandidates` (`003087E0`).
   >
   > **A wrong reading here was worse than an open question**, because "the index the walk reached"
   > is a plausible sentence that a reimplementation would have built on, and the field it describes
   > is zero at every one of those twelve sites.
   > *Answered 2026-09-12 (FABLE, E-8). **FOLDED INTO THE CONTRACT BY OPUS 2026-09-13** — no longer a note awaiting revision; the item above carries it.* **The word
   > is the candidate buffer's selection recipe — byte `+1` the key type, byte `+2` the pick rule —
   > and its one reader is `AiOrder_SelectFinalTargetFromCandidates` (`003087E0`).** Correction
   > first: `r13` in the selector is the **zero register** (`xor r13d, r13d` at `00301B41`; the same
   > register zeroes `count` beside each store), so the twelve `r13w` stores write **0**, not a
   > running index — a non-keyed filter. The keyed arms write the two bytes separately: `byte [r14+1]
   > = 1` for an **integer key** at `003022C7`, `0030236D`, `0030259D`, `003026D3`, `00302E4B`,
   > `00302EDF`, `0030325A`, and `= 2` for a **float key** at `003027F4`, `00302888`, `0030290B`,
   > `0030298D`, `00302A3C`, `00302B86`, `00302BFB`, `00302CE5`, `00302D7A`; each then stores
   > `byte [r14+2] = 2 + (polarity bit)` — **2 = take the minimum, 3 = take the maximum** — from the
   > selector row's inverted bit (`r12d`, `00301B44`–`00301B4C`), copies the candidate entry in
   > (`movups`), and writes the **key into the copied entry's `+8`** by a displacement-0 store that
   > every `+8` census missed: `mov dword ptr [r14 + rax*8], ecx` with `rax = 2·(count+1)`
   > (`003022E5`–`003022EF`; the float arms store `xmm6` the same way after `minss` / `maxss`
   > over the row's scalar, `003027A8`–`003027AE`). The single-entry arm writes `0x100` (`00301ECC`):
   > no key, rule **1 = random**. `BattleUnit_RebuildPerceptionCandidateCache` (`0032487C`) and
   > `BattlePerception_RefreshCandidateCacheGeneration` (`00324FF7`) write 0 — the perception cache
   > carries no recipe — and the reset's `mov word [rdi+1], 0` is the same field. **The reader**:
   > `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`) builds the candidates into a **stack**
   > buffer (`[rsp+0x460]`) and calls `003087E0(unit, candidates, out = [rsp+0x40], actionId)` at
   > `003017BF` — the only call site. That function resets `out`, then switches on `+1` (`00308813`):
   > **0** copies every eligible candidate (`00308825`–`0030886C`); **1** keeps the entries whose
   > integer `+8` is the extremum — rule 3 seeds `0x80000001` and keeps the greatest (`003089D7`–
   > `00308A61`), rule 2 seeds `0x7FFFFFFF` and keeps the least (`00308A73`–`00308AF4`) — ties
   > appended; **2** does the same on the float `+8` (`comiss`, seed the `.data` float `02F973B8` or
   > its negation, `00308882`–`003089BC`). Eligibility on every path is
   > `BattleAction_CheckTargetEligibility` (`003083B0`). With more than one survivor, rule **1**
   > returns `LCG % count` (`00308B0D`–`00308B1C`, `RNG_SharedGameplayLCG_NextU32`); otherwise the
   > **nearest by squared XZ distance** from the actor's `+0xE0` (`00308B3E`–`00308B76`,
   > `Vector3_ComputeSquaredXZDistance`), index returned. So `+0x01` = `keyType` {0 none, 1 int,
   > 2 float}, `+0x02` = `pickRule` {0 nearest, 1 random, 2 minimum, 3 maximum}, meaningful only
   > in the candidate buffer the selector fills, and entry `+8` in that buffer is the **sort key**,
   > not an outcome — the same slot means different things in the two buffer roles. *Not
   > established:* the value of `02F973B8` (outside the file image; by role the positive float
   > extremum), and the game's names for the rules.

## 15. Evidence

> **The tier column was reworded 2026-09-11**, for the same reason as the gambit walk's: every row
> read *"static, isolated original code"* while §13 read *"Empty"*, which is only consistent if the
> phrase meant *the shipped bytes, read* — and it did. Now that they have been **run**, the column
> separates **`static`** (decoded) from **`executed`** (run and compared against a reconstruction).
> No confidence changes.

| claim | evidence | tier | confidence |
|---|---|---|---|
| size 0x208 | `00316CFF mov r8d, 0x208` as the fill length; **executed** — all 520 bytes compared on 27 dumps, and the reconstruction asserts the size at compile time | 1 (static + **executed**) | PROVEN |
| cap 32 | `00316CD4 cmp eax, 0x20 / jge`; **executed** across the whole accepting range and past it | 1 (static + **executed**) | PROVEN |
| stride 16 | `00316CD9 add rax, rax` with `[rcx + rax*8 + 8]`; independently `00316D8E add rax, 0x10`; **executed** — every entry position depends on it | 1 (static + **executed**) | PROVEN |
| count is signed | `movsxd` in both readers — `00316CD0` in add and `00316D70` in find; `jle` guard at `00316D7D`; **executed** at `−1`, `−2` and `−3`, where the sign is what puts the write outside the structure | 1 (static + **executed**) | PROVEN |
| flags bit 0 survives reset | `00316CFA` / `00316D05` / `00316D10` / `00316D16`; **executed** over five flag patterns from a `0xCD`-filled buffer, with all 520 bytes compared after | 1 (static + **executed**) | PROVEN |
| flags bit 0 is the `+0xBC0` refresh-skip gate | **CORRECTS the 2026-09-12 census note** ("one setter and no reader"): `00324F32 test byte ptr [rdi], 1` in `BattlePerception_RefreshCandidateCacheGeneration` early-returns 0 when set — a real consumer; and the bit is born set by `00172CA1 mov qword ptr [rbx + 0xbc0], 1` in unit initializer `00172C30`, plus `00316D30`'s `or byte ptr [rcx], 1` via `00236A85`/`003087C6` — two setters, both verified. No clearer exists in the enumerated population (all `+0xBC0` displacement sites; byte-0 scan of every buffer-holding callee), so the work arm is dead-in-ship unless a clearer hides behind an unenumerated pointer route. On `+0x778` the bit stays 0 and is never read | 1 (static — the consumer/setter paths are outside this pilot) | PROVEN |
| find returns -1 when absent | `00316D97 or eax, 0xffffffff` before `ret`; **executed** | 1 (static + **executed**) | PROVEN |
| find returns the index when present | `00316D9B mov eax, r9d`; **executed**, including the first-of-three-duplicates case | 1 (static + **executed**) | PROVEN |
| a consumer relies on the `-1` | `00300710 cmp eax, -1 / je` in `BattleStats_ModifyHPAndProcessLethalState`, which searches the source's buffer and skips the bit fetch on not-found | 1 (static — **the consumer is not run here**) | PROVEN |
| the return cannot distinguish refusal | both paths reach `00316CE7 ret`; the refused path arrives with `eax` = count; **executed**, and the refusal was found to return the count rather than a literal 32 — see §10.2 | 1 (static + **executed**) | PROVEN |
| two instances per unit | `BattleUnit +0x778` and `+0xBC0` in `_types/fields.tsv` | 1 (static — **not exercised**; the harness plants one standalone buffer) | PROVEN |
| caller sets | `callers.py` E8/E9 census with a positive control on `002EF2B0`. **Re-measured 2026-09-11: 121 SITES in 70 FUNCTIONS.** `check_consistency.py` flags a disagreement between this page and `03-World-Area-Field/Weather/weather-apply-and-environment-materialization.md`; there is **none**. Both figures are correct and neither stated which quantity it counted — one is the site count, the other the distinct-function count. The two pages should each say which. `memcpy` control: 632 sites | 1 (static — a census is **not** an execution) | PROVEN  **§15a, 2026-09-12:** those are the CONTROL's figures — `002EF2B0` is `SaveImage_GetPersistentPayloadBase`, a save-image helper with no path to this buffer — and this row never measured its own subject. **The buffer's caller set is 19 sites in 10 functions** (`add` 7/4, `reset` 8/8, `find` 4/3; §15a names them). The `memcpy` control reproduces at **632** exactly under a decoded-`call` rule |
| nothing runs live | — | none | — |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Independent census: capstone over `functions.tsv`, **per function** (38,161 functions, 1,787,590
instructions, **0 skipped**), counting **decoded `call` instructions with an immediate target** —
not raw `E8`/`E9` bytes, which fall inside displacements and immediates and produced a 171-for-40
miscount earlier in this sweep.

**The control fixes the rule.** `memcpy` reproduces at **632 sites** exactly — the figure §15 states —
only when tail `jmp`s are excluded; counting them gives 637. So the rule is decoded `call`, and it is
now stated rather than left to be guessed.

### A refutation I did not make

At a glance the `caller sets` row reads as claiming this buffer has **121 sites in 70 functions**.
It does not: those are the figures of its **positive control**, `002EF2B0`
`SaveImage_GetPersistentPayloadBase` — a save-image helper, owner `Save_Load_Settings`, with no path
to this buffer — and my census reproduces them exactly, 121 and 70. **The row is reporting that its
control held.** Reading it twice was the difference between a correction and a false accusation.

One thing in its reconciliation *is* wrong, though. The row says of the `check_consistency` flag that
*"neither stated which quantity it counted"*. The weather page states both, explicitly and with
attribution: *"70 distinct calling functions … those 70 functions contain 121 call sites, which is
the number the actor-record page quotes."* The ambiguity was on one side only.

### What the row never measured: this buffer's own callers

**19 sites in 10 functions**, and the set is coherent — every one is battle or AI:

| caller | uses |
|---|---|
| `00300530 BattleStats_ModifyHPAndProcessLethalState` | `find` |
| `003014C0 AiOrder_EvaluateAndResolveActionTarget` | `reset` |
| `00301AD0 AiOrder_EvaluateTargetSelector` | `reset` |
| `003087E0 AiOrder_SelectFinalTargetFromCandidates` | `reset` |
| `0030D160 Battle_BuildActionTargetSet` | `add` · `find` · `reset` |
| `0030F130 AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` | `add` · `reset` |
| `0030F760 BattleUnit_CommitAction` | `add` · `reset` |
| `003105D0 BattleUnit_CancelAndResetCurrentAction` | `reset` |
| `00313120 FUN_00313120` | `add` · `reset` |
| `00319F50 BattleUnit_HandleActorTimelineEvent` | `find` |

Per entry point: `add` `00316CD0` **7 sites / 4 functions**, `reset` `00316CF0` **8 / 8**, `find`
`00316D70` **4 / 3**.

> **This corroborates an existing claim from a new direction.** §15 says *"a consumer relies on the
> `-1`"*, citing `00300710` inside `BattleStats_ModifyHPAndProcessLethalState`. That function is in
> the independently-derived caller set, and `find` is the entry point it calls — the claim's consumer
> and the census's caller are the same function, arrived at two different ways.

**Only one caller is unnamed** (`FUN_00313120`), and `Battle_BuildActionTargetSet` is the sole
function using all three entry points — the shape you would expect of the buffer's owner.

**Not claimed:** no live observation and no new execution; §13 is unchanged and the pause holds.

## 16. Parity plan

`STRUCTURAL` — the 0x208 layout and the 16-byte stride, checked by reading a live unit's two buffers.
`CONTRACT` — drive an action at more than 32 targets and assert the count saturates at 32, the 33rd
actor is absent, and the buffer is byte-identical before and after the refused append.
`STATE-TRANSITION` — reset, then append, then cancel, asserting that bit 0 of `flags` is the only
thing that crosses a reset.
`EDGE-CASE` — append the same actor twice and assert both entries exist and `find` returns the lower
index.

**Three of the four are done offline** — see §13. `STRUCTURAL`, `CONTRACT` (as the refusal case),
`STATE-TRANSITION` and `EDGE-CASE` are all covered by the differential run; the one that is **not**
is the first plan item's *"by reading a live unit's two buffers"*, because the harness plants a
standalone buffer and never constructs a `BattleUnit`. That distinction is kept rather than blurred:
the layout is proven, its **placement inside the unit** is not, and those are different claims.

**Four things a reimplementer must take from this contract:**

1. **Append returns the count, not a status.** Not a bool, not `-1`, and on refusal not a literal
   `32` — the count it was handed. A caller distinguishes refusal from success by comparing with
   the count it held before, or by re-`find`ing.
2. **Do not add the lower-bound check.** A negative count is *accepted*, writes before the array,
   and leaves the count at 0. Adding the check is a divergence; it may well be the right divergence
   for a reimplementation, but it must be recorded as one.
3. **The `+0x01` field is unaligned.** A naturally-aligned struct is `0x20A` and every later offset
   moves. Pack it and assert the size.
4. **Do not deduplicate and do not sort.** §9's warning is the sharpest thing in this contract: the
   family is deterministic, but its contents are only as deterministic as the query that filled it,
   so a reimplementation that tidies the set diverges while reproducing this family exactly.

## 17. Related

- `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` — the two instances in context.
- `_types/types.tsv` — `BattleTargetBuffer`, `BattleTargetEntry`.
- `04-Actor-Entity/Battle-Unit/battle-unit-accesses.tsv` — the access census both instances draw on.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings (the image-address resolver, the audio request chain) are recorded in the registry, not here.*

- **Party — SERVICE.** `BattleUnit_ResolveByFocusHandle` turns a party focus handle into a battle unit for six functions
  this contract cites: `00301AD0`, `00309990`, `0030D160`, `0030F760`, `00313120` and `0031ADB0`. `00301AD0` also reads
  `BattleUnit_GetPartyLeader` and `PartyFocus_IsCurrentPackedActorHandle`, and `0031ADB0` reads
  `PartyFocus_GetCurrentPackedActorHandle`.
- **Movement — SERVICE.**
  - `Battle_ProcessActionTarget` (`00307300`) turns and steers the actor through `Actor_SetDesiredMovementHeading`,
    `Actor_SetFacingHeading_Variant1` and four movement helpers of 55–448 bytes.
  - `BattleUnit_CancelAndResetCurrentAction` resets the path through `BattleLocomotion_ResetPathAndSetTargets`.
  - The presentation dispatcher is also called by the 68-byte stance-bit setter `00313500`.
- **Spawn_Encounter_Lifecycle — SERVICE.** The HP write `00300530` calls
  `SpawnGroup_RecordMemberDeathAndHandleCompletion` directly, and that function calls the presentation dispatcher
  ([group completion](../05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md)).

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatFormula — SERVICE and CLIENT, 16 edges.**
  - Cited functions call `BattleFormula_ResolveTargetResult` (2), `BattleFormula_ApplyTargetResult`, `BattleFormula_MapOutcomeToTargetEntryCode`, `BattleStats_FindOwningBattleUnit` and `BattleStats_GetByBattleSlotIndex`.
  - They are called by `BattleStats_ModifyHPAndProcessLethalState` (2), `BattleFormula_ApplyTargetResult`, `BattleStats_ReconcileCurrentHpToEffectiveMaximum`, `BattleStats_SetCurrentHP` and `BattleStats_RebuildEffectiveStatsAndAffinityState`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — CLIENT (27 edges through 13 of this page's functions).** The Gameplay layer reaches this page at `00301AD0`, `0030D160`, `00313120`, `00300530` and 9 more. `BattleEncodedId_DispatchQueryMode0Value` is the worked example, read in full - it is the encoded-id dispatch, and it says how an id is built: `0xFFFF` answers `-1`, the top nibble `id & 0xF000` must be **`0xE000` or below**, and `id >> 12` is the class that selects the arm; **3 of the 11 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — SHARED LEAF.** The allocator `001A1470` that `00864D10` calls is also invoked by the UI body `0018EEE0`. The buffer only borrows the allocator; the UI's own use of it is not claimed here. The crossing is that call, not a shared responsibility.

## SWE2-EC7-76 update (2026-09-19) - `0026D610` kind-0x60 forwarder measured

`0026D610` (20 B) is the kind forwarder: `byte[rcx+3] & 0xE0 == 0x60`
tails `002E6090`, anything else returns - the `0x60`-kind filter the
target-buffer bodies share.
Interior anchor `0026D61D` (the `je 0x2E6090`).

## SWE2-EC7-91 update (2026-09-20) - `00864D10` record alloc + vtable init measured

`00864D10` (82 B) is the allocation the buffer callers run:
`0016D6A0(1)` gates, `001A1470([rip-global], 0x100)` reserves a
0x100-byte record whose first qword takes the `rip`-relative
vtable `0x146ADDD`-relative image address; the record lands in
`[rbx+8]` and the body returns `record + 0x10` (or 0 on
allocation failure).
Interior anchor `00864D1E` (the `0016D6A0` call).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**CombatAI — BOTH DIRECTIONS, 30 edges: the gambit and AI-order evaluators are the buffer's main producer.**
- **Filling and resetting.** `AiOrder_EvaluateAndResolveActionTarget`, `AiOrder_EvaluateTargetSelector`,
  `AiOrder_SelectFinalTargetFromCandidates` and `AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` reset the
  buffer through `BattleTargetBuffer_ResetPreservingFlag0` and fill it through `BattleTargetBuffer_TryAppendActorWork`.
  They reach the relation and distance tests (`BattleTarget_MatchesRelationMode`,
  `BattleTarget_ComputeSurfaceDistance*`) and `BattleAction_CheckTargetEligibility`.
- **Committing.** The commit path `BattleUnit_SelectAndCommitNextAction` / `BattleUnit_TrySelectAndCommitAiOrderFromSet`
  calls `BattleUnit_CommitAction`.
- **Perception.** `BattleUnit_RebuildPerceptionCandidateCache` refreshes through the `BattlePerception_*` bodies.
- **The frame.** `BattleUnit_UpdateCombatFrame` cancels, resets and dispatches presentation events.
- **Enmity.** `Battle_ProcessActionTarget` applies `BattleEnmity_ApplyActionParameters`.

Which target a gambit chooses is owned by the 09 pages (`CONTRACT-gambit-walk`). This contract owns the buffer those
choices are written into.

**WorldAreaField — DEPENDENCY, eleven edges: one shared field flag.** Nine buffer and AI bodies read
`FieldData_GetActiveFieldRecordBit15`, the active field record's bit 15. `AiOrder_EvaluateTargetSelector` also reads
`FieldData_GetFormat0RecordVectorByIndex`, and `BattleUnit_HandleActorTimelineEvent` (a `find` caller) can request
`WorldTransition_RequestFieldTransition`. What the field flag means is the field-record page's.

**Status_Periodic_Terminal — CLIENT, five edges.**
- A status change cancels the current action: `BattleUnit_ResetActionControlForStatusTransition` and
  `BattleUnit_RecoverFromTerminalStatusSetIfClear` call `BattleUnit_CancelAndResetCurrentAction`.
- `BattleStats_ChangeStatusAndProcessSideEffects` posts presentation events through
  `BattleUnit_DispatchActorPresentationEvent`.
- `BattleStats_ModifyHPAndProcessLethalState` hands a lethal result to the status write.

The status pages own those transitions.

**Script_VM_Native_Bridge — CLIENT, six edges.** The kind-0x60 forwarder `0026D610` (the filter the buffer bodies
share) is also called from script handlers `0033F330` and `0050D660`. `0033F330` is itself a script verb, called from
`0033FC60` / `00340380`, that pops through `VMValueStack_PopInt32CoerceFloat32`. `003495A0` calls the append-and-reset
caller `00313120`.

**RNG_Random_Selection — SERVICE, three edges.** `AiOrder_SelectFinalTargetFromCandidates` and
`AiOrder_EvaluateAndResolveActionTarget` draw `RNG_SharedGameplayLCG_NextU32`, the latter also through
`BattleData_ResolveWeightedId`. That is a random pick among buffered candidates, mapped in
`which-roll-is-on-which-generator`.

**Resource — MECHANICAL, one edge.** `BattleUnit_HandleActorTimelineEvent` calls `001D6AE0`, a shared helper with
callers across the image.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page and the cited pages read them; no new body read
(OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*
