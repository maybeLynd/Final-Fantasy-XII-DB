# BF-1 — what every ScriptVM opcode does

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Control: `bf1_opcodes.py` (11 checks, FAILS 0) for the handlers read here. Rows citing another page rest on that page's
own reading and control.

**How the table was built.** The interpreter `WorldActorScriptVM_InterpretBytecode` (`0025E4C0`) dispatches 100 opcodes
through the RVA table `00261DF8`. Opcode N's mnemonic is record N−1's `+8` pointer in the descriptor table `01EFEA60`
(the interpreter page §11). The instruction length is record N's `+0`. Every handler was read, here or on the cited
page. Every one returns through the common tail, which advances the pc by the length.

**The machine.**
- **Value stack.** An int/float stack at `02099AC0`: at most `0x3F` entries, a type byte per entry (1 int, 2 float),
  values at `+0x184 + 4i`.
- **Truncation.** Integer operators truncate float operands (`cvttss2si`).
- **Other entry types.** They reach the retail no-op error stub `008620C0` and read as 0.
- **Per-thread registers.** A, X and Y live in the execution context, the interpreter's third argument: `+0x10`, `+8`
  and `+0xC`.
- **Per-actor registers.** I0–I3 and F0–F3 live in the actor record (§13 of the interpreter page).
- **Constants.** The slot's int and float constant pools are at `+0x68` and `+0x70`.

**What the census shows:**
- **Inert.** Six opcodes share the invalid-opcode target. `DVAR` hands its value to a `ret 0` stub. `SYSTEM`, `PREQ*`
  and `PREQWAIT` only pop their operands. The retail interpreter carries twelve opcodes with no effect beyond stack
  traffic.
- **A crash.** `OPMOD` divides with no zero test, so a script `MOD 0` faults. `OPDIV` is guarded on both paths.
- **Connections to other rows.**
  - `REQCHG` (`0x34`) is the script route into the per-actor resource-override array FI-1 named, through `0025AF60`.
  - `INCINITTAG` (`0x62`) marks a target's channel as requested without filing a request.

| op | mnemonic | len | handler | what it does | source |
|---|---|---:|---|---|---|
| `0x00` | `NOP` | 0 | `0025E613` | advance the pc by the instruction length; nothing else (the common tail every handler returns through) | here (K1) |
| `0x01` | `LABEL` | 0 | `0025E60A` | inert: shares the invalid-opcode target 0025E60A (marks the tick finished and advances) | interpreter page §4 |
| `0x02` | `TAG` | 0 | `0025E60A` | inert, as 0x01 | interpreter page §4 |
| `0x03` | `SYSHALT` | 1 | `0025E5EA` | halt: set actor +0x14 bit 6 and rewind the pc, so the instruction repeats every tick | here (K3) |
| `0x04` | `SYSTEM` | 1 | `0025E649` | pop one value and discard it | here (K3) |
| `0x05` | `OPLOR` | 1 | `0025E664` | logical OR: pop b, pop a (int, floats truncated), push (a != 0 or b != 0) | here |
| `0x06` | `OPLAND` | 1 | `0025E6D8` | logical AND: push (a != 0 and b != 0) | here |
| `0x07` | `OPOR` | 1 | `0025E7E7` | bitwise OR: push a | b | here |
| `0x08` | `OPEOR` | 1 | `0025E8A2` | bitwise XOR: push a ^ b | here |
| `0x09` | `OPAND` | 1 | `0025E95D` | bitwise AND: push a & b | here |
| `0x0A` | `OPEQ` | 1 | `0025EA18` | compare equal through 0025D740, push 0/1 | interpreter page §4 (the 0x0A-0x0F family) |
| `0x0B` | `OPNE` | 1 | `0025EA30` | compare not-equal, push 0/1 | interpreter page §4 |
| `0x0C` | `OPGT` | 1 | `0025EA48` | compare greater, push 0/1 | interpreter page §4 |
| `0x0D` | `OPLS` | 1 | `0025EA60` | compare less, push 0/1 | interpreter page §4 |
| `0x0E` | `OPGTE` | 1 | `0025EA78` | compare greater-or-equal, push 0/1 | interpreter page §4 |
| `0x0F` | `OPLSE` | 1 | `0025EA90` | compare less-or-equal, push 0/1 | interpreter page §4 |
| `0x10` | `OPSLL` | 1 | `0025EAA8` | shift left: push a << b | here |
| `0x11` | `OPSRL` | 1 | `0025EB86` | arithmetic shift right: push a >> b (sar) | here |
| `0x12` | `OPADD` | 1 | `0025EC64` | add: int + int as int, otherwise float (addss) | here |
| `0x13` | `OPSUB` | 1 | `0025EE79` | subtract: int or float path (00267560 selects) | here |
| `0x14` | `OPMUL` | 1 | `0025EF92` | multiply: int or float path | here |
| `0x15` | `OPDIV` | 1 | `0025F0AC` | divide: int (idiv) or float (divss); a zero divisor is tested on both paths and yields 0 | here (K9) |
| `0x16` | `OPMOD` | 1 | `0025F1D6` | remainder: int idiv only, with NO zero test - MOD 0 faults | here (K9) |
| `0x17` | `OPNOT` | 1 | `0025F232` | logical NOT: push (a == 0) | here |
| `0x18` | `OPBNOT` | 1 | `0025F2B8` | bitwise NOT: push ~a | here |
| `0x19` | `OPUMINUS` | 1 | `0025E60A` | inert (shares 0025E60A) - unary minus is not implemented | interpreter page §4 |
| `0x1A` | `OPFIXADRS` | 1 | `0025E60A` | inert (shares 0025E60A) | interpreter page §4 |
| `0x1B` | `PUSHA` | 1 | `0025F322` | push register A (context +0x10) | here (K5) |
| `0x1C` | `POPA` | 1 | `0025F32A` | pop into register A | here (K5) |
| `0x1D` | `PUSHX` | 1 | `0025F39D` | push register X (context +8) | here (K5) |
| `0x1E` | `PUSHY` | 1 | `0025F3A5` | push register Y (context +0xC) | here (K5) |
| `0x1F` | `POPX` | 1 | `0025F3AD` | pop into register X | here (K5) |
| `0x20` | `POPY` | 1 | `0025F420` | pop into register Y | here (K5) |
| `0x21` | `REQ` | 1 | `0025F493` | request: pop (channel, function id, actor) and file a kind-0, mode-1 request | scheduling page §2.4 |
| `0x22` | `FREQ` | 1 | `0025F7F2` | request, kind 2 (F), mode 1 | scheduling page §2.4 |
| `0x23` | `TREQ` | 1 | `0025FBC9` | request, kind 4 (T), mode 1 | scheduling page §2.4 |
| `0x24` | `REQSW` | 1 | `0025FFA0` | request kind 0, mode 2 (start-wait: the requester parks as wait kind 4 until the target starts) | scheduling page §2.4 |
| `0x25` | `FREQSW` | 1 | `00260300` | request kind 2, mode 2 | scheduling page §2.4 |
| `0x26` | `TREQSW` | 1 | `002606C3` | request kind 4, mode 2 | scheduling page §2.4 |
| `0x27` | `REQEW` | 1 | `00260A86` | request kind 0, mode 3 (end-wait: parks until the target's function returns) | scheduling page §2.4 |
| `0x28` | `FREQEW` | 1 | `00260DBE` | request kind 2, mode 3 | scheduling page §2.4 |
| `0x29` | `TREQEW` | 1 | `002610B5` | request kind 4, mode 3 | scheduling page §2.4 |
| `0x2A` | `PREQ` | 1 | `0026121A` | pop three values; no request is filed | here (K4) |
| `0x2B` | `PREQSW` | 1 | `0026121A` | as 0x2A (shared handler) | here (K4) |
| `0x2C` | `PREQEW` | 1 | `0026121A` | as 0x2A (shared handler) | here (K4) |
| `0x2D` | `RET` | 1 | `00261239` | return: retire the active entry, select the next pending one, and resume the caller's wait slot (or service the wait state when none is outstanding) | here; the request page |
| `0x2E` | `RETN` | 1 | `0026131C` | return N: pop a depth and recycle the entry range above it, then resume as RET | here |
| `0x2F` | `RETT` | 1 | `002613DD` | return and transfer: as RET, and start the next entry's script (003DBDC0) | here |
| `0x30` | `RETTN` | 1 | `0026147B` | return N and transfer | here |
| `0x31` | `DRET` | 1 | `0025E60A` | inert (shares 0025E60A) | interpreter page §4 |
| `0x32` | `REQWAIT` | 1 | `00261539` | wait for a request: pop (function id, actor); if that actor has the entry active, park as wait kind 3 on it | here (K8) |
| `0x33` | `PREQWAIT` | 1 | `002615A6` | pop two values; no wait is armed | here (K4) |
| `0x34` | `REQCHG` | 1 | `002615BA` | set an actor's resource-override slot: pop (value, actor, slot) into 0025AF60; slots 0x10-0x11 re-arm the EH-5 countdown when the target's +0x0B bit 3 is set | here (K8); FI-1 record |
| `0x35` | `REQCANCEL` | 1 | `00261301` | cancel: pop an index and recycle the entry range above it (003DB420) | here (K8) |
| `0x36` | `POPI0` | 1 | `0026161C` | pop into per-actor int register I0 (record +0x64) | interpreter page §13 |
| `0x37` | `POPI1` | 1 | `0026162D` | pop into I1 | interpreter page §13 |
| `0x38` | `POPI2` | 1 | `0026163E` | pop into I2 | interpreter page §13 |
| `0x39` | `POPI3` | 1 | `0026164F` | pop into I3 | interpreter page §13 |
| `0x3A` | `POPF0` | 1 | `00261660` | pop into float register F0 | interpreter page §13 |
| `0x3B` | `POPF1` | 1 | `00261673` | pop into F1 | interpreter page §13 |
| `0x3C` | `POPF2` | 1 | `00261686` | pop into F2 | interpreter page §13 |
| `0x3D` | `POPF3` | 1 | `00261699` | pop into F3 | interpreter page §13 |
| `0x3E` | `PUSHI0` | 1 | `002616AF` | push I0 | interpreter page §13 |
| `0x3F` | `PUSHI1` | 1 | `002616C0` | push I1 | interpreter page §13 |
| `0x40` | `PUSHI2` | 1 | `002616D1` | push I2 | interpreter page §13 |
| `0x41` | `PUSHI3` | 1 | `002616E2` | push I3 | interpreter page §13 |
| `0x42` | `PUSHF0` | 1 | `002616F3` | push F0 | interpreter page §13 |
| `0x43` | `PUSHF1` | 1 | `00261706` | push F1 | interpreter page §13 |
| `0x44` | `PUSHF2` | 1 | `00261719` | push F2 | interpreter page §13 |
| `0x45` | `PUSHF3` | 1 | `0026172C` | push F3 | interpreter page §13 |
| `0x46` | `DVAR` | 1 | `00261742` | pop one value and hand it to the ret-0 stub 0016D6A0 - inert | here (K10); script-variables page |
| `0x47` | `LONGCODESTART` | 1 | `0025E60A` | inert (shares 0025E60A) | interpreter page §4 |
| `0x48` | `PUSHV` | 3 | `00261761` | push a variable (resolved by descriptor; width and int/float from the descriptor) | script-variables page |
| `0x49` | `POPV` | 3 | `00261778` | pop into a variable, coerced to its kind | script-variables page |
| `0x4A` | `PUSHDBG` | 3 | `0026178F` | resolve a variable for the debug print path | script-variables page |
| `0x4B` | `PUSHP` | 3 | `002617B2` | push a variable reference (how an array element is passed) | script-variables page |
| `0x4C` | `PUSHTAG` | 3 | `002617C9` | push the tag value of the operand's entry in the bound definition's table (0x8000 when out of range) | here |
| `0x4D` | `PUSHACT` | 3 | `00261806` | push the packed actor handle of the operand's actor index ((word << 16) | index | bit 14; 0x8000 when out of range) | here |
| `0x4E` | `PUSHI` | 3 | `00261855` | push the int constant the operand indexes in the slot's pool (+0x68) | here (K7) |
| `0x4F` | `PUSHII` | 3 | `0026186D` | push the operand itself, sign-extended | here (K7) |
| `0x50` | `PUSHF` | 3 | `0026187D` | push the float constant the operand indexes in the slot's pool (+0x70) | here (K7) |
| `0x51` | `JMP` | 3 | `002618A8` | jump to bytecode base + the script's jump table[operand] | here (K6) |
| `0x52` | `POPCMPYEQJMP` | 3 | `00261897` | pop v; jump if v == Y | here (K6) |
| `0x53` | `POPCMPYLOWJMP` | 3 | `002618DD` | pop v; jump if v > Y | here (K6) |
| `0x54` | `POPCMPYLOWEQJMP` | 3 | `002618F0` | pop v; jump if v >= Y | here (K6) |
| `0x55` | `POPCMPYHIGHJMP` | 3 | `00261903` | pop v; jump if v < Y | here (K6) |
| `0x56` | `POPCMPYHIGHEQJMP` | 3 | `00261916` | pop v; jump if v <= Y | here (K6) |
| `0x57` | `POP2CMPYBTWNJMP` | 3 | `0026192C` | pop two bounds, order them, jump if Y lies between them | interpreter page (handler read, 2026-09) |
| `0x58` | `CALL` | 3 | `0026199D` | call native verb [operand] with X = the actor's own index; if the verb yields, rewind and save the pc so the call repeats next tick | here; verb-dispatch page §2 |
| `0x59` | `CALLACT` | 3 | `002619EF` | as CALL, but first pop the target actor into X (skipped while the context is resuming, +0x15) | here; verb-dispatch page §2 |
| `0x5A` | `POPXJMP` | 3 | `00261A52` | pop into X, then jump | here |
| `0x5B` | `POPXCJMP` | 3 | `00261A91` | pop into X; jump if non-zero | here |
| `0x5C` | `POPXNCJMP` | 3 | `00261AA6` | pop into X; jump if zero (the for-loop idiom) | here |
| `0x5D` | `CALLPOPA` | 3 | `00261ABB` | as CALL, and when the verb completes pop its result into register A | here |
| `0x5E` | `CALLACTPOPA` | 3 | `00261AFE` | as CALLACT, and when the verb completes pop its result into register A | here |
| `0x5F` | `REQALL` | 3 | `00261B15` | request on a whole actor list (waits while any listed actor still has the channel active) | bytecode page §5 |
| `0x60` | `JMPINTERNAL` | 3 | `002618A8` | jump - JMP's own handler | here (K6) |
| `0x61` | `REQWAITALL` | 3 | `00261CCD` | wait on a whole actor list (wait kind 5) | bytecode page §5 |
| `0x62` | `INCINITTAG` | 3 | `00261D36` | peek three values (pop and push back) and mark the target's channel as requested (002659F0: +0x24 bit, +0x10 count) without filing a request | here; script-variables page (002659F0) |
| `0x63` | `REQIALL` | 3 | `00261C12` | REQALL with the immediate-mark flag | bytecode page §5 |
