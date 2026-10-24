---
title: "Generated function families: the small compiler- and template-generated bodies, their instruction forms and member lists"
kind: "reference"
category: "Compiler and C runtime"
addresses: "0x0016D6A0, 0x00584730, 0x00210EC0, 0x00808B90, 0x00861EC0, 0x007DF6D0, 0x003844F0, 0x00633390, 0x005A2B80, 0x005BEC00, 0x006B2950, 0x006B2970, 0x005A4830, 0x0030DCB0, 0x003008A0, 0x005CDAA0"
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
with 7,807 listed functions. Every listed member of every family decodes to its family's
form; nine leaf families have two to five spellings of it (with or without an offset, or at
different operand widths). For each family the image was also searched for every function with that form that calls
every target the listed members share. For all 171 families the search returns exactly the member list, so
each family's member count is the number of functions in the image with its body.

Two pairs of lists share one form and are told apart by a value the form drops:

- the vtable-installing deleting destructors, by whether the destructor they call is `0x00633390`;
- the field clears and the constant field stores, by whether the stored constant is 0.

The virtual tail calls and the fixed-slot adapters share the form `mov rax, [rcx]; jmp [rax+slot]` and are
told apart by their references. A fixed-slot adapter is never called directly and never held as a pointer in
the image; its address is taken only by a `lea` in installer code: the six static initialisers `0x00162FF0` to
`0x001630E0`, which pass three adapters each to `0x006155B0`, the static initialiser `0x007943E0`, and `0x0079F150`. A
virtual tail call is held as a pointer in a vtable or a pointer table.

### The shared functions the families call

Many families call the same few runtime functions:

| Function | Body | Called by |
|---|---|---|
| `0x0016D6A0` | `ret 0` | the guarded static teardowns, the bit-2 arm of the deleting destructors (so that arm frees nothing), the global handle reads, the three-float record adapters |
| `0x00584730` | `if (p) jmp 0x0019C570`, and `0x0019C570` is `jmp [0x008C2B70]`, the `_aligned_free` import | the deleting destructors, the owned-buffer resets, the static object fixups |
| `0x00210EC0` | `or r8d, -1; xor edx, edx; jmp 0x0085E730`, and `0x0085E730` is `jmp [0x008C2B40]`, `malloc` | the lazy singleton allocators |
| `0x00808B90` | `atexit`: calls `_onexit` (`0x00808B40`) and returns 0 or -1 | the static initialisers, as their tail jump |
| `0x00861EC0` | `jmp [0x008C2A60]`, `memset` | the zero-init initialisers, the zeroing out-record initialisers |
| `0x007DF6D0` | `InitializeCriticalSection(this)` (IAT `0x008C20B0`), then zeroes `+0x28` to `+0x4B` and returns `this` | the zero-init initialisers |
| `0x003844F0` | `jmp 0x003697F0`, which returns for null and otherwise jumps to `0x00369860(p, 0)` | the static handle replacements |

### Reflection descriptor slots

The return-value adapters are 26 bytes each. `0x005A2B80` is typical:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x005A2B80` | `...` | push rbx |  |
| `0x005A2B82` | `sub` | rsp, 0x20 |  |
| `0x005A2B86` | `mov` | rcx, rdx | ; the second argument becomes the first |
| `0x005A2B89` | `mov` | rbx, r8 | ; the third is an out pointer |
| `0x005A2B8C` | `call 0x005BEC00` | ; the only part that differs between members |  |
| `0x005A2B91` | `mov` | [rbx], rax | ; store the returned pointer |
| `0x005A2B94` | `add` | rsp, 0x20 |  |
| `0x005A2B98` | `pop` | rbx |  |

```
0x005A2B99  ret
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
appear three times, 34 twice, `0x006B2950` six times and `0x006B2970` ten times. Those two are the
only adapters shared between classes: `0x006B2950` serves `Matrix3`, `Matrix4` and `PMatrix4`, and
`0x006B2970` serves `Point3`, `Quat`, `Vector2`, `Vector3` and `Vector4`.

The other 401 targets each load the name of one script pointer accessor,
`Phyre::PScripting::PScriptAccessors::PObjectAccessor<T *>::Get`, beside their error messages;
none loads a reference accessor's (`T &`) name.

`0x005BEC00`, the target above, starts with
`0x00682980`, which looks up `PhyreObject` in the Lua registry (pseudo-index `-1001000`) and returns
non-null only when the comparison `0x00810810` succeeds, and it names
`PObjectAccessor<class Phyre::PAnimation::PTimeScaleOffsetController *>::Get`. So slot 5 of a
class descriptor converts a script value into a pointer to an object of that class, and the
adapter gives every class the same `(descriptor, value, T **out)` call. The shared targets of
`0x006B2950` and `0x006B2970` (`0x00683B10`, `0x00683BF0`) load no accessor name.

The owned-buffer reset adapters (`0x005A4830`, 59 bytes) are slot 11 of the same descriptors: their
46 bodies appear 138 times, all at slot 11, once each in the `ForType`, `Abstract` and `Concrete`
descriptor of one class. The instance they reset is a count word, whose bit 31 when set keeps the
buffer from being freed, and a data pointer at `+8`.

### The serial-range loops

The seven `Runtime.SerialRangeInvokeLoop` members each walk one class of ids. `0x0030DCB0` sets
`ebx` to `0x1000` and, while `ebx` is below `0x1000 + [0x01EEBD54]`, calls
`0x003008A0(bx, 0x63, 0, 1, 0)` (`0x0030DCD0` to `0x0030DCE4`). The other six use bases `0x2000`,
`0x3000`, `0xC000`, `0x8000`, `0x4000` and `0x6000` with the counts at `0x01EEBDAC`, `0x01EEBE04`,
`0x01EEC11C`, `0x01EEBFBC`, `0x01EEBE5C` and `0x01EEBF0C`.

`0x003008A0` is the entry that changes what the
party owns ([item and ability ids](../Engine-Core/item-and-ability-ids.md)): each call
adds 99 of one id on channel 1, so each member adds 99 of every id of its class.

### Lists beside the families

These member files beside the page are not single-form families:

- [`generated-function-families-trivial-global-accessors.tsv`](generated-function-families-trivial-global-accessors.tsv): functions whose whole body is one instruction with one rip-relative operand and `ret`: `lea`, loads and stores of 1, 2, 4 or 8 bytes, and constant stores. The image has 570
  such functions; the list names part of them.
- [`generated-function-families-documented-global-leaf-accessors.tsv`](generated-function-families-documented-global-leaf-accessors.tsv): a list of small bodies, each row naming a target global.
- [`generated-function-families-explained-callee-adapters.tsv`](generated-function-families-explained-callee-adapters.tsv): a list of small adapters, each row naming the function it forwards to.
- [`generated-function-families-generated-families-installed-classes.tsv`](generated-function-families-generated-families-installed-classes.tsv): for the vtable-installing families, the class whose vtable each member installs. Each
  of its 120 rows names the class of the first rip-relative address in the member's body that is
  preceded by a valid RTTI locator.
- [`generated-function-families-generated-families-shared-implementations.tsv`](generated-function-families-generated-families-shared-implementations.tsv): for each family, the functions every member calls.
  The 15 rows for families on this page each name a function every member of that family calls;
  the other 8 rows are for the Lua and PhyreEngine reflection families on other pages.

## Columns

| Column | Meaning |
|---|---|
| `family` | the family's name |
| `shape` | what every member's body does, in instruction terms |
| `members` | the number of members; the image search returns exactly the member list for every family |
| `example` | one member's entry address (the lowest) |
| `member_list` | the file beside this page that lists every member |

## Data

### Leaf getters, stores and predicates

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeLeaf.ConstantDwordReturn` | 89 | `0x0017E410` | `mov eax, imm32; ret`: returns a constant. |
| `NativeLeaf.DoubleCallBool` | 4 | `0x0017E4E0` | Calls one function, calls a second on its result, returns the second result's low byte zero-extended. |
| `NativeLeaf.DoubleDerefFlagExtract` | 6 | `0x001E4AE0` | `rax = [rcx+off]`; returns one bit of the dword at `[[rax]+off2]` (`shr`, `and 1`). |
| `NativeLeaf.FieldByteGetter` | 31 | `0x00187530` | `movzx eax, byte [rcx+off]; ret` (or `[rcx]`). |
| `NativeLeaf.FieldByteStore` | 27 | `0x001863E0` | `mov byte [rcx+off], dl; ret` (or `[rcx]`). |
| `NativeLeaf.FieldClear` | 20 | `0x00189C10` | `mov [rcx+off], 0; ret`, byte to qword width. Same instruction form as the constant stores, with the constant 0. |
| `NativeLeaf.FieldConstStore` | 19 | `0x00193930` | `mov [rcx+off], imm; ret` with a non-zero constant, byte to qword width. |
| `NativeLeaf.FieldDwordGetter` | 52 | `0x00186980` | `mov eax, [rcx+off]; ret` (or `[rcx]`). |
| `NativeLeaf.FieldDwordStore` | 22 | `0x001B1FA0` | `mov [rcx+off], edx; ret`. |
| `NativeLeaf.FieldFlagMaskClear` | 6 | `0x00313F70` | `and [rcx+off], mask; ret`: clears flag bits of a byte or dword field. |
| `NativeLeaf.FieldFloatGetter` | 35 | `0x001867D0` | `movss xmm0, [rcx+off]; ret`. |
| `NativeLeaf.FieldFloatStore` | 23 | `0x00194300` | `movss [rcx+off], xmm1; ret`. |
| `NativeLeaf.FieldQwordGetter` | 36 | `0x00186660` | `mov rax, [rcx+off]; ret` (or `[rcx]`). |
| `NativeLeaf.FieldQwordStore` | 16 | `0x001B22D0` | `mov [rcx+off], rdx; ret` (or `[rcx]`). |
| `NativeLeaf.FlagBit1SetClear` | 4 | `0x0018B070` | When the byte argument `dl` is non-zero, sets bit `0x2` of the dword at `this+0x20`; otherwise clears it. |
| `NativeLeaf.FlagBit2SetClear` | 4 | `0x0026A320` | Clears one bit of a byte field, then sets it again when `edx` is non-zero (`setne`, `shl`, `or`). |
| `NativeLeaf.GlobalHandleStateRead` | 6 | `0x001B5FB0` | Calls `0x0016D6A0` with `ecx` = (pointer global non-zero), then returns a second global. |
| `NativeLeaf.GlobalQwordStore` | 9 | `0x00378B80` | `mov eax, ecx; mov [global], rax; ret`: stores the zero-extended argument into a qword global. |
| `NativeLeaf.MemberAddressAccessor` | 22 | `0x001B0FA0` | `lea rax, [rcx+off]; ret`: returns the address of a member. |
| `NativeLeaf.NoOpReturnStub` | 38 | `0x006DA8C0` | `ret 0`: returns at once. |
| `NativeLeaf.NullableDerefWordAdd` | 4 | `0x003E6CF0` | `rdx = [rcx+off]`; when it and its word at `+0x10` are non-zero returns that word plus the low 32 bits of `rdx`, sign-extended; otherwise 0. |
| `NativeLeaf.PairedStaticConstStore` | 10 | `0x0017F270` | Two `mov [global], imm` stores into two globals, then `ret`; byte to dword width. |
| `NativeLeaf.PayloadBaseBitExtract` | 6 | `0x00314A80` | Calls `0x002EF2B0` and returns one bit of a byte at a fixed offset in the returned block. |
| `NativeLeaf.PayloadBaseFlagSet` | 4 | `0x00314BB0` | Calls `0x002EF2B0`, clears one bit of a byte in the returned block, and sets it again when the argument is non-zero. |
| `NativeLeaf.StaticGlobalFloatSetter` | 21 | `0x002B6670` | `movss [global], xmm0; ret`: stores the float argument into a global. |
| `NativeLeaf.StaticPointerBitfieldGetter` | 14 | `0x00236780` | Loads a pointer global and returns one bit of a dword field of its object (`shr`, `and 1`). |
| `NativeLeaf.StaticPointerNestedFieldGetter` | 14 | `0x0027E9D0` | Loads a pointer global and returns the qword at a fixed offset in what it points to. |
| `NativeLeaf.StaticPointerNonNullPredicate` | 11 | `0x00228480` | Returns 1 when a pointer global is non-zero (`cmp [global], 0; setne al`). |
| `NativeLeaf.TaggedStaticAddressAccessor` | 23 | `0x005C51E0` | `lea rax, [global]; or rax, 1; ret`: returns a static's address with bit 0 set. |
| `NativeLeaf.ThreeFloatStore` | 4 | `0x00194330` | Stores `xmm1`, `xmm2` and `xmm3` into three adjacent float fields of `this`. |
| `NativeLeaf.TwoFloatStore` | 5 | `0x00180870` | Stores `xmm1` and `xmm2` into two adjacent float fields of `this`. |
| `NativeLeaf.VectCountFloatOrConst` | 4 | `0x001C0820` | Divides the span `[+0x60] - [+0x58]` by 20 (multiply by `0x6666666666666667`); when non-zero returns a float constant, else 0.0 when `[+0x10]` is 0, else the float at `[[+0x18]+0x24]`. |

### Forwarders that set an argument and jump

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.ConstantFirstArgumentTailCall` | 26 | `0x002549F0` | `mov ecx, imm; jmp target`. |
| `NativeAdapter.FieldResetOffsetTailCall` | 26 | `0x0051E580` | Stores 0 or 1 into a dword field of `this`, sets `edx` to a small constant, adds `0x20` (`0x70` in four members) to `rcx` and jumps to one of four targets (`0x00470050`, `0x0046FFA0`, `0x0051DDC0`, `0x0051DBF0`); the members come in 0 / 1 pairs. |
| `NativeAdapter.FirstMemberPointerTailCall` | 18 | `0x00210960` | `mov rcx, [rcx]; jmp target`: the offset-0 spelling of the member-pointer forwarder. |
| `NativeAdapter.FourthArgumentZeroTailCall` | 7 | `0x00214B80` | `xor r9d, r9d; jmp target`. |
| `NativeAdapter.GlobalOffsetTailCall` | 5 | `0x0028E220` | `mov rcx, [global]; add rcx, off; jmp target`. |
| `NativeAdapter.MemberFieldSpanTailCall` | 4 | `0x00537F10` | Sets `rdx = this`, `r8 = this+off`, `rcx = [this+0xE0] + off2` and `r9` = the second argument, then jumps to `0x003A56C0`. |
| `NativeAdapter.MemberOffsetTailCall` | 44 | `0x001A5800` | `add rcx, off; jmp target`: calls a member sub-object's method. |
| `NativeAdapter.MemberPointerTailCall` | 45 | `0x00210B60` | `mov rcx, [rcx+off]; jmp target`: calls a method of a pointed-to member. |
| `NativeAdapter.NullableFirstMemberTail` | 5 | `0x002BDAE0` | `mov rcx, [rcx+off]; test rcx, rcx; jne target; ret`. |
| `NativeAdapter.NullableGlobalTailDispatch` | 12 | `0x001AD450` | `mov rcx, [global]; test rcx, rcx; jne target; ret`. |
| `NativeAdapter.NullGuardTailCall` | 5 | `0x002681D0` | `test rcx, rcx; jne target; ret`: forwards only a non-null `this`. |
| `NativeAdapter.RelativeMemberAddressTailCall32` | 46 | `0x005C9720` | `rcx = rdx + ([this+0x48] - [[this+0x18]+0xF4])`, `edx = r8d`, then `jmp target`. |
| `NativeAdapter.RelativeMemberAddressTailCall64` | 19 | `0x005CA350` | The same relative address with the 64-bit `r8` kept as `rdx` and `r9d` moved to `r8d`, then `jmp target`. |
| `NativeAdapter.SecondArgumentConstTailCall` | 12 | `0x0024ACE0` | `mov edx, imm; jmp target`. |
| `NativeAdapter.SecondArgumentZeroTailCall` | 13 | `0x0025E3F0` | `xor edx, edx; jmp target`. |
| `NativeAdapter.SetneFirstArgTailCall` | 5 | `0x00291D70` | `ecx = (ecx != 0)`, then `jmp target`. |
| `NativeAdapter.StaticAddressTailCall` | 2948 | `0x00160310` | `lea rcx, [static]; jmp target`: passes a static's address. |
| `NativeAdapter.StaticPointerTailCall` | 298 | `0x0017E520` | `mov rcx, [global]; jmp target`: passes a pointer global. |
| `NativeAdapter.ThirdArgumentZeroTailCall` | 10 | `0x0025A690` | `xor r8d, r8d; jmp target`. |
| `NativeAdapter.VtableInstallTail` | 400 | `0x00212C50` | `lea rax, [vtable]; mov [rcx], rax; jmp target`: installs a vtable, then tail-calls. |
| `NativeAdapter.ZeroFirstArgTailCall` | 16 | `0x002A2BF0` | `xor ecx, ecx; jmp target`. |
| `NativeAdapter.ZeroSecondArgTailCall` | 4 | `0x002DF610` | `mov r8d, edx; xor edx, edx; jmp target`: shifts the second argument to the third and passes 0 as the second. |

### Adapters that call one function and pass its result on

| Family | Members | Example | Body |
|---|---|---|---|
| `FrameAdvanceContinuation` | 51 | `0x003D9000` | Calls `0x002F2530(this)`; when it returns non-zero calls a second function on `this`; returns the first result. |
| `NativeAdapter.BoolArgFetchResultTail` | 7 | `0x0017F720` | Saves `ecx != 0`, calls a getter, then `jmp target(result, saved bool)`. |
| `NativeAdapter.ByteSaveSecondArgResultTailCall2` | 5 | `0x0017F650` | Saves the low byte of `ecx`, calls a getter, then `jmp target(result, saved byte)`. |
| `NativeAdapter.CallBoolNormalizeReturn` | 6 | `0x001803D0` | Calls a function and returns `al != 0` as 0 or 1. |
| `NativeAdapter.CallBoolNormalizeReturnSete` | 15 | `0x002FFED0` | Calls a function and returns `eax == 0` as 0 or 1. |
| `NativeAdapter.CallResultArgShiftTailCall` | 9 | `0x0017FB90` | Saves `ecx` and `edx`, calls a getter, then `jmp target(result, ecx, edx)`. |
| `NativeAdapter.CallResultField32Getter` | 21 | `0x0017D340` | Calls a getter and returns the dword at a fixed offset in its result. |
| `NativeAdapter.CallResultMarshal24Bytes` | 16 | `0x005A3CE0` | Calls a function with `rcx = rdx` and copies 24 bytes of its result to the pointer in `r8`. |
| `NativeAdapter.CallResultMarshalCompositeRecord` | 19 | `0x00867040` | Calls a function with `rcx = rdx` and copies fields `+0x08` to `+0x20` (qword, qword, dword, byte, dword) of its result to the record in `r8`. |
| `NativeAdapter.CallResultTailCall` | 72 | `0x0017E220` | Calls a getter, then `jmp target` with its result as `rcx`. |
| `NativeAdapter.CallResultWithSavedIntTailCall` | 38 | `0x0017D940` | Saves `ecx`, calls a getter, then `jmp target(result, saved ecx)`. |
| `NativeAdapter.CallResultWithSavedThisTailCall` | 15 | `0x0017F190` | Saves `rcx`, calls a getter, then `jmp target(result, saved rcx)`. |
| `NativeAdapter.CallThenReturnZero` | 21 | `0x005A0D20` | Calls one function and returns 0. |
| `NativeAdapter.CallThenTailCall` | 20 | `0x0017D650` | Calls one function, then `jmp` to another. |
| `NativeAdapter.ChainedMemberResultTailCall` | 7 | `0x00340230` | Calls `0x00263F10(rdx)`, a member function on that result, then `jmp 0x0026B4E0(this, result)`. |
| `NativeAdapter.ConstFirstArgumentCallTailCall` | 7 | `0x00295CA0` | `ecx = imm`, calls one function, then `jmp` to another. |
| `NativeAdapter.DoubleSelfInvoke` | 6 | `0x001F40F0` | Calls `0x0067F580(this)` twice. |
| `NativeAdapter.EHCallWrapper` | 11 | `0x00199D30` | An exception-frame prologue (`[rsp+0x20] = -2`) around one call with the incoming arguments. |
| `NativeAdapter.FanoutFieldUpdate4` | 5 | `0x0050C450` | Calls one function on `this`, then three field-object functions on `this+off` with the saved `edx`, and returns the address of a later field. |
| `NativeAdapter.FanoutFieldUpdate5` | 4 | `0x005324C0` | Calls one function on `this`, then four field-object functions on `this+off` with the saved `edx`, and returns the address of a later field. |
| `NativeAdapter.FixedPipelineCallResult` | 5 | `0x00271420` | Calls `0x0036C1D0(3, 0xF)`, `0x0036A100(ecx)`, `0x0036C140()`, and returns the middle call's result. |
| `NativeAdapter.ForwardSecondArgumentCallReturnTrue` | 50 | `0x005A3420` | Calls a function with `rcx = rdx` and returns 1. |
| `NativeAdapter.MemberArgumentEHCallWrapper` | 12 | `0x001A28B0` | The same frame around one call with `rdx = [this+0x18]`. |
| `NativeAdapter.NamedRecordRegisterPair` | 7 | `0x00862E90` | Calls `0x001FB840` with one string, then `jmp 0x0020E630` with a second string and the saved `ecx`. |
| `NativeAdapter.SavedFourArgCallResultCall` | 6 | `0x001816F0` | Saves four arguments, calls a getter, then calls a second function with the result and the four arguments (the fourth on the stack). |
| `NativeAdapter.SharedGetterThreeArgTailCall` | 6 | `0x001DBAC0` | Saves three arguments, calls `0x00210B30`, then `jmp target(result, arg1, arg2, arg3)`. |
| `NativeAdapter.SmallRecordVtableCtor` | 8 | `0x001F17B0` | Calls `0x00212CC0(this)`, stores `edx` at `+0x18`, installs a vtable and returns `this`. |
| `NativeAdapter.StackConstOneCall` | 5 | `0x00272F60` | Stores a constant (0 or 1) as the fifth argument and calls one function. |
| `NativeAdapter.TwoSubobjectInvokeTailCall` | 6 | `0x00219470` | Calls one function on two member sub-objects of `this`, then `jmp` to another on `this`. |

### Guarded and conditional adapters

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.BooleanSelectedCallReturnTrue` | 10 | `0x0062EE00` | Calls one of two functions on `rdx`, chosen by the byte in `r8b`, and returns 1. |
| `NativeAdapter.CallResultDualTailDispatch` | 8 | `0x00340B90` | Calls `0x00267E10(r9)` and jumps to one of two functions chosen by whether the result is zero. |
| `NativeAdapter.ChainPredicateReleaseTail` | 5 | `0x005DD5E0` | Calls a predicate on `this`; when true calls a second function on `this`; then jumps to a third on `this`. |
| `NativeAdapter.ConditionalDoubleCallResultTailCall` | 9 | `0x0017F040` | Saves `ecx`; calls a getter, and when non-null calls it again and jumps to `target(result, saved ecx)`. |
| `NativeAdapter.DoubleCallResultTailCallSavedThis` | 5 | `0x00182310` | Saves `rcx`; calls a getter, and when non-null calls it again and jumps to `target(result, saved rcx)`. |
| `NativeAdapter.DynamicOffsetRefFlagCall` | 5 | `0x005CA3E0` | Returns 5 when bit 31 of `r9d` is set; otherwise sets it, calls a function on `rdx + ([this+0x48] - [[this+0x18]+0xF4])` and returns 0. |
| `NativeAdapter.FirstMemberInvokeFieldStore` | 7 | `0x0029F100` | When the pointer at `this+off` is non-null, calls a function on it and then clears the field. |
| `NativeAdapter.FlagByteConditionalOp` | 4 | `0x005CE800` | When the byte at `rdx+8` is non-zero, calls `0x005CDAA0(3, string)`; when the pointer at `rdx+0x20` is non-null, calls `0x006108C0` on it; returns 1. |
| `NativeAdapter.FlagGatedInitTailCall` | 7 | `0x00227460` | When one bit of the dword `0x01FD46D4` is clear, calls `0x00226BE0(imm, 0, 0, 0, -1, -1)` and jumps to `0x00226280`. |
| `NativeAdapter.GlobalGuardIndexedCall` | 4 | `0x00226180` | When one bit of the dword `0x01FD46D4` is set, calls `0x00225CD0(imm, -1)` and jumps to `0x00226280`. |
| `NativeAdapter.GuardedCallResultBoolInvert` | 6 | `0x005113A0` | Calls `0x00280120`; when non-zero returns 0, else calls a function and returns `eax == 0`. |
| `NativeAdapter.GuardedPairInvokeFieldStore` | 11 | `0x0044BA80` | Calls `0x002F2D60(this)`; when non-zero calls a function on `this`, then `0x0044B960`, stores its result in a field and returns 1. |
| `NativeAdapter.GuardedRecordBuildCookie` | 4 | `0x005571F0` | Under a stack cookie: when a field of `this` is zero, builds a stack record, calls `0x00244F50`, stores the result in that field and passes it to `0x00246AD0`. |
| `NativeAdapter.GuardedSharedPairTailCall` | 9 | `0x00511510` | Calls `0x00280120`; when zero calls `0x00267E10(r9)` and jumps to a function with that result. |
| `NativeAdapter.HandleRecordOutFloatInit` | 4 | `0x002E9A90` | Resolves the argument with `0x003588B0`, follows `+0xC0` into the same `0x740`-stride table, calls a function on the out record in `rdx` when `+0x284` is set, zeroes its first 12 bytes when the handle or record pointer is missing, and always stores 1.0 at its `+0xC`. |
| `NativeAdapter.IndexedRecordStoreCookie` | 4 | `0x00227E20` | Under a stack cookie: builds a stack record holding the sign-extended argument and calls `0x00244F50(imm, code address, record)`. |
| `NativeAdapter.NullableCallChainTailCall` | 19 | `0x0017CFD0` | Calls a getter; when it returns non-null, calls it again and jumps to a second function with that result. |
| `NativeAdapter.NullableFetchByteTail` | 4 | `0x0017F5B0` | Saves the low byte of `ecx`; calls a getter, and when non-null calls it again and jumps to `target(result, saved byte)`. |
| `NativeAdapter.NullableRecordWordTail` | 4 | `0x002E8B60` | When `this`, the pointer at `+0xC0` and its dword are valid (not null, not -1), jumps to a function with the record's word in `ecx`. |
| `NativeAdapter.OutRecordMemberCallTailCall` | 5 | `0x0042DCA0` | Calls `0x00426220(this, [rdx+8])`; when it returns 0, jumps to a function on `this`. |
| `NativeAdapter.PredicateGuardConstCall` | 4 | `0x00347C60` | Calls a predicate; when non-zero calls `0x00314D40(imm)` and returns 1, else returns 0. |
| `NativeAdapter.PredicateGuardSharedCall` | 4 | `0x0044A5F0` | Calls `0x002F2D60(this)`; when non-zero calls a function on `this` and returns 1, else returns 0. |
| `NativeAdapter.RefFlagSetCallZero` | 5 | `0x005CA2B0` | When bit 31 of `r8d` is clear, sets it and calls a function; returns 0. |
| `NativeAdapter.TableIndexDispatchSetFlag` | 8 | `0x002E7450` | The same resolution; when `+0x284` is non-zero calls a function on the record and sets bit `0x800` of its `+0x290`. |
| `NativeAdapter.TableIndexDispatchTailCall` | 5 | `0x002E5BC0` | Resolves the word at `[[this+0xC0]]` through the record table whose base is the qword `0x022C6F28` (stride `0x740`) and jumps to a function when the record's dword `+0x284` is non-zero. |
| `NativeAdapter.TripleMemberChainReturnTrue` | 6 | `0x005CF750` | Calls a predicate on `rdx`; when true calls a second function on `rdx`; always calls a third on `rdx`; returns 1. |
| `NativeLeaf.NullableGlobalClearCall` | 5 | `0x00366A00` | When a pointer global is non-null, calls a function on it and then zeroes the global. |
| `NativeLeaf.StaticHandleReplaceWithPreRelease` | 12 | `0x00238390` | Frees the handle in a global through `0x003844F0` when it is non-null, then stores the sign-extended argument there. |

### Adapters over an argument record

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.FloatFetchPushForward` | 4 | `0x00342040` | Calls a float getter on `rdx`, passes the float to `0x00267F60(r9)`, then jumps to a function with the four original arguments. |
| `NativeAdapter.PopIntForwardTail` | 4 | `0x00342340` | Reads an integer from the record in `r9` with `0x00267E10`, passes it through one function and jumps to another with the result. |
| `NativeAdapter.PopThreeFloatGuardTail` | 4 | `0x00340D00` | Reads three floats with `0x00267DB0` and an integer with `0x00267E10`, calls `0x0016D6A0` and `0x003EB700` on the integer, then jumps to a function with the result and the three floats. |
| `NativeAdapter.PopThreeIntForwardTail` | 4 | `0x00348C50` | Reads three integers with `0x00267E10`, passes the last through `0x00264010` and `0x00263F10`, then jumps to a function with that result and the first two. |
| `NativeAdapter.SharedNormalizeTailCallOne` | 6 | `0x0034B450` | Calls `0x0026A1A0(rdx, 1)`, restores the four arguments and jumps to a function. |
| `NativeAdapter.SharedNormalizeTailCallZero` | 6 | `0x00341390` | Calls `0x0026A1A0(rdx, 0)`, restores the four arguments and jumps to a function. |
| `NativeAdapter.TwoSharedComposeTailCall` | 6 | `0x00340DC0` | Calls `0x002640C0`, reads an integer with `0x00267E10(r9)`, then jumps to a function with both. |

### Out-record initialisers

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.NullableOutRecordHeaderInitReturnTrue` | 9 | `0x005CE010` | When `rdx` is non-null writes a constant qword (a different one per member) and two zero qwords there; returns 1. |
| `NativeAdapter.NullableOutRecordVptrCall` | 5 | `0x0063F2A0` | When `rdx` is non-null calls a function on it and installs a vtable at `+0`; returns 1. |
| `NativeAdapter.OutRecordDescriptorInitReturnTrue` | 19 | `0x00866FA0` | When `rdx` is non-null writes three addresses at `+0`, `+8`, `+0x10`, zeroes `+0x18` and `+0x1C`, and stores 1.0 at `+0x20`; returns 1. |
| `NativeAdapter.OutRecordVtablePairStore` | 7 | `0x0063EF60` | When `rdx` is non-null calls a function on it and stores two addresses at `+0` and `+8`; returns 1. |
| `NativeAdapter.OutRecordZeroInitMemberInit` | 7 | `0x005CFF00` | When `rdx` is non-null clears `0x90` bytes there with `memset` (`0x00861EC0`) and calls an initialiser on it; returns 1. |
| `NativeLeaf.TaggedOutRecordFloatVcall` | 5 | `0x006B3120` | Advances the cursor in the fifth argument by 8, converts the double there to float, calls `[this+8](rdx, float)`; when the third argument equals `0x006B0B20()` with bit 0 set, stores the result at `out+8`, zeroes `out+0` and returns 1, else 0. |

### Construction, destruction and static lifetime

| Family | Members | Example | Body |
|---|---|---|---|
| `CompilerGeneratedCpp.GuardedStaticObjectTeardown` | 28 | `0x008B0E20` | Calls `0x0016D6A0` (`ret 0`) with a static's address and returns. |
| `CompilerGeneratedCpp.StaticContainerTeardown.IndirectAllocator` | 60 | `0x008A69F0` | When a static container holds more than one byte and a non-null begin, returns the storage through slot 3 of its allocator object. |
| `CompilerGeneratedCpp.StaticZeroInitObjectInitializer` | 11 | `0x00169A10` | Clears a `0x50`-byte static with `memset`, constructs its lock with `0x007DF6D0`, and registers its teardown with `atexit` (`0x00808B90`). |
| `CxxObjectLifecycle.ConditionalTeardownReturnTrue` | 29 | `0x00611A10` | When `rdx` is non-null calls a destructor on it; returns 1. |
| `CxxObjectLifecycle.DeletingDestructor.AlignedOrGuardedFree` | 196 | `0x005AC810` | Deleting destructor: calls the destructor; when flag bit 0 is set frees `this` with `0x00584730`, or, when bit 2 is also set, calls `0x0016D6A0(this, size)`; returns `this`. |
| `CxxObjectLifecycle.DeletingDestructor.VtableAlignedOrGuardedFree` | 14 | `0x0017CC70` | The same deleting destructor with a vtable install before the destructor call. |
| `CxxObjectLifecycle.DerivedConstructorVtableInstall` | 27 | `0x001F1740` | Calls the base constructor on `this`, installs the derived vtable, returns `this`. |
| `CxxObjectLifecycle.VtableInstallStub` | 42 | `0x0018D0E0` | `lea rax, [vtable]; mov [rcx], rax; ret`. |
| `DeletingDestructor.SharedTeardown` | 1185 | `0x00584870` | The vtable-installing deleting destructor whose destructor call is always `0x00633390`. Same instruction form as the previous family. |
| `Platform.Windows.CriticalSectionStaticInitializer` | 19 | `0x00169690` | `InitializeCriticalSection` (IAT `0x008C20B0`) on a static, then registers its teardown with `atexit`. |
| `Runtime.NamedRegistryRecord.StaticInitializer` | 60 | `0x0015C510` | Calls `0x005DC6F0(static, string, 0)`, then registers its teardown with `atexit`. |
| `Runtime.NameRegistryEntry.StaticInitializer` | 56 | `0x00162430` | Calls `0x005FDCB0` with a static's address, then registers its teardown with `atexit`. |
| `Runtime.Singleton.LazyAllocatorInitializer` | 13 | `0x0019CDE0` | When a pointer global is null, allocates a fixed size with `0x00210EC0`, constructs the object in it, and stores the pointer. |
| `Runtime.Singleton.StaticObjectFixupRegisterRelease` | 19 | `0x008AF570` | Installs a vtable in a static; when a link static does not point at itself, calls slot `0x48` of the object in another static; calls `0x006B6700` on a member static; frees a buffer with `0x00584730` when bit 0 of a flag byte is set. |

### Owned buffers and allocator releases

| Family | Members | Example | Body |
|---|---|---|---|
| `Runtime.Container.OwnedBufferAlignedFreeResetReturnTrue` | 11 | `0x005C3430` | On `rdx`: when bit 31 is clear and the count is above 1, frees `+8` with `0x00584730`; zeroes both; returns 1. |
| `Runtime.Container.OwnedBufferReset` | 25 | `0x001B6EA0` | When bit 31 of the count word at `+0` is clear frees the pointer at `+8` with `0x00584730`; zeroes both. |
| `Runtime.Container.OwnedBufferTeardownResetReturnTrue` | 13 | `0x005C31D0` | On `rdx`: when bit 31 is clear calls a teardown with the pointer and the count; zeroes both; returns 1. |
| `Runtime.Container.SpanCheckMemberVcall` | 6 | `0x001AAD20` | When the span `[this] .. [this+0x10]` holds more than one byte and begins non-null, calls slot 3 of the object at `this+0x18`. |
| `Runtime.Memory.IndirectAllocatorRelease` | 22 | `0x00185070` | When `[this]` is non-null, returns the span `[this] .. [this+0x10]` (masked to the element alignment) through slot 3 of the allocator object at `this+0x18`. |

### Virtual and indirect dispatch

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.DualLookupIndirectCallback` | 13 | `0x005C2060` | Calls two lookups on `rdx`; when the second is non-null calls the function at `[this+8]` with both results; returns 0. |
| `NativeAdapter.TwoMemberCallIndexedVcall` | 7 | `0x0063A300` | Calls two functions on `rdx`; when the second is non-null calls `[this+8]` with `rcx = result + [this+0x10]`; returns 0. |
| `NativeDispatch.GlobalHandlerSlotTailCall` | 25 | `0x004174F0` | Loads a handler global; when set, jumps to it with `rdx = rcx` and `rcx = [r8+0x2E0]`. |
| `NativeDispatch.MemberVirtualTailCall` | 28 | `0x00726DB0` | `mov rcx, [rcx+off]; mov rax, [rcx]; jmp [rax+slot]`. |
| `NativeDispatch.NullableVirtualTailCall` | 11 | `0x0017F0C0` | Returns when `rcx` is null; otherwise `jmp [[rcx]+slot]`. |
| `NativeDispatch.VirtualTailCall` | 14 | `0x00616E24` | `mov rax, [rcx]; jmp [rax+slot]`. Same instruction form as the fixed-slot adapters; held as a pointer in a vtable or a pointer table. |
| `Runtime.VirtualDispatch.FixedSlotAdapter` | 20 | `0x00616E0C` | `mov rax, [rcx]; jmp [rax+slot]`. Same form as the virtual tail calls; its address is taken only by an installer's `lea`, and it is never called directly or held as a pointer in the image. |

### Loops, walks, lookups and table reads

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.BitfieldOrNodeWalk` | 9 | `0x001A20A0` | Initialises a record in `this` (zeroes `+0` to `+0x1B`, `+0x20` = `rdx+0x38`, `+0x28` = the list's first node, `+0x30` = a table address), steps it with `0x001B7CE0` until that returns true, then calls `0x001AA0A0`; returns `this`. |
| `NativeAdapter.CountedLoopMemberInvoke` | 5 | `0x0062B020` | For each index below the count at `+0x18` (bit 31 masked, at least 1), calls `0x005CCB80(1)` while a lookup's dword is positive. |
| `NativeAdapter.GlobalSlotFlagClearOps` | 4 | `0x003302B0` | Clears bit 13 of the qword `table[ecx]`; when no bit but bit 0 remains, calls `0x00263FF0(ecx)` and clears bit 3 of the byte at its `+0x11`; when a non-zero slot became zero, calls `0x0032F1B0(ecx)`. |
| `NativeAdapter.MallocRecordEmplaceTailCall` | 7 | `0x0018B5D0` | Allocates `0x20` bytes through `0x0085E730` (`malloc`), constructs a record with `edx`, appends its pointer to the vector in `this` (end `+8`, capacity `+0x10`, grown by `0x001AB570`), then jumps to `0x0018AFF0(0x0018B4E0(), record)`. |
| `NativeAdapter.MemberPredicateTreeSearch` | 6 | `0x00219E30` | Walks the circular list at `this+8` calling a predicate on each node's `+0x10` with the three other arguments; returns 1 at the first true, else 0. |
| `NativeLeaf.BoundedTableWordLookup` | 5 | `0x0032F260` | When `ecx` is within a bound, takes a row pointer from a table; when the row's first byte is non-zero returns its dword at `+8 + edx*8`, else -1. |
| `NativeLeaf.ClampedIndexTableStore` | 4 | `0x002E2050` | Stores `edx` into entry `ecx` of a table (fixed stride); a negative index stores into entry 0, an index at or above the bound stores nothing. |
| `NativeLeaf.ClampedTableLookup` | 7 | `0x0035EE50` | Returns 0 when `ecx` is at or above a bound; otherwise takes row `ecx` (stride `0x294`), wraps `byte [row+1] + edx` into 0 to 15, and returns the word at `+0x4A` of that 36-byte entry. |
| `NativeLeaf.ListStringCompare` | 4 | `0x005C5250` | Walks a global chain (next at `+8`) comparing each node's name at `+0` with the argument; returns the node or 0. |
| `NativeLeaf.RecursiveListVcallWalk` | 5 | `0x001A48C0` | Recurses into `[node]`, then calls slot 3 of the object at `this+0x30` with `(node, 0x38)`, moving to `[node+8]` until null. |
| `Runtime.Container.RecursiveSpanNodeWalk` | 7 | `0x001A4B50` | The same recursive walk with node size `0x40`, which also returns each node's own span `[node+0x20] .. [node+0x30]` through slot 3 of the allocator at `node+0x38`. |
| `Runtime.Container.StringKeyedChainAttach` | 11 | `0x006B8D20` | Returns `0x11` when the name at `+8` is null; walks a global chain comparing names byte by byte; returns `0x12` on a match, else links `this` at the head and returns 0. |
| `Runtime.Registry.StringLookup` | 10 | `0x006C04C0` | Walks a global chain (next at `+0x10`) comparing each node's name at `+8` with the argument; returns the node or 0. |
| `Runtime.SerialRangeInvokeLoop` | 7 | `0x0030DCB0` | For every id of one class, `0x1000 * class + i` below the class count, calls `0x003008A0(id, 0x63, 0, 1, 0)`. |

### Large bodies

| Family | Members | Example | Body |
|---|---|---|---|
| `NativeAdapter.RecordChainDoubleResolve` | 4 | `0x00429A50` | Under a stack cookie: resolves a word id through the `0x740`-stride table, checks each hop with `0x00426220`, follows the record's `+8` word the same way, and calls `0x0042EF90` for the words at `+8` and `+0xA`. |
| `NativeAdapter.RecordFieldCopy` | 5 | `0x0068C260` | Calls a getter with `rcx = rdx` and copies its fields from `+8` onward to the record in `r8`, field by field. |
| `NativeLeaf.FloatBankGlobalPublish` | 4 | `0x004630D0` | Copies the vector at `this+0x60` into a bank of float globals (adding each lane to a base), stores `this` in a global, then continues through `0x0039AF70`, `0x00398F90` and others. |
| `NativeLeaf.LargeFloatGlobalPublish` | 4 | `0x00452020` | Under a stack cookie: copies a record with `0x00430B90` into `this+0x110`, publishes it to a bank of float globals, then runs a long sequence of fixed calls. |
| `NativeLeaf.SlideTableRecordCopyInvoke` | 10 | `0x002EFE70` | Two word globals select two 16-byte slots of a global record array; copies a 16-byte record and an 8-byte tail between them, advances the counters, and calls the function in `rcx`. |

### Reflection descriptor adapters

| Family | Members | Example | Body |
|---|---|---|---|
| `Reflection.OwnedBufferResetAdapter` | 46 | `0x005A4830` | On `rdx`: when bit 31 of the count word at `+0` is clear and the pointer at `+8` is non-null, frees it with `0x00584730`; zeroes both; returns 1 (59 bytes). |
| `Reflection.ReturnValueAdapter` | 403 | `0x00584780` | `push rbx; sub rsp, 0x20; mov rcx, rdx; mov rbx, r8; call target; mov [rbx], rax; ...; ret` (26 bytes): calls the target with the second argument and stores the returned pointer through the third. |


## Related

- [Global state accessors](../Engine-Core/global-state-accessors.md): the one-instruction
  getters of globals, counted over the whole image.
- [Jump thunks](../Engine-Core/jump-thunks.md): the one-jump forwarders and the `ret 0`
  stub `0x0016D6A0`.
- [Vtable methods](../Engine-Core/vtable-methods.md): every virtual slot with its class.
- [Debug logging](../Engine-Core/debug-logging.md): the log call `0x005CDAA0` one family
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
