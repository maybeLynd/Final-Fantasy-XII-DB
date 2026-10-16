---
title: "Thunks and import stubs: jump forwarders, argument-adjusting tail calls, import stubs and the import table"
kind: "system"
category: "Compiler and C runtime"
addresses: "008C2000, 01DEAB00, 00861E90, 00808888, 0080F2BC, 00861EAE, 00861EB4, 00861ED8, 00809958, 008C31C0, 00313F60, 00377C20, 00291D40, 0028E8B0, 002BE020, 0028FB40, 005A5850, 0016D6C0, 002A2BF0, 0025E3F0"
---

## What the player sees

Nothing. These are the seams where the compiler and linker joined code together. They matter to
anyone who hooks a function or counts its callers, because one body can be reached under two or more
addresses.

## How it works

### The import table

The import directory (`01DEAB00`) describes 30 DLLs and 538 imported names. The loader writes their
addresses into the import address table, `008C2000` to `008C31C0` (`.idata$5`), one qword per name
and a zero qword after each DLL's run. Code reaches an import in one of three ways:

- `call qword ptr [slot]`: 3,543 sites. 530 of the 538 slots are called or jumped through this way.
- `jmp qword ptr [slot]` at the end of a function: 139 tail jumps; the other 120 of the 259
  `FF 25` jumps are the stubs below.
- `call stub`, where the stub is a function whose whole body is `jmp qword ptr [slot]`: 3,348 call
  sites and 147 jump sites, through 120 stubs.

Eight slots are never called or jumped through. Six are data exports of `MSVCP140.dll` read as
data: four locale facet ids, `std::_BADOFF` and `std::cout`. The other two, `SymGetModuleBase64`
(`008C3100`) and `SymFunctionTableAccess64` (`008C3108`), are loaded as values (`005CCE88`) and passed
to the stack walker of the crash-dump writer. Which DLL supplies which service is on
[runtime-services.md](runtime-services.md).

### Import stubs

An import stub is six bytes, `FF 25 disp32`, or seven, `48 FF 25 disp32`; the image has 111 and 9.
The 120 stubs name 117 slots: three stubs share the `free` slot `008C2B48` and two the `malloc` slot
`008C2B40`. They sit in three runs and twelve single places:

| Where | Stubs | Contents |
|---|---:|---|
| `00861E90` to `00862082` | 84 | CRT, `VCRUNTIME140` and maths imports, packed six bytes apart |
| `00808888` to `008088FA` | 20 | 19 `MSVCP140` stream-buffer and facet virtuals, then `DirectInput8Create` |
| `0080F2BC` to `0080F2CE` | 4 | `MiniDumpWriteDump`, `D3D11CreateDevice`, `D3D11CreateDeviceAndSwapChain`, `CreateDXGIFactory` |
| single | 12 | for example `0019C590` (`free`), `0085E730` (`malloc`), `007911D0` (`D3DReflect`) |

- 26 stubs have their address held in data. The 19 `MSVCP140` stubs of the second run are virtual
  functions of stream buffers and facets: `0080889A` (`basic_streambuf<char>::showmanyc`) is slot 5
  of the vtables of `basic_filebuf<char>` (`008F3EC8`), `basic_stringbuf<char>` (`00900F20`) and a
  JsonBox output filter (`00905070`).
- `00861EB4` (`__CxxFrameHandler3`) and `00861ED8` (`__C_specific_handler`) are named by RVA in
  unwind records, and `00861EAE` (`__std_terminate`) is the target of 86 exception-cleanup pads; see
  [exception-handling.md](exception-handling.md).
- The stubs come from 18 DLLs: `api-ms-win-crt-math` 34, `MSVCP140` 20, `api-ms-win-crt-runtime`
  16, `VCRUNTIME140` 13, `api-ms-win-crt-heap` 9, `api-ms-win-crt-string` 7, `KERNEL32` 5, `IMM32`
  3, two each from `d3d11`, `XINPUT9_1_0` and `api-ms-win-crt-stdio`, and one from each of seven
  more.

The member list `thunks-and-import-stubs-external-import-stubs.tsv` holds 117 of the 120 and
`thunks-and-import-stubs-external-import-stubs-map.tsv` gives the DLL and name of each; the three it
leaves out are `00861EAE` (`__std_terminate`), `00862028` (`_exit`) and `00862034` (`_c_exit`).

### The guard-check stub

`00809958` has the import-stub form, `48 FF 25`, but its slot is `008C31C0`, the first qword after
the import table. That slot is the load configuration's guard-check function pointer, and on disk it
holds `0016D6A0`, a `ret 0`. Eleven call sites in the runtime's support routines call it just before
an indirect call, among them the vector constructor and destructor iterators (`0080901D`,
`008090A2`). The slot is on [image-hardening.md](image-hardening.md).

### Jump forwarders

A forwarder is a body that is exactly one `jmp rel32` into `.text`, followed by `int3` padding or by
another start. It sits at a `.pdata` begin, or right after an `int3`, a `ret` or another `jmp rel32`.
It is itself a start: a `.pdata` begin, the target of a `call` or `jmp rel32`, a qword in `.rdata`
or `.data`, the target of a rip-relative `lea`, or an `E9` right after `int3` padding. The terminate
pads, which jump to `00861EAE`, are not forwarders.

By this rule the image has 763 forwarders with 763 distinct targets; 33 of the targets are
themselves forwarders. Each forwarder is counted once, in the first row that fits:

| Reached by | Forwarders |
|---|---:|
| a direct `call` | 234 |
| its address held as a qword or taken by `lea`, and no call | 404 |
| only a `jmp` from another function | 113 |
| nothing | 12 |

384 forwarders are held as a qword at all, 26 are taken by `lea`, and 158 are jumped to at all. The
twelve that nothing reaches are `006DAA00`, `006DAA10`, `006DAA20`, `006DAA30`, `006DAA40`,
`006DF270`, `006DF280`, `007122F0`, `00719360`, `00719370`, `00809930` and `00809940`.

So 751 forwarders are reached by something. `0017CDE0` is one of them: it is the qword at `008C5788`,
slot 5 of the `GameApplication` vtable `008C5760`, and the `lea` at `00298290` takes it.

The terminate pads are 86 bodies of `jmp 00861EAE`. 85 are packed back to back from `008A26E4` to
`008A508D`. The 86th, `008A5B1F`, stands alone after the `ret` of a funclet that ends at `008A5B1E`.

[Jump thunks](../Engine-Core/jump-thunks.md) tabulates 568 of the forwarders and 85 of
the terminate pads with their callers and targets. The member list
`thunks-and-import-stubs-internal-tail-call-forwarders.tsv` holds 749 rows. The 14 forwarders it
leaves out are the twelve that nothing reaches and `0026DC50` and `0036E9A0`, which are reached
only by jumps.

### Tail calls that change an argument

Some one-jump functions change a register before they jump, so they are not interchangeable with
their target:

| Body | Bytes | Count | Effect |
|---|---:|---:|---|
| `mov rcx, rdx ; jmp T` | 8 | 102 | `T` gets the second argument as its first; 101 are reached only by address (`0016D6C0`) |
| `push rbx ; … mov rcx,rdx ; mov rbx,r8 ; call A ; mov rdx,rax ; mov rcx,rbx ; … jmp B` | 33 | 87 | returns `B(arg3, A(arg2))`; all reached only by address (`005A5850`) |
| `xor ecx, ecx ; jmp T` | 7 | 16 | first argument forced to 0 (`002A2BF0`) |
| `xor edx, edx ; jmp T` | 7 | 13 | second argument forced to 0 (`0025E3F0`) |
| `mov rcx, [0209BE80] ; add rcx, imm ; jmp T` | 19 | 5 | calls `T` on a sub-object of the object `0209BE80` points to |

The five receiver binders are `0028E220` (`+0x8FA0`, to `002BDCE0`), `0028E860` (`+0x7EA0`, to
`0028CA30`), `0028E8B0` (`+0x8FA0`, to `002BE020`), `0028FB40` (`+0xA0`, to `003F8D20`) and `0028FB60`
(`+0x5380`, to `0028A080`).

The member lists `thunks-and-import-stubs-forward-second-argument-tail-calls.tsv` (72 entries) and
`thunks-and-import-stubs-call-result-then-tail-call-adapters.tsv` (29 entries) hold part of the first
two rows. `thunks-and-import-stubs-thunk-address-taken.tsv` lists 297 one-jump functions whose
address appears in a qword or a `lea`, with the section of each reference.

### Why caller counts disagree

A forwarder and its target are two names for one body, so a caller count depends on which name it
counts and whether a jump counts as a call. `00313F60` is `jmp 00377C20`:

- 67 call sites name `00313F60`;
- 79 call sites name `00377C20`, and one jump does: the forwarder's own;
- so 146 call sites reach the body. A tool that folds the forwarder into its target reports 146 for
  `00377C20`; one that counts instructions reports 79 calls and one jump.

A chain can also change a register on the way. `00291D40` is `jmp 0028E8B0`, and `0028E8B0` loads
`[0209BE80]`, adds `0x8FA0` and jumps to `002BE020`. Its six callers therefore reach `002BE020` with a
different `rcx` from the one they passed, while the four call sites that name `002BE020` directly
pass their own.

## Layouts

`ImportDescriptor` (`0x14` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | lookupTable | RVA of the name-lookup qwords (.idata$4) |
| `04` | `u32` | timeStamp | 0 |
| `08` | `u32` | chain | forwarder chain |
| `0C` | `u32` | name | RVA of the DLL name |
| `10` | `u32` | firstThunk | RVA of the DLL's first slot in the import address table |

`ImportStub` (`0x6` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8[2]` | opcode | FF 25 |
| `02` | `i32` | disp | slot address minus the address of the next instruction |

The seven-byte form puts a `48` prefix before `FF 25`, and its displacement counts from `+7`.

`JumpForwarder` (`0x5` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | opcode | E9 |
| `01` | `i32` | disp | target minus (forwarder + 5) |

## Shipped data

| Fact | Value |
|---|---|
| imported DLLs and names | 30 DLLs, 538 slots, `008C2000` to `008C31C0` |
| largest suppliers | `MSVCP140` 115, `KERNEL32` 110, `USER32` 59, `api-ms-win-crt-stdio` 45, `api-ms-win-crt-math` 45 |
| direct uses of slots | 3,543 `call [slot]`, 259 `jmp [slot]` (139 tail jumps, 120 stubs) |
| import stubs | 120 (111 six-byte, 9 seven-byte), plus `00809958` on the guard slot |
| jump forwarders | 763, all to different targets; 751 reached by something |
| terminate pads | 86 `jmp 00861EAE`, 85 packed from `008A26E4` to `008A508D` plus `008A5B1F` |
| argument-adjusting tail calls | 102 `mov rcx,rdx`, 87 call-result, 16 `xor ecx`, 13 `xor edx`, 5 receiver binders |

## Modding notes

- To intercept an import everywhere, patch its slot in the import address table. A stub catches only
  the calls that go through it: the 3,543 direct `call [slot]` sites bypass it, and `free` has three
  stubs.
- Patching a five-byte forwarder redirects exactly the callers that use that address and leaves the
  direct callers of the target alone. For a forwarder whose address is held in data or taken by
  `lea` (404 are reached no other way), the forwarder is also the entry that calls through that pointer use.
- Before treating a short tail call as a pure forward, read its first instruction: the families in
  the table above change `rcx` or `rdx`, and a hook placed after them sees the changed value.
- State which convention a caller count uses: call instructions only, calls and jumps, or the
  target with its forwarders folded in.

## Related

- [Jump thunks](../Engine-Core/jump-thunks.md): the per-forwarder table with caller counts.
- [Exception handling](exception-handling.md): the handler and terminate stubs and the funclets that
  jump to them.
- [Image hardening](image-hardening.md): the guard-check slot `008C31C0` and `0016D6A0`.
- [Runtime services](runtime-services.md): what the imported DLLs provide.
- [Generated function families](generated-function-families.md): the larger compiler-generated
  shapes, such as static destructors and vtable installers.
- [Maths library](maths-library.md): the 34 maths stubs and their call counts.
- [MSVC containers](msvc-containers.md): the `MSVCP140` imports behind the stream virtuals.
