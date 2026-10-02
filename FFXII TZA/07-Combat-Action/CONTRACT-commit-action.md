---
contract: commit a chosen action and target onto a battle unit, or refuse
category: 07-Combat-Action
scope: operation
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md
entries: ["0030F760"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 71 addresses cited - 1 data, 10 entry, 60 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-commit-action-pass-1 # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — committing an action

`BattleUnit_CommitAction` (`0030F760`, 570 B). The middle of the chain: the gambit walk calls it, it
resets and refills the unit's target buffer, and what it commits is what the HP write eventually
consumes. `CONTRACT-gambit-walk.md` §14.3 asked what makes a commit fail; this answers it.

## 1. Purpose

An action and a target have been chosen. This decides whether the unit will actually do it, and if so
records the commitment on the unit — and on the *target*.

## 2. Interface

| | |
|---|---|
| entry point | `0030F760` |
| `rcx` | the acting battle unit |
| `rdx` | the order record being committed — stored as the action context |
| `r8w` | the action id, used as a **word** (`0030F77E movzx edi, r8w`) |
| `r9d` | a parameter, resolved through `0031B7E0` into a unit pointer |
| `[rsp+0x70]` | non-zero means **cancel the current action first** (`0030F776`–`0030F78A`, calling `003105D0`). *Callers differ (2026-10-01, OPUS, on ASTRA's `autoattack-commit-exception/` correction `fd45553c7`, ACCEPT by SWE2-AUDIT-SPEC, re-read by OPUS): the recommit `0030FA00` passes 1 (`0030FA54`) with the id from `+0x714`; the automatic engage `00312FA0` passes 0 (`0031309C`) with the fixed Attack id `0x96` (`00313096`), and only after its snapshot `0030EFF0` returned non-zero (`0031307B`). `0030EFF0` returns 0 before its slot allocator `0030DFA0`, with no non-stack write, when bit 24 of the unit's first dword is set (`0030EFFF`) or when the current action word `+0x714` is at most `0x21E` (542, unsigned, `0030F016`) and the phase byte `+0x6B4` is at least 6 (`0030F01F`) *(on ASTRA's `automatic-suspend-phase-domain/`, ACCEPT by SWE2-AUDIT-SPEC)*; an eligible unit still gets 0 when no slot is free. So this caller never interrupts the same unit's ordinary action (id up to 542) at phase 6 or later; ids above 542 skip the phase test. The caller has already cleared `+0x28` before the call, so a refusal is not side-effect-free for the caller; cross-unit ownership and lifetime stay OPEN. No caller's value is inferred from another's.* |
| return | `int32`: **1 committed** (`0030F97A`), **0 refused** (`0030F981`) |

## 3. What decides a refusal

The action id must fall in **one of two bands**, and this is the answer the gambit walk's §14.3 was
missing:

```asm
0030F798  mov  r13d, 0x21e
0030F7A1  cmp  di, r13w
0030F7A5  ja   0030F7D9          ; not in band 1 -> try band 2
...
0030F7D9  mov  ecx, 0x4000
0030F7E1  sub  ax, cx
0030F7E4  mov  ecx, 0x166
0030F7E9  cmp  ax, cx
0030F7EC  ja   0030F981          ; not in band 2 either -> return 0
```

**Band 1 is `id <= 0x21E`. Band 2 is `0x4000 <= id <= 0x4166`**, tested by unsigned subtraction so the
wrap does the range check in one compare. An id outside both is refused with nothing changed.

> `0x21E` also bounds the action-timeout multiplier choice in the HP write. That is a shared bound and
> nothing more: image-wide it appears 40 times in 37 functions, and the neighbouring immediate `0x220`
> appears 51 times, so frequency does not make it special and no common meaning is claimed here.

## 4. Preconditions · postconditions · invariants

**Preconditions.** A unit in `rcx`. The order record may be anything the caller chose; it is stored,
not validated. The optional cancel runs **before** the band test, so a refused commit can still have
cancelled the previous action.

**Postconditions, on acceptance.** The unit's commitment block is written, its target buffer is reset
and refilled, and the **target's** attacker mask is updated (§6). On refusal, only the optional cancel
has run.

**Invariant.** The commitment block and its copy are consistent after every accepted commit — the copy
is taken from the block in the same instruction sequence that writes it.

## 5. The commitment block, and its copy

```asm
0030F7F2  and   dword ptr [rbx + 0x700], 0xfffffffc   ; clear the low two state bits
0030F7F9  mov   qword ptr [rbx + 0x708], r12          ; the order record = the action context
0030F800  mov   dword ptr [rbx + 0x710], ebp          ; the parameter
0030F806  mov   word  ptr [rbx + 0x714], di           ; the action id
0030F80D  movups xmm0, xmmword ptr [rbx + 0x700]      ; 16 bytes of the block
0030F81B  movsd  xmm1, qword ptr [rbx + 0x710]        ; 8 more
0030F823  movups xmmword ptr [rbx + 0x718], xmm0      ; -> the copy
0030F82A  movsd  qword ptr [rbx + 0x728], xmm1
```

**The live commitment is 24 bytes at `+0x700` and its copy is 24 bytes at `+0x718`**, taken as one
16-byte and one 8-byte move immediately after the block is written. A reimplementation that copies
field by field, or that copies at a later point, can observe a block the original never exposes.

`+0x714` is the field the HP write's timeout test reads, which is how an action's identity reaches
that transition.

## 6. It writes the target, not only the actor

```asm
0030F960  or    ecx, edx
0030F962  mov   dword ptr [r15 + 0xea4], ecx
0030F975  call  00313B30
```

`r15` is the unit resolved from the `r9d` parameter — **the target**. The commit adds the actor to the
target's committed-attacker slot mask at `+0xEA4`. **A commit is a two-unit operation**, and a
reimplementation that treats it as purely local leaves targets unaware of who is committed against
them.

**Corrected 2026-09-12 (`OPUS-COMMITACTION-ISOLATED`): the mask is a SET, and nothing happens when
the bit is already in it.** The three instructions above are the tail of a guarded block:

```asm
0030F940  movzx ecx, byte ptr [rbx + 0xea9]   ; the ACTOR's slot
0030F947  mov   edx, 1 / shl edx, cl          ; the bit is 1 << slot, shift masked to 5 bits
0030F94E  mov   ecx, dword ptr [r15 + 0xea4]
0030F955  test  edx, ecx
0030F957  jne   0030F97A                      ; ALREADY SET -> return 1, nothing done at all
0030F959  inc   byte ptr [r15 + 0xea8]        ; a COUNTER, only on a change
0030F960  or    ecx, edx / mov [r15+0xea4], ecx
0030F975  call  00313B30                      ; and the notify, only on a change
```

So `+0xEA8` is the cardinality of the mask, and a reimplementation that ors unconditionally
double-counts it and notifies twice. The whole block is vetoed when **bit 22 of the dword at the
unit's `+0x00`** is set (`0030F937`/`0030F939 bt rax, 0x16`).

### The propagation, which this contract did not have

**Added 2026-09-12 (`OPUS-COMMITACTION-ISOLATED`).** Between the commitment block and the mask there
is a second two-unit effect the contract never described, and it is a *group* effect rather than a
pairwise one:

```
0030F8C5  call 0030AB40(actor, target, 0)
0030F8CA  cmp eax, 1 / jbe                    ; 0 or 1 -> skip the whole walk
0030F8CF  [actor + 0x754] = param
0030F8D5  if ([actor+0x08] != [actor+0x24]) skip   ; the actor's handle must equal its group
0030F8DD  n = 00236850()                      ; and the count is asked AGAIN every pass, 0030F928
0030F8E6  for i in 0 .. n-1:
            u = 00236820(i)                   ; NULL entries are skipped
            r = u->+0x698                     ; so is a unit with no stats record
            if ((r->+0x64 | r->+0x3C) & 0x80000003) and !FieldData_GetActiveFieldRecordBit15():
                skip                          ; the same mask and override as the HP write
            if (u->+0x24 == actor->+0x24): u->+0x754 = param
0030F931  [actor + 0x750] = param
```

**So a commit whose query answers more than 1 writes the parameter onto every eligible unit of the
actor's group**, not only onto the actor. The walk re-reads the count on every iteration, so a list
that grows or shrinks under it is followed rather than snapshotted — reproduced as written. The
`0x80000003` mask with the bit-15 override is the third subsystem using that rule, after the HP
write and the gambit condition evaluation.

Both `+0x750` and `+0x754` are otherwise cleared to 0 when the actor's handle differs from its group
(`0030F89B`–`0030F8A3`), which happens before the walk and on every accepted commit.

## 7. Ordering

1. optional cancel of the current action (`003105D0`)
2. resolve the parameter to a unit (`0031B7E0`)
3. the two-band id test — refuse here changes nothing further
4. **reset the unit's target buffer and append the target's work pointer** (`0030F7B3 call 00316CF0`,
   `0030F7CD call 00316CD0`) — **band one only**, see below
5. write the commitment block and take its copy
6. consult `+0x770`, the stats record's kind byte, and `+0x744` the last cancelled action id
7. **band one only:** the propagation walk (§6, added 2026-09-12)
8. update the target's attacker mask, if it is not already set, and return 1

**Corrected 2026-09-12 (`OPUS-COMMITACTION-ISOLATED`): step 4 does not happen on every commit.**
This section said "every commit clears the buffer before the action's targets are appended". It does
not: `0030F7A5 ja 0030F7D9` sends every id above `0x21E` to the band-two test, and a successful
band-two test falls through at `0030F7EC` to `0030F7F2` — **past** the reset at `0030F7B3` and
**past** the append at `0030F7CD`. A band-two action commits with the previous action's target
buffer still in place. The same `ja` at `0030F8B2` skips the entire propagation walk for band two,
so a band-two commit writes the block, settles `+0x770`, and goes straight to the mask.

Executed: 51 buffer resets across 62 commits in the pilot's own trace (§13).

## 8. Script · resource · event interactions

**None directly.** The commit takes an order record that a gambit or a menu has already produced; it
does not read a script, touch a resource, or raise an event of its own. What it does emit is a
target-buffer reset (§7 step 4), which `CONTRACT-battle-target-buffer.md` owns.

**Added 2026-09-12 (`OPUS-CONTRA-SECTION-NUMBERS`)** — see the note in §12.

## 9. Determinism

No RNG, no timing. Fully determined by the arguments and the two units' state.

## 10. Failure paths and edge conditions

1. **An id outside both bands returns 0** with the commitment untouched — but the optional cancel in
   step 1 has already run, so "refused" does not mean "nothing happened".
2. The id is handled as an unsigned **word** throughout; a caller passing a wider value has it
   truncated at `0030F77E` before any test.
3. The order record is stored without validation; a null one becomes the action context.

## 11. Observable behaviour

In memory: after an accepted commit, `+0x708` holds the order record, `+0x714` the id, and the 24
bytes at `+0x718` mirror `+0x700`. On the target, `+0xEA4` gains the actor's bit. After a refusal none
of those change, while the previous action may have been cancelled.

## 12. Reproduction formula

```
commit(actor rcx, order rdx, actionId r8w, param r9d, cancelFirst [rsp+0x70]) -> int32
    if cancelFirst != 0:  cancelCurrentAction(actor)          /* 003105D0 */
    unit = resolveParam(param)                                /* 0031B7E0 */
    if not twoBandIdTest(actionId): return 0                  /* §3 - refuse, nothing written */
    resetTargetBuffer(actor)                                  /* 00316CF0 */
    writeCommitmentBlock(actor, order, actionId) and take its copy   /* §5 */
    consult actor+0x770 (stats kind byte) and actor+0x744 (last cancelled id)
    updateAttackerMask(target)                                /* §6 */
    return 1
```

The action id is used as a **word** throughout (`0030F77E movzx edi, r8w`); a reimplementation
widening it to a dword changes which band the two-band test puts it in.

**Added 2026-09-12 (`OPUS-CONTRA-SECTION-NUMBERS`).** This contract carried its runtime section at
11 and its evidence table at 13, two below the template, because it had neither a
`Script · resource · event` section nor a reproduction formula. **`check_gate26` reads section 13 —
so it was classifying this contract's EVIDENCE section as its runtime validation.** Both missing
sections are written from what the contract already establishes; §7's ordering is the source of the
formula above and nothing in it is new analysis.

## 13. Runtime validation

**Evidence class: isolated original-code, over the whole function. Live capture: still absent.**
(2026-09-12)

**What ran:** `0030F760` as shipped bytes under Unicorn at its real virtual address, with all
**nine callees supplied as scripted oracles at their own real addresses** — `003105D0`, `0031B7E0`,
`00316CF0`, `00316CD0`, `0030AB40`, `00236850`, `00236820`, `00377C20`, `00313B30` — and the posture
table at `022C1DB8` planted. **What did not run:** anything inside those nine, and no caller.

**Instrument:**
[`diff_commit_action.py`](../../../Reconstruction/Tests/Differential/diff_commit_action.py) against
[`commit_action.c`](../../../Reconstruction/Game/Combat/commit_action.c).

**Result: 1309 commands, 704 compared lines, 0 mismatches** — 57 commits accepted and 5 refused,
48 mask notifies, and **51 buffer resets across 62 commits**, which is the correction in §7 stated
as a count.

### The positive control

Both corrections were re-applied to the reconstruction **as this contract had them**, rebuilt from a
deleted executable, and re-run:

| control | what it restored | result |
|---|---|---|
| the buffer reset on every commit | §7 step 4 as written before | **FAIL**, 607 of 659 lines |
| the attacker mask ored unconditionally | §6 as written before | **FAIL**, 100 of 640 lines |

The second number is the smaller because the mask only differs on a re-commit; the first is large
because a spurious reset shifts every later trace line.

### The mutation campaign

**73 mutants: 69 KILLED, 2 SURVIVED, 2 EQUIVALENT, 0 INVALID,
0 NO_BUILD**, with `production_inputs_stable: true` and all four input hashes re-checked
against the files as published.

**A first run left five survivors and three of them were gaps in the fixture, not equivalences.**
Each was a write whose *effect* was invisible because the field already held the value being
written: nothing planted a non-zero `+0x6B4` before a commit, nothing planted a non-zero `+0x750`,
and nothing looked at the dword past the block copy. With those three inputs added, 2
survive. *A write of zero into a field that is already zero tests nothing.*

**The 2 survivors are equivalences by reasoning:** `line 6: 0 -> 1  (commit_action.c)`; `line 71: 0 -> 1  (commit_action.c)`. Each is an initialiser or a predicate the code reads only for truth, where the mutated value cannot reach an observable.

### What execution settled

- **The two bands, from both sides of every bound.** `0`, `1`, `0x21E`, `0x21F`, `0x3FFF`, `0x4000`,
  `0x4166`, `0x4167` and `0xFFFF` all driven: the unsigned `sub ax, cx` wrap accepts exactly
  `0x4000`–`0x4166` and the refusal returns 0 with **nothing written**.
- **The cancel is the fifth argument and nothing else.** It runs before the band test, so a
  **refused** commit still cancels the current action — driven at an id outside both bands.
- **`+0x770` survives exactly twice**: a kind-0 unit re-committing the same id *and* the same
  parameter it last cancelled, and a kind-1 unit committing anything. Every other combination
  clears it, and when it is already zero the stats record is never read at all — driven with a NULL
  stats pointer, which would fault otherwise.
- **The posture byte is re-picked only when bit 1 of `+0x6B0` is set, and that bit is consumed**;
  the byte comes from `022C1DB8 + slot * 12`, driven at slots 0, 1, 3 and 255.
- **The mask bit's shift is masked to five bits**, driven at slots 31, 32 and 33, where 32 and 33
  alias slots 0 and 1.

### What is still owed, and it is live-only

Every callee is scripted, so nothing here shows what a real cancel, a real target-buffer reset or a
real notify does with what this function hands it. §4's out-of-range slot — an authored recipe list
carrying a slot past the table — is still unobserved, and is a modding question rather than a
shipped-content one.

**Experiment records that name this contract** — found by `OPUS-CONTRACT-RUNTIME-AUDIT`, 2026-09-13. Each names this
contract in its own `contract:` frontmatter while this section did not cite it back.

- [`EXP-040`](../_experiments/EXP-040-cancel-snapshot-control.md) — **method B**, isolated original-code execution.
- [`EXP-047`](../_experiments/EXP-047-attacker-mask-reset.md) — **method B**, isolated original-code execution.
- [`EXP-033`](../_experiments/EXP-033-commit-id-boundary.md) — **method B**, isolated original-code execution. **The original falsifies the annotation, not the prose.** The assembly note read `cmp di,r13w` as a comparison with `0x21F`; the shipped bytes give `0030F798 mov r13d,0x21e`, so the first gate at `0030F7A1` compares against `0x21E` and branches ABOVE it into the extended-range check. §6's band `id <= 0x21E` is right and the quoted constant in the annotation was wrong. Linked 2026-09-14 (OPUS).
- [`EXP-034`](../_experiments/EXP-034-focus-resolver.md) — **method B**, isolated original-code execution of the committed-focus resolver chain from `+0x710`. **No live target binding is claimed**, and it is listed here because `+0x710` appears in no other contract in the corpus. Linked 2026-09-14 (OPUS).

**None of these is a live run**, so none of them changes the evidence-class statement at the
top of this section. They are listed because a reader auditing what has been executed against
this contract should not have to find them from the experiment side only.

## 13a. The nine callees, executed — `EXP-091`, consumed 2026-09-18 (OPUS)

§13 states its own boundary: *"**What did not run:** anything inside those nine, and no caller."*
[`EXP-091`](../_experiments/EXP-091-commit-callees-exec.md) (SWE2-ORACLE, 2026-09-17, method B)
ran exactly those insides — every scripted callee plus its bounded transitive closure, ~54 shipped
bodies, then `0030F760` re-driven end to end with the real callees wired in. **85/85 cases, 10/10
byte-level mutants detected, stable across two processes.** §13's boundary sentence is superseded
for the callees; it still holds for the **caller**, which nothing has executed.

**Evidence class is unchanged: isolated original-code under Unicorn. No live capture, and
`EXP-091` claims none.**

### What it settles here

- **`+0x770` is a re-commit latch** (§14.2). Re-derived from the bytes, and the rule has an arm the
  experiment's summary does not mention. With `esi = 0` throughout (`0030F796`), `0030F832` compares
  `+0x770` against zero; if it is already zero the store is a no-op. **When it is nonzero it is
  preserved iff** the stats kind byte `[+0x698]+5` is **1** (`0030F849 cmp ecx, 1` → `0030F85D je`),
  **or** the kind byte is **0** *and* the committed id `+0x744` equals the incoming id
  (`0030F84E`) *and* the committed param `+0x740` equals the incoming param (`0030F857`).
  **Anything else clears it** (`0030F85F`). *The experiment's prose gives only the kind-0 conjunction;
  the kind-1 shortcut preserves the latch regardless of id and param, which a reimplementation that
  followed the summary alone would drop.*
- **`00313B30` is notify** (§14.3). Target stats null → `r8` decides directly. Stats mask
  `([+0x64] | [+0x3C]) & 0x80000003` **clear** → collect unconditionally, `r8` ignored; mask set →
  `00377C20` flag77, pass → collect, fail → `r8 != 0` suppresses and `r8 == 0` collects. Collecting
  with actor stats `+5 == 0` walks `0031B810(i)` for `i = 0..3` capped at four; otherwise a single
  self-record. The dispatch record is `{+0 kind (self 1 / other 2), +1 flag (`r8 == 0`), +4 uid,
  +8 aid, +0xC tid}`, handed to `002ED2A0(uid, &rec)` per unit.

### Three the contract did not describe, re-derived here before recording

| body | what it does | re-derivation |
|---|---|---|
| `00308270` postf | runs its body **only when bit 22 is set** — `bt rax, 0x16` / `jae` skips to the tail (`0030827B`–`00308280`); then `+0x28 = 0`, `unlink(+0x695)`, `+0x695 = 0xFF`, posture row `0x22C1DB0 + ea9*12` | table base and the `*12` index confirmed: `lea rcx,[rip→ 0x22C1DB0]` (`0030829C`), `lea rdx,[rax+rax*2]` then `word [rcx+rdx*4]` |
| `0030EDA0` `BattleUnit_RestoreSuspendedActionState` | copies **`0x4F0` bytes** from `[unit+0xB88]` to ~~**`unit+0x730`**~~ **`unit+0x6B0` .. `unit+0xBA0` (exclusive)** *(corrected 2026-10-01, OPUS)*, then scans the eight slots at `0x22BEFC0` for an entry address equal to the source and clears bit `i&7` of `0x22BEFB0[i>>3]` | ~~destination is `unit + 0x6B0 + 0x80` (`0030EDA7`/`0030EDB6`)~~ *Corrected 2026-10-01 (OPUS, on ASTRA's `suspend-restore-copy-origin/`, ACCEPT by SWE2-AUDIT-SPEC, `_index/candidates/auditspec-review-astra-suspend-restore-copy-origin-1001/`; re-read by OPUS): `rcx = unit + 0x6B0` (`0030EDA7`), and the loop's `lea rcx, [rcx + 0x80]` (`0030EDB6`) runs before its stores at `rcx - 0x80` (`0030EDC7`), so the first store is at `unit + 0x6B0`; nine `0x80` rounds end at `+0xB30` and the `0x70` tail (`0030EE13`-`0030EE44`) ends at `+0xBA0`. The snapshot `0030EFF0` copies the same `[0x6B0, 0xBA0)` out to its pool slot (`0030F04A`), clears it with `memset` `00861EC0` (base `0030F0E5`, length `0x4F0` at `0030F0AC`) and then stores the slot pointer to `+0xB88` (`0030F0F1`). The range holds `+0xB88` itself: the source pointer is loaded into `r8` at `0030EDA0`, before the copy overwrites the slot, and the scan compares that saved `r8` (`0030EE5D`).* 9 × `0x80` plus a `0x70` tail = `0x4F0`; a null `+0xB88` faults at **`0x30EDBD`**, the first `movups`, which is a real precondition rather than a guard |
| `0030C970` unlink | **two** `cmp cl, 0x1F` gates — `0x30C983` selects the entry for the tail (out of bounds → none) and `0x30C9A1` gates the unlink itself, so `cl == 0xFF` skips the unlink but **still runs the tail** | as cited |

### Two facts worth keeping because they are faults, not behaviour

- **`00316CD0` append does not guard a negative count.** The bound is `count < 0x20` only; with a
  negative count it writes eight bytes *below* the buffer and increments `-1 → 0`.
- **`0030AB40` relat faults on null stats when `r8 & 1 == 0`** (`0x30AC14`); `r8 & 1 == 1` skips the
  dereference. A genuine crash input, kept as a case rather than smoothed away.

### What `EXP-091` discloses about itself, carried here rather than left in the experiment

Four entries were **stubbed** (entry byte patched to `ret`, calls logged): `0x512F30` the deep
render/event sink, `0x33C9B0`, and `0x2FC9D0`/`0x2FCBA0`, the family-table handlers whose signature
is not established. Two host helpers (`memset`, ~~`tick`~~ **`rand`**) are IAT. *Corrected 2026-09-25 (FABLE, Claude Opus
5.5), on OPUS block 305: the import at `008C3098` is the CRT `rand` (`api-ms-win-crt-utility`), not a timing source. And
EXP-091's "bit1 / 208 B" for the target-buffer reset should read: `00316CF0` keeps **bit 0** of byte 0 (`00316D05 and
ebx, 1`) and clears **`0x208`** bytes (`00316CFF`), i.e. 520.* Fixture content supplies the unit
array, stats records, the `0x2EBF190` tables, the link and posture tables and the cookie. The
`bodies.json` spans are a linear scan with forward-branch reachability and are **approximate on
jump-table dispatchers**, though every listed VA was genuinely executed. **So these are measurements
of the shipped bytes under a supplied world, not observations of the game.**

## 14. Unresolved

1. ~~**What the two id bands mean** — `<= 0x21E` and `0x4000..0x4166` are two disjoint spaces of action
   ids.~~ **ANSWERED 2026-09-22 (SWE2-CONTRACT) by citation — this was stale:**
   [`Action-Dispatch/battle-action-handler-table.md`](Action-Dispatch/battle-action-handler-table.md)
   mapped the whole band 2026-09-02. Band 1 (`<= 0x21E`) is the **ordinary action space** — Attack,
   Magick, Technick, Item — and carries the target buffer this contract owns. Band 2
   (`0x4000`–`0x4166`) is the **internal-order space**: 359 slots at `01EEC460[id − 0x4000]`, 341
   live across 8 distinct handlers, **no target buffer** — movement goals, state commands, waits,
   and 64 literal "set/clear status *n*" ids. Its `0x4000`–`0x4024` sub-range is locomotion's own
   byte table (`BattleLocomotion_DecodeOrderGoal`, `00312798`), and the handler table's first empty
   slot is `0x4025` — the two subsystems agree on the boundary. The earlier partial answer stands
   inside this: `0x414D` is an *order*, which is why a unit that fails the action gates can still
   be given it.
2. ~~**What `+0x770` gates** at step 6; it is compared against zero and the branch is not followed here.~~
   **ANSWERED — §13a.** It is a **latch that survives a re-commit of the same action**, and the
   branch is now followed.
3. ~~**What `00313B30` does** with the actor and target after the mask update.~~ **ANSWERED — §13a:**
   it is the **notify** body, and it builds a dispatch record per recipient.

## 15. Evidence

**Claim table corrected and executed 2026-09-12 (`OPUS-COMMITACTION-ISOLATED`).** Two rows said
more than the code does and are narrowed; five claims are new, four of them from reading the body
for the pilot and one - the propagation - from a stretch this contract had never described.
"Executed" means the shipped bytes ran against the reconstruction (§13).

| claim | evidence | tier | confidence |
|---|---|---|---|
| two acceptance bands | `0030F798`–`0030F7A5` and `0030F7D9`–`0030F7EC`, the second an unsigned subtraction so the wrap does the range check. Executed on both sides of all four bounds | 1 (isolated original-code) | PROVEN |
| returns 1 on commit, 0 on refusal | `0030F97A mov eax, 1` versus `0030F981 xor eax, eax`. Executed, and a refusal writes nothing | 1 (isolated original-code) | PROVEN |
| the optional cancel precedes the band test, so a REFUSED commit still cancels | `0030F776`–`0030F78A`, ahead of `0030F798`. Executed at an id outside both bands | 1 (isolated original-code) | PROVEN |
| the commitment block is 24 bytes and copied whole, with the low two bits of its first dword cleared | `0030F7F2`–`0030F82A`. Executed over recognisable prior contents in both the block and its copy | 1 (isolated original-code) | PROVEN |
| only a BAND ONE commit resets the target buffer and appends to it | `0030F7A5 ja 0030F7D9`, and the band-two path lands at `0030F7F2`, past `0030F7B3` and `0030F7CD`. Executed: 51 resets across 62 commits. **This row said "every commit" until 2026-09-12** | 1 (isolated original-code) | PROVEN |
| the attacker mask is a SET: nothing happens when the actor's bit is already present | `0030F955 test edx, ecx` / `jne 0030F97A` guards the counter at `+0xEA8`, the `or`, and the notify. Executed with the bit present and absent; the control that ored unconditionally FAILED | 1 (isolated original-code) | PROVEN |
| the mask bit is 1 << the actor's own slot byte, with the shift masked to five bits | `0030F940`–`0030F94C`. Executed at slots 31, 32 and 33, where 32 and 33 alias 0 and 1 | 1 (isolated original-code) | PROVEN |
| bit 22 of the dword at the unit's +0x00 vetoes the whole mask step | `0030F937`/`0030F939 bt rax, 0x16`. Executed set and clear, against the neighbouring bit 21 | 1 (isolated original-code) | PROVEN |
| a commit whose query answers more than 1 writes the parameter onto every eligible unit of the actor's group | `0030F8C5`–`0030F931`, gated on `[actor+0x08] == [actor+0x24]`, skipping NULL units, units with no stats record, and units the `0x80000003` mask refuses unless the field override says otherwise. Executed at query 0, 1, 2 and 100, with NULL entries and refusing statuses. **This stretch was not in the contract at all** | 1 (isolated original-code) | PROVEN |
| the walk re-reads the unit count on every pass | `0030F928`, not hoisted. Executed at counts 0, 1, 2 and 3 | 1 (isolated original-code) | PROVEN |
| +0x770 survives exactly two ways | a kind-0 unit re-committing the same id AND parameter it last cancelled (`0030F84E`, `0030F857`), or a kind-1 unit (`0030F849`); everything else clears it at `0030F85F`. Executed across kinds 0, 1 and 2 with the pair matching and not | 1 (isolated original-code) | PROVEN |
| when +0x770 is already zero the stats record is never read | `0030F838 je 0030F85F` jumps over the load. Executed with a NULL stats pointer, which would fault otherwise | 1 (isolated original-code) | PROVEN |
| the posture byte is re-picked only when bit 1 of +0x6B0 is set, and that bit is consumed | `0030F86B`–`0030F894`, reading `022C1DB8 + slot * 12`. Executed at slots 0, 1, 3 and 255 and with the bit clear | 1 (isolated original-code) | PROVEN |
| `0x21E` is not a distinguished constant | 40 **immediate** sites in 37 functions against 51 for `0x220`. **Reproduced exactly 2026-09-12 by an independently written census** — and the word *immediate* is load-bearing: counting displacements too gives 171 and 630, because `0x220` appears as a struct offset at **389** further sites | 1 (static) | PROVEN |
| **the unit count is re-read by a CALL on every pass, not merely re-loaded** | `0030F926 inc esi` / `0030F928 call 0x236850` / `0030F92D cmp esi, eax` / `0030F92F jl 0x30F8E6` — the bound is a function result fetched each iteration, so a unit appearing mid-walk is seen | 1 | PROVEN |
| nothing observed live | — see §13 | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED

Checked at the instructions and the counts the claims cite.

| claim | what the bytes say |
|---|---|
| the optional cancel precedes the band test | **exact.** `0030F776 cmp dword ptr [rsp+0x70], 0` / `0030F788 je 0x30F78F` / `0030F78A call 0x3105D0`, all **above** `0030F798 mov r13d, 0x21E`. A commit refused by the band test **has already cancelled** |
| bit 22 vetoes the mask step | `0030F937 mov eax, [rbx]` / `0030F939 **bt rax, 0x16**` / `0030F93E jb 0x30F97A` — a `bt`, not an `and` |
| the mask bit is `1 <<` the slot byte, shift masked to five bits | `0030F940 movzx ecx, byte ptr [rbx + 0xEA9]` / `0030F947 mov edx, 1` / `0030F94C shl edx, cl` — x86 masks `cl`, so slots 32 and 33 alias 0 and 1 |
| the walk re-reads the unit count on every pass | **stronger than stated:** `0030F928 call 0x236850` inside the loop — the bound is a **function result fetched on each iteration**, not a re-loaded variable |

### The literal census reproduces to the digit, and the word "immediate" is why

§15 says *"40 sites in 37 functions against 51 for `0x220`"*. An independently written census over
every function in the census returns **exactly 40 immediate sites in 37 functions** for `0x21E` and
**exactly 51** for `0x220`.

**A first attempt returned 171 and 630** — because it matched the literal anywhere in the operand
text, including displacements. `0x220` appears as a **struct offset at 389 further sites**; `0x21E`
at only 2.

> **A literal census must say whether it counts immediates or displacements**, and this one turns
> out to mean immediates. For `0x220` the two readings differ by a factor of eight, which is more
> than enough to invert the comparison the claim rests on. The word is now in the claim.

**Mechanical:** no stated body size drifts from the current census; a banned-evidence sweep found
nothing; the single entry `0030F760 BattleUnit_CommitAction` resolves at 570 bytes with four callers
across CombatAI and CombatAction, and the 55 other citations are instruction sites inside it.

> **This pass read instructions and counted literals.** The contract's executed claims were executed
> by its own pilot and are not re-run here.

## 16. Parity plan

`CONTRACT` — ids at `0x21E`, `0x21F`, `0x3FFF`, `0x4000`, `0x4166`, `0x4167`: accept, refuse, refuse,
accept, accept, refuse.
`STATE-TRANSITION` — a refused commit with the cancel flag set must still have cancelled.
`INTEGRATION` — after a commit, the target's `+0xEA4` must carry the actor's bit — **and after a
SECOND commit by the same actor, the counter at `+0xEA8` must not have moved again** (added
2026-09-12; the original plan would have passed an implementation that double-counts).

## 17. Related

- `09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md` — the caller, whose §14.3 this answers.
- `07-Combat-Action/CONTRACT-battle-target-buffer.md` — step 4.
- `08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md` — what eventually consumes it.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings (the image-address resolver, the audio request chain) are recorded in the registry, not here.*

- **Presentation — SERVICE.** `BattleUnit_CommitAction` (`0030F760`) calls `BattleUnit_BroadcastPartyCombatTargetRel…`
  (`00313B30`), which calls `CharacterRender_DispatchCombatRelationEv…`. So the commit reaches character rendering. The action-permission bit is also read by `AddMotion_ApplyBonePose`,
  `PartyCombat_UpdateStanceState` and `BattleUnit_ComputePresentationSuppression…`.
- **Movement — CLIENT.**
  - The unit-table accessors `BattleUnit_GetBySlotIndex` / `BattleUnit_GetSlotCount` are walked by the locomotion
    solvers: `PartyFollow_SolveFormation`, `BattleLocomotion_BuildSolverContext`,
    `BattleLocomotion_ResolveTargetSpacingAnd…`, `BattleLocomotion_QueryDynamicActorObstru…` and eight unnamed bodies
    of 84–1,362 bytes.
  - `BattleUnit_ResolveByFocusHandle` is read by `BattleLocomotion_DecodeOrderGoal`, two solvers and a 442-byte body.
  - The permission bit is read by five movement bodies.
  - `BattleUnit_CancelAndResetCurrentAction` resets the path.
- **Party — CLIENT.** `PartyConfiguration_SetSelectorsAndReconc…` and `PartyConfiguration_ReconcileRosterFromCu…` walk
  the unit table. A 639-byte Party-filed body reads the permission bit.
- **Items_Equipment_Shops_License — CLIENT.** `BattleStats_ClearAllEquipmentSlotsByMapp…` walks the unit table.
  `Inventory_QueryOwnedCountIncludingReservedActionItems` and `Equipment_UnequipEncodedItemFromActiveRoster` read the
  permission bit.
- **Spawn_Encounter_Lifecycle — CLIENT.** `Spawn_CountActiveCapTrackedActors` walks the unit table.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — CLIENT.** `BattleUnit_UpdateEngagementStateFlag`, owned by that layer, calls `00377C20` on this page. That caller is the engagement test, which reads the actor's `+0x698` block and tests `+0x3C` OR `+0x64` against its own mask; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer, calls `00377C20` on this page. That caller is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Status_Periodic_Terminal — CLIENT (5 edges, both subjects and a caller read).** The status layer
consults two functions on this page. `00300140`
`BattleUnit_ResetActionControlForStatusTransition` and `00301140`
`BattleUnit_RecoverFromTerminalStatusSetIfClear` call `003105D0`
`BattleUnit_CancelAndResetCurrentAction` — and `00300140` calls it **only when its second argument
is non-zero** (`00300149 test edx, edx / je`), so a status transition that is not told to cancel
leaves the committed action alone. `003105D0` itself requires the action block at `[unit+0x698]`,
clears `byte[+0x6B6]`, releases both action-slot handles at `byte[+0x695]` and `byte[+0x696]`
through `0030C970` and writes `0xFF` back into each, then masks the flag qword at `[unit]` with
`0xFFFFBFF75FFFCFFF` and `dword[unit+4]` with `0xFFDFFF7F`. Separately `0030E360`, `0030F690` and
`00310DB0` call `00377C20` `FieldData_GetActiveFieldRecordBit15`, which resolves the active field
index through `003148F0`, bounds it against `dword[02ADD100+4]`, reads the 16-bit entry at stride 2
from `02ADD100+8` and returns **bit 15**; an index out of range returns 0, so an unknown field
answers "clear" rather than failing. The crossing is that the status layer consults these two
functions; this page owns nothing in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## SWE2-EC7-39 update (2026-09-19) - `00313B30`

`00313B30` (410 B) is the notify the page names - `01F44830`/`022C1788`, `00377C20` pair plus `0031B810`/`002ED2A0`/`00808C40`. Interior anchor `00313B6E` (a `00377C20` call).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**CombatAI — CLIENT, 26 edges: the AI-order and perception code walks the battle-unit slots this contract
resolves.**
- `AiOrder_EvaluateTargetSelector`, `AiOrder_ComputeBoundedSelectorScalar`, `BattleEnmity_PropagateToPerceivingFoes`
  and `BattleUnit_RebuildPerceptionCandidateCache` iterate `BattleUnit_GetSlotCount` / `BattleUnit_GetBySlotIndex`.
- They resolve units through `BattleUnit_ResolveByFocusHandle` and `BattleUnit_FindMappedDefinitionSelectorByIndex`,
  and classify them through `BattleTarget_ClassifyRelationshipClass`.
- They reset and append the target buffer, and read `FieldData_GetActiveFieldRecordBit15`.
- The commit path `BattleUnit_SelectAndCommitNextAction` / `BattleUnit_TrySelectAndCommitAiOrderFromSet` calls
  `BattleUnit_CommitAction`.
- `BattleUnit_UpdateCombatFrame` calls `00308270` and the cancel/reset.

The gambit pages own the choice; this contract owns the commit.

**CombatFormula — CLIENT, eight edges.**
- `BattleStats_FindOwningBattleUnit` and `BattleStats_GetOwningActorHandle` find a stats record's unit by walking the
  same slots, as does `00384F40`.
- `BattleStats_RebuildEffectiveStatsAndAffinityState` cancels the current action.
- `00388D50` resolves a definition selector.
- `BattleStats_ModifyHPAndProcessLethalState` reads the field flag.

**UI — CLIENT, five edges.** `BattleMenu_BuildCommandEntryList` and `00322A80` walk the slots and resolve the
focused unit to build the command menu.

**Script_VM_Native_Bridge, Input and InputGameplay — MECHANICAL, six edges, all to one getter.** This page cites
`FieldData_GetActiveFieldRecordBit15` (`00377C20`). Its other readers include four script handlers (`00344740`,
`00352FA0`, `003537D0`, `00355680`), `InputGameplay_ArbitrateDigitalInputAndModalState` and `00313A00`. A shared field
flag read everywhere is not a crossing this contract makes.

*Tier 2: ledger names, sizes and `edges.tsv`; no new body read (OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*
