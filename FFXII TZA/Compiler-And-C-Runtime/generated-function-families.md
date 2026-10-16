---
title: "Generated function families: the small compiler- and template-generated bodies, their instruction forms and member lists"
kind: "reference"
category: "Compiler and C runtime"
addresses: "0016D6A0, 00584730, 00210EC0, 00808B90, 00861EC0, 007DF6D0, 003844F0, 00633390, 005A2B80, 005BEC00, 006B2950, 006B2970, 005A4830, 0030DCB0, 003008A0, 005CDAA0"
---

## What it lists

A family is a set of functions whose bodies are the same instruction sequence. Decoding each
member from its entry over its body and dropping every immediate, displacement, call or jump
target and rip-relative address leaves one sequence of mnemonics and registers, the family's
form; the members differ only in the dropped values.

Many forms are the compiler's idioms, written out once per class or per declaration: deleting
destructors, static initialisers registered with `atexit`, vtable installs and argument-forwarding
tail calls. Knowing a family tells you what every
member does without reading each one; it does not tell you what the values a member passes or
the functions it calls mean.

The page covers 171 families, one row each in [the data file](generated-function-families.tsv),
with 2,444 listed functions. Every listed member of every family decodes to its family's
form; nine leaf families have two to five spellings of it (with or without an offset, or at
different operand widths). For each family the image was also searched for every function with that form that calls
every target the listed members share:

| Result | Families |
|---|---|
| the search returns exactly the member list | 84 |
| the image holds more functions of that form than the list | 87 |

The member count is given for the first group only. For the second, the list names part of the
functions with that body.

Three pairs of lists share one form and are told apart by a value the form drops:

- the vtable-installing deleting destructors, by whether the destructor they call is `00633390`;
- the virtual tail calls and the fixed-slot adapters (`mov rax, [rcx]; jmp [rax+slot]`);
- the field clears and the constant field stores, by whether the stored constant is 0.

### The shared functions the families call

Many families call the same few runtime functions:

| Function | Body | Called by |
|---|---|---|
| `0016D6A0` | `ret 0` | the guarded static teardowns, the bit-2 arm of the deleting destructors (so that arm frees nothing), the global handle reads, the three-float record adapters |
| `00584730` | `if (p) jmp 0019C570`, and `0019C570` is `jmp [008C2B70]`, the `_aligned_free` import | the deleting destructors, the owned-buffer resets, the static object fixups |
| `00210EC0` | `or r8d, -1; xor edx, edx; jmp 0085E730`, and `0085E730` is `jmp [008C2B40]`, `malloc` | the lazy singleton allocators |
| `00808B90` | `atexit`: calls `_onexit` (`00808B40`) and returns 0 or -1 | the static initialisers, as their tail jump |
| `00861EC0` | `jmp [008C2A60]`, `memset` | the zero-init initialisers, the zeroing out-record initialisers |
| `007DF6D0` | `InitializeCriticalSection(this)` (IAT `008C20B0`), then zeroes `+28`<sub>h</sub> to `+4B`<sub>h</sub> and returns `this` | the zero-init initialisers |
| `003844F0` | `jmp 003697F0`, which returns for null and otherwise jumps to `00369860(p, 0)` | the static handle replacements |

### Reflection descriptor slots

The return-value adapters are 26 bytes each. `005A2B80` is typical:

```asm
005A2B80  push rbx
005A2B82  sub  rsp, 0x20
005A2B86  mov  rcx, rdx          ; the second argument becomes the first
005A2B89  mov  rbx, r8           ; the third is an out pointer
005A2B8C  call 005BEC00          ; the only part that differs between members
005A2B91  mov  [rbx], rax        ; store the returned pointer
005A2B94  add  rsp, 0x20
005A2B98  pop  rbx
005A2B99  ret
```

The image holds 403 functions with this body, each calling a different target. Their addresses
appear 1,185 times as qwords in `.rdata`. Walking back from each to the start of its vtable (the
first slot whose preceding qword points at a valid RTTI complete-object locator) puts every one
of the 1,185 at slot 5 of a PhyreEngine class-descriptor vtable:

| Descriptor template | Slot-5 appearances |
|---|---|
| `PClassDescriptorForType<T>` | 409 |
| `PClassDescriptorAbstract<T>` | 386 |
| `PClassDescriptorConcrete<T>` | 331 |
| `PClassDescriptorWithoutDefaultConstructor<T>` | 38 |
| `PClassDescriptorWrapper<T>` | 15 |
| `PClassDescriptorHeader<T>`, `…HeaderWithoutDefaultConstructor<T>` | 3, 1 |
| `PClassDescriptorForClassDescriptor`, `PClassDescriptorBase` | 1, 1 |

There is one `ForType` descriptor per class, so the adapters serve 409 classes. 367 adapters
appear three times, 34 twice, `006B2950` six times and `006B2970` ten times. Those two are the
only adapters shared between classes: `006B2950` serves `Matrix3`, `Matrix4` and `PMatrix4`, and
`006B2970` serves `Point3`, `Quat`, `Vector2`, `Vector3` and `Vector4`.

The other 401 targets each load the name of one script pointer accessor,
`Phyre::PScripting::PScriptAccessors::PObjectAccessor<T *>::Get`, beside their error messages;
none loads a reference accessor's (`T &`) name.

`005BEC00`, the target above, starts with
`00682980`, which looks up `PhyreObject` in the Lua registry (pseudo-index `-1001000`) and returns
non-null only when the comparison `00810810` succeeds, and it names
`PObjectAccessor<class Phyre::PAnimation::PTimeScaleOffsetController *>::Get`. So slot 5 of a
class descriptor converts a script value into a pointer to an object of that class, and the
adapter gives every class the same `(descriptor, value, T **out)` call. The shared targets of
`006B2950` and `006B2970` (`00683B10`, `00683BF0`) load no accessor name.

The owned-buffer reset adapters (`005A4830`, 59 bytes) are slot 11 of the same descriptors: their
46 bodies appear 138 times, all at slot 11, once each in the `ForType`, `Abstract` and `Concrete`
descriptor of one class. The instance they reset is a count word, whose bit 31 when set keeps the
buffer from being freed, and a data pointer at `+8`.

### The serial-range loops

The seven `Runtime.SerialRangeInvokeLoop` members each walk one class of ids. `0030DCB0` sets
`ebx` to `1000`<sub>h</sub> and, while `ebx` is below `1000h + [01EEBD54]`, calls
`003008A0(bx, 63h, 0, 1, 0)` (`0030DCD0` to `0030DCE4`). The other six use bases `2000`<sub>h</sub>,
`3000`<sub>h</sub>, `C000`<sub>h</sub>, `8000`<sub>h</sub>, `4000`<sub>h</sub> and `6000`<sub>h</sub> with the counts at `01EEBDAC`, `01EEBE04`,
`01EEC11C`, `01EEBFBC`, `01EEBE5C` and `01EEBF0C`.

`003008A0` is the entry that changes what the
party owns ([item and ability ids](../Engine-Core/item-and-ability-ids.md)): each call
adds 99 of one id on channel 1, so each member adds 99 of every id of its class.

### Lists beside the families

These member files beside the page are not single-form families:

- `generated-function-families-trivial-global-accessors.tsv`: functions whose whole body is one instruction with one rip-relative operand and `ret`: `lea`, loads and stores of 1, 2, 4 or 8 bytes, and constant stores. The image has 570
  such functions; the list names part of them.
- `generated-function-families-documented-global-leaf-accessors.tsv`: a list of small bodies, each row naming a target global.
- `generated-function-families-explained-callee-adapters.tsv`: a list of small adapters, each row naming the function it forwards to.
- `generated-function-families-generated-families-installed-classes.tsv`: for the vtable-installing families, the class whose vtable each member installs. Each
  of its 120 rows names the class of the first rip-relative address in the member's body that is
  preceded by a valid RTTI locator.
- `generated-function-families-generated-families-shared-implementations.tsv`: for each family, the functions every member calls.
  The 15 rows for families on this page each name a function every member of that family calls;
  the other 8 rows are for the Lua and PhyreEngine reflection families on other pages.

## Columns

| Column | Meaning |
|---|---|
| `family` | the family's name |
| `shape` | what every member's body does, in instruction terms |
| `members` | the number of members, given when the image search returns exactly the member list; empty otherwise |
| `example` | one member's entry address (the lowest) |
| `member_list` | the file beside this page that lists every member |

## Data

### Leaf getters, stores and predicates

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeLeaf.ConstantDwordReturn` |  | `0017E410` | `mov eax, imm32; ret`: returns a constant. |
| `NativeLeaf.DoubleCallBool` |  | `0017E4E0` | Calls one function, calls a second on its result, returns the second result's low byte zero-extended. |
| `NativeLeaf.DoubleDerefFlagExtract` | 6 | `001E4AE0` | `rax = [rcx+off]`; returns one bit of the dword at `[[rax]+off2]` (`shr`, `and 1`). |
| `NativeLeaf.FieldByteGetter` |  | `00187530` | `movzx eax, byte [rcx+off]; ret` (or `[rcx]`). |
| `NativeLeaf.FieldByteStore` |  | `001863E0` | `mov byte [rcx+off], dl; ret` (or `[rcx]`). |
| `NativeLeaf.FieldClear` |  | `00189C10` | `mov [rcx+off], 0; ret`, byte to qword width. Same instruction form as the constant stores, with the constant 0. |
| `NativeLeaf.FieldConstStore` |  | `00193930` | `mov [rcx+off], imm; ret` with a non-zero constant, byte to qword width. |
| `NativeLeaf.FieldDwordGetter` |  | `00186980` | `mov eax, [rcx+off]; ret` (or `[rcx]`). |
| `NativeLeaf.FieldDwordStore` |  | `001B1FA0` | `mov [rcx+off], edx; ret`. |
| `NativeLeaf.FieldFlagMaskClear` | 6 | `00313F70` | `and [rcx+off], mask; ret`: clears flag bits of a byte or dword field. |
| `NativeLeaf.FieldFloatGetter` |  | `001867D0` | `movss xmm0, [rcx+off]; ret`. |
| `NativeLeaf.FieldFloatStore` |  | `00194300` | `movss [rcx+off], xmm1; ret`. |
| `NativeLeaf.FieldQwordGetter` |  | `00186660` | `mov rax, [rcx+off]; ret` (or `[rcx]`). |
| `NativeLeaf.FieldQwordStore` |  | `001B22D0` | `mov [rcx+off], rdx; ret` (or `[rcx]`). |
| `NativeLeaf.FlagBit1SetClear` | 4 | `0018B070` | When the byte argument `dl` is non-zero, sets bit `2`<sub>h</sub> of the dword at `this+20h`; otherwise clears it. |
| `NativeLeaf.FlagBit2SetClear` | 4 | `0026A320` | Clears one bit of a byte field, then sets it again when `edx` is non-zero (`setne`, `shl`, `or`). |
| `NativeLeaf.GlobalHandleStateRead` |  | `001B5FB0` | Calls `0016D6A0` with `ecx` = (pointer global non-zero), then returns a second global. |
| `NativeLeaf.GlobalQwordStore` |  | `00378B80` | `mov eax, ecx; mov [global], rax; ret`: stores the zero-extended argument into a qword global. |
| `NativeLeaf.MemberAddressAccessor` |  | `001B0FA0` | `lea rax, [rcx+off]; ret`: returns the address of a member. |
| `NativeLeaf.NoOpReturnStub` |  | `006DA8C0` | `ret 0`: returns at once. |
| `NativeLeaf.NullableDerefWordAdd` | 4 | `003E6CF0` | `rdx = [rcx+off]`; when it and its word at `+10`<sub>h</sub> are non-zero returns that word plus the low 32 bits of `rdx`, sign-extended; otherwise 0. |
| `NativeLeaf.PairedStaticConstStore` | 10 | `0017F270` | Two `mov [global], imm` stores into two globals, then `ret`; byte to dword width. |
| `NativeLeaf.PayloadBaseBitExtract` |  | `00314A80` | Calls `002EF2B0` and returns one bit of a byte at a fixed offset in the returned block. |
| `NativeLeaf.PayloadBaseFlagSet` | 4 | `00314BB0` | Calls `002EF2B0`, clears one bit of a byte in the returned block, and sets it again when the argument is non-zero. |
| `NativeLeaf.StaticGlobalFloatSetter` |  | `002B6670` | `movss [global], xmm0; ret`: stores the float argument into a global. |
| `NativeLeaf.StaticPointerBitfieldGetter` |  | `00236780` | Loads a pointer global and returns one bit of a dword field of its object (`shr`, `and 1`). |
| `NativeLeaf.StaticPointerNestedFieldGetter` |  | `0027E9D0` | Loads a pointer global and returns the qword at a fixed offset in what it points to. |
| `NativeLeaf.StaticPointerNonNullPredicate` |  | `00228480` | Returns 1 when a pointer global is non-zero (`cmp [global], 0; setne al`). |
| `NativeLeaf.TaggedStaticAddressAccessor` | 23 | `005C51E0` | `lea rax, [global]; or rax, 1; ret`: returns a static's address with bit 0 set. |
| `NativeLeaf.ThreeFloatStore` | 4 | `00194330` | Stores `xmm1`, `xmm2` and `xmm3` into three adjacent float fields of `this`. |
| `NativeLeaf.TwoFloatStore` |  | `00180870` | Stores `xmm1` and `xmm2` into two adjacent float fields of `this`. |
| `NativeLeaf.VectCountFloatOrConst` | 4 | `001C0820` | Divides the span `[+60h] - [+58h]` by 20 (multiply by `6666666666666667`<sub>h</sub>); when non-zero returns a float constant, else 0.0 when `[+10h]` is 0, else the float at `[[+18h]+24h]`. |

### Forwarders that set an argument and jump

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.ConstantFirstArgumentTailCall` |  | `002549F0` | `mov ecx, imm; jmp target`. |
| `NativeAdapter.FieldResetOffsetTailCall` | 26 | `0051E580` | Stores 0 or 1 into a dword field of `this`, sets `edx` to a small constant, adds `20`<sub>h</sub> (`70`<sub>h</sub> in four members) to `rcx` and jumps to one of four targets (`00470050`, `0046FFA0`, `0051DDC0`, `0051DBF0`); the members come in 0 / 1 pairs. |
| `NativeAdapter.FirstMemberPointerTailCall` |  | `00210960` | `mov rcx, [rcx]; jmp target`: the offset-0 spelling of the member-pointer forwarder. |
| `NativeAdapter.FourthArgumentZeroTailCall` |  | `00214B80` | `xor r9d, r9d; jmp target`. |
| `NativeAdapter.GlobalOffsetTailCall` |  | `0028E220` | `mov rcx, [global]; add rcx, off; jmp target`. |
| `NativeAdapter.MemberFieldSpanTailCall` | 4 | `00537F10` | Sets `rdx = this`, `r8 = this+off`, `rcx = [this+E0h] + off2` and `r9` = the second argument, then jumps to `003A56C0`. |
| `NativeAdapter.MemberOffsetTailCall` |  | `001A5800` | `add rcx, off; jmp target`: calls a member sub-object's method. |
| `NativeAdapter.MemberPointerTailCall` |  | `00210B60` | `mov rcx, [rcx+off]; jmp target`: calls a method of a pointed-to member. |
| `NativeAdapter.NullableFirstMemberTail` |  | `002BDAE0` | `mov rcx, [rcx+off]; test rcx, rcx; jne target; ret`. |
| `NativeAdapter.NullableGlobalTailDispatch` |  | `001AD450` | `mov rcx, [global]; test rcx, rcx; jne target; ret`. |
| `NativeAdapter.NullGuardTailCall` | 5 | `002681D0` | `test rcx, rcx; jne target; ret`: forwards only a non-null `this`. |
| `NativeAdapter.RelativeMemberAddressTailCall32` |  | `005C9720` | `rcx = rdx + ([this+48h] - [[this+18h]+F4h])`, `edx = r8d`, then `jmp target`. |
| `NativeAdapter.RelativeMemberAddressTailCall64` | 19 | `005CA350` | The same relative address with the 64-bit `r8` kept as `rdx` and `r9d` moved to `r8d`, then `jmp target`. |
| `NativeAdapter.SecondArgumentConstTailCall` |  | `0024ACE0` | `mov edx, imm; jmp target`. |
| `NativeAdapter.SecondArgumentZeroTailCall` |  | `0025E3F0` | `xor edx, edx; jmp target`. |
| `NativeAdapter.SetneFirstArgTailCall` |  | `00291D70` | `ecx = (ecx != 0)`, then `jmp target`. |
| `NativeAdapter.StaticAddressTailCall` |  | `00160310` | `lea rcx, [static]; jmp target`: passes a static's address. |
| `NativeAdapter.StaticPointerTailCall` |  | `0017E520` | `mov rcx, [global]; jmp target`: passes a pointer global. |
| `NativeAdapter.ThirdArgumentZeroTailCall` |  | `0025A690` | `xor r8d, r8d; jmp target`. |
| `NativeAdapter.VtableInstallTail` |  | `00212C50` | `lea rax, [vtable]; mov [rcx], rax; jmp target`: installs a vtable, then tail-calls. |
| `NativeAdapter.ZeroFirstArgTailCall` |  | `002A2BF0` | `xor ecx, ecx; jmp target`. |
| `NativeAdapter.ZeroSecondArgTailCall` | 4 | `002DF610` | `mov r8d, edx; xor edx, edx; jmp target`: shifts the second argument to the third and passes 0 as the second. |

### Adapters that call one function and pass its result on

| Family | Members | Example | Body |
|---|---|---|---|
| `FrameAdvanceContinuation` | 51 | `003D9000` | Calls `002F2530(this)`; when it returns non-zero calls a second function on `this`; returns the first result. |
| `NativeAdapter.BoolArgFetchResultTail` |  | `0017F720` | Saves `ecx != 0`, calls a getter, then `jmp target(result, saved bool)`. |
| `NativeAdapter.ByteSaveSecondArgResultTailCall2` |  | `0017F650` | Saves the low byte of `ecx`, calls a getter, then `jmp target(result, saved byte)`. |
| `NativeAdapter.CallBoolNormalizeReturn` | 6 | `001803D0` | Calls a function and returns `al != 0` as 0 or 1. |
| `NativeAdapter.CallBoolNormalizeReturnSete` |  | `002FFED0` | Calls a function and returns `eax == 0` as 0 or 1. |
| `NativeAdapter.CallResultArgShiftTailCall` |  | `0017FB90` | Saves `ecx` and `edx`, calls a getter, then `jmp target(result, ecx, edx)`. |
| `NativeAdapter.CallResultField32Getter` |  | `0017D340` | Calls a getter and returns the dword at a fixed offset in its result. |
| `NativeAdapter.CallResultMarshal24Bytes` | 16 | `005A3CE0` | Calls a function with `rcx = rdx` and copies 24 bytes of its result to the pointer in `r8`. |
| `NativeAdapter.CallResultMarshalCompositeRecord` | 19 | `00867040` | Calls a function with `rcx = rdx` and copies fields `+08`<sub>h</sub> to `+20`<sub>h</sub> (qword, qword, dword, byte, dword) of its result to the record in `r8`. |
| `NativeAdapter.CallResultTailCall` |  | `0017E220` | Calls a getter, then `jmp target` with its result as `rcx`. |
| `NativeAdapter.CallResultWithSavedIntTailCall` |  | `0017D940` | Saves `ecx`, calls a getter, then `jmp target(result, saved ecx)`. |
| `NativeAdapter.CallResultWithSavedThisTailCall` |  | `0017F190` | Saves `rcx`, calls a getter, then `jmp target(result, saved rcx)`. |
| `NativeAdapter.CallThenReturnZero` |  | `005A0D20` | Calls one function and returns 0. |
| `NativeAdapter.CallThenTailCall` |  | `0017D650` | Calls one function, then `jmp` to another. |
| `NativeAdapter.ChainedMemberResultTailCall` | 7 | `00340230` | Calls `00263F10(rdx)`, a member function on that result, then `jmp 0026B4E0(this, result)`. |
| `NativeAdapter.ConstFirstArgumentCallTailCall` |  | `00295CA0` | `ecx = imm`, calls one function, then `jmp` to another. |
| `NativeAdapter.DoubleSelfInvoke` | 6 | `001F40F0` | Calls `0067F580(this)` twice. |
| `NativeAdapter.EHCallWrapper` | 11 | `00199D30` | An exception-frame prologue (`[rsp+20h] = -2`) around one call with the incoming arguments. |
| `NativeAdapter.FanoutFieldUpdate4` |  | `0050C450` | Calls one function on `this`, then three field-object functions on `this+off` with the saved `edx`, and returns the address of a later field. |
| `NativeAdapter.FanoutFieldUpdate5` | 4 | `005324C0` | Calls one function on `this`, then four field-object functions on `this+off` with the saved `edx`, and returns the address of a later field. |
| `NativeAdapter.FixedPipelineCallResult` |  | `00271420` | Calls `0036C1D0(3, Fh)`, `0036A100(ecx)`, `0036C140()`, and returns the middle call's result. |
| `NativeAdapter.ForwardSecondArgumentCallReturnTrue` |  | `005A3420` | Calls a function with `rcx = rdx` and returns 1. |
| `NativeAdapter.MemberArgumentEHCallWrapper` | 12 | `001A28B0` | The same frame around one call with `rdx = [this+18h]`. |
| `NativeAdapter.NamedRecordRegisterPair` |  | `00862E90` | Calls `001FB840` with one string, then `jmp 0020E630` with a second string and the saved `ecx`. |
| `NativeAdapter.SavedFourArgCallResultCall` |  | `001816F0` | Saves four arguments, calls a getter, then calls a second function with the result and the four arguments (the fourth on the stack). |
| `NativeAdapter.SharedGetterThreeArgTailCall` |  | `001DBAC0` | Saves three arguments, calls `00210B30`, then `jmp target(result, arg1, arg2, arg3)`. |
| `NativeAdapter.SmallRecordVtableCtor` |  | `001F17B0` | Calls `00212CC0(this)`, stores `edx` at `+18`<sub>h</sub>, installs a vtable and returns `this`. |
| `NativeAdapter.StackConstOneCall` | 5 | `00272F60` | Stores a constant (0 or 1) as the fifth argument and calls one function. |
| `NativeAdapter.TwoSubobjectInvokeTailCall` | 6 | `00219470` | Calls one function on two member sub-objects of `this`, then `jmp` to another on `this`. |

### Guarded and conditional adapters

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.BooleanSelectedCallReturnTrue` | 10 | `0062EE00` | Calls one of two functions on `rdx`, chosen by the byte in `r8b`, and returns 1. |
| `NativeAdapter.CallResultDualTailDispatch` | 8 | `00340B90` | Calls `00267E10(r9)` and jumps to one of two functions chosen by whether the result is zero. |
| `NativeAdapter.ChainPredicateReleaseTail` | 5 | `005DD5E0` | Calls a predicate on `this`; when true calls a second function on `this`; then jumps to a third on `this`. |
| `NativeAdapter.ConditionalDoubleCallResultTailCall` |  | `0017F040` | Saves `ecx`; calls a getter, and when non-null calls it again and jumps to `target(result, saved ecx)`. |
| `NativeAdapter.DoubleCallResultTailCallSavedThis` |  | `00182310` | Saves `rcx`; calls a getter, and when non-null calls it again and jumps to `target(result, saved rcx)`. |
| `NativeAdapter.DynamicOffsetRefFlagCall` | 5 | `005CA3E0` | Returns 5 when bit 31 of `r9d` is set; otherwise sets it, calls a function on `rdx + ([this+48h] - [[this+18h]+F4h])` and returns 0. |
| `NativeAdapter.FirstMemberInvokeFieldStore` | 7 | `0029F100` | When the pointer at `this+off` is non-null, calls a function on it and then clears the field. |
| `NativeAdapter.FlagByteConditionalOp` | 4 | `005CE800` | When the byte at `rdx+8` is non-zero, calls `005CDAA0(3, string)`; when the pointer at `rdx+20h` is non-null, calls `006108C0` on it; returns 1. |
| `NativeAdapter.FlagGatedInitTailCall` |  | `00227460` | When one bit of the dword `01FD46D4` is clear, calls `00226BE0(imm, 0, 0, 0, -1, -1)` and jumps to `00226280`. |
| `NativeAdapter.GlobalGuardIndexedCall` | 4 | `00226180` | When one bit of the dword `01FD46D4` is set, calls `00225CD0(imm, -1)` and jumps to `00226280`. |
| `NativeAdapter.GuardedCallResultBoolInvert` | 6 | `005113A0` | Calls `00280120`; when non-zero returns 0, else calls a function and returns `eax == 0`. |
| `NativeAdapter.GuardedPairInvokeFieldStore` | 11 | `0044BA80` | Calls `002F2D60(this)`; when non-zero calls a function on `this`, then `0044B960`, stores its result in a field and returns 1. |
| `NativeAdapter.GuardedRecordBuildCookie` | 4 | `005571F0` | Under a stack cookie: when a field of `this` is zero, builds a stack record, calls `00244F50`, stores the result in that field and passes it to `00246AD0`. |
| `NativeAdapter.GuardedSharedPairTailCall` | 9 | `00511510` | Calls `00280120`; when zero calls `00267E10(r9)` and jumps to a function with that result. |
| `NativeAdapter.HandleRecordOutFloatInit` | 4 | `002E9A90` | Resolves the argument with `003588B0`, follows `+C0`<sub>h</sub> into the same `740`<sub>h</sub>-stride table, calls a function on the out record in `rdx` when `+284`<sub>h</sub> is set, zeroes its first 12 bytes when the handle or record pointer is missing, and always stores 1.0 at its `+C`<sub>h</sub>. |
| `NativeAdapter.IndexedRecordStoreCookie` |  | `00227E20` | Under a stack cookie: builds a stack record holding the sign-extended argument and calls `00244F50(imm, code address, record)`. |
| `NativeAdapter.NullableCallChainTailCall` |  | `0017CFD0` | Calls a getter; when it returns non-null, calls it again and jumps to a second function with that result. |
| `NativeAdapter.NullableFetchByteTail` | 4 | `0017F5B0` | Saves the low byte of `ecx`; calls a getter, and when non-null calls it again and jumps to `target(result, saved byte)`. |
| `NativeAdapter.NullableRecordWordTail` | 4 | `002E8B60` | When `this`, the pointer at `+C0`<sub>h</sub> and its dword are valid (not null, not -1), jumps to a function with the record's word in `ecx`. |
| `NativeAdapter.OutRecordMemberCallTailCall` | 5 | `0042DCA0` | Calls `00426220(this, [rdx+8])`; when it returns 0, jumps to a function on `this`. |
| `NativeAdapter.PredicateGuardConstCall` |  | `00347C60` | Calls a predicate; when non-zero calls `00314D40(imm)` and returns 1, else returns 0. |
| `NativeAdapter.PredicateGuardSharedCall` |  | `0044A5F0` | Calls `002F2D60(this)`; when non-zero calls a function on `this` and returns 1, else returns 0. |
| `NativeAdapter.RefFlagSetCallZero` | 5 | `005CA2B0` | When bit 31 of `r8d` is clear, sets it and calls a function; returns 0. |
| `NativeAdapter.TableIndexDispatchSetFlag` |  | `002E7450` | The same resolution; when `+284`<sub>h</sub> is non-zero calls a function on the record and sets bit `800`<sub>h</sub> of its `+290`<sub>h</sub>. |
| `NativeAdapter.TableIndexDispatchTailCall` | 5 | `002E5BC0` | Resolves the word at `[[this+C0h]]` through the record table whose base is the qword `022C6F28` (stride `740`<sub>h</sub>) and jumps to a function when the record's dword `+284`<sub>h</sub> is non-zero. |
| `NativeAdapter.TripleMemberChainReturnTrue` | 6 | `005CF750` | Calls a predicate on `rdx`; when true calls a second function on `rdx`; always calls a third on `rdx`; returns 1. |
| `NativeLeaf.NullableGlobalClearCall` | 5 | `00366A00` | When a pointer global is non-null, calls a function on it and then zeroes the global. |
| `NativeLeaf.StaticHandleReplaceWithPreRelease` |  | `00238390` | Frees the handle in a global through `003844F0` when it is non-null, then stores the sign-extended argument there. |

### Adapters over an argument record

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.FloatFetchPushForward` | 4 | `00342040` | Calls a float getter on `rdx`, passes the float to `00267F60(r9)`, then jumps to a function with the four original arguments. |
| `NativeAdapter.PopIntForwardTail` | 4 | `00342340` | Reads an integer from the record in `r9` with `00267E10`, passes it through one function and jumps to another with the result. |
| `NativeAdapter.PopThreeFloatGuardTail` | 4 | `00340D00` | Reads three floats with `00267DB0` and an integer with `00267E10`, calls `0016D6A0` and `003EB700` on the integer, then jumps to a function with the result and the three floats. |
| `NativeAdapter.PopThreeIntForwardTail` | 4 | `00348C50` | Reads three integers with `00267E10`, passes the last through `00264010` and `00263F10`, then jumps to a function with that result and the first two. |
| `NativeAdapter.SharedNormalizeTailCallOne` | 6 | `0034B450` | Calls `0026A1A0(rdx, 1)`, restores the four arguments and jumps to a function. |
| `NativeAdapter.SharedNormalizeTailCallZero` | 6 | `00341390` | Calls `0026A1A0(rdx, 0)`, restores the four arguments and jumps to a function. |
| `NativeAdapter.TwoSharedComposeTailCall` | 6 | `00340DC0` | Calls `002640C0`, reads an integer with `00267E10(r9)`, then jumps to a function with both. |

### Out-record initialisers

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.NullableOutRecordHeaderInitReturnTrue` | 9 | `005CE010` | When `rdx` is non-null writes a constant qword (a different one per member) and two zero qwords there; returns 1. |
| `NativeAdapter.NullableOutRecordVptrCall` | 5 | `0063F2A0` | When `rdx` is non-null calls a function on it and installs a vtable at `+0`; returns 1. |
| `NativeAdapter.OutRecordDescriptorInitReturnTrue` | 19 | `00866FA0` | When `rdx` is non-null writes three addresses at `+0`, `+8`, `+10`<sub>h</sub>, zeroes `+18`<sub>h</sub> and `+1C`<sub>h</sub>, and stores 1.0 at `+20`<sub>h</sub>; returns 1. |
| `NativeAdapter.OutRecordVtablePairStore` |  | `0063EF60` | When `rdx` is non-null calls a function on it and stores two addresses at `+0` and `+8`; returns 1. |
| `NativeAdapter.OutRecordZeroInitMemberInit` | 7 | `005CFF00` | When `rdx` is non-null clears `90`<sub>h</sub> bytes there with `memset` (`00861EC0`) and calls an initialiser on it; returns 1. |
| `NativeLeaf.TaggedOutRecordFloatVcall` | 5 | `006B3120` | Advances the cursor in the fifth argument by 8, converts the double there to float, calls `[this+8](rdx, float)`; when the third argument equals `006B0B20()` with bit 0 set, stores the result at `out+8`, zeroes `out+0` and returns 1, else 0. |

### Construction, destruction and static lifetime

| Family | Members | Example | Body |
|---|---|---|---|
| `CompilerGeneratedCpp.GuardedStaticObjectTeardown` | 28 | `008B0E20` | Calls `0016D6A0` (`ret 0`) with a static's address and returns. |
| `CompilerGeneratedCpp.StaticContainerTeardown.IndirectAllocator` | 60 | `008A69F0` | When a static container holds more than one byte and a non-null begin, returns the storage through slot 3 of its allocator object. |
| `CompilerGeneratedCpp.StaticZeroInitObjectInitializer` | 11 | `00169A10` | Clears a `50`<sub>h</sub>-byte static with `memset`, constructs its lock with `007DF6D0`, and registers its teardown with `atexit` (`00808B90`). |
| `CxxObjectLifecycle.ConditionalTeardownReturnTrue` |  | `00611A10` | When `rdx` is non-null calls a destructor on it; returns 1. |
| `CxxObjectLifecycle.DeletingDestructor.AlignedOrGuardedFree` |  | `005AC810` | Deleting destructor: calls the destructor; when flag bit 0 is set frees `this` with `00584730`, or, when bit 2 is also set, calls `0016D6A0(this, size)`; returns `this`. |
| `CxxObjectLifecycle.DeletingDestructor.VtableAlignedOrGuardedFree` |  | `0017CC70` | The same deleting destructor with a vtable install before the destructor call. |
| `CxxObjectLifecycle.DerivedConstructorVtableInstall` |  | `001F1740` | Calls the base constructor on `this`, installs the derived vtable, returns `this`. |
| `CxxObjectLifecycle.VtableInstallStub` |  | `0018D0E0` | `lea rax, [vtable]; mov [rcx], rax; ret`. |
| `DeletingDestructor.SharedTeardown` |  | `00584870` | The vtable-installing deleting destructor whose destructor call is always `00633390`. Same instruction form as the previous family. |
| `Platform.Windows.CriticalSectionStaticInitializer` | 19 | `00169690` | `InitializeCriticalSection` (IAT `008C20B0`) on a static, then registers its teardown with `atexit`. |
| `Runtime.NamedRegistryRecord.StaticInitializer` | 60 | `0015C510` | Calls `005DC6F0(static, string, 0)`, then registers its teardown with `atexit`. |
| `Runtime.NameRegistryEntry.StaticInitializer` | 56 | `00162430` | Calls `005FDCB0` with a static's address, then registers its teardown with `atexit`. |
| `Runtime.Singleton.LazyAllocatorInitializer` |  | `0019CDE0` | When a pointer global is null, allocates a fixed size with `00210EC0`, constructs the object in it, and stores the pointer. |
| `Runtime.Singleton.StaticObjectFixupRegisterRelease` |  | `008AF570` | Installs a vtable in a static; when a link static does not point at itself, calls slot `48`<sub>h</sub> of the object in another static; calls `006B6700` on a member static; frees a buffer with `00584730` when bit 0 of a flag byte is set. |

### Owned buffers and allocator releases

| Family | Members | Example | Body |
|---|---|---|---|
| `Runtime.Container.OwnedBufferAlignedFreeResetReturnTrue` | 11 | `005C3430` | On `rdx`: when bit 31 is clear and the count is above 1, frees `+8` with `00584730`; zeroes both; returns 1. |
| `Runtime.Container.OwnedBufferReset` |  | `001B6EA0` | When bit 31 of the count word at `+0` is clear frees the pointer at `+8` with `00584730`; zeroes both. |
| `Runtime.Container.OwnedBufferTeardownResetReturnTrue` | 13 | `005C31D0` | On `rdx`: when bit 31 is clear calls a teardown with the pointer and the count; zeroes both; returns 1. |
| `Runtime.Container.SpanCheckMemberVcall` | 6 | `001AAD20` | When the span `[this] .. [this+10h]` holds more than one byte and begins non-null, calls slot 3 of the object at `this+18h`. |
| `Runtime.Memory.IndirectAllocatorRelease` | 22 | `00185070` | When `[this]` is non-null, returns the span `[this] .. [this+10h]` (masked to the element alignment) through slot 3 of the allocator object at `this+18h`. |

### Virtual and indirect dispatch

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.DualLookupIndirectCallback` |  | `005C2060` | Calls two lookups on `rdx`; when the second is non-null calls the function at `[this+8]` with both results; returns 0. |
| `NativeAdapter.TwoMemberCallIndexedVcall` | 7 | `0063A300` | Calls two functions on `rdx`; when the second is non-null calls `[this+8]` with `rcx = result + [this+10h]`; returns 0. |
| `NativeDispatch.GlobalHandlerSlotTailCall` |  | `004174F0` | Loads a handler global; when set, jumps to it with `rdx = rcx` and `rcx = [r8+2E0h]`. |
| `NativeDispatch.MemberVirtualTailCall` |  | `00726DB0` | `mov rcx, [rcx+off]; mov rax, [rcx]; jmp [rax+slot]`. |
| `NativeDispatch.NullableVirtualTailCall` | 11 | `0017F0C0` | Returns when `rcx` is null; otherwise `jmp [[rcx]+slot]`. |
| `NativeDispatch.VirtualTailCall` |  | `00616E24` | `mov rax, [rcx]; jmp [rax+slot]`. Same instruction form as the fixed-slot adapters. |
| `Runtime.VirtualDispatch.FixedSlotAdapter` |  | `00616E0C` | `mov rax, [rcx]; jmp [rax+slot]`. |

### Loops, walks, lookups and table reads

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.BitfieldOrNodeWalk` | 9 | `001A20A0` | Initialises a record in `this` (zeroes `+0` to `+1B`<sub>h</sub>, `+20`<sub>h</sub> = `rdx+38h`, `+28`<sub>h</sub> = the list's first node, `+30`<sub>h</sub> = a table address), steps it with `001B7CE0` until that returns true, then calls `001AA0A0`; returns `this`. |
| `NativeAdapter.CountedLoopMemberInvoke` | 5 | `0062B020` | For each index below the count at `+18`<sub>h</sub> (bit 31 masked, at least 1), calls `005CCB80(1)` while a lookup's dword is positive. |
| `NativeAdapter.GlobalSlotFlagClearOps` | 4 | `003302B0` | Clears bit 13 of the qword `table[ecx]`; when no bit but bit 0 remains, calls `00263FF0(ecx)` and clears bit 3 of the byte at its `+11`<sub>h</sub>; when a non-zero slot became zero, calls `0032F1B0(ecx)`. |
| `NativeAdapter.MallocRecordEmplaceTailCall` |  | `0018B5D0` | Allocates `20`<sub>h</sub> bytes through `0085E730` (`malloc`), constructs a record with `edx`, appends its pointer to the vector in `this` (end `+8`, capacity `+10`<sub>h</sub>, grown by `001AB570`), then jumps to `0018AFF0(0018B4E0(), record)`. |
| `NativeAdapter.MemberPredicateTreeSearch` | 6 | `00219E30` | Walks the circular list at `this+8` calling a predicate on each node's `+10`<sub>h</sub> with the three other arguments; returns 1 at the first true, else 0. |
| `NativeLeaf.BoundedTableWordLookup` | 5 | `0032F260` | When `ecx` is within a bound, takes a row pointer from a table; when the row's first byte is non-zero returns its dword at `+8 + edx*8`, else -1. |
| `NativeLeaf.ClampedIndexTableStore` | 4 | `002E2050` | Stores `edx` into entry `ecx` of a table (fixed stride); a negative index stores into entry 0, an index at or above the bound stores nothing. |
| `NativeLeaf.ClampedTableLookup` | 7 | `0035EE50` | Returns 0 when `ecx` is at or above a bound; otherwise takes row `ecx` (stride `294`<sub>h</sub>), wraps `byte [row+1] + edx` into 0 to 15, and returns the word at `+4A`<sub>h</sub> of that 36-byte entry. |
| `NativeLeaf.ListStringCompare` | 4 | `005C5250` | Walks a global chain (next at `+8`) comparing each node's name at `+0` with the argument; returns the node or 0. |
| `NativeLeaf.RecursiveListVcallWalk` | 5 | `001A48C0` | Recurses into `[node]`, then calls slot 3 of the object at `this+30h` with `(node, 38h)`, moving to `[node+8]` until null. |
| `Runtime.Container.RecursiveSpanNodeWalk` |  | `001A4B50` | The same recursive walk with node size `40`<sub>h</sub>, which also returns each node's own span `[node+20h] .. [node+30h]` through slot 3 of the allocator at `node+38h`. |
| `Runtime.Container.StringKeyedChainAttach` |  | `006B8D20` | Returns `11`<sub>h</sub> when the name at `+8` is null; walks a global chain comparing names byte by byte; returns `12`<sub>h</sub> on a match, else links `this` at the head and returns 0. |
| `Runtime.Registry.StringLookup` | 10 | `006C04C0` | Walks a global chain (next at `+10`<sub>h</sub>) comparing each node's name at `+8` with the argument; returns the node or 0. |
| `Runtime.SerialRangeInvokeLoop` | 7 | `0030DCB0` | For every id of one class, `1000h * class + i` below the class count, calls `003008A0(id, 63h, 0, 1, 0)`. |

### Large bodies

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.RecordChainDoubleResolve` | 4 | `00429A50` | Under a stack cookie: resolves a word id through the `740`<sub>h</sub>-stride table, checks each hop with `00426220`, follows the record's `+8` word the same way, and calls `0042EF90` for the words at `+8` and `+A`<sub>h</sub>. |
| `NativeAdapter.RecordFieldCopy` | 5 | `0068C260` | Calls a getter with `rcx = rdx` and copies its fields from `+8` onward to the record in `r8`, field by field. |
| `NativeLeaf.FloatBankGlobalPublish` | 4 | `004630D0` | Copies the vector at `this+60h` into a bank of float globals (adding each lane to a base), stores `this` in a global, then continues through `0039AF70`, `00398F90` and others. |
| `NativeLeaf.LargeFloatGlobalPublish` |  | `00452020` | Under a stack cookie: copies a record with `00430B90` into `this+110h`, publishes it to a bank of float globals, then runs a long sequence of fixed calls. |
| `NativeLeaf.SlideTableRecordCopyInvoke` |  | `002EFE70` | Two word globals select two 16-byte slots of a global record array; copies a 16-byte record and an 8-byte tail between them, advances the counters, and calls the function in `rcx`. |

### Reflection descriptor adapters

| Family | Members | Example | Body |
|---|---|---|---|
| `Reflection.OwnedBufferResetAdapter` | 46 | `005A4830` | On `rdx`: when bit 31 of the count word at `+0` is clear and the pointer at `+8` is non-null, frees it with `00584730`; zeroes both; returns 1 (59 bytes). |
| `Reflection.ReturnValueAdapter` |  | `00584780` | `push rbx; sub rsp, 20h; mov rcx, rdx; mov rbx, r8; call target; mov [rbx], rax; ...; ret` (26 bytes): calls the target with the second argument and stores the returned pointer through the third. |


## Related

- [Global state accessors](../Engine-Core/global-state-accessors.md): the one-instruction
  getters of globals, counted over the whole image.
- [Jump thunks](../Engine-Core/jump-thunks.md): the one-jump forwarders and the `ret 0`
  stub `0016D6A0`.
- [Vtable methods](../Engine-Core/vtable-methods.md): every virtual slot with its class.
- [Debug logging](../Engine-Core/debug-logging.md): the log call `005CDAA0` one family
  calls.
- [Object construction and destruction](object-construction-and-destruction.md): the constructor and
  deleting-destructor forms across the image.
- [Static initialisation and teardown](static-initialisation-and-teardown.md): the initialisers and
  `atexit` registrations.
- [Lazy statics and one-time initialisation](lazy-statics-and-one-time-init.md): the guarded
  function-local statics.
- [Thunks and import stubs](thunks-and-import-stubs.md): the import stubs several shared functions
  end in.
- [Runtime services](runtime-services.md): the imports these bodies reach.
