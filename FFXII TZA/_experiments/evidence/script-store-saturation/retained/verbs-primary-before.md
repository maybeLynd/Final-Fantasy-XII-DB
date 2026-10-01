---
system: ScriptVM verb dispatch and parameter encoding — call id to native handler
category: 01-Script-VM-Native-Bridge
status: AUDITED
owner_layer: PrimaryOwner:Script_VM_Native_Bridge
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 4
  last_pass: 2026-09-08
  last_pass_state: GN160-xiionline-61-shape-vs-slots
  crossref_clean: true
  reopened_count: 0
---

# ScriptVM verb dispatch and parameter encoding

> Every verb an FFXII zone script can call — `setweatherslot`, `setforcefightmode`,
> `getmapjumpposbyindex`, all 1,960 of them — is a 16-bit number in the bytecode. This document is
> the arithmetic that turns that number into a native function, and the exact rules by which the
> verb's arguments get from the script into that function's registers.

Companion data file: [`scriptvm-verb-table.tsv`](scriptvm-verb-table.tsv) — **1,960 rows**, one per
command slot: id, verb name, the three callback addresses, the measured argument count and operand
types, and a status column saying how strongly each row is proven. **1,870 of the 1,960 rows carry a
measured arity**; on the 1,210 of those that the authored catalog also names and declares, the two
agree **1,209 times** (§10, §12).

## 1. What the player sees

Nothing on screen belongs to this system by itself — and almost everything on screen passes through
it.

When a cutscene changes the weather, when a guard turns to watch you, when a chest refuses to open
until a flag is set, when the game holds a line of dialogue until you press a button, when Vaan
walks to a mark and the camera waits for him to get there — a zone script issued a *verb*, and this
is the machinery that found the engine code behind that verb and handed it its arguments.

For a modder this is the seam between the two halves of FFXII. One half is authored: the `.ebp`
scripts inside the game's archive, which can be decompiled, edited and recompiled. The other half is
compiled engine code that cannot. A script says `setweatherslot(2)`. Knowing *which* native function
answers that call, and that it takes exactly one whole number which it then clamps to the range 1–3,
is the difference between editing a script with confidence and editing it by experiment.

It also explains a shape of the scripting language a modder meets immediately: some verbs finish
instantly (`setforcefightmode`) and some take time (`camerasync`, `wait`, `motionsync`) and hold the
script until they are done. That is not a convention the script authors invented — it is built into
the table, and you can read which kind a verb is straight out of it.

## 2. Native mechanism

### 2.1 A verb call is one bytecode instruction with a 16-bit operand

The interpreter (`WorldActorScriptVM_InterpretBytecode`, `0025E4C0`) fetches an opcode byte from the
program counter in `r14`. For every opcode at or above `0x47` it pre-decodes the two bytes that
follow as a little-endian 16-bit immediate into `bx`:

```asm
0025E59D  movzx r12d, byte ptr [r14]     ; opcode = *pc
0025E5A9  cmp   r12b, 0x47
0025E5AD  jb    0x25E5C2                 ; short instruction: no immediate
0025E5AF  movzx ebx, byte ptr [r14 + 2]  ; high byte
0025E5B4  movzx eax, byte ptr [r14 + 1]  ; low byte
0025E5B9  shl   bx, 8
0025E5BD  or    bx, ax                   ; bx = *(u16 *)(pc + 1)
```

Four opcodes turn that immediate into a native verb call. All four are three bytes long — one opcode
byte plus the 16-bit call id:

| opcode | mnemonic | what it does with the actor | what it does with the result |
|---:|---|---|---|
| `0x58` | `CALL` | binds the verb to the **current** actor: `cmdState[8] = *(u16 *)actor` | leaves it on the value stack |
| `0x59` | `CALLACT` | **pops** an actor id off the value stack and binds the verb to it | leaves it on the value stack |
| `0x5D` | `CALLPOPA` | like `CALL` | pops it into the **A register**, `cmdState[0x10]` |
| `0x5E` | `CALLACTPOPA` | like `CALLACT` | pops it into the A register |

That is the whole of `SCRIPT.verb(...)` versus `ACTOR.verb(...)` in the source language: the same
verb id, a different opcode, and one extra stack operand. The `…POPA` pair exists because the
executor **always** pushes a return value (§2.4) — a script that does not want it needs an opcode
that takes it back off. `cmdState[0x10]` is the A register because opcode `0x1B PUSHA` pushes that
slot and `0x1C POPA` pops into it.

> **These four opcode numbers are not the ones the interpreter document originally listed.** The
> mnemonic column of the shipped descriptor table is rotated one record relative to its numeric
> columns. Corrected there on 2026-09-02 — see that document's §11, and §8 below.

`CALLACT` (`0x59`) and `CALLACTPOPA` (`0x5E`) both pop the actor id **only on the command's first
call** (`cmp byte [rsi+0x15], 0`), so a durative verb does not re-consume its actor operand every
frame. Only three of the four opcodes contain a direct call to the dispatcher — `002619B6` (`CALL`),
`00261A19` (`CALLACT`) and `00261AD4` (`CALLPOPA`); `CALLACTPOPA` reaches it by jumping into
`CALLPOPA`'s body at `00261ABF`, just past the current-actor load it does not want.

### 2.2 The id splits into a family and a command

`VMNativeCommand_ExecuteLifecycle` (`002621D0`) takes the id in `r9d` and immediately cuts it in two:

```asm
00262205  sar r12d, 0xc          ; family  = id >> 12      (0..15)
0026220C  and r15d, 0xfff        ; command = id & 0x0FFF   (0..4095)
```

**Four bits of family and twelve of command.** Sixteen families exist because the field is four bits
wide, and `VMNativeCommandDispatch_InitializeFamilyTables` (`003DC2D0`) fills exactly sixteen
pointers. It writes a default into all sixteen with a `rep stosq`, then overwrites four:

```asm
003DC2D5  lea rax, [rip + 0x1b4a444]   ; -> 0x01F26720   the default table
003DC2DC  mov ecx, 0x10                ; 16 entries
003DC2E1  lea rdi, [rip + 0x277bc08]   ; -> 0x02B57EF0   the family array
003DC2E8  rep stosq
003DC2F0  lea rax, [rip + 0x1b11409]   ; -> 0x01EED700
003DC2F7  mov [rip + 0x277bbf2], rax   ; -> 0x02B57EF0 + 0x00  = family 0
003DC2FE  lea rax, [rip + 0x1b4beab]   ; -> 0x01F281B0
003DC305  mov [rip + 0x277bbfc], rax   ; -> 0x02B57EF0 + 0x18  = family 3
003DC30C  lea rax, [rip + 0x1b4d105]   ; -> 0x01F29418
003DC313  mov [rip + 0x277bbfe], rax   ; -> 0x02B57EF0 + 0x28  = family 5
003DC31A  lea rax, [rip + 0x1b4d11f]   ; -> 0x01F29440
003DC321  mov [rip + 0x277bc00], rax   ; -> 0x02B57EF0 + 0x38  = family 7
```

Every one of those RIP-relative targets is arithmetic you can redo by hand: displacement plus the
address of the *next* instruction. Nothing here is guessed.

| family | id range | table | commands |
|---:|---|---|---:|
| **0** | `0x0000`–`0x0FFF` | `0x01EED700` | **1,496** |
| **3** | `0x3000`–`0x3FFF` | `0x01F281B0` | **147** |
| **5** | `0x5000`–`0x5FFF` | `0x01F29418` | **1** |
| **7** | `0x7000`–`0x7FFF` | `0x01F29440` | **104** |
| 1, 2, 4, 6, 8–15 | — | `0x01F26720` | **212**, shared |

**1,960 command slots in five physical tables.** Twelve families share the default table, so ids in
them alias: `0x2005` and `0x4005` resolve to the same command.

### 2.3 Three callbacks per command

The three accessors give the record layout with no interpretation left over:

```asm
GetBeginCallback  (003DC270):  movsxd rax, edx ; shl rax, 5 ; mov rax, [rax + rcx + 8]
GetPollCallback   (003DC240):  movsxd rax, edx ; shl rax, 5 ; mov rax, [rax + rcx + 0x10]
GetResultCallback (003DC2A0):  movsxd rax, edx ; inc rax ; shl rax, 5 ; mov rax, [rax + rcx]
```

`(command + 1) * 32` is the same address as `32 + 32 * command`, so all three land in one 32-byte
record that starts at `table + 8 + 32 * command`:

```
table + 0x00                    s32   command count
table + 0x04                    -     4 bytes of padding (zero in all five tables)
record N = table + 8 + 32*N
  +0x00   ptr   begin (N)
  +0x08   ptr   poll  (N)
  +0x10   ptr   -- unused --
  +0x18   ptr   result(N)
```

All three accessors reject a null family table and bounds-check the command against the table's own
count (`cmp edx, [rcx] / jge`), returning `NULL` on failure. **An out-of-range verb fails closed**;
it does not read past the table.

**The `+0x10` slot is null in all 1,960 records**, in every family. The engine never uses it.

> **Cross-check 2026-09-11 (FABLE, answering OPUS-VM-FAMILY-LAYOUT / -SURFACE-MEASURED).** OPUS read
> the same three accessors independently and enumerated the four populated tables: family 0 1,496
> (270 begin / 230 poll / 1,227 result), family 3 147 (5 / 4 / 132), family 5 one, family 7 104
> (27 / 30 / 74) — **1,748 slots**. The 212 between that and the 1,960 above are the default table
> `0x01F26720` (count `0xD4`), which is a real command table and not a default *handler*: family 2's
> `0x2000`–`0x20D3` debug verbs live in it and are reachable (the `0x2000+` note below), and the other
> eleven families alias it. OPUS's reading that the result callback sits "at the next record's base"
> is the same bytes with the record origin taken at `table + 0` instead of `table + 8`; from `+8` the
> three callbacks are `+0x00` / `+0x08` / `+0x18` of one record, as above. Verb 97 of family 3 is
> `0x3061` `btlAtelSetHpLowLimit`, result-only — the record at `0x01F28DD8` reads `NULL`, `NULL`,
> `NULL`, `005105E0` — and the count `0x93` = 147 bounds it, so OPUS's retracted index 392 was the
> descriptor base taken as the array base, nothing more. `0016D6A0` (`_guard_check_icall`) stands in
> for an absent callback in every table, as it does in the calculator table at `0x01EFA5C0`.

### 2.4 The lifecycle: what actually runs, and when

Reading `002621D0` end to end gives a different flow from a plain three-way branch on the phase byte:

```c
phase = cmdState[0x15];
poll  = GetPollCallback(family, command);          /* fetched up front, always */

/* the command's owner context: cmdState[8] is the actor the verb was bound to */
owner = (cmdState[8] == *(u16 *)b) ? b : FUN_00358940(a);

if (phase == 0) {                                  /* first call */
    cmdState[0x0C] = 0;                            /* clear the return slot */
    begin = GetBeginCallback(family, command);
    if (begin) begin(b, owner, cmdState + 0x18, valueStack, a);
}
                                                   /* phase 0 and 1 both fall through to poll */
running = poll ? poll(b, owner, cmdState + 0x18) : 0;
if (running & 1) { cmdState[0x15] = 1; return 1; } /* stay in progress, come back next frame */

/* finished (or never durative) - run the result callback in this same call */
result = GetResultCallback(family, command);
if (result) result(b, owner, cmdState + 0x18, valueStack);

/* push the command's return value back onto the value stack */
switch (cmdState[0x15]) {                          /* the result callback set this */
  case 2:  push_int  (valueStack, *(s32   *)&cmdState[0x0C]); break;
  case 3:
  default: push_float(valueStack, *(float *)&cmdState[0x0C]); break;   /* phase >= 3 */
  case 0: case 1:
           push_int  (valueStack, 0);              /* callback wrote no result */
}
cmdState[0x15] = 0;                                /* slot reusable */
return 0;
```

Three consequences a reader should take away:

- **A command with only a `result` callback completes inside one call.** With no `poll`, `running`
  comes from a zero-initialised local, so the executor falls straight through to `result`. That is
  why 1,573 of the 1,960 commands are instantaneous even though the phase byte starts at 0.
- **Every native command yields exactly one value.** The executor pushes one — the callback's result,
  or integer `0` if none was written. That is why the bytecode has `CALLPOPA` and `CALLACTPOPA`
  opcodes at all: to throw the value away when the script does not want it. The ff12-script header
  says the same thing from the authored side — *"actually every single one returns value, but use
  CALLPOPA to ignore it when value isn't needed"* — and the executor proves it from the binary side.
- **The phase byte's values 2 and 3 are transient.** They are written by the result callback and read
  a few instructions later in the *same* invocation to choose int or float; the executor then resets
  the byte to 0. On entry the byte is only ever 0 or 1.

### 2.5 Where a callback's arguments come from

Every callback receives the same four things, in the Microsoft x64 convention:

```
rcx = b            the script/actor context the verb was issued from
rdx = owner       the resolved target actor (differs from b only after CALLACT)
r8  = cmdState + 0x18    16 bytes of per-command scratch, private to this command
r9  = valueStack   <-- the arguments live here      (begin and result only; poll gets three args)
```

Which is why nearly every handler in the game starts the same way: `mov rcx, r9` followed by a call
to a pop primitive. That two-instruction sequence *is* "read an argument".

**Where the arguments are read from depends on the command's shape:**

- **Instantaneous** (result only) — the `result` callback pops the arguments, does the work, and
  writes the return value.
- **Durative** (`begin` present) — the `begin` callback pops the arguments and stashes what it needs
  in the 16-byte scratch block; `poll` then runs each frame off that scratch, and `result` writes the
  return value.

This is measured, not assumed: across §10, §11 and §12 the net value-stack effect of the argument
column reproduces the authored argument count on **1,209 of 1,210** measurable rows. The one
exception is a verb whose handler is a 3-byte `ret 0`. Two refinements are needed to get there and
both are mechanisms in their own right: a handler may hand its arguments to **another verb's
handler** over the same stack, and a handler may **bail out before reading anything** — §12.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0x02B57EF0` | family table array | 128 B | 16 pointers, one per family; built at startup |
| `0x01EED700` | family 0 command table | — | 1,496 commands — the main verb vocabulary |
| `0x01F281B0` | family 3 command table | — | 147 commands |
| `0x01F29418` | family 5 command table | — | 1 command |
| `0x01F29440` | family 7 command table | — | 104 commands |
| `0x01F26720` | default command table | — | 212 commands, shared by twelve families |
| `003DC2D0` | `VMNativeCommandDispatch_InitializeFamilyTables` | 89 B | writes the five table pointers |
| `003DC270` / `003DC240` / `003DC2A0` | Get **Begin** / **Poll** / **Result** callback | 39/39/41 B | the indexing arithmetic |
| `002621D0` | `VMNativeCommand_ExecuteLifecycle` | 461 B | id decode, phase machine, return-value push |
| `0025E4C0` | `WorldActorScriptVM_InterpretBytecode` | 14,646 B | issues the call at `002619B6` (`0x58 CALL`), `00261A19` (`0x59 CALLACT`), `00261AD4` (`0x5D CALLPOPA`) |
| `00267E10` | `VMValueStack_PopInt32CoerceFloat32` | 78 B | read one argument as `s32` |
| `00267DB0` | `VMValueStack_PopNumericDiscard` | 84 B | read one argument as `f32` — **the name is wrong**, see §8 |
| `00267F90` | `VMValueStack_PushInt32` | 39 B | push an integer |
| `00267F60` | `VMValueStack_PushFloat32Bits` | 41 B | push a float |
| `0026B4E0` | `VMResult_WriteInt32` | 28 B | write an integer return value + phase 2 |
| `0026B4C0` | `VMResult_WriteFloat32` | 28 B | write a float return value + phase 3 |
| `00267FC0` | opcode `0x48 PUSHV` body | 296 B | read a script variable by declared type and push it |
| `00267E60` | opcode `0x49 POPV` body | 256 B | pop and store into a script variable |
| `00268100` | opcode `0x4B PUSHP` body | 164 B | push a **reference** to a variable (out-parameters) |
| `002650B0` | reference resolver | 206 B | turns a pushed reference back into a real address |
| `0016D6A0` | the shared `ret 0` stub | 3 B | fills ~~27~~ **34 callback slots over 33 commands** (25 `result`, 9 `begin`, 0 `poll`; 18 commands have only the stub) — corrected 2026-09-15, `OPUS-CONTRA-VERB-STUB-COUNT-27` |

Addresses are Ghidra image base `0x00120000`, which is also this executable's PE `ImageBase`; file
offsets follow from the section table (`.data` VA `0x01DF0000` ↔ raw `0x01CCE600`, so
`0x01EED700` is at file offset `0x01DCBD00`).

## 4. Data structures and formulas

### 4.1 Reaching a handler from a call id — the whole chain

```c
/* bytecode:  [0x58] [id_lo] [id_hi]     three bytes, opcode 0x58/0x59/0x5D/0x5E */
u16   id      = *(u16 *)(pc + 1);

u32   family  = id >> 12;                       /* sar r12d, 0xC */
u32   command = id & 0x0FFF;                    /* and r15d, 0xFFF */

void *table   = *(void **)(0x02B57EF0 + 8 * family);
if (table == NULL)                    -> callback is NULL
s32   count   = *(s32 *)table;                  /* 1496 / 147 / 1 / 104 / 212 */
if ((s32)command >= count)            -> callback is NULL

void *begin   = *(void **)((u8 *)table +  8 + 32 * command);
void *poll    = *(void **)((u8 *)table + 16 + 32 * command);
void *result  = *(void **)((u8 *)table + 32 + 32 * command);
```

Worked by hand for the two verbs this document is anchored on:

```
setforcefightmode, id 0x0334
  family  = 0x0334 >> 12   = 0
  command = 0x0334 & 0xFFF = 0x334 = 820
  table   = 0x01EED700 ,  count = 1496 , 820 < 1496  -> in range
  result  = *(u64 *)(0x01EED700 + 32 + 32*820)
          = *(u64 *)(0x01EED700 + 0x6620)
          = *(u64 *)0x01EF3D20
          = 0x003444D0                                  <-- the handler
  begin = poll = NULL  ->  instantaneous

openfullscreenmenu_48d, id 0x048D
  family = 0, command = 0x48D = 1165
  begin  = *(u64 *)(0x01EED700 +  8 + 32*1165) = 0x003462D0
  poll   = *(u64 *)(0x01EED700 + 16 + 32*1165) = 0x00352E00
  result = *(u64 *)(0x01EED700 + 32 + 32*1165) = 0x00346DA0
  begin non-null  ->  durative
```

### 4.2 The command state record — 40 bytes

The 5th argument to the executor is one 40-byte record, and the result primitives locate the *same*
record independently, which is what ties the two halves together:

```c
/* VMResult_WriteInt32 (0026B4E0) */
s8    slot = *(s8 *)(ctx + 0x11);
u8   *base = *(u8 **)(ctx + 0xA8);
u8   *rec  = base + slot * 40;              /* lea r8,[rax+rax*4] = *5, then [r8*8] = *40 */
rec[0x15]  = 2;                             /* phase: finished, integer */
*(s32 *)(rec + 0x0C) = value;
/* VMResult_WriteFloat32 (0026B4C0) is identical with phase 3 and a movss */
```

```
command state record (stride 0x28 = 40 bytes)
  +0x00  ...   (unread here)
  +0x08  u32   bound actor id      compared against *(u16 *)b at 00262225
  +0x0C  u32   return value        read as s32 (phase 2) or f32 (phase >= 3)
  +0x15  u8    phase               0 = not started, 1 = running,
                                   2 = finished/int, 3+ = finished/float (both transient)
  +0x18  16 B  per-command scratch passed to begin/poll/result as r8
```

The scratch block at `+0x18` is how a durative verb carries state across frames: `begin` writes it,
`poll` reads it every frame. `openfullscreenmenu_48d`'s `begin` writes `scratch[4]` and
`scratch[8]`; `setforcefight`'s writes `scratch[0]`, `scratch[2]`, `scratch[3]`, `scratch[4]` and
`scratch[0xC]`.

### 4.3 The value stack — where arguments live

One flat structure of parallel arrays, capacity 63:

```
value stack
  +0x000            s32   sp                  the number of values on the stack
  +0x004 + i        u8    kind                1 = integer, 2 = float
  +0x044 + i        u8    source type         0..5 = the declared type of the variable it came from
                                              (uchar, char, ushort, short, int, float);
                                              6 = a literal or computed value, not from a variable
  +0x084 + i*4      u32   word A              written 0 by all 78 stores (proven, BQ-1); never read
  +0x184 + i*4      u32   word B              THE VALUE - int32, float32 bits, or a reference
```

**Push** (`VMValueStack_PushInt32`, `00267F90`):

```c
s32 i = *(s32 *)stack;
if (i >= 0x3F) return;                      /* full: silently drops the value */
stack[0x04 + i]        = 1;                 /* kind = integer   (2 for the float push) */
stack[0x44 + i]        = 6;                 /* source type = literal */
*(u32 *)(stack + 0x84 + i*4) = 0;
*(u32 *)(stack + 0x184 + i*4) = value;
*(s32 *)stack = i + 1;
```

**Pop as int32** (`VMValueStack_PopInt32CoerceFloat32`, `00267E10`):

```c
s32 n = *(s32 *)stack;
if (n <= 0)          return 0;              /* underflow: 0, stack untouched, no diagnostic */
n--; *(s32 *)stack = n;
switch (stack[0x04 + n]) {
  case 1: return *(s32 *)(stack + 0x184 + n*4);                        /* verbatim */
  case 2: return (s32)*(float *)(stack + 0x184 + n*4);                 /* cvttss2si: truncate toward zero */
  default: FUN_008620C0(1); return 0;                                  /* bad kind */
}
```

**Pop as float32** (`00267DB0`, currently named `VMValueStack_PopNumericDiscard`):

```c
s32 n = *(s32 *)stack;
if (n <= 0) { FUN_008620C0(1); return 0.0f; }
n--; *(s32 *)stack = n;
switch (stack[0x04 + n]) {
  case 1: return (float)*(s32   *)(stack + 0x184 + n*4);               /* cvtdq2ps */
  case 2: return        *(float *)(stack + 0x184 + n*4);               /* verbatim */
  default: return 0.0f;                                                /* no diagnostic */
}
```

The two pops are **mirror images in their error handling**: the int pop is silent on underflow and
noisy on a bad kind; the float pop is noisy on underflow and silent on a bad kind. `FUN_008620C0` is
the fatal-error emitter, and in the retail build it tail-jumps to the `ret 0` stub — so **neither
diagnostic does anything in the shipped game.** A script that under-flows the stack gets a zero and
keeps running.

**Coercion is automatic in both directions and is lossy in one.** Pushing `3.7` and popping it as an
integer yields `3` (truncation toward zero, not rounding). Pushing `-3.7` yields `-3`.

### 4.4 Argument order

Arguments are read in **stack order, top first**. The ff12-script decompiler builds its parameter
list by popping the reconstructed operand stack in the same order
(`popOperands` → `transferCallArguments`), so the catalog's `paramType[0]` **is the first value the
handler pops.**

Proved against a five-argument verb with a distinctive shape, `getmapjumpposbyindex` (`0x0211`,
handler `003538F0`), whose catalog signature is
`{FLOAT|POINTER, FLOAT|POINTER, FLOAT|POINTER, FLOAT|POINTER, SHORT|INT}`:

```c
p1 = resolve(pop());     /* pops 1..4 each go straight into the reference resolver 002650B0 */
p2 = resolve(pop());
p3 = resolve(pop());
p4 = resolve(pop());
idx = pop();             /* pop 5 is used as a plain integer index */
FUN_00377AB0(idx, out);  /* fills four floats */
*p4 = out[0]; *p3 = out[1]; *p2 = out[2]; *p1 = out[3];
```

Four pointer-typed parameters followed by one integer, in exactly the catalog's order. A wrong
ordering convention would have put the integer first.

### 4.5 Reference (out-)parameters

A verb that writes back into a script variable receives a **packed reference**, pushed by opcode
`0x4B PUSHP` (`00268100`):

```c
u32 desc  = variableDescriptor;             /* from the instruction's operand */
u32 type  = desc >> 28;                     /* 0..5, the declared element type */
u32 index = elementIndex;
if (type is 16-bit) index *= 2;             /* add edx, edx   */
if (type is 32-bit) index *= 4;             /* lea edx,[rdx*4]*/
u32 packed = ((desc & 0x00FFFFFF) + index) | (desc & 0x07000000) | 0x70000000;
push_int(packed);                           /* kind = 1, source type = the variable's type */
```

and turned back into an address by `002650B0`:

```c
u32 scope = (packed >> 24) & 7;             /* sar eax,0x18 ; and eax,7 */
u32 off   =  packed & 0x00FFFFFF;
switch (scope) {                            /* 6-way jump table, default for scope 6 and 7 */
  case 0: return *(u8 **)(ctx + 0x48) + off;
  case 1: return *(u8 **)(ctx + 0x40) + off;
  case 2: return ((u8 *(*)(void *))*(void **)(ctx + 0x98))(ctx) + off;
  case 3: { u8 *m = *(u8 **)ctx; return m + *(u32 *)(m + 0x40) + off; }   /* the data area */
  case 4: return *(u8 **)(ctx + 0x58) + off;
  case 5: return *(u8 **)(ctx + 0x60) + off;
}
```

> **Corrected 2026-09-12 (FABLE):** the three last arms were listed in code order. The jump table
> at `00265180` reads `{002650E8, 002650FC, 00265110, 00265155, 0026512D, 00265141}`, so **scope 3
> is the script image plus its `+0x40` data offset** (the arm at `00265155`), scope 4 is `ctx+0x58`
> and scope 5 is `ctx+0x60` — the order [the storage-class page](../Interpreter-Core/script-variables-and-their-storage-classes.md)
> §4 already had. Corroborated from data: all 502 scripts calling `0x3018 btlAtelSetEntryStruct`
> pass `0x03xxxxxx`, and the entry tables parse at `image + [image+0x40] + offset` in every one
> ([the keep-entry page](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md)
> §7 FD-1).

So a reference is an ordinary integer on the value stack whose top nibble is `0x7`, carrying a
3-bit scope and a 24-bit byte offset. The `+0x44` byte alongside it carries the element type so the
callee knows the width to write.

### 4.6 Actor handles

Opcode `0x4D PUSHACT` (`00261806`) packs an actor reference into a single integer:

```c
if (index < *(u32 *)actorTable) {
    u16 hi = *(u16 *)(actorTable + 16*index + 0x0E);
    value  = (hi << 16) | index;
    value |= (1 << 14);                     /* bts edx, 0xE */
} else {
    value = 0x8000;                         /* the "no actor" sentinel */
}
push_int(value);
```

**Bit 14 set marks a live actor handle; `0x8000` is the out-of-range sentinel.** `PUSHTAG` (`0x4C`)
uses the same `0x8000` sentinel for an out-of-range tag.

### 4.7 Reading a variable's declared type

`PUSHV` (`00267FC0`) dispatches on `descriptor >> 28` through a six-case jump table whose arms are,
in order: `movzx byte`, `movsx byte`, `movzx word`, `movsx word`, `mov dword`, `movss` — i.e.
`uchar, char, ushort, short, int, float`, exactly ff12-script's `enVarType` 0..5. The value's
declared type then travels with it in the value stack's `+0x44` byte.

## 5. Call chain

```
authored .ebp zone script  (ff12-script can decompile and recompile it)
  -> compiled bytecode
     -> WorldActorScriptVM_InterpretBytecode              0025E4C0
        opcode 0x58 CALL / 0x59 CALLACT / 0x5D CALLPOPA / 0x5E CALLACTPOPA
        id = *(u16 *)(pc+1)
          -> VMNativeCommand_ExecuteLifecycle             002621D0     [AUTHORITY 01 -> *]
             family = id>>12 , command = id & 0xFFF
               -> familyTables[family]                    0x02B57EF0
                  -> GetBegin/Poll/ResultCallback         003DC270 / 003DC240 / 003DC2A0
                     -> the native handler
                        -> VMValueStack_Pop*              reads the arguments
                        -> the engine subsystem           WorldAreaField, UI, Movement, Party, ...
                        -> VMResult_Write*                writes the return value
             -> push the return value back on the value stack
```

**Upstream (who causes this):** only the interpreter, and this was checked across the whole
executable, not just the interpreter. Disassembling every function in `.text` finds **exactly three
call sites for `002621D0`** — `002619B6`, `00261A19`, `00261AD4`, inside the `CALL`, `CALLACT` and
`CALLPOPA` opcode handlers (`CALLACTPOPA` jumps into `CALLPOPA`) — and **exactly one caller for each
of the three callback accessors**, which is `002621D0` itself. The dispatch has no second
entrance.

**Downstream (what this causes):** the whole engine. Of the 2,277 non-null callback pointers across
all five tables, 2,187 are owned by `Script/VM Native Bridge`, 20 by Movement, 11 by Party, 1 by
ActorEntity and 58 are unowned. **1,886 distinct functions** serve as callbacks; verbs share
handlers, so the count is smaller than the number of slots.

**This is an owner transition, not a trigger** — `[AUTHORITY 01 -> *]` under `CALL-CHAINS.md` rule 6,
labelled 2026-09-18. Above `002621D0` the state belongs to the script VM;
below it, to whichever subsystem the handler edits. **The destination is `*` because it is selected
at run time from `familyTables[id>>12]`**, named in the chain above — and this hop is why rule 6
allows `*` on the destination at all: its first draft refused it, on the reasoning that a hop always
knows where it landed. A dispatcher does not. The transition is the reason the standing rule
*"a ScriptVM wrapper is authored-intent evidence, never a replay seam"* exists: the seam is the
handler, not the verb.

**Do not confuse with:**

- **The opcode jump table at `0x00261DF8`** — 100 entries, selects *which instruction* runs.
  This document is about the table that selects *which verb* an instruction calls. The two are
  different tables with different strides and different index spaces.
- **The interpreter's own value-stack helper `FUN_0025D740`** — a binary-operand pop shared by the
  comparison opcodes. It reads the same value stack but is not part of verb dispatch.
- **Phyre's embedded Lua** — a completely separate scripting system in the same binary.
- **`0x01EFA5C0`, the combat formula step table** — a different 32-bit-indexed table in the same
  region of `.data`.

## 6. Modding notes

- **[`scriptvm-verb-table.tsv`](scriptvm-verb-table.tsv) is the bridge.** Decompile a zone with
  `ff12-script.exe`, find the verb, look up the row, read `arg_handler` in Ghidra.
- **Trust the row according to `arity_status`:**

  | value | rows | what it means |
  |---|---:|---|
  | `CONFIRMED` | 1,229 | the handler's net stack effect was measured exactly and equals the authored argument count |
  | `DERIVED` | 653 | measured exactly; the authored catalog declares the verb *unknown*, so **the binary supplies the arity** |
  | `DERIVED-UNNAMED` | 19 | measured exactly; no authored name for the slot at all |
  | `GUARDED` | 34 | the handler opens with an early-out test; the arity is what the **other** branch reads. See §12 |
  | `CONDITIONAL` | 24 | both branches read: class-3 predicate `00263D00` (`guard` column) skips one mid-handler pop, so the arity is `n` for most actors and `n−1` when it holds — `net_or_sums` carries the `lo\|hi` pair; `arity` is the catalog value where it agrees (15 rows, incl. `aturny` = the smaller), else the larger. The 12 turn verbs (via `00357DE0`) measure `2\|3`, the 12 look-at verbs (`00357D10`/`00357C40`) `3\|4`. BQ-9 |
  | `LOWER-BOUND` | 0 | (retired 2026-09-27 — BQ-9 measured all 33) |
  | `UNPROVEN` | 0 | (retired 2026-09-27 — BQ-9 measured all 57) |
  | `CONFLICT` | 1 | `unkCall_5c7`: declared 2 arguments, handler is the shared `ret 0` |

- **`guard` names the early-out** where there is one: `fsmenu` for the 33 fullscreen-menu verbs that
  share one null-object test, `other` for the single family-3 verb with its own. **A guarded verb
  that bails does not read its operands** — §12.

- **`pops_int` and `pops_float` give the operand *types*, not just the count.** For a verb the
  catalog leaves unknown this is the only type information there is: `setmapambient` reads four
  floats, `setmapidfloor_101` reads four integers, `bganimespeed` reads one of each.
- **Maximum arity is 8**, measured — and ff12-script's `tCallTarget` allocates exactly
  `paramType[8]`. Two independent sources hit the same ceiling.
- **Read all three callbacks, not just one.** A verb with a `begin` is durative: its arguments are
  read in `begin`, not in `result`. Looking only at the `result` column is what produced a
  long-running false contradiction in the predecessor document.
- **327 verbs are durative, 1,573 are instantaneous.** If you need a verb that takes time, it needs
  `begin` and `poll`; a `result`-only slot completes within the frame.
- ~~**27 command slots point at the 3-byte `ret 0` stub** and 33 have no callback at all.~~ **34 callback slots over
  33 commands point at the 3-byte `ret 0` stub** (25 `result`, 9 `begin`, none `poll`; `0x03BD` has it in both), and
  **4 commands have no `begin`, `poll` or `result` callback at all**. Measured 2026-09-15 over all five tables
  (1,496 / 147 / 1 / 104 / 212 records, which equal the published counts) — `OPUS-CONTRA-VERB-STUB-COUNT-27`. The 18
  commands whose only callback is the stub parse, dispatch, return integer `0`, and do nothing. `unkCall_5c7` is one: the authored catalog
  gives it two arguments, and the shipped handler consumes none.
- **The `0x2000+` "debug" verbs are real and reachable.** They are family 2 on the shared default
  table, with working handlers — `debug_setline` takes six floats, exactly like the retail `setline`.
- **13 catalog verbs cannot be called at all**: ids `0x05D8`–`0x05E4` (`unkCall_5d8` … `unkCall_5e4`)
  are past family 0's 1,496-command bound, so all three lookups return `NULL` and the dispatch fails
  closed with a pushed `0`.
- **Best intervention point:** the handler address, not the verb. Repointing a table entry changes
  one verb everywhere; hooking the handler is equivalent and leaves the table intact. Do **not**
  intervene at `002621D0` — every verb in the game passes through it every frame.
- **Regenerates itself:** the family table array at `0x02B57EF0` is built at startup by `003DC2D0`.
  Patching it in the file has no effect; patch the tables it points at, or the initializer.
- **Breaks if:** you add a command past a table's count (`table + 0`), which is the bound all three
  accessors check. Growing the vocabulary means growing that count and the table together.
- **Mod compatibility:** the authored `.ebp` scripts are the layer other mods legitimately edit. A
  mod that only changes scripts cannot conflict with one that only hooks handlers — the id space is
  the contract between them.
- **XIIOnline:** a durative command is engine state with a phase and a 16-byte scratch block, not an
  instantaneous event. Replaying "the script called verb X" is not equivalent to replaying the
  command; the begin/poll/result progression has to be respected or two clients will disagree about
  whether a scripted action is still running. The `result`-only verbs are the ones that *are* safe to
  treat as events.

## 7. What is not known

- [x] ~~What the value stack's word A at `+0x84` is for. Every push path writes it, always with zero
      by both push primitives and by all four of the executor's push paths. The interpreter contains
      **69 writes to it and 0 reads**, and neither pop primitive reads it. Whether any of those 69
      writes can carry a non-zero value is not established.~~ **BQ-1 ANSWERED 2026-09-13 (FABLE):** **word A carries no information in this image: every store of it is zero, and nothing reads it.** An image-wide census of `[base + index*4 + 0x84]` finds **78 stores**: 69 in `WorldActorScriptVM_InterpretBytecode`, 4 in `VMNativeCommand_ExecuteLifecycle` (`0026229C`, `0026232A`, `00262349`, `00262372`), one in each push primitive, two in `PUSHV` `00267FC0` (`00268085`, `002680D0`) and one in `PUSHP` `00268100` (`00268189`). Five store a literal 0; the other 73 store `r11d` (56), `ecx` (13) or `esi` (4), and a must-be-zero data-flow pass over each function's control-flow graph (zero only after `xor r,r` / `mov r,0`; any other write, or a call for a volatile register, makes it unknown; switch arms take the meet of every indirect jump) proves the register zero at **all 73**. Control: the same pass reports UNKNOWN at the value stores into word B (`+0x184`) held in `eax`, `ecx` or `edx` (28 of 28). The census's only two reads with that operand shape, `008845A0` and `008888F0`, are middleware functions far from the VM (interior read 2026-09-17, SWE2-FRONTIER: `008888F0`'s hit is [`00889186`](../../_index/ADDRESS-INDEX.md) — `movss xmm2, [rax + rdx*4 + 0x84]`, a float-array read inside a `00861EC0`/`00861FB0`/`00861FB6` wrapper set; `008845A0`'s hit is [`00884649`](../../_index/ADDRESS-INDEX.md) — `mov eax, [r10 + rcx*4 + 0x84]`, a dword-array read inside a `00808F10`-dominated body), and the non-indexed `+0x84` accesses in the VM range address other structures. So a reconstruction may store zero there or drop the field; nothing observable depends on it, except code that copies the whole stack by size. What the field was for when authored is not recoverable from the image.
- [x] ~~The scope numbering of packed references. `002650B0` decodes a contiguous 3-bit field 0..5,
      while ff12-script's `enVarScope` uses 0, 1, 2, 4, 5, 7. The correspondence is **not**
      established and must not be assumed.~~ **BQ-2 ANSWERED 2026-09-12 (FABLE) — the same field,
      the same numbers** ([the storage-class page](../Interpreter-Core/script-variables-and-their-storage-classes.md) §2.2 already matched the enum to the class switch; this
      adds the bit-level proof). ff12-script packs a reference as the bitfield `tVariable { pos : 24,
      scope : 3, flv : 1, type : 4 }` (`CScriptContainer.h`) and writes that `u32` verbatim into the
      variable table (`CScriptCompileAsmWrite.cpp`, `_writeVariableEntries`); the native decoder reads
      **bits 24–26** — `sar eax, 0x18 / and eax, 7` (`002650BC`–`002650C2`) — and the low 24 bits as the
      offset (`and eax, 0xFFFFFF`). So the enum values *are* the native scope numbers: `GLOBAL 0` →
      `ctx+0x48`, `FILE 1` → `ctx+0x40`, `LOCAL 2` → the virtual call `[ctx+0x98]`, `SCRATCHPAD1 4` →
      `ctx+0x58`, `SCRATCHPAD2 5` → `ctx+0x60`. `TABLE 7` is the **array** class the descriptor
      resolver handles (`002624D2`–`00262537`, the storage-class page) — the tool marks a table's
      variable-table entry with it and points `pos` at a descriptor whose inner `var` carries the
      element's real scope; `002650B0` itself treats any value above 5 as offset-only (`0026516C`,
      base 0). Native **scope 3** — the script image plus its `+0x40` data area — has **no name in
      the tool**: its `getScopeName()` returns *"unknown"* for it, and the compiler never assigns it
      (`_scopeFromScopeDef` accepts only `global` / `scratch1` / `scratch2`, `_assignVariableStorage`
      only `FILE` / `LOCAL`), so the `0x03xxxxxx` references the shipped scripts carry (the
      keep-entry tables, FD-1) are a form the decompiler can dump but its assembler cannot re-emit.
      *Evidence added 2026-09-12:* native scope 3 resolves to the script's `+0x40` data area (the
      corrected switch above), and ff12-script's `.src.data` output is byte-equal to that area in
      602 of 602 scripts.
- [x] ~~Why **19 command slots carry no authored name** (10 in family 0, 7 in family 3, 1 in family 5,
      1 in the default table) and why **13 authored names** (`0x05D8`–`0x05E4`) have no slot.
      **BQ-3.**~~ (This supersedes **AO-5**,
      which framed the discrepancy as a single count difference of six; it is a two-way mismatch of
      19 unnamed slots against 13 unslotted names, netting to six.)
      **BQ-3 answered 2026-09-15 (FABLE): every part of the mismatch sits at a family's TAIL, and two
      of the nineteen are not verbs at all. The two sides are the same fact seen from opposite ends —
      the shipped table and the authoring catalog diverge only where a table grows.**
      - **Family 0's ten unnamed slots are `0x059E`, `0x059F`, `0x05AA`, `0x05AE`, `0x05AF`, `0x05B2`,
        `0x05B3`, `0x05C0`, `0x05C1`, `0x05CC`.** The family spans `0x0000`–`0x05D7` (1,496 rows), so
        the **first** of them stands at **96.1 %** of the family and **all ten lie in its last 3.9 %**.
      - **Family 3's seven are `0x3086`–`0x308F`** in a family spanning `0x3000`–`0x3092` (147 rows):
        the first at **91.2 %**, all seven in the last **8.8 %**.
      - **The 13 unslotted names are `0x05D8`–`0x05E4` — the thirteen ids immediately after family 0's
        last id `0x05D7`, contiguous, with no gap.** Not scattered through the table: appended past its
        end.
      - **Two of the nineteen are not verbs.** `0x20D3` is the **last id of family 2** and its handler
        is `0016D6A0`, the folded three-byte `ret 0` — the terminator the dispatch falls closed onto,
        which is what the count called "the default table". And family 5 **has exactly one row**,
        `0x5000`, so its "unnamed slot" is the whole family; its handler `003567F0` is the one
        `keywait` and `keywaitr` already share.
      - **Three handlers are shared by pairs of unnamed slots** — `0050C7F0` (`0x05B2`/`0x05B3`),
        `0050F3C0` (`0x3086`/`0x3088`) and `0050F3F0` (`0x3087`/`0x3089`) — the same alias-pair shape
        that `keywait` / `keywaitr` show under a name.
      - **The reading those facts support, offered as a reading.** A mismatch caused by *renaming* or
        *reordering* would scatter through the table; a mismatch caused by **version skew between the
        shipped table and the authoring catalog** appears only where a table grows, which is its end.
        The image carries verbs at the tail of two families that the catalog never learned, and the
        catalog knows thirteen consecutive verbs past family 0's end that the image does not ship. The
        netting to six that `AO-5` reported is an arithmetic coincidence of two unrelated tails.
      - **What would falsify it, stated so the reading can be tested:** a single unnamed slot in the
        *middle* of a family, or an unslotted name that is not adjacent to a family bound. Neither
        occurs in this table.
      - **Not claimed:** which build each side comes from, or which direction is newer. The positions
        show the two artefacts diverge at their tails; they do not date either one.
- [x] ~~Whether the seven `*sync` verbs whose `begin` performs a push-then-pop round trip are
      genuinely zero-argument or hide an optional argument.~~ **ANSWERED 2026-09-02 — genuinely
      zero-argument.** All seven measure net 0 and all seven are `CONFIRMED` against a declared 0.
      The round trip is no longer purposeless either: §12 proves that handlers hand arguments to one
      another **through the value stack**, and a push-then-pop pair is that same hand-off with the
      producer and consumer inlined into one function and the argument a constant. **BQ-4.**
- [x] Whether any writer outside `002621D0` sets the phase byte to 2 or 3 before entry, which would
      make the executor's `phase >= 2` arm reachable as a persistent state rather than a transient
      one. **BQ-5.**
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): no writer outside the executor's own call leaves 2 or 3 behind, so the `>= 2`
      entry arm is unreachable from any writer in this image.** Control: `../Native-Command-Lifecycle/members/bq5_phase_writers.py` (4 checks, FAILS 0).
      - **The non-zero writers are exactly four.** `VMResult_WriteFloat32` writes 3; `VMResult_WriteInt32` writes 2;
        `002651A0`, a write-and-read-back, writes 2; the executor writes 1. The census covers every byte write to the
        phase byte image-wide in all three addressing shapes: indexed, through `cmdState`, and through a callback's
        `cmdState + 0x18` parameter. Every other writer stores 0.
      - **The three result writers run only inside lifecycle callbacks.** All 382 functions that call them are
        callbacks in [the verb table](scriptvm-verb-table.tsv), or helpers reached only from callbacks. A callback
        with a direct caller is called only by another callback. No callback's pointer sits in data more often than
        its table roles, and no writer's address is taken.
      - **No callback changes the current slot** `b[0x11]`, so a written result lands on the slot being run. The
        one writer of that byte starts entry scripts and is not a callback.
      - Inside the call, the executor resets the byte to 0 on every result path, or overwrites it with 1 while a
        poll reports busy.
- [x] What the descriptor table's `+0x02` field means (it reproduces ff12-script's `unk4` exactly, **ANSWERED 2026-09-02** — a displacement scan over all 38,161 bodies **with a positive control**: descriptor `+0x00` is touched at 22 sites (reproducing the document's own figure) while `+0x02` and `+0x08` are touched at **0 sites each**. The instrument answers on the field that *is* read, so the zero is a measurement, not a silence.
      100/100, and no reader of it exists in `.text`). **BQ-6.**
- [x] ~~646 of the 1,960 rows carry no arity evidence at all.~~ **CLOSED 2026-09-02** — **1,870 of
      1,960 rows now carry a measured arity**, agreeing with the authored count 1,209 times out of
      1,210. The 41 path-dependent rows that §10 could not measure are resolved in §12: 7 were
      argument hand-offs between handlers, and 34 are early-out guards whose other branch reads
      exactly the declared count. **BQ-7.**
- [x] The **90 rows still without a measured arity**: 33 command slots with no callback at all,
      31 whose operand reads sit inside a loop or whose control-flow graph exceeded the path budget,
      and 26 whose handler calls a function whose own stack effect is not exactly known. Each needs a
      body read; none is blocked on an instrument. **BQ-9.**
      *ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: all 90 now have an arity - the 33 no-callback verbs are 0 by
      the dispatch ABI, 22 have a single need, 24 turn/look-at verbs take n or n-1 operands through the class-3
      predicate, and the 11 loop rows are read by hand; per-row values in the register row and
      [the control](../../_index/candidates/bq9-sync-arity/bq9_sync_arity.py). The TSV's status column is its generator's.*
      *TSV updated 2026-09-27 (SWE2-DATA): all 90 rows carry the answer — `members/bq9_arity_update.py`. The 33
      no-callback rows keep `pops_int` empty (there are no pop sites — the family has no callback that receives the
      stack) and read `arity 0`; the 33 exact rows read `CONFIRMED`/`DERIVED` per the catalog rule; the 24 two-valued
      rows carry the new `CONDITIONAL` status above. The sync family is what "no callback" *is*: a sync verb blocks
      until its paired operation finishes rather than dispatching one, and arity 0 is proven by the dispatch ABI —
      `002621D0` hands the value stack (`r9`) only to `begin` and `result`, and none of the 27 distinct poll bodies
      reads `r9` before writing it.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `family = id >> 12`, `command = id & 0xFFF` | `sar r12d, 0xc` / `and r15d, 0xfff` in the complete body of `002621D0` | 1 |
| Five tables at the five stated addresses, and which family indices they fill | complete body of `003DC2D0`; every RIP-relative displacement re-added by hand from the next instruction's address | 1 |
| Command counts 1496 / 147 / 1 / 104 / 212 | first dword of each table read out of the file at the offsets the PE section table gives | 1 |
| Record layout `+8 begin`, `+16 poll`, `+32 result`, stride 32 | complete bodies of `003DC270`, `003DC240`, `003DC2A0` | 1 |
| All three bound-check and fail closed | `test rcx,rcx / je` and `cmp edx,[rcx] / jge` in all three | 1 |
| The `+0x10` slot is unused | swept all 1,960 records in all five tables: **0 non-null** | 1 |
| No callback points outside `.text` or off a function entry | swept all 5,880 pointer slots: **0** violations of either | 1 |
| Call ids come from a 16-bit immediate at `pc+1` | `movzx/movzx/shl/or` at `0025E5AF`–`0025E5BD`, and `movzx r9d, bx` at each of the three call sites | 1 |
| The four call opcodes and what they do with the actor and the result | complete handler bodies at `0026199D` (`0x58`), `002619EF` (`0x59`), `00261ABB` (`0x5D`), `00261AFE` (`0x5E`), reached through the opcode jump table at `0x00261DF8`; `cmdState[0x10]` identified as the A register from `0x1B PUSHA` (`0025F322`) and `0x1C POPA` (`0025F32A`) | 1 |
| Value-stack layout and capacity 63 | complete bodies of `00267F90`, `00267F60`, `00267E10`, `00267DB0`, plus the executor's own push paths | 1 |
| Coercion rules (`cvttss2si` truncating, `cvtdq2ps` widening) | the exact instructions in the two pop primitives | 1 |
| Command state stride 40, phase at `+0x15`, return at `+0x0C`, scratch at `+0x18` | complete bodies of `0026B4E0` / `0026B4C0` (`lea r8,[rax+rax*4]` then `[r8*8]`), cross-checked against `002621D0`'s `[rdi+0x15]`, `[rdi+0xc]`, `lea r8,[rdi+0x18]` | 1 |
| Every command yields exactly one value | the executor's four push paths after `result`, all reached unconditionally | 1 |
| `0x0334` → `003444D0` → force fight mode | table read gives `003444D0`; its complete body pops one int and tail-jumps to `00254EA0`, which writes `1` or `0` to `0x01E0C2B8` | 1 |
| The fullscreen selector maps 0..6 → 17/18/10/15/19/6/22, default 2 | complete body of `002E0DA0`: `btr ecx,0xf`, `cmp ecx,6 / ja`, jump table at `0x002E0E08`, seven `mov eax,imm` arms plus the default | 1 |
| Argument order is stack order, top first | `003538F0` reads four references then one index, matching `getmapjumpposbyindex`'s catalog signature exactly | 1 + 9 |
| Reference packing and resolution | complete bodies of `00268100` and `002650B0`; the scope order from the jump table at `00265180` (2026-09-12) | 1 |
| Verb names and authored argument counts | `CScriptContainerInitializers.cpp` `callMap`, 1,954 rows parsed mechanically | 9 |
| The mapping is not spurious | path-sensitive net value-stack effect reproduces the authored argument count on **1,090 of 1,091** exactly measurable rows, the sole exception being a `ret 0` stub; see §10 | 1 + 9 |
| Measured operand types (int vs float per argument) | which pop primitive each site calls, over the same 1,870 measured rows | 1 |
| Handlers pass arguments to one another over the value stack | complete body of `00354FB0`: one pop, four `VMValueStack_PushFloat32Bits`, then a call to `00350510` — which is `0x0019 setpos_19`'s own `result` callback, declared with four arguments | 1 + 9 |
| The fullscreen-menu family bails without reading its operands | complete body of `00280120` (20 B) and of the 32 handlers that open with it; `min(sums) == 0` on all 34 guarded rows and `max(sums)` equals the declared count on all 25 that declare one | 1 + 9 |

### Correction to a neighbouring document — the opcode mnemonic table is rotated by one

[`../Interpreter-Core/worldactor-scriptvm-interpreter.md`](../Interpreter-Core/worldactor-scriptvm-interpreter.md)
§10 publishes a 100-entry opcode name list read from the descriptor table at `0x01EFEA60` by pairing
record *N*'s mnemonic pointer with opcode *N*. **That pairing is off by one for all 100 entries.**

The descriptor table's numeric columns and its mnemonic column do not agree with each other. Compared
mechanically against ff12-script's `instrArr` (101 entries, index 0 = `NOP`):

| alignment | mnemonic matches | `+0` length matches | `+2` field matches |
|---|---:|---:|---:|
| binary record *i* ↔ ff12 index *i* | **0 / 100** | **100 / 100** | **100 / 100** |
| binary record *i* ↔ ff12 index *i+1* | 96 / 100 | 97 / 100 | 83 / 100 |

The numeric columns are indexed by the opcode — which is also how the interpreter itself reads the
length, at `0025E5FE` and five other sites. So `ff12 index == opcode`, and the mnemonic stored in
record *N* names opcode ***N+1***.

**Four independent behavioural confirmations**, each read from a complete handler body:

| jump-table entry | what the handler actually does | name under the correction |
|---|---|---|
| `0x57` → `0026192C` | pops two values, sorts them, tests whether a third is between them, branches | `POP2CMPYBTWNJMP` |
| `0x58` → `0026199D` | stores the **current** actor id and calls the native dispatcher | `CALL` |
| `0x59` → `002619EF` | **pops** an actor id, then calls the native dispatcher | `CALLACT` |
| `0x48` → `00261761` | calls `00267FC0`, which reads a variable by type and **pushes** it | `PUSHV` |

Under the published (unshifted) list, `0x48` would be `POPV` — a function that unambiguously pushes.
The correction also dissolves that document's own open lead: it flagged `0x47 PUSHV` as "a
default-dispatched opcode of length 1 sitting immediately below `0x48 POPV` of length 3 … a retired
immediate-carrying opcode would look exactly like this." Opcode `0x47` is **`LONGCODESTART`**, which
is length 1 by design; `PUSHV` is `0x48` and is length 3 because it carries a variable id. There is
no anomaly.

**It answers BF-7.** The table is 100 records for 100 opcodes; opcode `0x00` is `NOP`, whose string
`'NOP'` at `0x00D11A10` is unreferenced precisely because the rotation means no record points at it;
record `0x63`'s `+8` holds `0x0000000A` rather than a pointer because it would have to name a
non-existent opcode `0x64`. Reading (i) of that document's two candidate readings is correct.

**Practically it changes which opcodes are safe to repurpose.** The six that dispatch to the default
handler are `0x01`, `0x02`, `0x19`, `0x1A`, `0x31`, `0x47` — under the corrected names **`LABEL`,
`TAG`, `OPUMINUS`, `OPFIXADRS`, `DRET`, `LONGCODESTART`**, not `TAG`/`SYSHALT`/`OPFIXADRS`/`PUSHA`/
`REQWAIT`/`PUSHV`. That document's safety warning survives intact — the length-0 opcodes are `0x00`,
`0x01`, `0x02`, so two of the six (`0x01 LABEL`, `0x02 TAG`) are still traps that spin the PC — but
the names attached to the warning were wrong.

### Correction: `00267DB0` is not a discard

The GFZ names `00267DB0` **`VMValueStack_PopNumericDiscard`**. Its complete body returns a value in
`xmm0` on every one of its four exit paths — an `int→float` widening (`cvtdq2ps`), a verbatim float,
a zero on a bad kind, and a zero on underflow. It discards nothing; it is the **pop-as-float32**
primitive, the exact counterpart of `00267E10`'s pop-as-int32, and callers such as
`setline`'s handler use its result. Proposed name: **`VMValueStack_PopFloat32Coerce`**. Recorded here
rather than applied — this session holds no mutation authority.

**Superseded readings.** None of this document's own; it is new. Its relationship to the two
existing documents in this category is corrective and is stated in §8 and §10.

## 9. Related

- [`../scriptvm-native-dispatch-table.md`](../scriptvm-native-dispatch-table.md) — the predecessor,
  which located family 0's `result` column; this document supplies the other two columns, the other
  four tables, and the parameter encoding
- [`../Native-Command-Lifecycle/native-command-lifecycle.md`](../Native-Command-Lifecycle/native-command-lifecycle.md)
  — the begin/poll/result lifecycle; §10 below refines its phase machine and refutes its
  "one record with four handlers"
- [`../Interpreter-Core/worldactor-scriptvm-interpreter.md`](../Interpreter-Core/worldactor-scriptvm-interpreter.md)
  — the interpreter that issues these calls; **its opcode name list is corrected in §8 above**
- [`../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md`](../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md)
  — `0x0334`, the anchor this document reproduces from the binary
- [`../../03-World-Area-Field/Weather/weather-slot-state-model.md`](../../03-World-Area-Field/Weather/weather-slot-state-model.md)
  — `0x021A setweatherslot`, whose handler clamps its one argument to 1..3
- [`../../16-UI/Request-Router/ui-request-router.md`](../../16-UI/Request-Router/ui-request-router.md)
  — where the fullscreen selector's 17/18/10/15/19/6/22 land
- [`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) — the tiers cited above

## 10. Falsification pass 2026-09-02 — arity as the test the mapping could have failed

**Attack chosen.** A table mapping is easy to get plausibly wrong: a wrong stride or a one-record
shift still lands on real functions in the right subsystem, and no aggregate "does it point into
`.text`" check can see it. That failure mode has already happened once in this category. So the test
had to be a quantity derived from the *handler bodies* and compared against a quantity derived from
*authored data*, with neither one able to see the other.

**The measure.** For each command's argument-reading callback, disassemble the body linearly and
compute the **net value-stack effect**: calls to the two pop primitives minus calls to the two push
primitives. Compare to the argument count in ff12-script's `callMap`. Restrict the strong claim to
handlers where the count is *exact* — no backward branch, no call to anything but the six VM
primitives, no indirect call — because in those bodies the static count is the dynamic count.

### SURVIVED: 75 of 76 exactly-measurable rows

| subset | n | exact | rate |
|---|---:|---:|---:|
| straight-line `begin` callbacks, named verbs | 47 | **47** | **100.0 %** |
| straight-line `result` callbacks, instantaneous, named verbs | 29 | 28 | 96.6 % |
| **combined** | **76** | **75** | **98.7 %** |
| all named verbs, argument column, any shape | 1,187 | 1,066 | 89.8 % |

The single exception is `unkCall_5c7`, whose handler is `0016D6A0` — the shared 3-byte `ret 0`. The
catalog gives it two arguments; the shipped binary has no implementation to consume them. That is not
a mapping error, it is an unimplemented verb, and the mapping is what revealed it.

Across the full 1,187 named rows the misses are **all on the negative side** (net < declared), with a
zero-length positive tail in the clean subset. That is the signature of under-counting inside loops
and callees, which is exactly what a linear count cannot follow — not of a shift, which would
produce errors in both directions.

### KILLED: the first version of this measure, and why it mattered

The first pass counted **pops only** and scored 60.0 % on `begin` callbacks — bad enough to suggest
the `begin` column was not the argument reader at all. It was wrong, and reading a body settled it.
`camerasync`'s `begin` (`0034C290`) is:

```asm
xor  edx, edx
call 0x267f90        ; VMValueStack_PushInt32(vs, 0)
call 0x267e10        ; VMValueStack_PopInt32CoerceFloat32(vs)
mov  [rdi], eax      ; -> the command scratch
```

**Push then pop — net zero.** `setforcefight`'s `begin` (`003419F0`) does the same thing three deep:
one real pop, three pushes, three pops, net one, matching its declared single argument. These are
register-shuffling idioms, not argument reads. Subtracting pushes moved `begin` from 60.0 % to
100.0 % on the clean subset and moved the combined rate from 71 % to 98.7 %.

**The lesson is the one this database keeps relearning:** a count of an operation is not a
measurement of its effect. The first measure produced a number that looked like evidence and would
have supported a false conclusion about which callback reads the arguments.

### SURVIVED: the two required anchors, re-derived from the file

Both were computed from the PE by hand-checkable arithmetic, not looked up in any prior artifact:

- `0x0334` → family 0, command `0x334` → `*(u64 *)(0x01EED700 + 32 + 32*820)` = **`003444D0`**, whose
  complete body pops one integer and tail-jumps to `00254EA0`, which writes `1` or `0` to
  **`0x01E0C2B8`**. `setforcefightmode`, arity 1. Matches C-5's answer exactly.
- `002E0DA0` maps selector values 0..6 to UI requests **17, 18, 10, 15, 19, 6, 22**, default **2**,
  through a jump table at `0x002E0E08`. Matches C-3 exactly. It additionally preserves **bit 15** of
  the selector into the emitted request (`btr ecx,0xf` … `or eax, edx`), which C-3 does not record.

### REFUTED: "one record carries four handlers"

[`../scriptvm-native-dispatch-table.md`](../scriptvm-native-dispatch-table.md) reports a field-count
histogram ending in *"4 handlers: 1 record"*, and
[`../Native-Command-Lifecycle/native-command-lifecycle.md`](../Native-Command-Lifecycle/native-command-lifecycle.md)
repeats it as *"unused in every record but one"*. Swept in the correct frame, the `+0x10` slot is
**null in all 1,960 records of all five tables**. The single non-null came from reading
`table + 56 + 32*1495`, which is **past the end** of family 0's 1,496 records. There is no
four-handler command.

### REFINED: the phase machine is not a three-way branch across frames

The lifecycle document reads the executor as branching *"three ways — `0`, `1`, and `>= 2`"*. The
branch structure is right, but the `>= 2` arm is not a state the executor can leave behind: it resets
the byte to `0` at `00262382` on every completion, and writes `1` only while a poll says "running".
Phases 2 and 3 are written by `VMResult_Write*` and consumed a few instructions later in the *same*
call. The document's table — *"2 = finished, return an integer; 3+ = finished, return a float"* — is
correct about what the values *mean* and wrong to imply they persist between frames. Whether some
other writer can set them before entry is open (**BQ-5**). *Answered 2026-09-26 (FABLE, Claude Opus 5.5): none can; see the BQ-5
box.*

### What was tried and did not break anything

- **Re-derived the base and stride from the PE alone.** `ImageBase = 0x00120000`, `.data` at VA
  `0x01DF0000` / raw `0x01CCE600`, so `0x01EED720` is at file offset `0x01DCBD20` — reproducing the
  predecessor document's stated offset exactly, from an independent parse.
- **Checked every pointer slot in all five tables** (1,960 records x 4 fields = 7,840 slots):
  0 outside `.text`, 0 landing off a known function entry. A wrong base or stride cannot survive that.
- **Tried to find a second argument-reading primitive** that would explain the under-counts.
  `00267E60`, `00267FC0` and `00268100` all touch the value stack, but they are the `POPV`, `PUSHV`
  and `PUSHP` opcode bodies, not verb argument readers. None is called from a command callback.
- **Tested the shared default table's naming.** Family 2's authored names line up with it
  independently: `debug_setline` (`0x203B`) measures six float pops, and retail `setline` (`0x001C`)
  is declared as six floats. `debug_setrect` measures five. A wrong table would not produce matched
  debug/retail signatures.
- **Looked for a reader of value-stack word A (`+0x84`).** 69 writes in the interpreter, 0 reads;
  neither pop primitive touches it. Left open rather than explained away.

### Status

`DOCUMENTED`, one falsification pass survived. Extended by §11, which raises the measured coverage
from 76 rows to 1,691 — and finds two more defects in the same instrument on the way.

## 11. Falsification pass 2026-09-02 (second) — BQ-7, and the instrument was wrong twice more

**Attack chosen.** §10 proved the mapping on **76** exactly-measurable rows out of 1,960 and left
**646** with no arity evidence at all. A 98.7 % agreement rate on 4 % of the table is a small sample
defending a large claim. The obvious attack is to grow the sample: if the mapping is right, agreement
should hold as the sample grows; if it is wrong, a bigger sample should break it.

### Why 646 rows had no evidence — two filters that were far too blunt

§10 disqualified a handler from exact measurement if it had **any** backward branch or **any** call
to a function other than the six VM primitives. Both throw away sound measurements:

- **A loop elsewhere in the body does not make the argument reads ambiguous.** Only a pop or push
  *inside* a loop span does. Fix: compute the backward-branch spans and disqualify only when a VM
  primitive call site falls inside one.
- **A call to a subsystem function that cannot reach a value-stack primitive cannot change the net.**
  Fix: build the whole-binary call graph, take the reverse-reachability closure of the four stack
  primitives — **1,245 of 38,161 functions can reach one** — and disqualify only handlers that call
  into that set.

That alone took exactly-measured rows from 76 to **1,128**, at 99.3 % agreement. Eight rows
disagreed. Reading them found two more defects — **in the instrument, not in the table.**

### DEFECT 3: the count was path-insensitive

`maskopen` (`0x008A`, handler `00353D90`) is declared with one argument and measured two:

```asm
00353D96  movzx ecx, byte ptr [rdx + 0x15]
00353D9D  call  0x267310
00353DA5  test  eax, eax
00353DA7  je    0x353DD6
00353DA9  call  0x267E10        ; <-- pop, arm A
   ...
00353DD6  call  0x267E10        ; <-- pop, arm B
```

**An if/else in which both arms pop exactly once.** Summing call sites gives 2; the arity is 1. Three
more rows (`maskclose`, `sethpmenu`, `sethpmenu_436`) had the same shape, and `sethpmenu_436`'s count
was exactly doubled — 4 against a declared 2 — which is the signature.

Fix: split the body into basic blocks, give each block its net stack effect, and walk every
entry→exit path. **If all paths carry the same net, that net is the arity; if they differ, the
handler is not measurable this way** and is reported as such rather than guessed. Forty-one rows
genuinely do differ between paths and are now honestly marked, instead of silently carrying whichever
number the sum happened to produce.

### DEFECT 4: the ledger's body extent over-runs into the next function

`hidecomplete` (`0x03E6`) is declared with no arguments and measured one. Its handler:

```asm
00350320  mov  rcx, rdx
00350323  xor  edx, edx
00350325  jmp  0x26DC50          ; the function ends here - 3 instructions
0035032A  int3  x6               ; alignment padding
00350330  sub  rsp, 0x28         ; A DIFFERENT FUNCTION
00350334  mov  rcx, r9
00350337  call 0x267DB0          ; <-- the pop that was being counted
```

The ledger gives `00350320` a **56-byte** body. The real function is 11 bytes. The linear scan ran
through the `int3` padding and counted the *next* function's pop. Fix: stop decoding at the first
`int3` that follows a terminating instruction.

**This one is worth flagging beyond this document.** Any measurement that walks a function by
`entry + body_bytes` inherits the same error wherever a ledger extent covers padding, and the result
looks like ordinary code because it *is* ordinary code — just not this function's.

### SURVIVED: 1,090 of 1,091, and the rate went up as the sample grew 14×

| measure | §10 | §11 |
|---|---:|---:|
| rows exactly measured | 76 | **1,691** of 1,960 |
| named + declared, exactly measured | 76 | **1,091** |
| agreement with the authored count | 75 (98.7 %) | **1,090 (99.91 %)** |
| unexplained disagreements | 0 | **0** |

The single non-agreement is still `unkCall_5c7`, declared with two arguments and served by the shared
3-byte `ret 0` — a fact about the shipped game, not about the mapping. **The delta histogram over all
1,091 rows contains exactly two values: 0 (1,090 times) and −2 (that stub).** No shift, no drift, no
tail.

**That a fourteen-fold larger sample raised the agreement rate is the actual result.** A mapping that
was subtly wrong would have degraded; a measurement that was accidentally right on 76 rows would not
survive 1,091.

### What this delivers, beyond the check

- **600 verbs now have a measured arity the authored catalog does not carry** (581 named as
  `unkCall_*`/unknown, 19 with no name), 401 of them non-zero. `keywait` takes 1, `setmapambient`
  takes 4, `debug_setline` takes 6.
- **Operand types come with them.** The measure records *which* pop primitive each site calls, so a
  verb the catalog leaves untyped gets int-vs-float per argument: `setrotangzx` one float,
  `setmapidfloor_101` four integers, `bganimespeed` one of each.
- **An independent ceiling check.** The measured maximum arity is **8**; ff12-script's `tCallTarget`
  allocates exactly `paramType[8]` and declares exactly one 8-argument verb. Two sources that cannot
  see each other stop at the same number.

### What is honestly left

| reason a row is not exactly measured | rows |
|---|---:|
| handler calls a function that can itself reach a stack primitive | 164 |
| net stack effect **differs between paths** | 41 |
| slot has no callback at all | 33 |
| pops sit inside a loop, or the CFG exceeded the path budget | 31 |

The 41 path-dependent rows are the interesting ones: a verb whose operand count depends on a branch
is unusual, and each is a small, bounded read. **BQ-7** stays open on those four categories.

### The pattern, now four for four

Every defect found in this block was in the measuring instrument, and every one produced a
**plausible number** rather than an obvious failure: pops-without-pushes (§10), branch-insensitive
summing, a body extent that ran into the next function, and — in the neighbouring dispatch-table
document — a sweep that read past the end of a table. None was caught by looking at the number. All
four were caught by taking the handful of rows that disagreed with an independent source and
**reading the bodies**.

**The disagreements were the instrument's error report.** Had the authored catalog not existed to
disagree with, all four defects would have shipped as findings.

### Status

`DOCUMENTED`, two falsification passes survived. Extended by §12, which resolves the 41
path-dependent rows §11 left open — into two real mechanisms, not a measurement limit.

## 12. Falsification pass 2026-09-02 (third) — the path-dependent verbs are two real mechanisms

**Attack chosen.** §11 left **41 rows** whose net value-stack effect **differs between execution
paths**. A verb whose operand count depends on a branch is either a design feature the authored
catalog cannot express — an optional-argument convention — or a defect in the measurement that had
not been found yet. Both answers matter, and only reading the bodies separates them.

**Neither guess was right. They are two unrelated mechanisms, and both are real.**

### Mechanism 1 — handlers hand arguments to each other through the value stack

Seven of the 41 are one verb's handler calling **another verb's handler**, passing the arguments
through the VM operand stack rather than in registers. `setentrypos` (`0x0405`, handler `00354FB0`)
is the clearest:

```c
idx = VMValueStack_PopInt32CoerceFloat32(vs);        /* the one real argument */
if (FUN_003DFD00(0, idx, &out) != 0) {               /* look the entry up -> four floats */
    VMValueStack_PushFloat32Bits(vs, out[0]);        /* 00354FFA */
    VMValueStack_PushFloat32Bits(vs, out[1]);        /* 00355008 */
    VMValueStack_PushFloat32Bits(vs, out[2]);        /* 00355016 */
    VMValueStack_PushFloat32Bits(vs, out[3]);        /* 00355024 */
    FUN_00350510(a, owner, scratch, vs);             /* 00355035 */
}
```

**`00350510` is the `result` callback of verb `0x0019 setpos_19`, declared with four arguments.**
`setentrypos(entryIndex)` is literally *"look up that entry's position and orientation, then do
`setpos_19` with them"* — and the four values travel over the same operand stack a script would have
used. `ucsetpos` (`0x0168`, handler `0034F800`) does the same thing by tail jump: it resolves its
target and jumps into **`0034EBC0`, the handler of `0x0001 setpos` (three arguments)**, or drains
three floats and does nothing when the target does not resolve.

Once a callee's own net stack effect is folded in, both shapes measure exactly:

```
setentrypos : 1 popped − 4 pushed + 4 consumed by setpos_19 = 1      (its arity)
ucsetpos    : path A  0 + 3 consumed by setpos = 3
              path B  3 popped and discarded     = 3                 (its arity)
```

**This also closes BQ-4.** §10 flagged seven `*sync` verbs whose `begin` pushes a value and
immediately pops it back — a round trip with no visible purpose. It is the *same* hand-off with the
producer and the consumer inlined into one function and the argument a compile-time constant. All
seven measure net 0 and all seven are `CONFIRMED` against a declared 0: **genuinely zero-argument.**

Folding callees whose net is itself exactly known — a fixpoint over 1,912 candidates, of which
**1,816 resolve** — took exactly-measured rows from 1,691 to **1,836** and cut the "callee net
unknown" category from 164 to **26**.

### Mechanism 2 — the fullscreen menu bails out without reading its operands

The other 34 all have the same signature: **`sums = [0, N]`**, two paths, one reading nothing.
Thirty-three of them are family 7 — the fullscreen menu — and **thirty-two share a single predicate**:

```c
/* FUN_00280120, 20 bytes, the whole function */
bool fullscreen_menu_absent(void) {
    void *ctx = *(void **)0x0209AC30;
    return *(u64 *)(ctx + 0xC0) == 0;      /* cmp qword ptr [rcx + 0xC0], 0 ; sete al */
}
```

Every guarded handler opens with it:

```asm
00511510  push  rbx                        ; fsmenu_setslot, the shortest of them
00511516  mov   rbx, r9                    ; keep the value stack
00511519  call  0x280120                   ; is the menu object absent?
0051151E  test  eax, eax
00511520  jne   0x511536                   ; yes -> return, WITHOUT reading anything
00511522  mov   rcx, rbx
00511525  call  0x267E10                   ; no  -> read the argument and do the work
00511531  jmp   0x283620
00511536  add   rsp, 0x20                  ; the bail-out
0051153A  pop   rbx
0051153B  ret
```

**The guard is family 7's standard prologue**, on **65 of its 131 callbacks**. It only produces a
path-dependent arity on the 33 records that have operands to read; the rest read none either way.
Family 7's records come in exactly four shapes:

| begin | poll | result | records |
|---|---|---|---:|
| — | — | guarded | 20 |
| guarded | guarded | — | 22 |
| — | — | plain | 54 |
| plain | plain | — | 5 |

A guarded **durative** verb guards *both* `begin` and `poll` and has no `result` at all, so when the
menu is absent nothing in the command ever reads the stack.

**The other branch reads exactly the declared count — 25 of 25.** Every one of the 34 guarded rows
has `min(sums) == 0`, and for every one the authored catalog declares an argument count, the
**maximum** matches it:

```
7001 fsmenu_setslot     declared 1   sums [0, 1]
7004 fsmenu_paddisable  declared 2   sums [0, 2]
7007 fsmenu_showauto    declared 3   sums [0, 3]
701C fsmenu_getrectchip declared 6   sums [0, 6]
                                        ... 25 rows, 0 mismatches
```

So the arity is not path-dependent at all: **the verb takes N arguments, and there is a path on which
it takes none of them.** That is a guard, not an optional-argument convention — the answer to the
question this pass was set. The 34th row, `unkCall_3092` in family 3, has the identical shape with its
own predicate (`FUN_002E9A30`), so the pattern is not unique to the menu.

### The consequence, and how to falsify it

**On the bail-out path the operands are not consumed.** Nothing else in the sequence takes them: a
guarded durative verb has no `result` callback, and the executor's own action after `result` is to
**push** one more value — the return value, or integer `0` when there is no `result` callback at all
(`00262360`). So a fullscreen-menu verb issued while the menu object is absent leaves its N operands
on a stack that then gains one more, against a **capacity of 63** beyond which
`VMValueStack_PushInt32` silently drops values.

That is what the code does. Whether it can *happen* is a separate claim and is **not** made here — it
requires a script to issue an `fsmenu_*` verb while `*(ctx + 0xC0)` is null, and nothing read so far
says whether that is reachable. **The killer observation:** find a shipped `.ebp` script that calls a
family-7 verb outside a fullscreen-menu sequence, or find the code that guarantees it cannot. Filed
as **BQ-10**.

> **BQ-10 answered 2026-09-12 (FABLE): the shipped scripts do not produce it, and the code shows
> why they could not usefully.** Every `section_000` in `FFXII_TZA.vbf` — 1,114 `us` containers and
> 8,914 across the other eight trees, decompiled with `ff12-script -dc` — uses a family-7 verb in
> exactly **four** scripts, the same four in all nine trees: `men_z0001`, `men_z0002`, `men_z0003`
> (the gambit / licence / sample tutorials, actors `gambit_tutorial` and `sample_tutorial`) and
> `rwf_b02`. In the three tutorials the verbs sit in `main(1)` around an
> `fsmenu_openmenu(0)` … `fsmenu_closemenu()` pair, with `fsmenu_registrestore`, `fsmenu_paddisable`,
> `fsmenu_setslot`, `fsmenu_loadresource` and `fsmenu_hidecursor` issued **before** `openmenu`
> (`men_z0001` lines 24–29) and `fsmenu_confirmwinsync` in a later routine. Those are not the null
> case: **`fsmenu_openmenu` itself carries the same guard** (`00511550` → `00280120`, `*(0209AC30
> + 0xC0) == 0` → skip), and `00280140`, the only writer of that slot (`002802A0`, `00280429`, null at
> `0028044C`), is a message handler with no direct caller — so no verb creates the menu object; it
> must exist before any family-7 verb can do anything, and the tutorials — which visibly open
> panels in the shipped game — run inside a menu context that created it. The one family-7 verb in a
> non-menu script, `rwf_b02`'s `fsmenu_disposeescape()` in the `起動` routine of `ロケタイイベント`
> (no `openmenu` anywhere in the file), is in the **unguarded** half of the family (62 of 104
> handlers have no guard): its handler `00511500` tail-jumps to `00366940`, which stores 0 to the
> global `022CBE18` and never touches the menu object, so it neither dereferences the null nor
> leaves operands (it takes none). The operand-leak path — a guarded verb with operands issued while
> the slot is null — is therefore reachable only by a script that no shipped tree contains; the
> census is exhaustive over the corpus, and the 63-slot stack is never exercised by it.

### Where the numbers stand

| | §10 | §11 | §12 |
|---|---:|---:|---:|
| rows with a measured arity | 76 | 1,691 | **1,870** of 1,960 |
| named + declared, measured | 76 | 1,091 | **1,210** |
| agreement with the authored count | 75 (98.7 %) | 1,090 (99.91 %) | **1,209 (99.92 %)** |
| delta histogram | 0 and −2 | 0 and −2 | **0 and −2** |
| rows with no arity evidence | 646 | 117 | **90** |

Three passes, three samples — 76, then 1,091, then 1,210 — and the delta histogram has contained
**exactly two values every time**: `0`, and the `−2` of `unkCall_5c7`, whose handler is the shared
`ret 0`. Growing the sample sixteen-fold has not produced a single new disagreement.

**What is honestly left (BQ-9):** 33 slots with no callback, 31 whose operand reads sit inside a loop
or whose control-flow graph exceeded the path budget, and 26 whose handler calls a function whose own
stack effect is not exactly known. Ninety rows, each needing a body read, none blocked on the
instrument.

### Status

`DOCUMENTED`, three falsification passes survived, against snapshot
`46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`. What would kill it: a command
whose declared arity is reproduced by neither `begin` nor `result` under path-sensitive measurement
with callee folding; a guarded verb whose non-bail branch reads a count other than its declared one;
a reader of the `+0x10` slot; or a caller of `003DC270`/`003DC240`/`003DC2A0` that indexes with
something other than `id >> 12` and `id & 0xFFF`.

## Refinement 2026-09-08 — `CY-4`: "durative" does not mean "blocks", and that is why `*sync` exists

**`CY-4` asked whether any verb's reach contradicts its recorded shape.** It does not — but the join
that went looking found something better, and it corrects the player-facing gloss in §1 of this
document.

### The shape column means "has a `begin`", and 77 durative verbs still finish instantly

§2 defines the two shapes exactly: *instantaneous* is `result` only, *durative* is **`begin` present**.
That is a statement about slots, and it is accurate. But §1 glosses it as *"some verbs finish
instantly and some take time and hold the script until they are done"* — and **for 77 verbs that
gloss is wrong.**

| slots present | verbs | what the dispatcher does |
|---|---:|---|
| `result` only — *instantaneous* | 1,571 | completes in one call |
| `begin` + `poll` (± `result`) — *durative* | **250** | **genuinely holds the script** |
| **`begin`, no `poll`** — also labelled *durative* | **77** | **completes in one call** |
| `poll` only — *empty* | 29 | holds the script, started by someone else |

**The 77 complete immediately because of the rule established in
[`../Native-Command-Lifecycle/native-command-lifecycle.md`](../Native-Command-Lifecycle/native-command-lifecycle.md)
§14: a null `poll` substitutes a zeroed local, and zero means finished.** A verb with a `begin` and
no `poll` runs its begin, is asked "still running?", the dispatcher answers "no" on its behalf, and
the command is done in the same call.

### Which is exactly why the game has `*sync` verbs

| verb | shape | `begin` | `poll` | behaviour |
|---|---|---|---|---|
| `rmove` `0x0042` | durative | `003488B0` | **—** | **starts a move, returns at once** |
| `movesync` `0x003D` | empty | — | `00356A90` | **waits for it** |
| `rturn` `0x0047` | durative | `0034B670` | **—** | starts a turn, returns at once |
| `turnsync` `0x0046` | empty | — | `00341D50` | waits for it |
| `wait` `0x0000` | durative | `0034CF90` | `0034DCC0` | genuinely blocks |
| `camerasync` `0x0079` | durative | `0034C290` | `0034C570` | genuinely blocks |

> **Movement and turning verbs do not block.** `rmove` puts a walk in motion and hands control
> straight back to the script; the waiting is a *separate verb*. That is why every move in an FFXII
> cutscene is followed by a `movesync`, and it is not an authoring convention — **the move verb
> physically cannot wait, because it has no `poll` slot for the dispatcher to ask.**
>
> [`../verbs-that-only-wait-and-verbs-that-do-nothing.md`](../verbs-that-only-wait-and-verbs-that-do-nothing.md)
> established that a `*sync` verb waits for *"something started by an earlier verb"*. **The earlier
> verb is now identified as a class: the 77 with a `begin` and no `poll`.** ~~Both halves of the idiom
> are accounted for.~~
>
> *Corrected 2026-09-26 (FABLE, Claude Opus 5.5) (`CZ-2`): the 77 are one kind of starter, not the only one, and the pairing is
> not one-to-one.* Control: [`cz2_start_waiter_pairing.py`](../../_index/candidates/cz2-start-waiter-pairing/cz2_start_waiter_pairing.py) (6 checks, FAILS 0).
> - **Many-to-one.** 37 of the 77 share their `begin` with a blocking twin: 8 whose poll is `turnsync`'s, 10
>   `movesync`'s, and 19 `lookatsync`'s. `turnsync` and `movesync` read the steering bytes `+0x28` and `+0x29`.
>   Every turn start reaches the `+0x28` writer and every move start reaches the `+0x29` writer.
> - **Other pairings.** The music fades pair with `musicfadeoutsync` through a slot word.
> - **Instantaneous verbs start work too.** In every shipped script, all 45,691 calls of `vibsync` follow
>   `vibplay`, an instantaneous verb. So a waiter is not always paired with one of the 77.
> - **Unused and inert.** 28 of the 77 are called by no shipped script in any language, `rturn` among them. The
>   two `atrac3` waiters' polls are the constant `return 0` stub, so they can never report busy.

**So the scripting language has three behaviours, not two** — finish, **start-and-return**, and block
— and only the first and third are visible in the `shape` column as it is named.

### The two genuine oddities

**Two verbs are labelled `instantaneous` and carry a `poll`**: `usemoviememory` (`0x0297`,
poll `003473C0`) and `debug_freeiopvoice` (`0x20B5`, poll `0050EA00`). Under the dispatcher a `poll`
without a `begin` is reached on the first call like any other, so **these two can block despite the
label.** Neither handler is read. `CZ-1`.

> *Answered 2026-09-14 (FABLE, `CZ-1`): both are **wait-then-act** verbs, and the label is wrong for both.* Under the
> dispatcher a poll with bit 0 set keeps the command running ([the native command lifecycle](../Native-Command-Lifecycle/native-command-lifecycle.md)).
> - **`usemoviememory`** — poll `003473C0` returns `0037B380() != 4`, where `0037B380` reads byte `02ADD932`. That byte is
>   set to 4 by `0037B3D0` after it replaces arena 11's backing store (the 3.75 or 4 MiB choice on
>   [where the game's memory comes from](../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md)),
>   and by `0037B390` from the boot fixer `0022A0B0`; `0037B490` is its plain setter. So the verb **holds the script until
>   the movie memory switch has completed**, then runs its result `003477E0` (`002640C0` → `003DDC20(…, 1)`).
> - **`debug_freeiopvoice`** — poll `0050EA00` returns `0036F000() == 0`. `0036F000` returns 0 while any entry of the two
>   `0x18`-stride state tables `022D9AB0` and `022D9AE0` is in state 1 or 2, and 1 when all are idle (`0036F010`–`0036F04A`;
>   the same test as on [the resource request queue](../../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md)).
>   So it **holds until those tables are idle**, then runs its result `0050EA60`.
>
> Neither is a new shape; each is "poll first, act once ready" with no `begin`. The shape vocabulary's `instantaneous` label
> is a catalogue error for these two rows.

### `CY-1`: why the reach map is silent, split four ways

[`what-each-script-verb-touches.md`](what-each-script-verb-touches.md) could not label 1,344 verbs.
That silence has four different causes, and they are not the same problem:

| cause | verbs |
|---|---:|
| labelled | 616 |
| **every tagged callee is bridge-owned** | **1,029** |
| handler calls nothing — the body is inline | 218 |
| every callee is untagged | 93 |
| no handler at all | 4 |

> **The dominant cause is not a tagging gap.** 1,029 handlers call only bridge plumbing — the value
> stack, the scratch block, the coercion helpers — and do their real work in their own instructions.
> **Only 93 verbs are silent because the ledger has not named their callees**, which is the one
> category a naming pass would fix.
>
> So *"read the handler"* is not a fallback for these 1,029; it is the only route. **The reach map
> cannot be extended to them by any amount of graph work.**

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Input and Presentation — SERVICE.** The boot initialiser `0022A0B0` calls the 119-byte Input-filed initialiser and the
Presentation loaders `AddMotion_LoadHighModelReplace` / `AddMotion_LoadSkeletonMapping`. Those are siblings in the boot
sequence, not verb dispatch.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**RNG_Random_Selection — SERVICE.** `0022A0B0` on this page calls `RNG_MT19937_Seed`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00863D30` - onto the CRT's Mersenne Twister seed; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — CLIENT (SWE2-EC7 2026-09-19, 2 edges).** `003A1C50`, a callee this page's `00377AB0` section cites,
is also called by two Audio-filed bodies (`00361810`, `00362850`). The audio callers are mechanical users of a
shared helper.

**CombatAction — CLIENT (SWE2-EC7 2026-09-19, 2 edges).** `0026B0C0` and `0026B620`, callees this page's
`00350510` section cites, are also called by the CombatAction-filed `00307300`. The combat-action caller is a
mechanical user of the same shared helpers.

**ActorEntity — SERVICE both ways (SWE2-EC7 batch-148).** The `00267E60` entry's caller `0025E4C0` is
`WorldActorScriptVM_InterpretBytecode` - the actor-side interpreter itself, so its ActorEntity callees
(`00268EA0`, `003587C0`, `00358940`, `003DB2A0`/`003DB420`/`003DB550`/`003DB640`/`003DB6E0`/`003DBDC0`/
`003DBF60`) are the dispatch's own actor traffic, and the entry's `0032F240` notify is ActorEntity-owned and
reached the other way from `0026C8C0`. The crossing is the interpreter serving actor scripts; no actor state
is owned here.

## SWE2-EC7-45 update (2026-09-19) - `003538F0`

`003538F0` (236 B) is a body - `002640C0`/`002650B0`/`00267E10`/`00377AB0`/`00808C40`. Interior anchor `00353915` (a `002640C0` call).

## SWE2-EC7-58 update (2026-09-19) - `00377AB0`

`00377AB0` (170 B) is the fills-four-floats verb helper - `00264B50`/`003A1C50` plus `0209A670`/`0209A678`/`02ADD0D8`. Interior anchor `00377AE5` (a `00264B50` call).


## SWE2-EC7-58 update (2026-09-19) - `00354FB0`

`00354FB0` (167 B) is the `setentrypos` verb handler the dispatch page names - `00267E10`/`00267F60`/`00350510`/`003DFD00`/`00808C40` plus `01F44830`. Interior anchor `00354FDA` (a `00267E10` call).

## SWE2-EC7-61 update (2026-09-19) - `00350510`

`00350510` (152 B) is a verb-dispatch body - `00267DB0`/`0026AF80`/`0026B0C0`/`0026B620`. Interior anchor `00350533` (a `00267DB0` call).


## SWE2-EC7-98 update (2026-09-20) - `002E1C70` measured

`002E1C70` (33 B) is the flag-word toggle `002628B0` and the
ten `00353xxx`/`00355xxx`/`00356xxx` verbs call: `ecx != 0`
sets bit `edx` of `word[0215F1B4]` (`bts`), `ecx == 0` clears
it (`btr`) - the 16-bit global flag bank the verb layer
drives.
Interior anchor `002E1C7B` (the `bts` arm).

`00267E60` (256 B) is the typed value-pop the interpreter `0025E4C0` runs through `00262440`: the popped block's `+0x34` kind selects the arm - kind 2 decrements `[rbx]`'s count and converts the `+0x184`-indexed element by its `+4`-byte tag (raw dword for tag 2, `cvtdq2ps` for tag 3), kind 1 pops it as a raw value or `cvttss2si`-truncates tag-2 floats; `008620C0` raises on empty pops, `0032F240` fires when `[rdi+0x28]-1 <= 2` with a zero `00262440` result, and `0026D530` releases the block

Interior anchor `00267E9C` (function `00267E60`).
