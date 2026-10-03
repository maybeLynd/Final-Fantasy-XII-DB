---
contract: Call a native verb from an authored script
category: 01-Script-VM-Native-Bridge
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: scriptvm-verb-dispatch-and-parameter-encoding.md
entries: ["0025E4C0", "002621D0", "003DC2D0", "003DC270", "003DC240", "003DC2A0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 37 addresses cited - 7 data, 12 entry, 18 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-12
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-verb-dispatch-abi-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — call a native verb from an authored script

> **Authored 2026-09-12 by OPUS.** The mechanism is FABLE's, on
> [the verb dispatch page](scriptvm-verb-dispatch-and-parameter-encoding.md), which has survived
> **three** falsification passes. This states it as an ABI: the encoding, the record layout, the
> callback signatures and the lifecycle rule, in the form a reimplementation needs.
>
> **What is re-derived here is marked as re-derived** — the id split and all three table accessors
> were read from the image for this contract. The population counts are that page's and are cited,
> not re-counted.

## 1. Purpose

**This is the interface every authored script crosses to reach the engine.** A cutscene moving a
character, a trigger opening a door, a battle script setting an Esper's HP floor — each is one
bytecode instruction carrying a 16-bit id, and the engine turns that id into up to three native
callbacks. Nearly two thousand verbs exist. **Anyone modding FFXII through its scripts is using this
ABI whether they know it or not**, and anyone reimplementing the engine has to reproduce it exactly
or every authored script in the game means something else.

## 2. Interface

### 2.1 The instruction

The interpreter (`0025E4C0`) pre-decodes a little-endian 16-bit immediate for every opcode `>= 0x47`.
**Four opcodes make a verb call**, each three bytes — the opcode plus that id:

| opcode | actor binding | the pushed return value |
|---:|---|---|
| `0x58` `CALL` | the **current** actor: `cmdState[8] = *(u16 *)actor` | left on the value stack |
| `0x59` `CALLACT` | **pops** an actor id and binds to it | left on the value stack |
| `0x5D` `CALLPOPA` | as `CALL` | popped into the **A register**, `cmdState[0x10]` |
| `0x5E` `CALLACTPOPA` | as `CALLACT` | popped into the A register |

`0x59` and `0x5E` pop the actor id **only on the command's first call** (`cmp byte [rsi+0x15], 0`),
so a durative verb does not re-consume its operand every frame. `0x5E` has no dispatcher call of its
own — it jumps into `0x5D`'s body at `00261ABF`, past the current-actor load it does not want, which
is why a caller census over direct calls finds three sites and not four.

### 2.2 The id is 4 bits of family and 12 of command

**Re-derived 2026-09-12** from `002621D0`:

```asm
00262205  sar r12d, 0xc              ; family  = id >> 12   (ARITHMETIC shift)
0026220C  and r15d, 0xfff            ; command = id & 0x0FFF
```

Sixteen families exist because the field is four bits. `003DC2D0` fills all sixteen pointers at
`0x02B57EF0` with the default table and then overwrites four:

| family | id range | table | commands |
|---:|---|---|---:|
| **0** | `0x0000`–`0x0FFF` | `0x01EED700` | 1,496 |
| **3** | `0x3000`–`0x3FFF` | `0x01F281B0` | 147 |
| **5** | `0x5000`–`0x5FFF` | `0x01F29418` | 1 |
| **7** | `0x7000`–`0x7FFF` | `0x01F29440` | 104 |
| 1, 2, 4, 6, 8–15 | — | `0x01F26720` | 212, **shared** |

**Twelve families alias one table**, so `0x2005` and `0x4005` resolve to the same command. That table
is a real command table and not a fallback handler: family 2's `0x2000`–`0x20D3` debug verbs live in
it and are reachable.

### 2.3 The command record — 32 bytes, three callbacks, one unused slot

**All three accessors re-derived 2026-09-12**, and they agree on one layout:

```asm
003DC270 begin : movsxd rax, ecx ; lea rcx,[→02B57EF0] ; mov rcx,[rcx+rax*8] ; test rcx,rcx ; je null
                 cmp edx,[rcx] ; jge null ; movsxd rax,edx ; shl rax,5 ; mov rax,[rax+rcx+8]
003DC240 poll  : … same prologue …                      shl rax,5 ; mov rax,[rax+rcx+0x10]
003DC2A0 result: … same prologue …            inc rax ; shl rax,5 ; mov rax,[rax+rcx]
```

`(command + 1) × 32` is `32 × command + 32`, so all three land in **one 32-byte record** based at
`table + 8 + 32 × command`:

```
table + 0x00   s32   command count
table + 0x04   —     padding, zero in all five tables
record N   =   table + 8 + 32*N
  +0x00  ptr  begin (N)
  +0x08  ptr  poll  (N)
  +0x10  ptr  — unused, NULL in all 1,960 records, in every family —
  +0x18  ptr  result(N)
```

### ⚠ CORRECTED 2026-09-12 by the 40th pilot — the guard is ONE-SIDED

This contract said "every accessor fails closed". **Half of that is right.** A null family table or
`command >= count` does return `NULL` (`xor eax, eax`), and an out-of-range verb reads nothing
**past** the table. But `cmp edx,[rcx] / jge` is a **signed** compare and `movsxd rax, edx`
sign-extends, so:

| input | what the accessor actually does — **executed, not reasoned** |
|---|---|
| `command` **negative** | passes the bound and reads **before** the table. At count 3 and command `-1`, `begin` returned the qword 24 bytes before it and `poll` the one 16 bytes before it, and **`result` returned the table's own count word, `0x0000000000000003`, as a callback pointer** |
| `family` **negative or ≥ 16** | indexes the sixteen-entry array with no bound at all. Family `16` resolved the pointer immediately past the array and family `-1` the pointer immediately before it, and **both returned a callback** from the table those pointers named |
| a **negative count** in the table header | refuses every command, because the compare is signed on *both* operands. Counts of `-1` and `0x80000000` returned `NULL` for command 0 in all three accessors |

**None of this is reachable from bytecode**, and the pre-decode is why. **Re-derived 2026-09-12**
at `0025E5AF`:

```asm
0025E5AF  movzx ebx, byte ptr [r14 + 2]   ; high byte, ZERO-extended - bits 8..31 of ebx cleared
0025E5B4  movzx eax, byte ptr [r14 + 1]   ; low byte
0025E5B9  shl   bx, 8                     ; 16-BIT shift - it cannot reach bits 16..31
0025E5BD  or    bx, ax                    ; 16-BIT or
```

Both halves of the assembly are 16-bit operations over a register whose upper half `movzx` already
cleared, so the id leaves the decoder in `0..65535` and the family is `0..15` **by construction, not
by convention**. (Below opcode `0x47` the decoder does not run at all and `ebx` stays `0`.) So
this is not a bug report about the shipping game. It is what a reimplementation has to copy: these
are `int` parameters, the guard admits half the `int` range, and writing the bound as `unsigned`
changes what the function does.

`0016D6A0` — `_guard_check_icall`, a 3-byte `ret` — stands in for an absent callback in every table,
so **a non-null pointer is not proof of a real handler**.

### 2.4 The callback signatures

Microsoft x64, and ~~the same four things every time~~ these four things, with `begin` taking a fifth on the stack *(corrected 2026-10-02, OPUS: `002622C4`–`002622CD`; added below 2026-09-13)*:

| | `begin` | `poll` | `result` |
|---|---|---|---|
| `rcx` | the script/actor context the verb was issued from | same | same |
| `rdx` | the resolved target actor — differs from `rcx` only after `CALLACT` | same | same |
| `r8` | `cmdState + 0x18`, **16 bytes of per-command scratch** | same | same |
| `r9` | the value stack — **where the arguments live** | *(not passed)* | the value stack |
| `[rsp+0x20]` | **the actor manager the executor received as its own first argument** | *(not passed)* | *(not passed)* |

**`begin` takes FIVE arguments, and the fifth is on the stack** — added 2026-09-13
(`AUDITSPEC-VERB-ABI-ARGS`). `002622C4` reloads the executor's param 1 from its home slot
`[rsp+0x70]` and writes it to `[rsp+0x20]` before `rcx`/`rdx` are loaded, so `begin` alone sees the
manager that `poll` and `result` never get. **Whether any of the 1,960 handlers reads it is
unmeasured; the ABI is in the image either way**, and a reimplementation that omits the slot leaves
whatever the caller last wrote there for the handler to find.

**`poll` takes three arguments, not four**, and that is the whole reason a durative verb must stash
what it needs: it cannot read arguments again. Nearly every handler in the game opens `mov rcx, r9`
followed by a pop primitive — **that two-instruction sequence is "read an argument"**.

## 3. Types

| type | size | where |
|---|---:|---|
| family table array | 16 × 8 | `0x02B57EF0`, one pointer per family |
| command table | `8 + 32 × count` | five of them; count at `+0x00`, records from `+0x08` |
| command record | `0x20` | `begin` `+0x00`, `poll` `+0x08`, unused `+0x10`, `result` `+0x18` |
| `cmdState` | ≥ `0x28` | `+0x08` bound actor id ~~(u16)~~ (u32) *(corrected 2026-10-02, OPUS: written as a dword, `002619AE`, `002619FD`, `00261ABF`, and read as one, `00262225`)* · `+0x0C` the return slot (4 bytes, int **or** float) · `+0x10` the A register · `+0x15` the phase byte · `+0x18` 16 bytes of command scratch |

## 4. Preconditions · postconditions · invariants

**Preconditions.** The family array is initialised (`003DC2D0` runs at startup). `cmdState` is the
caller's; the executor does not allocate.

**Postconditions.** Exactly one value is pushed on the value stack, always. The phase byte is 0 on
return unless the command is still running, in which case it is 1.

**Invariants.**

1. **Every native command yields exactly one value.** The executor pushes the callback's result, or
   integer `0` if none was written. **That is why `CALLPOPA` and `CALLACTPOPA` exist** — a script
   that does not want the value needs an opcode to take it back off.
2. **A command with only a `result` callback completes inside one call.** With no `poll`, the
   running flag comes from a zero-initialised local and the executor falls straight through.
3. **The phase byte on entry is only ever 0 or 1.** Values 2 and 3 are written by the `result`
   callback and read a few instructions later in the *same* invocation to choose int or float; the
   executor then resets the byte.
4. **Arguments are read once.** `begin` reads them for a durative verb and stashes what it needs in
   the 16-byte scratch; `poll` never sees the stack again.

## 5. State

Read: the family array, the command table's count and records, `cmdState[0x15]`, `cmdState[8]`.
Written: `cmdState[0x0C]` (cleared on the first call, set by the callback), `cmdState[0x15]`, and
the value stack. **Nothing is allocated or freed.**

## 6. Relationships

`0025E4C0` (the interpreter) → `002621D0` (`VMNativeCommand_ExecuteLifecycle`) → the three accessors
→ the command's own callbacks. `003DC2D0` initialises the family array once at startup.

## 7. State transitions

```
phase 0  --begin, then poll--> phase 1   (poll returned running & 1)
phase 0  --begin, then poll--> result, push, phase 0   (poll absent or not running)
phase 1  --poll-------------> phase 1   (still running; begin is NOT re-run)
phase 1  --poll-------------> result, push, phase 0
phase >=2 --result----------> push, phase 0            (NO begin and NO poll; EXP-085 (2))
```

**`begin` runs only from phase 0**, and the return slot is cleared with it. A reimplementation that
re-runs `begin` on a later frame re-reads arguments that are no longer on the stack.

**The third entry arm is not a curiosity.** `00262248`/`0026224C` test the phase byte for 0 and for
1; **anything else falls through to `00262255`, which fetches `result` and calls it directly**. And
the `+0xC` clear (`mov dword [cmdState+0xC], 0`, `002622B7`) **lives only in the phase-0 arm**, so an
entry at phase >= 2 pushes whatever `+0xC` already held — EXP-085 (4). A reimplementation that
initialises the phase byte to anything but 0, or that leaves it >= 1 after an abort, enters here.

## 8. Script · resource · event interactions

**This section is the whole contract**: the verb id is authored, in the script. `0x3061`
`btlAtelSetHpLowLimit` is a worked example — family 3, command 97, a **result-only** record at
`0x01F28DD8` reading `NULL, NULL, NULL, 005105E0`, bounded by that table's count `0x93` = 147.

## 9. Determinism

No RNG here; individual handlers may draw. **Ordering is the contract**: a durative verb is polled
once per frame from the script's own drive, which is
[the field runtime pass](../../04-Actor-Entity/CONTRACT-field-runtime-pass.md). Single-threaded.

## 10. Failure paths and edge conditions

| # | condition | result |
|---:|---|---|
| 1 | the family's table pointer is null | the accessor returns `NULL`; the callback is skipped |
| 2 | `command >= count` | `jge` → `NULL`. Reads nothing past the table. **Not fail-closed below zero** — see row 8 |
| 3 | all three callbacks absent | the executor still pushes integer `0` |
| 4 | a callback slot holds `0016D6A0` | a 3-byte `ret` — **not null, and not a handler** |
| 5 | the `+0x10` slot | **NULL in all 1,960 records.** The engine never uses it |
| 6 | an id whose family bits exceed the four available | impossible from bytecode — the immediate is 16 bits, so the family is 0–15 by construction. **The accessors themselves do not check it**: family `16` was executed and resolved the pointer past the array |
| 7 | a **negative** id reaching `002621D0` from a non-bytecode caller | `sar r12d, 0xc` is **arithmetic**, so the family is negative and `movsxd rax, ecx` indexes the array **backwards**. Nothing checks it. **EXECUTED**: family `-1` returned a callback from the pointer planted before the array |
| 8 | a **negative command** reaching an accessor directly | passes `jge` and reads a whole 32-byte record **before** the table. **EXECUTED**: `result` at command `-1` returns the table's own count word. Not reachable through the 12-bit mask in `002621D0` |
| 9 | a table whose count dword is **negative** | every command is refused, the compare being signed. **EXECUTED** at `-1` and `0x80000000`. No shipped table has one |

## 11. Observable behaviour

From a script: the verb's effect, and one value on the stack. In memory: `cmdState[0x15]` at 1 while
a durative verb runs, the 16-byte scratch at `cmdState+0x18`, and the return slot at `+0x0C`.

## 12. Reproduction formula

```c
/* CORRECTED 2026-09-13 (AUDITSPEC-VERB-ABI-ARGS, upheld). The previous prototype listed
   s/vs/id in the wrong slots and the body sent the two pointers to each other's places.
   Native order, re-derived at 002621D0: rcx, rdx, r8, r9d, then ONE stack argument. */
int VMNativeCommand_ExecuteLifecycle(actormgr *vm,   /* rcx  -> rbp at 00262209 */
                                     actor    *issuer, /* rdx  -> r14 at 00262202 */
                                     stack    *vs,   /* r8   -> rbx at 0026221D */
                                     int       id,   /* r9d  -> r15d/r12d       */
                                     cmdState *s)    /* [rsp+0x28] -> rdi at 002621E9 */
{
    int family  = id >> 12;                 /* sar: arithmetic */
    int command = id & 0x0FFF;
    void *poll  = GetPollCallback(family, command);       /* fetched up front, always */

    /* the compare reads the ISSUER's word-0 (00262230 movzx eax, word [r14]), and the
       fallback resolves the BOUND id out of the vm (00262238 rcx=rbp, edx still s->boundActor) */
    actor *owner = (s->boundActor == *(uint16_t *)issuer)
                 ? issuer                                        /* 00262245 mov rbp, r14 */
                 : ActorManager_GetRecordByOrdinal(vm, s->boundActor);

    if (s->phase == 0) {
        s->ret = 0;
        void *begin = GetBeginCallback(family, command);
        /* vm is the FIFTH argument and travels on the stack: 002622C4 reloads param1 from its
           home slot [rsp+0x70] and stores it to [rsp+0x20] before rcx/rdx are loaded */
        if (begin) begin(issuer, owner, s->scratch, vs, vm);
    }
    int running = poll ? poll(issuer, owner, s->scratch) : 0;
    if (running & 1) { s->phase = 1; return 1; }

    void *result = GetResultCallback(family, command);
    if (result) result(issuer, owner, s->scratch, vs);   /* 0026226B-00262278 */

    switch (s->phase) {                     /* the result callback set this */
        case 2:  push_int  (vs, *(int32_t *)&s->ret); break;
        case 3:
        default: push_float(vs, *(float   *)&s->ret); break;
        case 0: case 1: push_int(vs, 0);              break;
    }
    s->phase = 0;
    return 0;
}

void *GetBeginCallback (int f, int c) { t = fam[f]; return (!t || c >= t->count) ? 0 : t->rec[c].begin;  }
void *GetPollCallback  (int f, int c) { t = fam[f]; return (!t || c >= t->count) ? 0 : t->rec[c].poll;   }
void *GetResultCallback(int f, int c) { t = fam[f]; return (!t || c >= t->count) ? 0 : t->rec[c].result; }
```

## 13. Runtime validation

**Evidence class: isolated original-code. There is still no live evidence.** ~~for the DISPATCH half
only ... and the LIFECYCLE half is still unexecuted.~~

> **CORRECTED 2026-09-16 (OPUS). THE LIFECYCLE HALF WAS EXECUTED THREE DAYS AGO AND THIS SECTION
> WENT ON SAYING IT WAS NOT.** [`EXP-085`](../../_experiments/EXP-085-verb-lifecycle-execution.md)
> (SWE2-ORACLE, 2026-09-13, method B, isolated original-code under Unicorn against the shipping EXE)
> is titled `VMNativeCommand_ExecuteLifecycle` (`002621D0`) — **this section's own "not executed"
> row** — and reports **35/35 cases pass, 9/9 byte-level mutants detected**.
>
> **The experiment named the sentence it superseded and nobody carried it back.** EXP-085's header
> quotes this contract verbatim: *"§13: 'the LIFECYCLE half is still unexecuted'"*. It was found by
> `check_experiments.py`, which lists it under **NOT CITED — a RUN experiment its contract never
> names** *and exits 0*, so nothing ever had to look. A missing back-link was not a broken hyperlink;
> it was hiding a claim the corpus had already refuted.
>
> **What EXP-085 does NOT establish**, in its own words: a scripted callback is not a proved one, so
> what is shown is the executor's ordering, argument surface, phase machine and push rule — **not
> what any verb does**.

| what | pilot | cases | mismatches |
|---|---|---:|---:|
| the three accessors and the table initialiser — `003DC270`, `003DC240`, `003DC2A0`, `003DC2D0` | [`diff_verb_dispatch.py`](../../../../Reconstruction/Tests/Differential/diff_verb_dispatch.py) — the **40th** | 73 | **0** |
| the lifecycle executor `002621D0` | [`EXP-085`](../../_experiments/EXP-085-verb-lifecycle-execution.md) — isolated original-code, Unicorn ~~—~~ | 35 | **0** (9/9 mutants detected) ~~**not executed**~~ |

**Nothing is scripted.** These four functions have no callees at all, so what the fixture supplies
is memory rather than behaviour: a 64 KB window of the data segment, mapped at its real address
because all three accessors reach the family array by a hard-coded `lea` and cannot be relocated.
The suite compares the returned callback, **an FNV-1a over all 64 KB** — so "the accessors write
nothing" is checked rather than assumed — and the sixteen family pointers.

### What execution changed

**§2.3 and §10 now carry the correction.** The static reading of the record layout held exactly:
`begin` at `+0x00`, `poll` at `+0x08`, `result` at `+0x18` of one 32-byte record based at
`table + 8`, including the identity between `(c+1)*32` and `8 + 32c + 0x18` that two readings of
these bytes had diverged over. **What did not hold was "every accessor fails closed."** The guard
is one-sided, and the three measurements in §2.3's table are values the original returned, not
inferences from the instructions.

> **The fixture plants the unused `+0x10` slot NON-NULL.** It is `NULL` in all 1,960 shipped
> records, and a fixture that copied that would have made a `begin`/`poll`/`result` confusion
> partly invisible. Every slot of every record holds a distinct value instead.

> **Honest about what this run is worth.** Two contracts this session were refuted by their own
> pilots within the hour; this one was not. The difference is the subject, not the author — these
> are four functions of about eleven instructions with one branch each, against a 300-byte
> destructor and a validator with two comparisons on the same field. A clean first run on a small
> straight-line function is weak evidence that a careful reading of a large branching one is right.

**Mutation campaign: 52 points — 41 KILLED, 3 SURVIVED,
8 EQUIVALENT, 0 TIMEOUT, 0 INVALID. Status `FAIL`, reported as it
came back.** A first campaign scored `FAIL_INCOMPLETE` with **12 INVALID**, and the cause was the
harness rather than the reconstruction: it treated the fixture's own window refusal as an invalid
run instead of as a **difference from an original that has no bound**. Twelve mutants that should
have been kills were scored unevaluable. The refusal is now a compared observable and those twelve
are kills.

### Every non-kill, adjudicated

- **All 3 survivors are kind B, and they are structurally unkillable.** Two are the
  value the window helpers return when they refuse, one is the refusal code itself. The original
  has **no bound of any kind**, so the only case that could kill them is one where the
  reconstruction refuses — and any such case is already a mismatch. **No kind D remains.**
- **8 EQUIVALENT** — each compiled to byte-identical machine code. Three are dead
  initialisers the refusal path overwrites, three are `memcpy` lengths into fixed-width locals, one
  is `VD_SLOT_UNUSED` — **the slot no accessor reads, so a constant naming it cannot change
  behaviour, and that it cannot is the claim** — and one is the initialiser's first loop iteration,
  which is dead because `003DC2F7` overwrites family 0 immediately after the `rep stosq`.
- **The window's own edge is driven.** Two cases put the read on the last four and last eight bytes
  of the fixture's memory, because a bound no case touches is a bound nothing checks; before they
  existed, both window lengths survived.

Receipts: `Database/Tools/work/OPUS/litsuffix/verb_dispatch` (the 12-INVALID first run, kept) and
`verb_dispatch2`, and the counts row in
[`MUTATION-CAMPAIGNS.md`](../../../../Reconstruction/MUTATION-CAMPAIGNS.md).

**The live half, still queued and still unperformed:** breakpoint `002621D0` and read `id`, `phase`
on entry and the value the executor pushes, for one instantaneous and one durative verb.

## 13b. EXP-085's findings, adjudicated against the bytes — 2026-09-17 (OPUS)

`SWE2-ORACLE-REQ-OPUS-VERB-LIFECYCLE-FINDINGS` offered eight findings from
[`EXP-085`](../../_experiments/EXP-085-verb-lifecycle-execution.md). **All eight are accepted, one
with a corrected argument index.** Each was re-derived here by decoding `002621D0` from its **entry**,
so the instruction boundaries are real; nothing below rests on the experiment's prose.

### The argument surface, since every finding refers to it

| | register | what the bytes make it |
|---|---|---|
| arg0 | `rcx` → `rbp` (`00262209`), homed at `[rsp+8]` (`002621D5`) | **the actor manager** |
| arg1 | `rdx` → `r14` (`00262202`) | **the context** — its first `word` is the id tested |
| arg2 | `r8` → `rbx` (`0026221D`) | **the push record** — depth at `[rbx]`, type bytes `+4`/`+0x44`, values `+0x84`/`+0x184` |
| arg3 | `r9d` | the packed verb id — family `r9d >> 12` (`sar`, `00262205`), index `r9d & 0xFFF` (`0026220C`) |
| arg4 | `[rsp+0x28]` callee-side → `rdi` (`002621E9`) | **the command state** — phase byte `+0x15`, result slot `+0xC`, id `+8`, and `+0x18` handed to every callback |

### (1) Accepted, with the argument index corrected — the manager is **arg0**

The finding reads *"calls `00358940` on the MANAGER (arg1)"*. **Its substance is exactly right and
its parenthetical is not.** `0026223B call 00358940` is preceded by `00262238 mov rcx, rbp`, and
`rbp` is **arg0** (`00262209`). Everything else in the finding holds, and the callee confirms it:
`ActorManager_GetRecordByOrdinal` (`00358940`, 30 bytes) is
`mov r8, [rcx+8]` — **the actor table is `[manager+8]`** — bounds-checked against `dword [r8]`
(`0035894D`) and indexed `[r8 + ordinal*8 + 8]` (`00358955`). The ordinal is `edx`, still live from
`00262225 mov edx, dword [rdi+8]` — **`dword [cmdState+8]`**, exactly as the finding says.

**The finding's own sibling settles the label.** Finding (7) says *"begin alone gets the manager at
`[rsp+0x28]` callee-side"*, and the value begin is handed there is `[rsp+0x70]` (`002622C4`), which is
**arg0's home slot**. Findings (1) and (7) disagreed about which argument the manager is; (7) is the
one the bytes support, twice over.

**So the trigger clause stands verbatim** — `word[ctx] != dword[cmdState+8]` with `ctx` = arg1 and
`cmdState` = arg4 — and the rebind takes **neither of them**: it takes the manager, arg0. *The
tested object is not the rebound object*, which is the part a reimplementer needs.

**Call-context corroboration.** All three callers (`WorldActorScriptVM_InterpretBytecode`,
`002619B6` / `00261A19` / `00261AD4`) execute `movzx eax, word [r15]` then `mov [rsi+8], eax` and pass
`r15` as arg1 and `rsi` as arg4 — **the caller writes arg1's id into `[arg4+8]` immediately before the
call**, so the trigger is normally equal, and the rebind arm is the exception. At `00261A19` the value
comes from `00267E10` instead, which is where the two can differ.

### (2)–(8), accepted as written

| # | finding | the bytes |
|---|---|---|
| (2) | a third entry arm: phase >= 2 runs `result` with no begin and no poll | `00262248`/`0026224C` test 0 and 1; the fallthrough at `00262255` fetches `result` (`003DC2A0`) and calls it — §7 now draws it |
| (3) | the phase byte is **re-read** after `result` returns and selects the push flavour | `0026227A movzx eax, byte [rdi+0x15]`, `cmp al,2`: `< 2` pushes type 1 value `esi`=0 (`00262292`–`0026229C`); `== 2` pushes type 1 value `dword [rdi+0xC]` (`00262318`, `00262331`); `> 2` pushes type **2** with `movss xmm0, [rdi+0xC]` (`0026233A`, `00262355`) |
| (4) | the `+0xC` clear is in the phase-0 arm only | `002622B7 mov dword [rdi+0xc], esi` sits inside the `je 2622AF` arm; neither the phase-1 arm (`2622DF`) nor the fallthrough clears it |
| (5) | begin's return is discarded; `test al,1` is the whole poll check; a missing poll is not-running; a missing result still pushes int 0 | after `002622DB call rax` the result is never tested (`jmp 2622E1`); `00262303 test al,1` / `je` is the only test, so `0x100` reads as done; a null poll takes `[rsp+0x88]`, initialised 0 at `002621F7`; a null result jumps to `00262360`, which pushes type 1 value 0 |
| (6) | the push bound is `0x3F`, so 63 slots are usable, and a **negative** depth passes it | `movsxd rax, dword [rbx]` (`00262280`) is signed and every arm tests `cmp eax, 0x3f` / `jge` — index 63 is refused, and a negative index passes and writes at `[rax + rbx + 4]`, inside the depth dword itself |
| (7) | poll's `r9` is residual; begin alone gets the manager as a 5th argument | the poll call (`002622EE`) sets only `rcx`/`rdx`/`r8`; begin's (`002622C4`–`002622D5`) adds `[rsp+0x20]` = `[rsp+0x70]` = arg0 |
| (8) | the executor keeps the `sar`, so id `0xFFFFFFFF` resolves family `-1` | `00262205 sar r12d, 0xc` is arithmetic; the `0..15` invariant belongs to the pre-decode, not here |

**The callback ABI, which follows from (7) and is worth stating once.** Every callback is called with
`rcx` = the **context** (arg1), `rdx` = the **resolved record** (`rbp`), `r8` = `cmdState + 0x18`;
`begin` and `result` also pass `r9` = the **push record** (arg2), and `begin` alone passes the
**manager** as a fifth, stack argument. `poll` receives no `r9` — whatever the caller left there.

**What none of this establishes**, in EXP-085's own words: a scripted callback is not a proved one.
What is shown is the executor's ordering, argument surface, phase machine and push rule — **not what
any verb does**.

## 14. Unresolved

1. ~~**`VA-1`** — what the unused `+0x10` slot was for.~~ — **resolved 2026-09-22 (SWE2-CONTRACT) as far
   as the image can resolve it: dead space in the 32-byte stride.** Three facts bound it completely.
   The slot is NULL in all 1,960 records (re-verified this session against the corrected
   VA→file-offset mapping — `01EEC320`'s zero-fill finding was a helper bug, not image truth; the
   corrected decode stands). It has **no reader**: a full-image rip-relative reference census finds
   the five table bases `lea`'d only by the installer `003DC2D0` — so the only code that can ever
   form a record address is the three accessors, and they load `record+0x00`/`+0x08`/`+0x18`
   (table-relative `+8`, `+0x10`, `(c+1)·32`); none touches `record+0x10`. And it has **no writer**:
   the records live in file-backed `.data` and `003DC2D0` stores only the table pointers into the
   family array. A slot with no producer, no consumer, and NULL in every shipped record is unused
   space inside the stride — a reserved or removed fourth callback. Which of those two it was is
   not recoverable from the image; nothing else about it is open.
2. ~~**`VA-2`** — whether any caller reaches `002621D0`, or an accessor directly, with an id
   that is not a 16-bit immediate.~~ **Sharpened 2026-09-12 rather than closed**: the
   interpreter's pre-decode is now shown to zero-extend, so the question is entirely about
   OTHER callers, and §10 rows 7–9 are now three executed paths rather than one reasoned
   one. A caller census over `002621D0` and over `003DC240`/`003DC270`/`003DC2A0` would
   answer it; none has been run, and **an unrun census is not an absence**.
   **ANSWERED 2026-09-21 (SWE2-CONTRACT) — the census is now run, and the answer is no.**
   An exhaustive operand-level sweep of all 38,161 bodies in `functions.tsv` finds the
   complete edge set: `002621D0` has exactly three callers, all inside `0025E4C0`
   (`002619B6`, `00261A19`, `00261AD4`), and each passes the id as **`movzx r9d, bx`** —
   a 16-bit value by construction before the executor's own split runs. Each accessor
   has exactly one call site, all inside `002621D0` (`00262220` → `003DC240`,
   `0026225D` → `003DC2A0`, `002622BA` → `003DC270`), and each passes the **split
   halves** — `ecx = r12d` (`sar r9d, 0xc` family) and `edx = r15d` (`and r9d, 0xfff`
   command) — so no accessor ever sees a raw id wider than 12 bits, let alone 16.
   A whole-image byte scan for all four addresses as qword and dword finds **zero
   stored pointers** — no function-pointer table, no indirect route; every edge is a
   direct `call rel32`. The non-16-bit and negative-id behaviours the §10 fixture
   executes are therefore reachable only through a direct accessor call no shipped
   code makes — they are properties of the accessors, not reachable inputs of the
   dispatch path. **Re-verified 2026-09-22**: the E8/E9 census reproduces the edge set exactly —
   `002621D0` called only at `002619B6`/`00261A19`/`00261AD4` (in the `.pdata` body
   `0025E550..00261DDB`, the continuation chunk of the `0025E4C0` interpreter entry), each
   accessor at its single `002621D0` site, and all three sites re-disassembled to
   `movzx r9d, bx` byte-for-byte.
3. ~~**`VA-3`** — how many of the 1,960 slots hold `0016D6A0` rather than a handler.~~ The source page
   counts populated callbacks per family; it does not separate the stub.
   **ANSWERED 2026-09-21 (SWE2-CONTRACT), by exhaustive in-image census** — every callback slot of
   every record in all five tables was decoded against the §2.3 layout (`table + 8 + 32·N`, slots
   `+0x00`/`+0x08`/`+0x18`): **34 of the 5,880 callback slots hold the stub, spread over 33 of the
   1,960 records** — `begin` 9, `poll` **0**, `result` 25. Per family: family 0 has 13 records
   carrying 14 stubs, the shared table 8 records / 8 stubs, family 3 twelve records / 12 stubs;
   families 7 and 5 hold none. The stub never appears in `poll` anywhere. Three shapes account for
   every record: **18 wholly inert records** (`begin`/`poll` NULL, `result` the stub — the command
   does nothing and reports nothing; family 0 cmds 1196/1479, shared 15/25/26/29/40/41/73, family 3
   3/37/84–90); **8 poll-driven records** (`begin` stub + `poll` `005C5230`, `result` real or NULL —
   family 0 518/521/882/883/884/1198, shared 211, family 3 32); **6 fire-and-forget records** (real
   `begin` + real `poll`, `result` the stub — family 0 86/163/192/703, family 3 1/55); plus family 0
   cmd **957**, the only two-stub record (`begin` stub, `poll` `00345100`, `result` stub). For the
   reconstruction this is the populated-callback correction the item asked for: of the slots the
   source page counts as populated, **34 are the `ret 0` stub, not handlers** — and a `result`-stub
   record still runs `begin`/`poll` normally; the stub means "no result value," not "dead command."
   **Re-verified 2026-09-22**: an independent re-decode of all five tables through the corrected
   VA→file-offset mapping reproduces the numbers exactly — 1,960 records, 5,880 slots, 34 stub
   slots over 33 records (begin 9, poll 0, result 25), `+0x10` NULL everywhere.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the id splits 4/12 with an **arithmetic** shift | **re-derived 2026-09-12**: `00262205 sar r12d, 0xc`, `0026220C and r15d, 0xfff` | 1 | PROVEN |
| the family array is at `0x02B57EF0` and is indexed `[array + family*8]` with a null check | **re-derived**: `lea rcx,[→02B57EF0]` / `mov rcx,[rcx+rax*8]` / `test rcx,rcx` in all three accessors | 1 | PROVEN |
| the bound is `command >= count` against the table's first dword, and failure returns NULL | **re-derived**: `cmp edx,[rcx]` / `jge` → `xor eax,eax` at `003DC283`/`003DC294`, `003DC253`/`003DC264` and `003DC2B3`/`003DC2C6` | 1 | PROVEN |
| the record is 32 bytes at `table + 8 + 32*command`, callbacks at `+0x00`/`+0x08`/`+0x18` | **EXECUTED**: all three accessors driven over records whose four slots hold four distinct values, at commands -2, -1, 0, 1, 2, 5, 256 and 299 — the reading of `inc rax` that two accounts diverged over is settled by the negative commands | 1 | PROVEN |
| **the count dword is read as SIGNED** | **EXECUTED**: counts of `-1` and `0x80000000` return NULL for command 0 in all three accessors, where an unsigned compare admits every command | 1 | PROVEN |
| **the bound is one-sided — a negative command passes it and reads BEFORE the table** | **EXECUTED**: at count 3, command `-1` returns the qword 24 bytes before the table from `begin`, 16 before it from `poll`, and the table's own count word `0000000000000003` from `result`. This row replaces "every accessor fails closed" | 1 | PROVEN |
| **the family array is unbounded in BOTH directions** | **EXECUTED**: family `16` resolves the pointer immediately past the sixteen entries and family `-1` the one immediately before, and both return callbacks from the tables those name | 1 | PROVEN |
| **the accessors write nothing** | **EXECUTED**: an FNV-1a over all 64 KB of the fixture's window is unchanged across every accessor case | 1 | PROVEN |
| **`003DC2D0` writes exactly 128 bytes, and its first store is dead** | **EXECUTED**: driven over a window already full of `0xEE`, with the whole-window hash compared. The `rep stosq`'s entry-0 write is overwritten at `003DC2F7`, and the mutant that skips it compiles to identical code | 1 | PROVEN |
| four opcodes, three bytes each, and `0x5E` jumps into `0x5D`'s body | the source page §2.1, from the interpreter's pre-decode and `00261ABF` | 1 | PROVEN |
| **the pre-decode ZERO-extends, so the family is `0..15` by construction** | **re-derived 2026-09-12**: `0025E5AF movzx ebx, byte [r14+2]` / `0025E5B4 movzx eax, byte [r14+1]` / `0025E5B9 shl bx, 8` / `0025E5BD or bx, ax` — both halves are 16-bit operations over a register `movzx` already cleared | 1 | PROVEN |
| the lifecycle, the phase byte and the one-value push rule | the source page §2.4, from `002621D0` read end to end | 1 | PROVEN |
| the callback argument registers, and that `poll` takes three | the source page §2.5 | 1 | PROVEN |
| the five tables and their counts; the `+0x10` slot NULL in all 1,960 | the source page §2.2/§2.3 and its 2026-09-11 cross-check, which reconciles two independent enumerations | 1 | PROVEN  **§15a: re-derived EXHAUSTIVELY 2026-09-12** — the five addresses taken from the installer's own `lea` operands, then every record decoded: `01EED700` 1496, `01F26720` 212, `01F281B0` 147, `01F29440` 104, `01F29418` **1**; **1960 total, and `+0x10` is non-NULL in ZERO of them**. `+0x04` is zero in all five |
| `0016D6A0` stands in for an absent callback | the same cross-check; it is `_guard_check_icall`, a 3-byte `ret` | 1 (static) | PROVEN |
| the stub holds exactly 34 of the 5,880 callback slots across 33 records — 9 `begin`, 0 `poll`, 25 `result`; 18 records are wholly inert | exhaustive decode of all 1,960 records in the five tables against the §2.3 layout (§14 `VA-3`, 2026-09-21) | 1 (static) | PROVEN |
| no shipped caller reaches `002621D0` or an accessor with a non-16-bit id — all three executor calls pass `movzx r9d, bx`; the accessors see only the split halves (`ecx` family, `edx` command & 0xFFF) | exhaustive operand-level caller census over all 38,161 bodies (§14 `VA-2`, 2026-09-21): 3 edges into `002621D0` all in `0025E4C0`, 1 edge into each accessor all in `002621D0`, zero stored pointers to any of the four | 1 (static) | PROVEN |
| the dispatch half executed in isolation | **EXECUTED**: `diff_verb_dispatch.py`, the 40th pilot — 73 cases, 0 mismatches, nothing scripted | 1 | PROVEN |
| any execution of the LIFECYCLE half, or any live observation | EXECUTED by [`EXP-085`](../../_experiments/EXP-085-verb-lifecycle-execution.md) - the shipped `002621D0` plus four real leaf callees, 35 cases, 0 mismatches, 9/9 mutants; the live-observation alternative remains open (§13's stated class is isolated original-code) | isolated original-code | PROVEN |
| what the `+0x10` slot was for | **bounded 2026-09-22**: dead space in the stride — NULL in all 1,960 records, no reader (only installer `003DC2D0` ever `lea`s the five table bases; the three accessors load `+0x00`/`+0x08`/`+0x18` only), no writer (`003DC2D0` stores table pointers, not record bytes). Reserved or removed fourth callback; which is not recoverable | 1 (static) | PROVEN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### 1,960 is exhaustive, not a sample

The five table addresses were taken from **the installer's own `lea` operands** (`003DC2D0`, 89 bytes)
rather than from this document, then every record decoded at the layout §2 states:

| table | family | count | records with `+0x10` non-NULL | `+0x04` |
|---|---|---:|---:|---|
| `01EED700` | 0 | **1496** | 0 | zero |
| `01F26720` | 1, 2, 4, 6, 8–15 (shared) | **212** | 0 | zero |
| `01F281B0` | 3 | **147** | 0 | zero |
| `01F29440` | 7 | **104** | 0 | zero |
| `01F29418` | 5 | **1** | 0 | zero |

`1496 + 212 + 147 + 104 + 1 = ` **1960**, and **`+0x10` is non-NULL in none of them**. Every count in
§2.2 reproduces, and one table holds a **single** command. `VA-1` — what that slot was for — ~~stays~~ *(answered: resolved 2026-09-22 as dead space in the 32-byte stride, the `VA-1` line above; 2026-10-02, OPUS)*
~~open;~~ what is now closed is that it is empty in the shipped image *record by record* rather than by
citation.

### The "0..15 by construction" argument, completed

§15 cites `0025E5AF movzx ebx, byte [r14+2]` for the zero-extension. That instruction alone loads a
**byte**, which could not produce `id >> 12` at all; the construction is four instructions:

```asm
0025E5AF  movzx ebx, byte [r14+2]   ; high byte, zero-extended
0025E5B4  movzx eax, byte [r14+1]   ; low  byte, zero-extended
0025E5B9  shl   bx, 8
0025E5BD  or    bx, ax              ; a 16-bit id in ebx, upper half zero
```

**Both halves are zero-extended and the result is 16 bits, so bit 31 is guaranteed clear** — which is
precisely why `00262205 sar r12d, 0xc` is safe: on this value the arithmetic shift and a logical
shift cannot differ. The row cited the one instruction; the guarantee needs all four, and it holds.

### Byte-level spot checks

| claim | image |
|---|---|
| `00262205 sar r12d, 0xc` (**arithmetic**) and `0026220C and r15d, 0xfff` | both present, verbatim |
| `0016D6A0` is a 3-byte `ret` | `C2 00 00` — **`ret 0`**, three bytes, followed by `CC` padding |

**Not claimed:** ~~the lifecycle half is still unexecuted and~~ *(answered: the lifecycle half was executed, the 2026-09-16 correction in §13; 2026-10-02, OPUS)* nothing here is a live observation; §13
and `VA-1` are unchanged.

## 16. Parity plan

**Constructed, 2026-09-12:** `STRUCTURAL`, `CALCULATION` and `EDGE-CASE` are **COVERED** by
`diff_verb_dispatch.py` — the array, the table header, the 32-byte record and all four of its
slots; the three address expressions at eight commands including negative ones; and §10 rows 1–2
and 6–9 on both sides of every guard.

**Still constructible offline and still not built:** `STATE-TRANSITION` — the phase machine, which
needs the executor `002621D0` and three scripted callbacks. **A scripted callback is not a proved
one**, so what such a fixture would establish is the ordering and the push rule, not what any verb
does.

**Not constructible offline, and why:** `INTEGRATION` — the ABI's meaning is the 1,960 handlers on
the other side of it, and scripting them tests the executor rather than the interface; `TIMING` — the
per-frame poll cadence belongs to the field runtime pass; `PRESENTATION`; `RNG`; `SERIALIZATION`;
`FULL SUBSYSTEM`.


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
> accessors under link 6 are the 40th. **Links 4 and 5 — the 1,228-byte drive and the interpreter —
> have never been run**, and a chain whose ends are proved is not a proved chain.

> **Found by the cross-reference audit, not by reading.** It reported this as one unaccounted
> Movement edge on the verb-dispatch contract. Neither document had said the other was on the same
> wire, and the single-caller counts are what make the path worth stating at all: there is no second
> route to a verb to be missed.

## 17. Related

- [`scriptvm-verb-dispatch-and-parameter-encoding.md`](scriptvm-verb-dispatch-and-parameter-encoding.md)
  — the mechanism, with three falsification passes on it.
- [`../CONTRACT-script-to-native-bridge.md`](../CONTRACT-script-to-native-bridge.md) — the value
  stack these callbacks pop their arguments from.
- [`../../04-Actor-Entity/CONTRACT-field-runtime-pass.md`](../../04-Actor-Entity/CONTRACT-field-runtime-pass.md)
  — what polls a durative verb once per frame.
- [`../scriptvm-native-dispatch-table.md`](../scriptvm-native-dispatch-table.md) — the id-to-name
  mapping, and its own warning that a row is a lead until its arity is checked.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Party — SERVICE.**
  - The full-menu frame `0022B8C0` commits a pending party focus handle (`PartyFocus_CommitPendingPackedActorHandle_Th…`).
  - The field runtime pass `0025D9E0` reads `PartyFocus_GetCurrentPackedActorHandle`.
  - `World_UpdateSimulationTick` runs `PartyControl_UpdateControlledActorLocomotion` and
    `PartyFocus_UpdatePrimarySecondaryActorProcessing`.
- **Audio — SERVICE.** `0025D9E0` calls the 335-byte Audio body that reads the field id and the persistent payload
  base. `World_UpdateSimulationTick` calls the 1,036-byte positional Audio body and a 9-byte leg.
- **CombatAI, CombatAction and CombatFormula — MECHANICAL.** The selector lookup `0031B810` and the owner lookup
  `0031B860` are shared with:
  - `AiOrder_EvaluateTargetSelector` and `AiOrder_BuildCandidateTargetBufferFromStored…`;
  - `Battle_BuildActionTargetSet`, `BattleUnit_IssueCommandByFocusHandlesWithOpt…` and the target-preview functions;
  - dozens of combat-formula bodies.

  They are lookups, not verb ABI.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — SERVICE.** `0025D9E0` on this page calls `FUN_00234150`, owned by that layer. What it reaches is a 104-byte registration helper that takes the `.text` address `002FED60` as a callback and gates on `byte[+0] & 0x10` of what `0031B810` returns; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Items_Equipment_Shops_License — CLIENT.** `Inventory_QueryOwnedCountIncludingReservedActionItems`, owned by that layer, calls `0031B810` on this page. That caller is the owned-count query for an item id, which returns `-1` for the sentinel id `0xFFFF`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `Reward_ComputeExperienceForRecipient`, owned by that layer, calls `0031B810` on this page. That caller is the experience computation for one recipient: it needs `byte[rec+5] == 0` and takes its context from `0031B860`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).
- **ActorEntity — CLIENT and SERVICE (64 edges).** 29 inbound (ActorEntity bodies `ActorManager_RunFieldRuntimePass` (0025D9E0), `BattleUnit_ActivateAppliedDefinitionRuntime` (00233AD0), `00264010` call page-cited `ActorManager_GetRecordByOrdinal` (00358940), `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00), `BattleUnit_SetupEngagedActionState` (002FED60)); 35 outbound (page-cited `WorldActorScriptVM_InterpretBytecode` (0025E4C0), `ActorManager_RunFieldRuntimePass` (0025D9E0), `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) call ActorEntity bodies `ActorManager_GetRecordByOrdinal` (00358940), `00263660`, `ActorResource_RemoveActiveEntry` (003DB2A0)). Substantive edges include `ActorManager_RunFieldRuntimePass` (0025D9E0) calls `0025B820`; `ActorManager_RunFieldRuntimePass` (0025D9E0) calls `0025B250`; `ActorManager_RunFieldRuntimePass` (0025D9E0) calls `0025C170`; `ActorManager_RunFieldRuntimePass` (0025D9E0) calls `0025B600`; the remaining edges run through shared helpers the page cites.
- **CoreRuntimeScheduling — CLIENT and SERVICE (7 edges).** 4 inbound (CoreRuntimeScheduling bodies `0022A580`, `0022BC20`, `MainLoop_UpdateAndRenderFrame` (0022B8C0) call page-cited `World_UpdateSimulationTick` (00314020), `MainLoop_UpdateAndRenderFrame` (0022B8C0)); 3 outbound (page-cited `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00), `MainLoop_UpdateAndRenderFrame` (0022B8C0) call CoreRuntimeScheduling bodies `00374FD0`, `001EDDA0`, `001EDE80`). Substantive edges include `MainLoop_UpdateAndRenderFrame` (0022B8C0) is called by `0022A580`; `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `00374FD0`; `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `001EDE80`; `World_UpdateSimulationTick` (00314020) is called by `0022BC20`; the remaining edges run through shared helpers the page cites.
- **Input — CLIENT and SERVICE (12 edges).** 1 inbound (Input bodies `00226BE0` call page-cited `ActorManager_GetRecordByOrdinal` (00358940)); 11 outbound (page-cited `MainLoop_UpdateAndRenderFrame` (0022B8C0), `World_UpdateSimulationTick` (00314020) call Input bodies `InputControl_SetOneShotFrameCallback` (0035E9A0), `InputGameplay_RebuildFrameSnapshotFromChannelHistory` (002498B0), `InputGameplay_RebuildRemappedTransitionMaskState` (0036FDF0)). Substantive edges include `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `InputControl_SetOneShotFrameCallback` (0035E9A0); `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `InputGameplay_RebuildFrameSnapshotFromChannelHistory` (002498B0); `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `InputGameplay_RebuildRemappedTransitionMaskState` (0036FDF0); `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `00182D40`; the remaining edges run through shared helpers the page cites.
- **Movement — CLIENT and SERVICE (20 edges).** 7 inbound (Movement bodies `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00), `00313670`, `00310920` call page-cited `BattleUnit_FindMappedDefinitionSelectorByIndex` (0031B810), `BattleStats_FindOwningBattleUnit` (0031B860), `WorldActorScriptVM_InterpretBytecode` (0025E4C0)); 13 outbound (page-cited `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00), `World_UpdateSimulationTick` (00314020), `MainLoop_UpdateAndRenderFrame` (0022B8C0) call Movement bodies `00263560`, `0037CF00`, `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00)). Substantive edges include `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `00263560`; `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `0037CF00`; `ActorManager_RunFieldRuntimePass` (0025D9E0) calls `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00); `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `002E6310`; the remaining edges run through shared helpers the page cites.
- **Presentation — CLIENT and SERVICE (22 edges).** 6 inbound (Presentation bodies `BattleUnit_BroadcastPartyCombatTargetRelation` (00313B30), `PartyCombat_UpdateStanceState` (00307E70), `00465690` call page-cited `ActorManager_GetRecordByOrdinal` (00358940), `BattleUnit_FindMappedDefinitionSelectorByIndex` (0031B810)); 16 outbound (page-cited `MainLoop_UpdateAndRenderFrame` (0022B8C0), `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00), `World_UpdateSimulationTick` (00314020) call Presentation bodies `VFXSystem_RenderSpecialPassWithGraphicsFence` (002590F0), `002512B0`, `002528A0`). Substantive edges include `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `VFXSystem_RenderSpecialPassWithGraphicsFence` (002590F0); `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `002512B0`; `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `002528A0`; `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `GraphicsSync_WaitBackendState100ClearAndResetSharedState` (0036F2F0); the remaining edges run through shared helpers the page cites.
- **Resource — SERVICE (1 edge).** 1 outbound (page-cited `MainLoop_UpdateAndRenderFrame` (0022B8C0) call Resource bodies `00324510`). Substantive edges include `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `00324510`.
- **Save_Load_Settings — SERVICE (2 edges).** 2 outbound (page-cited `ActorManager_RunFieldRuntimePass` (0025D9E0) call Save_Load_Settings bodies `SaveWrite_GetBusyFlag` (00583920), `SaveImage_GetPersistentPayloadBase` (002EF2B0)). Substantive edges include `ActorManager_RunFieldRuntimePass` (0025D9E0) calls `SaveWrite_GetBusyFlag` (00583920); the remaining edges run through shared helpers the page cites.
