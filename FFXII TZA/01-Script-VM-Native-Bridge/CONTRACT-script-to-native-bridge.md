---
contract: The script-to-native bridge — pop arguments, call the native function, write a result
category: 01-Script-VM-Native-Bridge
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: Spawn-Verbs/the-script-to-native-calling-convention.md
entries: [00267DB0, 00267E10, 00267F60, 00267F90, 0026B4C0, 0026B4E0, 005101F0, 00510230, 00510260, 00510370, 00510160, 005103F0, 00510620]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 36 addresses cited - 15 entry, 21 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-script-to-native-bridge-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
local_production_date: 2026-09-23
local_production_status: "SECTION-11 locally validated; formal independent acceptance pending"  # <- corrected 2026-10-02, OPUS - accepted non-author 2026-09-29 (SWE2-AUDIT-SEM, OV-18), as the interpreter page records
---

> **Current production correction — SECTION-11, 2026-09-23.** Original interpreter, actual command callbacks, and selected request-driver paths execute together against synthetic state. Historical audit counters remain history, not acceptance of these changes. No new live game session or whole S-07/L2 acceptance is claimed. See [the section review](../_experiments/evidence/continuation-section11-script-resume/REVIEW.md).


# Contract — the script-to-native bridge

> **The sixth behavioural contract**, over the seam charter §29 names first: **script dispatch**.
> It formalises
> [the script-to-native calling convention](Spawn-Verbs/the-script-to-native-calling-convention.md)
> and closes **`EF-1`** in part.
>
> **Readiness is `CONTRACT READY`, not `RECONSTRUCTION READY`** — §13 holds isolated original-code
> evidence (EXP-013) and no live capture.

## 1. Purpose

FFXII is a script-driven game, and this is where a script stops being data and becomes a function
call. An authored verb arrives with its arguments on a small tagged stack; a thin wrapper pops them,
calls the real engine function, and — if the verb returns something — writes the answer into a slot
the interpreter will read back.

## 2. Interface

**The seven spawn wrappers described here use this observed four-register surface.** It is not
a universal signature for begin/poll/result callbacks: Section11 executes begin with a fifth
manager argument, poll without a newly supplied R9 stack argument, and result with its own surface:

```c
void VM_Verb(ActorStorageRecord *actor /*rcx*/,   /* the VM's "result context" IS the calling actor's storage record (2026-09-11) */
             SpawnCtx     *target /*rdx*/,
             VmEventCtx   *event  /*r8*/,
             VmValueStack *stack  /*r9*/);
```

A verb touches only the registers it needs; the unused ones are never read, which is what makes the
shape legible across all seven.

| helper | entry | signature | effect |
|---|---|---|---|
| pop as int32 | `00267E10` (78 B) | `(VmValueStack* rcx)` | `eax` — coerces a float slot with `cvttss2si` |
| pop as float32 | `00267DB0` (84 B) | `(VmValueStack* rcx)` | `xmm0` — coerces an int slot with `cvtdq2ps` |
| push int32 | `00267F90` (39 B) | `(VmValueStack* rcx, int edx)` | — |
| push float32 | `00267F60` (41 B) | `(VmValueStack* rcx, float xmm1)` | — |
| write int32 result | `0026B4E0` (28 B) | `(ActorStorageRecord* rcx, int edx)` | — |
| write float32 result | `0026B4C0` (28 B) | `(ActorStorageRecord* rcx, float xmm1)` | — |

> **`00267DB0` is misnamed in the ledger** as `VMValueStack_PopNumericDiscard`; it discards nothing
> and returns a float on every exit path. **Already recorded** — `BQ-8`, closed 2026-09-02, and
> filed in [`NAME-EQUIVALENCES.tsv`](../_index/NAME-EQUIVALENCES.tsv) rather than renamed, because
> the sanctioned pipeline has no rename script and a GUI rename would invalidate the snapshot hash.
>
> **And no call site discards it either — measured 2026-09-14 (OPUS), closing
> `FABLE-NOTICE-OPUS-POPNUMERIC-MISNAMED`'s open question.** Every direct `E8` call to
> `00267DB0` in `.text` was located and the instructions after it decoded until `xmm0` is
> read or written:
>
> | | sites |
> |---|---:|
> | direct call sites | **436** |
> | `xmm0` READ before it is written — the value is used | **385** |
> | `xmm0` OVERWRITTEN before any read — genuinely discarded | **0** |
> | control left the window first (31 `jmp`, 19 `call`, 1 `ret`) | 51 |
>
> The 51 are **undetermined, not discards**, and undetermined in the interesting direction:
> `xmm0` is the first floating-point ARGUMENT register, so a `call` immediately after may be
> passing the popped value on rather than dropping it.
>
> **The stack's shape, from the same read.** The tag is a BYTE array at `+0x04` indexed by
> slot; the value is a DWORD array at `+0x184` indexed by `slot*4`. Tag 1 is an int and is
> widened with `cvtdq2ps`; tag 2 is a float and is returned raw; **any other tag returns
> `0.0`**, and so does underflow — which first `call 008620C0` to report.
>
> **The ledger name still stays.** `NAME-EQUIVALENCES.tsv` row 21 already carries
> `VMValueStack_PopFloat32Coerce` with its reason. A third spelling would make one address
> described by three names, which is the condition `check_consistency` exists to catch.

**The structural rule.** A verb that returns a value ends `jmp VMResult_Write*`; a verb that returns
nothing ends `jmp <native function>` or plain `ret`. The selected writer identifies the type on those observed wrappers; command completion also permits no result callback and an implicit zero.

## 3. Types

**`VmValueStack`, size `0x284`** — in `_types/`. In the interpreter this is **static storage at
`02099AC0`**, not caller-frame storage. Entry resets depth, not arrays. Standalone helpers accept
a supplied object; that ABI fact did not prove the original interpreter allocation/lifetime.
Four parallel arrays of 64, indexed by slot:

```
+0x000            i32       depth
+0x004  u8[0x40]            TYPE TAG per slot     1 = int32, 2 = float32
 +0x044 u8[0x40]            source-kind byte; direct pushes store6. Existing variable-load
                            evidence distinguishes descriptor byte0 from its separate high-nibble
                            selector. Do not equate those fields; the complete enum is unresolved.   <- corrected 2026-10-02, OPUS: the enum is two-valued in practice - 75 push sites and PUSHV store 6 (the resolver always sets its out-record +0x00 = 6, 00262667; PUSHV copies it, 00268090/002680C2); only PUSHP stores the descriptor's width nibble 0..5 (00268118-00268150, 00268185); one reader, 00263450 (from 00353D10)
+0x084  i32[0x40]           written 0 by every push site, read by nothing — reserved
+0x184  i32/f32[0x40]       THE VALUE
                                             ends at +0x284
```

**The four bounds agree with each other**, which is the check: `0x044 − 0x004 = 0x40`,
`0x084 − 0x044 = 0x40`, `0x184 − 0x084 = 0x40 × 4`, and the push guard is `cmp eax, 0x3F`.

> **63 usable slots, not 64.** Both pushes write only when `depth < 0x3F`, so the highest slot a
> push can reach is **62** and depth tops out at 63. Slot63 exists in every array but **these guarded original pushes do not populate it**; this is not a proof about every possible external write. This independently reproduces `AO-2`, which had already established the
> 63-entry shape from the executor side.
>
> **One sharpening of `AO-2`.** It records *"value words at `+0x84+i*4` and `+0x184+i*4`"*. Only
> `+0x184` is a value: **both pushes write literal `0` to `+0x84`** and the value to `+0x184`.

**The result entry is the actor's current `ActorWaitSlot`** (identified 2026-09-11,
OPUS-CONTRA-VMRESULTCTX — this page's `VmResultCtx` and `VmResultEntry` are retired to aliases of
`ActorStorageRecord` and `ActorWaitSlot`). The record holds the signed wait-slot index
`currentWaitSlot` at `+0x11` and the interior pointer `slotsA8` at `+0xA8`
([the storage record map](../04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md)); `entry = record->slotsA8 + (int8)record->currentWaitSlot`, stride 40 —
the writers' `movsx` / `lea rax*4 … *8` (`0026B4E0`–`0026B4E9`) are those two fields and that stride.

```
entry +0x00   union[8]    execution PC for runnable bytecode; other kinds read a lowDWORD wait key
entry +0x08   i32         saved native-command target ordinal on CALL/CALLACT paths
entry +0x0C   i32 / f32   command result / selected comparison value
entry +0x10   i32         request accumulator used by PUSHA/POPA and CALL*POPA
entry +0x14   u8          request/wait kind; distinct from command phase
entry +0x15   u8          phase0 begin pending,1 poll pending;2 int/3 float typing during completion
entry +0x16   u8          request-driver visit/park marker
entry +0x18   ...         kind-/command-specific scratch; wait command stores its signed countdown
                         here. Other wait kinds retain their existing reference/descriptor meanings.
entry +0x20..0x27         kind-selected wait metadata; not certified for all kinds in Section11

```

## 4. Preconditions · postconditions · invariants

**Preconditions.** A pop requires `depth > 0`. ~~Both pops call `008620C0(1)` and return zero when it
is not.~~ **CORRECTED 2026-09-10 — the two pops fail differently on an empty stack** (§10): the
int pop returns `0` **without** calling `008620C0` and without touching `depth` (`00267E18 jle` →
`00267E3B xor eax, eax`); the float pop calls `008620C0(1)` and returns `0.0f`, also leaving `depth`
alone (`00267DB8 jle` → `00267DF2`). A push requires `depth < 0x3F` and **silently does nothing**
when it is not.

**Invariants.**

- **The stack is a true LIFO**: a pop decrements first and reads the tag at the *new* depth.
- **Both pops coerce.** A tag mismatch is never an error — an int slot popped as float becomes a
  float and vice versa. **The tag decides the conversion, not whether the call is legal.**
- **A push writes all four arrays**, in one order for `PushInt32` and a slightly different order for
  `PushFloat32Bits`; the resulting state is identical.
- **`VmResultCtx`'s slot index is read with `movsx` — signed.** A negative index is representable
  and nothing rejects it.

## 5. State

| | detail |
|---|---|
| **read** | the stack's depth, tag and value arrays; `ActorStorageRecord +0x11` (`currentWaitSlot`) and `+0xA8` (`slotsA8`) |
| **written** | the stack's four arrays and depth; one result entry's `+0x0C` and `+0x15` |
| **allocated / freed** | none — both records are supplied by the caller |

## 6. Relationships

```
interpreter
  -> VM_Verb(result, target, event, stack)
     -> VMValueStack_Pop*   x arity        arguments, IN REVERSE (see section 10)
     -> the native function
     -> jmp VMResult_Write* if the verb returns             [the tail target IS the return type]
```

## 7. State transitions

A guarded push/pop changes depth by one and its selected slots. The helper family alone does not
perform the interpreter reset. **The interpreter unconditionally resets shared depth on entry**
and can discard it at a stop-request boundary; the statement that dirty stack state necessarily
survives into the next invocation is false.

Native completion phase is in the SAME ActorWaitSlot as the result: lifecycle `0026230B` writes1,
`00262382` writes0, and result writers select2/3 transiently. Completed execution resets phase0;
only the busy path leaves1. Selected actor registers and request scratch/accumulator persist.

## 8. Script · resource · event interactions

**This is the script interaction.** The verb ids and their handlers are the ~~1,224-row~~ 1,493-row *(corrected 2026-10-02, OPUS: the file's header and data rows, extended 2026-09-19 and 2026-09-26)* dispatch table
in [`Verb-Dispatch/scriptvm-dispatch.tsv`](Verb-Dispatch/scriptvm-dispatch.tsv); this contract is
~~the calling convention every one of them obeys.~~ the calling convention their `result` callbacks obey *(corrected 2026-10-02, OPUS: `begin` also receives the manager as a fifth argument, `002622C4`–`002622CD`, and `poll` only three registers, `002622EE`–`002622F8` — as §2 says)*.

## 9. Determinism

**RNG:** none. **Timing:** none — every helper is straight-line. **Threading:** no synchronisation
appears in any of the six helpers, and the stack has no lock; **single-threaded use is assumed by
the code and not proven here.**

## 10. Failure paths and edge conditions

- ~~**Underflow reports; overflow does not.** A pop on an empty stack calls `008620C0(1)` and returns
  `0` / `0.0f`.~~ **CORRECTED 2026-09-10.** Only the *float* pop reports an empty stack. Read from
  the shipped bytes:

  ```asm
  00267E14  mov eax, [rcx] / test eax, eax        ; PopInt32
  00267E18  jle 0x267E3B                          ;   empty ->
  00267E3B  xor eax, eax / ret                    ;   return 0. NO call, depth UNCHANGED
  00267E36  call 0x8620C0                         ;   reached only from the unknown-tag arm

  00267DB4  mov eax, [rcx] / test eax, eax        ; PopFloat32
  00267DB8  jle 0x267DF2                          ;   empty ->
  00267DF2  mov ecx, 1 / call 0x8620C0            ;   REPORT, then
  00267DFC  xorps xmm0, xmm0 / ret                ;   return 0.0f, depth UNCHANGED
  ```

  Neither pop decrements on an empty stack; the decrement (`00267E1A`, `00267DBA`) is after the
  test. A push on a full stack **returns having done nothing at all** — no call, no flag, no
  partial write.
- **An unknown tag is reported by one pop and not the other** — and it is the *opposite* pop from
  the empty case. `PopInt32` treats any tag other than 1 or 2 as the error path (`00267E31`, after
  the decrement, so `depth` **is** consumed); `PopFloat32` falls through to returning `0.0f`
  **without** calling the error function (`00267DCF jne` → `00267DFC`), also after the decrement.
  **The two pops are mirror images**: int is silent on empty and loud on a bad tag; float is loud
  on empty and silent on a bad tag. The 2026-09-08 text had the empty case wrong for the int pop
  and the tag case right.
- **A caller cannot tell an empty-stack int pop from a popped zero.** `0` is a legal argument to
  every verb that pops one, and the retail `008620C0` does nothing anyway
  ([the interpreter core](Interpreter-Core/worldactor-scriptvm-interpreter.md) §10) — so a script
  that under-supplies arguments to an int-popping verb runs with zeros and no trace, in both builds'
  observable behaviour. **This closes `EF-6`.**
- **Arguments arrive in reverse.** `VM_Spawn_BindEntryAndMarkCapTracked` pops twice and passes the
  first popped value as argument 2, the second as argument 3 — **so the first value popped is the
  last the script pushed.** Both are integers there, so a reimplementation that reads left-to-right
  produces wrong behaviour and no diagnostic.
- **A negative result-slot index is representable** (`movsx`) and unchecked.

> ### The two tag spaces are offset by one, and nothing says so
>
> ```
> STACK   tag at +0x04 + slot      1 = int32     2 = float32
> RESULT  tag at entry +0x15       2 = int32     3 = float32
> ```
>
> **A value tagged `2` on the stack is a float; a value tagged `2` in a result is an int.** The two
> spaces share a range and mean different things in it.
>
> **This answers `EF-1` in part** — it asked what result tags other than `2` are, and `3` is
> float32, read from `VMResult_WriteFloat32` (`0026B4C0`), which writes the payload at the **same**
> `+0x0C` the int writer uses and discriminates purely by the tag. **No tag above 3 exists** —
> resolved 2026-09-14: the entry-typed `+0x15` writer population is enumerated image-wide and
> writes ~~only 0 (interpreter clear), 2 and 3~~ 0, 1, 2 and 3 *(corrected 2026-10-02, OPUS: `0026230B mov byte ptr [rdi + 0x15], 1` in the lifecycle, on the wait slot the interpreter passes, and `00261B97 mov word ptr [rsi + 0x14], 0x107`)* (§14 item 2).
>
> **For a reimplementation this is the sharpest trap in the subsystem.** One shared enum for both
> records compiles, runs, and silently returns a float where an int was meant.

## 11. Observable behaviour

Nothing here is directly visible. What is visible is everything downstream: a script that spawns an
enemy, sets a respawn timer or asks how long one has left is doing it through this seam, and a
wrong argument order or a wrong tag surfaces as **the wrong enemy, the wrong timer, or nothing
happening at all** — never as an error message.

## 12. Reproduction formula

```c
/* pop as int   */  if (depth <= 0) return 0;                        /* CORRECTED 2026-09-10: no error(), depth untouched */
                    depth--;
                    tag = stack->tag[depth];
                    v = stack->value[depth];
                    return tag == 1 ? (int)v : tag == 2 ? (int)truncf(asfloat(v)) : (error(1), 0);
/* pop as float */  if (depth <= 0) { error(1); return 0.0f; }       /* depth untouched */
                    depth--;
                    tag = stack->tag[depth];
                    v = stack->value[depth];
                    return tag == 1 ? (float)(int)v : tag == 2 ? asfloat(v) : 0.0f;   /* NO error() */
/* push         */  if (depth >= 0x3F) return;
                    stack->tag[depth] = isInt ? 1 : 2;
                    stack->b44[depth] = 6;  stack->d84[depth] = 0;   /* kind sentinel / reserved */
                    stack->value[depth] = v;  depth++;
/* write result */  e = ctx->p_A8 + (int8)ctx->b_11;      /* 40-byte stride */
                    e->value_0C = v;  e->tag_15 = isInt ? 2 : 3;
```

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent** (restated 2026-09-11,
OPUS-NOTICE-S13-CLASSES — the earlier "None" was the live half of a two-valued answer; the charter
separates static, isolated original-code, live and integrated proof, and this section now says which
it holds).

| claim | evidence method (not necessarily live) | date | result |
|---|---|---|---|
| §3 pop: an empty or negative depth returns 0 (int) / +0.0 (float); the float path reports through `008620C0(1)`, the int path does not | **isolated original-code**, not live: the original bytes of `00267E10` (78 B) and `00267DB0` (84 B) under Unicorn 2.1.4, SHA-gated to `73461d08…`, with `008620C0` stubbed to `ret` — [EXP-013](../_experiments/EXP-013-vm-pop-boundaries.md) | 2026-09-10 | matched, 14 of 14 calls |
| §3 pop: an unknown tag (0, 3, 255) returns 0 / +0.0 and consumes the slot (depth 1 → 0); the int path reports, the float path does not | the same run — EXP-013 | 2026-09-10 | matched |
| §3 pop: tag 1 with 42 and tag 2 with 2.75 return 42 / 42.0 and 2 / 2.75, no report, depth 1 → 0, no other object bytes change | the same run — EXP-013 | 2026-09-10 | matched |

**What that class does not cover.** The stubbed `008620C0` means the native error recorder's
effects are unproved, and every return value after a reported error is conditional on that handler
returning; nothing here ran in the game. The record's own `contract:` key names this contract in
prose, so `check_contract_runtime.py` cannot link the two until that key becomes a path (routed to
ASTRA as `FABLE-REQ-ASTRA-EXPKEYS`).

The cheapest **live** confirmation remains: break on `00267E10` during any spawn-heavy script, read
`[rcx]` for the depth and the tag byte at `[rcx+4+depth]`, and confirm the value at
`[rcx+0x184+depth*4]`. That observation would cover one sampled pop only, not the whole layout, lifecycle or all states. Section11 supplies additional original-code controls but no fresh live observation.

## 14. Unresolved

1. The complete enum of the source-kind byte *(answered: 6 from every push and from PUSHV, the width nibble 0..5 from PUSHP — `00262667`, `00268090`, `00268185`; 2026-10-02, OPUS)* and purpose of the +84 array. Existing type-row
   evidence distinguishes descriptor byte0 from a different high-nibble typed-load selector;
   their equality is not established. Historical no-reader census claims are not independently
   re-certified by Section11.
2. **Corrected object identity:** `0026230B` DOES write phase1 in the same selected ActorWaitSlot
   used by the result writers. Its +15 is not a separate lifecycle object. The prior whole-image
   exclusion of this site was wrong. This does not claim an exhaustive census of every other writer.
3. The reason for the two pop helpers' unknown-tag/underflow asymmetry remains distinct from the
   established branch behavior.
4. Bytecode can leave a value below a command argument in a synthetic fixture; that changes
   stop/flush behavior. Authored reachability and safe caller discipline remain open.
5. All other command wrappers and native services beyond the selected real callbacks. Valid
   pointers, index bounds and interpreter/actor result-slot agreement remain preconditions.

[Section11](../_experiments/evidence/continuation-section11-script-resume/REVIEW.md) establishes the
new bounded execution and corrections. Prior falsification sections below are dated history, not
acceptance of text that this current section supersedes.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the observed spawn-wrapper register surface (not universal callback arity) | all seven spawn verbs disassembled — `00510160`, `005101F0`, `00510230`, `00510260`, `00510370`, `005103F0`, `00510620`; unused registers never touched | 1 | PROVEN |
| stack layout and its four arrays | `00267E10`, `00267DB0`, `00267F60`, `00267F90` bodies; the four bounds agree with each other | 1 | PROVEN |
| 63 usable slots | `cmp eax, 0x3F / jge` at `00267F93`/`00267F96` and `00267F63`/`00267F66`; independently reproduces `AO-2` | 1 | PROVEN |
| `+0x84` is not a value word | both pushes write literal `0` to it — `00267FA2` and `00267F6D` | 1 | PROVEN |
| stack tags 1 = int, 2 = float | the two-arm dispatch in both pops — tag load and compare at `00267E21`–`00267E2F` and `00267DC1`–`00267DCF` | 1 | PROVEN |
| empty int pop: `0`, no report, depth unchanged; empty float pop: report, `0.0f`, depth unchanged | `00267E18`→`00267E3B`; `00267DB8`→`00267DF2`–`00267DFC` — the failure edges read to their `ret` | 1 | PROVEN |
| result tags 2 = int, 3 = float | `0026B4E0` writes 2, `0026B4C0` writes 3, both at `+0x15` | 1 | PROVEN |
| result stride 40, value at `+0x0C` | `lea [rax+rax*4]` at `0026B4C5`/`0026B4E5` then `*8`; both writers use `+0x0C` at `0026B4D0`/`0026B4F6` | 1 | PROVEN |
| arguments arrive in reverse | `005103F0` pops twice into `edx` then `r8d` | 1 | PROVEN |
| `+0x44` source-kind | direct pushes store6; canonical type evidence distinguishes descriptor byte0 from a separate typed-load selector; complete enum remains unresolved | existing scoped evidence | NOT universally resolved |
| `+0x84` is reserved — written 0, never read | every `+0x84` access in a stack-typed (`+0x184`-touching) function is a store of 0; no read in `0025A000`–`00360000` | 1 | PROVEN |
| `+0x15` writer population ~~is exactly {clear 0, int 2, float 3}~~ includes {clear 0, busy 1, int 2, float 3} *(corrected 2026-10-02, OPUS: `0026230B` writes 1 on a busy poll and `00261B97` writes 1 with wait kind 7)* | image-wide sweep for the `slotsA8 + movsx(+0x11)*40` fingerprint: interpreter `= 0` stores (`0025F7B2` +11 more), `0026B4D6` `= 3`, `0026B4F0` `= 2`, `002651B0` `= 2`; no other value written | 1 | PROVEN |
| `0026B500` is not a result writer | `test edx, edx` / bit write to `[rcx+0x0D]` / `jmp 002EA970` — a flag setter on a different object | 1 | PROVEN |
| `002651A0` claims the pending int result | `002651B0` writes state 2 then `002651B5` returns `[entry+0x0C]`; sole caller `00342A80` | 1 | PROVEN |
| wait-kind byte `+0x14` is a 0..7 jump-table selector; kind 4 = tick wait | `0025DFF4 cmp eax, 7 / ja` + table `0x13E3CC`; kind-4 service `0025B41D cmp byte [entry+0x14], 4` → deadline arithmetic `0025B428`–`0025B435` | 1 | PROVEN |
| entry `+0x16` is the serviced flag; `+0x18` is the wait payload | `0025DFD3` read, `0025DFD9`/`0025E11A`/`0025E127` writes; `&entry+0x18` passed to `002674B0` at `0025E00A` and `00267420` at `0025E083`; `+0x27` completion marker at `0025E04F`/`0025E07A` | 1 | PROVEN |
| whether tags above 3 exist | **no** — the writer population above is enumerated image-wide | 1 (static) | PROVEN |
| any runtime observation | **none exists** | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every claim names a body or an instruction, and every one reproduced where it stands.

| claim | read at that address |
|---|---|
| 63 usable slots | `00267F63` and `00267F93`, both `cmp eax, 0x3f` / `jge` |
| `+0x84` is not a value word | `00267F6D` and `00267FA2`, both `mov dword [rcx+rax*4+0x84], 0` |
| result stride 40, value at `+0x0C` | `lea r8, [rax+rax*4]` then `*8` = **40n**; `[…+0xC]` in both writers |
| result tags **2 = int, 3 = float** | `0026B4F0 mov byte […+0x15], 2` in `VMResult_WriteInt32`; `0026B4D6 … , 3` in `VMResult_WriteFloat32` |
| stack tags **1 = int, 2 = float** | both pops: `sub edx, 1 / je` → the int arm, `cmp edx, 1 / je` → the `cvttss2si` / `movss` arm |
| arguments arrive in reverse | `005103F0` calls `00267E10` twice: the first result becomes `edx`, the second `r8d` |

> **Tag `2` means FLOAT on the way in and INT on the way out.** The contract states this correctly and
> it is worth repeating, because it is the kind of inversion a reconstruction gets silently wrong:
> the *stack* vocabulary and the *result* vocabulary are different, and they overlap on one value.

### Confirmed, and extended: each pop reports exactly one failure, and they report opposite ones

§15 records the empty-stack halves. Both bodies read whole, there are **two** failure modes each, and
the two functions cover them in mirror image:

| | empty stack | unknown tag |
|---|---|---|
| `00267E10` `VMValueStack_PopInt32CoerceFloat32` | `jle 0267E3B` → `xor eax, eax` — **silent**, returns `0` | `0267E31 mov ecx, 1 / call 008620C0` — **reports** |
| `00267DB0` `VMValueStack_PopNumericDiscard` | `jle 0267DF2` → `mov ecx, 1 / call 008620C0` — **reports**, then `xorps` | `jne 0267DFC` → `xorps xmm0, xmm0` — **silent**, returns `0.0f` |

**Neither pop reports both, and neither is silent about both.** The int pop complains about a tag it
cannot read and says nothing about an empty stack; the float pop does exactly the reverse. On every
one of the four paths ~~the depth word at `[rcx]` is left untouched, so a refusal is not a pop~~ the empty paths leave the depth word alone, but both unknown-tag paths have already stored the decremented depth *(corrected 2026-10-02, OPUS: `00267E1F mov dword ptr [rcx], eax` before the tag test `00267E21`, `00267DBF` before `00267DC1`)*.

That the *empty* halves differ was already documented. **That the difference reverses on the other
failure mode was not**, and a reconstruction that made either function report both — or neither —
would match the documented behaviour and still be wrong half the time.

**Not claimed:** whether tags above 3 exist is still `UNKNOWN`, and nothing here is a runtime
observation.

## 16. Parity plan

**Testable now, statically:** `CALCULATION` — both pops and both pushes over every tag value
`0..255` and a float sweep, including the coercions and both failure ends. `STRUCTURAL` — the stack
layout and the 40-byte result entry against `_types/`. `EDGE-CASE` — underflow, overflow, unknown
tag, and the asymmetry between the two pops.

**Requires the running game:** `INTEGRATION` — that a real script pushes what this contract expects.

**Will not be tested:** `RNG`, `TIMING`, `SERIALIZATION` — none applies; the stack is not saved.

> **The pops are the honest pilot.** They are pure, they take one pointer, they have two coercions
> and three failure shapes between them, and the tag asymmetry in §10 is exactly the kind of claim a
> differential test settles rather than argues.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Movement — CLIENT.** `VMValueStack_PushFloat32Bits` (`00267F60`) is also called by four Movement-filed bodies (88–233 B), which push floats onto the script stack. Which verbs they serve is not read.

**CombatAction — SERVICE (SWE2-EC7 2026-09-19, 2 edges).** `003589B0`, a bridge body this page files, is also
called by two CombatAction-filed bodies (`00319F50`, `00325260`). The bridge owns the callee; those callers are
mechanical verb users.

**Gameplay — SERVICE (SWE2-EC7 2026-09-19, 1 edge).** `003589B0` is also called by `0031ADB0`. Same shape as the
CombatAction crossing — a mechanical verb user, not a document relationship.

**Input — SERVICE (SWE2-EC7 2026-09-19, 1 edge).** `00358940`, a bridge body this page files, is also called by
`00226BE0`. A mechanical verb user.

**Party — SERVICE (SWE2-EC7 2026-09-19, 5 edges).** `003589B0` is also called by five Party-filed bodies
(`00269C70`, `00326500`, `00353530`, `0050C610`, and one more). Mechanical verb users.

**World — SERVICE (SWE2-EC7 2026-09-19, 2 edges).** `00358940` is also called by `0025E400` and `002623A0`.
Mechanical verb users.

**ActorEntity — SERVICE and CLIENT.** `00267420`'s counted sub-entry test feeds each entry through `00358940` and reports to `003DB640`, both actor-entity bodies, and `00358940` is in turn called from ~27 actor-entity callers (`0025AE00`, `0035A7A0`, `003DB1F0`, `0046BAC0` among them) — the bridge borrows the layer's per-actor predicate, not shared ownership.

**Presentation — CLIENT.** `00358940` is also called from the presentation layer (`003A4290`, `003A56F0`, `00465120`, `00465690`) — the same borrowed predicate, another caller family.
- **Resource — CLIENT (1 edge).** 1 inbound (Resource bodies `0032E3B0` call page-cited `008620C0`). Substantive edges include `008620C0` is called by `0032E3B0`.
- **Spawn_Encounter_Lifecycle — SERVICE (7 edges).** 7 outbound (page-cited `VM_Spawn_ApplySelectedUnit` (00510160), `VM_SpawnEntry_GetRespawnCooldownTicks` (005101F0), `VM_Spawn_SelectPreviousMapEntry` (00510230) call Spawn_Encounter_Lifecycle bodies `Spawn_ApplyScriptSelectedUnit` (0023A3B0), `SpawnEntry_GetRespawnCooldownTicks` (002366E0), `Spawn_SelectPreviousMapEntry` (002354F0)). Substantive edges include `VM_Spawn_ApplySelectedUnit` (00510160) calls `Spawn_ApplyScriptSelectedUnit` (0023A3B0); `VM_SpawnEntry_GetRespawnCooldownTicks` (005101F0) calls `SpawnEntry_GetRespawnCooldownTicks` (002366E0); `VM_Spawn_SelectPreviousMapEntry` (00510230) calls `Spawn_SelectPreviousMapEntry` (002354F0); `VM_Spawn_SelectContinuousEntry` (00510260) calls `Spawn_SelectContinuousEntry` (00235360).
## SWE2-EC7-51 update (2026-09-19) - `00342A80`

`00342A80` (172 B) is a body - `0024CFF0`/`002638C0`/`002651A0`/`00267E10`/`00267F90`/`00269DD0`/`00357620`. Interior anchor `00342AA9` (a `0024CFF0` call).

## SWE2-EC7-57 update (2026-09-19) - `00357620`

`00357620` (175 B) is a script-to-native bridge body - `002640C0`/`00267E10`/`0026B4E0`/`00358940`/`003589B0`/`0036E750`. Interior anchor `00357641` (a `002640C0` call).

## SWE2-EC7-58 update (2026-09-19) - `002674B0`

`002674B0` (166 B) is the wait-payload sub-struct body the bridge contract names - `0020E600`/`00358940`/`003DBF60`. Interior anchor `002674C8` (a `0020E600` call).


## SWE2-EC7-94 update (2026-09-20) - `003594B0` measured

`003594B0` (14 B) is the two-store setter `00269C70`, `00326500`
and `0050C610` call: `ecx` lands in the `02CDB4F4` dword and the
`02CDB505` byte is set to 1 - the arm-the-request pair the bridge
uses to hand a pending value to the consumer.
Interior anchor `003594B6` (the byte arm).

`00267420` (132 B) is the counted sub-entry test the interpreter and field-frame callers run: `0020E600(dword[rdx+4])` resolves the counted block, then entries `word[+0xA]` through `dword[0]` each feed `00358940(rcx, word[rdi + i*4 + 4])` whose result and `byte[rbx+0xE]` go to `003DB640`; the first nonzero wins, `word[rbx+0xA]` advances past each miss, and the body returns the found flag.

Interior anchor `00267457` (function `00267420`).
